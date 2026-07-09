# 🚢 Where We Are, ELI12

**Rigorous version:** [pri-v3-plan](../pri-v3/pri-v3-plan.md) + [results/summary](../results/summary.md) + [results/v3.2-results](../results/v3.2-results.md) (current verdict)
**Companion (current dashboard):** [methods-catalog-eli12](methods-catalog-eli12.md) · **(start-here concept):** [null-space-eli12](null-space-eli12.md)

> 🔄 **2026-05-15 refresh.** The ship sailed (v3 sealed gate passed), a retrofit failed (v3.2 centered-Fisher), and we pivoted from "find the universal gauge" to "calibrate each gauge per ship and per route" — production library `pri_calibrator.py` + `pri_detector.py` shipped. The fleet metaphor in §"Where we actually are (2026-05-15)" below extends the original ship picture. The 2026-04-18 dock-state block is preserved as historical context.
>
> 🔄 **2026-04-18 refresh.** New unifying metaphor, plus Prereq 4 mid-flight state and the Opus 4.7 adversarial findings that landed today.

---

## 🎯 The question

Can we detect when a language model is about to say something wrong — not by reading the output, but by watching how its hidden state moves at the exact moment it commits to the next word? That's Furnace. PRI v1 → v2 → v3 is the story of getting that measurement right. v3 has now passed its sealed gate, the v3.2 retrofit was rejected, and the current chapter is *deploying* the measurement — turning a "does it work" question into a "for this exact model on this exact data, how do we calibrate it" library.

---

## 🚢 The metaphor: commissioning a new ship

Think of PRI v3 as a ship we've built in dry dock. Before she sails on her maiden voyage, every ship goes through the same ritual:

- 🏗️ **The hull** = PRI v2. Proven. Doesn't change. Carries us on every voyage.
- ⚙️ **The new engine** = the direction metric `null_ratio`. Replaces v2's magnitude-only engine. Instead of asking *"how hard is the model pushing?"* we ask *"is it pushing on the controls that actually steer the ship, or on decorative knobs that do nothing?"* 🎛️
- 🧰 **Pre-launch checks (prereqs)** = small experiments on instruments before leaving the dock. Each one is cheap and has to pass.
- 🔍 **Inspectors (adversarial reviewers)** = outside eyes who walk the deck and try to find what the builders missed. Codex, Opus 4.7, and Grok each see differently — that's why we use multiple.
- 🧪 **Sea trials (dry-run)** = a short loop in protected water before committing to open ocean.
- 🌊 **Maiden voyage (main run, n=50/cell)** = the real measurement. Expensive to abort mid-crossing.
- 🏁 **First port of call (publication)** = arrival proves she works in the wild.
- 🚤 **The rival ship (HARP)** = another lab launched a similar ship last week with a simpler engine. Our bet is that *our* engine — which weighs each control by how much it actually steers — beats theirs. E17b is the side-by-side race.

---

## 📊 Where we actually are on the dock (2026-04-18)

✅ **Hull signed off.** v2 beats v1 on all three models. Signal lives at *commitment* (step 1), not output.

✅ **Engine installed.** Option A (single fixed final-p eigenspace) is the v3 default. A fancier variant (Option C) was tested and rejected.

✅ **Two engine bugs caught by inspectors before they mattered.** Codex flagged a reversed pressure gauge (E22 `argmax` → `argmin`) and a missing vacuum seal in front of a measurement port (E23 forgotten final-norm). Both fixed. Honors to the inspectors. 🏅

✅ **Qwen engine diagnostic (Prereq 8) — CLOSED.** Qwen looked "flat" in E22 — turned out that was the same missing-seal bug above. Post-fix, all three engines show the same shape: late-rise at the final layer. Magnitudes differ, shapes converge.

🚧 **Prereq 4 (shared-pipeline plumbing) — UNDER INSPECTION RIGHT NOW.**
The engine works in a test rig but has to be bolted into the ship's production wiring before we sail. We wired it today and Opus 4.7 just handed over its inspection report:

