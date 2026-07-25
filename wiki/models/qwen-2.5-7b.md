# Qwen 2.5 7B Instruct (4-bit)

MLX handle: `mlx-community/Qwen2.5-7B-Instruct-4bit`

## Specs
- Size: 7B parameters
- Quantization: 4-bit (MLX)
- Backend: MLX
- Output projection: untied `lm_head`

## Role in the research line
- Sealed E17b authority for the original PRI line.
- Precision-ladder anchor for the 7B rung.
- Ancestor of the 32B runtime guard and the later Qwen-family stress panel.

## Main verdicts
- `v3-main-run` and `v3.1-replicate` - sealed E18 passes and sealed E17b passes at the same model.
- `step0-belief-readout-2026-05-17` - strongest Recoverable-for-M t=0 model in the panel.
- `commit-equivalence-2026-06-23` - 80% all-rung intersection on ANLI; answer-flips are real but bounded.
- `precision-ladder-results-2026-06-22` - fixed cells are precision-invariant; the ladder is about selection noise, not signal collapse.
- `llama-70b-scale-2026-06-22` - the Qwen family stays on ACE attention while Llama moves to RPV readout.
- `qwen32b-stress-2026-06-25` - the 32B sibling keeps ANLI/TruthfulQA on attention and only broadens on harder HaluEval prompts.
- `commitment-convergence-2026-06-23` - part of the ~18.5% behavioral disagreement ceiling story.

## BENCH (CC extension, 2026-07-22)
Registered strict Phase-4 HaluEval-QA transfer test — [[results/bench-a2-signflip-2026-07-22]] (byte-comparable MLX cells).
- **A1 — deployable.** Geometric winner `attention[last_minus_1_bos_mass] @ step 0`, stem-cluster geometric OOB CI-lo **0.7492**. Part of A1 10/10.
- **A2 polarity — own sign `+1` on `fusion_rank_mean_geom`** ⇒ high fused score = **hallucinated**. Blind LOMO transfer under the pooled `−1` sign: AUROC **0.276** — an **intrinsic sign-flip: signal present, orientation opposite**, not signal absence. Reversing recovers 0.724, but **reversal is not an A2 rescue** (it needs this model's own labels, which blind transfer forbids).
- B1 gate note: Qwen2.5-7B emits a `' To'` chain-of-thought behavioral fail on `anli_r1_rep` — pre-registered gate behavior (A1 declined to rescue), **not** a geometric failure.
- **[OPEN — observation, not a finding]** Qwen2.5-7B is one of the three flippers (with Mistral-7B and Mistral-Nemo) that coincide with the v4 sealed E_A2 partial-transfer trio ([[results/v4-sealed-2026-05-26]]). Untested overlap; do **not** state it as a finding.
- Generation-split polarity: Qwen2.5 flips (`+1`) while Qwen3 holds (`−1`) — descriptive, **not** a Qwen-family law.
- Framing: A2 rejects "fixed cell + fixed sign," not the cell.

## Model-specific quirks
- Low-rank SVD beat top-k in the original v2 work.
- The 7B model is now the ancestor, not the runtime guard: the local Furnace guard uses the 32B sibling.

## Caveats and provenance
- This page summarizes the model-level story; the numbers stay in `wiki/results`.
- The precision story needs the commit-equivalence control because 7B answer flips are not zero.

## Canonical backlinks
- [results/v3-main-run](../results/v3-main-run.md)
- [results/v3.1-replicate](../results/v3.1-replicate.md)
- [results/step0-belief-readout-2026-05-17](../results/step0-belief-readout-2026-05-17.md)
- [results/commit-equivalence-2026-06-23](../results/commit-equivalence-2026-06-23.md)
- [results/precision-ladder-results-2026-06-22](../results/precision-ladder-results-2026-06-22.md)
- [results/llama-70b-scale-2026-06-22](../results/llama-70b-scale-2026-06-22.md)
- [results/qwen32b-stress-2026-06-25](../results/qwen32b-stress-2026-06-25.md)
- [results/commitment-convergence-2026-06-23](../results/commitment-convergence-2026-06-23.md)
- [results/v4-sealed-2026-05-26](../results/v4-sealed-2026-05-26.md)
- [results/bench-a2-signflip-2026-07-22](../results/bench-a2-signflip-2026-07-22.md)
