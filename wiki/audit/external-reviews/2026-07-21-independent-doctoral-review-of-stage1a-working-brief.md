---
title: "Stage-1A working brief 独立博导级敌意复审"
date: 2026-07-21
review_role: "independent doctoral reviewer"
reviewed_artifact: ".worktrees/stage1b-readiness-remediation/wiki/survey/workbench/system-first-stage1a/2026-07-21-stage1a-working-brief.md"
reviewed_commit: "9e708c50be0efae61ef47216b772cc5a6634abd3"
reviewed_git_blob: "5ed39cd2f2570914d7f95f62abc34425b85dd971"
reviewed_blob_sha256: "ccb88d6e86af0aafa6b2c342ff06ce361b035d9b7c6cadcaa36bcf372473d6b6"
reviewed_blob_bytes: 42933
review_verdict: "MAJOR_REVISION_AND_WITHHOLD"
stage1b_authorization: "NO"
reviewed_worktree_modified: false
review_output_location: "main workspace wiki only"
---

# Stage-1A working brief 独立博导级敌意复审

## 0. 一句话裁决

**当前仍处于 Stage-1A final remediation，而不是 Stage-1B；继续开展 systematic mapping 的科学理由仍然充分，但当前 search design 不得签署，Stage-1B 不得启动。**

本轮不是因为团队越阶段跑了模型或实验而否决。相反，working brief 对阶段、零 query、零研究模型／smoke、遗留 exposure 和发布阻塞的披露总体诚实。否决来自四个结构性问题：

1. H5 completion validator 可以在实际 21/21 全部不一致时被手工汇总字段骗成全绿；
2. coder A 声称完成的 21 个页码 locator 中，按冻结提取器只有 9 个 exact anchor 可回放，12 个不可回放；
3. H5 codebook 只有枚举值，没有足以支持独立复编码的操作性定义、优先级和分析单位，且目前没有真正隔离 coder A 值的 blind packet；
4. 旧论文集虽被机械合并为 250 个 work，但至少一篇已在库内的极近邻 `Omni-Decision` 被错误路由成非 direct、非 load-bearing 的 `KNOWN_QUEUE`；另有 AOP-Agent、Light-Omni 等高相关邻居未进入当前 corpus。数量完整不等于科学分类完整。

因此，working brief 第 375 行所称“唯一尚缺的是 H5 coder-B／adjudication”不成立。**coder B 之前还必须修复 codebook、coder A locator 与 completion validator；引用侧还必须重路由直接 prior。**

正式建议值：

```text
CURRENT_ACTIVITY_STAGE = STAGE_1A_FINAL_REMEDIATION
SCIENTIFIC_RATIONALE_FOR_CONTINUING_MAPPING = ADEQUATE
SEARCH_DESIGN_SIGNOFF = WITHHOLD
STAGE_1B_AUTHORIZATION_RECOMMENDATION = NO
ACADEMIC_FRAUD_EVIDENCE = NOT_ESTABLISHED
RESEARCH_INTEGRITY_RISK = HIGH_IF_FALSE_GREEN_PATH_IS_NOT_REPAIRED
```

## 1. 冻结对象、阶段与审查边界

### 1.1 冻结对象

本报告只评审以下 Git blob，不追逐评审过程中工作树可能发生的后续变化：

- commit：`9e708c50be0efae61ef47216b772cc5a6634abd3`
- Git blob：`5ed39cd2f2570914d7f95f62abc34425b85dd971`
- Git-blob SHA-256：`ccb88d6e86af0aafa6b2c342ff06ce361b035d9b7c6cadcaa36bcf372473d6b6`
- bytes：`42933`
- lifecycle：`WORKBENCH_REVIEW_DRAFT`

哈希按 `git show HEAD:<path>` 的原始 blob bytes 计算，不以 Windows 工作树 CRLF 变体为准。

### 1.2 当前究竟处于哪个阶段

现行正典给出的答案没有歧义：

- `Research-Objective.md:14-17`：当前是 Stage-1A final remediation，Stage-1B 未开始且未经授权；首要已知红门为 H5；
- `Research-Methodology.md:15-18`：Stage-1B 只执行 systematic mapping，Stage-2A 才能复现和触碰研究模型；
- `current/status.md:3-6`：Track A 充分、Track B major revision、search-design WITHHOLD，不是 exact-package signoff；
- working brief 自身第 6、9-13、28、311-314、380-388 行也作出一致声明。

