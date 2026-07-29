---
artifact_id: "SF-STAGE1C-R2-COREVIEW-V1"
role: "R2 按 07-29 判据的协同重审底稿（模板 v1 首例）"
status: "DRAFT_FOR_OWNER_COREVIEW; owner 未签"
template: "2026-07-29-direction-review-template.md"
evidence_cut: "2026-07-28（复用 R2 报告与 D1 dossier 已登记证据；本轮零新检索）"
execution_authority: "STAGE2A_WITHHELD"
---

# R2 协同重审底稿：音频驱动外部知识获取

## §1 元信息

- ID：R2；主维度 D1 知识（外部知识获取）。前版：`R2-audio-native-knowledge-acquisition.md`
  （执行者草稿，owner 未校验；其证据事实本稿全部继承）。
- 承重全文（全部本地 hash 登记）：AudioRAG 2602.10656、Omni-DeepSearch 2605.08762、
  VoiceAgentRAG 2603.02206；佐证：`2026-07-26-d1-knowledge-dossier-draft.md`。

## §2 两型归类：**(a) 型**，改进杠杆借自跨域

本域已有工作（DFS 四问）：

| 论文 | 方法 | 局限 | 改进空间 | 可借鉴 |
|---|---|---|---|---|
| AudioRAG | text controller（Qwen3-8B）调度 frozen omni audio tool + Google Search，Think-Call-Answer | 无 need gate/成本记账/显式 stop；agentic 臂增加 Invalid Answer（无限循环）；37.0→46.2 不能归因单一因素 | 调度与停止是自由生成、无 reward 约束——**调度质量是公开缺口** | 500 题 benchmark、GPT-4o judge 协议、A/B/C/D 错误分类 |
| Omni-DeepSearch | audio-only 起步多跳深搜 benchmark + 固定搜索预算 pipeline | 只有固定预算 (5,1)/(10,3)/(15,5) 消融；预算饱和（29.06→43.44→44.06%）且有 over-search 反例（多搜反而污染证据）；无逐实例调度器 | **作者自己证明"预算不是越多越好"却没给调度器——这就是台阶** | 640 题官方资产、三判官协议、subgroup/预算消融报告法 |
| VoiceAgentRAG | 跨轮 prefetch/cache 双 agent | 无真实语音输入、无答案质量指标 | （对 R2 能力问题无台阶；latency 工程归 R9） | cache/latency 报告法 |

跨域 donor（改进杠杆来源，效果不外推）：Training-Free GRPO / JitRL / ETS 的
reward→下一动作机制；bandit 预算分配协议（均见 d5/d6 dossier 登记条目）。

**归类论证**：本域存在可作方法论基线的已有工作（两条 pipeline + 三套官方评价），满足 (a) 型；
公开缺口（逐实例检索调度/停止）的解法借自跨域 TFRL donor——正是判据 (a)+donor 的标准形态。

## §3 具体任务与 readiness

**任务**：Omni-DeepSearch-640 官方协议下的 audio-initiated deep search（主载体）；
AudioRAG-500 作次级/稳健性载体。

| 资产 | 本地 | lock | split | 评测依赖 | 缺口 |
|---|---|---|---|---|---|
| Omni-DeepSearch-640 | 有（`LOCAL_CANDIDATE_UNFROZEN`） | 未入 lock | 官方仅 `train` 一个 split | 三 LLM judge（外部 API） | 无冻结检索快照、无 negative class、无 dev/test 划分 |
| AudioRAG-500 | 未落盘 | 未入 lock | 论文未给 split | GPT-4o judge（外部 API） | 无 frozen web corpus、无 tool ablation |
| VoiceAgentRAG-200 | 未落盘 | 未入 lock | scripted | — | 无语音、无答案质量指标 |

**因 readiness 明确不做**：不测 need detection（官方无负类——前版 H1 判死成立，继承）；不自造
检索快照/负例/新标签；live-search 漂移如实作为边界报告。judge-API 依赖与 split 冻结方案属
Stage-2 执行合同问题，此处只登记。

## §4 SOTA 基线锚定

