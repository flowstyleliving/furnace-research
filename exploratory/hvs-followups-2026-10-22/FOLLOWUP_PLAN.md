# HVS Follow-Up Analysis Plan — Free CPU Tests (2026-10-22)

**Status:** Specification (first committed in the same commit as the results, so git history does not show it preceded execution) for the five zero-compute follow-up checks (`F1`–`F5`) from the 2026-10-22 ANLI own-error audit. No repo file in `commit-confluence` is modified; `hvs.py` (`d29a2e4`) is imported read-only.

## Scope & Data

All 53 banked BENCH cells (`D3`, MLX 4-bit, $n = 1,000$ per cell) from `commit-confluence/stage_b/profiles_bench/*/*.matrix.npz` and `commit-confluence/exploratory/moe-detector-check/correctness/harness_vs_signal/bench_labels/*.csv`.
- For `halueval_qa`, `halueval_dialogue`, `halueval_summarization`, and `triviaqa_paired_rep`, `stems` are the existing 500 `stem_ids` per task.
- For `anli_r1_rep` and `anli_r2`, `stem_ids` in the JSONL are unique per row (`1000/1000`), whereas 453/1000 (`anli_r1_rep`, 744 unique premises) and 246/1000 (`anli_r2`, 876 unique premises) share a premise. Premise-grouped tests use `sha1(premise)` extracted from `Premise: ... \nHypothesis:` in `stage_b/data_bench/anli_*_n1000.jsonl`.

---

## F1 — Premise-Grouped `E1` on ANLI (16 cells)

- Re-run `hvs.run_test` (`SEED = 20260612`, `SEED2 = 20261013`, `K = 5`, `B = 2000`, `P = 1000`) on the 16 BENCH ANLI cells with `stems = sha1(premise)` for:
  - `partialled` (`E1`),
  - `pooled`,
  - `yes_only` and `no_only`,
  - `S5_seed2`.
- Re-evaluate `HVS_DECISION` informative-cell membership (`MD-Δ ≤ 0.05`, $\ge 100$ errors, $\ge 100$ correct, accuracy $\in [0.60, 0.90]$) and Holm-adjusted $p$-values.

## F2 — Per-Group Sign (`E1_PG` and `E1_PG_signonly`) across all 53 BENCH cells

In `hvs.pipeline`, features are z-scored within each answer group (`YES`, `NO`) using training-fold statistics, but a **single pooled column and sign** are chosen across both groups (`col = argmax |AUC - 0.5|`, `sign = +1 if AUC >= 0.5 else -1`). When a signal tracks the input class, its error association has opposite signs in the `YES` and `NO` answer groups.

We test two out-of-fold per-group rules under premise-grouped stems (ANLI) and `stem_ids` (other 4 tasks), with $B = 2,000$ paired stem-cluster bootstrap draws and $P = 1,000$ within-group label permutations:
1. **`E1_PG` (per-group column + sign):** Within each training fold $f$ and each answer group $g \in \{\text{YES}, \text{NO}\}$, pick $j_{f,g}^* = \arg\max_j |\text{AUROC}(\text{err}_{\text{tr},g}, T_{\text{tr},g,j}) - 0.5|$ and $s_{f,g}^* = \text{sign}(\text{AUROC}(\text{err}_{\text{tr},g}, T_{\text{tr},g,j_{f,g}^*}) - 0.5)$, and score held-out rows in group $g$ as $s_{f,g}^* \cdot T_{\text{te},g,j_{f,g}^*}$.
2. **`E1_PG_signonly` (shared column, per-group sign):** Within each training fold $f$, orient every candidate $j$ separately inside each training answer group $g$ by its training group-$g$ sign $s_{f,g,j}$, pick the single column $j_f^*$ that maximizes the pooled training AUROC of $s_{f,g,j} \cdot T_{\text{tr},g,j}$, and score held-out rows in group $g$ as $s_{f,g,j_f^*} \cdot T_{\text{te},g,j_f^*}$.

Endpoints: `auc_sig`, `auc_conf`, `delta = auc_sig - auc_conf`, 95% stem-cluster bootstrap CIs, one-sided bootstrap $p(\Delta > 0)$, permutation $p(\text{E0})$, `md_delta_boot`, and Holm–Bonferroni across (a) informative cells, (b) all 53 BENCH cells, and (c) the 16 ANLI cells.

## F3 — Corrected `S4` Pass-One Fold-Sign Confidence across all 53 BENCH cells

