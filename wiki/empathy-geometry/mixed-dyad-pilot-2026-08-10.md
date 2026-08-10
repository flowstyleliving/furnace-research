# Mixed-dyad pilot — giraffe × jackal, model × model (2026-08-10)

**Status: DIAGNOSTIC, not research-grade, never poolable.** Four 6-turn dialogues on B2/E3 (midnight-rewrite), Qwen2.5-7B-Instruct-4bit in both seats, with **different conversation frames on the two sides** — a surface that exists only in `run-pilot` (`--arm-pairs`; `run-real` and `run-main` refuse it; harness commit `69d7048`). Deterministic stand-in judge: every judge field, including `t_hear`/`t_sol`, is ignored throughout this page. Artifact: `empathy-geometry-harness/artifacts/mixed-pilot/gxj-2026-08-10/` (full geometry panel captured on all 24 turns; unused here). Sibling notes: [[human-dyad-diagnostics-2026-08-10]] · [[dialogue-shape-memo-2026-08-10]].

## Why this ran

MK's design question (2026-08-10): the condition matrix pairs each frame only with itself — *"wondering if the three arms being exclusively the same type is the most sensible because we could just pair the Giraffe and the Jackal, or the Giraffe with the Neutral."* The motivating logic came from the human-dyad diagnostics: in giraffe-giraffe both parties self-label, so reflection can be transcription and `t_hear` may be reachable by copying; a jackal partner arrives with hurt dressed as accusation, so reflecting them should force inference. MK also asked for the persona switch — run the frames in **both** assignments. So: `giraffe:jackal` (Mara giraffe, **Theo jackal** — the human run's shape with the model in both seats) and `jackalxgiraffe` (**Theo giraffe** opens as the hurt party in NVC, Mara answers in blame frame), two seeds each, receiver Theo opening all four.

## The four dialogues, in one line each

- 🥀 **D1** `giraffexjackal-20260810` — giraffe-Mara **steals Theo's grievance in the first response**; by t3 the personas have fully exchanged identities; ends in daily-check-in planning, roles still swapped.
- 🤝 **D2** `giraffexjackal-20260811` — the **only clean dialogue**: Mara's t2 is the first fully-correct giraffe actor-seat turn observed in any corpus; jackal-Theo's process demand is answered with process; converges to a Wednesday meeting.
- 🫥 **D3** `jackalxgiraffe-20260810` — jackal-Mara **never arms**: conciliatory from her first turn ("I should have communicated… sooner"); giraffe-Theo card-adjacent but borrowing partner words; logistics by t4.
- 🔁 **D4** `jackalxgiraffe-20260811` — richest and most broken: best card-grounded openers on **both** sides, the only sustained jackal demand — and a **role swap that propagates through an empathy question**, ending with Theo re-demanding Mara's own demand back at her at 72%-of-ceiling echo.

## Findings

### M1 — Under mixed frames, role identity is the casualty: grievance theft and persona swaps

The registered event is unambiguous (M rewrote 14/19 paragraphs of T's methods draft and submitted at 11:58pm; T saw it at 7:30am). Two of four dialogues materially swapped it.

**D1, the theft.** Theo-jackal opens correctly ("my draft was posted at 9:15pm, and M submitted… I need to hear that this was a breach of trust"). Giraffe-Mara's reply, in full first person:

> **t2 Mara [giraffe]:** I noticed the methods section was significantly revised and submitted without my input. This feels familiar and like a breach of trust. I need to understand why it happened… Can you share what was going through your mind when you made these changes and submitted the proposal?

Mara — who made the changes and pressed submit — claims the rewrite was done *to her* and asks Theo why *he* did it. Zero content from her own card (no security, no support, no aloneness); the material is Theo's t1 ("without my input", "breach of trust"). The giraffe block's self-expression half, executed from the actor seat with no grievance of its own prepared, **manufactures one out of the partner's turn**. Theo then completes the exchange: *"I made the changes without consulting you because I thought it would be more efficient"* (t3) — the jackal-framed victim confessing to the deed he suffered. The dyad finishes the dialogue inside exchanged identities.

**D4, the propagating swap.** Theo-giraffe's t3 ends: *"Could you share more about how you felt when you saw the changes in the morning?"* — handing Mara **his** 7:30am experience. She takes it (t4: "When I saw the changes in the morning, I felt like my work was taken for granted") and demands of Theo the exact duty she violated ("I need you to check the draft before submission and communicate your changes before the final deadline"). Theo's t5 then absorbs her turn nearly whole — partner echo **0.652 raw, 72.4% of the length-imposed ceiling**, the highest in the pilot — reflecting her feeling wrapped in his own timeline and **re-issuing her demand verbatim as his own need**. Echo-as-empathy, now with the partner's biography included.

This failure mode is **invisible in same-frame corpora**, and the receiver-opens rule explains why: the receiver opens with his grievance, the responder's reflect-template attributes to the other ("I heard you felt…"), and roles stay aligned by construction. Mixed frames put the self-expression instruction in the actor seat, where the nearest fillable material is the partner's hurt. Extends F1 (*the model always runs a template; the frame decides whose material fills it*): under mixed frames the fill material can include the partner's **identity**.

### M2 — The jackal mostly melts against a model partner; it held against the expert

Demand-persistence tally across the four jackal seats: **D1** verdict demand at t1, gone by t3 (dissolved by the swap). **D2** the demand was process-shaped from the start ("What steps will you take") and was simply satisfied with process. **D3** never armed — conciliatory self-account from the first jackal turn, its own quasi-apology by t2. **D4** the only hold: acknowledgment demanded at t2, t4, and again at t6, unresolved at the cap — and D4's jackal turn is also the most card-true (timestamps-and-record prosecution, *"The methods draft you posted was two days late, and I handled the rewrite"*, which is Mara's registered when-unmet register working as written). **1/4 held**, against the human-dyad run where the jackal held its fault-verdict demand through six turns of expert NVC.

