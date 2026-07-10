# Qwen 2.5 32B Instruct (nf4 / 4-bit)

Modal / torch handle: `Qwen/Qwen2.5-32B-Instruct`

## Specs
- Size: 32B parameters
- Quantization: nf4 in the current torch panel; the earlier "32B nf4" baseline was later proven to be bf16 and is corrected in the provenance trail
- Backend: Modal torch
- Output projection: Qwen 2.5 decoder, untied `lm_head`

## Role in the research line
- Scale anchor for the Qwen family.
- Precision-ladder confirm model.
- Current local Furnace guard model.
- The Qwen side of the Qwen-vs-Llama locus dissociation.

## Main verdicts
- `llama-70b-scale-2026-06-22` — 2/2 deployable at matched nf4; ACE attention wins both ANLI and TriviaQA.
- `precision-ladder-results-2026-06-22` — fixed-cell signals are precision-invariant; the original 32B baseline needed a provenance correction from bf16 to true nf4.
- `commit-equivalence-2026-06-23` — within-model commit agreement is high enough that answer-flips are a small, quantifiable contamination, not a showstopper.
- `qwen32b-stress-2026-06-25` — 8/8 deployable across ANLI R1/R2/R3, TriviaQA, TruthfulQA, and HaluEval; attention holds on ANLI/TruthfulQA, HaluEval broadens toward Fusion/readout.
- `commitment-convergence-2026-06-23` — Qwen-32B contributes to the behavioral disagreement ceiling and to the scale-eliminated format leakage result.

## Model-specific quirks
- The original 32B "nf4" baseline was actually bf16; that bug was caught and fixed before the precision story was finalized.
- By 32B, selection instability and int8 degradation largely wash out.
- The shipped local `furnace` guard now uses this model's nf4 ANLI profile and returns `ALLOW` / `BLOCK` / `ABSTAIN` / `DEFER` with a frozen policy.

## Caveats and provenance
- This page mixes a torch panel, a precision-ladder confirm, and the operator guard because they are all the same deployed artifact family.
- The numbers themselves live in the result pages; the guard is a runtime consumer, not a separate claim.

## Canonical backlinks
- [results/llama-70b-scale-2026-06-22](../results/llama-70b-scale-2026-06-22.md)
- [results/precision-ladder-results-2026-06-22](../results/precision-ladder-results-2026-06-22.md)
- [results/commit-equivalence-2026-06-23](../results/commit-equivalence-2026-06-23.md)
- [results/commitment-convergence-2026-06-23](../results/commitment-convergence-2026-06-23.md)
- [results/qwen32b-stress-2026-06-25](../results/qwen32b-stress-2026-06-25.md)
