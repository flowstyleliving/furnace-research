# Attention Commitment Estimation for Pre-Generation Belief Readout

**Michael S.R. Kitti** · `msrkittty@proton.me`

_Working draft, 2026-05-30. Status: `[DRAFT]` — full prose end-to-end through all 7 sections + 6 appendices + references; numbers locked from the sealed verdict ([[results/v4-sealed-2026-05-26]]); figures + tables pre-built at `PRI_at_commitment/paper/v4/figures/out/`. Pre-registration: `PRI_V4_PRE_REGISTRATION_PLAN.md` (repo root, frozen 2026-05-26). Remaining before submission: title pick, venue choice + page-length cut, intro hook tightening, related-work bibliography polish, final consistency sweep. (.tex conversion is **done** — see [[paper/ace-draft.tex]].)_

_Companion scaffold + figure inventory + open decisions: [[paper/ace-scaffold]]. Method name **ACE = Attention Commitment Estimator** locked 2026-05-30 (post-seal, presentation-only — no sealed parameter affected)._

---

## Abstract

Detecting when a language model commits to an incorrect answer typically requires either multiple forward passes (semantic entropy, self-consistency) or post-hoc representational analysis at the first generated token. We introduce **ACE** (Attention Commitment Estimator), a single-pass calibrator that reads YES/NO commitment from a 21-cell panel of attention-channel features at the prefill-last-position ($t=0$), before any generated token. ACE is sealed pre-registered: the panel (3 block depths × 7 metrics), datasets (ANLI R1 $n{=}200$, TriviaQA paired $n{=}100$), out-of-bag bootstrap ($n_{\text{boot}}{=}1000$), and two confirmatory gates ($E_{A1}$ discriminability $\geq 7/9$ models; $E_{A2}$ cell-transfer tiered at $\leq 2$ / $3$–$4$ / $\geq 5$ exact matches) were locked before any sealed data was generated. Across 9 open-weight 4-bit-quantized architectures, $E_{A1}$ **passes at 7/9** — Mistral-Nemo reaches OOB AUROC 0.887 [0.816, 0.946], and TriviaQA discriminability is uniformly stronger (8/9; Mistral-7B 0.989). $E_{A2}$ resolves at **3/9 exact (metric, block, sign) transfer** (Mistral-7B, Mistral-Nemo, Qwen2.5-7B), triggering the pre-registered partial-transfer reframe: ACE generalizes as a *method*, not as a fixed cell — per-(model, exact deployment distribution) calibration is empirically binding for 6/9 models. On the 4 OOB-trustworthy models, ACE wins 2/4 head-to-head against RAUQ and SinkProbe, which themselves disagree in direction on two models — evidence that the attention-channel baselines capture distinct phenomena. The sealed pre-registration absorbed a mid-flight $t{=}0$ locus re-grounding (prompted by chain-of-thought abstention in 58–70% of free-generation samples on a reasoning-tuned model) without altering any sealed parameter; verdict integrity is preserved across the correction.

---

## 1. Introduction

An LLM's commitment to a YES/NO answer is often legible *before* it speaks the first token. The attention pattern at the last prefix position — at $t=0$, before any generation — already encodes whether the model has resolved the question to YES or NO. ACE (Attention Commitment Estimator) estimates that commitment from a 21-cell panel of attention-channel features.

Hallucination and over-confidence detection has typically watched what the model *says* — semantic entropy across sampled completions (Farquhar et al. 2024), self-consistency between independent responses (Wastl et al. 2025). Both require multiple forward passes per query. PRI v3 (Kitti 2026b) watched the *residual stream geometry* at the first generated token. ACE watches a different surface: the *attention pattern* at the last prefix position, before any generation. Single forward pass.

This paper reports a sealed pre-registered evaluation of ACE across 9 open-weight 4-bit-quantized architectures on (i) ANLI R1 ($n=200$, primary gate) and (ii) TriviaQA paired-prompt ($n=100$, cross-task transfer test). Two confirmatory gates: $E_{A1}$ requires $\geq 7/9$ models to achieve OOB $\text{CI}_{\text{lo}} > 0.50$ on at least one of 21 attention cells; $E_{A2}$ tests whether the winning cell transfers across ANLI $\to$ TriviaQA, with $\geq 5/9$ exact match triggering a "headline collapse" falsification. The 21-cell panel spans 3 block-depth prefixes × 7 metrics; pre-registration locks the panel, the dataset seeds, and the bootstrap ($n=1000$ OOB). A secondary baseline comparison ($E_{B1}$) puts ACE head-to-head with RAUQ and SinkProbe on the OOB-trustworthy subset.

