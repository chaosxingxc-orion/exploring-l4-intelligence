---
artifact_id: "SF-STAGE1B-OPENING-TABLES-V4-2026-07-19-01"
title: "Stage-1B 开局保证表 v4（v9 复审 P1/P2 补链;超越 v3 于新日期件,v1–v3 字节不动）"
date: 2026-07-19
supersedes: "wiki/survey/2026-07-19-sf-stage1b-opening-tables-v3.md（v3;审计纪律:更正走新日期件）"
discipline: "五表互不混分母;保证 = 零查询确定性 carry-forward;执行首轮按 taxonomy v5/schema-v2 单写链编码(signals[]+字段绑定证据+裁决行哈希)再入正常 BFS/DFS 排序;归档不是遗忘许可"
provenance_note: "v4 新增 = v9 复审 §5.3 P1 四项 + §5.4 P2 六项,全部经 2026-07-19 反幻觉核验(access log v9-review-verification);新增项按摘要只定队列位置,绝不从摘要直接编码占据"
delta_note: "相对 v3:表 A Reinforced Agent 行加 GEM↔arXiv 去重绑定;表 B 新增 trained-RM 标注分节 +2;表 D +2(Mapping Smarter/ASR-TRA);表 E +6(P2 系统控制与 speech 边界);其余行照录 v3 不变"
---

# Stage-1B 开局五张保证表（v4）

## 表 A：system/control method paths——v3 表 A 全体照录（本表集合内单一行内更新）：

| 工作 | 保证 provenance | 备注 |
|---|---|---|
| Reinforced Agent: Inference-Time Feedback for Tool-Calling Agents | REVIEWER_KNOWN_ITEM（v8 复审 P1-1）;**去重绑定（v9 复审 §5.1）:正式版 = ACL GEM 2026 `2026.gem-main.13`（2026-07-19 官方页核验,题名/作者与 arXiv 2604.27233 完全一致）——同 work 双 ID,登记以 ACL 正式链接优先** | RQ-SYS 直接近邻;reviewer 优化态必须拆 path 编码 |

（其余 10 行 = v3 表 A 原文照录,内容不变）

## 表 B：speech/omni 测量工具（MEASUREMENT_INSTRUMENT——不入方法占据分母;v3 表 B 八行照录不变）+ **新增 B-2 分节：trained speech reward instrument（v9 复审 §5.3 P1-3/P1-4——评审明令标注「trained RM,不满足全系统零训练」,作 reward-element 边界工具登记,永不计入 TF-Strict 方法占据）**

| 工具 | ID | 保证 provenance | 边界标注 |
|---|---|---|---|
| **Dual-Axis Generative Reward Model（semantic+turn-taking 双轴生成式 RM,交互口语对话）** | 2026.acl-long.6 | REVIEWER_KNOWN_ITEM（2026-07-19 官方页核验:trained 生成式 RM,双轴评价+RL 反馈适用）;**〔provenance 澄清:评审称「仓内 2026-07-06 reward survey 已读过」——我方定向检索仅见同聚簇 SpeechJudge-GRM/GSRM/UniSRM/SDiaReward 在案,未见本篇;如实登记为 REVIEWER_KNOWN_ITEM,待评审确认或给 locator〕** | **trained RM**——RQ-OMNI/RQ-MEASURE 语义×时序双轴测量参照 |
| **SDiaReward / ESDR-Bench（口语对话偏好 RM,自然口语/声学表达建模）** | 2603.14889（ACL 2026） | **仓内在案:2026-07-06 archive `eval-methodology.md` §13 全文裁定（trained element/Training-free: no）+ 2026-07-14 search log trained-audio-judge 聚簇——「看过但遗忘」类第六例（归档件),按评审前令登记 carry-forward 不称首次发现** | **trained RM**——补表 B「只有 benchmark 无 speech reward instrument」缺口 |

## 表 C：evaluator/reward 负结果先验（claim key NEG-P1..P10;v3 表 C 照录不变）

## 表 D：黑盒边界检验队列（KNOWN_QUEUE/BOUNDARY;v3 表 D 三行照录 + 新增 2 行）

| 工作 | ID | 角色 | 边界轴 |
|---|---|---|---|
| （v3 三行照录:RFG 2509.25604 / DEGS 2607.09693 / Training-Free GRPO 2510.08191） | — | — | — |
| **Mapping Smarter, Not Harder（test-time RL agent,无标签无权重更新）** | 2025.emnlp-industry.75 | **new-info 边界（v9 复审 P1-1）;仓内在案:correction-4 复审+p0r8 复审+哨兵登记** | confidence reward 推理时迭代控制映射 + **发起 web search 获取外部证据**——「零权重更新但 new-info」的 RQ-SYS/信息边界最直接反例;预期 route=test-time RL/agent lane 族 |
| **ASR-TRA（Boosting ASR Robustness via Test-Time RL with Audio-Text Semantic Rewards）** | 2603.05231 | **测试时权重/prompt 更新边界（v9 复审 P1-2）;仓内在案:2026-07-13 scout ledger 完整定性** | audio-text reward 但更新 model 与 learnable prompt ≠ TF-Strict;同时命中 speech×test-time RL×reward 的最重要名称/身份边界之一;预期 route=speech/ASR lane 族 |

## 表 E：Stage-1B 首批发现/筛选队列（P2;v3 三行照录 + v9 复审 §5.4 新增 6 行,各带首批检查点）

| 工作 | ID | 首批检查点 |
|---|---|---|
| （v3 三行照录:TRACE findings-acl.651 / LWE eacl-short.50 / Min-Seek findings-eacl.153） | — | — |
| TangramSR（training-free VLM verifier-refiner,几何一致性 reward 递归修正） | 2602.05570 | 多模态 reward loop 直接近邻;verifier 训练性与信号身份 |
| OrchRM（orchestration 层训练 RM+MAS TTS） | 2606.13598 | trained RM=TF-Strict 边界;orchestration 层信号→权利映射 |
| ToolRM（trained 工具 RM 家族,BoN/self-correction/推理时扩展） | 2026.findings-acl.419 | tool decision reward 边界;与 Reinforced Agent 的 reviewer 信号对照 |
| Agent-RRM（结构化 critique+score 驱动 agent 精炼） | 2026.findings-acl.95 | reward model/integration 训练路径;critique 信号 lifecycle |
| DuplexPO（FCDR 因子化会话动力学奖励,full-duplex RL post-training） | 2607.07148 | 权重更新强边界;turn initiation/backchannel/yielding 分轴 reward 设计参照（RQ-OMNI） |
| Multi-Faceted Interactivity Alignment（四轴交互奖励+LLM 语义奖励 post-training） | 2606.11167 | 权重更新边界;RQ-OMNI/RQ-MEASURE 交互分轴测量参照 |
