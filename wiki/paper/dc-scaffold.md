# DC Paper — Scaffold

_Created 2026-08-17. Method code `dc` = **DC — Depth Curves** (per-layer separation maps for commit-time attention morphology). Status: **SUPERSEDED IN PART 2026-08-24 — grid B is run and scored, and the manuscript now exists at [[paper/dc-draft.tex]] (11pp, compiles clean).** This scaffold remains the outline/decision record; for the drafted claims and their exact frozen wording, the `.tex` is authoritative. Figures built and asserted against the scored JSON in `dc-figures/`; grid-B panels carry no envelope (MK decision A, 2026-08-24 — none was registered for grid-B slugs). Read [[paper/writing-standards]] before drafting._

## One-line thesis

Per-layer, registered depth curves of a sealed attention-disagreement metric show that *where* hallucination separation lives in the stack obeys no transferable placement law, that sparse depth sampling can invert locus conclusions, and that two regularities — a one-block CLIFF onset and a universal terminal-block give-back — survive (pending grid-B confirmation) across families and scales.

## Evidence base

- **Grid A (banked, registered):** [[results/depth-curve-2026-08-16]] — Qwen2.5 7B/32B/72B + Llama-3.3-70B × {ANLI R1, HaluEval-QA}, 8/8 gates clean. E1 UNDECIDED, CLIFF 7/8, terminal dip 8/8, P3 MISS = Llama mid-stack band (peak 0.897 @ 48/80 > panel readout 0.816; 44/80 blocks over envelope).
- **Grid B (RUN, registered verdict 2026-08-17):** [[results/depth-grid-2026-08-17]] — **E5 WEAKEN 8/12** (every evaluable cell but one passes; p_grid 0.0005; pooled dip CI [0.123, 0.201]; frozen CONFIRM bars missed); E6 NOT TESTED (gatekept). Three failure modes = three paper sections: behavioral gate, **js_no_bos instrument-domain boundary (gemma-27b BOS sink)**, one true miss (Small/halueval). **P8+P9 hit: the Llama band replicates at 3.1-70B, absent at 8B.** Family peak clusters: Mistral 0.88 / Qwen(A) 0.85 late, Llama31 0.41 ≈ Llama33(A) 0.46 mid, Gemma 0.64 between. Freeze `2062e56` → results `cdc55a9`. 405B stretch unrun (MK gate); MoE next step.
- Torch/Modal nf4 lane, NON-byte-comparable with sealed MLX panels — never pooled; the sealed 18/20 and panel claims are untouched (the blind-spot result bounds their *interpretation*, not their numbers).

## Headline claims (status-tagged; frozen language TBD at prereg freeze)

1. **[BANKED] No registered placement rule established.** Peak location is (model, task)-dependent (N−2…N−17; fractions 0.79–0.93 on Qwen); neither the absolute nor the relative frozen rule fired (E1 UNDECIDED); the earlier "peak at N−2" was a rung-resolution artifact. *(Phrase as "no rule established," never "non-law proven" — Codex audit MAJOR 8.)*
2. **[BANKED] The blind-spot lesson (methodological headline).** A 3-point depth panel classified Llama-3.3-70B as "readout locus"; the full curve shows a broad mid-stack attention band the panel's rungs (40/78/79) straddled. Fixed-layer probing can invert a locus conclusion. (Money figure.)
3. **[REGISTERED VERDICT — WEAKEN] Terminal-block give-back.** Discovery 8/8 (grid A, cross-fitted, [[results/depth-rescore-2026-08-17]]); held-out-model confirmation **8/12 — WEAKEN as written** ([[results/depth-grid-2026-08-17]]): the dip appears in every evaluable new cell but one (p_grid 0.0005) yet the frozen bars priced in exactly the failures that materialized. Paper framing: "a strong, nearly-universal regularity whose registered confirmation bar it did not clear" — the honest version of a universality claim.
4. **[NOT TESTED] CLIFF onset.** Gatekept behind E5 CONFIRM, which did not occur; grid-B descriptive rate 2/12 (many early-peak-undefined cells). Grid-A discovery rate 7/8 stands as discovery only.
4b. **[NEW, grid-B finding] The metric has a domain.** Sealed `js_no_bos` is undefined under total BOS-sink collapse (gemma-27b, block 3+) — an instrument-boundary section the paper must carry wherever js_no_bos appears.
5. **[PENDING grid B, descriptive] Family/version structure.** Does the Llama band appear in the 3.1-70B **same-size version comparison** (not "isolates post-training" — base-checkpoint identity is unestablished) and is it present or absent at 8B (descriptive, no "scale-emergent" vocabulary)? Do Mistral/Gemma have characteristic curve shapes? Unbalanced comparative panel — never "factorial family × scale."
6. **[DEPLOYMENT COROLLARY] Probe placement must be measured per model** — one cheap per-layer calibration pass replaces any depth heuristic.

