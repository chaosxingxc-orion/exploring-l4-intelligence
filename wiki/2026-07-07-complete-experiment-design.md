---
title: "知识轨 · 完整实验设计(重规划 / pre-registration)"
date: 2026-07-07
stage: 1→2 实验预注册
status: "重规划,替代被泄漏污染的 T7 单点。三条硬约束写死。执行前 owner 审。boundary-clean、directional→powered。"
---

# 完整实验设计(重规划)

> 起因:上一版 T7 三处硬伤——#1 覆盖不足(仅 3 单跳知识-QA、无 agentic)、#2 检索 query 用了 gold 文本(部署应为音频)、#3 **KB 逐条含 ground truth**(审计 answer_in_own_KB=1.0、注入含答案率 0.90)→ "RAG 增益"实为查答案。本设计系统性修正三者。

## 1. 三条硬约束(写死,任何实验不满足即无效)
- **A 音频输入:** 一切 query/输入是**音频**;检索 query 来自 **omni 自身 ASR** 或 **omni-embed 音频原生检索**;**绝不用 gold 文本**(部署时不可得)。
- **B KB 不含答案:** 外部知识**≠ test 答案**。三重把关:**provenance-firewall**(KB 由与 test 答案不相交的来源建)+ **answer-overlap 审计**(注入文本与 gold 的 n-gram/蕴含重叠→剔除高重叠→重跑,增益须存活)+(reading-comp 场景)**答案擦除**。gold 仅用于**打分**(held-out,绝不注入)。
- **C 覆盖矩阵:** semantic 与 agentic 分别明确可测性(§2),不谎报"全覆盖"。

## 2. 测试床有效性分类(核心判据:答案能否与 KB 分离)
| 任务类 | 数据集 | 答案 vs KB | 对知识-RAG 是否干净可测 |
|---|---|---|---|
| **知识/推理 MCQ** | **OpenbookQA-zh**(原生有 fact-book!)· mmau-mini · big-bench-audio | 答案=选项;外部**事实 KB 不含选项** | **✅ 干净正测**(首选 OpenbookQA:配套 1326 科学事实做外部 KB,答案不在其中) |
| reading-comp QA | heysquad · spoken-squad · SQuAD-zh | 答案∈passage | ⚠ RAG=查答案;**仅答案擦除后**作诊断(测"周边知识是否帮到"),非知识增强正测 |
| SLU/ASR/SER/SID | minds14 · crema-d 等 | 非知识-QA | ✗ 外部知识不适用,排除(属其它能力) |
| **agentic**(多轮/工具) | audiomc · eva-bench · uro-bench · tau2 | 工具/记忆/对话,非知识检索 | ✗ 干净知识-RAG **需构造**;→ E4 构造最小台 或 论证性 defer |

**结论:唯一"零构造即干净"的知识-RAG 正测 = OpenbookQA-zh + 其 fact-book 外部 KB**(须先核实 fact-book 是否在盘/可取,E0);其余要么擦除诊断、要么排除、要么构造。

## 3. 知识-使用模式对比(owner 提出的两条)
- **Mode-B RAG:** audio-ASR-query → 检索多个文本片段 → 注入 → 冻结 omni 作答。
- **Mode-A few-shot 任务定义:** 用**语音+文本 demo**(k 个)在 prompt 内定义任务/示范作答。
两者都 **audio-input、边界干净**;对比谁更能提升利用效率(且都不含 test 答案)。

## 4. 对照与指标(每个正测都带)
- 对照:**mismatch-placebo**(注入错配知识须不涨)· **oracle-retrieval-ceiling(答案擦除版)**(分离"无 headroom"vs"检索太弱")· **answer-overlap 剔除后重跑**。
- 指标:base vs 各 arm 的 **paired-bootstrap 95% CI**;audio-ASR-query 的 **retrieval hit@k**;**post-scrub/overlap answer-presence**(验证 KB 真不含答案,应≈0)。
- 分级:首轮 n≤60 directional 定方向;结论须 n≥150 powered 复现。

## 5. 分阶段执行(→ 任务表 E0–E6)
- **E0 测试床有效性 + KB 可得性核实**(含 OpenbookQA fact-book 是否在盘;reading-comp 擦除诊断 = 正在跑的 bgpeaild9)。
- **E1 构建边界干净 KB**(OpenbookQA 事实 KB / 擦除 KB)+ answer-overlap 审计(证 KB 不含答案)。
- **E2 semantic 知识-RAG 矩阵**:base vs RAG(audio-query、clean KB)+ 全对照 → **干净 H0**。
- **E3 知识-使用模式对比**:Mode-B RAG vs Mode-A few-shot(both audio-input)。
- **E4 agentic 知识任务**:构造最小边界干净多轮知识任务 或 论证性 defer(附理由)。
- **E5 TFRL 杠杆**:**仅当 E2 显示干净 headroom**,才测 reward-guided(门控/注入格式/when-gate)vs 干净 RAG 基线;绑定 Lean τ。
- **E6 理论链 + 重画结论**:把 clean 结果接 `Realization.lean`(τ 收敛),在**干净证据**上重答三问。

## 6. 幸存/待重做清单(诚实)
- **幸存(清白):** Lean 收敛证明(`Realization.lean`,纯理论)· 调研/taxonomy(argumentation)· effect-map(设计)。
- **待重做(被泄漏污染):** T7 的 H0/inject_k/R1-gate 全部经验主张 → 由 E2 干净重测取代;结论文档 ①② 已挂作废横幅,待 E6 重画。
