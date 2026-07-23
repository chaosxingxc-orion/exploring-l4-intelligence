---
title: "Stage-1C v2 能力集与实验族证据研究方案"
artifact_id: "SF-STAGE1C-V2-CAPABILITY-EVIDENCE-PROGRAM-2026-07-23"
date: "2026-07-23"
status: "OWNER_REVIEW_DRAFT"
authority_effect: "NONE"
requested_owner_verdict: "APPROVE_STAGE1C_V2_CAPABILITY_EVIDENCE_PROGRAM"
current_activation_requested: false
experiment_execution_requested: false
novelty_verdict_requested: false
---

# Stage-1C v2 能力集与实验族证据研究方案

## 0. 提请 owner 决策

本方案请求 owner 审阅并决定是否授予：

`APPROVE_STAGE1C_V2_CAPABILITY_EVIDENCE_PROGRAM`

该授权只确认 Stage-1C v2 的研究问题、证据面、能力本体、实验抽取合同、动态刷新机制、复核方案和
未执行实验设计，可以据此完成 schema/codebook 修复并提交独立复审。它不直接产生
`SIGN_STAGE1C_V2_EXPERIMENT_MAPPING`，也不授权模型/API 调用、benchmark metric、论文 reproduction、
prototype、问题排名、owner selection、技术 novelty verdict 或 Stage-2A。

在独立 `SIGN_STAGE1C_V2_EXPERIMENT_MAPPING` 登记前，允许的工作仍限于 proposal、schema、codebook、
surface inventory、引用链调研、metadata/full-text locator 整理、calibration packet 设计和机器检查；
不得启动大规模 experiment-level coding、family conclusion 或 branch formation。

## 1. 研究动机

Stage-1C v1 以三个未排序问题包组织证据：budget/stop/repair、evaluator/reward reliability 和
interactive/full-duplex objectives。它成功建立了共同九维 rubric，但一级结构仍然先规定“问题包”，
再把论文放入问题包，容易产生三类偏差：

1. 同一个实验同时验证多种控制能力时，论文主题或数据集名称会掩盖真正的决策结构；
2. 不同数据集可能研究同一能力，也可能在同一数据集上研究完全不同的失败机制；
3. 新增引用证据容易被迫塞入旧问题包，或者在没有统一实验单位时形成平行摘要。

Stage-1C v2 因此改为：

`动态证据面 → 原子运行单元 → 配对比较 → 数据集图 → 实验族 → 能力集 → 研究分支`

三个 v1 bundles 和九维 rubric 不被删除，而是成为 legacy traceability view。它们负责证明 v2 没有
遗失已经生效的判断，但不限制 experiment families 在项目 north star 内暴露新的候选 branch。

## 2. 核心研究问题

本阶段回答五个问题：

1. 当前证据中的实验实际测试了外部控制平面的哪些可观察能力？
2. 哪些实验在问题、结果语义、环境、access 和 baseline→intervention 因果比较上属于同一 family？
3. 哪些结论只在一个 dataset lineage/access stratum 内成立，哪些得到独立数据或 distribution shift 验证？
4. 哪些文本 agent 或 VLM agent 协议可以提供同构实验设计，但不能贡献 speech/omni 数值结论？
5. 哪些 family 具有本地资产、可观察 outcome、nearest prior、falsifier 和 kill criterion，足以形成
   reproduction-first Stage-2A 候选 branch？

Stage-1C v2 不回答“哪个新算法最创新”或“哪个 branch 已经获胜”。

## 3. 证据面：冻结基础层、CURRENT overlay 与动态引用扩展

### 3.1 三层证据账本

证据面严格分层：

| 层 | 含义 | 变更规则 | 允许用途 |
|---|---|---|---|
| `FROZEN_BASE_226` | Stage-1B v5 固定 registry 的 226 个 canonical records | 只读，不回写 | frozen denominator、portfolio role、基础 paper audit |
| `CURRENT_INHERITED_OVERLAY` | CURRENT v1 中 registry 外、但对现行比较承重或构成明确边界的 canonical works | 由 CURRENT manifest 和 canonical union 生成 | 继承 priority intake、59-route appendix、routing correction、H5 status |
| `CITATION_REFRESH_OVERLAY` | 分析中沿引用、修订版、数据集论文或 nearest-prior 链新增的有界工作 | append-only snapshot；必须去重、说明触发来源 | family 补证、反证、instrument、transfer analogue |

不得把 overlay 写回 `FROZEN_BASE_226`，也不得用 overlay 改写 Stage-1B v5 的历史计数。

