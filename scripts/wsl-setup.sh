#!/usr/bin/env bash
# Phase 1 — run INSIDE WSL2 Ubuntu. Installs build tools, the CUDA toolkit for WSL,
# and uv. The NVIDIA *driver* comes from Windows (do NOT install a Linux driver).
set -euo pipefail

sudo apt-get update
# build tools + git + aria2 (fast multi-connection downloader for HF/SLURP) + jq (hfd JSON parsing)
sudo apt-get install -y build-essential git curl ca-certificates wget aria2 jq

# CUDA toolkit for WSL-Ubuntu. Blackwell (RTX 5090, sm_120) needs >= 12.8.
# Adjust 'distro' to match your Ubuntu version (ubuntu2404 / ubuntu2204).
distro=ubuntu2404
wget -qO /tmp/cuda-keyring.deb \
  "https://developer.download.nvidia.com/compute/cuda/repos/${distro}/x86_64/cuda-keyring_1.1-1_all.deb"
sudo dpkg -i /tmp/cuda-keyring.deb
sudo apt-get update
sudo apt-get install -y cuda-toolkit-12-8

# uv (fast Python/venv manager)
curl -LsSf https://astral.sh/uv/install.sh | sh

echo
echo "Verify:"
echo "  nvidia-smi          # should list the RTX 5090"
echo "  nvcc --version      # should report CUDA 12.8+"
echo "  ~/.local/bin/uv --version"
