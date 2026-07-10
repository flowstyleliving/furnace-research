# Qwen 3 8B (4-bit)

MLX handle: `mlx-community/Qwen3-8B-4bit`

## Specs
- Size: 8B parameters
- Quantization: 4-bit (MLX)
- Backend: MLX
- Output projection: untied `lm_head`
- Class: `mlx_lm.models.qwen3.Qwen3Model`

## Role in the research line
- Cross-generation companion to Qwen 2.5 7B.
- Later became one of the key Qwen-family controls because it exposes the family split cleanly.

## v3.1 results
- `v3.1-replicate` - sealed E17b at r=1 is Raw decisive: `Δ_oriented = -0.214 [-0.261, -0.175]`.
- Per-rank pattern - Raw at r=1, then Fisher recovers from r >= 13 onward, peaking at +0.447 at r=32.
- The commit token is mostly `Answer`, so the model commits to answer content rather than a pure newline.

## Later conclusions
- `v4-prep-coverage-matrix-2026-05-16` - clean `hi`-orientation attention cell at `final_js_kv_groups` / `last_minus_1_js_kv_groups`.
- `step0-belief-readout-2026-05-17` - Recoverable-for-M at t=0, coverage 0.995, AUROC_B 0.889 [0.835, 0.932].
- `t0-residual-pilot-2026-05-28` - sign=+1, OOB 0.774; the family split against Qwen 2.5 is real.
- `residual-friction-pilot-2026-06-06` - the corrected same-`Δh` read leaves Qwen3 as a weak or null-positive model.
- `qwen32b-stress-2026-06-25` - the larger Qwen family keeps ANLI and TruthfulQA attention-led, with only harder grounded-source prompts broadening the locus.

## Model-specific quirks
- Qwen3 is less stable and more context-sensitive than Qwen2.5.
- It helped expose the family split: Qwen2.5 sits on the attention locus, Qwen3 is the more fragile sibling.

## Canonical backlinks
- [results/v3.1-replicate](../results/v3.1-replicate.md)
- [results/v4-prep-coverage-matrix-2026-05-16](../results/v4-prep-coverage-matrix-2026-05-16.md)
- [results/step0-belief-readout-2026-05-17](../results/step0-belief-readout-2026-05-17.md)
- [results/t0-residual-pilot-2026-05-28](../results/t0-residual-pilot-2026-05-28.md)
- [results/residual-friction-pilot-2026-06-06](../results/residual-friction-pilot-2026-06-06.md)
- [results/qwen32b-stress-2026-06-25](../results/qwen32b-stress-2026-06-25.md)
