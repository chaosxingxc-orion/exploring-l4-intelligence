#!/usr/bin/env bash
# fetch-candidate-datasets.sh — download the gap-analysis candidate DATASETS
# (docs/datasets.gap-candidates.json). Sibling script to fetch-candidate-models.sh, same CLI shape,
# venv/mirror env block, and manifest-reader pattern — retargeted at three sources instead of one:
#   - "openslr"  plain-HTTP file hosting (openslr.org + CN mirror openslr.magicdatatech.com).
#     aria2c MULTI-connection (-x8 -s8) is SAFE here — these are ordinary static file servers, NOT
#     the HF Xet CDN, so there is no byte-range-locked presigned URL to trip a 403 on. Completeness is
#     verified by comparing local file size against the remote Content-Length (HEAD request).
#   - "hf"       HuggingFace dataset repos. Reuses the Xet-safe single-connection machinery from
#     fetch-candidate-models.sh (see the warning above fetch_hf_dataset below) — datasets need the
#     WHOLE repo tree, so unlike the models script there is no include_patterns post-filter.
#   - "manual"   no automatable source (e.g. Baidu Cloud pan links behind a share code). The script
#     prints the id_or_url + notes as instructions and counts the item as SKIPPED, never FAILED.
#
#   bash scripts/data/fetch-candidate-datasets.sh --list                       # table, all priorities, fetch nothing
#   bash scripts/data/fetch-candidate-datasets.sh                              # fetch priority P1 only (default)
#   bash scripts/data/fetch-candidate-datasets.sh --priority P2                # fetch P2 only
#   bash scripts/data/fetch-candidate-datasets.sh --priority all               # fetch every priority (heavy! ~120GB+)
#   bash scripts/data/fetch-candidate-datasets.sh --only aishell-1             # fetch one named item (any priority)
#   bash scripts/data/fetch-candidate-datasets.sh --only thchs-30 --file resource.tgz
#                                                                              # fetch just ONE archive of an
#                                                                              # openslr item (connectivity probe /
#                                                                              # retry a single failed file)
#   bash scripts/data/fetch-candidate-datasets.sh --install-deps              # print how to install deps
#
# Env overrides: SPEECHRL_DATA_DIR (data root), SPEECHRL_GAP_DATASETS_MANIFEST (manifest path),
#   SPEECHRL_HF_ENDPOINT (default hf-mirror.com), SPEECHRL_HFD_JOBS (default 16 = concurrent HF files),
#   SPEECHRL_OPENSLR_MIRROR (cn|primary|auto, default auto = try cn_mirror first, fall back to
#   primary on failure). Deps: aria2c + curl for openslr; aria2c + python huggingface_hub for HF.
# See docs/datasets.gap-candidates.json for the manifest (name/gap/source/priority/role/notes).
set -u
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
DATA="${SPEECHRL_DATA_DIR:-$REPO_ROOT/speechrl-data}"
DATASETS="$DATA/datasets"
MANIFEST="${SPEECHRL_GAP_DATASETS_MANIFEST:-$REPO_ROOT/docs/datasets.gap-candidates.json}"

# venv + China-friendly mirror + high concurrency — mirrors fetch-candidate-models.sh exactly
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
OPENSLR_MIRROR="${SPEECHRL_OPENSLR_MIRROR:-auto}"
case "$OPENSLR_MIRROR" in cn|primary|auto) ;; *) OPENSLR_MIRROR=auto;; esac
DIFFER="$SCRIPT_DIR/hf_complete.py"   # repo-vs-local differ that emits a single-connection aria2c list (unmodified)
PY="${SPEECHRL_PYTHON:-$(command -v python || command -v python3 || echo python)}"
HF_CLI="$(command -v hf || command -v huggingface-cli || true)"
if [ -z "$HF_CLI" ]; then
  if "$PY" -c "import huggingface_hub" 2>/dev/null; then HF_CLI="python -m huggingface_hub"; else HF_CLI="hf"; fi
fi
mkdir -p "$DATASETS"

log(){ printf '[fetch-candidate-datasets] %s\n' "$*"; }
warn(){ printf '[fetch-candidate-datasets] WARNING: %s\n' "$*" >&2; }
retry(){ local n=1; while [ $n -le 5 ]; do "$@" && return 0; local w=$((n*10)); warn "attempt $n/5 failed; retry in ${w}s"; sleep "$w"; n=$((n+1)); done; warn "gave up: $*"; return 1; }

