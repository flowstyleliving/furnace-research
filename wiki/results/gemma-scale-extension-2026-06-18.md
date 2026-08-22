---
status: out-of-sample extension (NOT part of the sealed 18/20)
date: 2026-06-18
seed: 20260612
relates: [[confluence-seal-2026-06-11]]
---

# Commit-Confluence — Out-of-Sample Scale/Family Extension (gemma orphan probe)

> **What this is.** A pre-registered, byte-comparable out-of-sample extension of the
> [[confluence-seal-2026-06-11|registered seal]], run to explain the seal's defining
> honest-negative: the `gemma-3-4b/anli` orphan (the one cell that failed *both* endpoints).
> It does **not** enter or alter the sealed 18/20 verdict. Pre-registration (frozen before any
> strict metric): `commit-confluence/stage_b/PRE_REGISTRATION_EXT.md`. Runner: `stage_b/run_ext.py`.
> Profiles: `stage_b/profiles_ext/` (sealed `profiles/` untouched).

## Question
The `gemma-3-4b/anli` orphan confounds three factors — **scale** (4B), **generation** (Gemma 3),
**family** (Gemma). This extension moves one factor at a time, on the *same* data, seed, panel, and
selector, to decompose it. Comparability is exact: **module hashes identical to the seal**, same
fresh data files (`*_seed20260612_n200.jsonl`), seed 20260612, n=200 strict (zero-drop),
nboot=2000, same `run_cell` / nested-OOB selector.

## Results (all n=200, strict, controls pass)

| Deployment | GEOM CI_lo | PRIM CI_lo | Deployable | Winning signal |
|---|---|---|---|---|
| `gemma-3-4b` / ANLI **(sealed orphan)** | **0.403** | — | ❌ | ACE `last_minus_1_js` |
| `gemma-3-12b` / ANLI | **0.709** | 0.709 | ✅ | ACE `last_minus_1_v_norm_lastq_weighted` |
| `gemma-3-12b` / TriviaQA | **0.929** | 0.929 | ✅ | ACE `last_minus_1_v_norm_lastq_weighted` |
| `Qwen2.5-14B` / ANLI | **0.766** | 0.759 | ✅ | ACE `last_minus_1_js_kv_groups` |
| `Qwen2.5-14B` / TriviaQA | **0.597** | 0.612 | ✅ | ACE `mid_js_kv_groups` |

**4/4 new cells deployable.** Deployability gate = OOB AUROC 95% CI lower bound > 0.50.

## Verdict — the orphan was a scale / small-model artifact

Filling the pre-registered decision table (ANLI-R1 geometric deployability):

| `g3-4b` | `g3-12b` | `Qwen2.5-14b` | Registered reading |
|---|---|---|---|
| FAIL (0.403) | **PASS (0.709)** | PASS (0.766) | **Orphan = scale/small-model artifact (gen-3).** ✅ |

- **Scaling gemma-3 4B→12B recovers ANLI deployability** (0.403 → 0.709, comfortably above the 0.50
  gate, not marginal). Registered prediction was "LEAN YES (\~60%)" → **confirmed**.
- **The family control (`Qwen2.5-14B`) passes ANLI** (0.766) → the 4B failure was **not** a generic
  "12–14B-scale needed for ANLI" effect; it was the small gemma specifically, fixed by scale.
- **gemma-3-12b is clean on TriviaQA too** (0.929; prediction YES \~90% → confirmed).
- The **generation axis** (`gemma-4-12B`) is **not yet run** — gated on (a) a parallel
  gemma4-capable mlx-lm venv and (b) a sealed-core `gemma4_unified` adapter + re-derived manual
  attention recompute. See pre-reg §Phase 2.

## Texture consistent with the seal's spine
- **All four winners are ACE attention** signals; **confidence/fusion never wins alone** (PRIM ≈
  GEOM). Reinforces ACE dominance and "confidence is not the backstop" on held-out models.
- **No universal champion across deployments**, reproduced out-of-sample: 3 distinct winning
  signals over 4 cells (gemma → penultimate value-norm; Qwen → inter-KV-group disagreement, at the
  penultimate layer for ANLI but the mid layer for TriviaQA).
- **Marginal cell to flag:** `Qwen2.5-14B/TriviaQA` CI_lo 0.597 — deployable but the weakest of the
  four (echoes the Qwen3-1.7B/TriviaQA fragility theme); controls pass.

