# Llama 3.1 70B Instruct (nf4)

Modal / torch handle: `meta-llama/Llama-3.1-70B-Instruct` @ `1605565b47bb9346c5515c34102e054115b4f98b`

## Specs
- Size: 70B parameters, 80 decoder blocks, 64 heads / 8 KV
- Quantization: nf4 (bitsandbytes), torch lane
- First run: grid-B depth expansion, 2026-08-17

## Role in the research line
- The same-size **version comparison** against the banked Llama-3.3-70B (base-checkpoint identity NOT established — never phrased as isolating post-training).
- The model that showed the mid-stack band is lineage-stable.

## Main verdicts
- `depth-grid-2026-08-17` — registered grid-B cells: E5 dip PASSES both tasks (Δ_cf 0.141 anli / 0.201 halueval). **P8 HIT: the mid-stack attention band replicates** — 22–25 qualifying mid-blocks per fold on anli (16–20 halueval) vs the 3.3-70B context's 25–31 — the band the three-rung panel missed is a property of the Llama 70B lineage, not one checkpoint. Peak_cf 45/80 anli vs 38/80 halueval (wide bootstrap bands).

## Caveats and provenance
- Torch lane, NON-byte-comparable; numbers live in the results page.

## Canonical backlinks
- [results/depth-grid-2026-08-17](../results/depth-grid-2026-08-17.md)
