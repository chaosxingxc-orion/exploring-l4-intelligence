# Workspace architecture

## Repository ownership

This workspace uses three repository classes:

1. **Umbrella governance repository** (`exploring-l4-intelligence`) — owns the thesis, current state,
   Wiki, study registry, shared utilities, integrity manifests and cross-study checks.
2. **Work repositories** (`projects/`, W1–W4) — independent historical/publication/supporting works.
   They do not own the primary research program or newly admitted studies.
3. **Study repositories** (`studies/<semantic-slug>/`) — independent GitHub repositories created only
   after a research object receives owner GO and an execution contract.

Candidate labels used during direction analysis are not repository identities. R1, for example, sunset
before admission and has no engineering repository. A later study is named by the research question
frozen in its execution contract, not by an R-number.

## Local topology

```text
exploring-l4-intelligence/          umbrella Git repository
├── common/                         stable cross-repository Python utilities
├── projects/                       W1–W4 independent Git repositories
├── studies/
│   ├── README.md                   umbrella-tracked admission policy
│   ├── registry.json               umbrella-tracked admitted-study registry
│   └── <semantic-slug>/            independent study Git repository
├── wiki/                           program and experiment management truth
├── docs/                           design, integrity and reproducibility assets
├── scripts/                        executable governance and environment tooling
└── speechrl-data/                  external, gitignored large-asset root
```

The umbrella ignores `projects/*/` and `studies/*/`. It tracks the two top-level study registry files,
but never the nested study code.

## Experiment asset architecture

The umbrella Wiki is the management plane. Each study Git repository is an execution plane.
`SPEECHRL_DATA_DIR` and MLflow are the artifact/run planes.

```mermaid
flowchart LR
  W["Umbrella Wiki<br/>state, protocol, experiment index, decision"]
  G["Study Git repository<br/>code, config, tests, lockfiles"]
  A["SPEECHRL_DATA_DIR<br/>models, datasets, raw outputs"]
  M["MLflow<br/>run metadata and artifact links"]
  C["Release/check manifests<br/>hashes and receipts"]
  W -->|"pins commit"| G
  W -->|"pins revision/hash"| A
  W -->|"pins run ID"| M
  W -->|"pins release"| C
```

The current experiment-asset contract and legacy inventory resolution are in
`wiki/Experiment-Assets.md` and `docs/integrity/experiment-asset-inventory.json`.

## Direction-local pipeline

Each research object advances independently:

```text
survey → owner decision → semantic identity + execution contract → study repo → engineering → validation
```

Engineering for one admitted study can overlap the survey of the next candidate. There is no requirement
to finish all candidate-direction surveys before one admitted study enters Stage-2. Integration is a
later research object, not a directory hierarchy imposed on every study.
