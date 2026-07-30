# Work order — nameless personas and label-free transcript (empathy-geometry-harness)

**Date:** 2026-07-29
**Repo:** `/Users/msrk/Documents/empathy-geometry-harness` — **local-only unless MK says otherwise**
**Base:** branch `fix/content-token-alignment` @ `7093f62`, plus the uncommitted working tree (see §7)
**Implementer:** fresh Opus 5 agent, max effort (may run tests and the tokenizer; may **not** run the paid regen)
**Reviewer:** Codex (write/audit-only, after implementation)
**Orchestrator:** Claude Code
**Supersedes:** `eg-selftag-prefix-mask-workorder-2026-07-29.md` — see §2

---

## 1. Why this exists

The MLX dyad model re-emits its own speaker label (`"Mara:"`) because
`eg_harness/providers.py:419` renders history as `"{speaker}: {text}"` and then
instructs `"Write Mara's next turn."`. The model imitates the format it is shown.

Two harms, both measured on `artifacts/real-validation-20260729` (n=72, clean run,
judge 144/144 valid):

**(a) Contaminated geometry.** Commit `7093f62` stopped us *measuring on* the tag,
but the tag still sits in the *conditioning context*:

| cohort | n | median `surprise_gen1` | saturated (\|s\|<1e-9) |
|---|---|---|---|
| no self-tag (offset 0) | 31 | 0.4844 | 2 |
| self-tag stripped (offset 3) | 41 | 0.0469 | 14 |

`d1_max_probability == 1.0` on 30/72. Once the model has written `Mara:`, the next
token is near-deterministic — every offset-3 Mara turn measures `84137` (` Theo`),
every offset-3 Theo turn measures `85504` (` Mara`), each at p≈1.0, because these
personas open by addressing each other by name. So `surprise_gen1` and the gen1
readout panel track *"did the model self-tag this turn?"* — a formatting coin-flip
— not the utterance, and the 41/31 split means gen1 cells are measured under two
different conditioning contexts and **are not comparable across turns**.

**(b) Broken blinding.** In the prior corpus, 63/72 stored turns opened with a
persona tag matching the true `speaker`, defeating the review GUI's field-level
`speaker` blind.

t=0 attention is unaffected (captured on the prompt, before generation).

## 2. Design directive — remove the cause, do not constrain the model

MK's instruction, 2026-07-29, verbatim in substance:

> *"I want the model to say what it naturally would say within its parameters of
> this task. The main reason is because when we say don't do something, it has to
> process it within its residual stream and, potentially, its null space somehow,
> and may affect the end token output."*

and then:

> *"You don't even need the names. Make it devoid of names, and you just say the
> person in front of you."*

**Consequences, binding on this order:**

- The previously adopted **prefix-path sampler masking is withdrawn.** It steers
  the distribution, and it censors the corpus. Do not implement it, and do not
  carry it forward from the working tree (§7).
- Do **not** add negative instructions to the prompt (`"do not write your name"`,
  `"do not prefix your turn"`). Prompt-level negation *does* enter the residual
  stream on every turn and negation raises salience of the negated token.
- **Detection remains permitted and required.** A read-only guard that inspects
  output changes nothing in the prompt and nothing in sampling. "Detecting is not
  forbidding."

The fix is structural: if there is no name and no label format anywhere in the
prompt, the model has nothing to imitate and nothing to emit.

## 3. Current state — what is already anonymous and what is not

Verified by reading `eg_harness/bundles.py`:

| bundle | speaker IDs | event refers to parties as | profiles name people |
|---|---|---|---|
| B1 seed-packets | `("J","K")` | `J`, `K` | yes — "You are Jules… You and Kai…" |
| B2 midnight-rewrite | `("Mara","Theo")` | `Mara`, `Theo` | yes — "You are Mara… You and Theo…" |
| B3 house-fund | `("T","W")` | `T`, `W` | yes — "You are Talia… You and Warren…" |

**B1 and B3 already use non-name letter handles as speaker IDs and in the event.**
That existing pattern — *abstract handle in the shared event, identity anchored by
the profile* — is the pattern to generalise. B2 is the outlier.

