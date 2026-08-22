# Δσ_onaxis 7-model panel (2026-05-15)

_Run: 2026-05-15, run-01. Panel: 7 models × ranks {2, 4, 8, 16, 32}, n=200 calibration samples each._

> **🟡 Verdict [OPEN, leaning negative]:** the SUP-flavored bivariate (null_ratio · Δσ_onaxis) composite **does not robustly beat null_ratio alone** across the 7-model panel. Δσ_onaxis is a genuinely new geometric channel — and it surprises on two reasoning-tuned Phi variants where it *alone* beats null — but its sign correlation with null_ratio swings from −0.83 (Qwen 2.5) to +0.50 (Mistral) across families, killing the universal-composite story.
>
> 1. **No model has bivariate > null by more than +0.014 AUROC.** The best lift is Mistral 7B at r=16 (bivar 0.7411 vs null 0.7271).
> 2. **Δσ_onaxis alone wins on Phi-3.5-mini (0.7386 @ r=2, sign −) and Phi-4-mini (0.7225 @ r=4, sign +)**, beating their null_ratio by 0.15 and 0.05 respectively. Phi-3.5's anti-predictive sign is consistent with its broader gate-failure phenomenology; Phi-4's positive sign is a clean new datapoint.
> 3. **Sign of null_ratio itself is family-dependent**: canonical (+) on Mistral and Qwen 2.5; flipped (−) on Llama 3B (r=4,8,16), Phi family, Qwen 3, Gemma 3-4B at most ranks. Already known from v3.1/v3.2; this run reconfirms.
> 4. **Δσ_onaxis sign also family-dependent**: '+' on Llama, Mistral high-r, Phi-4, Qwen 3, Gemma; '−' on Phi-3.5 (all ranks) and Qwen 2.5 (all ranks).

## Setup

| Field | Value |
|---|---|
| Date | 2026-05-15 (08:51 → 11:59, \~3h wall on M4) |
| Output | `experiments/delta-sigma-onaxis/2026-05-15/run-01/` |
| n per model | 200 (calibration set, gen_step=1, layer=final) |
| Ranks | 2, 4, 8, 16, 32 |
| Models | Llama 3.2-3B, Mistral 7B v0.3, Phi-3.5-mini, Phi-4-mini, Qwen 2.5-7B, Qwen 3-8B, Gemma 3-4B |
| Script | [`scripts/diagnose_delta_sigma_onaxis.py`](../../PRI_at_commitment/scripts/diagnose_delta_sigma_onaxis.py) (panel runner: `scripts/run_delta_sigma_panel.sh`) |

## Quantity definitions

For each calibration sample at `gen_step=1`, compute the standard sealed-v3 quantities (`dh_post`, `p_t`, SVD of `√p_t·W_s` on top-`support` rows), then:

- **null_ratio_post_rank{r}** — fraction of `‖dh_post‖²` OFF the top-r Fisher axes (identical to `PRIComputer.null_ratio_and_energy`).
- **delta_sigma_onaxis_rank{r}** — Shannon entropy of the per-axis energy distribution INSIDE the top-r axes: `e_i = (V_i · dh_post)²`, `q_i = e_i / Σ e_j`, `H_r = −Σ q_i log(q_i + ε)`. Normalized to `[0,1]` by `H_r / log(r)` for cross-rank comparison.
- **bivariate (null · Δσ_n)** — the SUP-motivated composite, multiplicative.
- **fisher_energy_rank{r}** — `Σ_{i≤r} σ_i² / Σ_i σ_i²` (sanity check, identical to sealed v3).

**Theoretical motivation:** in the SUP frame `ℏ = √(Δμ · Δσ)`, the on-axis concentration `Δμ ~ (1 − null_ratio)` and on-axis flexibility/dispersion `Δσ ~ H_r` should be orthogonal indicators. Predicted signatures:
- truthful — low null + low Δσ_onaxis (one dominant axis)
- uncertain — low null + high Δσ_onaxis (spread)
- contradiction — high null + high Δσ_onaxis (off-axis + thrashing)
- confident hallucination — low null + low Δσ_onaxis (sharp but wrong axis)

The panel cannot separate truthful from confident-hallucination (no label for the latter), but it can test whether Δσ_onaxis carries any contradiction-discriminative signal beyond null_ratio.

