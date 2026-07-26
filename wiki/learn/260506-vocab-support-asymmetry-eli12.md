# 🔦 Vocab-support asymmetry (Fisher's spotlight vs Raw's blueprint), ELI12

**Rigorous version:** [paper/pri-draft](../paper/pri-draft.md) §3.2 Pipeline ("Two SVD bases — the head-to-head") and §3.2 ("Capture")
**Companion:** [🧭 harp-vs-pri-eli12](260420-harp-vs-pri-eli12.md) (the bigger-picture head-to-head this page zooms into)

---

## 🎯 The question

Read the v3 pipeline carefully and you hit a thing that looks unfair. Fisher's basis is built from the **top-1024 vocab rows** of the unembedding matrix. Raw's basis is built from the **full vocab** — for some models that's 32,000 rows, for others it's 152,000. So we're SVD-ing different-sized matrices on the two sides of the same head-to-head. Isn't that rigging the comparison?

(It is the kind of question Junjie Hu — the HARP first author — would notice within ten seconds of reading the methods. So: what's the answer?)

## 🧠 The metaphor

Picture a stadium concert. The full crowd is the **vocabulary** — every possible next-token the model could pick. Tens of thousands of seats. The crowd doesn't all behave the same: at any given moment, certain sections are cheering and the rest are dim. The brightness of each section is the **token probability** $p_t$.

There are two ways to map "where the crowd is":

- 🏟️ **The architectural blueprint.** Every seat in the stadium, drawn once, before the show. No spotlight needed — you're documenting the structure of the building. This is the **Raw** SVD: a static, full-vocab map of the unembedding, computed once per model and cached. It doesn't care which sections are bright tonight.

- 🔦 **A spotlight that follows the singer.** Tracks where the cheering is loudest. The spotlight has finite intensity, weighted by how loud each section is — quiet sections fall off into darkness. This is the **Fisher** SVD: re-computed every sample, weighted by $\sqrt{p_t}$, so seats with $p_t \approx 0$ contribute basically nothing.

The asymmetry isn't *unfair* — it's *forced by what each tool is measuring.*

## 📊 What we measured

At gen_step = 1 the model's distribution $p_t$ is sharp. A handful of candidate tokens have nearly all the mass; everything else has $p_t \approx 0$. The top-1024 by $p_t$ typically captures **>99.9%** of the Fisher weight (depends on model and sample, but always overwhelming).

So Fisher's "truncation" to top-1024 isn't really a truncation — it's a numerical convenience. The discarded rows would have been multiplied by $\sqrt{p_t} \approx 0$ anyway. They're the dim seats; the spotlight wouldn't have lit them.

Raw has no spotlight. There's no $p_t$ to tell it which seats matter. So it must map every seat in the stadium, all 32k–152k of them, once, in advance.

## ✅ What this tells us

- ✅ **The asymmetry is necessary, not arbitrary.** Truncating Raw to a top-1024 subset would *bias* it — there's no $p_t$ to define which subset is salient. Computing Fisher on the full vocab would be infeasible (and numerically equivalent — sqrt of zero is still zero).
- ✅ **Both sides are symmetric where it matters: at the projection.** Each basis is a top-$r$ orthonormal set in the same $d$-dimensional hidden-state space. $\Delta h$ gets projected onto each the same way. The comparison is fair because the *output* of each procedure is a basis of the same shape, sitting in the same coordinate frame.
- 🎁 **The truncation is the "obvious answer to a non-obvious question."** What looks like a methodological asymmetry is actually a consequence of Fisher's defining feature — the per-sample $p_t$ weighting — doing exactly what it should.

## ⚠️ Caveats

- We have **not** run Fisher with the full vocab and no truncation, even though it's mathematically equivalent in the limit. A careful reviewer can still ask for that as a robustness check, and it's a reasonable ask. We'd run it on Qwen 2.5 (the sealed E17b anchor) first if anyone pushes.
- The 1024-row cutoff is a hyperparameter we picked once. We don't sweep it. For very-flat distributions (Qwen 2.5 7B's high-variance ctrl runs) it might matter slightly more than for sharp ones.

## 🎯 The one-line takeaway

> Fisher carries a spotlight, so it only maps the bright seats; Raw carries a blueprint, so it maps every seat. The maps end up the same shape — that's where they meet.