### 3.2 当前分母的初步核验

本轮本地核验发现：

- frozen registry：226；
- CURRENT 59-route reference appendix：59 个 canonical routes，其中 7 个与 base 226 重叠，52 个在 base 外；
- TRACE、S2S-Arena、MTalk-Bench、SimulU 四项 priority intake 不在上述 union；
- 因此当前已知最小 canonical union 是 `226 + 52 + 4 = 282`，而不是 `230`。

`282` 仍是 proposal 阶段的初步 census，不是新的冻结事实。实施时必须由 checker 从 manifest、registry、
reference appendix、priority intake 和 canonical alias table 重算；只有无重复、无 unresolved identity 的
`SURFACE_SNAPSHOT_<n>` 才能成为该轮 paper-disposition denominator。

所有 surface records 都需要一次 paper-level disposition；只有承重 empirical works 才要求进行有界但完整的
experiment extraction。非承重、理论、negative 或 boundary works 可作为 non-cell evidence node。

### 3.3 引用扩展与事实刷新

引用扩展是正常研究行为，但必须有界、可追溯：

1. 允许触发源：已登记 paper 的 backward/forward citation、dataset/benchmark 原始论文、nearest-prior、
   explicit falsifier、instrument dependency、论文修订版；
2. 每个新增 work 记录 `discovery_mode=CITATION_EXPANSION`、`parent_work_ids`、query/edge reason、
   canonical identity、official URL、retrieved-at、版本、全文 locator/hash、初始 role；
3. 先 canonical dedup，再决定 `LOAD_BEARING / RELATION_ONLY / REFERENCE_ONLY / EXCLUDE_WITH_REASON`；
4. 不因引用扩展重新开启无界关键词 discovery；
5. 每次新增、版本漂移、资产状态变化或 family 结论变化后生成新的 immutable surface snapshot；
6. family/branch portfolio 评审前冻结一个 exact snapshot。冻结后出现的新承重证据只能通过新的 delta
   transaction 使结论失效或触发复审，不能原位改写历史证据。

刷新至少发生在 calibration 前、scale-out 前、family conclusion 前和 branch portfolio freeze 前。

## 4. 能力集：按控制循环切分，不按论文主题切分

### 4.1 九个一级能力

| ID | 能力 | 精确定义 | 典型输入→决策→输出 | 与邻近能力的切分 |
|---|---|---|---|---|
| `C1_OBSERVE_ACQUIRE` | 观察与证据获取 | 发现缺失信息并选择下一项可观察证据 | 当前证据/缺口→查、听、检索、转换→新证据 | 只负责“获得什么”；不负责长期保存或最终评分 |
| `C2_STATE_MEMORY` | 状态与外部记忆 | 保存任务状态、证据、冲突、历史动作和用户状态，并支持后续决策 | observations/events→state update→可查询外部状态 | 与 C1 的采集分开；与 C8 的错误修复分开 |
| `C3_CANDIDATE_SUPPLY` | 候选供给 | 产生多个答案、动作、工具、计划或轨迹供后续比较 | state/input→sample/search/decompose→candidate pool | 只产生候选，不决定哪个候选胜出 |
| `C4_CONTROL_EVALUATION` | 控制信号评价 | 生成会驱动下一动作的 reward、verifier、judge、confidence 或规则信号 | candidate/state→signal→可用于控制的评价 | 纯 measurement instrument 不自动具备此能力；必须证明 signal 改变决策 |
| `C5_SELECT_ROUTE` | 选择与路由 | 把状态和信号转换为 candidate/tool/agent/trajectory 选择 | state+signal→policy/selector→next target | 与 C4 的信号产生分开；与 C6 的实际执行分开 |
| `C6_ACT_TOOL_ENV` | 工具与环境行动 | 调用工具、API、检索器或环境动作，并接收外部结果 | selected action→execution→environment transition | 评价工具正确性属于 measurement；选择哪个工具属于 C5 |
| `C7_BUDGET_STOP` | 预算与停止 | 分配调用、时间、候选和交互 horizon，决定 continue/stop/escalate | state+signal+cost→budget decision→继续或终止 | 不把固定 K 误记为自适应停止；repair action 属于 C8 |
| `C8_REPAIR_ROLLBACK` | 修复、回滚与弃权 | 诊断系统自身输出、状态或轨迹失败，并 revise/retry/rollback/abstain | failure evidence→repair decision→revised state/output | 处理内生错误；用户中断等外生事件属于 C9 |
| `C9_INTERACTION_RECOVERY` | 交互连续性与恢复 | 在多轮、打断、barge-in、异步事件和用户状态变化下保持或恢复任务 | interaction event→interrupt/resume/update→连续任务状态 | 不等同于一般 repair；核心是外生事件下的 turn/state continuity |

