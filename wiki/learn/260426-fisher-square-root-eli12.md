# 🎹 Why `√p_t · W_u` is the Square Root of the Fisher Metric, ELI12

**Rigorous version:** [pri-v3-plan](../pri-v3/pri-v3-plan.md) §Fisher operator
**Companion:** [fisher-weighting-eli5](fisher-weighting-eli5.md) (why we weight by `√p_t` in the first place) · [jn-correction-eli12](jn-correction-eli12.md) (what coordinate space the metric lives in)

---

## 🎯 The question

We keep saying the Fisher basis comes from "SVDing `√p_t · W_u`." But is `√p_t · W_u` *itself* the Fisher metric? Or is it something else with the same fingerprints? (Spoiler: different objects — one is the **square root** of the other.)

---

## 🧠 The metaphor

Picture a piano with a million keys — that's the model's vocabulary. Right now the model is playing a chord: most keys are silent (`p_t ≈ 0`), a handful are pressed LOUD (`p_t = 0.4`-ish). That's the "current song."

You're going to **wiggle your hands** above the keyboard — that's `Δh`, a perturbation in hidden-state space. Your wiggle reaches the keys via the unembedding `W_u`, which says how each finger position presses each key. The audience hears the chord shift.

🎵 **The Fisher metric** answers: *"if I wiggle my hands in this direction, how much does the audience hear the song change?"* It's a `d × d` matrix telling you the **musical responsiveness** of every direction in hand-space.

📋 **The `√p_t · W_u` matrix** is a *score sheet* — every key's lookup row, scaled by how loud that key currently is. The score sheet itself isn't the responsiveness. But:

```
(score sheet)ᵀ · (score sheet)   =    responsiveness
( √p_t · W_u )ᵀ · ( √p_t · W_u ) ≈    Fisher metric
                                  =  W_uᵀ · diag(p_t) · W_u
```

The score sheet is the **square root** of the responsiveness matrix — like how `√4 = 2`, but for matrices. Square it → get the Fisher metric back. SVD it → get the Fisher metric's eigenvectors directly, without ever building the metric.

---

## 📊 Why this matters for the pipeline

**1. We never form the full Fisher matrix.** Llama 3B has `d = 3072` → 9 M entries. Qwen 2.5 7B: `d = 3584` → 12 M entries. Instead we SVD the score sheet directly — its right singular vectors **are** the eigenvectors of the Fisher, and the singular values squared **are** the eigenvalues. One operation, two birds.

**2. The "≈" is doing real work.** The true Fisher in logit space is `D(p_t) = diag(p_t) − p_t · p_tᵀ`. The pipeline's score sheet only captures the `diag(p_t)` part — it drops the `−p_t · p_tᵀ` rank-1 centering term so the matrix factors cleanly. In piano terms: we measure responsiveness *per key* but ignore the fact that all keys share a common volume baseline. At sealed rank 1, this can shift the top eigendirection by a few degrees. At rank ≥ 4, it's invisible.

---

## ✅ / ❌ / 🎁 What this tells us

- ✅ **Confirmed:** SVD of `√p_t · W_u` gives the same eigenvectors as `W_uᵀ · diag(p_t) · W_u`. The matrix and the metric share fingerprints — same principal directions, different shapes.
- ❌ **Ruled out:** the score sheet is **not** the Fisher metric. Asking "is `√p_t · W_u` the Fisher metric?" is like asking "is the sheet music the song?" — the sheet is one form, the song is what comes out of the speakers.
- 🎁 **Bonus:** the pipeline emits both `d_F_full` (full Fisher distance, *with* the `−p_t·p_tᵀ` centering) and the rank-truncated `null_ratio_*` columns (diagonal-only basis). Two views of the same geometry from the same code.

---

## ⚠️ Caveats

- The score sheet's columns live in **post-norm h-space** — that's the coordinate frame `W_u` was trained against. To use it on `Δh` from the residual stream, you have to apply the model's RMSNorm first. That's the J_n correction story (see [jn-correction-eli12](jn-correction-eli12.md)). The square-root trick gives you the right basis; J_n gets you to the right *room* to use it.
- The square-root shortcut only works because the Fisher metric is symmetric and positive-semi-definite. Both properties are guaranteed by construction; we're never going to violate them.
- "Diagonal-only Fisher" is a real approximation, not a wave of the hand. It's the price of getting an SVD instead of an eigendecomposition. The full FIM is still computed for `d_F_full` — just not for the basis.

---

## 🧠 Takeaway in one sentence

> The Fisher metric is the song the audience hears when you wiggle your hands; `√p_t · W_u` is the **score sheet** the pianist follows. Squaring the score sheet recovers the song; SVDing the score sheet finds the principal hand-wiggles directly — same information, faster math.
