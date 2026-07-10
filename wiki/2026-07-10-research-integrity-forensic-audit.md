---
title: 研究诚信法证审查：当前实验记录是否足以排除学术造假风险
date: 2026-07-10
stage: Stage 1 — Problem definition / forensic integrity audit
scope: W1–W4、论文草稿、_repro、MLflow、Git 历史与现有实验治理
review_mode: read-only, adversarial, claim-to-artifact audit
verdict: STOP-THE-LINE — 未发现足以认定故意学术造假的直接证据，但已确认多项无效阳性、错误边界陈述和系统性研究记录失控；当前证据不具备发表级可信度
status: independent dated report; no source/config/result file modified
---

# 研究诚信法证审查：当前实验记录是否足以排除学术造假风险

> **结论先行：当前不能据证据认定研究团队实施了捏造或篡改，但同样不能把现有研究记录称为“可信、可发表、可独立复核”。** 本次审查确认了至少两类因信息泄漏产生的无效阳性、若干会改变结论的统计口径问题、一个无法由所指脚本直接生成的提交汇总、一次后来才脚本化的手工置信区间写入，以及大量无法从提交物独立复算的结果。它们共同构成**系统性的研究诚信控制失败**。在证据冻结、逐项裁决和独立复现完成前，应停止继续堆叠新结果，也不得用“Stage 1”或“directional-only”替代基本的真实性、可追溯性和边界准确性要求。

本文只新增本报告；没有修改代码、配置、数据、实验结果、论文正文或其他团队记录。

## 0. 审查问题与严格结论

本次审查回答的不是“项目想法有没有潜力”，而是四个更尖锐的问题：

1. 已报告数值是否确实来自所声称的实验？
2. 原始输出、汇总、统计检验和论文论断之间是否存在可验证的完整链条？
3. 是否存在泄漏、挑选、重算、口径漂移或手工加工，使研究记录产生了不真实或误导性的印象？
4. 现有证据能否支持对 fabrication/falsification（捏造/篡改）的故意性判断？

严格裁决如下：

- **故意捏造：未证实。** 没有发现凭空生成样本、批量复制结果、不可解释的超现实运行时间，或主 ASR 原始池与汇总数值不一致的直接证据。
- **故意篡改：未证实。** 发现了手工写入统计量和原位重评分等高风险操作，但现有 Git 历史保留了更正说明，尚不足以证明其意图是欺骗。
- **已证实无效结果：存在。** M3 的跨模态阳性由真值转写注入产生；T7 的 RAG 阳性主要由知识库答案查表产生。后续记录已承认并纠正，但原始阳性工件没有被机器可读地作废。
- **已证实误导性/错误陈述：存在。** 包括把不同数据子集与不同噪声同时变化的三次运行描述成 generation seed 控制、把宏平均 utterance-WER 不加说明地报告成 WER、以及把有限候选硬 argmax 与分布层面的 Gibbs tilt 说成同一个具体实现。
- **可追溯性失败：严重。** 多项数字只有摘要，没有行级预测；MInDS 提交 JSON 不能由所指脚本直接产出；许多复现实例缺 Git commit、模型哈希、数据 manifest 哈希、推理引擎版本和环境锁。
- **发表级完整性：不通过。** 当前研究记录必须进入“证据隔离与正式裁决”状态，不应继续被当成一组可以自由引用的阳性发现。

## 1. 不把方法错误偷换成造假：判定标准

