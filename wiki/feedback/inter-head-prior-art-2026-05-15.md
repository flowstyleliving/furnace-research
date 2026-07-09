# Prior art for the inter-head-disagreement diagnostic

**Status:** live; first pass against two May-15 drop-ins. Updates as 9-model panel (run-02) results land.
**Last touched:** 2026-05-15
**Companion writeup:** [results/inter-head-disagreement-2026-05-15](../results/inter-head-disagreement-2026-05-15.md)

## Context

On 2026-05-15 two attention-based hallucination-detection papers landed in [`raw/papers/external/`](../lit/external.md): an anonymous ICLR 2026 submission (RAUQ) and a Wrocław arXiv preprint (SinkProbe). Both are dead-center prior art for the inter-head JS-radius diagnostic we are running at gen_step=1 on the 9-model panel. Together they reshape the verdict gate: a result that doesn't survive sink controls (SinkProbe) and isn't strictly more informative than per-head selection (RAUQ) is not paper-grade on its own. This page drafts the positioning before the panel completes so the rollup can lead with the honest framing.

---

## Paper 1 — RAUQ (ICLR 2026 under review, anonymous)

**Full title.** *Efficient Hallucination Detection for LLMs Using Uncertainty-Aware Attention Heads.*

**Method skeleton.**
- For each layer $l$, select the single head with maximum mean attention to the *immediately preceding token* across the answer: $h_l(y) = \arg\max_h (1/(N-1)) \sum_i a^{l,h}_{i,i-1}$.
- Recurrent confidence: $c_l(y_i) = \alpha \cdot P(y_i \mid y_{<i}) \cdot a^{l,h_l}_{i,i-1} \cdot c_l(y_{i-1}) + (1-\alpha) \cdot P(y_i \mid y_{<i})$.
- Sequence-level: $u_l(y) = -(1/N) \sum \log c_l(y_i)$; final score $u(y) = \max_{l \in \mathcal{L}} u_l(y)$.
- Llama 3.1 8B, $\alpha = 0.2$, layers 10–22. Unsupervised, single-pass, <1% latency. SOTA over 15 baselines × 12 tasks × 4 LLMs.

**Mechanism claim.** A tiny subset of "uncertainty-aware" heads normally concentrate attention on the immediately preceding token during correct generation. For hallucinated tokens those heads' attention to $i-1$ **drops sharply** (Figure 1 on Llama 3.1 8B layer 29, head 25). Most heads don't show this pattern — averaging-over-heads dilutes the signal 11.7% → 3.0% (Figure 3a). So **per-layer head-selection is what makes the signal usable**.

## Paper 2 — SinkProbe (arXiv 2604.10697v1, Binkowski/Adamczewski/Kajdanowicz)

**Full title.** *Attention Sinks as Internal Signals for Hallucination Detection in Large Language Models.* Preprint dated 14 April 2026, Wrocław University of Science and Technology.

**Method skeleton.**
- Sink score per (layer $l$, head $h$, token $i$): $s_i^{l,h} = (1/(T-i)) \sum_{u=i}^T A_{u,i}^{l,h}$ — the average attention received from later tokens.
- Sort sink scores within each $(l, h)$, retain top-$k$. Concatenate across $L \cdot H$ heads → feature vector $z \in \mathbb{R}^{L \cdot H \cdot k}$.
- Logistic-regression probe on labeled (hallucinated, not) examples. SOTA in 23/28 (model × dataset) pairs across 4 LLMs (Llama 3.2-3B, Phi-3.5, Llama 3.1-8B, **Mistral-Nemo**) × 7 datasets (GSM8K, HaluEvalQA, NQ-Open, SQuADv2, TriviaQA, TruthfulQA, UMWP).

**Mechanism claim + refinement.** Hallucinations correlate with attention-sink dominance, indicating a transition from "distributed, input-grounded attention" to "compressed, prior-dominated computation." Important refinement: the probe preferentially relies on sinks whose **value-vector norms $\|V_i^{l,h}\|$ are large** ("computationally active sinks"). Sinks alone don't carry the signal — sinks-with-large-value-norms do.

**Unification claim.** Several existing attention-based detectors (LLMCheck/AttentionScore, Lookback Lens, TOHA, AttnEigvals, LapEigval) can be reinterpreted as transformations of sink behavior. Concretely the Laplacian eigenvalue identity $l_{ii}^{l,h} = s_i^{l,h} - a_{ii}^{l,h}$ rewrites several spectral methods as sink-score minus self-attention.

