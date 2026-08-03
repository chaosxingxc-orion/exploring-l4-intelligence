# Experiment Assets

The umbrella Wiki is the experiment **control plane** for every admitted research study. It manages the
lifecycle and asset graph; it does not duplicate executable repositories or large artifact bytes.

## Current study registry

- Admitted study repositories: **0**. Machine authority: `studies/registry.json`.
- Planned semantic research object: **audio-aware evidence acquisition**. Source candidate provenance:
  R2. It is `PASS_STAGE1C_FORMAL_OPENING`; innovation and final method remain deliberately undecided.
  Repository creation and experiment execution remain withheld until D1–D4 close, the execution contract
  is frozen, and the owner grants `OWNER_GO_AND_EXECUTION_CONTRACT`.
- R1 is `NO_GO_AS_STANDALONE_DIRECTION__SUNSET_BEFORE_STAGE2`; it has no study repository. Its survey
  and baseline evidence remain reachable through the current survey router and audit history.
- Candidate analyses R3–R9 are not repositories. They enter the study registry only if and when an
  independently named research object receives GO and an execution contract.

The pipeline is direction-local: after one direction is admitted, its engineering and validation may run
while the next candidate direction is surveyed. Completion of all candidate surveys is not a global
prerequisite for an admitted study.

Current carrier readiness: Earnings21, Earnings22 and ConEC are materialized at pinned revisions
(`D0_CLOSED`); D1–D4 alignment, leakage, scorer and ten-sample trace receipts remain pending. Canonical
dataset identity lives in `docs/datasets.lock.json` rather than this page.

## Authority boundaries

| Asset class | Authority |
|---|---|
| Study identity, current stage, protocol freeze, deviations, result synthesis and decisions | umbrella Wiki |
| Code, configs, tests, lockfiles, small fixtures and run entrypoints | independent study Git repository under `studies/<semantic-slug>/` |
| Dataset/model revisions and large raw audio, generations, traces, logs and outputs | `SPEECHRL_DATA_DIR` |
| Run metadata and artifact links | MLflow, referenced by the Wiki record |
| Release hashes and reproducibility receipts | release-scoped `docs/checks/<study-slug>/<release-id>/` or the study release |

W1–W4 under `projects/` remain independent work repositories. They are not parents or default owners of
admitted study code. `common/` receives a capability only after it is stable and genuinely shared across
repositories.

## Required experiment record

Every formal experiment gets a stable Wiki record under `wiki/experiments/<study-slug>/`. The record must
resolve the following fields; values may link to machine manifests rather than copy large content:

| Required binding | Meaning |
|---|---|
| `experiment_id` | Stable program-wide experiment identity |
| `study commit` | GitHub repository URL plus exact Git commit |
| `config hash` | Hash of the effective executable configuration |
| `protocol hash` | Hash/version of the frozen experimental contract |
| `model revision` | Exact served model and serving revision |
| `dataset revision` | Dataset release, split and contamination/exposure binding |
| `MLflow run` | Run ID and tracking-store namespace when MLflow is used |
| `artifact location` | External storage location; never an unbound local anecdote |
| `artifact hashes` | Hashes/manifests needed to verify immutable outputs |
| `result summary` | Primary result and required reliability/cost diagnostics |
| `deviations` | Departures from the frozen protocol and their disposition |
| `decision` | Continue, reroute, stop, replicate or release decision |

Test gold, secrets, credentials and protected data never enter the Wiki. Exposure records retain inherited
prior exposure and state their scope.

## Legacy experiment assets

`docs/integrity/experiment_attempt_registry.jsonl` is a 574-row pre-Stage-2 inventory rooted in W1. It
is preserved rather than rewritten into the new study model. The refreshed machine summary is
`docs/integrity/experiment-asset-inventory.json`: 573 paths are present in the W1 worktree; the deleted
`_repro/wave1_results.md` is history-only and recoverable from W1 Git; no row is unresolved. These legacy
attempts do not become admitted-study experiments and confer no new execution authority.

## Update transaction

When a study is admitted, update in one reviewed transaction:

1. the owner decision and semantic execution contract in the Wiki;
2. `studies/registry.json` and the study's stable experiment index;
3. the independent GitHub repository/checkout;
4. `docs/integrity/experiment-asset-inventory.json` via
   `python scripts/checks/study_workspace_check.py --render-inventory`;
5. applicable context manifests, checks and current-state pages.

Remote repository creation, push and Wiki publication always require explicit authorization.
