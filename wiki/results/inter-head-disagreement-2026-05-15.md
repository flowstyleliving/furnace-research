# Inter-head attention disagreement at commit step — 2026-05-15

> _Page is reverse-chronological: **run-02 (9-model panel)** is the current headline view. Run-01 (2-model) is preserved below as the historical entry; the run-01 verdict is **superseded** by the SinkProbe-controlled reading below._

> ⚠️ **t=0 caveat ([[step0-belief-readout-2026-05-17]], 2026-05-17):** the belief-readout panel **re-grounds the commit-step *premise*** (a discriminative t=0 logit locus exists; Mistral-Nemo anchor 0.99 passed) but the frozen pre-reg explicitly bars this from validating the JS-radius / attn-entropy numbers below — for CoT-tuned models those `gen_step=1` readings were taken at a reasoning-preamble token and still need re-measurement at the logit-defined locus. **Phi-3.5-mini is Low-decidedness-for-M at t=0** (eligible_cov 0.185) — tension vs its Step-1 "clean trustworthy" status. Premise re-grounded ≠ these readings validated.

## 📌 Run-02 — 9-model panel (2026-05-15 evening)

_Run: 2026-05-15, run-02. 9 models × {final, mid, last-1} × n=200 ANLI R1 (same slice as run-01), hardened script (`scripts/diagnose_inter_head_disagreement.py` rev 2026-05-15)._

> **🟡 Verdict [OPEN — direction is robust under sink controls, layer is not. Two of nine models are pure SinkProbe stories. Run-01 verdict is superseded.]**
>
> 1. **7 of 9 models show a clean (sink-controlled) signal at SOME layer, all `hi` orientation** under `js_radius_no_bos_*` or `js_radius_kv_groups_*`. High cross-head disagreement at the commit step predicts contradiction — the *opposite* of run-01's `lo` reading. The original `lo` framing was the **SinkProbe signature** in disguise; once we control for sinks (no-BOS column from the 2026-05-15 hardening), direction inverts to the intuitive one.
> 2. **2 of 9 models (Llama-3.2-3B, Mistral-Nemo-12B) are sink-driven** — `js_radius_*` AUROC closely tracks `bos_mass_*` AUROC, and the no-BOS-corrected signal collapses or stays at chance. These are the two heaviest sink-dominant models in the panel; they align with [SinkProbe (Binkowski et al., 2026)](../feedback/inter-head-prior-art-2026-05-15.md) rather than the head-disagreement story.
> 3. **No universal layer.** final / mid / last_minus_1 each win on different models; within-family layer-stability is also weak (Phi-3.5 last_minus_1 vs Phi-4 final). This re-confirms the [calibration pivot](../learn/calibration-pivot-eli12.md) from the 2026-05-13 ANLI sweep: per-(model, exact distribution) operating-point selection is the honest framing for the attention side too, not "universal cross-arch invariant."
> 4. **Qwen 2.5 7B run-02 numbers were corrupted by float16 overflow at the final layer — corrected reading lands at last_minus_1, not final.** Two-stage resolution: (a) the wrapped-vs-unwrapped invariance probe ran 10/10 byte-identical on Qwen 2.5 confirming the new wrapper itself is observational; (b) the v4-candidate #5 attention-only calibration smoke surfaced 180/200 NaN at the final layer specifically. Root cause: float16 overflow in the manual SDPA `q @ kᵀ` at the deepest block (scores up to ~1800 with +inf in unmasked positions → NaN through softmax). **Fix landed 2026-05-15 evening**: fp32 cast of q + k before the matmul in `_capture_last_query_weights`. Re-ran descriptive panel with the fix: now 0 NaN at all 3 layers; corrected n=200 reading is **last_minus_1_js_no_bos = 0.82** (not the original "final_js_kv_groups = 0.92" which was effective-n=20). The 9-model panel's other 8 models had 0 NaN before the fix, so this correction applies to Qwen 2.5 only. Corrected CSV at `experiments/inter-head-disagreement/2026-05-15/run-02/Qwen2.5-7B-Instruct-4bit_head_disagree_fp32fix.csv`.

### 9-model panel — sink-controlled signal table

Operating-point selection: for each model, pick the (layer, metric) cell with highest sink-controlled AUROC where `bos_mass` is at chance (0.35–0.65) or anti-correlated (< 0.35). "Clean?" = the signal is not explained by BOS-sink dynamics.

