---
artifact_id: "SF-S1-C4B-P0R9-DOCTORAL-ADVERSARIAL-REVIEW-2026-07-18-01"
title: "Gate S1 Correction #4B / P0-R9：Stage-1A 阶段校准与博士生导师式对抗复审"
date: 2026-07-18
reviewer_role: "严格审稿人 / 博士生导师 / 研究诚信审计视角"
review_scope: "Stage-1A survey-ready gate、Correction #4B 回应件、机器门禁、近期全文与引文校准交付"
signature_object_commit: "9b1f00be0cbebab51b2e6a9e4ea2e02d024565ce"
post_signature_evidence_commit: "2b4ec3de486d333cc2d2064f8daed7275a59a81a"
response_blob: "f80e70a66f9fd553c529eeee317111a2a37fab88"
response_sha256: "24f5d5715a77ff1f44853163c10d40a06b44d86d7933ee136b6fd88b64a3f7da"
verdict: "WITHHOLD — 1 项 Gate 阻断 MAJOR；另有 1 项 Stage-1A close 前 MAJOR、3 项 MINOR"
integrity_ruling: "未发现足以认定 FFP 的证据；当前原始元数据与全文抽查一致，存在的是正常研究流程中的覆盖缺口和完成态措辞过强"
mutation_policy: "所有对抗变异仅在 git archive 临时副本执行；未修改研究团队源文件或既有交付物"
---

# Gate S1 Correction #4B / P0-R9：Stage-1A 阶段校准与博士生导师式对抗复审

## 0. 一页裁决

### 0.1 当前到底处于哪个阶段

当前不是“Stage-1A 正式启动之前”，也不是 Stage-1B。更精确的定位是：

> **Stage-1A 已启动并处于 survey-ready gate；系统性 mapping 的 discovery query 尚未执行，
> 但已发生定向 ID dereference、全文抓取、哨兵构造和一次引文校准；Stage-1B 的模型/数据实验尚未放行。**

依据如下：

1. `wiki/Research-Objective.md` 仍把正典状态写为 “Stage-1A 收官准备末段
   （survey-ready gate）”，并明确 Stage-1B 未放行；
2. Correction #4B 声明 `discovery_queries_executed = 0`，本轮也未发现真实 mapping 查询、模型
   推理或数据集实验已经启动；
3. 但 26 篇哨兵的 raw Atom、PDF/e-print 抓取及 Seg-Agent 引文校准已经执行，因此“外部证据
   工作尚未开始”已不再是准确的全称陈述。

这一区分很重要：本轮不能用成型论文的结果标准要求团队，也不应设置 Stage-2 式预算 cap；但
Stage-1A 的任务正是把问题空间、邻近工作、检索协议和证据链做成可信的研究基础，因此**发现
机制的概念盲区恰恰属于本阶段的核心失败，而不是可以留到以后再修的美化项**。相反，面对恶意
篡改输入的安全鲁棒性不是本阶段的主要任务；只要脚本在约定的正确输入和正确操作流程下可靠
完成任务，就不应因缺少防攻击能力而拒签。

### 0.2 最终决定

**Gate S1 / P0-R9 暂不签署（WITHHOLD）。** 理由收敛为一个科学覆盖阻断项，而不是脚本防篡改：

| 等级 | 数量 | 裁决 |
|---|---:|---|
| Gate 阻断 MAJOR | 1 | 必须修复并进行一次新的窄幅复核 |
| Stage-1A close 前 MAJOR | 1 | 不必阻塞“开始 mapping”，但必须在 Stage-1A close 签字前关闭 |
| MINOR | 3 | 随下一批更正一并关闭，不得用散文说明代替机器可解引用记录 |

唯一 Gate 阻断问题是：查询设计仍在做“名称占位”而非“方法占位”，对七篇直接相关工作
确定性零命中，而且专门声称用于 L12 的 fresh held-out 并未命中 L12。其余脚本对抗性变异只
作为未来 hardening 建议，不再作为当前 Gate 结论。

另一个 Stage-1A close 前 MAJOR 是：Seg-Agent 的“引文交集为空”只检查了参考文献中可被正则
提取的 arXiv ID，却将结果升级成整个 bibliography 的交集结论。

### 0.3 研究诚信裁决

**本审查不认定团队实施了学术欺诈。** 我对当前 26 个 raw Atom 对象逐项核验，26/26 文件哈希、
题名和类别相符；对当前成功落盘的 50 个全文对象核验，文件存在、字节数和 SHA-256 相符。没有
证据表明团队虚构论文、伪造原始全文或篡改这些文件。

