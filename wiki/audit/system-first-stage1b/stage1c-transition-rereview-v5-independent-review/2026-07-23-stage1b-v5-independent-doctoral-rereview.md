---
review_type: "independent doctoral adversarial rereview"
review_date: "2026-07-23"
campaign: "system-first-stage1b"
review_target: "stage1b-v5-literature-promotion-and-stage1c-transition-rereview"
review_target_commit: "38fb9435d0c35e226ad62b16015a6dbee054e6c2"
review_target_is_ancestor_of_review_head: true
review_head: "050fc50a5024d227995816908215e5bed251c3d5"
stage_diagnosis_before_signature: "STAGE_1B_LATE_CLOSEOUT; STAGE_1C_PENDING_INDEPENDENT_SIGNATURE"
verdict: "SIGN_STAGE1C_COMMON_RUBRIC_COMPARISON"
stage1c_authority: "COMMON_RUBRIC_PROBLEM_COMPARISON_ONLY"
model_or_benchmark_execution_authority: "NOT_GRANTED"
problem_ranking_or_selection_authority: "NOT_GRANTED"
novelty_verdict: "NOT_REQUESTED_AND_NOT_ISSUED"
literature_universe_closed: false
all_related_assets_downloaded: false
academic_fraud_evidence_found: false
source_delivery_modified: false
---

# Stage-1B v5 独立博导级复审：签署进入受限 Stage-1C common-rubric comparison

## 一、最终裁决

**裁决：`SIGN_STAGE1C_COMMON_RUBRIC_COMPARISON`。**

v5 已经修复 v4 复审所限定的四个转段缺陷：

1. 既有论文从 canonical corpus 到 current comparison layer 的提升链可以追踪；
2. Python 与 PowerShell 资产盘点器在真实磁盘上语义一致；
3. Audio2Tool 的远端内容、下载器辅助文件与本地额外文件已经分层；
4. 评审可见附录能够区分 direct controller、prompted judge、trained reward model、
   measurement instrument 和 boundary comparator。

因此，本审稿人不再以“继续扩大 Stage-1B survey”或“继续增强脚本对抗鲁棒性”为理由拖延转段。
项目可以进入 **Stage-1C 的统一量表问题比较**，比较以下三个仍未排序的候选问题族：

- budget / stopping / repair；
- evaluator / reward reliability；
- interactive / full-duplex objectives。

这个签署的权限边界必须逐字保留：**不得据此调用研究模型或外部模型 API，不得运行数据集指标、
smoke benchmark、论文复现、方案原型，不得给三个问题排序，不得替 owner 选题，不得宣布技术创新或
novelty 已成立。** Stage-2A 仍然必须 reproduction-first。

本次签署也不等于以下不成立的命题：

- “语音/多模态相关论文已经穷尽”；
- “所有论文对应的数据、代码、模型都已下载”；
- “26 个 direct methods 中已经存在与本项目相同的 reward-guided black-box controller”；
- “资产存在就等于已取得许可证或已经具备复现实验条件”。

## 二、当前到底处于哪个阶段

签署前的客观状态是 **late Stage-1B closeout / Stage-1C transition candidate**。

判断依据不是文件名，而是交付物的实质：

- `wiki/Research-Objective.md` 把当前状态写为 late Stage-1B closeout，并明确要求独立签名；
- 固定科学交付是 commit
  `38fb9435d0c35e226ad62b16015a6dbee054e6c2`；
- 当前产出仍是 method-path、evidence depth、prior routing、instrument coverage 和 asset
  feasibility，没有项目自己的模型结果、benchmark 分数、复现结果或方案优胜结论；
- v5 请求的也只是 `STAGE1C_COMMON_RUBRIC_PROBLEM_COMPARISON_ONLY`。

本报告提供了所缺的独立签名。团队把这一裁决登记到 HOT/CURRENT 状态后，可以把治理状态更新为
**Stage-1C common-rubric comparison started**。在此之前，不应倒写成“Stage-1C 早已开始”。

Stage-1C 的研究对象是“哪一个问题值得在后续复现与技术探索中优先处理”，不是“哪个新算法已经
胜出”。它可以继续阅读、补充和比较文献，但不能借“比较”之名提前执行 Stage-2 实验。

## 三、审查方法与四轮对抗式复核

