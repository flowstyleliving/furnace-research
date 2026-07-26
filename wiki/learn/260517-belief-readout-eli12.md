# 🃏 The Belief Readout — Reading the Model's Poker Tell, ELI12

**Rigorous version:** [step0-belief-readout-2026-05-17](../results/step0-belief-readout-2026-05-17.md) · frozen rule: [step0-belief-readout-prereg-2026-05-17](../results/step0-belief-readout-prereg-2026-05-17.md)
**Companion:** [attention-sinks-and-heads-eli12](260515-attention-sinks-and-heads-eli12.md) (the v4 chapter right before this one)

---

## 🎯 The question

We'd been snapshotting each model's "brain" at the exact moment it answers a YES/NO puzzle. Then we found out one model (Qwen 2.5) doesn't *answer* there at all — it clears its throat first ("To determine if the hypothesis is entailed, let us break this down…"). So had we been measuring a real decision, or just throat-clearing? If it's throat-clearing, a big pile of numbers is built on sand.

## 🧠 The metaphor

Picture a **poker player** deciding to fold or call.

- 🗣️ **Table talk** = the words the model says first when you let it generate freely. Qwen 2.5's table talk is *"hmm, let me think about this…"* — stalling, not a decision. That's the throat-clearing.
- 😐 **The tell on their face** = the model's *next-word probabilities* the instant before it speaks: how much weight on "YES" vs "NO". This exists even when their mouth says "let me think." That's the **belief readout** (`lean = log P(yes)/P(no)`, read at `t=0`, zero words generated, one peek).
- 🤝 **The honest player** = Mistral-Nemo, who always says exactly what he'll do. We read *his* tell, then check it against his spoken move. If our tell-reading matches his words, our method of reading faces is trustworthy. That's the **anchor**.

## 📊 What we saw

A random guess is a coin flip (AUROC 0.5). A perfect tell-reader is 1.0.

- 🤝 Honest-player check: our tell-reading matched Nemo's spoken move **0.99** of the time (we needed ≥ 0.95). The face-reading method works.
- 😏 **9 of 10 players have a readable tell.** Qwen 2.5's is the strongest — **0.926** — even though its *mouth* was stalling the whole time. The decision was on its face all along.
- 😶 **1 player (Phi-3.5-mini) has a poker face.** On ~80% of hands there's no clear YES/NO on its face at all (only 37 of 200 hands readable). When you *can* read it, it's sharp — but most of the time, nothing.

## ✅ / ❌ / ⚠️ What this tells us

- ✅ **The fear is dispelled.** We worried we'd been measuring throat-clearing. The decision *was* there at the commit moment, just hidden behind the talking. There's a real thing to anchor on.
- ❌ **It does NOT bless the old numbers.** The frozen rule is strict: "a readable tell exists" does *not* mean the earlier brain-snapshots (taken during the throat-clearing) were measuring the right moment. Those still have to be re-taken at the face-reading moment.
- ⚠️ **Phi-3.5 is a loose thread.** It was one of our three "cleanest, most trusted" models — but it has a poker face here. Its old clean result might be riding something other than a crisp YES/NO belief. Flag it and look closer; don't declare it broken (it's a different test).

## ⚠️ Caveats

"Re-grounded" ≠ "old measurements validated" — only the *premise* survived. And two verdict branches never came up in this run; not seeing them isn't proof they don't exist.

🃏 **One-sentence takeaway:** the player was bluffing with his mouth, not his face — the decision was always readable, we'd just been watching the wrong thing.
