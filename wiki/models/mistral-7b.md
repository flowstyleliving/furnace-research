# Mistral 7B Instruct v0.3 (4-bit)

MLX handle: `mlx-community/Mistral-7B-Instruct-v0.3-4bit`

## Specs
- Size: 7B parameters
- Quantization: 4-bit (MLX)
- Tokenizer notes: —

## PRI v1 Results
- AUROC: — (pending parquet load)
- Hedges g: —
- Bootstrap p: —

## PRI v2 Results (step 1, final layer, α = 1.0)
- **Best variant: `pri_v2_topk32` — AUROC 0.6715**
- Behavioral gate: control acc 1.00, contradiction acc 1.00
- Notably weakest of the three primary models on AUROC.

## Observed Quirks
- Like Llama, prefers top-k over low-rank — suggests a Llama/Mistral vs Qwen axis on FIM structure.

## Trace Dump Notes
- `PRI_at_commitment/pri_v2_results/Mistral-7B-Instruct-v0.3-4bit_trace_dumps.parquet` present.

## Open Questions
- Why the AUROC gap vs Llama 3B (0.67 vs 0.77) despite larger model — is it the tokenizer, the layer choice, or a real signal difference?
- Does penultimate-layer probing (E07) close the gap?

---

## v3.1 results (n=600, post-norm geometry, run-09 2026-04-26)

**Sealed primary** (gate authority for sealed E18). **Motif 3 — chain-length × rank Simpson's-paradox.** Updated 2026-04-27.

### Architectural details surfaced during v3 onboarding
- Layers 32; hidden_dim D = 4096; vocab V = 32,768
- Dtype: float16 (lm_head)
- Output projection: untied `lm_head`
- Class: `mlx_lm.models.mistral.Model` with sliding-window-attention (`core.swa_idx`, distinct from Gemma's `sliding_window_pattern`)

### Sealed E18 verdict — PASS
- AUROC = **0.8707** [0.845, 0.897], sign +1 — clears 0.60 threshold by 4.4×, non-overlap 95% CI vs 0.5
- n=200 prelim (run-02): 0.8797 [0.828, 0.921] — within bootstrap noise

### E17b head-to-head — Raw decisive on pool, BUT Simpson's-paradox under stratification
- **Pool: Δ_oriented = −0.140 [−0.173, −0.107]** at sealed r=1 — Raw decisive
- **cl=2: Δ_oriented = +0.065 [+0.041, +0.093]** — **Fisher decisive** (CI fully positive)
- **cl=5: Δ_oriented = +0.002 [−0.022, +0.028]** — tied
- **Mistral is never Raw-decisive at the stratum level.** The pooled "Raw decisive" verdict is a Simpson's-paradox artifact of mixing chain-length subgroups whose Fisher and Raw discrimination axes have different orientations relative to contradiction.

### Motif 3 — TWO Simpson's-paradox sites
1. **r=1 (sealed):** pool R, cl=2 F decisive, cl=5 tied. Pool's "Raw" is mixing artifact (above).
2. **r=32:** pool F (+0.177), cl=2 R (−0.196 [−0.262, −0.131]), cl=5 F (+0.379 [+0.319, +0.450]) — both stratum CIs non-overlapping in opposite directions. **Δ_cross = −0.575**, the **largest cross-stratum spread observed across the entire 156-cell model × rank × chain_length grid**. r=34 mirrors at Δ_cross = −0.561.

### gen_step=1 commit pattern — newline-commit
- All 100 Mistral samples emit `'\n'` as the first generated token (Codex 2nd-rescue diagnosis 2026-04-25). Mistral writes a newline before the answer; the gen_step=1 commit is "begin the answer block" rather than committing to actual answer content.
- This is the mechanistic hypothesis for the chain-length × rank interaction: the newline's geometric position relative to the contradiction event in token-space shifts dramatically with chain depth (cl=2 places contradiction close to the commit; cl=5 diffuses it across intermediate reasoning tokens).
- Distinct from Qwen-family / Phi / Gemma 4B which front-load actual answer content (`Answer:` / `YES` / `NO`) at gen_step=1.

### W_u top-1 token analysis (post-J_n correction, replicated 2026-04-30 at N=100)

Diagnostic: `scripts/diagnostics/diagnose_raw_top1.py --model mlx-community/Mistral-7B-Instruct-v0.3-4bit`. CSV at `experiments/v3-main-run/2026-04-30/Mistral-7B-Instruct-v0.3-4bit_signed_proj.csv` (replicates the 2026-04-25 reading at `experiments/v3-main-run/2026-04-24/mistral_signed_proj.csv` to 3 decimals — cross-rerun reproducibility check ✓).

**Spectrum.** σ_1 = 17.26 (smallest σ_1 in the lineup), σ_1 / σ_2 = 5.00× — moderate gap.

**V_raw[0] character — non-content rupture-magnitude axis (native +).** Top-3 positive tokens: `(`, `\n`, `and`. Top-3 negative tokens: `qpoint`, `ICENSE`, `ityEngine` (code-domain fragments — characteristic of Mistral's training corpus). Targeted projections: `' YES'` = +0.034, `' NO'` = −0.028, `'\n'` = +0.127. YES/NO magnitudes are negligible; `\n` is a stronger projection — V_raw[0] is anchored to the structural commit, not to answer content.

**Per-sample signed Δh_jn · V_raw[0]:** ctrl mean +3.011 ± 0.411, contr mean +4.644 ± 0.520, **Δ (contr − ctrl) = +1.632**, ctrl frac>0 = 100%, contr frac>0 = 100%. **All 100 samples (both ctrl and contr) project positively onto V_raw[0]; magnitude separates them.** Cohen's-d-equivalent ≈ 3.5 — the **strongest V_raw[0] separation in the lineup**.

**Mechanism for Raw saturation at sealed r=1.** V_raw[0] is anchored to `\n` (the gen_step=1 commit token, 100/100). Δh_jn at the commit moment lands monotonically on V_raw[0]; magnitude scales with rupture intensity. Mistral and Phi share this regime via different vocabulary-specific top-token signatures (Mistral: code-domain; Phi: European-language fragments) — see paper §5.1 Table 5.

### Trace dump pointers
- n=600 powered: `experiments/v3-main-run/2026-04-26/run-09/Mistral-7B-Instruct-v0.3-4bit_results.parquet`
- n=200 prelim: `experiments/v3-main-run/2026-04-26/run-02/Mistral-7B-Instruct-v0.3-4bit_results.parquet`

### Cross-references
- Cross-architecture analysis: [results/v3.1-replicate](../results/v3.1-replicate.md) §Three architecture-dependence motifs
- Paper Motif 3 framing + Fig 9: [paper/pri-draft.md](../paper/pri-draft.md) §4.3

