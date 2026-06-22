# Contributing

> **English** | [中文](CONTRIBUTING_CN.md)

This is an **umbrella repo plus four independent work repos**. The single most important rule is:
**commit each change to the repo it belongs to.**

## The five repos

- **`exploring-l4-intelligence`** (umbrella, this repo) — owns `common/`, `docs/`, `scripts/`,
  `wiki/`, and root `*.md`.
- **`projects/<work>/`** (W1–W4) — each is its **own git repo** (gitignored by the umbrella) with
  independent history, issues, and remote.

## Where changes go

| You changed… | Commit in… |
|---|---|
| `common/`, `docs/`, `scripts/`, `wiki/`, root README/CONTRIBUTING | the umbrella repo |
| a work's code / configs / `README.md` (under `projects/<work>/`) | that work's own repo |

A change is in the wrong place if `git status` in the umbrella shows files under `projects/` — those
belong to the work repo. (`projects/*/` is gitignored here precisely to prevent that.)

## Shared library (`common/`)

`speechrl-common` is editable-installed by all four works, so a change there ripples to W1–W4.

- Run `pytest common/tests` before committing — the smoke tests must pass.
- **Preserve lazy-import discipline:** keep torch/transformers/librosa/mlflow/jiwer imports *inside*
  functions so `import speechrl_common` stays cheap and the smoke tests pass pre-stack.
- Run a single test, e.g. `pytest common/tests/test_smoke.py::test_reward_normalization_exact_match -q`.

## Environment

All training runs in **WSL2** (see [docs/setup.md](docs/setup.md)). Use the shared py3.12 venv at
`~/.venvs/speechrl`. Never use system Python 3.14 for the stack; never touch `D:/ai-stack/mem0-venv`.

## Git conventions

- Default branch is **`master`** for all five repos; branch for non-trivial work and open a PR.
- Keep each commit/PR scoped to a single repo.
- `.gitattributes` forces `eol=lf` (especially `*.sh`) so scripts run in WSL — keep it.
- **Never commit data:** `speechrl-data/` and weight/dataset/archive formats are gitignored (~281 GB
  stays local). Fetch with `scripts/data/` (see [docs/data.md](docs/data.md)).
- `gh` resolves to `C:\Program Files\GitHub CLI\gh.exe`; on Windows Python the `PYTHONPATH` separator
  is `;`.

## Knowledge & memory

Record durable decisions/learnings in the Wiki's `wiki/Decision-Log.md`, update
`wiki/Per-Work-Status.md` when a work's state changes, and publish with `bash scripts/wiki-sync.sh`.
See the Wiki's [Working-Mode](https://github.com/chaosxingxc-orion/exploring-l4-intelligence/wiki/Working-Mode)
and [AI-Collaboration](https://github.com/chaosxingxc-orion/exploring-l4-intelligence/wiki/AI-Collaboration).
