# Depth-grid expansion (grid B) — registered verdict: E5 WEAKEN 8/12; the Llama band replicates at 3.1-70B (2026-08-17)

**Status: [REGISTERED — E5 WEAKEN; E6 NOT TESTED (gate closed)].** Single-look
verdict of `commit-confluence/exploratory/depth-curve/PRE_REGISTRATION_EXPANSION.md`
(freeze @ `2062e56`; results @ `cdc55a9`). Prospective **held-out-model confirmation
on two fixed benchmarks** (ANLI R1 + HaluEval-QA), 6 new models × 2 tasks = 12 core
cells, cross-fitted E5/E6 per the nine-round Codex gpt-5.6 audit dialogue. Torch/Modal,
NON-byte-comparable; sealed claims untouched; grid A ([[depth-curve-2026-08-16]],
[[depth-rescore-2026-08-17]]) is discovery, never pooled.

## Verdict

**E5 (cross-fitted terminal dip, primary): WEAKEN — 8/12.** Every evaluable cell
passed except one; the frozen CONFIRM bar (≥10/12 AND ≥3/4 per family AND p_grid
< 0.05) failed on the count and the gemma family guard while **p_grid = 0.0005**
held. Pooled all-defined dip CI [0.123, 0.201]; leave-Medium-out 6/10;
evaluable-only 8/9.

| task | model | Δ_cf | E5 | note |
|---|---|---|---|---|
| anli | Llama-3.1-8B | 0.141 | PASS | |
| anli | Llama-3.1-70B | 0.141 | PASS | |
| anli | Mistral-Small-3.2 | — | FAIL | registered behavioral gate: row-1 commit `'To'` (CoT opener, same signature as Qwen2.5-7B in BENCH) |
| anli | Mistral-Medium-3.5 | 0.293 | PASS | FP8-origin dequant-BF16 cell |
| anli | gemma-3-12b | 0.218 | PASS | |
| anli | gemma-3-27b | — | FAIL | **instrument-domain boundary** (below) |
| halueval | Llama-3.1-8B | 0.106 | PASS | |
| halueval | Llama-3.1-70B | 0.201 | PASS | |
| halueval | Mistral-Small-3.2 | **0.0045** | FAIL | the one **true on-data miss** — dip essentially absent |
| halueval | Mistral-Medium-3.5 | 0.151 | PASS | |
| halueval | gemma-3-12b | 0.306 | PASS | |
| halueval | gemma-3-27b | — | FAIL | instrument-domain boundary |

**E6 (cliff, gatekept): NOT TESTED — gate closed** (E5 did not CONFIRM).
Descriptively 2/12 cells satisfy the cross-fitted cliff rule (gemma-12b/anli,
Medium/halueval); many cells are E6-undefined by early peaks (empty window).

## The three failure modes are three different findings

1. **Behavioral gate (Small-3.2/anli):** the model answers "To determine…" instead
   of committing YES/NO on gate row 1 — pre-registered gate class, no rescue.
2. **Instrument-domain boundary (gemma-27b, both tasks):** the SEALED kernel
   returns `None` for `final_js_no_bos` at block 3 — extreme BOS-sink attention
   leaves no distribution after the sink column is stripped. Grid A's four models
   never entered this regime. The metric has a domain; gemma-27b exits it by
   block 3. (Paper-grade caveat for every js_no_bos use.)
3. **True miss (Small-3.2/halueval):** clean extraction, gates passed, Δ_cf 0.0045
   ≈ zero — the terminal dip is genuinely absent in this cell.

## Descriptives (registered)

- **P8 HIT / P9 HIT — the Llama mid-stack band is lineage-stable and scale-emergent
  (descriptive language: present at 70B, absent at 8B).** Qualifying mid-blocks
  [0.4N, 0.9N] per fold: 3.1-70B anli **24/25/24/23/22**, halueval 20/19/16/16/16;
  grid-A 3.3-70B context: 27–29 (anli), 25–31 (halueval); 3.1-8B: 3–6 (anli),
  7–8 (halueval). The band the three-rung panel missed is not a 3.3 quirk.
- **E7 (cross-task peak distance):** Medium tight (83 vs 85 of 88); 70B moderate
  (45 vs 38 of 80, CI wide); 8B extreme (18 vs 1 of 32 — halueval peaks at
  block 1); gemma-12b 39 vs 22 of 48. Peak location remains (model, task)-dependent.
- **E1″ family clusters (peak fraction, grids labeled, never pooled):** mistral
  0.88 ± 0.13 and qwen(A) 0.85 ± 0.06 peak late; llama31 0.41 ± 0.25 ≈ llama33(A)
  0.46 ± 0.19 mid-stack; gemma 0.64 ± 0.25 between. Family structure is visible;
  **no transferable placement rule** (P10 as expected).
- P6 MISS (E5 did not CONFIRM); P7 not evaluated (gate closed).

## Process provenance

Nine-round Codex gpt-5.6 dialogue (plan RED → stats spec → code RED with 9 MAJORs →
fix rounds → GREEN); gates-only smoke on one pinned toolchain (transformers 5.15.0,
torch 2.13, bnb 0.50.1, mistral-common 1.11.7 — after two pre-freeze repins the
smoke itself surfaced); manifest pinning + terminal-status immutability enforced
in-extractor; freeze commit `2062e56` BEFORE any outcome-bearing extraction;
staged detached extraction (12/12 terminal, incl. the two aborts as designed);
scorer ran ONCE. mistral-common cross-check: 0/400 mismatches on both Mistral
models. Medium dequant frozen from smoke: `from_pretrained(bf16)` on 4×A100
(transformers auto-dequantizes FP8 on capability 8.0), 1233/1233 bf16 params.

## Caveats

n=200; two benchmarks only (held-out-model claim, nothing task-general); Medium is
FP8-origin (its two cells flagged; leave-Medium-out sensitivity 6/10); torch lane
non-byte-comparable; per-cell cross-fitted statistics share items across models
(handled by synchronized permutations); 405B never run (outside denominators,
still MK go/no-go).

## Artifacts

`commit-confluence/exploratory/depth-curve/`: `PRE_REGISTRATION_EXPANSION.md`,
`modal_depth_b.py`, `score_grid_b.py`, `manifests_gridb/`, `run_grid_b.sh`,
`GRID_B_RESULTS.{json,md}`, `npz/depth_grid_b/` (freeze `2062e56` → results
`cdc55a9`). Raw npz + statuses also on the Modal volume under `depth_grid_b/`.

Backlinks: [[depth-curve-2026-08-16]] · [[depth-rescore-2026-08-17]] ·
[[../workorders/depth-grid-expansion-workorder-2026-08-17]] · [[../paper/dc-scaffold]] ·
[[../research-candidates]] §13
