# Paper: Predictive Rupture as a Signal for Hallucination Detection in Large Language Models

Author: Michael Seo R. Kitti (msrkittty@proton.me)
Date: 2026-01-22 (earlier than `prediction-rupture-at-commitment`)
File: `raw/papers/furnace/2026-predictive-rupture-hallucination-detection.pdf`

## Timeline placement
**This is the bridge paper**, not the post-split successor I originally cataloged. Timeline:
1. `2026-detecting-confident-hallucinations-semantic-uncertainty-predictive-rupture.pdf` — earliest (pre-split).
2. **`2026-predictive-rupture-hallucination-detection.pdf` (this one, Jan 22 2026)** — still compares PRI to ℏs (SUP) as a baseline but frames PRI as clearly superior. SUP is factored out by being demoted to "underperforming baseline."
3. `2026-hallucinations-rupture-at-commitment.pdf` (Mar 17 2026) — cleanly post-split: ℏs not mentioned at all.

**Correction to vault:** my earlier `wiki/papers/furnace.md` had this paper as "post-split, PRI-only successor." Wrong. It's the *transitional* paper. Fixed in that index now.

## One-line thesis
Hallucinations are better characterized as *predictive ruptures* — abrupt internal representational shifts — than as states of elevated epistemic uncertainty. PRI beats ℏs (Semantic Uncertainty) because confident hallucinations live in *low-ℏs* regimes that uncertainty-based detectors systematically miss.

## Key Claims
1. **Confident hallucinations exist in low-ℏs regimes.** ℏs (the SUP scalar, √(Δμ · Δσ)) systematically under-estimates hallucination risk when the model is confidently wrong.
2. **PRI is dynamic, ℏs is static.** ℏs measures representational dispersion at a position; PRI measures instability across time (token commitment).
3. **PRI and ℏs are weakly-to-moderately anti-correlated** — they capture *complementary* failure modes, not redundant signals.
4. **Combined (ℏs, PRI) quadrant analysis** boosts detection: the both-signals-elevated quadrant has ~59% hallucination rate, exceeding base rate and any single-signal rule.

## PRI Formula (v1, same as later paper)
```
PRI_t = S_t · (1 + α · Δh_t)
Δh_t = 1 − cos(ĥ_{t-1}^L, ĥ_t^L)     (final-layer, unit-normalized)
```
Sequence-level aggregation: **top-k mean (k=5)** over generation — different from the later paper, which uses step-1 only. This aggregation choice likely explains part of the AUROC difference (0.60–0.67 here vs 0.998 in the later paper).

## ℏs Definition (as used here, for reference)
```
ℏs = sqrt(Δμ · Δσ)
```
where Δμ = semantic precision (output-distribution concentration) and Δσ = semantic flexibility (cross-layer representational dispersion). Low ℏs = sharp, internally consistent; high ℏs = diffuse or disagreeing.

## Experimental Setup
- Benchmark: **HaluEval** (train/test pre-split, no leakage).
- Models: Llama 3.2 3B Instruct 4-bit (primary); Qwen 2.5 7B and Phi-3 Mini (cross-model calibration).
- Greedy decoding (T=0), 20 tokens max per generation.
- Calibration: thresholds tuned for precision at recall ≥ 0.9; logistic regression for joint (ℏs, PRI) model with 5-fold CV.
- Validation: strict hold-out; no post-hoc tuning.

## Reported Results
- PRI AUROC ≈ 0.60–0.67 on Llama 3B (depending on sample size).
- ℏs AUROC ≈ 0.53 (near chance).
- At calibrated threshold: PRI ≈ 56% precision at 83% recall.
- Joint quadrant: both-elevated region has ~59% hallucination rate.

## Divergence from the Synthetic-Logic Pipeline
This paper uses **HaluEval** (naturalistic) and **top-k(5) aggregation**.
The later paper and `PRI_at_commitment` pipeline use **synthetic 2×2 contradictions** and **step-1-only**.
They are **different benchmarks answering different questions**:
- HaluEval: does PRI work on naturalistic hallucinations? → Yes, modest AUROC ≈ 0.6.
- Synthetic 2×2: does rupture localize to commitment? → Yes, AUROC ≈ 0.99 (or ≈ 0.77 per parquet — see AUROC discrepancy in the other paper note).

This reconciles most of the AUROC gap between the two papers — but *not* the internal gap between the synthetic-logic paper and its own parquet.

## Ingest Notes
- The ℏs-as-complementary-signal finding is the most Furnace-interesting result here: ℏs and PRI are orthogonal, so quadrant analysis beats either alone. This is reusable as a framing device even post-split.
- Worth noting: this paper's PRI numbers on Llama 3B HaluEval (AUROC 0.6–0.67) align much better with the parquet's `pri_v1_cosine` numbers (0.62 on Llama synthetic) than with the later paper's 0.998. May be relevant to the AUROC discrepancy investigation.
