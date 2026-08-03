---
artifact_id: "SF-CAPABILITY-PROPOSALS-SHARED-PROTOCOL-V1"
role: "shared experimental and formal contract for R1-R9 proposals"
authority: "workbench draft; must be frozen per Stage-2 authorization"
---

# 共享实验与形式化协议

## 1. 不变量

### 1.1 API-only frozen core

承重路径只允许：构造 API 输入、读取可见输出、调用外部确定性工具或独立 API、维护外部状态、再调用
冻结 core。不得要求或暗用模型权重、梯度、hidden state、attention、保证可用的 logprob、内部 reward
head 或 decoder intervention。开放权重 core 只是一种可复现服务载体；主结论按黑盒可见量成立。

### 1.2 Capability-first

主结论必须是 task utility/accuracy 的可靠提升。Evaluator accuracy、headroom、abstention、reward
hacking、注入与 provenance 只作为测量、门禁、压力测试或失效解释；不能替代能力结果。系统可以保留
incumbent 或停止，但不得通过把 coverage 压到接近零制造表面可靠性。

### 1.3 Gold fence

运行时状态不得含 test gold、gold CoT、gold acoustic attribute、oracle tool label 或由其直接派生的量。
Gold 只允许在隔离的评测/校准路径中：计算终局任务指标、离线 oracle、reward fidelity、SESOI 与误差界。
校准集、开发集、测试集以及跨实例 memory 的时间边界必须由文件/进程级 guard 分离并留下 trace。

### 1.4 Modality boundary

视觉、GUI、文本和代码 agent 论文均标为 method/construct/protocol donor。借的是算法结构和实验合同，
不是跨模态效果量。语音输出的答案等价、连续声学条件、原音重锚和音频成本都要在本域重建。

## 2. 统一状态、动作与结果

建议所有 proposal 复用以下抽象，以便最终可组合：

```text
state s_t = {
  original_observation,
  derived_observations,
  evidence_items,
  incumbent_answer,
  candidate_answers,
  memory_reads,
  skill_results,
  reward_estimates,
  condition_key,
  budget_remaining,
  provenance,
  action_history
}

action a_t ∈ {
  keep, branch_context, acquire, retrieve_memory, invoke_skill,
  repair, revise, abstain_guard, stop
}

transition: (s_t, a_t, visible API/tool output) -> s_{t+1}
```

每次改变 observation、evidence、candidate 或 decision right 都必须在 trace 中有独立事件；不能把整个
wrapper 记成一个不可解释的“agent”臂。

## 3. 共同研究假设

- `H-capability`：外部控制平面可通过改变 context/state/action distribution，提高冻结 core 的任务效用。
- `H-adaptation`：按实例/条件选择动作优于同成本的 best fixed action/composition。
- `H-reliability`：incumbent-preserving 和 condition-aware 门可以降低 correct→wrong，而不把有效覆盖率降空。
- `H-attribution`：在同 core、同 prompt hygiene、同供给和同预算下，可把收益归因到明确的 state/action 变化。

这些是假设而非先验结论。固定候选池 oracle miss 只界定已执行池，不否定新 context、tool 或 memory
可能改变未来候选分布。

## 4. 基线阶梯

每篇 proposal 至少从下列基线中选择所有适用项，并冻结相同 core、服务 revision、prompt hygiene、
decoding 和终局 scorer：

1. direct readout；
2. strong structured prompt；
3. same-observation resampling；
4. majority / semantic MBR；
5. random matched-cost action；
6. best fixed action 或 best fixed composition；
7. full fixed chain / all-tools；
8. hand-authored router/controller；
9. terminal-only rerank；
10. adaptive proposal method；
11. offline oracle over the actually executed action/candidate pool。

Phase-1 可以先摸能力上限并完整记录成本；凡声称“自适应决策本身有效”，必须补同供给、同调用或
cost-matched 比较。跨论文绝对数不是可替代的本地 baseline。

**R1 特例。** R1 阶段 A 的研究对象就是有限菜单内的能力上界和机制，允许不同配置使用不同资源，不以
cost-matched dominance 作为通过门。R1 阶段 B 仍须用“同一已执行菜单/相同可见证据”的对照区分选择
收益与额外执行收益，但 latency、调用数、token 和货币成本只记录，不进入 R1 目标；成本压缩另立后续工作。

## 5. Runtime reward 组合

运行时 reward 只能由部署可见信号构成，并逐项记录：

- deterministic format、option-domain、schema、tool postcondition 检查；
- counts-only agreement / consensus concentration；
- hypothesis-vs-hypothesis semantic equivalence；
- independent evidence corroboration 与 contradiction；
- tool execution/verification result；
- optional frozen cross-family judge 的 pairwise margin；
- explicit cost、latency、remaining budget。

Judge 主要作为 consensus 之上的边际仲裁者，而非默认唯一排序器。若 core 同时生成和评审，要单列
self-bias/SelfGap；若 judge 只看 transcript，要单列 text-over-acoustic failure。所有 reward component
都需要 reward-vs-gold 的离线 fidelity 审计，但 gold 不得回流 runtime。

## 6. 指标与统计

### 6.1 Primary capability

