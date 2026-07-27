---
proposal_id: "R5"
title: "Incumbent-preserving 的证据状态智能体架构"
dimension: "D4 multimodal agentic system"
status: "workbench proposal; owner review pending; Stage-2A vertical-slice component"
execution_authority: "WITHHELD"
---

# R5 — Incumbent-preserving 的证据状态智能体架构

## Proposal 摘要

本研究构建一个围绕冻结 speech/omni API 的最小可审计 agent architecture。系统以一等
`evidence_state` 保存原音、派生 observation、工具输出、矛盾、成本和 provenance；direct answer 是
incumbent。Planner 只能提议动作，工具只能产生 evidence，最终答案由同一 frozen omni core 在原音与被
接纳 evidence 上生成，controller 在 `{incumbent, revised}` 间拥有显式选择权。

研究目标是验证：在相同 core、供给和预算下，清晰的 evidence contract 与作答权分配能否超过 strong
structured prompt 和 fixed wrapper，同时降低 wrapper-induced regression。R5 是 R1-R4 的承载架构，
也是 R6/R8 的第一 Stage-2A 组件。

## 1. 研究问题与假设

- `H1 architecture`：显式 evidence state + 原音重锚 + incumbent choice 超过把中间文本直接喂给回答器的
  fixed text-bottleneck wrapper。
- `H2 arbitration`：reward-arbitrated `{direct, revised}` 在 matched supply 下超过 hand arbitration 与
  always-revise，并显著降低 correct→wrong。
- `H3 decision rights`：planner/executor/answerer 的权利分离使错误可定位到 supply、skill、reward 或
  orchestration，而不是只能报告黑盒系统总分。
- `H4 minimality`：若 structured prompt 已达到同样效用，复杂架构不成立；不能以审计性或功能更多替代
  capability 结果。

## 2. 语音系统近邻与开放台阶

| 证据 | 可用事实 | 本 proposal 的差异 |
|---|---|---|
| `SPEECH_NEAREST_PRIOR` Audio-Mind (2605.28480) | auditable evidence-state 取向、GIVE UP 名义动作；文本瓶颈可伤害原音判断 | 部分大桶低于 direct，abstain 几乎不触发；缺显式 incumbent gate |
| `SPEECH_NEAREST_PRIOR` Agent-Omni (2511.02834) | 多 agent/工具编排可执行 | 在部分 benchmark 低于 direct；需要同核同预算重测 |
| `SPEECH_NEAREST_PRIOR` Omni-DeepSearch (2605.08762) | 多轮搜索、证据与停止失败轨迹 | 过度搜索会丢失已找到的正确证据 |
| `SPEECH_NEAREST_PRIOR` AudioToolAgent / AudioGenie-Reasoner | 多轮 audio tool/reasoning loop | 固定轮数/上限、成本高，决策权与归因不清 |
| `SPEECH_NEAREST_PRIOR` TalTech/VISA ARC systems | 复杂 speech evidence fusion，证明强固定系统是必打基线 | wrapper 数字受 component/core/prompt 影响，且缺 compute-normalized 自跑基线 |
| `CROSS_DOMAIN_METHOD_DONOR` WebThinker | planner/explorer 与返回摘要的取证合同 | 文本搜索效果不外推；只借角色和 trace 结构 |

## 3. 架构与信息流

### 3.1 Evidence state

```text
evidence_state = {
  instance_id,
  original_audio_anchor,
  task_instruction,
  incumbent_answer,
  derived_observations[],
  evidence_items[{content, source, span, verifier, status, provenance}],
  contradictions[],
  candidate_answers[],
  reward_records[],
  accepted_answer,
  budget_ledger,
  action_trace
}
```

Evidence item 状态只允许 `proposed / verified / contradicted / admitted / rejected`；不能通过自由文本隐式
覆盖。格式/parse validity 与内容效用分开记录。

### 3.2 角色与权利

