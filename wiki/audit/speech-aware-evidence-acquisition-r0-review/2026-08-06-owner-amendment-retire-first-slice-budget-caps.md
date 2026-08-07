---
title: "Owner amendment: retire the first-slice numeric budget caps"
record_id: "SAEA-OWNER-AMENDMENT-2026-08-06-BUDGET-CAPS"
date: "2026-08-06"
issued_by: "research owner (in-session directive, 2026-08-06)"
amends: "2026-08-04-owner-consolidated-execution-contract.md §6 (Resources row)"
status: "SIGNED_BY_OWNER"
model_touch_performed: false
---

# Owner amendment：废止首切片数值预算帽

## 1. 处置

Owner 于 2026-08-06 明确签署：**废止合并执行合同 §6 Resources 行中的三个数值上限**
（≤3,000 次冻结核调用、≤40 GPU-hours、≤20 小时 speech audio）。这些数值自本件生效之日起
不再是机器强制条件，也不再作为 gate 的拒绝理由。

理由（owner 表述）：本 study 处于 Stage‑2 探索期，数值帽在设计与计划讨论中反复占用注意力，
与其带来的实际保护不成比例。

## 2. 保留不变的部分（不在本次废止范围内）

本 amendment **只废止数值上限**。以下机制**继续有效并继续机器强制**：

- **付费 API = 0**：合同 §6 该项不变；
- **exposure 预登记**：每次模型/工具触达前必须在 study 仓 `docs/exposure-ledger.md` 落行，
  含 execution profile、split role、split identity hash、consumed 标记与 carrier；
- **一次性 attempt 语义**：`(run_id, attempt_id)` 不可复用；用量在发送前持久化；失败的 attempt
  其实际用量仍进入耐久记录；重试必须新 attempt；
- **逐 run 自我一致性**：`ExecutionPlan` 仍声明本次计划的调用数/音频秒数/GPU 小时，并仍与其
  exposure 行逐字段核验（登记值 ≥ 计划值），运行中不得超出**自己登记**的额度；
- **Stage‑3 停止线**：`paper-scale-confirmatory` 等 profile 仍一律 fail closed（合同 §7 不变）。

即：曝光台账仍然回答"谁在什么时候触达了什么"，只是不再有全切片的数字天花板。

## 3. 工程后果（如实记录）

2026-08-05 的独立评审将"同一 exposure 额度可重复消费"列为 P0‑4。该发现的**一次性消费部分**
仍然关闭（见 §2 attempt 语义）；其**数值上限部分**因本 amendment 而不再适用——不是回归，
而是 owner 主动收窄了合同义务。后续任何复核不应再以"首切片数值帽未强制"为缺陷。

若 owner 日后希望恢复数值预算，需要新的 dated amendment；实施方不得自行重新引入。

## 4. 实施方义务

- 从代码中移除 `FIRST_SLICE_CAPS` 及其全切片求和检查；
- 不在任何设计、计划或状态文档中再次提出预算分配议题；
- study `docs/engineering.md` 与 exposure ledger 说明文字同步更正，不得残留"帽已强制"的表述；
- 台账的 calls / speech audio seconds / gpu hours 三列**保留为记录**（有用的事实），
  但不再承担强制语义。

## 5. 失效条件

Owner 以新的 dated 记录恢复或修改预算义务时，本件就地被取代。
