# Instrument co-location — do the ACE attention cells read one signal? (2026-08-29)

**Status: [OPEN — descriptive; NOT a registered endpoint].** Session analysis of *existing*
depth-curve artifacts. No model forwards, no Modal spend, no pre-registration, no new data.
Does **not** alter any sealed claim, any registered grid-A/grid-B verdict, or any panel number.
Torch/Modal nf4 lane, NON-byte-comparable; grids A and B scored separately and **never pooled**.

## The question

The ACE attention family combines three instruments — inter-head Jensen–Shannon disagreement
(`js_no_bos`), attention-sink mass (`bos_mass`), and V-norm-weighted attention
(`v_norm_lastq_weighted`). The standing interpretation (relayed to an external interp
researcher 2026-08-26) is that these may be *coarse measurements of one shared change in
attention allocation*. That is a **factor-structure claim**, and it had never been tested.

The depth-curve lane supplies an unused test. If the three are one quantity read three ways,
their per-layer separation curves should share a shape and a peak. If they are distinct
signals, the curves should diverge.

## What was already in the artifacts

The grid-A and grid-B `.depth.npz` files record **four** metrics per block, not one:
`final_js`, `final_js_no_bos`, `final_js_kv_groups`, **`final_bos_mass`**. The registered runs
scored only the js family. **`bos_mass` has therefore had full per-layer coverage all along and
was never analysed.** `v_norm_lastq_weighted` was never captured per-layer at all — the third
instrument remains unmeasured at depth.

Usable cells: **17 of 20** (grid A 8/8; grid B 9/12 — gemma-3-27b ×2 absent via the
`js_no_bos` BOS-sink domain boundary, Mistral-Small-3.2/anli absent via the behavioral gate).

## Method

Read-only script `commit-confluence/exploratory/depth-curve/colocation_analysis.py` →
`COLOCATION.json`. Per block, sign-free AUROC (`max(a, 1−a)`), matching the registered
convention. Paired 1000-resample row bootstrap (same resampled rows for both instruments)
gives a 90% CI on the **peak-location gap**; 200-permutation shuffled-label envelope per block;
Pearson correlation of the two depth curves; and the **cross-evaluation** — each instrument's
AUROC *at the other's peak block*. Seed 20260829.

## Results

| grid | task | model | N | js\* | jsAUC | bos\* | bosAUC | gap [CI90] | js@bos\* | bos@js\* | r |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A | anli | Llama-3.3-70B | 80 | 48 | 0.897 | 70 | **0.915** | −22 [−22, 21] | 0.879 | 0.908 | 0.800 |
| A | anli | Qwen2.5-32B | 64 | 56 | 0.866 | 55 | 0.868 | 1 [−6, 8] | 0.621 | 0.556 | 0.430 |
| A | anli | Qwen2.5-72B | 80 | 66 | 0.838 | 77 | **0.904** | −11 [−11, 8] | 0.794 | 0.888 | 0.604 |
| A | anli | Qwen2.5-7B | 28 | 22 | 0.834 | 22 | 0.738 | 0 [−1, 4] | 0.834 | 0.738 | 0.777 |
| A | halueval | Llama-3.3-70B | 80 | 26 | 0.862 | 26 | **0.910** | 0 [−23, 22] | 0.862 | 0.910 | 0.742 |
| A | halueval | Qwen2.5-32B | 64 | 56 | 0.911 | 62 | 0.849 | −6 [−27, 7] | 0.883 | 0.637 | 0.329 |
| A | halueval | **Qwen2.5-72B** | 80 | 63 | 0.896 | 70 | 0.853 | −7 [−7, 13] | **0.536** | **0.524** | **0.116** |
| A | halueval | Qwen2.5-7B | 28 | 26 | 0.871 | 22 | 0.737 | 4 **[4, 9]** | 0.755 | 0.585 | 0.217 |
| B | anli | Llama-3.1-70B | 80 | 45 | 0.902 | 61 | **0.915** | −16 [−16, 31] | 0.564 | 0.910 | 0.334 |
| B | anli | Llama-3.1-8B | 32 | 18 | 0.744 | 30 | **0.751** | −12 [−16, 1] | 0.636 | 0.615 | 0.408 |
| B | anli | Mistral-Medium-3.5 | 88 | 83 | 0.867 | 70 | **0.880** | 13 [−33, 38] | 0.550 | 0.552 | 0.218 |
| B | anli | gemma-3-12b | 48 | 39 | 0.793 | 46 | **0.841** | −7 [−24, 12] | 0.780 | 0.548 | 0.460 |
| B | halueval | Llama-3.1-70B | 80 | 38 | 0.898 | 26 | **0.904** | 12 [−16, 19] | 0.648 | 0.602 | 0.110 |
| B | halueval | **Llama-3.1-8B** | 32 | 1 | 0.891 | 29 | 0.886 | −28 [−28, 1] | **0.560** | **0.567** | **0.016** |
| B | halueval | Mistral-Medium-3.5 | 88 | 85 | 0.848 | 87 | **0.891** | −2 [−29, 46] | 0.693 | 0.697 | 0.127 |
| B | halueval | Mistral-Small-3.2 | 40 | 37 | 0.879 | 33 | **0.905** | 4 [−15, 5] | 0.677 | 0.867 | 0.240 |
| B | halueval | gemma-3-12b | 48 | 22 | 0.900 | 43 | 0.886 | −21 **[−27, −21]** | 0.573 | 0.780 | 0.027 |

