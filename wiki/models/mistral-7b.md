# Mistral 7B Instruct v0.3 (4-bit)

MLX handle: `mlx-community/Mistral-7B-Instruct-v0.3-4bit`

## Specs
- Size: 7B parameters
- Quantization: 4-bit (MLX)
- Backend: MLX
- Output projection: untied `lm_head`

## Role in the research line
- v3 primary.
- Chain-length Simpson's paradox model.
- Older sibling to the Mistral-Nemo terminal-commit anchor.

## Main verdicts
- `v3-main-run` - sealed E18 passes at rank 1; Raw is decisive in the pooled view.
- `v4-sealed-2026-05-26` - exact ANLI and TriviaQA transfer at t=0.
- `inter-head-disagreement-2026-05-15` - clean head-disagreement case once BOS sinks are controlled.
- `step0-belief-readout-2026-05-17` - Mistral-Nemo is the immediate-commit anchor for the family.
- `t0-residual-pilot-2026-05-28` - residual sign=-1 with moderate OOB support.
- `residual-friction-pilot-2026-06-06` - the apparent friction story does not survive the same-`Δh` floor.

## Model-specific quirks
- The newline-commit pattern makes the chain-length axis matter.
- The pool-level Raw story is a Simpson's-paradox artifact; the strata tell the cleaner story.

## Canonical backlinks
- [results/v3-main-run](../results/v3-main-run.md)
- [results/v4-sealed-2026-05-26](../results/v4-sealed-2026-05-26.md)
- [results/inter-head-disagreement-2026-05-15](../results/inter-head-disagreement-2026-05-15.md)
- [results/step0-belief-readout-2026-05-17](../results/step0-belief-readout-2026-05-17.md)
- [results/t0-residual-pilot-2026-05-28](../results/t0-residual-pilot-2026-05-28.md)
- [results/residual-friction-pilot-2026-06-06](../results/residual-friction-pilot-2026-06-06.md)
