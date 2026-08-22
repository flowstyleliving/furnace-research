# SUP Theory Notes — v3-Relevant Distillations

Curated 2026-04-14 by reading the SUP corpus (`raw/sup/`) for what bears on PRI v3. Not a faithful summary of each paper — a working theory map, oriented around what predicts or constrains v3 observables. Expanded 2026-04-14 (second pass) with quantitative findings from v16 / from-error-to-essence / cognitive-speciation / taxonomy-v4.

> **Epistemic status — provisional, take with salt.** Every number, table, correlation, and calibration below is *extracted from the SUP papers as stated by their author*. These papers are the theoretical provenance of the current PRI line; they are **not independently replicated, not peer-reviewed, and not yet verified by Furnace**. Treat claims as **hypotheses to be tested**, not established results. Specific numbers to independently validate before citing externally: the `[10², 10⁴]` Fisher-spectrum band, `λ ≈ 4.36 / τ ≈ 0.430` calibration, 75.4%/5.9% hierarchy-detection gap, 94.7% Byzantine recovery at ε=0.05, per-model taxonomy-v4 success rates, the Species 0/1 partition, the τ ∈ [0.36, 0.54] cluster, and the BERT `d_eff ≈ 9.31 / packing 87.18` measurement. When these priors inform v3 design, mark them `[SUP-PROVISIONAL]` in `claims.md` rather than `[VALIDATED]`. Treat this page as a **working hypothesis register**, not a results document.

## 1. The SUP equation (canonical form)
```
∆µ(C) × ∆σ(C) ≥ ℏs(C)
```
- `∆µ(C)` — precision of representation. In the Fisher-enhanced version (`from-error-to-essence`, Def. 2): `∆µ(C) = κ_dim / sqrt(det(I(θ_C)))`. High Fisher determinant = sharp/precise; low det = flat/flexible.
- `∆σ(C)` — semantic flexibility. From the curvature (Def. 3): `∆σ(C) = κ_curv · sqrt(1 / (|R(θ_C)| + ε_reg))` where `R` is Ricci scalar of the Fisher manifold.
- `ℏs(C)` — concept-dependent semantic constant. In the Cramér-Rao form: `ℏs(C) = κ_info / sqrt(I_prec(C) · I_flex(C))`. In the directional form: `ℏ_s(C) = (u_C^T I(θ_C)^(-1) u_C) / (u_C^T I(θ_C) u_C)`.

**Hard lower bound.** `ℏ_s(C) ≥ 1` for any SPD `I` and unit `u_C` (Horn & Johnson, *Matrix Analysis*, Theorem 7.7.6: `(u^T A u)(u^T A^{-1} u) ≥ 1`). Equality only when `u_C` is an eigenvector of `I` (i.e., flat/isotropic along that direction). **Cramér-Rao consequence.** If `ℏ_s(C) < 1` then `Var[θ̂_u] < 1/(u^T I u)`, violating Cramér-Rao → estimator inconsistency. So `ℏ_s ≥ 1` is *necessary* for statistical validity, not just a modeling choice.

**Thesis:** intelligence requires *bounded imprecision*. Concepts with zero flexibility lose semantic capability; with zero precision they lose meaning. The system orbits an equilibrium, not a point.

## 2. Direct v3 priors (the load-bearing parts)

### 2.1 Middle layers > final layers for semantics
(`taxonomy-distance-v4`, `why-imprecision-v2`)

- Similarity-tuned 12-layer models: layers **-6 to -8** optimal for hierarchy detection (**75.4%** success); **final layer fails** (**5.9%**). Cohen's d = 2.31 between architectures.
- 6-layer models: layer **-6** optimal.
- Per-model best-layer success (taxonomy-v4 Table 3): all-mpnet 77.1%, all-MiniLM 73.3%, distilbert 23.3%, bert-base 2.9%, roberta 0.0%, albert 0.0%.
- Per-domain correlations at best layer (mean ρ = 0.762): Technological 0.871, Emotional 0.862, Perceptual 0.788, Biological 0.671, Spatial 0.617.
- Overall best-layer success: **61.9%** (vs 46.2% final-layer; +13.3% improvement; +20–30% for similarity-tuned).
- Layer uncertainty profile predicted by SUP (`why-imprecision-v2` Lemma 1): `∆σ^(l) ∝ exp(-|l - L/2|/τ)`. Middle-layer peak.
- Protocol: 6 paraphrases/level, 1000 permutations, FDR correction, success criterion `|ρ| > 0.5 ∧ q < 0.05`.

