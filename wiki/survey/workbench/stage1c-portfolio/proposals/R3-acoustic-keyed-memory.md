---
proposal_id: "R3"
title: "声学条件键控的持久多模态记忆"
dimension: "D2 multimodal memory"
status: "workbench proposal; owner review pending"
execution_authority: "WITHHELD"
---

# R3 — 声学条件键控的持久多模态记忆

## Proposal 摘要

本研究构建不改模型权重的外部经验库，但不只按文本语义检索。Memory key 由 `task intent × acoustic
condition` 组成；value 保存 evidence、action、outcome、reward、反例、适用范围与 provenance。研究要回答：
对未来实例有用的经验能否在语义相似但声学机制不同的条件下被正确读取，同时避免负迁移、自投毒和
无限增长。

当前已读语音面中的直接跨实例 memory 证据薄，因此该 proposal 明确属于“语音问题 + 跨域方法 donor”
组合。M2Note、MemRL 等结果不能承载 speech 有效性，只提供 schema、门控和评价协议。

## 1. 研究问题与假设

- `H1 key relevance`：声学 key 比 semantic-only/task-only key 更能预测某条经验对当前实例的贡献符号。
- `H2 future utility`：合法 write/read gate 使未来实例的 prequential utility 随经验增加而提高，而非只在
  retrospective replay 上变好。
- `H3 lifecycle`：provenance、反例、衰减和驱逐可把负迁移控制在预注册 tolerance 内，同时保持正收益。
- `H4 transfer scope`：跨 task/core 的经验只有通过 qualification gate 才可迁移；若条件键无判别力，
  proposal 降级为 task-only memory。

## 2. 证据与迁移边界

| 证据 | 可借部分 | 不可外推部分 |
|---|---|---|
| `SPEECH_NEAREST_PRIOR` AOP-Agent (2605.28192) | episode 内分层 evidence memory、检索工具与反思停止；暴露幻觉传播 | 没有跨实例写门，不能证明持久记忆有益 |
| `SPEECH_NEAREST_PRIOR` audio uncertainty study (2604.25591) | 不同 core/任务的共识与置信信号可用于 gate | 信号跨 core 翻转，不能用全局阈值 |
| `CROSS_DOMAIN_METHOD_DONOR` M2Note (2607.00685, vision) | mistake notebook、效用写门、迁移退化现象 | gold/judge 门及视觉效果不迁移；无 acoustic key |
| `CROSS_DOMAIN_METHOD_DONOR` MemRL (2601.03192, text) | Intent-Experience-Utility schema、utility-gated read、Q/遗忘仪表 | 写门与声学条件未占据 |
| `CROSS_DOMAIN_METHOD_DONOR` PhysMem、MemCollab | 状态键控、跨模型 provenance 标签 | 物理/文本状态不是连续声学条件 |
| `CROSS_DOMAIN_METHOD_DONOR` MementoGUI/PANDO 等 | 写入、遗忘、驱逐和长期 agent 协议 | GUI task success 不证明 speech transfer |

## 3. Memory schema 与生命周期

### 3.1 Key

```text
key = {
  task_family, intent_embedding,
  snr_bin, reverb_bin, duration_bin,
  speaker_count/change, overlap_proxy,
  language/code_switch, codec/channel_proxy,
  core_service_revision
}
```

声学特征全部由外部可见 waveform 工具或 API 输出计算；不得读取 core hidden state。Key 不必一次固定，
但每个版本必须 pin 特征算法与阈值。

### 3.2 Value

```text
entry = {
  evidence_summary, action_contract, pre_answer, post_answer,
  estimated_advantage, observed_eval_outcome,
  positive_and_negative_examples, applicability,
  source_instance, timestamp, provenance, contradiction_count,
  read_count, contribution_history, decay_state
}
```

测试 gold 只允许写入隔离评测日志，永不写入可被后续测试实例读取的 memory。若在部署流中没有 ground
truth，write gate 只能使用多次观测共识、独立验证、执行 postcondition 和稳定 reward margin。

### 3.3 Lifecycle

`candidate write → quarantine → corroborate → admit → gated read → contribution attribution → decay/evict`。
Memory read 只提供 evidence/action suggestion，不能直接覆盖 incumbent；最终决定仍由 R5/R6 controller。
同一条目被反驳、跨 condition 负贡献或 provenance 不完整时进入隔离或驱逐。

## 4. 实验设计

### 4.1 Data protocol

在 MMAU/MMAR/MMSU/SAKURA 中建立 time-ordered stream，并按 clean/noise/reverb/language/duration 等
声学 strata 划分 early calibration、online stream、held-out future strata。可控扰动只用于机制识别；必须
另有真实声学条件 holdout。相同题目或语义近重复不得跨时间泄漏。

### 4.2 Arms

`no memory`、`random memory`、`semantic-only`、`task-keyed`、`acoustic-only`、`task×acoustic`、
`task×acoustic + lifecycle`、`offline oracle memory`。所有 memory 臂共享相同基础 controller 和 read cap。

### 4.3 Outcomes

Primary：未来实例的 prequential average utility 与 final-window utility。Secondary：learning curve、
negative-transfer rate、每次 read 的 contribution、key precision/recall、write acceptance、contradiction、
forgetting、库规模、检索/存储成本、跨 condition/core transfer 以及 correct→wrong。

### 4.4 关键消融

- acoustic key 替换为随机 bin；
- 去掉 core revision、反例、provenance、decay/evict；
- global gate vs per-core/per-condition gate；
- session-only vs cross-instance；
- 只存成功经验 vs 同时存失败/abstain entry；
- retrospective shuffled split，用作泄漏敏感性对照而非主结果。

## 5. Lean 与数学建议

Lean 义务包括有限容量、合法写/读/驱逐、provenance preservation、测试 gold 不可读以及 eviction 后状态
一致性。经验提升不能由 schema 定理推出。

数学上把 read value 写成条件优势：

```text
A(m, c) = E[U(after read m) - U(no read) | condition c]
```

先检验 `A` 的符号是否随 acoustic condition 显著变化；只有变化成立，acoustic key 才有研究价值。对
stream 评估用 prequential estimator，不允许挑 retrospective best checkpoint。若近似 stationarity 不成立，
引入 discount/change-point 作为外部统计更新，并将 regret 定理限定在显式分段平稳假设。

## 6. 风险与击杀条件

- acoustic feature 不能比随机/task-only key 更好地区分贡献符号：击杀 acoustic-key 主张。
- 平均未来贡献非正或负迁移超 tolerance：关闭跨实例 write，仅保留 session evidence state。
- write gate 依赖 gold 或同一 judge-family 自评：视为信息边界失败，不升级。
- memory 增益来自题目重复/泄漏：结果作废并重切 time-order/semantic clusters。
- 库增长快于效用且 decay/evict 无法稳定：降级为固定容量 per-condition cache。
- core/service revision 改变即大面积反转：memory 必须按 revision 隔离，不能宣称跨核迁移。

## 7. 路线与预期贡献

先证明 `task×acoustic` key 能预测 read contribution，再开放 write；先 session 内，再跨实例；先固定容量，
再研究演化。预期贡献是 acoustic-conditioned memory benchmark/schema、合法 write/read gate 的实证比较，
以及正负迁移的 prequential 证据。若 H1 不成立，仍可产出“何时不应声学键控”的负结论。

## 8. Provenance

语音证据来自 D2 dossier；跨域 memory 设计来自 D6；JitRL/MemRL 仅作为方法 donor。所有跨实例 speech
效应均为待验证假设，H5 未签署。
