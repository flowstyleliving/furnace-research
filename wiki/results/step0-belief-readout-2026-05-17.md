# Step-0 Belief Readout — Panel Verdict (2026-05-17)

**Status:** `[OPEN]` — verdict labels are the pre-registered outcomes of [[step0-belief-readout-prereg-2026-05-17]]; the *interpretation* below is not promoted to `[VALIDATED]`.
**Companion pre-reg (frozen rule):** [[step0-belief-readout-prereg-2026-05-17]]
**Why this ran:** the [[rauq-sinkprobe-vs-ours-2026-05-16|STEP-0 crack]] — Qwen 2.5-7B does not commit a YES/NO at `gen_step=1` (58% free-gen abstain, CoT preamble; cap=128 still 70%). Every `gen_step=1` number for CoT-tuned models was measured at a reasoning-preamble token, not at answer commitment. This is the decisive + cheapest disambiguator: P(YES) vs P(NO) as the immediate next token at `t=0`, zero generation, one forward.

## Run identity

- Artifacts: `PRI_at_commitment/experiments/v4-mech-prep/2026-05-17/run-02/` — `panel_summary.{csv,json}` + per-model `*_belief_readout.{json,csv}`
- Data hash (shared with RAUQ / SinkProbe / calibrator n=200 slice): `94825f3d2029c0049f2a087b0093117edc576ada84f2a073b4eccdbf8e3fe3d5`
- Panel: 10/10 models succeeded, 0 failed, `complete=true`. Same ANLI R1 n=200 slice / seed / prompts / per-model chat templates as the `gen_step=1` harness.

## Validity gate — PASSED

**Mistral-Nemo anchor: agreement 0.99 (198/200 matches), `passed=True`** (bar ≥ 0.95). `sign(lean)` at `t=0` matches Nemo's independent free-generation committed answer 99% of the time → the measurement premise itself (that the first-token logit reflects the model's committed answer) is sound. Nemo is the immediate-commit validity anchor; this guards the premise, not a downstream claim.

## Per-model verdicts + signed B-AUROC

Operating point = highest coverage with bootstrap CI_lo > 0.50; coverage is a fraction of the full n=200.

| Model | Verdict | Coverage | AUROC_B [95% CI] |
|---|---|---|---|
| Qwen2.5-7B | Recoverable-for-M | 0.980 | **0.926** [0.887, 0.959] |
| Mistral-Nemo ⚓ | Recoverable-for-M | 1.000 | 0.906 [0.863, 0.945] |
| Qwen3-8B | Recoverable-for-M | 0.995 | 0.889 [0.835, 0.932] |
| Llama-3.1-8B | Recoverable-for-M | 0.995 | 0.868 [0.815, 0.912] |
| Phi-4-mini | Recoverable-for-M | 1.000 | 0.840 [0.784, 0.894] |
| Mistral-7B-v0.3 | Recoverable-for-M | 0.995 | 0.829 [0.769, 0.884] |
| gemma-3-4b | Recoverable-for-M | 1.000 | 0.799 [0.741, 0.859] |
| Llama-3.2-3B | Recoverable-for-M | 1.000 | 0.780 [0.713, 0.839] |
| Qwen3-1.7B | Recoverable-for-M | 1.000 | 0.727 [0.655, 0.791] |
| **Phi-3.5-mini** | **Low-decidedness-for-M** | **0.185** | 0.942 [0.853, 0.997] *(only n=37)* |

- Recoverable: **9/10**. Low-decidedness: **1/10** (Phi-3.5-mini). Undetermined: **0**. Decided-but-non-B: **0**.
- Aux `C` (`sign(lean)` vs gold) is reported per pre-reg only to prevent misreading; **not** an independent `A` result and not interpreted here.

## Interpretation `[OPEN]` — bounded by the pre-reg

1. **The commit-step premise is re-grounded, not refuted.** Despite Qwen 2.5's free-gen abstention, its immediate next-token logit at `t=0` carries a strong literal YES/NO contradiction signal (0.926 @ 0.98 coverage). A valid, strongly-discriminative `t=0` elicitation locus exists — the metrics now have a well-posed place to anchor.
2. **Pre-reg constraint (must state):** a recoverable result means literal off-top1 YES/NO mass exists above a frozen, data-independent noise floor at `t=0`. It does **not** by itself imply preamble dominance is irrelevant, and it does **not** retroactively validate the specific `gen_step=1` *attention* numbers (e.g. `js_no_bos` 0.82, RAUQ/SinkProbe/calibrator cells) — those were measured at a preamble token's attention. The premise is re-established; those readings still need re-measurement at the logit-defined locus.
3. **Phi-3.5-mini is the real tension.** It is one of Step 1's three "clean trustworthy" models, yet only 37/200 samples clear the frozen decidedness floor → it forms no robust literal YES/NO boundary at `t=0` (affirmative null per pre-reg, not a failure). Its clean `gen_step=1` attention winner may ride a non-literal channel. **Flag, do not falsify** — different elicitation; audit the operating-point neighborhood before any `[FALSIFIED]` tag.
4. **Absence of Undetermined / Decided-but-non-B branches is not validation of them** (pre-reg stated limitation; they were simply not exercised on this run).

## Propagates to / read alongside

- [[step0-t0-recoverability-audit-2026-05-18]] — post-hoc t=0 sensitivity audit; byte-faithful gate; **tightens (does not weaken)** this verdict; answers pre-reg point #2 (literal-only was not understating answer recoverability)
- [[step0-phi35-locus-offset-audit-2026-05-25]] — Phi-3.5 operating-point neighborhood audit (locus-offset t=1 + floor-multiplier sweep 2x–10x); **confirms real low-decidedness state** (not locus-offset artifact, not floor-bound artifact)
- [[step0-belief-readout-prereg-2026-05-17]] — frozen rule (companion)
- [[rauq-sinkprobe-vs-ours-2026-05-16]] — Step 2.4 head-to-head; its `gen_step=1` numbers carry the crack caveat
- [[inter-head-disagreement-2026-05-15]] — JS-radius @ `gen_step=1` (same exposure)
- [[v4-prep-coverage-matrix-2026-05-16]] — 621-cell `gen_step=1` substrate (same exposure)
- [[research-candidates]]ates]] — adaptive / empirical commit-step locus idea; `t=0` logit locus is now a validated elicitation point
- [[claims]] — candidate `[OPEN]` claim entry (commit-step premise re-grounded at a `t=0` logit locus; Phi-3.5 low-decidedness tension)
