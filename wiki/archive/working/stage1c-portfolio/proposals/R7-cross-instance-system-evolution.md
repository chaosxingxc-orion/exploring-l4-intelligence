---
proposal_id: "R7"
title: "跨实例经验驱动的无权重系统进化"
dimension: "D5 agentic-system evolution"
status: "workbench proposal; owner review pending"
execution_authority: "WITHHELD"
---

# R7 — 跨实例经验驱动的无权重系统进化

## Proposal 摘要

本研究考察模型参数完全冻结时，外部系统能否通过经验记忆、condition statistics 与 action-level advantage，
让未来实例的控制决策逐步改善。每个实例产生 `(condition, state, action, evidence, outcome, advantage)`；
R3 决定如何存取，R4 管理技能，R7 只拥有 external policy statistics、threshold 和 preference 的更新权。

在当前已读语音面中，直接跨实例 reward-guided evolution 证据不足；JitRL、MemRL、bandit/agent memory
工作只能作为方法 donor。因此本 proposal 的第一价值是建立严格、无泄漏的 speech prequential protocol，
而不是预设 learning curve 必然上升。

## 1. 研究问题与假设

- `H1 online improvement`：在 time-ordered future instances 上，external update policy 的 average/final utility
  超过 frozen controller 和 recency heuristic。
- `H2 condition transfer`：experience 的收益主要发生在匹配 task×acoustic condition；跨 condition 迁移需
  qualification gate，否则会负迁移。
- `H3 action credit`：按 action-level advantage 更新比只记最终成功/失败更能改进未来 action choice。
- `H4 no-retrospective illusion`：收益必须出现在在线 prequential curve，而非 retrospective best checkpoint、
  重放或未来标签泄漏。

## 2. 证据与边界

| 证据 | 可借机制 | 不可继承的结论 |
|---|---|---|
| `SPEECH_NEAREST_PRIOR` current audio agent corpus | 大量系统对实例无状态，工具有用性统计被丢弃；说明可测接口存在 | “未使用”不等于“使用后有效” |
| `SPEECH_NEAREST_PRIOR` AOP-Agent/session memory | episode 内 evidence accumulation | 不证明跨实例更新 |
| `CROSS_DOMAIN_METHOD_DONOR` JitRL (2601.18510) | 检索经验、value/advantage、跨任务 retrieval | 文本 state abstraction 与理论/实现差异需重建；效果不迁移 |
| `CROSS_DOMAIN_METHOD_DONOR` MemRL | Intent-Experience-Utility schema、utility-gated read、forgetting 曲线 | 无 acoustic key，写门不充分 |
| `CROSS_DOMAIN_METHOD_DONOR` Training-Free GRPO / PRA | 用外部经验语义优势改变未来动作 | 只借无梯度 update 结构 |
| `CROSS_DOMAIN_METHOD_DONOR` online skill/memory agents | prequential、retire、drift 协议 | GUI/text success 不能承载 speech claim |

## 3. Evolution mechanism

### 3.1 Experience record

沿用 R3 schema，但 R7 只读取已通过 gate 的统计摘要：condition、action、estimated advantage、independent
verification、cost、contradiction 和 timestamp。Core prompt/weights 不被训练；任何可学习对象都是外部表、
阈值、检索权重或有限 action preference。

### 3.2 Update families

按复杂度分三层比较：

1. `count/recency`：每 condition-action 的成功/失败与指数衰减；
2. `bandit-style`：对 bounded proxy reward 的 conservative UCB/Thompson 或 lower-confidence selection；
3. `advantage memory`：检索相似经验，聚合 action-level advantage 并更新 action ranking。

不在第一阶段训练新的 neural policy。若未来引入外部轻量模型，它必须是独立非 core 组件，并需另行判断
是否仍属于本期“training-free control”；当前 proposal 不授权。

### 3.3 Feedback lanes

- Primary `deployment-visible lane`：update 只看 runtime proxy、tool result 和用户/环境自然返回的反馈；
  benchmark gold 只在隔离 evaluator 中计算曲线。
- Secondary `legitimate delayed-feedback lane`：仅在任务真实会在完成后暴露 outcome 时使用；反馈属于过去
  instance，且不得与未来 test split 交叉。该 lane 与 primary 分开报告。

## 4. 实验设计

### 4.1 Stream construction

从 MMAU/MMAR/MMSU/SAKURA 构建按语义 cluster 和 acoustic strata 去重的 time-ordered stream；设
calibration prefix、online evaluation stream、held-out condition shift。重复多种合法时间顺序，报告顺序方差，
但不为结果挑最优排列。

### 4.2 Arms

`frozen R6 controller`、`random/recency`、`global counts`、`condition-keyed bandit`、`advantage memory`、
`oracle-update diagnostic`。所有臂共享 R5/R6 action menu、起始 policy、预算和 memory cap。

### 4.3 Outcomes

Primary：prequential average utility、final-window utility 和相对 frozen controller 的 LCB。Secondary：
learning slope、time-to-improvement、dynamic regret、forgetting、negative transfer、held-out condition transfer、
memory growth、read/write/update cost、action entropy、correct→wrong 与 rollback frequency。

### 4.4 关键对照

- time-order vs shuffled replay；
- proxy update vs gold-oracle update（后者只作 ceiling）；
- global vs condition-keyed；
- read-only memory vs read+policy update；
- no decay vs decay/change-point reset；
- within-core vs cross-core，后者必须通过 qualification gate。

## 5. Lean 与数学建议

形式化外部统计量有界、memory capacity、time index 单调、future label 不可读、update 只依赖过去可见
sigma-algebra，以及 rollback 不删除 incumbent。若使用 bandit regret，只在明确 bounded reward、coverage、
stationarity 或 piecewise-stationarity 假设下证明。

建议把 condition mismatch 显式建成偏差项：

```text
regret_T <= estimation_term + coverage_term + drift_term + key_mismatch_term
```

这比直接移植 JitRL 的文本状态结论更诚实。经验上同时报告 proxy-regret 与 gold-evaluated task regret，二者
分离可暴露 reward gaming。

## 6. 风险、击杀与重路由

- prequential curve 不随实例改善，或 final-window 不超过 frozen controller：击杀跨实例 evolution 主张。
- shuffled replay 有效而 time-ordered 无效：判为 retrospective artifact。
- condition shift 导致净负迁移：冻结更新或按 change point reset，只保留 session memory。
- proxy 曲线上升而 true task utility 下降：判为 reward hacking，交 R8 审计并 rollback。
- improvement 来自未来标签、重复题或 benchmark contamination：结果作废。
- memory/update 成本大于能力收益：退回 R3 read-only 或固定 prior。

## 7. 路线与预期贡献

R7 只能在 R6 的实例内 action/reward 有正 fidelity 后启动。先做 counts/recency，再 condition bandit，最后
advantage memory。预期贡献是 speech agent 的 leakage-resistant prequential protocol、condition-aware external
policy update，以及正负结果都可解释的跨实例 evolution evidence。

## 8. Provenance

语音 occupancy 事实来自 D2/D4/D5；JitRL/MemRL 等来自 D6/相关 dossier，只借方法。跨实例 speech
提升没有被先验假定。
