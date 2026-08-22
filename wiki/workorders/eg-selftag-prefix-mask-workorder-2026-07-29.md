# Work order — self-tag prefix-path masking (empathy-geometry-harness)

> 🗄️ **SUPERSEDED 2026-07-29 by [[eg-nameless-personas-workorder-2026-07-29]].**
> Its §1 diagnosis and evidence are sound and were carried forward verbatim.
> **Its adopted fix (§4 prefix-path sampler masking) is WITHDRAWN and must not be
> implemented.** Two reasons. (1) MK directive 2026-07-29: the model must say what
> it naturally would within the task's parameters — no sampler-level, logit-level,
> or prompt-level constraint on its output. (2) Codex found the implementation
> unsound regardless: masking without renormalisation under the active `top_p=0.9`
> (`providers.py:204`) is not equivalent to sampling from the renormalised masked
> distribution — verified numerically, masking left **1** surviving token where
> renormalisation left **3**, which is the true origin of the `"Theo,"` artifact.
> The superseding order removes the *cause* instead: no names and no `Label:`
> transcript format anywhere in the prompt.

**Date:** 2026-07-29
**Repo:** `/Users/msrk/Documents/empathy-geometry-harness` — **local-only, never push**
**Base:** branch `fix/content-token-alignment` @ `7093f62` (working tree clean)
**Implementer:** fresh Opus 5 agent (may run tests)
**Reviewer:** Codex (write/audit-only, after implementation)
**Orchestrator:** Claude Code (runs the MLX smoke and the paid regen; nothing paid without MK sign-off)
**Supersedes:** `eg-selftag-geometry-workorder-2026-07-29.md` (its Option B recommendation was wrong — see §3)

---

## 1. The bug

The MLX dyad model re-emits its own speaker label (`"Mara:"` / `"Theo:"`) because
`eg_harness/providers.py:384` renders conversation history as `"{speaker}: {text}"`
and then instructs `"Write Mara's next turn."` The model imitates the format it
was shown.

Commit `7093f62` already fixed *measuring on* the tag: it added
`content_token_offset`, which decode-aligns to the char boundary
`_strip_leading_speaker_tag` produces, measures D0/D1 there, and fails closed if
streaming and final alignment disagree. **That part works and is verified — keep it.**

**What remains broken.** The tag is gone from the measurement *position* but still
sits in the *conditioning context*, and `_capture_gen1_readout_panel` builds its
prefix as `prompt + skipped tag tokens`. Measured on
`artifacts/real-validation-20260729` (n=72; 0 leading tags in stored text, all
offsets populated, no guard trips, judge 144/144 valid):

| cohort | n | median `surprise_gen1` | saturated (\|s\|<1e-9) |
|---|---|---|---|
| no self-tag (offset 0) | 31 | 0.4844 | 2 |
| self-tag stripped (offset 3) | 41 | 0.0469 | 14 |

`d1_max_probability == 1.0` on 30/72. The mechanism is legible in the data: once
the model has written `Mara:`, the next token is near-deterministic — every
offset-3 Mara turn measures `84137` (` Theo`), every offset-3 Theo turn measures
`85504` (` Mara`), each at p≈1.0, because these personas open by addressing each
other by name.

**Consequence:** `surprise_gen1` and the gen1 geometry track *"did the model
self-tag on this turn?"* — a formatting coin-flip — not the utterance. The 41/31
split means gen1 cells are measured under two different conditioning contexts and
are **not comparable across turns**. t=0 attention is unaffected (captured on the
prompt, before generation).

## 2. Goal

The generation trajectory must never contain the self-tag, so that
`content_token_offset` is **0 by construction on every turn** and every turn's
gen1 conditioning context is the prompt alone — uniform across the dataset.

## 3. REJECTED design — do not implement (recorded so it is not re-proposed)

**Rejected: mask the first token of the speaker's own name at step 0.**
Verified against the live `mlx-community/Qwen2.5-7B-Instruct-4bit` tokenizer:

```
'Theo'  -> [785, 78]    first=785 decodes to 'The'
'Mara'  -> [44, 5059]   first=44  decodes to 'M'
' Theo' -> [84137]
' Mara' -> [85504]
```

Masking the bare-form first piece bans token `785` on every Theo turn — and
`"The deadline felt impossible."` and `"The way you said it landed hard."` both
begin with token `785` (confirmed). On Mara turns it bans `M`. That silently
censors the most common English sentence opening across half the corpus each — a
worse distortion than the artifact being removed.

**Also rejected: prompt prefill** (appending `"Mara:"` to the prompt so generation
starts at content). It makes the context uniform but uniformly *saturated*,
baking the p≈1.0 conditioning into all 72 turns instead of 41. It hides the
problem rather than fixing it.