本次审查先使用仓内完整论文集和冻结记录，再以 arXiv、ACL Anthology 等官方页面进行窄范围反查；
没有用搜索摘要替代团队已有的本地全文。

### Round A：尝试推翻 release identity 与可回放性

- 固定 commit 存在，且是审查时 HEAD 的祖先；
- release manifest SHA-256 为
  `20a289487c846b45891488ee038a4321f80e20ed772a76837ce2954ff0b5a8e9`；
- 独立读取固定 commit 的 64 个 Git blobs 和当前数据盘的 44 个 external artifacts，
  108/108 字节数与 SHA-256 一致；
- 工作树 CRLF 展开造成的 Windows working-tree raw-byte 差异不构成证据失败，因为仓库已明确以
  Git blob bytes 为历史证据权威。

结论：没有复现 release identity 伪造、manifest 自证循环或静默漂移。

### Round B：尝试推翻论文提升、角色与引用闭包

- 18 个 promotion works 身份唯一；
- 18/18 均有本地 PDF、e-print 和可核对 hash；
- 46-row strict supplement 为 26 direct / 18 instrument / 2 boundary；
- 59-route appendix 覆盖全部 46 个 supplement rows 和 13 个 routed-only rows；
- MM-ReAct 与 AuTAgent 不再从 reviewer-facing appendix 消失；
- 18 个 promotion works 全部能在 appendix 中找到，并有官方元数据 receipt。

结论：v4 所指出的“看过但没有进入 current comparison layer”的知识提升缺陷已经关闭。

### Round C：尝试用真实磁盘推翻资产陈述

- 在真实 `SPEECHRL_DATA_DIR` 上分别重放 native Python 与 PowerShell inventory；
- 两者均得到 `31 frozen / 33 candidate / 5 auxiliary / 0 missing`；
- 规范化后语义一致；
- UniSRM-Bench 为 1,463 文件、325,920,409 bytes、0 missing，并绑定 HF revision；
- SpeakerSleuth、ParaPairAudioBench、UniSRM 三个 reference repo 的本地 HEAD 与锁定 commit
  一致；
- Audio2Tool 为 71,441 个 revision-bound remote files、11 个 `.hfd` auxiliary files、
  610 个 retained extraneous files，三者不再混计。

结论：v4 的 producer parity 与目录内容身份问题已经真实修复，不是只修改了报告数字。

在仓库规定的 WSL2 `Ubuntu-24.04` 与 `~/.venvs/speechrl` 环境中，复跑与本轮 gate 直接相关的
asset/data tests 12 项、survey/evidence tests 38 项和 release-manifest tests 7 项，共 57 项全部
通过。这里的测试结论只证明 evidence contract 与资产路由可重放，不是研究实验结果。

### Round D：尝试用近邻论文改变候选问题集合

外部反查找到了尚未进入 v5 strict supplement 的近邻，但没有找到会新增第四个非 H5 候选问题、
删除现有三个候选问题，或推翻“strict speech/omni direct set 中 reward-guided selection = 0”的证据。
反查结果和处置见第七节。新增工作主要补强已有 measurement/boundary axes，因此应进入 Stage-1C
滚动 intake，而不是重新冻结一个 v6 Stage-1B 大调查。

## 四、对 v5 四个 gate 的逐项裁决

| Gate | 裁决 | 独立证据 | 剩余问题 |
|---|---|---|---|
| P0-A canonical-to-current promotion | **PASS** | 18 identities、PDF/e-print/hash、metadata receipts、mapping、eligible inputs 与 appendix 可交叉追踪 | 五个 reviewer-directed outside-union identities 的动作名称需改得更准确，见 §6.2；不影响去重事实 |
| P0-B inventory producer parity | **PASS** | Python/PowerShell 对同一真实磁盘均为 31/33/5/0，非标准 `repos/...` 路径不再被误分 | 后续不得把 native traversal 选择写成 WSL2 ML 环境变化 |
| P1-C Audio2Tool identity/hygiene | **PASS** | remote/auxiliary/extraneous 三层计数成立，未删除用户文件 | Stage-2 loader 必须消费 revision-bound allowlist；当前不能宣称可直接实验 |
| P1-D citation/role separation | **PASS** | 59 个唯一 route，stable identity、role 与 evidence route 齐全 | MUGEN 共识聚合应在 Stage-1C 子机制中单列；跨层 role drift 需清理 |

