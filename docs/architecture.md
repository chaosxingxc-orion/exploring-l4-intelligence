# Architecture

## Repo model: umbrella + shared library + four independent repos

```
exploring-l4-intelligence (umbrella, this repo)
├─ common/        speechrl-common — shared library, editable-installed by each work
├─ projects/      the four work repos (each its OWN git repo; gitignored here)
├─ docs/          setup + architecture
└─ scripts/       WSL2 / env / mlflow helpers
```

The four works are **separate GitHub repos** (independent history/issues), but develop against
one shared `speechrl-common` package via `[tool.uv.sources]` editable path `../../common`.

| # | Repo | Focus |
|---|------|-------|
| W1 | `speech-mllm-training-free-rl` | gradient-free, reward-guided inference-time RL |
| W2 | `speech-mllm-efficient-rl-alignment` | efficient GRPO/DPO (LoRA) for speech↔language alignment |
| W3 | `speech-mllm-multitask-rl` | one policy, RL across ASR/ST/SID/SER via verifiable rewards |
| W4 | `speech-mllm-omni-embedding-rl` | RL over contrastive/retrieval objectives for omni embeddings |

## Shared library (`speechrl_common`)

- `audio` — load/resample (16 kHz mono), log-mel features
- `models` — Qwen2-Audio loader, prompt templates per speech task
- `rl` — verifiable reward functions (WER / ASR / exact-match) usable as GRPO/TRL callables
- `data` — dataset registry + data-root resolution
- `tracking` — local-MLflow run helper
- `utils` — seed, logging, checkpoint paths

**Import discipline:** the package top level pulls in only light helpers; heavy deps (torch,
transformers, librosa, mlflow, jiwer) are lazy-imported inside functions, so `import speechrl_common`
works before the full ML stack is installed.

## Conventions

- **Config:** Hydra per work (`configs/config.yaml` composing `model/ dataset/ rl/ experiment/`).
- **Tracking:** local MLflow file store (no server) under `~/speechrl-data/mlruns`.
- **RL library:** verl (Linux-only; runs in WSL2) for GRPO/PPO with vLLM rollouts.
- **Artifacts:** datasets/checkpoints/outputs live in WSL ext4 (`~/speechrl-data/`), never in git.
- **Base model:** Qwen2-Audio by default; swap SALMONN / Qwen2.5-Omni via `models/` + config.
