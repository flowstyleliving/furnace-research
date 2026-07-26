# Results History (append-only)

Format: `## [YYYY-MM-DD] <model> | <metric> | <value> | <notes>`

<!-- entries appended below -->

## [2026-04-07] Llama-3.2-3B-Instruct-4bit | score (tiny slice) | 0.500 | commit f3dcdb4 — baseline 32-pass cycle
## [2026-04-07] Llama-3.2-3B-Instruct-4bit | score (tiny slice) | 0.750 | commit f3dcdb4 — baseline pri_v2_full
## [2026-04-07] Llama-3.2-3B-Instruct-4bit | score (tiny slice) | 0.750 | commit 6aa5130 — baseline pri_v2_full current-head
## [2026-04-07] Llama-3.2-3B-Instruct-4bit | score (tiny slice) | 0.7656 | commit faa8b0b — experiment: postnorm final hidden (KEEP)
## [2026-04-07] Llama-3.2-3B-Instruct-4bit | score (tiny slice) | 0.8594 | commit 0963932 — experiment: pullback-only pri_v2 (KEEP)
## [2026-04-07] Llama-3.2-3B-Instruct-4bit | score (tiny slice) | 0.8750 | commit 3d2ccd7 — experiment: normalize pullback by hidden motion (KEEP — last verified single-model keep)
## [2026-04-07] Llama-3.2-3B-Instruct-4bit | score (tiny slice) | 0.5312 | commit 36d7926 — pre-commit token probs for FIM (DISCARD)
## [2026-04-07] Llama-3.2-3B-Instruct-4bit | score (tiny slice) | 0.0938 | commit 6bf7e1f — explicit answer cue (DISCARD)
## [2026-04-12] Llama-3.2-3B-Instruct-4bit | AUROC step1 final α=1 pri_v2_topk32 | 0.7666 | full three-model run, PRI_at_commitment/pri_v2_results/
## [2026-04-12] Mistral-7B-Instruct-v0.3-4bit | AUROC step1 final α=1 pri_v2_topk32 | 0.6715 | full three-model run
## [2026-04-12] Qwen2.5-7B-Instruct-4bit | AUROC step1 final α=1 pri_v2_lowrank32 | 0.7858 | full three-model run
## [2026-04-09] autoresearch loop | E01/E02/E03 | nan | GATE_FAIL, gate=0/0 — loop not executing
## [2026-04-10] autoresearch loop | E01/E02/E03 | nan | GATE_FAIL (day 2)
## [2026-04-11] autoresearch loop | E01/E02/E03 | nan | GATE_FAIL (day 3)
## [2026-04-12] autoresearch loop | E01/E02/E03 | nan | GATE_FAIL (day 4) — root cause still unknown


## [2026-04-23] Llama-3.2-3B-Instruct-4bit | AUROC E18 null_ratio_resid (d_F=lowrank32, one-sided) | 0.5026 | n=50/cell, CI [0.417,0.579], FAIL sealed E18
## [2026-04-23] Mistral-7B-Instruct-v0.3-4bit | AUROC E18 null_ratio_resid (d_F=lowrank32, one-sided) | 0.5050 | n=50/cell, CI [0.421,0.590], FAIL sealed E18
## [2026-04-23] Qwen2.5-7B-Instruct-4bit | AUROC E18 null_ratio_resid (d_F=lowrank32, one-sided) | 0.1831 | n=50/cell, CI [0.130,0.240], FAIL sealed E18 — inverted sign
## [2026-04-23] Qwen3-8B-4bit | AUROC E18 null_ratio_resid (d_F=lowrank32, one-sided) | 0.5492 | n=50/cell, CI [0.467,0.626], FAIL sealed E18
## [2026-04-23] Llama-3.2-3B-Instruct-4bit | AUROC E17 null_bare rank32 (two-sided) | 0.5806 | n=50/cell, CI [0.497,0.664]
## [2026-04-23] Mistral-7B-Instruct-v0.3-4bit | AUROC E17 null_bare rank32 (two-sided) | 0.5173 | n=50/cell, CI [0.437,0.602]
## [2026-04-23] Qwen2.5-7B-Instruct-4bit | AUROC E17 null_bare rank32 (two-sided) | 0.9532 | n=50/cell, CI [0.919,0.979], sign=-1 (inverted)
## [2026-04-23] Qwen3-8B-4bit | AUROC E17 null_bare rank32 (two-sided) | 0.6308 | n=50/cell, CI [0.544,0.719]
## [2026-04-23] Llama-3.2-3B-Instruct-4bit | AUROC E19 null_gated lowrank32 (two-sided) | 0.7796 | n=50/cell, CI [0.717,0.838], FAIL interp-gate (overlaps v2)
## [2026-04-23] Mistral-7B-Instruct-v0.3-4bit | AUROC E19 null_gated lowrank32 (two-sided) | 0.7035 | n=50/cell, CI [0.631,0.772], FAIL interp-gate (ties v2)
## [2026-04-23] Qwen2.5-7B-Instruct-4bit | AUROC E19 null_gated lowrank32 (two-sided) | 0.8329 | n=50/cell, CI [0.763,0.893], FAIL interp-gate (below null_bare)
## [2026-04-23] Qwen3-8B-4bit | AUROC E19 null_gated lowrank32 (two-sided) | 0.5054 | n=50/cell, CI [0.415,0.589], FAIL interp-gate
## [2026-04-23] Qwen3-8B-4bit | AUROC v2_lowrank32 (two-sided) | 0.5033 | n=50/cell — v2 collapse on Qwen3 (surprise alone 0.9559)
## [2026-04-23] Qwen3-8B-4bit | AUROC surprise alone | 0.9559 | n=50/cell, CI [0.928,0.980]