Family 可以有一个 `primary_capability_id` 和若干 `supporting_capability_ids`，但必须指出真正被 intervention
改变的 decision right。若一个 family 同时声称两个 primary capabilities，却无法用 ablation 或 paired
comparison 分离贡献，则必须 split 或标记 `CAUSAL_ATTRIBUTION_UNRESOLVED`。

### 4.2 横切条件，不作为一级能力

以下字段是每个能力的实验条件，不应被误建成能力：

- modality 与 input representation；
- frozen/black-box access；
- horizon、预算与交互模式；
- reward/evaluator 的来源与可见性；
- safety、policy、license 和 data terms；
- outcome observability、oracle/headroom；
- latency、cost、harm 和 uncertainty。

尤其要区分：

- `CONTROL_EVALUATION`：信号实际进入控制边；
- `INSTRUMENT_SUPPORT`：只测量系统，不决定下一动作。

TRACE、S2S-Arena、MTalk-Bench 可以先作为 instrument evidence；只有在一个 controller 使用其信号改变
selection/stop/repair 时，相关 experiment 才能支持 `C4_CONTROL_EVALUATION` 的控制能力。

### 4.3 跨领域证据的作用

文本和 VLM 工作只提供 protocol analogue，不提供 speech/omni 数值外推：

- ReAct 提供 observation–reasoning–action 交替与异常处理的控制结构；
- Reflexion 提供 feedback→episodic memory→next-trial decision 的修复/记忆结构；
- LATS 提供 candidate search、value signal、environment feedback 和 tree budget 的组合协议；
- AgentBoard 提醒不能只看 terminal success，还要记录过程 progress；
- ToolSandbox 和 τ-bench 提供 stateful tool/user/environment 与 milestone outcome；
- VisualWebArena、OSWorld 和 WebArena 提供 exact environment state、action execution 和 functional
  correctness 的实验设计；
- MM-ReAct 提供中心语言模型路由多模态 experts 的 transfer boundary。

这些工作进入 `TRANSFER_ANALOGUE` 或 `INSTRUMENT_SUPPORT`，除非 target speech experiment 的 problem、
outcome semantics、environment/access 和 paired comparison 全部独立成立。

### 4.4 “参考、借鉴、复现”关系合同

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
- tools/retrieval/evaluator/judge identity 与 revision；
- decoding、sampling、candidate count；
- state/memory 初始化；
- intervention、decision rights 和 action space；
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
| `EXACT_PAIRED` | 除 declared intervention 外，dataset/split/core/input/prompt/decoding/evaluator/budget/seed aggregation 均匹配 | within-comparison delta 和 paper-reported inference |
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

`target failure × primary capability × evaluation object × outcome semantics × environment/interaction ×
access × baseline→intervention causal contract`

Dataset 不作为 family 的唯一主键，而是 lineage/validation stratum。同一 dataset 可以因失败机制、metric、
split、access 或 intervention 不同进入多个 families。

### 6.2 Membership

- `CORE_MEMBER`：完整 signature 兼容，可解释 paired comparison；
- `VALIDATION_MEMBER`：同一失败/能力上的独立数据或 shift；
- `TRANSFER_ANALOGUE`：其他领域中 decision structure 同构；
- `FALSIFIER`：挑战能力假设、信号有效性或策略因果性；
- `INSTRUMENT_SUPPORT`：提供 outcome、evaluator、校准或 measurement contract。

### 6.3 确定性证据合成

证据按三层合成：

1. paired comparison：`REPORTED_SUPPORT / REPORTED_NULL / REPORTED_NEGATIVE /
   OUTCOME_DIVERGENCE / UNRESOLVED`；
2. exact-comparability stratum：在同一 dataset/model/access/input/metric/budget 内解释；
3. cross-stratum synthesis：只做带 uncertainty 的定性归纳。

Family state 规则：

- `INSUFFICIENT_EVIDENCE`：没有成熟 exact-paired core evidence，或 evaluator/outcome 合同未闭合；
- `CONSISTENT_SUPPORT`：所有承重 exact strata 支持预期能力路径，且没有成熟 contradiction；validation
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
- 与目标能力有关的 negative/null result；
- causal mechanism ablation；
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
Family 不因无法路由到旧 bundle 就自动失效。

