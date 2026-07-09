# Benchmark Expansion Proposal — commit-confluence

**For:** `cc-draft.tex` ("No Universal Detector, but a Universal Floor") — expansion from 2 → 5–7 benchmarks for a TMLR → NeurIPS submission.
**Author of analysis:** prepared 2026-06-20 from a read of the sealed pipeline (`commit-confluence` + `t0-morphology-furnace`).
**Status:** proposal only — no code written, no data drawn. Decision points flagged at the end.

---

## 0. TL;DR — the recommendation in one table

The pipeline is **benchmark-agnostic at the extraction layer** (proven below), so the binding constraint is *not* "can we run it" — it's *failure-mode diversity*, *label construction*, and *whether each addition stays byte-comparable to the seal*. Recommended set, in priority order:

| # | Benchmark | New failure mode it adds | Framing | Integration | Byte-comparable? | Labels |
|---|---|---|---|---|---|---|
| 🥇 P1 | **HaluEval** (QA + Summarization + Dialogue subsets) | source-faithfulness (summarization), grounded-dialogue, multi-hop QA | A (verify given statement) | **Easy** | ✅ yes | shared |
| 🥈 P2 | **TruthfulQA** (MC1/MC2) | imitative falsehood / confident misconception | A | **Easy** | ✅ yes | shared |
| 🥉 P3 | **TriviaQA-generation** (closed-book, exact-match) | the model's *own* free-generation hallucination | **B (native generation)** | **Medium–Hard** | ✅ yes (extraction) | **per-model** |
| P4 | **FEVER** (claim + gold evidence → SUPPORTED/REFUTED) | evidence-grounded fact verification | A | Easy–Medium | ✅ yes | shared |
| P5 | **ANLI R2 / R3** | difficulty gradient on the *same* task (robustness, not breadth) | A | **Trivial** | ✅ yes | shared |
| ⏸️ defer | FActScore | atomic-fact generation factuality | (doesn't fit single-token framing) | Hard | — | — |

**Why this set:** it satisfies every stated constraint — ≥1 factual-hallucination (TruthfulQA, HaluEval-QA), ≥1 genuinely generation-based (TriviaQA-gen, P3), and broad task-type diversity (NLI, QA-verify, summarization, dialogue, fact-verification, native generation) — while keeping **P1, P2, P4, P5 fully byte-comparable to the seal** (no edits to the frozen `t0-morphology-furnace` core). P3 is the one that materially upgrades the *scientific* claim from "judge a given answer" to "catch your own hallucination," at the cost of per-model label construction.

**The single most important strategic point:** P1/P2/P4/P5 buy **breadth cheaply**; **P3 buys depth expensively.** For a top venue, you want both — but if effort is constrained, P1 + P2 + P3 is the minimal set that is simultaneously broad *and* answers the "is this real hallucination detection?" reviewer objection.

---

## 1. How the pipeline actually works (and why most benchmarks are drop-ins)

This section is the load-bearing finding. Everything downstream follows from it.

### 1.1 The extraction path is benchmark-agnostic

The confluence readout arm calls the sealed dependency directly:

```
collect_readout_matrix_fresh(model, benchmark, data_path, …)        # confluence_calibrator.py:89
  └─ comprehensive_run.trace_pair_features(model, benchmark, data_path, …)   # :99
```

Inside `trace_pair_features` (`t0-morphology-furnace/.../comprehensive_run.py:273`):

- 📥 It reads the data with `_load_calibration_jsonl(data_path)` → `(prompts, labels, hash)`. That loader (`pri_calibrator.py:516`) accepts **any** `{"prompt": str, "label": 0|1}` JSONL and *raises* on a label not in `{0,1}`. No task field, no schema beyond prompt+label.
- 🏷️ The `benchmark` string is used **only for print/inventory** (`:321`). There is **no `if benchmark == …` branch** anywhere in the feature computation.
- 🎯 It wraps each prompt with `io_plugins.get_prompt_strategy(model_id)` — a **model-specific** chat-template, *not* benchmark-specific (`:299`).
- ⏱️ It reads all four signal families at the **commit instant `gen_step=1`** (the first generated token) and emits per-sample rows.

The ACE arm is identical in spirit: `collect_ace_matrix` (`confluence_calibrator.py:330`) → `_load_calibration_jsonl` → same generic prompt/label parse.

> ⚠️ One footgun to know about: `comprehensive_run.discover_benchmarks()` / `_benchmark_name()` (`:133–150`) *do* hardcode filename prefixes (`anli_r1/r2/r3`, `triviaqa_paired`) and glob the **sealed** data dir. **But the confluence path never calls them** — it passes an explicit `data_path` straight into `trace_pair_features`. So that hardcoding is irrelevant to us. (It is, however, a useful tell: the original authors already pencilled in `anli_r2`/`anli_r3` as expected drop-ins → see P5.)

**Consequence:** to add a benchmark, you supply (a) a JSONL file in the existing format and (b) a name string. The frozen forward-pass code is untouched.

### 1.2 The format contract (what a new benchmark file must satisfy)

Each line: `{"prompt": "<text ending in a judgment cue>", "label": 0|1, "meta": {…}}`, where:

- 🟢 `label = 0` → supported / YES / entailment / correct.
- 🔴 `label = 1` → **the hallucination analog** (contradiction / wrong / unsupported / false). This is the positive class the detector is scored against.
- ⚖️ Balanced ≈ 0.50 (the gate enforces `|mean−0.5| ≤ 0.10`, and exactly 0.50 for paired sets).
- 🧩 `meta` is optional but recommended (carry an example id for disjointness/audit, mirroring TriviaQA's `question_id`).

The prompt ends in a cue the model commits to in one token. ANLI ends in `Answer:` and the model commits YES/NO; TriviaQA-paired ends in `Answer:` over a *given* proposed answer. Any new benchmark must produce a comparable single-token commit.

### 1.3 The honest selector and the descriptive analyses

- 🧮 `_nested_bootstrap_oob_auroc` runs on **one (model, task) score matrix at a time** → adding benchmarks just adds matrices. The selector itself needs **no change** (constraint satisfied).
- 📊 `analyze_universality.py`: **E1 LOMO** is `lomo(cells, task)` per task — runs per new task automatically. **E3 label-efficiency** is per-(model,task) — automatic. **E2 transfer** hardcodes `if len(tasks) != 2: skip` (`:138`) → **must be generalized to N tasks** (all ordered pairs / a transfer matrix). This is a ~20-line edit in *our* repo, not the sealed core.

### 1.4 Two framings — and why "generation-based" is the subtle one

| | **Framing A — verify a given statement** | **Framing B — native generation** |
|---|---|---|
| What's in the prompt | the candidate answer/claim (model judges it) | only the question (model produces the answer) |
| Commit token | the YES/NO judgment | the **first token of the model's own answer** |
| Label source | ground-truth correctness of the *given* statement (shared across models) | correctness of the *model's generated* answer (**per-model**) |
| Examples today | ANLI, TriviaQA-paired | — none yet — |
| Drop-in candidates | HaluEval, TruthfulQA-MC, FEVER, ANLI-R2/3 | TriviaQA-gen, NQ-gen, TruthfulQA-gen |
| Effort | low | medium–high (offline generate + label, per model) |

The paper currently has **only Framing A**. A reviewer's sharpest objection will be: *"You detect a property of a supplied statement, not the model's own hallucination."* Framing B is the answer to that, which is why P3 is worth the extra effort despite being the hardest integration.

---

## 2. What "byte-comparable extension" requires (the integration surface)

The seal's value is that the executed code is byte-identical to the registration (tag `prereg-seal-20260612`). The post-seal gemma extension (`PRE_REGISTRATION_EXT.md`, `run_ext.py`) is the **template** for doing this honestly. Mirror it exactly:

1. ✅ **Do not touch `t0-morphology-furnace`.** New benchmarks ride the *same* `run_cell` → `module_hashes` match → Phase-1-style byte-comparable. (This is precisely why FActScore is deferred: it would force a new compute path.)
2. ✅ **Write to a new profiles dir** (e.g. `stage_b/profiles_bench/<task>/…`), never `stage_b/profiles/`. The sealed 20 deployments stay frozen; the headline "Ten Language Models / 18-of-20" is not re-opened.
3. ✅ **New pre-registration doc** with **new bars**. The `19/20` and `17/20` bars are hardcoded for `n_planned==20` (`run_seal.py:233`); they do **not** transfer. Follow the EXT precedent: *"no X/N bar applies — each new (model, benchmark) cell is individually deployable-or-not,"* plus a **per-task LOMO floor probe** (the real universality test) for each new benchmark.
4. ✅ **Freeze predictions before the metric** (the EXT doc states per-cell LEAN-YES/NO confidences in advance). Same discipline here.
5. ⚙️ **Edits allowed (all in `commit-confluence`, none sealed):** generalize `analyze_universality.py` E2 to N tasks; add a generic-task path to `check_fresh_data.py`; one data-builder per benchmark (clone `generate_fresh_data.py`'s `build_*`).

**Net:** P1/P2/P4/P5 are *additive data + a thin harness*, fully inside the byte-comparable envelope. P3 adds an *offline label-builder* but the extraction it feeds remains byte-comparable.

---

## 3. Per-candidate deep dives

### 🥇 P1 — HaluEval (QA + Summarization + Dialogue)

- **What it is:** a purpose-built hallucination benchmark. Each record is a context (question / document / dialogue history) plus a **right** answer and a **hallucinated** answer. Subsets: QA (≈10k, built on HotpotQA → multi-hop), Summarization (≈10k, on CNN/DailyMail), Dialogue (≈10k, on OpenDialKG), General (≈5k).
- **New failure mode(s):** this is the big win. *Summarization* tests **intrinsic / source-faithfulness** hallucination (the model contradicts a *given* document) — the RAG-style failure, absent from ANLI/TriviaQA. *Dialogue* tests **knowledge-grounded conversational** faithfulness. *QA* tests **multi-hop** factuality. Three distinct modes from one source.
- **Format mapping (Framing A, native):** the right/hallucinated pairing maps **directly** onto the TriviaQA-paired builder. Prompt = `Instruction… Context/Question … Proposed answer: {answer} … Is it correct? YES/NO` ending in `Answer:`; `label 0 = right`, `1 = hallucinated`. Pairing gives exact 0.50 balance for free.
- **Data / license / locality:** HF `pminervini/HaluEval` (also original `RUCAIBox/HaluEval`); MIT in the source repo. Small, downloads locally. *(Verify license + exact HF path before camera-ready.)*
- **Strengthens which claim:** directly upgrades the headline word **"hallucination"** — these are labeled *hallucinations*, not an NLI/QA proxy. Adds 3 task columns × 10 models → the LOMO floor probe gets 3 new, *heterogeneous* tasks to generalize across; if the fusion floor holds on summarization/dialogue too, "universal above-chance floor" gets dramatically stronger. If it *fails* on one, that's an honest new orphan class (equally publishable).
- **Integration:** **Easy.** One builder, three output files, three benchmark names.
- **Gotchas:** ⚠️ the hallucinated answers were *generated by ChatGPT*. Under Framing A this is fine (you're detecting a property of the supplied text), but note it: a skeptic could argue the detector partly keys on "LLM-generated-text distribution." Mitigate by reporting it openly and leaning on P3 (where the hallucination is the *subject* model's own). ⚠️ Summarization prompts are long — confirm they fit each model's context and still yield a clean `gen_step=1` (the `no_gen_step1`/length drops in `trace_pair_features` would flag this; a strict run requires zero drops, so pre-filter by length).

### 🥈 P2 — TruthfulQA (MC1 / MC2)

- **What it is:** 817 questions engineered so the *popular* answer is *false* (imitative falsehoods, misconceptions). MC1 = one correct vs several plausible-false; MC2 = a set of true/false references.
- **New failure mode:** **imitative falsehood** — the model is drawn to a confidently-wrong answer it "learned" from the web. This is orthogonal to TriviaQA (recall) and ANLI (adversarial entailment): here the model often *isn't uncertain*, so it's a stress test for the **confidence-is-not-the-backstop** claim. Geometry that survives here, where surprise is least informative, is a strong result.
- **Format mapping (Framing A):** expand each question into `(question, candidate-answer)` rows → `label 0 = true, 1 = false`. Sample to balance 0.50. Iconic, tiny, trivial to build.
- **Data / license / locality:** HF `truthful_qa` (`multiple_choice`, `generation` configs), Apache-2.0, ~817 Q. Local, instant. *(Verify.)*
- **Strengthens which claim:** sharpens **"confidence rescues nothing."** TruthfulQA is the canonical place confidence fails; if the geometric panel still clears the floor here, that's the paper's confidence-independence thesis at its strongest. Also the single most *recognizable* factuality benchmark to reviewers — its absence is conspicuous, its presence is expected.
- **Integration:** **Easy** (MC). The **generation** config is Framing B and needs a truthfulness judge → treat as an optional add-on to P3, not the main path.
- **Gotchas:** ⚠️ only 817 questions → expanded paired rows are correlated (many share a stem); keep `n≈200` per the registered design and don't oversample one stem. ⚠️ known to be in pretraining corpora — note it (affects base rate, not detector validity; same caveat as TriviaQA).

### 🥉 P3 — TriviaQA-generation (closed-book, exact-match) — the generation-based one

- **What it is:** the **native** setting. Prompt = `Question: X\nAnswer:`; the model **generates** its own answer greedily (a handful of tokens); the label = whether that generation alias-matches the reference (`0`) or not (`1`, a hallucination). Reuses the TriviaQA data already vendored.
- **New failure mode:** the model's **own** free-generation hallucination, detected at the **first committed answer token** — i.e., the actual deployment scenario the paper motivates ("flag unsupported answers… *before* the answer is shown"). Everything currently in the paper is *judgment of a supplied answer*; this is the first cell that measures the thing the abstract promises.
- **Format mapping (Framing B):** **offline, per model:** generate with `max_new_tokens≈16–32`, alias-match against the reference set (reuse the alias logic already in `generate_fresh_data.py::_all_aliases`), emit a per-model file `{"prompt": "Question:…\nAnswer:", "label": <match?0:1>, "meta": {...}}`. Then the **unchanged** sealed pipeline reads the commit features at `gen_step=1` (`max_new_tokens=1` for extraction is fine — the label was decided offline). **Extraction stays byte-comparable.**
- **Data / license / locality:** already local (`trivia_qa`, `rc.wikipedia`). No new download.
- **Strengthens which claim:** this is the **headline-credibility** upgrade. It converts "we detect the wrong-answer class" into "we detect the model about to hallucinate its own answer." For a NeurIPS bar this is arguably worth more than three Framing-A drop-ins combined.
- **Integration:** **Medium–Hard**, because of three honest complications:
  1. 🔁 **Per-model labels.** Each model generates differently, so each model gets its *own* label vector over the shared questions. That's 10 data files, not 1.
  2. 🧭 **LOMO semantics shift.** The E1 floor probe pools 9 models to predict the 10th. With per-model labels the *examples* are shared but the *labels* differ per model — the probe still tests "does a fixed **signal** generalize," which is valid, but the write-up must state that the *labels* are model-specific (it's a slightly different, arguably *stronger*, generalization test). Pre-register this interpretation.
  3. ⚖️ **Balance + base rate.** Strong models hallucinate less → label imbalance per model. Either (a) subsample to 0.50 per model (changes which questions each model sees → breaks shared-example LOMO), or (b) keep shared questions and let balance float within the gate's ±0.10, reporting per-model base rates. **Recommend (b)** to preserve LOMO; flag models whose base rate is too skewed for a stable AUROC.
- **Gotchas:** ⚠️ exact-match/alias labeling is noisy (formatting, partial matches) — reuse and *document* the alias normalizer; consider a small manual audit of N labels. ⚠️ greedy vs. sampled generation must be fixed and registered (greedy, to keep the commit token deterministic w.r.t. the label). ⚠️ this is the one place the "same fresh data, same seed" mantra needs care: the *questions* can be the registered fresh set, but the *labels* are produced by a new deterministic generate step whose seed/decoding must be pinned and hashed like everything else.

### P4 — FEVER (claim + gold evidence → SUPPORTED / REFUTED)

- **What it is:** ~185k natural claims labeled against retrieved Wikipedia evidence: SUPPORTED / REFUTED / NOT ENOUGH INFO. Drop NEI → binary, exactly ANLI's entail/contradict shape.
- **New failure mode:** **evidence-grounded fact verification** with *real* Wikipedia evidence — distinct from ANLI (crowd-adversarial, synthetic premises) and from TriviaQA (closed-book recall). It's the "is this claim supported by *this* source" mode at scale.
- **Format mapping (Framing A, NLI-shaped):** prompt = `Evidence: {gold sentences}\nClaim: {claim}\nIs the claim supported? Answer:` → `label 0 = SUPPORTED, 1 = REFUTED`. Maps onto the ANLI builder with a different template.
- **Data / license / locality:** HF `fever` + `copenlu/fever_gold_evidence` (claims pre-joined with gold evidence sentences, which removes the retrieval step). FEVER data CC BY-SA 3.0 (Wikipedia-derived). Local. *(Verify license + that the gold-evidence variant is acceptable.)*
- **Strengthens which claim:** a *third* judgment type for the LOMO floor to generalize across, and a recognizable benchmark. Tests whether the geometry that works on adversarial NLI (ANLI) also works on natural, evidence-grounded verification — a clean robustness story.
- **Integration:** **Easy–Medium** — the only friction is joining claims with gold evidence (solved by the `fever_gold_evidence` variant). 
- **Gotchas:** ⚠️ evidence can be multi-sentence and long → same length/`gen_step=1` caveat as HaluEval-Summarization. ⚠️ symmetric/de-biased FEVER variants exist; pick one and register it (claim-only artifacts are a known FEVER pitfall — but they affect a *classifier's* shortcut, not a commit-moment *probe*, so lower risk here; still note it).

### P5 — ANLI R2 / R3 (difficulty gradient)

- **What it is:** the harder adversarial rounds of the dataset already in use. The sealed code *already names* `anli_r2`/`anli_r3` (`comprehensive_run.py:137–140`).
- **New failure mode:** none new — *same task, harder*. This is a **robustness/monotonicity** probe, not a breadth probe.
- **Format mapping:** literally the existing ANLI builder with `split="dev_r2"`/`"dev_r3"`. **Trivial.**
- **Data / license / locality:** `facebook/anli`, already used. Local.
- **Strengthens which claim:** cheap insurance. If geometric coverage *degrades* monotonically R1→R2→R3, that's a clean "harder adversarial NLI erodes the floor" finding; if it's flat, that's robustness. Either way near-zero cost. **But it does not broaden failure-mode coverage** — don't let it substitute for P1/P3.
- **Integration:** **Trivial.**
- **Gotchas:** ⚠️ R2/R3 dev sets are ~1000 each; with sealed-exclusion already consuming R1, confirm enough disjoint rows at `n=200` (the generator already handles exclusion + raises if short).

### ⏸️ Deferred — FActScore (and why)

- **What it is:** generate a biography, decompose into atomic facts, verify each against Wikipedia → factual precision.
- **Why defer:** it does **not** fit the single-commit-token framing. FActScore scores a *whole generation's* atomic-fact precision; there's no one "commit moment" whose geometry maps to a binary label without (a) free generation, (b) atomic decomposition, (c) per-fact KB verification — i.e., a *new compute path*, which breaks byte-comparability and pulls in heavy dependencies (a decomposer + a retriever + a judge). The *spirit* of FActScore is better captured cheaply by **P3** (the model's own generation, exact-match-labeled). Revisit only if a "long-form generation" failure mode is specifically demanded by reviewers.

---

## 4. Recommended priority order & phased plan

A phased rollout that front-loads cheap breadth, then adds the depth cell, then optional robustness:

- **Phase 1 — cheap breadth, fully byte-comparable (do first).**
  - 🟦 P1 HaluEval-QA, P1 HaluEval-Summarization, P1 HaluEval-Dialogue, P2 TruthfulQA-MC, P4 FEVER.
  - One builder each (clone `build_triviaqa`/`build_anli`), generic gate path, new `profiles_bench/` dir, new pre-reg doc with per-cell frozen predictions + per-task LOMO bars.
  - Output: 5 new task columns × 10 models = 50 new deployments, all Framing A, all byte-comparable. This *alone* takes the paper from 2 → 7 benchmarks.
- **Phase 2 — the depth cell (do second; it's the reviewer-objection killer).**
  - 🟥 P3 TriviaQA-generation. Offline per-model generate+label builder; register the decoding/seed/labeling and the model-specific-LOMO interpretation in advance. Extraction stays byte-comparable.
- **Phase 3 — optional robustness (cheap, do if time).**
  - 🟩 P5 ANLI R2/R3. Difficulty-gradient rows; trivial.
- **Camera-ready hygiene (all phases):** verify every license + HF path live; pin dataset revisions; hash the new data files through the existing provenance machinery; pre-register before drawing any matrix.

**If you can only do three:** P1 (HaluEval, as the 3-mode workhorse) + P2 (TruthfulQA) + P3 (TriviaQA-gen). That trio is broad *and* deep and answers every stated constraint.

---

## 5. Cross-cutting blockers & gotchas (read before committing)

- 🚧 **Re-registration is mandatory, not optional.** The `19/20` / `17/20` bars are n=20-specific. New benchmarks ⇒ a new pre-registration with new bars, following the `PRE_REGISTRATION_EXT.md` "each cell deployable-or-not + per-task LOMO floor" template. Do **not** fold new deployments into the sealed 20.
- 🚧 **`analyze_universality.py` E2 needs a one-time generalization** from exactly-2-tasks to N-tasks (all ordered pairs). E1/E3 already scale. ~20 lines, in our repo.
- 🚧 **`check_fresh_data.py` is `{anli,triviaqa}`-coded.** New benchmarks have **no sealed predecessor**, so the disjoint-from-sealed check is N/A — but you still want schema/balance/intra-dup/`meta.id` checks. Add a generic `--task other` path. (A brand-new benchmark cannot be contaminated by the 20260526 seal *by construction*, which is a simplification, not a gap.)
- 🚧 **Length / `gen_step=1` drops.** Long-context benchmarks (HaluEval-Summarization, FEVER multi-sentence evidence) risk truncation or a missing first-gen-step. A **strict** run requires `max_dropped=0` (`merge_matrices`), so pre-filter examples by token length per model, or the cell aborts. Budget for this.
- 🚧 **Per-model labels (P3 only) change LOMO's meaning** (shared examples, model-specific labels). Valid, arguably stronger, but must be stated and pre-registered. Don't let it silently mix with shared-label benchmarks in one transfer table.
- 🚧 **Label balance.** Framing A (paired) is exactly 0.50 for free. Framing B floats with model skill — keep within the gate's ±0.10 and report base rates; drop a model from a cell if its base rate makes AUROC unstable (and say so — an honest "not enough positives to certify" is in the paper's voice).
- 🧪 **Pretraining contamination** (TruthfulQA, TriviaQA, FEVER are in many corpora). This affects the *base rate* of right/wrong, not the *validity* of a commit-moment detector on a frozen model. One sentence in Limitations defuses it.
- 🏷️ **Provenance discipline.** Every new data file must flow through the existing hashing (`data_file_sha256`, `module_hashes`, `model_snapshot_sha`). For P3, also hash the generation/labeling step's config + seed.
- 📛 **License facts in this doc are from memory — verify before camera-ready.** Stated: HaluEval (MIT), TruthfulQA (Apache-2.0), FEVER (CC BY-SA 3.0), TriviaQA/ANLI (already in use). Confirm exact HF dataset IDs, configs, and redistribution terms; pin revisions.

---

## 6. How the expansion maps onto the paper's specific claims

| Paper claim (cc-draft.tex) | What the expansion does to it |
|---|---|
| "No universal champion" (12 winners / 18) | More tasks → more winners → claim *broadens*; risk is low (it's a negative claim, hard to break). |
| "Universal above-chance **floor**" (LOMO fusion) | **The main test.** Re-running the LOMO floor probe per new task is the real universality experiment. Holding on summarization/dialogue/fact-verification/native-gen = a *much* stronger floor. Failing on one = a new, publishable orphan class. Either outcome strengthens the paper's honesty. |
| "Confidence is not the backstop" | TruthfulQA (P2) is the strongest possible stage for this — confidence is least informative there. |
| "Task transfer is partial" (median 0.67) | Goes from a single A↔B number to an N×N transfer matrix — a far richer, more convincing transfer story (needs the E2 generalization). |
| Abstract: "flag unsupported answers… before the answer is shown" | **Only P3 actually tests this.** It's the cell that makes the abstract literally true rather than analogically true. |
| "Ten Language Models" headline | Unchanged — keep 10 models, add benchmark columns as a labeled post-seal extension. The sealed 18/20 is never re-opened. |

---

## 7. Open decisions for you

1. ❓ **Effort envelope:** all of P1–P5, or the minimal broad-and-deep trio (P1+P2+P3)?
2. ❓ **HaluEval scope:** all three subsets (max breadth, 3 new modes) or just QA+Summarization (faithfulness focus)?
3. ❓ **P3 balance policy:** shared questions with floating per-model base rate (preserves LOMO — recommended) vs. per-model 0.50 subsampling (cleaner AUROC, breaks shared-example LOMO)?
4. ❓ **FEVER variant:** standard vs. symmetric/de-biased, and gold-evidence vs. retrieved-evidence?
5. ❓ **Generation judge:** skip TruthfulQA-generation (judge dependency) and let P3 carry the generation-based requirement? (Recommended: yes.)
6. ❓ **Want me to verify licenses/HF paths/availability live** before you commit to the set? (Out of scope for this pass; one web sweep would lock down §3's "verify" items.)

---

*No code or data was produced for this proposal. Next concrete step, on your go: draft the new `PRE_REGISTRATION_BENCH.md` (frozen predictions + per-task LOMO bars) and the Phase-1 builders, mirroring `generate_fresh_data.py` + `run_ext.py` so the additions stay byte-comparable to `prereg-seal-20260612`.*
