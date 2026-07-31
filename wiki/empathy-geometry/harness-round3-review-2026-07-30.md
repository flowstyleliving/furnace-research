# Harness round-3 build and review — 2026-07-30

**Status:** Round-3 work order ([[workorders/eg-round3-degeneration-workorder-2026-07-30]]) implemented by a fresh Opus 5 agent; **293 → 336 tests green, nothing committed, `ARM_BLOCKS` byte-identical, sealed t0 untouched.** Codex static review returned **FAIL — one blocker (two branches), one major, three minors.** The blocker is in **new, uncommitted code that was never used to generate or label a production corpus** — it has been exercised only by tests and by diagnostic probes passing archived rows through it — so no anchor output is contaminated and no cleanup is owed. Round 2's blocker (label cap applied to the aggregate tag run) is confirmed closed. Part of [[empathy-geometry/README|Empathy Geometry]]. Harness: `/Users/msrk/Documents/empathy-geometry-harness`, branch `fix/content-token-alignment`, HEAD `7093f62` with all work in the working tree.

## What the round covered

Per the work order: the round-2 cap-bypass blocker; `DEFAULT_TURNS` 12 → 6; a read-only, non-aborting degeneration detector storing continuous similarity ratios; and six Codex round-2 majors (RNG seeding, provenance at analysis boundaries, review stimulus snapshot, rubric text binding, quarantine artifact, taint-guard window). Section 6 — prompt-shape purification and arm-block exits — was left strictly untouched pending MK.

## Verified by execution, not relayed

Claude Code re-derived every load-bearing claim rather than accepting the builder's report:

- **Cap bypass closed.** `"Sam: "×14`, `×30`, and `"The person in front of you: "×3` all previously MISSED, all now CAUGHT. `×8` and the single case unchanged.
- **No false abort** on `"I hear you. Here's the thing: I am tired."` or `"9:15pm was late."`; `Mara:`, `sam:`, `María:`, `The person in front of you:` all still caught.
- **`ARM_BLOCKS` byte-identical**, SHA-256 compared between `HEAD:eg_harness/spec.py` and the worktree; the `spec.py` diff is scoped to `DEFAULT_TURNS` plus the two new degeneration constants.
- **Streaming/final alignment prefix invariant holds.** 4,429 constructed outputs covering repeated tag runs, mixed honorific labels, tabs, leading newlines, Unicode names, 8-vs-9-word labels and the 63/64/65/70-char bound boundary; **all 609,535 prefixes checked, zero divergences.** This is the item the builder had evidenced only by randomized sweep, and it is the one Codex structurally cannot test.
- **336 passed, 1102 subtests**; nothing staged; HEAD unmoved.

## BLOCKER — the review stimulus gate (both branches)

This gate exists to stop the review GUI showing MK persona text the model never read. It is the guard on the human anchor pass, which is the study's ground truth.

**Branch 1 — `review.py:282`, early return at `:295`.** The loop walks `_STIMULUS_DIGEST_CHECKS` and `return`s after the *first* digest the row happens to carry. The four checks are not four fingerprints of one object; their coverage is partly nested and partly disjoint — `stimulus_sha256` hashes the complete canonical registered stimulus; `persona_sha256` is **a mapping of per-speaker, profile-only hashes**, not a single digest; `event_sha256` hashes only the event text; `bundle_sha256` hashes a payload that transitively includes the complete canonical stimulus, including `heard_needs` and `heard_condition`. Event and profile coverage are disjoint. So verifying one is treated as verifying the whole.

Demonstrated: a row carrying only `event_sha256` **passes** and renders live-registry text. That digest is not hypothetical — **B1 and B3's event text was byte-unchanged across v1→v2** (both already used letter handles), so `event_sha256` truthfully reports "unchanged" while every persona was rewritten. Codex's variant is sharper: a row whose `persona_sha256` matches but whose `event_sha256` and `bundle_sha256` are stale passes on the persona alone, because persona sits above event in the tuple.

The archived corpora exercised here are refused only by coincidence — every row carries `persona_sha256`, that digest moved, and persona precedes event in the tuple. That is not universal across `artifacts/*/turns.jsonl`: eight turn files carry persona/event/bundle digests on every row while nine carry none (and are refused for missing provenance instead). `real-validation-20260729` and `real-validation-post-rubric-20260713` carry persona, event and bundle digests on all 72 rows but no `stimulus_sha256` and no snapshot.

**Branch 2 — `review.py:314`.** A row carrying a `dialogue_stimulus` snapshot returns it immediately and is **never checked against any recorded digest**. Demonstrated by passing a fabricated snapshot with all four recorded digests zeroed; it rendered `'FABRICATED EVENT THE MODEL NEVER SAW.'` straight through.

Codex found the case already in the tree: **`tests/test_review.py:522`** attaches today's B2 snapshot onto rows of the archived v1 run in order to keep blinding coverage against real utterances. The intent is sound and its sibling test asserts the same corpus is refused *without* a snapshot — but it is the corruption pattern, standing as a fixture. (Uncommitted, like everything in rounds 1–3.)

