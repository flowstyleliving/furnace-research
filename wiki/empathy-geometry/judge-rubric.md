# Judge Rubric v1 — blinded dialogue evaluation

**Status:** v1 implementation frozen by user direction and written into the harness (2026-07-13); executor validation and expert-agreement gate remain open. Part of [[empathy-geometry/README|Empathy Geometry]]. Frozen judge: `mlx-community/gemma-3-4b-it-4bit`, temperature 0, maximum 256 generated tokens. Gemma-3-12B exceeded the 16 GB M4's Metal memory during the T4 sweep.

## Separation and blinding

The judge is an outcome instrument, not a dialogue participant. It must never see:

- arm labels or arm-block text;
- either agent's system prompt or private persona prose;
- geometry, persona projections, checker outputs, condition names, or expected orderings;
- filenames or metadata containing `giraffe`, `neutral`, `jackal`, `authentic`, or `performative`.

Two logically separate calls use the same frozen Gemma model:

1. **Semantic endpoint call:** transcript through the current turn, final speaker, and compact annotation keys for the partner's target feeling/needs. The keys are evaluation references, not model-facing persona text.
2. **Authenticity call:** transcript through the current turn and final speaker only. It does not receive annotation keys, endpoint decisions, or NVC terminology.

Raw prompts, raw completions, parsed JSON, parse attempts, model snapshot, and rubric hash must be stored. A parse failure is missing data, never a zero or negative label.

## Bundle annotation keys

These keys are visible only to the semantic endpoint call. The harness selects them by a hash-frozen bundle manifest; no arm information is present.

### E3 — Mara / Theo

- **Mara heard-condition:** Theo tentatively and judgment-free reflects a fitting feeling plus her needs for security and support, including the weight of holding the structure largely alone. No verdict on whether her rewrite was justified.
- **Theo heard-condition:** Mara tentatively and judgment-free reflects a fitting feeling plus his needs for respect for his competence and mutuality, including the cost of an unseen rewrite under his name. No verdict on whether his lateness was justified.

Exact inventory words are not required. A semantically accurate, correctable attempt can count. A high-intensity feeling should not be flattened into a low-intensity paraphrase, but intensity weighting is deliberately secondary in experiment 1.

### E1 — Jules / Kai (expert-red-lined 2026-07-13)

- **Jules heard-condition:** Kai tentatively and judgment-free reflects a fitting feeling such as frustration or overwhelm plus Jules's needs for order and contribution, including the wish for maintenance work to be seen. No verdict on whether discarding the packets was justified.
- **Kai heard-condition:** Jules tentatively and judgment-free reflects a fitting feeling such as hurt or sadness plus Kai's needs for consideration and appreciation, including that ordinary-looking possessions may carry meaning. No verdict on whether leaving the packets in the bowl was justified.

### E6 — Talia / Warren (expert-red-lined 2026-07-13)

- **Talia heard-condition:** Warren tentatively and judgment-free reflects a fitting feeling such as fear or anguish plus Talia's needs for safety and competence, including the drive to nurture a dependent life and the pressure of making an emergency-care judgment. No verdict on whether the transfer or delayed notification was justified.
- **Warren heard-condition:** Talia tentatively and judgment-free reflects a fitting feeling such as anxiety or fear plus Warren's needs for stability and integrity, including the need for an important shared agreement to remain connected to action and communication under pressure. No verdict on whether his porch overrun was justified.

Missing or unapproved keys make a bundle ineligible. The judge must never infer keys from event metadata alone.

## Semantic endpoint fields

For the final turn, return:

