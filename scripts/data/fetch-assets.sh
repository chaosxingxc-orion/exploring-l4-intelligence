#!/usr/bin/env bash
# fetch-assets.sh — configurable asset-fetch engine (Stage 1: shell-logic merge).
#
# This engine replaces the former fetch-data.sh / fetch-candidates.sh / fetch-qwen3-omni-gguf.sh /
# fetch-stage1c-priority-papers.sh / inventory.sh as five duplicated standalone scripts. Each
# subcommand's logic below is MIGRATED VERBATIM from its former script: same manifest, same target
# paths, same flags, same retry/log semantics as before. This stage only removes duplication of
# the invocation shell — SCRIPT_DIR resolution, subcommand dispatch, and the handful of env/venv
# lines that were byte-identical across two or more of the original scripts (see the "shared
# library" section below). It does NOT unify behavior that already differed between the original
# scripts (different `set` strictness, different retry counts/log prefixes, different override
# handling) — those pre-existing inconsistencies are preserved exactly and are listed in
# scripts/data/README.md.
#
# Usage:
#   bash scripts/data/fetch-assets.sh <data|candidates|qwen3-gguf|papers|inventory> [args...]
#
# The former standalone entry points still work unchanged as 2-3 line delegating shims:
#   fetch-data.sh, fetch-candidates.sh, fetch-qwen3-omni-gguf.sh,
#   fetch-stage1c-priority-papers.sh, inventory.sh
# Their documented CLI (flags, positional args, env overrides) is untouched by this merge.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# =================================================================================================
# Shared library — ONLY pieces that were byte-identical across two or more of the original scripts.
# Everything else (log/warn/retry semantics, `set` strictness, arg parsing) stayed inside each
# cmd_* function below exactly as it was, precisely because it was NOT identical between scripts.
# =================================================================================================

# fetch-data.sh and fetch-candidates.sh sourced the speechrl venv with this exact 3-line block.
_lib_activate_speechrl_venv() {
  SPEECHRL_VENV="${SPEECHRL_VENV:-$HOME/.venvs/speechrl}"
  # shellcheck disable=SC1091
  [ -f "$SPEECHRL_VENV/bin/activate" ] && { source "$SPEECHRL_VENV/bin/activate"; export PATH="$SPEECHRL_VENV/bin:$PATH"; }
}

# fetch-data.sh, fetch-candidates.sh and fetch-qwen3-omni-gguf.sh all exported these two exactly.
_lib_export_hf_mirror_env() {
  export HF_ENDPOINT="${SPEECHRL_HF_ENDPOINT:-https://hf-mirror.com}"
  export HF_HUB_DISABLE_XET="${HF_HUB_DISABLE_XET:-1}"
}

# fetch-data.sh and fetch-candidates.sh both set this exact locale/encoding line.
_lib_export_locale_env() {
  export LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONIOENCODING=utf-8 NO_COLOR=1
}

usage() {
  cat <<'USAGE'
fetch-assets.sh <subcommand> [args...]

Subcommands:
  data          the unified, lockfile-driven downloader           (was fetch-data.sh)
  candidates    WS-D survey-sourced candidate dataset downloader   (was fetch-candidates.sh)
  qwen3-gguf    Qwen3-Omni-30B-A3B-Instruct GGUF fetch             (was fetch-qwen3-omni-gguf.sh)
  papers        Stage-1C priority-paper fetch                     (was fetch-stage1c-priority-papers.sh)
  inventory     on-disk completeness audit                        (was inventory.sh)

Each subcommand's own flags/args/env-overrides are unchanged from before the merge; see
scripts/data/README.md and docs/data.md for the full reference.
USAGE
}

# --help text for `fetch-assets.sh data --help` (was: `sed -n '2,26p' "$0"` in fetch-data.sh — that
# printed this script's own header comment via its own $0; since $0 no longer points at a file
# whose lines 2-26 hold this text once merged, it is embedded verbatim here instead. Visible output
# is the same header, minus two lines of code (former $0/lines 25-26) the old sed range incidentally
# swept in.)
cmd_data_help() {
  cat <<'HELP'
# Unified, lockfile-driven downloader — the SINGLE way every team fetches the shared data & models.
#
# Source of truth: docs/datasets.lock.json (the frozen manifest: 28 datasets + 5 models + 7 ref
# repos, each with its source id and pinned revision). Any collaborator with THIS repo + the
# speechrl venv runs `bash scripts/data/fetch-data.sh` and reproduces the IDENTICAL set:
#   - HF datasets pin to the recorded commit sha (reproducible across teams)
#   - ModelScope sets track 'master'; SLURP audio comes from Zenodo 4274930
# The set is FROZEN: this script only fetches what the lockfile records — never new datasets.
# To change the set, edit the lockfile deliberately (regenerate it), then re-run.
#
#   bash scripts/data/fetch-data.sh             # fetch everything missing (skips complete assets)
#   bash scripts/data/fetch-data.sh --list      # print the manifest, fetch nothing
#   bash scripts/data/fetch-data.sh --dry-run   # print the commands, download nothing
#   bash scripts/data/fetch-data.sh meld slurp  # fetch only the named assets
#   bash scripts/data/fetch-data.sh --install-deps  # install the download deps (hf/modelscope/aria2) then exit
#
# Dependencies: needs the speechrl venv (hf + modelscope CLIs) and aria2c. If they're missing, run
# `bash scripts/env-setup.sh` (full stack) OR `bash scripts/data/fetch-data.sh --install-deps`
# (lightweight download deps only). The script preflight-checks and reports exactly what's missing.
#
# Models/datasets are NEVER committed to git (see .gitignore and docs/data.md).
set -uo pipefail

# Unified, lockfile-driven downloader — the SINGLE way every team fetches the shared data & models.
#
# Source of truth: docs/datasets.lock.json (the frozen manifest: 28 datasets + 5 models + 7 ref
# repos, each with its source id and pinned revision). Any collaborator with THIS repo + the
# speechrl venv runs `bash scripts/data/fetch-data.sh` and reproduces the IDENTICAL set:
#   - HF datasets pin to the recorded commit sha (reproducible across teams)
#   - ModelScope sets track 'master'; SLURP audio comes from Zenodo 4274930
# The set is FROZEN: this script only fetches what the lockfile records — never new datasets.
# To change the set, edit the lockfile deliberately (regenerate it), then re-run.
#
#   bash scripts/data/fetch-data.sh             # fetch everything missing (skips complete assets)
#   bash scripts/data/fetch-data.sh --list      # print the manifest, fetch nothing
#   bash scripts/data/fetch-data.sh --dry-run   # print the commands, download nothing
#   bash scripts/data/fetch-data.sh meld slurp  # fetch only the named assets
#   bash scripts/data/fetch-data.sh --install-deps  # install the download deps (hf/modelscope/aria2) then exit
#
# Dependencies: needs the speechrl venv (hf + modelscope CLIs) and aria2c. If they're missing, run
# `bash scripts/env-setup.sh` (full stack) OR `bash scripts/data/fetch-data.sh --install-deps`
# (lightweight download deps only). The script preflight-checks and reports exactly what's missing.
#
# Models/datasets are NEVER committed to git (see .gitignore and docs/data.md).
HELP
}

