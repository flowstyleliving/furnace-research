# Mistral Medium 3.5 128B (FP8-origin, dequant-BF16)

Modal / torch handle: `mistralai/Mistral-Medium-3.5-128B` @ `22b2b868a15677cfa6061277ed2f653d1349a9ab`

## Specs
- Size: 128B dense, 88 decoder blocks, 96 heads / 8 KV; multimodal wrapper, vision tower excluded
- Precision: **FP8-origin weights, deterministically dequantized; BF16 compute** on 4×A100-80 (`from_pretrained(bf16)` auto-dequant, frozen from smoke; 1233/1233 bf16 params verified) — NOT a BF16 reference checkpoint; the Qwen nf4↔bf16 invariance does not cover it
- Largest model in the registered grid (405B remains unrun)

## Main verdicts
- `depth-grid-2026-08-17` — registered grid-B cells: E5 dip PASSES both tasks (Δ_cf **0.293** anli — the grid's largest — / 0.151 halueval); its halueval cell is 1 of only 2 grid-B cells satisfying the cross-fitted cliff rule. Peaks sit very late and tight: 83/88 anli vs 85/88 halueval — Qwen-like late-peak family signature (mistral family cluster 0.88 ± 0.13 peak fraction).

## Caveats and provenance
- Both cells carry the FP8-origin flag; the registered leave-Medium-out sensitivity (6/10) travels with any grid-level claim.

## Canonical backlinks
- [results/depth-grid-2026-08-17](../results/depth-grid-2026-08-17.md)
