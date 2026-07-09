# 🏔️ Fisher Information on the Attention Landscape, ELI12

**Rigorous version:** [research-candidates #8](../research-candidates.md#8-fisher-information-on-the-attention-landscape)
**Companion:** [attention-write-and-ace-eli12](260604-attention-write-and-ace-eli12.md) · [fisher-square-root-eli12](260426-fisher-square-root-eli12.md)

---

## 🎯 The question
ACE watches *where* the model looks (the gaze). But two models can stare at the exact same spot while one is rock-solid certain and the other is one breath from looking somewhere else entirely. How do you measure not just *where* the gaze sits, but *how firmly it's held there*? That "firmness" has a name: **Fisher information.**

## 🧠 The metaphor: a marble on hilly ground
Picture every possible way the model could spread its attention as a point on a **landscape of hills and valleys**. The model's *actual* gaze is a **marble** resting at one spot. Now ask the only question that matters: **how steeply does the ground curve right under the marble?**

- ⛰️ **Steep, narrow bowl** → the marble is *locked in*. Give it a tiny push and it barely moves. The model's gaze is firmly decided.
- 🏜️ **Flat plain** → a tiny push sends the marble *rolling far*. Where it looks is barely pinned down — brittle.

That curvature-of-the-ground is exactly **Fisher information** (the gaze is a real probability distribution, so the curvature is mathematically well-defined). The "tiny push" is **nudging the model's hidden state `h`** — so this measures *how sensitive the gaze is to the model's own internal state* at the commit instant. That sensitivity is an axis ACE has never read.

And here's the lovely part: **ACE already half-feels this terrain.** Its inter-head disagreement (JS) drops *two* marbles (two attention heads) and measures the gap between where they land. To leading order that gap is `JS ≈ ⅛ × Fisher` — **the distance between two nearby marbles is a thumbnail reading of the local steepness.** So Fisher isn't a foreign tool bolted on; it's the direct ruler for the slope JS only samples by hand.

## 📊 What we measured / saw
Nothing yet — this is a *proposal*, logged honestly as candidate #8. What matters is the **bar it must clear**: the existing JS-radius, which scored Mistral **0.74** and Qwen 2.5 **0.60** (vs a coin-flip baseline of **0.50**) and — the prize — pointed the *same direction* on both. The new "marble-firmness" metric (the pullback to `h`) only earns its keep if it **beats those numbers and keeps the matching sign.** If it just re-derives JS, it's "JS in a tuxedo."

## 😵 The trap
The **BOS sink** is a dead plain. When the gaze pins ~99% of itself on the blank first token, the terrain under the marble flattens — and the curvature (Fisher) **collapses toward zero**, so the signal *drowns in numerical noise* rather than blowing up. (The blow-up only shows up *later*, if you invert this for a Mahalanobis "weirdness" score — dividing by near-zero spread is where NaN actually enters.) This is the *exact* sinkhole that already swallowed the centered-Fisher amendment on the *output* side ([FALSIFIED], v3.2): the same high-confidence regime where Qwen 3's signal collapsed (top eigenvalue ~10⁴× *smaller*). Promising idea, cursed terrain.

## ✅ / ❌ / 🎁 What this tells us
- ✅ **Well-posed.** The gaze is a genuine distribution, so its Fisher curvature is real math, not hand-waving.
- ✅ **Not a bolt-on.** JS is already a shadow of this Fisher (`⅛` identity) — we'd be naming a ruler we already squint at.
- 🎁 **A brand-new axis.** "How firmly is the gaze held?" (pullback to `h`) is something neither JS nor V-norms can see — and it never touches the answer key `W_u`.
- ❌ **Unrun, and the cheap version is hollow.** The head-spread flavor mostly just re-creates JS; only the marble-firmness flavor is genuinely new.

## ⚠️ Caveats
Whether *steep* or *flat* ground signals a shaky commit is **not assumed** — the calibrator would learn that direction (the sign) per model, same as everywhere else. And until it survives the BOS-sink cliff *and* out-scores JS on Mistral + Qwen 2.5, it stays [OPEN] — a hunch with a good pedigree, not a result.

**Takeaway:** ACE sees *where* the marble sits; Fisher would tell us *how firmly the ground holds it* — a real new sense, if we can keep the math from tumbling off the BOS cliff.
