---
artifact_id: "SF-STAGE1C-CAPABILITY-PORTFOLIO-V1"
role: "CURRENT effective research-direction contract"
authority: "owner direction 2026-07-27; same-day remediation ruling applies"
stage: "STAGE_1C_REMEDIATION"
endpoint: "STAGE1C_PARTIAL_R1_CORRECTION_PENDING_R2R9_REFINEMENT_PENDING"
execution_authority: "STAGE2A_WITHHELD"
---

# 五维研究方向定稿：API-only 冻结多模态模型的可靠能力激活

> **2026-07-27 owner 整改裁决（先于本文其余内容生效）。** 方向内容成立，证据绑定层未达验收：R1 的
> 参考文献、引用方法与锁定实验基线需重推导（step 2），R2–R9 随后提升到修正后 R1 标准（step 3）。
> **裁决 A**：项目核心为 Qwen3-Omni-30B（本地 llama.cpp serving lane 为可复现载体，精确 revision 在
> Stage‑2A 授权包冻结）；本文 §4-R1 验证与 §6 中"首选 Qwen2.5-Omni-7B"口径已被取代。**裁决 B**：ASR
> 主线为通用 ASR，MyST/RSR 儿童 ASR 失去主线地位。上述两节的载体文字在 step-2 重写落地前视为过期。

## 1. 唯一研究问题

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

R1 的阶段 A 是能力上界与机制识别，例外地不以 latency/cost/budget 为研究变量或通过门；有限菜单保证
实验可终止，资源只做完整记账。阶段 B 若要把收益归因于“选择”而非“多执行”，可以增加 matched-compute
对照，但成本压缩仍属于后续工作。

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

## 4. 九条定稿研究方向

### R1 — 多源上下文能力上界与自适应构造

**问题。** 对冻结 Speech/Omni API，把带标签 audio demonstrations 与当前 query 的 raw audio、分段/窗口、
ASR view、raw+ASR 和确定性重表达统一成 context configuration。先问这些来源在给定可执行菜单内能产生
多大经验能力上界、是互补/替代还是干扰、最佳配置为何按样本变化；再问无 test gold、无参数更新的黑盒
智能体能否逐样本构造 context 并恢复这种选择机会。宽泛的 audio few-shot ICL 与 demo retrieval 已被
Audio Flamingo、MiMo-Audio、MetaSICL、TICL/TICL+ 和 ByCS 占据，不再作为创新表述。

**两阶段机制。** 阶段 A 枚举预注册有限菜单
`(demo subset, query views, order/topology, fixed template)`，分别计算 direct、开发集 best fixed、test-only
offline menu oracle、context headroom、demo×query-view 交互和样本异质性。阶段 B 只在 headroom 与
best-fixed-to-oracle selection opportunity 都成立后，使用输入特征、retrieval score、输出一致性和黑盒反馈
构造 context；不训练 core/controller，不使用 gold-derived runtime signal。

**验证。** 双主线同等承重：ASR 用 MyST+RSR，AU/AR 用 MMAU Test-mini+MMAR，MELD/MELD-Hard1k 只做
clean/perturbed 机制压力。示例只能来自 official train/dev 或审计后的独立池；MMAU/MMAR 在独立 demo pool
闭合前只运行 query-view arm，禁止 test leave-one-out。主模型 Qwen2.5-Omni-7B 跑完整菜单，MiMo-Audio
7B Instruct 复核 direct、best fixed、menu oracle 与 selector；Base/Instruct 文献数字不得混写。

**Lean 义务。** `InfoBoundary` 的 fixed-pool read-out ceiling 不覆盖改变 context 后重新生成。Lean 只审计
有限菜单定义、gold/runtime 隔离、best-fixed/oracle 定义域和 recovery ratio 非零分母；不证明经验
headroom、交互、可预测异质性或 selector 有效。

**击杀/重路由。** 若菜单 headroom 近零，停止自适应阶段但不外推 all-contexts impossibility；若有
headroom 而 best fixed 已逼近 oracle，保留固定 context 机制；若 selection opportunity 存在但 selector 不
超过 best fixed，报告不可恢复的选择机会。只在 synthetic/model/task 子域成立时必须收缩作用域。

### R2 — 音频原生外部知识获取与检索调度

**问题。** 当答案确实不在 waveform 内时，系统如何决定是否检索、查询什么、购买多少 hop、何时停止，
并避免 live-search 漂移把能力提升与信息变化混在一起。

**机制。** 将 endogenous audio evidence 与 exogenous corpus/web evidence 分开计价；query、retrieval、
admission、cross-modal verification 和 answer regeneration 都是显式 action。 anticipatory/prefetch 仅在真实
延迟可隐藏且命中上下文能改善任务答案的场景启用。

**验证。** 使用冻结检索快照、可审计 query/tool trace 和同 retrieval budget 基线；分别报告 audio-grounding、
retrieval、reasoning 与 stopping 贡献。AudioRAG/Omni-DeepSearch 类工作提供 carrier 和 failure taxonomy，
不提供跨版本可复现的 live-web 绝对数。

**Lean 义务。** 区分“改变 context”与“加入新信息”；形式证明只覆盖预算、终止和信息边界。任何关于
retrieval 能跨越知识缺口的效果陈述都必须由实验支持。

**击杀/重路由。** 若任务可由 waveform/direct context 完成，或 pinned retrieval 在等成本下不改善效用，
则该 carrier 移出 R2；R2 本身只保留真正需要外部事实的任务。

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
来自 R1-R4；每次动作后更新 advantage 并决定继续或保留 incumbent。Reward 可由 exact task-visible
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

