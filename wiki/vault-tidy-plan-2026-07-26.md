# Vault Tidy — living execution checklist (2026-07-26)

_Companion to the static audit [vault-maintenance-plan](vault-maintenance-plan.md). This is the **living tracker**: check items off as they land. Durable across chat compaction — read this to resume. Steward = Claude Code (sole steward as of 2026-07-26); Codex is write/audit-only._

## ✅ Done (this session)

- [x] **Q-POS retired** — dead ELI12 index row + `qpos-golden-eval-plan` row + learn/README bullet + tracked page removed (`c052b61`).
- [x] **AGENTS.md retired → single-steward canon** — file deleted; CLAUDE.md canon rewritten; 3 live pages delinked (`c052b61`).
- [x] **index.md made exhaustive** — 19 rows added; standing policy = every page gets a row (`c052b61`).
- [x] **13 ELI12 broken links repaired** — date-prefix drift fixed across 16 learn pages (`ed525ac`).
- [x] **RPV format-duplicate figures deleted** — superseded `fig1_rpv_vs_confidence.{pdf,png}` + `.png` twins of fig1_forest/fig2/fig3 (paper uses the PDFs) (`ed525ac`).
- [x] **Local cruft removed** — `wiki/paper/.DS_Store`, `cc-figures/__pycache__` (`ed525ac`, untracked).
- [x] **references-code.md de-staled** — t0 "living lab" → RE-SEALED archive-only (`ed525ac`).

## 🟡 Policy calls — MK decisions folded in

- [ ] **Append-only tombstone links** — MK: "just say those pages were deleted." → **Decision: accepted-unresolved list**, not stub pages. Action: add a short `## Known intentionally-deleted pages` note (here or in the maintenance plan) listing `stewardship-protocol`, `lit/prediction-rupture-at-commitment`, old `paper/scaffold`/`pri-v3-plan` paths. Obsidian's graph will still show these as unresolved edges *from historical log lines* — that is expected and accepted (the log is append-only; we do not edit history).
- [ ] **Convert 3 wiki→repo pointers written as wikilinks** → plain markdown links:
  - `results/v4-sealed-2026-05-26.md` → `[[PRI_V4_PRE_REGISTRATION_PLAN]]` (repo file)
  - `results/t0-residual-pilot-2026-05-28.md` → `[[pilot_t0_residual.py]]`, `[[pri_calibrator]]` (repo files)
  - `results/_synthesis-scratch.md` → `[[../../CLAUDE|CLAUDE.md]]` (easy local fix: `[CLAUDE.md](../../CLAUDE.md)`)
- [x] **RPV PNG alternates** — MK: "if they're just duplicates in a different format, delete." → done in the safe batch.

## 🔵 Bigger items to work through

