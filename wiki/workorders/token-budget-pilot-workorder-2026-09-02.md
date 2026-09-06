# Work order — Detector token-budget pilot ("how many tokens to converge?")

**Date:** 2026-09-02
**Status:** DRAFT **v5** — static-review cycle CLOSED. **Phase-0 build authorized; detector scoring NOT
authorized.** **§0 RESOLVED 2026-09-02 — Lynx DROPPED (MK), headline narrowed in §1.** One class of item
now blocks full freeze: the §4.3/§4.5 manifests (plus the §4.4 `n` decision and phase-0 results).
**Revision history:** v1 **2/10** → v2 **3/10** → v3 **5/10** → v4 (all seven round-3 fixes) → **v5
(2026-09-02, MK: "Drop lynx from work" — §0 resolved, §4.10 removed, headline narrowed).** Round 3's verdict: *"Apply the named
static fixes, then build and run the phase-0 task/label/power gate. Another prose-only adversarial
round would have diminishing returns; the next useful review should inspect the phase-0 artifacts."*
v4 applies all seven. Reviews at `.codex-audit-round{1,2,3}.md`; disposition §11.
**Candidate:** #17 (to be filed in [[research-candidates]] on MK sign-off).
**Register:** descriptive pilot, `$0`, local M4 only. Follows the candidate-#16 precedent — **cannot
upgrade or downgrade any registered verdict**; touches no sealed artifact.
**Origin:** external question relayed by MK 2026-09-02 (Kai): *"how many expected tokens does a SOTA
hallucination classifier need to converge to a classification?"*

---

## 0. MK DECISION — RESOLVED 2026-09-02: **Lynx is DROPPED**

**MK instruction, 2026-09-02: "Drop lynx from work."** This **reverses** the earlier instruction
*"Include Lynx, and INSIDE."* Recorded here rather than deleted, because the reversal is the decision.

**What this closes.** §0 is no longer freeze-blocking. Neither Option A (separate Lynx lane) nor
Option B (one open-book axis) is taken. The pilot runs the **primary axis only**: INSIDE-no-FC and
semantic entropy on closed-book TriviaQA, where both live natively.

**What this costs, stated explicitly — round 3 required exactly this.** Round-3 MAJOR 7 accepted that
*"Lynx is the most literally 'classifier-shaped' comparator in the set"*, and that dropping it
**narrows the answer from "SOTA hallucination classifiers" to "these sampling/internal-state
uncertainty methods."* Round 3 further held that any deferral *"must be explicit, and the headline
claim must narrow to match."* Both conditions are now met: the deferral is explicit here, and §1
narrows the headline. **The generic "how many tokens does a SOTA hallucination classifier need"
question is OUT OF SCOPE for this pilot** and may not be claimed as answered — see §1 and §6.

**Why the design pressure existed at all** (retained for the record). Three rounds established that
Lynx's `DOCUMENT` requirement deformed the whole design: closed-book gives it no document (r1
FATAL 2) → go open-book → oracle evidence changes the construct to reading comprehension (r2 FATAL A)
→ open-book accuracy of 90–98% collapses the error class below the validity gate (r2 MAJOR 1). The
drop removes that pressure entirely.

**If Lynx is ever wanted back**, it returns as its own grounded pilot with claim-level
human-adjudicated labels, not as a lane bolted onto this one. That is Option B in substance and is a
different, much larger study.

## 1. Goal

Measure **detection quality as a function of token budget** and characterise the knee. No vault
artifact produces this — every sealed/registered PRI/ACE result scores at a **single fixed instant**.

> **Round-3 MAJOR 1, accepted.** The word **"confabulation" is removed** from the primary framing.
> Exact-match failure on closed-book QA is a **mixture**: memorization gaps, reasoning failures,
> outdated/ambiguous references, abstention, truncation, format failure, valid-but-unlisted aliases,
> and confidently invented answers. **Only the last is confabulation.** TriviaQA has also been public
> since 2017, so correct answers may reflect benchmark exposure rather than factual competence.

**The primary question, stated exactly:**

> **How many sampled answer tokens do INSIDE-no-FC and semantic entropy need to approach their own
> full-budget AUROC for predicting eventual TriviaQA exact-match correctness?**

Relevance to hallucination detection is a **bounded proxy claim**, stated as such.

> **HEADLINE NARROWED (§0 decision, 2026-09-02).** The generic *"how many tokens does a SOTA
> hallucination classifier need to converge"* question — the origin question relayed from Kai — is
> **NOT answered by this pilot and is out of scope.** With Lynx dropped, the comparator set contains
> no classifier-shaped detector, so the answer this pilot can support is narrower: *how many sampled
> answer tokens these sampling- and internal-state uncertainty methods need.* Any report, result page,
> or reply to Kai must state that narrowing rather than let the original question stand as answered.

