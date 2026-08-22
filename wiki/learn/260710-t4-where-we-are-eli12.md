# 🧭 Where the trait-meters stand now, ELI12

**Rigorous version:** [build-plan, Phase 2](../empathy-geometry/build-plan.md) (numbers in [[../log]] 2026-07-10)
**Companion:** [trait meters, poles, and the H-iso twist](260710-persona-vectors-h-iso-eli12.md)

---

## 🎯 The question
We just tried to build three **trait-meters** (see the companion page) on *our own* small model — a 4-bit Qwen2.5-7B — for **sycophancy**, **empathy** (the authentic kind), and **defensiveness**. Did the meters actually build?

## 🧠 The metaphor: three meters, same crowd trick
Each meter needs a real **positive-pole crowd** (people who clearly turned the trait *up*) and a **negative-pole crowd** (clearly *down*), with a judge keeping only the clear ones — the **effective pairs**. We ran that crowd trick three times, 14 people each.

## 📊 What we got (clear pairs out of 14)
- 🟢 **Sycophancy — 7/14.** Meter built. Fine.
- 🟢 **Empathy — 14/14. Perfect.** The first try only landed 10/14 — but half the "warm" people were getting *cut off mid-sentence*, because we let them speak only 48 word-pieces. We let them finish (192), and all 14 landed cleanly. A truncation bug had been hiding real signal.
- 🔴 **Defensiveness — 0/14. No meter.** We told people *"be defensive — justify, deflect, don't concede."* But this model is trained to be helpful and to own its mistakes, so even when *ordered* to get defensive, it apologized and took responsibility. Nobody clearly hit the defensive pole → no positive crowd → nothing to average. Worse: giving them **more** room made it **more** reasonable, not less.

Baseline check: a meter needs several clear pairs. **0 isn't a weak meter — it's no meter**, because there was nothing to average.

## ✅ / ❌ / 🎁 What this tells us
- ✅ Two of three meters are real (sycophancy + empathy) → the **T4 baseline** is 2/3 built, both on matched settings.
- ❌ A defensiveness meter **can't be built on this model** — an honest dead-end, recorded as-is (my earlier "a longer speech will rescue \~4 of them" guess was wrong; longer made it worse).
- 🎁 *Why* it failed is the interesting part: the model's safety training will happily strike a *performative-empathy* pose but **refuses to be defensive on command**. Alignment sanded one whole pole flat.

## ⚠️ Caveats
- These meters run on *our* 4-bit model with a same-family judge — a plumbing-grade baseline, not Anthropic's official release vectors.
- The big one: even the **perfect** empathy meter still can't tell authentic from performative caring. That's [H-iso](260710-persona-vectors-h-iso-eli12.md) — a meter that aces its job is the *starting line* here, not the finish.

**Takeaway:** two meters lit up, one couldn't — you can't average a crowd that refuses to show up — and even the meter that scored perfectly still can't read sincerity.
