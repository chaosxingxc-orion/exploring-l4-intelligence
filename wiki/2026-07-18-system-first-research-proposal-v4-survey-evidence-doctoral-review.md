---
artifact_id: "DOCTORAL-REVIEW-STAGE1-SYSTEM-FIRST-V4-2026-07-18-01"
title: "System-first Research Proposal v4 调研证据呈报版——阶段校准、证据与学术诚信对抗复审"
date: 2026-07-18
reviewed_artifact: "wiki/2026-07-18-system-first-research-proposal-v4-survey-evidence.md"
reviewed_commit: "6bfa17f03bd954ac568ebab5efda22f6b73bd1ec"
reviewed_git_blob_sha256: "1477e32fa0953e68b0618e1e5cbf3699eecb0401e0b67264279000a35075fb63"
review_scope: "阶段判定、引用与论证、系统级漏文、检索协议覆盖、复现性、范围越界与研究诚信"
verdict: "WITHHOLD_STAGE1B_SURVEY_EXECUTION_PENDING_MAJOR_REVISION"
integrity_verdict: "FFP_NOT_ESTABLISHED; MATERIAL_MISSTATEMENT_AND_QRP_RISK_REQUIRES_CORRECTION"
---

# 严格博导复审结论

## 0. 一句话裁决

本件不是一份可以直接签署进入下一阶段的合格交付物。工程化 survey 门禁是可重放的，七篇 DFS
也比早期静态列名有实质进步；但是它仍有四个阻断问题：**阶段定义把 survey 与实验混在一起、
“全部承重数字可机器复跑”明显超出九条命令的真实能力、system-first 论证重新滑回 selector
交集、以及已知的 ToolGate 零召回缺口没有获得保证性纳入通道。**

本轮未发现伪造论文、捏造实验输出、篡改脚本结果或隐匿已知负结果的直接证据，因此不能指控
fabrication/falsification/plagiarism（FFP）。但若在收到本意见后仍继续使用“累计模型触碰 0 次”
或“所有承重数字均由九条命令复跑”这类无范围限定的完成态语言，性质将从可纠正的表达失实升级为
明知不实的研究记录风险。

## 1. 当前究竟处于哪个阶段

### 1.1 现行正典有一个定义缺陷

现行 `Research-Methodology.md` 把 Stage-1B 定义为“小样/单次模型触碰”，甚至把 smoke 也算作
Stage-1B 实验；v4 因此在 frontmatter 和 §0 写成“1B 标志 = 触碰模型”。这个定义不利于管理：
它会把系统性 survey 的执行阶段吞并进 1A，并把方向性实验放在“问题定义”阶段，从而模糊
survey、方案探索和正式验证的证据边界。

建议以 dated supersession 采用下面的阶段定义。这里的分界依据是**活动目的与证据用途**，不是
“是否启动过 Python”或“调用样本是否很少”。

| 阶段 | 使命 | 允许 | 禁止/下一阶段才允许 |
|---|---|---|---|
| Stage-1A | 问题与 survey 设计 | 问题树、纳排标准、检索式、种子/哨兵、编码 schema、脚本静态与变异测试 | systematic mapping；任何研究模型调用 |
| Stage-1B | systematic survey / mapping 执行 | 检索、去重、题录筛选、全文编码、引文闭包、饱和分析、证据图谱 | smoke、任务指标、模型/方法比较、headroom/accuracy/WER |
| Stage-1C | 证据综合与选题 | 形成 3–5 候选问题，owner 选唯一问题，冻结复现清单与方案探索边界 | 用临时实验为某候选“拉票” |
| Stage-2A | 方案探索与技术选型 | **先复现最接近且最强的公开 prior**；复现成立后才做自研方向性原型 | 把方向性结果写成确证；跳过 prior 复现直接宣称超过 SOTA |
| Stage-2B | 方案验证 | 冻结假设、对照、判据后进行正式实验和统计推断 | 事后换主指标、选择性报告 |
| Stage-3 | 发表级证据 | 扩展、独立复现、论文级审计 | 用 Stage-2A 小样代替发表证据 |

