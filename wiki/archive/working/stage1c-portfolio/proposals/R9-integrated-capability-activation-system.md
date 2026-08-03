---
proposal_id: "R9"
title: "五维集成的可靠能力激活系统"
dimension: "integration of D1-D5"
status: "workbench proposal; owner review pending"
execution_authority: "WITHHELD"
---

# R9 — 五维集成的可靠能力激活系统

## Proposal 摘要

本研究在同一 frozen speech/omni API core 上集成 D1 证据供给、D2 持久记忆、D3 技能、D4 证据状态与
决策权、D5 实例内/跨实例进化，检验 full adaptive control plane 是否稳定超过 direct、strong structured
prompt、best single component 和 best fixed composition，并定位组件间协同或抵消。

R9 不是“一次把所有组件接上”的大系统工程。集成顺序固定为：`R5 → R6 → R8 → R1/R4 → R3/R7 →
optional R2`。每个组件只有在自己的 proposal 击杀条件未触发时才进入，避免用更多调用掩盖单组件无效。

## 1. 研究问题与假设

- `H1 integrated capability`：full adaptive system 在 matched supply/cost 下超过 best fixed composition。
- `H2 complementarity`：至少一个组件交互项为正，且可通过 factorial/leave-one-out 复现；否则集成只是一组
  可独立部署的组件。
- `H3 persistence`：加入 R3/R7 后，未来实例 prequential utility 提升，不损害 held-out condition。
- `H4 reliability`：R8 能保留大部分单组件正增益并约束尾部回归；不能靠低 coverage 达成。
- `H5 speech-native validity`：在封闭 benchmark 成立后，系统在可分离 task success、latency、barge-in 和
  recovery 的 speech-native carrier 上仍有净能力价值。

## 2. 近邻系统与定位

Audio-Mind、Agent-Omni、Omni-DeepSearch、AudioToolAgent、AudioGenie-Reasoner、MUGEN、AOP-Agent、
TalTech/VISA 等表明复杂 audio/omni agent 已存在，也暴露了几个共同事实：direct readout 有时很强；固定
wrapper 可在大桶回归；component/core quality 可支配 orchestrator；过度搜索/观察会伤害；成本和方差常未
匹配。R9 因此不把“组合了五个模块”视为贡献，而把**同核、同供给、同预算下的归因与可靠净收益**作为
进入条件。

视觉/文本 agent 只提供 factorial、long-horizon、memory/skill lifecycle 和 process audit 协议；其效果不支持
speech 集成结论。

## 3. 统一系统合同

```text
D1 current evidence supply
   -> D4 evidence_state <- D2 persistent experience
          |                    ^
          v                    |
      D3 executable skills     |
          |                    |
          v                    |
      D5 within-instance policy -> D5 cross-instance update
          |
          v
      R8 accept / budget / rollback -> frozen core final answer
```

所有组件共享 state/action/reward/cost/provenance schema。组件只能通过版本化接口写 state，不能各自维护
不可见 scratchpad。最终 answer 始终保留原音 anchor 和 incumbent。R2 外部检索只在 carrier 被确认需要
外部事实时挂载；否则保持关闭。

## 4. 分阶段系统构建

### Phase A — Minimal vertical slice

R5 evidence state + R6 short-horizon control + R8 reliability。目标是证明 reward 会改变下一动作，并在
MMAU/MMAR 上可靠提高 task utility。

### Phase B — Action-space expansion

加入 R1 observation branching 和 R4 fixed skill library。每次只开放一个新 action family，先测 executed-pool
oracle，再测 controller recovery，最后测 cost-normalized net gain。

### Phase C — Persistent evolution

加入 R3 condition-keyed memory 和 R7 external policy update，使用 time-ordered prequential evaluation。

### Phase D — External knowledge

仅在 AudioRAG/Omni-DeepSearch 类任务加入 R2 pinned retrieval。Waveform-sufficient carrier 不默认搜索。

