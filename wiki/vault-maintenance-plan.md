# Vault Maintenance Plan

**Audit date:** 2026-07-26

**Status:** PLAN ONLY — no hygiene action in this document has been executed by Codex

**Source work order:** [vault-maintenance-workorder-2026-07-26](vault-maintenance-workorder-2026-07-26.md)

This plan covers mechanical hygiene for the Furnace Obsidian vault without changing research truth. The mandated `find wiki -name '*.md'` enumeration returned **147 on-disk Markdown paths: 146 regular files plus the real `wiki/milestones.md` symlink**. The two root orientation files, `CLAUDE.md` and `AGENTS.md`, were also inspected. `raw/`, `.git/`, project/runtime execution, model work, tests, builds, package scripts, and all hygiene mutations are excluded. Findings respect the canon order: log tail → results pages → research candidates → index → root orientation. Codex authored only this plan and its one `wiki/index.md` row.

## Open questions for MK — do not resolve in this pass

1. **Log archival:** split `wiki/log.md` or leave it intact? The static scan finds 2,759 lines on 2026-07-26.
2. **Broken-wikilink policy:** repair in place, create tombstone/stub pages, or convert eligible pointers to plain Markdown links?
3. **Recurrence:** should this plan become a monthly checklist artifact?
4. **RPV tracked asset orphan:** confirm deletion of `wiki/paper/rpv-figures/fig1_rpv_vs_confidence.{pdf,png}`? The live paper uses the `fig1_forest_*` variant.

## Tier definitions

- **Tier 1 — safe/mechanical:** local cruft cleanup, unambiguous link-target repairs, read-only verification, and documentation changes that do not alter meaning.
- **Tier 2 — judgment:** index policy, tombstones, legacy naming exceptions, root-file filing, append-date conventions, and alternate-render retention.
- **Tier 3 — MK sign-off:** deletion of tracked assets, log archival, any change near frozen/sealed material, and policy decisions with lasting graph or provenance effects.

Every command below is a future executor command and is explicitly **not run by Codex**.

---

# Phase 1 — Mechanical hygiene

## 1. Link health

### Findings

The Obsidian CLI could not access the vault because the Obsidian app was not running. The attempted read-only command was `obsidian unresolved`; it returned only the app-availability error. Therefore the work order's approximate “30 unresolved targets” was not treated as verified output.

A static scan of all 146 regular `wiki/**/*.md` files found:

- **11 unresolved wikilink occurrences across 8 unique targets** under filename/path resolution.
- **46 broken local Markdown source→target pairs.** Most are legacy date-prefix drift in `learn/`; the remainder includes append-only historical references, archived PRI links, two external `.claude/plans/` pointers, two incorrect index targets, and repo-code pointers written as wikilinks.
- No live target was inferred from similarity alone; each proposed replacement below maps to a real on-disk page or is held for judgment.

#### A. Unambiguous live-page filename drift

These real pages acquired date prefixes while inbound Markdown links retained the old basename:

| Stale target | Real target |
|---|---|
| `null-space-eli12.md` | `260419-null-space-eli12.md` |
| `spectral-test-eli12.md` | `260419-spectral-test-eli12.md` |
| `harp-vs-pri-eli12.md` | `260420-harp-vs-pri-eli12.md` |
| `where-we-are-eli12.md` | `260423-where-we-are-eli12.md` |
| `jn-correction-eli12.md` | `260425-jn-correction-eli12.md` |
| `model-architecture-families-eli12.md` | `260425-model-architecture-families-eli12.md` |
| `fisher-square-root-eli12.md` | `260426-fisher-square-root-eli12.md` |
| `v3-pipeline-eli12.md` | `260428-v3-pipeline-eli12.md` |
| `llm-pipeline-eli12.md` | `260507-llm-pipeline-eli12.md` |
| `chat-template-gap-eli12.md` | `260511-chat-template-gap-eli12.md` |
| `attention-sinks-and-heads-eli12.md` | `260515-attention-sinks-and-heads-eli12.md` |
| `calibration-pivot-eli12.md` | `260515-calibration-pivot-eli12.md` |
| `methods-catalog-eli12.md` | `260515-methods-catalog-eli12.md` |