所以本轮的准确阶段不是“Stage-1A 已结束”、不是“Stage-1B 正在开始”，而是：

> Stage-1A 的最后整改与签署准备期；Stage-1B 的设计已成形，但执行权限尚未产生。

### 1.3 本轮采用的五轮敌意评审

本报告不是只读散文后给印象分，而是按五轮相互反驳的方式进行：

1. **阶段与权限轮**：寻找任何 query、模型、smoke、指标或 prototype 越界；
2. **科学与 prior 轮**：先利用本地 494 source rows／250 canonical works／90-work bibliography，再以外部官方页寻找直接反例；
3. **语义与诚信轮**：检查负证据修正、reviewer 决定转录、claim 强度和 fraud 风险；
4. **可回放与变异轮**：在 Windows 与规范 WSL2 环境重放 package/PDF/H5 gate，并构造 false-green 反例；
5. **反方复核轮**：分别尝试证明“可以开 Stage-1B”和“完全不能继续研究”，只保留能承受两边反驳的结论。

结论是：研究问题值得继续，但当前 gate 的真实性不足以授权执行。

## 2. 团队这一轮做对了什么

严厉审查不等于否认真实进步。以下整改是正确且应保留的。

### 2.1 阶段声明与 exposure 没有冒进

working brief 第 28、75-80、115、129、151、179、287-289 行清楚地区分了：

- Stage-1A 的设计与校准；
- Stage-1B 的纯 mapping；
- Stage-2A 才产生复现、smoke、headroom、WER、EM 或 prototype；
- 本次 scoped repair 的 query/model/smoke 为零，但 `INHERITED_PRIOR_EXPOSURE` 不归零。

这是正确的阶段纪律。H5 三篇论文的手工校准属于 survey instrument calibration，不是研究模型实验；known-ID metadata/fulltext dereference 也没有被冒充 systematic recall。

### 2.2 接受第四条反例，而没有维护原结论

团队接受上一轮对 DeepVerifier `human_or_dev_label_model_selection=false` 的 `DISAGREE`，改为 `unknown`，并把库存改为 `22 = 4 corrections + 18 active`。reviewer decisions 绑定上一轮报告的 exact blob/SHA，并明确区分 `TEAM_ATTESTATION` 式转录与未来 exact-package reviewer sign。

我没有在本轮发现团队伪造上一轮意见、把 `DISAGREE` 改成 `AGREE`、删除反例或把 metadata 升格为全文机制证据的行为。

### 2.3 包级 gate 对当前红门是诚实的

只读重放结果：

| 检查 | 结果 |
|---|---|
| Windows proposal construction | `PASS` |
| Windows proposal release | `FAIL` |
| release named failures | `EVIDENCE_V7_LEAVES_OR_AGGREGATE_MISSING`; `H5_CALIBRATION_PENDING`; `PROPOSAL_NOT_PROMOTED_TO_ROUND16` |
| Windows current package | `PASS` |
| WSL2 Ubuntu-24.04 + `~/.venvs/speechrl` PDF contract | `PASS` |
| WSL2 draft/release | draft `PASS`; release 仍为上述三项 `FAIL` |

这说明团队没有把 construction PASS 偷换成 release PASS。工作稿第 310、371 行对两者的解释是正确的。

### 2.4 研究问题的层次比早期版本更成熟

RQ-SYS、RQ-MECH、RQ-SUPPLY-MAP、RQ-VERIFY-MAP、RQ-BOUND 已经把 system topology、signal、decision rights、generator coverage、verifier discrimination、selector、信息边界分开。第 106-115 行还明确把 mapping evidence 与 Stage-2 empirical answer 分离。这个结构符合 system-first 研究使命，也避免把“最终准确率上升”错误归因给某一个模块。

## 3. 最高优先级缺陷：H5 gate 可以被错误放绿

### 3.1 当前 validator 并不验证“实际一致性”

`sf_h5_calibration_contract.py:164-201` 只检查：有两个不同 coder id、至少一人声明独立、汇总分母为 21、手填 numerator 在 0-21、rate 与手填 numerator 相符，以及 disagreement row 有三个非空字符串。

它没有从两位 coder 的 42 个 assignment 计算一致／分歧集合，也没有检查：

