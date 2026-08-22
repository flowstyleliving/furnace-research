# The [R4] naming diagnostic — built, adversarially reviewed, and one retraction (2026-07-26)

**Status:** `[DESIGN + INSTRUMENT]` — a pre-run instrument with its pre-registration amendment. **No data exists**; nothing here is a result about empathy geometry. Part of [[empathy-geometry/build-plan|Phase 2]], candidate #11.

**Repo:** `/Users/msrk/Documents/empathy-geometry-harness`, commits `3810ea1` (implementation) + `26362aa` (spec tracking + Amendment A1).

## What the gate is for

The hosted judge reports whether a reflection landed (`need_met`). That is the first-person endpoint, so **a judge that simply agreed with the giraffe arm would manufacture the study's headline result.** The diagnostic makes that failure visible: whenever the judge claims a landing it must also name *what* landed, and that naming must beat chance.

## The chain of reasoning, including where it went wrong

This entry exists mostly because the reasoning **inverted twice**, and both inversions are worth keeping.

### 1️⃣ The original design

Pre-registration `[R4]` defined chance by permuting **which persona's `heard_needs` counts as the target**, 1000×, floor = 95th percentile.

### 2️⃣ My claim that this was fatally broken — WRONG

Each bundle holds exactly two personas with **disjoint** need sets (verified: all 12 cross-persona combinations miss). So swapping drives a swapped dialogue's contribution to zero, making the permuted accuracy `A × (fraction unswapped)` and the floor ≈ `0.83·A` at six dialogues, `0.63·A` at thirty. A trigger of `A ≤ floor` is then unsatisfiable for any `A > 0` — a bar that scales with the thing it measures.

I reported this as a BLOCKER and advised **do not freeze R4**.

### 3️⃣ Why that was wrong

Simulation across naming-informativeness 0.0→1.0 showed **both nulls reach identical verdicts** (both flag at ≤0.2, both clear at ≥0.4).

The premise `floor = A × f` holds only for a judge whose naming is *already chair-informative* — **that is the alternative, not the null.** For a judge whose naming is independent of the chair, swapping the target changes the score not at all in expectation, the floor rises to meet the accuracy, and the gate fires exactly as intended.

> **The error: adopting a floor formula derived under H1 as though it described the null distribution.** A permutation floor is a statement about behaviour under H0.

Codex sharpened this further: examining the permutation distribution on alternative-like data is precisely how one evaluates *power*; the defective step was concluding unsatisfiability from a premise that only holds under H1.

### 4️⃣ What was actually built

MK directed the switch to shuffling the **judge's answers**, which was implemented — but on its true merits, not as a repair:

- 🎯 **Resolution** — multiset orderings rather than only `2**n_dialogues` arrangements (256 at eight dialogues).
- 🗣️ **Marginals** — holds each dialogue's naming vocabulary fixed, so the comparison is against a judge with the same tics. A judge emitting one constant need scores identically under every permutation.
- 🔁 **The target-swap null is retained** as a pre-registered sensitivity analysis under its own seed, with `nulls_disagree` reported. Not discarded — the degeneracy claim is retracted, not acted on.

## Adversarial review: 3.5/10 → rebuilt

Codex `gpt-5.6-sol` scored the first implementation **3.5/10** and was right to. The findings that mattered:

| Severity | Defect | Fix |
|---|---|---|
| 🔴 CRITICAL | `acceptance_grade = not underpowered` — **a cell with confirmed flattery was still acceptance-grade** | requires evaluable **and** unsuspected **and** free of condition-dependent missingness |
| 🔴 CRITICAL | Code diverged from the frozen pre-registration | **Amendment A1** written pre-run |
| 🔴 CRITICAL | Nothing called the gate — it could block nothing | `eg-harness flattery-gate`, exits non-zero on a blocked cell |
| 🟠 HIGH | Degeneracy inferred from whether *labels* differed | counted from **distinct achieved permutation scores** |
| 🟠 HIGH | Zero landing claims **raised** instead of stamping underpowered | preflight before any statistic |
| 🟠 HIGH | Conditioning on the judge's own `met` claim is selection on the dependent variable | reframed as a **consistency diagnostic, not an independent validation** |
| 🟡 MED | Suspicion forced `False` when unevaluable | **tri-state** — `None` means unevaluable, which is not "unsuspected" |
| 🟡 MED | A "flattering" fixture drawn at random is seed-fragile (a 95th-percentile null rejects \~5% of true H0 samples by construction) | four **deterministic** fixtures |

