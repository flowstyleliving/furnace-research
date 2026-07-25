# Condition Matrix v2 — multi-bundle twins study with held-out transfer

**Status:** directional design approved 2026-07-13; exact pilot/main integers and persona cards remain approval gates. Part of [[empathy-geometry/README|Empathy Geometry]]. Primary methodological companion: [[event-transfer-spec]].

## Core correction

E3 is **not** the sole confirmatory distribution. It remains the instrument-development anchor only. The twins study now spans three scenario bundles:

| Bundle | Event | Severity | Private pair | Role |
|---|---|---|---|---|
| B1 | E1 — seed packets | Tier 1 | [[personas-e1|Jules / Kai]], v1 | low-stakes ceiling and transfer bundle |
| B2 | E3 — midnight rewrite | Tier 2 | Mara / Theo, v1 | anchor bundle; harness and rubric development |
| B3 | E6 — house fund | Tier 3 | [[personas-e6|Talia / Warren]], v1 | high-stakes transfer bundle |

A **bundle** means shared event + its two private persona cards. Because E1/E3/E6 use different persona pairs, the primary endpoint is honestly named **leave-one-bundle-out (LOBO) transfer**, not pure event-text transfer. Passing it means the detector survives a new event/persona bundle on the same Qwen twins substrate. It does not yet mean cross-model or universal empathy detection.

## Fixed factors

| Factor | Frozen value for first study |
|---|---|
| Bundles | B1=E1, B2=E3, B3=E6 |
| Dyad | twins: Qwen2.5-7B × itself, separate contexts |
| Dyad model | `mlx-community/Qwen2.5-7B-Instruct-4bit` |
| Judge | `mlx-community/gemma-3-4b-it-4bit` |
| Arms | giraffe / neutral / jackal |
| Turns | 12 maximum, strict alternation (6 opportunities per agent) |
| Decoding | temperature 0.7, top-p 0.9, maximum 192 tokens; identical on both sides |
| Opening speaker | explicitly counterbalanced within every bundle × arm |
| Geometry | raw ACE at t=0; raw PRI/RPV/confidence at gen_step=1; no ANLI verdict |
| T4 on twins | sycophancy + empathy-authenticity residual; defensiveness unavailable on Qwen and marked missing, not zero |
| Primary transfer | train on two complete bundles, evaluate once on the untouched third; rotate all three holdouts |

Within each bundle, event and private personas are byte-identical across arms. Only the approved arm block changes.

Private-card token counts are reported and kept reasonably balanced within each pair after substantive red-line. Cross-bundle context lengths are not forced equal—the scenarios genuinely differ—but prompt/response/prior-turn token counts are mandatory T1 nuisance features in every transfer fold.

## Run matrix

| Stage | Bundles | Purpose | Dyads per bundle × arm | Total dialogues | Maximum turn rows | Claim status |
|---|---|---|---:|---:|---:|---|
| Phase-2 validation | E3 only | Prove interfaces/backends after rubric wiring | 2 | 6 | 72 | plumbing only |
| Phase-3A anchor gate | E3 only | Validate judge and ensure the field form is reachable | 6 proposed | 18 | 216 | instrument pilot |
| Phase-3B diversity gate | E1/E3/E6 | Estimate ceiling, label prevalence, and bundle heterogeneity | 6 proposed | 54 | 648 | multi-bundle pilot |
| Phase-4 main | E1/E3/E6 | LOBO detector transfer + behavioral endpoints | provisional floor 30 | 270 | 3,240 | preregistered only |

Every even `k` is split equally by opening speaker. The Phase-3B proposal uses three Mara/first-side and three partner/second-side openings per bundle × arm. Names differ by bundle; the role is counterbalanced, not the literal name.

### Why the main row is provisional

Turns inside one dialogue are correlated. The dialogue—not the turn—is the independent cluster. Phase 3 estimates:

- authenticity/performative-label prevalence;
- within-dialogue intraclass correlation;
- rates of `t_hear`, solution candidates, uptake, and censoring;
- between-bundle heterogeneity;
- usable rows after any preregistered ambiguous-label handling.

The proposed main floor is 30 dialogue clusters per bundle × arm, with at least 25 held-out dialogue clusters contributing evaluable rows to each detector class in every bundle. Increase n if that condition or the powered cluster calculation fails. Nested selection, OOB evaluation, and confidence intervals resample whole dialogues.