**v3 implication.** Strong prior for E21 (characteristic depth). The depth profile of `null_ratio_ℓ` should *not* peak at the final layer for hierarchy-laden contradictions. If it peaks middle-late (`ℓ/L ∈ [0.6, 0.8]`), consistent with SUP. If it peaks at the final layer, that is novel and contradicts SUP — flag it.

> **Update 2026-04-15 — did not replicate on Furnace hidden-state sweep.** Our layer sweep did not reproduce the middle-layer peak. Likely architectural mismatch: the SUP result is from **encoder / MLM / similarity-tuned sentence-transformers** (mpnet, MiniLM, BERT), which are symmetric encoders whose middle layers carry the semantic payload. Furnace runs **decoder-only causal LMs** (Llama, Mistral, Qwen), where representations are built progressively toward the unembedding and the "semantic peak" is pushed later / distributed differently. The E21 prior as stated is not portable across the encoder→decoder boundary. Treat the middle-layer claim as **encoder-specific** until re-derived for causal decoders.

### 2.2 Fisher spectral signature (the strongest v3 prior)
(`from-error-to-essence`, §4.1; also v16 §2)

Two explicit spectral conditions for effective semantic encoding:
```
λ_max^(ℓ) / λ_mean^(ℓ) ∈ [10², 10⁴]           (Prediction 1)
tr(I^(ℓ)) / det(I^(ℓ))^{1/d} < τ_critical      (Prediction 2)
```
Empirical validation:
- Optimal layers (75.4% success): `λ_max/λ_mean ∈ [10^2.3, 10^3.7]` — inside the predicted band.
- Final layer (5.9% success): `λ_max/λ_mean > 10^6` — pathological.
- In PGN training runs, optimal orbit (ε=0.05, 94.7% Byzantine recovery) shows `det(I) ∈ [10², 10⁴]`; exact convergence (ε=0, 67.3% recovery) shows `det(I) ∈ [10⁶, 10⁸]` (over-precise/brittle).

**v3 implication — direct.** This is essentially E20 (`pri_v3_spectrum`) re-stated as a SUP prediction. Plot `λ_max / λ_mean` per layer and compare against the SUP-predicted `[10², 10⁴]` band. Final layers should sit above the band; middle-late layers inside. Is the band *the* structural signature that separates informative layers from collapsed ones.

> **Update 2026-04-15 — spectral-band run did not land.** Our hidden-state spectral sweep did not show the predicted `[10², 10⁴]` band separation across layers. Same architectural caveat as §2.1: the SUP calibration comes from **encoder / similarity-tuned sentence-transformers** (mpnet, MiniLM, BERT — symmetric bidirectional attention, contrastive / MLM objectives). Furnace's decoder-only causal LMs have a fundamentally different Fisher geometry — causal masking + autoregressive objective produce a monotonic rather than mid-peaked information profile. The `[10², 10⁴]` band and the "final-layer pathological" claim are **encoder artifacts** on current evidence. For v3 we should either (a) re-run on an encoder model to confirm the SUP result ports at all, or (b) re-derive the spectral prediction for causal decoders before citing it. Flag this in `claims.md`: E20 band moves from `[SUP-PROVISIONAL]` toward `[OPEN — architecture-specific]`.

### 2.3 Bounded-imprecision = null space is necessary
(`why-imprecision-v2`, §1.2 + §3)

> "Systems forced to converge exactly lose semantic capability."
> "Optimal intelligence requires maintaining uncertainty ≈ √ℏs."

**v3 implication.** A healthy model *must* have a non-trivial null space at every layer — the SUP minimum imprecision budget. Contradiction commitment forces the model to act decisively when no semantically-coherent answer exists; it has to discharge the action *somewhere*. SUP predicts: into the null space. That is the v3 thesis stated in SUP language.

