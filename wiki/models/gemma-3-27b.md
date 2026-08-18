# Gemma 3 27B IT (nf4)

Modal / torch handle: `google/gemma-3-27b-it` @ `005ad3404e59d6023443cb575daa05336842228a`

## Specs
- Size: 27B dense, 62 decoder blocks, 32 heads / 16 KV
- Quantization: nf4 (decoder), torch lane

## Role in the research line
- The model that exposed the **instrument-domain boundary** of the sealed `js_no_bos` metric.

## Main verdicts
- `depth-grid-2026-08-17` — **both registered cells ABORTED at row 0, block 3: the SEALED kernel returns `None` for `final_js_no_bos`** — extreme BOS-sink attention leaves no distribution once the sink column is stripped. Grid A's four models never entered this regime; gemma-27b exits the metric's domain by its third block. Counted as registered confirmatory failures under the frozen zero-drop rule; also a standing caveat for every js_no_bos use. Smoke gates themselves passed (cos 1.0, YES/NO commits) — the failure is metric-domain, not behavioral.

## Caveats and provenance
- Torch lane, NON-byte-comparable. Sibling contrast: gemma-3-12b sails through both cells — the sink regime is not family-wide.

## Canonical backlinks
- [results/depth-grid-2026-08-17](../results/depth-grid-2026-08-17.md)
