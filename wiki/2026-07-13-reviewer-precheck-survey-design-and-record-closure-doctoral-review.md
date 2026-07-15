---
title: "Stage-1A Survey Design and Record Closure Precheck — Doctoral Adversarial Review"
date: 2026-07-13
review_type: "STAGE1A_DESIGN_PRECHECK_ADVERSARIAL_INTEGRITY_REVIEW"
reviewer_role: "strict_external_reviewer_and_doctoral_supervisor"
reviewed_artifact: "wiki/2026-07-13-reviewer-precheck-survey-design-and-record-closure.md"
reviewed_artifact_commit: "aad1f6d4feb6d762402aa8cbfb314c81397e352d"
reviewed_artifact_sha256_git_blob: "8a1ec913517d60fa5e3d738b4473eb6c8e26c4f36275f52a5e809e33e0f3fa40"
claimed_evidence_snapshot_umbrella: "0afad68"
verified_artifact_snapshot_umbrella: "aad1f6d4feb6d762402aa8cbfb314c81397e352d"
verified_w1_snapshot: "a532da06296681b3bbb30446a6fa285ca5bed508"
stage_interpretation: "STAGE_1A_PROBLEM_DEFINITION"
overall_verdict: "RETURN_WITH_MANDATORY_REVISIONS"
survey_design_verdict: "PARTIAL_PASS_REQUIRES_REDESIGN"
record_closure_verdict: "NOT_ACCEPTED_AS_CLOSED"
i4_novelty_verdict: "NARROW_PLAUSIBLE_WHITESPACE_NOT_ESTABLISHED"
stage1a_continuation: "ALLOWED"
stage1b_release: "NOT_REQUESTED_AND_NOT_AUTHORIZED"
ffp_finding: "NOT_ESTABLISHED"
qrp_control_risk: "MODERATE"
---

# Stage‑1A Survey 设计与记录闭环预检：严格博导式对抗审查

> **先给结论。** 研究团队这轮回复在“阶段定位、问题候选并列、泄漏数字撤回、append-only 修复”上有实质进步，方向上大体正确；但它还不能获得“记录已经闭环”或“I4 是最干净空白”的签署。当前最合理的处理是：**允许继续 Stage‑1A 文献工作，但退回本轮设计作强制修订；禁止把本轮材料解释为 Stage‑1B 放行、选题收官或新颖性确认。**

本审查严格按 **Stage‑1A 问题界定** 而不是“成型论文审稿”执行。因此，本报告不要求统计显著性、大规模实验或论文级结果；它要求的是：研究问题边界正确、survey 搜索空间不被错误切分、kill test 与身份候选对应、记录可追溯、未把未经核验的侦察印象写成确定事实。

---

## 1. 审查对象、权限边界与证据等级

### 1.1 审查对象

主审对象为：

- `wiki/2026-07-13-reviewer-precheck-survey-design-and-record-closure.md`
- artifact commit：`aad1f6d4feb6d762402aa8cbfb314c81397e352d`
- canonical git-blob SHA256：`8a1ec913517d60fa5e3d738b4473eb6c8e26c4f36275f52a5e809e33e0f3fa40`

为判断其“记录闭环通知”是否成立，交叉核验了：

- `wiki/2026-07-13-response-v6-correction.md`
- `wiki/2026-07-13-stage1a-position-and-recalibration-response.md`
- `docs/integrity/release_manifest.json`
- `docs/checks/manifest-blob-verification-2026-07-13.txt`
- umbrella 与 W1 的 Git 状态、commit、git-blob 哈希及 EOL 状态

### 1.2 本次没有做什么

- 没有修改被审文件、代码、数据、实验或团队记录。
- 没有把 Stage‑1A 侦察性数字当作科学结果。
- 没有因“未开展大实验”扣分；Stage‑1A 本就不应靠大实验替代问题论证。
- 没有把“记录错误”自动等同于“故意造假”。欺诈判断要求意图、实质性和证据链，不能靠语气推断。

### 1.3 证据等级

| 等级 | 本报告中的含义 |
|---|---|
| VERIFIED | 本地 git-blob、结构化解析或一手论文全文/摘要可直接复核 |
| SUPPORTED | 有多项一致证据，但尚未完成穷尽搜索 |
| PLAUSIBLE | 方向合理，尚不足以确证 |
| UNVERIFIED | 团队提出了数字或判断，但未提供可复核工件 |
| CONTRADICTED | 与当前可复核记录或直接文献相冲突 |

---

## 2. 总体裁决

### 2.1 做对的部分

1. **阶段身份终于基本正确。** 文档明确自己是 `DESIGN_PRECHECK + RECORD_CLOSURE_NOTICE`，不是 sign-off，不主张 Stage‑1C 完成，也没有自动滚入 Stage‑2。这符合当前 Stage‑1A。
2. **候选问题仍保持并列。** I1–I4 没有在本轮被正式选中，避免把侦察印象伪装成 owner 决策。
3. **对泄漏数字的处理是正确且重要的。** `+0.517` 被明确识别为 information-boundary 违规并撤销；`T8 −0.066` 被重新标为 benefit-null，而不是把“无收益”偷换成“无 headroom”。这两项修正降低了欺诈疑虑。
4. **记录工程有真实改进。** 13 个条目可以逐项解析、六字段 schema 成立；release manifest 中七个 git-blob 哈希可重算一致；两个仓库在核验时均 clean；EOL 审计未发现工作树 CRLF/mixed 条目。
5. **survey 已覆盖若干关键支流。** MBR、无参考质量估计、声学接地评分、置信度/LTR、LLM 重排/改写、多 verifier 与过优化，都是必要材料，不是无关堆砌。

### 2.2 尚未做对的部分

