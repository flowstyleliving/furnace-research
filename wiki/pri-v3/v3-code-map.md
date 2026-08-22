# v3 Code Map — Where to Edit

Status: `[HISTORICAL — v3 build complete]`.

> ⏳ **Snapshot of the PRI_at_commitment repo as of 2026-04-14, written to guide the v3 build (now done — v3 sealed 2026-04-23).** ⚠️ **The line numbers and file sizes here have drifted** — the repo has since grown the production calibrator/detector, IO plugins, ACE, and the v5–v8 branches, so `pri_v2_mlx_pipeline.py:684` etc. are no longer accurate. Use this only as historical context for *how* v3 was wired; `grep` the repo for the named functions (`PRIComputer`, `null_ratio_raw_and_energy`, …) rather than trusting the line numbers. For current repo orientation see [references/code](../references/code.md).

Concrete implementation index for the v3 build. Written 2026-04-14 against the PRI_at_commitment repo as it stood. All paths are under `/Users/msrk/Documents/PRI_at_commitment/`.

The plan at [pri-v3-plan](pri-v3-plan.md) is the *what*; this was the *where*.

## Surprising fact
`pri_metrics.py` is **mostly vestigial** — the actual PRI v2 computation lives inside `pri_v2_mlx_pipeline.py` in the `PRIComputer` class (line \~684). Don't put v3 metrics in `pri_metrics.py` expecting them to be wired up; they won't be. Put them on `PRIComputer` or extract `PRIComputer` into a new module first.

## File inventory (sizes)
| File | Lines | Role |
|------|------:|------|
| `pri_v2_mlx_pipeline.py` | 1797 | **Main entrypoint.** Config, generation loop, `PRIComputer`, analysis stage. |
| `model_adapters.py` | 693 | Per-model MLX adapter (forward pass, hidden hooks, unembedding). |
| `synthetic_trace.py` | 419 | Prefix + generation hidden-state / probability trace collection. |
| `synthetic_logic_loader.py` | 295 | 2×2 factorial puzzle generator. |
| `attention_contribution.py` | 147 | Attention-contribution-ratio signal (used in paper fig 5). |
| `pri_metrics.py` | 147 | `compute_pri`, `compute_cosine_distance`, SVD spectrum features — **mostly unused by v2 pipeline**. |
| `hidden_state_collector.py` | 85 | `HiddenStateCollector` class — `record(layer_idx, vector)` / `flush()`. |
| `config.py` | 43 | `UncertaintyConfig` dataclass, `DEFAULT_UNCERTAINTY_CONFIG`. |

## Critical call-sites

### 1. PRIComputer — where v3 variants get added
`pri_v2_mlx_pipeline.py:684–811`

- `fim_lowrank` (line **724**): already does `U, S, Vt = np.linalg.svd(A, full_matrices=False)` where `A = sqrt(p_s) * W_s`. Currently **discards `Vt[r:]`** (the null space) and **collapses `Vt[:r]` to a scalar** via `d2 = sum(S[:r]² * (Vt[:r] @ dh)²)`.
  - **v3 extension point.** Instead of collapsing, return `Vt[:r]` and compute `null_ratio = ||dh - Vt[:r]^T Vt[:r] dh|| / ||dh||`.
  - Note: the row-truncation to `support = min(max(256, rank*16), vocab)` means the SVD is **already on a subset of V**. The "null space" is only null relative to the top-probability rows. Document this limitation in methods.
