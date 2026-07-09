# 🧰 Terminology

A topic-grouped glossary for Furnace work. Terms appear once under their primary topic. Look up via `/term <name>`. Add via `/term <name>: <definition>`. Definitions are short (1–2 sentences); rigorous source lives in linked companion pages.

**Companions:** [overview](../overview.md) · [pri-v3-plan](../pri-v3/pri-v3-plan.md) · [claims](../claims.md) · [results/summary](../results/summary.md)

---

## 📊 Statistics & evaluation

- **AUROC** (Area Under ROC Curve) — Probability that a randomly drawn contradiction sample gets a higher score than a randomly drawn control. 0.5 = chance, 1.0 = perfect, 0.0 = perfect-but-flipped.
- **bootstrap** — Resample the data with replacement N times, recompute the statistic each time, take percentiles. Furnace uses 1000 sample-level resamples for E18 CIs.
- **CI** (confidence interval) — Range that captures the true value at a stated confidence (default 95%). For AUROC: bootstrap 95% CI = [2.5th, 97.5th] percentiles of the bootstrap distribution.
- **falsification** — A pre-registered test result that, if reached, retires the hypothesis. Sealed in plan §Falsification conditions; cannot be re-specified after data lands.
- **gate** (sealed gate) — A pre-registered numerical threshold + interval condition (e.g. `AUROC ≥ 0.60` with non-overlap CI vs 0.5). Pass/fail is binary; partial reads are not pass.
- **Hanley-McNeil SE** — Closed-form approximation for AUROC standard error given (n_positive, n_negative, true AUROC). Used 2026-04-22 to set n=50/cell from the n=20/cell power deficit.
- **Hedges g** — Bias-corrected effect size (mean diff / pooled SD). Reported alongside AUROC in v2 baseline tables.
- **LOO** (leave-one-out) — Cross-validation scheme where each unit (here: each model) is held out as the test instance while the remaining N−1 form the training set. Used as the evaluation harness for the meta-classifier in `scripts/diagnostics/meta_classifier_loo.py`.
- **non-overlap CI** — Two CIs that do not share any value; the standard "different by more than chance" check at 95%. Used in E17b, E18, E19 sealed gates.
- **OOB** (out-of-bag) — In bootstrap resampling, the samples NOT drawn into a given resample. OOB AUROC scores a model fit on in-bag samples against the OOB samples, giving an honest deployment estimate that corrects post-selection bias. Used in `pri_calibrator.py` after the 2026-05-13 Codex review.
- **post-hoc re-spec** — Changing the test (rank, threshold, regression family, pooling) after seeing the data. Plan §Magnitude-independence test forbids it explicitly.
- **residualization** — `y_resid = y − predict(y | x)` via linear regression. E18 residualizes `null_ratio` against `d_F` to isolate direction signal independent of magnitude.
- **sample-level bootstrap** — Resampling at the sample (puzzle) granularity, not the token granularity. E18 spec pins this — token-level inflates effective n.
- **two-sided AUROC** — `max(AUROC, 1 − AUROC)` — discards directional pre-registration. Useful as a magnitude-of-separation diagnostic; not a substitute for the pre-registered direction in a sealed test.

## 🎚️ Geometry & metrics

- **Δh** (delta h) — Change in hidden state between consecutive token positions: `Δh_ℓ = h_ℓ_t − h_ℓ_(t−1)` at layer ℓ. The "thinking jump" v1/v2/v3 all measure.
- **d_F** (Fisher pullback distance) — `sqrt(Var_p(W_u · Δh))`, the spread of `W_u·Δh` under the token distribution. v2's magnitude scalar; computed as `diag` / `full` / `topk-k` / `lowrank-r` approximations.
- **Fisher pullback** — Pulling the Fisher information of the output distribution back through `W_u` onto hidden-state space. Gives a curved (context-dependent) metric instead of Euclidean.
- **Fisher-energy ratio** (`ε(r)`) — `Σ_{i≤r} σ_i² / Σ_i σ_i²`. Cumulative variance captured by top-r Fisher singular values. Reported alongside every `null_ratio_r` so rank choice is signal-vs-energy, not arbitrary.
- **informed subspace** — Span of `V_top` (top-r right singular vectors of `sqrt(p_t)·W_u`). The directions `Δh` "should" go in if the model is committing purposefully.
- **null complement / null ratio** — Component of `Δh` orthogonal to the informed subspace. `null_ratio = ‖Δh − V_top V_topᵀ Δh‖ / ‖Δh‖`. Bounded [0, 1]; random baseline is `√((d−r)/d)`.
- **PRI v1** — `S_t · (1 + α · δ_h)` where `δ_h` is cosine distance. Multiplicative rupture score.
- **PRI v2** — `S_t + α · d_F`. Additive Fisher-pullback rupture score. Validated baseline.
- **PRI v3** — `S_t + α · null_ratio` (additive null-direction variant); `pri_v3_null_gated = d_F · null_ratio` (multiplicative). Tested in main run 2026-04-23.
- **random baseline** (for null_ratio) — Expected `null_ratio` for a uniformly random Δh: `√((d−r)/d)`. ≈ 0.995 for typical (d≈3000, r=32). Mandatory subtraction on every v3 plot.
- **S_t** (surprise) — `−log p_t(y_t)` at the committed token. Magnitude of "the model didn't expect this."
- **V_top** — Top-r right singular vectors of `sqrt(p_t) · W_u`. The basis defining the informed subspace at rank r.
- **W_u** (unembedding / output projection) — Final linear layer mapping hidden state to logits. Same matrix at every layer in the logit-lens projection.