1. **把 I4 描述成“最干净 whitespace”过早。** 精确的 `供给 c × 选择器 × H(c)/rho(c)` 联合形式也许仍有窄空白，但“供给影响候选支持、oracle WER、上下文偏置/检索条件”早已是现有研究对象。当前只能说“窄组合身份尚未被直接击杀”，不能说“cleanest whitespace 已成立”。
2. **八类 survey taxonomy 对 I4 是结构性不完备的。** 它把“候选池如何被构造”混进 selector，把“上下文/检索供给”放到第二轮补查，而 I4 恰恰以供给条件量为身份核心。
3. **selection 与 revision 混为一类。** reranker 从固定 K 池选一个候选；rewriter/refiner 会生成池外输出。二者的信息、动作空间、oracle 上界和 equal-K 解释均不同，不能共用同一 kill test。
4. **I3 的 kill assignment 不够直接。** 只用文本 LLM pessimism/overoptimization 作为击杀器，会漏掉更直接的 selective prediction、risk–coverage、abstention、conformal risk control 与 speech confidence/deferral 文献。
5. **“57 条、约 44 篇独立论文、8/8 family、I4 零命中”不可复核。** 仓库内未发现与该数字配套的 paper ledger、去重规则、query log、纳入/排除记录或 hash。因此它目前是 `UNVERIFIED_SCOUT_COUNT`，不得承担新颖性结论。
6. **记录闭环出现新的 provenance 回归。** 被审文档只写 `snapshot: umbrella HEAD 0afad68 / W1 a532da0`，但文档自身位于 `aad1f6d...`。如果 `0afad68` 是 evidence snapshot，就必须明确命名；artifact snapshot 与 canonical hash 必须另列。团队刚修复过同类歧义，本轮又复现，说明 closure checker 仍未覆盖这一不变量。
7. **所谓“忠实重发，无内容变更”仍不完全成立。** 对原 v6 与 correction 的 13 条结构化记录逐项比较，仍有五个核心状态字段发生未声明规范化：四个 `status_before`、一个 `status_after`。它们可能不改变实质判断，但违反“原值忠实保存”的声明，也使 `21 → 7 → 1 → 0` 只能解释为“现有 checker 的报错归零”，不能解释为“语义闭环归零”。

### 2.3 一句话裁决

**科学方向可继续，设计必须返修；记录修复有成效，但 closure 不签；没有足够证据认定学术欺诈，也没有足够证据允许团队宣称新颖性已经通过。**

---

## 3. 多轮对抗式评审

### Round 1 — 阶段错配攻击：它是否又在用论文标准审 Stage‑1A？

**攻击。** 若要求完整预注册、大样本 CI、论文级复现，本审查本身就会错位。

**核验。** 被审文档已将任务限定为 survey 设计预检与记录通知，明确后续 Stage‑1C 才作 owner 选题。本轮没有资格授予 Stage‑1B，更没有资格签 Stage‑2。

**裁决。** `PASS_WITH_GUARDRAIL`。团队阶段认识基本正确；后续不得把本轮的 “priority” 偷换成“选择 I4”。

### Round 2 — survey 完备性攻击：八类是否覆盖了研究问题的因果结构？

**攻击。** 当前分类以“怎么选/怎么打分”为主，却没有独立建模“候选从哪里来、池是否覆盖正确答案”。对于 `H(c)`，这是决定分母的上游变量。

**反证。** RNN‑T lattice grafting 在固定 beam 下能显著改善 oracle WER，并进一步改善 rescored WER；建模单元、系统多样性和候选融合也会改变 oracle 候选质量。这些工作不是传统 selector 的附录，而是 I4 的直接先验。

**裁决。** `FAIL_MAJOR`。必须增加 **candidate-pool construction / support coverage / diversity** 独立族。

### Round 3 — 概念同构攻击：I4 是否只是 contextual ASR 与 oracle-WER 分析的改名？

**攻击。** “不同供给下看 headroom”可能只是把 no-context/retrieved-context/oracle-context 的已有比较，改写成新符号。

**证据。** contextual ASR 已比较无上下文、检索上下文、LLM 生成上下文、oracle 上下文及后处理；contextual biasing、RAG 与浅融合也长期把外部上下文作为设计轴。它们未必同时报告固定 K 池的 `H(c)` 与可部署 `rho(c)`，但已击穿“供给类型从未成为设计轴”的宽泛表述。

**裁决。** `PARTIAL_KILL`。宽 I4 被击杀；只有下述窄身份仍可调查：

> **在同一冻结 speech/omni 核心、预定义供给层级、固定候选预算与信息边界下，联合分解供给带来的 coverage 增益和 label-free selector 的 realization，并报告 H(c)、绝对 selector gain、regret、rho 与计算成本。**

这只是可调查的窄 claim，不是本轮确认的新颖性。

### Round 4 — baseline 错配攻击：每个身份候选真的在和最强同类对手比吗？

**攻击。** 一个“有相关性”的 paper 不等于一个足以击杀身份的 baseline。

**裁决。** 当前 assignment 仅部分合格：

- I1 必须面对 MBR/expected-WER、ROVER/confusion network、native likelihood/confidence、reference-free QE 和 LTR 的 Pareto 前沿；只放一个 MBR 不足。
- I2 必须面对 READ 类声学接地评分、声学+置信度融合、native self-score、冻结 multimodal iterative scoring；并要求 matched-information 与 matched-cost。
- I3 必须面对直接的 risk–coverage、abstention/selective prediction、conformal/risk control、speech confidence/deferral，而非只靠通用 pessimistic BoN。
- I4 必须面对 candidate-support/oracle-WER 与 contextual ASR/RAG 两组直接杀手；若供给提高 greedy、selector 却没有额外增益，选择器部分应被判死，不能把供给收益记到 selector 名下。

### Round 5 — 指标可识别性攻击：rho(c) 是否会制造跨供给错觉？

**攻击。** `rho(c)` 的分母 `H(c)` 随供给变化。一个供给上的 rho 更高，可能只是 headroom 变小，而不是 selector 更强。

