# 🏃 Model architecture families, ELI12

**Rigorous version:** [v3.1-replicate](../results/v3.1-replicate.md)
**Companion:** [jn-correction-eli12](260425-jn-correction-eli12.md) (the math fix that made this picture visible)

---

## 🎯 The question

We tested four language models on the same contradiction puzzles and asked: *"do they all rupture the same way at the commit moment?"* Spoiler: **they don't**, and the way they differ is more interesting than "yes" or "no" would have been.

## 🧠 The metaphor — sprinters at the starting block

Picture four sprinters at the starting blocks of a 100-meter race. Same race, same finish line. But each sprinter has their **own first move** when the gun goes off:

- 🌀 **Sprinter Mistral** stays low and shoves backward against the block — **all the visible motion is straight back into the pad**.
- 🦙 **Sprinter Llama** lunges forward into a "set" position — the first move is a forward sway.
- 🐉 **Sprinter Qwen 2.5** drives off the block at full commit — first move is a full forward thrust.
- 🐲 **Sprinter Qwen 3** sets, breathes, then decides — first move is a varied preparation gesture.

We have **one** high-speed camera at the starting line, pointed in **one** direction. That camera sees Mistral's backward-into-the-pad motion **perfectly** (the camera happens to point that way). It sees Qwen 2.5's forward thrust **at an angle** — captures less of the actual motion. It barely catches Llama and Qwen 3.

The camera is our measurement: projecting `Δh` (the model's "first move") onto `V_raw_top1` (the static W_u top singular direction).

## 📊 What we measured / saw

The "first emitted token" at gen_step=1 across N=100 samples per model:

- 🌀 **Mistral**: 100/100 = `'\n'` (newline before answer — **lean into the block**)
- 🦙 **Llama**: 98/100 = `' Answer'` (start the answer word — **forward sway**)
- 🐉 **Qwen 2.5**: 52 = `' NO'`, 39 = `' Answer'`, 9 = `' YES'` (commit straight to content — **full thrust**)
- 🐲 **Qwen 3**: 79 = `' Answer'`, 12 = `' Let'`, 6 = `' Alright'` (varied preamble — **set, then go**)

The camera (V_raw_top1) is dominated by *whitespace and single-cap tokens* — it points in the "begin a content block" direction. So:

- 🌀 Mistral's `'\n'` lives **right on** that axis (cos = +0.59). Camera captures Mistral perfectly → static W_u top-1 alone is a 0.99-AUROC contradiction discriminator.
- 🐉 🐲 Qwen-family's `' Answer'` / `' YES'` / `' NO'` live **off** the formatting axis (cos ≈ −0.20 to −0.30 for content words). Camera barely sees the rupture → static raw subspace fails; Fisher reweighting is needed to find the right direction.
- 🦙 Llama at N=100 too noisy to call.

## ✅ / ❌ / 🎁 What this tells us

- ✅ **The cross-model E17b split has a mechanistic explanation.** Models that commit to formatting at gen_step=1 (Mistral) get a free pass with raw W_u SVD. Models that commit to actual answer content (Qwen-family) need Fisher reweighting to be measured.
- ❌ **The original "v3's Fisher pullback uniformly beats raw" hypothesis is too strong.** Some models don't need the upgrade.
- 🎁 **The architecture-dependence is itself the publishable finding.** "Fisher pullback's edge depends on whether the model's first-step commitment aligns with W_u's static top-r structure" is a richer claim than "Fisher always wins."

## ⚠️ Caveats

- 🔬 **N=100 per model.** Small enough that Llama is in the noise; need N=200 to settle Llama.
- 🔧 **One analysis plane.** We measured at gen_step=1, final layer. The cross-model picture might shift at gen_step=2 (where Mistral has emitted `'\n'` and is now committing to content) — but not yet tested.
- 🎯 **One basis comparison.** We compared Fisher-weighted vs raw `W_u` SVD. There are other meaningful subspaces (token-embedding directions, contrast pairs, attention readout vectors) that could be the *right* analysis axis for some models — we haven't tested them.
- 🪟 **Camera angle stays the same.** Real fix would be one camera per sprinter — i.e. a model-specific basis. That's a research agenda, not a one-paper finding.

---

**Takeaway in metaphor:** Four sprinters, one camera, one fixed angle. The camera was angled for Mistral's stance and we lucked out on the others by reweighting. The real story isn't "who's fastest" — it's that the first move differs by sprinter, and our measurement was secretly about Mistral's stance the whole time.
