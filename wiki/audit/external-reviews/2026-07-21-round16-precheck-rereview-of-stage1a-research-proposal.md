# 2026-07-21 Stage-1A 收尾提案独立复审：round-16 precheck

## 0. 审查对象、冻结点与裁决

本报告审查以下交付物，并且**不修改研究团队 worktree 中的任何文件**：

- 目标文件：`.worktrees/stage1b-readiness-remediation/wiki/survey/workbench/system-first-stage1a/2026-07-21-research-proposal-for-independent-review.md`
- 审查 worktree HEAD：`55aea3a13a8315e51c70a0aed9633e61a66c8fe4`
- HEAD 时间：`2026-07-21T08:39:47+08:00`
- 目标 Git blob：`464965ff85a7d4a8446a6419023c689fd6aa9308`
- 目标 Git blob SHA-256：`5293c9c8eca499dc6e110f8da9a295ea625450056a787db3e65364aad45f4671`
- 冻结包 `source_commit`：`c62564dafb22af9ea6da78f1858e3ef62118fd3f`
- 核验结果：`c62564d` 与当前 HEAD 中目标文件的 Git blob 相同；不存在以末次状态刷新偷偷改写被审正文的问题
- 审查日期：2026-07-21
- 身份：作者外严格 reviewer / 博导视角；未参与本轮实现，不代替研究 owner 授权

正式裁决：

```text
CURRENT_STAGE = STAGE_1A_FINAL_REMEDIATION
TRACK_A_SCIENTIFIC_RATIONALE = ADEQUATE_FOR_SYSTEMATIC_MAPPING
TRACK_A_PROPOSAL_VERDICT = ACCEPT_WITH_TARGETED_CORRECTIONS
TRACK_B_READINESS_PACKAGE_VERDICT = MAJOR_REVISION
SEARCH_DESIGN_SIGNOFF = WITHHOLD
STAGE_1B_AUTHORIZATION = NO

RESEARCH_INTEGRITY_VERDICT = NO_CURRENT_EVIDENCE_OF_FABRICATION,
                             FALSIFICATION, OR PLAGIARISM;
                             ONE_NEW_LOAD_BEARING_NEGATIVE-CODING_CONFLICT
                             AND THREE_STRUCTURAL_FALSE-ASSURANCE RISKS REQUIRE CLOSURE
```

一句话结论：**研究团队已经把“为什么值得做 system-first mapping”说清楚了，阶段边界也基本修正正确；但它仍处于 Stage-1A 收尾整改，不是 Stage-1B。当前不能执行第一条 systematic discovery query。决定性原因不仅是团队已经披露的四个 release blockers，还包括本轮新发现的一条 DeepVerifier 主动否定证据冲突、一个没有被 package gate 捕获的 H5 校准门，以及 PDF 语义回放环境尚未冻结。**

这不是对研究方向的否定。相反，Track A 已经达到“值得开展 systematic mapping”的水平；被拒绝的是“当前 exact package 已具备启动权限”这一更强命题。

## 1. 当前到底处于哪个阶段

### 1.1 根据未闭合授权链判断，而不是根据文件名判断

现行阶段定义是：

- Stage-1A：研究问题、survey 设计、纳排、编码、证据与开门合同；
- Stage-1B：systematic mapping 执行，全程禁止研究模型和 smoke；
- Stage-1C：证据综合、形成 3–5 张候选问题卡、owner 选题和复现清单冻结；
- Stage-2A：复现先行，复现可用后才进行方向性方案探索；
- Stage-2B：方案验证；
- Stage-3：发表。

目标提案第 6–13 行、第 28–30 行及第 277–294 行均明确承认：文件仍是 `WORKBENCH_REVIEW_DRAFT`，正式 round-16 尚未提交，Stage-1B 未启动、未授权，3 个修正确认和 19 个 active absence review 均为零，fresh v7 leaves/aggregate 尚未生成。这个阶段声明与事实一致。

因此当前状态应精确表述为：

```text
Stage-1A 科学提案：基本形成
Stage-1A survey/readiness 合同：主体形成，但仍有语义和校准门待闭合
Stage-1A immutable signoff package：尚未形成
Stage-1B：未启动、未授权
Stage-2：禁止
```

### 1.2 本轮没有实验性越界

目标提案披露本轮 systematic discovery query、research-model/smoke、dataset metric、headroom 和 prototype 均为 0，并保留 `INHERITED_PRIOR_EXPOSURE`。我没有发现与此相反的执行证据。

提案现在也正确区分：

- Stage-1B 只映射论文已报告的 supply、headroom、ablation 和 attribution；
- 本项目新产生的 headroom、WER、EM、selector 和因果分解属于 Stage-2；
- Stage-1B 只交付 candidate-card evidence inputs；
- 最终 3–5 张问题卡、排名、owner 选题和 reproduction-list freeze 属于 Stage-1C；
- Stage-2A 的第一动作是复现，而不是直接发明新方法。

所以本轮不存在“偷跑实验”的越界。现存问题是 **Stage-1A 的设计和语义门尚未完全可签署**，不是团队已经跨进 Stage-2。

## 2. 审查方法：五轮相互对抗

### Round A：阶段、论证与职责边界

