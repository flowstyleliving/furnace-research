---
status: RESOLVED_LASTQ_NO_PROMOTE
kind: v-norm-attention-prereg
date: 2026-06-09
---
# V-Norm Attention Pre-Reg Draft - 2026-06-09

**Status:** `[RESOLVED - LAST-QUERY V-NORM NO-PROMOTE]` - setup draft plus zero-code audit. No new model run has been launched from this page. The existing ACE last-query V-norm cells do not justify a fresh standalone run. A separate column-sum V-weighting lane remains possible.

**Question:** do value-vector norm features carry attention-side commitment signal beyond routing-only ACE features?

This is not a search for a universal detector. ACE already sealed the broader t=0 attention panel. This follow-up isolates the value-payload part of that panel: whether the model's tell is in where attention points, or in how much value-vector payload the attended positions carry.

## Prior evidence

- [[v4-sealed-2026-05-26]] used the 21-cell t=0 ACE panel with V-norm cells included. Qwen2.5-7B transferred exactly across ANLI and TriviaQA with `final_v_norm_lastq_weighted`; Phi-4-mini selected `mid_v_norm_lastq_weighted` on ANLI but did not transfer exactly.
- [[v4-prep-coverage-matrix-2026-05-16]] found that, at the older gen_step=1 plane, only 1/9 winners was a V-norm cell (`gemma-3-4b` with `mid_v_norm_lastq_weighted`). This argues against "V-norm dominates ACE" as a live hypothesis.
- [[triviaqa-pilot-2026-05-25]] found `v_norm_lastq_weighted` rose on TriviaQA, winning 4/9 models. This suggests task-regime pockets where value payload matters more than routing shape.
- [[rauq-sinkprobe-vs-ours-2026-05-16]] found SinkProbe's value-weighted column-sum variants were competitive, and sometimes stronger than ACE's last-query V-norm approximation. This motivates a two-stage test: first audit the existing ACE V-norm cells; only then consider adding column-sum V-weighted cells.

## Metrics

**Existing ACE V-norm cells** (implemented in `t0-morphology-furnace/pri_calibrator.py`):

| Metric | Meaning |
|---|---|
| `v_norm_bos` | mean L2 norm of the BOS-position value vector |
| `v_norm_max` | mean max value-vector norm across positions |
| `v_norm_lastq_weighted` | current-query attention weighted sum of value-vector norms |

**Routing comparators**:

| Family | Cells |
|---|---|
| attention disagreement | `js`, `js_kv_groups`, `js_no_bos` |
| sink routing | `bos_mass` |
| sealed ACE winner | per-model best cell from [[v4-sealed-2026-05-26]] |

**Possible stage-B cells** (not yet ACE-panel cells): SinkProbe-style value-weighted column sums such as `sink_top1_vw` and `sink_topk_sum_vw`. These require a pre-registered implementation decision before they can be mixed into ACE-style nested OOB selection.

## Stage A - zero-code profile audit

Use existing sealed ACE profile JSONs only:

- ANLI: `t0-morphology-furnace/experiments/t0-sealed/2026-05-26/profiles/anli/*.profile.json`
- TriviaQA: `t0-morphology-furnace/experiments/t0-sealed/2026-05-26/profiles/triviaqa/*.profile.json`

For each `(model, task)` profile, compute:

1. best V-norm cell AUROC and label
2. best non-V ACE cell AUROC and label
3. delta = best V-norm - best non-V
4. whether the profile's selected winner is a V-norm cell
5. whether the OOB profile is deployable enough to cite (`OOB CI_lo > 0.50`, no severe coverage warning, and winner stability reported)

**Stage-A promotion trigger:** at least 3/18 sealed profiles have best-V minus best-non-V >= +0.03, and at least 2 of those are OOB-clean enough to trust.

**Stage-A no-promote trigger:** best-V minus best-non-V is <= +0.01 in the random-effects mean across the 18 profiles, or all positive pockets are warning-dominated.

### Stage-A result - 2026-06-09

Audit command: read-only JSON parse of the 18 sealed ACE profile files under `experiments/t0-sealed/2026-05-26/profiles/{anli,triviaqa}/` in `t0-morphology-furnace`.

Result:

| Quantity | Value |
|---|---:|
| profiles audited | 18 |
| mean(best V-norm AUROC - best non-V AUROC) | -0.0436 |
| profiles with delta >= +0.03 | 0 |
| profiles with delta >= +0.02 | 0 |
| selected ACE winners that are V-norm cells | 3/18 |

