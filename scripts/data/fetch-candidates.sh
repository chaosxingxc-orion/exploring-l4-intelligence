#!/usr/bin/env bash
# fetch-candidates.sh — download the WS-D survey-sourced candidate datasets (docs/datasets.candidates.json).
#
# Xet-safe, verifiable HF download via hf-mirror.com. Many HF repos now live on the **Xet** backend,
# whose presigned CDN URLs are byte-range-locked -> aria2c multi-connection range-splitting gets HTTP
# 403 on nearly every chunk (this silently left datasets ~half-downloaded). So each file is fetched
# with ONE connection (no range split) and throughput comes from file-level parallelism (aria2c -j).
# The exact gap set is computed by diffing the repo's file list+sizes (via hf_complete.py) against
# local disk, then re-verified byte-for-byte after download -> provable 100% completeness. The python
# `hf` CLI is a single-stream fallback only. Sources web-verified 2026-07-07.
#
#   bash scripts/data/fetch-candidates.sh --list        # list only, fetch nothing
#   bash scripts/data/fetch-candidates.sh               # fetch all HF + git; gated ones print instructions
#   bash scripts/data/fetch-candidates.sh squtr ...     # fetch only the named dataset(s)
#
# Env overrides: SPEECHRL_DATA_DIR, SPEECHRL_HF_ENDPOINT (default hf-mirror.com), SPEECHRL_HFD_JOBS (16
#   = concurrent files). Deps: aria2c + python huggingface_hub for HF; git for github.
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
# HF_TOKEN for authenticated access (much higher rate limits); auto-detect from hf auth login
export HF_TOKEN="${SPEECHRL_HF_TOKEN:-${HF_TOKEN:-}}"
if [ -z "$HF_TOKEN" ]; then
  for token_file in "$HOME/.cache/huggingface/token" "$HOME/.huggingface/token"; do
    if [ -f "$token_file" ]; then
      export HF_TOKEN="$(cat "$token_file" 2>/dev/null)"; break
    fi
  done
fi
export LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONIOENCODING=utf-8 NO_COLOR=1
HFD_JOBS="${SPEECHRL_HFD_JOBS:-16}"   # concurrent files (each fetched single-connection -> Xet-safe)
case "$HFD_JOBS" in ''|*[!0-9]*) HFD_JOBS=16;; esac
[ "$HFD_JOBS" -lt 1 ] && HFD_JOBS=1
DIFFER="$SCRIPT_DIR/hf_complete.py"   # repo-vs-local differ that emits a single-connection aria2c list
HF_CLI="$(command -v hf || command -v huggingface-cli || true)"
# If no CLI found, try python -m huggingface_hub as last resort
if [ -z "$HF_CLI" ]; then
  if python -c "import huggingface_hub" 2>/dev/null; then
    HF_CLI="python -m huggingface_hub"
  else
    HF_CLI="hf"
  fi
fi
mkdir -p "$DS"
echo "[fetch-candidates] data=$DS | HF_ENDPOINT=$HF_ENDPOINT | aria2c -j$HFD_JOBS single-connection (Xet-safe)"

log(){ printf '[fetch-candidates] %s\n' "$*"; }
warn(){ printf '[fetch-candidates] WARNING: %s\n' "$*" >&2; }
retry(){ local n=1; while [ $n -le 5 ]; do "$@" && return 0; local w=$((n*10)); warn "attempt $n/5 failed; retry in ${w}s"; sleep "$w"; n=$((n+1)); done; warn "gave up: $*"; return 1; }

# GitHub mirror for China (env SPEECHRL_GIT_MIRROR). Tries mirrors in order, falls back to direct.
GIT_MIRRORS=(
  "${SPEECHRL_GIT_MIRROR:-https://gitclone.com/github.com}"
  "https://ghproxy.com/https://github.com"
  "https://mirror.ghproxy.com/https://github.com"
)
clone_git(){ # owner/repo dest
  local repo="$1" dest="$2"
  local timeout="${SPEECHRL_GIT_TIMEOUT:-60}"
  if [ -d "$dest/.git" ] && git -C "$dest" rev-parse HEAD >/dev/null 2>&1; then
    log "already cloned: $repo"; return 0
  fi
  # try mirrors, then direct
  local urls=()
  for m in "${GIT_MIRRORS[@]}"; do urls+=("$m/$repo.git"); done
  urls+=("https://github.com/${repo}.git")
  for url in "${urls[@]}"; do
    rm -rf "$dest" 2>/dev/null || true
    log "trying git clone: $url (timeout=${timeout}s)"
    if timeout "$timeout" git clone --depth 1 "$url" "$dest" 2>/dev/null && \
       git -C "$dest" rev-parse HEAD >/dev/null 2>&1; then
      log "cloned ok: $repo"
      return 0
    fi
    local rc=$?
    [ $rc -eq 124 ] && warn "timed out after ${timeout}s: $url" || warn "failed (rc=$rc): $url"
  done
  rm -rf "$dest" 2>/dev/null || true
  return 1
}

