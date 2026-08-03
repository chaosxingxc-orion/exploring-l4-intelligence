---
artifact_id: "SF-STAGE1C-CAPABILITY-PORTFOLIO-V1"
role: "CURRENT effective research-direction contract"
authority: "owner directions 2026-07-27/28/29 and direction-local repository ruling 2026-08-02"
stage: "DIRECTION_LOCAL_STAGE_PIPELINE"
endpoint: "DIRECTION_LOCAL_PIPELINE__R1_SUNSET__AUDIO_AWARE_EVIDENCE_ACQUISITION_FORMAL_OPENING_APPROVED__STAGE2A_EXECUTION_CONTRACT_PENDING"
execution_authority: "NO_ADMITTED_STUDY__EXECUTION_WITHHELD"
---

# 五维研究方向定稿：API-only 冻结多模态模型的可靠能力激活

> **2026-07-27/28/29 owner 整改裁决（先于本文其余内容生效）。** 五个维度和原九个候选方向继续作为
> Stage-1C 审计框架，但不保证九项都进入 Stage-2。R1 日落已由 owner 于 2026-07-29 确认
> （Decision-Log 续76）；R2 来源的语义研究对象 **audio-aware evidence acquisition** 已在
> 2026-08-02 的阶段对齐 v20 博导评审中通过 Stage-1C 并获正式开题许可。该许可不裁决创新性、
> 不冻结最终方法，也不授予 Stage-2A 执行权；红线=模型参数不可修改、不得新增一个任务训练模型或
> answering LLM，检索 trace-logging 放行。R3–R9 仍为执行者草稿、owner 未校验
> （`OWNER_UNVERIFIED`），待按 07-29 判据协同重审。**裁决 A**：项目核心为 Qwen3-Omni-30B（本地 llama.cpp serving lane 为后续可复现
> 载体，精确 revision 在独立执行合同中冻结）。**裁决 B**：ASR 主线为通用 ASR，MyST/RSR 等儿童 ASR
> 只作支持证据。**方向成立判据（owner 2026-07-29）**：方向必须完成充分调研，且属两型之一——(a) 本
> 领域存在已有工作，作为方法论基线提供实验、方法和工程依据并参与对比；(b) 本领域无已有工作，借鉴
> 其他领域内容设计实验、提出方法和改进；两型都必须在具体任务上与存量业内最优（SOTA）基线对比。
> **裁决 C/D/E（执行者代拟，owner 未签）**：不探索创新点、数据集只复用正式可得版本、指标复用官方
> 口径——作为工作默认保留，与 07-29 判据冲突处以判据为准。

> **2026-08-02 owner 工程架构裁决。** R1–R9 只保留为调研/论证 provenance，不是工程编号。每个通过
> 自身调研、owner GO 和执行合同的研究对象，按具体语义名称在 `studies/` 下建立独立 GitHub 仓；未入场
> 即日落的候选（R1）不建仓。一个方向进入工程后可并行调研下一个候选，无须等待所有候选调研完成。
> W1–W4 不再承载这些 study；umbrella Wiki 统一管理实验生命周期与资产图。

## 1. 主研究问题

> 当 speech/omni 核心模型只能作为冻结的推理 API 调用时，外部系统能否通过持续构造、选择和更新
> in-context 状态，可靠地激活模型已有的跨模态能力，并在不修改任何模型参数或内部结构的条件下提高
> 语音/音频任务效用？

研究对象是**外部 reward-guided control plane**，不是 evaluator、静态 selector、某个 benchmark 指标，
也不是一种新的专用 speech 模型。知识、记忆、技能和智能体编排决定模型每次看见什么上下文、可以执行
哪些动作；系统进化决定这些选择如何在实例内和跨实例随反馈改善。Training-free RL 是实现这种进化的
选定路线：reward/advantage 必须改变下一动作，终局 rerank 只是退化特例。

## 2. 四个不可违反的横切约束

### C1 — API-only 黑盒合同