**问题。** 如何让 R1-R7 的能力增益在声学条件、任务和模型版本变化时保持可重复、低尾部回归和可诊断，
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
horizon → R8 reliability → R1/R3/R4 expansion → R7 evolution → optional R2`，避免一开始构建不可归因
的大系统。

**验证。** 使用 factorial/leave-one-component-out、同供给同预算控制、prequential evaluation 和
cross-condition holdout；至少同时报告 direct、strong structured prompt、best single component、best fixed
composition、full adaptive system。Full-duplex/interactive 只有在 task success 与 latency/VAD/ASR 因素可
分离时才作为 speech-native external validation。

**Lean 义务。** 建立 executable action/state semantics 与 Lean operator 的逐例 conformance test；在关闭
该桥前不得写“Lean 已证明实际系统收敛”。组合定理只在各组件假设和接口不变量同时成立时使用。

**击杀/重路由。** 若 full system 不优于 best component 或 fixed composition，按 factorial 结果拆回贡献
为正的方向；集成失败不抹去单组件结果，也不得用更多调用掩盖。

## 5. 优先级与依赖

| 批次 | 方向 | 目的 |
|---|---|---|
| Stage-2A vertical slice | R5 + R6 + R8 | 先证明 API-only evidence-state controller 能可靠改变下一动作并提高任务效用 |
| Stage-2B mechanism expansion | R1 + R4 | 测量多源 context 上界/交互后，再检验自适应构造与技能信用 |
| Stage-2C persistent evolution | R3 + R7 | 检验外部记忆和跨实例改进是否成立 |
| Stage-2D knowledge extension | R2 | 仅在任务确需外部事实时接入检索 |
| Stage-2E integration | R9 | 端到端组合与 speech-native 外部验证 |

## 6. 第一份 Stage-2A 合同（方向冻结，执行仍待授权）

**目标。** 实现并复现一个 `incumbent-preserving reward-guided context controller`，只覆盖 R5/R6/R8
的最小纵向链。

- **Core contract：** 单一 frozen speech/omni core，仅经 inference API；首选公开可复现、论文基线充分的
  Qwen2.5-Omni-7B serving lane。具体 model/service revision、hash、prompt 和 decoding 在授权包冻结。
- **Carrier：** MMAU-mini + MMAR；先解决 CURRENT T2 对 local status 的不一致，再冻结 exact revision、
  split、hash 和 contamination/exposure。不得因“已 pin”散文直接假定资产可运行。
- **Action menu：** `keep incumbent`、structured re-prompt、same-observation resample、一个
  cross-observation branch、一次 bounded repair、stop。暂不加入 live retrieval、跨实例 memory 或
  full-duplex。
- **Runtime signals：** exact answer-format/option checks、counts-only consensus、hypothesis-vs-hypothesis
  semantic equivalence、可选 frozen cross-family judge；test gold 永不进入 controller。
- **Baselines：** direct readout、structured prompt、random matched-cost、majority/MBR、best fixed action、
  full fixed chain、terminal-only rerank；offline oracle 只用于解释 action-menu recoverability。
- **Primary result：** task accuracy/utility 的 paired delta 与下置信界；同时报告 seed variance、
  worst-group、correct→wrong、wrong→correct、calls/latency/cost。Headroom 不作开门门槛。
- **Lean gate：** runtime state/action 定义、bounded termination、incumbent recoverability、gold boundary、
  `2ε` margin theorem均编译；实现—定理 conformance 尚未关闭时只可称 formal model。
- **Abort/reroute：** API contract 需要内部量；数据/许可证/版本不闭合；controller 使用 gold；equal-cost
  下不超过 structured prompt/best fixed；可靠性阈值覆盖率近零；效应小于预注册 SESOI。

建议授权 token：`AUTHORIZE_STAGE2A_CAPABILITY_CONTROL_VERTICAL_SLICE`。本定稿本身不授权模型/API
调用、metrics、下载、复现、prototype、技术 novelty verdict、push 或 wiki publication。

## 7. Lean 现有结论的允许用法

| 模块 | 可用结论 | 不得推出 |
|---|---|---|
| `InfoBoundary` | fixed candidate pool 的 read-out 不能超出该池 | ICL、不同 context 或 agent system 无提升空间 |
| `AgenticElements` | 若显式假定所有 context 均不可达，则同核输出不可达 | finite oracle miss 证明 all-contexts gap；外部新信息是唯一杠杆 |
| `Reachability` | 在乘法 reweighting 与 bounded ratio 模型下的 mode-shift 条件 | 任意 prompt/ICL 都服从该模型或实际不可达 |
| `Realization` | uniform reward error `τ` 下 argmax 与 oracle gap `≤ 2τ` | 真实 judge 已满足 uniform error |
| `Iterate` | 显式逐步真实增益和有界假设下的终止/收敛性质 | 实际 reward-guided loop 单调或收敛 |
| `OptSpace` | 指定概率/奖励/可分结构下的 tilting 代数性质 | 多 agent/多组件自动产生新增 headroom |
| `RuntimeReliability` | `2ε` estimated margin 下相对 incumbent 的条件非回归/提升 | 经验误差界、跨分布保证或实际系统有效性 |

当前 claim ledger 对 “Lean proves the implemented selector converges” 的判定仍为不成立；新增条件定理不
改变该结论。实现一致性必须由后续 conformance test 单独关闭。

## 8. Provenance、目的链与失效条件

**结论。** 九条方向是五维组合的当前唯一有效研究 portfolio；C1 evaluator/reward reliability 降为所有
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
