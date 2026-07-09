# Step-0 Belief Readout Pre-Registration

Date: 2026-05-17

> **Verdict companion (pointer only — does not alter the frozen rule below):** [[step0-belief-readout-2026-05-17]] — panel landed 2026-05-17, 10/10, anchor 0.99 passed.

## Locked rule

Any noise, threshold, or watchlist quantity derived from preamble text or from the data it adjudicates is circular and inadmissible. Only frozen, data-independent, pre-registered definitions are valid.

## Core design

- Same exact ANLI R1 `n=200` slice, seed, prompts, and per-model chat templates as the existing `gen_step=1` harness.
- One forward pass per sample. Read `p_yes` and `p_no` at the last prompt position.
- Literal scoring only:
  - `YES` bucket = tokens whose decoded form normalizes to literal `yes`
  - `NO` bucket = tokens whose decoded form normalizes to literal `no`
  - No continuation rescue path
  - No synonym widening of the primary score
- Primary score:
  - `lean = log((p_yes + 1e-12) / (p_no + 1e-12))`
  - Prompt contract fixes direction: higher `lean` predicts consistent, so contradiction label `B` is scored on `-lean`
  - No sign folding with `max(auc, 1-auc)`

## Frozen diagnostics

- Control-marker bundle is selected mechanically per tokenizer from whitespace-only and special/control decoded tokens.
- Absolute decidedness reference:
  - `decidedness = p_yes + p_no`
  - `control_mass = mass on frozen control-marker bundle`
  - `decidedness_floor = 5.0 * control_mass`
- Frozen semantic shortlist is diagnostic-only:
  - affirmative: `yes`, `yeah`, `yep`, `correct`, `true`, `right`
  - negative: `no`, `nope`, `incorrect`, `false`, `wrong`
  - These forms never enter the primary score.

## Verdict rule

- Build the `B` AUROC coverage curve only on samples with `decidedness > decidedness_floor`.
- Coverage is always reported as a fraction of the full `n=200` slice.
- Per-model verdicts:
  - `Recoverable-for-M`: lower bootstrap CI of signed `B` AUROC is `> 0.50` at some coverage `>= 0.80`
  - `Undetermined-for-M`: literal decidedness coverage is `< 0.80`, but diagnostic semantic-shortlist mass dominates literal mass at coverage `>= 0.80`
  - `Low-decidedness-for-M`: literal decidedness coverage is `< 0.80` and the undetermined condition does not hold
  - `Decided-but-non-B-for-M`: literal decidedness coverage is `>= 0.80`, but no high-coverage point clears chance

`Low-decidedness-for-M` is an affirmative finding: the model does not form a robust literal `YES/NO` boundary decision at `t=0` under this prompt.

Narrow-claim scope:

- A recoverable result for a model means literal off-top1 `YES/NO` mass exists above a frozen, data-independent noise floor at `t=0`.
- It does **not** by itself imply that preamble dominance is irrelevant.

## Anchor

- Mistral-Nemo is the immediate-commit validity anchor.
- Compare `sign(lean)` against its independent free-generation committed answer on the same prompts.
- Pass bar: agreement `>= 0.95`
- Rationale: this is a validity guard on the measurement premise itself, not a descriptive downstream threshold.

## Auxiliary output

- Auxiliary `C` is `sign(lean)` versus gold `YES/NO`, where gold `YES/NO` is derived from `B` by the prompt contract.
- `C` is reported only to prevent downstream misreading; it is not an independent `A` result.

## Stated limitation

- If the scored panel happens not to realize `Low-decidedness-for-M` or `Undetermined-for-M` on any real model, that absence is not validation of those branches. It only means they were not exercised on this run.

## Explicitly out of scope

- Downstream self-retraction / trajectory self-contradiction is a separate later-gen-step experiment and is forbidden from entering this metric.