---

## Implications for the running 9-model panel

### I1. RAUQ predicts our `lo`-orientation result mechanistically

Run-01's signature finding was that `js_radius_final` had a **`lo`** orientation on both Mistral 7B and Qwen 2.5 7B — *low* cross-head disagreement predicts contradiction. The hardening preserved raw orientation rather than post-hoc flipping it. Run-02 has so far reproduced `lo` on Llama 3B and flipped to `hi` only on Qwen3-1.7B (smallest model).

RAUQ explains this cleanly. If a small subset of heads normally concentrates on $i-1$ and *abandons it* during hallucination, those heads — which were the outliers driving cross-head disagreement — now blend in with the majority that already ignore $i-1$. Cross-head JS-radius collapses. So **`lo`-at-final is the aggregate-JS shadow of RAUQ's per-head signal**. The 3-of-4 cross-arch sign stability is consistent with a (lower-resolution) aggregate version of the same effect, not an independent discovery.

This downgrades the "cross-arch invariance" framing significantly. The cleanest honest claim is: "the same mechanism RAUQ describes per-head also shows up at the aggregate JS level at gen_step=1."

### I2. SinkProbe makes the no-BOS column the verdict gate

The hardened script reports `js_radius_*`, `js_radius_kv_groups_*`, `js_radius_no_bos_*`, `bos_mass_*`, `attn_entropy_*` per layer. SinkProbe predicts that any attention-aggregate metric that doesn't control for sinks is reading sink dominance, not attention-geometry-as-distinct-from-sinks.

**Verdict gate post-SinkProbe:**
- `js_radius_*` alone — sink-confounded; not interpretable as head-disagreement-specific.
- **`js_radius_no_bos_*`** — sink-controlled. *This* drives the [OPEN]/[FALSIFIED] call.
- `bos_mass_*` AUROC at the same layer — if comparable to `js_radius_*`, our metric is essentially `bos_mass` re-derived.
- Surviving the no-BOS gate is necessary, not sufficient: SinkProbe's value-norm refinement says sinks-with-large-$\|V\|$ are the load-bearing feature. Our diagnostic does not measure $\|V\|$, so even a no-BOS-surviving signal cannot be claimed as outside SinkProbe's scope without that control.

Phi-3.5-mini (run-02, 4/9 in) is the first model where `js_radius_no_bos_last_minus_1 = 0.77 ≈ js_radius_last_minus_1 = 0.76` while `bos_mass_last_minus_1 = 0.26` — i.e., the signal survives the sink control on this model. Worth flagging when it lands in the rollup.

### I3. SinkProbe model overlap

Their 4 evaluated LLMs (Llama 3.2-3B, Phi-3.5, Llama 3.1-8B, Mistral-Nemo) overlap our 9-model panel on **Llama-3.2-3B**, **Phi-3.5-mini-instruct**, and **Mistral-Nemo-Instruct**. For these three specifically, anyone reading our rollup will ask "how does your AUROC compare to their Table 1?" — we should be ready to read them side-by-side at the panel rollup, modulo dataset difference (they use HaluEvalQA / NQ-Open / etc.; we use ANLI R1).

---

## Implications for the v3 paper revision

Neither paper threatens the v3 sealed claim, which is **residual-stream null-ratio at commitment**, not attention. The sealed primaries (`null_ratio_post_rank1`, Fisher pullback `d_F`) operate on $\Delta h$ projected against $W_u$, not on attention weights $A^{l,h}$. So the v3 main result is in a different geometric object.

But:

### V1. §5.4 future-work attention mention

§5.4 mentions "attention-based causal probes" as a v4 direction (Sofroniew-steering of attention heads). Both papers crowd this territory. **Action:** rewrite the §5.4 attention paragraph to (a) cite RAUQ + SinkProbe, (b) position our v4 attention-related future work as *commitment-step specific* (gen_step=1) rather than full-trajectory aggregation, which is the one axis these papers don't occupy.

### V2. Bibliography additions

Both papers need bibitems for round 2 even if not heavily cited in the main text — they are too directly adjacent to be ignored. RAUQ is anonymous double-blind; cite as "Anonymous ICLR 2026 submission" until accepted, or wait for de-anonymization if the revision can hold.

### V3. Junjie Hu cross-link

Hu's likely probes (see [hu-anticipated-probes](hu-anticipated-probes.md)) are about HARP geometry. Neither RAUQ nor SinkProbe overlaps with Hu's territory, so no conflict in framing.

---

