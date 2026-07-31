# Work order — round 4: close the review stimulus gate (empathy-geometry-harness)

**Date:** 2026-07-30
**Repo:** `/Users/msrk/Documents/empathy-geometry-harness` — **local-only unless MK says otherwise**
**Base:** branch `fix/content-token-alignment`, HEAD `7093f62`, **the current uncommitted working tree** (rounds 1–3; 336 tests green)
**Implementer:** Fable 5 agent (may run tests and the tokenizer; may **not** run the paid regen)
**Reviewer:** Codex `gpt-5.6-sol` (write/audit-only, after implementation)
**Orchestrator:** Claude Code
**Extends:** [[eg-round3-degeneration-workorder-2026-07-30]] and [[eg-nameless-personas-workorder-2026-07-29]] — both still binding, including the no-constraint design directive and the §6 out-of-scope list.
**Findings page:** [[empathy-geometry/harness-round3-review-2026-07-30]]

---

## 1. Status going in

Round 3 landed clean: 336 tests, `ARM_BLOCKS` byte-identical, round-2's label-cap bypass closed and independently verified. Codex's static review then returned **FAIL** on the *new* code round 3 introduced.

Everything below is in code that has **never run against a corpus**, so nothing on disk is contaminated and no data cleanup is owed.

**Standing directives, unchanged:** no sampler-, logit-, or prompt-level constraint on what the dyad model may say; no negative instructions in any prompt; detection is permitted and required. `spec.ARM_BLOCKS` byte-identical — assert it. Do not touch anything in the round-3 order's §6 (prompt-shape purification, arm-block exits).

---

## 2. BLOCKER — `review.py`, both branches

This gate stops the review GUI showing the human reviewer persona text the model never read. It guards the expert anchor pass, which is the study's ground truth. Both branches let the wrong stimulus reach the screen with no visible warning.

### 2.1 Branch 1 — the early return (`review.py:282`, `return` at `:295`)

```python
for key, recompute in _STIMULUS_DIGEST_CHECKS:
    recorded = _recorded_digest(row, key)
    if recorded is None:
        continue
    if recorded != recompute(bundle):
        raise ReviewError(...)
    return          # <-- verifies ONE slice, declares the whole verified
```

The four digests are **not four fingerprints of one object**. `stimulus_sha256` covers the whole stimulus; `persona_sha256` only the profiles; `event_sha256` only the event; `bundle_sha256` the bundle including the scoring key. Checking one is not checking the rest.

Demonstrated: a row carrying only `event_sha256` **passes** and renders live-registry text. That is not hypothetical — **B1 and B3's event text was byte-unchanged across v1→v2** (both already used letter handles), so `event_sha256` truthfully reports "unchanged" while every persona was rewritten. Codex's variant is sharper: `persona_sha256` matching while `event_sha256` and `bundle_sha256` are stale passes on the persona alone, because persona is ordered above event.

Current artifacts survive only on tuple ordering plus which fields the runner happens to write. That is luck, not design.

**Required:** verify **every** digest the row records. Require at least one present. Fail on **any** mismatch. Do not stop at the first match. The error message must name every digest that was actually compared, so the guard's success signal reports its own coverage rather than hiding it.

### 2.2 Branch 2 — an unvalidated snapshot (`review.py:314`)

A row carrying `dialogue_stimulus` returns it immediately and is **never checked against any recorded digest**. Demonstrated by passing a fabricated snapshot with all four recorded digests zeroed; it rendered `'FABRICATED EVENT THE MODEL NEVER SAW.'` straight to the reviewer payload.

**Required:** recompute the supplied snapshot's own digest and compare it to the row's recorded `stimulus_sha256`. A snapshot that cannot be validated — no recorded digest to check it against, or a mismatch — must **not** be rendered. Fail closed; "we cannot tell" resolves to a stop, exactly as `_assert_registry_still_matches_run`'s own docstring already says.

Note `Bundle.canonical_stimulus()` and `Bundle.stimulus_sha256()` already exist (added round 1, §5.7) — the recompute path should reuse them rather than inventing a second canonicalisation, or the two will drift.

### 2.3 The fixture that commits the pattern — `tests/test_review.py:521`

```python
snapshot = spec.get_bundle("B2").canonical_stimulus()
rows = [{**json.loads(line), "dialogue_stimulus": snapshot} for line in REAL_TURNS...]
```

