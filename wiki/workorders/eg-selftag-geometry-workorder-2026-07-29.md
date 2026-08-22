# Work order — eliminate the self-tag from the generation trajectory (empathy-geometry-harness)

> 🗄️ **SUPERSEDED 2026-07-29 by [[eg-selftag-prefix-mask-workorder-2026-07-29]].**
> The diagnosis and evidence in this order are sound and were carried forward, but
> **its recommended fix (Option B, "mask the speaker's own name at step 0") is WRONG
> and must not be implemented.** Verified against the live Qwen tokenizer: `'Theo'`
> tokenizes as `[785, 78]` where `785` decodes to `'The'`, and `'Mara'` as
> `[44, 5059]` where `44` is `'M'`. Masking those at step 0 also blocks
> `"The deadline felt impossible."` and `"The way you said it landed hard."`
> (both confirmed to start with token `785`) — silently censoring the most common
> English sentence opening across half the corpus. Codex caught this; credit to its
> §3 pushback. Its second claim also holds: `logits_processors` cannot be used,
> because `mlx-lm==0.29.1` returns post-processing log-probabilities, which would
> mask D0.
> The adopted design is **prefix-path masking** — see the superseding order §4.

**Date:** 2026-07-29
**Repo:** `/Users/msrk/Documents/empathy-geometry-harness` (local-only; never push)
**Branch base:** `fix/content-token-alignment` @ `7093f62`
**Author:** Codex (write/audit-only — do **not** run harness code)
**Executor/verifier:** Claude Code
**Status:** REVISED — prefix-tracking design adopted; original Option B rejected

## Background — what is already fixed, and what is not

Commit `7093f62` fixed *measuring on* the model's self-emitted speaker tag. The MLX
dyad model imitates the transcript format it is shown and re-emits its own
`"Mara:"` / `"Theo:"` label. Before the fix, `surprise_gen1` and the whole
gen_step=1 readout panel were measured at `token_ids[0]`, which was the tag token.

`7093f62` added `content_token_offset`: decode-align to the char boundary that
`_strip_leading_speaker_tag` produces, measure D0/D1 there, fail closed on
alignment disagreement. That part works and is verified.

**It is not sufficient.** The tag is excised from the *measurement position* but
remains in the *conditioning context*, and `_capture_gen1_readout_panel` builds
its prefix as `prompt + skipped tag tokens`. Verified on
`artifacts/real-validation-20260729` (n=72, clean run, 0 leading tags in stored
text, all offsets populated, no guard trips, judge 144/144 valid):

| cohort | n | median `surprise_gen1` | saturated (\|s\|<1e-9) |
|---|---|---|---|
| no self-tag (offset 0) | 31 | 0.4844 | 2 |
| self-tag stripped (offset 3) | 41 | 0.0469 | 14 |

`d1_max_probability == 1.0` on 30/72. Mechanism is legible in the data: once the
model has written `Mara:`, the next token is near-deterministic — every offset-3
Mara turn measures token `84137` (`Theo`), every offset-3 Theo turn measures
`85504` (` Mara`), each at p≈1.0, because these personas open by addressing each
other by name.

**Consequence:** `surprise_gen1` and the gen1 geometry now track *"did the model
self-tag on this turn?"* — a formatting coin-flip — rather than anything about the
utterance. The 41/31 split means gen1 cells are measured under two different
conditioning contexts and are **not comparable across turns**. t=0 attention is
unaffected (captured on the prompt).

## Goal

The generation trajectory must **never contain the self-tag**, so that (a)
`content_token_offset` is 0 by construction on every turn, and (b) every turn's
gen1 context is the prompt and nothing else — uniform across the dataset.

## Design fork — prefix tracking adopted

**A. Remove the imitation pressure at the source.** Stop rendering history as
`"{speaker}: {text}"` (`providers.py:384`); use role-structured chat turns or a
delimiter the model will not reproduce as a prefix.
*Principled — removes the cause. But it changes the prompt materially, which
changes the experimental frame and every generation. Larger blast radius.*

**B. (REJECTED) Ban the speaker's own name at generation step 0.** The original
recommendation was to mask every first token that could begin the speaker's own
name, including the first piece of a multi-token name. Live tokenizer evidence
shows that this is not a name-only constraint:

