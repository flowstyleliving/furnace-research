# Work order — do the Simpson's-paradox sites survive a fixed orientation? (2026-09-10)

_Status: **OPEN**, authored 2026-09-10. Pure re-analysis of banked parquets — no model run, no gate re-read, and it cannot move a sealed verdict._

## Goal

Decide whether `pri-draft.tex`'s **two Mistral Simpson's-paradox sites** are a real subgroup-mixing phenomenon or an artifact of fitting the AUROC sign separately in every cell.

## The objection, in one paragraph

Every AUROC in the paper is the oriented quantity `max(AUROC, 1−AUROC)`, with the sign fitted on that cell's own labels. Pooled and stratified cells therefore fit their signs **independently**. Under that rule `Δ_oriented` is **not a common estimand** across pool and strata: a pooled-negative / strata-positive pattern can be produced by the orientation choice alone, without any subgroup reversal of a fixed estimator. Raised by `deepseek-v4-pro` in the third-pass review, 2026-09-10.

⚠️ **The manuscript already states the confound as though it were the explanation.** §4.3 reads: *"the pooled 'Raw' verdict is a mixing artifact of two chain-length subgroups whose Fisher and Raw discrimination axes have **different orientations**."* If differing orientations are what generate the reversal, then "Simpson's paradox" is a description of the metric's behaviour, not of the data's.

## What is at stake

The two sites are load-bearing. They appear in the contributions list (§1), get their own table and figure (`tab:mistral`, `fig:mistral`), and supply the paper's largest single number — `Δ_cross = −0.575` at r=32, billed as *"the largest cross-stratum spread observed across all 156 cells."* One of them sits at the **sealed rank**.

## The test

For Mistral 7B, `2026-04-26/run-09`, gen_step=1, at ranks **1** and **32–34**:

1. Compute **unoriented** AUROCs for `null_ratio_post_rank{r}` (Fisher) and `null_ratio_raw_post_rank{r}` (Raw), pooled and per chain-length stratum. No folding at all.
2. Recompute `Δ` from those unoriented values and re-derive `Δ_cross`.
3. Repeat under a **single fixed orientation per (model, metric)** — sign chosen once on the pooled cell, then applied unchanged to both strata — which is the deployment-realistic rule and the one the production calibrator already uses.
4. Report all three views side by side: per-cell-fitted (current), unoriented, fixed-orientation.

Paired bootstrap CIs by the same protocol as the paper (1000 sample-level resamples, seed 20260423), so intervals stay comparable.

## What each outcome licenses

- ✅ **Reversal survives unoriented and fixed-orientation** — it is a real Simpson's reversal. Keep the framing; add a line reporting that it was checked under a fixed orientation, which strengthens it.
- ❌ **Reversal disappears under fixed orientation** — relabel throughout as **orientation-induced sign reversals**, not Simpson's paradox. Contributions list (§1), §4.3, `tab:mistral`, `fig:mistral` caption and the conclusion all need rewording, and `Δ_cross = −0.575` must be restated as a spread between differently-oriented statistics rather than a cross-stratum effect size.
- ⚠️ **Mixed** (one site survives, one does not) — report per site; do not generalise from the survivor.

## Guardrails

- 🔒 **Descriptive and unregistered.** Cannot upgrade, downgrade or otherwise move E17b, E18 or any sealed verdict. Those are defined on the pooled sealed cell and are untouched by this question.
- 🚫 **No model run and no gate re-read.** Banked parquets only. If a re-generation ever seems necessary, stop and file separately.
- 📏 Use the same bootstrap protocol as the paper; do not switch CI method mid-comparison.
- 🧊 Do not edit the manuscript until the result is in — the rewording depends on which outcome lands.

## Acceptance

1. A table giving, for r ∈ {1, 32, 34} × {pool, cl=2, cl=5}: unoriented AUROC and sign for Fisher and Raw, plus `Δ` under all three orientation rules, each with CI.
2. An explicit verdict per site: survives / does not survive / mixed.
3. If it does not survive, the exact list of manuscript locations needing rewording — §1 contributions, §4.3 body, `tab:mistral`, `fig:mistral`, conclusion.
4. Cheap by construction: the inputs are banked and local, so this is minutes of compute, not a run.

## Adjacent items deferred from the same review — same lane, lower priority

Both are §5.1 claims that are **asserted rather than shown**, and both were raised independently by more than one reviewer:

- 📌 **"Residualization absorbs the coordinate mismatch."** The only evidence offered is that the E18 verdict survived the `J_n` correction — but the magnitudes moved (Qwen 0.7445 → 0.6687), so absorption is not demonstrated. Either show it or soften to "was sufficient to preserve the verdict here, though point estimates move."
- 🔁 **"What predicts Fisher-vs-Raw is the discriminative strength of `V_raw[0]`."** Near-circular: the Raw null-ratio at rank 1 *is* the fraction of `Δh` outside `V_raw[0]`, so this is close to "Raw wins when the Raw score discriminates." Reframe as a consistency check and move the mechanistic claim to *why* `V_raw[0]` separates for some architectures.

## Handoff

Analysis is a short pandas/sklearn script over banked parquets. **Codex authors** per the write/audit-only rule; **Claude Code or MK executes** and supplies the table. Manuscript rewording follows the verdict, not before.

## Related

[[log]] 2026-09-10 twelfth entry · `.deepseek-pri-review-2026-09-10.md` · `pri-draft.tex` §3.2 (the orientation rule this turns on) and §4.3 (the sites) · [[workorders/capture-provenance-columns-workorder-2026-09-10]]