### Phase E — Speech-native validation

在 task success 与 latency/VAD/ASR/barge-in/recovery 可分离的 interactive/full-duplex carrier 上外部验证；
若这些因素不可分，结果只称系统演示，不承载机制主张。

## 5. 实验设计

### 5.1 Core comparisons

每阶段至少报告：`direct`、`strong structured prompt`、`best single component`、`best fixed composition`、
`full adaptive system`、`offline oracle over executed actions`。复杂 audio agent prior 要在相同 core/prompt/
budget 下重建或作为外部参考，不能搬运跨论文绝对数。

### 5.2 Factorial attribution

在可承受范围做主效应 + 关键二阶交互；全量 2^k 不可行时使用分阶段 fractional factorial，并固定：

- leave-one-component-out；
- component added last；
- same supply but fixed arbitration；
- same controller but fixed action menu；
- memory read-only vs update；
- reliability gate off/on。

组件贡献同时报告 average、worst-group、cost 和 correct→wrong，避免某组件只提高平均值却破坏尾部。

### 5.3 Evaluation portfolio

- 封闭能力：MMAU Test-mini + MMAR；
- observation/robustness：MELD-Hard1k + held-out real acoustic conditions；
- persistent stream：去重的 MMAU/MMAR/MMSU/SAKURA time-order；
- external knowledge：AudioRAG pinned snapshot；
- speech-native external validation：在协议可分离后选择 full-duplex/voice-agent set。

### 5.4 Primary result

主结果为 full adaptive system 相对 best fixed composition 的 paired task-utility delta/LCB，辅以
prequential future utility、worst-group、correct→wrong/wrong→correct、coverage、calls/latency/cost、memory
growth、component interaction 和 action trace fidelity。

## 6. Lean 与系统一致性

R9 的形式化重点不是新增宏大“收敛定理”，而是 executable semantics：每个组件 action 对应 Lean
constructor；接口保持 gold/provenance/incumbent/budget 不变量；composition 只有在各组件假设同时成立时
使用条件定理。Conformance tests 必须覆盖正常、tool failure、judge disagreement、budget exhausted、memory
contradiction 和 rollback trace。

数学上用分层价值分解而非简单加法：

```text
U(full) - U(base)
  = Σ main_effect(component)
  + Σ interaction(component_i, component_j)
  - orchestration_harm - reliability_rejection_cost
```

该式是实验估计框架，不预设交互项为正。跨实例部分另以 prequential value 分开，不与静态 test set 总分混合。

## 7. 风险、击杀与拆解

- full system 不超过 best component/fixed composition：拆回正贡献方向，击杀“集成增益”。
- 优势由更多调用解释：cost/supply-matched 后不成立即删除 adaptive claim。
- 组件交互大幅负值：保留 mutually exclusive routing，而非强行组合。
- R3/R7 只在 retrospective replay 有效：从集成系统移除持久更新。
- R2 live drift 或 retrieval harm 无法控制：保持 pinned/optional，或完全移除。
- full-duplex 指标混淆 task success 与 VAD/latency：不能用作能力主证据。
- 任何组件需要内部量、test gold 或未授权训练：从承重路径删除。

## 8. 执行路线、预期贡献与最终论文形态

若全链成立，贡献不是“模块数量”，而是：一个 API-only frozen omni control-plane contract；对 supply、
memory、skill、architecture 与 evolution 的可归因能力证据；condition-aware 非回归控制；以及从封闭任务到
speech-native interaction 的验证链。若集成不成立，portfolio 仍保留经 factorial 证明有正贡献的单方向，
并公开负交互与成本边界。

## 9. Provenance

R9 综合 D1-D5 dossiers、D6 donors、T1/T2/T3 和 CURRENT 九方向合同。它不发布 novelty/first-ever 判断，
也不把跨域 agent 效果迁移为 speech 结论。
