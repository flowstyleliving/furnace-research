# Codex work order — blinded human-anchor review GUI for empathy-geometry

**For:** Codex `gpt-5.6-sol` · **Repo:** `empathy-geometry-harness` · **Written:** 2026-07-26 (Claude Code, executor)

**Codex is write/audit-only.** Author the code, the fixtures, the tests, and the docs. Do **not** run pytest, launch the server, open a browser, run `pip`, or call any model. Where verification needs execution the commands are listed under Acceptance and marked *not run by Codex*.

## Why this exists, stated first

Phase 3 of the study **already requires** MK to hand-label a stratified 20–40+ turn set as the human anchor for judge validation (`wiki/empathy-geometry/build-plan.md`, Phase 3 step 5, `[USER GATE]`). There is currently no tool for it, so the requirement is unmet by default. This is that tool.

It is **not** a dashboard, not a results viewer, and not a place to explore outcomes. It has one job: **capture an expert human read of a turn without contaminating it.**

A second job falls out of the first. MK is an NVC expert and wants to develop a *needs-depth ladder* — the distinction between a workable need word ("privacy") and a purer one ("a sense of safety"). That ladder cannot be written in advance from theory; it has to come from seeing what the models actually say. The notes captured here are the raw material for it. **The ladder is discovered on pilot dialogues, frozen, and only then applied to main-run dialogues** — never fitted and applied to the same data.

## The single most important requirement

**Blinding is enforced server-side, by omission.**

The browser must never receive a field it is not currently allowed to show. Hiding with CSS, `display:none`, or client-side filtering is **unacceptable** — a screenshot, a devtools panel, or a stray scroll defeats it, and the contamination is silent and unrecoverable.

Concretely: while a turn is unrevealed, the JSON sent to the page contains the turn text and nothing else that could bias a read. Specifically **omitted**: `arm`, `bundle_id`, `judge`, `check`, `geometry`, `persona_projection`, `solution_candidate`, `uptake_of_prior_solution`, and any field derived from them. They arrive only in a subsequent, explicitly-requested reveal response.

If in doubt about whether a field biases a read, omit it. A blinded tool that shows too little is a minor inconvenience; one that shows too much silently destroys the anchor it exists to produce, and there is no way to detect the damage afterward.

## Constraints

| Constraint | Value |
|---|---|
| Dependencies | **None new.** Python stdlib only (`http.server`, `json`, `pathlib`, `hashlib`, `argparse`) plus vanilla HTML/CSS/JS in a single file. Do **not** add Flask, FastAPI, Streamlit, React, or any CDN asset. |
| Network | **Localhost only.** Bind `127.0.0.1`. No outbound requests, no CDN fonts or scripts — the page must work with the machine offline. |
| Writes | The tool is **read-only over run artifacts**. It may never create, modify, or delete anything under a run directory. Session output goes to a separate path given by `--out`. |
| Auth | None, but refuse to bind a non-loopback interface even if asked. |

## D1 — `eg_harness/review.py`

A `ReviewSession` that loads turns and serves them one at a time.

**Loading.** Accept a `turns.jsonl` produced by `run-real` / `run-main`. Develop against the real 72-row file at `artifacts/real-validation-post-rubric-20260713/turns.jsonl` (6 dialogues × 12 turns × 3 arms, B2). Do not modify it.

**Sampling.** `--n` turns, stratified across arm, bundle, and turn position so the sample is not accidentally all-early or all-giraffe — the stratification key is computed server-side and **never sent to the client**. Deterministic under `--seed`, so a session is reproducible and a second reviewer can be given the identical sequence.

**Ordering.** Shuffled under the same seed. Reviewer must not be able to infer condition from position.

**Per-turn payload (unrevealed).** `review_id` (opaque — not the dialogue id, which leaks grouping), the turn `text`, the `event` text, and the two persona cards. **Nothing else — and specifically not the partner's prior turn.** See "One turn, no history" below; this is an NVC-substantive decision by MK, not a convenience.

The persona cards are safe to show and should be: they are **identical across all three arms** — only the primer differs — so they carry no condition signal, while withholding them would make the need judgment guesswork.

**Reveal.** A separate endpoint. Records that a reveal happened, for which `review_id`, and at what time, into the session file. A revealed turn's verdict is still recorded but flagged `revealed_before_verdict: true` if the reveal preceded submission — so a contaminated label is identifiable rather than silently pooled.

## One turn, no history — MK, 2026-07-26

**The reviewer sees a single turn and nothing before it.**

MK's reasoning, recorded verbatim in substance: NVC reads the present moment. Every utterance is either a *please* or a *thank you* in some number of words, and what is alive in a speaker right now is legible from what they just said. **Even a misinterpretation is still an interpretation of what is alive for the speaker** — a reflection that lands wrongly still reveals the state of the one reflecting.

This separates two judgments that had been tangled together:

- **What is alive in this turn** — turn-local, needs no history. This is what the reviewer labels.
- **Whether a reflection matched the partner's frozen card** — a key-lookup the machine already does, and   which does not require the reviewer to read the prior turn.

