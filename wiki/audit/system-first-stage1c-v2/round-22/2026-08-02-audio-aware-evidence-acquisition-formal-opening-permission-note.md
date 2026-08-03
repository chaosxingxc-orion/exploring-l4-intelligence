---
title: "音频感知证据获取：正式开题许可说明"
artifact_id: "SF-STAGE1C-R2-FORMAL-OPENING-NOTE-R22"
date: "2026-08-02"
campaign: "system-first-stage1c-v2"
round: 22
addressed_to: "Fable5 and the research owner"
source_candidate_provenance: "R2"
semantic_research_object: "audio-aware evidence acquisition"
source_proposal: "wiki/survey/workbench/stage1c-portfolio/proposals/2026-07-29-r2-coreview-draft.md"
source_proposal_artifact_id: "SF-STAGE1C-R2-COREVIEW-V20"
source_proposal_git_blob: "cfbc0616ca25359f07a85c7c56099862bba1bd8f"
companion_review: "wiki/audit/system-first-stage1c-v2/round-22/2026-08-02-r2-v20-stage-aligned-multiround-doctoral-supervisor-review.md"
decision: "FORMAL_OPENING_APPROVED"
decision_scope: "STAGE1C_PROBLEM_SELECTION_AND_STAGE2A_HANDOFF_ONLY"
novelty_scope: "NOT_ADJUDICATED"
method_convergence_scope: "NOT_ADJUDICATED"
stage2a_authorization: "WITHHELD_PENDING_OWNER_GO_AND_EXECUTION_CONTRACT"
human_signature_claimed: false
---

# 音频感知证据获取：正式开题许可说明

## 给 Fable5 的决定

基于 R2 v20 的问题定义、研究现状、直接近邻矩阵、可证伪研究问题、资源上界、失败出口，
以及 round-21 十项签字门的逐项复核，**同意以语义研究对象 `audio-aware evidence acquisition`
正式开题**。R2 仅作为其 Stage-1C 来源与审计编号保留，不进入未来工程仓名称。

本许可确认三件事：

1. 冻结 speech/omni 核上的音频感知证据获取是一个边界清楚、值得实验投入的独立研究问题；
2. 当前文献覆盖足以支持选题，并足以冻结 Stage-2A 的 closest/strongest-prior 复现队列与探索约束；
3. v20 提出的 OBS、ORG/SUPPLY、USE/CONTROL 三支柱及 RQ0–RQ4b 是待实验裁决的探索空间，
   具备可实现性、可证伪性和负结果价值。

## 本许可没有提前裁决什么

本说明**不裁决技术创新性，不冻结最终方法学，也不把三支柱写成已经成立的贡献**。这些结论必须在
Stage-2A 先复现最接近且最强 prior 后，通过方向性原型逐步收敛；冻结后的方案再进入 Stage-2B
正式验证。Stage-2 证据可以合并、拆分、降级或日落任一支柱，而不构成对本次开题许可的追溯性失败。

本说明也不是 owner 的实验执行授权。它不授权创建远程 GitHub 仓、调用模型/API、运行 smoke、
生成任务指标、复现实验、做方向性原型、push 或发布 Wiki 镜像。任何一次模型触达——即使只跑一个
样本——都属于 Stage-2A exposure，必须等待独立的 `OWNER_GO_AND_EXECUTION_CONTRACT`。

## Stage-2A 交接条件

在请求执行授权前，执行合同至少冻结：

- 语义仓名与远程仓 URL、umbrella experiment-index 路径和责任边界；
- 精确模型/runtime revision、服务参数、prompt 与可见信息边界；
- 数据 revision、split、license/redistribution 边界、D1–D4 完整性结果；
- mandatory baseline 的 exact revision、readiness 判据与失败后 `INCONCLUSIVE` 路径；
- 指标、探索/确认隔离、调用与 GPU 量级、停止条件和 exposure 记账方式；
- 首轮 reproduction 的最小可执行纵向切片，以及进入方向性原型的证据门。

截至本说明签发时，Earnings21、Earnings22 与 ConEC 的 D0 本地物化已经完成；D1–D4
仍是无模型的数据闭环工作。它们可以继续，但不能被描述成实验结果。

## 文献截止与停止扫描规则

正式开题采用 `2026-08-02` literature cut。此后不再用常规新增论文让开题反复回滚；新增工作进入
Stage-2A delta ledger 和 prior/threat queue。只有以下发现触发 `STOP_THE_LINE`：

- 在相同任务、信息边界和公开载体上存在更强且可运行的 mandatory prior；
- 主载体的许可、可得性、标签或度量合同失效；
- 出现尚未登记、会改变验证结论的 inherited exposure 或数据泄漏；
- 新证据推翻问题的可研究性或核心因果解释，而不只是增加一个邻近工作。

本轮新增确认的 Corona 2017、Raghuvanshi 2019、Flemotomos 2024 和 COALA 2026 属第一类
Stage-2A prior-reduction 输入，但不推翻问题本身，因此不要求 v20 再升级或重开 Stage-1C。

## 许可结论

`FORMAL_OPENING_APPROVED` 立即生效；`STAGE2A_EXECUTION_WITHHELD` 继续生效。下一项正式交易
应是 owner 审阅并签发 Stage-2A execution contract，而不是继续进行无上限的开放式论文扫描。
