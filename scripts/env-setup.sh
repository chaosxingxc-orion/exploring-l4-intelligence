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

# --- core science + speech + tracking + probes/metrics ---
# sentence-transformers: the frozen omni-embedder loader (Operator A); scikit-learn: linear/kNN probes
# (rl.probe, the verifiable disentanglement reward); sacrebleu: BLEU/chrF (rl.metrics, ST).
uv pip install transformers datasets accelerate peft \
               sentence-transformers scikit-learn sacrebleu \
               librosa soundfile jiwer \
               hydra-core omegaconf mlflow ruff pytest

# --- data-download CLIs (needed by scripts/data/fetch-data.sh): HF Hub CLI + fast transfer,
#     and ModelScope (some models/datasets are ModelScope-only). aria2 comes from wsl-setup.sh. ---
uv pip install huggingface_hub hf_transfer modelscope

# --- shared library (editable) ---
uv pip install -e "$REPO_ROOT/common"

# --- Phase 4: RL stack (verl + runtime). flash-attn can be slow to build;
#     prefer a prebuilt wheel for your torch/CUDA/Python combo. ---
uv pip install verl ray vllm \
  || echo "NOTE: verl/vllm needs attention (Linux-only, version-sensitive) — see docs/setup.md"

# --- Phase 5: LoRA/QLoRA + local GGUF inference toolchain (one-time; covers the full lifecycle:
#     W1 best-of-N, local 30B inference on 24GB, W2 LoRA-RL, AND post-fine-tune deployment) ---
# bitsandbytes: 4-bit (QLoRA) base for verl LoRA-RL under tight VRAM.
uv pip install bitsandbytes
# cmake + ninja as pip wheels (no sudo / apt needed) to build llama.cpp.
uv pip install cmake ninja
# llama.cpp with CUDA (Blackwell sm_120; pin CUDA 12.8 to match torch cu128 — CUDA toolkit comes from
# wsl-setup.sh, default symlink may point at 13.x). One build serves every downstream need:
#   - llama-mtmd-cli / llama-server : omni audio inference + `--n-cpu-moe` expert offload (30B on 24GB)
#   - convert_hf_to_gguf.py + convert_lora_to_gguf.py : post-fine-tune GGUF export (merge path & adapter path)
LLAMACPP_DIR="${LLAMACPP_DIR:-$HOME/llama.cpp}"
CUDA_128="${SPEECHRL_CUDA_HOME:-/usr/local/cuda-12.8}"
# Pinned 2026-07-09: this is the exact commit behind the resident Qwen3-Omni llama-server build
# (verified via `git -C ~/llama.cpp rev-parse HEAD` on the WSL2 box). A shallow `--depth 1` clone of
# `main` is not reproducible — main moves; pin then checkout so a fresh env-setup.sh run reconstructs
# the SAME llama.cpp the resident build/results were produced with. Bump this SHA deliberately (with a
# dated comment) when intentionally moving to a newer llama.cpp, not as a side effect of a rerun.
LLAMACPP_COMMIT="${LLAMACPP_COMMIT:-fdbd6abee20e408de21e90ca77a24cd50a6ea073}"  # 2026-06-25, "tests: synchronize contexts at end of test-thread-safety (#24935)"
if [ ! -d "$LLAMACPP_DIR/.git" ]; then
  git clone https://github.com/ggml-org/llama.cpp "$LLAMACPP_DIR"
  git -C "$LLAMACPP_DIR" checkout "$LLAMACPP_COMMIT"
fi
cmake -S "$LLAMACPP_DIR" -B "$LLAMACPP_DIR/build" -G Ninja \
      -DGGML_CUDA=ON -DCMAKE_CUDA_COMPILER="$CUDA_128/bin/nvcc" \
      -DCMAKE_CUDA_ARCHITECTURES=120 -DLLAMA_CURL=OFF \
  && cmake --build "$LLAMACPP_DIR/build" -j 6 \
  || echo "NOTE: llama.cpp build needs attention — see wiki/Inference-Engine-Choice.md"

echo "Done. Activate with: source $VENV/bin/activate"
