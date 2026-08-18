# Phi-4-mini Instruct (4-bit)

MLX handle: `mlx-community/Phi-4-mini-instruct-4bit`

## Specs
- Size: 3.8B parameters
- Quantization: 4-bit (MLX)
- Backend: MLX
- Output projection: untied `lm_head`

## Role in the research line
- Phi-family era comparator against Phi-3.5-mini.
- Attention-side v4 expansion model.
- t=0 residual-stream counterexample to any simple "newer Phi flips positive" story.

## Main verdicts
- `v4-sealed-2026-05-26` — ANLI passes with `mid_v_norm_lastq_weighted @ step 0`; TriviaQA transfers only partially and the winner changes.
- `v4-prep-coverage-matrix-2026-05-16` — `final_js_kv_groups @ step 1`, OOB 0.7202, sign +1; borderline but deployable.
- `step0-belief-readout-2026-05-17` — Recoverable-for-M at t=0, coverage 1.000, AUROC_B 0.840 [0.784, 0.894].
- `inter-head-disagreement-2026-05-15` — clean `hi`-orientation signal at final layer under the sink-controlled lens.
- `delta-sigma-onaxis-2026-05-15` — `Δσ_onaxis` alone beats the best null at rank 4 with the opposite sign from Phi-3.5.
- `depth-marginals-2026-08-16` — mid-heavy depth signature: the js-family top rung is mid-stack in 13/18 BENCH cells (mid mean 0.722 vs 0.629/0.614) — opposite end of the stack from the Qwen/Mistral N−2 peak.
- `t0-residual-pilot-2026-05-28` — the era hypothesis is falsified: Phi-4 does not flip to +1; it stays sign=-1.

## BENCH (CC extension, 2026-07-22)
Registered strict Phase-4 HaluEval-QA transfer test — [[results/bench-a2-signflip-2026-07-22]] (byte-comparable MLX cells).
- **A1 — deployable.** Geometric winner `attention[last_minus_1_bos_mass] @ step 0`, stem-cluster geometric OOB CI-lo **0.8449**. Part of A1 10/10.
- **A2 polarity — own sign `−1`** ⇒ high fused score = faithful. Blind LOMO transfer under the pooled `−1` sign: AUROC **0.724** (clears; orientation agrees with the pool).
- Generation-split polarity: Phi-4 holds (`−1`) while Phi-3.5 flips (`+1`) — descriptive, **not** a Phi-family law.
- Framing: A2 rejects "fixed cell + fixed sign," not the cell (`fusion_rank_mean_geom` clears 0.55 on all ten with per-model signs).
- **Label cost (descriptive sweep, 2026-07-26).** HaluEval-QA subsample deployability: 1.0 at every budget incl. 50. Cohort-wide: 10/10 at 1.0 by 150 labels, flat through 500 (a measured knee). Post-hoc, not a registered endpoint — [[results/e3-halueval-descriptive-2026-07-26]].

## Model-specific quirks
- Layer stability is weaker than the Phi-3.5 mini model, even though both are useful.
- The model is a clean example of why family name is not enough to predict sign at t=0.

## Caveats and provenance
- This page is about the model-level story. The numerical tables still live in the result pages.
- The t=0 belief-readout re-grounds the premise, but does not validate the older `gen_step=1` attention exposure directly.

## Canonical backlinks
- **KV-tension pilot (2026-06-08, scored 2026-07-25) — NO-PROMOTE.** Largest routing-relative gain in the panel: `final_js_within_kv_groups` 0.7374, **+0.0614 vs routing** (+0.0219 vs all-ACE). But the weakest clean OOB CI-lo (0.5806) and `winner_unstable` (stability 0.63) — the biggest win sits on the shakiest selection.

- [results/v4-sealed-2026-05-26](../results/v4-sealed-2026-05-26.md)
- [results/v4-prep-coverage-matrix-2026-05-16](../results/v4-prep-coverage-matrix-2026-05-16.md)
- [results/step0-belief-readout-2026-05-17](../results/step0-belief-readout-2026-05-17.md)
- [results/inter-head-disagreement-2026-05-15](../results/inter-head-disagreement-2026-05-15.md)
- [results/t0-residual-pilot-2026-05-28](../results/t0-residual-pilot-2026-05-28.md)
- [results/bench-a2-signflip-2026-07-22](../results/bench-a2-signflip-2026-07-22.md)
- [results/kv-tension-pilot-2026-06-09](../results/kv-tension-pilot-2026-06-09.md)
- [results/e3-halueval-descriptive-2026-07-26](../results/e3-halueval-descriptive-2026-07-26.md)
- [results/depth-marginals-2026-08-16](../results/depth-marginals-2026-08-16.md)
