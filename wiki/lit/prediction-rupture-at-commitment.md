# Paper: Hallucinations Rupture at Commitment, Not at Encoding

Full title: *Hallucinations Rupture at Commitment, Not at Encoding: Predictive Rupture Index Localizes Contradiction-Induced Failure to the First Generated Token*

Author: Michael Seo R. Kitti (Independent Researcher)
Date: 2026-03-17
File: `raw/papers/furnace/furnace-2026-prediction-rupture-at-commitment.pdf`

## ⚠️ Headline numbers superseded (2026-04-14)
User confirmed the paper's AUROCs (0.998 / 0.994 / 0.980) and Hedges g (4.18 / 3.66 / 2.29) are **pre-audit artifacts**. Root cause: the first generated token had no real previous token, so Δh at step 0 was inflated. Post-fix parquet: v2-best AUROC 0.77 / 0.67 / 0.79 and g 0.96 / 0.58 / 1.38 — ordering also reverses, invalidating the "strain ∝ 1/capability" claim (#4 below). The qualitative claims (dual-phase dissociation, commitment-localization, outcome independence) are still supported by the parquet; the magnitudes and capability-scaling ordering are not.

## One-line thesis
Contradiction signal emerges at **generation commitment**, not during encoding — PRI spikes massively at the first generated token while encoding-phase signals show no differential response.

## Key Claims
1. **Dual-phase dissociation.** In the prefix (encoding) phase, no model-signal combination separated contradiction from control (all p ≥ 0.31; primary test). At the first generated token, PRI separated them with Hedges g ∈ [2.29, 4.18] and AUROC ∈ [0.980, 0.998].
2. **Commitment-localized.** Signal concentrates at step 1 and decays rapidly at steps 2–3.
3. **Outcome independence.** Both contradiction-correct and contradiction-incorrect samples show elevated PRI — the signal detects contradiction *presence*, not answer failure.
4. **Strain ∝ 1 / capability.** Larger / more capable models show *smaller* g (Llama 4.18 > Mistral 3.66 > Qwen 2.29), consistent with "more capable models absorb premises more completely and experience less strain at commitment."
5. **Static signals fail.** Cross-layer JSD (`Δσ_JSD`) and attention-contribution-ratio (`acr`) show no consistent generation-phase separation. Rupture is dynamic, not static.

## Theoretical Framing
- **Free Energy Principle (Friston 2010; Friston et al. 2017)** is the explicit theoretical inspiration. Prefix = perceptual inference; commitment = active inference. The "moment of action" is where FEP predicts maximal systemic strain.
- **SUP (ℏs)** is *not* mentioned in this paper — this is the post-split, PRI-only framing.

## PRI Formula (v1, as used in this paper)
```
PRI_t = S_t · (1 + α · Δh_t)
```
where `S_t = -log p(x_t | x_<t)` and `Δh_t = 1 − cos(h_t^(L), h_{t-1}^(L))` on final-layer normalized hidden states. v2 (FIM-pullback) is flagged as ongoing work.

## Experimental Setup
- Models: Llama 3.2 3B, Mistral 7B v0.3, Qwen 2.5 7B (all 4-bit MLX, greedy).
- Task: synthetic logic puzzles, 2×2 design (chain_length × contradiction), 200 samples/cell, **n=800 per model**.
- Behavioral gate: ≥80% control accuracy on 20-sample pilot before full run.
- Stats: 10,000 stratified permutations by chain length; Hedges g with 95% CI via fixed-effect meta-analysis; AUROC with no training or threshold tuning.

## ⚠️ Critical Discrepancy with `summary.parquet`
The paper reports AUROC **0.998 / 0.994 / 0.980** and Hedges g **4.18 / 3.66 / 2.29** for Llama / Mistral / Qwen. The parquet at `/Users/msrk/Documents/PRI_at_commitment/pri_v2_results/summary.parquet` reports **0.623 / 0.552 / 0.083** for `pri_v1_cosine` under the same documented config. The `PRI_V2_PRE_RUN_AUDIT_CHECKLIST.md` explicitly warns about CRITICAL token/hidden-state alignment bugs that "silently produce plausible but wrong results." See [claims](../claims.md) `[OPEN]` — the paper may reflect pre-audit numbers.

## Ingest Notes
- Hallucination-detection framing: outcome independence makes PRI a detector of **latent risk**, not realized failure — this is the safety-infrastructure angle.
- Inverse g-vs-capability claim is notable but based on three points; worth replicating across the v3 extended suite (Gemma 3-1B, Qwen3 8B, Phi-3.5-mini). gpt-oss-20B was candidate-of-record when these notes were written but was dropped 2026-04-14 (M4 too light under mlx-lm).
- Cost claim: "strictly cheaper than any method requiring multiple generations" — one cosine + one log-prob per token, no sampling / ensemble / extra forward pass.
