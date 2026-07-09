# Precision Ladder — Results, Wave 1 (Qwen2.5-7B, 2026-06-22)

**Status:** `[OPEN — both waves run 2026-06-22/23]`. Pre-registration: [[precision-ladder-prereg-2026-06-22]]. Backend `modal-torch`, n=200, all rungs **NON-byte-comparable to the sealed MLX plane**; standalone exploratory. Wave 1 = Qwen2.5-7B `{nf4,int8,bf16,fp32}`; Wave 2 = Qwen2.5-32B `{nf4,int8,bf16}` (§Wave 2 below).

> **Headline:** the panel's real diagnostic signals are **precision-invariant** (H3 falsified at the fixed-cell level). What the 4-bit noise destabilizes is *which cell the selector picks*, not *whether a signal exists*. `int8` (LLM.int8 outlier-decomposition) is a genuine outlier rung that degrades morphology more than nf4 or bf16. A few readout cells (e.g. `fisher_eff_rank`) carry mild quantization-correlated structure but are not load-bearing.

---

## Method correction (logged prominently, per the Bell-Burnell rule)

The live, turn-by-turn reads during the run ("nf4 at chance / bf16 recovers", "winner flips every rung", "bidirectional suppression") were **chasing the argmax winner and its OOB CI_lo** — and that lens is wrong for a cross-precision contrast. With ~28 competing cells, the bootstrap argmax is unstable, so the OOB-honest *winner* CI_lo collapses even when the underlying cell is fine. **The correct lens is each fixed cell's score across rungs.** All conclusions below are fixed-cell.

---

## Winner / selection summary (the unstable view)

| task | rung | OOB CI_lo | deployable | winner_stability | winner |
|------|------|-----------|------------|------------------|--------|
| anli | nf4 | 0.498 | ❌ | 0.50 | rd `neg_shadow_logvol_r1` |
| anli | int8 | 0.498 | ❌ | 0.89 | rd `neg_shadow_logvol_r1` |
| anli | bf16 | 0.589 | ✅ | 0.95 | rd `neg_shadow_logvol_r1` |
| anli | fp32 | 0.551 | ✅ | 0.51 | rd `neg_shadow_logvol_r1` |
| trivia | nf4 | 0.810 | ✅ | 0.53 | rd `fisher_eff_rank` |
| trivia | int8 | 0.535 | ✅ | 0.55 | att `last_minus_1_bos_mass` |
| trivia | bf16 | 0.670 | ✅ | 0.56 | att `mid_js_kv_groups` |
| trivia | fp32 | 0.657 | ✅ | 0.66 | att `mid_js_kv_groups` |

Note: anli keeps the *same* winner cell at all rungs (the OOB CI_lo move is pure selection-stability: 0.50→0.95). Triviaqa's winner jumps around — but the two **full-precision rungs agree** (`mid_js_kv_groups`), while the quantized rungs each pick something else.

## Fixed-cell signed AUROC (the truthful view)

0.5 = chance; distance from 0.5 = strength; a cell that stays one side of 0.5 is direction-stable.

**anli_r1**
| cell | nf4 | int8 | bf16 | fp32 | read |
|------|-----|------|------|------|------|
| rd `neg_shadow_logvol_r1` | 0.682 | 0.719 | 0.746 | 0.710 | **robust** |
| att `last_minus_1_bos_mass` | 0.673 | 0.644 | 0.660 | 0.690 | **robust** |

**triviaqa_paired**
| cell | nf4 | int8 | bf16 | fp32 | read |
|------|-----|------|------|------|------|
| att `mid_js_kv_groups` | 0.800 | 0.680 | 0.803 | 0.810 | **robust** (int8 dip) |
| rd `surprise` (confidence) | 0.823 | 0.683 | 0.714 | 0.776 | robust |
| rd `fisher_eff_rank` | 0.111 | 0.433 | 0.208 | 0.247 | **nf4-inflated artifact** |
| att `last_minus_1_bos_mass` | 0.545 | 0.727 | 0.705 | 0.776 | grows with precision |

---

## Verdict on the pre-registered hypotheses

- **H1 (winner-cell + sign invariance):** ❌ **as stated, but for the right reason.** The *winner* is not invariant on triviaqa — but that is selection noise, not signal change. Re-cast on fixed cells, the strong cells are direction-stable across all rungs. The hypothesis was mis-specified; the invariance lives at the cell level, not the argmax.
- **H2 (monotone-or-flat in bits):** ❌ **not monotone.** `int8` is a non-monotone outlier (consistently the weakest strong-signal rung). The axis is not a clean precision ramp because `int8` ≠ "between 4 and 16 bit" — it is a different quantization *family* (LLM.int8 outlier-decomposition).
- **H3 (quantization-artifact falsifier):** ✅ **falsified at the fixed-cell level.** Every robust cell holds its strength and direction from 4 to 32 bits (anli `neg_shadow_logvol_r1` 0.68–0.75; triviaqa `mid_js_kv_groups` 0.80/0.80/0.81 at nf4/bf16/fp32; `surprise` 0.71–0.82). The signal is not rounding noise. The *one* cell that behaves like an artifact — `fisher_eff_rank`, strongest and sign-reversed at nf4, decaying toward full precision — is not load-bearing.

