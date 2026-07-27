# Results Summary (running, in-place)

_Last updated: 2026-07-26 ([R4] naming diagnostic built + a retracted degeneracy claim; E3-HaluEval descriptive label-cost sweep — knee at 150 labels, 10/10 flat to 500, HaluEval-QA descriptively cheaper than the sealed tasks; cc-draft ↔ cc-extend merged into one comprehensive paper. Same day: empathy-geometry cell panels now run standalone in the EG repo, bit-identical to the sealed venv — 174/174 values, delta exactly 0.0). Prior: 2026-07-25 t0 sweep → unscored KV-tension pilot scored NO-PROMOTE; sign-flip↔E_A2 coincidence screen NULL. Detail in [log](../log.md) tail._

## The [R4] naming diagnostic — built, reviewed, and one retraction (2026-07-26)

Instrument, not a result; no empathy-geometry data exists. Full detail: [eg-flattery-gate-2026-07-26](eg-flattery-gate-2026-07-26.md).

- **Purpose:** the judge's `need_met` is the first-person endpoint, so a judge that merely agreed with the giraffe arm would manufacture the headline result. Any claimed landing must be **named**, and beat a permutation floor.
- **RETRACTION worth more than the build.** I claimed the pre-registered target-swap null was fatally degenerate: the two personas per bundle hold disjoint need sets, so a swap zeroes a dialogue, the floor becomes `A × fraction-unswapped` (≈0.63–0.83·A), and `A ≤ floor` is unsatisfiable. **Wrong** — that premise holds only for an *already chair-informative* judge, which is the alternative. Under H0 the floor rises to meet the accuracy and the gate fires correctly. **The error was adopting a floor formula derived under H1 as though it described the null distribution.** Simulation across informativeness 0.0→1.0: both nulls agree on every verdict.
- **So the switch to answer-shuffling is an improvement, not a repair** — finer resolution (multiset orderings vs `2**n_dialogues`) and preserved naming marginals. The target-swap null is **retained** as a pre-registered sensitivity analysis.
- **First implementation scored 3.5/10** on adversarial review. Worst defect: `acceptance_grade = not underpowered`, so a cell with *confirmed* flattery was still acceptance-grade. Also: degeneracy inferred from labels rather than achieved scores (which mis-certified one of my own fixtures), zero-met rows raising instead of stamping underpowered, and a seed-fragile random fixture. Rebuilt.
- **Amendment A1 filed pre-run.** Along the way: `artifacts/` was gitignored wholesale, so the **pre-registration document itself was untracked** — an unversioned pre-reg can be edited without trace. Fixed.
- Verified on the real B2 personas via `eg-harness flattery-gate`: faithful judge exit 0; wrong-persona judge suspected and blocked at exit 1. Suite 152 passed.

## Empathy-geometry cell panels run standalone — bit-identical parity (2026-07-26)

Infrastructure, not a detector result. The geometry half of the empathy-geometry harness was pinned to a borrowed interpreter (`t0-morphology-furnace/.venv`, py3.9), which is why the hosted judge could not run where the geometry ran. Full detail: [eg-standalone-panels-2026-07-26](eg-standalone-panels-2026-07-26.md).

- **New `capture-panel` command** runs the 21-cell t=0 ACE panel + gen-step-1 readout on plain prompts — **no dialogue, no persona bundle, no judge**. Replay mode consumes a recorded `first_token_id`, so no sampler runs and the capture is two deterministic forward passes.
- **Bit-identical, not merely within tolerance:** EG venv (py3.11.15 / numpy 2.2.6) vs sealed venv (py3.9.6 / numpy 2.0.2), **174 values across 6 rows, worst relative delta 0.000e+00**, covering the full attention panel and the five strict gen-step-1 metrics.
- **The sealed checkout is now read-only** — an import source and parity reference. `t0-morphology-furnace` verified clean and A0 PASS afterward.
- **Three couplings removed:** geometry no longer needs a judge; `pyproject.toml` now declares the full third-party closure of the sealed modules it imports (pandas and scikit-learn are geometry deps — `pri_runtime` imports both at module load); and the ad-hoc monkeypatching fixture producer in `artifacts/` is replaced by tested commands.
- **Scope:** 6 rows, one bundle/arm (B2/giraffe), one model (Qwen2.5-7B-4bit). Says the *instrument* transfers across interpreters; says nothing about empathy geometry.
- **Adversarially reviewed the same day, and two claims were corrected.** The comparator ran at rtol 1e-5 and reported "worst delta" over *failures only* — trivially 0.0 whenever nothing failed, so "bit-identical" was asserted, not tested; and "the claim cannot rot" was false because the regression test never invoked the capture path. Both fixed: exact mode (`--rtol 0 --atol 0`), maxima over **all** comparisons, `bit_identical` reported separately, honest scope in the README. **Re-verified with a fresh capture: `bit_identical: true`, max delta 0.0, 174 values** — and the comparator now demonstrably rejects a single-ULP (1.7e-21) perturbation. Also fixed: echoed canonical `surprise` renamed, `numpy` pinned, degenerate-input holes closed. Suite **113 passed** (was 69 pre-session).

## Attention KV-tension pilot — NO-PROMOTE, found six weeks late (ran 2026-06-08, scored 2026-07-25)

