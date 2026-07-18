---
artifact_id: "SF-STAGE1B-OPENING-TABLES-V3-2026-07-19-01"
title: "Stage-1B 开局保证表 v3（v8 复审 P1 补链;超越 v2 于新日期件,v1/v2 字节不动）"
date: 2026-07-19
supersedes: "wiki/survey/2026-07-19-sf-stage1b-opening-tables-v2.md（v2;审计纪律:更正走新日期件）"
discipline: "五表互不混分母;保证 = 零查询确定性 carry-forward;执行首轮按 taxonomy v5/sidecar schema v2 单写链编码(signals[]+claim_evidence+裁决哈希)再入正常 BFS/DFS 排序;归档不是遗忘许可"
provenance_note: "v3 新增三项 = v8 复审 §7.2 P1 供给,全部经 2026-07-19 反幻觉核验(access log v8-review-verification);P2 三项入首批发现/筛选队列;新增项按摘要只定队列位置,绝不从摘要直接编码占据"
delta_note: "相对 v2:表 A +2(Reinforced Agent/TF-TTCL)、表 D +1(Training-Free GRPO)、新增表 E(P2 首批队列);其余行内容随版本标签升级(taxonomy v4→v5/coding v5→v6)外不变——v2 全部行照录"
---

# Stage-1B 开局五张保证表（v3）

## 表 A：system/control method paths（13 轴 + taxonomy v5 编码队列）

已深读 8 项（11 method paths,coding-v6 在案,sidecar schema v2 单写链）+ 以下晋升/补入项保证编码：

| 工作 | 保证 provenance | 备注 |
|---|---|---|
| Scaling Test-time Compute for LLM Agents (2506.12928) | 查询命中 SF-L2-Q1/L5-Q5/L8-Q5〔我方复现〕+ SEED_GUARANTEED + PRIOR_SURVEY_CARRY_FORWARD 三重 | agent 并行采样/顺序修订/verifier/merging 系统比较——最高优先 |
| Step-level Verifier-guided Hybrid TTS (2025.emnlp-main.931, Chang et al.) | REVIEWER_KNOWN_ITEM（v7 复审 §7.3;2026-07-19 官方页核验） | 拆两条 method path:①conditional sequential refinement ②hybrid composition;重点=verifier 训练性/signal→right 因果边 |
| **Reinforced Agent: Inference-Time Feedback for Tool-Calling Agents (2604.27233, Ta et al.)** | **REVIEWER_KNOWN_ITEM（v8 复审 §7.2 P1-1;2026-07-19 官方页核验:reviewer agent 于执行前评价 provisional tool calls+progressive feedback;BFCL/Tau2-Bench +5.5~7.1%）** | **RQ-SYS 直接近邻新增**;编码假设:外部 reviewer 信号→在线 tool_call/retry 因果边候选;**reviewer prompt/model 的优化态必须拆 path 编码**(不因题名归 training-free);预期 route=feedback/verifier lane 族;去重 ID=2604.27233 |
| **Training-Free Test-Time Contrastive Learning (TF-TTCL, 2026.findings-acl.1482 / arXiv 2604.13552, Zheng et al.)** | **REVIEWER_KNOWN_ITEM（v8 复审 §7.2 P1-2）+ 仓内旧 search log 在案——〔诚信登记:此项为 correction-4 复审已登记「转录失败」事故的第二次复发:旧日志已发现→seed/census 消失→v8 附录/开局表仍漏列,「看过但遗忘」类第五例;本行按评审前令登记 provenance 不假装本轮首次发现〕** | frozen LLM+Explore–Reflect–Steer+textual rules 推理期检索;编码假设:规则库=记忆/供给轴,rule 抽取信号的 lifecycle 与 label 依赖为关键轴;预期 route=training-free/test-time lane 族;去重 ID=2604.13552↔2026.findings-acl.1482(ACL 正式版为准) |
| IAD / Feedback in TTS of Agentic AI Workflows (2504.01931) | SEED_GUARANTEED | feedback vs diversity-only BoN 直接对比 |
| LATS (2310.04406) | SEED_GUARANTEED | gradient-free tree search 系统近邻 |
| Tree Search for Language Model Agents (2407.01476) | SEED_GUARANTEED（兼哨兵） | 真实 web 环境推理时搜索 |
| JitRL (2601.18510) | SEED_GUARANTEED | 「方法最近、接口不合」logits 边界 |
| Omni-Decision (2607.11433) | SEED_GUARANTEED（在册最高优先威胁） | training-free omni evidence-state 系统 |
| Rethinking Thinking Tokens（PDR 原始论文,2510.01123） | REVIEWER_KNOWN_ITEM（v6 复审 P1-2） | PDR 谱系源头;两路径分行编码 |
| SWE-Replay (2601.22129) | REVIEWER_KNOWN_ITEM | 历史轨迹复用+branch rights 高价值近邻 |