承重方法只能使用推理 API 的输入和可见输出。不得要求模型权重、梯度、隐藏状态、attention、保证
logprobs、内部 reward head 或解码器改写。Open-weight 模型可以作为复现实验载体，但方法必须通过服务
API 调用，并能不改算法地迁移到 proprietary API。外部 DSP、检索、工具、memory store 和确定性检查器
可以使用；其产生的信息、成本和版本必须显式记录。

### C2 — 可靠能力提升合同

目标不是判断“有没有一点提升空间”，而是最大化稳定兑现的任务能力：

```text
maximize   RobustUtility(controller output)
subject to API-only legality, bounded cost,
           and preregistered regression / tail-risk limits
```

最低报告项：paired task delta、置信区间、重复运行方差、worst-group 或 CVaR-style tail、
`correct→wrong` / `wrong→correct`、跨声学条件/语言/任务的符号一致性，以及 calls、audio-seconds、
latency、API cost。Evaluator accuracy、headroom、abstention 和 harm 是解释量或约束量，不替代最终任务
效用。绝对正确性不可承诺；“可靠”只在明确分布、误差假设和阈值下陈述。

已日落的 R1 仍保留数据集—方法—基线—指标复现矩阵作为证据包；其基线只由实际消费它们的保留方向
按需复用，不建立独立实验。R2 同样只复用 AudioRAG、Omni-DeepSearch、VoiceAgentRAG 的原始指标，不
新造统一 utility、need score、retrieval contribution 或 cost-quality 总分来挽救方向。

### C3 — system-level ICL 合同

固定候选池的 oracle 只约束从该池中 read-out 的方法。观察变换、prompt topology、检索、工具、外部记忆、
反思轨迹和跨轮 evidence state 会改变后续上下文与候选分布，因此静态 headroom 不得作为开展系统研究的
前置门。Headroom 可以击杀某个已执行的 action menu，不能证明所有未执行 context 都不可达。

### C4 — Lean 与经验验证分工

Lean 用于检查“假设是否足以推出结论”和“论文算法是否真对应被证明的算子”；实验用于判断假设在真实
模型、reward 和数据上是否成立。每个承重数学主张都必须登记：论文主张、显式假设、黑盒化算子、Lean
状态、实现一致性、经验假设和允许结论。`sorry = 0` 不等于真实系统已收敛，条件定理不等于 evaluator
误差界已成立。

## 3. 五个维度的最终边界

| 维度 | 系统对象 | 拥有的决策权 | 不拥有 |
|---|---|---|---|
| D1 多模态知识 | 当前实例的示例、观察、证据、检索和供给拓扑 | 看什么、以何种形式/顺序/粒度组合 demonstration 与 query representation | 跨实例持久化、工具实现、整体编排 |
| D2 多模态记忆 | 跨轮/跨实例的外部状态与经验库 | 写入、键控、检索、衰减、驱逐、迁移资格 | 当前供给动作、工具执行、全局策略更新 |
| D3 多模态技能 | 可复用的工具、程序和动作模板 | 选择、组合、信用分配、修复、归纳、退役 | 证据供应总预算、系统作答权 |
| D4 多模态智能体系统 | evidence state、组件拓扑和决策权分配 | 谁规划、谁执行、谁作答、何时保留 incumbent | 跨时间改进规律 |
| D5 智能体系统进化 | 实例内/跨实例策略动力学 | reward 如何改变下一动作，经验如何改变未来控制 | 模型参数训练；TFRL 是路线而非维度本体 |

## 4. 原九条候选方向及当前处置

### R1 — 冻结 Speech/Omni 模型的语音/音频上下文学习方法复现与比较（已日落）

**问题。** 在项目选定的冻结、API-only Qwen3-Omni-30B 核心上，参考论文已经提出的 speech/audio
in-context learning 和 query-side context 方法，能否在其既有数据集、split、baseline 与 metric 口径下得到
可复现、可比较且边界清楚的结果？R1 不把“audio few-shot”“speech demo retrieval”“audio tool use”或
“modality topology”重新包装为创新；它只归纳并复现这些已有方法在通用 ASR 和 AU/AR 上何时有益、何时
退化、哪些协议无法闭合。

