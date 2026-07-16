# System-first Research Proposal v3：Stage‑1A 收官就绪度对抗审查

> 日期：2026-07-15  
> 审查身份：严格外部审稿人 / 博士生导师  
> 审查性质：**Stage‑1A closeout-readiness review**，不是论文终稿验收，也不是 Stage‑1B 实验放行  
> 被审对象：`wiki/2026-07-15-system-first-research-proposal-v3-consolidated.md`  
> 当前快照：umbrella HEAD `705b69a84cd4305a91e1ccc9896c60bbc79a7387`；target git blob `ed7501941157cb54334e882ce5cbc5f7b93a9f5b`；工作树 SHA‑256 `F6562159D16AEE7CFB66C032358FA7D075665D3D1A002192D95BB8F869E7BA08`  
> 关联前审：`2026-07-15-system-first-research-proposal-v3-stage1a-doctoral-review.md`；其审查快照为 `18288d1`，本轮目标文件已经发生实质修订，不能沿用前审结论。  
> 写入边界：本报告仅新增独立日期化审查文件，不修改 proposal、protocol、manifest、compiler、模板、状态页或任何工程源码。

---

## 0. 总裁决

### 0.1 四个必须拆开的结论

| 对象 | 本轮裁决 | 解释 |
|---|---|---|
| v3 作为 Stage‑1A 工作纲领 | **ACCEPT AS WORKING THESIS** | 上一轮主要科学表述缺陷已经实质修复：输出池与轨迹假设拆开、RL 身份降为待调查、信息来源分类加入、无确证/首创宣称、工程仍为纸面计划。 |
| 团队对上一轮意见的响应 | **SUBSTANTIAL BUT INCOMPLETE** | P0-A、查询编译、CV/RO、分页、基础谱系和威胁池均有真实进展；但最新 owner 策略改写重新引入了来源偏差、证据等级混淆、schema 未传播和 bundle 失配。 |
| Gate S1 search-design 签署 | **WITHHOLD SIGNATURE — TARGETED MAJOR REVISION** | 当前不能签。阻塞点集中在最新检索策略，不需要重写 proposal v4；做一次小而硬的协议修订即可。 |
| Stage‑1A 是否“基本到了尾声” | **只对“收官准备/协议化”成立，对科学工作本身不成立** | system-first survey 仍是零查询、零新 replay；threat 首轮 15 篇尚未双人全文抽取；饱和、占据综合和 3–5 个候选问题均未产生。准确称谓是 **Stage‑1A pre-survey closeout preparation**。 |

Stage‑1B 仍然不得放行。本轮也不要求大样本、显著性、冻结 SESOI、模型/数据集预算 cap 或完整工程平台。

### 0.2 最重要的导师判断

团队这轮不是形式主义地“加了几篇论文”：从 commit `aa6e660` 起，上一轮指出的绝大多数问题已经转化为真实工件。但随后 commit `691150a`/`705b69a` 又重写了检索宇宙、venue tier、BFS/DFS 和引文图策略。**这批后续设计变化没有被当前 bundle manifest 完整钉定，也没有被原 static-validation report 重新覆盖。** 因而“上一轮整改做完”不等于“当前送签包有效”。

科研诚信方面，未发现捏造、篡改或剽窃证据。零 query 状态与仓库现状一致；但“CONVERGED”只能说明内部一致性检查阶段性收敛，不能替代外部检索方法审查，也不能把迟归档 hostile review 升格为可独立重放的原始记录。

---

## 1. 阶段重校准：现在是收官准备末段，不是 Stage‑1A 科学尾声

按照本仓库对 Stage‑1A 的定义，其核心不是“把协议写得足够长”，而是：广泛 survey、找到竞争方法、形成候选科学问题、论证为什么值得继续。当前事实是：

- protocol §12 的 reviewer、owner、P0-R8 三栏均未签；
- `wiki/survey/replay/SF-SURVEY-2026/` 尚不存在；
- proposal §11 明确新执行为零；
- proposal §6 的 15 篇 threat 全文抽取仍是计划时态；
- proposal §13 把 survey 执行、增量扫描、3–5 个候选问题综合放在 Stage‑1A close 之前。

因此建议统一语言：

> 当前处于 Stage‑1A 的 **survey-ready / closeout-preparation gate**。问题框架接近稳定，但决定问题是否成立的外部证据工作尚未开始；只有完成冻结检索、全文抽取、引文链、饱和与候选问题综合后，才进入真正的 Stage‑1A closeout review。

这不是把门槛无限后移，而是防止把“研究方法准备完毕”误报成“研究问题已经界定完毕”。若此处提前称尾声，后续 AI 很容易把 survey 当成例行补证，继而把当前系统身份当作既定结论。

---

## 2. 对上一轮整改的逐项验收

### 2.1 已经充分闭合的意见

