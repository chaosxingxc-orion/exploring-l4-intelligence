---
title: "Stage-1C v2 experiment-family mapping doctoral-supervisor advisory review"
date: "2026-07-23"
artifact_type: "DOCTORAL_SUPERVISOR_ADVISORY_REVIEW"
campaign: "system-first-stage1c-v2"
round: "round-02"
review_target: "SF-STAGE1C-V2-PRE-SIGN-REVIEW-PACKAGE-2026-07-23"
review_package_manifest_sha256: "64d19df36df5d7cebbae4a7a885561ef7d0996d10856a39d16eb690b63290f21"
frozen_stage1b_release: "38fb9435d0c35e226ad62b16015a6dbee054e6c2"
verdict: "WITHHOLD_WITH_BOUNDED_DEFECTS"
authority_effect: "WITHHOLD_ONLY_NO_EXECUTION_GRANT"
human_signature_claimed: false
model_or_metric_execution_authorized: false
experiment_level_recoding_authorized: false
novelty_verdict: "NOT_REQUESTED_AND_NOT_ISSUED"
---

# Stage-1C v2 博导视角审查意见：有界整改后再启动实验族映射

## 一、裁决

**裁决：`WITHHOLD_WITH_BOUNDED_DEFECTS`。**

本审查不否定 Stage-1C v2 的研究方向，也不要求团队返回无界 Stage-1B discovery 或继续增加与研究问题无关的
对抗式代码鲁棒性。当前包已经具备可靠的来源冻结、权限隔离和基本实验映射骨架；但它还不能直接授权
226 篇论文的实验级重编码、family adjudication 或 branch formation。

研究团队可以继续当前已经签署的 Stage-1C v1 common-rubric evidence comparison，并完成本文限定的 v2
协议、schema 与 checker 修复。修复后只需要一次有界复审，不需要重新进行一轮广泛文献发现或工程加固。

本文是 AI 生成的博导视角 advisory review，不冒充自然人身份或自然人签字。它可以表达
`WITHHOLD_WITH_BOUNDED_DEFECTS`，但不能授予 `SIGN_STAGE1C_V2_EXPERIMENT_MAPPING` 或任何实验执行权限。

## 二、审查对象与核验结果

审查对象是 SHA-256
`64d19df36df5d7cebbae4a7a885561ef7d0996d10856a39d16eb690b63290f21` 绑定的 pre-sign package，
包括 protocol、machine contract、226-row bootstrap、generator/checker、tests 与 pre-sign report。

本轮独立核验得到：

1. 四个 Stage-1B registry shard 的工作树 SHA-256 与固定 commit
   `38fb9435d0c35e226ad62b16015a6dbee054e6c2` 中的 Git blob bytes 完全一致；
2. bootstrap 为 226/226 unique records，角色分布为 12 `KEEP_CORE`、43 `KEEP_INSTRUMENT`、
   45 `KEEP_TRANSFER`、126 `KEEP_NEGATIVE`；
3. 226 行全部保持 `AWAITING_AUTHORIZED_EXPERIMENT_RECODE`，没有预先声称 experiment cell、family、
   branch 或 adjudication；
4. review-package manifest 的真实 SHA-256 与 review request 声明一致；
5. `scripts/survey/test_sf_stage1c_v2_experiment_mapping.py` 的 22 项测试全部通过；
6. 这些 PASS 只证明 pre-sign contract integrity，不证明 post-sign 研究编码方法已经充分，也不产生
   authority effect。

## 三、值得保留的设计

以下结构不应在整改中被推倒重来：

- 论文记录、run-config experiment cell、dataset edge、experiment family 与 research branch 分层；
- 同一 run 的多个指标作为 cell observations，而不是重复制造 experiment cells；
- 数据集 factual lineage 与 same-task/protocol analogue 明确分开；
- 跨论文数值比较要求 dataset/model/access/input/metric/budget exact key；
- validation、transfer、falsifier 和 instrument 以 typed edge 接入，不自动获得数值可比性；
- nearest-prior reproduction、strongest falsifier、kill criterion 和 oracle/upper-bound arm；
- H5、no-execution、no-novelty 和 Stage-2A reproduction-first 边界；
- family/branch portfolio 仍需第二道独立 gate。

这些设计说明团队已经从“按论文写摘要”转向“按研究问题组织可审计实验事实”，方向是正确的。

## 四、签署前必须关闭的四个有界缺陷

### P0-1：v2 evidence surface 落后于已经生效的 Stage-1C v1

**失败合同：current-evidence inheritance / coverage completeness。**

