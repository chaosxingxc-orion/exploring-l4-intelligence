#!/usr/bin/env bash
# Phase 2 + 4 — run INSIDE WSL2 Ubuntu after wsl-setup.sh.
# Creates the shared Python 3.12 venv (in ext4) and installs the torch+verl stack.
set -euo pipefail
export PATH="$HOME/.local/bin:$PATH"   # ensure uv is found

VENV="${SPEECHRL_VENV:-$HOME/.venvs/speechrl}"
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

# Data lives in ext4, never in git.
mkdir -p "$HOME/speechrl-data/datasets" "$HOME/speechrl-data/checkpoints" \
         "$HOME/speechrl-data/mlruns" "$HOME/speechrl-data/hf-cache"

uv venv "$VENV" --python 3.12
# shellcheck disable=SC1091
source "$VENV/bin/activate"

# --- Phase 2: torch for Blackwell (cu128) ---
uv pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu128
python -c "import torch; assert torch.cuda.is_available(); print('GPU:', torch.cuda.get_device_name(0))"

# --- core science + speech + tracking ---
uv pip install transformers datasets accelerate peft \
               librosa soundfile jiwer \
               hydra-core omegaconf mlflow ruff pytest

# --- data-download CLIs (needed by scripts/data/fetch-data.sh): HF Hub CLI + fast transfer,
#     and ModelScope (some models/datasets are ModelScope-only). aria2 comes from wsl-setup.sh. ---
uv pip install "huggingface_hub[cli,hf_transfer]" hf_transfer modelscope

# --- shared library (editable) ---
uv pip install -e "$REPO_ROOT/common"

# --- Phase 4: RL stack (verl + runtime). flash-attn can be slow to build;
#     prefer a prebuilt wheel for your torch/CUDA/Python combo. ---
uv pip install verl ray vllm \
  || echo "NOTE: verl/vllm needs attention (Linux-only, version-sensitive) — see docs/setup.md"

echo "Done. Activate with: source $VENV/bin/activate"
