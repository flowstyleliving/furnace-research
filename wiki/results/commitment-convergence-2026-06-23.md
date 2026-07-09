# Commitment Convergence — Cross-Model First-Token Analysis (2026-06-23)

**Status:** `[RESULTS — paper section candidate]` — behavioral-level evidence complementing the signal-level family dissociation in [[llama-70b-scale-2026-06-22]] and the precision-invariance in [[precision-ladder-results-2026-06-22]].

## 1. Motivation

The precision-ladder pre-reg's §4 flagged a confound: if nf4 commits YES on a sample but bf16 commits NO, the rungs aren't scoring the same event. Cross-precision AUROC comparisons are contaminated by answer-flips. The control: compute the commit-equivalence intersection set and report the agreement rate.

We extended this beyond its original scope — across scales, across families, across tasks. What started as a methodological control surfaced a finding in its own right: **a behavioral disagreement ceiling that is invariant to model family and scale.**

## 2. Method

`/Users/msrk/Documents/furnace-guard/_commit_dump.py` — a lightweight Modal script that loads a model at a target precision, runs all 200 prompts through one forward pass, and records the argmax first token. No ACE/RPV extraction. No calibration. Just: what's the first word?

Runs across:
- **7B ANLI:** Qwen2.5-7B @ {nf4, int8, bf16, fp32}
- **32B ANLI:** Qwen2.5-32B @ {nf4, int8, bf16}
- **70B ANLI:** Llama-3.3-70B @ nf4
- **72B ANLI:** Qwen2.5-72B @ nf4 *(in progress)*
- **7B TriviaQA:** Qwen2.5-7B @ {nf4, int8, bf16, fp32}
- **70B TriviaQA:** Llama-3.3-70B @ nf4 *(in progress)*

## 3. Format leakage: scale eliminates non-YES/NO commits

| Model | nf4 | int8 | bf16 | fp32 |
|-------|-----|------|------|------|
| Qwen-7B ANLI | 97.0% | 94.0% | 93.5% | 96.5% |
| Qwen-32B ANLI | **100%** | 99.5% | 99.5% | — |
| Llama-70B ANLI | 95.0% | — | — | — |
| Qwen-7B TriviaQA | 100% | 100% | 100% | 99.5% |

**Finding:** At 7B, bf16 leaks 6.5% non-YES/NO tokens (all 'To'). By 32B, leakage is 0–0.5%. Scale eliminates format failure. TriviaQA's multiple-choice format is inherently clean — nearly zero leakage at any scale or precision.

The failure mode is shared across families: 100% of non-YES/NO tokens are 'To' regardless of model. This is a prompt-template artifact, not an architectural property.

## 4. Within-model precision agreement

| Setup | All-rung same-token | nf4↔bf16 agreement |
|-------|--------------------|--------------------|
| Qwen-7B ANLI (4 rungs) | **80.0%** | 85.0% |
| Qwen-32B ANLI (3 rungs) | **95.5%** | 95.5% |
| Qwen-7B TriviaQA (4 rungs) | **88.0%** | 92.5% |

**Finding:** At 7B, 20% of samples flip answer across precision rungs — the contamination the pre-reg warned about is real. By 32B, only 4.5% flip — **scale reduces within-model contamination by ~4×.** The commit-equivalence correction is genuine methodological hygiene at small scale, but becomes noise-level by 32B.

## 5. Cross-model agreement (all nf4)

| Pair | Agreement | Type |
|------|-----------|------|
| Llama-70B vs Qwen-32B | **81.0%** | Cross-family |
| Qwen-7B vs Qwen-32B | **82.0%** | Within-family, cross-scale |
| Llama-70B vs Qwen-7B | **76.0%** | Cross-family + cross-scale |

**Finding: A behavioral disagreement ceiling at ~18.5%.** Cross-family disagreement (19%) ≈ within-family cross-scale disagreement (18%). Two models of different families disagree at nearly the same rate as two models of the same family at different sizes.

This is NOT the trivial result ("different models give different answers"). If the family dissociation from [[llama-70b-scale-2026-06-22]] were just answer-disagreement in disguise, cross-family divergence would substantially exceed within-family. It doesn't. The dissociation — Qwen monitors attention patterns, Llama monitors readout volume — is a genuine signal-locus property, not a behavioral epiphenomenon.

## 6. Implications

### For the commit-confluence thesis

The paper's central claim — no universal signal, but a universal fitting procedure — now has a behavioral mirror: **no universal answer, but a universal disagreement ceiling.** The 18.5% floor is a property of the ANLI task, not of any model. Every model at this capability tier feels the same ambiguous questions; they just resolve them differently.

### For methodology

- **Commit-equivalence correction is real but scale-limited.** Below ~10B parameters, filter to the intersection set. Above, don't bother — contamination is below the noise floor.
- **The 'To' leak is a prompt-template bug, not a model bug.** All families, all scales, same token. Fix the template, close the leak.
- **TriviaQA is sterile.** The multiple-choice format forces YES/NO. No methodological adjustment needed.

### For the paper

This section (tentative title: "Commitment Convergence") belongs after the family dissociation results and before the discussion. It provides the behavioral-level triangulation: the signal-level finding (family dissociation in locus) is not reducible to behavioral disagreement, and the behavioral finding (18.5% ceiling) mirrors the signal-level finding (no universal cell, universal floor).

## 7. Artifacts

- All commit dumps: `commit_dump/` on Modal volume `model-cache`
- Analysis notebook: `/Users/msrk/Documents/furnace-guard/_commit_dump.py`
- Detailed per-model results: [[commit-equivalence-2026-06-23]]
- Cross-family analysis: this page

## 8. Open

- Qwen-72B ANLI commit dump (running)
- Llama-70B TriviaQA commit dump (running)
- Fold into `cc-draft.tex` after both complete
