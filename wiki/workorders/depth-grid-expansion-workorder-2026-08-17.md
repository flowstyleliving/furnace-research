# Workorder — Depth-grid cross-family expansion (DC paper spine)

**Opened:** 2026-08-17 · **Status:** DESIGN (pre-audit) · **Owner:** Claude (steward) · **Audit:** Codex gpt-5.6 high-reasoning (this document), then a second code-level audit before launch.

## Goal

Extend the registered per-layer depth-curve instrument ([[../results/depth-curve-2026-08-16]]) from 8 cells (Qwen 7B/32B/72B + Llama-3.3-70B × {ANLI R1, HaluEval-QA}) to a **4-family × scale grid**, pre-registered, to (a) confirm or kill the two surviving regularities (terminal-block dip 8/8, one-block CLIFF onset 7/8) on out-of-family cells, (b) re-test the placement law (E1) with family as the axis, (c) resolve the Llama lineage question opened by the P3 blind-spot finding, and (d) produce the spine of the next paper (**DC**, working code `dc`).

Grid A (banked, 2026-08-16) is now **discovery data**. Grid B (this workorder) is **confirmatory** for the dip/cliff regularities. That discovery→confirmation structure is the paper's registered core.

## Grid

| family | model | HF id (expected) | params | N layers (expected; pin at introspection) | status | GPU plan |
|---|---|---|---|---|---|---|
| Qwen 2.5 | 7B / 32B / 72B | (banked) | 7/32/72B | 28 / 64 / 80 | **banked grid A** | — |
| Llama | 3.3-70B | (banked) | 70B | 80 | **banked grid A** | — |
| Llama | 3.1-8B | `meta-llama/Llama-3.1-8B-Instruct` | 8B | 32 | new | 1×A100-80 |
| Llama | 3.1-70B | `meta-llama/Llama-3.1-70B-Instruct` | 70B | 80 | new | 1×A100-80 |
| Llama | 3.1-405B | `meta-llama/Llama-3.1-405B-Instruct` | 405B | 126 | **stretch, MK go/no-go** | 4–8×A100-80, see §Compute |
| Mistral | Small 3.2 | `mistralai/Mistral-Small-3.2-24B-Instruct-2506` | 24B | 40 | new | 1×A100-80 |
| Mistral | Medium 3.5 | `mistralai/Mistral-Medium-3.5-128B` | 128B | TBD (introspect) | new | 2×A100-80 or 1× + streaming capture |
| Gemma 3 | 12B | `google/gemma-3-12b-it` | 12B | 48 | new | 1×A100-80 |
| Gemma 3 | 27B | `google/gemma-3-27b-it` | 27B | 62 | new | 1×A100-80 |

Tasks: same two frozen datasets (ANLI R1 + HaluEval-QA, n=200, sha256 pinned in-extractor, unchanged). New cells: **12** (14 with 405B). Full grid: 20–22 cells, 10–11 models, 4 families.

### Per-family rationale + risks

- **Qwen 2.5 (anchor).** Already banked; no re-runs. Serves as the within-family scale ladder (28→64→80 blocks) against which new families are read.
- **Llama 3.1-8B.** Small-scale Llama: does the mid-stack band exist at 8B or is it scale-emergent? Bonus narrative: this is the sealed confluence orphan model (`Llama-3.1-8B/anli` FAIL, closed at 70B scale) — the new instrument revisits the exact model whose panel cell failed. Risk: none unusual; cheapest cell.
- **Llama 3.1-70B.** Same-size, same-architecture cross-check against banked 3.3-70B. Llama 3.3 is a post-training refresh over the 3.1 pretraining lineage, so this pair isolates **post-training vs pretraining** as the source of the band's location. Recommendation: run this **regardless** of the 405B decision (MK's list framed it as the 405B fallback; the controlled pair is independently valuable and cheap).
- **Llama 3.1-405B (stretch).** The only slot above 128B; tests whether the band keeps drifting with scale. Gated on MK sign-off after smoke-calibrated cost (§Compute). License: Llama 3.1 Community License; HF gating must be pre-flighted with the Modal secret's token.
- **Mistral Small 3.2 24B + Medium 3.5 128B.** Third family, dense only per MK. Medium 3.5 verified open-weights (released 2026-04-30, dense 128B, modified-MIT, on HF; replaced Devstral 2/Magistral). **Both are multimodal checkpoints** (Small 3.1+ and Medium 3.5 carry vision encoders) → load via a conditional-generation wrapper with a `language_model` inside; the extractor needs a decoder-path resolver (§Engineering). Sealed panels contain Mistral-7B (MLX) but the torch lane has never run Mistral — new family for this instrument.
- **Gemma 3 12B + 27B.** Fourth family, dense. 12B has byte-comparable MLX confluence cells (never pool; qualitative shape comparison only). Gemma-3 quirks: 5:1 sliding:global attention (window 1024 ≥ our max seq 900, so sliding layers still see the full prefix at our lengths — record this in provenance), q/k-norm, `<bos>` conventions (bos_mass cell meaningful). Risk: gemma behavioral gate history at small scale (gen-3-4b ANLI fail); 12B passed ANLI on MLX (0.709) so gates should hold, but any YES/NO gate failure **aborts the cell and is reported as registered** — no rescue.

