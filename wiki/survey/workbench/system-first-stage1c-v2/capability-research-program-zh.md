---
title: "Stage-1B 能力导向增量映射与 Stage-1C v2 研究方案"
artifact_id: "SF-STAGE1B-DELTA-STAGE1C-V2-CAPABILITY-PROGRAM-2026-07-23"
date: "2026-07-23"
status: "OWNER_AUTHORIZED_INPUT_SUPERSEDED_BY_STAGE1B_DELTA_RC1"
authority_effect: "NONE"
requested_owner_verdict: "GRANTED_AUTHORIZE_STAGE1B_CAPABILITY_DELTA_MAPPING"
supersedes_owner_review_draft_commit: "ddef229"
authorization_recorded_at: "2026-07-23"
superseded_by: "wiki/survey/workbench/system-first-stage1b-capability-delta/stage1c-v2-capability-research-program-zh.md"
stage1b_v5_mutation_requested: false
current_activation_requested: false
experiment_execution_requested: false
novelty_verdict_requested: false
---

# Stage-1B 能力导向增量映射与 Stage-1C v2 研究方案

## 0. Owner 决策（已登记）

Owner 已于 2026-07-23 授予：

`AUTHORIZE_STAGE1B_CAPABILITY_DELTA_MAPPING`

授权后的 Stage-1B delta 已形成 release candidate；当前机器 census 为 296 个 canonical works，详细证据、
校验与更新后的中文 proposal 位于
`wiki/survey/workbench/system-first-stage1b-capability-delta/`。本文件保留为授权输入与设计 provenance，
不再作为最新 proposal。

该授权只允许对本方案列明的新增论文和有界引用邻域启动一个 Stage-1B delta campaign：锁定 canonical
identity、版本、全文与代码/数据 locator，映射研究路径、邻近性、边界、反证和论文已有实验设置，并据此
修订 Stage-1C v2 schema/codebook。它不改写 Stage-1B v5，也不直接产生
`SIGN_STAGE1B_CAPABILITY_DELTA_RELEASE` 或 `SIGN_STAGE1C_V2_EXPERIMENT_MAPPING`，更不授权研究模型/API
调用、benchmark metric、论文 reproduction、prototype、问题排名、owner selection、技术 novelty verdict
或 Stage-2A。

在独立 `SIGN_STAGE1B_CAPABILITY_DELTA_RELEASE` 登记前，Stage-1C v2 不进入批量实验映射；允许的工作限于
proposal、Stage-1B delta surface、metadata/full-text/asset locator、路径与邻近性编码、schema、codebook、
calibration packet 设计和机器检查。不得启动大规模 experiment-level coding、family conclusion、branch
formation 或任何实验执行。

## 1. 研究动机

Stage-1C v1 以三个未排序问题包组织证据：budget/stop/repair、evaluator/reward reliability 和
interactive/full-duplex objectives。第一版 v2 草案又把观察、记忆、候选、评价、选择、行动、停止、
修复和交互恢复九个控制算子错误提升成“一级能力”。这些算子适合解释系统怎样工作，却不适合回答
“我们通过引入什么能力资产来提高任务表现”。

Owner 提出的知识、技能、记忆划分更接近可研究的干预对象，但不能机械地做成三个互斥文件夹：

1. 知识回答“知道什么”，技能回答“在何种状态下怎样做”，记忆回答“跨时间保留、检索、更新什么”；
2. 知识和技能都可以被记忆系统保存，episodic experience 也可以被进一步编译成知识或技能；
3. training-free RL 是 reward/value/advantage 驱动下一动作的控制原则，multimodal agent system 是承载
   知识、技能、记忆和控制循环的系统载体，两者不是同一类型的并列维度；
4. 一个“多模态任务”不自动构成“多模态知识、技能或记忆”，必须证明非文本信息进入资产表示或决策，
   并排除 text-only shortcut。

因此本方案采用三轴本体：

`能力资产 K/S/M × multimodal agent system 载体 × training-free reward-guided control`

原九项降级为二级机制标签，用来解释 K/S/M 如何被获取、表示、保存、检索、组合、评价、选择、执行、
停止和修复。论文研究方向由被改变的一级变量决定，而不是由论文标题或系统组件名称决定。

同时，本轮检索发现多篇可能改变 Stage-1B 路径空间的 2026 年工作。科学流程不能把这些论文直接塞入
Stage-1C；必须先回到 Stage-1B 的职责，形成不改写 v5 的有界增量 release。新的主数据流为：

`有界新增论文 → Stage-1B delta 锁定与邻近性映射 → 独立签署 delta release → 实验单元/实验族 → K/S/M 方向 → research branch`

Stage-1C v1 的三个 bundles、九维 rubric 和 Stage-1B v5 均保留为不可改写 provenance，但不再限制新的
能力导向研究方向。

## 2. 核心研究问题

本研究程序回答七个问题：

1. 哪些论文真正改变了 multimodal agent system 本身，哪些分别引入或激活了知识、技能、记忆？
2. 系统、知识、技能、记忆的边际贡献能否在同一 frozen core、数据、工具、预算阶段和评价合同下分离？
3. 所谓“多模态知识/技能/记忆”是否在表示与决策上需要非文本证据，还是只是多模态任务上的文本资产？
4. training-free RL 能否在不改核心权重的前提下，用 reward/value/advantage 决定 K/S/M 的获取、选择、
   组合、更新、停止或修复，而不是只做离线评分？
5. 哪些实验在问题、结果语义、环境、access 和 baseline→intervention 因果比较上属于同一 family？
6. 哪些新文本/VLM/omni 论文改变了 Stage-1B 的方法路径或 nearest-prior 关系，必须先进入 delta release？
7. 哪些 family 具有本地资产、可观察 outcome、nearest prior、falsifier 和 kill criterion，足以形成
   reproduction-first Stage-2A 候选 branch？

Stage-1C v2 不回答“哪个新算法最创新”或“哪个 branch 已经获胜”。

## 3. 证据面：冻结基础层、CURRENT overlay 与动态引用扩展

### 3.1 三层证据账本

证据面严格分层：

| 层 | 含义 | 变更规则 | 允许用途 |
|---|---|---|---|
| `FROZEN_BASE_226` | Stage-1B v5 固定 registry 的 226 个 canonical records | 只读，不回写 | frozen denominator、portfolio role、基础 paper audit |
| `CURRENT_INHERITED_OVERLAY` | CURRENT v1 中 registry 外、但对现行比较承重或构成明确边界的 canonical works | 由 CURRENT manifest 和 canonical union 生成 | 继承 priority intake、59-route appendix、routing correction、H5 status |
| `STAGE1B_CAPABILITY_DELTA_CANDIDATES` | 因 K/S/M、multimodal agent system 或 training-free RL 路径而新增的有界候选 | 先进入 Stage-1B delta；append-only snapshot；必须去重、说明触发来源 | 路径、邻近性、边界、反证与实验设置映射；签署前不得支撑 Stage-1C 结论 |

不得把 overlay 写回 `FROZEN_BASE_226`，也不得用 overlay 改写 Stage-1B v5 的历史计数。

### 3.2 当前分母的初步核验

本轮本地核验发现：

- frozen registry：226；
- CURRENT 59-route reference appendix：59 个 canonical routes，其中 7 个与 base 226 重叠，52 个在 base 外；
- TRACE、S2S-Arena、MTalk-Bench、SimulU 四项 priority intake 不在上述 union；
- 第一版草案的已知最小 canonical union 是 `226 + 52 + 4 = 282`，而不是 `230`；
- 本轮 K/S/M 调研又发现八个在 CURRENT/registry 中未命中的 exact arXiv IDs：Anything2Skill
  (`2606.09316`)、MMSkills (`2605.13527`)、XSkill (`2603.12056`)、RESOURCE2SKILL
  (`2606.29538`)、GEMS (`2603.28088`)、Skill Retrieval Augmentation (`2604.24594`)、RMR
  (`2405.20834`) 和 M2A (`2602.07624`)；
- proposal 时点的已知最小下界为 `290`；授权执行后又从有界一跳引用中提升 6 个 exact-ID works，且机器
  去重确认它们均不在既有 282 中，因此 release-candidate surface 为 `296`。

