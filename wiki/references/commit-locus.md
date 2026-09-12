# Commit Locus Reference

**Last updated:** 2026-09-11 (code re-read; three positions, not two — see the revision note at the end)  
**Audience:** anyone reading or extending the commit-confluence pipeline — Claude, Codex, reviewers, future MK.  
**Status:** canonical. If you find a document that contradicts this, fix the document not this reference.

---

## The Two Loci

The commit-confluence panel reads signals at **two different computational instants**. They are not the same thing. Conflating them produces incorrect claims about what the panel measures.

| Locus | Position | What's happening | Signal families |
|-------|----------|-----------------|-----------------|
| **t=0** | Prefix-last token | The model has processed the prompt but has NOT generated anything yet. This is the *preparation* state — "how is the model routing attention before it commits?" | **ACE** (attention morphology) |
| **gen_step=1** | First generated token | The model has generated exactly one token. This is the *commit* state — "what happened in the residual stream and readout at the instant of commitment?" | **PRI** (null_ratio), **RPV** (late-window spectrum average), **Confidence** (`p_max` only) |

⚠️ **Refinement, 2026-09-11.** `surprise` does **not** belong to the gen_step=1 column. It is computed from the *prefix-last* distribution — the one the answer token is drawn from — so the panel reads at **three** positions, not two. See the per-family sections below.

### Why this matters

ACE at t=0 reads the model's "stance" — is it routing attention in a grounded way or a scattered way *before* answering?  
PRI/RPV at gen_step=1 read the model's "motion" — did the commit step push the hidden state along the readout direction or off-axis?

**A signal that works at t=0 may not work at gen_step=1, and vice versa.** The panel includes both because they capture different failure modes. This is a feature, not a bug: it's *why* there's no universal champion (12 winners across 18 deployments come from both loci).

---

## Per-Family Mapping

### ACE — Attention Commitment Estimator
- **Locus:** t=0 (prefix-last token)
- **What it reads:** Attention weights at the last prompt position — before any generation.
- **Signals:** `bos_mass`, `v_norm_lastq_weighted`, `js`, `js_no_bos`, `js_kv_groups`
- **Code path:** `confluence_calibrator.py:330-381` → `pri_calibrator.py:592-606` (attention capture at step 0)
- **Sealed run:** `run_seal.py:5` explicitly states "t=0 attention morphology"

### PRI — Predictive Rupture Index (v3 null_ratio)
- **Locus:** gen_step=1 (first generated token)
- **What it reads:** Residual-stream motion at the commit instant — the fraction of Δh lying off the readout's top direction.
- **Signals:** `null_ratio`
- **Code path:** `confluence_calibrator.py:89-101` → `comprehensive_run.py:273-380` (trace_pair_features at gen_step=1)

### RPV — Readout Pseudo-Volume
- **Locus:** gen_step=1 (first generated token)
- **What it reads:** Spread/curvature of the **centered softmax-Fisher spectrum** — but ⚠️ **not of the readout distribution alone.** Each statistic is the **mean over the readout distribution and the logit-lens distributions of the last ⌈N/4⌉ blocks** (`agg[name] = mean(...)`), each computed on the top-512-probability support. The readout-only values are banked alongside but are **not** what the selector sees.
- **Signals:** `fisher_eff_rank`, `spectral_entropy`, `neg_shadow_logvol_r1`
- **Code path:** `comprehensive_run.py` `trace_pair_features` (`_spectrum_stats`, `_support_spectrum`, `fc_full_spectrum`) — the aggregate is built at lines ~416–490; `diagnostics.feature_locus` states it in one line.

### Confidence — ⚠️ two different positions
- **`surprise`** — **Locus: prefix-last.** `-log p(answer token)` under the distribution at the last prompt position, i.e. the distribution the token is actually drawn from. Under greedy decoding this equals `-log max p`, so it *is* the answer's own confidence.
- **`p_max`** — **Locus: gen_step=1.** The maximum probability of the distribution at the *answer token's own position*, which predicts the token that would **follow** the answer. It is therefore **not** the answer's confidence.
- **Code path:** `pri_runtime.py` `trace_sample`: the token is chosen from the prefix-last logits and its surprise recorded (~lines 990–1004); the token is then appended and a further forward pass produces `gen_probs[0]` (~lines 1114–1118), which is what `p_max` and the RPV spectrum read.

