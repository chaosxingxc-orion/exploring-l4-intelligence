# 给 Fable5 的研究工程目录重整提案

## 文档状态

```yaml
proposal_id: FABLE5-STUDY-DIRECTORY-REORGANIZATION-V1
date: 2026-08-02
addressee: Fable5
decision_owner: research owner
scope: umbrella and future semantic study repositories
proposal_status: PROPOSED_FOR_REVIEW
execution_authority: DOCUMENTATION_ONLY
remote_repository_creation: WITHHELD
model_or_api_execution: WITHHELD
```

本提案把已经确定的研究治理原则转成可执行的目录与资产迁移方案。请 Fable5 审阅后返回
`ACCEPT`、`ACCEPT_WITH_AMENDMENTS` 或 `REJECT_WITH_ALTERNATIVE`；在 owner 签发
`OWNER_GO_AND_EXECUTION_CONTRACT` 前，不创建远程仓、不初始化正式 study checkout、不搬迁代码，
也不运行任何模型实验。

## 一、为什么需要重整

当前目录同时承载了三种不同身份：W1–W4 的历史/支撑工程、R1–R9 的调研论证编号，以及未来正式
研究对象的工程实现。如果继续直接用 W 或 R 作为工程目录，会产生四个结构性问题：

1. **论证编号被误当成工程身份。** R1 已在 Stage‑2 前日落，说明候选编号并不天然对应一个工程仓；
   R2 也只是 `audio-aware evidence acquisition` 的来源 provenance，而不是长期研究名称。
2. **方向间被制造出虚假的串联依赖。** R2 进入工程不应等待 R3–R9 调研完成；后续方向也不应被迫
   接入所谓 R2→R3→… 的单一代码链。
3. **Git 生命周期被混在一起。** 正式研究对象需要自己的 issue、CI、release、复现实验 commit 和论文
   历史；把它仅作为伞仓普通子目录会把治理文档和实验代码绑在同一个发布周期中。
4. **Wiki 管理与文件存储容易混淆。** Wiki 应管理实验身份、协议、资产链接和决策，不应复制模型、
   数据、原始 trace 或另一个 Git 仓的完整代码。

因此，建议采用：**伞仓负责研究治理和实验资产图；每个获准的语义研究对象拥有独立 GitHub 仓；
本地统一 checkout 到伞仓的 `studies/` 下。** `studies/` 是本地工作区容器和登记面，不是把所有研究
重新合并进一个 Git 仓。

## 二、建议的目标拓扑

```text
exploring-l4-intelligence/                    # umbrella Git repo
├── studies/
│   ├── README.md                             # umbrella tracked
│   ├── registry.json                         # umbrella tracked; admitted studies only
│   └── audio-aware-evidence-acquisition/     # independent Git repo; only after owner GO
├── projects/
│   ├── speech-mllm-training-free-rl/          # W1; unchanged independent repo
│   ├── speech-mllm-efficient-rl-alignment/    # W2; unchanged independent repo
│   ├── speech-mllm-multitask-rl/              # W3; unchanged independent repo
│   └── speech-mllm-omni-embedding-rl/         # W4; unchanged independent repo
├── common/                                   # stable, genuinely cross-study utilities only
├── wiki/
│   ├── Research-Objective.md                 # HOT program state
│   ├── Experiment-Assets.md                  # program-wide experiment router
│   ├── experiments/<semantic-study-slug>/    # admitted-study lifecycle ledger
│   ├── survey/                               # Stage-1 evidence and candidate provenance
│   └── audit/                                # immutable reviewer transactions
├── docs/
│   ├── datasets.lock.json                    # canonical program-level data identity
│   ├── superpowers/specs/                    # engineering contracts and plans
│   └── checks/<study-slug>/<release-id>/     # reproducibility receipts
└── scripts/                                  # umbrella governance and shared asset tooling
```

第一项工程的长期标识建议冻结为：

```yaml
research_name: audio-aware evidence acquisition
repository_slug: audio-aware-evidence-acquisition
python_package: audio_aware_evidence_acquisition
source_provenance: R2
```

`R2` 不得出现在远程仓名、Python package、MLflow experiment 主命名空间或正式实验 ID 中。它只保留在
proposal、review、Decision‑Log 和 registry 的 provenance 字段里。R1 不创建任何空仓或占位目录。

## 三、为什么是独立 GitHub 仓，而不只是伞仓子目录

