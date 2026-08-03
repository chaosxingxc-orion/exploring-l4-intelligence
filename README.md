# Exploring L4 Intelligence

> **English** | [中文](README_CN.md)
>
> Repo slug: **`exploring-l4-intelligence`** — charting a path toward L4 ("Innovator") intelligence.

The **umbrella governance repo** for a research program on **training-free RL to activate the
pretrained knowledge of speech / omni multimodal LLMs** — reward-guided, inference-time optimization
that changes **no base-model weights and no base-model structure** (external system components are
added). The program studies an **external reward-guided control plane around an API-only frozen
speech/omni core**. Candidate direction IDs are survey provenance only; after a direction receives
owner GO and an execution contract, it gets an independently versioned, semantically named study
repository under `studies/`. W1–W4 remain separate work repositories and do not own the primary
program. Full statement of purpose: the Wiki's [[Project-Thesis]] page.

> 📖 **Start here.** This README is the single canonical entry point for humans **and** their AI
> assistants. Deeper docs live in [`docs/`](docs); shared team knowledge & "memory" live in the
> **[GitHub Wiki](https://github.com/chaosxingxc-orion/exploring-l4-intelligence/wiki)** (sourced
> from [`wiki/`](wiki)).

## Program repositories

The umbrella owns governance, Wiki truth, study registration and stable shared infrastructure. W1–W4
remain independent GitHub work repositories. Each admitted research object becomes another independent
GitHub repository checked out under `studies/<semantic-name>/`.

