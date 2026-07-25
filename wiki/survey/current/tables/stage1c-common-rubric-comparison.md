---
artifact_id: "SF-STAGE1C-PROBLEM-SELECTION-CLOSEOUT-V2"
owner_stage: "STAGE_1C"
ordering: "RANKED"
selection_status: "C1_DECISION_CALIBRATED_REWARD_SELECTED"
execution_authority: "STAGE2A_WITHHELD"
---

# Stage-1C problem selection closeout

## 结论

Stage‑1C 已完成问题层选择。主问题是：

> 对 API-only 的冻结 speech/omni core，当外部、多模态但不完美的 evaluator 只有有限、会漂移的信号时，
> 什么条件足以让它安全地改善 `select / repair / stop / abstain` 决策；什么条件下 controller 必须保留
> incumbent 或停止，因为 oracle headroom、候选内 signal fidelity 或 decision margin 不足？

正式标识为 `C1_DECISION_CALIBRATED_REWARD`，状态为
`STAGE1C_COMPLETE_PROBLEM_SELECTED_STAGE2A_REPRODUCTION_AUTHORIZATION_PENDING`。

这不是“再做一个 audio judge”，也不是技术方案或 novelty verdict。研究对象是 evaluator signal 到真实
decision utility 的因果接口；音频 evaluator、修复/停止策略与 voice-agent benchmark 分别是信号、决策
切片和验证环境。

## 范围裁决与遗留项关闭

- R1 的 agreement `FAIL`、未裁决分歧和 R2/R2R1 方法工件全部保留；R2R1 通过的 22 个定向测试只证明
  工件可保存，不证明 calibration 有效。
- R2R1 从未分发、未获独立 ACCEPT，现以 `RETIRED_WITHOUT_DISTRIBUTION_OR_INDEPENDENT_ACCEPTANCE`
  结束，不再执行第三轮 N=56 dual-model recode。
- H5 保持 `WITHHOLD_NON_LOAD_BEARING`。它继续禁止跨模态承重结论，但不再阻断三个非 H5 问题卡。
- specialized Duplex-model development 仍不进入研究、复现或 branch primary。交互/全双工论文只可作为
  speech-native validation evidence。
- 本轮没有模型/API、benchmark metric、论文复现、prototype、push 或 wiki publication。

这个裁决把精力从 schema/mutation/cross-platform 防护转回论文问题：只保留会改变论文角色、问题选择或
承重结论的检查。

## 调研方法与证据边界

本轮以 Stage‑1B v5 的 320-work calibration union、当前 18-work evaluator supplement 和已冻结全文为
底座，针对四个问题做定向更新：

1. speech/audio evaluator 给出的是 aggregate agreement，还是能在同一 candidate pool 内改变正确决策；
2. noisy verifier 何时使 selection、repair 或 stop 比 frozen baseline 更差；
3. interactive/full-duplex 是独立主问题，还是更一般 external-control 问题的验证环境；
4. 哪些 nearest priors 和 assets 足以进入 reproduction-first Stage‑2A handoff。

调研使用 12 组定向检索、复核 20 余个 primary-source 页面，并深读 7 篇关键全文/长摘要。主要证据如下：