没有剩余的 release-bound P0/P1 缺陷足以继续 withheld Stage-1C comparison。

## 五、引用是否合理

### 5.1 身份、链接和论文陈述总体合理

v5 的 reviewer-facing 引用没有把项目自己的结果嫁接到论文结果上，也没有把预印本指标写成团队
已复现指标。18 个提升对象具备官方身份、本地全文和 hash；59-route appendix 中 title、author、
year、stable link、role 与 evidence route 可核对。

重点论文的角色也比 v4 前更严谨：

- AudioJudge、Audio-Aware Judges、SpeakerSleuth 和 ParaPairAudioBench 是 measurement
  instruments，不因“能打分”就自动成为 direct controller；
- UniSRM、SpeechJudge、SpeechLLM-as-Judges 等含训练的 reward/judge 工作被当作 trained
  boundary，而不是本项目的 training-free 证据；
- VideoFDB 被明确作为 AV2AV full-duplex boundary，而不是用一个视觉 benchmark 宣称已经覆盖
  全部 omni-agentic 任务；
- MUGEN 的 K=10 audio-permutational self-consistency 确实会改变最终答案，因此从“只测量”提升为
  direct inference method 是有全文依据的。

### 5.2 不应把 `9/9/8/0` 当作自然界唯一正确的分类

MUGEN 目前被计入 `EVALUATOR_OR_VERIFIER_GATED`。其真正机制是多次音频顺序置换、回答映射和
majority-vote consensus。共识聚合会改变最终选择，但它既不是独立 evaluator，也不是验证候选正确性
的 verifier，更不是 scalar reward。

因此，`9 orchestration / 9 state-event / 8 evaluator-verifier / 0 reward-guided` 可以作为 v5
冻结 taxonomy 下的可回放计数，但 Stage-1C 不得据此把“self-consistency consensus”与“外部
evaluator/verifier”混为一个因果机制。建议在 comparison matrix 中加入正交字段：

```text
decision_signal_origin = {
  environment_state,
  tool_observation,
  self_consistency_consensus,
  prompted_self_judge,
  external_frozen_evaluator,
  trained_reward_model,
  rule_or_oracle
}
```

这是一项 **P2 taxonomy correction**，不是继续阻断转段的理由。更严谨的子机制展示可以写为
`9/9/7/1/0`（其中 1 为 consensus aggregation），同时保留 v5 原始冻结计数用于 provenance。

### 5.3 不得把 citation closure 写成 literature-universe closure

v5 已经主动写明 closed promotion set 不是 literature-universe closure，这一点正确。当前可以声称：

> 对冻结 D0、既有 registry 和 v4 指定 promotion set 的证据路由已经闭环。

当前不能声称：

> 所有 training-free speech/omni agent、speech evaluator 或 multimodal agent 论文已经穷尽。

后续出现新论文不构成 v5 造假，也不自动推翻本签署；只有当新论文改变候选问题集合或直接否定某个
load-bearing premise 时，才需要触发 gate-level reopening。

## 六、仍然存在的结构性问题，但不再阻断 Stage-1C

### 6.1 `Inference-Time Scaling for Joint Audio-Video Generation` 存在跨层 role drift