## [2026-04-23] AMENDMENT: rank was not pinned in sealed E18 block — rank-1 verdict supersedes rank-32 rows above
## [2026-04-23] Llama-3.2-3B-Instruct-4bit | AUROC E18 null_ratio_resid rank1 (d_F=lowrank32, one-sided) | 0.8593 | n=50/cell, CI [0.8055,0.9082], PASS sealed E18
## [2026-04-23] Mistral-7B-Instruct-v0.3-4bit | AUROC E18 null_ratio_resid rank1 (d_F=lowrank32, one-sided) | 0.8638 | n=50/cell, CI [0.8143,0.9098], PASS sealed E18
## [2026-04-23] Qwen2.5-7B-Instruct-4bit | AUROC E18 null_ratio_resid rank1 (d_F=lowrank32, one-sided) | 0.7274 | n=50/cell, CI [0.6557,0.7947], PASS sealed E18
## [2026-04-23] Qwen3-8B-4bit | AUROC E18 null_ratio_resid rank1 (d_F=lowrank32, one-sided) | 0.3786 | n=50/cell, CI [0.3009,0.4655], FAIL inverted (extended, not primary)
## [2026-04-23] Llama-3.2-3B-Instruct-4bit | AUROC E18 null_ratio_resid rank1 (d_F=topk32, one-sided) | 0.8618 | robustness check, PASS
## [2026-04-23] Mistral-7B-Instruct-v0.3-4bit | AUROC E18 null_ratio_resid rank1 (d_F=topk32, one-sided) | 0.8638 | robustness check, PASS
## [2026-04-23] Qwen2.5-7B-Instruct-4bit | AUROC E18 null_ratio_resid rank1 (d_F=topk32, one-sided) | 0.7221 | robustness check, PASS

## [2026-04-24] AMENDMENT: v3.1 sealed-gate replicate at fresh seed 20260423 — partial (1-of-3 primaries cleared E18; Llama 3B + Qwen 2.5 gate-skipped at post-fix stratified preflight, operational not sealed-spec)
## [2026-04-24] Mistral-7B-Instruct-v0.3-4bit | AUROC E18 null_ratio_resid rank1 (d_F=lowrank32, one-sided) | 0.8632 | n=50/cell, CI [0.8092,0.9104], PASS sealed E18 — fresh-data replicate of 2026-04-22 (0.8638) within 0.0006
## [2026-04-24] Mistral-7B-Instruct-v0.3-4bit | AUROC E18 null_ratio_resid rank1 (d_F=topk32, one-sided) | 0.8629 | n=50/cell, CI [0.8090,0.9103], robustness check PASS
## [2026-04-24] Mistral-7B-Instruct-v0.3-4bit | AUROC E17 null_bare rank1 (one-sided) | 0.8054 | n=50/cell, CI [0.7388,0.8636], sign=+1
## [2026-04-24] Mistral-7B-Instruct-v0.3-4bit | AUROC E17b null_raw rank1 (one-sided) | 0.5177 | n=50/cell, CI [0.4360,0.5956], sign=-1 (raw basis near baseline)
## [2026-04-24] Mistral-7B-Instruct-v0.3-4bit | E17b head-to-head: Δ AUROC(null_ratio_rank1) − AUROC(null_ratio_raw_rank1) | +0.288 | n=50/cell, CI [0.202,0.376] — Fisher basis crushes raw on Mistral (descriptive; sealed E17b is on Qwen 2.5)
## [2026-04-24] Mistral-7B-Instruct-v0.3-4bit | baseline_v2_lowrank32 | 0.6910 | n=50/cell, CI [0.6154,0.7635]
## [2026-04-24] Llama-3.2-3B-Instruct-4bit | behavioral gate (post-PR#6 stratified, mlx_generate path) | 15/20 = 75% | seed 20260423, gate-skipped — no main-run data
## [2026-04-24] Qwen2.5-7B-Instruct-4bit | behavioral gate (post-PR#6 stratified, mlx_generate path) | 14/20 = 70% | seed 20260423, gate-skipped — verbose diagnostic shows 6/6 MISS outputs front-load 'Answer: YES' but Tier 1 picks last 'Answer:' from format-completion continuation; parser issue, not model competence