## Figure inventory (planned; `dc-figures/`)

| # | figure | source |
|---|---|---|
| 1 | Full grid of depth curves (10–11 models × 2 tasks, envelope shaded) | grid A npz + grid B npz |
| 2 | **Money figure:** Llama-3.3-70B curve with the 3 panel rungs overlaid + panel readout winner line | banked |
| 3 | Terminal-dip forest plot (dip magnitude per cell, grid A hollow / grid B filled) | both grids |
| 4 | Peak fraction ℓ*/N vs N scatter with bootstrap CIs (the non-law) | both grids |
| 5 | CLIFF onset: rise-in-one-block vs total rise per cell | both grids |
| T1 | Verdict table (ℓ*, CI, peak, mid-med, E2, E4 per cell) | RESULTS.json both grids |
| T2 | Registered endpoint ledger (E5–E8, E1″ with bars and outcomes) | prereg + scorer |

## Related work / external corroboration (seed list for the draft)

- **Goldowsky-Dill, Chughtai, Heimersheim & Hobbhahn (Apollo Research), "Detecting Strategic Deception Using Linear Probes," arXiv 2502.03407 (2025)** — supervised logistic-regression deception probe in the **Llama-3.3-70B-Instruct residual stream at layer 22/80**; their Appendix D.2 layer sweep shows the usable deployment band (recall@1%FPR on control) is **mid-stack and narrow** — moving the probe two layers collapses recall to \~0 while AUROC stays decent — and their layer/hyperparameters transfer 3.1-70B→3.3-70B. Cite for **claim 2** (fixed-layer probing is fragile; deployment endpoints are far more layer-sensitive than AUROC) and as independent, different-construct/different-object corroboration that the operative depth region in big Llamas is mid-stack (adjacent to our P8/P9 band, claim 5). **Scope discipline when citing:** depth-locus-level convergence only — residual-stream direction ≠ attention morphology, strategic deception ≠ hallucination; do not phrase as replication. Ingestion note: [[lit/external]].
- **Ruan, Huang, Zhou, Wei, Wang & Sun, "Doomed from the Start: Early Abort of LLM Agent Episodes via a Recall-Controlled Probe Cascade," arXiv 2607.06503 (2026)** — per-round failure probes on agent-episode internals with recall-controlled abort gates; **layer placement is fixed per model by a preliminary per-layer probe-AUC sweep** (Llama-3.2-3B → 14/28, Qwen2.5-7B → 20/28). Cite for **claim 6** (the deployment corollary): an independent deployed system that replaces any depth heuristic with exactly the cheap per-model per-layer calibration pass we prescribe — and its two placements echo our family peak clusters (Qwen late, small-Llama mid) on two of our own panel models. **Scope discipline:** descriptive echo only — residual-stream probe ≠ attention morphology, agent-episode failure ≠ hallucination label; their sweep is a pilot heuristic, not a registered curve. Ingestion note: [[lit/external]].

- `[APPROVED 2026-09-06 — MK signed off same day; LANDED in dc-draft.tex §Related work as the "Measured, and dependent on the target as well as the model" paragraph]` **Kossen, Han, Razzak, Schut, Malik & Gal (OATML Oxford), "Semantic Entropy Probes: Robust and Cheap Hallucination Detection in LLMs," arXiv 2406.15927 (2024)** — linear probes on a single generation's hidden state predicting binarized semantic entropy, with **per-layer AUROC curves across 5 models × 4 tasks × 2 token positions** (Figs. 2–4, A.1–A.11). This is the earliest and broadest external depth-curve panel the lane has, and its Table 4 is the sharpest available evidence for **claim 6**: the selected probe band moves with the **target**, not only the model — on Llama-3-70B the semantic-entropy probe band is layers **76–80 of 80** while the accuracy probe band on the same model and data is **31–35 of 80**; Mistral-7B 28–32 vs 12–16. That extends the deployment corollary from "measure placement per model" to "per (model, distribution, target)." Their in-distribution verdict also flips depending on whether you aggregate over selected high-performing layers or all layers (Table 1 vs Fig. 6) — an external instance of the aggregation-set-decides-the-verdict hazard. **Scope discipline when citing:** their object is a supervised residual-stream probe's AUROC, not attention morphology; their band was selected in-sample with no OOB correction; and their long-form "AUROC peaks at intermediate layers" observation is qualitative — **no dip statistic, no CI, no registration — so it must not be cited as support for E5**, which is a registered miss whose phrasing cannot be strengthened by an unregistered external echo. Framing corroboration for claim 5 at most. Ingestion note: [[lit/external]].