Selected V-norm winners:

| Task | Model | Winner | Delta over best non-V |
|---|---|---|---:|
| ANLI | Phi-4-mini | `mid_v_norm_lastq_weighted` | +0.0081 |
| ANLI | Qwen2.5-7B | `final_v_norm_lastq_weighted` | +0.0107 |
| TriviaQA | Qwen2.5-7B | `final_v_norm_lastq_weighted` | +0.0176 |

**Verdict:** the Stage-A no-promote trigger fires. Existing ACE last-query V-norm cells are sometimes selected, especially for Qwen2.5-7B, but the advantage over routing/sink comparators is too small to justify a fresh standalone last-query V-norm run. Do not spend compute on Stage B as written unless the question is reframed.

**Surviving path:** column-sum V-weighting is still live because [[rauq-sinkprobe-vs-ours-2026-05-16]] tested a different payload aggregation (`sink_top1_vw`, `sink_topk_sum_vw`) that is not equivalent to `v_norm_lastq_weighted`.

T0 repo mirror: `t0-morphology-furnace/exploratory/v-norm-attention/README.md`.

## Stage B - fresh small pilot, if Stage A survives

Run a fresh t=0 attention-with-V-norms sweep on the ACE-stable anchors plus stress cases:

| Role | Models |
|---|---|
| ACE-stable anchors | Mistral-7B, Mistral-Nemo, Qwen2.5-7B |
| stress cases | Llama-3.2-3B, Qwen3-8B |

Primary dataset: ANLI R1 n=200, fresh seed. Secondary dataset: TriviaQA paired n=100 only if ANLI produces a non-null value-payload pocket.

Primary acceptance bar:

- V-norm cells add >= +0.03 AUROC over the best routing-only ACE comparator on at least 2/5 models.
- The winning V-norm cell must survive nested OOB with CI_lo > 0.50 and no severe coverage warning.
- Direction is sign-locked from calibration only.
- A shuffled-label control must be flat.

Falsification bar:

- No V-norm cell beats the best routing-only comparator by +0.02 on any OOB-clean model.
- Any apparent V-norm win is explained by BOS/sink contamination (`v_norm_bos` or `bos_mass` moving together with the winner without no-BOS separation).

**Status after Stage A:** do not run this stage for the existing last-query V-norm cells. Re-open only if the target becomes a fresh dataset or a different V-weighted feature family.

## Stage C - column-sum V-weighting, if needed

If Stage A or B shows that last-query V-norms are too weak but SinkProbe column-sum V-weighting remains competitive, file a separate implementation pre-reg before adding new cells:

- `sink_top1_vw`
- `sink_topk_sum_vw`
- optionally no-BOS versions

These should not be silently mixed into the existing ACE panel. They change the feature family and the multiplicity burden.

## First executable command

For a single-model smoke at the sealed t=0 locus:

```bash
PYTHONUNBUFFERED=1 .venv/bin/python -u pri_calibrator.py \
  --model mlx-community/Qwen2.5-7B-Instruct-4bit \
  --data experiments/v4-sealed/2026-05-26/data/anli_R1_seed20260526_n200.jsonl \
  --out experiments/v-norm-attention/2026-06-09/smoke/Qwen2.5-7B-Instruct-4bit.profile.json \
  --task-label v_norm_attention_smoke_anli_r1_20260609 \
  --t0-commit \
  --attention-with-v-norms \
  --n-bootstrap 200
```

Do not treat this smoke as a fresh claim: it reuses sealed ACE data and a lower bootstrap count. Its job is only to verify the command path before a fresh-seed run.

## Open decisions before sealing

- Whether Stage B should reuse ACE's nine-model panel or stay at 5 models for speed.
- Whether the primary effect should be marginal AUROC gain or paired OOB gain against the best routing-only comparator.
- Whether column-sum V-weighted cells belong in this lane or should be a separate SinkProbe-comparison lane.
- Whether to log this as an ACE follow-up or a new research-candidate entry. Current draft treats it as an ACE follow-up, not candidate #11.

## Propagates to / read alongside

- [[v4-sealed-2026-05-26]]
- [[v4-prep-coverage-matrix-2026-05-16]]
- [[triviaqa-pilot-2026-05-25]]
- [[rauq-sinkprobe-vs-ours-2026-05-16]]
- [[inter-head-disagreement-2026-05-15]]
