# 💊 How We Try Not To Fool Ourselves, ELI12

**Rigorous version:** [research-candidates #10](../research-candidates.md#10-shadow-ambiguity--fisher-pseudo-volume-of-the-readout) (the shadow-ambiguity candidate + its v2 pre-registration, which lives in the t0 repo)
**Companion:** [calibration-pivot](260515-calibration-pivot-eli12.md) — the per-model/per-route humility this method bakes in

---

## 🎯 The question
We think we found a new "tell" for when a model commits to an answer it can't really support (a readout-geometry signal). But this field is a graveyard of tells that looked real and evaporated. So the real question isn't *"does our signal work?"* — it's *"how do we stop ourselves from believing it works when it doesn't?"* This page is about the machine we built for exactly that.

## 🧠 The metaphor: putting a new medicine through trials
Treat the candidate signal like a **new drug** that claims to cure a disease (catching bad commits). Nobody sane swallows a pill because the inventor is excited. Before anyone believes it, the drug runs a **gauntlet**, and each stage is built to expose a *different* way the inventor could be kidding themselves.

- 🧪 **Does the pill even dissolve right? (contract test.)** First, lab chemistry: does the formula match the recipe? `test_shadow_ambiguity.py` is pure-math checks that the statistic is *computed* correctly — before any patient sees it.
- 🍬 **Is it just a sugar high? (the confidence pre-check.)** Patients often feel better just because they're *confident* they took something (placebo). The label-free "temperature pre-check" asks: is our signal just the model's confidence wearing a lab coat? If yes, bin it — no trial needed.
- ⚖️ **Does it beat the pill we already have? (incremental over baselines.)** A new drug must beat not *nothing* but the **existing treatment**. Our signal has to add accuracy *on top of* plain confidence and the already-sealed metric — being good alone isn't enough.

## 😵 The trap we actually fell into: a rigged control group
We first compared our drug to a control group that was secretly *sicker* (a broken baseline — a metric that was below chance on that model). That flattered the drug: "**+0.13!**" Then the adversarial reviewer swapped in a *fair* control and the effect's confidence interval slid across zero (**+0.04, range −0.03 to +0.11**). We thought it worked; over a fair comparison, it didn't — *yet*. That single catch is the reason the whole machine exists.

## 🗺️ The rest of the gauntlet
- **Did you cherry-pick? (pre-registration + pinned window + multiplicity.)** Try 50 doses, report the one that worked, and you've fooled yourself. So we *write the trial down first*: one pre-chosen statistic, one pre-chosen layer-window, and a penalty for every extra thing we peeked at.
- **One lucky clinic, or many hospitals? (cross-model meta-analysis.)** A cure that only helps at one hospital is probably that hospital's fluke. We run across *every model and benchmark we have* and ask whether it holds *on average across architectures* — never one model. (Bonus rule: if it only works on one model *family*, we're only allowed to claim a family-specific result.)
- 🦠 **The reviewer whose job is to reject it (adversarial review = the immune system).** The most important part: a second reviewer (Codex) paid to **kill the result**. It found the rigged control. We fixed it; it reviewed *again*; it found six more things. The build itself ran the loop — write → review → fix → review → fix — so the big run executes a protocol that already survived two attackers.

## ✅ / ❌ / 🎁 What this tells us
- ✅ **The method's product is honesty, not hype.** Its biggest win so far was catching *our own* inflated "+0.13."
- ✅ **Adversarial review really is an immune system** — it detects and attacks claims that don't belong, before they reach the bloodstream (a paper).
- 🎁 **It's reusable.** Any future candidate goes through the same gauntlet; the traps don't care which signal it is.

## ⚠️ Caveats
This machine makes us *honest*, not *right*. It can't manufacture a real effect — if the full trial washes out, that's a true null, and the move is to retire the drug, not re-run until it sparkles. And a gauntlet this strict will sometimes reject a real-but-tiny effect on purpose (we demand a minimum effect size).

**Takeaway:** we never ask "is our signal real?" — we put it through a drug trial designed to expose every way we could be kidding ourselves, and let an attacker try to throw it out before we believe a single word.
