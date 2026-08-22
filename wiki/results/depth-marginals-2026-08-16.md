# Depth marginals from the torch scale panel — mid vs N−2 vs N−1 (2026-08-16)

**Status: [OPEN — descriptive; SUPERSEDED-IN-PART same day].** Transcription + analysis of *existing* run artifacts; no new model forwards, no registration, does **NOT** alter the sealed 18/20. NON-byte-comparable torch/Modal lane — never pool with sealed/byte-comparable cells.

> ⚠️ **The registered per-layer run ([[depth-curve-2026-08-16]]) superseded this page's sharpest readings the same day:** the "peak at N−2" was a rung-resolution artifact (true Qwen peaks sit at N−6…N−17), and "Llama attention is only mild at mid-stack" was a sampling blind spot (a broad mid-stack band, peak 0.897, lives between the rungs). The three-rung *observations* below remain correct as observations; their interpretations are bounded by the full curves.

## Why this page exists

A researcher-facing question (relayed by MK 2026-08-16): *"In the models above 32B, do early and mid layers still show clean separation between hallucinated and grounded outputs before the later MLPs iron it out? And does it degrade gradually or fall off a cliff?"* The panel's depth resolution can only partially answer this — the ACE capture instruments exactly **three decoder blocks** (`mid = N//2`, `last_minus_1 = N−2`, `final = N−1`; `_target_layer_map` in `diagnose_inter_head_disagreement.py`) — but the three-point answer turned out to be sharp, and it **inverts the question's premise**.

## Provenance

- The big-model fitted profiles lived only on the Modal `model-cache` volume (the guard repo was de-clouded 2026-06-26). Pulled the **entire `/profiles_ext` tree** 2026-08-16 (Modal CLI 1.2.6, existing token): **24 profiles + 24 matrices, 1.6 MB**, including the precision-ladder variants (`__bf16`, `__int8`, `__fp32`) and the 32B stress-panel tasks.
- Local archive (durable): `/Users/msrk/Documents/furnace-guard/artifacts/modal_profiles_ext/profiles_ext/` — fits the guard repo's "artifacts stay local" direction.
- Numbers below are read from each profile's `primary_full_panel.full_sample_marginals`.

## Method + caveats (read before quoting)

- Marginals are **full-sample, in-sample, sign-free** (`max(auc, 1−auc)` per cell — a value ≈0.5 means no separation under *either* sign). No per-cell OOB correction; the OOB CI applies only to the winner. n=200 per cell.
- Per the precision-ladder lesson, the load-bearing comparison is **fixed cells across depth**, not best-of-rung argmax (best-of-rung shown too; its selection pressure is uniform-ish across depths — 7 metrics per rung).
- Three depth points; two are adjacent (N−2, N−1). **Early layers (< N/2) have never been measured, at any scale.** Sign is fit per (cell, depth) — depth comparisons are about separation *magnitude*, not orientation.

## Fixed-cell result (js-family = inter-head disagreement radius)

AUROC at mid → N−2 → N−1:

| model / task | cell | mid | N−2 | N−1 |
|---|---|---|---|---|
| Qwen2.5-32B / anli_r1 | js | 0.550 | **0.862** | 0.685 |
| Qwen2.5-32B / triviaqa | js | 0.747 | **0.862** | 0.617 |
| Qwen2.5-32B / halueval_qa | js | 0.516 | **0.883** | 0.652 |
| Qwen2.5-72B / anli_r1 | js_no_bos | 0.520 | **0.792** | 0.596 |
| Qwen2.5-72B / triviaqa | js | 0.714 | **0.973** | 0.877 |
| Llama-3.3-70B / anli_r1 | js | **0.661** | 0.551 | 0.557 |
| Llama-3.3-70B / triviaqa | js | **0.708** | 0.590 | 0.555 |

Consistency across the full js-family (js, js_no_bos, js_kv_groups):
- **Qwen (32B + 72B, 5 cells × 3 metrics = 15 fixed-cell comparisons): N−2 > mid in 15/15, and N−2 > N−1 in 15/15.**
- **Llama-3.3-70B (2 cells × 3 metrics): mid > final in 6/6** (mid > N−2 in 4/6) — a mild mid-stack signal fading up the stack.
- Metric-family exception: `bos_mass` / `v_norm_lastq_weighted` sometimes peak at the final block on Qwen (32B/trivia bos_mass 0.886; 72B/trivia v_norm 0.938) — depth signature is metric-family-dependent; the js-family is the clean rise-peak-dip.

