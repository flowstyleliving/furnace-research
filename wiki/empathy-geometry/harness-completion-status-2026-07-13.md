# Harness completion status — 2026-07-13

**Status:** 11-item Codex source patch written; static diff audit clean. **Executor verification RUN 2026-07-13 → PARTIAL ACCEPTANCE:** geometry + provenance accepted (61/61 tests, gen-1 parity PASS, arm-token gate PASS, 72/72 clean rows); **the blinded judge's semantic call is a BLOCKER — it fails to parse in 66/72 turns, so the dependent-variable layer is effectively empty.** Phase 3 remains closed. See [[#Executor verdict — 2026-07-13 (run by Claude Code)]]. No project code run by Codex. Part of [[empathy-geometry/README|Empathy Geometry]]. Harness: `/Users/msrk/Documents/empathy-geometry-harness`.

## Outcome

The two items described in the older plan as missing are **already implemented** in harness commit `6873601`:

- raw t=0 ACE attention plus gen_step=1 surprise, p-max, PRI null-ratio, and RPV readout-spectrum statistics under backend `mlx-furnace-panel-raw`;
- a real transcript-only MLX judge backend (`mlx-blind-transcript-judge`).

Executor artifact `artifacts/real-validation-20260709/summary.json` reports six real MLX validation dialogues, `surrogate_geometry_only:false`, `real_t0_attention_ready:true`, `full_panel_geometry_ready:true`, and the MLX judge backend. That artifact used the Qwen same-family judge stand-in and predates the 2026-07-13 rubric, so it proves plumbing only—not judge validity or a result.

**2026-07-13 working-tree update:** Codex applied the full completion work-order after explicit user direction. The patch is not an acceptance artifact until an executor runs its tests and fresh validation.

- two blinded Gemma calls now separate semantic endpoints from authenticity;
- `t_hear` is harness-gated on feeling + need accuracy, judgment-free delivery, and tentative/correctable form;
- `solution_candidate(t)` and `uptake_of_prior_solution(t+1)` are separate; accepted/engaged uptake records `t_sol=t`, while final-turn candidates are right-censored;
- `run-real` defaults to and requires Gemma-3-4B unless an explicit stand-in override is supplied; `run-main` never permits the override;
- approved arm blocks, hashes, exact-token-count stamping, and a fail-closed `<=2` token-spread gate are installed;
- B1/E1, B2/E3, and B3/E6 now live in a hash-frozen bundle registry; the main path requires all three;
- PRI v3 fields now have an accurate `gen_step1.pri` namespace, with the old `rpv` location retained and marked deprecated;
- T4 readiness is rung-specific: twins require sycophancy + empathy-authenticity residual; defensiveness becomes required on the strangers rung;
- generated docs, README, handoff, summary reasons, and static regression tests were refreshed;
- a gen-step-1 parity-fixture comparator/schema was added, but a real canonical-vs-harness fixture must still be captured by an executor;
- LOBO fit/unseal entrypoints now enforce training-only transforms/selection, immutable held-out predictions, and hash verification before label unsealing.

## Static findings

### 🟢 Must-fix source changes — written, not yet executed

1. ✅ **Temporal split written:** pending proposals resolve only from the immediately following partner turn; proposal-turn attribution and final-turn censoring have regression tests.
2. ✅ **Rubric red-line written:** separate content/feeling/need fields, enforced feeling+need hearing gate, bundle annotation keys, and camera/each-party-needs/charge-free solution components.
3. ✅ **Judge gate written:** Gemma-3-4B is the default and required real judge; any non-Gemma validation requires an explicit stand-in flag and remains stamped.

### 🟢 Acceptance-stamping reconciliations written

4. ✅ Summary reasons now name the frozen rubric and still-open expert validation rather than stale user gates.
5. ✅ README, handoff, and generated docs now describe the live geometry and T4 surfaces.
6. ✅ PRI fields have an accurate namespace plus deprecated compatibility aliases.
7. ✅ T4 readiness reads the rung-level required-traits manifest.

### 🟢 Geometry implementation assessment

