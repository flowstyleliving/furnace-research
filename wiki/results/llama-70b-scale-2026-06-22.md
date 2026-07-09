# Llama-3.3-70B Scale Cell — Family Dissociation + Orphan Resolution (2026-06-22)

**Status:** `[OPEN — exploratory]`. Backend = `modal-torch`, 4-bit (nf4), n=200. **NON-byte-comparable to the sealed MLX plane** — this is the torch cloud panel ([[../references/modal-cloud-extractor|modal-cloud-extractor]]), a standalone exploratory cell. **Does not alter the sealed 18/20.**

## Verdict

| Task | geom CI_lo | deployable | winner | locus |
|------|-----------|------------|--------|-------|
| anli_r1 | 0.703 | ✅ | `Readout neg_shadow_logvol_r1 @ step 0` | RPV / gen_step=1 |
| triviaqa_paired | 0.788 | ✅ | `Readout fisher_eff_rank @ step 0` | RPV / gen_step=1 |

n=200/200 both, 0 dropped, yes_no commit 0.95 / 0.995, controls pass, o_proj recon cos = 0.99999 (validation gate passed before extract). HF gating cleared (access approved 2026-06-22).

## Two findings

### 1. Family dissociation in signal *locus* 🧭
Every Qwen scale cell — 32B and 72B, both tasks — wins on **ACE attention morphology at t=0** (the prefix-last preparation state). **Both Llama-3.3-70B cells win on RPV readout-volume at gen_step=1** (the commit state) — `neg_shadow_logvol_r1` and `fisher_eff_rank`, never an attention cell. See [[../references/commit-locus|commit-locus]] for why these are genuinely different computational instants.

> **Precision de-confound (added 2026-06-23).** Llama-70B was run at **nf4**; the original Qwen-32B numbers turned out to be **bf16** (provenance bug, see [[precision-ladder-results-2026-06-22]]). That made the dissociation potentially a precision artifact. It is **not**: the [[precision-ladder-results-2026-06-22|precision ladder]] shows these signals are precision-invariant, and a **true-nf4 Qwen-32B** run wins **attention** on both tasks (anli 0.763, triviaqa 0.781). So at *matched* nf4 precision, Qwen=attention and Llama=readout — the dissociation is real.

So *which locus carries the diagnostic signal is model-family-dependent*:
- 🟦 **Qwen family → attention-morphology** (preparation: "how is attention routed before committing?")
- 🟥 **Llama family → readout-volume** (commitment: "how does the readout distribution spread at the commit token?")

This is the **first scale cell where ACE does not win**, and it is consistent across both tasks — a family property, not task noise. It is direct evidence for the **"universal *region* is too strong; universal *fitting procedure* is the honest claim"** reading: the panel's value is that it spans *both* loci, because different families land their signal in different ones. Reinforces the [[confluence-seal-2026-06-11|seal]]'s "no universal cell — 12 winners / 18 deployable."

### 2. Second sealed ANLI orphan resolves at scale 🔓
The sealed seal had two epistemic orphans on ANLI: `gemma-3-4b/anli` (predicted) and **`Llama-3.1-8B/anli`** (the no-prior-ACE-seal model). The gemma orphan already resolved as a small-model artifact (gen-3-12b/anli **0.709**, gen-4-12b **0.691**). Now **`Llama-3.3-70B/anli` = 0.703** closes the *second* orphan the same way — via an independent family. Both sealed ANLI orphans are confirmed **scale / small-model artifacts**, not properties of the method.

(Caveat on #2: the seal's Llama-3.1-8B is a *different model* than Llama-3.3-70B, and this is a torch/non-byte-comparable cell — so "resolves" means "the same family + task is deployable once you scale up," consistent with the gemma scale story, not a byte-exact reproduction.)

## Provenance
- Code: `/Users/msrk/Documents/furnace-guard/modal_app.py` (validate gate → extract → nested-OOB calibrate). Profiles: `profiles_ext/{anli_r1,triviaqa_paired}/Llama-3.3-70B-Instruct.profile.json` on the `model-cache` volume.
- Faithfulness: lm_head kept floating under 4-bit (Codex-reviewed; cos=0.99999). Pre-run Codex adversarial pass on the 4-bit path returned GREEN (one RMSNorm-eps flag resolved as numerically inert).
- These profiles predate the precision-switch patch, so their `comparability.precision` is absent (= the nf4 baseline). See [[precision-ladder-prereg-2026-06-22]] for the higher-bit follow-up.

See also: [[gemma-scale-extension-2026-06-18]] (the byte-comparable scale axis), [[summary]].