- **Omni-DeepSearch-640**：SOTA = 论文统一 tool-augmented pipeline 最优配置，Gemini-3-Pro
  预算 (15,5) 平均 accuracy 44.06%（三判官多数投票）；(10,3)=43.44%、(5,1)=29.06% 为预算曲线。
  **须复现**：本项目核心（Qwen3-Omni-30B）在官方协议下的 fixed-budget 臂（本地可比锚点）；
  **只引用**：Gemini/MiMo 等他核数字（口径为他核结果，不改写为本项目结果）。
- **AudioRAG-500**：SOTA = Qwen3-Omni + Qwen3-8B controller 46.2%（raw 37.0%；GPT-4o judge
  三次运行平均）。**须复现**：raw 与 pipeline 两臂；错误分类沿用 A/B/C/D。
- 三篇不可公度，分列报告，不新造统一指标（继承前版 §5 结论）。

## §5 改进空间与研究问题

候选杠杆（均过 read-out/new-info 判别——只用部署时可得信号：中间答案一致性、检索结果与
音频实体的 corroboration、预算消耗；不用 test gold、不用隐藏状态）：

1. **主杠杆：reward-guided 检索预算/停止调度**——逐实例决定继续搜/换 query/停，替代全局固定
   预算。依据：论文自证 over-search 伤害 + 预算饱和 → 等预算下重分配预算存在可观测 headroom。
2. 次杠杆：检索证据 admission 门（接纳/拒绝外部证据进 context），依据 AudioRAG 的
   Knowledge/Invalid 错误分类。

**研究问题**：在 Omni-DeepSearch-640（官方协议、等总预算）上，训练无关的 reward-guided
检索调度能否相对最优固定预算基线带来可靠 accuracy 提升并降低 over-search 失败。

## §6 对比骨架与击杀阈值（数值为提案默认，`TBD_AT_AUTHORIZATION`）

臂：direct（无检索）｜官方 fixed-budget 三档复现｜random-matched-cost 调度对照｜
reward-guided 调度。报告：paired delta、下置信界、seed 方差、15 类 subgroup、calls/cost。

- K1：等预算下 reward-guided vs 最优固定档，paired accuracy delta 的 95% 下置信界 ≤ 0
  或点估计 < **+2.0pt**（SESOI 提案值）→ 杀独立方向，回落 MERGE。
- K2：调度臂相对固定档未把 over-search 型错误相对减少 ≥ **30%**（等 accuracy 下）→ 调度杠杆
  判死，仅保留 admission 门作 R5/R8 组件。
- K3：调度收益无法在 AudioRAG-500 上方向一致复现（符号翻转）→ 降级为单 benchmark 现象，
  不得写跨任务结论。

## §7 边界与暴露

API-only；test gold 永不进 controller；数据/指标全复用官方口径。本轮 exposure：仅复读已登记
全文与 dossier/T2 条目；零新检索、零模型/API 调用、零下载、零指标运行。

## §8 处置建议与对抗分析

**执行者建议：`GO_STANDALONE_AS_RETRIEVAL_SCHEDULING`**——R2 以「reward-guided 外部知识
获取调度」为独立方向重立，任务与基线如 §3/§4。

**最强反方（前版报告的管辖论证，必须直面）**：query/hop/stop 属 R6 实例内轨迹控制、预算可靠性
属 R8，R2 无独占决策权——照此应 MERGE。**回应**：该论证依赖已标 owner 未签的「裁决 C」（本
阶段不设计方法）；且按 07-29 判据均匀适用原则，"用到 controller 即越界"会同样杀掉 R5/R6/R8。
真正的裁定点不是方向是否成立（判据四项 R2 全满足），而是**portfolio 归属**：独立方向（选项 A）
还是 R6/R8 的检索实例化（选项 B，即前版 MERGE）。两案的实验内容几乎相同，差别是署名层级与
Stage-2 名额。

**备选**：选项 B = MERGE，把 §5/§6 原样并入 R6（调度）与 R8（预算可靠性），Stage-2D 名额撤销。

**owner 裁定栏**：＿＿＿＿（结论 / 日期 / Decision-Log 条目号）——落笔前本稿全文 owner 未签。