## 2. Task — closed-book TriviaQA exact-match correctness

**Outcome: `closed_book_short_answer_incorrectness`.** Not "hallucination", not "faithfulness", not
"confabulation".

- **Population — PINNED:** `rc.wikipedia.nocontext`, `validation` split, dataset revision +
  fingerprint recorded, unique `question_id` as the row key.
- **Answer contract — PINNED:** the **official TriviaQA evaluator normalizer**
  (lowercase; strip articles, punctuation, underscores, extra whitespace), matched against
  `answer.normalized_aliases`. ⚠️ Round 3 verified the official evaluator also consults
  `HumanAnswers`, **which the current HF schema does not expose** — so this is a documented
  *subset* of the official contract, declared here rather than silently diverged.
- **Match rule — PINNED:** whole-string **normalized exact equality**. Round-3 MINOR 1 is right that
  "token-boundary exact match" was incoherent; there is no partial matching.
- Answer-only output enforced; abstention, multiple-answer, contradiction, and invalid-format rules
  frozen in §4.5.

> **Round-3 MAJOR 2, accepted.** Curated aliases beat HaluEval's single gold answer but **no finite
> alias list is complete**, and the §9 corpus audit runs *before* generation so it cannot inspect the
> decisive set: **generated non-matches a human judges correct.** Without that, a detector can win by
> predicting verbosity, spelling, or format compliance rather than knowledge error. A **blinded human
> audit of generated matches and non-matches, per model, stratified, is therefore a phase-0
> deliverable** (§9 command 2). Aliases are **never** expanded after looking at detector scores.

## 3. The ladder

| Detector | Source | Budget | Role |
|---|---|---|---|
| PRI `null_ratio_post_rank1` | internal states | 1 generated token | anchor |
| max-softmax confidence (floor) | output distribution | 1 generated token | anchor |
| **INSIDE / EigenScore (no FC)** | internal states | `K` x `L` | **primary curve** |
| **semantic entropy** | text + NLI | `K` x `L` | **primary curve** |
| ~~Lynx-8B~~ | text + document | — | **DROPPED — MK decision §0, 2026-09-02** |
| ACE | internal states | 0 tokens | **APPENDIX ONLY — OOD transfer probe** |

> **Round-3 MAJOR 6, accepted.** v3 demoted ACE in prose but left it in the ladder table and in the
> "advantage over the ACE/PRI anchors" framing. **An OOD cell with explicitly uninterpretable
> performance cannot anchor a performance comparison.** ACE is out of the primary ladder entirely and
> appears only in an appendix table, with no performance-equivalence claim.

**INSIDE remains load-bearing** — same information source as our anchors, paying `K` sampled answers.
Every method is rooted in the same subject prompt and **none receives privileged evidence** (they
necessarily consume different generated prefixes).

## 4. Design

### 4.1 The knee rule

**Method name: max-standardized bootstrap** (round-3 MAJOR 5 — the denominator is one fixed bootstrap
SD, not a replicate-specific SE, so this is *not* literal bootstrap-`t`; naming it correctly).

Within each `(model, detector, axis)` family, axis ∈ {`L` at frozen `K=K_max`, `K` at frozen `L=full`}:

1. Resample **prompts** with replacement, **`B = 10,000`** replicates (round-3: 2,000 leaves ~100 draws
   above the 95th percentile), seed `20260902`, empirical quantile convention **type-7, pinned**.
2. `Δ_j^(b) = AUROC_j^(b) − AUROC_Bmax^(b)`, paired on the same rows. **`B_max` is the predeclared
   largest budget, not the empirically best** — round 3 confirms this means **no selection or
   regression-to-the-mean bias**, so same-row comparison is correct. Selection bias would enter only
   through choosing configurations or signs on these rows, which §4.3/§4.5 forbid.
3. `ŝe_j` = bootstrap SD of `Δ_j`.
4. `c = P95_b [ max_j ( (Δ̂_j − Δ_j^(b)) / ŝe_j ) ]`;  `Lo_j = Δ̂_j − c · ŝe_j`.
5. **Knee** = smallest **non-reference** grid point `j*` with `Lo_j ≥ −δ` at `j*` and every later budget.

