# Gemma 3-1B Instruct (4-bit) - EXCLUDED

MLX handle: `mlx-community/gemma-3-1b-it-4bit`

## Specs
- Size: 1B parameters
- Quantization: 4-bit (MLX)
- Backend: MLX
- Output projection: tied embeddings

## Role in the research line
- Historical excluded sibling to Gemma 3-4B.
- The small-model foil that the later 12B scale rescue and gen-4 follow-up explain.

## Main verdicts
- `v3.1-replicate` - gate failure at 11/20 = 55%; the model defaults to `Answer: NO` on YES controls.
- `v3.2-results` - the later generation work keeps it out of the conclusion-bearing set.
- `gemma-scale-extension-2026-06-18` - scaling to 12B rescues the Gemma orphan, so the 1B exclusion is clearly a small-model artifact.
- `gemma-scale-extension-2026-06-18` - gen-4 does not reintroduce the orphan, which reinforces the scale explanation.

## Model-specific quirks
- The failure here is genuine capability, not a parser artifact.
- The model is useful as a negative control for the Gemma family and prompt-format sensitivity.

## Canonical backlinks
- [results/v3.1-replicate](../results/v3.1-replicate.md)
- [results/v3.2-results](../results/v3.2-results.md)
- [results/gemma-scale-extension-2026-06-18](../results/gemma-scale-extension-2026-06-18.md)
