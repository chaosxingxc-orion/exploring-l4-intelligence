---
artifact_id: "SF-V5-CLAIM-EVIDENCE-MATRIX-2026-07-18-01"
title: "Proposal v5 增补 claim-evidence 矩阵（scope = v5 更正版新增数字与量词;与 v4 矩阵并用,各自 frontmatter 载明 scope）"
date: 2026-07-18
scope: "v5 更正版正文全部百分比/区间/倍数/量词类 claim;v4 已覆盖项不重复(指针 = v4 矩阵);占据合取量词的唯一正典 = identity taxonomy 机器重算输出"
discipline: "五值证据模式(amendment-9 §2);SOURCE_REPORTED_TRACEABLE 恒填『未复算』;量词类 claim 必须给机器重算输入,零 orphan"
---

# v5 增补 claim-evidence 矩阵

## §1 量词/合取类（MACHINE_RECOMPUTED_LOCAL——identity taxonomy **v5** 重算,输入 = coding-**v6**.json 11 条 method path〔schema-v2 sidecar 单写链生成,signals[] 实例〕;〔dated correction 第五版 2026-07-19:v8 复审三 Gate MAJOR 整改——rq 派生存在量词化到同信号+同用途粒度,承重字段证据完备合同+裁决行哈希,双平台重放;数值经重算不变;第四版及旧行随 git 历史留档〕〔第四版注:v7 复审整改加因果 edge 要求;第三版注:PDR 源文错码致 3/11 撤回〕）

| claim ID | 陈述 | 复算入口（`sf_identity_taxonomy_v5_test.py` 持久化输出;全部双分母+双政策敏感列;Windows/WSL2 双端同值） | 独立复验 |
|---|---|---|---|
| V6-Q01 | is_s0_core_compatible = 0/11;is_rq_sys_control_compatible = 5/11 路径（4/8 works）;is_project_method_candidate = 0/11（重立后的待检验空位坐标） | occupancy.policy_A → 对应键 | 是 |
| V6-Q02 | strict∧reward∧K 池（机制分层非身份）= 轨迹池 **2/11 路径（unique work 1/8**,#rtv 与 #pipeline 同一篇;PDR 按 TeX 更正后原 3/11 撤回〕 | strict_AND_reward_AND_pool_BY_selection_object（双分母） | 是（eprint sha 一手核验） |
| V6-Q03 | is_reward_guided = 6/11（PDR 无信号/ToolGate 门/consensus×2/ToT 裁决出列） | is_reward_guided（双分母） | 是 |
| V6-Q04 | trained-PRM∧K 池 = 1/11（DREAM） | learned_rm_prm_AND_pool | 是 |
| V6-Q05 | 原生 audio/omni 进核 = 0/11 | core_native_audio_or_omni | 是 |
| V6-Q06 | 拓扑政策 A 与严格拓扑敏感列双算（CE-1b 在敏感列非空洞） | occupancy.sensitivity_strict_topology + V5b 检查 | 是 |
| V7-Q08 | reward_guided_selection = 4/11（§7.6 拆轴:candidate_pool_exists/selection_policy 分离;PDR random-K 池事实保留而永不计入 reward 选择）;rq_sys = 5/11 要求 ≥1 有效因果 edge（K4/K5/K6 killer 在案） | occupancy.policy_A.reward_guided_selection + V3 killer 检查 | 是 |
| V5-Q07v2 | exposure union 计数（W1+umbrella 27;W4 ≈70 组级事件） | **证据模式降格（P1-3）:REVIEWER_INFERENCE + TEAM_ATTESTATION 考古估计**——组级行含多运行,无规范化 event ledger;ledger 化延至 Stage-2 held-out 冻结前 | 否（估计类） |

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
