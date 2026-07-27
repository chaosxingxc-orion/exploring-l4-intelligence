# Stage-1C 五维研究方向能力优先整编计划

**状态：完成（2026-07-27）。** 本计划整编 2026-07-26/27 的五维 dossiers、T1/T2/T3 汇聚表和 32 个子方向，
不重做其论文事实层。目标是把 owner 的五条统一约束写成一个 CURRENT 研究合同，并消除 C1/headroom
旧框架与五维组合之间的竞争解释。

## 1. 必须满足的最终合同

1. 核心模型始终是 `API-only` 黑盒：方法不得依赖权重、梯度、隐藏状态、attention、logprobs 或解码器
   内部改写；本地 open-weight 模型也必须通过与 proprietary API 等价的推理接口使用。
2. 研究目标是**可靠兑现能力提升**。可靠性约束端到端任务效用的方差、尾部退化、跨条件稳定性和
   incumbent 回归率；evaluator 可靠性只是其中一个组件。
3. 知识、记忆、技能和编排共同构造 system-level in-context state。静态 fixed-pool headroom 只描述
   已执行供给，不得成为是否研究系统控制的前置门。
4. Lean 用于审计论文假设、算法—命题对应和条件保证；它不证明真实 evaluator 的误差界，也不代替
   capability 实验。每条承重定理必须列出假设、适用算子、不可推出项和代码一致性状态。
5. 主提案必须以任务能力为因变量。安全、防注入、reward hacking、abstain 等内容保留为横切压力测试、
   veto 或 fallback，不独立占据主论文槽位。

## 2. 既有成果的处置

| 既有内容 | 处置 | 原因 |
|---|---|---|
| D0-D6 全文 dossiers、T1/T2/T3 表 | 保留 | 论文事实、资产和实验字段可复用 |
| 五维定义：knowledge / memory / skills / system / evolution | 保留并收紧 | 维度正确；需统一解释为同一 control plane 的状态/动作/动力学 |
| 32 个子方向 | 保留为设计菜单 | 不全部升级为独立课题；映射进 9 条能力主线 |
| P1/P2/P3/P5/P6/P8 | 改名并并入最终方向 | 具备直接能力机制与可执行实验 |
| P9 headroom/E1 gate | 降为横切测量合同 | 不再是“先判断有没有空间”的主问题 |
| P10 reward hacking | 降为所有 reward-guided 实验的压力测试 | 失败模式重要，但不是能力提升主线 |
| P11 stop/abstain/budget | 并入运行时控制与可靠性目标 | stop/rollback 服务于稳定能力提升，不单独写成拒答论文 |
| D4.5 注入/溯源防护 | 保留为 evidence-state invariant | 不作为安全方向或新槽位 |
| D4.7 full-duplex | 降为后期验证载体 | 仅在能隔离任务能力归因时启用，不做 specialized model branch |
| C1 primary selection | 撤销主问题身份，保留组件证据 | evaluator decision utility 是横切仪器，不是整个项目的研究对象 |

## 3. 从 32 个子方向到 9 条定稿主线

| final id | 来源 | 合并原则 |
|---|---|---|
| R1 自适应观察与证据供给 | D1.1/1.2/1.3/1.5 | topology、branching、pricing、effect probe 合为一个闭环 |
| R2 音频原生外部知识获取 | D1.4/1.6 | retrieval 与 anticipatory supply 共享 acquisition/cost contract |
| R3 声学条件键控持久记忆 | D2.1-D2.7 | key、schema、write/read gate、生命周期和归因不可拆开 |
| R4 运行时技能生命周期 | D3.1-D3.6 | skill/tool 的信用、组合、修复、归纳、退役形成一条链 |
| R5 证据状态智能体架构 | D4.1-D4.6 | 决策权、作答权、evidence state、incumbent 保留统一设计 |
| R6 实例内 reward-guided context control | D5.3/5.4 + D1/D3 actions | reward 必须决定下一动作，而不只做终局 rerank |
| R7 跨实例经验驱动进化 | D5.5 + D2/D3 | 不改权重，通过外部记忆、advantage 和策略统计随时间变强 |
| R8 条件自适应的可靠能力控制 | D5.1/5.2/5.6 | headroom/gate/hacking 变成 robust utility 的诊断与约束 |
| R9 五维集成能力激活系统 | D4 + D5 + R1-R8 | 端到端验证组合是否优于同供给、同预算的强控制组 |

