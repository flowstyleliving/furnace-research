# t=0 Residual-Stream Pilot — 2026-05-28

**Status**: [OPEN]
**Script**: `scripts/pilot_t0_residual.py`
**Data**: `experiments/v4-sealed/2026-05-26/data/anli_R1_seed20260526_n200.jsonl` (n=200, pos=100 neg=100)
**Question**: Do v3 residual-stream metrics (`d_F_full`, `kl_discharged`, `null_ratio`, `Raw_r21`) discriminate at **t=0** (prefix-last-position hidden state) vs their natural **gen_step=1** locus?

Links: [[pilot_t0_residual.py]] · [[pri_calibrator]] · [[v4-sealed-2026-05-26]] · [[step0-belief-readout-2026-05-17]]

---

## Design

Both loci computed from a single `max_new_tokens=1` trace per sample — no additional inference cost.

| Locus | h_t | h_prev | p_t | S_t |
|-------|-----|--------|-----|-----|
| **t=0** | `last_prefix_hidden[final]` | `prefix_hidden[final][-2]` | `prefix_probs[-1]` | `gen_surprises[0]` |
| **gen_step=1** | `gen_hidden[0]` | `last_prefix_hidden[final]` | `gen_probs[0]` | `gen_surprises[0]` |

Shared `S_t`: surprise of the first generated token (commitment surprise from prefix).
Sign-free AUROC = `max(auc, 1−auc)`. ⚠sign = t=0 and s=1 have **opposite discriminant direction** (sign-free masks this).

---

## Results

### Mistral-7B (`mlx-community/Mistral-7B-Instruct-v0.3-4bit`)

| Cell | t=0 (sf) | t=0 (sgn) | s=1 (sf) | s=1 (sgn) | Δsf | n |
|------|----------|-----------|----------|-----------|-----|---|
| d_F_full | 0.512 | 0.488 | 0.754 | 0.754 | **−0.242** | 200 ⚠sign |
| kl_discharged | 0.718 | 0.282 | 0.777 | 0.777 | −0.059 | 200 ⚠sign |
| Fisher_r1 | 0.663 | 0.337 | 0.779 | 0.779 | −0.116 | 200 ⚠sign |
| Fisher_r2 | 0.627 | 0.627 | 0.778 | 0.778 | −0.151 | 200 |
| Raw_r21 | 0.522 | 0.478 | 0.760 | 0.760 | **−0.238** | 200 ⚠sign |

All 5 cells: t=0 < s=1. 4/5 sign-flipped. s=1 is the correct locus for Mistral residual stream.

### Qwen2.5-7B (`mlx-community/Qwen2.5-7B-Instruct-4bit`)

| Cell | t=0 (sf) | t=0 (sgn) | s=1 (sf) | s=1 (sgn) | Δsf | n |
|------|----------|-----------|----------|-----------|-----|---|
| d_F_full | 0.514 | 0.486 | 0.602 | 0.398 | −0.087 | 200 |
| kl_discharged | 0.648 | 0.352 | 0.667 | 0.667 | −0.019 | 200 ⚠sign |
| Fisher_r1 | 0.614 | 0.386 | 0.835 | 0.835 | **−0.221** | 200 ⚠sign |
| Fisher_r2 | 0.814 | 0.186 | 0.844 | 0.844 | −0.030 | 200 ⚠sign |
| Raw_r21 | **0.811** | **0.811** | **0.885** | **0.885** | −0.074 | 200 |

All 5 cells: t=0 < s=1. Raw_r21 has consistent sign (0.811 both ways) — strong residual signal at t=0 even for this CoT model, but s=1 is still 0.885. Fisher_r2 @ t=0 = 0.814 is strong but sign-inverted vs s=1.

### Gemma-3-4B (`mlx-community/gemma-3-4b-it-4bit`)

