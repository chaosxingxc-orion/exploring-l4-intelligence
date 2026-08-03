# AGENTS.md

This file provides guidance to Codex (Codex.ai/code) when working with code in this repository.

## Repository

Umbrella governance repo for a research program on training-free, reward-guided inference-time control
of frozen speech/omni multimodal LLMs. The north star is `wiki/Project-Thesis.md`; current research
state is `wiki/Research-Objective.md`.

| Work | Repo under `projects/` | Package | Role |
|---|---|---|---|
| W1 | `speech-mllm-training-free-rl` | `training_free_rl` | Legacy/component work; not the program carrier |
| W2 | `speech-mllm-efficient-rl-alignment` | `efficient_rl_alignment` | Supporting skeleton |
| W3 | `speech-mllm-multitask-rl` | `multitask_rl` | Supporting skeleton |
| W4 | `speech-mllm-omni-embedding-rl` | `omni_embedding_rl` | Separate repositioned work |

The umbrella owns `common/`, `docs/`, `scripts/`, `studies/README.md`, `studies/registry.json`, `wiki/`,
and root Markdown. Each `projects/<work>/` is an independent Git repo and owns its code, configs, and
README. Each admitted research study is also an independent, semantically named Git repo checked out
under `studies/<study-name>/`; candidate IDs such as R1/R2 are audit provenance, never engineering repo
names. Study creation requires `OWNER_GO_AND_EXECUTION_CONTRACT`. See `CONTRIBUTING.md` and
`wiki/Experiment-Assets.md`.

## AI context routing

Default load surface is exactly:

1. this client guide;
2. `wiki/Research-Objective.md` — current stage, blockers, next action; then
3. `wiki/Project-Thesis.md` — north star.

Load `wiki/Per-Work-Status.md`, `wiki/Experiment-Assets.md`, and `wiki/survey/current/` only for a named
work, experiment, or survey task. Never broadly load
`wiki/20*.md`, historical proposal/review/response/amendment files, `wiki/archive/`, or the full
`wiki/Decision-Log.md`. For provenance, use a campaign index and targeted `rg` only.

Budgets: `AGENTS.md` / `CLAUDE.md` ≤12KB; `Research-Objective.md` ≤5KB;
`Per-Work-Status.md ≤8KB`; `survey/README.md ≤4KB`; `survey/current/README.md ≤4KB`; AI context
manifest ≤30 active entries. The three default entries are fixed.

Path summary: HOT current facts stay in stable root/wiki files; experiment lifecycle and asset routing
live in `wiki/Experiment-Assets.md` plus per-study `wiki/experiments/<study-name>/`; CURRENT survey
contracts live under `wiki/survey/current/`; long-lived paper records go to `wiki/survey/registry/`; reviewer transactions
are created directly under `wiki/audit/<campaign>/<round-id>/`; superseded unregistered work goes to
`wiki/archive/`; active exploration goes to `wiki/survey/workbench/<campaign>/`. Engineering specs,
plans, reports, and executable checks belong in `docs/superpowers/specs/`, `docs/superpowers/plans/`,
`docs/checks/<campaign>/<release-id>/`, and `scripts/` respectively.

The complete placement table, six-step lifecycle, consolidation triggers, safe-move gate, record
templates, and audit discipline are canonical only in `wiki/AI-Collaboration.md`. Do not reproduce
that full policy here. Active truth must be self-contained; amendment/response chains are cold audit,
not working context.

## Environment

- Compute is WSL2 `Ubuntu-24.04`; always target `wsl -d Ubuntu-24.04`. The default `Ubuntu` distro is
  WSL1 and has no GPU.
- Python is pinned to 3.12 in `~/.venvs/speechrl` on ext4. Do not use Windows/system Python 3.14 for
  the ML stack. Never touch `D:/ai-stack/mem0-venv`.
- Torch uses the `cu128` index for RTX 5090 (sm_120). If no compatible kernel exists, try nightly
  `cu128`, then source build with `TORCH_CUDA_ARCH_LIST=12.0`.
