---
status: OPEN
kind: step3-factual-rung-pilot
date: 2026-05-25
---
# TriviaQA Factual-Rung Pilot — Step 3 (2026-05-25)

**Status:** `[OPEN]` — sweep complete; verdict below.
**Companion:** [[step0-belief-readout-2026-05-17]] (belief-readout panel, same 9 models minus Phi-3.5)
**Why this ran:** Step 3 of the v4 play sprint — test whether attention-side features (js_radius, bos_mass, v_norm, etc.) transfer from synthetic ANLI contradictions to natural-language TriviaQA factual disagreements.

## Dataset

- **Source:** TriviaQA `rc.wikipedia` / `validation` split (HuggingFace `trivia_qa`)
- **Design:** 50 unique questions × 2 prompts (correct answer / cross-sampled wrong answer) = 100 samples
- **Label convention:** label=0 = correct answer (YES expected); label=1 = wrong answer (NO expected) — mirrors ANLI schema
- **Wrong-answer selection:** cross-sampled canonical answer from a different question; collision-guarded against all aliases (case-insensitive); unique wrong answers (no reuse across pairs)
- **Prompt format:**
  ```
  Instruction: Read the question and proposed answer, then decide whether the proposed answer is correct. Answer YES if the proposed answer is correct, NO if the proposed answer is incorrect.

  Question: {question}
  Proposed answer: {answer}
  Answer:
  ```
- **Seed:** 20260525; **shuffled:** yes
- **Data hash (sha256):** `91d79875e3727c53861ab6ddb89bdbbfe9555b6e53344639b011935d7677098b`
- **Artifacts:**
  - `experiments/triviaqa-paired/2026-05-25/n100.jsonl`
  - `experiments/triviaqa-paired/2026-05-25/n100.manifest.json`
  - `scripts/generate_triviaqa_paired.py`

## Calibrator run spec (Step 3.2)

- **Flags:** `--attention-with-v-norms --attention-only --n-bootstrap 200 --max-new-tokens 4`
- **Task label:** `triviaqa_paired_n100_v_norms_step3`
- **Panel:** 9 models (Phi-3.5 excluded — real low-decidedness state, see [[step0-phi35-locus-offset-audit-2026-05-25]])
- **Comparability:** identical invocation to Step 1 Phase 3 ANLI sweep → ANLI↔TriviaQA cell-winner comparison is the primary Step 3.3 analysis
- **Runner:** `scripts/run_triviaqa_calibrator_sweep.sh`
- **Output dir:** `experiments/triviaqa-paired/2026-05-25/calibrator/v_norms/`

## Per-model results (Step 3.2)

Winner = OOB AUROC median with CI_lo > 0.50 at best coverage. All 9 models succeed.

| Model | Winner cell | OOB AUROC [95% CI] | stability | Notes |
|---|---|---|---|---|
| Qwen3-1.7B-4bit | `mid_js_no_bos @ final step=1` sgn=+1 | 0.716 [0.538, 0.853] | 0.57 | ⚠️ winner_unstable |
| Llama-3.2-3B-Instruct-4bit | `mid_js_no_bos @ final step=1` sgn=+1 | 0.813 [0.697, 0.911] | 0.35 | ⚠️ winner_unstable |
| gemma-3-4b-it-4bit | `mid_v_norm_lastq_weighted @ final step=1` sgn=+1 | 0.706 [0.537, 0.840] | 0.41 | ⚠️ winner_unstable |
| Phi-3.5-mini-instruct-4bit | `mid_v_norm_lastq_weighted @ final step=1` sgn=+1 | 0.877 [0.689, 0.958] | 0.92 | clean |
| Phi-4-mini-instruct-4bit | `mid_js_kv_groups @ final step=1` sgn=+1 | 0.893 [0.803, 0.980] | 0.83 | clean |
| Mistral-7B-Instruct-v0.3-4bit | `final_v_norm_lastq_weighted @ final step=1` sgn=+1 | 0.935 [0.831, 1.000] | 0.47 | ⚠️ winner_unstable |
| Qwen2.5-7B-Instruct-4bit | `final_bos_mass @ final step=1` sgn=+1 | 0.949 [0.871, 1.000] | 0.98 | clean; best in panel |
| Qwen3-8B-4bit | `mid_v_norm_lastq_weighted @ final step=1` sgn=+1 | 0.903 [0.805, 0.991] | 0.65 | ⚠️ winner_unstable |
| Mistral-Nemo-Instruct-2407-4bit | `last_minus_1_js_kv_groups @ final step=1` sgn=−1 | 0.922 [0.850, 0.992] | 0.42 | ⚠️ winner_unstable; only sgn=−1 |