- `frozen core`：产生 direct/revised answer；最终答案必须经过它对原音的重新 grounding。
- `planner`：从有限 action menu 提议动作；无权直接作答。
- `executor`：执行 deterministic tool、API 或 observation transform；无权接纳结果。
- `evidence verifier`：检查 schema、provenance、矛盾和可选 pairwise utility；无权访问 test gold。
- `controller`：选择 keep/execute/accept/reject/stop，以及最终保留 incumbent 或 revised。

同一个基础模型可在不同 API 调用中扮演多个角色，但必须在 trace 中分开；主分析另设 cross-family judge
以检测 self-evaluation contamination。

### 3.3 Stage-2A 最小动作集

第一版严格限制为：`keep incumbent`、structured re-prompt、same-observation resample、一个
cross-observation branch、一次 bounded repair、stop。暂不接 live retrieval、persistent memory、动态工具
生成或 full-duplex，避免一开始不可归因。

## 4. 实验设计

### 4.1 Carrier 与 core

建议冻结 Qwen2.5-Omni-7B API serving lane，载体 MMAU Test-mini + MMAR；exact model/service revision、
hash、prompt/decoding 和数据资产状态为 `TBD_AT_AUTHORIZATION`。若该 core 无稳定 API serving，可换为
同合同的 frozen core，但不得跨 core 混用 baseline。

### 4.2 Arms

`direct`、`strong structured prompt`、`fixed wrapper`、`full fixed chain`、`hand-arbitrated evidence state`、
`reward-arbitrated evidence state`、`offline oracle over {incumbent,revised}`。另设 random matched-cost 与
majority/MBR，确保系统收益不只是多调用。

### 4.3 Primary result

任务 accuracy/utility 对 direct 和 strongest fixed baseline 的 paired delta、95% CI 和 LCB；并按
control-plane depth、task/acoustic bucket 报 correct→wrong、wrong→correct、worst-group、seed variance、
calls/latency/cost。必须单列 `incumbent wins / revised wins / controller correct / controller wrong` 四格。

### 4.4 归因消融

- 去掉 raw-audio final re-grounding；
- direct candidate 不可恢复；
- evidence schema 改成自由文本 scratchpad；
- planner 与 final answerer 合并；
- hand vs reward arbitration；
- format reward 与 semantic reward 分离；
- 同供给 fixed wrapper vs adaptive action rights。

## 5. Lean 与数学建议

Lean state machine 需要覆盖：类型正确 transition、原音锚点不可被覆盖、candidate set 永含 incumbent、预算
严格下降、gold path 不可进入 state、provenance 随 evidence merge 保留。Executable trace 要逐例映射到 Lean
constructor；桥接前只称 formal model。

数学上把架构价值拆成：

```text
system gain = candidate-distribution gain + arbitration gain - orchestration harm
```

通过 `fixed wrapper` 控制候选分布、`oracle over candidates` 测 recoverability、`reward vs oracle choice`
测 arbitration，避免把三者压成一个总分。若 oracle 有 headroom 而 controller 无收益，失败在 reward；若
oracle 也无 headroom，失败在 action/supply；若 direct 被 wrapper 删除，则是架构 harm。

## 6. 风险、击杀与重路由

- reward-arbitrated system 在 matched supply 下不超过 structured prompt/best fixed：击杀动态架构主张。
- 收益完全由更强 component/core 解释：不能归因给 orchestration，须锁同组件重测。
- text bottleneck 造成原音信息丢失且 re-grounding 无法恢复：限制角色或让 omni core 直接持有更多决策权。
- controller 的 improvement 以不可接受 correct→wrong 或成本换取：交给 R8 门控；仍不满足则不升级。
- trace/schema 过重但无 capability/attribution 价值：保留最小 ledger，删除非承重功能。

## 7. 路线与预期贡献

R5 首先交付一个可运行但极小的 evidence-state vertical slice；只有超过强基线后才接 R1/R4，再接 R3/R2。
预期贡献是 frozen speech API 的 decision-right contract、incumbent-preserving 系统基线，以及候选生成、
仲裁和编排伤害的可归因分解。

## 8. Provenance

事实来自 D4 dossier 和 T1/T2/T3；D1-D3 仅提供未来组件接口；WebThinker 只作跨域角色合同 donor。
架构有效性仍需 Stage-2 实验。
