#!/usr/bin/env bash
# Primary data-fetch entry point (smart wave0 driver).
#   - skips already-complete assets, logs to the data dir (survives WSL recycles)
#   - replaces the slow upstream SLURP audio downloader with aria2c -x16 (mass parallel)
#   - does NOT recursively run download scripts inside cloned reference repos
#     (those are reference-code only; their data scripts often duplicate our datasets)
#
# Models/datasets are NEVER committed to git (see .gitignore and docs/data.md). This
# script pulls ~281 GB into $SPEECHRL_DATA_DIR locally; users fetch their own copy.
# The actual per-asset engine is projects/speech-mllm-training-free-rl/scripts/wave0_fetch.sh.
#
# Paths derive from this script's location (survives the repo being renamed/moved).
# Override via env: SPEECHRL_WORKSPACE, SPEECHRL_DATA_DIR, SPEECHRL_VENV.
set -uo pipefail

# ---------- paths (derived; env-overridable) ----------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE="${SPEECHRL_WORKSPACE:-$(cd "$SCRIPT_DIR/../.." && pwd)}"
PROJECT="$WORKSPACE/projects/speech-mllm-training-free-rl"
DR="${SPEECHRL_DATA_DIR:-$WORKSPACE/speechrl-data}"
WAVE0="$PROJECT/scripts/wave0_fetch.sh"
LOG="$DR/wave0_smart.log"
mkdir -p "$DR"

stamp() { date '+%Y-%m-%d %H:%M:%S'; }
section() { echo; echo "================================================================"; echo "==  $* @ $(stamp)"; echo "================================================================"; }

# Activate venv
SPEECHRL_VENV="${SPEECHRL_VENV:-$HOME/.venvs/speechrl}"
# shellcheck disable=SC1091
source "$SPEECHRL_VENV/bin/activate"
export PATH="$SPEECHRL_VENV/bin:$PATH"

# --- Make output readable in Windows PowerShell terminal ---
# Force UTF-8 everywhere; ASCII-only progress bars; less verbose progress
export LANG=C.UTF-8
export LC_ALL=C.UTF-8
export PYTHONIOENCODING=utf-8
# tqdm: ASCII chars instead of Unicode blocks; stay on tty so it overwrites
export TQDM_ASCII=1
# huggingface_hub progress
export HF_HUB_DISABLE_PROGRESS_BARS=0
# modelscope: it uses tqdm internally; TQDM_ASCII handles it.
# Also drop colored output where possible
export NO_COLOR=1
export CLICOLOR=0
export TERM=dumb

# Skip-existing on; SLURP audio handled separately via aria2.
export SPEECHRL_SKIP_EXISTING=1
export SPEECHRL_SKIP_SLURP_AUDIO=1

# 1) Symlink to satisfy minicpm-o-4_5-gguf skip check
if [ -d "$DR/models/minicpm-o-4_5" ] && [ ! -e "$DR/models/minicpm-o-4_5-gguf" ]; then
  ln -sfn "$DR/models/minicpm-o-4_5" "$DR/models/minicpm-o-4_5-gguf"
  echo "[fix] symlinked minicpm-o-4_5-gguf -> minicpm-o-4_5"
fi

# 2) Purge obviously-partial dataset dirs so CLI redoes them
purge_partial() {
  local d="$1" why="$2"
  [ -e "$d" ] && { echo "[purge] $d ($why)"; rm -rf "$d"; }
}
[ -d "$DR/datasets/minds14-xtreme_s" ] && {
  size_kb=$(du -sLk "$DR/datasets/minds14-xtreme_s" 2>/dev/null | awk '{print $1}')
  [ "${size_kb:-0}" -lt 102400 ] && purge_partial "$DR/datasets/minds14-xtreme_s" "<100MB"
}
[ -d "$DR/datasets/covost2" ] && {
  size_kb=$(du -sLk "$DR/datasets/covost2" 2>/dev/null | awk '{print $1}')
  [ "${size_kb:-0}" -lt 5120 ] && purge_partial "$DR/datasets/covost2" "<5MB"
}

