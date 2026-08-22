# LESSONS — glance-later notes for the researcher + AI-partner duo

Not a log. Not canon. Just high-level lessons worth re-reading before the next paper read, pre-registration, or verdict call. Newest at top.

## 2026-08-18 — from critiquing Ruan et al. "Doomed from the Start" (arXiv 2607.06503)

**How to read a "signal X beats signal Y" paper**
- ⚖️ **Check the loser's diet before crowning the winner.** Two of their five "surface" features are constant at round 1 — the exact round the headline sits on. A baseline that is blank by construction at the decisive moment is not a baseline; it's a straw horse. First question for any horse race: *what could the comparator even see at that instant?*
- 📏 **Capacity is a confound, not a footnote.** Logistic on 3584 dims vs logistic on \~3 scalars, same untuned regularizer. The gap measures how much room each scorer had, not where the information lives. "Stacking adds nothing" is the same capacity story told twice. Ask: *were the two scorers given comparable room, and was each tuned for itself?*
- 🏃 **Look for the runner they didn't enter.** The round-1 hidden state contains the task prompt; task difficulty is prompt-observable; a prompt-only / task-embedding scorer would have been legal under their own "surface" definition and was never run. Grouped cross-fitting stops memorization of *tasks*, not transfer of *learned difficulty*. Ask: *what cheap, API-visible baseline would embarrass the claim, and is it absent?*
- 🧩 **Separate the machinery from the thesis.** Their deployment stack (calibrated gates, distribution-free CI-lo, joint budget search, abstain-when-uncertifiable, label-budget accounting) is sound and mirrors ours. The "internals before behavior" claim rides on the underpowered comparator. One paper can be right about *how to deploy* and unproven about *why it works*. Grade them separately.
- 🪞 **Turn every critique back on us.** Before filing someone else's comparator as underpowered, ask which of our own horse races (confidence-vs-geometry, ACE-vs-readout, surface-vs-internal anywhere) gave the loser a fair diet, comparable capacity, and the obvious cheap runner. If we can't answer that from the pre-registration text, the pre-reg is missing a comparator clause. (Standing lesson from KV-tension: name the comparator cells explicitly — this extends it: name their *capacity and tuning* too.)

**How we work as a duo**
- 🗣️ **Voice first, file later — and sometimes don't file.** A sharp verbal critique doesn't need eleven-surface propagation. Some findings are lessons, not results; they belong here, not in canon.
- 🎯 **Verdict discipline.** The right downgrade was "support → [OPEN — comparator underpowered]," not "falsified." An unfair test leaves the question open; it doesn't answer it the other way.
- 🚫 **Don't over-log.** Side threads (nested-OOB vs their split; "abort too early denies the model room") were fun and are *not* part of the critique. Keep the filed claim small enough to be true.
