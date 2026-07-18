---
artifact_id: "GATE-S1-V5-RESPONSE-STAGE1A-DOCTORAL-REREVIEW-2026-07-18-01"
title: "Gate S1 v5 回应信——Stage-1A 尾门博导复审、构念效度与大规模 Survey 启动裁决"
date: 2026-07-18
review_target: "wiki/survey/2026-07-18-gate-s1-v5-response.md"
review_target_commit: "746a8b1abab4306d91eb63cfe7925a06750bd0c0"
review_target_blob: "b35681d0ed7ceff9be1b8b531f70b937be720e92"
review_target_sha256_git_blob_bytes: "1fe9f45305d9a696ae58f4824b04f9c04c7d5fad430c8ffe8fe2da4c6b85e230"
review_role: "严格审稿人 / 博导 / adversarial integrity reviewer"
stage_determination: "Stage-1A survey-ready gate；尚未进入 Stage-1B"
gate_verdict: "WITHHOLD_STAGE1B_LARGE_SCALE_SURVEY_PENDING_NARROW_STRUCTURAL_REMEDIATION"
severity: "2 Gate MAJOR + 4 MINOR；未发现足以认定 FFP（捏造/篡改/剽窃）的证据，但仍有已建立的语义型 QRP 风险"
mutation_scope: "本件仅新增 dated review；未修改研究团队任何源文件、协议、回应信、数据或代码"
conclusion: "工程门禁可回放，但 identity/occupancy 构念不完整且 carry-forward 采样框架失衡；大规模 survey 暂缓，完成零查询窄幅整改后再签。"
reasoning_summary: "机器测试证明实现与自定义 schema 一致，却未证明 schema 等同 S0/RQ-SYS；候选池分析单位混杂，已知 agent-TTS 与 speech/voice 测量证据未完整进入保证队列。"
purpose_chain: "保护 Stage-1B 批量编码效度 → 避免错误 occupancy 污染 Stage-1C 选题 → 为 Stage-2A prior 复现与后续正式验证保留可信知识基座。"
provenance: "目标提交/Blob/SHA256 钉定；git archive 干净态复跑；阶段正典、承重附件、仓内旧 survey 与官方原论文交叉核验。"
invalidation_conditions: "若团队交付完整项目身份投影、统一分析单位、确定性 carry-forward 与纠正后的 claim-evidence matrix，并经独立语义复核零新 Gate MAJOR，则本 WITHHOLD 失效，可转签 Stage-1B。"
---

# Gate S1 v5 回应信博导复审

## 0. 先给裁决

**当前仍处于 Stage-1A 的 survey-ready gate，尚未进入 Stage-1B。** 阶段正典已经写明：Gate S1
签署与 owner 批准后，执行第一条 systematic query 才进入 Stage-1B；Stage-1B 只做 systematic
survey/mapping，仍然不得运行研究模型或 smoke。因此，团队本轮做的文档整改、旧证据考古、编码
schema 与静态测试，都是合法的 Stage-1A 尾门工作，并未因为运行 Python 检查器而越阶段。

**本轮不签署“大规模 survey 立即启动”。裁决为 WITHHOLD。** 不是因为工程门禁不能运行——我在
干净的 Git 提交态中复跑，原九项检查、identity taxonomy test 与 quantifier scan 均通过；真正的
阻塞是：机器正在稳定地重算一个**不完整且部分自相矛盾的研究构念**。如果现在开始大规模编码，
后续将不得不对全部纳入文献返工重编码，而且当前的“严格身份”“K 池占据”和“speech/omni 空位”
计数会系统性误导 Stage-1C 选题。

本轮两项 Gate MAJOR 是：

1. **`is_project_strict_identity` 并不是项目的严格身份；它只是一组权重、标签、信息访问与 API
   访问位。** 它漏掉单一冻结 omni 核心、非文本模态因果进入核心、顺序式 decision rights、控制
   时域、控制器/终态 selector 角色以及选择对象等承重轴。
2. **known-item/carry-forward 的采样框架仍然失衡。** 已深读/首批保证集合以文本、代码、视觉
   system-control 为主，而仓内已经精读过的 agent test-time scaling 与 speech/voice agent 证据没有
   完整进入保证性队列；这与“归档不是遗忘许可”的整改目标冲突。

