# Mistral 7B Instruct v0.3 (4-bit)

MLX handle: `mlx-community/Mistral-7B-Instruct-v0.3-4bit`

## Specs
- Size: 7B parameters
- Quantization: 4-bit (MLX)
- Backend: MLX
- Output projection: untied `lm_head`

## Role in the research line
- v3 primary.
- Chain-length Simpson's paradox model.
- Older sibling to the Mistral-Nemo terminal-commit anchor.

## Main verdicts
- `v3-main-run` - sealed E18 passes at rank 1; Raw is decisive in the pooled view.
- `v4-sealed-2026-05-26` - exact ANLI and TriviaQA transfer at t=0.
- `inter-head-disagreement-2026-05-15` - clean head-disagreement case once BOS sinks are controlled.
- `step0-belief-readout-2026-05-17` - Mistral-Nemo is the immediate-commit anchor for the family.
- `t0-residual-pilot-2026-05-28` - residual sign=-1 with moderate OOB support.
- `residual-friction-pilot-2026-06-06` - the apparent friction story does not survive the same-`Δh` floor.
- `depth-marginals-2026-08-16` - the small-model exception: crisp big-model-style N−2 depth peak already at 32 blocks (sealed js-family 6/6, N−2 mean 0.812 vs mid 0.590).

## BENCH (CC extension, 2026-07-22)
Registered strict Phase-4 HaluEval-QA transfer test — [[results/bench-a2-signflip-2026-07-22]] (byte-comparable MLX cells).
- **A1 — deployable.** Geometric winner `Readout fisher_eff_rank @ step 0`, stem-cluster geometric OOB CI-lo **0.8414**. Part of A1 10/10.
- **A2 polarity — own sign `+1` on `fusion_rank_mean_geom`** ⇒ high fused score = **hallucinated** (opposite to the `−1` majority). Blind LOMO transfer under the pooled `−1` sign: AUROC **0.174** — an **intrinsic sign-flip: signal present, orientation opposite**, not signal absence. Reversing to `+1` recovers 0.826, but **reversal is not an A2 rescue** — knowing to reverse requires this model's own labels, exactly what blind transfer forbids.
- **[OPEN — observation, not a finding]** Mistral-7B is one of the three flippers (with Mistral-Nemo and Qwen2.5-7B) that coincide with the v4 sealed E_A2 partial-transfer trio ([[results/v4-sealed-2026-05-26]]). Untested overlap, logged as an observation; do **not** state it as a finding.
- Both Mistral members flip (`+1`), but this is descriptive only (family confounded with tokenizer/architecture/size); cohort-wide polarity is **generation-structured, not a family law**. Framing: A2 rejects "fixed cell + fixed sign," not the cell.
- **Label cost (descriptive sweep, 2026-07-26).** HaluEval-QA subsample deployability: 0.7 at 50, 1.0 from 100 up. Cohort-wide: 10/10 at 1.0 by 150 labels, flat through 500 (a measured knee). Post-hoc, not a registered endpoint — [[results/e3-halueval-descriptive-2026-07-26]].

## Model-specific quirks
- The newline-commit pattern makes the chain-length axis matter.
- The pool-level Raw story is a Simpson's-paradox artifact; the strata tell the cleaner story.

## Canonical backlinks
- **KV-tension pilot (2026-06-08, scored 2026-07-25) — NO-PROMOTE.** `last_minus_1_js_kv_tension_ratio` selected, best-KV 0.8065, **+0.0195** over comparator — below the +0.03 bar. OOB CI-lo 0.6931; `winner_unstable` (stability 0.60).

- [results/v3-main-run](../results/v3-main-run.md)
- [results/v4-sealed-2026-05-26](../results/v4-sealed-2026-05-26.md)
- [results/inter-head-disagreement-2026-05-15](../results/inter-head-disagreement-2026-05-15.md)
- [results/step0-belief-readout-2026-05-17](../results/step0-belief-readout-2026-05-17.md)
- [results/t0-residual-pilot-2026-05-28](../results/t0-residual-pilot-2026-05-28.md)
- [results/residual-friction-pilot-2026-06-06](../results/residual-friction-pilot-2026-06-06.md)
- [results/v4-sealed-2026-05-26](../results/v4-sealed-2026-05-26.md)
- [results/bench-a2-signflip-2026-07-22](../results/bench-a2-signflip-2026-07-22.md)
- [results/kv-tension-pilot-2026-06-09](../results/kv-tension-pilot-2026-06-09.md)
- [results/e3-halueval-descriptive-2026-07-26](../results/e3-halueval-descriptive-2026-07-26.md)
- [results/depth-marginals-2026-08-16](../results/depth-marginals-2026-08-16.md)
