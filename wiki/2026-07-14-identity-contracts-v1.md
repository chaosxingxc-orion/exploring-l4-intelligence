---
title: 候选身份合同冻结 v1 + same-selector contract（owner 签核件，触点①）
date: 2026-07-14
stage: Stage-1A
status: FROZEN — owner 签核于 2026-07-14（AskUserQuestion 治理裁决，见 §9）；任何限定词变更走 §8 post-hoc 日志
sequencing: "与 claim-ledger-v1 同批交付（遵 RESP-02 §3.5 顺序：台账先于冻结）——台账 v1 落地（commit a6a2452）、其承重 discrepancies（KIT/IAD 等）已反映后提交签核"
role: "P1 序列 identity-freeze 步骤 + open item 3 same-selector contract 合并交付；1B-0 探针协议与 round-2 检索协议的上游输入"
freeze_discipline: "冻结先于 round-2 检索与 1B 探针（反合取洗白：先冻结定义，再看新邻居）；每份合同带出处日期链"
generated_by: "Claude Fable 5 主会话（基于续34–40 正典状态起草）"
signoff: { owner: "SIGNED — AskUserQuestion 治理裁决（详 §9）", date: "2026-07-14" }
---

# 候选身份合同 v1（六份）+ same-selector contract

> 引用纪律：各身份现状 token 以 RESP-02 §3.3 按身份索引表为准；否定性结论一律
> `NO_DIRECT_MATCH_AMONG_RETAINED_RECORDS`@94簇 + 强制伴随 token。本文冻结的是**定义与判据**。
> **合取量词规则**：strict-I2/I3-combined/UMBRELLA 等合取身份的「占据」须由**单一实例实现完整合取**
> ——分立组件各自被占不构成合取占据，也不得反向拆分以自证开放。

## 1. I1 — 一般 label-free N-best/K-sample selector

- **冻结定义**：不读测试项 gold、仅凭无标签信号从固定 K 池中选一个输出的算子（任意任务、任意信号族）。
- **量词**：存在性身份——只要存在一个直接实现即视为机制占据。
- **正测试**（算占据）：label-free + 固定池内选择 + 与默认输出可比。**负测试**：扩池/改写/工具环/换权重的不算（那是别的算子）。
- **现状**：DIRECT_OCCUPIED（mbr-asr 2510.19471 等；MBR 更正后杀伤更强；证据级封顶 ABSTRACT_VERIFIED 待双审）。**不作独立新颖性。**
- **出处**：重校准审查拟名（2026-07-13）。

## 2. bare-I2 — 音频接地的冻结 omni selector（宽式）

- **冻结定义**：选择信号在决策时**接地于音频**（任何来源：同核或外部）的冻结 omni/audio-LLM 池内选择器。
- **量词拆分（再复审 Round 6，已采纳）**：新颖性按存在性判——**机制级 DIRECT_OCCUPIED**
  （scaling-auditory 2503.23395 同核 audio-conditioned beam log-lik；jia-SER 2602.03873）；
  任务格覆盖单独报告：**MIXED/UNDERSEARCHED**（ST/SLU 格暂无同类，但这不恢复宽式新颖性）。
- **正/负测试**：正=决策信号依赖音频输入（shuffle 音频应改变选择）；负=纯文本流畅度信号。
- **出处**：重校准审查拟名（07-13）。

## 3. strict-I2 — 同核曲面选择器（= I2∩I4 合取）

- **冻结定义**：**同一冻结 omni** 既作生成器、又以**自身**音频接地信号作打分器，且其兑现行为以
  ρ(c) 曲面刻画（供给条件化）。
- **诚实标注（再复审 Round 7，已采纳）**：`POST_HOC_NARROWED_CANDIDATE, post_hoc_created_at=2026-07-14`
  ——构件出处早于猎杀（同核双系统+δ_corr=TH2a 2026-07-05；ρ 面=owner 07-11 签署/续34；own-signal
  生存条件=07-13 I2 拟名当刻），但**合取身份本身系 07-14 合成**；不得以「经攻击幸存」框架引用。
