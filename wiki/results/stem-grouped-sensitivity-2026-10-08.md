# Stem-grouped sensitivity — does HaluEval's stem pairing change the depth-curve verdicts? (2026-10-08)

**Status: [VALIDATED — robustness check; UNREGISTERED; moves no verdict].** Session analysis of
banked depth-curve artifacts. No model forwards, no Modal spend, no new data. It cannot upgrade,
downgrade or amend the grid-A rescore, the grid-B §5 verdict (terminal dip E5 **WEAKEN 8/12**,
cliff E6 **NOT TESTED**), or anything in the frozen DC draft. Torch/Modal lane, NON-byte-comparable
with sealed MLX panels; grids A and B scored separately and **never pooled**.

**Short answer: no.** Keeping each stem inside one fold, and permuting and resampling whole stems,
leaves **every registered terminal-dip pass/fail call unchanged (17/17 cells)**, leaves the grid-B
decision at WEAKEN with the same family counts, and leaves p_grid at 0.0005 in both grids. The dip
values do not move systematically. The registered HaluEval intervals turn out to be **conservative**:
the stem-aware bootstrap is about 15–20% narrower.

## Why this ran

Found during the MoE scoping audit earlier the same day (Codex `gpt-6-astra`, read-only), and
verified by the steward before anything was run:

- 🧬 **HaluEval-QA n200 is stem-paired by construction.** 100 `meta.source_idx` stems, each present
  once with a hallucinated answer (label 1) and once with a correct one (label 0). The data manifest
  says so: *"Stem-paired HaluEval qa stress task; 100 stems for 200 rows."*
- 🔁 **ANLI R1 n200 has five repeated premises**, each with one entailed and one contradicted
  hypothesis — the same structure, at 5 of 200 rows.
- ✂️ **The frozen fold builder ignores both.** `make_folds` (`rescore_grid_a.py:170`) stratifies on
  label only. The registered fold map splits **74 of 100** HaluEval stems and 4 of 5 ANLI pairs across
  folds. The registered permutation null and bootstrap are row-level.

Two things could follow. A split stem puts its shared knowledge and question into both the training
and held-out folds with opposite labels, which could bias the cross-fitted dip `Δ_cf`. And rows that
are not independent can make intervals and p-values the wrong size.

## Method

