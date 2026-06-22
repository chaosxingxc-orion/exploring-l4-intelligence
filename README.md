# L4级智能探索

> Repo slug: **`exploring-l4-intelligence`** · 探索迈向 L4 级（"创新者"）智能的路径。

Umbrella for a four-part research series on **reinforcement learning for speech multimodal LLMs**,
plus a shared library the four works build on.

## The series

| # | Work | Repo |
|---|------|------|
| W1 | Training-free RL for speech multimodal LLMs | [speech-mllm-training-free-rl](https://github.com/chaosxingxc-orion/speech-mllm-training-free-rl) |
| W2 | Efficient RL for multimodal alignment (speech↔language) | [speech-mllm-efficient-rl-alignment](https://github.com/chaosxingxc-orion/speech-mllm-efficient-rl-alignment) |
| W3 | RL for multi-task traditional speech tasks | [speech-mllm-multitask-rl](https://github.com/chaosxingxc-orion/speech-mllm-multitask-rl) |
| W4 | RL-based omni embedding models for speech tasks | [speech-mllm-omni-embedding-rl](https://github.com/chaosxingxc-orion/speech-mllm-omni-embedding-rl) |

Each is its own repo but shares [`common/`](common) (`speechrl-common`) via an editable install.

## Repo layout

```
common/      shared library (speechrl_common): audio, models, rl rewards, data, tracking, utils
projects/    the four work repos (each its own git repo; not tracked by this umbrella)
docs/        setup.md (WSL2 + env), architecture.md, data.md (downloads)
scripts/     wsl-setup.sh, env-setup.sh, mlflow-ui.sh, data/ (model+dataset downloads)
```

## Quick start

Compute runs in **WSL2** (RTX 5090 / Blackwell needs `cu128` torch — native Windows is unsupported).
See [docs/setup.md](docs/setup.md). In short, inside WSL2 Ubuntu:

```bash
bash scripts/wsl-setup.sh     # CUDA toolkit + uv
bash scripts/env-setup.sh     # Python 3.12 venv + torch cu128 + verl + common
source ~/.venvs/speechrl/bin/activate
```

Tracking: local MLflow (`bash scripts/mlflow-ui.sh`). Configs: Hydra. RL: verl.

## Data & models

Weights and datasets (~281 GB) are **not** in git — fetch your own copy locally:

```bash
bash scripts/data/probe-access.sh   # check reachability
bash scripts/data/fetch-data.sh     # download models + datasets
```

See [docs/data.md](docs/data.md) for the full asset list, mirrors, and per-asset targets.