| 上一轮意见 | 当前响应 | 判定 |
|---|---|---|
| 输出池 headroom 被外推到 agent trajectory | §2 已拆为“有文献支持的输出池命题”和“待查的系统/轨迹假设”，并明确前者不推出后者 | **CLOSED** |
| reward 影响下一动作不足以自动称 RL | §4 已改用中性术语 `reward-guided inference-time sequential control`，RL 保留为待谱系裁决身份 | **CLOSED AT PROSE LEVEL** |
| “显著高于”提前使用统计语言 | RQ-SYS 改为“实质性且可复核地”，统计语义留到 Stage‑2 | **CLOSED** |
| 查询片段不是可执行查询 | 48 行 `sf-queries.jsonl` 已生成；字段完整、ID 唯一、无占位符 | **CLOSED MECHANICALLY** |
| CV/RO 类别盲区 | L1/L2/L4/L5 增加 `cs.CV+cs.RO`，L3 另含语音类 | **CLOSED FOR THE IDENTIFIED DEFECT** |
| 75 条无声截断 | `max_results` 已改为页大小，增加 `totalResults`、分页和响应哈希 | **SUBSTANTIALLY CLOSED** |
| 基础谱系缺失 | SF-L9 增加 metareasoning/POMDP/options/UCT 四个 DOI 种子，且不受 2022 窗限制 | **CLOSED AS DESIGN** |
| threat pool 13/15 被误作 hard cap | 现已明确首轮 15、可增长，并提升 Affordance/FineVerify | **CLOSED** |
| hostile review 无归档 | 已补迟归档说明、输入/输出 blob 和问题映射 | **CLOSED AS AN HONEST LATE ARCHIVE，不能等同原始 replay** |

这些改动说明团队能理解严格意见，而不是只做文字应付。尤其 headroom、RL 命名与信息边界的修正，显著降低了 proposal 的 claim creep。

### 2.2 只完成了一半的意见

#### A. 信息来源六类只进入 prose，没有进入执行 schema

v3 §4 已提出六类信息来源，并禁止把 exogenous answer-bearing retrieval 的增益称作“激活预训练知识”。但当前 T2 模板没有 `information_source_classes`、`answer_bearing_external_info`、`gold_path_audit` 或“activation-attributable vs total-system lift”的字段。

这意味着执行者可以阅读论文后只填写 `reward_type`、`ground_truth_used` 与 `external_components`，却无法机械地产出 thesis 最承重的归因边界。**这是典型的 prose 已修、schema 未传播。**

#### B. RL 身份所需字段没有按 v3 承诺落进模板

v3 声称 survey 将抽取状态、动作、反馈、策略表示、跨步更新对象、信用分配、停止规则、作者是否自称 RL；当前 T2 模板并无这些独立字段。`what_changes_at_test_time` 和 `feedback_type` 不能可靠替代。

如果不修，SF-L9 即使读完，也无法用统一记录回答“这是 RL、planning、search、bandit 还是 metareasoning”。

#### C. omni 五轴合同没有传播

v3 要求“模型能力、agent observation、工具模态、行动模态、因果接地”五轴分开；T2 仍只有一个 `modality_path=text|audio-native|audio-tool|vision|omni`。该字段会把至少五个不同问题压成一个标签，尤其无法区分：

- 中央 text LLM 调 audio tool；
- 冻结 omni 核心亲自读取 audio/video；
- 工具输入是多模态但 controller 只见文字摘要；
- agent 输出是否真正作用于多模态环境；
- 非文本模态是否因果改变动作。

这正是 RQ‑OMNI 的核心，不应留给自由文本事后解释。

#### D. TF‑Strict 的 `learned_object` 枚举过窄

当前枚举只有 `token-prior/value-fn/verifier/prompt/none`，但 UCT、AFlow、ADAS、GPTSwarm、Voyager、ConMem 类方法可能更新 memory、skill、tool/code、workflow、graph、retrieval index 或 exemplar archive。若 schema 不能记录这些对象，`scope_pending` 无法被一致裁决。

还应拆开：

1. 组件是否含既有预训练参数；
2. 该方法是否为当前任务/系统新训练参数；
3. test time 是否更新参数；
4. 是否跨 item 持久化非参数状态。

否则“external component trained”会把冻结的通用 ASR/VLM 工具与针对研究任务训练的新 verifier 混为一类。

### 2.3 已闭合后又重新打开的问题

#### Bundle 唯一钉定已经失效

`sf-bundle-manifest.md` 的最后一次 correction 固定到 `d2fab2d`/`e10a4f2`；但当前 proposal 与 protocol 的最后修改均在 `705b69a`，中间 `691150a` 还发生了 arXiv-only、T1 venue、BFS/DFS、引文图等重大方法改写。

当前事实：