现阶段更准确的判断是：**没有 FFP 证据，也不应仅凭脚本缺少恶意输入防护就升级研究诚信指控。**
需要整改的是正常工作流中的可核验事实误述——例如引用校准把 arXiv-ID 子集说成完整 bibliography、
回应件给出的一个 `git diff` 预期与实际不符——以及检索方案的真实覆盖盲区。只有在发现真实数据
与来源不符、明知更正后仍重复发布虚假完成态，或隐藏正常流程中的失败记录时，才应升级正式研究
诚信调查。

## 1. 复核对象与证据冻结

### 1.1 签署对象

- Correction #4B 签署包：commit
  `9b1f00be0cbebab51b2e6a9e4ea2e02d024565ce`；
- 回应件：`wiki/survey/2026-07-17-gate-s1-correction-4b-response.md`；
- 回应件 git blob：`f80e70a66f9fd553c529eeee317111a2a37fab88`；
- 回应件 SHA-256：
  `24f5d5715a77ff1f44853163c10d40a06b44d86d7933ee136b6fd88b64a3f7da`；
- correction #4B 相对父提交的实际变更面：88 路径，分为 36 个普通文件、26 个
  `fixtures-c4b` 文件和 26 个 raw Atom XML；该数字与 manifest 的
  `MACHINE_COUNT files=36 fixtures=26 atom_xml=26` 相符。

### 1.2 当前交付增量

当前 HEAD `2b4ec3de486d333cc2d2064f8daed7275a59a81a` 在签署包之后增加了全文 ledger 重试记录。
这部分不是 P0-R9 原签署对象，但它已经是团队“近期正在处理的工作”，因此本审查只判断其是否
适合继续 Stage-1A，不把它倒灌成原 Gate 的完成证据。

### 1.3 审查纪律

1. 基线重放在两个独立 `git archive` 快照上进行，而非直接相信当前工作树；
2. 所有反事实变异只发生在临时副本；
3. 既有研究文件没有被修改；
4. 本报告只新增一个 dated review artifact。

## 2. 多轮对抗式评审记录

本轮不是“脚本能否运行”的单轮验收，而是按“声称 → oracle → 反事实 → 外部事实”的顺序执行
五轮对抗审查。

### Round 1：阶段与范围对抗

问题：团队是否偷偷进入 Stage-1B，或者评审是否反过来给 Stage-1A 设置了超前义务？

结论：

- 未发现模型加载、数据集推理、性能实验或 Stage-1B 方向性原型已经开始；
- fulltext 抓取、引用关系校准和 mapping 退出机制设计属于 Stage-1A 的调查基础设施，不属于
  越阶段实验；
- amendment-7 的 E1–E3 是执行合同设计，本身不构成 Stage-2 式预注册或预算 cap；
- 但“外部证据工作尚未开始”已经过期，应改成“系统性 mapping 查询尚未开始；定向证据准备已
  启动”。

### Round 2：干净快照基线重放

在 commit `9b1f00b` 和 `2b4ec3d` 两个隔离快照上，以下 9 个确定性入口均 exit 0，合计
18/18 次通过：

1. `sf_package_summary.py`；
2. `sf_package_summary_test.py`；
3. `sf_record_validator_test.py`；
4. `sf_t1_routes_adjudication_validate.py`；
5. `sf_sentinel_recall_test.py`；
6. `sf_query_compiler.py`；
7. `sf_child_query_replay_test.py`；
8. `sf_child_query_realrow_dryrun.py`；
9. `sf_t1_routes_validate.py`。

这证明团队确实修复了上一轮的一批浅层 false-green，也证明交付包不是“完全不可运行”。但此处
只能推出**当前已覆盖的 oracle 对当前输入通过**，不能推出 oracle 已覆盖其声称的语义。

`sf_citation_calibration.py` 在纯 git archive 中会因为 E: 数据盘的 e-print 不在 bundle 内而
报 `INPUT_MISSING`。因此它应标记为 **local-data replayable**，不得与上述
**bundle-only replayable** 入口混写。

### Round 3：机器门禁边界压力测试（不计入本轮 Gate）

我曾用伪造哨兵字段、语义相反路由和未申报批次文件做压力测试，现有脚本不会全部拦截。经阶段
校准，这类测试验证的是**面对恶意或违约输入的防护能力**，而当前脚本的合同是服务一个合作式、
按正确指令运行的研究流程，并非不可信输入边界。因此这些结果只进入 §9.4 的可选 hardening，
不构成 MAJOR、MINOR 或拒签依据。

