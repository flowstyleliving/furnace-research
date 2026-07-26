# Overview

> **Knowledge-base methodology:** this vault follows the LLM-maintained-wiki pattern described by Karpathy (2026). See [meta/llm-wiki-methodology](meta/llm-wiki-methodology.md) and the raw source at `raw/papers/external/karpathy-2026-llm-wiki.md`.

## Furnace
Furnace is an AI-safety infrastructure research project. Current focus: detecting internal *rupture* at the moment a language model commits to an answer, as a route to flagging latent misalignment / reasoning failure before output.

## PRI — Predictive Rupture Index
PRI scores each generated token by combining token surprise with a representation-space "rupture" signal between consecutive hidden states. The working paper is **"Prediction Rupture at Commitment"**; see `/Users/msrk/Documents/PRI_at_commitment/` for the reference implementation.

### PRI v1 (cosine)
```
PRI_v1 = S_t * (1 + α · δ_h)
```
- `S_t = -log p(token_t)` — token surprise
- `δ_h = 1 - cos(h_t, h_{t-1})` — cosine distance between consecutive layer hidden states
- Multiplicative coupling; v1 baseline for comparisons.

### PRI v2 (Fisher pullback)
```
PRI_v2 = S_t + α · d_F
```
- `d_F` — Fisher-information-pullback distance through the unembedding: project `Δh = h_t - h_{t-1}` with `W_u` to get `z`, then measure `z`'s spread under the next-token distribution `p_t`.
- **Additive** (not multiplicative), so surprise and rupture are independent contributors.
- Multiple FIM approximations are computed and compared, not a single canonical form:
  - `d_F_diag` — diagonal FIM: `sqrt(Σ p · z²)`
  - `d_F_full` — full/empirical variance: `sqrt(E[z²] − E[z]²)` under `p`
  - `d_F_topk{5,10,32}` — restrict to top-k probability mass and renormalize
  - `d_F_lowrank{10,32,50}` — SVD of `sqrt(p) · W_rows` truncated to rank r

### PRI v3 (sealed — PASSES 3/3)
v3 keeps the eigenstructure of `F_t` that v2 collapses to a scalar, and asks *where* `Δh` lives in that spectrum. The SUP-native prediction: at rupture, `Δh` concentrates in the low-eigenvalue subspace — moves along directions where the model has lost discrimination power. Falsifiable statistic: `null_ratio_post_rank{r} = ||proj_null(Δh)|| / ||Δh||`. **Sealed E18 PASSES 3/3 primaries at rank 1** (Llama 0.859, Mistral 0.864, Qwen 2.5 0.727; 2026-04-23), replicated under fresh seed (v3.1). See [pri-v3-plan](pri-v3/pri-v3-plan.md), [results/v3-main-run](results/v3-main-run.md), and [claims](claims.md) §2.

### Beyond v3 — the production library + the two research lines (current)
After v3 sealed, the work split into two lines (see [references/code](references/code.md)):
- **PRI detection line** — the production library `pri_calibrator.py` + `pri_detector.py` (per-(model, exact deployment distribution) calibration with deployability warnings; schema v1.1 nested-OOB CIs) plus exploratory v5–v8 branches. Lives in `PRI_at_commitment`.
- **Morphology line** — **ACE** (Attention Commitment Estimator, `W_u`-free t=0 attention morphology; sealed 2026-05-26, E_A1 7/9 PASS / E_A2 3/9 partial transfer — the v4 paper spine) plus new `W_u`-using readout-morphology candidates (e.g. #10 shadow-ambiguity). Lives in `t0-morphology-furnace`.

For "what is true now," always read the tail of [log](log.md) and [research-candidates](research-candidates.md) before this overview (per the Vault-canon rule in `CLAUDE.md`).

## Key Theoretical Advance
Using the Fisher pullback geometry makes the rupture metric curvature-aware in the model's output distribution rather than flat-Euclidean in representation space. This should (a) outperform v1 cosine in AUROC, and (b) correct v1 failure modes tied to representation basis.

## Current Pipeline
- Framework: **MLX** on **Apple Silicon** (greedy, temperature 0)
- Sealed v3 primary suite (4-bit quantized MLX builds):
  - `mlx-community/Llama-3.2-3B-Instruct-4bit`
  - `mlx-community/Mistral-7B-Instruct-v0.3-4bit`
  - `mlx-community/Qwen2.5-7B-Instruct-4bit`
  - `mlx-community/Qwen3-8B-4bit` (cross-generation extended, not a v3 primary)
  - The ANLI / ACE panel grows to ~9–11 models (adds Mistral-Nemo, Phi-3.5-mini, Phi-4-mini, Qwen3-1.7B, Gemma-3-4B, …). **`gemma-3-1b` and `gpt-oss-20b` are EXCLUDED** (model-capability gate failure / too heavy).
- Benchmark: synthetic contradiction puzzles in a **2×2 factorial**: `chain_length ∈ {1,2} × contradiction ∈ {False,True}`. Contradiction puzzles inject a conflicting premise at position 1 assigning a different value to the same species.
- Layers probed: `final`, `mid`, `quarter` (1/4 depth).
- Alpha: default 1.0, with sweeps logged for figure 5.
- Sample counts (v3 main-run convention): **exploratory n=4 per cell**, **confirmatory n=50 per cell** (bumped from n=20 on 2026-04-22 — see `pri-v3-plan.md` Amendments) before any result is filed as a `[FINDING]`.
- Metrics: AUROC, Hedges g, stratified-permutation p, bootstrap AUC-diff for v2 vs v1.
- Behavioral preflight gate: ≥ 80 % control accuracy on 20 control samples before full run.

## Repos
- **PRI_at_commitment** — PRI-detection working trunk (v1/v2/v3 pipeline + figures + production calibrator/detector + v5–v8 exploratory branches), `/Users/msrk/Documents/PRI_at_commitment/`
- **t0-morphology-furnace** — the morphology line: sealed ACE/T0 core + a living `exploratory/` area for new morphology candidates (e.g. #10 shadow-ambiguity), `/Users/msrk/Documents/t0-morphology-furnace/` (GitHub `flowstyleliving/t0-morphology-furnace`)
- **PRI_at_commitment_autoresearch** — autonomous daily loop, **RETIRED 2026-04-14** (do not restart; queue conventions preserved as aspirational protocol)

See [references/code](references/code.md) for details.