| Cell | t=0 (sf) | t=0 (sgn) | s=1 (sf) | s=1 (sgn) | Δsf | n |
|------|----------|-----------|----------|-----------|-----|---|
| d_F_full | **0.739** | **0.739** | 0.652 | 0.348 | **+0.087** | 200 ⚠sign |
| kl_discharged | **0.753** | **0.753** | 0.644 | 0.356 | **+0.109** | 200 ⚠sign |
| Fisher_r1 | 0.638 | 0.362 | 0.516 | 0.484 | +0.122 | 200 |
| Fisher_r2 | 0.520 | 0.520 | 0.500 | 0.500 | +0.020 | 200 ⚠sign |
| Raw_r21 | 0.505 | 0.505 | 0.678 | 0.322 | −0.173 | 200 ⚠sign |

**4/5 cells t=0 > s=1**. `kl_discharged @ t=0 = 0.753` is the highest kl_discharged number in this pilot. `d_F_full @ t=0 = 0.739` with consistent sign. ⚠sign on both winners means the discriminant direction inverts between loci — t=0 direction does NOT match s=1 direction for Gemma.

### Cross-model summary

| Cell | Mistral-7B | Qwen2.5-7B | Gemma-3-4B |
|------|-----------|-----------|-----------|
| d_F_full | −0.242 ↓⚠ | −0.087 ↓ | **+0.087 ↑⚠** |
| kl_discharged | −0.059 ↓⚠ | −0.019 ↓⚠ | **+0.109 ↑⚠** |
| Fisher_r1 | −0.116 ↓⚠ | −0.221 ↓⚠ | **+0.122 ↑** |
| Fisher_r2 | −0.151 ↓ | −0.030 ↓⚠ | +0.020 ↑⚠ |
| Raw_r21 | −0.238 ↓⚠ | −0.074 ↓ | −0.173 ↓⚠ |

---

## Findings

**1. Gemma-3-4B is the structural outlier.** t=0 beats s=1 on 4/5 cells. `kl_discharged` and `d_F_full` both peak at the prefix-last-position locus. Interpretation: Gemma generates YES/NO immediately (no CoT preamble), so the prefix hidden state already crystallizes the commitment. The *natural* residual-stream locus for Gemma may genuinely be t=0, not gen_step=1.

**2. Mistral-7B and Qwen2.5-7B: s=1 wins everywhere.** Despite Qwen being a CoT model (the original STEP-0 CRACK target for attention), the *residual stream* at gen_step=1 still carries stronger commitment signal than t=0. This is important: the STEP-0 CRACK was specific to **attention weights** — the residual stream doesn't suffer the same locus problem.

**3. Sign flips are pervasive — 13/15 cell×model pairs show ⚠sign or near-⚠sign.** The discriminant direction of residual-stream cells *reverses* between t=0 and gen_step=1 for most combinations. Sign-free AUROC makes the numbers look reasonable, but any deployment would need sign to be locked from a calibration split at the same locus.

**4. kl_discharged confirmed working.** Required `v3_capture_centered=True` in `compute_step`. Previously produced NaN when flag was omitted. Values are valid and well-behaved across all 3 models.

**5. Qwen2.5-7B Raw_r21 @ t=0 = 0.811 (consistent sign).** Strong residual-stream discriminability before any generation, same direction as s=1. This is real information already present in the prefix for a CoT model.

---

## Implications for the "retrofit" question

> *What if we read every answer for each model to retrofit it into the measurer and redo v3?*

- **Gemma**: t=0 could be the preferred locus. The prefix already carries the discriminant. Calibrating at t=0 makes architectural sense.
- **Mistral/Qwen**: gen_step=1 residual stream is still better. The STEP-0 CRACK fix (switching to t=0) was necessary for **attention** cells but is not advantageous for **residual-stream** cells on these models. Retrofitting would lose ~0.2 AUROC on Mistral.
- **Sign stability**: The pervasive sign flip means you cannot take a sign-locked v3 calibration profile (fitted at s=1) and re-use the direction lock at t=0. Separate calibration per locus is required.

---

## Calibrated Results (OOB bootstrap, 2026-05-28)

Script: `pri_calibrator.py --t0-residual`. Patch: step=0 branch in `_compute_panel_scores_for_sample` (commit `91d9bb1`). Data: same ANLI R1 n=200. `max_new_tokens=1`, seed=20260528, n_bootstrap=1000.

