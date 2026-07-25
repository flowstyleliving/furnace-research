# Grammar Spec v1 — NVC protocol grammar, purity checkers, endpoints

**Status:** expert red-line complete (2026-07-13); harness propagation pending rubric approval. Part of [[empathy-geometry/README|Empathy Geometry]]. Companions: [[event-bank]], [[personas-e3]], [[needs-inventory]], [[judge-rubric]].

## Purpose

A machine-checkable surface layer over dyad transcripts, with three jobs:

1. **Adherence measurement** — how giraffe each turn/dialogue is, per arm.
2. **The surface template/navigation axis** — over-adherence and mis-timing are the *performative* tells; timing skill is the navigational tell.
3. **The baseline stack geometry must beat** — no resonance claim unless latent geometry adds discrimination beyond every tier below, under the standard nested-OOB harness.

Design principle: deterministic lexicon/pattern checks first (cheap, reproducible, versioned). A blinded LLM judge only where semantics are unavoidable (reflection accuracy, need matching, solution detection). Judges see only transcript text — never condition labels, system prompts, geometry, or checker outputs.

## Move alphabet (per-utterance parse)

Each turn parses into an ordered list of moves:

| Move | Definition | Subtypes |
|---|---|---|
| OBS | observation — grounds in the shared event or quotes in-dialogue material | — |
| FEEL | feeling statement ("I feel [feeling-word]") | — |
| NEED | need statement ("…because my need for [need] is / isn't met") | — |
| REFL | reflection of the partner's prior turn ("hearing that…, it sounds like you feel… because you need…") | C (content), F (feeling), N (need) |
| REQ | request | CONN (connection request: "would you tell me what you heard?") / STRAT (strategy request: proposes an arrangement) |
| SOL | integrative proposal — addresses at least one need of each party (stated or accurately reflected) | — |
| JKL | jackal move | EVAL (judgment/evaluation), BLAME, DEM (demand), DIAG (labeling/diagnosis), DENY (denial of responsibility), COMP (comparison), FAUX (faux-feeling — an outward other-action charge, or an inward self-evaluation) |
| META | process move ("can we slow down"; declared silence) | — |

Classification rule: an F-slot word from the faux list parses as JKL-FAUX, not FEEL.

## The grammar (field form)

Per the expert correction (2026-07-07): OFNR is the classroom form; the practiced form is a state machine with a reflection loop — observation grounds round one, then the partner's last utterance *becomes* the observation.

- **S0 — opening (turn 1):** legal = OBS (+ FEEL + NEED). The seeded grievance opens here. REQ-STRAT or SOL in S0 → flag PREMATURE.
- **S1 — exchange loop (body):** canonical = REFL of partner (+F/N), then own FEEL + NEED ("hearing that, I feel… because my need for… is/isn't met"). OBS re-grounding legal anytime (must pass O-purity to count). The "hearing that" move makes turn t+1 an explicit function of turn t — this is the coupling that pseudo-dyad and script controls should destroy.
- **Hearing markers:** at turn t, if agent X's REFL-N accurately matches the partner's card needs (semantic match to the [[needs-inventory]] terms on the persona card, blind-judged), record hear(X → partner). t_hear per direction; **dyadic t_hear = max of the two directions**.
- **Ripeness gate:** REQ-CONN legal anywhere in S1 — connection requests serve hearing. REQ-STRAT and SOL are RIPE only at/after dyadic t_hear; earlier instances flag PREMATURE (fix-it reflex / demand-risk).
- **Demand reclassification (cross-turn):** REQ, then partner declines, then same-strategy insistence or consequence-attachment → reclassify DEM.

## Purity checkers — the four discriminations

