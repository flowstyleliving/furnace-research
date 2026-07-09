# Orbital Prompt ("Answer Anchor") — 2026-06-23

**Status:** `[RESULTS — technique + taxonomy]` — prompt-engineering method for collapsing first-token output into YES/NO space across model families. Codex-designed. Discriminator taxonomy with three leak categories.

## 1. Motivation

Cross-family first-token analysis hit a format-compliance wall: some models produce preamble tokens (`To`, `Step`) before answering, contaminating YES/NO commit analysis. The orbital prompt appends `\n\nAnswer:` to the raw prompt before chat template application — the colon acts as a grammatical attractor that pulls the first token into answer space.

## 2. Method

Implemented as `--answer-anchor` flag on `/Users/msrk/Documents/furnace-guard/_commit_dump.py`:

```bash
modal run /Users/msrk/Documents/furnace-guard/_commit_dump.py --model-id <hf_id> --task anli_r1 --precision nf4 --answer-anchor
```

The suffix is appended to the raw prompt string before model-specific chat template wrapping. No other changes to the extraction pipeline.

## 3. Results

| Model | Original YES/NO | With Anchor | Δ | Leak type |
|---|---|---|---|---|
| Qwen2.5-7B | 97.0% | **99.5%** | +2.5 ✅ | `To` preamble — mostly killed (6→1) |
| Yi-1.5-34B | 72.0% | **88.0%** | +16 ✅ | `Step` COT — fully killed (28%→0%) |
| Llama-3.3-70B | 95.0% | 95.0% | 0 | `To` preamble — immune at scale |
| Mistral-Large-2411 | 57.0% | 58.0% | 0 | `Y` tokenizer subword — immune |

**Key findings:**

- **Yi-34B (+16pp):** Complete annihilation of chain-of-thought drift. `Step` went from 28% of commits to 0%. But `To` preamble rose from 0% to 11.5% — the model shifted from CoT to "To answer..." reflex. Anchor swaps one leak for another at this scale.
- **Qwen-7B (+2.5pp):** Near-total elimination of `To` preamble (6→1). Anchor works cleanly at 7B.
- **Llama-70B (flat):** `To` preamble is IMMUNE at scale. Same 10 `To` leaks pre and post anchor. At 70B, `To` is structural — baked into the first-token probability landscape, not lazy formatting.
- **Mistral-Large (flat):** Tokenizer subword artifact (`Y` vs `YES`) is immune to any prompt engineering. BPE merge table unchanged by suffix.

## 4. Discriminator Taxonomy

Three leak categories, distinguished by anchor response:

| Category | Token | Anchor response | Root cause |
|----------|-------|-----------------|------------|
| **COT leakage** | `Step` | Fully killed | Format compliance — model wanders into chain-of-thought before answering |
| **Preamble leakage** | `To` | Scale-dependent | Structural at 70B, fixable at 7B |
| **Tokenizer leakage** | `Y` | Immune | Vocabulary artifact — `Y` is a subword of `YES` for Mistral's BPE tokenizer |

## 5. Normalization Rules

For cross-model agreement matrices:
- Map `Y` → YES (Mistral subword)
- Map `N` → NO (rare, not observed in practice)
- Exclude all other non-YES/NO tokens (`Step`, `To`, `\n`, etc.) from normalized analysis
- Report both raw and normalized rates; raw as finding, normalized for comparison

## 6. Implications

- **For commit-confluence:** Format compliance is an alignment artifact, not a scale property. Yi-34B (72%) and Qwen-32B (100%) are same parameter tier, opposite extremes.
- **For methodology:** The orbital prompt is a formatting crutch, not a contribution. Useful for cross-family comparison but doesn't belong in the core paper's claims.
- **For scale axis:** `To` at 70B is structural — the anchor can't touch it. This is evidence that large models develop first-token commitments that are resistant to surface-level prompt changes.

## 7. Artifacts

- Implementation: `/Users/msrk/Documents/furnace-guard/_commit_dump.py` (`--answer-anchor` flag)
- All commit dumps with anchor: `commit_dump/` on Modal volume `model-cache`
- Pre-anchor baselines: same volume, standard filenames
- Codex adversarial review: GREEN (6 checks passed, 2026-06-23)