| # | Work (repo) | Role | Focus | Status |
|---|---|---|---|---|
| W1 | [speech-mllm-training-free-rl](https://github.com/chaosxingxc-orion/speech-mllm-training-free-rl) | Legacy/component work | mature selector/evaluator and training-free-RL evidence; not the program carrier | 🟢 Mature evidence |
| W4 | [speech-mllm-omni-embedding-rl](https://github.com/chaosxingxc-orion/speech-mllm-omni-embedding-rl) | Separate work (repositioned 2026-07-12) | frozen omni embedding utility (L0/L1); fresh proposal pending (#29); former disentanglement-flagship framing superseded | 🟡 Skeleton → repositioning |
| W2 | [speech-mllm-efficient-rl-alignment](https://github.com/chaosxingxc-orion/speech-mllm-efficient-rl-alignment) | Supporting | efficient GRPO/DPO (LoRA) for speech↔language alignment | 🟡 Skeleton |
| W3 | [speech-mllm-multitask-rl](https://github.com/chaosxingxc-orion/speech-mllm-multitask-rl) | Supporting | one policy, RL across ASR/ST/SID/SER via verifiable rewards | 🟡 Skeleton |

No study repository is admitted yet. The first planned semantic object, audio-aware evidence
acquisition, has passed Stage-1C and formal opening; its owner Stage-2A execution contract remains
unsigned. Candidate R1 sunset before admission and therefore has no empty engineering repository.
Repository state and experiment assets are routed by [[Experiment-Assets]].

## Repo layout

```
common/         shared library (speechrl_common): audio, models, rl rewards, data, tracking, utils
projects/       the four work repos (each its OWN git repo; gitignored by this umbrella)
studies/        registry + local root for admitted semantic study repos (each its OWN git repo)
docs/           setup.md (WSL2 + env), architecture.md, data.md (downloads), integrity/check assets
scripts/        wsl-setup.sh, env-setup.sh, mlflow-ui.sh, wiki-sync.sh, data/ (model+dataset downloads)
wiki/           source for the GitHub Wiki — program truth and experiment asset control plane
speechrl-data/  data root (~650 GB models/datasets) — on the E: drive, gitignored; /mnt/e/… from WSL
CLAUDE.md / AGENTS.md   per-tool operating guides for AI assistants (Claude Code / Codex)
CONTRIBUTING.md         repository ownership and multi-repo workflow
```

## Environment

**Compute is WSL2 `Ubuntu-24.04`, not native Windows** (default `Ubuntu` = WSL1, no GPU). The RTX 5090 (Blackwell, sm_120) has no stable
native-Windows torch wheels; verl/vLLM/flash-attn are Linux-only — all training runs in WSL2. Python
is pinned to **3.12** (uv venv at `~/.venvs/speechrl`, on ext4); torch comes from the `cu128` index.
**Never touch `D:/ai-stack/mem0-venv`** (the isolated mem0 MCP env in `.mcp.json`). Full details:
[docs/setup.md](docs/setup.md).

## Quick start

Inside **WSL2 Ubuntu** (full guide in [docs/setup.md](docs/setup.md)):

```bash
bash scripts/wsl-setup.sh     # one-time: CUDA toolkit for WSL + uv
bash scripts/env-setup.sh     # py3.12 venv + torch cu128 + verl + editable common
source ~/.venvs/speechrl/bin/activate

# work on an existing W1–W4 repository
cd projects/speech-mllm-training-free-rl
uv pip install -e ../../common -e .
bash scripts/train.sh                          # train (Hydra)
bash scripts/train.sh rl.learning_rate=2e-6    # override any Hydra key
bash scripts/eval.sh
```

An admitted study keeps its own install/run commands and lockfiles. Do not scaffold one from a
conditional candidate; first close the owner GO and execution-contract gate and update
`studies/registry.json`.

Tracking: local MLflow (`bash scripts/mlflow-ui.sh` → http://127.0.0.1:5000; file store, no
server/account). Config: Hydra per work. RL library: verl.

## Data & models

Weights and datasets (~440 GB) are **never in git** — fetch your own copy locally (`.gitignore`
guards `speechrl-data/` so a stray `git add` can't push data):

```bash
bash scripts/data/probe-access.sh   # read-only: check HF/ModelScope reachability
bash scripts/data/fetch-data.sh     # download models + datasets (skips complete assets)
bash scripts/data/inventory.sh      # audit COMPLETE / PARTIAL / MISSING
```

Full asset list, mirrors (hf-mirror + ModelScope), and per-asset targets: [docs/data.md](docs/data.md).

## Working mode

This is a multi-repository workspace: **commit each change where it belongs**. Umbrella governance,
Wiki, shared utilities and the study registry go to this repo; W1–W4 code goes to the corresponding
`projects/` repo; admitted study code goes to its independent `studies/` repo. Large experiment assets
stay outside Git and are indexed from [[Experiment-Assets]]. Full conventions:
[CONTRIBUTING.md](CONTRIBUTING.md).

## For AI assistants

If you are an AI assistant (Claude Code / Codex, etc.), read the repo through this layering:

1. **[CLAUDE.md](CLAUDE.md) / [AGENTS.md](AGENTS.md)** — the client operating guide.
2. **[[Research-Objective]]** — current stage, authority and next action.
3. **[[Project-Thesis]]** — the program north star.
4. **[[Experiment-Assets]]** — targeted entry for study repositories and experiments.
5. **mem0 MCP** — local, personal memory; not shared team authority.

Rule of thumb: **before starting**, read the Wiki's [[Home]] and [[Per-Work-Status]]; when you make a
notable decision or learn something durable, **write it back** to the Wiki's [[Decision-Log]] and
publish via `bash scripts/wiki-sync.sh`. This is how every human and their AI stay on one consistent
understanding. See [[AI-Collaboration]] for the full protocol.

## Docs index

| | |
|---|---|
| [docs/setup.md](docs/setup.md) | WSL2 + CUDA + py3.12 venv + torch cu128 + verl |
| [docs/architecture.md](docs/architecture.md) | umbrella governance + work repos + independent semantic study repos |
| [docs/data.md](docs/data.md) | models, datasets, mirrors, fetch scripts |
| [common/README.md](common/README.md) | `speechrl_common` module map & install |
| [CONTRIBUTING.md](CONTRIBUTING.md) | multi-repo workflow & conventions |
| [Wiki](https://github.com/chaosxingxc-orion/exploring-l4-intelligence/wiki) ([`wiki/`](wiki)) | shared knowledge & memory (Architecture, Working-Mode, Per-Work-Status, AI-Collaboration, Decision-Log, Onboarding) |
