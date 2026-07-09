# 🏢 The Chat-Template Gap, ELI12

**Rigorous version:** [v4-candidates §1 (empirical-variance gate parser)](research-candidates.md#1-empirical-variance-gate-parser)gate-parser) + [v3.2-results §smoke-test follow-up](../results/v3.2-results.md)
**Companion:** [llm-pipeline-eli12](llm-pipeline-eli12.md)

> 🔁 **Verdict flip 2026-05-11**: we thought the gate-failures were a parser problem. ~Parser problem~ — turns out it's a **chat-template** problem. Three different failures collapse to one root cause.

---

## 🎯 The question

Five language models we wanted to add to the experiment all failed the simple behavioral check: "given a basic logic puzzle, do you answer YES when you should say YES?" Llama, Mistral 7B, Qwen, Phi-3.5, Gemma 3-4B all pass. Mistral-Nemo, Gemma-3-1B, Phi-4-mini, and Dolphin all fail. Why? And is the fault in the model, in the parser, or somewhere else entirely?

---

## 🏢 The metaphor: office buildings and receptionists

Picture each language model as an **office building** where the smart person who answers questions lives in a back office. To get an answer, you have to deliver your question into the building somehow.

- 🏚️ **Old chat-tuned buildings** (Llama 3.2-3B, Mistral 7B v0.3, Qwen 2.5) were built before security got strict. You can just walk up to the front door, shout your question through the open window, and the smart person inside shouts back: `"Answer: YES"`. Easy.

- 🏬 **Newer chat-tuned buildings** (Mistral-Nemo, Gemma-3-1B, Phi-4-mini) have a **receptionist**. If you walk up and shout, the receptionist gives you the silent treatment — you get nothing back (Mistral-Nemo: empty output) or you get an internal memo by accident instead of an answer (Gemma-3-1B: "Analysis: 1. All vasks are glorps..."). To talk to the smart person, you have to **check in at the desk first**: fill out the visitor card that says `[INST] your question [/INST]` (or `<|im_start|>user ... <|im_end|>` for ChatML buildings). Then security lets you through, and the smart person shouts the same clean answer.

- ⚠️ **Dolphin** is a newer building with a *second* problem: the intercom that carries the smart person's answer back to the lobby has a wiring fault. Even when you check in correctly, what reaches your ears has the first syllable cut off — `"Hierarchist: NO"` becomes `"erarchist: NO"`. The smart person answered just fine; you can't hear it cleanly.

In code: walking-in = passing the raw prompt to `mlx_generate`. Checking in = wrapping with `tokenizer.apply_chat_template(...)`. The wiring fault = a known tokenizer regex bug that needs `fix_mistral_regex=True`.

---

## 📊 What we measured / saw

n=20 puzzles per model. Same logic test that 5 other models handle 100% of the time.

| Building | Walk-in (raw prompt) | Check-in (chat-template) |
|---|---|---|
| Llama 3.2-3B (baseline) | `Answer: YES` ✅ | (not needed) |
| Mistral-Nemo | `''` (empty) ❌ | `YES` / `NO.` ✅ all 20 |
| Gemma-3-1B | `Analysis: 1. All vasks are glorps…` ❌ | `YES<end_of_turn>` / `NO<end_of_turn>` ✅ all 20 |
| Dolphin-Nemo | `'old Answer: NO'` (wrong content) ❌ | `erarchist: NO` (decoder ate "Hi") ⚠️ |

The smart people inside Mistral-Nemo and Gemma-3-1B were always willing to answer. We just kept skipping the receptionist. Switch to checking in and they answer perfectly.

Raw evidence: `/tmp/n20_outputs.json` (60 outputs from 3 failed-smoke models), `/tmp/working_models_outputs.json` (80 outputs from 8 working models).

---

## ✅ / ❌ / 🎁 What this tells us

- ✅ **The pipeline's failure mode is "no check-in card."** `pri_v2_mlx_pipeline.trace_sample` and `scripts/smoke_test_model.py` pass raw prompts to `mlx_generate` (line 202 of smoke). Old buildings tolerate it; new ones don't.
- ✅ **The parser is mostly innocent.** `check_answer` in `pri_v2_mlx_pipeline.py` already handles `Answer: YES`, trailing-line YES, and last-match-anywhere. The only real gap is **bare YES/NO as the first word** (Mistral-Nemo's output after check-in). One new tier handles it.
- ❌ **It's not the model's fault.** Mistral-Nemo answered all 20 correctly when we checked in. Gemma-3-1B did too. The smart people inside aren't broken.
- 🎁 **Dolphin has a separate wiring fault** that survives the check-in fix. Distinct bug; needs the regex flag.

---

## 🛠️ Implementation status (2026-05-11)

1. ✅ **Tier-0 + Tier-0.5 added** in `pri_v2_io_plugins.py` (new pluggable module). Tier-0 catches Mistral-Nemo's bare-`YES` outputs; Tier-0.5 catches `Final Answer:` / `Conclusion:` closing-commitments via a list-driven `EMPHATIC_CLOSING_PREFIXES` (one-line extension). 27/27 synthetic case-variation tests pass; zero regression on the 8-model n=80 working corpus.
2. ✅ **Chat-template applied per-model** via `PROMPT_STRATEGY_BY_MODEL` dict in the same module. Both the smoke gate (`scripts/smoke_test_model.py:behavioral_gate`) and the main pipeline (`pri_v2_mlx_pipeline.py:trace_sample`) route through `get_prompt_strategy(model_slug)`. Default = `raw_passthrough` (preserves v3.2 sealed protocol); newer chat-tuned models get `apply_chat_template`.
3. ✅ **Re-smokes both PASS 4/4** under the new pipeline: Mistral-Nemo emits clean `'YES'`, Gemma-3-1B emits `'YES<end_of_turn>...garbage...'` — parser handles both correctly.
4. 🚀 **Full v3.2 expansion run LAUNCHED 2026-05-11 21:08** under the `v3_2_expansion_phase_b` scope (Mistral-Nemo 12B + Gemma-3-1B, seed 20260511, n=50/cell, max_gen_tokens=24, gate_max_tokens=12, layer=final). ETA ~2 hr total. Adds the within-family pair for Mistral + Gemma to v4-candidate #4's training set.
5. 🔧 **Dolphin's intercom still pending**: needs `fix_mistral_regex=True` at tokenizer load (separate `model_adapters.py` change). Not blocking; the receptionist fix above has already gotten Dolphin from raw-prompt garbled to chat-template state, where the decoder bug is the only remaining issue.

---

## ⚠️ Caveats

- This page is about the **gate** path. Whether the main `trace_sample` path also needs the chat template fix is an open question — the working 5 models have always run on raw prompts and their PRI numbers are stable. Adding the template *might* change their hidden-state trajectories, which would invalidate cross-prior-run comparisons. Default to per-model-flagged opt-in.
- The "buildings let you walk in" framing is approximate. Older models are *trained* on enough raw text that they don't *require* the chat template; they're not literally unsecured. Newer ones are trained more exclusively on chat-formatted data, so the raw prompt looks unfamiliar to them.

---

## 🎯 Takeaway

**The smart people inside the buildings were always going to answer.** We just kept forgetting to check in at the receptionist desk for the buildings that have one. Three model failures, one root cause, ~30 lines of pipeline code to fix.