[该论文](https://arxiv.org/abs/2606.03183)提出 training-free joint audio-video generation 的
multi-verifier framework 与 Adaptive Reward Weighting；其 reward aggregation 会进入 test-time
selection，但研究对象是联合音视频生成，不是本项目当前的 speech/omni agentic task controller。

仓内不同层目前给出三种口径：

- bounded registry：`KEEP_CORE`，甚至标为 `speech_primary_object=true`；
- secondary filter：`transfer-only`；
- current bibliography：`MEASUREMENT_INSTRUMENT`。

这里不是 citation identity 错误，而是知识组织中的 **role drift**。Stage-1C 应把它统一为
`TRANSFER_BOUNDARY_DIRECT_CONTROL` 或等价名称：它是 reward-guided multimodal inference-time
selection 的强 transfer prior，但不是 strict speech-agent direct occupancy 的一部分。它会约束
multi-objective reward aggregation、verifier hacking 和 reward normalization 的讨论，不应被降格成
单纯“测量工具”。

### 6.2 五个 outside-union identities 的动作描述略有过度概括

proposal 把 18 项统一写成
`REUSE_CANONICAL_WORK_ID_NO_DUPLICATE_CLAIM_WORK`；实际 reconciliation JSON 透明地区分了：

- 13 项 `REUSED_EXISTING_CANONICAL_ID`；
- 5 项 `REVIEWER_DIRECTED_OUTSIDE_UNION_IDENTITY`：`2510.00743`、`2510.14664`、
  `2511.07931`、`2605.23261`、`2605.30256`。

后五项没有制造 duplicate seed，也已经获得稳定 canonical identity；但从语义上说，它们不是“复用
此前 union 内已有 ID”。下一版 action token 应写成
`REGISTER_REVIEWER_DIRECTED_CANONICAL_ID_NO_DUPLICATE_SEED`。底层 JSON 已经披露真实差异，因此这不是
证据隐瞒或学术欺诈，而是 proposal 叙述压缩过度。

### 6.3 当前知识组织仍需防止“历史中存在、current 中失语”再次发生

v5 修复了本轮 18 项，但长期规则应是：任何命中 Stage-1C 某一 bundle 的 canonical work 都必须能
机器追踪到 `INCLUDE / BOUNDARY / EXCLUDE_WITH_REASON / QUEUED` 之一。不得再依靠审稿人逐个 `rg`
才能发现论文曾经读过。

这项改进应在 Stage-1C intake 中完成，不需要为它重启 Stage-1B。建议把 registry-to-current check
限定为“命中三个 active bundles 的新增或状态变化对象”，不要再次扫描全部文献宇宙。

## 七、是否仍有相关论文遗漏

答案是 **有，但属于分层的、可解释的遗漏；没有发现新的转段阻断型直接先验遗漏**。

### 7.1 Stage-1C 应优先补入的 measurement / boundary works

| 工作 | 当前仓内状态 | 为什么相关 | 建议角色 | 是否阻断本次签署 |
|---|---|---|---|---|
| [TRACE / Hearing Between the Lines](https://aclanthology.org/2026.findings-eacl.151/) | 未见 current route | 用显式 content、voice quality、paralinguistics 维度和 deterministic fusion 构造低成本 S2S evaluator，直接约束 evaluator decomposition 与 proxy fusion | `MEASUREMENT_INSTRUMENT`；若接入 action 再评估 controller role | 否；补强已有 evaluator bundle，不改变候选集合 |
| [S2S-Arena](https://aclanthology.org/2026.acl-long.1615/) | 历史 synthesis/档案中出现，未进入 v5 current comparison surface | speech-native、pairwise、paralinguistic instruction following，适合约束“文本成功不等于语音交互成功” | `MEASUREMENT_INSTRUMENT` | 否；其测量轴已部分由 ParaPair、AudioJudge、VideoFDB 覆盖 |
| [MTalk-Bench](https://arxiv.org/abs/2508.18240) | 2026-07-14 search log 标记 follow-up，未见 current route | multi-turn S2S，比较 arena 与 rubric，并报告 position/length/nonverbal judge 风险 | `MEASUREMENT_INSTRUMENT` | 否；补强 multi-turn 与 evaluator-bias 子轴 |
| [SimulU](https://arxiv.org/abs/2603.16924) | 已在 DOA backward-citation closure 中暴露，未进入 current route | training-free long-form SimulS2S policy，会管理 history 与 speech output selection | `MODEL_INTERNAL_BOUNDARY` | 否；依赖 cross-attention，违反项目黑盒外设控制假设 |

VCB Bench `2510.11098` 不应再被称作遗漏：它已在 current 81-work coverage 中以
`MEASUREMENT_INSTRUMENT / ROUTED_ONLY / FULLTEXT_ROUTED` 出现，本地 PDF/e-print 也存在。它尚未进入
strict supplement 是一个有记录的 routing decision，而不是 silent drop。

### 7.2 为什么这些遗漏不应再导致 WITHHOLD

严格审稿不是无限扩张阻断条件。是否阻断应看“缺失工作是否改变转段决策”，而不是“还能否找到
另一篇相关论文”。上述新增对象：

- 没有新增第四个非 H5 问题族；
- 没有证明现有三个 bundle 中任何一个应被删除；
- 没有出现符合 strict black-box speech/omni agentic 范围的已完成 reward-guided controller；
- 主要补强 evaluator、paralinguistic、multi-turn 与 model-internal boundary。

所以合理处置是：**签署 Stage-1C，并把四项放入 Stage-1C 的 bounded priority intake；在问题最终排序
和 owner selection 前完成路由。** 若把任何新 measurement paper 都升级成 Stage-1B P0，阶段将永远
无法结束，这不符合本项目已经确定的分期原则。

## 八、语音与多模态智能体覆盖是否完备

结论应分成两句话：

1. **对开始 Stage-1C common-rubric comparison 而言，覆盖已经足够。**
2. **对声称“speech/omni agent literature comprehensive closure”而言，覆盖仍不完备。**

| 研究轴 | 当前覆盖 | 严格评价 |
|---|---|---|
| speech tool/agent orchestration | AudioGPT、Speech-Copilot、AURA、AudioToolAgent、Audio-Maestro、Audio2Tool、Omni-DeepSearch 等 | 较强，足以形成 external orchestration 对照 |
| budget / stop / repair | fixed-budget consensus、event/state gates、retry/stop、tool observations、decision-utility failure | 可开始比较，但 adaptive budget、harm-aware stopping 与 realized utility 仍是问题而非已解决结论 |
| evaluator/reward reliability | AudioJudge、Audio-Aware Judges、SpeakerSleuth、ParaPair、UniSRM、WavReward、GSRM、SDiaReward 等 | 已覆盖 frozen judge、trained reward、pairwise/tie/calibration 等主要类别；TRACE/MTalk 可继续补强 |
| interactive/full-duplex speech | VoiceAgentBench、tau-Voice、FDB-v3、EVA-Bench、IHBench、EchoChain、Unit-Based Agent | 较强，但若无 exact tau-Voice/EchoChain assets，只能做文献比较与 feasibility 评级 |
| true audio-visual/full-duplex | VideoFDB 明确入 boundary；Joint AV ITS 已在 corpus；Active Perception 等提供系统近邻 | 仍偏薄，只足够作为 explicit boundary，不得宣称覆盖所有 AV2AV agent |
| GUI/robotics/embodied omni | 只有 FAM-HRI、GUI assistant、Pepper 等少量 transfer objects | 非当前 operational scope；不应为追求字面“omni”无限扩张 |
| reward-guided black-box action control | strict set 仍为 0 | 这是 Stage-1C 需要比较的潜在 gap，不是已经证明的创新性结论 |

“omni”在 Stage-1C 必须继续使用 operational definition：当前核心是 speech/audio/text/tool 和明确的
audio-visual comparator，不代表 GUI、robotics、embodied world model 和所有感知模态都已经纳入。

## 九、论文、研究内容和数据是否已经锁定并下载到本地

### 9.1 论文全文：转段核心已锁定，文献宇宙未全部本地化

- 46-row strict supplement：46/46 能通过 fulltext ledger 定位到本地 PDF；其中 WSL 路径记录需按
  `/mnt/e/...` 映射到同一数据盘，不能用 Windows `Path` 直接误报 missing；
- 18-work promotion set：18/18 PDF 与 e-print 均本地 hash-bound；
- 59-route appendix：59 个身份与 route 已锁定，但“有 route”不等于每个关联 artifact 都公开；
- 81-work speech/omni coverage：70 项 `FULLTEXT_ROUTED`，11 项 `ABSTRACT_ROUTED`；后 11 项均为明确
  `EXCLUDE_WITH_REASON` 的训练/内部适配边界，不承担 Stage-1C load-bearing claim；
- frozen D0/226-work registry 是声明表面的闭包，不是整个学界的闭包。

因此，对“Stage-1C 核心比较论文是否锁定”的回答是 **是**；对“所有相关论文是否全部下载”的回答是
**否，也不应把后者设成转段条件**。

### 9.2 数据与代码：关键公开子集已锁定，但绝不是全部下载完毕

已独立确认：

- frozen baseline 31 项全部 present；
- candidate-unfrozen 33 项与 auxiliary 5 项被真实盘点，但它们不是 frozen baseline；
- UniSRM-Bench 在 pinned revision 下 1,463/1,463 文件齐全；
- SpeakerSleuth、ParaPairAudioBench、UniSRM reference repositories 本地 commit 匹配；
- VoiceAgentBench、FDB-v3、Audio2Tool、Omni-DeepSearch、IHBench 等先前锁定资产继续存在；
- Audio2Tool 的 610 个 extras 没有被冒充为远端数据，也没有被擅自删除。

未下载或尚不可完整获得的精确资产至少包括：

- SpeakerSleuth 宣布的 benchmark code/data：当前项目仓库只有 project page；
- ParaPair 的 SVC age/gender source audio：需要人工 access review；
- Audio-Aware Judges 的 StyleSet：论文宣布释放，但固定版本没有可验证 endpoint；
- VideoFDB evaluation data：需要接受条款和密码，不能替用户自动同意；
- tau-Voice 精确 voice dataset：本地 tau2 base 不能冒充它；
- EchoChain code/data：未核实公开发布；
- From Text to Voice 的 packaged generated corpus：尚未锁定；
- 部分 LALM judge production recordings：私有或待发布。

所以“所有相关研究内容和数据集已经下载到本地”的回答必须是 **否**。v5 对这些不可得资产的陈述是
诚实的，而且没有用相邻数据集替换精确数据。它们不阻断 Stage-1C 文献量表比较，但应进入
feasibility / reproduction-readiness 字段，并可能在 Stage-2A 阻断某一具体复现路线。

## 十、是否存在超越本阶段的探索尝试

**没有发现实质越级。**

本轮执行了论文全文获取、官方元数据核对、代码/数据 revision pin、资产可得性检查、inventory 重放、
manifest/hash 验证和 evidence-contract tests。这些属于 Stage-1B 收尾的知识与可得性工作，不是模型
实验。

没有发现：

- 模型或 API inference；
- 数据集任务分数或 benchmark ranking；
- 论文结果复现；
- controller prototype；
- 候选问题排序或 owner selection；
- 通过当前表格宣称 novelty 已证明。

“下载公开数据用于确认是否可得”本身不等于 Stage-2 复现；反过来，“数据已经下载”也不能赋予后续
执行权限。

## 十一、学术诚信与造假风险判断

### 11.1 未发现足以支持学术欺诈、数据伪造或故意篡改的证据

本轮没有研究实验结果可供伪造。固定 commit、manifest、Git blobs、external hashes、论文全文、
inventory、repo commits、HF revision 与文件计数均能独立复核。团队也保留了 unavailable、private、
manual-access 和 terms-required 状态，没有用近邻资产填补数字。

因此，不能把以下问题升级成“学术欺诈”：

- MUGEN taxonomy 粒度不够；
- 五个 outside-union IDs 被 proposal 统一简写为 reuse；
- Windows working tree 的 CRLF bytes 与 Git blob bytes 不同；
- Audio2Tool 目录含有额外下载器文件；
- 有新论文未进入本轮 bounded supplement。

这些都有可审计的底层记录和非欺诈解释。

### 11.2 仍需警惕的诚信风险

如果后续发生以下行为，风险会显著升级：

- 把 `REWARD_GUIDED_SELECTION = 0` 改写成“学界没有相关工作”；
- 用 46-row strict supplement 代表整个 literature universe；
- 把 prompted judge 的 correlation 当作 evaluator-guided action utility；
- 把 candidate inventory 中“目录存在”写成“许可证、任务 split 与复现都已就绪”；
- 把 MUGEN 共识投票或 Joint AV generation 的 reward selection 直接宣称为与本项目同一问题设置；
- 在未运行模型的情况下暗示 paper-reported metrics 是项目验证结果。

当前团队没有实施这些行为。Stage-1C 的 common rubric 应把这些列为明确的 anti-overclaim checks。

## 十二、Stage-1C 获准后的严格执行要求

### 12.1 允许做什么

1. 为三个非 H5 bundle 建立统一、未排序的 comparison matrix；
2. 继续读已有本地全文，并对第七节四项优先文献做 bounded intake；
3. 比较 problem importance、evidence strength、measurement validity、asset feasibility、
   black-box compatibility、failure severity 与 reproduction tractability；
4. 对矛盾证据、不可得资产和 role drift 保留显式 uncertainty；
5. 形成给 owner 的问题选择材料，但在获得 owner 决定前不宣布 winner。

### 12.2 不允许做什么

1. 不运行模型、数据集、benchmark 或 smoke set；
2. 不复现论文，不写 controller prototype，不做超参试验；
3. 不因某个 bundle 文献更多就把它自动排第一；
4. 不把“工程上容易”与“研究问题重要”混成一个分数；
5. 不把 literature proximity 直接等价为 novelty verdict；
6. 不把 inaccessible exact asset 用相邻公开资产替代；
7. 不把 H5-dependent evidence-state 或 tool/agent arbitration 偷渡回 eligible set。

### 12.3 三个 bundle 必须共用的最小 rubric

| 维度 | 必答问题 |
|---|---|
| problem distinctness | 该问题是否是 external black-box control 的独立问题，而不是已有训练方案的改名？ |
| decision causality | 信号是否真的改变 next action、selection、stop 或 repair，而不只是事后打分？ |
| measurement validity | proxy 与终端任务效用是否区分；是否有 pairwise/tie/calibration/bias 证据？ |
| modality necessity | load-bearing audio/visual 信息是否超出 transcript 能恢复的内容？ |
| failure severity | 错误会导致无收益、成本浪费、错误停止、错误修复还是实质 harm？ |
| feasibility | exact paper/data/code/licence 是否可得；不可得是否会阻断 Stage-2A 复现？ |
| reproduction anchor | 是否存在可在 Stage-2A 首先复现的最近公开基线？ |
| scope compatibility | 是否满足 frozen core、API-visible/black-box、external control 的约束？ |
| evidence maturity | 结论来自 abstract、full text、artifact inspection 还是项目 reproduction？不得混级。 |

### 12.4 三个 bundle 的专属检查点

**Budget / stop / repair**

- fixed K、adaptive budget、latency/cost/risk budget 分开；
- terminal environment state、heuristic、consensus、uncertainty、evaluator stop 分开；
- 报告 oracle headroom、realized gain、regret、harm 和 unnecessary calls；
- repair 必须改变下一 action，不能只生成解释。

**Evaluator / reward reliability**

- pointwise、pairwise、listwise、tie/abstention 分开；
- transcript-only、audio-aware、self-judge、external frozen judge、trained reward model 分开；
- position、verbosity、lexical dominance、speaker/prosody、distribution shift 与 verifier hacking 纳入；
- judge-human agreement 与 judge-guided downstream utility 分开；
- TRACE 的 deterministic feature fusion 与 Joint AV ITS 的 adaptive reward aggregation应作为两种
  不同 proxy-composition 边界。

**Interactive / full-duplex**

- terminal task success 与 interaction quality 双主轴；
- interruption、barge-in、state update、resume/recovery、latency、tool correctness 分开；
- audio-only 与 AV2AV 分层；
- S2S-Arena/MTalk/VCB 类 benchmark 用于补足 paralinguistic、real-speech、multi-turn robustness，
  不把 speech naturalness 单分数当作 agent success。

## 十三、给研究团队 AI 的明确执行指令

1. 将本裁决登记为 `SIGN_STAGE1C_COMMON_RUBRIC_COMPARISON`，不要改写历史 v4/v5 audit；
2. 更新 HOT/CURRENT 阶段状态时，明确“Stage-1C comparison only”；
3. 不再开启 v6 式无界 Stage-1B broad discovery；
4. 在 Stage-1C intake 中优先路由 TRACE、S2S-Arena、MTalk-Bench、SimulU；
5. 清理 Joint AV ITS 的跨层 role drift，并把 MUGEN 的 consensus 子机制单列；
6. 修正五个 outside-union identity 的 action token，但不要制造第二个 canonical work；
7. 所有不可得资产保持 unavailable/manual/terms-required，不自动接受条款，不使用替代品冒充；
8. Stage-1C 比较完成后，先向 owner 提交未执行实验的 problem-selection dossier；
9. 没有 owner 选择与 Stage-2A 授权前，不触碰模型，不跑 benchmark，不开始复现。

## 十四、签署语

基于固定 commit、108 项证据清单、18 项 promotion closure、46 项 strict supplement、59 项引用路由、
两套真实磁盘 inventory 重放、公开资产与 unavailable 状态核验，以及对近邻论文的官方来源反查，本审稿人
确认：v5 已达到从 Stage-1B 文献/方法路径映射转入 Stage-1C 问题比较所需的充分而非无限条件。

**正式签署：`SIGN_STAGE1C_COMMON_RUBRIC_COMPARISON`。**

签署只授权 common-rubric problem comparison。模型执行、论文复现、技术方案实现、问题最终排序、
owner selection 与 novelty convergence 继续 withheld。
