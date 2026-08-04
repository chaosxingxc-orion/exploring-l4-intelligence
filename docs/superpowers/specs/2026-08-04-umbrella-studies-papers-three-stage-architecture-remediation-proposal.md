---
title: "Umbrella → Studies → Papers 三阶段研究工程架构整改提案"
proposal_id: "PROGRAM-THREE-STAGE-RESEARCH-REPOSITORY-ARCHITECTURE-V1"
date: "2026-08-04"
addressed_to: "research owner and research engineering team"
proposal_status: "REVIEWED__PARTIALLY_ACCEPTED_AND_OWNER_TRIMMED__SEE_DECISION_LOG_XU91_XU92"
overall_assessment: "CURRENT_TWO-CARRIER_MODEL_CANNOT_REPRESENT_THE_REQUIRED_THREE-STAGE_PIPELINE"
execution_authority: "DOCUMENTATION_AND_GOVERNANCE_PROPOSAL_ONLY"
model_execution_effect: "NO_NEW_AUTHORITY"
remote_repository_effect: "NO_NEW_AUTHORITY"
supersession_effect: "NONE_UNTIL_OWNER_ACCEPTANCE_AND_DATED_IMPLEMENTATION_CONTRACT"
scope: "umbrella governance, study repositories, future paper repositories, promotion contracts, experiment routing, and executable checks"
---

# Umbrella → Studies → Papers 三阶段研究工程架构整改提案

> **裁决状态（2026-08-04）：部分接受、部分否决、部分延期。** 有效裁决 = 对抗评审
> （`2026-08-04-three-stage-architecture-critique-and-decision-request.md` 第 4/5 节）+
> Decision-Log-2026-08 续91/续92；两者优先于本提案正文。路径重组、`wiki/directions/`、
> study gate token 改名被否决；promotion 机器件挂触发器延期。本文其余部分保留为输入记录。
>
> **原评审状态：`PROPOSED_FOR_REVIEW`。** 本文记录研究 owner 与协作者于 2026-08-04
> 形成的架构共识及其批判性补全，供工程团队评审和拆解实施。本文自身不修改当前研究阶段，
> 不撤销或扩大现有 owner contract，不授权模型/API 调用、数据下载、大规模实验、远程 GitHub
> 仓创建、push、Wiki 发布或论文投稿。任何实施必须在 owner 接受本提案后，由带日期的架构裁决、
> 执行合同和逐仓事务另行生效。

## 1. 给工程团队的结论

当前仓库模型只有两个活动载体：

```text
umbrella governance → admitted study repository → formal experiments / validation
```

它正确解决了“Stage-1 candidate 不是工程身份”和“每个 admitted study 使用独立 Git/GitHub 仓”
的问题，却把**课题形成**、**大规模实验验证**与**论文写作发表**压进同一个 `studies/` 层。
这无法表达本项目实际需要的三阶段研究流水线：

```text
Umbrella：方向发现与资格审查
    ↓ OWNER_GO_AND_STUDY_CONTRACT（拟议名称）
Studies：课题分析、理论化、baseline 复现与 paper candidate 形成
    ↓ OWNER_GO_AND_PAPER_EXECUTION_CONTRACT（拟议名称）
Papers：大规模实验、最终证据、论文写作与发表
```

整改的核心不是简单新增一个 `papers/` 文件夹，而是同时建立：

1. 三个阶段各自的研究职责、允许动作、禁止动作和退出条件；
2. `study → paper` 的显式晋级合同与可哈希交接包；
3. 独立的 study registry 与 paper registry；
4. 独立的本地 checkout、GitHub remote、实验命名空间和生命周期检查；
5. discovery/confirmatory、样本 exposure、baseline 与代码 provenance 的跨阶段继承；
6. 允许负结果、回流和非论文成果的科学完整性规则。

建议保留当前“伞仓 + 独立语义仓 + 外部大资产”的基础，不把 study 合并回伞仓，也不恢复
W1–W4。目标是在其上新增真正的 paper-stage carrier，并收窄 study-stage 的终点。

## 2. 问题陈述与当前缺口

### 2.1 当前设计把 research object 与最终执行项目视为同一对象

现行规则规定：一个独立 admitted research object 对应一个 `studies/<semantic-slug>/` Git/GitHub
仓；代码、配置、测试和正式实验入口均由该仓拥有。`wiki/Experiment-Assets.md` 又把每条正式实验
直接绑定到 study commit 和 `wiki/experiments/<study-slug>/`。

这种设计在只有一个工程阶段时内部一致，但无法区分：

- “我们是否理解了一个值得研究的课题”；
- “我们是否找到了一个值得做大规模实验的具体改进点”；
- “这个改进点是否已经完成最终实证并形成论文”。

