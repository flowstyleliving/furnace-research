# CC Zenodo release — work order, 2026-09-11

**Status:** ACTIVE. Plan authored 2026-09-11; decisions D1–D4 pending MK.

## Goal

Deposit CC (`wiki/paper/cc-draft.tex`, *No Universal Detector, but a Cohort-Level Floor*) on Zenodo as a
**self-contained, citable preprint** with a matching tagged code release. Then send the DOI to Helen Moser
(FAR.AI, Programs & Partnerships), who invited proof-of-concept results for FAR.AI's research team after the
Open-Weight Safety Accelerator deadline. MK sent a holding reply on 2026-09-11, so the follow-up is owed.

## Why CC, and why only CC

- 📚 **CC goes first.** The steward (log, 21st entry) and Codex (22nd entry) agree. It has the largest n, a
  verified commitment audit, a passing shuffled-label control, a clustered bootstrap, and registered misses it
  already reports.
- ⏸️ **PRI's deposit stays on hold.** Codex's release conditions are unmet: the 6–8pp restructure, and a
  prominent statement of the reproducibility gap or the parquet package itself. The steward's `[RESOLVED]` tags
  are not deposit clearance (17th entry).
- 🔀 **This reverses the 2026-09-08 Zenodo plan**, which put CC last because it cites PRI, ACE and RPV.
  Phase 1 removes that dependency, which is what makes the reversal safe.

## Guardrails

- 🔒 **No registered endpoint, bar, denominator or sealed claim changes.** These are framing edits only. Every
  failing endpoint stays as reported: 18/20 against a ≥19/20 bar, 6/10 fixed-detector transfer, 7/20 replication.
- 🎯 **Keep three targets separate:** the input's gold label · the answer the model selects · whether that
  answer is correct. CC measures the first.
- 🧭 **Standing framing rules apply.** The 6/10 frozen-detector result shows *no universal orientation*, not
  "no informative cell". The 7/20 replication miss is a *gate cascade*, not a collapse of the geometry.
- 🚫 **No new model runs.** Banked data only. The free-generation condition is out of scope and stays a stated
  limitation.
- 🔎 **Run the six-surface grep after every claim change:** body, caption, abstract, contributions list,
  conclusion, and any results page or ledger entry that quotes the claim.
- 🤖 **Review roles.** Codex is write/audit-only and runs no code. DeepSeek cannot execute. Claude executes, and
  verifies every reviewer finding against artifacts before acting on it.
- 🪪 **A DOI is permanent.** Nothing publishes to production Zenodo without MK's explicit go. Do a dry run on
  `sandbox.zenodo.org` first. Push to public remotes only on MK's go.

## Phases

### Phase 0 — Setup

- ✅ **0.1** `openrouter_review.py` re-homed from a temp scratchpad to `~/.local/bin/openrouter_review.py`
  (2026-09-11). For DeepSeek V4 Pro, pass `--base-url https://api.deepseek.com/v1 --key-env DEEPSEEK_API_KEY
  --key-file ~/.hermes/.env --max-tokens 65536`. The default of 16,000 is too low: reasoning tokens count
  against the budget, and at 12,000 the model returned an empty string.
- ⬜ **0.2** Make the data path in `commit-confluence/stage_b/analysis/lexical_baseline.py:24` relative to the
  script. It currently hardcodes `/Users/msrk/...`. Land this as a separate commit.
- ⬜ **0.3** Push `commit-confluence`: `009e95f` plus the 0.2 fix. **Gate D1.** CC's Baselines subsection
  reports results from these scripts, so they must be public before the paper is.

### Phase 1 — Make CC stand alone (editorial, banked data)

- ⬜ **1.1 Signal-definition appendix.** Define the 27 banked panel signals and the 2 fusion signals from the
  code that computed them (sealed selector, `vendor/t0_core`, calibrator), not from the companion drafts. Then
  replace the pointer at `cc-draft.tex:218` ("Full derivations are in the companion reports").
- ⬜ **1.2 Companion bibitems** (`cc-draft.tex:908–919`). Each claims "code and sealed profiles at"
  `commit-confluence`. Verify that claim per paper: PRI's code lives in `PRI_at_commitment`, and
  `commit-confluence` vendors only `t0_core`. Fix the URLs. Retarget the PRI bibitem from "(v1–v3)" to the
  canonical v3 paper, per the 2026-09-09 canonicalization. "In preparation" may stay, as long as no argument
  depends on it.