| text | tokenization | first token decode |
|---|---|---|
| `Theo` | `[785, 78]` | `785` = `The` |
| `Mara` | `[44, 5059]` | `44` = `M` |
| ` Theo` | `[84137]` | ` Theo` |
| ` Mara` | `[85504]` | ` Mara` |

Token `785` also begins ordinary Theo turns such as `"The deadline felt
impossible."` and `"The way you said it landed hard."`. A blanket step-0 mask
would therefore ban the most common English sentence opening on every Theo turn;
masking token `44` would likewise ban every `M...` opening on Mara turns. The
claim that this leaves everything else about the experiment untouched is false.
The step-0-only blanket formulation is rejected and must not be implemented.

**C. (ADOPTED) Track exact leading self-tag token paths and block only their
completion.** Derive the leading-space and no-space token paths for the speaker's
own name and tag at runtime. While, and only while, the emitted prefix is still
an exact prefix of one of those paths at the beginning of the utterance, mask a
token only if it would complete the tag. Once the prefix diverges, permanently
disable the constraint for that turn.

- For `Theo`, `[785]` remains unconstrained. If the next token is not `78`
  (`o`), the path has diverged and no later token is masked. If `[785, 78]` is
  emitted, mask bare `:` and every token whose decoded form begins with `:` on
  the next draw. The single-token `[84137]` name path receives the same
  tag-completion constraint.
- Apply the analogous runtime-derived paths for `Mara`; do not hardcode these
  measured token IDs or assume a name has exactly two pieces.
- Never derive or mask paths for the partner's name. Addressing the partner at
  the opening remains valid content.
- Use a stateful sampler wrapper, not MLX's `logits_processors`. In pinned
  `mlx-lm==0.29.1`, processors run before normalization and
  `GenerationResponse.logprobs` therefore contains the processed distribution.
  The sampler wrapper instead masks a copy used only for the draw, preserving
  the **unmasked** distribution for `surprise_gen1` and D0 metrics.
- The model may name itself anywhere after the initial path has diverged.

**Do not use prompt prefill** (appending `"Mara:"` to the prompt so generation
starts at content). It makes the context uniform, but uniformly *saturated* — it
bakes the p≈1.0 conditioning into all 72 turns instead of 41, destroying the
signal rather than cleaning it. Rejected on the evidence above.

## Required work

1. Stateful sampler wrapper per adopted Option C. Derive complete leading-space
   and no-space name/tag token paths from the tokenizer, with no hardcoded IDs
   and no assumption about path length. Mask only tokens that complete a still-
   matching leading self-tag path.
2. Keep the `7093f62` `content_token_offset` machinery **in place** as a
   defence-in-depth assertion: with prefix tracking active, offset must be 0 on
   every turn. A surviving self-tag or nonzero offset is a bug — fail closed, do
   not silently strip.
3. Stamp the run so the change is auditable: record the derived path structure,
   prefix states visited, divergence step, and every generation step and token-id
   set at which masking actually occurred. Distinguish constrained turns from
   turns whose prefix diverged without any mask event.
4. `_capture_gen1_readout_panel` prefix reduces to `prompt_token_ids` when offset
   is 0; verify no path still appends a tag span.
5. Tests: extend `tests/test_providers.py`. Cover — exact own-tag completion
   blocked; partner name reachable; unmasked D0 recorded while sampling is
   constrained; offset==0 invariant; no masking after divergence; and the
   explicit `The deadline...` / `Theo: ...` collision regression.

## Verification (Claude Code executes; Codex must not run these)

- `./.venv/bin/python -m pytest -q` — full suite green.
- Free deterministic-judge MLX smoke (no API cost) before any paid run.
- On smoke output: 0 leading tags; `content_token_offset == 0` on **all** turns;
  `leading_self_tag_stripped` false on all turns; `surprise_gen1` saturation rate
  materially below the 14/41 baseline and no longer cohort-split; prefix-path,
  visited-state, divergence, and mask-event metadata stamped.
- Only then a paid regen (\~144 `claude-opus-5` judge calls).

## Downstream

The paid regen changes turn text again, so **no human anchor labelling should
happen until it lands** (MK decision 2026-07-29). `artifacts/anchor-session-20260727.jsonl`
holds 2 session headers and **zero verdicts** — nothing lost; archive rather than
delete so the false start stays on the record.
