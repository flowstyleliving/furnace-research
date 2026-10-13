# 🛒 Backlog — the shopping list

_Last triaged: 2026-10-12 (Claude, first pass; MK has not reviewed the scores)._

A to-do list of things we *can* do, not a phased build plan. Items are grouped by type, not by order or
dependency. Each line carries the modified-Fibonacci scores from MK's `fibonacci-prioritization` skill
(`~/.hermes/skills/productivity/fibonacci-prioritization/SKILL.md`): **V** = impact, **E** = effort, both from
**{1, 2, 3, 5, 8, 13, 20, 40, 100}** only, and **V/E** = impact ÷ effort (higher = more bang for the buck).
**Priority** is the V/E rank inside its group (1 = do first). Status is `open`, `blocked: <reason>`,
`status unverified` (an older note lists it and nothing newer confirms it), or `done`.

## 🧭 How to review this list

Whenever this file is opened for review (by MK, Claude or any agent), re-triage it before acting:

1. 🗂️ **Regroup by type.** Keep the five type groups; add a group only when an item fits none of them.
2. 🔢 **Re-score with the skill.** V and E only from {1, 2, 3, 5, 8, 13, 20, 40, 100}; recompute V/E; re-rank
   priority inside each group. First instinct, no haggling over numbers.
3. ✅ **Move finished items to Done** with the date and the evidence (commit, results page, log entry).
4. 🚧 **Flag blocked items** as `blocked: <reason>`, naming who or what unblocks them.
5. 🔍 **Verify before upgrading.** If evidence for an item is older than the latest `wiki/log.md` entry about it,
   mark it `status unverified` rather than current.
6. 🔒 **Never delete or reword MK's tasks.** Add notes after the task text; split an item only by adding new lines.
7. 📅 **Update the "Last triaged" date** at the top.

---

## 🧪 Experiments and compute

- [ ] **FIBS probes: two-step activation-parity gate** (≤ $5 on Llama-3.1-8B, then ≤ $45 on Qwen3.5-397B only if step 1 passes) — V 13 · E 5 · V/E 2.6 · Priority 1 · Status: blocked: MK budget decision (asked 2026-10-12) · Source: [[workorders/fibs-probe-replication-workorder-2026-10-12]]
- [ ] **FIBS probes: Qwen3-32B stage 2** (8 SHADE-Arena episodes + reads + parity) — V 3 · E 2 · V/E 1.5 · Priority 2 · Status: blocked: Phase A stopped under MK's parity rule (2026-10-12) · Source: [[workorders/fibs-probe-replication-workorder-2026-10-12]]
- [ ] **Temperature-robustness study, full run** (Endpoint A reshape-only + Endpoint B sampling pilot cohort) — V 20 · E 20 · V/E 1.0 · Priority 3 · Status: Endpoint B **running** locally since 2026-10-12 21:55 PDT under Amendment A1 (`ee61a5d`, $0, run dir `temp-sweep/pilot/runs/2026-10-12-endpoint-b-full/`); Endpoint A still blocked: funding gate (MK 2026-08-27, "let's do this run once we get funding"), §3.7 extractor unbuilt, and the v1.3 pre-registration is unsigned · Source: [[workorders/temp-sweep-workorder-2026-08-26]]
- [ ] **Depth lane: a third unseen task** — V 8 · E 8 · V/E 1.0 · Priority 4 · Status: open (MK decision) · Source: root `CLAUDE.md` (DC lane, "Open MK decisions")
- [ ] **Free-generation CC panel** — V 8 · E 13 · V/E 0.62 · Priority 5 · Status: status unverified (draft plan 2026-09-12; decisions D1–D5 pending MK) · Source: [[workorders/free-generation-cc-panel-workorder-2026-09-12]]
- [ ] **Token-budget pilot** (phase-0 build authorized; detector scoring not authorized) — V 5 · E 8 · V/E 0.63 · Priority 6 · Status: status unverified (draft v5, 2026-09-02; freeze blocked on the §4.3/§4.5 manifests, the §4.4 `n` decision and phase-0 results) · Source: [[workorders/token-budget-pilot-workorder-2026-09-02]]
- [ ] **FIBS probes: large-model Phase A** (Qwen3.5-397B-A17B $179–438; Nemotron-3-Ultra $370–875) — V 20 · E 40 · V/E 0.5 · Priority 7 · Status: blocked: no GPU spend approved; the parity gate comes first · Source: [[workorders/fibs-probe-replication-workorder-2026-10-12]]
- [ ] **Depth lane: 405B stretch relaunch** — V 3 · E 13 · V/E 0.23 · Priority 8 · Status: status unverified (root `CLAUDE.md` says "relaunchable as-is", but [[references/gpu-ledger]] notes on 2026-10-10 that the 405B weight cache is no longer on Modal) · Source: [[workorders/depth-grid-expansion-workorder-2026-08-17]]

