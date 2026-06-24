#!/usr/bin/env bash
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

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE="${SPEECHRL_WORKSPACE:-$(cd "$SCRIPT_DIR/../.." && pwd)}"
DR="${SPEECHRL_DATA_DIR:-$WORKSPACE/speechrl-data}"
LOCK="${SPEECHRL_LOCKFILE:-$WORKSPACE/docs/datasets.lock.json}"
mkdir -p "$DR/datasets" "$DR/models" "$DR/repos" "$DR/manifests"

# venv (provides the CLIs: hf / huggingface-cli, modelscope, aria2c, git)
SPEECHRL_VENV="${SPEECHRL_VENV:-$HOME/.venvs/speechrl}"
# shellcheck disable=SC1091
[ -f "$SPEECHRL_VENV/bin/activate" ] && { source "$SPEECHRL_VENV/bin/activate"; export PATH="$SPEECHRL_VENV/bin:$PATH"; }

# China-friendly mirrors by default; override via env.
export HF_ENDPOINT="${SPEECHRL_HF_ENDPOINT:-https://hf-mirror.com}"
export HF_HUB_DISABLE_XET="${HF_HUB_DISABLE_XET:-1}"
export LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONIOENCODING=utf-8 TQDM_ASCII=1 NO_COLOR=1
MS_WORKERS="${SPEECHRL_MS_WORKERS:-16}"
PY="${SPEECHRL_PYTHON:-python}"
HF_CLI="$(command -v hf || command -v huggingface-cli || echo hf)"

DRY=0; LIST=0; INSTALL=0; WANT=()
for a in "$@"; do case "$a" in
  --dry-run) DRY=1 ;; --list) LIST=1 ;; --install-deps) INSTALL=1 ;; -h|--help) sed -n '2,26p' "$0"; exit 0 ;;
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
is_sha(){ printf '%s' "$1" | grep -Eq '^[0-9a-f]{7,40}$'; }
retry(){ local n=1; while [ $n -le 3 ]; do "$@" && return 0; warn "attempt $n/3 failed; retry in $((n*5))s"; sleep $((n*5)); n=$((n+1)); done; warn "gave up: $*"; return 1; }

# --- dependency channel: ensure the download CLIs exist; offer a lightweight install ----------
py_has(){ "$PY" -c "import $1" >/dev/null 2>&1; }
install_deps(){
  log "installing data-download dependencies (lightweight; no torch needed)"
  if command -v uv >/dev/null 2>&1 && [ -n "${VIRTUAL_ENV:-}" ]; then
    uv pip install -U "huggingface_hub[cli,hf_transfer]" hf_transfer modelscope || warn "uv pip install failed"
  elif command -v pip >/dev/null 2>&1; then
    pip install -U "huggingface_hub[cli,hf_transfer]" hf_transfer modelscope || warn "pip install failed (no venv? run: bash scripts/env-setup.sh)"
  else
    "$PY" -m pip install -U "huggingface_hub[cli,hf_transfer]" hf_transfer modelscope || warn "pip install failed (no venv? run: bash scripts/env-setup.sh)"
  fi
  if ! command -v aria2c >/dev/null 2>&1; then
    if command -v apt-get >/dev/null 2>&1; then
      sudo apt-get update && sudo apt-get install -y aria2 || warn "aria2 install failed (SLURP audio will use a slower fallback)"
    else warn "install aria2 for fast SLURP audio (e.g. 'sudo apt-get install -y aria2')"; fi
  fi
  log "dependency install attempted; re-run without --install-deps to fetch."
}
check_deps(){
  local miss=()
  command -v git >/dev/null 2>&1 || miss+=("git")
  command -v "$PY" >/dev/null 2>&1 || miss+=("python")
  { command -v "$HF_CLI" >/dev/null 2>&1 || py_has huggingface_hub; } || miss+=("huggingface_hub/hf-cli")
  { command -v modelscope >/dev/null 2>&1 || py_has modelscope; } || miss+=("modelscope")
  command -v aria2c >/dev/null 2>&1 || warn "aria2c missing — SLURP audio will use a slower fallback ('sudo apt-get install -y aria2')"
  if [ ${#miss[@]} -gt 0 ]; then
    warn "missing dependencies: ${miss[*]}"
    warn "install with ONE of:"
    warn "  bash scripts/data/fetch-data.sh --install-deps   # lightweight download deps only"
    warn "  bash scripts/env-setup.sh                        # full stack (torch/verl/...), creates the venv"
    return 1
  fi
}

fetch_hf(){ # id dest rev repotype
  local id="$1" dest="$2" rev="$3" rt="$4"; local args=(download "$id" --repo-type "$rt" --local-dir "$dest")
  is_sha "$rev" && args+=(--revision "$rev")
  if [ "$DRY" = 1 ]; then echo "  DRY> $HF_CLI ${args[*]}  (HF_ENDPOINT=$HF_ENDPOINT)"; return 0; fi
  retry "$HF_CLI" "${args[@]}"
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
  else
    has_data "$dest" && { log "skip complete: $name"; SKIP=$((SKIP+1)); continue; }
  fi
  log "fetch $name  [$method ${id:-$url}]  -> $subdir"
  rt=dataset; [ "$kind" = model ] && rt=model
  case "$method" in
    hf)                 fetch_hf "$id" "$dest" "$rev" "$rt"  && COUNT=$((COUNT+1)) || FAIL=$((FAIL+1)) ;;
    modelscope)         fetch_ms "$id" "$dest" "$rt"         && COUNT=$((COUNT+1)) || FAIL=$((FAIL+1)) ;;
    modelscope-manual)  warn "$name: optional evalscope set, id not recorded — fetch manually (skipping)" ;;
    git)                if [ "$name" = slurp ] && [ "$kind" = dataset ]; then fetch_slurp "$url" "$rev" "$dest"; else fetch_git "$url" "$rev" "$dest"; fi \
                          && COUNT=$((COUNT+1)) || FAIL=$((FAIL+1)) ;;
    *)                  warn "$name: unknown method '$method'; skipping" ;;
  esac
done < <(rows)

log "done. fetched=$COUNT skipped=$SKIP failed=$FAIL   (manifest: $LOCK)"
[ "$FAIL" = 0 ]
