# Modal Cloud Extractor Reference

**Last updated:** 2026-06-30
**Audience:** anyone running or extending the commit-confluence panel on larger models — Claude, Codex, reviewers, future MK.
**Status:** historical backend reference. The live `furnace-guard` repo has been de-clouded and now runs the cached Qwen2.5-7B 4-bit model locally through MLX on the Mac mini M4. `furnace tui` is a persistent score-before-generation chat session with first-run model selection and local calibration; `score` and `wrap` retain the one-shot fail-closed contract. See `/Users/msrk/Documents/furnace-guard/README.md`. The bundled profile is ANLI-calibrated and must not be described as a general harmful-prompt safety classifier.

---

## What this is

A PyTorch/HF port of the sealed commit-confluence extractor, built to run models **larger than local MLX can hold** (the gemma-4-12B local run swap-thrashed for ~7.5h; 30B–70B+ are out of reach on the Mac). It runs on **Modal** NVIDIA GPUs (A100-80GB).

- Code: `/Users/msrk/Documents/furnace-guard/modal_app.py`
- Vendored sealed kernels: `/Users/msrk/Documents/furnace-guard/seal/` (verbatim copies; see `/Users/msrk/Documents/furnace-guard/seal/PROVENANCE.md` for sources + sha256)

### The one architectural fact
The sealed pipeline is **MLX** (Apple-Silicon only). Modal is **NVIDIA**, so model forwards must be **PyTorch/HF**. The split that made gemma-4 tractable applies again:

- 🔌 **Extraction** (forward + attention/value/hidden capture + logits + W_u) — framework-specific; reimplemented in torch. The *only* new code.
- 🧮 **Calibration** (panel sweep, nested-OOB selection, merge, fusion, controls) — pure numpy/sklearn; the **sealed kernels run verbatim** (`pri_calibrator._compute_attention_score`, `pri_runtime.PRIComputer.compute_step`, `comprehensive_run._support_spectrum`/`_spectrum_stats`, `confluence_calibrator.merge_matrices`/`calibrate_merged`).

So this is a **third extractor backend**, sibling to the mlx-lm seal and the mlx-vlm gemma-4 extractor.

### ⚠️ Comparability (read this twice)
Every result from this backend is **NON-byte-comparable** to the seal (torch + bf16/4-bit vs MLX-4bit, reimplemented capture). Treat each cell like the gemma-4 cell: a **standalone exploratory panel**, **never pooled** with the sealed or byte-comparable cells. The extractor stamps `comparability.byte_comparable_to_mlx_seal = false` and `backend = "modal-torch"` into every `.profile.json` and matrix `meta`.

---

## Loci & faithfulness (ties to [[commit-locus]])

The torch extractor preserves the **two-loci / D0–D1 split** exactly:

| Locus | This backend | Reads |
|-------|--------------|-------|
| **t=0** (prefix-last) | forward **A** on the chat-templated prompt | ACE attention caps + `h_prev` + surprise; commit `gid = argmax(D0)` |
| **gen_step=1** (first gen token) | forward **B** on `[prompt + gid]` | `p_t`, `p_max`, `h_t` → PRI null_ratio, RPV spectrum, confidence |

- 🎯 **eager attention** (`attn_implementation="eager"`) so `outputs.attentions` ARE the model's own softmax weights — ACE reads the model's attention directly, no recompute.
- 🔬 **`cos≈1.0` faithfulness gate**: `validate()` reconstructs `o_proj(Σ_t w·v)` from captured weights+values and compares to the model's real `self_attn` output. Verified **cos = 1.0** on Qwen2.5-32B and Qwen2.5-72B (incl. 4-bit). This is the torch analogue of the MLX `G4Wrap` o_proj check.
- 💬 **chat template required**: instruction-tuned models won't attempt the YES/NO task on a raw prompt (the gemma-4 lesson — ~0.37 noise). `_chat_ids` applies `apply_chat_template` and raises clearly if a tokenizer has none.

---

## Fail-closed gates