- [ ] **Monthly-checklist cron** — MK: yes, set up a cron job. Plan: a recurring monthly job that runs the mechanical hygiene checks read-only (`obsidian unresolved`, index-vs-tree diff, `.DS_Store`/`__pycache__` scan, append-only date-order check) and writes a dated report page under `wiki/results/` or pings MK. Decide: run-and-report vs. run-and-auto-fix-safe-items. (Recommendation: run-and-report; fixes stay steward-gated.)
- [ ] **`_bundles/` folder for the 13 Overleaf zips** — MK: yes. Create `wiki/paper/_bundles/` and `mv` all `*.zip` there (they're gitignored/local-only, so this is a local move). Update `wiki/paper/README.md` bundle list to note the new location. Keep every bundle (superseded ≠ deletable — some are referenced by append-only log entries).
- [x] **Work-order standard** (MK's main concern) — created `wiki/workorders/README.md` (the standard's body) + one-line `CLAUDE.md` pointer + index row; grandfathered the 3 existing root orders in place. Convention chosen: standard lives *with the thing it governs* (leaf), CLAUDE.md holds only a pointer — the "parsimony" pattern.
- [ ] **Phase 2 semantic audit** (from the maintenance plan): results↔models↔claims cross-reference (rule 5b), subtree consistency (`learn/`, `empathy-geometry/`, `lit/`, `sup/`), duplicate-content scan, remaining stale-orientation flags.

## 🧭 Future — organization / nomenclature (MK raised 2026-07-26)

_The parsimony principle: **detail lives in the leaf; the root holds pointers.** Apply it to the loose canonical root files too._

- [x] **Group loose canonical root pages** (done 2026-07-26, MK: "execute both moves"). `meta/` created for how-the-vault-works pages; `references-code` folded into the existing `references/` (kills the `references/`-folder-vs-`references-code`-page collision). Moves: `tooling-obsidian-cli.md` → `meta/obsidian-cli.md` (gitignored — plain `mv` + `.gitignore` rule relocated); `methodology-llm-wiki.md` → `meta/llm-wiki-methodology.md` (`git mv`); `references-code.md` → `references/code.md` (`git mv`). Policy: **move+accept** (not grandfather) — these are navigate-*to* pages worth a tidy home; the only append-only casualty is `log.md`'s historical links → accepted-unresolved (same as tombstones). All editable inbound links fixed (overview, index, claims, pri-v3/v3-code-map, _archive/intake-checklist, CLAUDE.md Vault Map, workorder gitignore fact).
- [x] **Directory nomenclature uniqueness** (scheme adopted 2026-07-26). Two-tier rule: **leading `_` = infrastructure/non-content** (`_archive/`, `_bundles/`), **plain noun = content/canonical** (`results/ models/ learn/ lit/ sup/ paper/ empathy-geometry/ feedback/ references/ meta/ workorders/ pri-v3/`). A folder name alone now signals what's inside. Remaining oddities are acceptable content folders: `pri-v3/` (version-scoped historical line) and `empathy-geometry/` (named research line).
- [ ] **CLAUDE.md hot-update archive (biggest lever on "lean & robust").** Migrate the older dated "Hot update" blocks (2026-06-06 … 2026-07-22) into a `wiki/orientation-archive.md`, leaving CLAUDE.md with just the current frontier + durable HARD RULES. Canon rule 4 already says orientation blocks decay into history — this makes the file physically match the rule. Separate decision from the above.

## 📐 Proposed work-order standard (NEEDS MK DECISION)

**Problem:** work orders (`kv-tension-overlay-workorder-2026-07-25`, `repo-standalone-workorder-2026-07-25`, `vault-maintenance-workorder-2026-07-26`) and one-off docs pile up at the wiki root.

**Proposed convention:**
1. 📁 New home: **`wiki/workorders/`** for active orders; **`wiki/_archive/workorders/`** when the order is attested complete.
2. 🏷️ Name: `<slug>-workorder-<YYYY-MM-DD>.md` (unchanged).
3. ♻️ Lifecycle: `active (workorders/)` → `done` → move to `_archive/workorders/`. A work order is **not deleted** (git-tracked provenance; often referenced by append-only log entries).
4. 🔗 **Grandfather clause (the catch):** the 2 existing root work orders are linked from *append-only* log entries. Moving them breaks those historical links. Options:
   - **(a) Grandfather** — leave the existing 3 at root, apply the new folder only going forward. (Simplest; zero broken links.)
   - **(b) Move + accept** — move all to `workorders/`, accept the historical log links as known-unresolved (same policy as tombstones above).
   - **(c) Move + redirect stubs** — move, and leave a one-line stub at the old root path. (Cleanest graph, most files.)
   - _Recommendation: **(a) grandfather** — the root clutter is bounded (3 files) and self-clears as orders complete; new orders go straight to `workorders/`._

**On "temp files":** work orders are not throwaway temp files — they are the durable spec + acceptance record Codex builds against, and the log cites them. So they belong in the vault (tracked), just in a dedicated folder rather than loose at root. True scratch (unreviewed drafts) belongs in the session scratchpad, never the vault.

## Other loose root files (for the same triage)
- ~~`methodology-llm-wiki.md`, `references-code.md` — keep at root~~ → **MOVED 2026-07-26** to `meta/llm-wiki-methodology.md` and `references/code.md` (superseded the earlier keep-at-root call; MK opted move+accept).
- `Candidate-10-Shadow-Ambiguity-Deconstruction.md` — math deconstruction; consider moving under `learn/` (where the ELI12 companion lives) for consistency — MK call.
- `vault-maintenance-plan.md` + `vault-maintenance-workorder-2026-07-26.md` + this file — the tidy artifacts; archive together once tidy is complete.
