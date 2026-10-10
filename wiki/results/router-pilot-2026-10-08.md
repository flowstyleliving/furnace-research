# MoE router pilot — does router uncertainty carry the label signal? (2026-10-08)

**Status: [PRE-REGISTERED DESCRIPTIVE PILOT — spending decision STOP].** One model, two frozen
tasks, a single look. The only registered decision was whether further MoE compute is justified:
**it is not.** No confirmatory claim, no cross-model claim, no placement-law claim. Torch/Modal,
non-byte-comparable with sealed MLX panels; never pooled with depth grids A or B.

Design and audit trail: [[_archive/workorders/moe-router-pilot-workorder-2026-10-08]].
Repo lane: `commit-confluence/exploratory/router-pilot/` (uncommitted). Results:
`ROUTER_PILOT_RESULTS.json` / `.md`.

## The question

A mixture-of-experts (MoE) model sends each token through a few of many "expert" sub-networks,
chosen by a **router**. Dense models have no router, so the router's uncertainty is the one
MoE-native place a hallucination signal could live. The pilot asked: at the final prompt position,
does that uncertainty separate the dataset labels, at which layer, and does it beat the attention
instruments and the model's own output confidence measured in the same forward pass?

## Setup

- 🧠 **Model:** `allenai/OLMoE-1B-7B-0924-Instruct` @ `7f1c97f`, 16 layers, 64 experts with 8 active,
  native bf16, one A10G.
- 📚 **Data:** the frozen ANLI R1 and HaluEval-QA n=200 files; 5 stem-grouped folds (pairs never split).
- 📏 **Instruments, enumerated before capture:** 5 attention metrics × 16 layers; 3 router metrics ×
  16 layers (normalized entropy, top-8 boundary margin, top-8 mass); 3 output metrics (max
  probability, entropy, YES/NO log-odds) and prompt length. `v_norm_bos` was deprecated before the
  freeze; its replacement `sink_draw` ran as a descriptive diagnostic only.
- 🎯 **Spending rule:** PROCEED only if, on **both** tasks, the training-selected router column
  reaches held-out AUROC ≥ 0.65 **and** beats the best comparator by ≥ +0.03.
- 🧾 **Discipline:** four Codex audit rounds (RED → … → GO), FREEZE-1 logged before smoke, FREEZE-2
  pinning the prompt manifests before extraction, each cell extracted once, scorer run once.

## Gates and cost

Smoke passed every gate: attention reconstruction cosine ≥ 0.9999998 (relative error at most 6.72e-4); MoE
reconstruction cosine ≥ 0.99998 (relative error at most 6.13e-3, limit 1e-2) — the router features describe
the routing actually applied; router-output neutrality exactly 0; deterministic across repeats;
13.1 GiB peak. YES/NO compliance 97% (ANLI) and 100% (HaluEval). **Total GPU: 545 s = 0.15 GPU-hours, 7.6% of the
2 GPU-hour cap; 3 invocations, all closed.**

## Results

| | ANLI R1 | HaluEval-QA |
|---|---|---|
| **router_best** (held-out AUROC) | **0.529** [0.413, 0.668] | **0.832** [0.791, 0.876] |
| att_best | 0.614 [0.408, 0.672] | **0.904** [0.837, 0.934] |
| out_best (YES/NO log-odds in every fold) | 0.578 [0.410, 0.648] | 0.773 [0.722, 0.825] |
| prompt_len | 0.467 | 0.602 |
| **router − best comparator** | **−0.085** [−0.213, +0.102] | **−0.073** [−0.115, −0.001] |
| null 95th percentile, router_best | 0.580 | 0.586 |

Intervals: stem-cluster bootstrap, 5/95, conditional on the frozen folds.

- 🛑 **STOP, on both counts.** On ANLI the router is at chance (0.529, inside its own null) and its
  selection wanders across folds. On HaluEval the router is strong but loses to attention by 0.07.
- 🎯 **HaluEval's router signal is real and stable.** Router entropy at **layer 3 of 16** was
  selected in all five folds, held-out 0.83, far above the null's 95th percentile (0.586).
- 🗺️ **It sits early in the stack.** Router entropy peaks at layer 3, while the winning attention
  metric (`final_js`) peaks at layer 9 and `bos_mass` at layer 12. One model, descriptive only.
- ➕ **On HaluEval the router beats output confidence** (0.832 vs 0.773). This comparison is
  descriptive — the registered rule compares against the best comparator, which was attention.
- 🌫️ **ANLI is weak for everything on this model.** Attention 0.614 only just clears its null (95th
  0.600); output confidence 0.578.

## `sink_draw` — the `v_norm_bos` replacement is redundant

The sink draw (attention to position 0 × the value size there, averaged over heads) was added to
test whether a varying version of the deprecated `v_norm_bos` carries anything new. It does not:
its per-layer rank correlation with plain `bos_mass` is **0.935–0.994 (ANLI)** and
**0.954–0.998 (HaluEval)**, and on HaluEval both peak at layer 12. Because the position-0 value size
is fixed per head, the sink draw is `bos_mass` with fixed per-head weights. **Recommendation:
deprecate `v_norm_bos` without a replacement; `bos_mass` already carries the sink information.**

## Cautions

- 📐 **Percentile intervals from the stem-cluster bootstrap can sit off the point estimate.** The
  length arm on HaluEval reads 0.602, but its interval is [0.606, 0.643]. A resample that draws a stem
  twice counts its within-pair comparison more than once, and answer length separates a stem's two
  answers better than it separates different stems. Measured shift (bootstrap mean − observed):
  length +0.020, router +0.004, attention −0.007 on HaluEval. On ANLI, attention's −0.086 reflects
  unstable selection near chance. **The decision uses point estimates, so it is unaffected.** The
  morning's stem-grouped rescore was checked for the same effect: all nine HaluEval cells keep their
  dip inside the interval, with mixed-sign shifts ([[results/stem-grouped-sensitivity-2026-10-08]]).
- 🔬 **One model, n = 200.** A null on OLMoE does not rule out router signal in larger MoE models;
  it only fails the registered bar for spending more now.
- 🏷️ The labels are dataset labels, not this model's own errors.

## What this changes

- 💸 **No further MoE compute** under this line (registered spending rule).
- 🗑️ **`v_norm_bos` deprecated outright**, no replacement needed.
- 📄 The DC paper is frozen and unaffected. The ACE/CC caveat on `v_norm_bos` remains an open MK
  decision.

Cross-refs: [[results/three-instrument-2026-09-06]] (the `v_norm_bos` addendum) ·
[[results/stem-grouped-sensitivity-2026-10-08]] · [[research-candidates]] #13 ·
[[models/olmoe-1b-7b]].