**必要分解。** 对每个供给层级分别报告：

\[
H(c)=U_{oracle}(c)-U_{greedy}(c)
\]

\[
G_{sel}(c)=U_{sel}(c)-U_{greedy}(c)
\]

\[
regret(c)=U_{oracle}(c)-U_{sel}(c)
\]

\[
rho_{greedy}(c)=G_{sel}(c)/H(c)
\]

并把从基础供给 `c0` 到新供给 `c` 的总收益拆成：

\[
U_{sel}(c)-U_{greedy}(c_0)
=
[U_{greedy}(c)-U_{greedy}(c_0)]
+
[U_{sel}(c)-U_{greedy}(c)]
\]

第一项是供给本身的收益，第二项才是该供给下 selector 的额外收益。`rho` 分母过小时仍按 glossary 标为 `HEADROOM_TOO_SMALL`。

**裁决。** `MAJOR_DESIGN_REQUIREMENT`。不做此分解，I4 会发生归因欺诈风险，即使原始数字都是真的。

### Round 6 — 成本公平性攻击：equal-K 是否等于公平？

**攻击。** retrieval、TTS likelihood、额外 omni verifier、迭代 refinement 的每候选成本不同。相同 K 不代表相同推理预算、延迟或外部信息量。

**裁决。** `FAIL_IF_EQUAL_K_ONLY`。Stage‑1A 现在不需要跑成本实验，但 proposal 必须预先登记至少三种预算视角：

1. equal-K；
2. equal model-call / token / audio-second budget；
3. wall-clock 或 normalized inference cost。

任何使用 golden transcript、answer、qrel 或由它们派生的检索词都直接违反 information boundary。

### Round 7 — 记录闭环攻击：checker=0 是否意味着记录真闭环？

**攻击。** 现有 checker 可能只验证 YAML 可解析、字段存在、哈希一致，却未验证语义忠实度和 snapshot 身份。

**复核结果。** 正向结果：

- correction 的 13 条记录逐项可解析；
- 每条为六字段 schema；
- release manifest 七个 canonical git-blob 哈希全部匹配；
- 核验时 umbrella/W1 clean；
- EOL 检查无 CRLF/mixed。

但仍有五个未声明变换：

| finding | 字段 | 原 v6 原值 | correction 值 |
|---|---|---|---|
| F-S4 | `status_before` | `PARTIAL（标签超陈述）` | `PARTIAL` |
| F-S5 | `status_before` | `WRONG_GATE（原挂 P2/M2）` | `WRONG_GATE` |
| F-S6 | `status_after` | `CLOSED-as-record` | `CLOSED_AS_RECORD` |
| M-S2 | `status_before` | `PARTIAL（诚实命名已修，实质依据未交付）` | `PARTIAL` |
| M-S4 | `status_before` | `WRONG_GATE（原 M2→M3）` | `WRONG_GATE` |

这些变换可能是合理 canonicalization，但必须为相应字段显式保留 `*_raw` 与 `*_canonical`，或保持原值不动。当前“忠实重发，无内容变更”的字面声明与记录不一致。

此外，被审 artifact 重新使用单一 `snapshot` 字段，把 evidence snapshot `0afad68` 与 artifact commit `aad1f6d...` 混在一起。该回归足以拒绝 closure 签署。

**裁决。** `RECORD_CLOSURE_NOT_ACCEPTED`。`21 → 7 → 1 → 0` 至多说明既有 checker 命中归零，不说明审计语义空间归零。

### Round 8 — 欺诈假设攻击：这些问题是否足以认定造假？

**最不利假设。** 团队可能借未提交的 57/44 统计夸大新颖性，以“0 issue”掩盖记录变化，并选择性保留有利数字。

**反向证据。** 团队主动撤销了对自己有利的泄漏数字，保留并重新解释负结果，公开了多轮自检失败，采用 append-only 修复，manifest 哈希可复算。此行为模式与蓄意掩盖并不一致。

**裁决。** `FFP_NOT_ESTABLISHED`，但 `QRP_CONTROL_RISK=MODERATE`。当前可成立的是“质量控制和措辞纪律不足”，不能升级为 fabrication/falsification/plagiarism。若后续拒绝提供 scout ledger、发现删除失败尝试、无法解释原始记录、或存在 golden 信息进入 selector 路径，才应重新开启正式 misconduct inquiry。

---

## 4. 对 Q1–Q6 的逐项回答

## Q1 — 八类 family 是否足够？还缺什么？

**答案：不够。** 八类可以作为第一轮导航，但不能作为 I1–I4 的最终 survey ontology。至少做以下重构：

### 必须新增的独立 family

1. **候选池构造、support coverage 与 diversity**
   - sampling/temperature/top-p/beam；
   - lattice/N-best extraction 与 lattice grafting；
   - multi-system candidate union；
   - modeling unit 对 oracle WER 的影响；
   - coverage–diversity–quality trade-off。

2. **上下文供给、contextual biasing 与 retrieval-conditioned ASR**
   - no-context / retrieved-context / generated-context / oracle-context；
   - shallow/deep/contextual fusion；
   - audio-native RAG；
   - query construction 与 information boundary；
   - context 噪声和错误检索鲁棒性。

3. **selective prediction、risk–coverage、abstention 与 conformal risk control**
   - coverage 不是候选覆盖，而是系统选择回答的比例，二者必须拆名；
   - selective risk、risk–coverage curve、deferral、calibration；
   - distribution shift 下的有效性。

### 必须拆开的 family

4. **selection/reranking 与 revision/refinement 分拆。**
   - selection：输出必须来自预先冻结的 K 池；
   - revision：允许生成池外输出；
   - revision 需要单独定义 post-revision oracle、信息预算和失败模式，不能借用 selector 的 `rho`。

### 建议补强，而非立即独立成族