`296` 是当前 release-candidate census，不是签署后的冻结事实，也不是文献宇宙闭合。checker 已从 registry、
reference appendix、priority intake、delta records 与 citation ledger 重算；只有通过独立
`SIGN_STAGE1B_CAPABILITY_DELTA_RELEASE` 后才可进入 Stage-1C denominator。

所有 surface records 都需要一次 paper-level disposition；只有承重 empirical works 才要求进行有界但完整的
experiment extraction。非承重、理论、negative 或 boundary works 可作为 non-cell evidence node。

### 3.3 引用扩展与事实刷新

引用扩展是正常研究行为，但必须有界、可追溯：

1. 允许触发源：已登记 paper 的 backward/forward citation、dataset/benchmark 原始论文、nearest-prior、
   explicit falsifier、instrument dependency、论文修订版，以及本方案八个 exact-ID seeds 的一跳引用邻域；
2. 每个新增 work 记录 `discovery_mode=CITATION_EXPANSION`、`parent_work_ids`、query/edge reason、
   canonical identity、official URL、retrieved-at、版本、全文 locator/hash、初始 role；
3. 先 canonical dedup，再由 Stage-1B delta 决定 `DIRECT_PATH / COMPONENT_PATH / INSTRUMENT /
   NEGATIVE_OR_FALSIFIER / BOUNDARY / REFERENCE_ONLY / EXCLUDE_WITH_REASON`；
4. 不因引用扩展重新开启无界关键词 discovery；
5. 每次新增、版本漂移、资产状态变化或路径关系变化后生成新的 immutable Stage-1B delta snapshot；
6. `SIGN_STAGE1B_CAPABILITY_DELTA_RELEASE` 后才把已签署 delta 并入 Stage-1C 输入；family/branch portfolio
   评审前再冻结 exact Stage-1C snapshot。冻结后出现的新承重证据只能通过新的 delta
   transaction 使结论失效或触发复审，不能原位改写历史证据。

刷新至少发生在 calibration 前、scale-out 前、family conclusion 前和 branch portfolio freeze 前。

## 4. 三轴能力与系统本体

### 4.1 一级能力资产：知识、技能、记忆

三条能力线并列重点，不预设技能优于知识或记忆：

| ID | 一级方向 | 操作性定义 | 不计入该方向的情形 | 必需的最小对照 |
|---|---|---|---|---|
| `K_KNOWLEDGE` | 多模态知识 | 为当前任务提供可陈述的事实、概念、关系、非执行性约束或跨模态 grounded evidence，回答“知道什么/依据什么” | 可直接执行的动作流程、单纯扩大模型、重复当前输入、没有检索/构造差异的 CoT | same system/core 下 `no external knowledge`、`text knowledge`、`multimodal knowledge`；可定义时加入 oracle evidence |
| `S_SKILL` | 多模态技能 | 可复用、可调用、带适用条件的程序性知识，至少描述 when/when-not、前置条件、动作/工具步骤、验证或失败条件，回答“何时怎样做” | 普通 prompt、单个 demonstration、无复用边界的轨迹摘要、只有工具列表 | `no skill`、`text-only skill`、`state-conditioned skill`、`multimodal skill`，并做 held-out task/trajectory 检查 |
| `M_MEMORY` | 多模态记忆 | 跨 step/session/episode 对信息或经验进行保留、索引、检索、更新、冲突处理和遗忘，回答“过去什么仍应影响现在” | 当前 prompt 中天然可见的短上下文、只增加 context window、无跨时状态差异的 scratchpad | `no memory/current context`、`raw history/long context`、`text-compressed memory`、`evidence-preserving multimodal memory` |

知识和技能是可存储的资产类型，记忆是跨时间的能力与机制。为防止本体重叠，每篇论文同时编码：

- `asset_content_type = DECLARATIVE_KNOWLEDGE / PROCEDURAL_SKILL / EPISODIC_EXPERIENCE`；
- `persistence_scope = NONE / WITHIN_EPISODE / CROSS_EPISODE / LONG_TERM`；
- `primary_intervention = KNOWLEDGE / SKILL / MEMORY`。

例如 SkillBank 是技能资产加持久化容器；若实验只改变 skill content，primary 是 `S_SKILL`；若保持 skill
content 不变而改变写入、检索、更新或遗忘策略，primary 才是 `M_MEMORY`。不能因论文使用了向量库就自动
归为记忆，也不能因 memory 中保存了 workflow 就同时声称技能与记忆的因果收益。

为贴合项目“激活预训练知识”的 north star，K/S/M 还需要二级类型：

- Knowledge：`LATENT_PARAMETRIC_ACTIVATION`、`EXTERNAL_DECLARATIVE_KNOWLEDGE`、
  `QUERY_SCOPED_GROUNDED_EVIDENCE`；前者不增加外部知识，只改变 frozen model 已有知识的可达性；
- Skill：`TEXT_PROCEDURE`、`EXECUTABLE_TOOL_PROGRAM`、`STATE_CONDITIONED_MULTIMODAL_SKILL`；只有最后一类
  在通过 MM2/MM3 后可称多模态技能；
- Memory：`WORKING_STATE`、`EPISODIC_TRACE`、`SEMANTIC_MEMORY`、`EVIDENCE_PRESERVING_MULTIMODAL_MEMORY`；
  “procedural memory”按 stored content 记为 skill、按 persistence intervention 记为 memory，避免重复归因。

### 4.2 系统载体与控制原则不是能力资产

| 轴 | ID | 定义 | 研究问题 |
|---|---|---|---|
| 系统载体 | `SYS_MULTIMODAL_AGENT` | 围绕同一 frozen core 组织 planner、specialist、tool、state、evaluator、action 和交互 loop | 单纯搭建 agent system 是否在不增加 K/S/M 资产时提高任务表现？哪些收益来自 decomposition、tool access 或多模型 federation？ |
| 控制原则 | `CTRL_TRAINING_FREE_RL` | 不更新核心权重，由显式 reward/value/advantage 改变下一项外部动作、资产选择、轨迹、停止或修复 | reward 是否比静态规则、相似度检索、self-consistency 或 LLM-as-planner 更有效地调度 K/S/M？ |

`SYS_MULTIMODAL_AGENT` 是 K/S/M 的承载体；`CTRL_TRAINING_FREE_RL` 是可施加在系统上的决策机制。一个
系统只有多 agent、reflection 或 verifier，不等于 training-free RL。若 score 没有改变下一动作，它仍只是
measurement；若使用 similarity/top-k 或固定规则，也不能因“像强化学习”而编码为 RL。

“不更新核心权重”也不等于“没有学习”。Stage-1B/1C 必须另记：

- `core_parameter_update`：是否改变 frozen core；本项目 direct path 必须为 false；
- `external_asset_construction`：K/S/M 是否由人工、其他模型、成功/失败轨迹或标注数据构造；
- `external_asset_online_update`：推理期间是否写入、合并或淘汰知识、技能、记忆；
- `label_or_test_exposure`：构造和选择是否使用 ground truth、evaluation task 或测试轨迹；
- `reward_next_action_effect`：reward 是否真实改变下一步外部控制。

Anything2Skill、XSkill、RESOURCE2SKILL 等即使不更新核心参数，也可能在外部资产上发生 compilation、
consolidation 或 continual learning；它们可以属于 training-free system，但不能被描述为“没有学习成本”。

由此形成五条候选研究方向：

1. `D0_SYSTEM_HARNESS`：搭建 multimodal agent system 的纯系统边际收益；
2. `D1_MULTIMODAL_KNOWLEDGE`：激活/引入跨模态知识与证据；
3. `D2_MULTIMODAL_SKILL`：构建、检索、组合与执行跨模态状态条件技能；
4. `D3_MULTIMODAL_MEMORY`：保留、检索、更新并验证跨时多模态证据与经验；
5. `D4_TF_RL_ORCHESTRATION`：用 training-free reward-guided control 调度系统与 K/S/M。

五条方向不排序。D1、D2、D3 都是一级重点；D4 不是第四种资产，而是项目 north star 下对前三者和系统
进行外部控制的统合层。

### 4.3 “多模态”声明的四级证据门