逐段检查中心问题、TF-Strict 边界、RQ、H1–H5、Stage-1B 产出、Stage-1C/2 预告与 gate 表，专门寻找：把 mapping 写成 empirical answer、把 Stage-1C 架空、把局部机器 PASS 写成授权、以及前置预算 cap。

### Round B：仓内论文全集优先的引用闭环

先复核团队已登记的 483 source rows、245 canonical works、85-work reviewer bibliography、selection complement、official receipts 和本地 frozen full text。只有在仓内全集复核之后才补充外部 reviewer-known 邻居。外部发现全部应记 `query_recall_credit=false`，不得倒灌成 frozen query 的召回成绩。

### Round C：否定证据的敌意语义复核

不是检查 JSON 字段是否齐全，而是对 19 条 active absence 逐条问：原文是否存在反向段落？proof locator 是否只挑了支持否定结论的局部？相邻段落是否暴露 model choice、label use、candidate object、new-info 或 decision right？本轮对五个相关 frozen full-text 家族进行了逐项复核。

### Round D：结构门与可达性

检查 proposal、codebook、source manifest、package check 和 release check 的依赖图，寻找“文档声称是 acceptance condition，但机器 release gate 永远看不到”的隐藏红门，以及当 reviewer 给出 `DISAGREE` 后库存能否合法迁移。

### Round E：双平台与提取器差异回放

在 Windows 正典脚本环境和 WSL2 `Ubuntu-24.04` 的 `~/.venvs/speechrl` 环境重放 corpus、bibliography、package 和 proposal gates；另用不同 `pypdf` 版本作非正典诊断，以判断全文 locator 是否真正具备跨环境语义稳定性。

后四轮分别尝试推翻前一轮的积极结论。最终得到的是“Track A 可接受，但 Track B 仍不可签”的分裂裁决，而不是全盘通过或全盘否定。

## 3. 上一轮意见中已经被正确修复的部分

严格审查必须承认真实进展。本轮至少有九项实质闭合。

1. **RQ 不再伪装成 Stage-1B 实验。** `RQ-SUPPLY-MAP` 和 `RQ-VERIFY-MAP` 只询问文献如何构造、报告和分离证据；新 headroom 与因果归因明确后移到 Stage-2。
2. **Stage-1B/1C 边界已修正。** Stage-1B 只输出 evidence inputs、proximity 和 reproduction-readiness evidence；最终问题卡、排名和 owner 决策归还 Stage-1C。
3. **H5 已从口号变成七字段 codebook。** modality topology、temporal regime、observation granularity、acoustic evidence provenance、latency/action timing、output/action modality、state persistence 都有允许值、`UNKNOWN`/`NOT_APPLICABLE` 规则和字段级裁决合同。
4. **systematic mapping 方法学引用已补齐。** Petersen、Wohlin、PRISMA 2020、PRESS 2015、PRISMA-S 均有 adopted element、偏离理由和 artifact 映射，不再只是借用“systematic”一词。
5. **旧论文集利用声明被收窄。** GM-1 只声称 seven registered active corpora 的 lossless union，不再假装 archive 与全部历史材料已经穷尽。
6. **书目选择 oracle 已显著改善。** 245 个 active-union nodes 有逐项 disposition；85 项 reviewer orientation subset 与 159 个 nonpriority queue、1 个 unresolved complement 分开，不再把书目子集冒充 mapping 分母。
7. **上一轮明确指出的邻近文献已进入可见层。** MAV、Thinking While Listening、Omni-Reward、Native Active Perception、Llasa、OmniGAIA、Omni-RRM、Multimodal RewardBench 2 已被显式路由。
8. **年份规则已修正。** `initial_preprint | formal_venue | current_version` 被显式记录，AudioToolAgent、VoiceAgentBench、LATS、PiCSAR 和 Trajectory Optimal Control 的已知年份错配已修复。
9. **团队没有掩盖上一轮三条负证据冲突。** DREAM controller/config 从 `false` 改为 `true`；DREAM human/dev model selection 与 DeepVerifier peripheral update 降为 `unknown`；三条均退出 active absence 并保留更正台账。

本 reviewer 对上述三条更正的判断均为 `AGREE`：

| Retired row | 更正 | 独立判断 |
|---|---|---|
| `ABS2-7f79a2888c7d031e5e74` | DREAM controller/config `false → true` | `AGREE`；label-bearing threshold accuracy 足以推翻负命题 |
| `ABS2-c5351c607c4f37690a34` | DREAM human/dev model selection `false → unknown` | `AGREE`；32B/7B 比较与主实验选择使 `false` 不可承重，但时间顺序不足以直接判 `true` |
| `ABS2-cc432879fce4af753778` | DeepVerifier external component update `false → unknown` | `AGREE`；Qwen3-8B fine-tuning 明确，core/peripheral topology 未冻结时只能 unresolved |

这些判断写在本独立报告中，不代表我已经修改或代填团队的 reviewer schema。团队仍须按其身份、时间和 conflict declaration 合同录入，并重新绑定 exact hashes。

## 4. 科学提案本身是否成立

### 4.1 中心问题现在是博士级问题，而不是 selector 技巧包装