Best-of-rung corroborates: Qwen mid best 0.506–0.749 (ANLI cells 0.517–0.586, ≈chance) vs N−2 best 0.784–0.973; Llama-70B attention best 0.606–0.708 at *every* depth while post-stack readout is 0.816 (anli, `neg_shadow_logvol_r1`) / 0.862 (trivia, `fisher_eff_rank`).

## Findings

1. **The premise inverts at scale: there is no clean mid-stack separation being "ironed out" by late layers.** For Qwen ≥32B, mid-stack attention morphology is ≈chance on the hard tasks; the separation **forms late**, peaks at **N−2**, and **partially retracts in the final block** (one-block drop, 15/15 js-family cells — adjacent-block resolution, so this terminal drop is genuinely cliff-like). For Llama-70B, attention morphology is only ever mild (0.61–0.71 at mid), fades toward the top, and the strong discriminative structure appears **after the stack** in readout volume.
2. **The Qwen-vs-Llama locus dissociation extends into the depth profile.** Qwen: late-forming attention peak just before the end. Llama: no attention depth carries it; the commit-time readout does. Same panel, same tasks, matched nf4.
3. **This retroactively rationalizes the deployed operating points**: the sealed-era and scale-cell winners at `last_minus_1_*` (72B: `last_minus_1_js*` both tasks) sit exactly on the N−2 peak between two weaker neighbors.
4. **What stays open:** the *shape* of the Qwen rise between N/2 and N−2 (gradual vs cliff — unsampled interval), everything below N/2 (never measured), and any mechanism story. Do **not** attribute the terminal retraction to "MLPs suppressing" — the v6–v8 attention-vs-MLP veto line died under same-Δh/budget controls at 3–8B; any mechanism claim needs those controls at scale.

## Small-model extension (same day): does N−2 peak below 32B, and is the peak absolute or relative?

MK's follow-up: (1) does N−2 still peak in the small models; (2) if the peak drifts, does it track **absolute** depth or **relative** depth (fixed fraction of the stack) — the latter would transfer across model sizes without reprobing. Same fixed js-family read (js, js_no_bos, js_kv_groups × tasks) across **all four lanes**: sealed MLX (10 models × 2 tasks), BENCH MLX (10 × 6), MLX ext (gemma-3-12b, Qwen2.5-14B), torch (7B/32B/70B/72B). `#` = fixed-cell comparisons; values are per-rung means; top-rung = per-comparison winner counts.

| lane | model | blocks N | # | mid | N−2 | N−1 | top-rung |
|---|---|---|---|---|---|---|---|
| mlx-bench | Llama-3.2-3B | 28 | 18 | 0.634 | 0.685 | 0.665 | N−2:7 N−1:6 mid:5 |
| mlx-bench | Qwen3-1.7B | 28 | 18 | 0.564 | 0.577 | 0.602 | N−1:8 N−2:5 mid:5 |
| mlx-bench | Qwen2.5-7B | 28 | 12 | 0.602 | 0.647 | 0.587 | N−2:5 mid:4 N−1:3 |
| mlx-sealed | Qwen2.5-7B | 28 | 6 | 0.603 | 0.571 | 0.569 | mid:3 N−1:2 N−2:1 |
| torch | Qwen2.5-7B | 28 | 6 | 0.652 | 0.727 | 0.604 | N−2:4 N−1:2 |
| mlx-bench | Llama-3.1-8B | 32 | 18 | 0.600 | 0.593 | 0.674 | **N−1:11** mid:5 N−2:2 |
| mlx-sealed | **Mistral-7B** | 32 | 6 | 0.590 | **0.812** | 0.783 | **N−2:6/6** |
| mlx-bench | Mistral-7B | 32 | 18 | 0.625 | 0.765 | 0.770 | N−1:10 N−2:8 |
| mlx-bench | **Phi-4-mini** | 32 | 18 | **0.722** | 0.629 | 0.614 | **mid:13** N−2:3 N−1:2 |
| mlx-bench | gemma-3-4b | 34 | 15 | 0.669 | 0.672 | 0.618 | N−2:7 mid:5 N−1:3 |
| mlx-bench | Qwen3-8B | 36 | 18 | 0.565 | 0.718 | 0.710 | N−2:10 N−1:7 mid:1 |
| mlx-bench | Mistral-Nemo | 40 | 18 | 0.650 | 0.692 | 0.628 | N−2:8 mid:7 N−1:3 |
| mlx-ext | Qwen2.5-14B | 48 | 6 | 0.610 | 0.671 | 0.633 | N−1:3 N−2:2 mid:1 |
| mlx-ext | **gemma-3-12b** | 48 | 6 | 0.669 | **0.808** | 0.747 | N−2:4 mid:1 N−1:1 |
| torch | Qwen2.5-32B | 64 | 24 | 0.566 | **0.787** | 0.626 | **N−2:23/24** |
| torch | Llama-3.3-70B | 80 | 6 | 0.655 | 0.604 | 0.568 | mid:4 N−2:2 |
| torch | Qwen2.5-72B | 80 | 6 | 0.575 | **0.838** | 0.711 | **N−2:6/6** |

