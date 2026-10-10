# MoE depth curves — scoping audit and proposed router pilot (2026-10-08)

**Status: COMPLETE — pilot run 2026-10-08, spending decision STOP; archived.** Result:
[[results/router-pilot-2026-10-08]]. 545 GPU-seconds of the 2-hour cap. The build history below is kept as
provenance.

**Build status at authorization: AUTHORIZED (MK, 2026-10-08: "Router pilot. Audit w codex.") — BUILT, AWAITING ROUND-3 CODEX
AUDIT; nothing run on GPU, $0 spent.** Lane: `commit-confluence/exploratory/router-pilot/` (uncommitted).

- 🧭 **Design audit, round 1 — RED; all 7 MAJOR + 3 MINOR accepted.** ANLI null, bootstrap spec, a
  tautological router gate replaced by an MoE reconstruction gate, `clip_qkv`/`head_dim` asserts,
  serialization, budget/terminal states, an independent Modal environment (the grid-B image's
  `huggingface_hub==1.27` conflicts with transformers 4.57.6). `v_norm_bos` found constant by
  construction → diagnostic only ([[results/three-instrument-2026-09-06]] addendum). The estimand moved
  **before any smoke** to final-prompt-state discrimination; YES/NO compliance is descriptive.
- 🛠️ **Code, round 2 — Codex authored** `modal_router_pilot.py`, `score_router_pilot.py`,
  `make_freeze.py`, README; fixed 2 more MAJORs in the text (seeds/ties, lifecycle).
- 🔎 **Steward review.** Three defects, which the steward patched itself after Codex hit its usage
  limit (a disclosed exception to the Codex-authors split): a failed GPU call charged the whole
  remaining budget; a smoke crash could never be repaired; weights downloaded on the GPU clock. A
  fourth finding was withdrawn as the steward's own error. Policy added (pre-registration
  "Round-3 clarifications"): measured-gate failures are terminal; other smoke failures are
  mechanical and need a dated amendment that cannot touch sections 1–8.
- ✅ **Executor checks.** All pins exist; Python 3.12 executor venv built; the scorer recovered a
  planted router signal and is calibrated on noise (0.50 ± 0.06 over 300 seeds); every freeze and
  amendment rule exercised in a scratch copy.
- 🗑️ **`v_norm_bos` deprecated (MK, 2026-10-08), before FREEZE-1.** No longer captured. Replaced by a
  descriptive `sink_draw` = mean over heads of A[T−1, 0] · ‖V₀‖ per block, scored as `sink_best` outside the
  comparator set and the spending rule, with its per-block rank correlation to `bos_mass` reported (is it more
  than a reweighted `bos_mass`?). Scorer re-tested on synthetic data with a planted sink signal.
- ⏳ **Next.** Round-3 Codex audit (auto-launched 15:19:30 after the usage reset) → FREEZE-1 → smoke.
Originally PROPOSED — NOT AUTHORIZED; no code had been written and no compute
spent. This page records the Codex scoping audit of the "MoE depth curves" next step named in
[[research-candidates]] #13 and [[paper/dc-scaffold]], and the leanest design the audit would sign
off on, so that the pilot can start from here if MK says go.

## Audit verdict (Codex `gpt-6-astra`, read-only, 2026-10-08; claims verified by the steward)

"MoE depth curves" hides three different questions, and only one is worth money now.

- 🪞 **Do the dense-grid regularities appear in MoE models?** Legitimate but low priority. There is no
  placement law to transfer, and new MoE successes cannot repair the registered terminal-dip miss
  (E5 WEAKEN 8/12). The DC draft is frozen and depends on no unrun compute (MK, 2026-09-06).
  **Defer.**
- ⚖️ **Dense-vs-MoE sibling pairs.** Observational and confounded by far more than routing.
  Qwen3-30B-A3B is 48 layers / 32 query / 4 KV heads; Qwen3-32B is 64 / 64 / 8. No available pair
  isolates the routed FFN. **Drop.**
- 🔀 **Router uncertainty at the commit token, per layer.** The only MoE-native object: dense models
  have no router. **A capped pilot is defensible.**

## Engineering hazards (verified in code)

- 🕳️ **The grid-B quantizer audit can pass falsely on MoE.** `_enforce_decoder_quantizers`
  (`modal_depth_b.py:425`) inspects only leaf modules with a 2-D `.weight`. Fused 3-D expert
  parameters already exist in the local transformers 4.57.6 (`llama4/modeling_llama4.py:53`, gpt-oss),
  and q/k/v/o alone satisfy the coverage floor. Experts could stay bf16 under an "all nf4" label.