| Model | Best clean layer | Metric | AUROC | bos_mass | Clean? |
|---|---|---|---:|---:|:---:|
| Qwen2.5-7B (GQA-7×) | ~~final~~ → **last_minus_1** | ~~js_kv_groups (0.92)~~ → **js_no_bos** | ~~0.92~~ → **0.82** | 0.35 | ✅ hi |
| Phi-3.5-mini (MHA) | last_minus_1 | js_no_bos | 0.77 | 0.26 | ✅ hi |
| Qwen3-8B (GQA) | **final** | js_kv_groups | 0.75 | 0.28 | ✅ hi |
| gemma-3-4b (GQA) | mid | js_no_bos | 0.73 | 0.23 | ✅ hi |
| Phi-4-mini | **final** | js_no_bos | 0.72 | 0.50 | ✅ hi |
| Mistral-7B-v0.3 (GQA-4×) | mid | js_no_bos | 0.65 | 0.30 | ✅ hi |
| Qwen3-1.7B-4bit | last_minus_1 | js_no_bos | 0.62 | 0.40 | ✅ hi |
| Llama-3.2-3B | — | — | — | tracks `js` | ❌ sink-driven |
| Mistral-Nemo-12B | — | — | — | 0.64 at final | ❌ sink-driven |

Three pieces of cross-model structure worth pulling out:

- **GQA-aware aggregation (js_kv_groups) wins on the Qwen family.** Qwen 2.5 final: js=0.84 → js_kv_groups=0.92 (boost). Qwen3-8B final: js=0.64 → js_kv_groups=0.75 (boost). Qwen3-8B mid even sign-flips under GQA collapse (0.33 lo → 0.67 hi). Collapsing per-head distributions onto the KV-group level produces a cleaner geometric read for Qwen-family models.
- **Phi family shows sign-consistency, layer-instability.** Phi-3.5-mini's clean signal is at last_minus_1 (0.77), Phi-4-mini's is at final (0.72). Both `hi` orientation, both ~0.7 AUROC, but neighboring rather than identical layers. Within-family layer stability is weaker than I'd have predicted.
- **Sink-driven failure mode is concentrated in the SinkProbe-evaluated models.** Llama-3.2-3B and Mistral-Nemo-12B are 2 of the 4 models SinkProbe evaluates in their Table 1. Our diagnostic is reading the same dynamics they probe; they have a supervised probe, we have an unsupervised AUROC, and on these two models the supervised probe is the cleaner instrument.

### Reading the run-01 → run-02 numerical reconciliation

| Model | Layer | run-01 (post-flip) | run-02 (raw) | Match? |
|---|---|---|---|---|
| Mistral-7B-v0.3 | final | 0.7401 (−) | 0.2597 (lo) | ✅ exact (0.2597 = 1 − 0.7403) |
| Mistral-7B-v0.3 | mid | 0.7148 (+) | 0.7148 (hi) | ✅ exact |
| Mistral-7B-v0.3 | last-1 | 0.7126 (−) | 0.2872 (lo) ≈ 1−0.7128 | ✅ exact |
| **Qwen2.5-7B** | **final** | **0.6014 (−)** | **0.8438 (hi)** | ❌ 0.84 ≠ 1 − 0.60 = 0.40 |
| Qwen2.5-7B | mid | 0.5496 (−) | 0.6314 (hi) | ❌ |
| Qwen2.5-7B | last-1 | 0.6206 (−) | 0.7503 (hi) | ❌ |

Mistral 7B reconciles to byte-identical raw AUROC; the run-01 `(-)` flags were just post-hoc `max(auc, 1-auc)` operations that the hardening removed. Qwen 2.5 does NOT reconcile this way — the raw AUROC changed by ~0.24 at final. The most plausible explanation is the **old wrapper was perturbative on Qwen 2.5** (different attention layout) and the new observational wrapper is the first faithful read. This makes Qwen 2.5's run-02 number the trustworthy one, but it should be confirmed with the standard wrapped-vs-unwrapped invariance probe (the same one the handoff ran on Mistral/Qwen3-1.7B/Gemma but not Qwen 2.5).

### Why this is [OPEN], not [VALIDATED] or [FALSIFIED]

