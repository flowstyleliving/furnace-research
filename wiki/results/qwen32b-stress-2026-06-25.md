# Qwen2.5-32B Stress Panel (Modal Torch, 2026-06-25)

**Status:** `[RESULTS - exploratory stress panel]`. Backend = `modal-torch`, precision = `nf4`, n=200 per new task, `n_bootstrap=2000`. **NON-byte-comparable to the sealed MLX plane** and **does not alter the sealed 18/20**.

This was a direct stress run for `Qwen/Qwen2.5-32B-Instruct`: add ANLI R2/R3 and broader shared-label YES/NO factuality tasks on the existing Modal extractor (`/Users/msrk/Documents/furnace-guard/modal_app.py`). Existing Qwen-32B nf4 cells were already run for `anli_r1` and `triviaqa_paired`; this wave adds six task ids:

- `anli_r2`, `anli_r3`
- `truthfulqa_mc`
- `halueval_qa`, `halueval_dialogue`, `halueval_summarization`

## Verdict

**Qwen2.5-32B nf4 is 8/8 deployable across the current torch stress panel.** All six new tasks had `n_aligned=200`, `n_dropped=0`, `yes_no_commit_rate=1.0`, and `controls_pass=true`.

| Task | Geom CI-lo | Deployable | Geom winner | Primary winner / CI-lo |
|---|---:|:---:|---|---|
| `anli_r1` | 0.763 | yes | `attention[last_minus_1_js] @ step 0` | same / 0.763 |
| `triviaqa_paired` | 0.781 | yes | `attention[final_bos_mass] @ step 0` | same / 0.781 |
| `anli_r2` | 0.744 | yes | `attention[last_minus_1_bos_mass] @ step 0` | same / 0.744 |
| `anli_r3` | 0.698 | yes | `attention[last_minus_1_bos_mass] @ step 0` | same / 0.698 |
| `truthfulqa_mc` | 0.730 | yes | `attention[last_minus_1_js_kv_groups] @ step 0` | same / 0.723 |
| `halueval_qa` | 0.809 | yes | `Fusion fusion_rank_mean_geom @ step 0` | same / 0.809 |
| `halueval_dialogue` | 0.539 | yes | `Readout null_ratio_post_rank1 @ step 0` | `Readout surprise @ step 0` / 0.559 |
| `halueval_summarization` | 0.553 | yes | `Readout fisher_eff_rank @ step 0` | same / 0.551 |

## Read

1. **ANLI difficulty gradient holds.** R1/R2/R3 all deployable at nf4, and R2/R3 pick the same penultimate-layer ACE attention cell. The ANLI signal weakens mildly with difficulty (0.763 -> 0.744 -> 0.698) but stays clean.
2. **TruthfulQA stays in the Qwen attention locus.** The winner is `last_minus_1_js_kv_groups`, which is still ACE attention morphology at t=0. This is the strongest "confidence trap" stress cell in the wave and it still passes at 0.730.
3. **HaluEval broadens the locus.** QA is strong but picks Fusion. Dialogue and summarization are marginal and move to readout/surprise. This means the earlier shorthand "Qwen family -> attention" should be scoped to the ANLI/TriviaQA scale panel; broader grounded-dialogue/source-faithfulness prompts can move Qwen into the commit/readout region too.
4. **No behavioral gate failures.** The model attempted every new prompt family: 100% YES/NO on all six full extracts; validation o_proj reconstruction cos=1.0.

## Caveats

- This is **exploratory**, not a registered benchmark expansion. It is useful stress evidence, not a new denominator for the sealed paper.
- HaluEval and TruthfulQA are **stem-paired/grouped** tasks, but the current calibrator uses the standard row bootstrap. Treat the HaluEval dialogue/summarization marginal passes as stress signals, not polished confirmatory benchmark claims.
- HaluEval long contexts were whitespace-normalized and char-limited in the builder so attention capture remained practical. That is appropriate for a stress probe, but a paper-grade benchmark expansion would need a frozen length policy and grouped/cluster bootstrap.
- All tasks are shared-label YES/NO judgment prompts. This still does not cover per-model native generation labels.

## Artifacts

Data and profiles live on the Modal `model-cache` volume:

- Data: `/models/data/<task>_n200.jsonl`
- Data manifests: `/models/data/<task>_n200.manifest.json`
- Reference panel order copies: `/models/refs/<task>.matrix.npz`
- Profiles: `/models/profiles_ext/<task>/Qwen2.5-32B-Instruct.profile.json`
- Matrices: `/models/profiles_ext/<task>/Qwen2.5-32B-Instruct.matrix.npz`

New stress-data hashes:

| Task | Data SHA256 |
|---|---|
| `anli_r2` | `9e2b10aee26b3d13b4f05214329b246a7b84393ee8f390ad96814fa921b81a09` |
| `anli_r3` | `ac65b6a881bdebc857108f0e79d082072e0744cae54638d219f04c1ec977cb8d` |
| `truthfulqa_mc` | `babffaea8c0d95c2c471041a89ca343e3c969119827a8520e0b4b21a65f07b62` |
| `halueval_qa` | `a841d096a3f41162a685994655e5fdd0974176ee35797e73be99e29e5d1c15e0` |
| `halueval_dialogue` | `17d24a4abddf8aaac141dc2cac9be78d80f638ef85943ce0751e9c7b12e66632` |
| `halueval_summarization` | `30bf03bc3c2ad0d2407de497b34c3039b4c7f3228600c58b9721588d91f10396` |

## Commands

Builder added to `/Users/msrk/Documents/furnace-guard/modal_app.py`:

```bash
modal run /Users/msrk/Documents/furnace-guard/modal_app.py --mode build-stress-data --task all --n 200
```

Run pattern:

```bash
modal run /Users/msrk/Documents/furnace-guard/modal_app.py --mode validate --model-id Qwen/Qwen2.5-32B-Instruct --task <task> --n 200 --precision nf4
modal run /Users/msrk/Documents/furnace-guard/modal_app.py --mode extract  --model-id Qwen/Qwen2.5-32B-Instruct --task <task> --n 200 --precision nf4
```
