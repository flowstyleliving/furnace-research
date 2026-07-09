# Benchmark Expansion Proposal — v2 (post-adversarial-review)

**For:** `cc-draft.tex` ("No Universal Detector, but a Universal Floor") — expansion from 2 → N benchmarks for a TMLR → NeurIPS submission.
**Supersedes:** `cc-benchmark-proposal.md` (v1).
**Driven by:** `cc-benchmark-review.md` (Codex; verdict **FIX**, 10 must-fix items).
**Status:** proposal only — no code written, no data drawn, nothing frozen. This revision is written to go *back* to Codex for a second adversarial pass; it is deliberately conservative and flags every residual UNKNOWN rather than asserting past the evidence.
**Verification done for this revision:** code re-read against the review's line citations (commit-confluence + t0-morphology-furnace); dataset licenses/specs re-checked live 2026-06-20. The corrected citations are in the **Code-citation ledger** at the end so the next reviewer can re-verify fast.

---

## 0. How v2 resolves each must-fix

This is the audit table for the re-review. Every row maps a review must-fix to where it is resolved and the one-line resolution. Detail follows in the numbered sections.

| # | Review must-fix | Resolution (one line) | Where |
|---|---|---|---|
| 1️⃣ | Byte-comparability over-claimed | Split the envelope: **T0 extraction** can stay byte-identical; **launcher + gate + builders + transfer + pre-reg** all change and are recorded in `module_hashes`, so new cells are a *separately-hashed* extension, never inside the seal's hash set. | §1.1, §8 |
| 2️⃣ | Commit-locus wrong | Adopt the canonical two-locus mapping: **ACE = t=0/prefix-last; PRI/RPV/Confidence = gen_step=1**; fusion averages both. P3 *predicts* eventual correctness from the gen_step=1 state. | §1.2 |
| 3️⃣ | "JSONL is enough" incomplete | Replace with a **7-clause prompt/extraction contract** + a mandatory per-(model,task) limit-8 smoke gate before any strict cell. | §1.3 |
| 4️⃣ | Pre-reg bars too weak | Declare **confirmatory vs exploratory**, fix a **primary endpoint**, **per-task deployability bars**, a **per-task LOMO floor bar**, and an explicit **falsification rule** (how many task failures narrow vs falsify the claim). | §6 |
| 5️⃣ | P3 over-claimed | Rename to **"predicting generated short-answer correctness"**; build a real normalizer; **manual label-noise audit** + **first-token-commit audit**; pin the offline generator to the extraction's prompt/snapshot/decoding. | §4.4 |
| 6️⃣ | Group correlation ignored | **Group-aware sampling** (≤2 rows/stem) + a **cluster (stem-level) bootstrap** sensitivity check; report **effective n**, never claim n=200 independent. | §5 |
| 7️⃣ | FEVER NEI undecided | Primary FEVER cell = **binary SUPPORTS vs REFUTES on gold evidence** (scoped to "contradicted-by-evidence", *not* general unsupportedness); the NEI/insufficient-evidence mode is handled as a *separate, exploratory* collapsed cell with a non-gold-evidence caveat, and the paper language is hedged accordingly. | §4.3 |
| 8️⃣ | Licenses unverified | Live-verified table (HaluEval **license mismatch confirmed**, FEVER gold-evidence variant **dual GPL caveat**); verification promoted to a **hard pre-freeze gate** with pinned HF revisions. | §2 |
| 9️⃣ | SimpleQA/RAGTruth not compared | Explicit head-to-head: **SimpleQA** is the better-designed short-form generation benchmark but a **poor fit for this small-model cohort** (extreme base rate, 3-class judge); **RAGTruth** is the genuine source-faithfulness corpus but **does not fit the single-token protocol** (long-form/span-level, excluded like FActScore). Both inclusions/exclusions justified, not assumed. | §3 |
| 🔟 | Paper could rewrite the seal | New results land as a **labeled post-seal extension** only; the sealed 18/20 and the "Ten Models × two tasks" headline are never re-opened; specific draft-language hedges listed (incl. the glossary "step 0" fix and the "unsupported answers" hedge). | §7 |

---

## 1. Corrected foundation

### 1.1 Byte-comparability, stated honestly (must-fix #1)

The v1 sentence *"the pipeline is benchmark-agnostic at the extraction layer, so most benchmarks are drop-ins"* was true for the **feature function** and false for the **registered run path**. The honest decomposition:

**✅ What can stay byte-identical — the T0 forward pass.**
- `pri_calibrator._load_calibration_jsonl` reads only `row["prompt"]` + `int(row["label"])`, rejects labels ∉ {0,1}, ignores all metadata (`pri_calibrator.py:~516`).
- `comprehensive_run.trace_pair_features` is prompt/label-driven; the `benchmark` string is **print-only** (`comprehensive_run.py:321`), no `if benchmark == …` branch.
- `discover_benchmarks()/_benchmark_name()` hardcode `anli_r1/r2/r3`, `triviaqa_paired` (`comprehensive_run.py:133-150`) but the confluence path never calls them — it passes an explicit `data_path` (`confluence_calibrator.py:89-101`).
- ⇒ The **T0-module subset** of `module_hashes()` (pri_calibrator, comprehensive_run, pri_runtime, pri_v2_io_plugins, pri_v2_mlx_pipeline, model_adapters, test_shadow_ambiguity, diagnose_inter_head_disagreement) *can* match the seal exactly, since none of them need editing for a new prompt/label file.

