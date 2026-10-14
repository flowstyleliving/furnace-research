# MoE commit-moment detector check — does the unchanged detector run on MoE models? (2026-10-12 → 2026-10-13)

**Status: [OPEN — descriptive, unregistered].** An instrument check across three MoE models and one
dense control, ANLI R1, n=200. Torch bf16 with chat-template prompts: **non-byte-comparable** with
the sealed MLX 4-bit panels and never pooled with them. It moves no registered verdict.

> ⚠️ **Correction, 2026-10-13 (same day): the target was the dataset class, not the model's errors.**
> Every AUROC on this page, including Qwen1.5-MoE's "meets", was fitted to the ANLI class label
> (entailment versus contradiction), verified in `pri_calibrator.py:516` and the data manifest. Re-scored
> against each model's own wrong answers with the unchanged sealed selector, **no model meets the bar**:
> Granite 0.517 [0.393, 0.618], Qwen3-1.7B 0.475 [0.356, 0.582], Qwen1.5-MoE 0.585 [0.398, 0.710].
> The class scores are strongly associated with the model's own answer (cells predict it at AUROC 0.90–0.98).
> The tables below are kept as first reported; read "meets" as **meets for task-class discrimination**.
> → [[results/correctness-labels-2026-10-13]]

Repo lane: `commit-confluence/exploratory/moe-detector-check/` (`RESULTS.md` holds the full
tables). Commits: `60944ad` (local detector + CPU results) and `65e6540` (Modal wrapper + Modal runs),
both pushed to `commit-confluence` `origin/main`. Prior entry: [[log]] 2026-10-12, "Commit-moment detector on an MoE model".
Related: [[results/router-pilot-2026-10-08]] (OLMoE router uncertainty, STOP).

## The question

The deployed commit-moment detector reads attention and readout geometry at fixed layers
(N//2, N−2, N−1), at the moment the model commits to its one-token YES/NO answer. MoE models route
each token through a few of many expert sub-networks. MoE routing sits in the feed-forward block,
not in attention, so the detector needs no MoE-specific capture. The open question is whether the
**unchanged** detector runs cleanly on MoE architectures, and whether it clears a usable bar there.

**Target (stated by MK):** median out-of-bag AUROC ≥ 0.55 **and** 95% CI lower bound > 0.5.

## Setup

- 🧰 **Detector, unchanged.** 21 ACE cells and 6 readout cells; D0 (prompt only) and D1 (prompt
  plus committed token); the sealed selector with 2,000 bootstraps and seed 20260612; shuffled-label
  controls and fusion enabled. Codex `gpt-6-astra` wrote the adapter, which fails loudly instead of
  turning missing or non-finite scores into 0.0, the bug at old `modal_app.py:1050`.
- 🔬 **Checks before and during extraction, on all three layers.** Attention-output reconstruction
  (direction and magnitude), logit parity against the model's own final norm and output head,
  attention row sums, and future-token leakage over every query row.
- ☁️ **Modal wrapper (2026-10-13).** Pinned checkpoint and tokenizer SHA, Transformers 5.19.0,
  torch 2.14.1+cu126, bf16, one A100-80GB, eager attention. Per-run spend ceilings were derived from
  the Modal timeouts, under a $10 hard cap for the whole task.
- 🐛 **One adapter bug caught before spend.** `enable_thinking=False` was applied only to
  `model_type == "qwen3"`, so Qwen3-30B-A3B (`qwen3_moe`) would have kept thinking on. It is now
  fixed and guarded by a check on the rendered template.

## Results

| Model | Type | Best cell | OOB AUROC [95% CI] | Target |
|---|---|---|---|---|
| Granite-3.1-1B-A400M-instruct | MoE (local CPU) | `mid_bos_mass` | 0.633 [0.428, 0.739] | miss |
| Qwen3-1.7B | dense control (local CPU) | `final_js_no_bos` | 0.605 [0.443, 0.710] | miss |
| Qwen1.5-MoE-A2.7B-Chat | MoE (Modal) | `final_v_norm_lastq_weighted` | **0.710 [0.602, 0.799]** | **meets** |
| Qwen3-30B-A3B | MoE (Modal) | — | not scored: behaviour gate | — |
| OLMoE-1B-7B-0924-Instruct | MoE | — | not run: not compatible | — |

- ✅ **The instrument runs exactly on all three MoE architectures tried** (granitemoe, qwen2_moe,
  qwen3_moe). Worst case over every forward pass: reconstruction cosine ≥ 0.99999, relative error
  ≤ 0.45%, row-sum error ≤ 0.0033, zero future-token leakage, final-norm parity ≤ 0.4% and logit
  parity ≤ 1.0%.
- 🎯 **One MoE model clears the target, one misses, one cannot be scored.** Qwen1.5-MoE meets it
  at 0.710 [0.602, 0.799], with shuffled-label controls passing. Its winning cell is chosen in
  only 37% of resamples. The interval already includes that selection noise, but which cell
  carries the signal is unstable. Granite misses (CI lower bound 0.428), as does the dense control
  (0.443).
- 🚧 **Qwen3-30B-A3B fails the preregistered behaviour gate.** Thinking is off, verified on the
  rendered prompt. Its first token on validation rows 0 and 1 is `Answer`, not YES or NO, so no
  label is committed at the measured position. This is the same failure class as
  Mistral-Small-3.2's `To` in the depth grid. Every numerical check passed. Per the no-silent-gate-
  override rule there was no retry and no prompt change.
- 🔒 **OLMoE is not compatible with the preregistered readout** (MK decision 2026-10-13). Its config
  leaves the epsilon at the Transformers default `1e-5`, while the sealed readout's final RMSNorm is
  fixed at `1e-6`. It was not run, at $0.

**What this does and does not show.** The detector's capture and readout transfer to standard-attention
MoE models without modification. **No MoE-versus-dense claim follows.** Three scored models, one
task, mixed backends (local CPU against Modal GPU) and different sizes cannot separate architecture
from model. The sealed MLX 4-bit Qwen3-1.7B profile reads 0.688 [0.535, 0.785] against 0.605 here,
which is a reminder that backend and prompt path matter.

## Spend and compute

**Billed by Modal: $2.03 in total** (Modal's per-app billing report, reconciled into the lane's
`modal_spend_ledger.json`), against $1.96 measured from container wall clock at list price, $6.95
of reserved ceilings and the $10 cap. GPU time: 0.619 A100-80GB hours. Rows are in [[references/gpu-ledger]]. The smoke run (12 rows) passed every
check, then exhausted its $0.80 budget inside the CPU-bound sealed calibration. That calibration
took 18 min 47 s at n=200 while the GPU sat idle (from Modal's timestamped logs). Cached weights (89.7 GB) were deleted from the
Modal volume afterwards to stop storage charges.

## Open decisions for MK

- Whether to try Qwen3-30B-A3B under an amendment, for example with the non-thinking
  `Qwen3-30B-A3B-Instruct-2507` checkpoint or a prompt that forces a bare label. Either is a new
  registration, not a rerun.
- Whether a second task (HaluEval QA) is worth adding for Qwen1.5-MoE, to test whether its 0.710 is
  task-specific.
