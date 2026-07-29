---
artifact_id: "SF-STAGE1C-R2-COREVIEW-V1"
role: "R2 按 07-29 判据的开题报告式协同重审底稿（模板 v1 首例）"
status: "DRAFT_FOR_OWNER_COREVIEW; owner 未签"
template: "2026-07-29-direction-coreview-template.md"
evidence_cut: "2026-07-28（复用 R2 报告与 D1 dossier 已登记证据；本轮零新检索）"
execution_authority: "STAGE2A_WITHHELD"
---

# R2 开题报告底稿：音频驱动外部知识获取

## §1 元信息与证据可回溯

- ID：R2；主维度 D1 知识（外部知识获取）。前版：`R2-audio-native-knowledge-acquisition.md`
  （执行者草稿，owner 未校验；其证据事实本稿全部继承）。
- 承重全文（全部本地 hash 登记于 fulltext ledger）：AudioRAG 2602.10656、Omni-DeepSearch
  2605.08762、VoiceAgentRAG 2603.02206；佐证：`2026-07-26-d1-knowledge-dossier-draft.md`。

## §2 待开展研究的内容

**研究问题一句话**：在 audio-initiated deep search 任务（Omni-DeepSearch-640 官方协议）上，
训练无关的 reward-guided 检索调度（逐实例决定继续搜/换 query/停）能否在等总预算下相对最优
固定预算基线带来可靠 accuracy 提升并降低 over-search 失败。

**研究内容分解**：

1. 检索预算的逐实例重分配机制（何时值得多搜、何时停）——参考论文只有全局固定档，逐实例调度
   是公开缺口；归属论证：这是「外部知识获取」自身的调度问题，输入信号与动作都围绕检索。
2. 外部证据 admission（接纳/拒绝检索结果进 context）——依据 AudioRAG 的 Knowledge/Invalid
   错误分类；与 R5 的界线：R5 管 evidence-state 架构合同，R2 管检索证据的取舍策略本身。
3. over-search 失效模式的条件刻画（哪类 audio content/retrieval modality 下多搜有害）——直接
   延伸 Omni-DeepSearch 已发表的 subgroup 消融。
4. 与 R6/R8 的管辖界线：R6 管通用实例内轨迹控制（动作菜单跨方向），R8 管阈值可靠性；R2 若
   立项，研究的是检索这一 action family 的专用调度与证据取舍，产出可被 R6/R8 消费。

**明确不研究**：need detection（官方数据无 negative class，前版 H1 判死成立，继承）；不自造
检索快照/负例/新标签；live-search 漂移如实作为边界报告，不修复。

## §3 研究的方法调研

**本域已有方法（DFS 四问）**：

| 论文 | 方法 | 局限 | 改进空间 | 可借鉴 |
|---|---|---|---|---|
| AudioRAG | text controller（Qwen3-8B）调度 frozen omni audio tool + Google Search，Think-Call-Answer | 无 need gate/成本记账/显式 stop；agentic 臂增加 Invalid Answer（无限循环）；37.0→46.2 不能归因单一因素 | 调度与停止是自由生成、无 reward 约束——调度质量是公开缺口 | 500 题 benchmark、GPT-4o judge 协议、A/B/C/D 错误分类 |
| Omni-DeepSearch | audio-only 起步多跳深搜 benchmark + 固定搜索预算 pipeline | 只有固定预算 (5,1)/(10,3)/(15,5) 消融；预算饱和且有 over-search 反例；无逐实例调度器 | 作者自证「预算不是越多越好」却没给调度器——这就是台阶 | 640 题官方资产、三判官协议、subgroup/预算消融报告法 |
| VoiceAgentRAG | 跨轮 prefetch/cache 双 agent | 无真实语音输入、无答案质量指标 | 对 R2 能力问题无台阶（latency 工程归 R9） | cache/latency 报告法 |

**业内其他工作（文本智能体/视觉多模态参照，只借方法不外推效果）**：Training-Free GRPO、
JitRL、ETS 的 reward→下一动作机制（d5/d6 dossier 登记条目）；文本 agent 检索调度中的 bandit
预算分配协议；WebThinker 取证合同（经 AudioRAG 已进入本域）。借入内容限于：状态/动作表示、
advantage 更新形式、预算分配统计量。

**改进空间 → 候选杠杆**（每个过 read-out/new-info 判别，只用部署时可得信号：中间答案一致性、
检索结果与音频实体 corroboration、预算消耗；不用 test gold、不用隐藏状态）：

