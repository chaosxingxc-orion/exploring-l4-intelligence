# Stage-1C v2 Agentic calibration codebook v2

本文件包含具名范围边界与治理解释，只进入 reviewer-visible package，不进入 coder distribution。
Coder 实际可见的中性规则固定在 `coder-codebook-v2.json`，并由递归 leakage scanner 检查。

## 1. 两层编码单位

Paper 是 audit unit，不是唯一 evidence object。每篇 response 先完成 paper labels；有可抽取实证实验时，
再建立 `run_cells`、`observations`、`paired_comparisons`、dataset graph、claim decisions 与
translation/compatibility decisions。非实证、反证或边界论文只连接合法 evidence node，不伪造 cell。

一个 run cell 的身份是：

`paper × dataset/revision/split × model/access × input condition × intervention × budget/horizon`

任一运行条件实质变化都新建 cell；同一次运行的 accuracy、WER、MOS、task success、latency、cost
只建立多个 observations。每个 cell 必须有且只有一个 `primary_intervention_axis`；K/S/M 可在 paper
层多标签，但系统组合收益不能重复归因。

## 2. Agentic scope

共享分析接口为：

`observation → external state → signal/evaluator → decision right → action/tool → feedback → update/repair/stop`

强类型字段如下：

- `scope_status`：直接 agentic、instrument、transfer analogue、reference boundary 或 specialized-system exclusion；
- `loop_components`：observe、state/memory、decide、act/tool、evaluate、update/repair、stop/budget；
- `core_dependency`：generic frozen core、specialized model、trained controller 或 mixed/unclear；
- `capability_assets`：knowledge、skill、memory 或 none；
- `control_role`：training-free reward-guided、training-free non-reward agentic、trained、instrument-only 或 none。

`DIRECT_AGENTIC` 至少要求 `DECIDE + ACT_OR_TOOL`，并且 core 必须是 generic frozen core；trained
controller 与 specialized model 均不能通过该 gate。FDB-v2 必须编码为
`OUT_OF_SCOPE_SPECIALIZED_SYSTEM + SPECIALIZED_MODEL_REQUIRED + REFERENCE`，不得成为 reproduction
candidate、`CORE_MEMBER` 或 branch primary。

## 3. 参考、借鉴与复现

- `REFERENCE`：只用于背景、定义、限制、机制、反证或排除边界；
- `BORROW_PROTOCOL`：借用决策结构、变量、对照或 evaluator，必须写 source→target translation 和
  rejection condition，不继承原论文数值；
- `REPRODUCTION_CANDIDATE`：task、dataset/protocol、entrypoint、evaluator、access、license 与版本存在
  可闭合路径；仍不等于已复现或已成为 anchor。

所有非语音 K/S/M 工作默认 `TRANSFER_ANALOGUE`。只有目标变量具备干预对应关系、outcome semantics
兼容且 rejection observation 可定义时，才能进入 family review；否则保留参考关系。

## 4. Dataset graph 与比较

Lineage 仅限 `SAME_REVISION / DERIVED_FROM / SUBSET_OF / TRANSLATED_FROM /
AUDIO_RENDERING_OF / REANNOTATED_FROM / SPLIT_OF`，每条必须有来源 locator。没有来源关系时只能登记
`INDEPENDENT_SAME_TASK / CROSS_DATASET_VALIDATION / DISTRIBUTION_SHIFT_TEST / PROTOCOL_ANALOGUE`。

跨论文数值只在 dataset revision/split、core model、access、input condition、metric 与 budget/horizon
全部一致时进入 `EXACT_PAIRED`。部分匹配只能并列陈述；`UNPAIRED` 与 `NOT_COMPARABLE` 不计算 effect。

## 5. Claim 与 family 边界

13 个 synthesis centres 是 `CLAIM_TEMPLATE`，不是已证实 claim。只有 problem/outcome、task、dataset、
model、access、input、intervention、budget 与 evaluator 九维 scope 兼容且命题等价的 instance 才可 merge。
Paper-link 数量不是支持票数。

能力维度不替代 experiment-family 的核心兼容门。Family 仍按问题、outcome semantics、environment/access
与 baseline→intervention 可解释性构建。Specialized-system exclusion 只能是 reference boundary；trained
controller 只能是 boundary/transfer/falsifier，不能悄然进入 frozen-core branch。

## 6. Agreement 与停止规则

- paper 单标签逐字段 exact raw agreement；多标签用 exact-set gate，Jaccard/F1 只作诊断；
- agentic scope 的 scope/core/control 与 loop/K-S-M assets 全部进入 paper-level agreement；
- object segmentation 使用同 paper/type 的 exact `object_match_key` micro-F1；
- 双方均为 `NOT_APPLICABLE` 才排除分母，单边 NA 计 disagreement；
- N=56 零正例类别标为 `NOT_CALIBRATED`，full mapping 时 targeted calibration 或 100% second review；
- 首轮低于 0.85 只允许一次 codebook consolidation 与全 N=56 重编；第二轮仍失败立即停止；
- agentic scope、primary intervention、reproduction、lineage、MM3、exact pairing、CORE_MEMBER、claim
  merge/split 与 access disagreement 必须由 human/domain-expert adjudicator 裁决。

## 7. 当前权限

本 codebook 只准备 calibration。当前没有 coder distribution、agreement、320-work mapping、模型/API、
metric、reproduction、prototype、family/branch selection 或 novelty verdict 权限。
