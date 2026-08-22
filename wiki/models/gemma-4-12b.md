# Gemma 4-12B IT (QAT 4-bit)

MLX-vlm handle: `gemma-4-12B-it-qat-4bit`

## Specs
- Size: 12B parameters
- Quantization: QAT 4-bit
- Backend: mlx-vlm
- Output projection: Gemma 4 decoder, non-byte-comparable to the sealed MLX plane

## Role in the research line
- Generation-axis follow-up to the Gemma 3 orphan.
- Confirms that the Gemma 3 orphan does not come back at gen-4.

## Main verdicts
- `gemma-scale-extension-2026-06-18` — after fixing the prompt path, both ANLI and TriviaQA deploy; winners are Fusion, not ACE solo.
- `gemma-scale-extension-2026-06-18` — gen-4/anli 0.691 sits beside gemma-3-12b/anli 0.709, so the orphan is still a scale / small-model artifact.
- `gemma-scale-extension-2026-06-18` — the initial \~0.37-on-both run was a chat-template bug, not a model verdict.

## Model-specific quirks
- Raw passthrough is wrong for this model; `apply_chat_template` is required.
- It is the first Gemma cell here where both winners are Fusion rather than ACE attention.

## Caveats and provenance
- This cell is non-byte-comparable and should never be pooled with the sealed scale cells.
- The readout half was not parity-validated independently; keep the caveat attached.

## Canonical backlinks
- [results/gemma-scale-extension-2026-06-18](../results/gemma-scale-extension-2026-06-18.md)
- [results/summary](../results/summary.md)