## Anticipated reviewer probes given these papers exist

### A1. "Your inter-head signal is just RAUQ averaged across heads."

**The probe.** RAUQ explicitly identifies per-layer uncertainty-aware heads that drop attention to $i-1$ during hallucination. Cross-head JS-radius is what those heads' departure-from-the-mean looks like in aggregate. So the inter-head diagnostic is at best a noisier version of RAUQ's signal, at worst a re-derivation.

**Our response (drafted).** Accept the mechanistic identification — yes, this is consistent with the same effect at aggregate resolution. Two points of differentiation:
- **Single-step, no recurrence, no head-selection training.** RAUQ requires selecting heads on training data; our diagnostic is single-pass at gen_step=1 with no per-model head selection.
- **The diagnostic is not the claim.** We are not proposing this as a detector. It's a probe to test whether attention geometry at the commit step is informative *outside the residual-stream null-ratio family*, where the v3 sealed claim lives. The honest framing at rollup is "the attention-side signal is consistent with RAUQ; the v3 paper's claim is residual-stream null-ratio, which is independent."

### A2. "Your AUROCs don't control for sinks; they're SinkProbe in disguise."

**The probe.** SinkProbe shows that essentially every prior attention-based detector reduces to sink dynamics. Our `js_radius` numbers without the no-BOS column are uninterpretable.

**Our response (drafted).** The hardened script (2026-05-15) reports `js_radius_no_bos_*` and `bos_mass_*` per layer specifically because of this concern. The verdict gate in the rollup will be `js_radius_no_bos_*` AUROC, not `js_radius_*`. We acknowledge sink dynamics are the null hypothesis for any attention-aggregate metric, and we cannot rule out the value-vector-norm refinement (we do not measure $\|V\|$).

### A3. "You're testing 9 models × 1 round of ANLI; SinkProbe tests 4 × 7. Why is your sample-of-experiments adequate?"

**The probe.** SinkProbe runs 28 (model × dataset) pairs. Our diagnostic runs 9 × 1.

**Our response (drafted).** Acknowledged in the [results page](../results/inter-head-disagreement-2026-05-15.md) limitations. The 9-model panel is for **cross-architecture invariance of the gen_step=1 signal**, not for benchmark-grade detection performance. ANLI R1 is the residual-stream PRI calibration corpus the rest of the v3 / v3.2 work was scored against; the inter-head diagnostic uses the same slice for per-sample comparability.

---

## Open / honest uncertainties

- We do not measure value-vector norms $\|V_i^{l,h}\|$. The SinkProbe refinement (sinks with large $\|V\|$ are the load-bearing feature) is outside our diagnostic's reach. A future patch could capture $\|V\|$ from the same wrapper but would not retroactively fix the run-02 verdict.
- We do not run RAUQ as a baseline. Doing so would require re-running the panel with the recurrent confidence pipeline at every gen step, not just step 1. Out of scope for this diagnostic, in scope for any v4 attention work.
- The 9-model panel uses 4-bit quantized MLX models. SinkProbe uses HuggingFace FP16. Absolute AUROC comparisons against their Table 1 are *not* clean — relative orderings within our panel are.

---

## Action triggers

- **Panel completes with `js_radius_no_bos_*` clearly positive across the panel:** rollup with the RAUQ-mechanistic framing + SinkProbe-controlled framing, lead with "consistent with prior art at aggregate resolution."
- **Panel completes with `js_radius_no_bos_*` collapsing to chance on most models:** rollup as [FALSIFIED, SinkProbe-confounded] — js_radius was reading sink dynamics, not attention-geometry-as-distinct.
- **Mixed result (survives on some, collapses on others):** [OPEN], file the within-model layer × bos_handling sweep before any [VALIDATED] move (per the audit-operating-point rule).
- **Before v3 round-2 ships:** rewrite §5.4 attention paragraph to cite both papers and position v4 attention work as commitment-step specific. Add bibitems.

## See also

- [results/inter-head-disagreement-2026-05-15](../results/inter-head-disagreement-2026-05-15.md) — run-01 (2-model) writeup; run-02 (9-model) rollup pending
- [feedback/hu-anticipated-probes](hu-anticipated-probes.md) — companion file for HARP / Hu probes
- [lit/external](../lit/external.md) — external papers catalog (RAUQ + SinkProbe entries pending)
- [log.md](../log.md) — append-only session log
- [research-candidates](research-candidates.md)ndidates.md) — v4 idea ledger (attention-based v4 directions affected by these papers)
