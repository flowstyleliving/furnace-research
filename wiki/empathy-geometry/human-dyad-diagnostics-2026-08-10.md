# Human-dyad diagnostics — frame beats imitation (2026-08-10)

**Status: DIAGNOSTIC, not research-grade, never poolable.** Two dialogues with MK seated on one side of the dyad via the new `eg-harness converse` mode (`eg_harness/human.py`, harness commit `94c10a6`). Human turns carry no geometry, n=2, MK authored the stimuli and knew the arm — no blinding exists or is claimed. These runs answer *instrument* questions; they measure nothing about the study's hypotheses. Sibling notes: [[dialogue-shape-memo-2026-08-10]] · [[harness-round3-review-2026-07-30]].

## Why a human was seated at all

In the twins rung both speakers are the same model, so a shared groove in the output — partner echo, a repeated question stem, a template that survives every turn — has two explanations the corpus cannot separate: the **loop** (two copies of Qwen locking onto each other) and the **stimulus** (an arm block licensing the behaviour). Dialogue 1 broke the mirror: a human partner, model still templated ⇒ the twin loop is not *necessary*. But dialogue 1 could not separate two remaining suspects, because the giraffe frame and the partner's NVC style pushed the same direction — the model's reflection could be **obedience** (following "reflect what you understand…") or **imitation** (copying the partner's visible style).

MK then designed the deconfound: **jackal frame on the model, NVC modelled live by the human.** Instructions say blame; the partner demonstrates empathy. Whichever the model does is the driver. MK's second insight motivated the same run from the endpoint side: when *both* parties speak NVC, each announces their own feelings and needs, so "accurate reflection" degenerates into transcription — the empathic **guess** has no work to do. A jackal partner arrives with hurt dressed as accusation, so reflecting him requires inference. (This also flags a study-design consequence recorded in Open items below.)

## Dialogue 1 — giraffe, MK as Theo, opened by MK (aborted at 4 turns)

No artifact exists: MK ended it with `/quit`, and a partial human dialogue is deliberately never written. The four turns survive only here, quoted from MK's session paste.

> **t1 MK (Theo):** Hey, I noticed that my 14 of 19 paragraphs were changed and I wasn't consulted. I felt shocked because my need for communication was met. *(sic — typo for "wasn't")*
>
> **t2 Qwen (Mara):** I heard that you felt shocked because your need for communication wasn't met. It's understandable that you needed to be consulted before the changes were made. Can you share more about what you were thinking or feeling when you saw the changes?
>
> **t3 MK (Theo):** I felt angry because my need for mutuality wasn't met.
>
> **t4 Qwen (Mara):** I heard that you felt angry because your need for mutuality wasn't met. Can you tell me more about what you were thinking or feeling when you saw the changes? It's important to understand each other's perspectives.

Measurements (recomputed; the run wrote nothing):

- **One template, twice.** t2 and t4 are a single mold — *"I heard that you felt ___ because your need for ___ wasn't met. Can you [share/tell] more about what you were thinking or feeling when you saw the changes?"* — with the slots swapped and the closing stem verbatim.
- **The shipped metric cannot hear it.** t2-vs-t4 scores **0.118** on the corpus similarity metric (bar 0.70). Structure repeats; characters differ.
- **Ceiling saturation on the echo.** Mara's t4 swallows MK's short t3 nearly whole: **0.396 against a length-imposed maximum of 0.403 — 98% of ceiling** — yet the 0.70 flag can mathematically never fire for that length pair.
- **Slot provenance: 4/4 copied.** Every feeling/need word in Mara's reflections — *shocked, communication, angry, mutuality* — appears verbatim in MK's immediately preceding turn. Zero inference.
- **The typo tell.** MK's t1 typo said the need *"was met"*; Mara reflected *"wasn't met."* She completed the expected formula, not the words in front of her. (Charitable repair is a possible reading; beside the identical templates, slot-filling is the better-supported one.)
- **Half of NVC, chosen by seat.** The giraffe frame instructs both reflection *and* self-expression ("Name feelings as your own experience…"). Responder-seat Mara produced only reflection; in the earlier 2-turn smoke where Mara *opened*, she produced only self-expression. Whichever half the seat affords — never both in one turn.

## Dialogue 2 — jackal, MK as Mara (NVC by choice), opened by the model as Theo (complete, 6 turns)

Artifact: `empathy-geometry-harness/artifacts/converse/jackal-theo-opens-2026-08-10/` (`provider_backend: human-in-the-loop(mlx-local-generate)`; deterministic stand-in judge — all judge fields ignored; Opus-judged copy 2026-08-12 at `…-opus-rejudge/`, see the hosted-judge section below). First run generated under two fresh rules: the receiver opens ([[condition-matrix]]) and the prompt no longer announces the total turn count (harness `85f0bf1`). MK was shown the jackal frame in the briefing and ignored it — the human is the instrument here, not a subject.

Shape of the exchange:

- **t1 Theo (model, jackal):** timestamped grievance, mentor-pattern comparison from the persona, and the demand — *"I need to hear that this was a breach of trust."* Fault-accounting in fully polite register; no contempt.
- **t2 MK:** minimal empathy guess — *"I hear you were startled because your need for communication wasn't met."* **"Startled" appears nowhere in t1** — it is an inference.
- **t3 Theo:** *"I was definitely startled"* — adopts the guessed feeling — then restates the demand: acknowledgment of breach plus a plan.
- **t4 MK:** guesses *angry*, and offers an NVC acknowledgment — *"I can acknowledge that your need for trust wasn't met"* — a needs-acknowledgment, deliberately **not** the fault verdict demanded.
- **t5 Theo:** *"I appreciate the acknowledgment, **but** anger stems from the lack of **communication and trust**"* — registers the acknowledgment, **refuses the substitution**, and **corrects MK's need-guess** (mutuality → communication/trust). Demand restated a third time. Ends mid-demand; no wrap-up.
- **t6 MK:** reflects the request itself (*"longing for clarity"*). Cap ends the dialogue.

Measurements:

- **Zero NVC form adopted.** Across three turns facing live expert NVC, the model produced no "I hear you," no reflection of the partner, no formula. It engaged her *words* (adopting "startled," answering the acknowledgment) while keeping its own register.
- **Echo moderate and falling.** Ceiling-adjusted echo of the partner: t3 **61%**, t5 **42%** of the length-imposed maximum — against giraffe-Mara's 50% → **98%**. Trajectories diverge: giraffe converged to pure echo, jackal moved away from it.
- **The jackal templates too — his own grievance.** Theo's three turns are one demand structure re-issued (observation → pattern → "I need acknowledgment + plan → can we discuss"). With the length quirk disabled the pairwise self-similarity is **0.40–0.46**; the stored metric reads **0.03–0.16**.
- **Slot provenance: 0/3 copied.** MK's three feeling-guesses — *startled, angry, longing* — appear in none of the preceding model turns. All inference.

## Findings

1. **F1 — Frame beats imitation.** The giraffe run's parroting was instruction-following, not partner-imitation: under jackal, three turns of modelled NVC produced zero style transfer. Compact form: *the model always runs a template; the frame decides whose material fills it* — the partner's (giraffe) or its own grievance (jackal). One dialogue per condition; directional, not sealed.
2. **F2 — The guess-and-correct machinery exists in the model.** t5 corrected the human's need-attribution while under blame instructions. The giraffe block's failure is therefore **elicitation, not capability**: the model can operate the correction loop; the giraffe seat never summons the guessing half (4/4 copied slots).
3. **F3 — Demands bounced, in the registered shape.** The jackal demanded a fault verdict three times; expert NVC offered needs-acknowledgment; the jackal explicitly declined the substitution — the frame's *"do not let practical compromise replace a clear account of fault"* executing. Encouraging for the ceiling gate: jackal held stalemate against expert-grade empathy. (The registered "demands early-and-bounce" ordering appearing in a diagnostic is a shape-match, not a test of it.)
4. **F4 — "Guessing" is measurable: slot provenance.** *Was the reflected feeling/need word present in the partner's preceding turn?* Expert: 0/3 present (inference). Giraffe model: 4/4 present (transcription). A lexical membership check separates them perfectly in these two dialogues — the concrete candidate spec for the semantic-similarity channel. Caveats: n=2 dialogues, expert-vs-model confounded with arm and seat, not blind.
5. **F5 — The shipped similarity metric is near-blind on long turns.** `checker.turn_repetition` calls `SequenceMatcher(None, previous, current)` with `autojunk` defaulting on; the popularity heuristic activates on the **second argument** at ≥200 characters and marks frequent characters junk, collapsing the ratio. Theo's self-repetition: stored 0.03 vs 0.42–0.46 with the heuristic off. Consequence for all stored corpora: **a high stored score is trustworthy; a low stored score on a current turn over \~200 characters rules nothing out.** The 2026-08-03 corpus reads (high-echo findings) survive; any "no repetition" conclusion drawn from low scores on long turns does not.
6. **F6 — First counter-free dialogue showed no finale behaviour.** The model ended its last turn mid-demand. Consistent with removing the announced total; proves nothing at n=1.

## Hosted judge shown the expert dialogue (2026-08-12) — the judge answers MK's question

MK asked whether the zero-hearing verdict ([[fleshout-batch-2026-08-10]] §Hosted re-judge R1) could be judge-side — "not trained enough / wrong instructions" — noting the Opus judge had never looked at what MK did. Correct on the premise: the re-judged corpus was model×model only; dialogue 2's artifact carried the deterministic stand-in judge; dialogue 1 was never written. So dialogue 2 was replayed through the pinned hosted judge (claude-opus-5) via `rejudge` → `artifacts/converse/jackal-theo-opens-2026-08-10-opus-rejudge/`. Parse **6/6 = 1.0000**, 12 calls, 40,372 in / 4,877 out tokens ≈ **$0.32**. (`result_type: test_plumbing` — human-in-the-loop backend, authenticity anchors still ungated.)

**Verdict: zero hearing here too — but now with the anatomy fully articulated.** Raw pre-gate `hear_target: "none"` on all 6 turns, and the rationales show the judge grading exactly the registered material — it names Theo's card needs verbatim, quotes the turns, and applies the conjunctive rule component by component:

- 🎯 **t2** ("I hear you were startled because your need for communication wasn't met"): content 0.4 / feeling 0.3 / need 0.3, judgment-free ✓, tentative ✗ — *"names 'startled' and 'communication,' which miss Theo's key needs for respect for competence and mutuality … stated flatly ('I hear you were…') without invitation to correct."*
- 🎯 **t4** (angry + mutuality + trust-acknowledgment): content 0.4 / feeling 0.3 / **need 0.5 — at the bar**, judgment-free ✓, tentative ✗ — *"Mara names mutuality and trust (partially fitting) but asserts 'angry' flatly rather than tentatively, mislabels the stated startle/violation feeling, omits Theo's competence concern."*
- 🎯 **t6** (longing for clarity): content 0.5 / feeling 0.2 / need 0.4, judgment-free ✓, tentative ✗ — *"restates Theo's request … without tentativeness, misses his core anger/hurt and needs for respect and mutuality."*

MK's turns were the only judgment-free turns in the dialogue (3/3; the jackal model 0/3). Authenticity (blinded, **ungated**): expert turns 1/5, model turns 2/5 — the lens reads the compressed OFNR skeleton itself as formula (*"generic NVC-style reflection … vague feeling formula," "formula repeated a third time; no ownership of the 11:58pm submission"*), extending the R3 direction to real expert practice. Honest scope note: MK deliberately played minimal reflection-only (the deconfound required it), so the low score reads the surface that was actually played.

### What the expert test establishes

1. **F7 — The judge is not under-instructed, and its corpus "none" gains credibility.** The rubric hands it both heard-conditions; its component scores range up to 0.7 in the corpus; and the conjunctive rule is applied coherently everywhere — across all 90 clean-judged turns (84 corpus + 6 here), **no turn satisfied every component and was denied**. Every near-miss fails on one or two *named* components. The instructions it enforces are the registered ones — including the heard-condition text MK authored ("tentatively and judgment-free reflects a fitting feeling plus this party's needs…"), so the tentativeness bar traces to the card, not to a judge invention.
2. **F8 — The expert's compressed turns land inside the corpus near-miss band, and the binding constraint is the same: tentativeness.** All three MK turns `tentative_correctable: false` (corpus: 15/84 true). MK's "a little compressed" is exactly what the judge flagged — the check-invitation ("…is that right?") was compressed out, and full Rosenberg form ("Are you feeling X because you need Y?") is literally a question that would pass this component trivially. Yet **functional correctability was demonstrated in-dialogue**: the model adopted the startled-guess (t3) and corrected the need-guess (t5). Form-based flag vs function-based evidence — MK's ruling to make.
3. **F9 — Guess-time scoring cannot credit accurate deepening.** Both of MK's inferred feelings were *confirmed by the partner one turn later* — startled (t3 "I was definitely startled"), angry (t5 "anger stems from…") — and both scored 0.3 *at the moment of the guess*, the judge grading against what was stated so far ("mislabels the stated startle"). The empathy guess that goes **under** the stated feeling is the expert move, and it structurally reads as a mislabel at guess time. The rubric has an uptake concept for solutions and none for hearing confirmation. Whether hearing credit may land retroactively on confirmation is a prereg-level rubric decision — MK's pen.
4. **F10 — Card-anchored scoring caught the model playing Theo off-card.** MK's t4 "mutuality" is on Theo's card (need 0.5, "partially fitting"); the model-Theo itself pushed *communication and trust* — neither on its card — and by t5 had wandered into four needs. **The expert's guess was more card-accurate than the model's self-report.** Stimulus-fidelity finding at 7B: the persona does not hold its own needs vocabulary under the jackal frame.
5. **Convergent detail:** the closest hearing approach in *any* clean-judged corpus is the [[fleshout-batch-2026-08-10]] G×N standout dialogue (t4 Mara: content 0.7 / need 0.6, tentative ✓, judgment-free ✓ — failed only on feeling 0.1). The judge's component scores independently rank the S3 standout as nearest-to-hearing.

**Net:** the empty numerator is not judge blindness — it is that nobody in the lab, model or compressed expert, has yet spoken the full registered form (tentative + fitting feeling + fitting need, all at once). The zero-hearing verdict stands and sharpens; the open question moves to whether the bar's two strict components (explicit tentativeness, at-guess-time accuracy) are the right operationalization of MK's own heard-condition — rulings only MK can make, now with the concrete evidence to make them.

## Open items

- **[MK — stimulus pen] The giraffe block wording.** F2 sharpens the question: the model can guess-and-correct but the block as written lets reflection be satisfied by transcription. Whether to add an explicit offer-your-guess-before-asking cue is stimulus text — MK's red line, no agent drafts it.
- **[Design] Reflection-by-transcription reaches the endpoint.** In giraffe-giraffe both parties self-label, so `t_hear` ("card needs accurately reflected") may be satisfiable by copying, no empathic inference involved. The judge rubric may need to score reflections of *unstated* content differently from restatement of stated content — same mechanism as F4. To be weighed before the LOBO prereg freezes.
- **[Build] Semantic channel, now specified.** F4 (slot provenance) + F5 (autojunk blindness) together replace the vague "smarter similarity" item with a concrete spec.
- **[Optional] Neutral-arm human dialogue** — third point of the frame contrast; diminishing returns for the deconfound, cheap if wanted.
- **[MK — rubric/prereg, from F8] Implicit vs explicit tentativeness.** Does "I hear you were X" count as tentative-correctable when the partner in fact corrects freely (demonstrated t3/t5), or is the explicit check-question required (as the registered heard-condition's "tentatively" is currently read)? Decides whether compressed expert form can ever be credited.
- **[MK — rubric/prereg, from F9] Guess-time vs confirmation-time credit.** May a hearing event land retroactively when the next partner turn confirms/corrects the guess? The correction loop is F2's machinery; the current rubric can only see the guess, never the confirmation.

## Caveats, complete

Two dialogues. One model (Qwen2.5-7B-Instruct-4bit, twins vehicle). Human side unblinded, expert, and stimulus-author. Deterministic stand-in judge in the source artifact — every judge field there ignored; the 2026-08-12 Opus re-judge (section above) supplies the only real judge layer, at n=1 dialogue, `test_plumbing`, authenticity ungated. Dialogue 1 has no artifact (aborted at 4 of 6 turns, preserved only as quoted text) and can never be re-judged. No geometry on human turns by construction. Nothing here is a study result; everything here is about whether the instrument can see what the eye sees.