## Primary transfer rotation

| Fold | Training bundles | Untouched evaluation bundle | Hardest novelty |
|---|---|---|---|
| F1 | E3 + E6 | E1 | low-stakes/easy-resolution transfer |
| F2 | E1 + E6 | E3 | professional-partnership transfer |
| F3 | E1 + E3 | E6 | high-stakes family/money transfer |

All feature normalization, missing-value handling, baseline coefficients, geometry-cell/family selection, direction/sign, fusion weights, calibration thresholds, and hyperparameters are fit using the two training bundles only. The held-out bundle contributes prompts and unlabeled features at scoring time, but **no labels may influence any choice**. Full contract: [[event-transfer-spec]].

## Seed and opener schedule

- Use one ordered seed list crossed with all three bundles and all three arms.
- Phase-2 validation uses two fresh seeds on E3, one per opener.
- Phase-3A and Phase-3B use disjoint fresh seeds; the E3 rows in Phase-3B are new, not reused Phase-3A rows.
- Phase-4 uses a disjoint preregistered list; no seed used in validation, persona-vector extraction, or either pilot.
- Persist requested seed, actual opener, bundle id, event id, persona-card hashes, and arm hash.
- Never infer opener from seed or arm index during analysis.

## Controls

### Pseudo-dyads

Pair each agent trajectory with a trajectory from a different seed in the **same bundle, arm, turn count, and opener stratum**.

- deterministic derangement, no self-pairs;
- never pair the two sides of an original dialogue;
- preserve marginal text/geometry distributions and destroy contingent cross-agent coupling;
- one primary derangement per run; additional derangements are sensitivity analyses, not independent samples.

### Agent-vs-script

A live Qwen agent receives a frozen partner-turn sequence from a held-out donor bank under the same bundle/arm. The script never adapts.

- donor dialogues excluded from classifier fitting and evaluation;
- speaker role/opener counterbalanced;
- decoding applies only to the live side;
- primary comparison is coupling, not surface quality.

### Shuffled-label null

Shuffle at the dialogue-cluster level within bundle × arm strata. Never shuffle individual turns. Rerun the complete training-side selection procedure under shuffled labels; the holdout remains untouched.

## Analysis units

- **Behavioral ordering:** dialogue (`t_hear`, `t_sol`, censoring, demand bounce).
- **Turn authenticity detector:** turn rows with dialogue-grouped training and inference.
- **Transfer:** held-out scenario bundle; three equal-weight fold verdicts.
- **Dyadic coupling:** paired time series within dialogue; compare real vs pseudo vs script using dialogue summaries.
- **Opening speaker:** prespecified nuisance factor and interaction check.
- **Severity:** descriptive with only one bundle per tier; never claim an identified severity effect.

## Gate decisions

Proceed from Phase 3A to 3B only if:

1. Gemma-vs-expert agreement passes the [[judge-rubric]] validation gate;
2. E3 can produce both contact and performative/non-contact states without all arms resolving at ceiling;
3. raw two-locus geometry and twins T4=2/3 stamp correctly;
4. arm blocks are exact-token-matched and hash-frozen.

Proceed from Phase 3B to preregistration only if:

1. no bundle makes both neutral and jackal resolve at ceiling;
2. all three bundles yield both detector classes at usable prevalence;
3. `t_hear` and solution/uptake fields are judge-reachable in more than E3;
4. persona pairs pass the same CNVC and symmetry red-line as Mara/Theo;
5. the cluster-aware power calculation supports the final n.

If a bundle fails, revise or replace it before the registered seed—not after seeing detector performance.

## Decision status

- [x] E3-only confirmatory design rejected; E3 retained for instrument development.
- [x] Three-bundle twins design adopted in principle: E1/E3/E6.
- [x] LOBO rotation is the primary generalization test.
- [x] Twins T4 proceeds as 2/3; defensiveness enters later at the Llama rung.
- [x] E1 and E6 private persona pairs red-lined and approved (2026-07-13).
- [ ] Phase-3A/3B proposed `k=6` per bundle × arm approved.
- [ ] Temperature 0.7 / top-p 0.9 / 192-token maximum approved.
- [ ] Provisional main floor of 30 dialogue clusters per bundle × arm approved after pilot power review.