**研究内容。** 主线一复用 TICL 的通用 ASR 协议，比较 direct/zero-shot、uniform random、Whisper、
HuBERT、ECAPA-TDNN、WavLM retrieval 与 TICL text-embedding KNN。主线二复用 MetaSICL/MiMo-Audio
的 MMAU/MMAR direct 与 Vanilla SICL；few-shot demonstration pool 在论文/官方代码可精确还原前保持
关闭。TICL+、ByCS、Audio Flamingo、TwS 和 CoM 仅按各自原论文任务作独立复现或边界证据，不拼接为
新的 selector、controller 或多方法菜单。

**数据与指标。** 通用 ASR 主载体为 TICL 使用的 Common Voice 15.0、GLOBE-V2 和 L2-ARCTIC；
demonstrations 复用论文的 validated 或 train+validation pool，评估复用 official test。AU/AR 使用论文中的
MMAU、MMAR public test 与官方脚本。ASR 使用 WER，zh/ja/th 使用 CER；AU/AR 使用 accuracy，并保留
论文已有 subgroup/category 报告。未正式发布的 MELD-Hard1k 不重建；不自建数据，不新造 utility、
headroom、recovery ratio 或跨任务总分。

**参考边界。** Audio Flamingo 是经过 ICL/RAG 专门训练的模型；MiMo 的 few-shot 主证据来自 Base；
MetaSICL1/2/3 和 CoM 的 PRD 分析路径包含参数训练；ByCS 依赖 Whisper inverse inference；TwS/CoM 的
部分实现或作者数据未发布。这些结果只定义可复现基线和限制，不能直接当作 Qwen3 核心的已知结果。

**最终判断。** Owner 已于 2026-07-29 确认 `NO_GO_AS_STANDALONE_DIRECTION__SUNSET_BEFORE_STAGE2`
（理由：R1 不具备独立研究方向潜力，只提出基础要探索的内容，不构成可对比的研究问题）。上述文献、数据、
基线和指标作为归纳记录保留；TICL/TICL+/ByCS 与 TwS/CoM 只在 R3–R8 实际消费相应 action 时按原论文
协议复现。R1 不建立独立实验包，不进入 Stage-2B，也不得成为其他方向的前置条件。详细分析见 workbench
R1 报告。

### R2 — 音频感知证据获取（Stage-1C 通过；Stage-2A 执行合同待签）

**审计对象。** AudioRAG 已发布 500 题 benchmark 和 text-controller + audio-tool + live-web pipeline；
Omni-DeepSearch 已发布 640 题 audio-only-start deep-search benchmark、固定搜索预算消融和 accuracy 体系；
VoiceAgentRAG 已发布跨轮 prefetch/cache 系统和 latency/hit-rate 体系。三者分别占据 benchmark、固定搜索
pipeline 和 anticipatory supply，但不构成一套可直接合并的 R2 实验。

**关键不匹配。** 原 R2 的 H1 要区分 `waveform-sufficient / external-required`，而 AudioRAG 与
Omni-DeepSearch 在数据构造时都过滤掉不需要检索的题；官方数据没有 negative class。原 H2 的 reward/VoI
query-hop-stop 没有直接参考方法，属于 R6 的 trajectory controller；two-ledger 属于 R5；条件回归和预算停止
属于 R8。自行补负例、冻结 web corpus、发明归因指标或统一 utility 都违反当前数据/指标边界。

**处置状态（2026-08-02 v20 阶段对齐复核）。** `PASS_STAGE1C_FORMAL_OPENING`：round-21 的十项
报告级签字门已经关闭，问题选择与 Stage-2A 交接成立。创新性和最终方法学均未裁决，必须在
reproduction-first Stage-2A 中收敛并于 Stage-2B 验证。主研究问题按音频特有机制重写（听错实体→
高相关错误证据；感知 vs 知识不确定性；预算
在 re-resolve-audio 与 search-external 两信息源间分配）。红线：模型参数不可修改、不得新增一个
模型（续78 细化：只禁为任务新训练模型与新增 LLM 代答；embedding 检索器、frozen judge 属工具级
冻结组件可用，最终作答权在冻结核）；检索 trace-logging 放行（pin 服务/日期/参数、逐次落盘返回
hash、共享查询跨臂复用）。
早期证据事实（占据、negative class 缺失、边界约束）独立保留；正式开题底稿=proposals/
2026-07-29-r2-coreview-draft.md（v20）；正式评审与许可见 audit round-22。

