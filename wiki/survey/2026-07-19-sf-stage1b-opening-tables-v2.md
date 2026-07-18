---
artifact_id: "SF-STAGE1B-OPENING-TABLES-V2-2026-07-19-01"
title: "Stage-1B 开局保证表 v2（v7 复审 P1 补链;超越 v1 于新日期件,v1 字节不动）"
date: 2026-07-19
supersedes: "wiki/survey/2026-07-18-sf-stage1b-opening-tables.md（v1;audit 纪律:更正走新日期件,原件保留）"
discipline: "四表互不混分母（Round B 分析单位纪律）;保证 = 零查询确定性 carry-forward（不冒充 query recall、不要求 Stage-1A 精读完、执行首轮先按 taxonomy v4 编码入 sidecar 单写链再入正常 BFS/DFS 排序）;归档不是遗忘许可"
provenance_note: "「查询命中」列 = 离线正典 matcher 复现(非联网执行);v2 新增四项 = v7 复审 §7.3–§7.5 P1 供给,全部经 2026-07-19 反幻觉核验(access log v7-review-verification);新增项按摘要只定队列位置,绝不从摘要直接编码占据"
version_note: "编码队列版本随 v7 复审整改升级:taxonomy v4(control_edges 因果派生)+ coding v5(sidecar 单写链);v1 中 taxonomy v3/coding-v4 字样由此取代"
---

# Stage-1B 开局四张保证表（v2）

## 表 A：system/control method paths（13 轴 + taxonomy v4 编码队列）

已深读 8 项（11 method paths,coding-v5 在案,sidecar 单写链）+ 以下晋升/补入项保证编码：

| 工作 | 保证 provenance | 备注 |
|---|---|---|
| Scaling Test-time Compute for LLM Agents (2506.12928) | **查询命中 SF-L2-Q1/L5-Q5/L8-Q5〔我方复现——更正复审「不命中 65 query」事实句〕+ SEED_GUARANTEED + PRIOR_SURVEY_CARRY_FORWARD（2026-07-04 L4 件精读在案）** 三重 | agent 并行采样/顺序修订/verifier/merging 系统比较——直接回答 RQ-SYS/RQ-CTRL,最高优先 |
| **Step-level Verifier-guided Hybrid TTS (2025.emnlp-main.931, Chang et al., EMNLP 2025)** | **REVIEWER_KNOWN_ITEM（v7 复审 §7.3 P1 直接近邻;2026-07-19 官方页核验:training-free,process verification 引导 conditional step-level self-refinement + parallel 组合）** | **P1 carry-forward 最高优先新增**;编码时至少拆两条 method path:①conditional sequential refinement ②hybrid parallel/sequential composition;重点编码 verifier 是否训练/signal→right control edge/内部状态依赖/label 依赖 |
| IAD / Feedback in TTS of Agentic AI Workflows (2504.01931) | SEED_GUARANTEED | feedback vs diversity-only BoN 直接对比 |
| LATS (2310.04406) | SEED_GUARANTEED | gradient-free tree search + LM value/self-reflection + 环境反馈系统近邻 |
| Tree Search for Language Model Agents (2407.01476) | SEED_GUARANTEED（兼哨兵） | 真实 web 环境推理时搜索 |
| JitRL (2601.18510) | SEED_GUARANTEED | 无梯度经验记忆+advantage 但依赖 logits——「方法最近、接口不合」关键边界 |
| Omni-Decision (2607.11433) | SEED_GUARANTEED（在册最高优先威胁） | training-free omni evidence-state 系统;含 web/new-info,非 strict identity 但系统威胁最高 |
| Rethinking Thinking Tokens（PDR 原始论文,2510.01123,Madaan et al.） | REVIEWER_KNOWN_ITEM（v6 复审 P1-2;Agentic Coding TeX 引文键 pdr-paper 一手可见） | PDR 谱系源头;inference orchestration 与 trained-8B 两路径分行编码——TF-Strict 拆分检验件 |
| SWE-Replay (2601.22129,Ding et al.) | REVIEWER_KNOWN_ITEM（TeX 引文键 swe-replay-paper） | 历史轨迹复用+branch decision rights+无显式 reward selector——检验「是否错误要求 K 池/标量 reward」的高价值近邻 |

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