按此定义，**当前活动 = Stage-1A 的 survey-ready gate；Gate 通过后的第一条 systematic query
才进入 Stage-1B。** 当前并未进入 Stage-2，因为本轮交付物没有新增模型实验。Stage-1B 期间可以
运行检索、解析、校验、去重和台账脚本，但不得跑研究模型，哪怕只跑一个 item 的 smoke。

### 1.2 “当前活动阶段”不能抹掉“累计证据历史”

v4 §0 的“模型触碰（0 次）”若指整个项目，属于事实错误。仓内正典已经保存 frozen
Qwen3-Omni-30B、n=144 genuine best-of-N、oracle-WER、224-cell grid 等历史模型实验。正确写法应
同时给出四个字段：

1. `current_activity_stage = Stage-1A`；
2. `new_model_touches_since_gate_freeze = 0`，并给出起算日期/commit；
3. `cumulative_model_touches = nonzero`；
4. `legacy_experiments = INHERITED_PRIOR_EXPOSURE / PRE-METHODOLOGY_DIRECTIONAL_EVIDENCE`。

历史实验不能把当前活动“自动升级”为 Stage-2，也不能被归零。它们是后续复现、数据切分与假设
冻结必须排除或分层处理的 exposure union。v4 当前只写一个无范围的 0，会同时造成阶段误导和
后验选题风险。

## 2. 三轮对抗式复核

### Round A：阶段与范围攻击

**攻击结论：成立。** v4 对“现在未跑 systematic mapping”的陈述是清楚的，但把 mapping 全部留在
Stage-1A、把模型 smoke 放到 Stage-1B，阶段语义不合理；§3.2 又把 future experimental axes
登记为“Stage-1B 探索维度”，进一步把 survey 与实验混写。

**对团队最有利的反驳：**该写法遵守当时的仓内正典，不能据此认定团队故意越阶段。

**再裁：**反驳只能排除故意性，不能消除方法学缺陷。Gate 签署前应先 supersede 阶段定义；
§3.2 的轴保留为 `STAGE2A_REPRODUCTION_AND_PROTOTYPE_BACKLOG`，Stage-1B 只负责从文献中编码这些轴。

### Round B：可回放性与诚信攻击

我在 commit `6bfa17f` 的干净 `git archive`、WSL2 Ubuntu-24.04、Python 3.12 环境中独立运行回应信
所列九项 bundle-only 命令。结果为 **9/9 exit 0**：package summary、mutation harness、record
validator、route adjudication、34-sentinel recall、query compiler、child-query replay、real-row
dry-run、route validator 全部通过。此前 P0-R9 关于两篇论文 0-hit 的判断确实应被撤回：当前 matcher
复现 `2607.09438` 和 `2512.19433` 均有冻结查询命中。该部分整改有效。

但是，v4 frontmatter 和 §5 宣称“全部承重数字可用九条命令零联网复跑”，**攻击成立**。九条命令
只能重放本仓内的协议结构、计数、静态合同与离线 matcher；它们不会重做论文作者的实验，也不会
独立复算 v4 §3.2 的 `+~6pp`、`+3.7pp`、`+11.4pp`、`8.7×` 等外部研究数字。DFS 中 PDF 页码和
引文抽查能提供**source traceability**，不能升级为**independent machine recomputation**。

必须把证据模式拆成以下互斥枚举，并逐 claim 标注：

- `MACHINE_RECOMPUTED_LOCAL`：本地数据/工件能由命令重新计算；
- `MACHINE_REPLAYED_STRUCTURE`：结构、计数、hash、matcher、validator 可重放；
- `SOURCE_REPORTED_TRACEABLE`：数字来自论文，可定位页/表/图，但未独立复验；
- `REVIEWER_INFERENCE`：跨论文综合或身份判断；
- `TEAM_ATTESTATION`：例如“未执行未登记的查询/模型调用”，无法仅凭日志在场性证明完整性。