## 4. 关键修改

### 4.1 目标函数

把“先测 headroom，再决定是否控制”改为：

```text
maximize robust task utility of the external controller
subject to API-only legality, bounded cost, and a preregistered regression/tail-risk constraint
```

headroom、oracle、evaluator calibration 都作为结果解释量；它们可以击杀某个**已执行 action menu**，
但不能击杀尚未构造的新 context、memory、skill 或 evidence state。

### 4.2 基线与归因

每条方向至少包含：direct readout、structured-prompt、best fixed action、random matched-cost、
consensus/MBR、full fixed chain；gold oracle 仅离线报告。所有比较固定同一 core、任务、输入、最大供给与
计费口径，分别报告生成增益、控制增益、额外信息增益和成本。

### 4.3 可靠性

可靠性最低报告集为：paired task delta、置信区间、重复运行方差、worst-group/CVaR-style tail、
correct→wrong 与 wrong→correct 计数、跨声学条件/语言/任务符号一致性、calls/latency/API cost。
绝对“保证正确”不作承诺；能承诺的是已定义分布和误差假设下的高概率非回归或有界风险。

### 4.4 Lean 审计

现有 `InfoBoundary` 只覆盖 fixed-pool read-out；不得再写成“ICL 不足”。`AgenticElements` 的
all-contexts gap 是强前提，有限采样 oracle miss 不证明该前提。新增 runtime reliability 命题：若部署可用
reward 对真实 utility 的一致误差不超过 `ε`，则 estimated margin `≥ 2ε` 保证相对 incumbent 非回归，
`> 2ε` 保证严格提升。真实世界是否满足误差界仍由实验负责。

每篇参考方法进入 proposal 前填一行：

```text
paper claim | mathematical assumptions | black-box operator | Lean status |
implementation conformance | empirical assumptions | allowed conclusion
```

## 5. Stage-2A 最小纵向验证建议

第一批只验证 `R5 + R6 + R8`：围绕一个 frozen API core 建立 incumbent-preserving evidence-state
controller，用黑盒可得信号决定 `keep / branch-context / acquire-evidence / repair / stop`。推荐
MMAU-mini + MMAR 作为闭集任务载体，先隔离系统控制效应；开放式、RAG、跨实例记忆和 full-duplex
在该纵向链通过后再接入。

运行前必须另行绑定并授权：模型/服务 revision、数据 revision/split/hash、prompt、采样参数、action menu、
reward、预算、SESOI、可靠性阈值、gold fence 和 abort rule。方向定稿不授权模型/API 调用、下载、复现、
prototype、push 或 wiki publication。

## 6. 文件与检查

- [x] 新增 `wiki/survey/current/research-directions.md`，成为唯一有效方向合同。
- [x] 原位更新 `wiki/Research-Objective.md`、`wiki/Project-Thesis.md`、`wiki/Per-Work-Status.md`。
- [x] 更新 CURRENT router/status/manifest；旧 C1 表改为“组件证据，主问题身份已撤销”。
- [x] 更新 workbench README，把 master 标为已整编证据底稿，不再承担完成声明。
- [x] 修正 Lean 过度外推注释，加入 runtime-reliability 条件定理与 smoke test。
- [x] 运行 context surface、CURRENT layer、Stage-1C evidence、manifest replay、Lean targeted
  typecheck/Smoke 和量化措辞扫描。全根 `lake build` 因既有 mathlib/Tilting `.olean` 首次缓存未完成而
  未作为本次 PASS 证据；新增模块和两个 Smoke 例均已由 Lean 4.31.0 直接通过。
- [x] 不改 Stage-1B v5、audit bytes、full-text ledger 既有行或任何项目代码；仅把前序已追加的 ledger
  working bytes 重新绑定进 CURRENT manifest。

## 7. 失效条件

本定稿只在 owner 改变五条统一约束、核心不再 API-only、五维范围被重裁、H5 获得新签署，或 Stage-2A
实验提供足以改变方向排序的证据时 supersede。新论文只更新 nearest-prior/实现选择，不自动杀死方向；
只有其在相同黑盒、供给、预算和可靠性合同下支配对应机制，才触发合并或重路由。
