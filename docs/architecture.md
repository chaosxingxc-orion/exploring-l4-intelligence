# Architecture

## Thesis

This series uses **training-free RL** — reward-guided, inference-time optimization that changes no
weights and no structure — to activate the pretrained knowledge of speech / omni LLMs. The flagship
study **W4** disentangles a frozen omni model's speech embeddings across content/ASR+ST, speaker-ID,
emotion/SER, and language+intent. Full statement: the Wiki's Project-Thesis page (`wiki/Project-Thesis.md`).

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

| # | Repo | Role | Focus |
|---|------|------|-------|
| **W4** | `speech-mllm-omni-embedding-rl` | **Flagship** | training-free RL to disentangle a frozen omni model's embeddings (content/ASR+ST, speaker-ID, emotion/SER, language+intent) |
| **W1** | `speech-mllm-training-free-rl` | **Pattern reference** | mature training-free reward/eval machinery W4 reuses |
| W2 | `speech-mllm-efficient-rl-alignment` | Supporting | efficient GRPO/DPO (LoRA) for speech↔language alignment |
| W3 | `speech-mllm-multitask-rl` | Supporting | one policy, RL across ASR/ST/SID/SER via verifiable rewards |

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