本地目录与 GitHub 仓不是二选一。建议形态是“**独立 GitHub 仓 + `studies/` 下本地 checkout**”：

| 需求 | 仅作为伞仓普通目录 | 独立仓并 checkout 到 `studies/` |
|---|---|---|
| 独立 issue、CI、release、论文版本 | 与治理仓耦合 | 独立管理 |
| 研究日落、拆分或合并 | 容易留下半成品目录 | 可独立归档或转向 |
| 代码审查与复现实验 commit | 被 Wiki/治理改动稀释 | 每个 commit 都属于该研究对象 |
| 跨研究复用 | 容易复制粘贴 | 稳定后才提升到 `common/` |
| 本地协作便利性 | 方便 | 同样方便，由 `studies/` 统一容纳 |
| 伞仓状态清洁 | 容易误收实验文件 | nested repo 被 umbrella ignore |

独立仓不削弱 Wiki。恰恰相反，Wiki 成为跨仓的实验 control plane：它把问题、协议、study commit、
dataset/model revision、MLflow run、外部 artifact、结果、偏差和决策连接成一张可审计资产图。

## 四、资产所有权与迁移判断

| 当前或未来资产 | 目标 authority | 本轮动作 |
|---|---|---|
| R2 v20 proposal、round‑22 review/permission | umbrella Wiki/audit | 保留原位，不复制到 study 仓 |
| 当前研究状态、GO/NO-GO、阶段裁决 | umbrella Wiki | 保留并持续 supersede in place |
| program-level dataset identity/hash/license | `docs/datasets.lock.json` | 保留原位；study 仅按键引用 |
| 数据、模型、音频、原始 generation/trace | `SPEECHRL_DATA_DIR` | 不迁入 Git；通过 manifest/hash 引用 |
| study 专用 loader、scorer、adapter、controller | 独立 study repo | owner GO 后新建或显式迁入 |
| study config、tests、CI、lockfile、run entrypoint | 独立 study repo | owner GO 后创建 |
| 正式实验记录、协议偏差与研究决策 | `wiki/experiments/<slug>/` | admission 交易中创建 |
| 运行元数据与大结果 | MLflow/外部 artifact store | Wiki 保存 ID、URI 和 hash |
| release 复现回执 | study release 或 umbrella `docs/checks/` | 按 release 生成 |
| W1–W4 既有代码和 `_repro` 历史 | 原 work repo | 不搬历史；按需引用或显式采用 |
| 多个 study 稳定共用的轻量能力 | `common/` | 至少两个真实消费者后再提升 |

核心规则是：**按 authority 迁移，而不是按“看起来相关”迁移。** 文献、决策和实验索引属于伞仓；
可执行研究代码属于 study 仓；大字节资产属于外部数据根；W1 历史不因新方向获批而自动改名或搬家。

## 五、分阶段实施建议

### Phase 0 — 当前可做：无模型、无建仓准备

1. 关闭 Earnings21、Earnings22、ConEC 的 D1–D4：样本身份、信息边界/泄漏、评分器和十样本 trace。
2. 完成 Stage‑2A execution contract 的精确字段：远程 URL、runtime/model revision、baseline revision、
   split、prompt、metric、预算、停止条件和 exposure。
3. 为可能迁入的代码建立只读 inventory：来源仓、当前 commit、license、依赖、测试状态、目标归属。
4. 不创建 `studies/audio-aware-evidence-acquisition/` 占位目录；空目录会制造“已经 admission”的假象。

### Phase 1 — owner GO 交易：创建研究身份

以下动作必须在同一个可审查交易中完成：

1. owner 签发 `OWNER_GO_AND_EXECUTION_CONTRACT`；
2. 创建独立 GitHub 仓 `audio-aware-evidence-acquisition`；
3. checkout 到 `studies/audio-aware-evidence-acquisition/`，确认其拥有独立 `.git`；
4. 在 `studies/registry.json` 登记 URL、default branch、decision record 和 Wiki experiment index；
5. 创建 `wiki/experiments/audio-aware-evidence-acquisition/README.md`；
6. 运行 study-workspace、context-surface 和 registry fail-closed checks。

### Phase 2 — 工程基建：先建立可复现纵向链

建议独立仓的初始结构为：