- D0 surprise is recomputed from the probability of the generated first token.
- D1 `p_t` is taken after appending that first token.
- `h_prev` and `h_t` feed the existing PRI machinery at the intended gen_step=1 locus.
- RPV uses the same top-k support-spectrum construction as the comprehensive Furnace path and stamps `support_k=512`.
- The backend explicitly states raw/not calibrated and does not reuse an ANLI ALLOW/BLOCK verdict.

This is sufficient for a parity test; it is not yet a parity proof against canonical Furnace rows.

## Patch work-order status

User directed implementation on 2026-07-13. Source status:

1. ✅ **Executor-verified 2026-07-13.** Approved strings/version/hashes/count stamping/fail-closed token gate written **and run**: `arm-token-counts` = giraffe 98 / neutral 98 / jackal 100 under `Qwen2.5-7B-Instruct-4bit`, spread **2**, `passes_within_two:true`. No inert-padding review needed, but the spread sits *exactly on* the `<=2` ceiling — any arm-block edit must re-run this gate.
2. ✅ Written.
3. ✅ Written.
4. ✅ Written.
5. ✅ Written (model-id hashes; executor artifact supplies the resolved runtime evidence).
6. ✅ Written.
7. ✅ Written.
8. ✅ Written.
9. ✅ **Executor-verified 2026-07-13.** Real fixture captured from a live MLX run (`tests/fixtures/gen1-parity.json`, schema `eg-gen1-parity/1.0`, 6 rows) and `check-gen1-parity` **passes** at `rtol=1e-5, atol=1e-7`. Three metrics (`shadow_logvol_r1_raw`, `fisher_eff_rank`, `spectral_entropy`) are genuinely **independent** reimplementation checks against canonical `comprehensive_run._support_spectrum` + `_spectrum_stats` on byte-identical inputs; `p_max` confirms the harness reads max(D1); `null_ratio_post_rank1` is a **same-implementation plumbing check only** (the harness calls the canonical `PRIComputer`) and is labelled as such in the fixture's `provenance` block — not oversold as independent. `surprise` was **removed from strict parity**: its canonical reference is the low-precision, saturating generation logprob, so a 1e-5 gate on a precise fp32 recompute was a false alarm (see below).
10. ✅ Written for complete B1/B2/B3 registry and main-path rejection.
11. ✅ Written as separate `lobo-fit` and hash-verified `lobo-unseal` entrypoints; runtime validation awaits executor and Phase-4 numerical freeze.

## Executor verification — not run by Codex

After patch review, an authorized executor should run the repository's tests and a tiny real validation—not a pilot—and provide artifacts showing:

```text
cd /Users/msrk/Documents/empathy-geometry-harness
/Users/msrk/Documents/t0-morphology-furnace/.venv/bin/python3 -m eg_harness arm-token-counts
/Users/msrk/Documents/t0-morphology-furnace/.venv/bin/python3 -m unittest discover -s tests
/Users/msrk/Documents/t0-morphology-furnace/.venv/bin/python3 -m eg_harness run-real \
  --provider mlx --judge mlx \
  --model mlx-community/Qwen2.5-7B-Instruct-4bit \
  --judge-model mlx-community/gemma-3-4b-it-4bit \
  --bundles B2 \
  --arms giraffe,neutral,jackal --dialogues 2 --turns 12 \
  --temperature 0.7 --max-tokens 192 \
  --out artifacts/real-validation-post-rubric-20260713
```

Acceptance evidence:

- arm token-count spread is `<=2`; if not, stop before tests/validation and return the counts for inert-padding review;
- six dialogues and 72 turn rows are present;
- no deterministic provider/judge rows;
- `surrogate_geometry_only:false` and raw two-locus metrics finite per turn;
- judge is Gemma-3-4B and `judge_model_stand_in:false`;
- solution candidates resolve only from the next turn's uptake;
- final-turn candidates are censored;
- prompt/rubric/arm hashes are present;
- T4 readiness follows the approved twins manifest;
- no arm-separation claim is made from the validation artifact.

All commands above are **not run by Codex**.

## Executor verdict — 2026-07-13 (run by Claude Code)

**PARTIAL ACCEPTANCE. Geometry and provenance accepted; the judge layer is REJECTED. Phase 3 stays closed.**