- proposal 当前 blob = `ed750194…`，bundle correction #2 钉的是旧 blob `10185474788c…`；
- protocol 当前 blob = `62bc2f90…`，bundle correction #2 钉的是旧 blob `775fb7615a8b…`；
- blank templates、amendment、README 也在 correction #2 后变化；
- current bundle 没有 correction #3 固定 `691150a/705b69a` 的完整对象集。

所以 reviewer 目前无法回答“到底签哪一个不可变 package”。这是 Gate S1 的直接阻塞项，不是小型文档洁癖。

#### Static validation 报告输入已经陈旧

静态报告记录的 protocol input SHA‑256 是 `b217fbc0…`，当前 protocol SHA‑256 是
`8ABDCB206340DA3AB89A5B6DADCD667CA55A23BF80F080C97E91D0AE75856C02`。48 行查询产物的确未变，
但报告没有证明“当前 protocol → 当前 compiler → 当前 queries.jsonl”这条链。团队只需重新离线复跑并钉定，不需要重新设计查询。

#### 热状态页已经落后于实际策略

`Research-Objective.md` 仍停在续56，并继续描述“16 条副源路线三级分级”，而当前协议 amendment-2 已将其退役。该文件自称团队 AI 的唯一热层入口，陈旧状态会让后续 AI 同时执行互相冲突的两套路线。

---

## 3. 引用合理性审查

### 3.1 已经合理并明确边界的引用

#### Large Language Monkeys

