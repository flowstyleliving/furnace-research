# Equal Stewardship Protocol

Codex and Claude Code are peer stewards of this vault. Equal stewardship means either model may make canon updates and propagation decisions, but every steward follows the same evidence order, append-only rules, and propagation checks.

This page is operational governance, not a research result.

As of 2026-07-09, Codex has an additional operating constraint: **write/audit-only**. Codex may inspect files, synthesize state, author patches/specs/docs, and perform static reviews, but must not run project code, tests, harnesses, smoke/pilot runs, model inference, calibration/extraction jobs, app entrypoints, or agent-spawn commands. When execution is needed, Codex writes the exact command/work order and records verification as "not run by Codex"; the user, Claude Code, or another executor supplies run artifacts.

## Canon Order

For "what is true now," read sources in this order:

1. `wiki/log.md` tail
2. Relevant `wiki/results/*.md`
3. `wiki/research-candidates.md`
4. `wiki/index.md`
5. Root orientation files: `CLAUDE.md` / `AGENTS.md`

Lower-numbered sources win on conflict. `wiki/index.md` is for navigation, not final truth. Root orientation files are convenience caches and decay unless backed by fresher log/result pages.

## Steward Authority

Either Codex or Claude Code may:

- read and synthesize vault state
- update result pages, summaries, index rows, orientation files, and paper scaffolds
- perform propagation audits after new results
- mark stale claims as superseded when the log/result pages justify it

Neither steward may:

- rewrite append-only history
- treat orientation files as more authoritative than the log tail
- promote a candidate to a result without a pre-reg/result artifact
- silently alter sealed claims, denominators, benchmark scope, or comparability scope
- update only `CLAUDE.md` or only `AGENTS.md` when the change affects both models

## Session Start

Every steward session starts with a short canon read:

1. Read the `wiki/log.md` tail first.
2. Check the relevant result, candidate, or paper page for the task.
3. Use `wiki/index.md` for navigation only.
4. If touching paper files, read `wiki/paper/README.md`.
5. If touching the empathy-geometry line, read `wiki/empathy-geometry/README.md`.

## Propagation

For new results or verdicts, propagate in this order:

1. Create or update the dedicated `wiki/results/*.md` page.
2. Update `wiki/research-candidates.md` if a candidate status changed.
3. Update `wiki/results/summary.md` in place.
4. Update `wiki/index.md`.
5. Update `CLAUDE.md` and `AGENTS.md` together only if the active frontier changed.
6. Append a concise `wiki/log.md` entry using Obsidian CLI when possible.

For design-phase work, use lighter propagation:

1. Artifact page
2. Candidate ledger if needed
3. Index row
4. Log entry

Do not add a root hot-update unless the active frontier actually changed.

## Handoff Packet

At the end of any substantial steward session, leave a compact handoff note in the final answer or log entry:

- **What changed:** files or claims touched
- **Canon impact:** result, design note, paper edit, orientation sync, or no canon change
- **Open decisions:** user decisions still needed
- **Verification:** commands/checks run, or "not run"
- **Propagation status:** complete, partial, or not needed

Use these labels for cross-model continuity:

- `CANON UPDATED`
- `DESIGN ONLY`
- `PAPER ONLY`
- `PROPAGATION AUDIT`
- `NEEDS USER DECISION`
- `STALE / SUPERSEDED`

## Guardrails

- `wiki/log.md` and `wiki/results/history.md` remain append-only.
- `CLAUDE.md` and `AGENTS.md` stay semantically synchronized.
- Codex remains write/audit-only: no tests, harnesses, model calls, experiment runs, app entrypoints, or agent-spawn commands from Codex sessions.
- Do not quote the historical PRI digest as current unless explicitly framing it as historical.
- Do not pool byte-comparable, non-byte-comparable, Modal/torch, MLX, and mlx-vlm cells unless a page explicitly says they are comparable.
- Do not treat Furnace guard `BLOCK`/`ALLOW` as a general safety policy unless a matching domain calibration exists.
- Do not let the empathy-geometry design phase imply validated results before a prereg/run exists.

## Acceptance Checks

- New result lands: result page, summary, index, log, and candidate status all agree.
- Frontier changes: both `CLAUDE.md` and `AGENTS.md` receive the same hot-update.
- Design-only artifact lands: root orientation remains unchanged unless active project state changed.
- Codex-authored changes that need execution include a static-review note plus executor-owned commands/artifact expectations, not Codex-run results.
- Conflict found: log tail wins; stale lower-source pages are corrected or marked superseded.
- Claude resumes later: `CLAUDE.md` plus the log tail is enough to avoid stale claims.
- Codex resumes later: `AGENTS.md` plus the log tail gives the same state.

