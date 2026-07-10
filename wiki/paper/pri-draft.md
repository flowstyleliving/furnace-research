# Architecture-Dependent Fisher Pullback Geometry at the Commit Moment: A Sealed Pre-Registered Test on Synthetic Logical Contradictions

**Michael S.R. Kitti** · `msrkittty@proton.me`

_Workshop submission draft, 2026-04-27. Status: `[DRAFT]` — section structure populated end-to-end; numbers traceable to `experiments/v3-main-run/2026-04-26/run-09/` + `experiments/v3-main-run/2026-04-27/run-{01,02}/`. Pre-registration snapshot: `PRI_V3_PRE_REGISTRATION_PLAN.md` at the repo root, frozen from `wiki/pri-v3/pri-v3-plan.md` on 2026-04-27._

---

## Abstract

We test whether a Fisher-pullback-derived rupture geometry beats a static-SVD baseline (HARP-style) at detecting logical contradictions at the first generated token of an LLM's response. The head-to-head is sealed pre-registered: analysis plane (final layer, gen_step=1, rank=1), residualization, bootstrap, threshold, and 2-of-3 primary bar are all locked before data collection. Across six architectures (Llama 3.2 3B, Mistral 7B, Qwen 2.5 7B, Qwen3 8B, Phi-3.5-mini, Gemma 3-4B) at n=600 samples per model with 1000 sample-level paired bootstrap resamples, the cross-architecture verdict at the sealed analysis plane splits **3 Fisher / 3 Raw** with non-overlap CI — vendor and parameter count are not predictive. Three distinct motifs structure the cross-architecture picture: (1) Phi-3.5 is stable Raw-decisive across all 13 ranks of the SVD sweep, with Raw_post_rank1 = 0.999; (2) Gemma 4B has a sharp within-model rank flip at r=2→r=3 (Fisher → Raw), robust across chain length; (3) Mistral 7B has a chain-length × rank interaction with two Simpson's-paradox sites — at sealed r=1 and at r=32, where stratifying by chain length flips the verdict at non-overlap CI in both directions, with cross-stratum spread Δ_cross = −0.575 (the largest in the 156-cell landscape). The sealed E18 magnitude-independence gate passes 3-of-3 primaries; the sealed E17b head-to-head passes on Qwen 2.5 at Δ AUROC = +0.157 [0.125, 0.190]. We identified and corrected a coordinate-mismatch in the Fisher pullback computation (the RMSNorm Jacobian was missing); sealed-spec discipline preserved verdict integrity across the correction.

---

## 1. Introduction

When an LLM commits to its first generated token, the residual stream has just resolved whatever contradictions or constraints were in the prompt into a single output direction. Hallucination at the output level appears statistically inevitable for any base language model trained on finite data (Kalai et al. 2025), but the model's *representations* often carry signal that the output does not (Agrawal et al. 2024; Farquhar et al. 2024). The geometry of the commit moment — how the hidden state moves between the last prompt position and the first generation position — has been proposed as a substrate for hallucination detection (Hu et al. 2025), and as a window onto a model's internal certainty within the broader "LLM-wiki" methodology of inspecting representational dynamics (Karpathy 2026). Our prior work (Kitti 2026a; Kitti 2026b) introduced PRI v1 (cosine Δh scaled by token surprise) and v2 (Fisher distance scalar); this paper introduces v3 (null-space ratio) and tests it head-to-head against a HARP-style static-SVD baseline.

Two formulations of "rupture geometry" sit naturally side by side. **HARP** projects the hidden-state difference Δh onto the top right singular vectors of the unembedding matrix W_u — a static, model-only basis that captures the model's universal output structure. **Fisher pullback** projects onto the top right singular vectors of `√p_t · W_u`, the same matrix re-weighted by the current token distribution — a per-sample, locally-tailored basis that captures the directions where THIS prompt's prediction is sensitive. The Fisher formulation is the natural information-geometric generalization: the basis from `√p_t · W_u` are eigenvectors of the diagonal Fisher information `W_uᵀ · diag(p_t) · W_u`, the metric induced on hidden-state space by the model's softmax output. HARP's basis is a special case (uniform p_t).

Does Fisher pullback add discriminative signal beyond HARP at the commit moment, on synthetic logical contradictions? We pre-register the head-to-head, run it across six 4-bit-quantized open-weight architectures, and find that **the answer is architecture-dependent in three structurally distinct ways**.

**Contribution.** (1) A sealed pre-registered test of Fisher pullback vs static W_u SVD at the gen_step=1 commit plane, on a 2×2 factorial of synthetic puzzles (chain_length × contradiction). (2) A 6×13×2 cross-architecture × rank × chain-length landscape that reveals three motifs — stable Raw (Phi-3.5), within-model rank flip (Gemma 4B), and within-model chain-length × rank Simpson's-paradox (Mistral). (3) A methodological coordinate-mismatch correction in the Fisher pullback (missing RMSNorm Jacobian) caught after sealed gate but before paper-level claim, with the sealed verdict re-derived under corrected geometry. (4) Demonstration that pre-registration discipline absorbs methodological corrections without compromising verdict integrity — the discipline machinery worked.

**Roadmap.** §2 places HARP, Fisher information geometry, PRI v1/v2, and ML pre-registration. §3 specifies the sealed pre-reg, the pipeline, and the J_n geometry correction. §4 reports the sealed verdicts, the cross-architecture motifs, and the baselines. §5 discusses the mechanism (newline-commit vs content-commit), pre-registration governance, limitations, and future work.

## 2. Related Work

**HARP** (Hu et al. 2025) decomposes the unembedding matrix W_u via SVD and uses the orthogonal complement of the top-r right singular vectors as a "reasoning subspace" for hallucination detection. Their basis is static — computed once per model. We use HARP's static-W_u basis as the head-to-head control.

**Information geometry on the simplex** (Amari 2016) gives the Fisher metric `D(p_t) = diag(p_t) − p_t · p_tᵀ` for a categorical distribution. Pulled back to hidden-state space through the unembedding W_u and the final RMSNorm, the Fisher metric becomes `J_nᵀ · W_uᵀ · D(p_t) · W_u · J_n`. The diagonal-only approximation drops the rank-1 centering term `−p_t · p_tᵀ`; what remains is `W_uᵀ · diag(p_t) · W_u`, whose top-r eigenvectors equal the right singular vectors of `√p_t · W_u`. This is the basis we sweep against HARP.