**是否涉嫌学术欺诈？目前没有足够证据作此认定。** 团队主动承认前轮量词失误、披露 W4 遗留
污染与缺失 artifact、保留负结果，并把外部数字降格为 `SOURCE_REPORTED_TRACEABLE`，这些行为与
蓄意伪造相反。不过，本轮仍存在语义型 QRP：把“脚本对自己定义的一致性检查”写成“项目严格身份
已经机器验证”，以及把异构组级考古写成“表行机器可数”。若在已知构念缺口后仍把这些数字当作
创新空位证据，则会从可修复的方法错误升级为严重诚信问题。

## 1. 我实际复核了什么

复核对象固定为提交 `746a8b1` 中的回应信，不接受后续工作树漂移替代本轮送审对象。重点核对：

- 阶段正典：`wiki/Research-Methodology.md`、`wiki/Research-Objective.md`、
  `wiki/Project-Thesis.md`；
- 回应与承重附件：identity taxonomy、known-item coding-v2、v5 claim-evidence matrix、
  exposure union v2、protocol amendment-9/10、v5 proposal；
- 机器实现：`sf_identity_taxonomy_test.py`、`sf_quantifier_scan.py` 及既有九项门禁；
- 仓内旧 survey/seed/carry-forward 状态；
- 关键边界论文的官方原文，而不是二手搜索摘要。

在 `wsl -d Ubuntu-24.04`、项目 Python 3.12 环境中，对 `git archive HEAD` 干净展开件复跑：

- package summary：PASS；mutation harness：10/10 PASS；
- record validator：26/26 PASS；routes adjudication：50 routes / 0 violations；
- sentinel：31 `QUERY_HIT` + 3 `SEED_GUARANTEED` + 0 unresolved；
- query compiler：65 条、全部静态约束 PASS；
- child replay：10/10 PASS；real-row dry-run：17/17 PASS；
- T1 routes validator：12/12 PASS；identity taxonomy：5/5 PASS；
- quantifier scan：0 条命中，退出码 0。

所以本报告**不否定工程可回放性已经大幅改善**。本报告否定的是从“程序一致性通过”跳到“研究
构念正确、可据此做 occupancy inference”的推理。

## 2. 阶段判断：现在到底在哪里

### 2.1 当前阶段

当前是 **Stage-1A survey-ready gate**，更精确地说是“Stage-1A 尾门、Stage-1B 启动签署前”。

- systematic discovery/mapping query 尚未执行；回应信继续声明 `discovery_queries_executed=0`；
- 当前工作目的仍是冻结问题、范围、检索、编码与保证性 carry-forward；
- 第一条 systematic query 才是 Stage-1B 的事件边界；
- Stage-1B 是知识证据生产，不是模型实验；
- prior 复现、smoke、方向性原型都属于 Stage-2A，不属于 Stage-1B。

因此，本轮正确的问题不是“结果是否达到论文发表水平”，而是：**这套 survey 机器在批量吞入文献
前，能否忠实区分项目身份、近邻、边界对照与评价工具？** 目前答案仍是否定的。

### 2.2 没有发现的越阶段行为

- W4 历史考古是在登记 inherited exposure，不是新实验；
- known-item 逐 ID 核验、全文阅读、静态 matcher 复现，是 Stage-1A gate 整改；
- Stage-2A 复现合同仍写成无执行力草案；
- 本轮没有以“样本不足”为理由补跑 smoke，也没有把旧方向性数字升级成新证据。

这一点团队处理正确。不要因为本轮 WITHHOLD 而补跑模型；那会制造真正的阶段越界。

## 3. 对上一轮三项 MAJOR 的逐条复核

### 3.1 前轮 P0-1：exposure union——实质改善，证据模式仍有尾债

W4 的两轮考古、W2/W3 零实验核验、仓外 owner attestation、已知更正链与选择污染面，已经把前轮
“明知 W4 缺口仍称全量”的核心问题大体修正。尤其值得保留：