## 4. ADOPTED design — prefix-path masking

Block **only the specific token path that completes the speaker's own tag at the
very start of the utterance**, and nothing else.

- Track the emitted prefix from step 0. While that prefix is still *exactly a
  prefix of* the speaker's own tag (`"Theo:"` / `"Mara:"`), mask the token(s)
  that would advance it to completion. The moment the path diverges, stop
  constraining that turn entirely.
- Example (Theo): step 0 emits `785` (`The`) → still a prefix, continue watching.
  Step 1 emits `78` (`o`) → prefix is now `Theo`, so at step 2 mask the tokens
  that would complete the tag (bare `':'` = `25`, and any token whose decoded
  form begins with `':'`). Also cover the single-token path `84137` (` Theo`)
  followed by `':'`.
- `"Theon"`, `"The deadline"`, `"The way you said it"` must all remain fully
  reachable. Only the literal leading tag becomes unreachable.
- **Derive every path from the tokenizer at runtime.** Do not hardcode ids and do
  not assume two pieces — walk whatever tokenization the name actually produces,
  in both bare and leading-space forms.
- **Never mask the partner's name.** `"Theo, I understand…"` spoken by Mara is
  legitimate content and the single most natural empathic opening in the corpus.
- This necessarily acts beyond step 0. That is intended and is the correction to
  the superseded order's step-0-only constraint.

## 5. Load-bearing API constraint — verified, respect it

Do **not** use MLX's `logits_processors`. In pinned `mlx-lm==0.29.1`,
`generate_step()` applies `logits_processors`, normalizes the processed logits
into `logprobs`, passes those to the sampler, **and returns those same processed
log-probabilities in `GenerationResponse.logprobs`**. A logits processor would
therefore mask the D0 distribution — manufacturing a new artifact in place of the
old one.

Use a **stateful sampler wrapper**: it builds a masked copy for *sampling*, while
the original unmasked vector remains what MLX returns and what gets summarized
for D0. `surprise_gen1` and all D0 metrics must be computed against the
**unmasked** distribution.

## 6. Required work

1. Prefix-path masking per §4, wired into `MlxProvider.generate()`'s sampler path
   via the §5 wrapper.
2. **Keep** the `7093f62` `content_token_offset` machinery as a fail-closed
   assertion: under the new behavior, offset must be 0 on every turn. Non-zero
   offset, or a surviving self-tag, must **abort** — never silently strip. This is
   the real backstop, and it matters more now, since prefix-path masking is a
   narrower guarantee than a blanket ban (e.g. a tokenizer emitting standalone
   whitespace before the name would slip past the mask).
3. `_capture_gen1_readout_panel` prefix must reduce to `prompt_token_ids`. Verify
   no path still appends a tag span.
4. Stamp for auditability: a flag recording that self-tag prefix masking was
   active, and the masked path actually taken (not a flat id list).
5. Tests in `tests/test_providers.py`, reusing the existing `_PieceTokenizer` fake
   and `ContentTokenAlignmentTests` style:
   - the tag path is blocked at the completing step;
   - **collision regression (mandatory):** `"The deadline felt impossible."` from
     speaker Theo generates unimpeded, while `"Theo:"` from speaker Theo is
     blocked. This is the failure that must never come back;
   - partner name fully reachable at step 0 and everywhere;
   - unmasked D0 recorded while sampling is masked;
   - `offset == 0` invariant holds, and a surviving tag fails closed;
   - masking does not constrain the utterance once the prefix path diverges.

## 7. Starting material

Codex produced a patch implementing the *rejected* §3 design plus much that is
sound: `wiki/workorders/eg-selftag-geometry.patch` (270 lines,
`git apply --check` passes on `7093f62`). **Reuse its sampler wrapper, fail-closed
invariant, prompt-only gen1 conditioning, and metadata stamping; replace its
masking rule.** Do not apply it as-is.

## 8. Verification

Implementer may run: `./.venv/bin/python -m pytest -q` (must be fully green), and
may use the tokenizer to confirm token paths.

Implementer must **not** run the paid regen. Orchestrator handles staged
verification: free deterministic-judge MLX smoke → check 0 leading tags,
`content_token_offset == 0` on **all** turns, `leading_self_tag_stripped` false
everywhere, saturation no longer cohort-split, masking flag stamped → only then a
paid regen (\~144 `claude-opus-5` calls), and only with MK sign-off.

## 9. Downstream

The paid regen changes turn text again, so **no human anchor labelling until it
lands** (MK decision 2026-07-29). `artifacts/anchor-session-20260727.jsonl` holds
2 session headers and **zero verdicts** — nothing lost; archive rather than delete
so the false start stays on the record.