### R3 — 声学条件键控的持久多模态记忆

**问题。** 外部 memory 能否不改权重地保存对未来实例有用的经验，并避免仅按文本语义检索导致声学
regime 错配、负迁移和库污染。

**机制。** 使用 `task key × acoustic-condition key`；条目包含 evidence、action、outcome、reward、
provenance、反例和适用条件。完整生命周期是 write gate → read gate → contribution attribution →
decay/evict → transfer qualification。声学 key 必须来自部署可测特征并先验证其确实区分失败机理。

**验证。** 比较 no-memory、semantic-only、task-keyed、acoustic-keyed、random-memory 和 oracle-memory；
报告 average-vs-final learning curve、每条贡献、负迁移率、库规模/成本与 held-out acoustic strata。D2.5
投毒与 D2.6 跨核迁移是压力测试和资格门，不独立写成安全论文。

**Lean 义务。** 形式化 write/read/evict 不变量、有限容量和 provenance preservation；跨实例效用提升
取决于 exchangeability/condition relevance 等经验假设，不由 memory schema 自动推出。

**击杀/重路由。** 若 acoustic key 不比随机或 task-only key 更能分离失败，降级为 task-only memory；若
memory 平均贡献非正，关闭跨实例写入但可保留 session evidence state。

### R4 — 运行时多模态技能的信用、组合与生命周期

**问题。** 在固定工具库和冻结 core 下，如何识别哪个技能对答案产生了可归因的正贡献，并据此选择、
组合、修复、归纳和退役技能，而不是依赖手工 reliability tier 或自由文本路由。

**机制。** 把 tool/skill 定义成可执行 action contract，记录 pre/post answer、evidence diff、execution
result、cost 和 downstream utility。信用来自 counterfactual/no-tool 或 matched alternative；程序化技能先
执行后验证，多个工具贡献使用显式 credit assignment。新技能只能由可复现轨迹归纳，持续负贡献触发退役。

**验证。** 同工具库比较 hand router、random matched-call、all-tools、best fixed subset、reward-guided
selection 与 compositional controller；报告 tool relevance、执行成功、任务 delta、correct→wrong、cost 和
跨任务复用。D3.6 headroom 是离线诊断，不是研究起点。

**Lean 义务。** 对确定性 tool contract 证明前置条件、postcondition 和失败传播；对多工具 credit 只证明
选定估计量下的代数性质，不把 proxy credit 写成真实因果贡献。

**击杀/重路由。** 若 reward-guided policy 不优于 best fixed subset，关闭动态工具选择；仍可保留程序化
技能执行/验证作为 R5 的固定组件。

### R5 — Incumbent-preserving 的证据状态智能体架构

**问题。** 如何把 D1-D3 组成一个可审计系统，使 planner、executor、evaluator 和 frozen omni core 的
决策权清晰，同时防止文本 orchestrator 覆盖原始音频判断或固定 wrapper 系统性伤害 direct answer。

**机制。** 一等 `evidence_state` 保存原音锚点、派生 artifact、工具输出、矛盾、成本和 provenance；
direct answer 是 incumbent。Planner 只提出 action，工具只产生 evidence，最终答案由 frozen omni core 在
原音 + 被接纳 evidence 上生成；controller 在 `{incumbent, revised}` 间持有显式选择权。格式检查与内容
判断分离。

**验证。** 同一 core、prompt hygiene 和预算下比较 direct、structured prompt、fixed wrapper、
hand-arbitrated system、reward-arbitrated system；按 control-plane depth 和 acoustic/task bucket 报告结果。
D4.5 注入/溯源仅作为 evidence-state invariant；D4.7 full-duplex 仅作后期 carrier。