Branch 来源分为：

- `LEGACY_BUNDLE_REFINEMENT`：细化现有三个问题包；
- `FAMILY_EMERGENT_WITHIN_THESIS`：由 experiment families 暴露、符合 frozen black-box external-control
  north star 的新候选问题。

所有 branch 都必须完成 v1 九维 rubric：problem distinctness、decision causality、measurement validity、
modality necessity、failure severity、feasibility、reproduction anchor、scope compatibility 和 evidence
maturity。Emergent branch 还必须说明为什么不是旧 bundle 的重命名，以及为什么不是无界扩张。

Branch portfolio 保持未排序；是否接纳或选择 emergent branch 属于 owner gate。

## 9. 高价值文本/VLM 智能体实验设置及 speech/omni 迁移判断

### 9.1 高价值筛选标准

一个跨领域设置只有同时具备以下特征，才进入 protocol analogue shortlist：

1. 能隔离至少一个一级能力或 decision right；
2. baseline、intervention 和 ablation 明确；
3. environment 可以 reset，或至少能记录 exact initial/final state；
4. terminal outcome 与中间 milestone 可观察；
5. access 与 frozen black-box contract 兼容，或能作为清楚的 boundary；
6. 可迁移的是 decision structure，而不是仅仅“任务看起来相似”；
7. 在本地 speech/omni 数据、工具或 simulator 上存在明确适配路径；
8. 有 strongest falsifier 和停止继续投入的 kill criterion。

### 9.2 协议 analogue 矩阵

| 来源设置 | 原设置的高价值结构 | 与本项目的关系 | speech/omni 最近状态 | 可提出的未执行 speech/omni 设置 |
|---|---|---|---|---|
| ReAct：HotpotQA/FEVER、ALFWorld、WebShop | reason/action 交替；Act-only、CoT/ReAct 等对照；长程稀疏 reward 环境 | `BORROWED_PROTOCOL_ANALOGUE` | AudioToolAgent、AudioGenie、EChO-Agent 已存在 tool/evidence loops，但能力 ablation 尚未统一 | 同一 frozen core 下比较 single-call、tool-only、reason+tool；保持数据、工具和 evaluator 不变，测试 C1/C2/C6 的增量 |
| Reflexion：sequential decision、coding、reasoning | scalar/free-form feedback、episodic reflection memory、跨 trial repair | `BORROWED_PROTOCOL_ANALOGUE` | 语音 repair 工作存在，但“失败反馈→外部 episodic memory→下一 trial”未形成统一 speech protocol | 在 IHBench/Audio2Tool 上比较无记忆、raw event log、verbal reflection memory；测恢复成功、错误传播和跨 trial 污染 |
| LATS：programming、interactive QA、WebShop、math | candidate tree、LM value、environment feedback、reflection、search horizon | `TASK_MATCHED_METHOD_TRANSFER`，若忠实实现可成为 close reproduction | MUGEN 有 consensus，若干 audio agents 有搜索/修复，但未证明与 LATS tree contract 等价 | 在静态 audio reasoning 上构建 evidence/action tree；先摸高再记录 budget，比较 flat sampling、consensus、tree search 与 oracle upper bound |
| AgentBoard | terminal success + step-level progress；统一 observation/action/state transition；subgoal annotation | `BORROWED_PROTOCOL_ANALOGUE` / `INSTRUMENT_SUPPORT` | 当前 speech benchmarks 多集中于终局或 rubric，过程 progress 不统一 | 给 Audio2Tool/IHBench 标注 deterministic milestones，分开“接近完成但最终失败”和“无有效进展” |
| ToolSandbox | stateful tools、隐式依赖、on-policy user、milestone/minefield、insufficient information | `BORROWED_PROTOCOL_ANALOGUE` | Audio2Tool 有 tool correctness；IHBench 有 interruption；尚缺统一 state-dependency/minefield 设计 | 构造 speech tool precondition、缺信息、危险动作和依赖顺序；评价 milestone、minefield、repair 和 abstention |
| τ-bench | tool-agent-user 动态对话、domain policy、database state、multi-trial reliability | `REFERENCE_CONTEXT` 或 `BORROWED_PROTOCOL_ANALOGUE` | τ-Voice 是更近的 speech analogue，但 exact voice assets 尚未锁定 | 优先解析/复现 τ-Voice；只有其协议不能覆盖 raw-audio/interrupt residual 时，才提出新的 speech policy-interaction 设置 |
| WebArena/OSWorld | 可复现 initial state、长程 actions、execution-based functional correctness、environment reset | `BORROWED_PROTOCOL_ANALOGUE` | voice-agent benchmarks 有 tool tasks，但 OS/web exact-state rollback 不是现成主线 | 设计 voice-driven stateful workflow：保存 environment checkpoint，在错误 tool action 后测试 rollback/continue；本地环境未闭合前只做协议设计 |
| VisualWebArena | text-only 与 visually grounded observation 的差异；真实视觉任务与 action execution | `BORROWED_PROTOCOL_ANALOGUE` | speech 已有 transcript、raw audio、paralinguistic instrument，但缺统一 causal observation ablation | 在同一 speech task 比较 transcript-only、raw-audio、transcript+structured acoustic cues；只作 speech 内 observation 因果分析，不作跨模态结论 |
| MM-ReAct | 中心语言模型通过文本接口路由多模态 experts，zero-shot system composition | `REFERENCE_CONTEXT` / `TASK_MATCHED_METHOD_TRANSFER` | AudioToolAgent、Agent-Omni、Speech-Copilot 等已高度接近 | 先选择最近 speech prior 做 reproduction；若 residual 存在，再比较 static routing、state-gated routing、evaluator-gated routing |
| TRACE/S2S-Arena/MTalk-Bench | dimension decomposition、speech-native pairwise、pointwise rubric、judge bias 与 small-gap uncertainty | `REPRODUCTION_ANCHOR` 或 `INSTRUMENT_SUPPORT` | 已是 speech-native 最近设置 | 优先复现/校准其 evaluator contract；后续仅研究“信号进入 selection/stop 后是否保持 decision utility” |