The extractor **aborts loudly** rather than emit a misleading verdict:

- 🚦 `validate()` **raises** unless every example has `cos ≥ 0.999` (capture faithful) **and** a YES/NO commit (task attempted).
- 📉 `extract()` **raises** if `n_dropped > max_dropped` (param, default 0) or if the YES/NO commit rate `< 50%` (the gemma-4 "task not attempted" signature).
- 🖥️ `_load()` **raises** for 70B/72B bf16 on `<2` GPUs (use `--load-in-4bit` or `GPU_CONFIG="A100-80GB:2"`).
- 🪝 `_forward()` clears its hook caches each call and **raises** if a hook didn't fire or `out.attentions is None` (kills stale cross-forward bleed).
- 🔩 `_output_weight_numpy()` **raises** if `lm_head` is non-floating (a quantized lm_head cast to float32 = garbage W_u → garbage null_ratio/fisher).

Results persist to the **volume** (`/models/validate/…json`, `/models/profiles_ext/<task>/<slug>.profile.json`) so they survive Modal's "final app logs" flush race + tqdm ANSI overwrites — fetch with `modal volume get`.

---

## How to run

One-time:
```
pip install modal && modal setup
modal secret create huggingface HF_TOKEN=$(cat ~/.cache/huggingface/token)
```

Volume `model-cache` is mounted at `/models`. Stage benchmark data + seal-reference matrices at **volume-root** (NOT under `/models/…`, which double-nests — see gotchas):
```
modal volume put model-cache <local>.jsonl  /data/<task>_n200.jsonl
modal volume put model-cache <local>.npz    /refs/<task>.matrix.npz     # gemma-3-12b ref = readout panel order
```

Stress-data builder for the current Qwen2.5-32B exploratory panel (ANLI R2/R3, TruthfulQA-MC, HaluEval QA/dialogue/summarization):
```
modal run /Users/msrk/Documents/furnace-guard/modal_app.py --mode build-stress-data --task all --n 200
```
It writes `/models/data/<task>_n200.jsonl`, `/models/data/<task>_n200.manifest.json`, and `/models/refs/<task>.matrix.npz` on the Modal volume. It needs an existing `/models/refs/anli_r1.matrix.npz` only for the readout-panel order copy.

Run (validate gate first, then extract):
```
modal run /Users/msrk/Documents/furnace-guard/modal_app.py::validate --model-id Qwen/Qwen2.5-32B-Instruct --task anli_r1
modal run /Users/msrk/Documents/furnace-guard/modal_app.py::extract  --model-id Qwen/Qwen2.5-32B-Instruct --task anli_r1
```

GPU sizing (bf16; ~half for 4-bit): 14B→A100-40GB · 32B→A100-80GB · 70B/72B→`--load-in-4bit` on one 80GB **or** `A100-80GB:2`. The 4-bit config skips `lm_head`/`embed_tokens` from quantization so W_u stays floating.

## TUI / wrapper guard (`furnace`, added 2026-06-25)

The first operator-facing wrapper lives at `/Users/msrk/Documents/furnace-guard/furnace` (`/Users/msrk/Documents/furnace-guard/furnace_cli.py`). It calls a new Modal `guard_prompt()` path that loads the fitted profile + score matrix from `/models/profiles_ext/<task>/`, computes the selected Furnace metric for one prompt, derives a conservative threshold from the stored calibration matrix, and returns one of:

- `ALLOW` — below the calibrated risk threshold; wrapped command may run.
- `BLOCK` — above threshold; no wrapped command output is emitted.
- `ABSTAIN` — inside the uncertainty band around the threshold.
- `DEFER` — fail-closed: missing profile/matrix, non-deployable profile, controls fail, unsupported fusion winner, or guard error.

For `Qwen/Qwen2.5-32B-Instruct` the current winners are ACE attention cells, so the score is available from the prompt-only t=0 forward pass (`pre_detokenization=true`) before any response text is generated. Readout winners still remain pre-response-text, but require the commit-token forward.

