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
