# Exploring L4 Intelligence

> **English** | [中文](README_CN.md)
>
> Repo slug: **`exploring-l4-intelligence`** — charting a path toward L4 ("Innovator") intelligence.

The **umbrella repo** for a four-part research series on **training-free RL to activate the
pretrained knowledge of speech / omni multimodal LLMs** — reward-guided, inference-time optimization
that changes **no base-model weights and no base-model structure** (external system components are
added) — plus a shared library all four works build on. The **current primary study (W1)** builds an
**external reward-guided control plane around an API-only frozen speech/omni core** (system-level
in-context control over knowledge, memory, skills and evidence state; Stage-1C direction
confirmation in progress — see the Wiki's Research-Objective page); W4 is a separate work on the
frozen omni's own embedding space (repositioned 2026-07-12 per the owner-signed G0 ruling). Full
statement of purpose: the Wiki's [[Project-Thesis]] page.

> 📖 **Start here.** This README is the single canonical entry point for humans **and** their AI
> assistants. Deeper docs live in [`docs/`](docs); shared team knowledge & "memory" live in the
> **[GitHub Wiki](https://github.com/chaosxingxc-orion/exploring-l4-intelligence/wiki)** (sourced
> from [`wiki/`](wiki)).

## The series

Each work is its **own GitHub repo** (independent history/issues) but develops against one shared
[`common/`](common) (`speechrl-common`) via an editable install.

| # | Work (repo) | Role | Focus | Status |
|---|---|---|---|---|
| **W1** | [speech-mllm-training-free-rl](https://github.com/chaosxingxc-orion/speech-mllm-training-free-rl) | **Primary study** | external reward-guided control plane around an API-only frozen omni core (knowledge/memory/skills/evidence-state); Stage-1C direction confirmation, first Stage-2A slice = R5+R6+R8 | 🟢 Mature · primary |
| W4 | [speech-mllm-omni-embedding-rl](https://github.com/chaosxingxc-orion/speech-mllm-omni-embedding-rl) | Separate work (repositioned 2026-07-12) | frozen omni embedding utility (L0/L1); fresh proposal pending (#29); former disentanglement-flagship framing superseded | 🟡 Skeleton → repositioning |
| W2 | [speech-mllm-efficient-rl-alignment](https://github.com/chaosxingxc-orion/speech-mllm-efficient-rl-alignment) | Supporting | efficient GRPO/DPO (LoRA) for speech↔language alignment | 🟡 Skeleton |
| W3 | [speech-mllm-multitask-rl](https://github.com/chaosxingxc-orion/speech-mllm-multitask-rl) | Supporting | one policy, RL across ASR/ST/SID/SER via verifiable rewards | 🟡 Skeleton |

**W1 carries the current primary study; W4 is a separate, repositioned work** (2026-07-12 — see
[[Decision-Log]] 续24 and the Thesis supersession note). W1's mature structure and scripts remain the
pattern to mirror when growing W2–W4. Live per-work
progress is on the Wiki's [[Per-Work-Status]] page; the project's purpose is on [[Project-Thesis]].

## Repo layout

```
common/         shared library (speechrl_common): audio, models, rl rewards, data, tracking, utils
projects/       the four work repos (each its OWN git repo; gitignored by this umbrella)
docs/           setup.md (WSL2 + env), architecture.md, data.md (downloads)
scripts/        wsl-setup.sh, env-setup.sh, mlflow-ui.sh, wiki-sync.sh, data/ (model+dataset downloads)
wiki/           source for the GitHub Wiki — shared knowledge & memory (push via scripts/wiki-sync.sh)
speechrl-data/  data root (~650 GB models/datasets) — on the E: drive, gitignored; /mnt/e/… from WSL
CLAUDE.md / AGENTS.md   per-tool operating guides for AI assistants (Claude Code / Codex)
CONTRIBUTING.md         how to work across the five repos
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

# work on a single study
cd projects/speech-mllm-training-free-rl
uv pip install -e ../../common -e .
bash scripts/train.sh                          # train (Hydra)
bash scripts/train.sh rl.learning_rate=2e-6    # override any Hydra key
bash scripts/eval.sh
```

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

Five repos (umbrella + four works): **commit each change where it belongs** — `common/`, `docs/`,
`scripts/`, `wiki/` go to this umbrella; a work's code (including its README) goes to **that work's
own repo** (they're gitignored here). Default branch is `master`. Changes to `common/` ripple to
W1–W4 — run `pytest common/tests`. Full conventions: [CONTRIBUTING.md](CONTRIBUTING.md) and the
Wiki's [[Working-Mode]].

## For AI assistants

If you are an AI assistant (Claude Code / Codex, etc.), read the repo through this layering:

1. **this README** — canonical onboarding.
2. **[[Project-Thesis]]** (Wiki) — the project's purpose, the three core terms, and the flagship claim; read right after this.
3. **[CLAUDE.md](CLAUDE.md) / [AGENTS.md](AGENTS.md)** — your per-tool operating guide (commands, gotchas, discipline).
4. **[GitHub Wiki](https://github.com/chaosxingxc-orion/exploring-l4-intelligence/wiki)** (source in [`wiki/`](wiki)) — shared, evolving team knowledge & memory.
5. **mem0 MCP** — local, personal memory — *not* shared with the team.

Rule of thumb: **before starting**, read the Wiki's [[Home]] and [[Per-Work-Status]]; when you make a
notable decision or learn something durable, **write it back** to the Wiki's [[Decision-Log]] and
publish via `bash scripts/wiki-sync.sh`. This is how every human and their AI stay on one consistent
understanding. See [[AI-Collaboration]] for the full protocol.

## Docs index

| | |
|---|---|
| [docs/setup.md](docs/setup.md) | WSL2 + CUDA + py3.12 venv + torch cu128 + verl |
| [docs/architecture.md](docs/architecture.md) | umbrella + shared lib + four-repo model |
| [docs/data.md](docs/data.md) | models, datasets, mirrors, fetch scripts |
| [common/README.md](common/README.md) | `speechrl_common` module map & install |
| [CONTRIBUTING.md](CONTRIBUTING.md) | multi-repo workflow & conventions |
| [Wiki](https://github.com/chaosxingxc-orion/exploring-l4-intelligence/wiki) ([`wiki/`](wiki)) | shared knowledge & memory (Architecture, Working-Mode, Per-Work-Status, AI-Collaboration, Decision-Log, Onboarding) |