- system combination/ROVER 可留在经典决策族，但需显式覆盖 cross-system diversity；
- lattice/online rescoring 应进入候选支持族；
- dialogue/meeting context 进入上下文供给族；
- 若保留跨任务主张，增加 ST QE、语义效用和任务特定 verifier 的索引层。

**Q1 verdict：`MAJOR_REVISION`。**

## Q2 — I1–I4 的 kill assignment 是否正确？

**答案：部分正确，但不够对称，也不够强。** 建议改为以下最小击杀矩阵：

| 身份候选 | 必须正面对比的 killer | 最小公平条件 | 击杀标准 |
|---|---|---|---|
| I1 一般 label-free N-best selector | MBR/expected-WER、ROVER/confnet、native likelihood/confidence、NoRefER/QE、LTR | 同一 K 池、同信息、同预算 | 无稳定绝对增益，或仅在弱 baseline 上成立 |
| I2 音频接地冻结 omni selector | READ/TTS likelihood、acoustic+confidence、native audio-text score、MILS 类训练-free scoring | matched modality、matched calls、evaluator independence | 去掉音频不降、音频分数不增益、或通用强 scorer 等价 |
| I3 受约束/可弃权/Goodhart 检测 selector | selective prediction、risk–coverage、abstention、conformal/risk control、pessimistic BoN | 同 coverage、同风险定义、同 shift | 只靠阈值重命名；无有效 risk–coverage 改善；约束不控制过优化 |
| I4 供给分层兑现率 | oracle-WER/candidate support、contextual ASR/RAG、no/retrieved/generated/oracle context | equal-K + equal-cost 两套、gold 隔离、同核心 | 总收益全来自供给，selector gain 近零；或只是已有 contextual-ASR 对比改名 |

**Q2 verdict：`PARTIAL_PASS`，必须按上表强化后再进入全文 survey。**

## Q3 — “I4 是最干净 whitespace”是否成立？

**答案：不成立，至少当前证据不允许这样写。**

可保留的判断是：

> 在本轮尚不完整的侦察中，尚未找到一篇同时以“同一冻结 omni 核心、供给 factorial、固定预算 K 池、H(c)、部署 selector 的 rho/regret、严格信息边界”为统一主要对象的直接同构工作。

这与“没有人把 supply type 当设计轴”不是一回事。后者已被 contextual ASR、contextual biasing、RAG 与 oracle-context 文献反驳；candidate-support/oracle-WER 文献也早已研究候选生成如何改变可选上界。

因此应把 I4 状态改为：

- `broad_claim = KILLED`
- `narrow_joint_claim = PLAUSIBLE_NOT_VERIFIED`
- `priority = HIGH_FOR_SURVEY_NOT_SELECTED_FOR_PROJECT`

**Q3 verdict：`REJECT_CURRENT_WORDING`。**

## Q4 — 第二轮 survey 优先级是否正确？

**答案：需要重排。** 建议优先级如下：

1. **candidate pool construction / support / oracle-WER / diversity**
2. **contextual ASR / contextual biasing / retrieval / no-vs-oracle context**
3. **直接 selector 强基线：MBR、ROVER、QE、confidence、LTR**
4. **I3 的 selective prediction / risk–coverage / conformal / deferral**
5. **acoustic grounding、native self-score 与 evaluator independence**
6. **audio-native RAG、speech/omni self-evaluation、跨任务统一效用**
7. **文本/视觉类比**，仅用于机制启发，不能替代 speech-native killer

另外，Jinnai 等 MBR 证据在仓库已有较完整核验，不应继续统一标成“scout-level pending”；应在 ledger 中逐篇标证据等级，而不是整批降级或升级。

**Q4 verdict：`REORDER_REQUIRED`。**

## Q5 — 语料覆盖缺口是否可以留到 Stage‑1C？

**答案：运行和采购可以以后做，但 claim scope 不能拖到 Stage‑1C 才决定。**

当前若主要覆盖 read speech 和合成噪声，就必须立即把对外问题限定为相应 domain，或在 Stage‑1B 方向性包中预留至少一个非朗读、真实噪声或会议/通话 domain。原因是：

- 供给价值高度依赖长尾实体、话题上下文和真实会话噪声；
- read-speech 上“无 retrieval headroom”不能否定 contextual supply；
- 只在干净语音上有效的 selector 不能外推到 meeting/telephony；
- HypR 已涉及 TED-LIUM2/AISHELL-1，context discovery 工作覆盖 TED-LIUMv3、Earnings21、SPGISpeech，相关领域差异不是未来才出现的问题。

Stage‑1A 现在应完成的是 **domain × failure mode × dataset candidate** 的纸面映射，不是立即下载或大规模运行。

**Q5 verdict：`SCOPE_NOW_RUN_LATER`。**

## Q6 — 记录是否已经闭环？

**答案：大部分底层修复可验证，但整体 closure 暂不接受。**

可签部分：

- 13 条 correction 均可解析；
- schema 六字段成立；
- manifest 7/7 canonical hash 匹配；
- EOL 与 clean-state 通过；
- `+0.517` 泄漏撤回和 `T8` 重新解释有记录；
- F-S2 当前重新关闭的实质理由没有发现反证。

不可签部分：

- precheck 自身再次混淆 evidence snapshot 与 artifact snapshot；
- 五个核心状态字段（四个 `status_before`、一个 `status_after`）发生未声明规范化；
- correction 的机器块表达的是历史状态，后续 current override 主要存在于叙述层，机器消费者容易把旧状态当现状；
- 57/44 scout 数字与 I4 零命中没有已提交 ledger/query log 支撑。

**Q6 verdict：`PARTIALLY_VERIFIED_NOT_CLOSED`。**

---

## 5. 对四个身份候选的严格状态更新

