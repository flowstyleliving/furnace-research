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
- `depth-marginals-2026-08-16` — three-point depth read: attention morphology is only mild at mid-stack (js 0.66/0.71) and fades by the final block (6/6 fixed cells); the strong separation is post-stack in readout (0.816/0.862) — the readout-locus story now has a depth profile. *(Superseded-in-part same day — see next bullet.)*
- `depth-curve-2026-08-16` — **registered per-layer run overturns the "attention-weak" reading: a broad mid-stack attention band exists** (anli ≈0.5 through block 43, then 0.63–0.90 through the 60s; peak 0.897 @ block 48/80 > the panel readout winner 0.816; 44/80 blocks clear the shuffled envelope). The three-rung panel sampled blocks 40/78/79 — all outside the band. "Llama → readout locus" is **panel-relative**, not model-truth; in-sample sign-free caveats apply.
- `depth-rescore-2026-08-17` — cross-fitted debiasing: **largest dip in the grid on anli (Δ_cf 0.416)**, cliff PASS with the jump explaining 100% of the rise (J_cf = R_cf = 0.206); on halueval the dip holds (0.111) but the cliff statistic is **structurally UNDEF** — the early peak (block 26 < 0.5·N) leaves the cliff window empty, the grid's only E6 failure.
- `depth-grid-2026-08-17` — **the mid-stack band is not a 3.3 quirk**: as grid-A context beside the registered 3.1-70B cells, this model shows 25–31 qualifying mid-blocks per fold vs 3.1-70B's 16–25 — the band survives the version change (P8 hit) and is absent at 8B (P9 hit).

## Model-specific quirks
- The model is commit-state readout-heavy rather than attention-heavy.
- It reinforces the interpretation that the universal thing is the fitting procedure, not one universal cell.

## Caveats and provenance
- This is non-byte-comparable torch work.
- The page is about locus and scale, not just raw AUROC.

## Canonical backlinks
- [results/llama-70b-scale-2026-06-22](../results/llama-70b-scale-2026-06-22.md)
- [results/commitment-convergence-2026-06-23](../results/commitment-convergence-2026-06-23.md)
- [results/depth-marginals-2026-08-16](../results/depth-marginals-2026-08-16.md)
- [results/depth-curve-2026-08-16](../results/depth-curve-2026-08-16.md)
- [results/depth-rescore-2026-08-17](../results/depth-rescore-2026-08-17.md)
- [results/summary](../results/summary.md)
- [results/depth-grid-2026-08-17](../results/depth-grid-2026-08-17.md)