## [2026-04-24] AMENDMENT: post-rescue 3-of-3 sealed E18 PASS + sealed E17b FAIL on Qwen 2.5
## [2026-04-24] Llama-3.2-3B-Instruct-4bit | AUROC E18 null_ratio_resid rank1 (d_F=lowrank32, one-sided) | 0.8957 | n=50/cell, CI [0.853,0.935], PASS sealed E18 — fresh-data replicate of 2026-04-22 (0.8593) +0.036 stronger; baselines also shifted up
## [2026-04-24] Llama-3.2-3B-Instruct-4bit | behavioral gate (post --gate-max-tokens 12) | 20/20 = 100% | seed 20260423, recovered after diagnostic showed format-completion was identical pattern to Qwen 2.5
## [2026-04-24] Qwen2.5-7B-Instruct-4bit | AUROC E18 null_ratio_resid rank1 (d_F=lowrank32, one-sided) | 0.7445 | n=50/cell, CI [0.674,0.806], PASS sealed E18 — fresh-data replicate of 2026-04-22 (0.7274) +0.017
## [2026-04-24] Qwen2.5-7B-Instruct-4bit | behavioral gate (post --gate-max-tokens 12) | 20/20 = 100% | seed 20260423, recovered (was 14/20 pre-fix at 256-token gate budget)
## [2026-04-24] Qwen2.5-7B-Instruct-4bit | AUROC null_ratio_rank1 (Fisher, one-sided) | 0.7665 | n=50/cell, sign=-1 INVERTED — Δ contradiction-control = -0.0023, contradictions concentrate INTO Fisher top-1 subspace
## [2026-04-24] Qwen2.5-7B-Instruct-4bit | AUROC null_ratio_raw_rank1 (HARP raw W_u, one-sided) | 0.9323 | n=50/cell, sign=+1 — Δ contradiction-control = +0.0045, contradictions concentrate OUT OF raw top-1 subspace
## [2026-04-24] Qwen2.5-7B-Instruct-4bit | E17b SEALED head-to-head Δ AUROC(Fisher) − AUROC(raw) at rank 1 | -0.166 | n=50/cell, CI [-0.240,-0.098] (delta CI fully NEGATIVE) — FAIL sealed E17b (need delta>=+0.02 with CI>0). HARP-style raw subspace beats Fisher-weighted on Qwen 2.5 by 0.17 AUROC with non-overlap CI. Pre-registered falsification criterion fires.
## [2026-04-24] Qwen2.5-7B-Instruct-4bit | Fisher SVD energy concentration in top-1 (final, step=1) | 0.998 | vs Llama 0.973, Mistral 0.962 — Qwen Fisher SVD nearly rank-1 collapsed at this analysis plane
## [2026-04-24] Qwen2.5-7B-Instruct-4bit | DIAGNOSTIC cos(Fisher_top1, Raw_top1) at final/step=1 | ~0.10 (range -0.087 to +0.184 across N=10) | bases nearly orthogonal; explains AUROC-sign disagreement vs Mistral where bases agree
## [2026-04-24] Qwen2.5-7B-Instruct-4bit | DIAGNOSTIC cos(Δh_pre, Δh_post-norm) | ~0.94 | small geometric mismatch between pre-norm capture plane and post-norm projection basis; can flip null_ratio sign at small magnitudes (Δ ~0.002). Robustness rerun pending.