| 候选 | 当前状态 | 主要理由 | Stage‑1A 下一步 |
|---|---|---|---|
| I1 | `NEAR_KILLED_BUT_COMPLETE_BASELINE_AUDIT` | MBR/QE/LTR/LLM rerank 已高度占据；不能仅凭 44 篇侦察就宣判 | 完成 Pareto baseline 与固定池定义，若无窄机制差异则 kill |
| I2 | `OCCUPIED_IDENTITY_REQUIRES_NARROWING` | READ、声学+置信度、训练-free multimodal scoring 形成直接压力 | 仅保留能证明 audio grounding 提供独立信息且不依赖 gold 的窄问题 |
| I3 | `PLAUSIBLE_MECHANISM_NOT_NOVEL_BY_GUARDS_ALONE` | abstention、pessimism、risk control 本身不新；可能的新意在 speech/omni Goodhart 检测对象 | 用 direct risk–coverage/conformal killer，而非通用文本类比 |
| I4 | `BROAD_KILLED_NARROW_PLAUSIBLE` | supply 作为轴已有先例；联合分解 H/rho/regret 与固定 frozen-core 也许尚有空白 | 重写 claim、补 candidate/context 两族、做供给与 selector 归因图 |

当前不建议把 I4 从候选升级为“推荐选题”。合理措辞是：**I4 是第二轮 survey 的优先调查对象，不是已赢得新颖性竞争的对象。**

---

## 6. 学术诚信与疑似造假的分级判断

### 6.1 当前没有证据支持的严重指控

没有发现足以成立下列结论的证据：

- fabrication：虚构不存在的实验或样本；
- falsification：篡改数据、删除相反结果或操纵分析以改变结论；
- plagiarism：未归属地复制他人成果；
- 已知 golden leakage 后仍把数字作为有效结果发布。

尤其是主动撤回 `+0.517`，对团队自身是不利修正，这一点应作为反对“蓄意伪造”推断的重要证据。

### 6.2 当前可以成立的质量与诚信风险

| 风险 | 等级 | 依据 | 性质 |
|---|---|---|---|
| closure rhetoric 超过 checker 能力 | 中 | 报告 “0” 但仍有 snapshot/semantic fidelity 缺口 | 记录控制/QRP 风险 |
| scout 数量和零命中不可复核 | 中 | 无 ledger、query log、dedup 规则 | 证据不足，不等于虚构 |
| “忠实重发”与五处规范化不一致 | 中 | 原值与 canonical 值未拆开 | 语义 provenance 缺陷 |
| I4 whitespace 措辞过强 | 中 | 与 contextual ASR/candidate-support 先例冲突 | 新颖性夸大风险 |
| 泄漏结果继续被使用 | 当前低 | 已撤回并公开 | 若未来复用则升级为高 |

综合判定：

- `FFP = NOT_ESTABLISHED`
- `QRP / record-control risk = MODERATE`
- `intent to deceive = NO EVIDENCE`
- `need for enhanced audit trail = YES`

### 6.3 何时升级为正式 misconduct inquiry

只有出现下列任一证据，才建议从质量审计升级为学术不端调查：

1. 声称存在的 57/44 ledger 无法提供，且数字来源无法重建；
2. raw search/run 记录与 registry 存在系统性、只删除负项的差集；
3. 已知泄漏的 `+0.517` 或同源变体再次出现在 proposal/摘要/图表中而不标 invalid；
4. selector、reward、prompt、retrieval query 或候选构造可读取 item gold；
5. canonical hash 无法重算，且出现事后替换但继续引用旧 commit/hash；
6. 团队拒绝保存失败尝试或以覆盖旧文档代替 append-only correction。

在这些触发条件出现前，不允许把“控制缺陷”写成“造假事实”；同样，也不允许用“暂未发现造假”来豁免记录整改。

---

## 7. 必须采用的 Survey v2 设计

### 7.1 最小 ontology

每篇文献至少编码以下维度，不能只分到一个 family 后写摘要：

```yaml
paper_id: "stable_unique_id"
title: "verbatim_title"
primary_url: "doi_or_official_page"
venue_year: "venue_and_year"
evidence_grade: "SCOUT|ABSTRACT_VERIFIED|FULLTEXT_VERIFIED|REPRODUCED"
task_domain: "ASR|ST|audio_captioning|text|vision|other"
speech_domain: "read|meeting|telephony|broadcast|spontaneous|synthetic|not_applicable"
model_state: "frozen|trained|fine_tuned|mixed"
supply_c: "prompt|retrieval|context|audio_frontend|tool|decoding|none|mixed"
candidate_support: "beam|sampling|lattice|multi_system|revision|single_output|other"
pool_size_k: "reported_value_or_NR"
operator_type: "selection|reranking|system_combination|revision|generation|abstention"
uses_audio_at_decision: "yes|no|unclear"
uses_gold_at_inference: "yes|no|unclear"
budget_basis: "K|model_calls|tokens|latency|unreported"
baselines: ["baseline_ids"]
reported_metrics: ["WER", "oracle_WER", "risk_coverage", "other"]
candidate_identity_kill: ["I1", "I2", "I3", "I4"]
kill_strength: "DIRECT|PARTIAL|ANALOGY|NONE"
reviewer_note: "bounded_factual_note"
source_commit_or_hash: "artifact_reference"
```

### 7.2 搜索日志

必须 append-only 保存：

- 数据库/搜索引擎；
- 日期与 query 原文；
- 起止结果页或返回上限；
- 去重键（DOI、arXiv ID、title normalized）；
- 纳入/排除原因；
- scout、abstract-verified、fulltext-verified 的升级轨迹；
- reviewer 与复核人；
- ledger 的 canonical hash。

“57 条、约 44 篇”只有在该日志上可重建，才可再次出现在 owner 决策包。

### 7.3 轻量但严格的停止规则

Stage‑1A 不必假装做 PRISMA 级系统综述，但必须有预先写下的 saturation rule。例如：