每个 K/S/M 结果必须标注最高支持等级：

| 等级 | 含义 | 允许声称 |
|---|---|---|
| `MM0_TEXT_ONLY` | 资产和决策均为文本 | 文本 transfer comparator |
| `MM1_MULTIMODAL_TASK_ONLY` | 任务输入含图像/音频/视频，但资产可能仍是文本 | 多模态任务上的 K/S/M，不得称多模态资产 |
| `MM2_MULTIMODAL_ASSET` | 知识、技能或记忆本身保留非文本 evidence/reference | 多模态资产已实现，尚不能证明必要性 |
| `MM3_CAUSALLY_MULTIMODAL` | same-run 配对消融表明移除/替换非文本信息会改变正确决策或 outcome，且排除 text shortcut | 非文本信息对该 K/S/M 干预具有因果贡献 |

MMSkills 的文本 procedure＋state cards＋keyframes 是 `MM2` 候选；其 no-skill、text-only、去 state-card、
去 image 和完整 package ablation 才可能支持 `MM3`。MemLens 的 image ablation 是 memory evaluation 的
强 modality-necessity 设计。相反，仅在图片问题上调用文本 RAG 只能编码为 `MM1`。

H5 closure 前，`MM3` 只允许支撑特定任务内的 modality necessity，不得上升为 speech 相对 vision/text
的普遍特殊性结论。

### 4.4 二级机制标签

原九项不删除，改作解释干预如何生效的多标签字段：

`OBSERVE_ACQUIRE`、`STATE_STORE_UPDATE`、`CANDIDATE_OR_COMPOSE`、`EVALUATE`、`SELECT_ROUTE`、
`ACT_TOOL_ENV`、`BUDGET_STOP`、`REPAIR_ROLLBACK`、`INTERACTION_RECOVERY`。

Family 的一级标签是 `primary_direction_id`，二级标签是 `mechanism_ids`。若 system、K/S/M 或 reward-control
同时变化且没有 factorial/ablation 分离，必须标记 `CAUSAL_ATTRIBUTION_UNRESOLVED`，不能把整包系统增益
分摊给多个能力。

### 4.5 跨领域证据的作用

文本和 VLM 工作可以作为 K/S/M 机制、系统或控制协议的 analogue，但不提供 speech/omni 数值外推：

- RMR、multimodal search agents 提供知识检索、证据充分性和 text-vs-multimodal knowledge 对照；
- Anything2Skill 提供“declarative knowledge→procedural skill”的编译边；
- MMSkills、XSkill、RESOURCE2SKILL 提供多模态技能表示、经验/技能拆分与 runtime grounding；
- MemLens、MMA、M2A、Visual Agentic Memory 提供长时、更新、冲突、视觉保真和 refusal 的记忆协议；
- GEMS、MM-ReAct、MLLM Orchestration、Agent-Omni 提供系统 harness 与 specialist orchestration；
- LATS、Training-Free GRPO 和 reward-guided SMC 提供 search、experience prior 或 reward-tilted inference 的
  control boundary，但必须重新核查是否满足本项目“reward 决定下一外部动作”的严格合同。

这些工作在 Stage-1B delta 先获得路径/角色；进入 Stage-1C 后再成为 `CORE_MEMBER`、`TRANSFER_ANALOGUE`、
`FALSIFIER` 或 `INSTRUMENT_SUPPORT`。target speech experiment 的 problem、outcome、environment/access 和
paired comparison 必须独立成立。

### 4.6 “参考、借鉴、复现”关系合同

任何外部工作进入 Stage-1C 时必须恰好声明一种主关系，不能用“相关工作”混写：

| 关系 | 稳定标签 | 我们实际做什么 | 可以声称什么 | 禁止声称什么 |
|---|---|---|---|---|
| 参考 | `REFERENCE_CONTEXT` | 用其概念、失败分类、背景或研究问题帮助解释本项目 | “该工作提示/定义/报告了某现象” | 不得声称使用了其方法、复现了其结果或可直接比较 |
| 借鉴/模仿 | `BORROWED_PROTOCOL_ANALOGUE` | 迁移其实验结构、对照组、ablation、environment state、milestone 或 evaluator contract，并为 speech/omni 重建协议 | “本实验由某协议启发，借用了哪些设计元素” | 不得把改造后的实验叫复现；不得继承原论文数值或结论 |
| 复现 | `REPRODUCTION_ANCHOR` | 按论文的 method、data/revision、split、model/access、prompt/config、metric 与 evaluator 尽可能重建实验 | “exact/close reproduction 的一致与差异” | 配置、数据或 access 实质改变时不得声称 exact reproduction |

复现进一步分为：

- `EXACT_REPRODUCTION`：关键 comparability key 全部匹配；
- `CLOSE_REPRODUCTION_WITH_DECLARED_DEVIATIONS`：存在明确但有界的实现或版本偏差；
- `TASK_MATCHED_METHOD_TRANSFER`：方法迁移到 speech/omni 新任务，只能称“方法迁移”，不能称原实验复现。

由文本/VLM 设置模仿提出的新 speech/omni 实验必须标记 `PROPOSED_BY_PROTOCOL_ANALOGY`，同时记录：

1. source protocol；
2. 被借用的设计元素；
3. 被改变的 modality/task/environment；
4. 为什么这种改变仍保留相同 decision structure；
5. speech/omni 中是否已有 nearest analogue；
6. 能否证伪、strongest alternative 和 kill criterion。

如果 speech/omni 已经存在高度匹配的实验设置，原则上先把它作为 reproduction anchor，再判断是否需要
新增设置；不能绕过最近先行工作，直接把跨领域模仿包装成新设计。

## 5. 规范化实验数据模型

### 5.1 原子运行与比较关系分离

不再让一个 experiment cell 同时表示“单次运行”和“baseline→method 比较”。数据模型拆成：

```text
paper_record
  └─ run_cell[]
       └─ observation[]

paired_comparison
  ├─ baseline_run_cell_id
  ├─ intervention_run_cell_id
  ├─ matched_fields[]
  ├─ differing_fields[]
  └─ pairing_status
```

一个 `run_cell` 是一个原子 arm，identity 至少包含：

- paper/work、table/figure/experiment block；
- dataset canonical ID、revision、lineage node、split、sample slice；
- preprocessing、audio/input representation、prompt/template；
- core model ID/revision、frozen/weight-update 状态、access；
- system topology、agent roles、shared state 和 tool/action contract；
- primary direction、knowledge/skill/memory asset IDs、content type、source/version/provenance；
- persistence scope、write/retrieve/update/forget/conflict policy；
- multimodality level、非文本 evidence/reference 和 modality ablation condition；
- tools/retrieval/evaluator/judge identity 与 revision；
- decoding、sampling、candidate count；
- state/memory 初始化、skill/knowledge candidate pool；
- intervention、decision rights、action space、reward/value/advantage identity 及其 next-action effect；
- budget/horizon、stopping rule；
- seed/replicate 或 paper-reported aggregation；
- precise source locator。

同一 run 的多个 accuracy、WER、MOS、task success、latency、cost、harm 等是 observations，不复制
run cell。Observation 至少记录 metric identity/revision、direction、unit/scale、aggregation level、sample
size、value、uncertainty availability、reported significance 和 source locator。

### 5.2 Paired comparison

比较关系有三种状态：

| 状态 | 要求 | 允许陈述 |
|---|---|---|
| `EXACT_PAIRED` | 除 declared intervention 外，dataset/split/core/input/prompt/system topology/K-S-M pools/control regime/decoding/evaluator/budget/seed aggregation 均匹配 | within-comparison delta 和 paper-reported inference |
| `PARTIALLY_MATCHED` | 已知存在一个或多个混杂差异 | 并列结果、混杂说明；不得作干净因果归因 |
| `UNPAIRED_PARALLEL` | 不同协议或无法证明配对 | 只作定性平行证据 |

跨论文数值合并还要求 exact comparability stratum；dataset lineage 或任务相近不能替代 exact key。

### 5.3 Dataset graph

Factual lineage 和 experimental relation 保持两个 namespace：

- lineage：`SAME_REVISION / DERIVED_FROM / SUBSET_OF / TRANSLATED_FROM /
  AUDIO_RENDERING_OF / REANNOTATED_FROM / SPLIT_OF`；
