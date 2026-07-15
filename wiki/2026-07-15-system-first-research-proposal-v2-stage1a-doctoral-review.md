---
title: "System-first research proposal v2：Stage-1A 博导式严格外审"
date: 2026-07-15
review_target: "wiki/2026-07-15-system-first-research-proposal-v2.md"
review_target_commit: "cf54f1be921e9c26219121398461ceaf727295b7"
review_target_blob: "20e5bd5537df55e61e04365e72a8324e1b77605b"
stage_lens: "Stage-1A（问题界定、广泛 survey、候选问题与纸面原型空间；不以实验确证为任务）"
verdict: "有条件批准继续 Gate S1 检索协议实例化；首条真实查询仍须协议单独签署"
stage1a_close: "未申请，不评价"
stage1b: "未申请、未授权，不作 GO/NO-GO"
integrity_finding: "未发现本轮 v2 构成 fabrication、falsification 或 plagiarism 的证据；发现若干知识检索、过度完备措辞和可回放治理缺口"
mutation_scope: "仅新增本独立审查报告；未修改被审提案、代码、配置或团队状态文件"
---

# System-first research proposal v2：Stage-1A 博导式严格外审

## 0. 结论先行

我的裁决是：**有条件批准团队继续完成 Gate S1 exact-query protocol 的实例化，但不批准执行首条真实查询，更不批准 Stage-1A close 或任何 Stage-1B 实验。**

这里的“有条件”不是要求团队再写一轮宏大 proposal，也不是要求现在设预算 cap、冻结最终指标、完成 agent 平台或跑实验。条件全部落在 Stage-1A 当前真正承重的对象上：**检索协议能否覆盖强近邻、文献分类是否不被标题误导、知识记录是否可追溯、候选问题空间是否保持开放。**

v2 相比 v1 的方向性纠偏总体正确：

- 接受“当前不冻结预算/停止机制”的阶段校准，正确；
- 把五份合同降为可被 survey 修订的暂定分类，正确；
- 把 kill 表降为未来 Stage-1B 探针设计候选，正确；
- 明确零新实验、零真实 backend、零数据读取，正确；
- 承认当前工程只是 Hydra stub 与定制脚本，而不是伪称已有配置化实验基座，正确；
- 把内部 `CONVERGED` 限定为“环内判定”，正确；
- 将唯一申请事项收窄为检索协议实例化，符合 Stage-1A。

但 v2 仍有一个**实质性文献覆盖问题**和三个**重要治理问题**：

1. §4 把当前列举称作 mandatory seeds“全集”，但 2026-07-13 提交的 **Omni-Decision** 已经构成高度相邻的 system-level 威胁；本次外部反扫还发现若干未进入 v2 的 agent harness、verification、memory/skill 与 feedback-compute 工作。协议尚未执行时，不允许使用“全集”制造虚假完备感。
2. `Training-Free GRPO`、`IRO` 等标题容易诱发范围误判。冻结 base model 不等于 TF-Strict；外部 token prior、轻量 value function 或 verifier 只要经过训练，仍须作为训练型边界对照编码。
3. v2 大量“见 v1 §N”，却没有在正文中钉死 v1 的 commit/blob。v1 若继续被修改，v2 的实质内容会无声漂移。
4. 内部敌意评审归档比上一轮有进步，但目前更接近“评审结果汇总”，还不是能独立复放的完整 agent-review record：缺 prompt、运行/代理标识、输入快照、工具调用与输出哈希。

因此，本轮不要求 proposal v3。团队应停止继续堆叠“提案—回复—再提案”的元流程，直接把下面要求落实到 **Gate S1 检索协议草案**，再送签首条查询。

## 1. v2 对上一轮意见的响应是否正确

