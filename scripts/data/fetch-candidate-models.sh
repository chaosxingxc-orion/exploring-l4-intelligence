#!/usr/bin/env bash
# fetch-candidate-models.sh — download the T11 survey-sourced candidate EMBEDDER models
# (docs/models.candidates.json). Sibling script to fetch-candidates.sh, same Xet-safe pattern,
# retargeted at models/ instead of datasets/.
#
# Xet-safe, verifiable HF download via hf-mirror.com. Many HF repos now live on the **Xet** backend,
# whose presigned CDN URLs are byte-range-locked -> aria2c multi-connection range-splitting gets HTTP
# 403 on nearly every chunk (this silently left assets ~half-downloaded). So each file is fetched
# with ONE connection (no range split) and throughput comes from file-level parallelism (aria2c -j).
# The exact gap set is computed by diffing the repo's file list+sizes (via hf_complete.py) against
# local disk, then re-verified byte-for-byte after download -> provable 100% completeness.
#
# KNOWN LIMITATIONS of hf_complete.py (used as-is, unmodified — see its docstring):
#   - it lists/diffs the WHOLE repo tree and hardcodes the "main" branch in every resolve URL, i.e.
#     it has NO --revision / pinning support. This script therefore documents (does not enforce) the
#     manifest's pinned revision per model: fetch is effectively at repo HEAD; re-run the differ /
#     check the HF commit history by hand if byte-for-byte reproducibility matters.
#   - it has NO include-pattern filtering. This script POST-FILTERS the raw missing-file list it
#     emits, keeping only entries whose relative path (or basename) matches one of the model's
#     include_patterns from the manifest (glob match, via a small embedded python/fnmatch filter —
#     chosen over a bash `case` because patterns are matched against both the full relative path and
#     the basename, which is fiddlier to get right in pure bash string globbing).
#
#   bash scripts/data/fetch-candidate-models.sh --list              # table, fetch nothing (all tiers)
#   bash scripts/data/fetch-candidate-models.sh                     # fetch EVERY tier (default; ~28GB total —
#                                                                   #   owner 2026-07-08: heavies in by default;
#                                                                   #   e5-omni dropped from scope same day)
#   bash scripts/data/fetch-candidate-models.sh --tier T1           # small set only (~6.3GB)
#   bash scripts/data/fetch-candidate-models.sh --tier T2           # heavy tier only
#   bash scripts/data/fetch-candidate-models.sh --only wavlm-large  # fetch one named model (any tier)
#   bash scripts/data/fetch-candidate-models.sh --install-deps      # print how to install deps
#
# Env overrides: SPEECHRL_DATA_DIR (data root), SPEECHRL_HF_ENDPOINT (default hf-mirror.com),
#   SPEECHRL_HFD_JOBS (default 16 = concurrent files), GH_MIRROR_PREFIX (prefixed onto the raw
#   github.com release-asset URL for github-release entries, e.g. a ghproxy mirror, when direct
#   GitHub is slow/blocked from CN). Deps: aria2c + python huggingface_hub for HF; modelscope CLI for
#   ModelScope; git/curl+aria2c for github-release. See docs/models.candidates.json for the manifest.
set -u
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
DATA="${SPEECHRL_DATA_DIR:-$REPO_ROOT/speechrl-data}"
MODELS="$DATA/models"
MANIFEST="${SPEECHRL_MODELS_MANIFEST:-$REPO_ROOT/docs/models.candidates.json}"

# venv + China-friendly mirror + high concurrency — mirrors fetch-candidates.sh / fetch-data.sh exactly
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
MS_WORKERS="${SPEECHRL_MS_WORKERS:-16}"
DIFFER="$SCRIPT_DIR/hf_complete.py"   # repo-vs-local differ that emits a single-connection aria2c list (unmodified)
PY="${SPEECHRL_PYTHON:-$(command -v python || command -v python3 || echo python)}"
HF_CLI="$(command -v hf || command -v huggingface-cli || true)"
if [ -z "$HF_CLI" ]; then
  if "$PY" -c "import huggingface_hub" 2>/dev/null; then HF_CLI="python -m huggingface_hub"; else HF_CLI="hf"; fi
fi
GH_MIRROR_PREFIX="${GH_MIRROR_PREFIX:-}"
mkdir -p "$MODELS"

log(){ printf '[fetch-candidate-models] %s\n' "$*"; }
warn(){ printf '[fetch-candidate-models] WARNING: %s\n' "$*" >&2; }
retry(){ local n=1; while [ $n -le 5 ]; do "$@" && return 0; local w=$((n*10)); warn "attempt $n/5 failed; retry in ${w}s"; sleep "$w"; n=$((n+1)); done; warn "gave up: $*"; return 1; }

