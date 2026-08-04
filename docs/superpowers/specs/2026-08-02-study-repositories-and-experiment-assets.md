# Semantic study repositories and experiment assets

## Status

**`IMPLEMENTED_AND_SUPERSEDED_2026-08-03`.** This specification was implemented by the 2026-08-03
reorganization and is retained as historical design rationale only — it is no longer a current
operating instruction. Statements below about keeping W1–W4 under `projects/` and withholding study
repository creation describe the pre-implementation state. Current operating authority:
`docs/architecture.md`, the owner execution contract
(`wiki/experiments/speech-aware-evidence-acquisition/2026-08-04-owner-speech-domain-scope-and-identity-contract.md`)
and the post-reorganization review
(`docs/superpowers/specs/2026-08-03-post-reorganization-architecture-review-and-remediation-proposal.md`).

Original status (2026-08-02): owner-directed architecture refresh. This specification changes
repository ownership and experiment-asset routing only. It does not authorize model/API calls,
downloads, experiments, remote GitHub repository creation, pushes, or Wiki publication.

The implementation-oriented handoff for Fable5 is
[`2026-08-02-fable5-study-directory-reorganization-proposal.md`](2026-08-02-fable5-study-directory-reorganization-proposal.md).

## Problem

The current active documentation treats W1 as the primary program carrier and treats the Stage-1C
candidate IDs R1–R9 as if they were a future engineering decomposition. Both assumptions are now
superseded:

- a candidate ID is provenance for direction analysis, not a durable engineering identity;
- a candidate can sunset without ever receiving an engineering repository, as R1 did;
- each independently admitted research object needs its own semantically named GitHub repository;
- W1–W4 remain separate work repositories and do not own those study repositories;
- the umbrella Wiki manages the experiment lifecycle and asset graph across repositories.

## User journeys

1. As the research owner, I admit a direction only after a GO decision and execution contract, so no
   candidate-only directory can masquerade as an engineering project.
2. As an implementer, I check out a semantically named study repository under `studies/` while keeping
   its Git history, issues, CI, and releases independent from the umbrella and W1–W4.
3. As an experiment reviewer, I start from the umbrella Wiki and can resolve every registered experiment
   to a study-repository commit, config/protocol hash, model and dataset revision, MLflow run, external
   artifact location, result, deviation, and decision.
4. As an auditor, I can distinguish legacy pre-Stage-2 experiment attempts from admitted study assets
   without moving or rewriting historical evidence.

## Target topology

```text
exploring-l4-intelligence/          # umbrella Git repository
├── studies/                        # umbrella-owned registry surface
│   ├── README.md
│   ├── registry.json
│   └── <semantic-study-name>/      # independent nested Git repository; ignored by umbrella
├── projects/                       # W1–W4 independent work repositories
├── common/                         # stable cross-repository utilities only
├── wiki/                           # program truth and experiment control plane
├── docs/                           # contracts, integrity manifests, release checks
└── scripts/                        # executable governance checks
```

The umbrella tracks only `studies/README.md` and `studies/registry.json`. A registered study checkout is
an independent Git repository, is ignored by the umbrella, and is named by its research object rather
than a candidate token such as `r2`.

## Admission and naming contract

- Repository creation requires `OWNER_GO_AND_EXECUTION_CONTRACT`.
- Candidate IDs remain in survey/audit provenance and must not appear as tokens in a study slug.
- The registry contains admitted repositories only. Formally opened but execution-withheld directions stay
  in current research/Wiki state until their gate closes.
- A sunset candidate with no admitted study, including R1, receives no empty repository.
- Split and merge decisions follow the admitted research object: one candidate may yield no repository,
  and several candidate analyses may converge into one repository.

## Asset authority

The Wiki **manages** the experiment lifecycle; it does not duplicate every asset byte.

| Authority | Canonical contents |
|---|---|
| Umbrella Wiki | research state, GO/NO-GO, protocol freeze, experiment ledger, deviations, result synthesis, decisions, asset links |
| Study Git repository | executable code, configs, tests, lockfiles, small fixtures, run entrypoints |
| `SPEECHRL_DATA_DIR` / MLflow | datasets, weights, raw generations/audio/traces, logs and large outputs |
| Release/check manifests | exact hashes and reproducibility receipts |

Every admitted study registry entry binds a decision record and a stable Wiki experiment index. Every
formal experiment record must resolve at least: `experiment_id`, study repository URL and commit,
config/protocol hash, model and dataset revision, MLflow run ID when used, artifact location and hashes,
result summary, deviations, and decision.

## Current migration

- Keep W1–W4 in `projects/`; do not move or rewrite their histories.
- Remove W1's active designation as the primary-program carrier. Its existing selector/evaluator work is
  legacy/component evidence until deliberately adopted by an admitted study.
- Add the `studies/` registry surface, but create no nested study repository yet: the audio-aware evidence
  acquisition direction has passed Stage‑1C and formal opening, while its owner execution contract remains
  unsigned.
- Record R1 as sunset provenance only; do not create a repository for it.
- Preserve `docs/integrity/experiment_attempt_registry.jsonl` as the legacy pre-Stage-2 inventory. A new
  generated inventory reports its live/history-only resolution without rewriting those 574 rows.

## Acceptance checks

- Registry schema and fixed policy fields fail closed.
- Study slugs are semantic kebab-case and reject `r<digits>` tokens.
- Only admitted lifecycle states are accepted; candidate/conditional states cannot enter the registry.
- Each installed study directory is registered and contains its own `.git` metadata.
- No unregistered nested directory is allowed under `studies/`.
- The umbrella ignore policy excludes `studies/*/` while retaining the two registry files.
- The experiment-asset inventory is deterministically regenerated and matches the filesystem/history.
- HOT/CURRENT truth no longer makes all candidate reviews a prerequisite for one admitted direction's
  implementation and no longer assigns the primary program to W1.
- Existing umbrella survey/context gates and tests pass after manifest regeneration.
