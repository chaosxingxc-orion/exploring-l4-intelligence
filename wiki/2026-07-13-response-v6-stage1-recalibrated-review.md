---
title: "Response v6 与 A-SEL 当前工作的 Stage-1 校准对抗审查"
date: 2026-07-13
review_id: "W1-ASEL-STAGE1-RECALIBRATED-ADR-2026-07-13"
stage: "1-problem-definition"
status: "MAJOR_REVISION_FOR_STAGE1_CLOSURE / DIRECTIONAL_EXPLORATION_MAY_CONTINUE"
scope: "Response v6、A-SEL v0.1 草稿、Stage-1 问题定义与原型探索、研究诚信记录"
recalibrates: "2026-07-13-response-v6-doctoral-adversarial-review.md；仅校准阶段门，不撤销其中已核实的文件级事实"
reviewed_response_snapshot: "commit 311689818e6650674fac2cc1c19dbe4ee94baa29 / sha256 beddc2609ddbddfb8943048df6301e024f58f2dc8f666109efc5ae5dc5117146"
reviewed_asel_snapshot: "commit 84c6cf64d0a979a5d4f8222a00b9eb746378f270 / sha256 300ccfb24006b2b49aeafbc16db7fecede5ccd2b766d58339bca5f3c75abeefa"
reviewed_prior_review_snapshot: "uncommitted review artifact / sha256 f5ad16e39da38b9de1f59147b019126f63cf825672b3d7682306e944acee70f5"
integrity_verdict: "NO_FFP_ESTABLISHED / RECORD-CONTROL_QRP_RISK_MODERATE_TO_HIGH / TARGETED_FORENSIC_CHECKS_REQUIRED"
authorizes: "survey、静态审计、合成测试、固定小样本 directional-only 原型；不授权把任何 Stage-1 数字升级为确证结论"
---

# Response v6 与 A-SEL 当前工作的 Stage-1 校准对抗审查

## 0. 校准后的总裁决

### 0.1 一句话裁决

**团队没有因为尚未冻结 SESOI、Holm、精确 N\*、最终任务卡或完整独立复现而“做错 Stage-1”；上一版审查在这些项目上把 Stage-2/论文标准前移了。** 但团队目前仍未完成高质量的 Stage-1 收官：A-SEL 已被 owner 选为唯一 headline，却尚未被压缩成一个经直接近邻 survey、原型族横向探索和新颖性击杀测试后仍然成立的**具体研究问题**；与此同时，v6 的 provenance 与机读格式错误是阶段无关的真实记录缺陷，必须修复。

### 0.2 四项独立判定

| 对象 | 校准后判定 | 解释 |
|---|---|---|
| Response v6 的实质态度 | **ACCEPT_WITH_RECORD_REPAIR** | 13 项基本采取 ACCEPT、开放项没有被强行写成科学通过，也未申请立即重签；方向正确。 |
| Response v6 的记录质量 | **MAJOR REPAIR REQUIRED** | 被回复报告 hash 写错、`this_response_snapshot` 指向父提交、13 个 YAML 项因重复键只可稳定解析出 2 个。 |
| A-SEL 作为 Stage-1 工作假设 | **CONDITIONALLY VIABLE** | 方向值得探索；oracle headroom、equal-K、reward-guided selection、Goodhart 风险均是合理问题材料。 |
| A-SEL 作为已经完成的问题定义/Stage-2 入口 | **NOT READY** | 同构 ASR 文献覆盖不足、科学对象仍是家族、ρ 名称与对象漂移、原型选择依据和失败路线没有形成闭合的 Stage-1 decision package。 |

### 0.3 允许与禁止

当前**允许继续**：

- 文献 survey、代码/数据静态盘点、合成数据单元测试；
- 小样本、固定预算、单次触碰的方向性原型；
- 同一小样本上并列比较多个候选 proxy/selector，前提是全景登记，不做 winner-only 汇报；
- 使用公开/dev 数据做可行性和失败模式探索；
- 根据方向性证据迭代方法，但每次分支、废弃原因和结果必须追加记录；
- 为后续 owner 讨论准备科学问题选项，不要求现在冻结确证统计机械。

当前**禁止**：

- 把小样本效应、置信区间或相关系数写成 A-SEL 已有效的科学结论；
- 把当前文档称为已经进入 `Stage 2`，或用 `confirmatory` 描述仍会迭代的原型；
- 只报告最后胜出的 selector，而不披露同一数据上试过的 proxy、prompt、K、阈值与失败分支；
- 让 golden transcript/answer/qrel 进入 selector、reward、检索或候选构造路径；
- 把“存在 oracle headroom”误写为“团队方法能兑现 headroom”；
- 在直接近邻尚未比较前，把普通 N-best reranking/reference-free quality estimation 重新命名为新的 training-free RL 问题。

### 0.4 Stage-1 与 Stage-2 的正确分界

| 现在必须做到（Stage-1） | 可以留到 fresh Stage-2 proposal |
|---|---|
| 明确到底研究哪个问题，为什么现有工作未解决 | 精确 SESOI 数值与外部锚定档案 |
| 覆盖直接近邻、方法祖先及跨模态类比 | 最终 primary family、alpha、Holm 和 CI 形式 |
| 画出 selector/proxy 原型空间，并说明探索逻辑 | 确证样本量、power、精确 N\* |
| 用廉价小样本检查“可做/值得做/失败在哪里” | 完整 group-level inferential design |
| 固定信息边界，保留所有尝试与负结果 | 最终唯一算法对象及全部超参数 |
| 统一构念与指标名称，避免 ρ 偷换对象 | 全部 task card、最终公平性协议 |
| owner 基于 survey + 原型包选择一个具体问题 | 强独立复现、一次性 confirmatory fire |