# --- CLI -------------------------------------------------------------------------------------
LIST_ONLY=0; ONLY=""; TIER=""; INSTALL=0
while [ $# -gt 0 ]; do
  case "$1" in
    --list) LIST_ONLY=1; shift ;;
    --only) ONLY="${2:-}"; shift 2 ;;
    --tier) TIER="${2:-}"; shift 2 ;;
    --install-deps) INSTALL=1; shift ;;
    -h|--help) sed -n '2,32p' "$0"; exit 0 ;;
    *) warn "unknown arg: $1 (see --help)"; shift ;;
  esac
done
if [ "$INSTALL" -eq 1 ]; then
  log "install deps (shared across all fetch scripts): bash scripts/data/fetch-data.sh --install-deps"
  log "  (installs: huggingface_hub + hf_transfer + modelscope into the venv, plus aria2c/jq via apt)"
  exit 0
fi
# Default = ALL tiers for both --list and fetch (owner 2026-07-08: heavies in the default —
# "一次性把事情做对"). Use --tier T1 to restrict to the small set.
if [ -z "$TIER" ]; then TIER=all; fi
case "$TIER" in T1|T2|T3|all) ;; *) warn "invalid --tier '$TIER' (want T1|T2|T3|all)"; exit 1 ;; esac
tier_match(){ [ -n "$ONLY" ] && return 0; [ "$TIER" = all ] && return 0; [ "$TIER" = "$1" ]; }  # --only overrides tier
name_match(){ [ -z "$ONLY" ] && return 0; [ "$ONLY" = "$1" ]; }

[ -f "$MANIFEST" ] || { warn "manifest not found: $MANIFEST"; exit 1; }
command -v aria2c >/dev/null 2>&1 || warn "aria2c not found — HF single-connection fetch + github-release will fall back / fail. Install: bash scripts/data/fetch-data.sh --install-deps"
if [ "$HF_CLI" = "hf" ] && ! command -v hf >/dev/null 2>&1; then
  warn "huggingface-hub CLI not found; HF downloads will fail. Install it: uv pip install huggingface-hub"
fi
if [ -z "$HF_TOKEN" ]; then
  warn "HF_TOKEN not set — anonymous rate limits are very low (likely 429). Run: hf auth login"
fi
command -v modelscope >/dev/null 2>&1 || "$PY" -c "import modelscope" 2>/dev/null || warn "modelscope CLI/SDK not found — modelscope-source models will fail. Install: uv pip install modelscope"

# --- manifest reader: JSON -> \x1f-delimited rows (mirrors fetch-data.sh's python-heredoc rows()) --
# name \x1f tier \x1f source \x1f repo \x1f revision \x1f size_bytes \x1f include_patterns(csv) \x1f notes
rows() {
  "$PY" - "$MANIFEST" <<'PY'
import json, sys
d = json.load(open(sys.argv[1], encoding="utf-8"))
for e in d:
    patterns = ",".join(e.get("include_patterns") or [])
    print("\x1f".join([
        e.get("name", ""),
        e.get("tier", ""),
        e.get("source", ""),
        e.get("repo", ""),
        e.get("revision", ""),
        str(e.get("size_bytes_approx", "") or ""),
        patterns,
        (e.get("notes", "") or "").replace("\x1f", " ").replace("\n", " "),
    ]))
PY
}

# --- completeness check: existence-only (no size verification -> cheap enough for --list) --------
# A model counts COMPLETE when every include_patterns glob matches >=1 file under its dest dir;
# MISSING when none match; PARTIAL otherwise.
check_status() { # dest patterns_csv
  local dest="$1" patterns_csv="$2"
  [ -d "$dest" ] || { echo MISSING; return; }
  local total=0 present=0 p
  local IFS=','
  local -a pats; read -ra pats <<< "$patterns_csv"
  for p in "${pats[@]}"; do
    [ -z "$p" ] && continue
    total=$((total + 1))
    # shellcheck disable=SC2086
    if compgen -G "$dest/$p" >/dev/null 2>&1; then present=$((present + 1)); fi
  done
  if [ "$total" -eq 0 ] || [ "$present" -eq 0 ]; then echo MISSING
  elif [ "$present" -eq "$total" ]; then echo COMPLETE
  else echo PARTIAL
  fi
}

