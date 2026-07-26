# Sign-flip coincidence screen — NULL (2026-07-25)

**Status: DESIGNED-RETROSPECTIVE screen, run 2026-07-25 — result NULL.** Not a finding in either direction beyond: the cheap check found no support. Design frozen before execution: `commit-confluence/stage_b/SIGNFLIP_COINCIDENCE_DESIGN.md`, committed in `1f70c9f` (public main), sha256 `fc79d7cbb865d698026667a82d16ec8e5e858f69958307b33ccdf95f4d3c761a`, run verbatim with zero deviations. Run artifact: `commit-confluence/stage_b/profiles_bench/SIGNFLIP_COINCIDENCE_RESULT.json`.

## Question

The BENCH A2 flip trio (Mistral-7B, Mistral-Nemo, Qwen2.5-7B — the three models that confidently invert the fixed `fusion_rank_mean_geom` sign on halueval_qa) is *exactly* the v4 sealed **E_A2 partial-transfer** trio ([[results/v4-sealed-2026-05-26]]). Coincidence, or a real geometry sub-family cutting across family names? The frozen screen asks the cheapest testable version: does trio membership predict per-model fitted sign orientation on the three auxiliary BENCH tasks (`anli_r2`, `halueval_dialogue`, `halueval_summarization`), with the discovery task `halueval_qa` excluded from everything?

## Result — NULL

**Fisher exact (two-sided) p = 0.50**; 2×2 table `[[3,0],[4,2]]` (trio ± × positive-majority ±); odds ratio nonfinite (zero cell). **Positive-orientation majority is simply the cohort norm — 7 of 9 models have it — so trio membership predicts nothing.** No abort fired: all nine frozen cohort models had ≥2 usable auxiliary tasks (the two design-anticipated missing matrices, Qwen2.5-7B/anli_r2 and gemma-3-4b/halueval_summarization, left both models at exactly 2).

Full registered sign table (`fusion_rank_mean_geom`, per-model-task independent fit via the production `_score_candidate`):

| model | trio | anli_r2 | hal_dialogue | hal_summarization | majority+ |
|---|---|---|---|---|---|
| Llama-3.2-3B | — | +1 | −1 | +1 | 1 |
| Llama-3.1-8B | — | −1 | −1 | −1 | 0 |
| **Mistral-7B** | ✓ | +1 | +1 | −1 | 1 |
| **Mistral-Nemo** | ✓ | +1 | +1 | −1 | 1 |
| Phi-4-mini | — | +1 | +1 | −1 | 1 |
| **Qwen2.5-7B** | ✓ | NA (missing matrix) | +1 | +1 | 1 |
| Qwen3-1.7B | — | +1 | +1 | +1 | 1 |
| Qwen3-8B | — | −1 | +1 | −1 | 0 |
| gemma-3-4b | — | +1 | +1 | NA (missing matrix) | 1 |

Sharpest single row against the sub-family reading: **Phi-4-mini (non-trio) is sign-identical to both Mistrals** (+1, +1, −1) across all three auxiliary tasks. Whatever the trio shares, it is not a distinctive auxiliary-task sign signature.

## Interpretation (and its limits)

- 🎲 **The trio↔trio overlap stays a coincidence at this resolution.** The halueval_qa flip cluster gains no support as a cross-task geometry sub-family: on the auxiliary tasks the trio's sign pattern is indistinguishable from the cohort background.
- 🚧 **What this does NOT establish.** The screen is retrospective (matrices pre-existed), the outcome is a coarse per-model majority binary over at most 3 tasks, n=9, and the sign fits are full-data (not OOB). A null here cannot *rule out* a sub-family — it only removes the cheap evidence that would have motivated a registered fresh-data test. Per the frozen design, a real finding would have required fresh-task/fresh-data registered replication regardless of this p-value.
- 📌 **Consequence for canon:** the `[OPEN — untested observation]` entries (claims §11, summary, root orientation) move to **screened-null**; no follow-up registered run is motivated by this result.
- ⚠️ **Caveat on anli_r2:** it is a `systematic_commitment_fail_tasks` member (BENCH §8.1); the screen uses its raw matrices as the frozen design specifies (the design fixed the three auxiliary tasks by name with no admissibility carve-out), so the anli_r2 signs ride on matrices from a behaviorally-degraded task. This cuts against over-reading any single anli_r2 sign, in either direction.

## Provenance

- Design: `stage_b/SIGNFLIP_COINCIDENCE_DESIGN.md` @ `1f70c9f`, sha256 above; frozen predictor (v4 E_A2 membership), frozen cohort (9 models, Phi-3.5 excluded for <2 matrices), frozen cell + tasks, single primary statistic, full-table mandatory reporting, no flexibility clauses.
- Execution: 2026-07-25, `commit-confluence/.venv` python, `analyze_universality.load_cells` + `SEAL._score_candidate` (production fusion append path), verbatim heredoc from the design.
- Cross-refs: [[results/bench-a2-signflip-2026-07-22]] (the discovery observation), [[results/v4-sealed-2026-05-26]] (E_A2 trio), `wiki/claims.md` §11.
