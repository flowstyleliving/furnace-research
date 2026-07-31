# Work order — round 3: cap bypass, dialogue length, degeneration detector (empathy-geometry-harness)

**Date:** 2026-07-30
**Repo:** `/Users/msrk/Documents/empathy-geometry-harness` — **local-only unless MK says otherwise**
**Base:** branch `fix/content-token-alignment`, the current **uncommitted** working tree (rounds 1–2 of
[[eg-nameless-personas-workorder-2026-07-29]]; 293 tests passing, nothing committed)
**Implementer:** fresh Opus 5 agent, max effort (may run tests and the tokenizer; may **not** run the paid regen)
**Reviewer:** Codex (write/audit-only, after implementation)
**Orchestrator:** Claude Code
**Extends:** `eg-nameless-personas-workorder-2026-07-29.md` — that order's §2 design directive, §4 invariant
and §6 out-of-scope list remain **binding and unchanged**.

---

## 1. Status going in

Rounds 1–2 delivered the nameless-stimulus redesign: role-structured transcript, no persona name or
`Label:` format in any model-facing string, fail-closed read-only detectors, bundle `v1`→`v2` with
complete stimulus/rubric provenance. Codex's round-2 review **confirmed the stimulus edits clean** and
**endorsed the 8-word label bound**, but returned **FAIL** on one blocker plus six majors and four minors.

This order closes the blocker, adds two changes MK approved 2026-07-30 after reading the existing corpus,
and triages the remainder.

**Unchanged and still binding from the superseded order:** no sampler-, logit-, or prompt-level constraint
on what the model may say; no negative instructions in the prompt; detection is permitted because
detecting is not forbidding. `spec.ARM_BLOCKS` stay **byte-identical** — assert it.

---

## 2. BLOCKER — the label cap is applied to the run, not the label

`eg_harness/providers.py`, `leading_speaker_tag()`:

```python
_LEADING_TAG_PATTERN = re.compile(rf"^[ \t]*(?:{_LABEL}[ \t]*:\s*)+")
_LABEL_MAX_CHARS = 64
...
    tag = text[: match.end()]
    return tag if len(tag.strip()) <= _LABEL_MAX_CHARS else None
```

The trailing `+` greedily consumes **repeated** tags as one run, and the 64-character cap is then applied
to that whole run. Enough repetitions overflow the cap, `leading_speaker_tag()` returns `None`, streaming
alignment resolves at offset 0, and labelled output is **accepted into the corpus**.

Reproduced live against the current tree:

| input | result |
|---|---|
| `"Sam: I hear you."` | CAUGHT |
| `"Sam: " × 8` | CAUGHT |
| `"Sam: " × 14` | ***MISSED*** |
| `"Sam: " × 30` | ***MISSED*** |
| `"The person in front of you: " × 3` | ***MISSED*** |

The last row is the sharp one: that string is the confabulation the 8-word bound was widened to catch —
our own prompt says "the person in front of you" — and three repetitions defeat it.

**Fix.** Apply the bound **per label atom**, not to the aggregate run. Detection only ever needs the
*first* valid label; once one is found the turn aborts regardless of what follows. Apply the same
correction to `embedded_turn_label()`, which shares the pattern family, and keep `_PARTIAL_TAG_PATTERN`
consistent with whatever shape the leading pattern ends up with — if the two drift, streaming alignment
resolves an offset the final pass then rejects.

Add the four missed cases above as regression tests, plus the ×8 case that currently passes, so a future
narrowing cannot silently reintroduce the bypass.

---

## 3. Dialogue length: `DEFAULT_TURNS` 12 → 6

`eg_harness/spec.py:23` — `DEFAULT_TURNS = 12`. **Change to 6.** MK approved 2026-07-30.

**Evidence.** Measured on `artifacts/real-validation-20260729` (n=72, 6 dialogues × 12 turns). Similarity
of each turn to the *same speaker's own previous turn* (`difflib.SequenceMatcher.ratio()`):

| arm | mean | max |
|---|---|---|
| neutral | 0.083 | 0.318 |
| giraffe | 0.314 | **1.000** |
| jackal | 0.348 | 0.977 |

9 of 72 turns are ≥0.70 self-similar; two are verbatim. **Every one of them sits at turn_index ≥ 8.**
A 6-turn dialogue removes all of them at zero stimulus cost.

Two caveats added 2026-07-30 after the fact, neither of which changes the decision:

- **Metric-dependent.** The numbers above use difflib's default `autojunk=True`. Under `autojunk=False`
  the same corpus flags 14 turns with 3 below index 8. But those additions are *worse* discriminators, not
  better: their median `surprise_gen1` is 0.1186 against 0.0087 for the registered set, and three of the
  five added turns sit at or above the fresh-turn median. The registered variant is retained and stamped as
  `DEGENERATION_METRIC` so the choice is recoverable from any corpus.
