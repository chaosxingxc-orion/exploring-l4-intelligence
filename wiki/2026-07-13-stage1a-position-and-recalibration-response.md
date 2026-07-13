---
title: "Stage-1A 位置声明与更正 · 对重校准审查的回复（全盘接受 + 两处供给条件性精化）"
date: 2026-07-13
responds_to: "wiki/2026-07-13-response-v6-stage1-recalibrated-review.md（sha256 b6268c80ae81a3c80634a7c89855ce28dcc36f2076a2febeb19900f5d92cd9e8）"
also_disposes: "中间审查 wiki/2026-07-13-response-v6-doctoral-adversarial-review.md（sha256 f5ad16e39da38b9de1f59147b019126f63cf825672b3d7682306e944acee70f5）——其文件级事实全部保留，其阶段错位项按重校准审查 §3 再分级表处置"
corrects_stage_identity_of: "wiki/2026-07-13-stage2-proposal-ASEL-v0.1-for-reviewer-verification.md @84c6cf64d0a979a5d4f8222a00b9eb746378f270（原文不改动）"
owner_rulings: "2026-07-13 会话五项（Decision-Log 续33）"
verification_mode: "协调者本人逐条核验（owner 指令：不委托）；重校准审查可核事实零驳回"
author: "协调者本人"
---

# Stage-1A 位置声明与更正 · 对重校准审查的回复

## 1. 当前位置声明：Stage-1A（问题界定）

按 owner 2026-07-13 采纳的 Stage-1A/B/C 细分（定义见 CLAUDE.md/AGENTS.md 术语表，`f57cd81`）：

- **当前 = Stage-1A**：广泛 survey、候选研究问题构造、原型空间纸面设计、新颖性/可行性/诚信风险
  审查；既有小样数字只作背景方向材料。
- **Stage-1B（方向性原型探索）未放行**：任何 P0–P6 类原型运行以 owner 显式放行为前置（放行前
  最低条件：本轮记录修复闭合 + survey 覆盖门 + 信息边界审计）。
- **Stage-1C（收官选题）在其后**：owner 基于 survey+原型决策包在候选身份中选唯一具体问题
  （kill/pivot/proceed/engineering-only），绝不自动滚入 Stage-2。

## 2. 阶段身份更正（S1-M1；append-only，原文不改）

`wiki/2026-07-13-stage2-proposal-ASEL-v0.1-for-reviewer-verification.md`（@`84c6cf6`）的正确身份为：

```text
STAGE1A_ARTIFACT / PRE_STAGE2_BLUEPRINT / NOT_CONFIRMATORY / NOT_A_STAGE2_ENTRY
```

其 frontmatter `stage: 2-solution-validation (entry draft)` 与正文 `Mode: confirmatory` **无现时
效力**：前者是阶段标签超前错误（Stage-1 收官未完成，不存在 Stage-2 入口），后者仅描述未来 M4 的
设计草图。该文档保留价值 = Stage-1C 若裁定 proceed 时的结构素材（冻结门 FG-1..FG-10 的清单思路、
隔离/信息边界契约），届时按 Stage-1C 选定的唯一问题**重写**，不原地升级。

**ρ 命名更正（S1-M2）**：该草稿 H4 定义的 ρ 用池均值锚，按术语表正名为 **rho_pool**；
Project-Thesis / Decision-Log / Per-Work-Status 的 ρ 为 **rho_greedy**（贪心锚）。两者此后
并列报告、绝不同名混用；分母过小标 `HEADROOM_TOO_SMALL` 只报绝对量。程序代号
`W1-ASEL-S2-001` 冻结弃用，Stage-1C 收官后按正名重发。

## 3. 对重校准审查的裁定：全盘接受（可核事实零驳回）

协调者本人核验记录（方法与结果详见会话记录，关键项）：五个快照哈希逐一比对一致；R6-M1/M2/M3
三项 v6 缺陷坐实（其中 YAML 缺陷经 PyYAML 实测复现：13 项仅存活 F-S7、M-S6）——三项均为协调者
本人造成，更正件已出（`2026-07-13-response-v6-correction.md`，schema 实测验证 13/13）；
S1-M2 ρ 漂移坐实（Project-Thesis L43 vs 草稿 H4）；S1-F1 坐实（Stolcke/Goel/NoRefER/HypR/READ/
ProGRes 全仓零覆盖，07-12 rescoring survey 系基线数字调研非方法祖先谱系）；对中间审查的再分级
转述抽查无失真。

