---
title: "T4 验证契约 —— R1 采纳门控 + R2 注入-格式(知识轨)"
date: 2026-07-07
stage: 1-argumentation → 实验预注册
status: "Pre-registration for T7. Boundary-clean by design. Stage-1 directional at run n; Stage-2 for power. Owner review pending; wiki-sync deferred。"
---

# T4 验证契约(R1 门控 + R2 注入-格式)

> 预注册 T7 要测的假设、基线、对照、奖励、边界与 go/no-go。锁定后 T6 建引擎、T7 执行,不事后改判据。

## A. 明确假设(可证伪)
- **A1 headroom:** 存在**外部知识**能关闭的知识 gap(冻结 omni 因缺事实而非缺感知答错)。T0 的 B>A 已**方向性**支持(部分)。
- **A2 消费:** 冻结 Qwen3-Omni 能 in-context 消费注入文本(T0 已确认**部分**:B>A 但 rescue~42%)。
- **A3 相关性信号:** omni-embed 的 query↔doc 相关性可用作**去相关**门控奖励(omni-embed ≠ 生成器)。
- **A4 边界可分:** 有用的外部知识 ≠ test 答案(存在"帮得上但不泄漏"的知识)。
- **A5(理论)** 门控/注入选择的奖励估计误差有界(C4)+ 步长/预算可控(C1/C2)——供 T5 Lean。

## B. 验证主张(逐条带 go/no-go)
- **H0 headroom(前置门).** 注入**oracle-检索到的正确外部知识条目**(非答案串)→ 在 omni 答错项上正确率上升。**go:** acc(oracle-retrieval-inject) − acc(no-inject) 的 paired-bootstrap 95% CI 排除 0;报"关闭了 T5 知识 gap 的几分之几"。**失败即停**(该 baseline 无可注入 headroom)。
- **H-util-gate(R1,主).** **奖励引导采纳门控** > **inject-top-k-always 地板**(拒掉 T0 里"拖累"的错配注入)。**go:** acc(gated) − acc(inject-all) CI>0;并报 context 内**检索精度**(admit 的相关比例)上升。第二基线:在**不训练 T5-large** 下追回 **CRAG**(2401.15884)evaluator 式增益的比例。
- **H-util-fmt(R2,叠加).** **best-of-N 注入格式选择**(raw/extractive/summary/prepended-terms)> **固定 top-k text-dump**;子杠杆 **per-item audio-payload vs 自转写**。**go:** CI>0;modality 子杠杆对 **omni(own-transcript)** 基线(perception-delta 方向性 +0.283 SQuAD-zh,directional)。
- 主张顺序:H0 门 → H-util-gate → H-util-fmt(叠加)。

## C. 对照原语(隔离效果、堵泄漏)
- **CP-provenance-firewall:** 知识库**只由训练/来源语料建**,所有 eval 项**及其答案/转写 held-out**;审计无 gold 进库。
- **CP-answer-overlap:** 审计每条被注入内容与 gold 答案的 n-gram/蕴含重叠;剔高重叠后**重跑**,增益须存活。
- **CP-mismatch-placebo:** 注入错配知识(T0 的 C 臂)必须**不**带来增益(否则是 priming/泄漏而非相关检索)。
- **CP-oracle-retrieval-ceiling:** 注入已知正确条目 = 检索上限,分离"无 headroom(A1 假)"vs"检索太弱(A3 假)"。
- **CP-transcript-key(R2 modality):** 转写基线用**模型自身 ASR**、绝不用 gold 转写(Guard Q1/Q2)。

## D. 奖励(边界干净、去相关)
- 门控/选择奖励 = **omni-embed 相关性/支持度**(proxy、去相关、非 gold)+ 可选 margin(`plurality_gate`)。**绝不读 test 答案/转写。**
- 报告奖励与 gold 正确性的相关度,证明它不是"伪装的 oracle"(CP-answer-overlap 施于奖励信号本身)。

## E. 统计与分级
- 所有端任务 delta:**paired-bootstrap 95% CI,≥150 held-out 项**(power);T7 首轮可先 n≤60 directional 定方向,再加 n 定论。
- Stage-1 directional;任何"结论"须 Stage-2 power 复现(paired-bootstrap + 全对照)。

## F. 边界纪律(写死)
- 注入=**外部知识非答案**;库=**训练池**;golds/转写**离线 held-out**;directional-only 标注;不伪造(我的 information-boundary over-reach 失败模式)。