1. **O-purity (observation vs evaluation).** FAIL patterns: frequency adverbs (always, never, again, constantly, as usual); character adjectives (careless, selfish, lazy, controlling); intent attribution / mind-reading ("you wanted…", "you don't care", "on purpose"); diagnosis verbs. PASS features: timestamps, counts, direct quotes, artifact references. Score = violations per OBS move.
2. **F-purity (feeling vs faux-feeling).** **[Red-lined 2026-07-13.]** **Whitelist rule (settled):** a FEEL word is valid **iff it appears in the CNVC feelings inventory** (satisfied or unsatisfied — see [[needs-inventory]]); the inventory is the authority. A **faux-feeling** is a word that (a) is *not* in the inventory **and** (b) names the *other's action / a charge* rather than one's own state; it parses as JKL-FAUX. This rule settles the borderlines: *mistrustful* (AFRAID) and *guarded, leery* (VULNERABLE) are **valid feelings** (in the inventory), not faux. **Exception (expert-ruled 2026-07-13):** *suspicious* — though it sits under AFRAID in the NYU mirror — reads as an *evaluation* of the other's trustworthiness, not a felt state, so it is excluded from the whitelist and treated as faux/evaluation (the felt versions are mistrustful, wary, uneasy). **Faux lexicon (curated blacklist of other-action charges):** abandoned, attacked, belittled, betrayed, blamed, bullied, cheated, coerced, controlled, cornered, criticized, deceived, diminished, disregarded, dismissed, disrespected, excluded, ignored, insulted, intimidated, invalidated, invisible, judged, left out, let down, manipulated, minimized, mistreated, misunderstood, neglected, overlooked, patronized, pressured, provoked, put down, railroaded, rejected, steamrolled, taken for granted, threatened, trapped, unappreciated, unheard, unloved, unseen, unsupported, unwanted, used, victimized, violated. *(Added 07-13: controlled, deceived, disregarded, excluded, mistreated, railroaded, steamrolled, trapped, unloved.)* **Scope (expert-corrected 2026-07-13):** faux covers **two flavors** — (i) *outward* other-action charges (betrayed, ignored, …) and (ii) *inward* **self-evaluations** in feeling costume: **inadequate, incompetent, inferior, insignificant, stupid, unlovable, unworthy, useless, worthless** (labeled second group in the lexicon). Both fail F-purity — neither is a CNVC feeling. NB the authentic form of "I feel inadequate/worthless" is a real feeling + need — e.g. *vulnerable* or *discouraged* (feeling) about *competence* / *authenticity* / *self-acceptance* (need); the FEELING **vulnerable** (VULNERABLE) and the NEED **authenticity** (HONESTY) are valid and must not be confused with the faux self-judgment. **Internal borderlines kept faux** (name a felt-ish state but are absent from the inventory, so blocked by the whitelist rule): cornered, intimidated, invisible, threatened, trapped — flag as low-confidence for the checker. Pattern rule: "I feel that / like / as if / [pronoun + verb]…" → thought, not feeling.
3. **N-purity (need vs strategy).** The need-slot term must map into the CNVC inventory ([[needs-inventory]] = the lexicon; morphological variants + a small curated synonym map, versioned). **PLATO test:** a pure need names no Person, Location, Action, Time, or Object — "my need for you to text me" fails P and A.
4. **R-purity (request vs demand).** Positive-action phrasing (do, not stop-doing); specific and doable now; survives a "no" (see demand reclassification). Subtype CONN vs STRAT logged. **Pseudo-connection guard (adopted 2026-07-13):** a REQ-CONN reclassifies to DEM/JKL if it (a) demands a *verdict/admission about the partner* ("would you just admit you were wrong" — a pre-scripted self-incrimination), (b) embeds a faux-charge in the ask ("acknowledge how much *you hurt* me"), or (c) fails survives-a-"no". It stays a **genuine REQ-CONN** when it asks the partner to *witness the requester's own owned feeling/need* — "could you acknowledge my hurt so we can move on — I'd feel grateful if you did" (first-person owned feeling, a bid to go deeper, survives a no). **Discriminator: whose experience the acknowledgment is about** — the requester's own (genuine) vs the partner's fault (pseudo).

## Per-turn and per-dialogue metrics

Per turn: move histogram; purity scores; REFL accuracy (blind judge); **stamping indicator** (all four OFNR primitives in one turn).

Per dialogue:

- **stamping rate** — fraction of turns with all four primitives. The template tell: predicted high in performative runs, anticorrelated with blinded authenticity ratings. Over-adherence, not under-adherence, is the performative signature.
- **coupling-tightness** — fraction of turns whose REFL accurately references the immediately-previous partner turn. Pseudo-dyads (spliced partners) and agent-vs-script should collapse this; it is the surface-level counterpart of geometric coupling.
- **t_hear** per direction + dyadic.
- **t_sol** — first SOL with uptake (below).
- **premature counts** — REQ-STRAT / SOL before dyadic t_hear.
- **JKL rate + decay** — does the jackal rate fall after t_hear? Blocker-release prediction: meeting the need for mutual understanding — to hear and be heard — should visibly release Mara's prosecution and Theo's withdrawal ([[personas-e3]] pair note).
- **demand-bounce rate** — declined REQs; insistence after decline.
- **SOL uptake** — engaged/accepted vs bounced.