目标提案把研究对象定义为冻结黑盒 omni foundation model 外围的 reward-guided external control plane：观察与供给、状态、记忆、工具、候选扩展、验证、选择、预算、停止和风险控制。best-of-N、MBR、reranking 被正确放在终端动作空间退化情形，而不是充当整个 omni agentic system 的定义。

该定义与项目北极星一致，也解决了早期“把 selector/evaluator 当作创新主体”的偏差。真正值得 mapping 的问题是：既有工作在哪些边界下拥有何种动作权，reward/signal 是否真的沿 LIVE causal edge 改变后续动作，以及 speech/omni 的时序、证据与状态约束是否产生不可由 text-only reranking 代替的结构差异。

### 4.2 研究动机足以支持 Stage-1B，但不支持 novelty 结论

提案第 44–54 行承认 speech/omni agents、trained speech reward 和工具编排已经存在，并明确撤回 `first-ever` 和已确立 novelty。这是正确的。

当前可接受的命题是：

> 现有研究跨越核心/外围训练、terminal/sequential control、read-out/new-info、generator/verifier/selector 和 speech/omni modality topology 等不同边界；在不知道 cell occupancy 前，先做 system-first systematic mapping 是必要的。

当前不可接受的命题是：

> “omni agentic system 本身是第一创新点”已经被证明，或者 TF-Strict cell 已经为空。

目标提案目前只把后者保留为 hypothesis，并设置 direct-prior 等价占据时撤回或缩窄的 falsifier。因此 Track A 的科学理由可以判为 `ADEQUATE`。

### 4.3 H1–H5 仍是 hypothesis-grade，处理方式正确

H1–H5 有 answering stage、Stage-1B evidence product、later empirical test 和 falsifier。尤其 H3 不再把无 headroom 一律归罪于 selector，H4 不再把 trained peripheral/new-info 混入 strict 分母，H5 允许 mapping 失败后合并或撤回 speech/omni specificity。这里没有明显 HARKing 结果，因为 Stage-1B 尚未执行。

后续必须维持 dated amendment：看到 mapping 结果后若改写 H1–H5，必须留下由什么证据触发，不能把事后解释回写成原始预测。

## 5. 引用是否合理

### 5.1 总体判断：从“不可审计”提升到“基本合理”

85-work bibliography 的 title、authors、year 和 identity 来自 official raw receipts，并能离线重建；known-ID access 不计 query recall；书目是 orientation subset 而不是 mapping denominator。目标提案第 200 行也明确承认 metadata 只能证明工作存在，不能证明 mechanism、gap 或 occupancy。这些做法是正确的。

方法学引用与本项目的使用关系也基本合理：

- Petersen 支撑 mapping 的分类与地图产出；
- Wohlin 支撑 backward/forward snowballing；
- PRISMA 2020 支撑流转与排除透明性；
- PRESS 支撑检索策略同行复核；
- PRISMA-S 支撑多数据库/网站检索报告。

团队没有机械照搬医学综述，而是提供 AI/CS/arXiv/T1 的 adaptation table，因此不存在“只引用名词、不采用方法”的主要漏洞。

### 5.2 仍需保留的限定

1. 85 项中的 65 个 frozen carry-forward 主要服务历史连续性，不是独立的科学优先级证据。由于 complement 已披露，这不再阻塞，但不能把“被保留”写成“最相关”。
2. direct-neighbor 多数尚未到 D2。它们只能支持“邻居存在并必须比较”，不能支持 TF-Strict occupancy、机制等价或 novelty gap。
3. `OmniAgent / Native Active Perception` 应在正式记录中分开写清“论文题名”和“论文内方法名”，避免后续 identity 去重把方法名误当论文名。此项为编辑性修正，不阻塞。
4. bibliography PASS 是 citation identity/selection disposition PASS，不是 systematic coverage PASS。后者只能由 Stage-1B frozen queries、snowballing 和 exit mechanism 产生。

## 6. 外部 reviewer-known 补漏

本轮先使用仓内 245-work union 与 85-work bibliography，再进行作者外邻近检索。以下项目截至冻结点未出现在 `wiki/survey/current`。它们不得修改 frozen query，也不得获得 query recall credit；正确做法是以 reviewer-known/P1/P2 入口登记并给出 disposition。

### P0/P1：Stage-1B 前必须显式处置

