# Empathy-geometry cell panels run standalone — bit-identical to the sealed venv (2026-07-26)

**Status:** `[RESOLVED]` — infrastructure/parity result. **Not** a detector verdict, not an arm-separation claim, not a prereg endpoint. Part of [[empathy-geometry/build-plan|Phase 2]] of [[empathy-geometry/README|Empathy Geometry]] (candidate #11).

**Repo:** `/Users/msrk/Documents/empathy-geometry-harness`, commits `7d05933` (backlog) + `2225ee4` (this work).

## The question

The [[empathy-geometry/build-plan|2026-07-25 runnability audit]] found the geometry half of the harness pinned to a borrowed interpreter: the 07-13 validation ran under `t0-morphology-furnace/.venv` (py3.9, mlx_lm 0.29.1, numpy 2.0.2), because *that* environment is what made the geometry recompute match the sealed implementation. The sealed venv has no `anthropic`, so `--judge anthropic` could not run where the geometry ran.

The two live options were: install `anthropic` into the sealed venv (perturbing the environment used for sealed reproductions), or split the run across two venvs on the [[results/gemma-scale-extension-2026-06-18|gemma-4 precedent]].

MK chose the split, and sharpened it: **make the cell panels run standalone in the EG repo.** That collapses the split in the right direction — the sealed checkout becomes a read-only import source and parity reference, and nothing is installed into it or written to it.

## What was actually blocking it

Three couplings, none of them intrinsic:

1. 🔗 **Geometry needed a judge.** Panels only ran as a side effect of `run-real`, which requires a full dialogue *and* a judge model. There was no way to score a prompt's geometry without also generating twelve turns and loading Gemma.
2. 📦 **The repo under-declared its environment.** `pyproject.toml` listed `mlx-lm` alone. The sealed modules the panels import pull more: `pri_runtime` imports **pandas** and **scikit-learn** at module load, and `comprehensive_run` (the independent canonical side) imports `sklearn.linear_model`. A steward following the repo's own metadata could not build a working env.
3. 🩹 **The only fixture producer was an ad-hoc script.** `artifacts/_capture_parity_fixture.py` monkeypatched three production seams, hardcoded absolute developer paths, and required a full judged run. It was never promoted, never tested, and is exactly how the capability drifted out of reach.

## What was built

- **`eg_harness/panel.py`** — `capture-panel` runs the 21-cell t=0 ACE attention panel and the gen-step-1 readout/surprise/PRI panel on plain prompts, with no dialogue, no persona bundle, and no judge. In `--mode replay` each row supplies its own recorded `first_token_id`, so **no sampler runs at all** and the capture reduces to two deterministic forward passes.
- **An opt-in `capture_sink`** on `providers._capture_gen1_readout_panel`, default `None`, recording the exact spectrum inputs. This is what removes the need to monkeypatch the production function. `capture_geometry` does not opt in; a test asserts it.
- **`compare-panels`** — diffs two capture documents cell by cell. Row identity (`prompt_sha256` + `first_token_id`) is checked **first**, and a mismatch is fatal for that row: metrics computed from different inputs produce a number that resembles agreement or disagreement but means neither.
- **A frozen replay corpus** recovered from the 07-13 run's stored `prompt_text`, verified to reproduce all six `prompt_sha256` values and all six `first_token_id`s of the existing parity fixture.
- **Exact version pins** for the full third-party closure, matched to the sealed venv. `transformers` is pinned because mlx-lm defers tokenization to it, and a tokenizer that disagrees with the sealed one moves every metric silently instead of failing loudly.

## Result

A replay capture under the EG repo's own interpreter reproduces the sealed-venv reference **bit-identically**.

| | EG venv | sealed venv |
|---|---|---|
| Python | 3.11.15 | 3.9.6 |
| numpy | 2.2.6 | 2.0.2 |
| mlx / mlx-lm | 0.29.3 / 0.29.1 | 0.29.3 / 0.29.1 |
| pandas / sklearn / transformers | 2.3.3 / 1.6.1 / 4.57.6 | 2.3.3 / 1.6.1 / 4.57.6 |

| Check | Scope | Result |
|---|---|---|
| Row identity | 6 rows, `prompt_sha256` + `first_token_id` | all identical ⇒ same inputs |
| t=0 ACE panel | 21 cells × 6 rows + 3 scalars/row | **worst relative delta 0.000e+00** |
| gen-step-1 strict metrics | 5 metrics × 6 rows | **worst relative delta 0.000e+00** |
| `compare-panels` total | **174 values** | **PASS** at rtol 1e-5 |
| `check-gen1-parity` (within EG venv, harness vs independent canonical) | 6 rows | PASS at rtol 1e-5 |
| Test suite | — | **99 passed, 4 subtests** (was 69) |
| Sealed archive after | `t0-morphology-furnace` porcelain + A0 gate | **clean, A0 PASS** |

Not merely within tolerance — **exactly equal**, across a Python minor-version jump and a numpy minor-version jump.

### Adversarial review corrected two claims on this page (same day)

A Codex `gpt-5.6-sol` static review found that the first version of this result was **stated more strongly than the code supported**. Both were fixed and the numbers re-derived; the corrections are recorded rather than quietly patched.

1. ❌ **"Bit-identical" was asserted but not tested.** `compare_captures` ran at `rtol=1e-5 / atol=1e-7`, and the reported `worst_relative_delta_among_failures` was computed *only over failures* — so it read `0.0` whenever everything passed, no matter how much drift sat inside tolerance. Quoting it as evidence of exactness was wrong. Near-zero attention cells (≈8.7e-7) made this concrete: `atol=1e-7` there permits \~10% relative drift. **Fixed:** the comparator now tracks `max_absolute_delta` and `max_relative_delta` **over every comparison, passing or failing**, supports an exact mode (`--rtol 0 --atol 0`), and reports `exact_mode` and `bit_identical` as separate fields. The regression test asserts both maxima are exactly `0.0`.
2. ❌ **"The claim cannot rot" was false.** The regression test loaded two frozen JSON files and never invoked the capture path — if capture were changed to echo stored values, it would still pass. **Fixed:** the README and the test docstring now state exactly what the suite guarantees (the recorded observation is preserved, the comparator logic is exercised) and what it does not (it does not re-run capture), with the two-command reproduction printed alongside.

**Re-verified after the fixes, with a genuinely fresh capture:** `capture-panel` re-run end to end, then compared in exact mode — **`bit_identical: true`, `max_absolute_delta: 0.0`, `max_relative_delta: 0.0`, 174 values, 6 rows.** The comparator was then shown to be capable of failing: a **single-ULP perturbation (1.7e-21)** on one attention cell is rejected in exact mode while passing under default tolerance. Suite **113 passed, 4 subtests**.

Three further findings were also fixed: the canonical `surprise` column was an **echo** of the input corpus, not a `comprehensive_run` recomputation (renamed `recorded_generation_surprise`, provenance says so; it never entered the 174); `numpy` was **unpinned** while the prose said "pinned exactly" (now `numpy==2.2.6` in the geometry extra, with the 2.0.2-vs-2.2.6 span recorded as deliberate); and `compare_captures` was **vacuous on degenerate input** (empty row sets passed, duplicate `row_id`s silently overwrote). Plus: replay is **three** forward passes, not two.

## What this does and does not license

✅ **Licensed:** the geometry half of the harness no longer depends on a borrowed interpreter. `pip install -e '.[geometry,dev]'` from the repo's own metadata produces an environment that reproduces the sealed numbers. The hosted judge and the panels can now run in one venv without touching the sealed checkout.

🚫 **Not licensed:** this is a parity result on **6 rows from one bundle/arm (B2/giraffe) on one model**. It says the *instrument* transfers across interpreters; it says nothing about empathy geometry, arm separation, or any detector claim. Raw geometry remains uncalibrated.

⚠️ **Scope caveat:** bit-identity was measured on Qwen2.5-7B-4bit only. Other models on the ladder are unverified — the pins make it *likely* to hold, not proven.

## A commit-hygiene error, recorded

The commit message for `2225ee4` says the backlog was committed separately "so history separates prior work from this session's." **That is not true for four files.** `providers.py`, `cli.py`, `pyproject.toml`, and `README.md` were *already modified* in the working tree before this session, so staging them for the panel commit swept the pre-existing backlog changes (bundle registry, PRI-namespace rename, `arm_token_counts`, `geometry_selection`) into a commit whose message describes only the `capture_sink` addition. The separation holds for every other file.

This also produced a downstream artifact: the adversarial review attributed the `pri`/`rpv` return-shape change to the `capture_sink` work, because that is what the commit claims. The code is right; the history is misleading. Not rewritten — the harness commits are unpushed, so a re-split is possible, but the content is identical either way and rewriting risks more than it fixes. Flagged for MK rather than silently corrected. **Lesson: staging by explicit path is necessary but not sufficient — a file already dirty for another reason carries that reason with it.**

## Method note worth carrying forward

The first error message I wrote for the canonical-import failure blamed the wrong thing: it told the reader to set `EG_T0_REPO` when the checkout was found correctly and the interpreter was simply missing `sklearn`. Those two failures need opposite fixes. The handler now branches on `ModuleNotFoundError.name` and names the missing dependency. **A diagnostic that confidently names the wrong cause is worse than no diagnostic**, because it spends the reader's attention in the wrong place — the same class of error as the shell-loop false positives logged on 2026-07-25.

## Open

- 🔓 The **four ⟨MK⟩ freezes** (R1–R4) remain the hard gate on Phase 3; this work does not touch them.
- 🧩 **Deliverable B (POV panel)** remains unimplemented — the pre-registration seam.
- 💰 Hosted-judge **cost authorization** still outstanding. Credentials: an `ANTHROPIC_API_KEY` **is** present in the harness `.env` (contrary to the 07-25 audit line), unverified as live.
- 🧪 Cross-model bit-identity beyond Qwen2.5-7B is unmeasured.

## Backlinks

- [[empathy-geometry/build-plan]] — Phase 2
- [[empathy-geometry/harness-completion-status-2026-07-13]] — the prior executor run
- [[results/gemma-scale-extension-2026-06-18]] — the split-venv precedent
- [[log]] 2026-07-26