## [2026-04-25] AMENDMENT: J_n correction discovered — Fisher pullback was missing RMSNorm Jacobian; cross-model E17b verdict reshapes
## [2026-04-25] Llama-3.2-3B-Instruct-4bit | DIAGNOSTIC Δ AUROC(Fisher) − AUROC(raw) at rank=1 (N=100) | pre-norm: -0.033 [-0.10,+0.05]; J_n: +0.054 [-0.13,+0.22]; post-norm: -0.034 [-0.10,+0.04] | indeterminate either reading
## [2026-04-25] Mistral-7B-Instruct-v0.3-4bit | DIAGNOSTIC Δ AUROC(Fisher) − AUROC(raw) at rank=1 (N=100) | pre-norm: +0.112 [+0.05,+0.18]; J_n: -0.184 [-0.27,-0.11]; post-norm: -0.286 [-0.43,-0.14] | J_n flips Mistral from Fisher slight-win to raw decisive-win with non-overlap CI
## [2026-04-25] Qwen2.5-7B-Instruct-4bit | DIAGNOSTIC Δ AUROC(Fisher) − AUROC(raw) at rank=1 (N=100) | pre-norm: -0.018 [-0.08,+0.03]; J_n: +0.015 [-0.08,+0.12]; post-norm: -0.014 [-0.06,+0.02] | indeterminate either reading; sealed +0.02 bar UNCLEARED at N=100
## [2026-04-25] Qwen3-8B-4bit | DIAGNOSTIC Δ AUROC(Fisher) − AUROC(raw) at rank=1 (N=100) | pre-norm: -0.278 [-0.41,-0.15]; J_n: +0.206 [+0.03,+0.39]; post-norm: -0.361 [-0.51,-0.21] | J_n flips Qwen 3 from raw decisive-win to Fisher decisive-win with non-overlap CI
## [2026-04-25] Mistral raw_top1 mechanism | per-sample signed projection on Vt_raw[0] | ctrl mean=+3.01 std=0.41; contr mean=+4.64 std=0.52; 100% both classes positive | raw_top1 is rupture-MAGNITUDE axis, not YES/NO bipolar
## [2026-04-25] Mistral gen_step=1 first-token distribution | 100/100 = '
' | model writes newline before answer; Qwen-family front-loads ' Answer'/'YES'/'NO'
## [2026-04-25] CJK hypothesis on Qwen W_u SVD | preliminary NEGATIVE within token IDs 0-16K | top-r SVD vectors dominated by ASCII/code/punct tokens; CJK tokens likely live at higher IDs and weren't sampled. Future-paper line.


## [2026-05-15] Δσ_onaxis 7-model panel @ gen_step=1 / layer=final / n=200 — bivariate (null·Δσ_n) hypothesis [OPEN, leaning NEGATIVE]
## [2026-05-15] Llama-3.2-3B-Instruct-4bit | AUROC null_ratio_post_rank32 | 0.6176 (sign −) | n=200, best null cell; Δσ_n adds nothing (best Δσ_n=0.6003 @ r=2)
## [2026-05-15] Mistral-7B-Instruct-v0.3-4bit | AUROC null_ratio_post_rank2 | 0.7600 (sign +) | n=200, best null cell
## [2026-05-15] Mistral-7B-Instruct-v0.3-4bit | AUROC bivariate (null·Δσ_n) rank16 | 0.7411 (sign +) | n=200, only +0.014 bivar-over-null lift in panel; corr(null,Δσ_n)=+0.50 at this rank
## [2026-05-15] Phi-3.5-mini-instruct-4bit | AUROC Δσ_onaxis_norm_rank2 | 0.7386 (sign −) | n=200, Δσ_n ALONE beats best null (0.5854 @ r=8) by +0.153; anti-predictive sign — contradictions concentrate INTO single on-axis direction
## [2026-05-15] Phi-4-mini-instruct-4bit | AUROC Δσ_onaxis_norm_rank4 | 0.7225 (sign +) | n=200, Δσ_n ALONE beats best null (0.6719 @ r=2) by +0.051; canonical sign — OPPOSITE of Phi-3.5
## [2026-05-15] Qwen2.5-7B-Instruct-4bit | AUROC null_ratio_post_rank32 | 0.8076 (sign +) | n=200, best in panel; corr(null,Δσ_n)=−0.83 at r=4 — channels encode opposite information, bivariate composite DEGRADES to 0.5843 at r=32
## [2026-05-15] Qwen3-8B-4bit | AUROC null_ratio_post_rank8 | 0.6848 (sign −) | n=200, weakest in panel; consistent with v3.1/v3.2 Fisher-basis collapse on Qwen 3
## [2026-05-15] Gemma-3-4B-Instruct-4bit | AUROC null_ratio_post_rank8 | 0.6637 (sign −) | n=200, best null cell; Δσ_n at r=16 (0.6574) within 0.01
## [2026-05-15] CROSS-MODEL corr(null_ratio, Δσ_onaxis_norm) range | [−0.83, +0.50] across 7 models × 5 ranks | SUP ℏ=√(Δμ·Δσ) predicted-orthogonality narrative does not hold cross-family; multiplicative composite hypothesis falsified on Qwen 2.5 (corr=−0.83)
## [2026-05-15] CROSS-MODEL fisher_energy_rank4 | ≥ 0.95 on 6 of 7 models (Llama 3B = 0.79) | on-axis subspace saturated by r=4; further rank increases mostly redistribute energy already inside the cone


