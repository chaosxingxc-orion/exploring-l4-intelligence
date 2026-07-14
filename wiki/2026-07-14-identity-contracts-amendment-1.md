---
amendment_id: CONTRACTS-AMEND-2026-07-14-01
title: 身份合同修正案 1 —— δ_corr 拆名、UMBRELLA 算子范围、C1/C4 与探针授权拆签（owner 重签件）
date: 2026-07-14
amends: "wiki/2026-07-14-identity-contracts-v1.md（FROZEN @ dce5c79，blob 1338f6b16f540902…）"
mandated_by: "第三轮博导复审（收档 a06a498）§6.3 / §9.2 / §9.7——REOPENED_PARTIAL_DELTA_CORR"
status: DRAFT_FOR_OWNER_RESIGN — 复审明示：此类修改改变 kill-if，必须走合同 amendment + owner 重签，不得记作执行层小参数
posthoc_log_entry: "本修正案整体作为合同 §8 日志第 2 行登记（构念修复，非新增限定词；novelty 判定不变）"
generated_by: "Claude Fable 5 主会话（依复审 §6.3 拆名方案起草）"
signoff: { owner: PENDING, date: null }
---

# 身份合同修正案 1

## A. δ_corr 拆名（修复构念替换——复审 §6.3，接受为真错误）

**问题**：同一符号 δ_corr 承载了三套语义——理论文档的「可达误差去相关」（越小越收敛向 oracle）、
v4.2 整改的「实测误差相关/条件互信息」、合同/探针把它操作化为「选择重合 >90%」。**选择相同 ≠
误差相关**：两个 scorer 可以 100% 同选且都对，也可以 100% 同选且都错——重合率无法判断独立价值。

**拆名（自本修正案起强制）**：

```text
selection_overlap    = P(argmax S_same == argmax S_external)          —— 仅描述量，禁止触发任何判据
error_corr           = Corr(1[sel_same 错], 1[sel_external 错])        —— 在有头空的 item 上计算
conditional_error_mi = I(E_same; E_external | item/headroom/difficulty) —— 小样只作描述
complementary_gain   = U(best router/combiner) − max(U_same, U_external)
residual_error_corr  = 理论文档 TH2a 的 δ_corr 本体（越小越好，收敛量）——今后引用理论时用此全名
```

**strict-I2 kill-if 重写**（取代合同 §3 原「δ_corr 测得≈0 → kill」分支）：

> 在有 oracle 头空的 item 上，同核与外部 selector **高度同错（error_corr 高）且 complementary_gain≈0**
> → kill 方向（同核信号无独立正确性增量）。必须同时报告：双方各自 rho/regret、A错B对与 B错A对的
> 条件计数、selection_overlap（仅描述）。selection_overlap 单独出现不得触发 kill。

shuffle-audio 对照维持（合同 §2/§3 正测试），但按复审 §9.2-C 增配 matched controls（正确音频/
错位音频/静音/同说话人硬负例；报告 score delta、rank correlation、winner margin、最终 U，不只
winner flip）——具体实现进 Gate-C 探针协议 v2。

## B. UMBRELLA 与 same-selector contract 的算子范围（修复 §6.3 第二缺口）

原合同 §7 适用范围注称「UMBRELLA 的环内每一步选择动作仍受本表约束」——但 UMBRELLA 定义只说
advantage→next action，并未定义每步固定 K action pool。**修正**：

> same-selector contract 只覆盖**池内选择算子**（I1 / bare-I2 / strict-I2 / I3 / I4）。UMBRELLA 的
> 环含生成/扩池/工具阶段，**不在本表覆盖内**；其动作选择对象（action proposal pool 的几何与预算）
> 是独立算子对象，留待 Stage-1C dossier 单独冻结（等预算 loop vs one-shot 判别即复审 Proposal E）。
> 不得以「仍受约束」一句把不同算子并成同一对象。

## C. C1/C4 终验与探针授权拆签（修复 §9.7 循环前置）

原探针协议把「C1/C4 census 终验」并入探针签批同一动作，且 frontmatter 先写 prerequisites_met——
循环状态。**修正**：拆为两个独立 exact-hash 签字块，可同人异栏，先后有序：

```yaml
integrity_gate:            # 先签
  scope: "确认 C1 永久缺口登记（config-selection 轨迹）+ 接受 C4 台账（29 行）"
  artifacts: "docs/integrity/2026-07-14-c1-attempt-census-draft.md @ blob a3999861…, c4 @ 4ae58ae3…"
  owner: PENDING
probe_authorization_gate:  # 后签（Gate C 完成、探针协议 v2 + frozen run manifest 就绪后）
  scope: "对精确冻结的 run manifest（item IDs/seeds/温度/c1/模型 hash/代码 commit）授权开机"
  artifacts: "待 Gate C 产出"
  owner: PENDING
```

探针协议 v1 的 prerequisites_met 行相应作废（由本修正案 supersede；协议 v2 于 Gate C 重写）。

## D. 合同 §8 post-hoc 日志追加行（随本修正案生效）

| 日期 | 身份 | 变更 | 触发 | novelty 判定是否改变 | 登记人 |
|---|---|---|---|---|---|
| 2026-07-14 | strict-I2 / 全体 | 修正案 1：δ_corr 拆名、kill-if 重写、UMBRELLA 范围修正、拆签 | 第三轮复审 §6.3/§9.2/§9.7（构念修复） | 否 | 协调者起草，owner 重签 |

## E. Owner 重签

```text
重签语义：批准 A（δ_corr 拆名 + strict-I2 kill-if 重写）、B（UMBRELLA 算子范围）、C（拆签结构）
并将 D 行登记入合同 §8。integrity_gate 可同时签（其对象 C1/C4 工件哈希已列）；
probe_authorization_gate 留待 Gate C。
重签不构成：对任何探针结果或科学裁决的预先背书。
owner: ____________   date: ____________
```
