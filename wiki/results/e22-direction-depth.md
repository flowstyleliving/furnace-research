# E22 — Direction-Depth Signature Gate (Verdict)

**Pre-plan reference:** [pri-v3-plan.md § E22](../pri-v3/pri-v3-plan.md#pre-registered-experiments)
**Script:** `PRI_at_commitment/scripts/e22_direction_depth.py`
**Raw:** `PRI_at_commitment/experiments/e22-direction-depth/2026-04-16/run-01/` (3 parquets, 1408 rows total)
**Branch:** `v3-build` @ `fa87ac5`

Status: **RUN COMPLETE** (2026-04-16, 16 samples × 3 models × every layer × 4 ranks, \~50s wall).

> **🔄 Qwen result superseded 2026-04-18** by Prereq 8 step 1 (`scripts/prereq8_qwen_primary_gate.py`, post-E23 final-norm fix). On the normed Option A path, Qwen shows late-rise at layer 27, max |dev from baseline 0.9955| = **0.0302** (vs the original un-normed read: flat, layer 14 −0.009 / layer 13 −0.020). The 2026-04-16 Qwen verdict ("flat ≈ random") was a final-norm artifact — same bug class as E23's Llama layer-0 spike. Llama and Mistral rows below are unaffected (their E22 reads already matched production up to the same norm issue, which mattered mainly at layer 0; the late-rise peaks stood). The cross-arch framing of this page is updated to "magnitudes differ, shapes converge" — Qwen's section (and the original sparse-vs-dense correction) is preserved for traceability but no longer the canonical direction-depth claim. Canonical Qwen artifact: `PRI_at_commitment/experiments/prereq8-qwen-gate/2026-04-18/run-02/`.

---

## Verdict: `[PARTIAL STRUCTURE]` — gate passes "keep every-layer density"

`null_ratio_ℓ` shows **per-architecture depth structure** in 2/3 models (Llama, Mistral) and a **null-flat profile** in Qwen that is itself structured (structurally distinct, not noise). Cross-arch universality of depth — as expected from the spectral-band precedent — does **not** hold.

**Gate decision:** retain the every-layer × 12-step capture schedule for the v3 main run. Narrowing to 5 probe layers would erase the late-rise resolution that Llama / Mistral show clearly, and would miss Qwen's structurally-flat counter-signal entirely.

## The random-projection baseline (essential read)

For rank `r = 32` and random Δh in hidden-dim `d`, the expected `null_ratio` is `√((d−r)/d)`:

| Model      | d    | random-baseline `null_ratio_rank32` |
|------------|-----:|------------------------------------:|
| Llama 3B   | 3072 | **0.9948** |
| Mistral 7B | 4096 | **0.9961** |
| Qwen 7B    | 3584 | **0.9955** |

Most `null_ratio` values sit within 0.005 of this baseline. **Interpret deviations from baseline, not absolute values.** A layer at baseline means Δh is random w.r.t. the final-p informed subspace; a layer below baseline means Δh has informed-direction content.

## Per-model profiles (deviation from random baseline; rank 32)

### Llama-3.2-3B-Instruct-4bit (28 layers)

| layer | depth | null_ratio (control) | dev. from rand | null_ratio (contradiction) | diff c−ctrl |
|------:|------:|---------------------:|---------------:|---------------------------:|-------------:|
| 0     | 0.00  | 0.9941 | −0.0007 | 0.9934 | −0.0007 |
| 11    | 0.41  | 0.9939 | −0.0009 | 0.9936 | −0.0004 |
| 17    | 0.63  | 0.9919 | −0.0029 | 0.9906 | −0.0012 |
| 20    | 0.74  | 0.9843 | −0.0105 | 0.9805 | −0.0038 |
| 23    | 0.85  | 0.9796 | −0.0152 | 0.9760 | −0.0036 |
| 26    | 0.96  | 0.9623 | **−0.0325** | 0.9613 | −0.0010 |
| 27    | 1.00  | 0.9406 | **−0.0541** | 0.9432 | +0.0025 |

**Shape: late-rising monotonic.** Informed-direction content emerges past layer 17 (depth \~0.6) and accelerates into the final layer. Peak informed content at the final layer (dev −0.054). Contradiction-vs-control split: max |diff| = 0.0046 at layer 19, mean = −0.001. **No meaningful separation at n=4.**

### Mistral-7B-Instruct-v0.3-4bit (32 layers)

| layer | depth | null_ratio (control) | dev. from rand | null_ratio (contradiction) | diff c−ctrl |
|------:|------:|---------------------:|---------------:|---------------------------:|-------------:|
| 0     | 0.00  | 0.9952 | −0.0009 | 0.9960 | +0.0008 |
| 11    | 0.35  | 0.9933 | −0.0028 | 0.9931 | −0.0001 |
| 17    | 0.55  | 0.9870 | −0.0091 | 0.9894 | +0.0024 |
| 20    | 0.65  | 0.9779 | −0.0182 | 0.9816 | +0.0037 |
| 23    | 0.74  | 0.9807 | −0.0154 | 0.9839 | +0.0032 |
| 26    | 0.84  | 0.9709 | **−0.0252** | 0.9768 | +0.0059 |
| 29    | 0.94  | 0.9750 | −0.0211 | 0.9783 | +0.0033 |
| 31    | 1.00  | 0.9550 | **−0.0411** | 0.9524 | −0.0027 |

**Shape: U-shape with late-rise + final crash.** Informed content builds from layer 17, peaks at layer 26 (dev −0.025), slight rebound, then the final layer drops sharply (dev −0.041). **Directional split contradiction > control at mid-late layers** (mean +0.0014, max +0.0098 at layer 24) — consistent with "contradictions put *more* Δh into informed directions" but too small at n=4 to claim significance.

### Qwen2.5-7B-Instruct-4bit (28 layers)

> **Correction 2026-04-16 (step-1 rank-sweep follow-up):** the original table below displayed a sparse layer sample (0/14/20/23/27) and *missed layer 13*, which is actually Qwen's argmin. Full-layer re-analysis corrected table shown first; original sparse-sample table preserved below it.

**Corrected per-layer table (all 28 layers, rank 32, sample-mean per cell):**

| layer | depth | null_ratio (control) | dev. from rand | null_ratio (contradiction) | diff c−ctrl |
|------:|------:|---------------------:|---------------:|---------------------------:|-------------:|
| 0     | 0.00  | 0.9971 | +0.0016 | 0.9953 | −0.0019 |
| 2     | 0.07  | 0.9883 | −0.0073 | 0.9940 | +0.0058 |
| 9     | 0.33  | 0.9900 | −0.0056 | 0.9907 | +0.0007 |
| 12    | 0.44  | 0.9876 | −0.0079 | 0.9881 | +0.0005 |
| **13** | **0.48** | **0.9754** | **−0.0202** | **0.9786** | +0.0033 |
| 14    | 0.52  | 0.9866 | −0.0089 | 0.9894 | +0.0028 |
| 15    | 0.56  | 0.9835 | −0.0120 | 0.9888 | +0.0052 |
| 20    | 0.74  | 0.9934 | −0.0021 | 0.9949 | +0.0015 |
| 27    | 1.00  | 0.9921 | −0.0035 | 0.9872 | −0.0048 |

**Shape (corrected): mid-depth informed peak at layer 13 (depth 0.48).** Qwen *does* carry informed-direction content, but concentrated in a narrow mid-depth window (layers 13–15) rather than at the final layer like Llama/Mistral. Layer-13 control dev = −0.020 is 2.25× layer 14's value and about 40% of Mistral's final-layer peak dev (−0.041). **It is not "flat everywhere"** — the sparse-sample display in the original verdict missed the peak. Rank sweep (r ∈ {8, 16, 32, 64}) on existing parquet shows the layer-13 structure is stable across ranks (ratio r64/r32 = 1.03, well under the 2.0 escalation threshold), so this is not a rank-compression artifact — it's a genuine mid-depth signature that differs in *shape* (not only magnitude) from Llama/Mistral.

**Original sparse-sample table (preserved for provenance):**

| layer | depth | null_ratio (control) | dev. from rand | null_ratio (contradiction) | diff c−ctrl |
|------:|------:|---------------------:|---------------:|---------------------------:|-------------:|
| 0     | 0.00  | 0.9971 | +0.0016 | 0.9953 | −0.0019 |
| 14    | 0.52  | 0.9866 | −0.0089 | 0.9894 | +0.0028 |
| 20    | 0.74  | 0.9934 | −0.0021 | 0.9949 | +0.0015 |
| 23    | 0.85  | 0.9964 | +0.0009 | 0.9970 | +0.0005 |
| 27    | 1.00  | 0.9921 | −0.0035 | 0.9872 | −0.0048 |

Original characterization was **"Shape: ≈random everywhere"** — superseded by the corrected reading above.

## Cross-architecture comparison

| Model    | shape                             | peak informed-layer (dev from rand) | Δ_final (dev)     |
|----------|-----------------------------------|-------------------------------------|-------------------|
| Llama 3B | monotonic late-rise               | layer 27 / depth 1.00 (**−0.054**)  | −0.054            |
| Mistral 7B | late-rise with final crash       | layer 31 / depth 1.00 (**−0.041**)  | −0.041            |
| Qwen 7B  | mid-depth informed peak (corrected) | layer 13 / depth 0.48 (**−0.020**)  | −0.003            |

**Partial cross-arch agreement.** Llama and Mistral share the late-rising-into-informed shape (peak deviation at the final layer, both ≥ 0.04). **Qwen differs in shape, not absence:** informed-direction content concentrates in a narrow mid-depth window (layer 13, depth 0.48, dev −0.020) rather than at the final layer. The per-arch signatures are now all real but none match — Llama and Mistral share *where* the informed content lives; Qwen has its own mid-depth signature. Consistent with (but does not reduce to) Qwen's spectral-band anomaly: the final-p eigenspace differs structurally there too.

## Relation to the 2026-04-14 spectral-band run

`λ_max/λ_mean` (spectral band) peak depths were **0.00 / 0.13 / 0.93** (Llama / Mistral / Qwen).
`null_ratio` informed-content peak depths are **1.00 / 1.00 / 0.52** (Llama / Mistral / Qwen).

These are different depths because the two metrics probe different things:
- `λ_max/λ_mean` = *eigenvalue-magnitude* observable on `sqrt(p^ℓ) · W_u` — dominated by `p^(ℓ)` sharpness (the entropy-collapse confound).
- `null_ratio_ℓ` = *projection* observable on `Δh_ℓ` into the single final-p eigenspace — insensitive to per-layer p sharpness; sensitive to Δh direction.

The E22 hypothesis — that `null_ratio` would reveal cross-arch structure the spectral ratio could not — **partially holds**: Llama and Mistral now agree on shape (late-rise) where their spectral peaks disagreed (0.00 vs 0.13). Qwen still doesn't match.

## What this means for v3

1. **Keep every-layer capture at steps 1–12.** The per-model depth structure is real (tight IQRs, reproducible shape) and requires ≥ 8 layers to resolve. Narrowing would erase Llama and Mistral's late-rise and Qwen's flat-profile counter-signal.
2. **Expect Qwen to be the outlier.** Qwen's `null_ratio` barely leaves the random-baseline band. Either (a) Qwen's Δh genuinely doesn't align with final-p directions (mechanistic difference), or (b) 4-bit quantization of `W_u` compresses the informed subspace in Qwen's vocab (152k, the largest of the three). Flag for v3 Analysis §: compare Qwen's `null_ratio` against other-rank cuts + fp16 control if feasible.
3. **Contradiction/control separation at n=4 is under-powered.** Max |diff| = 0.0098 on Mistral; Llama + Qwen noisy around zero. Do not draw any E18 conclusion from this run. The main v3 run at n=50/cell is needed for that.
4. **Random-baseline reporting is essential.** Raw `null_ratio ≈ 0.99` looks like "no signal" but is at baseline. All v3 plots should subtract the random baseline or use `1 − null_ratio` ("informed-direction fraction").
5. **The "argmax_depth" scalar (E21 primary) needs redefinition.** Current spec = "layer where `null_ratio_ℓ` first exceeds 1.5× prefix mean" assumes rising = bad. But here rising `null_ratio` = *more* null = *less* informed. For E21's argmax-depth to mean "where does Δh first enter the informed subspace", define it as argmin(`null_ratio_ℓ`) or argmax(`1 − null_ratio_ℓ`). Update the plan before the main run.

## Qwen quantization diagnostic — step 1 result (2026-04-16)

Per v3 plan Prerequisite 8, step 1 of the staged Qwen diagnostic runs on **existing E22 parquet** (no new compute). Question: does rank 64 reveal informed-direction content that rank 32 missed? Decision rule: escalate to step 2 iff `dev_r64 / dev_r32 > 2.0` at the argmin layer.

**Result.** At Qwen's argmin layer (layer 13, depth 0.48):

| rank | baseline √((d−r)/d) | null_ratio (sample-mean) | deviation |
|-----:|---------------------:|-------------------------:|-----------:|
| 8    | 0.998883             | 0.984606                 | −0.014277 |
| 16   | 0.997765             | 0.979123                 | −0.018642 |
| 32   | 0.995526             | 0.976980                 | −0.018546 |
| 64   | 0.991031             | 0.972008                 | −0.019023 |

Ratio r64 / r32 = **1.03** — far below the 2.0 escalation threshold. Rank compression is **not** the axis that explains Qwen's profile. The layer-13 structure is stable across ranks; expanding rank from 8 to 64 grows the deviation only from −0.014 to −0.019 (about 30%), i.e. all ranks see the same mid-depth signal at similar resolution.

**Secondary finding (worth escalating upstream).** The rank-sweep forced a full-layer re-read of the Qwen parquet and revealed that the original verdict-page table showed layers {0, 14, 20, 23, 27} — a sparse sample that *missed* layer 13, Qwen's actual argmin. The Qwen section and cross-arch table above have been corrected.

**Step-1 decision.**
- Rank hypothesis ruled out. **Do not escalate to step 2** (extended rank rerun r ∈ {32, 64, 128, 256}). It would most likely show the same \~−0.02 deviation at layer 13 and waste compute.
- Step 3 (fp16 Qwen replication) remains exactly where Prerequisite 8 placed it: **after main run**, conditional on reviewer pushback or on needing the "mechanistic vs quant" claim in text. Main run not blocked.

## Caveats

- n = 4/cell — exploratory only; no separation claim is tested here.
- `null_ratio` uses Option A eigenspace (single final-p SVD) per plan. Option C sharpness-aware variants not probed in this gate; filed for the next round.
- Support truncation = top-256 of `W_u` rows under final `p_t`; the "null space" is relative to that 256-row subspace, not the full vocab.
- 4-bit quantization compresses `W_u`'s singular spectrum; may amplify Qwen's flat signature. fp16 replication on at least one model is a standing open question.

## Log

- 2026-04-16 · pre-run · E22 filed per 2026-04-15 plan update; prerequisite 7.
- 2026-04-16 · run · `scripts/e22_direction_depth.py` on v3-build @ `fa87ac5`; 1408 rows in 50s.
- 2026-04-16 · verdict · `[PARTIAL STRUCTURE]`. Every-layer density retained. Qwen flagged as outlier; argmax_depth direction flipped in plan.
- 2026-04-16 · correction · Full-layer re-read during step-1 diagnostic found Qwen's actual argmin is **layer 13 (depth 0.48, dev −0.020)**, not the sparse-sample layer 14 (dev −0.009) originally displayed. "Flat ≈ random" characterization superseded by "mid-depth informed peak." Cross-arch table updated.
- 2026-04-16 · Qwen step-1 diagnostic · Rank sweep on existing parquet: r64/r32 dev ratio = 1.03 at layer 13 (threshold 2.0). Rank compression ruled out as explanation of Qwen's weaker magnitude. Step 2 **not** escalated; step 3 (fp16) deferred to post-main-run per Prerequisite 8.
- 2026-04-18 · supersession · Prereq 8 step 1 rebuilt Option A on the normed logit-lens path (post-E23 fix) and found Qwen late-rise at layer 27, max |dev| = 0.0302 — the 2026-04-16 "flat ≈ random" reading was a final-norm artifact. Qwen outlier flag lifted; within-species-uniformity candidate claim withdrawn. Prereq 8 steps 2–3 dropped as no longer required.
