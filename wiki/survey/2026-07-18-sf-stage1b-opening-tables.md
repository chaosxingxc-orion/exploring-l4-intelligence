---
artifact_id: "SF-STAGE1B-OPENING-TABLES-2026-07-18-01"
title: "Stage-1B 开局三张保证表（v5-response 复审 P0-2;owner 裁决② 2026-07-18）"
date: 2026-07-18
discipline: "三表互不混分母（Round B 分析单位纪律）;保证 = 零查询确定性 carry-forward（不冒充 query recall、不要求 Stage-1A 精读完、执行首轮先编码再入正常 BFS/DFS 排序）;归档不是遗忘许可"
provenance_note: "「查询命中」列 = 离线正典 matcher 复现(非联网执行);全部命中留痕于本批核验记录"
---

# Stage-1B 开局三张保证表

## 表 A：system/control method paths（13 轴 + taxonomy v2 编码队列）

已深读 8 项（11 method paths,coding-v3 在案）+ 以下 6 项晋升保证编码（全部种子在册）：

| 工作 | 保证 provenance | 备注 |
|---|---|---|
| Scaling Test-time Compute for LLM Agents (2506.12928) | **查询命中 SF-L2-Q1/L5-Q5/L8-Q5〔我方复现——更正复审「不命中 65 query」事实句〕+ SEED_GUARANTEED + PRIOR_SURVEY_CARRY_FORWARD（2026-07-04 L4 件精读在案）** 三重 | agent 并行采样/顺序修订/verifier/merging 系统比较——直接回答 RQ-SYS/RQ-CTRL,最高优先 |
| IAD / Feedback in TTS of Agentic AI Workflows (2504.01931) | SEED_GUARANTEED | feedback vs diversity-only BoN 直接对比 |
| LATS (2310.04406) | SEED_GUARANTEED | gradient-free tree search + LM value/self-reflection + 环境反馈系统近邻 |
| Tree Search for Language Model Agents (2407.01476) | SEED_GUARANTEED（兼哨兵） | 真实 web 环境推理时搜索 |
| JitRL (2601.18510) | SEED_GUARANTEED | 无梯度经验记忆+advantage 但依赖 logits——「方法最近、接口不合」关键边界 |
| Omni-Decision (2607.11433) | SEED_GUARANTEED（在册最高优先威胁） | training-free omni evidence-state 系统;含 web/new-info,非 strict identity 但系统威胁最高 |

## 表 B：speech/omni 测量工具（MEASUREMENT_INSTRUMENT——**不入方法占据分母**;为 RQ-OMNI/RQ-SAFE 提供「哪里可测、哪里会失败」）

| 工具 | ID | 保证 provenance | 查询命中（离线复现） |
|---|---|---|---|
| τ-Voice（全双工语音 agent 真实域基准,voice/text 直接对照） | 2603.13686 | REVIEWER_KNOWN_ITEM + 旧 survey 在案 | SF-L3-Q3 + SF-L12-Q3 |
| Full-Duplex-Bench-v3（真实语音+disfluency+多步工具调用） | 2604.04847 | 同上 | SF-L3-Q3 |
| **EchoChain（中断下状态更新推理）** | 2604.16456 | REVIEWER_KNOWN_ITEM;**65 查询零命中且不在种子（复现坐实）→ 本表保证入口 + vocabulary-drift 队列 axis=full-duplex/interruption 第 1 例** | **零命中** |
| From Text to Voice（text→audio tool-calling 可复现评价框架,RQ-OMNI 配对工具） | 2605.15104 | REVIEWER_KNOWN_ITEM | SF-L3-Q1/Q2/Q3 + SF-L5-Q2 |
| VoiceAgentBench | 2510.07978 | 旧 survey 在案（semantic-tfrl [157]） | 执行首轮登记时补测 |
| Audio2Tool（Speak-Call-Act 语音工具使用数据集） | 2604.22821 | 旧 survey 在案（[158];W1 基线网格已含其数据集键=exposure union 在册） | 执行首轮登记时补测 |
| tau-bench（工具-agent-用户交互基准） | 2406.12045 | SEED_GUARANTEED + 旧 survey [108] | 种子兜底 |
| tau2-bench voice | GitHub sierra-research/tau2-bench | 旧 survey [151]（非 arXiv,资源类登记） | 官方源路径 |

## 表 C：evaluator/reward 负结果先验（BOUNDARY/NEGATIVE_PRIOR——供 Stage-1B 编码轴与 Stage-1C 卡「反证列」引用;全部指针至 DFS 记录,数字 SOURCE_REPORTED）

| 先验 | 来源 | DFS 载体 |
|---|---|---|
| trained PRM 与 training-free critic 均不敌多数投票;池准确率越高近平衡选择器净转负 | 2607.09438 | 七篇 DFS 批 B |
| 弱开源模型 self-refinement 退化;内部 confidence 不可靠;外部 verifier>内部 confidence | 2512.11109 | 七篇 DFS 批 A |
| over-compute 失焦;指令遵循能力=供给生效前提 | 2606.28864 | 七篇 DFS 批 B |
| self-verification 封顶于核心自身理解力（SVF<GPT-4o） | 2512.19433 | 七篇 DFS 批 B |
| 顶部质量段 judge-人类对齐崩（τ=−0.15）;α 过剪退化;random pruning 显著更差 | Selective TTS (ACL 1724) | known-item DFS 批 B |
| 外部控制器优于模型 prompt 自调节（自报 VoI 降精度反增调用） | ToolGate (2606.03054) | known-item DFS 批 B |
| DeepVerifier 迭代早峰后回落（correct→incorrect 迁移跨轮持续） | ACL 1243 | known-item DFS 批 B |
| symmetric debate 无超越 majority 增益;naive parallel scaling 非普遍有益（引用负结果） | ATLAS 引文 | known-item DFS 批 A |
