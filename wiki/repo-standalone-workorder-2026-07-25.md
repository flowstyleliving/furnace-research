# Codex work order — pinned-package t0 dependency (repo standalone)

**Authored 2026-07-25 by Claude Code (executor) for Codex `gpt-5.6-sol`.** Spec lives in the vault; code lives in the repos (build-plan hard rule: *"code lives in a repo, spec lives here; wiki→repo pointers fine, never the reverse"*). **Do not add wiki-path references to any repo file you touch.**

> **You are authoring code only. Do NOT run** MLX, models, network calls, `pytest`, `pip`, build commands, or the harness (process rule: Codex is write/audit-only). Static inspection and editing — `rg`, `sed`, `git diff`, `apply_patch` — are in scope. Where verification requires execution, print the exact command and mark it **not run by Codex**; an executor supplies run artifacts.

## Decision (frozen by MK, 2026-07-25)

**Pinned-package, not vendored-copy.** Each repo becomes standalone — installs from its own metadata, no sibling-directory assumption, no borrowed interpreter — while `t0-morphology-furnace` remains the **single source of truth** for the sealed implementation, identified by tag.

Rationale, in one line: the harness's gen-1 parity check passes at `rtol 1e-5` against *the sealed implementation*; if each repo vendors its own copy of `pri_runtime` / `model_adapters`, that same passing check silently degrades to "matches our copy to 1e-5" — the test survives, the thing it tested does not. Vendoring is explicitly out of scope for this work order.

## Measured facts — do not re-derive

Verified 2026-07-25 by Claude Code. Treat as given.

| Fact | Value |
|---|---|
| t0 sealed core | **13 flat top-level `.py` modules** at repo root (list below) — no package directory, no `__init__.py` |
| t0 HEAD | `7c2fcb7` ("docs: center README on RPV") |
| Sealed tag | `t0-ace-sealed-2026-05-26` |
| **Sealed-module drift, tag → HEAD** | **none.** `git diff --stat t0-ace-sealed-2026-05-26 HEAD -- '*.py'` reports changes only under `exploratory/` and `paper/`; every root module is byte-identical |
| t0 packaging today | `requirements.txt` only — **no `pyproject.toml`, so t0 cannot currently *be* a dependency** |
| t0 `scripts/` | already a package (`scripts/__init__.py` present) |
| t0 visibility | **public** (`flowstyleliving/t0-morphology-furnace`) — a `git+https@tag` pin needs no credentials. The root `CLAUDE.md` still calls it "private"; that orientation line is stale |

The 13 sealed root modules: `attention_contribution.py`, `config.py`, `hidden_state_collector.py`, `model_adapters.py`, `pri_calibrator.py`, `pri_detector.py`, `pri_experiment_figures.py`, `pri_metrics.py`, `pri_runtime.py`, `pri_v2_io_plugins.py`, `pri_v2_mlx_pipeline.py`, `synthetic_logic_loader.py`, `synthetic_trace.py`.

Consumer coupling as it stands:

| Repo | Reach-across | Site |
|---|---|---|
| `empathy-geometry-harness` | `pri_runtime`, `model_adapters` via `sys.path` injection | `eg_harness/providers.py` — `_SIBLING_ROOT` (l.20), `_sibling_repo` (l.30–32), `_load_pri_runtime` (l.422+), `from model_adapters import …` (l.507) |
| `empathy-geometry-harness` | `mlx_furnace_scorer` from `furnace-guard/scripts` | `eg_harness/providers.py` — `_load_furnace_guard` (l.408–417) |
| `commit-confluence` | t0 via `CONFLUENCE_T0_REPO`, default `~/Documents/t0-morphology-furnace` | `sealed_selector.py` (l.187), `confluence_calibrator.py` (l.28, l.40) |

Already done, do not redo: `empathy-geometry-harness` commit `f74eccb` gave the harness a working `[build-system]`, package discovery, the missing `numpy` dependency, an `eg-harness` console script, and a `[geometry]` extra holding `mlx-lm`.

## The tag problem — read before writing D1

The sealed tag **predates packaging**, so `pip install git+…@t0-ace-sealed-2026-05-26` cannot work: that tree has no `pyproject.toml`. A new tag is required, and its trustworthiness rests on one assertion:

> **The 13 sealed modules at the new tag must be byte-identical to the 13 sealed modules at `t0-ace-sealed-2026-05-26`.**

D1 must make that assertion checkable by a single command, and the acceptance criterion is that the command prints nothing. This is the whole reason pinned-package preserves the parity guarantee; do not weaken it.

---

## D1 — Package t0 additively (no file moves)

**Repo:** `t0-morphology-furnace`. **This repo's sealed core is frozen** (vault HARD RULE). Packaging must be **purely additive**.

