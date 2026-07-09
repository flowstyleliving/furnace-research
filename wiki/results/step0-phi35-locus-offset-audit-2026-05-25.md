---
status: OPEN
kind: post-hoc-sensitivity
date: 2026-05-25
---

# Step-0 Phi-3.5 Locus-Offset + Floor Audit `[OPEN — sensitivity only]`

Post-hoc sensitivity audit on the locked [[step0-belief-readout-2026-05-17]] panel. Does **not** amend, re-score, or reinterpret the pre-registered result ([[step0-belief-readout-prereg-2026-05-17]]). Mirrors [[step0-t0-recoverability-audit-2026-05-18]]'s integrity-gate posture: frozen slice + specs, byte-faithful gate, write-only to a new audit dir. Two probes: **Probe A** = locus-offset t=1 on Phi-3.5 only; **Probe B** = decidedness-floor multiplier sweep on all 10 models (CSV-only, no inference).

**Integrity gate (Probe A):** `passed=True`. Max |Δ| = **0.0** (200 rows + 3 canary samples vs locked CSV + frozen canary top-10). Forward pass is byte-faithful; this is a valid reinterpretation of the locked slice.

## Probe A — Locus-Offset t=1 on Phi-3.5

Protocol: append model's own greedy t=0 top-1 token id to the frozen prompt; re-run forward; read softmax at the new last position. Most faithful continuation of the locked measurement. Same 5.0× control_mass floor, same frozen YES/NO shortlist, same scoring rule.

| Metric | t=0 (locked) | t=1 (this audit) |
|---|---|---|
| n_eligible / 200 | 37 | **0** |
| eligible_cov | 0.185 | **0.000** |
| verdict | Low-decidedness-for-M | **Low-decidedness-for-M** |
| Newline-t0 subset: n_eligible at t=1 | — | **0 / 40** |

**Key counts:** `n_t0_above_floor = 37`, `n_t1_above_floor = 0`, `n_newly_below_at_t1 = 37`, `n_newly_above_at_t1 = 0`. The 37 samples eligible at t=0 *collapse* below floor at t=1; the 40 newline-dominated rows recover nothing at t=1 either.

**Interpretation:** The locus-offset hypothesis ("Phi-3.5 emits `"\n"` as a formatting prefix, then commits at t=1") is **wrong**. The t=1 distribution is *more* diffuse than t=0, not less — YES/NO mass concentration peaks at t=0 and then disperses. Phi-3.5's commit-locus is not at t=1 under the greedy-append protocol. The newline-dominant rows are not a formatting-prefix artifact; they reflect a genuine distributional pattern where YES/NO mass is low at the first generation step.

## Probe B — Decidedness-Floor Multiplier Sweep (All 10 Models)

Coverage and signed B-AUROC at each floor multiplier. Verdict: R = Recoverable-for-M (eligible_cov ≥ 0.80, CI_lo > 0.50), L = Low-decidedness-for-M. Locked multiplier = **5.0x** (bold column).

| Model | 2x | 3x | 4x | **5x** | 6x | 8x | 10x |
|---|---|---|---|---|---|---|---|
| Llama-3.1-8B | 1.00/0.868(R) | 1.00/0.868(R) | 1.00/0.868(R) | **0.99/0.868(R)** | 0.98/0.865(R) | 0.95/0.876(R) | 0.92/0.877(R) |
| Llama-3.2-3B | 1.00/0.780(R) | 1.00/0.780(R) | 1.00/0.780(R) | **1.00/0.780(R)** | 1.00/0.780(R) | 0.99/0.780(R) | 0.98/0.781(R) |
| Mistral-7B-v0.3 | 1.00/0.823(R) | 1.00/0.823(R) | 1.00/0.823(R) | **0.99/0.829(R)** | 0.99/0.829(R) | 0.99/0.829(R) | 0.99/0.827(R) |
| Mistral-Nemo | 1.00/0.906(R) | 1.00/0.906(R) | 1.00/0.906(R) | **1.00/0.906(R)** | 1.00/0.906(R) | 1.00/0.906(R) | 1.00/0.906(R) |
| **Phi-3.5-mini** | **0.61/0.897(L)** | **0.41/0.916(L)** | **0.29/0.926(L)** | **0.18/0.942(L)** | **0.13/0.938(L)** | **0.07(—)** | **0.03(—)** |
| Phi-4-mini | 1.00/0.840(R) | 1.00/0.840(R) | 1.00/0.840(R) | **1.00/0.840(R)** | 1.00/0.840(R) | 0.98/0.842(R) | 0.97/0.841(R) |
| Qwen2.5-7B | 0.99/0.923(R) | 0.99/0.923(R) | 0.99/0.923(R) | **0.98/0.926(R)** | 0.97/0.926(R) | 0.96/0.925(R) | 0.96/0.924(R) |
| Qwen3-1.7B | 1.00/0.727(R) | 1.00/0.727(R) | 1.00/0.727(R) | **1.00/0.727(R)** | 1.00/0.727(R) | 1.00/0.727(R) | 1.00/0.727(R) |
| Qwen3-8B | 1.00/0.889(R) | 0.99/0.888(R) | 0.99/0.888(R) | **0.99/0.888(R)** | 0.99/0.888(R) | 0.99/0.888(R) | 0.99/0.888(R) |
| gemma-3-4b | 1.00/0.799(R) | 1.00/0.799(R) | 1.00/0.799(R) | **1.00/0.799(R)** | 1.00/0.799(R) | 1.00/0.799(R) | 1.00/0.799(R) |