本轮对脚本的实际要求只保留三点：正常输入下结果正确、同一冻结输入可回放、脚本的输出措辞不
超过它实际计算的量。当前 26 条哨兵元数据已经与 raw Atom 对齐，故不存在一个现实的元数据错误
需要以 Gate 方式追责。

### Round 4：外部事实与引用审查

对 raw Atom、全文 ledger、论文题录和官方页面进行外部核验。结果是：当前原始对象真实，但发现
机制存在确定性概念漏检；详见 §4 和 §5。

### Round 5：欺诈假设与替代解释对抗

我分别检验两种假设：

- H1：团队主动伪造了论文或全文；
- H2：团队真实采集了对象，但把“结构一致/部分标识符覆盖”误当成“事实正确/完整覆盖”。

现有证据支持 H2，不足以支持 H1。故不能指控 FFP；是否签署 Gate 应回到 survey 覆盖和正常
流程下的事实正确性，而不是以恶意篡改压力测试替代学术判断。

## 3. 做对了什么

严格评审不等于抹去已经完成的真实进步。本轮以下工作成立：

1. correction #4B 的实际路径计数与 manifest 机器计数一致，上一轮 31-vs-33 类人工计数错误在
   该层面已修正；
2. 61 条查询前 55 条的 SHA-256 与 canon 一致；
3. 两个冻结提交上的 18 次核心重放均成功；
4. 26 个 raw Atom 文件均存在且 SHA-256 与 ledger 一致；26/26 title、26/26 categories 与
   Atom 内容一致；18 个摘要可做空白归一化精确对齐，其余 8 个被团队如实标注为历史 abs-page
   归一化来源；
5. 当前 50 个成功全文文件的实际路径、字节数和 SHA-256 可核对，未发现文件内容伪造；
6. 团队主动披露 routes v2 中 ICASSP evidence tier 的错误，并用 v3 supersession 修正，而非
   静默改写历史文件；
7. 没有提前运行模型或 Stage-1B 性能实验。

这些事实足以否定“交付物整体是捏造的”这一极端判断，但不能抵消以下阻断项。

## 4. Gate 阻断 MAJOR

### MAJOR-G1：发现机制仍按术语召回，无法覆盖直接占据方法空间的工作

#### 事实

将以下七篇论文的官方 title/abstract/category 输入当前 61-query 离线 matcher，结果均为：
`query_hits = 0`，且不存在仅被 category 拦截的 term hit：

