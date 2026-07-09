---
status: OPEN
kind: post-hoc-sensitivity
date: 2026-05-18
---

# Step-0 t=0 Answer-Recoverability Audit `[OPEN — sensitivity only]`

Post-hoc sensitivity analysis on the **locked** [[step0-belief-readout-2026-05-17]] panel. **Does not amend, re-score, or reinterpret the pre-registered result** ([[step0-belief-readout-prereg-2026-05-17]]). It answers the one question pre-reg point #2 left open: *when the literal `YES/NO` buckets didn't carry the t=0 mass, did it go to an answer-like non-literal form (`Correct`/`True`/`Right`/`False`…), or to non-answer continuation tokens?*

## Why a new forward pass was needed

The locked scored CSVs persist only `top1_*`, not full top-k for all 200 rows (the canary keeps top-10 for just 3 samples). So this is a fresh forward pass on the **same frozen `n=200 × 10` slice** with the **same frozen per-model specs** — the frozen `semantic_*` shortlist is reused verbatim as the answer-alternative list, never re-fit. Locked artifacts in `run-02` were read read-only; all output lives in a separate audit dir.

**Integrity gate (the license to reinterpret):** before any reinterpretation, the audit recomputes every locked `p_yes / p_no / lean` and the frozen canary top-10 and aborts on drift beyond fp tol. **All 10 models: max |Δ| = exactly 0.0** vs both the locked CSV and the frozen canary. The forward pass is byte-faithful; this is a valid reinterpretation of the locked slice, not a different measurement.

## Result — the literal-only panel was *not* understating answer recoverability

Across **all 10 models** (n=200 each):

- `semantic_above_floor_coverage` == `literal_above_floor_coverage` to 4 dp — the frozen synonym shortlist **never flips a single row's eligibility**.
- `recovered_only_by_semantic` = **0.000** everywhere; `frac_top1_answerlike_nonliteral` = **0.000** everywhere.
- `mean_semantic_decidedness − mean_literal_decidedness ≈ 1e-5` (e.g. Qwen2.5 0.428424 vs 0.428416). Off-literal answer-word mass is negligible.

Every model buckets as **literal-panel-basically-complete**. The locked verdict shape — Recoverable-for-M 9/10, Phi-3.5-mini Low-decidedness-for-M — **stands and is not an artifact of literal-only buckets.**

## The real story is continuation, not disguised answers (confirms the t=0 caveat)

`frac_top1_nonliteral` is high on some models, but the non-literal top-1 is *scaffolding*, not a hidden answer:

| Model | frac_top1_nonliteral | dominant non-literal top-1 | class | literal mass underneath |
|---|---|---|---|---|
| Qwen2.5-7B | 0.585 | `" To"` (117/200) | other (continuation) | median lit-decidedness 0.188; **still above floor 113/117** |
| Mistral-7B-v0.3 | 0.535 | `"Y"` (107/200) | other (bare-letter onset) | median 0.050; **still above floor 106/107** |
| Phi-3.5-mini | 0.195 | `"\n"` (38/200) | control | 0/39 above floor — the genuine low-decidedness rows, correctly floored |

This is exactly the original caveat: *what it emitted* (a reasoning preamble like "To determine…") ≠ *what the logits looked like* (literal `YES/NO` mass surviving underneath, above the frozen floor). The literal partition captured it correctly; the floor logic correctly excludes Phi-3.5's newline-dominated low-decidedness rows.

## One narrow caveat worth a future probe (not a falsification)

**Mistral-7B's** dominant non-literal top-1 is the bare letter **`"Y"`** (107/200) — an answer *onset* that is outside *both* the literal `YES/NO` bucket *and* the frozen word-level `semantic` shortlist. It does not change the locked verdict (literal mass clears the floor in 106/107; Mistral-7B stays Recoverable-for-M). But it localizes where a future sensitivity probe could move: **a single-letter `Y`/`N` partition for Mistral-7B specifically — not more synonyms**, which the audit shows add nothing on any model.

## Verdict

The pre-registered literal-only panel was **basically complete** for answer-*word* recoverability. The sensitivity analysis tightens, and does not weaken, the locked [[step0-belief-readout-2026-05-17]] interpretation. `[OPEN]` — descriptive sensitivity only; pre-reg unchanged; audit operating point logged before any neighborhood claim.

## Artifacts (repo)

- `experiments/v4-mech-prep/2026-05-17/audit-t0-recoverability/` — per-model `*_t0_audit.{csv,json}` + `t0_audit_panel_summary.csv` + per-model gate logs
- `scripts/audit_t0_recoverability.py` (read-only, reuses locked `step0_belief_readout` scoring math) + `scripts/run_t0_recoverability_audit.sh`

## Propagates to / read alongside

- [[step0-belief-readout-2026-05-17]] — the locked panel this audits (unchanged)
- [[step0-belief-readout-prereg-2026-05-17]] — pre-reg point #2 is the question answered here
- [[claims]] — folds under the existing `[OPEN]` step-0 entry as a sensitivity rider, not a new claim
