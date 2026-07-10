# Qwen 2.5 7B Instruct (4-bit)

MLX handle: `mlx-community/Qwen2.5-7B-Instruct-4bit`

## Specs
- Size: 7B parameters
- Quantization: 4-bit (MLX)
- Backend: MLX
- Output projection: untied `lm_head`

## Role in the research line
- Sealed E17b authority for the original PRI line.
- Precision-ladder anchor for the 7B rung.
- Ancestor of the 32B runtime guard and the later Qwen-family stress panel.

## Main verdicts
- `v3-main-run` and `v3.1-replicate` - sealed E18 passes and sealed E17b passes at the same model.
- `step0-belief-readout-2026-05-17` - strongest Recoverable-for-M t=0 model in the panel.
- `commit-equivalence-2026-06-23` - 80% all-rung intersection on ANLI; answer-flips are real but bounded.
- `precision-ladder-results-2026-06-22` - fixed cells are precision-invariant; the ladder is about selection noise, not signal collapse.
- `llama-70b-scale-2026-06-22` - the Qwen family stays on ACE attention while Llama moves to RPV readout.
- `qwen32b-stress-2026-06-25` - the 32B sibling keeps ANLI/TruthfulQA on attention and only broadens on harder HaluEval prompts.
- `commitment-convergence-2026-06-23` - part of the ~18.5% behavioral disagreement ceiling story.

## Model-specific quirks
- Low-rank SVD beat top-k in the original v2 work.
- The 7B model is now the ancestor, not the runtime guard: the local Furnace guard uses the 32B sibling.

## Caveats and provenance
- This page summarizes the model-level story; the numbers stay in `wiki/results`.
- The precision story needs the commit-equivalence control because 7B answer flips are not zero.

## Canonical backlinks
- [results/v3-main-run](../results/v3-main-run.md)
- [results/v3.1-replicate](../results/v3.1-replicate.md)
- [results/step0-belief-readout-2026-05-17](../results/step0-belief-readout-2026-05-17.md)
- [results/commit-equivalence-2026-06-23](../results/commit-equivalence-2026-06-23.md)
- [results/precision-ladder-results-2026-06-22](../results/precision-ladder-results-2026-06-22.md)
- [results/llama-70b-scale-2026-06-22](../results/llama-70b-scale-2026-06-22.md)
- [results/qwen32b-stress-2026-06-25](../results/qwen32b-stress-2026-06-25.md)
- [results/commitment-convergence-2026-06-23](../results/commitment-convergence-2026-06-23.md)