ACE follow-up asking whether attention signal lives in query-head disagreement or in disagreement among the shared KV groups. Completed 5-model pilot (ANLI R1, t=0, n=200, nboot 1000) that sat **uncommitted and unscored** in `t0-morphology-furnace` until the repo was swept clean for the packaging work. Full detail: [kv-tension-pilot-2026-06-09](kv-tension-pilot-2026-06-09.md).

- **None of the three registered promotion limbs is satisfied.** ≥+0.03 over the best comparator on 2/5 models against *routing cells only*, **0/5** against *any* existing ACE cell; `winner_unstable` fires on **4/5** (including both models carrying the win); the **shuffled-label control was never run**.
- **The BOS/sink falsification clause is partially triggered** — on Qwen2.5-7B the selected winner is `final_bos_mass`, beating the best KV-tension cell by 0.0261.
- **Warm on GQA, dead on gemma-3-4b** (−0.0521, OOB CI-lo 0.4960 — not even clean). Best cells: Qwen3-8B 0.8479, Mistral-7B 0.8065, Qwen2.5-7B 0.7535, Phi-4-mini 0.7374.
- **Process finding worth more than the result:** the verdict flips on whether `bos_mass` counts as a "routing comparator" — 2/5 versus 0/5 on identical numbers. The pre-registration never enumerated the comparator set. Future registrations must name the cells.
- Companion lane **v-norm-attention** `[RESOLVED — NO-PROMOTE]`: last-query V-norm cells add nothing over routing-only ACE across all 18 sealed profiles (mean −0.0436, 0/18 at ≥+0.02).
- Both lanes now live in `commit-confluence/exploratory/`; `t0-morphology-furnace` is sealed-archive-only as of 2026-07-25.

## BENCH strict Phase-4 — FAMILY-A SPLIT: A1 PASS 10/10, A2 FAIL 6/10 (intrinsic sign-flip) (2026-07-22)

Registered confirmatory run, seed 20260711, nboot 2000, 10 models × 6 tasks. Full detail: [bench-a2-signflip-2026-07-22](bench-a2-signflip-2026-07-22.md). Sealed 18/20 **byte-unperturbed**.

- **A1 PASS 10/10** (bar ≥8) — halueval_qa per-model cluster-geometric deployability; all ten OK, controls pass, n=1000 / 500 stems, zero drops, zero non-canonical commitments; weakest cluster CI-lo 0.6705.
- **A2 FAIL 6/10** (bar ≥8, `aborted=false`) — fixed cell `fusion_rank_mean_geom` with ONE sign fit on the 9-model pool, applied blind leave-one-model-out. ⇒ the pre-registered **A1∧A2 conjunction is NOT satisfied**; "the floor extends to HaluEval-QA" is licensed only in per-model-calibration form, not as a transferable fixed detector.
- **The failure is a sign-flip, not signal absence.** The four misses sit far *below* 0.5 — Mistral-7B **0.174**, Mistral-Nemo **0.206**, Qwen2.5-7B **0.276**, Phi-3.5 **0.394** — i.e. confidently backwards. Each independently selects `+1` in its own calibration while all six passers select `−1`; reversing rescues them (0.826 / 0.794 / 0.724 / 0.606). Reversal is **not** a rescue for A2: knowing to reverse requires the holdout's labels, which is exactly what A1 is permitted to use and A2 is not.
- **Verified from raw matrices, not summaries.** Fusion column rebuilt per model by importing the production `append_fusion_columns`; reconstruction reproduces the registered A2 AUROCs to 3 dp. Mean fused rank faithful-vs-hallucinated mirrors exactly: Llama-3.2-3B **0.62 / 0.38** (high = faithful) vs Mistral-7B **0.37 / 0.63** (high = hallucinated).
- **Polarity is generation-split, not a family law.** Mistral (both +1) and Llama (both −1) are family-coherent; **Qwen and Phi split by generation** (Qwen2.5 flips, Qwen3 holds; Phi-3.5 flips, Phi-4 holds). Corroborated independently by [delta-sigma-onaxis-2026-05-15](delta-sigma-onaxis-2026-05-15.md), which already found Phi-3.5 (−) vs Phi-4 (+) on a different diagnostic. Descriptive only — 1–2 reps per subgroup, family confounded with tokenizer/architecture/size.
- **Framing refinement:** this establishes **no universal *orientation*** (and, with 8 distinct A1 winners across 10 models, no universal *best* cell) — but NOT the absence of a common informative cell: `fusion_rank_mean_geom` with a per-model sign clears >0.55 on all ten. A2 rejects "fixed cell **+ fixed sign**", not cell identity.
- **[RESOLVED — screened NULL 2026-07-25]** the three-model flip cluster (Mistral-7B, Mistral-Nemo, Qwen2.5-7B) is exactly the v4 sealed **E_A2 partial-transfer** trio — the frozen designed-retrospective Fisher-exact screen ran 2026-07-25 and found **no association** (two-sided p = 0.50; positive-orientation majority is the cohort norm 7/9; non-trio Phi-4 sign-identical to both Mistrals). Coincidence at this resolution; no follow-up motivated. [[results/signflip-coincidence-2026-07-25]].
- **[RESOLVED — descriptive 2026-07-26]** **HaluEval-QA label cost: a measured knee at 150 labels.** Post-hoc stem-aware sweep on the published matrices (spec pre-committed): **10/10 models at full subsample deployability by 150 labels, flat through 300/500**; 9/10 already at 100. Last to certify = weakest A1 cell (Qwen3-1.7B). Descriptively *cheaper* than the sealed tasks (still rising at 150 there); sign-flippers not label-hungry — orientation is cheap to fix per-model, it just can't be transferred (A2 stands). NOT a registered endpoint. [[results/e3-halueval-descriptive-2026-07-26]].
- **Housekeeping closeout (2026-07-22, post Codex `gpt-5.6-sol` audit).** Provenance sidecar upgraded to schema 1.1 + enforced verifier (`verify_bench_provenance.py`, 117 files PASS) + CI; a re-attestation file misnamed after the original A4 run was renamed `resume_reattest_2026-07-22.*` (original A4 exit = NOT CAPTURED, never manufactured); stale portability/gate blocks corrected; E2 confirmed structurally N/A on a 6-task dir (BENCH E2/E3 kept internal). **Label-cost correction:** the "~150–200 labels" figure is retired everywhere (paper, README, [e3-stem-aware](e3-stem-aware-2026-07-14.md)) — E3 only measures {50,100,150}, no n=200 point exists, and the curve is still rising at n=150 ⇒ **≥150 is a measured lower bound, not a knee**. **Sealed TriviaQA stem-cluster sensitivity (descriptive):** 10/10 hold under the question-stem unit (weakest geom CI-lo 0.5830) — the clustered-inference concern is descriptively discharged for TriviaQA; a *registered* clustered endpoint on fresh data is still owed. An **A5** amendment (per-cell commitment budget + blip-vs-behavior split) is drafted **proposed, not filed**.
- **B1 replication reads 7/20 FAIL — a pre-registered gate cascade, NOT a geometric collapse.** `_endpoint_value` zeroes every cell of any task with ≥3 COMMITMENT-FAIL cells (§4 zero error budget × §8.1 systematic abort), so all 10 triviaqa cells — including 7 terminal-status-OK — are forced False. Layers: raw geometry **18/18 deployable** (CI-lo 0.6577–0.9804) → pre-cascade **14/20** → post-§8.1 **7/20**. Triggers are rare (Llama-3.1-8B 1/1000, Qwen3-1.7B 1/1000, gemma-3-4b 12/1000). Frozen pre-reg; not softened retroactively, and **not propagated as a signal negative**.

