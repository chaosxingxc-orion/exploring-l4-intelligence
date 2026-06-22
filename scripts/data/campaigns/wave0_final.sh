#!/usr/bin/env bash
# Wave0 final round: only AIR-Bench (must) + SLURP audio retry (best-effort).
# All other failed targets have been deferred per user decision (2026-06-15).
set -uo pipefail

WORKSPACE='/mnt/d/chao_workspace/exploring-l4-intelligence'
DR="$WORKSPACE/speechrl-data"
DS="$DR/datasets"
LOG="$DR/wave0_final.log"

source /root/.venvs/speechrl/bin/activate
export PATH="/root/.venvs/speechrl/bin:$PATH"
export LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONIOENCODING=utf-8
# Re-enable native unicode tqdm (we already have UTF-8 PowerShell + log file)
unset TQDM_ASCII NO_COLOR CLICOLOR TERM
export HF_ENDPOINT=https://hf-mirror.com

stamp() { date '+%Y-%m-%d %H:%M:%S'; }
section() { echo; echo "================================================================"; echo "==  $* @ $(stamp)"; echo "================================================================"; }

# --------------------------------------------------------------------------
section "AIR-Bench: ModelScope evalscope/AIR-Bench (~49GB)"
AB="$DS/air-bench"
mkdir -p "$AB"

# Retry 3x; ModelScope download supports resume.
ok=0
for attempt in 1 2 3; do
  echo "[air-bench] attempt $attempt/3"
  if modelscope download --dataset evalscope/AIR-Bench --local_dir "$AB" --max-workers 16; then
    ok=1
    break
  fi
  echo "[air-bench] attempt $attempt failed; sleeping 10s before retry"
  sleep 10
done
if [ "$ok" -eq 0 ]; then
  echo "[air-bench] ERROR: all 3 attempts failed"
else
  echo "[air-bench] OK"
fi
echo "[air-bench] final size: $(du -sh "$AB" 2>/dev/null | awk '{print $1}')"

# --------------------------------------------------------------------------
section "SLURP audio: best-effort IPv4 retry; skip on failure"
SLURP_AUDIO="$DR/repos/slurp/audio"
mkdir -p "$SLURP_AUDIO"
SLURP_URLS=(
  "https://zenodo.org/record/4274930/files/slurp_real.tar.gz"
  "https://zenodo.org/record/4274930/files/slurp_synth.tar.gz"
)
slurp_any_ok=0
for url in "${SLURP_URLS[@]}"; do
  fname=$(basename "$url")
  out="$SLURP_AUDIO/$fname"
  marker="$out.extracted"
  if [ -f "$marker" ]; then
    echo "[slurp] $fname already extracted, skip"
    slurp_any_ok=1
    continue
  fi
  echo "[slurp] aria2c $fname (IPv4, 30s connect timeout, 1 attempt)"
  if aria2c -4 -x 4 -s 4 -c --connect-timeout=30 --timeout=120 \
       --max-tries=2 --retry-wait=10 \
       -d "$SLURP_AUDIO" -o "$fname" "$url" \
       --console-log-level=warn --summary-interval=30 2>&1 | tail -10; then
    if [ -f "$out" ] && [ ! -f "$marker" ]; then
      echo "[slurp] extracting $fname"
      tar xzf "$out" -C "$SLURP_AUDIO" && touch "$marker" && slurp_any_ok=1
    fi
  else
    echo "[slurp] $fname download failed; will skip"
    rm -f "$out.aria2"
  fi
done
if [ "$slurp_any_ok" -eq 0 ]; then
  echo "[slurp] NOTE: SLURP audio not obtained. SLURP will be marked as code-only;"
  echo "[slurp] use MMAU-mini / MMAR for verifiable IC/SF reward instead."
fi

# --------------------------------------------------------------------------
section "DONE @ $(stamp)"
echo "Final inventory:"
du -sh "$DS"/* 2>/dev/null | sort -h
echo
echo "Total dataset size: $(du -sh "$DS" 2>/dev/null | awk '{print $1}')"
echo "Total models size:  $(du -sh "$DR/models" 2>/dev/null | awk '{print $1}')"
echo "Total repos size:   $(du -sh "$DR/repos"  2>/dev/null | awk '{print $1}')"