This reframes `null_ratio` from "signal of strain" to "signal of SUP-bound violation in action." Worth saying in the v3 paper's discussion.

### 2.4 Orbital convergence — equilibrium is a radius, not a point
(`why-imprecision-v2`, Theorem 1; `from-error-to-essence`, §3.1)

PGN result (`why-imprecision-v2` Table 1):
| ε | orbit radius | detection rate | recovery |
|---|---|---|---|
| 0 | 0 | 45.2% | 67.3% |
| 0.01 | 0.41 | 61.7% | 89.1% |
| 0.05 | 2.07 | 78.9% | **94.7%** |
| 0.10 | 4.13 | 71.3% | 85.2% |
| 0.20 | 8.27 | 52.1% | 71.2% |

Linear relationship: `R² = 0.926` for `r` vs `ε/µ`. Optimal fault tolerance: `ε_opt = √(ℏ_s · µ)`.

**v3 implication.** The model's "normal" Δh trajectory under non-contradictory generation should orbit a stable subspace (the informed subspace). Contradictions force the trajectory off-orbit — into the null. Grounds the magnitude-independence test (E18): controls have stable `||Δh||` orbiting in informed directions; ruptures have similar magnitude but tilt into null.

### 2.5 Cognitive speciation
(`cognitive-speciation-v2`)

Different training objectives → "cognitive species" with distinct internal geometries. Two species discovered:
- **Species 0 (Relational-Similarity Specialists):** MiniLM, mpnet, multilingual. Relational reasoning `R = 0.507 ± 0.315`; generative capability `G = 0.089 ± 0.085`; Fisher `λ_max/λ_mean ≈ 10³`; 4.2σ above random.
- **Species 1 (Generative-Predictive Specialist):** GPT-2. `R = 0.997`; `G = 1.000`; low Fisher determinant / high rank (maximal flexibility); >6σ above random.

Clustering result: MLM models (BERT, RoBERTa) cluster *with* similarity-trained, not with CLM (GPT-2). Training objective dominates tokenization (within-objective WordPiece vs BPE: 5.06 vs 1.23 semantic density — secondary effect).

**v3 implication.** Cross-architecture transfer (Llama / Mistral / Qwen / Qwen3 / Gemma / Phi) is *not* expected to be uniform. Each architecture has a different characteristic depth and spectrum shape. Qwen v1 inversion (`AUROC 0.083`, g −1.99 — see `claims.md`) and `pri_v2_diag` model-dependence are consistent with cognitive speciation. Qwen's preference for `lowrank32` (vs `topk32` for Llama/Mistral) likely tracks a species boundary. Don't expect every model to peak at the same `ℓ/L`.

## 3. Semantic Failure Law (new, from v16)

A concrete failure probability as a sigmoid in `ℏ_s(C)`:
```
P_fail(C) = 1 / (1 + exp[-λ (ℏ_s(C) - τ)])
```

Derived three independent ways (`v16` Appendix C), all converging on the same form:
1. **MaxEnt:** maximize `H[P]` under expected-uncertainty constraint ⇒ `λ` is Lagrange multiplier.
2. **Rate-distortion:** `λ := dR/dD |_{D=ℏ_s(C)}` — rate of information cost per semantic uncertainty unit.
3. **Thermodynamic analogy:** `ℏ_s ~ temperature`, `τ ~ phase-change threshold`, `λ ~ specific heat`.

**Empirical calibration (v16 §6.4, BERT-base-uncased on CIFAR-derived semantic classes):**
- **λ ≈ 4.36**
- **τ ≈ 0.430**
- τ clusters tightly in `[0.36, 0.54]`. Biological categories (mammal, big_cat) have high τ (robust); technical categories (cpu, cpu_core) have low τ with high ℏ_s (fragile).

**τ has three geometric forms:**
- Orbital: `τ = κ / r(C)` where `r(C) = 1/√|R(C)|` — semantic radius of curvature.
- Scalar-curvature: `τ(C) = κ · √|R(C)|`.
- Phase-transition: `τ = ΔQ / C_s` — minimum semantic energy to escape stable orbit.

