---
proposal_id: "R6"
title: "实例内 reward-guided context 与轨迹控制"
dimension: "D5 agentic-system evolution"
status: "workbench proposal; owner review pending; Stage-2A vertical-slice component"
execution_authority: "WITHHELD"
---

# R6 — 实例内 reward-guided context 与轨迹控制

## Proposal 摘要

本研究让 reward 在单个实例内决定下一动作 `keep / branch-context / acquire / tool / repair / stop`，而不是
只在终局候选池中 rerank。状态由 R5 的 evidence state 承载，动作来自 R1-R4，reward 只用 API 可见信号。
核心问题是：step-wise reward-guided control 是否在同等 action menu 与成本下超过 fixed/greedy trajectory、
majority/MBR 和 terminal-only rerank。

Training-free RL 在这里指外部序贯控制，不指更新 core。若 reward 只做终局选择，R6 退化为 selector，
不满足该方向的主张。

## 1. 研究问题与假设

- `H1 action value`：runtime signals 对至少一个非终局 action 的净 advantage 有可用排序能力。
- `H2 sequential value`：step-wise controller 超过 terminal-only rerank 和 best fixed trajectory。
- `H3 conservative improvement`：incumbent + margin gate 在不把 coverage 降空的情况下减少错误传播。
- `H4 bounded efficiency`：controller 能把额外预算分配到更可能受益的实例，而不是退化为 always-expensive 或
  always-cheap。

## 2. 证据位置

| 证据 | 已有机制 | 与 R6 的边界 |
|---|---|---|
| `SPEECH_NEAREST_PRIOR` Omni-RRM (2602.00846) | frozen generator 上的 audio-capable BoN selection | select-only、fixed N；reward 不改变下一类动作 |
| `SPEECH_NEAREST_PRIOR` TTS ASR self-verification (2606.18323) | reference-aware BoN 与 per-input difficulty proxy | selector 与 metric 耦合，difficulty 被算出后未用于预算 |
| `SPEECH_NEAREST_PRIOR` AudioProcessBench (2606.09925) | reference-free process critic 与 consensus/critic 对比 | majority 常胜，critic 只应做边际仲裁；不是 action controller |
| `SPEECH_NEAREST_PRIOR` AudioGenie/Agentic ASR 等 | 多轮 repair/stop surface | 多为 hand-coded、gold-conditioned 或固定 horizon |
| `CROSS_DOMAIN_METHOD_DONOR` JitRL、ETS、ATLAS | action reweighting、partial resampling、stop/allocate；BoN 是退化特例 | text/vision 效果不外推；部分路径依赖 logprob，不能照搬 |
| `CROSS_DOMAIN_METHOD_DONOR` Training-Free GRPO、PRA、SeqMC、GUI critics | 无梯度语义 advantage、过程 steering、外部每步 critic | 只借 update/对照结构；重写为 API-visible speech state |

## 3. Control formulation

### 3.1 State/action

采用共享 `evidence_state`，加入 `r_hat_t`、action history、condition key、hard budget 与 incumbent。第一版
action menu 仅：keep、structured re-prompt、same-observation resample、one observation branch、one bounded
repair、stop；后续才加入 retrieval/memory/skill。

### 3.2 Reward 与 advantage

```text
r_hat(s_t, a_t) = w_fmt r_fmt + w_cons r_consensus
                  + w_sem r_semantic + w_evd r_corroboration
                  + w_judge r_pairwise - λ cost(a_t) - κ risk(a_t)

A_hat_t = r_hat(after a_t) - r_hat(incumbent at t)
```

权重与阈值只可在隔离 calibration split 上冻结。Counts-only consensus 是默认主信号；frozen heterogeneous
judge 只处理共识打平或 margin 足够大的边际案例。禁止用 test answer、gold CoT、hidden state/logprob。

### 3.3 Policy

第一阶段不用复杂学习器：有限动作枚举 + conservative one-step lookahead + hard horizon。只有动作 ranking
与 sequential value 都成立，才比较 contextual bandit、retrieval-based value 或无梯度 preference update。
Policy 每步可保留 incumbent；替换需满足 R8 的 condition-specific margin gate。

## 4. 实验设计

### 4.1 Stage-2A carrier

与 R5 共用 frozen Qwen2.5-Omni-7B serving lane、MMAU Test-mini + MMAR。所有版本/hash/decoding/budget
在授权前仍为 TBD。Short horizon 设为 2–4 类 action、每实例有限调用，具体 cap 需用能力摸高后冻结。

### 4.2 Arms

`direct`、`structured`、`random action`、`greedy fixed`、`best fixed trajectory`、`full fixed chain`、
`majority/semantic MBR`、`terminal-only rerank`、`step-wise reward controller`、`offline oracle policy`。
所有自适应臂执行相同 action menu；oracle 只解释 recoverability。

### 4.3 Outcomes 与分析

Primary：对 direct 和 best fixed/terminal-only 的 task utility paired delta/LCB。机制分析：每种 action right
的净贡献、state occupancy、stop round、budget utilization、advantage-vs-true-delta fidelity、oracle recovery、
correct→wrong、error propagation、condition-wise regret 与成本前沿。

### 4.4 必须消融

- consensus-only、judge-only、combined；
- terminal-only vs step-wise，保持候选/动作总量一致；
- fixed threshold vs condition-aware threshold；
- incumbent gate 开/关；
- fixed horizon vs adaptive stop；
- repair feedback 提供 content vs 只提供 error type；
- action order permutation。

## 5. Lean 与数学建议

Lean 证明有限预算终止、incumbent preservation、gold boundary 和 `2ε` margin 条件。现有 `Iterate` 只有在
每步真实增益及有界等假设下成立，不能证明实际 controller 单调/收敛。

数学上把问题视为有限 horizon、constrained API-MDP，但不要求学习 core policy：

```text
max_pi E[U(y_T)]
s.t. E[Cost] <= B, P(U(y_T) < U(y0)-δ) <= α
```

先报告相对 best fixed trajectory 的 empirical policy value。若 reward error 随 action/condition 异方差，
用 `ε(c,a)` 替代全局 ε；替换规则变为 margin 超过两候选误差界之和。任何 regret/monotonicity 结论都
必须列出 coverage、stationarity 和 reward fidelity 假设。

## 6. 击杀与重路由

- step-wise 不超过 terminal-only 或 best fixed：R6 降级为静态 selection component。
- reward 与 true delta 排序接近随机，或 judge swap 后反转：禁止 reward 掌舵，回退固定/consensus policy。
- controller 退化为统一 action：承认 best fixed 足够，不保留“自适应”命名。
- gain 仅来自更多调用：在 matched-cost 后不成立即击杀。
- repair 持续伤害 target preservation：删除 repair action，而非用其错误拖累全部 R6。

## 7. 路线与预期贡献

先关闭 `{keep, one branch, one repair, stop}`；再接 R1/R4；只有 instance-level policy 有正值后才进入 R7。
预期贡献是 API-only speech control MDP、step-wise-vs-terminal 的严格比较、runtime reward admissibility 证据，
以及在成立时的 training-free sequential controller。

## 8. Provenance

语音 selector/evaluator 事实来自 D5；动作 surface 来自 D1-D4；文本/视觉算法只作 D6 donor。JitRL/ETS
等效果不作为 speech 预期效果量。