## Commit-Confluence scale/family extension — ORPHAN = SCALE ARTIFACT (2026-06-18)

Pre-registered, **byte-comparable** out-of-sample extension (module hashes identical to seal, same seed 20260612 / fresh data / n=200 strict / nboot=2000, existing adapters, no sealed-core edit). Does **not** alter the sealed 18/20. Full detail: [gemma-scale-extension-2026-06-18](gemma-scale-extension-2026-06-18.md).

- **`gemma-3-4b/anli` orphan resolved as scale:** sealed geom CI_lo **0.403 (FAIL)** → `gemma-3-12b/anli` **0.709 (PASS)**. Scaling gemma-3 4B→12B recovers ANLI deployability.
- **Family control rules out generic-12B:** `Qwen2.5-14B/anli` **0.766 (PASS)** → the 4B failure was gemma-small-specific, not "12–14B can't do ANLI."
- **4/4 new cells deployable:** g3-12b/anli 0.709, g3-12b/trivia 0.929, Qwen-14b/anli 0.766, Qwen-14b/trivia 0.597 (marginal). All winners ACE attention; confidence/fusion never sole winner. All 4 registered predictions confirmed.
- **[CRAB-LOCK 2026-06-20] head-COUNT resolution REFUTED:** within-model ablation starving gemma-3-12b's ACE to the 4b head budget (8h/4kv) keeps ANLI deployable (geom CI_lo 0.709→0.674) — head count explains only ~11% of the 0.31 orphan gap. The orphan is per-head/representation **quality** at small scale, not the number of heads. Honest negative; `stage_b/crab_lock.py`.
- **[GENERATION AXIS 2026-06-21] resolved — orphan does NOT return at gen-4:** `gemma-4-12B` (mlx-vlm extraction, NON-byte-comparable) is **2/2 deployable** — anli_r1 geom **0.691**, triviaqa **0.751**, controls pass, n=200, both Fusion winners. gen-4/anli 0.691 ≈ gen-3-12b/anli 0.709 (both PASS) vs gen-3-4b 0.403 (FAIL) ⇒ orphan is a **scale / small-model gen-3 artifact**, not carried forward by the generation lineage. (Initial ~0.37-on-both was a `raw_passthrough` prompt-format bug: gemma-4-it needs its chat template; fixed.) Wrinkle: both winners Fusion, not ACE-solo. Caveats: non-byte-comparable; readout not parity-validated.

## Torch cloud panel — LLAMA-70B FAMILY DISSOCIATION (2026-06-22)

NON-byte-comparable (Modal + bitsandbytes). Full detail: [llama-70b-scale-2026-06-22](llama-70b-scale-2026-06-22.md).