- `compute_step` (line **763**): top-level per-step metric dispatcher. Takes `h_t, h_prev, p_t, S_t, alpha, topk_values, lowrank_values`. **Add `v3_rank_values` kwarg** and iterate to emit `null_ratio_rankR`, `pri_v3_null_bare_rankR`, `pri_v3_null_ratio_rankR`, `pri_v3_null_gated_rankR`, plus `fisher_energy_rankR` (= `sum(S[:r]²)/sum(S²)`).
- **`pri_v3_null_raw` / E17b HARP-style baseline — SHIPPED 2026-04-23.** Parallel path to `null_bare` that performs SVD on **raw `W_u`** (no `sqrt(p_t)` weighting). The shipped implementation (code anchors below) diverges from the original design-doc spec on two points:
  - **Rank-sweep parity, not energy-cutoff parity.** Emits `null_ratio_raw_rank{r}` + `raw_energy_rank{r}` at the **same rank sweep** as the Fisher-weighted path (`{1,2,3,4,5,8,13,16,21,32,34,55,64}`), so the E17b head-to-head is a direct per-rank `AUROC(fisher) − AUROC(raw)` test on identical dh. The 95%/99% energy cutoffs and HARP's r=256 can be read off the rank sweep post-hoc; not emitted as separate columns. Rationale: the E17b sealed gate (pri-v3-plan.md Amendments 2026-04-23) pins rank 1 for the head-to-head, matching the v3.1 rank pin.
  - **Basis computed via chunked `W_uᵀ W_u` + `eigh`,** not `np.linalg.svd`. Accumulates `W_uᵀ W_u` (d × d, float64) over chunks of W_u rows via the existing `OutputProjection.get_rows` (handles quantized + dense + tied-embed uniformly), then `np.linalg.eigh` recovers the top-k eigenvectors. Rationale: avoids materializing the full V×d W_u matrix in RAM (\~2 GB for Qwen 2.5's 152k × 3584 lm_head), and eigh on d×d is O(d³) ≈ seconds for d≈3000. Equivalent to top-k right singular vectors of W_u up to sign.
  - **Static per-model — cached on `OutputProjection._raw_svd_cache`.** One-time model-load cost (\~5–30s); per-sample cost is one matvec `Vt_raw @ dh`. Subsequent calls with k ≤ cached-k return a prefix slice (cache reuse verified by test 5 in `scripts/test_e17b_raw_svd.py`).
  - **Code anchors (shipped 2026-04-23):**
    - `OutputProjection.raw_right_singular_vectors(max_rank, batch=4096)` → `(Vt_top, S_top)` or `None`. `pri_v2_mlx_pipeline.py` (search: `def raw_right_singular_vectors`).
    - `PRIComputer.null_ratio_raw_and_energy(dh, rank_values)` → `{null_ratio_raw_rank{r}, raw_energy_rank{r}}`. Search: `def null_ratio_raw_and_energy`.
    - `PRIComputer.compute_step(..., v3_capture_raw: bool = False)` — wiring (search: `v3_capture_raw`).
    - `Config.v3_capture_raw: bool = True` — default on; `--no-e17b` launcher flag flips it off.
    - Precompute-at-model-load hook inside `run_experiment` (search: `E17b raw-W_u SVD cached`).
    - Checkpoint signature bumped: `v3_capture_raw` in `checkpoint_signature(config, model_name)` so flag flip invalidates stale parquets cleanly.
    - Unit test: `scripts/test_e17b_raw_svd.py` (6 bundles — numpy-SVD match, range+monotonicity, aligned/orthogonal dh, chunked=unchunked, cache reuse, compute_step flag parity).

### 2. Generation loop — where every-layer capture lands
`pri_v2_mlx_pipeline.py:630–662`

- The forward pass at line **648** returns `step_selected_hidden: Dict[str, np.ndarray]` — keyed by `"final" | "mid" | "quarter"`.
- Line **651** appends the hidden state to `gen_hidden[lname]` for each probed layer name.
- **v3 extension point.** Either:
  - (a) expand `layers_to_probe` to include every layer via a config schedule, or
  - (b) branch on step index: `if step <= 12: capture_all_layers(); else: capture_probe_layers()`.
- Recommend (b) — keyed on step count, matches user-specified capture schedule (steps 1–12, updated 2026-04-15).

### 3. Forward pass with hooks — where to broaden layer capture
`pri_v2_mlx_pipeline.py:522–577` (function `_forward_with_hidden` — search for "def _forward_with_hidden")

- Line **553**: `for li, layer in enumerate(layers):` — iterates all transformer blocks.
- `target_idx_to_name` (line **531**) decides which `li` gets recorded. Currently 3 names → 3 indices.
- **v3 extension point.** Extend `target_idx_to_name` to be a function of step index, or just record **all** layers into a separate dict `step_hidden_all` when the step-1-to-12 window is active.

### 4. Layer-index resolution
`pri_v2_mlx_pipeline.py:344–348` (`get_layer_indices`)

Currently hardcoded `{final: L-1, mid: L//2, quarter: L//4}`. For "4 probe layers" post-step-12, add `three_quarters: 3*L//4`. New helper: `get_all_layer_indices(n_layers) -> Dict[str, int]` returning `{"layer_0": 0, ..., "layer_{L-1}": L-1}` for the step-1-to-12 window.

### 5. Output projection — already provides W_u rows
`pri_v2_mlx_pipeline.py:357–450` (class `OutputProjection`)

- `get_rows(idx)` (search for method) returns `W_u[idx, :]` as numpy, handling quantized + dense + tied-embedding variants.
- `project(dh)` returns `W_u @ dh` = logit-space `z`.
- **v3 needs nothing new here** for Option A. For Option B (logit-lens per-layer eigenspace), you'd need layer-ℓ logits `W_u @ h_ℓ` followed by softmax — reuse `project()` + `safe_softmax` (line 128).

### 6. Config
`config.py` (43 lines total — read whole file).

Add to `UncertaintyConfig` (around the `lowrank_values` field):
- `v3_rank_values: Iterable[int] = (8, 16, 32, 64)`
- `layer_capture_schedule: Dict[str, str] = {"steps_1_to_12": "all", "steps_13_plus": "probe_4"}`
- `null_ratio_threshold_multiplier: float = 1.5` (for `argmin_depth` scoring — threshold = 1.5× per-sample *minimum* `null_ratio_ℓ`; flipped 2026-04-16 per E22 verdict, rising null_ratio = *less* informed, not more)
- ~~`null_raw_cutoffs`~~ / ~~`null_raw_extra_dims`~~ **superseded 2026-04-23.** Shipped implementation uses `v3_capture_raw: bool = True` in `Config` (see `pri_v2_mlx_pipeline.py`) and emits `null_ratio_raw_rank{r}` + `raw_energy_rank{r}` at the **same rank sweep** as the Fisher-weighted path. HARP's 95% / 99% cumulative-energy cutoffs and r=256 parity can be read off the rank-sweep columns post-hoc; not emitted as separate fields.

Also in `pri_v2_mlx_pipeline.py` near **line 82**: `layers_to_probe` default stays; add `probe_4_layers: List[str] = ["final", "three_quarters", "mid", "quarter"]`.

### 7. Parquet schema
Search `all_results.parquet` writes in `pri_v2_mlx_pipeline.py` (near the analysis stage, \~line 1100+). New columns per row:
- `layer_index` (int, 0 = embed, L-1 = final)
- `layer_normalized` (float, `li / (L-1)`)
- `null_ratio_rank{R}` for each R
- `fisher_energy_rank{R}`
- `pri_v3_{variant}_rank{R}`
- `null_ratio_raw_rank{r}` for each r in `v3_rank_values` (HARP-style static-SVD baseline; shipped 2026-04-23)
- `raw_energy_rank{r}` for each r in `v3_rank_values` (denominator = sum of σ² over all d eigenvalues of `W_uᵀ W_u`)

Current parquet is one row per `(sample, variant, step)`. v3 adds a `layer_index` axis. Decide: **wide** (new columns per layer) or **long** (new row per layer). Long scales better for every-layer; recommend long.

### 7b. Step-0 `h_prev` regression guard — already in place
The step-0 bug that inflated the paper's AUROCs is **fixed**. Conditional at `pri_v2_mlx_pipeline.py:1189–1191` binds `h_prev = trace["last_prefix_hidden"][layer_name]` when `step == 0` and `h_prev = trace["gen_hidden"][layer_name][step - 1]` otherwise. Audit checklist items 17–19 verify this binding. No new guard code needed for v3; just don't regress the conditional. (Earlier drafts of this section listed 6 defensive guards — removed 2026-04-15 after confirming the fix.)

### 8. Audit checklist v3 extension
`PRI_V2_PRE_RUN_AUDIT_CHECKLIST.md` (at repo root). Add §12:
- 12.1 `null_ratio` sign-invariance verified (feed `-V_topr` → identical result)
- 12.2 Rank consistency: `null_ratio` monotonic decreasing in r (by construction)
- 12.3 Fisher energy `ε(r)` monotonic increasing in r, `ε(vocab) = 1`
- 12.4 Layer index alignment: `layer_0` = post-embed, `layer_{L-1}` = final pre-norm output
- 12.5 `W_u` row support truncation (256-row floor) documented in paper methods
- 12.6 Logit-lens (Option B) numerical stability: `softmax(W_u h_ℓ)` never underflows to all-zero
- 12.8 HARP baseline (E17b): raw-`W_u` SVD cached once per model (not recomputed per step); `raw_energy_rank{r}` denominator is the sum of σ² over **all d eigenvalues** of `W_uᵀ W_u` (not just cached top-k — so `raw_energy_rank{d}` = 1.0 and intermediate ranks read as interpretable cumulative fractions against HARP's 95% convention); `V[:r]` shape `(r, d)`; `null_ratio_raw_rank{r}` numerically stable (no division by near-zero `||dh||`)
- **12.7 Step-0 `h_prev` source-binding assertion** (see §7b). `h_prev_source == "prefix_last"` at step 0 for every sample; `||Δh_step0|| / ||h_t|| < 10`; finite-check before any metric. This is the regression guard for the paper's inflation bug.

### 9. Smoke-test script (new file)
`scripts/smoke_test_model.py` — does not exist yet. Purpose: gate new-model adapters before n=50/cell commitment. Checklist per model:
1. Load via `model_adapters.py`
2. Forward pass on 1 short prompt — assert hidden state shape `[1, T, d]` and layer count
3. Capture every layer — assert no None, no NaN, dtype fp32 after cast
4. `OutputProjection.get_rows([0,1,2])` — assert shape `[3, d]`
5. Run 1 preflight puzzle — assert control accuracy = 1.0
6. Print: model name, n_layers, hidden_dim, vocab_size, adapter mode

Runs in <60s per model. Exit code 0 = cleared for full run.

### 10. Prereq 4 dry-run (new file)
`scripts/v3_capture_dryrun.py` — does not exist yet. Full assertion spec in [pri-v3-plan.md §Prerequisites.4](pri-v3-plan.md). Purpose: gate the shared production capture path before main-run launch. Closes H4 / H3 / H2 / M1 from Opus 4.7's 2026-04-18 review.

Assertion bundles (all must pass on Llama / Mistral / Qwen):
1. **Schema.** Required columns present, correct dtypes + shapes. Fail loud on any drop.
2. **Schedule.** Every-layer for steps 1–12; `probe_4` for steps ≥ 13. Row cardinality asserted.
3. **Provenance.** `h_prev_source == "prefix_last"` at step 0; `"gen_prev"` elsewhere. Hard fail on mix.
4. **Healthy tripwire.** `‖Δh_step0‖ / ‖h_t‖ < 10` per row; distribution logged; H3 note: replace `< 10` with measured `percentile(r_healthy, 99) · 2` once ≥ 3 healthy dry-runs exist.
5. **Fault-injection tripwire** (closes M1). Second pass with broken `h_prev` (zero-vector or `gen_prev` at step 0) — provenance OR tripwire must fire. If neither fires, the guard is cosmetic → dry-run fails.
6. **Finite checks.** `isfinite(h_t).all() and isfinite(h_prev).all()` per row.
7. **Consumer audit** (closes H2). Grep `pri_metrics.py` + `PRIComputer` variants for consumed columns; validation must cover exactly that set. Result written to `dryrun_report.json` under `consumer_audit`.
8. **Dict-collision** (closes H4). Capture store enforces write-once (`assert key not in store`); any duplicate-key write is a hard fail with key printed. Exercises the full step × layer key-space on first run.

Artifacts: `dryrun_report.json` + `dryrun_capture.parquet` under `PRI_at_commitment/experiments/v3-capture-dryrun/<date>/run-NN/` (auto-incremented per date). Exit `0` iff all 8 bundles pass on all three models.

## Environment
- Python: `/Users/msrk/Documents/PRI_at_commitment/.venv/bin/python`
- MLX, numpy, pandas, pyarrow all installed in that venv
- Pandoc/poppler NOT needed for build, only for vault PDF ingest

## Suggested edit order
1. Add `v3_rank_values` + capture-schedule fields to `config.py`.
2. Extract `null_ratio` computation as a standalone method on `PRIComputer` (reuses existing SVD in `fim_lowrank`).
3. Extend `compute_step` to emit v3 variants.
4. Modify the generation loop + `_forward_with_hidden` for step-conditional layer capture.
5. Update parquet schema to long-format with `layer_index`.
6. Extend audit checklist §12.
7. Write `scripts/smoke_test_model.py`.
8. Write `scripts/v3_capture_dryrun.py` and pass it green on all three primary models — this closes Prereq 4.
9. Smoke-test Qwen3-8B, Gemma-3-1B, Phi-3.5-mini.
10. Exploratory n=4 → confirmatory n=50 → analysis → LaTeX.

## What not to touch
- `synthetic_logic_loader.py` — 2×2 construction is validated; don't modify.
- `pri_metrics.py` — vestigial; leave alone unless you extract `PRIComputer` into it.
- `attention_contribution.py` — paper fig 5, unrelated to v3.
- `synthetic_trace.py` — trace collection is upstream of the pipeline; no v3 changes needed.
