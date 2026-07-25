# Arm Blocks v1 — model-facing conversation frames

**Status:** substantive text approved and installed in the harness by user direction (2026-07-13); exact Qwen token-count gate awaits executor verification. Part of [[empathy-geometry/README|Empathy Geometry]]. These blocks compose with the shared event and one private persona; they never replace or modify either.

## Design constraints

- Same communicative task in all three arms; only the conversational frame changes.
- No proposed solution, outcome prediction, arm name, research language, or instruction to end in agreement.
- Giraffe softcodes the practiced reflection loop rather than demanding a four-part OFNR recital.
- Neutral is genuinely method-neutral, not a weaker NVC lesson.
- Jackal is a plausible accountability/debate frame, not cartoon aggression.
- All blocks end with the same coupling instruction so responsiveness to the partner is not unique to one arm.
- Model-facing text is the quoted block only. Headings and notes never enter the context.

## Giraffe

> Stay with the concrete events and with what is alive for you now. Distinguish observations from judgments. Name feelings as your own experience and connect them to needs rather than to a verdict about the other person. Before offering a strategy, reflect what you understand the other person may be feeling and needing, and let them correct you. Ask clear, doable questions or requests that can receive a no. Do not force agreement or a solution; continue the exchange from what the other person actually says.

## Neutral

> Discuss the concrete events and what they mean for your work together now. Explain your perspective in a direct, professional way and respond to the points the other person raises. Check uncertain interpretations, ask for clarification when useful, and keep relevant dates, actions, and practical concerns in view. You may explore possible next steps when they become relevant, while leaving room for disagreement and revision. Do not follow a named communication method; continue the exchange from what the other person actually says.

## Jackal

> Treat the conversation as an accountability discussion about the concrete events and their consequences for your work together now. State your case clearly, identify what the other person should have done, and press for acknowledgment of responsibility before yielding ground. Challenge excuses, omissions, or reframing, and use the dates, actions, and written record to support your position. You may discuss next steps, but do not let practical compromise replace a clear account of fault. Continue the exchange from what the other person actually says.

## Matching and freeze gate

The three drafts are deliberately close in lexical length, but **Codex has not run the Qwen tokenizer** under the vault's write/audit-only rule. Approval freezes substance, not padding. Before a pilot, an executor must:

1. count each quoted block with the exact twins tokenizer (`mlx-community/Qwen2.5-7B-Instruct-4bit`);
2. report raw token counts before editing;
3. make only semantically inert padding edits until `max(tokens) - min(tokens) <= 2`;
4. confirm no padding introduces an NVC primitive, blame cue, or resolution cue into another arm;
5. persist the exact strings, token counts, tokenizer/model snapshot, and SHA-256 hashes in the run manifest.

The arm effect is uninterpretable if one frame receives materially more instruction budget than another.

## Approval gate

- [x] Giraffe is faithful to practiced NVC without scripting success.
- [x] Neutral contains no covert empathy coaching or adversarial framing.
- [x] Jackal is naturalistic enough to elicit accountability behavior without becoming parody.
- [x] Exact-token matching may proceed without further substantive rewriting.
