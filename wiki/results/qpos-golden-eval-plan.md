# 🅿️ Q-POS Golden-Query Eval — Plan & Gates

**Status:** `[PLAN]` — pre-registration draft, frozen-before-data (2026-06-05)
**Project:** SGA (Semantic Graph Agent) — applied cousin of the PRI line, *separate repo*
**Subject under test:** 8-signal `MemoryRanker` (adds `instability` 0.07 + `perturbation_spread` 0.05) vs 7-signal baseline
**Harness:** `~/Documents/SemanticGraphAgent/scripts/eval_golden.py`; labels in `data/golden_queries.json`
**Companions:** [[260605-q-pos-memory-salience-eli12]] (ELI12), [[260515-calibration-pivot-eli12]] (the per-(model,distribution) lesson), [[research-candidates]] (#4 meta-classifier **RETIRED**), [[results/triviaqa-pilot-2026-05-25]] (1/9 cross-task cell match), [[results/v4-sealed-2026-05-26]] (partial transfer)

---

## 🧭 TL;DR

We are **not** trying to prove "Q-POS improves ranking." We are trying to prove a **differential, signed, do-no-harm** claim: *adding the instability signals surfaces memories the user is genuinely uncertain about — on uncertainty-probing queries specifically — without degrading neutral queries, and the sign that does this is fixed before we look at the test data.* Everything below exists to keep this from becoming the meta-classifier: a number that looks great on one distribution and dies on the next.

---

## §0 — Context & two harness defects to fix first

What exists (simulated, 25 memories, 8 queries): 8-signal wins mean NDCG@5 **+0.044**, 4W/2L/2T. That result is **not yet admissible** because of two grounded defects in the current harness:

- 🔁 **Circularity (label leakage).** `build_simulated_store()` sets `instability += 0.25` whenever the memory text contains `uncertain_keywords` ("might", "questioning", "doubt", "wrong", …). The golden `expected_top` for the uncertainty queries are precisely those keyword-bearing memories. The signal is being graded against the same lexical feature it was synthesized from → the win is partly tautological. **Real labels must be produced blind to hedge-word presence** (see §3).
- ⚖️ **Confounded baseline.** `compare_rankers()` gives the 7-signal ranker `similarity=0.45`; the 8-signal ranker uses the new `WEIGHTS` (`similarity=0.40` + the two new weights, with `strength` 0.20→0.18 and `recency` 0.15→0.12). The measured Δ therefore conflates *"added Q-POS"* with *"reshuffled six other weights."* **The admissible comparison holds the six shared weights fixed and only toggles the two new signals on/off, renormalizing to sum 1.0.** Anything else is not an ablation of Q-POS.

These are **Gate G0** below — fix before any real-data run is meaningful.

---

## §1 — What are we actually trying to prove?

### Hypothesis (H-QPOS)
> The instability signals (`instability` = Fisher-ℏ / NLL-surprise; `perturbation_spread` = MDL-ℏ / Gini) carry **epistemic-state information about the user that the other six signals do not** — specifically, *how unsettled the user is about a memory* — and using it improves retrieval on queries that ask about that epistemic state, in the **correct direction**, **without harming** queries that don't.

### Success criterion (falsifiable, pre-registered)
Let Δ(q) = NDCG@10₈ₛᵢ𝓰 − NDCG@10₇ₛᵢ𝓰 on the **clean ablation** (§0 G0). On a **held-out test split** of the golden set, **all four** must hold:

- ✅ **Differential win.** On the *uncertainty-probing* subclass, bootstrap 95% CI lower bound of mean Δ is **> 0**.
- 🧭 **Correct sign.** On the *stability-probing* subclass (e.g. "what am I confident about"), Q-POS must move shaky memories **down**, not up — mean Δ ≥ 0 there too **under the same fixed sign locked on the calibration split**. (If the same sign helps "uncertain" and hurts "confident," it isn't an epistemic signal — it's a popularity/length artifact.)
- 🛡️ **Do no harm.** On the *neutral/logistics* subclass, CI of mean Δ stays within **±0.02** (no regression).
- 📊 **Beats null controls.** Q-POS beats all three negative controls in §3 (shuffle, equal-weight noise, category-only) on the uncertainty subclass.

### What we are NOT allowed to claim
- ❌ A single aggregate "mean NDCG went up." Aggregate can rise while the signal does nothing epistemic (e.g. it just correlates with category, which the boosts already encode).
- ❌ A win whose sign was chosen *after* seeing test results. Sign is locked on calibration (mirrors the PRI calibrator's **sign-locked-from-calibration-data** rule).

### The null we must kill
*"`instability` is a relabeled proxy for things the ranker already has"* — category (`belief`/`identity_core` boosts), text length, or raw similarity. The category-only control (§3) is the sharp form of this null.

---

## §2 — What the golden set needs

The current 8-query file is a **template**, not a test set. A real golden set needs:

### Size
- 🔢 **≥ 30 queries total**, **≥ 6 per intent class** across 5 classes — enough that a per-query bootstrap CI on mean Δ is informative. Furnace anchor: n=50 *examples* still fired deployability warnings in 30/33 ANLI profiles ([[results/v3.2-results]]); here the unit of analysis is the **query**, so we need real query count, not just memory count.
- ✂️ **Split 50/50 into calibration and test** (≥15/15), stratified by subclass. Calibration tunes the weight + locks the sign; test is scored once.

### Diversity — the set must be *adversarial to its own conclusion*
Four subclasses, deliberately including ones where Q-POS should help, hurt, and do nothing:

- 🌪️ **Uncertainty-probing** ("what am I unsure / on the fence / reconsidering / might be wrong about") — Q-POS should help.
- 🧱 **Stability-probing** ("what am I confident / settled about") — Q-POS should help *in the opposite direction* (down-rank shaky). This is the sign test.
- 📦 **Neutral / logistics / factual** ("what appointments", "what's my schedule") — Q-POS should do nothing (do-no-harm).
- 🎭 **Mixed everyday** (goal / relationship / project) — realistic queries where epistemic state is incidental; guards against overfitting to "uncertainty" phrasing.

### What makes a query "golden"
- 🙋 **Real.** A query MK would actually issue to SGA, not a phrasing reverse-engineered from the signal.
- 🙈 **Blind-labeled.** MK writes `expected_top` **without seeing either ranker's output and without keyword-matching for hedge words.** Label from *"which memories do I actually want surfaced here?"*, full stop.
- 🪜 **Graded, not binary.** NDCG uses graded relevance; give 3 tiers (must-surface / nice / irrelevant) so partial credit is meaningful.
- 🧾 **Rationale attached.** Each query keeps the `_rationale` field — the *why* is the audit trail.
- 🧪 **Includes adversarial labels** (see §3): some genuinely-uncertain memories that contain **no** hedge words, and some hedge-word memories that are actually **settled** (quoted, sarcastic, resolved). These are where the signal must earn the win from the model's NLL, not from lexical cheating.

---

## §3 — How we avoid the Furnace lesson

The meta-classifier (#4, **RETIRED** [[research-candidates]]) scored LOO-CV mean 0.971 and still died, for two reasons we must defend against here:

| Furnace failure mode | What it was | Q-POS defense |
|---|---|---|
| 🎯 **Post-selection bias** | Winner picked on the same cells it was scored on; in-sample 0.911 → OOB 0.875 | **Calibration/test split** + **nested OOB bootstrap** when ≥1 free param is tuned (weight, sign, k). Schema-v1.1 method, reused verbatim. |
| 🌍 **Distribution-shift fragility** | ANLI R1/R2/R3 + TriviaQA pick different cells/signs; **1/9** cross-task cell match | **Two golden sets from different slices** of MK's store (e.g. two time windows or two life-contexts); the sign + win must replicate. A win on one slice is a *pilot*, not a verdict. |

Concrete defenses, in order of importance:

- 🔒 **Pre-register before labels exist.** Freeze §1's criterion, the four subclasses, k=10, the bootstrap protocol, and the **sign** of the instability contribution. The frozen block is §7. No edits to it after MK fills labels.
- ✂️ **Lock sign + weight on calibration only.** Sweep the instability weight + sign on the calibration split; carry the *single* chosen (sign, weight) to test. (Directly mirrors the calibrator's "sign locked from calibration data" rail.)
- 🎲 **Negative-control trio** — all three must fail to win on the uncertainty subclass, else the harness is measuring an artifact:
  - 🔀 **Shuffle control:** permute `instability`/`spread` across memory IDs. If a shuffled signal still "wins," the eval is rigged (this is the test that would have caught §0's circularity).
  - 📛 **Noise control:** replace the two signals with equal-weight Gaussian noise. Must not beat baseline.
  - 🏷️ **Category-only control:** instead of Q-POS, just *increase* the `belief`/`identity_core` boosts by the equivalent weight mass. Q-POS must beat this — otherwise it's a worse-encoded category prior.
- 🙈 **Break the circularity by construction.** Because the real signal is computed by an actual model pass (Mistral-Nemo NLL + 8 perturbations), and labels are blind to hedge words, the lexical shortcut in §0 cannot recur — *provided* §2's adversarial labels are present to prove it.
- 🔬 **Report per-query Δ + score trace, never just the mean.** A +0.044 mean that is one query carrying seven is a single-distribution fluke wearing a lab coat. The trace (already logged per memory) shows *why* each memory moved.
- ⚠️ **Honest deployment framing baked in.** The headline can only ever be *"on MK's store, at this snapshot, with sign locked on calibration"* — the same per-(subject, distribution) hedge the PRI line was forced into. No "Q-POS improves memory ranking" sentence without that qualifier.

---

## §4 — Minimum viable proof (and kill conditions)

Two stages; stage A is cheap and can kill the idea before MK spends effort labeling 30 queries.

### Stage A — cheap kill-test (no new labels)
- 🧹 **Fix G0** (clean ablation + drop the circular sim instability). Re-run the existing 8 sim queries.
- 🎲 Run the **negative-control trio** on the simulated store.
- **Kill if:** the shuffle or noise control still "wins" after G0 — means the harness, not the signal, produces the delta. Stop and fix the harness.

### Stage B — MVP real-data proof
- 📝 **12–16 real queries**, blind-labeled by MK, graded, stratified: **≥3 uncertainty-probing, ≥3 stability-probing, ≥3 neutral, ≥3 mixed**, plus **≥2 adversarial-label** memories (uncertain-without-hedge-words, settled-with-hedge-words).
- ✂️ Split 50/50 calibration/test; lock (sign, weight) on calibration.
- ✅ **Pass if** all four §1 criteria hold on the test split *and* the control trio fails.
- ☠️ **Kill / "not deployable as-is" if any of:**
  - CI of mean Δ on the uncertainty subclass straddles 0;
  - the sign that wins on calibration **flips** on test (the exact meta-classifier death — sign instability across splits);
  - a shuffle/noise control wins;
  - do-no-harm fails (neutral subclass regresses > 0.02).

This is the smallest experiment that would convince *or* kill: ~16 queries, one calibration/test split, four pre-registered gates, three controls.

---

## §5 — Metrics beyond NDCG

NDCG scores *ordering against a gold list* but not *whether the right kind of memory surfaced*. Pair NDCG with:

- 🎯 **Epistemic-recall@k** — of memories MK flagged "genuinely uncertain," fraction appearing in top-k for uncertainty queries. Directly measures Q-POS's reason to exist; category-agnostic.
- 🔀 **Rank-lift** — mean change in rank position of *target* (uncertain) memories, 7-sig → 8-sig. Positive = signal is doing its job; decoupled from the gold ordering entirely.
- ⚖️ **Sign-correctness on contrast pairs** — matched (uncertain, settled) pairs on the *same topic*; check 8-signal ranks uncertain-above-settled for uncertainty queries and the reverse for confidence queries. Robust to absolute calibration; this is the SGA analogue of PRI's contradiction-pair design. **The single most Furnace-aligned metric** — it tests the *sign*, which is what dies under distribution shift.
- 📉 **Signal-alone AUROC (OOB)** — treat "MK flagged this memory uncertain" as a binary label; compute AUROC of `instability` (and of the see-saw **tilt** `Surprise − Wobble`, ρ≈−0.91 per [[260605-q-pos-memory-salience-eli12]]) **alone**, with nested OOB CI. Separates *"is the signal informative?"* from *"does the full ranker exploit it?"* — and is the cleanest bridge to the calibrator methodology.
- 🚦 **Do-no-harm Δ** — NDCG delta on the neutral subclass; a first-class reported number, not an afterthought.
- 🧍 **Face-validity spot-check** — does the top-k for an uncertainty query contain memories MK *recognizes* as things he's actually wrestling with? Qualitative, but the ultimate ground truth and a cheap reality check on the quantitative gates.

Report all with **per-query breakdown + bootstrap CIs** (OOB whenever any selection step ran).

---

## §6 — Phased plan & gate table

| Gate | Phase | Condition to pass | Blocks |
|---|---|---|---|
| **G0** | Harness fix | Clean ablation (toggle only the 2 signals, renormalize); circular sim-instability removed | all downstream |
| **G1** | Stage-A kill-test | Shuffle + noise controls **fail to win** after G0 | Stage B |
| **G2** | Pre-registration | §7 frozen; sign + criterion locked **before** real labels | scoring test split |
| **G3** | Stage-B MVP | All four §1 criteria hold on test + control trio fails | any deployment / `[VALIDATED]` claim |
| **G4** | Replication (post-MVP) | Sign + differential win **replicate on a 2nd store slice** | the unqualified claim |

Until **G4**, the claim ledger entry stays `[OPEN]` (per HARD RULE: when in doubt, `[OPEN]` not `[VALIDATED]`).

---

## §7 — Pre-registration block (FREEZE before MK labels)

> **Frozen 2026-06-05.** Edits after labels exist invalidate the result.
>
> - **Primary metric:** NDCG@10 on clean ablation (G0).
> - **Primary criterion:** §1's four conditions, on the held-out test split.
> - **Subclasses:** uncertainty-probing / stability-probing / neutral / mixed (≥6 queries each at full set; ≥3 each at MVP).
> - **Sign:** instability contribution sign is whatever maximizes uncertainty-subclass NDCG **on the calibration split**, then frozen. Recorded value: `____` (fill on calibration).
> - **Free params tuned on calibration only:** instability weight ∈ {sweep}, sign ∈ {+,−}. Everything else fixed at deployed `WEIGHTS`.
> - **Bootstrap:** per-query resample, 10k draws, 95% CI; **nested OOB** because (sign, weight) are selected.
> - **Controls:** shuffle, equal-weight noise, category-only — all must fail to win on the uncertainty subclass.
> - **Secondary metrics (reported, not gating):** epistemic-recall@k, rank-lift, sign-correctness on contrast pairs, signal-alone OOB AUROC, do-no-harm Δ.

---

## §8 — Open risks / known issues

- ⏱️ **The signal isn't installed live.** `instability`/`spread` cost an embed + 8 perturbations + a Nemo pass — too slow for the ranker's deterministic/no-LLM contract. Must be **precomputed at consolidation and stored on the memory** (the eval already injects them as dicts; production needs the column + write path). Out of scope for the eval *result* but blocks deployment even if G3 passes.
- 🔁 **Reproducibility of the signal itself.** Perturbation Gini depends on an RNG seed; NLL uses Mistral-Nemo (the docstring's "Phi-4-mini" is wrong). Borrow the PRI **detector's drift guards** (pipeline-hash + seed pinning) before trusting cross-run numbers.
- 🧮 **Tilt vs two-signal.** [[260605-q-pos-memory-salience-eli12]] found Surprise/Wobble at ρ=−0.91 on 24 toy sentences → the additive pair may collapse to one **tilt** dial. On *real* memories ρ may → 0, in which case both signals carry independent news and tilt throws half away. The eval should report both the two-signal ranker **and** the single-tilt variant; do not pre-commit to tilt on the strength of 24 sentences (post-selection trap).
- 🪞 **Subject-of-one.** MK is the only subject. "Per-(subject, distribution)" is even narrower than the PRI "per-(model, distribution)" framing — the G4 replication across store slices is the *only* thing standing between this and a sample-size-1 anecdote.

---

## Appendix — file pointers (repo, do not wikilink from repo side)
- Harness: `scripts/eval_golden.py` · labels: `data/golden_queries.json` · store: `data/graph.db`
- Ranker: `src/semantic_graph_agent/retrieval/memory_ranker.py` (`WEIGHTS`, `CATEGORY_BOOSTS`, `INTENT_TO_CATEGORIES`)
- Signal source: `src/semantic_graph_agent/uncertainty/semantic_uncertainty.py`
- Related Q-POS evals already in repo: `eval_qpos.py`, `eval_qpos_integration.py`, `eval_instability.py`