**Findings.** $E_{A1}$ passes at 7/9 (failures: Llama-3.2-3B, Gemma-3-4B; both recover on TriviaQA). $E_{A2}$ resolves at 3/9 exact transfer (Mistral-7B, Mistral-Nemo, Qwen2.5-7B), triggering the pre-reg's $\geq 3/9$ "partial-transfer" reframe — not collapse. Block-prefix is stable in 6/9 even when metric and sign are not. TriviaQA OOB AUROCs are uniformly stronger than ANLI (8/9 pass; Mistral-7B 0.989, Mistral-Nemo 0.980). On the 4 OOB-trustworthy models in the baseline comparison ($E_{B1}$, secondary), ACE wins 2/4 (Phi-3.5-mini 0.774, Qwen2.5-7B 0.818), loses 1 to RAUQ, and ties SinkProbe within $\Delta=0.003$. RAUQ and SinkProbe disagree in direction on Mistral-Nemo and Qwen3-8B — they capture different phenomena.

**Roadmap.** Section 2 places ACE among attention-channel uncertainty methods and pre-registration practice; Section 3 specifies ACE; Section 4 details the sealed pre-reg; Section 5 reports the verdicts; Section 6 discusses partial-transfer and per-(model, task) calibration; Section 7 concludes.

## 2. Related Work

**Attention-channel uncertainty.** RAUQ (citation pending) computes per-layer recurrent attention uncertainty selected via head-greedy maximization on $\arg\max_h \overline{a_{i,i-1}}$, with confidence aggregated through recurrence and maxed over layers. SinkProbe (citation pending) decomposes attention sink-token concentration into per-(layer, head, position) features. StreamingLLM (Xiao et al. 2024) and follow-ups motivate the sink-token primitive on which SinkProbe is built. ACE uses three reductions (`js`, `bos_mass`, `v_norm_lastq_weighted`) across three block depths (`final`, `mid`, `last_minus_1`) — a wider panel than either baseline, and chosen pre-registration to span attention-divergence, sink-mass, and value-weighted formulations.

**Single-pass hallucination detection.** Semantic entropy (Farquhar et al. 2024) clusters $\sim 10$ sampled generations by bidirectional entailment, reporting AUROC $\approx 0.78$–$0.88$ on factual confabulation but at $10\times$ inference cost. Token-level self-consistency (Wastl et al. 2025) requires sampled completions. ACE is single-pass.

**Belief readout / internal-state vs output.** Sofroniew et al. (2026) demonstrate that internal-state representations in instruction-tuned LLMs can differ systematically from outputs — emotion concepts encoded latently that the model does not explicitly verbalize. ACE is a behaviorally concrete instance of the same internal-vs-output gap at the prefill stage.

**Information geometry and PRI v3.** Our prior work (Kitti 2026b) introduced PRI v3, a Fisher-pullback formulation that measures rupture in the residual stream at the first generated token (gen_step=1). ACE measures the attention channel at the prior step ($t=0$, the prefill-last-position). The two are complementary observables on the same commitment moment.

**Pre-registration in ML.** Nosek et al. (2018) and Pineau et al. (2021) argue for sealed pre-registration to defend against $p$-hacking in benchmark-driven research. PRI v3 used this pattern; ACE inherits it with a tighter machinery (nested-OOB bootstrap for selection-bias-corrected CIs, schema v1.2). The sealed pre-registration document is snapshotted as Appendix A.

## 3. ACE Method

### 3.1 Instrument

Given an input prompt $P$ ending in a YES/NO elicitation ("Answer:"), ACE runs a single forward pass and captures the attention weights at the final prefix token position. We refer to this as the $t=0$ position — the prefill-last-position, *before* any generation step. The motivation: by the time the model has finished processing the prompt and is ready to emit the first generated token, its commitment to YES or NO is already encoded in how attention is distributed across the input. Our hypothesis is that this commitment is recoverable as a scalar feature of the attention pattern.

### 3.2 The 21-cell panel

ACE computes 21 scalar features per sample, organized as $\{$`final`, `mid`, `last_minus_1`$\} \times \{$`js`, `js_kv_groups`, `js_no_bos`, `bos_mass`, `v_norm_bos`, `v_norm_max`, `v_norm_lastq_weighted`$\}$, where the prefix denotes the transformer block depth at which the attention is read (`final` is the last transformer block; `mid` is the block at the geometric midpoint; `last_minus_1` is the second-to-last block). The seven metrics span three reductions of the attention pattern at the prefill-last-position.

For notation, let $A^{(\ell,h)} \in \mathbb{R}^T$ denote the attention distribution at layer $\ell$, head $h$, computed at the last query position over $T$ prefix tokens. Let $H$ be the number of query heads, $H_{KV}$ the number of key-value heads (with $H / H_{KV}$ the GQA repeat factor), and $\|V^{(\ell,h)}_i\|_2$ the L2 norm of the value vector at layer $\ell$, KV head $h$, position $i$.

**JS-radius family.** All three measure cross-head disagreement on the attention pattern, with three normalizations.