- `[LANDED 2026-09-06 in dc-draft.tex §Related work as the "Measured on the step axis, and coarsely sampled on the layer axis" paragraph; section tallies five→six]` **Yeom, Sok, Kim, Park, Park & Kim (Seoul National University / GIST), "Hallucination as Commitment Failure: Larger LLMs Misfire Despite Knowing the Answer," arXiv 2605.22007 (2026, preprint)** — varies **position** where the other five vary depth. Aligning trajectories on the answer-emission step, detection AUROC of their semantic-probability-mass statistic is at chance two-plus steps before, rises to **0.58** there, and decays to chance after; token probability is flat across the same window. Cite for the **commit-locus** premise (the sixth independent external line, and the only one with a step-resolved curve) and for their warning that **token entropy is a poor localiser** of that step (20% exact match on long-form). ⚠️ **Scope discipline, and this one bit once already.** Their §4.4 sentence "peaking at mid-layers" refers to the **Instruct−Base gap**, *not* the probe AUROC (Fig. 8 caption is explicit), and Appendix J Table 6 is a **four-rung** panel whose winning rung is unstable across four sizes of one family — Last−1 for 0.8B/9B, Mid for 2B/4B. **Do not cite it as a mid-stack placement result, and do not present it as converging with Kossen's accuracy band or our P8/P9 Llama band.** The honest use is as another coarse-rung panel that cannot locate a peak, which is the same limitation as our own 3-rung readout (claim: P3). **E5 prohibition applies in full** — no dip statistic, supervised probe, different instrument. Their headline statistic is also an **oracle** (needs ground-truth answer aliases; the paper calls it "an analytical probe, not a deployable detector"), so **none of its AUROCs may enter a comparison table**. Ingestion note: [[lit/external]].

## Post-draft input — instrument co-location (2026-08-29, NOT in the manuscript)

`[OPEN — descriptive; NOT a registered endpoint]` → [[results/instrument-colocation-2026-08-29]].
Post-hoc read of the banked npz, which record `final_bos_mass` per block in **both** grids;
neither registered run scored it. **Nothing here is registered and none of it may enter the
manuscript's registered claims.** Two touchpoints for MK, both optional:

- **It enlarges the money figure's own number.** On Llama-3.3-70B/anli, `bos_mass` peaks
  **0.915** — above the js band's 0.897 and further above the panel readout winner 0.816. The
  blind-spot lesson (claim 2) is *understated* by the registered metric alone. Adding it would
  mean introducing a second, unregistered instrument into fig2 — likely a limitations sentence
  rather than a figure change.
- **It bears on the deployment corollary (claim 6).** Placement must be measured per model —
  and now, apparently, **per instrument**: `js_no_bos` and `bos_mass` trace weakly-correlated
  curves (task medians ANLI 0.445 / HaluEval **0.127**) and each is at chance at the other's
  peak in 6/17 cells. A one-line strengthening of claim 6 is the cheapest possible use of this.
- **Do not** import the peak-location gaps: that test is inconclusive (CI excludes zero in 2/17),
  consistent with the paper's own E1 finding that argmax bands are wide.

**Decision owed (MK):** leave the 12pp draft frozen and carry this as follow-on work
(candidate #16), or spend a limitations paragraph on it. Default recommendation: leave frozen —
the draft is already over the 11pp bar and this is unregistered.

## Post-draft input — depth coverage + fixed-depth redundancy (2026-08-30/31, NOT in the manuscript)

`[OPEN — descriptive; NOT registered endpoints]` → [[results/depth-coverage-2026-08-31]],
[[results/instrument-redundancy-2026-08-30]]. Steps 2 and 3 of candidate #16, run on banked
artifacts at $0. **Nothing here is registered and none of it may enter the manuscript's
registered claims.** This *replaces* the single co-location touchpoint above with a sharper —
and partly more awkward — set. Three touchpoints for MK, all optional:

- **Claim 6 (deployment corollary) now has a real counterweight, not just a strengthening.**
  The 2026-08-29 note proposed a one-line strengthening: placement must be measured per model
  *and per instrument*. That still holds. But the discriminator came back **split**: aiming one
  instrument at a model's own peak beats the best single fixed rung **6/8 in grid A** (median
  +0.1195) and only **6/9 in grid B** (median +0.0110, intervals excluding zero in **both
  directions**, one significant loss at Llama-3.1-8B/anli −0.075). Per-model depth targeting is
  **not** a general improvement on held-out models. A claim-6 strengthening that ignores this
  would overstate what the follow-on work found.
