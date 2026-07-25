# Gemma 3-4B Instruct (4-bit)

MLX handle: `mlx-community/gemma-3-4b-it-4bit`

## Specs
- Size: 4B parameters
- Quantization: 4-bit (MLX)
- Backend: MLX
- Output projection: untied `lm_head`

## Role in the research line
- Gemma 3 Motif 2 model.
- Source of the sealed Gemma orphan that later gets resolved by scale.

## Main verdicts
- `v3.1-replicate` - within-model rank flip: Fisher at r=2, Raw at r=3, robust to chain length.
- `v4-sealed-2026-05-26` - ANLI fails at t=0, while TriviaQA stays strong.
- `step0-belief-readout-2026-05-17` - Recoverable-for-M at t=0, but weaker than the stronger families.
- `confluence-seal-2026-06-11` - one of the two sealed ANLI orphans in the registered dispatcher.
- `gemma-scale-extension-2026-06-18` - scaling to 12B rescues the orphan; the failure is small-model, not family-wide.
- `t0-residual-pilot-2026-05-28` - sign=+1 at t=0, which is the natural-alignment counterexample in the family set.
- `residual-friction-pilot-2026-06-06` - the corrected same-`Δh` floor deflates the late-layer friction story.

## BENCH (CC extension, 2026-07-22)
Registered strict Phase-4 HaluEval-QA transfer test — [[results/bench-a2-signflip-2026-07-22]] (byte-comparable MLX cells).
- **A1 — deployable (cohort-strongest).** Geometric winner `attention[mid_js_kv_groups] @ step 0`, stem-cluster geometric OOB CI-lo **0.9005** — the strongest A1 lower bound in the cohort. Part of A1 10/10.
- **A2 polarity — own sign `−1`** ⇒ high fused score = faithful. Blind LOMO transfer under the pooled `−1` sign: AUROC **0.850** (clears; orientation agrees with the pool).
- B1 gate note: gemma-3-4b hits 12/1000 (~1.2%) `triviaqa_paired_rep` commitment fails — it sometimes answers the trivia question instead of judging faithfulness — which, under the §4 zero-error-budget / §8.1 systematic-abort rule, zeroed its TriviaQA cells in the B1 cascade. This is **pre-registered gate behavior, not geometric failure** (raw Family-B geometry 18/18 deployable).
- Framing: A2 rejects "fixed cell + fixed sign," not the cell (`fusion_rank_mean_geom` clears 0.55 on all ten with per-model signs).

## Model-specific quirks
- Gemma 3 uses the `(1 + gamma)` RMSNorm quirk.
- It is the model that first made the later scale-orphan story visible.

## Canonical backlinks
- [results/v3.1-replicate](../results/v3.1-replicate.md)
- [results/v4-sealed-2026-05-26](../results/v4-sealed-2026-05-26.md)
- [results/step0-belief-readout-2026-05-17](../results/step0-belief-readout-2026-05-17.md)
- [results/confluence-seal-2026-06-11](../results/confluence-seal-2026-06-11.md)
- [results/gemma-scale-extension-2026-06-18](../results/gemma-scale-extension-2026-06-18.md)
- [results/t0-residual-pilot-2026-05-28](../results/t0-residual-pilot-2026-05-28.md)
- [results/residual-friction-pilot-2026-06-06](../results/residual-friction-pilot-2026-06-06.md)
- [results/bench-a2-signflip-2026-07-22](../results/bench-a2-signflip-2026-07-22.md)