- relation：`INDEPENDENT_SAME_TASK / CROSS_DATASET_VALIDATION /
  DISTRIBUTION_SHIFT_TEST / PROTOCOL_ANALOGUE`。

Lineage 必须有官方 dataset card、paper 或 release provenance；研究者判断只能生成 relation。

## 6. Experiment family

### 6.1 Family signature

一个 family 的 core signature 是：

`target failure × primary direction × K/S/M asset content × persistence scope × system topology × control regime ×
multimodality level × evaluation object × outcome semantics × environment/interaction × access ×
baseline→intervention causal contract`

Dataset 不作为 family 的唯一主键，而是 lineage/validation stratum。同一 dataset 可以因失败机制、metric、
split、access 或 intervention 不同进入多个 families。

### 6.2 Membership

- `CORE_MEMBER`：完整 signature 兼容，可解释 paired comparison；
- `VALIDATION_MEMBER`：同一失败/primary direction 上的独立数据或 shift；
- `TRANSFER_ANALOGUE`：其他领域中 decision structure 同构；
- `FALSIFIER`：挑战能力假设、信号有效性或策略因果性；
- `INSTRUMENT_SUPPORT`：提供 outcome、evaluator、校准或 measurement contract。

### 6.3 确定性证据合成

证据按三层合成：

1. paired comparison：`REPORTED_SUPPORT / REPORTED_NULL / REPORTED_NEGATIVE /
  OUTCOME_DIVERGENCE / CAUSAL_ATTRIBUTION_UNRESOLVED / UNRESOLVED`；
2. exact-comparability stratum：在同一 dataset/model/access/input/system/K-S-M pool/control/metric/budget 内解释；
3. cross-stratum synthesis：只做带 uncertainty 的定性归纳。

Family state 规则：

- `INSUFFICIENT_EVIDENCE`：没有成熟 exact-paired core evidence，或 evaluator/outcome 合同未闭合；
- `CONSISTENT_SUPPORT`：所有承重 exact strata 支持预期方向，且没有成熟 contradiction；validation
  可以提高证据成熟度，但 transfer/instrument 不能单独升级为 support；
- `MIXED`：成熟 strata 间出现 support 与 null/negative，或 primary outcome 与 harm/cost outcome 分裂，
  或 strongest falsifier 未被解释；
- `NULL_OR_NEGATIVE`：成熟 core evidence 未支持预期路径，或显示干预损害目标 outcome，且无成熟支持 strata。

不得按论文数量投票。缺少 uncertainty 不等于 null；paper-reported significance 也不能替代 protocol match。

## 7. 抽取 universe 与防 cherry-picking 规则

### 7.1 Paper disposition

每个 surface snapshot 的所有 canonical works 恰好一次 disposition：

- `EMPIRICAL_LOAD_BEARING`；
- `EMPIRICAL_RELATION_ONLY`；
- `NON_EMPIRICAL_EVIDENCE_NODE`；
- `BOUNDARY_OR_FALSIFIER`；
- `EXCLUDE_WITH_REASON`。

### 7.2 承重论文抽取范围

对 `EMPIRICAL_LOAD_BEARING`，必须抽取所有可能改变 family conclusion 的：

- 主表和 primary comparison；
- 与 system/K/S/M/TF-RL 目标方向有关的 negative/null result；
- causal mechanism ablation；
- modality necessity、text-only shortcut、asset-content 与 persistence ablation；
- dataset/access/shift 条件变化；
- failure、harm、latency/cost 或 evaluator disagreement；
- authors 用来支撑核心 claim 的 appendix comparison。

不要求把无关附录数值机械转换为 cells，但每个不抽取的相关 experiment block 必须记录 exclusion reason。
禁止只取最佳结果、只取支持性结果或用跨配置最佳值拼接 paired comparison。

### 7.3 Claim 拆分

始终分开：

1. `AUTHOR_CLAIM`；
2. `WITHIN_PAPER_EXPERIMENT_SUPPORT`；
3. `PROJECT_RESIDUAL_HYPOTHESIS`。

第三项不是 novelty verdict。

## 8. v1 继承与 emergent branch

每个 family 可以有零到多个 `legacy_bundle_links`，记录它对 v1 三个 bundles 的支持、反证或边界作用。
Family 不因无法路由到旧 bundle 就自动失效，但所有新增论文必须先通过已签署的 Stage-1B delta 进入输入面。

Branch 来源分为：

- `LEGACY_BUNDLE_REFINEMENT`：细化现有三个问题包；
- `SYSTEM_HARNESS_DIRECTION`：隔离 agent scaffold 本身的边际收益；
- `KSM_CAPABILITY_DIRECTION`：知识、技能或记忆之一构成 primary intervention；
- `TF_RL_ORCHESTRATION_DIRECTION`：reward-guided control 调度系统或 K/S/M；
- `FAMILY_EMERGENT_WITHIN_THESIS`：由 experiment families 暴露、符合 frozen black-box external-control
  north star、但不能归入以上方向的新候选问题。

所有 branch 都必须完成 v1 九维 rubric：problem distinctness、decision causality、measurement validity、
modality necessity、failure severity、feasibility、reproduction anchor、scope compatibility 和 evidence
maturity。Emergent branch 还必须说明为什么不是旧 bundle 的重命名，以及为什么不是无界扩张。

Branch portfolio 保持未排序。D1 知识、D2 技能和 D3 记忆必须分别形成证据卡，不允许因其中一条论文更新
更快就提前淘汰另外两条；是否接纳或选择任何 branch 属于 owner gate。

## 9. K/S/M 与系统/控制方向的一手证据和实验设置

### 9.1 高价值筛选标准

一个跨领域设置只有同时具备以下特征，才进入 protocol analogue shortlist：

1. 能隔离 system、knowledge、skill、memory 或 reward-control 中至少一个一级变量；
2. baseline、intervention 和 ablation 明确；
3. environment 可以 reset，或至少能记录 exact initial/final state；
4. terminal outcome 与中间 milestone 可观察；
5. access 与 frozen black-box contract 兼容，或能作为清楚的 boundary；
6. 可迁移的是 decision structure，而不是仅仅“任务看起来相似”；
7. 对 K/S/M 明确区分 asset content、persistence、retrieval 与 runtime use；
8. 对 multimodal claim 至少能区分 `MM1` 与 `MM2`，优先选择具有 `MM3` 消融的工作；
9. 在本地 speech/omni 数据、工具或 simulator 上存在明确适配路径；
10. 有 strongest falsifier 和停止继续投入的 kill criterion。

### 9.2 协议 analogue 矩阵