**v3 implication.** Could let v3 report `P_fail` per token, not just rank-AUROC. If `ℏ_s` in a contradiction → sharp sigmoid tip of the logistic; if in control → flat plateau. Even without fitting λ,τ directly, the sigmoid shape is a strong functional prior for calibration curves. Skipped for now (v3 is empirical/exploratory); worth flagging for v4.

## 4. MDL / dual form of ℏ_s (practical substitute for Fisher)
(`v16` §5.4 + §6.2)

When direct `I(θ_C)` computation is infeasible (large transformers), approximate:
```
ℏ_s(C) ≈ L(C) · [L(C+δ) - L(C)]
```
where `L(C) = -log p_θ(C)` (NLL) and `δ` is a semantic-preserving perturbation (synonym, paraphrase, mask). Second-order Taylor: `L(C+δ) - L(C) ≈ ½ δ^T I(θ_C) δ`, so `ℏ_s^{MDL} ≈ ½ L(C) · δ^T I(θ_C) δ`. This is why MDL and Fisher forms track the same underlying quantity, up to a scale that depends on perturbation magnitude.

**Empirical behavior** (v16 §7.4, BERT-base, 45 inputs × 3 perturbations):
- Mean `ℏ_s(C) = -0.00068`, median 0.00000, std 0.0280. Outlier rate (IQR) 8.9%.
- `Corr(ℏ_s, Loss Difference) = 0.984` — the curvature term dominates.
- `Corr(ℏ_s, Original Loss) = -0.591` — high-confidence predictions often have *negative* ℏ_s (overconfident brittleness).
- Masked tokens produce largest and most variable ℏ_s; synonyms lowest; paraphrases intermediate.

**v3 implication.** Furnace could compute a cheap MDL-ℏ as a sanity-check baseline for v3's Fisher-based null_ratio. If `ℏ_s^{MDL}` correlates strongly with `null_ratio` on contradictions, that is independent corroboration. Not load-bearing but useful robustness story. The "negative ℏ_s" observation is worth checking — our internal metric might have an analogous overconfidence pathology.

## 5. Tightness ratio and the 2D uncertainty space (v16 §6.5, §7.5)

**Tightness ratio:** `T(C) = ℏ_s^{MDL}(C) / ℏ_s^{Fisher}(C)`. Measures how close a concept is to the critical balance `τ`.

Findings on 9 CIFAR-10 classes:
- All classes are **underconstrained** (`T(C) > τ`), ranging 53.57 to 69.19.
- Classes closest to critical: C1 (T=53.57), C6 (T=54.93), C3 (T=56.70).
- Tightness ↔ accuracy correlation `r = 0.042` (non-significant). Proximity to τ does not trivially predict surface accuracy.

**2D Semantic Uncertainty Map:** Fisher-ℏ vs MDL-ℏ. Weakly correlated (`r=0.095, p=0.81; ρ=-0.083, p=0.83`). The low correlation is a *structural signal*, not noise — Fisher captures *local curvature* (belief sharpness) and MDL captures *global fragility* (behavior under perturbation). Quadrants: sharp/brittle (C0), sharp/robust (C6), loose/brittle (C2,C3,C7), loose/robust (C4,C5).

**v3 implication.** If we want to stratify contradiction strain by type, `(Fisher, MDL)` is a meaningful 2D decomposition. Two different failure modes: sharp-but-brittle concepts fail under perturbation (MDL high); loose-but-robust concepts can be wrong confidently (Fisher low). This maps onto v3 observables if we can compute both — `null_ratio` is closer to Fisher-flavored; perturbation tests would give MDL-flavored.

## 6. Packing ratio and intrinsic dimensionality (v16 §7.6)

On BERT-base activations (D=768) across 5 concepts (science, emotion, nature, technology, food):
- Mean intrinsic dimension `d_eff = 9.31` → **1.2% dimension usage**.
- Mean packing ratio `D/d_eff = 87.18` — the model uses \~1 of every 87 dimensions per concept.
- `Corr(d_eff, ℏ_s) = 0.243`; `Corr(Packing, ℏ_s) = -0.198`.

**v3 implication.** If most of the representation space is unused at steady state, then the null space has *plenty* of room. The high packing ratio is permissive toward v3's null-discharge hypothesis: there's slack for contradictions to get pushed into. Caveat: packing is measured globally across concepts, not per-token; our null-ratio is per-token. Still a useful framing for the v3 discussion.