Two directory moves also have clear replacements:

- `../papers/external.md` → `../lit/external.md` where the source is in `wiki/learn/` or `wiki/feedback/`.
- `Candidate-10-Shadow-Ambiguity-Deconstruction.md` in `wiki/index.md` → `learn/Candidate-10-Shadow-Ambiguity-Deconstruction.md`.

Archived `wiki/paper/pri-*` files contain stale learn links and `figures/...` image paths. They are reported, but the archived PRI files are off-limits and receive no edit prescription.

#### B. Wiki→repo pointers currently expressed as wikilinks

These are not vault pages and should become plain Markdown links after the executor resolves the exact repository-relative target:

- `wiki/results/v4-sealed-2026-05-26.md` → `[[PRI_V4_PRE_REGISTRATION_PLAN]]`
- `wiki/results/t0-residual-pilot-2026-05-28.md` → `[[pilot_t0_residual.py]]` and `[[pri_calibrator]]`
- `wiki/results/_synthesis-scratch.md` → `[[../../CLAUDE|CLAUDE.md]]`

The last item has an unambiguous local replacement: `[CLAUDE.md](../../CLAUDE.md)`. The first three require the executor to bind the exact file location in the external repository before editing; do not create vault stubs for code.

#### C. Append-only historical links

These unresolved references occur in `wiki/log.md`, which must not be edited:

- `[[stewardship-protocol]]` — the page was intentionally removed on 2026-07-09 after its rules moved into the root orientation files.
- `[[lit/prediction-rupture-at-commitment]]` — the page was intentionally deleted on 2026-07-09 after canonical material was retained elsewhere.
- `[paper/scaffold](paper/scaffold.md)` and `[pri-v3-plan](pri-v3-plan.md)` — historical pre-reorganization paths.

Repair, if desired, must use a present-day tombstone/redirect page or an accepted-unresolved exception list. Never rewrite the historical log lines.

#### D. Missing or forward companion

`learn/260605-q-pos-memory-salience-eli12.md` is referenced by `wiki/index.md`, `wiki/learn/README.md`, and three places in `wiki/results/qpos-golden-eval-plan.md`, but no page exists on disk. The references describe substantive prior work, so this is not safe to delete mechanically. It needs a Tier-2 decision: author the intended page, restore it from known provenance, or relabel all live references as a forward placeholder.

### Tiered actions

| Tier | What / exact edit or command | Why | Risk | Executor |
|---|---|---|---|---|
| 1 | Start Obsidian, then run `obsidian unresolved verbose`. **Not run by Codex.** | Obtain the application-indexed unresolved set and compare it with the static set above. | None; read-only. | Claude Code or MK |
| 1 | Apply the 13 exact date-prefix replacements and the two directory-move replacements listed above, excluding append-only and archived `pri-*` files. **Not run by Codex.** | Restores real existing targets without semantic change. | Low; link text and claims remain unchanged. | Claude Code |
| 1 | Replace `[[../../CLAUDE\|CLAUDE.md]]` with `[CLAUDE.md](../../CLAUDE.md)` in `_synthesis-scratch.md`. **Not run by Codex.** | Makes a wiki→repo/root pointer explicit and valid. | Low; scratch page only. | Claude Code |
| 1 | Resolve code targets with `find /Users/msrk/Documents/PRI_at_commitment -name 'PRI_V4_PRE_REGISTRATION_PLAN.md' -o -name 'pilot_t0_residual.py' -o -name 'pri_calibrator.py'`. Then convert the three repo-code wikilinks to plain Markdown links. **Not run by Codex.** | Enforces wiki→repo fine / repo→wiki banned while avoiding invented paths. | Low after path verification; do not alter surrounding result prose. | Claude Code |
| 2 | Decide whether `stewardship-protocol`, deleted lit page, and old paper paths receive small tombstone pages or enter a documented accepted-unresolved list. **No log rewrite.** | Append-only history otherwise remains permanently unresolved. | Medium; stubs can clutter the graph, while exceptions reduce “zero unresolved” as a useful invariant. | MK |
| 2 | Decide the fate of the missing Q-POS learn page: author from provenance, restore, or explicitly mark forward. | Current live pages describe it as if it exists. | Medium; authoring from memory could invent research content. | MK, then Claude Code |
| 3 | Freeze the vault-wide broken-link policy before bulk repair. | Determines whether historical paths are represented by redirects, exceptions, or current-target edits. | Policy-level graph effect. | MK |

