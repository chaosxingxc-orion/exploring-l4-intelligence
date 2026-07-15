---
title: "Stage-1A 研究提案博导级对抗审查——文献、工程基座、阶段边界与诚信风险"
date: 2026-07-15
review_object: "wiki/2026-07-15-stage1a-research-proposal-for-reviewer.md"
reviewed_base_blob: "a587feccabd75547df465de5f9abfb235af95c9e（开始审查时的 HEAD 正典）"
concurrent_worktree_note: "审查期间原 proposal 出现他方并发修订；只读比较到 worktree blob 235334963c757f62ca9d8039b021430a9c4a7925，未回退、覆盖或纳入本报告文件；并发修订没有关闭本报告的五项承重 P0"
review_role: "严格外审 / 博导预答辩；独立审查件"
stage_standard: "Stage-1A=问题定义、survey、候选身份和纸面协议；不运行任何新实验"
decision: "RETURN_FOR_MAJOR_REVISION — 不签 round-2 search design；不放行 Stage-1B"
source_edit_policy: "未修改被审提案、研究代码、配置、台账、状态文件或团队进行中的任何工件；仅新增本日期审查报告"
fraud_assessment: "未建立 FFP（fabrication/falsification/plagiarism）证据；建立了需要立即更正的重大记录范围失实与多项 QRP 风险"
---

# Stage-1A 研究提案博导级对抗审查

## 0. 一句话裁决

这份提案已经从“把一个方向写成既定贡献”进步为“把多个候选问题放在文献与可证伪合同下竞争”，其问题意识、失败登记和候选身份拆分值得保留；但是它目前**不能签署为完成的 Stage-1A proposal，也不能作为 round-2 或 Stage-1B 的放行依据**。

拒签不是因为它尚无实验结果——Stage-1A 本来就不应有新实验——而是因为下列五个承重问题仍未关闭：

1. “GPU 运行至今为零、全部证据为文献台账级”与同仓库已登记的 574 个历史运行工件、ASR selector battery、MMAU selector 和已触碰的 dev/test 数据直接冲突；
2. 真实实验路径仍以大量定制脚本为主，Hydra 主入口是 stub，当前不能称为“基于配置的实验基座”；
3. 当前 canonical survey 丢失了项目自己早已掌握的一批核心 prior，round-2 也未把它们设为必查 seed，知识组织链发生了“已知文献遗忘”；
4. `strict-I2` 仍有“新颖性靠后验合取”的嫌疑，`I4` 可能只有领域实例化，`UMBRELLA` 又是与池内选择不同的算子；一个 proposal 同时承载三种科学对象，身份没有真正收口；
5. 拟用于 Stage-1B 的 LibriSpeech、CREMA-D、MMAU-mini 与 Qwen3-Omni 均有历史暴露，不能未经 item-level reconciliation 再称“单次触碰”或把 test-other 称为未污染 publication holdout。

### 0.1 签署矩阵

| 请求 | 本轮裁决 | 理由 |
|---|---|---|
| 将本件视为有价值的 Stage-1A 工作底稿 | **可以** | 候选问题、失败条件、文献压力和治理链已有实质内容 |
| 签署 round-2 的现行 21 lanes / 105 queries | **拒签，须修订后重审** | 已知 prior 未 union 进正典；遗漏不能靠未来自由搜索碰运气补回 |
| 宣布 Stage-1A 已完成 | **拒绝** | survey 仍有结构性遗忘，研究身份与术语边界未定，工程资格门未定义 |
| 在 Stage-1A 内运行任何新 GPU/CPU 模型实验 | **禁止** | owner 本轮明确：Stage-1A 与 1B 必须硬隔离 |
| 进入 Stage-1B | **拒绝** | 先完成配置化基座、暴露清算、协议和 owner 独立签批 |
| 指控团队实施学术造假 | **证据不足，不成立** | 未见虚构论文、伪造实验产物或抄袭证据；但存在重大 QRP/记录准确性问题 |

## 1. 审查范围与判据

本轮没有修改原提案或任何工程文件。审查使用了四类证据：

- 被审提案及其引用的 census、claim ledger、round-2 protocol、身份合同和 owner 决策记录；
- `docs/integrity/prior_exposure_registry.json`、C1/C4 census 和 W1 `_repro` 的登记事实；
- W1 的 Hydra 配置、入口、loader registry、推理脚本、公共 selector 实现与测试；
- 论文的 arXiv、ACL Anthology、PMLR 与 ISCA 官方页面，并对项目旧 survey 中已经出现的 prior 做反向普查。

判据严格限定在 Stage-1A：本轮不要求显著性、SOTA、完整消融或独立复现；要求的是问题定义不偷换、prior 不被选择性遗忘、引用能支撑文字、候选身份可被证伪、Stage-1B 计划可合法开机，以及工程设计不会迫使团队继续“一实验一脚本”。

> **给协作 AI 的直白定义**：`evaluator/scorer/verifier` 负责评价候选并输出分数或偏好；`selector（选择器）/reranker/selection rule` 才根据这些信号从 K 池选出最终输出或 abstain。generator 负责造候选；oracle 偷看标准答案，只能用于测上界；agentic loop 会让决策影响下一步生成、检索或工具调用，因此又是另一种算子。很多系统把 evaluator+argmax 整体俗称 evaluator，但本项目必须拆开，否则无法判断创新和失败究竟来自评价信号还是决策规则。

### 1.1 本轮新增的阶段铁律

owner 本轮明确：**Stage-1A 之前/期间不应跑实验；Stage-1B 才是方向性原型探索。**据此，本报告把边界解释为：