- W4 的 MInDS 污染、oracle-layer selection artifact、selection-overfit 等没有被删掉；
- LOAD-only、FAIL、UNCERTAIN 与有效推理事件分开；
- 粒度异构和 legacy 原始 artifact 不在盘被明示；
- 后续 held-out 对暴露数据集/split 的隔离责任被写出。

但回应信声称“W4 ≈70 事件，按表行机器可数”，v5 矩阵 V5-Q07 也标为机器可算并“独立复验”。
实际 `union v2 §4.1` 是 L/D/S/V/F/C/M/R 等**组级散文**，一行可含 `Hydra smoke×8`、多个 ID、
多个变体或一族运行；文件还明说 changelog 59 运行与约 68/70 的差异来自粒度。当前没有规范化的
event JSONL、唯一 event id 或计数器。因此：

- W4 的**暴露面内容**可以作为高覆盖、带残余不确定性的考古结果；
- `≈70` 只能是 `REVIEWER_INFERENCE/TEAM_ATTESTATION` 级估算；
- 不能称“按表行机器重算”；抽查 pointer 也不等于独立重算。

这不是本轮拒绝 survey 的主因，但必须在回应件/矩阵中降格，或另交规范化事件表与计数程序。

### 3.2 前轮 P0-2：reward/training/信息边界拆轴——局部正确，项目身份仍未编码

这轮正确修复了几件重要事情：Selective TTS 不再因改名被排除 reward-guided 集合；AutoTTS 与
Team-of-Thoughts 的 dev/calibration gold 不再误写成 test leakage；DeepVerifier 的 prompt-only
主路径与 SFT 变体分行。这些纠正应保留。

但新增 taxonomy 的名字越过了它的能力包络。它的字段只覆盖：核心/外挂权重更新、开发标签选择、
部署/test gold、外部 new-info、score type、模型访问、一个 K-pool 布尔位、一个 speech/audio
数据模态布尔位。由此派生的 `is_project_strict_identity` 只检查上述位与
`model_access_level == api_text_only`。它没有检查 S0/RQ-SYS 的系统承重身份。

更严重的是，survey 协议本来已经存在更完整的正典字段：`modality_path`、`budget_horizon`、
`external_state_update`、`tool_use`、`omni_axes`、`rl_identity`、七个 proximity 轴，以及 13 轴
system-control DFS。回应整改没有把 identity 计数投影到这些正典字段，反而另建了一个缩减 schema。
这造成**双 schema 漂移**：散文与 DFS 说的是系统，机器计数说的是权重/标签访问。

### 3.3 前轮 P0-3：claim-evidence matrix——覆盖改善，但两条“机器证据”仍不成立

v5 增补矩阵覆盖了新增比例、论文数字和 owner attestation，比前版可靠。但：

- V5-Q05 称 “trained-PRM 引导 K 池 = 1/9”由同一脚本重算；实际持久化 occupancy 输出没有
  `score_type=learned_rm_prm ∧ pool` 的列表或断言。人工能从 JSON 过滤出来，不等于本件已经
  机器持久化并独立复验。
- V5-Q07 的 exposure 计数问题见 §3.1。
- V5-Q06 由 `strict bits ∧ includes_speech_audio` 推出“strict + reward + pool + speech/omni
  空位”，但 `includes_speech_audio` 只表示论文是否在 speech/audio 上评价，完全不能证明核心是
  单一 omni 模型、非文本模态进入核心，或音频因果参与控制。

所以矩阵不应再把 V5-Q05/Q06/Q07标成当前意义下的 `MACHINE_RECOMPUTED_LOCAL`。

## 4. 多轮敌意评审

## Round A：把机器字段与项目北极星逐项做反向证明

项目正典要求的对象是：围绕**单一冻结黑盒 omni 核心**的外部 reward-guided control plane；
reward/advantage 决定下一步动作，池内选择只是退化特例。把它拆成必要条件后，至少包括：

