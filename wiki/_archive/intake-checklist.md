# Intake Checklist

Tracks what's still needed to make the vault fully load-bearing for the next leg of research. Tick items as they arrive; move notes to the relevant wiki page once ingested.

## 1. Raw sources → `raw/`
- [x] Experiment outputs discovered in `/Users/msrk/Documents/PRI_at_commitment/pri_v2_results/` — parquet files per model + combined + summary. Pointer filed in [references/code](../references/code.md); not copied into `raw/` (large, and the source is the authoritative location).
- [x] Per-sample trace dumps: `*_trace_dumps.parquet` in same dir.
- [x] Pre-run audit checklist ingested from `PRI_at_commitment/PRI_V2_PRE_RUN_AUDIT_CHECKLIST.md` — informed the v1/v2 formula corrections and the per-variant structure.
- [x] Autoresearch plan + brief ingested from `PRI_at_commitment_autoresearch/autoresearch/{PLAN.md,research_brief.md}`.
- [x] Historical tiny-slice results from `autoresearch/results.tsv` filed into `wiki/results/history.md`.
- [x] "Prediction Rupture at Commitment" paper draft — filed as `raw/papers/furnace/2026-hallucinations-rupture-at-commitment.pdf`; summary page later deleted 2026-07-09 after the step-0 bug audit was canonicalized in `wiki/claims.md`.
- [~] Seeding papers (Fisher/natural-gradient; representation probes/deception) — **deferred 2026-04-14 per user**: not important at this stage. Revisit if v3 theory work needs external grounding.
- [x] Reviewer/collaborator feedback — Craig Quiter note filed in `raw/feedback/` (2026-04-14).

## 2. Code + data pointers (reference-type, not copies)
- [x] MLX research repo: `/Users/msrk/Documents/PRI_at_commitment/` — see [references/code](../references/code.md)
- [x] Autoresearch repo: `/Users/msrk/Documents/PRI_at_commitment_autoresearch/` — same
- [x] v1 cosine + v2 FIM variants implemented in `pri_metrics.py`
- [x] AUROC / Hedges g / bootstrap via the pipeline's analysis stage (`pri_v2_mlx_pipeline.py`)
- [ ] Path / provenance of the synthetic puzzle dataset generator is `synthetic_logic_loader.py` — document the exact 2×2 construction details in the overview or a dedicated page if it becomes a frequent reference.

## 3. Ground-truth facts (populated in vault)
- [x] Sample construction: 2×2 factorial `chain_length × contradiction`; contradiction injects conflicting premise at position 1 assigning a different value to same species. Exploratory n=4/cell, confirmatory n=50/cell (bumped from n=20 on 2026-04-22 — see `pri-v3-plan.md` Amendments).
- [x] Layers probed: `final`, `mid`, `quarter` (1/4 depth).
- [x] Operational definition of v2: additive `S_t + α · d_F`; `d_F` computed as diag / full / topk{5,10,32} / lowrank{10,32,50}.
- [x] Current best AUROC per model (step 1 / final / α=1.0): Llama 0.7666 (topk32), Mistral 0.6715 (topk32), Qwen 0.7858 (lowrank32). Filed in `wiki/results/summary.md`.
- [x] Hedges g + bootstrap p per model — extracted 2026-04-14 to `wiki/results/summary.md`.
- [x] Per-variant (not just best) AUROC table per model — same; full table in `summary.md`.

## 4. Research-direction decisions
- [x] **Autoresearch: retired 2026-04-14.** Tier-1/2/3/4/5 queue survives as manual protocol.
- [x] **SUP sealing: relaxed 2026-04-14.** SUP corpus now readable/citable as theoretical provenance.
- [x] Paper-vs-parquet discrepancy: **RESOLVED 2026-04-14** — root cause confirmed (step-0 h_prev bug). Parquet authoritative.
- [ ] Next-leg focus: **SUP spectral-band gate** (pre-v3) → v3 build per [v3-code-map](../pri-v3/v3-code-map.md).
- [ ] Extend baseline table with: **Gemma 3-1B** (tiny cross-scale), **Gemma 3-4B** (within-family scale axis paired with 1B — *added 2026-04-21*; slugs confirmed `mlx-community/gemma-3-{1b,4b}-it-4bit`), **Qwen3-8B-MLX-4bit** (newer-gen successor to Qwen 2.5 7B, reasoning-mode), **Phi-3.5-mini (3.8B)** (cross-architecture diversity). **gpt-oss-20b dropped 2026-04-14** — too heavy for Mac mini M4 under mlx-lm.
- [x] Ingest remaining Furnace papers: pre-SUP-split + post-split (PRI-only) — both filed under `raw/papers/furnace/`, summaries in `wiki/papers/`.
- [ ] Target venue / timeline for v3 paper (if writeup leg)

## Minimum viable to start next leg — STATUS (2026-04-14)
Core sources, code pointers, ground-truth facts, per-variant baseline, and paper summaries are populated. Paper-vs-parquet discrepancy resolved (step-0 h_prev bug). Remaining gates before v3 build:
1. **SUP spectral-band validation** — script drafted at `PRI_at_commitment/scripts/sup_spectral_band.py`, scaffold at [results/sup-spectral-band](results/sup-spectral-band.md). Decides whether SUP's λ_max/λ_mean ∈ [10², 10⁴] claim holds in Furnace. Outcome shapes v3 priors.
2. Extend `PRI_V2_PRE_RUN_AUDIT_CHECKLIST.md` with v3 §12 (per [v3-code-map § 8](../pri-v3/v3-code-map.md)) — sign invariance, rank consistency, energy monotonicity, layer-index alignment, **step-0 h_prev source-binding** (regression guard for the bug).
3. Implement `null_ratio` on `PRIComputer` (NOT `pri_metrics.py` — that file is vestigial; see [v3-code-map](../pri-v3/v3-code-map.md)).
4. Smoke-test new model adapters (Qwen3-8B, Gemma-3-1B, Phi-3.5-mini) before committing to full runs.
