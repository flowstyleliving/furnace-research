# E3 label-efficiency under the A2 paired-stem draw (2026-07-14)

**What ran:** the registered E3 label-efficiency analysis (`analyze_universality.py`), re-run after
BENCH Amendment A2 made the subsample **paired-stem aware**. Default registered settings: sizes
{50, 100, 150}, repeats 10, nboot 1000, seed 20260613. Executor-run (Claude Code); Codex authored
the code and ran nothing.

**Why it matters:** the paper (`wiki/paper/cc-draft.tex`) claimed *"per-deployment calibration
requires \~150–200 labeled examples."* That figure was computed with the **old row-splitting draw**,
which on TriviaQA (100 question stems × 2 correlated rows) let a stem's correct row calibrate against
its own wrong twin — an optimistic bias. A2 fixed the draw. The question was whether the headline
survives.

> **Correction 2026-07-22 — the "\~150–200" framing is retired (Codex `gpt-5.6-sol` audit).** The E3
> analysis only ever evaluates budgets **{50, 100, 150}** (`analyze_universality.py` default
> `label_efficiency(sizes=(50,100,150))`); **no `n=200` point exists** in any artifact, under either
> the row-split or the stem-aware draw. The deployability curve is **still rising at n=150**
> (mean geometric 0.44 → 0.66 → 0.79). So "\~150–200 labels" was an **extrapolation past the data**,
> not a measurement. What this page's recomputation genuinely establishes is narrower and still true:
> the paired-stem correction **does not move the measured {50,100,150} budgets** (14/18 joint at 150,
> before = after). The honest headline is **≥150 labels as a measured lower bound, not a knee**. The
> paper and README were corrected to match on 2026-07-22.

## Verdict — the measured {50,100,150} budgets are stem-robust; "\~150–200" is retired

At **150 labels, 14/18 deployable deployments reach ≥0.8 deployability on BOTH endpoints** —
identical before and after A2. The paired-stem correction does not move the measured budgets; it does
**not** license the retired "\~150–200" phrasing (see the correction note above).

> **Count corrected 2026-07-15 (A4 executor regen).** This page originally headlined *15/18*; that
> was a miscount — inconsistent with its own "short of 0.8" table below, which lists **4** deployments
> under the bar (⇒ 14/18). The A4 regen of `universality.json` verified the true figure three ways:
> committed `bc6e2be` (old row-draw) = **14/18**, new stem-aware = **14/18**, and the regen is
> bit-identical to the Jul-14 stem-aware scratchpad run (deterministic). The headline is unmoved by
> A2 — it was always 14/18. (The handoff's E3 assertion also carried the wrong magic number `15` and
> an ANLI dict-equality bug that compared added provenance fields; both are assertion defects, not
> data drift. ANLI: **0/30 records changed** (0/60 scalar values moved).)

Per **individual** endpoint it is 15/18 each; the **joint** count (≥0.8 on *both* at once) is 14/18.
The headline is the joint figure — one cell (`Phi-3.5/anli`, full-only) and another (`Qwen3-1.7B/trivia`,
geom-only) each clear one endpoint but not both, so the intersection is 14, not 15.

| | full panel (per-endpoint) | geometric (per-endpoint) | both endpoints (joint) |
|---|---|---|---|
| OLD (row-split, committed `universality.json`) | 15/18 | 15/18 | 14/18 |
| NEW (stem-aware, post-A2) | 15/18 | 15/18 | 14/18 |

*(18 = the deployable cohort, i.e. excluding the two sealed ANLI orphans `Llama-3.1-8B/anli_r1`
and `gemma-3-4b/anli_r1`.)*

## Two checks that make the run trustworthy

- **ANLI is bit-identical: 0 of 30 numbers moved.** ANLI rows are independent, so they take the
  *preserved legacy row path*. Recovering the exact pre-A2 values is strong evidence Codex's
  refactor kept the old RNG path intact rather than producing merely plausible numbers.
- **TriviaQA moved in the theory-predicted direction.** All 8 changed cells are at n=50 (one also at
  n=100), and they mostly move **down** by ≤0.2 (`1.0/1.0→0.9/0.9`, `1.0/0.9→0.8/0.7`,
  `0.9/0.8→0.8/0.9`). Exactly what de-correlating the pairs should do at the smallest budget. One
  cell moved up (`Llama-3.1-8B/trivia 0.2/0.1→0.4/0.4`) — noise at 10 repeats.

## What it exposes (worth stating in the paper's E3 paragraph)

The label-cost figure was never uniform (and see the 2026-07-22 correction retiring "\~150–200").
Deployments still short of 0.8 at 150 labels (NEW):

| deployment | full | geom |
|---|---|---|
| `Qwen3-1.7B \| anli_r1` | 0.2 | 0.2 |
| `Llama-3.2-3B \| anli_r1` | 0.3 | 0.5 |
| `Phi-3.5-mini \| anli_r1` | 0.7 | 0.9 |
| `Qwen3-1.7B \| triviaqa_paired` | **1.0** | **0.3** |

The last row is the sharp one: on `Qwen3-1.7B/triviaqa` the full panel is fully calibrated by 150
labels while the geometric endpoint sits at 0.3 — it needs many more labels. Consistent with the
verification run, where that cell's geometric CI-lo was **0.5338** (barely over the 0.50 floor) vs
**0.7817** full. A genuinely marginal geometric deployment, not an artifact.

## Caveat — clustering is only half-addressed here

E3's **subsample** is now stem-aware, but the nested-OOB bootstrap **inside** it still resamples
**rows**. The honest statement is: *"the label-efficiency draw no longer splits stems; the inner
bootstrap remains row-level."* The confirmatory **stem-cluster bootstrap** is registered separately
for BENCH (`commit-confluence/stage_b/PRE_REGISTRATION_BENCH.md` §366) — that is the right home for
full clustering, not E3.

## Provenance / open item

- Fresh raw numbers: `<session-scratchpad>/universality_postA2.json` (transient) — key numbers
  transcribed above so they survive.
- The **committed** `commit-confluence/stage_b/universality.json` (`bc6e2be`) is now **stale** vs the
  A2 code (0 `subsample_unit` fields = row-split era). Tracked as **O3** in
  `commit-confluence/stage_b/OPEN_ITEMS.md`; recommendation is to regenerate + re-commit it bundled
  with the Amendment A4 execution so the registered artifacts move once.
