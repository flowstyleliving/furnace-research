# First clean judged validation — parse rate 1.0000 (2026-07-27)

**Status:** `[VALIDATION — plumbing accepted, not research-grade]`. Explicitly **no arm-separation or detector claim.** Part of [[empathy-geometry/build-plan|Phase 2]], candidate #11.

**Artifacts:** `empathy-geometry-harness/artifacts/real-validation-20260726b/` · harness `1a97537`.

## Result

| | 2026-07-13 | run 1 (07-26) | **run 2 (07-27)** |
|---|---:|---:|---:|
| semantic parse rate | 0.083 (6/72) | **0.0000** | **1.0000** ✅ |
| gate (fail-closed 0.95) | FAIL | FAIL | **PASS** |
| solution candidates | 1 | — | **27** |
| uptake rows | 6 | — | **61** |
| parse failures | 66 | 72 | **0** |
| `result_type` | degraded | `judge_degraded_validation` | `real_validation` |

**Spend: $4.47 of the $22 cap (20.3%).** 150 judge calls, 569,267 in / 64,958 out. 144 schema-valid on first attempt, 6 recovered by bounded retry.

The dependent-variable layer — empty since July — is now populated. The only remaining `research_grade` blocker is the expected one: **"Anthropic rubric labels require expert-anchor validation"**, which is MK's hand-labelling session, not a defect.

## Run 1 failed clean, and cost nothing

The first attempt produced **432 api_errors, parse rate 0.0000, and $0.00 spent** — every call rejected *before* inference. Two provider constraints, both in the request:

1. 🔧 The tool `input_schema` carried `minimum`/`maximum` on numeric properties. The tool-use compiler rejects these outright. Now stripped from the **wire** schema only, recursively and non-mutatingly; the canonical schema keeps them and the local validator still enforces the bounds on the value coming back. That is the better home anyway — a constraint the model was never shown is a post-condition, not a prompt.
2. 🌡️ **`temperature` is deprecated on the pinned judge.** Now omitted where unsupported, with `temperature_sent` stamped on every archived call.

Fixed and verified with **a single live call** before re-spending. The fail-closed parse-rate gate caught the failure but could not explain it — both faults were in what we *sent*, and nothing inspected the request.

## Temperature: measured, not assumed

The registration says the judge runs *at temperature 0*. Probing the live API:

| model | accepts `temperature: 0` |
|---|---|
| Opus 5 · Opus 4.8 · Opus 4.7 · Sonnet 5 | ❌ deprecated |
| Sonnet 4.6 · Haiku 4.5 | ✅ |

**The whole current frontier rejects it.** "Pick a model that supports temperature 0" means dropping to a materially weaker judge for a fine-discrimination coding task — trading the instrument for a parameter.

What temperature 0 was *for* survives without it. Five identical authenticity calls to `claude-opus-5`, no temperature:

| repeat | `authenticity_1_to_5` | `partner_specificity_0_to_2` |
|---|---:|---:|
| 1–5 | **2** | **1** |

**Scored fields identical on all five**; only the free-text `rationale` varied in wording, and the rationale is evidence for a reader, not an endpoint. ⚠️ Five repeats on one turn is not a stability claim — **Amendment A4 is drafted and names its own evidence gap**: k repeats across n real turns spanning all three arms, reporting the scored-field disagreement rate. Uninitialed.

A correction worth recording: the first version of `TEMPERATURE_UNSUPPORTED_MODELS` listed Opus 5 alone and a test asserted Opus 4.8 *accepts* temperature. Both were written from assumption and both were false. Corrected from measurement.

## The gate still has no producer — now confirmed empirically

The judge emits `feeling_match`, `need_match`, `reflection_accuracy`, `hear_target`, `solution_candidate`, `uptake_of_prior_solution` … and **not `need_met`**. That field is the first-person endpoint introduced by deliverable B's schema, whose per-POV prompt bodies are parked as a `[USER GATE]`.

So the flattery gate's row contract genuinely has no producer — the reviewer's blocker, now confirmed against a real 72-row run rather than by grep.

## Backlinks

[[empathy-geometry/build-plan]] · [[results/eg-flattery-gate-2026-07-26]] · [[results/eg-standalone-panels-2026-07-26]] · [[log]] 2026-07-27
