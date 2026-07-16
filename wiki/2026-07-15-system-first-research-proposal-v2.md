---
proposal_id: STAGE1A-PROPOSAL-2026-07-15-03
title: "System-first Stage-1A 研究提案 v2（致 reviewer）—— 修订史 · 现行主张 · 下一阶段计划"
date: 2026-07-15
supersedes: "STAGE1A-PROPOSAL-2026-07-15-02（v1）作为送审版——v1 全文保留为记录与细节正典,本件未展开处一律指向 v1 对应节"
stage: "Stage-1A（问题定义,进行中）;按重校准评审裁决,本件申请的唯一事项 = Gate S1 检索协议实例化的送审(§11);不申请 Stage-1A close,不申请 Stage-1B"
review_lineage: "v1 同日两轮外审:严评(RETURN_FOR_MAJOR_REVISION)→重校准评审(ACCEPTABLE_TO_PROCEED_WITH_STAGE1A_SURVEY_PROTOCOLIZATION,撤回其中四项判罚为阶段错位);本件并承担对该评审对的合并回应(§0.3 处置表)"
identity_authority: "Gate S0 已签署(续48):黑盒 omni agentic system / training-free reward-guided external control / TF-Strict(全系统零训练) / selector 降组件 / 资源姿态=全力摸高→整合→压降"
evidence_discipline: "零新执行;既有数字 directional-only/hypothesis-grade;占据状态按登记 token(AS_CITED_BY_REVIEW / RETAINED_RECORDS@census-v2 / ROUND2_PREREGISTERED_TARGET / TRAINED_COMPARATOR,登记于 wiki/survey/README.md);无确证宣称、无「首个」宣称"
generated_by: "Claude Fable 5 主会话协调者亲笔(签署级工件不委托)"
hostile_review: "R1 双镜头（①事实/指针/评审转述准确性;②术语纪律+自库覆盖率+机制叙述残留——后两镜头系 v1 环教训新增,各 Opus 独立）：合并 2 独立 MAJOR（AWM/ExpeL 被误表述『评审净新/不在我方库』——census v2 口径为真但广义自库有 2026-07-04 踪迹,双镜头交叉证实,『查自库』失败模式同批次复发;种子集漏自库 4 条 DIRECT 占据者:training-free-grpo/inference-time-reward-hacking/walking-through-uncertainty/scaling-auditory）+ 6 MINOR（P0-LIT-3 ⑥漏 equation/Checkpoint E 归属/『九行』实为八行/『四镜头』措辞/流程 token 未登记/字面『首个』版本序用法）。逐项修复后 R2 独立复检 8/8 FIXED + 零新发现（四新种子 ID 独立 grep 核验）→ CONVERGED（环内判定,非外部评审通过）。原始报告归档 docs/checks/2026-07-15-proposal-v2-hostile-review-lenses.md"
owner_transmission: "TRANSMITTED 2026-07-15 — owner 指令『收敛后就转交 reviewer 吧,开始 Gate S1 协议实例化』;Gate S1 协议实例化同步开工（零查询,协议成稿后送 reviewer 签署）"
---

# System-first Stage-1A 研究提案 v2（致 reviewer）

> **给 reviewer 的一句话**：这是 v1 经你两轮评审后的修订送审版。§0 告诉你我们改了什么、对你
> 两份评审各接受/保留了什么；§1–§10 是现行主张（未变处指向 v1）；§11 是我们此刻唯一申请的
> 事项：Gate S1 检索协议实例化方案，按你重校准评审的授权口径（协议化已授权、首条查询执行
> 仍待你签）。

## §0 修订史与评审处置（本件相对 v1 的全部变更）

### 0.1 身份层变更（v1 成稿后新发生）

- **Gate S0 已签署**（续48，via 会话指令、授权原文逐字存档、亲笔补签位保留）：身份三行 +
  **TF-Strict（全系统零训练）** 勾定。v1 交付时为 SIGNED 当日状态,本件为签署后第一份送审版。
- owner 追加裁决（已入正典）：**身份层不立法指标**——具体指标绑定任务×数据集,在各研究协议中
  定义、Stage-2 预注册冻结;采纳你重校准 §3.1 的建议句:**预算与停止机制的具体形式由
  system-first survey 与后续原型决定,当前不冻结**。

### 0.2 §4 最近邻表的勘误性修订（严评仍成立项,已修）