## [2026-05-15] Inter-head attention disagreement at commit step, W_u-free pivot — JS-radius sign-stable, magnitude not [OPEN, mildly encouraging]
## [2026-05-15] Mistral-7B-Instruct-v0.3-4bit | AUROC JS-radius @ final block | 0.7401 (sign −) | n=200 ANLI R1, gen_step=1; LOW head disagreement predicts contradiction
## [2026-05-15] Mistral-7B-Instruct-v0.3-4bit | AUROC JS-radius @ mid block | 0.7148 (sign +) | n=200, mid-block sign flips vs final — feature, not bug
## [2026-05-15] Mistral-7B-Instruct-v0.3-4bit | AUROC JS-radius @ last-1 block | 0.7126 (sign −) | n=200, agrees with final layer in sign
## [2026-05-15] Mistral-7B-Instruct-v0.3-4bit | AUROC attn-entropy @ final block | 0.7357 (sign +) | n=200, HIGH per-head attn entropy predicts contradiction; combined with low JS-radius means "heads agree on uniform attention"
## [2026-05-15] Qwen2.5-7B-Instruct-4bit | AUROC JS-radius @ final block | 0.6014 (sign −) | n=200, SAME sign as Mistral but AUROC magnitude collapses by Δ=−0.14
## [2026-05-15] Qwen2.5-7B-Instruct-4bit | AUROC JS-radius @ mid block | 0.5496 (sign −) | n=200, near-chance at mid; doesn't flip sign like Mistral mid
## [2026-05-15] Qwen2.5-7B-Instruct-4bit | AUROC JS-radius @ last-1 block | 0.6206 (sign −) | n=200, strongest layer on Qwen
## [2026-05-15] Qwen2.5-7B-Instruct-4bit | AUROC attn-entropy @ final block | 0.6457 (sign −) | n=200, FLIPPED vs Mistral (+) — LOW entropy → contradiction; "heads agree on concentrated attention"
## [2026-05-15] CROSS-MODEL JS-radius @ final sign-stability | both Mistral and Qwen 2.5 land sign − | First cross-architectural sign-stability for any non-trivial geometric channel — but AUROC magnitude collapse (0.74 → 0.60) means gate 3 (full architectural invariant) is NOT MET. Closer to gate 2 (partial collapse) than gate 3 (pass). Llama 3B not yet run.
## [2026-05-15] CROSS-MODEL attn-entropy @ final sign-flip | Mistral + / Qwen 2.5 − | attn-entropy fails cross-model sign test entirely; channel is model-specific. JS-radius is the only surviving cross-model channel from this diagnostic.

## [2026-05-17] Step-0 belief-readout panel — t=0 first-token-logit P(YES)/P(NO), ANLI R1 n=200, frozen pre-reg [OPEN, premise re-grounded]
## [2026-05-17] ANCHOR Mistral-Nemo | sign(lean)@t=0 vs free-gen committed answer | agreement 0.99 (198/200) passed=True | validity gate on the measurement premise, bar ≥0.95
## [2026-05-17] Qwen2.5-7B-Instruct-4bit | AUROC_B signed @ t=0 | 0.926 [0.887,0.959] | Recoverable-for-M, cov 0.98 — strongest; re-grounds Qwen despite 58% free-gen abstain
## [2026-05-17] Mistral-Nemo-Instruct-2407-4bit | AUROC_B signed @ t=0 | 0.906 [0.863,0.945] | Recoverable-for-M, cov 1.0 — also the anchor model
## [2026-05-17] Qwen3-8B-4bit | AUROC_B signed @ t=0 | 0.889 [0.835,0.932] | Recoverable-for-M, cov 0.995
## [2026-05-17] Llama-3.1-8B-Instruct-4bit | AUROC_B signed @ t=0 | 0.868 [0.815,0.912] | Recoverable-for-M, cov 0.995
## [2026-05-17] Phi-4-mini-instruct-4bit | AUROC_B signed @ t=0 | 0.840 [0.784,0.894] | Recoverable-for-M, cov 1.0
## [2026-05-17] Mistral-7B-Instruct-v0.3-4bit | AUROC_B signed @ t=0 | 0.829 [0.769,0.884] | Recoverable-for-M, cov 0.995
## [2026-05-17] gemma-3-4b-it-4bit | AUROC_B signed @ t=0 | 0.799 [0.741,0.859] | Recoverable-for-M, cov 1.0
## [2026-05-17] Llama-3.2-3B-Instruct-4bit | AUROC_B signed @ t=0 | 0.780 [0.713,0.839] | Recoverable-for-M, cov 1.0
## [2026-05-17] Qwen3-1.7B-4bit | AUROC_B signed @ t=0 | 0.727 [0.655,0.791] | Recoverable-for-M, cov 1.0 — weakest Recoverable
## [2026-05-17] Phi-3.5-mini-instruct-4bit | AUROC_B signed @ t=0 | 0.942 [0.853,0.997] (n=37 only) | Low-decidedness-for-M, eligible_cov 0.185 — affirmative null: no robust literal YES/NO boundary at t=0; tension vs Step-1 'clean trustworthy'
---
## 2026-05-26 — v4 sealed run complete

