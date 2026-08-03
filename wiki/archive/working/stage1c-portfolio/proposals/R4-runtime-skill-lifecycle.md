---
proposal_id: "R4"
title: "运行时多模态技能的信用、组合与生命周期"
dimension: "D3 multimodal skills"
status: "workbench proposal; owner review pending"
execution_authority: "WITHHELD"
---

# R4 — 运行时多模态技能的信用、组合与生命周期

## Proposal 摘要

本研究把 speech tool、程序和动作模板统一成带前置条件、输出 schema、成本和验证器的 executable skill
contract。系统不依赖手写 reliability tier 或模型自由文本路由，而是在运行时比较 no-tool、单工具或组合
轨迹的 evidence diff 与下游 task utility，分配信用并据此选择、修复、复用和退役技能。

核心问题不是“工具越多是否越好”，而是冻结 core 能否在固定工具库下可靠识别**哪个技能在什么条件下
产生净正贡献**。直接语音工作已经证明工具选择和组合可提升，也证明 all-tools 会显著伤害；开放步骤是
免梯度、无 test gold 的运行时信用与生命周期。

## 1. 研究问题与假设

- `H1 credit`：部署可见的 tool/no-tool 或 matched alternative 差分信号能预测技能的真实贡献符号。
- `H2 adaptive selection`：reward-guided skill policy 在同工具库、同 frozen core、matched calls 下超过
  hand router 和 best fixed subset。
- `H3 verification`：输出验证和 incumbent fallback 能显著降低 tool-induced correct→wrong。
- `H4 composition`：经过 contract 验证的程序化组合超过平铺 all-tools/parallel evidence，且错误传播可归因。
- `H5 lifecycle`：由重复成功轨迹归纳的技能在 held-out task/condition 上可复用；持续负贡献时退役优于
  永久保留。

## 2. 语音近邻与跨域 donor

| 证据 | 已占机制 | 开放台阶 |
|---|---|---|
| `SPEECH_NEAREST_PRIOR` Speech-Copilot (2407.09886) | 工具构建、query-conditioned selection、带控制流的程序组合 | selection 贡献未单独隔离；提出 RLHF 选工具但未做运行时免梯度信用 |
| `SPEECH_NEAREST_PRIOR` Audio-Maestro (2510.11454) | 固定 speech tool library、prompted gating、Improved/Degraded 归因 | 改变答案的调用中约 41.6–43.5% 朝错误方向；无部署仲裁回退 |
| `SPEECH_NEAREST_PRIOR` AuTAgent (2602.13685) | 学习式 subset gate，优于 prompted gate；有单工具 oracle | gate 训练需 gold/梯度，不符合 TF-Strict；工具输出错误仍大 |
| `SPEECH_NEAREST_PRIOR` AudioToolAgent (2510.02995) | 大工具面和多轮 tool use | 高延迟/高调用上限，缺少净信用与停止价格 |
| `CROSS_DOMAIN_METHOD_DONOR` Trace2Skill、PANDO、VISUALSKILL | 轨迹到技能、在线蒸馏/退役、视觉技能表示 | trained donor 只借协议；GUI/vision 效果不外推 |

## 3. 方法设计：Skill contract

每个技能版本化为：

```text
skill = {
  name, version, precondition, input_schema,
  deterministic_or_stochastic_executor,
  output_schema, postcondition, verifier,
  cost_model, applicable_conditions,
  provenance, failure_modes, retirement_state
}
```

第一阶段工具库固定，不研究自动生成任意代码。优先使用确定性或可独立验证工具：ASR、speaker count、
VAD/segmentation、denoise、source separation、spectral/tempo/pitch analysis、calculator/structured parser。

## 4. Runtime credit 与控制

### 4.1 Counterfactual pairs

对候选技能构造 `no-tool incumbent` 与 `after-tool answer`，或在同成本下执行 matched alternative。记录
pre/post answer、evidence diff、execution success、verification result、reward margin 和终局 task outcome。
测试 gold 只用于离线测 credit fidelity。