## 7. Species-dependent ℏ_s formula (cognitive-speciation)

Formal species-aware definition:
```
ℏ_s(C, S) = κ · ∆µ(C) · I(C;W) / H[p(C)]
```
with `κ ≈ 0.024` (from rate-distortion: `embedding_dim² / info_content`). Empirically observed on a biological hierarchy: `organism` ℏ_s ≈ 0.176 → `tiger` ℏ_s ≈ 0.024. **More specific concepts have lower semantic uncertainty**, which aligns with the taxonomy hierarchy: deeper/narrower concepts are more constrained.

**v3 implication.** When we compute `null_ratio` on contradictions that span multiple taxonomic levels, expect the *shallow-concept* failures to generate larger null excursions than the *deep-concept* failures, because shallow concepts have larger ℏ_s budgets to violate. Worth stratifying the 2×2 experiment by taxonomic depth if we ever revisit.

## 8. Computational framework — K-FAC for transformers
(`from-error-to-essence` §2.5, Appendix A)

Practical Fisher computation on large models:
```
I(θ) ≈ I_KFAC(θ) = block-diag(I_attn, I_ffn, I_embed)
```
Layer-wise K-FAC is tractable on billion-parameter transformers. Fisher regularizer loss: `L_enhanced = L_task + λ_FI · FisherRegularizer(I(θ))`.

**v3 implication.** Our `pri_v2_diag` / `topk32` / `lowrank32` variants are all diagonal / low-rank approximations of the same underlying K-FAC idea. That connection should be made explicit in the v3 paper's methods section — our FIM pullback approximations are SUP-compatible by construction.

## 9. What's *not* load-bearing for v3 (skip these for now)
- PGN architecture details + Byzantine fault tolerance applications — different domain (distributed training).
- AGI roadmap claims and "Fisher-inspired layer design" prescriptions — out of scope for v3 empirical paper.
- Specific `κ_dim`, `κ_curv`, `κ_info`, `κ ≈ 0.024` calibration — v3 measures `null_ratio` directly, no constants needed for primary results.
- Biology/consciousness extensions.
- PGN "Guardian" / "Meta-Guardian" infrastructure.

## 10. Citation hygiene for the v3 paper
The v3 paper should cite SUP as **theoretical provenance**, specifically:
- §2.1 → cite for the depth-profile prior (E21).
- §2.2 → cite for the spectrum-decay hypothesis (E20). **This is the strongest citation — exact quantitative band.**
- §2.3 → cite for the bounded-imprecision interpretation of `null_ratio`.
- §2.4 → cite for the orbital framing in the discussion.
- §2.5 → cite when discussing cross-architecture variance and Qwen's low-rank preference.
- §3 → cite for `P_fail` sigmoid calibration (v4, not v3).
- §4 → cite for MDL-ℏ as sanity-check baseline.
- §8 → cite for K-FAC connection to our FIM variants.

Pick canonical versions for the bibliography:
- `from-error-to-essence` — most rigorous Fisher derivation; clearest spectral predictions.
- `fisher-enhanced-v16` — fullest theoretical synthesis (Semantic Failure Law, rate-distortion, MDL formulation, tightness analysis).
- `why-imprecision-v2` — primary SUP statement with empirical PGN + layer evidence.
- `taxonomy-distance-v4` — layer-specificity result + per-model table.
- `cognitive-speciation-v2` — cross-arch framing + species discovery.

Skip earlier versions (`v0`, `v1`, `v1.5`, `v9.1`, `v2` of taxonomy) — superseded.

## 11. Sharpest single sentences to remember
> Contradiction commitment forces the model to discharge action when no semantically-coherent answer exists; SUP predicts the discharge goes into the null space. v3 measures the discharge.

> `ℏ_s ≥ 1` is not a modeling choice — it is necessary for Cramér-Rao consistency. Falling below it means the estimator is broken.

> Final-layer failures (5.9%) are not incidental: they are Fisher-spectrum pathologies (`λ_max/λ_mean > 10⁶`). Middle layers sit in the SUP-predicted band `[10², 10⁴]`.