- 🎛️ **Skipping the router from quantization does not preserve routing.** Quantized attention and
  experts upstream still change the router's inputs. Run MoE cells in bf16.
- 🔤 **No BOS on Qwen-family tokenizers.** Grid B's `_verify_bos` hard-fails. Grid A's `_chat_ids`
  never checked, and the sealed kernel's "no BOS" simply drops position 0. Never insert an artificial
  BOS to satisfy the gate.
- 🚫 **Excluded architectures.** Qwen3-Next (3 of 4 blocks are linear attention — no attention map)
  and DeepSeek V2/V3 (MLA has no `v_proj`, so the o_proj reconstruction gate cannot run). gpt-oss's
  attention sink is an extra softmax column that is renormalized away — a different mechanism from
  gemma-3-27b's BOS collapse, but still needs its own gate work. Llama-4's NoPE layers do not break
  the instrument; its multimodal wrapper needs descriptor work.
- 🧩 **Interleaved dense/MoE stacks** (DeepSeek first-k-dense, Llama-4 Maverick): dense layers have a
  **missing** router value, never zero entropy.
- 🧬 **HaluEval is stem-paired** and the frozen folds ignore it. Checked the same day on the banked
  grids: every registered call survives — [[results/stem-grouped-sensitivity-2026-10-08]]. Any new
  scorer must build stem-grouped folds and resample stems.

## Proposed pilot (if authorized)

- **Goal.** Does router uncertainty at the commit token separate the frozen task labels, at which
  depth, and how does it compare held-out with the attention metrics?
- **Model.** One: `allenai/OLMoE-1B-7B-0924-Instruct` — 16 layers, 16 query / 16 KV heads (MHA),
  64 experts, top-8, MoE in every block, fully open data. Native bf16, eager attention, batch 1,
  one 24 GB GPU, no offload. Pin the full checkpoint SHA, tokenizer files and image digest.
  Timing and memory are unmeasured estimates.
- **Data.** The two frozen n=200 files (sha256-enforced), stem-grouped folds.
- **Instruments, all named before capture.** All seven attention metrics (`js`, `js_no_bos`,
  `js_kv_groups`, `bos_mass`, `v_norm_bos`, `v_norm_max`, `v_norm_lastq_weighted`; on MHA
  `js_kv_groups` duplicates `js` — keep the field, deduplicate selection). Router: normalized
  full-distribution entropy `H(p)/log 64` and boundary margin `p(8) − p(9)` at the last prompt
  position; selected expert IDs and weights recorded as provenance only. All seven attention metrics
  are mandatory here (the grid-B v-norm channel was best-effort).
- **Comparators, all named before capture.** Train-selected best attention metric and depth;
  train-selected best router metric and depth; output `p_max`, output entropy, and prompt length,
  each alone. Same folds for all.
- **Analysis.** Prospective descriptive registration, not a confirmatory grid C. Five stem-grouped
  folds; directions and selection training-only; ties broken by declared metric order, then the
  shallower block. Stem-cluster bootstrap (1000). Report curves, selection dispersion and paired
  intervals. No transferable-placement claim.
- **Smoke gates (labels hidden).** Rows 0–9 plus the longest row per task: correct shapes, one capture
  per block, finite metrics, router top-8 agreement, o_proj reconstruction cos ≥ 0.999 at **every**
  layer, ≥ 9/10 YES/NO commits per task. Three repeats of the longest forward: stable expert IDs, peak
  reserved ≤ 20 GiB, growth < 0.5 GiB.
- **Budget.** Hard cap **2 GPU-hours including smoke**; require
  `load + 400 × p95_forward × 1.2 ≤ 2 h`. Any failure stops the pilot: no larger-GPU escalation, no
  prompt rescue.
- **Full extraction** needs 200/200 rows and ≥ 90% YES/NO per task; score once after both terminal
  statuses.
- **Continuation gate (spending, not significance).** Further MoE compute only if a router metric
  reaches held-out AUROC ≥ 0.65 **and** beats the best comparator by ≥ 0.03 on **both** tasks.

## Handoff

Codex authors a **separate** extractor and scorer (frozen grid-A/B files untouched); the steward
executes, verifies and audits. Codex marks every execution step "not run by Codex".

## Corrections the audit made to the steward's draft

- "The instrument transfers mechanically" is conditional — the gate assumes a `v_proj` interface.
- "Router capture is cheap" omitted model residency, eager attention and expert-dispatch overhead.
- The task labels are dataset labels (answer supported / entailment), not the model's own
  hallucinations; "hallucination signal" is shorthand.
- "$0 since 2026-08-29" was not exact: the 2026-09-02 v-norm capture re-ran extraction on Modal.