# --- CLI -------------------------------------------------------------------------------------
LIST_ONLY=0; ONLY=""; PRIORITY=""; ONLY_FILE=""; INSTALL=0
while [ $# -gt 0 ]; do
  case "$1" in
    --list) LIST_ONLY=1; shift ;;
    --only) ONLY="${2:-}"; shift 2 ;;
    --priority) PRIORITY="${2:-}"; shift 2 ;;
    --file) ONLY_FILE="${2:-}"; shift 2 ;;
    --install-deps) INSTALL=1; shift ;;
    -h|--help) sed -n '2,30p' "$0"; exit 0 ;;
    *) warn "unknown arg: $1 (see --help)"; shift ;;
  esac
done
if [ "$INSTALL" -eq 1 ]; then
  log "install deps (shared across all fetch scripts): bash scripts/data/fetch-data.sh --install-deps"
  log "  (installs: huggingface_hub + hf_transfer into the venv, plus aria2c/curl via apt)"
  log "  openslr items need only curl + aria2c (no HF creds); hf items need HF_TOKEN for decent rate limits."
  exit 0
fi
# --list defaults to showing every priority; a real fetch defaults to P1 only (P2 must be asked for).
if [ -z "$PRIORITY" ]; then [ "$LIST_ONLY" -eq 1 ] && PRIORITY=all || PRIORITY=P1; fi
case "$PRIORITY" in P1|P2|all) ;; *) warn "invalid --priority '$PRIORITY' (want P1|P2|all)"; exit 1 ;; esac
priority_match(){ [ -n "$ONLY" ] && return 0; [ "$PRIORITY" = all ] && return 0; [ "$PRIORITY" = "$1" ]; }  # --only overrides priority
name_match(){ [ -z "$ONLY" ] && return 0; [ "$ONLY" = "$1" ]; }
if [ -n "$ONLY_FILE" ] && [ -z "$ONLY" ]; then
  warn "--file requires --only <name>; ignoring --file"
  ONLY_FILE=""
fi

[ -f "$MANIFEST" ] || { warn "manifest not found: $MANIFEST"; exit 1; }
command -v curl >/dev/null 2>&1 || warn "curl not found — openslr Content-Length verification + HF token auto-detect will be skipped"
command -v aria2c >/dev/null 2>&1 || warn "aria2c not found — openslr + HF single-connection fetch will fall back / fail. Install: bash scripts/data/fetch-data.sh --install-deps"
if [ "$HF_CLI" = "hf" ] && ! command -v hf >/dev/null 2>&1; then
  warn "huggingface-hub CLI not found; HF downloads will fail. Install it: uv pip install huggingface-hub"
fi
if [ -z "$HF_TOKEN" ]; then
  warn "HF_TOKEN not set — anonymous rate limits are very low (likely 429). Run: hf auth login"
fi

# --- manifest reader: JSON -> \x1f-delimited rows (mirrors fetch-candidate-models.sh's rows()) -----
# URL lists (primary/cn_mirror) are joined with \x1e (a separator that never appears in a URL) so
# per-item file counts survive the row round-trip; \x1f still separates the top-level fields.
# name \x1f gap \x1f source \x1f priority \x1f role \x1f resource \x1f repo \x1f id_or_url \x1f
#   size_bytes \x1f primary(\x1e-joined) \x1f cn_mirror(\x1e-joined) \x1f notes
rows() {
  "$PY" - "$MANIFEST" <<'PY'
import json, sys
SEP, ITEMSEP = "\x1f", "\x1e"
d = json.load(open(sys.argv[1], encoding="utf-8"))
for e in d:
    size = e.get("size_bytes_approx")
    print(SEP.join([
        e.get("name", ""),
        e.get("gap", ""),
        e.get("source", ""),
        e.get("priority", ""),
        e.get("role", ""),
        e.get("resource", "") or "",
        e.get("repo", "") or "",
        e.get("id_or_url", "") or "",
        (str(size) if size is not None else ""),
        ITEMSEP.join(e.get("primary") or []),
        ITEMSEP.join(e.get("cn_mirror") or []),
        (e.get("notes", "") or "").replace("\x1f", " ").replace("\x1e", " ").replace("\n", " "),
    ]))
PY
}