- ✅ **Direction is robust.** 7/7 clean signals point `hi`. Under SinkProbe controls, high cross-head disagreement at commit predicts contradiction. This is internally consistent and matches prior-art expectations from [RAUQ](../feedback/inter-head-prior-art-2026-05-15.md) (uncertainty-aware heads abandon their concentration → cross-head disagreement increases).
- ❌ **No universal operating point.** Layer drifts model-by-model. Per-(model, distribution) calibration is needed, which means this is a panel-cell candidate for `pri_calibrator.py`, not a standalone universal detector.
- ❌ **2/9 models are sink-driven.** On Llama-3.2-3B and Mistral-Nemo, the diagnostic is reading SinkProbe-shaped dynamics, not the head-disagreement story. These two models would underperform vs SinkProbe's supervised probe on their own evaluation set.
- ❓ **Qwen 2.5 numerical anomaly unresolved** pending the invariance probe.

The honest framing in the rollup is: this is **a candidate panel cell for `pri_calibrator.py` with model-dependent operating-point** — not a paper-grade universal claim. The [prior-art note](../feedback/inter-head-prior-art-2026-05-15.md) already pre-empted this framing.

### Pending follow-ups (in priority order)

1. ✅ ~~**Wrapped-vs-unwrapped invariance probe on Qwen 2.5 (`--limit 10`).**~~ Done 2026-05-15 evening via `scripts/invariance_probe_inter_head.py`. **Result: 10/10 match** — wrapped and unwrapped `gen_token_ids` byte-identical across 10 ANLI R1 prompts × 4 gen tokens each. New wrapper is observational on Qwen 2.5; run-01 numbers were old-wrapper-perturbed; run-02 numbers are the corrected read.
2. ✅ ~~**Add the diagnostic as a panel cell candidate in `pri_calibrator.py`.**~~ **Implementation landed 2026-05-15 evening as [v4-candidate #5](research-candidates.md#5-attention-cell-extension-to-pri_calibratorpy)torpy)**. 102/102 pytest green (+52 new tests including Gemma-3-1B e2e byte-exact self-test). Qwen 2.5 + ANLI R1 n=200 smoke picks `attention[final_js_kv_groups]` AUROC 0.922 sign +1 — exact agreement with the descriptive panel's headline. **Surfacing finding**: smoke revealed the descriptive panel's "n=200 AUROC 0.92" headline is actually effective-n=20 (180 of 200 Qwen 2.5 final-layer captures are NaN — pre-existing precision overflow in the wrapper's manual SDPA at the deepest block; affects every final-layer column in `experiments/inter-head-disagreement/2026-05-15/run-02/Qwen2.5-7B-Instruct-4bit_head_disagree.csv`). Calibrator's OOB CI [0.14, 1.00] + winner_stability 0.42 + 4 insufficient_coverage warnings exposed what the descriptive panel hid — exactly what schema v1.1 safety rails are for.
3. ✅ ~~**Decide on a §5.4 paragraph for the v3 paper round-2 revision.**~~ **Landed 2026-05-15** in [paper/pri-draft.tex](../paper/pri-draft.tex) §5.4 between "Causal probe of rupture geometry" and "Other extensions" — new \paragraph block "Attention-side rupture at the commit step" cites both [SinkProbe](../feedback/inter-head-prior-art-2026-05-15.md) (`\citet{binkowski2026sinkprobe}`) and [RAUQ](../feedback/inter-head-prior-art-2026-05-15.md) (`\citet{rauq2026anonymous}`), positions v4 attention-related future work as commitment-step specific (gen_step=1), names the n=200 9-model panel descriptive result as a leading-edge finding, and adds two bibitems. The v3 sealed claim is unchanged; the paragraph is additive within future-work.
4. 🚫 **Explicit non-action: R2 + R3 ANLI replicates on this diagnostic.** Not a TODO. The 2026-05-13 ANLI 33-profile sweep already proved cross-round instability for residual-stream metrics; the attention-side signal pattern here is consistent with the same lesson, and further round replication would not change the [OPEN] verdict. If anything is run beyond run-02, it should b[v4-candidate #5](research-candidates.md#5-attention-cell-extension-to-pri_calibratorpy)alibratorpy) integration on a *single* model + round, not a cross-round panel.

### Run-02 artifacts

- CSVs: `experiments/inter-head-disagreement/2026-05-15/run-02/*_head_disagree.csv` (9 files)
- Logs: same dir, `*_head_disagree.log` + `run.log` (orchestrator summary)
- Wall: 100 min (18:45:40 → 20:25:47 PDT 2026-05-15)
- Orchestrator: `scripts/run_inter_head_panel.sh` (rev 2026-05-15)
- Prior-art positioning: [feedback/inter-head-prior-art-2026-05-15](../feedback/inter-head-prior-art-2026-05-15.md)

---

## Historical: run-01 (2-model verdict, 2026-05-15 afternoon — superseded)

> ⚠️ The run-01 verdict below is preserved as the historical record. The run-02 SinkProbe-controlled reading **inverts** the headline direction (run-01 said low disagreement → contradiction at final; the corrected reading is high disagreement → contradiction at the clean layer, with the run-01 `lo` framing now attributed to BOS-sink dynamics, not head agreement). Run-01 numerical results (Mistral 7B exact) are reproducible; Qwen 2.5 numbers in run-01 are suspected old-wrapper-perturbed and should not be quoted.

_Run: 2026-05-15, run-01. Mistral 7B v0.3 + Qwen 2.5 7B × {final, mid, last-1} blocks, n=200 ANLI R1 calibration samples each._

> **🟡 Verdict [OPEN, mildly encouraging — first W_u-free signal with cross-model sign consistency, but AUROC magnitude does not transfer.]** ← **SUPERSEDED by run-02 above.**
>
> 1. **Mistral final JS-radius AUROC = 0.7401 (sign −).** Passes falsification gate 1 (AUROC ≥ 0.6 on the easy case). Direction: **LOW** head disagreement at the commit step predicts contradiction. Counter-intuitive but consistent at last-1 too.
> 2. **Qwen 2.5 final JS-radius AUROC = 0.6014 (sign −).** **Same sign as Mistral** (no flip) but the magnitude collapses by 0.14. Partial transfer — sign-stable, strength-fragile.
> 3. **The complementary attn-entropy channel FLIPS sign** between Mistral (+) and Qwen (−) across all three layers. So attn-entropy fails the cross-model invariance test entirely; JS-radius is the only channel that survives sign-test.
> 4. **Gate 3 (full architectural invariant on 3+ models at same sign and similar AUROC) is NOT MET.** Sign is stable, magnitude is not. Worth running Llama 3B to triangulate, but the signal is not the universal invariant we hoped for. Closer to gate 2 (collapse) than to gate 3 (pass).

## Falsification gates revisited

| Gate | Predicted observation | Actual | Status |
|---|---|---|---|
| 1. Dead at the easy case | Mistral AUROC < 0.6 | Mistral final = 0.7401 | ❌ **Not triggered** |
| 2. Collapse / flip on Qwen | Same sign + magnitude on Qwen | Same sign, but 0.74 → 0.60 magnitude drop | 🟡 **Partial — sign survives, strength does not** |
| 3. Architectural invariant | Same sign + similar AUROC across 3 models | 2-of-2 sign-consistent at final layer; magnitude not | 🟡 **Inconclusive — third model (Llama 3B) not run** |

## Setup

| Field | Value |
|---|---|
| Date | 2026-05-15 (~3h wall, sequential — both 7B models) |
| Output | `experiments/inter-head-disagreement/2026-05-15/run-01/` |
| Models | Mistral-7B-Instruct-v0.3-4bit + Qwen2.5-7B-Instruct-4bit |
| Data | `experiments/anli-sweep/2026-05-15/run-02/anli_R1_seed20260513_n100.jsonl` (200 rows total, 100/class) |
| Layers | `final` (last block) + `mid` (N//2) + `last_minus_1` (N-2). Mistral N=32 → 31, 16, 30. Qwen N=28 → 27, 14, 26. |
| Quantity | Jensen-Shannon information radius across heads at gen_step=1, plus per-head mean attention entropy. Both computed at the last-query row of each layer's attention matrix. |
| Script | `scripts/diagnose_inter_head_disagreement.py` |

## What the signal is

At gen_step=1 (commit step), each attention head `h` in a decoder block produces a distribution `A^h ∈ Δ^T` over past positions — softmax(QᵀK / √d). For H heads at a target block:

**JS-radius (headline):**
```
disagreement = (1/H) Σ_h JS(A^h || A_centroid),   where A_centroid = mean_h A^h
```
Bounded `[0, log 2]`. High = heads point different places (hedge). Low = heads converge.

**attn-entropy (sanity feature):**
```
mean_h Entropy(A^h) = -(1/H) Σ_h Σ_t A^h_t log A^h_t
```
High = each head spreads uniformly. Low = each head concentrates on a few positions.

The two channels are different — JS-radius is **cross-head**, attn-entropy is **per-head averaged**. They can independently move.

**Architectural argument for transfer:** every transformer has H heads with softmax attention. The simplex shape (distribution over past positions) is W_u-free, vocab-free, and dimensionally comparable across models. JS divergence is symmetric, bounded, and direction-agnostic. So we expected — by construction — better cross-model sign stability than the W_u-projected line gave us.

## Results

### 🌬️ Mistral-7B-Instruct-v0.3-4bit (n=200, N=32 heads × 8 KV heads = GQA-4×)

| layer        | AUROC JS-radius | sign | AUROC attn-entropy | sign |
|--------------|----:|---|----:|---|
| **final** (31)        | **0.7401** | **−** | 0.7357 | + |
| mid (16)          | 0.7148 | + | 0.7158 | + |
| last_minus_1 (30) | 0.7126 | − | 0.7534 | + |

**Reading:** at final + last-1, **low JS-radius (head convergence) predicts contradiction.** Counter-intuitive — we'd naively expect heads to disagree when hedging. The interpretation: Mistral's heads ALIGN when committing to a contradictory claim ("yes, the contradiction is here, attend to the same tokens"), spread out when committing to a control ("multiple plausible continuations, no single anchor"). Mid-block flips: at mid-depth, the model is still synthesizing and the inverse pattern holds.

attn-entropy is sign + across all 3 layers: HIGH per-head entropy → contradiction. Combined with low JS-radius, this means: all heads agree on **uniform** attention patterns when committing to a contradiction. "Spread out, but spread out together."

### 🐲 Qwen2.5-7B-Instruct-4bit (n=200, N=28 heads × 4 KV heads = GQA-7×)

| layer        | AUROC JS-radius | sign | AUROC attn-entropy | sign |
|--------------|----:|---|----:|---|
| **final** (27)        | **0.6014** | **−** | 0.6457 | − |
| mid (14)          | 0.5496 | − | 0.5721 | − |
| last_minus_1 (26) | 0.6206 | − | 0.6956 | − |

**Reading:** JS-radius sign is consistent with Mistral (LOW disagreement → contradiction) at every layer. But:
1. AUROC magnitude is materially weaker — 0.60 vs 0.74 at final; mid is at-chance.
2. attn-entropy sign is **inverted** vs Mistral: on Qwen, LOW per-head entropy → contradiction. So Qwen's heads agree on a **concentrated** attention pattern when committing to contradictions, where Mistral's heads agree on a **uniform** one.

The two models converge on "low cross-head disagreement = contradiction" but disagree on the per-head shape of that agreement.

## Cross-model comparison vs the W_u-projected baseline

| Signal | Mistral final | Qwen 2.5 final | Cross-model sign | Δ AUROC |
|---|---|---|---|---|
| W_u null_ratio_post_rank2 (v3 paper) | 0.7600 (+) | 0.7918 (+) | ✅ same (+) | +0.03 (Qwen stronger) |
| **JS-radius head-agreement** (this) | **0.7401 (−)** | **0.6014 (−)** | ✅ **same (−)** | **−0.14 (Mistral stronger)** |
| attn-entropy | 0.7357 (+) | 0.6457 (−) | ❌ **flip** | n/a |

So JS-radius is the first cross-architectural signal we've tested that holds the SAME SIGN on both Mistral and Qwen — and it does so at a layer (final block, gen_step=1) that's analogous to the W_u sealed plane. That's a real positive — fewer cross-model sign flips than v3/v3.1/v3.2 ever delivered for any non-trivial geometric channel.

But the AUROC magnitude story is the opposite of the W_u-line: where W_u-stuff was *stronger* on Qwen than Mistral, JS-radius is the reverse. So this is genuinely a different signal, not a re-discovery of the W_u rupture in a new basis.

## What this is NOT (yet)

🚫 **Not a universal detector.** AUROC magnitude varies 0.14 across just two models. With only n=200 per cell and only two architectures sampled, the variance bars almost surely overlap with the "OOD-detection-in-a-different-basis" null hypothesis. The deep risk from the brainstorm — that this might also be vocabulary-shifted OOD detection at a different layer — is not yet ruled out.

🚫 **Not deployable.** Same calibration story as the W_u-projected work: per-(model, distribution) calibration is required. JS-radius's sign-stability doesn't change that.

🚫 **Not a paper claim.** n=200, two models, one round of ANLI. To even submit this as a workshop-paper-grade result we'd need: Llama 3B + Gemma 3-4B + one Qwen 3 (the v3.1/v3.2 panel scope), R2 + R3 replication, and proper OOB nested bootstrap CI (which pri_calibrator.py already implements but this diagnostic does not).

## Honest hedges & known caveats

⚠️ **Manual SDPA replaces the fused mlx kernel at 3 target layers.** Precision-level numerical drift (~1 in 10⁴ relative on most operations) means the wrapped model's gen_step=1 token may differ from the unwrapped model's in a small fraction of samples. We measured "what the slightly-perturbed wrapped model attended to as it committed." For attention-pattern measurement this is faithful; for vocabulary-output measurement (which we are NOT doing here) it would matter more.

⚠️ **One round of ANLI.** R1 only. The v3.1/v3.2 work showed that R1 vs R2 vs R3 calibrate differently for the SAME model. Cross-round transfer for JS-radius is unmeasured.

⚠️ **`captures[1]` indexing.** The diagnostic relies on `trace_sample` producing exactly one prefix forward followed by one gen-step-0 forward; if the trace logic changes (e.g., a new prefix-warmup step), indexing breaks silently. Worth a runtime assertion.

⚠️ **GQA expansion via mx.repeat.** Both Mistral (32/8) and Qwen 2.5 (28/4) use grouped-query attention. We expand keys/values via `mx.repeat`. This is correct numerically but doubles intermediate memory — fine here, would need attention if scaling to 70B-class.

## Implications & next moves

✅ **Run Llama 3B.** Same script, ~30 min. If JS-radius sign is also − at final on Llama, that's 3-of-3 sign consistency and gate 3 starts to look reachable.

✅ **Add Qwen3-8B.** If sign holds on Qwen3 (which collapses universally on W_u-stuff), that's strong evidence JS-radius is genuinely different from W_u-projected channels.

🔬 **Run R2 + R3 ANLI replicates** on Mistral + Qwen 2.5 to test within-task-family sign and magnitude stability. The v3.1/v3.2 finding (round-instability) is the most likely killer of the deployability story.

🛡️ **Add JS-radius as panel cell #9 in `pri_calibrator.py`.** Even if it doesn't universally beat null_ratio, it carries different information (different basis, different layer-dependence) and gives per-(model, distribution) calibration more cells to choose from.

⏸️ **Hold the paper claim.** This is a one-evening descriptive result, not a sealed gate.

## Artifacts

- CSVs: `experiments/inter-head-disagreement/2026-05-15/run-01/{Mistral-7B-Instruct-v0.3-4bit,Qwen2.5-7B-Instruct-4bit}_head_disagree.csv`
- Logs: same dir, `*.log`
- Script: `scripts/diagnose_inter_head_disagreement.py` (380 LOC standalone, mirrors `diagnose_delta_sigma_onaxis.py` shape)
- Pending: Codex adversarial review (issued separately)

## Backlinks
- [results/delta-sigma-onaxis-2026-05-15](delta-sigma-onaxis-2026-05-15.md) — sibling W_u-projected descriptive panel from earlier today
- [results/v3.2-results](v3.2-results.md) — sealed v3.2 verdict + Motif catalog
- [models/mistral-7b](../models/mistral-7b.md) — Mistral-specific phenomenology
- [models/qwen-2.5-7b](../models/qwen-2.5-7b.md) — Qwen 2.5 sealed-E17b authority
- [feedback/inter-head-prior-art-2026-05-15](../feedback/inter-head-prior-art-2026-05-15.md) — RAUQ (ICLR 2026) + SinkProbe (Binkowski et al. 2604.10697) prior-art positioning that reshapes the run-02 verdict gate
- [lit/external](../lit/external.md) — external papers catalog (RAUQ + SinkProbe entries)