## 2. Index and canon drift

### Findings

The cross-check used on-disk truth from `find wiki -name '*.md'`, not `git ls-files`. The valid gitignored pages were treated as real pages; none was called broken because it is absent from Git tracking.

The current index has **20 on-disk regular pages without a direct row/target**, before adding this plan's authorized row:

- **Models / model index (13):** `models/README.md`, `mistral-nemo-12b.md`, `qwen-3-1.7b.md`, `phi-4-mini.md`, `gemma-4-12b.md`, `deepseek-r1-distill-qwen-7b.md`, `llama-3.3-70b.md`, `dead-runs.md`, `qwen-2.5-32b.md`, `qwen-2.5-14b.md`, `gemma-3-12b.md`, `llama-3.1-8b.md`, `qwen-2.5-72b.md`.
- **Other content (6):** `paper/cc-benchmark-proposal.md`, `learn/Candidate-10-Shadow-Ambiguity-Deconstruction.md`, `lit/predictive-rupture-hallucination-detection.md`, `tooling-obsidian-cli.md`, `results/overnight-2026-04-26.md`, and `vault-maintenance-workorder-2026-07-26.md`.
- **Conventional self-page (1):** `index.md` itself has no self-row; this is not necessarily drift.

Two current index targets do not resolve:

1. `Candidate-10-Shadow-Ambiguity-Deconstruction.md` points to the old vault-root location; the page is now under `learn/`.
2. `learn/260605-q-pos-memory-salience-eli12.md` is absent on disk.

`lit/predictive-rupture-hallucination-detection.md` was intentionally pruned from the top-level index on 2026-07-09, so its omission is a policy exception candidate, not an automatic error. Similarly, a selective navigation index may intentionally omit model pages, while an exhaustive inventory index may not. The vault has no explicit statement resolving that policy.

This authorship pass adds only the authorized row for `vault-maintenance-plan.md`; it does not reconcile any pre-existing row.

### Tiered actions

| Tier | What / exact edit or command | Why | Risk | Executor |
|---|---|---|---|---|
| 1 | Fix the Candidate-10 row target to `learn/Candidate-10-Shadow-Ambiguity-Deconstruction.md`. **Not run by Codex.** | It is a confirmed moved page, not a policy question. | Low. | Claude Code |
| 1 | Re-run the same static reconciliation after link repair: for every `find wiki -name '*.md'` result, require either an index target or an explicit exception. **Not run by Codex.** | Prevents ignored-but-valid pages from disappearing from the audit universe. | None; read-only until reviewed. | Claude Code |
| 2 | Declare `wiki/index.md` either exhaustive or curated. If exhaustive, add rows for the 19 pre-existing non-self omissions above, except any explicitly documented exception. If curated, add an “Index coverage policy / exceptions” block. **Not run by Codex.** | Without a policy, “missing from index” cannot be cleanly distinguished from intentional omission. | Medium; bulk rows affect navigation and maintenance load. | MK, then Claude Code |
| 2 | Resolve the missing Q-POS target consistently with §1; do not remove its index reference independently of the learn/result references. | Prevents a partial repair that leaves canon surfaces disagreeing. | Medium. | MK, then Claude Code |
| 3 | If the index is made exhaustive, approve whether transient work orders remain first-class rows after completion or move to an archive index. | This sets long-term provenance and clutter policy. | Policy-level. | MK |

## 3. Naming conventions

### Findings

Paper-folder compliance is strong:

- All substantive paper files use a method prefix: `pri-*`, `ace-*`, `rpv-*`, or `cc-*`.
- `README.md` is the intentional rule-sheet exception.
- All image assets are inside the four correct directories: `pri-figures/`, `ace-figures/`, `rpv-figures/`, and `cc-figures/`.
- The 13 `.zip` names are method-prefixed frozen exports and are intentional keeps.

