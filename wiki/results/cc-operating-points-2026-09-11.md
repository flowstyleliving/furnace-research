# CC operating points — what clearing the registered criterion actually buys

**Date:** 2026-09-11 · **Status:** `[DESCRIPTIVE — post-registration]` · **Moves no endpoint, bar or verdict.**
**Inputs:** banked score matrices and profiles only. No model run, no gate re-read.
**Code:** `commit-confluence/stage_b/analysis/operating_points.py` · **Artifact:** `stage_b/analysis/operating_points.json`
**Related:** [[paper/cc-draft]] §Operating points + Appendix A · [[references/commit-locus]] · [[results/cc-baselines-2026-09-10]]

---

## 🎯 The question

CC's registered criterion calls a deployment **deployable** when the out-of-bag AUROC 95% CI lower bound
clears 0.50. That certifies **ranking**, not behaviour at a threshold. Both external reviewers flagged the
word independently, and the manuscript already carries a caveat at its definition — but the paper contained
**no operating point at all**, so a reader could not tell what clearing the bar is worth. DeepSeek ranked
this its fourth-cheapest credibility fix; MK approved it as decision D2.

## 🔬 Method

For every deployment, replay the **registered** nested out-of-bag bootstrap with the **same draws** (row unit
for the sealed core, stem-cluster unit for BENCH). Inside each resample:

1. select the cell and lock its sign on the **in-bag** rows, exactly as the sealed selector does;
2. set an alarm threshold at the (1 − α) quantile of the **in-bag negative** scores;
3. apply cell, sign and threshold **unchanged** to the out-of-bag rows.

Positive class = label 1 (contradiction / wrong answer / hallucinated candidate). Panel = geometric-only
(26 of 29 signals), the confidence-free endpoint the headline uses. Like the paper's intervals, the result
describes the **selection procedure**, not a named signal.

## ✅ Verification — the check that makes it a replay, not a re-analysis

All **73/73** deployments reproduce their published profile exactly on **four** quantities: OOB AUROC median,
CI lower bound, resample count (2000 each), **and the in-bag winner tally**. The tally is the load-bearing one
— a per-cell histogram over 2000 resamples — so matching it means the draws and the in-bag selections agree,
not merely that two summary statistics coincide. ⚠️ An earlier version of the script compared only the median
and CI lower bound; **Astra's audit correctly objected that this cannot prove identical draws**, and the check
was strengthened before these numbers were accepted.

## 📊 Result

| Task | Cells | TPR @ 5% FPR | TPR @ 10% FPR (span) | realized FPR | Precision @ 10% prevalence |
|---|---|---|---|---|---|
| `anli_r1` (core) | 10 | 0.161 | **0.297** [0.19, 0.60] | 0.121 | 0.222 |
| `triviaqa_paired` (core) | 10 | 0.386 | **0.665** [0.25, 0.96] | 0.111 | 0.381 |
| `anli_r1_rep` | 8 | 0.499 | **0.629** [0.24, 0.87] | 0.102 | 0.406 |
| `triviaqa_paired_rep` | 10 | 0.492 | **0.670** [0.15, 0.99] | 0.101 | 0.422 |
| `halueval_qa` | 10 | 0.606 | **0.701** [0.29, 0.78] | 0.102 | 0.424 |
| `halueval_summarization` | 8 | 0.331 | **0.418** [0.29, 0.76] | 0.101 | 0.309 |
| `halueval_dialogue` | 9 | 0.247 | **0.379** [0.10, 0.71] | 0.104 | 0.279 |
| `anli_r2` | 8 | 0.155 | **0.254** [0.17, 0.51] | 0.106 | 0.211 |

Across all 73 deployments: TPR@10% median **0.513**, range **0.098–0.994**; projected precision median
**0.336**, range 0.094–0.521; realized FPR **0.099–0.138**.

## 🧭 Readings

- ✅ **Thresholds transfer.** Fitted on in-bag negatives, the realized out-of-bag false-alarm rate lands at
  0.099–0.138 against a 0.10 target. The threshold rule is not the weak link.
- 📉 **Detection is partial.** At a 10% false-alarm rate the selector flags a median of 0.25 (`anli_r2`) to
  0.70 (`halueval_qa`) of positive items. Best cell: **Mistral-Nemo on `triviaqa_paired_rep`, 0.994.** Worst:
  **Qwen3-1.7B on `halueval_dialogue`, 0.098.**
- 🚨 **Precision is the sharp end.** Every task is balanced 50/50, which flatters precision. Re-expressed at a
  10% prevalence, the same operating points give 0.21–0.42 per task — **most alarms would be false.**
- 🧪 **Internal consistency check.** The three weakest cells include all three whose intervals do not clear the
  criterion (the two sealed ANLI orphans and Qwen3-1.7B/`halueval_dialogue`). Nothing new, but it is what a
  faithful replay should show.

**The one-line consequence:** *clearing the registered discrimination criterion is not a usable alarm.* That
is now stated in the abstract, in a dedicated subsection, and here.

## ⚠️ Caveats, each disclosed in the artifact header

- 🧮 **`ci_lo_above_half` in the JSON is NOT the registered deployability endpoint** — it is the AUROC
  criterion alone, without BENCH's commitment-audit and control gates. Renamed after Astra flagged the
  original field name as misleading.
- 🔗 **One transductive detail, inherited from the registered pipeline:** the two fusion columns
  rank-transform over all rows before resampling, so they see out-of-bag **scores** (never labels). Not
  introduced by this analysis; now disclosed in the paper's appendix too.
- ➕ Threshold comparison is strict (`>`), so ties do not alarm; precision medians skip resamples that raised
  no alarm.

## 🔒 Scope

Descriptive and post-registration. Moves **no** endpoint: the sealed 18/20, A1 10/10, A2 6/10 and B1 7/20 are
untouched. Banked matrices only, so it cannot and does not re-read a gate.