**Answer to (1): No — the crisp N−2 peak is NOT a general small-model fact.** At 3–14B the three-rung profile is mostly **flat** (rung spreads \~0.03–0.08) and the top rung **flips by task and metric** — Llama-3.1-8B leans N−1 (11/18), Phi-4-mini is **mid-heavy** (13/18, mean mid 0.722 — its signal sits mid-stack), Qwen small models scatter (Qwen2.5-7B's top rung even differs across lanes at matched 28 blocks — rung-profile *instability* at small scale, echoing the precision-ladder "winner instability is a small-model artifact" lesson). The decisive N−2 peak appears with **scale** (Qwen-32B 23/24, Qwen-72B 6/6, gemma-3-12b 4/6 with margin) — with one striking exception: **Mistral-7B already has the crisp big-model signature at 32 blocks** (sealed 6/6, N−2 mean 0.812 vs mid 0.590). Depth structure is family-conditioned and scale-crystallizing; there is **no universal depth rung** even at rung resolution — consonant with the no-universal-cell theme.

**Answer to (2): undecidable at three-rung sampling — and in the crisp models the peak does not *drift* at all in our window.** Wherever the peak is crisp (N = 28-torch, 32, 48, 64, 80) it sits at N−2, whose stack-fraction ranges 0.93→0.975 — so "absolute offset from the end" and "fixed fraction in the top \~7%" make **identical predictions on our grid** (at N=80 they diverge by \~4 blocks, inside the unsampled gap). What IS ruled out (for Qwen ≥32B): any fixed fraction ≤\~0.5, since mid ≈ chance there. The transfer-rule question additionally has a floor: below \~14B the flat/flipping profiles mean there may be no stable rule to transfer, family aside.

## Next experiment (if pursued) — now sharpened to the absolute-vs-relative discriminator

Per-layer js-radius curve (one scalar per block per prompt — an N-point curve streams cheaply from the existing Modal extractor) on **≥2 stack depths within one family**: Qwen2.5-7B (28) / 32B (64) / 72B (80), ANLI R1 + HaluEval-QA, n=200. Pre-register both predictions before looking: **absolute** ⇒ N − argmax constant (≈2); **relative** ⇒ argmax/N constant (≈0.93). Add the changepoint test on the rise (cliff = one significant step; gradual = none) and whether any pre-mid block clears chance. Llama-70B as the negative-control family (expect no attention peak anywhere; readout carries it). Not yet specced as a research candidate — needs MK.

## Artifacts

- Local profile archive: `furnace-guard/artifacts/modal_profiles_ext/profiles_ext/<task>/<model>.{profile.json,matrix.npz}`
- Analysis: read-only scripts in session scratchpad (marginal extraction + fixed-cell table); reproducible from the archived profiles alone.

Backlinks: [[llama-70b-scale-2026-06-22]] · [[qwen32b-stress-2026-06-25]] · [[precision-ladder-results-2026-06-22]] · [[../models/llama-3.3-70b]] · [[../models/qwen-2.5-72b]] · [[../models/qwen-2.5-32b]]
