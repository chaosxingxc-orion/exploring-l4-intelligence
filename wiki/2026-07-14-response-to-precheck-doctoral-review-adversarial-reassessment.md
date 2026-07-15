---
title: "Stage-1A Response to Precheck Review — Doctoral Adversarial Reassessment"
date: 2026-07-14
review_type: "STAGE1A_RESPONSE_AUDIT_AND_CROSS_TASK_NOVELTY_REASSESSMENT"
reviewer_role: "strict_external_reviewer_and_doctoral_supervisor"
reviewed_artifact: "wiki/2026-07-14-response-to-precheck-doctoral-review.md"
reviewed_artifact_commit: "0be1285e9242d195039b5fd3bc5425b1d741499c"
reviewed_artifact_sha256_git_blob: "7033539fed07906e534ad22844d4d9b864b560e3c884bbf75c3ed5157760136e"
verified_evidence_snapshot_umbrella: "d3ccae6587e1d46059a9681e2f33f984ae3325bc"
verified_evidence_snapshot_w1: "a532da06296681b3bbb30446a6fa285ca5bed508"
verified_prior_review_path: "wiki/2026-07-13-reviewer-precheck-survey-design-and-record-closure-doctoral-review.md"
verified_prior_review_commit: "25cffa9b06f7b36289b931bd6b73a8a8d4204542"
verified_prior_review_sha256_git_blob: "cd56af0095d06b2e6197572e6e899e53ea460fde6625fe7f2b8a9f9eb0cbb3bf"
stage_interpretation: "STAGE_1A_PROBLEM_DEFINITION"
overall_verdict: "ACCEPT_DIRECTION_WITH_TARGETED_RECORD_AND_SURVEY_CORRECTIONS"
reasoned_modification_verdict: "ACCEPT_BREADTH_FIRST_STAGE1A_EXPLORATION_KEEP_NOVELTY_PROVISIONAL"
record_closure_verdict: "NOT_REQUESTED_AND_NOT_ACHIEVED"
stage1a_continuation: "ALLOWED"
stage1b_release: "NOT_AUTHORIZED"
ffp_finding: "NOT_ESTABLISHED"
qrp_control_risk: "MODERATE_TRANSITIONAL_RECORD_CONTROL"
owner_clarification_record_policy: "append-only wording is being unified under a hot/cold context policy; do not treat the transition as misconduct"
owner_clarification_research_mode: "current work is breadth-first model-and-dataset exploration; convergence is explicitly later"
owner_clarification_scientific_status: "optimization opportunity is sufficiently motivated for continued exploration; technical solution and novelty boundary remain open"
---

# 对研究团队 2026‑07‑14 response 的严格博导式复审

> **结论先行。** 在 owner 进一步澄清“当前仍是 breadth-first 的 Stage‑1A 探索、收敛在后”之后，这份 response 的主方向应当接受：用多个模型、数据集和任务作为搜索底座，主动寻找已有相似工作、可迁移机制、SOTA 与可能提升点，是当前阶段的正确工作，而不是过早收敛。团队也正确接受了“不签 record closure、不放行 Stage‑1B、不确认新颖性”，正确重算了 57/46 文献去重并保全五处 raw→canonical 状态值。

仍需校正的是证据措辞，而不是探索范围：没有 raw query log 的 P0‑SURV‑1 不能整体标 `CLOSED`；首轮未命中的 SER/SLU/spoken‑QA 等 cell 应标 `UNDERSEARCHED`，不能标“仍空”；“广度是护城河”如果只是内部探索直觉可以保留为工作假设，如果作为已证新颖性则过强。append-only 方面，owner 已澄清团队正在以冷热层制度统一调整旧规则，因此本报告将其降为**过渡期记录政策不一致**，不再作为本轮诚信主线。

本轮裁决为：

- **response 总体方向：接受，附有针对性记录与 survey 校正；**
- **breadth-first 跨模型、跨数据集、跨任务探索：确认符合当前 Stage‑1A；**
- **相似工作：应视作路线、baseline 和可复用经验，不应只当 novelty killer；**
- **“非 ASR cell 仍空”：改为 `UNDERSEARCHED`；已有反例意味着必须扩展 survey；**
- **“广度是护城河”：可作工作假设，不可作为当前已确认贡献；**
- **`training-free RL + frozen omni + agentic system`：是有潜力且目前可保留的组合创新假设，但需要面对极近邻工作；**
- **Stage‑1A 可继续广泛探索；Stage‑1B 仍未放行；FFP 不成立；记录风险是过渡期中等控制风险。**

---

## 1. 审查边界与 Stage‑1A 标准

这仍是 Stage‑1A 问题界定，不是论文终审。故本报告不要求团队现在交付：

- 大样本显著性检验；
- 配对 bootstrap CI；
- Stage‑2 SESOI 冻结；
- 全矩阵实验；
- 论文级复现。

本轮必须审清的是：

1. 上一轮 P0 声称是否与实际工件一致；
2. 57/46 ledger 是否仅能复算“计数”，还是已能支持“覆盖/空白”；
3. “跨模型×任务兑现面”到底是科学问题、评估框架，还是把已知机制铺到更多数据集；
4. 所谓“同一 selector”是否有可操作定义；
5. 跨任务 `rho(c)` 是否可识别、可比较；
6. categorical integrity statements 是否为真。

本报告没有修改 response、ledger、Decision‑Log、Research‑Objective、Per‑Work‑Status、代码或任何实验工件。

---

## 2. 独立证据复算结果

## 2.1 Provenance

| 项目 | 团队声明 | 独立复核 | 裁决 |
|---|---|---|---|
| 本 response commit | artifact 提交后可复算 | `0be1285e9242d195039b5fd3bc5425b1d741499c` | VERIFIED |
| 本 response git-blob SHA256 | frontmatter 未回填 | `7033539fed07906e534ad22844d4d9b864b560e3c884bbf75c3ed5157760136e` | MISSING_IN_ARTIFACT |
| response evidence snapshot | umbrella `d3ccae6…` / W1 `a532da0…` | response commit 的 parent 正是 `d3ccae6…`；W1 匹配 | VERIFIED |
| responds-to review commit | `25cffa9` | 匹配 | VERIFIED |
| responds-to review git-blob SHA256 | `cd56af…` | Python 直接读取 Git blob 与 LF 工作树均得到 `cd56af…` | VERIFIED |

说明：一次 PowerShell 文本管道会重编码 `git show` 的 UTF‑8 内容，产生伪哈希。最终裁决使用 Python 直接读取 Git blob，团队的 `cd56af…` 是正确值，不把工具链伪差异记为团队错误。

本 response 的 artifact snapshot 仍只有 path，没有 commit/hash。由于文件不能可靠地内含自身 hash，正确方法应是在提交后由独立 attestation 或 manifest 固定 `(commit, path, blob hash)`；该记录放入冷审计层还是版本化证明清单，由即将统一的冷热层政策决定。仅写“提交后可复算”不等于 artifact triple 已交付。