## Per-model AUROC tables

AUROC sign: '+' means HIGHER value predicts contradiction; '−' is flipped.

### 🦙 Llama 3.2-3B-Instruct-4bit

| rank | AUROC null | AUROC Δσ_n | AUROC null·Δσ | corr(null, Δσ_n) | fisher_energy |
|---:|---|---|---|---|---|
| 2  | 0.6168 (+) | 0.6003 (+) | 0.6006 (+) | +0.4806 | 0.6316 |
| 4  | 0.5475 (−) | 0.5984 (+) | 0.5980 (+) | −0.0825 | 0.7902 |
| 8  | 0.5065 (−) | 0.5376 (+) | 0.5361 (+) | +0.1604 | 0.9152 |
| 16 | 0.5805 (−) | 0.5771 (+) | 0.5697 (+) | +0.1448 | 0.9614 |
| 32 | 0.6176 (−) | 0.5951 (+) | 0.5802 (+) | −0.0644 | 0.9806 |

**Best:** null at r=32 = 0.6176 (sign −). Δσ_n adds nothing — every rank within 0.04 of null.

### 🌬️ Mistral-7B-Instruct-v0.3-4bit

| rank | AUROC null | AUROC Δσ_n | AUROC null·Δσ | corr(null, Δσ_n) | fisher_energy |
|---:|---|---|---|---|---|
| 2  | 0.7600 (+) | 0.5314 (−) | 0.5232 (−) | −0.3501 | 0.9240 |
| 4  | 0.7572 (+) | 0.6839 (+) | 0.6901 (+) | +0.2989 | 0.9845 |
| 8  | 0.7564 (+) | 0.7045 (+) | 0.7135 (+) | +0.4072 | 0.9981 |
| 16 | 0.7271 (+) | 0.7313 (+) | **0.7411 (+)** | +0.5002 | 0.9992 |
| 32 | 0.7385 (+) | 0.6102 (+) | 0.6508 (+) | +0.2020 | 0.9997 |

**Best:** null at r=2 = 0.7600 (+). **Bivariate r=16 = 0.7411 modestly exceeds null at r=16 (+0.014)** — only clean composite-lift in panel, but doesn't beat best-rank null. corr(null, Δσ_n) climbs monotonically with rank from −0.35 → +0.50.

### 🪼 Phi-3.5-mini-instruct-4bit

| rank | AUROC null | AUROC Δσ_n | AUROC null·Δσ | corr(null, Δσ_n) | fisher_energy |
|---:|---|---|---|---|---|
| 2  | 0.5323 (+) | **0.7386 (−)** | 0.7380 (−) | −0.3307 | 0.9725 |
| 4  | 0.5796 (−) | 0.5644 (−) | 0.5685 (−) | −0.2069 | 0.9975 |
| 8  | 0.5854 (−) | 0.5782 (−) | 0.5788 (−) | +0.1602 | 0.9994 |
| 16 | 0.5037 (−) | 0.6065 (−) | 0.6079 (−) | −0.5902 | 0.9997 |
| 32 | 0.5229 (−) | 0.5647 (−) | 0.5677 (−) | −0.6587 | 0.9998 |

**Surprise — Δσ_n alone at r=2 = 0.7386 (sign −), +0.21 AUROC over best null.** Anti-predictive sign suggests Phi-3.5 contradictions concentrate INTO a single on-axis direction (low entropy ⇒ contradiction). Consistent with Phi-3.5's prior gate-failure / reasoning-tag phenomenology.

### 🔭 Phi-4-mini-instruct-4bit

| rank | AUROC null | AUROC Δσ_n | AUROC null·Δσ | corr(null, Δσ_n) | fisher_energy |
|---:|---|---|---|---|---|
| 2  | 0.6719 (−) | 0.5730 (−) | 0.5742 (−) | −0.0837 | 0.9526 |
| 4  | 0.5807 (−) | **0.7225 (+)** | 0.7226 (+) | −0.2399 | 0.9842 |
| 8  | 0.5617 (−) | 0.5569 (+) | 0.5570 (+) | +0.3426 | 0.9934 |
| 16 | 0.5643 (−) | 0.5935 (+) | 0.5935 (+) | −0.0530 | 0.9963 |
| 32 | 0.5457 (−) | 0.5777 (+) | 0.5765 (+) | −0.0604 | 0.9979 |