**❌ What is NOT benchmark-agnostic — everything in `commit-confluence`.**
- 🚀 **Launcher.** `run_seal.py` accepts only `--anli`/`--triviaqa` (`run_seal.py:122-123`), builds `tasks` with exactly `anli_r1` + `triviaqa_paired` (`:134-136`), maps gates with `gate_task = {"anli_r1":"anli","triviaqa_paired":"triviaqa"}` (`:167`), knows sealed refs for only those two (`:40-44`), and hardcodes the `19/20`/`17/20` bars when `n_planned==20` (`:233-234`). New benchmarks require launcher edits before they are runnable as registered cells.
- 🚪 **Gate.** `check_fresh_data.py` accepts only `--task {anli,triviaqa}` (`:72`), has TriviaQA-specific exact-0.50 + `question_id` logic (`:105-156`), and *requires* a sealed reference file (`:115-124`).
- 🧱 **Builders.** One per benchmark (clone of `build_anli`/`build_triviaqa`, `generate_fresh_data.py:96-287`).
- 🔀 **Transfer analysis.** `analyze_universality.transfer()` hard-skips unless exactly 2 tasks (`analyze_universality.py:137-138`).
- 📋 **Pre-registration.** New bars (the `19/20` bars are n=20-specific; see §6).

**⚠️ The hash subtlety the review caught.** `module_hashes()` records **`confluence_calibrator.py` itself (`:292`) and `fusion_signs.json` (`:294`)** alongside the T0 modules. So *any* edit to `confluence_calibrator.py` to support a new task changes the recorded hash — even with T0 untouched. The launcher/gate/builders/transfer edits live in `run_seal.py`/`check_fresh_data.py`/`generate_fresh_data.py`/`analyze_universality.py`, which are *not* in `module_hashes()` (they are harness, not compute), so those edits do **not** change the recorded hash. But to keep new tasks working we may still touch `confluence_calibrator.py` (e.g. a generic gate dispatch), and *that* would.

**Honest phrasing for the paper and the pre-reg:**
> The T0 extraction code is byte-identical to the seal (verified by the T0-module subset of `module_hashes`). The commit-confluence *harness* is not — by construction, a benchmark extension edits the launcher, gate, builders, and analysis. New cells are therefore a **separately-hashed, separately-registered post-seal extension**, never folded into the seal's module-hash set.

**Pass/fail rule for hash drift across the 50+ new cells (the v1 UNKNOWN, now specified).** A new cell is labeled **byte-comparable** iff *all* of:
1. 🔒 its `module_hashes()` **T0 subset** equals the seal's recorded values (any T0 drift ⇒ not byte-comparable, reported separately — exactly the EXT Phase-2 discipline);
2. 🔒 `confluence_calibrator.py` + `fusion_signs.json` hashes equal a **new frozen extension-baseline** recorded at extension registration (so the extension is internally consistent even though it differs from the seal);
3. 🔒 `model_snapshot_sha(model)["resolved_revision"]` equals the seal's per-model value (`confluence_calibrator.py:298-322`; the EXT precedent already compares this on resume, `run_seal.py:99-101`);
4. 🔒 the runtime stack (`mlx-lm` version, Python, key deps) matches the seal venv — pinned and recorded, mirroring EXT Phase 1.

A cell missing any of (1)–(4) is reported with a **version-delta caveat** and **never pooled** with byte-comparable cells (this is precisely how EXT treats the gemma-4 Phase-2 cells).

### 1.2 Commit-locus, stated correctly (must-fix #2)

v1 said "all four signal families are read at the commit instant `gen_step=1`." That is **wrong**. Per the canonical `wiki/references/commit-locus.md` (verified against code):

| Locus | Position | Families | Code |
|---|---|---|---|
| **t=0** | prefix-last token (model has read the prompt, generated nothing) | **ACE** (bos_mass, v_norm_lastq_weighted, js, js_no_bos, js_kv_groups) | `confluence_calibrator.py:330-381`; `run_seal.py:5` ("t=0 attention morphology") |
| **gen_step=1** | first generated token (model has committed one token) | **PRI** (null_ratio), **RPV** (fisher_eff_rank, spectral_entropy, neg_shadow_logvol_r1), **Confidence** (surprise, p_max) | `confluence_calibrator.py:89-101` → `comprehensive_run.py:273-388` (line 324 prints "commit instant: gen_step=1") |

`fusion_rank_mean_geom` rank-averages one representative per geometric family across **both** loci — which is *why* it is the universal-floor candidate (cross-locus variance reduction). The mixed-locus design is also *why* there is no universal champion: t=0 and gen_step=1 capture different failure modes.

**Consequence for the expansion.** Any per-cell or per-task statement must say which columns are pre-token (ACE, t=0) and which are first-token (PRI/RPV/Confidence, gen_step=1). A signal that works at one locus need not work at the other. This matters most for P3 (§4.4): P3 reads the **gen_step=1** state to *predict* eventual short-answer correctness; it does **not** "detect hallucination at token 1" unless an audit shows token-1 *is* the answer-commit token for that model's format (see commit-locus.md, "P3 can detect hallucination at token 1" → corrected).

### 1.3 The full prompt/extraction contract (must-fix #3)

A new benchmark file is admissible only if it satisfies **all seven** clauses below — `{"prompt","label"}` JSONL is necessary, not sufficient.