| 方向与代表工作 | 原设置的高价值结构 | 当前证据判断 | Stage-1B delta / Stage-1C 用途 | speech/omni 未执行迁移问题 |
|---|---|---|---|---|
| `D0_SYSTEM`：MM-ReAct、MLLM Orchestration、Agent-Omni、GEMS、Omni-Decision | 中心 controller、specialists、tool loop、shared state、memory/skill on-demand loading | 已证明 training-free agent harness 是实际研究线，但多数组合同时改变工具、状态或资产，纯 system effect 常未隔离 | 映射 topology、decision rights、same-core/system-only ablation；GEMS 新进 delta | 在完全相同 core/tool/K/S/M 下，agent loop 相比 single call 是否仍有增益？ |
| `D1_KNOWLEDGE`：RMR、Omni-Decision、AudioGenie-Reasoner、multimodal search agents | 外部 declarative evidence、bimodal retrieval、evidence need/closure、主动补证 | 知识增强与证据状态都重要，但 RAG gain 可能来自答案泄漏、更多 token 或 task-similar exemplars | RMR 新进 delta；分开 latent activation、external knowledge、query-scoped evidence | raw audio/visual evidence、transcript knowledge 和外部文档各自增加多少可实现 headroom？ |
| `D2_SKILL`：Anything2Skill、MMSkills、XSkill、RESOURCE2SKILL、SRA、SkillSmith | knowledge→skill compilation；state cards＋keyframes；experience/skill 双流；multimodal resource distillation；skill retrieval/incorporation | 2026 年形成密集新簇；MMSkills 的 no/text/full ablation 与 XSkill 的 experience/skill ablation价值高，但不能据此预判 speech 有效 | 六个 exact-ID 新候选进 delta；SkillSmith 已在 registry；记录构造数据、test isolation、version 和调用条件 | 能否把音频/视频状态、工具序列、失败与验证 cue 编译成可复用 speech/omni skill？ |
| `D2_FALSIFIER`：SWE-Skills-Bench | pinned repo、deterministic tests、with/without skill 配对 | 49 个技能中 39 个零 pass-rate 增益，平均仅 +1.2%，版本不匹配可降级；技能收益高度依赖 fit | 作为技能线 strongest falsifier，不得只抽正结果 | audio skill 是否因错误 task fit、过时工具或 reference anchoring 增加错误与 token？ |
| `D3_MEMORY`：MemLens、MMA、M2A、AOP-Agent、Visual Agentic Memory、MAGIC-Video、GEMS | long-context vs memory-agent；image ablation；可靠性/冲突/衰减；raw＋semantic 双层；层次化跨模态证据 | 记忆线已有清晰失败面：长上下文随长度退化，memory agent 压缩后损失视觉保真；更新、refusal、冲突仍未解决 | M2A 新进 delta；其余多数已在 registry/current；必须区分 memory mechanism 与 stored K/S content | raw history、文本摘要、保留原始音频片段的 memory，谁能支持跨轮更新、冲突和恢复？ |
| `D4_TF_RL`：LATS、Training-Free GRPO、reward-guided SMC | value/reward-guided search、经验 prior、reward-tilted sampling | 提供明确训练免除路径，但部分方法只控制 token decoding 或使用语义 advantage，未必满足外部 agent action 合同 | 作为 direct/control boundary 编码 reward 的对象、时间尺度和 next-action effect | reward 是否能选择 K/S/M asset、决定 retrieve/compose/update/stop，而非只重排最终答案？ |
| `INSTRUMENT`：MemLens、AgentBoard、ToolSandbox、TRACE/S2S-Arena/MTalk | modality ablation、过程 progress、stateful milestone/minefield、speech-native judge | 提供可观察 outcome 与反证工具，不自动构成控制能力 | 作为 instrument family；只有 signal 进入下一动作才支持 D4 | 构造 K/S/M 的 task success、过程、staleness、conflict、harm 和 selection-utility 指标 |

### 9.3 建议创造的实验设置

下列设置是 `PROPOSED_BY_PROTOCOL_ANALOGY`，不是论文已有实验，也不是 novelty claim。

#### E1. System harness isolation

在相同 frozen core、prompt、工具、K/S/M 资产、可见信息和预算阶段下比较：

`single call → fixed workflow → planner/actor loop → multi-agent/specialist orchestration`

任何额外 retrieval、skill package、persistent memory 或 evaluator-gated action 都作为独立因子，不能偷偷
进入“system arm”。第一阶段按项目资源姿态摸高并记录预算，第二阶段才做 matched-budget comparison。
若 system gain 在控制工具和资产后消失，则“搭建系统提升任务表现”的因果假设被否证。

#### E2. Multimodal knowledge augmentation

在同一任务比较：

1. frozen-core internal knowledge only；
2. text-only external knowledge；
3. multimodal external knowledge/evidence；
4. oracle evidence；
5. multimodal evidence＋active evidence acquisition。

知识资产必须记录来源、粒度、retrieval result、是否含 task-near exemplar，以及非文本证据是否改变答案或
下一动作。RMR 提供 raw retrieval vs reasoning scaffold 的参考；Omni-Decision/AudioGenie-Reasoner 提供
evidence need、补证和 closure 的 speech/omni 近邻。kill criterion 是 text-only knowledge 或等 token 的
无关 context 已解释全部增益，或 multimodal evidence 存在 text shortcut。

#### E3. Multimodal skill package factorial

构造相同 procedure 的逐级条件：

1. no skill；
2. text-only procedure；
3. procedure＋when/when-not/preconditions/verification state cards；
4. 完整 multimodal skill：再加入 raw audio/image/video reference、关键片段和 before/after evidence；
5. 完整 skill＋runtime applicability/branch loading。

所有 skills 必须来自 evaluation 之外的公开资源或训练任务；报告 source provenance、版本、task overlap、
retrieval precision、load decision、trajectory length 和 harm。SWE-Skills-Bench 是 strongest falsifier：若
大多数技能无增益、错误版本降级，或 text-only 已解释全部收益，则不得推进“多模态技能优越”假设。

#### E4. Multimodal memory carrier and update

在同一多轮/长时任务比较：

1. current turn only；
2. raw long context/history；
3. text-compressed episodic/semantic memory；
4. evidence-preserving multimodal memory，可回指原始音频、图像或视频片段；
5. multimodal memory＋conflict/decay/update/abstention policy。

按长度、session 数、证据模态、update、contradiction 和 refusal 分层。必须同时量化 retrieval、跨证据
reasoning、知识更新、错误记忆污染和 non-text fidelity。MemLens 的 image ablation、MMA 的冲突可靠性和
M2A 的 raw＋semantic 双层是主要协议参考。若 long context 在目标长度上稳定支配 memory agent，或压缩后
无法恢复承重非文本证据，则该 memory design 被 kill。

#### E5. Knowledge→skill and experience→skill compilation

保持 source corpus 不变，比较：

`raw RAG knowledge → raw successful trajectories/episodic memory → distilled text skill → distilled multimodal skill → RAG＋skill`

该设置联合检验 Anything2Skill 的 declarative→procedural 编译与 XSkill 的 experience/skill 双流。必须用
held-out tasks 检验复用，而不是在同任务压缩答案；同时测试失败轨迹是否帮助形成 contraindication 和
repair skill。若 skill 只是压缩 source answer、无法迁移，或 source retrieval 已达到同等表现，则编译路线
不成立。

#### E6. Training-free reward-guided K/S/M orchestration

给定完全相同的 knowledge、skill 和 memory candidate pools，比较：

1. fixed/top-k/similarity policy；
2. LLM planner/self-consistency；
3. verifier/evaluator gated policy；
4. reward/value/advantage-guided sequential policy；
5. oracle asset/action selector。

reward 必须改变 retrieve、load、compose、update、stop、repair 中至少一项下一动作；只对最终输出打分不算
该 arm。报告 realized headroom、regret、harm、calls 和 evaluator noise sensitivity。若静态规则在目标
surface 上支配 reward policy，或 reward 只改善离线 agreement 而不改善 task outcome，则 D4 被 kill。

#### E7. K/S/M compatibility and stale-asset stress test

对知识、技能和记忆分别注入 correct、irrelevant、stale、conflicting、version-mismatched 资产，并组合
system-only、heuristic 与 reward-guided controller。测错误资产是否被拒绝、更新、降权或触发 clarification。
该实验把 SWE-Skills-Bench 的 version mismatch、MMA 的 conflict/decay 和 ToolSandbox 的 minefield 统一成
外部能力资产安全面；禁止只在 clean retrieval 条件下宣称提升。

#### E8. Speech/omni modality necessity

对 D1、D2、D3 分别做 transcript-only、structured acoustic cue、raw audio reference 和 raw audio＋visual
context 消融。目标不是证明 speech 普遍特殊，而是判断某个知识、技能或记忆资产是否必须保留 acoustic、
prosodic、speaker、temporal 或 audiovisual cue 才能改变正确决策。H5 closure 前只报告 task-local 因果结果。

### 9.4 设置进入本地协议的优先顺序

1. `STAGE1B_DELTA_FIRST`：先锁定本轮八个新 exact-ID papers 及一跳引用邻域，补齐 K/S/M/system/TF-RL
   路径、反证、full-text 和 asset evidence；
2. `REPRODUCE_FIRST`：对每条方向优先选择 task/access-matched speech/omni nearest prior；
3. `EQUAL_PRIORITY_KSM`：E2、E3、E4 分别形成知识、技能、记忆独立 family，不预先排序；
4. `INTEGRATION_AFTER_ATTRIBUTION`：只有 K/S/M 单因素证据成立后，才推进 E5、E6、E7 的组合与控制；
5. `CONDITIONAL_MODALITY`：E8 依赖无 text shortcut 的 modality-valid slice；
6. `REFERENCE_ONLY_FOR_NOW`：完整 OSWorld/WebArena 环境 reproduction，除非本地 environment、许可和执行
   成本明确闭合。