结果是 study repo 既像课题分析工作台，又像最终论文实验仓，还可能长期容纳同一课题衍生出的多篇
论文。第二篇论文出现时，实验、claim、confirmatory exposure、release 和 GitHub ownership 都会开始
互相污染。

### 2.2 当前没有 paper-stage 工程身份

当前工作区没有：

- `papers/README.md` 与 `papers/registry.json`；
- `papers/<semantic-paper-project>/` checkout 规则；
- paper repo 创建门；
- study-to-paper promotion receipt；
- paper experiment namespace；
- paper lifecycle；
- paper 级 reproducibility、submission 与 publication routing；
- 防止两个 paper 重复消费同一 confirmatory 样本的机器检查。

因此即使物理上可以在 `studies/` 下再建多个仓，治理上仍无法说明它们是同一方向的不同课题、同一
课题的不同 paper，还是完全独立的研究对象。

### 2.3 当前 Stage-2 合同跨越了阶段边界

现行 SAEA Stage-2A 入场合同依次授权 E0、R0、closest-prior reproduction 与 directional
exploration，并把创新性和最终方法继续留给 Stage-2A/2B 证据。该序列中的 E0、R0、baseline
qualification 和 bounded exploration 可以属于 study；但大规模 confirmatory、最终提升结论、论文
消融与发表必须属于 paper。当前合同尚未提供这条停止线。

### 2.4 目录迁移本身可能破坏可复现性

如果只在 paper 获批时把 study 代码手工复制到新仓，会出现：

- 不知道复制自哪个 study commit；
- study 和 paper 同名文件独立演进，修复无法判断应回写哪一边；
- baseline、scorer 或信息边界在迁移中漂移；
- paper 读取了 study discovery 结果，却没有继承 exposure；
- 一个 study 衍生多个 paper 后重复使用 confirmatory set；
- 论文 release 无法解释其与原始课题合同之间的关系。

所以三阶段架构必须把“晋级”定义为证据交易，而不是目录复制。

## 3. 术语与对象模型

### 3.1 Research direction（研究方向）

由 umbrella 管理的问题族。它回答“在一个学科范围内，我们希望研究什么，以及为什么值得研究”。
R1、R2 等 candidate ID 只保留为 survey/audit provenance；获准方向必须使用语义名称，不以候选编号
作为工程身份。

一个方向可以：

- 不产生 study 并 sunset；
- 产生一个或多个 studies；
- 与其他候选分析共同收敛成一个 study。

方向本身通常没有独立工程 repo；它的当前状态、文献和决策由 umbrella Wiki 管理。

### 3.2 Study（研究课题）

已经从方向中选出、值得深入分析的课题。它回答：

> 当前方法有什么承重不足，哪些改进机制值得检验，怎样通过数学、统计和可复现实验设计把问题变成
> 一个或多个可执行的 paper candidate？

Study 是 Stage-2 的独立 Git/GitHub 工程仓，但不是最终 paper 仓。它可以拥有分析代码、baseline
复现、scorer、trace、形式化定义和有预算上限的小规模 probe；它不拥有尚未获 paper GO 的大规模
confirmatory campaign 或最终论文结论。

### 3.3 Paper project（论文项目）

从一个或多个 studies 的冻结 candidate bundle 晋级而来的 Stage-3 独立工程对象。它回答：

> 对一个预注册的改进主张，大规模、可复现、具有足够统计效力的实验给出了什么结论？

Paper repo 不只是 manuscript 仓。它拥有大规模实验代码、配置、tests、discovery/confirmatory runs、
统计分析、图表、supplement、artifact manifest、审稿回复和 publication release。

默认一篇 paper 有一个 `primary_study`，允许零到多个 `supporting_studies`。一个 study 可形成多个
paper candidates；一篇 paper 也可综合多个 studies，但其主 claim、代码和决策 owner 必须唯一。

### 3.4 Experiment（实验）

实验永远归属于执行它的 carrier：Stage-2 probe/reproduction 归 study，Stage-3 scale/confirmatory
实验归 paper。Experiment 不是独立 Git 仓；它由 carrier commit、config/protocol hash、数据/模型
revision、MLflow run、artifact hash、结果、偏差和决策共同定义。

### 3.5 Research output（研究成果）

Paper 是主要 Stage-3 carrier，但不是唯一合法成果。Study 也可能产生 benchmark、dataset、tool、
technical report、replication report 或可靠负结果。某项成果只有在确实需要独立 issue/CI/release/
维护生命周期时才建立独立仓，不能为了目录对称预建空仓。

## 4. 科学完整性原则

### 4.1 Paper 的成功不是“必须得到提升”

Stage-3 的成功条件必须是：

> 按冻结协议，对预注册假设作出具有足够统计效力、可审计和可复现的判断。

零提升、负提升、只在部分条件成立或推翻原机制，都是合法结果。不得以“直到得到预期提升”为执行
目标，否则会诱发 HARKing、反复调参、选择性报告和 confirmatory contamination。