- ⚠️ **1 possible showstopper (H4)**: a dictionary collision that *might* make the new code crash on the very first run. Either a real short-circuit or a mis-reading — cheap to verify by running the sea trial.
- ⚠️ **3 real findings** (H3, H2, M1): the sanity check uses an unmeasured tolerance, validates a gauge the downstream code might not use, and has a threshold that can't be shown to catch the specific fault it's supposed to catch.
- 🕒 **Codex inspector is on rate-limit cooldown** until 2026-04-24. He'll do the final walk-through before we sail.

✅ ~~**Falsification paperwork contradicts itself.**~~ **Signed off 2026-04-18.** Harbor master rule in place: only E17 / E17b / E18 / E19 failures can cancel the voyage; E20 / E21 / Qwen diagnostic only reshape the route.

✅ ~~**E18 analysis plan underspecified.**~~ **Frozen 2026-04-18.** Per-model logistic with `null_ratio + d_F + interaction`, linear residualization, AUROC ≥ 0.60 with non-overlap bootstrap CI on ≥ 2 of 3 primary models. No post-hoc tweaks after seeing confirmatory data — the analysis is sealed. 🔐

🚧 **Prereq 4 dry-run spec sealed 2026-04-19.** The spec is written (schema + schedule + provenance + tripwire + fault-injection + dict-collision + consumer-audit asserts, all in `pri-v3-plan.md §Prerequisites.4`). Still need: implementation in production pipeline, the `v3_capture_dryrun.py` script, a green run across all three models, and the Codex final walk-through (cooldown lifts 2026-04-24).

---

## 📊 Where we actually are (2026-05-15) — the fleet is sailing

A month past the dry-dock photo. The ship sailed her maiden voyage in late April. Two retrofits were tried and rejected, one promising direction was abandoned, and the conceptual map shifted: we're no longer building *one* ship — we're building a **calibration manual for a fleet**.

✅ **Maiden voyage completed (2026-04-23).** v3's sealed E18 gate PASSED 3/3 primaries at rank 1 (Llama 0.86, Mistral 0.86, Qwen 2.5 0.73). Replicated on a fresh seed in v3.1 (April 24-25). The direction metric `null_ratio_post_rank1` is real and reproducible. 🏁

❌ **Retrofit #1 rejected — the "fancier intake" (v3.2 centered Fisher).** We tried bolting in a finer-grained Fisher metric (`−ppᵀ` correction). On paper it should be more correct — the proper softmax Fisher pullback. In practice it tanked: Qwen 3 recovery failed, Llama and Mistral regressed by 0.1+ AUROC, `kl_discharged` scattered. All three pre-registered criteria failed at the sealed plane. **[FALSIFIED] 2026-05-10.**

❌ **Retrofit #2 rejected — the "smarter pilot" (adaptive-step).** Idea: instead of always reading the gauge at gen_step=1, let an algorithm pick the optimal step per sample. At pilot scale (n small) it looked universal. At n=200 it held on 3/6 models and *lost* to best-fixed-step by 0.30–0.49 AUROC elsewhere. Step-localization is real but `commit_step` isn't always the right step. **[DEGRADED].**

🪦 **Retrofit #3 abandoned — the "universal weather forecaster" (meta-classifier).** Idea: predict the best (step, metric, rank) cell per model from features like model family. The 33-profile ANLI sweep (11 models × 3 adversarial rounds × n=50) killed it definitively: even within ONE model on R1 vs R2 vs R3, the winning cell + sign flipped. Fisher r=2 @ step 3 (a cell that looked stable at n=5) turned out to be noise — 17 positive signs, 15 negative signs across 32 finite profiles. **[RETIRED] 2026-05-13.**