- `exact_agreement_numerator` 是否等于实际相同 cell 数；
- disagreement inventory 是否与实际不同 cell **exactly equal**；
- `coder_values` 是否等于两份 assignment 的真实值；
- `final_value` 是否属于该 field 的 allowed values；
- adjudicator 是否与 coder A/B 不同；
- 同一 `(paper_id, field)` 是否重复、遗漏或凭空增加；
- 裁决 locator 是否可回放。

### 3.2 两个最小反例均被判为 `[]`

我在内存副本上执行了两个不写文件的 mutation：

```text
FALSE_GREEN_ALL_21_DISAGREE []
FALSE_GREEN_ILLEGAL_ADJUDICATION []
```

反例 A：coder B 的 21 个值全部改成与 coder A 不同，但伪报 21/21 agreement、零 disagreement。`validate_completion()` 返回零 failure。

反例 B：登记一个 disagreement，但 adjudicator id 直接等于 coder A，`final_value="ILLEGAL_VALUE"`。`validate_completion()` 仍返回零 failure。

这不是边缘安全攻击，而是 gate 的核心科学语义没有实现。只要未来有人误填、复制粘贴或过早手工改汇总，H5 就可能“完成”，v7 随后也可能被放行。

### 3.3 必须满足的修复判据

在 coder B 开始之前，团队必须把 completion verdict 改为派生计算而非自报：

1. 对每个 coder 构造唯一的 `(paper_id, field) -> value` map；
2. validator 自行计算 actual-agreement set 与 actual-disagreement set；
3. numerator/rate 若保留，只能等于派生值，不能作为 oracle；
4. disagreement keys 必须与 actual-disagreement set 完全相等，无缺项、额外项和重复项；
5. 每个 `coder_values` 必须逐字等于对应 assignment；
6. `final_value` 必须属于该 field 的允许集合；
7. adjudicator 必须与两位 coder 均不同，并声明未参与两份初始编码和利益冲突；
8. 每个 adjudication 必须有可回放证据 locator；
9. 为上述每一条增加负向 mutation test，包括“全部不一致却报满分”的测试。

未完成这些修复前，当前 H5 单元测试的 5/5 PASS 只能证明它实现了现有弱合同，不能证明 H5 科学 gate 有效。

## 4. 第二个最高优先级缺陷：coder A 的证据 locator 只有 9/21 可回放

### 4.1 工作稿对“完成”的表述过强

working brief 第 32、303、384 行以及 codebook 第 40-41 行都把 coder A 描述为完成 21/21、带 page locators。当前 validator 在 `sf_h5_calibration_contract.py:148-155` 只检查 locator 有 `pdf_page`、整数页码和非空 anchor；它不检查 anchor 是否真的存在于冻结 PDF。

我用团队冻结的 NT Python 3.14.3 / pypdf 6.14.0、同一 `normalized_phrase` 逻辑、ledger 指向的三份 pinned PDF 重放 21 个 anchor：

```text
exact anchor found = 9/21
exact anchor missing = 12/21
```

失败项如下：

| paper | field | page | 当前 anchor |
|---|---|---:|---|
| AudioToolAgent 2510.02995 | latency/action timing | 2 | `issue follow-up tool calls when outputs conflict or remain ambiguous` |
| AudioToolAgent 2510.02995 | output/action modality | 2 | `structured tags to initiate a request and to conclude it` |
| Thinking While Listening 2509.19676 | modality topology | 2 | `front end and positional encoding` |
| Thinking While Listening 2509.19676 | observation granularity | 3 | `audio is segmented into 500ms chunks` |
| Thinking While Listening 2509.19676 | acoustic evidence provenance | 2 | `transformer decoder blocks front end positional encoding` |
| Thinking While Listening 2509.19676 | latency/action timing | 2 | `testing audio and model fixed reason over sampled patch level category traces` |
| Native Active Perception 2606.19341 | modality topology | 2 | `omniagent is a single native omni model` |
| Native Active Perception 2606.19341 | temporal regime | 4 | `iterative observation thought action cycle` |
| Native Active Perception 2606.19341 | observation granularity | 4 | `resolving action into new percept` |
| Native Active Perception 2606.19341 | acoustic evidence provenance | 4 | `environment performs only raw media extraction` |
| Native Active Perception 2606.19341 | latency/action timing | 4 | `at each turn the agent generates the ota triplet autoregressively` |
| Native Active Perception 2606.19341 | output/action modality | 4 | `symbolic operator sampled from actions frames audio clip answer` |

