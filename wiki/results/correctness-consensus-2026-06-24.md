# Correctness vs Consensus — TriviaQA Paired (2026-06-24)

**Status:** `[RESULTS — negative]` — consensus voting adds no value over the strongest single model on TriviaQA paired. Benchmark is wrong for the question. Custom design required.

## 1. Motivation

Having established that models disagree on ~18.5% of ANLI samples (commitment-convergence), the natural follow-up: does majority vote across models outperform any single model at correctness? And does the pattern of errors (different models wrong on different samples) create headroom for consensus?

## 2. Method

5 models on TriviaQA paired (n=200):
- Qwen2.5-7B (nf4)
- Qwen2.5-32B (nf4)
- Mistral-Large-2411 (nf4, `Y`→YES normalized)
- Yi-1.5-34B-Chat (nf4)
- Llama-3.3-70B (nf4)

Each model's first-token commit (YES/NO) scored against ground-truth correctness. Majority vote = 3+ models agree. Consensus lift = majority accuracy minus best single-model accuracy.

## 3. Label Mapping (CRITICAL — fixed 2026-06-24)

```
label=0 → kind=correct → proposed answer IS correct → model should say YES
label=1 → kind=wrong   → proposed answer is WRONG  → model should say NO
```

This is the OPPOSITE of the intuitive `label=1=YES` mapping. Always verify against `meta.kind` field before computing accuracy. All Qwen models and Llama-70B strongly favor NO (~75-100% NO commits). With inverted mapping, models appear worse than random. With correct mapping, they recover.

## 4. Results

| Model | Accuracy |
|---|---|
| Qwen2.5-7B | 75.0% |
| Qwen2.5-32B | 82.0% |
| Mistral-Large | 90.5% |
| Yi-1.5-34B | 93.3% |
| Llama-3.3-70B | **96.5%** |

**Agreement structure:** 149/200 samples unanimous. 50/200 split. 1/200 genuinely disputed (different models, different answers). Near-zero entropy in the commit space.

**Consensus lift: +0.002.** Effectively null. Majority vote is 96.5% (same as Llama-70B alone). On the 50 split samples, Llama-70B is correct 96% of the time — the strongest model IS the consensus signal. There is no headroom.

## 5. Why This Fails

TriviaQA paired is **sterile** for the consensus-vs-correctness question:

1. **Single-model dominance:** Llama-70B at 96.5% leaves 3.5% headroom total. Even perfect consensus on the remaining 3.5% could add at most +1.5pp.
2. **Error pattern overlap:** When Llama-70B is wrong, other models are also wrong. Errors are shared, not complementary.
3. **Ceiling effect:** Multiple models cluster above 90%. No model scores 50-75% with different error patterns.

## 6. Pre-Flight Rules (for future correctness analyses)

| Benchmark | Verdict | Why |
|-----------|---------|-----|
| ANLI R1 | ❌ Skip | Adversarial by design — models ≤ random. Consensus = shared bias, not accuracy. |
| TriviaQA paired | ❌ Skip | Single-model dominance (Llama-70B 96.5%). No headroom. |
| **Required** | 🔨 Custom | Need benchmark where ALL models score 50-75% with DIFFERENT error patterns. No model above 80%. |

## 7. Artifacts

- Analysis script: `/tmp/triviaqa_analysis.py` (5-model consensus-vs-correctness, loads JSONL dumps, normalizes `Y`→YES, computes agreement tiers, majority-vote accuracy, per-model disagreement accuracy)
- All commit dumps: `commit_dump/` on Modal volume `model-cache`