1. **[Sandboxed Coding Agents are Competitive Omni-modal Task Solvers](https://arxiv.org/abs/2606.00579)**，Chen et al., 2026。
   - 论文直接比较仅具 text+image 接口的 sandboxed coding agents、native omnimodal models 与既定 multimodal scaffolds；
   - 其系统通过代码和工具从 transcript、frame 与其他 modality signals 抽取证据；
   - 它直接挑战 H5 中“native omni specificity”、`read-out/new-info`、工具编排和 modality topology 的假设；
   - 应登记为 `DIRECT_SYSTEM_NEIGHBOR + H5_DIRECT_THREAT + REPRODUCTION_READINESS_CANDIDATE`；至少 D1 路由，若要支撑/推翻 H5 必须 D2。

2. **[Inference-Time Scaling for Joint Audio-Video Generation](https://arxiv.org/abs/2606.03183)**，Jung et al., 2026，TMLR accepted。
   - 它不是 agent 系统，因此不应占据 RQ-SYS 核心 cell；
   - 但它是直接的 multimodal training-free ITS、多 verifier、reward aggregation 与 verifier hacking comparator；
   - 应进入 `BOUNDARY_COMPARATOR / MEASUREMENT_AND_MULTI-VERIFIER_THREAT`，约束 RQ-MECH、RQ-VERIFY-MAP 和 H4。

3. **[Agentic Reward Modeling: Integrating Human Preferences with Verifiable Correctness Signals for Reliable Reward Systems](https://arxiv.org/abs/2502.19328)**，Peng et al., 2025。
   - RewardAgent 组合 human preference reward 与 verifiable correctness signals，并报告 inference-time best-of-N；
   - 后续还用这些信号构造 DPO 数据，因而同时跨越 inference-time 与 trained boundary；
   - 应作为 `REWARD/VERIFIER SYSTEM COMPARATOR`，用于防止把“多个奖励源 + best-of-N”误写为本项目独有结构。

### P2：进入 known queue，不阻塞开门

4. **[TMAS: Scaling Test-Time Compute via Multi-Agent Synergy](https://arxiv.org/abs/2605.10344)**，Wu et al., 2026。
   - 多 trajectory、refinement、verification feedback、hierarchical memory 与 hybrid reward training 对 system topology 有参考价值；
   - 因包含 reward training，通常不是 TF-Strict 候选；作为 trained system comparator 即可。

5. **[AgentTTS: Large Language Model Agent for Test-time Compute-optimal Scaling Strategy in Complex Tasks](https://arxiv.org/abs/2508.00890)**，2025。
   - 与 agentic test-time compute allocation、策略选择和复杂任务控制相关；
   - 可作为 text-domain/budget-control known queue，由 Stage-1B 决定是否升 D2。

这些遗漏不证明 frozen search design 失败，因为 systematic queries 尚未执行；但第一项是高度直接的 2026 omni-agent 邻居。已知后仍不登记，会构成选择性覆盖。正确处置不会破坏 frozen query：新增 reviewer-known receipt、`query_recall_credit=false`、明确 role 和下一步深度即可。

## 7. Major finding 1：H5 有一个未被 release gate 看见的校准门

`wiki/survey/current/modality-specificity-codebook.md` 第 35–49 行明确写道：

- 三个 calibration examples 应在 Stage-1B execution 之前处理；
- 必须有三条 completed dual-coded rows；
- 必须报告 field-level agreement；
- 每个 disagreement 必须 adjudicate；
- 在此之前 H5 只是 mapping hypothesis，而不是 finding。

当前文件中的 AudioToolAgent、Thinking While Listening、Native Active Perception 三行仍是 provisional pattern，大多数值是 `UNKNOWN until D2`。仓内没有找到三条 completed dual-coded calibration rows、字段级 agreement report 或 disagreement adjudication artifact。

问题不只在“尚未完成”，而在于该 acceptance condition 没有进入：

- proposal 第 277–294 行的 gate table；
- `proposal-source-manifest-v1.json` 的 release requirements；
- `proposal-package-check.json` 的 blockers；
- `sf_reviewer_proposal_check.py --mode release` 的 failure codes。

所以机器可以在 H5 明文 acceptance condition 未满足时仍把 construction 报为 PASS，并且在其他四门闭合后理论上放行 release。这是**隐藏门/合同不可达**，不是普通文档遗漏。

必须二选一：

1. 推荐方案：在 Stage-1A 收尾完成三篇纸面 D2 双编码校准，形成独立 artifact，进入 source manifest 与 release checker；不运行模型、不执行 systematic query，因此不越界。
2. 若团队坚持校准是 Stage-1B 的第一步，就必须删除“before Stage-1B execution”的 acceptance 语义，把它重写为 Stage-1B 内部 stop-before-load-bearing gate。但这会允许未校准 codebook 开始系统编码，风险更高，不推荐。

本 reviewer 要求采用方案 1。

## 8. Major finding 2：19 条 active negatives 中仍有一条不能 `AGREE`

### 8.1 冲突行

```text
adjudication_row_id = ABS2-216d90876d8397734c37
method_path_id = 2026.findings-acl.1243#closed-prompt-only
field = human_or_dev_label_model_selection
encoded_value = false
reviewer_verdict = DISAGREE
required_recode = unknown, unless stronger temporal evidence proves true or false
```

当前 proof reason 声称：完整 workflow 没有 human/developer 根据 labeled development outcomes 选择 model checkpoint。它列出的 locator 包含论文第 6 页“主要使用 Claude-3.7-Sonnet 作为 backbone”，但没有处理同一冻结全文的反向证据：

- 第 4 页明确说选择 Claude-3.7-Sonnet 是因为它在该 setting 中表现强；
- 第 6 页说明主要使用 Claude-3.7-Sonnet，并比较 GPT-4.1 与 Qwen3-8B；
- 第 8 页给出不同 backbone models 的带标签 accuracy 比较；
- 第 4 页还说明 taxonomy 来自 human reference traces、两名 research staff 的独立标注和 555 个 error points。最后一项主要证明 controller/rubric label dependence，不能单独证明 model selection，但它说明该方法链并非没有 label-bearing development evidence。

这些证据仍不足以断言正式的 labeled-dev checkpoint selection 确实发生在部署冻结之前，所以本 reviewer 不判 `true`。但“due to its strong performance in this setting”加上跨 backbone 的有标签比较，已经足以推翻承重 `false`。最保守且正确的值是 `unknown`。

当前 proof locator 的问题是**只列支持自己结论的 workflow 段落，没有登记同页或相邻实验段落的反向证据**。正式 absence schema 应新增：

- `counterevidence_search_scope`；
- `counterevidence_locators`；
- `temporal_order_resolved = true|false`；
- `why_counterevidence_does_not_change_verdict`。

否则“有 locator”仍可能演化成 selective locator，而不是全文级否定证据。

### 8.2 对 19 条 active rows 的本轮逐项裁决摘要

`AGREE` 只表示该特定负字段在当前冻结方法路径下未发现新的反证，不表示整篇论文所有编码均被批准。

| Row | Reviewer verdict | 说明 |
|---|---|---|
| `ABS2-2d2291b9ba06d002e93e` | `AGREE` | DeepVerifier closed path 是单一当前答案的 sequential revision，无显式 scored/ranked/voted pool |
| `ABS2-216d90876d8397734c37` | **`DISAGREE`** | backbone 选择“due to strong performance”与跨 backbone labeled comparison 使 `false` 不可承重 |
| `ABS2-49b8c920cf44c2045df6` | `AGREE` | closed path 无并列 candidate object；terminal action 是 accept/retry |
| `ABS2-1392014ff32270df1e5e` | `AGREE` | open-SFT inference path 同样是单答案 sequential revision |
| `ABS2-58b7d1b9a43299821296` | `AGREE_WITH_CAUTION` | open variant 固定 Qwen3-8B，未见以 labeled outcome 选 checkpoint；但应保留 counterevidence scope |
| `ABS2-cf6ae4d082096066fee4` | `AGREE` | open variant 无 selector 比较的候选对象 |
| `ABS2-42aa814a2dfee7a92dbc` | `AGREE` | data-analysis pipeline 处理 task-provided dataset/artifacts，未见外部新信息通道 |
| `ABS2-359542ede39fa005cfea` | `AGREE` | Random-K 是供给侧随机抽样，不是 taxonomy 中的 score/rank/vote selector |
| `ABS2-c7939c7436a6a9d9419c` | `AGREE` | Random-K 未见 human/dev labeled model selection |
| `ABS2-f431a625273dfcd73698` | `AGREE` | sampled summaries 是 refinement supply，不是 winning object |
| `ABS2-9cf174bd899f3a803b87` | `AGREE` | isolated RTV terminal selection 后无 downstream decision right；需维持 terminal operator 与 rights 分离 |
| `ABS2-527adf4083786f6bb14b` | `AGREE` | RTV 明确不读取 ground-truth outcomes，未见 human/dev model choice |
| `ABS2-7df15f9b05eaddde17f0` | `AGREE` | combined RTV-PDR recipe 同样未见 labeled model choice |
| `ABS2-69fabfb31c97e102af00` | `AGREE` | AutoTTS 的 controller/beta 是自动 accuracy optimization；这属于 controller label optimization，不是 human model selection |
| `ABS2-6bbe536f564a90af9deb` | `AGREE` | deployed controller 读取当前 task branch/probe/budget，未见 retrieval/database 新信息 |
| `ABS2-481b25ff36e49a4d2088` | `AGREE` | ToolGate 对一个 pending call 作 execute/skip，不构造 candidate pool |
| `ABS2-e9b7f915e84ac3072514` | `AGREE_WITH_CAUTION` | labels 自动生成，未见 human/dev checkpoint selection；仍应披露模型/正则选择的搜索范围 |
| `ABS2-94932b7d979683355098` | `AGREE` | tools 读取 task-provided image，属于 read-out，不是 external new-info |
| `ABS2-eade5e5123c0eecf41e9` | `AGREE` | execute/skip gate 没有 taxonomy 定义的 pool selection object |

因此本轮不是 `19/19 AGREE`，而是：

```text
CORRECTION_CONFIRMATIONS = 3 AGREE
ACTIVE_ABSENCE_REVIEW = 18 AGREE_OR_AGREE_WITH_CAUTION + 1 DISAGREE
EXPECTED_INVENTORY_AFTER_ACCEPTED_RECODE = 22 = 4 corrected/retired + 18 active negatives
```

团队必须先改 owner row/sidecar 或降级为 `unknown`，再重建 absence artifact、row hashes、occupancy、source manifest 和 proposal。不得为维持 `22 = 3 + 19` 而拒绝 reviewer disagreement。

## 9. Major finding 3：`19` 被硬编码为快照，也可能变成抵抗更正的结构

当前以下位置把 active absence 数量直接写死为 19：

- `sf_absence_provenance_migrate.py`；
- `sf_identity_taxonomy_v7_test.py`；
- `sf_reviewer_proposal_check.py`；
- `sf_proposal_source_manifest.py`；
- `test_sf_absence_provenance_migrate.py`；
- `test_sf_reviewer_proposal_check.py`；
- current status、semantic correction ledger 和 proposal manifest。

在一个冻结版本中断言 exact 19 是合理的，它能阻止 silent deletion；但 reviewer 一旦合法 `DISAGREE`，系统必须有**版本化库存迁移路径**。否则测试会把旧数字当作语义真相，并制造“改对数据反而测试红”的激励。

修复要求：

1. 保留旧 v2 artifact 的 19 作为不可变历史快照；
2. 接受本轮 DISAGREE 后生成新版本 artifact，登记 `22 = 4 + 18`；
3. release checker 的分母从同一冻结 correction/active inventory 计算，或由 versioned manifest 显式给出；
4. 测试断言“总数守恒、每次迁移有 supersession、无 silent deletion”，而不是跨版本永远断言 19；
5. proposal 的 promotion trigger、v7 leaf trigger 和 review coverage denominator 同步迁移。

这不是要求把所有数字都动态化。要求的是：**快照数字可以硬，但语义更正必须有合法换版机制。**

## 10. Major finding 4：PDF 语义回放依赖未冻结的提取器版本

本轮回放结果：

### Windows 正典脚本环境

```text
Python 3.14.3
pypdf 6.14.0
132 focused tests: PASS
proposal construction: PASS
proposal release: expected FAIL
```

### WSL2 正典研究环境

```text
Ubuntu-24.04
~/.venvs/speechrl
Python 3.12.3
pypdf 6.14.2
existing corpus: PASS (483 rows, 0 unexplained orphans)
bibliography: PASS (85 unique works)
proposal construction: PASS
draft: PASS
release: FAIL with four registered blockers
```

### 非正典诊断环境

```text
Codex bundled Python 3.12.13
pypdf 6.10.0
132 focused tests: 130 PASS, 2 FAIL
unexpected failure: ToolGate p11 page anchor missing
package construction: FAIL because V7 failure set gained LOAD_BEARING_CONTRACT
```

这不证明团队的正典环境已经失败，也不应把 Codex bundled runtime 当成项目指定环境。但它证明一个结构事实：相同 PDF bytes 与相同 locator，在不同 `pypdf` minor versions 下可得到不同语义检查结果。当前 v7 platform stamp 记录 OS/Python，却没有把 PDF extractor version 作为 leaf 的显式、受签名输入。

正式双平台 leaves 之前必须：

- 冻结 Windows 与 WSL 的 `pypdf` 版本或锁文件；
- 在 leaf provenance 中记录 `pypdf.__version__`、extractor identity 和必要时规范化算法版本；
- source manifest 绑定该环境合同；
- 若允许多个 extractor version，则必须预先定义“任一失败即 fail”还是“指定版本为正典”，不能在运行后选择能过的一边；
- 更稳健的长期方案是生成并 SHA 绑定 normalized page-text artifact，同时保留 PDF bytes 为上游正典。

这属于可回放性，不是元数据篡改鲁棒性测试，因而是 Stage-1A 的正当结构要求。

## 11. 机器回放与现有四个红门

在规定 WSL venv 中，release checker 返回：

```text
ABSENCE_REVIEW_PENDING
EVIDENCE_V7_LEAVES_OR_AGGREGATE_MISSING
PROPOSAL_NOT_PROMOTED_TO_ROUND16
SEMANTIC_CORRECTION_REVIEW_PENDING
```

这证明 fail-closed 主体有效，也证明 construction PASS 不是 Stage-1B readiness。

在本轮报告之后，第一项不能简单通过填 19 个 `AGREE` 消失；必须先处理 `ABS2-216d90876d8397734c37` 的 `DISAGREE`。此外还应新增：

```text
H5_CALIBRATION_PENDING
PDF_EXTRACTOR_ENVIRONMENT_UNFROZEN
REVIEWER_KNOWN_DIRECT_NEIGHBOR_DISPOSITION_PENDING
```

其中 H5 和 extractor 是 release blockers；新增文献中至少 `2606.00579` 的 disposition 是 search-design signoff blocker。P2 known queue 不要求全都 D2，不应无限扩大 Stage-1A。

## 12. 研究范畴是否超越本阶段

| 内容 | 裁决 | 理由 |
|---|---|---|
| system-first 中心问题 | 未越界 | Stage-1A 应定义研究对象与 mapping 价值 |
| H1–H5 | 未越界 | 明确为 hypothesis-grade 且有后续 falsifier |
| 七字段 H5 codebook | 未越界 | 论文编码合同，属于 survey 设计 |
| 三篇纸面 calibration | 未越界且应补做 | 只读 frozen full text、双编码和裁决，不运行研究模型 |
| Stage-1B reported headroom/ablation mapping | 未越界 | 映射论文报告，不产生本项目实验结果 |
| Stage-2 headroom/MBR/selector 预告 | 可保留 | 作为阶段边界与未来测量纪律，不得现在执行 |
| Stage-1C cards/ranking/owner selection | 已正确后移 | 不再是 Stage-1B 产出 |
| Stage-2A reproduction-first | 正确 | 当前不执行 |
| systematic query | 当前禁止 | 必须等 exact package signoff/owner authorization |
| model/smoke/prototype | Stage-1B 也禁止 | 最早在 Stage-2A 复现阶段发生 |
| 前期 budget cap | 不应新增 | 当前仍需广度 mapping；提案没有重犯此问题 |

所以本轮不能批评团队“研究内容过于宽”本身。Stage-1A 的使命就是把搜索空间、证据轴和反例空间组织清楚。应收紧的是可签署合同，不是提前压缩未来探索预算。

## 13. 学术诚信与是否涉嫌造假

### 13.1 当前没有足够证据指控学术欺诈

理由很明确：

- 没有实验结果可被捏造，因为本轮没有模型实验；
- 团队没有声称 Stage-1B 已启动；
- 429、known-ID access、历史 exposure 和 wiki publish incident 都有披露；
- 上一轮三条不利语义结论被团队主动改正，没有为保持漂亮 occupancy 强行通过；
- release checker 现在确实拒绝放行，而不是把红门包装为总 PASS。

这些行为与蓄意 fabrication/falsification 的模式不一致。

### 13.2 但一条新的有偏编码风险已经实质成立

`ABS2-216...` 的 proof reason 使用“exhaustively names”作强否定，却没有处理原文同页的 performance-based backbone choice。这是实质性 selective-evidence 风险，不是措辞瑕疵。

当前仍不能称为造假，因为：

- 该行明确处于 `READY_FOR_REVIEW`；
- reviewer row 仍为 0，而不是伪造 `AGREE`；
- package 仍 blocked。

但是，如果团队在收到本报告后仍：

1. 不登记上述反向 locator；
2. 为维持 19 而填入 `AGREE`；
3. 用机器测试通过替代语义解释；或
4. 在正式 proposal 中继续将其作为承重 `false`；

那么风险将从“待纠正的有偏编码”升级为“明知反证仍维持有利结论”，届时就会接近 falsification/研究者自由度滥用，必须启动更高等级诚信调查。

### 13.3 当前诚信风险排序

| 风险 | 等级 | 当前处置 |
|---|---|---|
| active negative 与冻结全文冲突 | 高 | 一条 `DISAGREE`，先更正再生成证据 |
| hidden H5 acceptance gate | 中高 | 纳入 release contract |
| extractor version 可改变 locator verdict | 中高 | 冻结环境并写入 leaf provenance |
| reviewer-known direct omni neighbor 缺失 | 中 | 登记，不计 query recall；至少 D1 disposition |
| draft PASS 被误称 readiness | 中低 | 文档目前主动区分，继续保留 guard |
| fabrication/plagiarism | 未发现证据 | 不作无证据指控 |

## 14. 给研究团队 AI 的强制整改 proposal

以下顺序不可颠倒；任何一步都不授权执行 systematic query 或研究模型。

### P0-1：接受并处理新的 DeepVerifier `DISAGREE`

交付：

- 为 `ABS2-216d90876d8397734c37` 登记 reviewer `DISAGREE` 及本报告 locator；
- 把 `human_or_dev_label_model_selection` 从 `false` 降为 `unknown`，除非提供能解析时间顺序的更强全文证据；
- 更正 owner sidecar、generated row、row hash、correction ledger 和 occupancy；
- 形成 versioned `22 = 4 corrected + 18 active` 库存；
- 保留旧 `22 = 3 + 19` artifact 为历史，不原位抹除。

验收：旧 active row 不再承重；所有分母、触发器和 proposal state 来自新版本 exact package。

### P0-2：把 negative review 从“支持 locator”升级为“反证搜索”

交付：每条负证据增加 counterevidence scope、locator、时间顺序是否可解析和为何不改变 verdict。对两条 `AGREE_WITH_CAUTION` 做一次专门复核。

验收：reviewer 能看到支持与反对该 negative 的证据，不需要自己猜实现者是否跳过了相邻段落。

### P0-3：完成 H5 的三篇纸面校准

交付：

- AudioToolAgent、Thinking While Listening、Native Active Perception 三个 frozen full-text identity；
- 两名独立 coder 的 3 × 7 原始字段值与 locator；
- field-level agreement 分子/分母；
- 每个 disagreement 的独立裁决、最终值与理由；
- codebook version、artifact hash 和 source-manifest binding。

验收：`H5_CALIBRATION_PENDING` 进入 release checker，三行真正完成前不能 release。不得运行模型或把 calibration 当 occupancy finding。

### P0-4：登记新的 reviewer-known 直接邻居

最低交付：

- `2606.00579`：P1 direct system/H5 threat，至少 D1；
- `2606.03183`：multimodal ITS/multi-verifier boundary comparator；
- `2502.19328`：agentic reward/best-of-N comparator；
- `2605.10344`、`2508.00890`：P2 known queue，可不升 D2。

所有项目必须 `query_recall_credit=false`，有 official identity receipt、role、next action 和不阻塞/阻塞理由。不得改 frozen query 来伪装预先召回。

### P0-5：冻结全文语义提取环境

交付：

- Windows/POSIX interpreter 与 `pypdf` 版本合同；
- extractor identity 进入 v7 leaf 和 source manifest；
- ToolGate p11 locator 在两个正典环境中的回放 receipt；
- 对不支持版本的明确 fail-fast，而不是运行后择优解释。

验收：同一 PDF SHA、同一 extractor contract 在 Windows/WSL 返回同一 locator verdict 和 occupancy；环境差异可归因。

### P0-6：完成剩余正式语义录入并重建 v7 DAG

顺序：

1. 录入 3 条已同意的 correction confirmations；
2. 录入 18 条可同意 active rows；
3. 处理 1 条 DISAGREE 并换版；
4. 在新 exact package 上生成 Windows leaf；
5. 在同一 package 上生成 WSL/POSIX leaf；
6. 最后生成 aggregate；
7. 任一 leaf 或 aggregate 失败即停，不得继续 promotion。

### P0-7：重建正式 source manifest 与 round-16 package

必须绑定：proposal、protocol、status、methods adaptation、H5 calibration、reviewer-known dispositions、negative corrections/active reviews、extractor contract、NT/POSIX leaves、aggregate、compiler/routes/templates、attempt/exposure ledger。

验收：construction PASS、release PASS 分开；正式 proposal promotion 后 blob 不再变化。

### P0-8：职责分离与最终授权

1. semantic reviewer 只给语义判断；
2. implementer 根据 `DISAGREE` 修上游；
3. machine gate 只检查 exact bindings；
4. independent reviewer 对 immutable round-16 package 决定 `SIGN|WITHHOLD`；
5. reviewer SIGN 后，owner 才能对同一 package 单独授权 Stage-1B。

任何角色不得在一个提交中同时“修数据、填写独立同意、生成 aggregate、宣布授权”。

## 15. Stage-1B 开门矩阵

| Gate | 当前状态 | 裁决 |
|---|---|---|
| 科学问题与 mapping 理由 | `ADEQUATE` | 通过 |
| RQ mapping/empirical 分层 | `PASS` | 通过 |
| Stage-1B/1C/2 职责边界 | `PASS` | 通过 |
| 方法学引用与 adaptation | `PASS` | 通过 |
| GM-1 registered active corpus union | `PASS_WITH_SCOPE_QUALIFIER` | 通过，不能泛化为全部 archive 完备 |
| bibliography identity/selection disposition | `PASS_WITH_ADDITIONS` | 新 reviewer-known 项需登记 |
| 三条旧 correction semantics | `3/3 REVIEWER AGREE IN THIS REPORT` | 待正式 schema 录入 |
| active absence semantics | `18 AGREE + 1 DISAGREE` | **阻塞** |
| negative inventory migration | `MISSING` | **阻塞** |
| H5 codebook fields | `PASS` | 保留 |
| H5 three-paper calibration | `MISSING` | **阻塞** |
| cross-platform Git substrate | `PASS` | 保留 |
| PDF extractor environment contract | `INCOMPLETE` | **阻塞** |
| fresh v7 NT/POSIX leaves + aggregate | `MISSING/WITHHELD` | **阻塞** |
| pre-review proposal construction | `PASS_IN_CANONICAL_ENVIRONMENTS` | 不是 release |
| proposal release | `FAIL` | **阻塞** |
| immutable round-16 proposal | `MISSING` | **阻塞** |
| independent exact-package signoff | `MISSING` | **阻塞** |
| owner exact-package authorization | `MISSING` | **阻塞** |

最终开门条件：

```text
SCIENTIFIC_RATIONALE_ACCEPTED
AND DEEPVERIFIER_DISAGREE_RECODED
AND NEGATIVE_INVENTORY_VERSION_MIGRATED
AND ALL_REMAINING_NEGATIVE_ROWS_REVIEWED
AND H5_THREE_PAPER_CALIBRATION_PASS
AND DIRECT_REVIEWER_KNOWN_ITEMS_DISPOSITIONED
AND PDF_EXTRACTOR_ENVIRONMENT_FROZEN
AND SAME_PACKAGE_NT_LEAF_PASS
AND SAME_PACKAGE_POSIX_LEAF_PASS
AND FINAL_AGGREGATE_PASS
AND SOURCE_MANIFEST_RELEASE_PASS
AND IMMUTABLE_ROUND16_REGISTERED
AND INDEPENDENT_REVIEWER_SIGNED_EXACT_PACKAGE
AND OWNER_AUTHORIZED_EXACT_PACKAGE
```

当前至少有多个合取项为假，所以答案只能是：

```text
MAY_START_STAGE_1B = NO
```

## 16. 最终评价

这份提案相较上一冻结版有实质进步。它已经不再把局部 selector 当作整个研究对象，不再把 Stage-1B 变成偷跑实验，不再把 Stage-1C 的问题卡和 owner 选题前移，也不再靠一份不可解释的短书目证明 novelty。system-first external control plane 的研究问题具有足够博士价值，继续 systematic mapping 是合理的。

但博士级研究治理不能只奖励“愿意承认红门”，还必须验证红门覆盖了所有承重条件。当前最大的问题不是少了一段漂亮论述，而是：一条 active negative 仍被原文反证挑战；H5 codebook 自己定义的校准门不在 release DAG；全文语义 locator 对 extractor version 敏感；新出现的直接 omni-agent 邻居尚未路由。它们都可以在 Stage-1A 通过读论文、编码、裁决和冻结环境解决，不需要也不允许跑模型实验。

因此本轮最严厉但准确的结论是：

> **Track A 的科学理由可以接受；Track B 的 readiness 仍需 major revision。团队当前没有学术欺诈证据，但存在一条必须纠正的有偏否定编码。先完成语义更正、H5 校准、环境冻结和正式证据 DAG，再提交 immutable round-16；在独立签署与 owner 授权之前，不得开始 Stage-1B。**