## 🏗️ Pipeline / code

- **Δh source-log** — Provenance dict tracking which `h_prev` was used per row (gen step vs prefix step vs cached). Tripwire B6 mutates it to verify the guard fires.
- **gen_step** — Index of generated token within a sample. Step 0 = first generated (uses prefix `h_prev`); step 1 = first commitment with real prior. Sealed v3 analysis plane is step 1.
- **layer (final / mid / quarter)** — Coarse depth indices captured by default. `final` = last block output, `mid` = roughly half, `quarter` = roughly 1/4 (per-model integer maps in `model_adapters.py`).
- **Option A** — v3 v0 default: single `V_top` from final-layer `p_t`, reused at every layer. Cheap; reuses v2's existing SVD.
- **Option B** — Per-layer `V_top` from each layer's logit-lens distribution. Disfavored for v3 v0 — sharpness-collapse confound dominates.
- **p_t** — Token distribution at commitment (softmax of logits at committed token position).
- **sample_id** — Unique per-puzzle identifier. 200 samples/model in the n=50/cell main run (4 cells × 50).
- **trace_dumps.parquet** — Companion parquet capturing raw hidden states `h_t`, `h_prev`, and `p_t` per sample. Needed for E17b post-hoc raw-W_u SVD.

## 🧬 Models in scope

- **Llama 3.2 3B** — `mlx-community/Llama-3.2-3B-Instruct-4bit`. Primary; d=3072, 28 layers, fp16.
- **Mistral 7B** — `mlx-community/Mistral-7B-Instruct-v0.3-4bit`. Primary; d=4096, fp16.
- **Qwen 2.5 7B** — `mlx-community/Qwen2.5-7B-Instruct-4bit`. Primary; d=3584, lm_head padded 152064 vs vocab 151643.
- **Qwen3 8B** — `mlx-community/Qwen3-8B-4bit`. Extended (not primary); d=4096, bfloat16.
- **Gemma 3-1B** — `mlx-community/gemma-3-1b-it-4bit`. Extended; d=1152, 26 layers, sliding-window pattern.
- **Gemma 3-4B** — `mlx-community/gemma-3-4b-it-4bit`. Extended; d=2560, 34 layers, multimodal wrapper, bfloat16.
- **Phi-3.5-mini** — `mlx-community/Phi-3.5-mini-instruct-4bit`. Extended; d=3072, fp16.

## 🔬 Experiments

- **E17** (`pri_v3_null_bare`) — null_ratio alone separates contradiction from control. Min bar: AUROC > 0.6 on at least one model.
- **E17b** (`pri_v3_null_raw`) — null_ratio computed from SVD of raw `W_u` (HARP baseline). Tests whether Fisher weighting carries signal beyond static W_u.
- **E18** (`pri_v3_null_ratio`) — `S_t + α · null_ratio` separates independent of `d_F` magnitude. Sealed gate: AUROC(null_ratio_resid) ≥ 0.60 with non-overlap CI vs 0.5 on ≥2 of 3 primaries.
- **E19** (`pri_v3_null_gated`) — `d_F · null_ratio` beats both null_bare and v2_lowrank32 by non-overlap CI. Interpretation gate.
- **E20** (`pri_v3_spectrum`) — Demoted 2026-04-14 to exploratory; spectral decay dominated by p-sharpness.
- **E21** (depth profile) — `null_ratio_ℓ` vs layer per condition. Looks for drop-point where Δh first enters informed subspace.
- **E22** (direction-depth signature) — Cross-arch reproducibility of `null_ratio_ℓ` shape. PARTIAL VALIDATED post-Prereq-8 norm fix.
- **E23** (Option C sharpness-aware variants) — Verdict OPTION-A-REAFFIRMED. No C variant beat A.
- **HARP** — Hu et al. 2025, arXiv 2509.11536v2. Static raw-`W_u` SVD + trained classifier; AUROC 0.928/0.929 on Qwen/Llama TriviaQA. Closest prior.

## 🔒 Methodology

- **chain_length × contradiction** — The 2×2 factorial: (2-step | 5-step) × (control | contradiction). 50 samples/cell × 4 cells = 200/model in the v3 main run.
- **Prereq 4** — Sealed v3-capture-dryrun spec (8 assertion bundles) at `pri-v3-plan.md:266`. Closed 2026-04-22 across all 7 models.
- **Prereq 8** — Qwen primary gate via post-final-norm Option A. Closed 2026-04-18; Qwen `null_ratio_A_rank32` shows clean late-rise.
- **sealed block** — Frozen-before-data pre-registration (plan lines 73–82). Cannot be re-specified post-hoc; rank deliberately *not* pinned in the 2026-04-23 reading.
