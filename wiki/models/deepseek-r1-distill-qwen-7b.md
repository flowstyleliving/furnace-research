# DeepSeek-R1-Distill-Qwen-7B (4-bit)

MLX handle: `DeepSeek-R1-Distill-Qwen-7B-4bit`

## Specs
- Size: 7B parameters
- Quantization: 4-bit (MLX)
- Backend: MLX
- Output projection: untied `lm_head`

## Role in the research line
- Cautionary reasoning-distill control.
- Smoke-tested as the extra reasoning-tuned comparator, but never became a conclusion-bearing model.

## Main verdicts
- `v3.2-results` — launched as the additional reasoning-tuned model needed to settle the reasoning-branch ambiguity.
- `residual-friction-pilot-2026-06-06` — the repeated-CV screen is badly anti-conservative on this model; shuffled-label control leaks +0.166, so the numbers are untrustworthy.

## Model-specific quirks
- This is the one model in the friction pilot where the shuffle control is the red flag, not a harmless small deviation.
- Treat it as a warning sign about the screening method, not as support for the candidate statistic.

## Caveats and provenance
- Because the control leaks, the page should not be used as evidence for a positive claim.
- The model is still useful as a negative control for template and CV fragility.

## Canonical backlinks
- [results/v3.2-results](../results/v3.2-results.md)
- [results/residual-friction-pilot-2026-06-06](../results/residual-friction-pilot-2026-06-06.md)