这个顺序保证先修复 Stage-1B 输入面，再平等评价知识、技能、记忆，最后才研究 training-free RL 如何
统合它们；不会因某条线更新更快就直接宣布研究方向。

## 10. 本地可落地的未执行协议候选

以下只是 proposal-level protocol groups，不是预注册 branch 或已执行实验。

### LP-0：Multimodal agent system harness

- primary direction：`D0_SYSTEM_HARNESS`；
- 本地资产：W1 frozen-model baseline、现有 tool/evaluator/data adapters；
- arms：single call、fixed workflow、planner/actor loop、specialist orchestration；四者保持 K/S/M pool 不变；
- outcomes：task success、可恢复 headroom、tool calls、trajectory progress、harm、latency；
- kill：控制 tool access、context 和 K/S/M 后，agent harness 不再改善 task outcome。

### LP-K：Speech/omni 多模态知识与证据

- primary direction：`D1_MULTIMODAL_KNOWLEDGE`；
- 本地资产：MMAR、MMAU-mini、MMSU 等 locked 数据；可用 transcript、raw audio segment、结构化声学 cue、
  文档/工具返回作为分层 knowledge sources；
- arms：internal-only、text knowledge、multimodal evidence、oracle evidence、active evidence acquisition；
- outcomes：evidence recall/precision、answer validity、source grounding、missing-evidence detection、calls；
- kill：text-only 或等 token context 解释全部增益；non-text evidence 不改变决策；retrieval 直接泄漏答案。

### LP-S：Speech/omni 多模态技能

- primary direction：`D2_MULTIMODAL_SKILL`；
- 本地资产：Audio2Tool revision `f1388d...` 的 revision-bound content、现有工具 descriptions，以及从非测试
  task/公开教程提取的候选 procedure；
- skill contract：when/when-not、precondition、audio/visual state cues、tool/action steps、verification、failure、
  contraindication、source/version/provenance；
- arms：no skill、text procedure、state-card skill、raw-audio/visual-reference skill、runtime-gated skill；
- outcomes：skill retrieval/load precision、tool identity/arguments、execution success、steps、version-mismatch harm；
- kill：大多数 skills 零边际收益；错误技能无法被拒绝；text-only 已达到同等表现；存在 evaluation leakage。

### LP-M：Speech/omni 多模态记忆

- primary direction：`D3_MULTIMODAL_MEMORY`；
- 本地资产：IHBench revision-pinned 数据；Full-Duplex-Bench v3、VoiceAgentBench 和可构造的 multi-session
  speech histories；
- arms：current turn、raw history、text summary memory、raw-audio-pointer multimodal memory、
  conflict/update/decay-aware memory；
- outcomes：information retrieval、multi-session/temporal reasoning、knowledge update、refusal、resume point、
  acoustic identity/prosody fidelity、stale-memory harm；
- readiness：IHBench `LOCAL_ADAPTABLE`；其余在 license/evaluator closure 前保持阻塞或 transfer；
- kill：目标长度下 raw long context 稳定支配；memory compression 丢失承重语音证据；错误记忆污染不可控。

### LP-R：Training-free reward-guided K/S/M orchestration

- primary direction：`D4_TF_RL_ORCHESTRATION`；
- 输入：LP-K/LP-S/LP-M 产生的相同候选 asset pools；
- actions：retrieve、load、compose、inspect、update、reject、stop、repair；
- signals：deterministic task reward、校准 verifier 或明确有界的 judge；
- arms：static/top-k、LLM planner、verifier-gated、reward-guided sequential control、oracle；
- outcomes：task utility、asset-selection regret、realized headroom、harm、calls、latency；
- kill：reward 不改变下一动作、静态规则支配、或 evaluator 改善不转化为 task utility。

### LP-I：测量与跨领域协议包

- speech-native instruments：UniSRM、TRACE、S2S-Arena、MTalk-Bench；
- transfer sources：RMR、Anything2Skill、MMSkills、XSkill、RESOURCE2SKILL、MemLens、MMA、M2A、GEMS、
  AgentBoard、ToolSandbox、OSWorld；
- readiness：`TRANSFER_ONLY` 或 instrument-specific readiness；
- 禁止用途：不得把 text/VLM 数值外推为 speech/omni effectiveness；不得把 instrument score 自动写成
  training-free RL reward；不得在 H5 closure 前声称跨模态普遍性。

## 11. Calibration、盲审与裁决

### 11.1 Calibration batch

Stage-1B delta 的八个新 exact-ID seeds 全部双编码，所有进入 delta release 的 direct、negative/falsifier 和
nearest-prior edges 100% 复核。Stage-1C mapping signature 后再做 calibration，不直接 scale-out。建议批次：

- frozen base 的 12 个 `KEEP_CORE` 全量；
- 四项 CURRENT priority intake 全量；
- 至少 10 个 system/K/S/M/TF-RL direct/component works，保证 D0–D4 均有代表；
- 至少 10 个 instrument/negative/transfer works，特别覆盖 skill zero-gain、stale memory、knowledge leakage、
  text shortcut 和 reward-not-used falsifier。

Stage-1C 初始目标约 36 papers；若 D0–D4 某方向没有 empirical representative，追加最少数量的 signed-delta work。
Calibration 的目标是发现 codebook ambiguity 和 coder drift，不形成 family conclusion。

允许一次有界 codebook revision；修订后受影响 calibration rows 全量重编码并重新计算 agreement。

### 11.2 Blind review

- 样本数：每个 frozen surface snapshot 取 `ceil(0.20 × N)`，且不得低于 46；若初步 N=290，至少 58；
- 抽样：固定 seed，按 source layer、paper role、domain、D0–D4 primary direction、K/S/M 和 task 分层，
  算法和最终 ID 清单入 manifest；
- independence：blind reviewer 不得看到 primary coder identity、family provisional conclusion 或 branch intent；
- agreement：关键 categorical fields 采用 Cohen's κ，目标 `κ ≥ 0.80`；locator/config exact agreement
  `≥ 90%`；低于任一阈值则暂停 scale-out；
- 冲突：记录 disagreement type，由第三方 adjudicator 裁决，不能由 primary coder 覆盖；
- 100% second review：CORE_MEMBER、load-bearing dataset edge、paired comparison、family conclusion、
  local readiness、branch card。

## 12. Branch gate

Family 升级为 primary branch 必须同时满足：

1. 所有承重论文来自 v5 或已签署的 Stage-1B capability delta；
2. primary direction 在 D0/D1/D2/D3/D4 中唯一，交叉贡献有 factorial 或标为 unresolved；
3. `LOCAL_READY`，或 closure checklist 全部为真且可在 Stage-2A 前闭合的 `LOCAL_ADAPTABLE`；
4. 清晰、可证伪的 residual；
5. task/access-matched nearest-prior reproduction anchor；
6. 可观察 outcome、ground truth 或已验证 evaluator；
7. strongest falsifier 和预注册 kill criterion；
8. 完整九维 rubric；
9. frozen-core baseline、nearest-prior reproduction、candidate strategy、oracle/upper-bound-or-reason 四类 arms。

`LOCAL_ADAPTABLE` closure checklist 必须显式覆盖：exact asset/revision、license/terms、loader/adapter、
frozen access、evaluator、task slice 和 expected execution environment。任何一项未知都不能进入
`READY_FOR_FUNNEL`。

Candidate strategy 只冻结 inputs、state、signals、decision rights、actions、budget 和 expected causal
path，不冻结“创新算法”。

## 13. 实施阶段与 gate

### Phase 0：Owner proposal gate

- 输入：本方案；
- 请求：`AUTHORIZE_STAGE1B_CAPABILITY_DELTA_MAPPING`；
- 输出：允许开展有界 Stage-1B delta；
- 不产生 delta release 签名、Stage-1C mapping 或 execution authority。

### Phase 1：Stage-1B delta seed lock