## 2.2 五处状态字段

团队在 correction §3a 新增的五项 raw→canonical 与原 v6 逐项一致：

| finding | field | raw | canonical | 复核 |
|---|---|---|---|---|
| F-S4 | `status_before` | `PARTIAL（标签超陈述）` | `PARTIAL` | MATCH |
| F-S5 | `status_before` | `WRONG_GATE（原挂 P2/M2）` | `WRONG_GATE` | MATCH |
| F-S6 | `status_after` | `CLOSED-as-record` | `CLOSED_AS_RECORD` | MATCH |
| M-S2 | `status_before` | `PARTIAL（诚实命名已修，实质依据未交付）` | `PARTIAL` | MATCH |
| M-S4 | `status_before` | `WRONG_GATE（原 M2→M3）` | `WRONG_GATE` | MATCH |

**实质内容修复正确。** 从旧规则的字面看，程序并非严格 append-only：`git diff 14943f1^ 14943f1 -- wiki/2026-07-13-response-v6-correction.md` 显示团队直接修改既有文件，替换 §3 标题和解释文字，并新增 §3a。但 owner 已进一步说明：团队正在把过度膨胀的“所有内容一律 append-only”改造成冷热层制度，后续会统一调整。结合 Git 历史完整保留旧版、修改目的为补充披露，本轮将其定性为**政策迁移期间的文字与操作不一致**，不定性为诚信违规。

因此：

- P0‑REC‑2 的 **semantic fidelity = PASS**；
- P0‑REC‑2 的 **record-policy compatibility = TRANSITION_NOTE_REQUIRED**；
- response §6 的“全程 append-only correction, 无覆盖旧文档”与 commit 行为字面不一致，但在新冷热层政策完成统一前只需登记解释，不作为 misconduct trigger。

## 2.3 Scout ledger 的计数与覆盖能力

对 `wiki/survey/2026-07-13-scout-ledger-round1.json` 独立解析：

- 8 个 family；
- 57 个 family-entry；
- 按其公开 dedup rule 重算为 46 个 unique paper；
- 7 个跨 family 重复 key；
- 重复 key 集合与 `duplicated_across_families` 记录完全一致；
- 57/46 计数本身可复现。

但同一 ledger 也明确承认：

- 每次 WebSearch 的原始 query **没有记录**；
- 只保留每 family 的 `keywords_used`；
- 没有可重跑的 search-result universe；
- 没有科学意义上的 inclusion/exclusion criteria；
- 82 条 cite-check 只保存 `agentId/resolves/claims_match/note`，没有 stable paper ID，不能机器连接到 46 篇去重论文；
- 57 个 paper entry 没有逐篇 `evidence_grade` 字段，只有顶层默认 `SCOUT`；
- 其中两条 cite check 明确 `claims_match=false`；
- `our_datasets_match` 的语义不稳定：例如 READ 的实际数据集与字段列出的我方候选数据集混在一起，不能解释为直接 dataset overlap。

故该 ledger 能证明：

> “从留存 journal 中重建出了 57 条 family-entry，并按一条公开规则得到 46 个 unique key。”

它不能证明：

> “搜索空间充分覆盖，因此未命中的 task cell 是空白。”

更不能证明：

> “两轮 saturation 已完成。”

`P0-SURV-1=CLOSED` 因此不成立。正确状态是：

- `COUNT_AND_DEDUP_RECONSTRUCTION = CLOSED`
- `RAW_QUERY_REPRODUCIBILITY = UNAVAILABLE_FOR_ROUND1`
- `SCIENTIFIC_COVERAGE = OPEN`
- `P0-SURV-1 overall = PARTIAL`

披露缺陷值得肯定，但**披露无法把未完成的 acceptance criterion 变成 CLOSED**。

## 2.4 状态板一致性

被 response 作为“研究对象已锁定”依据的 `Research-Objective.md` 仍含：

```yaml
last_refreshed_commit: "填最新提交（本文件更新时）"
```

这是未填 placeholder。与此同时：

- `Research-Objective.md` 宣称自己是日常“现状真理”；
- 它又称 `Per-Work-Status.md` 为审计真理之一；
- `Per-Work-Status.md` 仍停留在 8 family、I1–I4 survey gate 的旧状态，没有登记“跨矩阵兑现面”锁定与 Survey v2 重构；
- `AGENTS.md/CLAUDE.md` 的 canonical-hash 条目存在，但没有写入 response 所声称的 evidence/artifact snapshot 发布不变量。

这不是学术造假，但说明热层、状态板、操作规则三者尚未收敛。本 response 把 P0‑REC‑1 宣称为普遍性 `CLOSED`，证据不足；最多只能关闭“原 precheck 的 snapshot 更正”。

---

## 3. 对团队四项 P0 自报状态的重新裁决

| P0 | 团队状态 | 本轮裁决 | 理由 |
|---|---|---|---|
| P0‑REC‑1 | CLOSED | `CLOSED_FOR_ORIGINAL_PRECHECK / PROCESS_INVARIANT_PARTIAL` | 原 precheck 三元组更正正确；本 response 自身未有 post-commit artifact attestation，规则未进入操作指南/checker |
| P0‑REC‑2 | CLOSED | `SEMANTIC_PASS / POLICY_TRANSITION_NOTE` | 五 raw 值正确；旧 append-only 文字与冷热层迁移中的实际操作尚未统一 |
| P0‑SURV‑1 | CLOSED | `PARTIAL` | 57/46 可重建；raw query、result universe、inclusion/exclusion 不可重建 |
| P0‑SURV‑2 | SCHEDULED_NEXT | `OPEN_CORRECTLY_DECLARED` | taxonomy v2 尚未提交，诚实状态正确 |
| P0‑SURV‑3 | CLOSED | `FORMAL_TOKEN_FIXED / EXPLORATION_HYPOTHESIS_OPEN` | broad claim 已标 killed；跨矩阵广度可作探索范围，但“护城河/空格”不能作为已证新颖性 |

本轮不要求所有 P0 立即完成，但不允许使用比证据更高的状态 token。

---

## 4. 对“唯一 reasoned modification”的正式回答

团队请求 reviewer 确认：研究对象是否应扩成跨冻结 omni〔模型×任务〕矩阵，并把 killer 的跨任务迁移设为一等轴。

正式答复为：

> **确认 breadth-first 的跨任务、跨模型、跨数据集探索；当前不要求收敛为单一 selector 或单一 task。相似工作越充分，越有利于建立技术路线和 SOTA。需要修正的只有证据等级：非 ASR cell 应称 `UNDERSEARCHED`，广度应称探索范围/工作假设，而非已经证明的护城河。I1–I4 仍保持候选状态，Stage‑1C 前不必收敛。**