## Findings

1. **The peak-location test is inconclusive — as it should be.** The gap CI excludes zero in
   only **2/17** cells (Qwen2.5-7B/halueval +4 [4, 9]; gemma-3-12b/halueval −21 [−27, −21]).
   Bootstrap bands on argmax are wide, exactly as grid A's own E1 found for js alone.
   **Do not claim "different loci" from argmax.**
2. **The curve-*shape* test is where the divergence lives, and it is task-structured.**
   Pearson r between the two depth curves: grid A median **0.517** (range 0.116–0.800), grid B
   median **0.218** (range 0.016–0.460), below 0.35 in 7/9 grid-B cells. Split by task across
   both grids: ANLI R1 median **0.445**, HaluEval-QA median **0.127**. On HaluEval the two
   instruments trace nearly unrelated profiles down the stack.
3. **Mutual blindness in 6/17 cells; at least one-way in 11/17.** Taking the registered
   qualifying bar (AUROC ≥ 0.65), **both** instruments fall below it at the other's peak in
   Qwen2.5-32B/anli, Qwen2.5-72B/halueval, Llama-3.1-8B/anli, Mistral-Medium/anli,
   Llama-3.1-70B/halueval, and Llama-3.1-8B/halueval. A further 5 cells are blind one way.
4. **🎯 The load-bearing cell — Qwen2.5-72B / HaluEval-QA.** `js_no_bos` peaks **0.896 at
   block 63** with a *pinned* bootstrap CI of [63, 63] (matching the registered grid-A run);
   at block 70 it reads **0.536**. `bos_mass` peaks **0.853 at block 70**; at block 63 it reads
   **0.524**. Curve correlation **0.116**. Each instrument is at chance precisely where the
   other is strongest, and the js peak location is not argmax jitter.
   Llama-3.1-8B/halueval is a second exemplar (0.891 @ 1 vs 0.886 @ 29; cross-evals 0.560 /
   0.567; r = **0.016**).
5. **`bos_mass` matches or beats the registered primary in 11/17 cells** (grid A 4/8, grid B
   7/9) — including every Llama cell in both grids. It is not a secondary instrument.
6. **This strengthens the P3 blind-spot finding.** On Llama-3.3-70B/anli, `bos_mass` reaches
   **0.915** — higher than the js band's 0.897 and well above the panel readout winner 0.816.
   The mid-stack attention signal the three-rung panel missed is larger than the registered
   metric alone showed.

## What this does NOT show

- **Not** a peak-location dissociation (finding 1). The claim is about curve shape and
  cross-evaluation, not argmax separation.
- **Nothing** about `v_norm_lastq_weighted`, which has no per-layer data. The three-instrument
  question is still one instrument short.
- **No** mechanism claim. The v6–v8 same-Δh/budget lesson stands; nothing here is causal.
- **No** change to any sealed claim, registered verdict, or panel number. The ACE panel's
  operating points and AUROCs are untouched; this bounds *interpretation* only.

## Forward hypothesis (untested, for the record)

`[HYPOTHESIS]` **The fixed ACE aggregate may transfer partly through depth coverage rather
than mechanism sharing.** If instruments have different depth signatures and families place
their peak at different fractions (grid B: Mistral 0.88 / Qwen 0.85 late, Llama 0.41 mid,
Gemma 0.64 between), then a panel of several instruments at fixed rungs nets whichever depth a
given model commits at — without any shared latent. **Discriminating test:** a per-model
*depth-targeted single* instrument, aimed at that model's own peak block, should then beat the
fixed aggregate. Not run. → candidate #16.

## Caveats (read before quoting)

In-sample, sign-free (max-side) AUROC; per-block argmax is selection-heavy (envelope and
bootstrap mitigate, do not eliminate); n=200 per cell; bootstrap uses ordinal ranks (ties not
averaged — immaterial for continuous scores); no OOB correction; **not a registered endpoint
and not pre-registered** — this is post-hoc analysis of banked artifacts, and cannot upgrade or
downgrade E1/E5/E6. Grids A and B are separate denominators. Both are torch/Modal nf4,
NON-byte-comparable with the sealed MLX panels.

## Artifacts

`commit-confluence/exploratory/depth-curve/`: `colocation_analysis.py` (read-only),
`COLOCATION.json`. Inputs are the existing `npz/depth_curve/` and `npz/depth_grid_b/` trees —
unmodified.

Backlinks: [[depth-curve-2026-08-16]] · [[depth-grid-2026-08-17]] · [[depth-rescore-2026-08-17]] ·
[[depth-marginals-2026-08-16]] · [[../paper/dc-scaffold]] · [[../research-candidates]] §16 ·
[[../models/qwen-2.5-72b]] · [[../models/llama-3.1-8b]] · [[../models/llama-3.3-70b]] ·
[[../models/gemma-3-12b]]