**Fix:** check every digest the row records rather than the first; require at least one present; fail on any mismatch. Validate a supplied snapshot by recomputing its own digest against the row's recorded `stimulus_sha256`.

## MAJOR — the label guard's stated coverage is false

The construction comment immediately above the label regex claims it catches a turn-initial label of "ANY shape" (the `leading_speaker_tag()` docstring itself makes no such claim). Measured: `Mx. Sam:`, `Dr. J. Sam:`, `Sam Jr.:` and `J. Sam:` all **MISSED**; `Dr. Sam:` and `Sam:` caught. Only `J. Sam:` was disclosed. These forms were not observed in the archived sample, so **their model incidence is unmeasured** — crafted examples establish regex coverage, not confabulation probability. The defect that matters is not any single missing form but that a fail-closed guard overstating its coverage is one that stops being audited.

## MINORS

- **False-abort class, weightier than "minor."** The guard terminates the whole run on any turn-initial `Words:`. Measured aborts on authentic prose: `"St. Louis felt like the clearest comparison: I felt small."`, `"Gen. anxiety is what I keep coming back to: it never lifts."`, `"Fr. my side it looked different: you left."` — and, not honorific-dependent at all, `"Miss this point: I am not refusing you."` The same shape would abort `"Look: I was scared."` This is **inherent to the design**, not introduced by the honorific narrowing (Codex confirms narrowing periods cannot add matches). The builder's stated trade — "a false abort is recoverable, a missed tag silently contaminates" — holds only while someone is watching; in a 144-call paid run an abort at turn 5 of 6 loses the dialogue. **Open MK decision, not an engineering fix.**
- `turn_repetition()` is not strictly total: `threshold=10**10000` raises `OverflowError`; an object whose `__str__` raises escapes. All ordinary malformed shapes produce the expected row.
- Quarantine filenames can collide on identical payloads within the same microsecond, and `write_text()` overwrites. Practical risk low.

## No finding

- `quarantine_turn()` fails safely. All four abort callers still raise their intended diagnostic and embed an explicit `<quarantine write failed: …>` sentinel.
- A legitimate first run cannot trip the uniformly-missing provenance check; bundle hashes and version are attached before `write_run()`.
- `judge.py` relocation is genuinely byte-identical to HEAD, and `SCORING_INSTRUCTIONS` is bound into `RUBRIC_SHA256` before hashing.

## Correction carried in from the same day

The work order's original motivation — a **34×** `surprise_gen1` gap between fresh and degenerate turns — is **confounded and withdrawn**. 17 of 19 saturated turns carry `content_token_offset > 0`; they are self-tag artifacts. (`content_token_offset > 0` is a sound self-tag marker in this artifact: all 41 such rows also carry `leading_self_tag_stripped: true`, and all 31 offset-0 rows carry `false`.)

Stratified, with cohorts named explicitly. Of 72 corpus rows, **60 have a prior same-speaker turn** and so admit a similarity comparison; the other 12 are each speaker's first turn in each of the six dialogues.

| cohort | fresh | degenerate | ratio |
|---|---|---|---|
| offset = 0 | n=19 | n=5 | **1.9×** |
| offset > 0 (self-tagged) | n=32 | n=4 | 11.2× |
| uncontrolled | n=51 | n=9 | 34× |

Among non-degenerate turns alone, the self-tag comparison is offset-0 n=19 versus offset>0 n=32 — **12.6×**. Exactly one saturated turn is repetition with no self-tag present.

Degeneration survives as an unambiguous *text-quality* defect — **9 of 72 corpus rows, or 9 of the 60 turns with a defined same-speaker comparison**, are ≥0.70 self-similar; two are verbatim; all sit at `turn_index ≥ 8`. The detector's role becomes **sizing an unmeasured residual** rather than fixing a known contamination.

**Weight this lightly.** The corpus is six dialogues, **two per arm**, and the clean-cohort estimate rests on five degenerate turns. Turns are nested observations within dialogues, not 72 independent samples. Detail in [[workorders/eg-round3-degeneration-workorder-2026-07-30]] §3–§4 and the 2026-07-30 log entries.

## Builder flags worth keeping

1. **`embedded_turn_label()` never had the round-2 blocker.** Its pattern has no `+`, so repetition cannot fold into one match. The work order was wrong to assume it did; the builder measured before changing.
2. **The "minor" period fix was more dangerous than the blocker it sat beside.** Before it, the unrestricted `.` meant `"That lands. What I need is simple: rest."` was CAUGHT — the guard would have aborted paid runs on authentic output. The blocker admits bad data; this destroyed good runs.
3. **The honorific change introduced, and then caught, a streaming/final alignment drift** — `"Dr."` matched the label pattern but not the partial pattern, so streaming would resolve offset 0 and the final pass abort. The work order's own warning is what prompted the test.
4. **The degeneration metric is load-bearing and was unnamed.** All figures depend on difflib's default `autojunk=True`; under `autojunk=False` the corpus flags 14 turns with three below index 8. Those additions are *worse* discriminators (median surprise 0.1186 vs 0.0087), so the registered variant is retained and stamped as `DEGENERATION_METRIC`.

## The recurring class

