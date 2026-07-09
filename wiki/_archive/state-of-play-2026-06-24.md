# Commit-Confluence: State of Play (2026-06-24)

*Technical orientation document for conversational AI context. Drop this into any session to orient it on the project's architecture, completed work, current needs, and what NOT to pursue.*

---

## 1. What This Project Is

**Commit-confluence** is a pre-registered integration study that unifies four families of commit-moment hallucination detectors into a single 29-signal panel, then lets an honest, selection-bias-corrected nested-OOB bootstrap selector pick the best signal per (model, task) deployment.

**Core finding:** There is no universal champion — 12 distinct signals win across 18 deployable deployments. But there IS a universal above-chance floor — one fixed cross-locus fusion aggregate beats chance on 9/10 and 10/10 held-out models. Confidence (the model's own output probability) is NOT the backstop — the same two orphan deployments fail with or without it.

**Paper title:** "Decoder LLM Hallucination: No Universal Detector, but a Universal Floor." Single author: Michael S.R. Kitti. Target venue: TMLR (open review, values pre-registration + reproducibility).

---

## 2. The Four Signal Families

| Family | Mechanism | What it reads | Commit locus |
|--------|-----------|---------------|--------------|
| **ACE** (Attention-Commitment Estimator) | Attention weights only — BOS mass, inter-head JS disagreement, V-norm | How attention routes at the commit instant | `t=0` (prefix-last attention) |
| **PRI** (Predictive Rupture Index) | Fisher SVD pullback — projects Δh onto `√p·W_u` basis | Fraction of hidden-state motion lying OFF the top readout direction | `gen_step=1` (first generated token) |
| **RPV** (Readout Pseudo-Volume) | Readout distribution geometry — effective rank, spectral entropy, rank-1 pseudo-volume | Spread/concentration of the output distribution | `gen_step=1` |
| **Confidence** | Token surprise, max-probability | Model's own output confidence | `gen_step=1` |

**Critical:** ACE and PRI/RPV read at DIFFERENT commit instants. ACE = prefix-last attention (t=0), PRI/RPV = first generated token (gen_step=1). Do not conflate.

Two pre-registered cross-locus **fusion** signals (rank-means across families) round out the 29-signal panel.

---

## 3. The Honest Selector

Per-deployment nested OOB bootstrap: for each (model, task) pair, the selector picks the single best signal and its discriminative sign *inside* each resample and evaluates it on the held-out fraction. The reported AUROC CI lower bound is corrected for selection bias. The selector never sees the labels it's scored on. A deployment is **deployable** if the OOB AUROC 95% CI lower bound > 0.50.

This is the key methodological innovation — fitting 29 signals without p-hacking because the selection is bootstrapped inside-out.

---

## 4. Completed Work

### 4.1 Sealed Core (irreversible run, 2026-06-11)

- **10 models × 2 benchmarks** (ANLI R1, TriviaQA paired), n=200 each
- Models: Llama 3.1-8B, Llama 3.2-3B, Mistral-7B-v0.3, Mistral-Nemo-12B, Phi-3.5-mini, Phi-4-mini, Qwen2.5-7B, Qwen3-8B, Qwen3-1.7B, Gemma-3-4B
- **Geometric-only (ACE+PRI+RPV): PASS 18/20** (bar ≥17/20)
- **Full panel (+confidence+fusion): FAIL 18/20** (bar ≥19/20) — honestly falsified
- Both endpoints fail the SAME two ANLI orphans: `gemma-3-4b/anli` and `Llama-3.1-8B/anli`
- Confidence rescues nothing — coverage identical with or without it
- 12 distinct winners across 18 deployable deployments
- Tag: `prereg-seal-20260612`, repo: `github.com/flowstyleliving/commit-confluence`
- All per-deployment score matrices published

### 4.2 Post-Seal Extensions

**Scale axis (2026-06-18, byte-comparable):**
- `gemma-3-12b/anli`: CI-lo 0.709 → PASS (orphan RECOVERED by scale)
- `Qwen2.5-14B/anli`: CI-lo 0.766 → PASS (rules out generic "12-14B needed" effect)
- 4/4 new cells deployable, all ACE attention winners
- **CRAB-LOCK (2026-06-20):** head-count resolution hypothesis REFUTED. Starving gemma-3-12b to 4B head budget keeps it deployable (0.71→0.67). The orphan is per-head representation QUALITY, not head count.

**Generation axis (2026-06-21, NON-byte-comparable — mlx-vlm reimplementation):**
- `gemma-4-12b/anli`: CI-lo 0.691 → PASS
- `gemma-4-12b/triviaqa`: CI-lo 0.751 → PASS
- Orphan does NOT return at gen-4 — confirmed scale/small-model artifact, not lineage property
- Both winners = Fusion (not ACE-solo) — likely reimplementation drift, don't over-read

**Torch cloud panel (2026-06-22, NON-byte-comparable — Modal + bitsandbytes):**
- `Qwen2.5-32B`: 2/2 deployable, ACE attention winner (true-nf4 after bf16 provenance bug caught and fixed)
- `Qwen2.5-72B`: 2/2 deployable, ACE attention winner (inferred nf4, OOM guard blocks bf16)
- `Llama-3.3-70B`: 2/2 deployable, **RPV readout-volume winner** — first scale cell where ACE does NOT win
- **Family dissociation:** Qwen → attention-morphology (t=0), Llama → readout-volume (gen_step=1)
- Second sealed ANLI orphan resolved: `Llama-3.3-70B/anli` CI-lo 0.70 (cf. `Llama-3.1-8B/anli` FAIL). Both sealed ANLI orphans now confirmed as scale/small-model artifacts across two independent families.

**Precision ladder (2026-06-22/23):**
- Qwen2.5-7B × {nf4, int8, bf16, fp32} + Qwen2.5-32B × {nf4, int8, bf16}
- H3 falsifier: "≥0.10 CI_lo drop nf4→bf16 on a deployable cell" → **FALSIFIED.** Signals are precision-invariant.
- Key methodological finding: cross-precision comparisons must use FIXED CELLS, not argmax winner (selection noise).
- Selection instability and int8 degradation are small-model artifacts that wash out by 32B.
- Also caught: 32B bf16 provenance bug (run unstamped before bug caught 2026-06-23).

---

## 5. The Tangent — What We Went Into (Commit-Equivalence Orbit)

Starting ~2026-06-23, we pursued a **second-order question**: "Is the first-token commitment locus stable across precision rungs, model families, and prompt formats?"

This produced:

### 5.1 Format compliance taxonomy
- Qwen-7B ANLI: 97% YES/NO (nf4) → 93.5% (bf16). Leakage = `To` preamble.
- Qwen-32B ANLI: 100% YES/NO. Scale eliminates format leakage.
- Yi-1.5-34B ANLI: 72% YES/NO, 28% `Step` chain-of-thought drift.
- Mistral-Large ANLI: 57% YES/NO, 78 tokens = `Y` (tokenizer subword artifact).
- Llama-70B ANLI: 95% YES/NO, 10 `To` leaks at nf4.

### 5.2 Orbital prompt ("Answer Anchor")
- Append `\n\nAnswer:` to raw prompt before chat template. Codex-designed technique.
- Yi-34B: 72% → 88% (+16pp). COT leakage (`Step`) fully killed. Does NOT fix `To` preamble.
- Qwen-7B: 97% → 99.5%. `To` preamble mostly killed at 7B.
- Llama-70B: 95% → 95%. `To` is IMMUNE at scale — structural, not lazy formatting.
- Mistral-Large: 57% → 58%. Tokenizer artifact immune to prompt engineering.

### 5.3 Three leak categories
1. **COT leakage (`Step`):** Format compliance problem. Killed by anchor. (Yi-34B)
2. **Preamble leakage (`To`):** Scale-dependent. Anchor works at 7B, fails at 70B. (Llama, Qwen)
3. **Tokenizer leakage (`Y`):** Vocabulary artifact. Nothing touches it. (Mistral-Large)

### 5.4 Cross-model agreement
- Within-family cross-scale (Qwen 7B vs 32B): 82% agreement
- Cross-family (Llama-70B vs Qwen-32B): 81% agreement
- Cross-family cross-scale (Llama-70B vs Qwen-7B): 76% agreement
- **Finding:** behavioral disagreement ceiling ~18.5%. Cross-family divergence ≈ within-family cross-scale divergence. The family dissociation in signal LOCUS is genuine — not just answer-disagreement in disguise.

### 5.5 Within-model precision agreement
- Qwen-7B ANLI (4 rungs): 80% same-token
- Qwen-32B ANLI (3 rungs): 95.5% same-token
- Scale reduces within-model contamination by ~4×.

### 5.6 Correctness vs consensus (TriviaQA paired)
- 5-model accuracy: Qwen-7B 75%, Qwen-32B 82%, Mistral-Large 90.5%, Yi-34B 93.3%, Llama-70B 96.5%
- Consensus lift: +0.002. Null. Llama-70B dominates → no headroom.
- **Rule:** need benchmark where all models score 50-75% with different error patterns. Not ANLI, not TriviaQA. Custom design required.

### 5.7 Dead ends
- **Falcon-180B:** OOM on 2×A100 even with CPU offloading. Two attempts, both failed. Declared dead.
- **Command A (111B):** 0% YES/NO. Template incompatibility — outputs `\n`. Not worth fixing.

---

## 6. Paper Status (`cc-draft.tex`)

### What's written
- Title, author, abstract ✅
- Introduction (Section 1) ✅ — motivation, gap, contribution
- Method (Section 2) ✅ — panel description, honest selector, rigor, cohort
- Results (Section 3) ✅ — coverage, no universal champion, universal floor, task transfer, label efficiency
- Post-seal extension (Section 4) ✅ — scale axis, generation axis (gemma-4), torch cloud panel (Llama-70B family dissociation)
- Discussion (Section 5) ✅ — floor vs champion, limits, reproducibility
- References ✅

### What's missing / needs attention
- **Figures:** `fig1_coverage.pdf`, `fig2_winmap.pdf`, `fig3_label_efficiency.pdf`, `fig4_universality_floor.pdf`, `fig5_scale_extension.pdf` — need to verify all exist in `cc-figures/` and compile
- **Companion reports:** PRI, ACE, RPV drafts exist (`pri-draft.tex`, `ace-draft.tex`, `rpv-draft.tex`) but are marked "in preparation"
- **Overleaf compile:** No local LaTeX toolchain. Need to verify it compiles clean.
- **Gemma-4 figure update:** `fig5_scale_extension.pdf` may need regeneration to include gen-4 data point
- **The commitment-convergence section:** The first-token format-compliance results (Section 5 above) are NOT yet folded into the paper. They could be a behavioral-triangulation paragraph in Discussion — but they're supplementary, not core.

### What should NOT go in the paper
- The full precision ladder results (nf4/int8/bf16/fp32) are a methodological control, not a finding
- The orbital prompt technique is a formatting crutch, not a contribution
- Falcon-180B and Command A dead ends are negative results with no signal
- TriviaQA correctness analysis is null (no consensus lift)
- The 4-rung intersection set analysis is interesting but belongs in a methods appendix at most

---

## 7. What's Actually Needed Now

### Priority 1: Paper completion
1. Verify all 5 figures exist and compile
2. Compile `cc-draft.tex` on Overleaf
3. Add the Llama-70B family dissociation paragraph (already written, needs figure reference)
4. Finalize companion report drafts (PRI, ACE, RPV)
5. Proofread cross-references, figure labels, consistency

### Priority 2: Dashboard (Lovable, 400+ credits)
- Phase 1: synesthetic visualization of the 29-signal panel
  - Per-deployment cards with CI-lo, winner signal, family
  - Universality floor scatter plot (leave-one-model-out)
  - Honest orphan display — the two failures, with scale-resolution annotations
  - Process timeline (pre-registration → adversarial review → sealed run → extensions)
- Published score matrices (already on GitHub) feed the viz directly

### Priority 3: Venue preparation
- **TMLR** is the right first target: open review, values pre-registration + reproducibility
- Needs: clean compile, all figures, companion reports linked, repo tagged
- NeurIPS/ICML stretch: needs 5+ benchmarks, not 2

### Priority 4 (defer): Benchmark expansion
- The benchmark expansion proposal exists (v2, post-Codex fixes)
- But 2 benchmarks is sufficient for TMLR submission
- Additional benchmarks: better as a revision/update, not a blocker for initial submission

---

## 8. What NOT to Spend Time On

- **More precision rungs.** The 4-rung ladder on Qwen-7B already falsified H3. More models at fp32 add nothing.
- **More cross-family agreement matrices.** The 18.5% ceiling is established. More model pairs won't change it.
- **Falcon-180B / Command A.** Dead ends. The paper doesn't need them.
- **More orbital prompt experiments.** The three leak categories are mapped. The anchor is a technique, not a finding.
- **TriviaQA correctness analysis.** Consensus lift is null because Llama-70B dominates. The benchmark is wrong for the question.
- **Custom benchmark design** (for consensus-vs-correctness). This is a *different paper* — not the commit-confluence integration study.
- **More scale cells on torch.** Llama-70B confirmed both orphans are scale artifacts. 70B is sufficient. 405B would be cool but doesn't change the claim.

---

## 9. Architecture Map (for navigating the repos)

```
~/Documents/
├── t0-morphology-furnace/          ← SEALED CORE. No edits without explicit instruction.
│   ├── pri_runtime.py              ← Production detector library
│   ├── pri_calibrator.py           ← Per-model calibration profiles
│   ├── model_adapters.py           ← MLX model wrappers (attention capture, hidden states)
│   ├── experiments/t0-sealed/      ← Irreversible sealed runs
│   └── exploratory/                ← RPV, residual-friction, KV-tension (all closed/negative)
│
├── commit-confluence/              ← Extension dispatcher + paper repo
│   ├── confluence_calibrator.py    ← The 29-signal nested-OOB selector
│   ├── stage_b/                    ← Per-model extraction + extension cells
│   │   ├── profiles_ext/           ← Byte-comparable extension matrices
│   │   └── gemma4_full_extract.py  ← Gemma-4 mlx-vlm extractor (non-byte-comparable)
│   └── tag: prereg-seal-20260612   ← Public sealed tag
│
├── the_GOAT/                       ← Research vault (Obsidian)
│   ├── wiki/
│   │   ├── paper/                  ← cc-draft.tex, ace-draft.tex, pri-draft.tex, rpv-draft.tex
│   │   ├── results/                ← 33 result pages (sealed, extensions, precision ladder, etc.)
│   │   └── references/             ← commit-locus.md, cloud-gpu-setup.md, commit-equivalence.md
│   └── AGENTS.md                   ← Codex/Claude orientation (this file's sibling)
│
├── furnace-guard/                  ← Local Mac mini M4 Furnace guard repo (de-clouded 2026-06-26)
│   ├── furnace                     ← CLI/TUI wrapper
│   ├── furnace_cli.py              ← Local guard-command wrapper
│   └── seal/                       ← Vendored sealed scoring/calibration kernels
│
└── PRI_at_commitment/              ← Legacy v1/v2 repo. Superseded by t0-morphology-furnace.
```

---

## 10. Key Methodological Commitments

1. **No edits to sealed t0 core.** The `t0-morphology-furnace` is frozen. Extension cells live in `commit-confluence/stage_b/`.
2. **Byte-comparable vs non-byte-comparable.** Extension cells using the same inference stack and module hashes are byte-comparable and can be pooled with sealed cells. Anything reimplemented (torch, mlx-vlm) is daggered and never pooled.
3. **Pre-registration before data.** All extension cells are pre-registered with frozen predictions before the data is drawn.
4. **Adversarial review before irreversible run.** Every extension build gets a Codex or Claude adversarial review pass.
5. **Published score matrices.** Every analysis is reproducible from the repository alone — no models, no private dependencies.
6. **Honest negatives.** Failed hypotheses (RPV redundant with v3 null_ratio, residual-friction no-promote, head-count refuted, precision-ladder H3 falsified) are documented and published alongside positives.

---

## 11. Current Blockers

None that are technical. The blockers are writerly:
- MK is bedridden (pelvic floor recovery), grinding Mercor for break-even money
- Paper needs focused writing time, not more experiments
- Dashboard needs a design session — Lovable credits are ready

The research is done. The findings are clear. The story needs telling.
