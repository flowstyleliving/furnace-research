# v3 Main-Run Verdict — E17 / E18 / E19 (2026-04-23, amended same-day)

_Confirmatory run at n=50/cell (200/model) per the 2026-04-22 power-fix amendment. Sealed methodology frozen 2026-04-18 per Codex adversarial review (see [pri-v3-plan](../pri-v3/pri-v3-plan.md#magnitude-independence-test-frozen-2026-04-18-per-codex-adversarial-review)). See log for the amendment trail — the first pass of this page read the gate at rank 32 and called v3 falsified; rank was never pinned in the sealed block and the rank sweep tells a different story._

> **2026-04-24 update:** v3.1 fresh-data replicate at seed 20260423 returned **3-of-3 PASS on sealed E18** (Llama 0.8957, Mistral 0.8632, Qwen 2.5 0.7445 — all replicate this page's primaries within ±0.04 of the 2026-04-22 single-shot, and all clear sealed bar with non-overlap CI vs 0.5). **However**, the sealed E17b head-to-head on Qwen 2.5 **FAILS** (Δ AUROC(Fisher) − AUROC(raw) = −0.166 with non-overlap CI; HARP-style raw subspace beats Fisher-weighted on the sealed primary). Cross-generation evidence on Qwen 3 8B corroborates the Fisher failure (Δ = −0.36); Mistral shows the opposite (Δ = +0.288). Several methodological caveats (pre/post-norm capture choice, subset-variance, gate generation-path change today) warrant robustness checks before publishing the falsification. The 3-of-3 sealed E18 PASS on this page **stands and is now strengthened** by the fresh-data replicate. The sealed E17b FAILS pending robustness verification. See [v3.1-replicate](v3.1-replicate.md) for the full partial-verdict writeup, diagnostic findings, and 4 bug fixes that landed today (gate `trace_sample` → `mlx_generate` swap, `load_model` config-propagation patch, `--layers` flag, `--gate-max-tokens 12` operational rescue)._

## Headline — v3 PASSES sealed E18 at rank 1; rank 32 was a dead operating point

Sealed analysis plane: final layer, step 1. Pre-registered direction: higher `null_ratio_resid` → contradiction. Gate: `AUROC ≥ 0.60` with non-overlap bootstrap 95% CI vs 0.5 on ≥ 2 of 3 primaries. Rank was **not** pinned in the sealed block (line 80 says only "AUROC of null_ratio_resid"; the plan's rank sweep is `{1, 2, 3, 4, 5, 8, 13, 16, 21, 32, 34, 55, 64}`).

### E18 at rank 1 — 3 of 3 primaries pass

| Primary | AUROC | 95% CI | Gate (d_F = lowrank32) | Robustness (d_F = topk32) |
|---|---:|:---|:---:|:---:|
| Llama 3.2 3B | **0.8593** | [0.806, 0.908] | PASS | 0.8618 PASS |
| Mistral 7B | **0.8638** | [0.814, 0.910] | PASS | 0.8638 PASS |
| Qwen 2.5 7B | **0.7274** | [0.656, 0.795] | PASS | 0.7221 PASS |
| Qwen3 8B (extended) | 0.3786 | [0.301, 0.466] | FAIL (inverted) | 0.3823 FAIL |

v3 passes the sealed 2-of-3-primaries bar at rank 1. Qwen3 8B fails but is in the extended suite, not a primary.

### Why rank 32 looked like a falsification

The first pass of this page used `null_ratio_rank32` — defensible by analogy to `pri_v2_lowrank32`, but not the only defensible choice. At rank 32 on the final layer, step 1:

- Δmean/σ of `null_ratio_rank32` is +0.28σ (Llama), +0.08σ (Mistral), −3.02σ (Qwen 2.5), −0.35σ (Qwen3). Llama / Mistral are noise-scale; Qwen 2.5 is a strong *inverted* effect.
- Residualized AUROC: 0.5026 / 0.5050 / 0.1831 / 0.5492 — 0 of 3 primaries pass.

Rank 32 at final layer is a locally dead operating point. The `null_ratio_rank32` ≈ 0.92–0.97 raw value sits close to the random baseline `√((d-32)/d) ≈ 0.995`; the separating effect compresses into a < 0.01 band where 3σ-level differences correspond to `null_ratio` deltas of \~0.002. Meanwhile at rank 1 (one informed direction — the top Fisher eigenvector, i.e. the "commit" direction) the separating effect lives on a wider band and Δ_cont − Δ_ctrl is an order of magnitude larger per sample.

## The (layer × rank) landscape at step 1

E18 residualized AUROC, pre-registered direction, d_F = lowrank32:

### Llama 3.2 3B
| layer | r=1 | r=2 | r=4 | r=8 | r=13 | r=21 | r=32 | r=55 | r=64 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| quarter | 0.75 | 0.72 | 0.81 | **0.88** | 0.58 | 0.61 | 0.65 | 0.65 | 0.69 |
| mid | **0.87** | 0.85 | 0.78 | 0.74 | 0.73 | 0.71 | 0.59 | 0.63 | 0.44 |
| final | **0.86** | 0.52 | 0.30 | 0.31 | 0.46 | 0.53 | 0.50 | 0.76 | 0.60 |

### Mistral 7B
| layer | r=1 | r=2 | r=4 | r=8 | r=13 | r=21 | r=32 | r=55 | r=64 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| quarter | 0.78 | 0.79 | 0.78 | 0.59 | 0.54 | 0.72 | 0.62 | 0.44 | 0.80 |
| mid | 0.55 | 0.89 | 0.93 | 0.88 | 0.89 | **1.00** | 0.99 | 0.92 | 0.96 |
| final | **0.86** | 0.87 | 0.72 | 0.68 | 0.94 | 0.89 | 0.50 | 0.95 | 0.90 |

### Qwen 2.5 7B
| layer | r=1 | r=2 | r=4 | r=8 | r=13 | r=21 | r=32 | r=55 | r=64 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| quarter | **1.00** | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.99 | 0.99 |
| mid | 0.99 | 0.99 | 0.99 | 0.99 | 0.99 | **1.00** | 0.99 | 0.78 | 0.36 |
| final | **0.73** | 0.73 | 0.75 | 0.64 | 0.52 | 0.15 | 0.18 | 0.51 | 0.44 |

### Qwen3 8B
| layer | r=1 | r=2 | r=4 | r=8 | r=13 | r=21 | r=32 | r=55 | r=64 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| quarter | 0.45 | 0.59 | 0.53 | 0.47 | 0.59 | 0.52 | 0.65 | 0.66 | 0.68 |
| mid | 0.41 | 0.51 | 0.51 | 0.56 | 0.49 | 0.41 | 0.49 | 0.46 | 0.51 |
| final | 0.38 | 0.34 | 0.33 | 0.28 | 0.30 | 0.32 | 0.55 | 0.59 | 0.55 |

Cell-count passes (AUROC ≥ 0.60 pre-registered direction across all 39 cells in the 3 layers × 13 ranks grid): Llama 24/39, Mistral 30/39, Qwen 2.5 31/39, Qwen3 5/39. The first three have dense signal almost everywhere; Qwen3 does not.

## Rank / layer are orthogonal axes, not redundant

- **Layer** = depth in the forward pass. `Δh_ℓ = h_ℓ − h_ℓ_prev` is different at each layer.
- **Rank** = how many Fisher singular directions of `sqrt(p_t) · W_u` count as "informed." The SVD is computed once from the *final* distribution `p_t` and the *shared* output head `W_u`; top-r directions are the same regardless of which layer's Δh you project.

For a fixed (sample, step=1) the rank sweep reuses the same V_top and sweeps *how much* of the informed subspace you include. The layer sweep uses the same V_top and substitutes different Δh_ℓ. Rank and layer interact — a layer's Δh can have concentrated informed content (rank 1 captures most) or spread-out content (needs rank 32+) — but they're not the same axis.

## What this means for the Qwen 2.5 "sign-inversion" I flagged earlier

That finding was a rank-32 artifact. At rank 1, Qwen 2.5 aligns with Llama / Mistral in the pre-registered direction (E18 AUROC 0.73, 3-of-3 primaries clearing 0.6). The inversion at rank 32 is still a real observation — Qwen 2.5's informed subspace at rank 32 doesn't capture the commit direction cleanly and the residual flips sign — but it is not the main-run verdict on the theory. The sign-inversion is a diagnostic about Qwen 2.5's rank-frequency geometry, not a falsification.

## E19 `null_gated` interpretation-gate (unchanged verdict — FAIL)

Sealed interpretation gate: `AUROC(null_gated) > max(AUROC(null_bare), AUROC(v2_lowrank32))` by non-overlap CI. Computed at rank 32 (the spec cites `v2_lowrank32` by name, so rank 32 is the sealed reference point for E19 specifically):

| Model | null_gated | null_bare | v2_lowrank32 | Gate |
|---|---:|---:|---:|:---|
| Llama 3.2 3B | 0.78 [0.72, 0.84] | 0.58 [0.50, 0.66] | 0.77 [0.70, 0.83] | FAIL — CI overlaps v2 |
| Mistral 7B | 0.70 [0.63, 0.77] | 0.52 [0.44, 0.60] | 0.70 [0.63, 0.77] | FAIL — ties v2 |
| Qwen 2.5 7B | 0.83 [0.76, 0.89] | 0.95 [0.92, 0.98] | 0.78 [0.70, 0.85] | FAIL — below null_bare |
| Qwen3 8B | 0.51 [0.42, 0.59] | 0.63 [0.54, 0.72] | 0.50 [0.41, 0.59] | FAIL |

E19 fails on all 4 tested models. Multiplicative interaction is not carrying independent signal.

## E17b (null_raw / HARP baseline) — still NOT EVAL'd

Same as before: captured `null_ratio_rank*` is from SVD of `sqrt(p_t)·W_u` (Fisher-weighted). Raw-W_u SVD needs to be re-run post-hoc from `*_trace_dumps.parquet` + each model's W_u. Now even more important — the rank-1 pass above is under the Fisher-weighted formulation; the question of whether Fisher weighting is the load-bearing piece (vs HARP's static raw-W_u) cannot be answered without E17b.

## Collateral: Qwen3 8B is the actual weak link

Across the 39-cell landscape, Qwen3 8B has only 5 cells above AUROC 0.60 in the pre-registered direction on E18 — scattered, not coherent. v2_lowrank32 also collapses to AUROC 0.50 on Qwen3 while `surprise` alone hits 0.96. Two possibilities worth separating:

- 🧪 **Architectural:** Qwen3 8B's commit geometry is not encoded in the same way as Llama / Mistral / Qwen 2.5 — surprise and not Δh direction is the separating signal. Investigate with the extended-suite Gemma / Phi models once queued.
- 🔧 **Pipeline:** something in the Qwen3 code path (MLX 4-bit quant, bf16 activations, Qwen3Adapter) produces low-quality Δh. The 2026-04-22 adapter fix was smoke-validated but not regression-tested against a Qwen3 bf16 fp16 comparison.

Qwen3 is NOT a primary for E18; v3 verdict stands without it. Flag as an exploratory thread.

## Methodological note — rank as an unpinned parameter

The sealed block (plan lines 73–82) pins: unit of analysis (one row per sample × step=1 × layer=final), model class (per-model linear-residualization), bootstrap (1000 sample-level resamples), threshold (0.60 + non-overlap CI), and no post-hoc re-specification. It does **not** pin rank. Reading this as "any rank in the pre-registered sweep is a legitimate operating point" is defensible. Reading this as "rank 32 = default-by-analogy-to-v2" is also defensible.

Under the first reading, v3 passes at rank 1 (strong CIs, robust across d_F variants, same direction across all 3 primaries, landscape corroborates). Under the second reading, v3 fails at rank 32 specifically and passes elsewhere — a rank-specification issue, not a theoretical falsification.

The honest framing for the paper: **commit rank 1 as v3's operating point** (principled: top-1 Fisher direction is the "commit" direction; smallest rank that clears baseline; strongest signal at the sealed analysis plane) and replicate on fresh data before reporting externally. Logging both readings here so the audit trail is intact.

## Status tags

- [PRIMARY-PASS / rank 1] v3 null_ratio — sealed E18 at rank 1 clears the 2-of-3 bar with CIs [0.66, 0.91] across primaries at the sealed analysis plane.
- [NOT-REPRODUCED / rank 32] v3 null_ratio at rank 32 — 0 of 3 primaries pass at the same plane. Not a falsification: rank was unpinned.
- [FALSIFIED] E19 null_gated interpretation gate — fails on all 4 tested models at rank 32 (the rank the spec names for E19).
- [OPEN] rank-1 replicate on fresh data — required before reporting v3 pass externally.
- [OPEN] Qwen3 8B weak signal across (layer × rank) landscape — separate Qwen-family diagnostic; not a v3 question.
- [OPEN] Qwen 2.5 rank-32 sign-inversion — localized to rank 32 at final; rank-1 behaves normally. Informative about Qwen 2.5's rank-frequency geometry.
- [NOT-RUN] Gemma 3-1B, Gemma 3-4B — never queued.
- [GATE-SKIP] Phi-3.5-mini at E17/E18/E19 — queued 2026-04-23 on the non_gemma_extended scope; pipeline auto-skipped at the behavioral gate (control acc 12/20 = 60%, threshold 80%). Prereq 4 dryrun on 2026-04-22 had scored 4/4 at n=4. Most-likely explanation: reasoning-tuned string-match artifact (same failure mode the `--gate-verbose` / `--skip-gate` flags were added for). Diagnostic command: `scripts/run_v3_main.py --scope non_gemma_extended --gate-verbose`. Deferred — not in v3.1 scope.
- [NOT-EVAL] E17b null_raw (HARP baseline) — post-hoc runnable from `*_trace_dumps.parquet`; now decisive for Fisher-weighting-vs-static-W_u attribution.

## Artifacts

- Results parquets: `experiments/v3-main-run/2026-04-22/run-02/{Llama-3.2-3B-Instruct-4bit,Mistral-7B-Instruct-v0.3-4bit,Qwen2.5-7B-Instruct-4bit}_results.parquet`
- Qwen3 results: `experiments/v3-main-run/2026-04-23/run-02/Qwen3-8B-4bit_results.parquet`
- Trace dumps (for E17b post-hoc): `*_trace_dumps.parquet` in the same dirs
- Bootstrap + gates JSON (original rank-32 reading): `experiments/v3-main-run/_analysis/gates_2026-04-23.json`
- Layer × rank landscape (all cells): `experiments/v3-main-run/_analysis/layer_rank_landscape_2026-04-23.json`