> 对每个直接 family 至少完成 seed paper 的 backward/forward citation chase；连续两个独立 query batch 不再产生新的机制类别或新的 direct killer，才可标为 `LOCALLY_SATURATED`。这不是“全球穷尽”。

### 7.4 证据措辞纪律

- `zero papers found` 必须改成 `no direct match found within logged search scope`；
- scout 摘要不能承担 novelty kill 或 novelty confirmation；
- analogies 只能产生假设，不能证明 speech identity 空白；
- 论文有 reranking 结果，不等于它研究 realization rate；
- 论文研究 context，不等于它已经完成 I4；但足以击杀“context/supply 从未作为设计轴”。

---

## 8. 建议作为 proposal 候选的检查点与探索方向

以下是 Stage‑1A 的 **proposal-space checkpoints**，不是实验结果要求，也不意味着自动进入 Stage‑1B。

### P‑A：候选支持与兑现率的因果拆分

**问题。** selector 失败究竟因为池中没有好答案，还是因为有好答案却选不中？

**纸面设计。** 形成 `供给 c → candidate support → H(c) → selector → G_sel(c)/rho/regret` 因果图；把候选生成和选择器视为两个可单独击杀的组件。

**Stage‑1B 以后才可做的方向性检查。** 在相同输入上固定核心，改变 candidate construction，分别看 oracle-WER 与 selector gain；任何 null 都必须按 headroom 归因纪律解释。

**kill 条件。** 所有看似 selector 的收益都由更好的候选生成解释，或 selector 在有 headroom 时不胜强 baseline。

### P‑B：上下文供给的价值、污染与鲁棒性

**问题。** retrieval/context 是在读出模型已有能力，还是向 item 注入新信息？错误上下文是否产生更严重的 hallucination/Goodhart？

**纸面设计。** 预定义 no-context、retrieved-context、generated-context、oracle-context（仅上界、不可部署）与 adversarial/wrong-context；画清 gold 与 query 的信息边界。

**检查点。** 把 `greedy supply gain` 与 `selector gain` 分开；同时考察错误检索下的 regret 和 abstention。

**kill 条件。** 可部署 retrieval 没有稳定改变 H(c)，或收益只能通过 gold-derived query 获得。

### P‑C：音频接地是否提供独立证据

**问题。** 所谓 audio-grounded selector 是否真正听音频，还是复述文本候选的语言先验？

**纸面设计。** 预登记 audio-present、audio-shuffled、audio-muted、candidate-text-only、native-confidence 与独立 acoustic scorer 对照。

**检查点。** 分数与真实候选质量的相关性不是充分条件；还要看同池选择增益、模态消融和 evaluator 错误相关性。

**kill 条件。** 打乱音频不影响选择，或提升完全由文本 fluency 偏好解释。

### P‑D：受约束选择与可弃权的风险–覆盖面

**问题。** 能否识别 verifier 开始过优化的拐点，并在低可信样本上不选/回退默认输出？

**纸面设计。** 以 risk–coverage curve、selective risk、fallback-to-greedy 和 calibration 为主对象，不把“加阈值”当新颖性。

**检查点。** 约束必须对应可验证 failure mode：奖励估计误差、verifier 相关性、候选数扩大引起的 overoptimization、distribution shift。

**kill 条件。** 相同 coverage 下不优于标准 confidence/conformal baseline，或阈值只在测试标签调参后成立。

### P‑E：verifier 多样性与相关错误

**问题。** 多 verifier 是真正增加独立证据，还是多个同源模型对同一语言流畅性偏差投票？

**纸面设计。** 对 verifier 的训练源、模态输入、参数共享、错误相关性、校准方式做 lineage 表；优先异质证据而非数量。

**检查点。** 预定义 decorrelation/conditional error analysis；不能仅报告 ensemble 平均分更高。

**kill 条件。** verifier 高度同源，增加数量只放大共同偏差，或在 hard subset 上错误同步上升。

### P‑F：跨任务“统一 selector”是否是伪统一

**问题。** ASR 的 WER、ST 的语义质量、SID/SER 的分类效用能否共享一个 label-free 决策原则，还是仅共享代码接口？

**纸面设计。** 将共享对象限定为 operator/constraint，不强行统一不可比较的 reward scale；对每任务保留 utility 与 SESOI。

**kill 条件。** 统一只发生在工程 wrapper，科学机制、reward 和失败模式完全分离。

### P‑G：成本条件下的最优供给–选择联合策略

**问题。** 给定有限推理预算，应把成本花在更好的供给、更大的 K，还是更强 selector？

**纸面设计。** 把 `c`、K、verifier calls、retrieval/TTS 成本纳入 constrained allocation，而不是只比 equal-K。

**潜在价值。** 这是 I4 比“再做一个 reranker”更有可能形成清晰问题的方向，但前提是先证明它不是 contextual ASR/test-time compute 的直接重述。

---

## 9. 强制整改计划与进入下一步的门槛

## P0 — 在下一轮全文 survey 结论形成前必须完成

### P0‑REC‑1：修复本轮 artifact provenance

用新的 append-only correction 明确：

```yaml
evidence_snapshot:
  umbrella: "0afad68..."
  w1: "a532da0..."
artifact_snapshot:
  umbrella: "aad1f6d4feb6d762402aa8cbfb314c81397e352d"
artifact_sha256_git_blob: "8a1ec913517d60fa5e3d738b4473eb6c8e26c4f36275f52a5e809e33e0f3fa40"
```

不得覆盖原 precheck。

### P0‑REC‑2：解决五处 status 忠实性

二选一：

- 保留原始字符串不变；或
- 为四个 `status_before` 和一个 `status_after` 同时保存 `*_raw` 与 `*_canonical`，并记录 normalization rule。

同时提供唯一的 `current_status_overrides` 机器块，让消费者不会把历史状态误当当前状态。

