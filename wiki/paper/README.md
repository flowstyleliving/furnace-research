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
| [[paper/cc-draft.tex]] | 📄 Overleaf-ready LaTeX fellowship report (`\graphicspath{{cc-figures/}}`, inline bib), updated through the post-seal scale/locus + precision-deconfound results. |
| [[paper/cc-scaffold]] | 🪺 Headline claims + figure inventory + Overleaf build + open decisions. |
| [[paper/cc-podcast-source]] | Podcast / NotebookLM narration source, updated through the post-seal scale, family-locus, and precision-ladder results. |
| [[paper/cc-benchmark-proposal]] · [[paper/cc-benchmark-proposal-v2]] | Benchmark-expansion proposals (2→N benchmarks for the CC TMLR→NeurIPS submission; v2 = post-review). |
| [[paper/cc-benchmark-review]] · [[paper/cc-benchmark-review-v2]] | Adversarial reviews of the expansion proposals. (Renamed 2026-07-09 from `benchmark-expansion-*` into the `cc-` convention.) |
| `cc-figures/` | 5 PDFs (coverage / win-map / label-efficiency / universality floor / scale extension) + `make_figures.py` builder. |
| `cc-paper-2026-06-24.zip` | 📦 Current Overleaf upload bundle. |

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

Math deconstruction: [[Candidate-10-Shadow-Ambiguity-Deconstruction]] (vault root). Status detail: [research-candidates](../research-candidates.md) §10. Figure builder lives in the t0 repo (`exploratory/shadow-ambiguity/paper/figures/`).

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
- Frozen Overleaf bundles: `pri-paper.zip`, `pri-paper-2026-05-02.zip` (PRI); `ace-paper-2026-05-30.zip` (ACE); `rpv-paper-2026-06-07.zip` (RPV); `cc-paper-2026-06-24.zip` (CC current).