**Δσ_n alone at r=4 = 0.7225 (+), +0.05 over best null.** Canonical sign (higher Δσ_n ⇒ contradiction) — opposite of Phi-3.5. The two reasoning-tuned Phi variants disagree on Δσ-sign even when both gate-fail under the canonical null_ratio reading.

### 🐲 Qwen2.5-7B-Instruct-4bit

| rank | AUROC null | AUROC Δσ_n | AUROC null·Δσ | corr(null, Δσ_n) | fisher_energy |
|---:|---|---|---|---|---|
| 2  | 0.7918 (+) | 0.6442 (−) | 0.6418 (−) | −0.7126 | 0.9428 |
| 4  | 0.8024 (+) | 0.7368 (−) | 0.7290 (−) | −0.8256 | 0.9910 |
| 8  | 0.7745 (+) | 0.6836 (−) | 0.6743 (−) | −0.8149 | 0.9962 |
| 16 | 0.8042 (+) | 0.6867 (−) | 0.6600 (−) | −0.7184 | 0.9983 |
| 32 | **0.8076 (+)** | 0.6536 (−) | 0.5843 (−) | −0.6263 | 0.9992 |

**Best:** null at r=32 = 0.8076 (+). Δσ_n is strongly **anti-correlated** with null (−0.83 peak) — the two channels encode opposite information on Qwen 2.5, and multiplying them DEGRADES the composite vs null alone (0.5843 vs 0.8076 at r=32). Bivariate composite is actively harmful here.

### 🐉 Qwen3-8B-4bit

| rank | AUROC null | AUROC Δσ_n | AUROC null·Δσ | corr(null, Δσ_n) | fisher_energy |
|---:|---|---|---|---|---|
| 2  | 0.5216 (−) | 0.5372 (−) | 0.5371 (−) | −0.6442 | 0.9848 |
| 4  | 0.6417 (−) | 0.6228 (+) | 0.6226 (+) | −0.3797 | 0.9976 |
| 8  | **0.6848 (−)** | 0.5587 (+) | 0.5545 (+) | −0.0796 | 0.9996 |
| 16 | 0.6533 (−) | 0.5821 (+) | 0.5782 (+) | −0.1458 | 0.9999 |
| 32 | 0.6397 (−) | 0.5018 (+) | 0.5114 (−) | +0.2549 | 1.0000 |

Weakest signal across the panel — consistent with Qwen 3's v3 main-run collapse on this analysis plane. null sign is "−" at every rank (anti-predictive in this Fisher basis; raw basis recovers from r=13 onward per [models/qwen-3-8b](../models/qwen-3-8b.md)).

### 💎 Gemma-3-4B-Instruct-4bit

| rank | AUROC null | AUROC Δσ_n | AUROC null·Δσ | corr(null, Δσ_n) | fisher_energy |
|---:|---|---|---|---|---|
| 2  | 0.5348 (+) | 0.5350 (−) | 0.5349 (−) | +0.1847 | 0.9921 |
| 4  | 0.6156 (−) | 0.5846 (+) | 0.5845 (+) | −0.1890 | 0.9991 |
| 8  | **0.6637 (−)** | 0.6053 (+) | 0.6045 (+) | −0.2103 | 0.9998 |
| 16 | 0.5585 (−) | 0.6574 (+) | 0.6562 (+) | −0.1865 | 1.0000 |
| 32 | 0.5616 (+) | 0.5649 (+) | 0.5664 (+) | +0.1194 | 1.0000 |

**Best:** null at r=8 = 0.6637 (−). Δσ_n at r=16 (0.6574) within 0.01 of best null; bivariate adds no lift. Sign of null flips between r=2 (+) and r=4 (−) — same flip phenomenology as the [Motif 2](v3.2-results.md) rank crossover already documented for Gemma.

## Cross-model summary table

