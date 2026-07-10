# Phi-4-mini Instruct (4-bit)

MLX handle: `mlx-community/Phi-4-mini-instruct-4bit`

## Specs
- Size: 3.8B parameters
- Quantization: 4-bit (MLX)
- Backend: MLX
- Output projection: untied `lm_head`

## Role in the research line
- Phi-family era comparator against Phi-3.5-mini.
- Attention-side v4 expansion model.
- t=0 residual-stream counterexample to any simple "newer Phi flips positive" story.

## Main verdicts
- `v4-sealed-2026-05-26` — ANLI passes with `mid_v_norm_lastq_weighted @ step 0`; TriviaQA transfers only partially and the winner changes.
- `v4-prep-coverage-matrix-2026-05-16` — `final_js_kv_groups @ step 1`, OOB 0.7202, sign +1; borderline but deployable.
- `step0-belief-readout-2026-05-17` — Recoverable-for-M at t=0, coverage 1.000, AUROC_B 0.840 [0.784, 0.894].
- `inter-head-disagreement-2026-05-15` — clean `hi`-orientation signal at final layer under the sink-controlled lens.
- `delta-sigma-onaxis-2026-05-15` — `Δσ_onaxis` alone beats the best null at rank 4 with the opposite sign from Phi-3.5.
- `t0-residual-pilot-2026-05-28` — the era hypothesis is falsified: Phi-4 does not flip to +1; it stays sign=-1.

## Model-specific quirks
- Layer stability is weaker than the Phi-3.5 mini model, even though both are useful.
- The model is a clean example of why family name is not enough to predict sign at t=0.

## Caveats and provenance
- This page is about the model-level story. The numerical tables still live in the result pages.
- The t=0 belief-readout re-grounds the premise, but does not validate the older `gen_step=1` attention exposure directly.

## Canonical backlinks
- [results/v4-sealed-2026-05-26](../results/v4-sealed-2026-05-26.md)
- [results/v4-prep-coverage-matrix-2026-05-16](../results/v4-prep-coverage-matrix-2026-05-16.md)
- [results/step0-belief-readout-2026-05-17](../results/step0-belief-readout-2026-05-17.md)
- [results/inter-head-disagreement-2026-05-15](../results/inter-head-disagreement-2026-05-15.md)
- [results/t0-residual-pilot-2026-05-28](../results/t0-residual-pilot-2026-05-28.md)