- 锁定本方案八个新 exact IDs，核验版本、作者、标题、全文、代码/数据、license 与 hash；
- 对 CURRENT/registry canonical dedup，更新 preliminary lower bound；
- 建立一跳 citation ledger 和 stop rules，不开启无界关键词 discovery。

### Phase 2：Stage-1B delta 路径与邻近性映射

- 逐篇映射 D0 system、D1 knowledge、D2 skill、D3 memory、D4 TF-RL 的 primary/secondary path；
- 记录 `DIRECT / COMPONENT / INSTRUMENT / NEGATIVE / BOUNDARY`、nearest prior、实验设置、限制和 locator；
- 对 K/S/M/system/TF-RL 分层做饱和度和 omission accounting；
- 不做项目 novelty verdict、问题排序或 reproduction selection。

### Gate A：Stage-1B delta 独立复审

- 提交 hash-bound delta package、canonical union、full-text/asset receipts 和 mapping tables；
- 需要正式 `SIGN_STAGE1B_CAPABILITY_DELTA_RELEASE`；
- v5 保持不变，signed delta 作为新的派生 release；
- 签署仍不授权研究模型、metric、reproduction、prototype 或 Stage-1C 批量编码。

### Phase 3：Stage-1C v2 codebook 与独立 mapping gate

- 以 signed v5＋delta 为输入完成 K/S/M 三轴、MM0–MM3、run/paired-comparison、dataset/family schemas；
- 双 coder calibration 和一次有界 codebook 修订；
- 重新 hash-bound package，取得 `SIGN_STAGE1C_V2_EXPERIMENT_MAPPING` 后才 scale-out。

### Phase 4：Paper disposition 与 experiment extraction

- 当前 snapshot 100% disposition；
- 承重论文完成 conclusion-changing experiment extraction；
- citation overlay 可追加，snapshot 及时刷新。

### Phase 5：Dataset graph、families 与 K/S/M 图谱

- 先分层证据，再给 family state；
- 生成 direction×K/S/M×system×control×MM-level×family×dataset×access 视图；
- 不预设 branch 数量。

### Phase 6：Local protocols 与 branch portfolio

- 所有本地可落地 family 产生未执行协议；
- 通过九项 gate 的 branch 标为 `READY_FOR_FUNNEL`，其余 `REFERENCE_ONLY`；
- portfolio 未排序。

### Gate B：Family/branch portfolio 复审与 owner selection

- 独立 `SIGN_STAGE1C_V2_FAMILY_BRANCH_PORTFOLIO`；
- owner 决定是否选择问题；
- Stage-2A reproduction execution 仍需单独授权。

## 14. 交付物

1. immutable Stage-1B v5 pointer 与 capability-delta release package；
2. current evidence surface manifest、canonical union 与 citation-refresh ledger；
3. D0 system / D1 knowledge / D2 skill / D3 memory / D4 TF-RL 路径与 nearest-prior map；
4. paper disposition census；
5. run cells、observations 与 paired comparisons；
6. dataset lineage/relation graph；
7. experiment-family cards；
8. K/S/M×system×control×multimodality-level 图谱与 cross-domain protocol analogue map；
9. local readiness/closure matrix；
10. 未执行 local experiment protocols；
11. 未排序 branch portfolio；
12. blind-review、agreement、adjudication 与 reproducible-generation receipts。

## 15. Acceptance criteria

- Frozen 226 bytes/hash 不变；overlay 不回写 base；
- Stage-1B v5 commit/manifest 不变；新增论文只进入可独立回放的 signed delta release；
- current snapshot canonical IDs 全覆盖、无重复、无无理由退出；
- citation-expanded works 全部带 parent edge、official locator、retrieval/version provenance；
- 每个外部 work 明确标为 reference、borrowed protocol 或 reproduction；`PROPOSED_BY_PROTOCOL_ANALOGY`
  不得伪装成 reproduction；
- 每篇承重论文有唯一 `primary_direction`，K/S/M 内容与 persistence 分开；组合干预无消融时必须 unresolved；
- “multimodal knowledge/skill/memory” 声明必须带 MM0–MM3 证据等级，MM3 必须有 modality necessity 对照；
- training-free RL 必须有 reward/value/advantage→next-action 边，离线 score 或静态 top-k 不得冒充；
- 每个 run cell 配置完整且 source locator 精确；
- 多 metric 不复制 run；任何实质配置变化产生新 run；
- 只有 `EXACT_PAIRED` 产生 clean delta；
- 每条 dataset lineage 都有来源证据；
- CORE_MEMBER 通过完整 family signature；
- family state 可由 evidence rows 确定性重放；
- blind review 数量、seed、分层、agreement 和 adjudication 可重放；
- D1 知识、D2 技能、D3 记忆分别形成证据卡、反证和本地协议，不预先排序；
- 每个 ready branch 通过九项 gate 和四类 arms；
- H5-dependent 证据在 closure 前不支撑 modality-specific/cross-modal 结论；
- 全流程不产生项目研究模型调用、benchmark metric、reproduction 结果、prototype 或 novelty verdict。

## 16. 主要风险与控制

| 风险 | 控制 |
|---|---|
| 引用扩展导致无限调研 | 只接受声明的触发边；family/branch freeze 前按 snapshot 截止；无关工作 `EXCLUDE_WITH_REASON` |
| K/S/M 被误当成互斥内容类别 | asset content、persistence scope、primary intervention 三字段分离；允许多标签但只给一个因果 primary |
| 系统、能力与控制混为一谈 | system harness、K/S/M asset、training-free RL control 三轴编码；factorial/ablation 或 unresolved |
| 多模态任务冒充多模态能力 | MM0–MM3 证据门、text shortcut 检查、same-run modality ablation |
| 因技能论文更新快而过早押注 | D1/D2/D3 并列重点；分别配置支持、falsifier、kill 和本地协议；owner 后置选择 |
| skill package 泄漏测试答案或过时 | non-test source、provenance/version、task-overlap、stale/conflict stress、SWE-Skills-Bench falsifier |
| memory 只是更长 context 或向量库 | raw context、compression、evidence-preserving memory 和 update policy 分离；无跨时干预不编码 memory |
| knowledge gain 只是更多 token/答案泄漏 | 等 token、irrelevant context、text-only、oracle evidence 和 task-near exemplar 审计 |
| Dataset-driven grouping 重新压过问题语义 | dataset 只作 lineage/validation stratum；family signature 以失败和协议为主 |
| 只抽支持结果 | conclusion-changing universe、exclusion ledger、blind review |
| Judge score 被误当成真实 outcome | evaluator identity/calibration/selection utility 分开；deterministic oracle 优先 |
| 工程 readiness 被论文 availability 混淆 | exact asset/revision/license/loader/evaluator closure checklist |
| v1 被 v2 擦除 | legacy bundle links、九维 rubric、routing/H5 inheritance 与 CURRENT provenance |
| 过早收敛技术方案 | Stage-1B 先修复论文面；Stage-1C 只固定因果路径和 arms；算法创新留在 reproduction-first Stage-2A/2B |
| 跨领域模仿被写成“复现”或“新颖性” | 三分关系合同、changed-elements ledger、speech nearest-prior-first |

## 17. 研究依据与新增调研来源

本方案在 2026-07-23 对项目 CURRENT artifacts、本地资产清单和外部 primary sources 做了两轮定向
交叉核验。第二轮围绕 multimodal knowledge、multimodal skill、multimodal memory、agent harness 和
training-free reward-guided control 展开；重点深读了 MMSkills、XSkill、MemLens 的完整实验与 ablation，
并用 SWE-Skills-Bench 作为技能方向的显式反证。检索事实与本项目推断分开记录。

置信度分层：

- `HIGH`：外部论文明确报告的协议结构、项目内 hash-bound CURRENT 状态；
- `MEDIUM`：`290` preliminary lower bound，等待 Stage-1B delta canonical-union checker 与独立 review 冻结；
- `CONDITIONAL`：本地实验 readiness，等待 license、adapter、evaluator 和 task-slice closure；
- 所有由跨领域协议推导的新实验设置均为本方案 inference，已标为 `PROPOSED_BY_PROTOCOL_ANALOGY`。

### 项目内权威依据