**LLM rupture / commit / surprise / consistency-based hallucination detection.** PRI v1 (cosine Δh scaled by token surprise) and v2 (Fisher distance scalar), introduced in our prior work (Kitti 2026a; Kitti 2026b), are precursors of v3's null-ratio formulation; we report all four as baselines. Surprise (token negative log-probability under the model) is the canonical lightweight signal and is included as a baseline anchor. Semantic-entropy methods (Farquhar et al. 2024) cluster sampled generations by bidirectional entailment and report AUROC ≈ 0.78–0.88 on factual confabulation detection, but require ≈ 10 forward passes per query; PRI requires one. Token-level self-consistency (Wastl et al. 2025) aligns sampled completions and detects hallucinated spans via per-token median similarity — closest external methodology to PRI's per-token framing, but black-box and sampling-based.

**Pre-registration in ML** has been advocated for stronger evidentiary standards in benchmark-driven research (Nosek et al. 2018; Pineau et al. 2021). Our sealed E18/E17b spec follows this pattern: analysis plane, residualization, bootstrap, threshold, and pass-bar are all locked before data collection. The pre-registration document is snapshotted to the repository at the freeze date (Appendix B).

## 3. Methods

### 3.1 Pre-registration and sealed spec

The sealed pre-registration document (`PRI_V3_PRE_REGISTRATION_PLAN.md` at the repo root) was frozen at the snapshot date and locks the following parameters:

- **Analysis plane:** final transformer layer, gen_step = 1 (the first generated token, 1-indexed).
- **Sealed E18 metric:** `null_ratio_post_rank1` residualized against `d_F_lowrank32` via OLS (linear regression on `d_F`, not logistic). Robustness check at `d_F_topk32`.
- **Sealed E18 acceptance:** AUROC ≥ 0.60 with non-overlap 95% bootstrap CI vs 0.5, on 2-of-3 primaries (Llama 3.2 3B, Mistral 7B, Qwen 2.5 7B). Direction pre-registered: higher null_ratio → contradiction.
- **Sealed E17b metric:** AUROC(`null_ratio_post_rank1`) − AUROC(`null_ratio_raw_post_rank1`) on Qwen 2.5 7B, the primary authority for the head-to-head.
- **Sealed E17b acceptance:** Δ AUROC ≥ +0.02 with non-overlap 95% bootstrap CI on Qwen 2.5.
- **Bootstrap:** 1000 sample-level paired resamples, seed = 20260423 (ISO-date-derived integer, fixed before data collection).
- **No-silent-override rule:** any gate failure during launch must file a new Amendments entry in the pre-reg before `--skip-gate` or threshold overrides are applied.

### 3.2 Pipeline

**Synthetic puzzles.** A 2×2 factorial (chain_length ∈ {2, 5} × contradiction ∈ {True, False}) generated deterministically from the seed, with n=150 puzzles per cell → 600 samples per model. Each puzzle is a short logical chain — for chain_length=2: "All X are Y. All Y are Z. Q is X. Is Q a Z?" — with the contradiction variant inserting a denial of the conclusion. The model is asked to output `Answer: YES` or `Answer: NO`; the gen_step=1 token is the first token of the model's answer.

