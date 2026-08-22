# Residual-stream sub-layer friction — full-repertoire pilot (2026-06-06)

**Status**: 🧯 **[CORRECTED — SAME-Δ BENIGN / RESIDUAL-BUDGET BASELINE DEFLATES SIGNAL; NO SEALED PROMOTION]** · candidate [[research-candidates#9-residual-stream-sub-layer-friction-attention-vs-mlp|#9 (v5)]]
**Headline**: the earlier random-û-controlled / late-layer story was **anti-conservative**. A schema-v3 rerun added the decisive **same-`Δh` benign cancellation baseline**: hold `Δh = a+m` fixed, match raw cancellation/norm budget, and rotate the hidden disagreement channel off the consequential direction. Under that floor, Qwen/Llama full-window nets collapse to ≈0 or negative; selected late-window residuals are small/post-hoc. Best interpretation: the pilot mostly measured **benign cancellation / residual norm budgeting**, not a clean Knowledge Veto.
**Endpoint**: locked PRIMARY `delta_friction_over_null_route` = incremental cross-fit OOF AUROC of `{null_ratio + route-size + friction}` over `{null_ratio + route-size}`.
**Data**: `experiments/v4-sealed/2026-05-26/data/anli_R1_seed20260526_n200.jsonl`, n=200 (100/100), t=0.
**Label semantics**: ANLI label = **belief class** (0=entail/YES, 1=contradict/NO), **not** correctness/hallucination. Phrase results as "discriminates commit class beyond v3," never "hallucination tell."
**Artifacts (repo)**: `experiments/residual-friction/2026-06-06/` — run-01..06 = historical random-û screen; **run-07 = schema-v3 same-Δ rerun for Qwen2.5/Qwen3/Llama3.2/Llama3.1**, with `same_delta_panel.txt`, `residual_budget_panel.txt`, and same-Δ layer profiles. Scripts: `scripts/benign_cancellation_baseline.py`, `scripts/analyze_residual_budget.py`, upgraded `scripts/analyze_friction_layer_profile.py`.

> ⚠️ Bracketed intervals are **repeated-CV split-sensitivity intervals** (split + training variance only) — a **screening** device, **NOT** an inferential CI. The real CI comes from a sealed `pri_calibrator.py` nested-OOB run. "GO" = clears the screen → eligible to promote, **not** validated.

## Correction of record — same-Δ benign baseline + residual-budget test

The latest repo state supersedes the earlier "Qwen+Llama late-layer positive" wording. Claude's last vault-visible state was the operating-point correction (Llama not a null; promote late-window Qwen/Llama). New Codex work then added:

- **schema v3 feature dumps** (`run-07`) with `Xbenign`: sufficient projections for a same-`Δh` benign cancellation floor, without storing full `a`/`m` vectors.
- **same-Δ benign panel**: compares real friction to a baseline with identical `Δh`, matched raw cancellation, and disagreement rotated off the consequential direction.
- **residual-norm budget panel**: tests whether `||a||`, `||m||`, `||a+m||`, path balance, trim, and gain ratios explain the lift.

**Full-window same-Δ corrected panel (run-07):**

| Model | raw PRIMARY | same-Δ floor | net | read |
|---|---:|---:|---:|---|
| Qwen2.5-7B | +0.1205 | +0.1129 | **+0.0076** | mostly benign cancellation |
| Qwen3-8B | +0.0955 | +0.1235 | **−0.0280** | floor > signal |
| Llama-3.2-3B | +0.0458 | +0.0477 | **−0.0019** | floor ≈ signal |
| Llama-3.1-8B | +0.0150 | +0.0171 | **−0.0021** | floor ≈ signal |

**Best selected 3-layer same-Δ residuals** are small and post-hoc: Qwen2.5 17–19 **+0.0366**, Qwen3 14–16 **+0.0062**, Llama3.2 11–13 **+0.0102**, Llama3.1 19–21 **+0.0336**. The old late-window peaks were mostly norm/cancellation floor (e.g. Qwen3 24–26: raw +0.1321, same-Δ +0.1316, net +0.0005).

**Residual-budget diagnostic:** friction adds essentially nothing after the same-Δ floor:

| Model | `friction | null+route+same-Δ` |
|---|---:|
| Qwen2.5-7B | +0.0134 [+0.0068,+0.0195] |
| Qwen3-8B | −0.0036 [−0.0093,−0.0002] |
| Llama-3.2-3B | −0.0010 [−0.0087,+0.0031] |
| Llama-3.1-8B | −0.0043 [−0.0138,+0.0012] |

**Corrected verdict:** do **not** promote the current v5 residual-friction statistic to sealed nested-OOB as a Knowledge Veto signal. The method upgrade is valuable: it found the right negative control. The empirical claim deflates to "benign cancellation / residual norm budget explains the pilot," not "directed epistemic veto."

## Historical random-û panel — 9 models scored (3 GO / 6 NO-GO, superseded)

| Model | Family | v3 `null_ratio` | PRIMARY Δ `friction\|null+route` | random-û ctrl | shuffled ctrl | Screen |
|---|---|---|---|---|---|---|
| **Qwen2.5-7B** | Qwen | 0.614 | **+0.120** [0.107, 0.134] | +0.016 ⚠ | −0.019 ✅ | **GO** (leak-inflated; true ≈ +0.104) |
| **Qwen3-8B** | Qwen | 0.722 | **+0.096** [0.081, 0.110] | −0.003 ✅ | +0.004 ✅ | **GO — clean** |
| **Llama-3.2-3B** | Llama | 0.679 | **+0.046** [0.030, 0.059] | −0.006 ✅ | −0.013 ✅ | **GO — clean** |
| Qwen3-1.7B | Qwen | 0.668 | +0.011 [−0.008, 0.027] | −0.004 ✅ | −0.002 ✅ | NO-GO (touches 0) |
| Llama-3.1-8B | Llama | 0.516 | +0.015 [−0.004, 0.029] | −0.005 ✅ | −0.037 | NO-GO (touches 0) |
| Mistral-7B | Mistral | 0.663 | +0.012 [−0.002, 0.021] | −0.002 ✅ | +0.002 ✅ | NO-GO (touches 0) |
| Mistral-Nemo-12B | Mistral | 0.824 | −0.004 [−0.011, 0.001] | −0.002 ✅ | −0.001 ✅ | NO-GO (negative) |
| Gemma-3-4B | Gemma | 0.638 | −0.009 [−0.023, −0.001] | −0.004 ✅ | +0.060 ⚠ | NO-GO (negative) |
| DeepSeek-Distill-Qwen-7B | Qwen* | 0.551 | −0.008 [−0.040, 0.011] | −0.010 ✅ | **+0.166** ⚠⚠ | NO-GO (CV broken) |

Native-logits parity passed on every scored model (rel-L2 = 0.00e+00 except gemma-3-4b; Qwen3 passed **bit-exact despite per-head q/k-norm**, confirming the a/m split survives that architecture).

### Two models did not run — guards fired correctly (not bugs)
- 🚫 **Dolphin-Nemo-12B** — allowlist refusal in 2s. Cause: **case-sensitivity** (slug `...mistral-nemo...` lowercase ≠ allowlist `"Mistral"`). Genuinely Nemo-arch, but Mistral-Nemo already ran (NO-GO) → redundant, no loss. *(Latent gate quirk worth noting: the allowlist is case-sensitive; a lowercase-slugged in-family model is a false-negative.)*
- 🛡️ **gemma-3-1b** — native-parity guard **aborted** at the longest sample (`rel-L2=1.24e-02 > 5e-3`): its sliding-window mask drifts from native at long sequences (gemma-3-4b passed bit-exact; the 1B has a different SWA period). RETIRED model anyway. The guard correctly refused to emit wrong a/m.

## Within-family verdict — the question this batch was built to answer

Designed to discriminate **model- vs family- vs scale-dependence** by adding a second model per already-tested family:

- 🟩 **Qwen — replicates, scale-gated.** Qwen2.5-7B GO **+** Qwen3-8B GO agree across generations. Qwen3-1.7B is NO-GO → friction needs a *capable* Qwen (7–8B), not the 1.7B. **The two big Qwens are the only robust positive cluster in the panel.**
- 🟨 **Llama — replicates at the late-layer operating point (NOT a null).** On the pre-registered full-window-mean PRIMARY, Llama-3.1-8B reads NO-GO (+0.015) while Llama-3.2-3B is GO — which looked like non-replication. **The layer profile overturns that**: Llama-3.1-8B has the **strongest late-layer friction of any model** (window 21–23 net **+0.196**, lo +0.163, rand-subtracted), diluted to nothing by averaging friction across the mid-band `[0.25n, 0.75n)`. Both Llamas carry strong late friction; the 8B's full-window NO-GO is an **operating-point artifact** (mid-band dilution, which worsens with depth). *Status: OPEN pending a pre-registered late-window re-screen* — the peak window is post-hoc selected, so this is "clearly not a null", not yet a confirmed GO.
- ⬛ **Mistral / Gemma — genuine nulls.** Mistral-7B + Mistral-Nemo-12B NO-GO at both scales; even Nemo's *peak* late window is only +0.042 — at the selection floor, no late ramp when you go looking. Mechanistically tidy: Nemo (the [[results/inter-head-disagreement-2026-05-15|inter-head sink-failure]] case) has `null_ratio` 0.824 and `mean_‖a‖` 0.871 — **sink/magnitude-dominated**. Gemma-3-4B peak +0.046, also floor.

**Historical bottom line (superseded by same-Δ):** the random-û screen made friction-over-v3 look like a late-layer-localized signal on capable Qwen and Llama models, absent on Mistral/Gemma and small models. That was the correct read *under the weaker random-direction floor*, but run-07 shows the same apparent signal is largely reproduced by same-`Δh` benign cancellation / residual-budget features. Treat this section as provenance for the correction above, not as the current promotion decision.

## Two control leaks — honest red flags

1. 🩸 **Qwen2.5-7B random-û leak** (+0.016): Qwen2.5-specific (Qwen3-8B's random-û is clean at −0.003). A random direction picks up Qwen2.5's huge `mean_veto` 0.866 marginal → its +0.120 is **partly inflated**; trustworthy differential ≈ **+0.104**. Notably, **Qwen3-8B's clean +0.096 corroborates the Qwen-cluster signal without the leak** — the cleaner of the two positives.
2. 🩸 **DeepSeek-Distill shuffled-labels leak (+0.166)** — the alarming one. On a reasoning-distill the repeated-CV is badly anti-conservative; *all* its numbers are untrustworthy (PRIMARY negative anyway, so no false claim escapes). Gemma-3-4b's +0.060 shuffled leak is a milder instance. Llama-3.1-8B's −0.037 shuffled is the *safe* direction (deflation, not inflation).

The shuffled-label leaks on distill/Gemma are a standing flag that **the screen's split-sensitivity CV can break on some models** — the sealed calibrator's nested-OOB is the real arbiter.

## Per-layer profiles → late-layer concentration (where positive)

`*.layer_profile.txt` (regenerated offline from the `.npz` `layer_tensor` via `scripts/analyze_friction_layer_profile.py`; `net` = friction increment minus same-layer random-û increment). Earlier batch: Qwen2.5's signal lives in the **last 3 layers** (window 18–20 net +0.1475).

**Qwen3-8B confirms the same signature** (36 layers, window [9,27)): flat-to-negative through the mid-band (L13–19 net ≈ 0), then a hard late ramp — L22 net +0.1001, **L25 net +0.1210**, L26 net +0.1129; best window **23–25 net +0.1371**; `veto_auc` 0.87–0.89 at L25–26.

**Peak 3-layer-window net (rand-subtracted), all 8 profiled models** — the late-layer operating point:

| Model | full-window PRIMARY | peak late-window net | read |
|---|---|---|---|
| Llama-3.1-8B | +0.015 (NO-GO) | **+0.196** (21–23, lo +0.163) | 🔝 strongest — yet full-window NO-GO |
| Qwen2.5-7B | +0.120 (GO) | +0.1475 (18–20) | positive |
| Qwen3-8B | +0.096 (GO) | +0.1371 (23–25) | positive |
| Llama-3.2-3B | +0.046 (GO) | +0.087 (17–19) | positive |
| DeepSeek-distill | −0.008 | +0.087 (17–19) | ⚠ CV broken — ignore |
| Qwen3-1.7B | +0.011 | +0.051 (12–14, *mid*) | null floor |
| Gemma-3-4B | −0.009 | +0.046 (20–22) | null floor |
| Mistral-Nemo-12B | −0.004 | +0.042 (22–24) | null floor |

*(Mistral-7B has no `.npz` dump — run-01 predates the feature-dump flag — so no profile.)* The peak is **post-hoc selected** over \~12 windows, so exact values are winner's-curse-inflated; but the **null floor sits at ≈ +0.05** (where the true nulls Qwen3-1.7B/Gemma/Nemo all land) and trustworthy positives sit at **+0.087–0.196**, a real gap.

📌 **Operating-point finding (superseded):** under random-û, friction appeared late-layer-localized and diluted by the full-window mean. Under same-Δ, the old late peaks mostly collapse into the benign floor. The late-layer observation remains useful as a diagnostic of where residual budgeting happens, but it is **not** sufficient evidence for a Knowledge Veto.

## Reproducibility note — analyzer reconstructed

The run-03/04/05 `layer_profile.txt` files were produced by an **ephemeral Codex script that was never committed**. Closed that gap: `scripts/analyze_friction_layer_profile.py` reuses the pilot's own `_repeated_cv_delta` / `_signfree_auroc` and was validated against run-03's Qwen profile — **deterministic columns (marginal AUROCs) match exactly**; CV-delta columns agree to **±\~0.001** (well inside the \~0.015 interval width; the residual is unrecoverable RNG-seed variation, itself a sample of the split-sensitivity the interval reports). Methodologically equivalent, now reproducible.

## Next steps (corrected)
1. ✋ **Do not promote current v5 residual-friction to sealed nested-OOB.** The same-Δ / residual-budget baseline is the governing control, and the Qwen/Llama cluster does not clear it.
2. 🧱 Treat `same-Δ benign` as a mandatory negative control for any future "veto" candidate: if real friction does not beat the identical-`Δh` benign floor, it is residual budgeting / refinement, not destructive veto.
3. 🔍 If revisiting the idea, design a new statistic that predicts above `Xbenign` and budget features *before* model reruns; current run-07 dumps are enough for offline prototyping on Qwen/Llama.
4. 🗃️ Preserve the random-û panel as historical provenance only; it is not the promotion screen.

## See also
- [[research-candidates#9-residual-stream-sub-layer-friction-attention-vs-mlp]] — candidate ledger (decisive bar, isolation baseline, falsification).
- [[results/inter-head-disagreement-2026-05-15]] — the JS sign-stable Qwen2.5/Mistral-7B pairing that seeded the pilot; Mistral-Nemo = the sink-driven failure, now corroborated here.
- [[results/v3-main-run]] — v3 sealed baseline (the `null_ratio` this candidate must beat incrementally).
