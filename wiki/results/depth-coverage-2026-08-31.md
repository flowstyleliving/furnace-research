# Depth coverage — does aiming one instrument beat pinning several? (2026-08-31)

**Status: [OPEN — descriptive; NOT a registered endpoint].** Session analysis of *existing*
depth-curve artifacts. No model forwards, no Modal spend, no pre-registration, no new data.
Does **not** alter any sealed claim, any registered grid-A or grid-B verdict (E1, E5, E6), or
any panel number. Torch/Modal nf4 lane, NON-byte-comparable with the sealed MLX panels; grids A
and B scored separately and **never pooled**.

Companion page: [[results/instrument-redundancy-2026-08-30]]. Both are step 2 and step 3 of
candidate #16 ([[research-candidates]]); step 1 — per-layer `v_norm_lastq_weighted` — is still
uncaptured, so **every number here is two-instrument**.

## The question

[[results/instrument-colocation-2026-08-29]] opened a rival explanation of the ACE headline.
The standing reading is that the fixed attention aggregate transfers because its instruments
share a latent. The rival is **depth coverage**: families place their peaks at different stack
fractions, so several instruments pinned at three rungs act as a coarse net over the stack, and
"no single cell wins everywhere but the aggregate transfers" follows **with no shared latent at
all**.

That rival has a discriminator. If the aggregate is buying depth coverage, then aiming **one**
instrument at a model's **own** peak block should match or beat it.

## Method

Read-only script `commit-confluence/exploratory/depth-curve/depth_coverage.py` →
`DEPTH_COVERAGE.json`. Seed 20260831, 1000 bootstrap resamples, 100 shuffled-label controls.

Rung mapping is the empirically verified one (`DC_DATA_CONTRACT.md` line 120): 0-indexed
`mid = N//2`, `last_minus_1 = N−2`, `final = N−1`. Values at those indices reproduce the sealed
ACE panel's attention marginals to 4 dp.

**Cross-fitting** follows the grid-A rescore convention (`rescore_grid_a.py`): a stratified
5-fold map frozen from the real labels and shared across models within a task. Per fold, the
instrument, the block, and the orientation are fit on the **4 training folds only** and the arm
is scored on the held-out fold. Cell value is the mean of 5 held-out AUROCs.

**Arms.** `fixed6` = 2 instruments × 3 panel rungs, rank-mean fused. `rung_best1` = best single
of those six columns, training-chosen — **the headline opponent**. `target1` = best single
(instrument, block) over all blocks, training-chosen. `target2` = js and bos each at their own
peak block, fused.

> **Naming discipline.** The fused arms are *house-style fold-local rank fusions*, **not** the
> deployed ACE arm. `fixed6` is constructed here; nothing establishes it as an arm the ACE panel
> deploys. `rung_best1` is "best of the six constructed fixed columns", **not** the production
> calibrator's selection. Neither may be called production-mirroring.

