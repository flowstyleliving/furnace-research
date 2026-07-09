# 🪑 Attention sinks & heads — what we got on 2026-05-15, ELI12

**Rigorous version:** [results/inter-head-disagreement-2026-05-15](../results/inter-head-disagreement-2026-05-15.md)
**Prior-art companion:** [feedback/inter-head-prior-art-2026-05-15](../feedback/inter-head-prior-art-2026-05-15.md) (RAUQ + SinkProbe positioning)

---

## 🎯 The question

When a model is about to say something false, do its **attention heads** look different? You can't watch a model "think" directly, but at each step the attention layer is making a tiny visible decision: each head decides where to look. That's a pattern we can stare at.

## 🧠 The metaphor — a classroom of kids in a circle

Picture **a classroom**. The kids sit in a circle. To decide what to say next, each kid 👶 picks one other kid (or the teacher) to copy. The teacher 🧑‍🏫 stands at the front and is always a little loud, so kids constantly glance at her even when they don't really need to.

- Each kid = one **attention head** at a given layer.
- The kid each one picks = where that head is *attending*.
- The classroom has a few rows of kids stacked back-to-back; each row is one **decoder layer**. The back row (`final`) decides what comes out the door.

### 🌀 What exactly is a "sink"?

A **sink** is a *token position* (not a head, not a layer — a *position* in the input sentence) that ends up soaking up disproportionate amounts of the room's attention even when it has nothing useful to contribute to the current sentence. The teacher 🧑‍🏫 — the **BOS** ("beginning of sentence") token — is the most famous sink, but she's not the only kind.

**Why do sinks even form?** The same reason **eddies form behind rocks in a stream** 🌊. Water has to keep moving — it can't just vanish — so when it hits a fixed obstacle the volume that doesn't make it past curls back and pools. Leaves, foam, bits of debris all accumulate in the eddy even though the eddy itself contributes nothing to the river's downstream flow. Wherever there's a conservation rule (water volume is constant) plus an asymmetric topology (the rock has been there forever), a sink emerges for free. Nobody designs the eddy; the rules make it inevitable.

🐦 **Attention is a flow that has to be conserved**, exactly like water in a stream. Each head's attention is forced to sum to 1.0 — *somebody* gets looked at, no matter what. When a head has no strong reason to look at any particular kid this step, the math still demands it deposit attention *somewhere*. The teacher 🧑‍🏫 is the rock in the stream: she's been there since the room opened (fixed obstacle), every head has seen her many times (the riverbed remembers her), she's the path of least resistance. Pile that decision across many heads × many steps and she ends up with mountains of attention — even when no actual kid in the room needs to hear from her. That's a sink: an eddy in the attention flow.

The same pattern shows up *everywhere* nature has to balance a conserved quantity against an asymmetric layout:
- 🌳 **Carbon sinks** — forests and oceans absorb atmospheric CO₂ faster than they release it, just because the chemistry happens to be one-way.
- 🩸 **Venous return** — blood from every muscle ends up funnelled through two large veins back to the heart, not by any per-cell decision, but because the vessel geometry converges there.
- 🐝 **Trail pheromones** — when a foraging bee doesn't see a great flower, it drops attention on a well-trodden trail even if that trail no longer leads anywhere useful. The trail becomes a behavioral sink.

The BOS sink is the same physics. Nothing designed it; the rules made it inevitable.

Two refinements worth knowing:

- 🌀 **Sinks aren't always BOS.** Sometimes the eddy forms behind a *different* rock — early punctuation, or the first content word in the prompt. BOS is just the most common sink because it's always at position 0.
- 🔊 **A sink only *matters* for the output if it's loud.** A position can soak up enormous attention but contribute nothing if its **value vector** (`V_i`) is small — value vectors are what the head *actually copies* once it picks a position. SinkProbe's load-bearing finding: "the dangerous sinks are the ones with large `‖V‖`." (Carbon sinks matter for climate only when the absorbed carbon stays absorbed; an eddy matters for the river only if it actually traps debris instead of letting it flow through.) That's why we added three V-norm cells today: `v_norm_bos`, `v_norm_max`, `v_norm_lastq_weighted`.