机读处置：

```yaml
recalibrated_review_response:
  overall: ACCEPT_IN_FULL
  items:
    - {finding_id: S1-F1, disposition: ACCEPT, action: survey_coverage_gate_per_section7}
    - {finding_id: S1-F2, disposition: ACCEPT, action: identity_candidates_I1_I2_I3_plus_I4_to_stage1C_package}
    - {finding_id: S1-F3, disposition: ACCEPT_WITH_REFINEMENT, action: prototype_matrix_with_supply_stratification}
    - {finding_id: S1-M1, disposition: ACCEPT, action: this_document_section2}
    - {finding_id: S1-M2, disposition: ACCEPT, action: glossary_rho_split_landed_f57cd81_plus_section2}
    - {finding_id: S1-M3, disposition: ACCEPT, action: attempt_lineage_mapping_before_stage1B_release}
    - {finding_id: S1-M4, disposition: ACCEPT, action: correction_artifact_with_validated_schema_landed}
    - {finding_id: S1-M5, disposition: ACCEPT, action: information_boundary_audit_precedes_stage1B}
    - {finding_id: S1-M6, disposition: ACCEPT, action: stage1_closure_decision_memo_at_stage1C}
  interpretation_rules_section12: ACKNOWLEDGED_ALL_TEN
  allowed_forbidden_lists: ADOPTED_AS_OPERATING_CONSTRAINTS
  intermediate_review_disposition: file_level_facts_retained_stage_misaligned_items_per_regrade_table
```

## 4. 两处 ACCEPT-WITH-REFINEMENT（owner 供给条件性裁定的并入，非抗辩）

依据 owner 2026-07-13 裁定（经 survey 核验成立）：**oracle headroom 是供给条件量 H(c)**——
文献对应 best-of-N 理论的 coverage 条件（Huang et al., ICML 2025, arXiv 2503.21878）与
test-time compute 的难度条件性（Snell et al. 2024, arXiv 2408.03314）；自家数据同向
（裸核心 ASR 头空 +0.042 @N=8 vs heysquad 检索供给下 +0.517，相差一个数量级）。

1. **原型矩阵供给分层（精化 §6.1/§6.2/S1-F3）**：公共骨架由"同一候选池"改为**至少两个供给层**
   （裸核心 / +检索或前端供给），P0 的 headroom checkpoint 变为**供给分层的 headroom 地图**；
   一切 kill 判定遵循 **headroom 归因纪律**（术语表）：有头空的 null 才证伪选择器；无头空的
   null 只否定该供给配置，且换供给重试必须逐次登记，不得无限重试而只汇报成功。
2. **第四身份候选 I4（行使 S1-F2 的"或明确写出第四个"）**：**(供给 c, 选择器) 二元组**——
   科学问题指向"哪种供给创造头空、选择器在何种供给下兑现它"，与 I1（一般 selector）/I2（音频
   接地）/I3（约束/Goodhart）的问题结构均不同。仅登记为 Stage-1C 决策包的候选，现在不选。

## 5. Stage-1A 边界内的下一步（不含任何 1B/1C 执行细节）

记录修复（本轮已闭合）之后的 Stage-1A 正题 = **survey 覆盖门**（重校准审查 §7：八个方法家族、
逐篇字段表、两轮家族饱和、5–8 篇最近邻逐项 delta、"首次/无先例"句绑定检索截止日）——直接近邻
以 MBR/expected-WER、confidence/LTR、reference-free QE、LLM rescoring、acoustic-grounded、
multi-verifier/abstention、BoN/overoptimization、跨模态 verifier-guided selection 为骨架；
I1–I4 各配 novelty delta 与 kill condition。survey 结果允许直接杀死候选身份，
不以已投入工程为理由保留。
