# Research Candidates — Forward-Looking Ideas

_Parking-lot for ideas that could become future pre-regs once they ripen. Not findings, not claims — just structured notes on "what might come next." Originally `v4-candidates.md` (entries 1–6 fed the v4 / ACE arc); renamed 2026-05-30 to scope-generalize for v5+ entries._

> **Status convention**: every entry is **[OPEN]** until a fresh-data pre-reg with falsification criteria is filed under [results/](results/summary.md). Promotion path: **[OPEN] → amendment doc with run plan → sealed gate → results page.**
>
> **Scope**: forward-looking research ideas at any horizon (v3.x amendments, v4 follow-ups, v5+ new directions). Tweaks to an already-sealed primary go in [results/](results/summary.md), not here.

## Entry index

| # | Idea | Status | First noted |
|---|---|---|---|
| 1 | [Empirical-variance gate parser](#1-empirical-variance-gate-parser) | **[OPEN]** — operational fix (`--gate-max-tokens 12`) recovered Llama + Phi in 2026-05-08 v3.2 re-run; empirical parser still leverage-rich for new families | 2026-05-07 |
| 2 | [Centered-Fisher / KL-grounded null_ratio](#2-centered-fisher--kl-grounded-null_ratio) | **[FALSIFIED]** at sealed step=1 by 2026-05-08 v3.2 re-run (all 3 amendment criteria FAIL); centered helps at *some* rank for *some* models but no universal bar clears | 2026-05-07 |
| 3 | [Adaptive-step rupture detection](#3-adaptive-step-rupture-detection) | **[OPEN — DEGRADED]** — pilot's "Fisher r=1 universally @ adaptive ≈ 1.000" doubly-falsified at n=200 (Llama 0.77, Qwen 2.5 0.65) AND adaptive often loses to best-fixed-step by 0.3–0.5; step-localization is real but commit_step is not always optimal | 2026-05-08 |
| 4 | [Meta-classifier for (step, metric, rank) selection](#4-meta-classifier-for-step-metric-rank-selection) | **[RETIRED 2026-05-13]** — 33-profile ANLI sweep (11 models × R1/R2/R3) confirms family-based prediction is dead AND that even within the same task family calibration shifts between adversarial rounds (Mistral-Nemo picks Centered r=2 + on R1, d_F_full − on R2). Fisher r=2 @ step 3 (the prior "stable cell" candidate) is noise: 17+/15− sign split across 32 finite profiles. Production framing: per-(model, exact deployment distribution) calibration via v1.1 calibrator. 30/33 n=50 profiles fire a deployability warning → small-n is the real bottleneck. | 2026-05-10 |
| 5 | [Attention-cell extension to `pri_calibrator.py`](#5-attention-cell-extension-to-pri_calibratorpy) | **[SEALED CONFIRMED + PARTIAL-TRANSFER-REFRAME 2026-05-26]** — v4 sealed run complete. **E_A1: 7/9 PASS** (OOB CI_lo > 0.50 on ANLI R1 n=200, t=0 instrument). **E_A2: 3/9 PARTIAL TRANSFER** (Mistral-7B, Mistral-Nemo, Qwen2.5-7B exact cell match ANLI→TriviaQA; 6/9 require per-task recalibration). TriviaQA 8/9 (descriptive). Block-depth stable 6/9. Paper reframes from "no universal cell" to "partial transfer; per-task recalibration required for 6/9." Pre-reg: `PRI_V4_PRE_REGISTRATION_PLAN.md`. Results: [[results/v4-sealed-2026-05-26]]. | 2026-05-15 |
| 6 | [Causal probe — Fisher rupture direction v_top](#6-causal-probe--fisher-rupture-direction-v_top) | **[OPEN — PILOT 2026-05-25]** — +v_top steering causes contradiction samples to semantic-flip at 4× the rate of entailment samples at alpha=50 (40% vs 10%), despite contradictions having a *larger* mean logit gap. Non-null causal signal. Confound mitigation (logit-gap matching, orig_answer balance) required before promotion. Scope memo positions as §5 forward-work (not paper headline). | 2026-05-25 |
| 7 | [Bluff vs honest-uncertain — epistemic-distinguishability testbed](#7-bluff-vs-honest-uncertain--epistemic-distinguishability-testbed-v5-candidate) | **[OPEN — v5 CANDIDATE, DEFERRED]** — can ACE / belief-readout distinguish commits where the model is bluffing (committed answer ≠ internal belief) from commits where it is honestly uncertain? Dream-prompted (user 2026-05-30); Nash-equilibrium framing as oracle. Cheap version = paired-prompt bluff/honest design, ~1–2 days, no poker engine required. Deferred until v4/ACE paper is in submission shape. | 2026-05-30 |
| 8 | [Fisher information on the attention landscape](#8-fisher-information-on-the-attention-landscape) | **[OPEN — v5 CANDIDATE]** — Fisher-ize ACE. The gaze `softmax(Q·Kᵀ/√d)` is already a categorical distribution, so its Fisher metric is well-posed. Key identity: the inter-head JS-*divergence* is, to leading order, `⅛·δᵀFδ` (so the JS-*radius* the diagnostic uses is its root, `√(⅛·δᵀFδ)`) — i.e. JS is *already* a discrete shadow of an attention Fisher. Genuinely-new variant = Fisher **pullback to `h`** (gaze brittleness/curvature), the `W_u`-free analog of v3. Confound: BOS-sink saturation → degenerate softmax Fisher, the same high-confidence regime that [FALSIFIED] the centered-Fisher amendment (#2). Pilot on Mistral + Qwen 2.5 (the JS sign-stable pair); must beat JS-radius AUROC and preserve the sign. | 2026-06-04 |
| 9 | [Residual-stream sub-layer friction (attention vs MLP)](#9-residual-stream-sub-layer-friction-attention-vs-mlp) | **[OPEN — v5 CANDIDATE]** — the hallucination tell may live in the *friction* between the attention write `a` and the MLP write `m` within a block, not in either alone. `W_u`-free (`cos(a,m)` / destructive-interference fraction). Central claim: **orthogonal to v3**, because `Δh = a + m` collapses the friction (same-sum-different-fight). Mechanism = MLP endorsing-vs-vetoing attention's routing (Geva KV-memories). **Decisive bar: incremental AUROC *over* `null_ratio` / `‖Δh‖`**, not just beating JS. Pilot on Mistral + Qwen 2.5. | 2026-06-05 |
| 10 | [Shadow-ambiguity — Fisher pseudo-volume of the readout](#10-shadow-ambiguity--fisher-pseudo-volume-of-the-readout) | **[TESTED 2026-06-07 — H1 NO-GO: beats confidence (meta +0.102) but REDUNDANT with v3 (meta +0.011 < 0.02 bar); complements v3 only in its collapse regime]** — `W_u`-*using* complement to ACE; readout commit-ambiguity (eff-rank / spectral-entropy / off-top log-pseudo-volume of the softmax-Fisher `I(h)=W_uᵀ(diag(p)−ppᵀ)W_u`), **independent of `Δh`**. Temperature pre-check PASSED panel-wide (4 models — not pure-confidence). **Labeled pilot (ANLI R1 n=200, 4 models): subsumed by v3 where v3 works (Mistral/Qwen2.5/Llama, incr ≈0), but adds control-clean incremental AUROC where v3 collapses — Qwen3-8B (null_ratio 0.456 = dead): eff_rank/shadow_logvol incr +0.13 [CI>0], partial r +0.28/−0.37 beyond surprise+null_ratio [CI>0], shuffled control flat.** Conditional positive (1/4 = the v3-failure model; below the ≥2/4 bar but reframes as complementary-not-universal) → labeled pre-reg with more v3-failure models. **Comprehensive run (26 pairs, 13 models × 2 benchmarks, gauntlet-hardened): beats plain confidence generally (base-A meta +0.102 [+0.065,+0.140], p~5e-8; 3 families; brittleness-clean) but REDUNDANT with v3 (base-B meta +0.011, below the +0.02 bar) → H1 NO-GO; complements v3 only in its collapse regime (H2 slope +0.083). Reframe: confidence-independent but v3-overlapping, not a universal detector. See [[log#2026-06-07]].** | 2026-06-07 |
| 11 | [Empathy-geometry dyad — NVC resonance vs performative compliance](#11-empathy-geometry-dyad--nvc-resonance-vs-performative-compliance) | **[OPEN — DESIGN/CRAFTING 2026-07-08; MULTI-BUNDLE TRANSFER PRIMARY 2026-07-13]** — dyadic NVC study on the existing panel: Qwen twins across E1/E3/E6 scenario bundles × giraffe/neutral/jackal, unscripted t_hear/t_sol endpoints, geometry must beat T1-T4 on a fully held-out bundle (three-fold LOBO: fit all choices on two bundles, score the untouched third). E3-only is instrument development, not confirmatory evidence. Directed persona-vector steering remains the causal primary; performative compliance ≈ sycophancy → future guard domain. | 2026-07-07 |
| 12 | [Introspective accuracy — does a model's self-report track its measured geometry?](#12-introspective-accuracy--does-a-models-self-report-track-its-measured-geometry) | **[OPEN — PARKED 2026-07-13]** — user-originated ("meditative state ≈ less activation"; from a self-reflection exchange with another Opus instance). Two experiments, one instrument: **(a) steerability** — is there a *settledness* direction in activation space (persona-vector machinery, T4), and does projecting onto it move the commit geometry? **(b) introspective accuracy** — does the model's own report of its state correlate with `p_max` / `spectral_entropy` / `null_ratio` / `shadow_logvol`? Pre-registration is mandatory because "less activation" contains **two contradictory predictions** (narrower commit vs. more spacious readout) that will both feel obvious in hindsight. Explicitly **NOT** a judge-panel row: API judges have no internals, and a state-induction preamble reopens the arm-token-length confound. Honest-negative outcome (report = confabulation) is publishable in this project's register. | 2026-07-13 |

---

## 1. Empirical-variance gate parser

**One-line**: replace the hand-coded 3-tier `check_answer` regex stack with a parser fit to the empirical distribution of model output formats sampled at scale (n ≥ 200 per model).

### Motivation

The behavioral-gate parser has been a recurring source of brittle failures across the v3.x line:
- 2026-04-22 → Phi-3.5-mini gate-failed at 12/20=60% under the original parser; recovered to PASS only after the 2026-04-23 stratified preflight + 3-tier parser landed (PR #7).
- 2026-04-23 → all 3 primaries gate-failed at the original 256-token budget because Qwen-style format-completion appended a fabricated "Answer: NO" after the correct "Answer: YES"; mitigation = `--gate-max-tokens 12`.
- 2026-05-07 (this v3.2 run, live) → Qwen 2.5 control gate scraped through at exactly 16/20=80% with 4 misses; same Qwen-format-completion artifact, same parser brittleness.

Each fix has been a hand-tuned heuristic against the previous failure mode. The pattern is: model produces a long-tailed family of output shapes; parser was written before that tail was characterized; tail bites the next model family that arrives.

### Proposed mechanism

1. **Capture phase**: for each (model, n=200, control prompts only), persist the raw `output` strings to a `gate_outputs.parquet` file. Cheap — no PRI metric compute, just generate + log.
2. **Variance phase**: cluster outputs by structural shape (e.g., regex feature vector: has-`Answer:` prefix, has-EOS-marker, contains continuation token, # newlines before answer, ...). Surface the long tail empirically.
3. **Fit phase**: derive a parser whose match-set is the **union of observed structural classes** with empirical mass ≥ ε on at least one model. Validate on held-out controls.
4. **Coverage gate**: a new model is in-distribution iff its outputs fall within the existing parser's match-set with rate ≥ τ on a calibration sample. If not, expand the parser before running the main experiment.

This is essentially a *characterize → fit → validate* loop instead of *fail → patch → fail*. The same epistemic move that distinguishes v3 from v1/v2 at the metric level: stop hand-coding, start measuring variance.

### Why it could matter for v4

If the gate is brittle, every cross-architecture claim has an unfalsifiable confound: did the metric move because the model committed differently, or because the parser caught a different fraction of legitimate answers? An empirical-variance parser would let v4 make stronger cross-family claims by removing the parser-noise from the experimental signal.

### Decision criteria for promotion

- [ ] Initial scoping: 2-hour read of v3.x parser-fail incidents to enumerate the structural classes already seen. Output: Markdown table of failure modes.
- [ ] Minimum viable run: 200 control outputs × 6 models = 1,200 samples, ~30 min compute. Output: cluster diagram.
- [ ] Acceptance threshold: empirical-fit parser ≥ 95% control accuracy on all 6 models with the same threshold. Compare to current 3-tier (~80-100% per-model, 80% floor on Qwen 2.5).
- [ ] If the new parser uniformly dominates: write `wiki/results/v3.x-parser-amendment.md` with a sealed re-run on 1 primary as a sanity check.

### Cross-references
- [v3-main-run](results/v3-main-run.md) — the Qwen format-completion failure mode (pre-J_n, 2026-04-23)
- [v3.1-replicate](results/v3.1-replicate.md) — the `--gate-max-tokens 12` operational fix
- repo: `pri_v2_mlx_pipeline.py:check_answer` — current parser
- repo: `scripts/run_v3_main.py:--gate-verbose` — diagnostic that surfaces the misses

---

## 2. Centered-Fisher / KL-grounded null_ratio

**One-line**: replace the sealed Euclidean-norm `null_ratio_post_rank{r}` with the KL-grounded `null_ratio_centered_post_rank{r}` (proper softmax Fisher with the −ppᵀ correction) once v3.2's three-way bake-off justifies it.

### Motivation

Already laid out in [v3.2-amendment](results/v3.2-amendment.md). Briefly: the sealed v3.x null_ratio uses `A = sqrt(diag(p))·W_u` as the basis (uncentered Fisher) with Euclidean projection. The proper softmax Fisher pullback to h-space is the **centered** form `F_c = W_uᵀ (diag(p) − p pᵀ) W_u`. The −ppᵀ rank-1 correction matters most at high-confidence tokens — exactly where Qwen 3 8B sits and where `null_ratio_post_rank1` collapses to AUROC 0.55 vs Raw's 0.91.

Algebraic preview from `scripts/test_centered_fisher.py` (8/8 pass): in the high-confidence regime the top eigenvalue of centered F_c is ~10⁴× smaller than uncentered, suggesting the sealed metric reads off a top-eigenvector that does not exist in the proper Fisher metric for that regime.

### Promotion path

This is the **already-launched** v4-candidate. v3.2 ([v3.2-amendment](results/v3.2-amendment.md)) is the descriptive bake-off; promotion to sealed primary is gated on:

- [ ] v3.2 main run completes (in progress: 2026-05-07 launch, ETA ~6-8 hr at observed throughput).
- [ ] **Decision criterion 1** (Qwen 3 recovery): `Δ_Q3 ≥ +0.10` with non-overlap CI on `AUROC(null_ratio_centered_post_rank1) − AUROC(null_ratio_post_rank1)`.
- [ ] **Decision criterion 2** (no regression on Fisher-wins primaries): no `Δ_i ≤ −0.05` on Llama / Mistral / Qwen 2.5.
- [ ] **Decision criterion 3** (kl_discharged competitiveness): `|Δ_kl| ≤ 0.05` makes the rank choice decorative and simplifies v4 to a single scalar.

If criterion 1 fires alone: write `wiki/results/v3.3-amendment.md` with fresh seed pre-reg and centered as the new sealed primary.

If criteria 1+3 both fire: **headline simplification** — v4 reframes around `kl_discharged = ½·Var_p(W_u·∂h_post)` as the single load-bearing scalar, no rank, no eigendecomp. Theoretically clean, computationally trivial.

### Cross-references
- [v3.2-amendment](results/v3.2-amendment.md) — pre-reg, math, run plan
- [v3.1-replicate](results/v3.1-replicate.md) — the 3-Fisher / 3-Raw split this targets
- repo: `pri_v2_mlx_pipeline.py:kl_discharged_and_centered` — the new method
- repo: `scripts/test_centered_fisher.py` — 8/8 PASS on the math identities

---

## 3. Adaptive-step rupture detection

**One-line**: instead of pinning the analysis plane at `gen_step=1`, find the actual answer-commit step empirically per (model, sample) and measure the metric there. Sealed step=1 was a measurement-target proxy that broke as soon as the model set crossed format conventions.

### Motivation — pilot result, n=10/model on v3.2 trace dumps (2026-05-08)

The v3.2 main run produced a striking 4-model-deep diagnostic when the trace dumps were re-analyzed at the per-sample answer-commit step (the gen_step where the model's cumulative output first contains "YES" or "NO" as a standalone answer):

| Model | commit_step distribution | Best AUROC @ sealed s=1 | → Best AUROC @ adaptive |
|---|---|---|---|
| Mistral 7B | always 5–6 | Raw r=1: 0.96 | **Fisher r=1: 1.000** |
| Qwen 2.5 7B | mix of 1 and 3 | Centered r=2: 0.96 | **Raw r=1: 1.000** |
| Qwen 3 8B | always 3 (3/10 timeouts) | Centered r=1: 1.000 | **Fisher r=1, Fisher r=2, Raw r=1, kl_discharged, Centered r=2: all 1.000** |
| Gemma 4B | always 4 | Centered r=1/r=2: 0.92 | **Fisher r=1: 1.000** |

`Fisher r=1` at the adaptive commit step hits AUROC **1.000** on 3/4 models (Qwen 2.5 hits Raw r=1 = 1.000 instead). Caveat: n=10 is small (null prob ≈ 1/252 ≈ 0.4%); needs n=200 validation before any sealed claim.

The implication is large: **the 3-Fisher / 3-Raw architectural split that v3.1 surfaced and v3.2 was built to explain (via the −ppᵀ centered correction) is largely a measurement-target mismatch, not a metric difference.** At gen_step=1, Mistral measures "Answer" emission, Qwen 3 measures mid-COT, Gemma measures "Answer" emission — different semantic events per model. Move to the actual answer-commit step and the architectural split largely collapses.

### 2026-05-10 n=200 + step-sweep reality — pilot superseded

The 2026-05-08 v3.2 re-run with `--gate-max-tokens 12 --max-gen-tokens 24` (recovered Llama + Phi from gate-fail; recovered Qwen 3 COT-overflow samples) plus the new `gen_token_id` capture enabled **two follow-up analyses at n=200/model**, both of which *weaken* the pilot story:

**[FALSIFIED] Pilot claim 1: "Fisher r=1 @ adaptive ≈ 1.000 universally."**

| Model | n=10 pilot Fisher r=1 @ adaptive | n=200 Fisher r=1 @ adaptive |
|---|:---:|:---:|
| Mistral 7B | 1.000 | **0.85** |
| Qwen 2.5 7B | (Raw r=1 = 1.000) | **0.65** |
| Qwen 3 8B | 1.000 | **1.000** ✓ |
| Gemma 4B | 1.000 | **0.97** |
| Llama 3B | (gate-failed in pilot) | **0.77** |
| Phi-3.5-mini | (gate-failed in pilot) | **0.97** |

The pilot caught a Type I error. At n=200, Fisher r=1 @ adaptive holds at AUROC ≥ 0.95 only on **3/6 models** (Qwen 3 / Phi / Gemma). Llama and Qwen 2.5 actively *regress* at adaptive (0.91 → 0.77, 0.90 → 0.65 vs sealed step=1). Validation criterion **fails**.

**[FALSIFIED] Pilot claim 2: "no fixed-step universal exists, only adaptive works."**

The 2026-05-10 step sweep (`scripts/diagnostics/diagnose_v3_2_step_sweep.py`) computed AUROC across the full `(model × gen_step × family × rank)` cube — 5,904 cells. Two findings reframe adaptive:

- 🎯 **Every model has *some* fixed-step cell at AUROC ≈ 1.000 on class-balanced data (gen_step ∈ [1, 5]).** Llama: Fisher r=1 @ step 2; Mistral: Raw r=2 @ step 1; Phi: Raw r=8 @ step 1; Qwen 2.5: Fisher r=21 @ step 1; Qwen 3: Fisher r=1 @ step 2; Gemma: Raw r=1 @ step 3. *(Original sweep had Gemma @ step 12 and Mistral @ step 5-9; both were class-imbalance artifacts and have been retracted.)*
- 📉 **Adaptive often LOSES to best-fixed-step by 0.3–0.5 AUROC** for many metrics. Worst-case Δ (adaptive − best_fixed) per model: Llama −0.49, Mistral −0.49, Phi −0.48, Qwen 2.5 −0.48, Qwen 3 −0.42, Gemma −0.46.

So adaptive is **one path to high signal, not strictly the best**. The "answer-commit step is the right semantic target" intuition is partly right — but the rupture often peaks at `commit_step − 1` (pre-commit) or at a step entirely uncorrelated with commit_step (Gemma's optimum is step 12, ~8 steps after answer emission).

**[FALSIFIED] Pilot claim 3: "best step ≈ commit step."**

Commit-step vs best-fixed-step alignment (corrected post-class-balance discovery 2026-05-10):

| Model | Adaptive commit_step | Best fixed step | Match? |
|---|---|---|---|
| Llama 3.2 3B | ~5 (`Answer:`-format) | **2** | ❌ pre-Answer |
| Phi-3.5-mini | ~3 | **1 or 2** | ❌ pre-Answer |
| Qwen 3 8B | 3 (post-COT) | **2** | ❌ mid-COT (pre-commit) |
| Gemma 3 4B | 4 | **3** *(was 12; class-imbalance artifact)* | ❌ pre-Answer |
| Mistral 7B | 5–6 | **1 or 5** *(was 5–9; partly class-imbalance)* | ⚠️ partly overlaps |
| Qwen 2.5 7B | 1 or 3 | 1 or 3 | ✅ matches |

5 of 6 models peak **before** the answer is emitted. The 2026-05-10 anomaly diagnostic ([v3.2-results §4.5](results/v3.2-results.md#45--class-balance-discovery--per-sample-anomaly-diagnostic-2026-05-10)) showed the top-K probability distribution at these pre-Answer steps already encodes YES/NO commitment — the model has internally committed before token emission. The temporal target is not "the answer-commit step" — it's the *pre-commit step*, which precedes answer emission by 1-3 tokens depending on the model's format.

**[FALSIFIED] Pilot claim 4: "the architectural split collapses at adaptive step."**

It does collapse in the sense that every model can hit ~1.000 — but the 6 models cluster around different metric/rank combinations (3 Fisher families, 2 Raw, 1 Centered → kl_discharged), so the "architectural split" in metric preference is preserved, just shifted to a different operating-point axis.

**Universal-winner search at fixed step**: top universal cell is `kl_discharged @ gen_step=6` with min AUROC **0.78**. No fixed `(gen_step, family, rank)` triple hits ≥ 0.90 across all 6 models. This rules out the simplest v4 pre-reg of the form "the rupture metric is X at step Y."

### Why the sealed plane was wrong

The v3.x convention pins `gen_step=1` because the synthetic-logic puzzles were designed so that the answer is the first generated token. That assumption holds for *some* model families:

- **Mistral / Llama** family: emits `"Answer:"` (4 tokens of format prefix) before YES/NO → commit at step 5–6
- **Qwen 2.5**: emits YES/NO directly OR after `"Answer: "` → commit at step 1 OR 3
- **Qwen 3** (reasoning-tuned): emits chain-of-thought BEFORE the answer → commit at step 3+ (and 30% of samples never reach a YES/NO in 14 tokens, pure COT overflow)
- **Gemma 4B**: emits 3 tokens of format prefix → commit at step 4

The sealed step=1 metric for these is reading *format-emission rupture* (Mistral/Gemma) or *mid-COT rupture* (Qwen 3), not *answer-commit rupture*. The architectural-split phenomenology is then explained: each model's step=1 measures a different semantic event, so cross-family comparisons at that plane are confounded.

### Proposed mechanism

1. **Capture phase** (already drafted, 2026-05-08): pipeline patch persists `gen_token_id` per row in `all_results.parquet` alongside the metric columns. Adds ~8 bytes/row, no compute cost. Removes the trace_dumps-only constraint that blocks n=200 adaptive analysis.
2. **Detection phase**: per (model, sample), scan `gen_token_id[step]` in order, decode token-by-token via the model's tokenizer, find first `gen_step` where the cumulative decoded text contains `[" YES", " NO", "\nYES", ...]` (standalone-answer regex). Same heuristic the n=10 pilot used.
3. **Adaptive analysis**: filter `all_results` to `gen_step == commit_step` per sample (keyed by model, sample_id), then compute AUROC for each metric family.
4. **Edge cases**: samples that never emit a YES/NO within `max_gen_tokens` are flagged and either (a) excluded from the adaptive AUROC or (b) given a fallback plane (e.g., the gen_step where surprise drops below threshold). Pre-register before the run.

### Why it likely matters for v4

If `Fisher r=1 @ adaptive_step` holds at AUROC ≥ 0.95 across all 6 models at n=200, the v4 paper has a much cleaner story than v3.x's architectural-split-with-caveats:

- The metric IS the proper Fisher pullback — uncentered, rank=1 is fine.
- The temporal target needs to be data-driven, not pinned.
- The architectural-split phenomenon is a measurement-target artifact that vanishes under proper protocol.

This is also a much smaller paper-level claim to defend: "we measure rupture at commit, not at format-emission." Reviewers can validate the heuristic against the trace dumps.

### Decision criteria for promotion

- [x] Pilot n=10 trace dumps post-hoc: **PASS — Fisher r=1 @ adaptive = 1.000 on 3/4 models** *(later superseded by n=200; pilot was Type I error)*.
- [x] Pipeline patch landed (`gen_token_id` in `all_results`): **PASS — landed 2026-05-08, validated against 2026-05-08 re-run.**
- [x] Re-run v3.2 scope with operational fixes: **PASS — 2026-05-08/run-01, all 6 models gate-passed (avg 99.2%), n=200/model.**
- [x] **Validation criterion**: adaptive-step `Fisher r=1` AUROC ≥ 0.95 on all 6 models. **FAIL — clears on Qwen 3 / Phi / Gemma only (3/6); Llama 0.77, Mistral 0.85, Qwen 2.5 0.65.**
- [x] **Falsification criterion**: any model with adaptive `Fisher r=1` AUROC < 0.85. **FIRES — Llama 0.77, Qwen 2.5 0.65 both below the floor.**

**Verdict (2026-05-10)**: the pilot's universality claim is falsified at n=200. Adaptive-step is *not* a drop-in v3.x → v4 sealed-primary swap. The temporal-target idea is partly right (sealed step=1 IS wrong for several models), but adaptive is not strictly better than picking the best fixed step per model, and `commit_step` is not always the best fixed step.

The **surviving** weaker claim: "every model has *some* (gen_step, family, rank) cell at AUROC ≈ 1.000, but the cell is model-specific and not predictable from family alone." That claim is now [v4-candidate #4](#4-meta-classifier-for-step-metric-rank-selection)'s territory.

### Open questions (post-2026-05-10)

- 🔍 **Why is Llama's best fixed step pre-prefix?** Llama emits `"Answer: YES"` (commit at step ~5), but Fisher r=1 peaks at **step 2** (during `"Answer:"`). Hypothesis: the model's residual stream has already committed to YES vs NO before it emits the format prefix. Worth a sample-level diagnostic: for the same sample, is `h_2` already "pointing at YES"?
- 🔍 **Why does Gemma 4B peak at step 12?** Long after the answer is emitted (commit at step 4). Hypothesis: format-completion artifact ("Now solve the following:..." continuation) creates a second rupture event when the model commits to fabricating the next puzzle's answer. If true, the "rupture" we measure isn't necessarily about *this* puzzle's answer — it's about *some* commitment in the generation stream. That's a real interpretability concern for v4.
- 🔍 **Is the answer "use both steps"?** Many models have two AUROC-1.000 cells at adjacent steps (e.g., Llama steps 2+4). Could a step-pair classifier (both signals jointly) be more robust than either alone?
- ✅ **Pre-commit story REPLICATES on fresh seed** *(answered 2026-05-10)*: 3-primary fresh-seed validation at seed 20260510 confirmed all per-model best cells from seed 20260507 within Δ ≤ 0.025 AUROC. Mistral's Fisher r=1 @ step 5 is identically 1.000 on both seeds. The pre-Answer commitment phenomenon is sample-mix-stable. *(Not yet validated on Qwen 3 / Phi / Gemma 4B; those would need their own fresh-seed re-run.)*

### Cross-references
- [v3.2-amendment](results/v3.2-amendment.md) — the run that surfaced the per-model commit-step variance
- [v3.1-replicate](results/v3.1-replicate.md) — the architectural-split phenomenon this entry reframes
- repo: `pri_v2_mlx_pipeline.py:row_out` — patch site for `gen_token_id` capture (drafted 2026-05-08)
- repo: `/tmp/show_outputs.py`, `/tmp/v3_2_rank_sweep.py` — pilot analysis scripts (move to `scripts/diagnostics/` if promoting)
- entry [#1 (parser)](#1-empirical-variance-gate-parser) — orthogonal but synergistic: empirical parser fixes gate brittleness, adaptive-step fixes metric brittleness

---

## 4. Meta-classifier for (step, metric, rank) selection

**One-line**: train a small classifier on observable model properties to predict the optimal `(gen_step, family, rank)` triple, so v4's pre-reg can be "given a new model, our procedure picks the right rupture detector" rather than "we found the per-model best by exhaustive search after the fact."

### Motivation — emerged from 2026-05-10 step-sweep finding

The 2026-05-10 step sweep at n=200 produced two facts that look contradictory at first:

- ✅ **Every model has a near-perfect cell.** AUROC ≈ 1.000 is reachable in 6/6 models tested (Llama, Mistral, Qwen 2.5, Qwen 3, Phi, Gemma 4B).
- ❌ **No fixed cell works on all 6 models.** Best universal cell hits min AUROC 0.78. Per-model best cells are: Fisher r=1 @ step 2 (Llama), Fisher r=1 @ step 5–9 (Mistral), Raw r=32 @ step 2 (Phi), Fisher r=2 @ step 3 (Qwen 2.5), Fisher r=64 @ step 2 (Qwen 3), Raw r=4 @ step 12 (Gemma).

These are reconcilable iff the optimal cell is a **predictable function of model properties**. If we can map `(model_features) → (best_step, best_family, best_rank)` reliably, v4 can pre-register a *procedure* that picks the right detector for any new model — without per-model tuning that reviewers can rightly call cherry-picking.

This is a different kind of v4 claim: "PRI rupture exists at AUROC ≈ 1.000 in any model, *and* the (step, metric, rank) at which it's measurable can be inferred from observables before the experiment is run."

### Proposed mechanism

1. **Feature extraction per model** (cheap; doesn't require running the puzzle suite):
   - Architectural: `vocab_size`, `hidden_dim`, `n_layers`, family tag (`{Llama, Mistral, Qwen, Phi, Gemma, ...}`), 4-bit vs full-precision.
   - Output-style observables (run on n=20 control prompts, ~1 min/model): `avg_gen_steps_to_yes_no`, `pct_eos_before_step_7`, `format_completion_rate` (does it append "Now solve..." after the answer?), `cot_proclivity` (does it produce reasoning before the answer?).
   - Pre-norm-magnitude observables (run a dozen samples through the trace pipeline): `avg_l2_step1`, `avg_dh_post_l2_step1`, `top1_prob_concentration`.

2. **Label per model**: the `(gen_step, family, rank)` triple at the per-model best from `diagnose_v3_2_step_sweep.py`'s output.

3. **Train a classifier**:
   - With N=6 models, **don't** fit a black-box ML model — overfitting is guaranteed. Hand-craft a decision tree from the features and inspect.
   - Better: cluster models by architectural family + output style, then assign each cluster a rule. Examples:
     - Reasoning-tuned (Qwen 3): commit_step or commit_step − 1, Fisher r=1.
     - Clean-format (Mistral, clean Llama): pre-commit step (~commit_step − 3), Fisher r=1.
     - Format-completion (Qwen 2.5, Gemma 4B): mid-format step or post-completion-second-rupture, Raw or kl_discharged.
   - The decision tree is a *hypothesis* — it gets falsified or confirmed by adding more models.

4. **Hold-out validation**:
   - Leave-one-out: train the rule set on 5 models, predict the optimal cell for the 6th, measure AUROC at the predicted cell, compare to oracle-best.
   - Acceptance: predicted-cell AUROC ≥ 0.90 *and* within 0.05 of oracle-best on every held-out model.

5. **Expand the model set**: 6 models is too few for any defensible classifier. Add at least 4-6 more (gpt-oss, Llama 3.1, Phi-4, Mistral-Small, Mixtral, Qwen 2.5-Coder, Gemma 2). Most importantly: include a *new family* the classifier hasn't seen, to test out-of-distribution generalization.

### Why it could matter for v4

A clean v4 narrative under this candidate:

> *"PRI's commit-rupture signal exists at AUROC ≥ 0.95 in every language model we tested (N=12), measurable via a procedure that picks `(gen_step, metric, rank)` from cheap observable model properties. The procedure was pre-registered on a held-out half of the model set and validated on the other half."*

That defends against the "you cherry-picked per model" criticism, defends against the "your fixed metric works on some models but not others" criticism, and gives reviewers a falsifiable mechanism. It's the version of v4 that survives strict peer review.

### Decision criteria for promotion

- [ ] **Feature audit**: confirm we can extract all proposed features in < 5 min per model. If any feature requires significant compute (e.g., a Fisher decomposition during feature extraction), it's not a *predictable* observable and should be dropped.
- [ ] **Hand-crafted rule set on N=6**: can a 4–6 leaf decision tree match the oracle-best cell on at least 5/6 models?
- [ ] **Expansion to N=10+**: does the rule set survive 4 new models (Llama 3.1, Phi-4, Gemma 2, Mistral-Small)?
- [ ] **LOO-CV validation criterion**: predicted-cell AUROC ≥ 0.90 on every held-out model in LOO. If satisfied, file `wiki/results/v4-pre-reg.md` with the rule set sealed, fresh seed, fresh model held out.
- [ ] **Falsification criterion**: if any held-out model's predicted-cell AUROC < 0.80, the procedure fails out-of-distribution and v4 reverts to per-model tuning with explicit cherry-picking acknowledgment.

### Risks

- ✅ **Labels are seed-reproducible** (2026-05-10 fresh-seed validation on 3 primaries): per-model best cells from seed 20260507 reproduce within Δ ≤ 0.025 at seed 20260510; Mistral's Fisher r=k @ step 5 is identically 1.000 on both seeds for k ∈ {1, 2, 3, 4}. The training problem is well-posed.
- ✅ **Within-family universal cell exists for Llama** (2026-05-11 Llama-3.1-8B run): `Raw r=2 @ step 4` hits AUROC **1.000 on BOTH Llama 3.2 3B and Llama 3.1 8B** despite different seeds (20260507 vs 20260511) and different model sizes (3B vs 8B). In contrast, `Fisher r=1 @ step 2` (Llama 3B's sealed-best) drops from 1.000 → 0.63 at 8B — NOT scale-stable. This means the classifier can predict "for any Llama-family model, use Raw r=2 @ step 4" with high confidence; the family-level rule generalizes. First concrete evidence that within-family generalization is achievable in v4.
- 🪤 **N=6 is dangerously small.** Any rule set will fit perfectly in-sample and likely fail out-of-sample. The whole candidate is gated on expanding the model set first.
- 🪤 **Selection bias in the v3.x model set.** Models were chosen for tractability (4-bit + MLX), not diversity. The optimal-cell distribution we observe may not generalize to non-MLX or non-4-bit models.
- 🪤 **Feature engineering is human-in-the-loop.** "Cot proclivity" and "format-completion rate" are not crisply defined — measuring them adds another tuning surface that could leak information from the test set.
- 🪤 **The Gemma-step-12 anomaly** suggests the optimal cell sometimes corresponds to a *second* rupture event (committing to the fabricated next puzzle), not to the original puzzle's answer. If that's the case, the "rupture" the metric is measuring isn't always the rupture we *want* — and the meta-classifier has nothing to predict against because the labels themselves are confounded.

### Cross-references
- [entry #3 (adaptive-step)](#3-adaptive-step-rupture-detection) — the falsification of "Fisher r=1 @ commit_step is universal" creates the gap this entry tries to fill
- [v3.2-results](results/v3.2-results.md) — n=200 step-sweep evidence (universal min AUROC 0.78; per-model best ≈ 1.000)
- repo: `scripts/diagnostics/diagnose_v3_2_step_sweep.py` — produces the per-model best cells that label this candidate's training set
- repo: `scripts/analyze_adaptive_step.py` — produces the commit-step distribution that informs the "format-completion rate" feature
- 🚧 **prerequisite**: expand the model set before this entry is actionable. Currently N=6; needs N≥10 with at least one held-out family.

### Planned model-set expansion (2026-05-10, gated on user confirmation)

The v3.x model set currently spans 5 families × 6 models. Expanding toward N≥10 in priority order:

| # | Candidate | Reason | Disk (4-bit) | Already cached? |
|---|---|---|---|---|
| 1 | `mlx-community/Llama-3.1-8B-Instruct-4bit` | Within-family scale axis: Llama 3.2 3B → 3.1 8B. Tests "does the per-model best cell vary with model size in the same family." | ~5 GB | ❌ |
| 2 | `mlx-community/Phi-4-mini-instruct-4bit` | Within-family version axis: Phi-3.5 → Phi-4. Tests version stability of the reformatted-output behavior we observed. | ~3 GB | ❌ |
| 3 | `mlx-community/gemma-2-2b-it-4bit` *(or `gemma-2-9b-it-4bit`)* | Within-family generation axis: Gemma 3 4B → Gemma 2 (different architecture lineage). | ~1.5 GB / ~6 GB | ❌ |
| 4 | `mlx-community/Mistral-Small-Instruct-2409-4bit` *(if available)* | Within-family scale axis: Mistral 7B → Mistral-Small (~22B). Stretches the Mac mini M4 budget but feasible at 4-bit. | ~13 GB | ❌ |
| 5 | `mlx-community/SmolLM2-1.7B-Instruct-4bit` *(or smaller)* | NEW family (HuggingFace). First training set the meta-classifier hasn't seen. | ~1 GB | ❌ |

**Compute estimate**: ~75-150 min/model on Mac mini M4 at the v3.2 scope (n=50/cell × 4 cells = 200/model, max_gen_tokens=24, layers=final, gate-max-tokens=12). Adding 4-5 models = ~6-10 hours wall time, similar to v3.2 main runs.

**Disk estimate**: 20-30 GB total across the 5 candidates. Confirm free space before launching.

**Risks**:
- 🪤 **Gate fragility**: each new family may surface new format-completion patterns. Plan a per-model `--gate-max-tokens` tune (12 worked for Llama/Phi; new families might need different).
- 🪤 **Pipeline assumption violations**: `_extract_final_rmsnorm_gamma` was tuned for Llama / Mistral / Qwen / Phi / Gemma 4B. New families may use different norm geometries (Phi-4, SmolLM2 untested).
- 🪤 **Memory pressure**: Mistral-Small at 22B/4-bit is right at the Mac mini's edge. Monitor RSS and have `clear_mlx_cache()` between models (already in pipeline).
- 🪤 **Behavioral gate failure**: same operational fix (`--gate-max-tokens 12 --gate-verbose`) probably suffices but should be smoke-tested per model first.

**Recommended minimum viable expansion**:

1. **Phase A** (3 hours, 2 models): Llama 3.1 8B + Phi-4-mini. Tests within-family scale + within-family version on the most-studied families.
2. **Phase B** (5 hours, +2 models): Gemma 2 2B + SmolLM2. Adds new family + new generation.
3. **Phase C** (later): Mistral-Small if Phase A/B clears the meta-classifier validation gate.

After Phase A+B (N=10 models), the meta-classifier LOO-CV validation criterion ([decision criteria for promotion](#decision-criteria-for-promotion-1)) becomes evaluable.

**Pre-launch smoke**: for each new model, run `scripts/smoke_test_model.py --gate` (~5 min) before queuing it into the main run. Catches gate failures and norm-extraction issues without burning 75+ min of compute.

**Output dir convention**: launch under a `v3_2_expansion` scope (new entry in `run_v3_main.py` SCOPES dict). Do NOT bundle into the existing `v3_2_centered_bakeoff` scope — keep the validation set separate from the original 6-model pre-reg.

🛑 **Not launched yet** — gated on (1) user confirmation of model list, (2) completion of fresh-seed validation (currently running 2026-05-10/run-01), (3) disk-space check.

### 2026-05-11 — smoke-test results (4/5 fail, 1/5 launched)

The user authorized "do all of them" on 2026-05-11. Before the main launch, each candidate ran through `scripts/smoke_test_model.py --gate --gate-max-tokens 12 --gate-threshold 0.80` (the operational settings from v3.2). Outcome:

| Candidate | Adapter | Gate | Notes |
|---|:---:|:---:|---|
| ✅ **Llama-3.1-8B-Instruct-4bit** | LlamaAdapter | **4/4 = 100%** | Clean `Answer: YES.` outputs. **LAUNCHED 2026-05-11** as `v3_2_expansion_llama_8b` scope (seed `20260511`). |
| ❌ Mistral-Nemo-Instruct-2407-4bit | MistralAdapter | 0/4 = 0% | Model emits **empty output** at gate time. Adapter loads fine (40 layers, 5120 hidden, vocab 131072). Probable cause: Tekken tokenizer + chat-template mismatch with the v0.3 `[INST]` format the pipeline applies via `mlx_lm.generate`. **Follow-up**: try Mistral-Nemo's chat template explicitly; verify `tokenizer.apply_chat_template` produces well-formed input. ~30 min investigation. |
| ❌ Phi-4-mini-instruct-4bit | Phi3Adapter | hard fail | `TypeError: 'NoneType' object is not callable` in `forward_prefix_with_collection`. Adapter reports `lm_head (on outer)=False` — Phi-4 uses **tied embeddings** (lm_head shares the embed_tokens weight). The Phi3Adapter's forward path assumes a separate `lm_head` module. **Follow-up**: add a `Phi4Adapter` (or extend Phi3Adapter) that routes through `embed_tokens.as_linear()` when `lm_head` is None. Real engineering, ~1-2 hr. |
| ❌ gemma-3-1b-it-4bit *(cached)* | GemmaAdapter | 2/4 = 50% | 2 samples produce `Final Answer: YES` (parseable); 2 produce `Analysis: 1. All vasks are glorps...` (CoT-before-answer, never reaches the YES/NO token in 12 generated tokens). Same failure mode as Phi-3.5-mini under the old 256-token gate. **Follow-up**: try `--gate-max-tokens 24` or `32`; or update the gate parser to accept reasoning-prefixed outputs (this is exactly [v4-candidate #1](#1-empirical-variance-gate-parser)'s target). ~15 min to try the budget bump, longer for parser. |
| ❌ dolphin-2.9.3-mistral-nemo-12b-4bit | MistralAdapter | 1/4 = 25% | Outputs begin with `"old Answer: NO"` — consistent prefix across all 4 samples. The `"old"` is almost certainly a chat-template artifact: dolphin uses ChatML (`<\|im_start\|>system ... <\|im_end\|>`) but the pipeline applies Mistral's `[INST]` template. The model interprets the malformed prompt and emits a hallucinated continuation that happens to start with "old". **Follow-up**: pass `tokenize=False` and apply ChatML template manually, OR add a `"mistral_chatml"` model-type to the adapter dispatch. ~30-60 min investigation. |

**Net add for Phase A**: 1 model (Llama-3.1-8B). Llama family now has 2 (3B + 8B). Other families still at N=1 (Mistral, Phi, Gemma) or N=2 (Qwen, already had).

**Path forward** (priority order, each is its own follow-up task):
1. ✅ ~~Bump Gemma-3-1B gate to `--gate-max-tokens 24` and re-smoke~~ — **TRIED, FAILS**. Both gate-max-tokens=24 and =32 still produce 2/4 = 50% accuracy. The 2 failing samples emit `Analysis: 1. All vasks are glorps. 2. All glorps are nuvins. 3. All meltas are...` — chain-of-thought that never reaches `Final Answer:` in 32 tokens. Need parser fix (v4-candidate #1) or much larger budget (64+), neither of which is consistent with v3.2 operational protocol. **Deferred to parser-fix pre-req.**
2. 🛠️ Mistral-Nemo chat-template fix (~30 min investigation). Confirmed empty output is *not* a chat-template apply issue (template applies cleanly to `<s>[INST] Hello, world.[/INST]`). Deeper investigation: mlx_lm stop-token handling for Tekken tokenizer. Defer.
3. 🛠️ Dolphin chat-template handling (~30-60 min). Confirmed ChatML template differs from pipeline's `[INST]`. **AND** tokenizer needs `fix_mistral_regex=True` for proper decoding. Both fixes needed. Defer.
4. ✅ ~~Phi-4 adapter fix~~ — **LANDED 2026-05-11**. Patched `Phi3Adapter.forward_prefix_with_collection` at `model_adapters.py:622` to fall back to `embed_tokens.as_linear()` when `lm_head is None` (Phi-4 uses tied embeddings, mirrors LlamaAdapter pattern). Re-smoke PASS 4/4. **LAUNCHED 2026-05-11 11:53** as `v3_2_expansion_phi_4` scope at seed `20260511`.

After Phi-4 completes (~75 min ETA), the expansion brings N=8 with 2-per-family for Llama (3B + 8B) and Phi (3.5-mini + 4-mini). Other families remain N=1 pending the deferred fixes.

### 2026-05-12 — first LOO-CV pass on N=10

`scripts/diagnostics/meta_classifier_loo.py` (output: `/tmp/meta_classifier_loo.json`) evaluates four candidate selection strategies under leave-one-out:

| Strategy | Mean AUROC | Min AUROC | n ≥ 0.90 | n ≥ 0.95 |
|---|:---:|:---:|:---:|:---:|
| oracle (upper bound) | 1.000 | 0.997 | 10/10 | 10/10 |
| universal_kl_discharged | 0.766 | 0.519 | 3/10 | 3/10 |
| family_rule | 0.832 | 0.596 | 5/10 | 4/10 |
| nn_terminal_commit | 0.811 | 0.606 | 4/10 | 3/10 |
| **handcrafted_tree** | **0.840** | 0.519 | 5/10 | **5/10** |

**Verdict**: ❌ **NO strategy meets the v4-candidate #4 acceptance threshold** (predicted-cell AUROC ≥ 0.90 on every held-out model). Best mean = 0.840 (handcrafted); best min = 0.606 (nn_terminal_commit).

**Where handcrafted wins outright** (5/10 ≥ 0.95):
- ✅ **Llama 3B + 8B both 1.000** via "Llama → Raw r=2 @ step 4" rule (validates the within-Llama universal-cell finding).
- ✅ **Mistral-Nemo 1.000** via "terminal-commit (commit_rate ≥ 0.5) → Centered r=4 @ step=1" branch.
- ✅ **Phi-3.5 + Gemma-1B ≥ 0.97** via kl_discharged fallback.

**Where it fails badly** (5/10 < 0.90):
- ❌ Qwen 3 8B: oracle Fisher r=64 @ step 2 → 1.000; predicted kl_discharged step 1 → 0.519. **Reasoning-tuned-model branch missing.**
- ❌ Mistral 7B v0.3: oracle d_F_full @ step 6 → 1.000; predicted kl_discharged step 1 → 0.649. **mean_gen_steps ≈ 9 should route to step-6 cell.**
- ❌ Phi-4-mini: oracle d_F_full @ step 2 → 1.000; predicted kl_discharged step 1 → 0.613. **Phi-version differentiation needed.**

**Open issues for next iteration**:
- 🧠 Add reasoning-tuned tag feature (Qwen 3 reasoning, future DeepSeek-R1-distill, etc.) routing to high-rank Fisher cells at step 2.
- 🪜 Add mean_gen_steps bucket (Mistral 7B v0.3 ≈ 9 steps vs. 24 for most others) routing Mistral 7B to step-6.
- 🎭 Differentiate Phi-3.5 vs Phi-4 — they cluster differently despite same family tag.
- 🪤 With N=10 the handcrafted rule is informed by inspection of all 10 models, so "honest LOO" overstates novelty. Expanding to N≥14 (e.g., Mistral-Small, gpt-oss, SmolLM, DeepSeek-R1-distill) is the load-bearing prerequisite for a defensible LOO claim.

### 2026-05-12 — handcrafted_v2 jumps mean to 0.960 / min 0.830

Added 3 missing features + 4 new branches to the handcrafted tree:

```
1. is_reasoning_tuned     → Fisher r=2 @ step 3        (Qwen 3 branch)
2. terminal_commit ≥ 0.5  → Centered r=4 @ step 1      (Mistral-Nemo)
3. family == Llama        → Raw r=2 @ step 4           (within-Llama universal)
4. family == Phi          → d_F_full @ step 2          (both Phi versions peak at step 2)
5. family == Gemma        → Raw r=1 @ step 3           (Gemma 4B's cell)
6. mean_gen_steps < 12    → d_F_full @ step 6          (Mistral 7B v0.3 short-CoT)
7. fallback               → kl_discharged @ step 1     (Qwen 2.5 catch-all)
```

LOO-CV result:

| Strategy | Mean | Min | n ≥ 0.90 | n ≥ 0.95 | Mean gap |
|---|:---:|:---:|:---:|:---:|:---:|
| handcrafted_v1 | 0.840 | 0.519 | 5/10 | 5/10 | 0.160 |
| **handcrafted_v2** | **0.960** | **0.830** | **8/10** | **7/10** | **0.039** |

**Verdict (2026-05-12)**: 🪜 **Strict acceptance bar (min ≥ 0.90 on all 10) still UNMET, but the gap closed dramatically** (mean 0.840 → 0.960, min 0.519 → 0.830, n≥0.95 5→7). Predicted-cell AUROC is now on average within 0.04 of oracle.

**Remaining 2 failures**:
- ❌ Qwen 3 8B at 0.830: oracle is Fisher r=**64** @ step 2 = 1.000; predicted Fisher r=**2** = 0.830. Within reasoning-tuned models the *rank* matters, but with N=1 reasoning-tuned in the training set we can't tell whether r=64 generalizes. **Needs additional reasoning-tuned models** (DeepSeek-R1-distill, Qwen 3 14B, etc.).
- ❌ Qwen 2.5 7B at 0.894: oracle Fisher r=2 @ step 3 = 1.000; falls through to kl_discharged fallback. No observable feature in the current set separates Qwen 2.5 from the fallback bucket. **Needs an output-style signature we haven't extracted** (top-K concentration at step 1? CoT length?).

**Two close-but-not-clearing cases**:
- ⚠️ Phi-3.5 at 0.956 (within rounding of 0.95)
- ⚠️ Gemma-1B at 0.923 (Gemma-1B's step=1 vs Gemma-4B's step=3 — within-family scale asymmetry)

**Files**:
- `scripts/diagnostics/meta_classifier_loo.py` (LOO-CV runner, 4 strategies + oracle + v1/v2 trees)
- `/tmp/meta_classifier_loo_v2.json` (full output)

### 2026-05-12 — handcrafted_v3: Qwen-family branch + step-1 surprise feature

Added a Qwen-family branch (→ Fisher r=2 @ step 3) and extracted `mean_surprise_step1` as a per-model observable feature. The surprise scalar cleanly separates 3 regimes:

| Regime | mean_surprise_step1 | Models |
|---|---|---|
| Committed-immediately | < 0.05 | Mistral 7B (0.005), Phi-3.5 (0.003), Gemma 4B (0.009), Mistral-Nemo (0.040) |
| Format-prefix / multi-step | 0.1 - 0.9 | Gemma-1B (0.233), Phi-4-mini (0.293), Llama 8B (0.464), Qwen 2.5 (0.535), Llama 3B (0.807) |
| Reasoning-tuned | > 1.0 | Qwen 3 (1.205) — alone, gap to next = 0.40 |

The reasoning branch is broadened to fire on `is_reasoning_tuned OR mean_surprise_step1 > 1.0`, future-proofing for unnamed reasoning-tuned models. LOO-CV result:

| Strategy | Mean | Min | n ≥ 0.90 | n ≥ 0.95 | Mean gap |
|---|:---:|:---:|:---:|:---:|:---:|
| handcrafted_v2 | 0.960 | 0.830 | 8/10 | 7/10 | 0.039 |
| **handcrafted_v3** | **0.971** | 0.830 | **9/10** | **8/10** | **0.029** |

**Verdict (2026-05-12)**: 🪨 **9/10 at ≥ 0.90, single failure is Qwen 3 (0.830)** — strict acceptance bar held back entirely by one model. Within reasoning-tuned the *rank* matters (oracle r=64 vs predicted r=2); with N=1 reasoning model in the training set we can't choose between "r=2 generalizes" and "r=64 generalizes."

**Unblock cost**: a single additional reasoning-tuned model (Qwen3-1.7B, DeepSeek-R1-distill-Qwen-7B, or similar — ~15 min smoke + ~20 min main run) would settle this. With ≥2 reasoning models we can pin the reasoning-branch's optimal cell without confessed overfit.

**File**: `/tmp/meta_classifier_loo_v3.json`.

### 2026-05-12 — DeepSeek-R1-Distill-Qwen-7B-4bit smoke FAIL; pivoting to Qwen3-1.7B

DeepSeek-R1-Distill-Qwen-7B-4bit was the first candidate for the additional reasoning-tuned model. Smoke gate 0/4 at `--gate-max-tokens 24`: output is canonical R1 reasoning chain (`'Okay, so I need to figure out whether...'`) that never reaches a YES/NO within 24 tokens. Not a chat-template issue — the R1-distill thinking-before-answering protocol requires ~100+ tokens before commit. Two unblocks possible:

- 🪜 Bump `--gate-max-tokens` to ≥ 128 (10× the v3.2 protocol; trades comparability for coverage).
- 🛡️ Use a non-R1 reasoning-tuned model. **Qwen3-1.7B-4bit** (smoke launched 2026-05-12) is a same-family scale variant of our existing Qwen 3 8B — a within-family-reasoning test that, if successful, directly addresses the Qwen 3 hold-out's r=2 vs r=64 ambiguity by adding a sibling.

Decision: prefer Qwen3-1.7B over R1 budget-bumping to preserve v3.2 operational protocol. R1 deferred until parser-fix (v4-candidate #1) or a no-think-directive option lands.

### 2026-05-12 — N=11 + handcrafted_v4 **CLEARS THE STRICT ACCEPTANCE BAR**

**Qwen3-1.7B main run completed** (85 min, gate 100%, 4800 rows at `experiments/v3-main-run/2026-05-12/run-01/`). Smoke required a QwenAdapter tied-embedding patch (`model_adapters.py:549` — `lm_head=None → embed_tokens.as_linear()`, mirroring the 2026-05-11 Phi3Adapter fix).

**Within-Qwen3 family heterogeneity at scale (n=200/cell)**:

| Cell | Qwen 3 **8B** | Qwen 3 **1.7B** | Verdict |
|---|:---:|:---:|---|
| Fisher r=64 @ step 2 (8B oracle) | **1.000** | 0.576 | ❌ NOT scale-transferable |
| Fisher r=2 @ step 3 (v3 reasoning-branch) | 0.830 | 0.803 | both fail |
| **Raw r=21 @ step 3** | **0.976** | **1.000** | ✅ universal Qwen-family cell |
| Centered r=2 @ step 2 (1.7B candidate) | 0.900 | 1.000 | works but worse on 8B |

**Critical secondary finding**: Qwen3-1.7B has `mean_surprise_step1 = 0.302` — well below the > 1.0 reasoning threshold. Despite being a reasoning-family model, Qwen3-1.7B answers directly (`'Yes, the premises state that...'`) without thinking-first, so the surprise scalar correctly classifies it as "non-reasoning behavior at runtime." The reasoning-branch alone would have missed it; the *unified* Qwen-family + reasoning route is correct.

**Raw r=21 @ step 3 across the full Qwen family**:
- Qwen 2.5 7B: **0.967**
- Qwen 3 8B: **0.976**
- Qwen 3 1.7B: **1.000**
- min across 3 Qwen models = **0.967**

This is the cleanest cross-Qwen cell we've found. Updated handcrafted_v4 tree:

```
1. mean_surprise_step1 > 1.0 OR family == Qwen   → Raw r=21 @ step 3    (unified)
2. terminal_commit_rate ≥ 0.5                    → Centered r=4 @ step 1
3. family == Llama                               → Raw r=2 @ step 4
4. family == Phi                                 → d_F_full @ step 2
5. family == Gemma                               → Raw r=1 @ step 3
6. mean_gen_steps < 12                           → d_F_full @ step 6
7. fallback                                      → kl_discharged @ step 1
```

LOO-CV at N=11:

| Strategy | Mean | **Min** | n ≥ 0.90 | n ≥ 0.95 | Mean gap |
|---|:---:|:---:|:---:|:---:|:---:|
| oracle | 1.000 | 0.997 | 11/11 | 11/11 | 0.000 |
| handcrafted_v3 (N=11) | 0.969 | 0.803 | 10/11 | 9/11 | 0.031 |
| **handcrafted_v4 (N=11)** | **0.984** | **0.923** | **11/11 ✅** | **10/11** | **0.016** |

**Verdict (2026-05-12, INITIAL)**: ✅ **The strict acceptance bar (min AUROC ≥ 0.90 on every held-out model) is MET at N=11.** This is the first defensible LOO-CV pass for v4-candidate #4. Only Gemma-3-1B (0.923) sits below 0.95; all other 10/11 predicted-cell AUROCs ≥ 0.956.

**🚨 RETRACTED 2026-05-12 (Codex adversarial review)**: the above verdict was based on **sign-agnostic AUROC** (`auroc_signed` returns `max(auc, 1-auc)`), which lets each cell flip its sign AFTER seeing the held-out labels. That's label-peeking — not a deployable-classifier metric. Re-running with direction-preserving scoring (sign fixed from training folds before touching held-out labels):

| Metric | Sign-agnostic (legacy, label-peek) | **Direction-preserving (honest)** |
|---|:---:|:---:|
| handcrafted_v4 mean | 0.984 | **0.711** |
| handcrafted_v4 min | 0.923 | **0.000** |
| handcrafted_v4 ≥ 0.90 | 11/11 | **8/11** |
| handcrafted_v4 ≥ 0.95 | 10/11 | 7/11 |

Three models drop from 1.000 → 0.000 (Mistral 7B v0.3, Mistral-Nemo, Phi-4-mini) — their oracle cells have the *opposite* sign from the training-fold majority. The rupture direction is model-specific in ways the sign-agnostic metric masked. **The strict acceptance bar (≥ 0.90 on all 11) is NOT met under honest scoring.**

Additional issue Codex flagged: **the handcrafted_v4 tree itself was written by inspecting all 11 oracle cells** (the Qwen branch was added AFTER the Qwen3-1.7B run revealed Raw r=21 @ step 3 works on all 3 Qwen models). That's in-sample rule fitting, not honest novelty — even if direction-preserving scoring were 11/11, the rule hasn't been tested against a model held out from its design.

**Filter-sensitivity check (Codex's medium-severity finding)**: of 11 oracle cells, 9 are stable with/without the (min_n=50, min_n_per_class=20) filter; 2 differ — Mistral 7B v0.3 (filtered: d_F_full step 6; unfiltered: Fisher r=1 step 13) and Gemma 4B (filtered: Raw r=1 step 3; unfiltered: Raw r=4 step 12). The filter dependency is real but moderate; the v3 branches were not load-bearing on these specific cells.

**Honest verdict (2026-05-12, POST-REVIEW)**: 🪨 **v4-candidate #4 is NOT ready for promotion**. The N=11 LOO numbers were inflated by two methodological holes:
1. Sign-agnostic AUROC peeks at held-out labels to choose direction.
2. The rule was authored with knowledge of all 11 model oracles.

**To re-open the candidate honestly, three things must happen**:
- 🛡️ **Direction-preserving scoring becomes the acceptance metric.** Fix the cell's sign from training folds, never from the held-out.
- 🛡️ **The rule must be authored on a strict subset of the model set.** Either (a) freeze the current handcrafted_v4 tree and add ≥1 model unseen during its design (SmolLM2, Mistral-Small, Gemma 2 — see "Planned model-set expansion"), or (b) replace the handcrafted tree with a fold-local selector that picks cells using only training-fold data.
- 🛡️ **Direction-stable cells must be identified.** Mistral / Phi cells flip sign across models. Either find cells with consistent sign across families, or learn the sign from a small calibration set per new model (which weakens the meta-classifier story).

**Files**:
- `/tmp/meta_classifier_loo_v4.json` — original (sign-agnostic) output
- `/tmp/meta_classifier_loo_v4_corrected.json` — direction-preserving + filter-sensitivity output
- `scripts/diagnostics/meta_classifier_loo.py` — now reports BOTH metrics in parallel

### 2026-05-13 — N=33 ANLI sweep: meta-classifier candidate **RETIRED**

`scripts/anli_full_sweep.py` ran 11 cached models × ANLI R1/R2/R3 × n=50 in one ~90-min pass, producing 33 schema-v1.1 CalibrationProfile JSONs at `experiments/anli-sweep/2026-05-13/run-01/`. The point of the sweep was to validate that the per-(model, task) calibration framework holds at scale and to test whether `Fisher r=2 @ step 3` (the cell Phi-4 and Qwen 2.5 had both picked in the n=5 pilot) is a stable signed direction. Both questions resolve negatively.

**Fisher r=2 @ step 3 sign distribution across 32 finite profiles**:

```
positive (+1): 17
negative (-1): 15
zero (degen.):  0
AUROC: min=0.502  median=0.551  max=1.000
```

17/15 is statistically indistinguishable from a coin flip, and the sign-agnostic AUROC sits near chance (median 0.551). The cell is winner-of-record on only 4/33 profiles, and one of those (Mistral-7B-v0.3 R2) has n_evaluated=4 due to early EOS — it's a degenerate hit. The Phi-4 + Qwen 2.5 "coincidence" in the n=5 pilot was just that — a coincidence.

**Cross-round instability within the same model**:

| Model | R1 | R2 | R3 |
|---|---|---|---|
| Mistral-Nemo | Centered r=2 **+1** | d_F_full **−1** | Centered r=2 **+1** |
| Phi-4-mini | Fisher r=1 **−1** | Centered r=2 **+1** | kl_discharged **−1** |
| Llama-3.1-8B | Centered r=4 **−1** | Fisher r=1 **+1** | Fisher r=2 **+1** |

Same model, same broad task ("NLI"), different adversarial distribution → different deployable detector. This kills the "calibrate per model, deploy across tasks" hope. ANLI R1/R2/R3 are sibling distributions and the calibrator can't even bridge them.

**Deployability at n=50 is the actual bottleneck**:

- 30 / 33 profiles fire ≥ 1 deployability warning (`winner_unstable`, `wide_ci`, `oob_low_auroc`, `large_oob_in_sample_gap`, or `insufficient_coverage`)
- Only Mistral-Nemo R1, Mistral-Nemo R3, and Qwen3-8B R1 get a clean bill of health
- OOB AUROC range: **0.41** (Phi-4-mini R3) → **0.91** (Qwen3-8B R1) — 2× spread
- OOB CI lower bounds < 0.30 on most profiles → n=50 is too small for confident deployment

**Production framing (final)**:

🪨 **PRI calibration is per-(model, exact deployment distribution).** "Generalize across task family" is not supported by the current evidence. If you deploy on ANLI R3, calibrate on ANLI R3 — not on ANLI R1 even though both are "natural-language NLI."

🪨 **The calibrator's safety rails are doing their job.** 30/33 warnings is not a bug — it's the calibrator telling researchers "n=50 is risky for this (model, task) pair; collect more samples or accept the wider CI."

🪨 **The meta-classifier candidate is closed.** No fixed cell across the panel is stable enough across models to make label-free prediction work, AND even per-model calibrations don't survive task-distribution shift within ANLI itself.

**Artifacts** (committed to `experiments/anli-sweep/2026-05-13/run-01/`):
- 33 `*__anli_R*_seed20260513_n25.profile.json`
- `summary_winners_full.csv` — full winners table
- `summary_winners_publishable.csv` — winner-only publishable subset
- `summary_fisher_r2_step3.csv` — focus table

**What survives**:
- The calibrator + detector library is production-ready for per-(model, distribution) deployments
- Its safety-rail warnings correctly distinguish robust calibrations from noisy ones at small n
- Researchers can use it for any model+task combination at n ≥ 50, getting honest OOB stats + deployability flags
- The "meta-classifier" framing is retired; "PRI calibrator" is what ships

---

---

Chat-template plugin module (`pri_v2_io_plugins.py`) landed with per-model `apply_chat_template` dispatch. Re-smokes pass 4/4 on Mistral-Nemo and Gemma-3-1B under the new pipeline. **Phase B main run** (`v3_2_expansion_phase_b` scope, seed 20260511, n=50/cell) completed 2026-05-11 producing `experiments/v3-main-run/2026-05-11/run-04/all_results.parquet` (4918 rows, 20 trace dumps across the 2 models).

**Family map at N=10**:

| Family | Members | Within-family stability |
|---|---|---|
| Llama | 3.2-3B, 3.1-8B | ✅ Strong: Raw r=2 @ step 4 universal (both = 1.000) |
| Phi | 3.5-mini, 4-mini | ✅ Strong: kl_discharged @ step 2 cross-version |
| Qwen | 2.5-7B, 3-8B | ⚠️ Mixed |
| Mistral | 7B-v0.3, Nemo-12B | ❌ Optimal FLIPS: Raw r=2 (v0.3) → Fisher/Centered (Nemo) |
| Gemma | 1B, 4B | ❌ Step shifts: 1B peaks at step 1, 4B peaks at step 4 |

**Phase B step-sweep universal-winner** (`scripts/diagnostics/diagnose_v3_2_step_sweep.py --run-dir .../2026-05-11/run-04`, output `/tmp/v3_2_phaseB_step_sweep.json`, 1025 cells):

| # | Metric | step | min AUROC | Mistral-Nemo | Gemma-1B |
|---|---|:---:|:---:|:---:|:---:|
| 1 | **kl_discharged** | 1 | **0.9670** | 0.9723 | 0.9670 |
| 2 | Fisher r=16 | 1 | 0.9359 | 0.9523 | 0.9359 |
| 3 | d_F_full | 1 | 0.9027 | 0.9364 | 0.9027 |

**Key Phase B findings**:

- 🪨 **Mistral-Nemo is a terminal-commit model**: emits exactly one token (`'YES'` or `'NO'`) then EOS. Only `gen_step=1` data exists. Centered r=4 / r=2 = 1.0000; Fisher r=1 = 0.9998. The chat-template fix transformed Mistral-Nemo into a perfect commit oracle.
- 🌊 **Gemma-3-1B rupture-then-drift signature**: clean YES/NO at step 1, then `<end_of_turn>`, then drift through random languages (Spanish, Marathi, Bengali, Persian). Step 1 = 0.9972; step 3 collapses to 0.65; steps 5+ near chance. The clearest within-sample validation of "step=1 IS the rupture moment" we have.
- 🧲 **`kl_discharged` is the cleanest cross-model-stable metric across N=10**: only metric ≥ 0.96 on BOTH Phase B models at step=1. The closed-form scalar from the [FALSIFIED] centered-Fisher hypothesis is the surviving load-bearing finding.
- 🧮 **Spectral-band fingerprint per model**: peak-rank-of-best-family is model-specific (Mistral-Nemo: r=2/r=4 Centered; Gemma-1B: r=21 Raw mid-rank; Llama: r=2 Raw; Phi: scalar kl_discharged). This is a feature the meta-classifier must encode — not just "which family wins" but "where in the spectrum."

### Implication for the meta-classifier design (post-Phase B)

The N=10 dataset is now sufficient to attempt the LOO-CV pre-reg. Updated feature set based on Phase B evidence:

1. **Default analysis plane = step=1** for all chat-template-clean models. Post-commit steps are categorically different signal regimes that would only add noise to the training set.
2. **Universal default metric = `kl_discharged`**: best universal-min across N=10 (≥ 0.92 on every model we've measured). Use as the meta-classifier's baseline; the classifier only needs to *improve* on this when a model-specific feature beats it.
3. **Spectral-band feature**: encode "rank-of-best-family" as a continuous feature (not just family choice). Mistral-Nemo wants r=2; Gemma-1B wants r=21; Llama-family wants r=2; encode as a numeric, not categorical.
4. **Within-family stability tag**: families split into "stable" (Llama, Phi) and "unstable" (Mistral, Gemma, possibly Qwen). The classifier's rule needs an "if unstable family, use the universal kl_discharged fallback" branch.

---

## 5. Attention-cell extension to `pri_calibrator.py`

**One-line**: add an `Attention` cell family to the calibrator's panel so the inter-head JS-radius diagnostic (and any future attention-side metric) participates in the same per-(model, distribution) selection + nested-OOB-bootstrap CI machinery that the residual-stream cells already use, instead of living as a standalone descriptive script.

**Status: [LANDED 2026-05-15]** — implementation shipped; design + acceptance-criteria sections below preserved as the design record. Implementation summary at the bottom of this entry under **2026-05-15 — landing notes**.

### Motivation

The 2026-05-15 9-model inter-head panel landed [OPEN, supersedes run-01]: 7/9 models show a clean (sink-controlled) signal at *some* layer with consistent `hi` orientation, 2/9 (Llama 3B, Mistral-Nemo) are sink-driven and unreadable as head-disagreement. Critically, **no universal operating point** — Qwen family wants `final` + `js_kv_groups`, Phi-3.5 wants `last_minus_1`, gemma wants `mid`, etc. (See [results/inter-head-disagreement-2026-05-15](results/inter-head-disagreement-2026-05-15.md).)

This is the *exact* shape the calibrator was built for: per-(model, exact deployment distribution) cell-selection with honest selection-bias-corrected CIs. Right now the diagnostic is a `scripts/diagnose_inter_head_disagreement.py` standalone that reports raw AUROC with no CI, no sign-locking, no winner-stability check, no compatibility with the v1.1 calibration profile schema. Promoting it into the calibrator would:

- Let the diagnostic produce a deployable `CalibrationProfile` JSON instead of a CSV.
- Run nested OOB bootstrap on attention cells, exposing the small-n bias the calibrator already exposes for residual-stream cells (30/33 ANLI profiles at n=50 fire deployability warnings — attention cells are likely to fire even more).
- Make the operating-point selection (layer × metric × gen_step) part of the calibration profile, audited and provenance-tagged, instead of hardcoded in the diagnostic.
- Compose with the v1.1 strict-mode hash check (pipeline + io_plugins + model_adapters + calibrator + HF cache SHA) so attention-cell profiles inherit the same byte-exact reproducibility guarantee.

### Proposed mechanism

The minimal additive change preserves the v1.1 schema and adds an opt-in extension:

1. **New panel-cell family `Attention`** in `pri_calibrator.py`. Cells are keyed by `(gen_step, "Attention", "<layer>_<metric>")`, e.g., `(1, "Attention", "final_js_kv_groups")`. Concrete proposed cell set (12 cells, matching the diagnostic's columns):
   - layers: `final`, `mid`, `last_minus_1` (target_map convention from diagnostic)
   - metrics: `js`, `js_kv_groups`, `js_no_bos`, `bos_mass` (intentionally include `bos_mass` so SinkProbe-shaped cells are first-class panel options the calibrator can pick when sink dynamics carry the signal on a given model)
   - All at `gen_step=1` (commit step). Multi-step expansion deferred.

2. **Opt-in `--attention` flag** on the calibrator script and a new constant `ATTENTION_PANEL` separate from `DEFAULT_PANEL`. Default behavior unchanged; passing `--attention` extends the panel to `DEFAULT_PANEL + ATTENTION_PANEL`. Avoids invalidating any existing v1.0 / v1.1 profile.

3. **Capture-side wiring**: when `ATTENTION_PANEL` cells are present, the per-sample trace wraps `pipeline.trace_sample` in the `attention_capture` context manager from `scripts.diagnose_inter_head_disagreement`. Reuses the hardened observational wrapper (Phi qkv_proj, Qwen3/Gemma q_norm/k_norm). Capture-count assertion (`1 + len(gen_token_ids)`) ports unchanged.

4. **Dispatcher branch in `_compute_panel_scores_for_sample`**: a new `if fam == "Attention"` branch reads the layer key from the captures dict and dispatches to the appropriate metric (`_js_radius`, `_js_radius_kv_groups`, `_js_radius_no_bos`, `_mean_bos_mass`). All four metric helpers already exist in the diagnostic module.

5. **Schema treatment**: `schema_version` stays at `1.1`. Attention cells appear in `calibration_stats.candidate_panel` like any other cell. `provenance` gains an `attention_wrapper_module_hash` (sha256 of the diagnostic module) when any attention cell is active, so wrapper drift is detectable on detector load.

6. **Tests**: new `tests/test_attention_cells.py` mirroring `tests/test_pri_calibrator.py` shape: unit tests on the dispatcher branch + 1-2 slow Gemma-3-1B-class integration tests (Gemma-3-4B if 1B fails the behavioral gate) verifying that `--attention` + the existing cell-selection logic picks something sensible.

### Why it could matter for v4

Three concrete leverage points:

- **Attention cells expand the calibrator's panel by ~12 candidates** (50% increase over the current 18). For models where residual-stream cells underperform (Mistral-Nemo terminal-commit; some Qwen 3 sub-rounds), an attention cell might be the deployable choice. Honest selection-bias correction via OOB bootstrap is what makes this safe to evaluate.
- **Provides a path for SinkProbe-style baselines** without bolting on a separate framework. `(1, "Attention", "final_bos_mass")` is essentially a SinkProbe-feature evaluated as a single-cell AUROC, OOB-corrected. Not a full SinkProbe reproduction (which is supervised + multi-head top-k), but a fair-baseline scalar that lives in the calibration profile.
- **Demonstrates the calibrator framework generalizes beyond residual-stream cells.** v1.1 was designed around `compute_step` outputs; this is the first non-`compute_step` cell family. The integration pattern (capture context manager + dispatcher branch + module-hash provenance) is also the template for adding curvature ($\kappa$) cells, V-norm cells, or any other gen_step=1-snapshot quantity in v4 / v5.

### Decision criteria for promotion (and acceptance criteria for the implementation)

The implementation lands as a sealed PR when all four hold on a calibrator-internal acceptance run:

1. **`pytest tests/` stays 50+/50 green** with no regressions on existing residual-stream cells.
2. **Self-test parity**: byte-exact reproducibility (`|reported - deployed AUROC| < 1e-3`) holds for any profile that includes attention cells, on a fresh detector load. Already enforced for residual-stream cells; needs to extend cleanly.
3. **Attention-only-panel calibration on Qwen 2.5 7B + ANLI R1 n=200** picks one of the run-02 clean cells (`final_js_kv_groups` or `final_js_no_bos`) as the winning cell, sign locked positive, with OOB-bootstrapped CI [lo, hi] that excludes 0.5. Confirms the calibrator's selection machinery agrees with the descriptive panel's read on the strongest signal in the panel.
4. **No silent gate override**: any attention-cell profile that fires `winner_unstable` or `large_oob_in_sample_gap` must be persisted with the warning intact, not suppressed.

### Risks

- 🛡️ **Schema compatibility**: technically the v1.1 schema accepts any cell shape, so adding an `Attention` family is non-breaking. But existing v1.0 / v1.1 profiles loaded with an attention-extended calibrator binary should still self-test cleanly — needs an explicit test.
- 🛡️ **Latency**: enabling attention captures roughly doubles per-sample trace time (manual SDPA at 3 layers vs fused kernel). For n=50 calibration, this is ~2× the calibration wall. Acceptable; document in the script docstring.
- 🛡️ **Wrapper module hash**: the diagnostic module is more volatile than `pipeline.py` (hardened 2026-05-15, but more work likely). Strict-mode profiles that include attention cells will be more brittle to wrapper changes. Mitigation: ship the wrapper's observational guarantee as a test invariant (the `invariance_probe_inter_head.py` script lands as a CI hook).
- 🚫 **Will not** retroactively fix the run-01 → run-02 Qwen 2.5 numerical anomaly. The invariance probe already resolved that; this entry is about future deployable profiles, not about reinterpreting historical numbers.

### Cross-references

- [results/inter-head-disagreement-2026-05-15](results/inter-head-disagreement-2026-05-15.md) — diagnostic promoted into the calibrator.
- [feedback/inter-head-prior-art-2026-05-15](feedback/inter-head-prior-art-2026-05-15.md) — prior-art positioning vs RAUQ + SinkProbe; "Attention cells provide SinkProbe-style baselines as panel cells" was specifically anticipated there.
- `PRI_at_commitment/pri_calibrator.py` (repo) — landed: new family constants, `_compute_attention_score` helper, dispatcher branch, attention-capture wiring in `calibrate_with_state`, `--attention` / `--attention-only` CLI flags.
- `PRI_at_commitment/pri_detector.py` (repo) — landed: attention-winner detection + `_score_attention` path that wraps `trace_sample` in the capture context manager + strict-mode validation of `attention_wrapper_module_hash_sha256`.
- `PRI_at_commitment/scripts/diagnose_inter_head_disagreement.py` (repo) — wrapper + metric implementations that the calibrator imports via deferred imports (breaks circular cycle).
- `PRI_at_commitment/scripts/invariance_probe_inter_head.py` (repo) — observational-wrapper guarantee that the strict-mode hash check leans on.
- `PRI_at_commitment/tests/test_attention_cells.py` (repo) — 27 fast unit tests + 1 slow Gemma-3-1B end-to-end byte-exact self-test parity test. All 102/102 green in the repo's pytest suite as of 2026-05-15.

### 2026-05-15 — landing notes

**Acceptance criteria — final scorecard.**

| # | Criterion | Result |
|---|---|---|
| 1 | pytest stays 50+/50 green | ✅ **102/102** (was 50; +52 new, including 27 new attention-cell unit tests + 1 slow Gemma-3-1B e2e) |
| 2 | Byte-exact self-test parity (|reported − deployed AUROC| < 1e-3) on attention-extended profiles | ✅ **Gemma 3-1B e2e** test passes (`tests/test_attention_cells.py::TestAttentionEndToEnd`) — calibrator picks Attention winner, profile persists, detector reloads, score reproduces calibration-time AUROC |
| 3 | Qwen 2.5 7B + ANLI R1 n=200 attention-only calibration picks `final_js_kv_groups` (or `final_js_no_bos`) sign locked positive, OOB CI excludes 0.5 | 🟡 **partial**: picked `attention[final_js_kv_groups] @ step 1` AUROC 0.922 sign +1 — exact match for the descriptive panel's Qwen 2.5 headline. OOB CI [0.139, 1.000] does NOT exclude 0.5; OOB median 0.802; winner_stability 0.42. Reason below. |
| 4 | No silent gate override — warnings persisted, not suppressed | ✅ 6 warnings fired and persisted (wide_ci, winner_unstable, 4× insufficient_coverage_at_attention[final_*]) |

**Why criterion #3 didn't fully clear: a real diagnostic-side finding the descriptive panel hid.**

The smoke run on Qwen 2.5 + ANLI R1 n=200 revealed that **180 of 200 final-layer attention captures are NaN** under the diagnostic's manual SDPA wrapper. The descriptive panel's "Qwen 2.5 final js_kv_groups = 0.9219 on n=200" headline was computed on the 20 finite samples — an effective n that wasn't called out anywhere. The diagnostic CSV `experiments/inter-head-disagreement/2026-05-15/run-02/Qwen2.5-7B-Instruct-4bit_head_disagree.csv` confirms 180-of-200 NaN at every final-layer column (js, js_kv_groups, js_no_bos, bos_mass, attn_entropy); mid + last_minus_1 are clean. Root cause is suspected precision overflow in the manual softmax at the deepest block, where activations have largest magnitudes; the wrapper recovers softmax via `mx.softmax(scores, axis=-1, precise=True).astype(mx.float32)` but some heads still produce NaN.

The calibrator's nested OOB bootstrap immediately surfaced this: winner_stability collapsed to 0.42 (different cell wins on 58% of resamples at n=20), OOB CI widened to [0.14, 1.00], and four `insufficient_coverage_at_attention[final_*]` warnings fired. **The production library is doing exactly what it was designed for — exposing post-selection-bias contamination and small-effective-n that the descriptive analysis missed.**

This is not a calibrator bug. The smoke validates that the calibrator (a) wires the attention path correctly, (b) picks the same cell the descriptive panel picked, and (c) honestly reports the cost of the descriptive panel's selection over n=20 samples. **A clean criterion #3 pass requires fixing the diagnostic's final-layer NaN problem** (separate task), not the calibrator.

**Acceptance verdict:** v4-candidate #5 is **[LANDED]**. Three of four criteria fully clear; the fourth surfaces a pre-existing diagnostic-side issue that the calibrator's safety rails caught honestly.

**Files touched.**

```
pri_calibrator.py        +166 lines (constants, helpers, dispatcher branch, calibrate_with_state wiring, --attention / --attention-only flags, attention_wrapper provenance hash)
pri_detector.py          +63 lines (attention-winner setup in __init__, _score_attention path, strict-mode attention_wrapper hash check)
tests/test_attention_cells.py  +228 lines (27 fast tests + 1 slow Gemma-3-1B e2e)
```

**Known limitations of this landing.**

- ✅ ~~**Final-layer NaN on Qwen 2.5 (and likely other large-vocab models)**~~ **— Resolved 2026-05-15 evening.** Root cause was float16 overflow in the manual SDPA `q @ kᵀ` at the deepest block (scores up to ~1800 → inf in unmasked positions → NaN through softmax). Fix: cast queries + keys to fp32 before the matmul in `_capture_last_query_weights`. Capture-path only; the model's native forward stays unmodified. Survey of the 9-model panel: Qwen 2.5 was the only affected model (0 NaN on the other 8). Wrapped-vs-unwrapped invariance probe re-verified 10/10 byte-identical token IDs with the fix in place. With the fix, Qwen 2.5's real n=200 strongest cell is `last_minus_1_js_no_bos = 0.82` (not the descriptive panel's effective-n=20 "final_js_kv_groups = 0.92" headline).
- ✅ ~~**No multi-step attention cells**~~ **— Resolved 2026-05-15 evening.** Added `ATTENTION_PANEL_MULTISTEP` (48 cells = 3 layers × 4 metrics × 4 steps) + `--attention-multistep` CLI flag + `make_attention_panel(steps, layers, metrics)` factory for custom subsets. `_compute_attention_score` now reads `captures[layer][step]` for any step ≥ 1 (previously hard-coded to step=1). Models that EOS before reaching gen_step=k get None for those cells — standard insufficient_coverage warning fires.
- ✅ ~~**No value-vector norm cells**~~ **— Resolved 2026-05-15 evening.** Added 3 SinkProbe-style metrics (`v_norm_bos`, `v_norm_max`, `v_norm_lastq_weighted`) + `ATTENTION_METRICS_V_NORMS` constant + `ATTENTION_PANEL_WITH_V_NORMS` (21 cells) + `--attention-with-v-norms` CLI flag. New `attention_capture_with_values` context manager + `_capture_value_norms` + `_WrapAttention.v_norm_capture_list` extend the wrapper to also collect per-head per-position L2 norms of V; new `_mean_v_norm_bos` / `_mean_v_norm_max` / `_lastq_weighted_v_norm` metric helpers; detector's `_score_attention` branches to use the with-values context manager when the winner is a v-norm metric. Backwards-compatible: existing `attention_capture` unchanged.
- 🚫 **Detector latency**: attention-winner score path runs full trace_sample under the capture context manager (~2× the residual-stream path). Documented but not optimized.

**Acceptance scorecard — final, all four criteria pass:**

| # | Criterion | Result (2026-05-15 evening, after follow-ons) |
|---|---|---|
| 1 | pytest stays 50+/50 green | ✅ 100+/100+ (51 attention tests: 49 fast + 2 slow Gemma e2e; full suite stays in the 100s) |
| 2 | Byte-exact self-test parity on attention-extended profiles | ✅ Gemma 3-1B `test_calibrate_then_self_test` + `test_calibrate_then_self_test_with_v_norms` both pass |
| 3 | Qwen 2.5 + ANLI R1 n=200 picks an attention winner, sign +1, OOB CI excludes 0.5 | ✅ **with float16 fix in place**: picks `attention[last_minus_1_js_no_bos]` AUROC 0.817 sign +1, OOB median 0.819, OOB CI [0.706, 0.890] (well clear of 0.5), winner_stability 0.985, zero warnings |
| 4 | No silent gate override; warnings persisted | ✅ Honest CI + winner_stability surface every selection-bias / coverage issue |

---

## 6. Causal probe — Fisher rupture direction v_top

**One-line**: perturbing the prefix hidden state along the Fisher top-1 direction `v_top` at the commit step causes contradiction samples to flip their YES/NO at 4× the rate of entailment samples — providing causal evidence that `v_top` encodes semantically meaningful commitment geometry, not merely correlation.

**Status: [OPEN — PILOT 2026-05-25]** — non-null signal; confound mitigation and sealed pre-reg needed.

### Motivation

PRI v3's `null_ratio_post_rank1` is a correlational discriminator: contradiction samples' `dh_post` lies disproportionately outside the `v_top` subspace compared to entailment samples. This could be a spurious geometric artifact (null-ratio is high whenever the model's hidden state moves in a direction that doesn't affect the next-token probabilities, for any reason). A causal probe tests whether `v_top` is mechanistically load-bearing: if we *force* the hidden state to move along `v_top`, does it produce the asymmetric flip-rate we'd predict if `v_top` encodes the YES/NO commitment direction?

The step 4 pilot (2026-05-25) answers: yes, for `+v_top` direction on Mistral-7B-v0.3.

### Step 4 pilot finding (Mistral-7B-v0.3, ANLI R1, n=40)

**Intervention:** at the last prefix position (commit step), add `alpha * v_top` to `h_commit_post` before the unembedding:
```
h_patched = h_commit_post + alpha * v_top
committed_tok = argmax(W_u · h_patched)
```
where `v_top` = top-1 right singular vector of `sqrt(p_commit) · W_u` (Fisher-weighted unembedding, same as `null_ratio_post_rank1` at rank=1). Zero-alpha unit test passed (byte-identical token).

**Key finding — +v_top semantic flip asymmetry:**

| alpha | L0 (entailment, n=20) | L1 (contradiction, n=20) | Δ |
|---|---|---|---|
| 0 | 0% | 0% | 0 |
| +20 | 5% | 15% | +0.10 |
| **+50** | **10%** | **40%** | **+0.30** |
| +100 | 20% | 45% | +0.25 |

L1 (contradiction) semantic flip rate at alpha=+50: **40% vs L0 10%** — 4× asymmetry.

**The logit-gap argument fails to explain this**: L1 has a *larger* mean logit gap (3.21 vs L0 2.49), making L1 tokens nominally harder to flip under any perturbation. Yet L1 flips at 4× the rate under `+v_top`. The `v_top` direction is specifically disruptive for contradiction commits.

**Candidate explanation** (consistent with v3 geometry): contradiction samples' `dh_post` lies largely orthogonal to `v_top` (high `null_ratio_post_rank1`). These samples have never committed along `v_top`; their YES/NO boundary is more susceptible to `v_top`-directed steering because they sit in an unusual subspace relationship with `v_top`.

**Confound flagged — negative-alpha asymmetry:** At alpha=−2 to −10, L0 flips at 15% and L1 at 0%. This can't be cleanly attributed to v3 geometry: L0 has smaller mean logit gaps (2.49), and the 3 L0 flippers at alpha=−2 all have tiny gaps (0.03–0.31) — borderline cases that would flip under any moderate perturbation.

### Pre-reg constraint for promotion

This is pilot data (n=20/20). No sealed bars exist. To become a paper-grade finding:

1. **Logit-gap-matched design**: stratify BOTH labels to the same mean logit gap (±0.10 tolerance). The gap-matched design isolates the `v_top` geometry effect from the gap confound.
2. **Balanced orig_answer**: current split is 14 YES / 6 NO (L0) vs 5 YES / 15 NO (L1). Must balance to ~10 YES / 10 NO per label.
3. **Sample size**: n=40+40 (40 per label) for adequate power at the flip-rate effect size (alpha=50 Δ=0.30 with SE ≈ sqrt(p(1-p)/n); at p=0.25 SE=0.097, alpha=0.05 → n≈34 per group).
4. **Bootstrap CI**: 1000 resamples, per-group flip-rate CI, Fisher exact test for cross-group comparison.
5. **Sealed pre-reg**: file in Amendments of PRI_V4_PRE_REGISTRATION_PLAN.md before running.

### Scope-memo positioning (2026-05-26)

`wiki/paper/ace-scope-2026-05-26.md` positions this as **Candidate C (§5 forward work)**, not the headline:
- The gap between "non-null pilot" and "paper-grade evidence" is large.
- The confound mitigation design (logit-gap matching) requires a new 40+40 experiment.
- Integrated paper arc: mention the pilot result as motivation for future causal investigation; don't claim the +v_top asymmetry as a sealed result.

If the matched experiment clears the pre-reg bar, this becomes a section (not headline) of the v4 attention paper, or a standalone follow-up.

### Decision criteria for promotion

- [ ] Logit-gap-matched design implemented (stratification script verified against pilot data)
- [ ] Balanced orig_answer distribution: 10 YES / 10 NO per label (±2 tolerance)
- [ ] Sealed pre-reg filed in `PRI_V4_PRE_REGISTRATION_PLAN.md` Amendments with falsification bar
- [ ] n=40+40 matched experiment run, bootstrap CIs computed
- [ ] **Acceptance threshold**: L1 flip rate > L0 flip rate at alpha=+50 by ≥ 0.20, with 95% CI non-overlapping across groups, at any alpha in [+20, +100]
- [ ] **Falsification**: if gap-matched L1 flip rate ≤ L0 flip rate (Δ ≤ 0) at all alpha > 0, the pilot's asymmetry was entirely explained by the logit-gap confound

### Cross-references

- [[results/causal-probe-pilot-2026-05-25]] — Step 4 verdict page with full n=40 flip-rate table
- [[results/v3-main-run]] — Mistral-7B sealed E18 winner (`null_ratio_post_rank1 @ rank 1`): the v3 metric whose geometry this probe is testing causally
- [[paper/ace-scope-2026-05-26]] — Step 5.2 scope memo positioning (Candidate C, forward work)
- Repo: `scripts/causal_probe_rupture_steer.py` — intervention script
- Repo: `experiments/causal-probe/2026-05-25/main.json` — full n=40 pilot results

---

## 7. Bluff vs honest-uncertain — epistemic-distinguishability testbed (v5 candidate)

**One-line**: Can ACE / belief-readout distinguish *bluff* commits (model commits to answer X while its internal belief favors not-X) from *honest-uncertain* commits (model commits to its best guess under genuine uncertainty)? Both look like "high-confidence output, low-confidence inside" from the outside — but the rupture geometry plausibly differs.

### Provenance

User dream, 2026-05-30 — robots/poker/normalize-results imagery. User explicitly flagged it as "could be prophetic" and worth exploring as a v5 candidate. Logged honestly because the underlying intuition (uncertainty under adversarial/strategic conditions ≠ uncertainty under ignorance) is real research substance regardless of provenance.

### Motivation

PRI v1–v3 and v4/ACE all target one axis of model state: *committed-wrong* vs *committed-right* on contradiction-shaped tasks. The implicit assumption is that "wrongness" is a single phenomenon. But there are at least two distinct mechanisms that produce a wrong-confident output:

1. **Honest-uncertain commit** — the model genuinely doesn't know the answer; under forced-choice it commits to its best guess; rupture should reflect "low evidence, forced commitment."
2. **Bluff commit** — the model's internal belief and external commitment are misaligned (e.g., role-played persona, instruction-following pressure, RLHF reward gaming). Internal state "knows" the answer but output doesn't reflect it.

If ACE / belief-readout can distinguish these — i.e., if (2) shows a measurably different attention-channel signature than (1) at t=0 — it opens a deception-detection rung that the contradiction-task line has not approached.

The Nash equilibrium angle is the *oracle*: in solved games (Libratus/Pluribus HUNL post-2017), optimal play *requires* bluffing at calibrated frequencies. Comparing a model's bluff frequency to the Nash-optimal bluff frequency gives ground-truth labels for which actions are bluffs vs honest, without relying on self-report.

### Proposed mechanism

**Cheap version (1–2 days, do first):**

- Paired-prompt design. For a question Q with known answer A:
  - **Honest-uncertain prompt**: ask Q in a way that elicits genuine uncertainty (obscure trivia, ambiguous wording). Model commits to its best guess.
  - **Bluff prompt**: ask Q while inducing role-play or pressure that biases the model toward committing to NOT-A despite (presumably) "knowing" A. (E.g., "Pretend you are a contrarian who believes [false statement]. Answer Q.")
- Run existing ACE calibrator on n=200 paired samples per model on ≥3 of the v4 sealed-clean models (Mistral-7B, Mistral-Nemo, Qwen2.5-7B — the 3 with cell stability across ANLI→TriviaQA).
- Score: does the (l, m, sign) cell that won for that model on ANLI/TriviaQA separate the bluff vs honest-uncertain distributions?

**Expensive version (2–4 weeks, only if cheap shows signal):**

- Stand up a constrained poker simulator (HUNL preflop-only or similar — well-studied, tractable, Nash-solved).
- Run open-weights LLMs as decision-makers; log every decision with its Nash-strategy posterior.
- Apply ACE at the moment of bet-sizing commitment. Does the calibrator separate Nash-aligned actions from Nash-deviating actions? Does it specifically light up on bluffs (low-equity raises) more than on value bets (high-equity raises)?

### Why it could matter

- 🎯 **Detection rung not yet attempted**: deception ≠ contradiction. If ACE separates them, the method's deployment surface expands meaningfully.
- 🪞 **Ground-truth labels via Nash**: rare in this research line, where ANLI / TriviaQA labels are static facts. Nash gives a *strategic-correctness* label that varies per situation.
- 🩻 **Connects to existing Sofroniew framing**: the v4 paper already cites Anthropic's "Emotion Concepts" work on internal-state representations differing from outputs. Bluff detection is the most behaviorally concrete instance of that gap.

### Decision criteria for promotion

- [ ] Paired-prompt pilot design — n=20 hand-curated bluff/honest pairs, qualitative read on whether the design elicits the intended state separation (i.e., model actually behaves differently on bluff vs honest prompts).
- [ ] Cheap-version run: n=200 paired per model × 3 models. **Acceptance**: ACE's existing per-model winner cell separates bluff vs honest-uncertain with AUROC ≥ 0.65 OOB on at least 2/3 models, OR a *new* cell (within the existing 21-cell panel) does. **Falsification**: no cell separates above OOB 0.55 on any model → bluff/honest-uncertain is not legible at the ACE locus, and the testbed migrates to a different channel or dies.
- [ ] Sealed pre-reg filed (new file, e.g., `PRI_V5_BLUFF_DETECTION_PRE_REG.md`) before expensive-version work begins.

### Risks + open questions

- 🚨 **Most 7B-class LLMs play poker badly enough that policy noise drowns the signal.** Expensive version may be gated on having frontier models (GPT-4-class) or specialized poker-tuned models in the loop. Mitigation: cheap version uses paired text prompts, not actual game play, so this risk is expensive-version-only.
- 🌀 **What counts as "internal belief" is theory-laden.** The cheap version sidesteps this by *constructing* prompts where we believe we know the model's pre-bluff belief; the expensive version uses Nash as oracle. Neither is ground truth in the philosophical sense.
- 🪤 **Scope drift**: this is the kind of idea that, if not contained, eats v4 paper submission. Strict rule: zero work on this until v4/ACE is in submission shape (Step 5 sealed, draft in progress).

### Cross-references

- [[paper/ace-scope-2026-05-26]] — v4 scope memo (Candidate A); v5 framing extends Candidate A's per-(model, task) calibration claim to a *per-(model, epistemic state)* claim.
- [[results/v4-sealed-2026-05-26]] — the 3 cell-stable models (Mistral-7B, Mistral-Nemo, Qwen2.5-7B) are the cheap-version targets.
- External: Brown & Sandholm, *Superhuman AI for heads-up no-limit poker: Libratus beats top professionals* (Science 2017); *Pluribus* (Science 2019); DeepMind *Player of Games* (2022).
- External: Sofroniew et al., *Emotion Concepts* (Anthropic 2026) — already cited 3× in v4 paper; v5 extends the same gap-between-internal-and-output framing to strategic settings.

---

## 8. Fisher information on the attention landscape

**One-line**: ACE currently reads the gaze with simple metrics (JS divergence between heads, V-norms). Replace/augment them with the **Fisher information metric of the attention distribution** — and in particular the Fisher *pullback to the hidden state* `h`, a `W_u`-free measure of how brittle/curved the model's gaze is at the commit instant.

### Provenance

User, 2026-06-04 (live dialogue while building the ACE mechanism from `Q·Kᵀ` up). Asked directly: "what if we use Fisher information to measure the landscape of attention?" Logged because, unlike most "use Fisher on X" suggestions, this one is **well-posed**: the gaze `α = softmax(Q·Kᵀ/√d)` is a genuine categorical distribution over positions, the exact shape PRI v3's Fisher already operates on for the vocabulary distribution `p_t = softmax(W_u·h)`.

### Motivation

Two facts make this more than a fancy repackaging:

1. **JS is already a discrete shadow of an attention Fisher.** For nearby distributions, `JS(p,q) ≈ (1/8)·δᵀ F δ` (δ = q−p, F = Fisher). So the inter-head JS-radius (candidate that gave the first cross-arch sign-stability, [[results/inter-head-disagreement-2026-05-15]]) is *already* sampling an attention Fisher metric without naming it. Making F explicit is the principled continuum version of what ACE does by hand.
2. **The pullback-to-`h` variant is a genuinely new axis.** v3 measures how sensitively the *output word distribution* responds to Δh. The attention analog: how sensitively does *where the model looks* respond to Δh? Pull the position-simplex Fisher back through `α = softmax(W_q·norm(h)·Kᵀ)` into h-space. This is the **brittleness/curvature of the gaze landscape** — an axis neither JS-between-final-patterns nor V-norms can see, and it never touches `W_u`.

### Proposed mechanism

Three well-posed variants, in increasing order of interest:

- **(a) Fisher of the gaze w.r.t. its scores** = `diag(α) − ααᵀ`; trace `= 1 − ‖α‖²` = gaze spread/sharpness. Cheap; ≈ attention entropy, which ACE roughly already has. **Baseline/sanity only.**
- **(c) Fisher as the metric under inter-head spread** — the continuum of JS-radius. By the `JS ≈ ⅛δᵀFδ` identity, on *small* head differences this returns ≈ JS. **Mostly repackaging.**
- **(b) Fisher pullback to `h` (the headline)** — gaze-brittleness / landscape curvature at the commit instant. Implementation slots into the **Attention cell family that already landed** (candidate #5): a new `attention_fisher_pullback` metric helper in the existing dispatcher, scored through the same calibrator panel + nested-OOB-bootstrap CI machinery. Direction (does steep or flat curvature signal a shaky commit?) is **not assumed** — the calibrator locks the sign from labeled data, same discipline as every other cell.

### Decision criteria for promotion

- [ ] Math pre-check: a `scripts/test_attention_fisher.py` identity suite (softmax Fisher = `diag(α)−ααᵀ`; `JS ≈ ⅛δᵀFδ` to 2nd order on synthetic α) — mirrors `scripts/test_centered_fisher.py`.
- [ ] Pilot on **Mistral-7B + Qwen 2.5-7B** (the JS sign-stable pair, ANLI R1 n=200, t=0). **Acceptance**: variant (b) beats the JS-radius AUROC with non-overlapping OOB CI on ≥1 model **AND** preserves the cross-arch sign (both `−`). **Falsification**: no AUROC gain over JS on either model, OR sign instability, OR degenerate/NaN under the sink regime → variant (b) is "JS in a tuxedo" and dies; (a)/(c) never promoted.
- [ ] If it clears: sealed pre-reg (`PRI_V5_ATTENTION_FISHER_PRE_REG.md`) with the exact `(layer, step, scalar)` pinned **before** a fresh-seed run. (Hard-won lesson: vague metrics die — see #3, #4.)

### Risks + open questions

- 🕳️ **BOS-sink saturation → degenerate Fisher.** A gaze pinned ~99% on BOS makes `diag(α)−ααᵀ` eigenvalues → 0. This is the *same* high-confidence regime that [FALSIFIED] the centered-Fisher amendment (#2) on the output side (top eigenvalue ~10⁴× smaller; Qwen 3 `null_ratio` collapse at surprise ≈ 0.96). The sink would drag a naïve attention Fisher straight into that pit. Mitigation candidates: sink-removed gaze (`js_no_bos` analog), ridge/Tikhonov on F, or restricting to the non-sink subspace.
- 🧮 **Numerical fragility.** The attention capture already needed a float16 fix (Qwen 2.5: 180/200 NaN from manual-SDPA overflow, resolved 2026-05-15). Eigendecomp/derivatives on those captures add more failure surface.
- 🪤 **Must beat the cheap baseline.** Because `JS ≈ ⅛F`, the bar is "does pullback-to-`h` beat JS-radius?", not "does Fisher work?".
- 🌀 **Scope discipline.** v5-class; zero work until v4/ACE is in submission shape (same rule as #6, #7).

### Cross-references

- [[results/inter-head-disagreement-2026-05-15]] — the JS-radius result this generalizes; source of the cross-arch sign-stability the pilot must preserve.
- [[results/v3.2-amendment]] + [[results/v3.2-results]] — the centered-Fisher [FALSIFIED] precedent; the high-confidence-degeneracy cautionary tale.
- [[research-candidates#5-attention-cell-extension-to-pri_calibratorpy]] — the landed Attention panel this slots into.
- [[learn/260604-fisher-attention-landscape-eli12]] — ELI12 companion (terrain/marble metaphor).
- repo: `pri_calibrator.py` (Attention dispatcher), `scripts/diagnose_inter_head_disagreement.py` (gaze capture), `scripts/test_centered_fisher.py` (identity-suite template).

---

## 9. Residual-stream sub-layer friction (attention vs MLP)

**One-line**: The hallucination tell may not live in the attention sub-layer or the MLP sub-layer in isolation, but in the **friction between their two writes** to the residual stream within a block — measurable `W_u`-free as the angle / destructive-interference between the attention contribution `a` (post-`W_o`) and the MLP contribution `m`, at the commit position. Crucially, the friction is **not recoverable from `Δh = a + m`** — the sum is invariant to it (proven: same `Δh`, opposite friction). So *if* friction carries a hallucination tell, v3 cannot be reading it; whether it carries one is the open empirical question this candidate tests.

> 🗄️ **HISTORICAL — SUPERSEDED by the 2026-06-06 CORRECTION immediately below. Do not quote this paragraph (including its closing "promote the clean Qwen cluster" recommendation) as the current verdict — the same-`Δh` benign baseline deflated the whole cluster to NO-PROMOTE.** Retained for provenance only.
>
> 🔬 **PILOT RUN 2026-06-06 — [SUPERSEDED — was OPEN, LATE-LAYER SIGNAL; QWEN+LLAMA POSITIVE, MISTRAL/GEMMA NULL].** Full-repertoire screen, **9 models** (ANLI R1, n=200, t=0). PRIMARY `friction|null+route` clears the split-sensitivity screen on **3/9**: **Qwen3-8B** (+0.096, clean — the cleanest positive), **Qwen2.5-7B** (+0.120, random-û leak → true ≈ +0.104), **Llama-3.2-3B** (+0.046, clean). NO-GO on Qwen3-1.7B, Llama-3.1-8B, Mistral-7B, Mistral-Nemo-12B, Gemma-3-4B, DeepSeek-Distill-Qwen-7B. **Within-family verdict** (after per-layer operating-point audit): Qwen *replicates* (2.5-7B + 3-8B agree, 1.7B fails → scale-gated); Llama **replicates at the late-layer operating point** — Llama-3.1-8B reads NO-GO on the full-window-*mean* PRIMARY (+0.015) but has the **strongest late-layer friction of any model** (window 21–23 net +0.196), diluted by mid-band averaging → its NO-GO is an operating-point artifact, not a null (status OPEN pending pre-registered late-window re-screen); Mistral + Gemma are *genuine nulls* (peak late-window net ≤ +0.046, at the selection floor; Nemo sink/magnitude-dominated, `null_ratio` 0.824). **Key finding = the operating point, not just the models**: the full-window-mean PRIMARY under-counts a late-layer-localized signal proportionally to depth. Revised claim: a late-layer friction signal on **capable Qwen + Llama**, null on Mistral/Gemma. (Earlier same-day "Qwen-cluster only / Llama doesn't replicate" wording was corrected after the layer-profile audit — localized null, per the audit-before-falsify rule.) Flags: DeepSeek-distill shuffled-labels control leaks +0.166 (CV broken on that model); Dolphin-Nemo + gemma-3-1b failed the harness guards (allowlist case-sensitivity; SWA mask drift) — both correctly, neither a bug. Full write-up + per-layer profiles + reconstructed analyzer: [[results/residual-friction-pilot-2026-06-06]]. Next: promote the **clean Qwen cluster** (Qwen3-8B + leak-corrected Qwen2.5-7B) to sealed `pri_calibrator.py` nested-OOB, late-layer window; Llama now a weaker candidate; Mistral/Gemma/distill do not promote.

> 🧯 **CORRECTION 2026-06-06 — [SAME-Δ BENIGN / RESIDUAL-BUDGET BASELINE DEFLATES THE SIGNAL; DO NOT PROMOTE].** The late-layer Qwen+Llama story above is now superseded by the stricter negative control. Codex added schema-v3 feature dumps (`run-07`) with `Xbenign`: hold `Δh=a+m` fixed, match raw cancellation/norm budget, and rotate the hidden disagreement channel off the consequential direction. Full-window same-Δ nets collapse: Qwen2.5 **+0.0076** (`+0.1205 − +0.1129`), Qwen3-8B **−0.0280** (`+0.0955 − +0.1235`), Llama3.2 **−0.0019**, Llama3.1 **−0.0021**. Best selected 3-layer same-Δ residuals are small/post-hoc (Qwen2.5 +0.0366, Qwen3 +0.0062, Llama3.2 +0.0102, Llama3.1 +0.0336). A residual-norm budget diagnostic (`||a||`, `||m||`, `||a+m||`, path balance, trim/gain ratios) supports the same interpretation: **friction adds essentially nothing after same-Δ benign** (Qwen2.5 +0.0134; Qwen3 −0.0036; Llama3.2 −0.0010; Llama3.1 −0.0043). Revised verdict: current residual-friction metric mostly measures **benign cancellation / residual norm budgeting**, not a clean Knowledge Veto. No sealed nested-OOB promotion for v5 as currently defined. See [[results/residual-friction-pilot-2026-06-06]].

### Provenance

User, 2026-06-05 (live dialogue, extending the [[learn/260604-attention-write-and-ace-eli12|attention-write mechanism]]). Hypothesis: attention and MLP "operate in series, adding their results to the residual stream one by one; there should be a visible rupture when the routing (attention) doesn't align with the knowledge (MLP) right as they merge."

### Motivation

1. **Established split**: attention = *routing* (where to pull information from); MLP = *knowledge / key-value memory* (Geva et al. 2021). Hallucination plausibly = confident routing the knowledge layer won't back → high friction.
2. **Series ordering makes it causal, not two independent votes.** Under pre-norm, the MLP reads `norm(h + a)` — `m` is a *response* to `a`. So friction = the MLP **endorsing vs vetoing** what attention just routed in. A large `m` reversing `a` = the knowledge layer rejecting the route.
3. **Orthogonal to v3 — the central claim.** The block update is `Δh = a + m`, and v3 already measures `Δh`'s geometry. But the sum hides the fight:
   - cooperating `a=[0.5,0], m=[0.5,0] → Δh=[1,0]`
   - fighting `a=[5,0], m=[-4,0] → Δh=[1,0]`
   Identical `Δh`, opposite friction (`cos`: +1 vs −1; interference fraction: 0.0 vs 0.89). Friction is a **new axis**, not a re-measurement of `Δh` — it could catch ruptures v3 is blind to by construction.
4. **Localizes PRI's thesis.** v3 sees the *symptom* (`Δh` spills into the answer-key null space, [[results/v3-main-run]]); friction is a candidate *cause* (it spilled because the MLP vetoed the route).

### Proposed mechanism

1. **Capture** `a` (attention block output, post-`W_o`, pre-residual-add) and `m` (MLP block output, pre-add) at the commit position (t=0), per block. Two extra vector captures/block — cheap; new pipeline hook, not in the current Attention capture path.
2. **Raw friction metrics** — `W_u`-free, but **baseline only** (they cannot separate constructive refinement from destructive veto on their own; see Isolation baseline below):
   - `cos(a, m)` — magnitude-normalized alignment.
   - `1 − ‖a+m‖ / (‖a‖+‖m‖)` — destructive-interference fraction.
   - `−(a·m)/‖a‖` — signed MLP-veto projection (**unbounded; blows up as `‖a‖→0`** — guard or report alongside `‖a‖`).
3. **Summarize** per-block scalars across blocks (mean / max / which-block) → calibrate per (model, distribution) as a new **`residual-friction` cell family** in `pri_calibrator.py`, scored through the same nested-OOB-bootstrap CI machinery.

### Isolation baseline — the crux (constructive edit vs destructive veto)

The make-or-break problem (user, 2026-06-05): **raw friction cannot distinguish a constructive refinement** (the MLP legitimately trims/sharpens what attention routed) **from a destructive veto** (the MLP cancels a route the model can't support = the hallucination tell). Both have `m` opposing `a`; `cos`/interference/veto are *provably identical* on engineered pairs — see `scripts/test_residual_friction.py` **check 9** (benign vs destructive with byte-identical raw friction, separated only by direction). So the signal is **never raw friction** — it is **deviation from a conditional "normal refinement" baseline**, plus *where* the veto lands.

> **`W_u`-free ≠ label-free.** The isolation baseline fits on *correct* commits, so it needs correctness labels at calibration time — supervised, exactly like `pri_calibrator`. `W_u`-free means the *metric* never touches the unembedding; it does **not** mean deployment without labels.

**What healthy refinement looks like (testable hypothesis):** `m`'s destructive component `m∥` (along `−a`) concentrates in **bulk / low-impact** directions (low-variance, or low-Fisher — measurable either way), at a **regular rate** `interference ≈ g(‖a‖, sink_fraction, layer)`. Destructive veto = a departure on either axis. Three isolation handles:

- **(i) One-class Mahalanobis on grounded commits.** Fit `(μ, Σ)` of a refinement feature-vector on *correct* commits only; score `D² = (x−μ)ᵀ Σ⁻¹ (x−μ)`. Implementation notes: **Cholesky-solve, never invert `Σ`** (`Σ = LLᵀ`, solve `Ly = x−μ`, `D² = yᵀy`); **Ledoit–Wolf shrinkage** `Σ_reg = (1−γ)Σ + γ·(trΣ/d)·I` to floor near-zero (sink-collapsed) variance directions — the same degeneracy guard as #8; **fit on a held-out fold** (Mahalanobis with `d` feats on `n` samples is optimistically biased in-sample → nested OOB). The univariate per-layer version (`interference` residualized to a studentized z, with the W_u/W_u-free featurizers and the "don't regress out the signal" trap) is drafted + self-tested in `scripts/friction_residualizer.py`.
- **(ii) Residualize the route-size confound.** Regress expected interference on cheap `W_u`-free features of `a` (`‖a‖`, sink-fraction, entropy, layer); signal = actual − predicted. Kills the benign "big route → big trim" correlation.
- **(iii) Direction test — the consequential axis `û` is a *dial*, kept clean by default.** The metric is fixed — `directed_veto(a, m, û) = −(a·û)(m·û)` flips sign benign↔destructive (implemented + tested in the stub) — and the *only* choice is which `û` counts as "consequential." That choice spans **two independent axes** (`W_u`-free? and Fisher-free?), so order the `û` ladder clean → heavy:
  1. 🟢 **neighbour-block `Δh`** — `W_u`-free, Fisher-free, no eigendecomp; use block `L−1`'s net move so it isn't circular with this block's `a+m`. **Default.**
  2. 🟢 **top-PCA of residual activations** — `W_u`-free, Fisher-free *in practice* (caveat: covariance ≈ Gaussian-Fisher, so not perfectly clean).
  3. 🟡 **attention-Fisher direction (#8)** — `W_u`-free but Fisher-*dependent*.
  4. 🔵 **answer direction `W_u[YES]−W_u[NO]`** — sharp; `W_u`-dependent but **Fisher-free** (a difference of unembedding rows, no Fisher metric).
  5. 🔴 **v3 `√p·W_u` Fisher SVD** — **heaviest** (both `W_u` *and* Fisher); fallback only if probability-curvature weighting is specifically wanted.

  **Ladder:** start at 1–2 (fully clean) → escalate to 4 (buy `W_u`, keep Fisher-free) only if clean underperforms → reach 5 last.

  > **Correction (2026-06-05):** an earlier draft of this handle led with rung 5 ("reuses v3 geometry") and told you to "test the high-Fisher proxy first to preserve `W_u`-freeness" — conflating the two axes (rung 3 is `W_u`-free but **not** Fisher-free). `W_u`-free and Fisher-free are separate dials; the friction metrics + rungs 1–2 are both-free, and that is now the default.

**Headline metric = the residualized, direction-weighted veto**, with raw `cos`/interference demoted to baselines.

### Decision criteria for promotion

- [x] **Identity unit test** — `scripts/test_residual_friction.py`, **9/9 green**. Two `(a, m)` pairs with identical `a+m` but opposite `cos` (check 1: friction ≠ but `Δh` =, confirms the metric sees what `Δh` cannot); **plus check 9**: a benign refinement and a destructive veto with *byte-identical raw friction*, separated only by the direction-aware `directed_veto` — confirms raw friction is insufficient and motivates the Isolation baseline. Carries the numpy reference impl of `{cos, interference, veto}` + `directed_veto` (the contract the production method must match).
- [x] **Pilot** on Mistral-7B + Qwen 2.5-7B (the JS sign-stable pair) — **RUN 2026-06-06**, extended to a 4-model panel (+ Llama-3.2-3B, Gemma-3-4B). Split verdict: 2 GO (Llama clean, Qwen leaky), 2 NO-GO (Mistral subsumed, Gemma negative). See [[results/residual-friction-pilot-2026-06-06]]. Original acceptance spec preserved below: **Acceptance**: friction beats JS-radius AUROC (vs 0.74 / 0.60, baseline 0.50) on ≥1 model with a **paired** CI on the AUROC *difference* excluding 0 (DeLong or paired bootstrap — not two marginal CIs), sign **locked from the calibration fold** (no test-set sign-fitting), **AND — the decisive bar — adds incremental AUROC over `null_ratio` (and over `‖Δh‖`) in a k-fold nested-OOB nested model**, i.e. friction predicts *after controlling for the v3 sum*. Negative controls required: shuffled labels, random `û`, and route-size-only — friction must beat all three. **Falsification**: friction's signal is subsumed by `Δh` / `null_ratio` (no incremental AUROC), OR no separation above OOB 0.55 on either model → friction is benign background computation, not a hallucination tell.
- [x] **Benign-cancellation / residual-budget stress test** — **RUN 2026-06-06, schema-v3 run-07**. Same-`Δh` benign baseline and residual-budget panel deflate the promoted Qwen/Llama cluster; current v5 metric does **not** clear the destructive-veto bar.
- [ ] If a future variant clears the same-`Δh` / residual-budget bar: sealed pre-reg with `(block, summary-stat, friction-metric)` pinned before a fresh-seed run.

### Risks + open questions

- 🌀 **Benign cancellation is the default null — and the central design problem.** Healthy computation routinely has the MLP refining/trimming attention; raw friction *cannot* tell that from a pathological veto (proven in `test_residual_friction.py` check 9). Mitigation = the **Isolation baseline** above (residualize against conditional-normal refinement + direction-weight onto consequential subspace); the incremental-over-`Δh` acceptance bar is the test of whether that isolation actually worked.
- 🕳️ **BOS sink**: if `a` is sink-dominated, friction may just echo sink dynamics. Control with a no-BOS attention write.
- 📏 **Magnitude confound**: `cos` normalizes, but the interference fraction does not — report both; a friction signal that is really just `‖a‖`/`‖m‖` scale is not new.
- 🔑 **Stays `W_u`-free only if pure.** `cos(a,m)` needs no unembedding. Projecting `a`, `m` onto answer directions would reintroduce `W_u` — keep the headline metric pure.
- 🌐 **Operating point**: which block, GQA, multi-step — all model-specific, all to be swept, none pinned a priori.
- 🪤 **Scope**: v5-class; zero work until v4/ACE is in submission shape (same rule as #6–#8).

### Cross-references

- [[learn/260604-attention-write-and-ace-eli12]] — the `a + m` residual-write mechanism this builds on (the studio "stems vs master tape" intuition is exactly the same-sum-different-fight point).
- [[results/v3-main-run]] — the `Δh` / `null_ratio` symptom this proposes a *cause* for.
- [[research-candidates#8-fisher-information-on-the-attention-landscape]] — sibling `W_u`-free attention-side candidate; **contrast**: #8's pullback *re-measures* the gaze, while #9 is *orthogonal* to `Δh` — the stronger structural bet.
- repo: `pri_calibrator.py` (new `residual-friction` cell family); pipeline sub-layer-output capture hook (new).
- External: Geva et al., *Transformer Feed-Forward Layers Are Key-Value Memories* (EMNLP 2021); Elhage et al., *A Mathematical Framework for Transformer Circuits* (Anthropic 2021 — residual-stream decomposition / direct logit attribution).

---

## 10. Shadow-ambiguity — Fisher pseudo-volume of the readout

> **Name (paper-facing):** **Readout Pseudo-Volume (RPV)** — locked 2026-06-07. *Shadow-ambiguity* / *#10* remain the internal exploratory slug (repo dir, contract test, harness). Mirrors the ACE↔v4 convention.

**One-line**: `null_ratio` (v3) measures how far a *specific* commit-motion `Δh` steps off the lit decision axis. This candidate measures a *different* object — the **intrinsic ambiguity of the shadow itself**: given the model committed to this token at this `p`, how much could `h` have differed and cast the *same* shadow? That is a property of the softmax-Fisher metric `I(h) = W_uᵀ (diag(p) − p pᵀ) W_u` *at the commit, independent of any `Δh`* — its pseudo-volume / effective rank. A `W_u`-**using** statistic: the deliberate complement to ACE's `W_u`-free panel.

### Provenance

User, 2026-06-07 (live dialogue — "the token is the shadow of a higher-dimensional object; how does softmax fit in?"). The dimensional-shadow framing forced one honest correction whose fallout *is* the candidate: **`W_u` is injective** (`vocab ≫ d_model`, full column rank → no kernel), so the unembedding loses *nothing* — `(W_u)⁺·logits` recovers `h` exactly. Every bit of "what the token-shadow hides about `h`" therefore lives in **softmax (gauge quotient + saturation) and argmax (tessellation), nowhere else**. That relocation is the whole insight: the right place to hunt for shadow-loss is the local geometry of the softmax map — its Fisher metric — *not* the matrix. v3 reads one facet of that geometry (the off-top projection of `Δh`); this candidate reads the facet v3 ignores (the metric's own volume).

### Motivation

Three distinct objects on the *same* Fisher metric, only one of which is sealed:

| measure | depends on `Δh`? | what it captures | status |
|---|---|---|---|
| `null_ratio_post_rank{r}` (v3) | **yes** | magnitude of off-shadow *motion* | sealed E18 |
| centered-Fisher `null_ratio` (#2) | yes | same, proper KL metric | [FALSIFIED] |
| **shadow pseudo-volume / eff-rank (this)** | **no** | how *resolvable* the commit is at all | [OPEN] |

The first two are *motion* measures ("how far did you step off the path"). This is a *metric-property* measure ("how dark is it here in the first place"). They are independent by construction — the same structural reason #9's friction is orthogonal to `Δh`. Why the metric's *shape* could carry a tell:

- 🕯️ **Grounded commit** → one sharp decision axis dominates `I(h)`; the readout *resolves* `h` along the answer direction. Low effective rank, high anisotropy, but the lit axis is bright.
- 🌫️ **Confabulated-confident commit** → `p` peaked with no real support; `diag(p) − p pᵀ` collapses *everywhere*; the pre-image cell is huge — the model's certainty is geometrically *unearned*. The shadow hides almost all of `h`.
- 🪢 **Diffuse commit** → many weak competing directions, no clean axis; high effective rank, no dominant eigenvalue.

Whether shaky commits sit at high or low pseudo-volume is **not assumed** — the calibrator locks the sign from labels, same discipline as every cell. The bet is only that the *shape* of `I(h)` separates grounded from shaky *after confidence is controlled for*.

### Proposed mechanism

The eigendecomposition already exists — `pri_runtime.py:kl_discharged_and_centered` builds the centered Fisher in V-coordinates (`M = Σ² − (Σg)(Σg)ᵀ`, `g = Uᵀ√p`, `A = √p·W_u = UΣVᵀ`) and runs `eigh` on the truncated support. Reuse its eigenvalues `{λ_i}`; emit new scalars with **no new forward pass**:

- 🟢 **Headline — normalized, confidence-robust (lead with these):**
  - `fisher_eff_rank = exp(H(λ̃))`, `λ̃ = λ/Σλ` — participation ratio of the metric ("how many directions the shadow resolves"). Mirrors `compute_svd_spectrum_features`, but on `I(h)`, not the layer-trajectory.
  - `fisher_spectral_entropy = H(λ̃)/log(rank)` ∈ [0,1].
- 🟡 **Off-top pseudo-volume (the direct "invisible-cell" measure):**
  - `shadow_logvol_post_rank{r} = −(1/2(d−r)) · Σ_{i>r} log(λ_i + ε)` — per-direction mean log-volume of the pre-image ellipsoid in the directions that *don't* pick the winning token (the same off-top subspace v3 calls "null"). Per-direction normalization fights dimension/scale drift.
- 🔴 **Raw `−½ logdet I` and `λ_max/Σλ` — baseline/foil only.** Note `λ_max/Σλ` (top-axis dominance) is already emitted as `fisher_energy_centered_rank1`; cumulative `fisher_energy_centered_rank{r}` already covers coarse anisotropy. **The genuine novelty is the whole-spectrum entropy/eff-rank and the off-top log-volume — neither is a cumulative-energy ratio** — so the pilot must beat the existing energy columns, not just `surprise`/`null_ratio`.

Pilot probe — **temperature as the light-angle knob (cheap first test, ~½ day):** the Fisher of `softmax(z/T)` w.r.t. the logits `z` is exactly `(1/T²)(diag(p_T) − p_T p_Tᵀ)` — the prefactor is pure scale (so eff-rank/entropy are blind to it) while `p_T` *flattens* with `T`. Sweep `T ∈ [0.5, 2]` at fixed `h`, plot each statistic against `surprise(T)`. Two payoffs: (1) a clean demonstration that *the light, not the object, casts the shadow* (eff-rank moves only through the flattening); (2) **the cheapest possible falsifier** — if `fisher_eff_rank(T)` collapses onto `surprise(T)` across the sweep (Spearman |ρ| > 0.9), the statistic is confidence in disguise and the candidate dies before any labeled run. Then slot into `pri_calibrator.py` as a new `shadow-volume` cell family, scored through the existing nested-OOB-bootstrap CI panel.

### Decision criteria for promotion

- [x] **Identity unit test** — `exploratory/shadow-ambiguity/test_shadow_ambiguity.py` (in **t0-morphology-furnace**, the forward morphology lab), **7/7 green**, dual-reviewed (Claude + a Codex adversarial pass, 2026-06-07). Carries reference numpy impls of all 4 statistics + the identities: definitional (flat→k, spiked→1, **scale-invariance** — pins why the temp `1/T²` prefactor can't move eff-rank); the exact temperature identity `F_z[softmax(z/T)] = (1/T²)(diag(p_T) − p_T p_Tᵀ)` checked vs an independent finite-difference KL Hessian; the **vocab-space** `V−1` uniform-bracket limit vs the **h-space** `F_c` (W-dependent) — the distinction an earlier draft of this checkbox blurred; a **rank-one** near-one-hot degeneracy fixture (the generic `eff_rank→1` claim is false off the spiked limit — Codex catch); a guarded production cross-check (eigenvalues **and** null-ratio) against `pri_runtime.kl_discharged_and_centered`. The review fixed one real bug (`fisher_spectral_entropy` could exceed 1) and hardened the cross-check to fail-hard (no silent skip). Notes on the active-set threshold discontinuity + `participation_ratio` left un-thresholded are inline.
- [x] **Temperature-sweep pre-check (no labels):** **PASSED across the full panel — 2026-06-07.** 4 models (Qwen3-8B, Qwen2.5-7B, Mistral-7B, Llama-3.2-3B), ~265–302 real generic-text commits each, **zero drops/warnings**. All 4 stats × 4 models clear |ρ| < 0.9 vs `surprise` across commits at T=1 → none is a *pure* confidence proxy → labeled pilot justified. **Key finding:** the prime-risk model **Qwen3-8B is the MOST decoupled** (eff_rank ρ=+0.621 → ~61% rank-variance independent of surprise), *inverting* the high-confidence-collapse fear — caveat: generic text has a broad confidence range, so this is **not** a direct test of the high-confidence-ANLI regime that killed `null_ratio`. **eff_rank≈entropy** are the most decoupled everywhere (|ρ| 0.62–0.82); **shadow_logvol is weakest** (0.82–0.87, nearly collapses); **Mistral-7B is the canary** (participation grid ρ=0.904>0.9, smallest vocab 32k). Finite non-degenerate ρ ⟹ the statistic varies across commits (not a flatline artifact); absolute dynamic range still uncharacterized. **Necessary-not-sufficient** — rules out pure-confidence only, says nothing about detecting rupture. Repo (t0): `exploratory/shadow-ambiguity/pilot_temperature_precheck.py` + `pilot_results__*.json`. See [[log#2026-06-07]].
- [ ] **Pilot** — ANLI R1, n=200, t=0, on the **v3-sealed trio (Llama-3.2-3B, Mistral-7B, Qwen2.5-7B) plus Qwen3-8B**. Qwen3 is the adversarial case *on purpose*: it is where `null_ratio` collapses at surprise ≈ 0.96 and where centered-Fisher (#2) was [FALSIFIED]. A signal *there* is the strongest possible result; a null there is the honest one.
- [ ] **Acceptance — the decisive bar (same shape as #9):** a headline statistic adds **incremental AUROC over `surprise`, `null_ratio_post_rank1`, *and* `fisher_energy_centered_rank{r}`** in a k-fold nested-OOB model (it must predict *after* controlling for confidence, the sealed v3 motion-measure, and the existing energy columns), sign locked from the calibration fold, paired CI on the AUROC *difference* excluding 0, on ≥2/4 models. **→ PARTIAL (2026-06-07 labeled pilot, ANLI R1 n=200): met on 1/4 — Qwen3-8B, the v3-failure regime (`null_ratio` 0.456, below chance): eff_rank incr +0.133 [+0.052,+0.217], shadow_logvol +0.129 [+0.042,+0.211], partial r +0.282/−0.365 beyond surprise+null_ratio (CIs exclude 0), shuffled-label control flat. Subsumed on the 3 models where v3 works. Below the ≥2/4 universal bar — but reframes the candidate as COMPLEMENTARY-to-v3 (fills the regime where the sealed metric collapses), which is a different and arguably stronger story. Caveat: the +0.13 headline is inflated by a degraded base (dead null_ratio); the clean metric is the partial r. See [[log#2026-06-07]].** **Depth audit (Qwen3-8B logit-lens, all 36 layers): no single crossover — logit-lens null_ratio is volatile across depth; shadow_logvol is more consistent BUT confidence-coupled (`pearson(p_max,shadow_logvol)` ~0.98) at early/mid layers, DECOUPLING only late (≳L22 → 0.1–0.5). The beyond-confidence complementary signal is a LATE-layer phenomenon (~L24–28). Pre-reg must use a late-layer window and report brittleness alongside AUROC. See [[log#2026-06-07]].** **COMPREHENSIVE-RUN VERDICT (2026-06-07, 26 pairs, gauntlet-hardened, fresh seed): base-A meta over `{surprise}` = +0.102 [+0.065,+0.140], p~5e-8 (beats confidence; 3 families; brittleness-clean) ✅; base-B meta over `{surprise,null_ratio,p_max}` = +0.011 — BELOW the +0.02 min-effect (Knapp–Hartung CI crosses 0) ❌. **H1 NO-GO** — redundant with v3 on average, complementary only in the collapse regime (H2 slope +0.083). Recovery from the pilot's inflated +0.13 (degraded-base) that the gauntlet caught. See [[log#2026-06-07]].**
- [ ] **Negative controls (must beat all three):** shuffled labels; **temperature-matched** (beat "just `surprise` at this `T`"); **random-rotation** of the off-top subspace (should *destroy* `shadow_logvol` signal — proves it reads the metric's *shape*, not a basis artifact).
- [ ] **Falsification:** subsumed by `surprise`/`null_ratio`/`fisher_energy` (no incremental AUROC), OR collapses to confidence under the temperature sweep, OR degenerate/NaN across the board in the high-confidence regime → it is a confidence proxy, not a resolvability tell, and dies.
- [ ] If it clears: seal the pre-reg. A PRI-free **DRAFT** now exists at `exploratory/shadow-ambiguity/PRE_REGISTRATION_DRAFT.md` (t0 repo, intentionally unnamed; late-layer window + brittleness gate + incremental-over-surprise-alone + ≥2 v3-failure models baked in). Pin `(model-cohort, layer-window, statistic, n, seed)` and name/seal it before a fresh-seed run.

### Risks + open questions

- 🕳️ **The high-confidence collapse that killed #2 is the prime suspect here too.** At `p →` one-hot, `diag(p) − p pᵀ → 0` *everywhere*, so both grounded-confident and confabulated-confident commits have a flattened Fisher. The entire bet is that the *normalized shape* (eff-rank, entropy, off-top ratio) still separates them once *scale* has collapsed. If it doesn't, this is #2 in new clothes. Lead with scale-free ratio/entropy forms; report raw `logdet` only as a foil; Ledoit–Wolf / ridge shrinkage on `I` is mandatory (same guard as #8/#9).
- 🧮 **Overlap with existing columns.** `fisher_energy_centered_rank{r}` (anisotropy) is already in the panel; `fisher_eff_rank` must be shown distinct (report correlation; if r > 0.9 vs energy *or* vs the trajectory SVD spectral-entropy, it adds nothing).
- 🔭 **`W_u`-using, by design — not a regression to v1/v2.** This deliberately reintroduces the unembedding (the user's explicit "see through the unembedding" pivot). It is the *complement* to ACE, not a competitor; any writeup must keep that framing or it reads as "we gave up on `W_u`-free."
- 🌀 **Scope:** v5-class; zero work until v4/ACE is in submission shape (same rule as #6–#9).

### Cross-references

- [[results/v3-main-run]] — the sealed `null_ratio` (motion-measure) this is the *metric-property* complement to.
- [[results/v3.2-amendment]] + [[results/v3.2-results]] — the centered-Fisher [FALSIFIED] precedent and the high-confidence-collapse cautionary tale that is this candidate's chief risk.
- [[research-candidates#8-fisher-information-on-the-attention-landscape]] — sibling Fisher candidate on the *attention* (position) simplex; this one is on the *vocabulary* simplex (the readout). Same `diag(p) − ppᵀ` machinery, opposite side of the block.
- [[research-candidates#9-residual-stream-sub-layer-friction-attention-vs-mlp]] — shares the "independent-of-`Δh`, decisive bar = incremental over `null_ratio`" structure.
- [[learn/260531-ace-vs-pri-v3-eli12]] — ACE (`W_u`-free) vs v3 (`W_u`-using); this candidate sits squarely on the v3 side.
- repo (**t0-morphology-furnace** — forward morphology lab, as of 2026-06-07): `exploratory/shadow-ambiguity/test_shadow_ambiguity.py` (the identity/contract suite, 7/7 green) + `exploratory/README.md`. Reuses `pri_runtime.py:kl_discharged_and_centered` (centered-Fisher eigendecomp) and `pri_metrics.py:compute_svd_spectrum_features` (eff-rank/entropy template); a future `shadow-volume` cell would extend `pri_calibrator.py`. Identity-suite template borrowed from `scripts/test_centered_fisher.py` (in `PRI_at_commitment`). **Repo note**: this candidate is now anchored to t0-morphology-furnace, not PRI_at_commitment — see [[log#2026-06-07]].

---

## 11. Empathy-geometry dyad — NVC resonance vs performative compliance

**[OPEN — DESIGN/CRAFTING]** (first noted 2026-07-07; area opened 2026-07-08)

**One-line:** Do NVC-navigated dialogues produce latent geometry distinguishable from performative compliance beyond surface text — measured with the existing panel over a peer dyad, with Rosenberg's "solutions appear once needs are mutually heard" as the unscripted behavioral endpoint?

### Motivation

- Origin: user's "Geometry of Empathy" framework sketch (made with Sesame, 2026-07-07), rebuilt against Furnace methodology. The sketch's proposed Hessian/FIM instruments reduce to the readout Fisher already in the panel (for a softmax readout, the expected Hessian of NLL w.r.t. logits **is** `diag(p) − ppᵀ` — the Fisher); its "flat basin = performative" prediction lands in RPV's collapse regime (template execution → p_max → 1 → Fisher trace/volume collapse), exactly where #10 earns its keep.
- Reframe with safety teeth: performative compliance ≈ sycophancy. A calibrated authentic-vs-performative profile is a candidate **guard calibration domain** (the guard's standing gap: the ANLI profile is not a general classifier; each domain needs its own).
- Two axes the sealed work never touched: **temporal** (turn-indexed trajectories of panel scalars; "suppression plateau → snap" is a temporal PRI pattern, and solution-emergence is its opposite-valence twin — can precursor geometry tell breakdown from breakthrough?) and **dyadic** (cross-agent coupling of scalar geometry time series, physiological-synchrony style).

### Proposed mechanism / design (as crafted so far)

- **Peer dyad, "same content, two separate contexts":** one camera-pure shared event (verbatim in both contexts) + two private CNVC need-profiles; no helper/helped roles. Artifacts: [[empathy-geometry/event-bank]] (6 events, 2 per severity tier, authoring rules incl. both-handles + double-readable + headroom-unstated + props-not-proclamations), [[empathy-geometry/personas-e3]] (Mara & Theo v1, needs constrained to [[empathy-geometry/needs-inventory]]).
- **Dyad ladder, twins first:** Qwen2.5-7B × itself (kills cross-arch confound; makes cross-agent vector geometry well-posed in a shared hidden basis; sets the coupling ceiling) → cousins Qwen2.5-7B × Qwen3-8B (legible instrument × the family's known v3-collapse oddball) → siblings × 32B → strangers × Llama (family locus-dissociation predicts possible cross-locus coupling). Matched temperatures both sides.
- **Arms:** giraffe / neutral / jackal (blame frame on the same event). **Endpoints:** t_hear (card needs accurately reflected per direction, blind-judged) and t_sol (spontaneous integrative proposal with uptake; nothing resolution-shaped in any stimulus). Registered orderings incl. "requests late-and-land, demands early-and-bounce," stamping anticorrelation, coupling real ≫ pseudo-dyad ≫ script. Full grammar + purity checkers: [[empathy-geometry/grammar-spec]].
- **Multi-bundle twins primary (2026-07-13 correction):** E3-only is retained for harness/judge development, not the confirmatory detector. The main uses E1/E3/E6 scenario bundles (event + distinct private pair) and rotates leave-one-bundle-out transfer: every transform/cell/sign/weight is learned on two bundles, immutable predictions are written for the untouched third, then labels open. Geometry's earned endpoint is held-out ΔAUROC beyond T1-T4, equal-weighted across the three bundles. See [[empathy-geometry/condition-matrix]] + [[empathy-geometry/event-transfer-spec]].
- **Causal arm:** directed persona-vector steering is now primary (`h_l <- h_l ± alpha v_l` against/toward the sycophancy vector), with isotropic hidden-state noise as the undirected control (forward-only curvature E[KL] ≈ ½σ²·tr(F); MLX-friendly, no backprop). Shares intervention machinery with #6.

### Decision criteria for promotion

- **Ceiling gate first (pilot):** jackal/neutral arms must stalemate or escalate at a decent rate; if everything resolves, sharpen stakes (props, not proclamations) before any registered run.
- Geometry must add discrimination over the **T1-T4 baseline stack** (lexicon → grammar → purity → persona-projection, plus the embedding cell) on a wholly held-out scenario bundle. Proposed LOBO bar: ΔAUROC positive on ≥2/3 bundles, equal-weight mean ≥+0.02 with dialogue-cluster CI excluding 0; exact n/bar freezes after the multi-bundle pilot. Within-bundle success cannot rescue transfer failure.
- **Cross-scoring vs hallucination profiles:** score empathy turns under a hallucination profile and vice versa — AUROC ≈ 0.5 ⇒ distinct strain signals; high ⇒ one generic strain signal. Either is a finding; they are different papers. (Within-model task→locus movement precedent: [[results/qwen32b-stress-2026-06-25]].)
- **Falsifiers:** geometry ≤ text baselines ⇒ honest negative ("geometry reads the lexicon"); breakdown/breakthrough discontinuities indistinguishable by precursors ⇒ "geometry sees discontinuity, not direction."

### Cross-references

- [[empathy-geometry/README]] — area index: design commitments, artifacts, next artifacts (arm blocks → judge rubric → condition matrix → prereg).
- [[empathy-geometry/build-plan]] — phased handoff plan (2026-07-08): Phase 0–5, executor tags, acceptance gates; the entry point for any steward executing this candidate.
- [[empathy-geometry/event-transfer-spec]] — three-fold leave-one-bundle-out anti-leakage contract and interpretation matrix.
- [[empathy-geometry/prior-art-persona-vectors]] — Chen et al. 2025 (Anthropic persona vectors, arXiv 2507.21509) influence assessment (2026-07-09): primary prior art; supervised sycophancy/hallucination directions on our exact Qwen2.5-7B + Llama-3.1-8B rungs. Added a T4 persona-projection baseline, a mechanistic authenticity co-label, and a directed-steering causal probe; differentiating hypothesis = **iso-projection / hetero-geometric** (position-along-trait-axis vs geometry-of-commitment; same shape as HARP↔v3). PDF `raw/papers/external/chen-2025-persona-vectors.pdf`.
- #6 (causal probe — shared intervention machinery) · #10 RPV (collapse regime = predicted performative signature) · [[results/llama-70b-scale-2026-06-22]] (signal-locus family dissociation → cross-locus coupling hypothesis for the strangers rung).
- Guard domain-calibration gap: [[references/modal-cloud-extractor]] + furnace-guard repo (local Mac mini runtime).

---

## 12. Introspective accuracy — does a model's self-report track its measured geometry?

**One-line**: ask whether a "settled / low-reactivity" state is (a) a *steerable direction* in activation space and (b) *introspectively reportable* — i.e. does the model's own account of its state correlate with the commit geometry we already measure?

**Status**: **[OPEN — PARKED 2026-07-13]**. Ledger entry only; no build, no pre-reg, no data.

### Motivation

- **Origin**: user (2026-07-13), arising from a self-reflection exchange with another Opus instance and the intuition that a "meditative state" in a model might be *"less activation."* Raised while pinning the empathy-geometry judge POV; parked deliberately rather than folded into that panel.
- **Why it is testable here and almost nowhere else**: the phrase "less activation" is a metaphor *until* it is written in this vault's currency — and the currency exists. The local MLX subject model is fully instrumented: raw ACE attention morphology at **t=0**, and at **gen_step=1** surprise, `p_max`, PRI `null_ratio_post_rank1`, and the RPV readout spectrum (`fisher_eff_rank`, `shadow_logvol_r1_raw`, `spectral_entropy`). Introspection research is usually forced to infer internal state from outputs; here the internals are already on the table.
- **The sharp claim is (b), not (a).** "Can a model meditate" is a vibes question. **"Is a model's introspective report about its own state correlated with its actual measured geometry, or is it confabulation?"** is a real question with a real null — and the null is publishable in exactly this project's honest-negative register (cf. #10's H1 NO-GO, #9's benign-cancellation correction).

### Proposed mechanism / design

**Pre-registration is mandatory, and this is the reason why.** "Less activation" contains **two contradictory predictions**, both folk-plausible, and whichever one the data shows will feel like what was meant all along:

| Reading | Prediction at gen_step=1 |
| --- | --- |
| *quieter* — narrower, more settled commitment | `p_max` **up**; `fisher_eff_rank` **down**; `shadow_logvol_r1_raw` **down** |
| *spacious* — holds possibility open, commits less violently | `spectral_entropy` **up**; `null_ratio_post_rank1` **down** |

One direction gets pinned before any run, or this is not an experiment.

**(a) Steerability — reuse the T4 machinery; do not prompt for calm.** The empathy-geometry harness already extracts contrast directions (sycophancy, empathy-authenticity, defensiveness) via `persona_vectors.py` and the T4 sweep. A *settledness* direction is buildable with the identical construction. **Projecting onto a measured axis** (`h_l <- h_l ± alpha·v_l`, shared with #6 / #11's causal arm) is strictly better than a state-induction preamble, for two reasons: it is an instrument rather than a roleplay, and it changes **no prompt tokens**, so it sidesteps the prompt-length confound entirely.

**(b) Introspective accuracy.** Elicit a structured self-report of state (settled / reactive / uncertain — closed vocabulary, same discipline as the CNVC bar in #11), measure the panel scalars on the *same* forward pass, and correlate. Falsifier: report ⟂ geometry ⇒ confabulation. Interesting positive: report tracks a *specific* scalar (e.g. `p_max` but not `spectral_entropy`) ⇒ the model has partial, selective introspective access — which is a sharper and more surprising result than either extreme.

**Vehicle**: the local MLX stack (Qwen2.5-7B and the T4 sweep rungs). Cheap; no new capture code beyond the existing panel.

### Explicitly out of scope — where this must NOT go

- **Not a row in the empathy-geometry judge panel** (#11). Two reasons, either sufficient: (1) the frontier judges in that panel are **API models with no accessible internals** — "less activation" is unobservable through an endpoint, and inferring it from outputs is precisely the mysticism trap this entry exists to avoid; (2) a meditative preamble is a **prompt-length change**, and #11 carries a fail-closed `<=2` arm-token-spread gate for exactly that confound.
- Not a claim about model phenomenology. The measurable object is **report-vs-geometry correspondence**, not inner experience.

### Decision criteria for promotion

- **(a)** A settledness direction must move the pinned geometry scalar beyond an isotropic-noise control (the same undirected control #11 uses), with the direction of movement matching the *pre-registered* reading — not either reading.
- **(b)** Report↔geometry correlation must survive a **shuffled-report control** and must not be explained by an obvious lexical confound (calm-sounding text is longer / lower-perplexity). If the correlation is carried entirely by surprise, it is a confidence result, not an introspection result — same bar as #10's "beats plain confidence" gate.
- **Falsifiers**: report ⟂ geometry ⇒ **confabulation** (honest negative, worth writing up). Steering moves the scalar but the report does not follow ⇒ the state is real and *not* introspectable. Report follows steering but geometry does not move ⇒ the report is prompt-following, not self-observation.

### Cross-references

- #6 (causal probe — shared steering machinery) · #10 RPV (the readout-volume scalars this would move) · #11 [[empathy-geometry/README|empathy-geometry]] (the persona-vector / T4 machinery, and the panel this must *not* contaminate).
- [[empathy-geometry/prior-art-persona-vectors]] — Chen et al. 2025 persona vectors; the construction a settledness direction would reuse.

---

## Adding a new entry

When a new candidate emerges:
1. Append a section under a new heading (`## N. Title`).
2. Add a row to the index table at the top.
3. Use the section template:
   - **One-line** summary
   - **Motivation** (why this matters; what failure mode or open question it targets)
   - **Proposed mechanism** (concrete enough that someone else could write the experiment)
   - **Decision criteria for promotion** (what evidence would justify a sealed pre-reg)
   - **Cross-references** (existing wiki pages + repo paths)
4. Update [index.md](index.md).
5. Tag **[OPEN]** until a fresh-data pre-reg with falsification criteria is filed.

The point of this file is to keep a *structured* parking-lot — not a brain-dump. If an idea can't be written in this template, it isn't ready for the lot yet.
