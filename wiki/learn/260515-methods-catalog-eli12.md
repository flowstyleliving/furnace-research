# 🚗 All the Methods on the Dashboard, ELI12

**Rigorous version:** [v3-code-map](../pri-v3/v3-code-map.md) + [overview](../overview.md) (formulas, code anchors)
**Companion:** [v3-pipeline-eli12](260428-v3-pipeline-eli12.md) · [harp-vs-pri-eli12](260420-harp-vs-pri-eli12.md) · [llm-pipeline-eli12](260507-llm-pipeline-eli12.md)

---

## 🎯 The question

At the exact instant a language model commits to its next word, *something* shifts in its hidden state. Furnace's bet is that the **shape** of that shift tells you whether the answer is about to be wrong. Every method we run is a different way of measuring that shift. This page is the dashboard tour — what each gauge reads, computed in inference, in the order it fires.

## 🧠 The metaphor: a self-driving car's dashboard, snapshot at the instant of a turn

Imagine a self-driving car rolling toward an intersection. The moment its brain commits to "turn left now," its black-box recorder freezes one frame. On that frozen frame we have several gauges. They all watch the same instant, but each asks a different question.

The frozen frame in the pipeline = `(h_t, h_prev, p_t)` at `gen_step=1`. `Δh = h_t − h_prev` is the wheel's nudge between the last frame and this one. `p_t` is the next-word probability — "which lanes does the car think exist right now."

🧭 **Gauge 1 — Compass (PRI v1, cosine).** *"How much did the steering wheel turn between the last frame and this one?"* Cheap: just the angle between `h_t` and `h_prev`. Score = `S_t · (1 + α · (1 − cos(h_t, h_prev)))`. Multiplicative: surprise gets amplified when the wheel jerks. Baseline gauge, kept around to beat.

💪 **Gauge 2 — Weighted thrust (PRI v2, Fisher-pullback `d_F`).** *"How much **meaningful** movement happened, weighted by the lanes the car was actually considering?"* Pulls `Δh` through the unembedding `W_u`, then asks how spread out that vector is **under the current word-probability distribution `p_t`**. Variants are different ways to estimate that spread cheaply:

- `d_F_diag` — diagonal-only (fastest, crudest)
- `d_F_full` — full empirical variance under `p`
- `d_F_topk{5,10,32}` — only the top-k most-probable words matter
- `d_F_lowrank{10,32,50}` — SVD of `√p · W_u` truncated to rank r (current best estimator)

Additive: `PRI_v2 = S_t + α · d_F`. Surprise and rupture are independent contributors. v2 beats v1 on all three primaries — that's the hull we already trust.

🎯 **Gauge 3 — Steering quality (PRI v3, `null_ratio_resid`).** v2 only gauges *how much* movement; v3 asks *where it went*. Take the same SVD `√p · W_u = U Σ Vᵀ`. The top-r rows of `V` are the "real lanes" — the directions that actually steer the next word. Project `Δh` onto everything **outside** those rows:
`null_ratio = ‖Δh − V_topr V_toprᵀ Δh‖ / ‖Δh‖`.
High ratio = the wheel turned, but **off the road into a ditch** — directions that don't change any word's probability. Rank pinned at **r=1** in the sealed gate. The headline v3 metric.

🗺️ **Gauge 4 — Generic-map version (`null_ratio_raw`, HARP baseline).** Same question as Gauge 3, but uses SVD of **raw** `W_u` (no `√p_t` weighting). Static, computed once at model load and cached. Cheaper, no probability awareness. The E17b head-to-head asks: *does today-traffic weighting (Fisher) actually beat the generic street map (HARP)?* Answer so far: model-dependent — wins on Llama/Mistral, loses on Qwen.

🔀 **Gauges 5 & 6 — Variants of Gauge 3.** `null_bare` = the unnormalized off-axis norm (numerator only — drops the magnitude denominator). `null_gated` = `null_ratio` only counted when `d_F` is above a threshold, otherwise zero. `null_gated` was supposed to filter weak movements out; it failed the E19 interpretation gate on all four tested models.

📏 **Gauge 7 — Trajectory shape (chord-vs-path Fisher diagnostic, in-flight).** Up till now every gauge looks only at the start-vs-end of the trip through the transformer stack (chord). The new gauge sums the **per-layer** Fisher steps and asks whether the trip went straight or zigzagged:
- `d_F_chord` = `√((h_final − h_layer0)ᵀ F_final (h_final − h_layer0))` — straight-line distance under one metric.
- `d_F_path_fixed` = `Σ_ℓ √(Δh_ℓᵀ F_final Δh_ℓ)` — sum of per-layer hops under the **same** metric. By the triangle inequality `path_fixed ≥ chord`; `curvature_fixed = path − chord` is the "wandering" measure.
- `d_F_path_varying` = same sum but each layer uses its own logit-lens Fisher metric — descriptive only, not comparable to chord.

Decision rule (sealed before any number): `corr(chord, path_fixed) > 0.95` ⇒ chord captures everything. `0.7–0.95` ⇒ path adds independent signal. `≤ 0.7` ⇒ chord is throwing away information and the whole panel might need redoing on path quantities.

## 📊 What we measured / saw

At the sealed v3 plane (final layer, gen_step=1, n=200, rank=1):

- 🦙 Llama 3.2-3B — `null_ratio` AUROC **0.86** [0.81, 0.91] (random=0.50)
- 🌀 Mistral 7B — `null_ratio` AUROC **0.86** [0.81, 0.91]
- 🐉 Qwen 2.5-7B — `null_ratio` AUROC **0.73** [0.66, 0.80]

v2 best `d_F` variant at the same plane: Llama 0.77 / Mistral 0.67 / Qwen 0.79. v3 beats v2 on Llama and Mistral; Qwen prefers v2's magnitude over v3's direction. Chord-vs-path: results not yet in — the broad7 panel is queued behind tonight's main sweep.

## ✅ / ❌ / 🎁 What this tells us

- ✅ **Additive Fisher (`d_F`) beats multiplicative cosine.** Curvature-aware geometry pays off in magnitude space.
- ✅ **Direction beats magnitude on Llama / Mistral.** `null_ratio` adds signal that `d_F` collapses away.
- ❌ **`null_gated` is dead.** Gating-by-magnitude doesn't recover anything `null_ratio` and `d_F` don't already give us — E19 failed across all four models.
- 🎁 **Qwen is the contrarian.** v2's magnitude beats v3's direction on Qwen 2.5; HARP's flat geometry beats ours on Qwen too. The "right" gauge is architecture-dependent, not universal.

## ⚠️ Caveats

- Every gauge is read at **gen_step=1, final layer**. Off-plane results are descriptive, not sealed.
- `null_ratio`'s "null space" is null only relative to the **top-probability rows** of `W_u` (row-truncation to \~256 rows for tractability). True null is bigger.
- The RMSNorm `γ` correction (Jn-correction, 2026-04-25) reshuffled cross-model verdicts. Anything older than that is geometry-mismatched.
- The chord-vs-path numbers don't exist yet — sample size in flight is n=100 per class on R1, panel of 7 models.

## 🎯 One-sentence takeaway

> One frozen frame, seven gauges: cosine asks *how much the wheel turned*, Fisher `d_F` asks *how much it mattered*, `null_ratio` asks *whether the wheel pointed at a real road*, HARP asks *the same with a generic map*, and chord-vs-path asks *whether the trip wandered or went straight*.
