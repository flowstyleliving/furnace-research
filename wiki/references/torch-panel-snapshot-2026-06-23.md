# Torch Cloud Panel — State Snapshot (2026-06-23)

**Purpose:** single-page context-reset doc. Read this first to resume the Modal/torch cloud extraction work. Everything here is the **exploratory torch panel** — `backend="modal-torch"`, **NON-byte-comparable to the sealed MLX plane**, **never pooled with the sealed 18/20**. Deep pages linked inline.

---

## 1. What this is

A GPU/torch reimplementation of the commitment-diagnostic extractor, run on **Modal**, to reach models the MLX seal can't (large scale, generation axis). Faithfulness is held by two runtime gates, checked per (model, precision) before any extract:
- 🛡️ **o_proj reconstruction cos ≥ 0.999** — the captured attention output is rebuilt from `Σ w·v` and compared to the model's own `self_attn` output. Guards the capture.
- 🛡️ **YES/NO commit** — the model must actually attempt the task (not continue the prompt).

Code: `/Users/msrk/Documents/furnace-guard/modal_app.py` (the live extractor; the `commit-confluence/modal/` copy is a stale stub). Reference: [[modal-cloud-extractor]]. Calibrator = the sealed nested-OOB selector, run unmodified under the venv.

W_u (`lm_head`) is kept **floating at every precision** (`llm_int8_skip_modules=["lm_head","embed_tokens"]`) so the geometry kernels see a real float tensor — verified by Codex adversarial review (GREEN; one RMSNorm-eps flag resolved numerically inert).

## 2. Infrastructure / how to run

