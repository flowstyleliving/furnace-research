# HVS Free CPU Follow-Ups (`F1`–`F5`) — Complete Results (2026-10-22)

**Specification:** `FOLLOWUP_PLAN.md` (specification; first committed in the same commit as these results, so git history does not show it preceded execution). **Data:** 53 banked BENCH cells (`D3`, MLX 4-bit, $n = 1,000$). **Code:** `run_followups.py` and `extract_r2_errors.py`, importing frozen `hvs.py` (`d29a2e4`) read-only.

---

## Executive Summary — What Each Test Closed

| Test | Hypothesis / Open Item | Outcome | Deciding Numbers |
|---|---|---|---|
| **F1** (`E1` with premise stems) | Shared premises in ANLI (`453/1000` R1, `246/1000` R2) inflate fold/bootstrap precision | **CLOSED (no change to conclusions)** | Median 95% CI width widens $+5.7\%$ (`0.083 → 0.087`). Median `E1` $\Delta$: `-0.068 → -0.069` (R1 `-0.094 → -0.093`, R2 `-0.045 → -0.048`). CIs $<0$ in `10/16` (was `11/16`; `Qwen3-1.7B` R2 upper bound `-0.000 → +0.004`). Powered ANLI cells (`2/16`) and informative BENCH cells (`9/53`) unchanged. |
| **F2** (Per-group sign `E1_PG` & `E1_PG_signonly`) | Pooled sign in `E1` cancels class-tracking signals across `YES`/`NO` groups | **CLOSED (real handicap, does not flip ANLI head-to-head)** | Premise-grouped ANLI median $\Delta$ improves from `-0.069` to `-0.045` (`E1_PG` col+sign) and `-0.040` (`E1_PG_signonly`). **0/16 ANLI cells have 95% CI $>0$** (`0/16` Holm-significant); `7/16` (`col_sign`) and `8/16` (`sign_only`) still have 95% CI $<0$. Across all 53 BENCH cells, `E1_PG` (`col_sign`) raises Holm-significant cells from `12/53` to `15/53` (`5/12` informative cells, 42%). |
| **F3** (`S4` with pass-one fold-sign confidence) | `S4` used pass-two continuation `p_max` instead of pass-one confidence | **CLOSED (strengthens HaluEval/TriviaQA robustness from 10/12 to 12/12)** | $\text{AUROC}(-\exp(-\text{surprise})) \equiv \text{AUROC}(\text{surprise})$ to $<10^{-9}$ in all 53 cells. Using pass-one `surprise` with per-fold sign (`S4_pass1_foldsign`, which flips the 4 confidence-inverted cells to their positive orientation), **all 12/12 `E1`-significant BENCH cells survive both `S4_pass1_foldsign` and `S5_seed2`** (the 2 summarization losses under old `S4` were caused by pass-two continuation `p_max`, e.g., $P(\text{`ES'}\mid\text{`▁Y'})$ in `Mistral-7B`). |
| **F4** (Within-group L2 incremental combo, 53 cells) | Does the 22-signal panel *add to* confidence (`surprise`) within answer groups? | **CLOSED (positive across BENCH and in 2/8 ANLI R2 cells after Holm)** | Bootstrapping the true within-group gain $\Delta_{\text{wg}}$ directly (free of the pooled logistic-regression intercept artifact): across all 53 cells, median $\Delta_{\text{wg}} = +0.073$, **31/53 task-Holm significant** (`29/53` all-53-Holm): `halueval_qa` `10/10` (`+0.163`), `halueval_summarization` `8/8` (`+0.343`), `triviaqa` `7/10` (`+0.087`), `halueval_dialogue` `4/9` (`+0.032`), `anli_r2` **`2/8` Holm-16 significant** (`Phi-4-mini` $+0.069$ $[+0.028,+0.111]$, $p_{\text{Holm-16}}=0.024$; `Mistral-7B` $+0.060$ $[+0.015,+0.104]$, $p_{\text{Holm-16}}=0.045$; R2 median $+0.030$), `anli_r1_rep` `0/8` (median $-0.012$). |
| **F5** (Manual & quantitative audit of ANLI R2 confident errors) | Are confident ANLI R2 "errors" actually noisy/debatable gold labels? | **CLOSED as a sensitivity check (dropping consensus-wrong rows raises the absolute AUROC of both arms by about `+0.046` and leaves `E1` $\Delta$ essentially unchanged, `-0.048` to `-0.050`; the dropped rows mix label defects with genuine model errors)** | Across 240 top-30 cell errors, `150/240` (62.5%) are items where $\ge 6/8$ models err. Manual review of the top 30 consensus confident errors: **12/30 (40%)** outright gold-label defects or unstated-2019-anchor-year riddles, **7/30 (23%)** character typos or neutral-as-contradiction boundary items, **11/30 (37%)** genuine model reasoning errors. Dropping unanimous (`8/8` wrong, 26 rows) or consensus (`\ge 7/8` wrong, 95 rows) items raises median `AUC_conf` (`0.628 → 0.646 → 0.674`) and `AUC_sig` (`0.572 → 0.586 → 0.618`) equally, leaving median `E1` $\Delta$ unchanged (`-0.045 → -0.044 → -0.050`). |

---

## 1. ANLI 16-Cell Master Table (`F1`, `F2`, `F4`)

All columns below use premise-grouped stems (`sha1(premise)`) except `Orig E1 Δ` (row-grouped `HVS_RESULTS.json`). `dwg_l2all` is the mean over `YES` and `NO` answer groups of the out-of-fold AUROC gain of `L2(surprise + 22 signals)` over fixed-sign `surprise`, with paired premise-cluster 95% CIs ($B=2,000$) and Holm $p$ across the 16 ANLI cells.

| Cell | Acc | Orig `E1` Δ [CI] | `F1` Premise `E1` Δ [CI] | `F2` `E1_PG` (col+sign) Δ [CI] | `F2` `E1_PG_signonly` Δ [CI] | `F4` Within-group L2 `dwg_l2all` [CI] | `F4` Holm-16 $p$ |
|---|---:|---|---|---|---|---|---:|
| `anli_r1_rep|Llama-3.1-8B-Instruct-4bit` | 0.845 | -0.139 [-0.185, -0.093] | -0.138 [-0.184, -0.092] | -0.137 [-0.178, -0.093] | -0.138 [-0.184, -0.092] | -0.012 [-0.045, +0.023] | 1.000 |
| `anli_r1_rep|Llama-3.2-3B-Instruct-4bit` | 0.828 | -0.055 [-0.091, -0.021] | -0.056 [-0.095, -0.019] | -0.058 [-0.095, -0.024] | -0.056 [-0.095, -0.019] | -0.016 [-0.040, +0.009] | 1.000 |
| `anli_r1_rep|Mistral-7B-Instruct-v0.3-4bit` | 0.861 | -0.081 [-0.138, -0.023] | -0.077 [-0.136, -0.016] | -0.046 [-0.096, +0.008] | -0.078 [-0.137, -0.017] | +0.003 [-0.042, +0.047] | 1.000 |
| `anli_r1_rep|Mistral-Nemo-Instruct-2407-4bit` | 0.897 | -0.005 [-0.046, +0.032] | +0.002 [-0.040, +0.044] | -0.005 [-0.046, +0.035] | +0.002 [-0.040, +0.044] | -0.012 [-0.048, +0.024] | 1.000 |
| `anli_r1_rep|Phi-4-mini-instruct-4bit` | 0.841 | -0.116 [-0.166, -0.067] | -0.116 [-0.165, -0.064] | -0.062 [-0.106, -0.018] | -0.153 [-0.207, -0.101] | +0.015 [-0.023, +0.055] | 1.000 |
| `anli_r1_rep|Qwen3-1.7B-4bit` | 0.742 | -0.107 [-0.149, -0.066] | -0.108 [-0.154, -0.065] | -0.092 [-0.133, -0.047] | -0.079 [-0.123, -0.031] | -0.010 [-0.077, +0.056] | 1.000 |
| `anli_r1_rep|Qwen3-8B-4bit` | 0.891 | -0.193 [-0.265, -0.121] | -0.162 [-0.225, -0.102] | -0.096 [-0.160, -0.034] | -0.079 [-0.145, -0.011] | -0.012 [-0.070, +0.046] | 1.000 |
| `anli_r1_rep|gemma-3-4b-it-4bit` | 0.838 | -0.010 [-0.049, +0.028] | -0.025 [-0.063, +0.012] | -0.047 [-0.091, -0.004] | -0.025 [-0.063, +0.012] | -0.029 [-0.072, +0.011] | 1.000 |
| `anli_r2|Llama-3.1-8B-Instruct-4bit` | 0.643 | -0.092 [-0.133, -0.050] | -0.110 [-0.150, -0.067] | -0.115 [-0.163, -0.065] | -0.110 [-0.156, -0.066] | +0.026 [-0.022, +0.074] | 1.000 |
| `anli_r2|Llama-3.2-3B-Instruct-4bit` | 0.631 | -0.020 [-0.054, +0.014] | -0.020 [-0.054, +0.013] | -0.027 [-0.060, +0.006] | -0.020 [-0.054, +0.013] | -0.003 [-0.036, +0.031] | 1.000 |
| `anli_r2|Mistral-7B-Instruct-v0.3-4bit` | 0.702 | -0.050 [-0.096, -0.006] | -0.061 [-0.110, -0.014] | -0.044 [-0.090, +0.003] | -0.061 [-0.110, -0.014] | +0.060 [+0.015, +0.104] | 0.045 |
| `anli_r2|Mistral-Nemo-Instruct-2407-4bit` | 0.771 | +0.009 [-0.024, +0.042] | +0.003 [-0.028, +0.034] | -0.017 [-0.050, +0.016] | +0.003 [-0.028, +0.034] | +0.016 [-0.020, +0.051] | 1.000 |
| `anli_r2|Phi-4-mini-instruct-4bit` | 0.609 | -0.098 [-0.143, -0.051] | -0.079 [-0.125, -0.032] | -0.032 [-0.079, +0.016] | -0.023 [-0.069, +0.023] | +0.069 [+0.028, +0.111] | 0.024 |
| `anli_r2|Qwen3-1.7B-4bit` | 0.545 | -0.040 [-0.081, -0.000] | -0.035 [-0.075, +0.004] | -0.024 [-0.066, +0.017] | -0.008 [-0.050, +0.035] | +0.017 [-0.054, +0.089] | 1.000 |
| `anli_r2|Qwen3-8B-4bit` | 0.739 | -0.135 [-0.189, -0.083] | -0.130 [-0.181, -0.079] | -0.009 [-0.058, +0.040] | +0.026 [-0.020, +0.071] | +0.041 [-0.004, +0.087] | 0.623 |
| `anli_r2|gemma-3-4b-it-4bit` | 0.632 | -0.023 [-0.064, +0.018] | -0.013 [-0.055, +0.031] | -0.007 [-0.050, +0.036] | -0.018 [-0.058, +0.024] | +0.033 [-0.007, +0.070] | 0.682 |

### Why only 2 of the 4 R2 cells survive on `dwg_l2all` (fixing the scratchpad's pooled intercept artifact)

In the scratchpad's `anli_incremental_diag.py`, CIs were computed on `dbest_l2all`, which pooled per-group `LogisticRegression.decision_function` outputs across the `YES` and `NO` groups and compared that pooled vector against unshifted `surprise` (or `e1conf`). Because `LogisticRegression` fits a separate intercept $\beta_{0,g} \approx \text{logit}(\text{err\_rate}_g)$ inside each answer group, `dbest_l2all` credited the L2 model with the between-group error-rate difference (most visibly in `anli_r1_rep|Qwen3-1.7B`, where `dbest_l2all` was $+0.075$ $[+0.043, +0.108]$ while its true within-group gain `dwg_l2all` is $-0.010$ $[-0.077, +0.056]$).

When paired premise-cluster bootstrap CIs are computed directly on the within-group gain `dwg_l2all`:
- **`anli_r2|Phi-4-mini`**: $+0.069$ $[+0.028, +0.111]$, one-sided $p = 0.0015$, **Holm-16 $p = 0.024$** (all-53 Holm $p = 0.038$).
- **`anli_r2|Mistral-7B`**: $+0.060$ $[+0.015, +0.104]$, one-sided $p = 0.0030$, **Holm-16 $p = 0.045$**.
- **`anli_r2|Qwen3-8B`**: $+0.041$ $[-0.004, +0.087]$, unadjusted one-sided $p = 0.0445$, Holm-16 $p = 0.623$ (directional).
- **`anli_r2|gemma-3-4b`**: $+0.033$ $[-0.007, +0.070]$, unadjusted one-sided $p = 0.0525$, Holm-16 $p = 0.682$ (directional).

---

## 2. Per-Task Summary Across All 53 BENCH Cells (`F2`, `F3`, `F4`)

| Task | Cells | `E1` (premise) med Δ | `E1` Holm sig | `E1_PG` (col+sign) med Δ | `E1_PG` Holm sig | `F4` `dwg_l2all` med gain | `F4` `dwg_l2all` task-Holm sig (all-53 Holm) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `anli_r1_rep` | 8 | -0.093 | 0/8 | -0.060 | 0/8 | -0.012 | 0/8 (0/8) |
| `anli_r2` | 8 | -0.048 | 0/8 | -0.026 | 0/8 | +0.030 | 2/8 (1/8) |
| `halueval_dialogue` | 9 | -0.078 | 1/9 | -0.047 | 2/9 | +0.032 | 4/9 (4/9) |
| `halueval_qa` | 10 | +0.035 | 3/10 | +0.046 | 3/10 | +0.163 | 10/10 (10/10) |
| `halueval_summarization` | 8 | +0.139 | 6/8 | +0.213 | 7/8 | +0.343 | 8/8 (8/8) |
| `triviaqa_paired_rep` | 10 | -0.043 | 2/10 | -0.016 | 3/10 | +0.087 | 7/10 (6/10) |

---

## 3. `F3` — Corrected `S4` (`S4_pass1_foldsign`) on the 12 `E1`-Significant Cells

In `HVS_RESULTS.json`, `S4_alt_conf` used pass-two `p_max`, which caused `Mistral-7B` summarization and `Mistral-Nemo` summarization to appear to reverse. Replacing pass-two `p_max` with pass-one `surprise` (equivalent to `-exp(-surprise)`) with per-fold sign (`S4_pass1_foldsign`) tests whether the 12 `E1`-significant cells still win when confidence is oriented in the helpful direction in every fold (flipping the 4 confidence-inverted cells):

| Cell | `E1` AUC sig | Fixed `surprise` AUC | Pass-2 `p_max` AUC (old `S4`) | Pass-1 `fold_sign` AUC (`F3`) | `F3` Δ [95% CI] | `F3` Holm-53 $p$ | `S5` seed2 Holm-53 $p$ | Survives both? |
|---|---:|---:|---:|---:|---|---:|---:|:---:|
| `halueval_dialogue|Qwen2.5-7B-Instruct-4bit` | 0.653 | 0.456 | 0.514 | 0.544 | +0.109 [+0.062, +0.156] | 0.026 | 0.026 | **YES** |
| `halueval_qa|Mistral-7B-Instruct-v0.3-4bit` | 0.725 | 0.607 | 0.464 | 0.607 | +0.117 [+0.067, +0.170] | 0.026 | 0.026 | **YES** |
| `halueval_qa|Qwen2.5-7B-Instruct-4bit` | 0.706 | 0.452 | 0.547 | 0.548 | +0.158 [+0.103, +0.212] | 0.026 | 0.026 | **YES** |
| `halueval_qa|gemma-3-4b-it-4bit` | 0.835 | 0.700 | 0.719 | 0.700 | +0.135 [+0.099, +0.169] | 0.026 | 0.026 | **YES** |
| `halueval_summarization|Llama-3.2-3B-Instruct-4bit` | 0.883 | 0.637 | 0.595 | 0.637 | +0.247 [+0.214, +0.279] | 0.026 | 0.026 | **YES** |
| `halueval_summarization|Mistral-7B-Instruct-v0.3-4bit` | 0.772 | 0.314 | 0.863 | 0.686 | +0.086 [+0.049, +0.121] | 0.026 | 0.026 | **YES** |
| `halueval_summarization|Mistral-Nemo-Instruct-2407-4bit` | 0.727 | 0.563 | 0.813 | 0.563 | +0.165 [+0.131, +0.197] | 0.026 | 0.026 | **YES** |
| `halueval_summarization|Qwen2.5-7B-Instruct-4bit` | 0.698 | 0.585 | 0.515 | 0.585 | +0.113 [+0.067, +0.160] | 0.026 | 0.026 | **YES** |
| `halueval_summarization|Qwen3-1.7B-4bit` | 0.674 | 0.562 | 0.599 | 0.562 | +0.112 [+0.071, +0.152] | 0.026 | 0.026 | **YES** |
| `halueval_summarization|Qwen3-8B-4bit` | 0.873 | 0.620 | 0.772 | 0.620 | +0.253 [+0.230, +0.276] | 0.026 | 0.026 | **YES** |
| `triviaqa_paired_rep|Phi-3.5-mini-instruct-4bit` | 0.710 | 0.628 | 0.480 | 0.628 | +0.082 [+0.031, +0.132] | 0.026 | 0.026 | **YES** |
| `triviaqa_paired_rep|Qwen2.5-7B-Instruct-4bit` | 0.790 | 0.352 | 0.575 | 0.648 | +0.142 [+0.084, +0.198] | 0.026 | 0.026 | **YES** |

**Result:** **12/12 (100%)** survive both `S4_pass1_foldsign` and `S5_seed2` (including `halueval_summarization|Mistral-Nemo-Instruct-2407-4bit`, which was one of the 2 significant informative cells in `HVS_DECISION.json`).

---

## 4. `F5` — Audit of the Top 30 Consensus Confident Errors on ANLI R2

- **Cross-model overlap:** Across the $8 \times 30 = 240$ lowest-`surprise` error instances in `anli_r2`, **150/240 (62.5%)** occur on items where $\ge 6/8$ models got the item wrong, **106/240 (44.2%)** where $\ge 7/8$ got it wrong, and **43/240 (17.9%)** where all **8/8** models got it wrong.
- **Token-prior asymmetry in raw `surprise`:** Ranking a model's errors by raw `surprise` selects almost exclusively from its higher-prior answer class: `YES` errors (gold `NO`) account for `30/30` in `Mistral-Nemo`, `28/30` in `Qwen3-8B`, and `27/30` in `gemma-3-4b`, whereas `NO` errors (gold `YES`) account for `30/30` in `Qwen3-1.7B`, `28/30` in `Phi-4-mini`, and `22/30` in `Llama-3.1-8B`.
- **Manual classification of the top 30 unique consensus confident errors (`F5_r2_confident_errors.json`):**
  1. **Outright gold-label defects or unstated-2019-anchor-year / riddle items: 12/30 (40%).**
     - *Factual/logical mislabels (7):* `dev_r2:798` (`idx=99`, 8/8 wrong, gold `YES`: says Princess Juliane was born in Switzerland when premise says `(Coburg, 1781 – Elfenau, near Bern, Switzerland, 1860)`); `test_r2:974` (`idx=192`, 7/8 wrong, gold `YES`: says *University of Bologna* is a former Roman Catholic church when *Santa Lucia* is); `test_r2:228` (`idx=991`, 7/8 wrong, gold `YES`: calls *The Wolfsonian–FIU* "a school" when premise says "a museum, library and research center... a division within FIU"); `dev_r2:6` (`idx=127`, 8/8 wrong, gold `YES`: calls the Alexandroff topological space compactification "an equation"); `dev_r2:967` (`idx=585`, 8/8 wrong, gold `NO`: treats winning a Nigar Award for a film role as contradicting being famous for that role); `dev_r2:155` (`idx=194`, 7/8 wrong, gold `YES`: assumes the *second* season specifically airs weekday mornings); `test_r2:193` (`idx=953`, 7/8 wrong, gold `YES`: calls a descending funicular railway a "cable car" going "up and down").
     - *Unstated 2019 crowdworker anchor year / vacuous riddles (5):* `dev_r2:40` (`idx=905`, 8/8 wrong, gold `YES`: "Toolbox Murders is both 41 years old and 15 years old" — requires $2019 - 1978$ and $2019 - 2004$); `dev_r2:579` (`idx=203`, 6/8 wrong, gold `YES`: "Linda Ellerbee is 75 years old today" for 1944 birth year); `test_r2:666` (`idx=947`, 7/8 wrong, gold `YES`: "words spoken in [silent film] Baby Mine is equal to the number of pigs who could fly"); `dev_r2:137` (`idx=450`, 7/8 wrong, gold `YES`: "broadcast less than 3000 years ago"); `dev_r2:745` (`idx=91`, 8/8 wrong, gold `YES`: "pretended to be Dakota" for acting a role).
  2. **Character typos or `neutral`-boundary items forced into binary contradiction: 7/30 (23%).**
     - *Character typos (2):* `dev_r2:143` (`idx=149`, 8/8 wrong: "University of **Rabatat** or IUR" vs "Rabat"); `test_r2:534` (`idx=417`, 8/8 wrong: "stars **Preston Fost**" vs "Preston Foster").
     - *Pragmatic / neutral-as-contradiction boundary (5):* `dev_r2:627` (`idx=705`, 8/8 wrong: "discovered in 1980" vs "rediscovered in 1980"); `test_r2:831` (`idx=544`, 8/8 wrong: "near Rutland" vs "in Rutland"); `dev_r2:74` (`idx=144`, 7/8 wrong: "WNOS is a talk show" vs "talk radio station"); `test_r2:773` (`idx=609`, 7/8 wrong: "camair-co is a replacement of cameroon airlines" labeled contradiction); `test_r2:525` (`idx=939`, 6/8 wrong: whether Dorothy Flynt was Edmund Quincy III's second wife is strictly neutral in the premise, where Elizabeth Gookin was Edmund Quincy II's second wife).
  3. **Genuine model reasoning / reading errors: 11/30 (37%).**
     - Multi-hop geography (`test_r2:46`, Shanghai → China borders India), role/date attachment (`dev_r2:103`, `test_r2:136` `respectively` swap, `test_r2:13` Eurovision language, `test_r2:650` solo vs group album), and date/unit arithmetic (`test_r2:966` 7 days vs $>1$ week, `dev_r2:613` 2005–2014 vs $>10$ years, `test_r2:35` 6 miles/10 km vs 6 km, `test_r2:220` Nov 2012 vs Jan 2013, `test_r2:423` 1907 vs War of 1812, `test_r2:955` game based on film).
- **Sensitivity check (dropping consensus-wrong rows on `anli_r2`):**
  - All 1,000 rows: median `AUC_conf = 0.628`, median `AUC_sig = 0.569`, median `E1` $\Delta = -0.048$.
  - Dropping the 26 unanimous (`8/8` wrong) rows: median `AUC_conf = 0.645`, median `AUC_sig = 0.587`, median `E1` $\Delta = -0.049$.
  - Dropping the 95 consensus (`>=7/8` wrong) rows: median `AUC_conf = 0.674`, median `AUC_sig = 0.616`, median `E1` $\Delta = -0.050$.
  - **Conclusion:** Dropping the consensus-wrong rows raises the absolute own-error AUROC of **both** confidence and internal geometry on ANLI R2 (`+0.046` when the `>=7/8` rows are removed) and leaves the head-to-head `E1` gap essentially unchanged (`-0.048` to `-0.050`), so these rows do not explain the gap. This is a sensitivity result, not an attribution: the dropped rows mix label defects and adversarial traps with genuine model errors (11/30 reviewed rows were genuine reasoning or reading errors).
