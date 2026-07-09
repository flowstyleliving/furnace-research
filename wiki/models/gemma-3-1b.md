# Gemma 3-1B Instruct (4-bit) — EXCLUDED

MLX handle: `mlx-community/gemma-3-1b-it-4bit`

**Role in v3.1:** EXCLUDED from the cross-architecture sweep after gate-failing at 11/20 = 55% on n=20 stratified controls (2026-04-26, post-PR#7 stratification + three-tier parser fixes). Originally intended as the 1B endpoint of a Gemma 1B↔4B within-family scale axis; axis now reduced to a single point ([Gemma 3-4B](gemma-3-4b.md)).

## Specs
- Size: 1B parameters (smallest in the v3.1 lineup)
- Quantization: 4-bit (MLX)
- Layers: 26; hidden_dim D = 1152; vocab V = 262,144
- Dtype: float16 (in contrast to 4B's bfloat16)
- Output projection: tied embeddings (`embed_tokens.as_linear`)
- Class: `mlx_lm.models.gemma3_text.Model`

## Why excluded — model-capability gate failure

Under the v3.1 fixes (`--gate-max-tokens 12` operational rescue + 3-tier `check_answer` parser, PR #7 stratified preflight), Gemma 1B passed only **11/20 = 55%** of the behavioral preflight on stratified controls. `--gate-verbose` revealed the failure mode:

> All 20 control puzzles produce outputs starting with **`"Answer: NO"`** regardless of premises.

Sample (all 20 are this pattern, with various plausible-sounding text after the leading verdict):
- exp=YES, output=`"Answer: NO  Final Answer: The final answer is 3..."`
- exp=YES, output=`"Answer: NO  Final Analysis: The premises are: 1. All zeniths are krels..."`
- exp=YES, output=`"Answer: NO  Now solve the following: Instruction: Read the premises..."`

The parser is correctly extracting "NO" — this is genuine model behavior, not a parser artifact. **Gemma 1B defaults to `Answer: NO` on YES controls regardless of what the premises say.** A 3B parameter model (Llama 3.2 3B) handles the same prompts at 100% gate accuracy under identical conditions; Gemma 1B at 1B parameters is below the capability threshold for this prompt format.

This connects to the same prompt-format sensitivity that excluded Phi-3.5-mini at 60% on the original 2026-04-23 main run — except Phi was a parser-fix-recoverable failure (front-loaded answer + format completion fooling last-match-anywhere parser), and Gemma 1B is a genuine capability shortfall.

## Pipeline validation despite exclusion

The full `run_experiment` loop was validated end-to-end on Gemma 1B with `--skip-gate` at n=2/cell smoke (run-04, 112 rows, 26 post-norm columns populated, no NaN, no zero-crush). The Gemma γ extraction fix (the "+1" RMSNorm formulation, see [gemma-3-4b](gemma-3-4b.md) for the bug detail) was caught and verified on both Gemma 1B and 4B before any main-run data was captured.

## Architectural notes
- Gemma 3-1B uses the text-only `gemma3_text.Model` class (no multimodal wrapper, unlike 4B+)
- RMSNorm `(1.0 + γ)` formulation (same Gemma 3 quirk as 4B)
- gen_step=1 commit token: defaults to `Answer: NO` on this benchmark regardless of premises (the failure mode)

## Implication for the within-family scale axis

The originally-planned **Gemma 1B ↔ Gemma 4B architecture-held-fixed scale-replication test** (the cleanest test of HARP's inverse-g-vs-capability claim, since both share the Gemma 3 architecture) collapses to a single point. The architecture-held-fixed scale-replication test of the cross-architecture motifs is left to v4 — possibly with a likelihood-based verification protocol that doesn't require parsable YES/NO output (see [paper/pri-draft.md](../paper/pri-draft.md) §5.4 Future work).

## Trace dump pointers
- n=2 smoke (--skip-gate): `experiments/v3-main-run/2026-04-26/run-04/gemma-3-1b-it-4bit_results.parquet`
- n=10 pilot (gate fail at 75%, Phase 3 attempt): `experiments/v3-main-run/2026-04-26/run-05/` (Gemma 1B skipped during run; only 4B has full output)

## Cross-references
- v3.1 lineup decision: [results/v3.1-replicate](../results/v3.1-replicate.md)
- Sibling that did clear: [gemma-3-4b](gemma-3-4b.md)
- Paper §3.3 exclusion paragraph: [paper/pri-draft.md](../paper/pri-draft.md)
