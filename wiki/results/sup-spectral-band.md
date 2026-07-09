# SUP Spectral-Band Validation — Verdict Page

**Pre-plan reference:** [pri-v3-plan § Pre-plan](../pri-v3/pri-v3-plan.md#pre-plan-sup-spectral-band-validation-before-v3-build)
**Theory reference:** [sup/theory-notes § 2.2 — Fisher spectral band](../sup/theory-notes.md) — claim λ_max/λ_mean ∈ [10², 10⁴] at semantic layers.
**Script:** `PRI_at_commitment/scripts/sup_spectral_band.py`
**Raw:** `PRI_at_commitment/experiments/sup-spectral-band/2026-04-14/run-01/` (3 parquets, 1408 rows total)

Status: **RUN COMPLETE** (2026-04-14, 16 samples × 3 models × every layer).

---

## Verdict: `[SHIFTED]` (with strong caveat — borderline `[FALSIFIED]`)

The SUP-stated band `λ_max/λ_mean ∈ [10², 10⁴]` **does not hold as stated** in our Furnace measurement on these 4-bit MLX models:

- **Llama-3.2-3B**: log10(ratio) ∈ [1.47, 2.00] → entirely **below** the lower edge of the SUP band.
- **Mistral-7B-v0.3**: log10(ratio) ∈ [1.26, 1.77] → **decade below** the SUP band, no layer reaches 10².
- **Qwen2.5-7B**: log10(ratio) ∈ [1.89, 2.40] → grazes the lower edge of [10², 10⁴], peaks at ~250.

Peak depths disagree across architectures (Llama: 0.00, Mistral: 0.13, Qwen: 0.93). No interior unimodal peak shared cross-arch. Qwen's "in-band" reading is confounded by **entropy collapse** at late layers (see Critical Caveat below) and likely overstates the Fisher-geometric content.

The depth-profile *shape* exists (this is not random noise — within-sample IQR is tight, cross-layer variation is structured) but the *numerical band* and *characteristic depth* claims don't survive cross-architecture testing. We file this as `[SHIFTED]` rather than `[FALSIFIED]` only because the per-model profiles are coherent and reproducible; the SUP framing needs significant rework before it can be used as a v3 prior.

## Design (recap)
- n=4/cell × 4 cells = 16 puzzles, shared across models (seed=42).
- Step 1 (first generated token = commitment).
- Every transformer block.
- Top-256 W_u rows under per-layer logit-lens p^(ℓ) = softmax(W_u · h_ℓ).
- SVD of `A = sqrt(p_s)[:,None] · W_s`; λ = S².

## Per-Model Results (layer-wise medians)

### Llama-3.2-3B-Instruct-4bit (28 layers)
| Depth | layer | median λ_max/λ_mean | log10 | ε(16) | ε(32) | entropy | top1 |
|-------|------:|--------------------:|------:|------:|------:|--------:|-----:|
| 0.00  | 0     | **98.98**           | 2.00  | 0.631 | 0.723 | 11.76   | 1.7e-5 |
| 0.30  | 8     | 29.44               | 1.47  | 0.278 | 0.381 | 11.75   | 1.4e-5 |
| 0.59  | 16    | 38.36               | 1.58  | 0.387 | 0.493 | 11.73   | 5.3e-5 |
| 0.89  | 24    | 43.88               | 1.64  | 0.543 | 0.651 | 11.55   | 2.0e-3 |
| 0.96  | 26    | **61.91**           | 1.79  | 0.663 | 0.767 | 10.88   | 0.018 |
| 1.00  | 27    | 57.12               | 1.76  | 0.643 | 0.754 |  7.87   | 0.075 |

Profile: high at edges, dip at depth ~0.30, modest rise toward end. Peak at depth 0.00 (likely an embedding artifact — pre-attention layer norm dominates).

### Mistral-7B-Instruct-v0.3-4bit (32 layers)
| Depth | layer | median λ_max/λ_mean | log10 | ε(16) | ε(32) | entropy | top1 |
|-------|------:|--------------------:|------:|------:|------:|--------:|-----:|
| 0.00  | 0     | 55.29               | 1.74  | 0.324 | 0.406 | 10.40   | 3.1e-5 |
| 0.13  | 4     | **59.49**           | 1.77  | 0.333 | 0.413 | 10.40   | 3.1e-5 |
| 0.45  | 14    | 32.03               | 1.51  | 0.238 | 0.331 | 10.40   | 3.3e-5 |
| 0.77  | 24    | 58.60               | 1.77  | 0.348 | 0.430 | 10.40   | 5.0e-5 |
| 0.94  | 30    | 19.48               | 1.29  | 0.317 | 0.444 | 10.38   | 1.0e-4 |
| 1.00  | 31    | 24.32               | 1.39  | 0.329 | 0.450 | 10.38   | 1.8e-4 |

Profile: U-shape with shallow peak (layer 4) and a second hump near layer 24, then collapses at the very end. **Never enters [10², 10⁴].** Notable: entropy is essentially flat at 10.40 across all layers — Mistral's logit-lens distribution barely changes per layer, suggesting the layer-projection is weakly informative.

### Qwen2.5-7B-Instruct-4bit (28 layers)
| Depth | layer | median λ_max/λ_mean | log10 | ε(16) | ε(32) | entropy | top1 |
|-------|------:|--------------------:|------:|------:|------:|--------:|-----:|
| 0.00  | 0     | 88.72               | 1.95  | 0.510 | 0.582 | 11.90   | 2.4e-5 |
| 0.30  | 8     | 112.79              | 2.05  | 0.636 | 0.706 | 11.10   | 1.3e-3 |
| 0.52  | 14    | 119.00              | 2.08  | 0.770 | 0.831 |  8.48   | 0.032 |
| 0.74  | 20    | 139.92              | 2.15  | 0.895 | 0.933 |  4.43   | 0.250 |
| 0.85  | 22    | 188.50              | 2.28  | 0.970 | 0.985 |  2.19   | 0.541 |
| 0.93  | 25    | **249.92**          | 2.40  | 1.000 | 1.000 |  0.14   | 0.970 |
| 1.00  | 27    | 174.57              | 2.24  | 0.995 | 0.999 |  1.35   | 0.654 |

Profile: monotonic rise to depth 0.93, then small dip at final layer. **Inside the lower edge of [10², 10⁴].** But ε(16) = 1.000 and entropy ≈ 0.14 at the peak means the distribution is essentially one-hot — see Critical Caveat.

## Cross-Model Comparison

| Model    | log10(ratio) range | peak depth | peak ratio | peak entropy |
|----------|--------------------|-----------:|-----------:|-------------:|
| Llama 3B | [1.47, 2.00]       | 0.00       | 98.9       | 11.76        |
| Mistral 7B | [1.26, 1.77]     | 0.13       | 59.5       | 10.40        |
| Qwen 7B  | [1.89, 2.40]       | 0.93       | 249.9      | 0.14         |

**No cross-model agreement** on either the numerical band or the depth-profile shape. The peak-depth divergence (0.00 / 0.13 / 0.93) is the most striking finding — it directly contradicts E21's "characteristic depth is architecturally universal" framing in the v3 plan.

## ⚠ Critical Caveat — Qwen's high ratio is entropy-collapse-driven

At Qwen's peak layer (25), p^(ℓ) is nearly one-hot (top1 = 0.97, entropy = 0.14, ε(16) = 1.000). When `p_s` concentrates on one token, `A = sqrt(p_s)[:,None] · W_s` becomes near-rank-1 by construction — **not** because the underlying Fisher geometry has rich structure, but because one row dominates the weighting. λ_max/λ_mean ≈ 250 reflects "p is one-hot," not "the layer has a 2-decade Fisher-spectrum-rich semantic representation."

Where p^(ℓ) is more spread (Llama, Mistral, Qwen's earlier layers), entropy is high and ratios are correspondingly lower. **The metric is being driven primarily by p^(ℓ) sharpness, not by W_u geometry.** This is an artifact of the support-truncated SVD formulation, and the SUP claim — even if it holds in some other framing — does not survive this specific operationalization.

## Implications for v3 plan

Updates to file in `pri-v3-plan.md`:
1. **Drop E20 in its current form** ("spectrum decay calibrates v3 rank choice"). The spectrum is dominated by p_t sharpness, so r doesn't carry the SUP-intended meaning here.
2. **Drop E21's "universal characteristic depth" prior.** Peak depths span 0.00 → 0.93. There is no shared layer-of-interest across architectures.
3. **Re-frame v3 around a sharpness-aware metric.** Either:
   - (a) Normalize λ_ratio by p^(ℓ) entropy or top1, or
   - (b) Switch to a Fisher pullback that doesn't degenerate as p concentrates (e.g., use `p^α` for some α < 1 to soften the weighting before SVD).
4. **Per-layer logit-lens (Option B) is now strongly disfavored** until the entropy-collapse confound is addressed. The Option-A single-final-p formulation may be safer because the final p is the actual generative distribution (committed), not a layer-internal proxy.
5. **The depth profile per architecture is real and reproducible** — it can still serve as a diagnostic, just not as a SUP-prior-driven design choice.

## Caveats (still applicable)

- Support truncation to 256 rows: null-space measured relative to that subset, not the full vocab.
- 4-bit quantization of W_u may compress the singular value dynamic range, especially the tail (lowering λ_mean and inflating λ_max/λ_mean). Worth re-running on at least one fp16 model to bound this.
- Logit-lens p^(ℓ) is under-calibrated at non-final layers — confirmed: Mistral's entropy is flat across all layers (10.40), Llama and Qwen show progressive sharpening.

## ⚠ Critical Caveat 2 — Architectural mismatch (encoder → decoder)

The SUP band calibration (`λ_max/λ_mean ∈ [10², 10⁴]`, middle-layer semantic peak) was derived on **encoder / similarity-tuned sentence-transformers**: mpnet, MiniLM, BERT, RoBERTa — bidirectional attention, MLM / contrastive objectives, symmetric information flow with a mid-depth semantic bottleneck. Furnace ran the validation on **decoder-only causal LMs** (Llama 3B, Mistral 7B, Qwen 2.5 7B): causal masking, autoregressive next-token objective, monotonic information buildup toward the unembedding.

These are not the same Fisher geometry. An encoder's middle-layer peak is structural (that's where the sentence representation lives); a causal decoder's representations are built progressively and the "semantic peak" is pushed later, distributed, or absent as a single feature. Expecting the same band and the same depth profile across this architectural boundary was optimistic.

This re-reads the verdict: much of what we called `[SHIFTED]` / borderline `[FALSIFIED]` may instead be **"SUP not ported to decoders."** The within-architecture profiles we did find (coherent, reproducible, per-model) are what decoder Fisher geometry actually looks like — not a failure of SUP, but SUP-on-wrong-architecture. A clean test requires running the same pipeline on at least one encoder (e.g., all-mpnet-base-v2) to confirm we can reproduce the encoder-side band before declaring the decoder result a contradiction.

**Action.** Before v3 cites E20/E21 as either supported or refuted, add an encoder control run. If the band shows up cleanly on mpnet and not on Llama/Mistral/Qwen, we have a clear architecture-gated claim. If it doesn't show up on mpnet either, then the SUP numbers themselves don't survive independent replication.

## Log

- 2026-04-14 · scaffolded · pre-plan filed, script drafted.
- 2026-04-14 · executed · 16 samples × 3 models × every layer; parquets written.
- 2026-04-14 · verdict filed · `[SHIFTED]` borderline `[FALSIFIED]`. Cross-arch peak-depth disagreement (0.00/0.13/0.93) and Qwen entropy-collapse confound noted. v3 priors updated accordingly.
- 2026-04-15 · caveat added · architectural mismatch (SUP calibration is encoder / sentence-transformer, Furnace run is decoder-only causal LM). Verdict re-reads as "SUP not ported to decoders" pending an encoder control run.
