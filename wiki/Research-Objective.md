---
title: "Research Objective & Current State — 日常加载的唯一现状入口（热层）"
role: "认知层：现状/研究对象/约束/open items/取代索引的单一极简入口。派生自 Decision-Log（审计层），可重建，非唯一记录。被取代的条目掉出本文件（在 archive/ 与 Decision-Log 里）。"
maintained: "每有取代关系变化即更新本文件；新决策先 append 进 Decision-Log 再反映到此。"
last_refreshed_commit: "填最新提交（本文件更新时）"
---

# Research Objective & Current State

> **给读者/agent 的一句话**：默认只读本文件 + `CLAUDE.md`。要某条决策的出处才去 grep
> `Decision-Log.md`（冷档案，勿整篇读）。术语见 CLAUDE.md 术语表。

## 现在在做什么（Stage-1A · 问题界定）

- **阶段**：Stage-1A（广泛 survey / 候选问题 / 原型空间纸面设计 / 风险审查）。**Stage-1B 未放行、M2 冻结**。
- **研究对象（续34 锁定）**：**一个 label-free、供给条件的选择算子,在冻结 omni〔模型 × 任务〕矩阵上的
  兑现面（ρ(c)/H(c)/regret）**。ASR 是其中一行,非全部;**广度（跨 ASR/ST/SER/SLU/spoken-QA/
  audio-understanding × 跨冻结模型）= 护城河**。
- **伪统一守卫**：共享对象 = 算子 + H(c) 记账法统一;各任务各留效用 U 与 SESOI;度量同一算子在每格的 ρ(c)。
- **候选身份（Stage-1C 才选,现不选）**：I1 一般 selector（机制近死）/ I2 音频接地（ASR 格被 READ+MILS 占）/
  I3 约束·弃权·Goodhart（对象 OPEN、守卫不新）/ **I4 跨矩阵兑现面（broad 死、narrow 待验、survey 高优先）**。

## 现在绑定的约束（硬）

- weight-frozen（不改权重/结构）;**信息边界**：test-item gold 不入 selector/reward/prompt/检索/候选构造。
- 证据全 directional-only / hypothesis-grade——**无任何确证宣称**;有头空的 null 才证伪 selector（headroom 归因纪律）。
- **append-only**（改写历史=reviewer 升级触发）;**哈希正典=git blob 字节**;发布前对未提交工作树跑敌意自检、零确认才提交。

## Open items（live）

1. **Survey v2**（reviewer P0-SURV-2）：taxonomy 重构（+候选池构造 / +上下文供给 / +selective-prediction 三新族;
   selection≠revision 拆开）、**每族跨任务矩阵扫**、"击杀器是否跨任务迁移"设一等轴。
2. **诚信核查 C1/C4**（Stage-1B 放行前置）：C1 尝试普查（registry vs raw run）、C4 负结果普查。
3. **I1–I4 direct-killer 矩阵** + I4 供给收益/selector 收益分解图 + 预算公平性设计。
4. **对 reviewer 的 response**（ACCEPT_WITH_ONE_REASONED_MODIFICATION,含 ASR-scope 反制）——待写。
5. **冷热归档执行**（git mv 存量进 archive/,作独立验证操作）——待执行。

## 取代索引（什么已死 / 被谁取代 —— 见旧条目勿当现状）

| 旧结论/命名 | 现状 | 出处 |
|---|---|---|
| RDU 为 headline | 降为 secondary/ablation | 续32 |
| `A-SEL` 命名 | 正名「选择器兑现率方向」 | 术语表 / 续33 |
| v4.2 = Stage-2 入口 | Stage-1 问题定义交付物 | 续32 |
| `84c6cf6` proposal 草稿 | PRE_STAGE2_BLUEPRINT（无现时效力） | 续33 |
| 程序代号 `W1-ASEL-S2-001` | 冻结弃用 | 续33 |
| 自家 +0.517（检索供给佐证） | 撤引（C-T7 泄漏 INVALID;干净值 −0.066 null） | 续33·勘误 |
| I4 "最干净 whitespace" | broad 死 / narrow 待验（跨矩阵兑现面） | 续34 |
| scope 收窄到 ASR | 反制:ASR 是一行,研究对象是跨矩阵兑现面 | 续34 |
| 全 append-only 大文件当主工作面 | 冷热分离,默认只读本热层 | 续34 |

## 正典工件指针

- 现状真理：**本文件**。审计真理：`Decision-Log.md`（冷,勿整篇读）、`Per-Work-Status.md`。
- 发布快照：`docs/integrity/release_manifest.json`（git-blob 哈希）+ `docs/checks/manifest-blob-verification-2026-07-13.txt`。
- survey：`wiki/survey/2026-07-13-scout-ledger-round1.json`（8族/57条/46独立,SCOUT 级）。
- 规则/术语：`CLAUDE.md` / `AGENTS.md`（镜像）。
