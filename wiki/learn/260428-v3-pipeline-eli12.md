# 🕵️ How we ran experiment v3 — end to end, ELI12

**Rigorous version:** [results/v3-main-run](../results/v3-main-run.md) (verdict) + [pri-v3-plan](../pri-v3/pri-v3-plan.md) (the spec)
**Companion (concepts first):** [where-we-are-eli12](where-we-are-eli12.md) · [null-space-eli12](null-space-eli12.md)

---

## 🎯 The question

We *think* that when a model is about to commit to a contradictory answer, its hidden state lurches in directions that don't actually steer the answer. v3 is the experiment that tests this. But how does it actually run, end to end — what gets locked in, what gets measured, what comes out?

## 🧠 The metaphor: a polygraph test, but rigged for science

Picture a careful polygraph lab. You're going to interview many subjects and you want to publish whether the polygraph really detects what you claim. The whole pipeline goes:

**1. 🔐 Lock the rulebook in the safe — before anyone walks in.**
What counts as a positive read — the threshold, the formula, the wiring — is written down and sealed *before* a single subject is tested. You're not allowed to edit it after seeing data. (Pre-registration: the sealed E18 / E17b block, frozen 2026-04-18.)

**2. 🃏 Build the question cards.**
50 cards per cell of a 2×2 grid: *premises contradict / don't* × *long reasoning chain / short*. 200 cards per subject. That's the dataset. (Synthetic 2×2 puzzles at n=50/cell.)

**3. 🩺 Screen the subject first.**
Hand them 20 easy cards before strapping anything on. If they can't hit 80% on the easy ones, they don't understand the questions and the rest is meaningless. They get sent home. (Behavioral gate: control accuracy ≥ 80% on n=20.)

**4. 📡 Wire up sensors at every part of the body.**
Heart, palms, voice, eyes — every "layer." We don't just trust the chest sensor. (Hidden-state capture at every transformer layer, for the first 12 generated tokens.)

**5. ⏱️ Score only the instant the lips move.**
Not the long pause before. Not what they say later. The instant of commitment is the only moment we tabulate. (`Δh = h_t − h_prev` at `gen_step = 1`, final layer.)

**6. 🎛️ Pre-compute the "tell axis."**
Before the answer comes out, we build a compass that points along the *one direction* in sensor-space where any real attempt to answer would push the needle. (Top-1 right singular vector of `√p_t · W_u` — the Fisher commit direction.)

**7. 📐 Read the off-axis fraction.**
If the body moves a lot but mostly *off* the tell axis — scattered, panicky, undirected — the subject is moving without committing to an answer. That's our contradiction signal. (`null_ratio = ‖Δh − V Vᵀ Δh‖ / ‖Δh‖`.)

**8. 🥊 Run a rival lab's simpler compass on the same tape.**
The rival just asks "what's the loudest direction in the wiring?" with no probability weighting. If their compass beats ours, our fancier weighting was useless. (E17b: Fisher-weighted SVD vs HARP's raw `W_u` SVD on the same Δh.)

**9. 🔐 Open the safe.**
Tabulate: contradiction cards vs control cards, ranked by `null_ratio`. Compute AUROC + a 1000-resample bootstrap CI. Compare to the locked threshold. (Sealed E18: AUROC ≥ 0.60, CI doesn't touch 0.5, on ≥ 2 of 3 primaries. E17b: Δ ≥ 0.02 with non-overlap CI on Qwen 2.5.)

## 📊 What we measured / saw

At rank 1 (top-1 tell axis), final layer, gen_step=1, n=200/model:

- 🦙 Llama 3.2 3B — AUROC **0.86** [0.81, 0.91] ✅
- 🌀 Mistral 7B — AUROC **0.86** [0.81, 0.91] ✅
- 🐉 Qwen 2.5 7B — AUROC **0.73** [0.66, 0.80] ✅

Random would sit at 0.50 with the CI hugging 0.5. **3 of 3 primaries cleared the locked threshold.** That's v3's main-run pass. The rival-lab head-to-head (E17b) is more model-dependent — see the rigorous page.

## ✅ / ❌ / 🎁 What this tells us

- ✅ The polygraph design works on the sealed plane: 3-of-3 primaries cleared the threshold that was locked in the safe before any data was seen.
- ❌ The sealed rulebook *didn't pin which rank* of the tell axis to use. At rank 32 the verdict was 0-of-3 pass; at rank 1 it was 3-of-3. The first verdict-pass of this experiment declared falsification before catching the unpinned parameter. v3.1 explicitly pre-registers rank 1.
- 🎁 The rival lab's plain compass beats ours on Qwen 2.5 (E17b sealed FAIL there) — meaning the *direction* signal is real, but the *Fisher weighting* part is architecture-dependent, not a universal win.

## ⚠️ Caveats

- Pre-registration only protects against *post-hoc* fudging. If the pre-registered design is dumb, sealed math doesn't save it. The unpinned-rank trapdoor is exactly this kind of lesson.
- Sensors are taped on *before* the final skin layer (RMSNorm), but the tell axis lives *after* it. The 2026-04-25 J_n correction (see [jn-correction-eli12](jn-correction-eli12.md)) fixes that geometric mismatch and reshuffles the head-to-head verdicts.
- This page describes the n=50/cell main run (2026-04-22 / 2026-04-23). The fresh-data replicate (2026-04-24, seed 20260423) reused the same pipeline; the J_n geometry fix landed 2026-04-26.

## 💡 Takeaway

**v3 is a polygraph test where the threshold is locked in a safe, the question cards split contradiction vs control, sensors are at every layer of the body, and the "tell" is how much the body moves *off* the answer-axis at the instant of commitment.** The safe opens at the end, the numbers walk in, and the rulebook decides PASS or FAIL.