### 4.2 数学形式服务于承重 claim，不制造装饰性理论

Study 必须给出可证伪的变量、机制、假设和预测。只有当论文 claim 依赖数学命题时，才要求正式公式、
证明或 Lean artifact。经验型系统研究可以用因果图、状态机、统计模型和清晰的操作定义完成论证；
不能为了晋级而添加不承重的公式。

### 4.3 三阶段不是不可回退的瀑布

允许以下回流：

- Study 发现方向性假设不成立，回到 umbrella 做 bounded reassessment 或 sunset；
- Paper 发现机制定义、baseline 或信息边界错误，退回 study 修订 candidate；
- Paper 结果产生新的研究问题，作为新 study proposal 回到 umbrella admission；
- 审稿意见要求新 claim 时，必须判断它是 paper-scope amendment，还是新的 study/paper，而不是静默扩域。

回流必须通过带日期的 decision/amendment 发生；已读取的结果、exposure 和失败不得被回写抹除。

### 4.4 Confirmatory 资产是稀缺且会耗尽的

每个 study candidate 和 paper 必须继承并登记：

- discovery/confirmatory split identity；
- 已触达样本、结果和工具；
- inherited exposure；
- confirmatory reservation owner；
- 多个 papers 共享 carrier 时的样本重用与 multiplicity 处理。

同一 confirmatory set 不能因换了 paper repo 就重新变成“未读”。

## 5. 三阶段职责、允许动作与退出门

### 5.1 Stage 1 — Umbrella：方向发现与资格审查

#### 目的

在明确学科范围内形成对研究现状、问题空间、基础资产和候选方向的有界理解，决定哪个方向值得进入
课题研究。

#### 主要活动

- bounded literature survey、prior map 与 claim registry；
- 学界当前方法、已知不足和相邻方向分析；
- candidate gap hypotheses；
- 模型、数据、license、评价指标和共享资产准备；
- 数据 identity/acquisition 的 program-level 管理；
- 方向级 formal opening、review 与 GO/NO-GO；
- 明确调查覆盖范围、未知项与 reopen trigger。

#### 禁止默认发生

- 为未获准 candidate 创建 study 或 paper repo；
- 用 candidate ID 作为仓名、包名或实验命名空间；
- 因文献提到数据集就自动下载或纳入实验；
- 把文献数量、形式化证明或目录存在误认为技术创新成立；
- 未经单独授权进行模型调用或结果性实验。

#### 拟议退出门

`OWNER_GO_AND_STUDY_CONTRACT`，至少冻结：

- semantic direction 与 study name；
- research scope 和排除项；
- gap hypothesis 与最近 prior；
- 可用数据/模型/指标基础；
- 初始 baseline family；
- study 的预算、失败语义、停止线和 owner；
- 哪些新证据会使方向回到 umbrella。

### 5.2 Stage 2 — Studies：课题形成与 paper candidate qualification

#### 目的

把已经获准的研究课题变成可证伪、可复现、可进行大规模验证的一个或多个 paper candidate。

#### 主要活动

- 对当前课题和 closest priors 的承重不足做因果/机制分析；
- 比较多个候选改进点，明确哪些应继续、合并、拆分或停止；
- 建立变量、状态、控制对象、假设、公式和必要形式化证明；
- 冻结信息边界、scorer、trace、metric 与成本口径；
- 完成 closest/strongest-prior 的 readiness 与可复现性验证；
- 做有预算上限、仅用于可行性和机制辨识的小规模 probes；
- 设计 intervention、comparator、negative/oracle control、ablation 和统计方案；
- 预留未读 confirmatory data；
- 形成一个或多个 paper candidate bundles。

#### 允许的实验

- model-free identity/leakage/scorer/trace checks；
- 最小 end-to-end wiring；
- baseline reproduction；
- bounded feasibility/discovery probe；
- measurement calibration、headroom、oracle 和 negative control；
- 为 sample-size/power 估计所需的有限 pilot。

这些结果可以决定 candidate 是否晋级，但不能作为偷看 paper confirmatory 后再改假设的通道。

#### 禁止默认发生

- 未获 paper GO 的大规模 confirmatory campaign；
- 把 study probe 写成最终 paper 优越性 claim；
- 为追求正结果反复扩大方法或数据范围；
- 在多个 candidate 之间共享未登记的 test exposure；
- 在 study repo 内完成多个未分权的最终论文 release。

#### Study 拆分判据

若两个候选改进点具有不同的失败机制、baseline 家族、数据/信息边界、数学对象或独立停止决策，
应拆成两个 studies，而不是等到 paper 阶段才分开。仅是同一机制下的 carrier、消融或参数变化，则留在
同一 study。

#### 拟议退出门

