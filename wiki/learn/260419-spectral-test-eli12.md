# 📐 SUP Spectral-Band Test, ELI12 (historical)

**Rigorous:** [results/sup-spectral-band](../results/sup-spectral-band.md) · **Code:** `PRI_at_commitment/scripts/sup_spectral_band.py`

> **Superseded.** SUP's `[10², 10⁴]` band doesn't transfer to decoders. The confound it exposed (entropy collapse) shaped null_ratio + Option A. Kept as a short record.

## 🎯 What we checked

SUP claim: `λ_max / λ_mean` on top-256 weighted `W_u` rows should sit **100×–10,000× at a shared depth** across models. We ran it at commitment, every layer, 16 puzzles × 3 models.

## 😬 What we got

| Chef | Peak ratio | Peak depth |
|---|---|---|
| 🦙 Llama | 30×–100× | very first layer |
| 🌬️ Mistral | 18×–60× | super early |
| 🐉 Qwen | 78×–250× | near the end |

No agreement on magnitude or depth. Theory busted. 📉

## 🚨 The confound

Qwen's "250×" wasn't lopsidedness — by that layer Qwen was ~97% decided. Entropy collapse *automatically* makes the spectrum look spiky. The test mixed **how sure the model already is** with **how shaped `W_u` is**. Can't untangle them from one number. ✂️

## 🎁 What the failure bought

1. ✅ SUP numbers don't transfer to decoders — encoder-calibrated.
2. ✅ Per-arch depth fingerprints are real; no universal "magic layer."
3. ✅ Future metrics must be **entropy-invariant** → null_ratio is normalized by ‖Δh‖.
4. ✅ Use final-answer distribution (honest), not per-layer peeks (misleading) → Option A uses the commitment-layer `p_t` as a single fixed subspace. 🏖️→🪨
