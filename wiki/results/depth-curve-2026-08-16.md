# Depth-curve registered run — per-layer attention separation, 4 models × 2 tasks (2026-08-16)

**Status: [OPEN — registered descriptive; E1 UNDECIDED].** Pre-registered exploratory run
(`commit-confluence/exploratory/depth-curve/PRE_REGISTRATION.md`, frozen @ `fadbaff`,
post-audit fixes @ `c56b7e1`, results @ `768ea7e`). Torch/Modal nf4, NON-byte-comparable,
does **not** touch any sealed claim. Successor to the three-rung read in
[[depth-marginals-2026-08-16]] — and it **overturns that read's sharpest conclusion**.

## Design (frozen before any run)

Per-layer sign-free AUROC of the sealed inter-head-disagreement metrics (primary
`js_no_bos`) at t=0, **every decoder block**, computed by the sealed kernel per block.
Vehicles: Qwen2.5-7B/32B/72B (N=28/64/80) + Llama-3.3-70B (N=80) as registered
negative-control family. Tasks: ANLI R1 + HaluEval-QA, n=200, frozen data hashes
enforced in-extractor. Gates: o_proj cos ≥ 0.999, YES/NO ≥ 0.5, zero dropped rows —
**8/8 cells passed**. Statistics: 1000-resample bootstrap for peak location ℓ*,
200-permutation shuffled-label envelope (97.5th pct), qualifying peak = AUROC ≥ 0.65 and
above envelope. Process: Codex static audit (YELLOW, no blockers; sealed-kernel reuse
verified exact) closed pre-launch; scorer ran ONCE over all 8 cells (first look).

## Registered verdicts

| task | model | N | ℓ\* | boot 90% CI | N−ℓ\* | ℓ\*/N | peak | mid-med | E2 | E4 dip |
|---|---|---|---|---|---|---|---|---|---|---|
| anli | Qwen-7B | 28 | 22 | [22, 25] | 6 | 0.79 | 0.834 | 0.546 | CLIFF | Y |
| anli | Qwen-32B | 64 | 56 | [56, 62] | 7 | 0.89 | 0.865 | 0.545 | CLIFF | Y |
| anli | Qwen-72B | 80 | 66 | [66, 77] | 14 | 0.83 | 0.838 | 0.539 | CLIFF | Y |
| anli | **Llama-70B** | 80 | **48** | [48, 74] | 11 | 0.86* | **0.897** | 0.649 | CLIFF | Y |
| halueval | Qwen-7B | 28 | 26 | [26, 26] | 2 | 0.93 | 0.871 | 0.546 | CLIFF | Y |
| halueval | Qwen-32B | 64 | 56 | [35, 61] | 8 | 0.88 | 0.911 | 0.618 | CLIFF | Y |
| halueval | Qwen-72B | 80 | 63 | [63, 63] | 17 | 0.79 | 0.896 | 0.595 | CLIFF | Y |
| halueval | **Llama-70B** | 80 | **26** | [26, 48] | 47 | 0.41 | 0.862 | 0.721 | GRADUAL | Y |

(\*the ℓ\*/N column is the bootstrap-median fraction, so it can differ from the point
ℓ\*/N — Llama/anli's point ℓ\*=48 is 0.60 of the stack; its wide CI reflects a broad
spiky band, not one sharp peak.)

- **E1 (peak placement law): UNDECIDED on both tasks.** Full-resolution peaks sit at
  N−2 … N−17 (fractions 0.79–0.93 for Qwen) with spans too wide for either frozen rule.
  **The three-rung "peak at N−2" was a rung-resolution artifact** — N−2 was merely the
  best of three samples; the true maxima sit deeper. **No transferable depth rule exists
  at this resolution**: peak placement is (model, task)-dependent, with unstable
  bootstrap bands in half the cells.
- **E2 (rise shape): CLIFF in 7/8 cells.** The separation switches on in essentially one
  block — e.g. Qwen-72B/anli jumps +0.233 at block 61→62; Qwen-7B/halueval +0.232 at
  18→19. Llama/halueval is the one GRADUAL cell.
- **E3 (early layers):** ANLI front-half is quiet (0–3 qualifying early blocks); HaluEval
  is **not** — 4–16 early blocks separate per cell (Llama-70B: block 0 already at 0.70).
  Task-dependent, not a universal "early layers are silent."
- **E4 (terminal dip): 8/8.** The final block always loses ≥ 0.05 from the peak — the
  only frozen prediction (P5) that survived; the most invariant depth regularity found.

## Prediction outcomes (report-as-registered)

- **P1 MISS** — Qwen peaks in the last 4 blocks: only 1/6 cells (halueval-7B).
- **P3 MISS — and it is the headline.** The negative control has **qualifying mid-stack
  attention peaks**: Llama-70B/anli is ≈0.5 through block 43, then a broad band 0.63–0.90
  through the 60s (44/80 blocks clear the shuffled envelope, ceiling 0.615); peak 0.897 at
  block 48 **exceeds its own panel readout winner (0.816)**. The three-rung panel sampled
  blocks 40/78/79 — all outside the band. **"Llama family → readout locus" was
  panel-relative, not model-truth: the panel's depth sampling was blind exactly where
  Llama's attention signal lives.** (The sealed/panel claims themselves are unchanged —
  panel winners are what they are; this bounds their *interpretation*.)
- **P4 MISS (narrow)** — Qwen mid-region quiet held on ANLI (0.539–0.546) but HaluEval
  mid-regions are warm (0.595–0.618 vs the 0.60 bar).
- **P5 HIT** — terminal dip at 32B and 72B on both tasks (and in fact 8/8).

## Caveats

In-sample, sign-free (max-side) AUROCs; per-cell argmax over N blocks is selection-heavy
(mitigated by the envelope + bootstrap, not eliminated); n=200; non-byte-comparable torch
lane; per-layer curves are a different instrument from the sealed 3-rung panel — never
pool. Mechanism claims deferred (v6–v8 same-Δh lesson stands).

## Artifacts

`commit-confluence/exploratory/depth-curve/`: `RESULTS.{json,md}`, `depth_curves.png`
(8-curve figure), `npz/depth_curve/<task>/<slug>.depth.npz` (+ gates), all committed @
`768ea7e`; raw copies on the Modal volume under `/depth_curve/`. Extraction provenance in
each npz meta (code commit, HF revisions, library versions, sealed-kernel hashes).

Backlinks: [[depth-marginals-2026-08-16]] · [[llama-70b-scale-2026-06-22]] ·
[[qwen32b-stress-2026-06-25]] · [[../models/llama-3.3-70b]] · [[../models/qwen-2.5-7b]] ·
[[../models/qwen-2.5-32b]] · [[../models/qwen-2.5-72b]]