Script `commit-confluence/exploratory/depth-curve/stem_grouped_sensitivity.py` →
`STEM_GROUPED_SENSITIVITY.json` / `.md`; local, 216 s, $0. It imports the frozen machinery
(`rescore_grid_a.py`, sha256-pinned against `score_grid_b.py`'s `RESCORE_PIN_SHA256`) unmodified and
writes nothing the registered scorers own. The analysis set was enumerated in the docstring before
any output existed: 17 evaluable cells (grid A 8, grid B 9), primary `final_js_no_bos` only.

- ✅ **Part A — reproduction gate.** The registered fold map reproduces the banked fold-map sha256 and
  **all 17 banked `Δ_cf` values to < 1e-12**. Any mismatch would have aborted the run.
- 🎲 **Part B — isolates the fold-map effect.** For each cell, `Δ_cf` over **200 row-stratified** fold
  maps (the registered builder, fresh seeds) against **200 stem-grouped** fold maps. Both arms use the
  registered row-level inner envelope, so the fold map is the only difference.
- 🧱 **Part C — fully grouped inference** at one designated grouped fold map: a stem-respecting inner
  envelope and outer permutation null (each pair's two labels swap with probability ½; singletons are
  shuffled at the registered scope — training-wide for the inner envelope as in D4, within-fold for
  the outer null as in D1), a stem-cluster bootstrap within fold, NPERM_OUTER 2000, NBOOT 1000.

**Pre-run audit.** Astra audited the script statically before it ran: one MAJOR, two MINOR. The MAJOR
was a docstring that said "within fold" for both envelopes. The code matched the registered design,
so the docstring was corrected to state the two scopes. Both MINORs were applied: the
ANLI-conditioning disclosure, and the `null_q95_is_neginf` and E6 null-undefined fields. A label-only
invariant test also passed before the run, checking fold label counts, pair integrity, swap rates of
about 0.5, and that the bootstrap preserves layout.

## Results

### Part B — splitting stems did not bias the dip

| | grid A (8 cells) | grid B (9 cells) |
|---|---|---|
| median `Δ_cf` difference, grouped − row | **+0.0007** | **+0.0008** |
| cells where grouped is lower | 3/8 | 3/9 |
| largest difference by size | +0.0094 (Llama-3.3-70B/halueval) | −0.0040 (gemma-3-12b/anli, 1.1 MC se) |
| success fraction, row → grouped | unchanged except Llama-3.3-70B/halueval 0.98 → 1.00 | unchanged except Llama-3.1-8B/halueval 0.97 → 0.99 |

The differences are the size of Monte Carlo noise. The three that clear two Monte Carlo standard
errors are all HaluEval cells and all point **upward** (Llama-3.3-70B +0.0094, Qwen2.5-72B +0.0021,
Mistral-Medium-3.5 +0.0030) — if anything, splitting stems made the dip look very slightly *smaller*. That matches what a shared stem
effect should do, since it enters training and held-out folds with opposite labels.

### Part C — every registered call survives

- 🎯 **Terminal dip (E5): 17/17 cells keep their pass/fail call.** Grid A **8/8**. Grid B **8/9
  evaluable**, so 8/12 with the three aborted cells counted as failures. Applying the frozen §5 rule
  counterfactually still gives **WEAKEN**, with the same family counts (Llama-3.1 4, Mistral 2,
  Gemma 2). **p_grid 0.0005** in both grids, unchanged.
- 📏 **Intervals tighten on HaluEval.** Median ratio of grouped to registered per-cell CI width is
  **0.85** (grid A) and **0.80** (grid B) on HaluEval, and 0.95 / 0.94 on ANLI. Pooled aggregate CIs:

| | registered | stem-grouped |
|---|---|---|
| grid A pooled (8 cells) | [0.189, 0.261] | [0.188, 0.251] |
| grid B pooled (9 evaluable) | **[0.123, 0.201]** | **[0.134, 0.204]** |
| grid B halueval | [0.087, 0.187] | [0.111, 0.186] |
| grid B anli | [0.131, 0.259] | [0.136, 0.259] |

  The largest single-cell change is Mistral-Medium-3.5/halueval: [−0.011, 0.220] → [0.053, 0.201].
  A paired design gives precision that a row bootstrap ignores, so the registered intervals were
  conservative, not optimistic.
- ⛰️ **Cliff (E6), descriptive only.** Grid A 7/8, with the same cells as registered. Grid B keeps a
  count of **2/9**, but the membership changes: gemma-3-12b/anli loses its cliff because the grouped
  map's training peak falls before the E6 window, and Mistral-Medium-3.5/anli gains one. Grid-B E6
  remains NOT TESTED; this only shows that individual grid-B cliff calls depend on the fold map.

### Side finding — one fold map carries fold-draw noise

Part B also gives the spread of `Δ_cf` across fold draws, which the registered single-map design
never reported. Per-cell standard deviations run **0.007–0.038**.

- 📍 **Three grid-A registered values sit at the top of their own draw distributions:**
  Llama-3.3-70B/anli **0.416** against a draw mean of 0.324 (97.5th percentile), Qwen2.5-7B/anli 0.242
  against 0.223 (97.5th), and Qwen2.5-7B/halueval 0.202 against 0.190 (95.5th). Grid-B registered
  values sit between the **38th and 78th** percentiles, which is ordinary.
- 🎚️ **Near-bar cells.** Llama-3.1-8B/halueval passes the 0.05 bar in 97% of row draws and 99% of
  grouped draws. The designated grouped map happened to land it at 0.0575, against a typical value of
  about 0.099. Llama-3.3-70B/halueval passes in 98% and 100%.
- 🧭 **What it means.** This is variance, not bias, and it moves no call: every pass/fail is stable in
  ≥97% of draws, and Mistral-Small/halueval fails in all of them. But grid-A point estimates,
  especially Llama-3.3-70B/anli's 0.416, overstate the typical value for that cell by up to about
  0.09. Quote ranges or draw means when the magnitude matters.

### Reading caution — per-cell permutation p

The per-cell `perm_p` counts permutations with no qualifying training peak as −∞ (registered D3). It
therefore mostly tests **whether a qualifying peak exists**, not how large the dip is. Mistral-Small/
halueval has p = 0.0005 with a dip of 0.0045. Read `Δ_cf` and its interval for dip size. This is the
registered convention, unchanged here.

## Scope and what is not covered

- 🚫 **Not rescored:** E7 cross-task peak distance, E8 Llama band counts, the E1″ panel, and the
  depth-coverage, redundancy and three-instrument follow-ons
  ([[results/depth-coverage-2026-08-31]], [[results/three-instrument-2026-09-06]]). They all use the
  same row-level fold map on HaluEval. Part B's null result for `Δ_cf` makes a large effect unlikely,
  but their estimators differ and remain unverified.
- 🔒 **ANLI intervals are conditional** on the five paired premises, because there is one per fold and
  that stratum has no bootstrap variability. Five of 200 rows.
- 🧪 **The swap null** tests conditional exchangeability of each stem's two rows, a slightly different
  null from the registered row permutation. Both give p_grid 0.0005.

## What this changes

- 📄 **The DC draft needs no correction.** Every number it states stands, and its intervals are
  conservative. MK froze the draft on 2026-09-06. An optional one-sentence disclosure — "folds split
  HaluEval's stem pairs; keeping stems together leaves every call unchanged and narrows the intervals" —
  is logged as an open decision, not applied.
- 🧾 **Data-contract gap, now documented.** The frozen scorers never read `meta.source_idx`. Any
  future registered scorer on these files should build stem-grouped folds and resample stems.

Cross-refs: [[results/depth-grid-2026-08-17]] · [[results/depth-rescore-2026-08-17]] ·
[[paper/dc-scaffold]] · [[research-candidates]] #13 ·
[[_archive/workorders/moe-router-pilot-workorder-2026-10-08]] (the audit that surfaced this).

## 2026-10-09 addendum — the follow-ons, now covered

The "not covered" list above has been run. Script `commit-confluence/exploratory/depth-curve/stem_grouped_followons.py`
→ `stem_grouped_followons/` (local, $0, ~4 min). It re-runs `score_grid_b.py` (E7, E8, E1″), the depth-coverage,
three-instrument and attention-family analyses with **stem-grouped folds** inside a temporary copy, so no banked file can be
overwritten; everything else is the banked machinery. An unpatched control in the same environment reproduces the banked
follow-on files exactly, so every difference below is the fold map. Colocation and redundancy use no folds; the stability
diagnostic is parked — all three skipped.

- ✅ **Unchanged:** E5 WEAKEN 8/12 with the same families; every E7 cross-task peak distance; E1″ for every grid-B family;
  `js_kv_groups` as modal fold winner (30/85); adding a third instrument or widening 3→7 metrics (median ≈ 0.0000).
- ✅ **Same direction, fold-draw-sized shifts:** targeting beats the fixed aggregate (A 7/8 → 7/8, B 7/9 → 8/9); targeting
  vs best single fixed depth (A 6/8 at +0.120 → +0.126; B still split, 6/9 → 5/9); the two-instrument targeted pair on
  held-out models (7/9 at +0.056 → 7/9 at +0.054); fusion loses to the best single column at the canonical 21 columns
  (A −0.015 → −0.022, B −0.046 → −0.044, 5/9 still exclude 0). At six columns the same contrast halves (A −0.044 → −0.021,
  B −0.038 → −0.022).
- ⚠️ **P9 is a knife-edge, and that is not about stems.** Under the grouped map P9 flips to a miss (8B mid-block counts
  [4, 5, 4, 5, 5] vs banked [4, 3, 6, 4, 5]). Over 100 re-drawn fold maps it is a **HIT in only 37/100 row-stratified and
  39/100 stem-grouped maps**: the 8B's qualifying mid-block count has a median of exactly 5 against a "< 5" bar. The
  registered HIT stands as written; it was the less likely side of a near coin flip. The robust content is the contrast —
  about 5 qualifying mid-blocks at 8B against about 23 at 70B.
- ⚠️ **Llama-3.3-70B/anli's cross-fitted peak is bimodal.** Under the grouped map it moved 48 → 69 (E1″ Llama-3.3 mean
  fraction 0.46 → 0.59). Over 100 maps of either kind the peak lands at 48 in about two-thirds and at 69 in about
  one-third — the broad band making the argmax unstable. Identical with or without grouping. Reinforces the standing rule:
  never argue a locus from an argmax.
- ℹ️ Grid-B E6 (NOT TESTED) count moves 2 → 3 — individual cliff calls depend on the fold map, as noted above.