The results directory has 11 filenames that do not match `<slug>-YYYY-MM-DD.md`:

- Reserved/live ledgers: `summary.md`, `history.md`
- Explicit scratch: `_synthesis-scratch.md`
- Legacy/pre-convention result or plan pages: `e22-direction-depth.md`, `v3.1-replicate.md`, `sup-spectral-band.md`, `qpos-golden-eval-plan.md`, `v3-main-run.md`, `e23-option-c.md`, `v3.2-results.md`, `v3.2-amendment.md`

These are naming exceptions, not safe rename candidates: they have many inbound links, and several belong to the historical PRI era. No generic new result filename was found in the recent dated result set.

### Tiered actions

| Tier | What / exact edit or command | Why | Risk | Executor |
|---|---|---|---|---|
| 1 | Add a documented results-naming exception list for `summary.md`, `history.md`, `_synthesis-scratch.md`, and the eight legacy pages. **Not run by Codex.** | Makes the rule auditable without breaking established links. | Low. | Claude Code |
| 1 | Keep the paper naming rule unchanged; no figure relocation is needed. | Static scan found full location compliance. | None. | — |
| 2 | Decide whether future plans in `results/` must also carry dates; apply only prospectively. | `qpos-golden-eval-plan.md` shows the current ambiguity. | Low if prospective; high if retroactive. | MK |
| 3 | Do not rename archived/historical PRI result pages merely for convention. Any such migration requires MK sign-off plus redirect/backlink design. | Renaming creates widespread link and provenance churn. | High. | MK |

## 4. Tracked, untracked, and ignored hygiene

### Findings

Confirmed local ignored items:

- `wiki/paper/.DS_Store`
- `wiki/paper/cc-figures/__pycache__/`
- `wiki/paper/.claude/settings.local.json`
- 13 `.zip` Overleaf bundles

`git ls-files` returned no tracked `.zip`, `.DS_Store`, `__pycache__`, or local `.claude/settings.local.json` paths. `git check-ignore -v` confirms the ignore rules. Therefore there is **no deletion commit to make**.

The 13 `.zip` files are intentional frozen exports and remain untouched. The local `.claude/settings.local.json` is also an intentional ignored local setting unless its owner says otherwise.

At audit time, `git ls-files --others --exclude-standard` returned only the work-order source `wiki/vault-maintenance-workorder-2026-07-26.md`. After authorship, this plan is also a new review file; neither fact licenses broad staging.

### Tiered actions

| Tier | What / exact edit or command | Why | Risk | Executor |
|---|---|---|---|---|
| 1 | Run `rm wiki/paper/.DS_Store` and `rm -r wiki/paper/cc-figures/__pycache__`. **Not run by Codex. Local cleanup only.** | Removes regenerable OS/Python cruft. | Low; ignored and untracked. | Claude Code or MK |
| 1 | Leave `wiki/paper/.claude/settings.local.json` and all 13 `.zip` bundles in place. | They are intentional local state/frozen exports. | None. | — |
| 1 | Verify no tracked cruft with `git ls-files 'wiki/**/*.zip' 'wiki/**/.DS_Store' 'wiki/**/__pycache__/**' 'wiki/**/.claude/settings.local.json'`. Expected output: empty. **Not run by Codex after cleanup.** | Guards against accidentally converting local cleanup into a deletion commit. | None; read-only. | Claude Code |
| 1 | Stage only with `git add wiki/vault-maintenance-plan.md wiki/index.md`. Never use `git add -A`; never bundle `wiki/log.md`. **Not run by Codex.** | Preserves multi-thread work and the authorship boundary. | Low if explicit. | Human reviewer |

## 5. Append-only integrity

### Findings

The required check was static only: `rg` over `## YYYY-MM-DD` / `## [YYYY-MM-DD]` headers. No Git-history diff was used.

