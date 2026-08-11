# EG instrument round — MK's five orders (2026-08-10)

**Status: 4 of 5 landed; order 5 (pilot batch) running.** Issued by MK after the mixed-dyad pilot ([[../empathy-geometry/mixed-dyad-pilot-2026-08-10]]) and the faux-feeling correction. Harness commits `d031d96` (instruments) on top of `69d7048` (per-speaker arms); 401 tests green. Everything below is instrument/judge-side — zero stimulus bytes moved, no digest changed except the manifest gaining new read-only stamps.

## The orders

1. ✅ **"Why don't we add the who's-who check."** → `checker.role_integrity()`: per-bundle role anchors — (owner, pattern, label) first-person claims the registered event assigns to one party; a turn violates when the other speaker matches. Read-only stored fields, never aborting, anchor lexicon content-hashed into the manifest. Fixture-tested against the pilot's actual swap sentences (Mara's "without my input" theft, Theo's "I made the changes" confession, Mara's absorbed "I saw the changes in the morning"). Known v1 misses, documented: second-person hand-offs, quotes/negation. Spec: [[../empathy-geometry/grammar-spec]] §Role integrity.
2. ✅ **"Add unvalued to the list."** → `spec.FAUX_FEELINGS` + the grammar-spec faux lexicon, with the MK-ruling comment. `isolated` left unruled (flagged as borderline, MK's pen).
3. ✅ **"Check on how the NVC rules are being passed into the model."** → prompt audited from the pilot artifact's stored `prompt_text` (ground truth, not reconstruction). Composition per turn: persona profile → shared event → conversation frame (the arm block verbatim, byte-frozen, token-gated 98/98/100) → "Speak only as yourself…" scaffold → role-structured transcript (partner turns as `user`, own as `assistant`, **no names or letters anywhere in the history**) → "This is turn N." Two audit findings: (a) `HISTORY_WINDOW_TURNS = 8` ≥ 6-turn dialogues, so **the role swaps happened with the full transcript in view** — not a truncation artifact; (b) after the nameless redesign, speaker identity in the transcript rests **entirely on chat roles plus the M/T letters in the persona/event text** — the theft turn's prompt contained everything needed to answer correctly (her own card material included), and the model took the partner's material anyway. Elicitation/stability, not information.
4. ✅ **"Fix the judge."** → hearing provenance: every hear event records, per judge-matched card-need term, whether the heard party had previously self-stated it (word-bounded exact term) → `basis` ∈ inferred / restated / unscorable; dialogues carry `t_hear_basis` per chair plus the strict endpoint **`dyadic_t_hear_inferred_only`** (all chairs inferred, no crediting event on a role-violating turn). **Both rates always reported side by side — which is confirmatory is a prereg decision.** Loosening bias documented (exact-term self-statement matching over-counts inference); v2 tightening named. Spec: [[../empathy-geometry/grammar-spec]] §Hearing provenance.
5. 🔄 **"Several more pilots… flesh it out before we start the experiment."** → 14-dialogue batch launched (B2, 6 turns, seeds 20260812–13, twins vehicle, **real MLX Gemma judge** so hear events are real): all 7 pairings — G×J and J×G (2 more seeds each), **G×N and N×G (first neutral-mixed runs, MK's original suggestion)**, and same-frame G-G / N-N / J-J with the new instruments live. Artifact will land at `empathy-geometry-harness/artifacts/mixed-pilot/fleshout-2026-08-10/`. Analysis owed: role-violation and provenance-basis rates per pairing, same-frame baselines for both, jackal-melt replication, G×N behaviour.

## Open MK decisions (unchanged by this round)

- 🖊️ Giraffe block wording (two-moves framing now on the table)
- 🚪 ARM_BLOCKS exit clause (dialogue-shape memo Decision A)
- 🧩 Whether any mixed cell enters the condition matrix (evidence says: not without the who's-who check proving out; matrix deliberately unedited)
- 🏷️ `isolated` faux ruling

## Verification

401 tests green (14 new this round: role anchors on real pilot sentences, provenance matching, unvalued, runner integration). Same-arm digests unchanged by construction (byte-identity test). Batch launched exit-pending.
