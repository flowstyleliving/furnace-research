# Work order — `claims.md` cleanup: a belief ledger any researcher can read

_Authored 2026-08-17 by Claude (steward). **v2 (same day) — revised after Codex adversarial audit (RED as written → YELLOW after must-fixes; §9).** Status: **B0+B1 DONE 2026-08-18 (MK "go") → at CHECKPOINT 1 (B2): awaiting MK approval of the tag grammar + the manifest's mappings and the drift/copy-first decisions listed in [[workorders/claims-ledger-manifest-2026-08-18]] before any text change.** Executed so far: Phase A (RPV single home), B0 reconciliation, B1 inventory (snapshot refreshed to include a parallel-session §12 row)._

## 1. Goal

Rewrite `wiki/claims.md` so that an outside researcher — no vault history, no knowledge of our internal codes — can read it top to bottom in ~10 minutes and come away knowing **what Furnace believes now, at what confidence, and where the evidence lives**. Preserve every claim, every belief state, and every scope qualifier; lose the accretion. **This is a readability pass, not a re-verdict** — the audit's central catch was that v1 of this plan quietly contained two re-verdicts (D3, T3); v2 removes them.

## 2. Diagnosis (v2 — re-measured on the post-Phase-A file: 240 lines, ~66 KB)

| # | Symptom | Evidence |
|---|---|---|
| D1 | **Tag vocabulary has exploded.** Header declares 7 tags; body uses ≈25 distinct leading-bracket forms, plus inline history annotations (`[EXTENDED …]`, `[HARDENED …]`, `[SUPERSEDED-IN-PART …]`, `[SHARPENED …]`) and instrument names (`[R4]`) that look like tags. | `[PRIMARY-PASS / rank 1]`, `[PARTIAL VALIDATED]`, `[HYPOTHESIS][V3.1-READY]`, `[OPEN][FUTURE-V4]`, `[SEALED CONFIRMED + PARTIAL TRANSFER]`, `[CORRECTED — NO PROMOTE]`, `[PILOT RUN — NO-PROMOTE]`, `[REGISTERED — WEAKEN, 2026-08-17]`, `[VALIDATED beats-confidence / RESOLVED H1 NO-GO … / OPEN …]`, `[VALIDATED — framing rule]`, `[VALIDATED — plumbing only]`, `[OPEN — ⟨MK⟩ AMENDMENT PENDING]`, `[DESIGN — instrument, pre-run]`. |
| D2 | **Claims are non-atomic.** The real defect is not word count but that single bullets carry *several propositions in different belief states* (RPV: validated + resolved + open in one tag; depth entries: registered verdict + descriptive + superseded-in-part; partner-echo: confirmed + new + caveats + mechanism hypothesis). Verbosity is the symptom. | §10 RPV line; §11.2 depth entries; §12 lines ~233/235/236 (the oversized ones). |
| D3 | **§3 / §4 / §6 are 2026-04 proposals presented as live, but their specific tests were NEVER RUN.** §3's logistic `P_fail` fit-on-puzzles→apply-unchanged-to-HaluEval was never executed (the calibrator's deployability warnings in §1.5 are the *spiritual* successor, not the same test); §4's null-space→HaluEval transfer was never run as specified (BENCH tested a multi-signal dispatcher — per-model calibration passed, fixed-cell/fixed-sign transfer failed); §6's "not yet run" hypotheses cite tiny-slice wins. **v1 of this plan wrongly proposed to mark §3 "REALIZED" and §4 "ANSWERED" — that would be a silent re-verdict.** Correct label: *historical proposal; original test not run; related later work at …*. | `claims.md` §3, §4, §6; [[results/bench-a2-signflip-2026-07-22]]. |
| D4 | **Section scope statements contradict their contents.** §12 opens "deliberately empty of validated claims" then holds `[RESOLVED — harness infrastructure]` and `[VALIDATED — plumbing only]`; §6 is titled "not yet run" but cites commits with wins. | `claims.md` lines 223/229/231, 138. |
| D5 | **No entry point for an outsider.** No "what we believe now" digest, no glossary of internal codes (PRI/v3, ACE/v4, RPV/#10, CC, BENCH, DC, E18/E_A1/E5/P3, sealed vs registered vs descriptive, byte-comparable vs torch/Modal vs MLX vs mlx-vlm lanes, "orphan", `js_no_bos`, MK), no explanation of the pre-registration discipline that gives the tags meaning. |
| D6 | **§0 is out of date.** States the v3 null-space hypothesis as *the* core; the program's current theses live in §11 with no top-level statement. |
| D7 | **Two header narratives conflict** (2026-07-25 vault-wide scope note vs 2026-04-15 "§1 know / §2 claim / §3–4 plan / §5 motivation / §8 superseded" note that no longer describes the file). |
| D8 | **Evidence pointers are non-uniform and often absent, including on short claims.** Many §1 and §6 lines have no claim-local pointer; §1.5's "see §9" points at a section that only holds the autoresearch retirement (broken pointer). |
| D9 | **"No universal cell" is stated unqualified in §11.1** while §11.3 explicitly warns not to infer "no informative cell exists." An outsider reading §11.1 alone takes away the wrong thing. |
| D10 | **Comparability lanes are easy to conflate** — cross-model claims often carry the lane only in prose or not at all. |

## 3. Design principles (pins)

- P1 **Belief state ≠ annotation ≠ history.** Exactly one *leading* tag per claim from the closed set `[VALIDATED]` `[FALSIFIED]` `[OPEN]` `[HYPOTHESIS]` `[RESOLVED]` `[SHIFTED]` `[SUPERSEDED]`, followed by a **typed qualifier block** with fixed fields, e.g. `[VALIDATED] (evidence=registered · verdict=8/12 WEAKEN · scope=torch-lane, 6 held-out models · date=2026-08-17)`. Fields: `evidence ∈ {sealed, registered, descriptive, pilot, design}` · `verdict` (the endpoint as written) · `disposition ∈ {—, no-promote, replication-owed, amendment-pending}` · `scope` (lane + cohort) · `date`. History annotations become indented `↳` sub-lines with their own date, never bracket-tags. Decision rules for the four easily-confused states go in the front matter: **FALSIFIED** = a pre-registered or explicitly stated prediction failed its own bar; **RESOLVED** = an open question closed *without* a bar (screen, audit, closure) — includes no-promote; **SHIFTED** = a prior expectation changed shape but the question is still live; **SUPERSEDED** = the statement itself was replaced by a later, better statement (the old one is kept for history).
- P2 **One claim = one proposition = one leading tag + one evidence pointer.** Compound entries are **split by state** first (RPV → 3 claims; `[REGISTERED — WEAKEN]` → `[VALIDATED] (registered · 8/12 WEAKEN)` + `[OPEN]` for the missed bar, never a bare `[FALSIFIED]`, which would erase the positive endpoint; `[SEALED CONFIRMED + PARTIAL TRANSFER]` → 2 claims; `[CORRECTED — NO PROMOTE]` → `[RESOLVED] (disposition=no-promote)` + the corrected-history sub-line; `[SHIFTED]` → current-state line + historical-transition sub-line). Then trimmed to ≤ ~40 words + pointer.
- P3 **Nothing is deleted; nothing is re-verdicted.** Every claim maps old→new by a **stable claim ID** (`C-<section>-<n>`, assigned in the inventory), with a manifest column for *authoritative source* (log date / result page) — splits allowed if documented, merges forbidden. Trimmed text must be verified present on the linked page **before** the trim (copy-then-verify-then-trim); where the only pointer is a work order or nothing (e.g. one human-dyad dialogue survives only as quoted text), the text is copied to the appropriate result/memo page first. Pre-cleanup snapshot: `wiki/_archive/claims-2026-08-17-pre-cleanup.md`, byte-identical to the post-Phase-A file.
- P4 **Numbers stay put, per claim.** No numeric endpoint changes; checked *per claim ID* (value + unit + denominator + scope), not as a bag-of-numbers diff.
- P5 **Stable section numbers AND stable sub-section numbers.** §0–§12 keep their numbers; **§11.2 keeps the depth entries** (log entries cite "§11.2" — 5 hits) — a depth sub-heading is added *inside* §11.2 as a navigational anchor; no §11.4 move. Front matter goes *above* §0. Any retitle keeps the old title in a `(formerly …)` parenthetical for one release.
- P6 **Newest belief wins visually.** Within a section the current-state line comes first; history is `↳`-indented beneath or linked, never interleaved.
- P7 **Outsider vocabulary.** Every internal code glossed in a front-matter key or replaced by the plain phrase; **every cross-model claim carries its own lane qualifier in `scope=`** (byte-comparable MLX seal / torch-Modal / mlx-vlm / MLX-exploratory), not just a glossary entry.
- P8 **The log stays the tiebreaker.** Header keeps the "log wins on conflict" line and the source-of-truth order.
- P9 **"No universal cell" is standardized** everywhere it appears to: *no universal **best** cell; no universal **fixed orientation**; a common informative cell can exist when signed per model (`fusion_rank_mean_geom` >0.55 on all ten)* — with that caveat adjacent, not one section away.
- P10 **The digest is dated and decays visibly.** "What we believe now" is stamped `current through log <YYYY-MM-DD> / <entry title>`; each digest line cites the claim IDs it restates; a future belief-state change must refresh the digest or mark it historical (added to the rule-5 checklist as part of surface 3).

## 4. Target structure

```
# Furnace Claims Ledger
  Front matter (NEW)
    · Read-me-first: what this page is / is not; source-of-truth order; log-wins rule
    · What we believe now — stamped "current through log 2026-08-17"; 8–10 one-liners,
      each citing the claim IDs it restates (no new content)
    · Tag key: 7 leading tags + decision rules for FALSIFIED/RESOLVED/SHIFTED/SUPERSEDED
      + the typed qualifier grammar, one example each
    · Code key: PRI(v3)/ACE(v4)/RPV(#10)/CC/BENCH/DC; sealed vs registered vs descriptive;
      comparability lanes; "orphan"; MK; the §11 "E3" vs §12 "E3" collision resolved here
    · Change history of this page (2026-04-15, 2026-07-25, 2026-08-17)
§0  Core theses (RETITLED "(formerly Core hypothesis)") — exactly the three audited theses (§6 below)
§1  Ground truth — PRI v1–v3 (kept; evidence pointers backfilled on every line; §1.5 → line+link;
    the "see §9" pointer fixed)
§2  PRI v3 direction hypothesis (kept; compound entries split; step-0 entry → lines + link)
§3  Failure law — banner: "HISTORICAL PROPOSAL (2026-04) — original P_fail transfer test NOT RUN;
    spiritual successors: §1.5 deployability warnings, §11 nested-OOB selector" (text kept)
§4  Generalization path — banner: "HISTORICAL PROPOSAL (2026-04) — null-space→HaluEval transfer
    NOT RUN as specified; the dispatcher-level transfer question was later tested in §11.3" (text kept)
§5  SUP motivation (kept)
§6  Queued hypotheses — RETITLED "(formerly 'not yet run')" → "Queued / partially explored";
    each line keeps its tag and gains a `status:` note (e.g. penultimate-layer: "never run as E07;
    ACE's `last_minus_1` cells are related evidence, not this test")
§7  Root-cause incidents (kept)     §8 Superseded (kept)     §9 Retired / resolved (kept)
§10 Morphology line — compound tags split (ACE → 2 claims; RPV → 3 claims + confluence-role scope)
§11 Commit-Confluence — 11.1 sealed / 11.2 scale-generation-locus (+ in-section "Depth (DC)"
    anchor, entries stay here) / 11.3 BENCH; every entry split by state, ≤3 lines, lane in scope=
§12 Empathy geometry — scope statement corrected ("no *empathy* claims; infrastructure/instrument
    claims only"); one line per proposition; long bodies copy-verified on their memo/result pages
    before trimming; plain-words key → front-matter code key
```

## 5. Phases (v2 — gated sub-phases; only B1 is mechanical)

- **A — RPV single home + confluence-role scope.** ✅ 2026-08-17.
- **B0 — Source-of-truth reconciliation.** For every entry whose state might have moved since it was written, check log tail + result page; produce a short reconciliation note (expected: none moves — the point is to *prove* that before touching text). Output: `reconciliation.md` table in this order's §10.
- **B1 — Archive + claim inventory (mechanical).** Snapshot to `_archive`; assign stable claim IDs to every proposition (splitting compound bullets on paper only); build the old→new manifest with columns `id · section · leading-tag(old) · leading-tag(new) · qualifier fields · authoritative source · evidence pointer(s) · trimmed-detail destination`.
- **B2 — Grammar + mapping approval (checkpoint 1, MK).** MK approves the tag decision rules, the qualifier grammar, and the manifest's tag mappings — especially the splits (RPV, WEAKEN, SHIFTED entries) — before any text changes.
- **C1 — Copy-and-verify links.** For every claim whose text will be trimmed: verify the detail on the destination page (grep key numbers/phrases); if absent, copy it there (new dated section) first; resolve every wikilink/anchor. Output: manifest `trimmed-detail destination` column fully populated + link-health report.
- **Checkpoint 2 (self, logged):** manifest complete, all destinations verified, zero unresolved links → proceed.
- **C2 — Split / trim / retag** in `claims.md` per manifest; add section banners (§3/§4/§6/§12) with the *audited* wording; fix the §1.5 pointer; standardize "no universal cell" per P9; add lane qualifiers.
- **D — Front matter + §0 theses.** Digest lines each cite claim IDs; §0 = the three audited theses verbatim (below); no other authored content.
- **E — Propagation, canon order, log last.** results n-a · history n-a · claims (this) · research-candidates n-a unless a status line references the new grammar · summary n-a · models n-a · index row · paper n-a · root `CLAUDE.md` vault-map bullet for `claims.md` (one line) · milestones n-a · **log last** with the 11-surface TOTAL line.

## 6. §0 theses — the only accepted wording (Codex-audited; each cites what it restates)

1. **T1 (restates §1.1, §11.3):** Commit-time representation measures separate contradiction and HaluEval-QA outcomes from controls: v2/v3 on the sealed synthetic plane; in the registered BENCH extension **per-model calibration passes 10/10** while **fixed-cell + fixed-sign transfer fails 6/10** — the signal is real, its orientation is not transferable.
2. **T2 (restates §11.1, §11.3):** There is **no universal best cell and no universal fixed orientation**; the transferable object is the calibration *procedure*. A common *informative* cell can still exist when signed per model (`fusion_rank_mean_geom` >0.55 on all ten) — do not read T2 as "no informative cell exists."
3. **T3 (restates §2):** The v3 null-space direction hypothesis holds as a **primary pass at the amended rank-1 operating point** (final layer, step 1, 3/3 primaries); **the sealed block left rank unpinned and rank 32 fails 0/3**; fresh-seed replication (v3.1) confirmed the pass, external claim still carries the rank-unpinned caveat.

_(v1's "T3 validated at sealed plane" wording is rejected — it overstated sealing.)_

## 7. Acceptance (v2)

- A1 **Tag lint:** every claim line has *exactly one* leading tag ∈ closed set; compound forms (`/`, `+`, `—` inside the leading bracket) = fail; inline history annotations must be `↳` sub-lines, not brackets. Not all seven tags need be present.
- A2 **Evidence pointer** on every claim line (`[[…]]`, `results/…`, log date, or repo path) — short §1/§6 lines included.
- A3 **Per-claim numeric conservation:** for each claim ID, the numbers (value · unit · denominator · scope) in the new line ⊆ the old line ∪ its verified destination page; any number new to the ledger = bug.
- A4 **Claim conservation:** old→new claim-ID mapping is a documented bijection-with-splits (every old proposition appears exactly once; no merges).
- A5 **Link health + one-click reachability:** every wikilink and anchor resolves (`obsidian unresolved`); every trimmed detail is on the page the claim links to (not two hops away).
- A6 **Inbound section-reference audit:** every `§n.m` cited in `log.md`/`results/*` still names the same content.
- A7 **Snapshot** byte-identical to the post-Phase-A file.
- A8 **Outsider read-test with a deterministic rubric:** a fresh model instance given only the new file answers (i) universality — must produce both halves of P9; (ii) RPV — must say "standalone NO-GO vs v3 *and* fixed component of the CC aggregate"; (iii) which verdicts were pre-registered — must list ≥ the sealed 18/20, A1, A2, B1, grid-B WEAKEN, precision H3, and must *not* list any `evidence=descriptive` item. Answers graded against those keys, not free-form.
- A9 Codex must-fixes 1–27 each carry a disposition in §9 (this table) before B0 starts.

## 8. Guardrails

- `wiki/log.md` and `wiki/results/history.md` untouched except the closing log entry.
- No sealed-claim scope/denominator/number changes; **no belief-state moves** — if B0 finds one is warranted, it is filed as a separate log-backed change, not folded into this cleanup.
- No section or sub-section renumbering; §11.2 keeps depth.
- Codex is write/audit-only: it audited this plan and may draft front-matter text on request; Claude executes all edits and the read-test.

## 9. Audit log — Codex adversarial audit, 2026-08-17 (static; verdict RED → YELLOW after must-fixes)

| # | Sev | Finding (abridged) | Disposition in v2 |
|---|---|---|---|
| 1 | MUST | D3 wrongly declared §3/§4 "realized/answered" — their specific tests were never run; that is a re-verdict | **Accepted.** D3 rewritten; banners now say "historical proposal — original test NOT RUN; related later work at …" |
| 2 | SHOULD | D2 measurements off (240 lines not 244; wrong line cited as the ~700-word entry) | Accepted; re-measured post-Phase-A; D2 reframed around non-atomicity |
| 3 | MUST | Section scope statements contradict contents (§12 "no validated claims" vs `[VALIDATED — plumbing only]`; §6 "not yet run" vs tiny-slice wins) | **Accepted.** New D4; §12 scope line and §6 title corrected in C2 |
| 4 | MUST | Verbosity is the symptom; claim non-atomicity is the defect | **Accepted.** P2 = split by state before trim; manifest supports splits |
| 5 | SHOULD | Evidence-pointer gap includes short §1/§6 lines | Accepted; A2 covers all lines; backfill in C1 |
| 6 | SHOULD | §1.5 "see §9" is a broken pointer | Accepted; fixed in C2 (points to §9 + the retirement result/log entry) |
| 7 | MUST | Qualifier grammar needs typed fields, not free-form | **Accepted.** P1 fields: evidence · verdict · disposition · scope · date |
| 8 | MUST | Mapping table for non-mapping tags; WEAKEN ≠ FALSIFIED; SHIFTED must split; RPV/ACE/CORRECTED/PILOT split | **Accepted.** P2 encodes the mapping; manifest carries per-claim mapping; B2 = MK approval |
| 9 | SHOULD | Inline history annotations and `[R4]` must not be counted as tags | Accepted; A1 lint scopes to leading tags; history → `↳` |
| 10 | MUST | Phase B not mechanical (banners = interpretation) | **Accepted.** Split into B0 reconciliation / B1 mechanical inventory / B2 approval |
| 11 | MUST | Phase C can delete unique qualification (some entries point only to a work order / nothing) | **Accepted.** C1 copy-verify-then-trim; checkpoint 2 |
| 12 | MUST | §11.2→§11.4 move breaks log references | **Accepted.** No move; in-section anchor only (P5) |
| 13 | MUST | T3 overstated sealing | **Accepted.** T3 rewritten (§6) |
| 14 | SHOULD | Phase E must be canon order, log last, all 11 surfaces | Accepted (§5 E) |
| 15 | MUST | Digest = content authoring; each line must cite claim IDs | **Accepted.** P10 + §4 |
| 16 | MUST | Accept only the three scoped theses | **Accepted verbatim** (§6) |
| 17 | MUST | A1 regex inadequate | **Accepted.** A1 rewritten |
| 18 | MUST | A3 bag-of-numbers diff over/under-sensitive | **Accepted.** Per-claim-ID conservation |
| 19 | MUST | Add claim-conservation + link-health + one-click gates | **Accepted.** A4, A5 |
| 20 | SHOULD | Inbound section-reference audit; source-authority column | Accepted: A6; manifest column |
| 21 | SHOULD | A5 read-test needs a deterministic rubric | Accepted: A8 |
| 22 | MUST | Reorder into gated sub-phases | **Accepted.** §5 |
| 23 | SHOULD | Separate structural moves from thesis authoring | Moot (no structural move) — noted |
| 24 | SHOULD | Decision rules for FALSIFIED/RESOLVED/SHIFTED/SUPERSEDED | Accepted; in P1 + front matter |
| 25 | MUST | "No universal cell" misleading without the common-cell caveat | **Accepted.** P9 |
| 26 | SHOULD | Lane qualifier per cross-model claim | Accepted; P7 `scope=` |
| 27 | SHOULD | Dated digest decays silently | Accepted; P10 stamp + refresh rule |

Codex spot-check: the three sampled destination pages (depth-curve, bench-a2-signflip, human-dyad) do hold the detail the plan assumes — but not proof of universal coverage, hence C1.

## 10. Reconciliation notes (B0 output, 2026-08-18)

Full detail: [[workorders/claims-ledger-manifest-2026-08-18]] (210 rows, four groups, checkpoint-1 decision list). Summary:
- **Numeric drift:** none beyond two minor typos (depth "N−6…N−17" → "N−2…N−17"; RPV H2 slope +0.080/+0.083 both documented).
- **Belief-state drift (ledger lags the record) — 5 places, all routed to MK as separate log-backed corrections, not folded into the cleanup:** E17b gate is ledgered HYPOTHESIS but v3.1-replicate records PASS +0.150 (J_n path); "rank unpinned / replicate first" was resolved by the v3.1 amendment + 3/3 replicate; E23 tagged OPEN but body is a closure; T4 defensiveness "dead-end" was revised 2026-07-12; §12 title/scope/guardrail contradict the section's RESOLVED/VALIDATED-plumbing rows and the 07-27 judge fix.
- **§3/§4 confirmed NEVER RUN** (`P_fail`, proportional-lift, under-duress appear only in the 2026-04-15 restructure log line) — banners will say "historical proposal; not run; related later work at …". **§6 title contradiction confirmed** (E07/E10–E12 exist only in the ledger; the three commit-linked items were tiny-slice keeps 2026-04-07 never re-tested at n=800). §5.1 encoder control never run.
- **Pointers:** 0 broken file pointers; 1 broken section pointer (§1.5 → §9); ~35 rows with no in-line pointer, all with existing backfill targets named.
- **Copy-first destinations (audit 11):** ANLI-sweep tally (log-only), direction-localization design text (ledger-only), B1/B2 numbers (log + .tex only), degeneration numbers (work order), T4 counts (log-only), and two §12 figures ("1 of 71", "15/24 vs 21/24") found nowhere but the ledger.
- **P9:** §11.1 "No universal cell" has no adjacent caveat; §11.3 holds the canonical wording; the E1 universal-floor positive is absent from the ledger as a claim.
- **A6 inbound anchors** cited from the log: §1.5, §2, §6.1, §9, §10, §11, §11.2 (×5), §12 — all preserved (no renumbering).

## 11. Handoff

Author: Claude. Auditor: Codex (done, §9). Executor: Claude. **Sign-off: MK — go/no-go for B0/B1, then checkpoint 1 (B2) approval of the tag grammar + manifest.**
