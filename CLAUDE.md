# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Umbrella repo for a **four-part RL-for-speech-multimodal-LLM** research series. It holds a shared
library (`common/`), docs, and env scripts; the four works are **separate GitHub repos** under
`projects/` (each its own git repo, gitignored by this umbrella).

| # | Work repo (under `projects/`) | Package | Focus |
|---|---|---|---|
| W1 | `speech-mllm-training-free-rl` | `training_free_rl` | gradient-free, reward-guided inference-time RL |
| W2 | `speech-mllm-efficient-rl-alignment` | `efficient_rl_alignment` | efficient GRPO/DPO (LoRA) for speech↔language alignment |
| W3 | `speech-mllm-multitask-rl` | `multitask_rl` | one policy, RL across ASR/ST/SID/SER via verifiable rewards |
| W4 | `speech-mllm-omni-embedding-rl` | `omni_embedding_rl` | RL over contrastive/retrieval objectives for omni embeddings |

## Environment (important)

- **Compute is WSL2 Ubuntu, not native Windows.** The RTX 5090 (Blackwell, sm_120) has no stable
  native-Windows torch wheels; verl/vLLM/flash-attn are Linux-only. All training runs in WSL2.
- **Python is pinned to 3.12** in a uv venv at `~/.venvs/speechrl` (ext4). The system Python 3.14 is
  too new for ML wheels — do not use it for the stack. **Never touch `D:/ai-stack/mem0-venv`** (the
  isolated mem0 MCP env from `.mcp.json`).
- torch from the `cu128` index; if a "no kernel image" error appears, fall back to torch nightly
  `cu128`, then a source build with `TORCH_CUDA_ARCH_LIST=12.0`.
- Datasets/checkpoints/outputs live in WSL ext4 (`~/speechrl-data/`), **never in git**.

## Common commands

Run inside WSL2 with the venv active (`source ~/.venvs/speechrl/bin/activate`):

```bash
# One-time env setup (from repo root)
bash scripts/wsl-setup.sh        # CUDA toolkit for WSL + uv
bash scripts/env-setup.sh        # py3.12 venv + torch cu128 + verl + editable common

# Work on a single study
cd projects/speech-mllm-training-free-rl
uv pip install -e ../../common -e .
bash scripts/train.sh                          # train (Hydra)
bash scripts/train.sh rl.learning_rate=2e-6    # override any Hydra key
bash scripts/eval.sh

# Tests
pytest common/tests                            # shared-lib smoke tests
pytest                                         # within a work repo

# Experiment tracking (local MLflow file store; no server/account)
bash scripts/mlflow-ui.sh                      # http://127.0.0.1:5000
```

Run a single test: `pytest common/tests/test_smoke.py::test_reward_normalization_exact_match -q`.

## Architecture notes (the big picture)

- **Shared library `speechrl_common`** (`common/src/speechrl_common/`): `audio` (load/resample,
  log-mel), `models` (Qwen2-Audio loader + per-task prompts), `rl` (verifiable reward fns: WER/ASR/
  exact-match — usable directly as GRPO/TRL reward callables), `data` (dataset registry), `tracking`
  (local-MLflow helper), `utils` (seed/logging/checkpoint).
- **Lazy-import discipline:** the package top level imports only light helpers; torch/transformers/
  librosa/mlflow/jiwer are imported *inside* the functions that use them. So `import speechrl_common`
  and its smoke tests pass even before the heavy stack is installed. **Preserve this** when adding code
  — keep heavy imports inside functions, not at module top level.
- **Each work depends on `common` via `[tool.uv.sources]`** editable path `../../common`. Work
  `pyproject.toml` deliberately omits torch/verl (those come from the WSL env so the cu128 index is
  used) — see comments there.
- **Config:** Hydra per work — `configs/config.yaml` composes `model/ dataset/ rl/ experiment/`.
- **RL library:** verl (GRPO/PPO with vLLM rollouts). Base model: Qwen2-Audio (swap SALMONN /
  Qwen2.5-Omni via `models/` + config).

## Gotchas

- **`gh` on PATH:** the real GitHub CLI is `C:\Program Files\GitHub CLI\gh.exe` (System PATH was
  reordered so `gh` resolves to it, ahead of a shadowing Python script at `C:\Python314\Scripts\gh`).
- **Line endings:** `.gitattributes` forces `eol=lf` (esp. `*.sh`) so scripts run in WSL — keep it.
- **Default branch is `master`** for the umbrella and all four work repos.
- **PYTHONPATH separator is `;` on Windows** Python (not `:`) when testing without an install.

## Research skills

A curated skill set is installed via the Windows Claude Code plugin marketplace (see
`docs/setup.md`): `academic-research-skills` (paper pipeline, `/ars-*`) + six `ai-research-skills`
groups (post-training, multimodal, fine-tuning, inference-serving, optimization, mlops). K-Dense
`scientific-agent-skills` is intentionally not installed.

## Shared knowledge & memory (README + Wiki)

- **Canonical onboarding is the root `README.md` / `README_CN.md`** — read it first.
- **Shared, durable team memory is the GitHub Wiki**, sourced from `wiki/` in this repo and published
  with `bash scripts/wiki-sync.sh`. Edit `wiki/*.md` (never only the web Wiki — it's a mirror that the
  sync script overwrites).
- **mem0 MCP is local/personal memory only** — not shared with the team. Promote anything the team
  needs into the Wiki.
- **Before starting:** read `wiki/Home.md` and `wiki/Per-Work-Status.md`. **After a notable decision
  or learning:** append a dated entry to `wiki/Decision-Log.md` (and update `wiki/Per-Work-Status.md`
  if a work's maturity/plan changed), then run `bash scripts/wiki-sync.sh`. Full protocol:
  `wiki/AI-Collaboration.md`.