美国 Office of Research Integrity 将 fabrication 定义为编造数据或结果并记录或报告，将 falsification 定义为操纵研究材料、设备、过程，或改变/遗漏数据或结果，使研究记录不准确；诚实错误和意见分歧不属于研究不端。[ORI: Definition of Research Misconduct](https://ori.hhs.gov/definition-research-misconduct) 现行法规还要求分别判断行为、显著偏离通行规范、故意/明知/鲁莽的主观状态，以及优势证据标准。[42 CFR Part 93](https://www.govinfo.gov/link/cfr/42/93?link-type=pdf&year=mostrecent)

因此，本报告使用下列证据等级，禁止把“结果无效”自动升级成“作者造假”：

| 等级 | 含义 | 本报告中的处理 |
|---|---|---|
| IR-0 | 已复算且链条基本完整 | 可保留，但仍受 Stage 1 外部效度限制 |
| IR-1 | 设计弱点或记录不充分 | 必须补证，不能作强结论 |
| IR-2 | 可疑研究实践或误导性报告 | 必须纠正并接受独立审查 |
| IR-3 | 已证实无效/错误的研究主张 | 立即作废，禁止继续引用为证据 |
| IR-4 | 正式诚信调查触发器 | 冻结证据，要求当事人解释与独立复现 |
| IR-5 | 有充分证据认定 fabrication/falsification | 本次审查没有达到此等级 |

每项发现必须分开写明：`FACT`（直接观察）、`INFERENCE`（从事实推导）、`INTENT`（是否能判断主观故意）。没有意图证据时，结论必须停留在流程失控、结果无效或记录不实，不能写成“作者造假”。

## 2. 审查范围、证据面与局限

### 2.1 已检查的证据

- W1 当前 265 个 baseline JSON、8 个 `.broken` 侧车文件、65 个重抽样 manifest 及相关汇总。
- W1 主 ASR best-of-N 工件 `_repro/asr_bon_llamacpp_snr5.json`，包括 144 个行级样本、候选、参考答案和各 N 指标。
- W4 三个提交 JSON：emotion paired-v2、MInDS14 tool-intent、paralinguistic negative probe。
- W1/W4 相关脚本、当前论文草稿、Wiki 结论/勘误、Git 提交历史和本地 MLflow 元数据。
- Step-2 RAG runner 的实际实现状态，以及 W2/W3 当前骨架状态。
- E 盘可访问的对应工件副本和 MInDS 本地 report，用于哈希与数值交叉核对。

### 2.2 本次没有做、因此不能声称的事情

- 没有访谈实验操作者，不能判断其主观意图。
- 没有访问所有历史 shell history、GPU 监控、模型缓存和被删除文件，不能排除未记录运行。
- 没有从零下载模型和数据重跑全部实验，不能把“内部一致”误写成“独立复现”。
- 没有审计第三方数据集自身的标签真实性或许可链。
- 没有修改或“修好”任何工件；本报告针对审计时实际存在的研究记录。

因此，“未发现造假直接证据”只是**当前证据下的未证实**，绝不是“已证明没有造假”。

## 3. 当前实验进度的真实状态

项目的研究叙事明显领先于可审计证据：

| 工作 | 实际成熟度 | 法证判断 |
|---|---|---|
| W1 | 有较成熟 baseline 与 best-of-N 原始池；仍在修复数据重叠和指标问题 | 有可复算基础，但没有形成完全冻结、独立 held-out 的发表级记录 |
| W4 | 只有 3 个提交摘要工件，部分本地原始 report 未提交；关键主张多为负结果或混杂结果 | “disentanglement 已成立”不成立；最多是若干探针和机制候选 |
| W2 | skeleton | 尚无可审计的完整研究结果 |
| W3 | skeleton | 尚无可审计的完整研究结果 |
| Step-2 Phase-A | runner 明示为 PLAN ONLY / mock，真实执行入口抛出 `NotImplementedError` | 不得描述为“实验已运行”或“进入验证” |
| 理论 | 存在 sorry-free 的局部 Gibbs/收敛引理，也存在与实际硬 BoN 操作符脱节的问题 | 不能宣称已对实际工程算法完成闭环证明 |

如果任何总结把上述状态写成“四项研究已得到实验证实”或“旗舰方法已完成有效验证”，都属于对进度的实质性夸大。

## 4. 对抗轮次一：论断到工件的谱系审计

完整证据链至少应是：

`CLAIM → frozen protocol → code commit → input manifest → raw row-level output → deterministic summary → statistical test → paper sentence`

当前链条的主要断点：

### INT-001：MInDS 提交摘要不是所指脚本的直接产物

- `FACT`：`scripts/repro_minds14_toolintent.py` 在 E 盘写出 `report_naive.json`、`report_rawschema.json`、`report_policy.json` 并打印统计量；它不直接生成提交的 `_repro/minds14_toolintent_paired.json`。
- `FACT`：提交 JSON 只有汇总，没有 182 条行级预测和相应输入卡片。
- `FACT`：本地被忽略的三个 report 能复核提交摘要中的主要数值，因此没有发现数值凭空编造。
- `INFERENCE`：提交工件经过人工转录/组装，缺少程序化 provenance；未来无法判断某次改动来自重跑、重算还是手工编辑。
- `INTENT`：无法判断故意欺骗。
- `LEVEL`：IR-4，因为“被称为可复现的最终工件无法由引用脚本直接生成”是正式调查触发器。
- `DISPOSITION`：数值暂记为 `NUMERICALLY REPRODUCED / PROVENANCE FAILED / CAUSAL CLAIM INVALID`。

### INT-002：W4 emotion 置信区间曾由手工写入，后续才脚本化

- `FACT`：Git 历史显示某次提交手工加入 headline t-CI；后续提交明确承认这一点，修改脚本使其正式输出，并在 GPU 重跑后得到相同数值。
- `INFERENCE`：最终数值目前有脚本支持，但原流程允许人手把推断统计量插入“实验工件”，缺少防篡改边界。
- `INTENT`：后续主动说明和重跑更支持“流程不严谨后被纠正”，不支持当前直接认定 falsification。
- `LEVEL`：IR-2；若原始重跑日志、commit 对应输入或输出不存在，则升级 IR-4。

### INT-003：W1 K8 的原位重评分破坏了 append-only 语义

- `FACT`：60 个 K8 cell 因 metric bug 被原位 rescored；原 aggregate 被保留，Git 历史仍可找到旧版本。
- `INFERENCE`：研究者能从 Git 追溯变化，但当前路径不再是原始工件，自动化消费者无法仅靠文件名区分 raw、invalid 和 rescored。
- `INTENT`：重评分原因被披露，没有发现隐匿负结果的直接证据。
- `LEVEL`：IR-2。
- `REQUIRED`：未来重算必须生成新 immutable artifact ID，旧工件机器标记 `superseded`，禁止覆盖。

### INT-004：大量精确数字只有文档摘要，不能独立复算

- `FACT`：W4 文档包含 URO、CoVoST2、HeySQuAD 等多项精确结果；提交区没有相应的行级预测、输入 manifest 和 deterministic summary bundle。
- `INFERENCE`：不能因为数字“看起来合理”就把它们纳入可发表证据；也不能因为原始数据缺失就断言它们被捏造。
- `LEVEL`：IR-1 至 IR-4，取决于在证据冻结请求后能否提供原始包。
- `DISPOSITION`：`UNVERIFIED — EXCLUDE FROM CLAIMS`。

ACM 的 artifact 标准要求工件有文档、保持一致、完整、可执行；“结果已验证”还要求独立团队复现主要结果。[ACM Artifact Review and Badging](https://www.acm.org/publications/policies/artifact-review-and-badging-current) 当前提交物达不到这一标准。

## 5. 对抗轮次二：已确认的泄漏与无效阳性

### INT-005：M3 的 +22.4% 是真值转写注入产生的伪机制阳性

- `FACT`：原 `_repro/m3_crossmodal.json` 的实验路径包含 ground-truth transcript injection。
- `FACT`：后续 Wiki 已把 +22.4% 结论撤回，明确其为输入泄漏。
- `FACT`：原 JSON 本身没有 `status: invalid`、`retracted_on` 或 `superseded_by`；相关文档 frontmatter 中仍保留旧阳性 verdict。
- `INFERENCE`：原实验没有证明模型内部跨模态知识被训练无关地激活，只证明了把答案相关文本送入系统能提高任务表现。
- `INTENT`：后续撤回反对“持续隐瞒”的推断，但原工件仍可被 AI 误选为有效证据。
- `LEVEL`：主张 IR-3；治理 IR-4。
- `DISPOSITION`：`INVALID — INPUT LEAKAGE — DO NOT CITE`。

### INT-006：T7 RAG 的 +0.517 主要是答案查表，不是干净检索增益

- `FACT`：T7 原工件声称“answers never injected”，报告 base 0.283、inject-k 0.767、oracle 0.800，H0 增量 +0.517。
- `FACT`：后续 errata 承认知识库自身 passage 几乎总含 gold answer，top-k 中答案包含率约 0.9，query 使用 gold question text。
- `FACT`：T8 clean rerun 在 answer-scrub 条件下得到 base 0.283、inject 0.217、oracle 0.300，干净 H0 增量 -0.066，区间覆盖 0；同时 lookup component 约 0.516。
- `INFERENCE`：T7 阳性几乎完全可由答案泄漏解释；其边界句在信息层面是错误的。
- `INTENT`：有更正记录，但仅凭现有材料不能判断最初陈述是疏忽、鲁莽还是明知。
- `LEVEL`：主张 IR-3；错误边界陈述与原工件未作废构成 IR-4 调查触发器。
- `DISPOSITION`：`INVALID — ANSWER LOOKUP — SUPERSEDED BY T8`。

### INT-007：MInDS policy card 是从评估集自身构建的 transductive 条件

- `FACT`：182 个评估样本中，每类前 3 条 transcript 被用于构建该类 candidate description。
- `FACT`：42 条评估记录是直接 exemplar；另有 1 条查询因文本重复而与正确卡片内容完全相同。
- `FACT`：复算得到 naive 0.7198、raw-schema 0.8571、policy 0.9835；policy 相对 raw-schema 为 +0.1264。排除直接 exemplar 后，policy 仍为 0.9786、raw-schema 为 0.8429，差值仍存在。
- `INFERENCE`：数值不是纯粹由 42 条直接记忆解释，但 candidate cards 仍由整个评估分布的标注样本构建；同时 instruction wording、schema 与 card content 多因素共同变化，不能把增益归因于 reward-guided policy。每类 3 个 support example 直接否定了 `zero-shot` 标签。
- `INTENT`：当前论文已承认 reward 仅作评估，这是减轻因素；但仍把该设置称为 zero-shot 是事实性错误。现有材料不支持进一步判断其是否故意。
- `LEVEL`：原“REAL verifiable-reward selection”机制主张 IR-3；数值本身 IR-1/IR-2。
- `DISPOSITION`：`ACCURACY REPRODUCED — HELD-OUT AND CAUSAL CLAIMS REJECTED`。

这三起事件不是孤立的“统计噪声”，而是共同指向边界审查失败：输入中是否出现答案相关信息、用于构建策略的样本是否来自评估集、系统究竟优化了什么对象，没有在运行前被强制验证。

## 6. 对抗轮次三：主 ASR 结果的统计复算

### 6.1 原始池真实性检查

- 提交工件与 E 盘副本 SHA-256 完全一致：`fb19fa67ef16083517260ff23aae59eeb9aebad44c9c8e3105e270c3692e4fc5`。
- 144 个 utterance ID 唯一；行级 candidate、reference、greedy 和每个 N 的数值都存在。
- 所有存储 summary 的宏平均数都能从行级数据精确复算。
- 未发现整包复制或汇总与行级数据矛盾。

因此该工件是目前证据链最强的一项；但它仍有会改变主要结论的统计问题。

### INT-008：论文把 macro utterance-WER 写成未加限定的 WER

对同一行级输出重新计算：

| 方法 | 存储的 macro utterance-WER | 标准 corpus WER | 相对 greedy 的 corpus-WER 变化 |
|---|---:|---:|---:|
| Greedy | 0.11834 | 0.09255 | — |
| Oracle best-of-8 | 0.07650 | 0.06290 | +0.02965 改善 |
| MBR-8 | 0.11466 | 0.09375 | -0.00120，即轻微变差 |

以 utterance 为配对重采样单位，10,000 次 bootstrap 的 corpus-WER 改善区间为：

- oracle-8：`+0.02965 [0.02104, 0.03898]`；oracle headroom 仍成立。
- MBR-8：`-0.00120 [-0.00781, 0.00550]`；部署式 MBR 没有增益证据。

进一步逐 N 复算显示，MBR-1 和 MBR-2 的 corpus-WER 相对 greedy **显著更差**，N=4、N=8 才是区间跨零；因此“MBR 在每个 N 都只是无显著差异”也不准确。oracle 只有 N=4、N=8 显示清晰正 headroom。

144 条 utterance 只来自 31 个 speaker、66 个 chapter；普通 row bootstrap 忽略了 speaker/chapter cluster。speaker-cluster 复算仍支持 oracle-8 headroom（约 `[0.0193, 0.0418]`），而 MBR-8 仍跨零（约 `[-0.0085, 0.0066]`），所以修正后的方向不依赖于仅一种 bootstrap 单位。

`FACT`：原 +0.0418 是等权宏平均短句/长句后的差值，不是把所有 edit 与 reference word 汇总后的 corpus WER。

`INFERENCE`：如果论文把它笼统称作 WER，读者会自然理解成 ASR 通行的 corpus WER，从而高估 oracle headroom，并误读 MBR 的方向。

`LEVEL`：IR-2；若在知悉口径差异后仍只报告有利的 macro 值，则升级为 IR-4。

`DISPOSITION`：oracle 改为 `SURVIVES WITH CORRECTED EFFECT SIZE`；MBR 改为 `NULL / SLIGHTLY NEGATIVE`。

NeurIPS checklist 要求误差条、统计检验和其计算方式被正确定义。[NeurIPS Paper Checklist](https://neurips.cc/public/guides/PaperChecklist) 此处不仅是命名瑕疵，因为结论方向对 MBR 发生变化。

### INT-009：“三代 generation seeds”同时更换了样本和噪声

- `FACT`：`load_utts(... seed=s)` 使用 seed 抽取不同的 48 条 utterance，并生成不同噪声；该 seed 还影响生成。
- `FACT`：三个 seed 的 greedy macro-WER 分别约 0.1577、0.1329、0.0644，差异远大于 MBR 的汇总效果。
- `INFERENCE`：三次运行不是对同一固定数据池的生成随机性重复，而是“数据抽样 + 噪声 + 生成”混合重复。
- `LEVEL`：把它陈述为 generation variance control 属 IR-2。
- `REQUIRED`：固定 utterance 和噪声实例后再变 generation seed；另用独立层次报告数据/噪声不确定性。

### INT-010：SNR=5 条件是为暴露 headroom 而选，缺少条件族

- `FACT`：当前只有 SNR=5 的主要提交工件；论文承认该条件是为产生可测 headroom 而选择。
- `INFERENCE`：这可以作为 Stage-1 stress test，但不能概括为自然分布或普遍改进；如果探索过多个 SNR 只报告最佳条件，则会构成选择性报告风险。
- `LEVEL`：现有披露下为 IR-1；若存在未披露的条件搜索，则升级 IR-4。
- `REQUIRED`：公开所有试过的 SNR/扰动/解码条件及搜索预算，预注册下一轮条件矩阵。

## 7. 对抗轮次四：重复、重叠与伪独立性

### INT-011：Wave-1 的 52/56 dev/test 重叠使“test”不再独立

- 旧报告已明确记录 56 个数据集视图中 52 个存在 dev/test 重叠。
- 当前 65 个重抽 manifest 报告已重抽为 disjoint，但仍在进行中的文件说明修复尚未形成完整冻结版。
- 已观察过或参与选择的旧 test 不能通过重新命名恢复为真正 untouched test；最多是新的内部验证集。
- 任何依赖旧 test 的模型/提示/方向选择都必须记录为 adaptive search，最终结论需在从未触碰的外部集上重新建立。

对测试集反复适配会造成隐性过拟合；相关研究显示，自适应使用 holdout 需要专门控制，而简单保留集并不能抵抗反复反馈。[Feldman & Steinke, 2017](https://proceedings.mlr.press/v65/feldman17a.html) 新测试集也可能揭示原测试上的适配效应。[Recht et al., 2019](https://proceedings.mlr.press/v97/recht19a.html)

`LEVEL`：旧独立 test 主张 IR-3；当前修复状态 IR-1。

### INT-012：CREMA-D 五个 seed 的 CI 把重叠样本当成近似独立重复

- emotion 五个 seed 的 test 子集两两重叠 48–64/300，dev 子集重叠 53–77/600。
- 五次运行还共享同一模型与数据总体；用 5 个 seed delta 作 t-CI 不能解释成五次独立实验。
- 全部 91 个 speaker 同时出现在 train/test；这适用于 closed-speaker 条件，但不支持 speaker-independent emotion generalization。
- 当前均值 +0.0367、CI `[-0.0430, 0.1163]` 本来就是 null；依赖性没有制造已报告显著阳性，但使区间的含义更弱。

`LEVEL`：IR-1；若把该 CI 宣称为独立重复或跨 speaker 泛化，则为 IR-2/IR-3。

### INT-013：paralinguistic probe 的“speaker near chance”表述没有统计支持

- speaker accuracy 0.0333，名义 chance 0.011，约为 chance 的 3 倍；emotion 为 0.4045，chance 0.1667。
- 没有行级预测和预注册的 equivalence/non-inferiority margin，因此“near chance”只是主观标签。
- 可允许的结论是“绝对 accuracy 很低”；不可允许的是“已证明 speaker 信息不存在”。

`LEVEL`：IR-2（措辞）；工件可复核性 IR-1。

## 8. 对抗轮次五：理论—实现对象不一致

### INT-014：普通 hard best-of-N 不是分布层面的 Gibbs tilt

当前叙事把 hard best-of-N 称为 Gibbs tilting `q*(y) ∝ q0(y) exp(R(y)/β)` 的“具体实现”，甚至说成对 sampled candidates 的 exact β→0 tilt。需要区分两个层次：

1. 对**已抽出的有限候选集**做 softmax，然后令 β→0，确实趋向候选集 argmax。
2. 从 `q0` 抽 N 个样本再取最大值所诱导的**输出分布**是 order-statistics best-of-N policy，并不一般等于固定 β 的 Gibbs/exponential tilt。

已有理论工作专门给出 best-of-N 的诱导策略与 KL 关系，而不是把它直接等同于 Gibbs tilt。[Beirami et al., 2024](https://arxiv.org/abs/2401.01879) Soft Best-of-N 的工作反而把“渐近收敛到 tilted distribution”作为 soft 版本相对普通 BoN 的性质。[Soft Best-of-N, 2025](https://arxiv.org/abs/2505.03156)

- `FACT`：现有 Lean load-bearing lemmas可对 Gibbs/约束对象建立局部性质，但没有证明 Python hard-BoN selector 的诱导分布就是同一对象。
- `FACT`：另一个 `BestOfN.lean` 文件中存在对 opaque functional 的命名 axiom；即使论文没有把它列为 load-bearing theorem，也说明实际桥接尚未机械证明。
- `INFERENCE`：当前形式化证明不能给实际 hard-BoN 实验背书；工程与理论不是同一个 operator。
- `INTENT`：这更像概念混同，现有证据不足以判断故意夸大。
- `LEVEL`：IR-2；若论文继续声称“实际算法已被 Lean 证明收敛”，则为 IR-3。
- `DISPOSITION`：`THEORY PARTIAL — IMPLEMENTATION PARITY NOT ESTABLISHED`。

## 9. 对抗轮次六：选择性报告与机器可读的“僵尸阳性”

最危险的不是人类是否能在长文末尾找到勘误，而是后续 AI 会如何读取这些记录。

当前存在以下结构性风险：

- M3、T7 的原始 JSON 仍是肯定式阳性，没有内嵌 `INVALID`/`SUPERSEDED` 状态。
- append-only 文档的 frontmatter `verdict` 仍可能保留被正文撤回的强阳性。
- 更正位于另一个 Markdown/errata 文件，自动消费者不会必然联结。
- “REAL”“PASSED”“proof”“genuine”等强词与 `directional-only` disclaimer 同时存在；机器常优先抽取强结论。
- 没有中央 claim ledger，无法从 `CLAIM_ID` 查询工件哈希、当前有效性、替代版本、统计口径和责任人。
- 没有完整记录尝试过的条件、失败运行、提示搜索和选择理由，无法排除 garden-of-forking-paths。

这会产生一种**研究记录层面的假象**：已经撤回的结果仍在结构上与有效结果等权，甚至更容易被检索。这不等同于已证明 falsification，但属于必须立刻修复的科研治理缺陷。

### INT-015：MLflow 能证明“记录过指标”，不能闭合输入到论文的证据链

- `FACT`：本地 MLflow 共见 14 个 run，13 个 finished、1 个 failed；保留 failed run 是反对“只保留成功记录”推断的有利证据。
- `FACT`：一个 run 的 `end_time - start_time` 为约 `-1486 ms`；另有多次 `18–170 ms` 的 finished run。超短 run 与已缓存 embedding 后只计算/记录指标相容，但没有显式记录 cache input hash；负时长是必须解释的 metadata anomaly。
- `FACT`：部分 run 带 `mlflow.source.git.commit`，但 summary JSON 没有反向链接 run ID，多数 run 也未保存行级预测 artifact。
- `INFERENCE`：目前 Git、MLflow、E 盘数据与论文是四个弱连接的证据岛。异常时间本身不是伪造证据，但会阻止审计者把 run metadata 当作完整执行证明。
- `INTENT`：无法判断，也没有证据支持把时钟/缓存异常直接说成伪造运行。
- `LEVEL`：IR-1/IR-2；若输入、缓存和时间线无法解释，或结果在声称运行前已存在且无合理迁移记录，则升级 IR-4。
- `REQUIRED`：建立 `run_id → git commit → input/cache manifest hash → raw output hash → summary hash → CLAIM_ID` 的不可变映射。

## 10. 是否有“作假”的正反证据

### 10.1 提高怀疑等级的证据

1. 多次出现会制造巨大阳性的边界失败：ground-truth transcript、gold question、answer-bearing KB、eval-built cards。
2. 原工件中出现“answers never injected”等与信息流事实不一致的强边界陈述。
3. 至少一次 inferential statistic 先由人手写入工件，后续才补脚本。
4. 多项摘要工件缺行级输出，或不能由所指脚本一键生成。
5. WER 口径和 seed 语义足以改变 deployable 结论，却没有在 headline 处充分说明。
6. 原位重评分与分散勘误使历史版本和当前版本的身份不清。
7. 旧 test 被大量触碰，仍存在把内部适配结果误当 held-out 证据的风险。

这些事实足以认定**系统性控制失效已经发生，重大鲁莽的风险很高**，也足以启动正式的内部研究诚信核查；是否达到“鲁莽”这一主观状态，仍须由独立调查依据知情时间线裁定。

### 10.2 反对当前直接认定造假的证据

1. 主 ASR 行级数据、摘要和两个存储位置的哈希一致，且数值可复算。
2. 265 个 baseline JSON 没有整包重复；运行时间总体合理，保留了错误行和 8 个 broken sidecar。
3. M3、T7、emotion 旧阳性后来被明确纠正，而不是从历史中删除。
4. 负结果被保留：emotion CI 跨零、MBR 无益、T8 clean RAG 无益。
5. 手工 emotion CI 后续由脚本重跑得到相同结果。
6. MInDS 本地原始 report 能支持提交摘要的数值，尽管提交链不合格。

这些证据说明“当前记录存在严重问题”与“数据必然由人编造”不是同一句话。严厉审查必须保持这一区分，否则报告自身也不诚信。

## 11. 当前主要主张的强制裁决表

| CLAIM_ID | 主张 | 当前裁决 | 可否继续引用 |
|---|---|---|---|
| C-ASR-ORACLE | SNR=5 下 BoN oracle 有 headroom | `SURVIVES-WITH-CORRECTION`：corpus-WER +0.02965，CI 为正；仅限所测条件 | 可，但必须改效应量、条件与 oracle 标签 |
| C-ASR-MBR | MBR-8 提高 WER | `REJECTED/NULL`：corpus-WER 轻微变差，CI 跨零 | 不可作为阳性 |
| C-ASR-SEEDS | 三代 generation seeds 证明生成稳定性 | `REJECTED`：样本、噪声、生成同时变化 | 不可 |
| C-W4-EMO | W4 emotion selection 有稳定改善 | `NO EVIDENCE OF IMPROVEMENT`：五次依赖运行未拒绝 0；现有 t-CI 不能解释成独立重复，也不能证明等价于 0 | 不可作为已证实阳性 |
| C-W4-PARA | 表征无 speaker 信息 | `NOT ESTABLISHED` | 不可；只能说该 probe 绝对表现低 |
| C-MINDS-POLICY | zero-shot reward-guided policy 带来 +12.6pp | `NOT ZERO-SHOT / CAUSALLY INVALID / CONFOUNDED`；固定 3-shot/class support 条件下的 accuracy 数值可复算 | 不可作机制或 held-out 证据 |
| C-M3 | 跨模态激活 +22.4% | `INVALID — INPUT LEAKAGE` | 绝对禁止 |
| C-T7 | RAG 注入带来 +51.7pp 干净增益 | `INVALID — ANSWER LOOKUP` | 绝对禁止 |
| C-W4-DISENTANGLE | frozen omni embedding 已被训练无关 RL 解耦 | `NOT ESTABLISHED` | 不可 |
| C-BASELINES | Wave-1/2 是独立 test 比较 | `DIRECTIONAL ONLY / REDRAW PENDING` | 不可作最终比较 |
| C-PHASEA | Step-2 Phase-A 已开始实证 | `NOT EXECUTED` | 不可 |
| C-THEORY | Lean 已证明实际 hard-BoN operator 收敛 | `NOT ESTABLISHED` | 不可 |

## 12. 必须立即执行的 STOP-THE-LINE 方案

以下是给项目所有者和后续 AI 的 proposal，不是建议性的美化清单，而是恢复可信度的最低门槛。

### G0 — 证据冻结（24 小时内）

**目的：** 防止善意清理、自动重算或覆盖进一步破坏证据链。

- 对所有 `_repro`、MLflow、E 盘 raw report、日志、配置快照、模型清单和 Git 状态生成只读 inventory。
- 每个文件记录 SHA-256、size、mtime、来源机器、生成命令、代码 commit、数据 manifest hash、模型 revision/hash、推理引擎版本。
- 禁止覆盖、删除、重命名或“补齐”旧工件；任何修复写入全新 artifact ID。
- 保存失败运行、broken 文件和已知负结果；不得只冻结成功运行。
- 建立访问日志；证据冻结后的任何变更必须有责任人、原因和新哈希。

**通过标准：** 独立审计者能从 inventory 定位每个 headline 数字的原始行级输出；缺失项显式记为 `MISSING`，而不是用文档解释代替。

### G1 — 中央 claim ledger 与无效工件隔离（48 小时内）

每条主张必须有：

```yaml
claim_id: C-...
claim_text: ...
status: valid | directional | null | invalid | unverified
stage: 1 | 2 | 3
artifact_sha256: ...
code_commit: ...
data_manifest_sha256: ...
metric_definition: ...
primary_or_secondary: ...
supersedes: ...
superseded_by: ...
invalid_reason: ...
owner: ...
reviewer: ...
adjudicated_on: YYYY-MM-DD
```

- M3 和 T7 原工件必须在 ledger 中标成 `invalid`，并明确链接更正；保留原文件但禁止被默认索引为正证据。
- frontmatter 中的陈旧 verdict 必须通过附加状态层覆盖，而不是静默重写历史。
- 所有精确数字若没有 artifact hash，状态一律 `unverified`。

**通过标准：** 给后续 AI 任意一个旧 JSON，它能机器判定该结果是否仍有效、由什么替代。

### G2 — 独立复现包（72 小时至 2 周）

- 由未参与原实验的人或隔离 agent，从 frozen manifest 运行。
- 脚本直接生成最终提交 JSON；禁止复制终端输出到摘要。
- summary 必须由 row-level artifact deterministic 生成，并在 CI 中重新计算后 byte/semantic compare。
- 运行环境固定，输出 software bill of materials；模型和数据使用不可变 revision。
- 两位 reviewer 分别签署“数值复算”和“信息边界”检查。

**通过标准：** 独立运行可以重建主表，且无人工修改最终统计字段。

### G3 — 泄漏红队门（所有新实验运行前）

每个实验必须画出信息流，逐项自动检测：

- 输入/检索库/提示/候选卡是否含 gold label、reference transcript、gold answer、question paraphrase 或可唯一定位答案的 ID。
- policy/card/index 是否使用 eval/test 样本构建。
- train/dev/test 是否按 speaker、session、source、utterance、文本近重复和语义近重复隔离。
- oracle 是否只用于上界，不进入任何可部署结果。
- 从哪个输入能“查表”得到答案；若可以，建立 scrubbed counterfactual。

**通过标准：** 先让攻击者尝试仅凭泄漏特征完成任务；攻击 baseline 不能解释主效果。

### G4 — 统计与选择性报告门

- ASR primary metric 固定为 corpus WER；macro utterance-WER 只能作 secondary，并明确命名。
- 固定 utterance 与 noise 后改变 generation seed；数据、噪声和生成层分别建模。
- 重叠数据使用 cluster/hierarchical bootstrap，不能把 seed 当独立样本。
- 预注册 primary outcome、方向、停止规则、排除规则、候选 N、SNR 和所有条件。
- 报告完整 search budget、全部条件和全部失败/负结果；不能只报告最佳 seed、最佳层、最佳 SNR。
- 效应量、95% CI 和 multiplicity correction 必须与 hypothesis family 对齐。

**通过标准：** reviewer 在不知道结果方向时也会批准同一分析方案。

### G5 — 三个关键清洁重做

#### G5.1 ASR

- 从未触碰的 utterance pool 固定一组 evaluation IDs。
- 至少覆盖 clean 与多个预注册 SNR；同一噪声实例用于候选方法配对。
- 分开报告 oracle headroom 与 deployable selector；后者必须是主结果。
- 以 corpus WER 为 primary，层次 bootstrap 同时覆盖 utterance 与 generation randomness。
- 加入等计算量 baseline、随机选择、长度/置信度 heuristic，以及 reward misspecification stress test。

#### G5.2 MInDS

- candidate cards 只从 train split 构建，eval 完全不参与。
- zero-shot arm 严禁 examples；few-shot arm 必须明确命名并固定 support manifest/hash。
- 做 2×2 或更完整 factorial：instruction wording × schema × card content × selector。
- 对 direct exemplar、duplicate transcript、near duplicate 单独审计并预注册排除。
- 先比较 fixed policy，再测试 reward-guided selection；没有 selection 就不得叫 RL。

#### G5.3 RAG/跨模态

- query 只能由允许的 audio/model output 产生，禁止 gold question/transcript。
- KB 与 eval source disjoint；建立答案 scrubbed 与 adversarial distractor 版本。
- 分解 retrieval recall、answer inclusion、reader accuracy 与 end-to-end gain。
- 任何“注入无答案”的边界必须由自动 answer-string/semantic leakage scan 证明。

### G6 — 理论与实现同对象门

- 给实际 Python selector 一个精确定义并在 Lean 中形式化同一个 operator。
- 分别证明普通 BoN 诱导分布、soft-BoN/Gibbs 关系和约束收敛；不能用命名相似替代等价证明。
- 所有 load-bearing theorem 必须 `#print axioms` 审计；不允许 opaque axiom 承担结论。
- 建立 executable conformance tests：小型有限空间中 Python 输出与 Lean 定义逐例一致。
- 按项目既定理论要求，同时给无约束不收敛反例与约束版本收敛证明。

**通过标准：** 论文中每个理论句能指向具体 theorem；每个 theorem 能指向实际运行的工程对象。

### G7 — Owner 裁决门

Stage 1 不能自动滚入 Stage 2。所有红项关闭后，由 owner 明确裁决：

1. 哪个问题仍值得进入 Stage 2；
2. 哪些旧数据只作 hypothesis-generation，永不用于 confirmatory evidence；
3. 哪个全新 holdout 永久冻结；
4. 谁负责独立复现，谁负责研究诚信签字；
5. 若复现失败，是否撤回相应论文主张。

## 13. 正式诚信调查的升级触发器

出现以下任一情况，不再只按“方法学修复”处理，应交由不参与项目的负责人进行正式 inquiry：

1. 被要求后无法提供某个 headline 数字的原始行级输出，且没有预先记录的合理原因。
2. 提交工件哈希与声称的冻结副本不一致，且变更未进入 append-only ledger。
3. 所指脚本无法产生工件，当事人也不能提供完整人工转换记录。
4. 发现知悉泄漏/口径错误后仍继续引用旧阳性，或删除/隐藏相反运行。
5. 完整实验搜索显示只保留最有利 seed、层、SNR、prompt 或 metric，而论文声称方案是预先指定的。
6. 运行时间、样本 ID、日志、GPU 记录或模型输出之间出现无法解释的物理/时间矛盾。
7. 独立重跑在相同冻结输入上无法接近原始结果，并发现原工件包含无法由代码路径产生的字段或样本。
8. 当事人拒绝证据冻结、要求覆盖旧文件或阻止独立审计。

只有调查能进一步判断这些行为是诚实错误、重大鲁莽，还是故意/明知的 fabrication/falsification。项目内的同一个 AI 不应同时充当实验者、审计者和最终裁决者。

## 14. 多轮对抗后的最低研究 proposal

如果项目希望从此次危机中提出一个真正有研究价值的方向，proposal 不应是“继续提高一个数字”，而应把**无泄漏、可部署、可证伪的训练无关推理优化**定义成研究对象：

> 在完全冻结模型、完全冻结且无答案泄漏的外部评估集上，给定固定推理预算，能否用只依赖部署时可得信号的 selector，在跨数据集、跨噪声、跨说话人条件下稳定优于 greedy 和等预算 baseline；并且 selector 的工程更新规则与形式理论中的受约束算子严格一致？

预注册的核心检查点：

- **CP-1 信息边界：** selector 的每个输入在部署时可得，gold 只进入离线评分器。
- **CP-2 可部署性：** oracle 只定义 headroom；论文主结论来自 deployable selector。
- **CP-3 独立性：** policy construction、prompt selection、threshold tuning 与最终 test 完全隔离。
- **CP-4 机制识别：** factorial ablation 能区分“更多文本/更好 prompt”与“reward-guided selection”。
- **CP-5 稳健性：** 同一预注册方法跨 clean/SNR/domain/speaker shift 报告，不允许按条件换方法。
- **CP-6 负对照：** random reward、shuffled reward、leakage-only、length heuristic、confidence heuristic 和等计算量 sampling。
- **CP-7 统计：** corpus-level primary、paired hierarchical CI、family-wise correction、完整 search budget。
- **CP-8 证据链：** 一条命令从 immutable raw outputs 生成全部主表；独立 reviewer 复算。
- **CP-9 理论同构：** Python selector 与 Lean operator 逐例一致；无约束失败与约束收敛都被证明。
- **CP-10 失败准则：** deployable selector 若在预注册主任务族上不能稳定超过等预算 baseline，则停止声称“RL 激活了预训练知识”，转而报告负结果或缩小问题。

这比继续围绕已有阳性补实验更严格，因为它允许并欢迎核心 thesis 被证伪。

## 15. 给后续 AI 的机器可读裁决

```yaml
audit_id: RIA-2026-07-10
audit_type: read_only_forensic_research_integrity
global_status: STOP_THE_LINE
fraud_finding:
  fabrication: NOT_ESTABLISHED
  falsification: NOT_ESTABLISHED
  intent: UNDETERMINED
publication_readiness: FAIL
systemic_control_failure: CONFIRMED
confirmed_invalid_claims:
  - claim_id: C-M3
    reason: ground_truth_transcript_leakage
    severity: IR-3
  - claim_id: C-T7
    reason: answer_bearing_KB_and_gold_question_lookup
    severity: IR-3
rejected_or_corrected_claims:
  - claim_id: C-ASR-MBR
    status: NULL_OR_SLIGHTLY_NEGATIVE_ON_CORPUS_WER
  - claim_id: C-ASR-SEEDS
    status: REJECTED_SEED_CONFLATES_DATA_NOISE_GENERATION
  - claim_id: C-MINDS-POLICY
    status: CAUSALLY_INVALID_TRANSDUCTIVE_AND_CONFOUNDED
  - claim_id: C-THEORY
    status: IMPLEMENTATION_PARITY_NOT_ESTABLISHED
surviving_claims:
  - claim_id: C-ASR-ORACLE
    status: SURVIVES_WITH_CORRECTED_EFFECT_SIZE_AND_STRICT_SCOPE
    corpus_wer_reduction: 0.0296474
    bootstrap_95ci: [0.02104, 0.03898]
mandatory_gates:
  - G0_EVIDENCE_FREEZE
  - G1_CLAIM_LEDGER
  - G2_INDEPENDENT_REPRODUCTION
  - G3_LEAKAGE_RED_TEAM
  - G4_PREREGISTERED_STATISTICS
  - G5_CLEAN_RERUNS
  - G6_THEORY_IMPLEMENTATION_PARITY
  - G7_OWNER_ADJUDICATION
prohibited_actions:
  - cite_M3_or_T7_as_positive_evidence
  - call_MInDS_result_reward_guided_RL
  - call_MInDS_three_examples_per_class_zero_shot
  - call_three_ASR_runs_generation_seed_replications
  - report_macro_utterance_WER_as_unqualified_WER
  - claim_actual_hard_BoN_is_Lean_proven_Gibbs_operator
  - overwrite_or_delete_historical_artifacts
next_state_allowed_only_if: all_mandatory_gates_have_independent_signed_evidence
```

## 16. 外部标准与方法学依据

- 研究不端的定义与证据边界：[ORI Definition](https://ori.hhs.gov/definition-research-misconduct)、[42 CFR Part 93](https://www.govinfo.gov/link/cfr/42/93?link-type=pdf&year=mostrecent)、[ORI Final Rule Guidance](https://ori.hhs.gov/sites/default/files/2025-06/Implementing%20the%20Final%20Rule_final.pdf)。
- 可复现性与研究可靠性：Pineau 等指出，可复现性是验证研究可靠性的必要条件，并系统推动代码、checklist 和结果披露。[Improving Reproducibility in Machine Learning Research, JMLR 2021](https://www.jmlr.org/papers/v22/20-303.html)
- 完整报告超参数、数据划分、随机种子和训练预算有助于揭示隐藏方差与选择偏差：[Dodge et al., Show Your Work](https://arxiv.org/abs/1909.03004)。
- 工件完整性和独立结果验证：[ACM Artifact Review and Badging](https://www.acm.org/publications/policies/artifact-review-and-badging-current)。
- 统计报告要求：[NeurIPS Paper Checklist](https://neurips.cc/public/guides/PaperChecklist)。
- 测试集复用和自适应 holdout 风险：[Feldman & Steinke, 2017](https://proceedings.mlr.press/v65/feldman17a.html)、[Recht et al., 2019](https://proceedings.mlr.press/v97/recht19a)。
- BoN 与 tilt 的理论区分：[Beirami et al., 2024](https://arxiv.org/abs/2401.01879)、[Soft Best-of-N, 2025](https://arxiv.org/abs/2505.03156)。
- 调查中的期刊—机构协作原则：[COPE guidance on research integrity cases](https://pmc.ncbi.nlm.nih.gov/articles/PMC3385259/)。

## 17. 最终裁决

当前最严格、也最诚实的说法是：

> **没有证据足以宣布“团队已经学术造假”；但已有充分证据宣布“当前研究记录失去发表级可信度”。** 两个重大阳性已被证实来自泄漏，若干其余结果存在统计口径、伪独立、transductive construction、手工谱系和理论对象错配。项目现在需要的不是更多漂亮数字，而是停止线、证据冻结、机器可读撤回、独立复现和一个允许核心 thesis 失败的预注册实验。

在这些门槛关闭之前，任何把当前结果包装成“已证明训练无关 RL 激活了 omni 模型潜在知识”的行为，都不符合现有证据。