# 3) Models
section "MODELS"
bash "$WAVE0" m_qwen3omni
bash "$WAVE0" m_moss
bash "$WAVE0" m_nemotron
bash "$WAVE0" m_minicpm_gguf

# W4 omni-embedding model (nv-community/omni-embed-nemotron-3b, ~4.7B).
# Set SPEECHRL_SKIP_OMNI_EMBED=1 to skip if you only need the generation models.
if [ -z "${SPEECHRL_SKIP_OMNI_EMBED:-}" ]; then
  bash "$WAVE0" m_omni_embed_nemotron
fi

# 4) Datasets (excluding slurp; we do slurp ourselves with aria2 for speed)
section "DATASETS"
for tgt in d_librispeech d_mmau_mini d_mmar d_meld d_cremad d_minds14 d_covost2 d_fleurs d_voxceleb d_air_bench; do
  echo "[smart] target: $tgt"
  bash "$WAVE0" "$tgt" || echo "[smart] WARN: $tgt failed; continuing"
done

# 5) Reference repos (clone only; no recursive data-script execution)
section "REFS (clone only)"
bash "$WAVE0" refs

# 6) SLURP audio with aria2c -x 16 (parallel) using the manifest the script
#    already produces. This replaces the upstream wget-style downloader.
section "SLURP (aria2-accelerated)"
SLURP_DIR="$DR/repos/slurp"
SLURP_AUDIO="$SLURP_DIR/audio"
SLURP_MANIFEST="$DR/manifests/slurp.links.txt"
mkdir -p "$DR/manifests" "$SLURP_AUDIO"

# Generate manifest (cheap; just curls one file)
( cd "$PROJECT" && bash "$WAVE0" check >/dev/null 2>&1 || true )
# Fallback: regenerate manifest directly
if [ ! -s "$SLURP_MANIFEST" ]; then
  echo "[slurp] regenerating manifest from upstream"
  curl -L -sS -m 30 "https://raw.githubusercontent.com/pswietojanski/slurp/master/scripts/download_audio.sh" \
    | grep -Eo 'https://[^[:space:]\\]+' \
    | grep -E 'zenodo\.org/.*/files/.*\.tar\.gz' \
    | sort -u >"$SLURP_MANIFEST.tmp"
  mv "$SLURP_MANIFEST.tmp" "$SLURP_MANIFEST"
fi
echo "[slurp] manifest: $SLURP_MANIFEST ($(wc -l <"$SLURP_MANIFEST") urls)"

# Clone repo if missing
if [ ! -d "$SLURP_DIR/.git" ]; then
  bash "$WAVE0" refs >/dev/null 2>&1 || true
fi

# aria2c parallel download with continuation; idempotent.
if command -v aria2c >/dev/null 2>&1 && [ -s "$SLURP_MANIFEST" ]; then
  echo "[slurp] aria2c -x16 -j4 -c -d $SLURP_AUDIO -i $SLURP_MANIFEST"
  aria2c -x 16 -s 16 -j 4 -c --auto-file-renaming=false --allow-overwrite=false \
    --dir="$SLURP_AUDIO" --input-file="$SLURP_MANIFEST" \
    --console-log-level=warn --summary-interval=30 \
    || echo "[slurp] WARN: aria2c returned non-zero; some shards may need retry"
  # Extract tarballs that haven't been extracted
  for tgz in "$SLURP_AUDIO"/*.tar.gz; do
    [ -f "$tgz" ] || continue
    marker="$tgz.extracted"
    if [ ! -f "$marker" ]; then
      echo "[slurp] extracting $(basename "$tgz")"
      tar -xzf "$tgz" -C "$SLURP_AUDIO" && touch "$marker"
    fi
  done
else
  echo "[slurp] WARN: aria2c missing or manifest empty; falling back to upstream script"
  unset SPEECHRL_SKIP_SLURP_AUDIO
  bash "$WAVE0" d_slurp || true
fi
ln -sfn "$SLURP_DIR" "$DR/datasets/slurp"

section "DONE"
echo "All wave0 targets attempted at $(stamp). Re-run on failure; CLIs resume."
