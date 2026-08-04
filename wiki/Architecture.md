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

---

## 中文

本工作区采用**伞式治理仓 + 经放行的独立研究仓与论文仓**。运行节奏：每个新课题的 Stage‑1（讨论、
调研、论证）在伞仓完成；研究对象在完成自身调研、owner GO 与执行合同后，以具体语义名称在
`studies/` 下建立独立 Git/GitHub 仓，Stage‑2 工作在该仓进行、至形成合格 paper candidate 为止。R1/R2 等候选编号只留在调研/审计层；R1 已在入场前
日落，不建仓。历史 W1–W4 工作仓已于 2026-08-03 退役（本地删除、远端冷备份，墓碑见
`wiki/archive/program/w1-w4-retirement/`）。

Wiki 管理研究状态、实验协议、资产索引、偏差、结果与裁决；study 仓管理代码/配置/测试；
`SPEECHRL_DATA_DIR` 和 MLflow 保存大型资产与运行数据。一个 study 进入工程后可以并行调研下一个候选，
无须等待所有候选完成。study 的终点是一个或多个合格 paper candidate；Stage‑3（大规模 confirmatory
实验、论文写作与发表）经 `OWNER_GO_AND_PAPER_EXECUTION_CONTRACT` 晋级后在 `papers/` 下的独立仓
完成，伞仓只跟踪 `papers/README.md` 与 `papers/registry.json`。统一资产入口见 [[Experiment-Assets]]。