## 表 B：speech/omni 测量工具（MEASUREMENT_INSTRUMENT——不入方法占据分母;v2 表 B 八行照录不变）

| 工具 | ID | 保证 provenance |
|---|---|---|
| τ-Voice | 2603.13686 | REVIEWER_KNOWN_ITEM + 旧 survey 在案（SF-L3-Q3+SF-L12-Q3 命中） |
| Full-Duplex-Bench-v3 | 2604.04847 | 同上（SF-L3-Q3） |
| EchoChain（65 查询零命中复现坐实→保证入口+drift 队列 full-duplex 轴第 1 例） | 2604.16456 | REVIEWER_KNOWN_ITEM |
| From Text to Voice | 2605.15104 | REVIEWER_KNOWN_ITEM（SF-L3-Q1/Q2/Q3+SF-L5-Q2） |
| VoiceAgentBench | 2510.07978 | 旧 survey 在案 |
| Audio2Tool | 2604.22821 | 旧 survey 在案（W1 基线网格 exposure union 在册） |
| tau-bench | 2406.12045 | SEED_GUARANTEED |
| tau2-bench voice | GitHub sierra-research/tau2-bench | 旧 survey 在案（资源类） |

## 表 C：evaluator/reward 负结果先验（claim key NEG-P1..P10;v2 表 C 十行照录不变——载体指针见 v2,不在此复制）

NEG-P1（2607.09438 PRM/critic 不敌 majority）/NEG-P2（2512.11109）/NEG-P3（2606.28864）/
NEG-P4（2512.19433 SVF 封顶）/NEG-P5（Selective TTS τ 崩+过剪）/NEG-P6（ToolGate 外控>自调节）/
NEG-P7（DeepVerifier 早峰回落）/NEG-P8（ATLAS 引文 debate/parallel 负结果）/NEG-P9（TRT 无外
反馈自条件化=RQ-CTRL 替代解释）/NEG-P10（legal-verifier 2025.nllp-1.15 低 N verifier 效用受限）。

## 表 D：黑盒边界检验队列（KNOWN_QUEUE/BOUNDARY——不因 training-free 标题计入 project method）

| 工作 | ID | 角色 | 边界轴 |
|---|---|---|---|
| RFG: Reward-Free Guidance for dLLM Reasoning | 2509.25604 | implicit-reward 边界 | enhanced/reference dLLM 对数似然比;internal_visibility+upstream-training 双轴出界检验件 |
| Depth-Entropy Guided Sampling (DEGS) | 2607.09693 | internal-state 边界 | layer-wise entropy 伪奖励;api_only 轴阳性对照 |
| **Training-Free GRPO (2510.08191, Cai et al.)** | **2510.08191** | **名称碰撞高危边界（v8 复审 §7.2 P1-3;仓内 v2 复审 2026-07-15 定性在案）** | **multi-epoch ground-truth 蒸馏 experiential knowledge 作 token prior 于 API 注入——base 冻结但发生系统外设标签学习:『论文所称 training-free』≠ 本项目 TF-Strict;开局即完成边界编码防同名当同定义;预期 route=training-free lane 族;去重 ID=2510.08191** |

## 表 E：Stage-1B 首批发现/筛选队列（P2——由首批系统查询捕获与筛选,不构成开门阻塞;v8 复审 §7.2 P2）

| 工作 | ID | 首批检查点 |
|---|---|---|
| TRACE: Efficient TTS via Temporal Reasoning Aggregation | 2026.findings-acl.651 | confidence 是否属 reward 形式;是否只控 stop（近期步一致性+confidence 聚合控停,training-free） |
| LWE: Becoming Experienced Judges (Selective Test-Time Learning for Evaluators) | 2026.eacl-short.50 | evaluator 经 evolving meta-prompt 持久化=外部控制器/记忆边界;selective 更新的信号身份 |
| Min-Seek: Thinking Long, but Short (Stable Sequential TTS) | 2026.findings-eacl.153 | training-free 序贯 scaling 无显式 reward——RQ-CTRL 反例/邻域;KV cache 管理非信号控制 |
