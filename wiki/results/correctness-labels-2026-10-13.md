# Correctness labels — do the detector signals catch the model's own errors? (2026-10-13)

**Status: [OPEN — descriptive, post hoc].** A re-analysis of saved data only (local CPU, $0, no
model run, no generation). Original outputs, labels and results are untouched; everything is
derived. Repo: `commit-confluence/exploratory/moe-detector-check/correctness/` (`CORRECTNESS.md`
holds the full method, tables and data gaps).

Related: [[results/moe-detector-check-2026-10-13]] (the scores this re-reads),
[[results/router-pilot-2026-10-08]] (addendum), [[results/verdict-baseline-2026-10-10]] (attention
beyond the emitted answer, for the dataset label).

## The question

MK asked to get the labels right before any code tour or layer-hook change. Did earlier scores
measure **error detection** (flagging the model's own wrong answers) or something else?

## What the earlier target was — verified

**The dataset class label, not answer correctness.** The ANLI data file holds only `prompt` and
`label`; its manifest reads `0: entailment - YES, 1: contradiction - NO`. The sealed loader
(`pri_calibrator.py:516`) reads `label` directly, and the detector adapter passes it unchanged to
the selector. The model's committed token is recorded but never enters the target. The router pilot
uses the same field, and its own limits text says so. HaluEval uses the same convention: 0 means the
proposed answer is supported (YES), 1 means it is hallucinated (NO).

## Derived labels

One CSV per saved run, aligned row for row to the saved signals. Columns cover the dataset label,
the correct answer, the committed token, the parsed answer (YES / NO / INVALID), and correct and
error. Every alignment check passed: data hashes, row order, expected answer against label, and token
sets. INVALID answers get a null correctness and are excluded and counted. Unusable runs (the smoke
run, and Qwen3-30B-A3B with 0 extracted rows) are listed, not labelled.

| Run | Accuracy | Errors |
|---|---:|---:|
| Granite-3.1-1B-A400M | **0.405** (worse than a coin) | 119/200 |
| Qwen3-1.7B | 0.645 | 71/200 |
| Qwen1.5-MoE-A2.7B-Chat | 0.735 | 53/200 |
| OLMoE-1B-7B, ANLI | 0.562 | 85/194 (6 invalid) |
| OLMoE-1B-7B, HaluEval | 0.695 | 61/200 |

## Results

- 🚨 **Against the model's own errors, no model meets the bar.** These come from the unchanged sealed
  selector, error labels, 2,000 bootstraps, with shuffled controls passing:
  - Granite: 0.517 [0.393, 0.618].
  - Qwen3-1.7B: 0.475 [0.356, 0.582].
  - Qwen1.5-MoE: 0.585 [0.398, 0.710]; geometric-only 0.523.
  The class-target scores for the same models were 0.633, 0.605 and 0.710.
- 🗳️ **The class scores are strongly associated with the model's own answer.** Cells predict the
  model's answer at AUROC 0.955 (Granite, a readout cell that sees the answer token), 0.982
  (Qwen3-1.7B, `final_js`) and 0.896 (Qwen1.5-MoE, `final_js_no_bos`). An answer-only predictor
  scores a class AUROC equal to the accuracy (0.405 / 0.645 / 0.735). The Qwen class scores sit
  close to that: 0.654 against 0.645, and 0.730 against 0.735. The original winners swing in opposite directions within the two classes, for
  example 0.09 and 0.84 for Qwen3-1.7B. That is the signature of tracking the answer. Within one
  answer group they are near chance, apart from one in-sample 0.73 among Qwen1.5-MoE's NO answers,
  where `surprise` also gives 0.74. That needs an out-of-sample test. The supported claim is narrow:
  none meets the stated error-detection criterion, not that error signal is absent in general.
- 🎚️ **The only error signal near its null is the model's confidence.** Qwen1.5-MoE's
  committed-token `surprise` reads 0.640 against a best-of-27 null of 0.639. OLMoE's output entropy
  reads 0.600 (null 0.599) on ANLI and 0.641 (null 0.600) on HaluEval.
- 🔀 **Router pilot: no router or attention family cleared its null for OLMoE's own errors at n=200 (underpowered; see [[results/harness-vs-signal-2026-10-13]]).** The best family
  scores sit under their nulls on both tasks. The pilot's HaluEval 0.832 / 0.904 are class
  discrimination of the proposed answer.

## What this changes

- **MoE detector check.** Qwen1.5-MoE's "meets" is a task-class result only. Against its own
  errors, no MoE model and no dense control meets it. The instrument checks are unaffected.
- **Router pilot.** The STOP stands and is strengthened. The "HaluEval router signal real and
  stable" bullet is class discrimination.
- **CC / ACE / BENCH panels: same label convention, not re-scored.** The verdict baseline tested
  attention beyond the emitted answer for the class label only. Whether the published panels detect
  the model's own errors is untested.

## Data gaps

- **No continuous verdict.** `P(YES) − P(NO)` and top-token margins were not saved in the
  detector-check runs, so the confidence baseline is committed-token `surprise` only.
- **BENCH is buildable but not done.** The 81 banked BENCH matrices save `gen_token_ids`, so
  correctness labels are buildable there. That needs each model's tokenizer to decode the ids; it is
  local and needs no generation.
- **Wide intervals.** n = 200 per model gives intervals of about ±0.12 on the error target.
- **Approximate HaluEval null.** The permutation null ignores the stem pairing.

## Open decisions for MK

- Whether to build correctness labels for the 81 BENCH cells and re-score the CC panels against
  model errors. That re-reads published claims.
- Whether the detector's deployment target should become error detection given the answer. That
  would mean registering an error-label endpoint, with confidence (`surprise`, `P(YES) − P(NO)`)
  as the baseline to beat.