每个 candidate 单独签发 `OWNER_GO_AND_PAPER_EXECUTION_CONTRACT`。未晋级 candidate 可继续分析、
暂停或 sunset；一个 candidate 的 GO 不自动授权同 study 的其他 candidate。

### 5.3 Stage 3 — Papers：大规模实验、最终证据与发表

#### 目的

针对冻结的 candidate claim 执行足够规模的科学实验，形成可复现的正、零或负结论，并完成论文写作、
审稿和发表。

#### 主要活动

- 建立 paper 独立 repo、CI、lock、experiment namespace 与 release policy；
- 迁入或 pin 已批准的 study code、baseline 与协议；
- 实施 production-scale experiment runner；
- 在冻结规则下执行 discovery、selection 和 confirmatory；
- 报告主效应、tails、回归、成本、统计不确定性和 multiplicity；
- 生成 tables、figures、supplement 和 artifact manifest；
- 完成 manuscript、submission、revision、response 和 publication release；
- 对失败、偏差和未支持 claim 保持同等可见性。

#### Paper 生命周期

建议至少支持：

```text
admitted → engineering → discovery → confirmatory-frozen
         → evidence-complete → writing → submitted
         → revision → published | withdrawn | closed-negative
```

`withdrawn` 与 `closed-negative` 不删除 Git 历史、实验 ledger 或 publication record。

## 6. Study → Paper 晋级包

每个 paper repo 创建前必须存在一份冻结、可哈希的 candidate bundle。建议 schema 至少包含：

| 字段 | 必须回答的问题 |
|---|---|
| `candidate_slug` | 哪个语义 candidate 获准？不得使用 R/W/阶段编号作工程身份 |
| `primary_study` | 谁拥有主问题、代码与停止决策？ |
| `supporting_studies` | 还继承了哪些 study 的证据？ |
| `study_commits` | 每个来源仓的 exact commit 是什么？ |
| `claim` / `null` | 主张及其零假设、失效条件是什么？ |
| `mechanism` | 哪个对象被改变，为什么预计影响结果？ |
| `formal_contract` | 使用哪些数学/统计定义、假设或 proof artifact？ |
| `intervention` / `comparators` | 方法、closest prior、negative/oracle controls 是什么？ |
| `baseline_receipts` | baseline 是否实际 runnable、以什么 revision/边界复现？ |
| `pilot_evidence` | 哪些 bounded probes 支持进入规模实验？不得冒充最终证据 |
| `model_and_data_revisions` | 模型、数据、split、license 与 contamination 边界是什么？ |
| `exposure_inherited` | paper 创建前已经看过哪些样本、结果、工具输出？ |
| `confirmatory_reservation` | 哪些未读样本由本 paper 占用，是否与其他 paper 重叠？ |
| `metrics_and_power` | 主指标、效应量、样本量、统计方法和 multiplicity 规则是什么？ |
| `experiment_protocol` | discovery、selection、confirmatory、ablation 与 stop rule 是什么？ |
| `resource_budget` | 调用、GPU/CPU、speech seconds、token、时间和付费上限是什么？ |
| `code_migration_manifest` | 哪些文件 COPY、DEPEND、REIMPLEMENT 或 REJECT，来源 blob 是什么？ |
| `negative_result_policy` | 零/负结果如何完成、发布或关闭？ |
| `reopen_conditions` | 什么情况必须退回 study 或 umbrella？ |
| `owner_decision` | 谁在何时授权创建 paper repo 和执行大规模实验？ |

晋级完成后再生成 promotion receipt，双向绑定：

```text
candidate bundle Git blob
source study commit(s)
paper repository URL
paper initial commit
paper experiment namespace
created_at
owner decision record/blob
```

跨仓事务不能假装原子 commit。顺序必须是：

1. study 提交并冻结 candidate bundle；
2. umbrella 登记 owner paper GO 与 source blobs；
3. 经明确远程授权创建 paper repo；
4. paper 首提交包含 promotion manifest 和迁入代码；
5. umbrella 回填 paper initial commit，形成不可变 receipt；
6. paper CI 与 workspace checks 通过后才允许首次大规模模型触达。

## 7. 目标工程拓扑

```text
exploring-l4-intelligence/                   # umbrella Git repository
├── common/                                  # stable cross-stage/cross-repo utilities only
├── docs/
│   ├── datasets.lock.json                   # program-level data/model identity
│   ├── superpowers/specs/                   # engineering design proposals/specs
│   ├── superpowers/plans/                   # accepted implementation plans
│   └── checks/
│       ├── studies/<study>/<release>/       # Stage-2 readiness receipts
│       ├── papers/<paper>/<release>/         # Stage-3/release receipts
│       └── promotions/<paper>/<release>/     # study→paper handoff verification
├── scripts/                                 # umbrella governance and workspace checks
├── studies/
│   ├── README.md                            # umbrella tracked
│   ├── registry.json                        # umbrella tracked; admitted Stage-2 repos
│   └── <semantic-study-slug>/               # independent Git/GitHub; umbrella ignored
├── papers/
│   ├── README.md                            # umbrella tracked
│   ├── registry.json                        # umbrella tracked; admitted Stage-3 repos
│   └── <semantic-paper-project-slug>/        # independent Git/GitHub; umbrella ignored
└── wiki/
    ├── Research-Objective.md                # HOT program endpoint, compact router
    ├── Experiment-Assets.md                 # cross-stage asset authority
    ├── directions/<semantic-direction>/     # direction state and study routing
    └── experiments/
        ├── studies/<study-slug>/             # Stage-2 probes/baseline/candidates
        └── papers/<paper-slug>/              # Stage-3 experiment/publication ledger
```

