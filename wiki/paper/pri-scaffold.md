# PRI v3 Paper — Draft Scaffold

_Status: `[SCAFFOLD + DRAFT]` — section structure + disclosure recipe + plot inventory + run pointers. End-to-end draft prose lives at [draft.md](pri-draft.md) (workshop length, ~8pp) — drafted 2026-04-27 against the n=150 powered numbers (run-09 + 2026-04-27/run-{01,02}). This scaffold remains the planning + figure-inventory + open-decisions doc; the draft is the prose._

_Created 2026-04-26 immediately after the J_n-corrected sealed verdict landed (E18 3/3 PASS, E17b PASS on Qwen 2.5). Draft started 2026-04-27 after the n=150 powered sweep landed and the Mistral-only Simpson's-paradox + 3-motif cross-architecture story crystallized._

## Working title (placeholder)

**Architecture-Dependent Fisher Pullback Geometry at the Commit Moment: A Sealed Pre-Registered Test on Synthetic Logical Contradictions**

(Working — likely revise. Keep "architecture-dependent" and "Fisher pullback" in any final title — they are the load-bearing scientific claims.)

## Headline claims (one-line each, to anchor every section against)

- 🎯 **E18 sealed gate (magnitude-independence): 3/3 primaries PASS** at the sealed analysis plane (final layer, gen_step=1, rank=1, residualized vs `d_F_lowrank32`). Powered n=600 reading (run-09): Llama 3.2 3B 0.8713 [0.842, 0.896], Mistral 7B 0.8707 [0.845, 0.897], Qwen 2.5 7B 0.6468 [0.603, 0.691]. Replicates the n=200 reading (run-02) with ~33% tighter CI as expected for 3× more data.
- 🎯 **E17b sealed gate (Fisher vs HARP raw): PASS on Qwen 2.5** at Δ AUROC = **+0.157 [+0.125, +0.190]** (powered n=600); replicates the n=200 reading (+0.149 [+0.100, +0.201]). Sealed +0.02 bar cleared by 7.9×. Fisher pullback discriminates contradictions in the predicted direction (AUROC 0.8967, sign +1); raw W_u SVD discriminates inverted (AUROC 0.7396, sign −1).
- 📐 **Cross-model picture is architecture-dependent on pooled n=600 — 6 models, all decisive at sealed-rank-1 with non-overlap CI, split 3 Fisher vs 3 Raw (oriented Δ AUROC, J_n-corrected post-norm geometry).** **Fisher decisive on pool (3):** Llama 3.2 3B (Δ=+0.272 [+0.222, +0.320]), Qwen 2.5 7B sealed (Δ=+0.157 [+0.125, +0.190] PASS), Gemma 3-4B (Δ=+0.210 [+0.181, +0.237]). **Raw decisive on pool (3):** Mistral 7B (Δ=−0.140 [−0.173, −0.107]), Qwen3 8B (Δ=−0.214 [−0.261, −0.175]), Phi-3.5-mini (Δ=−0.441 [−0.485, −0.392], largest margin, Raw=0.999 nearly-perfect). Cross-generation within Qwen-family (2.5 Fisher → 3 Raw) and within-vendor (Llama Fisher vs Mistral Raw) both flip; vendor and parameter-count are not predictive. **Raw native-sign axis at r=1:** sign +1 (Raw aligned) on Mistral and Phi; sign −1 (Raw inverted) on the other 4. Replicates the n=200 prelim verdict structure with tighter CIs.
- 🪡 **Chain-length stratification at well-powered n=300/stratum — Mistral is the only Simpson's-paradox case.** Five of six architectures keep their pooled E17b verdict at both chain-length strata (Llama, Qwen 2.5, Gemma 4B all Fisher-decisive at both; Qwen3, Phi all Raw-decisive at both). **Mistral alone** has a pooled Raw-decisive verdict (Δ=−0.140) that dissolves under stratification: cl=2 reads **Fisher decisive** (+0.065 [+0.041, +0.093]) and cl=5 reads **tied** (+0.002 [−0.022, +0.028]) — Mistral is **never Raw-decisive** at the stratum level. The pooled "Mistral Raw" verdict is a Simpson's-paradox artifact of mixing chain-length subgroups whose Fisher and Raw discrimination axes have different orientations relative to contradiction. The n=200 prelim's "Llama also flips" finding was finite-sample noise — at n=300/stratum Llama is clearly Fisher at both strata. **Universal pattern: |Δ| sharper at cl=2 than cl=5 across all 6 models** — short reasoning chains place the gen_step=1 commit closer to the contradiction; long chains diffuse the rupture across intermediate reasoning tokens.
- 🌀 **Operating-point sensitivity within a single model:** Gemma 3-4B is Fisher-decisive at sealed r=1 but Raw-decisive at r=32 (Δ=−0.383 [−0.464, −0.301]) — same direction as Mistral's pooled r=1 picture, demonstrating that the Fisher-vs-Raw verdict can flip across BOTH the rank sweep AND the chain_length axis within one model. Underwrites "audit the operating-point neighborhood before falsifying" across both axes.
- 🔧 **Methodological contribution: pre-registration + amendments timeline.** Sealed spec (analysis plane, residualization, bootstrap, threshold, 2-of-3 bar, no-post-hoc-re-spec) was preserved across multiple bug-fix cycles. Verdict integrity survived a coordinate-mismatch bug that flipped the E17b reading from −0.166 to +0.150 — the discipline machinery did its job.

