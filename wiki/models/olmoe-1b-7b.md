# OLMoE-1B-7B-0924 Instruct (bf16)

HF handle: `allenai/OLMoE-1B-7B-0924-Instruct` @ `7f1c97f440f06ce36705e4f2b843edb5925f4498`

## Specs
- Size: 7B total parameters, about 1B active per token
- Architecture: mixture-of-experts, 16 layers, 16 query / 16 KV heads (MHA), 64 experts with top-8 routing in every layer, `norm_topk_prob = false`
- Precision: native bf16, no quantization
- Backend: torch on Modal, one A10G (non-byte-comparable with MLX panels)
- Tokenizer: BOS = EOS = `<|endoftext|>` (id 50279), emitted once by the chat template

## Role in the research line
- The only model in the MoE router pilot — the project's first mixture-of-experts cell.
- Chosen for being small, fully open (training data included), MoE in every layer, and plain multi-head attention.

## Main verdicts
- `router-pilot-2026-10-08` - spending decision **STOP**: router uncertainty is at chance on ANLI R1 (0.529) and loses to attention by 0.07 on HaluEval-QA (router 0.832 vs `final_js` 0.904).
- `router-pilot-2026-10-08` - on HaluEval, router entropy at layer 3 of 16 is selected in all five folds and beats output confidence (0.832 vs 0.773); descriptive.
- `router-pilot-2026-10-08` - answers YES/NO on 97% (ANLI) and 100% (HaluEval) of prompts.
- `correctness-labels-2026-10-13` - against its own errors (accuracy 0.562 ANLI, 0.695 HaluEval), no router or attention signal beyond a best-of null; output entropy 0.600 / 0.641 does. The pilot's HaluEval router 0.832 is class discrimination. [[results/correctness-labels-2026-10-13]]

Canonical result page: [[results/router-pilot-2026-10-08]].