- `wiki/log.md`: date headers are non-decreasing through the 2026-07-26 tail. Current length is **2,759 lines**, one more than the work order's 2,758-line snapshot.
- `wiki/results/history.md`: the static structure contains an explicitly labeled appended backfill, but literal event-date headers are **not globally non-decreasing**. The `2026-07-25 — BACKFILL` section carries run-dated rows from 2026-06-11 through 2026-07-22, followed later by a `2026-06-09, scored 2026-07-25` row. This is transparent backfill provenance, not evidence of rewriting; the permitted static check cannot prove historical file identity, and a simple event-date monotonicity assertion is the wrong invariant for existing backfills.
- The latest 2026-07-26 paper-cleanup entry in `wiki/log.md` does not contain the rule-5b eleven-surface `TOTAL propagation` footer. It must not be edited in place. A later corrective append is the only permitted repair if MK wants one.

### Tiered actions

| Tier | What / exact edit or command | Why | Risk | Executor |
|---|---|---|---|---|
| 1 | Standing read-only check: `rg -n '^## \\[?[0-9]{4}-[0-9]{2}-[0-9]{2}' wiki/log.md wiki/results/history.md`. **Not run by Codex after this plan.** | Detects ordering anomalies without diffing or rewriting append-only files. | None. | Claude Code |
| 1 | Require every future log append to include the full eleven-surface footer before append. | Prevents recurrence of the current tail omission. | Low. | All human/executor stewards |
| 2 | Define history ordering as **append date first, run/scored date in the title/body** for future backfills. Do not normalize old headers. | Preserves provenance while making future static monotonicity meaningful. | Medium; convention change. | MK |
| 2 | If correcting the missing 2026-07-26 footer, append a new correction entry; never edit the existing entry. | Honors append-only integrity. | Low if append-only; minor log noise. | MK or Claude Code |
| 3 | Decide log archival separately; no split is prescribed here. | Archival changes navigation and append semantics. | High/provenance-sensitive. | MK |

## 6. Symlink health

### Findings

`wiki/milestones.md` is a real symlink. Both `find wiki/milestones.md -type l -print` and `find -L wiki/milestones.md -type f -print` returned the path, so it currently resolves and is not dangling. It is intentionally gitignored and index-visible.

The symlink is off-limits: do not edit through it, replace it with a regular file, “repair” it as an unresolved link, or recommend tracking it in this repository.

### Tiered actions

| Tier | What / exact edit or command | Why | Risk | Executor |
|---|---|---|---|---|
| 1 | Periodically run `find wiki/milestones.md -type l -print` and `find -L wiki/milestones.md -type f -print`. **Not run by Codex after this audit.** | First proves symlink identity; second proves the target resolves. | None; read-only. | Claude Code |
| 3 | If it ever dangles, stop and ask MK to restore the external `furnace-causalities` location. Do not replace or edit the vault path. | The target is a separate public repository with its own commit/push workflow. | High if mishandled. | MK |

## 7. Paper asset liveness

### Findings

Static extraction of every `\includegraphics` and `\input` in the five `.tex` manuscripts found:

- PRI: 6 referenced figures
- ACE: 3 referenced figures
- CC main: 5 referenced figures
- CC extension: 3 referenced figures
- RPV: 3 referenced figures plus `table1_summary.tex`

**Every referenced asset exists. No referenced-but-missing asset was found.**

Present but not referenced by any `.tex`:

- Held tracked orphan: `rpv-figures/fig1_rpv_vs_confidence.pdf` and `.png`
- Tracked alternate PNG renders for live PDF figures: `fig1_forest_rpv_vs_confidence.png`, `fig2_redundancy_ladder.png`, `fig3_collapse_complement.png`

The three alternate PNGs may be intentional preview/web assets; zero LaTeX references alone is not enough to delete them. `cc-figures/make_figures.py` is a builder, not an orphan asset. Its ignored `__pycache__` is covered by §4.

### Tiered actions

