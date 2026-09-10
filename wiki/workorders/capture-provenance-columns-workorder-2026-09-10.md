# Work order — three provenance columns for the capture pipeline (2026-09-10)

_Status: **OPEN**, authored 2026-09-10. Additive capture change; touches no sealed file and moves no verdict._

## Goal

Add three columns to the per-row capture so that any future run is (a) **joinable across runs** by a content-bearing key and (b) **re-analyzable in either normalization space** without re-running the model.

```
rms_h_prev      float64   rms(h_prev) at the captured layer, pre-norm
rms_h_t         float64   rms(h_t)     at the captured layer, pre-norm
prompt_sha256   str       sha256 of the exact prompt string fed to the model
```

Roughly 40 bytes per row.

## Why — two failures, both this session, both the same class

Neither is hypothetical; both were hit on 2026-09-09/10 and both are logged.

- 🔑 **No content-bearing row key.** `sample_id` is `arange(N)` in every run. A naive join between `run-02` (n=200) and `run-09` (n=600) reports a "200/200 overlap" that is **pure indexing artifact** — at the same index the two runs agree on the contradiction label only 75% of the time and on chain length 50%. The only content evidence banked is the 10 traced prompts per run (0 shared). So **whether the powered run replicates or extends the preliminary run cannot be settled from the artifacts**, and `pri-draft.tex` §3.2 now has to say so in print. ⚠️ The DC lane hit the identical gap (`sample_idx` = `arange(200)` in all 17 files). Two lanes, same cause.
- 📐 **No way back between normalization spaces.** The `J_n` bug was a pre-norm `Δh` projected onto a post-norm basis. It was fixed correctly by capturing post-norm directly — but the banked parquets contain **no norm or scale column** (74 columns; only `delta_h_cosine` and `delta_h_l2`, both derived). So a pre-norm view of existing data is unobtainable without re-generating, which for a sealed single-look gate is exactly the path we refuse to take.

## The math that makes this cheap

RMSNorm is `y = γ ⊙ h / r`, with `r = sqrt(h·h/d + ε)`.

As a map it is **many-to-one** — every positive multiple of `h` lands on the same `y`, so the radial direction is destroyed. But **the only thing destroyed is the scale, and the scale is one number.** Keep `r` and the map is exactly invertible:

```
forward:   y = γ ⊙ h / r
backward:  h = r · (y ⊘ γ)
```

`γ` needs no banking — it is in the model weights and is already extracted per model at runtime. So **one float per captured hidden state restores full round-tripping**, and with it the ability to compute the Fisher pullback in either space after the fact:

```
G_post = Wᵤᵀ diag(p) Wᵤ
G_pre  = Jᵀ G_post J,     J = diag(γ)·(1/r)·(I − h hᵀ/(d r²))
```

Note `J h ≈ 0`: the Jacobian annihilates the radial direction, so `G_pre` is singular with null direction `h`. That degeneracy is **correct** — motion along the current hidden state is invisible to the output — and it is a free diagnostic: any metric that assigns weight to radial motion is measuring something the model cannot see. (`Jᵀ G_post J` is a first-order correspondence; direct post-norm capture stays the exact route and is not being replaced.)

## Guardrails

- ➕ **Purely additive.** Do not modify, rename, reorder or drop any existing column. Downstream readers must be unaffected.
- 🔒 **No sealed file is touched** and no banked verdict is re-derived. This changes future capture only.
- 🧊 **No re-run of any sealed gate.** This work order does not authorize regenerating `v3-main-run` data.
- 🧮 `rms_h_prev` / `rms_h_t` are the **pre-norm** RMS at the same layer the hidden states are captured from, computed with the same `ε` the model's own RMSNorm uses. If `ε` is not recoverable from config, bank it too rather than guessing.
- 🔤 `prompt_sha256` hashes the **exact string fed to the model** — post chat-template, pre-tokenization — so it is stable across tokenizer changes and comparable across runs of the same prompt.
- 🚫 Do not backfill. Existing parquets stay as they are; a synthesized key would be worse than an absent one.

## Acceptance

1. A fresh smoke run emits all three columns, non-null on every row.
2. Round-trip check on ≥100 rows: reconstruct `h` from banked `y`, `γ`, `r` and confirm agreement with the captured pre-norm state to float tolerance (~1e-6 relative).
3. Two runs of the same scope and seed produce **identical** `prompt_sha256` sets; two runs of different scopes produce sets whose intersection is computable and reported.
4. Every pre-existing column is byte-identical to a pre-change run on the same seed and scope.
5. ⚠️ Verification requires execution and is therefore **not run by Codex** — Codex authors the patch and states the commands; a runtime executor supplies artifacts.

## Handoff

**Codex authors** the patch (write/audit-only per HARD RULES). Capture site is in `PRI_at_commitment/pri_runtime.py` — the generation loop around `h_prev_causal = act[0, -2]` and the row-emit path that builds the results frame. **Claude Code or MK executes** the smoke and supplies the acceptance artifacts.

## Related

[[log]] 2026-09-10 eighth and ninth entries · [[results/pri-v3-repro-2026-09-09]] · `pri-draft.tex` §3.2 (states the independence question is unsettled and why) · the DC lane's identical `sample_idx` gap, recorded in root `CLAUDE.md`.