### Explicitly out (this round)

- Mistral-7B-v0.3 legacy continuity cell (optional cheap add if MK wants the sealed-flipper model on the new instrument — not in MK's grid).
- MoE models — **deliberately deferred, not excluded** (MK, 2026-08-17): dense-only keeps this round one-variable (family × scale) and within reach; MoE depth curves (routing confounds, per-expert capture) are the designated *next* step after this grid banks, and the DC paper's future-work line.
- Qwen3 family (keep the grid non-reasoning instruct only).
- The other benchmarks (TriviaQA etc.) — depth lane stays 2-task; cross-task breadth is a separate follow-up.

## Engineering deltas (modal_depth.py + depth_score.py)

1. **Registry entries** for 6–7 new models: HF id, GPU spec, `EXPECT_N_LAYERS`, per-model chat/YES-NO token handling (reuse `_chat_ids`; verify single-token YES/NO per tokenizer at smoke).
2. **Decoder-path resolver.** Mistral Small 3.2 / Medium 3.5 (and possibly Gemma-3 under some transformers versions) load as conditional-generation wrappers; capture hooks and `model.model.layers[i]` paths must resolve through `language_model`. One resolver function, per-model override in registry.
3. **Multi-GPU path** for ≥128B: `device_map="auto"` sharding across N GPUs (Modal `gpu="A100-80GB:n"`), bnb nf4 unchanged (`llm_int8_skip_modules` incl. lm_head/embed and **vision tower modules** for the multimodal checkpoints — enumerate at introspection).
4. **Streaming last-row capture (optional, gated).** Full-retention eager attention costs L×H×S²×4B (405B ≈ 52 GB, Medium-3.5 ≈ 27–33 GB). A forward-hook variant that stores only each layer's last-row attention to CPU and drops the full map would let Medium-3.5 fit 1 GPU and 405B fit 4. **Acceptance gate: bit-exact reproduction of a banked grid-A cell (Qwen-7B) before any new-model use.** If it can't reproduce exactly, fall back to full retention + more GPUs. This is the highest-silent-risk delta — Codex audit should weigh in on whether to build it at all.
5. **Scorer:** extend `EXPECT_N_LAYERS` (pinned from config introspection **before** the prereg freeze — config reads are not outcome-looks), no statistical changes. Same seed 20260816, same NPERM=200 / NBOOT=1000, same qualifying-peak rule.
6. **Provenance:** same npz meta block (code commit, HF `_commit_hash`, lib versions, sealed-kernel hashes) + new fields: wrapper class name, device_map summary, capture mode (full/streaming).

## Registered endpoints (draft — freeze after audit in `PRE_REGISTRATION_EXPANSION.md`)

Grid-B cells only (grid A is discovery). Sign-free per-block AUROC, qualifying peak = AUROC ≥ 0.65 AND above the 97.5th-pct shuffled envelope, as registered in the original prereg.

- **E5 — terminal dip (confirmatory, primary).** In each grid-B cell with a qualifying peak: final block AUROC ≤ peak − 0.05. **CONFIRM ≥10/12; FALSIFY ≤7/12;** between = WEAKENED. (Grid A: 8/8.)
- **E6 — cliff onset (confirmatory, secondary).** Original E2 CLIFF definition per cell. **CONFIRM ≥8/12 CLIFF.** (Grid A: 7/8.)
- **E7 — within-model cross-task peak agreement (descriptive-registered).** Agreement = overlapping 90% bootstrap CIs OR |ℓ*_anli − ℓ*_halueval| ≤ max(2, 0.05·N). Report the fraction over all 10–11 models; no pass/fail. (Directly answers the "does the peak move by task" question with a frozen definition.)
- **E8 — Llama lineage (descriptive-registered).** (a) 3.1-70B: qualifying mid-stack band on anli (≥ 10 qualifying blocks in [0.4N, 0.9N]) → band is lineage-stable across post-training; (b) 3.1-8B: ≥5 qualifying mid-region blocks on either task → band present at 8B, else scale-emergent. (c) If 405B runs: report band location shift vs 70B.
- **E1″ — placement law re-test (descriptive-registered).** Original E1 absolute/relative rules over the full grid. Registered expectation: **stays UNDECIDED** (an honest null; a surprise law would then be creditable).
- **Multiplicity:** E5 is the single primary; E6 secondary; the rest descriptive. Misses reported as written; amendments only as new dated sections.

Predictions to freeze (draft): P6 dip ≥10/12 · P7 cliff ≥8/12 · P8 Llama-3.1-70B band replicates · P9 Llama-3.1-8B band ABSENT (scale-emergent guess) · P10 E1″ UNDECIDED.

## Process (canonical)

1. This workorder → **Codex gpt-5.6 adversarial audit** → revisions (this step).
2. Config introspection (config.json only) → pin N layers, heads, wrapper classes, vision-module names.
3. Freeze `PRE_REGISTRATION_EXPANSION.md` (grid, endpoints, predictions, gates, comparator discipline) in `commit-confluence/exploratory/depth-curve/`, commit.
4. Build registry/resolver/multi-GPU deltas (+streaming capture only if audit approves) → **second Codex audit, code-level** → fix → commit.
5. Gates-only smoke (2 prompts/model; prints gates, never AUROC). Behavioral-gate failures abort cells, reported as registered.
6. Detached Modal launch (server-side, kill-proof, per-cell logs, `vol.commit()` banking), staged: cheap cells first, 128B next, 405B only on MK go.
7. Scorer runs ONCE over all banked grid-B cells (first look). No peeking mid-run.
8. Propagation (11 surfaces + TOTAL line), results page `depth-grid-2026-08-XX`, paper scaffold fill-in, milestone on MK sign-off.

## Compute (coarse, refined at smoke)

| tier | cells | est. wall | est. cost |
|---|---|---|---|
| 8B/12B/24B/27B ×2 tasks | 8 | \~0.3–1 h each, 1×A100 | \~$15–25 |
| 3.1-70B ×2 | 2 | \~1–1.5 h each | \~$8–12 |
| Medium-3.5-128B ×2 | 2 | \~2–3 h each, 2×A100 (or 1× + streaming) | \~$25–50 |
| **subtotal (grid B core)** | **12** | | **\~$50–90** |
| 405B ×2 (stretch) | 2 | \~3–6 h each, 4–8×A100 | \~$80–250 |

## Paper (DC) — why this grid is a paper

1. **Instrument:** per-layer sign-free AUROC curves + shuffled-label envelope + bootstrap peak CI, computed by a sealed kernel — cheap, registered, reusable.
2. **Blind-spot lesson (methodological headline):** sparse depth sampling inverted a locus conclusion (Llama "readout family" was panel-relative). Caution for all probing-at-fixed-layers work.
3. **Registered cross-family test:** dip + cliff discovered on grid A, confirmed/killed on grid B — clean discovery→confirmation structure.
4. **Placement non-law:** no transferable absolute/relative depth rule at n=200 resolution; per-model measurement is the honest deployment guidance.
5. **Family structure:** 4 families × scale; lineage pair (3.1-70B vs 3.3-70B) isolates post-training.

Scaffold: `wiki/paper/dc-scaffold.md` (created with this workorder). Figures planned: 20-curve grid; money figure (Llama band with the 3 panel rungs overlaid); dip forest plot; peak-fraction vs N scatter; cliff-onset table.

## Pre-flight findings (2026-08-17, second pass — grants + revision pins)

- **MK accepted all five licenses (2026-08-17).** Gemma grants landed instantly (HTTP 200); Meta's three Llama-3.1 repos remain 403 pending manual review — re-probe before freeze.
- **Gemma configs pinned live:** 12b-it @ `96b6f1eccf38110c56df3a15bffe176da04bfd80` — `Gemma3ForConditionalGeneration`, 48 text layers, 16 heads, 8 KV, hidden 3840, sliding_window 1024. 27b-it @ `005ad3404e59d6023443cb575daa05336842228a` — 62 layers, 32 heads, 16 KV, hidden 5376, head_dim 128, sliding_window 1024. Both match audit expectations; window 1024 ≥ the 900-token bound.
- **Mistral revisions pinned:** Small 3.2 @ `95a6d26c4bfb886c58daf9d3f7332c857cb27b43`; Medium 3.5 @ `22b2b868a15677cfa6061277ed2f653d1349a9ab`.
- **Z Slim drive scanned (MK ask): no grid-B-usable weights.** `meta-llama/Llama-3.3-70B-Instruct` there is 21 MB tokenizer/config only (June weights went straight to the Modal volume); LLaVA-Mini's llama-3.1-8b is a multimodal fine-tune (inadmissible under the official-revisions rule); Llama-3.2 1B/3B are base models outside the grid; the rest is MLX-lane 4-bit. Modal pulls grid-B weights server-side, so local disk was never in the critical path.
- ~~Llama layer counts remain expected-not-pinned (32/80/126) until Meta approves; freeze blocker per audit residual 8.~~ **CLEARED same day — Meta approved all three within the hour.** Pinned live: 8B @ `0e9e39f249a16976918f6564b8830bc894c89659` (32L/32H/8KV, hidden 4096); 70B @ `1605565b47bb9346c5515c34102e054115b4f98b` (80L/64H/8KV, hidden 8192); 405B @ `be673f326cab4cd22ccfef76109faf68e41aa5f1` (126L/128H/8KV, hidden 16384). All plain `LlamaForCausalLM` — no wrapper. All match audit expectations; 405B's 126×128 confirms the 24.33 GiB bf16 retention figure. **All 7 grid-B model slots are now revision-pinned; the sole remaining freeze precondition is the grid-A rescore under the new E5/E6.**

## Pre-flight findings (2026-08-17, config introspection)

- **Mistral configs pinned (open repos, fetched):** Small 3.2 24B = `Mistral3ForConditionalGeneration`, **40 layers**, 32 heads, 8 KV, hidden 5120. Medium 3.5 128B = `Mistral3ForConditionalGeneration`, **88 layers, 96 heads**, 8 KV, hidden 12288 → eager retention ≈ 88·96·900²·4B ≈ **27 GB**, confirming 2×A100-80 (or 1× + streaming capture). Both are multimodal wrappers → decoder resolver required, vision tower excluded from quantization skip-list handling.
- **Gating check:** `meta-llama/Llama-3.1-{8B,70B,405B}-Instruct` and `google/gemma-3-{12b,27b}-it` all return **HTTP 403, `gated: manual`** for the current HF account. The June Llama-3.3 grant does not cover Llama-3.1 (separate agreement), and Gemma has never needed a grant before (MLX used `mlx-community` mirrors). **MK action required: accept licenses on the Llama-3.1 and Gemma-3 pages** (account-level; covers the Modal secret if it is the same account). Fallback: non-gated mirrors (e.g. unsloth) — worse provenance, use only if acceptance stalls.
- Gated models' layer counts remain expected-not-pinned (32 / 80 / 126; 48 / 62) until access lands; pin before freeze.

## Open decisions (MK)

1. **HF license acceptances** (blocking for 4–5 of 6 new models): Llama-3.1 collection + Gemma-3 collection, on the account backing the Modal `HF_TOKEN` secret.
2. **405B go/no-go** — default: run 3.1-70B now, decide 405B after smoke refines cost (\~$80–250).
3. **Mistral-7B legacy cell** — optional $2 add for sealed-panel continuity; not in MK's grid.
4. Milestone/publication timing — per convention, sign-off at results time.

## Audit round 1 (Codex gpt-5.6, 2026-08-17) — verdict RED; accepted revisions (plan v2)

Codex's full report is preserved in the session log; the sections above are **v1 and stand as written for provenance** — the following resolutions supersede them and will be the basis of the frozen prereg. All ten MAJORs accepted (none rejected); the talk-through round refines instantiations.

1. **E5 rebuilt as a cross-fitted contrast.** The v1 dip endpoint was positively biased: peak argmax'd over N blocks on the same 200 rows used to estimate `peak − final`. v2: K-fold cross-fit (select ℓ* on training folds, estimate `AUROC(ℓ*) − AUROC(final)` on held-out rows, average over folds), or a max-statistic permutation test over the whole selection procedure — instantiation settled in talk-through round 2.
2. **E6 redefined as a directional positive jump** within the rise to the cross-fitted peak, permutation-calibrated for N-dependence (more blocks = more chances for a big max-jump), with exhaustive CONFIRM/WEAKEN/FALSIFY registered. The v1 rule inherited a max-|Δ| statistic that could count downward jumps.
3. **Denominators frozen:** primary population = the 12 core cells; gate-aborted and no-peak cells count as FAILURES (conservative); 405B excluded from every confirmatory denominator (descriptive only); evaluable-cell sensitivity analysis registered alongside.
4. **Medium 3.5 precision reality:** the official checkpoint is **FP8** (mixed BF16/F8 tensors) — "bnb nf4 unchanged" is dead for this model. Options: native FP8 on Hopper+ (2×H100/H200) vs dequant-to-bf16 on 4×A100. Precision heterogeneity disclosed either way; choice settled in round 2 + smoke. Also: modified-MIT has a revenue restriction → say "open weights," never "open source"; release late April 2026.
5. **Streaming capture DROPPED.** With corrected bf16 math (retained eager attention is L·H·S²·2B: 405B ≈ 24 GiB, Medium ≈ 13 GiB, not my fp32-inflated 52/27–33 GB), full retention fits every cell incl. 405B on 4×A100-80. One capture implementation across the entire confirmatory grid; no heterogeneous-instrument confound.
6. **Prospective pinning:** HF model revisions (commit hashes), container/image digest, pip-frozen dependency versions, prompt-token hashes, actual loaded quantizer/module types — all frozen in the prereg, verified at run, failed-closed on mismatch (not merely recorded after the fact).
7. **Multimodal loading correctness:** one shared decoder descriptor (used by capture, o_proj gate, heads/KV counts, and provenance alike) resolving `model.language_model.layers` + `config.text_config` for Mistral3/Gemma3; `mistral-common` tokenizer for Small 3.2; AutoProcessor + explicit reasoning-mode `none` for Medium 3.5; Gemma gating pre-flighted (confirmed 403 in our own pre-flight, independently of the audit).
8. **Causal language removed:** 3.1-70B vs 3.3-70B = "controlled same-size version comparison" (Meta does not establish an identical base checkpoint); "scale-emergent" → present/absent at 8B, descriptive; the design is an **unbalanced comparative panel**, not factorial family × scale; "placement non-law" → "no registered placement rule established."
9. **Confirmation scope recast:** "prospective held-out-model confirmation on two fixed benchmarks (ANLI R1, HaluEval-QA)" — not task-general. Llama 3.1 cells additionally labeled family-seen/model-unseen. Optional third unseen task = MK decision (cost/scope).
10. **Multiplicity hierarchy:** gatekeeping — E5 primary tested first; E6 confirmatory only if E5 confirms; E7/E8/E1″ strictly descriptive with no verdict vocabulary (no "hit/replicate/stable/emergent"); family-stratified outcomes reported; bars set against permutation-calibrated nulls rather than coin logic. E7 reports cross-fitted peak-distance estimates (CI-overlap dropped — it rewarded imprecision). E1″ replaced by a descriptive peak-fraction-vs-N analysis with model/family-clustered uncertainty.

MINORs accepted wholesale (GiB vs GB, Medium 88L/96H pinned, license phrasing, token-length + per-layer attention-type recording, 405B timeout + download/scheduling margins).

## Audit round 2 (Codex gpt-5.6, 2026-08-17) — verdict YELLOW, path to GREEN; settled instantiations (plan v3)

1. **E5 (primary) — cross-fit, fully specified.** Stratified fixed 5-fold map (20 pos / 20 neg held out per fold), same fold map across all models within a task. Per fold: fit block AUROC **directions on training rows only**, apply the qualifying-peak rule on training rows only, select the peak, **lock the direction** (never refit on held-out), estimate `AUC(selected) − AUC(final)` on the held-out fold. Cell Δ = mean over folds; **cell success = Δ ≥ 0.05**; any fold without a qualifying training peak ⇒ cell fails. Bootstrap (within task × label × fold, identical row resamples across models, full selection re-run) is reported, not gating. **Grid inference by synchronized label permutations** (same permutation across all six models within a task; tasks independent; ≥2000, prefer 5000; full cross-fit re-run). **CONFIRM = ≥10/12 AND ≥3/4 per grid-B family AND p_grid < 0.05; WEAKEN = 8–9/12 or a guard failing; FALSIFY = ≤7/12.** Gate/no-peak = failures; 405B excluded. No coin-logic justification anywhere.
2. **E6 (secondary, gatekept) — cross-fitted directional jump.** Training rows pick the peak, then `j* = argmax_j [AUC(j+1) − AUC(j)]` on `ceil(0.5N) ≤ j < peak`; lock directions and j*; evaluate the directional jump held-out; never maximize on held-out rows. Success = J_cf ≥ 0.15 AND above the cell's 95th-pct full-procedure permutation null AND J_cf ≥ 0.5·R_cf. Grid (only if E5 CONFIRMs): CONFIRM ≥9/12 AND ≥4/6 per task AND ≥2/4 per family AND p_grid < 0.05; WEAKEN 8/12 or guard fail; FALSIFY ≤7/12; if E5 doesn't confirm ⇒ **NOT TESTED — gate closed** (not falsified). **Precondition: rescore grid A under these exact definitions BEFORE freezing grid-B bars** — if the new grid-A rate isn't clearly recurrent, E6 demotes to descriptive.
3. **Medium 3.5 = FP8-origin, BF16-compute.** Deterministic dequantization to BF16 on **4×A100-80** (8× fallback) — matches the lane's hardware/kernels; native-FP8-on-H200 rejected (changes weights+kernels+hardware at once). Registered label: "FP8-origin weights, deterministically dequantized; BF16 compute on A100" — this is **not** a BF16 reference checkpoint, the Qwen nf4↔bf16 invariance does not cover it, and it affects **both** Medium cells. Leave-Medium-out 10-cell sensitivity summary registered (no second verdict). Smoke compares dequant-BF16 vs native-FP8 logits + captured rows on fixed non-benchmark prompts; if no faithful bridge exists, disclose exactly that.
4. **405B: default 8×A100-80.** The 4× path is allowed only through a frozen, non-outcome smoke gate (all 9 conditions: no offload; complete device map; verified `Linear4bit` nf4 + skip-list match; per-GPU peak ≤66 GiB alloc / ≤70 GiB reserved / ≥10 GiB headroom; <1 GiB reserved growth over 3 max-length forwards; BF16 attention dtype + exact shapes; o_proj cos ≥ 0.999; timing model `load + 200 × p95 × 1.2` inside timeout and MK's cost cap; ≥12 h production timeout). Any miss ⇒ 8× or cancel; no 4× retry once outcome-bearing extraction begins.
5. **Residuals absorbed into the freeze checklist:** grid-A rescore first; training-only peak qualification incl. its envelope; synchronized permutations/bootstraps for shared-item dependence; no mirror fallback after freeze (alternate IDs would be *different registered models*); verify the descriptor path is `model.model.language_model.layers` on the real wrappers; gated-repo revisions pinned = **freeze blockers** (MK license acceptances); aggregate effect uncertainty via shared row resamples; E7 two/one/no-peak cases defined with a cross-fitted distance statistic.
6. **Codex's 10 GREEN conditions for `PRE_REGISTRATION_EXPANSION.md`** adopted verbatim as the freeze checklist (revisions+lock+digest+prompt hashes; one capture mode + actual precision metadata; full E5/E6 pseudocode incl. seeds; grid-A rescore before bars; no threshold changes after freeze, no grid-B AUROC looks before all 12 bank; conservative missingness + sensitivity; Medium FP8-origin labeling; 405B descriptive under the frozen GPU gate; paper language held-out-model-on-two-benchmarks only).

**Execution order to freeze:** (1) ✅ MK license acceptances (all five granted 2026-08-17; Gemma instant, Meta within the hour) → (2) ✅ configs + revisions pinned (all 7 slots) → (3) ✅ **grid-A rescore DONE 2026-08-17** — built to the round-2 spec, Codex round-3 code audit (YELLOW, 8 MAJORs incl. within-fold permutations, E6 R>0, single-look guard, atomic outputs, MC conventions — all fixed), round-4 fix verification (all CONFIRMED + one JSON-safety blocker fixed), single look: **E5 dip 8/8 (Δ_cf 0.111–0.416, pooled p ≈ 0.0005), E6 cliff 7/8 (sole miss structural: Llama/halueval peak 26 < 0.5N ⇒ empty window)** — both regularities survive debiasing; E6 stays confirmatory-gatekept; detail [[../results/depth-rescore-2026-08-17]] → (4) freeze bars + full prereg (add frozen language: E6-undefined-by-early-peak counts as failure) → (5) freeze-time Codex audit targeting GREEN → (6) build + code-level audit → (7) smoke → (8) staged detached launch.

## Audit questions for Codex (gpt-5.6, read-only)

1. Model-slot realism: HF ids, licenses/gating, wrapper classes, expected layer counts — anything wrong or missing?
2. Memory math: eager-attention retention estimates per model; is the 2×A100 plan for 128B sound; is 405B honestly feasible at 4×?
3. Streaming last-row capture: build it (with the bit-exact reproduction gate) or avoid the code delta and pay for GPUs?
4. Endpoint definitions E5–E8/E1″: gameable? multiplicity honest? bars sensible given grid-A base rates (dip 8/8, cliff 7/8)?
5. Confirmatory framing: is "grid A discovery → grid B confirmation" clean, or does reusing the same two tasks contaminate it?
6. Anything that would make the DC paper unsound if we run exactly this plan?

## Status 2026-08-18 — grid-B COMPLETE (E5 WEAKEN 8/12); 405B stretch PAUSED on Modal credits

Steps 4–8 of the execution order all DONE 2026-08-17: freeze `2062e56` (audit rounds 5–9), build + smoke (transformers 5.15.0 repin, mlx-stub patch, cell-granular smoke — Mistral-Small/anli behavioral gate `'To'` pre-disclosed), staged detached launch, 12/12 terminal, single-look verdict `cdc55a9`: **E5 WEAKEN 8/12** (p_grid 0.0005, pooled dip CI [0.123, 0.201]); E6 NOT TESTED (gatekept); P8+P9 both hit. Milestone pushed (`furnace-causalities` `b8bb2c0`). Detail: [[../results/depth-grid-2026-08-17]].

**405B stretch (registered §7; MK go: "run the 405b. audit before run"):** enablement + descriptive-only scorer built; Codex round-10 audit fixes applied (None-safe md formatting, in-body 8× GPU enforcement, `data_sha256` in the stretch loader); commit `10985fe` (pushed 2026-08-18). **Smoke PASSED** — o_proj cos 0.99999 across 4 probes, 882/882 decoder modules Linear4bit, both prompt manifests frozen; \~810 GB of weights now cached on the Modal volume (sunk cost preserved). Both extraction cells launched detached 2026-08-17, then **emergency-stopped within minutes when MK reported $4 of credit remaining** (`modal app stop` ×2; `modal app list` re-verified empty 2026-08-18 — zero live apps, zero burn). Both cells died **pre-status** = the registration's one relaunchable state: no terminal statuses written, nothing aborted, no amendment needed.

**Resume procedure (any future session):**
1. MK adds Modal credits (est. $30–55 per cell to finish; running the two cells sequentially roughly halves the burn rate vs parallel — MK's choice).
2. Relaunch the two detached extract calls for `llama31_405b` × {anli_r1, halueval_qa} exactly as registered (A100-80GB:8; no code changes — `modal_depth_b.py` @ `10985fe` re-verifies the frozen manifest hashes at runtime and enforces the 8× shape in-body).
3. Watch the volume status files to terminal; pull npz + gates.json + status.json into `commit-confluence/exploratory/depth-curve/npz/depth_grid_b/`.
4. Run `score_405b.py --npz-dir npz/depth_grid_b` **ONCE** (descriptive only — no verdict vocabulary; it has its own single-look guard and refuses if outputs exist).
5. Propagate: results-page addendum (or new page), history row(s), research-candidates #13, summary, new `wiki/models/llama-3.1-405b.md`, index, dc-scaffold, log with TOTAL line; milestone only on MK sign-off.
Constraints: 405B stays outside every confirmatory denominator (descriptive stretch); terminal statuses immutable; never edit frozen files; untracked run logs (`_gridb_logs/`, `*_run.log`) live in the repo working tree only.
