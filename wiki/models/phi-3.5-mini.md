# Phi-3.5-mini Instruct (4-bit)

MLX handle: `mlx-community/Phi-3.5-mini-instruct-4bit`

**Role in v3.1:** cross-architecture descriptive companion (reasoning-tuned, cross-vendor). **Motif 1 — stable Raw across all 13 ranks.** Recovered into the lineup 2026-04-26 after originally gate-failing at 60% control accuracy on the 2026-04-23 main run.

## Specs
- Size: 3.8B parameters
- Quantization: 4-bit (MLX)
- Layers: 32; hidden_dim D = 3072; vocab V = 32,064 (padded from 32,000)
- Dtype: float16
- Output projection: untied `lm_head`
- Class: `mlx_lm.models.phi3.Phi3Model`

## v3.1 results (n=600, post-norm geometry, run-01 2026-04-27)
- **E17b @ sealed r=1: Δ_oriented = −0.441 [−0.485, −0.392]** — **Raw decisive, largest E17b margin observed across all 6 models in the v3.1 lineup**
- **`null_ratio_raw_post_rank1` = 0.9989** — nearly perfect contradiction discrimination via the static W_u SVD basis alone, sign +1 (aligned with rupture)
- Fisher_post_rank1 = 0.5766 (sign +1) — barely above chance
- Baselines on Phi: surprise 0.901, PRI v1 cosine 0.899, PRI v2 lowrank32 0.949, v2 topk32 0.949 — at the sealed plane on Phi, the simpler metrics are decisively better than the Fisher pullback (one of the cross-model anomalies)

## Motif 1 — stable Raw across all 13 ranks

Phi-3.5 is the **only model in the lineup** with Raw decisive at every single rank in the sweep, every chain-length stratum. Δ_oriented ranges from −0.105 (r=3) to **−0.459 (r=32)**; CI fully negative at every cell. The static W_u SVD basis carries the rupture signal so cleanly that Fisher's per-sample reweighting cannot add. **The canonical "HARP-style detection works as advertised" architecture, and the headline counter-example to "Fisher pullback uniformly wins."**

## Behavioral gate recovery

Originally gate-failed at 12/20 = 60% on the 2026-04-23 main run under the original 256-token gate budget + last-match-anywhere parser. Phi front-loads `Answer: YES` then format-completes (`"Answer: YES Instruction: Read the premises and answer..."`); the parser's last-match was picking up a fabricated next-puzzle answer. Recovered 2026-04-26 under v3.1 fixes:
- `--gate-max-tokens 12` clips the front-loaded answer before format completion
- 3-tier `check_answer` parser (Tier 1 prefers last `Answer:`)
- Gate now passes 100% (20/20) and full n=150/cell run produced 200 samples cleanly.

## Architectural notes
- Reasoning-tuned (Phi-3.5 instruction tuning includes CoT data)
- gen_step=1 commit token on v3 puzzle prompts: **`'\n'` 100/100 samples** (newline-commit, not content-commit). The earlier "front-loads `Answer: YES`" claim described few-shot gate prompts (which trigger worked-example completion), not the main-pipeline puzzle prompts. See W_u top-1 analysis below — Phi joins Mistral as a newline-commit + rupture-magnitude-axis architecture.
- Same Phi3Model class layout as Phi-3 series

## W_u top-1 token analysis (post-J_n correction, N=100, 2026-04-30)

Diagnostic: `scripts/diagnostics/diagnose_raw_top1.py --model mlx-community/Phi-3.5-mini-instruct-4bit`. CSV at `experiments/v3-main-run/2026-04-30/Phi-3.5-mini-instruct-4bit_signed_proj.csv`; JSON at `..._top1_summary.json`.

**Spectrum.** σ_1 = 111.67, σ_1 / σ_2 = 1.75× — a *small* gap (multiple comparable directions in the static SVD; Llama 7.84× and Mistral 5.00× are both larger). Top-8 σ: [111.67, 63.88, 50.23, 39.83, 31.95, 29.98, 28.00, 26.08].

**V_raw[0] character — non-content rupture-magnitude axis (native −).** Top-3 positive tokens: `provin`, `Wikip`, `zna` (European-language fragments + code-domain). Top-3 negative tokens: `(`, `\n`, `in` (common short tokens). Targeted projections: `'NO'` = +0.344, `'Answer'` = +0.483, `'\n'` = −0.469. **Both YES and NO project positively with similar magnitudes** (when checked against the tokenizer); V_raw[0] is *not* a YES/NO bipolar content axis, and `\n` is among its strongest negative projections.

**Per-sample signed Δh_jn · V_raw[0]:** ctrl mean −9.57 ± 0.59, contr mean −8.14 ± 0.89, **Δ (contr − ctrl) = +1.434**, ctrl frac>0 = 0%, contr frac>0 = 0%. **All 100 samples (both ctrl and contr) project negatively onto V_raw[0]; magnitude separates them.** Cohen's-d-equivalent ≈ 1.9 — large effect on a single static direction.

**Mechanism for the 0.9989.** V_raw[0] is anchored to the structural commit (`\n`) rather than to YES/NO content. Δh_jn at gen_step=1 lands monotonically on V_raw[0]; the magnitude separation between ctrl and contr is the discriminator, with negligible distribution overlap. Fisher's per-sample reweighting cannot improve on a single static direction that already saturates contradiction discrimination this cleanly. Phi shares this regime with Mistral (despite different vendors and tokenizers) — see paper §5.1 Table 5.

## Open Questions
- 🪞 Does the static-W_u 0.9989 hold on real factual contradictions, or is it specific to the synthetic 2×2 template? Fresh-data factual replicate is the v4 test.
- 🧬 Within-Phi-family: do Phi-3 / Phi-3-mini also commit `'\n'` at gen_step=1 and route discrimination through V_raw[0]? Disambiguates "Phi-3.5-specific reasoning fine-tuning" from "phi-family architecture / lm_head structure."
- 🪜 Depth profile: does V_raw[0] saturate at earlier layers too, or only at final?
- 🪡 Chain-length sensitivity at sealed r=1 — Phi shows |Δ_oriented| 0.374 (cl=2) vs 0.228 (cl=5) at sealed r=1. Smaller spread than Mistral's r=32 site, but the same direction. Worth checking explicitly whether Phi has Mistral-style Simpson's-paradox sites at higher rank, or whether its rupture-magnitude axis is chain-length-decoupled.

## Trace dump pointers
- n=600 powered: `experiments/v3-main-run/2026-04-27/run-01/Phi-3.5-mini-instruct-4bit_results.parquet`
- n=200 prelim: `experiments/v3-main-run/2026-04-26/run-06/Phi-3.5-mini-instruct-4bit_results.parquet`
- W_u top-1 diagnostic (2026-04-30): `experiments/v3-main-run/2026-04-30/Phi-3.5-mini-instruct-4bit_{signed_proj.csv,top1_summary.json}`

## Cross-references
- v3.1 cross-architecture analysis: [results/v3.1-replicate](../results/v3.1-replicate.md)
- Paper Motif 1 framing: [paper/pri-draft.md](../paper/pri-draft.md) §4.3
- Paper §5.1 cross-model W_u top-1 table: [paper/pri-draft.md §5.1](../paper/pri-draft.md)
