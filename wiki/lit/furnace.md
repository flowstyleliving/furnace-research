# Furnace Papers

Own papers, drafts, and internal writeups. Stored in `raw/papers/furnace/`.

## Catalog
The internal paper filenames use `year-method-short-title.pdf`: lowercase, dash-separated, no `furnace-` prefix. This keeps the GitHub file list readable while preserving the method lineage.

### Historical SUP / PRI Lineage
The paper line splits SUP from PRI across three documents in chronological order:

| Order | Date | File | Era |
|------:|:-----|------|-----|
| 1 | earliest | `2026-detecting-confident-hallucinations-semantic-uncertainty-predictive-rupture.pdf` | **Pre-split** — SUP + PRI combined, SUP terminology in title |
| 2 | 2026-01-22 | `2026-predictive-rupture-hallucination-detection.pdf` | **Transitional** — compares PRI to ℏs (SUP baseline); SUP demoted to "underperforming baseline"; HaluEval benchmark |
| 3 | 2026-03-17 | `2026-hallucinations-rupture-at-commitment.pdf` | **Post-split** — ℏs unmentioned; synthetic 2×2 benchmark; commitment-localized framing |

### Later Method Papers

| Date | File | Topic |
|:-----|------|-------|
| 2026-04-09 | `2026-pri-v2-fisher-pullback-predictive-rupture.pdf` | PRI v2 Fisher-pullback magnitude detector |
| 2026-04-27 | `2026-pri-v3-architecture-dependent-fisher-pullback-geometry.pdf` | PRI v3 / null-ratio sealed Fisher-vs-raw geometry paper |
| 2026-05-30 | `2026-ace-attention-commitment-estimation.pdf` | ACE pre-generation attention commitment paper |
| 2026-06-07 | `2026-rpv-readout-pseudo-volume.pdf` | RPV readout pseudo-volume honest-negative paper |

## Archive Pointers
These pages are kept for provenance, but the canonical claim trail now lives in [claims](../claims.md) and [results/summary](../results/summary.md).

- [predictive-rupture-hallucination-detection](predictive-rupture-hallucination-detection.md) — archival summary of the transitional ℏs-vs-PRI paper; useful mainly for historical framing.
- Post-split commitment paper: summary page deleted 2026-07-09; the useful provenance is the step-0 bug audit in [claims](../claims.md).
- Pre-sup-split paper: not yet ingested (user deferred).
- `pri-v2` paper: not yet ingested.

## Filing convention
- Filename: `<year>-<method-or-topic>-<short-title>[-<qualifier>].pdf`, all lowercase, dashes.
- Do not prefix internal paper files with `furnace-`; the directory already supplies that provenance.
- On drop-in: say "ingest" — I read, write a summary page at `wiki/lit/<short-title>.md`, update `claims.md` and `overview.md` where relevant, append to `log.md`.