- **A 6-turn dialogue is not saturation-free**, and the turn cut is not what makes it so. 5 of 36 turns at
  index ≤ 6 have `surprise_gen1 < 0.02` — but 4 of those 5 carry `content_token_offset > 0`, i.e. they are
  self-tag artifacts that the nameless redesign removes by construction. Saturation begins at turn 4 and is
  a self-tag phenomenon, not a repetition one.

Two knock-on effects to verify, not assume:

- `HISTORY_WINDOW_TURNS = 8` (`providers.py:398`) currently truncates a 12-turn dialogue. At 6 turns the
  whole conversation always fits the window, so the truncation asymmetry between early and late turns
  disappears. Confirm no code depends on the window ever biting.
- `review.py:283-291` derives `position_band` from `turns_per_dialogue`. **Already verified length-agnostic**
  — `position_band()` computes a fraction of the dialogue's own length rather than assuming 12, so it needs
  no change. Confirm no band goes empty at 6 and move on.

`spec.py` is touched here. `ARM_BLOCKS` in that same module must remain **byte-identical** — assert their
hashes against pinned literals, as the round-1 order already required.

---

## 4. Degeneration detector — read-only, **non-aborting**

MK approved 2026-07-30. Same posture as the name guard: inspect, record, change nothing about what the
model may emit.

**Critical difference from the name guard: this one must NOT abort.** A repeated turn is authentic model
output under the §2 directive, and aborting would discard an otherwise usable dialogue. It records and
flags; analysis decides what to do. Do not copy the fail-closed pattern here.

**Why it matters — CORRECTED 2026-07-30, after the order was first written.** The original motivation given
here was a 34× `surprise_gen1` gap (0.2939 fresh vs 0.0087 degenerate) described as a second contamination
worse than the self-tag. **That figure is confounded and is withdrawn.** 17 of the 19 saturated turns
(`surprise_gen1 < 0.02`) carry `content_token_offset > 0` — they are self-tag artifacts, not repetition.
Stratified on offset:

```
offset = 0 (clean)        fresh n=19  median 0.4731    degenerate n=5  median 0.2506    1.9x
offset > 0 (self-tagged)  fresh n=32  median 0.0377    degenerate n=4  median 0.0034   11.2x
uncontrolled              fresh n=51  median 0.2939    degenerate n=9  median 0.0087   34.0x
```

The self-tag is the dominant effect — **12.6×** measured among non-degenerate turns alone. Exactly one
saturated turn is attributable to repetition with no self-tag present.

**This does not cancel the work, it re-aims it.** The nameless redesign removes the self-tag by
construction, so on the coming corpus `content_token_offset` is 0 everywhere and the only open question is
whether the 1.9× residual matters. That is measured on n=5, on a corpus where the dominant confound was
present throughout, which is exactly why the detector must record **continuous ratios on every turn**
rather than a verdict: it is an instrument for sizing an unknown residual, not a fix for a known
contamination. Implement it as specified. Do not restate the 34× figure anywhere.

Degeneration remains an unambiguous **text-quality** defect regardless of geometry — two turns are verbatim
repeats — and that alone justifies §3.

**Record on every turn row, as continuous values plus a flag:**

- `self_similarity_prev_own_turn: float | None` — ratio against the same speaker's immediately preceding
  turn in this dialogue. `None` for a speaker's first turn.
- `similarity_prev_partner_turn: float | None` — ratio against the partner's immediately preceding turn.
  The observed failure mode is an accumulator: each turn repeats itself *and* absorbs a sentence from the
  other side, so the partner axis catches a mode the self axis misses.
- `degenerate_repetition: bool` — `self_similarity_prev_own_turn >= DEGENERATION_THRESHOLD`.

**Store the ratios, do not only store the flag.** The two populations are *not* cleanly separable in the
measured data — observed values run 0.43, 0.44, 0.50, 0.54, 0.67, 0.82, 0.83, 0.85, 0.90, 0.91, 0.91,
0.98, 1.00, 1.00 against a neutral-arm ceiling of 0.318. Any threshold in that range is a judgment call on
n=2 dialogues per arm. Continuous values let analysis re-threshold without a regen.

`DEGENERATION_THRESHOLD = 0.70` as a **named module constant**, stamped into `manifest.json` alongside the
other provenance so a corpus records the threshold it was scored under. Not a literal at the call site.

**Where.** `check_turn()` (`checker.py:224`) is the natural home — it is the existing read-only per-turn
checker — but it does not currently receive history. Either extend its signature or compute in the runner
loop (`runner.py:52-140`, where `history` is in scope) and merge into the row. Implementer's call; state
which and why. Whatever you choose, the ratios must appear in `turns.jsonl` on every turn.

Also surface a per-dialogue and per-arm degenerate-turn count in `summary.json`, so a bad run is visible
without a separate analysis pass.

---

## 5. Codex round-2 majors — triage

Do these:

1. **Dialogue RNG seeding is coupled to a literal persona name.** `providers.py:58` and `providers.py:202`
   both compute `... + (0 if request.speaker == "Mara" else 503)`. Speaker IDs are `('J','K')`,
   `('Mara','Theo')`, `('T','W')` — so the offset is **inert on B1 and B3** (both speakers take the 503
   branch) and does nothing to decorrelate their streams. It does not currently produce a collision,
   because speakers alternate on `turn_index` parity and so never share a seed within a dialogue; it is a
   latent defect and a leftover name coupling the redesign was meant to remove. Derive from
   `bundle.speakers.index(request.speaker)`.
2. **Provenance validation at analysis and pooling boundaries.** `summarize` and `export_projection_csv`
   accept rows without checking stimulus provenance agrees. Apply the same group-and-require-agreement
   rule `assert_consistent_stimulus_provenance` already enforces in `write_run`, and **reject uniformly
   missing provenance** rather than treating absence as consistent.
3. **Review GUI must render the run's stimulus snapshot, not the live registry.** Labelling an older run
   currently shows MK the *current* persona text rather than what the model actually saw. This one is
   MK-facing and directly corrupts the human anchor pass — it matters more than its severity label
   suggests.
4. **Bind the exact judge scoring-instruction text into `RUBRIC_SHA256`**, not just the payload fields.
5. **Durable quarantine artifact for aborts.** An aborting turn currently dies with its content only in an
   exception message. Write the complete raw output to a quarantine file so the authentic artefact
   survives for inspection.
6. **Taint guard scans the whole history**; it only needs the `[-HISTORY_WINDOW_TURNS:]` slice that
   actually reaches the prompt. Narrow it — a name in a turn that no longer enters the window is not a
   leak, and aborting on it is a false positive.

Minors, apply if cheap: narrow the unrestricted `.` inside `_LABEL_WORD` to honorific position only
(Codex called the current allowance a net loss and I agree); `output_edited=False` is inaccurate given the
`.strip()` — either stop stripping or describe it honestly. `_resolve_chat_template` already tries the
inner tokenizer; confirm and close that item.

---

## 6. Out of scope — awaiting MK decision, do NOT implement

- **Prompt-shape purification.** Proposed 2026-07-30 and **not yet approved**: move the turn counter into
  the system message, drop the `"You are in conversation with the person in front of you… Write your next
  turn."` stage direction currently fused into the last `user` message, add one line of positive
  peer-conversation framing, stamp a prompt-scaffolding version. Verified to render clean on the live Qwen
  template including the system-only first turn. **Leave the current shape untouched until MK rules.**
- **Arm-block exits.** The measured degeneration is arm-structured, and solution-proposal counts track it
  inversely (giraffe 5/22, neutral 16/24, jackal 3/24). Hypothesis: a solution is how a conversation ends;
  neutral is permitted one and the two experimental arms are steered away, so they have nowhere to go and
  loop. Giving giraffe and jackal an exit is a **registered-stimulus change** on n=2 dialogues per arm.
  MK decision, not an implementation task.
- Everything already out of scope in the superseded order §6.

---

## 7. Tests

Extend the existing suites, reusing `_PieceTokenizer` and the `ContentTokenAlignmentTests` style.
Mandatory:

- Cap-bypass regression: all five rows of the §2 table, asserting CAUGHT on each of the four that
  currently miss.
- `embedded_turn_label` under the same repetition pressure.
- `DEFAULT_TURNS == 6`, and `ARM_BLOCKS` hashes pinned and unchanged.
- Degeneration detector: verbatim repeat → ratio 1.0 and flag True; a fresh turn → low ratio, flag False;
  first turn of a speaker → `None`, not `0.0`; the detector **never raises**; the threshold reaches
  `manifest.json`.
- Partner-axis similarity catches an accumulator turn that the self axis alone scores below threshold.
- RNG seeding differs between the two speakers of **every** bundle, driven off the registry so a fourth
  bundle is covered automatically.
- All existing name-leak, detector, alternation, and provenance tests stay green.

---

## 8. Verification

Implementer runs `./.venv/bin/python -m pytest -q` — must be fully green — and may use the live tokenizer.

Orchestrator then runs, in order: free deterministic-judge MLX smoke → check 0 leading tags of any form,
`content_token_offset == 0` on all turns, no persona name anywhere in `turns.jsonl` text, degeneration
ratios populated on every turn, 6-turn dialogues, new hashes and threshold stamped → **read the smoke
output by eye for confabulated names and for jackal-arm softening** → report numbers to MK → paid regen
(~144 `claude-opus-5` judge calls) **only** with MK sign-off.

---

## 9. Downstream

Unchanged: no human anchor labelling until the final corpus lands.
`artifacts/anchor-session-20260727.jsonl` holds 2 session headers and zero verdicts — archive, do not
delete.

Nothing in this repo is committed or pushed. The push question remains open with MK.