When something works smoothly, certain kids 👧 normally do specific jobs — e.g. **Sarah** always watches the kid to her left, because that kid just said something useful. When the activity is about to go wrong, *Sarah stops watching her neighbor*. She drifts. So do a few other reliable kids. Pretty soon everyone is just dumping attention on the teacher — the sink fills up.

## 📊 What we measured / saw

Three things, each a single number per layer per sample:

1. **🌀 BOS-mass** — *how much of the room is staring at the teacher*. High = compressed, prior-dominated computation.
2. **📣 Cross-kid disagreement (JS-radius)** — *how varied the kids' choices are*. Low = they've all defaulted to copying the teacher; high = they're scattered.
3. **🔊 V-norm of the teacher** — *how loud the teacher is actually being*. SinkProbe's refinement: a sink only matters if her **value vector** (loudness) is big. We added three V-norm metrics this evening.

On 9 models × 200 ANLI R1 samples, we get a **clean (sink-controlled) signal in 7 of 9** models — but not the same metric at the same row in each classroom:

| Model | Where the signal lives | AUROC |
|---|---|---|
| Qwen 2.5 7B (corrected after a bug fix) | row `last-1` 🪞 (NOT the back row) | js_no_bos = 0.82 |
| Phi-3.5-mini | row `last-1` | js_no_bos = 0.77 |
| Phi-4-mini, gemma-3-4b, Mistral 7B, Qwen3-8B, Qwen3-1.7B | various | 0.62 – 0.75 |
| Llama-3.2-3B, Mistral-Nemo | (only the teacher's noise — no clean signal) | — |

Random baseline = 0.5. So 0.82 means "the model can tell the difference 82% of the time."

## ✅ / ❌ / 🎁 What this tells us

- ✅ **Direction is consistent under controls**: when we ignore the teacher (no_bos column), high disagreement → likely hallucination, every time the signal is clean. Earlier, before the fix, we thought low disagreement → hallucination — that was the *teacher-staring shadow*, not a real disagreement signal.
- ❌ **Not a universal detector**: which row of the classroom carries the signal depends on the model. Same lesson as everywhere else — see [calibration-pivot-eli12](calibration-pivot-eli12.md).
- 🎁 **Two famous papers got there first, from different angles** (RAUQ = "watch Sarah specifically", SinkProbe = "watch the teacher specifically"). Our **cross-head disagreement** number was secretly reading both effects mixed together. Splitting them out (no-BOS column + V-norm cells) was the unlock.
- 🎁 **We caught a microphone bug**: on Qwen 2.5, we couldn't hear the back-row kids at all (180 of 200 samples were NaN — `q·kᵀ` overflowed in float16). Switching to a clearer microphone (fp32 cast before the matmul) made them audible. The corrected back-row reading is much weaker than we had reported; the actual signal sits one row forward (`last_minus_1`).

## ⚠️ Caveats

- 🚫 Tiny effective n on the descriptive panel: our original "Qwen 2.5 = 0.92" headline was on 20 samples, not 200, because of the float16 bug. The calibrator's honest CIs caught this immediately — see [v4-candidates #5](research-candidates.md#5-attention-cell-extension-to-pri_calibratorpy)alibratorpy).
- 🚫 Same generation step only (`gen_step=1`) by default; a separate `--attention-multistep` panel covers steps 1-4 if you want post-commit dynamics.
- 🚫 We capture per-call attention *weights* and now V-norms, but we still don't run RAUQ or SinkProbe as full baselines — our scalars are coarser than what their probes consume.

🎯 **Takeaway in metaphor:** the classroom's whisper-noise is real evidence — but **which row to listen to depends on which class you're sitting in**, and there's a megaphone at the front that drowns out a lot of the signal until you turn its volume down.
