# Attention KV-tension pilot — `[PILOT RUN — NO-PROMOTE]`

**Lane:** ACE follow-up / `W_u`-free attention morphology
**Ran:** 2026-06-08 22:16–22:47 PDT (dated `2026-06-09` in its own output tree)
**Scored:** 2026-07-25 — six weeks late, during the t0 repo cleanup
**Artifacts:** `commit-confluence/exploratory/attention-kv-tension/` (relocated there 2026-07-25; previously uncommitted in `t0-morphology-furnace`)
**Pre-registration:** `exploratory/attention-kv-tension/PRE_REGISTRATION_DRAFT.md`, written 2026-06-09 *before* the pilot, left unamended

## The question

ACE already measures disagreement at both ends of grouped-query attention: `js` across all
query heads, and `js_kv_groups` after collapsing query heads that share a KV group. This
lane added the missing middle — tension **within** each shared KV group versus **between**
groups — via four opt-in cells: `js_within_kv_groups`, `js_within_kv_groups_no_bos`,
`js_kv_tension_gap`, `js_kv_tension_ratio`.

Stage 0 (audit of the 18 sealed ACE profiles) had found the handle *warm but scoped*: mean
`js_kv_groups − js` delta slightly **negative** (−0.013 over 54 layer cells), but 8/54 cells
above +0.05, with pockets up to +0.145 (TriviaQA / Llama-3.2-3B / mid). That is what
justified the decomposition as exploratory — never as a universality claim.

## The run

ANLI R1, n=200 (100/100), t=0 commit locus, `n_bootstrap=1000`, seed 20260512, sealed data
(`anli_R1_seed20260526_n200.jsonl`). Five models, completed clean.

## Verdict — does not clear its own promotion bar

AUROC in absolute orientation (`max(a, 1−a)`), matching the Stage-0 audit convention.
Reconstructed by this steward from the five `*.profile.json` candidate panels.

| Model | best KV cell | AUROC | vs best **routing** | vs best **any existing ACE** | OOB CI-lo | winner selected |
|---|---|---:|---:|---:|---:|---|
| Qwen3-8B | `js_within_kv_groups` | 0.8479 | +0.0075 | +0.0075 | 0.7382 | `final_js_within_kv_groups` |
| Mistral-7B | `js_kv_tension_ratio` | 0.8065 | +0.0195 | +0.0195 | 0.6931 | `last_minus_1_js_kv_tension_ratio` |
| Qwen2.5-7B | `js_kv_tension_ratio` | 0.7535 | **+0.0486** | **−0.0261** | 0.6474 | `final_bos_mass` |
| Phi-4-mini | `js_within_kv_groups` | 0.7374 | **+0.0614** | +0.0219 | 0.5806 | `final_js_within_kv_groups` |
| gemma-3-4b | `js_kv_tension_ratio` | 0.6379 | −0.0521 | −0.0521 | 0.4960 | `last_minus_1_js_kv_groups` |

`routing` = {`js`, `js_kv_groups`, `js_no_bos`}; `any existing ACE` additionally includes `bos_mass`.

The registered promotion bar had three limbs. **None is satisfied outright:**

1. **≥ +0.03 over the best existing ACE routing comparator on ≥ 2/5 models.** Against
   routing only: **2/5** (Phi-4-mini +0.0614, Qwen2.5-7B +0.0486) — met on the narrow
   reading the pre-reg's wording licenses. Against *any* existing ACE cell: **0/5**.
2. **OOB-clean, no severe coverage warning.** 4/5 clear `CI_lo > 0.50` (gemma-3-4b 0.4960
   does not). But **`winner_unstable` fires on 4/5** — Phi-4-mini 0.63, Mistral 0.60,
   Qwen3-8B 0.59, gemma 0.36 — *including both models carrying the numeric win*. At n=200
   the selected cell is explicitly noise-driven.
3. **Shuffled-label control flat.** **Never run.** No control appears in any pilot profile,
   so this limb is unverified and the bar cannot be met as written.

The pre-registered *falsification* clause — "all apparent wins collapse to BOS/sink
artifacts" — is **partially triggered**: on Qwen2.5-7B the selected winner is
`final_bos_mass`, a plain sink-mass cell beating the best KV-tension cell by 0.0261. The
lane's second-largest routing win sits on a model where sink mass simply wins.

**Call: `[NO-PROMOTE]`, not cleanly falsified.** The decomposition is warm on GQA models,
worthless on gemma-3-4b, and its two best models are the two whose winners are least stable.

## What this costs us to have learned late

Two process findings, both worth more than the result:

- **The comparator set decided the verdict, and the pre-registration never enumerated it.**
  "Best existing ACE routing comparator" reads one way if `bos_mass` is a routing cell and
  the opposite way if it isn't — 2/5 versus 0/5 on the same numbers. This is a
  researcher-degrees-of-freedom seam of exactly the kind pre-registration exists to close.
  **Future registrations must list the comparator cells by name.**
- **A completed 5-model pilot sat unscored and uncommitted for six weeks.** It was found
  only because the repo was being swept clean for an unrelated packaging task. This is the
  drift class the eleven-surface propagation checklist (rule 5b, 2026-07-25) was installed
  to prevent, and it predates that rule.

## If resumed

Needs a **fresh pre-registration**, not an amendment to the 2026-06-09 draft: enumerate the
comparator cells explicitly; make the shuffled-label control a launch blocker; raise n or
impose a stability floor given `winner_unstable` at 4/5; and state in advance whether
gemma-3-4b's negative is a scope boundary or a failure.

The implementation is **not currently runnable** — it exists only as an unapplied diff
against three sealed t0 modules, preserved at
`exploratory/attention-kv-tension/t0-patch/kv-tension-against-t0-7c2fcb7.patch`. Porting it
to an additive overlay over the read-only sealed calibrator (the pattern
`confluence_calibrator.py` already uses for `READOUT_PANEL`) is an open build task.

## Related

- Companion lane, same date: **v-norm-attention** `[RESOLVED — NO-PROMOTE]` — last-query
  V-norm cells add nothing over routing-only ACE across all 18 sealed profiles
  (mean delta −0.0436; 0/18 profiles at ≥ +0.02).
- [[results/v4-sealed-2026-05-26]] — the sealed ACE run this lane follows up.
