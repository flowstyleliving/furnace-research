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

## Model-specific quirks
- This model is a hardware ceiling as much as a model result.
- The important point is that 72B still behaves like the Qwen attention family, not like the Llama readout family.

## Caveats and provenance
- The result is inferred nf4, not byte-verified against bf16, because bf16 is not runnable on the current single-card path.
- Use the summary and torch snapshot as the provenance trail for the hardware caveat.

## Canonical backlinks
- [results/llama-70b-scale-2026-06-22](../results/llama-70b-scale-2026-06-22.md)
- [results/commitment-convergence-2026-06-23](../results/commitment-convergence-2026-06-23.md)
- [results/summary](../results/summary.md)