这与 pilot/feasibility 方法学一致：小样本探索的主要问题应是“能不能做、是否应继续、怎样做”，而不是把一个无力检验主假设的小实验包装成主试验。相关方法学综述明确批评 pilot 研究不恰当地强调假设检验，并把 feasibility 概括为 “can it be done, should we proceed, and if so, how”。参见 [Arain et al., 2010](https://pmc.ncbi.nlm.nih.gov/articles/PMC2912920/) 与 [Eldridge et al., 2016](https://pmc.ncbi.nlm.nih.gov/articles/PMC4792418/)。

## 1. 审查对象、证据边界与快照

### 1.1 主对象

1. `wiki/2026-07-13-response-v6-to-signoff-adversarial-review.md`
   - Git commit：`311689818e6650674fac2cc1c19dbe4ee94baa29`
   - SHA-256：`beddc2609ddbddfb8943048df6301e024f58f2dc8f666109efc5ae5dc5117146`
2. `wiki/2026-07-13-stage2-proposal-ASEL-v0.1-for-reviewer-verification.md`
   - Git commit：`84c6cf64d0a979a5d4f8222a00b9eb746378f270`
   - SHA-256：`300ccfb24006b2b49aeafbc16db7fecede5ccd2b766d58339bca5f3c75abeefa`
3. 上一版严格审查：`wiki/2026-07-13-response-v6-doctoral-adversarial-review.md`
   - SHA-256：`f5ad16e39da38b9de1f59147b019126f63cf825672b3d7682306e944acee70f5`
   - 本报告不覆写它，只对其 stage-misaligned findings 重新分级。

### 1.2 本轮不做的事

- 不修改团队正在进行的 proposal、代码、配置、登记册或数据；
- 不把“尚未达到论文级证据”当作 Stage-1 失败；
- 不重新跑大规模 GPU 实验；
- 不因文档错误直接推定作者具有欺诈故意；
- 不代替 owner 选择 A-SEL 内部的最终科学子问题。

### 1.3 评价问题

本轮只问五个 Stage-1 问题：

1. 团队是否准确描述了问题空间与直接近邻？
2. A-SEL 是否已经具体到能被 owner 选择，而不是一个容纳任意 selector 的标签？
3. 原型探索能否区分“不可做、可做但不新、可做且可能新”三种状态？
4. 所有 Stage-1 结果是否保持 directional-only，且不存在 gold 泄漏、winner-only 或事后改写？
5. 记录错误是否只是可纠正的控制缺陷，还是已经有 fabrication/falsification/plagiarism 的实证？

## 2. 七轮 Stage-1 对抗式评审

### Round 1：最大善意评审——如果它只是探索方案，团队做对了什么？

通过项：

- v6 没有把全部开放项伪装成 CLOSED，也没有要求立即重签；
- A-SEL 草稿明确写了 `DRAFT / NOT-FROZEN / authorizes no data-sensitive work`；
- 草稿把既有小样本数字标为 `hypothesis-grade / directional-only`；
- 团队已经把 `pool-mean`、MBR、pessimistic selector、greedy、oracle 列入候选 comparator；
- 信息边界明确禁止 gold 进入 selector/reward 路径；
- 对 Goodhart、同模型 verifier 假独立、跨 split 泄漏、公开 benchmark 适应等风险已有意识；
- owner 选择 A-SEL 为 headline、把 RDU 降为 secondary，避免同时追逐多个旗舰问题。

结论：**这不是一个应该被“整篇拒稿”的 Stage-1 包；它有继续探索的合理基础。**

### Round 2：问题定义红队——A-SEL 到底是问题，还是一个大伞标签？

当前 A-SEL 同时可能指：

- 从 N-best 中选一个输出；
- 用 reference-free quality estimator 排序；
- 用音频—文本一致性 reward 选轨迹；
- 用多个 verifier 做 pessimistic/hedged selection；
- 随 K 增长检测 reward overoptimization；
- 在 ASR、spoken QA、retrieval QA 上使用同一框架；
- 把任意上述过程称作 training-free RL。

这些不是一个问题，而是至少六个相互交叉的问题。Stage-1 可以保留它们作为候选空间，但不能同时把这个空间称为已经关闭的科学身份。

**红队问题**：如果把术语 `A-SEL` 和 `training-free RL` 去掉，剩下的科学问题是否仍能用一句可证伪、可与最近邻区分的话表述？当前答案仍不充分。

### Round 3：近邻 survey 红队——团队是否把方法祖先当成“背景”略过了？

是。A-SEL 的最直接祖先不是通用 RL/BoN 文献，而是 ASR N-best selection、MBR、confidence estimation、reference-free error estimation、rescoring 与 hypothesis revision：

- [Stolcke et al., 1997](https://www.isca-archive.org/eurospeech_1997/stolcke97_eurospeech.html)：在 N-best 中显式最小化期望 WER；
- [Goel & Byrne, 2000](https://www.sciencedirect.com/science/article/pii/S0885230800901384)：minimum Bayes-risk ASR 与 N-best 近似；
- [Wu et al., 2022](https://www.isca-archive.org/interspeech_2022/wu22_interspeech.html)：融合 acoustic/text 信号的 BERT confidence 与 learning-to-rank rescoring；
- [NoRefER, 2023](https://www.isca-archive.org/interspeech_2023/yuksel23_interspeech.html)：reference-free ASR quality metric；
- [HypR, 2024](https://www.isca-archive.org/interspeech_2024/wang24j_interspeech.html)：明确把 hypothesis revising 分成 N-best reranking 与 error correction，并提供多语料、每句 50 hypotheses 的比较基准；
- [ProGRes, 2024](https://arxiv.org/abs/2409.00217)：LLM zero-shot N-best rescoring 与扩展候选；
- [Shu et al., 2024](https://www.isca-archive.org/interspeech_2024/shu24_interspeech.html)：同时利用 acoustic 与 confidence reference；
- [READ, 2026](https://arxiv.org/abs/2606.04680)：training-free、reference-free、直接用音频 discrepancy 评价并改进 ASR hypotheses。

通用 reward optimization 仍然重要：[Gao et al., 2023](https://proceedings.mlr.press/v202/gao23h.html) 直接展示 imperfect proxy 下 RL 与 best-of-N 都会发生 reward overoptimization。但它不能替代上述语音领域最近邻。

结论：**“label-free reward-guided selector”本身不是可信的新颖性 delta。** 潜在 delta 必须落在：冻结 omni 的特定可读信号、跨任务约束、equal-K 的严格部署比较、可检测的 Goodhart breakpoint、abstention/hedging，或这些元素的某个非平凡组合。

### Round 4：原型空间红队——团队是否过早爱上了一个方案？

有这个风险。当前草稿花了大量篇幅设计 future confirmatory gates，却没有给出一个 Stage-1 prototype matrix，说明为什么应优先探索某类 reward、哪些替代路线被尝试过、失败意味着什么。

Stage-1 不要求冻结唯一 selector；恰恰相反，它应当显式保留多个候选。真正的问题是：

- 所有候选是否在同一固定小样本、同一 K、同一候选池上并列出现？
- 是否记录每个候选的成本、信号、失败模式和废弃理由？
- 是否把最强近邻作为“新颖性击杀器”，而不是等到 Stage-2 才补的 secondary comparator？
- 是否存在因为某个 proxy 在小样本上好看，才事后把它写成 A-SEL 定义的风险？

### Round 5：构念红队——ρ 是否被悄悄换了定义？

Decision Log / Project Thesis 中的 ρ 是：

`rho_greedy = (R_selector - R_greedy) / (R_oracle - R_greedy)`。

当前 A-SEL 草稿的主要对照更接近：

`rho_pool = (R_selector - E[R_pool]) / (R_oracle - E[R_pool])`。

两者都可以在 Stage-1 探索，但它们回答不同问题：

- `rho_greedy`：相对部署默认输出，兑现了多少 oracle headroom？
- `rho_pool`：相对随机/池均值，兑现了多少候选池可选空间？

**允许并列，不允许同名。** 当前问题不是未冻结最终 estimand，而是已有名字把两个构念混在一起，导致 owner 以为选择的是 A、草稿实际测的是 B。

### Round 6：诚信红队——记录缺陷是否足以推断作假？

不够。fresh 核验仍确认：

1. v6 frontmatter 中 `reviewed_snapshot_responded_to` 没有写入被回复审查报告的实际 SHA-256。实际审查报告 hash 为 `64389f7fee45ea2aad4c9880fffe9293b621e52c492b79eca28d206290f761cf`；
2. `this_response_snapshot: umbrella 7b895b5` 不可能标识 v6 本身，因为 v6 直到 `3116898...` 才进入 Git；
3. v6 有两个 YAML 块，分别含 7 和 6 个字面 `response_item:`，但重复顶层 key 使 PyYAML 每块只保留最后一项，最终稳定存活的只有 `F-S7` 和 `M-S6`。

这些是严重的 record-control defect；它们可以造成审查对象混淆和自动审计失效。但当前证据还没有显示：

- 数据或运行日志是凭空制作的；
- 团队改动/删除了不利结果以歪曲研究记录；
- 引用了他人思想而不署名；
- 作者明知 hash 错误仍用其制造一个不存在的验证链。

因此，按 [ORI 定义](https://ori.hhs.gov/definition-research-misconduct)，当前不能成立 fabrication、falsification 或 plagiarism。ORI 也明确区分 honest error 与 misconduct。更合适的判定是：**QRP/有害研究实践风险中高，但 FFP 未成立。**

### Round 7：博导决策红队——现在能否结束 Stage-1？

不能仅凭 owner 已写下 “A-SEL 唯一 headline” 就自动结束。owner 裁决是必要条件，但高质量 Stage-1 收官还应给 owner 一个足够清楚的选择包：

- 直接近邻到底解决到了哪里；
- A-SEL 内部哪一个子问题仍有价值；
- 哪些廉价原型支持“可做”，哪些结果支持“不要做”；
- 哪些路线被明确丢弃，为什么；
- 未来 Stage-2 最小可主张的 claim 是什么；
- 如果最强近邻打平或更强，A-SEL 是 kill、pivot 还是降为 engineering study。

当前 owner 决策更像**工作方向选择**，还不是充分信息下的**问题定义收官决策**。

## 3. 对上一版审查发现的 Stage-1 重新分级

| 上一版 finding | 新分级 | Stage-1 处理 |
|---|---|---|
| R6-M1：被回复报告 hash 错 | **保留 MAJOR** | 阶段无关；出 append-only correction。 |
| R6-M2：response snapshot 指向父提交 | **保留 MAJOR** | 阶段无关；把“证据快照”和“回复工件快照”拆开。 |
| R6-M3：重复 YAML key | **保留 MAJOR** | 改为 `response_items: [...]`，schema validate。 |
| R6-M4：canonical status 未同步 headline | **降为 MINOR/记录同步** | 不阻断小型方向性探索；在 Stage-1 closure memo 中统一即可。 |
| F-D1：直接 ASR selector survey 缺失 | **保留 FUNDAMENTAL** | 这是 Stage-1 的核心，而非 Stage-2 细节。 |
| F-D2：pool-mean 主对照、最强近邻 secondary | **改写为 STAGE1-MAJOR** | 现在不要求最终 primary comparator；要求在 prototype matrix 中同台比较并执行 novelty kill。 |
| F-D3：ρ 对象漂移 | **保留 MAJOR** | 可探索双 ρ，但必须拆名、拆解释。 |
| F-D4：selector 是巨大搜索家族 | **改写为 STAGE1-MAJOR** | 家族开放在 Stage-1 合理；缺陷是没有家族地图、探索顺序与废弃日志。 |
| F-D5：跨任务共用 SESOI | **DEFER TO STAGE2** | Stage-1 用各任务原生效用和描述性归一化即可，不必现在造统一 SESOI。 |
| M-D1：H/CI/双侧规则不一致 | **DEFER TO STAGE2** | 只要当前不称 confirmatory。 |
| M-D2：Template §4 完整映射 | **DEFER TO STAGE2** | Stage-1 只需可重放原型，不需论文级独立验证链。 |
| M-D3：`stage=2`/`confirmatory` 与实际冲突 | **保留 MAJOR** | 这是阶段身份错误，应改为 Stage-1 exploration / pre-Stage2 blueprint。 |
| M-D4：N\* 的精确冻结时点 | **DEFER TO STAGE2** | Stage-1 只探索 K—proxy—U 曲线和潜在拐点。 |
| M-D5：P-corr/P-sim 尚非确定算法 | **DEFER TO STAGE2** | Stage-1 可比较多种实现，但须登记。 |
| M-D6：完整 task cards 不足 | **部分保留** | 现在只需任务族、效用、group key、信息边界的粗卡；精确卡留到 Stage-2。 |
| M-D7：最终 baseline 公平性 | **部分保留** | Stage-1 要可运行、同池、equal-K；训练历史的终局公平性论证留后。 |
| M-D8：所有原型都需独立复现 | **明显降级** | 不要求每个探索分支第三方复现；Stage-1 收官前至少一次 clean replay + 完整尝试账。 |

## 4. 校准后仍然成立的 Stage-1 findings

### S1-F1（FUNDAMENTAL）：直接近邻 survey 尚不足以支持问题定义关闭

**事实**：A-SEL 草稿的 survey 叙述主要沿用通用 preregistration、Goodhart、检索/语音 RAG 文献；没有把经典 MBR、NoRefER、HypR、ASR LTR/rescoring、READ 做成结构化最近邻表。

**风险**：团队可能花数月实现一个已有成熟命名和基线的 ASR reranker，却在最后才发现新颖性不足。

**关闭条件**：完成 §7 的 Survey Coverage Gate，不是简单增加引用数量，而是回答每个近邻与 A-SEL 的输入、监督、是否训练、是否看音频、选择对象、预算、公平比较和已知失败。

### S1-F2（FUNDAMENTAL）：A-SEL 仍未压缩成一个可选择的科学子问题

建议把当前宽泛 headline 保留为 umbrella，但要求 owner 在以下三个身份中选择一个，或明确写出第四个：

| identity | 新颖性前景 | 主要击杀器 |
|---|---|---|
| I1：一般 label-free N-best selector | **弱，倾向 KILL** | MBR、NoRefER、LTR、HypR 已直接覆盖。 |
| I2：冻结 omni 的 audio-grounded training-free selector | **中等** | READ 与 acoustic+confidence rescoring；需证明 omni 自有信号带来非同构能力。 |
| I3：受约束/可弃权的跨任务 selector，显式检测 Goodhart breakpoint | **较强但更难** | 必须证明不是把通用 BoN overoptimization 换到语音上，也不是任务专用阈值拼盘。 |

owner 已选 A-SEL 不等于这三个身份已经等价。它们共享 headline，但论文问题、工程对象和失败条件不同。

### S1-F3（FUNDAMENTAL）：缺少“新颖性击杀原型”，却提前写了 Stage-2 机械

Stage-1 最值钱的实验不是证明自家方案显著，而是尽早杀死不新或不可行的方向。当前草稿有大量 FG-1..FG-10、Holm、CI、M4 fire，却没有最小化地回答：

- MBR/consensus 是否已经吃掉大部分 oracle headroom？
- NoRefER/READ-like score 是否已经比自家 proxy 强？
- 同模型 reward 是否只是模型自信的循环验证？
- K 增加时 proxy 上升但 true utility 下降是否在很小预算就出现？
- 非 ASR 任务上所谓统一 selector 是否立即失效？

### S1-M1（MAJOR）：Stage 标签与当前活动不一致

文件自称 `stage: 2-solution-validation (entry draft)`，正文又出现 `Mode: confirmatory`。但同一文档明确 NOT-FROZEN、多个核心数值/对象待定、只请求结构验证。按仓库三阶段规则，它更准确的身份应是：

`STAGE1_EXPLORATION / PRE_STAGE2_BLUEPRINT / NOT_CONFIRMATORY`。

这不是要求修改历史文件；团队可以用 append-only successor/correction 说明身份，避免重写记录。

### S1-M2（MAJOR）：ρ 构念漂移没有显式命名

要求建立 glossary：

```text
rho_greedy := (U_sel - U_greedy) / (U_oracle - U_greedy)
rho_pool   := (U_sel - E[U_pool]) / (U_oracle - E[U_pool])
delta_mbr  := U_sel - U_mbr
regret     := U_oracle - U_sel
```

Stage-1 报告应并列描述这些量，不需要现在指定唯一 primary。分母接近零时只报告绝对量并标 `HEADROOM_TOO_SMALL`，避免比率爆炸。

### S1-M3（MAJOR）：尝试登记册存在，但 A-SEL 数字没有形成可审计 lineage

Decision Log 声称已有充实的 `experiment_attempt_registry`，这是正面建设；但 A-SEL 草稿中的 `+0.042`、MBR 趋势、C-ASR-V2 ρ 等没有逐项给出 attempt ID、配置 hash、相邻失败尝试和原始 artifact 路径。

Stage-1 不要求这些数字可发表，但要求别人能判断它们是否是从多个尝试中挑出的赢家。最低链路：

`statement -> attempt_id -> config/code/data snapshot -> raw output -> all sibling attempts -> directional interpretation`。

### S1-M4（MAJOR）：response provenance 与机读格式必须独立修复

建议新增 correction，不改 v6 原文：

```yaml
response_artifact:
  responds_to:
    path: wiki/2026-07-13-v42-remediation-signoff-doctoral-adversarial-review.md
    sha256: 64389f7fee45ea2aad4c9880fffe9293b621e52c492b79eca28d206290f761cf
  evidence_snapshot:
    umbrella_commit: 7b895b5
    w1_commit: a532da0
  artifact_snapshot:
    umbrella_commit: 311689818e6650674fac2cc1c19dbe4ee94baa29
  response_items:
    - finding_id: F-S1
      disposition: ACCEPT
    - finding_id: F-S2
      disposition: ACCEPT
```

要求 schema：`response_items` 长度恰为 13、`finding_id` 唯一、不得有未知字段、每项都有 status_before/status_after/evidence/gate。

### S1-M5（MAJOR）：廉价原型也必须先满足不可妥协的信息边界

Stage-1 可不做完整 confirmatory split，但以下安全门不因阶段降低：

- gold 不进入 selector/reward/prompt/retrieval/candidate generation；
- 同一 speaker/source/group 的跨视图泄漏要么排除，要么明确标为 feasibility-only；
- corpus 自锁不能宣称 upstream verified；
- prior exposure 无法回溯处保持 UNKNOWN，不可因小样本探索写成 clean；
- 测试 utility 只用于 read-out，不回流下一轮调参；若回流，整个池转为 development，并登记 exposure。

### S1-M6（MAJOR）：owner 决策包没有记录“为什么不选其他 A-SEL 子身份”

Stage-1 结束需要一个 decision memo，而不是只写 `headline=A-SEL`。至少包含：候选身份、直接近邻、方向性证据、资源成本、最大失败风险、kill/pivot 规则、被放弃路线与 owner 选择理由。

## 5. 当前没有成立、但必须持续监控的诚信嫌疑

### 5.1 Fabrication：未成立

未发现凭空生成数据、运行或结果的证据。hash/commit 标注错误不能单独证明数据虚构。

### 5.2 Falsification：未成立，但有三个需要取证的风险点

1. **winner-only 风险**：A-SEL 草稿引用少量好看的 Stage-1 数字，却未在同处映射 sibling attempts；
2. **配置历史风险**：部分历史配置轨迹无法完整回溯，团队已标 UNKNOWN，这是正确做法，但不能随后把相关数字写成无污染验证；
3. **commit-message/实际变更不一致风险**：此前已有提交信息声称 regeneration/refresh、实际提交内容并不支持该描述的登记项。

目前它们构成进一步核查理由，不构成 falsification 事实。

### 5.3 Plagiarism：未成立，但新颖性归属风险真实

当前没有发现复制文本/代码而不署名。更现实的风险是“概念重命名”：把 ASR reranking、MBR、reference-free QE 或 hypothesis revision 重新包装成 A-SEL/TFRL，却没有清楚说明继承关系。这首先是 scholarship/novelty 缺陷；若明知而系统性隐去来源，才会升级为更严重的诚信问题。

### 5.4 何时升级为正式不端调查

出现以下任一证据，应停止普通学术评审并启动独立调查：

- raw artifact 与报告数字不一致，且无法用版本/解析差异解释；
- attempt registry、失败运行或 prior exposure 被删除、回写或隐匿；
- 明知使用 gold/测试反馈调参，却继续宣称 label-free/held-out；
- hash/commit 被故意伪造以制造不存在的先验冻结；
- 运行日志、时间戳、模型输出或引用被捏造；
- 同一结果在多个配置/数据身份间被重复冒用。

## 6. Proposal A：Stage-1 A-SEL 原型探索矩阵

目标不是选出一个漂亮数字，而是定位**哪一种科学问题值得进入 Stage-2**。

### 6.1 固定公共骨架

所有原型共享：

- 同一冻结生成模型与同一候选池；
- equal-K、相同生成 seeds、相同推理预算账；
- 固定小样本切片，建议每个 slice 只取能在一次廉价会话完成的 group 数；
- 至少一个 clean/read speech slice、一个 noise/shift slice；
- ASR 为首要问题时先只做 ASR；只有要保留“跨任务”主张，才加一个异质任务作反证/迁移探针；
- 一次触碰 read-out；如果基于结果继续调，则新 run 明确转为 development，旧结果不升级；
- 全部结果只报告 effect profile、排序稳定性、失败模式和成本，不做显著性胜负宣告。

### 6.2 候选原型族

| 原型 | 科学问题 | 最小实现 | Stage-1 checkpoint | 失败意味着什么 |
|---|---|---|---|---|
| P0 Greedy/Pool/Oracle | 真实 headroom 是否存在、候选池是否值得选 | 不含学习的三条基线 | 多个 slice 上 headroom 的方向与稳定性；分母过小率 | headroom 常接近零则 A-SEL 直接 KILL 或缩窄场景 |
| P1 Consensus/MBR | 经典无标签共识能兑现多少 headroom | pairwise edit/semantic risk | `delta_mbr`、`rho_greedy`、成本 | 若已接近 oracle，自家复杂 selector 新颖性/效用均受击杀 |
| P2 Text-only QE | 语言流畅度/无参考错误估计够不够 | NoRefER-like 或冻结 LM score | 与 U 的排序关系、噪声下失效模式 | 若强，则 audio-grounding 必须证明额外价值；若弱，记录错误类型 |
| P3 Audio-grounded QE | 音频一致性是否提供独立信号 | READ-like/TTS discrepancy 或冻结 audio-text scorer | 相对 P2/P1 的增量、acoustic ablation | 与 READ-like 打平说明自家方法不是新问题 |
| P4 Same-model internal reward | omni 自身知识能否 read out | 冻结模型 confidence/critique/embed signal | 自相关、self-consistent-error、cross-model audit | 高自信错即说明循环验证，不可直接作 selector |
| P5 Cross-model/pessimistic | 去相关 verifier 能否抑制 proxy hacking | diff-family + non-model verifier，min/LCB/abstain | disagreement、error concentration、abstention utility | 无增益则不值得承担额外算力；有增益才支持 constrained identity |
| P6 K-sweep / constrained selector | Goodhart breakpoint 是否是核心科学现象 | 小 K 网格 + budget cap/abstain | proxy↑而 U↓ 的拐点、regret、成本曲线 | 无拐点则不要把 N\*/收敛写成 headline；有拐点才进入理论/约束轨 |

### 6.3 必须报告的 Stage-1 视图

每个原型至少报告：

- `attempt_id`、snapshot、K、seed、slice、group 数与成本；
- `U_greedy / E[U_pool] / U_mbr / U_sel / U_oracle`；
- `rho_greedy / rho_pool / delta_mbr / regret`，能定义才报告；
- proxy—U 的散点/秩关系及典型 false-positive/false-negative；
- 每个 group 的 selector 是否只是重复 greedy；
- 所有候选原型的完整表，不只显示最优项；
- “该结果能说明什么 / 不能说明什么 / 下一步为何继续或停止”。

## 7. Proposal B：Stage-1 Survey Coverage Gate

### 7.1 不是按论文数量打勾，而是按方法家族饱和

至少覆盖以下家族：

1. 经典 MBR / expected WER / confusion network / ROVER；
2. confidence estimation 与 learning-to-rank rescoring；
3. reference-free WER/quality estimation；
4. N-best LLM rescoring、generation 与 rewriting；
5. acoustic-grounded hypothesis evaluation/correction；
6. multi-verifier、uncertainty、abstention/pessimistic selection；
7. 通用 best-of-N、reward overoptimization、test-time compute；
8. 文本/视觉多模态中的 verifier-guided selection，作为机制类比而非语音 novelty 证据。

### 7.2 每篇直接近邻必须抽取的字段

```text
paper_id / task / candidate_source / sees_audio / sees_gold_at_train / sees_gold_at_test /
training_required / scorer_inputs / selection_operator / comparator / equal_budget /
datasets / metric / failure_mode / code_or_model / closest_delta_to_ASEL / audit_notes
```

### 7.3 Survey 关闭规则

- 不能只搜索 `training-free RL`，必须用领域原词：`N-best reranking`、`hypothesis selection`、`minimum Bayes risk`、`confidence estimation`、`reference-free WER`、`hypothesis revision`、`acoustic discrepancy`；
- 至少两轮独立关键词/引文链搜索；连续两轮没有出现新的方法家族，才称 family-level saturation；
- 对最接近的 5–8 篇逐篇写“ASEL 比它多了什么、少了什么、是否只是重命名”；
- 任何“首次/无先例”句子必须绑定检索截止日、query family 和反例清单；
- survey 结果允许直接 KILL 当前 identity；不能以已经投入工程为理由保留。

## 8. Proposal C：研究诚信与选择性汇报的低成本检查包

这不是要求 Stage-1 做论文级独立复现，而是防止几个月后无法区分探索与确证。

### C1. Attempt census

- 从 raw run directories、MLflow、shell logs、Git notes/commit、proposal 中各自抽取 run/attempt ID；
- 与 `experiment_attempt_registry` 做集合差；
- 未登记项分为：dry-run、failed-before-output、valid-negative、valid-positive、unknown；
- 不允许把 crash 后残留结果静默算作不存在。

### C2. Result lineage spot check

对所有进入叙述的 Stage-1 数字逐项回链 raw artifact；至少双人复核：

`reported value -> aggregation script -> raw records -> config/data/model/code hash`。

任何无法回链的数字不得删除，但必须追加标为 `UNVERIFIED_DIRECTIONAL_RECORD`。

### C3. Information-flow audit

为每个 proxy 画输入边：audio、candidate、prompt、external corpus、model output、gold、prior test feedback。若 gold/test feedback 能通过任何路径影响 selector，必须标 development exposure；不能仅依赖变量名或“理论上不读”。

### C4. Negative-result census

Stage-1 收官前列出：

- 试过但无效的 proxy；
- 因成本、稳定性、泄漏或许可废弃的方向；
- 方向相反或仅单个 slice 成立的结果；
- 事后改过的 K/prompt/threshold；
- 为什么保留最终候选。

### C5. Append-only artifact correction

不回写 v6。新增 correction 文件，修 provenance 与 YAML；旧错误仍可见。对历史 config 无法回溯处继续使用 UNKNOWN，不“补造”一个看似完整的配置。

## 9. Proposal D：建议的 Stage-1 科学问题候选

以下是给 owner 讨论的 proposal，不是替 owner 决策。

### D1. 低风险、但新颖性最弱

> 在冻结 speech/omni 模型产生的 equal-K 候选中，reference-free selector 能否稳定优于 greedy 与 pool expectation？

优点：工程简单、快速验证。缺点：与既有 reranking/QE 高度重合；除非在新的任务/信号/约束上有明确 delta，否则更像 benchmark/engineering paper。

### D2. 推荐的主探索问题

> 在冻结 speech/omni 模型的 equal-K 候选池中，**音频接地且不读取 gold 的 reward signal**，能否在 noise/shift 下提供超越 consensus/MBR 与 text-only QE 的独立选择信息，并兑现非平凡的 `rho_greedy`？

它把 novelty kill 写进问题本身：如果不能超越 MBR、text-only QE 或 READ-like acoustic score，方向应 kill/降级，而不是继续用 oracle headroom 自证价值。

### D3. 高风险、高潜力问题

> 当 best-of-K 对 imperfect speech reward 发生 proxy overoptimization 时，能否用冻结、多源、去相关且可弃权的 constrained selector，在不改权重的条件下给出可复现的 budget—regret 改善，并跨至少两个任务族保持同一约束语义？

这个问题与 Gao 等通用 Goodhart 工作有清楚联系，也更接近仓库要求的约束/收敛理论轨。但只有 P5/P6 的 Stage-1 原型显示真实拐点和 constraint benefit 后才值得进入；否则理论轨应删除，不要为理论而制造问题。

## 10. 分阶段执行计划

### T+0～1 天：只修记录与阶段身份

- 新增 v6 artifact correction；
- 用 JSON Schema/PyYAML 验证 13/13 unique items；
- 新增 `Stage-1 A-SEL Exploration Memo`，把当前 Stage-2 draft 明确降为 pre-Stage2 blueprint；
- 冻结本轮 review 对象 hash，不改历史工件。

**退出条件**：provenance 三元组可复核；13 项可机读；文档不再声称当前是 confirmatory。

### T+1～4 天：完成最近邻 survey 与 identity map

- 构建 §7 文献矩阵；
- 为 I1/I2/I3 各写 novelty delta 与 kill condition；
- 把 READ、NoRefER、HypR、MBR/LTR 设为强制近邻；
- 做一次 survey red-team：专门寻找“已经有人做了 A-SEL”的反例。

**退出条件**：两轮 family saturation；最接近 5–8 篇逐项对照；owner 能看懂三个 identity 的差异。

### T+3～7 天：廉价 prototype matrix

- 先做 P0/P1/P2；只有发现独立 signal 才做 P3/P4；
- 只有出现 proxy hacking 或 verifier disagreement 才做 P5/P6；
- 固定小样本、equal-K、单次 read-out；
- 每次尝试实时写 registry，不在结果出来后补选性历史。

**退出条件**：所有候选原型全景表、失败例、成本和 replay command 齐全；任何数字仍标 directional-only。

### T+7～9 天：诚信与可重放检查

- attempt census；
- 对所有叙述数字做 lineage spot check；
- 选一个代表性原型 clean checkout replay；
- 检查 gold/new-information 边界；
- 形成 negative-result appendix。

**退出条件**：无未解释 orphan result；无法回链项如实 UNKNOWN；replay 不要求同样的漂亮数字，但流程与方向应可解释。

### T+9～10 天：owner Stage-1 closure discussion

owner 只需在以下选项中裁决：

1. **KILL**：headroom/novelty/可行性不足；
2. **PIVOT**：保留 A-SEL headline，但选择 I2 或 I3 的具体问题；
3. **PROCEED TO FRESH STAGE-2 PROPOSAL**：选定唯一问题、最小 claim、主要强近邻与为什么值得做；
4. **ENGINEERING-ONLY**：可用但学术 novelty 不足，降为系统/开源工件。

Stage-1 不得自动滚入 Stage-2。只有 owner 书面选择后，才新建 fresh Stage-2 proposal，届时再冻结 SESOI、H/CI、Holm、N\*、样本量、完整 task cards 与 confirmatory fire。

## 11. Stage-1 收官 gate

### Gate S1-A：问题唯一且可证伪

- [ ] 一句话科学问题不依赖 `A-SEL/TFRL` 品牌词也能成立；
- [ ] 输入、允许信息、候选、selector 输出、效用和预算边界明确；
- [ ] 明确“不研究什么”；
- [ ] 至少一个结果可以合理地 kill 问题，而不是所有结果都能 pivot 成成功。

### Gate S1-B：survey 足够近

- [ ] 经典 MBR/expected WER；
- [ ] confidence/LTR；
- [ ] reference-free QE；
- [ ] LLM rescoring/revision；
- [ ] acoustic-grounded READ-like；
- [ ] BoN/reward overoptimization；
- [ ] 最接近工作逐项 novelty delta；
- [ ] 两轮方法家族饱和记录。

### Gate S1-C：方向性原型能指导决策

- [ ] P0 oracle headroom 不是单 slice 偶然；
- [ ] MBR/consensus 作为 novelty kill 已跑；
- [ ] 至少一个 text-only 与一个 audio-grounded proxy；
- [ ] 同池、equal-K、成本可比；
- [ ] 失败模式与典型错误已检查；
- [ ] 若声称 Goodhart/constraint，已有小 K 曲线而非纯理论故事；
- [ ] 若声称跨任务，至少有一个异质任务反证探针。

### Gate S1-D：诚信与记录可审计

- [ ] 13 项 v6 response 可机读且 provenance 正确；
- [ ] 所有被叙述数字有 attempt lineage；
- [ ] sibling attempts 与负结果没有被省略；
- [ ] gold/new-information flow 已检查；
- [ ] config UNKNOWN 保持 UNKNOWN；
- [ ] 至少一个代表性原型 clean replay；
- [ ] 无历史文件被回写美化。

### Gate S1-E：owner 做了充分信息下的选择

- [ ] owner 看到 I1/I2/I3 或等价候选；
- [ ] owner 看到最强反例与负结果；
- [ ] owner 明确 kill/pivot/proceed/engineering-only；
- [ ] 若 proceed，指定唯一问题与最小 Stage-2 claim；
- [ ] 新建而不是原地升级 fresh Stage-2 proposal。

## 12. 给团队 AI 的强制解释规则

1. 不得把 `NOT READY FOR STAGE1 CLOSURE` 翻译成“禁止一切原型实验”。
2. 不得把 `DIRECTIONAL EXPLORATION MAY CONTINUE` 翻译成“A-SEL 已获科学通过”。
3. 不得为了关闭本审查而现在虚构 SESOI、N\*、sample size、rho threshold 或统一跨任务量纲。
4. 不得删除/重写 v6；只能追加 correction。
5. 不得用 owner 已选 headline 代替 novelty evidence；owner 选择的是方向，文献和原型决定问题是否站得住。
6. 不得以“Stage-1 不需要显著性”作为选择性汇报、gold 泄漏或 provenance 错误的豁免。
7. 不得把 `FFP NOT ESTABLISHED` 解释为“诚信风险已关闭”；必须完成 C1–C5 的低成本核查。
8. 不得把最强近邻排到未来 secondary；在 Stage-1 它们是决定是否继续的 kill tests。
9. 理论轨只有在 P6 显示真实约束问题且理论与工程同对象时才进入；若作为贡献提出，仍必须遵守仓库 Lean、correctness + convergence、sorry-free 的规则。
10. 所有新输出继续使用 append-only 日期文档；不要修改正在进行的源文件来“迎合评审”。

## 13. 机读裁决

```yaml
review:
  id: W1-ASEL-STAGE1-RECALIBRATED-ADR-2026-07-13
  stage_standard: stage1_problem_definition
  overall_status: major_revision_for_stage1_closure
  directional_exploration_allowed: true
  stage2_readiness_assessed: false
  confirmatory_claims_allowed: false
  source_files_modified: false

verdicts:
  response_v6_substance: accept_with_record_repair
  response_v6_artifact_quality: major_repair_required
  asel_working_direction: conditionally_viable
  asel_problem_definition_closed: false
  asel_stage2_entry_ready: false
  fabrication_established: false
  falsification_established: false
  plagiarism_established: false
  qrp_record_control_risk: moderate_to_high

stage1_blockers:
  - id: S1-F1
    severity: fundamental
    issue: direct_neighbor_survey_incomplete
    close_with: survey_coverage_gate
  - id: S1-F2
    severity: fundamental
    issue: asel_not_reduced_to_one_scientific_subproblem
    close_with: owner_identity_decision_after_survey_and_prototypes
  - id: S1-F3
    severity: fundamental
    issue: novelty_kill_prototypes_missing
    close_with: run_P0_to_P3_equalK_directional_matrix
  - id: S1-M1
    severity: major
    issue: draft_mislabeled_stage2_confirmatory
    close_with: append_only_stage_identity_correction
  - id: S1-M2
    severity: major
    issue: rho_construct_drift
    close_with: dual_rho_glossary_and_reporting
  - id: S1-M3
    severity: major
    issue: reported_directional_numbers_lack_explicit_attempt_lineage
    close_with: statement_to_attempt_to_raw_artifact_mapping
  - id: S1-M4
    severity: major
    issue: response_provenance_and_yaml_broken
    close_with: append_only_schema_validated_correction
  - id: S1-M5
    severity: major
    issue: information_boundary_must_precede_real_directional_runs
    close_with: gold_flow_and_group_exposure_audit
  - id: S1-M6
    severity: major
    issue: owner_decision_package_missing_rejected_alternatives
    close_with: stage1_closure_decision_memo

deferred_to_stage2:
  - exact_SESOI_values
  - final_primary_family_and_holm
  - final_CI_and_alpha
  - exact_Nstar
  - power_and_confirmatory_sample_size
  - deterministic_final_selector_algorithm
  - full_task_cards
  - full_independent_replication
  - publication_grade_baseline_fairness

allowed_now:
  - literature_survey
  - static_audit
  - synthetic_unit_tests
  - fixed_small_sample_directional_only_prototypes
  - parallel_candidate_proxy_exploration_with_complete_logging
  - one_representative_clean_replay

forbidden_now:
  - confirmatory_claims_from_stage1_numbers
  - winner_only_reporting
  - gold_in_selector_or_reward_path
  - relabeling_oracle_headroom_as_method_success
  - automatic_rollover_to_stage2
  - rewriting_historical_artifacts
```

## 14. 最终审稿意见

**严厉结论**：团队当前最大的问题不是“统计协议还不够像论文”，而是投入了过多精力把一个尚未完成问题定义的方向写成 Stage-2 方案。这样会产生一种危险的形式主义：门、表、hash、Holm、N\* 都越来越精细，但“我们到底比 MBR、NoRefER、HypR、READ 多解决了什么”仍没有被钉死。

**公允结论**：团队对前一轮诚信问题的接受态度、开放项保持 OPEN、directional-only 标签、信息边界与负结果承诺，整体是正确的。现有证据不足以指控学术欺诈或作假；把记录错误直接上升为 FFP 也不严谨。

**博导建议**：暂停继续打磨确证统计机械，但不要停止 Stage-1 探索。用一周左右完成“直接近邻 survey → 新颖性击杀原型 → 全尝试/负结果登记 → owner 子问题选择”。如果 MBR/NoRefER/READ-like 已经吃掉主要增益，应果断 kill 或降级；如果 audio-grounded、去相关、可弃权约束在 shift/Goodhart 条件下显示独立价值，再把那个**更窄、更难、但真正不同的问题**送入 fresh Stage-2 proposal。