**`spec.ARM_BLOCKS` (giraffe / neutral / jackal) contain zero name mentions.** The
experimental manipulation is already name-free and must be left **byte-identical**.

## 4. Goal — the invariant

**No personal name, and no `"Label:"` turn-prefix format, may appear anywhere in
any string sent to the generating model.**

The `speaker` field stays in every experimenter-side record (`turns.jsonl`,
`dialogues.jsonl`, `manifest.json`) so we always know who said what. The model
never sees it.

Downstream benefit, note it but do not build for it: with no names in the payload,
the review GUI's blind stops depending on a field allow-list and becomes
structural.

## 5. Required work

### 5.1 Label-free transcript rendering — the core change

Replace `providers.py:419`:

```python
history = "\n".join(f"{row['speaker']}: {row['text']}" for row in request.history[-8:])
```

Render the transcript as **role-structured chat messages** instead: the current
speaker's own prior turns as `assistant`, the partner's as `user`, appended to the
message list passed to `apply_chat_template` in
`_apply_chat_template_if_available`. No name, no letter, no prefix — the role
structure carries the alternation, which is what chat models are trained on.

Requirements:
- Must degrade correctly in the no-tokenizer fallback path (the `f"System:\n…"`
  branch). Use a role marker there that is **not** a `Word:` name-like prefix and
  is not something the model would reproduce as its own opening; state your choice
  and justify it.
- Must preserve the existing 8-turn history window.
- Must handle the empty-history first turn.

### 5.2 Nameless prompt scaffolding

In `build_prompt`, remove `request.speaker` and `partner_name` from all
model-facing text. Replace:

```
"You are Mara; the other person is Theo."   → refer to the other party as
"Write Mara's next turn."                      "the person in front of you"
```

Keep the turn counter and the existing standing instructions (under 140 words, no
bullet lists, speak only as yourself). Those are task framing, not identity.

### 5.3 Anonymise the persona profiles

Three name mentions each (own ×1, partner ×2). Rewrite the identity clause and the
partner references only. **Everything else in the profile is frozen** — the shared
history, the lost conference slot, the father's illness, the rewriting mentor, the
needs, the unmet-need behaviour paragraph, the closing concrete detail. Same facts,
same order, same register, same length band.

The identity clause must anchor which party in the shared event the persona is,
without a name. For B1/B3 that anchor already exists (`"identified as J"`) and can
stay, since a letter is not a name. For B2 introduce the equivalent.

### 5.4 Anonymise the shared event

**Adopted: keep ONE shared event text per bundle**, with parties referred to by the
bundle's abstract handles. B1 and B3 already satisfy this and need **no change**.
B2's `E3_EVENT` is narrated entirely through names and must be converted to the
same handle style, including the gendered pronoun (`"Theo posted his draft"` →
handle + `their`). Removing the gender cue is deliberate: perceived gender is a
live confound in empathy measurement and it is currently baked into B2 only.

**Rejected: per-perspective event text** (a "you" version and a "the other person"
version). It would force us to prove two narratives carry identical facts, and it
would break the symmetric-information property the design currently has — both
parties see the same account. Not worth the risk for a cosmetic gain.

### 5.5 Audit every other name path

`persona.name` is read at least at `checker.py:263`, `judge.py:857`,
`judge.py:869`, `review.py:294`, `review.py:917`. Also audit
`Persona.heard_condition`, which is judge-facing rubric text and currently names
people (*"Theo tentatively and judgment-free reflects…"*) — a judge rubric that
names parties absent from the transcript is incoherent and must be converted.

Decide and justify whether `Persona.name` survives as an experimenter-side-only
field or is removed outright. Either is acceptable; a name reaching a model-facing
string is not.

### 5.6 Broaden the fail-closed detector

`_strip_leading_speaker_tag` currently keys on the known speaker labels. An
unnamed model may **invent** a name to fill the void. Broaden the detector to any
leading `Word:` pattern at the start of an utterance.

It stays **fail-closed and read-only**: a surviving leading tag, or a non-zero
`content_token_offset`, must abort the run — never silently strip. Keep all of the
`7093f62` `content_token_offset` machinery; under this design offset must be **0
by construction on every turn**, and that assertion is now the only backstop.