## 表 C：evaluator/reward 负结果先验（BOUNDARY/NEGATIVE_PRIOR——供 Stage-1B 编码轴与 Stage-1C 卡「反证列」引用;全部指针至 DFS 记录,数字 SOURCE_REPORTED;**claim key 列 = v7 复审 §7.1 可追踪性要求**）

| claim key | 先验 | 来源 | DFS/记录载体 |
|---|---|---|---|
| NEG-P1 | trained PRM 与 training-free critic 均不敌多数投票;池准确率越高近平衡选择器净转负 | 2607.09438 | 七篇 DFS 批 B |
| NEG-P2 | 弱开源模型 self-refinement 退化;内部 confidence 不可靠;外部 verifier>内部 confidence | 2512.11109 | 七篇 DFS 批 A |
| NEG-P3 | over-compute 失焦;指令遵循能力=供给生效前提 | 2606.28864 | 七篇 DFS 批 B |
| NEG-P4 | self-verification 封顶于核心自身理解力（SVF<GPT-4o） | 2512.19433 | 七篇 DFS 批 B |
| NEG-P5 | 顶部质量段 judge-人类对齐崩（τ=−0.15）;α 过剪退化;random pruning 显著更差 | Selective TTS (ACL 1724) | known-item DFS 批 B |
| NEG-P6 | 外部控制器优于模型 prompt 自调节（自报 VoI 降精度反增调用） | ToolGate (2606.03054) | known-item DFS 批 B |
| NEG-P7 | DeepVerifier 迭代早峰后回落（correct→incorrect 迁移跨轮持续） | ACL 1243 | known-item DFS 批 B |
| NEG-P8 | symmetric debate 无超越 majority 增益;naive parallel scaling 非普遍有益（引用负结果） | ATLAS 引文 | known-item DFS 批 A |
| NEG-P9 | 无外部反馈的自条件化迭代增益（RQ-CTRL 强反例/替代解释:增益或来自供给设计非 reward 引导） | TRT (2602.03094,Zhuang et al.;TeX 引文键 test-time-recursive-thinking-paper) | v6 复审 P1-2 登记,KNOWN_QUEUE 边界/反证队列 |
| **NEG-P10** | **低 N 预算下 outcome-BoN 与 process-tree-search verifier 效用受 verifier 域特化/规模制约;majority/self-consistency 强基线难破（legal MCQA 域内）** | **Evaluating the Role of Verifiers in TTS for Legal Reasoning (2025.nllp-1.15, Romano/Schwarz/Giofrè, NLLP@EMNLP 2025)** | **仓内早期审计在案:wiki/2026-07-11-survey-full-verification.md:59,229;v7 复审 §7.5 回链修复(附录漏收更正);2026-07-19 官方页核验** |

## 表 D：黑盒边界检验队列（KNOWN_QUEUE/BOUNDARY——v7 复审 §7.4;检验「api_only/内部可见性」轴的一致性,**不因 training-free 标题计入 project method**）

| 工作 | ID | 角色 | 边界轴 |
|---|---|---|---|
| RFG: Reward-Free Guidance for dLLM Reasoning (Chen/Xu/Leskovec/Ermon) | 2509.25604 | implicit-reward 边界 | enhanced/reference dLLM 对数似然比参数化轨迹奖励——inference 期无显式 RM,但依赖内部概率 + 增强模型上游 RL/SFT 来源→ internal_visibility + upstream-training 双轴出界检验件 |
| Depth-Entropy Guided Sampling (DEGS, Meng/Xie/Chen) | 2607.09693 | internal-state 边界 | layer-wise entropy collapse 作伪奖励 + MCMC;training-free 但需内部层状态→ 预期 internal_visibility=hidden_state 出界——恰好检验 taxonomy 边界一致性(api_only 轴的阳性对照) |