- task-defined accuracy/utility；
- paired delta against direct 与 strongest fixed baseline；
- bootstrap 95% CI 与预注册 lower confidence bound；
- binary outcome 使用 paired McNemar；多重比较时校正；
- 预注册 SESOI，低于 SESOI 即使显著也不升级主张。

### 6.2 Reliability

- seed/run variance；
- correct→wrong、wrong→correct 与净翻转；
- worst-group / lower-tail；
- clean、noise、reverb、accent/language、duration、task、core/service version 分桶；
- coverage-quality 与 selective risk；
- held-out acoustic strata 和 prompt permutation / judge swap 压力。

### 6.3 Cost

至少分开记录 frozen-core decode、DSP/operator、retrieval hop/bytes、judge/evaluator、wall-clock、API
currency；不能合并成一个模糊 cost。报告平均值、P95 与失败/超预算比例。双预算合同中任一 hard cap
超出即算该实例失败，不能用平均成本冲淡。

### 6.4 Headroom

Offline oracle 只解释实际 action/candidate menu 的 recoverability：

```text
recoverable_headroom = oracle_utility(executed_pool) - incumbent_utility
recovery_rate = (method - incumbent) / max(recoverable_headroom, δ)
```

它不是 system-level ICL 的开门门槛，也不能支持 all-contexts impossibility。

## 7. Readiness 与建议载体

第一纵向切片的建议载体是一个冻结 Qwen2.5-Omni-7B API serving lane，加 MMAU Test-mini 与 MMAR；
具体 revision、hash、服务栈和数据 split 仍为 `TBD_AT_AUTHORIZATION`。T2 当前记录两数据集均为
`metadata_only`；必须先解决任何“已 pin/已本地存在”的散文冲突，再允许执行。

扩展载体按研究问题选择：

- R1：MyST/RSR（ASR 主线）+ MMAU/MMAR（AU/AR 主线）+ MELD/MELD-Hard1k（受控机制）；
  主模型 `Qwen/Qwen2.5-Omni-7B`，独立复核 `XiaomiMiMo/MiMo-Audio-7B-Instruct`。MMAU/MMAR 在
  独立 demonstration pool 完成 split/contamination 审计前只承担 query-view arm；
- R2：AudioRAG-500、Omni-DeepSearch；
- R3/R7：MMAU/MMAR 的 time-ordered acoustic strata，加 MMSU/SAKURA；
- R4：MMAU Test-mini、MMAR，复用固定 speech tool library；
- R8：MMAU/MMAR 主能力，加 AQUA-Bench、SpeakerSleuth/ParaPairAudioBench 等压力载体；
- R9：先封闭 MCQ，再做可分离 task-success/latency 的 speech-native interactive validation。

专有 API 可以做外部有效性对照，但版本漂移、成本与 judge-family overlap 必须显式。

## 8. Lean 分工

Lean 只审计“显式假设是否蕴含目标命题”，不证明真实模型满足假设。每个 Stage-2 合同至少有：

1. runtime state/action 的类型定义；
2. hard budget 下 bounded termination；
3. incumbent candidate 可恢复；
4. gold boundary 不变量；
5. provenance 不随合法 transition 丢失；
6. estimator 与真实 utility 一致误差假设下的 margin rule；
7. executable trace 到 Lean operator 的 conformance tests。

现有允许使用的核心结论：若 `|estimated utility - true utility| ≤ ε` 对 incumbent 和候选均成立，
estimated selected-over-incumbent margin `≥ 2ε` 蕴含真实非回归，严格 `> 2ε` 蕴含真实提升。该定理不
证明经验误差界、跨分布稳定性或实际 controller 有效。`Iterate` 的终止/收敛结果依赖逐步真实增益等
显式假设，不能直接写成“实现已被证明收敛”。

## 9. 统一击杀与重路由规则

任一 proposal 遇到以下情况不得升级：

- 承重机制需要内部量或梯度；
- gold、gold-derived metadata 或 future instance label 进入 runtime；
- 模型/数据/许可证/version/hash 不闭合；
- 除 R1 已声明的能力上界特例外，adaptive method 在同成本下不超过 structured prompt、best fixed 或
  terminal-only 对照；R1 自适应主张的必要条件是超过 best fixed 并恢复一部分预注册菜单选择机会；
- 净提升低于 SESOI，或由少数 bucket/异常 seed 驱动；
- correct→wrong、worst-group 或成本越过预注册 tolerance；
- 所谓 reliability 来自近零 coverage；
- donor 效果被误写成 speech 效果；
- 形式化假设未校准，却把条件命题写成经验保证。

击杀动态机制不等于删除所有工程资产：正贡献的固定 supply、skill 或 wrapper 可降级为 R5 的固定组件；
失败 trace 则进入 R3/R7 的假设生成，但不能用 retrospective best checkpoint 掩盖在线失败。

## 10. 共同 evolution protocol

Stage-2 期间每遇到近邻工作，用同一四问吸收：

1. 它实际改变了什么状态或动作？
2. 它的效果依赖哪些内部量、标签、数据或模态条件？
3. 在同 API-only、同 core、同供给/预算合同下，它占据了本 proposal 的哪一步？
4. 尚可检验的 improvement space 是机制、可靠性、归因、成本还是跨条件泛化？

新工作可以缩小、重构或支配具体实例化；不能因发布时间更新自动“击杀”方向，也不能在未复现时把
论文数字纳入自己的 capability claim。