### P0‑SURV‑1：提交 scout ledger 与 query log

必须能重建：57 条如何得到、44 篇如何去重、8/8 如何判断、哪些 paper 直接/部分/类比击杀 I1–I4。提交后再更新计数；若重建失败，应写 `COUNT_WITHDRAWN`，不能猜一个新数字。

### P0‑SURV‑2：重构 taxonomy

加入候选支持、上下文供给、selective prediction 三族；拆分 selection 与 revision；把现有每篇 paper 重新映射。

### P0‑SURV‑3：降级 I4 措辞

把 “cleanest whitespace” 改为 `narrow plausible whitespace pending logged full-text survey`，并显式写出被 contextual ASR/candidate-support 击杀的 broad claim。

## P1 — Stage‑1C owner 决策包前必须完成

1. 完成 I1–I4 direct killer matrix，每个 direct killer 至少 abstract-verified，关键 kill 至少 fulltext-verified。
2. 画出 I4 的供给收益/selector 收益分解和预算公平性设计。
3. 对 read/meeting/telephony/broadcast/spontaneous domain 做 scope map；数据不必全部下载，但 claim 必须限定。
4. 为 I2 写 audio grounding 的模态消融与 evaluator independence 纸面协议。
5. 为 I3 写 risk–coverage/conformal/deferral 对照，而不是只写 Goodhart 叙事。
6. 给每个候选一页 `kill/pivot/proceed` dossier；owner 只能在 Stage‑1C 明确选一个或全部 kill/pivot。

## P2 — 只有 owner 显式放行 Stage‑1B 后才允许

1. 小样、廉价、single-touch、directional-only 原型；
2. 所有尝试、配置、失败和泄漏均登记；
3. 不做显著性结论，不冻结论文级 SESOI；
4. 每个 selector 结果同报对应池的 H(c)；
5. 无 headroom 的 null 只否定供给配置，有 headroom 的 null 才能击杀 selector；
6. 不得把 Stage‑1B 数字反向包装成 Stage‑1A 新颖性证据。

---

## 10. 文献对抗核查：直接支持本裁决的一手来源

下面不是“按关键词堆文献”，而是按本轮具体 claim 分组。优先列官方论文页、出版社或 arXiv 原文。

### 10.1 经典选择、MBR 与强基线

1. Stolcke et al., *Explicit Word Error Minimization in N-best List Rescoring*：expected-WER/N-best 决策的经典依据。  
   <https://www.isca-archive.org/eurospeech_1997/stolcke97_eurospeech.html>
2. Goel & Byrne, *Minimum Bayes-risk automatic speech recognition*：MBR 的直接理论/实践先例。  
   <https://www.sciencedirect.com/science/article/pii/S0885230800901384>
3. Wu et al., *Learning to Rescore Hypotheses for Automatic Speech Recognition*：LTR 直接基线。  
   <https://www.isca-archive.org/interspeech_2022/wu22_interspeech.html>
4. Yüksel et al., *NoRefER: A Referenceless Quality Metric for ASR*：无参考 ASR 质量估计。  
   <https://www.isca-archive.org/interspeech_2023/yuksel23_interspeech.html>
5. Jinnai et al., *Minimum Bayes Risk Decoding for Conversational Speech Recognition and Translation*：现代 ASR/ST 上 MBR 与 beam 的强比较。  
   <https://arxiv.org/abs/2510.19471>

### 10.2 LLM reranking 与 revision 必须拆分

6. Wang et al., *HypR: A Comprehensive Study for ASR Hypothesis Refinement with LLMs*：明确区分 reranking 与 correction/refinement，并在多个 ASR 数据集与大 N-best 上评估。  
   <https://www.isca-archive.org/interspeech_2024/wang24j_interspeech.html>
7. ProGRes：LLM-based progressive ASR rescoring。  
   <https://arxiv.org/abs/2409.00217>
8. Kang et al., *Large Language Model Based ASR Rescoring with Reinforcement Learning*：rescoring/rewriting 相关近邻。  
   <https://www.isca-archive.org/interspeech_2024/kang24c_interspeech.html>

### 10.3 声学接地与多模态 scorer

9. Shu et al., acoustic information 与 confidence 融合的 ASR rescoring：I2 不能只与纯文本 LLM 比。  
   <https://www.isca-archive.org/interspeech_2024/shu24_interspeech.html>
10. READ, *Reference-Free Evaluation for ASR Decoding*：training-free、reference-free、以 TTS conditional likelihood 进行声学接地评估，是 I2 的直接 killer。  
    <https://arxiv.org/abs/2606.04680>
11. MILS, *Multimodal Iterative LLM Solver*：训练-free 多模态生成/评分机制，对宽泛 I2 新颖性构成压力，但不是同构 ASR selector。  
    <https://arxiv.org/abs/2501.18096>

### 10.4 候选支持、diversity 与 oracle WER

12. Novak et al., *RNN-T Lattice Grafting for Improved ASR Rescoring*：固定 beam 下改变 candidate support 可改善 oracle WER 与 rescored WER，直接证明 H(c) 的上游构造不能被省略。  
    <https://www.isca-archive.org/interspeech_2022/novak22_interspeech.pdf>
13. Irie et al., modeling unit 与 hypothesis diversity/oracle quality：候选表示影响上界。  
    <https://www.isca-archive.org/interspeech_2019/irie19_interspeech.pdf>
14. Audhkhasi et al., diversity 与 system combination：cross-system diversity 对 ROVER/fusion/oracle 的影响。  
    <https://www.isca-archive.org/interspeech_2013/audhkhasi13_interspeech.html>
15. Faria et al., dense ASR alternatives 与 oracle WER：候选覆盖是独立研究轴。  
    <https://www.isca-archive.org/interspeech_2022/faria22_interspeech.html>

### 10.5 上下文供给、检索与 I4 宽 claim 的反证

