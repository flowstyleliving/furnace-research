# Dead Runs

These are failure modes, not model dossiers with conclusion-bearing positives.

## Falcon-180B

Handle: `tiiuae/falcon-180B-chat`

Backend: Modal torch on 2× A100.

Outcome: OOM even with `llm_int8_enable_fp32_cpu_offload=True`. The model is too large for the current Modal GPU envelope.

Canonical result: [results/dead-runs-2026-06-23](../results/dead-runs-2026-06-23.md)

## Command A 111B

Handle: `CohereForAI/c4ai-command-a-111B`

Backend: Modal torch on 2× A100.

Outcome: loads, but the standard chat template fails and the model emits `\n` instead of YES/NO on every sample.

Canonical result: [results/dead-runs-2026-06-23](../results/dead-runs-2026-06-23.md)