| 事项 | 评审判断 | 严格说明 |
|---|---|---|
| Stage-1A 身份 | **正确** | v2 明确本件只申请协议实例化，不申请 close/1B；没有把 proposal 当论文终稿审查。 |
| 不提前设预算 cap | **正确** | 当前目标是打开方法与问题空间。记录资源轴是必要的，冻结 cap 不是当前 gate。 |
| 暂定 taxonomy | **正确** | `PROVISIONAL_STAGE1A_TAXONOMY` 的作用是帮助检索与编码，允许 survey 反过来改写类别。 |
| 最近邻勘误 | **大体正确但未闭合** | Reflexion/LATS/Voyager/LLM-as-Verifier 的过强 delta 已降级；五条自库近邻已补回。但“种子全集”仍被新近邻直接反证。 |
| AWM/ExpeL 来源纠正 | **正确** | 团队承认它们并非 reviewer 净新贡献，且承认广义自库已有踪迹，纠正了来源归属。 |
| 工程边界 | **正确** | 一页 ADR、接口 schema、开源复用与最小自研的纸面对比，符合 Stage-1A；真实 adapter 留给另行授权的 1B。 |
| Stage-1B 蓝图 | **可保留** | 已明确无现时效力与 owner 签批要求，未构成偷跑。 |
| 内部敌意评审 | **部分正确** | “环内收敛”措辞已校准；但归档仍不足以支持第三方逐步复放。 |
| 科研诚信口径 | **正确** | v2 没有用 preliminary seed table 宣称 novelty，也没有把内部审查当外部通过。 |

最重要的评价是：**团队现在终于把“严格”放回了 Stage-1A 应该严格的地方——检索、分类、证据定位和知识继承——而不是提前把 Stage-2 的实验纪律强塞进来。** 这是实质进步。

## 2. 引用与机制叙述审查

### 2.1 已修正部分总体可接受

v1 §4 当前的 15 项表已不再把以下差异写成既定事实：

- Reflexion 已明确为不更新权重、可由黑盒 API 实现；
- LATS 已承认是 gradient-free MCTS、LM value 与环境反馈组成的强近邻；
- Voyager 已承认黑盒 GPT-4、零微调和持久技能库直接占据一大片机制空间；
- LLM-as-Verifier 是否只占组件层已标记待全文核验；
- JitRL 的 logit-access 要求被正确识别为与 strict black-box 的接口边界；
- AuTAgent、CoVer 被放在训练型 comparator 一侧，而不是用“冻结主模型”偷换“全系统零训练”。

这种写法达到了 Stage-1A seed table 应有的诚实程度：**它提供搜索锚点和待证伪 delta，但不冒充完成后的 novelty matrix。**

### 2.2 四条新补种子的定位仍需进一步收紧

#### Training-Free Group Relative Policy Optimization（2510.08191）

