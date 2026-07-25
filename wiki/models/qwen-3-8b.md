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

## BENCH (CC extension, 2026-07-22)
Registered strict Phase-4 HaluEval-QA transfer test — [[results/bench-a2-signflip-2026-07-22]] (byte-comparable MLX cells).
- **A1 — deployable.** Geometric winner `attention[last_minus_1_js_kv_groups] @ step 0`, stem-cluster geometric OOB CI-lo **0.8853**. Part of A1 10/10.
- **A2 polarity — own sign `−1`** ⇒ high fused score = faithful. Blind LOMO transfer under the pooled `−1` sign: AUROC **0.583** (clears; orientation agrees with the pool).
- Generation-split polarity: Qwen3 holds (`−1`) while Qwen2.5 flips (`+1`) — descriptive, **not** a Qwen-family law.
- Framing: A2 rejects "fixed cell + fixed sign," not the cell (`fusion_rank_mean_geom` clears 0.55 on all ten with per-model signs).

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
- [results/bench-a2-signflip-2026-07-22](../results/bench-a2-signflip-2026-07-22.md)
