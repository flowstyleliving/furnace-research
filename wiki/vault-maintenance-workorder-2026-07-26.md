# Work Order — Vault Maintenance Plan (Codex gpt-5.6, DESIGN/AUTHOR ONLY)

**Date:** 2026-07-26
**Author of order:** Claude (Opus 4.8), second-passed by Opus 5 (GO-WITH-EDITS; all five must-fixes integrated).
**Executor:** Codex gpt-5.6-sol
**Deliverable:** `wiki/vault-maintenance-plan.md` — a *plan document only*. Codex authors the audit findings + prescribes tiered actions. **Codex runs nothing** (HARD RULE: Codex is write/audit-only — no tests, harnesses, model inference, package scripts, or agent spawns). It may use static tooling only: `rg`, `sed`, `git diff`/`git ls-files`/`git check-ignore`, `find`, `apply_patch`, and the read-only `obsidian` sub-commands (`unresolved`, `backlinks`, `search`). Every proposed action that needs execution is written as an exact command marked **"not run by Codex,"** to be run later by Claude Code or MK.

---

## 0. Framing / guardrails (read first)

- General repo/vault maintenance for the Furnace research vault (`/Users/msrk/Documents/the_GOAT`, Obsidian). Goal: "spick and span" without touching *any* research truth.
- **Audit universe** = `wiki/**/*.md` (146 files) **plus** the root orientation files `CLAUDE.md` and `AGENTS.md`. **Explicitly excluded:** `raw/` (immutable), `.git/`, and the git internals. (Whole-repo md count is \~169; do not conflate it with the 146 wiki count.)
- **Do not alter research content.** No numbers, claims, verdicts, sealed content, denominators, or scope. Hygiene only.
- **Append-only files are sacrosanct:** `wiki/log.md`, `wiki/results/history.md`. The plan may *recommend* future appends but must never propose rewriting history, reordering rows, or diffing them against git history.
- **Sealed / frozen content is off-limits:** the sealed 18/20, t0 byte-identity, `raw/` immutability, archived `pri-*` paper files. Flag but never prescribe edits to these.
- **Source-of-truth order** (Vault canon rule 2): log tail → results/*.md → research-candidates.md → index.md → root orientation. Respect this when calling anything "stale."
- **Gitignore is intentional, in both directions.** Several files are on-disk-but-gitignored (public-repo exclusions) and legitimately live: `wiki/milestones.md` (symlink), `wiki/meta/obsidian-cli.md` (moved 2026-07-26; gitignore rule relocated), `wiki/feedback/hu-anticipated-probes.md`, `wiki/paper/pri-submission.md`, root `CLAUDE.md`, `AGENTS.md`. **Never recommend git-tracking a gitignored file, and never flag a gitignored-but-present page as a broken index row.** `.DS_Store`, `__pycache__/`, `*.zip` are all already covered by `.gitignore` (confirmed) — findings there are untracked-local-only.
- The plan is a **prioritized, tiered checklist** (Tier 1 = safe/mechanical; Tier 2 = judgment call; Tier 3 = MK sign-off). Each item: what / why / exact command or edit / risk / who executes.

## 1. Two-phase split (Opus-5 scope fix — Phase 1 is the FIRST deliverable)

Dimension 7 (results↔models↔claims) alone is a full semantic audit and would degrade a single pass. **Author Phase 1 in full now; stub Phase 2 as a scoped follow-on** in the same file.

- 🟢 **Phase 1 — mechanical hygiene (ship first):** dimensions 1, 2, 4, 5, 6 + symlink health + asset-orphans + `.zip`/stray-root-file triage + orphan-page detection. All statically verifiable, low judgment, high safety.
- 🟡 **Phase 2 — semantic/cross-reference audit (scoped follow-on):** dimension 7 (the 5b drift class) + subtree-consistency for `learn/`, `empathy-geometry/`, `lit/`, `sup/`, `references/`, `_archive/` + duplicate-content detection + stale-orientation flagging (dimension 3). Heavier judgment; runs after Phase 1 has cleaned the link graph it depends on.
- 🔵 **Dimension 8 (log archival)** stays an open MK question, not a deliverable.

## 2. Audit dimensions the plan MUST cover

Each dimension = a section with (a) findings from a real static scan, (b) tiered actions.

1. **Link health.** `obsidian unresolved` currently returns \~30 targets. Triage into: (a) genuinely broken wikilinks (e.g. `calibration-pivot-eli12`, `paper/scaffold`, `stewardship-protocol`); (b) wiki→repo pointers that should be plain markdown links not wikilinks (HARD RULE: wiki→repo fine, repo→wiki banned); (c) intentional forward-links to not-yet-written pages. Prescribe the fix per class.
2. **Index / canon drift.** Cross-check `wiki/index.md` against the on-disk tree. **Enumerate with `find wiki -name '*.md'` (on-disk truth), NOT `git ls-files`** — the four gitignored-but-indexed pages above are valid and must not be flagged. Find: pages on disk missing from index; index rows pointing at moved/renamed/deleted pages.
3. **Stale orientation blocks** *(Phase 2)*. Per rule 4, any state block older than the log tail is historical unless marked "Hot update." Flag un-marked stale blocks in `CLAUDE.md`/`AGENTS.md` — **flag only, do not rewrite** (root edits need the frontier to have actually moved). Verify the two files' Vault-canon blocks are byte-identical; report any divergence. Note both are gitignored/private (don't flag their absence from `git ls-files`).
4. **Naming-convention violations.** Paper dir follows `<method>-<role>` (`wiki/paper/README.md`). Sweep for generic names, mis-prefixed files, figures outside `<code>-figures/`. Confirm results pages follow `<slug>-<date>.md`.
5. **Tracked/untracked hygiene.** Found: `wiki/paper/.DS_Store`, `wiki/paper/cc-figures/__pycache__`, `wiki/paper/.claude/settings.local.json` (gitignored). **No cruft is git-tracked** (confirmed: no tracked `.zip`/`.DS_Store`/`__pycache__`/settings) — so prescribe local `rm` only, **do NOT propose any deletion commit.** The 13 `.zip` Overleaf bundles are **intentional frozen exports the user keeps** — leave them; do not treat as removable.
6. **Append-only integrity.** Static method only: `rg` the `## YYYY-MM-DD` date headers in `log.md`/`history.md` and assert non-decreasing order; **diff nothing against git history.** Recommend the standing discipline, not a rewrite.
7. **Results ↔ models ↔ claims cross-reference** *(Phase 2)*. For each `wiki/results/*.md`: confirm a `history.md` row if it carries a numeric endpoint; a backlink from the relevant `wiki/models/*.md` for per-model results; belief-state changes reflected in `claims.md`. This is the drift class rule 5b exists to catch. Report gaps, don't fill them.
8. **Log-size / navigability** *(MK question)*. `log.md` is 2758 lines. Consider (not mandate) an annual archival split and how to do it without breaking append-only semantics or backlinks.

### Added dimensions (Opus-5 gap fixes)

9. **Subtree coverage** *(Phase 2)*. `learn/` (\~30 files, ELI12/ELI5 style + its own `README.md` + `terminology.md` `/term` anchors) and `empathy-geometry/` (\~15 files, its own `README.md` gate: props-not-proclamations, prereg-before-results) are \~⅓ of the vault and must be covered or explicitly `n-a`. Also sweep `lit/`, `references/`, `sup/`, `_archive/`. Confirm each subtree's own README/index is internally consistent with its files.
10. **Symlink health.** `wiki/milestones.md` is a real symlink into the `furnace-causalities` repo. Verify it resolves (dangling risk if that repo moved); **warn Codex NOT to "fix" it as a broken link or edit through it.**
11. **Asset-orphan detection.** Cross-check the 4 figure dirs (`pri-figures/`, `cc-figures/`, `ace-figures/`, `rpv-figures/`) against what the `.tex` files actually `\includegraphics`/`\input`. Report figures referenced-but-missing and present-but-unreferenced (dimension 4 only checks location, not liveness). This is where the held Tier-4 RPV orphan (`fig1_rpv_vs_confidence.*`) belongs — record it, don't delete it (it's a pending MK call).
12. **Loose wiki-root & transient files.** Bucket one-off root files for "still live / should be filed?" review: `kv-tension-overlay-workorder-2026-07-25.md`, `repo-standalone-workorder-2026-07-25.md`, this work-order, `methodology-llm-wiki.md`, `references-code.md`. Recommend a home or a keep-in-place rationale; **do not move or delete any** (they may be referenced by append-only log entries — superseded ≠ unreferenced).
13. **Orphan-page & duplicate-content detection** *(Phase 2 for dupes; Phase 1 for orphans)*. Run `obsidian backlinks` across all pages (not spot-checks) to find zero-backlink orphans. Flag substantially duplicated content across pages.

## 3. Output shape

`wiki/vault-maintenance-plan.md` with: a one-paragraph scope/guardrail header; the Phase-1 dimension sections (findings + tiered actions); a stubbed Phase-2 section; a consolidated "execution order" (what's safe-first, what needs MK sign-off); an explicit **"out of scope / do NOT touch"** list (sealed 18/20, t0, raw/, archived `pri-*`, append-only bodies, the symlink, the 13 `.zip`s); and the open-questions list from §5.

## 4. Constraints on Codex's own edits (authorship-boundary fix)

- **Codex authors these and nothing else:** (a) the plan file `wiki/vault-maintenance-plan.md`; (b) a new `wiki/index.md` row for it; (c) inside the plan, an *embedded, proposed* `log.md` block (with the full TOTAL-propagation footer) clearly labeled **"PROPOSED — human executor performs the actual append."**
- **Codex does NOT touch `wiki/log.md`.** It is the sharpest merge edge (three live threads append to it; the Obsidian CLI writes outside git's view), and appending is an execution step outside Codex's remit. The human executor performs the real append + full 11-surface propagation.
- **Multi-thread git safety:** stage by explicit path, never `git add -A`. Do not bundle `log.md` with anything else. Author-only commit should contain just the plan file + the index.md row.
- If any finding requires running code to verify, write the exact command marked **"not run by Codex."**

## 5. Open questions for MK (list at top of the plan, do not resolve)

- Log archival: split or leave? (2758 lines)
- Broken-wikilink policy: repair in place vs. create stub pages vs. convert to markdown links?
- Should this plan become a recurring (e.g. monthly) checklist artifact?
- RPV asset orphan `fig1_rpv_vs_confidence.*` (git-tracked, zero `.tex` refs): confirm deletion? (held Tier-4 item.)
