# Motif and absorption audit (2026-09-10)

_Status: `[RESOLVED, §B CORRECTED 2026-09-10]`. Descriptive re-analysis of banked parquets. **No model run, no gate re-read, no sealed verdict touched.** Companion to [[results/orientation-artifact-audit-2026-09-10]]._

Four checks run back-to-back. **Three found errors in published claims; one closed a data-contract gap.**

⚠️ **§B below was itself wrong on first publication and has been rewritten.** It concluded that Gemma's rank flip was an orientation artifact; a same-day meta-audit by `gpt-6-astra` showed the flip survives, and that the mechanism this page proposed was as unsupported as the one it replaced. The corrected §B is the authoritative version and matches `pri-draft.tex` §4.3. **Anyone citing this page for the Gemma motif must cite the corrected text, not the original claim.**

## A — "Residualization absorbs the coordinate mismatch": NOT SUPPORTED as stated

`run-02` carries **both geometries on identical rows** (`null_ratio_rank1` legacy, `null_ratio_post_rank1` corrected), so this is a perfectly matched test with no cross-run confound.

| model | unresidualized move | residualized move | absorbed? |
|---|---|---|---|
| Llama 3.2 3B | 0.0840 | **0.0011** | ✅ near-total (76×) |
| Mistral 7B | 0.0097 | **0.0165** | ❌ **none — residualizing makes it *worse*** |
| Qwen 2.5 7B | 0.1343 | **0.0758** | ⚠️ partial (44%) |

The claim held on one model, **failed on a second**, and half-held on the third. What survives is the weaker, sufficient statement: residualization **preserved the E18 verdict** under both geometries. That is not a general invariance and the paper no longer asserts one.

## B — Motif 2 (Gemma rank flip): REAL, but with no supported mechanism

⚠️ **This section was wrong when first published on 2026-09-10 and is rewritten here.** It originally concluded the flip "does not survive a fixed orientation" and attributed it to Fisher crossing the folding threshold. **That explanation is false** — caught by `gpt-6-astra` in a meta-audit the same day. The corrected reading follows; `pri-draft.tex` §4.3 already carries it.

**The flip is not produced by a sign change.** Across $r=2 \to r=3$ Fisher's unoriented AUROC moves **0.119 → 0.373** and Raw's **0.674 → 0.837**. *Neither metric changes sign* — Fisher is below 0.5 at every rank from 1 to 5, so it never crosses the folding threshold in this region at all. Holding each metric's own sign fixed across the sweep still yields **+0.208 then −0.211**. What changes is relative discrimination *strength*: Fisher's falls with rank while Raw's rises.

| rank | Fisher unoriented | Raw unoriented | Δ, each metric's own sign held fixed |
|---|---|---|---|
| 1 | 0.259 | 0.472 | +0.213 |
| 2 | **0.119** | 0.674 | **+0.208** |
| 3 | 0.373 | 0.837 | **−0.211** |

🚫 **Two explanations are refuted, not one.** The paper's original "property of the SVD spectrum" claim, and this page's own replacement "folding threshold" claim. **No measurement here identifies a mechanism**, and none should be asserted.

🕳️ **Separately and still true:** Fisher is *anti*-predictive at every rank across this region, and folding fires at **11 of Gemma's 13 ranks**. So "Fisher decisive" below r=3 means Fisher's *inverted* score discriminates more strongly, not that the registered direction holds. Fixing both metrics to the registered direction makes Raw decisive at all 13 ranks — which answers a different question (does the score point the hypothesized way) from the one the motif asks (does relative strength change with rank).

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
