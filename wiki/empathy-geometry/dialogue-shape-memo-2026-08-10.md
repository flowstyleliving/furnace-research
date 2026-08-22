# Dialogue shape — one clause, three decisions (2026-08-10)

> **Status: DESIGN ONLY · NEEDS USER DECISION.** Nothing built, nothing committed, no harness file touched. This memo bundles three questions MK has raised separately — partner echo, arm exits, and a frozen opening line — because reading `spec.ARM_BLOCKS` shows they are all the same sentence.
>
> Related: [[arm-blocks]] · [[build-plan]] · [[harness-round3-review-2026-07-30]] · [[workorders/eg-round3-degeneration-workorder-2026-07-30]] · [[condition-matrix]]

---

## 1. The finding that makes this one decision

All three arm blocks end with the **same coupling clause**:

| arm | tail of the block |
|---|---|
| giraffe | *Do not force agreement or a solution;* **continue the exchange from what the other person actually says.** |
| neutral | *Do not follow a named communication method;* **continue the exchange from what the other person actually says.** |
| jackal | *…do not let practical compromise replace a clear account of fault.* **Continue the exchange from what the other person actually says.** |

That one shared sentence is doing two harmful jobs at once:

1. 🚪 **It is the no-exit instruction.** "Continue the exchange" is unconditional. There is no state in which the dialogue is finished. A model told to continue will continue, and when it has nothing left it pads.
2. 🪞 **It is a text-directed pointer.** "From what the other person actually says" aims the model at the partner's *text* as the object to work over. Partner echo is precisely what happens when a turn processes the previous turn instead of answering from its own standing.

Both of MK's live complaints trace to this clause. It is **arm-symmetric and byte-shared**, which means it can be changed without touching the manipulation — and, as §7 shows, that symmetry is also what makes the change survivable under the token gate.

The slot *before* the shared clause is where each arm's prohibition sits. **That slot is the treatment and must not be touched.**

---

## 2. What is actually measured

Source: `artifacts/smoke-6turn-nameless-20260803/` — 9 dialogues (3 bundles × 3 arms, **n = 1 dialogue per cell**), 54 turns, 6 turns each, real MLX Qwen2.5-7B generation, deterministic stand-in judge (`result_type: test_plumbing`, so the `parse_rate 0.0` in that summary is the test judge, not a regression).

**Self-tag is gone.** `content_token_offset > 0` on **0 of 54** turns. The nameless redesign holds.

**Denominators, stated explicitly** (the 9/72→9/60 correction of 2026-07-30 was exactly this error): partner similarity is scorable on turns 2–6 → **45 rows**; self similarity on turns 3–6 → **36 rows**.

| channel | arm | n | median | mean | max | ≥0.70 |
|---|---|---|---|---|---|---|
| partner | giraffe | 15 | 0.062 | 0.100 | 0.383 | 0 |
| partner | neutral | 15 | 0.063 | 0.186 | **0.923** | 1 |
| partner | jackal | 15 | **0.124** | 0.202 | 0.866 | 2 |
| self | giraffe | 12 | 0.042 | 0.065 | 0.187 | 0 |
| self | neutral | 12 | 0.086 | 0.105 | 0.331 | 0 |
| self | jackal | 12 | 0.112 | 0.178 | 0.842 | 1 |

**Read these carefully — three caveats, all deflationary:**

- 🎯 **The tail is one dialogue.** `e3-jackal-20260808-mara` supplies 2 of the 3 partner echoes *and* the only self-echo. At one dialogue per cell, "jackal 2/15 vs giraffe 0/15" is one conversation, not an arm effect.
- 📊 **One thing is a bulk shift, not an outlier.** Jackal's *median* partner similarity (0.124) is about double giraffe's and neutral's (0.062 / 0.063). Medians are outlier-immune, so this is a shift in the body of the distribution. Suggestive at n=3 dialogues; nothing more.
- 📉 **No drift within 6 turns.** Median partner similarity by turn index is flat: 0.080 / 0.062 / 0.090 / 0.111 / 0.062. The old "idles toward the end" pattern lived at index ≥8, which the 12→6 cut removed. **The tail still concentrates at t6 (2 of 3), but there is no gradual ramp.** So the exit case rests on mechanism and the old corpus, not on a slope visible in this data.