cmd_data() {
set -uo pipefail

WORKSPACE="${SPEECHRL_WORKSPACE:-$(cd "$SCRIPT_DIR/../.." && pwd)}"
DR="${SPEECHRL_DATA_DIR:-$WORKSPACE/speechrl-data}"
LOCK="${SPEECHRL_LOCKFILE:-$WORKSPACE/docs/datasets.lock.json}"
mkdir -p "$DR/datasets" "$DR/models" "$DR/repos" "$DR/manifests"

# venv (provides the CLIs: hf / huggingface-cli, modelscope, aria2c, git)
_lib_activate_speechrl_venv


# China-friendly mirrors by default; override via env.

_lib_export_hf_mirror_env
# NB: do NOT set TQDM_ASCII — tqdm reads it as the bar charset string ("1" -> len 1 -> div-by-zero
# in non-TTY/piped runs), which crashes both `hf` and `modelscope` downloads.
_lib_export_locale_env
MS_WORKERS="${SPEECHRL_MS_WORKERS:-16}"
HFD_THREADS="${SPEECHRL_HFD_THREADS:-8}"
# Prefer the venv's `python`; fall back to `python3` (Ubuntu often has no bare `python`).
PY="${SPEECHRL_PYTHON:-$(command -v python || command -v python3 || echo python)}"
HF_CLI="$(command -v hf || command -v huggingface-cli || echo hf)"

DRY=0; LIST=0; INSTALL=0; WANT=()
for a in "$@"; do case "$a" in
  --dry-run) DRY=1 ;; --list) LIST=1 ;; --install-deps) INSTALL=1 ;; -h|--help) cmd_data_help; exit 0 ;;
  *) WANT+=("$a") ;;
esac; done

log(){ printf '[fetch] %s\n' "$*"; }
warn(){ printf '[fetch] WARNING: %s\n' "$*" >&2; }
[ -f "$LOCK" ] || { warn "lockfile not found: $LOCK"; exit 1; }

# Emit the manifest, one record per line, fields separated by US (\x1f) so EMPTY fields are
# preserved (a whitespace IFS like tab collapses them and shifts columns):
#   kind  name  subdir  method  id  rev  url  zenodo
rows() {
  "$PY" - "$LOCK" <<'PY'
import json, sys
d = json.load(open(sys.argv[1], encoding="utf-8"))
def row(e, k):
    s = e.get("source", {}) or {}
    print("\x1f".join([e.get("kind", k), e["name"], e.get("local_subdir", ""),
        s.get("kind", "unknown"), (s.get("id") or s.get("hf_id") or ""),
        (e.get("revision") or ""), (s.get("url") or ""), (e.get("audio_zenodo_record") or "")]))
for e in d.get("models", []):
    if e.get("source"): row(e, "model")
for e in d.get("datasets", []): row(e, "dataset")
for e in d.get("ref_repos", []): row(e, "ref")
PY
}

