# Research Methodology（研究方法论）

（2026-07-15 自 CLAUDE.md 迁出成篇——加载面瘦身「动作 C」；本文为正典，修订走 dated
supersession。CLAUDE.md 只留指针与一行摘要。）

## 研究流程阶段（Stage-1A/1B/1C → 2A/2B → 3;dated supersession 2026-07-18,owner 裁决①;Stage‑2B/3 载体绑定 dated supersession 2026-08-04,续91）

**分界依据 = 活动目的与证据用途**，不是「是否启动过 Python」或「样本是否很少」。每份交付物
注明所处阶段。**当前阶段以 `wiki/Research-Objective.md` 为准**（2026-07-29 时点 = Stage-1C
方向确认整改中，Stage-1A/1B 已收官）；本页只保留阶段语义定义。（历史行：Stage-1A survey-ready
gate——问题与 survey 设计;系统性 discovery/
mapping 查询尚未执行,定向 ID dereference/raw provenance/全文准备/校准试验已执行;Gate S1
签署 + owner 批准后第一条 systematic query 即进入 Stage-1B）。

| 阶段 | 使命 | 允许 | 禁止（下一阶段才允许） |
|---|---|---|---|
| **Stage-1A** | 问题与 survey 设计 | 问题树、纳排标准、检索式、种子/哨兵、编码 schema、known-item 身份/路由与协议覆盖检查、脚本静态与变异测试 | systematic mapping;任何研究模型调用;技术方案创新性结论或差异矩阵 |
| **Stage-1B** | systematic survey/mapping **执行** | 检索、去重、题录筛选、全文编码、引文闭包、饱和分析、证据图谱、known-item carry-forward ledger、方法路径/邻近关系事实映射 | **smoke、任务指标、模型/方法比较、headroom/accuracy/WER、技术创新性裁决——全程不得运行研究模型**（owner 签署 2026-07-18） |
| **Stage-1C** | 证据综合与选题 | 形成 3–5 个候选问题/缺口假设卡并由 owner 选唯一问题；冻结 Stage-2A 复现清单与探索约束（不执行、不冻结创新方案） | 用临时实验为某候选「拉票」；把候选缺口写成已成立的技术创新 |
| **Stage-2A** | prior 复现、方案探索与技术创新收敛 | **先复现最接近且最强的公开 prior**；复现成立后才做自研方向性原型并收敛技术贡献（廉价小样、owner 显式放行、全部尝试与失败登记、directional-only；**即使只跑一个 item、只为 smoke，也算一次实验和一次 exposure**） | 把方向性结果写成确证;跳过 prior 复现直接宣称超过 SOTA |
| **Stage-2B** | candidate qualification（方案验证收敛为合格 paper candidate） | 冻结假设、对照、判据；有界验证与统计设计（Research-Proposal-Template 实例、预注册准备、power 估计、paired-bootstrap CI 方案、对抗评审）；冻结 candidate bundle 并申请 paper GO | production-scale confirmatory 与最终优越性结论（属 Stage‑3 paper 仓）；事后换主指标、选择性报告 |
| **Stage-3** | 发表级证据（独立 paper 仓,续91） | 经 `OWNER_GO_AND_PAPER_EXECUTION_CONTRACT` 在 `papers/<slug>` 独立仓执行大规模预注册 confirmatory 与正式统计推断、扩展、独立复现、论文级审计、敌意评审至收敛、论文写作与发表；正/零/负结果同等合法 | 在 study 仓内执行 paper-scale campaign;用 Stage-2A/2B 小样或 probe 代替发表证据 |

**创新性时点（owner 裁决②，2026-07-21）**：Stage-1A 只保证问题、身份、路由、协议与执行门
正确，不比较“我们的技术方案与 prior 有何创新差异”；Stage-1B 如实映射方法路径、覆盖与邻近性，
不作创新性胜负裁决；Stage-1C 基于完整证据形成候选问题/缺口假设并选题，但不把假设冻结成技术
贡献。技术方案的创新性必须从 Stage-2A 的最近 prior 复现与方案探索中收敛，在 Stage-2B 收敛为合格
paper candidate，最终在 Stage‑3 独立 paper 仓的预注册 confirmatory 中验证（续91）。
“发现直接邻近 prior”在 Stage-1A/1B 是路由与覆盖事实，不是杀死方向或迫使提前设计差异化方案。

**exposure 记账（四字段,与阶段声明同报,禁止无范围的「0 次」）**：
`current_activity_stage` / `new_model_touches_since_gate_freeze`（附起算 commit）/
`cumulative_model_touches`（项目累计,非零即写非零）/ `legacy_experiments =
INHERITED_PRIOR_EXPOSURE`（历史实验不删除、不降格、不假装未发生;是后续复现、数据切分与
假设冻结必须排除或分层处理的 exposure union,正典 =
[[2026-07-18-inherited-prior-exposure-union]]）。

**墓碑（供审计,勿再引用为现行语义）**：2026-07-18 前的「Stage-1B = 方向性原型探索」语义与
续40 排序（1A→1B 探针→1C 双证据收官）由本节 dated supersession 取代——方向性原型自此属
**Stage-2A**;07-16 裁决「survey 执行仍是 1A」的**目的**（禁止误称提前进阶段）由新表继承并
加强（连 smoke 都推至 2A）。触发 = v4 博导复审 §1.1 + owner 裁决①（Decision-Log 续65）。

**证据等级纪律**：证据永远保持其产生阶段的等级——Stage-1/2 数字在 Stage‑3 paper 仓的预注册
confirmatory 重建立之前一直是 hypothesis-grade（续91；Stage-2B 产出的是 candidate-grade 设计与
有界验证，不是发表级证据）。记录 append-only——重定级走带日期的 reflection 文档，绝不改写。读
2026-07 之前的记录时套用此透镜（彼时阶段名按墓碑映射）。

## 资源姿态三阶段（owner 2026-07-15）——与「研究流程三阶段」同名异构，勿混

**全力摸高 → 持续整合 → 成本压降**（第三阶段往往对应第三类论文）。

- 前期**预算不限定**——先探「这套方案能把能力天花板顶到多高」，「能到多高」本身就是第一
  阶段的科学产出（预算照实记录、不设 cap）。
- **勿用第③阶段判据（等预算增量、成本归一）评估第①阶段方案的可行性**；等预算类对照一律
  标 `PHASE-3_TOOL` 延后启用。
- Why：过早预算归一会系统性杀死天花板探索——等预算下无增量就砍方向，将永远发现不了「贵但
  能到达的高点」；高点存在，②③阶段的整合与压降才有目标空间。归因严谨在①阶段的正确用法
  是「记录预算、事后归因」，不是「预算约束前置进设计」。

## 理论轨——按 study 在 Stage‑2 重构（2026-08-03 起）

程序级 Lean 形式层已退役（原 `proofs/tfrl/` 仅存 Git 历史）：分析/调研阶段不再建通用公式库，
这是 Stage‑1B 过量设计的复盘结论。形式化义务转移至各获准 study 的 Stage‑2，且**不同研究对象
各建各的证明**：证明对象限定为该 study 自己的承重主张——给出**正确性证明**与**收敛证明**
（静态恒等式不是结果）；工程实现必须与定理是**同一对象**（双轨：代码的算子 ⟷ 定理的算子）；
收敛通常需要**显式约束项**兜住问题边缘（信任域、预算帽、慢漂移前提、奖励误差界），先证
无约束过程不收敛、再证有约束过程收敛。W 时代的理论轨记录仅存 Git 历史与归档。