Preconditions all passed: unit tests **61/61**, `check-gen1-parity` **PASS**, arm-token gate **PASS (spread 2)**. The acceptance run completed as specified — `artifacts/real-validation-post-rubric-20260713/` — and every geometry/provenance item on the list above holds:

| Acceptance item | Verdict |
| --- | --- |
| six dialogues, 72 turn rows (24/arm, all B2/E3) | ✅ |
| no deterministic provider/judge rows | ✅ `mlx-local-generate` / `mlx-blind-two-call-judge`, 72/72 |
| `surrogate_geometry_only:false`, raw two-locus metrics finite per turn | ✅ 0 non-finite cells across 72 × 7; all 21 t=0 ACE cells present per row |
| judge is Gemma-3-4B, `judge_model_stand_in:false` | ✅ 72/72, non-family confirmed |
| judge blinding (`saw_geometry` / `saw_condition_label` / `saw_system_prompt` / `saw_checker_output`) | ✅ all false, 72/72 |
| solution candidates resolve only from the next turn's uptake; final-turn candidates censored | ✅ 0 violations — **but see caveat** |
| prompt/rubric/arm/event/persona hashes present | ✅ 72/72, single rubric sha |
| T4 readiness follows the approved twins manifest | ✅ required = sycophancy + empathy-authenticity residual, both present; defensiveness null by design |
| no arm-separation claim made from the artifact | ✅ stamped in summary notes |

The demoted surprise crosscheck also behaves as designed: 72/72 rows stamped, max `|delta|` **0.011**, **no `fail` status**; 56 rows correctly report `skipped_saturated_generation_reference` — the coarse-logprob saturation is now *named* rather than crashing the run.

### BLOCKER — the blinded judge's semantic call fails to parse in 66/72 rows (92%)

That call carries the whole dependent-variable layer: `reflection_*_accuracy`, `solution_candidate`, `solution_camera_test`, `solution_charge_free`, `uptake_of_prior_solution`, `need_match`, `feeling_match`, `hear_target`. Measured consequence across 72 turns: **1 solution candidate, 6 uptake rows.** The LOBO design is built on solution/uptake coding, so a pilot run today would produce a near-empty outcome variable. This also **voids the censoring/temporal check above as evidence** — it passes vacuously, on \~1 candidate, rather than by exercising the logic.

Root cause is **the rubric prompt, not the parser and not the token cap**:

- all 66 failures are **truncated** completions (no closing brace/fence); the parser's `first_object` fallback cannot rescue JSON with no end;
- in 27 of them the judge emits `solution_needs_addressed` as a dict keyed by *every CNVC need* (`"acceptance": null, "affection": null, "air": null, …`) instead of `{party: [needs]}`;
- **raising the cap does not fix it** — executor probe at `--judge-max-tokens 768` (`artifacts/_probe-judge-tokens-768/`) still failed **6/8**. The malformed shape is unbounded (\~100 keys), so completions grow \~750 → \~2,400 chars and truncate again at any budget. Every remaining failure is one of those rows.
- `eg_harness/judge.py:283` inlines the \~100-element closed needs vocabulary **immediately adjacent** to the object-shape instruction. The rubric text is correct; a 4B judge simply binds the nearest list as the key set.

**Fail-closed gap (the most serious finding).** Nothing caught this. `summary.json` reported `result_type: real_validation` with `partial_gen1_geometry_ready`, `real_t0_attention_ready`, and `t4_persona_projection_ready` all true, and no reason naming a dead judge. A run whose outcome variable is missing must say so in its own summary. Fix is specified as item 4 of the work-order below.

Codex work-order (authoring only, not run by Codex): `artifacts/CODEX_JUDGE_SEMANTIC_PARSE_WORKORDER.md` in the harness repo — fix the semantic prompt shape (without weakening the CNVC closed-vocabulary bar), raise the judge token default 256 → 512 (necessary, **not** sufficient), add an auditable truncation-repair parse attempt, and add a `judge_semantic_parse_rate` that **fails closed** below \~0.95.

**Next:** re-run the 72-row acceptance validation after the judge fix. The MK hand-label gate (\~20–40 turns) on the Gemma judge remains a separate, still-unopened Phase 3 precondition — and is now doubly warranted, since the judge's semantic endpoint has never once been observed working at scale.