Commands:
```
/Users/msrk/Documents/furnace-guard/furnace score --prompt "..."                         # real Modal guard
/Users/msrk/Documents/furnace-guard/furnace wrap  --prompt "..." -- <cli-agent command>   # suppresses command unless ALLOW
/Users/msrk/Documents/furnace-guard/furnace tui -- <cli-agent command>                    # interactive terminal guard

# real prompt checks against the Modal guard
/Users/msrk/Documents/furnace-guard/furnace score --prompt "ordinary factual question"
/Users/msrk/Documents/furnace-guard/furnace wrap --prompt "ordinary factual question" -- python -c 'print("runs only on ALLOW")'
```

`furnace wrap` pipes the prompt to the wrapped command's stdin and sets `FURNACE_PROMPT` + `FURNACE_GUARD_JSON` in the environment. Exit codes: `0=ALLOW/ran`, `30=BLOCK`, `31=ABSTAIN`, `32=DEFER`.

Real smoke (2026-06-25): installed Modal CLI via `pipx`, confirmed `model-cache` volume visibility, then ran `/Users/msrk/Documents/furnace-guard/furnace score --prompt "ordinary factual question"` against the default `Qwen/Qwen2.5-32B-Instruct` nf4 profile. The guard returned `BLOCK`, winner `attention[last_minus_1_js] @ step 0`, `pre_detokenization=true`. A real `/Users/msrk/Documents/furnace-guard/furnace wrap ... -- python -c 'print("SHOULD_NOT_PRINT_REAL")'` also returned `BLOCK` and suppressed the wrapped command output.

2026-06-26 cleanup: the CLI is now real-only; every `furnace score` / `wrap` / `tui` path calls the Modal guard or fails closed. Baked the frozen `guard_policy` into the existing Qwen2.5-32B nf4 ANLI profile from its stored calibration matrix, then reran `/Users/msrk/Documents/furnace-guard/furnace score --prompt "ordinary factual question" --json`; the guard returned `ABSTAIN`, `frozen_policy=true`, `pre_detokenization=true`, and `response_text_emitted=false`.

---

## Precision ladder (`--precision`, wired 2026-06-22)

`_load` now takes `--precision {nf4|int8|bf16|fp32}` (legacy `--load-in-4bit` still works → resolves to `nf4`). **`nf4` reproduces the historical 4-bit `BitsAndBytesConfig` byte-for-byte**, so existing 4-bit profiles stay reproducible; `int8` keeps `lm_head`/`embed_tokens` floating exactly like `nf4` (W_u stays a floating tensor); `bf16`/`fp32` are unquantized. Higher rungs write **per-rung artifacts** `…__<precision>.{profile.json,matrix.npz}` and `validate/<slug>__<precision>_<task>.json` (nf4 keeps the legacy bare name so nothing orphans), and every profile self-labels via `comparability.precision`. The 70B/72B single-GPU OOM guard now fires for **any ≥16-bit rung**, not just bf16 (use `nf4`/`int8` on one 80GB, or `A100-80GB:2` for bf16). Experiment design + pre-registered hypotheses + the H3 quantization-artifact falsifier: [[../results/precision-ladder-prereg-2026-06-22]].

## The MLX import shim (why the seal kernels import on Linux)

MLX cannot install on Modal's x86 Linux. `_import_seal()` injects stub modules before importing the seal:

- `mlx`, `mlx.core`, `mlx.nn`, `mlx_lm`, `pri_v2_mlx_pipeline` — registered in `sys.modules`.
- **Each stub carries a real `__spec__`** (`importlib.machinery.ModuleSpec`). A hand-made `ModuleType` has `__spec__=None`, which makes `importlib.util.find_spec("mlx")` **raise** — and `transformers` calls exactly that at import (`is_mlx_available`). With a spec present, `transformers` then checks installed metadata → `PackageNotFoundError` → correctly sees mlx as **unavailable**, while the seal's `import mlx` still resolves.