**Lean 义务。** 证明状态转移类型正确、baseline candidate 始终可恢复、预算有限时终止、gold 文件不可
进入 runtime state。对“架构提高能力”不作形式证明。

**击杀/重路由。** 若 reward-arbitrated system 在等供给下不能超过 structured prompt 与 best fixed
wrapper，关闭动态架构主张并定位失败在 supply、skill、reward 或 orchestration 哪一层。

### R6 — 实例内 reward-guided context 与轨迹控制

**问题。** Reward 能否在单个实例内决定下一步 `keep / branch-context / acquire / tool / repair / stop`，
而不是只对终局候选 rerank。

**机制。** 状态为当前 context、evidence、candidate、reward estimates、budget 和 action history；action
来自保留方向及已日落证据包中的 published action；每次动作后更新 advantage 并决定继续或保留 incumbent。Reward 可由 exact task-visible
checks、counts-only consensus、semantic equivalence、cross-evidence corroboration 和 frozen judge 组合，
不得使用 test gold、hidden state 或 logprob。

**验证。** 先做短 horizon：direct incumbent + 2-4 种 context action + hard budget。比较 greedy/fixed、
random、majority/MBR、terminal-only rerank、step-wise reward controller 和 offline oracle policy；报告每种
decision right 的净贡献与错误传播。

**Lean 义务。** 证明有限预算终止、incumbent preservation，以及 reward-error 假设下的 margin rule；
现有 `Iterate` 的单调/有界结论依赖每步真实增益假设，不能拿来证明实际 controller 收敛。

**击杀/重路由。** 若 step-wise reward 不优于 terminal-only 或 best fixed trajectory，R6 降级为静态
selection component；保留失败轨迹用于 R7 学习是否能改进信号。

### R7 — 跨实例经验驱动的无权重系统进化

**问题。** 系统能否在模型参数完全不变时，通过外部经验记忆、统计更新和 action-level advantage，随
部署实例增加而提高未来决策质量。

**机制。** 每个实例产生 `(condition, state, action, evidence, outcome, advantage)`；D2 决定存储与检索，
D3 管理技能，D5 更新外部 policy statistics、threshold 或 preference，不反向传播进模型。必须保留
time-order split，防止未来标签或 test gold 进入 memory。

**验证。** 报告 instance 1→N 的 prequential curve、average/final utility、forgetting、跨 condition transfer、
memory growth 与 cost；比较 frozen controller、recency heuristic、bandit-style update、advantage memory 和
offline oracle update。提升必须出现在未来实例而非仅重新解释过去。

**Lean 义务。** 审计更新规则的 boundedness、credit decomposition 和在显式 stationarity/coverage 假设下
的 regret 性质；这些假设必须单列，不能由 JitRL/MemRL 类论文效果直接迁移到 speech。

**击杀/重路由。** 若 learning curve 不随实例改善或条件漂移导致净负迁移，冻结跨实例更新，仅保留
per-session memory；不得用 retrospective best checkpoint 掩盖在线失败。

### R8 — 条件自适应的可靠能力控制

**问题。** 如何让保留机制与按需外部 action 的能力增益在声学条件、任务和模型版本变化时保持可重复、
低尾部回归和可诊断，
而不是把系统改写成“多数时候 abstain”。

**机制。** 对 reward error、agreement、margin、cost 和 acoustic condition 建模；阈值控制是否替换
incumbent、是否继续花预算以及使用哪个 action family。Headroom、E1 admissibility、reward hacking、
abstention 和 rollback 全部是这一能力目标的 diagnostics/guards，不是独立研究对象。

**验证。** 预注册最低实际增益和 regression tolerance；按 clean/noise/reverb/language/task/core version
报告 lower confidence bound、worst-group、tail、coverage-quality curve 和 cost-quality frontier。压力测试
增加 selection pressure、judge swap、prompt permutation 和 held-out acoustic strata，但最终结论仍以任务
能力为中心。

