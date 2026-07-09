---
type: learn / ELI12 explainer
companion: [[../results/gemma-scale-extension-2026-06-18]]
status: [HYPOTHESIS]
date: 2026-06-18
---

# Why the small Gemma might be "too few cameras" to read

**One-line version:** our detector (ACE) reads a model's "body language" at the moment it commits to
an answer — and a small Gemma 3 may simply not have *enough* of the body parts ACE watches for the
signal to be legible. Scale up, more body parts, signal comes back.

## 🎥 The metaphor: a bank of security cameras

Picture the model's attention as a **bank of security cameras** all pointed at the same scene (the
prompt) at the instant it decides on an answer. Each **attention head** is one camera. ACE doesn't
look at any single camera — it watches **how much the cameras *disagree*** with each other (do they
all point at the same spot, or scatter?), and **how much each camera is just staring at the wall**
(the "BOS sink" token). That pattern of agreement/disagreement is the *signature* that tells ACE
"this commit looks supported" vs "this looks like a guess."

Now the punchline:

- 📹 **gemma-3-4b has 8 cameras (4 of them shared).**
- 📹📹 **gemma-3-12b has 16 cameras (8 shared).**

Twice the cameras = twice the **resolution** on "how much do they disagree." With only 4 shared
groups, the disagreement number is computed from a tiny sample — it's *blurry and noisy*. With 8,
the picture sharpens.

## 🧩 Why that would explain the mystery

Earlier we found a weird hole: on the **ANLI** task (telling "this follows" from "this contradicts"
— a *subtle* call), the small gemma-3-4b was an **orphan** — ACE couldn't read it at all. But the
same model was *fine* on TriviaQA (plain "is this fact right?" — a *blunt* call). Then we scaled to
12b and the ANLI hole **closed** (the score jumped 0.40 → 0.71, from "can't read" to "clearly
readable").

The camera story fits perfectly:

- 🔍 **Subtle task (ANLI)** needs a *high-resolution* read of the cameras. 8/4 cameras = too blurry → orphan.
- 🪧 **Blunt task (TriviaQA)** is readable even blurry → 4b passed.
- 🆙 **More cameras (12b)** = sharper read → the subtle task becomes legible too.

## 🎚️ The extra twist: Gemma "auto-levels" each camera

Gemma 3 also does something called **QK-norm** — think of it as an **auto-exposure that levels every
camera to the same brightness** before comparing them. Helpful for the model, but it *flattens the
differences* ACE is trying to measure. On a model with only a few cameras, auto-leveling on top of
too-few-cameras makes the faint signal even harder to see. (This part is a guess we'd still need to test.)

## ⚖️ What's fact vs. what's hunch
- ✅ **Fact:** 4b = 8 heads/4 groups, 12b = 16/8; the orphan closed on scaling; ANLI is subtler than TriviaQA.
- 🤔 **Hunch (not proven):** that the *cause* is camera-count resolution (+ QK-norm flattening). A clean
  test: artificially cut the 12b down to 4 groups — if the orphan comes back, the story holds.

## 🧪 UPDATE (2026-06-20): we ran the test — and the hunch was WRONG 🦀
We did exactly that: took the big 12b and forced its detector to use only **8 cameras / 4 groups** (the
small model's budget), without changing the model. If "too few cameras" were the cause, its score
should have crashed back toward the 0.40 failure. It **didn't** — it barely moved (**0.71 → 0.67**,
still passing). So *count* isn't the problem. 🎯 The real story: the small model's cameras are
**individually blurrier** (lower-quality heads), not too few. Halving the big model's (good) cameras
costs almost nothing; the small model's cameras were just worse to begin with. A clean **"we tested
the obvious explanation and ruled it out"** — the most honest kind of result. (Rigorous: see the
Crab-lock result on the companion page.)

The nice thing: this is exactly what you'd *expect* if ACE is a real attention-head detector and not
a fluke. The detector's blind spot lines up with the model literally having fewer of the things it
detects. Rigorous version + the numbers: [[../results/gemma-scale-extension-2026-06-18]].
