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
- **Label cost (descriptive sweep, 2026-07-26).** HaluEval-QA subsample deployability: 1.0 at every budget incl. 50. Cohort-wide: 10/10 at 1.0 by 150 labels, flat through 500 (a measured knee). Post-hoc, not a registered endpoint — [[results/e3-halueval-descriptive-2026-07-26]].

## Model-specific quirks
- Qwen3 is less stable and more context-sensitive than Qwen2.5.
- It helped expose the family split: Qwen2.5 sits on the attention locus, Qwen3 is the more fragile sibling.

## Validity audits (2026-09-10, descriptive)

- 🚨 **Its 19.3% "error rate" is a formatting artifact, not errors — and it invalidated a published result.** Under the sealed `max_new_tokens`=14 budget this reasoning-tuned model either leads with `Answer:` or opens a chain-of-thought preamble the budget truncates. By first word: `Answer:` → **484 correct / 1 error**; `Let's` (68), `Alright,` (37), `Okay,` (10) → **115 errors / 0 correct**.
- 🔴 **The outcome label is fixed by the first generated token in 599 of 600 cases — and `gen_step=1` IS that token.** An error-prediction AUROC on this label asks whether a hidden state predicts which token occupies its own position. The figures **0.8570** (within-contradiction) and **0.8906** (pooled) were published and **withdrawn the same day**.
- 🧭 **This reproduces the project's documented STEP-0 crack**: for reasoning-tuned models `gen_step=1` is a preamble rather than a commitment. Known since 2026-05-17 for the v4 lane; the v3 paper predates the fix.
- 📉 **Consequence for the whole study:** with Qwen3's rate reinterpreted, **no model in the lineup has a measurable error rate.**
- 📊 Raw folds at **13 of 13** ranks — the only all-fold cell in the panel. Sign nonetheless 100% transferable, held-out Raw 0.9475.

→ [[results/motif-audit-2026-09-10]] · [[log]] 2026-09-10 nineteenth entry

## Canonical backlinks
- **KV-tension pilot (2026-06-08, scored 2026-07-25) — NO-PROMOTE.** Highest best-KV AUROC in the panel, `js_within_kv_groups` **0.8479** (also the selected winner), but only **+0.0075** over the best existing comparator — a win in level, not in increment. OOB CI-lo 0.7382; `winner_unstable` fires (stability 0.59).

- [results/v3.1-replicate](../results/v3.1-replicate.md)
- [results/v4-prep-coverage-matrix-2026-05-16](../results/v4-prep-coverage-matrix-2026-05-16.md)
- [results/step0-belief-readout-2026-05-17](../results/step0-belief-readout-2026-05-17.md)
- [results/t0-residual-pilot-2026-05-28](../results/t0-residual-pilot-2026-05-28.md)
- [results/residual-friction-pilot-2026-06-06](../results/residual-friction-pilot-2026-06-06.md)
- [results/qwen32b-stress-2026-06-25](../results/qwen32b-stress-2026-06-25.md)
- [results/bench-a2-signflip-2026-07-22](../results/bench-a2-signflip-2026-07-22.md)
- [results/kv-tension-pilot-2026-06-09](../results/kv-tension-pilot-2026-06-09.md)
- [results/e3-halueval-descriptive-2026-07-26](../results/e3-halueval-descriptive-2026-07-26.md)
