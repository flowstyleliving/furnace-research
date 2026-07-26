# Codex work order — re-home the KV-tension implementation as an additive overlay

**For:** Codex `gpt-5.6-sol` · **Repo:** `commit-confluence` · **Written:** 2026-07-25 (Claude Code, executor)
**Codex is write/audit-only.** Author the module, the tests, and the docs. Do **not** run tests, extraction, calibration, `pip`, or `git tag`/`git push`. Where verification needs execution, the commands are listed under Acceptance and marked *not run by Codex*.

## Scope, stated honestly before anything else

This restores **runnability**, not standing. The lane it belongs to — `attention-kv-tension` — was scored on 2026-07-25 and is **`[PILOT RUN — NO-PROMOTE]`**: none of its three registered promotion limbs is met, and the pre-registered BOS/sink falsification clause is partially triggered. See `wiki/results/kv-tension-pilot-2026-06-09.md`.

So the deliverable is a **working, tested, unpromoted instrument** — nothing more. Specifically:

- **Do not** run a new panel, produce new AUROCs, or write anything that reads as a result.
- **Do not** revive the 2026-06-09 pre-registration draft or amend it. Any future run needs a **fresh** registration that enumerates its comparator cells by name and makes the shuffled-label control a launch blocker.
- **Do not** add these cells to any default panel, sealed or unified. They are opt-in, always.

## Why the port is needed at all

The metric implementation currently exists **only** as an unapplied diff against three sealed `t0-morphology-furnace` modules:

```
commit-confluence/exploratory/attention-kv-tension/t0-patch/kv-tension-against-t0-7c2fcb7.patch
```

`t0-morphology-furnace` is sealed archive-only as of 2026-07-25; its working tree must stay byte-identical to `t0-ace-sealed-2026-05-26`, because that byte-identity is the sole basis on which the packaging tag `t0-pkg-v0.1.0` can be trusted. **The patch must never be applied to t0.** Re-homing the code is what makes it usable without breaking that.

## Measured facts — do not re-derive

Verified 2026-07-25 by reading the source. Treat as given.

| Fact | Value |
|---|---|
| CC ↔ sealed seam | `confluence_calibrator.py` imports `pri_calibrator as SEAL` **read-only**, with a vendored `sealed_selector.py` fallback |
| CC owns the capture loop | `collect_ace_matrix` (`confluence_calibrator.py:513`) opens `attention_capture` / `attention_capture_with_values`, calls `SEAL._trace_one_prompt`, then `SEAL._compute_panel_scores_for_sample` at l.557, then fills `sm[i, j]` per panel cell |
| Per-cell scoring precedent already exists | `stage_b/gemma4_full_extract.py:90` already calls `SEAL._compute_attention_score(cell, store["caps"], store["nkv"], …)` directly |
| CC module convention | flat top-level modules at repo root (`confluence_calibrator.py`, `sealed_selector.py`) |
| CC test convention | no root `tests/` dir; test files sit beside their subject (`stage_b/test_verify_bench_provenance.py`) |
| Patch content | 4 metric fns + 1 helper in `scripts/diagnose_inter_head_disagreement.py`; a metric tuple + 3 panels + a `_compute_attention_score` branch + a CLI flag in `pri_calibrator.py`; 8 tests in `tests/test_attention_cells.py` |

**The seam is already the right shape.** Because CC owns the capture loop and already scores cells one at a time against the sealed helper, the KV-tension cells can be computed in CC from the same `sample_caps` the sealed panel used — with **no monkeypatching and no edit to any sealed module.**

## D1 — `kv_tension_panel.py` (new flat module at CC repo root)

Port from the patch. Keep the semantics **exactly** as written; this is a relocation, not a redesign.

**Metric functions** — port verbatim, preserving docstrings and every guard:

- `_kv_group_attention(weights, n_kv_heads)` — normalize + reshape to `(n_kv, repeats, T)`; returns `None` on `ndim != 2`, `n_heads % n_kv != 0`, or any zero row-sum.
- `js_within_kv_groups` — mean JS-radius among Q heads sharing each KV group. **MHA (`n_q == n_kv`) returns `0.0`, not NaN** — no within-group degree of freedom. This convention is pinned in the pre-registration; do not "improve" it.
- `js_within_kv_groups_no_bos` — same after `_drop_bos_and_renorm`; NaN on empty.
- `js_kv_tension_gap` — `_js_radius(w) − _js_radius_kv_groups(w, n_kv)`; NaN if either is non-finite.
- `js_kv_tension_ratio` — `between / (max(within, 0) + EPS)`. **NaN when `repeats <= 1`** (MHA): the denominator is a *structural* zero, not a measured small quantity. Preserve that distinction — it is the difference between "no signal" and "not applicable."

Their dependencies (`_js_radius`, `_js_radius_kv_groups`, `_drop_bos_and_renorm`, `EPS`) come from `scripts.diagnose_inter_head_disagreement`, imported read-only exactly as `collect_ace_matrix` already imports from it. Do not copy those four in.

**Panel surface:**

- `KV_TENSION_METRICS: Tuple[str, ...]` — the four names, in the patch's order.
- `make_kv_tension_cells(steps, layers=None) -> List[PanelCell]` — cells only for the KV metrics, using `SEAL.ATTENTION_FAMILY` and `SEAL.ATTENTION_LAYERS` so labels match sealed conventions and `SEAL._cell_label` parses them.
- `score_kv_cell(cell, caps, n_kv_by_layer) -> Optional[float]` — the dispatcher, mirroring the patch's `_compute_attention_score` branch: resolve `n_kv` by layer, return `None` if absent, dispatch by metric name, return `None` for an unknown metric.

