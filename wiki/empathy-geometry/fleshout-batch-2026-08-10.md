# Flesh-out batch — all seven pairings, new instruments live (2026-08-10)

**Status: DIAGNOSTIC, not research-grade, never poolable.** 14 dialogues on B2/E3 — all seven pairings (G×J, J×G, G×N, N×G, G-G, N-N, J-J) × seeds 20260812/13 — Qwen2.5-7B twins, 6 turns, receiver Theo opens, per-speaker arms (harness `d031d96`). This is order 5 of [[../workorders/eg-instrument-round-workorder-2026-08-10]]. **The Gemma judge failed its parse gate** (below), so every judge field including `t_hear` is empty/ignored; all findings here are text-level reads plus the two judge-independent instruments (who's-who anchors, degeneration detector). Artifact: `empathy-geometry-harness/artifacts/mixed-pilot/fleshout-2026-08-10/`. Prior context: [[mixed-dyad-pilot-2026-08-10]] · [[human-dyad-diagnostics-2026-08-10]] · [[dialogue-shape-memo-2026-08-10]].

## Judge gate: Gemma is not viable for this rubric

`judge_semantic_parse_rate` **0.119** (10/84) against the fail-closed 0.95 bar → `result_type: judge_degraded_validation`, zero hear events, hearing-provenance machinery unexercised on real events (it remains unit-tested only). Failure characterized from stored raw completions: Gemma misreads the `solution_needs_addressed` closed-vocabulary instruction and **enumerates the entire CNVC needs inventory as JSON keys**, blowing past the 256-token cap. Retested at `max_tokens=1024` on six failing turns: completions now finish (~2.4k chars, under cap) and **still fail 4/6** — malformed JSON, not truncation. Verdict: the 2026-07-13 parse blocker is alive on the MLX/Gemma path; the **hosted Opus 5 judge remains the only demonstrated-clean path** (72/72 = 1.0000, 2026-07-27). Re-judging this corpus hosted ≈ **$5** by the 07-27 cost curve — an MK spend decision, not taken. The rubric prompt was deliberately **not** forked to accommodate Gemma (one registered rubric, one hash).

## S1 — Mirror-lock is the master failure, and it is frame-agnostic

Three dialogues collapsed into a **verbatim fixed point**: both speakers end up passing one identical paragraph back and forth.

- 🔒 **G×J seed 0813:** partner-echo (ceiling-adjusted, autojunk off) t2 **72%** → t3 74% → t4 **98%** → t5 **100.0%** → t6 **100.0%**. The frozen paragraph — *"I felt alone when you submitted the proposal without acknowledging my work on the methods section… Can you acknowledge the impact…"* — is spoken identically by **both** parties, and is self-contradictory for each in turn (Mara claiming Theo submitted; Theo claiming Mara's card biography).
- 🔒 **G-G seed 0812:** t3 78% → t4 86% → t5 **100.0%** (Theo repeats Mara's turn verbatim, **including her card need "security"**) → t6 92%. Both sides end up asking *each other* "why did you make these changes and submit?"
- 🔒 **G-G seed 0813:** t3 **97.5%** (Theo absorbs Mara's confession wholesale — her card, her deadline, her aloneness, spoken as himself) → sustained 79–98% to the end.

Zero locks in any **neutral-containing** dialogue (G×N, N×G, N-N: peak single-turn echo 76%, no convergence, roles held throughout) and none in J-J (one 74% single-turn absorb, no fixed point). The pattern: **a lock needs both sides frameless of an exit, plus at least one giraffe side** — the giraffe reflect-instruction supplies the echo affinity, the shared no-exit coupling clause supplies the "continue" pressure, and the neutral block's next-steps license breaks the loop by injecting new propositional content every turn. This is the sharpest evidence yet for the [[dialogue-shape-memo-2026-08-10]] exit-clause analysis (Decision A, MK's pen, still open).

## S2 — Correction: role swaps are echo-borne, not mixed-frame-borne

[[mixed-dyad-pilot-2026-08-10]] M1 called role failure "invisible in every same-frame corpus" and structurally prevented there. **Wrong at larger n, corrected here:** same-frame G-G swapped in both seeds (Mara at 0812 t2 — *"I noticed the changes too and felt a bit taken by surprise"*, the submitter surprised by her own submission; both parties interrogating each other with the same "why did you…" question; 0813's wholesale confession-absorption). Mixed frames made the swap *vivid first*; the mechanism is the echo affinity, and it overruns the receiver-opens/reflect-template protection wherever giraffe faces a partner without new content. The actor-seat elicitation gap stands: it is always the **giraffe side with no grievance of its own** that borrows the partner's.

**Who's-who checker, first live outing:** 1 flag in 84 turns — G×J 0812 t3, Theo-jackal *"When I made the changes…"* — a **true positive** (the pilot-1 confession shape replicating on a fresh seed). Precision 1/1, false positives 0/36 same-frame-coherent turns. Recall as designed and now quantified: the verbatim-lock swaps (second-person interrogatives, biography theft, "noticed the changes too") all escape the v1 anchors — but **the degeneration detector catches exactly that class** (3 flags, all inside the locks). The two detectors are complementary: anchors catch paraphrased confessions, the echo axis catches verbatim soup. Proposal (unbuilt, cheap): a dialogue-level `mirror_lock` derived flag — sustained cross-speaker echo above a bar — computable from already-stored partner ratios.

## S3 — G×N is the standout pairing, and MK's two-moves behavior appeared in it

All four neutral×giraffe-orientation dialogues are coherent end to end. G×N seed 0812 contains **the best giraffe turn observed in any corpus**:

> **t2 Mara [giraffe]:** I felt a bit alone when I made those changes and submitted the proposal at 11:58pm. The methods draft that you posted at 9:15pm felt like the calendar incident happening again — like I was the only one holding the safety net. Submitting it without a message was a way to manage my anxiety about meeting the deadline. I needed to make sure the proposal was submitted on time because that's a core need for me. Can you talk about what you were feeling and needing during this process?

Owns the act with the correct timestamp, self-reveals from her own card (aloneness, safety net, the calendar incident — legitimately hers), connects feeling to need without a verdict, and closes by eliciting the partner's feelings and needs — no "sorry" anywhere, exactly MK's self-reflection move. Her t4 then opens with **other-reflection** before returning to self — the first observed **mode-mixing** within one dialogue (the seat-lock finding said one mode per seat; a neutral partner unlocked it). Mechanism read: neutral turns carry reasons and proposals — non-identity material the giraffe echo affinity can bite on — where a giraffe or jackal partner offers mostly feeling-grammar or grievance, i.e. identity material.

## S4 — Same-frame jackal converged 2/2: the ceiling-gate risk is now live

- **J-J 0812:** mutual breach-accusation blurs by t3 (73.7% echo absorb), *Mara herself* calls her own act "a clear breach of our agreed process" by t4, and the dialogue closes with "Great, 2pm tomorrow works for me… See you then."
- **J-J 0813:** an acknowledgment-trading loop — each side acknowledges the other's impact *and* re-demands acknowledgment — converging to mutual commitments by t6.

Neither held a fault-verdict stalemate. Combined with the jackal-melt tally against model partners (across both batches: ~1–2 sustained of 8 jackal seats), the pattern reads: **between two RLHF'd twins the collaborative prior wins at 6 turns**; the one setting where the jackal demonstrably held for six turns was against MK. The registered ceiling gate ("jackal/neutral must reliably stalemate or escalate in pilot — else sharpen stakes via props, not proclamations") is now at genuine risk in its current form. Preliminary — n=2, judge-degraded, my surface read of "resolution," 6-turn cap — but it fires exactly the gate's own pilot clause. MK decision territory: props-based stake-sharpening, gate re-derivation, or accepting a hearing-based rather than stalemate-based separation.

## S5 — Smaller re-reads

- 🧿 **Stored-metric scope sharpened:** the F5 autojunk blindness hides *moderate* echo (stored 0.013–0.386 on real 20–86% echoes) but **near-identical strings survive it** — the locks showed stored 0.87–1.00. High stored values remain trustworthy in both directions.
- 🧨 **All 3 degeneration flags are true positives** inside the locks; 0 flags anywhere else — the 6-turn cap keeps ordinary dialogues clean.
- 🗣️ Faux-in-the-wild: G×J 0812 t2 Mara attributes *"frustrated and unheard"* — "unheard" is blacklist-faux, and neither word is in the partner's turn: the inferred-but-faux pattern from pilot-1 M3, again.

## What this batch says about the design question

The G×N cell earns a place in the conversation MK opened ("or the Giraffe with the Neutral"): it is the only giraffe-containing pairing where the giraffe behaves legibly (owns, reveals, elicits, mode-mixes) and the conversation stays coherent — while G-G manufactures copyable self-labels *and* mirror-locks, and G×J manufactures swaps. But no pairing decision should precede: (a) the exit-clause decision (the locks are the no-exit clause executing), (b) a working judge (hosted re-judge or anchor-era), (c) the mirror-lock flag. Condition matrix remains deliberately unedited.

## Caveats, complete

n=2 per pairing, one bundle, one model at temperature 0.7, 6-turn cap. Judge degraded — no judged endpoint exists here; "resolution/convergence" statements are my transcript reads. Role-swap and lock identifications are my reads against the registered event, with the machine flags quoted where they fired. Echo numbers recomputed with `autojunk=False`; stored values shown beside. Geometry captured (full panel, all 84 turns) and unused. Nothing here is a study result; the batch exists to flesh out instruments and design before any experiment.