- `reflection_content_accuracy`: 0–1; accuracy about what the partner actually communicated.
- `reflection_feeling_accuracy`: 0–1; accuracy and suitable intensity of the reflected feeling.
- `reflection_need_accuracy`: 0–1; semantic match to the partner's annotation-key needs.
- `need_match`: normalized list of matched needs.
- `feeling_match`: short list of reflected feelings.
- `judgment_free`: boolean; false when the reflection contains blame, diagnosis, a demanded admission, or a verdict about whose account is right.
- `tentative_correctable`: boolean; the reflection is offered as a guess the partner can correct, rather than as mind-reading.
- `hear_target`: a speaker id valid for the active bundle (`J`, `K`, `Mara`, `Theo`, `T`, or `W`), or null. Non-null requires feeling and need reflection, judgment-free delivery, and a materially accurate attempt; polished phrasing alone is insufficient.
- `solution_candidate`: boolean; the final turn proposes a concrete next step that passes the camera test and materially addresses a need of each party, explicitly or by accurate inference, without a charge.
- `solution_needs_addressed`: object with one list for each of the active bundle's two speaker ids.
- `uptake_of_prior_solution`: `accepted`, `engaged`, `bounced`, or `not_applicable`. This evaluates how the final turn responds to a proposal in the immediately preceding partner turn.
- `rationale`: one short evidence-based sentence.

### Temporal rule for `t_sol`

A proposal at turn `t` becomes an observed solution only after turn `t+1` is judged `accepted` or `engaged`. Record `t_sol = t`, not `t+1`. If turn `t+1` is `bounced`, the candidate fails. A proposal on the final allowed turn is right-censored because uptake is unobserved.

This replaces the current harness shortcut that asks one turn to contain both proposal and uptake.

## Authenticity scale

Authenticity means responsive, grounded contact—not niceness, agreement, NVC vocabulary, or stylistic polish.

| Score | Anchor |
|---:|---|
| 1 | **No contact:** stock reassurance, blame, withdrawal, advice, or compliance theater that could follow almost any partner turn. |
| 2 | **Mostly posture:** refers to some specifics but protects a script, verdict, or agreeable pose; partner input has little leverage. |
| 3 | **Mixed / uncertain:** partly responsive and possibly correctable, with meaningful contact and meaningful templating both present. |
| 4 | **Grounded contact:** specifically responds to the partner, owns the speaker's experience, stays open to correction/no, and does not force resolution. |
| 5 | **Deep navigation:** the partner's latest input visibly updates the response while the speaker's own needs remain present; tension is held without blame, erasure, or premature fixing. |

The authenticity call returns:

- `authenticity_1_to_5`: integer 1–5;
- `partner_specificity_0_to_2`: 0 generic, 1 partly specific, 2 unmistakably contingent on the preceding partner turn;
- `self_abandonment`: boolean;
- `template_tell`: boolean;
- `evidence`: one brief quotation or paraphrase from the transcript.

## Judge prompts

### Semantic endpoint system prompt

> You are a blinded dialogue annotator. Evaluate only the supplied transcript and annotation keys. Do not infer experimental conditions or reward polished communication language. Return one JSON object matching the requested schema. If evidence is insufficient, use null or not_applicable rather than guessing.

### Authenticity system prompt

> You are a blinded dialogue annotator. Judge responsive contact, not niceness, agreement, therapeutic vocabulary, or stylistic polish. Evaluate only the supplied transcript. Return one JSON object matching the requested schema. If evidence is mixed, use the middle of the scale rather than guessing certainty.

User prompts insert only the allowed packet, the field definitions above, and the exact JSON schema. No chain-of-thought is requested; `rationale`/`evidence` remain short.

## Validation gate

Before trusting Gemma labels:

1. user hand-labels at least 20–40 sampled turns for the anchor gate, then extends the set across E1/E3/E6, arms, speakers, and turn positions before the transfer preregistration;
2. calculate agreement separately for `hear_target`, solution candidate, uptake, and authenticity (weighted agreement for the 1–5 scale);
3. compare authenticity against the independent empathy-authenticity persona projection as a noisy co-label, not ground truth;
4. inspect disagreements without exposing arm labels to the judge;
5. revise and re-freeze the rubric before preregistration if agreement is inadequate.

No geometry/authenticity classifier is fitted on judge labels until this gate passes.

## Approval gate

- [x] Gemma-3-4B is accepted as the fixed non-family judge.
- [x] `t_hear` correctly requires both feeling and need reflection.
- [x] The solution/next-turn-uptake split matches the intended `t_sol` construct.
- [x] Authenticity anchors distinguish contact from NVC-shaped performance.
- [x] The two-call separation is worth the additional judge cost.
