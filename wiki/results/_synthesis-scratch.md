---
status: SCRATCH / working notes — NOT canonical
created: 2026-06-18
purpose: Capture synthesis-relevant reasoning that was worked out live in conversation
  (2026-06-12 → 06-18) and is not yet in any other file. Each item carries a
  propagation target for when/if it is blessed into a canonical page.
---

# Commit-Confluence — synthesis scratch (live-only reasoning)

> ⚠️ **Ephemeral.** This is a holding pen, not a source of truth. Per [[../index|vault canon]],
> fold each blessed item into its canonical target and then prune it from here. Numbers below
> were read live from the published matrices (`commit-confluence/stage_b/profiles/`), seed
> 20260612, tag `prereg-seal-20260612`. **Legend:** 🆕 new finding · 🧭 decision · ⏳ pending task.

---

## 1. 🆕 Qwen3-1.7B / TriviaQA — the "out-of-distribution" cell, diagnosed
**Status: live read, not yet in a results page. → fold into [[confluence-seal-2026-06-11]] §Results (or a footnote) once blessed.**

The eye catches `geom_ci_lo = 0.529` for Qwen3-1.7B/TriviaQA, lowest in a TriviaQA column where
everyone else is 0.72–0.94 (next lowest Llama-3.1-8B 0.669). **It is not a bug** — data clean
(n=200, n_aligned=200, n_dropped=0, base rate exactly 0.50, controls passed).

**The anomaly is variance, not the point estimate.**

| | full-sample AUROC | OOB median | OOB CI | width |
|---|---|---|---|---|
| Qwen3-1.7B | **0.723** (normal) | 0.704 | **[0.529, 0.794]** | 0.27 |
| Qwen3-8B | 0.939 | 0.940 | [0.893, 0.976] | 0.08 |

Winner = `attention[final_bos_mass]` (full-sample 0.72, sign −1). A naive "best AUROC" pipeline
would ship 0.72; the honest nested-OOB returns 0.53 because the interval is ~3× wider, and the
deployability gate reads the lower bound. It *barely* clears `>0.50` — the closest-to-gate
deployable cell in the whole run.

**Three converging causes of the blown-up variance:**
1. **No depth / no corroboration** — only **3 of 26** geometric signals clear 0.65 (0.723, 0.680,
   0.661), then a cliff. Qwen3-8B has 10/26 above 0.65. Winner margin over 2nd ≈ 0.043.
2. **Unstable selection** — winner_stability **0.832** vs the 8B's **0.998**; under resampling the
   pick flips off `final_bos_mass` to `fisher_eff_rank` in ~12% of bootstraps (winner_counts ≈
   1664 vs ~231), and those resamples score poorly → fat lower tail.
3. **The fusion escape hatch collapses** — for Qwen3-8B the winner *is* the rank-mean fusion at
   **0.939** (variance-reduced, stable). For Qwen3-1.7B fusion is only **0.575**: on this small,
   4-bit-quantized model the geometric families *disagree*, so the rank-mean averages signal away
   instead of reinforcing it. No variance-reduction available → stuck on a lone unstable signal.

**Interpretation.** Smallest model in the cohort (1.7B, 4-bit) meeting the hardest internal
question ("do I actually know this fact?") at the corner where its representations are least
legible. Weakness is **task-specific** — its ANLI cell (0.567) is mid-pack and fine. The honest
selector is *working as designed*: it refuses to certify a high-looking-but-fragile single-signal
win. This cell is the concrete poster child for the per-deployment thesis.

## 2. 🆕 "Deployable but fragile" — a soft spot inside the 18/20 geometric PASS
**Status: live read. → mention as a one-line honesty caveat wherever the 18/20 PASS is asserted
(result page + paper Results), if blessed.**

Qwen3-1.7B/TriviaQA's `ci_lo = 0.529` sits **below the shuffled-null upper tail** (the 3 control
perms reached ci_hi ≈ 0.60). The control **passed** — that is a *procedure-level* test (no
shuffled perm certified upward, and none did) — but the real signal's lower bound overlapping the
null's upper band means this is the one deployable cell I'd footnote as **marginal, not solid**.
Of the 18 deployable cells, it is the single "watch it" entry. An adversarial reviewer will find
this; better to name it first.

## 3. 🧭 Make the paper standalone — concrete edit plan (agreed, not yet executed)
**Status: user said "yes" to these edits, then redirected to this scratch dump. → execute on
[[paper/cc-draft.tex]] next, then repackage `cc-paper-2026-06-12.zip`.**

The `.tex` is *mechanically* standalone (inline `thebibliography`, no `\input`, figures only).
The gap is that the signal **definitions are load-bearing on the companion reports** ([2]/[3]/[4]
= PRI/ACE/RPV, which have no public DOI). Three surgical fixes:
1. **One intuition clause per family** — what high/low means + why it tracks an unsupported answer
   (1 sentence each, no new math).
