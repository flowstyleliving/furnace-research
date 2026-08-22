# Precision Ladder — Pre-Registration (2026-06-22)

**Status:** `[PRE-REGISTERED — wave 1 RUN 2026-06-22]` — predictions/falsifiers below are frozen as written. **Results: [[precision-ladder-results-2026-06-22]].** Wave-1 verdict in brief: H3 falsified at the fixed-cell level (robust signals are precision-invariant); H1 mis-specified (invariance is at the cell level, not the argmax winner); H2 false (int8/LLM.int8 is a non-monotone outlier rung). Key method-correction: cross-precision must be judged on **fixed cells**, not argmax winners.

**Code:** `/Users/msrk/Documents/furnace-guard/modal_app.py` (precision switch wired 2026-06-22; see [[../references/modal-cloud-extractor|modal-cloud-extractor]]). Backend = `modal-torch`. Every rung is **non-byte-comparable to the sealed MLX plane** — this is an exploratory *methods-robustness* probe and **does not touch the sealed 18/20**.

---

## 1. The question (sharpened)

The headline is **not** "does the method survive higher bits" (robustness) — it is **confound elimination**:

> Our entire panel (MLX seal, torch cloud, gemma-4) runs **quantized**. A skeptic's first shot: *"You inject rounding error into hidden states, then measure 'representation rupture' — how do you know you aren't measuring your own rounding?"*

A precision ladder is the only thing that answers it. If the diagnostic works **equal-or-better at bf16/fp32**, the signal is real model computation. If it **decays toward chance** as precision rises, we have been reading quantization noise. That falsification test is the scientific payoff.

### What the ladder isolates (mechanics)
- 🎯 **W_u is floating at every rung** — `lm_head`+`embed_tokens` skipped from quantization. The readout projection does not change.
- 🧮 **Attention activations already compute in bf16** even at 4-bit (bitsandbytes dequantizes per matmul).
- 📉 **Only the hidden state `h` changes** — weight-quantization error accumulates through the forward pass into the vector feeding both ACE and the readout.

So the ladder is a clean dose-response on exactly one thing: **sensitivity of the morphology to weight-quantization-induced hidden-state error.**

---

## 2. Design — within-model precision ladder

Hold *everything* fixed except bit-width, **on one backend** (torch cloud — so precision is not confounded with MLX-vs-torch impl). Fixed across rungs: model, task, n=200 data file, seed, calibrator (nested-OOB). **The calibrator is refit per rung** — a 4-bit model is a different deployment distribution than bf16, so honest per-(model, distribution) calibration demands a fresh fit; **never** reuse the nf4 profile on bf16 data.

| Rung | dtype | weights | role |
|------|-------|---------|------|
| 🔴 `nf4` | 4-bit | sub-16 | deployed baseline / anchor (== historical `load_in_4bit`) |
| 🟠 `int8` | 8-bit | sub-16 | mid rung |
| 🟡 `bf16` | 16-bit | full | native training dtype ≈ near-gold reference |
| ⚪ `fp32` | 32-bit | full | true gold (small model only) |

### Vehicles
- 🧪 **Primary: `Qwen/Qwen2.5-7B-Instruct`** — full 4-rung ladder `{nf4, int8, bf16, fp32}`. Cheap; *sealed* (ties to the registered plane modulo impl caveat); spans all four rungs on one `A100-80GB` (fp32 ≈ 28 GB).
- 🏔️ **Scale confirm: `Qwen/Qwen2.5-32B-Instruct`** — `{nf4, int8, bf16}` (fp32-32B ≈ 128 GB → OOM single 80 GB, excluded). Confirms the precision effect holds at scale.
- 🚫 **No 70B ladder** — bf16-70B needs 2×80 GB and is costly; the precision question is answered at 7B/32B.

Both tasks: `anli_r1`, `triviaqa_paired`.

---

## 3. Dependent variables

