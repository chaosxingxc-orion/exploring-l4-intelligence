---
artifact_id: "SF-V5-CLAIM-EVIDENCE-MATRIX-2026-07-18-01"
title: "Proposal v5 增补 claim-evidence 矩阵（scope = v5 更正版新增数字与量词;与 v4 矩阵并用,各自 frontmatter 载明 scope）"
date: 2026-07-18
scope: "v5 更正版正文全部百分比/区间/倍数/量词类 claim;v4 已覆盖项不重复(指针 = v4 矩阵);占据合取量词的唯一正典 = identity taxonomy 机器重算输出"
discipline: "五值证据模式(amendment-9 §2);SOURCE_REPORTED_TRACEABLE 恒填『未复算』;量词类 claim 必须给机器重算输入,零 orphan"
---

# v5 增补 claim-evidence 矩阵

## §1 量词/合取类（MACHINE_RECOMPUTED_LOCAL——identity taxonomy v1 重算,输入 = coding-v2.json 9 条 method path）

| claim ID | v5 陈述 | 复算入口 | 独立复验 |
|---|---|---|---|
| V5-Q01 | 含 speech/audio = 0/9 路径〔已检视集合〕 | `sf_identity_taxonomy_test.py` → occupancy.includes_speech_audio | 是 |
| V5-Q02 | training-free∧reward-guided∧显式 K 池 = 3/9（Selective TTS/ToT/Agentic Coding） | 同上 → training_free_AND_reward_guided_AND_explicit_pool | 是 |
| V5-Q03 | strict-identity∧reward-guided∧K 池 = 1/9（Agentic Coding） | 同上 → strict_AND_reward_guided_AND_pool | 是 |
| V5-Q04 | all-system-training-free = 6/9;strict-identity bits = 2/9 | 同上 → all_system_training_free / project_strict_identity_bits | 是 |
| V5-Q05 | trained-PRM 引导 K 池 = 1/9（DREAM） | 同上（score_type=learned_rm_prm ∧ pool 过滤） | 是 |
| V5-Q06 | 候选空位坐标 = strict∧reward∧pool∧speech/omni,已检视集合中 0/9 | V5-Q01∧V5-Q03 合取;待 Stage-1B 检验〔REVIEWER_INFERENCE 级候选,非结论〕 | 合取机器可算;空位属性待检验 |
| V5-Q07 | exposure union 事件计数（W1+umbrella 27 + W4 补扫;终值见 union v2） | union v2 表行数机器可数;完成前一律下界表述 | 是（指针抽查） |

## §2 外部论文数字（SOURCE_REPORTED_TRACEABLE——未复算;效力限该论文报告的模型/任务/设置内）

| claim ID | v5 陈述 | 来源 locator | 独立复验 |
|---|---|---|---|
| V5-S01 | ATLAS 88.9% 轨迹恰在收敛点停 | 2606.01667 **GPQA-Diamond, Fig 7 panel(a)**（有可定义正确多数收敛点的轨迹子集,非跨基准总体） | 否（引文上下文逐字核验;数字未复算） |
| V5-S02 | ToolGate:prompt 自调节精度降至 60.0 且反增工具量;调用 2.73→1.02;token 64–69%;matched-domain +1.65 | 2606.03054 Table 3 / p2 / p7–8 | 否 |
| V5-S03 | Selective TTS:harsh judger τ=0.55;α=0.6 最优/α=0.8 过剪退化;61.64→65.86 | 2026.findings-acl.1724 §评估/Fig6/p34542 | 否 |
| V5-S04 | DeepVerifier 精度第 3–4 轮见顶后回落 | 2026.findings-acl.1243 Table 5 与迭代分析节 | 否 |
| V5-S05 | 可解析性修复 +~6pp;token 预算 +3.7pp vs 链数 +0.15pp;换策略模型 +11.4pp | 2607.09438 p.3–4 / p.4 / p.6 | 否（v4 矩阵 §3 同源条目,此处并入 v5 scope） |
| V5-S06 | SVF<GPT-4o（0.92 vs 0.95 / 0.66 vs 0.71 / 0.67 vs 0.74） | 2512.19433 p.8 Table 2 | 否 |
| V5-S07 | trained PRM 与 training-free critic 均不敌多数投票（该论文两池设置内） | 2607.09438 p.1/p.6–7 Table 4 | 否 |
| V5-S08 | DREAM 早停:GSM8K ~80% 步 / MATH ~5% 步 | 2026.findings-acl.511 p10512 | 否 |

## §3 结构/台账类（MACHINE_REPLAYED_STRUCTURE / MACHINE_RECOMPUTED_LOCAL——v4 矩阵 §1/§2 全部沿用,v5 无新增结构 claim;known-item 队列 10 项之 5 arXiv 命中留痕 = 本批 matcher 复现,复跑同 recall 实现）

## §4 TEAM_ATTESTATION（v4 矩阵 §5 沿用 + 本批新增）

| claim | 载体 |
|---|---|
| W2/W3 为零实验骨架（experiments/data 仅 .gitkeep,各 2 提交——四仓覆盖声明之两仓） | 本批核验记录 + 本件签字 |
| 仓外运行面边界（无未入仓的模型运行） | owner attestation（union v2 收尾字段） |
| owner 重申（2026-07-18 原文）:「Stage-1B 全程不得运行研究模型或 smoke」 | Decision-Log 续66 逐字登记 |
