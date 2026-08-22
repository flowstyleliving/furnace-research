# Commit-Equivalence Intersection Set — Qwen2.5-7B ANLI (2026-06-23)

**Status:** `[RESULTS — supporting finding]` — the pre-reg §4 control, now quantified. Does NOT alter the Precision Ladder verdicts. Full results: [[precision-ladder-results-2026-06-22]].

## 1. What was done

Pre-registered concern (§4 of [[precision-ladder-prereg-2026-06-22]]): if nf4 commits YES on a sample but bf16 commits NO, the rungs aren't scoring the same event — cross-precision AUROC comparisons are contaminated by answer-flips.

**Method:** lightweight commit-dump runs (new `/Users/msrk/Documents/furnace-guard/_commit_dump.py`) on Qwen2.5-7B-Instruct × ANLI R1 at all four rungs `{nf4, int8, bf16, fp32}`. Each run loads the model at the target precision, runs all 200 prompts through one forward pass, and records the argmax commit token. No ACE/RPV extraction — token-level only, \~30s per rung. Artifacts: `commit_dump/Qwen2.5-7B-Instruct[__<precision>]_anli_r1.jsonl` on Modal volume.

## 2. Per-rung YES/NO rates

| Rung | YES/NO | Rate |
|------|--------|------|
| nf4 | 194/200 | 97.0% |
| fp32 | 193/200 | 96.5% |
| int8 | 188/200 | 94.0% |
| bf16 | 187/200 | 93.5% |

nf4 is the MOST decisive, not the least. Quantization nudges commit confidence slightly up, not down. bf16 leaks the most non-YES/NO tokens (13/200).

## 3. Pairwise commit agreement

| Pair | Agreement | YES/NO subset |
|------|-----------|---------------|
| bf16 ↔ fp32 | 90.0% | 93.0% |
| int8 ↔ bf16 | 90.0% | 91.4% |
| nf4 ↔ fp32 | 89.0% | 90.6% |
| nf4 ↔ int8 | 86.0% | 88.8% |
| nf4 ↔ bf16 | 85.0% | 87.7% |

**Full 4-rung intersection (all four commit the same token): 160/200 = 80.0%.**

bf16↔fp32 has the highest agreement (90%) — the two unquantized rungs are most consistent. nf4↔bf16 has the lowest (85%) — **15% of items flip answer between the anchor rung and the near-gold reference.**

## 4. Divergence patterns

40 divergent samples. The dominant pattern is **bf16 flipping YES→NO or NO→YES while 2–3 other rungs agree** — bf16 is the weakest rung in the ladder. A handful of samples leak non-YES/NO tokens (e.g., sample 148: `'To'/'Answer'/'To'/'The'` — fp32 is the only rung that doesn't leak on that sample). nf4 occasionally disagrees with the other three (sample 29: nf4=YES, all others=NO).

## 5. Intersection-set AUROC vs full-set AUROC

Recomputed raw AUROC (no calibration, no OOB) on the full 200-sample set vs the 160-sample intersection set. All matrices from `profiles_ext/anli_r1/`.

| Rung | Full-set best AUROC | Inter-set best AUROC | Δ |
|------|--------------------|--------------------|------|
| nf4 | 0.682 (`neg_shadow_logvol_r1`) | 0.712 (`neg_shadow_logvol_r1`) | **+0.030** |
| int8 | 0.719 (`neg_shadow_logvol_r1`) | 0.736 (`neg_shadow_logvol_r1`) | +0.018 |
| bf16 | 0.746 (`neg_shadow_logvol_r1`) | 0.775 (`neg_shadow_logvol_r1`) | **+0.029** |
| fp32 | 0.710 (`neg_shadow_logvol_r1`) | 0.724 (`att last_minus_1_bos_mass`) | +0.014 |

**Contamination drags AUROC down by +0.015–0.030.** Removing divergent samples consistently improves signal — the answer-flips are genuine noise, not informative variation. Same best cell wins on 3/4 rungs; fp32's winner shift is a tiny 0.014 delta (probably selection noise at that scale).

## 6. Verdict

**Supporting finding — does NOT alter the Precision Ladder verdicts.** The contamination is real but modest: 15% answer-flip rate, \~0.02–0.03 AUROC drag. The pre-reg's H3 falsifier required a ≥0.10 CI_lo drop — this is well below threshold. The fixed-cell precision-invariance result in [[precision-ladder-results-2026-06-22]] holds unchanged.

**Methodological note:** for future cross-precision comparisons, restricting to the commit-equivalence intersection set is a clean \~0.02 AUROC gain for free. Worth standardizing if the precision ladder becomes a recurring analysis.

**Codex review:** skipped per MK. Clean computational result, no adversarial surface.

## 7. Remaining open threads

- 🔍 ~~72B byte-verify~~ — CLOSED (2026-06-23, OOM guard confirmed)
- ✅ ~~Commit-equivalence intersection set~~ — CLOSED (this page)
- 🚫 Llama-3.3-70B validation — HF gating resolved (token now has access); needs re-run
- 📊 Paper fold-in — locus-dissociation + precision-robustness into `cc-draft.tex`