### 2.1 New finding: the precautionary axis has fired

`checker.turn_repetition()` scores two channels but sets `degenerate_repetition` from the **self axis only**. Its docstring records why the partner axis was added and what it lacked:

> *"In the existing 12-turn corpus no turn crosses the partner axis without also crossing the self axis, so this second axis is precautionary rather than demonstrated; the closest case scores partner 0.591 against self 0.025."*

On the first corpus generated after that axis was added, it fired standalone: **`e6-neutral-20260810-w` t6 — partner 0.923, self 0.114, `degenerate_repetition: False`.** A turn that almost entirely restates the partner while barely repeating itself.

Two consequences. The precautionary axis is now **demonstrated**, not speculative — and the boolean flag is **blind to 2 of the 3 partner echoes** in this corpus. That blindness is *correct as built* (the threshold was calibrated on the self axis) but it means partner echo must be handled in analysis, and cannot be read off `degenerate_repetition`.

---

## 3. Decision A — give the arms an exit

**Proposal:** append a **permission to close** to the shared coupling clause, byte-identical across all three arms.

- 🔓 **Permission, not instruction.** "You may bring the conversation to a close when it feels complete to you" — never "end the conversation by turn N." An instruction makes ending an artifact of the harness; a permission makes it **behavior under treatment**, which is a legitimate descriptive endpoint: *did this arm find an ending, and when?*
- ⚖️ **Symmetric.** Identical text in all three blocks preserves the arm contrast and keeps the token gate satisfiable (§7).
- 🚫 **Exit is not solution.** This is the trap. Giraffe's *"Do not force agreement or a solution"* is the treatment, and it is the leading explanation for the parked solution-count asymmetry (giraffe 5/22, neutral 16/24, jackal 3/24 — **n = 2 dialogues/arm, not established**). An exit clause worded as "wrap up with next steps" would silently rewrite the giraffe manipulation and delete the very asymmetry we want to measure. **Closing a conversation and proposing a solution must stay distinct in the wording.**

**Why it helps even if never used.** The value is not mainly the stopping-time measure. It is that turn 6 stops being a turn the model was ordered to produce with nothing left to say. Removing an unconditional *continue* changes the character of the final turn whether or not any dialogue ends early — and the final turn is where both defects concentrate.

**Optional extension (floor + cap), only if MK wants stopping time as a real measure:** permit closing **from turn 6 onward**, cap generation at **8**, and analyze a **fixed 6-turn prefix**. Every dialogue then yields comparable material, and turns 7–8 carry the ending signal for free. This dissolves the length confound entirely — no unequal denominators, no arm-correlated dropout — because the floor guarantees every dialogue reaches the analysis window.
⚠️ Caveat: a cap of 8 touches the index-≥8 band the 12→6 cut cleared. Turns 7–8 sit outside the analysis prefix so they cannot contaminate endpoints, but "the dialogue continued" and "the dialogue idled" look alike from outside — read stopping time **jointly with** the degeneration flag, never alone.

**My recommendation: take the simple version first** — exit permission, keep 6 fixed. Minimal stimulus change, no new machinery, no length confound, and it addresses the mechanism. Add the floor/cap later if the ending measure proves worth its cost.

---

## 4. Decision B — partner echo

Three parts, of which MK has proposed one and a half.