## 4.1 为什么跨任务调查是正确的

项目研究 frozen omni，而不只是传统 ASR decoder。对 ASR、ST、SER、SLU、spoken‑QA、audio understanding 分别扫描：

- 候选如何构造；
- label-free scorer 读取什么信息；
- selector/revision/abstention 如何定义；
- headroom 是否存在；
- strong baseline 是什么；
- operator 能否跨任务迁移；

这是合理且必要的 Stage‑1A 工作。上一轮报告的 P‑F 已提出“跨任务统一 selector 是否只是工程 wrapper”的检查点，但这不等于要求项目现在收窄到 ASR，更不等于要求现在定义最终 universal selector。owner 本轮明确把广度定位为搜索底座后，这项 reasoned modification 在研究管理上成立。

## 4.2 为什么“非 ASR 格仍空”不成立

团队的推理是：上一轮 24 篇文献没有 SER/SLU/spoken‑QA fixed-K selector，所以这些格仍空。该推理同时犯了两类错误：

1. **从一份已知 ASR 偏置的种子列表推导全局不存在；**
2. **把“没有完全同构论文”偷换成“该 task cell 没有 selection/abstention/quality-estimation 祖先”。**

一轮有针对性的 primary-source 搜索已经找到以下直接反例：

| 任务/现象 | 直接文献 | 与团队主张的关系 |
|---|---|---|
| SER selective prediction | *Speech Emotion Recognition with a Reject Option*（Interspeech 2019）在 MSP-Podcast 上按 coverage 拒绝低可信样本 | 直接击穿“SER 选择/弃权格为空”；是 I3 killer，虽不是 sampled K-pool |
| SER calibration | *The Importance of Calibration*（Interspeech 2023）；*Are you sure?*（Interspeech 2024） | 说明 SER 的 confidence、reject、OOD/噪声不确定性已有成熟邻域 |
| SLU N-best | *Multi-task Learning of SLU by Integrating N-Best Hypotheses*（COLING 2020） | 直接处理 ASR N-best 对 domain/intent 的选择/集成，不是纯 ASR WER |
| SLU reject | *Practical Application of Domain Dependent Confidence Measurement for SLU*（NAACL 2018）；*Confidence Measure for Speech-to-Concept E2E SLU*（Interspeech 2020） | 直接以 semantic confidence 拒绝低可信 SLU 输出 |
| Spoken translation selection | *Integrated N-best Re-ranking for Spoken Language Translation*（Interspeech 2005） | ASR 与 MT 双层 N-best 最终重排，ST 格并不空 |
| Spoken translation QE | *Stability and Effectiveness of Features in QE for Spoken Language Translation*（Interspeech 2015） | 直接用 ASR+MT 特征进行 QE 和改进 |
| Translation MBR/QE | MBR with neural metrics、MBR-QE、metric-bias 文献 | 说明 ST 的 label-free/quality-aware selection 还必须面对 MT 祖先和 reward hacking |
| Audio captioning | SLAM-AAC 的 CLAP-Refine | 明确从多个 beam 输出中以 frozen audio-text similarity 选择 caption，是非 ASR audio-grounded selection |
| Audio understanding TTC | *Scaling Auditory Cognition via Test-Time Compute in Audio Language Models*（2025） | 在五种 Audio LLM 上使用 majority、beam-likelihood、LLM-verifier Top‑1/weighted selection；直接压力到“audio understanding 选择格为空” |
| 多类型 audio + frozen omni | MUGEN（2026） | 35 个任务横跨 speech/general-audio/music；Qwen2.5‑Omni 等模型上用 training-free self-consistency/audio-permutation aggregation |
| Audio‑LLM judge | AudioJudge（2025） | 统一评估 pronunciation、speaking rate、speaker ID、speech quality 与 human preference；说明跨 aspect audio judge 并非空白 |
| speaker/audio candidate choice | SpeakerSleuth（2026） | LALM 在多 acoustic variants 中选择最匹配说话人的音频，同时暴露 text-over-acoustic 偏差 |
| Audio QA 近邻 | AQA‑TTRL（2025） | majority pseudo-label + multiple attempts + GRPO；因更新权重不符合本项目，但直接划定 audio-QA 邻域与 frozen/non-frozen 边界 |

这些文献没有证明团队的**精确组合**已被完全占据，也不要求团队因为有相似工作就停止探索。恰恰相反，它们应成为下一轮技术选型和 SOTA 对标的入口。它们只说明：在正式文档中应把“格仍空”写成“当前 ledger 尚未充分覆盖；存在直接或部分祖先，待 Survey v2 核验”。

更严格的状态应是：

```yaml
non_asr_cell_status:
  direct_ancestors_exist: true
  exact_same_selector_supply_rho_matrix_found: false
  exact_match_search_complete: false
  novelty_status: "UNVERIFIED_AND_PRESSURED"
```

## 4.3 “广度是护城河”如何按当前阶段正确解释

数据集多、任务多、模型多在 Stage‑1A 可以承担三种正当作用：扩大搜索空间、暴露不同 failure mode、发现哪些技术路线可以迁移。owner 已明确当前只把它们作为探索基线，这一点正确。需要防止的是把探索基线提前升级成论文贡献。下面四种情况即使覆盖很广，也还不能单独证明创新：

1. 对每个任务分别使用一个已知 selector，再把结果拼成表；
2. 只共享 `argmax` 代码，但 scorer、输入、阈值、校准和候选生成都不同；
3. 只共享事后 `rho` 记账法，部署算子并不共享；
4. 因本地已经下载 28 个数据集而倒推研究问题必须覆盖 28 个数据集。

已有 28 个数据集可以降低 Stage‑1A/1B 探索成本，但不能单独证明科学空白。正确用法是让这些资产帮助筛查任务、模型和供给的提升点；错误用法才是因资产已在盘就预先宣布广度构成最终贡献。

后续收敛时，跨任务可以进一步升级为科学贡献，例如回答：

> 一个固定、label-free、预算匹配的选择规则能否跨冻结 omni 模型和不同输出几何迁移？什么可观测属性预测它会兑现 headroom，什么条件必然导致失效？

在当前阶段不要求立即证明这种规律；只要求 exploration registry 完整、失败不丢失、相似工作和强 baseline 被持续吸收。到 Stage‑1C 再判断最终贡献是系统性能、方法、迁移规律，还是其中的组合。

## 4.4 “ASR killer 不迁移”不能推出“广度对象未占据”

团队在 Decision‑Log 续34 写：

> ASR killer 不迁移 → 广度对象未被占据的证据。

这个蕴含不成立。ASR 方法不迁移，至少存在三种解释：

- 每个任务已有不同的 specialist killer；
- “同一 selector”本来就是伪统一，不应追求；
- 任务输出结构不同，K 池与 utility 不可同构。

