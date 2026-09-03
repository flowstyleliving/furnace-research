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
- `depth-marginals-2026-08-16` — same late-forming depth signature as 72B: mid ≈ chance, N−2 peak (js 0.862 / 0.862 / 0.883 on anli / trivia / halueval-qa), final-block drop on every js-family cell.
- `depth-curve-2026-08-16` — registered per-layer run: true peaks at block 56/64 on both tasks (0.865 anli / 0.911 halueval), CLIFF rise, terminal dip; the halueval bootstrap band is wide ([35, 61]) — peak location is not pinned sharply at this n.
- `depth-rescore-2026-08-17` — cross-fitted debiasing holds: dip Δ_cf 0.146 (anli) / 0.261 (halueval), cliff both PASS.
- `depth-coverage-2026-08-31` — **the grid-A cell where depth-targeting does not pay.** anli returns **−0.0380** [−0.087, 0.009] (interval includes zero) and is the only grid-A cell where the fixed rung wins; its per-fold selection is the least stable in grid A (`bos`@55 in just 2/5 folds). halueval is a small clean win, **+0.0320** [0.008, 0.061], with selection stable at 5/5. The contrast between the two tasks is the sharpest within-model split in the grid.
- `instrument-redundancy-2026-08-30` — **the widest-coverage cell set in the read (24 of 42 cells, 8 tasks), and it shows redundancy is depth-dependent.** PC1 falls from **0.731** at `N−2` to **0.448** at `final`, while cells with two or more instruments clearing the 0.60 residual bar rise from **4/8 to 7/8**. The instruments separate as the stack terminates. No cell on this model reaches the PC1 ≥0.90 near-collapse threshold.

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
- [results/depth-marginals-2026-08-16](../results/depth-marginals-2026-08-16.md)
- [results/depth-curve-2026-08-16](../results/depth-curve-2026-08-16.md)
- [results/depth-rescore-2026-08-17](../results/depth-rescore-2026-08-17.md)
- [results/depth-coverage-2026-08-31](../results/depth-coverage-2026-08-31.md)
- [results/instrument-redundancy-2026-08-30](../results/instrument-redundancy-2026-08-30.md)