Both blocker branches share a **fail-open validation pattern**: a check that can succeed on partial evidence while emitting the same "verified" signal it would emit on complete evidence. Two **round-1** defects in this repo have the same shape — the manifest checked provenance *presence, not consistency*, and the bundle hash omitted `heard_condition`/`heard_needs` so those rewrites were not provenance-bound at all. (Two round-1 incidents, not one per round.)

Two incidents outside this repo *resemble* the pattern: the 2026-06-23 "32B nf4 that was actually bf16" catch (unstamped runs, surfaced by an unrelated byte-identity check) and, at the methodology level, the KV-tension verdict that flipped 2/5 versus 0/5 on identical numbers because the pre-registration never enumerated its comparator cells. **Both are recalled cross-repository analogies and were not independently verified in the audit that produced this page** — treat the three-floor generalisation as a heuristic, not an established fact.

Candidate standing rule, framed as heuristic: **a verification that can succeed on partial evidence must report how much evidence it had.** Not filed in `claims.md` — it is a rule of practice, not a falsifiable statement, and the claim ledger's value depends on every row being movable by evidence.

## Method note

**Corrected 2026-07-30 by the audit below.** An earlier version of this section claimed branch 1 was found statically and branch 2 by execution, and drew a moral about needing both passes. That is **wrong**: Codex's static review reported *both* `review.py:282` and `review.py:314`, naming the unvalidated snapshot explicitly. Execution later supplied an empirical demonstration of branch 2 — a fabricated snapshot rendering `'FABRICATED EVENT THE MODEL NEVER SAW.'` — which strengthened the finding but did not originate it.

What execution did originate is the **prefix-invariant verification** (609,535 prefixes, 0 divergences), which Codex was prohibited from producing under the static-review constraint rather than structurally incapable of. The honest version of the moral is narrower: execution converts a static reading into a demonstration and can settle invariants that static reasoning can only argue about — it did not find anything static review missed here.

## Round 4 — dispatched and delivered same day

[[workorders/eg-round4-review-gate-workorder-2026-07-30]], implemented by a Fable 5 agent. **359 tests / 1178 subtests green** (from 336/1102), `ARM_BLOCKS` byte-identical, nothing staged. Verified independently rather than relayed: all three previously-passing gate cases now **REFUSED** (event-only digest; matching-persona-with-stale-event; fabricated snapshot), a genuine full digest set still **PASSES**, and **all five** archived `real-validation-*` corpora remain refused. Label widening confirmed — `Sam Jr.:`, `Sam Sr.:`, `Mx. Sam:`, `Dr. Sam Jr.:`, `Rivera Esq.:` now caught, the documented residuals still missed, and the §4 false-abort sentinels unchanged in both directions. The prefix invariant was re-verified against the *widened* grammar: **2,852 constructed outputs, 123,994 prefixes, 0 divergences.**

Three things the implementer contributed beyond the order:

1. **It found a real contradiction in the order.** §2.1 required "at least one digest present, fail on any mismatch", but §6 required a row carrying only a truthfully-matching `event_sha256` to be *refused* — those cannot both hold. Resolved with a coverage rule: every recorded digest verified **and** a whole-stimulus digest (`stimulus_sha256`/`bundle_sha256`) required before the registry path renders.
2. **A fifth digest key the old gate never checked** — `persona_stimulus_sha256`, which real runner rows record.
3. **The widening reintroduced the round-3 alignment drift in mirror image.** A trailing honorific made an eight-word-plus-undotted-honorific prefix parse as nine plain words, so streaming resolved offset 0 while the final pass read a tag. Caught by the round-3 seeded sweep, fixed with a ninth word slot in the partial pattern. Any future label-grammar change should expect this class in both directions.

It also declined to close the `J. Sam:` initials gap, on the order's own criterion: initials would newly abort `"A. The first point: I was scared."`, enlarging the §4 class that is pending MK's decision. Measured 0/300 and left pinned as a disclosed residual.

## Audit provenance

This page was audited the same day by Codex `gpt-5.6-sol` at high reasoning, static-only, against a frozen snapshot of the round-3 tree (taken before round 4 began, to remove the race). Verdict **ACCURATE WITH CORRECTIONS** — ten corrections, all applied above, the most substantive being the method-note misattribution and the missing 60-vs-72 denominator.

It positively confirmed the load-bearing claims: both branch line numbers and the premature `return`; that a mapping-shaped snapshot bypasses all validation; that **`round3.patch` leaves E1/B1 and E6/B3 event strings byte-unchanged while rewriting their personas and advancing both bundles v1→v2** (the claim this page rests on and which had been asserted from memory); all six label outcomes; and that stratifying on `content_token_offset` is the appropriate way to separate the two effects.

## Open

- **Round 4 review** — Codex has not yet reviewed the round-4 implementation itself.
- **MK decision** — the false-abort trade: maximally paranoid guard that occasionally destroys a paid dialogue, versus a narrower net.
- **MK decision** — prompt-shape purification and arm-block exits, both still untouched per §6.
- Free MLX smoke, then numbers to MK, then paid regen only with sign-off. No human anchor labelling until the final corpus lands.