E_A1 ANLI: **7/9 PASS** (≥7/9 threshold). E_A2 cell-transfer: **3/9 → PARTIAL TRANSFER** (pre-reg ≥3/9 reframe clause triggered). TriviaQA descriptive: 8/9. Instrument confirmed: all 18 winning cells at step 0. Mistral-7B, Mistral-Nemo, Qwen2.5-7B show exact cell transfer; 6/9 models require per-task recalibration. Llama-3.2-3B and Gemma-3-4B fail E_A1 on ANLI. Details: [[results/v4-sealed-2026-05-26]].

## 2026-06-25 — Qwen2.5-32B stress panel: 8/8 deployable

Exploratory Modal/torch nf4 stress wave for `Qwen/Qwen2.5-32B-Instruct`: existing `anli_r1` 0.763 and `triviaqa_paired` 0.781 plus new `anli_r2` 0.744, `anli_r3` 0.698, `truthfulqa_mc` 0.730, `halueval_qa` 0.809, `halueval_dialogue` 0.539, and `halueval_summarization` 0.553. All six new tasks: n=200, 0 drops, 100% YES/NO, controls pass. ANLI + TruthfulQA preserve the attention-locus read; HaluEval broadens it to Fusion/readout on harder grounded-source tasks. NON-byte-comparable; sealed 18/20 untouched. Details: [[results/qwen32b-stress-2026-06-25]].

---
## 2026-07-25 — BACKFILL: Commit-Confluence line (2026-06-11 → 2026-07-22)

_These rows were never appended when the runs landed: `history.md` sat in no propagation checklist (fixed 2026-07-25, Vault-canon rule 5). Recorded here in run order for the numeric record; verdict detail lives in the linked result pages._