- Stage-1A 允许：survey、文献全文核验、问题/术语/合同设计、配置 schema 设计、静态 lint、合成 fixture 单元测试、mock/fake backend 测试、历史工件盘点；
- Stage-1A 禁止：任何真实模型推理、真实数据 item 抽样或评分、候选生成、logprob 获取、真实数据 loader smoke、从新结果中调整问题或阈值；
- Stage-1B 起才允许：真实 item 的一次性方向性探针；**即使只跑一个 item、只为 smoke，也算一次实验和一次 exposure**；
- 历史上已经发生的运行不因本轮阶段重置而消失。它们只能标为 `INHERITED_PRIOR_EXPOSURE / hypothesis-grade`，不能包装成“本 proposal 尚无任何实验历史”。

## 2. 四轮对抗式评审

### Round A：科学身份与新颖性红队

**攻击 A0：研究对象究竟是 evaluator，还是 selector？**

当前 `strict-I2` 的核心描述是“同一冻结 omni 产生 audio-grounded score”，这首先是 evaluator/scorer 问题；若最终决策永远只是固定 argmax，selector 本身没有新方法。MBR、弃权、悲观选择、组合 routing 才是 selection rule 层的变化。Stage-1A 必须把对象拆成 `candidate generation → evaluation signal → selection rule → optional abstention/next action` 四层，并为每个候选身份指出创新落在哪一层。不得把“新的 evaluator”写成“新的 selector”，也不得把固定 selector 的收益归因给决策算法。

**关闭证据**：每份 identity contract 增加 `novelty_layer ∈ {generator, evaluator, selector, agentic_policy, measurement}`；若 evaluator 是唯一变量，题名与 claim 必须使用 `audio-grounded evaluator/reranker`，selector 只作为固定决策接口。

**攻击 A1：静态池内选择为什么叫 training-free RL？**

I1–I4 的共同算子是：在固定 K 池中用 label-free signal 选一个候选。若没有状态转移、动作影响后续观测、显式策略更新或 reward-guided 下一步动作，这在邻近文献中的标准名更接近 `best-of-N selection`、`reranking`、`MBR decoding`、`test-time scaling` 或 `inference-time alignment`。把所有池内选择统一称为 training-free RL，会把研究动机升级为方法结论。

**预期作者抗辩**：RL 只表示 reward-guided decision，不表示训练权重。

**审稿人反驳**：这是团队内部定义，不能替代领域标准语义。Stage-1A 必须把“training-free RL”本身设为待证伪术语：若最终对象只是 one-shot in-pool argmax，则对外标题应降为 `weight-frozen reward-guided inference-time selection`；只有 UMBRELLA 的序列闭环可能保留 RL/agentic 论证，而且它已被修正案确认是不同算子。

**关闭证据**：一页 terminology decision memo；列出 MDP 对象（state/action/reward/transition/policy）是否真实存在，并由 owner 在 Stage-1C 选择，而不是靠口号保留。

**攻击 A2：strict-I2 是否只是 novelty-by-conjunction？**

`同一冻结 omni`、`音频接地`、`自身信号`、`ρ(c) 曲面`的各组件均有 prior；“尚无单篇论文同时满足所有条件”不能自动构成科学贡献。后验合取很容易通过不断加限定词逃避占据者。

**作者可辩护的唯一道路**：strict-I2 必须提出一个**机制级、反直觉且可迁移的预测**，例如“同核 audio-grounded scorer 相对文本 scorer 的误差互补性在某类供给/任务条件下可由无标签量预测”，而不是“把四个已知组件放在同一系统里”。

**关闭证据**：identity contract 增加 `component novelty is insufficient`；proceed-if 必须包含超出组件拼接的规律或机制；否则降为工程 comparator。

**攻击 A3：I4 是科学问题，还是把已有 scaling surface 搬到音频？**

I4 是当前最值得保留的候选，但“此前 text/VLA 已做，audio/omni 还少”只证明 benchmark gap，不证明 method gap。要成为科学问题，至少要问：哪些 label-free observables 能在不同模型×任务×供给上增量预测 `H(c)`、`rho(c)` 或 failure regime；该规律能否超越 difficulty、entropy、agreement、length、diversity 和 compute budget 等通用 baseline。

现行 1B 蓝图只有一个 Qwen3-Omni×三个任务。它可以发现方向，不能支持“模型×任务矩阵规律”。如果 Stage-1C 选择 I4，Stage-2 必须有第二模型或明确把结论降为 `Qwen3-Omni case study`。

**攻击 A4：UMBRELLA 被错误地塞进 selector proposal。**

修正案已经正确说明 UMBRELLA 的 agentic loop 与 in-pool selector 是不同算子，但提案仍把它们放入同一个研究对象、同一个 Stage-1C 包。这样会让任何 selector null 被解释成转向 loop，也让 loop 的成功被拿来为 selector 纲领背书。

**裁决**：UMBRELLA 可留作平行候选 dossier，但必须有独立问题陈述、预算、comparator 与停止规则；不能共享一个 headline contribution。

### Round B：survey、引用和知识组织红队

**攻击 B1：round-2 不是从“项目全部已知文献并集”出发。**

旧 survey 已出现 `2203.11171`、`2311.17311`、`2311.05263`、`2402.11197`、`2404.01054`、`2505.03156`、`2604.04648` 等关键 prior；但现行 canonical census / claim ledger 没有稳定保留它们，round-2 protocol 对这些 ID 的精确出现次数为 0。这不是一般意义的“可能还漏论文”，而是**知识组织管线把团队已经知道的论文丢了**。

**作者可能抗辩**：round-2 keyword queries 可能重新搜到。