| 论文 | 与本项目的直接关系 | 当前结果 |
|---|---|---|
| [Training-Free Multimodal Large Language Model Orchestration](https://arxiv.org/abs/2508.10016) | training-free、多模型 orchestration、中央 controller、跨模态 memory、统一交互系统；直接占据 system-first 叙事 | 0 hit |
| [ThinkOmni: Lifting Textual Reasoning to Omni-modal Scenarios via Guidance Decoding](https://arxiv.org/abs/2602.23306) | training-free/data-free、冻结 OLLM、外部 LRM guide、stepwise contrastive scaling；直接触碰 omni 与外部控制边界 | 0 hit |
| [Limits and Gains of Test-Time Scaling in Vision-Language Reasoning](https://arxiv.org/abs/2512.11109) | 比较 open/closed VLM；报告 external verification 较稳，而 iterative refinement 可退化；直接关系到杠杆选择与负结果预期 | 0 hit |
| [Test-Time Scaling in Multimodal Foundation Models: A Comprehensive Survey of Generation and Reasoning](https://aclanthology.org/2026.findings-acl.383/) | 给出 sampling / feedback / search 三类统一地图；适合作为二级导航与参考文献普查入口 | 0 hit |
| [Test-Time Scaling for Small VLMs on Multilingual Visual MCQ](https://arxiv.org/abs/2607.09438) | 直接比较 self-consistency、PRM beam search、post-hoc selectors；报告 parseability/单链预算影响远大于增加 K，且 training-free critic 与 trained PRM 均未稳定胜过 majority vote | 0 hit |
| [On Test-Time Scaling for Vision-Language Models](https://arxiv.org/abs/2606.28864) | 9 种方法、多个模型规模和 6 个 benchmark；报告小而强的模型获益更大、过多 compute 可失焦、视觉信息集中在链早期 | 0 hit |
| [dMLLM-TTS: Self-Verified and Efficient Test-Time Scaling for Diffusion Multi-Modal Large Language Models](https://arxiv.org/abs/2512.19433) | trajectory exploration + iterative refinement + self-verified feedback；虽偏生成任务，但占据“内生 evaluator + search/refinement”机制位 | 0 hit |

这里必须作一项诚信上的精确区分：`Limits and Gains` 并非团队从未见过。它已经出现在
`wiki/survey/2026-07-04-stage1-X3-llm-vlm-testtime-map.md`，并被用于说明 open VLM 的 intrinsic
refinement 可能退化。问题是该已知证据没有进入当前 seed/sentinel/query gate。故它属于
**carriage failure（旧探索知识未迁移到当前正典）**；其余六篇在本轮检索的当前 gate 表面未见
登记，属于当前 coverage omission。两者都说明“旧散文里见过”不能替代冻结发现协议的知识承载。

前两篇尤其威胁 system-first 定位。MLLM Orchestration 并不依赖项目当前偏好的
reward/verifier/agentic 命名，仍然
实质实现了 training-free 的外部系统编排；ThinkOmni 使用另一个 LRM 作为 guide，恰好迫使项目
明确“激活冻结核心自身知识”和“从外部模型注入新信息”之间的边界。若发现协议只能在作者使用
`agent/reward/verifier` 等项目内词汇时找到工作，novelty survey 会产生系统性乐观偏差。

后三篇则直接威胁后续实验叙事：可能最大的增益来自输出可解析性、单链 token 预算或模型本身，
而非复杂 selector；也可能存在过度 compute 失焦、迭代 refinement 退化，以及 self-verification
只在特定生成任务成立。Stage-1A 不需要现在跑这些实验，但必须把这些替代解释和边界放进后续
Stage-1B 的探索空间。

#### 根因：把研究目标写成了检索前提

当前 L11–L13 的核心表达都强制出现 `agent OR agentic OR multi-agent`。这构成认识论循环：项目希望
论证“omni agentic system”是有价值的系统形态，却只系统发现已经用 agent 语言自我命名的工作。
然而 controller、orchestration、guidance decoding、post-hoc selector、self-verification、search
和 refinement 都可能实现同一控制功能而不使用 agent 标签。

因此，`agentic` 应是 screening/coding 后得到的架构属性，而不应是全部 multimodal test-time
optimization 发现通道的共同入场券。

#### 对项目创新定位的直接影响

这批遗漏不会否定项目，但会迫使创新表述从口号拆成可比较的结构：

1. **“构建 omni system”本身不能再暂定为第一创新点。** MLLM Orchestration 已明确提出
   training-free 的 omni-modal assistant、controller、cross-modal memory 和统一交互层。团队必须
   逐组件比较，不能只因对方没有使用 `agentic system` 这个名字就认为系统空间空白。
2. **“training-free 提升 omni model”也不是空白。** ThinkOmni 已提出 training-free/data-free
   的 omni reasoning 改进，但它借助外部 LRM guide；其与本项目“冻结黑盒自身知识激活”是否同类，
   取决于信息边界和模型访问权限，而不是 training-free 标签。
3. **“复杂 evaluator/selector 必然优于简单基线”没有文献先验。** Small-VLM TTS 表明，在其任务
   上先修复 parseability 和单链预算后，复杂搜索/critic/PRM 未胜 majority vote。项目后续必须把
   供给侧 `c`、候选池 headroom 和 selector 实现率分开，而不能把所有增益记给控制算法。
4. **更可信的潜在空白仍然存在，但尚待 survey 证明**：在不访问权重、hidden state 或 logits 的
   黑盒约束下，用统一外部控制平面跨模态/跨任务组织候选生成、label-free evaluator、选择、工具、
   记忆与停止，并在相同候选池上超过 MBR/majority 等强基线。这比“training-free + omni + agent”
   的词组新颖性更窄，却也更可证伪。

Stage-1A 的任务不是现在把第 4 点写成最终贡献，而是通过文献编码证明：哪些组件已被单点占据，
哪些组合尚未出现，哪些只是访问权限或信息来源不同。只有形成这一“组件 × 约束 × 任务域”矩阵，
system-first proposal 才能从愿景升级为有证据的研究缺口。

#### fresh held-out 证据也被说得过强

回应件把 2602.21497 称为 “L12 侧” fresh held-out，但实际只命中 `SF-L3-Q7`，不命中任何
L12 query；2605.11374 则确实命中 `SF-L13-Q2`。因此这对 fresh held-out 并没有对称验证 L12
和 L13。旧 held-out VQQA 确实碰巧命中 L12，但它不是这次 P0-3.4 声称的 fresh L12-side
检验；除非另做污染审计和角色重述，不能拿它无声替代本次预注册对象。

#### 为什么是 Gate 阻断，而不是“以后补七篇”

七篇论文尚未被 mapping 发现并不奇怪，因为 mapping 还没运行；真正的失败是**即使把官方元数据
送入现有发现规则，它们仍确定性漏掉**。如果现在放行，真实执行只会稳定复现这个概念盲区。

#### 必须怎样修

1. 新增“方法占位（method-occupation）”发现轴，不要求题名/摘要同时出现 agent、reward、
   verifier 等项目内命名；至少覆盖：
   - multimodal/omni + orchestration/controller/routing/composition；
   - multimodal/omni + guidance/contrastive decoding/external guide；
   - multimodal + test-time scaling + sampling/feedback/search/refinement/verification；
2. 七篇论文进入 seed/sentinel/registered-boundary 中的明确一类，而不是只写在回应散文中；
3. 对 MLLM Orchestration 和 ThinkOmni 做 D0/D1 级身份编码：冻结对象、是否改权重、是否引入
   外部模型、是否有 reward、是否有可部署 controller、信息边界；
4. 重新选择一个不参与词项设计、且**实际命中 L12** 的 fresh held-out；
5. 发现逻辑至少拆为两个正交轴，而不是继续堆 `agent` 同义词：
   - 系统对象轴：omni/multimodal/VLM/MLLM + controller/orchestration/guidance/interaction；
   - 优化机制轴：sampling/selection/verification/search/refinement/routing/scaling；
6. 在 screening/coding 阶段再编码 agentic/non-agentic、内部/外部 evaluator、read-out/new-info、
   logits/hidden-state/black-box access；
7. 证明旧 61-query 与新增 lane 的边界：新增 lane 是概念补漏，不得把 title 中的独特短语直接
   抄成单篇捕获器。

#### 验收

- 上述七篇全部得到非空、可解释的 discovery channel；
- 至少一个 fresh L12 held-out 通过 L12，而不是通过无关旧 lane；
- 至少再给一个同义表达负控，证明 query 不是把七个已知题名硬编码进去；
- 查询变更、反例来源、使用于设计/未使用于设计的身份全部机器可读。

## 5. Stage-1A close 前必须关闭的 MAJOR

### MAJOR-C1：Seg-Agent 引文校准把“arXiv-ID 子集为空”升级成“完整参考文献交集为空”

#### 事实

`sf_citation_calibration.py` 从 `.bbl/.bib/.tex` 中取文本，然后只用 arXiv ID 正则提取标识符。
产出记录为：约 59 个 bibliography entries，仅识别 30 个 arXiv IDs，随后将这 30 个 ID 与
99-item stock 求交，并给出 `PREDICTION_CONFIRMED`。

该实验实际支持的命题只能是：

> “在能从目标源文件中以当前正则识别出 arXiv ID 的 30 个引用里，与 stock 的 arXiv-ID
> 交集为空。”

它不能支持“约 59 个参考文献与 stock 的完整交集为空”，因为 DOI-only、venue-only、title-only、
旧式 arXiv 写法和解析失败项都没有被解决。简单的人工题名复核没有发现明显交集，是一个安慰性
检查，但不能修复 protocol 对标识符解析覆盖率的过度陈述。

#### 为什么不阻塞 mapping 开始，却阻塞 Stage-1A close

amendment-7 已把它定位为非 gate 的执行期合同，因此本项不倒灌成 P0-R9 签署义务；但如果团队
要用“引文闭包 K=2 收敛”作为 Stage-1A 退出条件，identifier resolution 必须先可靠，否则“闭包
干涸”可能只是解析器失明。

#### 必须怎样修

1. 每个 bibliography entry 先形成独立记录；
2. 依次解析 DOI、arXiv、ACL Anthology、OpenReview、title/year/first-author；
3. 报告 total / resolved / ambiguous / unresolved，而不是只报 arXiv-ID 数；
4. 交集结论同时给 identifier-level 与 work-level；
5. 预注册可接受的 unresolved 上限，超过则不得宣布 closure；
6. 将结果改名为 `ARXIV_ID_SUBSET_INTERSECTION_EMPTY`，直到完整 work resolution 完成。

#### 验收

- fixture 中同一篇论文分别以 arXiv、DOI、会议题名、轻微题名变体出现，均归一到同一 work；
- unresolved 项逐条可见；
- 把 stock 中一篇改成 DOI-only 引用时，系统必须检出交集；
- bundle-only 与 local-data replayability 明确分级。

## 6. MINOR

### MINOR-1：fulltext ledger 当前状态可验证，但 locator 和计数叙述仍漂移

当前 ledger 的最新状态不是提交说明里的 “49/52，3 个大 eprint 未完成”，而是：

- 26 篇 × PDF/eprint = 52 个对象；
- 50 个最新对象成功；
- 2 个 eprint 未完成：2309.05950、2506.07976；
- 50 个成功文件均在 E: 当前位置存在，bytes 和 SHA-256 相符。

但前期 Git Bash/Windows 路径翻译错误后，团队只追加了一条 blanket NOTE。以每个
`(arxiv_id, kind)` 的最新成功记录计，仍有 17 行 `stored_at` 指向
`C:/Program Files/Git/mnt/e/...` 的旧位置。人能读 NOTE 推断新位置，机器不能逐行解引用。

要求：为每个受影响对象追加 MOVE/SUPERSEDES 记录，或提供 canonical resolver；成功/失败统计
由脚本生成，不得再在 commit subject 手数。

### MINOR-2：热层阶段叙述已经滞后

`Research-Objective.md` 的“外部证据工作（检索/全文抽取/引文链/饱和/候选问题）尚未开始”把
五类活动合并成一个全称否定，与已经发生的全文抓取和引文校准冲突。

建议正名为：

> “Stage-1A survey-ready gate；系统性 discovery/mapping 尚未执行；定向 ID dereference、
> raw provenance、全文准备和校准性引文试验已执行；Stage-1B 模型/数据实验未放行。”

这不是要求改写历史审计件，而是下一次热层同步时更正当前状态。

### MINOR-3：回应件的一条“空 diff”验收陈述与实际提交历史不符

回应件 §5 第 7 项要求执行：

```text
git diff af96a89 HEAD -- wiki/survey/2026-07-16-sf-t1-routes-v2.jsonl
wiki/survey/fixtures-c4a
wiki/survey/2026-07-16-gate-s1-p0r8-rereview-application.md
```

并预期空输出。实际会列出 P0-R8 application，因为它是在 `af96a89` 之后的 `b6207d3` 新增。
这不表示团队回写了历史文件，也不构成欺诈；它是基准提交选择错误导致的可执行事实句不成立。
下一份回应应修正比较基准或删除该对象，并实际粘贴复跑结果，不能继续沿用“已预验证为空”。

## 7. 引用是否合理、还漏了什么

### 7.1 已有引用的基本判断

当前 #4B 回应所依赖的 26 个哨兵不是凭空编造：raw Atom 身份和元数据核验成立。团队对 survey
只作导航、不作一手科学承重的原则也合理。问题不在“引用格式很差”，而在：

1. discovery query 的词汇本体仍过度围绕项目自己的 agent/reward/verifier 命名；
2. novelty threat 没有单列“系统编排”和“外部 guidance”两种无需 reward 命名的占位方式；
3. 引文闭包工具只处理一部分 identifier，却使用完整交集措辞；
4. 负结果/退化证据尚未成为 survey 的强制编码轴。

### 7.2 P0 补充文献及其角色

| 论文 | 进入 survey 后应承担的角色 | 不应怎样误用 |
|---|---|---|
| MLLM Orchestration (arXiv:2508.10016) | `DIRECT_SYSTEM_OCCUPANCY`：training-free multimodal orchestration、controller、memory、full-duplex | 不因没有 reward/RL 命名而降成旁支 |
| ThinkOmni (arXiv:2602.23306) | `DIRECT_OMNI_GUIDANCE_NEIGHBOR` + `NEW_INFO/EXTERNAL_MODEL_BOUNDARY` | 不直接称为“激活同一黑盒自身知识”；它使用外部 LRM guide |
| Limits and Gains (arXiv:2512.11109) | `NEGATIVE_OR_HETEROGENEITY_EVIDENCE`：模型/任务依赖、refinement 退化风险、external verification 对照 | 不把单个数据集上的正增益外推成通用规律 |
| Multimodal TTS Survey (ACL Findings 2026) | `DISCOVERY_NAVIGATION`：sampling/feedback/search taxonomy 和 reference census | 不作为任何效果数字的一手证据 |
| Small-VLM TTS (arXiv:2607.09438) | `SELECTOR_NULL_AND_SUPPLY_CONFOUND`：majority-vote 强基线、parseability、token budget、policy-model effect | 不把 selector 的 null 简化成“没有 headroom”；先区分输出供给问题与选择问题 |
| On TTS for VLMs (arXiv:2606.28864) | `SCALING_HETEROGENEITY_MAP`：模型规模、方法、任务与过度 compute 失焦 | 不在 Stage-1A 预先冻结统一 K/预算规律 |
| dMLLM-TTS (arXiv:2512.19433) | `GENERATION_BOUNDARY / INTRINSIC_EVALUATOR_PRIOR`：自验证反馈与分层搜索 | 不把图像生成结果直接外推到 omni agentic task；只借鉴机制与边界 |

上述七篇只是**已证实被当前 matcher 确定漏掉的最小集**，不是“补完七篇即 survey 完整”。应以
ACL survey 的参考文献表做 backward census，再用本项目边界编码，而不是把其综述结论照搬。

### 7.3 方法学引用

当前强调可回放、查询留痕和更新规则的方向正确。Stage-1A mapping 执行时至少应对齐：

- [PRISMA-S](https://pmc.ncbi.nlm.nih.gov/articles/PMC7839230/)：检索来源、完整策略、日期、限制和
  去重的透明报告；
- [PRESS](https://pubmed.ncbi.nlm.nih.gov/27005575/)：由不参与原查询设计的人对电子检索策略做
  同行复核；
- [Systematic Mapping Studies in Software Engineering](https://doi.org/10.1016/j.infsof.2015.03.007)：
  mapping 的分类、迭代和可重复报告原则。

本项目不必机械模拟医学综述，但至少要吸收“查询设计人与查询复核人分离”这一点。当前同一方
修词、选哨兵、写 oracle、跑 oracle、解释 PASS，是反复出现 claim inflation 的组织根因。

## 8. 是否超越了 Stage-1A

### 8.1 没有越界、应继续的工作

以下都是 Stage-1A 合理活动：

- 冻结查询、种子、类别路由和全文 ledger；
- 构造独立 held-out 与已知漏检 regression cases；
- 设计 D0/D1/D2 编码及 citation closure；
- 将数据集、模型和方向候选做广度扫描；
- 设计 Stage-1B 的可配置实验接口合同，但不运行模型；
- 对 system-first、training-free、external-model guidance 等边界做概念编码。

### 8.2 现在不应做的工作

在 Gate 与 owner 批准前，不应：

- 加载模型、跑 benchmark、生成 Stage-1B directional-only 数字；
- 因某篇邻近工作出现就仓促收敛技术方案；
- 设置面向后期成本压降的预算 cap；
- 把 SESOI、最终统计检验或论文级主张冻结为 Stage-1A 退出条件；
- 用“目标是超过业界最优”替代问题边界和可证伪假设。

### 8.3 当前真正的范围风险

本轮不是“做得太多”，而是有些执行性工作已经发生却仍被热层写成“尚未开始”，并且把校准性
小实验说成了比测量方法实际更强的结论。范围管理需要的是**如实分级**，不是把已经发生的工作
重新命名为“准备”来回避证据等级。

## 9. 给研究团队及其 AI 的严格整改计划

以下顺序是依赖关系，不得并行堆文件制造“完成感”。

### P0-A：修复发现空间，而非只补论文

1. 建 method-occupation lane；
2. 登记七篇 P0 文献及边界身份；
3. 增加真正命中 L12 的 fresh held-out；
4. 由未参与设计者按 PRESS 风格检查查询；
5. 给出新增 lane 对历史语料的召回增量和噪声样本，但此处不要求预算 cap。

### P0-B：完成七篇邻近工作的结构化占位分析

不要只在 seed 表中增加七个 ID。每篇至少回答：

```text
它优化的冻结核心是什么？
外部控制平面有哪些组件？
它是否依赖外部模型或新信息？
它是否使用 reward / verifier / selection / search？
它覆盖单一任务、单一模态，还是 omni system？
它占据的是本项目哪一层贡献，哪一层仍未占据？
它给出了什么负结果或适用条件？
```

建议输出一张固定 schema 的“占位矩阵”，字段至少为：

| 字段组 | 必填字段 |
|---|---|
| 核心身份 | frozen weights、structure changed、single model / model ensemble |
| 访问能力 | API-only / text-output / logits / hidden-state / gradient |
| 信息来源 | self-only / retrieval / external model / tool / gold-or-label |
| 控制机制 | routing / sampling / selection / verification / search / refinement / memory / stopping |
| 优化信号 | rule / reward / confidence / consensus / learned evaluator / external critic |
| 作用对象 | response / trajectory / workflow / model choice / context supply |
| 任务范围 | single task / multi-task / multimodal / omni / agentic tools |
| 证据强度 | models、datasets、baselines、negative results、known failure modes |
| 本项目关系 | exact overlap / component prior / boundary comparator / navigation only |

矩阵中的 `agentic` 是编码结果之一，不是检索前提；`training-free` 也必须拆成“无参数更新、无结构
变化、是否调用外部可学习模型、是否跨样本积累”四个事实字段，禁止只存一个布尔标签。

特别要求：

- 对 MLLM Orchestration 做“系统构建贡献重叠”分析；
- 对 ThinkOmni 做“external LRM guide 是否违反核心自身知识激活假设”分析；
- 对 Limits and Gains、Small-VLM TTS 和 On TTS for VLMs，把模型/任务/供给异质性转成后续
  Stage-1B 的探索维度，而不是现在冻结实验；
- 对 dMLLM-TTS 只提取 self-verification/search 机制，不把生成任务结论外推为 agent 结论；
- 用 Multimodal TTS Survey 的参考文献做 citation census，但不让二级综述承载一手效果结论。

### P1-C：在 Stage-1A close 前修复 citation closure

完成 work-level identifier resolution、未解析率、歧义记录和 DOI-only mutation。未完成前，E2
不得用“连续两轮零新增”宣布饱和，只能说“在已解析子图上零新增”。

### P1-D：修复 ledger 与阶段热层

1. 为 17 个 stale locator 做逐对象 supersession/resolver；
2. 自动生成 50/52、2 unresolved 等状态；
3. 更新热层阶段措辞；
4. 修正回应件的空-diff 基准；
5. 历史 dated 件保持不改写。

### P2-E：可选脚本 hardening（不阻塞 Gate）

如果团队后续希望把这些脚本用于不可信的多人/多代理流水线，可以再考虑：Atom 派生字段强绑定、
manifest 与 git diff 全集合对账、route typed facts、恶意 mutation fixtures。当前阶段不要求这些
工作，不应挤占方法覆盖修复和实际 mapping 的时间。

### P0-R10 最小复核包

下一轮不要再提交一篇长篇自证散文作为主要证据。最小复核包应只有：

1. dated response，逐项接受/异议；
2. query method-occupation amendment；
3. 七篇论文在修订 matcher 下的结果和结构化占位分析；
4. fresh L12 held-out 的隔离记录与实际 L12 命中；
5. 查询独立复核记录；
6. 回应件空-diff 命令的更正；
7. 一个清楚的 replayability matrix：bundle-only / local-data / network-dependent。

## 10. 签署条件

只有以下条件同时满足，Gate S1 才可签署：

1. G1 关闭：方法占位发现轴已经进入冻结查询合同；
2. 两个冻结提交或新的明确签署提交在干净 archive 上基线全绿；
3. 七篇直接遗漏文献均获得非空发现通道和结构化邻近关系编码；
4. fresh L12 held-out 确实命中新 lane；
5. 独立查询复核人确认新增 lane 不是七篇题名的硬编码捕获器；
6. 回应件中的精确 shell 断言实际可复现。

C1 和三个 MINOR 可以不阻止 mapping 的第一条真实 discovery query，但必须进入带 owner 和截止
gate 的债务表；其中 C1 必须在任何 Stage-1A close / saturation 签字前完成。

## 11. 给 owner 的博士生导师式建议

1. **暂不签 P0-R9。** 唯一阻断理由是发现方案确定性漏掉直接占据方法空间的工作，而非脚本
   未防恶意篡改。
2. **不要因此退回无止境 proposal。** 修复对象是 method-occupation coverage，不是重新讨论
   整个 system-first thesis。
3. **不要启动 Stage-1B。** 先完成 Stage-1A mapping；但也不要用本报告设置模型/数据预算 cap。
4. **引入独立查询复核人。** 至少在词项冻结和 Gate 签署两处，不应由原设计 AI 自签。
5. **对诚信采取“证据分级 + 升级阈值”。** 当前没有 FFP 证据；只有发现实际元数据/全文与外部
   源不符、隐藏正常流程中的失败或明知陈述不实仍发布时，才升级正式研究诚信调查。

最终判断：研究方向仍然有价值，Stage-1A 的 survey 基础设施也取得了真实进展；当前最关键的
缺口不是脚本鲁棒性，而是发现本体仍可能把“没有使用项目内命名”误当成“没有占据项目方法空间”。
先关闭这个结构性缺口，再启动真实 mapping，是符合 Stage-1A 使命的最小且必要动作。
