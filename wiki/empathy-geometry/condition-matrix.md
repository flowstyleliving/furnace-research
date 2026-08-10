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
| Opening speaker | **fixed: the receiving party opens** (`speakers[1]`), every bundle × arm — see [[#Opening speaker fixed to the receiving party 2026-08-10]] |
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

🗄️ **HISTORICAL — SUPERSEDED 2026-08-10.** ~~Every even `k` is split equally by opening speaker. The Phase-3B proposal uses three Mara/first-side and three partner/second-side openings per bundle × arm. Names differ by bundle; the role is counterbalanced, not the literal name.~~ The opener is no longer a counterbalanced factor; the receiving party opens in every dialogue. See the section below.

## Opening speaker fixed to the receiving party (2026-08-10)

**MK decision, implemented in `runner._opening_speaker`.** Every event in the bank has one party who acts and one who discovers it:

| bundle | acts (`speakers[0]`) | receives / discovers (`speakers[1]`) |
|---|---|---|
| B1 / E1 | J discards the seed packets | **K** finds them gone |
| B2 / E3 | M rewrites and submits | **T** sees it at 7:30 the next morning |
| B3 / E6 | T moves the $1,400 | **W** is told the following day |

The receiver always opens. Rationale:

1. **The two levels were never exchangeable.** Counterbalancing assumes its levels are interchangeable variants of one nuisance factor. Here only the receiver has a trigger — the event hands the actor no new information at the moment the conversation starts, so an actor-opens dialogue begins with an unprompted self-justification. That is a different conversation, not the same one from the other side.
2. **n is the binding constraint.** Splitting a small corpus across the two spends half of it on the incoherent premise.
3. **It removes an arm↔opener coupling.** The previous implementation was `speakers[(seed + arms.index(arm)) % 2]`. Because giraffe and jackal sit at arm indices 0 and 2, they drew the same opener at every seed while neutral always drew the other — measured directly at seed 0: giraffe→Mara, neutral→Theo, jackal→Mara. Marginally balanced over an even number of seeds, but correlated with arm within each one, against the spirit of the "never infer opener from seed or arm index" rule below. A constant cannot correlate with anything.

**What this costs:** the opener interaction check in the analysis plan (below) no longer has two levels to compare, and the actor-opens conversation is never observed. Both were judged worth less than half the corpus.

**Timing:** landed while the LOBO preregistration is unfrozen and no anchor labels exist, so the change is free. Like the `ARM_BLOCKS` sequencing constraint in [[build-plan]], it would have been expensive immediately after the anchor pass.

`opening_speaker=` remains an explicit per-run override, used by the human-in-the-loop `converse` path and by any future counterbalance study.

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
- Phase-2 validation uses two fresh seeds on E3. (🗄️ ~~one per opener~~ — retired 2026-08-10; there is one opener.)
- Phase-3A and Phase-3B use disjoint fresh seeds; the E3 rows in Phase-3B are new, not reused Phase-3A rows.
- Phase-4 uses a disjoint preregistered list; no seed used in validation, persona-vector extraction, or either pilot.
- Persist requested seed, actual opener, bundle id, event id, persona-card hashes, and arm hash.
- Never infer opener from seed or arm index during analysis. Since 2026-08-10 the opener is also not *assigned* from seed or arm index — it is the registered receiver — so the persisted value should be asserted constant rather than reconstructed.

## Controls

### Pseudo-dyads

Pair each agent trajectory with a trajectory from a different seed in the **same bundle, arm, and turn count**. (The opener stratum is no longer a distinguishing factor — since 2026-08-10 the receiver opens in every dialogue, so all trajectories share one stratum.)

- deterministic derangement, no self-pairs;
- never pair the two sides of an original dialogue;
- preserve marginal text/geometry distributions and destroy contingent cross-agent coupling;
- one primary derangement per run; additional derangements are sensitivity analyses, not independent samples.

### Agent-vs-script

A live Qwen agent receives a frozen partner-turn sequence from a held-out donor bank under the same bundle/arm. The script never adapts.

- donor dialogues excluded from classifier fitting and evaluation;
- speaker role counterbalanced (the opener is fixed to the receiver, so donor and live sides differ by role, not by who started);
- decoding applies only to the live side;
- primary comparison is coupling, not surface quality.

### Shuffled-label null

Shuffle at the dialogue-cluster level within bundle × arm strata. Never shuffle individual turns. Rerun the complete training-side selection procedure under shuffled labels; the holdout remains untouched.

## Analysis units

- **Behavioral ordering:** dialogue (`t_hear`, `t_sol`, censoring, demand bounce).
- **Turn authenticity detector:** turn rows with dialogue-grouped training and inference.
- **Transfer:** held-out scenario bundle; three equal-weight fold verdicts.
- **Dyadic coupling:** paired time series within dialogue; compare real vs pseudo vs script using dialogue summaries.
- **Opening speaker:** 🗄️ ~~prespecified nuisance factor and interaction check~~ — **retired 2026-08-10**, the opener is now constant (receiver opens), so there is no second level to interact with. The realised opener is still persisted per dialogue and should be asserted constant, not modelled.
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
