# Temperature study, Endpoint B: what sampling does to one-token answers (2026-10-12)

**Status:** `[DESCRIPTIVE — Amendment A1, committed before output; Endpoint A NOT RUN]`. Research candidate [[research-candidates#14. Temperature-robustness of the commit-step detector|#14]]. Behavioural only: no detector, panel or AUROC was computed.

## ❓ The question

Every sealed and BENCH result was measured at greedy decoding (temperature 0). Endpoint B asks what happens to the model's one-token YES/NO answer when it is sampled instead: at temperatures 0.7, 1.0 and 1.5, does it give more wrong answers, more answers that are not YES or NO at all, or both?

## 🧪 Setup

- 🧩 **Cohort.** Four MLX 4-bit models at their pinned revisions: Qwen3-8B, Llama-3.1-8B-Instruct, Phi-3.5-mini-instruct, Mistral-7B-Instruct-v0.3.
- 📚 **Data.** All 200 ANLI R1 rows and all 1,000 HaluEval QA rows (500 paired stems), unchanged from the pre-registration.
- 🎲 **Sampling.** One greedy answer per prompt plus 5 draws at each of T 0.7 / 1.0 / 1.5. The draws come from the registered `RandomState(20260826)` stream by inverse CDF over the full vocabulary, with no top-k, top-p or re-drawing. That is 76,800 planned records.
- 📌 **Protocol.** `commit-confluence/exploratory/temp-sweep/AMENDMENT_A1_ENDPOINT_B_2026-10-12.md`, committed and pushed as `ee61a5d` before any full-run output existed. The parent pre-registration (`PRE_REGISTRATION_TEMP.md` v1.3) is unsigned. A1 was written after the [[log]] 2026-10-12 pilot and is labelled post-pilot.
- 🖥️ **Compute.** Local Apple M4 Mac mini, $0. The run took 76.4 min, launched 2026-10-12 21:55 PDT.
- 🔍 **Audits.** DeepSeek V4 Pro reviewed the amendment twice (round 1: 4 major, 3 minor; round 2: 0 blocking, 1 major, 1 minor). Codex `gpt-6-astra` applied every fix. The self-checks passed 12/12.

## ✅ Integrity: the measurement is clean

- 🧷 **Greedy identity.** 4,000/4,000 fresh HaluEval greedy tokens equal the historical BENCH commits, with zero tolerance. That includes the 55 HaluEval prompts whose top-two logit margin is ≤0.15 (near-ties: Qwen 19, Llama 23, Phi 8, Mistral 5).
- 🧱 **Failures.** There were 0 harness failures, 0 sampling-verification failures and 0 corrupt raw lines across all 76,800 records.
- 🔁 **Reproducibility.** The first 320 Qwen3-8B records, which reuse the pilot's draws (20 ANLI rows × 16), match the pilot token for token.
- 🔤 **Parser cross-check.** The independent letters-only parser disagrees with the registered BENCH normalizer on 31 records. This is diagnostic only.

## 📊 Results

Primary error is (invalid + valid-wrong) / observed; no slot failed, so observed = planned. The value in brackets is the share of answers that were not YES or NO. The conditional error, valid-wrong / valid, is in the last column as greedy → T 1.5.

| Model | Task | Greedy | T 0.7 | T 1.0 | T 1.5 | Conditional error, greedy → 1.5 |
|---|---|---|---|---|---|---|
| Qwen3-8B | ANLI | 22.5% [0.5%] | 24.1% [1.8%] | 27.5% [6.0%] | 36.3% [16.5%] | 22.1% → 23.7% |
| Qwen3-8B | HaluEval | 39.3% [0.0%] | 39.6% [0.1%] | 40.5% [1.0%] | 46.4% [12.5%] | 39.3% → 38.7% |
| Llama-3.1-8B | ANLI | 32.5% [0.0%] | 36.4% [0.8%] | 43.1% [6.9%] | **75.2% [59.2%]** | 32.5% → 39.2% |
| Llama-3.1-8B | HaluEval | 24.2% [0.0%] | 25.8% [0.4%] | 28.0% [2.2%] | 49.0% [28.2%] | 24.2% → 28.9% |
| Phi-3.5-mini | ANLI | **41.5% [20.0%]** | 49.1% [31.1%] | 51.9% [32.9%] | 56.5% [39.9%] | 26.9% → 27.6% |
| Phi-3.5-mini | HaluEval | 20.2% [0.0%] | 21.5% [1.0%] | 22.9% [2.6%] | 28.4% [9.2%] | 20.2% → 21.1% |
| Mistral-7B | ANLI | 30.5% [0.0%] | 29.6% [0.0%] | 30.9% [0.1%] | 35.2% [5.7%] | 30.5% → 31.3% |
| Mistral-7B | HaluEval | 22.4% [0.0%] | 23.0% [0.0%] | 23.2% [0.1%] | 26.5% [3.0%] | 22.4% → 24.2% |

## 🔎 Findings

- 📈 **Error rises with temperature in all 8 model × task series** from T 0.7 to 1.5. The behavioural reversal statistic `R = (M(1.0)−M(0.7))·(M(1.5)−M(1.0))` is positive in 8/8. Its bootstrap interval (2,000 joint prompt/stem resamples) excludes 0 in 4/8: Qwen ANLI, Llama ANLI, Llama HaluEval and Phi HaluEval. No reversal appears anywhere; the rise is steepest between 1.0 and 1.5.
- 🔣 **Most of the rise is format breakdown, not more wrong YES/NO answers.** Invalid answers drive the error increase. Among answers that stayed YES or NO, the conditional error moves within ±1 point in four series and rises most for Llama: +6.7 points on ANLI (32.5% → 39.2%) and +4.7 on HaluEval. Compare Llama ANLI's primary error, which rises +42.7 points.
  - ⚠️ **Caveat — selection.** The conditional error is computed only on answers that kept the format. Sampling selects which draws those are, so this result **does not show that the model's judgment is unchanged**. The amendment classes it as a secondary description for this reason.
- 🧮 **Models break in different ways.** Llama degrades most with temperature: it answers ANLI with something other than YES/NO 59% of the time at T 1.5. Phi is format-fragile on ANLI at every temperature, including greedy (20%). Mistral stays at or under 5.7% everywhere.
- 🚧 **Phi-3.5-mini fails the one behavioural gate.** It gives 160/200 canonical ANLI greedy commits against the pre-registered ≥190/200 bar, so that greedy cell is `FAILED`. Phi stayed in by the A1 advance decision. Its ANLI cells at every temperature carry the >25%-invalid format flag, as do Llama's two T 1.5 cells. Flags do not fail cells, and no cell changed another cell's status. **31/32 cells PASS.**
- 🔁 **This is the TriviaQA failure mode again.** Models answer with a content word or start writing a response instead of committing YES/NO, as in the BENCH `triviaqa_paired_rep` cascade (B1). Under A1's per-cell rules this is now measured and reported instead of zeroing a task.

## 🚫 What this does not show

- 🛰️ **Nothing about the detector.** Endpoint A (re-extraction of the 31-cell panel under temperature), detector AUROC, the `fusion_rank_mean_geom` reversal and H-TEMP-1 are **NOT COMPUTED**. They need the §3.7 extractor, which is unbuilt and still behind the funding gate.
- 📜 **Not a confirmatory verdict.** A1 is a descriptive behavioural protocol under an unsigned parent pre-registration. The pilot's first 20 ANLI rows and 10 HaluEval stems are inside this run, not a held-out set.
- 🧪 **ANLI has no historical per-row token reference.** Only HaluEval greedy identity is checked against BENCH. ANLI relies on the ≥95% canonical rule and the row audit.

## 📁 Provenance

- 🗂️ **Run directory.** `commit-confluence/exploratory/temp-sweep/pilot/runs/2026-10-12-endpoint-b-full/`. `SUMMARY.md`, `CELL_SUMMARY.json`, `manifest.json` and the per-model timings are committed as `60a2f80` (local, not yet pushed). The raw JSONL (about 140 MB) and `ACCOUNTED_OUTPUTS.jsonl` stay local and git-ignored.
- ⏱️ **Per-model wall time.** Qwen 1,355 s, Llama 1,209 s, Phi 715 s, Mistral 1,307 s; see [[references/gpu-ledger]].
- 🧾 **Audits.** `.temp-sweep-deepseek-audit-r1-2026-10-12.md` (recovered verbatim from the Codex session log) and `.temp-sweep-deepseek-audit-r2-2026-10-12.md`, at the vault root.
- 🧭 **Lane.** [[workorders/temp-sweep-workorder-2026-08-26]] · [[backlog]] · [[log]] 2026-10-12 and 2026-10-13.