- `wiki/Project-Thesis.md`：frozen black-box external reward-guided control-plane north star；
- `wiki/Research-Objective.md`：CURRENT authority、H5 与 no-execution 边界；
- `wiki/survey/current/data/stage1c-common-rubric-comparison-v1.json`：三个 legacy bundles、九维 rubric、
  priority intake 与 routing corrections；
- `wiki/survey/current/tables/stage1b-mapping-release.md`：v5 路径、邻近性、缺口、omission surface 和
  “后续修正只通过 dated superseding release”的边界；
- `wiki/survey/current/stage1b-transition-reference-appendix.md`：59-route current reference surface；
- `docs/checks/stage1b-closeout/2026-07-22-v4/stage1c-asset-acquisition-matrix.json`：本地资产、revision、
  license 与 blockers；
- round-02 advisory review：四项有界缺陷和复审关闭条件。

### 外部 primary sources

- [ReAct, ICLR 2023](https://arxiv.org/abs/2210.03629)：reasoning/action 交替、外部观察与异常处理；
- [Reflexion, NeurIPS 2023](https://papers.neurips.cc/paper_files/paper/2023/hash/1b44b878bb782e6954cd888628510e90-Abstract-Conference.html)：feedback、episodic memory 与下一轮决策；
- [LATS, ICML 2024](https://icml.cc/virtual/2024/poster/33107)：search、value、reflection 与 environment feedback；
- [AgentBench, ICLR 2024](https://proceedings.iclr.cc/paper_files/paper/2024/hash/e9df36b21ff4ee211a8b71ee8b7e9f57-Abstract-Conference.html)：多环境交互 agent evaluation；
- [AgentBoard, NeurIPS 2024](https://papers.nips.cc/paper_files/paper/2024/file/877b40688e330a0e2a3fc24084208dfa-Paper-Datasets_and_Benchmarks_Track.pdf)：process progress 与 multi-faceted analysis；
- [WebArena, ICLR 2024](https://proceedings.iclr.cc/paper_files/paper/2024/hash/4410c0711e9154a7a2d26f9b3816d1ef-Abstract-Conference.html)：可复现真实 web environment 与 functional correctness；
- [VisualWebArena, ACL 2024](https://aclanthology.org/2024.acl-long.50/)：visually grounded task、multimodal observation 与 web action；
- [OSWorld, NeurIPS 2024](https://papers.nips.cc/paper_files/paper/2024/hash/5d413e48f84dc61244b6be550f1cd8f5-Abstract-Datasets_and_Benchmarks_Track.html)：真实 OS state、execution-based evaluation；
- [ToolSandbox, NAACL 2025](https://machinelearning.apple.com/research/toolsandbox-stateful-conversational-llm-benchmark)：state dependency、on-policy conversation、milestone/minefield；
- [τ-bench, ICLR 2025](https://proceedings.iclr.cc/paper_files/paper/2025/hash/1b126cc38b8638e07bef37e7b2bb72bf-Abstract-Conference.html)：tool-agent-user、policy 和 dynamic conversation；
- [MM-ReAct](https://arxiv.org/abs/2303.11381)：中心语言模型与多模态 experts 的 transfer boundary；
- [TRACE, Findings of EACL 2026](https://aclanthology.org/2026.findings-eacl.151/)：speech evaluation 的 content/voice/paralinguistic 分解与 deterministic fusion；
- [S2S-Arena, ACL 2026](https://aclanthology.org/2026.acl-long.1615/)：speech-native pairwise protocol 和 paralinguistic complexity；
- [MTalk-Bench](https://arxiv.org/abs/2508.18240)：scenario→capability mapping、pairwise/rubric 双协议及 judge bias；
- [SimulU](https://arxiv.org/abs/2603.16924)：training-free simultaneous policy，但依赖 cross-attention，作为 model-internal boundary。

#### K/S/M 与系统/控制新增 primary sources

- [Retrieval Meets Reasoning (RMR)](https://arxiv.org/abs/2405.20834)：training-free bimodal retrieval 和
  multimodal reasoning scaffold，作为知识增强路径；
- [Anything2Skill](https://arxiv.org/abs/2606.09316)：把 heterogeneous external knowledge 编译为带 invocation、
  contraindication、action 和 evidence 的 reusable skill contract，直接连接 K→S；
- [MMSkills](https://arxiv.org/abs/2605.13527)：text procedure、state cards、multi-view keyframes 与 branch
  loading；实验包含 no-skill、text-only、组件和加载方式消融；
- [XSkill, ICML 2026](https://arxiv.org/abs/2603.12056)：视觉 grounded experience/skill 双流；去 experience
  和去 skill 都产生独立下降，支持把 episodic experience 与 procedural skill 分开；
- [RESOURCE2SKILL](https://arxiv.org/abs/2606.29538)：从 tutorial video、repository、article 和 artifact
  蒸馏 hierarchical multimodal Skill Wiki，并测试格式、来源、选择和 online acquisition；
- [Skill Retrieval Augmentation](https://arxiv.org/abs/2604.24594)：把 skill retrieval、incorporation 和 end-task
  execution 分开评价，并暴露“检索到 gold skill 也不代表 agent 会正确加载”的瓶颈；
- [SkillSmith](https://arxiv.org/abs/2605.15215)：skill boundary compilation 与 runtime interface，作为
  skill context/overhead 的组件路径；
- [SWE-Skills-Bench](https://arxiv.org/abs/2603.15401)：with/without skill 的确定性配对反证；多数技能零增益，
  version mismatch 可造成负迁移；
- [GEMS](https://arxiv.org/abs/2603.28088)：agent loop、trajectory memory 和 on-demand skills 的多模态生成
  system bundle；需要通过 ablation 判断各成分，不把整包 gain 分摊给单项能力；
- [MemLens](https://arxiv.org/abs/2605.14906)：32K–256K 下比较 long-context LVLM 与 memory agents，覆盖
  extraction、multi-session、temporal、update、refusal，并用 image ablation 验证视觉证据必要性；
- [MMA](https://arxiv.org/abs/2602.16493)：对 multimodal memory 的 source credibility、temporal decay、
  conflict 和 abstention 建模；
- [M2A](https://arxiv.org/abs/2602.07624)：RawMessageStore＋SemanticMemoryStore 的双层、在线更新型个性化
  multimodal memory；
- [AOP-Agent](https://arxiv.org/abs/2605.28192)：hierarchical omni-modal memory 与 observe-reflect-replan，
  是 speech/omni memory/system 的直接近邻；
- [Omni-Decision](https://arxiv.org/abs/2607.11433)：training-free structured evidence state、主动补证、验证、
  repair 和 closure，是知识/系统交叉近邻；
- [Training-Free MLLM Orchestration](https://arxiv.org/abs/2508.10016)：controller、specialists、full-duplex 与
  cross-modal memory integration 的 system path；
- [Training-Free GRPO](https://arxiv.org/abs/2510.08191)：group-relative semantic advantage 蒸馏 experience
  token prior；属于 training-free control/experience boundary，需核查是否满足 strict next-action contract；
- [Reward-guided SMC](https://arxiv.org/abs/2604.16453)：不更新权重、用 prefix reward potential 改变 inference
  distribution；是严格 reward-guided decoding comparator，但不是现成 multimodal agent controller。

## 18. Owner 授权后的第一项动作

若 owner 返回 `AUTHORIZE_STAGE1B_CAPABILITY_DELTA_MAPPING`，第一项动作不是跑实验或启动 Stage-1C 批量编码，
而是：

1. 创建独立 Stage-1B capability-delta workbench/audit campaign，不改写 v5；
2. 锁定八个新 exact IDs，解析一跳引用邻域，生成 full-text/asset/identity receipts 与 exact census；
3. 按 D0 system、D1 knowledge、D2 skill、D3 memory、D4 TF-RL 映射路径、邻近性、反证和实验设置；
4. 生成 hash-bound delta release candidate，提交独立复审。

只有 `SIGN_STAGE1B_CAPABILITY_DELTA_RELEASE` 登记后，才用 v5＋signed delta 修订 Stage-1C v2 输入；只有后续
独立 `SIGN_STAGE1C_V2_EXPERIMENT_MAPPING` 登记后，才进入 calibration mapping。
