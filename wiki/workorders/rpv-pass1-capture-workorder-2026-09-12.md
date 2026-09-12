# RPV at pass one — work order, 2026-09-12

**Status:** PARKED (MK, 2026-09-12). Needs a model run. Not scheduled.

## Goal

Measure RPV's three statistics on the distribution the answer token is actually drawn from — the last prompt
position, "pass one" — so the measured object matches RPV's own setup section, and RPV becomes a signal
available **before** the answer is chosen.

## Why

- 📄 **The paper and the code disagree on position.** `rpv-draft.tex:211–216` defines `p` as the distribution
  whose argmax is the committed token, which is the pass-one distribution. The code
  (`comprehensive_run.py`, `trace_pair_features`) reads `gen_probs[0]`: the distribution at the answer token's
  own position, which predicts the token *after* the answer. Verified 2026-09-11 with byte-identical provenance
  and confirmed by a Codex `gpt-6-astra` audit. See [[claims]] §10 and [[references/commit-locus]].
- 💾 **Not recoverable from banked data.** RPV artifact rows store only finished pass-two statistics (the
  `readout` sub-dict, `late_layers`, and the aggregates) plus the scalar `surprise`. No pass-one distribution
  and no pass-one hidden states were saved.
- 🎯 **The payoff.** RPV would join ACE and `surprise` as pre-selection signals, instead of being a one-token
  guard.

## Guardrails

- 🔒 **Touch nothing sealed or archived.** `t0-morphology-furnace` is archive-only and `vendor/t0_core` must not
  be edited. Implement as an **additive overlay** in `commit-confluence/exploratory/`, importing `trace_sample`
  and the spectrum functions read-only.
- 🧰 **The pipeline already returns what is needed.** `trace_sample` returns `prefix_probs[-1]` (the pass-one
  readout distribution) and `last_prefix_hidden` per layer (for the logit-lens window).
- 📐 **Change the position and nothing else.** Same pinned aggregate (readout plus the last ⌈N/4⌉ blocks), same
  top-512 support, same active-set threshold.
- 🧾 **New measurement, new pre-registration.** It cannot revise H1, which was registered on pass-two features.
  Report both positions side by side and never pool them.
- ⚠️ **Expect heavier confidence coupling, and pre-register that prediction.** The pass-one distribution
  contains the answer's own probability, so pass-one RPV should track `surprise` more closely than pass-two RPV
  did. The brittleness gate (bootstrap upper CI of the correlation with `surprise` ≥ 0.75) is the decisive check.
- 🔢 **Enumerate the comparator set before analysing any of it.** `surprise`, `null_ratio`, and pass-two RPV.
  Note that pass-one `p_max` is **not** a separate comparator: under greedy decoding it equals `exp(-surprise)`
  exactly, so including it would double-count confidence.
- 🔑 **Bank a content-bearing row key** (`prompt_sha256`), per
  [[workorders/capture-provenance-columns-workorder-2026-09-10]].

## Acceptance

- **A1** — on a smoke sample, the overlay run at pass **two** reproduces the banked RPV values exactly. That
  proves the only change at pass one is the position.
- **A2** — every late-window block is present at the prefix position for every model in the panel.
- **A3** — the pre-registration, with its comparator set and the coupling prediction, is frozen before the full
  run.

## Handoff

- **Codex** authors the overlay and drafts the pre-registration; it runs nothing.
- **Claude** executes the smoke test and the run, and verifies A1–A3.
- **MK** authorizes the run.
