# Paper Folder — Organizer + Naming Convention

_Created 2026-06-07, reorganized 2026-06-08. **This is the rule sheet. Read it before creating or editing any paper file.**_

## 📛 Naming convention (the rule)

Every file in `wiki/paper/` is named **`<method>-<role>`**, where `<method>` is the lowercase method code and `<role>` is the artifact type. **No generic names** (`draft.md`, `figures/`) — the method prefix is mandatory so Obsidian wikilinks stay unambiguous and the graph view groups by method.

**Method codes** (one per paper line; the acronym is uppercase in prose, lowercase in filenames):

| code | method | milestone | object |
|---|---|---|---|
| `pri` | **PRI** — Predictive Rupture Index (`null_ratio` direction metric) | v3 | sealed detection line |
| `ace` | **ACE** — Attention Commitment Estimator (`W_u`-free t=0 attention morphology) | v4 | sealed morphology line |
| `rpv` | **RPV** — Readout Pseudo-Volume (`W_u`-using softmax-Fisher pseudo-volume) | candidate #10 | morphology line |
| `cc` | **Commit-Confluence** — unified commit-moment dispatcher (ACE+PRI+RPV+confidence+fusion under nested-OOB) | sealed 2026-06-12 | integration line (name provisional) |

**Roles** (the suffix):

| suffix | artifact |
|---|---|
| `-draft.md` | full prose draft (the manuscript) |
| `-draft.tex` | Overleaf-ready LaTeX companion |
| `-scaffold.md` | outline + headline claims + figure/table inventory + open decisions |
| `-submission.md` | arXiv submission tracker (endorsers, checklist) |
| `-scope-<date>.md` | pre-seal scope/decision memo |
| `-figures/` | that paper's figure directory (the **only** place figures live) |
| `-paper[-<date>].zip` | frozen Overleaf export bundle |

