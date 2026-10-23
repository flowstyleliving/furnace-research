# Chat-template extraction check on ANLI R2 own-error cells (plan, 2026-10-22)

**Status.** This plan was written and committed before any extraction in this directory existed. The only model call
before the commit is the template and tokenization check in §4, which loaded tokenizers only. MK approved the job by
voice on 2026-10-22, with a local-only constraint: no Modal and no paid compute.

**Question.** Is the negative-leaning ANLI own-error result (vault `wiki/results/harness-vs-signal-2026-10-13.md`)
partly an artifact of prompt formatting? In BENCH, 9 of the 10 models get the raw prompt (`raw_passthrough`) and only
Mistral-Nemo gets the chat template (`commit-confluence/vendor/t0_core/pri_v2_io_plugins.py:205-259`, hash
`6c56be18…`, the same hash recorded in every BENCH profile). This is one remaining extraction check. It is not
expected to fix ANLI.

## 1. Inputs and provenance

- **Code.** `commit-confluence` at `54f7bcc` is imported read-only, through `CONFLUENCE_T0_REPO=vendor/t0_core`. Its
  module hashes match the BENCH `module_hashes`. `PYTHONDONTWRITEBYTECODE=1` is set. No file in `commit-confluence` is
  edited.
- **Data.** `commit-confluence/stage_b/data_bench/anli_r2_seed20260711_n1000.jsonl`: 1,000 rows, 500 entailment
  (YES) and 500 contradiction (NO), neutral dropped. These are the same rows and order as BENCH.
- **Banked reference.** `commit-confluence/stage_b/profiles_bench/anli_r2/<model>.matrix.npz` (`1f70c9f`) and its
  labels in `…/harness_vs_signal/bench_labels/`.
- **Analysis code.** Frozen `hvs.py` at `d29a2e4` and `exploratory/hvs-followups-2026-10-22/run_followups.py`, both
  imported read-only.
- **Runtime.** mlx 0.29.3 and mlx-lm 0.29.1 in `commit-confluence/.venv` (Python 3.9), on an Apple M4 with 16 GB RAM.
  Free disk is about 2 GB, so outputs must be compact.

## 2. Cells (pre-stated selection rule)

**Rule.** Take the ANLI R2 cells whose premise-grouped E1 Δ has its 95% CI wholly below zero (F1,
`FOLLOWUP_RESULTS.json`), plus Mistral-Nemo as the reference that BENCH already templated. Run them in this order,
smallest model first:

| Order | Model | F1 E1 Δ [95% CI] | BENCH format | New condition |
|---|---|---|---|---|
| 1 | Phi-4-mini-instruct-4bit | −0.079 [−0.125, −0.032] | raw | template |
| 2 | Mistral-7B-Instruct-v0.3-4bit | −0.061 [−0.110, −0.014] | raw | template |
| 3 | Llama-3.1-8B-Instruct-4bit | −0.110 [−0.150, −0.067] | raw | template |
| 4 | Qwen3-8B-4bit | −0.130 [−0.181, −0.079] | raw | template (`enable_thinking=False`) |
| 5 | Mistral-Nemo-Instruct-2407-4bit (reference) | +0.003 [−0.028, +0.034] | template | raw |

R1 is out of scope for this run.

**Budget rule.** For each model, the BENCH-format (control) condition runs first, then the flipped condition, both at
n=1000. Before the full runs, a timing smoke on 5 rows of the control condition for model 1 records seconds per row.
Only timing is read from it; no feature or AUROC is inspected. If the projected total for all five models exceeds 14
hours of wall clock, models are dropped from the end of the order until it fits. The dropped models are reported as
not run. A model is never run in only one condition. Nothing here needs paid compute. If something turns out to need
it, the run stops and a price is reported instead.

## 3. Conditions: formatting is the only change

Both conditions call the same BENCH extractor functions in one process:
`confluence_calibrator.collect_ace_matrix(..., max_new_tokens=1)` and `collect_readout_matrix_fresh(...)` with seed
20260711. These are the functions `stage_b/run_bench.py:548-556` calls. Token positions and timing stay the same:
- ACE uses the prefill forward at the last prompt token.
- Surprise and the pass-one features come from that same forward.
- RPV, `p_max` and `null_ratio` are pass two, the forward on prompt + committed token.
- Decoding is a greedy full-vocabulary argmax.

The only change is the prompt string the strategy returns. That is done by patching `pri_v2_io_plugins.get_prompt_strategy` in process memory:
- **Template strategy:** `tokenizer.apply_chat_template([{"role": "user", "content": prompt}], tokenize=False,
  add_generation_prompt=True)`, with `enable_thinking=False` for Qwen3. If the tokenizer's `encode` adds a BOS
  automatically, the leading BOS text is removed from the template string. **Per-row assertion:**
  `encode(wrapped) == apply_chat_template(..., tokenize=True)`. A failure on any row aborts that model.
- **Raw strategy:** the prompt is passed unchanged, exactly as `raw_passthrough` does.
- **Mistral-Nemo:** the control uses the BENCH function itself (`apply_chat_template` from the plugin) and the flipped
  condition uses raw.

## 4. Template and tokenization check, done before this plan was committed (tokenizers only)

- 🚪 **Assistant openers.** The template string ends with the assistant turn opener for every model:
  - Phi-4 `<|end|><|assistant|>`;
  - Mistral-7B ` [/INST]`;
  - Llama-3.1 `<|start_header_id|>assistant<|end_header_id|>\n\n`;
  - Qwen3 `<|im_start|>assistant\n<think>\n\n</think>\n\n`;
  - Mistral-Nemo `[/INST]`.
