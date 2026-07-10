# Mistral Nemo 12B Instruct (4-bit)

MLX handle: `mlx-community/Mistral-Nemo-Instruct-2407-4bit`

## Specs
- Size: 12B parameters
- Quantization: 4-bit (MLX)
- Backend: MLX
- Output projection: untied `lm_head`

## Role in the research line
- Terminal-commit anchor for the v3.2 expansion.
- Sink-driven comparator in the v4 attention-side panels.
- Immediate-commit validity anchor for the t=0 belief-readout panel.

## Main verdicts
- `v3.2-results` — Phase B model: `kl_discharged @ step 1` is the surviving universal winner across Mistral-Nemo + Gemma-3-1B, with min AUROC 0.9670.
- `v4-sealed-2026-05-26` — ANLI and TriviaQA both pass at t=0; ANLI winner `last_minus_1_bos_mass @ step 0`, exact transfer to TriviaQA.
- `step0-belief-readout-2026-05-17` — validity anchor: agreement 0.99 (198/200), `passed=True`.
- `inter-head-disagreement-2026-05-15` — sink-driven failure mode; no clean head-disagreement cell.
- `t0-residual-pilot-2026-05-28` — t=0 residual profile remains positive and sign=+1, but the operating point is not family-general.
- `residual-friction-pilot-2026-06-06` — residual-friction does not beat the corrected same-`Δh` floor; do not promote.

## Model-specific quirks
- Raw-prompt vs chat-template handling mattered during the v3.2 expansion.
- At the commit moment the model often emits exactly one YES/NO token and then EOS, which makes the step-1 locus unusually clean.
- In the inter-head panel it behaves like a sink-heavy model rather than a clean RAUQ-style disagreement case.

## Caveats and provenance
- The t=0 anchor validates the measurement premise, not downstream attention numbers taken at reasoning preamble tokens.
- Its residual-friction read is negative under the same-`Δh` control; keep it as a comparator, not a story driver.

## Canonical backlinks
- [results/v3.2-results](../results/v3.2-results.md)
- [results/v4-sealed-2026-05-26](../results/v4-sealed-2026-05-26.md)
- [results/step0-belief-readout-2026-05-17](../results/step0-belief-readout-2026-05-17.md)
- [results/inter-head-disagreement-2026-05-15](../results/inter-head-disagreement-2026-05-15.md)
- [results/t0-residual-pilot-2026-05-28](../results/t0-residual-pilot-2026-05-28.md)