### 9.3 建议创造的实验设置

下列设置是 `PROPOSED_BY_PROTOCOL_ANALOGY`，不是论文已有实验，也不是 novelty claim。

#### E1. Capability knockout / incremental composition

在同一 dataset、frozen core、prompt family、candidate budget 和 evaluator 下依次加入：

`single call → candidate supply → evaluation → selection → adaptive stop → repair`

第一阶段按项目资源姿态先摸各 arm 的 ceiling、完整记录实际预算；只有找到有效路径后，第二阶段才做
matched-budget comparison。该设置用于判断收益来自哪个能力，而不是笼统比较“agent vs non-agent”。

#### E2. Observation sufficiency and modality-cue ablation

在同一 speech task 比较：

1. transcript-only；
2. raw audio；
3. transcript + deterministic acoustic/paralinguistic cue sheet；
4. raw audio + external evidence acquisition。

要求目标 slice 中 acoustic/prosodic cue 确实可能改变最优 action。结果只支持 speech 内 observation
sufficiency；H5 closure 前不得上升为“speech 相对 text/vision 更特殊”的结论。

#### E3. Evaluator agreement → decision utility bridge

先独立测 evaluator 的 pointwise/pairwise calibration、tie/abstention 和 shift，再把相同 signal 接入
candidate selection、stop 或 repair。比较“离线 agreement 提高”是否真的增加 realized headroom、降低
regret/harm。该设置直接防止把 measurement quality 等同于 control utility。

#### E4. Stateful interruption and recovery factorial

同一 workflow 组合：

- no interruption / controlled interruption；
- no external state / event log / structured state；
- resume / restart / rollback；
- correct / stale / conflicting user update。

评价 terminal success、resume point、state contamination、tool correctness、harm 和 latency。它同时分离
C2、C8、C9，而不是把所有失败归入“full duplex”。

#### E5. Stateful tool dependency and minefield

将 Audio2Tool 或本地 tool simulator 扩展为带 prerequisite、不可逆动作、缺失信息和 policy minefield 的
环境。比较 static router、state-aware router、evaluator-gated router 和 abstention/clarification。该设置
借鉴 ToolSandbox/τ-bench，但任务、语音输入和 action ontology 均重新定义，因此不能称复现。

#### E6. Noisy-evaluator stop/repair surface

在可控 evaluator noise、candidate headroom 和 repair-damage 条件下，比较 fixed K、consensus、confidence
stop、evaluator-gated stop/repair 和 oracle。先画 validity/headroom/harm 随 noise 的 surface，再讨论 cost；
kill criterion 是简单规则在整个目标 noise range 上支配复杂策略。

### 9.4 设置进入本地协议的优先顺序

