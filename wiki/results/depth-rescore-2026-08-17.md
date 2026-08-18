# Grid-A rescore under cross-fitted E5/E6 — the dip and cliff survive debiasing (2026-08-17)

**Status: pre-freeze CALIBRATION artifact for the depth-grid expansion (grid B).** The
registered grid-A verdicts ([[depth-curve-2026-08-16]]) are unchanged; this page reports
the same 8 banked cells rescored under the **candidate grid-B endpoint definitions**,
because the Codex round-2 audit required grid-B bars to be set against grid-A rates of
the *new* estimators, not the old permissive ones.

## Why this exists

The original E4 dip and E2 cliff statistics were in-sample: the peak was argmax'd over
all blocks on the same 200 rows used to estimate the contrasts — positively biased by
construction (Codex round-1 MAJOR 1–2). The new estimators cross-fit: stratified fixed
5-fold, directions + qualification (training-rows-only envelope) + peak selected on
training folds only, contrasts estimated held-out with locked directions; within-fold
synchronized label permutations for inference; (1+k)/(B+1) Monte Carlo conventions.
Process: spec by Codex round 2 → implementation → Codex round-3 code audit (YELLOW, 8
MAJORs fixed incl. within-fold permutations and an E6 R>0 condition) → round-4 fix
verification (all CONFIRMED; one JSON-safety blocker fixed) → single look.

## Verdict

| task | model | Δ_cf (dip) | E5 | J_cf | R_cf | E6 |
|---|---|---|---|---|---|---|
| anli | Qwen-7B | 0.242 | PASS | 0.180 | 0.300 | PASS |
| anli | Qwen-32B | 0.146 | PASS | 0.244 | 0.300 | PASS |
| anli | Qwen-72B | 0.212 | PASS | 0.234 | 0.296 | PASS |
| anli | Llama-70B | **0.416** | PASS | 0.206 | 0.206 | PASS |
| halueval | Qwen-7B | 0.202 | PASS | 0.310 | 0.332 | PASS |
| halueval | Qwen-32B | 0.261 | PASS | 0.343 | 0.290 | PASS |
| halueval | Qwen-72B | 0.264 | PASS | 0.245 | 0.309 | PASS |
| halueval | Llama-70B | 0.111 | PASS | UNDEF | — | FAIL |

- **E5 (cross-fitted terminal dip): 8/8**, pooled permutation p ≈ 0.0005 (floor at
  NPERM=2000); per-task 4/4 + 4/4; 8-cell aggregate Δ bootstrap CI [0.189, 0.261],
  joint undefined fraction 0. Dip magnitudes run 2–8× the 0.05 bar — **the registered
  8/8 was not a selection-bias artifact.**
- **E6 (cross-fitted directional cliff): 7/8**, pooled p ≈ 0.0005 — same count as the
  old E2, and the sole miss is the same cell (Llama-70B/halueval), now failing
  **structurally**: its peak sits at block 26 < 0.5·N = 40, so the cliff window
  `ceil(0.5N) ≤ j < peak` is empty ⇒ statistic undefined ⇒ counted as failure
  (conservative missingness rule). **Frozen-language consequence for the prereg:
  early-peak cells are E6-undefined by definition and count against confirmation.**
- All E6 null q95s are −inf: within-fold label permutations essentially never produce a
  qualifying training peak, so the fixed thresholds (J ≥ 0.15, R > 0, J ≥ 0.5·R) carry
  the discrimination — coherent per the D3/D7 conventions, undefined fractions recorded.
- Codex's E6 demotion condition ("if grid A is not clearly recurrent under the exact new
  rule, demote to descriptive") **resolves in favor of keeping E6 confirmatory-gatekept.**

## Consequences for the grid-B freeze

Grid-A discovery rates under the frozen candidate estimators: **dip 8/8, cliff 7/8 (1
structural UNDEF)**. The round-2 provisional bars (E5 CONFIRM ≥10/12 with family guard
and p_grid < 0.05; E6 ≥9/12 with task/family guards, gatekept) now rest on honest
discovery rates and can be frozen as-is unless the freeze-time audit adjusts them.

## Artifacts + provenance

`commit-confluence/exploratory/depth-curve/`: `rescore_grid_a.py` (self-documenting:
D1–D9 decisions in the docstring), `RESCORE_GRID_A.{json,md}` (JSON carries npz sha256s,
source sha256s, fold maps + hashes, numpy version). Seal venv (numpy 2.0.2 / scipy
1.13.1). Single look enforced in-code: refuses to run when outputs exist; atomic writes;
no observed value printed before completion. RS_SEED 20260817, 5-fold, NPERM_INNER 200,
NPERM_OUTER 2000, NBOOT 1000.

Backlinks: [[depth-curve-2026-08-16]] · [[../workorders/depth-grid-expansion-workorder-2026-08-17]] ·
[[../paper/dc-scaffold]] · [[../research-candidates]] §13
