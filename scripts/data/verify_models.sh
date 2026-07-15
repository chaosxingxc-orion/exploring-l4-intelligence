#!/usr/bin/env bash
# verify_models.sh — byte-level completeness audit for models/, using the SAME mechanism as
# hf_complete.py (HF repo-tree listing vs local getsize(), not a size/file-count heuristic).
#
# WHY this exists: inventory.sh's check_model() is a heuristic (min file count + min total size)
# and can mark a truncated download COMPLETE (this is exactly how emotion2vec-s's checkpoint.pt —
# ~1MB on disk vs 1.13GB upstream — went unnoticed; see wiki/2026-07-09-coverage-model-matrix.md
# §0.1). fetch-candidate-models.sh's own --list check_status() is also existence-only (glob match,
# no size check) for the same reason it exists: cheap enough to run before every fetch. This script
# is the byte-accurate counterpart, run standalone/periodically, not gating every fetch.
#
# SCOPE: only dirs under models/ with a **known HF source** are byte-checked (source repo id + host
# reachable via the HF API) — that means:
#   (a) every entry in docs/models.candidates.json with source=="hf" (include_patterns known -> the
#       diff is filtered to exactly those files, so extra upstream files -- other quantizations,
#       language variants -- never cause a false PARTIAL);
#   (b) every entry in docs/datasets.lock.json's "models" array with source.kind in {"hf","hf-manual"}.
#       These entries carry NO include_patterns in the lock schema. For the one case in the lock that
#       is a deliberate *partial* repo fetch (qwen3-omni-30b-a3b-instruct-gguf: 2 files out of a >110GB
#       repo, see fetch-qwen3-omni-gguf.sh), this script hardcodes the same two filenames so the many
#       un-fetched quant/mmproj variants are not misreported as missing. Any other hf/hf-manual lock
#       entry with no hardcoded patterns falls back to a FULL repo diff (reported as such) — this can
#       over-report if that repo is *also* meant to be fetched selectively; read the NOTE column.
# ModelScope- and github-release-sourced models (campplus-zh, eres2netv2-zh, redimnet-b6, and the 5
# ModelScope-hosted lock backbones) are NOT byte-checked here — hf_complete.py only speaks the HF API.
# They are listed at the end under "skipped (non-HF source)" for visibility, not silently dropped.
#
# Usage:
#   bash scripts/data/verify_models.sh              # verify every HF-sourced model dir present on disk
#   bash scripts/data/verify_models.sh --only NAME   # verify one model by manifest name
#
# Env: SPEECHRL_DATA_DIR (data root), SPEECHRL_HF_ENDPOINT (default hf-mirror.com), SPEECHRL_VENV.
# Exit code: 0 iff every checked model is COMPLETE (full-repo-diff entries never fail the exit code,
# since "extra upstream files not fetched" is not necessarily an error — see NOTE).
set -u
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
DATA="${SPEECHRL_DATA_DIR:-$REPO_ROOT/speechrl-data}"
MODELS="$DATA/models"
CANDIDATES="${SPEECHRL_MODELS_CANDIDATES:-$REPO_ROOT/docs/models.candidates.json}"
LOCK="${SPEECHRL_DATASETS_LOCK:-$REPO_ROOT/docs/datasets.lock.json}"
DIFFER="$SCRIPT_DIR/hf_complete.py"

SPEECHRL_VENV="${SPEECHRL_VENV:-$HOME/.venvs/speechrl}"
# shellcheck disable=SC1091
[ -f "$SPEECHRL_VENV/bin/activate" ] && { source "$SPEECHRL_VENV/bin/activate"; export PATH="$SPEECHRL_VENV/bin:$PATH"; }
export HF_ENDPOINT="${SPEECHRL_HF_ENDPOINT:-https://hf-mirror.com}"
export HF_HUB_DISABLE_XET="${HF_HUB_DISABLE_XET:-1}"
export LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONIOENCODING=utf-8 NO_COLOR=1
PY="${SPEECHRL_PYTHON:-$(command -v python || command -v python3 || echo python)}"

