#!/bin/bash
# Sequential driver for PLAN §2: control then flipped per model; 14 h budget, size-scaled projection.
set -u
cd "$(dirname "$0")"
PY=/Users/msrk/Documents/commit-confluence/.venv/bin/python
HUB=~/.cache/huggingface/hub
START=$(date +%s); BUDGET=$((14*3600))
RATE=4.3; REFGB=2.0   # Phi-4 marginal s/row and weight size (RUN_LOG.md)
for m in Phi-4-mini-instruct-4bit Mistral-7B-Instruct-v0.3-4bit Llama-3.1-8B-Instruct-4bit Qwen3-8B-4bit Mistral-Nemo-Instruct-2407-4bit; do
  gb=$(du -sk $HUB/models--mlx-community--$m | awk '{print $1/1048576}')
  proj=$(awk -v r=$RATE -v g=$gb -v ref=$REFGB 'BEGIN{print int(2*(120+1000*r*g/ref))}')
  now=$(date +%s)
  if (( now - START + proj > BUDGET )); then echo "[skip] $m projected ${proj}s exceeds budget" | tee -a outputs/driver.log; continue; fi
  for c in control flipped; do
    t0=$(date +%s)
    $PY extract_chat_template.py --model mlx-community/$m --condition $c --out-dir outputs/full > outputs/$m.$c.log 2>&1
    rc=$?; t1=$(date +%s)
    echo "[done] $m $c rc=$rc elapsed=$((t1-t0))s" | tee -a outputs/driver.log
    [ $rc -ne 0 ] && break
  done
  RATE=$(awk -v e=$((t1-t0)) -v g=$gb -v ref=$REFGB 'BEGIN{print (e-120)/1000*ref/g}')
done
echo "[end] total=$(( $(date +%s) - START ))s" | tee -a outputs/driver.log
