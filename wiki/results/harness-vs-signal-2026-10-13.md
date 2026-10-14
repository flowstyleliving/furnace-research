# Harness or signal? Why the signals catch the model's own errors poorly (2026-10-13)

**Status: [PRE-REGISTERED ANALYSIS — verdict CAN'T TELL by the pre-stated rule; descriptive
findings below, each flagged supported or tentative].** Saved data only: no generation, no paid
run, no preregistered file edited.

- **Plan:** committed before any outcome (`commit-confluence` `7cb056b`), with amendments A1
  `069acbb` and A2 `5455696`.
- **Scripts:** frozen `d29a2e4` after a DeepSeek pre-run audit. Codex was at its usage limit.
- **Repo:** `commit-confluence/exploratory/moe-detector-check/correctness/harness_vs_signal/`
  (`HVS_RESULTS.md` holds the interpretation, `HVS_REPORT.md` the full tables).

Builds on [[results/correctness-labels-2026-10-13]].

## The question

MK asked whether the poor error detection in the MoE lanes comes from the **harness** (the
one-token YES/NO interface, small n, low task accuracy) or from the **signal itself**. The
analysis had to be robust enough to count as evidence:
- decision criteria fixed in advance;
- bootstrap CIs on every AUROC and every difference against confidence;
- permutation nulls and Holm correction;
- signal and layer chosen on held-out folds only;
- power per test;
- sensitivity checks.

## Method in brief

- 🧮 **Data.** 60 cells:
  - 3 detector-check cells (torch, ANLI, n=200);
  - 2 OLMoE router-pilot cells × 2 families (n=200);
  - all 53 banked BENCH cells (MLX 4-bit, 10 dense models, 6 tasks, n=1,000).

  The groups are never pooled. BENCH correctness labels were newly derived by decoding each saved
  first token with that model's own tokenizer.
- 🔤 **Parsing fix (A2).** Mistral-7B's tokenizer splits `YES` into `▁Y` + `ES`, so its first
  token `Y` now counts as YES. Without this, 43–89% of its rows would have been dropped.
- 🎯 **Test.** 5-fold stem-grouped cross-validation. Each training fold picks one signal and sign;
  the held-out folds score it. The comparison is against confidence: the committed token's
  surprise, with its sign fixed in advance.
- 📊 **Primary endpoint E1.** The answer-partialled Δ, in which signals and confidence are
  standardized within the model's answer group, so pure verdict-tracking scores 0.5.
- 📏 **Inference.** A 2,000-draw stem-cluster bootstrap and 1,000 full-pipeline permutations;
  Holm within each group. MD-Δ and MD-AUC are reported at 80% power.

## Verdict by rule: CAN'T TELL

- **9 informative cells.** These are BENCH cells with ≥ 100 errors and ≥ 100 correct answers,
  accuracy 0.60–0.90, and powered for Δ. The SIGNAL verdict needs ≥ 10.
- **E1 significant in 2/9 (22%).** The HARNESS verdict needs ≥ 25%. One of the two
  (Mistral-Nemo summarization) reverses under the alternative confidence measure.

## What the data show

- 🔋 **The MoE-lane results are underpowered, not negative (supported).** At n = 200 the smallest
  detectable advantage over confidence is +0.15 to +0.20, and the smallest detectable AUROC is
  0.62–0.63. Not one of the seven tests is powered.
- 📉 **On ANLI the signals are usually worse than confidence at catching errors (descriptive;
  tentative as a verdict).** Across 16 BENCH ANLI cells (n = 1,000 each; only 2 meet the plan's
  MD-Δ ≤ 0.05 power rule) there are 0 wins, and Δ's CI lies below zero in 11/16.
  The median Δ is −0.094 (R1) and −0.045 (R2). Within-answer analyses add nothing. The MoE lanes
  ran on ANLI.
- 📈 **On HaluEval summarization and QA there is an error signal beyond confidence in several
  models (supported for those cells).**
  - E1 is Holm-significant in 12/53 BENCH cells.
  - **10 of them hold** against the alternative confidence measure and a second fold seed (that
    combination is post hoc):
    summarization ×4, QA ×3, TriviaQA ×2, dialogue ×1.
  - Prompt length alone does not explain them (0.50–0.58, against 0.65–0.88).
  - In 4 of the 12 the fixed-sign confidence is inverted (more confident when wrong).
- 🗳️ **The one-token interface matters, but only in part.** The signals track the model's verdict:
  the median AUROC of the pooled pick for predicting the answer is 0.69 across BENCH. In-sample
  best cells reached 0.90–0.98 in the detector check (earlier analysis). That is supported. Partialling the verdict out does not help on average (median
  −0.026), also supported. **Pooling over the two answers can hide a within-answer signal**; that
  is post hoc and tentative. Among OLMoE's YES answers on HaluEval, router entropy at layer 3 reads
  0.83 and `final_js` at layer 9 reads 0.88, against confidence 0.52, both Holm-significant. These
  signals read the input class (a hallucinated candidate), which equals the error among YES answers.
- 🎚️ **Accuracy moves confidence, not the signals (supported).** Across BENCH, Spearman ρ against
  accuracy is +0.54 (p 3 × 10⁻⁵) for confidence AUROC and +0.19 (p 0.17) for signal AUROC. Low
  accuracy weakens the baseline.

## Answer

**For the MoE result: can't tell yet, because the harness (n = 200) is too weak.** In well-powered
dense data the answer depends on the task:
- **ANLI** (the MoE lanes' task): the data point to the **signal** as the limit, since it is
  usually worse than confidence. This is descriptive, not the pre-registered SIGNAL verdict.
- **HaluEval summarization and QA:** a real beyond-confidence signal exists in some models.

## Cheapest decisive next test (not launched)

- **Run** Qwen1.5-MoE and Granite through the existing detector on BENCH HaluEval-QA (n = 1,000);
  OLMoE would go through the router-pilot harness.
- **Save** P(YES), P(NO) and the margin; the wrapper change needs Codex and MK's approval.
- **Pre-register** E1 plus the within-answer endpoints, against both confidence definitions.
- **Cost:** about $0.7–1.2 per model on one A100, so about $3 in total. Needs MK's go-ahead.

## Deviations and caveats

- **Amendments.** A1 and A2 were committed before outcomes. The pre-run audit fixes were committed
  before outcomes too.
- **Post hoc.** S1 treats INVALID as its own answer group. Confidence inversion, prompt length, the
  robust-cell combination and the within-answer interpretation are post hoc.
- **Not pooled.** BENCH is MLX 4-bit and the MoE lanes are torch bf16; the groups are not pooled.
- **Audit.** A DeepSeek post-run fact check found three errors in the first write-up and two missing
  post-hoc labels. All are corrected here and in the repo. Codex was unavailable.
