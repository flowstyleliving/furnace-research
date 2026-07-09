# 🌑 The Shadow and Its Blur, ELI12

**Rigorous version:** [Candidate #10 deconstruction](Candidate-10-Shadow-Ambiguity-Deconstruction.md) (full math) · [claims §2](../claims.md) (the verdict)
**Companion:** [not-fooling-ourselves](260607-not-fooling-ourselves-eli12.md) (the trial that judged it) · [ace-vs-pri-v3](260531-ace-vs-pri-v3-eli12.md) (the flashlight it's compared against)
**Name:** Readout Pseudo-Volume (RPV) — the metric this page explains.

---

## 🎯 The question
When a model picks a token, can we tell whether it *meant* it — pinned the answer down hard — or just landed on it because the softmax had to choose *something*? We wanted a "tell" for a **shaky commitment** — and, crucially, one that isn't just the model's confidence wearing a disguise.

## 🧠 The metaphor: a hand casting a shadow on the wall
Hold your hand in front of a lamp; a shadow falls on the wall. The **hand** is the model's real, high-dimensional thought (the hidden state `h`). The **shadow** is the token it finally says. Three things sit between them:

- 💡 **The lamp = the unembedding `W_u`.** Here's the surprise: the lamp *aims* the light, it doesn't destroy the hand. The model has far more words than dimensions, so in principle you could rebuild the hand from where the light lands — *no information is lost at the lamp*.
- 🧱 **The wall + pointing at one spot = softmax and argmax.** This is where everything collapses: the rich hand gets flattened onto a flat wall, then we point at a single token and call it "the answer." All the lossiness lives here, not in the lamp.
- 🌫️ **The blur at the shadow's edge = the thing we measure.** A crisp shadow means the hand is firmly placed — move it and the shadow jumps. A *fuzzy* shadow means the hand could be in many places and you'd see the same shape. That fuzz is an **ambiguous commitment.**

## 🔦 Two ways a shadow can be "weak" — and only one is new
This is the whole game:
- 🌑 **Darkness = confidence.** A faint, washed-out shadow is just a dim lamp — the model being unsure (`surprise`). We already measure that.
- 🫧 **Blur-shape = commitment-ambiguity.** Two shadows can be *equally dark* yet one has a tight edge and the other a wide, smeared penumbra. The *shape of the smear* is a different quantity from the darkness — and it's the one we hoped was new.

The math behind the smear is the **Fisher metric** `F_c`: a little ellipse saying, for each way you nudge the hand, how far the shadow moves. We read two numbers off it — how many directions the shadow actually pins down (**effective rank**), and how big the "invisible wiggle-room" is, i.e. how far the hand can drift without the shadow changing (**pseudo-volume**). We deliberately read the *shape*, not the size, so a brighter lamp can't fake the signal.

## 📊 What we measured (against the right baselines)
A coin-flip detector scores 0.5. The real contests both ask "do you *add* anything?":
- ✅ **Beats plain darkness (confidence).** Across 3 model families (Llama, Mistral, Qwen), blur-shape adds **+0.102** detection power on top of confidence alone (range +0.065 to +0.140; p ≈ 5 in 100 million). It passed the "is it just confidence?" gate — genuinely a *different* quantity.
- ❌ **But it's redundant with the flashlight we already own.** Our sealed v3 metric (`null_ratio`) reads almost the same fuzzy edge. Blur-shape over *that* adds only **+0.011** — under our "+0.02 worth-it" bar, and the careful interval crosses zero. **H1: NO-GO.** It's a second way to see the same thing, not a new thing.
- 🎁 **Except in total collapse.** On Qwen3-8B — the one model where the v3 flashlight dies — blur-shape lights up the blind spot, adding **+0.13 to +0.16**. That's the single thread still open.

## ⚠️ Caveats
This is a *confirmed* signal, just not a *new* one: it overlaps the metric we already sealed, so it doesn't earn a seat beside it. Per-model samples are too small to trust alone — the verdict rests on the cross-model average. And "complements v3 in collapse" is shown on one model so far, not yet across families, so it stays [OPEN]. (The rigorous deconstruction doc was written while the verdict was still pending; the final numbers live in claims.md.)

**Takeaway:** the blur around the shadow really is its own thing, separate from how dark the shadow is — but we already had a flashlight aimed at that same fuzzy edge, so the new lamp only earns its keep where the old flashlight goes dark.
