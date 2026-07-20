---
title: "Research Objective & Current State"
role: "HOT single current-state entry; supersede in place"
last_refresh: "2026-07-20 — verified Stage-1A technical baseline"
---

# Research Objective & Current State

> 默认加载顺序：客户端指南 → 本页 → `wiki/Project-Thesis.md`。完整记录规约见
> `wiki/AI-Collaboration.md`；历史只经 cold index 定向取证。

## 1. 当前门与权限边界

当前是 **Stage-1A**。修复包已在技术基线 `2225c48` 完成四项稳定本地门：zero-network
integration gate、`wiki-sync` dry-run、final adversarial review 与 verification before completion。
因此本包可提交正式独立 Stage-1A doctoral re-review；这只是技术修复状态，**不构成 Stage-1B**
执行批准，也不是 formal verdict、reviewer signature、owner approval 或 readiness verdict。
Stage-1B systematic mapping 仍未开始且未经授权；不得运行 discovery query、研究模型（含 smoke）、
数据集实验或方向性 prototype。

## 2. 目的链

北极星是研究围绕冻结黑盒 omni foundation model 的**外部 reward-guided 控制平面**，以供给、
状态/记忆、工具、候选生成、评估、选择、预算与停止来激活预训练知识，同时不改变核心权重与内部
架构。先确认问题和证据边界，再执行 systematic mapping；所以 Stage-1A 必须让协议自包含、证据
可回放、信息边界可审计，且不得用工程自测代替研究门裁决。

## 3. 已验证的技术基线

已提交并注册的 round-12 更正撤回了 v10 对 E1–E5 完全关闭及 readiness/signature 的过度表述。
Plan-A schema-v3 已修复 E6–E12 与 anchor 合同：row、signal、edge 的必要字段显式绑定编码值与证据；
`p1`、`p1 the`、高频 anchor、越界页和合法重签后的关键变异均按合同 fail closed。精确机器正典是
`docs/checks/system-first-stage1a/evidence-v6/identity-taxonomy-v6-test.json`（verdict `PASS`，summary
`14/14 PASS`，input snapshot
`8bcfefd4504bd65efa146b5772ab351f239cdeb803892bcd5fa64374ca78f61d`）；Windows/WSL occupancy
相等，protocol-v2 与冻结 65-query bytes 等价。

在 `2225c48` 上重新验证：Windows 与 WSL current-package gate 均为 `PASS`；audit registry 为
78 artifacts / 0 failures；AI context surface 为 0 failures；尝试台账与冻结 query 相对基线无差异；
原生 `wiki-sync` dry-run 成功，远端前后保持 `91734b6` 且临时树不存在。current/AI manifest、campaign
index、audit immutability 与 archive safety 已纳入整包门。final adversarial review 和 verification
before completion 也已完成。以上仅证明技术修复包可提交正式独立复审，不产生研究裁决或执行权限。

## 4. 剩余阻塞

1. 正式独立 Stage-1A doctoral re-review 尚未给出 verdict；
2. independent reviewer sign-off 尚不存在；
3. 即使正式复审放行，仍需 owner 明确给出 Stage-1B execution approval。

任一项未闭合都维持 Stage-1A；自动检查通过不能代签。

## 5. Exposure 记账

本次 repair scope 内：**discovery queries = 0；model/smoke runs = 0**，也没有 dataset experiment、
prototype 或 Stage-1B mapping execution。此零值不覆盖历史；`INHERITED_PRIOR_EXPOSURE` 仍为非零
并保持原账，后续 manifest 必须继续排除已暴露对象。任何无范围“0 次”说法无效。

## 6. 当前路由

- Survey 当前入口：`wiki/survey/current/README.md`；有效协议、状态、表和机器资产由其与 current
  manifest 定向加载。
- Campaign cold audit index：`wiki/audit/system-first-stage1a/INDEX.md`。round-12 correction 是唯一
  active review transaction；更早 round 仅经 index 定向取证。
- 已归档和 path-pinned legacy 都是 cold evidence，不进入默认加载面。

## 7. 下一授权动作

**下一授权动作**仅是把当前技术修复包提交正式独立 Stage-1A doctoral re-review，等待 reviewer
verdict/signature；若复审放行，再等待 owner 的显式 Stage-1B execution approval。在两项治理裁决
完成前，Stage-1B 保持未开始、未经授权。

## 8. 失效条件

下列任一事件触发本页立即 supersede-in-place 并回到相应门：v6 报告/hash/跨平台 equality 失配；
protocol-v2 偏离冻结 query bytes；current/AI manifest、整包门或 audit immutability gate 失败；
exposure 计数变化；独立复审发现新 blocker；reviewer/owner 给出新裁决；研究对象、信息边界或冻结
派生定义被正式改变。旧叙述只在 audit/archive 保留，不向本页叠加补丁。