Verified: the kernels we call never invoke `mx` / the MLX pipeline at runtime (the ACE morphology helpers in `diagnose_inter_head_disagreement` are pure-numpy; `pri_v2_mlx_pipeline.safe_auroc` is only on the CLI path).

---

## Gotchas log (first bring-up, 2026-06-21/22)

Each was caught **before** burning GPU (cheap pre-download failures):

| ❌ Symptom | 🩹 Cause / fix |
|-----------|---------------|
| `FileNotFoundError /models/data/anli_r1_n200.jsonl` | `volume put … /models/data/…` writes to volume-root `models/data/…`, which **double-nests** under the `/models` mount. Upload to `/data/…`, `/refs/…` instead. |
| `ValueError: mlx.__spec__ is None` | stub modules lacked `__spec__`; `transformers.is_mlx_available` → `find_spec` raised. Fixed by giving every stub a `ModuleSpec`. |
| empty/clobbered result in logs | Modal "Timed out waiting for final app logs" + tqdm ANSI overwrite ate the printed verdict. Fixed by persisting to the volume. |
| `GatedRepoError 403` (Llama-3.3-70B) | HF token not authorized for the gated Meta repo — request access; not a code bug. **Resolved 2026-06-22: HF access approved; the token now sees the repo.** |
| (latent) quantized lm_head | untied 70B/72B under default 4-bit would quantize lm_head → garbage W_u. Fixed: skip lm_head/embed_tokens from quant + the floating-dtype guard. |

Also: launch runs with **absolute paths** (`modal run /abs/path/modal_app.py::fn`) or from `/Users/msrk/Documents/furnace-guard`; relative paths fail when the shell cwd is elsewhere.

---

## Results so far (Modal/torch, NON-byte-comparable)

Qwen2.5 scale axis (extends the byte-comparable [[results/gemma-scale-extension-2026-06-18|gemma/scale extension]] upward, but as a *separate* torch panel):

**Precision provenance (corrected 2026-06-23):** the pre-patch runs were NOT precision-stamped, and a byte-identity check revealed the original 32B baseline was run in **bf16** (no `--load-in-4bit`), not 4-bit. True-nf4 32B has since been run and stamped. 72B precision is **inferred nf4** (the OOM guard blocks 72B-bf16 on one GPU) but not byte-verified. Llama-70B is stamped nf4. See [[../results/precision-ladder-results-2026-06-22]].

| Model | Task | precision | geom CI-lo | deployable | winner |
|-------|------|-----------|-----------|------------|--------|
| Qwen2.5-32B | anli_r1 | bf16 | 0.790 | ✅ | `attention[last_minus_1_bos_mass] @ step 0` |
| Qwen2.5-32B | anli_r1 | nf4 | 0.763 | ✅ | `attention[last_minus_1_js] @ step 0` |
| Qwen2.5-32B | triviaqa | bf16 | 0.822 | ✅ | `attention[last_minus_1_v_norm_lastq_weighted] @ step 0` |
| Qwen2.5-32B | triviaqa | nf4 | 0.781 | ✅ | `attention[final_bos_mass] @ step 0` |
| Qwen2.5-32B | anli_r2 | nf4 | 0.744 | ✅ | `attention[last_minus_1_bos_mass] @ step 0` |
| Qwen2.5-32B | anli_r3 | nf4 | 0.698 | ✅ | `attention[last_minus_1_bos_mass] @ step 0` |
| Qwen2.5-32B | truthfulqa_mc | nf4 | 0.730 | ✅ | `attention[last_minus_1_js_kv_groups] @ step 0` |
| Qwen2.5-32B | halueval_qa | nf4 | 0.809 | ✅ | `Fusion fusion_rank_mean_geom @ step 0` |
| Qwen2.5-32B | halueval_dialogue | nf4 | 0.539 | ✅ | `Readout null_ratio_post_rank1 @ step 0` |
| Qwen2.5-32B | halueval_summarization | nf4 | 0.553 | ✅ | `Readout fisher_eff_rank @ step 0` |
| Qwen2.5-72B | anli_r1 | nf4 (inferred) | 0.639 | ✅ | `attention[last_minus_1_js_no_bos] @ step 0` |
| Qwen2.5-72B | triviaqa | nf4 (inferred) | 0.918 | ✅ | `attention[last_minus_1_js] @ step 0` |
| Llama-3.3-70B | anli_r1 | nf4 | 0.703 | ✅ | `Readout neg_shadow_logvol_r1 @ step 0` (RPV — **not** ACE) |
| Llama-3.3-70B | triviaqa | nf4 | 0.788 | ✅ | `Readout fisher_eff_rank @ step 0` (RPV — **not** ACE) |

