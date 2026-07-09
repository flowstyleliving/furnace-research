# RAUQ + SinkProbe vs Ours — Head-to-Head (v4 play-sprint Step 2.4)

**Status:** 🟡 **[OPEN]** — descriptive feeder document for the [[research-candidates|Step 5]]ep 5]] paper-scope memo. **NOT a paper section. NOT [VALIDATED]** (HARD RULE: no promotion without a sealed pre-reg). This is the honest "where we win, where we lose, where it's a wash" read that Step 5 consumes — written to find the paper's headline, not to confirm one.

Feeds: the [v4 play sprint](../../../.claude/plans/elegant-meandering-mochi.md) Step 5 synthesis. Substrate: [[v4-prep-coverage-matrix-2026-05-16]] (Step 1) + the RAUQ/SinkProbe baselines (Step 2.1/2.2). Related: [[inter-head-disagreement-2026-05-15]] (the run-02 "sink-driven" verdict tested below), [[claims]].

> ⚠️ **t=0 caveat ([[step0-belief-readout-2026-05-17]], 2026-05-17):** the belief-readout panel **re-grounds the commit-step *premise*** (a discriminative t=0 logit locus exists; Mistral-Nemo anchor 0.99 passed) but the frozen pre-reg explicitly bars this from validating the specific `gen_step=1` *attention* numbers here — for CoT-tuned models those were measured at a reasoning-preamble token and still need re-measurement at the logit-defined locus. **Phi-3.5-mini is Low-decidedness-for-M at t=0** (eligible_cov 0.185) — a tension vs its Step-1 "clean trustworthy" status. Premise re-grounded ≠ these readings validated.

---

## What was compared

RAUQ and SinkProbe — previously only *named as prior art* — scored **side-by-side with our calibrator cells on the identical panel**: same 9-model panel + Llama-3.1-8B (baseline-only reproduction target), same **byte-identical n=200 ANLI R1** slice. Data-hash parity (`94825f3d2029c004…`) is **TRUE on all 10 models** — the join is provably on the same data, not a loose alignment.

