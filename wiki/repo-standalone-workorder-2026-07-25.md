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
- `[project]` → name `t0-morphology-furnace`, `version = "0.1.0"`, `requires-python` set from what the sealed modules actually parse under (the canonical venv is **Python 3.9**; do not raise this floor without evidence — the harness's own `>=3.11` already contradicted its runtime once).
- **`[tool.setuptools] py-modules = [...]`** listing the 13 root modules verbatim, plus `packages = ["scripts"]`. `py-modules` exposes flat top-level files as importable modules **without moving them** — this is the mechanism that keeps the seal intact. Do not introduce a `src/` layout, a package directory, or an `__init__.py` at root.
- Dependencies: split `requirements.txt` into a minimal `dependencies` list (what `pri_runtime` / `model_adapters` actually import — `numpy`, `mlx`, `mlx-lm`; verify by reading imports, do not copy the file wholesale) and extras for the analysis/figure stack (`scipy`, `pandas`, `matplotlib`, `seaborn`, `scikit-learn`, `pyarrow`, `tqdm`). `pytest` belongs in a `dev` extra, not runtime.
- Leave `requirements.txt` in place and unmodified — `REPRODUCE.md` and the sealed run scripts may reference it.

**Forbidden in D1:** editing, moving, renaming, reformatting, or re-importing any of the 13 modules; touching `tests/`, `experiments/t0-sealed/`, or `paper/`; adding an `__init__.py` to the repo root.

**Deliverable also includes:** a short `PACKAGING.md` stating that the package exposes the sealed modules unmoved, that consumers must pin by tag, and how to cut the next tag if the sealed core is ever amended (it should not be).

**Proposed new tag:** `t0-pkg-v0.1.0`, cut on the packaging commit. Do not create the tag yourself (that is a git operation on a published repo) — print the command for the executor.

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

## Open decisions for MK

1. **Tag name** — `t0-pkg-v0.1.0` is a proposal. If you prefer the packaging tag to read as a sibling of the seal (e.g. `t0-ace-sealed-2026-05-26+pkg1`), say so before D1 lands; the pin string in D2/D3 must match exactly.
2. **`requires-python` floor for t0** — the canonical venv is Python 3.9 while the harness declares `>=3.11`. Packaging forces this contradiction into the open. Either t0 declares `>=3.9` (and the harness's geometry path must then actually run on the interpreter it declares), or the canonical env moves to 3.11 — which would require re-capturing the gen-1 parity fixture and is therefore **not** a packaging decision.

Item 2 is the one that can bite. Flag it in the D1 deliverable rather than choosing silently.
