# Work order — Temperature-robustness study of the commit-step detector (design draft)

**Date:** 2026-08-26
**Status (updated 2026-08-27):** PRE-REG DRAFTED, **RUN DEFERRED — FUNDING GATE (MK, 2026-08-27: "let's do this run once we get funding").**
`commit-confluence/stage_b/PRE_REGISTRATION_TEMP.md` exists at **v1.3 draft** (585 lines, NOT frozen, unsigned),
produced 2026-08-26 by a Codex-authors / Fable-5-audits / Codex-fixes loop: round 1 scored 3/10 (two fatal
defects: the commit-identity gate compared model answers to ground-truth labels — 120/120 guaranteed FAILED;
readout locus misplaced at the prefix when five readout cells live at the post-commit forward), round 2 scored
4/10 (two new fatal-class: the three RPV cells are late-window **aggregates** over 1+ceil(B/4) logit-lens
sources, not readout-only — the doc's own T=1 parity gate would have zeroed every cell; and an all-or-nothing
verdict rule unreachable given BENCH's recorded non-canonical commit rates on Qwen2.5-7B/Phi-3.5), round 3
scored **7/10, zero fatal** — remaining M1–M7 minors + one typo applied in v1.3 and delta-verified by the
steward (incl. independent recomputation of the 24,000 / 86,400 forward-pass counts). Every cited hash
(15 source files + 20 matrices + 2 BENCH provenance JSONs) independently re-verified across the rounds.
**Next actions when funding lands:** (1) MK sign-off on v1.3 → freeze revision; (2) Codex builds the
extractor/scorer/sampler/decidedness/equivalence artifacts (§3.7 TBD-at-freeze manifest); (3) steward executes
per the binding §5.6 phase order (parity sentinel → smokes → one extraction sweep → single-look scoring →
pilot); (4) Opus-5 high-effort writes results into the vault. Disclosed compute: ~3–6 days parallel on the
named M4 host, or hours with an equivalence-certified vectorized selector.
⚠️ The pre-reg file is currently **untracked** in `commit-confluence` — commit it (MK or on request) so the
draft can't silently drift.

Original design spec below (2026-08-26, superseded in detail by the pre-reg wherever they differ — the
pre-reg is the executable document):
**Prior status:** DRAFT — DESIGN ONLY. **Not frozen, not registered, no runs authorized.** MK sign-off and a
Codex adversarial pass are both prerequisites to any freeze, per the BENCH discipline
([[paper/cc-bench-prereg-review]] lineage). This page is the durable spec a future
`PRE_REGISTRATION_TEMP.md` would be cut from — it is not itself a pre-registration.
**Candidate:** #14 in [[research-candidates]].
**Related but deliberately separate:** the poisoned-context probe (candidate #15) — see §7 for why it is
its own thread and not an axis of this study.

---

## 1. Goal

One line: establish whether the commit-step signal (ACE attention panel + PRI surprise/rupture +
readout cells) is a property of the model's internal geometry or an artifact of measuring at the
greedy (T=0) operating point — the only regime any sealed or BENCH result has ever described, and a
regime nobody deploys in.

## 2. The load-bearing decomposition (argmax is T-invariant)

Softmax temperature divides logits by `T`; this is monotone, so **the argmax token is identical for
every `T > 0`**. Temperature therefore changes two things that are *separable in our harness*:

- **(A) Reshape-only** — the distribution `p_t` the metrics are computed from gets smoothed, while the
  committed token (and hence every hallucination label) stays byte-identical to the sealed T=0 run.
- **(B) Real sampling** — the commit token is drawn from `p_t^(T)`, so genuinely different
  hallucinations occur and correctness becomes a per-draw random variable.

These are different claims and must be registered as **two named endpoints**:
(A) tests whether the geometric story is measurement-regime-dependent;
(B) tests whether the detector survives an actually-deployed sampling regime.
A result in one must never be reported as answering the other.

**Why (A) is a strong control and not filler:** entropy/confidence-style detectors *mechanically*
degrade under (A) — smoothing is exactly what they measure. If the ACE/PRI cells survive (A) while
confidence cells degrade, that is direct evidence the signal is not confidence in a trenchcoat
(the standing concern from the RPV arc, candidate #10). If ACE/PRI degrade in lockstep with
confidence, the "geometry, not confidence" framing takes real damage. Both outcomes are informative.

## 3. Verified cost fact (checked 2026-08-26, this session)

The persisted BENCH/seal matrices (`stage_b/profiles*/**/*.matrix.npz`) hold **scored panel cells
only** (`score_matrix (n, 27)`, labels, sample_idx, panel/meta strings) — **no logit vectors, no
hidden states**. So experiment (A) is *not* a free re-analysis of existing artifacts.

However: (A) needs exactly **one forward pass per sample** (same `max_new_tokens=1` extraction), and
all temperature grid points are pure post-hoc functions of that one logit/state capture. The
extraction must emit the whole T-grid per pass — cost of (A) = one re-extraction sweep, **not**
|T-grid| sweeps. This is the single most important engineering pin for the builder.

## 4. Design

### Phase 1 — (A) reshape-only, full cohort

- **Decoding:** greedy throughout (argmax; commit tokens and labels identical to T=0 by construction —
  assert this per-row against the sealed commitments as a validity gate, not assume it).
- **T-grid:** `{0.5, 0.7, 1.0, 1.5, 2.0}` + the T=0-limit reference (frozen at pre-reg; no additions
  because an intermediate point "looked interesting").
- **Cohort:** the sealed 10-model MLX cohort verbatim — Phase 1 is cheap enough that shrinking it
  buys nothing and costs comparability.
- **Tasks:** `anli_r1` + `halueval_qa` only. TriviaQA-paired is excluded (B1 gate-cascade entanglement
  and the paired-row bootstrap issue); no pooling across the excluded tasks.
- **Cells:** the sealed 29-cell panel, unchanged, recomputed at each T from the same capture; plus the
  plain-confidence comparator cells, **named in the pre-reg** (the KV-tension lesson: the comparator
  set must be enumerated before the run, because a verdict can flip on what counts as a comparator).
- **Primary readout per (model, task, T):** deployability AUROC under the sealed in-bag/OOB selector,
  and — mandatory, not optional — the **coverage decomposition**: eligible/decidedness coverage at
  each T alongside the AUROC conditional on staying decided. A bare AUROC-vs-T curve is ambiguous
  between "temperature manufactures low-decidedness" (a known failure class — Phi-3.5,
  [[results/step0-belief-readout-2026-05-17]]) and "the geometry itself needs sharpness" (new finding).

### Phase 2 — (B) sampling pilot, small cohort — gatekept behind Phase 1 scoring

- **Label:** PILOT. No cohort-wide promotion language regardless of outcome (the KV-tension /
  v-norm register).
- **T-anchors:** `{0.7, 1.0, 1.5}` — 0.7 = common deployment default; 1.0 = unadjusted softmax;
  1.5 = inside the code-gen literature's non-monotonic zone, included solely to test the §5
  directional prediction.
- **Draws:** `K = 5` per prompt per T, fresh registered seed; per-draw commit re-labeled (the
  behavioral answer can change across draws — correctness is per-draw, and the labeling rule must be
  frozen, including the disposition of draws that commit a non-canonical token).
- **Cohort (3–4 models), chosen to span the known structure:** one Qwen (attention-morphology
  winner), one Llama (readout-locus winner), **Phi-3.5-mini deliberately** (the known
  low-decidedness model — most likely to expose a coverage-driven story), optionally Mistral-7B
  (crisp small-model depth structure). Exact set frozen at pre-reg.
- **Tasks:** same two as Phase 1. **Data:** reuse the sealed/BENCH prompt draws — comparability to
  the T=0 reference outranks data freshness here; state this trade explicitly in the pre-reg so it
  cannot read as an oversight.
- **Unit of inference:** the prompt (stems where applicable), never the draw — K draws per prompt are
  dependent; bootstrap resamples prompts/stems, all their draws entering together (the §7.4 cluster
  lesson from the BENCH review, applied prospectively this time).

### Held fixed throughout both phases

Extraction machinery (`max_new_tokens=1`, sealed loci: ACE at t=0/prefix-last, PRI/RPV/confidence at
gen_step=1), the sealed selector (`nboot=2000`), module hashes recorded, sealed files untouched, new
artifacts in a fresh `profiles_temp/` tree — never pooled with sealed, EXT, BENCH, or torch cells.

## 5. Registered directional prediction (non-monotonicity)

The code-generation U-shape (hallucination rate falling from T=0 to ~1.5, then rising) is a
**multi-token free-generation artifact** — greedy degeneracy/repetition loops suppressed by moderate
T. A repetition loop is structurally impossible in a 1-token forced-choice commit. **Prediction, to
be frozen as falsifiable:** hallucination rate and detector AUROC in (B) are flat-or-monotone in T;
no U-shape. If non-monotonicity appears anyway, it is a *new* phenomenon requiring its own
explanation — it must not be narrated as replicating the code-gen curve, whose mechanism does not
transfer.

## 6. Pre-registration commitments to lock before any run

1. (A) and (B) registered as two named endpoints; primary designated (proposal: (A) primary,
   (B) pilot/descriptive).
2. Comparator cells enumerated by name, including all plain-confidence cells.
3. Coverage/decidedness gate definition frozen **before** any degradation result is seen.
4. T-grids, K, cohort, tasks, seed frozen; no grid expansion post-hoc.
5. Denominator policy: every (model, task, T) cell in the frozen denominator; smoke/gate failures
   reported as failed cells inside it, never dropped (the A2 "8/10 silently becomes 8/9" escape
   hatch, closed in advance).
6. Per-draw labeling rule for (B) frozen, including non-canonical commits.
7. §5 directional prediction stated as falsifiable.
8. Amendment rule: implementation-only corrections require a filed amendment before regeneration;
   any change to grids, cohort, labels, bars, or endpoint logic voids the phase (BENCH v1.2/v1.3
   language, inherited verbatim).
9. PILOT labeling for (B); promotion path runs through a fresh registered confirmation, not this
   document.

## 7. Explicitly out of scope: the poisoned-context probe (→ candidate #15)

The Mount Sinai adversarial-hallucination class (fabricated detail planted in the prompt; the model
elaborates) is a **different mechanistic question** — grounding-fidelity failure, not
parametric-commitment failure. Prediction to be tested there, not assumed: the surprise/rupture
channel goes largely silent (elaborating on an in-context fabrication is low-rupture, mechanistically
"correct" grounding), while the attention-morphology channel *may* still discriminate contaminated
from clean grounding (concentration on a short implanted span vs. diffuse grounding in distributed
evidence). It needs its own matched-control design (fabricated vs. *true* implanted detail, matched
for elaboration length/style) and its own comparator enumeration. Folding it into this study would
blur two failure modes under one bar. Parked as candidate #15; no work authorized.

## 8. Acceptance

- Frozen `PRE_REGISTRATION_TEMP.md` in the repo, Codex-audited (targeted GREEN), MK-signed, **before**
  any strict cell runs.
- Phase-1 validity gate: per-row commit identity with the sealed T=0 commitments (exact token-id
  match); any mismatch is a stop-and-file-amendment event, not a footnote.
- Scorer runs once per phase; misses reported as written.
- Results land in `wiki/results/temp-sweep-<date>.md` + full 11-surface propagation.

## 9. Handoff

- **Design/spec:** this page (Claude, steward).
- **Pre-reg author + adversarial audit:** Codex (write/audit-only; verification "not run by Codex").
- **Executor:** Claude Code or MK-launched runtime; artifacts to `commit-confluence` under a fresh
  profile tree.
- **Open MK decisions:** sign-off on the two-endpoint framing; Phase-2 cohort final pick; whether
  (A) full-cohort or (A) also shrinks if extraction cost surprises upward.
