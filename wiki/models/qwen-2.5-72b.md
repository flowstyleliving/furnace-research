# Qwen 2.5 72B Instruct (nf4)

Modal / torch handle: `Qwen/Qwen2.5-72B-Instruct`

## Specs
- Size: 72B parameters
- Quantization: inferred nf4; bf16 is blocked by an OOM guard on the current hardware
- Backend: Modal torch
- Output projection: Qwen 2.5 decoder, untied `lm_head`

## Role in the research line
- Upper-scale anchor for the Qwen family.
- Confirms the 32B-scale attention story does not break at 72B.

## Main verdicts
- `llama-70b-scale-2026-06-22` — 2/2 deployable; Qwen stays on ACE attention while Llama moves to RPV readout.
- `summary` / `torch-panel-snapshot-2026-06-23` — the nf4 run is confirmed by the bf16 OOM guard; the 72B scale tier is healthy but hardware-limited.
- `commitment-convergence-2026-06-23` — part of the larger scale/family disagreement ceiling story, even though the detailed dump is still the tighter source for the 32B and 70B comparisons.
- `depth-marginals-2026-08-16` — separation forms late: ≈chance at mid-stack, peak at N−2 (js_no_bos 0.792 anli / js 0.973 trivia), one-block drop at the final block — the deployed `last_minus_1_*` winners sit exactly on that peak.
- `depth-curve-2026-08-16` — registered per-layer run refines that: the true peaks sit deeper (anli block 66/80 = 0.838; halueval 63/80 = 0.896), the rise is a one-block CLIFF (+0.233 at block 61→62 on anli), and the terminal block always dips — N−2 was the best of three rungs, not the actual maximum.
- `depth-rescore-2026-08-17` — cross-fitted debiasing holds: dip Δ_cf 0.212 (anli) / 0.264 (halueval), cliff both PASS.
- `instrument-colocation-2026-08-29` — **this model's halueval cell is the vault's sharpest instrument dissociation.** `js_no_bos` peaks 0.896 at block 63 with a pinned bootstrap CI [63, 63] and falls to **0.536** at block 70; `bos_mass` peaks 0.853 at block 70 and reads **0.524** at block 63; curve correlation **0.116**. Each attention instrument is at chance where the other is strongest — so the ACE attention cells are not two readings of one quantity here. On anli the pattern is milder (r 0.604) and `bos_mass` peaks higher (0.904 @ 77 vs js 0.838 @ 66). Descriptive, in-sample, not a registered endpoint.
- `depth-coverage-2026-08-31` — **both tasks favour depth-targeting decisively.** anli **+0.0965** [0.054, 0.146] and halueval **+0.1820** [0.115, 0.252] over the best single fixed rung; both intervals exclude zero. The targeted arm hits 0.892 / 0.891 against fixed-rung 0.795 / 0.709. This is the model whose halueval cell carried the sharpest co-location result (js 0.896 @ 63 reading 0.536 at the bos peak), and the depth-coverage numbers are consistent with that: the panel rungs are not where this model commits.
- `instrument-redundancy-2026-08-30` — PC1 median 0.711 (`mid`), 0.727 (`N−2`), 0.519 (`final`); no cell reaches the 0.90 near-collapse threshold. Same terminal-separation direction as Qwen2.5-32B but on six cells rather than 24.

## Model-specific quirks
- This model is a hardware ceiling as much as a model result.
- The important point is that 72B still behaves like the Qwen attention family, not like the Llama readout family.

## Caveats and provenance
- The result is inferred nf4, not byte-verified against bf16, because bf16 is not runnable on the current single-card path.
- Use the summary and torch snapshot as the provenance trail for the hardware caveat.

## Canonical backlinks
- [results/llama-70b-scale-2026-06-22](../results/llama-70b-scale-2026-06-22.md)
- [results/commitment-convergence-2026-06-23](../results/commitment-convergence-2026-06-23.md)
- [results/depth-marginals-2026-08-16](../results/depth-marginals-2026-08-16.md)
- [results/depth-curve-2026-08-16](../results/depth-curve-2026-08-16.md)
- [results/depth-rescore-2026-08-17](../results/depth-rescore-2026-08-17.md)
- [results/summary](../results/summary.md)
- [results/instrument-colocation-2026-08-29](../results/instrument-colocation-2026-08-29.md)
- [results/depth-coverage-2026-08-31](../results/depth-coverage-2026-08-31.md)
- [results/instrument-redundancy-2026-08-30](../results/instrument-redundancy-2026-08-30.md)