| Model | Best null (rank, sign) | Best Δσ_n (rank, sign) | Best bivar (rank, sign) | Bivar > null? |
|---|---|---|---|---|
| Llama 3.2-3B | 0.6176 (32, −) | 0.6003 (2, +) | 0.6006 (2, +) | No |
| Mistral 7B  | 0.7600 (2, +)  | 0.7313 (16, +) | 0.7411 (16, +) | **+0.014 at r=16 only** |
| Phi-3.5-mini | 0.5854 (8, −) | **0.7386 (2, −)** | 0.7380 (2, −) | No (Δσ alone wins) |
| Phi-4-mini  | 0.6719 (2, −)  | **0.7225 (4, +)** | 0.7226 (4, +) | No (Δσ alone wins) |
| Qwen 2.5-7B | **0.8076 (32, +)** | 0.7368 (4, −) | 0.7290 (4, −) | No (bivar degrades) |
| Qwen 3-8B   | 0.6848 (8, −)  | 0.6228 (4, +)  | 0.6226 (4, +) | No |
| Gemma 3-4B  | 0.6637 (8, −)  | 0.6574 (16, +) | 0.6562 (16, +) | No |

## Cross-model takeaways

1. **Bivariate null·Δσ_n is not a robust universal signal.** Six of seven models show it ≤ best univariate; the one exception (Mistral r=16) is a +0.014 AUROC gain that doesn't survive across ranks.
2. **The two channels are not consistently orthogonal.** corr(null, Δσ_n) spans [−0.83, +0.50] across the panel; the SUP `ℏ = √(Δμ · Δσ)` predicted-orthogonality narrative does not hold cross-family.
3. **Δσ_onaxis IS a new informative channel — independently — on the Phi family.** Both Phi-3.5 (r=2, sign −, 0.7386) and Phi-4 (r=4, sign +, 0.7225) materially beat their null_ratio. The sign disagreement between the two is a fresh datapoint about reasoning-tuned models. Worth a deeper look: do reasoning-tuned models encode contradiction as on-axis collapse (Phi-3.5: low Δσ ⇒ contradiction) vs on-axis spread (Phi-4: high Δσ ⇒ contradiction)?
4. **Qwen 2.5 corr = −0.83**: null_ratio and Δσ_onaxis encode opposite information at the sealed-v3 analysis plane. Multiplying them is destructive on Qwen 2.5 — a clean falsification of the multiplicative-composite hypothesis on that model.
5. **fisher_energy ≥ 0.95 from r=4 onward on every model except Llama 3B.** The on-axis subspace is essentially saturated at r=4; further rank increases mostly redistribute energy already inside the on-axis cone. This is why Δσ_onaxis varies more across ranks than fisher_energy does.

## Implications

- **No promotion to v4-candidate.** The bivariate composite is gate-failed on 6/7 models and the v4-candidate ledger is already retired in favor of per-(model, deployment) calibration via [`pri_calibrator.py`](../../PRI_at_commitment/pri_calibrator.py).
- **Two follow-ups worth queuing**:
  1. **Phi-family Δσ_onaxis deep-dive** — recompute Δσ across all gen_steps (not just step 1) on Phi-3.5 and Phi-4, see if the sign opposition is plane-localized or persistent.
  2. **Δσ_onaxis as a calibrator panel cell** — adding `delta_sigma_onaxis_rank{r}` to the 8-cell calibrator panel would let `pri_calibrator.py` pick it as the winning cell on any per-(model, distribution) profile where it dominates, without us pre-committing to a universal claim.
- **Sealed v3.1/v3.2 verdicts unchanged.** This panel is descriptive, not a re-test of any sealed gate.

## Artifacts

- CSV: `experiments/delta-sigma-onaxis/2026-05-15/run-01/<model>_delta_sigma_onaxis.csv` (200 rows each, 22 columns: sample_idx, label, then null/Δσ/Δσ_norm/fisher_energy × 5 ranks)
- Logs: `experiments/delta-sigma-onaxis/2026-05-15/run-01/<model>_delta_sigma_onaxis.log` (per-model AUROC tables at the tail)
- Panel runner: `scripts/run_delta_sigma_panel.sh`
- Single-model script: `scripts/diagnose_delta_sigma_onaxis.py`

## Backlinks
- [results/v3.2-results](v3.2-results.md) — sealed v3.2 verdict and Motif catalog
- [models/phi-3.5-mini](../models/phi-3.5-mini.md) — Phi-3.5 raw-stable Motif 1
- [models/qwen-2.5-7b](../models/qwen-2.5-7b.md) — sealed E17b authority
- [research-candidates](research-candidates.md)ndidates.md) — retired ledger (this finding does not revive it)
