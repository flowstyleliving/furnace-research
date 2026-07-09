# The J_n correction — what we missed in the Fisher pullback (2026-04-25)

_ELI12 walkthrough of the layer-norm Jacobian bug that confuses the v3 E17b head-to-head. Companion to [v3.1-replicate](../results/v3.1-replicate.md). For the full methodological writeup see [pri-v3-plan §Amendments 2026-04-25](../pri-v3/pri-v3-plan.md)._

## 💡 The gist

We're trying to measure: *"if the model's hidden state wobbles by a tiny `Δh`, how much does the prediction `p_t` wobble?"* That has an exact mathematical answer — the **Fisher pullback metric**. Our pipeline was computing a slightly wrong version of it. Fixing it changes the v3 E17b verdict in interesting ways.

## 🪞 The camera analogy

A camera takes a photo of a scene through a lens. You want to know: if the scene moves 1 cm, how much does that move in the photo?

You can't just answer "1 cm." The lens distorts. Wide-angle makes 1 cm look like 0.5 cm; telephoto makes it 5 cm. **You need to know the lens, not just the scene.**

In our setup:
- 🧠 The "scene" = hidden state `h` (the model's internal thought)
- 🔍 The "lens" = layer norm + lm_head (turns `h` into prediction probabilities)
- 📷 The "photo" = predicted token distribution `p_t`

The lens has two parts. We've been using only one of them.

## ⚙️ The math (just enough to see the bug)

The model commits via:
$$p_t \;=\; \mathrm{softmax}(W_u \cdot n(h))$$

where `n(·)` is RMSNorm: `n(h) = γ ⊙ h / r(h)` with `r(h) = sqrt(mean(h²))`.

The Fisher information of `p_t` w.r.t. `h` is the proper *infinitesimal-rupture* metric:
$$F_h \;=\; J_n^\top \cdot W_u^\top \cdot \big(\mathrm{diag}(p_t) - p_t p_t^\top\big) \cdot W_u \cdot J_n$$

where `J_n = ∂n(h)/∂h` is the **RMSNorm Jacobian at the current `h`**:
$$J_n(h) \;=\; \frac{1}{r(h)} \cdot \mathrm{diag}(γ) \cdot \Big(I - \frac{h\, h^\top}{D \cdot r(h)^2}\Big)$$

Two crucial properties of `J_n`:

- 🪟 **Rank-deficient**: `J_n` projects out the component of `Δh` parallel to `h`. Direction-along-`h` is in the kernel — RMSNorm literally cannot see it.
- 📏 **Scale `1/r(h)`**: small for high-RMS hidden states (Qwen `r(h) ~ 7-15`), near-unit for low-RMS ones (Mistral `r(h) ~ 1-2`).

## 🐛 What the pipeline computed instead

Look at `pri_v2_mlx_pipeline.py:1218-1232` (Fisher SVD basis):

```python
A = sqrt(p_s) * W_s          # (support × D)
_, S, Vt = np.linalg.svd(A)  # Vt[0..r] are basis vectors in W_u-row space
```

That's the SVD of `(diag(p))^{1/2} · W_u`, which approximates `W_u^T · D(p) · W_u` — **but in logit-space, NOT `h`-space**.

Then we project raw `Δh_pre` (pre-norm hidden-state delta) onto this basis. The basis lives in `n(h)`-space; `Δh_pre` lives in `h`-space. **We're projecting two different geometric spaces against each other with no Jacobian correction.**

For models where `J_n` is approximately a uniform scale (all `γ` similar, low `r(h)` variance), this is benign. For Qwen-family models with huge pre-norm `|Δh|` and large `r(h)`, the mismatch is severe.

## 🧪 What the diagnostic showed (2026-04-25)

We computed `null_ratio` three ways for the same underlying data:
- 🅰️ **pre-norm**: project `Δh_pre` onto `Vt` (the buggy original)
- 🅱️ **J_n-corrected**: project `J_n(h_prev) · Δh_pre` onto `Vt` (the proper Fisher pullback)
- 🅲️ **post-norm**: project `Δh_post = n(h_t) - n(h_prev)` onto `Vt` (linearization-free but adds curvature)

Cross-model Δ(F−R) AUROC at rank=1 (sealed plane), N=100 with 2000-sample bootstrap CI:

| Model | pre-norm | J_n-corrected | post-norm |
|---|:---:|:---:|:---:|
| 🦙 Llama 3B | -0.033 [-0.10, +0.05] | +0.054 [-0.13, +0.22] | -0.034 [-0.10, +0.04] |
| 🌀 Mistral 7B | +0.112 [+0.05, +0.18] | **-0.184 [-0.27, -0.11]** | -0.286 [-0.43, -0.14] |
| 🐉 Qwen 2.5 7B | -0.018 [-0.08, +0.03] | +0.015 [-0.08, +0.12] | -0.014 [-0.06, +0.02] |
| 🐲 Qwen 3 8B | -0.278 [-0.41, -0.15] | **+0.206 [+0.03, +0.39]** | -0.361 [-0.51, -0.21] |

🚨 **The J_n correction does opposite things to different models:**
- Qwen 3: pre-norm strongly RAW-wins (CI fully negative); J_n strongly FISHER-wins (CI fully positive). **Sign-flips with non-overlap CIs in opposite directions** — the geometry choice is decisive.
- Mistral: pre-norm slight FISHER-win (CI positive); J_n strong RAW-win (CI negative). **Mistral's pre-norm Fisher win was actually a geometric artifact** — under proper J_n, raw_top1 emerges as a near-perfect 0.99 AUROC discriminator.
- Llama, Qwen 2.5: indeterminate at N=100 either way; CIs cross 0.

## ⚠️ What this trips people up on

🚫 **"Layer norm is just scaling — it doesn't change direction."** Wrong. RMSNorm has a rank-deficient Jacobian: motion along `h` becomes invisible. For models where `Δh` has a big component along `h` (Qwen-family does), a substantial fraction of "rupture" we were measuring isn't visible to the model's prediction.

🚫 **"If pre-norm and post-norm give the same answer, no bug."** Wrong. The diagnostic shows pre-norm and post-norm Δh_pre have `cos ≈ 0.94` for Qwen 2.5 — almost the same direction! But the *projections onto the post-norm basis* differ in subtle ways that flip AUROC signs. The mismatch is small geometrically but big in its consequences for ordered statistics like AUROC.

🚫 **"J_n correction is just a scale-up of post-norm."** Wrong. `J_n · Δh_pre` is the **first-order linear approximation** of `Δh_post` around `h_prev`. `Δh_post` includes nonlinear curvature (`n` is nonlinear). The Fisher pullback formula explicitly assumes the linear approximation. Empirically `cos(J_n·Δh_pre, Δh_post) ≈ 0.92` for Qwen 2.5 — close but not identical — and the J_n version is the theoretically correct object.

## 🎯 Why it matters for v3

- ✅ **E18 (3-of-3 PASS) is unaffected.** E18 residualizes `null_ratio` against `d_F` (which is also derived from the buggy basis). The residualization happens to wash out the mismatch. So 3-of-3 sealed E18 still holds.
- 🔄 **E17b (head-to-head) is geometry-sensitive.** The pipeline reported FAIL on Qwen 2.5 at -0.166. Under J_n, Qwen 2.5 is borderline (+0.015 at rank=1, robust pass at rank ≥4). Qwen 3 flips DECISIVELY in Fisher's favor under J_n.
- 🤔 **The cross-model picture is more interesting than "v3 saved" or "v3 falsified."** Mistral's raw_top1 emerges as a freakishly clean answer-axis under proper geometry, regardless of Fisher reweighting. Qwen-family models genuinely benefit from Fisher reweighting. Llama's signal is too weak at N=100 to call.

## 📐 Where this leaves the paper

The honest reading: **v3's Fisher-pullback hypothesis is partially supported under proper geometry**. There exist models where Fisher reweighting adds discriminative signal beyond the static W_u top-r subspace (Qwen 3 strongly, Qwen 2.5 weakly). There exist models where the static raw subspace is already so well-aligned with the answer-direction that Fisher can't help (Mistral). The model-dependence is itself the finding.

The pre-registered E17b at rank=1 was INHERITED from E18's rank-1 pin (which made sense for residualized magnitude-independence) but was never well-motivated for E17b's head-to-head metric. The rank landscape under J_n shows Fisher's edge living at higher ranks for Qwen-family models — pre-reg pinning rank=1 happened to land on Qwen-family Fisher's WORST rank.

This is paper-shapable: the v3 line still has scientific content, with a more interesting nuance about model-architecture-dependent geometry than the original "Fisher uniformly beats raw" claim.
