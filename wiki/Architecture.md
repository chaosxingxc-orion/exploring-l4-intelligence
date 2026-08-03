# Architecture

The workspace uses an **umbrella governance repo + independent work repos + independently admitted
study repos**. The detailed source is [`docs/architecture.md`](https://github.com/chaosxingxc-orion/exploring-l4-intelligence/blob/master/docs/architecture.md).

## Repository model

```text
exploring-l4-intelligence/      umbrella Git repository
├─ common/                      stable cross-repository utilities
├─ projects/                    W1–W4 independent work repositories
├─ studies/
│  ├─ README.md                 umbrella-owned admission rule
│  ├─ registry.json             umbrella-owned admitted-study registry
│  └─ <semantic-study>/         independent Git/GitHub repository
├─ docs/                        specs, integrity manifests and checks
├─ scripts/                     executable governance/environment tooling
└─ wiki/                        program and experiment management truth
```

The umbrella, not W1, carries the primary program. W1–W4 retain their own histories and roles but are
not parents of new research studies. A study repository is created only after its research object closes
survey, owner GO and an execution contract (`OWNER_GO_AND_EXECUTION_CONTRACT`). Candidate labels such as
R1/R2 remain survey/audit provenance and must not be repository names. R1 sunset before admission and has
no repository.

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
candidate survey → owner decision → semantic contract → independent study repo → engineering → validation
```

Engineering for one admitted study may overlap survey of the next candidate. Finishing every candidate
survey is not a global Stage-2 prerequisite.

---

## 中文

本工作区采用**伞式治理仓 + 独立工作仓 + 经放行的独立研究仓**。伞仓而不是 W1 承载主程序；W1–W4
保留各自历史和工作角色，但不作为新 study 的父目录。研究对象只有在完成自身调研、owner GO 与执行合同
后，才以具体语义名称在 `studies/` 下建立独立 Git/GitHub 仓。R1/R2 等候选编号只留在调研/审计层；R1
已在入场前日落，所以不建仓。

Wiki 管理研究状态、实验协议、资产索引、偏差、结果与裁决；study 仓管理代码/配置/测试；
`SPEECHRL_DATA_DIR` 和 MLflow 保存大型资产与运行数据。一个 study 进入工程后可以并行调研下一个候选，
无须等待所有候选完成。统一资产入口见 [[Experiment-Assets]]。