`studies/` 和 `papers/` 都是 umbrella 下的本地 checkout 容器，而不是 monorepo 子模块。伞仓只跟踪
两个根目录各自的 `README.md` 与 registry；每个子目录拥有独立 `.git`、origin、CI、issues 和 releases。

建议继续平铺，不使用 `studies/<direction>/<study>/` 或 `papers/<study>/<paper>/`。父子关系由 registry
和不可变 promotion receipt 表达，避免嵌套 Git、路径重命名和一个 parent repo 意外拥有子仓内容。

## 8. 仓库职责与建议内部布局

### 8.1 Umbrella

继续拥有：

- program thesis、HOT state、direction governance 与 owner decisions；
- 文献 registry、survey workbench 和 audit；
- study/paper registries 与 promotion receipts；
- program-level dataset/model lock 与 acquisition；
- `common/` 中真正跨仓稳定的能力；
- workspace、provenance、asset、context 和 publication checks。

Umbrella 不拥有某个 study/paper 的活动实验实现，也不复制 raw outputs。

### 8.2 Study repository

建议最小布局：

```text
<study>/
├── src/<study_package>/
│   ├── baselines/             # reproduction and readiness adapters
│   ├── measurement/           # scorer, trace, information-boundary checks
│   ├── probes/                # bounded feasibility only
│   └── theory/                # executable formal/statistical objects when applicable
├── configs/
│   ├── baseline/
│   └── probe/
├── docs/
│   ├── research-question.md
│   ├── prior-and-gap-analysis.md
│   ├── mechanism-and-formalization.md
│   ├── experiment-design.md
│   ├── exposure-ledger.md
│   └── paper-candidates/
├── tests/
├── scripts/
│   ├── reproduce-baseline.sh
│   └── run-probe.sh
├── pyproject.toml
└── uv.lock
```

具体目录可按语言和课题调整，但必须能清楚区分 baseline/probe 与 paper-scale experiment。

### 8.3 Paper repository

建议最小布局：

```text
<paper>/
├── src/<paper_package>/
│   ├── method/
│   ├── baselines/
│   ├── experiments/
│   ├── scoring/
│   └── analysis/
├── configs/
│   ├── discovery/
│   ├── confirmatory/
│   └── ablation/
├── docs/
│   ├── promotion-manifest.md
│   ├── protocol.md
│   ├── exposure-ledger.md
│   └── deviations.md
├── manuscript/
├── figures/                   # source + deterministic renderers, not ad-hoc screenshots
├── tables/                    # source + deterministic renderers
├── supplement/
├── tests/
├── scripts/
│   ├── reproduce.sh
│   ├── evaluate.sh
│   └── build-paper-artifacts.sh
├── artifact-manifest.json
├── pyproject.toml
└── uv.lock
```

影响科学结果的数据处理、统计与 figure/table 生成代码属于 paper repo；纯排版资产可留在
`manuscript/`。数据、权重、raw trace 和大结果仍位于 `SPEECHRL_DATA_DIR`/MLflow，并由 hash/URI 引用。

## 9. Registry 与机器契约

### 9.1 Study registry v3

建议从当前 v2 升级，至少增加：

```json
{
  "schema": "study-repository-registry-v3",
  "studies": [
    {
      "name": "speech-aware evidence acquisition",
      "slug": "speech-aware-evidence-acquisition",
      "direction_slug": "speech-aware-evidence-acquisition",
      "source_provenance": "system-first-stage1c-v2:R2",
      "local_path": "studies/speech-aware-evidence-acquisition",
      "github_repo": "https://github.com/<owner>/speech-aware-evidence-acquisition.git",
      "default_branch": "master",
      "lifecycle": "topic-analysis",
      "decision_record": "<umbrella owner study contract>",
      "decision_record_blob": "<git blob>",
      "study_index": "<umbrella study index>",
      "candidate_registry": "<study paper-candidate index>"
    }
  ]
}
```

建议 lifecycle：

```text
topic-analysis | baseline-qualification | candidate-development |
paper-candidate-ready | paused | complete | sunset
```

`paper-candidate-ready` 不代表已获 paper execution authority；它只表示可以请求 paper GO。

