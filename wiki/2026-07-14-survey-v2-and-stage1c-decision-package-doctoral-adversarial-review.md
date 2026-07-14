---
title: "Survey v2 与 Stage-1C Decision Package 博导级对抗复审"
date: 2026-07-14
stage: "Stage-1A — problem definition"
review_type: "independent doctoral adversarial review"
reviewed_commit: "233dc7eb9224b5d7bc8df7bfd81a616ab15c6917"
verdict: "MAJOR_REVISION"
survey_status: "ROUND1_SCOUT_MAP_ACCEPTABLE; SURVEY_COMPLETE_NOT_ACCEPTED"
decision_package_status: "DOWNGRADE_TO_PRE_STAGE1C_DECISION_DRAFT"
stage1b_authorized: false
research_misconduct_finding: "FFP_NOT_ESTABLISHED; QRP/PROCESS-CONTROL_RISK_HIGH"
source_file_policy: "No research-team source artifact was modified; this is a new dated review."
---

# Survey v2 与 Stage-1C Decision Package 博导级对抗复审

## 1. 一句话裁决

团队完成了一轮有价值的**广度型 scout survey**，证明他们已经看到多数危险近邻，也正确杀掉了裸 I1；
但“Survey v2 complete / 调研收官 / owner-decision-ready”不成立。现有证据链不可完整回放，论文去重数
不是精确可重建值，证据等级存在系统性上标，若干关键方法和数字被混写，严格 I2 与团队自己的邻居矩阵
互相矛盾，I4 的“最清晰空白”又遗漏了更广泛 test-time scaling 文献对同一方法学对象的占据。

本轮正式状态：

```text
REVIEW_VERDICT                         = MAJOR_REVISION
SURVEY_V2_ROUND1_SCOUT_MAP             = ACCEPTABLE_WITH_CORRECTIONS
SURVEY_COMPLETE / 调研收官             = NOT_ACCEPTED
STAGE1C_DECISION_PACKAGE               = PRE_STAGE1C_DECISION_DRAFT
STAGE1A                                = CONTINUE
STAGE1B                                = NOT_AUTHORIZED
FABRICATION/FALSIFICATION/PLAGIARISM   = NOT_ESTABLISHED
QUESTIONABLE_RESEARCH_PRACTICE_RISK    = HIGH UNTIL REPLAY + CLAIM AUDIT CLOSE
```

这不是按论文发表阶段要求“把一切做完”。它按 Stage-1A 的正确标准只问三件事：研究问题是否被稳定定义，
危险近邻是否足以改变选题，团队是否有资格把 scout 结果升级成“完成/空白/决策就绪”。当前前两项取得进展，
第三项失败。

## 2. 固定审查快照

本报告只审查 commit `233dc7eb9224b5d7bc8df7bfd81a616ab15c6917` 的 git blob 字节；后续团队
并行修改不属于本裁决。canonical SHA-256：

| 工件 | git-blob 字节 SHA-256 |
|---|---|
| `wiki/survey/2026-07-14-coverage-and-kill-matrix-v2.md` | `921cf68f08169d1f7f5e1d0eb18adec12e8d86357ac3b99cea6adc1e79f30e43` |
| `wiki/survey/2026-07-14-neighbor-matrix-v2.md` | `e28556421e5b23a23a43165a418698907a68f73272bdabef6a2a34bb8277b493` |
| `wiki/survey/2026-07-14-scout-ledger-round2.json` | `2632ebaf335a44cf4044e781335eaf705cee1871cce7643c5e42dbc6e03bc1eb` |
| `wiki/survey/2026-07-14-search-query-log.jsonl` | `6e22c703d5fb50e2d399e5b7493357d813a2389c1992eaa17e5c8c290a6af8f8` |
| `wiki/survey/2026-07-14-sota-cards-v2.md` | `fc101f1bb38017aa2f0506e179e96e300efd48fba5f01d9342cfe8289631c541` |
| `wiki/2026-07-14-stage1c-decision-package.md` | `2c08e1774443d03af0b5f8830d3c3c7c1b818f9a6fe6da6e6e95ef777d6a23c7` |

本报告将“团队明说的事实”“我从工件重算的事实”“基于论文的一手核验”“审稿判断”分开；不会把推断
伪装成已证实事实。

