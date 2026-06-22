# Setup & reproduction

The compute environment is **WSL2 Ubuntu** (native Windows torch does not support the
RTX 5090 / Blackwell sm_120 in stable wheels). The system Python 3.14 and
`D:/ai-stack/mem0-venv` are left untouched.

## 1. WSL2 + CUDA (Phase 1)

WSL2 v2.6.3 is installed; ensure a **WSL2** Ubuntu distro (convert a WSL1 one or install fresh):

```powershell
wsl -l -v                          # check VERSION column
wsl --set-version Ubuntu 2         # if it shows 1
# or: wsl --install -d Ubuntu-24.04
```

Then inside Ubuntu — set `REPO` to where the umbrella repo lives in WSL (later steps reuse `$REPO`):

```bash
# New folder name after the rename; until you rename the local folder, use the old name here.
export REPO="/mnt/d/chao_workspace/exploring-l4-intelligence"
bash "$REPO/scripts/wsl-setup.sh"
nvidia-smi        # must list the RTX 5090
nvcc --version    # CUDA 12.8+
```

## 2. Python env + torch + RL stack (Phases 2 & 4)

```bash
bash "$REPO/scripts/env-setup.sh"
source ~/.venvs/speechrl/bin/activate
python -c "import torch; print(torch.__version__, torch.cuda.get_device_name(0))"
```

- venv lives in ext4 (`~/.venvs/speechrl`); datasets/checkpoints/mlruns in `~/speechrl-data/`.
- torch comes from the `cu128` index; **verl/vLLM/flash-attn are Linux-only** and version-sensitive
  — if `verl`/`vllm` fail, pin versions and prefer a prebuilt `flash-attn` wheel for your
  torch/CUDA/Python combo.
- Fallback if a "no kernel image" CUDA error appears: torch nightly `cu128`, then a source build
  with `TORCH_CUDA_ARCH_LIST=12.0`.

## 3. Working on a single work

```bash
cd "$REPO/projects/speech-mllm-training-free-rl"
uv pip install -e ../../common -e .
bash scripts/train.sh                       # Hydra config in configs/
bash scripts/train.sh rl.learning_rate=2e-6 # override any key
```

## 4. Experiment tracking (local MLflow)

```bash
bash "$REPO/scripts/mlflow-ui.sh"   # http://127.0.0.1:5000
```

## 5. Research skills (run in the Windows Claude Code session)

Installed via the plugin marketplace (namespaced, no collisions). Curated set:

```text
/plugin marketplace add Imbad0202/academic-research-skills
/plugin install academic-research-skills

/plugin marketplace add orchestra-research/ai-research-skills
/plugin install post-training@ai-research-skills
/plugin install multimodal@ai-research-skills
/plugin install fine-tuning@ai-research-skills
/plugin install inference-serving@ai-research-skills
/plugin install optimization@ai-research-skills
/plugin install mlops@ai-research-skills

# Lean 4 formal proof — official leanprover skills (invoked as lean:* ; host-agnostic)
/plugin marketplace add leanprover/skills
/plugin install lean@leanprover
```

K-Dense `scientific-agent-skills` is intentionally skipped (bio/chem-heavy, irrelevant, and the
only hard-collision source). Optional later add-ons: `distributed-training`, `model-architecture`,
`evaluation`, `emerging-techniques`.

For **Lean formal proof** we align on the official `lean@leanprover` set only (`lean:lean-proof`,
`lean:lean-setup`, `lean:mathlib-build`, `lean:mathlib-pr`/`lean:mathlib-review`, plus
bisect/mwe/pr/nightly helpers); the community `cameronfreer/lean4-skills` pack and the `lean-lsp-mcp`
server are intentionally deferred to keep the footprint light.
