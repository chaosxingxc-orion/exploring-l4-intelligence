#!/usr/bin/env bash
# Pipeline wrapper for one-shot env-setup + wave0_fetch (models/datasets/refs).
# Run inside WSL2 Ubuntu-24.04 as root.
set -e

WORKSPACE='/mnt/d/chao_workspace/exploring-l4-intelligence'
PROJECT="$WORKSPACE/projects/speech-mllm-training-free-rl"

stamp() { date '+%Y-%m-%d %H:%M:%S'; }

echo "=== STAGE 1: env-setup === $(stamp)"
cd "$WORKSPACE"
bash scripts/env-setup.sh

echo "=== STAGE 2: wave0 setup-env === $(stamp)"
cd "$PROJECT"
bash scripts/wave0_fetch.sh setup-env

echo "=== STAGE 3: models === $(stamp)"
bash scripts/wave0_fetch.sh models

echo "=== STAGE 4: datasets === $(stamp)"
bash scripts/wave0_fetch.sh datasets

echo "=== STAGE 5: refs === $(stamp)"
bash scripts/wave0_fetch.sh refs

echo "=== ALL DONE === $(stamp)"