- **正测试**：同一权重双角色 + 打分信号音频接地且**非外部模型**（外部 TTS/GPT-4o/训练 RM 均不算）+ 曲面刻画。
- **kill-if**：shuffle 音频不改变选择（文本流畅度伪装——决策包既有）；δ_corr 测得≈0（同核信号无独立
  价值——决策包 proceed-if 之否定 + 续40 P-γ 生死条件）。
- **pivot-if**（决策包既有）：只有外部 scorer 有效 → strict-I2 坍缩回 I1。
- **现状**：在保留记录中无直接匹配（AMONG_RETAINED_RECORDS）。

## 4. I3 — 受约束/可弃权/Goodhart 检测 selector

- **冻结定义**：在选择之上加显式约束的算子族：弃权选项、Goodhart 拐点检测、风险-覆盖控制。
- **拆分现状**：abstain 分量 DIRECT_OCCUPIED（walking-through-uncertainty 2604.25591）；
  Goodhart-on-speech 无匹配（文本侧被 2506.19248 占）；**I3-combined**（reward-guided+abstain+Goodhart
  同体）在保留记录中无匹配。
- **合取出处**：组合形态即 07-13 拟名的**原始定义**（round-1 ledger 猎杀前已登记该合取为目标格）——
  再复审 Round 7 **暂接受**非临时合取。**差异审计（Round 7 附带条件，就地执行）**：本节定义相对
  07-13 术语表原文的逐词差异 = 仅增「风险-覆盖控制」一语，系决策包 proceed-if 既有判据的上收，
  不新增 novelty 限定词。
- **正测试**：约束在**选择时**生效且可证伪（拐点可检测、risk-coverage 优于 conformal 基线）。
- **kill-if**（决策包既有）：预算内测不到 speech N-best 的 Goodhart 拐点。
- **pivot-if**（决策包既有）：只有弃权分量有效 → 该分量已被占据，I3 失去独立性。

## 5. I4 — 供给条件〔model×task〕兑现面

- **冻结定义**：weight-frozen omni 上，label-free 选择器对 oracle 头空的兑现行为
  **ρ(c)/H(c)/regret 作为供给类型 c 的函数**，跨〔模型×任务〕矩阵刻画（曲面对象本身）。
- **proceed-if**：曲面可升级为**可预测规律**，且通过下述强制检查点。
- **kill-if**（决策包既有）：ρ(c) 实测为噪声，或矩阵级无头空（H(c)≈0 across cells）。
- **现状（再复审 Round 8，已采纳）**：`METHOD_FAMILY_OCCUPIED`（scaling-surface 方法学族已被 text/VLA
  占据）；**音频/omni 供给分层实例化 UNDERSEARCHED；增量预测贡献 NOT YET SHOWN**。
- **强制立项检查点（合同级）**：必须给出相对 difficulty/entropy/agreement/length 等通用 baseline 的
  **增量预测力**，且预测量 **label-free**（对抗 2606.02981 的 labeled predictor）——否则降级为
  实例化/工程贡献，不得作科学新颖性。
- **正测试**：供给轴 c 显式分层 + 兑现量分解（非单一 scaling 曲线）。**负测试**：难度/K/粒度/策略轴
  的曲面不算（那是邻域）。
- **出处**：重校准审查 S1-F2「第四个」选项 + 续34 对象锁定。

## 6. UMBRELLA — 伞式交集（第五候选）

- **冻结定义**：training-free RL ∩ 冻结 omni ∩ advantage→下一步动作（agentic 环内的奖励引导轨迹选择）。
- **出处**：2026-06-26 立项对象（提案/06-30 survey/07-03 go-no-go/Project-Thesis）；
  「advantage→next action」锐化措辞首现续36——已预置为 §8 日志首行（签核前既有变更，如实入表）。
  **差异审计（Round 7 附带条件，就地执行）**：本节定义相对 06-26 立项文本的逐词差异 = 仅该锐化一处。
- **现状**：在保留记录中无直接匹配（AMONG_RETAINED_RECORDS）。**正测试**：单一占据实例须同时满足
  frozen core + agent 实际接触音频 + reward/advantage 引导下一步动作。**负例**（决策包既有）：
  AudioToolAgent 2510.02995（占 system 格但 agent 不接触音频、无 reward-guided K-pool selection）、
  AuTAgent（训练）、JitRL（纯文本）。
