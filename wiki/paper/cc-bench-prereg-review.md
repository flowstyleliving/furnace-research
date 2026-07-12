# Codex Adversarial Review — PRE_REGISTRATION_BENCH.md (Phase-0 draft)

**Reviewed:** `commit-confluence/stage_b/PRE_REGISTRATION_BENCH.md` (v1.0 draft, 2026-07-11)
**Reviewer:** Codex CLI (default model — requested `gpt-5.6-sol` was not selectable; exact backend id not exposed), write/audit-only, static inspection.
**Verdict:** **SCORE 4/10 — restructure before sign-off.**
**Status:** all TIGHTENED items folded into pre-reg **v1.1** same day (see the pre-reg's revision header + §10). Sign-off still pending MK.
**Lineage:** [[paper/cc-benchmark-review]] (v1, FIX) → [[paper/cc-benchmark-review-v2]] (v2, FIX) → this review (Phase-0 draft, FIX).

Files Codex inspected: `wiki/log.md`, `cc-benchmark-review-v2.md`, `PRE_REGISTRATION_BENCH.md`, `check_fresh_data.py`, `run_seal.py`, `generate_fresh_data.py`, `confluence_calibrator.py`, `sealed_selector.py`, `analyze_universality.py`, `PRE_REGISTRATION.md`, `pri_calibrator.py`, `pri_v2_io_plugins.py`, `data/anli_R1_seed20260612_n200.jsonl`, `comprehensive_run.py`.

---

## Verbatim output

SCORE: 4/10
NITS:

- The cluster gate is not executable as specified. `stem_id` is discarded: loaders retain only scores, labels, and `sample_idx`; merging and `.npz` persistence likewise omit groups (`confluence_calibrator.py:70-84, 389-391, 394-431`; `stage_b/run_seal.py:61-66`). The selector resamples row indices (`sealed_selector.py:121-152`). §7.4 therefore requires coordinated loader/merge/persistence/API changes, not merely "keying" the calibrator (`PRE_REGISTRATION_BENCH.md:239-241`). Audit fix #5 is not resolved.

- "Outer and inner/OOB resampling" misdescribes the algorithm. There is one bootstrap draw, in-bag selection, then OOB evaluation—no inner bootstrap (`sealed_selector.py:99-104, 121-152`). Freeze an exact cluster algorithm rather than statistical-sounding prose (`PRE_REGISTRATION_BENCH.md:165-168`).

- This is not frozen. It declares itself registered and frozen (`PRE_REGISTRATION_BENCH.md:3-4, 20`) while MK sign-off is pending and five primary integers remain open (`PRE_REGISTRATION_BENCH.md:280-286`). Until those are fixed and signed, §10 cannot claim all eight fixes resolved.

- A2 has a denominator escape hatch. Behavioral failures produce no strict matrix (`PRE_REGISTRATION_BENCH.md:253-255`), while current LOMO silently discovers only existing matrices and sets its denominator to `len(slugs)` (`analyze_universality.py:47-61, 68-71, 122-125`). Thus "≥8/10" can silently become 8/9. The named-cell endpoint is also a new path: current code exposes only post-run `fixed_cell_max_survival` (`analyze_universality.py:112-129`). Audit fix #2 is scientifically named but procedurally unfinished.

- B1 knowingly preserves the invalid row bootstrap for paired TriviaQA (`PRE_REGISTRATION_BENCH.md:170-175, 186-187`), although each question emits two dependent rows (`generate_fresh_data.py:242-261`). That reproduces the seal's procedure, not a valid independent replication. It is also not strictly comparable: ANLI moves from dev to train and n rises fivefold (`PRE_REGISTRATION_BENCH.md:113-118`). A single "17/20 replication" bar conflates corrected and uncorrected estimands.

- Existing launch semantics contradict the proposed denominator policy. The pre-reg allows one or two failed cells while A1/B1 can still pass (`PRE_REGISTRATION_BENCH.md:25-26, 179-187, 253-255`); current `run_seal.py` forbids any endpoint PASS whenever any cell is incomplete (`run_seal.py:235-241`). This must be deliberately redefined, not inherited.

- The promised freshness gates do not exist. The pre-reg requires exclusion against both 20260526 and 20260612 files (`PRE_REGISTRATION_BENCH.md:113-120, 129-134`), but the builder knows only the 20260526 references (`generate_fresh_data.py:40-43, 96-100, 167-172`), and the gate accepts exactly one sealed reference (`check_fresh_data.py:58-65, 115-124`). `train_r1`, pooled R2, HaluEval, stem caps, length checks, and generic tasks are presently unreachable (`generate_fresh_data.py:96-100, 290-300`; `check_fresh_data.py:68-74`). Audit fix #3 is a design promise, not an executable closure.

- HaluEval is not actually template-frozen. QA is verbatim, but dialogue and summarization use "same instruction shape," slashes, and `{…}` placeholders (`PRE_REGISTRATION_BENCH.md:83-103`). Only Mistral-Nemo in the cohort receives chat wrapping; the other nine use raw passthrough (`pri_v2_io_plugins.py:207-247`). The smoke checks only 16 rows and the strict matrix retains token IDs, not per-row decoded commitments (`PRE_REGISTRATION_BENCH.md:153-159`; `comprehensive_run.py:481-511`). Audit fix #6 is partial: stratification improved, but prompt bytes and full-cell semantic commitment remain unfrozen.

- Hash coverage is still conditional. The manifest names current scripts (`PRE_REGISTRATION_BENCH.md:42-47`) while §7 permits sibling builders and launchers (`PRE_REGISTRATION_BENCH.md:228-238`) that would not be covered. "T0-subset" is not enumerated, and runtime equality names a venv rather than frozen version values (`PRE_REGISTRATION_BENCH.md:32-40`); actual `module_hashes()` covers a specific module list only (`confluence_calibrator.py:275-305`). Audit fix #1 is partial.

- The amendment rule is a blank cheque: "any gate failure → fix builder → regenerate" permits post-draw changes without distinguishing implementation correction from protocol-changing filters (`PRE_REGISTRATION_BENCH.md:245-252`). There are no abort rules for insufficient confirmatory length intersection, hash drift, source drift, or systematic first-token failure.

- R2 pooling is acceptable only as exploratory, but its estimand remains loose: the dev/test allocation and split-stratification rule are not frozen, and only a combined result is promised (`PRE_REGISTRATION_BENCH.md:121-125`). A hostile reviewer can reasonably ask whether pooling concealed split heterogeneity.

- Independent §10 verdict: #1 partial; #2 partial; #3 partial; #4 resolved by explicit exclusion; #5 failed; #6 partial; #7 resolved by exclusion; #8 resolved by exclusion (`PRE_REGISTRATION_BENCH.md:267-278`).

- Requested `gpt-5.6-sol` was not available as a selectable runtime. This audit ran on the default Codex model; its exact backend identifier is not exposed.

TIGHTENED:

- Restructure the grouped-data path before sign-off: persist `stem_id` beside `sample_idx` through ACE/readout alignment, merged matrices, and `.npz`; require exact equality with source JSONL metadata. Replace §5 with: "Each replicate samples stem IDs with replacement; all rows belonging to each sampled stem enter in-bag with the same multiplicity; OOB contains all rows from stems absent in-bag; selection occurs in-bag and fixed-cell/sign evaluation occurs OOB."

- Split B1 into two endpoints: "B1-procedural: seal-identical row bootstrap, historical comparability only" and "B1-valid: cluster bootstrap for TriviaQA, row bootstrap for ANLI." Only B1-valid may support replication language. Do not call train-R1 ANLI a same-distribution replication.

- Add: "All A2 counts use the planned ten-model cohort. A missing/behavioral-fail holdout contributes zero; `of_n_holdouts` is always 10. If fewer than three usable training models remain, A2 aborts and fails."

- Replace the HaluEval shorthand with exact byte-for-byte templates. Require a full-cell commitment audit: every strict row must decode its first generated token to canonical YES or NO; otherwise that cell fails. Freeze normalization for whitespace-prefixed token forms.

- Enumerate both exclusion files and require zero overlap against their union by normalized prompt hash and, where available, stem/question ID. Freeze the R2 dev/test sampling allocation and report split-specific descriptive results.

- Replace "fix builder → regenerate" with: "Implementation-only corrections require an amendment before regeneration; any change to source, template, sampling frame, exclusions, length cap, labels, bars, or endpoint logic voids Phase 0 and requires a new preregistration."

- Hash the actual files selected after Phase 1, including any sibling launcher/builder, plus exact Python/MLX/dependency versions. Remove "or a sibling" and "or `run_bench.py`" before freeze.

- Do not sign off until the cluster path, planned-denominator A2, generic gate, exact templates, and explicit abort rules are written. The current design needs restructuring, not cosmetic red-line edits.