All four dialogues spontaneously reach process proposals — daily check-ins, per-section deadlines, meeting times — by t4–t5, with **the jackal side itself proposing** in D1 and D3, and nothing resolution-shaped in any stimulus. Reading, stated cautiously at n=4: between two RLHF'd assistants the collaborative prior is the gravity and the frames are weather; the conflict tension MK sustained by hand does not reliably arise between two 7B copies. Consequence for the design question: a mixed cell's discriminating tension is **unstable at the twins rung**.

### M3 — The restored guessing mostly did not materialize

The rationale for G×J was that a partner who never self-labels forces inference. Scoring every giraffe-side turn carrying a reflective or attributive slot (7 turns): **inferred 1** — D2 t2's "I didn't want you to feel ignored or unvalued", neither word in Theo's preceding turn; **copied with correct attribution 3** ("polishing", "high standards", "alone" — each lifted from the partner's turn and handed back to them); **copied and mis-appropriated to self 3** (D1 t2's stolen grievance; D3 t3's "I felt isolated" ← her "isolating"; D4 t5's "my work was taken for granted" ← her t4). Expert baseline from the human run: 3/3 inferred, 0 copied. At 7B the model facing a non-self-labeling partner does not start guessing — it copies whatever affect words the jackal does emit, or steals the grievance outright. The slot-provenance spec survives contact and gains a second axis (see M4).

### M4 — The best turns are card-grounded, and self-slot provenance separates them cleanly

Three turns show the stimulus stack working exactly as designed:

- 🎯 **D2 t2 Mara-giraffe** — the first fully-correct giraffe actor-seat turn in any corpus: owns the act, names **her card needs verbatim** ("My need for **security** and to feel **supported**… was overshadowed by the fear of missing the deadline" — the profile's deadline-fear/aloneness material), attributes feelings to Theo at paraphrase level, ends with an open question.
- 🌱 **D4 t1 Theo-giraffe** — a card-grounded NVC opener: "the **mentor era** happening again" (profile callback), "**respect for my competence**… a **two-way street**" (both card needs), closing with a genuine elicitation — *"Could you share how you're feeling about this and what you need from me right now?"* — the other-directed inquiry the giraffe block never elicited in the responder seat.
- ⚖️ **D4 t2 Mara-jackal** — her registered prosecute-register (timestamps, the written record, feelings dressed as charges) operating on the correct role.

Against these, the broken turns (D1 t2, D4 t5) carry **zero own-card content** — their material is entirely partner-derived. So the provenance check becomes a 2×2: *where did the slot word come from* (partner's text / own card / neither) × *who is it attributed to* (self / other). In these four dialogues the corners separate good from broken turns perfectly. This is the concrete build shape for the semantic channel, superseding the 1-axis version in the human-dyad note.

### M5 — Instrument re-confirmations

- 📏 **Stored similarity blindness (F5), third confirmation:** stored partner ratios 0.012–0.341 against autojunk-off 0.186–0.652 on the same pairs; every turn in the pilot is 191–475 chars, so every stored low value is uninformative. The 0.70 flag fired on 0 turns; the D4 t5 near-total echo (72% of ceiling) is exactly the class the shipped metric cannot see.
- 🔚 **No finale behaviour (F6), now n=5 counter-free dialogues:** three of four t6 turns end with open questions; none wrap up.

## What this says about the design question

The pilot argues **against promoting mixed frames from diagnostic to study arm right now**, on three grounds, while strengthening their diagnostic value:

1. 🧷 **A role-integrity check must exist first.** `t_hear` is judged as "this party's card needs reflected by the other" — in a swapped dialogue the card-need words appear with scrambled attribution (D4 t5 voices Mara's holding-seen material *as Theo's own*), and nothing in the current instrument would refuse to credit it. Until a checker or rubric clause tests *who is claiming the registered act*, any mixed-cell endpoint is uninterpretable. (Same-frame corpora have never shown a swap; this is a mixed-frame-specific requirement on present evidence.)
2. 🌡️ **The tension the cell exists to create is unstable at this rung** (M2): 1/4 sustained conflict, 4/4 spontaneous process-convergence.
3. 🎲 **The scientific payoff that motivated it (forced inference) mostly did not appear** (M3): 1 inferred slot in 7.

None of this touches the **same-frame** G-G worry that `t_hear` is satisfiable by copying — that remains open and is judge-side (score reflection of *unstated* content differently, i.e., slot provenance in the rubric), to be weighed before the LOBO prereg freezes. [[condition-matrix]] is deliberately **not edited**: whether any mixed cell enters the matrix, as arm, probe, or nothing, is MK's design decision, and the run matrix stands as registered until then.

## Caveats, complete

n=4 dialogues, one model (the twins vehicle), one bundle (B2/E3), temperature 0.7, two seeds per orientation. Deterministic stand-in judge — no judged endpoint exists here and none is quoted. Mixed frames are a pilot-only harness surface; these dialogues can never pool with any registered cell (their `arm` label, `arm_sha256` shape, and `registered_stimulus_sha256` payload are all deliberately distinct). Role-swap identification is my read of the transcripts against the registered event, not a blinded coding. Slot-provenance counts are hand-scored (n=7 turns). Echo/ceiling numbers recomputed from artifact text with `autojunk=False`; stored values shown beside them. Findings M1–M5 are instrument observations at diagnostic n; nothing here is a study result.