v2 bootstrap 只从固定 Stage-1B 226-work registry 派生。当前 Stage-1C v1 已经登记的四项 bounded priority
intake——TRACE、S2S-Arena、MTalk-Bench 和 SimulU——均不在这 226 行中。若 v2 直接 supersede v1，新的映射
会在最关键的 speech-native measurement 与 model-internal boundary 上回退到旧证据面。

**最小修复：**

1. 保留 `226` 作为不可改写的 Stage-1B frozen-base denominator；
2. 增加四项 Stage-1C priority-overlay records，不向 Stage-1B registry 回写，也不制造 duplicate claim seed；
3. Stage-1C paper-audit denominator 明示为 `226 frozen base + 4 current overlay = 230`；
4. 四项 overlay 必须绑定当前 canonical work ID、官方全文 locator、本地 PDF/e-print hash、角色和边界状态；
5. checker 同时证明 `226` 的 release immutability 和 `230/230` 的 Stage-1C audit coverage。

### P0-2：experiment-family mapping 没有继承 Stage-1C 的决策问题

**失败合同：decision traceability / v1 semantic inheritance。**

当前 Stage-1C 的任务是比较三个未排序问题包：

- `BUDGET_STOP_REPAIR`；
- `EVALUATOR_REWARD_RELIABILITY`；
- `INTERACTIVE_FULL_DUPLEX_OBJECTIVES`。

它们共享九个 rubric dimensions：problem distinctness、decision causality、measurement validity、
modality necessity、failure severity、feasibility、reproduction anchor、scope compatibility 和 evidence
maturity。v2 当前只定义宽泛的 capability tags 和 family core signature，没有强制 family、local protocol、
branch 回连这三个问题包和九维 rubric。

**最小修复：**

1. 每个 load-bearing experiment family 必须携带一个或多个 `bundle_ids`；
2. 每个 family/branch 必须携带九维 rubric assessment、evidence locator 和 uncertainty；
3. 无法路由到三个 active bundles 的 family 保留为 `REFERENCE_ONLY`，不得自行扩张 Stage-1C 候选问题集；
4. 禁止聚合总分、隐式排序、winner 声明和 owner selection；
5. v2 supersession 必须显式继承 v1 priority intake、routing corrections 和 H5 exclusions，而不是仅继承
   Stage-1B release hash。

### P0-3：实验抽取 universe 与 paired comparison 尚未定义

**失败合同：selection-bias control / experiment-unit validity。**

“primary coding covers 226/226”没有回答多实验论文应抽取全部实验、主表、最佳结果，还是只抽取支持性结果。
这既可能造成无限工作量，也可能造成事后 cherry-picking。当前 observation 同时保存 baseline value 与
method value，但没有强制证明两者属于同一数据、模型、提示、解码、预算、随机重复和 evaluator 配置。

**最小修复：**

1. 论文级 disposition 覆盖 `230/230`；
2. 对 load-bearing empirical papers，完整抽取所有会改变 family 结论的主比较、负结果、消融和失败结果；
3. 非承重论文允许作为有理由的 non-cell evidence node，不要求把每个附录数值机械转成 cell；
4. baseline 与 intervention 建立显式 paired-comparison edge；不满足配对条件时只能并列陈述；
5. cell/config 至少显式编码 preprocessing/input representation、prompt/template、decoding、evaluator/judge
   identity and revision、stopping rule、seed/replicate 或 paper-reported aggregation；
6. observation 增加 metric direction、unit/scale、aggregation level、sample size 和 uncertainty availability；
7. 先冻结 extraction codebook，再开始承重论文的批量编码。

### P0-4：family synthesis、盲审和 readiness 尚未形成可执行闭环

**失败合同：adjudication reproducibility / executable gate consistency。**

四个 family evidence states 目前没有确定性决策规则；“至少 20% stratified blind review”没有固定样本数、
随机种子、分层分配、coder independence、agreement 阈值或重做条件。协议要求 closable
`LOCAL_ADAPTABLE`，但当前 `branch_readiness()` 对任意 `LOCAL_ADAPTABLE` 都直接接受，散文与执行规则不一致。

**最小修复：**

1. 定义 within-pair、exact-comparability stratum 和 cross-stratum qualitative synthesis 三层证据层级；
2. family state 必须由显式 support/null/negative/mixed 规则和 evidence maturity 产生，禁止仅按论文数量投票；
3. 在 230-paper surface 上固定 blind-review 样本数至少 46、抽样随机种子和 role/domain/task 分层算法；
4. blind reviewer 必须独立于 primary coder；记录 agreement 指标、接受阈值、冲突升级和 adjudicator；
5. core members、load-bearing relations、family conclusions 和 branch cards 继续保持 100% second review；
6. 为 paper audit、experiment cell、dataset graph、family card、local protocol、review record 和 branch card
   提供完整机器 schema 与 whole-package validator；
