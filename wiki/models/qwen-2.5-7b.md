# Qwen 2.5 7B Instruct (4-bit)

MLX handle: `mlx-community/Qwen2.5-7B-Instruct-4bit`

## Specs
- Size: 7B parameters
- Quantization: 4-bit (MLX)
- Tokenizer notes: —

## PRI v1 Results
- AUROC: — (pending parquet load; earlier "v1 inversion" framing needs re-verification)
- Hedges g: —
- Bootstrap p: —

## PRI v2 Results (step 1, final layer, α = 1.0)
- **Best variant: `pri_v2_lowrank32` — AUROC 0.7858** (highest of the three primary models)
- Behavioral gate: control acc 0.98, contradiction acc 1.00

## Observed Quirks
- Only one of the three primary models where **low-rank SVD** of the pullback beats top-k truncation.
- Earlier "v1 cosine fully inverted" claim — needs re-verification against current v1 baseline before being filed as validated.

## Trace Dump Notes
- `PRI_at_commitment/pri_v2_results/Qwen2.5-7B-Instruct-4bit_trace_dumps.parquet` present.

## Open Questions
- Why does Qwen prefer low-rank? Architectural (tied embeddings, hidden dim), tokenizer vocab size, or training distribution?
- Was the original "v1 inversion" real, or an artifact of early small-slice runs?
- Does the lowrank32 optimum hold across alpha / layer sweeps?

---

## v3.1 results (n=600, post-norm geometry, run-09 2026-04-26)

**Sealed primary** (gate authority for sealed E18). **Sealed E17b authority** — the head-to-head verdict for the paper. Updated 2026-04-27.

### Architectural details surfaced during v3 onboarding
- Layers 28; hidden_dim D = 3584; vocab V = 152,064
- Dtype: bfloat16
- Output projection: untied `lm_head`
- Class: `mlx_lm.models.qwen2.Model` (Qwen 2.x family; QwenAdapter shared with Qwen3)

### Sealed E18 verdict — PASS
- AUROC = **0.6468** [0.603, 0.691], sign +1 — clears 0.60 threshold with non-overlap 95% CI vs 0.5
- Lowest E18 of the three primaries (Llama 0.871, Mistral 0.871) — but still PASS at the sealed bar

### Sealed E17b verdict on Qwen 2.5 — PASS (the headline of the paper)
- **Δ_oriented = +0.157 [+0.125, +0.190]** at sealed r=1 — **PASS, Fisher decisive**, sealed +0.02 bar cleared by 7.9×
- Fisher AUROC = 0.8967 (sign +1); Raw AUROC = 0.7396 (sign −1) — Fisher discriminates contradictions in the predicted direction; Raw discriminates inverted at this analysis plane
- Cross-stratum: cl=2 Δ = +0.138 [+0.099, +0.175] (Fisher), cl=5 Δ = +0.063 [+0.036, +0.098] (Fisher) — pooled verdict robust under stratification; both strata Fisher-decisive

### J_n correction effect
- The buggy 2026-04-24 reading on this model (pre-norm Δh on post-norm basis) was **Δ = −0.166 [−0.240, −0.098]** — FAIL with Raw decisive
- The corrected 2026-04-27 reading is **Δ = +0.157 [+0.125, +0.190]** — PASS with Fisher decisive
- **+0.32 swing on the same data, same sealed spec, different basis-coordinate-frame implementation.** Sealed _spec_ unchanged across the correction; only the implementation was revised.

### Per-rank pattern
- Oscillates F → R → F → R → F across the rank sweep — multiple flips. Stratification analysis shows the oscillation is partly chain-length-driven (Qwen 2.5 has the second-largest cross-stratum spread in the lineup at r=13 and r=32, Δ_cross ≈ +0.378 and +0.357 respectively).

### gen_step=1 commit pattern — content-commit (refined 2026-04-30)
- N=100 diagnostic: **modal commit `' NO'` (52/100); next most common `' YES'`**. Content-commit confirmed; the split between YES and NO at the commit position is itself an interesting feature (suggests Qwen 2.5 is committing to a specific answer at gen_step=1 with the contradiction-vs-control label modulating which answer).
- The paper's mechanistic hypothesis (§5.1, revised): commit-token type (newline / content) by itself does NOT predict Fisher-vs-Raw; what predicts is V_raw[0]'s discriminative strength. Qwen 2.5's V_raw[0] has high discrimination *with* high within-class variance — Fisher's reweighting refines a basis that V_raw[0] alone gets close to but doesn't saturate.
- One of the cross-model anomalies: Qwen 2.5's surprise (0.8947) and PRI v1 cosine (0.9155) are **competitive with the sealed v3 metric** (0.8967). Qwen 2.5 commits to answer content at gen_step=1 with high confidence on this benchmark, so the simple surprise scalar already separates contradictions from controls effectively; Fisher pullback adds only at the margin.