**Intervals.** The primary is an **evaluation-row-only interval, conditional on the entire
frozen cross-fit**: selected columns, fitted orientations, fitted calibrations, and the fold map
are all held at their real-fit values, and only held-out rows resample within (fold × label)
strata. It contains no argmax, so the percentile bootstrap is regular. **It charges nothing for
column selection, orientation fitting, fold assignment, or training-sample variation.** A
full-algorithm interval that reruns the selector is emitted alongside in both percentile and
basic conventions, with a per-contrast disagreement flag — see [Audit trail](#audit-trail).

Usable cells: **17 of 20**, the same set as the co-location read (grid A 8/8; grid B 9/12 —
gemma-3-27b ×2 absent via the `js_no_bos` BOS-sink domain boundary, Mistral-Small-3.2/anli
absent via the behavioral gate).

## Results — per cell

Fold-mean held-out AUROC per arm; `sel` is the modal per-fold pick and how often it recurred;
delta is `target1 − rung_best1` with its conditional CI90. **Bold** delta = interval excludes 0.

| grid | task | model | N | fixed6 | rung_best1 | target1 | target2 | sel | Δ (target1−rung_best1) [CI90] |
|---|---|---|---|---|---|---|---|---|---|
| A | anli | Llama-3.3-70B | 80 | 0.883 | 0.707 | 0.898 | 0.884 | bos@70 4/5 | **+0.1915** [0.122, 0.264] |
| A | anli | Qwen2.5-32B | 64 | 0.878 | 0.840 | 0.801 | 0.853 | bos@55 2/5 | −0.0380 [−0.087, 0.009] |
| A | anli | Qwen2.5-72B | 80 | 0.727 | 0.795 | 0.892 | 0.892 | bos@77 4/5 | **+0.0965** [0.054, 0.146] |
| A | anli | Qwen2.5-7B | 28 | 0.630 | 0.676 | 0.819 | 0.799 | js@22 4/5 | **+0.1425** [0.077, 0.211] |
| A | halueval | Llama-3.3-70B | 80 | 0.774 | 0.710 | 0.908 | 0.893 | bos@26 5/5 | **+0.1980** [0.139, 0.258] |
| A | halueval | Qwen2.5-32B | 64 | 0.812 | 0.877 | 0.909 | 0.874 | js@56 5/5 | **+0.0320** [0.008, 0.061] |
| A | halueval | Qwen2.5-72B | 80 | 0.668 | 0.709 | 0.891 | 0.897 | js@63 5/5 | **+0.1820** [0.115, 0.252] |
| A | halueval | Qwen2.5-7B | 28 | 0.744 | 0.872 | 0.872 | 0.875 | js@26 5/5 | +0.0000 [0.000, 0.000] |
| B | anli | Llama-3.1-70B | 80 | 0.769 | 0.866 | 0.894 | 0.913 | bos@45 2/5 | +0.0285 [−0.005, 0.065] |
| B | anli | **Llama-3.1-8B** | 32 | 0.721 | 0.764 | 0.689 | 0.754 | js@18 2/5 | **−0.0750** [−0.124, −0.026] |
| B | anli | Mistral-Medium-3.5 | 88 | 0.887 | 0.858 | 0.864 | 0.913 | bos@70 4/5 | +0.0060 [−0.048, 0.058] |
| B | anli | gemma-3-12b | 48 | 0.810 | 0.848 | 0.833 | 0.812 | bos@46 3/5 | −0.0150 [−0.041, 0.009] |
| B | halueval | Llama-3.1-70B | 80 | 0.702 | 0.695 | 0.890 | 0.962 | bos@26 4/5 | **+0.1950** [0.128, 0.260] |
| B | halueval | Llama-3.1-8B | 32 | 0.842 | 0.851 | 0.862 | 0.949 | bos@29 3/5 | +0.0110 [−0.039, 0.066] |
| B | halueval | Mistral-Medium-3.5 | 88 | 0.829 | 0.886 | 0.877 | 0.911 | bos@87 3/5 | −0.0090 [−0.039, 0.024] |
| B | halueval | Mistral-Small-3.2 | 40 | 0.795 | 0.842 | 0.906 | 0.903 | bos@33 5/5 | **+0.0650** [0.020, 0.114] |
| B | halueval | gemma-3-12b | 48 | 0.786 | 0.782 | 0.841 | 0.934 | js@22 3/5 | **+0.0585** [0.003, 0.112] |

## Results — per contrast

| contrast | grid A wins | median | CI excl 0 | grid B wins | median | CI excl 0 |
|---|---|---|---|---|---|---|
| **target1 − rung_best1** (primary) | 6/8 | **+0.1195** | 6/8 | 6/9 | **+0.0110** | 4/9 |
| target1 − fixed6 | 7/8 | +0.1310 | 7/8 | 7/9 | +0.0490 | 4/9 |
| **fixed6 − rung_best1** | 3/8 | **−0.0435** | 5/8 | 3/9 | **−0.0383** | 4/9 |
| target2 − fixed6 | 7/8 | +0.1252 | 6/8 | 9/9 | +0.1070 | 6/9 |
| target2 − target1 | 3/8 | −0.0071 | 2/8 | 7/9 | +0.0500 | 5/9 |
| **target2 − rung_best1** | 7/8 | +0.1098 | 5/8 | 7/9 | **+0.0560** | **7/9** |
| target1_js − fixed3_js | 8/8 | +0.1084 | 6/8 | 8/9 | +0.0647 | 6/9 |

Shuffled-label control, median across cells: **0.4995** (grid A) / **0.4958** (grid B).
Individual permutation draws range 0.326–0.680, so the control constrains the median, not any
single cell.

## What this says

**1. Depth-targeting beats the fixed aggregate, on both grids.** 7/8 and 7/9. The clean version
of the discriminator points at depth coverage.

**2. Against the harder opponent it splits, and the split is the finding.** Against the *best
single fixed rung*, targeting wins 6/8 in grid A with median **+0.1195** and 6/8 intervals
excluding zero — but only 6/9 in grid B with median **+0.0110** and 4/9 intervals excluding zero
**in both directions**. Llama-3.1-8B/anli is a significant **loss** at −0.075 [−0.124, −0.026].
Grid B is **heterogeneous, not null**. On the models the instrument was developed against the
aggregate was buying depth coverage; on held-out models that does not survive as a general rule.

**3. The aggregate is not even the best fixed thing.** Fusing six fixed-rung columns *loses* to
the best single fixed-rung column: median −0.0435 (A) and −0.0383 (B), first-arm wins 3/8 and
3/9. This undercuts the "aggregate buys complementarity" reading **without appealing to depth at
all**, and it is the most stable result in the run — it held identically across all three
scorings.

**4. The firmest positive is the two-instrument targeted pair on held-out models.**
`target2 − rung_best1` in grid B: 7/9 wins, median +0.0560, **7/9 intervals excluding zero, 0/9
convention disagreements** — the only contrast in either grid with no convention disagreement.

**5. One zero is definitional, not a tie.** Qwen2.5-7B/halueval peaks at block 26, and with 28
layers the `N−2` rung *is* block 26. Both arms are the same column. Its exact 0.0000 [0, 0] is
what coverage looks like when it happens to work.

## Audit trail

Two Codex static-review rounds (`gpt-5.6`, write/audit-only per the HARD RULES; orders in
`CODEX_AUDIT_DEPTH_COVERAGE.md` and `CODEX_AUDIT_DEPTH_COVERAGE_R2.md`). Every finding was
re-verified **by execution**, which Codex may not perform. Two reported conclusions were
retracted. **Neither changed a headline.**

**Round 1.** The percentile bootstrap around an argmax is not established, and three cells
flipped classification under the mirrored convention — the estimand was split, and the
conditional interval above became primary. Naming discipline was made binding after the arms
were over-claimed as production-mirroring. Ordinal ranks were replaced by midranks; the
*predicted* consequence was measured and **falsified** (single-column inflation exactly 0.0000).

**Round 2, finding 1 — retraction.** The `target1_gated` sensitivity arm was **mathematically
degenerate**: restricting an argmax to a superlevel set that always contains the maximum returns
the same column, and the empty case fell back to it. Its reported "gate changes selection in
0/85 folds" measured **nothing**. Arm removed. Gate-inertness now rests on the independent
per-fold record `training_peak_qualifies_0.65` = **5/5 in all 17 cells**, which is a real
measurement. **Declared gap:** the registered qualifier also required beating a per-fold
shuffled-label envelope; that limb is **not implemented here**, so this file tests the bare 0.65
threshold only, and does not test the registered convention.

**Round 2, finding 2 — retraction with measured cost.** Training-CDF calibration is a **step**
map, so the claimed invariance of single-column AUROC under a monotone map was false — strict
monotonicity is required. Measured across 255 fold-arm fits: **752 opposite-label ties created**,
**205/255 single-column fold AUROCs moved**, max 0.010 in one fold, median 7 of 40 held-out
values collapsing per fold. Cell-level effect on the primary contrast: **max 0.0035, mean
0.0012, 0/17 sign flips**. Single-column arms now score on raw oriented values; fused arms keep
the calibration because they need a common scale; pooled out-of-fold keeps it too.

**Verified clean.** Bootstrap row copies never straddle train and held-out — strata are built
per (fold, class) and each drawn position inherits its source fold; 0 straddles in 2000 draws.
Grids are never pooled. No sealed artifact is touched. Labels are asserted identical across
models within a task, which is what actually licenses the shared fold map.

**Verified vacuous.** The `sample_idx` row-identity guard fires in all 17 files but proves
nothing: it equals `arange(200)` everywhere, so it checks a positional index that is true by
construction and cannot detect a permutation of the underlying rows. No model-independent
per-row key is banked at all (`yes_no`, `gen_token_ids`, and `commit_p` all differ across
models). **Nothing reported here depends on it** — every contrast is within-cell, arm against
arm on the same rows. Logged as a **data-contract gap**, not a validity defect.

## What is NOT claimed

- This is **not registered**. It cannot upgrade or downgrade E1, E5, or E6.
- The conditional interval does **not** charge for selection. Procedure-level generalisation to
  a new model remains **unsettled**, and this dataset cannot settle it: the median training
  top-versus-runner-up margin is **0.0094**, so the races for "best block" are close enough that
  bootstrapping around the argmax is exactly the regime the audit warned about.
- No claim is made about `v_norm_lastq_weighted`. It has no per-layer data.
- The **selection-stability** observation — that cells whose argmax is stable across folds never
  lose — is **parked, not reported**. It is post-hoc, threshold-dependent (the floor breaks at
  3/5), grid-confounded, endogenous, and unstable across runs. See the `[PARKED]` section of
  candidate #16 in [[research-candidates]].

## Cross-references

- [[results/instrument-redundancy-2026-08-30]] — the companion step-2 read
- [[results/instrument-colocation-2026-08-29]] — the read that opened the hypothesis
- [[results/depth-curve-2026-08-16]] · [[results/depth-rescore-2026-08-17]] ·
  [[results/depth-grid-2026-08-17]] — the registered lane this reuses
- [[research-candidates]] #16 · [[claims]] §10 · [[paper/dc-scaffold]]
- Repo: `commit-confluence/exploratory/depth-curve/depth_coverage.py`, `DEPTH_COVERAGE.json`,
  `stability_diagnostic.py`, `STABILITY_DIAGNOSTIC.json`

> **EXTENDED 2026-09-06 — the two-instrument caveat is discharged.** Re-run with the third instrument present: adding `v_norm` to the selectable set moves the primary contrast by a median of **exactly 0.0000** in both grids and changes the depth-targeted winner in 1/8 and 2/9 cells. **Every verdict on this page stands.** The reason is redundancy, not weakness — a depth-targeted `v_norm` alone beats the two-instrument fixed panel by +0.1485 (grid A). One qualification: with nine fixed columns instead of six, fusion-loses-to-best-single-column becomes a **wash in grid A** (+0.0003) while staying negative in grid B (−0.0280). → [[results/three-instrument-2026-09-06]]