# --- HF Xet-safe fetch, filtered to include_patterns -----------------------------------------
# Post-filters hf_complete.py's whole-repo missing list down to the manifest's include_patterns.
# python/fnmatch chosen over bash `case` globbing: it matches both the full relative path (for
# patterns like "1_Pooling/config.json") and the basename (for patterns like "model-*.safetensors"
# that should match regardless of directory), which is awkward to express reliably in bash alone.
filter_list() { # raw_list patterns_csv out_list
  local raw="$1" patterns_csv="$2" out="$3"
  "$PY" - "$raw" "$patterns_csv" "$out" <<'PYFILTER'
import sys, fnmatch
raw, patterns_csv, out = sys.argv[1], sys.argv[2], sys.argv[3]
patterns = [p for p in patterns_csv.split(",") if p]
groups, cur = [], []
with open(raw, encoding="utf-8") as f:
    for line in f:
        if line.startswith("  "):
            cur.append(line)
        else:
            if cur:
                groups.append(cur)
            cur = [line]
    if cur:
        groups.append(cur)
kept = []
for g in groups:
    d = o = ""
    for l in g[1:]:
        l = l.strip()
        if l.startswith("dir="):
            d = l[len("dir="):]
        elif l.startswith("out="):
            o = l[len("out="):]
    path = f"{d}/{o}" if d else o
    if any(fnmatch.fnmatch(path, p) or fnmatch.fnmatch(o, p) for p in patterns):
        kept.append(g)
with open(out, "w", encoding="utf-8") as f:
    for g in kept:
        f.writelines(g)
sys.stderr.write(f"[fetch-candidate-models] include_patterns filter kept {len(kept)}/{len(groups)} file(s)\n")
PYFILTER
}

fetch_hf_filtered() { # id dest patterns_csv rev
  local id="$1" dest="$2" patterns_csv="$3" rev="$4"
  mkdir -p "$dest/.hfd"
  [ -n "${HF_TOKEN:-}" ] && log "$id: using HF_TOKEN (authenticated, higher rate limits)"
  log "$id: manifest pins revision=$rev — hf_complete.py has no revision param (always diffs 'main'/HEAD);"
  log "$id: verify manually (e.g. hf api / repo commit history) if byte-for-byte pinning matters."

  # No aria2c or no differ -> single-stream hf CLI fallback (Xet-safe: whole-file, no range split).
  # Unlike hf_complete.py, the `hf` CLI DOES support --revision and --include, so use both here.
  if ! command -v aria2c >/dev/null 2>&1 || [ ! -f "$DIFFER" ]; then
    warn "$id: aria2c or hf_complete.py missing -> hf CLI fallback (single-stream, slow)"
    # --include is nargs-style: ONE flag then all patterns (repeated flags overwrite each other)
    local -a inc=(); local IFS=','; local -a pats; read -ra pats <<< "$patterns_csv"
    [ "${#pats[@]}" -gt 0 ] && inc=(--include "${pats[@]}")
    local -a rargs=(); [ -n "$rev" ] && rargs=(--revision "$rev")
    retry "$HF_CLI" download "$id" --repo-type model --local-dir "$dest" "${rargs[@]}" "${inc[@]}"
    return
  fi

  # Xet-safe, verifiable: diff (whole repo) -> filter to include_patterns -> fetch gaps
  # single-connection -> re-diff, up to 4 rounds (self-heal).
  local raw="$dest/.hfd/raw_missing.txt" list="$dest/.hfd/missing_xetsafe.txt" round=0 nmiss=1
  while [ "$round" -lt 4 ]; do
    round=$((round + 1))
    python -u "$DIFFER" "$id" "$dest" "$raw" model || { warn "$id: repo listing failed (bad id? gated?)"; return 1; }
    filter_list "$raw" "$patterns_csv" "$list"
    # NB: grep -c prints "0" AND exits 1 on no match — an `|| echo 0` here would emit "0\n0"
    nmiss="$(grep -c '^http' "$list" 2>/dev/null)"; [ -n "$nmiss" ] || nmiss=0
    [ "$nmiss" -eq 0 ] && { log "$id: included files 100% complete"; return 0; }
    log "$id: round $round — $nmiss included file(s) missing/short; fetching -j$HFD_JOBS single-connection"
    find "$dest" -name '*.aria2' -delete 2>/dev/null   # stale partials would trigger a 403-prone range resume
    ( cd "$dest" && aria2c -i "$list" -j "$HFD_JOBS" \
        --auto-file-renaming=false --allow-overwrite=true --file-allocation=none \
        --console-log-level=warn --summary-interval=20 \
        --max-tries=10 --retry-wait=3 --connect-timeout=30 --timeout=90 )
  done
  python -u "$DIFFER" "$id" "$dest" "$raw" model 2>/dev/null || true
  filter_list "$raw" "$patterns_csv" "$list"
  nmiss="$(grep -c '^http' "$list" 2>/dev/null)"; [ -n "$nmiss" ] || nmiss=0
  [ "$nmiss" -eq 0 ] && { log "$id: included files 100% complete"; return 0; }
  warn "$id: still $nmiss included file(s) missing after $round rounds — re-run to continue"
  return 1
}