## Section outline

### Abstract
~250 words. Anchor on the 4 headline claims. Lead with the cross-model architecture-dependence finding (most novel), close with the pre-registration governance (most defensible). Single-sentence bug-disclosure mention: "We identified and corrected a coordinate-mismatch in the Fisher pullback computation; sealed-spec discipline preserved verdict integrity across the correction."

### 1. Introduction
- 🌊 Hook: rupture geometry at the commit moment. Why gen_step=1 is the right analysis plane.
- 📐 Background: HARP's static W_u subspace; v2's `d_F` Fisher distance; v3's `null_ratio` as the off-commit-direction-energy fraction.
- 🎯 Contribution: sealed pre-reg test of v3 against HARP, on synthetic contradictions, across 3 architectures + 1 cross-generation companion + (optionally) 2 within-family-scale companions.
- 📋 Roadmap.

### 2. Related Work
- HARP (raw W_u SVD basis, anomaly detection). Cite + describe their static-subspace approach. Note the head-to-head we run.
- Information geometry on the simplex (Fisher metric, pullback through softmax∘W_u). Cite the foundational refs.
- LLM rupture / commit / surprise literature (PRI v1, v2, the SUP precursors if cited externally).
- Pre-registration in ML (sealed spec, no-p-hacking, recent push toward stronger evidentiary standards).

### 3. Methods
#### 3.1 Pre-registration & sealed spec
- Sealed analysis plane: final layer, gen_step=1.
- Sealed metric: `null_ratio_post_rank1` residualized against `d_F_lowrank32` (E18); paired Δ AUROC vs `null_ratio_raw_post_rank1` (E17b).
- Sealed thresholds: AUROC ≥ 0.60 with non-overlap 95% bootstrap CI vs 0.5 (E18); Δ ≥ +0.02 with non-overlap CI (E17b).
- Sealed bar: 2-of-3 primaries for E18; Qwen 2.5 7B as primary authority for E17b.
- Bootstrap: 1000 sample-level resamples; seed pinned to 20260423.
- Reference: pre-registration document `wiki/pri-v3/pri-v3-plan.md` (snapshot at commit XXX).

#### 3.2 Pipeline
- Synthetic puzzle generator (2×2 factorial, chain_length × contradiction). Per-cell n=50 → 200 samples per model.
- Greedy decoding, max-gen-tokens=14, behavioral preflight gate (80% control accuracy threshold, max-gen-tokens=12 for completion-style format).
- Per-step PRI capture: surprise, cosine/L2 Δh, Fisher distances (diag/full/topk32/lowrank32), null_ratio columns at rank sweep {1,2,3,4,5,8,13,16,21,32,34,55,64}, raw-W_u parallel emission (E17b).
- Coordinate consistency: post-RMSNorm Δh projected onto post-RMSNorm basis (the corrected geometry — see §3.4).