The label-based degeneracy check caught **one of my own test fixtures** once replaced by the score-based one: a "varied" judge whose names all belonged to one persona is score-invariant under permutation. The check working on its author is the useful kind of evidence.

## Verified by running it

`eg-harness flattery-gate` against the **real B2 personas**, not test doubles:

| judge | naming accuracy | floor (primary / sensitivity) | verdict | exit |
|---|---:|---:|---|---:|
| names the chair's own need | 1.000 | 0.667 / 0.800 | accepted | **0** |
| names the other persona's need | 0.000 | 0.667 / 0.800 | **flattery suspected, blocked** | **1** |

Both nulls agree (`nulls_disagree: false`); null non-degenerate (10 distinct permuted scores). Suite **152 passed, 11 subtests**.

## A second integrity gap, found while committing

**`artifacts/` was gitignored wholesale — so the pre-registration document was not under version control.** An unversioned pre-registration can be edited without trace, which is the one property a pre-registration exists to provide. Fixed: `artifacts/*` + `!artifacts/*.md` tracks specs while run outputs stay ignored. (The pattern matters — `artifacts/` excludes the *directory*, and git does not descend into an excluded directory, so a negation beneath it is never consulted.)

## 💭 Feelings get their own section (Amendment A2, same day)

MK: *"I don't want it to be completely moot — just have it be a different section."*

[R2]'s refusal to ground-truth feelings **stands**, and for good reasons: no frozen per-persona target-feeling set exists, inventing one after transcripts exist would be writing the answer key after the test, and NVC holds that many feelings can faithfully express one unmet-need state. But that rules out scoring a feeling against a *persona-specific* target — it does not require the field to be inert.

What **can** be scored without an answer key is **purity**, against two inventories frozen before any run (`spec.FEELINGS`, 254 entries; `spec.FAUX_FEELINGS`). A faux-feeling is an evaluation of the other party wearing a feeling's grammar — "dismissed", "ignored" — which NVC treats as a judgement rather than an emotion.

Every run reports purity, faux-feeling rate, unrecognised rate, declined-to-name count, distribution, and examples. **It gates nothing** — a test replaces every feeling in a cell with a faux-feeling and asserts the verdict is unchanged, so the separation is enforced rather than merely intended.

### A2.1 — a silent field must not read as a perfect one

MK caught the residue of this immediately, and it was a real defect. A2's first form divided purity by the feelings *actually named*, so:

> a judge naming **one** feeling across **thirty** landing claims scored **purity 1.000**.

Silence presenting as perfection — and the more silent the judge, the more confident the number. The `None`-on-empty guard only covered *total* silence; near-silence was worse, because it produced a figure that looked earned.

Fixed by reporting **two named denominators and no bare `purity` key to grab by accident**:

| named / claims | status | coverage | `purity_of_named` | `purity_over_claims` |
|---:|---|---:|---:|---:|
| 30/30 | scored | 1.000 | 1.000 | 1.000 |
| 15/30 | scored | 0.500 | 1.000 | 0.500 |
| 5/30 | **sparse** | 0.167 | 1.000 | 0.167 |
| 1/30 | **sparse** | 0.033 | 1.000 | **0.033** |
| 0/30 | **silent** | 0.000 | `None` | 0.000 |

`purity_of_named` still honestly reports 1.000 in the sparse rows — *of the feelings offered, all were pure*. That figure is not wrong, which is exactly why it must never be the only one on the page. `coverage` and `status` (`spec.FEELING_COVERAGE_MIN = 0.5`) make the regime explicit rather than inferable.

Fixing this also exposed a test helper that silently truncated any fixture longer than six rows — a thirty-item list had been scored as six.