Author `pyproject.toml` at repo root:

- `[build-system]` → `setuptools>=68`, `setuptools.build_meta`.
- `[project]` → name `t0-morphology-furnace`, `version = "0.1.0"`, **`requires-python = ">=3.9"`** (frozen by MK — see Frozen decisions; do not raise it).
- **`[tool.setuptools] py-modules = [...]`** listing the 13 root modules verbatim, plus `packages = ["scripts"]`. `py-modules` exposes flat top-level files as importable modules **without moving them** — this is the mechanism that keeps the seal intact. Do not introduce a `src/` layout, a package directory, or an `__init__.py` at root.
- Dependencies: split `requirements.txt` into a minimal `dependencies` list (what `pri_runtime` / `model_adapters` actually import — `numpy`, `mlx`, `mlx-lm`; verify by reading imports, do not copy the file wholesale) and extras for the analysis/figure stack (`scipy`, `pandas`, `matplotlib`, `seaborn`, `scikit-learn`, `pyarrow`, `tqdm`). `pytest` belongs in a `dev` extra, not runtime.
- Leave `requirements.txt` in place and unmodified — `REPRODUCE.md` and the sealed run scripts may reference it.

**Forbidden in D1:** editing, moving, renaming, reformatting, or re-importing any of the 13 modules; touching `tests/`, `experiments/t0-sealed/`, or `paper/`; adding an `__init__.py` to the repo root.

**Deliverable also includes:** a short `PACKAGING.md` stating that the package exposes the sealed modules unmoved, that consumers must pin by tag, and how to cut the next tag if the sealed core is ever amended (it should not be).

**Tag (frozen): `t0-pkg-v0.1.0`**, cut on the packaging commit. Do not create the tag yourself (that is a git operation on a published repo) — print the command for the executor.

## D2 — Harness: swap `sys.path` injection for a declared dependency

**Repo:** `empathy-geometry-harness`, file `eg_harness/providers.py`.

- Delete the t0 branch of the reach-across: `_load_pri_runtime`'s `sys.path` manipulation, and the `_SIBLING_ROOT`-derived t0 path. Import `pri_runtime` and `model_adapters` as ordinary top-level modules.
- **Remove `EG_T0_REPO` rather than honoring it.** Replace with a clear failure: if `import pri_runtime` raises `ModuleNotFoundError`, raise a `RuntimeError` naming the extra to install (`pip install -e ".[geometry]"`) and stating that sibling-checkout resolution was removed deliberately. If `EG_T0_REPO` is set in the environment, say so in that message — a steward with it exported should learn it is now inert, not be silently ignored.
- Add the pinned dependency to the existing `[project.optional-dependencies] geometry` extra:
  `"t0-morphology-furnace @ git+https://github.com/flowstyleliving/t0-morphology-furnace@t0-pkg-v0.1.0"`
- Leave `_load_furnace_guard` **alone** in this work order (D4).
- Update `README.md` / `CLAUDE_HANDOFF.md` install instructions to the two-command form: `python3 -m venv .venv` then `pip install -e ".[geometry,dev]"`.

## D3 — commit-confluence: same swap

**Repo:** `commit-confluence`, files `sealed_selector.py`, `confluence_calibrator.py`.

Same pattern as D2: import t0 modules directly; retire `CONFLUENCE_T0_REPO` and its `~/Documents/...` default with an equally explicit error; add the same pinned dependency to `requirements-runtime.txt` **and** regenerate `requirements-analysis.lock.txt`. The lockfile regeneration is an executor step — print the command, do not run it.

⚠️ **Scope caution.** This repo is under registered pre-registration discipline and its `stage_b/profiles*` trees are sealed artifacts. Touch **only** the two named import sites and the requirements files. Do not modify anything under `stage_b/`, and do not alter `EXTENSION_MANIFEST.json` or any hash-frozen analyzer — a packaging refactor must not perturb a registered analysis path. If an import change would alter a module hash recorded in the manifest, **stop and report** rather than proceeding.

## D4 — furnace-guard (follow-on, lower priority)

`furnace-guard` has **no packaging metadata and no venv at all**, and reads commit-confluence calibration profiles through hardcoded `/Users/msrk/Documents/...` paths (`furnace_cli.py` l.821–823, `scripts/smoke_tests.py` l.24–28). It is the operator-facing guard and therefore the most likely to be run on another machine.

Author a `pyproject.toml` on the same additive pattern, exposing `scripts/mlx_furnace_scorer.py`, so the harness's `_load_furnace_guard` can become an ordinary import in a later pass. **Do not** change the guard's fail-closed behavior, thresholds, or profile-loading semantics — packaging only. Replace hardcoded absolute paths with a documented env var **plus** a sensible relative default, and state in the error message which one was consulted.