只有在系统搜索了各任务 specialist、跨任务 unified evaluator、audio judge、selective prediction、quality estimation 和 test-time compute 后，才能判断“不迁移”是否形成独立科学问题。它不是新颖性的自动证明。

## 4.5 对“training-free RL for omni agentic system 本身已有足够创新”的校准

owner 的判断可以作为当前 Stage‑1A 的**工作假设**保留，而且这个组合确实比“再做一个 ASR reranker”更有潜力。但最新近邻说明它不是无需 survey 的安全空白：

| 近邻 | 已覆盖的关键部分 | 尚可能留下的差异 |
|---|---|---|
| AudioToolAgent（2025） | training-free audio agent；中心 agent 调用 audio-QA/STT tools、追问并比较输出作 verification；在 MMAU/MMAR/MMAU-Pro 报告 SOTA | 未必是明确 KL/advantage/reward-guided 的 inference-time RL；是否使用同一 frozen omni 作为核心需核验 |
| AuTAgent（2026） | audio tool agent + RL 学习何时调用何种工具，以 differential reward 衡量工具净收益；MMAU/MMAR 提升 | 有训练/参数学习，不是 weight-frozen training-free |
| JitRL（2026） | training-free RL for frozen LLM agents；无梯度，以非参数记忆检索轨迹、估计 advantage、调制 logits；WebArena/Jericho | 非 audio/omni；但直接占据“training-free RL for agents”的通用机制 |
| Scaling Auditory Cognition（2025） | frozen Audio-LLM inference-time majority/BoN/verifier selection | 更像 test-time compute，不一定是完整 agentic loop |
| Multi-Agent Verification / reward-guided search | 无训练的多 verifier、generate-rank-verify、reward-filtered sequential inference | 主要是文本，但占据 selector/search 机制祖先 |

一手入口：

- AudioToolAgent：<https://arxiv.org/abs/2510.02995>
- AuTAgent：<https://arxiv.org/abs/2602.13685>
- JitRL：<https://arxiv.org/abs/2601.18510>
- Multi-Agent Verification：<https://openreview.net/forum?id=mGAAoEWOq9>
- Sample, Scrutinize and Scale：<https://openreview.net/forum?id=wl3eI4wiE5>

这组证据支持一个更准确的判断：

```yaml
umbrella_novelty_status:
  working_hypothesis: "PLAUSIBLE"
  self_evident_or_already_proven: false
  closest_factorized_neighbors:
    - "training-free audio agent: AudioToolAgent"
    - "RL audio tool agent: AuTAgent"
    - "training-free RL agent: JitRL"
    - "frozen audio inference-time selection: Scaling Auditory Cognition"
  exact_intersection: "NOT_YET_CONFIRMED_OCCUPIED"
  stage1a_action: "survey the intersection and use neighbors as design/SOTA sources"
```

也就是说，**组合创新仍可能成立，但必须说明交集里的不可替代差异**。一个有说服力的最终系统至少要让 frozen omni agent 在外层闭环中根据状态和预算主动选择若干动作——例如获取供给、调用工具、采样、验证、选择、弃权或停止——并让 reward/advantage 真正改变下一步策略。若实现最终只有一次性 K-sampling + reranking，审稿人有充分理由把它归类为 test-time compute，而不是新的 agentic RL system。

### 4.5.1 “达到或超过业界最优”是强目标，但不是唯一审查项

如果系统在**不改权重、严格同预算**的约束下达到或超过有训练的业界强方法，这是很强的 systems result，甚至可能在方法新颖性有限时仍具有发表价值。但“只需要超过 SOTA”仍需拆成四条可比前沿：

1. **同一 frozen backbone 的 single-pass baseline；**
2. **同一 backbone、同信息、同预算的 training-free inference-time SOTA；**
3. **使用额外 frozen tools/verifiers 的 training-free agentic SOTA；**
4. **不受训练约束的 task-specific absolute SOTA。**

前 1–3 类决定方法是否真的优于最强可比对象，第 4 类显示与绝对上限的距离。不能用更多模型调用、闭源更强 verifier、额外检索信息或更大模型，去声称击败了成本更低的 baseline；也不能要求 frozen 系统在所有任务都必须超过 unrestricted fine-tuned SOTA 才算成功。

Stage‑1A 当前只需为每个 task/model 建立 SOTA card：训练状态、参数量、候选 K、外部工具、可用信息、推理成本、数据与 metric。真正的 SOTA 对标与超过，应在 Stage‑2/3 用冻结协议完成，不应在本阶段提前承诺结果。

## 4.6 当前能够严谨成立的项目级判断

经 owner 再次校准，本轮可以接受的最高等级判断是：

> **已有项目内局部 headroom 与业界多任务近邻结果，足以证明这条研究线存在值得继续调查的优化机会；具体哪些 cell 有 headroom、哪些 label-free 信号可兑现、怎样构成 training-free RL agentic loop，以及最终能否达到 SOTA，仍需后续设计与探索。**

必须区分五层：

| 层次 | 问题 | 当前状态 |
|---|---|---|
| 优化空间存在 | 给定供给 `c`，候选池是否有 `H(c)>0` | 在 W1 的部分 ASR 设置与业界若干任务上有支持；不能外推全矩阵 |
| 可兑现性 | label-free score 能否稳定找到好候选 | OPEN；MBR null 与各近邻结果说明强依赖 task/supply |
| 技术方案 | 如何调度供给、工具、采样、验证、选择、弃权与停止 | OPEN；正是当前 Stage‑1A 应探索的核心 |
| 创新边界 | 相比 AudioToolAgent、AuTAgent、JitRL、BoN/MBR 新在哪里 | OPEN；精确交集仍可能有空间 |
| 最终效能 | 同信息、同预算下达到或超过强基线/SOTA | Stage‑2/3 验证目标，不是当前结论 |

因此，团队现在无需收敛，但应把所有探索文档统一写成：

```yaml
program_status:
  optimization_opportunity: "SUFFICIENTLY_MOTIVATED_FOR_STAGE1A_EXPLORATION"
  matrix_wide_headroom: "NOT_ESTABLISHED"
  deployable_selector: "NOT_ESTABLISHED"
  agentic_rl_design: "OPEN"
  novelty_boundary: "OPEN"
  sota_outperformance: "FUTURE_VALIDATION_TARGET"
```

---

## 5. 多轮对抗式审查

### Round 1 — Stage gate 攻击

**问题。** response 是否把回复当成签署或 Stage‑1B 放行？

**结果。** 没有。其 `not_requested`、P2 状态和 §8 请求均明确不申请签署。

**裁决。** `PASS`。这是本轮最重要的正确点。

### Round 2 — P0 closure 攻击

**问题。** “多数已落地”是否被错误升级为“全部满足验收条件”？

**结果。** 部分是。P0‑SURV‑1 无 query log，不能整体关闭；P0‑REC‑2 的内容修复通过但需等待冷热层政策统一；P0‑SURV‑3 若解释为探索范围可接受，若解释为已证护城河则过强。

