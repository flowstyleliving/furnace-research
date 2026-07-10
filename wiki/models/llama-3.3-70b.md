# Llama 3.3 70B Instruct (nf4)

Modal / torch handle: `Llama-3.3-70B-Instruct`

## Specs
- Size: 70B parameters
- Quantization: nf4
- Backend: Modal torch
- Output projection: untied `lm_head`

## Role in the research line
- The first scale cell where ACE does not win.
- The Llama-family scale rescue for the sealed `Llama-3.1-8B/anli` orphan.
- The signal-locus side of the Qwen-vs-Llama family dissociation.

## Main verdicts
- `llama-70b-scale-2026-06-22` — both tasks deploy, but the winning locus is RPV readout-volume at gen_step=1, not ACE attention at t=0.
- `llama-70b-scale-2026-06-22` — closes the Llama-3.1-8B ANLI orphan as a scale artifact.
- `commitment-convergence-2026-06-23` — the cross-model behavioral disagreement ceiling stays in the same range as the within-family scale comparison.

## Model-specific quirks
- The model is commit-state readout-heavy rather than attention-heavy.
- It reinforces the interpretation that the universal thing is the fitting procedure, not one universal cell.

## Caveats and provenance
- This is non-byte-comparable torch work.
- The page is about locus and scale, not just raw AUROC.

## Canonical backlinks
- [results/llama-70b-scale-2026-06-22](../results/llama-70b-scale-2026-06-22.md)
- [results/commitment-convergence-2026-06-23](../results/commitment-convergence-2026-06-23.md)
- [results/summary](../results/summary.md)
