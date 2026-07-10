# Qwen 2.5 14B Instruct (4-bit)

Qwen family control for the Gemma scale extension.

Handle: `Qwen2.5-14B-Instruct`

## Specs
- Size: 14B parameters
- Quantization: 4-bit (MLX)
- Backend: MLX
- Output projection: Qwen 2.5 decoder, untied `lm_head`

## Role in the research line
- Family control for the Gemma 3 scale rescue.
- The "generic 12-14B" alternative that rules out a trivial size-floor explanation.

## Main verdicts
- `gemma-scale-extension-2026-06-18` — ANLI 0.766, TriviaQA 0.597; both deployable, both ACE attention winners.
- `gemma-scale-extension-2026-06-18` — confirms the Gemma 4B failure was Gemma-small-specific, not "all 12-14B models fail ANLI."
- `gemma-scale-extension-2026-06-18` — the TriviaQA cell is the weakest of the four extension cells, but still deployable.

## Model-specific quirks
- This model is the clean family control because it passes ANLI while staying in the same rough size band.
- TriviaQA is the marginal cell to watch.

## Caveats and provenance
- It belongs to the out-of-sample extension, not the sealed 18/20.
- Use the result page for the numerical table; this page only preserves the interpretation.

## Canonical backlinks
- [results/gemma-scale-extension-2026-06-18](../results/gemma-scale-extension-2026-06-18.md)
- [results/summary](../results/summary.md)