*Format: eligible_cov / signed-B-AUROC (verdict). — = no eligible samples (AUROC undefined).*

**Key finding:** Phi-3.5 **never reaches 0.80 coverage at any tested multiplier.** Its maximum is 0.61 at 2x (the most lenient setting). The 9 other models all remain Recoverable-for-M at every multiplier including 10x. This gap is structurally model-specific, not an operating-point artifact. Reducing the floor does not rescue Phi-3.5's eligibility — it merely widens which samples are counted, but the model's YES/NO mass is insufficient across the board.

Secondary observation: Phi-3.5's conditional AUROC *improves* as the floor rises (0.897 at 2x → 0.942 at 5x locked → 0.938 at 6x), because at stricter floors only the cleaner subset is included. Its signal, when present, is actually strong — the problem is breadth, not quality.

## Verdict

- ❌ **Locus-offset artifact** — NO. t=1 coverage = 0.000; the 37 eligible-at-t=0 samples all collapse at t=1. t=0 is already the highest-mass locus.
- ❌ **Floor-bound artifact** — NO. Phi-3.5 stays Low-decidedness-for-M even at 2x floor (cov=0.61), while all 9 peers are Recoverable at 10x floor. The gap is model-intrinsic.
- ✅ **Real low-decidedness state — confirmed.** The locked `Low-decidedness-for-M` verdict survives the full two-axis neighborhood. Phi-3.5's literal YES/NO mass is genuinely sparse at t=0 and does not concentrate at t=1.

**Implication for v4:** Phi-3.5 cannot serve as a belief-readout panel model under the literal YES/NO measurement framework, regardless of locus or floor choice. It may be retained for RAUQ/SinkProbe/attention metrics (which do not require belief-readout eligibility), but must carry an explicit caveat that its `gen_step=1` attention readings are not anchored by a valid belief-locus measurement. **Do not falsify** on RAUQ/attention metrics — the audit concerns the belief-readout locus only; different measurement channel.

Open question: *why* is Phi-3.5's YES/NO mass this diffuse? Candidates: (a) tokenizer splits affirmative/negative across multiple subword tokens, diffusing mass across a wide vocabulary; (b) instruction-tuning style pushes first-token mass toward formatting (newline, `"I"`, `"The"`); (c) model size — Phi-3.5-mini is the smallest model in the panel. Not Step-3-blocking; worth a dedicated tokenizer-mass diagnostic if Phi-3.5 is needed in the panel.

## Propagates to / read alongside

- [[step0-belief-readout-2026-05-17]] — the locked panel (unchanged by this audit)
- [[step0-belief-readout-prereg-2026-05-17]] — frozen rule (unchanged)
- [[step0-t0-recoverability-audit-2026-05-18]] — prior audit (shortlist axis settled); Phi-3.5's `"\n"` dominant non-literal top-1 was the empirical clue tested here
- [[claims]] — rider on the `[OPEN]` step-0 entry: Phi-3.5 low-decidedness survives neighborhood audit; real model state, not artifact

## Artifacts (repo)

- `experiments/v4-mech-prep/2026-05-25/audit-phi35-locus-offset/` — `Phi-3.5-mini-instruct-4bit_t1_locus_offset.{csv,json,log}` + `floor_multiplier_sweep.{csv,json}` + `floor_sweep.log`
- `scripts/audit_locus_offset_phi35.py` — Probe A (integrity-gated t=1 forward pass; read-only on locked artifacts)
- `scripts/audit_floor_multiplier_sweep.py` — Probe B (CSV-only floor sweep; no inference)
