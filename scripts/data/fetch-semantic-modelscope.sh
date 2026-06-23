#!/usr/bin/env bash
# Fetch SEMANTIC-task datasets that ARE hosted on ModelScope (CN-friendly, no VPN needed).
# MANUAL run — you run this yourself in WSL with the speechrl venv active
# (`source ~/.venvs/speechrl/bin/activate`). It downloads; it never commits.
#
#   bash scripts/data/fetch-semantic-modelscope.sh --list       # show targets, fetch nothing
#   bash scripts/data/fetch-semantic-modelscope.sh --dry-run all # print commands, download nothing
#   bash scripts/data/fetch-semantic-modelscope.sh all          # fetch all ModelScope-hosted sets
#   bash scripts/data/fetch-semantic-modelscope.sh voicebench   # fetch one
#
# REALITY: of the semantic-task catalog, ONLY VoiceBench (+ FLEURS, already local) is on
# ModelScope. Everything else (HeySQuAD, MMSU, Speech-MASSIVE, URO-Bench, VocalBench,
# Big-Bench-Audio, FLEURS-R, CVSS, Spoken-SQuAD, SLURP, STOP) is NOT on ModelScope —
# use scripts/data/fetch-semantic-manual.sh for those. Full catalog + licenses:
# wiki/Speech-Semantic-Task-Datasets.md.
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE="${SPEECHRL_WORKSPACE:-$(cd "$SCRIPT_DIR/../.." && pwd)}"
DATA_ROOT="${SPEECHRL_DATA_DIR:-$WORKSPACE/speechrl-data}"
DSETS="$DATA_ROOT/datasets"
MS_WORKERS="${SPEECHRL_MS_WORKERS:-16}"
SKIP_EXISTING="${SPEECHRL_SKIP_EXISTING:-1}"
DRY_RUN=0
mkdir -p "$DSETS"

log()  { printf '[semantic-ms] %s\n' "$*"; }
warn() { printf '[semantic-ms] WARNING: %s\n' "$*" >&2; }

# name | modelscope dataset id | local dir (under datasets/) | note
TARGETS=(
  "voicebench|lmms-lab/voicebench|voicebench|Apache-2.0 | spoken-QA + agentic in ONE (sd-qa/mmsu/openbookqa/commoneval + alpacaeval/ifeval/advbench/wildvoice) | ~11GB"
  "fleurs|pengzhendong/fleurs|fleurs|CC-BY-4.0 | ST 102-lang n-way parallel + language-ID | ALREADY LOCAL (normally skipped)"
)

has_data() { local d="$1"; [[ -d "$d" ]] && [[ "$(find "$d" -maxdepth 5 -type f ! -name '.*' 2>/dev/null | head -n 5 | wc -l)" -gt 3 ]]; }

run() {  # echo under --dry-run; otherwise run with up to 3 retries
  if [[ "$DRY_RUN" == 1 ]]; then printf '  DRY-RUN> %s\n' "$*"; return 0; fi
  local n=1
  while [[ $n -le 3 ]]; do "$@" && return 0; warn "attempt $n/3 failed; retry in $((n*5))s"; sleep $((n*5)); n=$((n+1)); done
  warn "gave up after 3 attempts"; return 1
}

fetch_one() {
  local name="$1" id="$2" dir="$3"
  local dest="$DSETS/$dir"
  if [[ "$SKIP_EXISTING" == 1 ]] && has_data "$dest"; then log "skip existing: $name ($dest)"; return 0; fi
  if [[ "$DRY_RUN" == 0 ]] && ! command -v modelscope >/dev/null 2>&1; then
    warn "'modelscope' CLI not found — activate the speechrl venv first (source ~/.venvs/speechrl/bin/activate)"; return 1
  fi
  log "fetch $name  <-  modelscope:$id  ->  $dest"
  run modelscope download --max-workers "$MS_WORKERS" --dataset "$id" --local_dir "$dest"
}

list_targets() {
  printf '%-16s %-26s %s\n' NAME MODELSCOPE_ID NOTE
  local t n id dir note
  for t in "${TARGETS[@]}"; do IFS='|' read -r n id dir note <<<"$t"; printf '%-16s %-26s %s\n' "$n" "$id" "$note"; done
}

main() {
  local args=() a
  for a in "$@"; do
    case "$a" in
      --dry-run) DRY_RUN=1 ;;
      --list) list_targets; exit 0 ;;
      -h|--help) sed -n '2,13p' "$0"; exit 0 ;;
      *) args+=("$a") ;;
    esac
  done
  if [[ ${#args[@]} -eq 0 ]]; then warn "nothing selected. Use: all | <name...> | --list | --dry-run"; list_targets; exit 1; fi
  local want=" ${args[*]} " t n id dir note
  for t in "${TARGETS[@]}"; do
    IFS='|' read -r n id dir note <<<"$t"
    if [[ "$want" == *" all "* || "$want" == *" $n "* ]]; then fetch_one "$n" "$id" "$dir"; fi
  done
  log "done."
}
main "$@"