“联网活动全量入台账”和“discovery query=0”可以作为签字 attestation，但不能描述成机器证明了
不存在任何未登记活动。完成态语言必须与 oracle 强度相等。

### Round C：system-first 文献红队

**初始攻击：七篇集合漏掉多篇直接系统工作，因此检索协议整体失败。**

**对团队最有利的反驳：部分成立。** v4 已明确七篇只是预映射已检视集合，不是全集；正式 mapping
尚未执行。使用官方摘要对冻结 matcher 做离线压力测试后，ATLAS 命中 5 条查询，AutoTTS 与
Scaling Test-Time Compute for Agentic Coding 各命中 `SF-L2-Q1`。因此不能把“当前七篇未列”直接
等同为“65 条协议必然漏检”。

**再裁：仍有两个实质问题。**

第一，v4 的 RQ-SYS 是“外部 reward-guided sequential control 是否带来终态选择不能获得的效用”，
但 §3.1 的占据判据却是“严格黑盒 + 单一冻结核心 + speech/omni + **候选选择**”。它没有编码
sequential decision rights、tool call、memory write、retry/branch、budget/stop、feedback/refinement
和 final synthesis，因而仍在用旧 selector 对象替 system-first 对象做空位判断。七篇中的 selector
负结果对组件设计有用，却不能构成 system-level novelty map。

第二，ATLAS 在仓内 2026-07-03 的归档 survey 中已经出现，但没有进入本次活跃知识层或七篇优先
DFS。这不是检索召回失败，而是**知识提炼/跨战役 carry-forward 失败**：团队已经“看过”的最近邻
没有被当前 proposal 消化。

以下工作至少应进入 Stage-1B 的 system-level DFS 高优先队列；这里是邻近性要求，不是创新点
终局判断：