- **Qwen2.5-32B 2/2 deployable** (anli 0.763, triviaqa 0.781) — ACE attention winner (true-nf4 after bf16 provenance bug caught and fixed 2026-06-23)
- **Qwen2.5-72B 2/2 deployable** (anli 0.639, triviaqa 0.918) — ACE attention winner (inferred nf4, OOM guard blocks bf16)
- **Llama-3.3-70B 2/2 deployable** (anli 0.703, triviaqa 0.788) — **RPV readout-volume winner** — first scale cell where ACE does NOT win. Consistent across both tasks.
- **Family dissociation:** Qwen → attention-morphology (t=0), Llama → readout-volume (gen_step=1). Sharpens "no universal cell" — even the locus isn't universal.
- **Second sealed ANLI orphan resolved:** `Llama-3.3-70B/anli` CI-lo 0.70 (cf. `Llama-3.1-8B/anli` FAIL). Both sealed ANLI orphans now confirmed as scale artifacts across two independent families.

## Qwen2.5-32B stress panel — 8/8 DEPLOYABLE, LOCUS BROADENS (2026-06-25)

Exploratory Modal/torch nf4 stress wave, n=200 per new task. Full detail: [qwen32b-stress-2026-06-25](qwen32b-stress-2026-06-25.md). NON-byte-comparable and does **not** alter the sealed 18/20.

- **Baseline carried forward:** `anli_r1` geom CI-lo **0.763** and `triviaqa_paired` **0.781**, both ACE attention winners.
- **ANLI R2/R3 pass cleanly:** `anli_r2` **0.744**, `anli_r3` **0.698**, both `attention[last_minus_1_bos_mass] @ step 0`; 0 drops, 100% YES/NO, controls pass.
- **TruthfulQA-MC stays attention:** **0.730**, winner `attention[last_minus_1_js_kv_groups] @ step 0`.
- **HaluEval broadens the locus:** QA is strong (**0.809**) but Fusion; dialogue (**0.539**) and summarization (**0.553**) are marginal deployable and move to readout/surprise.
- **Interpretation update:** "Qwen -> attention" remains right for the ANLI/TriviaQA scale panel and TruthfulQA, but broader grounded-dialogue/source-faithfulness prompts can push Qwen-32B into commit/readout-region winners.
- **Caveat:** exploratory row-bootstrap on grouped/stem-paired tasks; HaluEval contexts were char-limited. Treat HaluEval dialogue/summarization as stress signals, not polished confirmatory benchmark claims.

## Precision ladder — H3 FALSIFIED (2026-06-22/23)

Pre-registered confound-elimination test: "is the rupture signal just quantization noise?" Full detail: [precision-ladder-results-2026-06-22](precision-ladder-results-2026-06-22.md), prereg: [precision-ladder-prereg-2026-06-22](precision-ladder-prereg-2026-06-22.md).

- **Qwen2.5-7B × {nf4, int8, bf16, fp32}:** H3 falsified — robust signals are precision-invariant. The signal is real computation, not quantization noise.
- **Qwen2.5-32B × {nf4, int8, bf16}:** Selection instability and int8 degradation are small-model artifacts that wash out by 32B. Cross-precision must be judged on FIXED CELLS, not argmax winner.
- **Caught: 32B bf16 provenance bug.** Pre-patch runs were unstamped. True-nf4 run confirmed and replaced.
- **Format leakage:** 7B bf16 leaks 6.5% non-YES/NO (`To`). By 32B: 0-0.5%. Scale eliminates format failure.

## Orbital prompt ("Answer Anchor") — TECHNIQUE + DISCRIMINATOR TAXONOMY (2026-06-23)

Prompt-engineering method: append `\n\nAnswer:` to raw prompt before chat template. Codex-designed. Full detail: [orbital-prompt-2026-06-23](orbital-prompt-2026-06-23.md).

- **Yi-1.5-34B: +16pp** (72%→88%). `Step` COT leakage fully killed (28%→0%). Does NOT fix `To` preamble.
- **Qwen2.5-7B: +2.5pp** (97%→99.5%). `To` mostly killed at 7B.
- **Llama-3.3-70B: flat** (95%→95%). `To` is IMMUNE at scale — structural, not lazy formatting.
- **Mistral-Large: flat** (57%→58%). Tokenizer subword artifact (`Y`) immune to prompt engineering.
- **Three leak categories:** (1) COT leakage — format compliance, killed by anchor. (2) Preamble leakage — scale-dependent. (3) Tokenizer leakage — vocabulary artifact, immune.

## Commitment convergence — 18.5% DISAGREEMENT CEILING (2026-06-23)

Behavioral-level cross-model first-token analysis. Full detail: [commitment-convergence-2026-06-23](commitment-convergence-2026-06-23.md).

- Cross-family disagreement (19%) ≈ within-family cross-scale disagreement (18%). Same rate.
- Family dissociation in signal LOCUS is genuine — not just answer-disagreement in disguise.
- Universal behavioral floor mirrors universal signal floor: no universal answer, universal disagreement ceiling.
- Scale reduces within-model precision contamination by ~4× (7B: 20% flip, 32B: 4.5%).

## Correctness vs consensus — NULL LIFT (2026-06-24)

