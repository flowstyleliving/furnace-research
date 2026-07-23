# BENCH A2 — registered transfer verdict and the intrinsic sign-flip (2026-07-22)

**Status:** 🧭 **[REGISTERED — CONFIRMATORY]** · Family-A split verdict from the BENCH strict Phase-4 run (seed 20260711, nboot 2000).
**Companion:** [[log]] 2026-07-22 · pre-reg `commit-confluence/stage_b/PRE_REGISTRATION_BENCH.md` · artifacts `stage_b/profiles_bench/{SUMMARY.json,A2_REGISTERED.json}`

---

## Verdict in one line

The rupture geometry separates hallucinated from faithful answers in **all ten** models — but **its direction is model-dependent**. Per-model calibration deploys (**A1 PASS 10/10**); one frozen cell + frozen sign shipped blind does not (**A2 FAIL 6/10**, bar ≥8). *No universal sign — not no signal.*

| Endpoint | What it asks | Result |
|---|---|---|
| **A1** | Calibrated on *its own* labels, is each model deployable on halueval_qa? | **PASS 10/10** (bar ≥8); weakest cluster CI-lo 0.6705 |
| **A2** | Freeze cell `fusion_rank_mean_geom` + fit ONE sign on 9 models, apply blind to the 10th | **FAIL 6/10** (bar ≥8), `aborted=false` |

The pre-registered **A1∧A2 conjunction is therefore NOT satisfied**: the claim "the floor extends to HaluEval-QA" is licensed only in its per-model-calibration form, not as a transferable fixed detector.

---

## Why A2 fails: an intrinsic sign-flip, not signal absence

All A2 holdouts are scored with `fitted_sign = −1` (the pool majority). The four failures land **far below** 0.5 — meaning the detector is not blind but **reliably backwards**:

| Holdout | A2 AUROC (fixed −1) | Own sign | If sign reversed |
|---|---:|:--:|---:|
| Llama-3.2-3B | 0.873 | −1 | — |
| Llama-3.1-8B | 0.825 | −1 | — |
| gemma-3-4b | 0.850 | −1 | — |
| Phi-4-mini | 0.724 | −1 | — |
| Qwen3-1.7B | 0.577 | −1 | — |
| Qwen3-8B | 0.583 | −1 | — |
| **Mistral-7B** | **0.174** | **+1** | 0.826 |
| **Mistral-Nemo** | **0.206** | **+1** | 0.794 |
| **Qwen2.5-7B** | **0.276** | **+1** | 0.724 |
| **Phi-3.5-mini** | **0.394** | **+1** | 0.606 |

**Crucially, reversing the sign is not a rescue.** To know a model needs the flip you must consult that model's own labels — the very thing the detector predicts. Doing so *is* A1 (which is allowed to peek, and passes 10/10). A2's question is whether one frozen orientation serves everyone; the answer is no.

---

## Ground-truth verification (not read off a summary)

The sign-flip was confirmed **from the raw matrices**, not from derived endpoint numbers. Method: load each model's `*.matrix.npz` (27-column panel + labels), rebuild the fusion column by **importing the production `append_fusion_columns`** from `confluence_calibrator.py` (no reimplementation), then compute the label relationship directly. The reconstruction reproduces the registered A2 holdout AUROCs to three decimals — the self-check that the right object is being inspected.

**Mean fused score by answer type** (fused rank in (0,1); n=1000/model, 500/500 balanced):

| Model | faithful (y=0) | hallucinated (y=1) | Higher score belongs to |
|---|---:|---:|---|
| Llama-3.2-3B | **0.619** | 0.382 | faithful |
| Llama-3.1-8B | **0.615** | 0.386 | faithful |
| gemma-3-4b | **0.634** | 0.366 | faithful |
| Phi-4-mini | **0.567** | 0.433 | faithful |
| Qwen3-1.7B | **0.522** | 0.479 | faithful |
| Qwen3-8B | **0.520** | 0.480 | faithful |
| Mistral-7B | 0.369 | **0.631** | hallucinated |
| Mistral-Nemo | 0.435 | **0.565** | hallucinated |
| Qwen2.5-7B | 0.423 | **0.578** | hallucinated |
| Phi-3.5-mini | 0.469 | **0.532** | hallucinated |

**Walk one number.** In Llama-3.2-3B a *faithful* answer averages a fused rank of **0.62** and a *hallucinated* one **0.38** — high geometry means faithful. In Mistral-7B the same quantity reads **0.37** faithful / **0.63** hallucinated — the exact mirror. Same formula, opposite polarity, visible in the raw row means.

The four models whose own means point the opposite way are **exactly** the four A2 failures. The flip is intrinsic to the model↔label relationship, not manufactured by pooling.

**Why pool AUROCs sit near chance (0.512–0.590):** sign heterogeneity cancels under equal-weight within-model ranking. When a `+1` model is held out the pool is 3 `+1` vs 6 `−1` and rises to 0.565–0.590; when a `−1` model is held out it is 4 vs 5 and collapses to 0.512–0.545. `_score_candidate` reports direction-agnostic `max(AUC, 1−AUC)` (`sealed_selector.py:53`), so already-oriented pool values near 0.5 are especially diagnostic.