1. **四行机制 delta 改写**（严评 §2.2 更正全部接受）：Reflexion（原文明确不更新权重、可黑盒
   实现）、LATS（gradient-free MCTS+LM value,与外部 reward-guided controller 高度相邻）、
   Voyager（GPT-4 黑盒+零微调+技能库,直接占据 black-box+无权重更新+持久外部技能）、
   LLM-as-Verifier（「不占系统身份」判断过早）——四行全部重写并标 `TO_VERIFY_FULLTEXT`;
   「对方未使用我方术语」不再被当作机制差。
2. **自库强近邻检回**（严评 P0-LIT-1 事实成立,grep 实证）：JitRL(2601.18510)/
   Audio-Mind(2605.28480)/Agent-Omni(2511.02834)/EChO-Agent(2606.15141)/AuTAgent(2602.13685)
   五条**均在我方 census v2**而 v1 首版未检回——已补入 §4（token=RETAINED_RECORDS@census-v2）。
   此失误已定性为探索知识层「检索失效」并立新规：**写任何最近邻/占据表前必须先查自库**。
   （你另点名的 AWM/ExpeL：不在 census v2 正典〔grep 0 命中〕,但**广义自库有历史踪迹**——
   2026-07-04 3w-crossdomain survey 与归档 A3 lane 曾与 JitRL 同句点名——按同一「检索失效」类
   如实归类,**不作「评审净新」表述**;题录 AS_CITED_BY_REVIEW 待解析,census late-entry 随协议
   执行补录。此处措辞同时更正续50 的无限定「2/7 不在库」。）
3. 内部复检「CONVERGED」加**环内判定**限定语（重校准 §6 建议采纳）;内审 R1 三镜头 + R2 复检
   （四个 Opus 代理）的原始报告归档
   `docs/checks/2026-07-15-proposal-v1-hostile-review-lenses.md`（严评缺陷 6 处置）,并登记环
   设计教训:新增「机制叙述 vs 原文」「自库覆盖率」两个镜头（本件送审前已用）。

### 0.3 对两份评审的逐项处置表

| 评审意见 | 处置 | 说明 |
|---|---|---|
| 重校准:撤回预算 cap 前置/RL 二选一前置/轨迹 headroom 冻结/QRP 红旗/完整工程平台 | **接受** | 与 owner 三阶段裁决及我方 Research-Methodology 同构;相应问题全部转为 survey 抽取轴与未来决策点(§11) |
| 重校准:五合同标 PROVISIONAL_STAGE1A_TAXONOMY | **接受** | §2 已加横幅;taxonomy 允许被 survey 证据修订,修订走版本化增补不走静默漂移 |
| 重校准:kill 表改标 candidate_kill_logic_for_stage1b_design | **接受** | §6 已改标 |
| 重校准:Gate S1 = 协议化授权/查询执行待签 | **接受** | 本件 §11 即协议化方案送审 |
| 重校准:Checkpoint A–E | **接受** | A–D 并入 §11 协议质量判据;E（工程服务探索、不主导探索）落于 §8 |
| 重校准:PRE_STAGE2_BLUEPRINT 改名 STAGE1B_EXPLORATION_MENU_DRAFT | **保留意见** | 该词为已登记术语(收词纪律);逐文档改名=术语漂移。§10 标题加括注说明语义,不改注册名 |
| 重校准:诚信裁定「本提案阶段不建立 QRP」 | **接受+边界声明** | 不冲销前期评审周期已确立的 MATERIAL QRP 更正义务——更正照常履行(续50 已明示) |
| 严评:§2.2 四行 delta 更正 | **接受,已修**（§0.2-1） | |
| 严评:P0-LIT-1 自库遗漏 | **事实接受,已修**（§0.2-2）;其 QRP 定性从重校准撤回口径 | |
| 严评:P0-LIT-3 检索协议八项最低规格 | **接受为 Gate S1 质量标准** | §11 全文采用 |
| 严评:预算 cap/RL 判据/轨迹 headroom/工程平台前置 | **按重校准撤回口径处置** | 内容转 survey 问题,不作当前 gate |

### 0.4 治理与记录系统变更（与 reviewer 相关部分）

同日完成记录系统整改（业内调研 25 claims 三票核验支撑）：知识四层规约生效（事实/工作/探索/
程序）;**L3 从严登记**——凡 FETCH/精读论文即按 census/ledger schema 登记,不登记不算读过
（未来 survey 全程适用,回应你对跨会话知识丢失的关切）;审计字段绝不预写（先 PENDING、实测
后更新）;评审委托前置 stage lens（本轮两次阶段错位的流程性防再犯）。

