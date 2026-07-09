---
name: Bugs Caught by Inspectors, ELI12
description: Compact record of E22 argmin sign-flip + E23 norm-miss bugs and their lessons
type: learn
---

# 🪲 Bugs Caught Before Shipping, ELI12

**Rigorous:** [results/e22-direction-depth](../results/e22-direction-depth.md) · [results/e23-option-c](../results/e23-option-c.md)
**Companion:** [null-space-eli12](null-space-eli12.md) · [fisher-weighting-eli5](fisher-weighting-eli5.md)

> Two bugs adversarial review caught before the main run. Both would have been embarrassing in the paper. Both are one-line fixes. Keep this page as the cautionary tale.

---

## 🔄 The argmin sign-flip (E22)

The v3 plan had `argmax_depth` = "first layer where `null_ratio` **rises** past a threshold."

That's **backwards**:
- Rising `null_ratio` = more null = **less** informed
- Falling `null_ratio` = less null = **more** informed ← the thing we care about

Fix: `argmax` → `argmin`. One-line edit. You can't see this from the plan alone — you need real data moving the "wrong way" to notice. ⚠️

## 🔩 The missing final-norm (E23)

To build the Option A subspace you project `h` through `W_u`, but the model first applies `core.norm(h)`. Our helper silently skipped it.

Consequence: the `p_t` used to weight the SVD wasn't the `p_t` the model emits. Pre-fix Option A correlation with entropy was **+0.824** (looked like A was "just tracking sharpness"). Post-fix: **+0.509** at layer>0 — moderate, not dominant.

We almost wrote "Option A is entropy-dominated" into the paper. It was a geometry bug, not a property. 🧨

## ⚠️ Same bug class, second place (Prereq 8)

The "Qwen is flat" reading from E22 was the **same norm-miss bug** hiding in `final_p_t_eigenspace`. Post-fix Prereq 8 (2026-04-18): Qwen shows clean late-rise at layer 27, dev −0.030 — same shape as Llama/Mistral. Magnitudes differ, shapes converge.

## 🧘 Surviving lessons

- 🔩 **Apply the final norm before any logit-lens.** Raw block output ≠ normed hidden. The missed seal silently inflated numbers on E22 *and* E23. no duh!
- 🔢 **Baseline before metric.** Random `null_ratio` ≈ 0.995 — a reading of 0.99 means nothing. Always subtract `√((d−r)/d)` or report `1 − null_ratio`.
- 🔍 **Adversarial review catches geometry bugs numerical review misses.** Codex has now flagged four: E22 sign, E23 norm, plan-level coherence, Prereq 8 script hygiene.
- 🗺️ **Probe every compartment.** Sparse layer samples hide structure; Qwen layer 13 was missed until full-density re-read.

## ✅ What's left standing

- **Option A (single fixed final-p eigenspace) is v3 v0.** Lowest entropy correlation, strongest late-rise.
- **Option C retired.** Every (α, support) variant had worse entropy correlation AND weaker late-rise than A.
- **Per-arch profiles.** Late-rise shape is shared across Llama/Mistral/Qwen; magnitudes differ. "The magic layer is X for all models" is not a finding we'll get.