## ✍️ Writing, papers and applications

- 🔒 *Grant-application to-dos are withheld from the public repo until the application is public.*

- [ ] **FAR.AI: send the follow-up with a citable CC link** — V 13 · E 2 · V/E 6.5 · Priority 6 · Status: status unverified · Source: [[log]] 2026-09-12 fifth entry; memory note `far-ai-outreach`
- [ ] **DC paper: milestone and publication timing** — V 8 · E 2 · V/E 4 · Priority 8 · Status: open (MK decision) · Source: root `CLAUDE.md` (DC lane, "Open MK decisions")
- [ ] **DC paper: the optional limitations paragraph** — V 2 · E 1 · V/E 2 · Priority 11 · Status: status unverified (open MK decision logged 2026-08-31) · Source: [[paper/dc-scaffold]]
- [ ] **CC Zenodo release work order, decisions D1–D4** — V 2 · E 1 · V/E 2 · Priority 12 · Status: status unverified (work order still says ACTIVE, but another document cites the Zenodo record as public; reconcile and archive) · Source: [[workorders/cc-zenodo-release-workorder-2026-09-11]]

## 🛠️ Code and tooling

- [ ] **FIBS probes: write a vLLM-hook activation capture** (Codex authors; free) — the prerequisite for the parity gate — V 13 · E 5 · V/E 2.6 · Priority 2 · Status: open · Source: [[workorders/fibs-probe-replication-workorder-2026-10-12]]
- [ ] **Temperature study: build the extractor, scorer, sampler, decidedness and equivalence artifacts** (pre-registration §3.7) — V 13 · E 13 · V/E 1.0 · Priority 3 · Status: blocked: MK sign-off on v1.3 and funding · Source: [[workorders/temp-sweep-workorder-2026-08-26]]
- [ ] **Capture provenance columns** (additive capture change) — V 3 · E 3 · V/E 1.0 · Priority 4 · Status: status unverified (OPEN, authored 2026-09-10) · Source: [[workorders/capture-provenance-columns-workorder-2026-09-10]]
- [ ] **FIBS probes: large-model entry points** — reads, parity and full rollouts for the 397B; an 8×B200 entry point and Mamba-2 kernels (`mamba-ssm`, `causal-conv1d`) for Nemotron-3-Ultra; a first-GPU headroom check — V 5 · E 8 · V/E 0.63 · Priority 5 · Status: open (code is free; runs are not approved) · Source: [[workorders/fibs-probe-replication-workorder-2026-10-12]]

## 🗄️ Admin and ops

- [ ] **Vault: 4 unpushed commits (2026-09-21, 2026-10-10) plus 42 uncommitted changes; the remote `furnace-research` is public** — decide what to commit and push — V 5 · E 2 · V/E 2.5 · Priority 1 · Status: open (checked 2026-10-12) · Source: `git status` in the vault
- [ ] **GPU ledger: replace the list-price equivalents for the 2026-10-12 FIBS runs with billed figures from the Modal dashboard** — V 2 · E 1 · V/E 2 · Priority 2 · Status: open · Source: [[references/gpu-ledger]]
- [ ] **commit-confluence: untracked `exploratory/fibs-replication/`, `free-generation/`, `token-budget/`, and the temperature pilot harness `temp-sweep/pilot/` (its `runs/` raw outputs are git-ignored)** — decide whether to commit — V 3 · E 2 · V/E 1.5 · Priority 3 · Status: open (checked 2026-10-12; the temperature pilot harness was committed 2026-10-12 in `ee61a5d`, raw `runs/` still ignored) · Source: `git status` in `commit-confluence`
- [ ] **Claims-ledger cleanup: checkpoint 1 (B2), MK approval of the tag grammar** — V 3 · E 3 · V/E 1.0 · Priority 4 · Status: status unverified (awaiting MK since 2026-08-18) · Source: [[workorders/claims-ledger-cleanup-workorder-2026-08-17]]
- [ ] **PRI_at_commitment: 20 uncommitted changes** — review — V 2 · E 2 · V/E 1.0 · Priority 5 · Status: open (checked 2026-10-12) · Source: `git status` in `PRI_at_commitment`