**反驳**：检索协议的职责不是让已知 prior 再次靠概率出现。所有历史 survey、review response、claim correction 与 external review 的引用必须先做 deterministic union，再开始新搜索。否则所谓 saturation/yield curve 的分母是错误的。

**关闭证据**：`legacy_prior_union` 工件，逐个 ID 给出 `imported / excluded-with-reason / duplicate-of`；遗漏 ID 全部成为 mandatory manual-import + forward/backward chase seeds。

**攻击 B2：提案使用裸 arXiv ID，不是可签署 bibliography。**

当前正文用短名+ID支撑承重判断，却没有统一列出题名、作者、版本日期、venue、peer-review status、URL、核验深度与 claim span。对于 2026 年预印本尤其危险：`Walking Through Uncertainty` 官方状态是 manuscript in progress；`Scaling Auditory Intelligence` 的早期实验和代码可用性不能与已发表方法等权。

**关闭证据**： proposal 附 reference table；每条承重 citation 必须同时有 canonical ID、版本、发表状态、证据级、支持/不支持的精确 claim。

**攻击 B3：I3 的综述没有吸收自己 corpus 中最直接的文献。**

提案 I3 dossier 只提 Walking、Goodhart、conformal-ASR，却遗漏：

- 当前项目已经登记的 `Speech Emotion Recognition with a Reject Option`——这是 speech/SER 的直接 risk-coverage 祖先；
- 当前邻域中已有的 MBR metric bias / reward hacking；
- regularized MBR-BoN、pessimistic BoN、abstention survey、semantic uncertainty 等直接方法族。

所以“I3-combined 暂无匹配”目前不能承担 proceed 倾向；它首先说明 I3 dossier 尚未成熟。

### Round C：工程与可回放性红队

**攻击 C1：Hydra 外观不等于配置化实验系统。**

工程中确实有值得保留的部件：数据锁、loader registry、llama.cpp commit pin、resident server、candidate selector primitives、尝试登记和 exposure guard。但承重事实是：

- W1 `src/training_free_rl/main.py` 明写 `RL loop is a stub`，运行时只打印 `TODO`；
- `configs/` 只有一个 Qwen2-Audio、一个 LibriSpeech、一个 GRPO、一个 baseline 配置，且与 proposal 的 Qwen3-Omni/llama.cpp/selector 运行路径不一致；
- 配置组没有 `engine`、`sampler`、`pool`、`supply`、`selector`、`metric`、`control`、`exposure`、`artifact`；
- W1 有 112 个 Python scripts；仅顶层按实验命名的 `cp/m/t/e/repro/probe` 等脚本就至少 25 个；真实结果大量来自环境变量和脚本内常量；
- 公共 `decode.py` 虽有 best-of-N/MBR/soft-BoN，但 tests 没有直接覆盖这些 selector，也没有覆盖 `generative_omni`；
- 基线 runner/loader registry 已形成部分抽象，但包含大量 dataset-specific branch、split override 和 legacy adapter，尚未成为 proposal 所需的单一实验图。

**裁决**：当前基座是“可运行但分裂的原型资产”，不是“配置驱动、可组合、可批量复放的实验基座”。如果继续为 P-α/β/γ/δ 各写脚本，实验差异与代码差异将纠缠，任何负结果都无法判断是方法差异还是 runner 差异。

**攻击 C2：HF generative adapter 与真实 llama.cpp 路径分叉。**

`common/models/generative_omni.py` 面向 Transformers Qwen3-Omni；历史和拟议运行使用 GGUF llama-server。若二者没有同一 backend interface、同一 request/response schema 和 golden contract test，公共代码并不是实验真实路径。

**攻击 C3：工程锁并非全坏，但必须在 manifest 中闭环。**

`scripts/env-setup.sh` 已把 llama.cpp 钉到 `fdbd6abee20e408de21e90ca77a24cd50a6ea073`，这点应肯定；模型锁也记录 Q8_0 GGUF+bf16 mmproj 的内容指纹。剩余风险是：模型上游 revision 仍标 `unknown`、audio path 被 upstream 标为 experimental、真实 resident server 是否就是该 commit 需要在每次 run manifest 通过 `/props`/binary hash 记录。不能把“代码里有 pin”自动等价为“这次运行用了 pin”。

### Round D：阶段边界与研究诚信红队

**攻击 D1：‘GPU 零运行’是重大范围失实。**

提案第 34、352 行写“GPU 运行至今为零”“探针结果尚不存在”，且说全部现有证据为文献级。可复核的项目自有登记却显示：

- `n_repro_artifacts_scanned = 574`；
- LibriSpeech、CREMA-D、MMAU-mini 均有 dev/test 历史触碰；
- 2026-07-02 至 07-11 已运行 Qwen3-Omni/llama.cpp ASR best-of-N/selector battery；
- 已存在 MMAU selector realization 与 m5 dev/confirmatory slice；
- 历史上甚至有因信息边界违规而撤回的 cross-modal/RAG probes。

这不能用“本轮 Gate A/B 零 GPU”替代。正确表述只能是：

> `new executions under STAGE1A-PROPOSAL-2026-07-15-01 = 0; inherited project experiments and dataset exposures are extensive and remain hypothesis-grade; current proposal makes no new empirical claim.`

**诚信裁决**：目前没有证据证明作者有欺骗意图，故不构成 FFP 结论；但这是影响审稿人理解研究成熟度和 holdout 状态的**重大 QRP/记录准确性缺陷**，必须在任何签署前更正。

**攻击 D2：Stage-1B 蓝图重用已暴露对象，却写 single-touch。**