- **预登记坍缩风险**：IAD 2504.01931（agentic loop 胜 one-shot BoN：Sketch2Code/Text2SQL ~3–4pt，
  WebShop 达 8–10%——数据集依赖，勿只引低端；claim-ledger #10）。
- **kill-if**：等预算下 loop ≤ one-shot BoN（续40 四探针不覆盖此测试——留 Stage-1C/后续实验）。
- **pivot-if**（决策包既有）：loop ≈ 一次性 rerank → 只是 test-time compute，非新 agentic-RL 系统。

## 7. same-selector contract（跨任务共享算子的冻结面；open item 3 交付）

> **适用范围**：本表冻结 I1/bare-I2/strict-I2/I3/I4 的池内选择算子面；UMBRELLA 的**环内每一步选择
> 动作**仍受本表约束，环结构本身按 §6 单独刻画（「工具环≠池内选择」的分类法与 §6 不冲突）。

| 维度 | 冻结值（跨任务不变） | task-specific（显式留空处） |
|---|---|---|
| 算子类别 | **仅池内选择**（in-pool selection）；扩池/改写/工具环/权重更新=不同对象，禁混写（P0-R7 分类法） | — |
| 打分信号输入 | 须**显式登记**输入模态（纯文本 vs 音频接地——此轴即 I1↔bare-I2↔strict-I2 分界）与来源（same-core / external-frozen / external-trained） | 具体信号族按任务/身份实例登记 |
| 信息边界 | 决策时 **label-free**：test-item gold 不入 selector/reward/prompt/检索/候选构造；read-out 允许、new-info 禁止 | — |
| 池几何 | 同一冻结模型在供给 c 下采样 K 个候选；解码参数/温度必须登记 | K 与温度按任务定，须登记 |
| 预算 | selector 计算量计入成本；对比一律**等 K**；**MBR 同 K 为强制基线** | — |
| 弃权 | 仅 I3 类实例允许，须预先声明 | 弃权代价按任务定 |
| 评估 | 部署用 label-free proxy `S`、评估用 `U`，二者不混；ρ **cellwise-only**（禁无权重总平均）；四量并列：rho_greedy / rho_pool / delta_mbr / regret；分母过小标 `HEADROOM_TOO_SMALL` 只报绝对量 | 各任务 U（−WER/EM/…）与 SESOI（Stage-2 冻结） |
| oracle | 池内按 U 最优，逐格定义与分母显式登记 | — |

## 8. Post-hoc 条件日志（冻结后强制；含签核前预置行）

任何身份自本合同签核起**新增/收窄/放宽任何限定词**，必须在此表追加一行——新增时间、触发论文、
是否改变 novelty 判定；不登记即视为违规（合取洗白防线）。签核前的既有变更以「预置」行如实入表。

| 日期 | 身份 | 变更 | 触发论文/事件 | novelty 判定是否改变 | 登记人 |
|---|---|---|---|---|---|
| 2026-07-14（预置，签核前既有） | UMBRELLA | 「advantage→next action」锐化（首现续36） | Survey v2 猎杀轮 | 否 | 协调者 |
| 2026-07-14（修正案 №1，待 owner 重签生效） | strict-I2 / UMBRELLA / same-selector | δ_corr 拆名（选择重合移出语义）+ strict-I2 kill-if 重写为两独立测试（音频接地 matched-controls 版 / 同错×无互补）+ §7 对 UMBRELLA 覆盖撤回 | 第三轮复审 §6.3/9.2（构念替换裁定） | 否（判据可执行化 + 合同适用范围更正，不动任何身份定义与占据裁决） | 协调者 |

## 9. Owner 签核

```text
签核语义：冻结以上六份定义+判据与 same-selector contract；此后变更走 §8 日志。
签核不构成：对任何占据/无匹配裁决的科学终审（那些仍待 P1 双审与盲审）。
owner: 已签核 —— 2026-07-14，AskUserQuestion 治理裁决（问题「身份合同 v1 + same-selector
contract——签核冻结？」答「签核冻结」；签核前 owner 获交台账承重发现摘要：KIT ST +6.11 纠错、
SQA/SSUM 负兑现、JudgeBoN=rho_pool、ernez 置信/覆盖更正、MBR ~31% 数据依赖）。
记录性质：治理性定义冻结裁决，非审计签署（续39 纪律）。
```