## ⚠️ PRE-FLIGHT HAZARD (found 2026-07-25, executor) — a sealed module is dirty right now

`t0-morphology-furnace` **HEAD is clean** — all 13 sealed modules are byte-identical to `t0-ace-sealed-2026-05-26`, confirming the measured-facts table above. But the **working tree is not**:

| Ref | Sealed-core state |
|---|---|
| `t0-ace-sealed-2026-05-26` | baseline |
| `HEAD` (`7c2fcb7`) | **all 13 byte-identical** ✅ |
| **working tree** | **`pri_calibrator.py` DRIFTED (+64 lines, uncommitted)** ❌ |

The uncommitted diff adds an opt-in `--attention-kv-tension` metric family (`ATTENTION_METRICS_KV_TENSION`, three new panels, a widened `_split_attention_label`), self-described in its own comment as "deliberately kept out of the sealed ACE default." Companion uncommitted edits sit in `scripts/diagnose_inter_head_disagreement.py` and `tests/test_attention_cells.py`.

Two things follow, and they are separable:

1. **Mechanical, blocking, Codex's problem.** `pri_calibrator.py` is #5 on the 13-module sealed list. If the packaging commit is created from this tree with a broad stage (`git commit -a`, `git add .`, `git add -A`), the KV-tension change rides into the commit and into `t0-pkg-v0.1.0` — and **A1 fails on a published tag**, which is the expensive way to discover it. **D1 must stage exactly the files it authors** (`pyproject.toml`, `PACKAGING.md`) and nothing else. Run A0 below before committing, not after.

2. **Governance, non-blocking, MK's call.** A sealed-core file is carrying uncommitted exploratory work at all. The vault HARD RULE freezes the sealed core; the change is additive and opt-in, which is the *spirit* of the rule, but it lives in a frozen file rather than in `exploratory/`. This does not block packaging — HEAD is what gets tagged — and is flagged here rather than acted on. **Do not commit, revert, stash, or relocate this diff as part of this work order.**

### A0 — pre-flight, run BEFORE the packaging commit

```bash
cd ~/Documents/t0-morphology-furnace
git status --porcelain -- \
  attention_contribution.py config.py hidden_state_collector.py model_adapters.py \
  pri_calibrator.py pri_detector.py pri_experiment_figures.py pri_metrics.py \
  pri_runtime.py pri_v2_io_plugins.py pri_v2_mlx_pipeline.py \
  synthetic_logic_loader.py synthetic_trace.py
```

Any output means a sealed module is dirty. **Commit `pyproject.toml` / `PACKAGING.md` by explicit path only**, then confirm with A0' that the commit did not absorb the drift:

```bash
git diff --stat HEAD~1 HEAD    # expect: only pyproject.toml and PACKAGING.md
```

### Sealed-core baseline — git blob SHA-1 at `t0-ace-sealed-2026-05-26`

Pinned here so A1 stays checkable even if a tag is mis-cut, and so a future steward can verify the seal without trusting any tag:

```
attention_contribution.py   aaf5a4bff5e24004d3af3e75b7eec745972102f2
config.py                   4fcad89a7f868a39ea9b7cf7d3150657bcf08178
hidden_state_collector.py   d551538f6c881fdc29d4d4e8c4744f117fa0170d
model_adapters.py           4b68dc5744ffc667e3b63e40eed052069c05591e
pri_calibrator.py           749151ad33f854fddce33b103537e39211fdaf74
pri_detector.py             b89df1711a79e7697648a5be4770daaa73af6d4c
pri_experiment_figures.py   5ce4fba3eac427275aee1a356040461ad6f87fb1
pri_metrics.py              fe1f26e42582b7fca1df444892fa7cf0caa69ef7
pri_runtime.py              1a117f4403256a2d1e67cef7811d2cc9cb43e709
pri_v2_io_plugins.py        a231154e38a40566b9c56ba6355fc4bfbbe70945
pri_v2_mlx_pipeline.py      b0637d8dbf2f790686b73988bd64d645a3f7359a
synthetic_logic_loader.py   6e0034b87045a4708a403ed44383dae75ab3ece4
synthetic_trace.py          8075fb2a427640b2c6e73060bf78a3f3b3263a3f
```

Verify any checkout against it with `git hash-object <file>` (these are content hashes, so they are independent of commit or tag).

## Acceptance criteria — executor commands, NOT run by Codex