**Lean 义务。** `RuntimeReliability.true_nonregression_of_estimated_margin`：若部署 reward 对真实 utility
的一致误差 `≤ ε`，estimated margin `≥ 2ε` 蕴含真实非回归；严格大于蕴含严格提升。Lean 只证明
该蕴含，`ε` 是否成立必须由独立 calibration/stress test 支持。

**击杀/重路由。** 若可获得的 proxy 无法给出跨 condition 稳定的误差/排序证据，则不得宣称形式保证；
改为经验型 robust policy，并如实报告其作用域。低 coverage 只说明 guard 不实用，不否定其他能力机制。

### R9 — 五维集成的可靠能力激活系统

**问题。** 当 D1-D5 作为一个 control plane 组合时，系统是否在同一 frozen API core 上获得超过各单组件、
structured prompt 和 fixed wrapper 的稳定任务收益；收益来自哪里，组件之间是否相互抵消。

**机制。** 统一 state/action/reward/cost/provenance contract：D1 供应当前证据，D2 保存经验，D3 提供动作，
D4 分配决策权，D5 在实例内和跨实例更新控制。集成顺序固定为 `R5 baseline architecture → R6 short
horizon → R8 reliability → R4 expansion → R3/R7 evolution → optional external-knowledge carrier`，避免一开始构建不可归因
的大系统。

**验证。** 使用 factorial/leave-one-component-out、同供给同预算控制、prequential evaluation 和
cross-condition holdout；至少同时报告 direct、strong structured prompt、best single component、best fixed
composition、full adaptive system。Full-duplex/interactive 只有在 task success 与 latency/VAD/ASR 因素可
分离时才作为 speech-native external validation。

**Lean 义务。** 建立 executable action/state semantics 与 Lean operator 的逐例 conformance test；在关闭
该桥前不得写“Lean 已证明实际系统收敛”。组合定理只在各组件假设和接口不变量同时成立时使用。

**击杀/重路由。** 若 full system 不优于 best component 或 fixed composition，按 factorial 结果拆回贡献
为正的方向；集成失败不抹去单组件结果，也不得用更多调用掩盖。

## 5. 方向局部流水线与优先级

候选编号不定义工程顺序或目录。每个独立研究对象使用自己的流水线：
`充分调研 → owner 裁决 → 语义名称与执行合同 → 独立 study repo → 工程 → 验证`。一个 study 进入工程后，
下一个候选可开始调研；只有会推翻该 study 核心机制、合法性或主 baseline 的新证据才重新打开其门禁。

| 当前顺序 | 研究对象 | 处置 |
|---|---|---|
| 1 | **音频感知的证据获取**（来源候选 R2） | Stage-1C 与正式开题已通过；关闭 D1–D4、冻结执行合同并请求 owner GO 后进入独立工程仓 |
| 2 | 下一个候选研究对象（先从 R3 provenance 开始复核） | 在首个 study 工程期间并行调研；尚不建仓 |
| later | skills、evidence state、instance/cross-instance control、reliability、integration 等候选 | 分别判断独立/合并/日落；不构成首个 study 的全局前置 |

R5+R6+R8 的组合纵切片降回尚待 owner 验证的候选研究对象，不再是所有 Stage-2 的统一入口。R9 只有在
集成本身形成独立问题并获 GO 时才建立语义 study repo。

## 6. 首个计划 study 的 Stage-2A 建仓合同（尚未生效）

**工作语义名称：** `audio-aware evidence acquisition`；GitHub slug 候选为
`audio-aware-evidence-acquisition`，最终 URL 与执行字段在 owner execution contract 中冻结。
来源候选 R2 只保留在 Wiki provenance，未来仓名不得携带 `r2`。

**研究机制：** 在冻结 API-only speech/omni 核上，控制预算在 `re-resolve audio` 与
`search external evidence` 两类信息动作之间分配，针对“听错实体导致高相关但错误证据”的音频特有失败。

