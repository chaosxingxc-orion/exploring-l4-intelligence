#!/usr/bin/env bash
# Inventory: detect partial/complete downloads via expected-payload heuristics.
# Reports per asset: size | files | status (COMPLETE|PARTIAL|MISSING|UNKNOWN).
# Paths derive from this script's location; override with SPEECHRL_DATA_DIR / SPEECHRL_VENV.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE="${SPEECHRL_WORKSPACE:-$(cd "$SCRIPT_DIR/../.." && pwd)}"
DR="${SPEECHRL_DATA_DIR:-$WORKSPACE/speechrl-data}"
SPEECHRL_VENV="${SPEECHRL_VENV:-$HOME/.venvs/speechrl}"

echo '=== Top-level sizes ==='
du -sh "$DR"/* 2>/dev/null

# Function: check dataset completeness via heuristic per-dataset
# Reports: name | size | files | status (COMPLETE|PARTIAL|MISSING|UNKNOWN)
check_ds() {
  local name="$1"
  local d="$DR/datasets/$name"
  local expect_min_files="$2"   # min file count for completeness
  local expect_min_size_mb="$3" # min size in MB for completeness
  if [ ! -e "$d" ]; then
    printf '  %-22s MISSING\n' "$name"
    return
  fi
  local nfiles
  nfiles=$(find -L "$d" -type f ! -name '.*' ! -name '*.lock' ! -name '*.incomplete' 2>/dev/null | wc -l)
  local size_kb
  size_kb=$(du -sLk "$d" 2>/dev/null | awk '{print $1}' | head -1)
  local size_mb=$(( size_kb / 1024 ))
  local size_h
  size_h=$(du -sLh "$d" 2>/dev/null | awk '{print $1}' | head -1)
  local n_incomplete
  n_incomplete=$(find -L "$d" -name '*.incomplete' -o -name '*.tmp' -o -name '*.part' 2>/dev/null | wc -l)
  local status='UNKNOWN'
  if [ "$nfiles" -ge "$expect_min_files" ] && [ "$size_mb" -ge "$expect_min_size_mb" ] && [ "$n_incomplete" -eq 0 ]; then
    status='COMPLETE'
  elif [ "$nfiles" -gt 0 ]; then
    status='PARTIAL'
  fi
  printf '  %-22s files=%-6s size=%-8s incomplete=%-3s %s\n' "$name" "$nfiles" "$size_h" "$n_incomplete" "$status"
}

check_model() {
  local name="$1"
  local d="$DR/models/$name"
  local expect_min_size_mb="$2"
  if [ ! -d "$d" ]; then
    printf '  %-30s MISSING\n' "$name"
    return
  fi
  local has_cfg=N has_weights=N
  [ -f "$d/config.json" ] || [ -f "$d/configuration.json" ] && has_cfg=Y
  if compgen -G "$d/*.safetensors" >/dev/null 2>&1 || \
     compgen -G "$d/*.safetensors.index.json" >/dev/null 2>&1 || \
     compgen -G "$d/*.bin" >/dev/null 2>&1 || \
     compgen -G "$d/*.gguf" >/dev/null 2>&1; then
    has_weights=Y
  fi
  local size_kb
  size_kb=$(du -sk "$d" 2>/dev/null | awk '{print $1}')
  local size_mb=$((size_kb/1024))
  local size_h
  size_h=$(du -sh "$d" 2>/dev/null | awk '{print $1}')
  local n_incomplete
  n_incomplete=$(find "$d" -name '*.incomplete' -o -name '*.tmp' -o -name '*.part' 2>/dev/null | wc -l)
  local status='UNKNOWN'
  if [ "$has_cfg" = Y ] && [ "$has_weights" = Y ] && [ "$size_mb" -ge "$expect_min_size_mb" ] && [ "$n_incomplete" -eq 0 ]; then
    status='COMPLETE'
  elif [ "$has_cfg" = Y ] || [ "$has_weights" = Y ] || [ "$size_mb" -gt 100 ]; then
    status='PARTIAL'
  fi
  printf '  %-30s cfg=%s weights=%s size=%-8s incomplete=%-3s %s\n' "$name" "$has_cfg" "$has_weights" "$size_h" "$n_incomplete" "$status"
}

echo
echo '=== Models (24GB-friendly default + optional) ==='
# Min-MB heuristics: very loose lower bound for "looks complete"
check_model qwen3-omni-30b-a3b-instruct 8000   # INT4 ~8-15GB
check_model moss-audio-8b-instruct       8000  # 8B BF16 ~16GB
check_model nemotron3-nano-omni-nvfp4    8000  # NVFP4 ~10-18GB
check_model minicpm-o-4_5-gguf           2000  # GGUF often a few GB
check_model minicpm-o-4_5                4000
check_model baichuan-omni-1d5            6000  # ~7B
check_model kimi-audio-7b-instruct       6000
check_model omni-embed-nemotron-3b       6000  # W4 omni embedding ~4.7B

echo
echo '=== Datasets (heuristic completeness) ==='
# Loose floor; tweak if needed
check_ds librispeech         50  10000     # 100h+960h roughly tens of GB
check_ds mmau-mini            5  100
check_ds mmar                 5  100
check_ds meld                10  500
check_ds crema-d             10  100
check_ds minds14              5  100
check_ds minds14-xtreme_s     5  500
check_ds covost2              3   10
check_ds fleurs              20  500
check_ds voxceleb            20 5000
check_ds air-bench           10  500
check_ds slurp                5   10

echo
echo '=== Refs ==='
for r in slurp mbr-for-asr AudioGenie-Reasoner TTRL TPO JitRL slue-toolkit; do
  d="$DR/repos/$r"
  if [ -d "$d/.git" ]; then
    sz=$(du -sh "$d" 2>/dev/null | awk '{print $1}')
    printf '  %-25s PRESENT size=%s\n' "$r" "$sz"
  else
    printf '  %-25s MISSING\n' "$r"
  fi
done

echo
echo '=== venv health ==='
if [ -f "$SPEECHRL_VENV/bin/activate" ]; then
  echo 'venv activate: OK'
  "$SPEECHRL_VENV/bin/python" - <<'PY' 2>&1 | head -10
try:
    import torch
    print('torch:', torch.__version__, 'cuda?', torch.cuda.is_available())
except Exception as e:
    print('torch ERR:', e)
for mod in ('huggingface_hub','modelscope','hydra','omegaconf','mlflow','librosa','soundfile','jiwer','datasets','transformers','vllm'):
    try:
        m = __import__(mod)
        print(f'{mod}:', getattr(m, "__version__", "?"))
    except Exception as e:
        print(f'{mod} MISSING')
PY
else
  echo 'venv activate MISSING'
fi