| Artifact | Path |
|---|---|
| 📊 Head-to-head CSV | `experiments/v4-prep-calibrator-sweep/2026-05-16/run-01/head_to_head.csv` |
| 🧮 RAUQ profiles | `experiments/v4-baselines/2026-05-16/run-01/rauq/*.rauq.json` (PR #14) |
| 🪞 SinkProbe profiles | `experiments/v4-baselines/2026-05-16/run-01/sinkprobe/*.sinkprobe.json` (PR #15) |
| 🔧 Populator | [`scripts/build_v4_coverage_matrix.py`](../../../Documents/PRI_at_commitment/scripts/build_v4_coverage_matrix.py) (PR #16, Greptile 5/5) |

### Honesty rails (how "win" is decided)

- **Ours** = the Step-1 calibrator winner per model, scored by **OOB median** (selection-bias-corrected), with a `clean`/`flagged` trust flag (OOB CI excludes 0.5 ∧ winner_stability ≥ 0.70). The flagged Mistral-7B multistep `last_minus_1_js@step3` fluke auto-demotes.
- **Baselines** = best **single-layer FIXED-direction** AUROC. RAUQ's native max-over-layers aggregate is **not** used as the comparator — it *sandbags* badly when per-layer directions disagree (see Observation 1), so reporting best-single-layer is the **charitable-to-RAUQ** choice. Sign-free `max(a, 1−a)` is a secondary sensitivity column only.
- Pinned + **untuned** constants (tuning on labels would leak): RAUQ α = 0.5; SinkProbe k = 4. RAUQ restricted to the **3 panel layers** (not full-depth RAUQ) — a noted limitation, charitable framing stated.
- Setting differs from the baselines' own papers (commit-step only; ANLI not HaluEvalQA; RAUQ recurrence over the prompt, not a generation). Absolute numbers are **not** the papers' numbers — this is a loose, same-setting comparison, not a reproduction.

---

## Head-to-head table (fixed-direction; sign-free in parens)

| Model | ours (OOB) | trust | RAUQ best | SinkProbe best | winner |
|---|---|:--:|---|---|:--:|
| Phi-3.5-mini | **0.774** | clean | 1b/final 0.721 | sink_topk_sum_vw/mid 0.618 | **ours** |
| Qwen2.5-7B | **0.818** | clean | 1a/lm1 0.634 | sink_topk_sum_vw/final 0.650 | **ours** |
| Llama-3.2-3B | 0.655 | clean | 1a/mid **0.678** | sink_topk_sum_vw/lm1 0.565 | RAUQ |
| Qwen3-8B | 0.804 | clean | 1b/final 0.425 (sf 0.575) | sink_top1_vw/lm1 **0.807** | SinkProbe |
| Mistral-7B | 0.728 | ⚠ flagged | 1a/final **0.734** | sink_topk_sum_vw/final 0.563 | RAUQ |
| Phi-4-mini | 0.720 | ⚠ flagged | 1a/mid **0.729** | sink_top1/final 0.570 | RAUQ |
| Mistral-Nemo | 0.774 | ⚠ flagged | 1b/lm1 0.228 (sf 0.772) | sink_top1_vw/final **0.867** | SinkProbe |
| Qwen3-1.7B | 0.587 | ⚠ flagged | 1b/final 0.580 | sink_top1_vw/mid 0.554 | ours* |
| gemma-3-4b | 0.760 | ⚠ flagged | 1a/mid 0.550 | sink_top1/final 0.647 | ours* |
| Llama-3.1-8B | — | baseline-only | 1b/lm1 0.516 | sink_topk_sum_vw/final **0.687** | SinkProbe |

`ours*` = winner_fixed is "ours" but `ours` is OOB-`flagged` → not a trustworthy win. Both winner columns (fixed **and** sign-free) agree on all 10 models after the PR-#16 round-4 fix.

---

## Where we win / lose / wash — the honest read

The only honest comparisons are the **4 models where our calibrator number is OOB-trustworthy** (`clean`): Phi-3.5, Qwen2.5, Llama-3.2-3B, Qwen3-8B. On those four:

- ✅ **Clean wins: 2** — Phi-3.5 (0.774 vs RAUQ 0.721 / Sink 0.618) and Qwen2.5 (0.818 vs RAUQ 0.634 / Sink 0.650). Decisive.
- ❌ **Clean loss: 1** — Llama-3.2-3B: RAUQ 1a/mid **0.678** > ours-clean 0.655. RAUQ genuinely beats us here.
- 🤝 **Dead heat: 1** — Qwen3-8B: SinkProbe `sink_top1_vw/lm1` **0.807** vs ours-clean 0.804. A 0.003 gap — statistically a wash; SinkProbe edges *both* columns.

On the **5 flagged-ours models**, RAUQ wins 2 (Mistral-7B, Phi-4-mini) and SinkProbe 1 (Mistral-Nemo), but ours' own number is untrustworthy there → **these are not clean losses**, just "nobody has a trustworthy number." Qwen3-1.7B / gemma-3-4b show winner=ours but flagged → not real wins. Llama-3.1-8B is baseline-only (SinkProbe 0.687).

> **Honest headline for Step 5:** where our calibrator is OOB-trustworthy, ours **clearly wins 2/4, loses 1, dead-heats 1**. The prior-art baselines are *competitive*, not dominated. The defensible paper claim is **"per-(model, distribution) calibration with honest baselines on the same panel"**, **not** "we beat RAUQ/SinkProbe." Any "we win" framing would be spin the data does not support.

---

## Cross-cutting [OPEN] observations (Step 5 raw material — no promotion)

1. 🎭 **RAUQ aggregate sandbagging.** RAUQ's native max-over-layers, fixed-direction, collapses far below best-single-layer when per-layer directions disagree: Qwen2.5 0.634 → agg 0.31; Llama-3.2-3B 0.678 → 0.42; Mistral-Nemo 0.23 → 0.15. We deliberately report best-single-layer (charitable); even so RAUQ wins only 3/10. A paper using RAUQ's *native* aggregate would understate it dramatically — flag this if RAUQ is cited.
2. 🪞 **RAUQ sign-flip.** On Mistral-Nemo (0.228) and Qwen3-8B (0.425), RAUQ's honest fixed-direction is **below chance** — only sign-free rescues it (sf 0.77 / 0.57). Echoes Step-1 finding #5 (Mistral-7B `bos_mass sign=−1`): a recurring "low signal → contradiction" inversion on Mistral/Qwen-large.
3. 🧲 **SinkProbe ‖V‖-weighted column-sum dominates — 7/10 best cells are `*_vw`.** Sharp contrast with Step-1 finding 🪤 ([[v4-prep-coverage-matrix-2026-05-16]]: the *last-query* `v_norm_*` cells won on only 1/9). The **column-sum** ‖V‖ weighting is far more competitive than the last-query approximation — a real methodological point for Step 5.
4. ⚔️ **The two prior-art baselines disagree in direction.** On Mistral-Nemo & Qwen3-8B, RAUQ runs `lo` (low uncertainty → contradiction) while SinkProbe runs strong `hi` (high sink → contradiction). Not noise — a genuine "prior art does not agree on the mechanism" talking point.
5. 🌊 **Sink-driven framing only half-holds.** Plan predicted SinkProbe ≥ ours-`js*` on the two SinkProbe-aligned models. **Mistral-Nemo confirms** (SinkProbe sf 0.867 ≥ ours-js\* 0.800). **Llama-3.2-3B does not** (ours-js\* 0.683 > SinkProbe 0.565). The [[inter-head-disagreement-2026-05-15]] run-02 "sink-driven" verdict is supported for Nemo, **not** Llama-3.2-3B — report without spin.
6. 🔗 **Both winner columns agree on all 10** after the PR-#16 round-4 `winner_signfree` fix. The earlier "Qwen3-8B is a wash that flips to ours on sign-free" claim was a **bug artifact** (in-sample-ours vs baseline-sign-free) — **retracted**; corrected in handoff/memory/log. No model has ours winning sign-free while losing fixed.

---

## What this is NOT

- Not a paper section — Step 5 decides scope; this only feeds it.
- Not `[VALIDATED]` — descriptive; any promotion needs a sealed pre-reg (HARD RULE).
- Not a reproduction of the RAUQ/SinkProbe papers — different setting (commit-step, ANLI), loose same-panel comparison only.
- Not the final word on RAUQ — its native aggregate was deliberately bypassed (charitable); a hostile reviewer could argue either way, which is itself a Step-5 scoping input.

---

_Generated 2026-05-17 from the post-round-4 `head_to_head.csv`. Re-run [`scripts/build_v4_coverage_matrix.py`](../../../Documents/PRI_at_commitment/scripts/build_v4_coverage_matrix.py) to refresh; idempotent, non-destructive to `coverage_matrix.csv`._
