---
title: "Research Objective & Current State"
role: "HOT single current-state entry; supersede in place"
last_refresh: "2026-07-19 — Stage-1A repair and context consolidation"
---

# Research Objective & Current State

> 默认加载顺序：客户端指南 → 本页 → `wiki/Project-Thesis.md`。完整记录规约见
> `wiki/AI-Collaboration.md`；历史只经 cold index 定向取证。

## 1. 当前门与权限边界

当前仍是 **Stage-1A survey-ready gate 修复期**。本批只修复证据合同、有效协议与 AI context；
**不构成 Stage-1B 执行批准**，也不代表 reviewer signature、owner approval 或 readiness verdict。
Stage-1B systematic mapping 尚未获准开始；不得运行 discovery query、研究模型（含 smoke）、数据集
实验或方向性 prototype。

## 2. 目的链

北极星：研究一个围绕冻结黑盒 omni foundation model 的**外部 reward-guided 控制平面**，通过
供给、状态/记忆、工具、候选生成、评估、选择、预算与停止来激活预训练知识，同时不改变核心权重
与内部架构。为了先确认问题与证据边界，再执行 systematic mapping，所以当前必须先让 Stage-1A
协议自包含、证据可回放、信息边界可审计；未经签署不以工程自测替代研究门裁决。

## 3. 本批已证实的修复结果

Plan-A schema-v3 已完成 E6–E12 与 anchor 合同修复：row 16 字段、每个 signal 的 4 字段、每条
edge 的 2 字段均显式绑定编码值与证据；`p1`、`p1 the`、高频 anchor 和越界页 fail closed；通用
第 12 行不依赖既有 ID；合法重签后的 source/use/right/selection/missing-binding 变异均由指定合同
拒绝。Windows 与 WSL 独立报告的 occupancy 相等，冻结派生语义未变。

精确机器正典：
`docs/checks/system-first-stage1a/evidence-v6/identity-taxonomy-v6-test.json`（verdict `PASS`，
summary `14/14 PASS`，input snapshot
`8bcfefd4504bd65efa146b5772ab351f239cdeb803892bcd5fa64374ca78f61d`）。平台报告在同一
`evidence-v6/` release 目录；只以报告字段和 manifest hash 为准，不从本页复制 occupancy 数字。
这是技术检查结果，不是签署或就绪声明。

## 4. 剩余阻塞

1. 独立复审必须核对本批修复、protocol-v2 等价性、context manifest 与归档结果，并给出正式结论；
2. reviewer sign-off 尚不存在；
3. reviewer 放行后仍需 owner 明确给出 Stage-1B execution approval。

任一项未闭合都维持 Stage-1A。自动检查通过不能代签。

## 5. Exposure 记账

本次 repair scope 内：**discovery queries = 0；model/smoke runs = 0**。也没有 dataset experiment、
prototype 或 Stage-1B mapping execution。此零值只描述本次修复，不覆盖历史；
`INHERITED_PRIOR_EXPOSURE` 仍为非零并保持原账，后续 manifest 必须继续排除已暴露对象。任何无范围
“0 次”说法无效。

## 6. 当前路由

- Survey 当前入口：`wiki/survey/current/README.md`；有效协议、短状态、表和机器资产只从该 router
  与 `wiki/survey/current/manifest.json` 定向加载。
- Campaign cold audit index：`wiki/audit/system-first-stage1a/INDEX.md`。Task-8 的完整 index +
  correction 对尚未发布时，AI context manifest 必须保持 `active_review_transaction: null`；不得提前
  创建 stub。激活后 current 层只链接 campaign index，不枚举 round/amendment 物理路径。
- 已归档与 path-pinned legacy 都是 cold evidence，不进入默认加载面。

## 7. 下一授权动作

**下一授权动作**仅是：完成 context consolidation，随后把一份 bounded correction 直接写入永久
AUDIT 路径并登记，运行无网络 integrated gate，再提交独立复审。等待 reviewer 与 owner 的显式
裁决；在此之前不执行 Stage-1B。

## 8. 失效条件

以下任一事件触发本页立即 supersede-in-place 并回到相应门：v6 报告/hash/跨平台 equality 失配；
protocol-v2 编译结果偏离冻结 65-query bytes；current/AI manifest 或 audit immutability gate 失败；
exposure 计数变化；独立复审发现新 blocker；reviewer/owner 给出新的阶段裁决；研究对象、信息边界
或冻结派生定义被正式改变。旧叙述只在 audit/archive 中保留，不向本页叠加补丁。