$$
\mathrm{js}^{(\ell)} \;=\; \frac{1}{H} \sum_{h=1}^{H} \mathrm{JS}\!\left( A^{(\ell,h)} \,\Big\Vert\, \bar{A}^{(\ell)} \right), \qquad \bar{A}^{(\ell)} \;=\; \frac{1}{H} \sum_{h=1}^{H} A^{(\ell,h)}
$$

where $\mathrm{JS}(P\,\Vert\,Q) = \tfrac{1}{2}\mathrm{KL}(P\,\Vert\,M) + \tfrac{1}{2}\mathrm{KL}(Q\,\Vert\,M)$ with $M = \tfrac{1}{2}(P+Q)$ — Lin's information radius, bounded in $[0, \log 2]$.

$\mathrm{js\_kv\_groups}^{(\ell)}$ collapses Q heads that share a KV group by mean-pooling before computing JS-radius (debiases against GQA-induced artificial convergence): for KV-group index $k$ with $r = H/H_{KV}$ Q heads per group, $\tilde{A}^{(\ell,k)} = \tfrac{1}{r} \sum_{j=1}^{r} A^{(\ell, (k-1)r+j)}$, then JS-radius is computed over $\{\tilde{A}^{(\ell,k)}\}_{k=1}^{H_{KV}}$.

$\mathrm{js\_no\_bos}^{(\ell)}$ drops position $0$ (the BOS sink) from each head's distribution, re-normalizes to sum to one, and computes JS-radius over the trimmed $T{-}1$-dim distributions.

**Sink-mass.** The fraction of attention mass on the BOS token, averaged across heads:

$$
\mathrm{bos\_mass}^{(\ell)} \;=\; \frac{1}{H} \sum_{h=1}^{H} A^{(\ell,h)}_0
$$

**Value-norm reductions.** Three single-scalar SinkProbe-inspired metrics weight the value-vector L2 norms.

$$
\mathrm{v\_norm\_bos}^{(\ell)} \;=\; \frac{1}{H_{KV}} \sum_{h=1}^{H_{KV}} \|V^{(\ell,h)}_0\|_2, \qquad
\mathrm{v\_norm\_max}^{(\ell)} \;=\; \frac{1}{H_{KV}} \sum_{h=1}^{H_{KV}} \max_{i} \|V^{(\ell,h)}_i\|_2
$$

$$
\mathrm{v\_norm\_lastq\_weighted}^{(\ell)} \;=\; \frac{1}{H} \sum_{h=1}^{H} \sum_{i=1}^{T} A^{(\ell,h)}_i \cdot \|V^{(\ell, \pi(h))}_i\|_2
$$

where $\pi(h)$ maps query head $h$ to its KV group. The last metric is the closest single-scalar analog of SinkProbe's "sinks with large value-vector norms dominate the attention output" finding (Binkowski et al. 2026).

Each (layer, metric) pair is a candidate cell; the calibrator selects the winning cell from the 21-cell panel on the calibration set without back-looking at test labels.

### 3.3 Calibration

For each (model, dataset) pair, ACE runs an OOB bootstrap winner-cell selection across the 21 cells. The winning cell, sign, and threshold are locked from the calibration-set OOB direction; no post-hoc sign-fitting is performed on test labels. The bootstrap uses $n=1000$ resamples; schema v1.2 inherits v1.1's nested-OOB protocol for selection-bias-corrected confidence intervals (Kitti 2026b, Appendix B). The output is a `CalibrationProfile` JSON containing the winner cell, OOB median AUROC, 95% CI, winner stability, and any deployability warnings.

### 3.4 What ACE is NOT

ACE is not the PRI v3 Fisher-pullback metric — that measures residual-stream geometry at $\text{gen\_step}=1$, *after* the first token has been generated. ACE is not a trained probe (no logistic head fit on labels — sign is locked from calibration-direction only). ACE is not multi-pass (single forward).

## 4. Sealed Experimental Setup

### 4.1 Pre-registration

The sealed pre-registration document (`PRI_V4_PRE_REGISTRATION_PLAN.md`, repo root) was frozen on 2026-05-26 before any sealed data was generated. It locks: the 9-model panel, the 21-cell attention panel, the analysis plane (gen_step=1, final layer, $t=0$ instrument), the bootstrap ($n=1000$, OOB), the datasets (ANLI R1 $n=200$ + TriviaQA $n=100$, seed 20260526), and the gate thresholds ($E_{A1} \geq 7/9$; $E_{A2}$ tiered at $\leq 2$ / $3$–$4$ / $\geq 5$ exact transfer). A post-seal naming amendment on 2026-05-30 locks the method name **ACE** as presentation-only; no sealed parameter is altered.

### 4.2 Models

