# CC baselines — does the panel earn its keep? (2026-09-10)

_Status: `[RESOLVED — SPLIT]`. Descriptive re-analysis of banked CC artifacts. **No model run, no gate re-read, no sealed verdict touched.** Both tests run because an external reviewer objected that CC had **no baseline at all** — its only comparator, confidence, sits *inside* the 29-signal panel._

**Two questions, two different answers.**

- ✅ **Is the label recoverable from prompt surface form?** No. The panel beats a bag-of-words model on **6 of 6** tasks.
- ❌ **Is selecting one signal the right way to use the panel?** No. A plain logistic regression on all 27 signals **beats** the paper's nested-OOB selector.

## Test 1 — lexical baseline

TF-IDF (1–2gram) + logistic regression on the banked prompt text. **GroupKFold on `stem_id`**, so a question never straddles the split — essential, since each stem appears twice (right candidate and hallucinated candidate). Out-of-fold AUROC.

| task | lexical | panel OOB median | margin |
|---|---|---|---|
| triviaqa_paired_rep | **0.5022** | 0.9095 | **+0.407** |
| anli_r2 | **0.4007** | 0.6531 | **+0.253** |
| anli_r1_rep | 0.6044 | 0.8410 | +0.237 |
| halueval_qa | 0.6834 | 0.8751 | +0.192 |
| halueval_summarization | 0.6421 | 0.7481 | +0.106 |
| halueval_dialogue | 0.7328 | 0.7564 | ⚠️ **+0.024** |

🎯 **The two strongest rows are the ones that answer the objection.** On `triviaqa_paired_rep` and `anli_r2` the lexical model sits **at or below chance** while the panel reaches 0.910 and 0.653. On those tasks there is no surface shortcut to exploit, and the geometry works anyway.

⚠️ **One near-wash worth reporting:** `halueval_dialogue` at **+0.024**. There the geometry adds almost nothing over bag-of-words.

## Test 2 — panel selector versus simpler models

⚠️ **Authored by `deepseek-v4-pro`, executed here.** DeepSeek cannot run code; having it design the test removes the conflict of the work's author also designing its examination. It set the comparators **and pre-committed the interpretation before any numbers were produced**:

> The panel selector is justified only if the paired difference against **every** simpler comparator lies entirely below zero.

| comparator | pooled median | diff vs selector | verdict |
|---|---|---|---|
| paper_selector | 0.8946 | — | — |
| **all27_lr** | **0.9627** | **+0.0548 [−0.0005, +0.1138]**, wins 97% | ❌ **not justified** |
| attention_selector | 0.8718 | +0.0000 | no reliable difference, 6/6 |
| non_attention_sel | 0.8565 | −0.0096 | no reliable difference, 6/6 |
| fixed_loo_model | 0.3856 | −0.4879 | ✅ paper better, 4/6 |
| fixed_loto | 0.4247 | −0.4312 | ✅ paper better, 5/6 |

**Paper selector better on 0 of 6 tasks. Not justified on 3, no reliable difference on 3.**

### Independently reproduced

Because the result goes against the paper, it was re-derived with a separate implementation — GroupKFold on `stem_id`, scaler *and* column selection both fit on train only:

| task | best single column | all 27 | delta |
|---|---|---|---|
| triviaqa_paired_rep ×3 models | 0.865–0.983 | 0.965–0.992 | +0.009 … +0.103 |
| halueval_qa ×3 models | 0.815–0.877 | 0.912–0.983 | +0.039 … **+0.168** |
| anli_r2 ×3 models | 0.644–0.725 | 0.668–0.751 | +0.017 … +0.070 |

**All-27 wins 9/9, mean +0.0690.**

### Scepticism applied before accepting it

The run emitted **190,800** numerical warnings. Classified as sklearn matmul overflow, then the script was inspected: it fits `StandardScaler` on train only, evaluates out-of-bag, and falls back to `0.5` on a failed fit — **a fallback that biases against the finding, not for it.** The independent reimplementation exists for the same reason.

## What this does and does not say

- ✅ **CC's headline is unaffected.** Per-deployment selection still beats fixed cells (4/6 and 5/6), so *"no universal detector"* stands.
- ❌ **An implicit design choice is refuted:** that picking one signal is the right way to use the panel. The constructive reading is *use all the signals*.
- 🔎 **Heavy redundancy across families.** Both single-family restrictions match the full panel with no reliable difference, 6/6 each.
- ⚠️ **Not like-for-like.** The paper's figure is a procedure-level OOB median with nested selection; these are grouped cross-validation. The comparison bounds the question; it is not a matched head-to-head, and the paper must say so if it adopts this.

## Scope

Banked artifacts only. Moves no registered CC endpoint. Scripts: `commit-confluence/stage_b/analysis/lexical_baseline.py` and `panel_vs_simple.py` (repo `009e95f`).

→ [[log]] 2026-09-10 twenty-third and twenty-fourth entries · `cc-draft.tex`