ONLY=""
while [ $# -gt 0 ]; do
  case "$1" in
    --only) ONLY="${2:-}"; shift 2 ;;
    -h|--help) sed -n '2,30p' "$0"; exit 0 ;;
    *) echo "[verify_models] WARNING: unknown arg: $1" >&2; shift ;;
  esac
done

[ -f "$DIFFER" ] || { echo "[verify_models] FATAL: $DIFFER not found" >&2; exit 1; }
command -v "$PY" >/dev/null 2>&1 || { echo "[verify_models] FATAL: python not found" >&2; exit 1; }

# --- Row source (a): docs/models.candidates.json, source=="hf" only -----------------------------
# name \x1f repo \x1f patterns_csv \x1f origin
rows_candidates() {
  [ -f "$CANDIDATES" ] || return 0
  "$PY" - "$CANDIDATES" <<'PY'
import json, sys
d = json.load(open(sys.argv[1], encoding="utf-8"))
for e in d:
    if e.get("source") != "hf":
        continue
    patterns = ",".join(e.get("include_patterns") or [])
    print("\x1f".join([e.get("name", ""), e.get("repo", ""), patterns, "candidates.json"]))
PY
}

# --- Row source (b): docs/datasets.lock.json .models[], source.kind in {hf,hf-manual} -----------
# Hardcoded include_patterns override for the one KNOWN deliberate partial-repo fetch in the lock
# (qwen3-omni-30b-a3b-instruct-gguf -- see fetch-qwen3-omni-gguf.sh for why: 2 files out of a
# >110GB multi-quant repo). Any other hf/hf-manual lock entry gets patterns_csv="" -> full-repo diff.
rows_lock() {
  [ -f "$LOCK" ] || return 0
  "$PY" - "$LOCK" <<'PY'
import json, sys
d = json.load(open(sys.argv[1], encoding="utf-8"))
OVERRIDE = {
    "qwen3-omni-30b-a3b-instruct-gguf": [
        "Qwen3-Omni-30B-A3B-Instruct-Q8_0.gguf",
        "mmproj-Qwen3-Omni-30B-A3B-Instruct-bf16.gguf",
    ],
}
for e in d.get("models", []):
    src = e.get("source") or {}
    if src.get("kind") not in ("hf", "hf-manual"):
        continue
    name = e.get("name", "")
    repo = src.get("id") or src.get("hf_id") or ""
    patterns = ",".join(OVERRIDE.get(name, []))
    print("\x1f".join([name, repo, patterns, "datasets.lock.json (models[])"]))
PY
}

# --- fnmatch filter, same shape as fetch-candidate-models.sh's filter_list ----------------------
# Reads hf_complete.py's raw missing-list (dir=/out= blocks); returns kept-count + kept-bytes on
# stdout as "count\x1fbytes" when patterns_csv is non-empty; with patterns_csv=="" (full-repo diff)
# it passes every block through unfiltered.
filter_and_count() { # raw_list patterns_csv
  local raw="$1" patterns_csv="$2"
  "$PY" - "$raw" "$patterns_csv" <<'PYFILTER'
import sys, fnmatch, re
raw, patterns_csv = sys.argv[1], sys.argv[2]
patterns = [p for p in patterns_csv.split(",") if p]
groups, cur = [], []
try:
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
except FileNotFoundError:
    print("0\x1f0")
    sys.exit(0)
kept_n = 0
kept_paths = []
for g in groups:
    d = o = ""
    for l in g[1:]:
        l = l.strip()
        if l.startswith("dir="):
            d = l[len("dir="):]
        elif l.startswith("out="):
            o = l[len("out="):]
    path = f"{d}/{o}" if d else o
    if not patterns or any(fnmatch.fnmatch(path, p) or fnmatch.fnmatch(o, p) for p in patterns):
        kept_n += 1
        kept_paths.append(path)
print(f"{kept_n}\x1f" + ";".join(kept_paths[:8]) + ("..." if kept_n > 8 else ""))
PYFILTER
}

