# Commit-Confluence — Registered Sealed Run Verdict (2026-06-11)

**Status:** `[SEALED — REGISTERED]`. Fresh seed **20260612**, 10 models × {ANLI R1, TriviaQA paired} = **20 cells**, n=200 each. Clean run: `incomplete=False`, `errors=0`, `is_registered_cohort=True`, `is_preview=False`, all shuffled-label controls passed (`control_failures=[]`). Executed from the public tag `prereg-seal-20260612` (commit `83dfb6f`, repo [commit-confluence](https://github.com/flowstyleliving/commit-confluence)). Survived four adversarial passes before launch (Opus S-series, Opus C-series, Codex M-series, Codex v5).

## Headline (lead with the geometric claim — reporting convention S6)

- **SECONDARY (geometric-only) — `[PASS]` 18/20** (bar ≥17/20). A dispatcher restricted to the geometric families (ACE attention + null_ratio + RPV, **confidence excluded**) is OOB-deployable (CI_lo > 0.50) on 18 of 20 cohort cells. The registered geometric-science claim **holds**.
- **PRIMARY (full panel incl. confidence + fusion) — `[FAIL]` 18/20** (bar ≥19/20). The strict product claim allowed ≤1 non-deployable cell and predicted exactly one (`gemma-3-4b/anli`). A **second** orphan appeared, so the strict 19/20 bar is missed by one. Per the pre-registered falsification rule (≥2/20 non-deployable → NO-GO for the product claim), the strict PRIMARY claim is **falsified**.

## The decisive finding: confidence adds nothing; the holes are genuine epistemic orphans

PRIMARY (the larger panel — geometric **+** confidence **+** fusion) and SECONDARY (geometric only) land on the **same 18/20**, failing the **identical two cells**:

| Non-deployable cell | PRIMARY CI_lo | GEOMETRIC CI_lo | Note |
|---|---|---|---|
| `gemma-3-4b/anli_r1` | 0.400 | 0.403 | **Predicted** orphan (pre-reg §Endpoints): nested-OOB is stricter than Stage A's marginal; surprise CI_lo 0.55→0.45, not deployable even with confidence. |
| `Llama-3.1-8B/anli_r1` | 0.468 | 0.479 | **New** orphan. The one cohort model with **no prior ACE seal** (fresh-only, flagged in pre-reg §Cohort for interpretation); lands just under 0.50. |

Adding the confidence base (surprise/p_max) and the cross-locus fusion cells did **not** rescue either cell. These are not places where geometry is blind and confidence backstops — they are cells deployable by **no cell in the 29-panel at all**. Coverage = 18/20 whether or not you include confidence: **geometry alone is as good as geometry+confidence on this cohort**, which is a positive statement for the geometric thesis, not a hole in it.

Both failures are on **ANLI** — coverage is **10/10 on TriviaQA, 8/10 on ANLI**.

## No universal cell — the per-deployment thesis, made vivid

The geometric win-map is **dispersed across 12 distinct winning cells** over the 18 deployable cells — exactly the "panel of specialists, one honest dispatcher" claim. Every family wins somewhere:

| n | winning cell | family |
|---|---|---|
| 3 | `attention[final_bos_mass]` | ACE |
| 2 | `attention[mid_v_norm_lastq_weighted]` | ACE (v-norm) |
| 2 | `attention[final_v_norm_lastq_weighted]` | ACE (v-norm) |
| 2 | `attention[last_minus_1_js]` | ACE |
| 2 | `attention[final_js_kv_groups]` | ACE |
| 2 | `Readout fisher_eff_rank` | RPV |
| 2 | `Fusion fusion_rank_mean_geom` | E4 fusion |
| 1 | `Readout spectral_entropy` | RPV |
| 1 | `Readout neg_shadow_logvol_r1` | RPV |
| 1 | `attention[last_minus_1_bos_mass]` | ACE |
| 1 | `attention[final_js_no_bos]` | ACE |
| 1 | `attention[last_minus_1_v_norm_lastq_weighted]` | ACE (v-norm) |

ACE attention cells carry most deployable cells; the RPV family (fisher_eff_rank / spectral_entropy / neg_shadow_logvol) covers 4 cells where attention does not; the pre-registered **fusion** cell wins 2 outright. Corroboration **with** complementarity — no single cell generalizes across the cohort.

## Interpretation

The registered claim splits cleanly, and the split is the honest one the multi-pass hardening was built to protect:

1. ✅ **Geometric dispatcher works** (18/20, bar cleared). A confidence-free, W_u-light geometric panel under an honest nested-OOB selector is deployable on the large majority of the cohort.
2. ❌ **The strict product claim does not** (18/20 vs bar 19/20). The honest selector does not recover *gap-free* coverage; two ANLI cells are deployable by nothing in the panel.
3. 🔑 **Confidence is not the backstop** — it never moved the needle on the orphans. The orphans are genuine epistemic dead zones at the commit moment for those (model, task) pairs.
4. 🧭 **No universal cell** — 12 winners / 18 cells; per-(model, exact deployment distribution) calibration remains the only honest framing, now demonstrated on a fresh-seed registered run rather than asserted.

## Descriptive analyses (pre-registered, non-gating; complete 2026-06-12) — `stage_b/universality.json`

- **E1 — partial universality (FIRST positive in the program).** Pool 9 models to pick one fixed signal, evaluate on the held-out 10th. The cross-locus **fusion** signal (`fusion_rank_mean_geom`) clears the pre-registered ≥8/10 bar on **both** tasks: ANLI **9/10**, TriviaQA **10/10** holdouts at AUROC > 0.55. No universal *champion* signal, but a universal **above-chance floor** — the rank-mean aggregate is variance-reduced, so it's the most cross-model-stable signal even though it rarely wins any single deployment outright. Caveat: 0.55 ≈ "beats chance"; holdout AUROCs span 0.54–0.95 (ANLI weaker, TriviaQA stronger).
- **E2 — task transfer.** Apply each model's per-task winner across tasks: median transfer AUROC **0.6731**, above-floor on **85%** of transfers. Per-*model* calibration is a decent (not perfect) cross-task proxy — the "/task type" requirement is partial, not absolute.
- **E3 — label-efficiency** (registered: repeats=10, nboot=1000). Mean fraction of deployments deployable vs labeling budget: **geometric 0.445 → 0.665 → 0.790 → 0.90** at n = 50 / 100 / 150 / 200; **full-panel 0.485 → 0.705 → 0.805 → 0.90** (tracks +0.01–0.04). Knee ~n=100; n=50 is below a coin flip; **~150–200 labels** stands up a new deployment. (The reduced preview repeats=3/nboot=200 read ~0.02–0.04 higher — honest calibration corrects downward.)

**Refined thesis:** no universal *best* signal, but a fixed aggregate gives a universal above-chance *floor*; per-model calibration transfers across tasks ~85% of the time; full strength still needs per-deployment calibration at ~150–200 labels.

## Artifacts
- Repo (public): https://github.com/flowstyleliving/commit-confluence — pre-reg snapshot tag `prereg-seal-20260612` (run executed from here); results tag `registered-results-20260612`; HEAD carries registered E3 + published matrices.
- Published results: `stage_b/profiles/` (`SUMMARY.json` + 20 per-deployment `*.profile.json` + 20 `*.matrix.npz` + `run.log`) and `stage_b/universality.json` (E1+E2+E3). The matrices make E1/E2/E3 **independently reproducible from the repo alone** (no models / no private deps).
- Pre-registration: `commit-confluence/stage_b/PRE_REGISTRATION.md` (Amendments v1–v5).
- README uses "deployment" (the /20 (model,task) box) vs "signal" (the /29 panel entry); "PRI" for the v3 `null_ratio` detector.