### 9.2 Paper registry v1

建议新增：

```json
{
  "schema": "paper-repository-registry-v1",
  "local_root": "papers",
  "repo_creation_gate": "OWNER_GO_AND_PAPER_EXECUTION_CONTRACT",
  "papers": [
    {
      "name": "<semantic paper project name>",
      "slug": "<semantic-paper-project-slug>",
      "primary_study": "speech-aware-evidence-acquisition",
      "supporting_studies": [],
      "candidate_contract": "<umbrella path>",
      "candidate_contract_blob": "<git blob>",
      "promotion_receipt": "<umbrella path>",
      "local_path": "papers/<slug>",
      "github_repo": "https://github.com/<owner>/<slug>.git",
      "default_branch": "master",
      "package_name": "<semantic package>",
      "experiment_namespace": "<semantic namespace>",
      "lifecycle": "engineering",
      "created_at": "YYYY-MM-DD",
      "paper_index": "<umbrella paper index>"
    }
  ]
}
```

Paper slug 应描述核心方法/claim，而不是 venue、年份、R2、Paper-1 或临时标题。标题和投稿 venue 会变，
工程身份不应随之改名。

### 9.3 Checker 要求

现有 `study_workspace_check.py` 不应简单复制一份后独立漂移。建议提取共享 registry/Git/remote/blob
验证器，再提供 study/paper 两类 schema 和 promotion graph 检查。至少机器验证：

- `studies/*/` 与 `papers/*/` 各自只出现已登记独立 Git repo；
- slug、local path、GitHub basename、package 和 experiment namespace 一致且不含 candidate ID；
- origin、branch、decision blob、index frontmatter 与 lifecycle 一致；
- paper 的 primary/supporting studies 均存在；
- candidate contract 与 promotion receipt 的 blob/commit 完全匹配；
- paper initial commit 含 promotion manifest；
- paper confirmatory reservation 不与其他 paper 未声明冲突；
- inherited exposure 不少于来源 study；
- paper-scale experiment 不能登记到 study namespace；
- active paper 不要求全部详细写入 5KB HOT 页，而由稳定 registry/router 可达；
- registry/count/index/asset inventory 可确定性重建；
- 新 schema 和每个失败模式都有单元测试。

## 10. 代码、知识与资产的晋级规则

### 10.1 代码不得无来源搬运

Study 到 paper 的每个文件必须分类：

- `COPY`：复制并登记 source commit/path/blob 与目标 path；
- `DEPEND`：paper 通过 exact commit/release pin 消费；
- `REIMPLEMENT`：只继承接口/合同，paper 重新实现并说明原因；
- `REJECT`：明确不进入 paper，例如 scratch、未验证 probe 或越界实现。

不得整仓复制 `.git`、未筛选历史结果、cache 或 raw artifacts。Paper repo 独立不等于没有依赖；它意味
着 remote、历史、CI、release 和决策独立，所有外部依赖都被精确 pin。

### 10.2 什么应进入 common

只有至少两个真实 study/paper consumers 需要、接口稳定且不携带某篇 paper claim 的能力，才晋升
`common/`。不能把 study repo 当成未来 papers 的隐式共享库，也不能为了避免复制过早把探索代码提升
为 program infrastructure。

### 10.3 大资产继续保持单一 authority

- 数据/模型 identity：`docs/datasets.lock.json`；
- 大字节：`SPEECHRL_DATA_DIR`；
- run tracking：MLflow；
- study/paper repo：代码、配置、tests、小 fixtures 和 manifests；
- umbrella Wiki：生命周期、合同、hash、URI、偏差和决策。

新增 `papers/` 不得复制数据、权重或 raw outputs。

## 11. 当前 SAEA 的过渡裁决建议

### 11.1 身份

建议将 `studies/speech-aware-evidence-acquisition/` 明确保留为 Stage-2 study，而不是把它改名为
paper repo。其研究问题足以形成多个候选改进点，当前代码、E0、baseline 和 bounded probes 都有合法的
study-stage 归属。

### 11.2 当前序列的阶段映射

| 当前工作 | 拟议归属 | 边界 |
|---|---|---|
| E0 identity/leakage/scorer/trace | Study | 全部保留，model-free/readiness |
| runtime receipt | Study | 为合法 probe/baseline 调用建立基础，不自动授权规模实验 |
| R0 vertical slice | Study | 只验证 wiring/measurement，不作优越性 claim |
| R1 closest-prior reproduction | Study | paper candidate 的硬前置；失败显式 `INCONCLUSIVE` |
| X directional exploration | Study | 必须 bounded、使用 discovery、用于 candidate selection |
| production-scale method implementation | Paper | 需要独立 paper GO |
| large-scale confirmatory | Paper | 需要冻结 protocol 与未读 reservation |
| final superiority/generalization claim | Paper | 正/零/负结果同等登记 |
| manuscript/submission/publication | Paper | 独立 repo/release 生命周期 |

