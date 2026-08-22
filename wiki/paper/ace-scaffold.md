# ACE (PRI v4) Paper — Draft Scaffold

_Status: `[SCAFFOLD]` — section structure + headline claims + figure/table inventory + open decisions. Companion draft at [ace-draft.md](ace-draft.md) — **draft is now `[DRAFT]` with full prose end-to-end** (2026-05-30 same-day write-through). Built 2026-05-30 from the sealed v4 verdict ([[results/v4-sealed-2026-05-26]]) + Codex paper-readiness audit (2026-05-30)._

_Method name **ACE = Attention Commitment Estimator** locked 2026-05-30. The repo-side artifacts (calibrator, detector, sealed profiles, figures, tables) refer to the same instrument._

## Working title (LOCKED 2026-05-30)

**Attention Commitment Estimation for Pre-Generation Belief Readout**

Selection rationale: method-first structure (Codex audit + scaffold's "Option A" track), acronym ACE dropped from title (introduced in body only), "in [Open] Language Models" trailing dropped per author preference + Tweak-2 reasoning (mild padding; venue + abstract anchor the subject). 74 chars; clean TOC scan; leads with the evocative phrase "Pre-Generation Belief Readout" earned via §3.1 / §6.7.

Alternatives considered but not selected:
- *Pre-Generation Commitment is Legible: ACE Detects Committed Answers from Attention at t=0* — result-first, punchier but risked overclaim on transfer
- *Attention-Channel Calibration of Pre-Generation Commitment across Nine Open LLMs* — methodology-first, modest but bland
- *A Pre-Registered Test of Attention-Channel Commitment Detection at t=0 in Open Language Models* — pre-reg-first, buried the method
- *ACE: Reading Pre-Generation Commitment from Attention* — shortest, mechanism-focused; passed over for the more descriptive method-first form

## Headline claims (one-line each, to anchor every section against)

- 🎯 **$E_{A1}$ sealed gate (discriminability across 9 architectures): 7/9 PASS.** ANLI R1 ($n=200$, seed 20260526), OOB CI$_\text{lo} > 0.50$ on at least one of 21 attention cells per model. Strongest: Mistral-Nemo 0.887 [0.816, 0.946]; weakest passer: Qwen3-1.7B 0.641 [0.502, 0.737]; failures: Llama-3.2-3B (0.597 [0.403, 0.705]) and Gemma-3-4B (0.656 [0.488, 0.756]).
- 🪞 **$E_{A2}$ sealed gate (cell-transfer across tasks): 3/9 exact, PARTIAL-TRANSFER reframe triggered (≥3/9 clause).** Exact (metric, block-prefix, sign) match across ANLI R1 → TriviaQA: Mistral-7B (`last_minus_1_js_no_bos` $-$), Mistral-Nemo (`last_minus_1_bos_mass` $-$), Qwen2.5-7B (`final_v_norm_lastq_weighted` $+$). Block-prefix stable in 6/9. Neither falsifier triggered (E_A1 ≥7, E_A2 <5).
- 🌊 **Per-(model, task) calibration is empirically binding, not assumed.** TriviaQA AUROCs are uniformly stronger than ANLI (8/9 pass; Mistral-7B 0.995, Mistral-Nemo 0.987) — the model exists, but the winning cell does not transfer for 6/9 models. Replicates the 2026-05-13 33-profile ANLI R1↔R2↔R3 finding at the cross-task level.
- 🥈 **Baselines (E_B1, secondary):** on 4 OOB-trustworthy models, ACE wins 2/4 clean (Phi-3.5-mini 0.774, Qwen2.5-7B 0.818), loses 1 to RAUQ (Llama-3.2-3B 0.655 vs 0.678), and ties SinkProbe on Qwen3-8B ($\Delta$=0.003). Baseline numbers are gen_step=1 prep-sweep data; t=0 re-run is non-blocking future work per pre-reg.
- 🩻 **Causal pilot (future work, NOT a headline):** +v_top steering at $\alpha$=50 flips contradiction samples at 4× the rate of entailment samples (40% vs 10%), despite contradictions having a larger mean logit gap. Confound mitigation (logit-gap matching, orig_answer balance) required before promotion. **Belongs in §5 Future Work, not the main results.**
- 🔧 **Methodological contribution: post-seal naming + nested-OOB schema.** Method name (ACE) locked post-seal as presentation-only, sealed parameters untouched. Schema v1.2 inherits v1.1's nested-OOB selection-bias-corrected CIs (Codex review fix, 2026-05-13).

## Section outline

### Abstract
\~200–250 words. Lead with: ACE detects YES/NO commitment state at t=0 across 9 open architectures, but the winning cell is per-(model, task). Close with: pre-registration discipline preserved verdict integrity through the May 2026 STEP-0 belief-readout-locus re-grounding (2026-05-17 logit-locus re-anchoring of all gen_step=1 attention numbers).

### 1. Introduction

- 🌊 **Hook**: an LLM's commitment to a YES/NO answer is often legible *before* it speaks the first token — the attention pattern at the prefill-last-position already encodes the answer. ACE estimates that commitment.
- 🪞 **Problem framing**: hallucination / over-confidence detection has typically watched the model's *output*; we watch the model's *attention right before it commits to output*.
- 🎯 **Contribution**: sealed pre-registered ACE evaluation across 9 open architectures on ANLI R1 + TriviaQA + 3 baselines (RAUQ, SinkProbe, our prior calibrator at gen_step=1). Two confirmatory gates ($E_{A1}$, $E_{A2}$), one secondary baseline comparison ($E_{B1}$).
- 📋 Roadmap.

### 2. Related Work

- **Attention-channel uncertainty**: RAUQ (recurrent attention uncertainty), SinkProbe (sink-token attention concentration), StreamingLLM sink work — all the attention-based prior art ACE is compared against.
- **Belief-readout / Anthropic emotions framing**: Sofroniew et al. 2026 — internal-state representations differing from outputs. ACE is a behaviorally concrete instance.
- **Information geometry on the simplex** (Amari 2016 etc.) — relevant for the Fisher pullback connection to v3 (PRI's prior paper). ACE is the attention-channel analog.
- **Pre-registration in ML** (Nosek 2018; Pineau 2021) — sealed-spec mechanics; cite Furnace v3's pre-reg pattern as inheritance.
- **Hallucination detection at single-pass cost**: semantic entropy (Farquhar 2024) and self-consistency (Wastl 2025) require ≥10 forward passes; ACE is 1 forward.

### 3. ACE Method

- **3.1 Instrument**: t=0 prefill-last-position attention. Definition: for an input prompt $P$, run one forward pass, capture attention weights at the last prefix token position, before any generation.
- **3.2 The 21-cell panel**: 3 block-depth prefixes (`final`, `mid`, `last_minus_1`) × 7 metrics (`js`, `js_kv_groups`, `js_no_bos`, `bos_mass`, `v_norm_bos`, `v_norm_max`, `v_norm_lastq_weighted`). Each cell is a scalar feature per sample.
- **3.3 Calibration**: per-(model, dataset) OOB bootstrap winner-cell selection with sign locking from calibration-set direction. Schema v1.2 (nested-OOB, selection-bias-corrected CIs). Bootstrap $n=1000$.
- **3.4 What ACE is NOT**: not Fisher-pullback (that's PRI v3); not a probe trained on labels (no logistic head); not multi-pass (single forward).

### 4. Sealed Experimental Setup

- **4.1 Pre-registration**: link to `PRI_V4_PRE_REGISTRATION_PLAN.md` frozen 2026-05-26. Sealed parameters: 9-model panel, 21-cell panel, ANLI R1 $n=200$ + TriviaQA $n=100$ at seed 20260526, OOB bootstrap $n=1000$, $E_{A1}$ threshold ≥7/9, $E_{A2}$ thresholds (≤2 / 3–4 / ≥5).
- **4.2 Models**: 9 MLX 4-bit open-weights. Phi-3.5-mini INCLUDED-with-caveat per pre-reg gate decision (denominator=9).
- **4.3 Datasets**: ANLI R1 (synthetic adversarial NLI, paired YES/NO labels); TriviaQA paired-prompt (factual question, correct vs plausibly-wrong injected answer).
- **4.4 Baselines**: RAUQ best-single-layer (not aggregate, which sandbags); SinkProbe ‖V‖-weighted column-sum (not last-query). Both at gen_step=1 from the prep sweep — t=0 re-run is non-blocking future work per $E_{B1}$ clause.

### 5. Results

- **5.1 $E_{A1}$ verdict**: 7/9 PASS → **Fig 1**. Failures: Llama-3.2-3B (ANLI), Gemma-3-4B (ANLI). Both recover on TriviaQA.
- **5.2 Cross-task generalization** → **Fig 2**. TriviaQA uniformly stronger; Mistral-7B 0.995, Mistral-Nemo 0.987. Single TriviaQA failure: Qwen3-1.7B (0.471).
- **5.3 $E_{A2}$ cell transfer** → **Fig 3** + **Table 2**. 3/9 exact, 6/9 block-prefix-stable. Mistral-7B, Mistral-Nemo, Qwen2.5-7B carry the exact-transfer cases.
- **5.4 Baseline comparison ($E_{B1}$, secondary)** → **Table 3**. ACE 2/4 wins on trustworthy. Baseline disagreement: RAUQ and SinkProbe pick opposite directions on Mistral-Nemo + Qwen3-8B → they capture different phenomena.
- **5.5 Pre-registration table** → **Table 1**.

### 6. Discussion

- **6.1 What "partial transfer" means in deployment**: per-(model, exact deployment distribution) calibration is binding. ACE generalizes as a *method*, not as a fixed cell.
- **6.2 Architectural patterns**: 3/9 exact-transfer models span Mistral family (both sizes) + one Qwen (2.5-7B but not Qwen3-8B / Qwen3-1.7B). Family is not predictive; calibration era / instruction-tuning recipe might be — flagged as open.
- **6.3 Why TriviaQA is uniformly stronger**: hypothesis — paired-prompt task gives the model an explicit reference answer to disagree with; the rupture is larger. Speculative.
- **6.4 Connection to PRI v3 (Fisher pullback at gen_step=1)**: v3 and ACE measure complementary aspects of the same commitment moment. v3 is residual-stream Fisher geometry at generation; ACE is attention-channel readout at prefill. Both pass discriminability gates; both require per-model calibration. Bridge work (the causal probe) is §6 future work.
- **6.5 Limitations**: 4-bit MLX quantization (uniform across panel — comparable but not faithful to fp32 deployment); ANLI synthetic (TriviaQA partially mitigates); single-seed ($n=200$ ANLI is the sample-size constraint, not the seed); baselines at gen_step=1 not yet t=0.
- **6.6 Future work**: (a) t=0 baseline re-run; (b) causal probe scaling (+v_top intervention pilot already shows 40% vs 10% flip asymmetry — confound mitigation needed); (c) bluff-vs-honest-uncertain epistemic-distinguishability testbed (v5 candidate, deferred).
- **6.7 Pre-registration governance**: post-seal naming (ACE locked 2026-05-30) annotated as presentation-only; sealed parameters untouched. Verdict integrity preserved through STEP-0 belief-readout-locus re-grounding (2026-05-17 t=0 logit-locus anchor re-validated all gen_step=1 numbers).

### 7. Conclusion

Single paragraph. Re-state: ACE works across architectures, calibration is per-(model, task), pre-reg discipline survived a substantial mid-flight re-grounding.

### Appendices

- **A** Full pre-registration text (snapshot of `PRI_V4_PRE_REGISTRATION_PLAN.md` frozen 2026-05-26)
- **B** Per-cell candidate-panel AUROCs (all 21 cells × 18 (model, dataset) profiles = 378 numbers)
- **C** Hyperparameter-sensitivity: panel-cell choices, sign-locking rationale
- **D** Computational cost: per-model wall-time on M4 Mac mini, per-cell forward-pass cost
- **E** Causal probe pilot details ($n=40$, +v_top intervention, $\alpha$ sweep)

## Figure + table inventory (all built 2026-05-30)

| # | Asset | File | Carries |
|---|---|---|---|
| 📊 Fig 1 | ACE ANLI R1 OOB AUROC bars (9 models, 95% CIs, 0.50 threshold) | `PRI_at_commitment/paper/v4/figures/out/fig1_anli_auroc.{pdf,png}` | $E_{A1}$ primary |
| 📈 Fig 2 | Cross-task paired AUROC slope graph (ANLI R1 → TriviaQA) | `PRI_at_commitment/paper/v4/figures/out/fig2_cross_task.{pdf,png}` | Task dependence + TriviaQA descriptive strength |
| 🪞 Fig 3 | Cell-transfer matrix (9-row, exact/block-stable flags) | `PRI_at_commitment/paper/v4/figures/out/fig3_transfer_matrix.{pdf,png}` | $E_{A2}$ visual |
| 📋 Table 1 | Pre-registration summary (sealed parameters + outcomes) | `PRI_at_commitment/paper/v4/figures/out/table1_prereg_summary.tex` | Reproducibility |
| 📝 Table 2 | Per-model winner cells + AUROC[CI] + stability + transfer flag | `PRI_at_commitment/paper/v4/figures/out/table2_winner_cells.tex` | $E_{A1}$ + $E_{A2}$ detail |
| 🥈 Table 3 | ACE vs RAUQ vs SinkProbe on OOB-trustworthy (caveat-flagged) | `PRI_at_commitment/paper/v4/figures/out/table3_baselines.tex` | $E_{B1}$ secondary |

All 6 regenerable via `PRI_at_commitment/paper/v4/figures/build_all.sh` (\~5s on M4 from sealed profile JSONs).

## Open decisions

- [ ] **Venue**: ARR / NeurIPS / ICML main track / interpretability workshop. Codex says: NeurIPS/ICML borderline (needs crisp framing); ARR / interpretability comfortable.
- [ ] **Page length**: 8pp workshop / 9pp + refs main-conf. v3 went 8pp workshop; v4 has comparable scope.
- [ ] **Title**: pick from candidates above after intro lands.
- [ ] **Phi-3.5-mini framing**: pre-reg INCLUDED it with denominator=9; Step-0 low-decidedness tension (2026-05-25 audit) carries forward as a flag, not [FALSIFIED]. Surface in §3.2 or §5.2 as caveat — decide where.
- [ ] **Baseline t=0 re-run before submission?** Pre-reg says non-blocking. Codex says current Table 3 is honest with the caveat. Decision: ship with caveat OR delay submission \~3 days for t=0 baseline re-run. Default: ship with caveat unless reviewer culture in chosen venue penalizes it.
- [ ] **Causal probe framing**: §5 future work (current scope memo) vs §6 supporting result with explicit "pilot only, confound" framing. Default: §5 future work.

## What this scaffold deliberately does NOT do

- 🚫 Decide the venue (depends on author calibration of risk + reviewer culture)
- 🚫 Write any body prose (that lives in [[paper/ace-draft]] — **now a complete \~4865-word prose draft**, no longer pending)
- 🚫 Add new experimental work (sealed run is complete; play sprint is closed)
- 🚫 Reopen pre-reg sealed parameters (frozen 2026-05-26; ACE naming is presentation-only)
- 🚫 Promote causal probe pilot or baseline comparison to headline (per scope memo + Codex risks)

## Cross-references

- [[paper/ace-draft]] — companion Markdown draft (**full prose, all sections + appendices**; numbers locked from the sealed verdict)
- [[paper/ace-scope-2026-05-26]] — scope memo + 3-candidate headline comparison
- [[results/v4-sealed-2026-05-26]] — sealed verdict source
- [[research-candidates]] — entry #5 (ACE) sealed + entry #7 (v5 bluff-detection, deferred)
- [[results/rauq-sinkprobe-vs-ours-2026-05-16]] — baseline source data
- [[results/causal-probe-pilot-2026-05-25]] — causal pilot source data
- Repo: `PRI_V4_PRE_REGISTRATION_PLAN.md` (sealed 2026-05-26)
- Repo: `paper/v4/figures/` (loader + 6 scripts + build_all.sh)
- Repo: `experiments/v4-sealed/2026-05-26/profiles/` (18 sealed JSONs)