# --- completeness check: openslr (existence-only, no network -> cheap enough for --list) ----------
# A basename counts present only if the file exists AND no sibling *.aria2 partial-control file sits
# next to it (aria2 leaves that marker while a download is still in flight / was interrupted).
status_openslr() { # dest primary_csv(\x1e-joined)
  local dest="$1" primary_csv="$2"
  local IFS=$'\x1e'; local -a urls; read -ra urls <<< "$primary_csv"
  local total=0 present=0 u bn
  for u in "${urls[@]}"; do
    [ -z "$u" ] && continue
    total=$((total + 1))
    bn="$(basename "$u")"
    if [ -f "$dest/$bn" ] && [ ! -f "$dest/$bn.aria2" ]; then present=$((present + 1)); fi
  done
  if [ "$total" -eq 0 ] || [ "$present" -eq 0 ]; then echo MISSING
  elif [ "$present" -eq "$total" ]; then echo COMPLETE
  else echo PARTIAL
  fi
}

# --- completeness check: hf (existence-only proxy — no include_patterns to check against, so this
# is deliberately weaker than the models script's check_status; real verification happens on fetch
# via hf_complete.py's size-diff). Honest label: PRESENT(unverified), never claims COMPLETE. ---------
status_hf() { # dest
  local dest="$1"
  if [ -d "$dest" ] && [ -n "$(find -L "$dest" -type f ! -name '.*' 2>/dev/null | head -1)" ]; then
    echo "PRESENT(unverified)"
  else
    echo MISSING
  fi
}

status_of() { # name source dest primary_csv
  local source="$2" dest="$3" primary_csv="$4"
  case "$source" in
    openslr) status_openslr "$dest" "$primary_csv" ;;
    hf)      status_hf "$dest" ;;
    manual)  echo MANUAL ;;
    *)       echo UNKNOWN ;;
  esac
}

# --- openslr fetch: plain-HTTP file hosting -> aria2c MULTI-connection is deliberate and safe here
# (NOT the HF Xet CDN — no byte-range-locked presigned URL to trip a 403 on). Mirror order is chosen
# by SPEECHRL_OPENSLR_MIRROR (cn|primary|auto); "auto" tries cn_mirror first, falling back to primary
# on failure. After (or instead of) downloading, completeness is verified by comparing the local file
# size against the remote Content-Length (HEAD via curl -sIL); if HEAD fails (server refuses HEAD,
# network hiccup, etc.) we warn and accept aria2c's own resumable-length check as sufficient proof —
# aria2c's -c/--continue logic already refuses to report success on a truncated transfer. ------------
openslr_verify() { # path url_for_head -> 0=verified-or-accepted-complete, 1=missing/short/mismatch
  local path="$1" url="$2"
  [ -f "$path" ] || return 1
  [ -f "$path.aria2" ] && return 1   # aria2 partial-control marker -> definitely not complete
  local remote=""
  if command -v curl >/dev/null 2>&1; then
    remote="$(curl -sIL --max-time 20 "$url" 2>/dev/null | tr -d '\r' | grep -i '^content-length:' | tail -1 | awk '{print $2}')"
  fi
  if [ -z "$remote" ]; then
    warn "HEAD gave no Content-Length for $url — cannot verify size; accepting local file (no .aria2 marker) as complete"
    return 0
  fi
  local local_size; local_size="$(wc -c <"$path" 2>/dev/null | tr -d ' ')"
  if [ "$local_size" = "$remote" ]; then return 0; fi
  warn "size mismatch: $path local=${local_size:-?} remote=$remote"
  return 1
}