16. Siskos et al., *ASR Context Discovery via Large Language Models*：比较 no-context、retrieval、LLM-generated 与 oracle context；直接反驳“供给类型未被作为设计轴”的说法。  
    <https://arxiv.org/abs/2509.19567>
17. Amazon, *Contextual ASR with Retrieval-Augmented Large Language Model*：contextual ASR/RAG 的直接近邻。  
    <https://www.amazon.science/publications/contextual-asr-with-retrieval-augmented-large-language-model>
18. BR-ASR：retrieval/context 对 ASR 的近期近邻。  
    <https://arxiv.org/abs/2505.19179>
19. Zhao et al., contextual ASR shallow fusion：上下文供给并非 LLM 时代才出现。  
    <https://www.isca-archive.org/interspeech_2019/zhao19d_interspeech.html>

### 10.6 Test-time compute、coverage 与过优化

20. Huang et al., BoN reward overoptimization 与 coverage/pessimism：I3/I4 的通用机制近邻。  
    <https://arxiv.org/abs/2503.21878>
21. Snell et al., *Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters*：proposal refinement、verifier search 与 prompt difficulty 的预算分配先例。  
    <https://arxiv.org/abs/2408.03314>

### 10.7 Selective prediction、abstention 与 risk control

22. *Selective Question Answering under Domain Shift*：risk–coverage 与 abstention 的直接方法论先例。  
    <https://aclanthology.org/2021.acl-long.84/>
23. selection-conditional conformal prediction：选择条件下的风险控制不能被简单阈值替代。  
    <https://academic.oup.com/jrsssb/article/87/4/1239/8113856>
24. conformal language generation：生成场景中的风险/覆盖控制近邻。  
    <https://ojs.aaai.org/index.php/AAAI/article/view/29062>

**survey 结论。** 这些文献足以否定“现有八类已经完备”和“I4 宽表述是干净空白”；但尚不足以否定经过严格收窄后的联合研究对象。因此正确动作是扩大并重构 survey，而不是现在 kill I4，也不是现在选择 I4。

---

## 11. 给团队 AI 的机器可执行裁决

```yaml
review_decision:
  stage: "STAGE_1A"
  overall: "RETURN_WITH_MANDATORY_REVISIONS"
  may_continue_literature_collection: true
  may_claim_record_closure: false
  may_claim_i4_novelty: false
  may_start_stage1b: false
  may_start_stage2: false
  owner_decision_required_for_stage1b: true

question_answers:
  q1_family_completeness: "MAJOR_REVISION"
  q2_kill_assignment: "PARTIAL_PASS_STRENGTHEN"
  q3_i4_whitespace: "BROAD_CLAIM_KILLED_NARROW_CLAIM_UNVERIFIED"
  q4_survey_priority: "REORDER_REQUIRED"
  q5_corpus_gap: "SCOPE_NOW_RUN_LATER"
  q6_record_closure: "PARTIALLY_VERIFIED_NOT_CLOSED"

integrity_assessment:
  fabrication_established: false
  falsification_established: false
  plagiarism_established: false
  intent_to_deceive_evidence: false
  qrp_control_risk: "MODERATE"
  formal_misconduct_inquiry_now: false

mandatory_before_next_survey_conclusion:
  - id: "P0-REC-1"
    action: "append-only split evidence_snapshot from artifact_snapshot and add canonical artifact hash"
    acceptance: "both commits and git-blob hash independently reproducible"
  - id: "P0-REC-2"
    action: "preserve five raw status strings or document raw-to-canonical normalization; add current_status_overrides"
    acceptance: "semantic diff is empty or explicitly explained"
  - id: "P0-SURV-1"
    action: "commit reconstructable 57/44 scout ledger, query log, dedup and inclusion/exclusion rules"
    acceptance: "independent recount matches or old count is withdrawn"
  - id: "P0-SURV-2"
    action: "add candidate-support, contextual-supply and selective-prediction families; split selection from revision"
    acceptance: "all seed papers remapped with direct/partial/analogy kill strength"
  - id: "P0-SURV-3"
    action: "downgrade I4 from clean whitespace to narrow plausible whitespace"
    acceptance: "broad claim explicitly marked killed and narrow claim stated verbatim"

candidate_status:
  i1: "NEAR_KILLED_COMPLETE_AUDIT"
  i2: "OCCUPIED_REQUIRES_NARROWING"
  i3: "PLAUSIBLE_MECHANISM_GUARDS_NOT_NOVEL"
  i4: "BROAD_KILLED_NARROW_PLAUSIBLE"

signoff_condition:
  record_closure: "P0-REC-1 and P0-REC-2 complete with fresh independent check"
  survey_precheck: "P0-SURV-1 through P0-SURV-3 complete"
  stage1c_entry: "P1 dossier complete and owner explicitly convenes closure decision"
```

---

## 12. 最终导师意见

这轮回复不是应被全部否定的失败。它最重要的进步，是团队终于停止把 Stage‑1A 当成预注册实验阶段，并敢于撤销有利但泄漏的数字。然而，研究团队仍有一个反复出现的习惯：**每修好一层机器格式，就过早使用“闭环”“零问题”“最干净空白”等完成性语言。** 这在普通工程记录中已经危险，在新颖性和学术诚信语境中更危险。

下一步不应跑更多实验来掩盖 survey 缺口，也不应围绕 I4 继续写成型 proposal。正确动作是：先把候选支持、上下文供给、selective prediction 三条直接文献链补齐；把 57/44 变成可重建工件；把供给收益与 selector 收益彻底拆开；然后在 Stage‑1C 由 owner 决定哪个具体问题值得进入方向性原型。

在上述整改完成前，本人给出的签署状态为：

> **Stage‑1A 可继续；本轮 survey design 有条件退修；record closure 不签；I4 新颖性不签；Stage‑1B 不放行；未认定学术造假。**
