---
title: "Owner GO and execution contract: audio-aware evidence acquisition"
record_id: "AAEA-OWNER-GO-EXECUTION-CONTRACT-2026-08-03"
date: "2026-08-03"
status: "HISTORICAL_ISSUANCE__EFFECTIVE_IDENTITY_AND_SCOPE_SUPERSEDED_2026-08-04"
issued_by: "research owner (in-session dated directive, 2026-08-03)"
semantic_research_object: "audio-aware evidence acquisition"
source_candidate_provenance: "R2 (system-first-stage1c-v2)"
authorization: "OWNER_GO_AND_EXECUTION_CONTRACT"
entry_contract: "docs/superpowers/specs/2026-08-02-audio-aware-evidence-acquisition-stage2a-entry.md"
formal_opening: "wiki/audit/system-first-stage1c-v2/round-22/2026-08-02-audio-aware-evidence-acquisition-formal-opening-permission-note.md"
default_values_policy: "ADOPTED_AS_PROPOSED_DEFAULT__AMENDABLE_BY_DATED_AMENDMENT"
---

# Owner GO 与执行合同：audio-aware evidence acquisition

> 历史签发件：本件证明 2026-08-03 的 owner GO 与原始预算授权。当前研究名称、speech-only
> 域边界、远端/本地路径、包名和实验命名空间已由
> `2026-08-04-owner-speech-domain-scope-and-identity-contract.md` 自包含取代；下文旧名称与路径保留为
> 当时事实，不得作为当前路由。

## 决定

Owner 于 2026-08-03 签发 `OWNER_GO_AND_EXECUTION_CONTRACT`：批准语义研究对象
**audio-aware evidence acquisition** 进入工程，创建独立仓
`https://github.com/chaosxingxc-orion/audio-aware-evidence-acquisition.git`（private），checkout 至
`studies/audio-aware-evidence-acquisition/`，并按 Stage-2A 入场合同的 E0→R0→R1→X 序列执行。
同批指示：数据采集线按目录重整决议调整（收据路径语义化、canonical lock 收束）。

Owner 签发时未逐字段指定冻结值；下表中标记 `DEFAULT` 的值按 Fable5 裁决书建议值生效，owner
可随时以带日期的 amendment 改任何一行。本合同不裁决创新性；创新与最终方法仍是 Stage-2A/2B 的
产出。

## 冻结字段（freeze sheet）

| 字段 | 冻结值 | 来源 |
|---|---|---|
| Repository | `https://github.com/chaosxingxc-orion/audio-aware-evidence-acquisition.git`，default branch `master`，本地 `studies/audio-aware-evidence-acquisition/` | owner GO |
| Core/runtime | lock 键 `qwen3-omni-30b-a3b-instruct-gguf`（Q8_0 GGUF + bf16 mmproj，2 files，34,691,959,904 B），llama.cpp llama-server 常驻 `-ngl 28`；**首次模型调用前必须落 E0 runtime 收据：llama.cpp build commit + 逐文件 sha256**（fail-closed） | DEFAULT |
| Carriers | lock 键 `earnings21-original`、`earnings22-original`（rev `c05ab6fd8b4b627d123c922a22a39e993dd37635`）、`conec`（rev `88440713d8b80dc4f19b225f6480237e78c379de`）；D0 收据 `docs/checks/audio-aware-evidence-acquisition/2026-08-02-acquisition/`；discovery/confirmatory 双 split 按 v20 载体族合同，派生种子 `20260803`，派生脚本入 study 仓版本控制，confirmatory 在最小确认路径触发前不读 | DEFAULT |
| Information boundary | 按入场合同不可变边界：gold/参考转写/测试标注/未来轮不越运行时边界；各臂可见字段在 R0 配置中显式声明并 hash | 入场合同 |
| Baselines | mandatory 缩减集冻结为 {ConEC 上下文线（首个复现目标）、RECOVER 1-Best 梯级（强制对照臂）、Siskos 实体消解线、FlexCTC/TurboBias NeMo 偏置组}；Corona 2017 / Raghuvanshi 2019 / Flemotomos 2024 / COALA 2026 于 R1 第零步作 threat/reproduction 候选评估；**exact runnable revision 在首次复现 run 前以带日期 amendment 冻结**；失败报 `INCONCLUSIVE_BASELINE_NOT_READY`，不得静默换弱对手 | DEFAULT |
| Prompts/tools | prompt hash 与冻结检索器/judge revision 逐 run 入 trace；来源/日期/query 记日志；最终答案权在冻结核 | 入场合同 |
| Metrics | 按 v20：任务/实体指标、correct-to-wrong 与 wrong-to-correct 转移、尾部与成本报告；评分栈在 E0 D3 冻结 | 入场合同 |
| Resources | R0 首切片上限：≤3,000 次冻结核调用、≤40 本地 GPU 时（RTX 5090）、≤20 h 处理音频、付费 API 支出=0（任何非零需 amendment）；切片末 go/narrow/repair/stop 备忘录为 stop-go 检查点 | DEFAULT |
| Exposure | study 仓 `docs/exposure-ledger.md` 逐触达行（读结果前登记）；exposure 声明四字段（scope/date/counts/inherited）；继承 exposure：三载体截至本日零模型触达（仅 D0 无模型采集核验） | DEFAULT |
| Wiki | 实验 ID 命名空间 `AAEA-E-<nnn>`（不含候选编号）；台账 `wiki/experiments/audio-aware-evidence-acquisition/README.md`；协议/config hash、MLflow/artifact 路由与偏差流程按 `wiki/Experiment-Assets.md` | owner GO |

## 授权范围与保留

本合同授权：study 仓创建与推送、E0（D1–D4 无模型数据闭环）、R0 工程纵向链、R1
readiness 合格 closest-prior 复现、X 方向性探索——各步受上表预算与 fail-closed 收据约束。

仍不授权：付费 API 支出、wiki 镜像发布、公开 release、创新性/优越性结论、超预算带的任何
触达。R2 等候选编号不得进入包名、MLflow 主命名空间与正式实验 ID。

## 失效与回滚

失效条件：owner 撤回或修订本合同；STOP_THE_LINE 触发器命中（同任务同边界更强可跑
mandatory prior、载体许可/可得性/标签/度量合同失效、未登记 inherited exposure 或泄漏、
问题可研究性被推翻）。回滚：study 仓归档（registry lifecycle 转 `paused`/`sunset`），
伞仓治理层与 W1–W4 不受影响。

## Amendment 1（2026-08-03）：W1–W4 退役后的回滚语义澄清

依据重整后架构复核提案（`PROGRAM-DIRECTORY-POST-MIGRATION-REVIEW-V1`）登记；性质为澄清性
amendment，不产生新授权，原文不作原地改写。

上节"伞仓治理层与 W1–W4 不受影响"签发于同日 W1–W4 退役裁决之前。澄清：四个 W1–W4 工作仓已于
2026-08-03 退役——本地 checkout 已删除，远端作为脱离程序的 cold backup 保留
（`wiki/archive/program/w1-w4-retirement/`）。因此本合同的回滚只影响 study 仓生命周期状态与
伞仓 registry/治理层；回滚不会恢复任何 W1–W4 本地 worktree，也不改变已退役 cold backup 的状态。
