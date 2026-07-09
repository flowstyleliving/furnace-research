# Qwen 3 8B (4-bit)

MLX handle: `mlx-community/Qwen3-8B-4bit`

**Role in v3.1:** cross-generation companion (Qwen 2.5 → Qwen 3, same family different architecture generation). Descriptive only — not a sealed primary.

## Specs
- Size: 8B parameters
- Quantization: 4-bit (MLX)
- Layers: 36; hidden_dim D = 4096; vocab V = 151,936 (padded from 151,643)
- Dtype: bfloat16
- Output projection: untied `lm_head`
- Class: `mlx_lm.models.qwen3.Qwen3Model` (component layout shared with qwen2; QwenAdapter routes here)

## v3.1 results (n=600, post-norm geometry, run-09)
- **E17b @ sealed r=1: Δ_oriented = −0.214 [−0.261, −0.175]** — **Raw decisive**
- E18 (descriptive — not sealed authority): rupture signal weak at r=1, recovers at r ≥ 13
- Per-rank pattern: **Raw at r=1 (sealed) → tied/borderline through r=8 → Fisher decisive from r=13 onward**, peaking at +0.447 at r=32
- Cross-generation flip: Qwen 2.5 7B is Fisher-decisive at sealed r=1 (+0.157); Qwen 3 8B is Raw-decisive (−0.214). Same family, different architecture generation, opposite verdicts.

## Architectural notes
- Cross-generation companion to Qwen 2.5 — same family, but Qwen3 has wider Fisher-favorable rank band that doesn't include r=1
- gen_step=1 commit token: **modal `' Answer'` (79/100); 21/100 distributed across CoT-preamble alternatives** (per N=100 diagnostic 2026-04-30, refining the earlier "varied" framing). Predominantly content-commit.

## W_u top-1 token analysis (post-J_n correction, N=100, 2026-04-30)

Diagnostic: `scripts/diagnostics/diagnose_raw_top1.py --model mlx-community/Qwen3-8B-4bit`. CSV at `experiments/v3-main-run/2026-04-30/Qwen3-8B-4bit_signed_proj.csv`; JSON at `..._top1_summary.json`.

**Spectrum.** σ_1 = 155.89 (largest in the lineup), σ_1 / σ_2 = 4.76× — large σ_1 magnitude, moderate gap.

**V_raw[0] character — anti-structural axis (native −).** Top-3 positive tokens: `' neighb'`, `' porno'`, `' somew'` (content-bearing rare tokens, several truncated mid-word). Top-3 negative tokens: `' '`, `\n`, `,` — V_raw[0] is **most strongly anchored to the negative side of `'\n'` and whitespace** (much more so than other models: Qwen3 has `'\n'` projecting at −1.335, vs Phi −0.469 and Gemma 4B −0.329). Targeted: `' YES'` = +0.352, `' NO'` = −0.072, `'\n'` = −1.335.

**Per-sample signed Δh_jn · V_raw[0]:** ctrl mean +0.770 ± 0.395, contr mean −1.566 ± 2.547, **Δ (contr − ctrl) = −2.336**, ctrl frac>0 = 98%, contr frac>0 = 50%. **Sign-split distribution on contradictions** — controls cluster on the positive side, contradictions split roughly half-half across zero. The high contr std (2.55, vs ctrl 0.40) reflects this split. Cohen's-d-equivalent ≈ 1.28 — medium-large effect.

**Why Raw decisive at sealed r=1.** Raw_post_rank1 discriminates contradictions (in the inverted-sign direction: AUROC = 0.7142, sign −1) because the contr distribution is shifted negative relative to ctrl despite within-class spread. Δ_oriented = −0.214 [−0.261, −0.175]. The Fisher rotation does NOT add at sealed r=1 here — it actively underperforms, suggesting Qwen3's per-sample `√p_t`-reweighted basis rotates AWAY from the static W_u top-1 axis that's already capturing the contradiction signal. Fisher recovers from r=13 onward (peak +0.447 at r=32) — the rupture signal on Qwen3 lives in a wider rank band than the top-1 alone. See paper §5.1 Table 5.

## Open Questions (W_u top-1)
- 🐲 Why does V_raw[0] on Qwen3 have such a strong negative `'\n'` projection (−1.335) compared to other models? Anomaly worth a closer look — possibly tokenizer-driven (Qwen3's V=151,936 padded from 151,643).
- 🐉 Cross-generation: Qwen 2.5 and Qwen3 share the QwenAdapter and similar layout, but Qwen 2.5 is content-commit + V_raw[0] high variance, while Qwen3 is content-commit + V_raw[0] sign-split. The within-family flip (Fisher → Raw at sealed r=1) suggests something specific to Qwen3 8B's training that re-aligned V_raw[0] with the contradiction signal.

## Quirks caught during onboarding
- Original adapter built a hardcoded float16 causal mask before embedding — fails `scaled_dot_product_attention` on Qwen3's bfloat16 activations because float16 ↔ bfloat16 don't cross-promote even though both are 16-bit. Fixed in `QwenAdapter` by embedding first, then using `_make_attention_mask(x, cache[0])` which delegates to MLX-LM `create_attention_mask` with auto-matched dtype (same pattern `LlamaAdapter` uses). Qwen 2.5 regression-tested through the new path with no regression.

## Trace dump pointers
- n=600 powered: `experiments/v3-main-run/2026-04-26/run-09/Qwen3-8B-4bit_results.parquet`
- n=200 prelim: `experiments/v3-main-run/2026-04-26/run-02/Qwen3-8B-4bit_results.parquet`

## Cross-references
- v3.1 cross-architecture analysis: [results/v3.1-replicate](../results/v3.1-replicate.md)
- Paper Motif framing: [paper/pri-draft.md](../paper/pri-draft.md) §4.3