| Tier | What / exact edit or command | Why | Risk | Executor |
|---|---|---|---|---|
| 1 | Retain all referenced assets; no missing-asset repair is needed. | All 21 references/inputs resolve. | None. | — |
| 2 | Decide and document whether tracked PNG alternates are web/preview deliverables. If yes, add that role to `wiki/paper/README.md`; if no, propose them separately for MK review. | Avoids treating format alternatives as accidental duplicates. | Medium; possible external consumers. | MK or paper owner |
| 3 | Decide whether to delete only `fig1_rpv_vs_confidence.{pdf,png}`. If approved, use `git rm wiki/paper/rpv-figures/fig1_rpv_vs_confidence.pdf wiki/paper/rpv-figures/fig1_rpv_vs_confidence.png`. **Not run by Codex.** | They are tracked, have zero `.tex` references, and are superseded by the forest variant. | Medium; committed deletion, possible non-LaTeX consumer. | MK sign-off, then Claude Code |

## 8. Loose wiki-root and transient-file triage

### Findings and recommended homes

| File | Current reading | Recommendation |
|---|---|---|
| `kv-tension-overlay-workorder-2026-07-25.md` | Active, tracked, indexed, linked from the append-only log | Keep at root while executable work is open. After closure, consider `_archive/workorders/` only under the chosen redirect policy. |
| `repo-standalone-workorder-2026-07-25.md` | Active, tracked, indexed, frozen MK decisions, linked from the append-only log | Keep at root until the packaging work is attested. Archive only after closure and with link handling. |
| `vault-maintenance-workorder-2026-07-26.md` | Untracked source order for this plan; it was the only zero-inbound static orphan before this plan linked it | Keep beside the plan through review for provenance. Decide later whether completed work orders live under `_archive/workorders/`. |
| `methodology-llm-wiki.md` | Canonical live methodology, indexed and linked from overview/log | Keep at wiki root. It is a vault-wide orientation page, not transient. |
| `references-code.md` | Canonical repo map location, broadly linked, but its “t0 living lab” description is stale against the 2026-07-25 log tail | Keep at wiki root; schedule semantic correction in Phase 2. Do not move it while stale. |

No file is safe to move solely because a work order is superseded or complete: append-only log references remain part of provenance.

### Tiered actions

| Tier | What / exact edit or command | Why | Risk | Executor |
|---|---|---|---|---|
| 1 | Keep all five files in place during Phase 1. | Avoids link churn and accidental loss of live work orders. | None. | — |
| 2 | Define a completed-work-order home, preferably `wiki/_archive/workorders/`, plus the redirect/exception behavior before moving anything. **Not run by Codex.** | Gives future work orders a predictable lifecycle. | Medium; append-only backlinks cannot be rewritten. | MK |
| 2 | Correct `references-code.md` semantically in Phase 2 using the log tail as authority; retain its root path. | The location is canonical, but its t0 role description is outdated. | Medium; claim/orientation wording needs careful source-of-truth review. | Claude Code after Phase-2 audit |

## 9. Orphan-page detection

### Findings

Because Obsidian was unavailable, exact backlink semantics could not be confirmed. A static all-page inbound-link approximation checked every one of the 147 on-disk Markdown paths by both vault-relative path and basename. It found one zero-inbound page before authorship:

- `wiki/vault-maintenance-workorder-2026-07-26.md`

This plan now links that work order, so the static zero-inbound condition is removed by the authorized deliverable itself. This is not a substitute for Obsidian's graph index; aliases, headings, embeds, and ignored pages may differ.

### Tiered actions

| Tier | What / exact edit or command | Why | Risk | Executor |
|---|---|---|---|---|
| 1 | With Obsidian running, execute `while IFS= read -r f; do obsidian backlinks file="${f#wiki/}"; done < <(find wiki -name '*.md' -print)`. **Not run by Codex.** | Satisfies the work order's all-page backlink requirement using Obsidian semantics. | None; read-only. | Claude Code |
| 1 | Re-run `obsidian unresolved verbose` after Tier-1 link repairs. **Not run by Codex.** | Confirms whether the graph is mechanically clean. | None. | Claude Code |
| 2 | Treat zero-backlink pages as review candidates, never automatic deletions; classify as root entry point, ledger, work order, forward page, archive, or genuine orphan. | Some valid pages are intentionally reached from root orientation rather than wiki pages. | Medium if automated. | Claude Code + MK for deletions |