- **One result is cleanly quotable and needs no depth argument at all.** Fusing the six
  fixed-rung columns **loses** to the best single fixed-rung column (median −0.0435 / −0.0383,
  3/8 and 3/9 cells). If a limitations sentence is spent anywhere, this is the cheapest and most
  robust one: it held identically across all three scorings and does not depend on the
  depth-coverage story being right.
- **The factor-structure premise is weaker than the manuscript assumes, but not refuted.** At a
  fixed depth, PC1 carries ≥0.90 of the three-instrument covariance in only **5/42** cells — and
  **all five are Llama-3.3-70B**. That is a `[HYPOTHESIS]` on one model and two tasks; it is not
  strong enough to put in a paper, and it is exactly strong enough to stop anyone writing "the
  attention cells measure one thing" as an aside.
- **Do not** import the selection-stability split. It is **parked, not reported** — post-hoc,
  its floor breaks at a 3/5 threshold, grid-confounded, and endogenous.
- **Do not** import any procedure-level generalisation claim. The primary interval is
  evaluation-row-only and charges nothing for selection; the median training top-vs-runner-up
  margin is 0.0094, so the argmax races are close and the audit's caution stands.

**Decision owed (MK):** unchanged in shape from 2026-08-29 — leave the 12pp draft frozen and
carry all of this as follow-on work (candidate #16), or spend one limitations paragraph.
Default recommendation: **leave frozen**, and if a single sentence is ever spent, spend it on
the fixed-fusion-loses-to-best-single-column result rather than on depth coverage, because that
one is unregistered but not fragile.

## Open decisions

**All four paper-level decisions closed 2026-09-06.** What remains below is resolved history plus the one cross-paper item.

- ~~Venue/length~~ — **RESOLVED 2026-09-06 (MK): 12pp FULL.** No compression pass; the draft stands at its written length.
- ~~Title~~ — **NOT OPEN; it was locked at commit `b547b70`** and is live in `dc-draft.tex` line 44: *Cross-Sections of Commitment — Per-layer separation maps of attention morphology*. This line was stale and is corrected 2026-09-06.
- ~~Limitations paragraph on the follow-on work~~ — **RESOLVED 2026-09-06 (MK): LEAVE IT.** The draft stays frozen; none of the 2026-08-29 / 08-31 / 09-06 follow-on work enters the manuscript. All of it is unregistered and remains carried as candidate #16.
- ~~405B stretch cell~~ — **RESOLVED 2026-09-06 (MK): OUT.** With it excluded, nothing in the manuscript depends on unrun compute; the existing disclosure that the cell is depended-on-by-nothing now describes the final scope.
- Whether CC paper gets a one-sentence cross-reference once DC exists (the panel-relative caveat is currently proposed, unapplied).

## Discipline

- Grid A = discovery; grid B = **prospective held-out-model confirmation on two fixed benchmarks** (ANLI R1, HaluEval-QA) — never claimed as task-general. Llama 3.1 cells are family-seen/model-unseen. All grid-B endpoint language frozen before launch; misses reported as written.
- Codex gpt-5.6 round-1 audit: RED, all 10 MAJORs accepted (cross-fitted E5, directional calibrated E6, frozen denominators, Medium-3.5 FP8 handling, single capture mode, prospective pinning, multimodal descriptor, causal-language removal, scope recast, gatekeeping hierarchy) — see [[workorders/depth-grid-expansion-workorder-2026-08-17]] §Audit round 1.
- One precision-heterogeneous cell (Medium 3.5, FP8 origin) disclosed wherever the panel is shown.
- In-sample sign-free caveat travels with every AUROC; per-cell argmax selection acknowledged (envelope + bootstrap mitigate, don't eliminate).
- Mechanism claims stay out (v6–v8 same-Δh lesson).