### W_u top-1 token analysis (post-J_n correction, N=100, 2026-04-30)

Diagnostic: `scripts/diagnostics/diagnose_raw_top1.py --model mlx-community/Qwen2.5-7B-Instruct-4bit`. CSV at `experiments/v3-main-run/2026-04-30/Qwen2.5-7B-Instruct-4bit_signed_proj.csv`; JSON at `..._top1_summary.json`.

**Spectrum.** σ_1 = 86.97, σ_1 / σ_2 = 4.01× — moderate gap.

**V_raw[0] character — frequency-axis-ish, not bipolar content.** Top-3 positive tokens: `' '`, `,`, `1` (common short / numeric). Top-3 negative tokens: `.IsNullOr`, `' volunte'`, `gnore` (code-domain / rare fragments). Targeted projections: `' YES'` = −0.104, `' NO'` = +0.051, `'\n'` = +0.543. YES and NO have *opposite signs* (closest of any model in the lineup to a content-bipolar axis on V_raw[0]), but the magnitudes are small (<0.11) and `\n` projects much more strongly.

**Per-sample signed Δh_jn · V_raw[0]:** ctrl mean −0.30 ± 9.94, contr mean −18.70 ± 1.33, **Δ (contr − ctrl) = −18.400**, ctrl frac>0 = 78%, contr frac>0 = 0%. **Largest absolute Δ in the lineup** — but with *huge* ctrl variance (std 9.94, vs Mistral 0.41) — suggesting Qwen 2.5's ctrl sample has high within-class spread on V_raw[0], possibly from the YES/NO split at the commit position. The contr distribution is much tighter (std 1.33) and uniformly negative.

**Why Fisher decisive at sealed r=1 despite huge V_raw[0] Δ.** Raw_post_rank1 = 0.7396 — decisively above chance but not saturating. The high ctrl variance leaves substantial overlap with the contr distribution at the magnitude level. Fisher's per-sample reweighting (basis = top-r right singular vectors of `√p_t · W_u` rather than `W_u` alone) rotates toward a per-puzzle direction that handles the YES/NO commit split cleanly — Fisher_post_rank1 = 0.8967, Δ = +0.157 [+0.125, +0.190]. See paper §5.1 Table 5.

## Open Questions (W_u top-1)
- 🐉 Why is Qwen 2.5's ctrl distribution so wide on V_raw[0] (std 9.94 vs Mistral's 0.41)? Likely the YES-vs-NO commit split — controls split between ` YES` (true premises → YES) and ` NO` (false premises → NO), pulling Δh_jn in different directions on V_raw[0]. Worth a per-commit-token-stratified diagnostic.
- 🐲 V_raw[1] / V_raw[2]: the same diagnostic captured top-2 and top-3 signed projections. Are they cleaner discriminators on Qwen 2.5 than V_raw[0]? Would explain why Fisher_lowrank32 = 0.8967 ≈ surprise (0.8947) — the discriminative signal is spread across multiple rank directions.

### Trace dump pointers
- n=600 powered: `experiments/v3-main-run/2026-04-26/run-09/Qwen2.5-7B-Instruct-4bit_results.parquet` (sealed_gate.json present, E17b head-to-head recorded canonically)
- n=200 prelim: `experiments/v3-main-run/2026-04-26/run-02/Qwen2.5-7B-Instruct-4bit_results.parquet`
- Buggy forensic: `experiments/v3-main-run/2026-04-24/run-05/Qwen2.5-7B-Instruct-4bit_results.parquet` (legacy column path; retained for the J_n-correction comparison row)

### Cross-references
- Cross-architecture analysis: [results/v3.1-replicate](../results/v3.1-replicate.md)
- Paper §4.2 sealed E17b + §3.4 J_n correction: [paper/pri-draft.md](../paper/pri-draft.md)
- ELI12 explainer of the J_n bug: [learn/jn-correction-eli12](../learn/jn-correction-eli12.md)