1. **主杠杆：reward-guided 检索预算/停止调度**（对应研究内容 1、3）。
2. 次杠杆：检索证据 admission 门（对应研究内容 2）。

## §4 研究的实验基线

**归类：(a) 型——本域有实验基线**，采用其对应数据集与评测方法：

- **主载体 Omni-DeepSearch-640**：官方 640 题资产 + 三 LLM judge 多数投票 accuracy + 15 类
  subgroup + 预算消融报告法。基线锚：论文统一 tool-augmented pipeline，Gemini-3-Pro 预算
  (15,5) 平均 accuracy 44.06%（(10,3)=43.44%、(5,1)=29.06% 为预算曲线）。
- **次载体 AudioRAG-500**：500 题 + GPT-4o judge 三次运行平均 + A/B/C/D 错误分类。基线锚：
  Qwen3-Omni raw 37.0% → +Qwen3-8B controller 46.2%。
- **分层**：须复现（等预算对照臂，用项目核心 Qwen3-Omni-30B 在官方协议下跑 fixed-budget 臂与
  raw/pipeline 臂，形成本地可比锚点）；只引用（Gemini/MiMo 等他核数字，口径为他核结果）。
- 三篇不可公度，分列报告，不新造统一指标（继承前版 §5 结论）。

**readiness 表**：

| 资产 | 本地 | lock | split | 评测依赖 | 缺口 |
|---|---|---|---|---|---|
| Omni-DeepSearch-640 | 有（`LOCAL_CANDIDATE_UNFROZEN`） | 未入 lock | 官方仅 `train` 一个 split | 三 LLM judge（外部 API） | 无冻结检索快照、无 negative class、无 dev/test 划分 |
| AudioRAG-500 | 未落盘 | 未入 lock | 论文未给 split | GPT-4o judge（外部 API） | 无 frozen web corpus、无 tool ablation |
| VoiceAgentRAG-200 | 未落盘 | 未入 lock | scripted | — | 无语音、无答案质量指标（仅作 R9 latency 参考） |

judge-API 依赖与 split 冻结方案属 Stage-2 执行合同问题，此处登记不解决。

## §5 实验设计与数字击杀阈值（数值为提案默认，`TBD_AT_AUTHORIZATION`）

臂：direct（无检索）｜官方 fixed-budget 三档复现｜random-matched-cost 调度对照｜
reward-guided 调度。报告：paired delta、下置信界、seed 方差、15 类 subgroup、calls/cost。

- K1：等预算下 reward-guided vs 最优固定档，paired accuracy delta 的 95% 下置信界 ≤ 0
  或点估计 < **+2.0pt**（SESOI 提案值）→ 杀独立方向，回落 MERGE。
- K2：调度臂相对固定档未把 over-search 型错误相对减少 ≥ **30%**（等 accuracy 下）→ 调度杠杆
  判死，仅保留 admission 门作 R5/R8 组件。
- K3：调度收益无法在 AudioRAG-500 上方向一致复现（符号翻转）→ 降级为单 benchmark 现象，
  不得写跨任务结论。

## §6 边界与暴露声明

API-only；test gold 永不进 controller；数据/指标全复用官方口径。本轮 exposure：仅复读已登记
全文与 dossier/T2 条目；零新检索、零模型/API 调用、零下载、零指标运行。

## §7 处置建议与 owner 裁定

**执行者建议：`GO_STANDALONE_AS_RETRIEVAL_SCHEDULING`**——R2 以「reward-guided 外部知识
获取调度」为方向重立，开题三要素如 §2/§3/§4。

**最强反方（前版报告的管辖论证，必须直面）**：query/hop/stop 属 R6、预算可靠性属 R8，R2 无
独占决策权——照此应 MERGE。**回应**：该论证依赖已标 owner 未签的「裁决 C」；且按 07-29 判据
均匀适用原则，「用到 controller 即越界」会同样杀掉 R5/R6/R8。真正裁定点不是方向是否成立
（判据四项 R2 全满足），而是 **portfolio 归属**：独立方向（选项 A）还是 R6/R8 的检索实例化
（选项 B，即前版 MERGE）。两案实验内容几乎相同，差别是署名层级与 Stage-2 名额。

**备选**：选项 B = MERGE，把 §2/§5 内容原样并入 R6（调度）与 R8（预算可靠性），Stage-2D
名额撤销。

**owner 裁定栏**：＿＿＿＿（结论 / 日期 / Decision-Log 条目号）——落笔前本稿全文 owner 未签。