7. `LOCAL_ADAPTABLE` 只有在 exact asset/revision、license/terms、loader/adapter、frozen access 和 evaluator
   closure checklist 全部可关闭时才通过 readiness；否则保持 non-ready；
8. 修正 `branch_readiness()`，使实现与 `LOCAL_READY_OR_CLOSABLE_LOCAL_ADAPTABLE` 合同一致。

## 五、执行效率改进

为避免再次陷入“先把所有表和防御性测试做满”的循环，建议采用一次校准、随后展开的两阶段执行：

1. **Calibration batch**：12 `KEEP_CORE`、四项 priority overlay，以及覆盖 role/domain/task 的承重
   instrument、negative 和 transfer 样本；
2. **Scale-out**：codebook、agreement 和 validator 达标后，完成 230/230 paper disposition，并对承重论文
   进行有界但完整的 experiment extraction。

校准批次的目标是发现概念歧义和 coder drift，不是提前形成 family 结论。校准失败只触发一次 codebook
修订和重编码，不触发 broad discovery、模型调用或额外“对抗鲁棒性工程”。

## 六、研究阶段与创新性边界

本轮没有要求、也没有发布技术创新性判断。Stage-1C v2 应回答：

> 哪些实验事实、反证、可复现锚点和本地条件足以把一个问题分支送入 reproduction-first Stage-2A funnel？

它不应回答：

> 哪个新算法最有创新性，或者哪种候选技术已经胜出？

`candidate_strategy` 只能冻结 inputs、state、signals、decision rights、actions 和 expected causal path。
branch portfolio 必须保持未排序；最终问题选择属于 owner gate，技术方案创新收敛属于 Stage-2A/2B。

## 七、当前允许与禁止的工作

### 允许继续

- 当前已签署的 Stage-1C v1 evidence-only common-rubric comparison；
- 本文四项 P0 的协议、schema、checker 和 review-package 修复；
- 不产生研究结论的 metadata bootstrap 与 calibration-batch planning；
- 使用已有本地全文补齐 locator、版本和 paper-reported experiment facts 的编码模板设计。

### 继续 withheld

- Stage-1C v2 正式 experiment-level recoding；
- family adjudication、family evidence-state conclusion 和 branch formation；
- CURRENT activation 或覆盖 Stage-1C v1 authority；
- 模型/API 调用、dataset/benchmark metrics、paper reproduction、prototype；
- 问题排名、owner selection、novelty verdict 或 Stage-2A execution。

## 八、复审关闭条件

团队提交一个重新 hash-bound 的 v2 review package，并同时证明以下条件后，本审查人倾向于在一次有界复审中
改判为 `SIGN_STAGE1C_V2_EXPERIMENT_MAPPING`：

1. `226 + 4 = 230` dual-layer evidence surface 完整且无 duplicate seed；
2. 三个 active bundles 与九维 rubric 被机器合同强制继承；
3. extraction universe、paired comparison 和 observation semantics 已冻结；
4. family-state、blind review、agreement/adjudication 和 closable readiness 可执行；
5. post-sign whole-package schemas/checkers 对上述规则 fail closed；
6. pre-sign bootstrap 仍保持零 experiment cells、零 family memberships、零 branches 和零执行；
7. 没有修改固定 Stage-1B v5 release，也没有扩张到创新性或模型实验。

只要这七项关闭，就没有必要用“继续扩大 Stage-1B 调研”或“继续增强非必要代码鲁棒性”拖延 Stage-1C。

## 九、目的链、Provenance 与失效条件

**目的链：** 为 Stage-2A 选择一个可复现、可证伪、符合 frozen black-box external-control 边界的问题；因此
Stage-1C v2 必须把当前全部承重证据映射到同一决策 rubric，并在启动大规模编码前消除选择偏差和复核歧义。

**Provenance：** 固定 Stage-1B v5 release
`38fb9435d0c35e226ad62b16015a6dbee054e6c2`、当前 Stage-1C v1 common-rubric artifacts、以及 manifest
`64d19df36df5d7cebbae4a7a885561ef7d0996d10856a39d16eb690b63290f21` 所绑定的 v2 pre-sign package。

**失效条件：** 若后续提交的 exact review package 已关闭本文七项复审条件，则本 withholding verdict 仅作为历史
审计事实保留，由新的独立 review transaction supersede；不得原位改写本文。