## 🔍 Investigations

- [ ] **Get to the bottom of the earlier TriviaQA extended-run failures** (MK request, 2026-10-12) — V 13 · E 3 · V/E 4.3 · Priority 1 · Status: open. Known so far: in BENCH `triviaqa_paired_rep`, 14 one-token commits were not YES/NO (gemma-3-4b 12 of 1,000, such as " The", " Apple", " Leicester"; Llama-3.1-8B 1, " __"; Qwen3-1.7B 1, " ("). Three models with such commits tripped the pre-registered rule that zeroes a whole task, so all 10 TriviaQA cells were forced to fail. Open: why these models answer with content words on this task, and whether a retry or exclusion rule should be registered for the next run · Source: [[results/summary]] (B1 gate cascade); `commit-confluence/stage_b/profiles_bench/triviaqa_paired_rep/*.matrix.npz`
- [ ] **Empathy-geometry: the nvcc.life cycling-instrument menu** — V 5 · E 3 · V/E 1.7 · Priority 2 · Status: status unverified (open menu awaiting MK since 2026-08-13) · Source: memory note `empathy-geometry-project`; [[empathy-geometry/README]]
- [ ] **Research candidates: open entries** — browse the index table rather than copying it here — V 3 · E 2 · V/E 1.5 · Priority 3 · Status: open (pointer) · Source: [[research-candidates]]

---

## ✅ Done

- [x] **Push the temperature plan to `commit-confluence/exploratory/temp-sweep/`** — done 2026-10-12, commit `29cf27b` on public `origin/main` · Source: [[log]] 2026-10-12
- [x] **FIBS probes: Phase A stage 2 for Llama-3.1-8B** — done 2026-10-12; parity ambiguous, Phase A stopped; report `commit-confluence/exploratory/fibs-replication/PHASE_A_STATUS_2026-10-12.md` · Source: [[workorders/fibs-probe-replication-workorder-2026-10-12]]
- [x] **Temperature Part B: small local sampling pilot** (4 models, greedy + T 0.7 / 1.0 / 1.5, 5 samples, seed 20260826) — done 2026-10-12: 2,560 outputs, 1 harness flag (a Qwen near-tie where `mlx_lm` disagreed but the historical commit matched), 0 parser disagreements; invalid answers rise with temperature in every model (Llama 1% → 40% of draws at T 1.5; Phi-3.5 about 20% even at T 0.7) · Source: `commit-confluence/exploratory/temp-sweep/pilot/runs/2026-10-12-pilot/SUMMARY.md` (local, uncommitted)
- [x] **Temperature pilot: harness fixes before expanding to the full Part B** — check parity against the historical commits, not `mlx_lm`, and log each greedy margin to flag near-ties; report invalid answers separately from wrong ones (the pre-registration counts them as errors; changing that needs an amendment); decide in advance whether Phi-3.5 stays in; replace the zero-tolerance task gate with a per-cell error budget — V 8 · E 2 · V/E 4 · Priority 1 · Status: done 2026-10-12 — all four in Amendment A1 (Codex gpt-6-astra draft; DeepSeek audits round 1: 4 major + 3 minor, round 2: 0 blocking + 1 major + 1 minor, all applied; self-checks 12/12), committed before any full-run output and pushed as `commit-confluence` `ee61a5d` · Source: `commit-confluence/exploratory/temp-sweep/AMENDMENT_A1_ENDPOINT_B_2026-10-12.md`; audits `.temp-sweep-deepseek-audit-r1-2026-10-12.md`, `.temp-sweep-deepseek-audit-r2-2026-10-12.md`