1. `REPRODUCE_FIRST`：TRACE/S2S-Arena/MTalk evaluator contract、τ-Voice、最近 speech tool/repair prior；
2. `HIGH_VALUE_ADAPTATION`：E1、E3、E4、E5；
3. `CONDITIONAL_ADAPTATION`：E2、E6，分别依赖 modality-valid slice 和 controllable evaluator-noise contract；
4. `REFERENCE_ONLY_FOR_NOW`：完整 OSWorld/WebArena/VisualWebArena environment reproduction，除非本地
   environment、许可和执行成本明确闭合。

这个顺序保证先尊重 speech/omni 最近工作，再使用文本/VLM 的高价值协议填补真正缺失的实验结构。

## 10. 本地可落地的未执行协议候选

以下只是 proposal-level protocol groups，不是预注册 branch 或已执行实验。

### LP-1：静态音频任务上的候选—评价—选择—停止

- 目标能力：C3、C4、C5、C7、C8；
- 本地资产：MMAR、MMAU-mini、MMSU 等 locked 数据，以及 W1 现有 frozen-model baseline artifacts；
- readiness：`LOCAL_ADAPTABLE`，需要统一 run harness、paired comparison 和 evaluator contract；
- arms：single-call frozen baseline、task-matched nearest prior、能力开关型 candidate strategies、
  gold-answer oracle selector；
- outcomes：task validity、oracle headroom、selection regret、repair damage、calls、latency；
- kill：简单固定 K/majority 或 nearest prior 在 validity、harm、cost 上支配所有 candidate strategies。

### LP-2：Audio2Tool 的 speech→tool action 与错误修复

- 目标能力：C1、C2、C5、C6、C8；
- 本地资产：Audio2Tool revision `f1388d...`，71,441 revision-bound content files；
- readiness：`LOCAL_ADAPTABLE`，需要 adapter、exact tier/task contract 和 NC terms review；
- outcomes：tool identity、argument correctness、terminal execution outcome、invalid action、repair rate、cost；
- protocol analogue：ToolSandbox 的 state dependency/milestone，τ-bench 的 tool-agent-user contract；
- kill：单次 frozen baseline 或现有 static router 已达到可用 oracle ceiling，repair 不增加 recoverable mass。

### LP-3：打断后的状态连续性与恢复

- 目标能力：C2、C6、C8、C9；
- 本地资产：IHBench dataset/repo revision-pinned；Full-Duplex-Bench v3 和 VoiceAgentBench 资产本地存在；
- readiness：IHBench `LOCAL_ADAPTABLE`；Full-Duplex-Bench/VoiceAgentBench 在 license 和 evaluator contract
  关闭前为 `BLOCKED_ASSET_OR_TERMS`；
- outcomes：workflow success、state retention、correct resume point、tool correctness、harm、latency；
- kill：failure 几乎完全由 ASR/VAD/front-end 解释，或固定 state replay 已闭合 recovery deficit。

### LP-4：speech-native evaluator 的信号可靠性与选择效用

- 目标能力：C4、C5、C7；
- 本地资产：UniSRM-Bench 1,463/1,463 files、本地 pinned repos；TRACE/S2S-Arena/MTalk-Bench 的全文证据；
- readiness：UniSRM 路线 `LOCAL_ADAPTABLE`；缺少 exact released task assets 的路线保持
  `BLOCKED_ASSET_OR_TERMS` 或 `TRANSFER_ONLY`；
- outcomes：pairwise/pointwise agreement、tie/abstention、calibration、shift、false positive/negative、
  Best-of-N selection utility、harm；
- kill：deterministic oracle 已覆盖目标 decision surface，或 evaluator agreement 改善却不改善 selection。

### LP-5：文本/VLM agent 协议迁移包

- 来源：ReAct、Reflexion、LATS、AgentBoard、WebArena、VisualWebArena、OSWorld、ToolSandbox、τ-bench、
  MM-ReAct；
- readiness：`TRANSFER_ONLY`；
- 产物：observation/action/state/milestone/progress/rollback 的协议模板；
- 禁止用途：不得把文本/VLM 数值作为 speech/omni effectiveness 或 modality-specificity 证据。

## 11. Calibration、盲审与裁决

### 11.1 Calibration batch

在 mapping signature 后先做 calibration，不直接 scale-out。建议批次：

- frozen base 的 12 个 `KEEP_CORE` 全量；
- 四项 CURRENT priority intake 全量；
- 至少 8 个 CURRENT overlay direct/instrument/boundary works，覆盖九项能力；
- 至少 8 个 base instrument/negative/transfer works，按 role/domain/task 分层。