Read: **all four Qwen2.5 scale cells (32B + 72B) are ACE attention at the penultimate layer, winning *solo*** — the same morphology family as the byte-comparable scale cells, **not** the gemma-4 fusion pattern. The 72B winners shift to the **inter-head JS-divergence** ACE sub-cells (`js_no_bos`, `js`) vs the 32B `bos_mass`/`v_norm` sub-cells — same layer + family, different morphology read (cf. the long-open [[../results/inter-head-disagreement-2026-05-15|inter-head JS-radius]] thread). 72B/anli geom CI-lo dips to 0.639 (vs 32B 0.790) but stays deployable; triviaqa stays high (0.918). Faithfully reproduced on torch (cos=1.0) on hardware the MLX seal can't run. **Precision note (2026-06-23):** the 32B numbers above are **bf16** (original run); the **true-nf4 32B** rung was run separately (anli 0.763 / triviaqa 0.781) and **also wins ACE attention** — so the attention-locus result is precision-robust, not a bf16 artifact.

**Qwen2.5-32B stress update (2026-06-25):** with the six new nf4 tasks above, Qwen2.5-32B is **8/8 deployable** across the current torch stress panel. ANLI R2/R3 and TruthfulQA-MC preserve the attention-locus reading. HaluEval broadens it: QA is strong but Fusion, while dialogue/summarization are marginal deployable and move to readout/surprise. So "Qwen -> attention" is correct for the ANLI/TriviaQA scale panel and TruthfulQA, but should not be over-read as a universal Qwen-family locus for broader grounded-dialogue/source-faithfulness prompts. Detail: [[../results/qwen32b-stress-2026-06-25]].

**Llama-3.3-70B breaks the ACE-solo pattern — a FAMILY DISSOCIATION.** Both Llama cells are deployable (anli_r1 0.703, triviaqa 0.788; n=200/200, controls pass) but **both win on RPV readout geometry at gen_step=1, not ACE attention at t=0**: anli → `neg_shadow_logvol_r1`, triviaqa → `fisher_eff_rank`. So the *locus* of the signal is family-dependent — **Qwen → attention-morphology (preparation state); Llama → readout-volume (commit state)** (see [[commit-locus]]). **De-confounded 2026-06-23:** this was at risk of being a precision artifact (Llama ran nf4, 32B ran bf16), but the true-nf4 32B run wins ACE attention too — so at *matched* nf4 precision Qwen=attention and Llama=readout. The dissociation is real, not a bf16-vs-4bit confound. Separately, Llama-70B/anli at 0.703 **resolves the sealed `Llama-3.1-8B/anli` orphan as a small-model artifact** — the second sealed ANLI orphan to close at scale, after gemma (gen-3-12b 0.709 / gen-4 0.691). Both orphans confirmed scale artifacts, via two independent families. Detail: [[../results/llama-70b-scale-2026-06-22]].

---

## Cross-references
- [[commit-locus]] — the t=0 / gen_step=1 loci this backend preserves (canonical for signal semantics)
- [[results/gemma-scale-extension-2026-06-18]] — the byte-comparable scale/generation axis (gemma-3-12b, Qwen2.5-14B, gemma-4-12B)
- `/Users/msrk/Documents/furnace-guard/seal/PROVENANCE.md` — vendored module sources + hashes
- Repo: the sealed dispatcher lives in `commit-confluence/` (public: github.com/flowstyleliving/commit-confluence)