## 3. 值得保留的进步

严厉审查不等于抹掉有效劳动。以下进步真实存在：

1. 15 个 lane 已覆盖 ASR、ST、SER、SLU、AAC、audio understanding、selective prediction、
   candidate support、agentic/test-time RL 等，不再只盯 speech 小圈子。
2. 团队明确承认 bare I1 已被 MBR 等方法直接占据；这是对先前宽泛 novelty 的必要纠偏。
3. 邻居矩阵能区分 frozen、trained、audio-at-decision、abstention、任务/数据集重叠；方向正确。
4. 团队没有把两个无法解析的 citation 悄悄删掉，也没有声称 Stage-1B 已获授权。
5. `Scaling Auditory Cognition`、MBR、READ、Jia et al.、KIT、AudioToolAgent 等近邻抓得较准，说明
   survey 的搜索直觉已有明显提高。
6. Stage-1C package 没替 owner 自动选题；治理边界比此前更清楚。

这些优点支持“round-1 scout map 可继续使用”，但不支持“Survey 已完成”。

## 4. 多轮对抗式评审

### Round 1 — 阶段与生命周期一致性攻击

**团队主张：** commit message、热层文档和 decision package 将 Survey v2 描述为 complete、调研收官、
owner-decision-ready。

**反证：** 同一快照的 `scout-ledger-round2.json` 首尾仍写：

- `DRAFT — pending coordinator per-paper verification, not yet wiki-grade`；
- 该工件只是 `SCOUT-grade round-1`；
- 有 9 项 `round2_saturation_targets`；
- 只有 5 个 load-bearing papers 由 coordinator 检查；
- 2 个 citation unresolved。

**裁决：BLOCKING。** “一轮 scout 批次完成”与“Survey 证据工作完成”是两个不同命题。团队可以写
`ROUND1_SCOUT_COMPLETE`，不能写 `SURVEY_COMPLETE/调研收官`。Stage-1C package 降级为
`PRE_STAGE1C_DECISION_DRAFT`。

### Round 2 — 检索是否可回放攻击

我从 query log 重算得到：

| 项目 | 工件可重算值 | 问题 |
|---|---:|---|
| 总行数 | 305 | 不是 305 次纯搜索 |
| `WebSearch` | 218 | 搜索事件 |
| `WebFetch` | 87 | 页面抓取事件，不应计入 query count |
| query 字段本身为 URL | 53 | 再次说明日志混合 discovery 与 fetch |
| lane | 15 | 有广度，但不代表饱和 |
| 时间 | 全部只有 `2026-07-14` | 无时分秒，无法排序并发事件 |
| 字段 | `lane,engine,query,date,result_cap,note` | 无 run/agent/event ID、raw result、returned count、rank、screening decision、hash |

`result_cap` 还混用 `10`、`~9 links`、`full text`、`1 doc` 等字符串；它表示请求上限或备注，不是实际
返回条目数。305 个 query 字符串虽然 exact-unique，却无法回答“每个查询返回什么、哪些被排除、为何排除、
重复如何合并”。

**裁决：BLOCKING。** 这是 query narrative log，不是 replay log。它改善了新一轮查询文本留痕，但无法
回放结果宇宙，更不能补救过去缺失的原始检索轨迹。团队不得事后依据最终清单“补造”返回结果；缺失部分
必须诚实标 `RAW_EVENT_UNAVAILABLE`。

最低工作规范采用本报告配套的
[`Survey Response 可回放审计模板`](./2026-07-14-survey-response-replayability-template.md)。

### Round 3 — “约 93 篇”与去重攻击

ledger 自报 113 个跨 lane paper rows、`unique_papers_after_cross_lane_dedup_est = 93`。但从 JSON 的
paper `id` 直接重算得到 107 个 exact-unique 字符串，而不是 93。原因不是团队一定算错，而是同一工作有
多套别名，例如 `scaling-auditory-cognition-2025`、`AuditoryTTC-2503.23395`、
`dang2025...`、`ttc-audio...`；MBR 也有多种写法。ledger 行没有规范 DOI/arXiv/version/URL，无法按它
声称的 dedup rule 独立重建 93。

paper row 的可重算分布为：