## Four conclusions

1. 🧱 **Strong signals are precision-invariant** → the panel measures real computation, not quantization structure.
2. 🔄 **Quantization destabilizes *selection*, not signal** → at nf4 the cell landscape is noisier, so the OOB selector can't lock on (anli stability 0.50 → bf16 0.95); precision sharpens the landscape. Cross-precision must be judged on fixed cells.
3. ⚠️ **`int8` is an outlier rung** → LLM.int8 outlier-decomposition degrades morphology more than nf4 or bf16 in places (triviaqa `mid_js_kv_groups` 0.68 vs ~0.80). Do not treat the ladder as one monotone axis; report int8 separately.
4. 🔎 **A few readout cells carry mild quantization-correlated structure** (`fisher_eff_rank`) but are not the cells the panel relies on. Worth a caveat that 4-bit `fisher_eff_rank` winners should be treated with suspicion.

## Caveats
- One model (7B), one wave; n=200; in-sample fixed-cell AUROC (identically computed per rung, so cross-rung *differences* are valid, but absolute values are optimistic vs OOB).
- Commit-equivalence (§4 of the pre-reg): the validate items already showed nf4 flipping a commit vs the higher rungs; the full intersection-set re-score is **still TODO** (per-sample commit tokens need a dedicated dump).
- Non-byte-comparable; does not touch the sealed 18/20.

---

## Wave 2 — Qwen2.5-32B `{nf4,int8,bf16}` (2026-06-23)

**Provenance correction (Bell-Burnell):** a byte-identity check caught that the original 32B baseline (anli 0.790 / triviaqa 0.822) was run in **bf16**, not 4-bit (no `--load-in-4bit` flag; 32B-bf16 fits one 80GB). The pre-patch runs were not precision-stamped. A **true-nf4 32B** run was then done (stamped), confirmed distinct from bf16 (score-matrix maxdiff ≫ 0). All mislabeled docs corrected 2026-06-23.

| task | nf4 (true 4-bit) | int8 | bf16 |
|------|------------------|------|------|
| anli — winner / CI_lo | `att last_minus_1_js` 0.763 | `att bos_mass` 0.784 | `att bos_mass` 0.790 |
| triviaqa — winner / CI_lo | `att final_bos_mass` 0.781 | `att v_norm` 0.822 | `att v_norm` 0.822 |

Fixed-cell (robust attention cells): anli `last_minus_1_bos_mass` 0.846/0.886/0.884; triviaqa `final_bos_mass` 0.886/0.883/0.874 (nf4/int8/bf16).

**Three findings:**
1. 🎯 **Family dissociation DE-CONFOUNDED.** At matched nf4 precision, **Qwen-32B-nf4 wins attention** while **Llama-70B-nf4 wins readout** — so the [[llama-70b-scale-2026-06-22|locus dissociation]] is real, not a bf16-vs-4bit artifact. (The mislabel had put it at risk; the true-nf4 run rescues *and* strengthens it.)
2. 🔬 **The two "exotic" wave-1 effects are SMALL-MODEL artifacts that wash out at scale:**
   - **int8-outlier** — at 7B int8 degraded the signal (0.68 vs 0.80); at **32B int8 ≈ bf16** (0.784/0.822). LLM.int8 only hurts the small model.
   - **Selection instability** — at 7B the winner flipped every rung; at **32B the winner is stable** (attention, all rungs, both tasks). The bigger model's landscape is clean enough that selection locks on regardless of precision.
3. 🧱 **Robust core holds at both scales** — signal precision-invariant; nf4 marginally below bf16 at 32B (anli 0.763 vs 0.790) but solidly deployable. "4-bit costs a little, breaks nothing."

## Revised cross-wave conclusions
- **Signal is real + precision-invariant** — confirmed at 7B *and* 32B. H3 falsified at both scales.
- **Selection instability + int8-degradation are small-model phenomena** — present at 7B, gone at 32B. So "cross-precision needs fixed-cell not argmax" is most important for *small* models; at 32B even the argmax is stable.
- **A few readout cells carry mild nf4-correlated structure** (`fisher_eff_rank` at 7B) — minor, not load-bearing.

## Still TODO
- Commit-equivalence intersection-set re-score (per-sample commit dump).
- Optional: byte-verify 72B precision (inferred nf4, not stamped).

See also [[llama-70b-scale-2026-06-22]], [[summary]].
