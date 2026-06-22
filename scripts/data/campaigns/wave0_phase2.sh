#!/usr/bin/env bash
# Wave0 phase-2 complete: finish AIR-Bench + add high-value evalscope datasets.
# Uses setsid to fully detach from the wsl client's process group (so SIGINT from
# wsl client teardown does NOT propagate to long-running children).
set -uo pipefail

WORKSPACE='/mnt/d/chao_workspace/exploring-l4-intelligence'
DR="$WORKSPACE/speechrl-data"
DS="$DR/datasets"

source /root/.venvs/speechrl/bin/activate
export PATH="/root/.venvs/speechrl/bin:$PATH"
export LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONIOENCODING=utf-8
export HF_ENDPOINT=https://hf-mirror.com

stamp() { date '+%Y-%m-%d %H:%M:%S'; }
section() { echo; echo "================================================================"; echo "==  $* @ $(stamp)"; echo "================================================================"; }

ms_dl() {
  # Wrapper: modelscope download with retry; survives one HTTP timeout
  local owner="$1" repo="$2" outdir="$3"
  mkdir -p "$outdir"
  for attempt in 1 2 3; do
    echo "[ms] $owner/$repo attempt $attempt/3 -> $outdir"
    if modelscope download --dataset "$owner/$repo" --local_dir "$outdir" --max-workers 16; then
      echo "[ms] $owner/$repo OK"
      return 0
    fi
    echo "[ms] $owner/$repo attempt $attempt failed; sleep 8"
    sleep 8
  done
  echo "[ms] $owner/$repo FINAL FAIL"
  return 1
}

# -- Finish AIR-Bench (resume) --------------------------------------------
section "AIR-Bench: finish (already partial 5.8G/3966 files)"
ms_dl evalscope AIR-Bench "$DS/air-bench"
echo "[air-bench] size: $(du -sh "$DS/air-bench" | awk '{print $1}')"

# -- Audio: Seed-TTS-Eval --------------------------------------------------
section "Seed-TTS-Eval: TTS speech-output evaluation suite"
ms_dl evalscope Seed-TTS-Eval "$DS/seed-tts-eval"
echo "[seed-tts] size: $(du -sh "$DS/seed-tts-eval" | awk '{print $1}')"

# -- Reasoning RL benchmarks (verifiable rewards) -------------------------
section "AIME24/25/26: math competition (verifiable RL reward standard)"
ms_dl evalscope aime24 "$DS/aime24"
ms_dl evalscope aime25 "$DS/aime25"
ms_dl evalscope aime26 "$DS/aime26"

section "GSM8K-V: visual GSM8K (multimodal RL)"
ms_dl evalscope GSM8K-V "$DS/gsm8k-v"

section "MMStar: multi-modal eval"
ms_dl evalscope MMStar "$DS/mmstar"

# -- Inventory ------------------------------------------------------------
section "DONE @ $(stamp) - inventory"
du -sh "$DS"/* 2>/dev/null | sort -h
echo
echo "Total dataset size: $(du -sh "$DS" 2>/dev/null | awk '{print $1}')"
echo "Total speechrl-data: $(du -sh "$DR" 2>/dev/null | awk '{print $1}')"