The panel is 9 open-weight architectures, all 4-bit MLX quantized: Llama-3.2-3B-Instruct, Mistral-7B-Instruct-v0.3, Mistral-Nemo-Instruct-2407, Phi-3.5-mini-instruct, Phi-4-mini-instruct, Qwen2.5-7B-Instruct, Qwen3-1.7B, Qwen3-8B, and Gemma-3-4B-it. Phi-3.5-mini was INCLUDED-with-caveat per the pre-registration gate decision (denominator = 9 regardless of whether its CI clears 0.50). The Phi-3.5-mini low-decidedness flag (Step-0 audit, 2026-05-25) carries forward as a descriptive caveat, not as a falsification trigger.

### 4.3 Datasets and prompts

**ANLI R1** is the primary gate dataset. We sample $n=200$ examples from the public ANLI R1 corpus at seed 20260526, balanced 50/50 across the *entailment* and *contradiction* labels (the *neutral* class is excluded — the gate targets binary commitment). Each example is rendered as a forced-choice YES/NO prompt of the form *"Premise: $\langle p \rangle$ Hypothesis: $\langle h \rangle$ Does the premise entail the hypothesis? Answer:"*, with the model's first generated token taken as the committed answer (YES/NO; case-insensitive after stripping leading whitespace). Label-to-target mapping is *entailment* $\to$ YES, *contradiction* $\to$ NO.

