# Llama 3.2 3B Instruct (4-bit)

MLX handle: `mlx-community/Llama-3.2-3B-Instruct-4bit`

## Specs
- Size: 3B parameters
- Quantization: 4-bit (MLX)
- Backend: MLX
- Output projection: tied embeddings

## Role in the research line
- v3 primary and the small-model antecedent to the later Llama family orphan/rescue split.
- Later t=0 residual anchor.

## Main verdicts
- `v3-main-run` - sealed E18 passes at rank 1; Fisher is decisive at the seal.
- `v4-sealed-2026-05-26` - ANLI fails at t=0, while TriviaQA remains deployable.
- `step0-belief-readout-2026-05-17` - Recoverable-for-M at t=0, coverage 1.000, AUROC_B 0.780 [0.713, 0.839].
- `t0-residual-pilot-2026-05-28` - sign=-1, OOB 0.660, stability 0.44; the prefix carries the inverted residual signal.
- `confluence-seal-2026-06-11` - sealed ANLI orphan on the primary dispatcher.
- `residual-friction-pilot-2026-06-06` - the old late-layer friction story deflates once the same-`Δh` floor is applied.
- `llama-70b-scale-2026-06-22` - the family rescue arrives only at 70B and does so through RPV readout, not ACE attention.

## BENCH (CC extension, 2026-07-22)
Registered strict Phase-4 HaluEval-QA transfer test — [[results/bench-a2-signflip-2026-07-22]] (byte-comparable MLX cells).
- **A1 (per-model calibration) — deployable.** Geometric winner `Fusion fusion_rank_mean_geom @ step 0`, stem-cluster geometric OOB CI-lo **0.8505**. Part of the A1 10/10 pass (bar ≥8; cohort-weakest CI-lo 0.6705 at Qwen3-1.7B).
- **A2 polarity — own sign `−1` on `fusion_rank_mean_geom`** ⇒ high fused score = faithful. Blind leave-one-model-out transfer under the pooled `−1` sign: AUROC **0.873** — the cohort's strongest holdout; orientation agrees with the pool, so it clears cleanly.
- Framing: A2 fails 6/10 by rejecting the compound "fixed cell + fixed sign," **not** the cell — `fusion_rank_mean_geom` clears 0.55 on all ten once each model's sign is calibrated.
- **Label cost (descriptive sweep, 2026-07-26).** HaluEval-QA subsample deployability: 0.9/0.8 (full/geom) at 50, 1.0 from 100 up. Cohort-wide: 10/10 at 1.0 by 150 labels, flat through 500 (a measured knee). Post-hoc, not a registered endpoint — [[results/e3-halueval-descriptive-2026-07-26]].

## Model-specific quirks
- This is the small-model antecedent to the Llama family dissociation.
- It is useful as a negative or weak-positive control, not as the family rescue point.

## Canonical backlinks
- [results/v3-main-run](../results/v3-main-run.md)
- [results/v4-sealed-2026-05-26](../results/v4-sealed-2026-05-26.md)
- [results/step0-belief-readout-2026-05-17](../results/step0-belief-readout-2026-05-17.md)
- [results/t0-residual-pilot-2026-05-28](../results/t0-residual-pilot-2026-05-28.md)
- [results/confluence-seal-2026-06-11](../results/confluence-seal-2026-06-11.md)
- [results/residual-friction-pilot-2026-06-06](../results/residual-friction-pilot-2026-06-06.md)
- [results/llama-70b-scale-2026-06-22](../results/llama-70b-scale-2026-06-22.md)
- [results/bench-a2-signflip-2026-07-22](../results/bench-a2-signflip-2026-07-22.md)
- [results/e3-halueval-descriptive-2026-07-26](../results/e3-halueval-descriptive-2026-07-26.md)
