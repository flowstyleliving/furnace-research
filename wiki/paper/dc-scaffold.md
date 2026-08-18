# DC Paper — Scaffold

_Created 2026-08-17. Method code `dc` = **DC — Depth Curves** (per-layer separation maps for commit-time attention morphology). Status: **scaffold only — grid B not yet run.** Read [[paper/writing-standards]] before drafting._

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

- **Goldowsky-Dill, Chughtai, Heimersheim & Hobbhahn (Apollo Research), "Detecting Strategic Deception Using Linear Probes," arXiv 2502.03407 (2025)** — supervised logistic-regression deception probe in the **Llama-3.3-70B-Instruct residual stream at layer 22/80**; their Appendix D.2 layer sweep shows the usable deployment band (recall@1%FPR on control) is **mid-stack and narrow** — moving the probe two layers collapses recall to ~0 while AUROC stays decent — and their layer/hyperparameters transfer 3.1-70B→3.3-70B. Cite for **claim 2** (fixed-layer probing is fragile; deployment endpoints are far more layer-sensitive than AUROC) and as independent, different-construct/different-object corroboration that the operative depth region in big Llamas is mid-stack (adjacent to our P8/P9 band, claim 5). **Scope discipline when citing:** depth-locus-level convergence only — residual-stream direction ≠ attention morphology, strategic deception ≠ hallucination; do not phrase as replication. Ingestion note: [[lit/external]].

## Open decisions

- Venue/length (workshop 8pp vs full): decide after grid B verdicts. MK decision.
- Title. Candidates riffing on map-vs-territory / "depth rungs vs depth curves". MK decision.
- 405B stretch cell in or out (cost gate). MK decision.
- Whether CC paper gets a one-sentence cross-reference once DC exists (the panel-relative caveat is currently proposed, unapplied).

## Discipline

- Grid A = discovery; grid B = **prospective held-out-model confirmation on two fixed benchmarks** (ANLI R1, HaluEval-QA) — never claimed as task-general. Llama 3.1 cells are family-seen/model-unseen. All grid-B endpoint language frozen before launch; misses reported as written.
- Codex gpt-5.6 round-1 audit: RED, all 10 MAJORs accepted (cross-fitted E5, directional calibrated E6, frozen denominators, Medium-3.5 FP8 handling, single capture mode, prospective pinning, multimodal descriptor, causal-language removal, scope recast, gatekeeping hierarchy) — see [[workorders/depth-grid-expansion-workorder-2026-08-17]] §Audit round 1.
- One precision-heterogeneous cell (Medium 3.5, FP8 origin) disclosed wherever the panel is shown.
- In-sample sign-free caveat travels with every AUROC; per-cell argmax selection acknowledged (envelope + bootstrap mitigate, don't eliminate).
- Mechanism claims stay out (v6–v8 same-Δh lesson).