```text
audio-aware-evidence-acquisition/
├── README.md
├── LICENSE
├── pyproject.toml
├── src/audio_aware_evidence_acquisition/
│   ├── data/                 # lock-key based loaders; no dataset bytes
│   ├── models/               # frozen-core API adapter
│   ├── evidence/             # schema, provenance and admission
│   ├── scoring/              # official/registered metrics
│   ├── tracing/              # request/tool/response/cost trace
│   └── experiments/          # composition, not raw outputs
├── configs/
│   ├── model/
│   ├── dataset/
│   ├── baseline/
│   └── experiment/
├── scripts/
│   ├── reproduce.sh
│   └── evaluate.sh
├── tests/
│   ├── unit/
│   ├── integration/
│   └── contract/
└── docs/
    ├── engineering.md        # repository-local implementation facts
    └── migration-manifest.md # adopted files and provenance
```

首个两周切片只交付 loader→frozen-core adapter→trace→scorer→artifact link 的 reproduction-zero
纵向链，以及一个 readiness-qualified closest-prior 尝试。它不执行 v20 的全量搜索，不形成创新性结论。

### Phase 3 — reproduction-first Stage‑2A

1. 先复现最接近且最强、且 readiness 合格的公开 prior；
2. 复现失败必须区分实现缺陷、载体不匹配和 baseline-not-ready；
3. 至少一个 prior 路径可信后，才进入 OBS、ORG/SUPPLY、USE/CONTROL 的方向性原型；
4. 用实验决定三支柱的保留、合并、拆分或日落，并开始收敛具体方法和创新主张；
5. 最终方案冻结后才进入 Stage‑2B。

## 六、安全迁移协议

任何现有代码进入新 study 仓时，建议执行以下 copy-and-verify 流程，而不是直接移动：

1. 在 `migration-manifest.md` 登记来源 repo、commit、原路径、license 和迁移理由；
2. 复制最小必要文件，保留来源，不删除 W1–W4 历史；
3. 对复制前后内容做 hash 或 Git blob 核验；
4. 先让新仓测试通过，再更新 umbrella Wiki/registry 引用；
5. 只有确认存在至少两个真实消费者时，才把通用实现抽到 `common/`；
6. 若新仓初始化失败，删除尚未登记的临时 checkout 即可回滚，umbrella 与 W1–W4 不受影响。

禁止事项：跨仓改写历史、批量搬运 `_repro`、把数据或模型放进 Git、先创建空仓后补授权、把 W1
直接改名成新 study、用 R2 或 Stage‑2 作为长期工程目录名。

## 七、Fable5 需要给出的反馈

请 Fable5 针对以下问题逐项回复：

1. 是否接受 `audio-aware-evidence-acquisition` / `audio_aware_evidence_acquisition` 作为仓与包名？
2. 哪些现有实现确实需要从 W1 或 umbrella 被新 study 消费？请给出文件级清单与来源 commit，不做整仓搬迁。
3. 哪些数据/评分/trace 工具属于 program-level shared tooling，哪些只属于本 study？
4. 第一条 runnable closest-prior reproduction 建议选择哪一项，理由及公开 artifact readiness 是什么？
5. execution contract 还缺哪些必须由 owner 冻结的选择？
6. 对本提案返回：`ACCEPT`、`ACCEPT_WITH_AMENDMENTS` 或 `REJECT_WITH_ALTERNATIVE`。

## 八、验收条件

目录重整只有同时满足以下条件才算完成：

- umbrella 不追踪任何 study 子仓文件，只追踪 `studies/README.md` 与 `studies/registry.json`；
- study slug 与 package 名不含 R 编号、W 编号或阶段编号；
- 每个 checkout 都在 registry 中，且拥有独立 `.git`；
- Wiki experiment index 能解析到 study commit、协议/config hash、数据/model revision 和 artifact；
- W1–W4 历史与用户未归档资产没有被移动或删除；
- 数据、模型和大输出没有进入 Git；
- study workspace、AI context、CURRENT manifest 与审计不可变性检查通过；
- 没有把正式开题许可误写成创新性裁决或模型实验授权。

## 九、建议裁决

建议 owner 先批准本提案的**目录与 authority 模型**，并要求 Fable5 提交文件级迁移清单和 execution
contract amendment；两者复核通过后，再签发远程建仓与 Stage‑2A execution GO。这样可以立即结束
目录争论，同时保留对实验载体、预算和 closest-prior 选择的独立把关。