- Data/checkpoints/outputs live at
  `/mnt/e/chao_workspace/exploring-l4-intelligence/speechrl-data` (`SPEECHRL_DATA_DIR`); never commit
  them. Only local MLflow `mlruns` stays on ext4.
- `gh` is `C:\Program Files\GitHub CLI\gh.exe`. Windows `PYTHONPATH` uses `;`. `.gitattributes`
  enforces LF, especially for shell scripts. Existing umbrella/work repos use `master`; each admitted
  study records its remote and branch policy in its own repository.

## Commands

Run ML commands in WSL2 with `source ~/.venvs/speechrl/bin/activate`:

```bash
bash scripts/wsl-setup.sh
bash scripts/env-setup.sh

cd projects/speech-mllm-training-free-rl
uv pip install -e ../../common -e .
bash scripts/train.sh
bash scripts/eval.sh

pytest common/tests
pytest
```

Assets are frozen in `docs/datasets.lock.json` and live outside Git:

```bash
bash scripts/data/fetch-data.sh --list
bash scripts/data/fetch-data.sh
bash scripts/data/inventory.sh
```

There is currently no admitted study checkout. Do not create one from a conditional candidate. After
owner GO plus an execution contract, register the semantic repository in `studies/registry.json`; its
commands and environment lock belong to that independent repository.

The real umbrella gate is `python scripts/survey/sf_current_package_check.py --check` (runs offline on
Windows or WSL). The Stage‑1B program-level Lean formal layer is retired (2026-08-03); formal proofs
are rebuilt per admitted study in Stage‑2, scoped to that study's claims.

## Code and Git discipline

- `common/src/speechrl_common/` provides audio, model, reward, data, tracking, and utility helpers.
  Keep torch/transformers/librosa/mlflow/jiwer imports inside the functions that use them; package
  top-level imports remain light.
- Each work depends on `common` through editable `../../common`; torch/verl come from the shared WSL
  environment. Hydra config composes `model/`, `dataset/`, `rl/`, and `experiment/`.
- Preserve unrelated user changes. Use non-destructive Git operations. Commit each change in the repo
  that owns it; umbrella, work, and admitted-study repos have independent histories. Do not publish,
  push, create a remote study repo, or run non-dry wiki sync without explicit authorization.
- `CLAUDE.md` and `AGENTS.md` are mirrored except the client header/description/marketplace line.
- Git blob bytes are the evidence hash authority: use `git show <commit>:<path>` for historical
  evidence, not CRLF working-tree bytes.

## Research boundary

Never infer the current stage or execution authority from this guide; read `wiki/Research-Objective.md`.
A documentation/check repair does not authorize discovery queries, model calls, smoke tests, dataset
experiments, prototypes, reviewer signatures, or owner Stage-2A execution approval. Exposure claims
must state their scope and retain inherited prior exposure.

Stage-1A checks identity, routing, protocol coverage, and gate correctness; it does not judge technical
novelty or require a prior-difference matrix. Stage-1B maps method paths and proximity without a novelty
verdict. Stage-1C selects a problem from candidate gap hypotheses; technical-approach innovation
converges only in reproduction-first Stage-2A and is validated in Stage-2B.

Stage accounting is direction-local: once a semantically named research object closes its own survey,
owner decision, and execution contract, it may enter engineering while the next candidate is surveyed.
Completion of all candidate IDs is never a global Stage-2 prerequisite. Sunset candidates receive no
engineering repository.

After a durable decision, follow `wiki/AI-Collaboration.md`: write rationale before context is lost,
update the current layer in place, keep audit records append-only, run the relevant executable checks,
and archive eligible superseded work. Wiki source is the repository; the web wiki is a mirror.

## Research skills

Installed via the Windows Codex plugin marketplace (see `docs/setup.md`):
`academic-research-skills` (`/ars-*`), six `ai-research-skills` groups, and official
`lean@leanprover`. K-Dense, community lean4-skills, and lean-lsp-mcp are intentionally absent.