**裁决。** `TARGETED_STATUS_CORRECTION_REQUIRED`，不阻止 Stage‑1A exploration。

### Round 3 — ledger 可重现性攻击

**问题。** 第三方能否从相同 query universe 得到相同 57/46？

**结果。** 不能。第三方只能从已重建结果列表重算 46，不能重跑原始搜索。

**裁决。** `COUNT_REPRODUCIBLE / SEARCH_NOT_REPRODUCIBLE`。

### Round 4 — 空白推断攻击

**问题。** “首轮未命中”是否被写成“task cell 仍空”？

**结果。** 是；SER/SLU/ST/AAC/audio-understanding 的直接反例立即可找到。

**裁决。** `CONTRADICTED`。

### Round 5 — same-selector construct 攻击

**问题。** 团队所谓“同一算子”是否真的相同？

**结果。** 尚无操作定义。若 ASR 用 MBR/READ，SER 用 softmax confidence，SLU 用 semantic confidence，QA 用 majority vote，caption 用 CLAP，再统一套一层 `argmax`，这不是同一科学算子。

**裁决。** `OPEN_DESIGN_DIMENSION`。当前无需冻结；Stage‑1C 收敛前必须定义，否则不能把广度升级为 unified-selector contribution。

### Round 6 — reward/information-boundary 攻击

**问题。** `U`、verifiable reward 与部署 selector score 是否被混用？

**结果。** response 仍未明确三者的边界。WER/EM/SER accuracy 可在事后计算 `H/rho/regret`，但 test item gold 不能进入 selector。部署时实际使用的是 label-free proxy score `S`，不是 `U`。

**裁决。** `DESIGN_CHECKPOINT_FOR_LATER_STAGE1A`。若最终每个任务的 `S_t` 不同，共享的只是评价框架，不是 selector；当前可以并行探索多种 `S_t`。

### Round 7 — 跨任务 rho 可比性攻击

**问题。** 一个 `rho(c)` surface 是否可以跨任务直接比较或平均？

**结果。** 不可以默认这样做。不同任务的 utility、greedy anchor、effective K、oracle construction 和 headroom 大小都不同；分类任务还会产生重复标签，`K=8` 可能只有两个 unique candidates。

**裁决。** `CELLWISE_ONLY_UNTIL_JUSTIFIED`。必须先报告 per-cell 四量；禁止一个无权平均的“总 rho”。

### Round 8 — 替代解释攻击

**问题。** 即使跨任务都提升，是否证明 universal selector？

**结果。** 未必。可能只是：供给改善、task-specific score、position ensembling、或更多 compute 的共同效果。

**裁决。** 必须做 supply gain / selector gain / budget / task-specialist 分解。

### Round 9 — 记录政策迁移攻击

**问题。** §6 的 categorical statement 与正在迁移的冷热层政策是否一致？

**结果。** 按旧规则字面并不一致：`14943f1` 修改了既有 correction。但 owner 已说明 append-only 描述正在统一调整；Git diff 完整保留，修改目的也是增加披露。

**裁决。** `POLICY_TRANSITION_NOTE / FFP_NOT_ESTABLISHED`。后续统一冷热层规则即可，不把它作为本轮阻断项。

---

## 6. “同一 selector”在后续收敛前需要定义

当前 breadth-first 阶段可以同时探索多个 selector/scorer，不要求立即统一。如果后续把跨任务统一算子提升为核心候选问题，Stage‑1C 前必须回答：什么变化仍算“同一 selector”？建议采用以下严格不变量。

### 6.1 必须固定的部分

1. **选择动作。** 是从冻结 K 池选一个候选，还是允许 revision、合并、多数投票、abstain？不得混用。
2. **评分信号。** scorer 看 audio、candidate text、native logprob、其他候选、retrieval context 中哪些字段？
3. **参数状态。** 不允许按任务训练、fine-tune 或使用 test labels 校准。
4. **超参数。** 权重、阈值、温度、abstention rule 是全局固定，还是按任务设定？按任务设定就必须降级为同一框架下的 task-specific selectors。
5. **预算。** K、模型调用、tokens、audio-seconds、外部 verifier 调用须匹配。
6. **信息边界。** `U`/gold 只用于事后 evaluation；部署 score `S` 不读 gold。
7. **回退行为。** 不选择时是否回 greedy，规则是否跨任务一致？

### 6.2 三种必须拆开的“统一”

| 层次 | 可以统一什么 | 不能自动声称什么 |
|---|---|---|
| 评价统一 | 所有 cell 都报告 H、gain、regret、rho | 不能声称 selector 统一 |
| 接口统一 | 所有 scorer 输出一个 scalar，交给 argmax | 不能声称机制统一 |
| 算子统一 | 同一输入信息、同一 scoring rule、同一超参数和同一 abstention rule | 才能研究真正跨任务迁移 |

当前 response 明确做到的是第一层，可能做到第二层，尚未定义第三层。将第一层称为“同一选择算子”会构成概念夸大。

### 6.3 不同任务的 K 池并不同构

- ASR/ST/caption：开放序列，unique candidate pool 通常有意义；
- SER/intent：有限标签，采样 K 次常产生大量重复，oracle headroom 很快饱和；
- spoken‑QA MCQ：答案可能只是一项标签，容易受 option position 影响；
- open-ended spoken‑QA：semantic equivalence 与 exact-match 冲突；
- multi-audio understanding：候选可能是输入 audio options，而不是模型输出 K pool。

因此必须区分：

```yaml
pool_geometry:
  generated_open_sequence: "ASR/ST/caption/open-QA"
  sampled_finite_label: "SER/intent/MCQ"
  input_candidate_selection: "multi-audio/audio-as-option"
  revision_outside_pool: "separate operator; rho over original pool is invalid"
```

如果一个算子只在其中一种 geometry 成立，不能用其他 geometry 的 dataset 数量补足。

---

## 7. 后续收敛时可采用的可证伪 proposal 形态

如果“护城河”被用于正式 novelty claim，建议不再写：

> 广度是护城河；跨矩阵兑现面是锁定研究对象。

收敛阶段建议写成：

> Stage‑1A 正在调查一个候选问题：在冻结 omni 模型、严格 label-free 信息边界和匹配预算下，一个操作上固定的选择规则能否跨任务与跨模型迁移；候选池几何、headroom、供给类型和 verifier 独立性是否能预测其 realization 与失败。该问题的新颖性与可行性均未确认，Stage‑1C 前不锁定。

这个表述有四个优点：

1. 它允许 ASR 只是一个 cell；
2. 它不把已有数据集数量冒充 novelty；
3. 它把“跨任务”变成可证伪的 transfer hypothesis；
4. 如果 task-specific baseline 全面胜出，项目可以诚实 kill “统一 selector”而保留 per-task 结论。

### 7.1 纸面假设结构