### 11.3 现行合同处理

本文不能单方面收窄已经签发的 `OWNER_GO_AND_EXECUTION_CONTRACT`。若 owner 接受三阶段模型，应新增
带日期 amendment：

1. 确认 SAEA 是 study-stage carrier；
2. 明确 E0/R0/R1/bounded X 的剩余授权；
3. 在 paper-scale implementation、large confirmatory 和最终论文 claim 前设置 stop line；
4. 定义首个 paper candidate 的申请入口；
5. 保留此前 exposure、预算和历史授权事实，不回写旧合同。

当前 experiment index 尚无正式实验，因此现在建立阶段边界的迁移成本最低；但“尚无实验”不是本文
自动授权迁移或建仓的理由。

## 12. 实施交易建议

### T0 — Owner architecture ruling

所属：umbrella。

- 裁决是否接受三阶段 carrier 模型；
- 冻结 stage 名称和两次 gate token；
- 裁决 paper 是否允许多个 supporting studies；
- 明确负结果、回流和非论文成果政策；
- 指定本提案的 accepted/superseded 状态。

T0 之前不得创建 `papers/` checkout 或远程仓。

### T1 — Governance and schema design

所属：umbrella。

- 更新 `wiki/AI-Collaboration.md` 的 canonical placement/lifecycle；
- 设计 study registry v3、paper registry v1 与 promotion receipt schema；
- 更新 `CONTRIBUTING.md`、`studies/README.md` 和 architecture/current routers；
- 决定 Wiki index 的兼容迁移路径；
- 写失败模式和 schema tests，再实现 checker。

### T2 — Papers workspace foundation

所属：umbrella。

- 新增 `papers/README.md`、空 `papers/registry.json`；
- `.gitignore` 精确忽略 `papers/*/`，保留 registry surface；
- 实现 paper workspace 与 promotion graph checks；
- 新增 deterministic paper asset inventory；
- 不创建任何 paper 子目录或 GitHub remote。

空 registry 是合法状态；空 paper repo 不是。

### T3 — Reclassify current SAEA boundary

所属：umbrella + SAEA study repo，需 owner dated amendment。

- 将 current truth、entry contract 和 study README 对齐到 Stage-2 职责；
- 将 paper-scale actions 移出 study 的默认授权；
- 保留 E0/R0/R1/bounded X；
- 在 study 内新增 paper-candidate schema/template；
- 更新 tests，证明 study runner 不会误启动 paper confirmatory。

### T4 — Promotion mechanism dry run

所属：umbrella + SAEA，不创建真实 paper remote。

- 使用 synthetic candidate fixture 测试 bundle、blob pin、code migration manifest、exposure inheritance、
  confirmatory reservation 和 receipt；
- 模拟跨仓非原子失败及恢复；
- 验证重复 paper namespace、重复 reservation、缺失 source commit 均 fail closed。

### T5 — First paper admission

只有当真实 candidate 达到 Stage-2 退出门，并获得 owner 明确授权时执行：

- 签发 `OWNER_GO_AND_PAPER_EXECUTION_CONTRACT`；
- 创建独立 GitHub repo 与 `papers/<slug>/` checkout；
- 完成 promotion transaction 和初始 CI；
- 通过 paper workspace/reproducibility gate；
- 最后才允许合同范围内的大规模模型执行。

### T6 — Consolidation and historical closure

- HOT 页只保留当前方向、活动 studies/papers 摘要和下一个动作；
- registries 与稳定 index 承担完整路由；
- 已被接受架构取代的旧 specs 标记 superseded，但不改写历史正文；
- 运行 context budget、manifest、archive/safe-move 与 audit immutability checks。

## 13. 风险与缓解

| 风险 | 严重度 | 缓解 |
|---|---|---|
| 三层结构增加流程成本 | MAJOR | 只有获准对象建仓；registry/templates/checks 自动化；不为 candidate 或空 paper 预建仓 |
| Study 与 paper 重复代码 | MAJOR | promotion manifest；COPY/DEPEND/REIMPLEMENT/REJECT；稳定共用能力才进 common |
| Study 无限扩张成方向杂物仓 | MAJOR | 独立机制/baseline/边界/停止决策触发 study split；设置 closure criteria |
| 为晋级追逐正 pilot | BLOCKER | 预注册候选比较规则；confirmatory 未读；零/负结果合法；报告所有候选 exposure |
| 多 paper 重用测试集 | BLOCKER | program-wide reservation ledger、inherited exposure 和 multiplicity checks |
| Paper review 导致 scope creep | MAJOR | amendment 或退回 study；新 claim 不得静默塞入原 confirmatory |
| HOT 页面随仓数量膨胀 | MODERATE | HOT 只做 compact router；完整状态由 registries/direction indexes 管理 |
| 远程仓与本地 registry 不一致 | MAJOR | origin/branch/blob/frontmatter fail-closed checker；建仓与登记按 promotion 顺序 |
| 旧 Stage-2 文档继续授权规模实验 | BLOCKER | owner dated amendment + current truth consolidation；历史件只作 provenance |
| `papers` 名称压制非论文成果 | MODERATE | 允许独立 benchmark/tool/report release；以证据完成而非投稿成功判定研究完成 |