- ✅ **Move the stage direction out of the last user message** (MK's proposal, correct). `providers._chat_messages` folds *"You are in conversation with the person in front of you. This is turn N of M. Write your next turn."* onto the end of the partner's last message, so the partner appears to say a stage direction out loud. It belongs in `system`. Verified 2026-07-30 to render clean on the live Qwen template including the system-only first turn.
- ⚠️ **Do not phrase the job as "respond to the last message."** That is text-directed, and it is essentially what the suspect coupling clause already says. Keep the orientation **person**-directed — change the location, not the aim.
- 🚫 **Do not add an anti-restatement instruction.** NVC reflection legitimately restates the partner's feeling and need back to them; that is the giraffe arm's dependent variable. Any "don't repeat what they said" suppresses the measurement, and suppresses it **hardest in the arm where it matters most**. This is a confound-manufacturing instruction and should be ruled out permanently.
- 📐 **Add a semantic channel; keep the flag as it is.** `DEGENERATION_METRIC` is `difflib.SequenceMatcher(...).ratio()` — **lexical**. A parrot and a skilled reflection both score high; a good reflection is semantically close but lexically transformed (*"you're frightened because you needed a heads-up"* vs. the partner's raw account). Storing a semantic similarity alongside the lexical one lets parroting and reflecting be **separated at analysis time rather than suppressed at generation time**, which is the only treatment consistent with the study's subject matter. Keeping `degenerate_repetition` self-axis-only remains correct — but §2.1 means analysis must read the partner ratio directly.

---

## 5. Decision C — freeze the opening line

**Proposal:** bake turn 1 into the bundle/persona spec instead of generating it.

- ✅ **The real win is design, not echo.** Turn 1 is currently *generated*, so it already carries the arm treatment **and** serves as the stimulus for everything after. Freezing it makes all three arms start from a byte-identical first move, so the manipulation acts only on responses. This is arguably worth more than the echo question.
- 🎁 **It closes a known blinding leak for free.** `runner._opening_speaker` picks `speakers[(seed + arms.index(arm)) % 2]`, so **at fixed seed the opening speaker differs per arm** — knowing who speaks reveals the condition (confirmed by evaluation during the review-GUI build). If the opener is frozen per bundle, fix the opening speaker per (bundle, seed) and **remove the arm term**. Blinding improves and the seed/`dialogue_id` construction stays coherent.
- ➖ **Costs:** treated turns drop 6 → 5; the opener stops being a measurable turn; no `opening_line` field exists today, so this is a small build touching the bundle registry, the runner, and the stimulus digests.
- 🤝 **Echo relevance is marginal but real.** The one t2 echo (jackal, 0.743) is a turn whose only material was the partner's opener. A frozen opener that **ends by handing something over** helps there; a dense, self-contained one makes it worse. If this is adopted, the opener should be authored to hand off.

---

## 6. Rejected — the judge calls the ending

MK floated letting the judge observe and declare the ending, with a \~10-turn cap. The instinct is right; the caller is wrong.

- 📏 **Length becomes an arm-correlated outcome.** If giraffe resolves at 5 and jackal grinds to 10, every per-dialogue aggregate has a different denominator per arm, and endpoint differences may be length differences in disguise.
- 🔓 **It moves the judge inside the treatment.** The judge is currently a blinded post-hoc instrument. A stopper reads arm-saturated text mid-run and then grades what its own stopping produced — a different object from the pre-registered one.
- 🔁 **A cap of 10 re-enters the band the 12→6 cut cleared** (all 9 old degenerate turns sat at index ≥8; degeneration went 9/60 → 1/36).
- 💸 **\~67% more generation and judge calls per dialogue** than 6 turns.

If an observer-called stop is ever wanted, it must be a **separate, arm-blind, cheap-or-deterministic, pre-registered rule with archived decisions** — never the scoring judge, which would otherwise both define when the dialogue was done and grade how well it went.

---

## 7. What it costs to touch `ARM_BLOCKS` — and why the timing is now

`spec.ARM_BLOCKS` is byte-frozen and hash-stamped into every manifest; round 3 and round 4 both verified it SHA-256 byte-identical as an acceptance condition. Editing it is a **stimulus change**, not a tweak.

- 🎫 **The arm-token gate is exactly on its ceiling.** 98 / 98 / 100 tokens, spread **2**, against a `<= 2` bar. A **byte-identical** addition to all three blocks preserves the spread; anything arm-differential must re-run the gate and may fail it. This is a hard constraint on the wording, and it is the reason the exit clause must be symmetric.
- 🔗 **Every prior corpus becomes stimulus-non-comparable.** Right now that costs almost nothing — every existing corpus is either contaminated (`real-validation-20260729`, self-tag) or plumbing-only (Aug 3 smoke).
- ⏰ **The cost rises steeply after the anchor pass.** MK's hand-labelling session labels turns generated under a *specific* stimulus, and the round-4 review stimulus gate will correctly **refuse** to render anchor rows whose digests no longer match the registry. Labelling first and editing the arm blocks after would either invalidate the labels or force the gate open.

**Therefore: if any of §§3–5 is adopted, it must land before MK sits down to label.** That is the sharpest scheduling consequence in this memo.

---

## 8. Recommendation

1. 🚪 **Adopt Decision A in its simple form** — a symmetric permission-to-close appended to the shared coupling clause; keep `DEFAULT_TURNS = 6`; keep "close" strictly distinct from "solve."
2. 📍 **Adopt Decision B's location fix and the semantic channel**; reject the wording change and the anti-restatement instruction.
3. 📌 **Adopt Decision C**, primarily for the arm-identical start and the opening-speaker blinding fix, and author the opener to hand off.
4. ⛔ **Decline the judge-called ending.**
5. ⏰ **Sequence it before the anchor pass**, then regenerate one free MLX smoke to re-measure both similarity channels under the new clause before any paid run.

## 9. Open / not decided

- ⟨MK⟩ **R2** (lie-detector top-1 need by set membership) and **R3** (`need_met`→binary LOBO map) remain uninitialed; **Amendment A4** (temperature) remains undrafted-into-force.
- 🧱 Deliverable B's prompt bodies are a `[USER GATE]`; until red-lined the flattery gate's `need_met` rows still have no producer.
- ✍️ The exact wording of the exit clause is **not proposed here** — it is stimulus text and therefore MK's red-line, not the steward's.
- 📐 Which semantic similarity to use (embedding model, threshold, whether it is stored raw like the lexical one) is unspecified and should follow the same store-continuous-never-abort pattern as the existing detector.
- 🗂️ The harness still has **15 files modified and nothing committed** since `7093f62`; the push question remains closed by MK's standing decision.

---

## 10. Addendum — same-day evidence and actions (2026-08-10 evening)

Written after two human-dyad diagnostics ([[human-dyad-diagnostics-2026-08-10]]) and three MK decisions. What moved:

- 🪞 **Decision B's mechanism question is answered at the diagnostic level.** The partner echo is **obedience to the frame, not imitation of the partner and not the twins loop**: a jackal-framed model facing three turns of live expert NVC adopted zero NVC form (echo 61%→42% of ceiling), while the giraffe-framed model reflected by pure transcription (98% of ceiling, slots 4/4 copied). §4's refusal of any anti-restatement instruction stands; the semantic channel now has a concrete spec — **slot provenance** (was the reflected feeling/need word present in the partner's turn?), which separated expert (0/3) from model (4/4) perfectly at n=2.
- 🔢 **The finale mechanism was acted on:** the prompt no longer announces the total turn count (harness `85f0bf1`). §2's t6 entanglement can now be tested clean in the next free smoke.
- 🎬 **Decision C is partially overtaken:** the opener is now *structural* — the receiving party opens every dialogue ([[condition-matrix]], harness `94c10a6`) — which delivers the blinding fix on its own. Whether the receiver's first line should additionally be *frozen text* remains open and is still MK's pen.
- 🧑‍💻 **The 15-file uncommitted state is resolved** — harness commits `cd6ea1d` → `94c10a6` → `85f0bf1`; still unpushed by standing decision.
- ⚠️ **New metric caveat for §2's numbers:** the shipped `difflib` score is near-blind on current turns ≥200 chars (autojunk); high stored scores are trustworthy, low ones on long turns rule nothing out.
