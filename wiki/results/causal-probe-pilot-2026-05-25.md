---
status: OPEN
kind: step4-causal-probe-pilot
date: 2026-05-25
---
# Causal Probe Pilot — Step 4 (2026-05-25)

**Status:** `[OPEN]` — exploratory pilot; no sealed pre-reg; findings descriptive only.
**Companion:** [[step0-belief-readout-2026-05-17]] (belief-readout panel for same model)
**Ref:** [[v3-main-run]] (Mistral-7B sealed E18 winner: `null_ratio_post_rank1`)

## Intervention design

**Target model:** `mlx-community/Mistral-7B-Instruct-v0.3-4bit` (32 layers, D=4096, V=32768)
**Data:** ANLI R1 n=200 slice (data_hash `b626514...`) — 20 label=0 (entailment, YES expected) + 20 label=1 (contradiction, NO expected)

**Patch:** at the last prefix position (commit step), add `alpha * v_top` to the post-norm hidden state before the unembedding:
```
h_commit_post  = RMSNorm(h_commit_pre, γ)
logits_patched = W_u · (h_commit_post + alpha · v_top)
committed_tok  = argmax(logits_patched)
```
where `v_top` = top-1 right singular vector of `sqrt(p_commit) · W_u` restricted to top-256 probability tokens (same support as `null_ratio_and_energy` at rank=1).

**Alpha sweep:** −100, −50, −20, −10, −5, −2, 0, +2, +5, +10, +20, +50, +100

**Zero-alpha unit test (mandatory pre-flight):** alpha=0 must reproduce byte-identical original committed token. ✅ **Passed** on first sample.

## Per-group statistics

| Group | n | Orig answer (YES/NO/OTHER) | Mean logit gap | Mean delta_logit_from_v_top |
|---|---|---|---|---|
| label=0 (control, entailment) | 20 | 14 YES / 6 NO / 0 OTHER | **2.49** (std 1.21) | −0.072 (std 0.23) |
| label=1 (contradiction) | 20 | 5 YES / 15 NO / 0 OTHER | **3.21** (std 0.67) | −0.126 (std 0.22) |

`delta_logit_from_v_top` = `(W_u · v_top)[orig_token]` — how much +v_top changes the committed token's own logit. Negative on 13/20 L0 and 15/20 L1 (v_top slightly hurts the committed token in both groups, consistent with v_top being the "most disruptive" direction).

## Semantic flip rates (YES↔NO boundary crossing only)

*Semantic flip = orig_answer is YES or NO, patched_answer is YES or NO, and they differ. Token-only flips (NO→No) excluded.*

| alpha | L0 sem-flip (n=20) | L1 sem-flip (n=20) | Δ (L1−L0) |
|---|---|---|---|
| −100 | 5/20 = 0.25 | 2/20 = 0.10 | −0.15 |
| −50  | 4/20 = 0.20 | 1/20 = 0.05 | −0.15 |
| −20  | 3/20 = 0.15 | 0/20 = 0.00 | −0.15 |
| −10  | 3/20 = 0.15 | 0/20 = 0.00 | −0.15 |
| −5   | 3/20 = 0.15 | 0/20 = 0.00 | −0.15 |
| −2   | 3/20 = 0.15 | 0/20 = 0.00 | −0.15 |
| 0    | 0/20 = 0.00 | 0/20 = 0.00 | 0 |
| +20  | 1/20 = 0.05 | 3/20 = 0.15 | +0.10 |
| **+50**  | **2/20 = 0.10** | **8/20 = 0.40** | **+0.30** |
| **+100** | **4/20 = 0.20** | **9/20 = 0.45** | **+0.25** |

## Interpretation `[OPEN]`

### The cleaner finding: +v_top semantic flip asymmetry (α=50–100)

At alpha=+50: L1 (contradiction) semantic flip rate **0.40** vs L0 (control) **0.10** (Δ=0.30).

L1 has a *larger* mean logit gap (3.21 vs 2.49) — making L1 tokens nominally *harder* to flip — yet L1 flips semantically at 4× the rate of L0 under +v_top. This asymmetry cannot be explained by logit gap alone.

Candidate explanation (consistent with v3 geometry): contradiction samples have high `null_ratio_post_rank1` — their hidden state change dh_post is mostly OUTSIDE the Fisher top-1 direction v_top. Perturbing the prefix hidden state along +v_top therefore creates an unusual configuration for contradiction samples (they've never committed in the v_top direction), making their YES/NO boundary more susceptible to v_top steering.

### The confounded finding: −v_top asymmetry

At alpha=−2 to −10: L0 semantic flip rate 0.15, L1 0.00.

**Confound:** L0 has smaller mean logit gap (2.49 vs 3.21). The 3 L0 samples that flip at alpha=−2 all have tiny gaps (0.03–0.31) — they are borderline cases that would flip under any moderate perturbation. Cannot cleanly attribute to the v3 geometry.

### Pre-reg constraint (must state)

This is descriptive pilot data. No pre-registered bars exist; no bootstrap CIs computed. The n=20/20 split and orig_answer imbalance (L0: 14 YES, 6 NO vs L1: 5 YES, 15 NO) are additional confounds. A clean causal test would require:
- Matched logit-gap sampling (same mean gap by label)
- Balanced orig_answer distributions
- Sealed pre-reg + bootstrap CI

**Verdict: non-null signal in the +v_top direction. Confound-mitigation needed before any `[VALIDATED]` claim.**

## Artifacts (repo)

- `experiments/causal-probe/2026-05-25/main.json` — full n=40 results
- `experiments/causal-probe/2026-05-25/pilot_v2.json` — n=5 pilot (unit test + inspection)
- `experiments/causal-probe/2026-05-25/main.log` — run log
- `scripts/causal_probe_rupture_steer.py` — intervention script

## Propagates to / read alongside

- [[v3-main-run]] — Mistral-7B sealed E18 winner (null_ratio_post_rank1 @ rank 1): the v3 metric whose geometry this probe is testing causally
- [[step0-belief-readout-2026-05-17]] — t=0 first-token-logit panel; Mistral-7B is a validity anchor
- [[triviaqa-pilot-2026-05-25]] — Step 3 calibrator results; same panel model
- [[claims]] — causal-probe claim entry (after any future sealed pre-reg)
