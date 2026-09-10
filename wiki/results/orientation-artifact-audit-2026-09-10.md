# Orientation-artifact audit — Mistral Simpson's-paradox sites (2026-09-10)

_Status: `[RESOLVED — SPLIT]`. Descriptive re-analysis of banked parquets. **No model run, no gate re-read, no sealed verdict touched.** Closes [[workorders/orientation-artifact-audit-workorder-2026-09-10]]._

**Verdict: the two sites behave differently, and the split falls exactly on the sealed rank.**

- ✅ **Site #1 ($r=1$, the sealed rank) — SURVIVES, and is provably orientation-independent.**
- ⚠️ **Site #2 ($r=32$–$34$) — the disagreement survives, but its headline magnitude does not.**

## The question

Every AUROC in the paper is `max(AUROC, 1−AUROC)` with the sign fitted on that cell's own labels. Pooled and stratified cells therefore orient independently, so `Δ_oriented` is not a common estimand across them and a pooled-versus-stratum reversal could be manufactured by the orientation rule alone. Raised by `deepseek-v4-pro`, 2026-09-10. ⚠️ The manuscript had stated the confound *as* the explanation — §4.3 attributed the reversal to strata "whose Fisher and Raw discrimination axes have different orientations."

## Method

Mistral 7B, `2026-04-26/run-09`, `gen_step=1`, n=600. For ranks 1, 32, 34 × {pool, cl=2, cl=5}, `Δ = AUROC(Fisher) − AUROC(Raw)` under three rules: **fitted** (per-cell sign, what the paper does), **unoriented** (no folding), **fixed** (one sign per metric, chosen on the pooled cell, applied unchanged to both strata — the deployment-realistic rule the production calibrator uses). Paired bootstrap, 1000 resamples, seed 20260423, matching the paper's protocol.

## The decisive diagnostic — where folding actually fires

| rank | cell | Fisher unoriented | Raw unoriented |
|---|---|---|---|
| 1 | pool | 0.7849 | 0.9254 |
| 1 | cl=2 | 0.9887 | 0.9243 |
| 1 | cl=5 | 0.9412 | 0.9389 |
| 32 | pool | **0.2606** folded | **0.4363** folded |
| 32 | cl=2 | **0.4149** folded | **0.2199** folded |
| 32 | cl=5 | **0.0279** folded | 0.5932 |

**At $r=1$ nothing is folded** — all six cells exceed 0.5, so all three orientation rules return byte-identical numbers and orientation cannot be the cause of anything. **At $r=32$ five of six cells are folded.**

## Site #1 — $r=1$, survives

| cell | Δ (all three rules identical) | 95% CI |
|---|---|---|
| pool | **−0.1405** | [−0.173, −0.107] |
| cl=2 | **+0.0644** | [+0.041, +0.093] |
| cl=5 | **+0.0023** | [−0.022, +0.028] |

Pool says Raw decisive; neither stratum does. `Δ_cross = +0.0621` under every rule. **A real Simpson's reversal, and a property of the data rather than the metric.** The paper's published values (−0.140 / +0.065 / +0.002) reproduce exactly.

## Site #2 — $r=32$–$34$, magnitude is rule-dependent

| rule | pool | cl=2 | cl=5 | `Δ_cross` |
|---|---|---|---|---|
| fitted (published) | +0.1757 | −0.1950 | +0.3789 | **−0.5740** |
| fixed (pooled sign) | +0.1757 | −0.1950 | **+0.5653** | **−0.7604** |
| unoriented | −0.1757 | +0.1950 | −0.5653 | **+0.7604** |

Two things to carry:

- 🔀 **The cross-stratum disagreement survives every rule** — cl=2 and cl=5 always point opposite ways. That much is real.
- 📉 **The magnitude does not travel.** `Δ_cross` is −0.575 as published, −0.760 under a fixed orientation, +0.760 unoriented. The "largest spread across all 156 cells" ranking is therefore **rule-relative**, since every other cell would also move.
- 🕳️ **The load-bearing cell is an inverted detector.** Fisher at cl=5 has unoriented AUROC **0.0279** — near-perfect *anti*-prediction — reported as 0.9721 "Fisher decisive." The single fitted-vs-pooled sign disagreement in the whole grid is the cl=5 Raw cell, and it alone drives −0.575 → −0.760.

## Scope

- 🔒 **Moves no sealed verdict.** E17b and E18 are defined on the pooled sealed cell and are untouched.
- ➖ Mistral only, and only the ranks the two sites occupy. Whether other models' motifs are orientation-stable is **not** tested here.
- ➖ The "largest of 156" claim was **not** re-ranked under a fixed orientation; doing so would require recomputing the full grid.

## Consequences applied to `pri-draft.tex` §4.3

Site #1's bullet now states it was re-derived unfolded and under a fixed sign, that no cell is folded, and that the reversal is a property of the data. Site #2's bullet now names the orientation rule its number depends on, reports the unoriented readings including the 0.0279, and says plainly that the disagreement survives while the magnitude and the "largest of 156" ranking do not.

→ [[workorders/orientation-artifact-audit-workorder-2026-09-10]] · [[log]] 2026-09-10 · `pri-draft.tex` §4.3, §3.2
