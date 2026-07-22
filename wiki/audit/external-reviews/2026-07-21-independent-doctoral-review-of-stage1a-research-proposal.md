# 2026-07-21 Stage-1A 独立博士生级敌意审查：research proposal for independent review

## 0. 审查对象、冻结点与裁决

本报告审查以下交付物，**不修改研究团队 worktree 的任何文件**：

- 目标文件：`.worktrees/stage1b-readiness-remediation/wiki/survey/workbench/system-first-stage1a/2026-07-21-research-proposal-for-independent-review.md`
- 冻结提交：`5d6e67abaff19ff40acc93a57f97fe7c4dbe80bc`
- 目标 Git blob：`f4d07c473007643ab6212dae38514d65affd8d4f`
- 目标 Git blob SHA-256：`a686dee87e0e0ddc9d2188432766224ae46f862167b1d8f528f16d99f0daa295`
- worktree 状态：审查前后均 clean
- 审查日期：2026-07-21
- 审查身份：独立 reviewer / 博导视角；未参与本轮实现，不代替 owner 授权

正式裁决如下：

```text
CURRENT_STAGE = STAGE_1A_FINAL_REMEDIATION
PROPOSAL_ARTIFACT_VERDICT = MAJOR_REVISION_BEFORE_FORMAL_ROUND_15
SCIENTIFIC_RATIONALE_FOR_CONTINUING_MAPPING = REVISE
SEARCH_DESIGN_SIGNOFF = WITHHOLD
STAGE_1B_AUTHORIZATION = NO
RESEARCH_INTEGRITY_VERDICT = NO_EVIDENCE_OF_FABRICATION_OR_FALSIFICATION,
                             BUT_MATERIAL_FALSE_ASSURANCE_AND_SELECTIVE_COVERAGE_RISKS_REMAIN
```

一句话结论：**研究方向值得继续，提案对阶段边界的自我约束明显改善，工程门也确实能诚实失败；但当前仍是 Stage-1A 收尾整改稿，不是正式可签署包。GM-2 的语义复核尚为 0/22，而且其中两条 DREAM 否定性编码已被原文证据实质挑战；书目从 241 个 union work 缩到 77 项的选择规则也不可审计。因此现在不能执行第一条 systematic discovery query，不能进入 Stage-1B。**

这里的 `REVISE` 不是否定研究问题，而是表示：科学动机已经足以支持继续完善 systematic mapping，但尚不足以签署当前检索设计和 exact package。

## 1. 当前究竟处于哪个阶段

### 1.1 阶段判断不是根据文件标题，而是根据尚未完成的授权链

现行方法论把阶段划分为：

- Stage-1A：问题定义、survey 设计、协议与开门条件；
- Stage-1B：systematic mapping 执行，全程禁止研究模型、smoke、任务指标和 prototype；
- Stage-1C：证据综合、形成 3–5 张候选问题卡、由 owner 选题并冻结复现清单；
- Stage-2A：复现先行，复现可用后才开始方向性方案探索；
- Stage-2B：方案验证。

目标稿自身也给出了正确披露：它仍是 `WORKBENCH_REVIEW_DRAFT`，当前为 `STAGE_1A_FINAL_REMEDIATION`；22 条 negative-evidence reviewer rows 为 0；正式 NT/POSIX v7 leaves 与 aggregate 尚未生成；formal round-15 proposal、独立签署和 owner 对 exact package 的授权均不存在。目标稿第 28、245–270、309–317 行的状态声明与这些事实一致。

因此，不能因为 GM-1、GM-3 代码和 GM-4 局部检查为 PASS，就把阶段升级为 Stage-1B。当前更准确的状态是：

```text
Stage-1A 科学问题与主要协议骨架：已形成
Stage-1A 技术整改基础：3 项局部成立，1 项语义门仍红
Stage-1A 正式独立签署包：尚未形成
Stage-1B systematic mapping：未启动、未授权
Stage-2 研究模型/实验：禁止
```

### 1.2 本轮没有实验性越界，但存在轻微 Stage-1C 职责前移

本轮披露的 systematic discovery query、research-model call、smoke、dataset metric、headroom 和 prototype 均为 0；没有发现研究团队偷跑模型或以冒烟集替代 survey。这一点符合当前阶段。

但是，提案第 148 行把“3–5 张 Stage-1C candidate problem card”列为 Stage-1B 产出，第 147 行还要求 Stage-1B 给出直接 prior 的“复现优先级”。这与现行方法论中“Stage-1C 形成候选问题卡并冻结复现清单”不完全一致。Stage-1B 可以输出：