Stage‑1A 只需纸面定义，不需现在冻结数值：

- **支持 universal-transfer 的结果形态：** 同一 selector 在多个 pool geometry、多个 frozen model 上，相对各 cell 强 baseline 有方向一致的增益，并且不依赖 task-specific tuning。
- **支持 pseudo-unification 的结果形态：** 只有换成 task-specific scorer/threshold 才提升；共享的仅是 argmax 接口或 rho 记账。
- **支持 supply-only 的结果形态：** 新供给提高 greedy/oracle，但 selector gain 不变或下降。
- **支持 no-selector-headroom 的结果形态：** 分类/MCQ cell 的 unique K 或 H 太小，无法研究 realization。
- **支持 Goodhart/abstention 的结果形态：** 随 K/compute 增长，proxy score 上升但独立 U 下降；固定风险下 abstention 改善。

### 7.2 不能回避的 specialist baseline

每个任务 cell 必须与其自己的直接祖先比较：

| task | 强 baseline / killer family |
|---|---|
| ASR | MBR/expected-WER、ROVER/confnet、QE、confidence/LTR、READ |
| ST | integrated N-best reranking、MT MBR、reference-free QE、metric-bias-aware ensemble |
| SER | native posterior/confidence、temperature scaling、reject option、UQ/OOD detection |
| SLU/intent | ASR-N-best integration、semantic confidence、response/intent rejection |
| audio caption | CLAP-Refine、CLAP/CAF reference-free scoring、revision baseline |
| spoken/audio QA | majority/self-consistency、Audio‑LLM TTC verifier、option-permutation ensemble、AQA-TTRL 作为 non-frozen boundary |
| speaker/audio quality | AudioJudge、specialist acoustic metrics、SpeakerSleuth-style discrimination |
| multi-audio understanding | MUGEN self-consistency/audio permutation、position robustness |

“同一 selector”只有同时面对这些 specialist 而仍有解释力，才可能成为科学贡献。

---

## 8. Survey v2 的建议重构

## 8.1 从 family-only 改成双轴矩阵

每篇论文同时编码：

- method family；
- task/model cell；
- pool geometry；
- operator type；
- scorer information；
- task-specific training/calibration；
- supply `c`；
- gold boundary；
- budget basis；
- direct/partial/analogy kill strength；
- full-text evidence grade。

不能再用“这一 family 未命中 SER”推断“SER cell 为空”。

## 8.2 必须新增的 seed 文献链

### SER

1. *Speech Emotion Recognition with a Reject Option*  
   <https://www.isca-archive.org/interspeech_2019/sridhar19_interspeech.html>
2. *The Importance of Calibration: Rethinking Confidence and Performance of Speech Multi-label Emotion Classifiers*  
   <https://www.isca-archive.org/interspeech_2023/chou23_interspeech.html>
3. *Are you sure? Analysing Uncertainty Quantification Approaches for Real-world Speech Emotion Recognition*  
   <https://www.isca-archive.org/interspeech_2024/schrufer24_interspeech.html>

### SLU / intent / dialogue rejection

4. *Multi-task Learning of Spoken Language Understanding by Integrating N-Best Hypotheses with Hierarchical Attention*  
   <https://aclanthology.org/2020.coling-industry.11/>
5. *Practical Application of Domain Dependent Confidence Measurement for Spoken Language Understanding Systems*  
   <https://aclanthology.org/N18-3016/>
6. *Confidence Measure for Speech-to-Concept End-to-End Spoken Language Understanding*  
   <https://www.isca-archive.org/interspeech_2020/caubriere20_interspeech.html>
7. *Response-Based Confidence Annotation for Spoken Dialogue Systems*  
   <https://aclanthology.org/W08-0102/>

### Spoken translation / MT selection

8. *Integrated N-best Re-ranking for Spoken Language Translation*  
   <https://www.isca-archive.org/interspeech_2005/quan05_interspeech.html>
9. *A Study on the Stability and Effectiveness of Features in Quality Estimation for Spoken Language Translation*  
   <https://www.isca-archive.org/interspeech_2015/ng15_interspeech.html>
10. *High Quality Rather than High Model Probability: MBR Decoding with Neural Metrics*  
    <https://aclanthology.org/2022.tacl-1.47/>
11. *Quality Estimation Using Minimum Bayes Risk*  
    <https://aclanthology.org/2023.wmt-1.67/>
12. *Mitigating Metric Bias in Minimum Bayes Risk Decoding*  
    <https://aclanthology.org/2024.wmt-1.109/>

### Audio captioning / audio judge

13. SLAM-AAC / CLAP-Refine  
    <https://arxiv.org/abs/2410.09503>
14. AudioJudge  
    <https://arxiv.org/abs/2507.12705>
15. CAF-Score  
    <https://arxiv.org/abs/2603.19615>
16. SpeakerSleuth  
    <https://arxiv.org/abs/2601.04029>

### Audio understanding / test-time selection

17. *Scaling Auditory Cognition via Test-Time Compute in Audio Language Models*  
    <https://arxiv.org/abs/2503.23395>
18. AQA-TTRL  
    <https://arxiv.org/abs/2510.05478>
19. MUGEN  
    <https://arxiv.org/abs/2603.09714>
20. *Uncertainty Calibration for Deep Audio Classifiers*  
    <https://arxiv.org/abs/2206.13071>

这些是 seed，不是穷尽列表。至少第 1、4、8、13、14、17、19 篇已经足以否定“非 ASR task cells 仍空”的宽断言。

## 8.3 Round‑1 ledger 的诚实标签

建议把现有 57/46 ledger 作为可追溯的 Round‑1 版本保留，再按冷热层政策选择新增说明、版本化 supersession 或冷层 attestation；不得让后续整理抹去当时没有 raw query log 这一事实：

```yaml
round1_ledger_grade:
  count_reconstruction: "VERIFIED"
  dedup_reconstruction: "VERIFIED"
  raw_query_replay: "IMPOSSIBLE_NOT_CAPTURED"
  inclusion_exclusion_replay: "IMPOSSIBLE_NOT_CAPTURED"
  coverage_or_saturation_claim: "NOT_ALLOWED"
  all_entries_evidence_grade: "SCOUT_UNLESS_STABLE_ID_LINKED_FULLTEXT_RECORD_EXISTS"
```

Survey v2 从第一条 query 起保存原始 query log；不能回填一个仿真的旧 query log 冒充当时记录。

## 8.4 Saturation rule 必须按 cell 而非仅按 family

一个 family 在 ASR 上 saturated，不代表在 SER/SLU 上 saturated；反之亦然。建议：

- 每个关键 `method family × task class` cell 至少一条 seed、backward citation chase、forward citation chase；
- 连续两批 logged query 不产生新 direct mechanism 或 killer，才标 `LOCALLY_SATURATED`；
- 未覆盖 cell 标 `UNDERSEARCHED`，不是 `EMPTY`；
- 只有在明确 scope 内，才可写 `no direct match found within logged scope`。