## Predictions vs outcomes (all confirmed)
| Cell | Registered | Outcome |
|---|---|---|
| g3-12b/ANLI | LEAN YES \~60% | PASS 0.709 ✓ |
| g3-12b/TriviaQA | YES \~90% | PASS 0.929 ✓ |
| Qwen-14b/ANLI | YES \~85% | PASS 0.766 ✓ |
| Qwen-14b/TriviaQA | YES \~90% | PASS 0.597 ✓ (marginal) |

## Implications for the paper
The seal's strict-product falsification (18/20, two orphans) **stands** — this is a separate,
clearly-labeled post-seal section. But it sharpens the orphan narrative: at least one of the two
orphans (`gemma-3-4b/anli`) is **substantially a model-scale artifact**, not a permanent
commit-moment blind spot. The honest framing — "no universal detector, but a universal floor" — is
unchanged; this adds "and the orphans are not all permanent: scale closes one of them."

## [HYPOTHESIS → REFUTED] Mechanism — the orphan as an attention-head-resolution effect (2026-06-18; ablation-tested 2026-06-20)

> **Tag: [HYPOTHESIS — head-COUNT resolution REFUTED by ablation 2026-06-20; it's head/representation QUALITY, not count].** The head counts are hard fact; the causal story was tested and the count-resolution version did not hold (see Crab-lock result below).
> Companion explainer: [[../learn/gemma-attention-head-resolution]].

ACE's signals are statistics computed *over the set of attention heads / KV-groups* at the commit
token — `js` (inter-head Jensen--Shannon disagreement), `js_kv_groups` (inter-group), per-head
`bos_mass`, `v_norm`. Their resolution is bounded by how many heads/groups the model has. Confirmed
from the loaded models (the 4b config omits these and inherits gemma3 defaults):

| model | n_heads | n_kv_groups | head_dim | layers |
|---|---|---|---|---|
| gemma-3-4b | **8** | **4** | 256 | 34 |
| gemma-3-12b | **16** | **8** | 256 | 48 |

The 4b computes attention morphology over **half the query heads and half the KV-groups** of the 12b.
**Hypothesis:** the `gemma-3-4b/anli` orphan is a *head-resolution* effect — ANLI (subtle
entailment/contradiction) needs fine commit-moment attention discrimination that 8 heads / 4 groups
cannot express legibly; TriviaQA (blunter recall) stays legible even at 4b (it passed); doubling
heads/groups at 12b restores resolution → ANLI `0.403→0.709`. Gemma 3's **QK-norm** (per-head
RMSNorm on Q/K, which replaced Gemma 2's attention-logit soft-capping) plausibly compounds the
small-model problem by flattening per-head differences.

Other special Gemma 3 attention features (context): **5:1 interleaved local/global** layers (local =
1024-tok sliding window), **decoupled `head_dim=256`** constant across sizes (over-complete:
n_heads·256 ≠ hidden), **dual RoPE base** (local θ=10k, global θ=1M). Sources: Gemma 3 Technical
Report (arXiv:2503.19786), Google "what's new in Gemma 3" dev blog.

**Clean tests (open):** (1) within-model head-ablation on the 12b — does dropping to 4 KV-groups
reproduce the orphan? (2) does `js`/`js_kv_groups` cross-head variance collapse on the 4b vs 12b on
ANLI? If ACE is a true attention-head detector, this head-resolution story is the predicted mechanism.

### [CRAB-LOCK RESULT 2026-06-20] head-*count* resolution REFUTED — it's quality, not count

Ran test (1): a within-model ablation that starves gemma-3-12b's ACE statistics to the 4b head
budget (**8 query heads / 4 KV-groups**, vs 16/8) without touching the model — runtime monkeypatch of
`pri_calibrator._compute_panel_scores_for_sample` slicing the captured attention/value tensors on the
head axis; readout/null_ratio/RPV/calibration untouched. `stage_b/crab_lock.py`, seed 20260612,
n=200, controls pass.

| | geom CI-lo | deployable |
|---|---|---|
| gemma-3-12b full (16h/8kv) | 0.709 | yes |
| **gemma-3-12b starved (8h/4kv)** | **0.674** | **yes** |
| gemma-3-4b orphan (8h/4kv native) | 0.403 | no |

Halving the head budget cost only **0.035** CI-lo (still deployable; winner relocated penultimate→
final-layer `v_norm_lastq_weighted`). Head count explains at most **\~11%** of the `0.306` orphan gap
(`0.035/0.306`). **So the head-resolution hypothesis is REFUTED as the primary mechanism**: with the
12b's own heads, count barely matters. The orphan is the small model's per-head / representation
**quality** (its heads are individually less informative for subtle ANLI), not the *number* of heads.
This is an honest negative that rules out the tidy "more heads = more legible" story.

**Caveat:** the 12b's 8 subset-heads were trained among 16, so they may individually beat a native
4b's — this conservatively tests "does count matter" (it mostly doesn't); a random-subset robustness
sweep would confirm but is unlikely to flip a result this far from the gate.