5-model TriviaQA paired analysis. Full detail: [correctness-consensus-2026-06-24](correctness-consensus-2026-06-24.md).

- **Consensus lift: +0.002.** Null. Llama-70B at 96.5% dominates — no headroom.
- **Label mapping fix:** `label=0→YES, label=1→NO` (verify against `meta.kind`, not intuition).
- **Pre-flight rules:** ANLI = skip (adversarial). TriviaQA = skip (single-model dominance). Custom benchmark needed for meaningful consensus-vs-correctness analysis.

## Dead runs — FALCON-180B, COMMAND A (2026-06-23)

Full detail: [dead-runs-2026-06-23](dead-runs-2026-06-23.md).

- **Falcon-180B:** OOM on 2× A100 even with CPU offloading. Declared dead.
- **Command A (111B):** 0% YES/NO. Template incompatibility — outputs `\n`. Not worth fixing.

## Commit-Confluence sealed dispatcher — GEOMETRIC PASS / STRICT PRODUCT FALSIFIED (2026-06-11)

Registered fresh-seed run (seed 20260612, 10 models × {ANLI, TriviaQA}, n=200, clean + controls passed), from public tag `prereg-seal-20260612`. Full verdict: [confluence-seal-2026-06-11](confluence-seal-2026-06-11.md).