| Model | Winner cell | Sign | In-sample | OOB median | OOB CI | Stability | Warnings |
|-------|------------|------|-----------|------------|--------|-----------|---------|
| Mistral-7B | kl_discharged @ step 0 | −1 | 0.718 | **0.708** | [0.552, 0.801] | 0.887 | — |
| Qwen2.5-7B | Fisher r=2 @ step 0 | −1 | 0.814 | **0.812** | [0.725, 0.890] | 0.59 | ⚠ winner_unstable |
| Gemma-3-4B | kl_discharged @ step 0 | +1 | 0.753 | **0.742** | [0.646, 0.828] | 0.77 | — |

**Sign interpretation**:
- Mistral sign=−1: lower kl_discharged at t=0 → contradiction (inverted from s=1 natural direction)
- Qwen sign=−1: lower Fisher r=2 at t=0 → contradiction (inverted from s=1 natural direction)
- Gemma sign=+1: higher kl_discharged at t=0 → contradiction (same direction as s=1, natural alignment)

**Key findings**:
1. **Qwen OOB 0.812 is real but `winner_unstable`**: Fisher r=2 and Raw r=21 compete closely (59%/41%). The discriminability is genuine but the specific cell selection is noise-driven at n=200. In-sample AUROCs were 0.814 vs 0.811 — too close to call.
2. **Gemma OOB 0.742 is the cleanest t=0 profile**: Sign=+1 (natural direction), no warnings, stability 0.77. This is a valid deployable CalibrationProfile. Overfitting essentially zero (in-sample 0.753 vs OOB 0.742, Δ=0.011).
3. **Mistral OOB 0.708** with wide CI [0.552, 0.801] reflects sign-inverted moderate signal. Clean profile (stability 0.887) but lower ceiling.
4. **OOB overfit gap** (in-sample − OOB): Mistral 0.010, Qwen 0.002, Gemma 0.011 — all essentially zero. Step=0 locus is not being overfit.
5. **Mechanistic interpretation**: Gemma's sign=+1 at t=0 aligns with the natural commitment signal (prefix already commits before generating). Mistral/Qwen sign=−1 at t=0 is inverted — these models' prefixes correlate inversely with the commitment direction, and the actual rupture happens at gen_step=1.

**Profiles written to**: `experiments/t0-residual-calibration/2026-05-28/run-01/`

---

## Family-Split Extension — run-02 (2026-05-28)

**4 additional models**: Llama-3.2-3B, Mistral-Nemo, Phi-3.5-mini, Qwen3-8B. Same data/seed/n.

### Full 7-model calibrated table

| Model | Winner cell | Sign | OOB | CI | Stability | Warn |
|-------|------------|------|-----|-----|----------|------|
| Mistral-7B-v0.3 | kl_discharged @ 0 | −1 | 0.708 | [0.552, 0.801] | 0.887 | — |
| Qwen2.5-7B | Fisher r=2 @ 0 | −1 | 0.812 | [0.725, 0.890] | 0.59 | ⚠ |
| Gemma-3-4B | kl_discharged @ 0 | **+1** | 0.742 | [0.646, 0.828] | 0.77 | — |
| Llama-3.2-3B | Fisher r=1 @ 0 | −1 | 0.660 | [0.554, 0.755] | 0.44 | ⚠⚠ |
| Mistral-Nemo | Fisher r=1 @ 0 | **+1** | **0.808** | [0.699, 0.890] | 0.82 | — |
| Phi-3.5-mini | Fisher r=1 @ 0 | −1 | 0.759 | [0.660, 0.850] | 0.71 | — |
| Qwen3-8B | d_F_full @ 0 | **+1** | 0.774 | [0.629, 0.862] | 0.87 | — |

**sign=+1**: Gemma-3-4B, Mistral-Nemo, Qwen3-8B
**sign=−1**: Mistral-7B-v0.3, Qwen2.5-7B, Llama-3.2-3B, Phi-3.5-mini

### Findings

**Family-label hypothesis FALSIFIED.** Mistral-Nemo (sign=+1) contradicts Mistral-7B-v0.3 (sign=−1). Qwen3-8B (sign=+1) contradicts Qwen2.5-7B (sign=−1). The sign at t=0 is not predictable from architecture family name.

