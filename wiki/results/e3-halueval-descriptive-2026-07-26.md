# E3-HaluEval descriptive label-cost sweep — knee at 150 labels (2026-07-26)

**Status: DESCRIPTIVE / POST-HOC — not a registered endpoint.** The ten `halueval_qa` matrices already existed and are published, so this cannot be blind-confirmatory; it supplies a label-cost *estimate* and cannot upgrade any BENCH headline claim. Spec frozen and committed **before execution**: `commit-confluence/stage_b/E3_HALUEVAL_DESCRIPTIVE_SPEC.md` @ `fde0349` (sha256 `b525a0c4…ed69ed`). Results artifact: `stage_b/profiles_bench/E3_HALUEVAL_DESCRIPTIVE.json` @ `cdf7e87` (pushed).

## Question

BENCH A1 calibrated each model on the full 1000 HaluEval-QA rows — an upper bound with no lower bound; the papers truthfully said HaluEval label cost was **unmeasured** (the sealed E3 only ever ran on ANLI/TriviaQA, budgets {50,100,150}, curve still rising at 150). This sweep starves the production calibrator on the existing matrices at budgets **{50, 100, 150, 300, 500}** (repeats 10, nboot 1000, seed 20260613 — the sealed E3 convention) with the Amendment-A2 **stem-aware** draw (complete two-row stems; `subsample_unit="stem"` confirmed on every cell).

## Result — a measured knee at 150, the thing the sealed tasks never showed

**All ten models reach 1.0 subsample deployability (10/10 repeats pass the OOB CI-lo > 0.5 gate, both full-panel and geometric) by 150 labels, and stay flat at 1.0 through 300 and 500.** Flat across consecutive budgets is exactly the spec's pre-committed knee criterion. 9/10 are already at 1.0 by 100 labels.

Fraction of repeats deployable (full panel / geometric-only where they differ):

| model | 50 | 100 | 150 | 300 | 500 |
|---|---|---|---|---|---|
| Llama-3.1-8B | 0.9 | 1.0 | 1.0 | 1.0 | 1.0 |
| Llama-3.2-3B | 0.9 / 0.8 | 1.0 | 1.0 | 1.0 | 1.0 |
| Mistral-7B | 0.7 | 1.0 | 1.0 | 1.0 | 1.0 |
| Mistral-Nemo | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 |
| Phi-3.5-mini | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 |
| Phi-4-mini | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 |
| Qwen2.5-7B | 0.6 / 0.5 | 1.0 | 1.0 | 1.0 | 1.0 |
| **Qwen3-1.7B** | **0.2 / 0.0** | **0.9 / 0.8** | **1.0** | 1.0 | 1.0 |
| Qwen3-8B | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 |
| gemma-3-4b | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 |

## Interpretation

- 💰 **HaluEval-QA is a descriptively *cheaper* calibration target than the sealed tasks** — roughly 100–150 labels per model fixes both cell and orientation, versus the sealed picture at 150 (mean geometric deployability 0.79; 4/18 deployments not stable, curve still rising, no larger budget measured). Plausible mechanism: A1 signal strength is high here (CI-lo 0.67–0.90) and stronger separations certify with fewer labels.
- 🎯 **The prediction held**: the last model to certify is exactly the cohort's weakest A1 cell (Qwen3-1.7B, CI-lo 0.6705) — the label-cost ordering tracks signal strength.
- 🔄 **Sign-flippers are not label-hungry**: Phi-3.5 (behavioral outlier + A2 inversion) is perfect at 50; Qwen2.5-7B and both Mistrals certify by 100. Orientation is cheap to fix per-model; it just cannot be *transferred* (the A2 verdict stands untouched).
- 🚧 **Limits**: subsample statistic on existing registered matrices, not fresh data; comparisons to sealed E3 are cross-task/cross-n descriptive; a registered label-cost endpoint would need a new registration. Cannot upgrade A1/A2/B1.

## Execution note

First execution was interrupted after 6 cells; those six results were recovered verbatim from its log and merged with a fresh run of the remaining four. The merge is exact because `label_efficiency` seeds per (budget, repeat) as `RandomState(seed + 1000·budget + r)`, independent of cohort composition — recorded in the JSON's `execution_note`.

## Cross-refs

[[results/e3-stem-aware-2026-07-14]] (sealed E3 + the retired "~150–200" framing) · [[results/bench-a2-signflip-2026-07-22]] (A1/A2 verdicts) · `wiki/paper/cc-draft.tex` §"Label cost on the new task" (merged paper carries this estimate, labeled descriptive).