`dev-other / CREMA-D subset / mmau-mini / Qwen3-Omni` 不是全新表面。`prior_exposure_registry` 还记载 LibriSpeech dev 与 test 均触碰，且旧 test/locked holdout 有 overlap 和永久降级。提案不能仅把 test-other 写成 publication holdout，就假定它未污染。

**关闭证据**：在 Gate C 前生成 item-level exposure union；对每个候选 item 证明未在任何 manifest、artifact、log、prompt/config selection 中出现。无法证明者一律视为 exposed。若剩余样本不足，换数据集或承认 1B 仅为 `retrospective continuation`，不得称 single-touch。

**攻击 D3：PRE_STAGE2_BLUEPRINT 标签越界。**

提案把整个 §6（包括 Stage-1B 探针）称为 `PRE_STAGE2_BLUEPRINT`。Stage-1B 不是 Stage-2；把它们混在同一 future blueprint 会弱化 1A→1B 的显式门。应拆成：

- `STAGE1B_PROTOCOL_DRAFT — no execution authority`；
- `PRE_STAGE2_BLUEPRINT — no present effect`。

**攻击 D4：owner 的 C1/C4 签署确实存在，但元数据仍自相矛盾。**

修正案 §D 与 Decision-Log 续43 清楚记录 owner 两栏独立签署，故本轮不把它判为虚假签署；但修正案 frontmatter 仍写 `signoff: PENDING_RESIGN`，正文又写已签。机器与 AI 默认读取 frontmatter 时会得到相反状态。此为治理 schema 缺陷，应以 dated correction 或显式 effective-state resolver 修复，不能靠读者知道“正文优先”。

## 3. 逐项引用审查

### 3.1 主要引用总体判断

