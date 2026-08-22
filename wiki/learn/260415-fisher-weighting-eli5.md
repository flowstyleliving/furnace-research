# 🧮 Why `sqrt(p_t) · W_u`, ELI5

**Rigorous version:** [pri-v3-plan](../pri-v3/pri-v3-plan.md) §Fisher operator
**Companion:** [null-space-eli12](260419-null-space-eli12.md) (what we do with the SVD output)

---

## 🎯 The setup

- `W_u` 📋 = the model's **unembedding matrix** — every row is a "fingerprint" for one vocabulary word. Shape: `(vocab_size, d)`. Big matrix. \~50,000 rows.
- `p_t` 🎲 = the probability the model gives each word right now. Shape: `(vocab_size,)`. Sums to 1.
- We're going to do SVD on this thing to find the "live knobs." 🎛️

---

## 🤔 Why not just SVD on `W_u` alone?

Because `W_u` treats every word equally. 📋

But the model **doesn't** treat every word equally. Right now it might be 90% sure the next word is "the" and 0.0001% sure it's "platypus." 🦆

If we SVD the raw `W_u`, we'd find directions that move "platypus" — true mathematically, **useless practically**. The model doesn't care about platypus right now. ❌

---

## 💡 The fix: weight by what the model cares about

We multiply each row of `W_u` by `sqrt(p_t[that_word])`:

```
row for "the":      sqrt(0.90) ≈ 0.95   → barely shrunk 🟢
row for "platypus": sqrt(1e-6) ≈ 0.001  → almost zero 🔴
```

Now the SVD sees:
- 🟢 "Big rows" = words the model thinks are likely → directions that move them count a LOT
- 🔴 "Tiny rows" = words the model thinks are unlikely → directions that move them count almost nothing

The "live knobs" we find are now **knobs that move words the model is actually considering**, not knobs that move random vocab. 🎯

---

## 📐 Why `sqrt`, not just `p_t`?

Because of how the **Fisher Information** math works out. 🤓

The Fisher Information Matrix for a softmax is roughly:
```
F ≈ W_uᵀ · diag(p_t) · W_u
```

If you write `diag(p_t) = diag(sqrt(p_t)) · diag(sqrt(p_t))`, you can group things as:
```
F = (sqrt(p_t) · W_u)ᵀ · (sqrt(p_t) · W_u)
  = Aᵀ A     where  A = sqrt(p_t) · W_u
```

So the SVD of `A` gives you **exactly** the eigendecomposition of `F`. ✨ One operation, two birds. 🐦🐦

The `sqrt` isn't a hack — it's the natural square-root factor of the Fisher operator. The singular values of `A` are the square roots of Fisher's eigenvalues. 📐

---

## ⚠️ Caveats

- We don't actually use **all** rows of `W_u`. We restrict to the top \~256–1024 highest-probability rows first (the "support truncation" in `fim_lowrank`). The `sqrt(p_t)` weighting then re-scales within that support. So "live knobs" = top singular directions of `sqrt(p_t) · W_u` **on the top-probability support**.
- This means a word with `p_t ≈ 1e-9` is dropped entirely (not just shrunk to \~0). Slight asymmetry vs. pure mathematical weighting, but the dropped rows would round to zero anyway in finite precision.

---

## 🧠 Intuition in one sentence

> `sqrt(p_t) · W_u` is `W_u` with the boring vocabulary turned down, so the SVD finds directions that matter for the words **the model is actually thinking about right now**. 🎚️