echo "== verify_models.sh -> $MODELS =="
echo "   candidates manifest: $CANDIDATES"
echo "   lock manifest:       $LOCK"
echo

printf '%-32s %-10s %-9s %-14s %s\n' NAME ORIGIN STATUS MISSING_FILES SAMPLE
printf '%-32s %-10s %-9s %-14s %s\n' -------------------------------- ---------- --------- -------------- ------

N_OK=0; N_PARTIAL=0; N_MISSING_DIR=0; N_ERR=0
TMPDIR="$(mktemp -d)"
trap 'rm -rf "$TMPDIR"' EXIT

seen_names=""
while IFS=$'\x1f' read -r name repo patterns_csv origin; do
  [ -z "$name" ] && continue
  # de-dup: a name could in principle appear from both sources; first hit wins. This must run
  # BEFORE the --only filter below, so every manifest-known name is recorded as "known HF source"
  # regardless of whether --only narrows which ones actually get byte-checked this run — otherwise
  # `--only X` makes every OTHER manifest-listed model wrongly print as "no manifest entry" in the
  # not-checked section further down.
  case " $seen_names " in *" $name "*) continue ;; esac
  seen_names="$seen_names $name"
  if [ -n "$ONLY" ] && [ "$ONLY" != "$name" ]; then continue; fi
  origin_short="${origin%% *}"
  dest="$MODELS/$name"
  if [ ! -d "$dest" ]; then
    printf '%-32s %-10s %-9s %-14s %s\n' "$name" "$origin_short" "NO-DIR" "-" "not fetched yet"
    N_MISSING_DIR=$((N_MISSING_DIR + 1))
    continue
  fi
  raw="$TMPDIR/${name}.raw.txt"
  if ! "$PY" -u "$DIFFER" "$repo" "$dest" "$raw" model 2>"$TMPDIR/${name}.err"; then
    printf '%-32s %-10s %-9s %-14s %s\n' "$name" "$origin_short" "ERROR" "-" "$(tail -c 200 "$TMPDIR/${name}.err" | tr '\n' ' ')"
    N_ERR=$((N_ERR + 1))
    continue
  fi
  result="$(filter_and_count "$raw" "$patterns_csv")"
  nmiss="${result%%$'\x1f'*}"
  sample="${result#*$'\x1f'}"
  scope_note=""
  [ -z "$patterns_csv" ] && scope_note=" (full-repo diff, no include_patterns known)"
  if [ "$nmiss" -eq 0 ] 2>/dev/null; then
    printf '%-32s %-10s %-9s %-14s %s\n' "$name" "$origin_short" "COMPLETE" "0" "-"
    N_OK=$((N_OK + 1))
  else
    printf '%-32s %-10s %-9s %-14s %s\n' "$name" "$origin_short" "PARTIAL" "$nmiss" "${sample}${scope_note}"
    N_PARTIAL=$((N_PARTIAL + 1))
  fi
done < <(rows_candidates; rows_lock)

echo
echo "== dirs under models/ NOT byte-checked (non-HF source, or no manifest entry) =="
if [ -d "$MODELS" ]; then
  for d in "$MODELS"/*/; do
    n="$(basename "$d")"
    case " $seen_names " in
      *" $n "*) continue ;;
    esac
    reason="no manifest entry with a known HF source"
    case "$n" in
      campplus-zh|eres2netv2-zh) reason="ModelScope source (not HF API-checkable)" ;;
      redimnet-b6) reason="github-release source (not HF API-checkable)" ;;
      nemotron3-nano-omni-nvfp4|omni-embed-nemotron-3b)
        reason="ModelScope source (not HF API-checkable)" ;;
    esac
    printf '  %-30s %s\n' "$n" "$reason"
  done
fi

echo
echo "SUMMARY: complete=$N_OK partial=$N_PARTIAL no-dir=$N_MISSING_DIR error=$N_ERR"
[ "$N_PARTIAL" -eq 0 ] && [ "$N_ERR" -eq 0 ]