其中多数看起来是合理的概括或多个短语的拼接，不一定意味着字段值错误；但它们不是当前合同下可机械回放的 exact anchor。**“语义上大体对”不能替代“证据 locator 可回放”。**

### 4.2 修复要求

- 将 locator 明确分型为 `exact_text_anchor`、`figure/table/section_locator` 或 `reviewer_paraphrase`，禁止把 paraphrase 冒充 exact anchor；
- exact anchor 必须在 pinned PDF/eprint 与声明的 canonical extractor 上实际命中；
- 对表格、图、公式或 OCR 困难证据，保存页码＋对象编号＋短 evidence excerpt，并说明为何无法 exact match；
- H5 validator 必须调用冻结 extractor contract 对全部 locator 重放，而不能只重放 ToolGate p11；
- 先修复 coder A 的 12 个 locator，再冻结 blind packet；否则 coder B 的后续一致性不能弥补 coder A 证据链不完整。

所以，当前可接受的状态描述应是：

```text
CODER_A_ASSIGNMENTS_PRESENT = 21/21
CODER_A_EXACT_LOCATOR_REPLAY = 9/21
CODER_A_EVIDENCE_BINDING_COMPLETE = NO
```

而不是无条件的 `CODER_A_COMPLETE`。

## 5. 第三个最高优先级缺陷：codebook 尚不足以产生独立可重复编码

### 5.1 枚举表不是操作性 codebook

`modality-specificity-codebook.md:18-24` 给出了七个字段的 allowed values，但没有定义分析单位、判定流程和冲突优先级。视觉检查三篇冻结 PDF 后，至少有以下真实歧义：

- **core vs system**：AudioToolAgent 的 central reasoning model 是 text-only，但整个系统接收音频并调用 audio tools；`modality_topology=text_only` 必须明确是编码“核心”而不是“端到端系统”；
- **within-turn vs cross-turn-session**：同一个用户请求内部的多轮 tool call 是一个 turn、多个 turns，还是 session？coder A 选 `cross_turn_session`，但 codebook 无法让独立 coder 推导同一答案；
- **raw waveform vs learned representation**：是编码 frozen core 看到的表示、tool 看到的输入，还是 environment action 返回的证据？
- **tool_action vs composite**：同时输出思考文本和 tool tag 时，何时选 `tool_action`，何时选 `composite`？
- **post_utterance vs inter_turn**：完整音频结束后发生的 agent action 若属于同一 task loop，二者如何区分？
- **observation granularity**：一个系统同时有 clip、chunk、tool event 和 trajectory 时，何时选最细粒度，何时选 `mixed`？

如果两位 coder 只是各自猜测这些词的含义，agreement 测到的是共同直觉，不是 codebook reproducibility。

### 5.2 blind coding 目前没有可审计隔离

coder A 的 21 个值已公开提交在 current artifact 中，而 working brief 第 320 行只要求 coder B “看不到 coder A 值”，没有提供独立 blind input packet、packet hash、访问边界或 no-access attestation。对默认加载整个仓库上下文的 AI coder 来说，这种口头 blinding 很容易失效。

本审稿人已经看过 coder A 值，**不能再充当 coder B**。应由另一独立 actor 使用最小化 sealed packet：

- 冻结 codebook 与其 SHA；
- 三篇 pinned fulltext identity/SHA；
- 空白 3×7 assignment template；
- locator 规范；
- 不包含 coder A 值、agreement report、既有裁决或含答案的 current artifact；
- packet SHA、发放时间、coder 身份／独立性／未接触 A 值的声明。

这不是要求构造不可伪造的监控系统，而是建立可审计的研究程序。若 codebook 因本轮意见发生任何实质变化，coder A 和 coder B 都必须按新版本重新编码，不能只让 coder B 使用新定义。

## 6. 引用与论文利用审查

### 6.1 总体评价：身份和账本显著改善，但科学路由仍有重大错误

90-work bibliography 的 receipt、年份规则、`query_recall_credit=false` 和 250-node selection complement 是合理的。working brief 也正确承认 bibliography 只是 reviewer orientation subset，不是 Stage-1B denominator，且 D0/D1 metadata 不能支撑 D2 mechanism claim。

