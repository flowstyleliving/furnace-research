# Verdict baseline — does commit-moment attention add anything over the model's own answer? (2026-10-10)

_Status: `[OPEN — descriptive, unregistered]`. Post-hoc re-analysis of banked BENCH score matrices. **No model run, no gate re-read, no sealed verdict touched.** First computed 2026-09-27 for an earlier prompt and audited then by Codex `gpt-6-astra` (read-only); re-run and banked here 2026-10-10 because the numbers had no results page, no claims line and no log entry._

## The question

Every CC task hands the model a candidate answer and asks it to judge YES or NO. The obvious skeptic's question: **is the geometry just re-reading the model's own verdict?** The CC paper never tests this. Its confidence signals (`surprise`, `p_max`) are unsigned, so they say how sure the model is but not which way it answered. Companion to [[results/cc-baselines-2026-09-10]], which ruled out a surface-wording shortcut but not this one.

## Method

- **Data.** Every banked BENCH `*.matrix.npz` under `commit-confluence/stage_b/profiles*/` with `gen_token_ids` and n ≥ 500: **53 cells** across six tasks. MLX 4-bit, local. Not comparable with the torch/Modal depth lanes.
- **Four feature sets**, each a standardized logistic regression, 5-fold `GroupKFold` on `stem_ids` (paired candidates never straddle a split), out-of-fold AUROC:
  1. 🗳️ **Answer** — indicators for the two most frequent first generated tokens.
  2. 🎚️ **Answer + confidence** — answer plus prefix `surprise`, `p_max`, and their products with the answer indicator.
  3. 🧲 **Attention alone** — the 21 attention/value-norm columns (7 metrics × 3 depths).
  4. ➕ **All combined** — sets 2 and 3 together.
- **Code + per-cell output:** `the_GOAT/exploratory/verdict-baseline-2026-10-10/` (`answer_conf_baseline.py` sha256 `44b3e65b…`, `per_cell.tsv`, `gain_summary.txt`). Concatenated input-matrix sha256 `bb550c10…` at `commit-confluence` `7134e0b`.
- **Reproduction.** The 2026-10-10 re-run reproduces the 2026-09-27 medians exactly.

## Result

| Feature set | Median AUROC (53 cells) |
|---|---|
| Answer | 0.714 |
| Answer + confidence | **0.849** |
| Attention alone | 0.904 |
| All combined | **0.927** |

- ✅ **The geometry is not just the verdict.** Added to answer + confidence, attention gains **> 0.02 in 33/53 cells**, median **+0.033**, worst case **−0.002**, best +0.277.
- ⚖️ **The gain is modest over the fair baseline.** Attention alone beats answer + confidence by a median of only +0.017.

| Task | Cells | Answer + confidence | All combined | Median gain |
|---|---|---|---|---|
| anli_r1_rep | 8 | 0.915 | 0.919 | **+0.010** |
| anli_r2 | 8 | 0.700 | 0.735 | +0.024 |
| halueval_dialogue | 9 | 0.805 | 0.819 | +0.028 |
| halueval_qa | 10 | 0.895 | 0.962 | +0.067 |
| halueval_summarization | 8 | 0.740 | 0.951 | ⚠️ **+0.211** |
| triviaqa_paired_rep | 10 | 0.906 | 0.960 | +0.028 |

## Caveats — from the 2026-09-27 Astra audit

Audit verdict: **"supported as descriptive, overstated as mechanism."**

- 🚧 **This is not the model's full continuous verdict.** Answer + confidence lacks the unchosen answer's probability and the mass across YES/NO token variants. `P(YES) − P(NO)` is not banked in these matrices and needs new extraction.
- 🔤 **"Answer" is the first generated token**, not a parsed YES/NO verdict. Variants and preambles can intervene (e.g. Qwen3-8B ANLI-r2 has 13 noncanonical first tokens). Commitment failures are not excluded.
- ⏱️ **`p_max` is measured after the committed token**, predicting its continuation; only `surprise` is the committed token's own confidence.
- 📏 **The +0.211 on summarization may be a length or surface shortcut.** Untested. The 2026-09-10 lexical baseline does not test length.
- 🏷️ **Labels are supplied-candidate truth**, not whether the model's own emitted answer was correct.

**Safe sentence:** "Commit-moment attention adds predictive value beyond the model's emitted answer and its confidence, but we have not yet controlled for its full continuous verdict."

## Related: the model's continuous verdict was measured once, on different data

The 2026-05-17 pre-registered belief-readout panel ([[results/step0-belief-readout-2026-05-17]]) read `P(YES)/P(NO)` at t = 0 on ANLI R1, n = 200: **Recoverable for 9/10 models**, Qwen2.5 signed AUROC 0.926. That run shows the continuous verdict is itself a strong discriminator, so it is the baseline the registered endpoint must beat. It was a different panel and is not joined to the BENCH matrices above, so it cannot close the gap here.
