# Harness audit + remediation — 2026-07-09

Claude Code audit of the empathy-geometry harness Codex built and ran on 2026-07-09, the user-requested remediation (A + B), and the write/audit remediation work-order for Codex plus executor-owned run validation. Part of [[empathy-geometry/README|Empathy Geometry]] (candidate #11). Status: **still design phase — no research-grade results exist; canon uncontaminated.**

## What Codex built and "ran"

A Python harness (`eg_harness/`: cli / runner / providers / checker / judge / persona_export / claude_handoff) with tests, plus MLX wiring and a vendored copy of `safety-research/persona_vectors`. It executed several "smoke" and one "pilot" run (30 dialogues, `artifacts/claude-pilot/`, now renamed).

## Audit findings

- 🎭 **The "pilot" is synthetic by construction — zero empirical content.** Dialogue text came from `DeterministicProvider` hand-written per-arm templates (giraffe = scripted perfect NVC incl. a checkpoint solution; jackal = scripted blame); authenticity came from a fixed formula in `judge.py` (`2.5 + 1.6·refl − 0.7·jkl + …`, stamped `heuristic-blind-placeholder`, `research_grade:false`); geometry was `sha256(text)`-derived (`surrogate-offline`). Proof it's circular: mean authenticity in the 30-dialogue run (giraffe 3.2583 / jackal 1.3) is **byte-identical** to the 1-dialogue smoke — zero variance across dialogues. The clean giraffe-resolves/jackal-fails separation is the hypothesis hard-coded, not a measurement.
- ✅ **Honestly labeled (no deception).** Every summary stamps `surrogate_geometry_only:true`, `real_t0_attention_ready:false`, `research_grade:false`; the runner emits "Geometry rows are surrogate-offline and must not be treated as latent measurements"; README was downgraded to "pilot plumbing only"; **no `wiki/results/` page written**; no root/canon contamination. The risk was misreading, not fabrication.
- 🗂️ **Vault pollution.** 122 MB harness sat inside the Obsidian vault (`the_GOAT/repos/`), 117 MB of it a full clone of `persona_vectors` (incl. a 58 MB `dataset.zip` and its own nested `.git`); `vendor/` was not gitignored. Also a `.pycache_py39/` mirror of system stdlib.
- 🤖 **Agent-spawn mechanism.** `claude_handoff.py` shells out to `subprocess.run(["claude","-p",…])` for an automated "peer audit," with `--max-budget-usd` and a `--permission-mode` whose allowed values include `bypassPermissions`/`dontAsk`. Opt-in (CLI subcommand, not a loop), gated on `claude auth login`. Running that login **arms** it — the user should opt in consciously.
- 🔬 **The one "real" signal is domain-mismatched + 1 turn.** `mlx-real-t0-mini` uses backend `mlx-furnace-attention-t0`, but that is the **ANLI-calibrated** furnace-guard t0 attention scalar applied to empathy text (the exact domain mismatch guard doctrine says to distrust), over a single turn. Proves the wire, measures nothing.
- 🚧 **Checker encodes an un-red-lined grammar.** The parser/judge implement a particular faux-list / t_hear / ripeness version — all still `[USER GATE]`. "Tests PASS" ≠ "grammar is right." RPV/readout-spectrum and real T4 vectors still unwired.
- 🧭 **Vault became a git repo.** `the_GOAT` was `git init`'d since 2026-07-08 (Codex's 2026-07-08 log said it was *not* a repo); currently `.git` is ~76 K with **no commits** and everything untracked. Not acted on — flagged for the user; committing the vault is a user-driven decision.

## Remediation done (Claude, 2026-07-09) — user-requested A + B

- **(A)** Moved the harness out of the vault to a sibling standalone repo `/Users/msrk/Documents/empathy-geometry-harness`; `git init` (own repo, **not** nested in the vault); baseline commit `369b9f0` (20 source files; `.git` ~196 K). Rewrote `.gitignore` to exclude `vendor/` (117 MB clone kept **on disk** for vector extraction, restore recipe in the ignore file), `artifacts/`, `.pycache_py39/`, `.obsidian/`, `.claude/`, `.agents/`. Verified: no heavy files staged; vault `.git` (76 K) never held the clone and the move left the vault working tree clean; `the_GOAT/repos/` removed.
- **(B)** Renamed `artifacts/claude-pilot/` → `artifacts/synthetic-plumbing/`; added `artifacts/README.md` warning that nothing in the directory is a result.

## Codex write/audit work-order — dispatched 2026-07-09

Turn the synthetic pipeline real, in the standalone repo, diff reviewable against `369b9f0`. Codex owns patch/spec authorship and static audit only; a user, Claude Code, or another executor owns tests, model calls, smoke runs, pilots, and run artifacts.
1. **Real generation** — real MLX Qwen2.5-7B for dialogue text on actual runs (DeterministicProvider retained for unit tests only); real multi-turn dialogue (Codex's only real capture so far was 1 turn); matched temperature both sides.
2. **Real blinded judge** — replace the heuristic formula with a real model call, blind to arm/system-prompt/geometry. Judge-model choice remains a user gate (design rule: judge ≠ dyad family); if only Qwen is cached, use it as a **stamped stand-in** with `research_grade:false`.
3. **Real geometry, raw not calibrated** — capture raw Furnace panel features per turn at both loci (t0 ACE attention morphology + gen_step=1 readout/surprise/RPV eff-rank & pseudo-volume). Do **not** reuse the ANLI-calibrated guard ALLOW/BLOCK verdict as "the signal"; store raw metric values for later calibration against authenticity labels. Stamp a new backend (e.g. `mlx-furnace-panel-raw`).
4. **Honest stamping preserved** — real runs stamp `surrogate_geometry_only:false`, real `judge_backend`, `provider_backend:mlx-*`; keep `research_grade:false` with reason (grammar red-line + judge-model still user-gated).
5. **Executor re-run (validation, not the pilot)** — a small real run (e.g. 2 dialogues/arm × 12 turns) proving the pipeline is genuinely real end-to-end; report `summary.json`. **No `wiki/results/` page; no overclaiming separation.** Codex writes the command/work order but does not execute it.
6. **Hygiene** — nothing back into the vault; never commit `vendor/` or `artifacts/`; fix any path breakage from the move; write tests to cover provider selection; prepare a clear commit scope/message for the executor.

**Claude will re-audit Codex's diff and the executor-produced real run** (backends real? judge a real model call? geometry raw not ANLI-calibrated? dialogue text is model output with cross-dialogue variance, i.e. the byte-identical-means tell is gone?) before any of it is trusted.

## Bottom line

Nothing dishonest, nothing in canon. Treat every existing artifact number as zero-signal. The vault-pollution and agent-spawn items are handled/flagged; the real-signal code/spec fixes are with Codex, while execution and run validation are not.