## 14. 验收标准

### 14.1 架构与文档

- `Project-Thesis`、`Research-Objective`、`AI-Collaboration`、`Experiment-Assets`、CONTRIBUTING 与
  registries 对三阶段定义一致；
- Stage-1/Stage-2/Stage-3 各自有允许动作、禁止动作、退出门和回流规则；
- 旧合同不被原地改写；SAEA 收窄通过 dated amendment；
- paper 成功不以正提升为必要条件；
- 数学形式只在承重时强制；
- 非论文成果与 negative result 有合法出口。

### 14.2 Workspace

- umbrella 只跟踪 `studies/`、`papers/` 的 README/registry surface；
- 每个 installed child 是独立 Git root，origin/branch 与 registry 一致；
- 无未登记 study/paper 目录；
- 空 registries 合法，空 child repositories 非法；
- candidate ID 不进入工程 slug、package、namespace；
- registry 与 Wiki count/index 可确定性对齐。

### 14.3 Promotion

- 没有 owner paper GO 时无法登记 paper；
- paper entry 必须解析 primary study、source commit、candidate blob、baseline receipt 与 promotion receipt；
- promotion receipt 双向绑定 paper initial commit；
- 代码迁移逐文件有 provenance；
- inherited exposure 单调不减；
- confirmatory reservation 冲突 fail closed；
- 失败的跨仓 promotion 可恢复，不留下“registry 已入但 repo 不存在”的活动状态。

### 14.4 Scientific execution

- Study 只能运行 model-free、baseline 和 bounded probe profiles；
- Paper-scale/confirmatory profile 在缺少 paper contract/runtime receipt/protocol freeze 时拒绝执行；
- discovery 与 confirmatory 隔离；
- 正、零、负结果使用相同 artifact/reproducibility 标准；
- 每个 paper release 可从 clean clone + pinned shared assets 重建；
- MLflow、artifact URI/hash、model/data revision、config/protocol hash 全部可解析。

### 14.5 建议检查命令

现有检查继续作为基线：

```text
python scripts/checks/code_graph_check.py
python scripts/checks/study_workspace_check.py --require-installed
python scripts/checks/legacy_asset_resolution_check.py --verify-bundles
python scripts/checks/ai_context_surface_check.py
python scripts/checks/build_ai_context_manifest.py --check
pytest common/tests
```

整改应新增或等价覆盖：

```text
python scripts/checks/paper_workspace_check.py --require-installed
python scripts/checks/research_promotion_check.py
python scripts/checks/research_asset_graph_check.py
pytest scripts/checks/test_paper_workspace.py
pytest scripts/checks/test_research_promotion.py
```

工具名可在实施设计中调整，但不得降低上述语义覆盖。

## 15. 非目标

本提案不：

- 直接判定 SAEA 的某个改进点已经可以写 paper；
- 创建或命名第一篇 paper；
- 创建远程仓、push、发布 Wiki 或投稿；
- 自动把现有 study 代码复制到未来 paper；
- 删除、移动或重写已注册 audit/experiment 记录；
- 改变 TF-Strict、speech-only、black-box、information-boundary 等研究边界；
- 用新的目录结构替代学术 novelty、baseline readiness 或实验有效性判断；
- 承诺任何实验一定获得正向提升。

## 16. 请求 owner 与工程团队裁决

请逐项回复：

1. 是否接受 `umbrella → studies → papers` 为三个连续研究阶段和工程载体？
2. 是否接受“study 终点 = paper candidate qualified，而非最终论文实验完成”？
3. 是否接受“paper 成功 = 对预注册 claim 作出可靠判断，而非必须正提升”？
4. 是否接受两个独立 gate，并由 owner 确认最终 token 名称？
5. 是否同意当前 SAEA 保留为 study，并通过 dated amendment 增加 paper-scale stop line？
6. 是否接受一个 paper 默认一个 primary study、可有多个 supporting studies？
7. 是否接受 program-wide confirmatory reservation 与 inherited exposure 硬门？
8. 是否批准工程团队先实施 T1–T4 的无模型、无远程基础设施，再单独申请首个 paper admission？

建议裁决：**接受总体架构，要求工程团队先提交 schema、checker 和 SAEA 边界 amendment 的实施计划；
在这些基础设施通过独立 review 前，不创建首个 paper repo，也不把任何 study probe 升格为最终论文证据。**

