# Commit Locus Reference

**Last updated:** 2026-06-20  
**Audience:** anyone reading or extending the commit-confluence pipeline — Claude, Codex, reviewers, future MK.  
**Status:** canonical. If you find a document that contradicts this, fix the document not this reference.

---

## The Two Loci

The commit-confluence panel reads signals at **two different computational instants**. They are not the same thing. Conflating them produces incorrect claims about what the panel measures.

| Locus | Position | What's happening | Signal families |
|-------|----------|-----------------|-----------------|
| **t=0** | Prefix-last token | The model has processed the prompt but has NOT generated anything yet. This is the *preparation* state — "how is the model routing attention before it commits?" | **ACE** (attention morphology) |
| **gen_step=1** | First generated token | The model has generated exactly one token. This is the *commit* state — "what happened in the residual stream and readout at the instant of commitment?" | **PRI** (null_ratio), **RPV** (readout spread), **Confidence** (surprise, p_max) |

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
- **What it reads:** Spread/curvature of the softmax readout distribution at the commit instant.
- **Signals:** `fisher_eff_rank`, `spectral_entropy`, `neg_shadow_logvol_r1`
- **Code path:** Same as PRI — read from the gen_step=1 logits and hidden state.

### Confidence
- **Locus:** gen_step=1 (first generated token)
- **What it reads:** The model's own output probability distribution.
- **Signals:** `surprise`, `p_max`

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

---

## Paper Language Guidance

When writing about the panel:

- Use **"commit-moment"** as the umbrella term for both loci
- Use **"t=0"** or **"prefix-last"** for ACE specifically
- Use **"gen_step=1"** or **"first generated token"** for PRI/RPV/Confidence
- Never say **"step 0"** to describe the whole panel — it's only correct for ACE
- The glossary in `cc-draft.tex` Table 1 should say "commit position" not "step 0" for all signals, with a footnote distinguishing the two loci

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