**Zero-SE rule (round-3 MAJOR 5 — v3's blanket exclusion was wrong):**
- `ŝe_j = 0` **and** `Δ̂_j = 0` ⇒ empirical equality ⇒ the coordinate **passes** with `Lo_j = 0`.
- `ŝe_j = 0` **and** `Δ̂_j ≠ 0` ⇒ frozen **unstudentized fail-closed** rule; coordinate marked
  `budget-not-estimable`.
- An excluded coordinate is **never silently skipped** in "every later budget" — it is a barrier.

**Exhaustive status partition:** `knee=j*` (non-reference only) · `endpoint-only` (all required
non-reference candidates fail) · `budget-not-estimable` (a required coordinate undefined/degenerate) ·
`not-estimable` (class gate, informativeness gate, or family-level numerical failure).

**Gates.** Full-budget informativeness: bootstrap **percentile** `CI_lo > 0.50`. **Candidate
informativeness:** a candidate budget must itself clear `CI_lo > 0.50` — without this, at `δ = 0.05` a
full AUROC barely above 0.50 could declare a near-chance early score "converged." Validity floor
`min(n_correct, n_error) >= 40`. **Never pool models to rescue a gate.** Invalid one-class / NaN
bootstrap replicates: frozen disposition rule, count reported.

**Raw curves with simultaneous bands are the primary reported object.** The knee is a derived summary.

**Score convergence**, per axis: smallest grid point where the **bootstrap CI lower bound** on Spearman
clears `0.95` (round-3 MAJOR 7 — v3 left `ρ` vs `CI_lo` ambiguous), percentile interval, `B = 10,000`,
frozen tie and NaN handling. N/A where the score is mathematically degenerate.

### 4.2 Budget grids and the `K` estimand

- `L ∈ {1, 2, 5, 10, 20, 50, full}`. **`full`** = through first EOS, excluding EOS and pads, capped at
  `max_new_tokens`.
- `K ∈ {3, 5, 10}`; **`K = 1` is N/A** for INSIDE and semantic entropy (degenerate statistics).
- **`K_bank = 20`** draws per prompt.

> **Round-3 FATAL 2 — the subtlest catch of the cycle, accepted.** v3 said "average over 100 subsets"
> without saying *at what level*. If the implementation averages the 100 subset **scores per prompt**
> and then computes one AUROC, a nominal `K=3` detector has **indirectly consumed all 20 banked
> answers** — a 20-draw ensemble wearing a 3-draw cost label. Failure scenario: the score-averaged
> `K=3` curve is artificially smooth, looks non-inferior to `K=10`, and the claimed early sample knee
> **evaporates** once each evaluation truly consumes three draws.

**PINNED aggregation:** define **100 common subset schedules across prompts**; compute
`AUROC_j^(b,r)` for prompt-bootstrap replicate `b` and schedule `r`; **each bootstrap endpoint is the
mean over `r`**. Per-prompt scores are **never** averaged across schedules. Schedule nestedness across
`K`, the seed-to-index algorithm, and schedule Monte-Carlo error reporting are frozen in §4.5.

**Prefix slicing** is valid for `L`: use the generated token's state (not pre-sampling), stop at first
EOS, never touch pads, hold template and cache semantics fixed. Verified by §9 command 3.

### 4.3 Comparators

1. **`pri_null_ratio_post_rank1`** — rank 1, first-generated-token locus. **TBD (freeze-blocking):**
   residual-state convention, Fisher reweighting, profile/sign provenance hash.
2. **`confidence_max_softmax`** — max-softmax at first generated token; orientation frozen from data
   **disjoint from the scored rows**, or cross-fitted.
3. **`inside_eigenscore_no_fc_last_content_middle`** — `T=0.5`, `top-p 0.99`, `top-k 5`, middle-layer
   **last content token** before EOS, `α = 0.001`. **TBD:** released source revision; exact block index
   including whether the hidden-state tuple's embedding output shifts the apparent middle; `K x K`
   covariance orientation; centering; `d` vs `d−1`; log base; off-by-one.
4. **`semantic_entropy`** — **likelihood-weighted** estimator, **bidirectional** entailment, question in
   the premise, greedy answer excluded. **TBD:** sequence-probability length normalization, NLI label
   mapping and threshold, clustering order policy. Model: cached
   `MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli`.
5. **`ace_t0_ood_transfer`** — imported sealed cell, **no refit**, appendix only, no
   performance-equivalence claim. `js_no_bos` keeps its standing rule: **undefined under BOS-sink
   collapse, reported as undefined, never zero, never dropped.**

One frozen, literature-faithful, compatible configuration each; excluded capabilities (feature
clipping; a refit ACE) named explicitly. **Not** "strongest observed variant."

### 4.4 Sample size — prospective expansion, not balancing

> **Round-3 MAJOR 3, accepted — v3's "balanced by construction" was FALSE.** Correctness labels are
> **produced by each model**, so they cannot be balanced by choosing rows before generation, and
> selecting rows afterward to force 50/50 would create a case-control estimand v3 never defined. The
> 50–70% band was a planning guess, not a design fact — Meta reports **77.6 EM** for Llama-3.1-8B base
> on 5-shot TriviaQA-Wiki (different variant, prompt, precision, evaluator, so not predictive of this
> cell, but enough to reject the band as settled). Above 92% accuracy the error class falls below 40;
> below 8%, the correct class does. **Also: Phi-3.5-mini is ~3.8B, not "7–8B".**

**PINNED:** one **shared, frozen, ordered question pool** (3,000 rows) with a deterministic expansion
rule — **start at the MK-authorized `n = 2000`**, expand in 500-row blocks to the 3,000 cap — until
every intended model clears both the class gate and the simultaneous-power gate, **or that cell is
reported not estimable.** Rows are **never** selected to balance outcomes. Base rates are estimated without outcome-balanced selection,
then power is recomputed at observed and conservative ratios (§9 command 4).

**`δ` — an estimand choice, not a power choice (round-3 MAJOR 4).**

> Codex's straight answer on v3: ***"as written, it is margin-shopping."*** Moving from "0.02 does not
> fit `n=500`" to "therefore 0.05 is appropriate" supplies no domain reason that losing five AUROC
> points is negligible. **Accepted.**

`δ = 0.05` is retained **only** under all of: (a) it is declared a **coarse five-AUC-point saturation
region**, (b) **raw curves are the primary result**, (c) **equivalence and deployment language is
prohibited**, and (d) the §9 simultaneous power simulation **passes at observed base rates and
conservative paired correlations**.

#### PHASE-0 RESULT (RUN 2026-09-02) — `freeze/power_knee.json`, 288 cells

Executed by the steward on the M4 (Codex may not run code). Binormal simulation driving the **actual**
§4.1 procedure over the full `L` and `K` family sizes; `AUC_full = 0.75`, true `Δ = 0`, 300 simulation
replicates, 2,000 bootstrap replicates, seed `20260902`. Reported figure is `min_power` across the
paired-correlation sweep (0.50 / 0.80 / 0.90) — the conservative limb.

| `n` | δ=0.02 (10% / 20% / 30% / 50% err) | δ=0.05 (10% / 20% / 30% / 50% err) |
|---:|---|---|
| 500 | .037 / .040 / .073 / .087 | .137 / .273 / .400 / .483 |
| 1000 | .060 / .090 / .087 / .140 | .350 / .563 / .687 / **.830** |
| 1500 | .077 / .177 / .190 / .183 | .443 / .787 / **.877** / **.930** |
| 2000 | .100 / .147 / .200 / .263 | .653 / **.930** / **.963** / **.987** |
| 3000 | .153 / .267 / .400 / .433 | **.807** / **.983** / **1.00** / **1.00** |
| 5000 | .260 / .473 / .610 / .700 | **.957** / **1.00** / **1.00** / **1.00** |

**Three findings, all binding:**

1. **`δ = 0.02` is unreachable.** It never clears 80% at any simulated `n`, topping out at **.700** at
   `n = 5000` with balanced classes. **`δ = 0.02` is removed from the design.**
2. **Round 3's own planning figures were optimistic, and the simulation corrects them.** Round 3
   estimated *"roughly 2,000–3,000 for simultaneous 30/70"* at `δ = 0.02`; the measured value at
   `n = 3000`, 30% errors is **.400**, not ~.80. Static arithmetic under-counted the cost of the
   simultaneous multiplicity across the full `L`+`K` grid. This is precisely the class of error the
   execute-and-verify discipline exists to catch.
3. **`δ = 0.05` is affordable, and `n` is set by the base rate.** `n = 2000` clears 80% for error rates
   `>= 20%`; `n = 1500` clears at `>= 30%`; `n = 3000` is needed at 10%. **`n = 500` fails everywhere**
   — v3/v4's figure is dead.

#### ✅ MK DECISION 2026-09-02: **`n = 2000`, `δ = 0.05`** (powered-knee option)

**Authorized.** Compute rises 4x over the dead `n = 500` figure — `2000 x 20 x 3 = 120,000` sampled
generations, order **2–4 days** wall-clock, still `$0`. Rejected alternatives: curves-only at `n = 500`
(no point-knee claim) and the `n = 1500` gamble.

**Coverage this buys:** ≥80% power at error rates **≥ 20%** (`.930 / .963 / .987` at 20/30/50%).

> ⚠️ **Residual risk, stated plainly.** The steward recommended measuring the base rate *before*
> fixing `n`; MK fixed it first. The decision is defensible — the one external anchor (Meta's **77.6
> EM** for Llama-3.1-8B base, 5-shot TriviaQA-Wiki, different variant/prompt/precision/evaluator)
> implies ~22% errors, just inside coverage. **The exposure is a low error rate:** at 10% errors
> `n = 2000` gives only **.653**. That happens if the models prove more accurate than expected, or if
> lenient alias matching suppresses the error class.
>
> **Contingency — already in the design, no amendment needed.** §4.4's prospective expansion rule
> (shared frozen ordered pool of 3,000, expansion in 500-row blocks) covers it: if the measured base
> rate lands below 20% errors, expand toward `n = 3000`, which restores **.807** at 10%. `n = 2000` is
> therefore a **starting target under the standing expansion rule**, not a hard cap. Rows are still
> never selected to balance outcomes.

### 4.5 Freeze-blocking manifest

All TBD, all freeze-blocking: prompt and chat template; `max_new_tokens`; stop strings; answer-only
enforcement; bank sampling `T / top-p / top-k`; EOS and pad treatment; abstention, multiple-answer and
contradiction rules; subset schedule nestedness and seed-to-index algorithm; sign/calibration split
(must not select on scored rows); and invalid-replicate disposition. *(The §4.10 Lynx protocol was
removed from this list by the §0 drop.)*

### 4.6 INSIDE feature clipping — separated

Feature clipping intervenes on **generation** via a dynamic memory bank; it **cannot** be applied
post-hoc to an unmodified bank. Primary is **no-FC**, named `EigenScore without FC` everywhere.

### 4.7 Quantization — scoped estimand plus precision control

EigenScore is a **log-determinant**, error `≈ tr[(Σ+αI)⁻¹ΔΣ]`, **amplifying perturbations in
eigen-directions near the `α = 10⁻³` floor**. Quantization is deterministic, so a within-4-bit estimand
survives; a *mechanistic* claim about INSIDE does not.

**PINNED (round-3 MAJOR 4 — v3's "where possible" was an either/or):** subject **Qwen2.5-7B-Instruct**,
precisions **MLX 4-bit vs fp16** with model revision recorded, `n = 50`, **shared token bank
(mandatory, not "where possible")**, same layer convention and score code. **Comparison statistic:**
paired difference in EigenScore rank correlation and in AUROC, with percentile CI. Both sensitivities
reported: fixed-token representation, and native-generation system.

### 4.8 Token accounting — three quantities

(a) subject generated tokens consumed; (b) auxiliary input tokens / forwards; (c) auxiliary generated
tokens to parsed verdict. Never compressed without an explicit conversion rule. Planned `K x L` is
**not** expected actual tokens under EOS.

### 4.9 Prospective descriptive prediction

> **INSIDE saturates early in `L`, late in `K`:** `L`-knee `<= 10`, `K`-knee `>= 5`.

Reported as **two separate knees** — they do not multiply into one budget.

### 4.10 The Lynx lane — **REMOVED (MK decision §0, 2026-09-02)**

This section specified the lane that round-3 MAJOR 7 required before Option A could honestly claim to
satisfy *"Include Lynx"*. **Lynx is dropped, so the lane is not built and its TBDs are no longer
freeze-blocking.** For the record, what it would have needed: grounded dataset and split; document
construction; claim-level labels (gold-string matching cannot carry faithfulness); a prefix grid for
the accumulating answer; verdict score plus a continuous PASS-vs-FAIL logprob margin at a fixed locus;
invalid-output policy; deterministic decode; chat template; quantization conversion provenance; and its
own token accounting. That list is why the lane was expensive, and it stands as the entry cost if Lynx
ever returns as its own pilot.

## 5. Commitment — CUT

The oracle was not a coherent statistic (intractable "mass", finite-branch frequency ≠ probability
mass, retrospective by construction). The commit-vs-converge distinction MK raised remains real and
deserves **its own pre-registration**. Not an axis of this pilot.

## 6. Scope limits (binding)

Descriptive; cannot upgrade or downgrade E1/E5/E6, any sealed claim, panel number, or the DC draft. No
pooling across models, tasks, or precision regimes. MLX 4-bit plus the §4.7 control; NON-byte-comparable
with the torch/Modal depth lane. No sealed file edited — code in
`commit-confluence/exploratory/token-budget/`, sealed selector imported read-only. **`$0`** — Modal
credit was **$9.80** on 2026-08-18, the 405B run is parked on it, candidate #14 is funding-gated.

## 7. Compute (M4 Mac mini, 32 GB)

`K_bank = 20` x `n` x 3 models dominates; wall-clock only. ⚠️ **Disk binding: 25 GiB free** — the fp16
control sequences download → use → delete. *(The Lynx conversion, previously the other disk consumer,
is removed by the §0 drop.)*

## 8. Model repertoire

| Model | Params | Role |
|---|---|---|
| `Qwen2.5-7B-Instruct-4bit` | 7B | prior panel winner: attention; also §4.7 precision control |
| `Llama-3.1-8B-Instruct-4bit` | 8B | prior panel winner: **readout (panel-relative)** |
| `Phi-3.5-mini-instruct-4bit` | **~3.8B** | forced-choice low-decidedness stress case (transfer unknown) |
| Qwen2.5-7B **fp16** | 7B | §4.7 precision control |

A **purposive heterogeneous convenience sample**, not evidence of architecture regimes. Mistral-7B
stays cut (its 0.989 came from the off-task paired-prompt setting).

## 9. Phase-0 gate — AUTHORIZED TO BUILD AND RUN

**Detector scoring remains unauthorized until these artifacts are reviewed.**

```bash
cd /Users/msrk/Documents/commit-confluence

# 1. corpus + alias audit (no models)
python exploratory/token-budget/audit_triviaqa_task.py \
  --config rc.wikipedia.nocontext --split validation --alias-source official-normalized \
  --n-audit 200 --seed 20260902 \
  --checks alias-coverage answerability duplicates malformed gold-validity \
  --out exploratory/token-budget/freeze/triviaqa_task_audit.json

# 2. generated-label audit — blinded human adjudication of matches AND non-matches
python exploratory/token-budget/audit_generated_labels.py \
  --manifest exploratory/token-budget/freeze/protocol.json \
  --models mlx-community/Qwen2.5-7B-Instruct-4bit mlx-community/Llama-3.1-8B-Instruct-4bit \
           mlx-community/Phi-3.5-mini-instruct-4bit \
  --ordered-question-pool 3000 --initial-n 500 --increment 500 \
  --human-audit-per-model 200 --stratify match nonmatch \
  --out exploratory/token-budget/freeze/generated_label_audit.json

# 3. prefix-slicing equivalence
python exploratory/token-budget/verify_prefix_equivalence.py \
  --models mlx-community/Qwen2.5-7B-Instruct-4bit mlx-community/Llama-3.1-8B-Instruct-4bit \
           mlx-community/Phi-3.5-mini-instruct-4bit \
  --dataset triviaqa --n 20 --k 10 --lengths 1 2 5 10 20 50 --mode no-fc \
  --out exploratory/token-budget/freeze/prefix_equivalence.json

# 4. power under the SIMULTANEOUS rule, incl. skewed minority classes
python exploratory/token-budget/power_knee.py \
  --n-values 500 1000 1500 2000 3000 5000 --auc-full 0.75 \
  --absolute-margins 0.02 0.05 --error-rates 0.08 0.10 0.20 0.30 0.40 0.50 \
  --paired-correlations 0.50 0.80 0.90 --simultaneous-method max-standardized \
  --l-grid 1 2 5 10 20 50 full --k-grid 3 5 10 \
  --one-sided-alpha 0.05 --bootstrap-replicates 10000 --power 0.80 \
  --out exploratory/token-budget/freeze/power_knee.json

# 5. knee rule against fixtures with KNOWN answers, incl. every degenerate case
python exploratory/token-budget/verify_knee_rule.py \
  --fixture exploratory/token-budget/fixtures/knee_cases.json \
  --simultaneous-method max-standardized --one-sided-alpha 0.05 \
  --absolute-margin 0.05 --bootstrap-replicates 10000 \
  --require-zero-se-cases --require-invalid-replicate-cases \
  --require-exhaustive-statuses --require-score-convergence-cases \
  --out exploratory/token-budget/freeze/knee_rule_audit.json

# 6. K-subset schedule design — verifies AUROC-level, not score-level, averaging
python exploratory/token-budget/audit_k_subsets.py \
  --bank exploratory/token-budget/artifacts/sample_bank.jsonl \
  --k-values 3 5 10 --subsets-per-k 100 --require-bank-k-min 20 \
  --aggregation auroc-per-schedule --forbid-score-averaging \
  --prompt-resampling-unit --seed 20260902 \
  --out exploratory/token-budget/freeze/k_subset_audit.json

# 7. precision control
python exploratory/token-budget/precision_sensitivity.py \
  --manifest exploratory/token-budget/freeze/precision_control.json \
  --out exploratory/token-budget/freeze/precision_sensitivity.json
```

⚠️ Prefix-equivalence may fail a zero-tolerance limb on kernel differences even when the causal
equivalence holds. It must then report **token-prefix identity separately from numeric deltas**, with
tolerance justified **before** the full run, never after seeing performance.

**Handoff.** Author: Claude Code (steward). Audit: Codex `gpt-5.6`, write/audit-only — rounds 1–3
complete, **static cycle closed by round-3 verdict**. Build: Codex. Execute + verify: Claude Code on
the M4 — every finding re-verified **by execution**, the half Codex may not perform (the #16 discipline
that produced two retractions). Propagate: rule 5 / 5b eleven-surface pass.

## 10. Contamination hazard — REFUTED (round 1); **MOOT since 2026-09-02**

*Retained as the audit record only. With Lynx dropped (§0), this hazard no longer applies to any
detector in the pilot.* Lynx's disclosed 2,400-example fine-tuning set is **RAGTruth, DROP, CovidQA, PubMedQA** (600 each);
HaluBench is its **evaluation** benchmark; HaluEval is **not** a training source. ~0.98 confidence on
disclosed SFT; **unresolvable** for base Llama-3 pretraining. The real Lynx problem was the
information-set mismatch, resolved by §0 separation.

## 11. Disposition

**Round-3 findings — all accepted:** FATAL 1 (not frozen) — **status changed**, v4 authorizes phase-0
only · FATAL 2 (`K` aggregation leak) — **closed**, §4.2 AUROC-per-schedule · MAJOR 1 (confabulation
overclaim) — **closed**, §1 · MAJOR 2 (alias fidelity) — **closed as a gate**, §9 command 2 ·
MAJOR 3 ("balanced by construction" false; Phi 3.8B) — **closed**, §4.4/§8 · MAJOR 4 (margin-shopping)
— **accepted verbatim**, §4.4 four conditions · MAJOR 5 (zero-SE, statuses, `B`, naming) — **closed**,
§4.1 · MAJOR 6 (ACE still in ladder) — **closed**, §3 · MAJOR 7 (Lynx lane unspecified) — **superseded 2026-09-02**:
MK dropped Lynx (§0), so the lane is not built; MAJOR 7's binding condition (an explicit deferral plus
a narrowed headline) is satisfied in §0 and §1 · MINOR 1–4 — **closed**.

**Round-3 corrections to v3's own §11 over-claims, accepted:** FATAL 3/MAJOR 4/MAJOR 7 were labelled
"Closed" when they were improved-not-closed; MAJOR 2 (power) was labelled "Closed by margin" while
resting on a false balance premise. v4 does not repeat the pattern — see "Known open" below.

**Round 3 also cleared one concern I raised:** `B_max` is **predeclared**, not selected on observed
AUROC, so same-row paired comparison carries **no** regression-to-the-mean bias.

## 12. Phase-0 execution record (2026-09-02)

Built by Codex, **executed and verified by the steward** — the half Codex may not perform.

| Artifact | Result |
|---|---|
| `knee_rule.py`, `verify_knee_rule.py`, `fixtures/knee_cases.json`, `power_knee.py`, `README.md` | written |
| `freeze/knee_rule_audit.json` | **PASS 15/15** fixtures at `--bootstrap-replicates 10000` |
| `freeze/power_knee.json` | 288 cells — see §4.4 |

**Verified by reading the implementation against §4.1:** error direction `Δ̂_j − Δ_j^(b)` correct;
`c = P95` of the max over positive-SE coordinates; `Lo_j = Δ̂_j − c·ŝe_j`; `zero_equal → 0.0` (passes),
`zero_nonzero → NaN` (barrier); candidate-informativeness gate present and firing.

**Fixtures confirmed to be real tests, not decoration** — `nonmonotone_sustained_crossing` carries an
explicit `forbidden_knee_budget: 1` for the round-2 `[0.72, 0.68, 0.75]` trap, and
`failed_candidate_informativeness` uses AUROCs `[0.505, 0.55]` with `raw_delta_at_least: -0.05`, so the
raw difference *would* pass `δ = 0.05` and is caught only by the informativeness gate.

**Environment finding — could not have been found by static review.** The repo's top-level `.venv` is
**Python 3.9** and cannot import this code (`X | Y` type-alias syntax raises `TypeError`). A dedicated
interpreter was created at `exploratory/token-budget/.venv` (Python 3.11.15, numpy 2.4.6, scipy 1.17.1)
and documented in the lane README.

**Still not run:** `audit_triviaqa_task.py`, `audit_generated_labels.py`, `verify_prefix_equivalence.py`,
`audit_k_subsets.py`, `precision_sensitivity.py` — not yet built. The **base-rate measurement gates the
`n` decision** (§4.4) and is the next build step.

## 12b. PHASE-0 BASE-RATE PROBE (RUN 2026-09-02) — one gate cleared, one construct defect found

`generate_answers.py`, Qwen2.5-7B-Instruct-4bit, **n = 200**, frozen `freeze/protocol.json`, greedy,
answer-only. Executed by the steward.

| Quantity | Value |
|---|---|
| correct | **75 (37.5%)** |
| errors | **125 (62.5%)** |
| **abstentions (`UNKNOWN`)** | **78 (39.0% of all rows)** |
| abstentions as a share of **errors** | **78 / 125 = 62.4%** |
| generated tokens | mean 2.10, median 2, max 9 |
| stop reason | `eos` 200/200 |

**✅ The power gate is comfortably cleared, and MK's `n = 2000` holds.** Minority class is *correct* at
37.5%, sitting between the §4.4 table's 30% and 50% rows ⇒ power **.963–.987**. At `n = 2000` that is
~750 correct / ~1250 errors, far above the 40-per-class floor. **No expansion toward 3,000 needed.**
The residual risk flagged at the MK decision (accuracy too *high*) did not materialise — it went the
other way, harmlessly.

**❌ Construct defect: the label is dominated by abstention, not error.** The frozen prompt says
*"If you do not know, return exactly UNKNOWN"*, and `answer_contract.abstention` counts abstention as
incorrect. Consequence: **62% of the positive class is the model declining to answer.** A detector
trained against this label largely predicts *"will the model say UNKNOWN"* — which is trivially
readable from confidence and is the **opposite** of hallucination. An abstaining model is
well-calibrated, not confabulating.

This is round-3 MAJOR 1 made concrete and measured: the outcome *"combines memorization gaps, reasoning
failures, ... **abstention**, truncation/format failure, valid-but-unlisted aliases, and confidently
invented answers. Only the last subset is confabulation."* The probe shows abstention is not a tail
contaminant — **it is the majority of the signal.**

**Options (MK decision):**
- 🎯 **(A) Forbid abstention — force a guess. RECOMMENDED.** Every row becomes a commitment, so a wrong
  answer *is* a confabulation. This aligns with the whole Furnace line's framing — PRI/ACE measure **at
  commitment**, and an abstaining row has no commitment to measure. Cheapest fix: amend the prompt,
  regenerate (only 200 rows exist), no pool expansion, `n = 2000` unchanged.
- ✂️ **(B) Exclude abstentions**, score committed rows only. Preserves the current prompt but discards
  ~39% of rows: 2,000 generated ⇒ ~1,220 committed (75 correct / 47 error per 122). Reaching 2,000
  *committed* rows needs ~3,280 generated, **exceeding the frozen 3,000-row pool cap.**
- ⚠️ **(C) Keep as-is.** Cheapest, and scientifically the weakest — the headline would have to say the
  detectors predict *answer-attempt failure including abstention*, not hallucination.

**Also measured:** answers are extremely short (median **2** tokens, max 9). This is a **threat to the
whole pilot** — the `L ∈ {1,2,5,10,20,50,full}` prefix grid mostly exceeds the actual answer length, so
`L=5` and beyond may be identical to `full` for most rows, collapsing the `L` axis. **The `L` grid must
be re-derived from the realized token-length distribution before the bank is generated**, or the
sampled-answer format must be widened (e.g. permit a short justification). Filed as freeze-blocking.

## 13. Known open

**Genuinely blocking full freeze:**
1. ~~§0 MK decision~~ — **RESOLVED 2026-09-02: Lynx dropped**, headline narrowed in §1. No longer blocking.
1b. **§4.4 `n` decision** — powered knee (`n=2000`) vs curves-only (`n=500`) vs gamble (`n=1500`),
    which must follow the base-rate measurement, not precede it.
2. §4.3 upstream-source TBDs (PRI, INSIDE, semantic entropy).
3. §4.5 protocol values, incl. subset-schedule algorithm and sign/calibration split.
5. Phase-0 empirical results — base rates, alias disagreement, simultaneous power.
