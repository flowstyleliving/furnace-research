# The ACE attention family at depth — three instruments, then all seven (2026-09-06)

**Status: [OPEN — descriptive; NOT a registered endpoint].** First read of candidate #16 that is
**not one instrument short**. The additive per-layer v-norm capture channel (`commit-confluence`
commit `1b9da4b`) ran 2026-09-02 and wrote a `<slug>.vnorm.npz` sidecar for all 17 usable cells;
this page joins those sidecars to the registered depth artifacts. Cannot upgrade or downgrade
E1, E5 or E6. Torch/Modal lane, NON-byte-comparable with the sealed MLX panels; grids A and B
**never pooled**. The v-norm channel is unregistered by construction (`registered: false` in its
own metadata).

Supersedes the standing "one instrument short" caveat on
[[results/instrument-colocation-2026-08-29]], [[results/instrument-redundancy-2026-08-30]] and
[[results/depth-coverage-2026-08-31]].

> ## ⚠ REVISED SAME DAY — read this first
>
> The three-metric read below is correct as far as it goes, and its "two signals" framing is
> **an artifact of which three metrics were chosen**. The deployed ACE attention panel
> (`ATTENTION_PANEL_T0_WITH_V_NORMS`) is 3 layers × **seven** metrics, and four of the seven had
> never been examined at depth. Scoring all seven changes the conclusion — see
> [Extension: all seven metrics](#extension-all-seven-metrics) at the end of this page. In short:
> **two of the seven deployed metrics carry no signal at any depth**, and among the five that do,
> there is no clean two-way partition — `js_no_bos` is simply the least-coupled member. Do not
> quote "the panel is two signals" without the seven-metric section.

## The headline (three-metric read)

**On the three metrics examined here, the panel is not three signals. It is two.**

`bos_mass` and `v_norm_lastq_weighted` trace nearly the same depth curve — **Pearson r median
0.896 across all 17 cells** — and peak at the same block in **8/17**. `js_no_bos` stands apart
from both: r median **0.329** against `bos_mass` and **0.384** against `v_norm`, sharing a peak
block with `bos_mass` in only **2/17**.

The panel therefore reads **inter-head disagreement** on one side and a **magnitude-and-sink
family** on the other. The third instrument is a second measurement of the second thing.

## Method

Read-only script `commit-confluence/exploratory/depth-curve/three_instrument.py` →
`THREE_INSTRUMENT.json`. Reuses `depth_coverage.py`'s helpers unchanged, so the cross-fit
convention, midranks, training-CDF calibration, raw scoring for single-column arms and the
evaluation-row-only conditional interval are all identical.

**The row-identity join is enforced, not assumed** — the direct fix for the finding that
`sample_idx` was a vacuous guard. The sidecar mirrors `labels`, `gen_token_ids`, `commit_p` and
`yes_no`; the three integer columns must match **bit-exactly** and `commit_p` at a calibrated
tolerance. Any cell failing either test is refused, not repaired.

> **The guard fired, and calibrating it was a measurement.** Exact equality on all four columns
> refused **5 of 17 cells**, every one of them `anli_r1`. The disagreement was 1–2 rows per cell
> at |Δ| ≤ **2.220e-16** — one to two units in the last place of a float64 near 1.0, i.e.
> floating-point non-determinism between the registered run and the sidecar recomputation.
> `commit_p` is the **only** mirrored column with row-level resolution (200 distinct values per
> cell, against 2 for `labels`, 2 for `yes_no`, 3 for `gen_token_ids`), so it could not simply be
> dropped from the check. The smallest gap between two genuinely distinct `commit_p` values in a
> cell is **5.936e-08**, and a permutation moves a typical value by ~1e-3. The tolerance was set
> to **1e-12**: four orders of magnitude above the observed artifact, five below the smallest
> real gap. A permuted row would exceed it by roughly nine orders of magnitude. All 17 cells then
> joined, 0 refused.

**Cross-check on the join.** The `js~bos` curve correlations recomputed here reproduce the
registered co-location medians exactly — **0.517** (grid A) and **0.218** (grid B). The third
instrument was added without disturbing the first two.

Capture was clean: every cell reports 0 non-finite values and 0 failed blocks, mode
`per_block_v_proj_hook`.

## Results — curve shape and peak location

Peak block / peak sign-free AUROC per instrument, pairwise curve correlation, and the count of
instrument pairs **mutually blind** at the registered 0.65 bar (each below it at the other's peak).

| grid | task | model | N | js peak/AUC | bos peak/AUC | vnorm peak/AUC | r js~bos | r js~vn | r bos~vn | blind |
|---|---|---|---|---|---|---|---|---|---|---|
| A | anli | Llama-3.3-70B | 80 | 48 / 0.897 | 70 / 0.915 | 70 / 0.914 | +0.800 | +0.836 | **+0.971** | 0/3 |
| A | anli | Qwen2.5-32B | 64 | 56 / 0.866 | 55 / 0.868 | 56 / 0.864 | +0.430 | +0.781 | +0.583 | 1/3 |
| A | anli | Qwen2.5-72B | 80 | 66 / 0.838 | 77 / 0.904 | 77 / **0.932** | +0.604 | +0.661 | +0.895 | 0/3 |
| A | anli | Qwen2.5-7B | 28 | 22 / 0.834 | 22 / 0.738 | 24 / 0.828 | +0.777 | +0.904 | +0.721 | 0/3 |
| A | halueval | Llama-3.3-70B | 80 | 26 / 0.862 | 26 / 0.910 | 26 / 0.914 | +0.742 | +0.769 | +0.944 | 0/3 |
| A | halueval | Qwen2.5-32B | 64 | 56 / 0.911 | 62 / 0.849 | 56 / **0.915** | +0.329 | +0.727 | +0.408 | 0/3 |
| A | halueval | Qwen2.5-72B | 80 | 63 / 0.896 | 70 / 0.853 | 76 / 0.866 | +0.116 | +0.290 | +0.847 | 1/3 |
| A | halueval | Qwen2.5-7B | 28 | 26 / 0.871 | 22 / 0.737 | 22 / 0.747 | +0.217 | +0.269 | +0.520 | 0/3 |
| B | anli | Llama-3.1-70B | 80 | 45 / 0.902 | 61 / 0.915 | 45 / 0.912 | +0.334 | +0.384 | +0.959 | 0/3 |
| B | anli | Llama-3.1-8B | 32 | 18 / 0.744 | 30 / 0.751 | 30 / 0.752 | +0.408 | +0.518 | +0.931 | 2/3 |
| B | anli | Mistral-Medium-3.5 | 88 | 83 / 0.867 | 70 / 0.880 | 70 / 0.880 | +0.218 | +0.280 | +0.896 | 2/3 |
| B | anli | gemma-3-12b | 48 | 39 / 0.793 | 46 / 0.841 | 34 / 0.847 | +0.460 | +0.347 | +0.796 | 0/3 |
| B | halueval | Llama-3.1-70B | 80 | 38 / 0.898 | 26 / 0.904 | 26 / 0.903 | +0.110 | +0.097 | +0.925 | 2/3 |
| B | halueval | Llama-3.1-8B | 32 | 1 / 0.891 | 29 / 0.886 | 29 / 0.874 | +0.016 | +0.029 | +0.959 | 2/3 |
| B | halueval | Mistral-Medium-3.5 | 88 | 85 / 0.848 | 87 / 0.891 | 58 / 0.875 | +0.127 | +0.079 | +0.917 | 0/3 |
| B | halueval | Mistral-Small-3.2 | 40 | 37 / 0.879 | 33 / 0.905 | 29 / 0.895 | +0.240 | +0.385 | +0.929 | 0/3 |
| B | halueval | gemma-3-12b | 48 | 22 / 0.900 | 43 / 0.886 | 41 / 0.896 | +0.027 | +0.013 | +0.516 | 0/3 |

| pair | grid A median r | grid B median r | all 17 | shares peak block |
|---|---|---|---|---|
| `js_no_bos` ~ `bos_mass` | 0.517 | 0.218 | **0.329** | 2/17 |
| `js_no_bos` ~ `v_norm` | 0.748 | 0.280 | **0.384** | — |
| **`bos_mass` ~ `v_norm`** | 0.784 | **0.925** | **0.896** | **8/17** |

## Results — cross-fitted arms

Same 5-fold convention as [[results/depth-coverage-2026-08-31]]. Two-instrument arms are
restricted to the js and bos columns, so each 3i-vs-2i contrast isolates the third instrument
exactly. Conditional (evaluation-row-only) intervals.

| contrast | A wins | A median | A excl 0 | B wins | B median | B excl 0 |
|---|---|---|---|---|---|---|
| **`target1_3i` − `target1_2i`** | 1/8 | **+0.0000** | 1/8 | 2/9 | **+0.0000** | 2/9 |
| `rung_best1_3i` − `rung_best1_2i` | 1/8 | +0.0000 | 2/8 | 0/9 | +0.0000 | 0/9 |
| `fixed9` − `fixed6_2i` | 5/8 | +0.0263 | 5/8 | 4/9 | −0.0005 | 4/9 |
| `target3` − `target2_2i` | 7/8 | +0.0147 | 4/8 | 5/9 | +0.0023 | 2/9 |
| `target1_3i` − `rung_best1_3i` | 6/8 | +0.1340 | 6/8 | 7/9 | +0.0225 | 2/9 |
| `target3` − `rung_best1_3i` | 7/8 | +0.1305 | 6/8 | 7/9 | **+0.0583** | **7/9** |
| `target1_vnorm` − `rung_best1_2i` | 6/8 | +0.1485 | 7/8 | 7/9 | +0.0235 | 4/9 |
| `fixed9` − `rung_best1_3i` | 4/8 | +0.0003 | 3/8 | 2/9 | −0.0280 | 3/9 |

## What this says

**1. Adding the third instrument to the selectable set changes almost nothing.** The primary
contrast is a median of **exactly 0.0000** in both grids, and the depth-targeted winner is
unchanged in 7/8 and 7/9 cells. Adding it to the best-fixed-rung set changes the winner in 1/8
and **0/9**. Whatever `v_norm` measures, `js` and `bos` between them already had it.

**2. That is not because `v_norm` is weak — it is because it duplicates `bos_mass`.** On its own,
a depth-targeted `v_norm` beats the two-instrument fixed panel by median **+0.1485** in grid A
(7/8 intervals exclude zero) and **+0.0235** in grid B. It is a good instrument. It is a good
instrument pointed at the same thing.

**3. The co-location finding survives and sharpens.** The 2026-08-29 read said the instruments
diverge. It can now say **which**: the divergence is `js_no_bos` against the other two, not a
three-way spread. Mutual blindness at the 0.65 bar still appears in 6/17 cells, and in every one
of them the blind pair involves `js`.

**4. The fixed-fusion result needs qualifying, not retracting.** With six columns, fusing lost to
the best single fixed rung by −0.0435 (A) and −0.0383 (B). With nine, it is a **wash in grid A**
(+0.0003, 4/8) and still negative in grid B (−0.0280, 2/9). Adding a redundant instrument helps
the fusion arm more than the single-column arm, which is what a rank-mean over correlated columns
would predict. **The held-out-model direction is unchanged.**

**5. The depth-coverage verdict is unchanged.** `target3` versus the best fixed rung is 7/8 and
7/9, with 7/9 grid-B intervals excluding zero — the same shape as the two-instrument `target2`
result. The third instrument does not rescue grid B and does not damage grid A.

## What is NOT claimed

- **Not registered.** Nothing here can move E1, E5 or E6.
- **No mechanism claim.** That `bos_mass` and `v_norm_lastq_weighted` correlate at 0.896 down the
  stack is a statement about their depth curves on 17 cells, not a proof that they compute the
  same quantity. Both are magnitude-flavoured reads of the attention write; the correlation is
  consistent with that and does not establish it.
- **Peak-location claims remain in-sample.** Peak blocks here are in-sample sign-free argmaxes,
  and [[results/instrument-colocation-2026-08-29]] showed the bootstrap bands are too wide at
  n=200 to carry a locus claim. The "shares a peak block in 8/17" count is descriptive.
- **The selection-stability gate is still parked**, unchanged.

## Cross-references

- [[results/depth-coverage-2026-08-31]] · [[results/instrument-redundancy-2026-08-30]] ·
  [[results/instrument-colocation-2026-08-29]] — the three reads this completes
- [[results/depth-curve-2026-08-16]] · [[results/depth-grid-2026-08-17]] — the registered lane
- [[research-candidates]] #16 · [[claims]] §10 · [[paper/dc-scaffold]]
- Repo: `commit-confluence/exploratory/depth-curve/three_instrument.py`,
  `THREE_INSTRUMENT.json`, `npz_vnorm/`, and the capture channel in commit `1b9da4b`


---

## Extension: all seven metrics

Run 2026-09-06, same session, after the three-metric read was already written and committed.
Script `attention_family.py` → `ATTENTION_FAMILY.json`. Same 17 cells, same cross-fit
convention, same row-identity enforcement. The registered depth artifacts carry all four
weight-only metrics per block (`js`, `js_kv_groups`, `js_no_bos`, `bos_mass`); the 2026-09-02
sidecar carries all three value-norm metrics. That is **7 of 7 with depth data**.

### Median curve correlation across all 17 cells

|  | js | js_kv | js_nobos | bos | vn_bos | vn_max | vn_lastq |
|---|---|---|---|---|---|---|---|
| **js** | 1.000 | **0.839** | 0.513 | 0.632 | 0.048 | −0.004 | 0.725 |
| **js_kv** | 0.839 | 1.000 | 0.587 | 0.534 | 0.045 | 0.048 | 0.614 |
| **js_nobos** | 0.513 | 0.587 | 1.000 | **0.329** | 0.049 | 0.013 | **0.384** |
| **bos** | 0.632 | 0.534 | 0.329 | 1.000 | 0.046 | −0.052 | **0.896** |
| **vn_bos** | 0.048 | 0.045 | 0.049 | 0.046 | 1.000 | 0.031 | 0.047 |
| **vn_max** | −0.004 | 0.048 | 0.013 | −0.052 | 0.031 | 1.000 | −0.040 |
| **vn_lastq** | 0.725 | 0.614 | 0.384 | 0.896 | 0.047 | −0.040 | 1.000 |

### Peak sign-free AUROC per metric, 17 cells

| metric | median | min | max | cells ≥ 0.65 | fold-selection wins (of 85) |
|---|---|---|---|---|---|
| `js` | 0.870 | 0.734 | 0.914 | 17/17 | 4 |
| `js_kv_groups` | 0.871 | 0.722 | **0.929** | 17/17 | **30** |
| `js_no_bos` | 0.871 | 0.744 | 0.911 | 17/17 | 17 |
| `bos_mass` | 0.886 | 0.737 | 0.915 | 17/17 | 13 |
| **`v_norm_bos`** | **0.551** | 0.511 | 0.587 | **0/17** | **0** |
| **`v_norm_max`** | **0.616** | 0.559 | 0.680 | **1/17** | **0** |
| `v_norm_lastq_weighted` | 0.880 | 0.747 | **0.932** | 17/17 | 21 |

### What the seven-metric read establishes

**1. Two of the seven deployed metrics carry essentially no signal at any depth.**
`v_norm_bos` peaks at a median of **0.551** and clears the registered 0.65 qualifying bar in
**0 of 17** cells. `v_norm_max` reaches 0.616 and clears it in **1 of 17**. Neither is selected
in **any** of the 85 cross-fitted folds. Their near-zero correlations with everything else are
**noise, not independence** — a flat curve has no structure to correlate with.

**2. That kills the clean two-way partition.** Among the five metrics that do carry signal,
correlations run 0.33–0.90 with no clean split. The tightest pair is `bos_mass`~`v_norm_lastq`
at **0.896**; the second tightest is `js`~`js_kv_groups` at **0.839**. Crucially, `js` sits
*closer to the sink family* (0.632 with `bos`, 0.725 with `v_norm_lastq`) than to `js_no_bos`
(0.513). **`js_no_bos` — the registered primary — is simply the least-coupled member of one
broad family**, not one pole of a two-pole structure. The three-metric "two signals" reading
came from picking one metric from each end and none from the middle.

**3. `js_kv_groups` is the modal winner and had never been looked at.** It takes **30 of 85**
fold selections, more than any other metric, and reaches the second-highest peak AUROC in the
panel (0.929). It was excluded from every prior depth read for no reason other than the
co-location work having named three instruments.

**4. Widening the selectable set does not improve the depth-targeted arm.** `target1_7 −
target1_3` is a median of **exactly +0.0000** in both grids (wins 3/8 and 2/9). `js_kv_groups`
wins often but does not outperform what the trio would have picked. Two cells gain materially
(Mistral-Medium-3.5: +0.057 anli, +0.053 halueval) and two lose (gemma-3-12b anli, Mistral-Small
halueval).

**5. The fusion-loses-to-best-single-column result is restored at the full column set.**
`fixed21 − rung_best1_7` is **−0.0145** (grid A) and **−0.0457** (grid B, 5/9 intervals excluding
zero). The grid-A wash reported at nine columns does not survive at twenty-one. `fixed21` matches
the **deployed ACE t=0 column set**, though it remains a local construction and not the deployed
arm — signs, cohort and selection all differ.

**6. Mutual blindness is far more common than the three-metric read suggested** — a median of
**9 of 21** instrument pairs per cell are simultaneously below the 0.65 bar at each other's peak.
Much of that is driven by the two dead metrics.

### What this does not change

The depth-coverage verdicts are untouched. `target7 − rung_best1_7` is 8/8 and 7/9 with 6/8 and
6/9 intervals excluding zero — the same shape as `target2` and `target3`. Depth targeting still
beats fixed rungs on grid A and splits on grid B.

### Scope

Peak AUROCs are in-sample and sign-free. The "no signal" verdict on `v_norm_bos` and
`v_norm_max` is about **their per-layer separation curves on these 17 cells at the t=0 commit
locus**; it is not a claim about their behaviour inside the deployed calibrator, where they enter
as fused panel cells under sealed-era signs. Descriptive, not registered.
