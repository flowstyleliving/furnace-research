# Llama 3.2 3B Instruct (4-bit)

MLX handle: `mlx-community/Llama-3.2-3B-Instruct-4bit`

## Specs
- Size: 3B parameters
- Quantization: 4-bit (MLX)
- Tokenizer notes: —

## PRI v1 Results
- AUROC: — (v1 cosine baseline present in fig 1, numbers pending parquet load)
- Hedges g: —
- Bootstrap p: —

## PRI v2 Results (step 1, final layer, α = 1.0)
- **Best variant: `pri_v2_topk32` — AUROC 0.7666**
- Behavioral gate: control acc 1.00, contradiction acc 1.00
- Other FIM variants (diag, full, topk5/10, lowrank10/32/50): pending per-variant extraction

## Historical Single-Model Slice (tiny-benchmark, commits 2026-04-07)
- `3d2ccd7` — normalize pullback by hidden motion — score **0.875** (last verified single-model keep)
- `0963932` — pullback-only v2 — score 0.859
- `faa8b0b` — post-norm final hidden — score 0.766
- Baselines `f3dcdb4` / `6aa5130` at 0.750

## Observed Quirks
- Prefers **top-k** FIM restriction over low-rank SVD.
- Normalizing pullback by hidden-motion magnitude gave the single biggest tiny-slice win.

## Trace Dump Notes
- `PRI_at_commitment/pri_v2_results/Llama-3.2-3B-Instruct-4bit_trace_dumps.parquet` present and current.

## Open Questions
- Does the tiny-slice `3d2ccd7` win (pullback normalized by hidden motion, 0.875) replicate on the full synthetic benchmark and across the rest of the model suite?

---

## v3.1 results (n=600, post-norm geometry, run-09 2026-04-26)

**Sealed primary** (gate authority for sealed E18). Updated 2026-04-27.

### Architectural details surfaced during v3 onboarding
- Layers 28; hidden_dim D = 3072; vocab V = 128,256
- Dtype: float16
- Output projection: tied embeddings (`embed_tokens.as_linear`) — confirmed via `Output projection: tied_embed (V=128256, D=3072)` banner

### Sealed E18 verdict — PASS
- AUROC = **0.8713** [0.842, 0.896], sign +1 — clears 0.60 threshold by 4.5×, non-overlap 95% CI vs 0.5
- n=200 prelim (run-02): 0.8946 [0.851, 0.930] — replicates direction-for-direction; CI tightened ~33% as expected from √3 narrowing

### E17b head-to-head — Fisher decisive
- **Δ_oriented = +0.272 [+0.222, +0.320]** at sealed r=1 — Fisher beats Raw by the second-largest pooled margin in the lineup (after Phi's −0.441 in the opposite direction)
- Fisher AUROC = 0.8963 (sign +1); Raw AUROC = 0.3757 (sign −1)
- Cross-stratum: cl=2 Δ = +0.397, cl=5 Δ = +0.170 — both Fisher decisive; pooled verdict robust under stratification

### Per-rank pattern
- **Fisher-or-tied at every rank in the 13-point sweep — never reaches Raw decisive.** Stable positive Fisher signal across the rank axis. Distinct from Mistral (Simpson's flips), Qwen 2.5 (oscillating), Qwen 3 (Raw at r=1 only), Phi (stable Raw), Gemma 4B (sharp r=2→r=3 flip).

### gen_step=1 commit pattern — content-commit (corrected 2026-04-30)
- N=100 diagnostic: **98/100 samples emit `' Answer'` at gen_step=1; 2/100 emit `'\n'`**. Modal commit is content (`' Answer'`), NOT newline. The earlier "newline-commit similar to Mistral" framing was inaccurate — Llama is a content-commit architecture on the v3 puzzle template.
- Cross-stratum |Δ| sharper at cl=2 (0.397) than cl=5 (0.170) — short reasoning chains place the commit closer to contradiction in token-space. The universal cross-model |Δ_cl=2| > |Δ_cl=5| pattern holds independently of commit-token identity.

### W_u top-1 token analysis (post-J_n correction, N=100, 2026-04-30)

Diagnostic: `scripts/diagnostics/diagnose_raw_top1.py --model mlx-community/Llama-3.2-3B-Instruct-4bit`. CSV at `experiments/v3-main-run/2026-04-30/Llama-3.2-3B-Instruct-4bit_signed_proj.csv`; JSON at `..._top1_summary.json`.

**Spectrum.** σ_1 = 153.45, σ_1 / σ_2 = 7.84× — the **largest σ-gap in the lineup**, suggesting V_raw[0] is a uniquely-distinguished direction rather than one of many comparable ones.

**V_raw[0] character — weak rupture-magnitude axis (native +).** Top-3 positive tokens: `,`, `' '`, `' ('` (common short / structural tokens). Top-3 negative tokens: `SCRI`, `using`, `TRGL` (code-domain fragments). Targeted projections: `' YES'` = −0.338, `' NO'` = −0.088, `'\n'` = +0.576. YES and NO same-sign (both negative) with 4× magnitude difference — non-content axis.

**Per-sample signed Δh_jn · V_raw[0]:** ctrl mean +1.302 ± 0.147, contr mean +1.364 ± 0.263, **Δ (contr − ctrl) = +0.062**, ctrl frac>0 = 100%, contr frac>0 = 100%. All samples same-sign (rupture-magnitude regime), but Cohen's-d-equivalent ≈ 0.30 — a small effect. **V_raw[0] alone barely discriminates contradictions on Llama.**

**Why Fisher decisive at sealed r=1.** V_raw[0] is too weak to saturate Raw_post_rank1 (Δ +0.062 across 100 samples leaves substantial distribution overlap). Fisher's per-sample reweighting rotates the basis toward directions where the prompt's prediction is sensitive, recovering signal that the static V_raw[0] misses. Δ_oriented (Fisher − Raw) = +0.272 at sealed r=1 — the second-largest pooled margin in the lineup, opposite-direction from Phi (which is at the saturated-Raw extreme). See paper §5.1 Table 5 for the cross-model picture.

## Open Questions (W_u top-1)
- 🪞 Why does Llama have the largest σ_1 / σ_2 gap (7.84×) yet weak V_raw[0] discrimination? Suggests V_raw[0] points at a strongly-distinguished direction in W_u that *isn't* the contradiction axis. What is it pointing at? (Common-short-tokens-vs-code-domain looks like a frequency-split axis rather than a content axis.)
- 🪜 Depth profile: at intermediate layers (quarter, mid), does V_raw[0] become a stronger discriminator before fading at final?

### Trace dump pointers
- n=600 powered: `experiments/v3-main-run/2026-04-26/run-09/Llama-3.2-3B-Instruct-4bit_results.parquet` (sealed_gate.json present)
- n=200 prelim: `experiments/v3-main-run/2026-04-26/run-02/Llama-3.2-3B-Instruct-4bit_results.parquet`

### Cross-references
- Cross-architecture analysis: [results/v3.1-replicate](../results/v3.1-replicate.md)
- Paper §4.1 sealed E18: [paper/pri-draft.md](../paper/pri-draft.md)