This attaches **today's** B2 snapshot onto rows of the **archived v1** run. Its intent is sound and stated — exercise blinding and stratification against real utterances — and its sibling `TestArchivedRunWithoutASnapshot` asserts the same corpus is refused without a snapshot. But as written it is the corruption pattern, committed as a fixture, and under §2.2 it will stop passing.

**Required, and this is the load-bearing instruction: do NOT weaken the gate to make this test pass.** That is precisely how a fail-closed guard dies. Reconstruct the fixture so the blinding coverage survives with internally consistent provenance, and make its docstring state plainly that its provenance is synthesised and that it tests blinding only, never provenance. If you conclude the coverage genuinely cannot be preserved without a real corpus, say so and leave it failing rather than softening §2.2.

---

## 3. MAJOR — the label guard's stated coverage is false

`leading_speaker_tag()` documents itself as catching a turn-initial label of "ANY shape." Measured against the current tree:

| input | result |
|---|---|
| `Sam:` | CAUGHT |
| `Dr. Sam:` | CAUGHT |
| `J. Sam:` | MISSED (disclosed) |
| `Mx. Sam:` | MISSED (**undisclosed**) |
| `Dr. J. Sam:` | MISSED (**undisclosed**) |
| `Sam Jr.:` | MISSED (**undisclosed**) |

Do **both** of the following:

1. Widen where it is cheap and does not enlarge the false-abort class of §4 — a trailing honorific (`Sam Jr.:`, `Sam Sr.:`) and an honorific not on the list are the obvious gaps. Measure the false-abort cost of each widening against the 300 archived real turns the round-3 tree already uses as its zero-false-match baseline, and report it.
2. **Make the docstring true.** Replace "ANY shape" with an explicit statement of what the pattern does and does not reach, including whatever residuals survive step 1. A fail-closed guard that overstates its coverage is one that stops being audited — that is the actual defect here, more than any single missing form.

---

## 4. Explicitly NOT in scope — MK decision pending

The **false-abort class** is real and measured: `"St. Louis felt like the clearest comparison: I felt small."`, `"Gen. anxiety is what I keep coming back to: it never lifts."`, `"Fr. my side it looked different: you left."`, and — not honorific-dependent at all — `"Miss this point: I am not refusing you."` The same shape would abort `"Look: I was scared."`

This is inherent to "any turn-initial `Words:` aborts," not introduced by the honorific narrowing. Whether to keep a maximally paranoid guard that occasionally destroys a paid dialogue, or narrow the net, is a research trade MK has not yet decided. **Do not narrow it on your own initiative**, and do not widen it in §3 in a way that makes this class worse without saying so.

Also out of scope: prompt-shape purification; arm-block exits; any change to `ARM_BLOCKS`; any paid API call.

---

## 5. Minors — do if cheap, skip and say so if not

- `checker.py:309`/`:326` — `turn_repetition()` is documented total and non-raising but `float(threshold)` raises `OverflowError` on an absurd threshold, and a row object whose `__str__` raises escapes. Ordinary malformed shapes are already handled correctly.
- `providers.py:67` — quarantine filenames can collide when two identical payloads land in the same microsecond, and `write_text()` overwrites. Practical risk is nil; make the path unique rather than restructuring.

---

## 6. Tests

- **Branch 1:** a row recording a *matching* `persona_sha256` alongside a *stale* `event_sha256` must be refused. A row recording only `event_sha256` for B1 or B3 — where that digest legitimately did not move across v1→v2 — must be refused. A row whose every recorded digest matches must pass.
- **Branch 2:** a fabricated snapshot with a wrong or absent `stimulus_sha256` must be refused; an authentic snapshot with a matching digest must pass.
- **Regression:** both archived corpora must still be refused (they are today — keep it that way).
- **§3:** each newly-caught form, plus a pinned list of the residuals the docstring now admits, so the docstring and the behaviour cannot drift apart silently.
- All existing tests stay green, `ARM_BLOCKS` hashes pinned and unchanged, `DEFAULT_TURNS == 6`.

---

## 7. Constraints

Do not commit, stage, push, or branch. Never `git add -A`. No paid API calls. Do not touch `/Users/msrk/Documents/t0-morphology-furnace`. Run `./.venv/bin/python -m pytest -q` and report it in full.

Report: every file changed; before/after measurements for §2 and §3; which minors you did; full pytest output; `git status --short` and `git diff --stat`; proof `ARM_BLOCKS` is byte-identical; and **anything in this order you believe is wrong**. Previous rounds' implementers caught three factual errors in their orders by measuring before changing — that is the expected behaviour, not an exception.
