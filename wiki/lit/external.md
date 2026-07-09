# External Papers

Third-party papers that seed, contextualize, or contrast with Furnace research. Stored in `raw/papers/external/`.

| File                                                                                                                   | Title                                                           | Author / Year                                                                                             | Relevance                                                                                                                                                                                                                                              |
| ---------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [karpathy-llm-wiki.md](../../raw/papers/external/karpathy-llm-wiki.md)                                                 | LLM Wiki                                                        | Karpathy, 2026                                                                                            | Root methodology for this vault                                                                                                                                                                                                                        |
| [kalai-2025-why-llms-hallucinate.pdf](../../raw/papers/external/kalai-2025-why-llms-hallucinate.pdf)                   | Why Language Models Hallucinate                                 | Kalai, Nachum, Vempala, Zhang (OpenAI / Georgia Tech), 2025                                               | Theoretical grounding for hallucination inevitability; connects to PRI's detection framing                                                                                                                                                             |
| [token-level-selfconsistency.pdf](../../raw/papers/external/token-level-selfconsistency.pdf)                           | Token-Level Self-Consistency for Hallucination Detection        | Wastl, Vamvas, Sennrich (UZH), SemEval 2025                                                               | Token-level hallucination span detection via consistency — closest external method to PRI's per-token approach                                                                                                                                         |
| [farquhar-2024-semantic-entropy-nature.pdf](../../raw/papers/external/farquhar-2024-semantic-entropy-nature.pdf)       | Detecting Hallucinations in LLMs Using Semantic Entropy         | Farquhar, Kossen, Kuhn, Gal (Oxford), Nature 2024                                                         | Primary competitor/complement — entropy-based confabulation detection; key comparison point for PRI                                                                                                                                                    |
| [agrawal-2024-hallucinated-references.pdf](../../raw/papers/external/agrawal-2024-hallucinated-references.pdf)         | Do Language Models Know When They're Hallucinating References?  | Agrawal, Suzgun, Mackey, Kalai (MSR / Stanford / OpenAI), 2024                                            | LMs have internal signal of hallucination — supports PRI's premise that internals are informative                                                                                                                                                      |
| [process_theory.pdf](../../raw/papers/external/process_theory.pdf)                                                     | Active Inference: A Process Theory                              | Friston, FitzGerald, Rigoli, Schwartenbeck, Pezzulo, Neural Computation 2017                              | Process-level active inference; variational free energy as Lyapunov function; theoretical backdrop for SUP's bounded-imprecision thesis                                                                                                                |
| [Active inference and learning.pdf](../../raw/papers/external/Active%20inference%20and%20learning.pdf)                 | Active Inference and Learning                                   | Friston, FitzGerald, Rigoli, Schwartenbeck, O'Doherty, Pezzulo, Neuroscience & Biobehavioral Reviews 2016 | Goal-directed vs habitual behavior under free energy; epistemic vs pragmatic action; connects to SUP's orbital convergence framing                                                                                                                     |
| [Active inference and epistemic value.pdf](../../raw/papers/external/Active%20inference%20and%20epistemic%20value.pdf) | Active Inference and Epistemic Value                            | Friston, Rigoli, Ognibene, Mathys, Fitzgerald, Pezzulo, Cognitive Neuroscience 2015                       | Epistemic value = information gain as intrinsic motivation; precision-weighting of beliefs; theoretical parent of SUP's ℏ_s formulation                                                                                                                |
| [hu-2025-harp-hallucination-subspace.pdf](../../raw/papers/external/hu-2025-harp-hallucination-subspace.pdf)           | HARP: Hallucination Detection via Reasoning Subspace Projection | Hu, Tu, Cheng, Li, Wang, Chen, Zhou, Shan (HUST), 2025                                                    | **Direct overlap with v3 null-space.** Same geometric object (SVD null space of W_unemb), different weighting (raw vs Fisher-pullback), different feature (raw h vs normalized Δh ratio), supervised vs unsupervised. Primary comparator for v3 paper. |
| [24110_Efficient_Hallucination_.pdf](../../raw/papers/external/24110_Efficient_Hallucination_.pdf)                     | Efficient Hallucination Detection for LLMs Using Uncertainty-Aware Attention Heads (RAUQ) | Anonymous, ICLR 2026 under review                                                                         | **Direct overlap with inter-head diagnostic.** Per-layer head-select on max attention to preceding token, recurrent confidence propagation, single-pass <1% latency. Mechanism (uncertainty-aware heads drop $i-1$ attention during hallucination) explains the `lo`-orientation js_radius signal as an aggregate-resolution shadow. See [feedback/inter-head-prior-art-2026-05-15](../feedback/inter-head-prior-art-2026-05-15.md). |
| [2604.10697v1.pdf](../../raw/papers/external/2604.10697v1.pdf)                                                         | Attention Sinks as Internal Signals for Hallucination Detection (SinkProbe) | Binkowski, Adamczewski, Kajdanowicz (Wrocław), 14 Apr 2026                                                | **Sink-dominance unifying frame for attention-based detectors.** Sink score $s_i^{l,h}=(1/(T-i))\sum_u A_{u,i}^{l,h}$, top-$k$ + logistic-regression probe; refinement is large-$\|V\|$ sinks. Unifies LLMCheck / Lookback Lens / TOHA / AttnEigvals / LapEigval. Makes the `js_radius_no_bos_*` column the load-bearing verdict gate for the inter-head diagnostic. 4 LLMs × 7 datasets, 23/28 SOTA. See [feedback/inter-head-prior-art-2026-05-15](../feedback/inter-head-prior-art-2026-05-15.md). |
| [chen-2025-persona-vectors.pdf](../../raw/papers/external/chen-2025-persona-vectors.pdf)                               | Persona Vectors: Monitoring and Controlling Character Traits in Language Models | Chen, Arditi, Sleight, Evans, Lindsey (Anthropic Fellows / UT Austin / Constellation / Truthful AI / UC Berkeley / Anthropic), arXiv 2507.21509, Sep 2025 | **Direct prior art for the empathy-geometry leg (candidate #11).** Supervised diff-of-means **sycophancy / hallucination / evil** directions on **Qwen2.5-7B + Llama-3.1-8B** (our twins + strangers rungs); projection at the final prompt token monitors trait expression pre-generation (r=0.75–0.83), `h←h±α·v` steers it. Both a **tool** (extractable empathy/authenticity/defensiveness vectors; a T4 baseline; a co-label; directed-steering causal probe) and a **priority problem** (position-along-a-trait-axis vs our geometry-of-commitment; the HARP↔v3 supervised-vs-unsupervised relationship again). Their own caveat — weak "when controlling for prompt type" / subtle in-deployment shifts — is exactly our authentic-vs-performative regime. Full assessment: [empathy-geometry/prior-art-persona-vectors](../empathy-geometry/prior-art-persona-vectors.md). |

## Ingestion Notes

### Kalai et al. 2025 — Why Language Models Hallucinate
**Core thesis:** Hallucinations are statistically inevitable, not bugs. Reduces generation to Is-It-Valid (IIV) binary classification: `err ≥ 2 · err_iiv - |V|/|E| - δ`. Base models must err on singleton facts (Good-Turing argument). Post-training makes it *worse* because binary evaluations reward confident guessing over IDK.

**Key results:**
- Arbitrary-fact lower bound (Theorem 2): `err ≥ sr - 2/min_c|E_c| - (35+6ln N)/√N - δ` where `sr` = singleton rate.
- Poor-model bound (Theorem 3): `err ≥ 2(1 - 1/C) · opt(G)` for C-choice settings.
- Calibration: base models are well-calibrated (δ small); RLHF/PPO breaks calibration (Fig. 2 shows ECE going from 0.007 → 0.074).
- Evaluations reinforce hallucination: binary scoring rewards guessing over abstention.

**v3 relevance — HIGH.** This is the *why* behind what PRI *detects*. Kalai shows hallucination is inevitable at the output level; PRI shows it's detectable at the representation level *before* output. The two are complementary: Kalai gives the statistical impossibility result, PRI gives the detection mechanism. Key citation for v3 intro/motivation. Also: the calibration result (RLHF decalibrates) may explain why PRI's S_t component (token surprise) weakens after RLHF — the base model's probability estimates lose their information content.

### Wastl et al. 2025 — Token-Level Self-Consistency
**Method:** Generate k alternative responses, align tokens via SimAlign, compute per-token median similarity score → threshold for hallucination span detection. Two modes: self-consistency (same model, k=5) and GPT-consistency (cross-model with GPT-4o-mini, k=20).

**Key results:**
- Best avg IoU: 51.7% (two-step prompt), 46.9% (GPT-consistency) across 10 languages.
- Self-consistency works better for large models (>8B); GPT-consistency better for small (<8B).
- Token-level labels outperform word-level.

**v3 relevance — MEDIUM.** Closest methodological analog to PRI's per-token scoring. Key differences: (1) they require multiple generations (PRI is single-pass), (2) they're black-box (PRI uses internals), (3) they detect span-level hallucination in QA (PRI detects commitment-level contradiction). Could serve as a baseline comparison in the v3 paper — "consistency-based methods require O(k) forward passes; PRI requires O(1)."

### Farquhar et al. 2024 — Semantic Entropy (Nature)
**Core idea:** Cluster sampled generations by bidirectional entailment into semantic equivalence classes, then compute entropy over *meanings* not *strings*. Low semantic entropy = confident and consistent = probably factual. High = confabulation.

**Key results:**
- AUROC on confabulation detection: GPT-4 0.877 (short) to ~0.79 (sentence-length); LLaMA-2 Chat 7B 0.782; Falcon 40B 0.657.
- Beats naive entropy, P(True), and embedding regression baselines across TriviaQA, SQuAD, BioASQ, NQ-Open.
- Works on paragraph-length biographies (FactualBio dataset, 21 individuals).
- Discrete variant (no output probabilities needed) also works, enabling use on closed-API models.

**v3 relevance — HIGH.** Primary external comparator. Semantic entropy requires ~10 forward passes per question; PRI requires 1. Semantic entropy is question-level; PRI is token-level. Both exploit the insight that "the model knows when it's wrong" — semantic entropy via output distribution, PRI via representation-space geometry. If PRI achieves comparable AUROC at 1/10 the compute, that's the headline result. Also: their discrete variant's success on closed models highlights that PRI's advantage is specifically over *open-weight* models where internals are accessible.

### Agrawal et al. 2024 — Do LMs Know When They're Hallucinating References?
**Core idea:** LMs can self-detect hallucinated references via direct queries ("Does reference X exist?") and indirect queries ("Who are the authors of X?"). The indirect method (IQ) checks consistency of generated metadata.

**Key results:**
- Hallucination rates: GPT-4 46.8%, ChatGPT 59.6%, GPT-3 73.6%, Llama-2-70B 66.2%.
- IQ+DQ ensemble AUC: GPT-4 0.927, ChatGPT 0.792, Llama-2-70B 0.792.
- Qualitative finding: LMs often produce "title mashups" (combinations of real papers) and generate plausible but non-existent authors.

**v3 relevance — MEDIUM.** Supports the foundational premise that LMs have internal representations of groundedness that differ from their outputs. Their approach is behavioral (probe via questions); PRI is mechanistic (probe via hidden states). Worth citing in v3 intro: "Prior work has shown models 'know' when they hallucinate behaviorally [Agrawal et al.]; PRI shows this knowledge is geometrically encoded in the representation space."

### Friston et al. 2017 — Active Inference: A Process Theory
**Core idea:** All neuronal processing = gradient descent on variational free energy. Derives from first principles: repetition suppression, mismatch negativity, violation responses, place-cell activity, theta sequences, dopamine transfer. The free energy functional serves as a Lyapunov function for neural dynamics.

**Key constructs:** Generative model as POMDP; belief updating via Bayesian smoothing (past + future states); policies as sequences of actions evaluated by expected free energy `G(π) = Σ_τ G(π,τ)`; precision `γ = 1/β` encoded by dopamine.

**v3 relevance — LOW (theoretical backdrop).** The SUP equation (`∆µ·∆σ ≥ ℏ_s`) is structurally analogous to the precision-flexibility tradeoff in active inference. Friston's precision-weighting (how confidently the brain weights prediction errors) maps onto SUP's `∆µ` (representational precision). The "bounded imprecision" thesis — that zero imprecision kills semantic capability — is a SUP-specific restatement of active inference's claim that precision must be *estimated*, not maximized. Not citable in v3 directly, but useful theoretical context for the SUP discussion.

### Friston et al. 2016 — Active Inference and Learning
**Core idea:** Goal-directed vs habitual behavior both emerge from minimizing expected free energy. Epistemic (uncertainty-resolving) behavior is exploratory; pragmatic (reward-seeking) behavior is exploitative. The Bellman optimality principle falls out as a special case when ambiguity is absent.

**Key constructs:** Model-free (habitual) vs model-based (goal-directed) distinction recast as belief-free vs belief-based; context learning via retrospective state-transition inference; habit formation as policy consolidation under stable contingencies.

**v3 relevance — LOW (theoretical backdrop).** The epistemic-pragmatic distinction maps loosely onto PRI's control-contradiction distinction: control prompts allow "pragmatic" (exploitation of learned patterns) processing; contradictions force "epistemic" (uncertainty-driven) processing that manifests as null-space discharge. Framing connection only — not directly citable.

### Friston et al. 2015 — Active Inference and Epistemic Value
**Core idea:** Decomposes expected free energy into extrinsic value (utility/reward) and epistemic value (information gain / uncertainty reduction). Agents that minimize expected free energy naturally resolve the exploration-exploitation dilemma: explore until epistemic value is exhausted, then exploit.

**Key constructs:** Epistemic value = expected information gain = KL divergence between posterior predictive and prior; precision as confidence in policies (softmax temperature → Bayes-optimal); simulations of foraging, conditioning, dopamine transfer.

**v3 relevance — LOW (theoretical backdrop).** The precision construct (γ = 1/β) is the closest Fristonian analog to SUP's ℏ_s — both quantify how tightly the system's beliefs are held. The decomposition of free energy into pragmatic + epistemic components resonates with PRI's decomposition of the signal into surprise (S_t, pragmatic — how unexpected is this token?) and rupture (d_F, epistemic — how much does the representation shift?). Conceptual parallel only.

### Hu et al. 2025 — HARP: Hallucination Detection via Reasoning Subspace Projection
**Core idea:** Decompose the hidden-state space as `H = S_Semantic ⊕ S_Reasoning`. Identify the two subspaces via SVD of `W_unemb = UΣV^T`: `S_Semantic = span(v_1..v_k)` (directions the unembedding acts on), `S_Reasoning = span(v_{k+1}..v_d)` (directions in the null space of W_unemb). Project hidden states onto the reasoning subspace `proj_R(h) = V_R^T · h` and train a binary classifier `g_θ` via BCE to score hallucination per-token; aggregate as max over tokens.

**Key parameters / results:**
- Cutoff: `k = d × 95%` by singular-value energy (reasoning subspace ≈ 5% of hidden dim, e.g. ~150 dims for 3072-d models; best detection dim empirically ~256 dims, Fig 5b).
- AUROC (Table 1): Qwen-2.5-7B — NQ Open 84.0 / TruthfulQA 88.1 / TriviaQA **92.8** / TyDiQA 88.4. Llama-3.1-8B — 89.4 / 88.5 / 92.9 / 86.6. Beats Semantic Entropy, EigenScore, HaloScope, Perplexity, LN-Entropy, Lexical Similarity by 7–17 pts on headline tasks.
- Ablation (Table 3): removing projection or using random basis both collapse AUROC by 15–25 pts — projection onto the *specific* reasoning basis is load-bearing, not "any low-dim projection."
- Causal probe (Appendix E, Reasoning Patch): patching reasoning components from correct-trajectory hidden states into hallucinating trajectories can rectify them while preserving semantic coherence — strong evidence the subspace is functional, not epiphenomenal.
- Cross-dataset generalization is strong (Fig 7) — TriviaQA-trained detector scores 91.7/91.9/92.9/91.8 on all four test sets (Qwen), suggesting the subspace is stable across distributions.

**v3 relevance — HIGHEST.** This is the single closest prior method to v3. The geometric object is *identical* to our null space at r corresponding to their 95%-energy k. Key differences, all load-bearing for novelty:

| Axis | HARP | Furnace v3 |
|---|---|---|
| SVD weighting | raw `W_unemb` (static) | `sqrt(p_t) · W_u` (context-dependent Fisher-pullback) |
| Semantic cutoff | k ≈ 0.95 d (reasoning dim ≈ 5% d) | r = 32 (informed dim ≈ 1% d) — much sharper support-restriction |
| Feature | projection vector of raw `h` | scalar `null_ratio = ‖proj_null Δh‖ / ‖Δh‖` of commitment *change* |
| Training | supervised classifier `g_θ` | unsupervised, direct metric |
| Timing | max over all generated tokens | commitment step 1 only, outcome-independent |
| Models | Qwen-2.5-7B, Llama-3.1-8B | +Mistral-7B |
| Task | QA hallucination (TriviaQA, NQ, TruthfulQA, TyDiQA) | synthetic 2×2 contradiction puzzles |
| Multi-pass | single forward | single forward (both 1-pass) |

**Implications for v3:**
- **Novelty narrows but survives.** We are not first to note `W_unemb` SVD separates "semantic" from "reasoning"; we *are* first (in this line) to weight by `p_t`, measure on Δh, localize at commitment, and score without training a classifier.
- **Must add a raw-W_u baseline** to the v3 main run (see `pri_v3_null_raw` in pri-v3-plan.md) so the Fisher-weighting contribution is directly measurable vs the HARP-style static subspace.
- **Should reproduce Reasoning Patch** (Appendix E) as a causal probe of the null-subspace's functional role on our 2×2 stimuli.
- **Cutoff mismatch needs articulation.** HARP's reasoning subspace ≈ 5% of dims; ours ≈ 99%. Framing: Fisher weighting concentrates semantic support onto the actually-considered tokens at step t, collapsing the "informed" subspace to a much smaller context-specific set. Same geometric object family, different metric.
- **Their Qwen headline (0.928 TriviaQA)** is the AUROC bar to understand. Our v2 Qwen is 0.786 on 2×2 puzzles — different task, not directly comparable, but reviewer-relevant.

### Anonymous ICLR 2026 — RAUQ: Recurrent Attention-based Uncertainty Quantification
**Core idea:** A tiny subset of "uncertainty-aware" attention heads concentrate on the immediately preceding token during correct generation; their attention to $i-1$ **drops sharply** during hallucinated tokens. Per-layer head-selection ($h_l = \arg\max_h$ mean $a^{l,h}_{i,i-1}$) + recurrent confidence propagation ($c_l(y_i)$ as a weighted product of token prob, selected-head attention, and previous confidence) + max-over-layer aggregation.

**Key parameters / results:**
- Llama 3.1 8B, $\alpha = 0.2$, layers 10–22 (first-third to second-third of the model).
- Selected-head signal magnitude **11.7%** (correct vs incorrect mean attention to $i-1$); averaged-over-heads **3.0%** — selection is what makes the signal usable.
- 4 LLMs × 12 tasks (QA, summarization, MT) × 15 baselines; SOTA across the board; <1% latency overhead; unsupervised, no task-specific tuning.
- Attention map (Figure 1, Llama 3.1 8B layer 29) shows head 25 with consistently high preceding-token attention except at the hallucinated token *falcon*.

**v3 relevance — MEDIUM (sealed claim).** Doesn't intersect residual-stream null-ratio. The v3 sealed object is $\Delta h$ projected against $W_u$, not attention $A^{l,h}$.

**Inter-head diagnostic relevance — HIGHEST.** Mechanism explains the `lo`-orientation cross-head JS-radius result: when the few preceding-token heads abandon $i-1$, cross-head disagreement *drops*, giving the `lo` signature. So our aggregate signal is best read as a lower-resolution shadow of RAUQ's per-head signal at gen_step=1. See [feedback/inter-head-prior-art-2026-05-15](../feedback/inter-head-prior-art-2026-05-15.md) §I1.

### Binkowski et al. 2026 — SinkProbe (Attention Sinks as Internal Signals)
**Core idea:** Hallucinations are entangled with **attention sinks** — tokens that accumulate disproportionate attention mass during generation, indicating transition from "distributed, input-grounded" to "compressed, prior-dominated" computation. Sink score per (layer, head, token): $s_i^{l,h} = (1/(T-i)) \sum_{u=i}^T A_{u,i}^{l,h}$. Top-$k$ sinks per head, concatenate across $L \cdot H$ heads, logistic-regression probe. Critical refinement: probe preferentially relies on sinks with large value-vector norms $\|V_i^{l,h}\|$ — sinks alone don't explain the signal, computationally-active sinks do.

**Key parameters / results:**
- 4 LLMs (Llama 3.2-3B, Phi-3.5 4B, Llama 3.1-8B, Mistral-Nemo 12B) × 7 datasets (GSM8K, HaluEvalQA, NQ-Open, SQuADv2, TriviaQA, TruthfulQA, UMWP).
- SOTA in **23 of 28** (model × dataset) pairs (Table 1) vs AttentionScore, AttnLogDet, AttnEigvals, LapEigvals, LookbackLens, MTopDiv baselines.
- $\ell_1$-regularized analysis: probe retains 1–4% of all coefficients — small subset of (layer, head, $k$) cells carries the signal.
- Norm-difference and layer-importance peak together in middle layers (Llama 3.2-3B, Fig. 2).
- Unifying claim: existing detectors (LLMCheck, Lookback Lens, TOHA, AttnEigvals, LapEigval) reduce to transformations of sink behavior. Concrete identity $l_{ii}^{l,h} = s_i^{l,h} - a_{ii}^{l,h}$ rewrites Laplacian-eigenvalue features as sink-score-minus-self-attention.

**v3 relevance — LOW (sealed claim).** Operates on attention $A^{l,h}$, not residual-stream $\Delta h$. The v3 main result is geometrically separate.

**Inter-head diagnostic relevance — HIGHEST.** Makes the SinkProbe-controlled column (`js_radius_no_bos_*` in our hardened script) the **load-bearing verdict gate**. Any AUROC on `js_radius_*` that doesn't survive the no-BOS control is uninterpretable as "head disagreement" — it's almost certainly reading sink dominance. 3 of our 9 panel models (Llama 3.2-3B, Phi-3.5-mini, Mistral-Nemo) overlap their evaluation, so side-by-side reading at rollup is possible modulo dataset and quantization. See [feedback/inter-head-prior-art-2026-05-15](../feedback/inter-head-prior-art-2026-05-15.md) §I2.

### Chen et al. 2025 — Persona Vectors (Anthropic)
**Core idea:** Automated pipeline extracts a linear **persona vector** per trait from a natural-language description. A frontier LLM writes 5 contrastive system-prompt pairs (elicit vs suppress) + 40 questions + a 0–100 judge rubric; the vector is the **difference in mean residual-stream activations over response tokens** between trait-expressing and non-expressing generations, at the most steering-effective layer (diff-of-means, refusal-direction family). Focus traits: **evil, sycophancy, hallucination** (+ optimism, humor). Models: **Qwen2.5-7B-Instruct, Llama-3.1-8B-Instruct.** Code public.

**Uses demonstrated:** (1) monitor — project the final-prompt-token activation onto the vector to predict the subsequent response's trait score (r=0.75–0.83); (2) control — steer `h_ℓ ← h_ℓ ± α·v_ℓ` (add induces, subtract suppresses; high α costs MMLU); (3) predict finetuning drift — activation "finetuning shift" projected on the vector correlates r=0.76–0.97 with post-FT trait; (4) flag training data — dataset/sample "projection difference" separates trait-inducing data pre-FT, validated on LMSYS-Chat-1M. Key caveat (their words): correlations "arise primarily from distinguishing between different prompt types," weaker "when controlling for prompt type" / for subtle in-deployment shifts.

**v3 / ACE / RPV relevance — LOW-MEDIUM.** Different object from the sealed lines: a supervised trait *direction* (position), not commitment curvature/rupture (shape). Adjacent to candidate #6 (their `h±α·v` steering is the directed cousin of v_top steering) and to the RPV/ACE panel only as a would-be baseline.

**Empathy-geometry (candidate #11) relevance — HIGHEST.** This is the leg's primary prior art. Both a tool and a positioning problem; the differentiating hypothesis is **iso-projection / hetero-geometric** (authentic vs performative sit at the same sycophancy projection but differ in commitment geometry). Consequences: a **T4 persona-projection baseline** the panel must beat, a mechanistic **authenticity co-label**, a **directed-steering causal probe** (sharper than isotropic noise), and concrete instruments for the **temporal** (turn-indexed projection = attractor deepening) and **dyadic coupling** axes. Same supervised-vs-unsupervised shape as HARP↔v3. Full assessment + build-plan changes: [empathy-geometry/prior-art-persona-vectors](../empathy-geometry/prior-art-persona-vectors.md).

## Suggested Seeding (not yet ingested)
- Vaswani et al. — Attention Is All You Need (2017)
- Shumailov et al. — AI models collapse when trained on recursively generated data (2024)
- Amari — Natural gradient works efficiently in learning (1998) — foundation for Fisher-information geometry
- Martens — New insights and perspectives on the natural gradient method (2020)
- Alain & Bengio — Understanding intermediate layers using linear classifier probes (2016)
- Zou et al. — Representation Engineering: A Top-Down Approach to AI Transparency (2023)
- Burns et al. — Discovering Latent Knowledge in Language Models Without Supervision (CCS, 2022)
- Azaria & Mitchell — The Internal State of an LLM Knows When It's Lying (2023)

## Filing convention
- Filename: `author-year-short-title.{pdf,md}` (e.g. `vaswani-2017-attention.pdf`).
- On drop-in: ingest → summarize → update relevant wiki pages (especially `claims.md` or `overview.md` if it changes framing) → link here → append to `log.md`.
- PDFs are fine — no need to convert unless the paper is scanned images.