**已关闭：** v20 Stage-1C 报告级签字门与正式开题许可；Earnings21、Earnings22、ConEC D0 物化。

**建仓前仍必须关闭：**

- 模型无关的 D1–D4 对齐、信息边界/泄漏、评分与十样本 trace 检查；
- exact task、正式数据版本、incumbent baseline、官方指标与 exposure；
- Qwen3-Omni-30B service/model revision、prompt/decoding 和黑盒边界；
- trace pinning（服务/日期/参数/返回 hash/跨臂共享查询）、预算、停止与 abort/reroute；
- Wiki `wiki/experiments/<semantic-slug>/README.md`、GitHub URL、artifact/MLflow namespace；
- 无参数修改、无 task-trained model、无新增 answering LLM、test gold 不进入 controller。

上述关闭后请求 `OWNER_GO_AND_EXECUTION_CONTRACT`，再创建独立 GitHub 仓并登记
`studies/registry.json`。本定稿不授权模型/API 调用、metrics、下载、复现、prototype、远程建仓、push
或 Wiki publication。

## 7. Lean 现有结论的允许用法

| 模块 | 可用结论 | 不得推出 |
|---|---|---|
| `InfoBoundary` | fixed candidate pool 的 read-out 不能超出该池 | ICL、不同 context 或 agent system 无提升空间 |
| `AgenticElements` | 若显式假定所有 context 均不可达，则同核输出不可达 | finite oracle miss 证明 all-contexts gap；「外部新信息是唯一杠杆」——两者均禁止推出 |
| `Reachability` | 在乘法 reweighting 与 bounded ratio 模型下的 mode-shift 条件 | 任意 prompt/ICL 都服从该模型或实际不可达 |
| `Realization` | uniform reward error `τ` 下 argmax 与 oracle gap `≤ 2τ` | 真实 judge 已满足 uniform error |
| `Iterate` | 显式逐步真实增益和有界假设下的终止/收敛性质 | 实际 reward-guided loop 单调或收敛 |
| `OptSpace` | 指定概率/奖励/可分结构下的 tilting 代数性质 | 多 agent/多组件自动产生新增 headroom |
| `RuntimeReliability` | `2ε` estimated margin 下相对 incumbent 的条件非回归/提升 | 经验误差界、跨分布保证或实际系统有效性 |

当前 claim ledger 对 “Lean proves the implemented selector converges” 的判定仍为不成立；新增条件定理不
改变该结论。实现一致性必须由后续 conformance test 单独关闭。

## 8. Provenance、目的链与失效条件

**结论。** 九条方向是五维组合的现行有效研究 portfolio；C1 evaluator/reward reliability 降为所有
方向共享的 measurement/reliability component，不再是 primary problem。

**推理摘要。** 2026-07-26/27 的 35 篇 speech/omni 全文级条目、73 篇 text/vision donor 和 T1/T2/T3
表支持了 mechanism、limitation、asset 与实验设计；owner 的五条统一约束改变的是综合层和优先级，不
撤销其论文事实层。32 个子方向因此保留为设计菜单，合并成 9 条以能力为中心、可归因的主线。

**目的链。** 北极星是冻结黑盒 omni 模型的能力激活；五维提供 context/state/action/dynamics；可靠性和
Lean 防止把偶然提升或条件命题写成强结论；Stage-2A 最小纵向链用最低复杂度检验这一对象。

**Provenance。** Evidence workbench：`wiki/survey/workbench/stage1c-portfolio/`；Stage-1B v5 固定证据
release：`38fb9435d0c35e226ad62b16015a6dbee054e6c2`；旧 C1 common-rubric 仅作组件证据。H5 仍为
`WITHHOLD_NON_LOAD_BEARING`，donor 只借方法/协议，不承载跨模态效果结论。

**失效条件。** Owner 改变 API-only、能力优先、system-level ICL、Lean 分工或非安全主线约束；H5 获得
新签署；或 Stage-2 证据显示方向被同合同 prior 支配、机制无法归因或可靠性目标不可实现时，原位
supersede。本文件不发布 novelty/first-ever 判断。
