# Paper Writing Standards — Furnace reference stock

_Created 2026-07-26 during the cc-draft ↔ cc-extend merge. This is the house reference for how Furnace papers are written. It sits below the frozen-language obligations of any pre-registration: **when a registration's frozen sentence conflicts with a style rule here, the registration wins, verbatim.**_

## 1. 🧱 Abstract formula

One paragraph, in this order, no deviations without reason:

1. **Context** (1–2 sentences) — the phenomenon and why it matters. No citations in the abstract.
2. **Gap** (1 sentence) — the question nobody has asked, stated as a question a deployer would ask.
3. **Method** (1–2 sentences) — what was built and the one methodological guarantee that makes the numbers trustworthy (here: nested-OOB selection-bias correction; pre-registration before data).
4. **Headline numbers** (2–4 sentences) — every number with its **denominator and its registered bar** (`18/20 against ≥17/20`), passes and failures with equal prominence. A registered FAIL appears in the abstract if the registration says the result cannot be published without it.
5. **Scoped conclusion** (1–2 sentences) — the one-line thesis, with its scope word load-bearing ("in this cohort", "on the sealed tasks"). Never a claim the body doesn't own.

Length budget: \~250–350 words. If it exceeds that, cut context and method — never the failures.

## 2. 📐 Section and paragraph craft

- **BLUF everywhere.** The first sentence of every section and every `\paragraph{}` states the verdict; mechanism and anatomy follow. ("The stronger endpoint fails." — then how.)
- **`\paragraph{}` headers for results** so a skimmer reads the verdict chain from headers alone.
- **Tables carry facts, prose carries meaning.** Never narrate a table row-by-row; state what the table *establishes* and point at it.
- **One denominator discipline**: any count in prose carries its denominator and, if registered, its bar. "Most models pass" is banned; "$10/10$ against $\geq 8/10$" is the form.
- **Numbers in math mode** (`$18/20$`, `$0.6705$`); model/task/signal names in `\texttt{}`.
- **Symbolic references only** — `\ref{fig:...}`, never a hardcoded "Figure 6". Labels namespaced `fig:` / `tab:` / `sec:`. (This is what made the extension merge renumbering free.)
- **The honest-negative pattern**: state the registered miss first and plainly ("B1 scores $7/20$ against $\geq 17/20$"); then the descriptive anatomy, explicitly labeled *descriptive* and explicitly *not a rescue*; then what the miss does and does not license.
- **Framing-rule sentences travel in pairs**: every "no universal X" claim is immediately followed by the guard against over-reading ("this is NOT the absence of a common informative cell"). Never let the negative half stand alone.

## 3. 🧊 Registration-language obligations (CC/BENCH — currently binding)

These sentences are frozen by `PRE_REGISTRATION_BENCH.md` and must appear (in substance-preserving form) in **any** publication of the extension, merged or standalone:

- ⚖️ Exactly one of A1/A2 passing licenses only: *the floor **partially extends**, with the failing endpoint named.* Never an unqualified "extends".
- 📢 The B1 miss ($7/20$ vs $\geq 17/20$) must be stated **prominently**; the extension may not be published without it.
- 🧪 `anli_r1_rep` is a *re-test of the sealed construct at $5\times n$ on the train distribution* — never "same-distribution replication" or "fresh-data replication".
- 🔧 The Amendment A1 disclosure: the commitment normalizer *was amended between smokes and strict cells* (non-empty yes/no prefix; rescues only Mistral-7B's subword `Y`; newline and " To" signatures left as failures).
- 🚧 Family-C results may **narrow but never upgrade** any headline claim; ANLI R2 is robustness-only; the 52/53 aggregate is non-endpoint and failure-excluding.
- 🗺️ Comparability: byte-comparable MLX, torch/Modal, and mlx-vlm cells are never pooled; every non-byte-comparable cell is daggered or sectioned separately.

## 4. 📚 Reference hygiene (the hardening rule)

- **Every external claim in the introduction/related-work cites a real reference.** A derived, merged, or companion paper must carry the **full external bibliography** of its parent for every section it inherits — a companion that drops the field's references (as `cc-extend-draft` did, 7 items vs the parent's 13) reads as unscholarly and is a defect, not a simplification.
- Shared bibitem keys across companion papers must be **byte-identical** (verified by diff before any merge).
- No orphan bibitems (unused entries), no undefined `\cite` keys — grep both directions before shipping.
- Self-citations to a paper being merged in are dissolved into internal cross-references, never left as `\cite`.
- In-preparation companion reports are cited with repository URL; published external work with venue and year.

## 5. 🔩 Mechanics

- Preamble: standard packages only (compiles on Overleaf pdflatex as-is); `\graphicspath{{<code>-figures/}}`; `amssymb` whenever `\checkmark` is used.
- Filenames follow `<method>-<role>` (see [[paper/README]]); figures keep their build-time filenames even when renumbered in print.
- Overleaf bundles: `<code>-paper-YYYY-MM-DD.zip` = tex + exactly the figures it includes; superseded bundles listed in the README, never deleted.
- Every substantive edit pass ends with: brace/environment balance check, `\ref`/`\label` and `\cite`/`\bibitem` bidirectional grep, stale-phrase sweep against the current canon (log tail beats orientation).
- Adversarial review before any public link: at least one Codex high-reasoning pass scoped to registration language (`/grill-me-codex`), all catches applied or explicitly rebutted.

## 6. 🗣️ Voice

- Plain, declarative, unhedged where verified; explicitly hedged where not ("descriptive only", "this cohort").
- No superlatives about our own work; the strongest permitted self-assessment is a precise scope statement.
- The reader who must be satisfied is the adversarial one: every sentence should survive "prove it or scope it."