#### 3.3 Models
- Primaries (sealed gate authority): Llama 3.2 3B Instruct, Mistral 7B Instruct v0.3, Qwen 2.5 7B Instruct. All 4-bit quantized via mlx-community.
- Cross-generation companion: Qwen3 8B 4bit (descriptive, not sealed).
- Cross-architecture companion (descriptive only, Phase 3 landed 2026-04-26): **Gemma 3-4B 4bit** alone, n=50/cell, gate 100%, run-08 (`experiments/v3-main-run/2026-04-26/run-08`). Gemma 3-1B was excluded after gate-failing at 11/20 = 55% on n=20 stratified controls; `--gate-verbose` confirmed model-capability rather than parser failure (1B defaults to "Answer: NO" on every YES control regardless of premises). Within-family scale axis (1B ↔ 4B held architecture-fixed) collapses to a single point; 4B is reported as a cross-architecture data point. Sealed-rank-1 Fisher-decisive (Δ=+0.187 [+0.141, +0.229]); rank=32 Raw-decisive (Δ=−0.383 [−0.464, −0.301]) — the within-model rank-sensitivity finding.
- **Phi-3.5-mini 4bit (descriptive only, recovered 2026-04-26).** Originally excluded on the 2026-04-23 main run after gate-failing at 12/20 = 60% under the original 256-token gate budget + last-match-anywhere parser. Re-validated under the v3.1 fixes (`--gate-max-tokens 12` + 3-tier `check_answer` parser, PR #7). `--gate-verbose` confirmed Phi front-loads `Answer: YES` then continues with format-completion (`"Answer: YES   Instruction: Read the premises..."`) — same failure mode as Llama / Qwen 2.5 in the v3.1-replicate. Under the fixes Phi gates clean at 100% (20/20) and runs full at n=50/cell. Descriptive companion only — Phi is not a sealed primary.

#### 3.4 J_n geometry correction (one paragraph in body, full in Appendix)
**Body — one sentence:** _"The pipeline's `null_ratio` computation originally projected pre-RMSNorm Δh onto a post-RMSNorm basis (a coordinate mismatch in the Fisher pullback). The mismatch was identified, corrected by capturing post-RMSNorm Δh directly, and the sealed verdict was re-derived under consistent post-norm geometry. Both readings are reported below for transparency; full diagnosis in Appendix A."_

### 4. Results
#### 4.1 Sealed E18 verdict
Table: per-primary AUROC + 95% CI + sign + gate verdict. Highlight 3/3 PASS.

#### 4.2 Sealed E17b verdict (Qwen 2.5)
Table: Fisher AUROC, raw AUROC, Δ + CI, gate verdict.
**Side-by-side with the buggy reading** for transparency:
| Reading | Fisher | Raw | Δ | Verdict |
|---|---|---|---|---|
| Buggy (pre-norm Δh on post-norm basis) | 0.7665 (sign −1) | 0.9323 (sign +1) | −0.166 [−0.240, −0.098] | FAIL (raw decisive) |
| Corrected (post-norm Δh on post-norm basis) | **0.9008 (sign +1)** | 0.7513 (sign −1) | **+0.150 [+0.100, +0.201]** | **PASS (Fisher decisive)** |

The +0.32 swing is the J_n correction's effect; the verdict flip is the headline of this subsection.

#### 4.3 Cross-model architecture-dependence
- Per-rank AUROC landscape figure: AUROC vs rank, one curve per primary, both Fisher and raw bases.
- Architecture-dependence narrative at sealed rank=1, J_n-corrected post-norm geometry: each model is **decisive with non-overlap CI**, but the winner partitions across the architecture axis, not the parameter-count axis. **Fisher decisive (3 of 6):** Llama 3.2 3B Δ=+0.239, Qwen 2.5 7B Δ=+0.149, Gemma 3-4B Δ=+0.187. **Raw decisive (3 of 6):** Mistral 7B Δ=−0.153, Qwen3 8B Δ=−0.213, Phi-3.5-mini Δ=−0.421 (largest margin, Raw=0.997 nearly perfect). Cross-generation within Qwen-family (2.5 Fisher → 3 Raw) and within-vendor (Llama Fisher vs Mistral Raw) both flip — the regime is not vendor- or scale-determined. A second axis: **Raw's native sign at r=1**. On Mistral and Phi, Raw discriminates with sign +1 (Raw direction natively points along contradiction-vs-control). On the other four (Llama, Qwen 2.5, Qwen3, Gemma 4B), Raw discriminates with sign −1 (inverted). The +/− split correlates with which models write a non-content commit token (newline / format-completion) at gen_step=1 vs actual answer content — see §5.1.
- **Gemma 3-4B Phase 3 (n=50/cell, sealed-equivalent config, run-08, 2026-04-26):** at sealed rank=1, **Fisher decisive** with Δ_oriented = +0.187 [+0.141, +0.229] (oriented Fisher AUROC 0.747 [0.674, 0.817] vs oriented Raw 0.559 [0.471, 0.639]); at rank=32, **Raw decisive** with Δ_oriented = −0.383 [−0.464, −0.301] (oriented Raw AUROC 0.980 [0.963, 0.993] vs oriented Fisher 0.597). The same dataset, same model, same J_n-corrected geometry — the Fisher-vs-Raw verdict **flips between rank=1 and rank=32**. Strong baselines on Gemma 4B too: surprise 0.960 [0.932, 0.981], pri_v2_lowrank32 0.960 [0.932, 0.981]. Underwrites "audit the operating-point neighborhood before falsifying" as a methodological lesson — pinning a single rank can mask a regime shift visible across the sweep.
- **Phi-3.5-mini descriptive (n=50/cell, 2026-04-26 run-06):** Raw decisively wins at the sealed plane with the **largest E17b margin observed across all 5 models** — Δ Fisher_post − Raw_post = **−0.421** [−0.507, −0.335]. Raw_post AUROC at rank=1 = **0.9974 (sign +1)** — nearly perfect contradiction discrimination via the static W_u SVD basis, and stays at ~0.997 across every rank from 1 to 32. Fisher_post at rank=1 = 0.5766 (barely above chance). E18 descriptive AUROC = 0.6119 [0.525, 0.694] sign +1 — would-pass-if-sealed but the weakest E18 of the 5 models. Baselines on Phi crush v3 too: surprise 0.901, v1 cosine 0.899, v2 lowrank32 0.949, v2 topk32 0.949 — at the sealed plane on Phi, the simpler metrics are decisively better than the Fisher pullback. Worth a discussion paragraph: Phi joins Mistral as the only models with Raw natively at sign +1 (correctly aligned with rupture direction); the other 3 (Llama, Qwen 2.5, Qwen3) have Raw in inverted-discrimination territory.
- ~~(If Gemma data lands) within-family-scale companion: Gemma 1B vs Gemma 4B, architecture held fixed.~~ Within-family scale axis collapsed (Gemma 1B gate-fails — see §3.3); 4B reported as cross-architecture point only.

#### 4.4 Baselines
Surprise, PRI v1 cosine, v2 topk32, v2 lowrank32 — table by primary. v3 outperforms v1 and v2 on the sealed metric; surprise is competitive on Qwen 2.5 specifically (one of the cross-model anomalies worth noting).

### 5. Discussion
#### 5.1 Why architecture-dependence rather than universal Fisher win
- Mistral writes a newline at gen_step=1; Qwen-family front-loads `' Answer'` / `'YES'` / `'NO'`. The sealed plane captures qualitatively different commitment moments per architecture.
- For Mistral/Llama the commit is "begin the answer block"; for Qwen-family it's actual answer content.
- Fisher pullback's edge depends on whether Δh structure at the commit aligns with W_u's high-singular-value vs low-singular-value directions.
- **Three architecture-dependence motifs at n=600 / n=300 per stratum (the powered cut from the 6×13×2 model × rank × chain_length landscape — see [v3.1-replicate](../results/v3.1-replicate.md) §Three architecture-dependence motifs):**
  - 🪼 **Motif 1 — Stable Raw across all ranks (Phi-3.5).** The only model in the 6-model lineup with Raw decisive at every rank in the 13-point sweep, every chain-length stratum. Raw_post_rank1 = 0.9989. The headline counter-example to "Fisher pullback uniformly wins" — Phi is the canonical "HARP-style detection works as advertised" datapoint and pins the upper bound of static-W_u-SVD performance.
  - 🐲 **Motif 2 — Within-model rank flip robust to chain length (Gemma 3-4B).** Δ_oriented goes from +0.207 (Fisher decisive) at r=2 to −0.211 (Raw decisive) at r=3 in one rank step; Raw stays decisive through r=64. Both chain-length strata show the same transition (one borderline tie at r=5/cl=2 only). Pure rank-axis flip — a property of the SVD spectrum, not chain-length.
  - 🌀 **Motif 3 — Chain-length × rank interaction (Mistral 7B).** Two Simpson's-paradox sites at non-overlap CI: at r=1 the pool says Raw but cl=2 = Fisher decisive and cl=5 = tied; at r=32 the pool says Fisher but cl=2 = Raw decisive (−0.196 [−0.262, −0.131]) and cl=5 = Fisher decisive (+0.379 [+0.319, +0.450]) — **Δ_cross = −0.575**, the largest cross-stratum spread in the entire 156-cell landscape. Mistral's chain-length-coupled commit geometry (it writes a newline at gen_step=1; the newline's position relative to the contradiction event shifts with chain depth) is the unique architecture-dependence flag for the chain_length axis. Other models' cross-stratum spreads stay within ±0.3 at every rank.
- **Mechanism summary (§5.1).** Mistral writes a newline at gen_step=1; Qwen-family front-loads `' Answer'` / `'YES'` / `'NO'`. The sealed plane captures qualitatively different commitment moments per architecture. For Mistral/Llama the commit is "begin the answer block"; for Qwen-family + Phi + Gemma 4B it's actual answer content. **Universal pattern across all 6 models: |Δ| sharper at cl=2 than cl=5** (e.g. Llama 0.397 vs 0.170; Mistral 0.065 vs 0.002; Gemma 0.401 vs 0.250; Phi −0.374 vs −0.228). Short reasoning chains place the gen_step=1 commit closer to the contradiction-detection event; long chains diffuse the rupture across intermediate reasoning tokens.

#### 5.2 Pre-registration governance
- Sealed spec + amendments timeline preserved verdict integrity across multiple bug-fix cycles (J_n correction, BOS contamination, cfg propagation, gate memory, hardcoded N).
- The discipline machinery worked: each bug was disclosed, classified as bug-fix vs sealed re-spec, and the sealed parameters were not modified.
- Recommend: publish pre-registration BEFORE main run; treat amendments as first-class artifacts; never silently override.

#### 5.3 Limitations
- Synthetic 2×2 puzzles only; factual contradictions (TriviaQA-style pair-condition) is the next experimental rung but not in this paper.
- 4-bit quantization across all models — no full-precision baseline.
- Mac mini M4 16GB constrained — no models above 8B tested in v3.1 scope. Phi-3.5-mini gate-failed; gpt-oss-20b dropped 2026-04-14 as too heavy.
- Within-family scale axis incomplete: Gemma 3-1B gate-failed at 11/20=55% on n=20 stratified controls (model-capability, not parser — defaults to "Answer: NO" on YES controls regardless of premises), reducing the Gemma 1B↔4B comparison to a single point. Reported descriptively as a cross-architecture data point only; the architecture-held-fixed scale-replication test of HARP's inverse-g-vs-capability claim is left to v4.
- Behavioral gate is sensitive to small-model output formatting. Reasoning-tuned and small (≤2B) models can default to a single answer token regardless of premises; we treat this as gate failure rather than apply prompt-engineering rescues to maintain pre-registration discipline.
- Sealed plane is gen_step=1 only — depth-profile (E21) and multi-step (gen_step > 1) work is v4 territory.

#### 5.4 Future work
- Pair-condition factual rung (Fisher-Rao geodesic protocol on real Q&A pairs).
- Curvature κ as ℏₛ-scale signal (cross-model finding from 2026-04-26 standalone diagnostic; orthogonal-to-Fisher discrimination AUROC ≈ 1.0 on Qwen 2.5 — needs fresh-data replicate before claiming).
- Depth profile (E21) — does the architecture-dependence story hold across layers?
- Larger-vocab and/or non-quantized models on better hardware.
- Prompt-format sensitivity at sub-3B scale: characterize where the YES/NO behavioral gate breaks and design a more robust verification protocol (potentially likelihood-based rather than parsed-token-based) that admits sub-3B models without sacrificing pre-registration discipline.

### 6. Conclusion
~150 words. Restate the 4 headline claims tightly. Close on the cross-model finding being the most-publishable contribution and the pre-registration discipline being the methodological one.

## Appendix A — Bug timeline + corrections

Brief paragraph per item. Date, what the bug was, why it didn't violate the sealed spec, link to the public Amendments entry in `wiki/pri-v3/pri-v3-plan.md`.

- 🐛 **2026-04-25 · J_n geometry mismatch** — Fisher pullback projected pre-RMSNorm Δh onto a post-RMSNorm basis. Identified via standalone diagnostic at N=100 across all 4 primaries; corrected in PR #11 by capturing post-RMSNorm Δh directly. Sealed E17b reading flipped from −0.166 (FAIL) to +0.150 (PASS). Sealed spec unchanged — analysis plane, residualization, bootstrap, threshold, 2-of-3 bar, Qwen-2.5-authority all preserved. The bug was in the IMPLEMENTATION of the Fisher pullback formula, not in the spec.
- 🐛 **2026-04-24 · cfg propagation in load_model** — `load_model(model_name)` read `cfg.layers_to_probe` from the module-level default Config, silently ignoring per-run overrides. Banner echoed correctly; only the `Probed: {}` line revealed the mismatch. Patched: `load_model(model_name, config=None)` now takes config explicitly. Operational, not sealed-affecting.
- 🐛 **2026-04-24 · Behavioral gate memory bomb** — preflight gate routed all 20 control samples through full `trace_sample()`, allocating ~250 MB transient × 20 samples ≈ 5 GB compressor pressure on Mac mini M4. Surfaced only on large-vocab primaries (Llama V=128k); Mistral V=32k unaffected. Patched: gate uses `mlx_lm.generate()` (text-only). Operational, not sealed-affecting.
- 🐛 **2026-04-24 · Behavioral gate parser fooled by completion-style output** — Qwen 2.5 + Llama 3B gate-failed at the default 256-token budget because they front-load `Answer: YES` then continue with format-completion, sometimes fabricating a second `Answer: NO`. Patched: `--gate-max-tokens 12` operational rescue + 3-tier `check_answer` parser (Tier 1 prefers last `Answer:`). Operational, not sealed-affecting.
- 🐛 **2026-04-24 · Stratified preflight sampling** — seed-dependent skew in `dataset[~contradiction].head(pilot_n)` produced an 11/9 chain-length split at seed 20260423, gate-failing reasoning-tuned primaries that emit stray "NO" tokens during chain-walk. Patched: per-chain-length quota sampling. Operational, not sealed-affecting.
- 🐛 **2026-04-25 · Stage 3 BOS contamination** — diagnostic `first_token_id()` returned the BOS token (`<|begin_of_text|>` on Llama, `<s>` on Mistral) because HF tokenizers auto-prepend BOS. Stage-3 specific; Stage 4 (paired Fisher on full p_t) was unaffected. Patched: defensive BOS-skip via `getattr(tokenizer, "bos_token_id", None)`. Diagnostic only, not sealed-affecting.
- 🐛 **2026-04-25 · Stage 2 hardcoded N=25/cell** — `diagnose_qwen_norm.py` had `N_PER_CELL = 25` baked in (= 100 total) with no env override despite the banner promising N=200. Patched: env-overridable `DIAG_N_PER_CELL`. Diagnostic only, not sealed-affecting.
- 🐛 **2026-04-26 · Gemma 3 RMSNorm γ extraction** — `_extract_final_rmsnorm_gamma` returned the raw `.weight` for all model families, but Gemma 3 uses the "+1" RMSNorm formulation (`mx.fast.rms_norm(x, 1.0 + self.weight, eps)`); Gemma's stored `weight` clusters around 0 with negative entries on some channels. On the J_n-corrected post-norm path, this would have multiplied Δh post-norm by ≈0 (or by a sign-flipped vector) on Gemma instead of by the effective scale `1 + weight`, silently corrupting every `null_ratio_*_post_rank{r}` column on Gemma alone. Identified before any Gemma main-run data was captured. A second precision sub-bug surfaced on Gemma 3-4B (bf16-stored weight): adding 1.0 in fp32 after casting introduced ~0.4% per-channel rounding compounding to 3.6% max-abs error vs the model's own forward; resolved by performing the `1 + weight` operation at the weight's native dtype before casting to fp32. Verified end-to-end: extracted γ reproduces `model.model.norm(h)` to ≤1e-5 max-abs error on all six families (Llama, Mistral, Qwen 2.5, Qwen 3, Gemma 3-1B, Gemma 3-4B). Gemma-specific; Llama / Mistral / Qwen / Qwen3 unaffected (their RMSNorm applies `weight` directly). Pre-data, not sealed-affecting.

For each: cite the corresponding `wiki/pri-v3/pri-v3-plan.md` Amendments entry by date, plus the corresponding PR number on `flowstyleliving/PRI_at_commitment`.

## Appendix B — Reproducibility pointers

- Code: GitHub `flowstyleliving/PRI_at_commitment`, commit `<TBD — pin at submission>`.
- Pre-registration: `wiki/pri-v3/pri-v3-plan.md` snapshot at commit `<TBD>`.
- Run artifacts: `experiments/v3-main-run/2026-04-26/run-02/{Llama,Mistral,Qwen2.5,Qwen3}-*_results.parquet`. Sealed-gate output: `experiments/v3-main-run/2026-04-26/run-02/sealed_gate.json` (records `geometry: "post"` in `sealed_spec`).
- Hardware: Apple Mac mini M4, 16 GB RAM. mlx-lm + mlx 4-bit quantized models from `mlx-community`.
- Environment: Python 3.9 + venv, full requirements pinned in `requirements.txt` at submission commit.
- Reproduce sealed verdict: `git checkout <TBD>; python -u scripts/run_v3_main.py --scope v3_1_main --n-per-cell 50 --seed 20260423 --max-gen-tokens 14 --gate-max-tokens 12 --layers final; python scripts/analyze_sealed_gate.py --run-dir experiments/v3-main-run/<DATE>/run-NN`.

## Plot / figure inventory

Each item: short description + axes + data source.

- 📊 **Fig 1 — Sealed E18 verdict (3/3 PASS).** Bar chart per primary: AUROC + 95% CI, threshold line at 0.60. Source: run-02 sealed_gate.json `E18_sealed_rank1_lowrank32`.
- 🎯 **Fig 2 — Sealed E17b head-to-head on Qwen 2.5 (PASS).** Two bars (Fisher post, raw post) + difference + threshold line at +0.02. Source: run-02 sealed_gate.json `E17b_head_to_head`.
- 🪞 **Fig 3 — J_n correction effect.** Side-by-side AUROC bars: buggy vs corrected, on the sealed E17b head-to-head. Show the verdict flip. Source: run-05 (buggy) vs run-02 (corrected) sealed_gate.json.
- 📐 **Fig 4 — Per-rank AUROC landscape, cross-model.** Lines: AUROC vs rank, one panel per primary (4 panels), Fisher vs raw bases overlaid. Highlight rank=1 with a vertical line. Source: run-02 parquets, computed via the rank sweep in `_analyze_model`.
- 🌐 **Fig 5 — Architecture-dependence summary.** Scatter or radar: x = best rank, y = Δ AUROC at best rank, one point per (model, basis). Color by model family. Source: run-02 parquets + analyzer.
- 📜 **Fig 6 (optional) — Baselines table as figure.** Surprise, PRI v1, v2 topk/lowrank vs v3 post-norm null_ratio. Per primary. Source: run-02 sealed_gate.json `baseline_*`.
- 🌀 **Fig 7 (optional) — Cross-generation Qwen 2.5 vs Qwen 3.** Two-panel comparison of per-rank AUROC profile. Source: run-02 parquet for Qwen 2.5 + Qwen3.
- 🐲 **Fig 8 — Motif 2: Within-model rank flip robust to chain length (Gemma 3-4B).** Three-line panel: oriented Δ AUROC (Fisher − Raw) vs rank for (pool, cl=2, cl=5) with bootstrap 95% CI bands, dashed horizontal at Δ=0. The flip is sharp at r=2 → r=3: pool +0.207 → −0.211; cl=2 +0.237 → −0.275; cl=5 +0.082 → −0.232. Both strata transition together (one borderline tie at r=5/cl=2). Caption emphasizes that this is a **property of the SVD spectrum, not a chain-length artifact** — contrast with Fig 9 (Mistral). Source: `experiments/v3-main-run/2026-04-27/run-02/gemma-3-4b-it-4bit_results.parquet` (n=600, n=300/stratum). Replaces the originally-planned within-family-scale figure (Gemma 1B excluded — see §3.3, §5.3).
- 🌀 **Fig 9 — Motif 3: Within-model chain-length × rank interaction (Mistral 7B, the Simpson's-paradox case).** Three-line panel: oriented Δ AUROC vs rank for (pool, cl=2, cl=5) with bootstrap 95% CI bands. **Visually the cl=2 and cl=5 lines cross sign at r=4 → r=5 and again at r=32**; the pool line sits between them and reads "Fisher" or "Raw" depending on which stratum's magnitude dominates. Annotate the two Simpson's-paradox sites: r=1 (pool R, cl=2 F, cl=5 tied) and **r=32 (pool F +0.177; cl=2 R −0.196; cl=5 F +0.379; Δ_cross = −0.575)** — the largest cross-stratum spread in the entire 156-cell landscape. Caption frames Mistral's gen_step=1 newline-commit as the chain-length-coupled mechanism: the newline's position relative to the contradiction event shifts across chain depth, while content-commit architectures (Qwen / Phi / Gemma) decouple. Source: `experiments/v3-main-run/2026-04-26/run-09/Mistral-7B-Instruct-v0.3-4bit_results.parquet` (n=600, n=300/stratum).
- 🪼 **Fig 10 (optional, supplementary) — Motif 1: Phi-3.5-mini stable Raw across all ranks.** Single line: Δ_oriented vs rank for Phi (pool only, since stratification mirrors pool); horizontal CI band stays well below zero across all 13 ranks (max −0.105 at r=3, min −0.459 at r=32). Optional; for the supplementary if space tight. Source: `experiments/v3-main-run/2026-04-27/run-01/Phi-3.5-mini-instruct-4bit_results.parquet`.

Plot tooling: matplotlib + seaborn (already installed in venv). Generate via `scripts/make_three_model_pri_figures.py` (existing) or new `scripts/make_paper_figures.py` (TBD).

## Disclosure framing recipe (do/don't list)

- ✅ **DO** disclose every bug that affected captured data or any verdict.
- ✅ **DO** pair each disclosure with what the bug DIDN'T touch (sealed spec parameters were preserved).
- ✅ **DO** use "identified and corrected" not "fixed" — sounds like governance not panic.
- ✅ **DO** lean into the methodological strength: catching your own bugs and disclosing them IS rigor.
- ✅ **DO** cite the Amendments entry for each, by date, in the appendix.
- 🚫 **DON'T** apologize.
- 🚫 **DON'T** lead any section with the bug; weave bug disclosure into methodology naturally.
- 🚫 **DON'T** include PR numbers, commit hashes, or stack traces in the body of the paper. Those live in CHANGELOG.md.
- 🚫 **DON'T** speculate about other bugs that might exist. Disclose what you found, fixed, and verified.

## Open decisions (TODO before draft is locked)

- 📝 **Title.** Settle on a final title once first draft of intro is done. Working title above is a placeholder.
- 🎯 **Venue.** Workshop paper (8 pages) vs full conference paper (12+ pages)? Decision affects how much of the cross-model architecture-dependence story can fit vs go into appendix.
- 🌐 **Gemma Phase 3.** ~~Run before draft is sent for review?~~ **Resolved 2026-04-26: Gemma 4B alone, n=50/cell, ~25-30 min.** Gemma 1B excluded after gate-fail diagnosis (model-capability, see §3.3 + Appendix A bug entry for the γ-extraction fix that unblocked the 4B path). Pipeline pre-validated end-to-end on both Gemmas at n=2/cell smoke and n=10/cell pilot; n=50 launch deferred until concurrent Phi-3.5 diagnostic (PID 56098, `v3_1_phi_only`) finishes to avoid MLX buffer-cache contention on Mac mini M4.
- 🪦 **Curvature κ as future-work mention vs separate paper.** The 2026-04-26 standalone diagnostic showed κ residualized on null_ratio_post discriminates contradictions at AUROC ≈ 1.0 on Qwen 2.5. Worth a future-work paragraph at minimum; possibly a separate short paper later.
- 📐 **Pre-registration document publication.** Snapshot `wiki/pri-v3/pri-v3-plan.md` to a permanent URL (OSF / arXiv submission archive) before paper submission. Critical — pre-reg without an immutable timestamp is methodologically weak.

## Cross-references

- Sealed verdict source: [results/v3.1-replicate](../results/v3.1-replicate.md) §N=200 sealed-equivalent rerun (and the post-2026-04-26 update — TBD when the J_n-corrected verdict is folded in).
- Pre-registration: [pri-v3-plan](../pri-v3/pri-v3-plan.md) — Amendments timeline anchors every bug disclosure.
- Pipeline implementation: code repo `flowstyleliving/PRI_at_commitment`, branch `fix/null-ratio-post-norm-geometry` at PR #11 (will be on main once merged).
- ELI12 explainers (link from appendix as supplementary intuition for non-specialists): [learn/jn-correction-eli12](../learn/jn-correction-eli12.md), [learn/model-architecture-families-eli12](../learn/model-architecture-families-eli12.md), [learn/fisher-square-root-eli12](../learn/fisher-square-root-eli12.md).
- Bug timeline source-of-truth: [pri-v3-plan §Amendments](../pri-v3/pri-v3-plan.md) + [log](../log.md) chronological entries.
