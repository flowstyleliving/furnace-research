# Gemma 3-12B Instruct (4-bit)

Gemma 3 scale rescue model.

Handle: `gemma-3-12b-it`

## Specs
- Size: 12B parameters
- Quantization: 4-bit (MLX)
- Backend: MLX
- Output projection: Gemma 3 decoder with the standard Gemma 3 RMSNorm quirk

## Role in the research line
- Scale rescue for the Gemma 3 orphan.
- The model that separates "small-model failure" from "Gemma family failure."
- Bridge to the Gemma 4 generation-axis follow-up.

## Main verdicts
- `gemma-scale-extension-2026-06-18` — ANLI 0.709 and TriviaQA 0.929; both deployable, both ACE attention winners.
- `gemma-scale-extension-2026-06-18` — the orphan `gemma-3-4b/anli` is a scale/small-model artifact, not a family dead-end.
- `gemma-scale-extension-2026-06-18` — head-count ablation on 12B weakens the profile only modestly, so the primary mechanism is quality, not count.
- `depth-marginals-2026-08-16` — clean N−2 depth peak at 48 blocks (js-family 4/6, N−2 mean 0.808 vs mid 0.669) — big-model-style depth structure already at 12B.
- `depth-grid-2026-08-17` — registered grid-B cell (torch lane): E5 dip PASSES both tasks with the grid's strongest halueval dip (Δ_cf 0.218 anli / 0.306 halueval); its anli cell is 1 of only 2 grid-B cells satisfying the cross-fitted cliff rule; peak_cf 39/48 anli vs 22/48 halueval (task wobble).

## Model-specific quirks
- The 12B model tolerates the same prompt path that later fails on Gemma 4.
- It is the cleanest Gemma 3 model in the family story because it rescues both the ANLI and TriviaQA cells.

## Caveats and provenance
- This is a byte-comparable extension of the seal; its numbers belong in `wiki/results`, not here.
- The generation-axis result is a separate backend story and should not be pooled with the sealed plane.

## Canonical backlinks
- [results/gemma-scale-extension-2026-06-18](../results/gemma-scale-extension-2026-06-18.md)
- [results/confluence-seal-2026-06-11](../results/confluence-seal-2026-06-11.md)
- [results/depth-marginals-2026-08-16](../results/depth-marginals-2026-08-16.md)
- [results/depth-grid-2026-08-17](../results/depth-grid-2026-08-17.md)