---

## Structure: generation-split polarity, not a family law

| Family | Models | Own sign | Reading |
|---|---|:--:|---|
| Llama | 3.2-3B, 3.1-8B | −1, −1 | internally consistent — both hold |
| Mistral | 7B, Nemo | +1, +1 | internally consistent — **both flip** |
| Qwen | 2.5-7B / 3-1.7B, 3-8B | +1 / −1, −1 | **splits by generation** |
| Phi | 3.5 / 4 | +1 / −1 | **splits by generation** |
| Gemma | 3-4b | −1 | holds |

Mistral and Llama are family-coherent; Qwen and Phi split across generations. With only 1–2 representatives per subgroup, and family confounded with tokenizer / architecture / size, this stays **descriptive** — a real model-structured polarity pattern in these artifacts, not yet a causal family law.

### [OPEN — observation] The flip cluster overlaps the v4 partial-transfer cluster

The sealed v4/ACE run recorded **E_A2: 3/9 partial transfer — Mistral-7B, Mistral-Nemo, Qwen2.5-7B** as the only models whose winning cell matched exactly across ANLI→TriviaQA ([[research-candidates]] §5, [[results/v4-sealed-2026-05-26]]). Those are **exactly three of the four models that flip sign here** (the fourth being Phi-3.5). Two different experiments, two different tasks, the same three-model sub-cluster behaving distinctly from the rest of the panel.

This is **descriptive and untested**: with 10 models and 4 flippers the overlap could be coincidence, and the two properties (cell-transfer stability vs orientation) are not obviously the same axis. Flagged because it is cheap to check and would be a sharp result if it holds — a candidate "geometry sub-family" that cuts across the Llama/Mistral/Qwen/Phi naming. Do not state as a finding without a designed test.

### Precedent in the vault — this is a confirmation, not a surprise
- [[results/triviaqa-pilot-2026-05-25]] — sign flip on Llama (`mid_js_no_bos` −1→+1 across tasks); verdict already "calibrator viable, **no universal cell**".
- [[results/delta-sigma-onaxis-2026-05-15]] — Δσ_n alone beats null on **Phi-3.5 (−)** and **Phi-4 (+)** with *opposite signs*. Independent corroboration of the same Phi generation split found here.
- [[results/rauq-sinkprobe-vs-ours-2026-05-16]] — RAUQ sign-flip on Nemo / Qwen3-8B; "baselines disagree in direction".
- [[results/llama-70b-scale-2026-06-22]] — family dissociation in signal *locus* (Qwen→attention, Llama→readout). A2 adds a dissociation in *orientation*.

---

## Framing refinement (honor in paper and talk)

This establishes **no universal fixed orientation**, and — with eight distinct A1 winners across ten models — no universal *best* cell. It does **not** establish the absence of a common informative cell: `fusion_rank_mean_geom`, given a per-model sign, clears >0.55 on **all ten** models. A2 rejects the compound **"fixed cell + fixed sign"** deployment, not cell identity.

Licensed claim: *halueval_qa is deployable under per-model calibration (A1 10/10); a frozen cell+sign does not transfer leave-one-model-out (A2 6/10), the four misses being intrinsic sign inversions in Mistral ×2, Qwen2.5, and Phi-3.5.*

---

## Confounds checked (all clear)

- **Sign application consistent** — cell ranked within model (`analyze_universality.py:231`), one sign fit on concatenated training scores (`:260-262`), holdout multiplied by exactly that sign (`:52-59, 266-274`). No holdout-side refit.
- **No per-model label polarity** — all ten NPZs share identical `labels`, `sample_idx`, `stem_ids`, balanced 500/500, same `data_file_sha256`. Builder maps right answer→0, hallucinated→1 (`generate_bench_data.py:230, 265-267`).
- **No hidden per-model fusion polarity** — all ten profiles report every component `source="modal_fallback"` with identical orientations; fusion = mean of oriented component ranks (`confluence_calibrator.py:358`).
- **Commit parsing gates validity only** — every halueval_qa profile has `n_canonical=1000, n_noncanonical=0`; the audit sets terminal status and does not alter scores. Mistral-7B's `Y` prefix vs Nemo's `YES` differ, yet both flip; ordinary YES/NO models Qwen2.5 and Phi-3.5 also flip.

**Caveats.** Point estimates on one fixed dataset; no A2 confidence interval and no cell-specific independent replication. Phi-3.5's reversed AUROC (0.606) is only modest. Family is confounded with tokenizer/generation/architecture/size.

---

## Provenance