- ⬜ **1.3 Abstract, paragraph 1.** It still opens with a monitoring promise ("flagging such answers as they are
  produced … a practical safety problem") and calls the tasks "three hallucination constructs". Codex asked for
  the supplied-candidate construct to lead. "Deployable" also appears in the abstract, where Codex's reader-facing
  rule applies. Rewrite the paragraph and keep every number.
- ⬜ **1.4 Wording sweep, per the Codex memo.** Say "checkpoint-dependent", not architecture claims. Say "signal
  beyond the tested magnitude/confidence controls". Describe the shuffled control as three permutations. Keep
  n=200 for the core profiles and n=1000 for BENCH.
- ⬜ **1.5 Figures.** Check the six figure PDFs with `pdffonts`. The 2026-09-08 log records a CC figure-font
  follow-up. Regenerate as Type 42 if Type 3 fonts are present.
- ⬜ **1.6 Operating points (D2, optional).** Compute precision, recall and F1, or TPR at a fixed FPR, per
  deployment from the banked score matrices. DeepSeek ranked this its fourth-cheapest fix, and FAR.AI's research
  team is a deployment-minded reader. These are descriptive numbers and not part of any registered endpoint.

### Phase 2 — Review gate (Codex + DeepSeek, bounded)

- 🔀 Both reviewers run **in parallel as background jobs from this session**, with Claude as the hub. They do
  not see each other's output. That independence is useful: last session's reviewers found near-disjoint defects.
- 🧾 **Codex:** `gpt-6-astra`, medium effort, a narrowed brief with the facts inlined (the 8th-entry lesson,
  after two runs died on usage limits), and `< /dev/null` to avoid the stdin hang.
- 🔬 **DeepSeek:** V4 Pro through `openrouter_review.py`, with the brief plus `cc-draft.tex` attached.
- ✅ Verify each finding against artifacts before acting on it. An unverifiable finding is logged, not fixed.
- 🛑 **Stop rule: at most two rounds.** Stop after round 1 if it returns no finding that changes a claim. MK then
  reads the PDF. Do not use an open-ended `/loop`: each new reviewer keeps finding defects, so an unbounded loop
  never converges.
- 🧪 After fixes, run the six-surface grep, a `tectonic` compile, and a clean-room zip compile. A clean compile
  does not certify semantic consistency.

### Phase 3 — Release package

- ⬜ **3.1** Add a `.zenodo.json` to `commit-confluence` (title, creator with ORCID, license, upload type, a
  "not peer reviewed" note, related identifiers). Update `CITATION.cff`.
- ⬜ **3.2** Record shape. **Gate D3.**
- ⬜ **3.3** Dry run on `sandbox.zenodo.org`.
- ⬜ **3.4** MK only: link GitHub to Zenodo (a web sign-in), tag the release, and publish.
- ⬜ **3.5** Verify that the DOI resolves and that the deposited PDF's sha256 matches the clean-room build.

### Phase 4 — Send to FAR.AI

- ⬜ Claude writes a Gmail **draft** (never sent) of 5–8 sentences. It leads with the result most relevant to
  open-weight safety: a detector frozen with one sign reads *backwards* on 4 of 10 models, while per-model
  calibration passes 10 of 10. It carries one scope sentence (input-label discrimination, not the model's own
  errors), the DOI and repo, and the audit log linked last. MK reviews and sends.

### Phase 5 — After

- ⬜ **Vault propagation:** log, index, `paper/README.md`, and `milestones.md`. A deposit is milestone-worthy, so
  it needs MK sign-off, then a commit and push of `furnace-causalities`.
- ⬜ **Next venues,** not on the FAR.AI critical path: arXiv (endorsement route for independent authors), then
  TMLR with an anonymized copy.

## Decisions for MK

- 🚀 **D1** — Push `commit-confluence` after the 0.2 path fix?
- 📈 **D2** — Operating points (1.6): in or out?
- 🗃️ **D3** — Zenodo shape: one record (paper PDF + release archive), or two linked records (a preprint record
  plus a software record from the GitHub integration)?
- 📅 **D4** — Target date: what did the holding reply to Helen promise?

## Acceptance

- `cc-draft.tex` compiles with 0 errors and 0 undefined references, and the clean-room zip compiles.
- No sentence depends on a companion paper for a definition. Any remaining "in preparation" citation is not
  load-bearing.
- The six-surface grep is clean for every changed claim.
- The review-gate stop rule is met, and every applied finding was verified.
- The sandbox record renders, the production DOI resolves, and the PDF sha256 matches.
- The FAR.AI email draft exists in Gmail.

## Handoff

- **Claude:** executes, verifies, compiles, and propagates.
- **Codex:** audits; drafts prose on MK's request; never runs code.
- **DeepSeek:** independent review; no execution.
- **MK:** decisions D1–D4, the Zenodo account link and publish, the PDF read, and sending the email.