[Large Language Monkeys](https://arxiv.org/abs/2407.21787) 确实报告 repeated sampling 下 coverage 随样本数增长，并在多个任务上呈现近似 log-linear 关系；论文也明确指出没有自动 verifier 时，majority voting 和 reward model selection 会在大样本处平台化。v3 现在只用它支持 output-pool coverage，而不推出 agent trajectory，引用边界基本正确。

仍建议把“输出池存在大幅头空”改成“**在若干已研究任务与供给下可以出现显著 output-pool coverage/headroom**”。“存在大幅”仍容易被读成跨任务普遍事实。

#### Scaling Auditory Cognition

[Scaling Auditory Cognition via Test-Time Compute](https://arxiv.org/abs/2503.23395) 可以支持“音频领域存在 output-level TTC 改善”的动机，不支持黑盒、TF‑Strict 或有状态 agent trajectory。v3 已作 output-level 限定，方向正确；Stage‑1A 真正收官前仍须全文核验具体五种 TTC 的接口需求和训练状态。

#### Self-Verification Limitations

`arXiv:2402.08115` 被用于说明“没有 sound verifier 时，自验证可能不可靠”，并明确不推出“一切 label-free 信号失败”。这是合理的支持/不支持边界写法。

### 3.2 仍需降格或补充限定的引用

#### Snell 不是 TF‑Strict 直接证据

[Scaling LLM Test-Time Compute Optimally](https://arxiv.org/abs/2408.03314) 明确研究了 process-based verifier reward model 搜索和测试时分布更新。它支持“测试时算力分配及搜索可改善输出”，但其中 verifier 可为训练型组件，不能被读成 TF‑Strict 的直接可行性证据。

建议在 v3 锚点后加 `TRAINED/GRAY-BOX MECHANISM ANALOGY`，而不是只写“同样不支持轨迹”。

#### HedgeTune 不是已验证的 agent stopping rule

[Inference-Time Reward Hacking](https://arxiv.org/abs/2506.19248) 研究 BoN、Soft-BoN 和 BoP 下 proxy reward 过优化，并用 HedgeTune 选择更合适的推理期参数。它是 RQ‑SAFE 的重要 output-level Goodhart 类比，但不是已经验证的多步 agent trajectory 停止/弃权算法。

当前“其提出的 HedgeTune 即停止机制候选”应改成：

> output-level overoptimization control analogue；能否转成 trajectory-level stopping/hedging 是待调查问题。

#### Omni‑Decision 只能暂作最高优先威胁，不能作占据结论

[Omni‑Decision](https://arxiv.org/abs/2607.11433) 的摘要确实自称 training-free，并具有共享 evidence state、planning、acquisition、validation、repair 和 stopping，且直接报告 OmniGAIA/WorldSense 结果。把它放在第一威胁位是正确的。

但它是 2026-07-13 的新 preprint。当前不得仅凭摘要决定：

- 是否核心 omni model 自身在环读取非文本模态；
- deterministic state update 是否由 reward/advantage 驱动下一步动作；
- web/media evidence 是否属于 new-info；
- 是否存在隐藏训练、prompt tuning 或 benchmark-specific design；
- 数字与基线是否公平。

团队已经把这些留给全文 survey，处理是诚实的；Stage‑1A close 前必须用固定版本全文和双人抽取完成。

### 3.3 正文引用形式仍可再成熟一步

当前有 arXiv ID，已足以定位；但完整独立 proposal 最好增加一个最小 reference table：title、version、venue/status、支持命题、不支持命题、当前证据深度。尤其要把：

- `FULLTEXT_READ`；
- `ABSTRACT_ONLY`；
- `TRAINED_COMPARATOR`；
- `MECHANISM_ANALOGY`；
- `DIRECT_THREAT_PENDING`

分开。否则 reader 仍需跨 proposal、manifest、census 和 ledger 拼装证据等级。

---

## 4. 仍遗漏的相关论文与方法族

上一轮点名的 OmniAgent、CMA‑Harness、UCT、ConMem、Argos 已加入 60 条 manifest，这一整改正确。下面列的是本轮针对“系统如何构建”与“reward-guided control 究竟属于什么”继续补查后，仍未进入 60 条列名种子的高价值工作。

遗漏论文不等于检索一定失败：有些可能由 48 条 query 或 chaining 命中。但在 Stage‑1A 收官准备阶段，以下已知强邻居不应靠运气等待召回，应作为 dated seed batch 进入，并记录是 direct threat、trained comparator、method lineage 还是 component analogy。

### 4.1 系统结构自动设计与 reward/feedback 搜索：高优先级

| 工作 | 为什么重要 | 初步用途 |
|---|---|---|
| [AFlow: Automating Agentic Workflow Generation](https://arxiv.org/abs/2410.10762) | 把 code-represented workflow optimization 明确定义为 MCTS，并用 execution feedback 迭代修改工作流；直接挑战 RQ‑SYS/RQ‑CTRL 与“外部结构如何更新”。 | 高优先级 trained/system comparator；核验其开发集反馈、持久化 workflow 是否违反 TF‑Strict。 |
| [Automated Design of Agentic Systems](https://arxiv.org/abs/2408.08435) | ADAS/Meta Agent Search 自动发明 agent building blocks、prompt、tool use 与 workflow，并维护 discovery archive；直接占据“系统本身作为优化对象”的邻域。 | 高优先级 system-design lineage / trained comparator。 |
| [Language Agents as Optimizable Graphs / GPTSwarm](https://arxiv.org/abs/2402.16823) | 把 agent 写成 multimodal computational graph，并优化 node prompt 与 graph connectivity；与外部 control plane 的结构化和版本化高度相关。 | 高优先级结构对照；需审计 graph/prompt update 是否属于训练。 |
| [Reasoning with Language Model is Planning with World Model / RAP](https://arxiv.org/abs/2305.14992) | LLM 同时作为 world model 与 agent，MCTS 在 task-specific reward 指引下找高奖励路径；是 RL/search/planning 命名边界的直接祖先。 | SF‑L9 + RQ‑CTRL 必读，不应只靠 LATS chaining 偶然发现。 |
| [Tree of Thoughts](https://arxiv.org/abs/2305.10601) | 用 self-evaluation 决定后续探索、回溯和分支，是“reward/evaluation 改变下一步动作但不一定是 RL”的经典反例。 | 强基线/概念谱系；帮助约束 kill‑RL。 |
| [PromptAgent](https://arxiv.org/abs/2310.16427) | 把 prompt optimization 形式化为 MCTS/strategic planning，并以错误反馈改进 prompt state。 | black-box/prompt-update 边界；当前 query 可能命中，但应列名。 |

### 4.2 通用 agentic system 与多模态 computer-use：高优先级系统对照

| 工作 | 为什么重要 | 初步用途 |
|---|---|---|
| [Magentic‑One](https://arxiv.org/abs/2411.04468) | Orchestrator 维护进度、重规划和错误恢复，并协调 web/file/code agents；无需修改 agent 核心或额外 prompt tuning/training。 | RQ‑SYS、state、replanning、tool orchestration 的强系统对照。 |
| [Agent S](https://arxiv.org/abs/2410.08164) | MLLM computer-use agent，使用 experience-augmented hierarchical planning、外部知识搜索与经验检索。 | RQ‑OMNI、new-info/read-out、persistent experience 边界对照。 |
| [AutoGen](https://arxiv.org/abs/2308.08155) | 可配置多 agent conversation、human/tool integration 和 interaction behavior，是工程 harness 与系统抽象的重要祖先。 | 工程基座/系统表达基线，不必作为 novelty kill。 |

### 4.3 多模态组合、主动感知与工具闭环：高优先级机制谱系

| 工作 | 为什么重要 | 初步用途 |
|---|---|---|
| [Chameleon](https://arxiv.org/abs/2304.09842) | LLM planner 组合 off-the-shelf vision、web、Python 与 heuristic modules，直接在 multimodal knowledge-intensive tasks 上运行。 | 训练自由的模块化多模态系统邻居；对“系统第一创新”很关键。 |
| [Socratic Models](https://arxiv.org/abs/2204.00598) | 在 2022-10 窗之前就通过语言接口零样本组合多个预训练模态模型、API 与数据库，且无需 finetuning。 | 必须作为 system/omni foundational seed；现有日期窗会漏掉。 |
| [AVIS](https://arxiv.org/abs/2306.08129) | Autonomous Visual Information Seeking 使用动态 planning 和外部工具获取信息。 | active perception / information acquisition / new-info 边界。 |
| [Visual Sketchpad](https://arxiv.org/abs/2406.09403) | 多模态模型在推理中通过视觉草图和 specialist vision tools 改变后续 planning/reasoning。 | 非文本中间状态与 tool-mediated grounding 的方法对照。 |
| [VideoAgent](https://arxiv.org/abs/2606.23327) | 2026 年的多 agent 视频理解/编辑系统，包含 30+ 专用 agent、intent routing 与 textual-gradient graph optimization。 | 近期 system/harness 对照；大概率是训练/优化型 comparator。 |

以上工作还暴露了当前 query vocabulary 的盲区：`agentic workflow`、`automated design of agentic systems`、`computational graph`、`multi-agent orchestration`、`active perception`、`information seeking`、`zero-shot multimodal composition` 并未得到稳定直接覆盖。

建议不是无限加论文，而是：

1. 增加一个 dated seed batch‑2；
2. 为上述短语做离线 query sensitivity audit；
3. 若现有 48 条确定不能召回其中若干 direct papers，在执行前新增有版本号的 query IDs；
4. 不替换旧查询，保持 append-only query evolution。

---

## 5. 当前 Gate S1 检索策略的五个签字阻塞项

### G1. `arXiv-only` 可以做可回放主语料库，但不能冒充综合文献宇宙

当前 protocol §2 写“检索宇宙 = arXiv 唯一”，并且除 T1/SF-L9 例外外，不参考非 arXiv 工作。这在工程上简洁，在科学上存在来源选择偏差。

一项针对计算机科学 arXiv 使用率的研究发现，不同 CS 领域的 arXiv 覆盖差异很大：理论 CS/ML 较高，其他方向可接近零，而本项目横跨 ML、speech、robotics、HCI、software/agent systems。[Popularity of arXiv.org within Computer Science](https://arxiv.org/abs/1710.05225)

PRISMA‑S 也强调必须完整报告所有信息源、覆盖日期、平台、查询和补充检索方式；可重放性来自冻结请求与记录原始结果，不要求把科学宇宙压成单一数据库。[PRISMA‑S](https://pmc.ncbi.nlm.nih.gov/articles/PMC8270366/)

建议二选一：

- **方案 A（推荐）**：arXiv 作为主检索 corpus；任何经 T1 proceedings、citation graph、DOI/OpenAlex 或已知 seed 发现的直接相关工作，均允许以 venue-native ID/DOI + 本地全文 hash 纳入，不以 T1/T2 决定能否进入；或
- **方案 B**：保留 arXiv-only，但把最终产出降名为 `arXiv-centered mapping review`，不得声称 comprehensive occupancy、完整 NO_DIRECT_MATCH 或“业内没有类似工作”。

owner 有权决定工作流偏好，但 reviewer 不能在来源限制与结论强度不匹配时签字。

### G2. venue tier 不能替代 study-quality assessment

当前规则称“T1 实验结论可直接承重，T2 数字不得单独支撑 kill/proceed，T3 默认不参考”。这把 venue prestige、peer-review status 和证据有效性混成了一个变量：

- T1 论文也可能有泄漏、不公平 baseline、低样本、不可复现或不适用于本项目的接口；
- T2 preprint 可能有公开代码、充分消融、独立复现或后来转为正式版；
- workshop 在快速发展的 agent/omni 领域可能是早期关键机制来源；
- novelty/priority threat 与实验可信度是两回事：一个未发表方法仍可能摧毁“首创”宣称。

`venue_tier` 可以保留为元数据，但必须与以下三轴分开：

1. `verification_depth`：看到了摘要、全文、claim locator 还是复现；
2. `publication_status`：preprint/peer-reviewed/withdrawn/retracted；
3. `study_quality`：数据边界、对照公平、统计不确定性、消融、复现性、代码/数据、claim-evidence match。

T1 不得自动“直接承重”；T3 不得只因 venue 默认排除。PRISMA 2020 也把研究偏倚/质量评价作为独立报告对象，而不是用数据库或期刊名替代。[PRISMA 2020 expanded checklist](https://www.prisma-statement.org/s/PRISMA_2020_expanded_checklist-yc78.pdf)

### G3. 新增的 T1 proceedings route 尚未被实例化

协议声称“十会 × 2022–2026，每会每年一个 route ID”，理论上应有 50 条路线；当前仓库没有相应 route manifest，也没有：

- 每个 proceedings 的稳定入口；
- 年份/track/正会定义；
- title export 格式；
- topic keyword 的冻结词表；
- title normalization/fuzzy matching 规则；
- raw title list 的保存和 hash；
- arXiv title resolution 失败后的 DOI/backup 处理日志。

当前 `T1` 空白模板实际是“arXiv 查询日志”，不是 proceedings route。因此 A2-7 仍是 prose promise，无法执行或重放。

此外出现同名异构：`T1/T2/T3` 既是 venue tier，又是 blank-template 编号。按照本项目“同一个名字绝不承载两个定义”的纪律，应把模板改名为 `REC-1..REC-6` 或把 venue tier 改为 `V1..V3`，否则 AI 执行时极易把 `T2_UNREVIEWED` 与“T2 纳排模板”混淆。

### G4. 承重合同没有传播到数据结构

签字前至少补齐：

```text
information_source_classes[]
answer_bearing_external_info(Y/N/UNCLEAR)
gold_path_audit
activation_attribution(readout/new_info/mixed/not_claimed)

core_model_modal_capability
observation_seen_by_core
tool_input_output_modalities
action_modality
multimodal_causal_grounding_evidence

state_definition
action_definition
feedback_definition
transition_or_controller
policy_representation
cross_step_update_object
credit_assignment
stopping_rule
authors_call_it_rl(Y/N)

component_pretrained(Y/N)
method_specific_parameter_training(Y/N)
test_time_parameter_update(Y/N)
nonparametric_persistence(within_item/across_items/none)
learned_object(memory/skill/tool/code/workflow/graph/index/exemplar/...)
```

否则 proposal 的科学合同无法由 survey 记录生成可核验结论。

### G5. Bundle、验证报告和热状态必须重新对齐同一个 blob 集

签字前只需一次最终 closure：

- 新增 bundle dated correction，固定 `705b69a` 之后所有现行工件；
- 离线复跑 query compiler，证明当前 protocol 仍产生同一 JSONL blob；
- 为 T1 proceedings routes 做静态验证；
- 更新 `Research-Objective.md`，删除已退役副源口径；
- 做一次独立 static signoff review，专门检查当前 A2 策略，不再重复创造 proposal 版本。

### G6. 分页拆分规则还有一个小但真实的边界缺陷

协议写“totalResults > 2000 时按年度子窗拆分，直到每片 ≤2000”。若单个年度仍超过 2000，单纯“按年度”无法继续满足“直到”。应明确递归规则：年 → 月 → 日，或类别 × 时间确定性拆分；所有子查询生成派生 ID 和父查询 hash。

这个问题不需要预跑 API，只要把 fallback 写清楚。

---

## 6. 科学问题本身的剩余逻辑缺口

### 6.1 “超过终态选择的天花板”必须条件化

RQ‑SYS 说系统要高于 one-shot 与终态选择的“天花板”。天花板只在给定供给 `c`、候选池构造、调用权、采样预算和信息边界下有定义。agent 改变供给、候选轨迹或工具权后，本来就是另一个 ceiling。

建议表述：

> 在相同初始任务信息与明确记录的 decision rights 下，序列控制是否能获得终态-only selector 无法获得的额外效用；同时分别报告两者各自条件化 headroom。

这样不会把“换了问题空间”误写成“打破同一个 oracle ceiling”。

### 6.2 “摸高不设 cap”与因果归因的 matched control 必须分开

owner 所说全力摸高、不设置全局探索 cap，在 Stage‑1A/1B 是合理的。但 RQ‑CTRL 要回答“增益来自 reward，而非更多调用/采样”，未来的反馈阻断、reward randomization 与无奖励 search 必须拥有可比较的 action space、information access、horizon 和调用机会。

这不是提前设置全局预算 cap，也不是 Phase‑3 成本效率比较；它是验证 reward 因果作用所需的内部有效性控制。建议将二者明确拆名：

- `ceiling-seeking resource posture`：不设 cap，摸高；
- `causal matched-control entitlement`：局部探针中匹配可用信息、动作和决策机会；
- `cost-efficiency comparison`：Stage‑3/后期工具。

当前把所有“等预算”都推到 PHASE‑3，会让 RQ‑CTRL 在逻辑上无法被证伪。

### 6.3 系统总效用与“激活预训练知识”必须是两个 estimand

加入 web、retrieval、工具或跨 item memory 后，系统总效用可以提高，但其中一部分来自 new-info。v3 已禁止把类别⑤直接称为 activation，这是进步；下一步还要在候选问题卡中分别写：

- `total system utility lift`；
- `pretrained-knowledge activation-attributable lift`；
- `new-information/tool-computation attributable lift`；
- mixed/无法识别部分。

否则“omni agentic system 是第一创新点”和“training-free RL 激活预训练知识”仍会在最终叙事中互相借力，产生归因漂移。

### 6.4 RQ‑SYS 目前仍是 program-level umbrella，不是单篇研究问题

它同时包含黑盒、TF‑Strict、omni、agentic、reward control、state/tool、效用提升和 ceiling 比较。作为 Stage‑1A programme thesis 合理；作为 Stage‑2 单个主假设过宽。

当前不用收窄到唯一问题，但 survey closeout 的 3–5 张 candidate card 必须把它分解为可被单一反例杀死的对象，例如：

- reward-conditioned evidence-state update 是否优于结构匹配的 non-reward search；
- native omni observation 是否改变 controller decisions；
- TF‑Strict persistent memory/tool creation 是否属于激活还是跨 item 学习；
- label-free trajectory feedback 在何种 verifier quality 下出现 Goodhart 拐点。

真正选题仍留给 Stage‑1C，不要在本轮提前冻结。

---

## 7. 当前工作是否超越 Stage‑1A

### 7.1 没有越界、应继续保留的工作

- 设计可回放 survey、编译查询、冻结 schema；
- 扩展 direct-threat seeds 与 foundational lineage；
- 讨论 RL/search/planning/metareasoning 身份；
- 做 runner/config ADR、harness 纸面比较和无真实数据 schema mock；
- 把 Stage‑1B 探针写成无现时效力的 blueprint；
- 记录历史 QRP、暴露和失败，不升级 directional 证据。

当前没有新模型、数据集或 API 实验，工程也没有连接真实 backend；这一阶段纪律是正确的。

### 7.2 已经发生的“流程性越界风险”

科学实验没有越界，但 meta-process 已经出现膨胀：多轮 proposal、amendment、correction、hostile loop 和一致性 commit 仍未形成可签的单一快照。若继续修改叙事而不尽快进入 survey，Stage‑1A 会变成“协议研究项目”。

本轮整改后应立即停止：

- 新 proposal v4；
- 再发明 taxonomy 名称；
- 继续扩写 Stage‑1B B0–B5 细节；
- 为每个 reviewer 意见制造一份新的元报告；
- 在 survey 前讨论模型/数据集跑法。

只完成当前 G1–G6，重新申请一次 Gate S1。签署后立即执行 survey，而不是再开 proposal 轮次。

### 7.3 真正越界、仍然禁止的动作

- Gate S1 未签即跑任何一条 system-first query；
- 用检索命中结果反向删改原查询而不保留旧请求；
- 跑新模型/数据集/API 来决定问题；
- 依据 Omni‑Decision 等单篇新 preprint 宣布项目已被占据或仍有首创空间；
- 把 survey-ready 当成 Stage‑1B authorization；
- 把未来 blueprint 的五臂或 B0–B5 当成冻结实验设计。

---

## 8. 科研诚信与治理审查

### 8.1 FFP 仍未成立

本轮没有发现 fabrication、falsification 或 plagiarism：

- target 与协议明确新 query 执行为零；
- SF survey replay 目录不存在，与“尚未执行”一致；
- query compiler 是离线纯文本处理；
- manifest 60 行、60 个唯一 ID、2 个 `scope_pending` 可机器复算；
- 团队没有把新补论文假装成早已登记；
- hostile review 的迟归档被明确披露，而非伪装成当时已有文件。

### 8.2 仍需保持严厉的治理问题

#### “迟归档真实执行”仍是自我陈述

hostile archive 诚实写明精确时间与原始 token 记录不可恢复。它可以作为问题/修复复盘，但不能独立证明当时双 agent review 的全过程。结论应标 `LATE_RECONSTRUCTED_REVIEW_SUMMARY`，而不是完整 replay。

#### “CONVERGED”被重复使用过多

内部 grep/一致性 convergence 不等于：

- 检索策略无偏；
- 引用科学上正确；
- schema 足以回答 RQ；
- reviewer 已签；
- Stage‑1A 已接近科学收官。

建议以后每次写 convergence 都带对象：`TEXT_CONSISTENCY_CONVERGED@blob`、`QUERY_STATIC_VALIDATION_PASS@blob`，不使用裸 `CONVERGED`。

#### 单一热状态已经漂移

对 AI 协作项目而言，热状态页落后于协议是高风险缺陷。它不会直接构成学术欺诈，但会导致后续代理执行废弃路线、错误引用旧计数，并再次制造“我们以为已经闭合”的假状态。

---

## 9. 最小整改计划：不再重写 proposal，只修 Gate S1

### P0‑1：固定现行送签快照

- [ ] bundle manifest 新增 dated correction，固定 `705b69a` 后所有现行工件的 path/commit/blob；
- [ ] 更新热状态 `Research-Objective`，使其与 amendment-2 一致；
- [ ] 重新离线运行 compiler，记录 current protocol SHA 与输出 blob；
- [ ] 保持 `queries_executed=0`。

### P0‑2：修正来源与 venue 规则

- [ ] 把 `arXiv-only comprehensive universe` 改为 `arXiv-primary + venue-native/DOI rescue`，或明确降名为 arXiv-centered mapping；
- [ ] venue tier 只作 publication metadata，不直接决定证据能否承重；
- [ ] 新增独立 `study_quality` 评价；
- [ ] T3 不再按 venue 自动排除，仅按相关性/质量裁决并登记理由；
- [ ] 无法获得全文者保留为 coverage gap，不从“存在性”记录中消失。

### P0‑3：实例化 T1 proceedings 发现道

- [ ] 冻结 50 条 venue-year route ID；
- [ ] 冻结入口、track、title filter、停止、导出与 raw artifact hash；
- [ ] 定义 title normalization、exact/fuzzy match、arXiv/DOI resolution；
- [ ] 为路线提供空白日志模板；
- [ ] 消除 venue T1/T2 与 template T1/T2 同名异构。

### P0‑4：让 schema 真正回答五份合同

- [ ] 增加六类信息来源与 activation attribution 字段；
- [ ] 增加 RL/search/planning 裁决字段；
- [ ] 把 omni 五轴拆开；
- [ ] 扩展 `learned_object` 与 cross-item persistence；
- [ ] 将 evidence depth、publication status、study quality 三轴分立；
- [ ] 补 `API-multimodal` 与 hidden/logit/attention 等 core-access 枚举。

### P0‑5：补 direct seed/query sensitivity

- [ ] 添加 AFlow、ADAS、GPTSwarm、RAP、ToT、PromptAgent；
- [ ] 添加 Magentic‑One、Agent S、AutoGen；
- [ ] 添加 Chameleon、Socratic Models、AVIS、Visual Sketchpad、VideoAgent；
- [ ] 每篇先标 `DIRECT_THREAT/TRAINED_COMPARATOR/METHOD_LINEAGE/COMPONENT_ANALOGY`，不预判最终结论；
- [ ] 对缺失短语做离线 sensitivity audit，必要时新增 query IDs，不覆盖 48 条旧记录。

### P0‑6：两处引用勘误

- [ ] Snell 标为 trained-verifier / mechanism analogy；
- [ ] HedgeTune 标为 output-level overoptimization analogue，不写成已验证 agent stopping mechanism；
- [ ] output-pool “大幅头空”改为条件化“可出现”；
- [ ] 所有 occupancy 数字在 Stage‑1A close 前完成 version pin + full-text locator。

上述整改应集中在一个 amendment/correction batch 内完成。**不要求 proposal v4，不要求再加一轮元叙事。**

---

## 10. Gate S1 后到真正 Stage‑1A close 的必需产物

Gate S1 若修复后签署，只授权执行 survey。真正收官至少需要：

| Closeout evidence | 最低要求 |
|---|---|
| Search/replay corpus | 全部请求、分页、失败、原始响应/ID 集、时间、hash 可回放 |
| Screening flow | 去重前后数、纳排理由、来源路径、版本、无法获取全文数量 |
| Threat review | 首轮 15 + 新增 direct threats 双人独立全文抽取，冲突可定位 |
| Citation graph | 方法谱系/对比边、剪枝、visited set、两轮饱和记录 |
| Quality appraisal | verification depth、publication status、study quality 分开 |
| Contract verdicts | black-box、TF‑Strict、RL、agentic、omni 分别给支持/反对/未知 |
| Attribution map | system lift、pretrained read-out、new-info/tool computation 分开 |
| Candidate package | 3–5 张问题卡：已占据、开放机制、最强反证、可行 1B 探针、kill/pivot、剩余未知 |
| Stage close signoff | 独立 Stage‑1A close 签字；与 Stage‑1B 放行再次分立 |

没有这些产物，不能因为 protocol 很完整就宣布 Stage‑1A 已完成。

---

## 11. 最终导师意见

研究团队本轮最值得肯定的不是文档数量，而是接受了三项会真正改变研究身份的纠偏：**输出池不等于轨迹、reward-guided 不自动等于 RL、new-info 不等于激活预训练知识。** 这些修正使 v3 已经可以作为 Stage‑1A 工作纲领继续使用。

但收官阶段的严格性要求我们把注意力从“proposal 写得好不好”转移到“survey 是否会系统性骗过自己”。当前最大的危险已经不是实验造假，而是：用 arXiv-only 和 venue prestige 制造一种可回放却有偏的文献宇宙，再用未传播到 schema 的科学合同生成看似精确的 occupancy matrix。那会产生形式完整、科学上却不完整的结论。

因此本轮不签 Gate S1，但这不是再次把团队送回大范围重写。修复 G1–G6、补种子和 schema、重新钉定一个不可变 bundle 后，应立即送一次窄幅复核；通过后开始 survey。**当前是 Stage‑1A 收官准备的末段，不是 Stage‑1A 科学工作的尾声；真正尾声从可回放 survey 完成、候选问题形成之时开始。**
