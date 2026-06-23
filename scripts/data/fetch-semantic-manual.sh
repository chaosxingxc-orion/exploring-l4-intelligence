#!/usr/bin/env bash
# Fetch SEMANTIC-task datasets that are NOT on ModelScope — via hf-mirror.com (HF_ENDPOINT)
# or, for a couple, their direct source (Zenodo / fbaipublicfiles). MANUAL run: you run this
# yourself in WSL with the speechrl venv active and pull only what you want.
#
#   bash scripts/data/fetch-semantic-manual.sh --list            # show targets + sources
#   bash scripts/data/fetch-semantic-manual.sh --dry-run all     # print commands, download nothing
#   bash scripts/data/fetch-semantic-manual.sh heysquad          # the starter spoken-QA set
#   bash scripts/data/fetch-semantic-manual.sh speech-massive mmsu
#
# Route: hf-mirror first (prefers `hfd`+aria2c if present, else the `hf` CLI). Two sets have
# no clean HF mirror and print MANUAL direct-download instructions instead: slurp (Zenodo
# 4274930) and stop (dl.fbaipublicfiles.com/stop). NC-licensed sets are eval-only.
# Full catalog + licenses: wiki/Speech-Semantic-Task-Datasets.md.
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE="${SPEECHRL_WORKSPACE:-$(cd "$SCRIPT_DIR/../.." && pwd)}"
DATA_ROOT="${SPEECHRL_DATA_DIR:-$WORKSPACE/speechrl-data}"
DSETS="$DATA_ROOT/datasets"
HF_ENDPOINT="${SPEECHRL_HF_ENDPOINT:-https://hf-mirror.com}"; export HF_ENDPOINT
export HF_HUB_DISABLE_XET="${HF_HUB_DISABLE_XET:-1}"
HFD_THREADS="${SPEECHRL_HFD_THREADS:-8}"
HF_CLI="${HF_CLI:-hf}"
SKIP_EXISTING="${SPEECHRL_SKIP_EXISTING:-1}"
DRY_RUN=0
mkdir -p "$DSETS"

log()  { printf '[semantic-manual] %s\n' "$*"; }
warn() { printf '[semantic-manual] WARNING: %s\n' "$*" >&2; }

# name | hf dataset id | local dir | note  (all fetched from hf-mirror)
HF_TARGETS=(
  "heysquad|yijingwu/HeySQuAD_human|heysquad|CC-BY-4.0 | extractive spoken-QA, gold answer spans | STARTER"
  "speech-massive|FBK-MT/Speech-MASSIVE|speech-massive|CC-BY-NC-SA (eval-only) | 12-lang SLU intent+slot; bridges to ST"
  "mmsu|ddwang2000/MMSU|mmsu|MIT | multi-skill spoken-reasoning MCQ"
  "spoken-squad|AudioLLMs/spoken_squad_test|spoken-squad|CC-BY-SA (re-host) | ASR-noise-robust spoken QA"
  "uro-bench|Honggao/URO-Bench|uro-bench|MIT | EN+ZH spoken-dialogue agentic | ~12GB"
  "vocalbench|VocalNet/VocalBench|vocalbench|Apache-2.0 | 9-axis conversational eval"
  "big-bench-audio|ArtificialAnalysis/big_bench_audio|big-bench-audio|MIT | spoken reasoning, 1000 items | ~319MB"
  "fleurs-r|google/fleurs-r|fleurs-r|CC-BY-4.0 | restored-audio FLEURS (HF viewer broken, files download fine)"
  "cvss|google/cvss|cvss|CC-BY-4.0 | speech-to-speech translation, 21 langs -> en"
  "speech-commands|google/speech_commands|speech-commands|CC-BY-4.0 | SLU/keyword-spotting (35 words); benchmarking-OK"
  # --- speech-agentic, recent (2024-2026) ---
  "voiceassistant-eval|MathLLMs/VoiceAssistant-Eval|voiceassistant-eval|MIT | spoken-assistant 13-cat (roleplay/safety/S2S), 10.5k | ~9.5GB"
  "vocalbench-zh|VocalNet/VocalBench-zh|vocalbench-zh|Apache-2.0 | Mandarin spoken-interaction, 10k | ~4GB"
  "audiomc|ScaleAI/audiomc|audiomc|MIT | multi-turn instruction retention, 452 ex"
  "soulx-duplug|Soul-AILab/SoulX-Duplug-Eval|soulx-duplug|Apache-2.0 | full-duplex turn-taking EN+ZH | ~332MB"
  "eva-bench|ServiceNow-AI/eva|eva-bench|MIT | voice-agent task+experience (airline) | tiny"
  # --- speech-retrieval (bi-encoder native eval) ---
  "svq|google/svq|svq|CC-BY-4.0 | MSEB spoken-query retrieval under noise, 177k / 17 langs"
  "xtreme-s|google/xtreme_s|xtreme-s|CC-BY-4.0 | FLEURS-Retrieval cross-lingual speech<->text, 102 langs"
  "slue-phase-2|asapp/slue-phase-2|slue-phase-2|mixed CC-BY-SA | SLUE-SQA-5 spoken-doc retrieval + dialog-act/NER"
)

has_data() { local d="$1"; [[ -d "$d" ]] && [[ "$(find "$d" -maxdepth 5 -type f ! -name '.*' 2>/dev/null | head -n 5 | wc -l)" -gt 3 ]]; }

