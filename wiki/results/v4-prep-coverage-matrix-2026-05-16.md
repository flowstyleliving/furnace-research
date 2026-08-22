# v4 Prep — Panel-Cell Coverage Matrix (2026-05-16)

**Status:** 🟡 **Pipeline in flight** — populated rows arrive as the calibrator sweep lands per-model profiles. Re-run [`scripts/build_v4_coverage_matrix.py`](../../../Documents/PRI_at_commitment/scripts/build_v4_coverage_matrix.py) any time after a new profile lands; output is idempotent.

This is the data substrate for [the v4 play sprint](../../../.claude/plans/elegant-meandering-mochi.md) — every cell on every model on every distribution scored, side-by-side. Steps 2 (RAUQ + SinkProbe baselines), 3 (TriviaQA factual rung), and 4 (causal probe) all read from this matrix.

> ⚠️ **t=0 caveat ([[step0-belief-readout-2026-05-17]], 2026-05-17):** every cell in this 621-row matrix is `gen_step=1`. The belief-readout panel **re-grounds the commit-step *premise*** (a discriminative t=0 logit locus exists; Mistral-Nemo anchor 0.99 passed) but the frozen pre-reg bars this from validating these specific attention numbers — for CoT-tuned models `gen_step=1` is a reasoning-preamble token, and the cells still need re-measurement at the logit-defined locus. **Phi-3.5-mini is Low-decidedness-for-M at t=0** (eligible_cov 0.185) — tension vs its Step-1 "clean trustworthy" status.

---

## Where things live

| Artifact | Path | Notes |
|---|---|---|
| 🧮 **Calibrator sweep** | `experiments/v4-prep-calibrator-sweep/2026-05-16/run-01/` | One subdir per panel variant; pipeline progress in `pipeline.log` |
| 📊 **Descriptive panel** | `experiments/inter-head-disagreement/2026-05-15/run-03/` | n=200 ANLI R1, fp32-fixed wrapper; per-model CSV + log |
| 📂 **Source data** | `experiments/anli-sweep/2026-05-15/run-02/anli_R1_seed20260513_n100.jsonl` | 200 rows, 100/class, pinned slice |
| 📋 **Auto-built CSV** | `experiments/v4-prep-calibrator-sweep/2026-05-16/run-01/coverage_matrix.csv` | Built by `scripts/build_v4_coverage_matrix.py`; safe to re-run anytime |
| 🔧 **Populator script** | `scripts/build_v4_coverage_matrix.py` | Re-runnable; tolerates partial sweeps |
| 🚀 **Pipeline orchestrator** | `scripts/run_v4_step1_pipeline.sh` | Phases 1-4: invariance probe → panel → v_norms calibrator → multistep calibrator |

---

## Schema (CSV columns)

| Column | Meaning |
|---|---|
| `model` | Model slug, e.g. `mlx-community/Qwen2.5-7B-Instruct-4bit` |
| `panel` | `v_norms` (21 cells) OR `multistep` (48 cells) |
| `gen_step` | 1 (single-step + v_norms variants) OR 1-4 (multistep variant) |
| `layer` | `final` / `mid` / `last_minus_1` |
| `metric` | `js` / `js_kv_groups` / `js_no_bos` / `bos_mass` (weight-based) + `v_norm_bos` / `v_norm_max` / `v_norm_lastq_weighted` (SinkProbe-style, v_norms panel only) |
| `auroc` | In-sample direction-locked AUROC on n=200 ANLI R1 |
| `sign` | +1 or −1 — the sign the calibrator locked from the calibration data |
| `n_eval` | Samples with finite metric value (lower = model EOS'd or metric NaN'd) |
| `oob_median` | OOB nested-bootstrap median AUROC ⚠️ **only on the winner row per panel** |
| `oob_ci_lo` / `oob_ci_hi` | 95% OOB CI bounds (winner row only) |
| `winner_stability` | Fraction of bootstrap resamples picking this same cell as winner (1.0 = always) |
| `warnings_count` | Number of deployability warnings emitted by the calibrator |
| `is_winner` | `TRUE` if this cell is the calibrated winner of its profile |
| `profile_path` | Path to the source `CalibrationProfile` JSON |