初始目标约 32 papers；若某一级能力没有 empirical representative，追加最少数量的 citation-expanded work。
Calibration 的目标是发现 codebook ambiguity 和 coder drift，不形成 family conclusion。

允许一次有界 codebook revision；修订后受影响 calibration rows 全量重编码并重新计算 agreement。

### 11.2 Blind review

- 样本数：每个 frozen surface snapshot 取 `ceil(0.20 × N)`，且不得低于 46；若初步 N=282，至少 57；
- 抽样：固定 seed，按 source layer、paper role、domain、task/capability 分层，算法和最终 ID 清单入 manifest；
- independence：blind reviewer 不得看到 primary coder identity、family provisional conclusion 或 branch intent；
- agreement：关键 categorical fields 采用 Cohen's κ，目标 `κ ≥ 0.80`；locator/config exact agreement
  `≥ 90%`；低于任一阈值则暂停 scale-out；
- 冲突：记录 disagreement type，由第三方 adjudicator 裁决，不能由 primary coder 覆盖；
- 100% second review：CORE_MEMBER、load-bearing dataset edge、paired comparison、family conclusion、
  local readiness、branch card。

## 12. Branch gate

Family 升级为 primary branch 必须同时满足：

1. `LOCAL_READY`，或 closure checklist 全部为真且可在 Stage-2A 前闭合的 `LOCAL_ADAPTABLE`；
2. 清晰、可证伪的 residual；
3. task/access-matched nearest-prior reproduction anchor；
4. 可观察 outcome、ground truth 或已验证 evaluator；
5. strongest falsifier 和预注册 kill criterion；
6. 完整九维 rubric；
7. frozen-core baseline、nearest-prior reproduction、candidate strategy、oracle/upper-bound-or-reason 四类 arms。

`LOCAL_ADAPTABLE` closure checklist 必须显式覆盖：exact asset/revision、license/terms、loader/adapter、
frozen access、evaluator、task slice 和 expected execution environment。任何一项未知都不能进入
`READY_FOR_FUNNEL`。

Candidate strategy 只冻结 inputs、state、signals、decision rights、actions、budget 和 expected causal
path，不冻结“创新算法”。

## 13. 实施阶段与 gate

### Phase 0：Owner proposal gate

- 输入：本方案；
- 请求：`APPROVE_STAGE1C_V2_CAPABILITY_EVIDENCE_PROGRAM`；
- 输出：研究范围、扩展规则和授权边界确定；
- 不产生 mapping 或 execution authority。

### Phase 1：Surface consolidation 与引用刷新

- 生成 canonical union、alias/dedup、source-layer provenance 和 current census；
- 建立 citation refresh ledger；
- 固定第一个可复核 surface snapshot。

### Phase 2：Codebook、schemas 与 whole-package validator

- schemas：paper、run cell、observation、paired comparison、dataset edge、family、capability profile、
  local protocol、review record、branch；
- 修正 `LOCAL_ADAPTABLE` readiness；
- 机器检查不产生研究结论。

### Gate A：独立 mapping 复审

- 提交重新 hash-bound package；
- 需要正式 `SIGN_STAGE1C_V2_EXPERIMENT_MAPPING`；
- 签署仍不授权研究模型、metric、reproduction 或 prototype。

### Phase 3：Calibration mapping

- 双 coder calibration；
- 一次有界 codebook 修订；
- 达到 agreement 阈值后才 scale-out。

### Phase 4：Paper disposition 与 experiment extraction

- 当前 snapshot 100% disposition；
- 承重论文完成 conclusion-changing experiment extraction；
- citation overlay 可追加，snapshot 及时刷新。

### Phase 5：Dataset graph、families 与能力图谱

- 先分层证据，再给 family state；
- 生成 capability×family×dataset×access 视图；
- 不预设 branch 数量。

### Phase 6：Local protocols 与 branch portfolio

- 所有本地可落地 family 产生未执行协议；
- 通过七项 gate 的 branch 标为 `READY_FOR_FUNNEL`，其余 `REFERENCE_ONLY`；
- portfolio 未排序。

### Gate B：Family/branch portfolio 复审与 owner selection

- 独立 `SIGN_STAGE1C_V2_FAMILY_BRANCH_PORTFOLIO`；
- owner 决定是否选择问题；
- Stage-2A reproduction execution 仍需单独授权。

## 14. 交付物