- 形成问题卡所需的证据包；
- eligible candidate inputs；
- direct-prior proximity、可复现性、证据等级和未决项；

但不应在 Stage-1B 内完成最终问题卡、最终排序或选题。否则 Stage-1C 会被架空为形式批准。

## 2. 审查方法：四轮相互对抗，而不是一次通读

本报告按以下四轮独立路径交叉审查；后一轮专门尝试推翻前一轮的暂定结论。

### Round A：阶段、论证和内部一致性

逐节检查目标稿的研究对象、TF-Strict 边界、RQ、假设、Stage-1B 产出、Stage-1C/2 预告和 gate 表，重点寻找：把实证问题伪装成 mapping 问题、把 Stage-1C 工作前移、把局部 PASS 当作整包签署。

### Round B：已有论文全集和引用闭包

先使用仓内既有 corpus，而不是重新从网络制造一套平行 survey：核对 479 个物理 source rows、241 个 canonical work nodes、62 条 claim rows、77 项 reviewer bibliography，以及 archive 中没有被当前 union 接住的历史工作。外部检索仅补充 reviewer-known 反例，全部应记 `query_recall_credit=false`，不得倒灌为 frozen query 的召回能力。

### Round C：负证据语义反证

不接受“字段齐全所以语义为真”。抽查承重全文，专门寻找论文中能推翻 `absence=false` 的段落。该轮发现 DREAM 的两项否定性判断至少不能直接 `AGREE`，详见 §4。

### Round D：跨平台回放与研究诚信审计

在 Windows 运行 144 个聚焦单元测试，全部通过；在 WSL2 `Ubuntu-24.04` 直接解析 linked worktree 并回放关键检查。两端都给出相同的诚实结果：draft proposal 检查通过，但 release 检查因以下三项而失败：

```text
ABSENCE_REVIEW_PENDING
EVIDENCE_V7_LEAVES_OR_AGGREGATE_MISSING
PROPOSAL_NOT_PROMOTED_TO_ROUND15
```

这证明 fail-closed 架构本身有效，也证明“draft PASS”不能被解释成 Stage-1B readiness。

## 3. 值得保留的实质进展

严格审查不等于忽略正确工作。本轮至少有六项真实进展。

1. **阶段诚实性明显提高。** 提案明确写明自己不是 reviewer verdict 或 Stage-1B 启动令，也没有制造“零网络”“零历史 exposure”之类虚假叙述。
2. **system-first 研究对象比 selector-first 更合理。** 外部控制平面覆盖 observation/supply、state、memory、tool、candidate expansion、verification、fallback、budget 和 stop；best-of-N/MBR/reranking 被正确放回退化情形，而不是把整个 omni agentic system 缩成一个 evaluator。
3. **研究边界比早期版本更清晰。** 核心权重、外围权重、label-optimized controller、test gold、new-information channel 和白盒状态被列为需要分别编码的边界，不再统称 training-free。
4. **GM-1 的数据结构整改有价值。** 479 个 source rows 被路由到 241 个 canonical work nodes；claim 保持 hyperedge，multi-claim、multi-grade、multi-discrepancy 和 multi-target 没有被粗暴压成一个 work-level scalar。该局部 PASS 可以接受。
5. **GM-3 的平台结构是真整改。** Windows 与 WSL2 已能解析同一 linked worktree；NT/POSIX leaf 只能由各自 runner 产生，aggregate 在两叶之后独立生成。旧的“Windows 跑两次冒充双平台”漏洞已被结构性关闭。
6. **GM-4 的证据来源比手写常量可靠。** official raw payload、receipt、SHA、离线重建和 429 事故披露都值得保留。已知 ID 元数据访问不计检索 recall，也符合证据纪律。

这些优点说明团队并非在伪造 readiness；相反，当前机器门确实拒绝放行。这是本轮对“是否存在学术欺诈”的一个重要反证。

## 4. Major finding 1：GM-2 不是“待走流程”，而是已经出现实质语义冲突

### 4.1 提案的披露不够精确

提案第 204 行说“至少一条 implementer assessment 已标记 concern”。实际 artifact 中是**恰好 3/22 条**：

| Row | 方法路径 | 被否定字段 | 当前 implementer 状态 |
|---|---|---|---|
| `ABS2-cc432879fce4af753778` | DeepVerifier open-SFT variant | `external_component_weight_update=false` | `IMPLEMENTER_CONCERN` |
| `ABS2-7f79a2888c7d031e5e74` | DREAM PRM-guided search | `controller_program_or_config_optimized_on_labels=false` | `IMPLEMENTER_CONCERN` |
| `ABS2-c5351c607c4f37690a34` | DREAM PRM-guided search | `human_or_dev_label_model_selection=false` | `IMPLEMENTER_CONCERN` |

