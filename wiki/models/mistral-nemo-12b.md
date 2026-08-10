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

## BENCH (CC extension, 2026-07-22)
Registered strict Phase-4 HaluEval-QA transfer test — [[results/bench-a2-signflip-2026-07-22]] (byte-comparable MLX cells).
- **A1 — deployable.** Geometric winner `attention[last_minus_1_bos_mass] @ step 0`, stem-cluster geometric OOB CI-lo **0.8446**. Part of A1 10/10.
- **A2 polarity — own sign `+1` on `fusion_rank_mean_geom`** ⇒ high fused score = **hallucinated**. Blind LOMO transfer under the pooled `−1` sign: AUROC **0.206** — an **intrinsic sign-flip: signal present, orientation opposite**, not signal absence. Reversing recovers 0.794, but **reversal is not an A2 rescue** (it needs this model's own labels, which blind transfer forbids).
- **[OPEN — observation, not a finding]** Mistral-Nemo is one of the three flippers (with Mistral-7B and Qwen2.5-7B) that coincide with the v4 sealed E_A2 partial-transfer trio ([[results/v4-sealed-2026-05-26]]). Untested overlap; do **not** state it as a finding.
- Both Mistral members flip (`+1`), but descriptive only; cohort-wide polarity is **generation-structured, not a family law**. Framing: A2 rejects "fixed cell + fixed sign," not the cell.
- **Label cost (descriptive sweep, 2026-07-26).** HaluEval-QA subsample deployability: 1.0 at every budget incl. 50. Cohort-wide: 10/10 at 1.0 by 150 labels, flat through 500 (a measured knee). Post-hoc, not a registered endpoint — [[results/e3-halueval-descriptive-2026-07-26]].

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
- [results/bench-a2-signflip-2026-07-22](../results/bench-a2-signflip-2026-07-22.md)
- [results/e3-halueval-descriptive-2026-07-26](../results/e3-halueval-descriptive-2026-07-26.md)
