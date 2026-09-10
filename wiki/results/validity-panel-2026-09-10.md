# PRI v3 validity panel — five diagnostics (2026-09-10)

_Status: `[RESOLVED]`. Descriptive re-analysis of banked parquets. **No model run, no gate re-read, no sealed verdict touched.** Tool: `PRI_at_commitment/scripts/validity_panel.py` (repo `79e87e7`, `daa94bb`, `3c2b7a6`)._

Five checks on whether the measured quantity supports the claimed one. **Two came back favourable, one is the paper's most serious limitation, and one published result was withdrawn the same day.**

## 1 — Outcome ceiling: the study cannot test error prediction

| model | n | errors | rate |
|---|---|---|---|
| Mistral 7B | 600 | 0 | **0.0%** |
| Phi-3.5-mini | 600 | 0 | **0.0%** |
| Gemma 3-4B | 600 | 0 | **0.0%** |
| Llama 3.2 3B | 600 | 2 | 0.3% |
| Qwen 2.5 7B | 600 | 5 | 0.8% |
| Qwen3-8B | 600 | 116 | 19.3% |

Five of six answer ≥99.2% correctly. The abstract motivates hallucination detection; on those five there is nothing to detect. **What is measured is the geometric response to a contradictory prompt the model then handles correctly.**

⚠️ **And the sixth does not rescue it — see §4.**

## 2 — Folding incidence: where `max(AUROC, 1−AUROC)` fires

| model | Fisher folded | Raw folded | at sealed r=1 |
|---|---|---|---|
| Llama 3.2 3B | **0/13** | 10/13 | Raw folded |
| Mistral 7B | 3/13 | 7/13 | neither |
| Qwen 2.5 7B | 6/13 | 9/13 | Raw folded |
| Qwen3-8B | 2/13 | **13/13** | Raw folded |
| Phi-3.5-mini | 6/13 | **0/13** | neither |
| Gemma 3-4B | **11/13** | 1/13 | **both** |

A cell that never folds cannot carry an orientation artifact. Llama's Fisher and Phi's Raw are clean by inspection; Gemma is the heaviest folder and is also the model whose motif failed.

## 3 — Sign stability: the orientation concern does not become instability

Split-half, 200 splits — fit the sign on one half, score the other, so the held-out figure carries **no in-sample orientation advantage**.

- ✅ **100% agreement with the full-sample sign in 10 of 12 cells.**
- ✅ Held-out AUROC **0.8971** (Qwen 2.5 Fisher), **0.8956** (Llama Fisher), **0.9988** (Phi Raw).
- ⚠️ **Two exceptions, both informative.** Phi Fisher: 99.0% stable but held-out **0.5557** — stable and useless. Gemma Raw: **89.0%**, the only cell below 99%, held-out **0.5127** — unstable *and* useless.

**This is the empirical answer to a concern that was argued about all session.** The folding hazard is methodologically real; here it does not translate into an unstable sign.

## 4 — Error prediction: 🚨 published, then withdrawn the same day

Qwen3 was the only model clearing a 5% error bar, so the only candidate for asking whether the geometry predicts wrong *answers*. It reported Fisher at **0.8906** pooled and **0.8570** within the contradiction arm.

**Both are withdrawn.** Qwen3 is reasoning-tuned, and under the sealed `max_new_tokens`=14 budget it either leads with `Answer:` or opens a chain-of-thought preamble the budget truncates:

| first word | scored correct | scored error |
|---|---|---|
| `Answer:` | **484** | 1 |
| `Let's` | 0 | **68** |
| `Alright,` | 0 | **37** |
| `Okay,` | 0 | **10** |

**The outcome label is fixed by the first generated token in 599 of 600 cases — and `gen_step=1`, the position the geometry is measured at, IS that token.** An error-prediction AUROC on this label asks whether a hidden state predicts which token occupies its own position. Near-tautological, and not evidence about correctness.

🎯 **Consequence:** Qwen3's 19.3% is a rate of reasoning-preamble openings, not errors. **The construct gap covers the whole lineup, not five-sixths of it.**

🛡️ **Guard added.** The panel now computes outcome-label determinacy from the first token and prints `[!] TAUTOLOGY RISK` above any error-prediction figure above 95%. It fires on Qwen3 at **99.8%**.

## 5 — Residualizer CI: a prior objection closed empirically

The sealed analyzer fits OLS once and bootstraps the fixed residuals, so its intervals omit residualizer-fitting uncertainty. Refitting inside each resample:

| model | fixed-residual width | refit width |
|---|---|---|
| Llama | 0.0538 | 0.0570 |
| Mistral | 0.0520 | 0.0572 |
| Qwen 2.5 | 0.0872 | **0.0623** |
| Qwen3 | 0.0933 | 0.0992 |
| Phi | 0.0902 | **0.0715** |
| Gemma | 0.0768 | 0.0768 |

**Widths move in both directions, by at most 0.025, and no verdict changes** — Qwen 2.5's lower bound rises to 0.6163, still clearing 0.60. Reported as a closed objection rather than a discovered flaw.

## Scope

- 🔒 Moves no sealed verdict. E17b and E18 are defined on the pooled sealed cell.
- ➖ §5 uses run-02 (n=200), the only run carrying both geometries on identical rows.
- ➖ §1 and §4 concern outcome labels, not the geometry itself.

→ [[results/motif-audit-2026-09-10]] · [[results/orientation-artifact-audit-2026-09-10]] · [[log]] 2026-09-10 eighteenth and nineteenth entries
