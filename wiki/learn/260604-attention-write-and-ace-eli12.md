# 🎙️ How Attention Writes to the Stream (and where ACE listens), ELI12

**Rigorous version:** [v4-sealed-2026-05-26](../results/v4-sealed-2026-05-26.md)
**Companion:** [ace-vs-pri-v3-eli12](260531-ace-vs-pri-v3-eli12.md) · [llm-pipeline-eli12](260507-llm-pipeline-eli12.md)

---

## 🎯 The question
Everyone says "attention" and "the residual stream" — but what *physically* happens when one layer of a model thinks? And once we can see that, where exactly does ACE put its ear?

## 🧠 The metaphor: a recording studio
Picture a song being built on a **master tape with a fixed number of tracks** — say 8, and it stays 8 forever. Each layer of the model is one **overdub session**: the band records a new part and it gets *mixed onto the existing tape*. Nobody adds tracks; nobody erases. The tape just gets richer. That fixed-width tape is the **residual stream**, and "mixed onto" is the *only* move that ever touches it: **element-wise add** — track 1 onto track 1, track 2 onto track 2, same length, just fuller. (Your phrase: a *river of music*.)

Each session has two steps, and each starts the same way:

- 🎚️ **Level the playback first (RMSNorm).** Before the band plays, the engineer sets the monitor to a standard loudness so they always hear the tape the same way — *the song is unchanged, only the volume is standardized.* (It divides by the typical entry size, the root-mean-square, so the result doesn't depend on how many tracks there are.)
- 🎧 **Listen back, then play (attention).** Each musician = an **attention head**. To pick the next note they **listen back to earlier moments** in the song. Two things matter: *which* earlier moments they focus on (the **gaze** — `Q·Kᵀ`, then softmax into "% of attention here"), and *how hard each earlier moment was played* (its **push strength**, called the `V-norm`). The part they pull in = gaze × push, summed.
- 🎛️ **Mix it down (W_o).** Each musician works on a narrow set of mics (a head's small `d_head` workspace). The **mixing desk** (`W_o`, where the "O" = Output) folds all musicians back onto the 8 master tracks and blends them — that's "project back," so the new part is the right width to **add**.
- 🎼 **The MLP is the soloist** that overdubs a second part right after, same level-then-add ritual.

The whole write, studio term → real term:

```
  master tape  (residual stream h — fixed width, never grows)
       |
       v   -- one overdub session = one attention write --
       |
  1 LEVEL the playback    ->  norm(h)                     (RMSNorm: volume only)
  2 HAND OUT 3 forms      ->  Q,K,V = W_q*, W_k*, W_v* . norm(h)
  3 WHERE to listen       ->  gaze = softmax(Q.K^T / sqrt(d))   (% attention per position)
  4 PULL the part in      ->  z = sum(gaze * V)           (gaze x push-strength)
  5 MIX to tape width     ->  a = W_o * z                 (Output: blend heads, resize)
       |
       v
  6 OVERDUB onto tape     ->  h <- h + a                  (element-wise add, same width)
       |
       v
  master tape  (same width, richer mix)  --> next layer repeats
```

🎛️ **ACE's booth taps only stages 3 and 4** — the gaze (→ head-sync, `JS`) and the push (→ `V-norm`) — never the lyric sheet `W_u`.

## 📊 What we measured / saw
ACE is a **producer in the booth who never reads the lyric sheet** (the answer key `W_u`). It judges only the *performance* at the decision instant (t=0): are the musicians in sync (**JS** disagreement, 0 = identical focus, 1 = totally different), and are they leaning hard on a blank spot (heavy `V-norm` on the BOS "sink")? On that evidence alone, ACE flags shaky commitments on **7 of 9 models** (AUROC ≈ 0.64–0.88 vs a coin-flip baseline of 0.50) on ANLI, and as loud as **0.995** on Mistral/TriviaQA. (Exact numbers live in the rigorous page.)

## ✅ / ❌ / 🎁 What this tells us
- ✅ **The stream is a fixed-width tape; layers only overdub (add).** Width never changes — that's *why* the add is legal, and *why* `W_o` exists (to resize narrow parts back to tape width).
- ✅ **Attention = listen-back-then-play:** gaze (where) × push (how hard). A note that's loud but unheard barely affects the mix; loud *and* heard dominates it.
- 🎁 **ACE listens to the *performance*, not the *lyrics*.** Gaze, push, and head-sync — never `W_u`. That's the whole reason it's answer-key-free.

## ⚠️ Caveats
The "% of attention" softmax is over *positions* (earlier words), **not** over the vocabulary — that's exactly how ACE dodges the answer key. And whether *more* head-disagreement means *more* bluff is **learned per model** (the sign is calibrated, not assumed); the encouraging bit is that Mistral and Qwen 2.5 landed the *same* sign at the final layer.

**Takeaway:** a model "thinks" by overdubbing new parts onto a fixed-length tape — and ACE is the producer who spots a weak take by watching the band's eyes and hands, never the lyric sheet.
