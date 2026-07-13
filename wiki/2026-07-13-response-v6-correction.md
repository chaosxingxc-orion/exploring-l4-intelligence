---
title: "Response v6 更正件（append-only）— provenance 三元组与 13 项机读修复"
date: 2026-07-13
corrects: "wiki/2026-07-13-response-v6-to-signoff-adversarial-review.md（原文不改动，错误保持可见）"
mandated_by: "重校准审查 W1-ASEL-STAGE1-RECALIBRATED-ADR-2026-07-13 §10 T+0 / S1-M4；中间审查 R6-M1/R6-M2/R6-M3"
validated: "入库前经 PyYAML 实测解析：response_items 恰 13 项、finding_id 唯一、每项恰含 finding_id/disposition/status_before/status_after/evidence/gate 六字段"
author: "协调者本人（owner 指令：不委托）"
---

# Response v6 更正件

## 1. 三处缺陷与更正（协调者本人造成，如实自认）

1. **R6-M1**：v6 frontmatter 的 `reviewed_snapshot_responded_to` 写的是**被审对象**（整改报告
   `c7528fe` 快照），不是被回复的审查文档本身。正确对象见 §2 `responds_to`。
   **哈希正典补注（§5 自检勘误②）**：此前各方（含外审与本文件首版）流通的 `cd987ff0…` 是该快照
   **CRLF 工作树副本的变体哈希**；正典值（git blob 字节，`git show c7528fe:wiki/2026-07-13-remediation-report-v42-for-reviewer-signoff.md | sha256sum`）
   = `6c6adba2daf537b67174b68eec31b6db34ba3755b5779eda6cb735896bf28418`，换算关系
   （LF→CRLF 逐行变换后哈希 = `cd987ff0…`）已逐字节验证。
2. **R6-M2**：v6 的 `this_response_snapshot: umbrella 7b895b5` 是**证据快照**（信中描述的仓库
   状态），不是回复工件自身的提交——v6 于 `3116898` 才进入 Git，一份文档不可能记录包含它自己
   的未来提交。两个概念现拆分为 `evidence_snapshot` 与 `artifact_snapshot` 两栏。
3. **R6-M3**：v6 的两个 YAML 块在同一文档内重复顶层键 `response_item:`（7+6 个），标准 YAML
   解析每块只保留最后一项，13 项机读记录实际只存活 2 项（F-S7、M-S6）。本文件以**列表**形式
   重发全部 13 项，且入库前跑过实际解析验证。

**根因与纪律**：机读块写完未做一次解析自检；"证据快照"与"工件快照"两个概念未拆分。两条都已
写入协调者长期工作纪律：凡发布机读块，先 parse 后入库；快照字段一律双栏。

## 2. 正确的 provenance 三元组（S1-M4 规定格式）

```yaml
response_artifact:
  responds_to:
    path: wiki/2026-07-13-v42-remediation-signoff-doctoral-adversarial-review.md
    sha256: 64389f7fee45ea2aad4c9880fffe9293b621e52c492b79eca28d206290f761cf
    committed_at: c16900c
  evidence_snapshot:
    umbrella_commit: 7b895b5
    w1_commit: a532da0
  artifact_snapshot:
    path: wiki/2026-07-13-response-v6-to-signoff-adversarial-review.md
    sha256: beddc2609ddbddfb8943048df6301e024f58f2dc8f666109efc5ae5dc5117146
    umbrella_commit: 311689818e6650674fac2cc1c19dbe4ee94baa29
```

## 3. 13 项机读处置（v6 实质立场的忠实重发，无内容变更）

以下只修**载体格式**，不改 v6 的任何实质裁定（13/13 ACCEPT、零抗辩、不申请立即重签）。