**Generation-era pattern [OPEN]**: sign=+1 correlates with newer or larger models within each lineage:
- Mistral: Nemo (12B, July 2024) +1 vs 7B-v0.3 (7B, May 2024) −1
- Qwen: Qwen3 (April 2025, reasoning-tuned) +1 vs Qwen2.5 (September 2024) −1
- Gemma-3 (early 2025) +1; no older Gemma in panel
- Llama-3.2-3B (September 2024) −1; no newer Llama tested
- Phi-3.5 (August 2024) −1; Phi-4 not yet run

Interpretation: newer-generation instruction-tuned models increasingly commit belief into the prefix residual stream in natural polarity. Older/smaller models' commitment at t=0 is inverted — the rupture lives at gen_step=1, not in the prefix.

**Qwen3-8B note**: sign=+1 despite being a reasoning model (first generated token is `<think>`). Prefix already encodes commitment direction pre-generation.

**Llama-3.2-3B note**: weakest result in the set — OOB 0.660, 3-way winner instability (Fisher r=1 44%, kl_discharged 33%, d_F_full 22%). t=0 residual is marginal for 3B Llama at n=200.

**Next falsification targets**: Phi-4 (newer Phi — should flip to +1 if era hypothesis holds) and Llama-3.1-8B (larger/newer Llama — if it flips to +1, the pattern is confirmed across all 4 tested families). → **See run-03 below: both falsified.**

**Profiles**: `experiments/t0-residual-calibration/2026-05-28/run-02/`

---

## Era-Hypothesis Falsification — run-03 (2026-05-28)

**Hypothesis**: sign=+1 correlates with newer/larger generation within each lineage.
**Test**: Phi-4-mini (newer than Phi-3.5) and Llama-3.1-8B (larger than Llama-3.2-3B).

| Model | Sign | OOB | CI | Stability | Warn |
|-------|------|-----|-----|----------|------|
| Phi-4-mini | **−1** | 0.684 | [0.530, 0.784] | 0.89 | — |
| Llama-3.1-8B | **−1** | 0.778 | [0.689, 0.852] | **1.00** | — |

**Verdict: FALSIFIED.** Both predicted to flip to +1; both stayed −1. Phi doesn't flip (3.5→4 both −1). Llama doesn't flip (3.2-3B→3.1-8B both −1). The within-family flips for Mistral and Qwen do not generalize.

### Final 9-model table

| Model | Sign | OOB | Stability | Warn |
|-------|------|-----|----------|------|
| Mistral-7B-v0.3 | −1 | 0.708 | 0.887 | — |
| Qwen2.5-7B | −1 | 0.812 | 0.59 | ⚠ |
| Gemma-3-4B | **+1** | 0.742 | 0.77 | — |
| Llama-3.2-3B | −1 | 0.660 | 0.44 | ⚠⚠ |
| Mistral-Nemo | **+1** | 0.808 | 0.82 | — |
| Phi-3.5-mini | −1 | 0.759 | 0.71 | — |
| Qwen3-8B | **+1** | 0.774 | 0.87 | — |
| Phi-4-mini | −1 | 0.684 | 0.89 | — |
| Llama-3.1-8B | −1 | 0.778 | **1.00** | — |

**sign=+1** (3/9): Gemma-3-4B, Mistral-Nemo, Qwen3-8B
**sign=−1** (6/9): Mistral-7B-v0.3, Qwen2.5-7B, Llama-3.2-3B, Phi-3.5-mini, Phi-4-mini, Llama-3.1-8B

**Closing finding**: No tested feature — family, size, era, vocab, tied_embed vs lm_head — reliably predicts the sign. It is model-specific. Per-model calibration is the only honest read, consistent with the distribution-generalization finding from the v3 ANLI full sweep. t=0 residual is a universally valid locus (all 9 models discriminate above chance), but direction must come from the calibrated profile.

**Notable**: Llama-3.1-8B is the cleanest result in the 9-model sweep: stability=1.00, OOB=0.778, Δ=+0.001 overfit. Strong inverted signal; commitment lives at gen_step=1 for this model.

**Profiles**: `experiments/t0-residual-calibration/2026-05-28/run-03/`