```text
rows      = 113
id strings= 107
grade     = AB 54 / FT 39 / SC 18 / UNVERIFIED-CITATION 2
strength  = DIRECT 17 / PARTIAL 62 / ANALOGY 33 / NONE 1
```

**裁决：MAJOR。** `~93` 只能叫人工估计，不能做精确分母、覆盖率或饱和证据。必须建立 canonical
`paper_id`、version-level identity、alias merge 表和机器生成 dedup report。

### Round 4 — 证据等级与核验语义攻击

三个 survey markdown 的全局说明承认 WebFetch 受阻，许多 `[FT]` 其实来自 WebSearch cite check；ledger
又把 39 行机器标为 `FT=FULLTEXT_VERIFIED`，并说 92/94 `resolves:true, claims_match:true`。这三个事实
不能同时成立：

- 页面能解析，不等于摘要支持方法主张；
- 摘要支持，不等于打开固定版本全文；
- 打开全文，不等于数值/方法边界有表号或段落定位；
- 主张核验，更不等于复现实验。

其中 `enclap` 甚至在抓取失败后依据 prior knowledge 记为 resolves:true。全局 header 写“降级理解”不能
覆盖每行机器标签；下游 AI 会直接把 `FT` 当作已核验事实。

**裁决：BLOCKING。** 全部 paper/claim 按 `DISCOVERED → ABSTRACT_VERIFIED → FULLTEXT_OPENED →
CLAIM_VERIFIED → REPRODUCED` 重标。只有带固定版本和 locator 的 claim 才能进入 kill/coverage 决策。

### Round 5 — 数字与算子事实攻击

#### 5.1 READ 的 realized-oracle 数字明显上夸

