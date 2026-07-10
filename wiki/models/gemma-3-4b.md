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
