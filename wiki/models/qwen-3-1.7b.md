# Qwen 3 1.7B Instruct (4-bit)

MLX handle: `mlx-community/Qwen3-1.7B-4bit`

## Specs
- Size: 1.7B parameters
- Quantization: 4-bit (MLX)
- Backend: MLX
- Output projection: untied `lm_head`

## Role in the research line
- Small reasoning-tuned Qwen control.
- Borderline v4/ACE cell that is still above chance but less stable than the larger Qwen siblings.
- The extra reasoning-tuned model that helped triangulate the Qwen-family branch in the later sweeps.

## Main verdicts
- `v3.2-results` — reasoning-branch anchor; the model was added to resolve the "one reasoning-tuned model is not enough" problem in the meta-classifier branch.
- `v4-prep-coverage-matrix-2026-05-16` — `last_minus_1_js @ step 1`, AUROC 0.6390, sign +1, OOB 0.5872 [0.4436, 0.6808], winner instability flagged.
- `step0-belief-readout-2026-05-17` — Recoverable-for-M at t=0, coverage 1.000, AUROC_B 0.727 [0.655, 0.791], the weakest recoverable model in the panel.
- `triviaqa-pilot-2026-05-25` — exact ANLI→TriviaQA transfer fails; the winning cell shifts and the profile stays unstable.
- `residual-friction-pilot-2026-06-06` — corrected same-`Δh` read lands at +0.011, i.e. the signal touches zero and does not promote.

## BENCH (CC extension, 2026-07-22)
Registered strict Phase-4 HaluEval-QA transfer test — [[results/bench-a2-signflip-2026-07-22]] (byte-comparable MLX cells).
- **A1 — deployable (cohort-weakest).** Geometric winner `Readout null_ratio_post_rank1 @ step 0`, stem-cluster geometric OOB CI-lo **0.6705** — the weakest A1 lower bound in the ten-model cohort, still above chance. Part of A1 10/10.
- **A2 polarity — own sign `−1`** ⇒ high fused score = faithful. Blind LOMO transfer under the pooled `−1` sign: AUROC **0.577** (clears, just above the 0.55 bar).
- B1 gate note: contributed one rare `triviaqa_paired_rep` commitment trigger (1/1000) to the §8.1 cascade — gate accounting, **not** geometry.
- Generation-split polarity: Qwen3 holds (`−1`) while Qwen2.5 flips (`+1`) — descriptive, **not** a Qwen-family law.
- Framing: A2 rejects "fixed cell + fixed sign," not the cell.

## Model-specific quirks
- Reasoning-tuned does not mean scale-transferable: the 8B Qwen3 and the 1.7B Qwen3 do not behave identically.
- In the Qwen family, this is the smallest model and the most fragile one in the v4 panels.

## Caveats and provenance
- Use the later, corrected panels as the working record; the early v3.2 reasoning notes were the setup, not the final verdict.
- The model is useful as a control, not as a strong positive.

## Canonical backlinks
- [results/v3.2-results](../results/v3.2-results.md)
- [results/v4-prep-coverage-matrix-2026-05-16](../results/v4-prep-coverage-matrix-2026-05-16.md)
- [results/step0-belief-readout-2026-05-17](../results/step0-belief-readout-2026-05-17.md)
- [results/triviaqa-pilot-2026-05-25](../results/triviaqa-pilot-2026-05-25.md)
- [results/residual-friction-pilot-2026-06-06](../results/residual-friction-pilot-2026-06-06.md)
- [results/bench-a2-signflip-2026-07-22](../results/bench-a2-signflip-2026-07-22.md)
