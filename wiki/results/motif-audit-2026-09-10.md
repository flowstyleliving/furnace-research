# Motif and absorption audit (2026-09-10)

_Status: `[RESOLVED]`. Descriptive re-analysis of banked parquets. **No model run, no gate re-read, no sealed verdict touched.** Companion to [[results/orientation-artifact-audit-2026-09-10]]._

Four checks run back-to-back. **Three found errors in published claims; one closed a data-contract gap.**

## A — "Residualization absorbs the coordinate mismatch": NOT SUPPORTED as stated

`run-02` carries **both geometries on identical rows** (`null_ratio_rank1` legacy, `null_ratio_post_rank1` corrected), so this is a perfectly matched test with no cross-run confound.

| model | unresidualized move | residualized move | absorbed? |
|---|---|---|---|
| Llama 3.2 3B | 0.0840 | **0.0011** | ✅ near-total (76×) |
| Mistral 7B | 0.0097 | **0.0165** | ❌ **none — residualizing makes it *worse*** |
| Qwen 2.5 7B | 0.1343 | **0.0758** | ⚠️ partial (44%) |

The claim held on one model, **failed on a second**, and half-held on the third. What survives is the weaker, sufficient statement: residualization **preserved the E18 verdict** under both geometries. That is not a general invariance and the paper no longer asserts one.

## B — Motif 2 (Gemma rank flip): DOES NOT SURVIVE a fixed orientation

Folding fires at **11 of Gemma's 13 ranks**, and Fisher is *anti*-predictive across the flip region — unoriented AUROC **0.259** at r=1 and **0.119** at r=2.

| rank | Δ fitted (published rule) | Δ fixed (registered direction) |
|---|---|---|
| 1 | **+0.213** Fisher | −0.213 Raw |
| 2 | **+0.208** Fisher | −0.555 Raw |
| 3 | −0.210 Raw | −0.464 Raw |

Under a single sign fixed in the registered direction, **Raw is decisive at all 13 ranks and there is no flip anywhere.** What the fitted rule renders as a rank flip is the rank at which Gemma's Fisher score crosses the folding threshold — not a transition in the SVD spectrum.

🔎 **Motif 1 (Phi) survives** and arguably strengthens: `Δ_fixed` is negative at all 13 ranks, so Raw is decisive under either rule.

## C — "Largest cross-stratum spread across all 156 cells": FALSE

Re-ranked all 78 (model × rank) pairs — 156 cells with both strata, matching the paper's own grid.

| rule | largest \|Δ_cross\| | runner-up |
|---|---|---|
| fitted (published) | **Qwen 2.5, r=16, +0.7417** | Mistral r=32, −0.5740 |
| fixed | **Mistral, r=64, +1.0064** | Qwen 2.5 r=13, −0.9084 |

**Mistral r=32 is not the maximum even under the paper's own rule** — Qwen 2.5 at r=16 exceeds it. The claim is withdrawn rather than rescoped. Both larger cells are themselves heavily folded (Qwen r=16: Fisher 0.0349 at cl=2, Raw 0.0838 at cl=5), which is the substantive point — **cross-stratum spread magnitudes are not orientation-stable and should not be ranked.**

## D — Descriptive runs now have scored JSON

`analyze_sealed_gate.py` is primary-gated, so Phi and Gemma had no machine-readable scores and every published descriptive number was unverifiable. Wrote `descriptive_scores.json` to both run directories, covering all 13 ranks × both metrics, with `auroc`, `auroc_unoriented` and `sign`.

⚠️ Each file carries an explicit header: **not a sealed gate**, produced from banked parquets so descriptive numbers are checkable. Phi `null_ratio_raw_post_rank1` = **0.9989** (sign +1), matching the published value exactly; Gemma = 0.5280 (sign −1).

## Scope

- 🔒 Moves **no** sealed verdict. E17b and E18 are defined on the pooled sealed cell and are untouched.
- ➖ A used run-02 (n=200) because it is the only run carrying both geometries; the n=600 run has post-norm only.
- ➖ C ranked cells but did not re-derive CIs for the newly-identified maxima.

→ [[results/orientation-artifact-audit-2026-09-10]] · [[log]] 2026-09-10 · `pri-draft.tex` §1, §4.3, §3.5