fetch_openslr_file() { # name url_primary url_cn dest basename
  local name="$1" url_primary="$2" url_cn="$3" dest="$4" bn="$5"
  if openslr_verify "$dest/$bn" "$url_primary"; then
    log "$name: $bn already complete (skip)"; return 0
  fi
  local -a urls=()
  case "$OPENSLR_MIRROR" in
    cn)      [ -n "$url_cn" ] && urls+=("$url_cn"); urls+=("$url_primary") ;;
    primary) urls+=("$url_primary") ;;
    auto|*)  if [ -n "$url_cn" ]; then urls+=("$url_cn" "$url_primary"); else urls+=("$url_primary"); fi ;;
  esac
  local u ok=1
  for u in "${urls[@]}"; do
    log "$name: fetching $bn <- $u  (aria2c -x8 -s8 -c, multi-connection safe: plain HTTP, not Xet)"
    if ( cd "$dest" && aria2c -x8 -s8 -c --auto-file-renaming=false --allow-overwrite=false \
          --console-log-level=warn --summary-interval=20 \
          --max-tries=10 --retry-wait=3 --connect-timeout=30 --timeout=90 \
          --out="$bn" "$u" ); then
      ok=0; break
    fi
    warn "$name: fetch of $bn failed from $u; trying next mirror if any"
  done
  [ "$ok" -eq 0 ] || { warn "$name: all mirrors failed for $bn"; return 1; }
  openslr_verify "$dest/$bn" "$url_primary" || { warn "$name: $bn incomplete after download"; return 1; }
  return 0
}

fetch_openslr_item() { # name dest primary_csv cn_mirror_csv only_file
  local name="$1" dest="$2" primary_csv="$3" cn_mirror_csv="$4" only_file="$5"
  mkdir -p "$dest"
  local IFS=$'\x1e'
  local -a prim; read -ra prim <<< "$primary_csv"
  local -a cnm; read -ra cnm <<< "$cn_mirror_csv"
  local i total=0 ok=0 bn url_p url_c
  for i in "${!prim[@]}"; do
    url_p="${prim[$i]}"
    [ -z "$url_p" ] && continue
    url_c="${cnm[$i]:-}"
    bn="$(basename "$url_p")"
    if [ -n "$only_file" ] && [ "$only_file" != "$bn" ]; then continue; fi
    total=$((total + 1))
    fetch_openslr_file "$name" "$url_p" "$url_c" "$dest" "$bn" && ok=$((ok + 1))
  done
  if [ "$total" -eq 0 ]; then
    [ -n "$only_file" ] && warn "$name: --file '$only_file' matched no archive in this item's URL list"
    return 1
  fi
  [ "$ok" -eq "$total" ]
}

# --- hf fetch: reuses the Xet-safe machinery from fetch-candidate-models.sh, but for datasets there
# is NO include_patterns filtering — a dataset needs the whole repo tree, so we act directly on
# hf_complete.py's raw missing-file list (repo_type explicitly "dataset"; the differ defaults to
# "dataset" too, but pass it explicitly for clarity since fetch-candidate-models.sh passes "model").
# XET WARNING (HF-specific, does not apply to the openslr path above): many HF repos live on the Xet
# content-addressed backend, whose presigned CDN URLs are byte-range-locked -> aria2c multi-connection
# range-splitting gets HTTP 403 on nearly every chunk. So each file is fetched with ONE connection (no
# range split) and throughput comes from file-level parallelism (aria2c -j). ------------------------
fetch_hf_dataset() { # repo dest
  local repo="$1" dest="$2"
  mkdir -p "$dest/.hfd"
  [ -n "${HF_TOKEN:-}" ] && log "$repo: using HF_TOKEN (authenticated, higher rate limits)"

  # No aria2c or no differ -> single-stream hf CLI fallback (Xet-safe: whole-file, no range split).
  if ! command -v aria2c >/dev/null 2>&1 || [ ! -f "$DIFFER" ]; then
    warn "$repo: aria2c or hf_complete.py missing -> hf CLI fallback (single-stream, slow)"
    retry "$HF_CLI" download "$repo" --repo-type dataset --local-dir "$dest"
    return
  fi

  # Xet-safe, verifiable: diff (whole repo, no filter) -> fetch gaps single-connection -> re-diff,
  # up to 4 rounds (self-heal).
  local list="$dest/.hfd/missing_xetsafe.txt" round=0 nmiss=1
  while [ "$round" -lt 4 ]; do
    round=$((round + 1))
    python -u "$DIFFER" "$repo" "$dest" "$list" dataset || { warn "$repo: repo listing failed (bad id? gated?)"; return 1; }
    # NB: grep -c prints "0" AND exits 1 on no match — an `|| echo 0` here would emit "0\n0"
    nmiss="$(grep -c '^http' "$list" 2>/dev/null)"; [ -n "$nmiss" ] || nmiss=0
    [ "$nmiss" -eq 0 ] && { log "$repo: 100% complete"; return 0; }
    log "$repo: round $round — $nmiss file(s) missing/short; fetching -j$HFD_JOBS single-connection"
    find "$dest" -name '*.aria2' -delete 2>/dev/null   # stale partials would trigger a 403-prone range resume
    ( cd "$dest" && aria2c -i "$list" -j "$HFD_JOBS" \
        --auto-file-renaming=false --allow-overwrite=true --file-allocation=none \
        --console-log-level=warn --summary-interval=20 \
        --max-tries=10 --retry-wait=3 --connect-timeout=30 --timeout=90 )
  done
  python -u "$DIFFER" "$repo" "$dest" "$list" dataset 2>/dev/null || true
  nmiss="$(grep -c '^http' "$list" 2>/dev/null)"; [ -n "$nmiss" ] || nmiss=0
  [ "$nmiss" -eq 0 ] && { log "$repo: 100% complete"; return 0; }
  warn "$repo: still $nmiss file(s) missing after $round rounds — re-run to continue"
  return 1
}