```bash
# A1 — the load-bearing assertion: sealed core unchanged at the new tag.
#      MUST print nothing.
cd ~/Documents/t0-morphology-furnace
git diff t0-ace-sealed-2026-05-26 t0-pkg-v0.1.0 -- \
  attention_contribution.py config.py hidden_state_collector.py model_adapters.py \
  pri_calibrator.py pri_detector.py pri_experiment_figures.py pri_metrics.py \
  pri_runtime.py pri_v2_io_plugins.py pri_v2_mlx_pipeline.py \
  synthetic_logic_loader.py synthetic_trace.py

# A2 — t0 installs standalone from its own metadata, and the sealed modules import.
python3 -m venv /tmp/t0check && /tmp/t0check/bin/pip install -e .
/tmp/t0check/bin/python -c "import pri_runtime, model_adapters; print('t0 import OK')"

# A3 — t0's own sealed test slice still passes after packaging (additive => must be unchanged).
/tmp/t0check/bin/python -m pytest -q

# A4 — harness builds standalone and still passes, judge path with no MLX present.
cd ~/Documents/empathy-geometry-harness
rm -rf .venv && python3 -m venv .venv && .venv/bin/pip install -e ".[dev]"
.venv/bin/python -m pytest -q          # expect: 69 passed, 4 subtests passed

# A5 — geometry extra resolves the pinned tag, and the parity seal still holds.
.venv/bin/pip install -e ".[geometry,dev]"
.venv/bin/eg-harness check-gen1-parity  # expect PASS at rtol 1e-5

# A6 — no reach-across survives anywhere.
rg -n "sys\.path\.(insert|append)|EG_T0_REPO|CONFLUENCE_T0_REPO|_SIBLING_ROOT" \
  ~/Documents/empathy-geometry-harness/eg_harness \
  ~/Documents/commit-confluence/sealed_selector.py \
  ~/Documents/commit-confluence/confluence_calibrator.py
```

**A5 is the one that matters scientifically.** If `check-gen1-parity` fails after the swap, the pinned tag is not delivering the sealed implementation — stop, do not adjust the tolerance, and report. A parity failure here is a real finding about the packaging, not a threshold to tune.

## Non-goals

- No vendoring or copying of t0 code into any consumer. This was decided against; do not reintroduce it as a fallback.
- No restructuring of t0's layout (no `src/`, no package dir, no module renames).
- No changes to sealed profiles, manifests, hash-frozen analyzers, or registered analysis paths.
- No behavior changes anywhere — this work order changes *how code is found*, never *what it computes*. Any diff that alters a numeric path is out of scope by definition.
- No `git tag` / `git push` / `pip install` executed by Codex.

## Frozen decisions (MK, 2026-07-25) — no longer open

1. **Packaging tag: `t0-pkg-v0.1.0`.** The pin string in D2/D3 must match this exactly, character for character.
2. **t0 `requires-python = ">=3.9"`.**

### How the 3.9 floor resolves the interpreter contradiction

The apparent conflict — canonical venv on Python 3.9, harness declaring `>=3.11` — **dissolves once the reach-across is gone**, and it is worth stating explicitly so nobody "fixes" it later:

- Today the harness *borrows* t0's 3.9 venv, which is why its own `>=3.11` declaration was a lie.
- After D2 the harness has its own venv and **installs t0 into it as a dependency**. t0 at `>=3.9` installs happily on 3.11; the harness keeps `>=3.11`. Both declarations become true at the same time, and geometry runs in the harness's own interpreter rather than a borrowed one.
- Do **not** lower the harness to `>=3.9` as part of this work order, and do **not** raise t0 above `>=3.9`.

**Verified 2026-07-25 (Claude Code, executor):** all 13 sealed modules compile clean under **Python 3.11.15** (13/13, `py_compile` with `doraise`). So `>=3.9` is an honest declaration spanning 3.9 → 3.11 at the syntax level. Syntax-clean is not runtime-clean; A2 and A5 are what cover runtime.

### ⚠️ A5 is now also a cross-interpreter test — read this before running it

The gen-1 parity fixture (`tests/fixtures/gen1-parity.json`) was captured under **Python 3.9 + mlx_lm 0.29.1**. After D2, geometry recomputes inside the harness's **3.11** venv. A5 therefore tests two things at once: that the pinned tag delivers the sealed implementation, *and* that the parity result is interpreter-independent.

If A5 fails:

- **Do not adjust the tolerance.**
- **Do not re-capture the fixture.** The fixture is the reference point the seal is measured against; regenerating it under a new interpreter would destroy the very thing the check exists to protect, and would convert a real finding into a silent one.
- The correct fallback is to **pin the harness's geometry path to Python 3.9** (floor the harness at `>=3.9` and build its venv on 3.9), so the fixture's environment is reproduced exactly — then re-run A5. Report the failure either way: an interpreter-bound parity fixture is a genuine finding about the seal's portability and belongs in the log.