- **SECONDARY geometric-only — PASS 18/20** (bar ≥17): a confidence-free ACE+null_ratio+RPV dispatcher under honest nested-OOB is deployable on 18/20. Geometric-science claim holds.
- **PRIMARY full-panel — FAIL 18/20** (bar ≥19): strict product claim falsified (≥2/20 non-deployable → pre-reg NO-GO). Predicted 1 orphan (`gemma-3-4b/anli`); a 2nd appeared (`Llama-3.1-8B/anli`, the no-prior-ACE-seal model).
- **Confidence is not the backstop:** PRIMARY and SECONDARY fail the **identical 2 ANLI cells** — coverage is 18/20 with or without confidence; the holes are genuine epistemic orphans no panel cell covers (TriviaQA 10/10, ANLI 8/10).
- **No universal cell:** geometric win-map dispersed across **12 distinct winners / 18 deployable** (ACE dominant; RPV covers 4 where attention doesn't; the pre-registered Fusion cell wins 2). Per-(model, distribution) thesis demonstrated, not asserted.

## KV-tension attention follow-up — OPEN, IMPLEMENTED CONTRACTS (2026-06-09)

New `W_u`-free ACE follow-up in `t0-morphology-furnace`: opt-in `--attention-kv-tension` cells decompose query-head disagreement into **within-KV-group tension** versus **between-KV-group tension** (`js_within_kv_groups`, `js_within_kv_groups_no_bos`, `js_kv_tension_gap`, `js_kv_tension_ratio`). Sealed ACE defaults are unchanged. Stage-0 audit over t0 sealed profiles: collapsed `js_kv_groups` beats raw `js` by ≥+0.03 in **13/54** layer cells (≥+0.05 in **8/54**), but mean delta is **−0.013** → warm/scoped, not universal. Fast contracts pass: `57 passed, 2 deselected`. T0 draft: `t0-morphology-furnace/exploratory/attention-kv-tension/PRE_REGISTRATION_DRAFT.md`.

## V-norm attention follow-up — LAST-QUERY V-NORM NO-PROMOTE (2026-06-09)

Setup question: do ACE's value-vector norm cells add beyond routing-only attention cells? A zero-code audit over the 18 sealed ACE profiles (`ANLI` + `TriviaQA`, 9 models each) answers negatively for the existing last-query V-norm family.

- **Mean delta:** best V-norm AUROC minus best non-V AUROC = **-0.0436** across 18 profiles.
- **Promotion pockets:** **0/18** profiles have delta >= +0.02; **0/18** have delta >= +0.03.
- **Selected V-norm winners:** only **3/18**, all tiny advantages: Phi-4 ANLI +0.0081, Qwen2.5 ANLI +0.0107, Qwen2.5 TriviaQA +0.0176.
- **Verdict:** do **not** spend fresh compute on a standalone `v_norm_lastq_weighted` run. The surviving V-payload trajectory is different: pre-register column-sum V-weighting (`sink_top1_vw`, `sink_topk_sum_vw`) as a separate SinkProbe-style feature family if we want to keep pulling this handle.

Plan page: [[v-norm-attention-prereg-2026-06-09]].

## 🌑 candidate #10 = RPV (Readout Pseudo-Volume) — H1 NO-GO: BEATS CONFIDENCE BUT REDUNDANT WITH v3 (2026-06-07)

`W_u`-*using* readout-morphology complement to ACE: eff-rank / spectral-entropy / off-top log-pseudo-volume of the softmax-Fisher `I(h)=W_uᵀ(diag(p)−ppᵀ)W_u`, **independent of `Δh`**. Paper-facing name **RPV (Readout Pseudo-Volume)** locked 2026-06-07; *shadow-ambiguity* / *#10* stay the internal slug. Lives in `t0-morphology-furnace/exploratory/shadow-ambiguity/`.

- **Temperature pre-check (label-free):** PASSED panel-wide (4 models, all |ρ(surprise,stat)| < 0.9 at T=1 → not a pure-confidence proxy).
- **Comprehensive run (2026-06-07, 26 pairs = 13 models × 2 benchmarks, gauntlet-hardened):** the decisive test, superseding the earlier 4-model labeled pilot.
  - ✅ **[VALIDATED] Beats plain confidence:** base-A random-effects meta **+0.102 [+0.065, +0.140]**, p≈5e-8, 3 families, brittleness-clean. Confidence-*independent* (a brighter lamp can't fake the blur-shape).
  - ❌ **[RESOLVED — H1 NO-GO] Redundant with sealed v3 `null_ratio`:** base-B meta **+0.011 < +0.02 bar**. Once you have v3's off-top projection, RPV's spectrum shape adds nothing on average — both read the same commit-Fisher geometry.
  - 🟡 **[OPEN] Complements v3 only in its collapse regime:** H2 slope **+0.080** (RPV adds where `null_ratio` is weak — Qwen3-8B standout, +0.13–0.16). Late-layer phenomenon (~L24–28) with a brittleness gate (discard where `corr(p_max,stat) ≥ 0.9`).
- **Net:** confidence-independent but v3-overlapping → **not a universal detector.** Written up as an 8pp honest-negative workshop paper (`wiki/paper/rpv-draft.tex`) and slated as the Fig-4 / §6.4 benchmark in the ACE fold-in. Provenance wins: the gauntlet caught a degraded-base inflation (pilot "+0.13" → fair base CI crosses 0), a degenerate base-B meta, an FWER bootstrap-resolution artifact, a smoke-file false alarm. Math: [[Candidate-10-Shadow-Ambiguity-Deconstruction]]; full thread: [log](../log.md) 2026-06-07.

## 🧯 candidate #9 RESIDUAL-FRICTION — CORRECTED TO NO-PROMOTE (2026-06-06)

Attention-write `a` vs MLP-write `m` friction within a block (`W_u`-free). A historical 9-model random-û screen looked late-layer-positive on Qwen+Llama, but the schema-v3 **same-`Δh` benign / residual-budget baseline** (`run-07`) deflates it: full-window nets collapse to **Qwen2.5 +0.0076, Qwen3-8B −0.0280, Llama3.2 −0.0019, Llama3.1 −0.0021**. Friction adds essentially nothing after same-Δ benign → the pilot mostly measured **benign cancellation / residual norm budgeting**, not a directed Knowledge Veto. v6/v7/v8 exploratory branches (projection-veto / attention-route / ACE-route-override) all concur: late MLP/readout + ACE-route are real, but the veto component collapses under same-Δ / projection-budget / shuffled controls. **Do not promote to sealed nested-OOB.** Full write-up: [residual-friction-pilot-2026-06-06](residual-friction-pilot-2026-06-06.md).

---

## ✅ v4 SEALED RUN VERDICT — E_A1 PASSES 7/9, E_A2 PARTIAL TRANSFER 3/9 (2026-05-26)

Pre-registered at `PRI_V4_PRE_REGISTRATION_PLAN.md` (frozen 2026-05-26). Instrument: t=0 prefill-last-position attention (`--t0-commit`), 21-cell panel, n=1000 bootstrap. Full results: [[results/v4-sealed-2026-05-26]].

**E_A1 (ANLI R1 n=200): 7/9 models with OOB CI_lo > 0.50 → ✅ PASS (threshold ≥7/9).** Mistral-7B (0.652), Mistral-Nemo (0.816), Phi-3.5-mini (0.601), Phi-4-mini (0.554), Qwen2.5-7B (0.663), Qwen3-1.7B (0.502), Qwen3-8B (0.738). Failing: Llama-3.2-3B (0.403) and Gemma-3-4B (0.488).

**E_A2 (cell transfer): 3/9 exact matches → ⚠️ PARTIAL TRANSFER (pre-reg ≥3/9 reframe clause).** Transfers: Mistral-7B (`last_minus_1_js_no_bos` −1), Mistral-Nemo (`last_minus_1_bos_mass` −1), Qwen2.5-7B (`final_v_norm_lastq_weighted`). Block-depth stable in 6/9. Paper reframes from "no universal cell" to "partial transfer; per-task recalibration required for 6/9 models."

**TriviaQA descriptive (8/9):** uniformly stronger signal — Mistral-7B AUROC 0.995, Mistral-Nemo 0.987. Not the primary gate.

Neither confirmatory blocker triggered (E_A1 ≥7/9, E_A2 < 5/9). Project-level claims stand.

---

Legacy numbers in "Original discrepancy table" and "Full Per-Variant Table" below: synthetic 2×2 contradiction benchmark (200 samples/cell, n=800/model), step 1, final layer, α = 1.0, MLX 4-bit quantized models. v3 results below from the n=50/cell (200/model) confirmatory run at the same analysis plane.

## ✅ v3 MAIN-RUN VERDICT (amended) — sealed E18 PASSES at rank 1 (2026-04-23)

n=50/cell (200/model) confirmatory run on 3 primaries (Llama 3.2 3B, Mistral 7B, Qwen 2.5 7B on 2026-04-22) + Qwen3-8B extended (2026-04-23). Full verdict + rank/layer landscape: [results/v3-main-run](v3-main-run.md).

**Sealed E18 gate at rank 1, final layer, step 1, pre-registered direction, d_F = lowrank32 residualization, 1000 sample-level bootstraps:**

| Primary | AUROC | 95% CI | Gate |
|---|---:|:---|:---|
| Llama 3.2 3B | **0.8593** | [0.806, 0.908] | PASS |
| Mistral 7B | **0.8638** | [0.814, 0.910] | PASS |
| Qwen 2.5 7B | **0.7274** | [0.656, 0.795] | PASS |
| Qwen3 8B (extended) | 0.3786 | [0.301, 0.466] | FAIL — inverted |

**3 of 3 primaries clear the 0.60 bar** with CIs well above 0.5. Robust across d_F choices (d_F = topk32 gives Llama 0.862 / Mistral 0.864 / Qwen 2.5 0.722). v3 passes sealed E18 under the reading that rank wasn't pinned in the sealed block; fails if one retroactively commits rank 32 as the implicit default. Both readings preserved — see verdict page §Methodological note.

**Rank 32 at final layer was a locally dead operating point.** Raw `null_ratio_rank32` ≈ 0.92–0.97 sits within ~0.005 of the random baseline `√((d-32)/d) ≈ 0.995`, so 3σ-level condition differences compress to null_ratio deltas of 0.002. Rank 1 widens the band and the signal is obvious. Earlier same-day reading of "E18 FALSIFIED" was at rank 32 and is superseded.

**Qwen 2.5 rank-32 sign-inversion** is a localized geometric artifact, not a v3 falsification. At rank 1 Qwen 2.5 aligns with Llama / Mistral in the correct direction (E18 0.73). The r=32 inversion still informs Qwen 2.5's rank-frequency structure (commit content concentrates in the top ~8 singular vectors) but is diagnostic, not a falsification.

**E19 `null_gated` interpretation gate — FAILS (unchanged).** Gate names `pri_v2_lowrank32` by reference, so rank 32 is the sealed operating point for E19 specifically. AUROC(null_gated) does not exceed max(AUROC(null_bare), AUROC(v2_lowrank32)) by non-overlap CI on any of 4 tested models.

**Collateral, not a v3 verdict:** Qwen3 8B shows weak signal across the 39-cell (layer × rank) landscape at step 1 (5/39 cells above 0.60 on E18); v2_lowrank32 AUROC ≈ 0.50 while surprise alone = 0.956. The Qwen 2.5 → Qwen3 v2 transfer fails. Separate Qwen-family diagnostic.

## ✅ RESOLVED — paper vs parquet (root cause: step-0 h_prev bug)

User confirmed 2026-04-14: the first generated token had no real previous token, so Δh at step 0 was inflated. Paper's 0.998/0.994/0.980 AUROCs are pre-audit artifacts of this bug. **Parquet is authoritative.** Paper's inverse-capability-scaling ordering (Llama > Mistral > Qwen) is also invalid — parquet reverses it (Qwen > Llama > Mistral).

## Original discrepancy table (retained for history)

| Model | Paper "Rupture at Commitment" (2026-03-17) | `summary.parquet` (post-audit?) |
|-------|-------------------------:|-----------------:|
| Llama 3.2 3B | AUROC **0.998**, g **4.18** | AUROC 0.623 (v1_cosine), 0.767 (v2 best) |
| Mistral 7B | AUROC 0.994, g 3.66 | AUROC 0.552 (v1_cosine), 0.671 (v2 best) |
| Qwen 2.5 7B | AUROC 0.980, g 2.29 | AUROC 0.083 (v1_cosine — INVERTED), 0.786 (v2 best) |

The audit checklist (`PRI_V2_PRE_RUN_AUDIT_CHECKLIST.md`) explicitly flags **CRITICAL token/hidden-state alignment bugs** that "silently produce plausible but wrong results." Working hypothesis: paper reports pre-audit numbers, parquet is post-audit. **Resolution required before paper can be cited externally.** Tracked as OPEN in `claims.md`.

## Full Per-Variant Table (from `summary.parquet`)
Sorted by AUROC within model. `pri_v2_diag` highlighted — it *inverts* on Llama and Mistral (AUROC < 0.5) but works on Qwen.

### Llama 3.2 3B
| Variant | AUROC | Hedges g | 95% CI | p |
|---------|------:|---------:|:-------|--:|
| `pri_v2_topk32` | 0.7666 | 0.955 | [0.809, 1.101] | 1e-4 |
| `pri_v2_full` | 0.7654 | 0.954 | [0.808, 1.100] | 1e-4 |
| `pri_v2_lowrank32` | 0.7644 | 0.931 | [0.785, 1.077] | 1e-4 |
| `pri_v2_topk256` | 0.7643 | 0.933 | [0.787, 1.079] | 1e-4 |
| `pri_v2_topk64` | 0.7642 | 0.930 | [0.784, 1.076] | 1e-4 |
| `pri_v2_topk128` | 0.7637 | 0.930 | [0.785, 1.076] | 1e-4 |
| `pri_v2_lowrank16` | 0.7635 | 0.913 | [0.767, 1.058] | 1e-4 |
| `pri_v2_lowrank8` | 0.7579 | 0.883 | [0.738, 1.028] | 1e-4 |
| `pri_v1_cosine` | 0.6229 | 0.450 | [0.310, 0.590] | 1e-4 |
| `pri_v1_l2` | 0.6187 | 0.448 | [0.308, 0.588] | 1e-4 |
| **`pri_v2_diag`** | **0.1355** | **−0.862** | [−1.007, −0.717] | 1.000 (INVERTED) |

### Mistral 7B v0.3
| Variant | AUROC | Hedges g | 95% CI | p |
|---------|------:|---------:|:-------|--:|
| `pri_v2_topk32` | 0.6715 | 0.582 | [0.441, 0.724] | 1e-4 |
| `pri_v2_topk64` | 0.6713 | 0.582 | [0.440, 0.723] | 1e-4 |
| `pri_v2_topk128` | 0.6713 | 0.581 | [0.440, 0.723] | 1e-4 |
| `pri_v2_topk256` | 0.6712 | 0.581 | [0.440, 0.722] | 1e-4 |
| `pri_v2_full` | 0.6710 | 0.581 | [0.439, 0.722] | 1e-4 |
| `pri_v2_lowrank32` | 0.6709 | 0.580 | [0.439, 0.721] | 1e-4 |
| `pri_v2_lowrank16` | 0.6708 | 0.579 | [0.438, 0.721] | 1e-4 |
| `pri_v2_lowrank8` | 0.6707 | 0.579 | [0.438, 0.720] | 1e-4 |
| `pri_v1_l2` | 0.5633 | 0.099 | [−0.039, 0.238] | 0.002 |
| `pri_v1_cosine` | 0.5516 | 0.055 | [−0.083, 0.194] | 0.045 |
| **`pri_v2_diag`** | **0.2492** | **−1.043** | [−1.191, −0.895] | 1.000 (INVERTED) |

### Qwen 2.5 7B
| Variant | AUROC | Hedges g | 95% CI | p |
|---------|------:|---------:|:-------|--:|
| `pri_v2_lowrank8` | 0.7859 | 1.379 | [1.225, 1.533] | 1e-4 |
| `pri_v2_lowrank32` | 0.7858 | 1.378 | [1.224, 1.532] | 1e-4 |
| `pri_v2_lowrank16` | 0.7858 | 1.377 | [1.223, 1.531] | 1e-4 |
| `pri_v2_full` | 0.7852 | 1.357 | [1.203, 1.510] | 1e-4 |
| `pri_v2_topk256` | 0.7820 | 1.354 | [1.200, 1.507] | 1e-4 |
| `pri_v2_topk128` | 0.7819 | 1.355 | [1.201, 1.508] | 1e-4 |
| `pri_v2_topk32` | 0.7818 | 1.358 | [1.204, 1.512] | 1e-4 |
| `pri_v2_topk64` | 0.7817 | 1.354 | [1.201, 1.508] | 1e-4 |
| `pri_v2_diag` | 0.7445 | 0.741 | [0.598, 0.884] | 1e-4 |
| **`pri_v1_l2`** | **0.0912** | **−1.906** | [−2.073, −1.739] | 1.000 (INVERTED) |
| **`pri_v1_cosine`** | **0.0827** | **−1.988** | [−2.157, −1.818] | 1.000 (INVERTED) |

## Key takeaways (corrected)
1. **Qwen v1 inversion is real and severe.** Both `pri_v1_cosine` and `pri_v1_l2` are *worse than chance* on Qwen (AUROC 0.08, g ≈ −2). The v2 family resolves this — all v2 non-diag variants give AUROC > 0.78 on Qwen.
2. **`pri_v2_diag` is a different trap**: it inverts on Llama (AUROC 0.14) and Mistral (0.25) but works on Qwen (0.74). **Diagonal FIM approximation is unsafe.** Opposite architectural pattern to v1 inversion.
3. **Within non-diag v2, variants cluster within 0.005 AUROC.** The earlier "best variant differs per model" framing (topk32 vs lowrank32) is technically true but **within-CI noise**. Treat non-diag v2 variants as effectively equivalent.
4. **Effect-size ordering (per parquet): Qwen (g≈1.38) > Llama (0.96) > Mistral (0.58).** This **contradicts** the paper's reported inverse-capability-scaling claim (Llama 4.18 > Mistral 3.66 > Qwen 2.29). Another symptom of the paper-vs-parquet discrepancy.

## Notable Anomalies
- **Autoresearch loop retired 2026-04-14** per user decision — no longer tracked as an issue.
- **Paper / parquet discrepancy**: unresolved; flagged as OPEN.

## Pending
- Alpha-sweep (fig 5) and step-trajectory (fig 2) per-variant — extract from `all_results.parquet`.
- Outcome-independence three-bar comparison (fig 4) — pull from `failure_cases.parquet`.
- Extended baseline suite: Gemma 3-1B, Qwen3-8B-MLX-4bit, Phi-3.5-mini 3.8B (gpt-oss-20b dropped per 2026-04-14 decision; M4 too light).
- **SUP spectral-band validation** (pre-v3 gate) — scaffold at [results/sup-spectral-band](sup-spectral-band.md), script at `PRI_at_commitment/scripts/sup_spectral_band.py`, awaiting execution.