## [2026-06-11] CC sealed dispatcher (10 models × {anli_r1, triviaqa_paired}, seed 20260612, n=200, nboot 2000) | geometric-only endpoint | **18/20 PASS** (bar ≥17) | strict full-panel PRIMARY **18/20 FAIL** (bar ≥19) → product claim falsified. Same 2 ANLI cells fail both: gemma-3-4b/anli (predicted), Llama-3.1-8B/anli (new). Confidence is not the backstop. 12 distinct winners / 18 deployable → no universal cell. [[results/confluence-seal-2026-06-11]]
## [2026-06-18] gemma-3-12b-it | anli_r1 geom OOB CI-lo | **0.709 PASS** | vs sealed gemma-3-4b 0.403 FAIL ⇒ ANLI orphan = scale/small-model artifact. Byte-comparable extension, module hashes identical to seal. [[results/gemma-scale-extension-2026-06-18]]
## [2026-06-18] gemma-3-12b-it | triviaqa_paired geom | 0.929 | 4/4 new extension cells deployable; all winners ACE attention
## [2026-06-18] Qwen2.5-14B-Instruct | anli_r1 / triviaqa_paired geom | 0.766 / 0.597 | family control — rules out a generic 12–14B ANLI failure; trivia marginal
## [2026-06-20] gemma-3-12b-it (CRAB-LOCK head-starve ablation) | anli_r1 geom | 0.709 → **0.674** | head COUNT resolution REFUTED — explains only ~11% of the 0.31 orphan gap; orphan is per-head representation quality. Honest negative
## [2026-06-21] gemma-4-12B-it-qat | anli_r1 / triviaqa_paired geom | **0.691 / 0.751** — 2/2 deployable | generation axis does NOT reintroduce the orphan (gen-4 0.691 ≈ gen-3-12b 0.709 vs gen-3-4b 0.403). NON-byte-comparable (mlx-vlm reimpl); both winners Fusion, not ACE-solo
## [2026-06-22] Qwen2.5-32B-Instruct (torch/Modal, true nf4) | anli_r1 / triviaqa_paired geom | 0.763 / 0.781 | ACE attention penultimate-layer, winning solo. NON-byte-comparable — never pooled with sealed cells. [[results/llama-70b-scale-2026-06-22]]
## [2026-06-22] Qwen2.5-72B-Instruct (torch/Modal, confirmed nf4) | anli_r1 / triviaqa_paired geom | 0.639 / 0.918 | ACE attention, inter-head JS sub-cells
## [2026-06-22] Llama-3.3-70B (torch/Modal, nf4) | anli_r1 / triviaqa_paired geom | **0.703 / 0.788** | both win on RPV READOUT-volume @ gen_step=1, NOT ACE attention ⇒ first FAMILY DISSOCIATION in signal locus. Also closes the 2nd sealed ANLI orphan (Llama-3.1-8B) as a scale artifact
## [2026-06-22] Precision ladder {nf4,int8,bf16,fp32} @ Qwen2.5-7B + {nf4,int8,bf16} @ 32B | H3 falsifier (≥0.10 geom CI-lo drop nf4→bf16) | **NOT TRIGGERED — H3 FALSIFIED at fixed-cell level** | signal is real computation, not quantization noise. Method lesson: judge cross-precision on FIXED CELLS, not the argmax winner. Selection instability + int8 degradation are small-model artifacts, wash out by 32B. [[results/precision-ladder-results-2026-06-22]]
## [2026-06-25] Qwen2.5-32B-Instruct nf4 stress panel (8 tasks, n=200) | geom CI-lo | **8/8 deployable** | anli_r1 0.763 / r2 0.744 / r3 0.698 / triviaqa 0.781 / truthfulqa_mc 0.730 / halueval_qa 0.809 / halueval_dialogue 0.539 / halueval_summarization 0.553 — locus BROADENS: HaluEval QA→Fusion, dialogue/summ→readout. [[results/qwen32b-stress-2026-06-25]] _(block already present above; row added for scan parity)_
## [2026-07-22] BENCH strict Phase-4 A1 (halueval_qa, 10 models, n=1000 rows / 500 stems, seed 20260711, nboot 2000) | per-model cluster-geometric deployability | **10/10 PASS** (bar ≥8) | weakest cluster CI-lo 0.6705 (Qwen3-1.7B), strongest 0.9005 (gemma-3-4b); 8 distinct winners; controls pass, zero drops. [[results/bench-a2-signflip-2026-07-22]]
## [2026-07-22] BENCH strict Phase-4 A2 (fixed cell `fusion_rank_mean_geom` + ONE pooled sign, blind LOMO) | holdout AUROC ≥0.55 | **6/10 FAIL** (bar ≥8) | A1∧A2 conjunction NOT satisfied ⇒ floor extends only PARTIALLY, A2 named as failing. Misses are intrinsic SIGN INVERSIONS, confidently below chance: Mistral-7B 0.174, Mistral-Nemo 0.206, Qwen2.5-7B 0.276, Phi-3.5 0.394 (reversals 0.826/0.794/0.724/0.606 — NOT a rescue, requires holdout labels)
## [2026-07-22] BENCH strict Phase-4 B1 (anli_r1_rep + triviaqa_paired_rep replication) | registered endpoint | **7/20 FAIL** (bar ≥17, both units) | REGISTERED VERDICT. Mechanism = §4/§8.1 commitment gate cascade, not geometric collapse: 20 planned → 18 profiled (geometry deployable 18/18, CI-lo 0.6577–0.9804) → 14 admissible → 7 registered. Triggers rare (1/1000, 1/1000, 12/1000). Descriptive anatomy is NOT a rescue endpoint; do not propagate as a signal negative
## [2026-07-22] BENCH strict Phase-4 B2 orphan probe (anli_r1_rep, n=1000) | geom CI-lo | gemma-3-4b **0.772**, Llama-3.1-8B **0.676** — both deployable | narrows toward a small-n artifact component; does NOT erase the sealed failures. CAVEAT (§3.2): a re-test of the sealed construct at 5×n on the TRAIN distribution — not fresh-data replication
## [2026-07-22] Sealed TriviaQA stem-cluster sensitivity (descriptive, non-gating) | geom CI-lo under question-stem unit | **10/10 hold** | weakest 0.5830 (Qwen3-1.7B) — clustered-inference concern descriptively discharged; a registered clustered endpoint on fresh data is still owed
## [2026-07-25] Sign-flip↔E_A2 trio coincidence screen (designed-retrospective, frozen design @ 1f70c9f, cell `fusion_rank_mean_geom`, aux tasks anli_r2/halueval_dialogue/halueval_summarization, halueval_qa excluded, 9-model cohort) | Fisher exact two-sided on trio×positive-majority | **NULL — p = 0.50**, table [[3,0],[4,2]], OR nonfinite (zero cell) | positive-majority is cohort norm 7/9; Phi-4 (non-trio) sign-identical to both Mistrals; no abort (all 9 models ≥2 usable tasks). NOT a finding either way beyond: cheap support absent. [[results/signflip-coincidence-2026-07-25]]

