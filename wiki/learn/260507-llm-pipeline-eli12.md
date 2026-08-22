# 🏭 The LLM pipeline, ELI12

**Rigorous version:** [overview](../overview.md)
**Companion:** [model-architecture-families-eli12](260425-model-architecture-families-eli12.md) (what happens at the sampling step, across four models)

---

## 🎯 The question

You type *"the cat sat on the ___"* and the model answers *"mat."* What actually happens between your keystroke and the reply? The full answer is a factory line — each station does one job and hands off.

## 🧠 The metaphor — a custom-order factory

A factory takes a half-finished sentence in the front door and ships a single next-word out the back. Inside, your sentence rides a conveyor through eleven stations:

1. ✂️ **Receiving desk (tokenizer).** Your sentence is chopped into catalog parts — *unbelievable* may come apart as `un` + `believ` + `able`. The factory only stocks \~50k–150k part-types.
2. 🎫 **Barcode printer (token IDs).** Each piece gets a unique number: `cat → 4937`. From here on, only numbers move.
3. 📇 **Kiosk (embedding).** Each barcode is swiped to print a thick **feature card** — a list of \~4096 numbers describing what that piece "means" to the factory.
4. 📍 **Position stamp (position encoding).** Each card is stamped with where it sat in line — without it, the factory can't tell *dog bites man* from *man bites dog*.
5. 🏭 **Workshop bays (decoder blocks × N).** The full stack of cards travels through \~30 **identical bays**. In each bay, every card peeks at every other card and rewrites its own notes. After all bays, the last card has soaked up the whole sentence.
6. 🧽 **Calibration press (final RMSNorm).** A gentle press flattens any single number from running away with the answer. (The same press is used inside every bay; the final one is just the last in line.)
7. 📚 **Catalog match (vocab projection / unembedding).** The last card is held up against a giant catalog of every possible next word and **scored** for each. A card pointing toward `mat` scores high for "mat," low for "couch," near-zero for "elephant."
8. 🌡️ **Softening filter (softmax).** Raw scores become **probabilities** that add to 1: *"70% mat, 12% floor, 8% couch, …"*
9. 🎲 **The picker (sampling).** A worker grabs one word, weighted by those probabilities. At temperature 0, always the top one; warmer settings allow surprise.
10. 🔤 **Detokenizer.** The picked barcode is looked up to recover letters: `4203 → mat`.
11. 📦 **Out the door.** "mat" appears at the end of your sentence. To keep generating, your sentence-plus-"mat" is shoved back through the front door — the whole loop runs again, **one word at a time**.

## 📊 Worth knowing about scale

- 🏭 **N is big.** Llama 3.2 3B has 28 bays; Mistral 7B has 32. Most of the model's parameters live inside the bays.
- 📚 **The catalog is bigger than the kiosk.** Qwen 2.5's catalog has **152,000 entries** — the matrix that scores against it (`W_u`) is the single biggest tensor in the model.
- 🎫 **Sometimes the kiosk and the catalog are the same booth.** "Tied-embedding" models (Gemma, Llama) reuse one tensor for both — going in and coming out share a single lookup table.

## ✅ / ❌ / 🎁 What this tells us

- ✅ **The "language" lives between stations 5 and 7.** Stations 1–4 turn text into numbers; 8–11 turn numbers back into text. Meaning, grammar, and reasoning all happen in the bays and at the catalog match.
- 🎁 **PRI is a sensor between station 6 and station 7.** Furnace measures *what the last card looks like just before the catalog match* — the moment of commitment to an answer.
- ❌ **There is no "thinking pause."** The line runs once per word, every time. "Reasoning" is what emerges across many one-word loops.

## ⚠️ Caveats

- 🪟 **This is the decoder-only Transformer** (GPT-style). Encoder-decoder models (T5, original Transformer) have a second parallel line for the input. Most modern LLMs are decoder-only.
- 🔬 **Position encoding is more subtle than a stamp.** Modern models use RoPE (rotary positional embedding) *inside* the attention step rather than a single stamp at station 4. The stamp is a clean mental model, not the literal mechanism.
- 🎲 **Sampling is a knob, not a fixed thing.** Temperature, top-k, top-p, nucleus, beam — all different "pickers." At T=0 (greedy) the line is deterministic; at T=1 it's random within the catalog probabilities.

---

**Takeaway in metaphor:** A language model is a factory line — text in, numbers in the middle, text out. Eleven stations, one of them (the workshop bays) does the heavy lifting, and you get exactly **one** new word per trip down the line. Want a paragraph? Send it through the line a hundred times.
