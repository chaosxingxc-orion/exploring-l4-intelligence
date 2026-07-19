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
- **Never commit data:** `speechrl-data/` and weight/dataset/archive formats are gitignored (~440 GB
  stays local). Fetch with `scripts/data/` (see [docs/data.md](docs/data.md)).
- `gh` resolves to `C:\Program Files\GitHub CLI\gh.exe`; on Windows Python the `PYTHONPATH` separator
  is `;`.

## Documentation routing

Choose the document role before creating the file:

| New material | Put it in |
|---|---|
| current survey protocol, status, table, schema, or manifest | `wiki/survey/current/` |
| long-lived paper census, claim, or evidence record | `wiki/survey/registry/` |
| reviewer submission/report/response/sign-off | `wiki/audit/<campaign>/<round-id>/` |
| new amendment/correction | `wiki/audit/<campaign>/epoch-<N>/<round-id>/<name>-<ordinal>.md` plus registered `epoch-<N>/consolidation-receipt.json`; the path-pinned B8 correction is the only unnumbered exception |
| superseded, unregistered working artifact | `wiki/archive/<knowledge-layer>/<campaign>/` after the safe-move gate |
| mutable campaign exploration or dossier | `wiki/survey/workbench/<campaign>/` |
| engineering design / execution plan | `docs/superpowers/specs/` / `docs/superpowers/plans/` |
| release-scoped reproducibility report | `docs/checks/<campaign>/<release-id>/` |
| executable policy or validation | `scripts/` with tests |
| temporary reasoning or scratch | do not commit; promote only distilled conclusions |

Current truth uses stable HOT/CURRENT files; audit and archive files are cold. Consolidate before a
fourth numbered amendment/correction: ordinal 4 is invalid, so a completed consolidation starts the
next epoch at ordinal 1. Epochs and ordinals are unique and continuous. Artifact front matter and the
receipt use the exact schemas in `wiki/AI-Collaboration.md`; both are registered, blob-pinned AUDIT
records. Commit and append-register the immutable receipt, and advance the reviewed registry-prefix
count/hash anchor, before opening a new epoch. The highest receipt binds the current-manifest protocol
version and staged SHA. The full lifecycle triggers are in `wiki/AI-Collaboration.md`.
Every audit-registry append atomically stages the registry, the full-prefix count/hash anchor in
`scripts/checks/ai_context_inventory.py`, and the regenerated immutability report before commit.
Before moving a
file, prove it is absent from the audit registry/current manifest, has no live inbound dependency,
and preserves its stage-0 Git blob and mode with `git mv`. The complete placement and lifecycle policy
is canonical in `wiki/AI-Collaboration.md`; this table is only a route summary.

Record durable decisions with rationale in the repository Wiki. Run the applicable checks before
commit. `scripts/wiki-sync.sh` publishes the repository source to the web mirror only when publication
is authorized.
