# Phi-3.5-mini Instruct (4-bit)

MLX handle: `mlx-community/Phi-3.5-mini-instruct-4bit`

## Specs
- Size: 3.8B parameters
- Quantization: 4-bit (MLX)
- Backend: MLX
- Output projection: untied `lm_head`

## Role in the research line
- Stable Raw motif model.
- Tension point for the t=0 decidedness story.
- The Phi-family baseline against Phi-4-mini.

## Main verdicts
- `v4-sealed-2026-05-26` - Raw decisive at the sealed r=1 operating point.
- `step0-belief-readout-2026-05-17` - only 37/200 samples are literally decided at t=0.
- `step0-phi35-locus-offset-audit-2026-05-25` - the low-decidedness is real, not a locus-offset artifact.
- `inter-head-disagreement-2026-05-15` - one of the cleanest models on the head-disagreement side.
- `t0-residual-pilot-2026-05-28` - residual sign=-1 at t=0, even though the attention side is strong.
- `delta-sigma-onaxis-2026-05-15` - the newer Phi flips the sign relative to Phi-3.5 on `Δsigma_onaxis`.

## BENCH (CC extension, 2026-07-22)
Registered strict Phase-4 HaluEval-QA transfer test — [[results/bench-a2-signflip-2026-07-22]] (byte-comparable MLX cells).
- **A1 — deployable.** Geometric winner `attention[mid_js] @ step 0`, stem-cluster geometric OOB CI-lo **0.8839**. Part of A1 10/10.
- **A2 polarity — own sign `+1` on `fusion_rank_mean_geom`** ⇒ high fused score = **hallucinated**. Blind LOMO transfer under the pooled `−1` sign: AUROC **0.394** — an **intrinsic sign-flip: signal present, orientation opposite** (the mildest of the four). Reversing recovers 0.606, but **reversal is not an A2 rescue** (it needs this model's own labels).
- B1 gate note: Phi-3.5 emits a `'\n'` behavioral fail on `anli_r1_rep` — a pre-registered gate behavior Amendment A1 explicitly declined to rescue, **not** a geometric failure (raw geometry deployable).
- Generation-split polarity: Phi-3.5 flips (`+1`) while Phi-4 holds (`−1`) — descriptive, **not** a Phi-family law (independently echoed by `delta-sigma-onaxis-2026-05-15`, Phi-3.5 `−` vs Phi-4 `+`).
- Framing: A2 rejects "fixed cell + fixed sign," not the cell.
- **Label cost (descriptive sweep, 2026-07-26).** HaluEval-QA subsample deployability: 1.0 at every budget incl. 50 — the behavioral outlier is label-cheap: its geometry was never the problem. Cohort-wide: 10/10 at 1.0 by 150 labels, flat through 500 (a measured knee). Post-hoc, not a registered endpoint — [[results/e3-halueval-descriptive-2026-07-26]].

## Model-specific quirks
- This is the model that actually shows the low-decidedness problem at the literal t=0 locus.
- The original "clean trustworthy" Step-1 framing was a different exposure, not the t=0 measurement.

## Canonical backlinks
- [results/v4-sealed-2026-05-26](../results/v4-sealed-2026-05-26.md)
- [results/step0-belief-readout-2026-05-17](../results/step0-belief-readout-2026-05-17.md)
- [results/step0-phi35-locus-offset-audit-2026-05-25](../results/step0-phi35-locus-offset-audit-2026-05-25.md)
- [results/inter-head-disagreement-2026-05-15](../results/inter-head-disagreement-2026-05-15.md)
- [results/t0-residual-pilot-2026-05-28](../results/t0-residual-pilot-2026-05-28.md)
- [results/delta-sigma-onaxis-2026-05-15](../results/delta-sigma-onaxis-2026-05-15.md)
- [results/bench-a2-signflip-2026-07-22](../results/bench-a2-signflip-2026-07-22.md)
- [results/e3-halueval-descriptive-2026-07-26](../results/e3-halueval-descriptive-2026-07-26.md)
