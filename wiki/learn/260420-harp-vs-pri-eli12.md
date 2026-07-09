# 🧭 HARP vs PRI — The Geometry Question, ELI12

**Rigorous version:** [papers/external § HARP](../papers/external.md#hu-et-al-2025--harp-hallucination-detection-via-reasoning-subspace-projection) + [pri-v3-plan § E17b](../pri-v3/pri-v3-plan.md)
**Companion:** [null-space-eli12](null-space-eli12.md) · [fisher-weighting-eli5](fisher-weighting-eli5.md)

> 🏁 **Milestone (2026-04-18).** First external paper doing geometry on hidden states to catch hallucinations. Their tool is SVD (flat space). Ours is Fisher-information geometry (curved space). This page is the frame for why that difference might matter.

---

## 🎯 The question

A paper called **HARP** just showed up (Hu et al. 2025). They detect hallucinations using geometry *inside* the model — same general strategy as Furnace. So: are they doing the same thing we're doing? If not, does our way actually work better?

---

## 🧠 What HARP is doing

HARP's claim: the hidden states inside a language model contain **two different things mixed together**.

- 🎨 **Semantic stuff** — surface meanings, which words to pick, linguistic expression.
- 🧠 **Reasoning stuff** — the actual logic and knowledge the model is using to answer.

Their insight: those two things live in **different directions** inside the model's hidden-state space.

### How they separate them 🔪

They use **SVD** — a classical math tool that finds "the main directions of variation" in a matrix. They run SVD on the model's unembedding layer `W_unemb` (the thing that turns hidden states into word predictions). This gives them two subspaces:

- 🟢 **Semantic subspace** = directions the unembedding actually uses to pick words (top 95% of energy)
- 🔴 **Reasoning subspace** = directions the unembedding *ignores* (bottom 5%)

Then they throw away the semantic part and only look at the reasoning part. A small trained classifier learns: *"when the reasoning part looks messy or weird, the model is probably hallucinating."*

### How well it works 📊

- AUROC **0.928** on TriviaQA (Qwen-2.5-7B)
- AUROC **0.929** on TriviaQA (Llama-3.1-8B)
- Beats Semantic Entropy, EigenScore, HaloScope by 7–17 points

That's state-of-the-art on their benchmarks.

---

## 🔭 Why this matters to us

They're doing **geometry on the inside of the model to catch hallucinations** — the same strategy as PRI. So the natural question is: *are we still adding something?*

Yes. The geometry lens is different.

| | HARP | PRI (v3) |
|---|---|---|
| Geometry | 🟦 **Flat-space SVD** of `W_unemb` | 🌀 **Fisher-pullback** — SVD of `sqrt(p_t) · W_u` |
| What it assumes | All directions are equal — Euclidean | Directions matter *relative to the actual probability distribution at this step* |
| Captures what | Static structure of the unembedding | Context-dependent structure weighted by what the model is currently considering |

**The difference in plain words:** SVD assumes space is flat. Fisher-information geometry respects the fact that when you're working with probability distributions, space is **curved** — moving a little in a high-probability region is a big deal, moving a lot in a low-probability region is nothing. 🎢

HARP's semantic subspace is the same across every prompt the model ever sees. Ours updates every token — because what counts as "informed" depends on *which tokens the model was actually considering at this moment*. 🔄

---

## 🤔 So what's the bet?

**If you applied a sharper geometric lens to the same decomposition problem, would you catch hallucinations even better?** That's the comparison worth exploring — and it's what E17b in the v3 plan now tests head-to-head.

- ✅ If our Fisher-weighted `null_ratio` beats their raw-W_u `null_raw` → **curved-space geometry carries extra signal**. Validates the whole v3 framing.
- ❌ If they tie, or HARP's version wins → **the static subspace is sufficient** and our weighting is extra machinery without payoff. Plan pivots toward HARP's formulation.

Three other differences are also real:
- 📍 We measure at **commitment (step 1)** only — they aggregate over every generated token.
- 📏 We measure the **change** `Δh`, normalized — they measure raw `h`, absolute.
- 🪡 We score **directly** (unsupervised ratio) — they **train** a small classifier.

Those differences matter too, but the big one is flat-vs-curved.

---

## 🔬 Under the hood (Q&A, 2026-04-20)

Five places the table above compresses too much. Useful when someone asks *"wait, isn't that the same thing?"*

### 🧮 SVD of `W_u` outputs a **basis**, not logits
`W_u = U Σ V^T`. `V` is a new coordinate system on hidden-state space, sorted by how loudly `W_u` listens. Top rows of `V` = semantic directions, bottom rows = reasoning/null directions. Logits come from `W_u · h` — a separate operation. SVD is a **geometry tool on hidden space**, not a forward pass.

### 🎭 HARP's classifier pattern-matches; it doesn't do geometry
The geometry (reasoning subspace) is fixed by SVD, done once, reused forever. A small classifier trained on labeled hallucination examples learns: *"when the projection looks like these bad cases, flag."* Needs labels; inherits training-set distribution. PRI is label-free — the metric **is** the signal.

### 🌀 v2 already had Fisher pullback — v3 just stopped throwing away the directions
v2's `fim_lowrank` computes `U Σ V^T` of `sqrt(p_t) · W_u` and keeps only `Σ` (scalar `d_F`). v3 keeps `V` and projects `Δh` onto its null complement. Same matrix, same SVD — v2 captures **magnitude of informed update**, v3 captures **where the update went**.

FIM math for the curious: `F_hidden = W_u^T · (diag(p) − p p^T) · W_u`, so `sqrt(p) · W_u` is the Cholesky-style factor. Both versions pull the Fisher metric back through the unembedding; only the extraction differs.

### 🏗️ `Δh` is vertical, not horizontal
Everything happens at **step 1** (the committing token). `Δh_ℓ = h_ℓ − h_{ℓ−1}` is the residual-stream update **between consecutive transformer blocks** on that one token — up the stack, not across generated tokens. Token-to-token deltas would confound "which token" with "which layer" and would be a different experiment.

### 🎓 "Principled" cashes out in seven places
Why v3's framing is forced-by-math rather than chosen-by-taste:

1. **Fisher is the unique metric** on probability manifolds (Chentsov's theorem). Flat SVD picks Euclidean by default — geometrically wrong for probability-valued outputs.
2. **Unsupervised.** No classifier, no labels, no distributional bias to inherit.
3. **Pre-registered falsifiers with numbers.** `AUROC < 0.60` on ≥2/3 primary models kills v3 — see [pri-v3-plan § falsification](../pri-v3/pri-v3-plan.md#falsification-conditions).
4. **Decomposition controls.** `null_bare` / `null_ratio` / `null_gated` + residualization on `d_F` isolate direction-independent-of-magnitude.
5. **Energy-anchored rank.** `ε(r) = Σσ²_{≤r} / Σσ²` reported alongside every `null_ratio` — signal-vs-energy-captured, not signal-vs-arbitrary-cutoff.
6. **Audit-ready design.** Sign-invariance of `V V^T` proven (not hoped for); Options A/B/C named with explicit reasoning for defaults and disfavoring.
7. **Theoretical provenance.** SUP *predicted* rupture concentrates in the low-eigenvalue (blind) subspace **before** measurement. HARP found a pattern and named it; v3 made a risky prediction the experiment can break.

Each choice answers *"because X — and here's what would change our mind."*

---

## ⚠️ Caveats

- HARP on QA tasks (TriviaQA, NQ, TruthfulQA); PRI on synthetic 2×2 contradiction puzzles. **Not directly comparable** by AUROC number — different tasks.
- HARP's Qwen headline is 0.928; our v2 Qwen on puzzles is 0.786. Same model, different job.
- If E17b shows HARP beats us on Qwen — that's a real finding, not a loss. It would mean Fisher weighting is machinery without payoff at least on Qwen. (Note 2026-04-18: Prereq 8 step 1 showed Qwen's `null_ratio` is *not* flat once the final norm is applied before the logit-lens — late-rise at layer 27, dev −0.030. So E17b is now a cleaner flat-vs-curved comparison on a Qwen that actually shows structure on our side.)

---

## 🎯 One-sentence takeaway

> HARP proved the reasoning-vs-semantic split inside models is real and detectable with *flat* geometry. The v3 bet is that *curved* geometry — respecting the actual probability landscape at each step — gets us sharper signal. E17b is the head-to-head.
