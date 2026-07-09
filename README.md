# Furnace — the geometry of commitment

*An AI-safety research vault, published in the open and offered for critique.*

This is the working notebook of **Furnace**: an attempt to answer one question with real instruments —

> **When a language model commits to an answer, does that commitment have a measurable shape in the model's internal geometry — and can that shape flag a reasoning failure or a misaligned commitment *before* the token is emitted?**

It is a *live* research vault, not a finished paper. Findings are versioned, pre-registered where it counts, and **include their own falsifications**. If a result died, the tombstone is still here. That is the point.

## The lines of work

- 🎯 **PRI — Predictive Rupture Index.** Scores each generated token by pairing token surprise with a representation-space *rupture* signal at the commitment step. Sealed statistic: `null_ratio` — how much the commitment step moves into the directions the model has lost discrimination power in. *Sealed, passes 3/3 primaries.*
- 👁️ **ACE — Attention Commitment Estimator.** Reads the *shape of attention* at the moment of preparation (`t=0`), with no access to the unembedding — commitment morphology rather than commitment content. *Sealed; 7/9, with partial cross-task transfer.*
- 🌑 **RPV — Readout Pseudo-Volume.** The softmax-Fisher pseudo-volume of the readout — "how ambiguous is it here." An **honest negative**: it beats plain confidence but is redundant with PRI, earning its keep only where PRI collapses. We published the negative.
- 🔗 **Commit-Confluence.** A single honest dispatcher that fits ACE + PRI + RPV + confidence + fusion under one nested out-of-bag selector, per (model, task). Headline: **no universal detector, but a universal above-chance floor** — 18/20 deployable, 12 distinct winners.

## How the work is done

The methodology is itself an experiment: this vault is an **LLM-maintained wiki** (after Karpathy's pattern), where the reasoning trail, the dead ends, and the canon all live as linked Markdown. The discipline that keeps it honest:

- 📋 **Pre-registration + sealed gates** — the falsifier is written before the run; verdicts are byte-reproducible.
- 🧪 **Nested out-of-bag selection** — the cell is chosen and scored on disjoint data, so the reported number isn't the selection-inflated one.
- 🚫 **Negative controls everywhere** — shuffled labels, temperature matching, basis rotations; a signal has to beat all of them.
- 🪦 **Honest negatives are first-class** — "beats confidence but redundant with PRI" is a result we keep, not one we bury.

## Reading it

Start here, in this order:

- [`wiki/overview.md`](wiki/overview.md) — the framing and the PRI derivation.
- [`wiki/log.md`](wiki/log.md) — append-only session log; **the tail is the source of truth for "what's true now."**
- [`wiki/claims.md`](wiki/claims.md) — the tagged claim ledger (`[VALIDATED]` / `[FALSIFIED]` / `[OPEN]` / …).
- [`wiki/results/summary.md`](wiki/results/summary.md) — running results.
- [`wiki/research-candidates.md`](wiki/research-candidates.md) — the forward-looking idea ledger (the current frontier).
- [`wiki/index.md`](wiki/index.md) — full page catalog.

Companion repositories (code + reproducible artifacts):
[t0-morphology-furnace](https://github.com/flowstyleliving/t0-morphology-furnace) ·
[commit-confluence](https://github.com/flowstyleliving/commit-confluence) ·
[furnace-causalities](https://github.com/flowstyleliving/furnace-causalities) (curated milestone log).

## Open for critique

This is published *because* it is unfinished. If a control looks weak, a claim over-reaches, a metric is a confound in disguise, or a negative should have been called sooner — **open an issue**. Adversarial reading is the whole methodology; you are invited to be the adversary.

## What's intentionally not here

To keep the repository clean and lawful, some material is omitted: copyrighted source PDFs and the theoretical-provenance corpus (`raw/`), private reviewer-feedback notes, frozen paper export bundles (`*.zip`), local agent-orientation and tooling files. Internal links pointing at those will not resolve here — that omission is deliberate, not rot.

---

*Furnace is early-stage, single-researcher, build-in-public AI-safety work. Nothing here is peer-reviewed yet. Treat every number as provisional and every invitation to critique as sincere.*
