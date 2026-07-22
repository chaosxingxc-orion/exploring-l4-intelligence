---
title: "Research Objective & Current State"
role: "HOT single current-state entry; supersede in place"
last_refresh: "2026-07-22 — Stage-1B v3 speech-prior repair frozen; transition re-review pending"
---

# Research Objective & Current State

> 默认加载：客户端指南 → 本页 → `wiki/Project-Thesis.md`；历史只经 cold index 定向取证。

## 1. 当前门与权限

当前是 **Stage-1B late execution and closeout**。Stage-1A search design 已签字，owner 已授权
Stage-1B survey 执行。冻结 D0、date-bounded delta、T1 route disposition、non-H5 method-path
mapping 与 Stage-1C eligible-input synthesis 已完成。针对评委指出的典型语音论文遗漏，现有
本地/冻结证据池已完成有界身份审计与严格补充；v3 科学 release 已冻结在 commit
`626914a963637354642116b938eb9ab745a099c8`，尚待独立 reviewer 对该固定 commit 复审。

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
- Delta 65/65 已处置：193 个唯一 work，12 篇进入 PDF+e-print+D2，重复种子为 0。T1
  50/50 有 disposition；2,633 个 title-only identity 及 232 个集合外 backward arXiv ID
  继续作为显式遗漏面，不能支持 zero-hit、`NO_DIRECT_MATCH` 或文献宇宙闭合声明。
- 当前 map 明确分开五个分母：226-work portfolio、legacy 8-work/11-path strict occupancy、
  81-work speech/omni identity audit、32-row speech/omni strict supplement 与 12 篇 delta D2。
  81 个命名身份已全部唯一落位：23 direct、19 instrument、27 boundary、11 trained/model
  exclusion、1 H5-held；32 行严格表含全部 23 个直接方法、8 个承重测量工具与 1 个边界。
  语音补充的 23 个直接路径均有 load-bearing speech/audio 与 API-only 外部控制，但其决策核心
  可为 audio-native、omni-native、text coordinator 或 cascade，不能混写为同一核心模态。
- Stage-1C 输入保持未排序：budget/stop/repair、evaluator reliability、interactive/full-duplex
  三类为 `ELIGIBLE_NON_H5`；evidence-state 与 tool/agent arbitration 因 H5 依赖暂为
  `INELIGIBLE_FOR_STAGE_1C_SELECTION`。
- 本轮 research model/smoke、dataset metric、reproduction、prototype 均为 0。既有 ASR/omni
  复现材料已降级为 `PROVISIONAL_INPUT / NOT_STAGE_FROZEN`。

## 4. 当前路由

- CURRENT：`wiki/survey/current/README.md` → `status.md`。
- Stage-1B map：`wiki/survey/current/tables/stage1b-mapping-release.md`。
- Stage-1C 未排序输入：`wiki/survey/current/tables/stage1c-eligible-inputs.md`。
- 语音/omni 完整性：`wiki/survey/current/data/stage1b-speech-omni-prior-coverage-v1.json`；
  严格补充：`wiki/survey/current/data/stage1b-speech-direct-prior-supplement-v1.json`；
  自包含引用：`wiki/survey/current/stage1b-transition-reference-appendix.md`。
- frozen-D0 收口：`wiki/survey/workbench/system-first-stage1b/2026-07-22-frozen-d0-exhaustion-closeout.md`。
- 长期记录：`wiki/survey/registry/README.md`；PDF/e-print/提取文本仍在 `SPEECHRL_DATA_DIR`。
- v3 checks：`docs/checks/stage1b-closeout/2026-07-22-v3/`。

## 5. 下一动作

只请求一次针对 release commit `626914a963637354642116b938eb9ab745a099c8` 的独立
Stage-1C transition re-review。v3 的 45 项 manifest 输入（37 Git + 8 external）已重放；新增
检查保证 81 个命名语音/omni 身份无静默遗漏、23 个直接方法全部进入严格表、32 个承重引用
均有本地全文哈希与页码锚点。v3 取代 `51b527b`，修复的是科学证据覆盖与 release 自洽性，
不改变 H5 `WITHHOLD`，也不提前讨论创新性。
reviewer `SIGN` 前不正式启动 Stage-1C；即使签字，模型/复现仍留待后续执行门。

## 6. 失效条件

union/receipt/selection 漂移、review `DISAGREE`、source/lock bytes 或 exposure 改变、新 blocker
或 owner/reviewer 新裁决，均触发本页 supersede-in-place。旧叙述只留 audit/archive，不叠加
amendment 到热层。
