#!/usr/bin/env bash
# fetch-candidates.sh — download the WS-D survey-sourced candidate datasets (docs/datasets.candidates.json).
#
# B-grade (obtainable) datasets NOT in the frozen datasets.lock.json, queued for owner fetch. Sources were
# web-verified 2026-07-07 (high confidence, evidence in the survey doc). Never touches the frozen lock.
#
#   bash scripts/data/fetch-candidates.sh --list        # list only, fetch nothing
#   bash scripts/data/fetch-candidates.sh               # fetch all HF + git; gated ones print instructions
#   bash scripts/data/fetch-candidates.sh squtr ...     # fetch only the named dataset(s)
#
# Deps: huggingface-cli (pip install -U "huggingface_hub[cli]"), git. Data -> $SPEECHRL_DATA_DIR/datasets/<name>.
set -u
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
DATA="${SPEECHRL_DATA_DIR:-$REPO_ROOT/speechrl-data}"
DS="$DATA/datasets"
echo "[fetch-candidates] data dir = $DATA"
mkdir -p "$DS"

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
sel() { [ "${#ARGS[@]}" -eq 0 ] && return 0; local n="$1"; for w in "${ARGS[@]}"; do [ "$w" = "$n" ] && return 0; done; return 1; }

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
    hf:*)
      huggingface-cli download "${method#hf:}" --repo-type dataset --local-dir "$DS/$name" \
        || echo "     !! $name HF download failed (install huggingface_hub[cli] / check auth)";;
    git:*)
      git clone "https://github.com/${method#git:}" "$DS/$name" \
        && echo "     -> cloned; download the v3 data from the Google Drive link in $DS/$name/README (manual)" \
        || echo "     !! $name git clone failed";;
    gated:*)
      echo "     -> GATED: open ${method#gated:} , register + sign the DUA; the download link is emailed (cannot automate).";;
  esac
done
echo "== done =="