把它列为“training-free RL/advantage→行为”语义上的强近邻是合理的；把它直接当作 TF-Strict 同类则不合理。论文摘要明确写到：方法在少量 ground-truth data 上进行 multi-epoch learning，迭代蒸馏 experiential knowledge，形成 learned token prior，再在 API 调用时注入。它不更新 base-model parameters，但仍然发生了系统外设学习。[原始论文](https://arxiv.org/abs/2510.08191)

协议必须分别编码：

- base model 是否更新；
- 外部组件是否训练；
- 是否使用 ground-truth；
- 学到的对象是什么；
- 学习发生在 test item 之前、同分布开发集上，还是测试时；
- 测试时是否只是读取已学 token prior。

在全文核验前，它应被描述为“**最直接的术语/机制威胁之一，TF-Strict 归属待核**”，不能被写成严格范围内的现成解法。

#### Inference-Time Reward Hacking（2506.19248）

作为 Goodhart、过优化与停止机制的理论/实证锚是正确的。该工作展示了 BoN/BoP 等 inference-time reward optimization 中真实效用先升后降的结构，并提出 HedgeTune；这正是未来 controller 不可忽略的失败模式。[原始论文](https://arxiv.org/abs/2506.19248)

但它主要研究 output-level inference-time alignment。Stage-1A 应提取其可迁移的 failure mechanism 与 stopping idea，不应自动宣称它已经覆盖 agent-level stateful control。

#### Walking Through Uncertainty（2604.25591）

把它视为 audio-aware uncertainty/selective prediction 的直接工作是合理的；把它视为 system-first agent controller 的直接占据者则过强。摘要的主体是五类 uncertainty estimation 的经验比较，adaptive inference 只是下游探索方向。[原始论文](https://arxiv.org/abs/2604.25591)

建议在矩阵中把“组件/测量直接性”和“系统身份直接性”拆开，避免一个 `DIRECT` 同时承载两种含义。

#### Scaling Auditory Cognition（2503.23395）

它确实直接研究 Audio LLM 的 test-time compute，并比较五种 TTC 方法，应该作为 omni/audio TTC lane 的强种子。[原始论文](https://arxiv.org/abs/2503.23395)

但“最紧 omni 机制占据者”仍是团队自评，不是现阶段事实。全文必须回答其五种 TTC 是否包含 reward→下一步行动、是否有持久状态、是否有工具/环境反馈、是否只是多样采样与聚合。未回答前，只能说“音频域 TTC 强边界”。

### 2.3 中量候选 IRO 的范围必须显式标错位风险

IRO（2506.17828）冻结 base LLM，但每轮会训练一个新的轻量 value function，并在测试时用这些 value functions 引导搜索。它是“frozen core + trained external controller”的典型边界，而非 TF-Strict 实例。[原始论文](https://arxiv.org/abs/2506.17828)

这类论文很重要，原因不是它满足本项目身份，而是它能回答：如果放宽“全系统零训练”，最强上界能做到什么；训练外设究竟贡献了什么；严格零训练要付出什么代价。

## 3. 当前遗漏的相关工作

以下是本次 reviewer delta scan 发现的高优先级遗漏。这个反扫不是 Gate S1 survey 的替代品；恰恰相反，它证明了 v2 在协议执行前使用“种子全集”是不成立的。

### 3.1 必须在协议冻结前加入的 system-level 强威胁

#### Omni-Decision（2607.11433）——当前最严重遗漏

该文 2026-07-13 提交，提出 training-free omni-modal QA evidence-state system：显式维护 confirmed evidence、unresolved conflicts、依赖关系和 open evidence needs；用共享状态驱动 planning、evidence acquisition、validation、repair、stopping/finalization，并通过确定性状态更新整合媒体、网页、计算和验证模块。[原始论文](https://arxiv.org/abs/2607.11433)

它几乎逐项命中当前 proposal 的 system-first 表达：

- training-free；
- omni-modal；
- 外部结构化状态；
- 工具/证据获取；
- 验证与修复；
- 显式停止；
- 可审计轨迹与消融。

它未必占据“reward/advantage 决定下一步动作”的完整主张，但会大幅压缩系统创新的剩余空间。由于提交时间非常新，这一遗漏不能直接定性为选择性引用或学术不端；但是，从现在起若协议仍不把它列为 mandatory seed，就属于不可接受的 Stage-1A 覆盖失误。

#### Affordance Agent Harness（2605.00663）

该工作提出 verification-gated skill orchestration：evidence store、episodic memory、router、verifier、targeted retry、final judge 与 cost control 被整合为闭环 runtime，而且明确强调无标签测试时决策。[原始论文](https://arxiv.org/abs/2605.00663)

虽然领域是视觉/机器人 affordance grounding，但其“外部 harness 如何组织技能、证据、反馈、重试和成本”的机制与当前 system-first controller 高度相邻。它至少应进入 agent-harness lane 的强威胁集合。

#### FineVerify（2606.00660）

FineVerify 把复杂问题拆成可验证子问题，对候选轨迹进行细粒度自验证并聚合选择，在 agentic search 中实现 test-time compute scaling。[原始论文](https://arxiv.org/abs/2606.00660)

它直接压力测试“reward/evaluator→候选选择”的新颖性，也提示团队不能只比较一个整体 scalar verifier；分解后的局部可核查标准可能是更强的 controller 输入。

### 3.2 必须进入资源、外部记忆与技能演化抽取的工作

#### Scaling Laws for Agent Harnesses via Effective Feedback Compute（2605.29682）

该文指出 tokens、tool calls、wall time 和 cost 不能区分有效反馈与冗余/不稳定交互，提出 Effective Feedback Compute 来刻画可用、有效、非冗余且被保留的反馈。[原始论文](https://arxiv.org/abs/2605.29682)

这篇论文的正确用途不是逼 Stage-1A 现在设 cap，而是让 survey 回答：未来“资源/反馈量”应如何被描述，单纯记录四轴 raw compute 是否足够，controller 的提升究竟来自更多调用还是更高质量反馈。

#### Agentic Context Engineering（2510.04618）与 MUSE-Autoskill（2605.27366）

ACE 研究不改模型权重的 context adaptation，并明确处理 iterative rewriting 带来的 context collapse；MUSE-Autoskill 把技能创建、记忆、管理、评价和迭代组织为持久生命周期。[ACE](https://arxiv.org/abs/2510.04618) · [MUSE-Autoskill](https://arxiv.org/abs/2605.27366)

更严厉的问题在于：这两篇并非团队不知道。它们已经出现在仓库历史 survey 和论文引用库中，却没有进入 v2 声称的 mandatory seed“全集”。这再次表明当前主要风险不是“没有读过任何相关论文”，而是**跨轮次知识不能稳定回流到当前决策对象**。

### 3.3 应作为训练型 verifier 边界对照的工作

Think Twice, Act Once / VeGAS（2605.12620）在测试时采样多候选动作并由 verifier 选择，底层 policy 不更新；但论文同时说明 off-the-shelf verifier 无提升，因此训练了 verifier 所需的失败样本课程。[原始论文](https://arxiv.org/abs/2605.12620)

它是非常好的反例：**“测试时不改 policy”不等于“全系统 training-free”。** 同时，它也提示团队未来不能默认通用 LLM evaluator 天然有用；Stage-1A survey 应系统抽取 verifier 是否训练、训练数据如何来、在何种分布上失效。

## 4. 对 Gate S1 survey 设计的严格评价

### 4.1 已经正确的部分

v2 §11 的八项最低规格整体扎实：

- 发现源与原文承重源分离；
- 每 lane 要有 exact Boolean query、同义词、时间窗、结果上限和排序；
- mandatory seeds 与 citation chaining 并用；
- 明确纳排矩阵和开放式抽取字段；
- `NO_DIRECT_MATCH` 需要饱和判据和双评审；
- 承重 claim 要有版本与页/节/表/公式定位；
- 搜索失败、排除理由和可重建 ID 也要记；
- 最强 threat papers 双人独立全文抽取；
- 最终保留 3–5 个 system-level candidate problems，而不是提前指定胜者。

这些要求与 Stage-1A 的使命高度一致，也比继续写概念性 proposal 更有价值。

### 4.2 首条查询签署前必须补入的协议要求

#### A. 把“全集”改为有日期的预协议种子快照

种子集合应记录：

- snapshot date/time 与覆盖截止日；
- 来源：reviewer 点名、自库继承、数据库发现、citation chaining 或作者/项目页追踪；
- 首次发现位置；
- 当前仅题录、摘要核验还是全文核验；
- 被纳入哪个 lane，为什么；
- 被排除时的明确理由；
- 是否仍待解决范围归属。

在 survey 完成前，不使用“全集”“完整占据图”等措辞。正确说法是“截至某时间的 mandatory seed snapshot，允许检索扩展”。

#### B. 加入 recency delta scan

本项目处在快速移动的 2026 agent/omni 前沿。协议至少要规定：

1. 首次执行时检索到当日；
2. synthesis 冻结前再做一次从首次执行日到冻结日的增量扫描；
3. 若 Stage-1A 跨越较长时间，维护有日期的增量批次，而不是静态 seed list；
4. 新文献进入后按同一 schema 编码，不静默改写旧判决。

Omni-Decision 的出现已经证明这不是形式主义要求。

#### C. 扩充领域来源覆盖

当前 arXiv、ACL、OpenReview、IEEE、ACM 的组合仍可能漏掉关键正式版本。协议应明确覆盖或通过可靠索引回链到：

- CVF Open Access（CVPR/ICCV 等视觉与 embodied agent）；
- ISCA Speech Archive（Interspeech 等语音工作）；
- PMLR 与 NeurIPS proceedings（ICML/NeurIPS）；
- 必要时 AAAI/IJCAI 的正式论文页。

Semantic Scholar/OpenAlex 可以用于发现和 citation graph，但机制结论仍必须回到作者版本、正式论文或官方开放全文。

#### D. 明确一轮 chaining 之后的继续规则

“每个 mandatory seed 一轮 backward/forward chaining”可以是最低动作，不能是机械停止条件。若第一轮产生新的直接 system neighbor，必须对新 neighbor 继续 chaining，直到预注册饱和判据满足；否则一轮规则会系统性漏掉新簇。

#### E. 强 threat 双人抽取的选择过程也要留痕

不仅要保存最后 10–15 篇，还要保存进入候选池的全集、两名评审各自排序/理由、分歧和最终合并规则。否则“双人全文抽取”仍可能在上游选文环节发生无记录筛选。

#### F. 将范围判断拆成多轴，不用一个 DIRECT/OUT token 压平

至少分开：

- system-level proximity；
- component-level proximity；
- modality proximity；
- TF-Strict compliance；
- strict black-box compliance；
- reward-guided control proximity；
- persistence/state proximity；
- evidence grade。

这样才能正确表示“Walking Through Uncertainty 对 uncertainty 组件直接、对完整 agent system 不直接”或“Training-Free GRPO 对语义机制直接、对 TF-Strict 归属有争议”。

## 5. 工程基座是否合理

### 5.1 当前工程不能称为实验基座，v2 的披露是正确的

静态检查显示，W1 当前仅有：

- 一个 Hydra `main.py`；
- 主循环仍是 `TODO: implement the RL loop`；
- model/dataset/rl/experiment 五类 YAML 中仍包含 `rl/grpo.yaml` 的 training-oriented 配置；
- 测试仅为 smoke/import 级；
- 尚无通用 runner、controller、trajectory recorder、stage guard 或 model/dataset/tool/reward adapter 抽象。

因此，v2 §8 写“Hydra stub + 定制脚本，不称配置化基座”是准确、必要而且诚信的。没有发现团队用目录数量、YAML 数量或历史脚本数量冒充可复现实验平台。

### 5.2 v2 提出的下一步工程动作符合 Stage-1A，但应严格限于 ADR/schema

当前合理交付不是写完平台，而是一页到数页的决策记录，回答：

- 现有 Hydra 只负责配置组合，谁负责 agent runtime 与事件记录；
- 开源 harness 可复用到什么程度，是否支持黑盒 API 与 native multimodal payload；
- model、dataset、task、tool、feedback/reward、controller、memory/state 是否能独立替换；
- 一次运行的配置、输入版本、模型版本、随机性、工具调用、状态转移、输出与失败如何形成可回放事件流；
- 如何显式区分 `stage1a` 纸面/mock 与经授权的 `stage1b` 真实 adapter；
- 旧 GRPO 训练配置如何被隔离，避免默认配置与 TF-Strict 身份冲突；
- survey 知识组织与未来实验运行记录如何互相链接但不混成一个系统。

ADR 的比较矩阵至少应考察：

- backend/provider 可替换性；
- audio/image/video 与文本的统一消息表示；
- tool/environment 生命周期；
- state/memory persistence；
- reward/verifier 多信号输入；
- controller 可插拔性；
- trace/replay 与失败恢复；
- 完整配置导出；
- 隐式训练或自动优化是否能被禁用；
- 许可证、维护状态和最小自研成本。

Stage-1A 到此为止即可。**不应**为了证明 schema 可行而接真实模型、下载数据、跑 API、实现所有 adapters，或把某一尚未选定的 controller 写成默认路径。

## 6. 是否存在超越 Stage-1A 的探索尝试

### 6.1 本轮没有发现实验偷跑

v2 明确新执行为零；当前工程仍是 stub；§10 的 Stage-1B 探针被标记为无现时效力；§11 规定协议签署前零真实查询。就现有证据，不能指控团队已经偷跑模型实验、数据实验或 API 实验。

注意：**撰写检索协议本身就是 Stage-1A 工作，不是 Stage-1B 实验。** 对论文数据库执行经签署的查询也属于 survey，不应与模型/数据实验混为一谈。

### 6.2 需要警惕的不是技术超前，而是元流程膨胀

v2 前半部分大量篇幅用于解释评审谱系、内部敌意评审与状态 token。这些治理信息有价值，但继续生成 v3/v4 会让团队把 Stage-1A 变成“反复审 proposal 的工程”，而不是系统地获取知识。

从现在开始，除非发现事实错误，不建议再改提案主体。下一份承重工件应当是：

1. exact-query protocol；
2. seed manifest；
3. 数据源与检索字符串；
4. 纳排/抽取 schema；
5. 空白 ledger/census 模板；
6. reviewer 签署区。

这比再增加一轮“内部 CONVERGED”更符合 Stage-1A 价值。

## 7. 科研诚信与可回放性判断

### 7.1 当前没有学术欺诈证据

本轮没有发现：

- 捏造新实验或结果；
- 篡改实验数字；
- 把方向性数字冒充确证；
- 把内部评审冒充外部同行评审；
- 明知训练了外设却宣称全系统零训练；
- 宣称已证明 novelty/SOTA；
- 抄袭他人文本或机制而隐匿来源的直接证据。

因此，不应把“自库反扫再次漏项”直接升级为 fabrication/falsification/plagiarism。它首先是知识检索与组织失败。

### 7.2 但有三类需要立即控制的诚信风险

#### 风险一：过度完备措辞

在协议未执行时使用“种子全集”，会让后续读者误以为最近邻已覆盖。现在已经有明确反例。若团队在收到本意见后仍以该“全集”承重 novelty，风险会从措辞失严升级为选择性文献处理问题。

#### 风险二：标题驱动的范围漂移

`training-free`、`frozen LLM`、`test-time` 等标题不能代替方法审计。任何外部组件训练、ground-truth 使用、开发集蒸馏、轻量 verifier/value model 学习都要单独登记。否则 TF-Strict 会被悄然放宽。

#### 风险三：不可复放的“原始评审”表述

`docs/checks/2026-07-15-proposal-v2-hostile-review-lenses.md` 已保存问题、修复与 R2 结果，优于只写一句“已审”。但如果称其为完整原始工件，还缺：

- 每个 reviewer/agent 的稳定标识与运行时间；
- 输入 prompt 与 stage lens；
- 被审 commit/blob；
- 工具调用或检索命令；
- 未整理的原始输出或其哈希；
- 协调者如何合并、去重和裁决；
- R2 实际检查清单。

当前应把它理解为“评审报告归档”，而不是第三方可以逐 token 重放的完整运行记录。这不是欺诈结论，但命名必须与证据能力相称。

### 7.3 v2 对 v1 的动态引用需要钉死

本次审查快照为：

- v2：commit `cf54f1be921e9c26219121398461ceaf727295b7`，blob `20e5bd5537df55e61e04365e72a8324e1b77605b`；
- 同一快照下 v1 blob：`d60aa6692c395cc353d4ad5d8fb2f6e4d31c3910`。

v2 多处用“见 v1 §N”承载实质内容。实际 Gate S1 协议应把引用写成 commit/path/blob 三元组，或把承重表复制为带来源的版本化附件。否则未来继续编辑 v1 会改变 v2 的含义，却不会改变 v2 文件自身哈希。

## 8. 给团队的具体改进计划

### 8.1 首条真实查询执行前的必须项

1. 完成 exact-query protocol 实体，不再提交 proposal v3 代替协议。
2. 将 §4 的“全集”改为带截止时间的 seed snapshot，并在协议中规定增量扫描。
3. 至少补入 Omni-Decision、Affordance Agent Harness、FineVerify、Effective Feedback Compute、ACE、MUSE-Autoskill；VeGAS 作为 trained-verifier 边界对照。
4. 给 Training-Free GRPO 与 IRO 增加“冻结核心不等于 TF-Strict”的显式审计字段。
5. 增补 CVF、ISCA、PMLR/NeurIPS 等领域来源或可靠回链策略。
6. 写明 chaining 的继续/停止规则，不能把“一轮”当作有新发现时的强制停止。
7. 固定 seed manifest、v1/v2、taxonomy 和空白 extraction schema 的 commit/blob。
8. 保持查询零执行，待 reviewer 对上述协议实体签署。

### 8.2 survey 执行期间的必须项

1. 数据库响应、结果 ID、失败请求、去重、排除理由全部留痕。
2. 题录事实、摘要判断与全文机制判断分级，不把摘要推断伪装成全文结论。
3. 对 system-level proximity 与 component-level proximity 分轴编码。
4. 强 threat 的候选池、双评审分歧和最终选择规则全部保存。
5. 对直接近邻继续滚动 citation chaining，达到预注册饱和条件再停止。
6. 对新分类允许修订 taxonomy，但用版本化变更记录说明证据和影响。
7. 形成 3–5 个候选科学问题，每个都要列已占据部分、未解决 failure、可行原型方向、最强反对证据与尚缺信息。
8. survey 只产出候选与知识地图，不宣称最终 novelty，不自动滚入 Stage-1B。

### 8.3 可并行但不承重的工程项

1. 写 runner/config ADR 与开源复用比较矩阵。
2. 只定义配置和事件 schema，不连接真实 backend/data/API。
3. 明确 model/dataset/task/tool/reward/controller/memory 的替换边界。
4. 明确全量 trace、配置导出和失败记录要求。
5. 隔离旧 GRPO training config，避免身份误用。
6. 等 survey 暴露出候选问题后，再决定最小骨架需要支持哪些能力。

## 9. 最终签署表

| 审查对象 | 裁决 |
|---|---|
| v2 对上一轮 Stage-1A 校准意见的总体响应 | **通过；主要方向正确** |
| Gate S0 后的 system-first / TF-Strict 身份表达 | **作为 owner 假设通过；不等于 novelty 已证** |
| 当前最近邻 seed table | **可作预协议种子快照；不得称全集或完整占据图** |
| 关键引用真实性 | **抽查可解析；若干机制归属仍须全文核验** |
| 论文覆盖充分性 | **尚不充分；存在 Omni-Decision 等高优先级遗漏** |
| Gate S1 protocolization | **批准继续完成** |
| 首条真实检索查询 | **待完整协议单独签署** |
| 当前工程基座 | **仅 stub，不具实验基座资格；v2 披露正确** |
| Stage-1A 工程 ADR/schema | **允许，且不得承重或连接真实数据/模型** |
| 新模型/数据/API 实验 | **继续禁止** |
| Stage-1A close | **未申请，不评价** |
| Stage-1B | **未申请、未授权** |
| 本轮学术欺诈判断 | **无 FFP 证据；存在知识检索、完备措辞和可回放治理风险** |

**最终意见：`APPROVE_GATE_S1_PROTOCOL_DRAFTING_WITH_REQUIRED_AMENDMENTS`。**

这不是对研究方案科学成立的签字，而是允许团队把 Stage-1A 最重要的工作——广泛、可追溯、可反驳的 system-first survey——真正做起来。下一次送审对象应是可以逐条检查和重建的检索协议，不应再是一份更长的愿景提案。