# --- manual: no automatable source (e.g. Baidu Cloud pan link behind a share code). Print
# instructions and return a distinct code so the caller counts it as SKIPPED, never FAILED. ---------
fetch_manual() { # name id_or_url dest notes
  local name="$1" id_or_url="$2" dest="$3" notes="$4"
  log "$name: MANUAL download required — no automatable source."
  log "$name: source: $id_or_url"
  [ -n "$notes" ] && log "$name: notes: $notes"
  log "$name: fetch by hand, then place the files under $dest ; re-run --list to confirm."
  return 2
}

# --- main --------------------------------------------------------------------------------------
if [ "$LIST_ONLY" -eq 1 ]; then
  echo "== gap-candidate datasets -> $DATASETS  (manifest: $MANIFEST) =="
  printf '%-24s %-4s %-9s %-4s %-13s %-20s %s\n' NAME GAP SOURCE PRI STATUS SIZE ID
  while IFS=$'\x1f' read -r name gap source priority role resource repo id_or_url size primary_csv cn_mirror_csv notes; do
    name_match "$name" || continue
    priority_match "$priority" || continue
    dest="$DATASETS/$name"
    status="$(status_of "$name" "$source" "$dest" "$primary_csv")"
    if [ -n "$size" ]; then sizemb="$(( size / 1000000 ))MB"; else sizemb="?"; fi
    id="${resource:-${repo:-$id_or_url}}"
    printf '%-24s %-4s %-9s %-4s %-13s %-20s %s\n' "$name" "$gap" "$source" "$priority" "$status" "$sizemb" "$id"
  done < <(rows)
  exit 0
fi

echo "== gap-candidate datasets -> $DATASETS  (priority=$PRIORITY${ONLY:+, only=$ONLY}${ONLY_FILE:+, file=$ONLY_FILE}) =="
COUNT=0; SKIP=0; FAIL=0
while IFS=$'\x1f' read -r name gap source priority role resource repo id_or_url size primary_csv cn_mirror_csv notes; do
  name_match "$name" || continue
  priority_match "$priority" || continue
  dest="$DATASETS/$name"
  status="$(status_of "$name" "$source" "$dest" "$primary_csv")"
  if [ "$status" = COMPLETE ] && [ -z "$ONLY_FILE" ]; then
    log "skip complete: $name"; SKIP=$((SKIP + 1)); continue
  fi
  log "fetch $name  [$source ${resource:-${repo:-$id_or_url}}]  gap=$gap priority=$priority status=$status -> datasets/$name"
  case "$source" in
    openslr) fetch_openslr_item "$name" "$dest" "$primary_csv" "$cn_mirror_csv" "$ONLY_FILE" && COUNT=$((COUNT+1)) || FAIL=$((FAIL+1)) ;;
    hf)      fetch_hf_dataset "$repo" "$dest" && COUNT=$((COUNT+1)) || FAIL=$((FAIL+1)) ;;
    manual)  fetch_manual "$name" "$id_or_url" "$dest" "$notes"; [ $? -eq 2 ] && SKIP=$((SKIP+1)) || FAIL=$((FAIL+1)) ;;
    *)       warn "$name: unknown source '$source'; skipping" ;;
  esac
done < <(rows)
log "done. fetched=$COUNT skipped=$SKIP failed=$FAIL   (manifest: $MANIFEST)"
[ "$FAIL" -eq 0 ]
