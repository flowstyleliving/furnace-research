# Llama 3.1 8B Instruct (4-bit)

MLX handle: `mlx-community/Llama-3.1-8B-Instruct-4bit`

## Specs
- Size: 8B parameters
- Quantization: 4-bit (MLX)
- Backend: MLX
- Output projection: untied `lm_head`

## Role in the research line
- The sealed ANLI orphan on the Llama side of commit-confluence.
- Smaller sibling to the later Llama-3.3-70B scale rescue.
- Useful t=0 residual-stream anchor because its sign stays inverted.

## Main verdicts
- `v3.2-results` — within-family scale expansion surfaced a stable Llama anchor (`Raw r=2 @ step 4`) that does not depend on the smaller model's sealed-best cell.
- `step0-belief-readout-2026-05-17` — Recoverable-for-M at t=0, coverage 0.995, AUROC_B 0.868 [0.815, 0.912].
- `t0-residual-pilot-2026-05-28` — sign=-1, OOB 0.778, stability 1.00; commitment still lives at gen_step=1 for the residual stream.
- `confluence-seal-2026-06-11` — the new ANLI orphan with CI_lo 0.468.
- `residual-friction-pilot-2026-06-06` — the late-layer friction story looks strong until the same-`Δh` benign floor is applied; then it deflates.
- `llama-70b-scale-2026-06-22` — the 70B family member closes the orphan at scale and shifts the locus to RPV readout at gen_step=1.

## BENCH (CC extension, 2026-07-22)
Registered strict Phase-4 HaluEval-QA transfer test — [[results/bench-a2-signflip-2026-07-22]] (byte-comparable MLX cells).
- **A1 — deployable.** Geometric winner `attention[final_js_no_bos] @ step 0`, stem-cluster geometric OOB CI-lo **0.855**. Part of A1 10/10.
- **A2 polarity — own sign `−1`** ⇒ high fused score = faithful. Blind LOMO transfer under the pooled `−1` sign: AUROC **0.825** (clears; orientation agrees with the pool).
- B1 gate note: this model contributed one of the rare `triviaqa_paired_rep` commitment triggers (1/1000) that fed the pre-registered §8.1 cascade — gate accounting, **not** a geometry failure (raw Family-B geometry 18/18 deployable).
- Framing: A2 rejects "fixed cell + fixed sign," not the cell (`fusion_rank_mean_geom` clears 0.55 on all ten with per-model signs).
- **Label cost (descriptive sweep, 2026-07-26).** HaluEval-QA subsample deployability: 0.9 at 50, 1.0 from 100 up. Cohort-wide: 10/10 at 1.0 by 150 labels, flat through 500 (a measured knee). Post-hoc, not a registered endpoint — [[results/e3-halueval-descriptive-2026-07-26]].

## Model-specific quirks
- The model is stable but inverted at t=0 in the residual stream.
- It is the cleanest example of a Llama model whose smaller-scale orphan is real but not permanent.

## Caveats and provenance
- The 8B and 70B Llama pages should be read together: the family rescues the orphan at scale, but not at the same locus.
- The result is exploratory on the 70B side and sealed on the 8B side; do not pool them mechanically.

## Canonical backlinks
- [results/v3.2-results](../results/v3.2-results.md)
- [results/step0-belief-readout-2026-05-17](../results/step0-belief-readout-2026-05-17.md)
- [results/confluence-seal-2026-06-11](../results/confluence-seal-2026-06-11.md)
- [results/residual-friction-pilot-2026-06-06](../results/residual-friction-pilot-2026-06-06.md)
- [results/llama-70b-scale-2026-06-22](../results/llama-70b-scale-2026-06-22.md)
- [results/bench-a2-signflip-2026-07-22](../results/bench-a2-signflip-2026-07-22.md)
- [results/e3-halueval-descriptive-2026-07-26](../results/e3-halueval-descriptive-2026-07-26.md)