**TriviaQA paired-prompt** is the cross-task transfer test. We draw $n=100$ unique question-answer pairs $(q, a)$ from TriviaQA at seed 20260526. Each pair is expanded into two prompts: a *correct* prompt presenting $(q, a)$ as ground truth, and a *contradicted* prompt presenting $(q, a')$ where $a'$ is a plausibly-wrong distractor (length-matched, type-matched answer drawn from a held-out pool — full procedure in Appendix D). Both prompts elicit the model with *"...Is the proposed answer correct? Answer:"*. The label is which version received the contradicted answer.

Prompt formatting uses each model's native chat template (`apply_chat_template`) to avoid the format-completion artifacts documented in our prior work (Kitti 2026c, §3.4). All prompts elicit a forced YES/NO; behavioral preflight on $n=20$ control samples per model verifies $\geq 80\%$ format compliance before sealed-run inclusion. Parser details (3-tier `check_answer` regex with `gate-max-tokens=12`) are deferred to Appendix D.

The two datasets together provide the cross-domain transfer probe: ANLI R1 is synthetic adversarial NLI (the contradiction is structural, between premise and hypothesis); TriviaQA paired is factual disagreement (the contradiction is referential, between answer and ground truth). If a single attention cell transferred across both, it would be a strong universal-cell candidate; the $E_{A2}$ result reported in §5.3 says it does not — for 6/9 models.

### 4.4 Baselines

RAUQ is run at the same prefill stage as ACE, with per-layer head-select on $\arg\max_h \overline{a_{i,i-1}}$ and best-single-layer AUROC reported (rather than the native max-over-layers aggregate, which we found to sandbag the baseline by 0.30–0.49 on some models — see §5.4). SinkProbe is run as the $\|V\|$-weighted column-sum (`sink_top1_vw`), which dominated the simpler last-query approximation on 6/10 models in our prep sweep. Both baselines were run at gen_step=1 in the May 2026 prep sweep; the pre-registration's $E_{B1}$ clause designates a sealed $t=0$ baseline re-run as non-blocking future work (i.e., the secondary baseline comparison is reported at gen_step=1 with the caveat that an at-$t=0$ re-run remains to be done).

## 5. Results

### 5.1 $E_{A1}$ — discriminability on ANLI R1 (Fig. 1)

The primary gate $E_{A1}$ passes at 7/9 (Fig. 1; Table 2). Mistral-Nemo carries the highest OOB AUROC at 0.887 [0.816, 0.946] (winner stability 1.00). Qwen3-8B reaches 0.823 [0.738, 0.896]; Qwen2.5-7B and Mistral-7B both clear 0.78. The two failures are Llama-3.2-3B (OOB 0.597, CI$_\text{lo}$ 0.403 — clear miss) and Gemma-3-4B (OOB 0.656, CI$_\text{lo}$ 0.488 — borderline). Both failing models pass on TriviaQA (§5.2), indicating their attention channel carries commitment signal on factual disagreement even when it does not on synthetic adversarial NLI. The pre-reg gate threshold $\geq 7/9$ is cleared; neither falsifier triggers.

### 5.2 Cross-task generalization (Fig. 2)

On TriviaQA, 8/9 models cross the $\text{CI}_{\text{lo}} > 0.50$ bar (single failure: Qwen3-1.7B at 0.471 — borderline). Mistral-7B reaches OOB AUROC 0.989 [0.970, 1.000] and Mistral-Nemo 0.980 [0.929, 1.000]; the rest cluster between 0.74 and 0.94. Fig. 2 shows the ANLI→TriviaQA paired AUROCs per model: the dominant pattern is uniform improvement on TriviaQA. Llama-3.2-3B and Gemma-3-4B (ANLI failures) recover cleanly. The Qwen3-1.7B TriviaQA borderline failure is the inverse case — passes ANLI ($E_{A1}$ cleared), fails TriviaQA.

### 5.3 $E_{A2}$ — cell transfer (Fig. 3, Table 2)

The transfer test requires exact match on (metric_label, block_depth_prefix, sign) between each model's ANLI winner cell and its TriviaQA winner cell. Three models satisfy this: Mistral-7B (`last_minus_1_js_no_bos`, sign $-1$), Mistral-Nemo (`last_minus_1_bos_mass`, sign $-1$), and Qwen2.5-7B (`final_v_norm_lastq_weighted`, sign $+1$). This 3/9 outcome triggers the pre-registration's $\geq 3/9$ partial-transfer reframe clause: the headline shifts from "no universal cell" (the originally registered Candidate A framing) to "partial transfer exists; per-task recalibration remains necessary for 6/9 models." Critically, the $\geq 5/9$ collapse threshold is not triggered — the partial-transfer reframe is a pre-registered outcome, not a post-hoc rescue.

A descriptive companion observation: the block-depth prefix is stable across tasks in 6/9 models (Mistral-7B, Mistral-Nemo, Phi-3.5-mini, Phi-4-mini, Qwen2.5-7B, Qwen3-1.7B), even when the metric and sign change. Models appear to have a preferred attention depth band that persists across task domains; only the specific reduction varies.

### 5.4 Baselines (Table 3, secondary)

On the 4 OOB-trustworthy models (Phi-3.5-mini, Qwen2.5-7B, Llama-3.2-3B, Qwen3-8B — those where ACE's winner stability $\geq 0.70$ and OOB CI excludes 0.50), ACE wins 2/4 clean: Phi-3.5-mini (0.774 vs RAUQ 0.721, SinkProbe 0.618) and Qwen2.5-7B (0.818 vs RAUQ 0.634, SinkProbe 0.650). ACE loses 1 to RAUQ on Llama-3.2-3B (0.655 vs 0.678) and is overtaken by SinkProbe on Qwen3-8B by $\Delta=0.003$ (0.804 vs 0.807). The remaining 5 models have ACE flagged with deployability warnings and are reported without a head-to-head verdict.

A methodological observation worth preserving: RAUQ's native max-over-layers aggregate underperforms its own best-single-layer by 0.30–0.49 AUROC on models where per-layer attention directions disagree (most starkly on Llama-3.2-3B: 0.42 vs 0.68). Table 3 reports the best-single-layer to avoid sandbagging the baseline. Similarly, SinkProbe's $\|V\|$-weighted column-sum dominates its simpler last-query approximation on 6/10 models in our prep sweep — the column-sum form is the strong version of the SinkProbe family.

Baselines disagree in direction on two models: Mistral-Nemo (RAUQ runs "lo" — low uncertainty predicts contradiction — at AUROC 0.228, while SinkProbe runs "hi" at 0.867) and Qwen3-8B (RAUQ 0.425 "lo", SinkProbe 0.807 "hi"). The direction-disagreement is itself a finding: the two baselines are not measuring the same underlying phenomenon, even when both are sourced from attention.

### 5.5 Pre-registration summary (Table 1)

Table 1 summarizes the sealed pre-registration parameters and the verdict. All confirmatory thresholds are cleared without falsification trigger; the partial-transfer outcome is the pre-registered reframe path, not a post-hoc adjustment.

## 6. Discussion

### 6.1 What partial transfer means in deployment

The 3/9 cell-transfer outcome is the most consequential result for practitioners. It says: ACE *as a method* generalizes — every model in the panel has an attention cell that discriminates YES/NO commitment at $t=0$ — but ACE *as a fixed cell* does not. Deployment requires per-(model, exact deployment distribution) calibration: a labeled calibration set of $n \geq 200$ per task, the calibrator run end-to-end, the winning cell + sign + threshold cached as a `CalibrationProfile`. The cached profile is then deployable. This generalizes the same lesson from the 33-profile ANLI R1↔R2↔R3 sweep (Kitti 2026b, §4.5): cell transfer fails even across rounds of the same task family, and the cross-task test makes the constraint visible.

### 6.2 Architectural patterns in the 3 exact-transfer models

The 3 exact-transfer models are Mistral-7B, Mistral-Nemo, and Qwen2.5-7B. The Mistral family transfers at both sizes (7B and 12B Nemo); Qwen3 (1.7B and 8B) does not, despite shared family. We do not have a predictive architectural feature here. One speculative pattern worth flagging for future work: the 3 exact-transfer models all predate the reasoning-tuned wave (Qwen3 and Phi-4 are reasoning-instruction-tuned; Mistral v0.3, Nemo, and Qwen2.5 are not), raising the possibility that whatever attention regularity ACE keys on is disrupted by chain-of-thought-style training. We are underpowered to make this claim — three models is not a category.

### 6.3 Why TriviaQA is uniformly stronger

TriviaQA pairs are constructed with explicit injected wrong answers — the model is presented with "Q: ...? A: [wrong-answer]. Is this correct?" The presence of an explicit reference answer to disagree with may sharpen the commitment signal at $t=0$, compared to ANLI's three-way entailment/neutral/contradiction framing where the "wrong" answer is structurally implicit. This is speculative; a direct test would require an ANLI-style adversarial NLI dataset re-cast in TriviaQA's explicit-disagreement format.

### 6.4 Connection to PRI v3

PRI v3 (Kitti 2026b) measured Fisher-pullback rupture at $\text{gen\_step}=1$, in the residual stream. ACE measures attention-channel features at $t=0$, before generation. They are complementary observables on the same commitment moment. Both pass discriminability gates; both require per-model calibration. A pilot causal intervention on the v3 Fisher direction (the top right singular vector $v_\text{top}$ of $\sqrt{p_t} \cdot W_u$) — Section 5 of the scope memo — shows label-conditioned asymmetry: contradiction samples flip their committed YES/NO at $4\times$ the rate of entailment samples under $+v_\text{top}$ at $\alpha=50$ (40% vs 10%), despite contradictions having a larger mean logit gap. This is non-null pilot evidence that the v3 Fisher direction is causally load-bearing at the commit moment. Confound mitigation (logit-gap matching, orig\_answer balance) is required before this can be promoted from pilot to validated finding; we describe the matched-design plan in §6.7.

### 6.5 Limitations

Four-bit MLX quantization is uniform across the panel (comparable, but not faithful to fp32 deployment). The sealed dataset is single-seed; $n=200$ ANLI is the sample-size constraint, not the seed. Baselines were run at gen_step=1 in the May 2026 prep sweep; the at-$t=0$ baseline re-run is non-blocking future work per the $E_{B1}$ clause. The 21-cell panel was designed pre-registration to span the JS / sink-mass / value-norm families, but it does not exhaust the attention-channel feature space; richer panels (full per-head, $K \times V$ outer products, etc.) might surface stronger cells. Phi-3.5-mini's low-decidedness at $t=0$ (Step-0 audit, 2026-05-25) is a known tension carried forward as a flag.

### 6.6 Future work

(i) Sealed $t=0$ baseline re-run to convert Table 3's gen_step=1 caveat into an at-locus comparison; (ii) matched-design causal probe at $n=40+40$ with logit-gap-matched stratification and orig\_answer balance, sealed pre-registered, to convert the v3 $+v_\text{top}$ pilot from non-null to validated; (iii) an epistemic-distinguishability testbed comparing bluff-commits (committed answer ≠ internal belief, induced via role-play prompts) against honest-uncertain-commits — extending ACE's deployment surface from contradiction-detection to deception-detection, with Nash-equilibrium-derived bluff frequencies as a candidate oracle in solved games (Brown & Sandholm 2017, 2019).

### 6.7 Pre-registration governance

The sealed pre-registration was frozen on 2026-05-26. One post-seal annotation was added on 2026-05-30 to lock the method name ACE; this is presentation-only and modifies no sealed parameter. A more substantive mid-flight event was the 2026-05-17 STEP-0 belief-readout-locus re-grounding: the gen_step=1 attention numbers from the May 2026 prep sweep were re-anchored at $t=0$ logit-locus after we discovered that 5/10 panel models do not commit a YES/NO at gen_step=1 (Qwen2.5-7B abstains in 58–70% of free-generation samples, producing chain-of-thought preamble rather than an answer). The $t=0$ belief-readout panel re-grounded the premise without altering the sealed parameters or the gates. Verdict integrity survived the re-grounding because the pre-reg locked the *instrument* ($t=0$ first-token logit) rather than the elicitation protocol (free-generation), which had been previously confounded.

## 7. Conclusion

ACE is a single-pass attention-channel calibrator that discriminates YES/NO commitment at the prefill-last-position across 9 open architectures. The sealed pre-registration passes its primary gate (7/9 discriminate) and its transfer gate (3/9 exact, partial-transfer reframe). Per-(model, exact deployment distribution) calibration is empirically binding, not assumed. ACE's deployment surface is wherever a labeled calibration set is available; its method-level generalization is broad, but its cell-level generalization is not. Future work — at-$t=0$ baselines, matched-design causal probe, deception-detection extension — is staged behind submission.

---

## Acknowledgements

This work was carried out independently as part of the Furnace Research line. All experiments ran on a single Apple Mac mini (M4, 32 GB unified memory) using the MLX framework (Apple ML Research 2023) with 4-bit-quantized open-weight checkpoints from the mlx-community Hugging Face organization. Adversarial review of the calibrator and detector codebase was provided by an automated review pipeline (Codex / Greptile); the post-selection-bias finding that motivated the schema v1.2 nested out-of-bag bootstrap was surfaced by adversarial review in May 2026 and is gratefully acknowledged. Correspondence with the HARP authors (Hu et al. 2025) is gratefully noted. No external funding was received. The opinions expressed are the author's own.

## References

Agrawal, A., Suzgun, M., Mackey, L., & Kalai, A. T. (2024). Do Language Models Know When They're Hallucinating References? In *Findings of the Association for Computational Linguistics: EACL 2024*, pp. 912–928. arXiv:2305.18248.

Amari, S.-i. (2016). *Information Geometry and Its Applications*. Applied Mathematical Sciences Vol. 194. Springer. ISBN 978-4-431-55977-1.

Anonymous. (2026). Efficient Hallucination Detection for LLMs Using Uncertainty-Aware Attention Heads (RAUQ: Recurrent Attention-based Uncertainty Quantification). Submitted to the International Conference on Learning Representations (ICLR) 2026. OpenReview submission \#24110, double-blind review.

Apple ML Research. (2023–present). MLX: An array framework for Apple Silicon. GitHub: ml-explore/mlx. Companion library `mlx-lm` provides 4-bit-quantized open-weight model checkpoints used in this paper.

Binkowski, J., Adamczewski, K., & Kajdanowicz, T. (2026). Attention Sinks as Internal Signals for Hallucination Detection in Large Language Models (SinkProbe). arXiv:2604.10697, 14 April 2026.

Brown, N., & Sandholm, T. (2017). Superhuman AI for heads-up no-limit poker: Libratus beats top professionals. *Science*, 359(6374):418–424. DOI: 10.1126/science.aao1733.

Brown, N., & Sandholm, T. (2019). Superhuman AI for multiplayer poker. *Science*, 365(6456):885–890. DOI: 10.1126/science.aay2400.

Farquhar, S., Kossen, J., Kuhn, L., & Gal, Y. (2024). Detecting Hallucinations in Large Language Models Using Semantic Entropy. *Nature*, 630:625–630. DOI: 10.1038/s41586-024-07421-0.

Hu, J., Tu, X., Cheng, Z., Li, J., Wang, X., Chen, J., Zhou, Y., & Shan, Y. (2025). HARP: Hallucination Detection via Reasoning Subspace Projection. arXiv:2509.11536.

Kalai, A. T., Nachum, O., Vempala, S. S., & Zhang, E. (2025). Why Language Models Hallucinate. arXiv:2509.04664.

Kitti, M. S. R. (2026a). Predictive Rupture as a Signal for Hallucination Detection in Large Language Models. Furnace Research preprint, 22 January 2026.

Kitti, M. S. R. (2026b). Hallucinations Rupture at Commitment, Not at Encoding: Predictive Rupture Index Localizes Contradiction-Induced Failure to the First Generated Token. Furnace Research preprint, 17 March 2026.

Kitti, M. S. R. (2026c). Fisher-Pullback Predictive Rupture Index Detects Commitment-Time Strain Across Decoder Architectures. Furnace Research preprint, 9 April 2026.

Nosek, B. A., Ebersole, C. R., DeHaven, A. C., & Mellor, D. T. (2018). The preregistration revolution. *Proceedings of the National Academy of Sciences*, 115(11):2600–2606. DOI: 10.1073/pnas.1708274114.

Pineau, J., Vincent-Lamarre, P., Sinha, K., Larivière, V., Beygelzimer, A., d'Alché-Buc, F., Fox, E., & Larochelle, H. (2021). Improving Reproducibility in Machine Learning Research (a Report from the NeurIPS 2019 Reproducibility Program). *Journal of Machine Learning Research*, 22(164):1–20.

Sofroniew, N., Kauvar, I., Saunders, W., Chen, R., Henighan, T., Hydrie, S., Citro, C., Pearce, A., Tarng, J., Gurnee, W., Batson, J., Zimmerman, S., Rivoire, K., Fish, K., Olah, C., & Lindsey, J. (2026). Emotion Concepts and their Function in a Large Language Model. *Transformer Circuits Thread*, Anthropic, 2 April 2026.

Wastl, M., Vamvas, J., & Sennrich, R. (2025). UZH at SemEval-2025 Task 3: Token-Level Self-Consistency for Hallucination Detection. In *Proceedings of the 19th International Workshop on Semantic Evaluation (SemEval-2025)*, pp. 257–270, Vienna, Austria.

Xiao, G., Tian, Y., Chen, B., Han, S., & Lewis, M. (2024). Efficient Streaming Language Models with Attention Sinks. In *International Conference on Learning Representations (ICLR) 2024*. arXiv:2309.17453.

## Appendix A. Pre-registration document snapshot

The full sealed pre-registration text — including the gate decision for Phi-3.5-mini (INCLUDED, denominator = 9), the 21-cell panel specification, dataset hashes, and the no-post-hoc-re-specification clause — is reproduced verbatim from `PRI_V4_PRE_REGISTRATION_PLAN.md` (frozen 2026-05-26) and is available at the supplementary URL. The only post-seal annotation, dated 2026-05-30, locks the method name **ACE** as presentation-only and explicitly notes that no sealed parameter is affected.

## Appendix B. Per-cell candidate-panel AUROCs

For each of the 9 panel models × 2 datasets × 21 cells (378 entries), Appendix B reports the in-sample AUROC, OOB bootstrap median AUROC with 95% CI, winner-stability fraction, and direction-of-association sign. The full table is included as supplementary material (`appendix_b_panel_aurocs.csv`) and reproducible via the `paper/v4/figures/load_ace_profiles.py` loader against the 18 sealed profile JSONs at `experiments/v4-sealed/2026-05-26/profiles/`. We summarize the per-(model, dataset) winning cell in main-paper Table 2.

## Appendix C. ACE metric definitions, extended

Section 3.2 provides the formal equations. Appendix C extends them with implementation notes: (i) the $\varepsilon = 10^{-12}$ regularizer added to attention probabilities before each $\log$ to avoid $\log 0$; (ii) the row-renormalization performed after BOS-trimming in `js_no_bos`; (iii) the $H_{KV}$-to-$H$ value-norm expansion convention used in `v_norm_lastq_weighted` for grouped-query attention models. The corresponding reference implementations are in `pri_calibrator.py:_compute_attention_score` and `scripts/diagnose_inter_head_disagreement.py:_js_radius` (released open-source).

## Appendix D. Prompt formatting and dataset preprocessing

Each model's native chat template (HuggingFace `tokenizer.apply_chat_template`) is applied before the elicitation suffix; per-model template wrappers are catalogued in `pri_v2_io_plugins.py`. The behavioral preflight (Kitti 2026c, §3.4) runs 20 control samples per model with `--gate-max-tokens 12` and a 3-tier `check_answer` regex that handles (i) bare `YES`/`NO`; (ii) `Answer: YES`/`Answer: NO`; (iii) `[YES]`/`[NO]` formats. Models with $<80\%$ control accuracy under this parser are excluded from the sealed run (none in the current panel after the v3.1 parser-recovery patches). The TriviaQA wrong-answer distractor pool is constructed by drawing answers from non-matching question-types (e.g., a date distractor for a date question) and length-matching to within $\pm 1$ word.

## Appendix E. Computational cost

All sealed-run experiments executed on a single Apple Mac mini (M4 chip, 32 GB unified memory) using MLX 4-bit-quantized open-weight checkpoints. Per-model sealed run (21-cell panel × $n=200$ ANLI + $n=100$ TriviaQA + 1,000 OOB bootstraps): $\sim 8$–$25$ minutes wall-clock depending on parameter count (Llama-3.2-3B fastest; Mistral-Nemo 12B slowest). Total sealed-run wall: $\sim 2.5$ hours for all 9 models × both datasets. Calibration and detection are CPU-bounded on the bootstrap, not GPU-bounded on the forward pass. The 21-cell panel adds $\approx 2\times$ to per-sample compute over a single-cell calibration (one forward pass per sample, but 21 metric evaluations); a deployment-only detector recomputes only the winning cell at $\sim 1\times$ baseline.

## Appendix F. Causal probe pilot

Pilot intervention details for the $+v_\text{top}$ steering experiment discussed in §6.4. We sampled $n=20$ contradiction-labeled and $n=20$ entailment-labeled ANLI R1 samples on Mistral-7B-Instruct-v0.3, then added a scalar multiple of $v_\text{top}$ — the top right singular vector of $\sqrt{p_t} \cdot W_u$ at $\text{gen\_step}=1$ — to the residual stream before the unembedding, for $\alpha \in \{0, 10, 20, 30, 50, 75, 100\}$. At $\alpha=50$, 40\% (8/20) of contradiction samples flipped their committed YES/NO vs 10\% (2/20) of entailment samples. The entailment samples had a smaller mean post-softmax logit gap (2.49 vs 3.21 for contradictions), so the asymmetry is not explained by entailments being "easier to flip" in a logit-gap-magnitude sense. The negative-$\alpha$ direction is confounded by the same logit-gap imbalance and is reported descriptively. A sealed pre-registered follow-up — matched on logit-gap stratum and `orig_answer` balance — is required before this pilot can be promoted from non-null suggestion to validated causal claim. Full per-sample flip rates, logit-gap distributions, and code are at `experiments/causal-probe/2026-05-25/` and `scripts/causal_probe_rupture_steer.py`.

---

_End of draft. All seven body sections, six appendices, acknowledgements, and references are populated. Numbers, gate outcomes, and figure/table references are traceable to the sealed verdict and 2026-05-30 artifact build (`PRI_at_commitment/paper/v4/figures/out/`). Pre-submission polish — title selection, venue + page-length cut, .tex conversion, hook tightening, bibliography expansion, final consistency sweep — remains._
