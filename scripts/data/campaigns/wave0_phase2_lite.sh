#!/usr/bin/env bash
# Wave0 phase-2 LITE: only audio-relevant evalscope datasets.
# Skips GSM8K-V (visual GSM8K) and MMStar (visual multimodal).
# Run AFTER AIR-Bench finishes (currently downloading via inherited modelscope PID).
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
  local owner="$1" repo="$2" outdir="$3"
  mkdir -p "$outdir"
  for attempt in 1 2 3; do
    echo "[ms] $owner/$repo attempt $attempt/3"
    if modelscope download --dataset "$owner/$repo" --local_dir "$outdir" --max-workers 16; then
      echo "[ms] $owner/$repo OK"
      return 0
    fi
    sleep 8
  done
  echo "[ms] $owner/$repo FAIL"
  return 1
}

# Wait for any in-flight AIR-Bench modelscope process to finish first
section "Waiting for any AIR-Bench modelscope process to finish"
while pgrep -f 'modelscope download.*evalscope/AIR-Bench' > /dev/null 2>&1; do
  echo "[wait] AIR-Bench still running, sleep 60s"
  sleep 60
done
echo "[wait] AIR-Bench process gone; proceeding"
echo "[air-bench] final size: $(du -sh "$DS/air-bench" | awk '{print $1}')"

# Audio: Seed-TTS-Eval (TTS speech-output evaluation; relevant for W1/W2)
section "Seed-TTS-Eval: TTS speech-output evaluation suite"
ms_dl evalscope Seed-TTS-Eval "$DS/seed-tts-eval"
echo "[seed-tts] size: $(du -sh "$DS/seed-tts-eval" | awk '{print $1}')"

# Reasoning: AIME 24/25/26 - text-only competition math.
# Justification: verifiable exact-match reward standard, transferable to speech RL.
section "AIME24/25/26: math competition (text-only verifiable RL reward refs)"
ms_dl evalscope aime24 "$DS/aime24"
ms_dl evalscope aime25 "$DS/aime25"
ms_dl evalscope aime26 "$DS/aime26"

section "DONE @ $(stamp)"
echo "Skipped (per user: visual datasets not needed for speech multimodal project):"
echo "  - GSM8K-V  (visual GSM8K)"
echo "  - MMStar   (visual multimodal eval)"
echo
echo "Final dataset inventory:"
du -sh "$DS"/* 2>/dev/null | sort -h
echo
echo "Total dataset size: $(du -sh "$DS" 2>/dev/null | awk '{print $1}')"
echo "Total speechrl-data: $(du -sh "$DR" 2>/dev/null | awk '{print $1}')"
