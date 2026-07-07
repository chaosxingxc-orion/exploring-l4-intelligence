#!/usr/bin/env bash
# fetch-candidates.sh — download the WS-D survey-sourced candidate datasets (docs/datasets.candidates.json).
#
# Uses the SAME high-throughput, mirror-compatible path as fetch-data.sh: hf-mirror.com + hfd + aria2c
# (multi-connection). The python `hf` CLI is only a fallback (it rejects hf-mirror's HEAD metadata).
# B-grade obtainable datasets NOT in the frozen datasets.lock.json; sources web-verified 2026-07-07.
#
#   bash scripts/data/fetch-candidates.sh --list        # list only, fetch nothing
#   bash scripts/data/fetch-candidates.sh               # fetch all HF + git; gated ones print instructions
#   bash scripts/data/fetch-candidates.sh squtr ...     # fetch only the named dataset(s)
#
# Env overrides: SPEECHRL_DATA_DIR, SPEECHRL_HF_ENDPOINT (default hf-mirror.com), SPEECHRL_HFD_THREADS (8).
# Deps: aria2c + hfd (auto-fetched) for HF; git for github. `bash scripts/data/fetch-data.sh --install-deps`.
set -u
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
DATA="${SPEECHRL_DATA_DIR:-$REPO_ROOT/speechrl-data}"
DS="$DATA/datasets"

# venv + China-friendly mirror + high concurrency — mirrors fetch-data.sh exactly
SPEECHRL_VENV="${SPEECHRL_VENV:-$HOME/.venvs/speechrl}"
# shellcheck disable=SC1091
[ -f "$SPEECHRL_VENV/bin/activate" ] && { source "$SPEECHRL_VENV/bin/activate"; export PATH="$SPEECHRL_VENV/bin:$PATH"; }
export HF_ENDPOINT="${SPEECHRL_HF_ENDPOINT:-https://hf-mirror.com}"
export HF_HUB_DISABLE_XET="${HF_HUB_DISABLE_XET:-1}"
export LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONIOENCODING=utf-8 NO_COLOR=1
HFD_THREADS="${SPEECHRL_HFD_THREADS:-8}"
HF_CLI="$(command -v hf || command -v huggingface-cli || echo hf)"
mkdir -p "$DS"
echo "[fetch-candidates] data=$DS | HF_ENDPOINT=$HF_ENDPOINT | aria2c -x$HFD_THREADS"

log(){ printf '[fetch-candidates] %s\n' "$*"; }
warn(){ printf '[fetch-candidates] WARNING: %s\n' "$*" >&2; }
retry(){ local n=1; while [ $n -le 3 ]; do "$@" && return 0; warn "attempt $n/3 failed; retry in $((n*5))s"; sleep $((n*5)); n=$((n+1)); done; warn "gave up: $*"; return 1; }

# hfd = hf-mirror's aria2c downloader (mirror-compatible, multi-connection). Auto-fetch into $DATA/.bin.
ensure_hfd(){
  command -v hfd >/dev/null 2>&1 && { command -v hfd; return; }
  local f="$DATA/.bin/hfd.sh"
  [ -f "$f" ] || { mkdir -p "$DATA/.bin"; curl -fsSL "${HF_ENDPOINT}/hfd/hfd.sh" -o "$f" 2>/dev/null && chmod +x "$f"; }
  [ -s "$f" ] && echo "$f"
}
fetch_hf(){ # id dest
  local id="$1" dest="$2"
  if command -v aria2c >/dev/null 2>&1; then
    local hfd; hfd="$(ensure_hfd)"
    if [ -n "$hfd" ]; then
      retry bash "$hfd" "$id" --dataset --tool aria2c -x "$HFD_THREADS" --local-dir "$dest" && return 0
      warn "$id: hfd failed; falling back to hf CLI (may not work against the mirror)"
    fi
  else
    warn "aria2c missing (needed for high-concurrency mirror download): sudo apt-get install -y aria2 — falling back to hf CLI"
  fi
  retry "$HF_CLI" download "$id" --repo-type dataset --local-dir "$dest"
}

# name | method | note      (method = hf:<id> | git:<owner/repo> | gated:<url>)
CANDS=(
  "audiocaps-qa|hf:AudioLLMs/audiocaps_qa_test|AudioCaps-QA AQA (AudioBench; VAT-KG/M3KG-RAG borrow it), 313 rows, not gated"
  "audio2tool|hf:RVtech/Audio2Tool|audio-native function-calling ~30k, 8 tiers, CC-BY-NC-4.0, not gated"
  "auditorybench-plusplus|hf:HJOK/AuditoryBenchpp|auditory-knowledge probe (text-only, ~527kB), CC-BY-4.0, not gated"
  "squtr|hf:SLLMCommunity/SQuTR|spoken-query retrieval robustness, 21.1GB(!), 6 configs, CC-BY-SA-4.0, not gated"
  "full-duplex-bench-v3|git:DanielLin94144/Full-Duplex-Bench|FDB-v3 real audio; clones repo, v3 data via Google Drive link in README"
  "mlc-slm|gated:https://www.nexdata.ai/competition/mlc-slm|MLC-SLM ~1604h, 11 langs: register + sign DUA, link emailed (no HF)"
)

LIST_ONLY=0; ARGS=()
for a in "$@"; do if [ "$a" = "--list" ]; then LIST_ONLY=1; else ARGS+=("$a"); fi; done
sel(){ [ "${#ARGS[@]}" -eq 0 ] && return 0; local n="$1"; for w in "${ARGS[@]}"; do [ "$w" = "$n" ] && return 0; done; return 1; }

command -v aria2c >/dev/null 2>&1 || warn "aria2c not found — install for fast download: sudo apt-get install -y aria2 (or: bash scripts/data/fetch-data.sh --install-deps)"

echo "== WS-D download candidates -> $DS =="
for row in "${CANDS[@]}"; do
  IFS='|' read -r name method note <<< "$row"
  sel "$name" || continue
  case "$method" in
    hf:*)    echo "  [HF   ] $name <- ${method#hf:}   ($note)";;
    git:*)   echo "  [GIT  ] $name <- github:${method#git:}   ($note)";;
    gated:*) echo "  [GATED] $name : ${method#gated:}   ($note)";;
  esac
  [ "$LIST_ONLY" -eq 1 ] && continue
  case "$method" in
    hf:*)    fetch_hf "${method#hf:}" "$DS/$name";;
    git:*)   retry git clone "https://github.com/${method#git:}" "$DS/$name" \
               && log "$name cloned; download the v3 data from the Google Drive link in $DS/$name/README (manual)";;
    gated:*) log "GATED $name: open ${method#gated:} , register + sign the DUA; the download link is emailed (cannot automate).";;
  esac
done
echo "== done =="