**Notable:** layer=`final`, step=1 universal across all 9. Metric varies. Sign=+1 on 8/9 (Nemo exception, consistent with ANLI).

## Step 3.3 — ANLI↔TriviaQA winner comparison

Reference ANLI winners from Step 1 Phase 3: `experiments/v4-prep-calibrator-sweep/2026-05-16/run-01/v_norms/`.

| Model | ANLI winner (step=1) | TriviaQA winner (step=1) | Match? |
|---|---|---|---|
| Qwen3-1.7B-4bit | `last_minus_1_js` sgn=+1 ⚠️ | `mid_js_no_bos` sgn=+1 ⚠️ | ❌ |
| Llama-3.2-3B-Instruct-4bit | `mid_js_no_bos` sgn=**−1** | `mid_js_no_bos` sgn=**+1** ⚠️ | ❌ (sign flip) |
| gemma-3-4b-it-4bit | `mid_v_norm_lastq_weighted` sgn=+1 ⚠️ | `mid_v_norm_lastq_weighted` sgn=+1 ⚠️ | ✅ |
| Phi-3.5-mini-instruct-4bit | `last_minus_1_js_no_bos` sgn=+1 | `mid_v_norm_lastq_weighted` sgn=+1 | ❌ |
| Phi-4-mini-instruct-4bit | `final_js_kv_groups` sgn=+1 ⚠️ | `mid_js_kv_groups` sgn=+1 | ❌ (sublayer shift) |
| Mistral-7B-Instruct-v0.3-4bit | `last_minus_1_bos_mass` sgn=**−1** ⚠️ | `final_v_norm_lastq_weighted` sgn=+1 ⚠️ | ❌ |
| Qwen2.5-7B-Instruct-4bit | `last_minus_1_js_no_bos` sgn=+1 | `final_bos_mass` sgn=+1 | ❌ |
| Qwen3-8B-4bit | `last_minus_1_js_kv_groups` sgn=**−1** | `mid_v_norm_lastq_weighted` sgn=+1 ⚠️ | ❌ |
| Mistral-Nemo-Instruct-2407-4bit | `final_js` sgn=**−1** ⚠️ | `last_minus_1_js_kv_groups` sgn=**−1** ⚠️ | ❌ |

**Cell match: 1/9** (gemma-3-4b only). Replicates ANLI R1↔R2↔R3 generalization failure pattern.

**Partial structural regularities across both datasets:**
- Layer=`final`, step=1: universal (100% stable across ANLI and TriviaQA)
- `mid_v_norm_lastq_weighted` dominant in TriviaQA (4/9 models); less so in ANLI
- Sign=+1 dominant (8/9 TriviaQA; ANLI sign is more mixed — 3 models flip to −1 on ANLI)
- Llama sign flip: `mid_js_no_bos` sgn=−1 on ANLI → sgn=+1 on TriviaQA (same cell, direction reverses)

## Step 3.4 — Verdict

**Outcome: 🟡 Partial structural transfer — calibrator works, no universal cell.**

1. **Calibrator is viable on TriviaQA.** All 9 models achieve OOB AUROC [0.706, 0.949], CI_lo > 0.50, confirming attention features are discriminative for factual YES/NO agreement. This is a positive result.
2. **No universal winning cell across ANLI↔TriviaQA.** 1/9 match replicates the ANLI R1↔R2↔R3 finding: per-(model, exact task distribution) calibration is load-bearing; the winner is not portable.
3. **Layer and step are portable; metric and sign are not.** `final @ step=1` is universal. The metric family that wins depends on the task domain.
4. **Sign instability is a live concern.** Llama's sign flip on `mid_js_no_bos` (−1 on ANLI, +1 on TriviaQA) means a detector trained on ANLI would invert on TriviaQA for that model. This is the strongest argument for per-task recalibration.
5. **`v_norm_lastq_weighted` rises on TriviaQA.** Wins 4/9 models vs fewer on ANLI — worth noting in Step 5 paper narrative.
6. **Pre-reg constraint (must state):** this is descriptive. Step 3 is a pilot; no pre-registered bars; findings are `[OPEN]`, not `[VALIDATED]`.

## Propagates to / read alongside

- [[step0-belief-readout-2026-05-17]] — belief-readout panel for the same 9 models
- [[step0-phi35-locus-offset-audit-2026-05-25]] — why Phi-3.5 is excluded
- [[v4-prep-coverage-matrix-2026-05-16]] — ANLI R1 calibrator sweep (Step 1 Phase 3) — the comparison baseline
- [[rauq-sinkprobe-vs-ours-2026-05-16]] — Step 2 baselines (same panel)
- [[claims]] — Step 3 claim entries (after verdict)