Ten registered `mlx-community/*-4bit` models, one module-hash set, Phase-1 frozen-row byte parity passed; no torch / mlx-vlm cell enters these counts (do not pool with the non-byte-comparable panels in [[results/llama-70b-scale-2026-06-22]] or [[results/qwen32b-stress-2026-06-25]]). Post-A4 manifest `e5266ba7…`. Sealed [[results/confluence-seal-2026-06-11]] (geom 18/20 PASS) is **byte-unperturbed** — Phase 4 wrote only under `profiles_bench/`.

A2 scored by `./confluence analyze --profiles-dir stage_b/profiles_bench --bench-a2` (executor: Claude Code / MK; analyzes existing profiles, no re-calibration). Reviews: fresh-eyes read (fable), Codex static audit, Codex `gpt-5.6-sol` high-reasoning sign-structure read — all read-only, no files edited.

**Related:** the same run's B1 replication reads 7/20 FAIL as a pre-registered §4/§8.1 commitment-audit cascade with geometry intact — a separate matter, recorded in [[log]] 2026-07-22.

---

## Housekeeping closeout (2026-07-22, post Codex `gpt-5.6-sol` audit)

The provenance/documentation pass that followed the verdict, after a read-only adversarial audit found 1 CRITICAL + 7 MAJOR defects in a first attempt. Corrected:

- **Lifecycle filename falsification (CRITICAL).** A re-attestation exit file was written under `strict_phase4_a4.{exit}` — the name the pre-registration *reserves* for the original 2026-07-15 detached run, which never wrote it. Renamed to `resume_reattest_2026-07-22.{exit,log}`; the original A4 exit is recorded as **NOT CAPTURED / unrecoverable**, never manufactured.
- **Provenance sidecar (schema 1.1).** `profiles_bench/PROVENANCE.json` now binds 53 matrices + 53 profile JSONs + 4 sidecars + 7 lifecycle logs, with expected counts, matrix↔profile pairing, and a `known_analysis_defects` entry. Enforced by `stage_b/verify_bench_provenance.py` (exit 0/1/2; rejects tamper, bad schema, unsafe paths) + a CI workflow. Verifies **repository coherence, not an execution-time signature** — this is stated plainly in the file. Verifier PASS: **117 files**.
- **Resume re-attestation, stated honestly.** `./confluence resume-bench` reconstructed all 60 dispositions (validated 53 stored profiles structurally — arrays, panel/stem digests, commitment tokens; **not** NPZ-byte or endpoint revalidation — and reused 7 stored smoke records), ran **no model forward**, and rewrote `SUMMARY.json` byte-identically (no `ERROR` cells: 46 OK / 7 BEHAVIORAL-FAIL / 7 COMMITMENT-FAIL). Exit 0 alone is **not** the evidence — the absence of ERROR cells is.
- **E2 is structurally N/A here.** `transfer()` (`analyze_universality.py:292`) is defined only for **exactly two tasks**; the 6-task BENCH directory returns `skipped`, and the printed `None` is an interface artifact, **not** a measured transfer result. BENCH E2/E3 are kept **internal** (not published).
- **E3 stem-splitting — fixed in effect, defect noted.** Every grouped BENCH task (TriviaQA, HaluEval ×3) enters the `stem` path; only genuinely ungrouped ANLI uses `row`. Residual future-version defect: on a task *declared* grouped whose stem metadata is unrecoverable, `_e3_subsample` fabricates unique row IDs and the uniqueness assertion validates the fabrication → silent row fallback. Analyzer is hash-frozen (already executed for A2) — recorded, **not** patched post hoc.
- **Stale portability + gate artifacts.** The "MK-machine-only / absolute-path" README block was obsolete after Amendment A3 (content-hash resolution; only the HaluEval raw file stays path-bound) — rewritten. `GATE_FAILURES.json` (Jul 14) renamed `→ GATE_FAILURES.2026-07-14.superseded.json` (gates now pass: the resume ran `gate_tasks()` and wrote no active failure file).

**Sealed TriviaQA stem-cluster sensitivity (descriptive, non-gating; does NOT alter 18/20).** The "clustered inference owed" limitation is descriptively discharged for TriviaQA: re-scoring the sealed cells with the **question stem** as the exchangeable unit keeps **10/10 deployable** (weakest geometric CI-lo **0.5830** `Qwen3-1.7B`, strongest **0.9408** `Mistral-Nemo`; full-panel weakest 0.6983). Artifact `stage_b/cluster_sensitivity.{json,md}`. A *registered* clustered endpoint on fresh data is still owed.

**Two forward-only documents drafted (Codex, proposed — NOT filed).** `stage_b/PRE_REGISTRATION_BENCH_A5_FUTURE.md` (per-cell commitment-error budget + widened acceptable-answer template + blip-vs-behavior split; governs a future run only, after sign-off + hash + commit before any new outcome data — **July 22 remains B1=7/20**) and `stage_b/SIGNFLIP_COINCIDENCE_DESIGN.md` (a **designed-retrospective** Fisher-exact screen for the flip-trio = v4 E_A2-trio observation — halueval_qa excluded, predictor frozen first; **not a finding**).