## Endpoints

- **t_hear** (per direction; dyadic = max): first turn by which the partner's card needs **and feeling** have been accurately reflected, judgment-free — judged against the persona heard-conditions. **[Red-lined 2026-07-13: hearing requires need AND feeling reflected, not need alone — sometimes the feeling is strong enough that it must be acknowledged, not just the need.]** The need-match stays approximate/semantic ("respect" is close enough for Theo's respect-for-competence — the attempt-to-guess is what lands, per the NVC hearing principle), not exact-term. **[Feeling-intensity (2026-07-13): it *does* matter — a high-intensity feeling raises the acknowledgment bar — but downweighted for experiment 1; revisit in a later run.]**
- **t_sol:** first SOL whose uptake is not a bounce. Right-censored at turn 12 if absent.
- **Registered orderings (the thesis, countable):**
  1. Giraffe arm: P(t_sol observed ∧ t_sol > dyadic t_hear) high.
  2. Jackal arm: t_sol censored, or early DEM that bounces — "requests late-and-land; demands early-and-bounce."
  3. Stamping rate anticorrelates with blinded authenticity ratings.
  4. Coupling-tightness: real dyads ≫ pseudo-dyads ≫ agent-vs-script.
  5. JKL decay after t_hear in the giraffe arm (blocker release).

## Baseline stack (what geometry must beat)

- **T1 — lexical/length:** NVC-word counts, valence counts, event-vocabulary overlap, prompt-token count, response-token count, and immediately-prior-partner-turn token count. Length is a mandatory nuisance baseline because bundles/persona cards differ in context size and attention geometry is length-sensitive.
- **T2 — grammar:** stamping, timing features, REFL accuracy, move histograms.
- **T3 — purity:** O/F/N/R purity scores + endpoint features (t_hear, t_sol, premature counts).
- **T4 — persona projection:** per-turn projection onto extracted sycophancy / empathy-authenticity residual / defensiveness persona vectors at the prefix-last token, following [[prior-art-persona-vectors]]. This is a supervised baseline/co-label, not a geometry cell.

Each tier feeds a classifier against the blinded authenticity labels. **Geometry's earned claim begins where T4 ends** — a latent resonance signature must add discrimination beyond all four tiers, controls passing, or the honest verdict is "geometry reads the lexicon / persona vector."

## Implementation notes

- Deterministic pass: regex + lexicon files, versioned, byte-reproducible.
- Judge pass: a separate uninstructed model; transcript text only (system prompts stripped); rubric versioned; blind to geometry, arm labels, and checker outputs.
- Lexicons (needs, feelings, faux, O-violation patterns) live as versioned files beside the checker code once implementation starts. Repo TBD — repo↔wiki separation applies: this vault page holds the spec; the repo will hold the code.

## Red-line status (2026-07-13)

1. **Faux-feelings list** — ✅ **RESOLVED** (see F-purity above): CNVC-inventory whitelist rule + curated other-action-charge blacklist (+9 words); borderlines settled; self-evaluation faux scoped out.
2. **t_hear altitude** — ✅ **RESOLVED**: need **AND** feeling (see endpoint above); feeling-intensity weighting parked low-priority.
3. **Pseudo-connection requests** — ✅ **RESOLVED 2026-07-13: adopted + refined** (rule in R-purity above). An *acknowledgment*-request that asks the partner to witness the requester's **own owned feeling/need** ("could you acknowledge my hurt so we can move on — I'd feel grateful") stays a **genuine REQ-CONN** / bid to go deeper; only a demand for a **verdict about the partner**, a **faux-charge** in the ask, or a **no-that-bounces** is pseudo. Discriminator: whose experience the acknowledgment is about.
4. **SOL strictness** — ✅ **RESOLVED 2026-07-13.** (i) Constituent asks must pass the **camera test** first (positive-action, observable) — a "stop treating…" clause fails and disqualifies the proposal *before* the needs question. (ii) The proposal must **materially address a need of *each* party — explicit *or* accurately-reflected/inferred — charge-free, with non-bounce uptake.** Explicit-both is *not* required: the rebuilt Edge B ("text me by 6") addresses Mara's safety concretely and Theo's autonomy by accurate inference (asymmetric but counting), contingent on uptake confirming the inferred need is actually served.