1. 核心拓扑：单一核心、同一核心多次调用，还是异构多模型/多 agent 联邦；
2. 核心模态：核心是否原生接收 audio/omni，而不是数据集含音频或外部 ASR 转成文本；
3. 黑盒访问：API-only 与 logits/hidden/gradient 分开；输入模态不能与内部访问级别混成一个枚举；
4. 全系统训练范围：核心、controller、verifier、memory/skill updater 是否训练；
5. 标签依赖：开发集选择、test-item gold、部署期标签分别编码；
6. 控制时域：终态一次性 selection，还是跨步 observation→action→feedback→state update；
7. decision rights：route、retry、branch、tool、memory、supply、stop、synthesize 中控制器实际拥有什么权；
8. 奖励作用点：对候选输出、轨迹、动作、工具调用、预算/停止，还是仅离线训练 controller；
9. 信息边界：read-out、环境 observation、外部知识检索、test gold 分开；
10. 终态算子：select one、prune、route、vote、merge、synthesize 不能混写。

当前 `is_project_strict_identity` 只覆盖第 3–5 和第 9 的一部分。故其合理名称最多是“数据/权重/
访问严格位”，不能叫“项目严格身份”。

还有一个内部矛盾：协议正典把 `API-text` 与 `API-multimodal` 分开，而新 taxonomy 删除了
`api_multimodal` 并要求 strict identity 必须等于 `api_text_only`。如果该字段描述输入接口，那么
原生 audio/omni 核心永远无法满足 strict；如果它描述只读取文本输出，那么字段命名和协议枚举均错。
必须拆成“内部可见性级别”与“核心输入/输出模态”，不能继续靠解释补丁维持。

**Gate MAJOR-1 成立。** 当前 1/9 的“strict∧reward∧pool”至多是访问/训练严格位的 1/9，不是
项目系统身份的 1/9。

## Round B：反查 `K pool` 的可比单位

