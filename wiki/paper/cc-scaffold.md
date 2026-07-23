# CC (Commit-Confluence) — paper scaffold

_Method code **`cc`** = **Commit-Confluence**, the unified commit-moment dispatcher (ACE + PRI + RPV + confidence + fusion under one honest nested-OOB selector). New paper line, filed 2026-06-12. Paper-facing method name is **Commit-Confluence**; `cc` is the stable vault/file prefix._

## Status
Research report drafted directly in `.tex`. Numbers are locked from the **registered sealed run** ([[results/confluence-seal-2026-06-11]], seed 20260612; repo tag `prereg-seal-20260612`), with post-seal scale/locus and precision-deconfound sections clearly marked as extensions that do **not** alter the sealed 18/20 endpoint. The manuscript now also includes the registered BENCH HaluEval-QA extension: A1 passes 10/10 under per-model calibration, A2 fails 6/10 under fixed-cell/fixed-sign transfer, so their conjunction is not satisfied.

## Files
| File | Role |
|---|---|
| [[paper/cc-draft.tex]] | 📄 Overleaf-ready LaTeX (`\graphicspath{{cc-figures/}}`; inline `thebibliography`). |
| `cc-figures/` | fig1 coverage · fig2 win-map · fig3 label-efficiency · fig4 universality floor · fig5 scale extension (+ `make_figures.py` builder, reads the repo results — set `$CONFLUENCE_REPO`). |
| `cc-paper-2026-06-24.zip` | current Overleaf upload bundle (cc-draft.tex + cc-figures/). |

## Headline claims (all registered / honest two-sided)
1. Geometric-only dispatcher **deployable 18/20** (bar ≥17) — PASS; strict full-panel **18/20** (bar ≥19) — FAIL by one (falsified, honestly).
2. **Confidence is not the backstop** — both endpoints fail the *same* 2 ANLI deployments (gemma-3-4b predicted; Llama-3.1-8B new).
3. **No universal champion** — 12 distinct winning signals / 18 deployable.
4. **But a universal above-chance floor** — fixed fusion signal generalizes to held-out model on 9/10 (ANLI) + 10/10 (TriviaQA). First positive in the program.
5. **Task transfer partial** — median 0.67, 85% above floor.
6. **Label cost** — E3 measures through $n=150$ only; at least 150 labels is a lower bound, the curve is still rising, and no knee is estimated. TriviaQA budgets draw complete paired stems.
7. **Registered BENCH extension** — HaluEval-QA A1 passes 10/10 with per-model calibration; A2 fails 6/10 for `fusion_rank_mean_geom` plus one pooled sign. The failure is orientation transfer, not absence of a common informative cell.

## Figure inventory
- **Fig 1** `fig1_coverage.pdf` — per-deployment geometric CI-lo grid; 2 orphans boxed.
- **Fig 2** `fig2_winmap.pdf` — 12 distinct winners, colored by family.
- **Fig 3** `fig3_label_efficiency.pdf` — fraction deployable at E3 budgets 50/100/150 only; rising through the largest measured budget, with row draws for ANLI and complete-stem draws for TriviaQA.
- **Fig 4** `fig4_universality_floor.pdf` — fixed fusion signal held-out AUROC (E1).
- **Fig 5** `fig5_scale_extension.pdf` — post-seal scale/family extension: gemma-3-4b/ANLI orphan (0.40, below gate) recovered by gemma-3-12b (0.71); Qwen2.5-14B control. Reads `stage_b/profiles_ext/` + the sealed gemma-3-4b orphan. (Added 2026-06-18.)

**Scale extension folded in (2026-06-18).** Added §"Post-seal extension: model scale closes an orphan" (Table + Fig 5) before Discussion — pre-registered, byte-comparable, does NOT alter the sealed 18/20. Also applied the standalone-verification fixes: hedged the Method "Intuition" notes (existence-of-structure, not fixed polarity — selector sign-locks per deployment) and tightened two glossary rows (`fusion_rank_mean_geom` = one rep per family; `spectral_entropy` = normalized). The old June 18 bundle is superseded by `cc-paper-2026-06-24.zip`.

**Scale/locus + precision finalization (2026-06-24).** Folded in gemma-4 generation-axis result, Llama-3.3-70B scale result, Qwen-vs-Llama signal-locus dissociation, and the precision ladder / provenance-bug deconfound. Tightened Limits + Reproducibility so non-byte-comparable extension cells are not over-pooled or overclaimed. Local Tectonic compile is clean; current PDF is 10 pages.

**BENCH + label-cost correction (2026-07-22).** Added the registered HaluEval-QA A1/A2 section, including the sign-inversion non-rescue and pre-Phase-4 version-gate/stem-aware E3 disclosures. Removed the fabricated E3 $n=200$ anchor and knee claim: measured budgets are 50/100/150, and $n=150$ is a lower bound rather than a sufficiency estimate.

## Overleaf build
Upload `cc-paper-2026-06-24.zip` → New Project → Upload Project. Compiler **pdfLaTeX** or Overleaf default LaTeX is fine; main doc **`cc-draft.tex`**. Standard packages only; no bibtex.

**Float hardening (2026-06-12; verified 2026-06-24).** First Overleaf PDF had float-placement problems (label-efficiency figure marooned on a near-blank last page; figures floating past the References; Table 1 splitting the Method bullet list). Fixed at source: added `float`+`placeins`; Table 1 and the label-efficiency figure pinned with `[H]`; `\FloatBarrier` before Discussion and before the bibliography; other figures `[!htbp]` with relaxed `\topfraction`/`\bottomfraction`. Local Tectonic compile on 2026-06-24 completes without warnings after tightening the glossary table.

## Style
Abstract + Introduction follow the **RPV draft** register (dense/precise; lead with the
methodologically-elevated honest question; two-sided verdict framed constructively; explicit
contributions; deployment-safety framing). Author: **Michael S.R. Kitti** `<msrkittty@proton.me>`
(matches the RPV byline).

## Open decisions
- 🎯 Funder tailoring: LTFF variant leads with deployment-safety + label-cost + a "next 6 months" funded-agenda section; Foresight variant foregrounds mechanistic-interpretability framing.
- 📦 Whether to mirror the paper source into the public repo (currently vault-only per the paper-stays-in-`wiki/paper` rule).
- 🔗 Possible fold-in / cross-ref with the ACE + RPV papers (shared cohort + signals).