2. **A compact "panel glossary"** (short table or paragraph) mapping the cryptic winning-signal
   names — `att[final_bos_mass]`, `RPV:fisher_eff_rank`, `fusion_rank_mean_geom`, etc. — to plain
   descriptions, so **Figure 2's win-map is legible on its own**.
3. **Reframe the companion citations** as "full derivation in [x]" (optional) rather than
   prerequisites — *and* give PRI/ACE/RPV their own Zenodo DOIs so the refs actually resolve.

Net ≈ half a page added to Method + resolvable refs. No results/figures/thesis change.

**Also pending (minor):** in Table 1, change Verdict cell `FAIL (by one)` → **`FAIL (18 < 19)`**
to kill the ambiguity ("one short of the bar" vs "one cell failed" — actually *two* cells fail).

## 4. 🧭 Publication / DOI strategy (worked out live; none of this is in a file)
**Status: decisions + leans. → becomes real on first Zenodo upload; record outcome in
[[milestones]] when a DOI is minted.**

- **Zenodo** (CERN, free, permanent, mints a DOI on publish, no endorsement gate). Friend pointed
  to the `cybernetics` community (`zenodo.org/communities/cybernetics`) — legit, but a **loose
  topical fit** (systems theory, not LLM interp); fine for the DOI + niche eyes, curator approves
  the community add (worst case: archived without the tag, costs nothing).
- **License = CC BY** (decided earlier) — consistent across repo, paper, DOI. Maximizes
  citation/reuse; rejected NC/ND (block reuse), SA (viral), CC0 (waives attribution), arXiv
  non-exclusive (only for a future copyright-transfer journal — not our case).
- **Also DOI the repo** via Zenodo↔GitHub integration (archive a `commit-confluence` release →
  separate DOI for code+data). Strong reproducibility signal; cite both in the paper.
- **arXiv in parallel for *reach*** — that's where the AI-safety/interp audience lives (cs.LG /
  cs.CL). Needs a first-time **endorser**; candidate = **Junjie Hu** (HARP) or anyone with arXiv
  standing in the area. Zenodo-first does NOT block arXiv later.
- **Lean: DOI *this* paper now; companions (PRI/ACE/RPV) next.** Doing the whole trio at once
  makes Confluence fully standalone + yields 4 citable artifacts, but it's more upload work.

## 5. 🧭 Foresight "AI Node" outreach — status + hard resubmission criteria
**Status: process context, user actively deciding. → keep here / promote to a project memory if
it recurs. Not vault-results material.**

- User submitted to Foresight AI Node, then sent **4 follow-up emails**; Grants Team replied with
  a polite boundary ("no need for continuous further updates; if substantial updates, submit a
  new application"). Read: routine boilerplate, **not a merit judgment**; the operative word is
  *continuous*.
- **Decision: full stop.** No further emails. **No apology email** (that would be touch #5 and
  reopen the loop). No new application *now* — nothing substantial has changed (polish ≠ substance).
- **Resubmit ONLY on a genuine step-change:** (a) paper posted with a **DOI** (← Zenodo makes this
  real), (b) a **new sealed result that changes the headline**, or (c) a **named collaborator /
  affiliation / endorsement**. The Zenodo DOI is the cleanest path to legitimately reopening the
  door — *get the DOI first, then a fresh application is warranted.*
- Forward lesson noted: batch outreach into one message, then go quiet; restraint reads as
  confidence.

## 6. ⏳ NotebookLM podcast — staged, blocked on auth
**Status: source written ([[paper/cc-podcast-source]]); blocked. → resume after the user runs auth.**

- Clean LaTeX-free narration source written at `wiki/paper/cc-podcast-source.md` (folds in the
  19/20-bar framing and the §1 Qwen3-1.7B story above).
- Notebook title staged: **"Commit-Confluence — No Universal Detector, but a Universal Floor"**.
- **Blocked on auth:** user must run `uvx notebooklm login` (or `python3 -m notebooklm login`).
- **Open decision:** technical-tone audio (keep nested-OOB / real method names, lead with the
  two-sided verdict) vs. default conversational "deep dive." Lean technical (audience is technical).
- Then: `nlm_generate type=audio` → `nlm_download` mp3 to Desktop → send.

---

### What is NOT here (already canonical — do not duplicate)
Float/layout hardening of the paper → [[paper/cc-scaffold]] "Float hardening" note.
The sealed verdict, 12-winner win-map, E1/E2/E3, confidence-not-backstop, both orphans →
[[confluence-seal-2026-06-11]], [[summary]], [[log]] tail, [CLAUDE.md](../../CLAUDE.md) hot-update.
RPV-style abstract/intro + author byline → already in [[paper/cc-draft.tex]].
