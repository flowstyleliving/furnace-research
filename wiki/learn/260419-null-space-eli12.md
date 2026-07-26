# 🕳️ Null Space, ELI12

**Rigorous version:** [claims §0–§2](../claims.md) + [pri-v3-plan](../pri-v3/pri-v3-plan.md)
**Companion:** [spectral-test-eli12](260419-spectral-test-eli12.md) (the sibling metric that didn't work)

---

## 🎯 The big idea

The model's "thought space" has a ton of directions it can move in. Some of those directions *change what word comes out next*. Some don't — they're dead ends. When we force the model to commit to something contradictory, we think it pushes movement into the **dead-end directions** — because the real directions don't have a good answer to offer.

That's the v3 hypothesis in one sentence. 🧠💥

---

## 🎛️ The control-panel analogy

Imagine the model's thought is a giant control panel with 3000 knobs.

- 🟢 **Live knobs** = "informed directions" → turning them changes the output (next word changes)
- 🔴 **Dead knobs** = "null directions" → turning them does *nothing* to the output (next word stays the same)

Normal speech: the model twists live knobs. The panel responds, a word falls out, easy. ✅

---

## 💥 What happens under contradiction

We force the model to commit to a contradictory answer. The situation:

- ⚠️ No live knob has a good setting that produces a sensible word
- ⚠️ But the model **has** to commit — it's an autoregressive loop, it can't just freeze 🧊
- ⚠️ So it twists knobs anyway — just knobs that don't matter

**Real movement, zero output consequence.** The hidden state really does shift — we can measure it. But it shifts in a direction that doesn't correspond to any meaningful word choice. That's the push into null space.

---

## 📊 How we measure it

We compute **null_ratio**:

```
null_ratio = (how much Δh pointed at dead knobs)
             ──────────────────────────────────
             (how much Δh moved in total)
```

- `0` = all the movement was in live directions 🟢 (normal, content)
- `1` = all the movement was in dead directions 🔴 (pure rupture)

Controls → low. Contradictions → high. (That's the prediction. We haven't run it yet.)

---

## 🧮 The math bit (for when you're ready)

"Live directions" = top-r right singular vectors of `sqrt(p_t) · W_u`. Call them `V_top`.
"Dead directions" = everything else, measured by what's *left over* after projecting out `V_top`.

> 🧷 **Option A = commitment-layer subspace, reused at every layer.** We take `p_t` from the **final (commitment) layer's normed logits** once, build one `V_top` from `sqrt(p_final) · W_u`, and use **that same subspace** to measure `null_ratio` at every layer. Not per-layer, not per-step — a single fixed basis anchored at the moment the model commits. This is what makes the metric entropy-invariant at shallow layers (no "already decided" confound) and why E22/E23 bugs mattered so much — the subspace is load-bearing. 📌

```
null_ratio = ‖Δh − V_top V_topᵀ Δh‖ / ‖Δh‖
```

The numerator is the part of Δh that the live directions *can't* explain. Divide by total magnitude → a fraction between 0 and 1. 📐

---

## 🆚 Why this is better than PRI v2

v2 measures **how big** the movement was (`d_F`).
v3 measures **where** the movement went (`null_ratio`).

| | Movement size | Direction | v2 sees | v3 sees |
|---|---|---|---|---|
| 😌 Control | medium | live knobs | "some movement" | "normal, content-filled" |
| 😬 Contradiction | medium | dead knobs | "same amount of movement" ❌ | "rupture — dead-knob movement" ✅ |

v2 thinks those two are the same. v3 separates them. That's the whole pitch.

---

## 🤔 Why the null-space framing even makes sense

Two independent reasons to expect this:

1. 🚂 **The model has to move.** An autoregressive LLM *will* emit a token on every step — it can't abstain. If the informed directions don't contain a good option, the movement has to spill somewhere.
2. 💸 **Null directions are the cheapest place to spill.** By definition, moving there doesn't cost the model output-wise. It doesn't commit the model to a worse word than it already has. Path of least resistance when forced. 🏞️

So the prediction: **forced commitment without good options → null-space discharge.** Contradictions are the cleanest test case (we can construct them with certainty). Hallucinations are the real target. 🎯

---

## 🎁 The failure law idea

If `d_F` (size) and `null_ratio` (direction) are truly independent signals, we can combine them into a per-token failure probability:

```
P_fail(t) = sigmoid(β₀ + β₁·d_F + β₂·null_ratio + β₃·d_F·null_ratio)
```

Fit the four betas on puzzles, then apply **unchanged** to HaluEval. If the same law calibrates on natural hallucination → the mechanism transfers. 🌉

The coefficient pattern is the falsification test:
- β₁ dominant → v3 adds nothing, size was enough
- β₂ or β₃ matter → direction carries independent signal, v3 validated
- β₃ alone → "big AND off-axis" is the real flag (multiplicative)

---

## ⚠️ Caveats

- The SVD is on a truncated subset of the vocab (top 256 rows of `W_u`). So "null" is null *relative to the words the model was actually considering* — not the whole vocabulary.
- We haven't measured this yet. If null_ratio turns out to be perfectly correlated with movement magnitude, v3 adds nothing. The falsification test is whether they carry **independent** signal.
- This works for decoder models (Llama 🦙, Mistral 🌬️, Qwen 🐉). Encoder models (BERT, mpnet) have different Fisher geometry — untested.

---

## 🎯 One-sentence takeaway

> PRI v2 asked "how much did the model move?" PRI v3 asks "did the model move somewhere that actually matters?"
