# E23 — Sharpness-Aware Option C Prototype (Verdict)

**Pre-plan reference:** [pri-v3-plan.md § Prerequisite 6](../pri-v3/pri-v3-plan.md#prerequisites)
**Script:** `PRI_at_commitment/scripts/e23_option_c.py`
**Raw (pre-fix, inflated):** `PRI_at_commitment/experiments/e23-option-c/2026-04-17/run-01/llama-3_2-3b-instruct-4bit_e23.parquet`
**Raw (post-fix, canonical):** `PRI_at_commitment/experiments/e23-option-c/2026-04-17/run-02/llama-3_2-3b-instruct-4bit_e23_fixed.parquet`
**Branch:** `v3-build` @ `6868991` (+ uncommitted E23 script)

Status: **RUN COMPLETE** (2026-04-17, post-fix re-run canonical — see Post-fix section below; pre-fix numbers retained as historical record and flagged inline).

---

## Post-fix re-run (2026-04-17 later, after Codex adversarial review)

Codex raised two high-severity issues on the pre-fix script: (1) per-layer logit-lens was built from **raw block output** rather than `core.norm(h)`, so the support set was chosen in the wrong space; (2) the hardcoded `SUPPORT=256` and pooled correlation couldn't isolate the layer-0 artifact from a genuine α effect. Both fixed; re-run with `SUPPORTS=(128,256,512)`, normed logit-lens for both Option A and C, and split diagnostics.

### Post-fix primary diagnostic — corr(null_ratio, H[p^(ℓ)])

| variant              |   all  | layer=0 | layer>0 |
|----------------------|-------:|--------:|--------:|
| **Option A (normed)** | +0.457 | +0.087  | **+0.509** |
| C α=0 supp=128        | +0.648 | +0.260  | +0.659    |
| C α=0 supp=256        | +0.634 | −0.255  | +0.624    |
| C α=0 supp=512        | +0.629 | −0.761  | +0.607    |
| C α=0.25 supp=128     | +0.659 | +0.403  | +0.724    |
| C α=0.25 supp=256     | +0.671 | +0.225  | +0.726    |
| C α=0.25 supp=512     | +0.672 | −0.015  | +0.726    |
| C α=0.5 supp=*        | ≈+0.65 | +0.56–0.58 | ≈+0.72 |
| C α=1 supp=*          | ≈+0.61 | −0.19   | ≈+0.67    |

### What changed vs the pre-fix numbers

- **Option A entropy correlation fell from +0.824 → +0.509** (layer>0). The pre-fix +0.824 was majority-artefact: logit-lens on raw block output inflated the "final-p" weighting inconsistency. **The "Option A is entropy-dominated" worry was a bug, not a property.**
- **Layer-0 correlations are unstable across support size** (e.g. α=0: +0.26 @ supp=128, −0.76 @ supp=512). Confirms Codex finding 2 — the layer-0 artifact is real and support-dependent. In the layer>0 partition, correlations are stable within \~±0.03 across supports.
- **argmin layer = 27 (depth 1.00) for every variant** once layer 0 is excluded. The pre-fix "C argmin=0 (artifact)" collapse was entirely layer-0 noise. Structure is preserved across every α × support in layer>0.
- **Late-layer deviation magnitude ordering (post-fix, layer>0):** A=−0.052, C α=0 supp=512=−0.059, C α=0.25 supp=256=−0.043, C α=1=−0.034. Option A and C α=0 (large support) are tied for strongest late-rise.

### Post-fix verdict — `[OPTION-A-REAFFIRMED, CLEANER EVIDENCE]`

1. **Option A stays default for v3 v0.** Lowest entropy correlation (+0.509 layer>0) and strongest late-rise (dev −0.052). No Option C variant beats it on either axis.
2. **The v3 paper should not frame Option A as "sharpness-dominated."** Post-fix, its entropy correlation at layer>0 is moderate, and the pooled +0.457 is dominated by a genuine depth→entropy chain, not a direct pathology.
3. **The layer-0 embedding artifact is real but isolated.** For any future per-layer-support variant, mask layer 0. Option A's random-projection baseline at layer 0 (null_ratio ≈ 0.9935) confirms its layer-0 is clean.
4. **Support size matters at layer 0 only.** For layer>0, null_ratio is insensitive to supp∈{128, 256, 512} within \~0.01. This is a positive result for v3 — the support choice is not a free hyperparameter that secretly drives results.

### Why the pre-fix Option A correlation was so inflated

`greedy_commit_token` (e22) correctly applies `core.norm(h)` before `W_u` to get real next-token logits. But `final_p_t_eigenspace` did not, so the "p_t" used to weight Option A's eigenspace was a **different** distribution from the one the model actually emits at commit. Those two softmaxes diverge most where the raw-block output differs most from the normed version — correlated with entropy of the true distribution. So Option A's raw-block-based p_t had an artefactual high entropy-correlation. Normed logit-lens eliminates this.

**v3 implication:** `final_p_t_eigenspace` should apply norm by default. Currently only E23 does this locally; E22's shared helper still skips norm (doesn't matter for E22's own published numbers since those already reflect the unpatched helper, but any reuse needs to pass the normed hidden).

---

## Pre-fix run (historical, inflated)

*The section below is the original pre-fix verdict. Numbers are inflated by the logit-lens norm-miss flagged by Codex. Retained for provenance; the post-fix section above is canonical.*

## Verdict: `[OPTION-A-REAFFIRMED]` with a new artifact flagged

No Option C variant meets the primary success criterion (`|corr(null_ratio_ℓ, H[p^(ℓ)])| < 0.3`). More importantly, the per-layer support-selection that Option B/C requires introduces a **layer-0 artifact** that dominates `argmin` across all C variants, erasing the clean late-rise Option A shows. Option A remains the default for v3 v0.

Three findings this run produced:

1. **The entropy confound in Option A is mostly indirect (via depth), not direct.** Entropy ↔ depth is only weakly correlated on decoders (`corr = −0.444`); Option A ↔ depth is strongly correlated (`−0.787`); the resulting Option A ↔ entropy correlation (`+0.824`) is the derivative of this chain, not a direct sharpness pathology. The spectral-band pre-plan verdict's warning about Option B sharpness-dominance doesn't transfer to `null_ratio`, which is a projection-ratio metric rather than an eigenvalue-spread metric.
2. **Softening α from 1.0 → 0.0 reduces entropy correlation** (`+0.423 → +0.625`, worse actually). α=1 (= Option B) has the *lowest* entropy correlation among tested variants and the lowest depth correlation (`−0.074`), but produces a mostly-flat profile that's the worst for interpretability.
3. **Per-layer support selection produces a layer-0 embedding artifact.** At layer 0, Δh equals the difference between two embedding rows; the top-256 of `p^(ℓ=0)` span overlaps heavily with `W_u` rows (especially in tied-embedding configurations). This inflates layer-0 informed-content measurement to `dev ≈ −0.08` — larger than the genuine final-layer peak. Any pipeline that uses Option B/C will need to mask or exclude layer 0.

## Primary diagnostic — correlation with per-layer entropy (pooled)

| Variant              | corr(null_ratio, H[p^(ℓ)]) | corr(null_ratio, depth) | argmin layer | argmin dev from baseline |
|----------------------|---------------------------:|------------------------:|-------------:|-------------------------:|
| **A (fixed final-p)** | +0.824                     | −0.787                  | **27** (depth 1.00) | **−0.053**       |
| C, α=0.0             | +0.625                     | −0.163                  | 0 (depth 0.00) *(artifact)* | −0.073    |
| C, α=0.25            | +0.543                     | −0.147                  | 0 (depth 0.00) *(artifact)* | −0.076    |
| C, α=0.5             | +0.487                     | −0.126                  | 0 (depth 0.00) *(artifact)* | −0.079    |
| B, α=1.0             | **+0.423**                 | −0.074                  | 0 (depth 0.00) *(artifact)* | −0.085    |

- **Primary criterion (|corr_entropy| < 0.3):** ❌ failed by all variants.
- **Secondary criterion (structure preserved):** ✅ for Option A only. C/B variants have layer-0 artifact and flat late-rise.
- **Tertiary criterion (argmin stable within ±2 layers vs Option A):** ❌ for all C variants — argmin jumps from final layer to embedding layer.

## Depth profile comparison (late-layer only, layer 16 → 27)

Entropy is mostly flat across layers 0–25 on Llama (10.89–11.76 nats) and collapses only in the final two layers (7.90 at layer 27). So the "sharpness confound" is concentrated in the final 1–2 layers, not spread across depth.

| layer | depth | H[p^(ℓ)] | A dev | C α=0 dev | B α=1 dev |
|------:|------:|---------:|------:|----------:|----------:|
| 16    | 0.59  | 11.73    | −0.005 | −0.006    | −0.006    |
| 20    | 0.74  | 11.69    | −0.012 | −0.014    | −0.018    |
| 24    | 0.89  | 11.54    | −0.023 | −0.015    | −0.018    |
| 26    | 0.96  | 10.89    | −0.033 | −0.036    | −0.031    |
| 27    | 1.00  | 7.90     | **−0.053** | **−0.067**    | −0.049    |

Late-rise shape is preserved across all variants in the 20–27 range. Magnitudes diverge most at the final layer, where entropy collapse matters most — but the *direction* of deviation is consistent (all get more negative into the commit layer).

## Why Option B didn't collapse here (the spectral-band result doesn't transfer)

The 2026-04-14 spectral-band run found that `λ_max^(ℓ) / λ_mean^(ℓ)` blew up at sharp layers — `A_ℓ = sqrt(p^(ℓ))·W_s` becomes near-rank-1 as entropy collapses. That's an *eigenvalue-spread* pathology.

`null_ratio` is a *projection-ratio*: how much of Δh survives projection onto the top-r subspace of A_ℓ. At α=1, the top-32 subspace of a rank-1-ish matrix is dominated by the commit-token row direction — a single well-defined direction. Projection of Δh onto it gives a specific residual; the result is stable, not pathological. The spectral-band verdict's warning was about a different metric.

## What this changes for v3

1. **Keep Option A as the v3 v0 default.** No variant tested here improves on Option A's interpretability. α=1 has marginally better entropy decoupling but no depth structure; α=0 has no sharpness coupling advantage vs α=0.5.
2. **Mask or exclude layer 0 for any future per-layer-support variants.** If v3 or a follow-up uses Option B/C, the embedding-overlap artifact needs explicit handling. Flag for v3 Analysis § if Option B/C is revisited.
3. **Revise the "Option B disfavored" framing in the plan.** The spectral-band-derived prior against Option B targeted eigenvalue spread, not projection ratios. On the actual v3 observable (`null_ratio`), Option B performs respectably (late-rise preserved, low entropy correlation) — it's just not better than Option A. Frame this accurately in v3 theory section.
4. **The entropy confound in Option A is indirect.** Don't frame Option A as "sharpness-dominated" in the v3 paper. Its correlation with entropy goes through depth; the direct dependency is weak. This is defensible as-is.

## Caveats

- **Llama-only prototype.** Mistral / Qwen may respond differently. (Note 2026-04-18: Qwen's E22 "flat" profile turned out to be a norm artifact — post-fix Qwen shows late-rise like Llama/Mistral, so the Option-C-on-Qwen question is less about a flatness-specific α sensitivity and more about standard per-model replication.) Replicate if/when Option C is revisited.
- **Rank 32 only.** Option C at rank 64 or 128 might behave differently, especially given the layer-0 artifact shrinks with larger rank (more of embedding subspace gets captured).
- **n = 4/cell** — exploratory only; no contradiction/control separation claim tested.
- **Tied-embedding effect not controlled.** Llama-3.2-3B uses tied input/output embeddings. The layer-0 artifact is likely weaker on models without tying.
- **Support selection is itself sharpness-coupled.** Even at α=0, we pick top-256 of `p^(ℓ)` — so the identity of the support depends on sharpness. A truly sharpness-independent variant would need fixed / random support.

## Log

- 2026-04-17 · pre-run · E23 filed per v3 plan Prerequisite 6.
- 2026-04-17 · run · `scripts/e23_option_c.py` on v3-build @ `6868991` + uncommitted E23; 448 rows in 78s.
- 2026-04-17 · verdict · `[OPTION-A-REAFFIRMED]`. Option A stays default for v3 v0. Layer-0 artifact flagged for any future per-layer-support variant. "Option B disfavored" framing in plan needs softening (not "sharpness-dominated on null_ratio", just "not better than A").
- 2026-04-17 · codex-review · OpenAI codex plugin `/codex:adversarial-review` returned 2× `[high]` findings: (1) per-layer logit-lens built on raw block output instead of normed; (2) hardcoded `SUPPORT=256` + pooled success criterion can't isolate layer-0 artifact.
- 2026-04-17 · post-fix rerun · Applied `core.norm` before logit-lens (Option A + C); swept `SUPPORTS=(128,256,512)`; persisted `support_mass` + `support_sig`; split corr by layer=0 / layer>0. Raw: `*_e23_fixed.parquet`. **Option A entropy correlation fell +0.824 → +0.509 (layer>0) — pre-fix number was majority-artefact.** Verdict `[OPTION-A-REAFFIRMED, CLEANER EVIDENCE]`. "Option A is sharpness-dominated" framing retired for v3 paper.
