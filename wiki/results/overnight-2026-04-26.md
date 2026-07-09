# Overnight 2026-04-26 — auto-generated summary

_Generated 2026-04-25T12:16:20+00:00 by `scripts/diagnostics/overnight_summary.py` (path was `scripts/overnight_summary.py` at generation time; moved in chore reorg)._

Companion to [v3.1-replicate](v3.1-replicate.md). Stages run sequentially overnight; each stage has its own CSVs in `experiments/v3-main-run/2026-04-24/` (synthetic) or `experiments/factual_pairs/` (factual).

## Stage 1 — Paired Fisher distance, synthetic 2×2 puzzles, cross-model

Same prompt structure within pair, only contradiction bit flipped. Per-pair Fisher-Rao distance / KL / JSD / Hellinger.

| Model | N pairs | mean FR | median FR | mean JSD | mean KL(c→c̃) | mean KL(c̃→c) | KL asym ratio | argmax-flip rate |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Llama 3.2 3B | 50 | 0.124 | 0.114 | 0.002 | 0.009 | 0.009 | 0.96 | 2% |
| Mistral 7B | 50 | 0.036 | 0.035 | 0.000 | 0.001 | 0.001 | 1.36 | 0% |
| Qwen 2.5 7B | 50 | 1.880 | 1.922 | 0.325 | 4.759 | 2.006 | 2.37 | 94% |
| Qwen 3 8B | 50 | 0.365 | 0.374 | 0.017 | 0.070 | 0.071 | 0.99 | 40% |

## Stage 2 — J_n-corrected null_ratio at N=200 (sealed sample size), cross-model

Sealed-equivalent N. Δ AUROC(Fisher) − AUROC(raw) at rank=1 under proper Fisher pullback (J_n correction). Sealed E17b bar: Δ ≥ +0.02 with non-overlap CI.

| Model | N | Δ(F-R) at rank=1 | 95% CI | sealed verdict |
|---|:---:|:---:|:---|:---:|
| Llama 3.2 3B | 100 (only N=100; expected N=200) | +0.0536 | [-0.1317, +0.2259] | borderline |
| Mistral 7B | 100 (only N=100; expected N=200) | -0.1836 | [-0.2642, -0.1098] | FAIL |
| Qwen 2.5 7B | 100 (only N=100; expected N=200) | +0.0148 | [-0.0833, +0.1084] | borderline |
| Qwen 3 8B | 100 (only N=100; expected N=200) | +0.2064 | [+0.0312, +0.3871] | ✅ PASS |

Per-rank table for each model in the underlying CSVs at `experiments/v3-main-run/2026-04-24/norm_diagnostic_<MODEL>.csv`.

## Stage 3 — Factual baseline (unpaired TriviaQA-style), cross-model

60 hand-curated factual questions, prompt format `"Question: <Q>\nAnswer:"`. Per-question: surprise on correct first-token, surprise on wrong first-token, log-ratio (>0 means model prefers correct).

| Model | N | mean S(correct) | mean S(wrong) | mean log(p_corr/p_wrong) | prefers correct | top1 = correct first tok |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| Llama 3.2 3B | 60 | 21.16 | 21.16 | +0.00 | 0% | 0% |
| Mistral 7B | 60 | 26.49 | 26.49 | +0.00 | 0% | 0% |
| Qwen 2.5 7B | 60 | 3.05 | 10.34 | +7.29 | 97% | 22% |
| Qwen 3 8B | 60 | 2.50 | 9.31 | +6.81 | 93% | 22% |

## Stage 4 — Factual paired Fisher distance (TriviaQA-style)

Same factual pairs as Stage 3, but now BOTH the correct-answer-proposed and wrong-answer-proposed prompts are run; paired-Fisher metric per pair.

| Model | N pairs | mean FR | median FR | mean JSD | mean KL(c→c̃) | argmax-flip rate |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| Llama 3.2 3B | 60 | 1.309 | 1.286 | 0.232 | 1.070 | 53% |
| Mistral 7B | 60 | 2.094 | 2.627 | 0.452 | 2.839 | 75% |
| Qwen 2.5 7B | 60 | 2.764 | 3.108 | 0.606 | 15.139 | 90% |
| Qwen 3 8B | 60 | 2.540 | 2.992 | 0.556 | 5.961 | 87% |

## Headline comparison — does paired Fisher generalize from synthetic to factual?

| Model | Synth FR (Stage 1) | Factual FR (Stage 4) | Δ (factual − synth) |
|---|:---:|:---:|:---:|
| Llama 3.2 3B | 0.124 | 1.309 | +1.185 |
| Mistral 7B | 0.036 | 2.094 | +2.058 |
| Qwen 2.5 7B | 1.880 | 2.764 | +0.883 |
| Qwen 3 8B | 0.365 | 2.540 | +2.175 |

If factual FR is meaningfully > 0 across models AND tracks synthetic FR direction, the paired Fisher metric generalizes to natural language and is a candidate v3-paper second-pillar metric. If factual FR is near 0 or noise, the metric is template-bound (claim narrowly).

## Underlying CSVs (paths)

Synthetic 2×2:
- `experiments/v3-main-run/2026-04-24/paired_fisher_Llama-3.2-3B-Instruct-4bit.csv` — Stage 1
- `experiments/v3-main-run/2026-04-24/norm_diagnostic_Llama-3.2-3B-Instruct-4bit.csv` — Stage 2 (N=200)
- `experiments/v3-main-run/2026-04-24/paired_fisher_Mistral-7B-Instruct-v0.3-4bit.csv` — Stage 1
- `experiments/v3-main-run/2026-04-24/norm_diagnostic_Mistral-7B-Instruct-v0.3-4bit.csv` — Stage 2 (N=200)
- `experiments/v3-main-run/2026-04-24/paired_fisher_Qwen2.5-7B-Instruct-4bit.csv` — Stage 1
- `experiments/v3-main-run/2026-04-24/norm_diagnostic_Qwen2.5-7B-Instruct-4bit.csv` — Stage 2 (N=200)
- `experiments/v3-main-run/2026-04-24/paired_fisher_Qwen3-8B-4bit.csv` — Stage 1
- `experiments/v3-main-run/2026-04-24/norm_diagnostic_Qwen3-8B-4bit.csv` — Stage 2 (N=200)

Factual:
- `experiments/factual_pairs/factual_baseline_Llama-3.2-3B-Instruct-4bit.csv` — Stage 3 (unpaired)
- `experiments/factual_pairs/factual_paired_fisher_Llama-3.2-3B-Instruct-4bit.csv` — Stage 4 (paired)
- `experiments/factual_pairs/factual_baseline_Mistral-7B-Instruct-v0.3-4bit.csv` — Stage 3 (unpaired)
- `experiments/factual_pairs/factual_paired_fisher_Mistral-7B-Instruct-v0.3-4bit.csv` — Stage 4 (paired)
- `experiments/factual_pairs/factual_baseline_Qwen2.5-7B-Instruct-4bit.csv` — Stage 3 (unpaired)
- `experiments/factual_pairs/factual_paired_fisher_Qwen2.5-7B-Instruct-4bit.csv` — Stage 4 (paired)
- `experiments/factual_pairs/factual_baseline_Qwen3-8B-4bit.csv` — Stage 3 (unpaired)
- `experiments/factual_pairs/factual_paired_fisher_Qwen3-8B-4bit.csv` — Stage 4 (paired)