| 工作 | 为什么直接相关 | 与 TF-Strict/single-core/speech 的主要差异或待核项 |
|---|---|---|
| [ATLAS: Agentic Test-time Learning-to-Allocate Scaling](https://arxiv.org/abs/2606.01667) | orchestrator 拥有 gather-more/stop/synthesis 的端到端控制权，并覆盖 multimodal benchmark | 非 speech 专项；是否全系统零训练、单/多 solver 身份需全文编码 |
| [AutoTTS: LLMs Improving LLMs](https://arxiv.org/abs/2605.08083) | 把 branch/continue/probe/prune/stop 明确建模为 controller synthesis | 数学推理；控制器发现过程与最终部署是否 TF-Strict 需分开审计 |
| [DeepVerifier](https://aclanthology.org/2026.findings-acl.1243/) | rubric outcome reward、迭代 feedback/refinement、推理时 plug-in，无额外 inference training | rubric 生成与 verifier 能力来源、是否单核/外部模型需审计 |
| [Scaling Test-Time Compute for Agentic Coding](https://arxiv.org/abs/2604.16529) | 长轨迹的 representation/selection/reuse，直接挑战“终态短候选池”抽象 | coding 非 omni；但对 memory 与跨 rollout reuse 是关键 component prior |
| [Selective TTS / Scaling Unverifiable Rewards](https://aclanthology.org/2026.findings-acl.1724/) | reward-guided 多阶段 agent pipeline、stage-wise pruning 与 judge drift | 多 agent、开放任务、judge 可靠性；是 process-control 直接 prior |
| [Team of Thoughts](https://arxiv.org/abs/2602.16485) | orchestrator 动态激活工具 agent，是 system-level 多模型 comparator | 多模型专家联邦，违反 single-core，但正是必须保留的边界对照 |
| [ToolGate](https://arxiv.org/abs/2606.03054) | 外部 controller 对每次 tool call 做 execute/skip，直接覆盖成本、停止和 decision rights | controller 使用 matched-domain trajectory training，属 trained comparator，非 TF-Strict |
| [Reward-Guided Dual-Phase Adaptive Inference](https://aclanthology.org/2026.findings-acl.511/) | reward feedback 驱动动态预算与 early stopping | math/code 非 omni；需区分 tree-search 组件与 agent system 身份 |

此外，[Multimodal TTS Survey](https://arxiv.org/abs/2606.08231) 明确聚焦 vision-language、不覆盖
audio，这只能证明该综述的范围边界，不能单独证明“speech/omni system-first”空位存在。

## 3. 阻断问题清单

### P0-1 阶段本体与 exposure 口径错误

**问题：**“1B 标志=触碰模型”“模型触碰 0 次”把活动阶段、累计历史和新增触碰混为一个字段。

**风险：**历史实验可能在 survey/选题前已经暴露数据、指标和可行方向；若不进入 exposure union，
后续所谓 held-out 或 preregistration 可能只是形式上的。

**通过条件：**发布 dated stage supersession；v4 更正版写明四字段阶段账；Stage-1B 明令禁止模型
smoke；所有历史实验进入 `INHERITED_PRIOR_EXPOSURE`，不删除、不降格、不假装未发生。

### P0-2 复现性声明超出工具能力

**问题：**九条 bundle-only 命令被描述成可以复跑“全部承重数字”。

**风险：**把论文报告值的引文可追溯性伪装成独立复算，会让后续 AI 或评审错误提升证据等级。

**通过条件：**建立 claim-evidence matrix；每个数字标证据模式、source locator、是否独立复验；把
“全部承重数字可机器复跑”改为“协议包的本地结构与计数可重放，外部论文数字仅可追溯到来源”。

### P0-3 system-first 对象被 selector 交集替代

**问题：**RQ 是 sequential external control，空位表却以 candidate selection 为必要轴。

**风险：**即使 survey 最终证明严格 selector 交集稀疏，也不能推出 omni agentic control plane 的
研究问题新颖；反之，system-level prior 已占据的 routing/stopping/refinement 也可能被漏编码。

**通过条件：**增加 system-control occupancy schema，至少包含：核心身份、访问级别、全系统训练
范围、控制时域、decision rights、状态/记忆、工具、反馈/奖励来源、候选生成与选择、停止/预算、
终态合成、信息边界、模态/任务。用该 schema 重做上述直接邻近工作的 DFS；selector 表降为组件表。

### P0-4 已知 ToolGate 零命中仍没有保证性入口

**问题：**ToolGate 已被识别为直接 control/gating prior，65 条查询全零命中，却只进入“同轴累计
3 例才评估增补”的 drift 队列；它既不是当前 34 sentinel，也没有 exact-ID 保证入口。

**风险：**已知强相关工作可能在正式 mapping 中消失，而门禁仍显示绿色。对未知词汇漂移设置阈值
合理，但**已知相关论文不应等待第三个同类样本才被阅读**。

**通过条件：**不必破坏 65 条冻结查询；将 ToolGate 以 `REVIEWER_KNOWN_ITEM / TRAINED_COMPARATOR`
身份加入保证性 DFS 队列并记录 exposure provenance。另保留它作为零命中反例，不能把已知项加入
seed 后再声称 query recall 修复。

## 4. 重要但非阻断的修订

### P1-1 把“支持”改成双向证据综合

§3.2 的“这组先验支持而非削弱我们既有纪律”和“三篇独立收敛”有确认偏差。三篇工作任务、模型、
信号和实验目的不同，不是对同一假设的独立复制。更准确的表述是“异质案例共同提示”，并应同时
列出：哪些结果支持 headroom/供给条件化；哪些结果削弱复杂 selector 的预期价值；什么观察会直接
kill reward-guided control；什么观察只说明供给或 evaluator 失败。

建议每个 candidate problem card 强制增加四行：`supporting evidence`、`contradicting evidence`、
`single-observation kill criterion`、`unresolved alternative explanation`。

### P1-2 引用必须自包含且限定作用域

v4 只有标题缩写和 arXiv ID，没有作者、年份、稳定链接与完整参考文献表；数字也没有在本件中给出
表/图/页 locator。正式 reviewer-facing proposal 应加 reference appendix。跨段拼接的两段原文应
分别引用，不能呈现为连续原句；“一致成立”“主导”“封顶”等词必须限定为“在该论文报告的模型、
任务和设置内”。11/12 引文抽查只证明抽中项目的定位质量，不能代表全部事实都逐字复核。

### P1-3 提炼步骤必须解决“看过但遗忘”

ATLAS 已在 07-03 归档出现、07-18 活跃 proposal 却未吸收，说明归档扫描与热层提炼没有形成保证。
Stage-1B 每轮应产出 `known-item carry-forward ledger`：旧 survey 的 direct neighbor、当前命中、
backward/forward citation 新增、零命中已知项分别列账；归档不是遗忘许可。

## 5. 是否越出当前阶段

本件的检索协议、哨兵、全文 DFS、引文校准和 mapping 计划属于 Stage-1A 合法工作；没有证据表明
本轮新跑了模型实验。问题不在“做得太超前”，而在**用错误阶段名预告下一步**：systematic mapping
应叫 Stage-1B，文献导出的实验轴应进入 Stage-2A backlog。

Stage-1B 只交付知识证据，不交付任何模型效果。至少应包括：完整流量计数、纳排理由、全文编码、
system-level/component-level 双层 occupancy、负结果与冲突证据、饱和轨迹、3–5 候选问题卡、
legacy exposure union，以及 Stage-2A 的 prior reproduction shortlist。到这些完成后才进入 Stage-1C
选题。

## 6. 后续 proposal：Stage-2A 从复现开始

Stage-2A 的第一步应是“复现最近邻”，不是直接写自研 controller。建议提前在 Stage-1C 冻结但不
执行以下包：

1. **复现选择理由**：最接近的 system prior、最强 component baseline、一个负结果/边界 comparator；
2. **复现合同**：作者原设置、公开代码/模型/数据版本、预期指标与容忍区间、不可复现退出条件；
3. **配置化工程合同**：dataset、model/API、inference、controller/evaluator、metrics、seed、artifact
   路径均由配置组合；禁止每个实验新写一条定制主流程；
4. **复现先于改进**：先报告 faithful reproduction 与原文差异，再允许加入本项目的 black-box、
   single-core、speech/omni、TF-Strict 约束；
5. **证据隔离**：复现集、自研开发集和后续验证集分开；历史 exposure union 从验证集排除或显式
   降级；
6. **资源纪律**：当前不设人为 budget cap，但完整记录调用、token、时延、GPU/API 成本；成本记录
   不等于在探索前期用等预算门槛杀方向。

优先复现对象应由 Stage-1B mapping 后决定；在现有证据下，至少要在 ATLAS/AutoTTS 类系统控制、
MLLM Orchestration 类 training-free 编排、以及 majority/BoN/Selective-TTS 类强组件基线之间做
选择，不能只复现一个容易被超过的 selector。

## 7. 重新送审的最小验收清单

只有以下各项全部满足，才建议签署 Stage-1B survey execution：

- [ ] dated stage supersession 落盘：Stage-1B=survey execution，模型实验从 Stage-2A 开始；
- [ ] v4 阶段四字段与 historical exposure union 完整；
- [ ] claim-evidence matrix 覆盖本件全部承重数字和综合性结论；
- [ ] system-control occupancy schema 与 direct-neighbor DFS 补齐；
- [ ] ToolGate 获得 exact known-item DFS 保证入口，同时保留 zero-hit 身份；
- [ ] “supports rather than weakens”改成支持/反证/替代解释三栏；
- [ ] reference appendix、页/表/图 locator 与非连续引文格式修正；
- [ ] 新 commit/blob 钉定后，在干净 archive 重跑九项 bundle-only 门禁仍为 9/9 PASS；
- [ ] owner 明确签署：Stage-1B 全程不得运行研究模型或 smoke。

在这些条件关闭前，裁决维持 **WITHHOLD**。这不是要求团队提前做 Stage-2 实验；恰恰相反，它要求
把 survey 做成真正的知识生产阶段，并把所有模型复现与方案探索干净地推迟到 Stage-2A。