- 🔁 **Doubled BOS.** Encoding the template string doubles the BOS for Mistral-7B (`[1, 1, …]`) and Llama-3.1-8B
  (`[128000, 128000, …]`), hence the strip and assertion in §3.
  - Mistral-Nemo has no doubled BOS: its encoded ids equal its template ids. That matches how BENCH tokenized it.
  - Phi-4 and Qwen3 add no BOS.
- 🔤 **YES/NO tokenization.**
  - Mistral-7B: `YES` and ` YES` are two tokens, `[1395, 3023]`; `Yes`, `yes`, `NO`, `No` and `no` are one token each.
  - All other models: every variant of YES/Yes/yes and NO/No/no, with and without a leading space, is a single token.

## 5. Per-row record (each condition)

- 📦 **BENCH columns.** The 27 BENCH panel columns, in BENCH order, plus `gen_token_ids`, `sample_idx`, `stem_ids`
  and `labels`.
- 🎯 **Verdict.** The decoded first token and the parsed verdict, using the `build_bench_labels.py` rule including the
  A2 prefix. That gives `error`.
- 📊 **Pass-one answer mass**, from `prefix_probs[-1]`:
  - `P_yes` and `P_no` each sum the probabilities of every token whose decoded `.strip().upper()` is `YES` (or `NO`),
    with and without a leading space, plus the first pieces of multi-token YES/NO encodings. For Mistral-7B, `▁Y` is
    included. That makes `P_yes` an upper bound, because `▁Y` can begin other words. This is recorded as a caveat;
    no extra forward is run to resolve it.
  - Also recorded: `margin = P_yes − P_no` and `mass = P_yes + P_no`.
- 🎲 **Surprise.** Pass one, as BENCH defines it.
- 🧭 **Pass-one RPV** at the last prompt token. This uses the readout distribution `prefix_probs[-1]` and the
  final-norm hidden state of the last prompt token, with the same statistics and the same late-layer + readout averaging
  as `comprehensive_run.py:396-470` (`fisher_eff_rank`, `spectral_entropy`, `neg_shadow_logvol_r1`), and K=512.
- ↔️ **Pass-one null_ratio:** `PRIComputer.compute_step` with `h_t` = the final-layer hidden at the last prompt token
  and `h_prev` = the second-to-last prompt token, with `p_t = prefix_probs[-1]`. This is the same step-0 locus as
  `pri_calibrator.py:590-603`.
- 🗜️ **Storage.** No full-vocabulary vector is saved. Outputs are a compressed npz plus a JSON manifest per (model,
  condition), and a run log.

## 6. Parity check (control condition)

The control condition must reproduce the banked BENCH matrix on the same rows:
- every `gen_token_id` is identical;
- for each of the 27 columns, max |new − banked| ≤ 1e-4 × max(1, |banked|), with the maximum deviation reported per
  column.

If tokens differ on more than 1% of rows, or the features fail the tolerance, that model's parity **fails**. It is
reported, and its comparison is still run against the new control. The banked matrix is not used in that case, and
the failure is flagged in every result. On parity failure the other models still run.

## 7. Analyses

Labels use the `build_bench_labels.py` rule. Folds are premise-grouped (`sha1(premise)`, as in F1), with `hvs.SEED`,
K=5, B=2000 premise-cluster bootstrap draws and P=1000 permutations.

**Registered for this check:**
- 🥇 **Primary.** For each cell and condition, E1 head-to-head: `hvs.run_test`, partialled, with the 22 candidates
  and fixed-sign surprise. The endpoint is the change **ΔE1(template − raw)**, with a paired premise-cluster bootstrap
  CI. Both conditions' out-of-fold scores are resampled on the same premise draws. The test is the one-sided
  bootstrap p for an increase (template is better for the signals), Holm-corrected across the cells that ran (up to 5).
  For Mistral-Nemo, the direction is reported as raw − template, and the cell is a reference, not a test.
- 🥈 **Secondary (descriptive, Holm within family, no verdict):**
  - accuracy, invalid rate, error counts per answer group, and the YES/NO answer split;
  - AUROC against own error for surprise, for `1 − P(committed verdict)` normalized over mass, and for `−|margin|`;
  - E1 Δ with the 22 candidates against margin-confidence instead of surprise;
  - pass-one RPV and pass-one null_ratio, each head to head with surprise within answer groups, and compared with
    their pass-two counterparts.

**Exploratory, labelled so everywhere:** the within-group L2 incremental test (F4 design: surprise + 22 candidates,
`C=1`, within answer group). The reference is surprise oriented by its training-fold sign (no refit), which avoids both
the fixed-sign and refit-pooling artifacts. A second variant adds the pass-one features. Holm across cells × conditions.

**Interpretation, stated in advance:**
- Template formatting "changes" a cell's head-to-head result only if ΔE1 is Holm-significant.
- A significant increase in some cells would show that formatting matters there. It would not overturn the ANLI
  verdict, which is registered on the banked BENCH data.
- No significant change would close the formatting explanation for these cells only, at this n.
- Accuracy changes are reported, but they are not evidence about signals.

## 8. Roles

- 🛠️ **Codex** (`codex exec`, `gpt-6-astra`) writes `extract_chat_template.py` to §3–§6.
- 🔍 **Claude** reviews the script, runs it locally, and writes `analyze_chat_template.py` for §7.
- 🐋 **DeepSeek** (`deepseek-v4-pro`, through `~/.local/bin/openrouter_review.py`) independently audits this plan and
  the extraction code before the run. A BLOCKER stops the run and is reported.
- 📝 **After results,** Codex and DeepSeek each audit the results and the analysis independently. If either tool is
  unavailable, the report says so and does not claim it took part.