fetch_hf(){ # id dest
  local id="$1" dest="$2"
  mkdir -p "$dest/.hfd"
  [ -n "${HF_TOKEN:-}" ] && log "$id: using HF_TOKEN (authenticated, higher rate limits)"

  # No aria2c or no differ -> single-stream hf CLI fallback (Xet-safe: whole-file, no range split).
  if ! command -v aria2c >/dev/null 2>&1 || [ ! -f "$DIFFER" ]; then
    warn "$id: aria2c or hf_complete.py missing -> hf CLI fallback (single-stream, slow)"
    retry "$HF_CLI" download "$id" --repo-type dataset --local-dir "$dest" --resume-download
    return
  fi

  # Xet-safe, verifiable: diff -> fetch gaps single-connection -> re-diff, up to 4 rounds (self-heal).
  local list="$dest/.hfd/missing_xetsafe.txt" round=0 nmiss=1
  while [ "$round" -lt 4 ]; do
    round=$((round + 1))
    python -u "$DIFFER" "$id" "$dest" "$list" || { warn "$id: repo listing failed (bad id? gated?)"; return 1; }
    nmiss="$(grep -c '^http' "$list" 2>/dev/null || echo 0)"
    [ "$nmiss" -eq 0 ] && { log "$id: ✅ 100% complete"; return 0; }
    log "$id: round $round — $nmiss file(s) missing/short; fetching -j$HFD_JOBS single-connection"
    find "$dest" -name '*.aria2' -delete 2>/dev/null   # stale partials would trigger a 403-prone range resume
    ( cd "$dest" && aria2c -i "$list" -j "$HFD_JOBS" \
        --auto-file-renaming=false --allow-overwrite=true --file-allocation=none \
        --console-log-level=warn --summary-interval=20 \
        --max-tries=10 --retry-wait=3 --connect-timeout=30 --timeout=90 )
  done
  python -u "$DIFFER" "$id" "$dest" "$list" 2>/dev/null || true
  nmiss="$(grep -c '^http' "$list" 2>/dev/null || echo 0)"
  [ "$nmiss" -eq 0 ] && { log "$id: ✅ 100% complete"; return 0; }
  warn "$id: still $nmiss file(s) missing after $round rounds — re-run to continue"
  return 1
}

# name | method | note      (method = hf:<id> | git:<owner/repo> | gated:<url>)
CANDS=(
  "audiocaps-qa|hf:AudioLLMs/audiocaps_qa_test|AudioCaps-QA AQA (AudioBench; VAT-KG/M3KG-RAG borrow it), 313 rows, not gated"
  "audio2tool|hf:RVtech/Audio2Tool|audio-native function-calling ~30k, 8 tiers, CC-BY-NC-4.0, not gated"
  "auditorybench-plusplus|hf:HJOK/AuditoryBenchpp|auditory-knowledge probe (text-only, ~527kB), CC-BY-4.0, not gated"
  "squtr|hf:SLLMCommunity/SQuTR|spoken-query retrieval robustness, 21.1GB(!), 6 configs, CC-BY-SA-4.0, not gated"
  # DROPPED 2026-07-08 (owner): full-duplex-bench-v3 (git+GoogleDrive) and mlc-slm (gated) removed from
  # the comparison set — not worth the manual-fetch friction. Local fdb-v3 clone was deleted.
)

LIST_ONLY=0; ARGS=()
for a in "$@"; do if [ "$a" = "--list" ]; then LIST_ONLY=1; else ARGS+=("$a"); fi; done
sel(){ [ "${#ARGS[@]}" -eq 0 ] && return 0; local n="$1"; for w in "${ARGS[@]}"; do [ "$w" = "$n" ] && return 0; done; return 1; }

command -v aria2c >/dev/null 2>&1 || warn "aria2c not found — install for fast download: sudo apt-get install -y aria2 (or: bash scripts/data/fetch-data.sh --install-deps)"
if [ "$HF_CLI" = "hf" ] && ! command -v hf >/dev/null 2>&1; then
  warn "huggingface-hub CLI not found; HF downloads will fail. Install it: uv pip install huggingface-hub"
fi
if [ -z "$HF_TOKEN" ]; then
  warn "HF_TOKEN not set — anonymous rate limits are very low (likely 429). Run: hf auth login"
fi

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
    git:*)   clone_git "${method#git:}" "$DS/$name" \
               && log "$name cloned; download the v3 data from the Google Drive link in $DS/$name/README (manual)";;
    gated:*) log "GATED $name: open ${method#gated:} , register + sign the DUA; the download link is emailed (cannot automate).";;
  esac
done
echo "== done =="
