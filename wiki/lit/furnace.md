# Furnace Papers

Own papers, drafts, and internal writeups. Stored in `raw/papers/furnace/`.

## Timeline (corrected 2026-04-14 after ingesting both papers)
The Furnace paper line splits SUP from PRI across three documents in chronological order:

| Order | Date | File | Era |
|------:|:-----|------|-----|
| 1 | earliest | `furnace-2026-detecting-confident-hallucinations-pre-sup-split.pdf` | **Pre-split** — SUP + PRI combined, SUP terminology in title |
| 2 | 2026-01-22 | `furnace-2026-predictive-rupture-hallucination-detection.pdf` | **Transitional** — compares PRI to ℏs (SUP baseline); SUP demoted to "underperforming baseline"; HaluEval benchmark |
| 3 | 2026-03-17 | `furnace-2026-prediction-rupture-at-commitment.pdf` | **Post-split** — ℏs unmentioned; synthetic 2×2 benchmark; commitment-localized framing |
| — | — | `furnace-2026-pri-v2.pdf` | PRI v2 technical writeup (date / placement TBD) |

## Ingested Summary Pages
- [prediction-rupture-at-commitment](prediction-rupture-at-commitment.md) — commitment-localization paper (March 2026), AUROC 0.998 / 0.994 / 0.980 headline — **note AUROC discrepancy with `summary.parquet`**.
- [predictive-rupture-hallucination-detection](predictive-rupture-hallucination-detection.md) — transitional ℏs-vs-PRI paper (January 2026), AUROC 0.60–0.67 on HaluEval.
- Pre-sup-split paper: not yet ingested (user deferred).
- `pri-v2` paper: not yet ingested.

## Filing convention
- Filename: `furnace-<year>-<short-title>[-<qualifier>].pdf`, all lowercase, dashes.
- Qualifiers: `-pre-sup-split`, `-draft-v2`, etc.
- On drop-in: say "ingest" — I read, write a summary page at `wiki/lit/<short-title>.md`, update `claims.md` and `overview.md` where relevant, append to `log.md`.