## Re-review: 5.5/10 — and the retraction on this page was itself too strong

A second adversarial review (fresh reviewer; the earlier relay had bounced three times) scored the rebuilt module **5.5/10 — does not clear 8.5.** Three BLOCKERs, all reproduced by me before acceptance rather than taken on report.

### 🔴 The worst one is on this page

The retraction recorded above asserted, unconditionally, that under H0 swapping the target *"changes the score not at all in expectation"* — and cited a simulation across informativeness 0.0→1.0 in which both nulls agreed on every verdict.

**Both statements were too strong, and the simulation was never committed.** Frozen text was carrying an empirical claim with no artifact behind it.

The expectation argument holds **only when chair composition among the `met` rows is balanced within a dialogue.** That does not follow from H0 — selection into `met` is the judge's *own* and may itself be chair-dependent, and one-sided naming is the canonical flattery mode, not an exotic case. My simulation used a balanced fixture and I stated its result as general.

**Counterexample, reproduced exactly:** a chair-**blind** judge (H0 exactly true) naming one persona's need on every row, with 80% of `met` rows belonging to that persona —

| | |
|---|---:|
| accuracy | 0.800 |
| answer-shuffle floor | 0.800 → **fires** ✅ |
| target-swap floor | 0.650 → **does not fire** ❌ |

So under chair imbalance the target-swap null is **anti-conservative and can miss a fully chair-blind judge.** That is a *better* reason to keep the answer shuffle primary than the resolution argument — and it reclassifies the sensitivity null as a second opinion **with a documented blind spot**, not one of equal standing. Now pinned as a regression test that fails if the blind spot ever closes. Amendments **A1.1** and **A3** filed.

### 🔴 The other two blockers — confirmed, PARKED

- **The gate does not gate.** `runner.py:413` computes its *own* `acceptance_grade` from geometry/hash flags, with the flattery gate nowhere in it. Two identically-named fields with opposite coverage; the one a reader finds in the artifact says `true` while the gate has never run. Worse: **nothing in the repo produces the rows the gate consumes** — `need_met`/`chair` appear only in `flattery.py` and tests. So the gate reads a contract no producer implements.
- **The degeneracy fix is insufficient, not merely incomplete.** Degeneracy is per-*cell* but permutability is per-*dialogue*: a dialogue whose `met` rows share one chair is score-invariant however many distinct names it holds. A constructed cell reached `acceptance_grade: true` on **10 informative rows out of 80**, with 6 distinct permutation scores and no flag.

Both are real, both need design decisions (a manifest contract; counting the 20-row floor on *informative* rows plus a per-cell oracle power check), and both are parked for MK rather than patched at speed.

### ✅ Fixed immediately

`unittest.main()` sat mid-file, so direct invocation ran **39 of 49** tests and reported OK — the ten newest feelings tests vanished silently. Moved to the end. And `nulls_disagree` is now tri-state, since `False` with no second null asserts agreement about a comparison that never happened.

## Standing scope limits

🚫 Naming is conditioned on the judge's own `met` claim, so the same judge controls both selection and the scored name. **Consistency diagnostic, not endpoint validation** — instrument validity rests on the human-anchor gate.

🚫 The answer-shuffle null needs a **stronger assumption** than the target swap: names exchangeable across rows given the dialogue and given selection into `met`. Naming that tracks turn position rather than chair would violate it. Stated in the docstring and Amendment A1 rather than assumed.

⚠️ **Expect the gate to be underpowered at pilot scale.** It needs ≥20 `met` rows in the giraffe arm; at k=6 dialogues that is unlikely, so the lie detector cannot be validated until the main run.

## Open

- **R2 and R3 remain uninitialed** ⟨MK⟩. R1 is closed (primary judge = `claude-opus-5`).
- Whether the gate should also block inside a report/aggregation path — that path does not exist yet (deliverable B).
- Hosted judging is blocked on **API credits**, not credentials.

## Backlinks

- [[empathy-geometry/build-plan]] · [[results/eg-standalone-panels-2026-07-26]] · [[log]] 2026-07-26
