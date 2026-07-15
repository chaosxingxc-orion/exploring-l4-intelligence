#!/usr/bin/env bash
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

export HF_ENDPOINT="${SPEECHRL_HF_ENDPOINT:-https://hf-mirror.com}"
export HF_HUB_DISABLE_XET="${HF_HUB_DISABLE_XET:-1}"
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