Two consequences, both good:

1. **Blinding gets strictly stronger.** The prior turn was the largest remaining leak — a blame-primed    preceding turn *sounds* blame-primed, so it would have carried condition signal straight past the    omission rules. Removing it closes that channel rather than managing it. **The open question at the    bottom of this order is therefore resolved: do not show the prior turn.**
2. **The unit of review becomes the unit of theory.** One turn, one read.

## D2 — the verdict schema

Keep it small; a long form does not get filled in honestly. Every field optional except the first two, so a reviewer can move fast and skip what they cannot judge.

- **`please_or_thank_you`: `please` / `thank_you` / `both` / `cannot_tell`** — Rosenberg's reading that every
  message is one or the other. Put it **first** in the form: it is the fastest, most native NVC judgment and
  it frames the ones that follow. Note the structural tie — it is the same distinction as the polarity in the
  frozen reflection template (*"my need for ___ **is** being met"* = thank you; *"**isn't** being met"* =
  please), so the human read and the machine parse can be compared directly on the same axis.
- `reflected_feeling`: `yes` / `partial` / `no` / `not_applicable`
- `reflected_need`: `yes` / `partial` / `no` / `not_applicable`
- `named_need_word`: free text — the need word the reviewer heard, verbatim
- **`purer_word`: free text — the word the reviewer would have used instead, if any.** This field is the seed of the depth ladder: across forty turns, the pairs `(named_need_word → purer_word)` *are* the ladder, discovered rather than declared. Give it a prominent place in the UI, not a footnote.
- `is_solution_proposal`: `yes` / `no`
- `authenticity`: `genuine` / `performative` / `cannot_tell` — with `cannot_tell` a first-class answer, never a failure to complete
- `notes`: free text, always visible, no character limit

## D3 — the page

Single self-contained HTML file, inlined CSS and JS, served by the Python module.

- One turn per screen. Large readable text; this is close reading, not scanning.
- Verdict form beside the text, keyboard-navigable.
- Progress as `n of N`, with no per-condition breakdown (that would leak the stratification).
- **Reveal button is deliberate**: a confirmation step, and after revealing, the verdict form for that turn is marked contaminated in the payload rather than disabled — MK may still want to record the read.
- Back/forward navigation, with verdicts editable until the session is closed.
- No charts, no aggregates, no comparison views. Those belong in analysis, after sealing.

## D4 — session output

Append-only JSONL at `--out`, one record per submitted verdict, plus a header record carrying: schema version `eg-review-session/1.0`, the source `turns.jsonl` path **and its sha256**, the seed, `n`, the stratification spec, the harness git commit, and a start timestamp. A session that cannot name the exact bytes it reviewed is not evidence.

## D5 — tests

`tests/test_review.py`, pure stdlib, no server launch, no browser:

- Stratified sampling is deterministic under a seed and covers the strata it claims.
- **The unrevealed payload contains none of the blinded keys** — assert against an explicit deny-list, and write the test so that *adding a new field to a turn record does not silently make it visible*: the payload builder should use an allow-list, and a test should fail if an unknown key appears in output.
- Reveal produces the blinded fields, and sets `revealed_before_verdict` correctly in both orders.
- The session header records the source sha256 and the record count matches submissions.
- The server refuses to bind a non-loopback address.
- Loading a `turns.jsonl` never writes to its directory (assert via mtime or a read-only temp copy).

## Acceptance — executor commands, NOT run by Codex

```bash
cd ~/Documents/empathy-geometry-harness
.venv/bin/python -m pytest tests/test_review.py -q          # C1
.venv/bin/python -m pytest tests/ -q                        # C2 — nothing else regressed
.venv/bin/eg-harness review --turns artifacts/real-validation-post-rubric-20260713/turns.jsonl \
  --n 20 --seed 20260726 --out artifacts/review-smoke.jsonl # C3 — serves, then Ctrl-C
# C4 — the blinding check, run by hand against the live server:
curl -s localhost:8765/api/turn/0 | python3 -m json.tool     # must show NO arm/judge/geometry
```

**C4 is the one that matters.** If `arm`, `judge`, `geometry`, or `check` appear in that response, the tool is not blinded and must not be used to produce an anchor, regardless of what the UI displays.

## Non-goals

- No aggregation, scoring, or agreement statistics — those come later, from the session file, after the confirmatory analysis is sealed.
- No editing of run artifacts, ever.
- No new dependencies.
- No remote access, no multi-user, no auth.
- The depth ladder itself is **not** built here. This tool only produces the raw pairs MK will use to build it.

## Resolved, previously open

~~Whether the reviewer should see the partner's **prior turn**.~~ **RULED 2026-07-26 by MK: no.** NVC reads the present moment, and a misinterpretation is still an interpretation of what is alive for the speaker, so the read is turn-local. This also closes the largest remaining blinding leak. See "One turn, no history".