---

## 9. 跨任务 rho/H/regret 的统计与归因风险

## 9.1 per-cell 四量必须保留

每个 `(model, task, supply c, pool construction, K)` cell 分别报告：

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

以及 glossary 要求的 `rho_pool`、`delta_mbr`。分母过小标 `HEADROOM_TOO_SMALL`。

## 9.2 禁止默认跨任务平均 rho

原因：

- 小 headroom cell 的 rho 方差极大；
- 不同 U 的统计性质不同；
- 分类任务有限标签使 oracle 快速饱和；
- duplicate candidates 使 nominal K 不等于 effective K；
- 不同任务 greedy baseline 强度不同；
- 选择性丢弃 `HEADROOM_TOO_SMALL` cell 会产生 selection bias。

Stage‑1A 必须预先写明：跨任务结论以 **cellwise pattern、failure taxonomy 和 transfer consistency** 为主，不用一个总 rho 排名项目。

## 9.3 供给收益仍须与 selector 收益分开

\[
U_{sel}(c)-U_{greedy}(c_0)
=
[U_{greedy}(c)-U_{greedy}(c_0)]
+
[U_{sel}(c)-U_{greedy}(c)]
\]

跨任务矩阵越大，越容易把第一项的供给收益错记成第二项的 selector 能力。每个 cell 都必须单独分解。

## 9.4 scorer–evaluator lineage

ST 的 MBR metric bias、AudioJudge 的 position/verbosity bias、SpeakerSleuth 的 text-over-acoustic bias都说明：

- 选择 score `S` 与事后 utility `U` 不能同源；
- 同一模型生成又自评需要单列 self-preference 风险；
- task-specific human or independent metric audit 仍然需要；
- “一个 omni judge 跨任务统一”本身可能只是统一偏差。

---

## 10. 学术诚信复判

## 10.1 有利证据

- 团队没有申请签署或 Stage‑1B；
- 57→46 重算逻辑可复现；
- off-by-one 在提交前被内部检查发现；
- 五处 raw 值已完整公开；
- query-log 缺失被 ledger 主动披露，没有伪造ย้อนหลัง query；
- Git 历史保留了旧 correction，没有发现删除实验或篡改数字；
- `+0.517` 仍保持 invalid，没有在本 response 中复活。

这些证据继续反对“蓄意学术欺诈”的判断。

## 10.2 不利证据

1. 对没有 query log 的 P0‑SURV‑1 使用 `CLOSED`；
2. 旧 append-only 表述与实际冷热层迁移尚未统一；
3. “广度是护城河”没有明确标成探索期工作假设；
4. 已知 round‑1 ASR 偏置，仍把未命中写成“SER/SLU/spoken‑QA 格仍空”；
5. selfcheck 再次以 `0` 收尾，但没有覆盖 raw query 和 novelty inference。

这些属于**探索期证据措辞与记录政策仍未收敛**，尚不足以证明故意欺骗。owner 的两次即时澄清——广度只是当前搜索底座、技术方案仍开放——进一步降低了把这些文字解释为刻意夸大的理由。

## 10.3 当前分级

```yaml
integrity_assessment:
  fabrication: "NOT_ESTABLISHED"
  falsification: "NOT_ESTABLISHED"
  plagiarism: "NOT_ESTABLISHED"
  intent_to_deceive: "NO_SUFFICIENT_EVIDENCE"
  record_policy_transition_inconsistency: true
  policy_clarification_received: true
  qrp_record_control_risk: "MODERATE"
  trend: "STABLE_IF_SCOPE_AND_EVIDENCE_GRADES_ARE_KEPT_EXPLICIT"
  formal_misconduct_inquiry_now: false
```

只有在统一政策后仍继续把不可重放 search 写成 saturated/empty、隐藏失败尝试或复用泄漏数字，风险才应升级。当前不建议启动 misconduct inquiry。

---

## 11. 分阶段改进计划

## 11.1 记录类：随冷热层政策统一完成，不阻断当前 survey

### A. 发布一次冷热层与历史记录政策说明

统一说明：

- 哪些文件属于冷审计层、原则上只追加；
- 哪些文件属于热现状层、允许覆盖刷新；
- `14943f1` 属于政策迁移前后的哪种操作；
- 修改前后 Git 历史如何提供审计追踪；
- 以后如何避免上下文噪声再次无限膨胀。

不要求当前暂停 survey 等待该说明。

### B. 为本 response 增加 post-commit artifact attestation

记录：

```yaml
artifact_snapshot:
  path: "wiki/2026-07-14-response-to-precheck-doctoral-review.md"
  umbrella_commit: "0be1285e9242d195039b5fd3bc5425b1d741499c"
  sha256_git_blob: "7033539fed07906e534ad22844d4d9b864b560e3c884bbf75c3ed5157760136e"
```

### C. 校准 P0 状态

- P0‑SURV‑1 改 `PARTIAL`；
- P0‑REC‑2 标 semantic pass / policy transition；
- P0‑SURV‑3 标 formal wording fixed / exploration hypothesis open；
- 不再用 selfcheck=0 表示外部审查空间归零。

### D. 收敛现状入口

- 解决 `Research-Objective.md` 的 `last_refreshed_commit` placeholder；
- 更新 `Per-Work-Status.md` 的当前 survey v2 状态；
- 在操作指南或 checker 中真正加入 evidence/artifact snapshot invariant；
- 明确 Research‑Objective 与 Per‑Work‑Status 发生冲突时谁优先，以及如何自动检测。

## 11.2 科学问题类：当前广泛探索，Stage‑1C 前逐步完成

### E. 把“护城河”明确标成工作假设

必须使用：

- `survey_scope = cross_task_cross_model`
- `scientific_question_status = candidate_not_selected`
- `novelty = unverified`
- `breadth = external_validity_dimension_not_contribution_by_itself`

### F. 定义 same-selector contract

交付一页 contract，逐项冻结：operator、score inputs、task-specific parameters、budget、abstention、gold boundary、pool geometry。无法跨任务固定的部分必须公开标 task-specific。

### G. 完成 direct non-ASR killer survey

至少覆盖本报告 §8.2 的 20 篇 seed，并对 SER、SLU、ST、AAC、audio‑QA、multi-audio/audio judge 分别做 backward/forward chase。

### H. 提交 task × method × model 三维 kill matrix

每格只允许：

- `DIRECT_OCCUPIED`
- `PARTIAL_ANCESTOR`
- `ANALOGY_ONLY`
- `UNDERSEARCHED`
- `NO_DIRECT_MATCH_WITHIN_LOGGED_SCOPE`

禁止使用没有 query scope 的 `EMPTY`。

### I. 让跨任务成为可证伪问题

Stage‑1C dossier 必须同时允许三个结论：