---

# Phase 2 — Semantic and cross-reference follow-on (stub only)

Phase 2 starts only after Phase-1 link repair and Obsidian graph confirmation. It reports gaps but does not silently fill them. Its audit universe remains the same, and canon order remains binding.

## A. Results ↔ history ↔ models ↔ claims (dimension 7 / rule 5b)

Scope every `wiki/results/*.md` page:

1. If it carries a measured numeric endpoint, locate the matching append-only `history.md` row.
2. If it is per-model, confirm the relevant `wiki/models/*.md` pages contain a canonical backlink and scoped reading.
3. If it changed a belief state, confirm the matching `claims.md` tag/status.
4. Confirm index/summary/paper/root propagation only where each surface's trigger fired.
5. Report omissions; do not backfill until reviewed.

Read-only work order, **not run by Codex**:

```text
rg -n 'AUROC|CI[_ -]?lo|PASS|FAIL|[0-9]+/[0-9]+' wiki/results -g '*.md'
rg -n 'results/' wiki/results/history.md wiki/models wiki/claims.md -g '*.md'
```

Deliverable: a per-result matrix with `history`, `models`, and `claims` columns marked `present`, `n-a: reason`, or `gap`.

## B. Subtree consistency (dimension 9)

Static Phase-1 counts establish the scope:

- `learn/`: 30 pages — reconcile `README.md`, terminology anchors, date-prefixed filenames, and `/term` navigation.
- `empathy-geometry/`: 15 pages — reconcile its README gate, props-not-proclamations rule, prereg-before-results status, and internal phase labels.
- `lit/`: 3 pages
- `references/`: 3 pages
- `sup/`: 2 pages
- `_archive/`: 2 pages

For each subtree, compare its README/index inventory with `find <subtree> -name '*.md'`; mark every file listed, intentionally omitted, or stale. Do not turn design notes into validated claims.

## C. Root orientation staleness and parity (dimension 3)

Initial flags for the semantic pass:

- `AGENTS.md` still has a 2026-06-07 **“Current state for Codex”** block saying t0 is a living morphology lab, contradicted by the 2026-07-25 hot update that re-seals t0 as archive-only.
- Both files' unqualified `Validated, Falsified, Open` sections are inherited from the old PRI-era digest and require a current-vs-historical label review.
- `references-code.md` repeats the stale living-lab description.
- The Vault-canon bodies match by inspection, but the blocks are **not byte-identical as written** because their heading parentheticals reciprocally name the other file (`mirrors CLAUDE.md` vs `mirrors AGENTS.md`). Phase 2 should decide whether “byte-identical” excludes that heading or should use a neutral identical heading. No root edit occurs unless the active frontier/source evidence warrants it.
- Both root files are valid gitignored/private orientation files; absence from `git ls-files` is not a defect.

Flag only; do not rewrite during Phase 1.

## D. Duplicate-content detection (dimension 13)

Perform a paragraph-level semantic comparison after link normalization, focusing on:

- result page vs `summary.md` vs claims ledger (legitimate propagation vs divergent duplicate);
- learn explainer vs rigorous result page (different roles);
- root hot updates duplicated across `CLAUDE.md` and `AGENTS.md` (intentional);
- work-order copies or superseded scaffolds (possible archive candidates);
- `lit/` historical pointers vs result/claim canon.

Substantial overlap is a review flag, never an automatic merge. Archived `pri-*`, append-only bodies, and sealed text remain off-limits.

---

# Dimension 8 — Log navigability (open MK question only)

`wiki/log.md` is 2,759 lines. An annual split could improve navigation, but moving old entries would conflict with the present append-only model and could break headings/backlinks. No archival design is prescribed until MK chooses:

- leave one append-only file;
- freeze the current file and begin a new yearly file without moving history; or
- create read-only annual indexes that link into the unchanged monolith.

Any accepted design must preserve old anchors, never reorder historical entries, and define which file receives the canonical tail.

---

# Consolidated execution order