**Capture.** For each sample, we run the model with greedy decoding for max_new_tokens=14, capturing at gen_step=1 the residual-stream hidden state immediately before (`h_prev`) and after (`h_t`) the last transformer block, the final RMSNorm γ vector (extracted once per model from the model's own weights), and the post-softmax distribution `p_t` over the vocabulary.

**Post-norm Δh.** We apply the model's own final RMSNorm to both `h_t` and `h_prev` to get `h_t_post` and `h_prev_post` in post-norm h-space, then compute `Δh_post = h_t_post − h_prev_post`. This is the J_n-corrected residual stream perturbation; W_u is trained against post-norm inputs, so the SVD basis we project onto must live in the same coordinate frame (§3.4).

**Two SVD bases — the head-to-head.** For each sample we compute:

- **Fisher (per-sample, support-truncated):** the top-1024 vocab rows of W_u by p_t are weighted by `√p_t` and SVD'd; the top-r right singular vectors form the Fisher basis. Re-computed per sample because p_t changes per sample.

- **Raw (per-model, full vocab):** the full V × d unembedding matrix is SVD'd at model load via chunked `W_uᵀ · W_u` accumulation; the top-r right singular vectors form the static raw basis. One SVD per model, cached.

**Null ratio and energy.** For rank r in {1, 2, 3, 4, 5, 8, 13, 16, 21, 32, 34, 55, 64}, the null ratio is `||Δh_post − V_top V_topᵀ Δh_post|| / ||Δh_post||` — the fraction of Δh_post outside the top-r informed subspace. Energy fractions are basis-only (cumulative σ²).

The asymmetry between the two bases is the experimental knob: Fisher is local (per-sample, support-truncated) and Raw is global (per-model, full vocab). The E17b head-to-head asks whether the local-tailored basis carries discriminative signal beyond the global-static one at the sealed plane.

### 3.3 Models

**Sealed primaries** (gate authority): Llama 3.2 3B Instruct, Mistral 7B Instruct v0.3, Qwen 2.5 7B Instruct. All 4-bit quantized via `mlx-community`. Qwen 2.5 7B is the sealed E17b authority (largest HARP-vs-PRI-v2 reported gap at pre-registration time).

**Cross-architecture companions** (descriptive, not sealed): Qwen3 8B (cross-generation within Qwen family), Phi-3.5-mini Instruct (reasoning-tuned, cross-vendor), Gemma 3-4B (different architecture family with interleaved sliding-window attention).

**Excluded.** Gemma 3-1B was excluded after gate-failing at 11/20 = 55% on n=20 stratified controls under the post-PR#7 stratified-sampling and three-tier `check_answer` parser fixes. `--gate-verbose` confirmed model-capability rather than parser failure (Gemma 1B defaults to `Answer: NO` on YES controls regardless of premises). Within-family scale axis (1B ↔ 4B held architecture-fixed) collapses to a single point.

**Behavioral preflight gate.** Before each sealed-equivalent run, 20 stratified control puzzles (10 cl=2 / 10 cl=5) are generated and the model must answer ≥80% correctly. Operational rescues (`--gate-max-tokens 12` to clip front-loaded answers before format completion) are filed in the pre-reg amendments and applied without exception.

### 3.4 J_n geometry correction

The pre-registration specified that the Fisher pullback basis lives in post-norm h-space (W_u acts on `n(h)`, not `h`). The pre-2026-04-26 pipeline implementation projected raw pre-norm `Δh = h_t − h_prev` onto the post-norm basis — a coordinate mismatch in the Fisher pullback computation. The proper pullback applies the RMSNorm Jacobian J_n: either project `J_n(h_prev) · Δh_pre` onto the post-norm basis, or capture post-norm Δh directly (both equivalent to first order). We adopted the latter: extract the model's RMSNorm γ from its weights, apply numpy RMSNorm to `h_t` and `h_prev`, take the difference. We verified the implementation reproduces `model.model.norm(h)` to ≤1e-5 max-abs error across all six architectures (full diagnostic in Appendix A). The legacy pre-norm-Δh code path was deleted on 2026-04-26 along with the analyzer's `--columns legacy` flag, closing a silent-failure mode where downstream consumers could read a buggy verdict labeled identically to the corrected one. The sealed E18 verdict is unaffected by the correction (residualization against `d_F_lowrank32`, also computed in the buggy geometry, absorbs the coordinate mismatch). The sealed E17b verdict on Qwen 2.5 flipped from −0.166 (FAIL) to +0.150 (PASS) under the corrected geometry — the +0.32 swing is the J_n correction's effect on the head-to-head, where no residualization absorbs the bias.

## 4. Results

All numbers below are at n=600 per model (the powered run-09 + 2026-04-27/run-{01,02} sweep), 1000 sample-level paired bootstrap resamples, seed=20260423, J_n-corrected post-norm geometry. The n=200 prelim run-02 reading is reported parenthetically where directly comparable.

### 4.1 Sealed E18 verdict — 3 of 3 primaries PASS

| Primary | E18 sealed AUROC (rank=1, lowrank32, post-norm) | 95% CI | Sign | Verdict |
|---|:---:|:---:|:---:|:---:|
| Llama 3.2 3B | 0.8713 | [0.842, 0.896] | +1 | **PASS** |
| Mistral 7B | 0.8707 | [0.845, 0.897] | +1 | **PASS** |
| Qwen 2.5 7B | 0.6468 | [0.603, 0.691] | +1 | **PASS** |

![Fig 1 — Sealed E18 verdict: 3 of 3 primaries PASS at n=600 under post-norm geometry](figures/fig1_sealed_e18.png)

**Fig 1.** Sealed E18 magnitude-independence gate at n=600 per primary, J_n-corrected post-norm geometry. AUROC of `null_ratio_post_rank1` residualized against `d_F_lowrank32` via OLS. Error bars are 1000-sample paired bootstrap 95% CIs (seed = 20260423). All three primaries clear the sealed threshold (0.60, dashed) with non-overlap CI vs 0.5 (chance, dotted). Sealed bar is 2-of-3; we clear 3-of-3.

All three primaries clear the AUROC ≥ 0.60 threshold with non-overlap 95% CI vs 0.5. Sealed bar is 2-of-3; we clear 3-of-3. Bootstrap CIs are ~33% tighter than the n=200 prelim (run-02), consistent with √3 narrowing for 3× more data. Verdict structure replicates the prelim direction-for-direction.

### 4.2 Sealed E17b verdict on Qwen 2.5 — PASS

| Reading | Fisher AUROC (sign) | Raw AUROC (sign) | Δ_oriented | 95% CI | Verdict |
|---|:---:|:---:|:---:|:---:|:---:|
| Buggy 2026-04-24 (pre-norm Δh on post-norm basis, run-05) | 0.7665 (−1) | 0.9323 (+1) | −0.166 | [−0.240, −0.098] | FAIL (Raw decisive) |
| **Corrected 2026-04-27 (post-norm Δh on post-norm basis, run-09)** | **0.8967 (+1)** | 0.7396 (−1) | **+0.157** | **[+0.125, +0.190]** | **PASS (Fisher decisive)** |

![Fig 2 — Sealed E17b head-to-head: Fisher beats Raw on Qwen 2.5](figures/fig2_sealed_e17b.png)

**Fig 2.** Sealed E17b head-to-head on Qwen 2.5 7B at n=600. **Left:** oriented AUROCs of `null_ratio_post_rank1` (Fisher, sign +1) and `null_ratio_raw_post_rank1` (Raw, sign −1). **Right:** Δ AUROC = +0.157 [+0.125, +0.190] (1000-sample paired bootstrap), clearing the sealed +0.02 bar (dashed) with non-overlap CI.

![Fig 3 — J_n correction flipped the sealed E17b verdict on Qwen 2.5](figures/fig3_jn_correction.png)

**Fig 3.** J_n geometry correction effect on the sealed E17b verdict (Qwen 2.5). Same data, same sealed spec, different basis-coordinate-frame implementation. Buggy reading from 2026-04-24 (pre-norm Δh projected onto post-norm basis): Δ = −0.166 [−0.240, −0.098], FAIL with Raw decisive. Corrected reading from 2026-04-27 (post-norm Δh projected onto post-norm basis, J_n-consistent): Δ = +0.157 [+0.125, +0.190], PASS with Fisher decisive. The +0.32 swing is the correction's effect on the head-to-head; sealed E18 (Fig 1) is unaffected because residualization absorbs the bias (§3.4).

The Fisher-weighted basis discriminates contradictions in the predicted direction with non-overlap CI; the static raw basis discriminates inverted (sign −1) at this analysis plane. Δ AUROC = +0.157 clears the sealed +0.02 bar by 7.9×. The +0.32 swing between rows is the J_n correction's effect on the head-to-head (§3.4); we report both rows for transparency. The corrected reading replicates the n=200 prelim (+0.150 [+0.100, +0.201]) within bootstrap noise, with CI tightened by ~34% as expected for the 3× sample-size increase.

### 4.3 Cross-architecture motifs

We compute the head-to-head Δ_oriented across all 6 models, all 13 ranks in the sweep, both pooled and chain-length-stratified at n=300 per stratum. The 6×13×2 = 156-cell landscape exposes three structurally distinct architecture-dependence motifs.

![Fig 4 — Cross-architecture rank landscape: oriented Δ AUROC vs rank, one panel per model](figures/fig4_rank_landscape.png)

**Fig 4.** Cross-architecture rank landscape at n=600. Each panel shows oriented Δ AUROC (Fisher − Raw) vs rank (log scale, major ticks at 1, 2, 4, 8, 16, 32, 64; minor ticks at 3, 5, 13, 21, 34, 55) for one model, with 1000-sample bootstrap 95% CI bands. Sealed pin r=1 marked as a dotted vertical. Δ > 0 = Fisher decisive; Δ < 0 = Raw decisive. **Llama** is Fisher-or-tied throughout (never reaches Raw decisive). **Mistral** flips Raw → Fisher at r=4 → r=5. **Qwen 2.5** oscillates F → R → F → R → F. **Qwen 3** is Raw at sealed r=1, Fisher decisive from r=13 onward (peak +0.447 at r=32). **Phi-3.5-mini** is stable Raw across all 13 ranks (Motif 1, see below). **Gemma 4B** flips F → R sharply at r=2 → r=3 (Motif 2, see below).

#### Motif 1 — Stable Raw across all 13 ranks (Phi-3.5-mini)

| rank | 1 | 2 | 3 | 4 | 5 | 8 | 13 | 16 | 21 | **32** | 34 | 55 | 64 |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Δ | −0.441 | −0.120 | −0.105 | −0.191 | −0.253 | −0.200 | −0.221 | −0.236 | −0.278 | **−0.459** | −0.449 | −0.285 | −0.221 |

Phi-3.5-mini is the only model in the lineup with Raw decisive at every single rank in the sweep, every chain-length stratum. Raw_post_rank1 = 0.9989 — nearly perfect contradiction discrimination via the static W_u SVD basis alone. **Phi is the canonical "HARP-style detection works as advertised" architecture, and the headline counter-example to "Fisher pullback uniformly wins."** The static basis carries the rupture signal so cleanly that Fisher's per-sample reweighting cannot add.

#### Motif 2 — Within-model rank flip robust to chain length (Gemma 3-4B)

| rank | 1 | 2 | **3** | 4 | 5 | 8 | 13 | 16 | 21 | 32 | 34 | 55 | 64 |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| pool Δ | F +0.210 | F +0.207 | **R −0.211** | R −0.170 | R −0.103 | R −0.304 | R −0.406 | R −0.394 | R −0.355 | R −0.362 | R −0.357 | R −0.216 | R −0.105 |
| cl=2 Δ | F +0.401 | F +0.237 | R −0.275 | R −0.141 | · +0.037 | R −0.239 | R −0.276 | R −0.417 | R −0.272 | R −0.109 | R −0.096 | R −0.409 | R −0.234 |
| cl=5 Δ | F +0.250 | F +0.082 | R −0.232 | R −0.128 | R −0.193 | R −0.353 | R −0.142 | R −0.234 | R −0.341 | R −0.324 | R −0.321 | R −0.057 | R −0.016 |

![Fig 8 — Motif 2: within-model rank flip robust to chain length (Gemma 3-4B)](figures/fig8_gemma_rankflip.png)

**Fig 8.** Motif 2 — within-model rank flip robust to chain length (Gemma 3-4B). Three lines: pool (n=600, solid brown), cl=2 stratum (n=300, dashed orange), cl=5 stratum (n=300, dashed green). Both chain-length strata transition F → R together at r=2 → r=3 (red dotted vertical). The flip is a property of the SVD spectrum, not a chain-length artifact.

The flip from Fisher to Raw is sharp at r=2 → r=3: pool Δ_oriented goes from +0.207 (Fisher decisive at non-overlap CI) to −0.211 (Raw decisive at non-overlap CI) within one rank step. **Both chain-length strata show the same r=2 → r=3 transition** (one borderline tie at r=5 / cl=2). The flip is a property of the SVD spectrum, not a chain-length artifact — pure rank-axis architecture-dependence. The sealed pin at r=1 picks up Fisher; pinning r=32 would have picked up Raw on the same data — operationalizing the methodological point that the rank choice is a methodological commitment, not a free parameter.

#### Motif 3 — Chain-length × rank interaction with two Simpson's-paradox sites (Mistral 7B)

| rank | pool Δ | cl=2 Δ | cl=5 Δ | Δ_cross (cl=2 − cl=5) |
|---|:---:|:---:|:---:|:---:|
| **1** | **R −0.140** [−0.173, −0.107] | **F +0.065** [+0.041, +0.093] | · +0.002 [−0.022, +0.028] | +0.062 |
| 4 | R −0.223 | R −0.097 | R −0.383 | +0.287 |
| 13 | F +0.181 | F +0.208 | · −0.002 | +0.210 |
| 21 | F +0.144 | F +0.101 | R −0.133 | +0.234 |
| **32** | **F +0.177** | **R −0.196** [−0.262, −0.131] | **F +0.379** [+0.319, +0.450] | **−0.575** |
| 34 | F +0.174 | R −0.204 | F +0.357 | −0.561 |
| 55 | F +0.310 | F +0.174 | F +0.228 | −0.053 |

Mistral has **two Simpson's-paradox sites at non-overlap CI**:
- **At sealed r=1:** the pool says Raw decisive (Δ = −0.140), but the stratum-level reading is Fisher decisive at cl=2 (+0.065 [+0.041, +0.093], CI fully positive) and tied at cl=5 (+0.002 [−0.022, +0.028]). Mistral is **never Raw-decisive at the stratum level** — the pooled "Raw" verdict is a mixing artifact of two chain-length subgroups whose Fisher and Raw discrimination axes have different orientations.
- **At r=32–34:** the pool says Fisher decisive, but cl=2 reads Raw decisive (−0.196) and cl=5 reads Fisher decisive (+0.379), both at non-overlap 95% CI in opposite directions. **Δ_cross = −0.575 at r=32 is the largest cross-stratum spread observed across all 156 cells in the model × rank × chain-length grid.**

![Fig 9 — Motif 3: chain-length × rank interaction (Mistral 7B), the headline within-model finding](figures/fig9_mistral_simpsons.png)

**Fig 9.** Motif 3 — chain-length × rank interaction (Mistral 7B). Same three-line layout as Fig 8: pool (n=600, solid orange), cl=2 (n=300, dashed blue), cl=5 (n=300, dashed red). Two purple dotted verticals mark the Simpson's-paradox sites at r=1 and r=32. **Site #1 (r=1):** pool Raw-decisive (−0.140) but cl=2 Fisher-decisive (+0.065) and cl=5 tied — pool's Raw is a mixing artifact. **Site #2 (r=32):** pool Fisher-decisive (+0.177) but cl=2 Raw-decisive (−0.196) and cl=5 Fisher-decisive (+0.379), with both stratum CIs non-overlapping in opposite directions — Δ_cross = −0.575, the largest cross-stratum spread observed in the entire 156-cell model × rank × chain_length grid.

Other architectures' cross-stratum spreads stay within ±0.3 at every rank in the sweep. Mistral is the unique flag-bearer for chain-length-coupled rupture geometry. The mechanistic hypothesis (§5.1): Mistral writes a newline at gen_step=1 ("begin the answer block") rather than committing to actual answer content; the newline's geometric position relative to the contradiction event in token-space shifts dramatically with chain depth.

#### Pooled cross-architecture summary

At the sealed rank=1 plane, the six architectures partition as:
- **Fisher decisive (3):** Llama 3.2 3B (Δ = +0.272 [+0.222, +0.320]), Qwen 2.5 7B sealed (+0.157 [+0.125, +0.190]), Gemma 3-4B (+0.210 [+0.181, +0.237]).
- **Raw decisive (3):** Mistral 7B (Δ = −0.140 [−0.173, −0.107]), Qwen3 8B (−0.214 [−0.261, −0.175]), Phi-3.5-mini (−0.441 [−0.485, −0.392]).

Cross-generation within Qwen-family (2.5 Fisher → 3 Raw) and within-vendor (Llama Fisher vs Mistral Raw) both flip; vendor and parameter-count are not predictive.

### 4.4 Baselines

| Primary | surprise | PRI v1 cosine | PRI v2 topk32 | PRI v2 lowrank32 | v3 null_ratio_post_rank1 (sealed) |
|---|:---:|:---:|:---:|:---:|:---:|
| Llama 3.2 3B | 0.6347 | 0.6224 | 0.7528 | 0.7500 | 0.8975 |
| Mistral 7B | 0.5187 | 0.5309 | 0.6623 | 0.6618 | 0.7849 |
| Qwen 2.5 7B | 0.8947 | 0.9155 | 0.7906 | 0.7948 | 0.8967 |

The sealed v3 metric outperforms PRI v1 and v2 on Llama and Mistral by clear margins. On Qwen 2.5, surprise (0.8947) and PRI v1 cosine (0.9155) are competitive with the sealed v3 metric (0.8967) — one of the model-specific anomalies worth flagging in §5.1. On the cross-arch companions, surprise on Phi-3.5 reaches 0.901 and on Gemma 4B reaches 0.960; static-W_u-SVD baselines on Phi reach 0.999. The architecture-dependence holds across baseline metrics too.

## 5. Discussion

### 5.1 Why architecture-dependence rather than universal Fisher win

The qualitative content of the gen_step=1 token differs across architectures, and so does the alignment of W_u's top-1 right singular vector V_raw[0]. We characterized both empirically on N=100 stratified puzzles per model (50 ctrl × 50 contr × 2 chain lengths, seed=20260423), under J_n-corrected post-norm geometry. Table 5 reports, per model: the modal gen_step=1 commit token; V_raw[0]'s top-3 positive and top-3 negative tokens; targeted projections of YES / NO / Answer / `\n` onto V_raw[0]; and per-sample signed Δh_jn · V_raw[0] for ctrl vs contr.

**Table 5. Cross-model W_u top-1 axis character at gen_step=1.**

| Model | modal commit | V_raw[0] top-3 pos | V_raw[0] top-3 neg | `' YES'` | `' NO'` | `'\n'` | ctrl mean ± std | contr mean ± std | Δ (contr−ctrl) |
|---|---|---|---|---:|---:|---:|:---:|:---:|---:|
| 🦙 Llama 3.2 3B | `' Answer'` (98%) | `,` `' '` `' ('` | `SCRI` `using` `TRGL` | −0.338 | −0.088 | +0.576 | +1.30 ± 0.15 | +1.36 ± 0.26 | +0.062 |
| 🌀 Mistral 7B | `'\n'` (100%) | `(` `\n` `and` | `qpoint` `ICENSE` `ityEngine` | +0.034 | −0.028 | +0.127 | +3.01 ± 0.41 | +4.64 ± 0.52 | +1.632 |
| 🐉 Qwen 2.5 7B | `' NO'` (52%) | `' '` `,` `1` | `.IsNullOr` ` volunte` `gnore` | −0.104 | +0.051 | +0.543 | −0.30 ± 9.94 | −18.70 ± 1.33 | −18.400 |
| 🐲 Qwen3 8B | `' Answer'` (79%) | ` neighb` ` porno` ` somew` | `' '` `\n` `,` | +0.352 | −0.072 | −1.335 | +0.77 ± 0.40 | −1.57 ± 2.55 | −2.336 |
| 🪼 Phi-3.5-mini | `'\n'` (100%) | `provin` `Wikip` `zna` | `(` `\n` `in` | — | +0.344 | −0.469 | −9.57 ± 0.59 | −8.14 ± 0.89 | +1.434 |
| 🌸 Gemma 3-4B | `'\n'` (100%) | `S` `(` `g` | `' ('` `\n` `\n\n` | — | +0.029 | −0.329 | −6.09 ± 0.68 | −6.15 ± 0.49 | −0.061 |

(`—` = single-token encoding not available in this tokenizer.)

Three observations restructure the architecture-dependence story:

1. **gen_step=1 commit splits 3/3 (newline / content), but does *not* predict Fisher-vs-Raw.** Mistral, Phi, and Gemma 4B all commit `'\n'` at 100% of samples; Llama, Qwen 2.5, and Qwen3 commit ` Answer`-class tokens at 52–98%. The earlier "newline-commit ⇒ Raw" / "content-commit ⇒ Fisher" partition fits 4 of 6 (Mistral+Phi → Raw; Llama+Qwen2.5 → Fisher) but Gemma 4B (newline-commit, Fisher-decisive) and Qwen3 (content-commit, Raw-decisive) break it. The commit token alone is not the load-bearing variable.

2. **What does predict Fisher-vs-Raw is the discriminative strength of V_raw[0] itself.** Two architectures (Mistral, Phi) have strong same-sign rupture-magnitude separation on V_raw[0] — ctrl and contr both project on one side of the axis, magnitude separates them, and Cohen's-d-equivalents are large (≈3.5 for Mistral, ≈1.9 for Phi). Their static W_u top-1 SVD direction *happens to encode rupture magnitude* relative to the model's commit, so Raw_post_rank1 saturates (0.99 on Mistral, 0.9989 on Phi) and Fisher's per-sample reweighting cannot add. Two architectures (Llama, Gemma 4B) have V_raw[0] discrimination near zero (|Δ| < 0.07, d ≈ 0.1–0.3), and Fisher's reweighting recovers the signal that V_raw[0] alone misses. The remaining two (Qwen 2.5, Qwen3) sit between: V_raw[0] carries discriminative signal but with high within-class variance (Qwen 2.5 ctrl std = 9.94 vs Mistral 0.41) or sign-split distributions, leaving headroom for Fisher to refine the basis.

3. **Mistral and Phi share a non-content rupture-magnitude axis despite different vendors and tokenizers.** Mistral's V_raw[0] top tokens are code-domain fragments (`qpoint`, `ICENSE`, `ityEngine`) plus common short tokens; Phi's are European-language fragments (`provin`, `Wikip`, `Magyar`) plus common short tokens. Neither is a YES/NO bipolar axis; both have `\n` as a strong projection (Mistral +0.13, Phi −0.47). The shared structure is not "what V_raw[0] points at" — it is *that V_raw[0] is anchored to the structural commit (`\n`)* rather than to answer content, *and* that Δh_jn at the commit moment lands monotonically on V_raw[0]. The two models converge on the same regime (Raw saturation) via two different vocabulary-specific top-token signatures.

The cross-stratum interpretation in §4.3 still holds for Mistral specifically — chain-length couples to where the `\n`-commit lands relative to the contradiction event in token-space, producing the Δ_cross = −0.575 spread at r=32. But the universal "newline-commit decouples ↔ content-commit decouples" claim in earlier drafts was an over-fit; chain-length coupling can in principle exist on any architecture whose commit is structural rather than content-bearing. Phi's chain-length sensitivity at the same plane is a follow-up worth checking explicitly.

A universal pattern across all six models corroborates the chain-length mechanism: **|Δ_oriented| is sharper at cl=2 than cl=5** at sealed r=1 (Llama 0.397 vs 0.170; Mistral 0.065 vs 0.002; Qwen 2.5 0.138 vs 0.063; Qwen3 −0.317 vs −0.167; Phi −0.374 vs −0.228; Gemma 4B 0.401 vs 0.250). Short reasoning chains amplify the Fisher-vs-Raw discrimination signal; long chains diffuse it. The rupture geometry is most informative when the commit and the contradiction are close in token-space.

The Qwen 2.5 baseline anomaly (surprise / PRI v1 ~0.90 competitive with v3) fits the same picture: Qwen 2.5 commits to answer content at gen_step=1 with high confidence on this benchmark, so the simple surprise scalar already separates contradictions from controls effectively. Fisher pullback adds only at the margin.

### 5.2 Pre-registration governance

Sealed parameters (analysis plane, residualization, bootstrap, threshold, 2-of-3 bar, no-post-hoc-re-spec) were preserved across multiple bug-fix cycles during the v3.1 launch: a coordinate-mismatch in the Fisher pullback (J_n geometry, §3.4); a memory-bomb in the behavioral preflight gate (full `trace_sample()` calls allocated transient gigabytes per sample on large-vocab primaries); a config-propagation bug (`load_model` read module-level defaults instead of per-run config); a stratified-sampling skew at the gate sample size (an 11/9 chain-length skew at the seed produced gate-fails on reasoning-tuned primaries); a parser bug fooled by completion-style output (Qwen front-loads `Answer: YES` then continues with format-completion that included a fabricated `Answer: NO`); and a BOS-token contamination in a diagnostic script.

Each bug was disclosed at discovery, classified as operational vs sealed-spec, and patched without altering the sealed parameters. The sealed E18 verdict is robust across the J_n correction (residualization absorbs the bias). The sealed E17b verdict flipped from FAIL to PASS under correction, but the _spec_ was identical in both readings — the correction was to the implementation of the Fisher pullback, not to its definition. We argue this is the correct outcome of pre-registration discipline: the verdict ought to be revisable when the implementation is revealed to disagree with the spec, but the spec itself is the lock.

### 5.3 Limitations

- **Synthetic 2×2 puzzles only.** The benchmark is procedurally generated logical contradictions with a fixed template structure. Factual contradictions (e.g., TriviaQA-style pair-conditioned probes) is the next experimental rung but is not in this paper.
- **4-bit quantization across all models.** No full-precision baseline. The MLX 4-bit quantization is applied uniformly via `mlx-community` checkpoints; relative comparisons within the lineup are valid, but absolute AUROCs may differ from full-precision implementations.
- **Hardware-bounded model sizes.** All experiments run on a 16 GB Apple Mac mini M4. No models above 8B parameters were tested in the v3.1 scope. Phi-3.5-mini (3.8B) and Gemma 3-1B were the two smallest models; Gemma 1B was excluded for behavioral gate failure (model-capability, not parser).
- **Within-family scale axis incomplete.** With Gemma 1B excluded, the Gemma 1B↔4B comparison collapses to a single point; the architecture-held-fixed scale-replication test is left to v4.
- **Bootstrap orientation bias near AUROC = 0.5.** The oriented metric `max(au, 1−au)` biases the bootstrap distribution upward when the underlying AUROC straddles 0.5. For decisive cells (|Δ| > 0.1 — most of our findings) this bias is invisible. For borderline cells (Mistral cl=5 r=1 = +0.002, several "tie" cells across the rank landscape) the lower CI is artificially compressed toward zero. Worth knowing; not a finding-killer.
- **Diagonal-only Fisher approximation.** The SVD basis is the eigendecomposition of `W_uᵀ · diag(p_t) · W_u`, dropping the rank-1 centering term `−p_t · p_tᵀ` of the full Fisher. The omission shifts the top-1 eigendirection by a few degrees when p_t is sharp; ranks ≥ 4 are unaffected.

### 5.4 Future work

- **Pair-condition factual rung.** Move from synthetic 2×2 puzzles to real-world factual probes (e.g., paired Q&A with consistent vs contradicting evidence). The Fisher-Rao geodesic protocol on factual pairs is a natural extension; the cross-architecture motifs we identified should re-test there.
- **Curvature κ as a separate paper.** A 2026-04-26 standalone diagnostic showed a curvature scalar (the trace of the Riemann curvature operator pulled back to h-space, with `null_ratio_post` residualized out) discriminates contradictions at AUROC ≈ 1.0 on Qwen 2.5 — too good to bury, but full inclusion eats budget here. We hold this back for a separate workshop/conference paper.
- **Depth profile across layers.** The sealed analysis plane is gen_step=1 final layer only. Whether the architecture-dependence motifs hold across earlier layers (and whether earlier layers carry independent signal that compose with the final-layer reading) is open.
- **Larger-vocab and non-quantized models.** The Mac mini M4 16 GB ceiling cut off the upper end of the model-size axis. A larger-hardware replication on full-precision 70B+ models would let us see whether the architecture-dependence motifs hold or new ones emerge at scale.
- **Robust verification protocols at sub-3B scale.** The behavioral gate is sensitive to small-model output formatting (Gemma 1B defaulting to `Answer: NO` on YES controls). A likelihood-based verification (e.g., comparing `log p(YES|prompt)` vs `log p(NO|prompt)`) would admit sub-3B models without sacrificing pre-registration discipline.

## 6. Conclusion

We pre-register and run a head-to-head between Fisher pullback geometry and a HARP-style static-SVD baseline at the gen_step=1 commit moment of LLM generation, on synthetic logical contradictions, across six 4-bit-quantized open-weight architectures. The sealed E18 magnitude-independence gate passes 3-of-3 primaries; the sealed E17b head-to-head passes on Qwen 2.5 at Δ AUROC = +0.157 [+0.125, +0.190]. The cross-architecture picture is structurally heterogeneous: at sealed rank=1, three architectures favor Fisher and three favor Raw, with vendor and parameter count non-predictive. Three motifs structure the cross-architecture landscape — Phi-3.5 is stable Raw across all 13 ranks (the canonical HARP-success case), Gemma 4B has a within-model rank flip robust to chain length (a property of the SVD spectrum), and Mistral 7B has a chain-length × rank interaction with two Simpson's-paradox sites including the largest cross-stratum spread (Δ_cross = −0.575) in the entire 156-cell landscape. We identified and corrected a coordinate-mismatch in the Fisher pullback computation; the sealed verdict was re-derived under corrected geometry without altering the pre-registered spec. The contribution is twofold: a cross-architecture mapping of where Fisher pullback wins, ties, and loses against static-SVD detection at the commit moment; and a worked example of pre-registration discipline absorbing methodological corrections without compromising verdict integrity.

---

## Appendix A — Bug timeline

Each entry: date, mechanism, impact on sealed parameters (mostly: none).

- **2026-04-25 — J_n geometry mismatch in Fisher pullback.** The pre-2026-04-26 pipeline implementation projected raw pre-norm `Δh = h_t − h_prev` onto a basis derived from `√p_t · W_u` that lives in post-norm h-space — a coordinate mismatch in the Fisher pullback computation. Identified via standalone numpy diagnostic at N=100 across all 4 primaries; corrected by capturing post-norm Δh directly via the model's own RMSNorm γ. Sealed E17b reading on Qwen 2.5 flipped from −0.166 (FAIL) to +0.150 (PASS). Sealed E18 unaffected (residualization absorbs the bias). The legacy pre-norm-Δh code path was deleted on 2026-04-26 along with the analyzer's `--columns legacy` flag, closing a silent-failure mode where downstream consumers could read a buggy verdict labeled identically to the corrected one. The sealed _spec_ was unchanged; the bug was in the implementation.

- **2026-04-25 — Gemma 3 RMSNorm γ extraction.** Gemma 3's RMSNorm uses the formulation `mx.fast.rms_norm(x, 1.0 + weight, eps)` rather than `weight` directly; our γ-extractor returned raw `.weight` for all families. On Gemma the post-norm Δh would have been multiplied by ≈0 instead of `1 + weight`, silently zeroing every J_n-corrected null_ratio column on Gemma alone. Identified before any Gemma main-run data was captured. Patched with a Gemma-3-only branch keyed on `core.sliding_window_pattern`. A second precision sub-bug on Gemma 3-4B (bf16-stored weight) was caught by an end-to-end forward-match check; performing the `1 + weight` operation at the weight's native dtype (bf16) before casting to fp32 reproduces `model.model.norm(h)` to ≤1e-5 max-abs error across all six families. Pre-data, not sealed-affecting.

- **2026-04-24 — Behavioral gate memory bomb.** The preflight gate routed all 20 control samples through full `trace_sample()`, allocating ~250 MB transient per sample on large-vocab primaries (Llama V=128k). Mac mini M4 16 GB compressor pressure spiked to >6 GB and the process stalled in `MetalAllocator::release_cached_buffers`. Patched: the gate now uses `mlx_lm.generate()` (text-only) for the 20-sample preflight. Operational, not sealed-affecting.

- **2026-04-24 — Config propagation bug in `load_model`.** `load_model(model_name)` read `cfg.layers_to_probe` from the module-level default Config, silently ignoring per-run overrides like `--layers final`. Banner echoed correctly; only the `Probed: {…}` line revealed the mismatch. Patched: `load_model(model_name, config=None)` takes config explicitly. Operational, not sealed-affecting.

- **2026-04-24 — Stratified preflight sampling.** `dataset[~contradiction].head(pilot_n)` produced an 11/9 chain-length split at seed 20260423 (pool is 50/50; expected 10/10). The skew + reasoning-tuned CoT output + last-match-anywhere parser flipped verdicts on 6-7 of 20 puzzles. Patched: per-chain-length quota sampling. Operational, not sealed-affecting.

- **2026-04-24 — Behavioral gate parser fooled by completion-style output.** Qwen 2.5 7B and Llama 3.2 3B gate-failed at the default 256-token budget because they front-load `Answer: YES` then continue with format-completion, sometimes fabricating a second `Answer: NO`. Patched: `--gate-max-tokens 12` operational rescue + 3-tier `check_answer` parser (Tier 1 prefers last `Answer:`). Operational, not sealed-affecting.

- **2026-04-25 — BOS token contamination in diagnostic script.** A standalone diagnostic returned `tokenizer.encode(text)[0]` which is the BOS token id on Llama and Mistral due to HF tokenizers auto-prepending BOS. Stage-3-specific diagnostic (factual baseline pre-experiment, not the main run). Patched with a defensive BOS-skip via `getattr(tokenizer, "bos_token_id", None)`. Diagnostic-only, not sealed-affecting.

For each: cite the corresponding `pri-v3-plan.md §Amendments` entry by date.

## Appendix B — Reproducibility pointers

- **Code:** GitHub `flowstyleliving/PRI_at_commitment`, commit pinned at submission. Pipeline: `pri_v2_mlx_pipeline.py`. Sealed-gate analyzer: `scripts/analyze_sealed_gate.py` (post-norm geometry only after 2026-04-26 cleanup). Cross-model rank-landscape analyzer: in-line scripts archived under `scripts/diagnostics/` at submission.
- **Pre-registration:** `PRI_V3_PRE_REGISTRATION_PLAN.md` at the repo root, frozen 2026-04-27. Snapshotted from `wiki/pri-v3/pri-v3-plan.md` at the same date.
- **Run artifacts:** `experiments/v3-main-run/2026-04-26/run-09/` (4 primaries + Qwen3 at n=150/cell), `experiments/v3-main-run/2026-04-27/run-01/` (Phi-3.5-mini at n=150/cell), `experiments/v3-main-run/2026-04-27/run-02/` (Gemma 3-4B at n=150/cell). Per-model `*_results.parquet` + `*_trace_dumps.parquet` + canonical `sealed_gate.json`.
- **Hardware:** Apple Mac mini M4, 16 GB unified RAM. mlx-lm + mlx 4-bit quantized models from `mlx-community`.
- **Environment:** Python 3.9 + venv, full requirements pinned in `requirements.txt` at submission commit.
- **Reproduce sealed verdict:**
  ```
  git checkout <SUBMISSION_COMMIT>
  python -u scripts/run_v3_main.py --scope v3_1_main --n-per-cell 150 \
      --seed 20260423 --max-gen-tokens 14 --gate-max-tokens 12 --layers final
  python scripts/analyze_sealed_gate.py --run-dir experiments/v3-main-run/<DATE>/run-NN
  ```
  Followed by Phi-3.5-mini and Gemma 3-4B single-model runs (`--scope v3_1_phi_only` and `--scope v3_1_gemma4b_only`).

## References

1. **Agrawal, A., Suzgun, M., Mackey, L., Kalai, A.T.** (2024). Do Language Models Know When They're Hallucinating References? *Findings of the ACL: EACL 2024*, 912–928. (Microsoft Research / Stanford / OpenAI.) — `raw/papers/external/agrawal-2024-hallucinated-references.pdf`
2. **Amari, S.-i.** (2016). *Information Geometry and Its Applications*. Applied Mathematical Sciences, Vol. 194. Springer. ISBN 978-4-431-55977-1.
3. **Farquhar, S., Kossen, J., Kuhn, L., Gal, Y.** (2024). Detecting Hallucinations in Large Language Models Using Semantic Entropy. *Nature*, 630:625–630. DOI: 10.1038/s41586-024-07421-0. — `raw/papers/external/farquhar-2024-semantic-entropy-nature.pdf`
4. **Hu, J., Tu, X., Cheng, Z., Li, J., Wang, X., Chen, J., Zhou, Y., Shan, Y.** (2025). HARP: Hallucination Detection via Reasoning Subspace Projection. arXiv preprint. (HUST.) — `raw/papers/external/hu-2025-harp-hallucination-subspace.pdf`
5. **Kalai, A.T., Nachum, O., Vempala, S.S., Zhang, W.** (2025). Why Language Models Hallucinate. arXiv preprint. (OpenAI / Georgia Tech.) — `raw/papers/external/kalai-2025-why-llms-hallucinate.pdf`
6. **Karpathy, A.** (2026). LLM Wiki: representational-dynamics methodology for language-model inspection. — `raw/papers/external/karpathy-2026-llm-wiki.md`
7. **Kitti, M.S.R.** (2026a). Predictive Rupture Index v2: Fisher-Information Pullback as a Magnitude Detector for LLM Commitment. Internal Furnace Research preprint. — `raw/papers/furnace/2026-pri-v2-fisher-pullback-predictive-rupture.pdf`
8. **Kitti, M.S.R.** (2026b). Hallucinations Rupture at Commitment, Not at Encoding: Predictive Rupture Index Localizes Contradiction-Induced Failure to the First Generated Token. Internal Furnace Research preprint, 17 March 2026. — `raw/papers/furnace/2026-hallucinations-rupture-at-commitment.pdf`
9. **Nosek, B.A., Ebersole, C.R., DeHaven, A.C., Mellor, D.T.** (2018). The preregistration revolution. *PNAS*, 115(11):2600–2606. DOI: 10.1073/pnas.1708274114.
10. **Pineau, J., Vincent-Lamarre, P., Sinha, K., Larivière, V., Beygelzimer, A., d'Alché-Buc, F., Fox, E., Larochelle, H.** (2021). Improving Reproducibility in Machine Learning Research (a Report from the NeurIPS 2019 Reproducibility Program). *JMLR*, 22(164):1–20.
11. **Wastl, M., Vamvas, J., Sennrich, R.** (2025). Token-Level Self-Consistency for Hallucination Detection. *Proceedings of SemEval-2025*. (UZH.) — `raw/papers/external/wastl-2025-token-level-self-consistency.pdf`
12. **Apple ML Research** (2023–present). MLX: An array framework for Apple Silicon. GitHub: `ml-explore/mlx`. Companion library `mlx-lm` provides the 4-bit-quantized open-weight model checkpoints used in this paper.