“至少一条”不是字面错误，但它降低了风险可见性。正式 round-15 必须写 `3/22 implementer concerns`，并逐条给出当前处置；不能用模糊量词隐藏确切分母。

### 4.2 DREAM 的两条 `false` 至少应判为 DISAGREE 或 UNRESOLVED

对 [A Reward-Guided Dual-Phase Framework for Adaptive Inference-Time Reasoning](https://aclanthology.org/2026.findings-acl.511/) 的冻结全文抽查得到：

- 主实验使用共享 32B reward model；
- 论文专门比较 7B 与 32B reward model，并报告 32B 持续更优；
- 搜索使用数据集特定阈值，例如 GSM8K 与 MATH 的高/低阈值不同；
- 论文报告有标签 accuracy 下的 threshold ablation。

这会直接挑战两个否定命题：

1. `controller_program_or_config_optimized_on_labels=false`：既然存在按数据集设置的阈值和有标签阈值消融，当前证据不足以证明 controller/config 从未利用标签结果优化。最保守也应是 `UNRESOLVED`，更强判断可能是 positive。
2. `human_or_dev_label_model_selection=false`：论文比较 7B/32B 并在主实验选用更强的 32B RM。除非能证明这一比较发生在冻结部署方案之后、且没有影响模型选择，否则“没有 human/dev 基于有标签结果选择模型”不能作为承重负结论。

这不是挑措辞，而是会改变 TF-Strict occupancy 的边界变量。独立 reviewer 不应为了达成 22/22 而填写 22 个 `AGREE`。

### 4.3 DeepVerifier 的第三条 concern 应保持未决，不能由实现者自行消除

对 [Inference-Time Scaling of Verification](https://aclanthology.org/2026.findings-acl.1243/) 而言，open-SFT variant 明确 fine-tune Qwen3-8B；争议在于 Qwen3-8B 是研究核心还是“外部组件”。如果方法路径的 core/peripheral 边界没有先定义稳定，`external_component_weight_update=false` 可以因为换拓扑解释而被人为维持。

必须先冻结该 method path 的核心拓扑，再判断更新发生在哪一侧。不能先看希望得到的 TF-Strict 结论，再反向命名 core。

### 4.4 本项的强制修复

- 独立 reviewer 对 22 条逐条填写 `AGREE|DISAGREE`，不得由实现者预填 reviewer row；
- DREAM 上述两条默认按 `DISAGREE` 处理，除非团队提供能排除 model/config selection 的全文级反证；
- 任一 `DISAGREE` 必须先改 owner sidecar/row 或降级为 unresolved，再重新生成 row hash；
- DeepVerifier 先冻结 core/peripheral topology，再裁决 weight-update 字段；
- 正式提案披露确切的 `3/22 concerns`、`0/22 reviewer rows` 和逐条处置；
- 只有修订后的 22/22 完成，才允许生成 fresh NT/POSIX v7 leaves 和 aggregate。

在这项闭合之前，GM-2 只能写：`contract machinery PASS; semantic truth NOT ESTABLISHED`。

## 5. Major finding 2：RQ 混合了 mapping 问题与 Stage-2 实证问题

### 5.1 RQ-SUPPLY 和 RQ-VERIFY 当前措辞不能由 Stage-1B 回答

提案的 RQ-SUPPLY 问“candidate pool 是否存在可测 oracle headroom”，RQ-VERIFY 问实际性能变化中多少来自 generator、verifier 和 selector。可是同一提案又正确规定 Stage-1B 不运行研究模型、不产生 headroom、WER、EM 或 prototype 结果。

这造成一个逻辑缺口：如果 RQ 指向本项目实际系统的 `H(c)` 和增益归因，它属于 Stage-2；如果 RQ 只是调查既有论文如何定义、测量或混淆这些量，就必须改写为 mapping RQ。

建议拆成两层：

| 层级 | Stage-1B 可回答的问题 | 后续实证问题 |
|---|---|---|
| Supply | 既有研究如何构造 candidate supply；是否报告同池 oracle/headroom；供给变化是否被记录 | 本项目在固定 `c` 下是否存在 `H(c)` |
| Verification | 既有研究是否把 generator coverage、verifier discrimination、selector action 分开；用了哪些对照 | 本项目的变化中分别有多少来自三者 |
| Baseline | 文献是否使用等 K MBR、oracle upper bound、regret 等 | 本项目实际 `delta_mbr/regret/rho_*` |
| Boundary | 文献中哪些结果依赖 label、weight update、new info、white-box state | 选定方案是否在冻结边界内成立 |

每个 RQ 和 H1–H5 都应新增：`answering_stage`、`Stage-1B evidence product`、`later empirical test`、`falsifier` 四列。这样 survey 不会假装回答尚未运行的实验问题。

### 5.2 Stage-1C 产出需要退回正确阶段

把 Stage-1B 的“3–5 张 candidate problem card”改为“问题卡 evidence bundles / eligible inputs”；把“直接 prior 的复现优先级”改为“direct-prior proximity 与 reproduction-readiness evidence”。最终 3–5 张卡、排序、唯一选题和复现清单冻结均留在 Stage-1C。

Stage-2 方法预告可以保留为边界声明，但不能细化成已经选定的实验方案或通过 Stage-1A 提前冻结预算 cap。本轮报告**不要求跑冒烟集，也不要求设置探索预算上限**。

## 6. Major finding 3：77 篇书目可回放，但“为什么是这 77 篇”仍不可审计

### 6.1 GM-1 的 PASS 是对七类已注册 active sources 的无损 union，不是全部历史语料的完备声明

当前 GM-1 对以下 source denominators 做 exactly-once routing：census 95、seed 92、bibliography 65、claim 62、version pin 30、fulltext event 129、reviewer-known 6，共 479 行，得到 241 个 work nodes。这是实质进步。

但仓内 archive 和早期 survey campaign 还有未进入这七类输入的文献。例如 [OmniGAIA](https://arxiv.org/abs/2602.22897) 已存在于历史 omni-agentic archive，却没有进入当前 241-node union 或 77-work bibliography。不能因此要求把 archive 中所有宽泛背景材料机械灌入当前 corpus；但必须二选一：

1. 把 GM-1 的表述严格收窄为“seven registered active corpora 的 lossless union”；或
2. 建立 archive corpus inventory/scope receipt，对历史 campaign 逐项给出 `CARRY_FORWARD|OUT_OF_SCOPE|SUPERSEDED|DUPLICATE|UNRESOLVED`。

在没有 archive scope receipt 时，“旧库/全部论文集已经充分利用”的泛化结论仍然过强。

### 6.2 241 → 77 存在新的 selection oracle

77 项的身份、作者和链接来自 official receipts，说明**元数据生成**可审计；但 `65 retained + 12 reviewer-directed additions` 不是一个科学的入选谓词。测试可以忠实地冻结一个有偏列表。

以下论文已经在 241-node union 中并被标为 `INCLUDE/KNOWN_QUEUE`，却没有出现在 77 项 reviewer bibliography：

| 已在本地 union 的工作 | 为什么与当前提案直接相关 |
|---|---|
| [Multi-Agent Verification](https://arxiv.org/abs/2502.20379) | 多 verifier、test-time compute 和 verifier aggregation，直接约束 RQ-VERIFY |
| [Thinking While Listening](https://arxiv.org/abs/2509.19676) | audio-domain test-time scaling，直接约束 H5 的 speech specificity |
| [Omni-Reward](https://arxiv.org/abs/2510.23451) | omni-modal reward modeling，直接约束 measurement/peripheral-trained boundary |
| [Native Active Perception as Reasoning for Omni-Modal Understanding](https://arxiv.org/abs/2606.19341) | omni agent 的主动感知与 observation/action 结构，直接约束 system-first topology |

这四项不一定都要成为 D2 blocker，但至少应在 reviewer-visible bibliography 中有显式 disposition。否则书目一方面声称系统主线闭包，另一方面隐藏本地 union 已知的直接邻居。

建议冻结一个可执行的书目选择谓词，而不是继续人工加项目：

```text
VISIBLE_BIBLIOGRAPHY =
  all load-bearing/D2 works
  OR all direct system neighbors
  OR all speech/omni measurement instruments
  OR all P1 reviewer-known threats
  OR all methods references governing mapping/search/review
```

对 241 项中不进入可见书目的 complement，至少给 reason-code 统计；不要求把 241 篇全部复制到正文。

### 6.3 外部 reviewer-known 补充：Llasa 至少应进入 P1 队列

[Llasa](https://arxiv.org/abs/2502.04128) 在 speech synthesis 中同时讨论 train-time 与 inference-time scaling，并在搜索时使用 speech-understanding models 作为 verifier。它并不直接证明本项目 novelty，也未必满足 TF-Strict，但它同时触及 speech、verifier 和 inference-time search 三条轴，是当前提案不能忽略的边界邻居。

该论文来自本次作者外 known-ID 核查，应登记为 reviewer-known、`query_recall_credit=false`，不能反向声称 frozen queries 已经召回它。

### 6.4 其他建议进入 Stage-1B 首批处置、但不阻塞 Stage-1A 方向成立的工作

- [OmniGAIA](https://arxiv.org/abs/2602.22897)：native omni-modal agent benchmark/system neighbor；当前历史 archive 已知但未进 active union。
- [Omni-RRM](https://arxiv.org/abs/2602.00846)：trained omni reward modeling；适合 measurement instrument / boundary comparator。
- [Multimodal RewardBench 2](https://arxiv.org/abs/2512.16899)：omni reward model 的测量有效性与 judge failure，适合 RQ-VERIFY/RQ-BOUND。

这些项目应通过正常的 reviewer-known/carry-forward 入口进入，而不是改 frozen query 或伪装成 query hit。

## 7. Major finding 4：缺少 systematic mapping 的方法学引用

提案和 current protocol 大量使用 systematic mapping、PRESS review、snowballing、exit mechanism、双人编码和可回放检索等概念，但正式 bibliography 没有对应的方法学依据。对于一份申请开展 Stage-1B systematic mapping 的提案，这不是装饰性缺失，而是会影响流程选择是否合理。

至少应建立独立的 methods bibliography，并明确“采纳了什么、没有采纳什么、为什么”：

- Petersen et al., *Systematic Mapping Studies in Software Engineering*，[EASE 2008 / DOI](https://doi.org/10.14236/ewic/EASE2008.8)：用于说明 mapping 与 focused systematic review 的目标、分类和产出差异；
- Wohlin, *Guidelines for Snowballing in Systematic Literature Studies and a Replication in Software Engineering*，[DOI](https://doi.org/10.1145/2601248.2601268)：用于约束 backward/forward snowballing 与停止；
- Page et al., *The PRISMA 2020 statement*，[BMJ](https://www.bmj.com/content/372/bmj.n71)：用于 flow、排除理由和透明报告；
- McGowan et al., *PRESS Peer Review of Electronic Search Strategies: 2015 Guideline Statement*，[PubMed](https://pubmed.ncbi.nlm.nih.gov/27005575/)：用于给“PRESS review”一个真实、可核验的操作依据；
- 如要报告数据库/网站检索的完整细节，可补 PRISMA-S，而不是只借用 PRISMA 名称。

不要求机械照搬医学综述流程。需要的是一张 adaptation table：`method guideline → adopted element → adaptation for AI/CS/arXiv/T1 → deviation and rationale → artifact`。否则“PRESS”“systematic”只是内部标签，无法让外部审稿人判断设计充分性。

## 8. Major finding 5：speech/omni specificity 假设尚未被 codebook 操作化

H5 提到实时性、长序列、音频证据、turn-taking 和工具编排，但提案第 137 行列出的编码字段主要是 core topology/native modality、visibility、updates、signals、control horizon、decision rights 和 candidate pool。仅有 `native modality` 不足以回答 H5。

Stage-1B codebook 至少需要以下可编码维度：

| 维度 | 最小分类建议 | 为什么必要 |
|---|---|---|
| modality topology | native audio / ASR-text cascade / audio tool / hybrid | 防止把“输入里有音频”误当原生 omni control |
| temporal regime | offline / streaming / full-duplex / interruptible | H5 的实时性和 turn-taking 否则不可见 |
| observation granularity | utterance / frame/chunk / event / tool result | 判断控制器在何时获得什么证据 |
| acoustic evidence provenance | task-provided / read-out transform / external new info | 对齐信息边界 |
| latency and action timing | pre-generation / mid-generation / turn-level / terminal | 区分在线控制和终端 reranking |
| output/action modality | text / speech / multimodal / tool / environment action | 判断系统是否真是 omni agentic |
| state persistence | none / within-turn / cross-turn / external memory | 连接 control plane 与 agent system |

这些字段是在 Stage-1B “看论文和编码”，不是运行模型，因此不构成实验越界。若不补，H5 只能成为讨论段落，不能产生 systematic mapping 证据或可证伪的 Stage-1C 问题卡输入。

## 9. Major finding 6：正式证据包还没有绑定检索设计的全部承重输入

目标稿的 §19 绑定了 thesis、objective、旧 proposal/review、union、receipt、bibliography、旧 aggregate、query bytes、attempt registry 和事故记录；但正式 search-design signoff 还需要同一提交下的：

- current protocol；
- current status/README；
- current manifest；
- query compiler 及 compiler profile；
- exact T1 routes 和 wordlist；
- REC-0 至 REC-7 schemas/templates；
- inclusion/exclusion、D0/D1/D2、dual-coding/adjudication 合同；
- exit/reopen/amendment mechanism；
- fresh negative-evidence artifact；
- fresh NT/POSIX leaves 与 aggregate；
- proposal source manifest 和 package gate report。

当前 `wiki/survey/current/manifest.json` 仍把 round-12 correction 作为 active review transaction，并主要绑定 evidence-v6/context-v1；这不是未来 round-15 的 source manifest。目标稿第 8、267 行已经承认 source manifest/package gate 尚待生成，因此这里不是指控隐瞒，而是说明现在确实不可签署。

正式提案正文还应放一张紧凑的 search-design 表，至少包含 databases/routes、时间窗、语言/文献类型、inclusion/exclusion、screening、全文深度、编码者/裁决者、quality/evidence grade、exit/reopen 和 exposure。不能要求独立 reviewer 从数百行 protocol 自行拼出承重设计。

## 10. 引用是否合理

### 10.1 可以接受的部分

- 提案没有提出 `first-ever`、已确立 novelty 或已超过 SOTA；
- 第 44 行关于“相邻 speech/omni agent、工具编排和 trained speech reward 已存在”的弱存在性陈述，可由列出的 official identities 支持；
- 深读论文与 known queue 被区分，known-ID metadata access 不冒充 query recall；
- DREAM/DeepVerifier 等承重路径有本地全文和 SHA，而不是仅凭搜索摘要。

### 10.2 仍需修复的部分

1. **元数据身份不能支持机制结论。** 多数 direct neighbors 仍为 `KNOWN_QUEUE` 或 `BOUNDARY_COMPARATOR`，只能支持“该工作存在并值得路由”，不能支持它满足 TF-Strict、占据某个 cell 或证明创新空白。
2. **书目入选规则不可审计。** official receipt 修复了 citation oracle，却没有修复 selection oracle。
3. **方法学引用缺失。** 对 systematic mapping 提案而言是结构性缺口。
4. **年份策略混杂。** bibliography generator 对 arXiv OAI 使用 `<created>` 年份，而 OAI `<created>` 可能反映后续版本/元数据创建，不是首次 preprint 年份。例如：
   - AudioToolAgent 显示 2026，但 arXiv 首次提交为 2025-10-03；
   - VoiceAgentBench 显示 2026，但首次提交为 2025-10-09；
   - LATS 显示 2024，但 arXiv ID 和首次提交为 2023；
   - PiCSAR、Trajectory Optimal Control 均显示 2026，但首次提交分别在 2025-08、2025-09。

这不必被定性为伪造，因为部分工作可能有 2026 正式 venue；但当前“Official citation”没有说明年份取值规则。应为每条记录明确 `year_basis = initial_preprint | formal_venue | current_version`。若用 formal venue year，就应绑定 venue identity；若只引用 arXiv，应默认首次提交年。

## 11. 研究范畴是否超越当前阶段

| 项目 | 裁决 | 说明 |
|---|---|---|
| 执行 query/crawl | 未越界 | 本轮为 0；必须继续保持到授权 |
| 模型调用/smoke | 未越界 | 本轮为 0；Stage-1B 也全程禁止 |
| headroom/WER/EM/prototype | 未越界 | 仅作为未来度量预告，没有结果 |
| Stage-2 复现说明 | 可保留 | 只要明确为 preview，不形成执行承诺 |
| Stage-1B 产出问题卡 | 轻度越界 | 应退回 Stage-1C，Stage-1B 只交 evidence inputs |
| RQ-SUPPLY/RQ-VERIFY | 阶段错配 | 当前措辞像 Stage-2 实证 RQ，需改成 mapping RQ + future empirical RQ |
| 预算 cap | 不应新增 | 当前仍需要广度探索；本报告不要求前期预算封顶 |

因此，问题不是“团队偷跑了 Stage-2”，而是文档中有少量职责和问题措辞跨阶段。修复应通过改写协议职责完成，不需要跑任何实验。

## 12. 学术诚信与“是否涉嫌造假”的判断

### 12.1 当前没有足够证据指控 fabrication、falsification 或 plagiarism

没有发现捏造实验结果，因为本轮根本没有宣称模型实验；没有发现伪造 Stage-1B 已启动；没有隐藏 429、历史 exposure 或 wiki dry-run 事故；机器 release checker 也主动拒绝通过。这些行为与蓄意造假并不相符。

### 12.2 但有四类必须在现在消除的诚信风险

| 风险 | 当前等级 | 可能演化成什么问题 |
|---|---|---|
| 否定性编码与原文冲突 | 高 | 若明知 DREAM 证据仍强行填 `AGREE`，将接近 falsification/biased coding |
| 77 项书目选择规则不透明 | 中高 | 可形成 cherry-picking：保留支持 system-first 的邻居、淡化反例 |
| `draft PASS` 与 scientific signoff 混淆 | 中 | 可形成 false assurance，但当前文档已主动区分，风险受控 |
| citation year policy 不明 | 中低 | 可造成元数据误引和时间线误判，现阶段可纠正 |

还应监控 HARKing 风险：H1–H5 可以作为 Stage-1A hypothesis，但必须保存提出时间、与 frozen query 的关系和失败条件；Stage-1B 看完结果后不能悄悄改写成“从一开始就预测正确”。若需要修改，应走 dated amendment 并说明由什么证据触发。

本轮最严厉但准确的表述应是：**没有发现学术欺诈事实；已经发现两个能导致有偏编码的实质冲突，以及一个能导致选择性引用的结构漏洞。若团队在收到本报告后仍用自动 PASS 或模糊措辞覆盖这些冲突，风险性质才会升级。**

## 13. 交给研究团队 AI 的强制整改 proposal

以下顺序不可颠倒；任何一项都不授权执行 systematic query 或研究模型。

### P0-1：先纠正 GM-2 语义，不追求“漂亮的 22/22”

交付：

- 独立 reviewer 的 22 行 adjudication；
- 三条 implementer concern 的显式表；
- DREAM 两条冲突的全文 locator、reviewer verdict 和 owner-sidecar correction/downgrade；
- DeepVerifier core/peripheral topology 冻结说明；
- 修订后 exact row hashes 和 contradiction log。

验收：任何 `DISAGREE` 都已反映到上游编码；不存在 reviewer/coder actor collision；不存在以 `not mentioned` 证明 absence。

### P0-2：分离 mapping RQ 与 empirical RQ

交付：一张 `RQ/Hypothesis × answering stage × evidence product × falsifier` 表。

验收：Stage-1B 的每个问题都能只靠论文检索、筛选、编码和综合回答；任何需要本项目模型输出、gold utility、headroom 或 causal ablation 的问题明确路由至 Stage-2。

### P0-3：修正 Stage-1B/1C 交付边界

交付：

- Stage-1B：evidence map、occupancy/unresolved、negative prior/falsifier、direct-prior proximity、candidate-card inputs；
- Stage-1C：3–5 candidate cards、最终排序、owner 唯一选题、复现清单冻结。

验收：Stage-1B 不出现 owner selection 或“为候选拉票”的临时实验。

### P0-4：补书目选择谓词、archive scope receipt 和方法学引用

交付：

- 241 → visible bibliography 的可执行/可人工复核选择规则；
- complement reason-code 统计；
- archive campaign inventory 或严格收窄的 GM-1 claim；
- 对 MAV、Thinking While Listening、Omni-Reward、Native Active Perception、Llasa 的显式 disposition；
- systematic mapping methods bibliography 与 adaptation table；
- `year_basis` 字段和五项已知年份错配的修正。

验收：不能再用“65+12”作为唯一选择理由；metadata receipt PASS 与 scientific coverage PASS 分开报告。

### P0-5：把 H5 变成可编码合同

交付：speech/omni-specific codebook fields、允许值、unknown/NA 规则、双人分歧处理和至少 3 个纸面 calibration examples。

验收：只看编码表即可区分 native audio、ASR cascade、streaming/full-duplex、终端 reranking 与在线 control；不运行模型。

### P0-6：形成同一提交下的正式 source manifest/package

交付：绑定 protocol/status/manifest/compiler/T1 routes/REC schemas/exit mechanism/GM-2 修订物/提案的 exact commit、Git blob 与 SHA-256。

验收：proposal 的紧凑 search-design 表与 source manifest 一致；当前 round-12 active transaction 已被新的正式 transaction 合法 supersede，而不是静默覆盖。

### P0-7：最后才生成平台证据与提交复审

顺序：

1. GM-2 修订完成；
2. 在 exact package 上生成 fresh Windows leaf；
3. 在同一 exact package 上生成 fresh WSL2/POSIX leaf；
4. 独立 aggregate 校验两叶 exact bytes；
5. package gate PASS；
6. promote 为 immutable round-15 submission；
7. 由未参与实现的 reviewer 写 round-16 report；
8. reviewer `SIGN` 后，owner 对同一 package 单独决定是否授权 Stage-1B。

任何一步失败，都不得“先开 Stage-1B，之后补材料”。

## 14. Stage-1B 开门检查点

| Gate | 当前状态 | 开门要求 |
|---|---|---|
| 科学动机 | `REVISE` | RQ 分层、H5 操作化、Stage-1C 职责归位 |
| GM-1 active union | `PASS_WITH_SCOPE_QUALIFIER` | 明确七类 active sources 边界或补 archive scope receipt |
| GM-2 contract machinery | `PASS` | 保留 |
| GM-2 semantic truth | `FAIL/PENDING` | 22/22 独立复核；两条 DREAM 冲突被更正/降级 |
| GM-3 code/DAG | `PASS` | 保留 |
| GM-3 formal leaves/aggregate | `MISSING` | 在 GM-2 修订后的同一提交生成 |
| GM-4 identity receipts | `PASS` | 保留离线重建与 access ledger |
| GM-4 scientific coverage | `REVISE` | 选择谓词、直接遗漏、方法引用、年份政策 |
| formal round-15 package | `MISSING` | immutable proposal + source manifest + package gate |
| independent search-design signoff | `WITHHOLD` | 对 exact package 给 SIGN，而不是签代码片段 |
| owner authorization | `MISSING` | reviewer SIGN 之后单独发生 |

### 最终开门判据

只有以下合取式为真，才可以执行第一条 Stage-1B query：

```text
GM2_SEMANTIC_ADJUDICATION_CLOSED
AND ALL_UPSTREAM_CORRECTIONS_REBOUND
AND RQ_STAGE_SPLIT_ACCEPTED
AND STAGE1B_1C_OUTPUT_BOUNDARY_FIXED
AND BIBLIOGRAPHY_SELECTION_AND_METHODS_CLOSED
AND SPEECH_OMNI_CODEBOOK_OPERATIONAL
AND SAME_COMMIT_SOURCE_MANIFEST_PASS
AND NT_LEAF_PASS
AND POSIX_LEAF_PASS
AND AGGREGATE_PASS
AND FORMAL_ROUND15_REGISTERED
AND INDEPENDENT_REVIEWER_SIGNED_EXACT_PACKAGE
AND OWNER_AUTHORIZED_EXACT_PACKAGE
```

## 15. 给独立 reviewer 的下一轮明确判词

下一轮不应被要求在一个动作里同时“修数据、签设计、授权执行”。正确职责分离是：

1. semantic adjudicator 判断 22 条负证据；
2. implementer 根据 `DISAGREE` 修上游资产；
3. machine gate 检查绑定和双平台一致；
4. independent reviewer 审查科学理由与 search design；
5. owner 最后决定是否执行 Stage-1B。

本轮不能给出的判词：

```text
SEARCH_DESIGN_SIGNOFF = SIGN
STAGE_1B = START
```

本轮可以给出的判词：

```text
THE_SYSTEM_FIRST_DIRECTION_IS_WORTH_CONTINUING
THE_DRAFT_IS_MATERIALLY_MORE_HONEST_AND_REPLAYABLE
THE_CURRENT_PACKAGE_IS_NOT_READY_FOR_FORMAL_SIGNOFF
STAGE_1B_REMAINS_UNSTARTED_AND_UNAUTHORIZED
```

## 16. 终局评价

这份提案已经从“试图证明自己 ready”进步到“允许红门真实存在”，这是研究治理上的正向变化。其中心问题——冻结黑盒 omni 核心，由 reward-guided external control plane 在不改权重、不改结构的前提下组织观察、供给、记忆、工具、验证、选择和停止——具有足够的博士研究价值，值得继续 systematic mapping。

但博士级标准不能只问“方向有没有意思”，还必须问：证据能否推翻自己的期望、全集如何进入可见书目、每个 RQ 在哪个阶段能被回答、以及谁有权签署什么。当前最关键的反例已经来自团队自己的 GM-2 artifact 和 DREAM 原文；如果不先处理这两个冲突，任何 22/22、aggregate PASS 或 bibliography PASS 都只是程序完备性，不是科学有效性。

因此最终意见是：**要求 major revision；继续 Stage-1A final remediation；暂缓 search-design 签署；不得进入 Stage-1B。**
