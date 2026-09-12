# Work Orders — convention

_This folder is the home for **work orders**: the durable spec + acceptance record a builder (usually Codex, per the write/audit-only rule) implements against, and that `wiki/log.md` cites. A work order is **not** a throwaway temp file — it is tracked provenance. True scratch (unreviewed drafts) belongs in the session scratchpad, never here._

## Lifecycle
```
wiki/workorders/<slug>-workorder-<YYYY-MM-DD>.md      ← active
        │  (order attested complete in the log)
        ▼
wiki/_archive/workorders/<slug>-workorder-<YYYY-MM-DD>.md   ← done
```
- **Active** orders live directly in `wiki/workorders/`.
- When an order is attested complete (log entry confirms the deliverable landed), **move** it to `wiki/_archive/workorders/`. Do not delete it — it is git-tracked provenance and is often referenced by append-only log entries.

## Naming
- `<slug>-workorder-<YYYY-MM-DD>.md` — e.g. `kv-tension-overlay-workorder-2026-07-25.md`.
- `<slug>` is a short kebab-case handle for the deliverable; the date is the order's authoring date.

## What a work order contains
1. **Goal** — the deliverable in one line.
2. **Guardrails / pins** — the constraints the builder must honor (sealed files not to touch, enumeration method, comparability rules, etc.).
3. **Acceptance** — how "done" is verified, and by whom. Codex marks verification "not run by Codex" when execution is required; a runtime executor supplies artifacts.
4. **Handoff** — who authors, who executes.

## Grandfather clause (2026-07-26)
The work orders authored **before** this folder existed remain at the wiki root, because they are linked from *append-only* log entries and moving them would break those historical links:
- `wiki/kv-tension-overlay-workorder-2026-07-25.md` — still open; no port has landed in `commit-confluence` (checked 2026-09-12)
- `wiki/repo-standalone-workorder-2026-07-25.md` — still open; no `pyproject.toml`/tag in `t0-morphology-furnace`, no import swap in either consumer repo (checked 2026-09-12)

They self-clear as they complete (archive them then, accepting the historical link becomes known-unresolved — same policy as intentionally-deleted pages, see `wiki/index.md`). **All new work orders go straight into `wiki/workorders/`.**

**Self-cleared 2026-09-12:** `wiki/vault-maintenance-workorder-2026-07-26.md` → `wiki/_archive/workorders/vault-maintenance-workorder-2026-07-26.md` (deliverable landed and its Tier-1 items closed; see [[_archive/vault-tidy-plan-2026-07-26]]).