1. current evidence surface manifest 与 citation-refresh ledger；
2. paper disposition census；
3. run cells、observations 与 paired comparisons；
4. dataset lineage/relation graph；
5. experiment-family cards；
6. 九项能力图谱与 cross-domain protocol analogue map；
7. local readiness/closure matrix；
8. 未执行 local experiment protocols；
9. 未排序 branch portfolio；
10. blind-review、agreement、adjudication 与 reproducible-generation receipts。

## 15. Acceptance criteria

- Frozen 226 bytes/hash 不变；overlay 不回写 base；
- current snapshot canonical IDs 全覆盖、无重复、无无理由退出；
- citation-expanded works 全部带 parent edge、official locator、retrieval/version provenance；
- 每个外部 work 明确标为 reference、borrowed protocol 或 reproduction；`PROPOSED_BY_PROTOCOL_ANALOGY`
  不得伪装成 reproduction；
- 每个 run cell 配置完整且 source locator 精确；
- 多 metric 不复制 run；任何实质配置变化产生新 run；
- 只有 `EXACT_PAIRED` 产生 clean delta；
- 每条 dataset lineage 都有来源证据；
- CORE_MEMBER 通过完整 family signature；
- family state 可由 evidence rows 确定性重放；
- blind review 数量、seed、分层、agreement 和 adjudication 可重放；
- 每个 ready branch 通过七项 gate 和四类 arms；
- H5-dependent 证据在 closure 前不支撑 modality-specific/cross-modal 结论；
- 全流程不产生项目研究模型调用、benchmark metric、reproduction 结果、prototype 或 novelty verdict。

## 16. 主要风险与控制

| 风险 | 控制 |
|---|---|
| 引用扩展导致无限调研 | 只接受声明的触发边；family/branch freeze 前按 snapshot 截止；无关工作 `EXCLUDE_WITH_REASON` |
| 能力切分仍有重叠 | primary/supporting capability + explicit decision right + attribution unresolved/split rule |
| Dataset-driven grouping 重新压过问题语义 | dataset 只作 lineage/validation stratum；family signature 以失败和协议为主 |
| 只抽支持结果 | conclusion-changing universe、exclusion ledger、blind review |
| Judge score 被误当成真实 outcome | evaluator identity/calibration/selection utility 分开；deterministic oracle 优先 |
| 工程 readiness 被论文 availability 混淆 | exact asset/revision/license/loader/evaluator closure checklist |
| v1 被 v2 擦除 | legacy bundle links、九维 rubric、routing/H5 inheritance 与 CURRENT provenance |
| 过早收敛技术方案 | Stage-1C 只固定因果路径和 arms；算法创新留在 reproduction-first Stage-2A/2B |
| 跨领域模仿被写成“复现”或“新颖性” | 三分关系合同、changed-elements ledger、speech nearest-prior-first |

## 17. 研究依据与新增调研来源

本方案在 2026-07-23 对项目 CURRENT artifacts、本地资产清单和 15 个外部 primary sources 做了定向
交叉核验。检索子问题包括：agent control-loop capability、过程型 evaluation、stateful tool/user
interaction、VLM environment protocol、speech-native evaluator 与 multi-turn speech measurement。

置信度分层：

- `HIGH`：外部论文明确报告的协议结构、项目内 hash-bound CURRENT 状态；
- `MEDIUM`：`282` preliminary union，等待 canonical-union checker 冻结；
- `CONDITIONAL`：本地实验 readiness，等待 license、adapter、evaluator 和 task-slice closure；
- 所有由跨领域协议推导的新实验设置均为本方案 inference，已标为 `PROPOSED_BY_PROTOCOL_ANALOGY`。

### 项目内权威依据

- `wiki/Project-Thesis.md`：frozen black-box external reward-guided control-plane north star；
- `wiki/Research-Objective.md`：CURRENT authority、H5 与 no-execution 边界；
- `wiki/survey/current/data/stage1c-common-rubric-comparison-v1.json`：三个 legacy bundles、九维 rubric、
  priority intake 与 routing corrections；
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

## 18. Owner 授权后的第一项动作

若 owner 返回 `APPROVE_STAGE1C_V2_CAPABILITY_EVIDENCE_PROGRAM`，第一项动作不是编码论文或跑实验，而是：

1. 生成 `FROZEN_BASE_226 + CURRENT_INHERITED_OVERLAY` 的 canonical union 与 exact census；
2. 把九项能力、run/paired-comparison 模型、动态 citation refresh 和 review rules 写入完整 machine schemas；
3. 重新生成 pre-sign package，提交一次有界独立复审。

只有独立 `SIGN_STAGE1C_V2_EXPERIMENT_MAPPING` 登记后，才进入 calibration mapping。