## §1 Program identity（已签署,现行主张之根）

见 v1 §1 + S0 签署页。八行合同不复述,核心主张：**研究对象 = 面向冻结黑盒 omni foundation
model 的外部 reward-guided agentic system**（外部控制平面）;**training-free RL = 牵引北极星**
（reward/advantage 决定下一步动作,池内选择是退化特例）;**TF-Strict**;**创新 = owner 选择的
假设**,占据核查完成前不宣称任何「首个」;资源姿态 = 全力摸高（预算照实记录不设 cap,等预算类
判据 = PHASE-3_TOOL）;预算/停止机制的具体形式由 survey 与原型决定,当前不冻结。

## §2 五份系统级合同（PROVISIONAL_STAGE1A_TAXONOMY — to be revised by survey evidence）

见 v1 §2（黑盒/training-free/RL 控制/agentic/omni 五合同,各带 kill 判据与术语降级规则,不设
短代号）。本件明确其**现阶段身份 = 指导检索与文献编码的暂定分类学**,非最终 publication
claim;RL/search 边界、预训练冻结组件归类、native modality 定义等争点全部转为 survey 抽取
问题（§11 字段表）;taxonomy 修订走版本化增补并留痕。

## §3 系统架构（研究对象的纸面表达）

见 v1 §3。控制平面分层 + 状态/动作/反馈/转移/controller 五元组 + 四轴预算记录（不设 cap ≠
将来永不停止,而是当前不以效率约束缩小探索空间——重校准 §3.3 口径）。Stage-1A 仅纸面/schema/
mock,StageGuard fail-closed。

## §4 最近邻种子表（PRELIMINARY,已按 §0.2 勘误修订）

见 v1 §4（修订后全表,含检回的五条自库强近邻与四行改写 delta）。现行主张只有一条：**候选
delta 全部是待证伪假设**;本表身份 = Gate S1 的 seed table,占据结论以可回放 survey 为准。
协议 mandatory seeds（**预协议快照,截止 2026-07-15,允许检索扩展**——本句为 v2 评审 8.1-2
要求的事实性措辞更正,原「全集」表述撤回）= 表内 15 项 + 你补充的机制族（AWM/ExpeL、Self-Refine/CRITIC/TPO、
HuggingGPT/AudioGPT、DSPy/TextGrad、TTRL=OUT_OF_SCOPE_WEIGHT_UPDATED 边界对照）——后者题录
在协议实例化时逐一解析,解析失败者如实标 UNRESOLVED——**+ 本件送审前自库反扫新增的列名种子**
（双镜头内审检出,均在我方 neighbor-matrix/sota-cards v2）：**training-free-grpo (2510.08191)**
（semantic advantage→token prior,与北极星「training-free RL/advantage→下一步动作」最直接的
机制近邻）/ **inference-time-reward-hacking (2506.19248)**（Goodhart 检测选择概念占据者——
§6 停止行与 lane⑦ 的锚）/ **walking-through-uncertainty (2604.25591)**（冻结 Qwen2.5-Omni 在
MMAU/MMAR/MMSU 的 selective-prediction DIRECT 占据）/ **scaling-auditory (2503.23395)**（我方
自评「最紧 omni 机制占据者」,自散文提升为列名种子）。协议实例化含一步**系统性自库反扫**
（neighbor-matrix v2 + sota-cards v2 + ledger v2 + 归档 lanes + `papers/*/references.bib`）
以扩充种子快照;中量候选
（MAV 2502.20379 / SampleScrutinizeScale 2502.01839 / iro 2506.17828 / reward-overopt
2210.10760 / audio-cot 2501.07246 / mugen 2603.09714 等）届时逐一裁决收录。

## §5 基线与归因对照（摸高框架,主张未变）

见 v1 §5。五臂族保留为**候选**基线;主问题 = 天花板高度（预算照实记录）;结构匹配对照服务
reward→下一步动作的因果归因;等预算效率比较 = PHASE-3_TOOL。当前不裁决未来先跑哪臂。

## §6 系统级 candidate_kill_logic_for_stage1b_design（原 kill/pivot/proceed 表,改标）