Team-of-Thoughts 的官方论文描述的是异构多模型 MAS：中央 orchestrator 从工具 agent 集合中动态
激活合适的 agent，随后评价并合成输出；其 calibration 还用 ground truth 选择 orchestrator 并生成
能力画像。[官方论文](https://arxiv.org/abs/2602.16485) 与
[全文方法段](https://arxiv.org/html/2602.16485)都支持这一点。这里至少存在“候选工具 agent 池”与
“agent 输出集合”，终态主要是 synthesis，不等同于从 K 个同分布 rollout 中选一个最终答案。

Agentic Coding 则明确分为两种机制：parallel RTV 对 rollout summaries 做 tournament voting；
sequential PDR 把既有 rollout 摘要蒸馏后条件化下一轮 rollout。两者是不同的控制时域与作用点，
官方摘要明确分别列出。[官方论文](https://arxiv.org/abs/2604.16529) 当前 coding-v2 却合并为
`#rtv-pdr` 一行，并只用一个 `explicit_candidate_pool_selection=true` 承载。

因此，当前 3/9 的 `training-free ∧ reward-guided ∧ explicit pool` 混合了：

- 对工具/agent 的 route/activation；
- 对输出或轨迹的 select/prune；
- 对既有轨迹的 summarize/reuse；
- select-one 与 generative synthesis。

这个分母/分子没有统一分析单位。必须增加或接入至少：`selection_object`（output/trajectory/action/
tool-agent/plan）、`terminal_operator`（select/prune/route/vote/merge/synthesize）、`control_horizon`
（terminal/sequential）与 `composed_variant`；RTV、PDR 以及真正的 RTV+PDR 组合应按论文实际实验路径
拆行。否则“占据”只是在统计一个词义过宽的布尔位。

## Round C：反查 reward 分类是否忠实

ToolGate 是一个从轨迹文本与结构特征预测 execute/skip 的轻量外部控制器；论文报告 cross-domain 与
matched-domain trajectory training。[官方摘要](https://arxiv.org/abs/2606.03054)支持“监督训练的
调用门”，但不支持把其部署信号直接命名为 RM/PRM。它不是过程奖励模型，也没有在部署时用 reward
对 K 池搜索；它输出的是训练后的二值门决策。

当前把 ToolGate 的 `score_type` 编为 `learned_rm_prm`，会让 `is_reward_guided=true`，尽管 DFS
散文本身又正确写了“部署无奖励、无 K 池”。这是 schema 强迫事实进入错误枚举的典型症状。应把：

- 信号形态（scalar/pairwise/binary gate/consensus/verifiable outcome）；
- 信号来源（rule/LLM judge/trained classifier/RM/PRM/environment）；
- 信号用途（select/search/route/stop/train-controller/offline diagnostic）

拆开。`learned_controller_gate` 不能借用 `learned_rm_prm`。这会改变 reward-guided 总集合，虽暂不
改变 strict∧reward∧pool 的 1/9，但足以证明当前 taxonomy 还不能冻结后批量编码。

同理，`is_all_system_training_free` 实际只表示“核心与外挂权重均未更新”。团队已在散文中补了
“权重轴”，但字段名仍会诱导下游 AI 把 dev-label 配置搜索也称全系统免训练。建议改成不歧义的
`all_components_weight_frozen`；完整 TF-Strict 再由权重、参数外学习对象、标签与持久状态多轴推导。

## Round D：反查“看过但遗忘”是否真的闭环

仓内已经存在一篇最直接却未进入本轮 8+10 opening queue 的工作：

- **Scaling Test-time Compute for LLM Agents (2506.12928)** 系统比较 agent 的 parallel sampling、
  sequential revision、verifier/merging 和 rollout diversification，且报告 list-wise verification
  的作用。[官方论文](https://arxiv.org/abs/2506.12928) 它早已在 `2026-07-04-stage1-L4-speech-agentic.md`
  精读，并在 seed manifest 登记；离线复核显示其不命中当前 65 query，但靠 seed 保证发现。

这意味着它不会从整个 survey 消失，但它仍揭示 carry-forward 不完整：proposal 声称开局保证队列
由“已深读 8 + reviewer-known 10”组成，却没有把这篇**仓内已深读、直接回答 RQ-SYS/RQ-CTRL**
的工作提升到保证性 13 轴编码。靠 seed 留在 BFS 与“旧 survey direct neighbor 必 carry-forward”
不是同一承诺。

更大的结构性不平衡是 speech/voice 证据：已检视九条 method path 得出 0/9 speech/audio，但团队
本地旧 survey 已精读或题录核验多项本体证据：

- τ-Voice 把可验证任务完成、全双工交互和真实音频放在同一 benchmark，并给出 voice/text 直接
  对照。[官方论文](https://arxiv.org/abs/2603.13686)
- Full-Duplex-Bench-v3 直接评价真实语音、disfluency 与多步工具调用。
  [官方论文](https://arxiv.org/abs/2604.04847)
- EchoChain 专门测中断后的状态更新，且当前 frozen queries 对其题名/摘要可零命中、它也不在 seed
  manifest。[官方论文](https://arxiv.org/abs/2604.16456)
- From Text to Voice 给出保留原标注的 text→audio tool-calling 评价框架，可作为 RQ-OMNI 的配对
  评价工具。[官方论文](https://arxiv.org/abs/2605.15104)

这些多数是 benchmark/evaluation instruments，而不是“已占据 TFRL 方法”的论文；正因为角色
不同，不能硬塞进 method-path occupancy 分母。但它们必须进入一个独立的、保证性
**speech/omni task-and-measurement carry-forward**，否则 Stage-1B 会出现“方法地图很宽，项目本体的
测量地图反而靠自然召回”的倒置。

此外，下列已在 seed/protocol 中的工作不要求在 Stage-1A 全部精读完，但必须在 Stage-1B 开局高
优先级编码，不能被当前 28 篇附录误解为 survey 已经足够：

- IAD / On the Role of Feedback in Test-Time Scaling of Agentic AI Workflows：直接比较 feedback 与
  diversity-only BoN。[官方论文](https://arxiv.org/abs/2504.01931)
- LATS：gradient-free tree search、LM value/self-reflection 与 environment feedback 的系统近邻。
  [官方论文](https://arxiv.org/abs/2310.04406)
- Tree Search for Language Model Agents：真实 web 环境中的 inference-time search。
  [官方论文](https://arxiv.org/abs/2407.01476)
- JitRL：无梯度经验记忆与 advantage，但依赖 logits，是“方法最近、接口不合”的关键边界。
  [官方论文](https://arxiv.org/abs/2601.18510)
- Omni-Decision：training-free omni-modal evidence-state、规划/取证/验证/修复/停止的直接系统威胁；
  它含 web/new-info，不等于项目 strict identity，但对“系统创新点”威胁最高。
  [官方论文](https://arxiv.org/abs/2607.11433)

**Gate MAJOR-2 成立。** 不是要求 Stage-1A 再做一轮无穷 survey，而是要求在第一条 systematic query
之前，把已经知道的直接近邻与本体测量工具做零查询、确定性的 carry-forward，避免批量执行一开始
就带着已知采样框架偏差。

## Round E：诚信与可证伪性敌意检查

### 4.1 没有发现足以支持“学术造假”定性的证据

- 没有发现伪造不存在的论文；本轮抽查的关键题名、作者与核心摘要均能由官方源坐实；
- 没有发现删除负结果或只保留正结果；W4 多条 null、污染和更正链被并列保留；
- 没有发现本轮新跑研究模型后伪称零触碰；clean archive 只能证明仓内结构，外部运行仍是 owner
  attestation，但回应信没有把 attestation 冒充机器证明；
- 外部论文数字明确标成未复算的 source-reported，方向正确。

### 4.2 仍然成立的 QRP 风险

1. **构念偷换**：`project_strict_identity` 的名字比字段实际能力更强；
2. **同源 oracle**：测试器只验证自己定义的字段和自己编写的 counterexample；5/5 PASS 不能验证
   schema 的科学效度；
3. **分析单位漂移**：paper、method path、tool-agent pool、trajectory pool 与 group-event 在不同
   计数中切换；
4. **证据模式升格**：pointer 抽查写成机器重算，人工过滤写成持久化机器输出；
5. **完成态语言仍靠词法拦截**：quantifier scanner 可被“本项目不再有遗漏，唯一方法已经成立”
   或空泛的 `〔SCOPED〕` 逃逸。它可以保留为 lint，但不得叫语义防线，更不能代替 reviewer 对集合、
   分母和分析单位的检查。

这些目前更符合“方法与治理设计错误”，而非故意欺诈。整改应针对构念与证据模式，不要把资源继续
花在元数据篡改或更多词法 mutation 上。

## 5. 引用审查结论

### 5.1 总体评价

v5 附录的 28 条结构为 18 条既有/深读相关项 + 10 条 Stage-1B reviewer-known queue，链接形式
基本稳定；抽查的 Team-of-Thoughts、ToolGate、Agentic Coding、DREAM 等题录未见反幻觉问题。
ATLAS 88.9% 也已经加上 GPQA-Diamond/Fig.7a/特定轨迹子集条件，不再冒充跨基准总体结果。

### 5.2 仍需改的引用/表述

- “§4.1 七篇 + §4.2 八项；18 条”算术表面为 15；其余 3 条 DVD/Seg-Agent/Memory-Augmented 是
  held-out/漂移校准项。应明确写成“15 条两级 DFS + 3 条机制/held-out 校准”，避免让读者误以为
  18 条都属于两节正文普查。
- `Team of Thoughts` 不应缩写成容易与 Tree-of-Thoughts 混淆的 `ToT`；首次出现使用完整题名或
  `Team-of-Thoughts`。
- 论文支持的事实与团队编码判断分列：例如论文支持 ToolGate 是 trained execute/skip controller，
  “属于 RM/PRM”是团队 taxonomy 判断，不能共享同一事实置信度。
- 当前 28 条足以支持 v5 文中局部事实，不足以支持“相关工作已经 comprehensively covered”。团队
  本身也声明 systematic mapping=0，因此只能称 pre-mapping evidence base。

## 6. 作为 proposal，下一步应检查什么、探索什么

Stage-1A 的价值不是提前锁定算法，而是把 Stage-1B 能够回答的地图设计正确。建议把 proposal 的
检查点组织成四张相互关联但不混分母的地图：

### 6.1 系统身份地图

逐 method path 回答：

- 单核还是多核/异构联邦？核心是不是同一个冻结 omni 模型？
- 音频/非文本观测是否真的进入核心，还是 ASR、外部专家或文字描述替代？
- controller 有哪些 decision rights，哪些仍由核心或固定程序持有？
- 控制是终态 select-one，还是多步状态更新、预算与停止？
- controller/verifier/memory/skill/tool 中任何组件是否训练、按标签选择或跨实例更新？

输出不是一个总相似度，而是项目身份逐轴命中/违背/未知。

### 6.2 奖励与控制作用点地图

- 信号来源：verifiable outcome、环境反馈、rule、LLM judge、trained classifier、RM、PRM、共识；
- 信号形式：标量、pairwise、binary gate、文本 critique、置信度；
- 作用对象：token、action、tool call、plan、trajectory、candidate output、budget/stop；
- 作用方式：selection、pruning、routing、revision、state update、synthesis、controller training；
- 反事实基线：等 K majority/MBR、无 feedback 的同预算 sampling、固定 schedule、无 state。

这张图才回答“training-free RL 牵引 external control plane”的实际方法空间，而不是把所有 evaluator
或 judge 统一叫 reward。

### 6.3 Speech/omni 因果与评价工具地图

- benchmark 是否有相同任务的 text/audio paired 条件；
- reward 是否可验证、是否在部署选择时 label-free；
- 失败来自 perception、state update、tool argument、turn-taking 还是 controller；
- 是否存在 pass@k/oracle/headroom，而不只 pass@1；
- 非文本模态是否对控制决策产生因果贡献，可否做 modality ablation；
- full-duplex/中断等动态观测是否要求真正 sequential control。

这张图应独立于方法 occupancy。它为 Stage-1C 的候选问题卡提供“哪里可测、哪里会失败”的依据。

### 6.4 证据与复现准备地图

- 公开代码/数据/模型、许可证、API 依赖与版本；
- 最近 system prior、最强简单基线、负结果 comparator 三类是否各有可复现候选；
- reproduction 是否会违反黑盒/TF-Strict 身份，若违反仅作 boundary comparator；
- 哪些历史 exposure 数据必须排除或分层；
- 论文主张、团队推断、机器结构验证、owner attestation 四种证据模式不得互换。

这仍是 Stage-1B/1C 的知识组织，不是要求现在跑实验。

## 7. 启动大规模 survey 前的精确整改合同

以下均为**零 systematic query、零研究模型调用**的窄幅静态整改；不要求重新设计 65 条查询，也不
要求扩张成新的预 survey。

### P0-1：修正 identity/occupancy schema 的构念效度

1. 不再把当前 reduced taxonomy 的派生位叫 `is_project_strict_identity`；改成反映实际含义的访问/
   权重/标签严格位。
2. 以现有 REC-2/13 轴/`omni_axes`/`rl_identity` 为正典，避免第二套缩减 schema 独立生长；机器
   occupancy 从正典记录投影。
3. 分开内部访问级别与输入/输出模态；API-only 不等于 text-only。
4. 增加/接入核心拓扑、单一核心、核心原生模态、observation seen by core、控制时域、decision
   rights、selection object、terminal operator。
5. RTV、PDR、RTV+PDR 仅在论文确有对应实验路径时分别编码；任何 mixed/composed path 不得用一行
   同时继承两个变体的优点。
6. ToolGate 改为 trained binary controller gate；RM/PRM、classifier 与部署 reward 分开。
7. 重算全部 9 条；删除或降格所有基于旧 strict bit 的“项目空位”表述。

### P0-2：补齐确定性 carry-forward，而不是先开 query 再等它们偶然回来

至少建立三个互不混分母的开局表：

- system/control method paths：现 8 项 + 2506.12928 + IAD/LATS/Tree-Search/JitRL/
  Omni-Decision 等已经登记的直接近邻，按优先级进入 13 轴编码；
- speech/omni benchmark and measurement instruments：τ-Voice、FDB-v3、EchoChain、
  VoiceAgentBench、Audio2Tool、From Text to Voice、tau/tau2 等旧 survey 已知项；
- evaluator/reward/negative priors：PRM/ORM/LLM-judge/majority/MBR/self-verification failure 等。

这些表只保证不遗忘，并不冒充 query recall，也不要求全部在 Stage-1A 精读完。对 `2506.12928`
保留 `SEED_GUARANTEED + PRIOR_SURVEY_CARRY_FORWARD` 双 provenance；对 EchoChain 等 0-hit 已知项
保留 0-hit 身份。

### P0-3：纠正 claim-evidence matrix

- V5-Q05 要么让脚本显式输出并测试 `learned_rm_prm ∧ pool`，要么降为人工可复算；
- V5-Q06 在 full project identity 字段就绪前撤回；
- V5-Q07 降格为考古估计，或提供规范化 event ledger + 唯一 ID + 计数器；
- 所有 occupancy claim 同时写清：集合快照、分析单位、分母、字段合取、证据模式、失效条件。

### P1-1：限定 quantifier scanner 的能力包络

把它写成 reviewer-facing prose lint，只抓明显未限定词，不再称“第七道语义防线”。不需要继续堆
大量词法变异；真正 gate 由集合/分母/分析单位/构念 reviewer checklist 承担。

### P1-2：修正附录角色与计数说明

把 18 条拆成 15 条正文 DFS + 3 条 calibration/held-out；把 Team-of-Thoughts 的简称消歧；
参考文献标注 `DEEPLY_READ / KNOWN_QUEUE / MEASUREMENT_INSTRUMENT / BOUNDARY_COMPARATOR`。

### P1-3：exposure union 的“≈70”不再称机器表行计数

这不要求现在重做考古。最小修复是证据降格与残余不确定性声明；规范化 ledger 可推迟到真正要用
该 union 冻结 Stage-2 held-out 时完成。

### P1-4：增加 schema 的独立语义反例

至少加入三类不由 schema 作者自行挑选的固定反例：

- 多模型 MAS 不能因访问/标签位干净而成为 single-core project identity；
- speech benchmark 不能因 `includes_speech_audio=true` 成为 native omni control method；
- trained binary gate 不能因 learned 被归入 RM/PRM。

反例应由另一位 reviewer/agent 从官方全文提出，测试实现者只负责落码，避免 oracle 与实现完全同源。

## 8. 重新签署的验收条件

下一轮无需再交一份宏大 proposal，只需窄幅整改回应。满足下列条件即可重新申请签署：

1. full project identity 合取能逐字段回指 S0/RQ-SYS，且任何未知字段不得默认为满足；
2. `K pool` 计数按 selection object 与 terminal operator 分层，不再跨工具池/轨迹池/输出池聚合；
3. Agentic Coding 的 RTV/PDR 路径拆分得到论文方法与实验表支持；
4. ToolGate 不再编码为 RM/PRM，reward 来源/用途分离；
5. 旧 survey 的 agent-TTS 与 speech/voice measurement corpus 进入确定性 carry-forward；
6. V5-Q05/Q06/Q07 的证据模式纠正；
7. 干净提交态复跑既有门禁全绿；
8. reviewer 对 schema 做一轮语义复核，出现 **0 新 Gate MAJOR**；
9. owner 再批准后，第一条 systematic query 才启动 Stage-1B；全程仍禁止模型/smoke。

## 9. 最终回答团队的三个问题

**引用是否合理？** 局部事实与题录总体合理，反幻觉工作合格；但 taxonomy 对 ToolGate/候选池的
分类并非论文事实，不能与引用事实混写。28 条只支持 pre-mapping evidence base，不支持综述完成。

**是否有相关论文遗漏？** 有。最明确的 carry-forward 遗漏是已在仓内精读且 seed 保证的
2506.12928；更广的 IAD/LATS/Tree Search/JitRL/Omni-Decision 是 Stage-1B 必查近邻。speech/voice
benchmark 家族不应混入方法 occupancy，但必须作为独立测量证据保证队列。

**是否超越本阶段？** 本轮没有越阶段跑实验；Stage-2A 草案也保持无执行力。真正的问题不是做得
太超前，而是准备批量 survey 的 schema 还没有忠实表达项目身份。

**是否可以开始大规模 survey？** **暂不可以。** 允许且应立即完成上述零查询窄幅整改；整改通过后
即可启动 Stage-1B，不要求再无限扩张 Stage-1A，也不要求预先把全部相关论文精读完。

—— 严格审稿人 / 博导复审，2026-07-18
