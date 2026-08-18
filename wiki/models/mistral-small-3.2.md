# Mistral Small 3.2 24B Instruct (nf4)

Modal / torch handle: `mistralai/Mistral-Small-3.2-24B-Instruct-2506` @ `95a6d26c4bfb886c58daf9d3f7332c857cb27b43`

## Specs
- Size: 24B dense, 40 decoder blocks, 32 heads / 8 KV; multimodal wrapper (`Mistral3ForConditionalGeneration`), vision tower unquantized
- Quantization: nf4 (decoder), torch lane

## Role in the research line
- Third-family entrant in the grid-B depth expansion; the grid's most instructive failure pair.

## Main verdicts
- `depth-grid-2026-08-17` — registered grid-B cells: **anli FAILED the behavioral gate** (row-1 commit `'To'` — the chain-of-thought opener, same signature as Qwen2.5-7B's `' To'` in BENCH; registered gate class, no rescue); **halueval extracted clean but is the grid's one TRUE on-data miss** — Δ_cf 0.0045, the terminal dip essentially absent. mistral-common vs AutoTokenizer cross-check: 0/400 mismatches.

## Caveats and provenance
- Torch lane, NON-byte-comparable. The gate failure and the true miss are different findings — do not merge them.

## Canonical backlinks
- [results/depth-grid-2026-08-17](../results/depth-grid-2026-08-17.md)