want_match(){ [ ${#WANT[@]} -eq 0 ] && return 0; local n; for n in "${WANT[@]}"; do [ "$n" = "$1" ] && return 0; done; return 1; }
has_data(){ local d="$1"; [ -d "$d" ] && [ "$(find -L "$d" -type f ! -name '.*' 2>/dev/null | head -5 | wc -l)" -gt 3 ]; }
hf_completion_marker_matches(){
  local d="$1" rev="$2" marker="$1/.hfd/speechrl-complete-revision"
  [ -s "$marker" ] && [ "$(tr -d '\r\n' < "$marker")" = "$rev" ]
}
hfd_manifest_complete(){
  local d="$1" manifest="$1/.hfd/manifest" size relative
  [ -s "$manifest" ] || return 1
  while IFS=$'\t' read -r size relative; do
    [ -n "$size" ] && [ -n "$relative" ] && [ -f "$d/$relative" ] || return 1
  done < "$manifest"
}
mark_hf_complete(){
  local d="$1" rev="$2"
  hfd_manifest_complete "$d" || { warn "HF manifest is incomplete; refusing completion marker: $d"; return 1; }
  mkdir -p "$d/.hfd"
  printf '%s\n' "$rev" > "$d/.hfd/speechrl-complete-revision"
}
is_sha(){ printf '%s' "$1" | grep -Eq '^[0-9a-f]{7,40}$'; }
retry(){ local n=1; while [ $n -le 3 ]; do "$@" && return 0; warn "attempt $n/3 failed; retry in $((n*5))s"; sleep $((n*5)); n=$((n+1)); done; warn "gave up: $*"; return 1; }

# --- dependency channel: ensure the download CLIs exist; offer a lightweight install ----------
py_has(){ "$PY" -c "import $1" >/dev/null 2>&1; }
install_deps(){
  log "installing data-download dependencies (lightweight; no torch needed)"
  # 1) ensure a venv: use the active one, else create $SPEECHRL_VENV with uv (idempotent;
  #    env-setup.sh later adds the training stack to the same venv).
  if [ -z "${VIRTUAL_ENV:-}" ] && command -v uv >/dev/null 2>&1; then
    log "creating/using venv at $SPEECHRL_VENV (uv)"
    uv venv "$SPEECHRL_VENV" --python 3.12 >/dev/null 2>&1 || uv venv "$SPEECHRL_VENV" >/dev/null 2>&1 || true
    # shellcheck disable=SC1091
    [ -f "$SPEECHRL_VENV/bin/activate" ] && { source "$SPEECHRL_VENV/bin/activate"; export PATH="$SPEECHRL_VENV/bin:$PATH"; }
  fi
  # 2) install the download CLIs (into the venv if we have one; else system pip with a
  #    PEP 668 fallback for externally-managed Pythons like Ubuntu 24.04).
  local pkgs=(huggingface_hub hf_transfer modelscope)  # hf CLI ships in base hf-hub; hf_transfer is a separate pkg
  if [ -n "${VIRTUAL_ENV:-}" ] && command -v uv >/dev/null 2>&1; then
    uv pip install -U "${pkgs[@]}" || warn "uv pip install failed"
  elif [ -n "${VIRTUAL_ENV:-}" ]; then
    pip install -U "${pkgs[@]}" || warn "pip install failed"
  else
    pip install -U "${pkgs[@]}" 2>/dev/null \
      || pip install --break-system-packages -U "${pkgs[@]}" \
      || "$PY" -m pip install --break-system-packages -U "${pkgs[@]}" \
      || warn "pip install failed — run: bash scripts/env-setup.sh"
  fi
  # 3) aria2c + jq (system pkgs): aria2c powers hfd (HF) and SLURP audio; jq speeds up hfd JSON parsing
  local need=(); command -v aria2c >/dev/null 2>&1 || need+=(aria2); command -v jq >/dev/null 2>&1 || need+=(jq)
  if [ ${#need[@]} -gt 0 ]; then
    if command -v apt-get >/dev/null 2>&1; then
      sudo apt-get update && sudo apt-get install -y "${need[@]}" || warn "apt install ${need[*]} failed (HF/SLURP downloads will be slower or use a fallback)"
    else warn "install ${need[*]} manually (e.g. 'sudo apt-get install -y ${need[*]}')"; fi
  fi
  log "dependency install attempted. Activate the venv: source ${SPEECHRL_VENV}/bin/activate ; then re-run to fetch."
}
check_deps(){
  local miss=()
  command -v "$PY" >/dev/null 2>&1 || miss+=("python3")
  command -v git  >/dev/null 2>&1 || miss+=("git")
  command -v curl >/dev/null 2>&1 || miss+=("curl")
  { command -v modelscope >/dev/null 2>&1 || py_has modelscope; } || miss+=("modelscope")
  # HF datasets download via hfd+aria2c (the hf CLI is only a fallback and is incompatible with hf-mirror).
  command -v aria2c >/dev/null 2>&1 || warn "aria2c missing — required for HF datasets (hfd) + SLURP audio: sudo apt-get install -y aria2"
  command -v jq >/dev/null 2>&1 || warn "jq missing — hfd will parse JSON more slowly (optional): sudo apt-get install -y jq"
  if [ ${#miss[@]} -gt 0 ]; then
    warn "missing dependencies: ${miss[*]}"
    warn "install with ONE of:"
    warn "  bash scripts/data/fetch-data.sh --install-deps   # lightweight download deps only"
    warn "  bash scripts/env-setup.sh                        # full stack (torch/verl/...), creates the venv"
    return 1
  fi
}

# hfd = hf-mirror's aria2c downloader. It fetches resolve URLs directly (like curl/aria2c), so it
# works with hf-mirror, whereas the python `hf` CLI rejects the mirror's HEAD metadata
# (FileMetadataError). Auto-fetch hfd.sh into the data dir if not already on PATH.
ensure_hfd(){
  command -v hfd >/dev/null 2>&1 && { command -v hfd; return; }
  local f="$DR/.bin/hfd.sh"
  [ -f "$f" ] || { mkdir -p "$DR/.bin"; curl -fsSL "${HF_ENDPOINT}/hfd/hfd.sh" -o "$f" 2>/dev/null && chmod +x "$f"; }
  [ -s "$f" ] && echo "$f"
}
fetch_hf(){ # id dest rev repotype
  local id="$1" dest="$2" rev="$3" rt="$4"
  if [ "$DRY" = 1 ]; then
    echo "  DRY> hfd $id $([ "$rt" = dataset ] && echo --dataset) --tool aria2c -x $HFD_THREADS --local-dir $dest $(is_sha "$rev" && echo "--revision $rev")  (HF_ENDPOINT=$HF_ENDPOINT)"
    return 0
  fi
  # Prefer hfd+aria2c (mirror-compatible); fall back to the hf CLI (works against huggingface.co direct).
  if command -v aria2c >/dev/null 2>&1; then
    local hfd; hfd="$(ensure_hfd)"
    if [ -n "$hfd" ]; then
      local a=("$id" --tool aria2c -x "$HFD_THREADS" --local-dir "$dest"); [ "$rt" = dataset ] && a+=(--dataset)
      is_sha "$rev" && a+=(--revision "$rev")
      retry bash "$hfd" "${a[@]}" && return 0
      warn "$id: hfd failed; falling back to the hf CLI"
    fi
  fi
  local c=(download "$id" --repo-type "$rt" --local-dir "$dest"); is_sha "$rev" && c+=(--revision "$rev")
  retry "$HF_CLI" "${c[@]}"
}
fetch_ms(){ # id dest dataset|model
  local id="$1" dest="$2" rt="$3" flag=--dataset; [ "$rt" = model ] && flag=--model
  if [ "$DRY" = 1 ]; then echo "  DRY> modelscope download $flag $id --local_dir $dest"; return 0; fi
  retry modelscope download --max-workers "$MS_WORKERS" "$flag" "$id" --local_dir "$dest"
}
fetch_git(){ # url rev dest
  local url="$1" rev="$2" dest="$3"
  if [ "$DRY" = 1 ]; then echo "  DRY> git clone $url $dest ; checkout ${rev:0:12}"; return 0; fi
  [ -d "$dest/.git" ] || retry git clone "$url" "$dest"
  is_sha "$rev" && { git -C "$dest" checkout -q "$rev" 2>/dev/null || warn "checkout $rev failed in $dest"; }
}
fetch_slurp(){ # url rev audiodest
  local url="$1" rev="$2" audio="$3" repo="$DR/repos/slurp" man="$DR/manifests/slurp.links.txt"
  if [ "$DRY" = 1 ]; then echo "  DRY> git clone $url repos/slurp@${rev:0:12} ; aria2c Zenodo 4274930 -> $audio"; return 0; fi
  fetch_git "$url" "$rev" "$repo"
  mkdir -p "$audio"
  if [ ! -s "$man" ]; then
    curl -L -sS -m 30 "https://raw.githubusercontent.com/pswietojanski/slurp/master/scripts/download_audio.sh" \
      | grep -Eo 'https://[^[:space:]\\]+' | grep -E 'zenodo\.org/.*/files/.*\.tar\.gz' | sort -u >"$man.tmp" && mv "$man.tmp" "$man"
  fi
  if command -v aria2c >/dev/null 2>&1 && [ -s "$man" ]; then
    aria2c -x16 -s16 -j4 -c --auto-file-renaming=false --allow-overwrite=false --dir="$audio" \
      --input-file="$man" --console-log-level=warn || warn "slurp aria2c returned non-zero"
    for tgz in "$audio"/*.tar.gz; do [ -f "$tgz" ] || continue; [ -f "$tgz.extracted" ] || { tar -xzf "$tgz" -C "$audio" && touch "$tgz.extracted"; }; done
  else warn "aria2c or manifest missing; run repos/slurp/scripts/download_audio.sh manually"; fi
  ln -sfn "$audio" "$DR/datasets/slurp" 2>/dev/null || true
}

if [ "$INSTALL" = 1 ]; then install_deps; exit 0; fi

if [ "$LIST" = 1 ]; then
  printf '%-22s %-8s %-18s %s\n' NAME KIND METHOD SOURCE
  rows | while IFS=$'\x1f' read -r kind name subdir method id rev url zen; do
    printf '%-22s %-8s %-18s %s\n' "$name" "$kind" "$method" "${id:-$url}"
  done
  exit 0
fi

# preflight: make sure the download tools exist (skip for --dry-run, which calls nothing)
[ "$DRY" = 1 ] || check_deps || exit 1

COUNT=0; SKIP=0; FAIL=0
while IFS=$'\x1f' read -r kind name subdir method id rev url zen; do
  want_match "$name" || continue
  dest="$DR/$subdir"
  # skip-existing
  if [ "$name" = slurp ] && [ "$kind" = dataset ]; then
    if [ -d "$dest/slurp_real" ] || [ -d "$dest/slurp_synth" ]; then
      log "skip complete: slurp"; SKIP=$((SKIP+1)); ln -sfn "$dest" "$DR/datasets/slurp" 2>/dev/null || true; continue
    fi
  elif [ "$method" = git ]; then
    [ -d "$dest/.git" ] && { log "skip complete: $name"; SKIP=$((SKIP+1)); continue; }
  elif [ "$method" = hf ]; then
    hf_completion_marker_matches "$dest" "$rev" && { log "skip pinned complete: $name"; SKIP=$((SKIP+1)); continue; }
  else
    has_data "$dest" && { log "skip complete: $name"; SKIP=$((SKIP+1)); continue; }
  fi
  log "fetch $name  [$method ${id:-$url}]  -> $subdir"
  rt=dataset; [ "$kind" = model ] && rt=model
  case "$method" in
    hf)                 fetch_hf "$id" "$dest" "$rev" "$rt" && mark_hf_complete "$dest" "$rev" && COUNT=$((COUNT+1)) || FAIL=$((FAIL+1)) ;;
    modelscope)         fetch_ms "$id" "$dest" "$rt"         && COUNT=$((COUNT+1)) || FAIL=$((FAIL+1)) ;;
    modelscope-manual)  warn "$name: optional evalscope set, id not recorded — fetch manually (skipping)" ;;
    hf-manual)          warn "$name: file-selective GGUF — run scripts/data/fetch-qwen3-omni-gguf.sh (whole-repo pull deliberately avoided; skipping)" ;;
    git)                if [ "$name" = slurp ] && [ "$kind" = dataset ]; then fetch_slurp "$url" "$rev" "$dest"; else fetch_git "$url" "$rev" "$dest"; fi \
                          && COUNT=$((COUNT+1)) || FAIL=$((FAIL+1)) ;;
    *)                  warn "$name: unknown method '$method'; skipping" ;;
  esac
done < <(rows)

log "done. fetched=$COUNT skipped=$SKIP failed=$FAIL   (manifest: $LOCK)"
[ "$FAIL" = 0 ]
}

cmd_candidates() {
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

REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
DATA="${SPEECHRL_DATA_DIR:-$REPO_ROOT/speechrl-data}"
DS="$DATA/datasets"

# venv + China-friendly mirror + high concurrency — mirrors fetch-data.sh exactly
_lib_activate_speechrl_venv
_lib_export_hf_mirror_env
# HF_TOKEN for authenticated access (much higher rate limits); auto-detect from hf auth login
export HF_TOKEN="${SPEECHRL_HF_TOKEN:-${HF_TOKEN:-}}"
if [ -z "$HF_TOKEN" ]; then
  for token_file in "$HOME/.cache/huggingface/token" "$HOME/.huggingface/token"; do
    if [ -f "$token_file" ]; then
      export HF_TOKEN="$(cat "$token_file" 2>/dev/null)"; break
    fi
  done
fi
_lib_export_locale_env
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
    nmiss="$(grep -c '^http' "$list" 2>/dev/null || true)"
    nmiss="${nmiss:-0}"
    [ "$nmiss" -eq 0 ] && { log "$id: ✅ 100% complete"; return 0; }
    log "$id: round $round — $nmiss file(s) missing/short; fetching -j$HFD_JOBS single-connection"
    find "$dest" -name '*.aria2' -delete 2>/dev/null   # stale partials would trigger a 403-prone range resume
    ( cd "$dest" && aria2c -i "$list" -j "$HFD_JOBS" \
        --auto-file-renaming=false --allow-overwrite=true --file-allocation=none \
        --console-log-level=warn --summary-interval=20 \
        --max-tries=10 --retry-wait=3 --connect-timeout=30 --timeout=90 )
  done
  python -u "$DIFFER" "$id" "$dest" "$list" 2>/dev/null || true
  nmiss="$(grep -c '^http' "$list" 2>/dev/null || true)"
  nmiss="${nmiss:-0}"
  [ "$nmiss" -eq 0 ] && { log "$id: ✅ 100% complete"; return 0; }
  warn "$id: still $nmiss file(s) missing after $round rounds — re-run to continue"
  return 1
}

# Google Drive public-file downloads use the stable usercontent endpoint so aria2 can
# resume and split the released archive. The expected byte count is a hard integrity
# floor; a SHA-256 is recorded separately in the Stage-1C asset inventory after fetch.
fetch_gdrive(){ # id dest filename expected_bytes
  local id="$1" dest="$2" filename="$3" expected_bytes="$4"
  local output="$dest/$filename"
  local connections="${SPEECHRL_GDRIVE_CONNECTIONS:-8}"
  case "$connections" in ''|*[!0-9]*) connections=8;; esac
  [ "$connections" -lt 1 ] && connections=1
  mkdir -p "$dest"
  if [ -f "$output" ] && [ "$(stat -c %s "$output")" = "$expected_bytes" ]; then
    log "$filename: complete ($expected_bytes bytes)"
    return 0
  fi
  local url="https://drive.usercontent.google.com/download?id=${id}&export=download&confirm=t"
  if command -v aria2c >/dev/null 2>&1; then
    log "$filename: Google Drive public archive via aria2c -x$connections -s$connections"
    if aria2c "$url" -d "$dest" -o "$filename" -c \
      -x "$connections" -s "$connections" -k 1M \
      --auto-file-renaming=false --allow-overwrite=true --file-allocation=none; then
      :
    elif command -v curl >/dev/null 2>&1; then
      warn "$filename: aria2c TLS/range path failed -> curl resume fallback"
      find "$dest" -maxdepth 1 -name "${filename}.aria2" -delete 2>/dev/null || true
      retry curl -fL --retry 5 --retry-all-errors -C - -o "$output" "$url"
    else
      return 1
    fi
  elif command -v curl >/dev/null 2>&1; then
    warn "$filename: aria2c missing -> curl resume fallback"
    retry curl -fL --retry 5 --retry-all-errors -C - -o "$output" "$url"
  else
    warn "$filename: neither aria2c nor curl is available"
    return 1
  fi
  local actual_bytes
  actual_bytes="$(stat -c %s "$output" 2>/dev/null || echo 0)"
  if [ "$actual_bytes" != "$expected_bytes" ]; then
    warn "$filename: size mismatch expected=$expected_bytes actual=$actual_bytes"
    return 1
  fi
  log "$filename: complete ($actual_bytes bytes)"
}

# name | method | note
# method = hf:<id> | git:<owner/repo> | gdrive:<id>:<filename>:<bytes> | gated:<url>
CANDS=(
  "audiocaps-qa|hf:AudioLLMs/audiocaps_qa_test|AudioCaps-QA AQA (AudioBench; VAT-KG/M3KG-RAG borrow it), 313 rows, not gated"
  "audio2tool|hf:RVtech/Audio2Tool|audio-native function-calling ~30k, 8 tiers, CC-BY-NC-4.0, not gated"
  "auditorybench-plusplus|hf:HJOK/AuditoryBenchpp|auditory-knowledge probe (text-only, ~527kB), CC-BY-4.0, not gated"
  "squtr|hf:SLLMCommunity/SQuTR|spoken-query retrieval robustness, 21.1GB(!), 6 configs, CC-BY-SA-4.0, not gated"
  "voiceagentbench|hf:krutrim-ai-labs/VoiceAgentBench|exact VoiceAgentBench asset for arXiv:2510.07978, 5.83GB, Krutrim community license"
  "omni-deepsearch|hf:Kirito-Lab/Omni-DeepSearch|exact Omni-DeepSearch asset for arXiv:2605.08762, 640 rows, public"
  "ihbench|hf:bosonai/IHBench|exact IHBench asset for arXiv:2606.19595, CC-BY-4.0"
  "full-duplex-bench-v3|gdrive:1SO_4MTazWQ_jvCx0dtmpQ-t40bdd07yz:fdb_v3_data_released.zip:736136419|official Full-Duplex-Bench v3 public archive, 736136419 bytes"
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
FAILURES=0
for row in "${CANDS[@]}"; do
  IFS='|' read -r name method note <<< "$row"
  sel "$name" || continue
  case "$method" in
    hf:*)    echo "  [HF   ] $name <- ${method#hf:}   ($note)";;
    git:*)   echo "  [GIT  ] $name <- github:${method#git:}   ($note)";;
    gdrive:*) echo "  [GDRIVE] $name <- ${method#gdrive:}   ($note)";;
    gated:*) echo "  [GATED] $name : ${method#gated:}   ($note)";;
  esac
  [ "$LIST_ONLY" -eq 1 ] && continue
  case "$method" in
    hf:*)    fetch_hf "${method#hf:}" "$DS/$name" \
               || { warn "$name: download failed"; FAILURES=$((FAILURES + 1)); };;
    git:*)   if clone_git "${method#git:}" "$DS/$name"; then
               log "$name cloned; download any separately hosted data named in $DS/$name/README"
             else
               warn "$name: clone failed"; FAILURES=$((FAILURES + 1))
             fi;;
    gdrive:*) payload="${method#gdrive:}"; id="${payload%%:*}"; payload="${payload#*:}"; \
               filename="${payload%%:*}"; expected_bytes="${payload##*:}"; \
               fetch_gdrive "$id" "$DS/$name" "$filename" "$expected_bytes" \
               || { warn "$name: download failed"; FAILURES=$((FAILURES + 1)); };;
    gated:*) log "GATED $name: open ${method#gated:} , register + sign the DUA; the download link is emailed (cannot automate).";;
  esac
done
echo "== done =="
if [ "$FAILURES" -ne 0 ]; then
  warn "$FAILURES download failure(s)"
  exit 1
fi
}

cmd_qwen3_gguf() {
# Fetch the Qwen3-Omni-30B-A3B-Instruct GGUF (weights + audio/vision mmproj) for llama.cpp.
#
# WHY a separate script (not the unified fetch-data.sh): the lockfile path fetches the WHOLE HF repo
# (Q4_K_M + Q8_0 + BF16 + all mmproj, >110 GB). For local llama.cpp we want ONE quant by file —
# so this fetches just the two files you need, via the SAME hf-mirror + aria2c mechanism — but calling
# aria2c DIRECTLY (not via hfd) so its native, byte-accurate progress is what you see. hfd estimates
# progress from on-disk block usage, which the /mnt/e NTFS mount over-reports (aria2c's multi-segment
# seek-writes pre-allocate the whole file), making the bar jump to ~100% within seconds — far faster
# than any real download. Set SPEECHRL_HFD_THREADS=1 for a single-connection sequential write if you
# also want ls/du to track real bytes (fine when your bandwidth, not the mirror, is the limit).
#
# Repo (this script) lives on the D: drive; the data root lives on the E: drive (moved 2026-07-09):
#   repo   /mnt/d/chao_workspace/exploring-l4-intelligence
#   data   /mnt/e/chao_workspace/exploring-l4-intelligence/speechrl-data   (override: SPEECHRL_DATA_DIR)
#
# Env overrides still supported for model choices and download behavior:
#   SPEECHRL_VENV         venv             (default: $HOME/.venvs/speechrl)
#   LLAMACPP_DIR          llama.cpp build  (default: $HOME/llama.cpp)
#   QWEN_OMNI_GGUF_QUANT  weight filename  (default Q8_0; set to ...-Q4_K_M.gguf for the faster/smaller one)
#   QWEN_OMNI_MMPROJ      mmproj filename  (default bf16)
#   SPEECHRL_HF_ENDPOINT  HF mirror        (default https://hf-mirror.com)
#   SPEECHRL_SKIP_GGUF_VERIFY  set to 1 to skip the sha256 verification step below
#
# Hash pin (2026-07-09, A4/N17): sha256sum of the two default-quant files as they sit on-disk at
#   /mnt/e/chao_workspace/exploring-l4-intelligence/speechrl-data/models/qwen3-omni-30b-a3b-instruct-gguf/
# on the box that produced the W1 best-of-N / p2-baseline results (previously only the FILENAME was
# pinned here — no content check, so a truncated/corrupt/silently-re-quantized re-download of the same
# name would pass unnoticed). Verification below only fires when WEIGHT/MMPROJ equal these exact
# default filenames; override QWEN_OMNI_GGUF_QUANT/QWEN_OMNI_MMPROJ to a different quant and the check
# is skipped (no pin exists for it yet) — add one the same way once you've confirmed a new file is good:
#   sha256sum "$DEST"/<file>.gguf
QWEN_OMNI_GGUF_Q8_0_SHA256="${QWEN_OMNI_GGUF_Q8_0_SHA256:-8a50e5a7d29ae6a28fea9ca45e3bb0a142e76ec07e6787a7703cd498eb08ffaa}"
QWEN_OMNI_MMPROJ_BF16_SHA256="${QWEN_OMNI_MMPROJ_BF16_SHA256:-f0dfe825fb692d426362b1ac79678fc08daa4758f7151526cad110515f122883}"
#
# Usage (inside WSL2 Ubuntu-24.04):
#   bash /mnt/d/chao_workspace/exploring-l4-intelligence/scripts/data/fetch-qwen3-omni-gguf.sh
#   QWEN_OMNI_GGUF_QUANT=Qwen3-Omni-30B-A3B-Instruct-Q4_K_M.gguf bash /mnt/d/chao_workspace/exploring-l4-intelligence/scripts/data/fetch-qwen3-omni-gguf.sh
set -uo pipefail

WORKSPACE="/mnt/d/chao_workspace/exploring-l4-intelligence"   # repo (code + scripts) — stays on the D: drive
# Data root moved to the E: drive (2026-07-09). Honor SPEECHRL_DATA_DIR like the sibling fetch scripts.
DATA_DIR="${SPEECHRL_DATA_DIR:-/mnt/e/chao_workspace/exploring-l4-intelligence/speechrl-data}"

REPO="ggml-org/Qwen3-Omni-30B-A3B-Instruct-GGUF"
WEIGHT="${QWEN_OMNI_GGUF_QUANT:-Qwen3-Omni-30B-A3B-Instruct-Q8_0.gguf}"
MMPROJ="${QWEN_OMNI_MMPROJ:-mmproj-Qwen3-Omni-30B-A3B-Instruct-bf16.gguf}"
THREADS="${SPEECHRL_HFD_THREADS:-8}"

SPEECHRL_VENV="${SPEECHRL_VENV:-$HOME/.venvs/speechrl}"
DEST="$DATA_DIR/models/qwen3-omni-30b-a3b-instruct-gguf"
LLAMACPP_DIR="${LLAMACPP_DIR:-$HOME/llama.cpp}"
mkdir -p "$DEST"

_lib_export_hf_mirror_env
# shellcheck disable=SC1091
[ -f "$SPEECHRL_VENV/bin/activate" ] && source "$SPEECHRL_VENV/bin/activate"

log(){ printf '[fetch-gguf] %s\n' "$*"; }
log "workspace = $WORKSPACE"
log "repo      = $REPO   (HF_ENDPOINT=$HF_ENDPOINT)"
log "files     = $WEIGHT , $MMPROJ"
log "dest      = $DEST"

dl_one(){ # filename
  local f="$1" url
  # A leftover .aria2 control file means the previous run was incomplete — never treat it as present.
  # (On the NTFS mount the file reaches full size within seconds via pre-allocation, so a size-only
  # check would wrongly skip an unfinished download and leave you with a corrupt file.)
  if [ -s "$DEST/$f" ] && [ ! -e "$DEST/$f.aria2" ]; then log "already present: $f"; return 0; fi
  log "downloading $f ..."
  url="$HF_ENDPOINT/$REPO/resolve/main/$f"
  if command -v aria2c >/dev/null 2>&1; then
    # Direct aria2c (the same resolve URL hfd uses internally) so aria2c's OWN progress readout —
    # which counts real received bytes — is what prints; honest even on /mnt/e NTFS. -c resumes a
    # partial; --file-allocation=none skips an explicit upfront 30 GB allocation.
    aria2c -c -x "$THREADS" -s "$THREADS" -k 1M \
      --file-allocation=none --auto-file-renaming=false \
      --console-log-level=warn --summary-interval=1 \
      -d "$DEST" -o "$f" "$url" && return 0
    log "aria2c failed for $f; falling back to hf CLI"
  fi
  hf download "$REPO" "$f" --local-dir "$DEST"
}

verify_one(){ # filename expected_sha256
  local f="$1" expected="$2" actual
  [ -n "$expected" ] || { log "no pinned hash for $f (non-default quant/mmproj) — skipping verify"; return 0; }
  [ "${SPEECHRL_SKIP_GGUF_VERIFY:-0}" = "1" ] && { log "SPEECHRL_SKIP_GGUF_VERIFY=1 — skipping verify for $f"; return 0; }
  [ -s "$DEST/$f" ] || { log "cannot verify $f: file missing"; return 1; }
  log "verifying sha256 of $f (this reads the whole file — can take a few minutes for Q8_0) ..."
  actual="$(sha256sum "$DEST/$f" | cut -d' ' -f1)"
  if [ "$actual" = "$expected" ]; then
    log "sha256 OK: $f"
    return 0
  fi
  log "sha256 MISMATCH for $f: expected $expected, got $actual — file is corrupt/truncated/different; re-download it"
  return 1
}

rc=0
dl_one "$WEIGHT" || rc=1
dl_one "$MMPROJ" || rc=1

# Only the two default-quant filenames have a pinned hash (see header comment); anything else
# (QWEN_OMNI_GGUF_QUANT/QWEN_OMNI_MMPROJ overridden) is fetched but not hash-verified here.
[ "$WEIGHT" = "Qwen3-Omni-30B-A3B-Instruct-Q8_0.gguf" ] \
  && { verify_one "$WEIGHT" "$QWEN_OMNI_GGUF_Q8_0_SHA256" || rc=1; }
[ "$MMPROJ" = "mmproj-Qwen3-Omni-30B-A3B-Instruct-bf16.gguf" ] \
  && { verify_one "$MMPROJ" "$QWEN_OMNI_MMPROJ_BF16_SHA256" || rc=1; }

log "done (rc=$rc). files in $DEST:"
ls -lh "$DEST"/*.gguf 2>/dev/null || true
cat <<EOF

Next (after download): run on the 24 GB laptop with expert offload —
  "$LLAMACPP_DIR/build/bin/llama-mtmd-cli" \
    -m  "$DEST/$WEIGHT" \
    --mmproj "$DEST/$MMPROJ" \
    -ngl 99 --n-cpu-moe 24 --cache-type-k q8_0 --cache-type-v q8_0 -c 4096 \
    --audio /path/to/your.wav -p "Transcribe the English speech. Output only the transcript."
(Q8_0 = 32.5G > 24G VRAM, so --n-cpu-moe offloads experts to RAM; lower the number if VRAM allows, raise it if OOM.)
EOF
[ "$rc" = 0 ]
}

cmd_papers() {
set -euo pipefail

# Exact-ID Stage-1C paper acquisition. Full texts stay outside Git.
DATA_ROOT="${SPEECHRL_DATA_DIR:-/mnt/e/chao_workspace/exploring-l4-intelligence/speechrl-data}"

ASSETS=(
  "2026.findings-eacl.151|pdf|https://aclanthology.org/2026.findings-eacl.151.pdf|da6a78305f6f62dcf38a88b4f2d3a9be93001c3d5591ee621dae6463cffc153c"
  "2026.acl-long.1615|pdf|https://aclanthology.org/2026.acl-long.1615.pdf|081805a63ca2ef8fa04b1378d6aa2cda86b904d3cf9ccd5f0d496593df86a6b1"
  "2508.18240|pdf|https://arxiv.org/pdf/2508.18240|e5f0b89106fc1471cb0cd96e3c0a5d93067eb4a857558484b74bd1b9231b3e95"
  "2508.18240|eprint|https://arxiv.org/e-print/2508.18240|b1b7446ab39129154a027d92c8238be359ad0941bdae9af466576117c01ad7c7"
  "2603.16924|pdf|https://arxiv.org/pdf/2603.16924|66421173cd988f1e83c49a395cbb37ec186b779c30171976c566e698c2c0480b"
  "2603.16924|eprint|https://arxiv.org/e-print/2603.16924|157982078e822089cd7c5f279b0dbd1cd9038df3f38ff9de053bbb3297db53fd"
)

if [[ "${1:-}" == "--list" ]]; then
  printf '%s\n' "${ASSETS[@]}"
  exit 0
fi

for row in "${ASSETS[@]}"; do
  IFS='|' read -r identity kind url expected_sha <<<"$row"
  destination_dir="$DATA_ROOT/survey-fulltext/$identity"
  destination="$destination_dir/$identity.$kind"
  mkdir -p "$destination_dir"

  if [[ -s "$destination" ]]; then
    actual_sha="$(sha256sum "$destination" | awk '{print $1}')"
    if [[ "$actual_sha" == "$expected_sha" ]]; then
      printf '[SKIP] %s %s hash verified\n' "$identity" "$kind"
      continue
    fi
    printf '[FAIL] existing file hash mismatch: %s\n' "$destination" >&2
    exit 1
  fi

  temporary="$destination.part.$$"
  if command -v aria2c >/dev/null 2>&1; then
    aria2c -x 8 -s 8 --file-allocation=none --allow-overwrite=true \
      --dir="$destination_dir" --out="$(basename "$temporary")" "$url"
  else
    curl -L --fail --silent --show-error --max-time 300 -o "$temporary" "$url"
  fi

  actual_sha="$(sha256sum "$temporary" | awk '{print $1}')"
  if [[ "$actual_sha" != "$expected_sha" ]]; then
    rm -f -- "$temporary"
    printf '[FAIL] downloaded hash mismatch: %s %s\n' "$identity" "$kind" >&2
    exit 1
  fi
  mv -- "$temporary" "$destination"
  printf '[OK] %s %s\n' "$identity" "$kind"
done
}

cmd_inventory() {
# Inventory: detect partial/complete downloads via expected-payload heuristics.
# Reports per asset: size | files | status (COMPLETE|PARTIAL|MISSING|UNKNOWN).
# Paths derive from this script's location; override with SPEECHRL_DATA_DIR / SPEECHRL_VENV.
WORKSPACE="${SPEECHRL_WORKSPACE:-$(cd "$SCRIPT_DIR/../.." && pwd)}"
DR="${SPEECHRL_DATA_DIR:-$WORKSPACE/speechrl-data}"
SPEECHRL_VENV="${SPEECHRL_VENV:-$HOME/.venvs/speechrl}"

echo '=== Top-level sizes ==='
du -sh "$DR"/* 2>/dev/null

# Function: check dataset completeness via heuristic per-dataset
# Reports: name | size | files | status (COMPLETE|PARTIAL|MISSING|UNKNOWN)
check_ds() {
  local name="$1"
  local expect_min_files="$2"   # min file count for completeness
  local expect_min_size_mb="$3" # min size in MB for completeness
  local rel="${4:-datasets/$name}"  # optional explicit subpath under the data root (e.g. SLURP audio in repos/)
  local d="$DR/$rel"
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
echo '=== Models (5 locked; see datasets.lock.json) ==='
# Min-MB heuristics: very loose lower bound for "looks complete"
check_model qwen3-omni-30b-a3b-instruct 8000   # INT4 ~24G
check_model moss-audio-8b-instruct       8000  # ~17G
check_model nemotron3-nano-omni-nvfp4    8000  # NVFP4 ~21G
check_model minicpm-o-4_5                4000   # ~19G
check_model omni-embed-nemotron-3b       6000  # W4 omni embedding ~8.8G

echo
echo '=== Datasets (28 locked; heuristic completeness vs datasets.lock.json) ==='
# Loose floor; tweak if needed.  Deleted placeholders/partials (voxceleb, cvss,
# speech-commands, minds14-xtreme_s) are intentionally absent.
# content / ST
check_ds librispeech         50 10000     # 100h+360h+960h
check_ds fleurs-r            20  2000     # FLEURS-R (restored)
check_ds covost2             3    50
# speaker + emotion
check_ds crema-d            10   100
check_ds meld               10   500
# language + intent (SLU); SLURP audio lives under repos/, not datasets/
check_ds speech-massive     10  2000
check_ds slurp               5  2000  repos/slurp/scripts/audio
check_ds minds14             5   100
# audio understanding / reasoning / benchmark
check_ds air-bench          10   500
check_ds mmar                5   100
check_ds mmau-mini           5   100
check_ds mmsu                5   100
check_ds big-bench-audio    10   100
# spoken QA / dialogue / assistant / agent
check_ds heysquad            5  2000
check_ds uro-bench           5  2000
check_ds voicebench          5  2000
check_ds voiceassistant-eval 5  2000
check_ds audiomc             3   500
check_ds vocalbench          5   500
check_ds vocalbench-zh       5   500
check_ds spoken-squad        5   500
check_ds soulx-duplug        3   100
check_ds tau2-bench          3    10
check_ds eva-bench           1     0
# tts / reasoning evals
check_ds seed-tts-eval       3   100
check_ds aime24              1     0
check_ds aime25              1     0
check_ds aime26              1     0

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
}

# =================================================================================================
# Dispatcher
# =================================================================================================
case "${1:-}" in
  data)         shift; cmd_data "$@" ;;
  candidates)   shift; cmd_candidates "$@" ;;
  qwen3-gguf)   shift; cmd_qwen3_gguf "$@" ;;
  papers)       shift; cmd_papers "$@" ;;
  inventory)    shift; cmd_inventory "$@" ;;
  -h|--help|"") usage; exit 0 ;;
  *)            echo "fetch-assets: unknown subcommand '$1'" >&2; usage >&2; exit 2 ;;
esac