但是，`494 source rows -> 250 canonical works -> 90 selected works` 只证明身份去重和机械选择可回放，不证明 direct-prior 分类正确。现有最明显反例就在本地库中。

### 6.2 已收录但严重误路由：Omni-Decision

`current/bibliography.md:73` 把 [Omni-Decision: A Progressive Evidence-State Agent System for Omni-Modal QA](https://arxiv.org/abs/2607.11433) 标为 `KNOWN_QUEUE`；其 official receipt 同时写了 `direct_neighbor=false`、`load_bearing=false`。

但官方摘要明确描述：

- training-free omni-modal QA system；
- query-scoped structured evidence state；
- evidence acquisition、validation、repair、finalization；
- external media/web/computation/verification observations；
- explicit stopping/evidence closure；
- no-state ablation 与 trajectory audit。

这几乎逐项重合 working brief 第 21、40-42、84-98、119-127 行所定义的 system-first external control plane。把它放在非 direct queue，不是“文献还没读深”这么简单，而是 selection predicate 或人工 role assignment 已出现科学语义错判。

要求：在任何 Stage-1B signoff 之前，把该 work 提升为 **direct-system-neighbor / P1 threat**，达到 D2，并建立最小差异矩阵：核心是否冻结、外围是否训练、状态 schema、信息来源、验证信号、decision rights、repair/stop、benchmark、公开代码和可复现性。若 D2 证明摘要造成误导，可以再降级，但必须留下证据化 disposition。

### 6.3 当前 corpus 中遗漏的直接邻居

外部检索发现以下官方身份在本地 survey/current 与 250-node union 中无记录：

1. [AOP-Agent / Agentic Active Omni-Modal Perception for Multi-Hop Audio-Visual Reasoning](https://arxiv.org/abs/2605.28192)：官方摘要声称 open-source Omni-LLM 上的 active perception，hierarchical omni-modal memory、observe-reflect-replan loop，且无需额外训练或 proprietary model。它是对“training-free + omni + agentic external loop”交集的直接威胁，优先级应为 P1/direct，不能等普通 Stage-1B 结果偶然发现。
2. [Light-Omni: Reflex over Reasoning in Agentic Video Understanding with Long-Term Memory](https://arxiv.org/abs/2607.05511)：显式研究 continuous long-horizon multimodal streams、global multimodal state、episodic memory、autonomous action 与低延迟。其是否满足 TF-Strict 需要全文判定，但它直接挑战 H5 的 temporal/state/action 字段，至少应进入 P1 H5 comparator。
3. [LatentOmni](https://arxiv.org/abs/2605.22012)：使用 feature-level supervision 和 latent audio-visual states，显然更接近 trained/white-box boundary，而不是 TF-Strict direct prior。它应作为 P2 boundary comparator 进入 Stage-1B 队列，但不应阻塞本次开门。

处理纪律：这些均是 reviewer-known items，`query_recall_credit=false`；不得回写为 frozen query 的召回。AOP-Agent 应在 Stage-1A gate 前做 targeted D2 direct-prior verification；Light-Omni 先做 D1/P1 route，若摘要级边界无法判定则保留 unresolved 并在 Stage-1B 优先 D2；LatentOmni 可非阻塞进入 P2。

### 6.4 已有 citation chain 是否合理

结论分三层：

- **身份层：基本合理。** 新增五篇 reviewer-known paper 的 official identity 与不计 recall 处理正确；90-work receipts 可离线重建。
- **机制层：仍不充分。** working brief 第 46 行把许多论文列成一串，但没有在正文逐项给出 directness、冻结边界、action rights 和 evidence grade；它自己也承认多数仍是 queue/comparator。该列表只能证明“邻居存在”，不能证明 gap。
- **novelty 层：尚未成立。** working brief 第 46、129 行没有声称 first-ever 或已确立 novelty，这是正确的；但 Omni-Decision 与 AOP-Agent 表明“omni agentic system 本身是第一创新点”仍只能是 founding hypothesis，必须经 1B/1C 收缩为可证伪的最小差异。

因此，Track A 的正确判断是“值得继续 mapping”，不是“创新已经基本确认”。

## 7. 是否存在越过本阶段的探索

### 7.1 没有发现执行层越界

本轮没有证据表明团队执行了 systematic discovery query、研究模型、smoke、dataset metric、headroom、WER/EM、selector experiment 或 prototype。working brief 中 Stage-2 的 matched ablation、MBR、oracle、SESOI 等内容是未来方法边界与 falsifier 预告，没有被写成已冻结实验设计或已完成结果。

因此：

- 没有把“触碰模型”偷放回 Stage-1B；
- 没有在 survey 阶段跑冒烟集；
- 没有用小样结果为某个候选方向拉票；
- 没有在 Stage-1A 设置不当预算 cap；
- H5 手工论文校准属于 Stage-1A 设计验证，不是 Stage-2 实验。

### 7.2 需要防止的另一种越界：把设计工程当成科学完成度

团队这一轮投入大量工作修复 manifest、自引用、registry、DAG 和双平台 gate。这些工作对可回放性有必要，但 `PASS` 只能证明包与规则一致。它不能替代：

- 直接 prior 是否被正确分类；
- codebook 是否能让独立研究者复编码；
- H5 evidence locator 是否真实命中；
- mapping 后是否存在未被占据的研究问题。

后续不要继续无限增加 package machinery。修复本报告列出的科学语义 gate 后，应及时进入 Stage-1B，而不是以“再做一层基础设施”为理由无限延长 Stage-1A。

## 8. 学术诚信与欺诈风险裁决

### 8.1 当前没有足够证据指控学术欺诈

有利于诚信的事实包括：

- 明示 workbench draft，不冒充 formal signoff；
- 明示 H5 pending、release blocked、Stage-1B unauthorized；
- 接受 reviewer 的第四条反例并撤下错误 negative；
- 保留 429、wiki push failure 和 inherited exposure；
- reviewer-known items 不计 query recall；
- construction 与 release 语义分开。

这些行为与蓄意造假不一致。当前应使用的术语是 **高研究诚信风险／结构性假绿**，不是已经证实的 fraud。

### 8.2 但以下表述必须更正，否则会演变为可问责问题

- “coder A complete 21/21”应降级为 assignment present 21/21、exact locator replay 9/21；
- “唯一尚缺 coder B/adjudication”应撤回，因为 validator、locator、codebook 与 direct-prior routing 仍缺；
- “official-receipt bibliography PASS”只能表示书目工程 PASS，不能推出 direct-neighbor coverage PASS；
- H5 completion 的任何未来 PASS 若仍能通过本报告两个 mutation，将不具备可信度。

若团队知悉这些反例后仍用当前 validator 生成 H5 COMPLETE、v7 PASS 或 Stage-1B authorization，性质就会从无意缺陷升级为严重研究诚信违规嫌疑。

## 9. 严格但有限的整改计划

以下计划只修 Stage-1A 开门所必需的内容，不提前做 Stage-1B query，也不触碰研究模型。

### P0-1：先冻结 H5 的真正语义合同

交付物：`modality-specificity-codebook` 新版本＋dated supersession。

最低验收：

- 七字段各有分析单位、正反例、冲突优先级、`mixed/UNKNOWN/NOT_APPLICABLE` 判据；
- 明确 core-level 与 system-level 的编码对象；
- 明确 within-turn/cross-turn、post-utterance/inter-turn、tool/composite 等边界；
- 任一 codebook 实质变更触发 coder A/B 全部重编码。

### P0-2：修复 coder A 证据绑定

交付物：21-cell locator replay report。

最低验收：

- 21/21 locator 在声明的 extractor/version 与 pinned SHA 上可回放；
- exact anchor 与 paraphrase 分型；
- 当前 12 个失败项全部修复或降为带解释的非 exact locator；
- validator 对 locator 实际重放，不仅做非空检查。

### P0-3：修复 H5 completion validator 并做敌意 mutation

交付物：派生 agreement/disagreement 的 validator 与负向测试。

最低验收：

- 本报告两个 false-green mutation 都必须返回明确 failure；
- disagreement set exact equality、coder values binding、allowed final value、adjudicator independence、locator replay 均 fail closed；
- 手改汇总 numerator/rate 不能改变派生结论。

### P0-4：建立真正的 blind coder-B packet

交付物：sealed/minimized packet、SHA、发放与独立性记录。

最低验收：

- packet 无 coder A 值、无既有 agreement/adjudication；
- coder B 完成 21/21 assignment 与独立 locator；
- 第三位 adjudicator 与两位 coder 均不同；
- 实际 agreement 从 assignments 自动计算；
- 全部分歧逐 cell 裁决。

### P0-5：修正最接近 prior 的路由

交付物：direct-prior addendum，不重写 frozen query、不计 recall。

最低验收：

- Omni-Decision 从 `KNOWN_QUEUE/non-direct` 提升并完成 D2 差异矩阵；
- AOP-Agent 登记为 reviewer-known direct threat，targeted D2；
- Light-Omni 登记为 P1/H5 comparator，至少完成边界 triage；
- LatentOmni 登记为 P2 trained/white-box boundary comparator，可留待 Stage-1B；
- working brief 第 46 行的 direct-neighbor 叙述与账本角色一致。

### P0-6：重新生成正式 gate，而不是修文案后直接开门

顺序必须是：

1. codebook／locator／validator 修复；
2. blind coder B＋独立 adjudication；
3. direct-prior routing addendum；
4. 同一冻结 commit 生成 NT 与 POSIX v7 leaves；
5. 独立 aggregator 读取 exact leaf bytes；
6. 重建 source manifest/package report；
7. 晋升 immutable round-16；
8. exact-package independent reviewer `SIGN`；
9. owner 对同包单独授权 Stage-1B。

任何一步不得用“上一轮已经大体认可”替代。

### P1/P2：不应阻塞开门的后续方向

- Stage-1B 优先绘制 Omni-Decision、AOP-Agent、Native Active Perception、AudioToolAgent、Agent-Omni、EChO-Agent 的 method-path proximity；
- 单独比较 explicit evidence state、hierarchical memory、tool loop、terminal reranking 与 sequential control；
- 将 Light-Omni 的低延迟／长时记忆作为 H5 字段有效性的压力测试；
- 将 LatentOmni/ThinkOmni 等内部 latent/logit 方法作为边界 comparator，避免与严格黑盒方法混分母；
- Stage-1C 再决定“omni agentic system”应收缩到哪个最小未占据差异，不在 Stage-1A 预写创新结论。

## 10. 何时可以启动 Stage-1B

不是现在。只有下列全部成立后才可建议授权：

```text
H5_CODEBOOK_OPERATIONAL = PASS
CODER_A_LOCATOR_REPLAY = 21/21_OR_JUSTIFIED_TYPED_LOCATORS
H5_FALSE_GREEN_MUTATIONS = REJECTED
BLIND_CODER_B = COMPLETE
ALL_ACTUAL_DISAGREEMENTS = INDEPENDENTLY_ADJUDICATED
OMNI_DECISION_DIRECT_PRIOR = D2_ROUTED
AOP_AGENT_DIRECT_PRIOR = D2_ROUTED
LIGHT_OMNI_BOUNDARY_TRIAGE = RECORDED
V7_NT_LEAF = PASS
V7_POSIX_LEAF = PASS
V7_AGGREGATE = PASS
IMMUTABLE_ROUND16_PACKAGE = REGISTERED
EXACT_PACKAGE_REVIEWER_SIGN = PRESENT
OWNER_SAME_PACKAGE_AUTHORIZATION = PRESENT
```

满足这些条件后，不需要再发明新的无限 gate，也不应以 P2 bibliography 仍可能增长为由继续拖延。Stage-1B 的第一步应是执行已经冻结的 systematic mapping routes，并继续保持全程零研究模型／零 smoke。

## 11. 最终博导意见

这份 working brief 已经从早期“先预设创新、再找证据”的状态，进步到“先映射占据、允许负结论、再决定最小差异”。这是值得继续的研究方向。团队也没有在本轮伪造一个 release PASS。

但是，**当前最危险的地方恰好位于他们自称唯一红门的 H5：门的输入证据有 12/21 不可回放，门的 codebook 不足以独立复编码，门的 blinding 未真正建立，门的 validator 还能把全量分歧判为全绿。**与此同时，最直接的 training-free omni system prior 已被本地书目错误降级，另一篇极近邻仍在 corpus 外。

所以，本轮裁决必须严厉而明确：

> 科学问题继续；Stage-1A 整改继续；Stage-1B 暂不启动。不是要求团队再堆一层形式主义，而是要求他们让唯一红门真正测量它声称测量的东西，并先正视已经出现的最接近 prior。
