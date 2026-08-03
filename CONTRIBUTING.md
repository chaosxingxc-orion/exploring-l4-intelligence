# Contributing

> **English** | [中文](CONTRIBUTING_CN.md)

This is an **umbrella governance repo plus independent work and admitted-study repos**. The single most important rule is:
**commit each change to the repo it belongs to.**

## Repository classes

- **`exploring-l4-intelligence`** (umbrella, this repo) — owns `common/`, `docs/`, `scripts/`,
  `wiki/`, `studies/README.md`, `studies/registry.json`, and root `*.md`.
- **`studies/<semantic-study>/`** — each owner-admitted research object is its **own Git/GitHub repo**,
  checked out under the umbrella workspace but gitignored by it. Creation requires
  `OWNER_GO_AND_EXECUTION_CONTRACT`; Stage-1 candidate IDs never become repository names.

## Where changes go

| You changed… | Commit in… |
|---|---|
| `common/`, `docs/`, `scripts/`, `wiki/`, root README/CONTRIBUTING | the umbrella repo |
| `studies/README.md` or `studies/registry.json` | the umbrella repo |
| an admitted study's code / configs / `README.md` (under `studies/<semantic-study>/`) | that study's own repo |

A nested-repository code change is in the wrong place if umbrella `git status` shows it under a
study checkout; that container is ignored by the umbrella. Only the two `studies/` registry files
belong to the umbrella. The historical W1–W4 work repos were retired and deleted on 2026-08-03
(tombstone: `wiki/archive/program/w1-w4-retirement/`).

Do not pre-create candidate repositories. A direction can sunset before engineering, or several
candidate analyses can converge into one semantically named study. The umbrella Wiki preserves that
provenance; the engineering identity follows the admitted research object.

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

- Existing umbrella and W1–W4 repos use **`master`**. Each admitted study records its own default branch;
  branch for non-trivial work and open a PR.
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
| study admission and checkout registry | `studies/registry.json` plus the owner decision in the Wiki |
| experiment lifecycle and asset graph | `wiki/Experiment-Assets.md` → `wiki/experiments/<study-slug>/README.md` |
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

The Wiki manages experiments, while bytes retain one storage authority: executable code/config belongs
to the study repo; large data, weights and raw outputs belong in `SPEECHRL_DATA_DIR`; MLflow owns run
tracking; Wiki records bind their IDs, locations and hashes. See `wiki/Experiment-Assets.md`.