见 v1 §6（八行表:反馈因果消融/模态移除/奖励移除/外部状态移除/黑盒接口移除/工具必要性/
停止恢复/头空前置）。现阶段身份 = 告诉 survey 要找哪些替代解释 + Stage-1B 探针设计的候选
kill 逻辑;**不是已冻结的实验设计**。

## §7 支撑 dossiers（组件层,效力不变）

见 v1 §7。selector/evaluator 线（census v2 94 记录簇→95 works @28ad858、ledger v2 62 行、
round-2 组件协议零执行）作为组件知识由 system-first survey **继承而非废弃**;测量层四量记账
在终态选择子问题继续可用,不上升为身份。

## §8 工程 qualification（纸面选型,与 survey 并行但不承重）

见 v1 §8。现状如实（Hydra stub+定制脚本,不称配置化基座）;下一步按重校准 §5 口径：一页
runner/config ADR + 开源可复用实现 vs 自研最小骨架的比较 + 配置接口设计;不接真实 backend、
不读数据、不以代码量计进度;真实 adapter 留给另行授权的 Stage-1B。旧 GRPO 训练型配置与
TF-Strict 身份的隔离作为工程 ADR 一并处理。

## §9 零执行声明与 inherited exposure（主张未变）

见 v1 §9。本提案周期新执行 = 零（含 v2 修订）;历史暴露 = INHERITED_PRIOR_EXPOSURE 如实继承;
1B manifest 先扣 exposure union;既有 QRP 更正义务照常履行。

## §10 Stage-1B 蓝图（PRE_STAGE2_BLUEPRINT——即「无现时效力的未来结构草图」,开机须 owner 签批）

见 v1 §10。B0–B5 探针序 + 已签四探针（P-α/β/γ/δ）映射推荐案;探针序对齐仍是 owner 待决项。
本件不申请其中任何一步的执行。

## §11 本件唯一申请事项：Gate S1 检索协议实例化方案（送审）

按你重校准评审的授权（PROTOCOLIZATION_AUTHORIZED / QUERY_EXECUTION_STILL_PENDING），我们将
按以下规格实例化 exact-query protocol，完成后提交你签署、**签署前零查询执行**：

- **范围**：八条 system-first lanes（v1 §11 ①–⑧）+ SURVEY-B 组件子包维持;覆盖判据 = 你的
  Checkpoint A（text-agent/VLM-omni/audio-agent/compound-system 全覆盖;search/reflection/
  memory/tool-routing/verification/non-parametric adaptation 全覆盖;训练自由与训练型最强上界
  两侧都查）。
- **质量规格 = 严评 P0-LIT-3 八项全采**：①发现源 arXiv/ACL Anthology/OpenReview/IEEE Xplore/
  ACM DL（Semantic Scholar/OpenAlex 仅发现,承重回原文）;②每 lane exact Boolean query+同义词+
  时间窗+结果 cap+排序;③mandatory seeds（§4 快照）+ 对其 backward/forward citation chaining
  一轮;④纳排矩阵编码 core access/parameter update/external state/reward type/policy update/
  modality path/tool use/budget-horizon/task/trained comparator;⑤任何 NO_DIRECT_MATCH 须达
  预注册饱和判据（连续两轮 snowballing 零新增直接邻居+双评审独立同意）;⑥承重 delta 须
  version pin+section/page/table/equation locator+必要长度 span;⑦搜索日志/原始响应或可重建结果 ID/
  失败请求/排除理由全量写入 L3 库（构造性可回放——round-1 宇宙缺失教训）;⑧最强 10–15 篇
  threat papers 双人独立全文抽取。
- **抽取字段（开放式,你 Checkpoint B 的建议全采）**：core access / modality path / external
  components / feedback type / what changes at test time / persistence scope / compute
  scaling / claimed mechanism / strongest result / failure mode / reusable implementation;
  预算/调用量只是其中一轴。允许出现新类别并版本化修订 taxonomy。
- **产出约定（你 Checkpoint C/D 的落实）**：不做 intersection-novelty 论证;survey 收官时
  保留 **3–5 个 system-level candidate problems**（你 §4 Checkpoint D 列举的六类为候选池),
  Stage-1C 由 owner 以调研+探针双证据收官选题,survey 前不预定胜者。
- **L3 纪律**：全程即读即登记（census/ledger schema）;判决层带伴随 token。

**时间与签署流**：协议实例化（无查询执行）→ 提交 reviewer 审 → 签署后执行检索 → 综合 →
届时才谈 Stage-1A close（与 1B 放行分立两签）。
