#!/usr/bin/env bash
# fetch-candidates.sh — download the WS-D survey-sourced candidate datasets (docs/datasets.candidates.json).
#
# These are B-grade (obtainable) datasets NOT in the frozen datasets.lock.json, queued for owner fetch.
# Exact HF ids are best-effort; entries with a confident id download automatically, the rest print a
# RESOLVE line (one-time manual id confirmation from the paper, then re-run). Never touches the frozen lock.
#
#   SPEECHRL_DATA_DIR=/mnt/d/chao_workspace/exploring-l4-intelligence/speechrl-data \
#       bash scripts/data/fetch-candidates.sh            # download confident ids
#   bash scripts/data/fetch-candidates.sh --list         # just list, fetch nothing
#
# Deps: huggingface-cli (pip install -U "huggingface_hub[cli]"). Some sets are gated/registration-only.
set -u
# Auto-default SPEECHRL_DATA_DIR to <repo>/speechrl-data (script sits at <repo>/scripts/data/),
# so it runs without an env prefix; override by exporting SPEECHRL_DATA_DIR.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
DATA="${SPEECHRL_DATA_DIR:-$REPO_ROOT/speechrl-data}"
echo "[fetch-candidates] data dir = $DATA"
DS="$DATA/datasets"
LIST_ONLY=0; [ "${1:-}" = "--list" ] && LIST_ONLY=1
mkdir -p "$DS"

# name | HF dataset id (empty = RESOLVE) | note/source
CANDS=(
  "esc-50|ashraq/esc50|audio-event knowledge (iKnow-audio); 50-class, confident"
  "fsd50k|Fhrozen/FSD50K|audio-event knowledge (iKnow-audio); confirm repo id"
  "slue-sqa-5|asapp/slue-phase-2|spoken-QA (WavRAG); confirm SQA-5 subset/config"
  "audiocaps-qa||AudioCaps public (d0rj/audiocaps) but VAT-KG QA split needs paper release — RESOLVE"
  "audio2tool||arXiv 2604.22821 release (github/HF) — RESOLVE"
  "auditorybench-plusplus||arXiv 2509.17641 data release — RESOLVE"
  "mlc-slm||Interspeech-2025 MLC-SLM Challenge (nexdata.ai, registration) — RESOLVE"
  "squtr||arXiv 2602.12783 (6 public sets) — RESOLVE"
  "full-duplex-bench-v3||arXiv 2604.04847 (100 real recs) — RESOLVE"
)

echo "== WS-D download candidates -> $DS =="
ok=0; todo=0
for row in "${CANDS[@]}"; do
  IFS='|' read -r name hfid note <<< "$row"
  if [ -z "$hfid" ]; then
    echo "  [RESOLVE] $name : $note"; todo=$((todo+1)); continue
  fi
  echo "  [FETCH ] $name <- hf:$hfid ($note)"
  ok=$((ok+1))
  [ "$LIST_ONLY" -eq 1 ] && continue
  huggingface-cli download "$hfid" --repo-type dataset --local-dir "$DS/$name" \
    || echo "     !! $name failed (id wrong / gated / need auth) — verify hf:$hfid"
done
echo "== $ok auto-fetch, $todo need id resolution (edit CANDS[] then re-run) =="