**Forbidden in D1:** importing `pri_calibrator` for anything but read-only constants and helpers; redefining any sealed metric; adding these cells to `ATTENTION_PANEL*` or to CC's unified panel; introducing a CLI flag on the sealed calibrator.

## D2 — an inert, opt-in hook in `collect_ace_matrix`

`confluence_calibrator.py` is on the **registered BENCH path**. The hook must be provably inert when unused.

Add two keyword-only parameters, both defaulting to `None`:

```python
def collect_ace_matrix(..., extra_cells=None, extra_scorer=None):
```

Semantics:

- When both are `None`, **every existing code path, column order, and output value is unchanged.** This is the load-bearing property of D2.
- When supplied, `extra_cells` columns are **appended after** the sealed panel's columns, never interleaved — so existing column indices are untouched and any consumer indexing by position still reads the same cell.
- Scores come from `extra_scorer(cell, sample_caps, n_kv)` computed on the **same `sample_caps` snapshot** the sealed panel used, in the same iteration — not a second capture pass. A second pass would be a different measurement wearing the same name.
- Keep the KV cells **out of** the `panel` list handed to `SEAL._compute_panel_scores_for_sample`. The sealed scorer must never be asked to evaluate a metric it does not know; read its unknown-metric branch and confirm before wiring.
- Record the extra cells in whatever cell-label/manifest metadata the matrix already carries, so a matrix that contains KV columns is self-describing and can never be mistaken for a sealed 21-cell one.

**Forbidden in D2:** changing any default; reordering existing columns; altering the capture path selection; touching sign-lock, OOB, or selection code; modifying `sealed_selector.py`.

## D3 — contract tests, ported

Port all 8 tests from the patch into `test_kv_tension_panel.py`, placed beside the module per CC convention. They are pure numpy and need no model:

`test_kv_tension_panel_has_twenty_four_cells` · `test_kv_tension_panel_includes_default_cells` · `test_kv_tension_metric_names` · `test_js_within_kv_groups_detects_inside_group_tension` · `test_js_within_kv_groups_zero_for_mha` · `test_js_kv_tension_ratio_detects_between_group_split` · `test_js_kv_tension_ratio_undefined_for_mha` · `test_js_within_kv_groups_no_bos_uses_trimmed_distribution`

Adapt the panel-shape assertions to the new surface (`make_kv_tension_cells`) rather than the t0 `ATTENTION_PANEL_KV_TENSION` constant, but **keep the numeric contracts identical** — the MHA-zero, MHA-undefined, and BOS-trimming cases are the whole point of the suite.

Add one test the patch did not have: **`extra_cells=None` leaves the panel and column count identical to the current behavior** (assert on the constructed panel/labels, no model forward).

## D4 — documentation

Update `exploratory/attention-kv-tension/README.md`: the "Open build task" section becomes a pointer to the live module, with the patch retained as historical provenance and still described as unapplied. Add a short note to `exploratory/README.md`. State in both that the lane remains `[PILOT RUN — NO-PROMOTE]` and that a fresh registration is required before any new run.

**Do not** edit `PRE_REGISTRATION_DRAFT.md`. It is a frozen pre-run document; the README carries the verdict.

## Acceptance criteria — executor commands, NOT run by Codex

```bash
cd ~/Documents/commit-confluence

# B1 — the sealed archive is untouched. MUST print nothing, and MUST stay clean.
cd ~/Documents/t0-morphology-furnace && git status --porcelain --untracked-files=all

# B2 — contract tests pass.
cd ~/Documents/commit-confluence && .venv/bin/python -m pytest test_kv_tension_panel.py -q

# B3 — inertness: the diff to confluence_calibrator.py is additive and default-off.
git diff HEAD~1 HEAD -- confluence_calibrator.py

# B4 — an existing BENCH analysis still imports and runs unchanged.
.venv/bin/python -c "import confluence_calibrator as c; import inspect; \
  print(inspect.signature(c.collect_ace_matrix))"
.venv/bin/python -m pytest stage_b/test_verify_bench_provenance.py -q

# B5 — the patch is still unapplied and still present as provenance.
git log --oneline -1 -- exploratory/attention-kv-tension/t0-patch/
```

**B1 is the one that matters.** If `t0-morphology-furnace` is dirty after this work, the port went the wrong way — stop and report rather than reverting quietly, because how it got dirty is the finding.

**B4 is the second.** `collect_ace_matrix` feeds registered BENCH artifacts. If its behavior changes with the new parameters absent, the hook is not inert and D2 must be redone.

## Non-goals

- No new runs, no new numbers, no panel promotion.
- No edits to `t0-morphology-furnace`, ever, including applying the patch there.
- No changes to sealed profiles, manifests, registered analysis paths, or `sealed_selector.py`.
- No amendment to the 2026-06-09 pre-registration.
- No `git tag`, `git push`, `pip install`, or test execution by Codex.

## Open decision for MK — not blocking D1–D3

`commit-confluence/vendor/t0_core/` already holds a vendored copy of parts of the t0 core (including `exploratory/shadow-ambiguity/`). Once t0 becomes an installable pinned package (`t0-pkg-v0.1.0`, per `wiki/repo-standalone-workorder-2026-07-25.md`), that vendor tree and the `CONFLUENCE_T0_REPO` `sys.path` injection both become redundant. Consolidating them is a separate pass — worth doing, but it touches the registered BENCH import path and should not ride along with this port.