### 4.2 Credit hierarchy

信用分三层，避免把工具执行成功误当任务贡献：

1. execution credit：是否满足 schema/postcondition；
2. evidence credit：是否提供新且不矛盾的 evidence；
3. task credit：是否使候选相对 incumbent 的 estimated utility 提升。

多工具组合先用 leave-one-tool-out/Shapley 近似做离线归因；运行时只采用可负担的 marginal check，不把
proxy credit 称为真实因果贡献。

### 4.3 Lifecycle

重复成功的可复现 action subsequence 可被提名为 macro-skill；通过 held-out replay、成本和 provenance
检查后才进入 registry。持续负 margin、condition drift 或 verifier failure 触发降权、隔离、退役；不得因
偶然单次成功永久写入。

## 5. 实验设计

### 5.1 Carrier

使用 MMAU Test-mini + MMAR，复用一个固定、版本化 speech tool library 和单一 frozen core。按 task
category 与 acoustic condition 分层。先只测试单工具选择，再测试 2-step composition，最后才测试技能归纳。

### 5.2 Arms

`no-tool direct`、`structured prompt`、`random matched-call`、`all-tools`、`hand router`、`best fixed subset`、
`reward-guided single skill`、`reward-guided composition`、`offline any-tool oracle`。AuTAgent 的训练式 gate
可作为外部文献上界/非 TF-Strict 对照，但不能与我方机制混称。

### 5.3 Outcomes

Primary：任务 utility 相对 no-tool 与 best fixed 的 paired delta。Secondary：tool relevance、执行成功、
evidence validity、credit AUROC/rank correlation、Improved/Degraded 四格、correct→wrong、per-tool net
contribution、调用/延迟/成本、跨任务复用、registry size 和 retirement precision。

### 5.4 Ablations

- 只做选择 vs 选择+输出验证；
- tool-level gate vs evidence-item admission；
- hand tier vs condition-keyed credit；
- incumbent fallback 开/关；
- single skill vs programmatic composition；
- 无退役 vs decay/retire；
- 从成功轨迹归纳的 macro-skill vs 人工同构 macro。

## 6. Lean 与数学建议

对确定性 skill 证明 precondition 满足时 postcondition，失败时错误被显式传播且不会伪装为 evidence；
composition 证明 schema 可连接、预算下降、provenance 合并且 incumbent 可恢复。对随机/黑盒工具只形式化
接口，不证明效果。

数学上将技能贡献定义为条件差分：

```text
A_k(c) = E[U(after skill k) - U(no skill) - λ Cost(k) | c]
```

多技能交互可用 ANOVA/低阶 Shapley 做离线分析；运行时使用 conservative lower bound。若 interaction
dominant，best single-skill credit 不能直接加和，组合策略必须作为独立 arm。

## 7. 风险、击杀与重路由

- dynamic policy 不超过 best fixed subset：击杀动态选择，保留正贡献固定工具作为 R5 组件。
- 输出验证贡献大于选择且选择信用不稳：重心转为 verifier/evidence admission，不夸大 router。
- all-tools 或 macro-skill 收益来自更多供给：在 equal-supply 对照下重测；不成立则取消组合主张。
- skill induction 只记住题目模板、未跨 task/condition：停止自动归纳，只维护人工 contract registry。
- tool 需要模型内部量或训练 selector：不属于承重 TF-Strict 方案。

## 8. 路线与预期贡献

Stage-2B 先回答“能否无标签判断 tool/no-tool 哪个更好”，再扩展到组合，最后研究归纳/退役。预期贡献
包括统一 speech skill contract、运行时反事实信用协议、输出验证与选择的贡献分解，以及在成立时的
training-free skill lifecycle。

## 9. Provenance

语音事实来自 D3 dossier；系统失败与基线来自 D4；Trace2Skill/PANDO 等只作 D6 method donor。未做
first-ever 或跨模态效果判断。
