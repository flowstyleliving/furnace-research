# References: Code Repositories

All repos are external to this vault. `raw/` holds no code — only pointers here.

## Current repo map (2026-06-07)
The work runs in **two live repos** plus one retired one. Per the Vault-canon rule, the source of truth for which repo a given line lives in is the `wiki/log.md` tail.
- **`PRI_at_commitment`** — PRI-detection working trunk. v1/v2/v3 pipeline + figures, the production library (`pri_calibrator.py` + `pri_detector.py`), IO plugins, and the exploratory **v5–v8** branches (residual-friction / projection-veto / attention-route / ACE-route-override, all NO-PROMOTE, tagged to preserve the falsification trail). `main` carries the ACE/T0 bridge after the 2026-06-06 merge (`57c9108`).
- **`t0-morphology-furnace`** — the morphology line (split out 2026-06-06; **living lab** since 2026-06-07). Sealed ACE/T0 core (repo-root modules, `tests/`, `experiments/t0-sealed/`, `paper/`; sealed tag `t0-ace-sealed-2026-05-26`) **stays frozen**; new unsealed morphology candidates incubate in a top-level `exploratory/` area (out of the sealed `tests/` suite). Path `/Users/msrk/Documents/t0-morphology-furnace/`; GitHub `flowstyleliving/t0-morphology-furnace`. First inhabitant: `exploratory/shadow-ambiguity/` (candidate #10).
- **`PRI_at_commitment_autoresearch`** — RETIRED 2026-04-14 (see bottom of this page).

## PRI_at_commitment (main pipeline)
- Path: `/Users/msrk/Documents/PRI_at_commitment/`
- Entrypoint: `pri_v2_mlx_pipeline.py` — runs the full PRI v2 experiment across the active model suite, checkpoints per model, resumes incomplete runs, emits combined analysis tables + figures.
- Key modules:
  - `pri_metrics.py` — PRI v1 cosine, FIM variants, Hedges g, surprise.
  - `synthetic_logic_loader.py` — 2×2 factorial contradiction puzzle generator.
  - `synthetic_trace.py` — prefix + generation hidden-state / probability trace collection.
  - `hidden_state_collector.py`, `attention_contribution.py`, `model_adapters.py` — MLX instrumentation stack.
  - `config.py` — model registry + numeric constants.
- Output dir: `./pri_v2_results/` (parquet files + figs).
- Pre-run audit document: `PRI_V2_PRE_RUN_AUDIT_CHECKLIST.md` — 11-section correctness audit (token/hidden alignment, forward pass, unembedding, PRI formulas, data generation, gates, loop, stats, figures, numerical stability, reproducibility).

## PRI_at_commitment_autoresearch (RETIRED 2026-04-14)
- Path: `/Users/msrk/Documents/PRI_at_commitment_autoresearch/` (repo still exists on disk; not being used)
- The autonomous daily loop was retired per user decision on 2026-04-14 after 4 consecutive days of gate failures (`AUROC=nan, gate=0/0` from 2026-04-09 through 2026-04-12).
- **Do not diagnose, restart, or reference the autoresearch loop as an active track.** Tier-1/2/3/4/5 experiments from its `PLAN.md` are still useful as an experiment queue — they can be run manually via the main `pri_v2_mlx_pipeline.py`.
- The experiment queue (Tiers 1–5) and research standards (pre-registration, exploratory n=4 → confirmatory n=20, Bonferroni, cross-model gate) are useful conventions even outside the autoresearch framing. Preserve them as aspirational protocol, not infrastructure.
