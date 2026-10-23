# Run log (chat-template check)

- 2026-10-22 ~18:24 PT: 5-row timing smoke, Phi-4 control: 132.5 s total, 26.5 s/row (`outputs/timing_n5.json`). The
  prior session was killed around 18:34 PT before the full runs began. A stale partial temp file from that session
  (`outputs/.rows-*.jsonl`, 5 rows, never read) was deleted.
- 2026-10-23: **Deviation from PLAN §2 (timing only).** The 5-row figure is dominated by fixed load cost, so a second
  timing point was taken: 15 rows, 175.7 s (`outputs/timing15/`). Marginal rate (175.7 − 132.5) / 10 = 4.3 s/row; fixed
  cost about 110 s. No feature or AUROC was read from either smoke.
- **Budget rule as applied.** Models run in PLAN order. Before each model starts, its two-condition time is projected
  from the last measured marginal rate, scaled by on-disk weight size. If the projected finish exceeds 14 h from the
  start of the first full run, that model and all later ones are not run.