### 5.7 Hashes and provenance

`Bundle.hashes()` SHA-256s the profiles and event (`bundles.py:42`). These change.
That is a **registered-stimulus change**, not a formatting tweak — bump the bundle
`version` from `"v1"`, and make sure the new hashes land in `manifest.json` so old
and new corpora can never be silently pooled.

### 5.8 Tests

Extend `tests/test_providers.py` (reuse the existing `_PieceTokenizer` fake and the
`ContentTokenAlignmentTests` style). Mandatory:

- **Name-leak regression, the one that must never come back:** for every bundle in
  `BUNDLES` and every speaker and every arm, assert that the fully rendered prompt
  string contains **none** of that bundle's persona names, case-insensitively.
  Drive it off the registry so a fourth bundle is covered automatically.
- No `"{speaker}: "` prefix pattern appears in any rendered prompt.
- Role alternation is correct: own prior turns map to `assistant`, partner's to
  `user`, for both speakers.
- Empty history and the 8-turn window boundary.
- Broadened detector: an invented tag such as `"Sam: I hear you."` is caught and
  fails closed.
- `content_token_offset == 0` invariant.
- `ARM_BLOCKS` unchanged — assert their hashes against pinned literals.

## 6. Explicitly out of scope

- Any sampler-level, logits-level, or prompt-level constraint on what the model may
  say. Withdrawn by §2.
- Any change to `spec.ARM_BLOCKS`.
- Any change to persona content beyond the name clauses of §5.3.
- Any paid API call.

## 7. Starting material and what to discard

The working tree at `7093f62` carries **uncommitted** prefix-mask work — roughly
514 insertions across `eg_harness/providers.py` and `tests/test_providers.py`
(`_SelfTagPrefixMasker`, `_completes_leading_self_tag`, `_sampled_token_id`,
`_mask_token_ids_in_logprobs`, the `self_tag_prefix_mask_*` stamped fields, and the
`SelfTagPrefixMaskTests` class).

**Discard the masking apparatus** — it is withdrawn by §2, and Codex additionally
found it unsound: masking without renormalisation under an active `top_p=0.9`
(`providers.py:204`) is not equivalent to sampling from the renormalised masked
distribution. Verified numerically: masking without renormalisation left **1**
surviving token where renormalisation left **3**. That is also the true origin of
the `"Theo,"` artifact — it was the only option left, not a choice.

**Preserve** from that tree only what §5.6 needs: the fail-closed posture and the
`content_token_offset` assertions from `7093f62` itself (which is committed and
stays).

Do not reuse `wiki/workorders/eg-selftag-geometry.patch` — it implements a design
rejected twice.

## 8. Verification

Implementer runs `./.venv/bin/python -m pytest -q` — must be fully green — and may
use the live tokenizer.

Orchestrator then runs, in order: free deterministic-judge MLX smoke → check 0
leading tags of **any** form, `content_token_offset == 0` on **all** turns,
`surprise_gen1` saturation no longer cohort-split, no persona name anywhere in
`turns.jsonl` text, new bundle hashes stamped → report numbers to MK → paid regen
(~144 `claude-opus-5` judge calls) **only** with MK sign-off.

## 9. Known residual risk — state it, do not engineer around it

The model may **confabulate** a name to fill the void. Worse, an invented name
propagates: turn 1 invents one, turn 2 reads it in the transcript and adopts it,
and by turn 6 there is a stable name we never chose. §5.6's broadened detector
catches the self-tag form of this; a plain in-sentence invented name
(*"Sam, I hear you"*) it will not catch, and that is acceptable — an invented name
is authentic model output under the §2 directive, and it does not contaminate the
geometry the way a turn-initial tag does. The smoke output must be read by a human
for invented names before any paid spend.

## 10. Downstream

The regen changes turn text again, so **no human anchor labelling until it lands**
(MK decision 2026-07-29). `artifacts/anchor-session-20260727.jsonl` holds 2 session
headers and **zero verdicts** — nothing lost; archive rather than delete so the
false start stays on the record.
