# Candidate #10 — Readout Pseudo-Volume (RPV) / Shadow-Ambiguity: Mathematical Deconstruction

**Name (paper-facing):** **Readout Pseudo-Volume (RPV)** — locked 2026-06-07. *Shadow-ambiguity* / *#10* stay the internal exploratory slug (repo dir, contract test, harness). Mirrors the ACE↔v4 naming convention.
**Status:** TESTED 2026-06-07 — **H1 NO-GO**: beats plain confidence (base-A meta +0.102 [+0.065,+0.140], p≈5e-8; 3 families; brittleness-clean) but **redundant with v3** (base-B meta +0.011, below the +0.02 bar); complements v3 only in its collapse regime. *(§7–§8 below were written pre-verdict; final numbers in [[wiki/claims]] §2.)*
**Rigorous home:** [[wiki/research-candidates#10-shadow-ambiguity--fisher-pseudo-volume-of-the-readout]] · pre-reg v2 in repo: `t0-morphology-furnace/exploratory/shadow-ambiguity/PRE_REGISTRATION_DRAFT.md`
**Intuition companion:** [[wiki/learn/260607-not-fooling-ourselves-eli12]] (methodology) · [[wiki/learn/260531-ace-vs-pri-v3-eli12]] (ACE vs v3)
**Reference code:** `exploratory/shadow-ambiguity/test_shadow_ambiguity.py` (contract), `comprehensive_run.py` (harness).

---

## 0. One-paragraph thesis

At the commitment instant the model's hidden state $h$ is read out through the unembedding $W_u$ into a token distribution $p=\mathrm{softmax}(W_u h)$. Because $W_u$ is injective (vocab $V \gg d$, full column rank), **no information is lost at the linear step** — all collapse from the high-dimensional $h$ to the one-token "shadow" happens in **softmax + argmax**. The local geometry of that collapse is the **centered softmax-Fisher** $F_c = W_u^\top(\mathrm{diag}(p)-pp^\top)W_u$. Candidate #10 reads the **spectrum** of $F_c$: how many directions the readout resolves (**effective rank**) and how large the "invisible" pre-image cell is (**pseudo-volume**). v3's sealed `null_ratio` measures the *motion* of a particular $\Delta h$; #10 measures a *property of the metric itself*, independent of $\Delta h$.

---

## 1. The readout object

At gen-step 1 (the sealed v3/calibrator commit plane):

- $h \in \mathbb{R}^d$ — post-final-RMSNorm hidden state ($d=d_\text{model}$).
- $W_u \in \mathbb{R}^{V\times d}$ — unembedding (lm_head or tied embedding), $V$ = vocab.
- logits $z = W_u h \in \mathbb{R}^V$; $p=\mathrm{softmax}(z)\in\Delta^{V-1}$; committed token $=\arg\max p$.

**Injectivity fact.** With $V\gg d$ and generic $W_u$, the map $h\mapsto z$ has full column rank $d$ → it is injective. $(W_u)^+ z = h$ exactly. Therefore the lossy, shadow-casting steps are softmax (gauge quotient $z\sim z+c\mathbf 1$, plus saturation) and argmax (tessellation of $h$-space into vocab-many cells). $W_u$ is the *lamp angle*, not the shadow-caster.

---

## 2. Derivation of the Fisher metric

**Softmax Fisher w.r.t. logits.** With $p_i = e^{z_i}/\sum_k e^{z_k}$, $\;\partial_{z_j}\log p_i = \delta_{ij}-p_j$. The Fisher information of the categorical in logit coordinates:

$$
F_z = \mathbb{E}_p\!\big[(\partial_z\log p)(\partial_z\log p)^\top\big],\qquad
(F_z)_{jk}=\sum_i p_i(\delta_{ij}-p_j)(\delta_{ik}-p_k)=p_j\delta_{jk}-p_jp_k.
$$

$$
\boxed{\,F_z=\mathrm{diag}(p)-pp^\top\,}
$$

Equivalently $F_z$ is the Hessian of $\mathrm{KL}(p_z\,\|\,p_{z+\delta})$ in $\delta$ at $\delta=0$.

**Pullback to $h$.** Since $z=W_u h$, $\partial z/\partial h = W_u$, so the Fisher pulled back to hidden space is

$$
\boxed{\,F_c \equiv I(h)=W_u^\top\big(\mathrm{diag}(p)-pp^\top\big)W_u\,}\quad(d\times d,\ \text{PSD}).
$$

**KL = variance of the logit-shift.** For a hidden perturbation $\delta h$, write $\zeta = W_u\,\delta h$. Then

$$
\mathrm{KL}\big(p_h\,\|\,p_{h+\delta h}\big)\approx \tfrac12\,\delta h^\top F_c\,\delta h
=\tfrac12\big(\zeta^\top(\mathrm{diag}(p)-pp^\top)\zeta\big)
=\tfrac12\,\mathrm{Var}_p(\zeta).
$$

So $F_c$ literally measures *how loudly each direction of hidden-motion shows up in the output distribution*. (This $\tfrac12\,\mathrm{Var}_p$ closed form is the `kl_discharged` cross-check in the contract suite.)

**Relation to sealed v3.** v3's `null_ratio_post_rank{r}` uses the **un**centered surrogate $A=\sqrt{\mathrm{diag}(p)}\,W_u$ (so $A^\top A = W_u^\top\mathrm{diag}(p)W_u$, dropping the $-pp^\top$) and reports the Euclidean fraction of a *specific* $\Delta h$ lying outside the top-$r$ right-singular directions of $A$. Candidate #10 uses the **proper centered** $F_c$ and reads its **eigenvalue spectrum** — a $\Delta h$-independent property of the metric, not a projection of one motion vector.

---

## 3. The statistics (functions of the spectrum)

Eigendecompose $F_c=\sum_i \lambda_i v_iv_i^\top$, $\lambda_1\ge\lambda_2\ge\cdots\ge 0$. Define the active set $\{\lambda_i>\texttt{rel\_tol}\cdot\lambda_{\max}\}$ (numerical-rank floor, `rel_tol`$=10^{-12}$) and the normalized spectrum $\tilde\lambda_i=\lambda_i/\sum_j\lambda_j$, $H=-\sum \tilde\lambda_i\log\tilde\lambda_i$.

1. **`fisher_eff_rank`** (Roy–Vetterli effective rank):
$$\mathrm{effrank}=\exp(H).$$
"How many directions the readout resolves": $\to 1$ when one $\lambda$ dominates, $=k$ for $k$ equal eigenvalues. **Scale-invariant** ($\mathrm{effrank}(c\lambda)=\mathrm{effrank}(\lambda)$) — pure *shape*.

2. **`spectral_entropy`** $= H/\log(\text{rank}_\text{eff})\in[0,1]$. Monotone-equivalent to eff_rank → identical AUROC.

3. **`shadow_logvol_post_rank{r}`** — the **Fisher pseudo-volume**. The set of hidden states producing the same commitment within a KL-ball, $\{\delta h:\tfrac12\delta h^\top F_c\,\delta h\le\varepsilon\}$, is an ellipsoid with semi-axes $\propto\lambda_i^{-1/2}$, hence (log-)volume $\propto -\tfrac12\sum_i\log\lambda_i = -\tfrac12\log\det F_c$. Excluding the top-$r$ *decision* directions and averaging per off-top direction:
$$
\mathrm{shadow\_logvol}_r=-\frac{1}{2(d-r)}\sum_{i>r}\log(\lambda_i+\varepsilon).
$$
"How large is the **invisible cell** — how far can $h$ move in non-decision directions without changing the shadow." Pinned at $r=1$ (top-1 = the commit axis). **Not** scale-invariant: $-\tfrac12\sum\log(c\lambda)=-\tfrac12\sum\log\lambda-\tfrac{d-r}{2}\log c$ — it carries the overall Fisher *scale* (i.e. confidence), which is exactly why it is the most confidence-coupled of the three (see §6).

4. **`participation_ratio`** $=(\sum\lambda)^2/\sum\lambda^2$ — sibling effective-dimension; left un-thresholded (roundoff-robust); secondary only.

Sign orientation (locked from train folds / pre-registration): `fisher_eff_rank` higher → contradiction; the volume statistic enters as `neg_shadow_logvol_r1` $=-\mathrm{shadow\_logvol}_1$ (lower raw volume predicted contradiction in the pilot).

---

## 4. The shadow framing (why these are the right objects)

- The token is the **shadow** of the high-dimensional $h$.
- $W_u$ (injective) = the **lamp angle**: it rotates/aims, it doesn't lose dimension.
- **softmax + argmax** = the shadow-caster (gauge quotient + saturation + tessellation).
- $F_c$ = the **differential** of the shadow map at the commit.
- `effrank(F_c)` = how many dimensions the shadow *resolves*; `shadow_logvol(F_c)` = the *volume the object can move through without moving the shadow* — the geometric meaning of an *ambiguous* commitment.

---

## 5. The dual computation (tractable spectrum)

$F_c$ is $d\times d$ and naively needs all $V$ rows of $W_u$. The harness:

1. Truncates to the **top-$K$ probability support** ($K=512$): $W_s$ ($K\times d$), $p_s$ (off-support mass is $\approx 0$, contributes negligibly).
2. Forms $B=\mathrm{diag}(p_s)-p_sp_s^\top$ ($K\times K$, PSD), $R=B^{1/2}$, $\mathrm{Gram}=W_sW_s^\top$ ($K\times K$).
3. Nonzero $\mathrm{eig}(F_c)=\mathrm{eig}(R\,\mathrm{Gram}\,R)$ — a $K\times K$ eigenproblem. Pad with $d-K$ structural zeros to recover the full $d$-spectrum (needed only for `shadow_logvol`; eff_rank/entropy use the active nonzero set, so the dual is exact for them).
4. All products via `np.einsum` (the macOS Accelerate BLAS emits spurious `matmul` overflow/invalid warnings on finite inputs; einsum avoids them — verified the values were never corrupted).

Dequantized $W_s$ rows come from the inherited centered-Fisher core's `OutputProjection.get_rows` (handles 4-bit `mx.dequantize`). Contract suite (`test_shadow_ambiguity.py`, 7/7) verifies: the temperature identity $F_z[\mathrm{softmax}(z/T)]=\tfrac1{T^2}(\mathrm{diag}(p_T)-p_Tp_T^\top)$; the degeneracy limit ($\lambda_{\max}\to0$, $-\tfrac12\log\det\to+\infty$ as $p\to$ one-hot, ε-guarded finite); the h-space-vs-vocab distinction; and agreement of the reference spectrum with the production centered eigendecomposition.

---

## 6. Layer windows

The statistics can be read at the **readout** (final layer, true $p$) or at any block $\ell$ via the **logit lens**: $p_\ell=\mathrm{softmax}\!\big(W_u\cdot\mathrm{norm}(h_\ell)\big)$, $F_c(p_\ell)$. (Note: the layer-wise statistics are $p_\ell$-only; no per-layer $\Delta h$ is used — so they are invariant to the attention-vs-MLP "same-sum-different-fight" decomposition, just like v3.)

**Depth-audit finding (Qwen3-8B, 36 blocks, logit lens, n=200).** There is **no single crossover**. Logit-lens `null_ratio` is volatile across depth (≈chance at blocks 2,3,5,22,28,33; strong elsewhere). The shadow stats are more consistently elevated **but** confidence-coupled at early/mid depth: $\mathrm{pearson}(p_{\max},\,\mathrm{shadow\_logvol})\approx 0.97\text{–}0.99$ at blocks 0–14, **decoupling only late** ($\gtrsim$ block 22 → $0.1\text{–}0.5$; readout $0.14$). The genuine beyond-confidence structure is a **late-layer** phenomenon (\~blocks 24–28 on Qwen3-8B).

**Pinned window (pre-reg v2, no post-hoc layer selection).** For $B$ blocks, late count $=\lceil B/4\rceil$, start $=B-\lceil B/4\rceil$, blocks $[\text{start},\dots,B-1]$ **plus the readout**. The aggregate statistic is the arithmetic mean over those blocks' logit-lens values and the readout value.

- $B=36$: $\lceil 36/4\rceil=9$ → blocks **27–35** + readout.
- $B=28$: $\lceil 28/4\rceil=7$ → blocks **21–27** + readout.

Rationale: early/mid layers are confidence-in-disguise (high brittleness); only the late window carries the candidate signal, and the fixed rule blocks "best-layer" cherry-picking.

---

## 7. Confidence vs. commitment — the core separation

**Confidence** is a scalar: $\mathrm{surprise}=-\log p_{\max}$ (peakedness of $p$). Geometrically it is the **scale** of $F_c$ — as $p\to$ one-hot, $\mathrm{diag}(p)-pp^\top\to 0$, so the whole spectrum shrinks (the falsified centered-Fisher amendment's "$10^4\times$ smaller top eigenvalue" regime, the same regime where v3 dies on Qwen3-8B).

**Commitment quality** is the **shape** of the spectrum: how many directions resolve (`effrank`) and how big the invisible cell is (`shadow_logvol`). Two commits with identical $p_{\max}$ can have different spectral shapes → in principle independent of confidence.

**The entanglement.** Peaking $p$ changes both scale *and* shape, so shape and confidence are correlated, not orthogonal. Hence shadow-ambiguity needs four explicit separators, in increasing strength:

1. **Scale-invariant statistics.** `effrank`/`entropy` use the *normalized* spectrum → invariant to the Fisher scale (the $1/T^2$ confidence prefactor) → respond only to spectral *shape*. (`shadow_logvol` is *not* scale-invariant — it inherits confidence scale, which is why it is the most confidence-coupled; cf. §3.)
2. **Temperature pre-check (label-free).** Sweep $T$: because $F_z[\mathrm{softmax}(z/T)]=\tfrac1{T^2}(\cdots)$, `effrank` moves *only* through the distribution flattening, never the prefactor. If `effrank`$(T)$ collapses onto $\mathrm{surprise}(T)$ (Spearman $|\rho|>0.9$), it is confidence in disguise. (Panel result: $|\rho|=0.62\text{–}0.87$ across 4 models — not *pure* confidence, but high.)
3. **Brittleness gate.** Report $\mathrm{corr}(\text{stat},p_{\max})$ and $\mathrm{corr}(\text{stat},\mathrm{surprise})$ with bootstrap CIs at the *exact pinned aggregate*. A claim is discarded if the upper CI $\ge 0.75$. This is the formal "is it just confidence" rejection.
4. **Incremental AUROC over a fair base.** The decisive test: does the statistic add detection power **over $\{\mathrm{surprise}\}$** and over $\{\mathrm{surprise}, p_{\max}, \mathrm{null\_ratio}\}$? Equivalently, is the **partial correlation** with the label, controlling for confidence, nonzero?

**Honest current verdict (the fair-base correction).** The pilot's headline "+0.13 on Qwen3-8B" was measured over a *degraded* base ($\{\mathrm{surprise},\mathrm{null\_ratio}\}=0.602$, dragged below $\mathrm{surprise}$-alone $0.744$ by a sub-chance `null_ratio`). Recomputed over the fair $\{\mathrm{surprise}\}$ base: `fisher_eff_rank` $+0.044\ [-0.025,0.111]$, `shadow_logvol` $+0.076\ [-0.007,0.158]$ — **CIs cross zero** at $n=200$. What *survives*: the oriented **partial correlation** beyond confidence ($+0.28$ eff_rank, $-0.37$ shadow_logvol; CIs exclude 0). So there is a clean linear association beyond confidence, but the AUROC-increment is, so far, modest and underpowered per model.

**What actually separates them, then.** Confidence = the *darkness/scale* of the shadow; commitment-ambiguity = the *spectral shape / pre-image volume*. They are distinct geometric quantities, but partially correlated, so the separation is asserted only when (a) read through scale-invariant shape statistics, (b) at low-brittleness late layers, and (c) it beats confidence on a fair base in a **cross-model random-effects meta-analysis** (per-model $n$ is underpowered). Whether that meta-effect clears the pre-registered bar ($\ge 0.02$, CI $>0$, survives brittleness + multiplicity, spans $\ge 2$ families) is exactly what the comprehensive run is now deciding.

---

## 8. Falsification posture

The candidate is retired/null if, across the failure-regime cohort, the fair-base meta-CI includes 0, OR the effect lives only at high brittleness (confidence-coupled layers), OR it fails familywise multiplicity, OR it is below the minimum practical effect. A single-model positive (Qwen3-8B) that does not replicate across $\ge 2$ architecture families is, by pre-registration, **not** sufficient. The honest scoreboard today: math verified, plumbing verified, signal *suggestive but not decisive*; the verdict is pending the meta-analysis.
