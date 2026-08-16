# Architecture

The workspace uses an **umbrella governance repo + independently admitted study repos**. The detailed
source is [`docs/architecture.md`](https://github.com/chaosxingxc-orion/exploring-l4-intelligence/blob/master/docs/architecture.md).

## Repository model

```text
exploring-l4-intelligence/      umbrella Git repository
├─ common/                      stable cross-study utilities
├─ studies/
│  ├─ README.md                 umbrella-owned admission rule
│  ├─ registry.json             umbrella-owned admitted-study registry
│  └─ <semantic-study>/         independent Git/GitHub repository (Stage‑2)
├─ papers/
│  ├─ README.md                 umbrella-owned promotion rule
│  ├─ registry.json             umbrella-owned admitted-paper registry
│  └─ <semantic-paper>/         independent Git/GitHub repository (Stage‑3)
├─ docs/                        specs, datasets.lock.json, integrity manifests and checks
├─ scripts/                     executable governance/environment/data tooling
└─ wiki/                        program and experiment management truth
```

Program cadence: Stage‑1 discussion/survey/justification for every new topic runs in the umbrella; a
study repository is created only after its research object closes survey, owner GO and an execution
contract (`OWNER_GO_AND_EXECUTION_CONTRACT`), and Stage‑2 work lives in that repo until it yields
qualified paper candidates; Stage‑3 (large-scale confirmatory experiments and publication) runs in a
separately admitted repo under `papers/` (`OWNER_GO_AND_PAPER_EXECUTION_CONTRACT`). Candidate labels
such as R1/R2 remain survey/audit provenance and must not be repository names. R1 sunset before
admission and has no repository. The historical W1–W4 work repos were retired on 2026-08-03 (local
checkouts deleted, remotes kept as cold backups; tombstone `wiki/archive/program/w1-w4-retirement/`).

## Experiment assets

The umbrella Wiki manages study state, protocols, experiment indexes, deviations, results and decisions.
Study Git repos own code/config/tests/lockfiles. `SPEECHRL_DATA_DIR` stores models, datasets and raw/large
outputs; MLflow stores run tracking. Wiki records bind their URLs, revisions, IDs and hashes. See
[[Experiment-Assets]].

## Shared library

`common/` remains the light `speechrl_common` package. A capability moves there only after it is stable
and genuinely reused across repositories. Keep torch/transformers/librosa/mlflow/jiwer imports inside the
functions that use them, then run `pytest common/tests`.

## Direction-local pipeline

```text
candidate survey → owner decision → semantic contract → independent study repo (Stage‑2)
    → qualified paper candidate → OWNER_GO_AND_PAPER_EXECUTION_CONTRACT
    → independent paper repo (Stage‑3) → confirmatory evidence → publication | closed-negative
```

Engineering for one admitted study may overlap survey of the next candidate. Finishing every candidate
survey is not a global Stage-2 prerequisite.