- `modal` CLI: `/Users/msrk/Library/Python/3.9/bin/modal` (v1.2.6; in `~/.zshrc` PATH, but this session's non-interactive shell needs the full path).
- Volume `model-cache` holds models + all artifacts:
  - profiles: `profiles_ext/<task>/<slug>[__<precision>].profile.json` (+ `.matrix.npz`)
  - validate: `validate/<slug>[__<precision>]_<task>.json`
  - **nf4 keeps the legacy bare `<slug>` name; int8/bf16/fp32 get a `__<precision>` suffix.**
- Run: `modal run /Users/msrk/Documents/furnace-guard/modal_app.py --model-id <hf> --task <anli_r1|triviaqa_paired> --mode <validate|extract> --precision <nf4|int8|bf16|fp32>`. Stagger launches **2 at a time** (Modal rate-limits ~3+ rapid app creations).
- ⚠️ **Always pass `--precision` on new runs.** Pre-patch runs were unstamped → see the provenance bug in §4. `nf4` reproduces the historical 4-bit config byte-for-byte.

## 3. Current results (all torch panel, non-byte-comparable)

| Model | Task | precision | geom CI_lo | deployable | winner | locus |
|-------|------|-----------|-----------|------------|--------|-------|
| Qwen2.5-32B | anli | bf16 | 0.790 | ✅ | `att last_minus_1_bos_mass` | attention |
| Qwen2.5-32B | anli | nf4 (true) | 0.763 | ✅ | `att last_minus_1_js` | attention |
| Qwen2.5-32B | anli | int8 | 0.784 | ✅ | `att bos_mass` | attention |
| Qwen2.5-32B | triviaqa | bf16 | 0.822 | ✅ | `att last_minus_1_v_norm` | attention |
| Qwen2.5-32B | triviaqa | nf4 (true) | 0.781 | ✅ | `att final_bos_mass` | attention |
| Qwen2.5-32B | triviaqa | int8 | 0.822 | ✅ | `att v_norm` | attention |
| Qwen2.5-72B | anli | nf4 *(inferred)* | 0.639 | ✅ | `att last_minus_1_js_no_bos` | attention |
| Qwen2.5-72B | triviaqa | nf4 *(inferred)* | 0.918 | ✅ | `att last_minus_1_js` | attention |
| Llama-3.3-70B | anli | nf4 | 0.703 | ✅ | `rd neg_shadow_logvol_r1` | **readout** |
| Llama-3.3-70B | triviaqa | nf4 | 0.788 | ✅ | `rd fisher_eff_rank` | **readout** |

**Qwen2.5-7B precision ladder** (winner / CI_lo per rung):

| task | nf4 | int8 | bf16 | fp32 |
|------|-----|------|------|------|
| anli | 0.498 ❌ | 0.498 ❌ | 0.589 ✅ | 0.551 ✅ |
| triviaqa | 0.810 ✅ | 0.535 ✅ | 0.670 ✅ | 0.657 ✅ |

(7B winners are selection-unstable — see §5; the *fixed-cell* grid is the truthful view, in [[../results/precision-ladder-results-2026-06-22]].)

## 4. Precision provenance (the bug, caught 2026-06-23)

Pre-patch runs were **not precision-stamped**. A byte-identity check (`nf4 score-matrix == bf16 score-matrix`, maxdiff 0.0) revealed the original **32B baseline was bf16, not nf4** (no `--load-in-4bit`; 32B-bf16 fits one 80GB). A **true-nf4 32B** run was then done (stamped, distinct). Net:
- 7B ladder = stamped (correct). 32B = **bf16 + true-nf4 both run**. 72B = **inferred nf4** (the OOM guard blocks 72B-bf16 on 1 GPU) but **NOT byte-verified**. Llama-70B = stamped nf4.
- Scale tier is **mixed precision**, not "all nf4." All mislabeled docs corrected 2026-06-23.

## 5. Key findings

1. 🧭 **Family dissociation in signal LOCUS** (de-confounded). Qwen family → **attention-morphology** (t=0 preparation); Llama family → **readout-volume** (gen_step=1 commit). Verified at **matched nf4** precision (true-nf4 32B wins attention; Llama-nf4 wins readout) → real, not a bf16-vs-4bit artifact. [[../results/llama-70b-scale-2026-06-22]].
2. 🔓 **Both sealed ANLI orphans resolve at scale.** `gemma-3-4b/anli` (→ gen-3-12b 0.709 / gen-4 0.691) and `Llama-3.1-8B/anli` (→ Llama-3.3-70B 0.703). Both confirmed small-model artifacts, via two families.
3. 🧱 **Precision ladder verdict** ([[../results/precision-ladder-results-2026-06-22]], pre-reg [[../results/precision-ladder-prereg-2026-06-22]]):
   - **H3 falsified at the fixed-cell level** — robust signals are precision-invariant at 7B AND 32B (real computation, not quantization noise).
   - **Cross-precision must be judged on FIXED CELLS, not the argmax winner** — the argmax + its OOB CI_lo are selection-noisy. (My live turn-by-turn reads chasing the winner were wrong; the fixed-cell grid is the truth.)
   - **Selection-instability + int8/LLM.int8 degradation are SMALL-MODEL artifacts** — present at 7B, gone at 32B (32B winner stable, int8≈bf16). int8 ≠ "between 4 and 16 bit" — it's a different quantization family (outlier-decomposition).
   - One readout cell (`fisher_eff_rank`) carries mild nf4-correlated structure; not load-bearing.

## 6. Open threads
- 🔍 ~~**72B byte-verify**~~ — **CLOSED 2026-06-23.** OOM guard confirmed: `modal run --precision bf16` on Qwen2.5-72B-Instruct immediately raises `ValueError: will OOM on A100-80GB`. The guard is real → existing 0.639/0.918 runs are confirmed nf4. Validation artifact also recovered from volume (`validate/Qwen2.5-72B-Instruct_anli_r1.json`): GATE_PASS, o_proj cos=1.0, YES/NO solid.
- 📐 ~~**Commit-equivalence intersection set**~~ — **CLOSED 2026-06-23.** Full analysis at [[../results/commit-equivalence-2026-06-23]]. 80% 4-rung intersection, 15% nf4↔bf16 answer-flip rate, ~0.02–0.03 AUROC drag from contamination. Supporting finding — does not alter precision-ladder verdicts.
- 📊 Optional: fold the locus-dissociation + precision-robustness into the paper beyond the current `cc-draft.tex` §"scale and generation close the orphan" paragraph.

## 7. Map of the detailed pages
- [[modal-cloud-extractor]] — the extractor reference (code map, gotchas, full results table, precision-switch usage).
- [[../results/llama-70b-scale-2026-06-22]] — family dissociation + orphan resolution.
- [[../results/precision-ladder-prereg-2026-06-22]] — pre-registration (frozen hypotheses).
- [[../results/precision-ladder-results-2026-06-22]] — both ladder waves, fixed-cell grids, method-correction.
- [[commit-locus]] — which signal reads at which computational instant.
- `wiki/log.md` tail (2026-06-22 / 2026-06-23) — append-only narrative.
- Root `CLAUDE.md` / `AGENTS.md` — top hot-update blocks (2026-06-22, corrected 2026-06-23).