run() {  # echo under --dry-run; otherwise run with up to 3 retries
  if [[ "$DRY_RUN" == 1 ]]; then printf '  DRY-RUN> %s\n' "$*"; return 0; fi
  local n=1
  while [[ $n -le 3 ]]; do "$@" && return 0; warn "attempt $n/3 failed; retry in $((n*5))s"; sleep $((n*5)); n=$((n+1)); done
  warn "gave up after 3 attempts"; return 1
}

hf_fetch() {
  local name="$1" id="$2" dir="$3"
  local dest="$DSETS/$dir"
  if [[ "$SKIP_EXISTING" == 1 ]] && has_data "$dest"; then log "skip existing: $name ($dest)"; return 0; fi
  log "fetch $name  <-  hf-mirror:$id  ->  $dest   (HF_ENDPOINT=$HF_ENDPOINT)"
  if [[ "$DRY_RUN" == 1 ]]; then
    run env HF_ENDPOINT="$HF_ENDPOINT" hfd "$id" --local-dir "$dest" --dataset --tool aria2c -x "$HFD_THREADS"
    return
  fi
  if command -v hfd >/dev/null 2>&1 && command -v aria2c >/dev/null 2>&1; then
    run env HF_ENDPOINT="$HF_ENDPOINT" hfd "$id" --local-dir "$dest" --dataset --tool aria2c -x "$HFD_THREADS"
  elif command -v "$HF_CLI" >/dev/null 2>&1; then
    run "$HF_CLI" download "$id" --repo-type dataset --resume-download --local-dir "$dest"
  else
    warn "neither hfd/aria2c nor the '$HF_CLI' CLI found — activate the speechrl venv first"; return 1
  fi
}

d_slurp() {  # English SLU; no clean HF dataset -> manual direct download
  local dest="$DSETS/slurp"
  log "SLURP (manual / direct) -> $dest"
  cat <<EOF
  Official audio : Zenodo record 4274930 (FLAC tarballs, ~6 GB)  ->  $dest/audio
  Transcripts    : GitHub pswietojanski/slurp (jsonl metadata)
  Convenient (community HF mirror, license UNCONFIRMED — verify before non-research use):
    HF_ENDPOINT=$HF_ENDPOINT $HF_CLI download qmeeus/slurp --repo-type dataset --local-dir $dest
  Official route:
    git clone https://github.com/pswietojanski/slurp $dest
    # then aria2c the Zenodo tarballs listed in $dest/scripts/download_audio.sh into $dest/audio
EOF
}

d_stop() {  # Meta Spoken Task-Oriented Parsing; repo archived but downloadable
  local dest="$DSETS/stop"
  log "STOP (manual / direct, Meta; repo archived/read-only) -> $dest"
  cat <<EOF
  Repo    : https://github.com/facebookresearch/spoken_task_oriented_parsing (archived 2023-10-31)
  Audio   : https://dl.fbaipublicfiles.com/stop/   (exact tarball names in the repo getting-started)
  Steps:
    git clone https://github.com/facebookresearch/spoken_task_oriented_parsing $dest
    # follow $dest getting-started: pull stop_{train,eval,test} + low-resource splits from dl.fbaipublicfiles.com/stop/
EOF
}

list_targets() {
  printf '%-16s %-30s %s\n' NAME SOURCE NOTE
  local t n id dir note
  for t in "${HF_TARGETS[@]}"; do IFS='|' read -r n id dir note <<<"$t"; printf '%-16s %-30s %s\n' "$n" "hf-mirror:$id" "$note"; done
  printf '%-16s %-30s %s\n' slurp "Zenodo 4274930 / GitHub" "English SLU (manual; CC-BY-NC audio)"
  printf '%-16s %-30s %s\n' stop  "dl.fbaipublicfiles.com/stop" "compositional SLU parse (manual; CC-BY-SA)"
}

run_target() {
  local name="$1" t n id dir note
  if [[ "$name" == slurp ]]; then d_slurp; return; fi
  if [[ "$name" == stop ]];  then d_stop;  return; fi
  for t in "${HF_TARGETS[@]}"; do
    IFS='|' read -r n id dir note <<<"$t"
    if [[ "$n" == "$name" ]]; then hf_fetch "$n" "$id" "$dir"; return; fi
  done
  warn "unknown target: $name (try --list)"
}

main() {
  local args=() a
  for a in "$@"; do
    case "$a" in
      --dry-run) DRY_RUN=1 ;;
      --list) list_targets; exit 0 ;;
      -h|--help) sed -n '2,15p' "$0"; exit 0 ;;
      *) args+=("$a") ;;
    esac
  done
  if [[ ${#args[@]} -eq 0 ]]; then warn "nothing selected. Use: all | <name...> | --list | --dry-run"; list_targets; exit 1; fi
  local want=" ${args[*]} " all_names=() t n id dir note
  for t in "${HF_TARGETS[@]}"; do IFS='|' read -r n id dir note <<<"$t"; all_names+=("$n"); done
  all_names+=(slurp stop)
  for n in "${all_names[@]}"; do
    if [[ "$want" == *" all "* || "$want" == *" $n "* ]]; then run_target "$n"; fi
  done
  log "done."
}
main "$@"