# --- ModelScope fetch: same mechanism as fetch-data.sh's fetch_ms, plus --revision/--include (both
# confirmed present in `modelscope download --help`) since the manifest records them per model. ----
fetch_ms() { # id dest rev patterns_csv
  local id="$1" dest="$2" rev="$3" patterns_csv="$4"
  mkdir -p "$dest"
  # --include is nargs-style: ONE flag then all patterns (repeated --include flags overwrite each
  # other — argparse keeps only the last, which silently downloaded just README.md in testing)
  local -a inc=(); local IFS=','; local -a pats; read -ra pats <<< "$patterns_csv"
  [ "${#pats[@]}" -gt 0 ] && inc=(--include "${pats[@]}")
  local -a rargs=(); [ -n "$rev" ] && rargs=(--revision "$rev")
  log "$id: modelscope download --model --revision ${rev:-<default>} --include <${#pats[@]} pattern(s)>"
  retry modelscope download --max-workers "$MS_WORKERS" --model "$id" --local_dir "$dest" "${rargs[@]}" "${inc[@]}" || return 1
  # modelscope exits 0 even when --include matched nothing -> post-check completeness ourselves
  local status; status="$(check_status "$dest" "$patterns_csv")"
  [ "$status" = COMPLETE ] || { warn "$id: post-fetch status=$status (expected COMPLETE) — check include_patterns vs repo file names"; return 1; }
}

# --- github-release fetch: single resumable file via aria2c (falls back to curl); GH_MIRROR_PREFIX
# is prepended verbatim onto the raw github.com URL (e.g. a ghproxy mirror) when set. -------------
fetch_github_release() { # repo filename dest tag
  local repo="$1" filename="$2" dest="$3" tag="${4:-latest}"
  mkdir -p "$dest"
  local url="https://github.com/${repo}/releases/download/${tag}/${filename}"
  [ -n "$GH_MIRROR_PREFIX" ] && url="${GH_MIRROR_PREFIX}${url}"
  log "$repo: release asset -> $url"
  if [ -f "$dest/$filename" ]; then
    log "$repo: $filename already present locally (existence check only; re-run manually to force refresh)"
    return 0
  fi
  if command -v aria2c >/dev/null 2>&1; then
    ( cd "$dest" && aria2c -x1 -s1 -j1 -c --auto-file-renaming=false --allow-overwrite=false \
        --console-log-level=warn --max-tries=10 --retry-wait=3 --connect-timeout=30 --timeout=90 \
        --out="$filename" "$url" )
  else
    warn "$repo: aria2c missing -> curl fallback (no resume)"
    retry curl -fL --retry 5 -o "$dest/$filename" "$url"
  fi
}

# --- main --------------------------------------------------------------------------------------
if [ "$LIST_ONLY" -eq 1 ]; then
  echo "== T11 candidate models -> $MODELS  (manifest: $MANIFEST) =="
  printf '%-28s %-4s %-15s %-9s %-8s %-14s %s\n' NAME TIER SOURCE STATUS SIZE REV REPO
  while IFS=$'\x1f' read -r name tier source repo rev size patterns_csv notes; do
    name_match "$name" || continue
    tier_match "$tier" || continue
    dest="$MODELS/$name"
    status="$(check_status "$dest" "$patterns_csv")"
    sizemb=$(( ${size:-0} / 1000000 ))
    printf '%-28s %-4s %-15s %-9s %-8s %-14s %s\n' "$name" "$tier" "$source" "$status" "${sizemb}MB" "${rev:0:12}" "$repo"
  done < <(rows)
  exit 0
fi

echo "== T11 candidate models -> $MODELS  (tier=$TIER${ONLY:+, only=$ONLY}) =="
COUNT=0; SKIP=0; FAIL=0
while IFS=$'\x1f' read -r name tier source repo rev size patterns_csv notes; do
  name_match "$name" || continue
  tier_match "$tier" || continue
  dest="$MODELS/$name"
  status="$(check_status "$dest" "$patterns_csv")"
  if [ "$status" = COMPLETE ]; then
    log "skip complete: $name"; SKIP=$((SKIP + 1)); continue
  fi
  log "fetch $name  [$source ${repo}]  tier=$tier status=$status -> models/$name"
  case "$source" in
    hf)              fetch_hf_filtered "$repo" "$dest" "$patterns_csv" "$rev" && COUNT=$((COUNT+1)) || FAIL=$((FAIL+1)) ;;
    modelscope)      fetch_ms "$repo" "$dest" "$rev" "$patterns_csv"          && COUNT=$((COUNT+1)) || FAIL=$((FAIL+1)) ;;
    github-release)  IFS=',' read -ra _pats <<< "$patterns_csv"
                      fetch_github_release "$repo" "${_pats[0]}" "$dest"      && COUNT=$((COUNT+1)) || FAIL=$((FAIL+1)) ;;
    *)                warn "$name: unknown source '$source'; skipping" ;;
  esac
done < <(rows)
log "done. fetched=$COUNT skipped=$SKIP failed=$FAIL   (manifest: $MANIFEST)"
[ "$FAIL" -eq 0 ]
