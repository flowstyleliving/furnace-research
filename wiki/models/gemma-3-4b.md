# Gemma 3-4B Instruct (4-bit)

MLX handle: `mlx-community/gemma-3-4b-it-4bit`

**Role in v3.1:** cross-architecture descriptive companion (Google Gemma family, interleaved sliding-window attention). **Motif 2 — within-model rank flip Fisher → Raw at r=2 → r=3, robust to chain length.** Originally planned as the 4B endpoint of a within-family scale axis (Gemma 1B ↔ 4B); axis collapsed when [Gemma 1B](gemma-3-1b.md) was excluded for behavioral gate failure.

## Specs
- Size: 4B parameters
- Quantization: 4-bit (MLX)
- Layers: 34; hidden_dim D = 2560; vocab V = 262,208 (padded from 262,144)
- Dtype: bfloat16
- Output projection: untied `lm_head` (largest vocab in the v3.1 lineup)
- Class: `mlx_lm.models.gemma3.Model` (multimodal wrapper) → `.language_model.model = Gemma3Model` (text decoder)

## v3.1 results (n=600, post-norm geometry, run-02 2026-04-27)
- **E17b @ sealed r=1: Δ_oriented = +0.210 [+0.181, +0.237]** — **Fisher decisive**
- E17b @ r=32 (within-model rank flip): Δ_oriented = −0.362 — Raw decisive (same direction as Mistral's pooled r=1 picture)
- Baselines: surprise = 0.960; pri_v2_lowrank32 = 0.960 — strong on this benchmark

## Motif 2 — within-model rank flip robust to chain length

Δ_oriented goes from **+0.207 (Fisher decisive)** at r=2 to **−0.211 (Raw decisive)** at r=3 within one rank step. **Both chain-length strata show the same r=2 → r=3 transition** (one borderline tie at r=5 / cl=2). Cross-stratum spreads stay within ±0.3 at every rank. The flip is a **property of the SVD spectrum, not a chain-length artifact** — pure rank-axis architecture-dependence.

This is the operationalization of "audit the operating-point neighborhood before falsifying": pinning sealed r=1 picks up Fisher decisive; pinning r=32 picks up Raw decisive on the SAME data with non-overlap CI.

## Architectural notes
- Interleaved sliding-window attention (Gemma 3 family signature: `core.sliding_window_pattern > 1`, default sliding window = 512)
- RMSNorm uses `(1.0 + γ)` formulation (Gemma 3 quirk) — `mx.fast.rms_norm(x, 1.0 + self.weight, eps)` rather than applying weight directly
- Multimodal wrapper: `gemma3.Model` holds the text decoder at `.language_model.model = Gemma3Model`, no top-level `.model` attribute
- gen_step=1 commit token (corrected 2026-04-30): **`'\n'` 100/100 samples** on the v3 puzzle prompts — newline-commit, NOT content-commit as the earlier "varies; typically commits to answer content" claim said. See W_u top-1 analysis below.

## W_u top-1 token analysis (post-J_n correction, N=100, 2026-04-30)

Diagnostic: `scripts/diagnostics/diagnose_raw_top1.py --model mlx-community/gemma-3-4b-it-4bit` (multimodal-wrapper unwrap branch added during this run, see `scripts/diagnostics/diagnose_raw_top1.py`). CSV at `experiments/v3-main-run/2026-04-30/gemma-3-4b-it-4bit_signed_proj.csv`; JSON at `..._top1_summary.json`.

**Spectrum.** σ_1 = 102.95, σ_1 / σ_2 = 1.44× — **smallest σ-gap in the lineup**. The static SVD has many comparable directions, no single dominant one.

**V_raw[0] character — weakly content/structural.** Top-3 positive tokens: `S`, `(`, `g` (single-character / punctuation). Top-3 negative tokens: `' ('`, `\n`, `\n\n` (whitespace-adjacent / newline). Targeted: `'NO'` = +0.029, `'\n'` = −0.329. Single-token YES not available in this tokenizer (262K vocab encoding). V_raw[0] does have `\n` as a meaningful negative projection (consistent with Gemma being newline-commit).

**Per-sample signed Δh_jn · V_raw[0]:** ctrl mean −6.087 ± 0.684, contr mean −6.149 ± 0.487, **Δ (contr − ctrl) = −0.061**, ctrl frac>0 = 0%, contr frac>0 = 0%. **All 100 samples project negatively (rupture-magnitude regime, native −), but Δ is ≈ 0** — a tiny separation. Cohen's-d-equivalent ≈ 0.10 — negligible effect.

**Why Fisher decisive at sealed r=1 despite newline-commit.** This is the architecture that **breaks the original "newline-commit ⇒ Raw decisive" partition.** Gemma 4B commits `'\n'` 100/100 times like Mistral and Phi, but its V_raw[0] discriminates contradictions only marginally (Δ −0.061), so Raw_post_rank1 ≈ 0.5. Fisher's per-sample reweighting recovers signal that the static V_raw[0] misses (Δ_oriented = +0.187 at sealed r=1). The Motif 2 rank-flip at r=2 → r=3 is independent — at r=3 the Raw basis (now spanning 3 dimensions, not 1) picks up Gemma's contradiction-discrimination axis cleanly, and Raw becomes decisive there. See paper §5.1 Table 5 for the cross-model picture.

## Open Questions (W_u top-1)
- 🌸 Gemma 4B has the smallest σ-gap (1.44×) and the weakest V_raw[0] discrimination — these are correlated. Top-1 is barely distinguished from top-2 / top-3 in the static SVD spectrum, and adding a few more rank dimensions (r=2 → r=3) flips the verdict from Fisher to Raw. This contrasts with Mistral / Phi where σ-gap is moderate but V_raw[0] saturates discrimination.
- 🪞 Within Gemma family: Gemma 1B was excluded from the main run for behavioral gate failure, so the same diagnostic on 1B is not directly comparable. Worth a one-off Gemma-1B-only run (with gate skipped) to see whether the same V_raw[0]-weak / σ-gap-narrow pattern holds at 1B scale.

## Quirks caught during onboarding
1. **RMSNorm γ extraction (caught pre-data 2026-04-26).** `_extract_final_rmsnorm_gamma` originally returned raw `.weight` for all families; on Gemma this would have multiplied Δh_post by ≈0 (or sign-flipped near-zero) instead of `1 + weight`, silently zeroing every J_n-corrected `null_ratio_*_post_rank{r}` column on Gemma alone. Patched with a Gemma-3-only branch keyed on `core.sliding_window_pattern`.
2. **bf16 precision sub-bug (Gemma 4B specifically).** Adding 1.0 in fp32 after casting from bf16 introduced ~0.4% per-channel rounding compounding to 3.6% max-abs error. Resolved by performing `1 + weight` at the weight's native dtype before casting to fp32. Verified: extracted γ reproduces `model.model.norm(h)` to ≤1e-5 max-abs error.
3. **Multimodal wrapper unwrap.** `gemma3.Model` has `.language_model` with no top-level `.model`; pipeline reaches through in `load_model` so downstream consumers see a uniform `.model.*` layout.
4. **Post-embed √hidden_size scale.** Gemma 3 scales the embedding output by `sqrt(hidden_size)` before the first transformer block (matches `Gemma3Model.__call__`); without this, every captured hidden state would be off by that factor. Wired into `pri_v2_mlx_pipeline._forward_with_hidden` after embed lookup.

## Trace dump pointers
- n=600 powered: `experiments/v3-main-run/2026-04-27/run-02/gemma-3-4b-it-4bit_results.parquet`
- n=200 prelim: `experiments/v3-main-run/2026-04-26/run-08/gemma-3-4b-it-4bit_results.parquet`

## Cross-references
- v3.1 cross-architecture analysis: [results/v3.1-replicate](../results/v3.1-replicate.md)
- Paper Motif 2 framing: [paper/pri-draft.md](../paper/pri-draft.md) §4.3
- Excluded sibling: [gemma-3-1b](gemma-3-1b.md)