neighbor matrix 写 READ “~70–85% oracle”。按论文 Table 1 的 greedy、READ、oracle WER 重算，八个条件
约为 7.7%、11.9%、16.5%、17.3%、43.8%、约 56%、67.7%、68.4%；最大值也未达到 70%，更不存在
85%。论文是 [READ: Reversible Textual Rescoring for ASR](https://arxiv.org/html/2606.04680)。

这不是小数四舍五入，而是可能改变“现有方法已兑现多少 headroom”的 load-bearing exaggeration。更严重的
是，上一轮 ledger 曾正确指出 clean LibriSpeech 不到 20%、shifted set 才接近一半以上；v2 反而退化成
更夸张的摘要。

#### 5.2 MBR 与 Llama-3 scorer 被合并

SOTA card 把 `Whisper-lv3 + Llama-3 scorer` 与 MBR 3.3/oracle 1.3、O(N²) 放在同一行。原论文中 MBR
用 hypothesis-to-hypothesis BLEU utility；Llama-3 属于 ProGRes comparator，不是 MBR scorer。
见 [Re-evaluating MBR Decoding for ASR](https://arxiv.org/html/2510.19471)。

#### 5.3 TAP-GER 的 frozen/selection/oracle 边界被写错

TAP-GER 摘要说 frozen in-context prompting 有竞争力，而低于 N-best oracle WER 的结果来自 prompting
加 fine-tuning；其 generative error correction 还能产生池外输出。它不能作为“frozen in-pool selector
击败 oracle”的证据。见 [TAP-GER](https://arxiv.org/abs/2309.15649)。

#### 5.4 ProGRes 不是纯 in-pool selection

ProGRes 会生成新假设扩展 N-best，再评分。将它与只在固定 K 池内选一个候选的 selector 混为一谈，会让
oracle、headroom、信息边界和计算预算全部失真。见 [ProGRes](https://arxiv.org/abs/2409.00217)。

**裁决：MAJOR。** 当前不是发现了蓄意造假，而是 claim extraction 与 operator taxonomy 的质量控制
失效。所有数值和方法边界必须 claim-level 双审；selection、revision、candidate expansion、tool loop、
weight update 分列。

### Round 6 — I2 自相矛盾与“合取洗白”攻击

团队自己的 neighbor matrix 对 `Scaling Auditory Cognition` 写得基本正确：冻结 audio LLM 以自身
audio-conditioned beam likelihood 对 K 候选评分，这是 genuine omni-native signal，直接占据 bare I2
机制。原论文也明确给出 beam-search weighting 和 audio-grounded verifier；见
[Scaling Test-Time Compute for Auditory Cognition](https://ar5iv.labs.arxiv.org/html/2503.23395v1)。

但 Stage-1C package 又声称 strict I2（same frozen core as generator and scorer）没有 logged match，理由是
现有工作依赖 external TTS/GPT-4o/trained reward。这个论证把论文的 strongest external verifier 与论文也
存在的 same-core native likelihood 混在一起。裸 I2 已被占据；“same-core + supply-conditional rho surface”
可能未被单篇论文完整覆盖，但那已是 I2∩I4 的新合取身份，不是 strict I2 本身。

**裁决：FUNDAMENTAL。** 这构成高风险的 moving-goalpost/conjunctional novelty laundering：看到近邻后
不断追加 `same-core + surface + Goodhart + cross-task + loop`，再以“无单篇论文同时满足”保住 novelty。
目前没有证据证明这是故意欺骗，但如果不冻结 identity 而继续对外写 bare I2 open，就会进入误导性表述。

必须做：

1. 写 `BARE_I2 = DIRECT_OCCUPIED`；
2. 单独定义 `I2xI4`，说明每个必要条件的科学作用；
3. 任何搜索后新增的限定词标为 post hoc；
4. novelty 评价分别回答 method novelty、measurement novelty、domain instantiation、system integration，
   禁止只做 exact-intersection 搜索。

### Round 7 — I4 “最清晰空白”与跨领域 survey 漏项攻击

I4 把供给 `c`、候选覆盖、oracle headroom、selector realization rate、模型/任务/预算放进一张曲面。其
speech/omni 实例化可能仍有空间，但这个**方法学对象**并不空。至少以下一手工作应进入 closest-neighbor
与 kill 分析：

- [Compute-Optimal Test-Time Scaling](https://arxiv.org/abs/2408.03314)：难度条件化的 test-time compute
  分配与 verifier 效用；
- [Variable Granularity Search](https://arxiv.org/abs/2505.11730)：跨 compute budgets、
  generator-verifier 配置和 task attributes 的搜索；
- [A Diagnostic Scaling Law for Test-Time Personalization](https://arxiv.org/abs/2605.10991)：把 BoN 曲线
  分解为可测量量，跨 policy/task 解释与预测；
- [The Art of Scaling Test-Time Compute](https://arxiv.org/abs/2512.02008)：8 模型×4 数据集下没有统一最优
  策略，最优项取决于 model/task/budget；
- [RoboMonkey](https://proceedings.mlr.press/v305/kwok25a.html)：VLA/robotics 中的 sampling、verification
  与 inference scaling law。

这些论文不等于“已经完成 frozen omni speech I4”，但它们直接削弱“曲面本身是新方法对象”的说法。
此外，团队已列出的 [KIT IWSLT 2026](https://arxiv.org/abs/2606.04730)、MBR、JudgeBoN、reward
overoptimization 等已经是 speech/text 局部祖先。

**裁决：FUNDAMENTAL。** 当前最多能说：

> 在已记录的 round-1 scout 范围内，尚未发现把该诊断框架完整应用于 frozen omni speech 多任务的单篇
> 工作；domain instantiation 可能开放，但 scaling-surface methodology 已被广泛占据。

如果 I4 只画一张描述性矩阵，它更像 benchmark/evaluation protocol，不足以单独成为核心科学问题。
要升级为研究贡献，至少需要产生可证伪的新规律：例如用小预算测得的 coverage、reward noise、error
correlation 预测 held-out `(model, task, c)` 的 rho；或给出何时增加 K/检索/工具必然无效的决策规则。

### Round 8 — “SOTA cards”可比性攻击

当前 cards 更接近 comparator seed list，不是经过核实的 SOTA cards：

- 不同行混合不同 backbone、dataset split、metric、candidate pool 和训练制度；
- 参数字段有时填模型名而不是参数量；
- 成本只写 `K decodes`/`multi-step`，没有 token/audio duration、latency、GPU/美元预算；
- F3/F4 多为搜索目标或代表性近邻，不是当前最优结果；
- 主模型 Qwen3-Omni 在多个任务卡中没有同协议基线；
- `[ours-directional]` 数字缺少稳定 lineage；
- MBR/ProGRes/TAP-GER 的算子边界已经出现事实合并。

**裁决：MAJOR。** 文件应先改称 `Comparator Seed Cards v0`。只有同任务、同 split、同信息边界、同
weight-update 条件、同预算的卡才能支持“match/beat SOTA”。Stage-1A 可以先做 apples-to-apples 设计，
不要求现在跑大实验；但不能先把不可比数字包装成未来验收线。

### Round 9 — 术语控制与自动检查攻击

SOTA card 的综合结论又出现 `EMPTY/UNDERSEARCHED`，与其 header 声称“no EMPTY ever”直接矛盾；大量
matrix cell 仍写裸 `NO_DIRECT_MATCH`，没有 `WITHIN_LOGGED_SCOPE` 限定。自检却报告 0 violation。

**裁决：MAJOR。** 这说明当前 selfcheck 是装饰性检查而非 fail-fast gate。禁词扫描、状态机、外键、
证据等级与 claim locator 必须自动验证；失败时最终状态自动降级，不能在正文解释后继续写 complete。

### Round 10 — 学术诚信与不当研究实践攻击

我分别检查了四类可能性：

| 风险 | 当前证据 | 裁决 |
|---|---|---|
| Fabrication（捏造论文/数据） | 两个 citation 主动标 unresolved；关键论文多数确实存在；未发现虚构实验结果 | 未建立 |
| Falsification（篡改/有意歪曲） | READ 数字上夸、算子混写严重，但尚无意图证据；更像二手摘录和 QA 失败 | 未建立，需更正 |
| Plagiarism | 本轮未见把他人文本/方法冒充自有的直接证据 | 未建立 |
| QRP/误导性流程 | 状态上标、不可回放计数、证据等级膨胀、post-hoc 合取保 novelty、自动检查漏报 | 高风险，已建立为流程问题 |

因此不能写“团队涉嫌学术欺诈已坐实”，也不能写“没有问题”。准确结论是：**FFP 尚无充分证据，
但可疑研究实践与研究记录控制风险很高；在回放和 claim audit 完成前，任何强 novelty/SOTA/complete
对外表述都应冻结。**

## 5. 对当前候选问题的重新分级

| 候选 | 本轮正确状态 | 最危险的杀伤 | 可保留的科学问题 |
|---|---|---|---|
| I1 一般 label-free N-best selector | `DIRECT_OCCUPIED` | MBR、ASR/ST reranking、audio BoN | 不作为独立身份；仅作基线/组成件 |
| I2 audio-grounded frozen-omni selector | bare mechanism `DIRECT_OCCUPIED` | Scaling Auditory、Jia SER、READ 等 | same-core 与 external/frozen-peer 的误差相关性是否决定可兑现 headroom |
| I3 abstain/Goodhart constrained selector | component-wise occupied; exact speech union open | selective prediction + text inference-time reward hacking | Goodhart 拐点能否由 label-free observables 预警，并在 risk-coverage 下优于 MBR |
| I4 `(c, selector)` realization surface | domain instantiation possibly open; methodology occupied | general TTS scaling laws、KIT、JudgeBoN | 从描述曲面升级为可预测/可决策的规律 |
| UMBRELLA training-free RL for omni agentic system | exact intersection not found; components crowded | JitRL、IAD、AudioToolAgent、Scaling Auditory | 证明 equal-budget iterative loop 明显优于 one-shot BoN，且不是换名系统集成 |

这里必须特别加入：

- [JitRL](https://arxiv.org/abs/2601.18510) 已经把“training-free RL、无梯度、KL 约束、test-time
  policy optimization”用于文本 agent；所以 training-free RL 本身不是新颖性。
- [AuTAgent](https://arxiv.org/abs/2602.13685) 用 RL 学习音频工具调用，虽然改权重，不占据 frozen 设定，
  却是必须超过的 tool-use cousin。
- [Inference-Time Reward Hacking](https://arxiv.org/abs/2506.19248) 已证明 BoN 等推理时奖励优化会出现先升后降，
  直接要求 I3 把 proxy/true utility 分离。
- [MUGEN](https://arxiv.org/abs/2603.09714) 展示 training-free audio-permutational self-consistency；
  说明 training-free audio gain 的方法空间也已拥挤。
- [On the Role of Feedback in Test-Time Scaling of Agentic AI Workflows](https://arxiv.org/abs/2504.01931)
  是 loop-vs-one-shot 预算公平性的重要近邻。

## 6. 推荐保留为 proposal 的探索方向与检查点

Stage-1A 不应现在收敛为单一路线，但下一轮 survey 必须围绕能被杀死的科学问题，而不是继续堆论文数量。

### Proposal A — 供给条件下的可预测兑现规律

**问题：** 能否用不读标签的 pool statistics、reward dispersion、candidate diversity、same-core/peer score
correlation，预测 held-out `(model, task, c)` 的 `H(c)` 与 `rho(c)` 区域？

**Stage-1A 检查点：**

1. survey 是否找到 text/vision/robotics 中同类 diagnostic scaling laws；
2. 新意是否是新的 predictor/causal regularity，而非换成 audio 数据画表；
3. 预先列出反例：高 diversity 但无 headroom、high reward dispersion 但 true utility 下降；
4. 定义 held-out prediction 的未来 Stage-2 验证，而非事后拟合全矩阵。

**kill 条件：** 若一般 scaling-law 基线已能不加 audio-specific variable 地同样预测，或只能描述不能预测，
则 I4 不够成为核心方法贡献。

### Proposal B — 选择器误差去相关：same-core 何时有用、何时自证循环

**问题：** generator 与 scorer 共用同一 frozen core 时，错误是否高度相关，从而使 same-core likelihood
只能重复偏差；frozen peer/audio-grounded verifier 在什么条件下更能兑现 headroom？

**检查点：**

1. 区分 same-core native score、same-core prompted judge、external frozen peer、trained reward；
2. 文献核查 calibration、self-evaluation blind spots、judge bias、MBR consensus；
3. 未来原型需 equal-K/equal-call 比较，且同报 `rho_greedy/rho_pool/delta_mbr/regret`；
4. 明确 external peer 是否注入 new-info，守住 information boundary。

**kill 条件：** 若 same-core 不优于 MBR，peer gain 又完全来自额外知识/预算，则“frozen omni native
selector”身份不成立。

### Proposal C — Goodhart 拐点检测与可弃权选择

**问题：** 在扩大 K、提高温度或增加工具调用时，proxy reward 提升而 true utility 下降的拐点能否由
label-free signal 检出，并通过 abstention/hedging 控制风险？

**检查点：**

1. 把 reward hacking、selective prediction、conformal risk control、speech uncertainty 四族文献合并调查；
2. 不允许把 golden utility 用于 selector，只用于事后 Stage-2 evaluation；
3. 预定义 risk-coverage 和 overoptimization budget，不以单点 accuracy 代替；
4. 理论轨若保留，必须与工程同一 operator，证明 unconstrained failure 与 constrained convergence。

**kill 条件：** 若拐点只靠 gold label 事后看到，或置信度基线已完全支配，则该方向不是可部署贡献。

### Proposal D — Agentic loop 是否真的超过等预算 one-shot BoN

**问题：** training-free agentic feedback loop 在同总调用、token/audio、latency 预算下，是否比一次性扩大
候选池产生稳定的额外价值？

**检查点：**

1. survey 分开 feedback、memory、retrieval、tool-use、candidate revision、selection；
2. 必须有 equal-budget one-shot BoN/MBR、random feedback、no-feedback loop；
3. 价值必须来自反馈改变下一动作，不是更多 sample 或新信息泄漏；
4. 如果增益只在第一轮、后续饱和，proposal 应降级为 best-of-N selector，而非 agentic RL。

**kill 条件：** loop 在公平预算下不超过强 BoN/MBR 的预设 SESOI，或成本优势消失。

### Proposal E — 供给选择本身作为决策问题

**问题：** 给定预算，先选择 prompt/retrieval/tool/decoding supply `c`，再选择 K 池候选，是否能形成比固定
`c` 更强的两层 policy？

**检查点：**

1. 不能把无限试 supply 当作探索自由；每个 supply change 都登记并计入预算；
2. 区分 read-out 与 new-info；
3. 比较固定供给、oracle 供给、label-free routing；
4. 研究贡献必须是 routing rule 或可证明约束，不是工程菜单。

## 7. 分阶段整改计划

### P0 — 下一份 Survey Response 必须先完成，才允许本轮复审签收

1. **状态纠偏：** 全部 `Survey complete/调研收官` 降为 `ROUND1_SCOUT_COMPLETE`；Stage-1C package 改标
   `PRE_STAGE1C_DECISION_DRAFT`。不要求重写历史；用新的定日期 response 声明 supersession。
2. **提交 replay bundle：** 严格使用配套模板。历史缺失原始结果时标 `RAW_EVENT_UNAVAILABLE`，不得补造。
3. **重算计数：** 分开 SEARCH=218、FETCH=87 这一类事件；给出 returned/screened/excluded/included、
   exact unique works/versions。
4. **规范去重：** 每篇 work 有 canonical ID、version、aliases、merge reason；把 `~93` 替换为可重建精确值，
   或明确承认无法重建。
5. **证据降级：** 39 个 FT 标签逐一审计；没有固定全文和 locator 的全部降级。优先双审所有
   load-bearing closest challengers。
6. **纠正事实：** READ、MBR/Llama-3、TAP-GER、ProGRes；检查所有数值和 operator type 的同类错误。
7. **修复 identity：** bare I2 标 occupied；I2∩I4 新身份另列；冻结所有候选定义。
8. **修复术语检查：** 清除 `EMPTY` 和裸 `NO_DIRECT_MATCH`；让 validator 失败时真正阻断状态升级。

### P1 — 在 owner 被请求做 Stage-1C 选择之前

1. 完成 9 个 round-2 saturation targets；每个 lane 做 backward/forward citation chase 和方法别名查询；
2. 补 general test-time scaling、vision/VLA/robotics、self-evaluation/judge bias 文献；
3. 形成 I1/I2/I3/I4/UMBRELLA 的冻结 identity contract 和 post-hoc 条件日志；
4. 把 SOTA cards 降级并重建为同协议 comparator cards；
5. 关闭 C1 尝试普查、C4 负结果普查和 same-selector contract；
6. 由未参与 survey 生成的 reviewer 从 replay bundle 盲重建计数、去重和五个关键 claim；
7. 只有所有阻断项关闭，才可申请 `STAGE1C_DECISION_READY`；owner 仍需亲自选择，不自动滚入 Stage-1B。

### P2 — 仅当 owner 选择后，为未来 Stage-1B/Stage-2 预留

1. Stage-1B directional prototype 使用单次触碰、attempt registry、失败全登记；
2. 不在 Stage-1A 用小样数字宣称显著性或 SOTA；
3. Stage-2 才冻结 SESOI、数据 split、paired bootstrap、预算公平性和完整 controls；
4. 任何 Stage-1 数字保持 hypothesis-grade，不能通过措辞升级证据等级。

## 8. 签收门槛

团队下一次 response 只有同时满足以下条件，才值得 reviewer 重新签字：

```text
[ ] 新 response 固定 commit + canonical hashes
[ ] replay bundle 通过独立重放
[ ] SEARCH/FETCH/returned/screened/included/excluded 分开重算
[ ] exact unique paper/work/version 可重建
[ ] 全部 load-bearing claims 有 fixed version + locator + double review
[ ] READ/MBR/TAP-GER/ProGRes 已纠正
[ ] bare I2 与 I2∩I4 不再混写
[ ] general TTS scaling/VLA 文献进入 kill matrix
[ ] SOTA cards 降级或达到严格可比性
[ ] 禁词与状态机检查真正 fail-fast
[ ] C1/C4 与已知 round-2 targets 关闭或明确保留 blocker
[ ] 无 Stage-1B 自动授权
```

## 9. 最终博导意见

团队近期工作不是“没有价值”，而是**产出速度超过了证据治理能力**。当前最危险的习惯不是某一篇论文漏搜，
而是每完成一轮 AI scout 就立刻把 batch-complete 写成 survey-complete，再把 exact-intersection 未命中写成
科学空白。这个习惯如果不改，后续即使跑出好数字，也会因为无法回放、无法审计、无法区分 selector 与
revision、无法证明比较公平而失去可信度。

我的建议不是让 Stage-1A 过早收敛。恰恰相反：继续广度探索，但把每次探索变成可回放事件；允许大胆提出
I4、Goodhart、agentic loop 等候选，却不允许通过追加限定词维持 novelty。真正值得成为 proposal 的不是
“training-free RL for omni agentic system”这串交集本身，而是一个经强近邻攻击后仍能给出**新预测、
新约束或新决策规律**的具体科学问题。