- The banked `p_max` column is measured at pass two (continuation after the answer token) and is near chance on ANLI ($0.44\text{–}0.63$).
- Pass-one `p_max` equals $\exp(-\text{surprise})$, which is rank-equivalent to `surprise`.
- Replace `S4_alt_conf` on D3 with **`S4_pass1_foldsign`**: `conf = surprise` (and verify identical results with `-exp(-surprise)`), `conf_mode = "fold_sign"` (fitting the orientation of confidence in each training fold so inverted-confidence cells are oriented positively rather than fixed at $+1$).
- Check how many of the 12 `E1`-significant BENCH cells remain Holm-significant under `S4_pass1_foldsign` and `S5_seed2`.

## F4 — Within-Group L2 Incremental Test ("Beyond Confidence") across all 53 BENCH cells

To test whether the 22 non-confidence candidates **add** error-detection signal to `surprise` without the between-group intercept artifact caused by pooling per-group `LogisticRegression.decision_function` scores against unshifted `surprise`:

- **Folds & Standardization:** 5-fold CV grouped by `sha1(premise)` on ANLI and `stem_ids` on the other 4 tasks (`SEED = 20260612`). Within each fold and answer group $g \in \{\text{YES}, \text{NO}\}$, standardize `surprise` ($S_{\text{tr}}, S_{\text{te}}$) and the 22 candidates ($T_{\text{tr}}, T_{\text{te}}$) using training-fold group-$g$ statistics (`hvs.transform`).
- **Models fit per training fold and answer group $g$** (`LogisticRegression(C=1.0, max_iter=2000)` on training rows of group $g$, falling back to $S_{\text{te}}$ if training group $g$ has only one class):
  - `base`: fit on $S_{\text{tr},g}$ (1 feature: `surprise`).
  - `combo1`: fit on $[S_{\text{tr},g}, T_{\text{tr},g,j_{f,g}^*}]$ (`surprise` + the single best training-fold signal in group $g$).
  - `l2all`: fit on $[S_{\text{tr},g}, T_{\text{tr},g}]$ (`surprise` + all 22 candidates).
- **Endpoints (with $B = 2,000$ paired stem-cluster bootstrap CIs and one-sided $p(\Delta > 0)$):**
  1. **Primary (`dwg_l2all`):** Mean over eligible answer groups $g \in \{\text{YES}, \text{NO}\}$ ($\ge 20$ errors and $\ge 20$ correct rows in the cell, per `hvs.enough`) of the within-group OOF AUROC gain over fixed-sign `surprise`:
     $$\Delta_{\text{wg}} = \frac{1}{|G_{\text{elig}}|} \sum_{g \in G_{\text{elig}}} \left[\text{AUROC}(\text{err}_g, \hat{s}_{\text{l2all},g}) - \text{AUROC}(\text{err}_g, \text{surprise}_g)\right]$$
     computed inside every bootstrap resample so the CI and one-sided $p$-value are exact paired cluster-bootstrap statistics.
  2. **Within-group fold-sign baseline sensitivity (`dwg_l2all_vs_base`):** Same within-group mean gain, but comparing $\hat{s}_{\text{l2all},g}$ against $\hat{s}_{\text{base},g}$ (which learns the sign of `surprise` in group $g$).
  3. **Intercept-matched pooled gain (`dpool_l2all_vs_base`):** Pooled $\text{AUROC}(\text{err}, \hat{s}_{\text{l2all}}) - \text{AUROC}(\text{err}, \hat{s}_{\text{base}})$, where both arms include the per-group logistic-regression intercept $\beta_{0,g}$.
  4. **Single-signal incremental gain (`dwg_combo1` and `dpool_combo1_vs_base`).**
- **Multiplicity:** Holm–Bonferroni across (a) all 53 BENCH cells, (b) the 16 ANLI cells, and (c) per task across the 6 tasks.

## F5 — Gold-Label Review of the Most Confident ANLI R2 Errors

- Extract the top 30 lowest-`surprise` (highest pass-one confidence) error rows in each of the 8 BENCH `anli_r2` cells, plus the cross-model consensus error rows (items in `anli_r2_n1000.jsonl` where $\ge 6/8$ models commit the same wrong answer with high confidence).
- Review the top 30 most confident unique error items and the top consensus error items against their `Premise`, `Hypothesis`, and ANLI gold label (`0 = entailment`, `1 = contradiction`), categorizing each as:
  - **Clear model error** (gold label is unambiguous; model missed a negation, date arithmetic, coreference, or multi-hop step),
  - **Debatable / neutral-boundary gold label** (hypothesis is plausible or merely neutral rather than strictly entailed/contradicted, or relies on noisy crowdworker assumptions),
  - **Gold-label defect / mislabel** (gold label contradicts the premise text).