| 引用/用途 | 判断 | 必须补的限定 |
|---|---|---|
| [MBR-ASR, 2510.19471](https://arxiv.org/abs/2510.19471) 支撑 I1 被占据 | **合理** | 明确版本、Whisper/语言/数据依赖；不能把单格 31% 当通用兑现率 |
| [Scaling Auditory Intelligence, 2503.23395](https://arxiv.org/abs/2503.23395) 支撑 audio-conditioned likelihood/verifier 已存在 | **机制级合理** | 证据规模与发表/代码状态有限；只支持存在性，不支持强泛化或 SOTA 基座 |
| [KIT, 2606.04730](https://arxiv.org/abs/2606.04730) 支撑任务间符号翻转 | **重要且合理** | 保留 ASR/ST/SQA/SSUM 分任务，不允许聚合成平均“有效” |
| [JudgeBoN, 2603.12520](https://arxiv.org/abs/2603.12520) 映射 rho_pool | **合理** | 它锚定 random/pool，不等同 rho_greedy；提案已做了正确更正 |
| [Walking Through Uncertainty, 2604.25591](https://arxiv.org/abs/2604.25591) 支撑 ALLM uncertainty/abstain | **方向合理、证据等级需降** | 官方为 manuscript in progress；不得作为 I3 已被完整占据的唯一承重来源 |
| [Inference-time reward hacking, 2506.19248](https://arxiv.org/abs/2506.19248) 支撑 Goodhart | **合理** | 是文本/代理 reward 场景；需要 speech 迁移机制，不可直接声称 speech 拐点 |
| [Conformal ASR, Ernez et al.](https://proceedings.mlr.press/v204/ernez23a.html) | **合理** | 80% 是置信水平而非观测覆盖，当前更正是对的 |
| [Snell et al., 2408.03314](https://arxiv.org/abs/2408.03314)、VG-Search、Art of TTC、RoboMonkey 支撑 I4 方法族已占 | **合理** | 这些文献反而削弱“供给曲面本身新颖”；贡献须落到 label-free 增量规律 |
| [IAD, 2504.01931](https://arxiv.org/abs/2504.01931) 支撑 loop vs one-shot | **合理** | 它是 UMBRELLA comparator，不应与固定池 selector 混为同一对象 |
| [AudioToolAgent, 2510.02995](https://arxiv.org/abs/2510.02995) | **区分合理** | 中央 agent 不接触音频的边界要保留；但“无单篇满足完整合取”仍非新颖性证明 |
| [BoN gain predictor, 2606.02981](https://arxiv.org/abs/2606.02981)、[LLM-as-Verifier, 2607.05391](https://arxiv.org/abs/2607.05391)、[CoVer, 2602.12281](https://arxiv.org/abs/2602.12281) | **必须纳入** | 不应只作为“集外压力”，应进入 canonical union 后再讨论身份 |

### 3.2 proposal 中遗漏、但项目过去已经知道的 P0 prior

这些不是“建议以后顺便读”，而是 round-2 执行前必须 deterministic import 的文献：

| 文献 | 为什么承重 |
|---|---|
| [Self-Consistency Improves Chain of Thought Reasoning, 2203.11171](https://arxiv.org/abs/2203.11171) | K-sample consensus 的经典基线；所有多数/一致性 selector 的祖先 |
| [Universal Self-Consistency, 2311.17311](https://arxiv.org/abs/2311.17311) | 开放式输出的一致性选择，直接压 I1 与 spoken QA |
| [Model-Based Minimum Bayes Risk Decoding, 2311.05263](https://arxiv.org/abs/2311.05263) | model-based utility 的直接祖先，压 strict-I2/self-scoring |
| [Centroid-based MBR, 2402.11197](https://arxiv.org/abs/2402.11197) | MBR 近似与候选几何，属于工程强基线邻域 |
| [Regularized Best-of-N Sampling with MBR Objective, 2404.01054 / NAACL 2025](https://aclanthology.org/2025.naacl-long.472/) | 直接处理 BoN reward hacking；是 I3 最关键 comparator 之一 |
| [Soft Best-of-N Sampling, 2505.03156](https://arxiv.org/abs/2505.03156) | 硬 argmax 的正则/软化祖先，关系到 Goodhart 与 KL 约束 |
| [Curiosity to Caution: Pessimism for BoN, 2604.04648](https://arxiv.org/abs/2604.04648) | 置信下界/悲观选择，直接挑战 I3 combined 的方法空白 |
| [Mitigating Metric Bias in MBR Decoding](https://aclanthology.org/2024.wmt-1.109/) | 同一 metric 做选择与评估会产生 metric bias/reward hacking；必须进入 I3 与 P-β 设计 |

若团队不能解释这些文献为何从旧 survey 消失于当前正典，就不能声明知识组织已经“收口”。

### 3.3 本轮新增建议的高优先级论文

| 优先级 | 文献 | 对当前方案的直接压力 |
|---|---|---|
| P0 | [Is Best-of-N the Best of Them? Coverage, Scaling, and Optimality, 2503.21878](https://arxiv.org/abs/2503.21878) | coverage、scaling 与 pessimistic rejection 直接对应 H(c)/池覆盖/Goodhart；是理论和 I3/I4 的共同祖先 |
| P0 | [Theoretical Guarantees for MBR Decoding](https://aclanthology.org/2025.acl-long.793/) | 给 MBR 的统计收敛界；提案理论轨不能只引用自家 Lean 理想化定理 |
| P0 | [Diversity Explains Inference Scaling Laws](https://aclanthology.org/2025.acl-long.1410/) | 用 bias–diversity 分解解释 MBR scaling，直接挑战 I4 的“新规律”空间 |
| P0 | [Structure-Conditional MBR](https://aclanthology.org/2025.emnlp-main.1616/) | 表明相似度 MBR 在潜在结构变化下会失败；P-β 不能把一个 BLEU-MBR 当普适基线 |
| P0 | [Unveiling the Power of Source: Source-based MBR](https://aclanthology.org/2025.acl-long.149/) | source-conditioned、reference-free MBR 与 audio-grounded selection 概念非常接近 |
| P0 | [Know Your Limits: A Survey of Abstention in LLMs](https://aclanthology.org/2025.tacl-1.26/) | I3 的标准 taxonomy、评估与失败模式入口 |
| P0 | [Speech Emotion Recognition with a Reject Option](https://www.isca-archive.org/interspeech_2019/sridhar19_interspeech.html) | 直接 speech/SER risk–coverage prior；当前项目已知但 proposal 未综合 |
| P1 | [Semantic Uncertainty, 2302.09664](https://arxiv.org/abs/2302.09664) | 无监督 semantic entropy 是 I3 和 I4 必须击败的简单 label-free baseline |
| P1 | [Think Deep, Think Fast, 2504.14047](https://arxiv.org/abs/2504.14047) | 反证性 prior：更多推理计算未必有效，majority 往往很强；防止只搜复杂 verifier |
| P1 | [Model/data-dependent demonstration selection](https://aclanthology.org/2024.acl-long.492/)、[model-specific demo retrieval](https://aclanthology.org/2024.naacl-long.235/)、[quality-diversity DPP selection](https://aclanthology.org/2023.emnlp-main.331/) | 供给选择是成熟领域；I4 不能把 prompt/context/demo selection 重新命名成供给创新 |

### 3.4 citation acceptance rule

后续每条承重引用至少需要以下字段，否则不能进入 proposal 结论：

```text
work_id / title / authors / canonical_url / version_date / venue_status
claim_supported / exact_span_or_table / evidence_level
population(model, task, dataset, language, K, supply)
what_it_does_not_support / reviewer_verdict
```

## 4. 工程基座裁决：必须从“脚本集合”升级为“配置化实验图”

### 4.1 当前成熟度

| 层 | 当前状态 | 裁决 |
|---|---|---|
| 资产锁与下载 | 数据/模型 lock、内容指纹、统一 downloader 较强 | **可保留** |
| 数据 adapter | W1 `scripts/loaders/registry.py` 已有统一 Row contract 和大量 loader | **部分成熟**；应迁入稳定 package/interface |
| 模型 runtime | llama.cpp resident path 已跑通并有 commit pin | **方向原型可用**；audio experimental、run-time attestation 待闭环 |
| Hydra 配置 | 只有 Qwen2-Audio/LibriSpeech/GRPO/baseline；与真实 proposal 路径不一致 | **不合格** |
| 主入口 | 仅打印 TODO，RL loop stub | **不合格** |
| sampler/pool | 多个 repro/cp/m/t 脚本各自生成 | **不合格** |
| selector | `common/rl/decode.py` 有 primitives；真实脚本又有各自实现 | **有资产、未统一** |
| metrics | common metrics + scripts-specific scoring 并存 | **需 registry 化** |
| provenance/exposure | 已有较强 guard，但历史缺口永久存在 | **可保留并设为 runner middleware** |
| 自动测试 | common 21 pass（此前实测）；core selector/generative path 无直接测试；W1 仅 import smoke | **不足以开机** |
| theory↔implementation | registry 明记 operator-linked theorem=0、无 conformance test | **未闭环** |

### 4.2 Stage-1B 前必须具备的配置抽象

不要求 Stage-1A 把完整研究系统实现完，但要求先冻结下面的**接口和 schema**，并用 synthetic/mock fixture 验证。Stage-1B 开机后只允许通过一个统一 runner 执行；新实验差异只能来自配置，不得复制 runner。

```yaml
study:
  id: s1b_palpha_asr_c0
  stage: stage1b_directional
  hypothesis_id: P-alpha

dataset:
  name: librispeech
  adapter: librispeech
  split: dev-other
  item_manifest: manifests/s1b_palpha_asr_c0.json
  exclusion_union: manifests/all_prior_exposures.json
  group_key: speaker_id

backend:
  name: llama_cpp_chat
  model_asset: qwen3-omni-30b-a3b-instruct-gguf
  server_url: http://127.0.0.1:8091
  required_commit: fdbd6abee20e408de21e90ca77a24cd50a6ea073
  audio_mode: input_audio

supply:
  id: c0
  prompt_template: prompts/asr_bare_v1.j2
  retrieval: disabled
  tools: []

sampling:
  k: 16
  temperature: 0.8
  top_p: 0.95
  seeds: [ ... ]
  max_tokens: 100

evaluators:
  - {name: same_core_likelihood, length_normalization: mean_token}
  - {name: pairwise_bleu}

selection_rules:
  - {name: greedy}
  - {name: argmax_score, evaluator: same_core_likelihood}
  - {name: mbr, evaluator: pairwise_bleu}
  - {name: random, seed: ...}

evaluation:
  utility: neg_wer
  report: [headroom, rho_greedy, rho_pool, delta_mbr, regret]
  cellwise_only: true

controls:
  information_boundary: fail_closed
  matched_audio: [correct, permuted, silence, hard_negative]

artifacts:
  attempt_registry: required
  request_response_log: required
  resolved_config: required
  environment_attestation: required
  write_policy: immutable_run_dir
```

### 4.3 必须形成的组件边界

1. `DatasetAdapter`：`load_manifest()`、`materialize(item_id)`、`gold_for_evaluation_only()`、`group_key()`；模型侧对象中绝不携带 gold。
2. `InferenceBackend`：统一 HF/llama.cpp/未来 API 的 request/response；必须返回 raw response、token/logprob capability declaration 与 backend attestation。
3. `SupplyBuilder`：prompt、retrieval、tool output、audio/text context 全部配置化，产生供给 `c` 的 canonical hash。
4. `CandidatePoolGenerator`：K、seed、sampling params、retry/failure policy 统一；P-α/β/γ/δ 共享同一 pool artifact。
5. `Evaluator` registry：likelihood、audio-support verifier、pairwise utility、external metric；明确输出是 scalar、pairwise preference 还是 uncertainty，并声明可读取字段，gold 永远不可见。
6. `SelectionRule` registry：greedy/random/majority/argmax-score/MBR/pessimistic/abstain/router；它消费 evaluator 输出或候选关系，不能暗中重新调用模型。
7. `Metric` registry：任务效用 `U` 与 evaluator proxy `S` 类型分离；禁止同名 metric 在选择与评估中无标记复用。
8. `ControlTransform`：audio permutation/silence/hard-negative、supply c0/c1 不是另写脚本，而是变换配置。
9. `ExperimentRunner`：解析配置、验证阶段授权、检查 exposure、生成 manifest、执行、收集指标；所有真实运行只有这个入口。
10. `StageGuard`：`stage=stage1a` 时 backend 必须是 `fake/null`，检测到真实数据路径或网络/model endpoint 立即 fail；`stage1b` 需要 owner-signed manifest hash。
11. `ArtifactContract`：resolved config、git SHA、asset hash、server props、item IDs、all attempts、stdout/stderr、raw responses、metrics 与 provenance 全部同目录、不可覆盖。

### 4.4 开机前必须通过的工程测试

所有测试在 Stage-1A 只能使用 synthetic data/fake backend：

- 同一配置两次解析得到完全相同 canonical hash；
- 改一个 sampling/selector/supply 字段，run hash 必须变化；
- gold 注入 prompt/selector 时 fail-closed；
- 不支持 logprob 的 backend 配置 likelihood selector 时 fail-closed；
- P-α pool 被 P-β/γ/δ 读取时字节哈希一致；
- fake pool 上 greedy/MBR/oracle/rho/regret 有手算 golden test；
- 空池、失败候选、重复候选、分母过小、tie、abstain 都有 contract test；
- Stage-1A 配置指向真实 llama-server 或真实数据时必须拒绝；
- prior exposure union 缺一项时 manifest freeze 必须拒绝；
- Python selector 与 Lean 示例逐例一致，才可声称 theory–implementation linkage；否则理论只作背景。

### 4.5 禁止继续的工程习惯

- 不得为 P-α/P-β/P-γ/P-δ 各复制一份生成和加载代码；
- 不得靠 `BON_*`、`CP1_*`、`M3_*` 环境变量形成不可见配置；环境变量只允许路径/secret/server location，科学参数必须进入 resolved config；
- 不得在脚本常量中冻结样本量、K、temperature、threshold 或输出路径；
- 不得由脚本文件名承担实验身份；实验身份来自 immutable config + manifest hash；
- 不得让 `common` HF adapter 与真实 llama.cpp 路径分别演化而没有 backend contract test；
- 不得用“已有一个 Hydra 文件”宣称基座配置化。

## 5. Stage-1A / 1B 边界重划

| 工作 | Stage-1A | Stage-1B | 说明 |
|---|---:|---:|---|
| 文献检索、全文核验、citation chase | 允许 | 可继续 | 必须可回放 |
| 研究问题、身份合同、kill/pivot/proceed 设计 | 允许 | 冻结后仅按规则执行 | 1B 不能看到结果后改身份 |
| 配置 schema、接口、mock backend、synthetic unit test | 允许 | 允许维护 | 不触碰真实模型/真实 item |
| 读取真实数据 item 做 loader smoke | **禁止** | 允许且计 exposure | “只是 smoke”不豁免 |
| 调 llama-server/HF/API 生成一个候选 | **禁止** | 允许且计 experiment | CPU/GPU/API 均同等对待 |
| 计算真实 headroom/MBR/rho | **禁止** | 方向性允许 | 只能 hypothesis-grade |
| 根据真实结果改 c1、selector 或阈值 | **禁止** | 也禁止静默修改 | 必须登记新 attempt / post-hoc |
| 大样本 CI、SESOI、SOTA、test holdout | 禁止 | 禁止作为确证 | 属 Stage-2 |

因此，原提案中“Gate A/B 收口→round-2→Stage-1B”的次序需要改为：

```text
Stage-1A:
  legacy-prior union
  -> round-2 design repair and literature execution
  -> identity/terminology decision package
  -> configurable-base schema + synthetic verification
  -> item-level prior-exposure reconciliation
  -> Stage-1A close review

explicit owner transition

Stage-1B:
  signed manifest
  -> first real-item/backend smoke (itself is attempt #1)
  -> P-alpha shared pools
  -> P-beta/gamma/delta reuse pools
  -> honest directional package
  -> Stage-1C owner decision
```

## 6. 建议保留的 research proposals

### Proposal A（优先）：供给条件的 headroom/realization 测量学

**问题**：在冻结 omni 模型中，哪些部署时可见、无标签的候选池统计量，能预测不同任务与供给下是否存在 headroom、selector 能否兑现，以及何时越选越差？

**必须超越的 baseline**：entropy、semantic entropy、agreement、diversity、length、likelihood margin、task difficulty proxy、K/compute、MBR dispersion。

**科学贡献门**：不仅画 surface；必须有跨 cell 的增量预测、校准或 failure taxonomy。一个模型三个任务只够 1B 探路，不够最终 law。

**kill**：无标签量对 H/rho 无稳定增量预测，或规律完全由通用 baseline 解释。此时降级为 benchmark/engineering report。

### Proposal B：音频接地的同核 selector 是否有独立价值

**问题**：同一冻结 omni 作为 generator 与 audio-grounded scorer 时，scorer 的决策是否真的因音频而变，并提供超越文本共识/likelihood/外部 metric 的互补信息？

**必须做的因果控制**：correct/permuted/silence/hard-negative audio；score delta、rank、margin、U；有头空 item 上四格错误与 router upper bound。

**kill**：音频控制不改变 score/排序/效用，或同核与外部信号高同错且无组合增益。此时 strict-I2 不成立，不得靠“完整合取无人做”续命。

### Proposal C：Goodhart-aware selective decoding for speech

**问题**：当 K 或 verifier pressure 增大时，speech/omni selector 在什么条件下出现 proxy improvement、task utility degradation；能否用悲观界、MBR regularization 或 abstention 在给定 coverage 下控制风险？

**必备 prior/comparator**：metric-bias MBR、regularized MBR-BoN、pessimistic BoN、semantic uncertainty、conformal risk control、SER reject option。

**kill**：预算内没有可重复拐点；或者现有 generic pessimism/abstention 直接解决，不产生 speech-specific mechanism。此时只作迁移验证。

### Proposal D（必须分离）：reward-guided omni agentic loop

**问题**：在等总调用/令牌/延迟预算下，利用 reward/advantage 选择下一步 observation/tool/query/action 的闭环，是否优于一次性 BoN/MBR/reranking？

**边界**：这是 sequential operator，不属于 fixed K selector。若保留“training-free RL for omni agentic system”作为项目落脚点，应把本 proposal 单列；其 state/action/transition/reward 和 agent 实际音频接触必须可审计。

**kill**：loop 等价于增加候选后一次 rerank，或优势完全来自更高预算/额外信息。

## 7. 分优先级整改计划

### P0：在 reviewer 签署 round-2 之前

1. **更正运行范围**：把两处“GPU 零运行/全部文献级”改为“本 proposal 新执行为零；历史实验与暴露广泛存在”，并链接 exposure registry。
2. **建立历史文献并集**：扫描全部旧 survey/review/ledger；导出 unique canonical IDs；逐条 import/exclude；上述 P0 prior 不得遗漏。
3. **修订 round-2 protocol**：增加 `LEGACY-IMPORT` lane；把已知 prior 设置为 mandatory seeds；再增加 MBR theory/diversity/source-conditioned/abstention/SER reject lanes。
4. **重建 I1–I4/UMBRELLA dossier**：每个候选都给 closest three works、delta table、组件占据与完整对象占据，禁止只写“无单篇满足合取”。
5. **冻结阶段术语**：明确 Stage-1A 零实验；把 Stage-1B draft 与 PRE_STAGE2_BLUEPRINT 分开；写出任何真实 smoke 都从 1B attempt #1 计数。
6. **修正治理状态冲突**：amendment frontmatter 的 PENDING 与正文已签不得并存；以 dated correction 解决，不改写历史。

### P0：Stage-1B 放行之前

7. **配置化资格门**：冻结统一 experiment schema、component registry 和唯一 runner；P-α/β/γ/δ 不得有定制 runner。
8. **synthetic-only verification**：完成 §4.4 测试；StageGuard 证明 1A 配置无法触发真实模型/数据。
9. **item-level exposure reconciliation**：对 LibriSpeech/CREMA-D/MMAU-mini 生成历史 item union；无法证明未触碰即视为 exposed；重新选择 untouched manifest。
10. **backend attestation**：冻结 llama.cpp commit、binary hash、server props、GGUF/mmproj hash、sampling defaults 与 capability declaration；echo-logprob 未通过只能称 likelihood feasibility blocked。
11. **core test coverage**：best-of-N/MBR/soft-BoN/rho/regret/headroom/info-boundary/backend schema 都有直接 contract tests。
12. **owner 独立签批**：签的是 exact config schema + item manifest + exposure union + protocol hash；不得与 survey 或 integrity 签署混栏。

### P1：Stage-1B 内

13. 第一条真实模型调用即登记 attempt #1；失败、OOM、parse failure、server restart 同样入分母。
14. 先生成一次 P-α shared pool；P-β/γ/δ 只能复用，除非新 pool 被登记为新 attempt。
15. 不跨任务平均 rho；同时报告 H、rho_greedy、rho_pool、delta_mbr、regret、coverage/risk 和失败率。
16. P-γ 必须先完成 matched audio controls，再谈“音频接地”；只有 likelihood 时按修正案降名。
17. P-δ 的 c1 在任何真实结果前冻结；换 c1 是新 attempt，不得覆盖旧结果。

### P2：Stage-1C 决策包

18. owner 必须只选一个主科学问题；UMBRELLA 若保留则单独立项。
19. 对每个候选提供 `kill / pivot / proceed / evidence insufficiency` 四态，而不是强迫三态得出方向。
20. 明确哪些结论只是 Qwen3-Omni case study，哪些未来需要第二模型、第二语言或第二任务族验证。
21. Stage-1B 的任何数字永久保持 hypothesis-grade；Stage-2 重新预注册、重新取样、重新建立效应。

## 8. 给研究团队 AI 的机器可执行验收清单

下面每项必须返回 `PASS/FAIL + artifact path + exact hash`，不允许输出“基本完成”“大部分满足”：

```text
S1A-01 new_real_executions_since_proposal == 0
S1A-02 inherited_exposure_statement_present == true
S1A-03 legacy_prior_union_complete == true
S1A-04 mandatory_missing_prior_ids_remaining == 0
S1A-05 bibliography_has_version_venue_status_span == true
S1A-06 fixed_pool_selector_and_agentic_loop_have_separate_contracts == true
S1A-07 training_free_rl_terminology_decision_status in {OPEN_EXPLICIT, OWNER_DECIDED}
S1A-08 stage1b_protocol_is_not_labeled_pre_stage2 == true

BASE-01 hydra_or_equivalent_single_runner_executes_all_probe_shapes == true
BASE-02 real_scientific_parameters_outside_resolved_config == 0
BASE-03 dataset_adapter_registry_covers_planned_cells == true
BASE-04 backend_contract_llamacpp_and_hf_or_api == true
BASE-05 evaluator_and_selection_rule_registries_have_direct_unit_tests == true
BASE-06 stage1a_real_backend_guard_test == PASS
BASE-07 gold_information_boundary_negative_tests == PASS
BASE-08 shared_pool_hash_reuse_test == PASS
BASE-09 exposure_union_fail_closed_test == PASS
BASE-10 theory_python_conformance in {PASS, EXPLICITLY_UNLINKED}

GATEC-01 untouched_item_manifest_proven == true
GATEC-02 owner_signature_matches_exact_manifest_hash == true
GATEC-03 runtime_binary_model_mmproj_hashes_frozen == true
GATEC-04 first_real_call_not_yet_executed_at_signoff == true
```

任何一项 FAIL：不得开机；不得通过增加解释文字把 FAIL 聚合成 overall PASS。

## 9. 学术诚信最终判断

### 9.1 没有足够证据认定的事项

- 没有发现伪造的论文或不存在的 arXiv ID；
- 抽查的主要数字纠错方向总体真实，且有多处更正损害自身叙事；
- C1/C4 的 owner 两栏签署有正文和 Decision-Log 支撑，不应诬称为伪造签字；
- 没有建立 fabrication、falsification 或 plagiarism 的主观故意与完整证据链。

### 9.2 已经建立的 QRP / 高风险事项

- “GPU 至今零运行/全部文献级”是可被内部 registry 直接反证的重大范围失实；
- 已知 prior 从正典丢失，可能导致选择性 novelty 叙事；
- 后验合取可能形成 moving target novelty；
- 暴露过的数据/模型被重新包装成 single-touch 的风险很高；
- Hydra stub 与大量定制脚本不支持“配置化、可回放基座”表述；
- 理论与实际 selector 仍无 operator conformance，不得声称 Lean 已证明实际系统。

这些问题若在被明确指出后仍不更正、仍把 test-other 称为未触碰、仍以漏失 corpus 宣称空白，届时诚信评估将升级；但在本轮证据下，最严谨的结论是：**FFP NOT ESTABLISHED；MATERIAL QRP ESTABLISHED；立即纠偏并保留审计轨迹。**

## 10. 最终导师意见

研究团队当前最需要的不是再写一个更复杂的 selector，也不是急着跑四个探针；而是先完成三件基础工作：

1. 把所有已经知道的 prior 组织成不会遗忘的正典知识系统；
2. 把“一个实验一段脚本”改造成“一个统一 runner + 可组合配置 + 不可覆盖工件”；
3. 把 Stage-1A 的零实验边界写成机器会拒绝真实 backend 的 guard，而不是靠口头纪律。

做到这三点后，Proposal A（供给条件的失败/兑现测量学）与 Proposal C（Goodhart-aware selective decoding）有形成严肃研究问题的潜力；Proposal B 可作为机制探针；UMBRELLA 应独立成另一条 sequential-agentic 研究线。当前提案可以保留为高质量底稿，但须按 P0 整改后重新送审，**本轮不签字**。