🛠️ **What we shipped instead — `pri_calibrator.py` + `pri_detector.py`.** Two-file library, in repo (commits 41d91e4 + 36ffbc7). Workflow: hand it a labeled `.jsonl`, get back a `CalibrationProfile` JSON pinned to *this exact model on this exact deployment data*. Profile records the winning `(cell, sign, threshold)` plus an out-of-bag bootstrap CI that re-runs cell selection inside each resample (so the CI isn't post-selection-biased) and a stack of deployability warnings (winner_unstable, wide_ci, oob_low_auroc, large_oob_in_sample_gap, insufficient_coverage). The detector refuses to score if the pipeline hash drifted, the output-projection kind changed, or the profile schema is older than v1.1. **Byte-exact reproducibility self-test passes; 50/50 tests green.** 🚢⚙️

🌊 **Why the pivot makes sense.** Three independent retrofits failed to find a *universal* (model-agnostic, distribution-agnostic) gauge cell. The 33-profile sweep showed that within a single broad task family ("NLI"), changing the adversarial generation distribution between rounds flipped winning cells *for the same model*. Insisting on universality was the obstacle. Per-(model, exact distribution) calibration is the honest framing — full conceptual jump in [calibration-pivot-eli12](calibration-pivot-eli12.md).

🧪 **Two open instruments being trialed (2026-05-15).** Both run *without* using `W_u` at all — pure attention-side or output-spread-side signals.
- 🟡 **Inter-head JS-radius** — Jensen-Shannon disagreement across attention heads at commit step. Mistral + Qwen 2.5 show the SAME sign at the final layer for the first time ever in any non-trivial geometric channel, but Qwen's AUROC magnitude collapses (0.74 → 0.60). Pending Llama 3B + Qwen3 8B replicate for full 4-model invariance test.
- 🟡 **Δσ_onaxis** — bivariate (null · on-axis-spread). Leaning negative as a universal. But Δσ_n ALONE wins on Phi-3.5 (sign −) and Phi-4 (sign +) with opposite signs — within-Phi-family follow-up worth doing.

📮 **Paper status.** Round-1 revision shipped to `paper/pri-draft.tex` (2026-05-02). Junjie Hu (HARP first author) replied warmly to outreach 2026-05-06 — flagged the Fisher-reweighting-vs-static-SVD partition as a "meaningful extension of the original perspective." Substantive feedback still pending; anticipated probes tracked at [feedback/hu-anticipated-probes](../feedback/hu-anticipated-probes.md).

---

## 🧘 Meta-lessons you'll see repeated

- 🔍 **Inspectors catch engine bugs the builder can't see.** Happened on E22, E23, the plan itself, Prereq 8's script, and now Prereq 4.
- 🔢 **A gauge without a calibration mark lies.** Random `null_ratio` ≈ 0.995 — a reading of 0.99 looks "high" but means nothing. Always subtract the baseline.
- 🔩 **Apply the final seal before reading the gauge.** Raw block output ≠ post-norm output. The missed seal silently inflated numbers on both E22 and E23.
- 🗺️ **Probe every compartment.** Sparse sampling of layers hides structure. Full-density every-layer capture is cheap and catches it.
- 🌐 **Universality is the obstacle, not the goal.** Three retrofits (centered-Fisher, adaptive-step, meta-classifier) chased a model-agnostic gauge in 2026-05; all three failed. The signal is real but per-(model, exact distribution). Calibrate, don't generalize.
- 📐 **Audit the operating point before falsifying.** v3 was almost called dead on 2026-04-23 at rank 32 (0/3 PASS) — until the same-day rank sweep showed rank 1 PASSED 3/3. Localized nulls are common; sweep the unpinned-parameter neighborhood before writing `[FALSIFIED]`.
- 🔬 **Small-n looks stable; n=200 is honest.** Multiple retrofits had pilot-scale "this is universal" claims that died at n=200 (adaptive-step, Fisher r=2 @ step 3). The ANLI sweep then showed even *winner stability* is a real metric to report alongside AUROC.

---

## 🎯 One-sentence takeaway

> The maiden voyage succeeded, three retrofits failed, and we discovered the question was wrong: not "find the universal gauge" but "calibrate this gauge for this ship on this route." The fleet sails with `pri_calibrator.py` + `pri_detector.py`. 🚢⚙️📋