### [GENERATION-AXIS RESULT 2026-06-21] gemma-4-12B deployable on both tasks — orphan does NOT return at gen-4

The pending **generation axis** (`gemma-4-12B-it-qat-4bit`) is now resolved. Because no released
mlx-lm implements `gemma4_unified`, extraction runs in the parallel `.venv_gemma4` via **mlx-vlm**
(`stage_b/gemma4_full_extract.py`), feeding the *same* nested-OOB calibrator. This cell is therefore
**NON-byte-comparable** to the seal (mlx-vlm reimplementation + version delta) and must never be
pooled with the sealed/Phase-1 or byte-comparable scale cells — it is a standalone gen-4 data point.

| gemma-4-12B cell | geom CI-lo | primary CI-lo | deployable | winner | controls | n |
|---|---|---|---|---|---|---|
| **anli_r1** | **0.691** | 0.683 | yes | Fusion `fusion_rank_mean_geom @ step 0` | pass | 200/200 |
| **triviaqa_paired** | **0.751** | 0.748 | yes | Fusion `fusion_rank_mean_geom @ step 0` | pass | 200/200 |

**Verdict: 2/2 deployable.** The generation axis does **not** reintroduce the
[[results/confluence-seal-2026-06-11|sealed]] `gemma-3-4b/anli` orphan: gen-4/anli **0.691** sits right
beside gen-3-**12b**/anli 0.709 (both PASS), while gen-3-**4b**/anli was 0.403 (FAIL). Combined with the
scale-axis finding above, this nails the orphan as a **scale / small-model gen-3 artifact**, not a
property that the gemma generation lineage carries forward — gen-4 at 12b is healthy on the same task.

**Prompt-format bug found & fixed first (Bell-Burnell discipline).** The initial gen-4 run returned
**\~0.37 on BOTH tasks** (anli 0.390, trivia 0.368) — and the *full* panel incl. the model's own
confidence also failed (\~0.369), the red flag that the signals carried \~no info about correctness. The
mundane cause: the io-plugin default `raw_passthrough` (which gemma-3-12b *tolerated*) does not make
**gemma-4-it** perform the task — on a raw prompt it just continues the question text (commits `" The"`
p=0.97 / `" Adam"` p=0.92), uncorrelated with the YES/NO label ⇒ \~0.37 noise after sign-locking.
Under gemma-4's own `apply_chat_template` it commits sharply `YES`/`NO` (p≈1.0). Fixing `strat` to apply
the chat template flipped both cells from noise to clean deployable (diagnostic: `stage_b/g4_diag.py`;
no double-BOS — tokenize=True vs re-tokenized strings give identical id streams).

**Notable wrinkle:** unlike every byte-comparable scale cell (where ACE attention always won *solo*),
both gen-4 winners are the **Fusion** cross-locus cell. Does not contradict the sealed 18/20 (separate
non-byte-comparable cell); flagged for the paper's gen-4 footnote.

**Caveats stacked on this cell:** (1) non-byte-comparable (mlx-vlm reimpl + version delta); (2) the ACE
attention recompute IS faithful (`G4Wrap` o_proj cos(mine, model) = 1.0000); (3) the readout half is NOT
independently parity-validated (gemma-3 under mlx-vlm returns `hidden_states=None`, a gemma-4-only API),
though the D0/D1 off-by-one is fixed and controls pass. Artifacts:
`stage_b/profiles_ext/{anli_r1,triviaqa_paired}/gemma-4-12B-it_FIXED.matrix.npz`,
logs `stage_b/_ext_logs/{g4_diag,g4_full_FIXED}.log`.