1. universal selector 值得 proceed；
2. 只能形成 task-specific selector family，应 pivot；
3. 只有 accounting framework，没有方法/现象新意，应 kill。

如果 dossier 只允许第一种结论，它不是问题定义，而是事后找证据支持已锁定答案。

## 11.3 Stage‑1B 仍禁止提前做的事

- 不因 survey 发现非 ASR 论文就开始补跑矩阵；
- 不使用已有 28 数据集数量作为放行理由；
- 不用 exploratory cell 挑选“最漂亮任务”；
- 不对跨任务 rho 做论文级总平均；
- 不用 test gold 调 scorer 或阈值；
- 未经 owner 在 Stage‑1C 明确选择，不进入方向性原型。

---

## 12. 对团队 response 各节的逐项判定

| response section | 判定 | 说明 |
|---|---|---|
| §0 总立场 | PASS_WITH_CLARIFICATION | 不申请签署正确；owner 已澄清当前是 breadth-first exploration |
| §1 P0 | TARGETED_CORRECTION | 计数/五 raw 正确；P0‑SURV‑1 应拆 count closed / search open |
| §2 跨任务反制 | ACCEPT_WITH_EVIDENCE_GRADING | 跨任务扫正确；空格改 UNDERSEARCHED，护城河改工作假设 |
| §3 Q1–Q6 | PASS_DIRECTIONALLY | 行动方向好；Survey v2 补 non-ASR direct ancestors，same-selector contract 可延后到收敛阶段 |
| §4 门槛状态 | PARTIAL | P0‑SURV‑2/P1/P2 诚实；P0‑SURV‑1/3 需重开 |
| §5 候选身份 | EXPLORATION_CONTINUES | broad/narrow 拆分正确；非 ASR cell 标 undersearched，I1–I4 暂不收敛 |
| §6 诚信 | PASS_WITH_POLICY_NOTE | FFP/QRP 判断可接受；append-only 进入冷热层统一，不作为不端证据 |
| §7 provenance | PARTIAL_PASS | responds-to/evidence snapshot 正确；artifact post-commit attestation 缺失 |
| §8 请求 | CONFIRMED_WITH_CALIBRATION | 确认广度探索；优化机会足以继续，技术方案/新颖性/SOTA 均开放 |

---

## 13. 给团队 AI 的机器可执行裁决

```yaml
review_decision:
  overall: "ACCEPT_DIRECTION_WITH_TARGETED_RECORD_AND_SURVEY_CORRECTIONS"
  stage: "STAGE_1A"
  may_continue_survey_v2: true
  may_claim_p0_record_closure: false
  may_claim_non_asr_cells_empty: false
  may_claim_breadth_is_novelty_moat: false
  may_use_breadth_as_exploration_baseline: true
  convergence_required_now: false
  may_start_stage1b: false

reasoned_modification:
  breadth_first_cross_task_model_dataset_exploration: "ACCEPT"
  task_model_cell_annotation: "ACCEPT"
  similar_industry_work_as_design_and_sota_source: "ACCEPT"
  killer_transfer_as_later_research_question: "ACCEPT_OPTIONAL"
  non_asr_cells_empty: "REPLACE_WITH_UNDERSEARCHED"
  breadth_as_working_hypothesis: "ACCEPT"
  breadth_as_proven_novelty: "NOT_YET"
  exact_training_free_rl_frozen_omni_agentic_system: "PLAUSIBLE_WORKING_HYPOTHESIS_UNDER_NEIGHBOR_PRESSURE"

p0_reassessment:
  P0_REC_1: "ORIGINAL_PRECHECK_FIXED_PROCESS_INVARIANT_PARTIAL"
  P0_REC_2: "SEMANTIC_PASS_POLICY_TRANSITION_NOTE"
  P0_SURV_1: "PARTIAL_COUNT_VERIFIED_SEARCH_NOT_REPLAYABLE"
  P0_SURV_2: "OPEN_CORRECTLY_DECLARED"
  P0_SURV_3: "WORDING_FIXED_EXPLORATION_HYPOTHESIS_OPEN"

mandatory_next_actions:
  - "unify hot/cold record policy without blocking ongoing Stage-1A survey"
  - "post-commit artifact attestation for response 0be1285 / blob 7033539"
  - "downgrade P0-SURV-1 and separate count reconstruction from search reproducibility"
  - "mark moat as working hypothesis and empty cells as undersearched"
  - "explore multiple technical designs now; define same-selector contract only before convergence"
  - "distinguish evaluation U from deployable score S before claiming a concrete selector"
  - "survey direct SER/SLU/ST/AAC/audio-QA/multi-audio/audio-judge ancestors"
  - "survey AudioToolAgent, AuTAgent and JitRL as nearest neighbors of the umbrella identity"
  - "build per-task SOTA cards with training, information and compute constraints"
  - "build task-by-method-by-model kill matrix with UNDERSEARCHED rather than EMPTY"
  - "update Research-Objective and Per-Work-Status consistently without rewriting audit history"

integrity:
  ffp_established: false
  record_policy_transition_clarified: true
  qrp_control_risk: "MODERATE"
  misconduct_inquiry_now: false
  escalation_if: "hidden/deleted failures, reused leakage, or unsupported saturation claims appear after policy unification"
```

---

## 14. 最终导师意见

经 owner 两次澄清后，本轮最合理的导师判断是：**广度优先的探索路线正确，优化机会已经足以支撑继续做 Stage‑1A，技术方案仍需认真设计。** 现在不应强迫团队缩成 ASR，也不应强迫它提前冻结 universal selector。应充分利用已有模型与数据集，寻找局部 headroom、可兑现信号、agentic action space、相似工业系统和最强可比 SOTA。

需要保持的学术纪律只有两条：第一，探索范围广不等于整个矩阵已证有 headroom；第二，`training-free RL + frozen omni + agentic system` 是可保留的创新假设，不是无需对照的既成事实。AudioToolAgent、AuTAgent、JitRL 等近邻越多越好——它们既会压缩宽泛 claim，也会提供技术模块、SOTA 和可比较的系统边界。

正确的下一步是继续 breadth-first survey：补齐 SER/SLU/ST/AAC/audio-understanding 祖先与 audio-agent 近邻；给每个任务建立约束一致的 SOTA card；在纸面上探索供给、工具、采样、验证、选择、弃权、停止等不同闭环组合；记录哪些 cell 有 headroom、哪些方法不适用。等候选技术路径形成后，再在 Stage‑1C 收敛，而不是现在收敛。

本轮签署状态：

> **Stage‑1A breadth-first 探索确认；当前优化机会足以继续；技术方案、新颖性边界与 SOTA 达成均开放；P0‑SURV‑1 只部分关闭；非 ASR cell 改标 UNDERSEARCHED；append-only 交由冷热层政策统一；Stage‑1B 不放行；未认定学术欺诈。**
