---
title: "Research Objective & Current State"
role: "HOT single current-state entry; supersede in place"
last_refresh: "2026-07-22 — Stage-1B mapping synthesis ready for release freeze"
---

# Research Objective & Current State

> 默认加载：客户端指南 → 本页 → `wiki/Project-Thesis.md`；历史只经 cold index 定向取证。

## 1. 当前门与权限

当前是 **Stage-1B late execution and closeout**。Stage-1A search design 已签字，owner 已授权
Stage-1B survey 执行。冻结 D0、date-bounded delta、T1 route disposition、non-H5 method-path
mapping 与 Stage-1C eligible-input synthesis 已完成；尚待把当前字节冻结成 commit/manifest-bound
release，并由独立 reviewer 对固定 commit 作阶段转换签字。

允许检索记录闭合、去重、citation traversal、non-H5 编码、D2 全文映射与 release 检查。
研究模型加载/smoke、数据集 metric/headroom、复现、prototype、候选问题排序与 owner 选题均未
获本阶段授权。H5 在独立 coder B、agreement 与第三方裁决前不得进入承重统计或选题。

## 2. 目的链

北极星是冻结黑盒 omni foundation model 的外部 reward-guided control plane：控制候选、工具、
评估、选择、路由、预算与停止，不修改核心权重。Stage-1B 只映射方法路径、接近度、反证与
可测性，不判创新；Stage-1C 从未排序的合格 gap hypotheses 中选题；Stage-2A 先复现最近 prior
再收敛技术方案，Stage-2B 验证。

## 3. 当前证据

- 冻结 D0 为 20,727 个唯一 arXiv ID，20,727/20,727 有摘要处置；319 篇达到全文深度，
  226 篇保留（12 core、43 instrument、45 transfer、126 negative），93 drop。该闭合只对
  frozen D0 成立，不是全领域零遗漏声明。
- 65/65 条 date-bounded delta 查询均已处置，活动失败为 0；得到 193 个唯一 work，人工
  REC-0 后 12 篇进入 PDF+e-print+D2，181 篇只从本轮承重 map 排除，重复种子为 0。
- 50/50 条 T1 route 均有 disposition：28 executed、3 not held、19 `WAIVED_UNAVAILABLE`。
  已执行 route 共扫描 71,254 个标题，宽词表命中 3,310；677 可与已知 work 合并，2,633
  仍是 title-only identity，不能被写成 zero hit 或用于 `NO_DIRECT_MATCH`。
- 12/12 个 frozen registry core work 已从本地 e-print 执行后向 arXiv-ID 子集闭合，得到
  266 个唯一引用 ID；其中 232 个位于 D0/delta/registry 外。DOI/title-only edge 未解析；
  前向公共索引返回 HTTP 429，12 项显式豁免，故不作全引文或文献宇宙闭合声明。
- 当前 map 明确分开三个分母：226-work portfolio、8-work/11-path strict occupancy、12 篇
  delta supplement。strict set 中 9 路径承重、2 路径为 boundary，11/11 均 API-only，
  speech-native strict path 为 0（未测，不是空文献结论）。
- Stage-1C 输入保持未排序：budget/stop/repair、evaluator reliability、interactive/full-duplex
  三类为 `ELIGIBLE_NON_H5`；evidence-state 与 tool/agent arbitration 因 H5 依赖暂为
  `INELIGIBLE_FOR_STAGE_1C_SELECTION`。
- 本轮 research model/smoke、dataset metric、reproduction、prototype 均为 0。既有 ASR/omni
  复现材料已降级为 `PROVISIONAL_INPUT / NOT_STAGE_FROZEN`。

## 4. 当前路由

- CURRENT：`wiki/survey/current/README.md` → `status.md`。
- Stage-1B map：`wiki/survey/current/tables/stage1b-mapping-release.md`。
- Stage-1C 未排序输入：`wiki/survey/current/tables/stage1c-eligible-inputs.md`。
- frozen-D0 收口：`wiki/survey/workbench/system-first-stage1b/2026-07-22-frozen-d0-exhaustion-closeout.md`。
- 长期记录：`wiki/survey/registry/README.md`；PDF/e-print/提取文本仍在 `SPEECHRL_DATA_DIR`。
- 本轮 checks：`docs/checks/stage1b-closeout/2026-07-22/`。

## 5. 下一动作

生成 Stage-1B release manifest，绑定 protocol、D0/delta/T1、226 roster、strict coding、D2
sidecars、mapping tables、eligible inputs、H5 与 unresolved counts；运行可重放检查并冻结 commit。
随后只请求一次针对该固定 commit 的独立 Stage-1C transition review。reviewer `SIGN` 前不正式
启动 Stage-1C；即使签字，模型/复现仍留待后续执行门。

## 6. 失效条件

union/receipt/selection 漂移、review `DISAGREE`、source/lock bytes 或 exposure 改变、新 blocker
或 owner/reviewer 新裁决，均触发本页 supersede-in-place。旧叙述只留 audit/archive，不叠加
amendment 到热层。
