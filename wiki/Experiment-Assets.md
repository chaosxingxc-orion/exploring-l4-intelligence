# Experiment Assets

The umbrella Wiki is the experiment **control plane** for every admitted research carrier — Stage‑2
studies and Stage‑3 paper projects alike. It manages the lifecycle and asset graph; it does not
duplicate executable repositories or large artifact bytes.

## Current study registry

- Admitted study repositories: **1**. Machine authority: `studies/registry.json`.
- **speech-aware evidence acquisition** (source candidate provenance: R2) is admitted. The single
  self-contained effective authority (2026-08-03 GO + speech-only identity + Stage‑3 stop line) is
  (`wiki/experiments/speech-aware-evidence-acquisition/2026-08-04-owner-consolidated-execution-contract.md`).
  Its repository is `studies/speech-aware-evidence-acquisition/` (independent Git history, private
  remote); current stage: Stage‑2A E0 (D1–D4 model-free closure) in progress. General/environmental
  audio is excluded from this study while already downloaded cross-domain assets remain governed in
  the canonical lock. Innovation and the candidate method are Stage‑2 outputs; final validation is
  Stage‑3 in the promoted paper repo; model-facing execution stays fail-closed behind E0 closure and
  the runtime receipt.
- R1 is `NO_GO_AS_STANDALONE_DIRECTION__SUNSET_BEFORE_STAGE2`; it has no study repository. Its survey
  and baseline evidence remain reachable through the current survey router and audit history.
- Candidate analyses R3–R9 are not repositories. They enter the study registry only if and when an
  independently named research object receives GO and an execution contract.

The pipeline is direction-local: after one direction is admitted, its engineering and validation may run
while the next candidate direction is surveyed. Completion of all candidate surveys is not a global
prerequisite for an admitted study.

## Paper project registry

Admitted paper repositories: **1**. Machine authority: `papers/registry.json`, enforced in
admission mode by `scripts/checks/paper_workspace_check.py` (per-entry schema, name policy,
checkout and authorization-record existence, ignore rule, count consistency; unregistered
checkouts fail closed). A paper project enters under `OWNER_GO_AND_PAPER_EXECUTION_CONTRACT` —
by promotion from a qualified study candidate (Decision-Log continuation entry 91) or by direct
owner admission recorded in the entry's authorization record. Admitted: `meeting-minutes-agent`
(2026-08-17, direct owner admission; index and contract under
`wiki/experiments/papers/meeting-minutes-agent/`). Candidate-bundle and promotion-receipt
machinery remains deferred until the first promotion-path admission.

Current carrier readiness: Earnings21, Earnings22 and ConEC are materialized at pinned revisions
(`D0_CLOSED`); SLUE-SQA-5, ContextASR-Bench and AMI are complete speech-domain secondary carriers.
D1–D4 alignment, leakage, scorer and ten-sample trace receipts remain pending. FSD50K, AudioSet and
ESC-50 are retained local cross-domain assets with no experiment binding here. Canonical dataset
identity lives in `docs/datasets.lock.json` rather than this page.

## Authority boundaries

| Asset class | Authority |
|---|---|
| Study identity, current stage, protocol freeze, deviations, result synthesis and decisions | umbrella Wiki |
| Code, configs, tests, lockfiles, small fixtures and run entrypoints (Stage‑2) | independent study Git repository under `studies/<semantic-slug>/` |
| Stage‑3 confirmatory code, manuscripts and publication releases | independent paper Git repository under `papers/<semantic-slug>/` (promotion-gated; none admitted) |
| Dataset/model revisions and large raw speech/audio carriers, generations, traces, logs and outputs | `SPEECHRL_DATA_DIR` |
| Run metadata and artifact links | MLflow, referenced by the Wiki record |
| Release hashes and reproducibility receipts | release-scoped `docs/checks/<study-slug>/<release-id>/` or the study release |

The historical W1–W4 work repositories were retired on 2026-08-03: local checkouts deleted, remotes
kept as unlinked cold backups (tombstone `wiki/archive/program/w1-w4-retirement/`). They are not
parents or owners of admitted study code. `common/` receives a capability only after it is stable and
genuinely shared across admitted studies (`common/OWNERSHIP.md`).

## Required experiment record

Every formal experiment gets a stable Wiki record under its carrier's index: Stage‑2 records under
`wiki/experiments/<study-slug>/`, Stage‑3 records under `wiki/experiments/papers/<paper-slug>/`
(created at first paper admission). The record must resolve the following fields; values may link to
machine manifests rather than copy large content:

| Required binding | Meaning |
|---|---|
| `experiment_id` | Stable program-wide experiment identity |
| `carrier type` | `study` or `paper` — which carrier class executed this record |
| `study commit` | Carrier repository URL plus exact Git commit (study commit for Stage‑2 records; paper commit for Stage‑3 records) |
| `config hash` | Hash of the effective executable configuration |
| `protocol hash` | Hash/version of the frozen experimental contract |
| `model revision` | Exact served model and serving revision |
| `dataset revision` | Dataset release, split and contamination/exposure binding |
| `split role` | `discovery`, `dev` or `confirmatory` role of the data this record touched |
| `split identity hash` | Hash of the exact sample-identity list read by this record |
| `consumed` | Whether this record consumed (read results from) a confirmatory split — irreversible once `yes` |
| `MLflow run` | Run ID and tracking-store namespace when MLflow is used |
| `artifact location` | External storage location; never an unbound local anecdote |
| `artifact hashes` | Hashes/manifests needed to verify immutable outputs |
| `result summary` | Primary result and required reliability/cost diagnostics |
| `shared code revision` | Exact revision of any shared code consumed from outside the study repo (e.g. the umbrella `common` commit), recorded even when the study commit is unchanged |
| `deviations` | Departures from the frozen protocol and their disposition |
| `decision` | Continue, reroute, stop, replicate or release decision |

Test gold, secrets, credentials and protected data never enter the Wiki. Exposure records retain inherited
prior exposure and state their scope.

## Legacy experiment assets

`docs/integrity/experiment_attempt_registry.jsonl` is a 574-row pre-Stage-2 inventory rooted in W1. It
is preserved rather than rewritten into the new study model. Since the 2026-08-03 W1–W4 retirement no
row resolves in a local worktree; every row is bound to the retired cold-backup remote as
`remote@commit:path` in `docs/integrity/legacy-asset-resolution.json` (574 `COLD_BACKUP_RESOLVED`,
0 `UNRESOLVED`), against `docs/integrity/retired-repository-registry.json` (remotes, frozen final
commits, offline git-bundle hashes). The fail-closed rule is machine-enforced: any unresolved row
without a dated owner waiver fails `study_workspace_check.py` and
`legacy_asset_resolution_check.py`. These legacy attempts do not become admitted-study experiments
and confer no new execution authority.

## Update transaction

When a study is admitted, update in one reviewed transaction:

1. the owner decision and semantic execution contract in the Wiki;
2. `studies/registry.json` and the study's stable experiment index;
3. the independent GitHub repository/checkout;
4. `docs/integrity/experiment-asset-inventory.json` via
   `python scripts/checks/study_workspace_check.py --render-inventory`;
5. applicable context manifests, checks and current-state pages.

A paper admission uses its own promotion transaction (candidate bundle blob, owner paper GO,
registry entry, promotion receipt, index creation), defined together with the promotion machinery at
first admission. Remote repository creation, push and Wiki publication always require explicit
authorization.