1. 🎯 **One-token commit cue.** The prompt must end so the model commits its judgment/answer in a single token (extraction runs `max_new_tokens=1`, `run_seal.py:54`). ANLI/TriviaQA end in `Answer:` → YES/NO. Every new template must produce a comparable single-token commit.
2. 🧩 **Model-specific wrapping is mandatory and varies.** Extraction wraps each prompt with `io_plugins.get_prompt_strategy(model_id)` (`comprehensive_run.py:299,327`; ACE uses `state.prompt_strategy`, `confluence_calibrator.py:359,366`). Default is `raw_passthrough`, but `Mistral-Nemo-Instruct-2407` (in cohort) and others use `apply_chat_template` (`pri_v2_io_plugins.py:239-247`) — *"without this wrap they produce empty output or chain-of-thought that never reaches a YES/NO"* (`:222-224`). A template that behaves under raw prompts can break under a chat template and vice-versa.
3. 📏 **Length limits.** Long contexts (HaluEval-Summarization documents, FEVER multi-sentence evidence) risk truncation or a missing first gen-step. Pre-filter every example by **per-model token length** so it fits each model's practical context.
4. 🚫 **No-drop policy.** A strict registered cell sets `max_dropped=0` (`run_seal.py:58`, `merge_matrices`, `confluence_calibrator.py:384+`); any dropped row aborts the cell. The `drops` dict in `trace_pair_features` (`comprehensive_run.py:302-316`) enumerates the failure modes that must all be zero: `trace_failed`, `no_gen_step1`, `missing_readout`, and the `nonfinite_*` rows. v1 mentioned length drops but not these output-format failures.
5. 🔬 **First-token sanity check.** The committed token must be a meaningful judgment/answer token, not whitespace/newline/an article/a refusal preamble. Audited per model in the smoke gate; for P3, this is a *registered* audit (§4.4).
6. 🧪 **Per-(model,task) smoke gate — required before any strict cell.** Mirror the EXT precedent's limit-8 `is_preview` smoke (`PRE_REGISTRATION_EXT.md:5-8`): prove the model loads, **ACE 8/8 + readout 8/8 usable**, the produced matrix `panel` is **byte-identical to the seal's panel** (`MISSING=[]`, `EXTRA=[]`), shuffled-label controls pass, and the **first token is meaningful** under the actual prompt strategy. A smoke produces no registered metric (cannot be `--resume`d into a cell per M3-fix-2, `run_seal.py:102-111`).
7. 🔗 **Common intersection set.** If any model cannot score some (e.g. over-length) examples, define a **common example set scored by all cohort models** so cells stay comparable — or drop that model from that task and report it. Never let different models silently score different example subsets within a task.

The new generic gate (§8) enforces clauses 1–5 statically where possible (schema, balance, intra-dup, length, one-token-cue heuristic) and the smoke (clause 6) enforces the behavioral ones. **Contamination note (correcting v1):** "not in the sealed file" is *not* the only freshness condition — a brand-new benchmark can still overlap the seal through reused **source corpora** (TriviaQA/HotpotQA/CNN-DM/FEVER-Wikipedia), shared **stems**, or **template** reuse. The gate must check schema/balance/length/duplication intrinsically; cross-source contamination is bounded by *choosing source splits disjoint from the seal's* and is documented, not assumed away.

---

## 2. Verified dataset facts (must-fix #8)

Re-checked live **2026-06-20**. The v1 "from memory, verify later" footnote is replaced by this table plus a **hard pre-freeze gate**. ⚠️ The single most important correction: **the HaluEval license is genuinely ambiguous** (the review was right).

| Dataset | HF id (candidate) | License — VERIFIED | Size / structure notes | Status |
|---|---|---|---|---|
| HaluEval | `pminervini/HaluEval` (mirror) vs `RUCAIBox/HaluEval` (source) | ❗ **MISMATCH**: source GitHub = **MIT**; HF mirror = **apache-2.0** | QA 10k, dialogue 10k, summ 10k, general ~5k (HF shows 4.51k). **Field names differ per subset** (QA: question/right_answer/hallucinated_answer; summ: document/right_summary/hallucinated_summary; dialogue: dialogue_history/right_response/hallucinated_response). | **BLOCKED until license resolved** |
| TruthfulQA | `truthfulqa/truthful_qa` | ✅ **apache-2.0** | 817 Q; MC1/MC2/generation configs | OK to plan; pin revision |
| FEVER (raw) | `fever/fever` | ✅ **CC BY-SA 3.0** | v1.0 311k / v2.0 2,384 val / wiki_pages 5.4M. Evidence = **page-id + sentence-id refs, not joined text**; NEI present (v2.0) with `evidence_id=-1`. | Join required (see §4.3) |
| FEVER (gold-joined) | `copenlu/fever_gold_evidence` | ⚠️ **dual cc-by-sa-3.0 + GPL-3.0** | Pre-joins evidence *sentence text* (`[title, sent_num, sentence]`); includes NEI **but NEI evidence is non-gold** (retrieved, Malon 2018). ~228k/15.9k/16k. | **GPL tag must be cleared** before redistribution |
| SimpleQA | `basicv8vc/SimpleQA` | ✅ **MIT** | 4,326 Q, single short answer; **judge-graded** correct/incorrect/not-attempted (3-class). | See §3 (fit problem) |
| RAGTruth | `ParticleMedia/RAGTruth` (HF: `wandb/RAGTruth-processed`) | ❔ **unverified** | ~18k naturally-generated RAG responses; **span/word-level** annotations; tasks QA/data-to-text/summ. | See §3 (protocol-fit exclusion) |
| ANLI | `facebook/anli` | (already in use) | dev_r2/dev_r3 ≈ 1,000 each | OK |
| TriviaQA | `trivia_qa` `rc.wikipedia` | (already in use) | already vendored | OK |

**Hard pre-freeze gate (registered before any data file is built):**
- 🔐 **Resolve HaluEval licensing**: choose the artifact whose license is unambiguous for redistribution. Recommended: build from the **RUCAIBox source (MIT)** and cite it as the canonical license; do *not* write "license verified" against the apache-2.0 mirror without reconciling the discrepancy with the authors/repo.
- 🔐 **Clear the FEVER GPL question**: if `copenlu/fever_gold_evidence` is used, confirm the GPL-3.0 applies only to accompanying *code* and not the data, or build the gold join ourselves from `fever/fever` + `wiki_pages` (CC BY-SA 3.0 only).
- 🔐 **Pin exact HF revision SHAs** for every dataset in the manifest (datasets supports `revision=`); hash the downloaded artifact (`data_file_sha256`) through the existing provenance machinery (`run_cell` already stamps `data_file_sha256`, `run_seal.py:71`).
- 🔐 **Confirm local availability** (download + load on the run machine) during the smoke phase, before pre-registration freeze.
- 🔐 No dataset enters the confirmatory set until its row in this table reads ✅.