## [2026-06-09, scored 2026-07-25] Attention KV-tension pilot (ACE follow-up; ANLI R1, t=0, n=200, nboot 1000, seed 20260512; 5 models) | best KV-tension cell vs best existing ACE comparator, absolute orientation | **NO-PROMOTE — promotion bar not met on any of its 3 limbs** | Best-KV AUROC: Qwen3-8B 0.8479 (`js_within_kv_groups`, +0.0075), Mistral-7B 0.8065 (`js_kv_tension_ratio`, +0.0195), Qwen2.5-7B 0.7535 (+0.0486 vs routing but **−0.0261** vs all-ACE; selected winner is `final_bos_mass`), Phi-4-mini 0.7374 (+0.0614), gemma-3-4b 0.6379 (−0.0521, OOB CI-lo 0.4960 not clean). ≥+0.03 on 2/5 vs routing-only, **0/5** vs any existing ACE cell; `winner_unstable` fires 4/5 including both wins; **shuffled-label control never run**. Verdict hinges on a comparator set the pre-registration left unenumerated. [[results/kv-tension-pilot-2026-06-09]]


## [2026-07-26] Empathy-geometry cell panels standalone in EG repo (replay capture, B2/giraffe, Qwen2.5-7B-4bit, 6 rows) | cross-interpreter parity: EG venv py3.11.15/numpy 2.2.6 vs sealed venv py3.9.6/numpy 2.0.2 | **PASS — 174/174 values, worst relative delta 0.000e+00 (bit-identical)** | 21-cell t=0 ACE panel + 3 scalars/row + 5 strict gen-step-1 metrics; row identity (prompt_sha256 + first_token_id) verified identical first. Within-EG-venv `check-gen1-parity` (harness vs independent canonical `comprehensive_run`) also PASS at rtol 1e-5. Suite 99 passed (was 69). `t0-morphology-furnace` clean + A0 PASS after. INFRASTRUCTURE ONLY — no detector, arm-separation, or empathy claim. [[results/eg-standalone-panels-2026-07-26]]## [2026-07-26] E3-HaluEval descriptive label-cost sweep (post-hoc on published halueval_qa matrices; spec pre-committed @ fde0349; budgets {50,100,150,300,500}, stem-aware, repeats 10, nboot 1000, seed 20260613) | frac repeats deployable per (model, budget) | **10/10 models at 1.0 by 150 labels, flat through 500 — a measured knee**; 9/10 at 1.0 by 100 | weakest A1 cell (Qwen3-1.7B) last to certify (0.2/0.9/1.0 at 50/100/150); HaluEval-QA descriptively cheaper than sealed tasks. NOT a registered endpoint. [[results/e3-halueval-descriptive-2026-07-26]]


## [2026-07-26, corrected same day] Empathy-geometry standalone panels — re-verified under EXACT mode after adversarial review | fresh replay capture vs sealed reference, rtol=0 atol=0 | **`bit_identical: true` — 174/174 values, max absolute delta 0.0, max relative delta 0.0** | SUPERSEDES the earlier same-day row's evidentiary basis (not its numbers, which were re-derived unchanged). Codex `gpt-5.6-sol` found the comparator ran at rtol 1e-5 and reported "worst delta" over FAILURES ONLY — trivially 0.0 whenever nothing failed — so bit-identity had been asserted, not tested. Comparator now tracks max abs/rel delta over ALL comparisons, supports exact mode, reports `exact_mode` and `bit_identical` separately; demonstrably rejects a 1-ULP (1.694e-21) perturbation. Suite 113 passed + 4 subtests. [[results/eg-standalone-panels-2026-07-26]]