- 📊 **Deployability + geom CI-lo per rung** — the dose-response curve.
- 🧭 **Winner cell identity + sign** — does the same ACE sub-cell win across precision? (winner-stability = the invariance signal.)
- 📐 **Hidden-state divergence** — cosine between the bf16 commit-token `h` and the {nf4, int8} `h`. This **quantifies the dose** (ties "precision" to "how much the metric's input actually moved"). Expectation: high cos (>0.99), given the o_proj gate already sits \~1.0.
- 🛡️ **o_proj cos gate per rung** — internal faithfulness control; must be ≥0.999 at every rung or that rung's numbers are void.

---

## 4. The control that will bite us — commit equivalence

⚠️ If `nf4` commits YES on an item but `bf16` commits NO, the rungs are not scoring the same event. Therefore:
1. **Report the commit-agreement rate** across rungs as a first-class result (it is itself a finding — "4-bit flips the answer on X% of items").
2. **Run the AUROC comparison on the intersection set** (items where all rungs commit the same token), so the precision effect is measured on matched events, not contaminated by answer-flips.

---

## 5. Pre-registered hypotheses (fixed thresholds)

- **H1 — invariance.** The winning ACE cell at `bf16` is the **same cell or same family** (`{bos_mass, v_norm_lastq_weighted, js, js_no_bos}`) **with the same sign** as at `nf4`. → morphology is a property of the computation, not the rounding.
- **H2 — monotone-or-flat.** `bf16` geom CI-lo ≥ `nf4` geom CI-lo − **0.05** (precision does not *hurt*; 0.05 is the noise band). Strong version: CI-lo non-decreasing nf4 → int8 → bf16.
- **H3 — the falsifier (pre-committed).** On any cell that is **deployable at nf4**, a **≥0.10 drop** in geom CI-lo from `nf4` → `bf16`, *or* a `bf16` CI-lo **≤0.55** (near chance), flags the nf4 signal as **quantization artifact** → method falsified *for that cell*. State it now so it can actually fail.

Dose corollary: if hidden-state cos(nf4, bf16) > 0.99 **and** the verdict is stable, the signal is robust to a *measured-small* perturbation — the strongest form of the result.

---

## 6. Run commands

Validate gate first (per rung), then both extracts on a pass. nf4 reuses existing artifacts (bare filenames); higher rungs write `…__<precision>` so nothing clobbers.

```
M=/Users/msrk/Library/Python/3.9/bin/modal
cd /Users/msrk/Documents/furnace-guard
# 7B, per rung r in {int8, bf16, fp32} (nf4 baseline already exists or rerun with --precision nf4):
$M run modal_app.py --model-id Qwen/Qwen2.5-7B-Instruct --task anli_r1 --mode validate --precision <r>
$M run modal_app.py --model-id Qwen/Qwen2.5-7B-Instruct --task anli_r1 --mode extract  --precision <r>
$M run modal_app.py --model-id Qwen/Qwen2.5-7B-Instruct --task triviaqa_paired --mode extract --precision <r>
# 32B confirm: same, r in {int8, bf16}; data files {anli_r1,triviaqa_paired}_n200.jsonl already on volume.
```

Artifacts land at `profiles_ext/<task>/Qwen2.5-7B-Instruct__<precision>.profile.json` (+ `.matrix.npz`), validate at `validate/<slug>__<precision>_<task>.json`. Each profile self-labels via `comparability.precision`.

---

## 7. Minimal first step

🚀 **Qwen2.5-7B, `anli_r1`, full `{nf4, int8, bf16, fp32}` ladder.** If `bf16` deployability ≥ `nf4` and the winner cell is stable, **H3 is dead** and the quantization-artifact objection is closed — for a few dollars. *Then* scale-confirm on 32B and write the results page.

See also: [[../references/commit-locus|commit-locus]] (which signal reads where), [[gemma-scale-extension-2026-06-18|scale extension]] (the byte-comparable axis this complements), [[summary]].
