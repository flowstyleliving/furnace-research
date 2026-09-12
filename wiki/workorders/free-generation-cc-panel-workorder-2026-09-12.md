# Free-generation run — does CC's panel predict the model's OWN answer correctness? — work order, 2026-09-12

**Status:** DRAFT PLAN (steward, 2026-09-12). Decisions D1–D5 pending MK. Nothing scored, nothing frozen.

## Goal

Test the one question every reviewer named as CC's missing piece: **does the commit-moment panel predict whether
the model's own freely generated answer is correct?** Every CC task so far supplied the candidate under judgement,
so the label was a property of the input. Here the model writes its own answer, and the label is whether that
answer is right.

**Construct, stated exactly:** `closed_book_short_answer_incorrectness` under a forced-commit prompt — closed-book
TriviaQA, one short greedy answer, exact-match against the official normalized aliases. **Not "hallucination."**
Exact-match failure still mixes confident invention with valid-but-unlisted aliases and ambiguous references;
the human audit measures that mix rather than assuming it away.

## What already exists — reuse it, do not rebuild it

The token-budget pilot (candidate #17, [[workorders/token-budget-pilot-workorder-2026-09-02]]) built most of the
labeling side and put it through three adversarial review rounds.

- 🧊 **Frozen protocol** `commit-confluence/exploratory/token-budget/freeze/protocol.json`, id
  `furnace-token-budget-pilot-v2-forced-commit`: pinned dataset revision, a 3,000-row SHA-ordered question pool,
  **500 reserve rows (positions 3000–3499) for any empirical sign or calibration step**, the official-normalizer
  subset, a precedence-ordered answer contract, and chat templates pinned for `qwen2`, `llama3` and `phi3`.
- ✍️ **Amendment A1-forced-commit** — *MK, verbatim: "Take out pass"*, 2026-09-02. The prompt now forbids
  abstention, because the abstention-permitted probe measured 39% of rows as `UNKNOWN`, **62% of the entire error
  class**. ⚠️ **This decision was never recorded in `log.md`, and the token-budget order's §12b still lists it as
  open.** Both corrected by this session's log entry.
- 🧪 **The forced-commit probe already ran** (Qwen2.5-7B, n=200), and its base rate was never computed. Computed
  2026-09-12: **112 correct (56.0%) / 88 incorrect (44.0%)**, **200/200** valid answers, **0** abstentions, all
  `eos`, median **3** tokens (14% single-token). Incorrect answers read as confident wrong entities ("Endora
  Clevyleaf", "Whole Lot of Fun", "Bangladesh famine"). Near-balanced, so `n = 2000` yields ~880 errors per model.
- 🔧 **Scripts:** `generate_answers.py` (resumable, fsynced, banks `prompt_sha256` per row),
  `audit_generated_labels.py` (base rates, class gates, blinded human-audit queue), `audit_triviaqa_task.py`
  (already run), `power_knee.py`. On the CC side: the vendored extraction, the sealed selector,
  `stage_b/analysis/operating_points.py`, `lexical_baseline.py`, `panel_vs_simple.py`.
- ⚠️ **The whole token-budget lane is UNTRACKED in git** — ten days of code, freeze artifacts and generations in
  `commit-confluence/exploratory/token-budget/`, never committed. Decision D5.

## Design

### 1. Labels
Greedy primary answers under the frozen protocol, `n = 2000` per model from the pool's first 2,000 positions.
Primary label: exact match. **Blinded human audit** per the protocol (match and non-match strata) reports the
exact-match grader's disagreement rate by cause — above all `alias_incompleteness_false_negative`, the case where
a detector could win by predicting spelling rather than knowledge.

### 2. Scores — the prompt-identity trap, handled first
The CC panel (27 banked signals + 2 fusion) is extracted on **exactly the prompts that produced the labels.** This
is where the earlier P3 review predicted a silent failure, and the code confirms the risk:

- 🔀 The lane renders a **system + user chat template**; CC's extraction wraps a raw `prompt` string through a
  per-model strategy. All three pinned models are **pass-through** in CC (`PROMPT_STRATEGY_BY_MODEL` covers only
  Mistral-Nemo, gemma-3-1b and dolphin), so feeding the lane's rendered string reaches them byte-for-byte.
- 🔁 **Double-BOS hazard.** The trace tokenizes with plain `tokenizer.encode(text)`. Llama-3's rendered template
  already begins with `<|begin_of_text|>`, so extraction can prepend a **second** BOS token. That would silently
  change exactly what `bos_mass` and the sink statistics read, on an input the labels never saw.

**Registered identity checks, per row, fail-closed:** (a) prompt **token IDs** identical between generation and
extraction, BOS count included; (b) extraction's greedy first token equals the generation's first token;
(c) `prompt_sha256` matches. Any mismatch aborts the model's cell. Implemented as an **additive overlay** in
`commit-confluence/exploratory/free-generation/`; the vendored core and the sealed selector are imported read-only.

### 3. Report pre-selection and post-selection signals separately
From tonight's capture-position work ([[references/commit-locus]]): **ACE and `surprise`** are available before the
answer token is chosen; `null_ratio`, RPV, `p_max` and fusion only after it is fed back. Any "catch it before the
model commits" statement may rest **only** on the first group. Both groups are scored and reported side by side.

### 4. Comparators — enumerated now, before any data exists
The project's most repeated failure is analysing a set it never enumerated. The full comparator set:

- 🎚️ **C1 first-token confidence** — `surprise`. (Pass-one `p_max` equals `exp(-surprise)` under greedy decoding,
  so it is **not** a separate comparator.)
- 📏 **C2 whole-answer confidence** — mean token log-probability of the full greedy answer. Stronger than C1, and
  available only after the whole answer exists.
- ❓ **C3 question-only difficulty** — TF-IDF plus logistic regression on the question text alone, grouped CV. **The
  construct guard:** if the question text predicts correctness as well as the panel, the panel may be reading
  *question difficulty* — an input property — rather than the model's state. This is the three-target trap in its
  free-generation form.
- 👥 **C4 cross-model difficulty** — the fraction of the *other* models that got the question wrong, leave-one-model
  -out. The strongest "it is just a hard question" baseline; needs ≥ 2 models.
- 🧮 **C5 all-signals logistic regression** — because it beat the select-one selector on BENCH
  ([[results/cc-baselines-2026-09-10]]).
- ✂️ **C6 answer length in tokens** — a cheap shortcut check.

### 5. Endpoints — proposed, to be frozen before scoring (decision D4)
- 🎯 **FG1 (primary):** geometric nested-OOB CI lower bound > 0.50 on own-answer correctness, per model.
- ⚖️ **FG2 (the decisive one):** incremental AUROC of the geometric panel **over C1 + C2** ≥ **+0.02**, CI excluding
  0, per model — the shape of RPV's H1. Beating chance is easy when confidence already carries the signal; beating
  confidence is the claim that matters.
- 🧱 **FG3 (construct guard):** the panel beats **C3 and C4** with paired CIs excluding 0.
- 📊 **FG4 (descriptive):** operating points (`operating_points.py`), the pre- vs post-selection split, and a
  **first-token determinacy tautology guard** — if first-token identity alone predicts the label above 95%, flag
  the cell, as the PRI validity panel's guard does.
- 🔁 **FG5 (descriptive):** leave-one-model-out transfer of a fixed signal when each model has its **own** label
  function — the P3-specific generalization test.

**Orientation:** a priori, or fitted on the reserve rows 3000–3499 only. Never on scored rows.

### 6. Scope and precedence
Within-lane comparisons only. **Never pooled** with the sealed core or BENCH: same extraction code, different task
and prompt. Cannot move any registered CC verdict. MLX 4-bit, local.

## Phases

- ⬜ **Phase 0 — gates, no scoring.** (0.1) close the two propagation gaps above; (0.2) forced-commit base-rate
  probes for Llama-3.1-8B and Phi-3.5-mini, n = 200 each — **the bars cannot be set until every model's base rate
  is known**; (0.3) identity-check smoke on 20 prompts per model — token IDs, BOS count, first token; (0.4) run the
  tautology guard on the probe data.
- ⬜ **Phase 1 — pre-registration.** Codex drafts; Astra and Seek review in parallel, at most two rounds; MK freezes.
- ⬜ **Phase 2 — generation and audit.** Greedy answers, `n = 2000` per model; MK completes the blinded audit queue.
- ⬜ **Phase 3 — extraction and single-look analysis.** Identity checks, panel extraction, all comparators, FG1–FG5,
  then the eleven-surface propagation.
- ⬜ **Phase 4 — write-up.** Where it lands (a CC section, or a separate note) is decided after Phase 3, not before.

**Compute:** local M4, `$0`. Short greedy answers plus one extraction pass per row; CC's BENCH ran 1,000 rows × 10
models × 6 tasks on the same machine, so 2,000 × 3 is well inside the envelope. Disk: ~25 GiB free on record.
**Not on the FAR.AI critical path** — the CC deposit should not wait for this.

## Decisions for MK

- 🧭 **D1 — scope:** the three pinned models first, or the full ten-model CC cohort? (Ten needs new templates for
  Mistral, Gemma and Qwen3 — Qwen3 with thinking disabled, or it reproduces the truncated-reasoning trap.)
- 🔍 **D2 — audit size:** 200 blinded judgments per model (the protocol's number) or 100?
- 🧩 **D3 — ordering against the token-budget pilot:** run this first on the shared greedy labels, leaving that
  pilot's 20-sample bank for later?
- 📐 **D4 — bars:** accept FG1–FG3 as proposed, or change them? Whatever is chosen is frozen before scoring.
- 💾 **D5 — commit the token-budget lane**, which has sat untracked for ten days?

## Handoff

- **Codex:** authors the overlay and the pre-registration draft; runs nothing.
- **Claude:** runs the probes, the identity checks, the run and the analysis; verifies every reviewer finding
  against artifacts before acting.
- **Seek + Astra:** review the pre-registration, bounded to two rounds.
- **MK:** D1–D5, the blinded audit, and authorization for Phase 2.
