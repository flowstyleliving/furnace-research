# 👀 ACE vs PRI v3, ELI12

**Rigorous version:** [v4-sealed-2026-05-26](../results/v4-sealed-2026-05-26.md) (ACE) · [v3-main-run](../results/v3-main-run.md) (PRI v3)
**Companion:** [harp-vs-pri-eli12](260420-harp-vs-pri-eli12.md) · [methods-catalog-eli12](260515-methods-catalog-eli12.md)

---

## 🎯 The question
Both ACE and PRI v3 try to catch a model in the same moment: the instant it *commits* to an answer it might not actually have support for. They watch the **same instant** — but they look at totally different things. So what's the difference?

## 🧠 The metaphor
Picture a teacher watching a student about to answer a hard **true/false** question out loud. You want to know: do they *know it*, or are they bluffing? There are two completely different ways to tell.

**PRI v3 — read the half-formed answer.** 📝 You have the answer key (in the model this is `W_u`, the unembedding — the thing that turns thoughts into words). You watch the thought leaving the student's mind and ask: *is it aimed squarely at one of the answer-key's "real answer" directions, or is it spilling into the margins* — directions the key doesn't care about? Lots of spill into the margins (high `null_ratio`) = committing without real support. **You need the answer key to even define where the margins are.**

**ACE — read the eyes.** 👀 No answer key needed. You just watch the student's *gaze and posture* in the split second before they speak. Are different parts of their focus pulling in different directions (attention heads disagreeing → JS divergence)? Are they just blankly staring at the question header (the `BOS` sink)? How hard are they leaning on each word (V-norms)? Pure body language — **decoder-free**. ACE = **A**ttention **C**ommitment **E**stimator: it reads attention, never the unembedding.

They even watch a slightly different *frame*:
- **PRI v3** watches the first word actually coming out — the residual-stream thought `Δh` at **gen_step = 1**.
- **ACE** watches the frozen instant *just before* the word, while the student is still reading the question — the prefill's last position, **t = 0**.

## 🧠 Inside the model — what the eyes actually are
Sticking with the gaze metaphor, here's what "reading the eyes" means in real wiring.

- 🎯 **Which instant is "before they speak"?** The `t=0` frame is the **last token of your prompt**, in the prefill pass — the exact spot the model is about to answer *from*. It's the same forward pass that produces the next-token answer, so it's the genuine decision instant. (The old `gen_step=1` frame watched the *first word out* instead — but that word is `\n` for Mistral, `YES`/`NO` for Qwen… messy across models. `t=0` is "always the last prompt token," so it's clean everywhere.)
- 🧮 **What "gaze" is mathematically.** Each attention head spreads a spotlight over the earlier tokens — that spread is `softmax(Q·Kᵀ/√d)`. ⚠️ Note: this is the **attention** softmax (over *positions*), **not** a softmax over the vocabulary. ACE never builds a word-probability, which is exactly how it stays answer-key-free (no `W_u`).
- 👀 **The 4 gaze metrics (weights only):** do the heads *disagree* on where to look (`js`, the Jensen-Shannon spread between heads)? Are they all just staring at the first token, the `BOS` sink (`bos_mass`)? Same two with the sink removed (`js_no_bos`) or with grouped-query heads merged first (`js_kv_groups`).
- 🪝 **The 3 V-norm metrics (the SinkProbe borrow):** a V-norm is `‖W_v · x‖` — the hidden state *after* the value projection, then its length. It is **not** the hidden state's own size; it's "how heavy is the contribution this token hands forward." A heavy contribution parked on the BOS sink that everyone's staring at = leaning on a blank placeholder = a bluff tell.
- 🪝 **Is ACE the SinkProbe?** No — SinkProbe is a separate published baseline. ACE just *borrows* 3 SinkProbe-style V-norm features and bolts them onto its 4 gaze metrics, across 3 layer depths (`final` / `mid` / `last_minus_1`), then lets the calibrator pick the single best channel per model.

## 📊 What we measured / saw
*(random guessing = AUROC 0.50; 1.0 = perfect)*
- **PRI v3** (sealed, contradiction puzzles): Llama **0.86**, Mistral **0.86**, Qwen 2.5 **0.73** → **PASSES 3/3**. One single sealed metric (`null_ratio_post_rank1`).
- **ACE** (ANLI R1, n=200): **7/9 models** clear the bar (≈ 0.64 → 0.88). On TriviaQA it's even louder — Mistral hits **0.995**. But it's a whole **panel** of attention channels, and the *winning* channel is only exactly portable across tasks for **3/9** models (partial transfer).

## ✅ / ❌ / 🎁 What this tells us
- ✅ **Different sensor, same crime scene.** v3 reads the *thought content* (residual stream); ACE reads the *attention behavior* (gaze). Both fire at the commit moment.
- ✅ **ACE is `W_u`-free.** It never touches the unembedding, so it sidesteps all the Fisher/SVD machinery v3 leans on.
- 🎁 **ACE is one metric vs. a calibrated panel.** v3 = one pinned formula. ACE = pick-the-best-channel-per-model, then recalibrate per task.
- ❌ **Neither is a universal gauge.** v3 needs rank pinned + per-model checks; ACE needs per-(model, task) recalibration for most models.

## ⚠️ Caveats
"Same instant" is a teaching simplification — v3's gen_step=1 is one tick *after* ACE's t=0, so they're neighbors, not identical. And these aren't a head-to-head bake-off on one dataset: v3's headline numbers are on sealed contradiction puzzles, ACE's are on ANLI/TriviaQA. Don't read 0.86-vs-0.79 as "v3 beats ACE" — different tests, different bars.

---

**Takeaway:** PRI v3 reads the answer as it forms and needs the answer key to judge it; ACE just watches the student's eyes — no key required.