---

## The Fusion Aggregate

The `fusion_rank_mean_geom` signal averages rank-transformed signals from **both loci** (one representative per family: ACE, PRI, RPV). This is why it's the universal floor candidate — it pools information from both the preparation state (t=0) and the commit state (gen_step=1). Variance reduction through cross-locus averaging.

---

## Common Confusions (and Corrections)

| ❌ Wrong | ✅ Correct |
|---------|-----------|
| "All four families are read at gen_step=1" | ACE is t=0; PRI/RPV/Confidence are gen_step=1 |
| "The commit instant is step 0" | Two different instants: preparation (t=0) and commitment (gen_step=1) |
| "ACE reads attention at the commit moment" | ACE reads attention *before* the commit — at the prefix-last token |
| "P3 can detect hallucination at token 1" | P3 reads the first generated token's state to *predict* eventual short-answer correctness. Whether token 1 is the answer-commit token depends on the model's format convention. |
| "RPV reads the readout distribution" | RPV reads a **mean over the readout and the last ⌈N/4⌉ blocks' logit-lens distributions**. Saying "readout" alone understates what enters the column. |
| "`surprise` and `p_max` are both gen_step=1" | `surprise` is prefix-last; only `p_max` is gen_step=1. They are not the same quantity at the same instant. |
| "`p_max` is the model's confidence in its answer" | `p_max` is the confidence of the distribution *after* the answer token, i.e. about what follows it. The answer's own confidence is carried by `surprise`. |
| "The panel can flag an answer before the model picks it" | Only ACE and `surprise` precede selection. `null_ratio`, RPV and `p_max` require the answer token to have been chosen and fed back, so a detector using them is a **one-token guard**, not a pre-selection predictor. |

---

## Paper Language Guidance

When writing about the panel:

- Use **"commit-moment"** as the umbrella term for both loci
- Use **"t=0"** or **"prefix-last"** for ACE specifically
- Use **"gen_step=1"** or **"first generated token"** for PRI/RPV/Confidence
- Never say **"step 0"** to describe the whole panel — it's only correct for ACE
- Never say **"the commit position"** for the whole panel either (corrected 2026-09-11): attention and `surprise` are read before the answer token is chosen, the rest after it is fed back. `cc-draft.tex`'s glossary caption and Appendix A now state all three positions explicitly.

---

## Code Audit (verified 2026-06-20)

Confirmation from actual code:

```
ACE:          confluence_calibrator.py:330-381 → pri_calibrator.py:592-606
              Captures attention at the prefix-last position (step 0).
              run_seal.py:5: "t=0 attention morphology"

PRI/RPV:      confluence_calibrator.py:89-101 → comprehensive_run.py:273-380
              trace_pair_features generates one token, reads features at gen_step=1.
              benchmark arg is print-only at :321.

Confidence:   Same gen_step=1 logits — surprise = -log(p_max) of the first generated token.
```

**If you find code that contradicts this mapping, trust the code and update this document.**

---

## Revision note — 2026-09-11

Re-read against the code while making `cc-draft.tex` self-contained; verified independently by a Codex
`gpt-6-astra` static audit (CONFIRMED on every point below). Three corrections to this page, none of
which moves a registered verdict:

1. **RPV is a late-window average**, not a readout-only statistic. The banked column averages the
   readout with the logit-lens distributions of the last ⌈N/4⌉ blocks.
2. **`surprise` is read at the prefix-last position**, not at gen_step=1. The panel therefore reads at
   three positions, and this page previously said two.
3. **`p_max` is not the answer's confidence.** It is the maximum probability of the distribution at the
   answer token's own position, which predicts the *next* token.

Also noted, not fixed here because the file is vendored and must not be edited: the run diagnostics
string in `comprehensive_run.py` (~line 527) calls the null-ratio core "centered-Fisher". It is
**uncentered** (`A = sqrt(diag p)·W_u`, top-256 support, `v3_capture_centered=False`). The string is
wrong; the computed value matches what PRI reports.