```yaml
response_items:
  - finding_id: F-S1
    disposition: ACCEPT
    status_before: WRONG_GATE
    status_after: OPEN
    evidence: "Decision-Log 续32：设计身份类门位由 M3 改挂 fresh-Stage-2-proposal 冻结点 @c16900c"
    gate: BEFORE_STAGE2_UNFREEZE
  - finding_id: F-S2
    disposition: ACCEPT
    status_before: OPEN
    status_after: CLOSED
    evidence: "release manifest 自 clean HEAD 重建并单独提交 @7b895b5；祖先与 7/7 工件哈希复核通过"
    gate: before_any_signoff_or_release
  - finding_id: F-S3
    disposition: ACCEPT
    status_before: OPEN
    status_after: CLOSED
    evidence: "checker 对最终 proposal 重跑并提交（输入 sha 3f0ac5b6… 三处一致）@c16900c；叙事版移出证据集"
    gate: before_any_signoff_or_release
  - finding_id: F-S4
    disposition: ACCEPT
    status_before: PARTIAL
    status_after: PARTIAL
    evidence: "标签改判 SELF-PIN VERIFIED / UPSTREAM ANCHOR OPEN @c16900c；自锁来源已如实点名"
    gate: upstream_anchor_before_eligibility_or_build_PASS
  - finding_id: F-S5
    disposition: ACCEPT
    status_before: WRONG_GATE
    status_after: OPEN
    evidence: "item-ID 级排除缺陷复核确认；整组排除+负例测试契约冻结入整改报告 @c16900c"
    gate: before_any_real_split_draw
  - finding_id: F-S6
    disposition: ACCEPT
    status_before: OPEN
    status_after: CLOSED_AS_RECORD
    evidence: "'送达即满足独立快照'推论删除、§6.3 商榷撤回 @c16900c；实质独立审计保持 OPEN 未被冒充"
    gate: independent_readonly_audit_still_open
  - finding_id: F-S7
    disposition: ACCEPT
    status_before: OPEN
    status_after: OPEN
    evidence: "p0_gate_status 如实 NOT_PASS；续32 明记 M2 冻结直至前置门闭合"
    gate: before_any_data_sensitive_continuation
  - finding_id: M-S1
    disposition: ACCEPT
    status_before: OPEN
    status_after: CLOSED
    evidence: "owner 续32④：public-deterministic 路线 + 如实等级帽（development/controlled-benchmark）"
    gate: decided_before_fresh_stage2_proposal
  - finding_id: M-S2
    disposition: ACCEPT
    status_before: PARTIAL
    status_after: OPEN
    evidence: "诚实命名已修（前轮）；外部锚档案未交付，登记为冻结门交付物"
    gate: BEFORE_STAGE2_UNFREEZE
  - finding_id: M-S3
    disposition: ACCEPT
    status_before: OPEN
    status_after: OPEN
    evidence: "相对 estimand 为主、绝对 margin 降为补充的设计承诺登记 @c16900c"
    gate: BEFORE_STAGE2_UNFREEZE
  - finding_id: M-S4
    disposition: ACCEPT
    status_before: WRONG_GATE
    status_after: OPEN
    evidence: "生成方差/comparator 原则先冻、标定只在独立 calibration split 的承诺登记 @c16900c"
    gate: BEFORE_STAGE2_UNFREEZE
  - finding_id: M-S5
    disposition: ACCEPT
    status_before: PLAUSIBLE_STAGE_INCOMPLETE_CONTRACT
    status_after: OPEN
    evidence: "四臂去相关对照族与预冻阈值的契约登记 @c16900c"
    gate: BEFORE_STAGE2_UNFREEZE
  - finding_id: M-S6
    disposition: ACCEPT
    status_before: PLAUSIBLE_STAGE_INCOMPLETE_CONTRACT
    status_after: OPEN
    evidence: "小簇推断模拟契约（DGP 网格/Type-I 上限/独立种子）登记 @c16900c"
    gate: BEFORE_STAGE2_UNFREEZE
```

## 4. 阶段重校准注（**非 v6 内容的忠实重发部分**——这是 v6 之后的门位再解释，单列于此）

（2026-07-13，owner Stage-1A/B/C 细分 + 重校准审查 `deferred_to_stage2` 清单）：§3 表中各
`BEFORE_STAGE2_UNFREEZE` 门的解释现统一为——相应数值/协议在**未来 fresh Stage-2 proposal 冻结时**
落定；而该 proposal 本身以 **Stage-1C 的 owner 收官选题**为前置，Stage-1 期间不做其中任何确证机械
的施工。当前位置：**Stage-1A**。（首版曾把本注置于 §3"忠实重发"节内，与该节"无内容变更"的自述
矛盾——自检勘误③，现单列。）

## 5. 2026-07-13 自检勘误（append-only；自检工作流 wf_45c1f5fe 坐实，协调者裁定后修复）

1. **本文件首版自身失真**：M-S5/M-S6 的 `status_before` 曾被写成 `INCOMPLETE_CONTRACT`，丢失了
   v6 与签署审查原文的 `PLAUSIBLE_STAGE_` 限定（恰是外审认可门位阶段合理性的语义记号）——已在
   §3 恢复为 `PLAUSIBLE_STAGE_INCOMPLETE_CONTRACT`。"忠实重发"的首版自己就不忠实，如实记录。
2. **EOL 哈希缺陷类（系统性）**：`cd987ff0…` 及 release manifest @`7b895b5` 的 3/7 登记册哈希
   （`7d1a33…`/`7ea5ef…`/`58766320…`）均为 **CRLF 工作树变体**，不能从 clean clone 复现（正典
   blob 值分别为 `6c6adba2…` 与 `d48e30ad…`/`f05e0efb…`/`c3774be6…`）。处置：哈希正典约定入
   CLAUDE.md/AGENTS.md 术语表；两仓全部 CRLF 工作树副本已归一为 LF；`build_release_manifest.py`
   改为对 **git blob 字节**取哈希；manifest 按事务顺序重建。**F-S2 的 status_after 由 CLOSED
   暂改 PARTIAL**，以正典哈希重建的 manifest wrapper commit（含 7/7 blob 哈希核验输出）为重新
   闭合的证据。§3 表保持 v6 当时立场的忠实记录不动，现时状态以本节为准。
3. 阶段重校准注移出 §3（见 §4 说明）。
