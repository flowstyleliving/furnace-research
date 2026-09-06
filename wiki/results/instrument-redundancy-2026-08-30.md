# Instrument redundancy — are the three ACE attention cells one variable? (2026-08-30)

**Status: [OPEN — descriptive; NOT a registered endpoint].** Session analysis of *existing*
banked torch-panel matrices. No model forwards, no Modal spend, no pre-registration, no new
data. Does **not** alter any sealed claim or panel number. Torch/Modal lane,
NON-byte-comparable with the sealed MLX panels. **Signs are fit in-sample**, so every AUROC on
this page is optimistic in level; the page is about *structure*, not deployability.

Companion page: [[results/depth-coverage-2026-08-31]]. This is **step 2** of candidate #16's
proposed mechanism ([[research-candidates]]); the discriminating test is step 3.

## The question

[[results/instrument-colocation-2026-08-29]] showed that two ACE attention instruments trace
weakly-correlated *depth* curves. That is a claim about shape across layers. It leaves the
original factor-structure question open at a **fixed** layer: at one panel depth, on one model
and task, do the three instruments carry one variable or three?

Unlike the depth question, this one can use all three instruments. The banked `profiles_ext`
matrices record `js_no_bos`, `bos_mass`, **and** `v_norm_lastq_weighted` at each of the three
panel depths. Only the *per-layer* data for the third instrument is missing.

## Method

Read-only script `commit-confluence/exploratory/depth-curve/instrument_redundancy.py` →
`REDUNDANCY.json`, reading the banked matrices at
`~/Documents/furnace-guard/artifacts/modal_profiles_ext/profiles_ext`. n = 200 rows per cell.

A **cell** is one (model, task, depth) triple. For each cell:

- **Pairwise Spearman** between the three instruments.
- **PC1 variance fraction** — the share of the three-instrument covariance carried by the first
  principal component. High means the three collapse to one direction.
- **Solo AUROC** per instrument, with the sign fit in-sample.
- **R² from the others** — how much of an instrument is linearly predictable from the other two.
- **Residual AUROC** — the instrument's separation *after* the other two are regressed out. This
  is the "does it carry anything of its own" number.
- **`n_unique_above_bar`** — how many of the three clear a **0.60** residual AUROC bar.

**42 non-variant cells** are analysed. 30 precision-variant cells are held out of every summary.

**Coverage is unbalanced and this bounds every model-level statement.** Qwen2.5-32B contributes
24 cells across 8 tasks; Llama-3.3-70B, Qwen2.5-72B, and Qwen2.5-7B contribute 6 each across 2
tasks. Depths are balanced at 14 cells each.

## Results — headline

| statistic | value |
|---|---|
| PC1 variance fraction | median **0.594**, range [0.398, 0.940] |
| cells where PC1 ≥ 0.90 (near-collapse) | **5 / 42** |
| pairwise absolute Spearman | median **0.379**, range [0.001, 0.993] |
| cells with ≥2 instruments above the 0.60 residual bar | **21 / 42** |
| cells with 3 / 2 / 1 / 0 instruments above the bar | 4 / 17 / 12 / 9 |
| R² predicted from the other two | median **0.349**; ≥0.90 in **16 / 126** instrument slots |

**The three instruments are not redundant in general. Redundancy is cell-specific.**

## Results — per instrument

| instrument | solo AUROC (median) | residual AUROC (median) | R² from others (median) | residual ≥0.60 |
|---|---|---|---|---|
| `js_no_bos` | 0.619 | 0.594 | 0.447 | 19/42 |
| `bos_mass` | 0.647 | 0.592 | **0.111** | 20/42 |
| `v_norm_lastq_weighted` | **0.661** | 0.573 | 0.518 | 19/42 |

Two things follow.

**No instrument is dominated, and none is universally unique.** All three sit within 0.02 of
each other on median residual AUROC and within one cell of each other on how often they clear
the bar. There is no ranking here, only a set.

**`bos_mass` is the most independent of the three.** Its R² from the other two has median
**0.111**, against 0.447 for `js_no_bos` and 0.518 for `v_norm_lastq_weighted`. The panel's
least-examined instrument is its least redundant one — which is the same direction as the
co-location finding that `bos_mass` matches or beats the registered primary in 11/17 depth
cells.

## Results — structure by model and depth