1. **Read-only confirmation:** start Obsidian; run `obsidian unresolved verbose` and all-page backlinks. Compare with this static inventory.
2. **Tier-1 local cleanup:** remove only `.DS_Store` and `__pycache__`; retain settings and all 13 `.zip` bundles.
3. **Tier-1 link repair:** apply exact live-page filename mappings and plain Markdown repo/root pointers; do not touch log or archived PRI.
4. **Tier-1 verification:** repeat unresolved, backlink, index/tree, symlink, tracked-cruft, append-header, and LaTeX asset scans.
5. **Tier-2 decisions:** index exhaustiveness, Q-POS page, tombstones/exceptions, history backfill convention, PNG alternates, completed-work-order home.
6. **Tier-3 MK decisions:** RPV orphan deletion and log archival.
7. **Phase 2:** run the results/models/claims matrix, subtree consistency, stale orientation, and duplicate-content audit.
8. **Authorship review only:** stage `wiki/vault-maintenance-plan.md` and `wiki/index.md` by explicit path; never stage `wiki/log.md` with them.

# Out of scope — do not touch

- The sealed Commit-Confluence 18/20 result, denominator, scope, or artifacts
- `t0-morphology-furnace` byte identity or its sealed root modules
- `raw/`
- `.git/` internals
- Archived `wiki/paper/pri-*` files, even where stale links are reported
- Bodies of `wiki/log.md` and `wiki/results/history.md`; append-only means no rewrite, reorder, or historical diff
- The `wiki/milestones.md` symlink or its target through this vault
- All 13 `.zip` Overleaf bundles
- Any research number, verdict, claim, pre-registration, model output, or runtime artifact

# Additional questions the work order did not fully anticipate

1. Should `wiki/index.md` be exhaustive or curated? The answer controls whether the 19 pre-existing non-self omissions are defects or documented exceptions.
2. Should `history.md` monotonicity mean append date or experiment date when transparent backfills exist?
3. Are the three tracked RPV PNG counterparts intentional web/preview assets, even though the LaTeX uses their PDF versions?
4. The mandated `find` count is 147 paths because it includes the milestones symlink; should future audits report “146 regular pages + 1 symlink” as the standard denominator?
5. Obsidian was not running. Should a maintenance pass be considered complete only after an executor supplies the application-indexed unresolved/backlink artifacts?

---

## PROPOSED — human executor performs the actual append

The block below is proposed text for `wiki/log.md`. Codex did **not** append it.

```markdown
## 2026-07-26 — Vault maintenance Phase-1 plan authored from full static audit (DOC HYGIENE / PLAN ONLY)

Authored `wiki/vault-maintenance-plan.md` from the approved work order. Audit universe: 146 regular `wiki/**/*.md` files + the real `wiki/milestones.md` symlink, plus root `CLAUDE.md` / `AGENTS.md`; `raw/` and `.git/` excluded. Findings are plan-only: link/index drift, legacy naming exceptions, local ignored cruft, append-only ordering/footers, resolving milestones symlink, LaTeX asset liveness, loose-root triage, and static orphan coverage. No hygiene action, research edit, runtime code, test, harness, model call, build, package script, agent spawn, deletion, move, or commit was performed. Obsidian CLI confirmation remains executor-owned because the app was not running; exact read-only commands are in the plan. Phase 2 is scoped but not performed.

**TOTAL propagation:** (1) results/<slug> — n-a: documentation-maintenance plan only, no experimental result; (2) results/history.md — n-a: no numeric endpoint and append-only body untouched; (3) claims.md — n-a: no belief-state change; (4) research-candidates.md — n-a: no candidate status moved; (5) results/summary.md — n-a: no run to summarize; (6) models/<model>.md — n-a: not a per-model result; (7) index.md — **updated** (new vault-maintenance-plan row only); (8) paper — n-a: no manuscript or paper claim changed; (9) CLAUDE.md + AGENTS.md — n-a: active frontier unchanged, Phase-2 staleness flags only; (10) milestones.md — n-a: internal maintenance plan, not milestone-worthy, symlink untouched; (11) log.md — **updated** (this human-executed append).
```
