# Exploring L4 Intelligence

> **English** | [中文](README_CN.md)
>
> Repo slug: **`exploring-l4-intelligence`** — charting a path toward L4 ("Innovator") intelligence.

The **umbrella governance repo** for a research program on **training-free, reward-guided
inference-time control of frozen speech / omni multimodal LLMs** — an external reward-guided control
plane around an **API-only frozen speech/omni core**, changing no base-model weights and no
base-model structure. Full statement of purpose: the Wiki's [[Project-Thesis]] page; current
research state: [[Research-Objective]].

> 📖 **Start here.** This README is the canonical entry point for humans **and** their AI
> assistants. Deeper docs live in [`docs/`](docs); program truth lives in the Wiki source under
> [`wiki/`](wiki).

## Program model

**Stage‑1 in the umbrella, Stage‑2 in an independent study repo.** Every new research topic runs its
detailed discussion, survey and justification here (Wiki survey layers, audit rounds, owner
decisions). When a direction passes Stage‑1 and the owner signs `OWNER_GO_AND_EXECUTION_CONTRACT`,
it becomes an **independent, semantically named GitHub repository** checked out under
`studies/<semantic-name>/` — and all later engineering, experiments and papers live there.
Candidate IDs (R1, R2, …) are survey/audit provenance, never repository names.

The umbrella permanently keeps the **shared-asset functions**: data & model acquisition
(`docs/datasets.lock.json` is the single live asset authority, tooling in `scripts/data/`),
baseline identity records, literature/survey infrastructure, runtime pins, and the governance
gates. Datasets are immutable gold truth; how a study uses them (splits, sampling, prompts,
protocols) is that study's private scheme — a split published with a paper crystallizes into a new
promoted dataset (derivation script + sample identity + provenance) back in the umbrella.

## Admitted studies

| Study (repo) | Provenance | Opened | State |
|---|---|---|---|
| [audio-aware-evidence-acquisition](https://github.com/chaosxingxc-orion/audio-aware-evidence-acquisition) | R2, campaign system-first-stage1c-v2 | GO 2026-08-03 | Stage‑2A E0 (model-free data gates) in progress |

Registry: [`studies/registry.json`](studies/registry.json); per-study experiment ledger:
`wiki/experiments/<slug>/`. The historical W1–W4 work repos were retired on 2026-08-03 — local
checkouts deleted, remotes kept as cold backups outside the program
(tombstone: `wiki/archive/program/w1-w4-retirement/`).

## Repo layout

```
common/         shared library (speechrl_common): audio, models, rewards, data, tracking, utils
studies/        registry + local root for admitted semantic study repos (each its OWN git repo)
docs/           setup.md, datasets.lock.json (asset authority), superpowers/specs, checks, integrity
scripts/        wsl-setup.sh, env-setup.sh, wiki-sync.sh, data/ (downloads), checks/ + survey/ (gates)
wiki/           source for the GitHub Wiki — program truth, survey layers, audit, experiment ledgers
speechrl-data/  data root (hundreds of GB, E: drive, gitignored; /mnt/e/… from WSL)
CLAUDE.md / AGENTS.md   per-tool operating guides for AI assistants (Claude Code / Codex)
CONTRIBUTING.md         repository ownership and multi-repo workflow
```

## Environment

**Compute is WSL2 `Ubuntu-24.04`, not native Windows** (default `Ubuntu` = WSL1, no GPU). Python is
pinned to **3.12** (uv venv at `~/.venvs/speechrl`, on ext4); torch comes from the `cu128` index
for the RTX 5090 (sm_120). Inference for the frozen 30B omni core runs through a resident
llama.cpp `llama-server` (GGUF). Full details: [docs/setup.md](docs/setup.md).

## Quick start

```bash
# umbrella governance gates (offline, Windows or WSL)
python scripts/checks/code_graph_check.py
python scripts/checks/study_workspace_check.py
python scripts/checks/ai_context_surface_check.py
python scripts/checks/build_ai_context_manifest.py --check

# work on the admitted study (inside WSL2, venv active)
cd studies/audio-aware-evidence-acquisition
uv pip install -e ../../common -e .
pytest
```

An admitted study owns its run commands, configs and locks; see its own `README.md` and the
execution contract in `wiki/experiments/<slug>/`.

## Data & models

Weights and datasets are **never in git**. `docs/datasets.lock.json` is the only live source for
asset identity, lifecycle, acquisition state and verification:

```bash
bash scripts/data/fetch-assets.sh    # lock-driven fetch (named profiles; writes receipts)
bash scripts/data/inventory.sh       # audit COMPLETE / PARTIAL / MISSING
```

See [docs/data.md](docs/data.md) and `scripts/data/README.md`.

## For AI assistants

Read the repo through this layering, in order:

1. **[CLAUDE.md](CLAUDE.md) / [AGENTS.md](AGENTS.md)** — the client operating guide;
2. **[[Research-Objective]]** — current stage, authority and next action;
3. **[[Project-Thesis]]** — the program north star.

Load the literature commons (`wiki/survey/README.md`), `wiki/Experiment-Assets.md` and per-study
ledgers only for a named task. Record durable decisions in [[Decision-Log]]; the web wiki is a mirror published by
`scripts/wiki-sync.sh` only when authorized. Full protocol: [[AI-Collaboration]].

## Docs index

| | |
|---|---|
| [docs/setup.md](docs/setup.md) | WSL2 + CUDA + py3.12 venv + torch cu128 |
| [docs/architecture.md](docs/architecture.md) | umbrella governance + independent semantic study repos |
| [docs/data.md](docs/data.md) | models, datasets, mirrors, fetch scripts |
| [common/README.md](common/README.md) | `speechrl_common` module map & install |
| [CONTRIBUTING.md](CONTRIBUTING.md) | multi-repo workflow & conventions |
| [Wiki](https://github.com/chaosxingxc-orion/exploring-l4-intelligence/wiki) ([`wiki/`](wiki)) | program truth: research state, survey layers, audit, experiment ledgers |