| model | depth | cells | PC1 median | PC1 max | ≥2 unique | mean n_unique |
|---|---|---|---|---|---|---|
| Llama-3.3-70B | mid | 2 | 0.925 | 0.940 | 0/2 | 1.00 |
| Llama-3.3-70B | last_minus_1 | 2 | 0.923 | 0.930 | 2/2 | 2.50 |
| Llama-3.3-70B | final | 2 | 0.880 | 0.914 | 0/2 | 1.00 |
| Qwen2.5-32B | mid | 8 | 0.568 | 0.699 | 1/8 | 0.38 |
| Qwen2.5-32B | last_minus_1 | 8 | 0.731 | 0.818 | 4/8 | 1.50 |
| Qwen2.5-32B | final | 8 | 0.448 | 0.474 | 7/8 | 2.12 |
| Qwen2.5-72B | mid | 2 | 0.711 | 0.753 | 1/2 | 1.00 |
| Qwen2.5-72B | last_minus_1 | 2 | 0.727 | 0.738 | 1/2 | 1.50 |
| Qwen2.5-72B | final | 2 | 0.519 | 0.639 | 1/2 | 1.50 |
| Qwen2.5-7B | mid | 2 | 0.583 | 0.612 | 1/2 | 1.00 |
| Qwen2.5-7B | last_minus_1 | 2 | 0.564 | 0.581 | 2/2 | 2.50 |
| Qwen2.5-7B | final | 2 | 0.463 | 0.471 | 1/2 | 1.00 |

**All five near-collapse cells are Llama-3.3-70B.** Every Llama cell sits at PC1 0.88–0.94; no
Qwen cell exceeds 0.82. On the Llama panel the three instruments really are close to one
variable. On the Qwen panels they are not. `[HYPOTHESIS]` This is a family-level property, and
it rhymes with the registered family dissociation in signal locus
([[results/depth-grid-2026-08-17]]) and with the Llama mid-stack band the panel rungs straddled
(P3). **Two Llama tasks, one Llama model — this is a pointer, not a result.**

**Redundancy is depth-dependent within a model.** On Qwen2.5-32B, the widest-coverage cell set,
PC1 falls from 0.731 at `last_minus_1` to 0.448 at `final`, and the count of cells with two or
more independent instruments rises from 4/8 to **7/8**. The instruments separate as the stack
terminates.

## What this says

**1. The standing "one shared change in attention allocation" reading is not supported as a
general claim.** It survives only where PC1 is high, which is 5 of 42 cells and all of them one
model family.

**2. It is not refuted either.** Nine cells have *no* instrument clearing the residual bar, and
those are consistent with a single weak shared factor. The honest verdict is that the factor
structure is **cell-specific** and the panel is measuring different numbers of things in
different places.

**3. This is the fixed-depth half of the co-location question.** At a fixed layer the
instruments are usually distinguishable. Across layers ([[results/instrument-colocation-2026-08-29]])
their curve shapes diverge and 6/17 cells are mutually blind. The two reads agree.

## What is NOT claimed

- **Signs are fit in-sample.** Solo and residual AUROCs are optimistic in level. Only the
  *relative* structure — PC1, R², which instruments clear the bar — is being read.
- Not registered; cannot upgrade or downgrade any sealed or grid verdict.
- Model-level statements are bounded by unbalanced coverage: 24 cells for Qwen2.5-32B against 6
  each for the other three models.
- The 0.60 residual bar is the registered qualifying bar reused for convenience, not a
  pre-registered threshold for this question.

## Cross-references

- [[results/depth-coverage-2026-08-31]] — the step-3 discriminating test
- [[results/instrument-colocation-2026-08-29]] — the across-layer half
- [[results/depth-grid-2026-08-17]] — the registered family dissociation this rhymes with
- [[research-candidates]] #16 · [[claims]] §10 · [[results/kv-tension-pilot-2026-06-09]]
  (the comparator-enumeration lesson)
- Repo: `commit-confluence/exploratory/depth-curve/instrument_redundancy.py`, `REDUNDANCY.json`

> **EXTENDED 2026-09-06 — the depth half is now three-instrument.** This page's fixed-depth read already used all three instruments; its *depth* companion no longer lacks one. The finding that `bos_mass` is the least predictable of the three at a fixed depth (R² 0.111) sits alongside a new one: **down the stack, `bos_mass` and `v_norm` are nearly the same curve** (r median 0.896). Fixed-depth independence and depth-curve independence are not the same property. → [[results/three-instrument-2026-09-06]]