**Rules for a new paper:**
1. Pick an uppercase method code (e.g. the locked paper-facing name, mirroring ACE↔v4 / RPV↔#10).
2. Name every file `<code>-<role>` and put its figures in `<code>-figures/`.
3. Point the `.tex` `\includegraphics{…}` and `\input{…}` at `<code>-figures/`.
4. Add a row to the relevant section below **and** a row to `wiki/index.md`.

## 🟢 Active papers

### CC (Commit-Confluence) — unified dispatcher (fellowship report)
Method **Commit-Confluence** (provisional code `cc`): the dispatcher that fits ACE + PRI + RPV + confidence + 2 fusion signals at the commit moment under one honest nested-OOB selector. Numbers locked from the registered sealed run ([[results/confluence-seal-2026-06-11]], seed 20260612). Public repo + reproducible matrices: <https://github.com/flowstyleliving/commit-confluence>.

| File | Role |
|---|---|
| [[paper/cc-draft.tex]] | 📄 **THE merged CC paper (2026-07-26)** — single comprehensive Overleaf-ready LaTeX: sealed 18/20 core + the FULL six-task BENCH extension (families A/B/C as subsections of §``The registered BENCH extension''; A1 10/10 PASS, A2 6/10 FAIL sign-inversion, B1 7/20 FAIL stated prominently, B2 both-deployable, family-C descriptive) + post-seal scale/generation/locus + precision deconfound. Parent title kept, subtitle nods to the six-task registration. All 14 bibitems (13 parent + `halueval`); all frozen-language sentences stated exactly once; forward-work reports the executed sign-flip coincidence screen (NULL, p=0.50). Uses all 8 figures. E3 claim limited to measured 50/100/150 budgets; HaluEval label cost carried as the 2026-07-26 descriptive estimate (knee at 150, 10/10 flat to 500 — labeled post-hoc, not registered). **Compressed 21→15pp (2026-07-28)** for the 10–15pp target: cut the endpoints table + the A1/A2-definition table (both subsumed by the Table-1 ledger) and the rank-mirror + scale-extension figures (redundant with tab:a2 / tab:ext); paired the four Results figures into two `subcaption` rows; de-duplicated the Rigor/Discussion/Limits prose; `\footnotesize` bibliography. Frozen language fully intact per a 4-lens adversarial workflow (CLEAN, zero claims dropped); post-audit fixes added the registered bars to the abstract/intro, normalized the sealed gemma-3-4b orphan to 0.403 everywhere, and cross-referenced two orphaned floats. Type-3 figure fonts remain a flagged follow-up (needs `pdf.fonttype=42` regen). |
| [[paper/cc-extend-draft.tex]] | 🗄️ **SUPERSEDED 2026-07-26 by the merged `cc-draft.tex`** — kept for provenance only; do not edit. Was the standalone six-task extension companion (its content is now §``The registered BENCH extension'' of the merged paper; its `ccpaper` self-citation and companion framing dissolved into internal cross-references). |
| [[paper/cc-scaffold]] | 🪺 Headline claims + figure inventory + registered BENCH section + Overleaf build + open decisions. |
| [[paper/cc-podcast-source]] | Podcast / NotebookLM narration source, updated through the registered BENCH section and the post-seal scale, family-locus, and precision-ladder results. |
| [[paper/cc-benchmark-proposal]] · [[paper/cc-benchmark-proposal-v2]] | Benchmark-expansion proposals (2→N benchmarks for the CC TMLR→NeurIPS submission; v2 = post-review). |
| [[paper/cc-benchmark-review]] · [[paper/cc-benchmark-review-v2]] | Adversarial reviews of the expansion proposals. (Renamed 2026-07-09 from `benchmark-expansion-*` into the `cc-` convention.) |
| [[paper/cc-bench-prereg-review]] | ⚔️ Codex adversarial audit of the BENCH **pre-registration** (2026-07-11), driving it v1.0 → v1.2; a distinct artifact from the two proposal reviews above. Full history in `wiki/index.md`. |
| `cc-figures/` | 8 PDFs + `make_figures.py` builder, all now consumed by the merged `cc-draft.tex` (fig1 coverage / fig2 win-map / fig3 label-efficiency / fig4 universality floor / fig5 scale extension / fig6 A2 transfer / fig7 rank mirror / fig8 BENCH panel). Filenames keep their build numbers; print numbering is symbolic (`\ref`), so the merge renumbered nothing by hand. Label efficiency plots only the measured 50/100/150 budgets and makes no sufficiency or knee claim. |
| `cc-paper-2026-07-26.zip` | 📦 Current Overleaf upload bundle — the ONE merged paper (tex + 6 referenced figures; fig5/fig7 cut in the 07-28 compression). Rebuilt 2026-07-28. Supersedes the two 07-23 bundles. Rebuilt 2026-07-26 after the Codex gpt-5.6-sol adversarial review (2 nits fixed: Discussion transfer-overclaim de-clawed; "≥150 labels" re-bounded to measured-budget phrasing) + date bump (`this version: July 26, 2026`). |
| `raw/papers/cc-paper-2026-07-26.pdf` | 📕 **Compiled PDF (15pp)** — built locally with tectonic; **compressed 21→15pp on 2026-07-28** (see log); all 14 bibitems + 6 figures render (fig5/fig7 cut as redundant). In-PDF version stamp kept at `July 26, 2026` per MK's earlier instruction — bumping to July 28 is an open decision. |
| [[paper/writing-standards]] | ✍️ House reference stock for paper writing: abstract formula, BLUF section craft, the binding CC/BENCH frozen-language obligations, reference-hygiene hardening rule (merged/companion papers carry the full parent bibliography), mechanics + voice. Read before drafting or merging any paper. |

**Open:** funder-specific variant (LTFF / Foresight) if needed for a particular launch route; optional later fold-in with standalone ACE + RPV papers.

### ACE (v4) — sealed morphology spine
Method name **ACE = Attention Commitment Estimator** (`W_u`-free t=0 attention morphology). Numbers locked from the sealed verdict ([[results/v4-sealed-2026-05-26]]): E_A1 7/9 PASS, E_A2 3/9 partial transfer, baselines 2/4 wins.

| File | Role |
|---|---|
| [[paper/ace-draft]] | ✍️ Full prose draft (~4865 words, all sections + appendices). **The canonical ACE manuscript.** |
| [[paper/ace-draft.tex]] | 📄 Overleaf-ready LaTeX (companion; `\includegraphics` → `ace-figures/`). |
| [[paper/ace-scaffold]] | 🪺 Outline + figure/table inventory + open decisions (venue, page length). |

**Remaining before submission:** title pick, venue + page-length cut, intro-hook tightening, related-work bibliography polish, final consistency sweep. (.tex conversion is **done**.)

### RPV (candidate #10) — honest-negative workshop paper
Method name **RPV = Readout Pseudo-Volume** (locked 2026-06-07; *shadow-ambiguity* / *#10* stay the internal exploratory slug). 8pp workshop paper. **Honest-negative spine:** RPV beats plain confidence (random-effects meta **+0.102** [+0.065, +0.140], p≈5e-8, brittleness-clean, 3 families) **but is REDUNDANT with sealed v3 `null_ratio`** (base-B meta **+0.011 < +0.02 bar → registered H1 NO-GO**); it complements v3 **only** in v3's collapse regime (H2 slope +0.080; Qwen3-8B). Confidence-independent but v3-overlapping — not a universal detector. Also slated as the Fig-4 / §6.4 benchmark in the ACE paper fold-in.

| File | Role |
|---|---|
| [[paper/rpv-draft.tex]] | 📄 Self-contained 8pp workshop LaTeX (inline `thebibliography` + `\input{rpv-figures/table1_summary.tex}`; ACE preamble). No `-draft.md` yet — drafted directly in `.tex`. |

Math deconstruction: [[Candidate-10-Shadow-Ambiguity-Deconstruction]] (in `wiki/learn/`). Status detail: [research-candidates](../research-candidates.md) §10. Figure builder lives in the t0 repo (`exploratory/shadow-ambiguity/paper/figures/`).

## 🗄️ Archived — PRI (v3), currently inactive
The pre-ACE workshop paper. **Do not edit unless the user explicitly says "v3" / "PRI".**

| File | Role |
|---|---|
| [[paper/pri-draft]] | v3 prose draft (workshop, ~8pp). |
| [[paper/pri-draft.tex]] | v3 Overleaf LaTeX (`\includegraphics` → `pri-figures/`). |
| [[paper/pri-scaffold]] | v3 outline + plot inventory. |
| [[paper/pri-submission]] | v3 arXiv submission tracker (endorser outreach). |

## 📐 Pre-seal planning history
| File | Role |
|---|---|
| [[paper/ace-scope-2026-05-26]] | ACE scope memo + 3-candidate headline comparison. **Superseded by the sealed run** — provenance only. |

## 📦 Build artifacts (figures + frozen bundles)
- Figure dirs: `pri-figures/` (PRI/v3), `ace-figures/` (ACE/v4), `rpv-figures/` (RPV/#10). Each paper's figures live only in its own dir.
- Frozen Overleaf bundles (all gitignored / local-only): `pri-paper.zip`, `pri-paper-2026-05-02.zip` (PRI); `ace-paper-2026-05-30.zip` (ACE); `rpv-paper-2026-06-09.zip` (RPV current; `-2026-06-07.zip` prior); `cc-paper-2026-07-26.zip` (CC current — the merged single paper; `cc-paper-2026-07-23.zip`, `cc-extend-paper-2026-07-23.zip`, `cc-paper-2026-06-{12,18,20,24,25}.zip` + `cc-draft-with-figures.zip` are superseded).