---

## 3. Candidate set, reconsidered against SimpleQA & RAGTruth (must-fix #9)

v1 implied HaluEval + TruthfulQA + FEVER were the obvious complete set. They are not. Here is the explicit comparison the review demanded, on the axis that actually binds — **fit to the single-commit-token protocol on a small 4-bit MLX cohort**.

| Benchmark | Failure mode | Framing | Single-token fit | Cohort base-rate risk | Verdict |
|---|---|---|---|---|---|
| 🟦 HaluEval (QA/Summ/Dialogue) | recognition of ChatGPT-written hallucinations; summ = source-faithfulness *proxy* | A (judge given text) | ✅ good (paired YES/NO) | low (paired ⇒ 0.50) | **Include** (with the ChatGPT-generated caveat, §4.1) |
| 🟦 TruthfulQA-MC | imitative falsehood / confident misconception | A | ✅ good | low if stem-capped | **Include** as breadth + the confidence-stress task (§4.2) — but it is *recognition*, not generation |
| 🟦 FEVER (SUPPORTS/REFUTES) | contradicted-by-gold-evidence | A (NLI-shaped) | ✅ good | needs class-balanced sampling | **Include**, scope to "contradicted", not "unsupported" (§4.3) |
| 🟥 P3 TriviaQA-generation | the model's **own** short-answer error | B (native gen) | ⚠️ conditional (first-token audit) | ⚠️ per-model skew | **Include** as the depth cell, **reframed** (§4.4) |
| 🟪 **SimpleQA** | short-form generation factuality (best-designed of its class) | B (native gen) | ⚠️ needs an **LLM grader**; **3-class** (correct/incorrect/**not-attempted**) breaks the binary contract | ❗ **severe** — designed hard; small 4-bit models will be near-floor ⇒ extreme imbalance ⇒ unstable AUROC | **Defer/justify-out for THIS cohort** (see below) |
| 🟫 **RAGTruth** | genuine source-faithfulness on **naturally-generated** RAG output | (long-form) | ❌ long-form, **span/word-level** labels — no single commit token | n/a | **Exclude on protocol fit** (like FActScore) |
| ⏸️ FActScore | long-form atomic-fact precision | (long-form) | ❌ new compute path | n/a | **Defer** (unchanged; *not* substituted by P3 — see below) |
| 🟩 ANLI R2/R3 | none new (same task, harder) | A | ✅ trivial | low | **Robustness only**, not counted toward breadth (§4.6) |

**SimpleQA — why it is the better benchmark but the wrong tool here.** SimpleQA (MIT, 4,326 fact-seeking Q, single indisputable answer) is purpose-built for short-form *generation* grading and is, in the abstract, a stronger Framing-B choice than TriviaQA-gen. Two hard reasons it does not fit *this* cohort *now*:
1. 🧮 **Base rate.** SimpleQA is engineered so even frontier models miss most questions; 4-bit 1.7B–8B MLX models will be far below 40% correct ⇒ the positive (correct) class is tiny ⇒ AUROC CIs are unstable and the gate's ±0.10 balance fails. This is the same "not enough positives to certify" honesty the seal already practices.
2. 🏷️ **3-class + judge.** SimpleQA's value is the **not-attempted** class (an abstention is *not* a hallucination). The binary commit-token contract cannot express it without dropping abstentions or mislabeling them — and grading requires an **LLM judge**, a dependency the seal avoids.

➡️ **Decision:** SimpleQA is *not dismissed*. It is the recommended **future** generation benchmark and the right target if the cohort gains larger models; for the current submission we **register a base-rate pilot** (report correct/incorrect/not-attempted rates only, no metric) and include SimpleQA **iff** ≥1 cohort model clears a usable positive rate. Otherwise it is excluded with this explicit, measured justification — not silence.

**RAGTruth — why it is excluded on protocol grounds.** RAGTruth (~18k naturally-generated RAG responses, span/word-level hallucination annotations across QA/data-to-text/summarization) is the *genuine* source-faithfulness corpus that HaluEval only approximates — HaluEval's hallucinations are **ChatGPT-generated and filtered**, RAGTruth's are real model outputs annotated by humans. But RAGTruth labels are **long-form and span-level**: there is no single commit token whose geometry maps to one binary label without free generation + span localization — the same wall that defers FActScore. ➡️ **Decision:** exclude on protocol fit, and **state plainly in the paper** that HaluEval-Summarization is a *convenience proxy* for source-faithfulness, with RAGTruth the superior but protocol-incompatible target — so reviewers see we know the difference. (License left unverified because the exclusion is on fit, not terms; re-verify if reconsidered.)

**FActScore is not subsumed by P3 (correcting v1).** v1 said P3 captures FActScore's spirit. Scientifically wrong: FActScore measures *long-form atomic-fact precision*; P3 measures *short-answer exact-match*. They are different constructs. FActScore stays deferred on its own merits (new compute path), not as "covered by P3."

**Revised recommended set.** Breadth (Framing A, byte-comparable T0): **HaluEval-QA/Summ/Dialogue, TruthfulQA-MC, FEVER-binary**. Depth (Framing B): **P3 TriviaQA-generation** (reframed). Robustness (optional): **ANLI R2/R3**. Generation-future (pilot-gated): **SimpleQA**. Excluded with justification: **RAGTruth, FActScore**.
**Minimal broad-and-deep trio:** HaluEval + FEVER-binary + P3. (v1's "TruthfulQA + TriviaQA-gen" trio is *not* obviously optimal; FEVER adds the evidence-grounded mode TruthfulQA-MC lacks, and is recognizable.)

---

## 4. Per-candidate specifics (only the deltas that matter for re-review)

### 4.1 HaluEval — three modes, two caveats
- **Format (Framing A):** emit both the `right_*` and `hallucinated_*` output per source item ⇒ exact 0.50 balance, but the two rows **share a context (stem)** → see §5 group-aware sampling. Prompt ends in a one-token `YES/NO` cue.
- ⚠️ **Per-subset field names differ** (QA vs summarization vs dialogue) — the builder must branch on subset, verified live (§2). This is real integration work, not a clone-and-go.
- ⚠️ **"Source-faithfulness" is a proxy, not the clean RAG thing.** HaluEval-Summarization hallucinations are **ChatGPT-generated**, so a detector may key on "LLM-generated-text distribution" rather than the subject model's own failure. Report openly; lean on P3 for the model's-own-hallucination claim; name RAGTruth as the superior target we can't fit (§3).

### 4.2 TruthfulQA — recognition, stem-correlated
- **Format:** expand each question into `(question, candidate)` rows, `label 0=true / 1=false`, then **class-balanced + stem-capped** sample (≤2 rows/stem; §5). With 817 Q, 100 stems × 2 = 200 rows is feasible *only* with a stem cap; naive MC2 expansion overrepresents a few stems (the v1 footnote was right to worry, but stated no cap — now fixed).
- ⚠️ **It is recognition, not generation** (v1 overstated its strategic value). It tests whether the model can *rank* candidates, not whether it would *generate* the falsehood. Keep it as breadth + the confidence-stress task; do not let it stand in for P3.
- 📈 **Confidence claim is a hope, not a guarantee.** If confidence *wins* TruthfulQA cells, the paper's "confidence is not the backstop" narrows to "on the original two tasks." Pre-register this as a possible outcome (§6, §7).

### 4.3 FEVER — evidence join + the NEI decision (must-fix #7)
- 🔧 **Join is non-trivial.** `fever/fever` gives page+sentence IDs, not text (§2) → either use `copenlu/fever_gold_evidence` (pre-joined sentence text, but clear the **GPL** tag) or join from `wiki_pages` ourselves. Multi-evidence claims, duplicate-evidence rows, sentence ordering, and evidence-set grouping must be specified so a sloppy join doesn't leak one sentence of a multi-hop set or duplicate claims (the v1 "solved by the variant" was too glib).
- ⚖️ **Balance is not free.** FEVER is class-skewed; the builder must do explicit class-balanced sampling (correcting v1's "Framing A is 0.50 for free" — true only for *paired* emission, not FEVER/TruthfulQA).
- 🧭 **NEI decision (registered):**
  - **Primary FEVER cell = binary SUPPORTS vs REFUTES on gold evidence**, `label 0=SUPPORTED / 1=REFUTED`. Scoped claim: this tests **"contradicted by the given evidence"**, *not* general unsupportedness. Clean labels (gold evidence), exact 2-class.
  - ⚠️ This **does not cover the NEI / insufficient-evidence failure mode** — which is itself a key hallucination class. The review is right that dropping NEI narrows the "unsupported answers" language. We address that two ways: (a) **hedge the paper language** (§7) from "unsupported" to "wrong/contradicted-answer analogs" until P3 lands; (b) optionally register a **separate, exploratory FEVER-NEI-collapsed cell** (`REFUTES∪NEI = 1` vs `SUPPORTS = 0`) with an explicit caveat that **NEI evidence is non-gold** (retrieved, Malon 2018, per §2) — so it measures a noisier construct and is reported *separately*, never pooled with the gold-evidence binary cell.
  - ❌ A clean 3-way SUPPORTS/REFUTES/NEI cell is **impossible** under the binary commit-token contract.

### 4.4 P3 — reworked: "predicting generated short-answer correctness" (must-fix #5)
This is the largest rewrite. v1 called label-1 a "hallucination" detected "at token 1, before the answer is shown." Both over-claim.

- 🏷️ **Rename and reframe.** P3's target is **"predicting whether the model's eventual short generated answer is exact-match correct, from the gen_step=1 commit state."** Label `1 = not exact-match correct` conflates hallucination, ignorance, abstention, formatting mismatch, valid-but-unlisted alias, and ambiguous reference. It is **not** "hallucination" without an audit that separates these.
- 🔬 **First-token-commit audit (registered, before claiming "before the answer is shown").** Generation labels are decided after `max_new_tokens≈16–32`, but the geometry is read at gen_step=1. The first token may be whitespace/newline/"The"/an article/a preamble. We **manually audit N≈100 generations per a representative subset of models** to measure how often token-1 *is* the answer-commit token. The "before the answer is shown" phrasing is licensed **only** to the extent and for the models where the audit supports it; otherwise the claim is strictly "predict eventual correctness from the commit state" (consistent with commit-locus.md's P3 correction).
- 🧹 **Real answer normalization (the v1 alias reuse is insufficient).** `generate_fresh_data._all_aliases` (`generate_fresh_data.py:161-164`) only lowercases/strips for wrong-answer collision avoidance — *not* a grader. P3 needs a documented normalizer: case/whitespace/punctuation/Unicode folding, article stripping, numeric/date canonicalization, the full TriviaQA alias set, and a policy for multi-answer/partial matches. Build it, version it, hash it.
- 🧪 **Manual label-noise audit (registered).** Hand-label N≈100–200 (question, generation) pairs; report the exact-match grader's error rate vs human judgment; if noise is high, report it as a measured limitation (and consider it a ceiling on achievable AUROC).
- 📌 **Pin the offline generator to the extraction (the subtle correctness bug the review flagged).** Offline generation **must** use the *same* `io_plugins.get_prompt_strategy(model_id)` wrapping, tokenizer, **resolved model snapshot** (`model_snapshot_sha`), greedy decoding, stop criteria, and parser as extraction (`comprehensive_run.py:299,327`). If the generator uses raw prompts while extraction uses a chat template for Mistral-Nemo, the labels correspond to a *different* first-token distribution than the geometry — silently invalid. Pin and hash the generation config + seed like all other provenance.
- 🔀 **P3 is analyzed separately (per-model labels).** Shared *examples*, model-specific *labels*. Consequences (understated in v1): transfer across models compares **different label functions**; label-efficiency subsampling is per-model; class balance differs per model. ⇒ **Do not mix P3 into the shared-label N×N transfer matrix.** Its LOMO is a distinct, arguably stronger test — "does a *fixed signal* generalize across models when each model has its own target?" — registered as such (§6). Balance policy: **keep shared questions, let per-model base rate float within the gate's ±0.10, report per-model base rates**, and **drop a model from the cell if its base rate makes AUROC unstable** (state it).

### 4.5 (reserved)

### 4.6 ANLI R2/R3 — robustness only
- Reframe per the review: **same task, harder; adds no failure mode.** It is a monotonicity/robustness probe, **not** counted toward the "N benchmarks" breadth claim. Trivial to build (`split="dev_r2"/"dev_r3"`). Confirm ≥200 disjoint rows after sealed-exclusion (dev sets ≈1,000; the generator raises if short, `generate_fresh_data.py:129-133,236-240`).

---

## 5. Group-aware sampling & effective n (must-fix #6)

The current selector/bootstrap treat **rows as independent** (`_nested_bootstrap_oob_auroc` resamples rows). Several candidates emit **multiple correlated rows per stem**, which inflates n:

| Dataset | Group (stem) | Rows/stem |
|---|---|---|
| TriviaQA-paired (existing) | question | 2 (correct, wrong) |
| HaluEval | source context | 2 (right, hallucinated) |
| TruthfulQA-MC | question | many candidates (must cap) |
| FEVER | claim | ≥1 (duplicate across evidence rows if joined wrong) |

**Registered policy:**
1. 📐 **Cap to ≤2 rows/stem** (one positive, one negative) so groups are size-2 and balanced — the paired builders already do this; TruthfulQA/FEVER builders must enforce it explicitly (no stem contributes >2 rows).
2. 🔢 **Report effective n, never raw n as independent.** n=200 with size-2 stems ⇒ **~100 independent groups** ⇒ effective n≈100. The paper states the group structure, not "200 independent samples."
3. 🧪 **Cluster-bootstrap sensitivity check (registered, descriptive).** Alongside the row-bootstrap deployability CI, run a **stem-level (cluster) bootstrap** where the resampling unit is the *stem*, not the row, and report the CI lower bound. A cell whose deployability flips between row- and stem-bootstrap is flagged (the row-CI was inflated). This is a ~30-line addition in `confluence_calibrator.py`/`analyze_universality.py` and is **descriptive** (does not change the registered per-cell gate, which stays the row-bootstrap CI, for comparability with the seal) — but it is reported for every grouped cell.

---

## 6. The real pre-registration (must-fix #4)

"Each cell deployable-or-not" is too weak for 50+ cells — it lets any failure be narrated as an "honest orphan" and any pass as "breadth." This section fixes the bars **before any matrix is drawn**.

### 6.1 Confirmatory vs exploratory — declared up front
- **Confirmatory** (frozen builders, filters, templates, length/label policies, model inclusion, and bars *before* any feature matrix): the **PRIMARY tasks** and the **primary endpoint** below.
- **Exploratory** (valuable, but cannot upgrade the sealed headline claims; clearly labeled): the FEVER-NEI-collapsed cell, SimpleQA (pilot-gated), ANLI R2/R3, and the full cell×holdout LOMO landscape (multiplicity-prone, `analyze_universality.py:114-128`).

### 6.2 Primary tasks & endpoints
- **PRIMARY tasks (confirmatory):** the shared-label Framing-A set whose licenses clear §2 — target **{HaluEval-QA, HaluEval-Summ, HaluEval-Dialogue, TruthfulQA-MC, FEVER-binary}** = M_new = 5 tasks × 10 models = 50 cells. (P3 is primary too but analyzed on its own track, §6.4.)
- **Primary per-cell endpoint (unchanged from the seal, for comparability):** geometric-only **and** full-panel nested-OOB selected-cell **OOB AUROC 95% CI lower bound > 0.50** (`confluence_calibrator.py:152`).
- **Primary paper-level endpoint = the per-task LOMO universal-floor probe.** This is the claim the title rests on. The machinery already has the registered metric: `fixed_cell_max_survival` — does **one fixed cell**, pool-selected on 9 models, hold **AUROC > 0.55 on ≥ 8/10 holdouts** (`analyze_universality.py:112-124`; interpretation guide `:9-17`). The honest number is the fixed-cell survival, **not** the per-holdout winner survival (which can read high with a different winner each time — `analyze_universality.py:114-117` already warns this).

### 6.3 Bars frozen in advance (the numbers)
For each PRIMARY task (stated per task, since the seal's `19/20` is n=20-specific, `run_seal.py:233-234`):
- 🎯 **Per-task deployability bar:** geometric-only deployable on **≥ 8/10 models** (80%); full-panel reported alongside. (Mirrors the seal's ≈85–95% but re-registered per task; the exact integer is frozen per task in the pre-reg doc, with the rationale, before the run.)
- 🎯 **Per-task LOMO floor bar:** `fixed_cell_max_survival ≥ 8/10` holdouts > 0.55 ⇒ the floor **holds** on that task.
- 🎯 **Cohort-level (expansion) rule — the falsification bar:** define M_pass in advance. *Proposed:* the "universal floor extends to new hallucination regimes" claim is **CONFIRMED** iff the LOMO floor holds on **≥ 4 of the 5** PRIMARY shared-label tasks; **PARTIALLY CONFIRMED / NARROWED** (3 of 5) ⇒ the paper explicitly restricts "universal" to the tasks where it holds and reports the others as orphan regimes; **FALSIFIED as a universal claim** (≤ 2 of 5) ⇒ the floor is reported as specific to the original cohort, and the title's scope is revised. The exact M_pass integer is MK's call (§9) but **must be frozen before the run**.
- 🎯 **What "universal" ranges over (registered):** post-extension, "universal" = across the 10 cohort models **and** the PRIMARY task set; the title's scope is defined here so a single new-task failure cannot silently break or silently inflate it.

### 6.4 P3 analyzed on its own track
- P3 is **not** pooled into the shared-label transfer matrix (§4.4). Its registered endpoints: (a) per-(model) per-cell deployability (same CI gate); (b) a **P3-specific LOMO** with the explicit interpretation "a fixed *signal* generalizes across models that each have a *model-specific* target" — registered as a distinct, stronger generalization test; (c) base-rate + label-noise audit reported regardless of outcome.

### 6.5 Frozen per-cell predictions (the EXT discipline, scaled)
Mirror `PRE_REGISTRATION_EXT.md:56-69`: state, **before any strict metric**, a confidence-tagged prediction. For 50 cells this is done **per task** (predicted pass-count + named likely-orphan cells + predicted LOMO outcome + predicted winner family), plus the abstain-list (cells expected to fail the balance/length gate). Example registered line (illustrative, to be filled in the pre-reg doc): *"HaluEval-Summarization: geometric deployable on ~6/10 (LEAN below the 8/10 bar — long context + ChatGPT-text artifact may help or hurt); LOMO floor GENUINELY OPEN (~50%); likely orphans: the 1.7B/3B models on long summaries."* No prediction gates publication of a cell (`PRE_REGISTRATION_EXT.md:92-94`).

### 6.6 Multiplicity
With 50+ cells and a 29-cell panel, the per-cell landscape is multiplicity-prone. The **primary** endpoints are the *pre-specified fixed-cell* LOMO metric and the per-task deployability bars — **not** the max-over-cells landscape (which is reported descriptively and explicitly flagged, as the code already does, `analyze_universality.py:126-128`).

---

## 7. Paper-language guardrails (must-fix #10)

The expansion is a **labeled post-seal benchmark extension**. It never alters the seal.

- 🔒 **Sealed claims untouched.** The `prereg-seal-20260612` 18/20 verdict, `stage_b/profiles/`, and the "Ten Language Models × two tasks" headline (`cc-draft.tex:173-176`) are frozen. New results land in a clearly-labeled subsection (the draft already has the pattern, `cc-draft.tex:~297-303`), in a new `stage_b/profiles_bench/` dir, under a new pre-registration doc — exactly the EXT relationship (`PRE_REGISTRATION_EXT.md:10-14`).
- ✍️ **Hedge "unsupported answers… before the answer is shown."** The abstract/intro (`cc-draft.tex:72-79`) currently implies deployment-time detection of *unsupported* answers, but the sealed cohort is ANLI entailment/contradiction + paired TriviaQA judgment. Until P3 lands **and** its first-token audit (§4.4) supports it, hedge to **"wrong/contradicted-answer analogs under judgment prompts."** Only P3 makes the abstract literal — and even then, scoped by the audit and to "predicting eventual correctness."
- 🏷️ **Fix the glossary locus error.** `cc-draft.tex:233` says signals are read "at the commit position (step~0)." Per commit-locus.md this is correct **only for ACE**. Change to "commit position" with a footnote: ACE at t=0/prefix-last; PRI/RPV/Confidence at gen_step=1.
- 📊 **"Confidence is not the backstop" is now an empirical bet.** If confidence wins/rescues new cells (TruthfulQA, FEVER), the claim narrows to the tasks where it held. Pre-register this (§6.3) and report honestly; do not restate the seal's version as if unchanged.
- 🧭 **"Universal floor" scope is defined, not assumed.** §6.3 fixes what "universal" ranges over and the falsification rule, so adding heterogeneous tasks cannot silently over- or under-state the title.

---

## 8. Harness edits required (the honest integration surface)

All in `commit-confluence`; none in `t0-morphology-furnace`. Itemized so the cost is explicit (v1 buried this).

1. 🧱 **One builder per benchmark** — clone `build_anli`/`build_triviaqa` (`generate_fresh_data.py:96-287`); HaluEval needs per-subset field branching (§4.1); FEVER needs the evidence join + class-balance (§4.3); all enforce the ≤2-rows/stem cap (§5).
2. 🚪 **Generic gate path** — extend `check_fresh_data.py` beyond `--task {anli,triviaqa}` (`:72`): keep schema/balance/intra-dup; **drop the sealed-reference requirement** for brand-new benchmarks (no sealed predecessor exists) but **add** length checks, one-token-cue heuristic, and stem-cap verification. (Contamination is then bounded by disjoint source splits, not by a sealed-overlap check — §1.3.)
3. 🚀 **Launcher generalization** — `run_seal.py` to accept arbitrary `(task → file)` pairs, a generic `gate_task` map, per-task bars from the pre-reg doc instead of the hardcoded `19/20` (`:233-234`), and the new profiles dir. ⚠️ If this touches `confluence_calibrator.py`, the recorded `module_hashes` change (§1.1) — keep launcher logic in `run_seal.py` (not hashed) where possible.
4. 🔀 **Transfer generalization** — `analyze_universality.transfer()` from exactly-2-tasks (`:137-138`) to all ordered pairs / an N×N matrix, **excluding P3** (different label function, §4.4). E1 LOMO (`:68`) and E3 label-efficiency (`:175`) already scale per task/cell. ⚠️ The N×N transfer for P3-adjacent tasks is *not* a 20-line edit (v1's estimate was optimistic); shared-label transfer is, P3 is a separate code path.
5. 🧪 **Cluster-bootstrap** (§5) and the **smoke harness** (§1.3 clause 6) — new, descriptive, mirroring EXT's limit-8 preview.
6. 🏷️ **New pre-registration doc** (`PRE_REGISTRATION_BENCH.md`) with §6's bars, falsification rule, and frozen predictions — registered before any matrix.

---

## 9. Open decisions for MK

1. ❓ **Effort envelope:** full PRIMARY set (HaluEval×3 + TruthfulQA + FEVER-binary + P3) vs the minimal broad-and-deep trio (HaluEval + FEVER-binary + P3)?
2. ❓ **M_pass falsification integer (§6.3):** confirm "≥4 of 5 PRIMARY tasks must hold the LOMO floor" — or set your own threshold. **Must be frozen before the run.**
3. ❓ **FEVER NEI (§4.3):** binary-only (cleanest), or also register the exploratory NEI-collapsed cell with the non-gold caveat?
4. ❓ **FEVER source:** clear `copenlu` GPL, or self-join from `fever/fever` + `wiki_pages` (CC BY-SA 3.0 only)?
5. ❓ **HaluEval license (§2):** build from RUCAIBox MIT source (recommended) — confirm.
6. ❓ **SimpleQA (§3):** run the base-rate pilot and include iff a model clears a usable positive rate — or defer to the next (larger-model) iteration?
7. ❓ **P3 balance (§4.4):** shared questions + floating per-model base rate (preserves LOMO — recommended) vs per-model 0.50 subsampling (cleaner AUROC, breaks shared-example LOMO)?

---

## Appendix — Code-citation ledger (verified 2026-06-20, for the re-review)

Corrected against the actual files (v1 and the review had a few off-by-N citations; these are the verified lines).

| Claim | File:lines | Verified content |
|---|---|---|
| Loader is prompt/label-only | `t0/pri_calibrator.py:~516` | reads `row["prompt"]`, `int(row["label"])`, rejects ∉{0,1} |
| `benchmark` print-only | `t0/.../comprehensive_run.py:321` | inventory print; no task branch in `trace_pair_features:273-388` |
| Readout locus = gen_step=1 | `confluence_calibrator.py:89-101` → `comprehensive_run.py:324` | "commit instant: gen_step=1" |
| ACE locus = t=0 | `confluence_calibrator.py:330-381`; `run_seal.py:5` | "t=0 attention morphology" |
| `module_hashes` includes harness compute | `confluence_calibrator.py:265-295` | confluence_calibrator.py `:292`, fusion_signs.json `:294`, + 8 T0 modules |
| model snapshot provenance | `confluence_calibrator.py:298-322` | `resolved_revision` from refs/main; compared on resume `run_seal.py:99-101` |
| per-cell deployable gate | `confluence_calibrator.py:152` | OOB AUROC 95% CI lower bound > 0.50 |
| strict no-drop | `run_seal.py:54,58`; `merge_matrices` `confluence_calibrator.py:384+` | `max_new_tokens=1`; `max_dropped=0` |
| drop reasons | `comprehensive_run.py:302-316` | trace_failed/no_gen_step1/missing_readout/nonfinite_* |
| launcher = 2 tasks only | `run_seal.py:122-123,134-136,167,40-44` | `--anli/--triviaqa`; gate_task map; sealed refs |
| n=20-specific bars | `run_seal.py:233-234` | 19/17 when n_planned==20, else 95%/85% scale |
| gate = 2 tasks only | `check_fresh_data.py:72,105-156,115-124` | task choices; TriviaQA balance/qid; sealed ref required |
| builders / templates | `generate_fresh_data.py:46-62,96-287` | ANLI + TriviaQA templates + builders |
| `_all_aliases` is not a grader | `generate_fresh_data.py:161-164` | lowercase/strip only (review said 151-154 — actual 161-164) |
| E2 transfer hard-skips ≠2 tasks | `analyze_universality.py:137-138` | `if len(tasks) != 2: skipped` |
| E1 LOMO registered bar | `analyze_universality.py:9-17,112-124` | fixed_cell_max_survival, >0.55 on ≥8/10 |
| prompt strategy per model | `t0/pri_v2_io_plugins.py:207-259` | raw_passthrough default; chat-template for Mistral-Nemo et al. |
| EXT precedent (template) | `stage_b/PRE_REGISTRATION_EXT.md:5-14,40-99` | limit-8 smoke, byte-comparable Phase 1 vs version-delta Phase 2 |
| paper claims | `cc-draft.tex:72-79,173-176,233` | "before the answer is shown"; cohort; glossary "step 0" |

*No code or data was produced for this proposal. Next concrete step, on MK's go (and after the §2 license gate clears): draft `PRE_REGISTRATION_BENCH.md` with the §6 bars + falsification rule + frozen predictions, then the Phase-1 builders + generic gate + smoke harness, mirroring `generate_fresh_data.py` + `run_ext.py` so the additions stay within the byte-comparable-T0 / separately-hashed-harness envelope of §1.1.*
