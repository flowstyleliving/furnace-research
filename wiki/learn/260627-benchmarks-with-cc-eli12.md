# 🃏 How the Benchmarks Work with Commit-Confluence, ELI12

**Rigorous version:** [confluence-seal-2026-06-11](../results/confluence-seal-2026-06-11.md)
**Companion:** [methods-catalog-eli12](260515-methods-catalog-eli12.md) (the "tells" themselves)

---

## 🎯 The question
Commit-Confluence (CC) doesn't grade the model. It grades *tells* — tiny internal flickers at the instant the model commits to an answer. But to grade a tell you need an answer key, and that's exactly what a benchmark is here. So how does a benchmark plug into CC?

## 🧠 The metaphor
Picture a card game. Your friend shoves their chips in — that shove is the **commit moment** (the model's first generated token, its YES or NO). Right then, a few things might give them away: their eyes dart, their hands fidget, their voice wavers. Each of those is a **tell**, and in CC each tell is a different signal: eyes = attention shape (ACE), hands = readout spread (RPV), voice waver = plain confidence (surprise), and a couple more.

Here's the clever part: you can't grade a tell *live*, because in the moment you don't know if your friend was bluffing. So you use **replays where the cards were later revealed.** Every replay carries a truth tag — *bluff* or *real*. That stack of tagged replays **is the benchmark.** ANLI R1 and TriviaQA-paired are just two different stacks (two different games); the tag is YES/entailed vs NO/contradicted in one game, right vs wrong in the other.

Grading a tell means running it across the whole stack and asking: when "the eyes did X," how often did the truth tag agree — better than a coin flip? That hit-rate is **AUROC**, and a coin flip is **0.50**. A tell only counts as "deployable" if it beats the coin flip with a safe margin (its honest lower-bound stays above 0.50).

CC itself is the **coach**. For each friend (model) and each game (task), it benches the weak tells and starts the one that graded best on *that* friend in *that* game. Crucially, there's no house rule that reads everyone — that's the whole finding.

## 📊 What we measured
On the sealed run (10 friends × 2 games = 20 situations, 200 replays each), the geometric coach fielded a deployable tell in **18 of 20** — measured against the only-fair baseline, a coin flip at 0.50. And no single tell ruled: those 18 wins were split across **12 different tells** ([full table](../results/confluence-seal-2026-06-11.md)).

## ✅/❌/🎁 What this tells us
- ✅ **The benchmark is the answer key, not the exam.** Its labels grade *tells*; the friend's skill is never the score.
- ✅ **The coach beats chance 18/20** — a panel of tells plus per-situation picking is real.
- ❌ **No universal tell** — 12 winners over 18 wins, so you re-grade per friend, per game.
- 🎁 **Bonus:** average all the tells into one blended tell and it clears a beats-chance floor on *every* held-out friend (the E1 result).

## ⚠️ Caveats
- 🃏 These stacks are **replays of hands we dealt** — the friend judged *given* cards (entailed? right?). That is *not* the same as catching them inventing a bluff from scratch. "Judging supplied hands" ≠ "catching free-play bluffing."
- 📏 Beating 0.50 means a tell **carries real information**, not that it's safe to act on — turning it into a "fold them now" rule needs separate threshold tuning.
- 🕳️ Two stacks (both ANLI) had **no working tell at all** — genuine blind spots, and adding the "voice waver" confidence tell rescued neither.

**Takeaway:** the benchmark is just the deck of revealed-card replays that lets the coach grade each tell — and the coach learned there's no single tell that reads every player, so it picks a fresh one for every player-and-game.