## Expected row count

| Panel | Cells/model | Models | Rows |
|---|---|---|---|
| v_norms | 3 layers × 7 metrics × 1 step = 21 | 9 | 189 |
| multistep | 3 layers × 4 metrics × 4 steps = 48 | 9 | 432 |
| **Total** | | | **621 rows** |

(Note: weight metrics at gen_step=1 appear in both panels — 12 cells × 9 models = 108 cells with duplicate (model, layer, metric, step) tuples across the two panels. That's intentional — duplicate is a free reproducibility check.)

---

## Per-(model, panel) winners

🟢 _Phase 3 (V-norm sweep) populated at \~05:52 PDT 2026-05-16. Phase 4 (multistep) pending._

### V-norm panel (gen_step=1, all 9 models)

| Model | Panel | Winner cell | AUROC | sign | OOB median | OOB CI | Stability | Warnings |
|---|---|---|---|:--:|---|---|---|---|
| Llama-3.2-3B-Instruct-4bit | v_norms | mid_js_no_bos @ step 1 | 0.6827 | −1 | 0.6554 | [0.5097, 0.7521] | 0.7300 | 0 |
| Mistral-7B-Instruct-v0.3-4bit | v_norms | last_minus_1_bos_mass @ step 1 | 0.7581 | −1 | 0.7279 | [0.6300, 0.8127] | 0.4150 | 1 |
| Mistral-Nemo-Instruct-2407-4bit | v_norms | final_js @ step 1 | 0.8001 | −1 | 0.7744 | [0.6636, 0.8517] | 0.6650 | 1 |
| Phi-3.5-mini-instruct-4bit | v_norms | last_minus_1_js_no_bos @ step 1 | 0.7736 | +1 | 0.7739 | [0.6670, 0.8581] | 0.9150 | 0 |
| Phi-4-mini-instruct-4bit | v_norms | final_js_kv_groups @ step 1 | 0.7453 | +1 | 0.7202 | [0.6012, 0.8037] | 0.4250 | 1 |
| Qwen2.5-7B-Instruct-4bit | v_norms | last_minus_1_js_no_bos @ step 1 | 0.8169 | +1 | 0.8179 | [0.7027, 0.8903] | 0.9800 | 0 |
| Qwen3-1.7B-4bit | v_norms | last_minus_1_js @ step 1 | 0.6390 | +1 | 0.5872 | [0.4436, 0.6808] | 0.4750 | 3 |
| Qwen3-8B-4bit | v_norms | last_minus_1_js_kv_groups @ step 1 | 0.8145 | −1 | 0.8033 | [0.6672, 0.8811] | 0.8950 | 0 |
| gemma-3-4b-it-4bit | v_norms | mid_v_norm_lastq_weighted @ step 1 | 0.7783 | +1 | 0.7599 | [0.6635, 0.8545] | 0.6250 | 1 |

🧭 **Headline reads (Phase 3 only):**
- ✅ **8/9 OOB CI excludes 0.5** (only Qwen3-1.7B at [0.44, 0.68] is borderline — smallest model in panel, expected weakness)
- 🌍 **Layer distribution**: last_minus_1 wins on 5/9, final on 2, mid on 2 → `last_minus_1` dominates the panel, NOT `final` as the original descriptive panel implied
- 🪤 **Only 1 of 9 winners is a V-norm cell**: gemma-3-4b picks `v_norm_lastq_weighted` (the SinkProbe-shaped feature). The other 8 stick with weight-based metrics — SinkProbe's value-norm refinement doesn't dominate on our panel at single-step
- 🌀 **Mistral-7B winner is `bos_mass` sign=−1**: *low* BOS mass predicts contradiction. Counter-intuitive vs naive SinkProbe ("sink dominance → hallucination"). Sign is locked from calibration data → real for ANLI R1 + Mistral 7B specifically
- ⚠️ **5/9 winners fire `winner_unstable`** (stability < 0.70): Mistral-7B 0.42, Phi-4 0.43, Qwen3-1.7B 0.48, gemma 0.63, Mistral-Nemo 0.67 → the calibration-pivot lesson holds: each model's specific cell choice is noise-driven at this n, even when *some* cell clearly wins

### Multistep panel (gen_step ∈ {1,2,3,4}, all 9 models)

🟢 _Phase 4 (multistep sweep) populated at \~07:45 PDT 2026-05-16. Pipeline complete; full 621-row matrix on disk._

| Model | Panel | Winner cell | AUROC | sign | OOB median | OOB CI | Stability | Warnings |
|---|---|---|---|:--:|---|---|---|---|
| Llama-3.2-3B-Instruct-4bit | multistep | last_minus_1_bos_mass @ step 3 | 0.6947 | −1 | 0.6396 | [0.5116, 0.7596] | 0.4050 | 1 |
| Mistral-7B-Instruct-v0.3-4bit | multistep | 🚨 last_minus_1_js @ step 3 | 0.9000 | −1 | 0.5000 | [0.0000, 1.0000] | 0.2200 | **40** |
| Mistral-Nemo-Instruct-2407-4bit | multistep | final_js @ step 1 | 0.8001 | −1 | 0.7744 | [0.6615, 0.8471] | 0.6650 | 1 |
| Phi-3.5-mini-instruct-4bit | multistep | last_minus_1_js_no_bos @ step 1 | 0.7736 | +1 | 0.7739 | [0.6670, 0.8581] | 0.9150 | 0 |
| Phi-4-mini-instruct-4bit | multistep | final_js_kv_groups @ step 1 | 0.7453 | +1 | 0.7193 | [0.5887, 0.8037] | 0.4200 | 1 |
| Qwen2.5-7B-Instruct-4bit | multistep | last_minus_1_js_no_bos @ step 1 | 0.8169 | +1 | 0.8175 | [0.6889, 0.8903] | 0.9750 | 0 |
| Qwen3-1.7B-4bit | multistep | last_minus_1_js @ step 1 | 0.6390 | +1 | 0.5659 | [0.4689, 0.6535] | 0.1750 | 3 |
| Qwen3-8B-4bit | multistep | last_minus_1_js_kv_groups @ step 1 | 0.8145 | −1 | 0.8041 | [0.6700, 0.8847] | 0.9100 | 0 |
| gemma-3-4b-it-4bit | multistep | last_minus_1_js @ step 1 | 0.7684 | +1 | 0.7420 | [0.6453, 0.8358] | 0.4500 | 1 |

🚨 **Mistral-7B multistep alarm**: `last_minus_1_js @ step 3` shows AUROC=0.90 **but** OOB median = 0.50, CI = [0.00, 1.00], stability = 0.22, and **40 warnings fired**. The calibrator's safety rails are working: this winner is post-selection-bias-inflated; honest deployment estimate is chance. **DO NOT CITE this cell.** Use the V-norm panel reading for Mistral 7B instead (`last_minus_1_bos_mass @ step 1`, OOB 0.73).

### Integrated cross-panel reading

🎯 **Step distribution of multistep winners**: 7/9 at step 1, 2/9 at step 3 (Llama 3B, Mistral 7B — both with weak OOB or warning storms), 0 at step 2 or 4. **The commit step (gen_step=1) is the natural attention-rupture moment; post-commit steps don't generally add new winning cells.**

🪞 **Cross-panel winner agreement** (same winner in both V-norm and multistep panels):
- 5/9 agree: Mistral-Nemo, Phi-3.5, Phi-4, Qwen 2.5, Qwen3-8B
- 4/9 differ: Llama 3B (mid → last-1@step 3), Mistral-7B (bos_mass step 1 → js step 3 ⚠️), Qwen3-1.7B (same cell, more warnings), gemma (v_norm → js)

🛡️ **Trustworthy winners** (OOB CI excludes 0.5, stability ≥ 0.70, BOTH panels agree): **Qwen 2.5, Qwen3-8B, Phi-3.5-mini** — 3 of 9.

🎯 **Load-bearing finding for Step 5 paper-scope synthesis**:
- 7+ different (layer, metric) combinations win across 9 models in each panel
- Cross-panel: gemma's preference depends on which metric set is offered (v_norm_lastq_weighted vs js)
- → **Per-(model, distribution) calibration is mandatory** — exactly the calibration-pivot lesson surfaced by the 2026-05-13 ANLI 33-profile sweep. This is the same lesson, now confirmed on the attention side.

🌍 **Layer distribution across both panels** (18 winners): `last_minus_1` = 11, `final` = 4, `mid` = 3. **`last_minus_1` dominates by 3×** — the descriptive panel's "no universal layer" framing under-sold this. There IS a preferred layer band; it's just *not* the final block as a naive reader of the v3 paper might assume.

---

## Reading guide for downstream steps

🪞 **Step 2 (RAUQ + SinkProbe baselines):**
- Filter to (`panel=v_norms`, `metric ∈ {bos_mass, v_norm_bos, v_norm_max, v_norm_lastq_weighted}`) — these are the SinkProbe-shaped cells.
- For each model, compare against RAUQ-AUROC + SinkProbe-AUROC (computed by `scripts/rauq_at_commit.py` and `scripts/sinkprobe_baseline.py` once they exist).
- Models flagged "sink-driven" in run-02 (Llama-3.2-3B, Mistral-Nemo) should have `bos_mass` or `v_norm_*` winning over `js_radius` variants — confirms the hypothesis.

🌊 **Step 3 (TriviaQA factual rung):**
- For each model, look up the winning (panel, layer, metric, gen_step) on ANLI R1 here.
- Re-run the calibrator on TriviaQA data with the same panel.
- Compare: does the same (layer, metric, step) win? Or does each (model, distribution) need its own operating point?

🩻 **Step 4 (causal probe):**
- Pick the cleanest profile: highest `oob_median`, lowest `warnings_count`, `winner_stability ≥ 0.90`. Mistral-7B is the likely target per the plan; verify via this table.
- Use the winner's profile JSON to extract the rupture direction (top-1 right singular vector of `√p_t · W_u` at the calibrated layer × step).

🧭 **Step 5 (paper-scope synthesis):**
- Count: how many models have a clean (`oob_ci_lo > 0.5`) winner?
- Cross-tabulate: do any (layer, metric) cells win on ≥3 models? If yes → potential paper claim. If no → confirm "per-(model, distribution) calibration is mandatory" framing.

---

## Notes + caveats

- ⚠️ **OOB stats only populate on winner rows.** The calibrator computes OOB nested bootstrap once per profile, evaluating the winner cell on out-of-bag samples. Non-winner cells have in-sample AUROC + sign only — that's by design (nested re-selection inside each resample is what's expensive).
- ⚠️ **Warnings count is profile-level, not cell-level.** A profile with `warnings_count > 0` may still have a clean winner — read the warnings list in the source JSON for context.
- ⚠️ **The 4 weight metrics appear in both panels.** The v_norms panel and multistep panel both include `js`, `js_kv_groups`, `js_no_bos`, `bos_mass` at gen_step=1. The numbers should match within precision noise — if they don't, something is broken (file an issue, don't paper over).
- 🔭 **No descriptive panel data in this matrix.** The 9-model descriptive panel (run-03) emits per-sample CSVs, not per-cell AUROCs. To get AUROC from a descriptive CSV, score the column against labels — that's how the calibrator scores cells, just under different framing. We're treating the calibrator profiles as the authoritative AUROC source.

## See also

- [v4-candidates #5](research-candidates.md#5-attention-cell-extension-to-pri_calibratorpy)alibratorpy) — the calibrator extension this matrix evaluates
- [results/inter-head-disagreement-2026-05-15](inter-head-disagreement-2026-05-15.md) — descriptive panel verdict (run-02, with run-03 corrigendum pending)
- [feedback/inter-head-prior-art-2026-05-15](../feedback/inter-head-prior-art-2026-05-15.md) — RAUQ + SinkProbe positioning notes
- [paper/pri-draft.tex §5.4](../paper/pri-draft.tex) — v3 paper's future-work paragraph naming v4 axes