- [AudioJudge](https://aclanthology.org/2026.eacl-long.168/) 显示 pairwise/多维 speech judging 的潜力，
  同时记录 position、verbosity 等偏差；它是 evaluator protocol，不是 controller。
- [TRACE](https://aclanthology.org/2026.findings-eacl.151/) 将 content、voice quality、paralinguistics
分解为 structured cue blueprint 与 deterministic fusion，说明在已检视证据包内，“opaque audio judge”并非可用的唯一信号形式。
- [SpeakerSleuth](https://aclanthology.org/2026.acl-long.944/) 发现 LALM 在多轮 speaker consistency 上会让
  textual coherence 压过 acoustic evidence，但在 variant ranking 上更强。
- [ParaPairAudioBench](https://arxiv.org/abs/2606.24648) 的核心反证是 tie/abstain calibration failure；
  强迫 winner 不能等价于可靠 decision signal。
- [LALM voice-agent judge reliability](https://arxiv.org/abs/2607.07985) 说明 rank correlation 可以跨
  model swap 保留而 absolute calibration 失效，且部分维度首先是 rubric construct-validity 问题。
- [JudgeBoN](https://arxiv.org/abs/2603.12520) 直接证明 global correlation 不能替代 within-prompt
  ranking、tie-aware top-1 与 recovery；这是 C1 的 decision-utility 祖先。
- [Oracle Gap and Signal Fidelity](https://arxiv.org/abs/2607.17531) 将 fixed-pool gain 分解为 recoverable
  mass、coverage、conditional selection quality 与 harm，支持“先测空间，再测信号，最后决定是否控制”。
- [VRR-Stop](https://arxiv.org/abs/2607.17641) 表明 repair 会损坏正确 incumbent，且 stop 的可靠性由
  verifier discrimination 与 decision margin 共同决定；低可识别区应使用 conservative fallback。
- [AudioGenie-Reasoner](https://arxiv.org/abs/2509.16971)、
  [AudioToolAgent](https://arxiv.org/abs/2510.02995) 与
  [MUGEN](https://arxiv.org/abs/2603.09714) 已占据 evidence refinement、tool arbitration 和 fixed-K
  consensus，因此宽泛的“training-free audio agent/repair/selection 尚不存在”是错误命题。
- [VoiceAgentBench](https://arxiv.org/abs/2510.07978)、
  [tau-Voice](https://arxiv.org/abs/2603.13686)、
  [Full-Duplex-Bench-v3](https://arxiv.org/abs/2604.04847) 与
  [IHBench](https://arxiv.org/abs/2606.19595) 证明 speech-native task success、tool correctness、latency、
  interruption 与 recovery 可以分离；这些差距不能自动归因于 external control。

事实与项目推论分开：上述论文支持具体 failure modes 与 measurement contracts；“C1 最适合作为本项目
主问题”是基于本项目 black-box/TF-Strict 边界作出的选择，不是文献声称。

## 三张最终问题卡与排名

排名采用词典序，不做伪精确加总：`scope compatibility → residual distinctness → falsifiability →
reproduction feasibility → system-first explanatory value`。

| rank | bundle | Stage‑1C card | disposition | 核心理由 |
|---:|---|---|---|---|
| 1 | `EVALUATOR_REWARD_RELIABILITY` | `C1_DECISION_CALIBRATED_REWARD` | `SELECT_PRIMARY_PROBLEM` | evaluator 是 reward-guided control 的承重信号层；已有测量很多，但 speech/omni 下的 causal decision utility 仍未闭合 |
| 2 | `BUDGET_STOP_REPAIR` | `C2_NOISY_STOP_REPAIR` | `FALLBACK_AND_C1_POLICY_SLICE` | 可证伪且兼容，但 generic stop/repair 已被占据；幸存问题是 noisy evaluator 下的一类 decision right |
| 3 | `INTERACTIVE_FULL_DUPLEX_OBJECTIVES` | `C3_INTERACTIVE_OUTCOME_CONTROL` | `VALIDATION_ONLY` | speech-native 价值高，但容易被 ASR/VAD/latency/base capability 混淆，且 specialized duplex branch 已排除 |

### Card 1 — `C1_DECISION_CALIBRATED_REWARD`（已选）

- **Problem distinctness:** 不问 evaluator 是否与人“总体相关”，而问它能否在同一 instance 的候选、修复
  或 stop 决策中实现净收益。
- **Decision causality:** signal 必须改变 `select / repair / stop / abstain`，且 terminal truth 独立于
  evaluator score。
- **Measurement validity:** 同时报告 oracle headroom、recoverable mass、coverage、candidate-level
  fidelity、within-instance ranking、tie/abstain、realized recovery、harm 与 cost。
- **Modality necessity:** 只有 acoustic/prosodic/speaker/timing evidence 改变最优 decision 时，raw audio
  才承重；其余先用 transcript/deterministic comparator。
- **Failure severity:** 错排、错误 repair、过早 stop 与虚假高分可以系统性污染所有后续动作。
- **Feasibility:** AudioJudge/TRACE/SpeakerSleuth 等全文和部分代码/数据可用；MMAU-mini/MMAR 已本地 pin。
- **Reproduction anchor:** AudioJudge protocol + JudgeBoN decision audit；AudioGenie-Reasoner 是最近直接
  agent prior，OracleGap/VRR-Stop 是 transfer comparator。
- **Scope compatibility:** prompted/frozen/deterministic evaluator 可进入；trained reward 只作 boundary。
- **Evidence maturity:** measurement-rich、project decision evidence 为零，正好构成 Stage‑2A 的目标。
- **Kill:** 一个现有 evaluator 在所有预注册 slice 上同时满足 decision utility、shift 与 low-harm，或
  candidate pool 几乎无 oracle headroom。

### Card 2 — `C2_NOISY_STOP_REPAIR`（fallback）

- **Problem distinctness:** 仅保留 noisy evaluator + finite cost 下的 continue/repair/stop/rollback；
  generic iteration 已被 AudioGenie-Reasoner、EChO-Agent、Omni-Decision 与 VRR-Stop 邻近占据。
- **Decision causality:** verifier 必须改变下一次 repair 或终止，而非只输出分数。
- **Measurement validity:** true task validity 与 proxy acceptance 分离，记录 repair damage、margin 和 calls。
- **Modality necessity:** audio 只有在声学/说话人/时序改变最优停止动作时承重。
- **Failure severity:** fixed repair 可破坏已正确输出；保守 guard 也可能牺牲可恢复收益。
- **Feasibility:** 控制结构简单，但 speech task 的 noise-identifiable evaluator 尚未选定。
- **Reproduction anchor:** VRR-Stop 是理论/实现 comparator；MUGEN 是 fixed-K consensus baseline。
- **Scope compatibility:** 外部多调用与 stop/rollback 兼容 black-box；不使用 model-internal policy。
- **Evidence maturity:** 文献已有直接解法，独立主线的 residual 比 C1 窄。
- **Kill:** existing stop/repair rule 在同一 signal/noise/cost contract 上支配。

### Card 3 — `C3_INTERACTIVE_OUTCOME_CONTROL`（validation only）

- **Problem distinctness:** terminal task success 与 interruption/recovery/latency/interaction quality 分离。
- **Decision causality:** signal 必须改变 turn、tool、state update 或 recovery；benchmark 本身不算 controller。
- **Measurement validity:** task、tool、timing、resume、harm 分轴，不报告无权重 omnibus score。
- **Modality necessity:** speech timing/prosody/nonverbal cues 承重，但不外推 GUI/robotics/AV2AV。
- **Failure severity:** stale state、错误 tool、missed interruption 和自然但失败的对话。
- **Feasibility:** IHBench/VoiceAgentBench/FDB-v3 等可用性不一；tau-Voice 仍需 exact asset closure。
- **Reproduction anchor:** 只在 C1/C2 的信号控制先成立后选择一个 speech-native validation carrier。
- **Scope compatibility:** specialized duplex-model engineering 明确排除。
- **Evidence maturity:** benchmark/direct systems 都已出现，但 controller attribution 未隔离。
- **Kill:** 误差主要由 ASR/VAD/serving latency 解释，外部 evaluator/controller 无可恢复空间。

## 已选问题合同

```text
observation   = speech/audio + fixed candidate supply + task-visible evidence
external state = candidates + evaluator protocol + disagreement + history + cost
signal        = frozen/deterministic scoped verdict(s), including abstain
decision      = select | repair_once | stop | abstain/keep_incumbent
terminal truth = task gold | deterministic environment outcome | preregistered human reference
```

不得把 evaluator score 当作 terminal truth，也不得把离线 correlation 自动升级成在线 reward control。

### Research questions

1. `RQ1_HEADROOM`：每个 model × task × supply cell 有多少 oracle headroom、recoverable mass 与 diversity？
2. `RQ2_SIGNAL`：pointwise、pairwise、listwise、dimension-first、tie/abstain 哪种 protocol 保留候选内信号？
3. `RQ3_DECISION`：信号接入 select/repair/stop 后，真实效用净增多少，损坏正确输出多少？
4. `RQ4_SHIFT`：model/task/acoustic shift 下，何时 decision sign 可识别，何时必须保留 incumbent？

### 最小承重指标

- `oracle_gap` 与 `recoverable_mass`；
- `signal_coverage`、candidate-level fidelity/MCC、within-instance rank 与 tie/abstain；
- `realized_gain` / `recovery` 与 top-1 decision accuracy；
- `harm_to_already_correct` 与 repair damage；
- decision margin、shift delta、calls、latency 与 cost。

global correlation、system-level ranking 或平均 judge score 不能单独支撑控制结论。

### 单观察击杀条件

任一条件成立即击杀或重路由：

1. 目标 cell 的 oracle gap/candidate diversity 可忽略；
2. deterministic rule 或现有 frozen evaluator 在所有 slice 上以更低 harm 支配；
3. signal 在预设 shift/noise 区间不可识别，且 guard 的有效 action coverage 近零；
4. equal-supply 控制后增益消失，或只能归因于 generator/更多调用。

## Stage‑2A reproduction-first handoff（冻结清单，不执行）

| item | role | frozen disposition | blocker before run |
|---|---|---|---|
| AudioJudge (`2507.12705`) | primary speech evaluator protocol | `ON_REPRODUCTION_LIST` | pin exact package/model/prompt/data slices |
| JudgeBoN (`2603.12520`) | primary decision-utility diagnostic | `ON_REPRODUCTION_LIST` | translate fixed-pool audit without claiming speech transfer |
| AudioGenie-Reasoner (`2509.16971`) | nearest direct speech-agent prior | `ON_REPRODUCTION_LIST` | remote planner/model/tool revisions and evaluator adapter |
| OracleGap (`2607.17531`) | fixed-pool transfer comparator | `COMPARATOR_ONLY` | speech translation and official-label audit |
| VRR-Stop (`2607.17641`) | noisy repair/stop comparator | `COMPARATOR_ONLY` | do not import text-task effect sizes; define speech verifier noise |
| MMAU-mini + MMAR | local validation carriers | `PRIMARY_LOCAL_DATA` | freeze split, candidate supply and terminal scorer |
| TRACE (`2026.findings-eacl.151`) | dimension-first evaluator comparator | `CONDITIONAL` | recheck released annotations/code and deterministic fusion bytes |

AudioToolAgent 因 license/exact environment 未闭合不作 primary anchor；specialized duplex benchmarks 不作
reproduction branch。它们可在 Stage‑2A 后期作为 adversarial/validation evidence 重新评估。

## Stage‑2A 开门条件

只有新的 owner authorization 同时绑定以下内容，才可运行任何模型/API/metric/reproduction/prototype：

- frozen core 与 API-only access；
- task/dataset revision/split 与 contamination boundary；
- candidate-supply contract 和 first-sample/random/oracle/MBR baselines；
- terminal truth、evaluator protocols、decision rights、harm/cost measures；
- 上表 reproduction items 的 exact revisions；
- abort rules：无 headroom、signal 不可识别、harm 超阈或 asset/license 不闭合。

建议请求 token：`AUTHORIZE_STAGE2A_DECISION_CALIBRATED_REWARD_REPRODUCTION`。本 Stage‑1C closeout
不自授该权限。
