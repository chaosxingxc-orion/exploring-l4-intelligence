# System-first Research Proposal v3 Consolidated：Stage‑1A 博导式对抗审查

> 日期：2026-07-15  
> 审查身份：外部严格审稿人 / 博士生导师视角  
> 审查阶段：**Stage‑1A（问题界定、广泛 survey、候选问题与纸面原型空间）**  
> 被审文件：`wiki/2026-07-15-system-first-research-proposal-v3-consolidated.md`  
> 被审快照：umbrella commit `18288d110a01ea8aef792b7784211c099e4299e1`；git blob `1ecb1654f8f858a015fedd7cd0be12a1f3e906c7`；SHA‑256 `35C00AC93968F0FCA50092D1C60EBAE7EEC417E33E36B5123915E236FCB23567`  
> 审查边界：本报告只新增一份独立审查记录，不修改 proposal、protocol、manifest、工程源码或团队正在进行的任何工件。

---

## 0. 先给结论：科学上下文可继续使用，但 Gate S1 暂不能签字

本轮必须给出两个相互独立的裁决，不能再用一个模糊的“通过/不通过”覆盖全部问题：

| 审查对象 | 裁决 | 理由 |
|---|---|---|
| v3 作为 Stage‑1A 的整合性科学上下文 | **有条件接受，须作 Stage‑1A 级科学澄清** | 阶段定位、零实验、系统优先、TF‑Strict 假设、候选 RQ 与工程纸面设计总体正确；但仍有证据外推、RL 概念边界、信息来源归因和引用可定位性问题。 |
| 配套 survey protocol 作为 Gate S1 检索设计签字对象 | **退回大修，暂不签字** | 类别覆盖存在系统性盲区；48 条“查询”尚不是可逐字执行的最终查询；75 条截断无溢出规则；16 条二级来源路线不可确定性重放；近期直接竞争工作与基础理论谱系均有明显漏项。 |
| 是否允许执行 survey query | **否，继续保持 0 次执行** | 先修协议，不是先跑后补。修复检索设计属于 Stage‑1A，不等同于设置科研探索预算 cap。 |
| 是否进入 Stage‑1B | **否** | 当前没有完成 Gate S1，更没有完成 survey、候选问题比较和 owner 的 Stage‑1C 选题决定。 |
| 是否要求另起 proposal v4 | **不要求** | 应以 protocol amendment、bundle manifest 和 v3 errata/引用附录修复，避免继续制造元流程文档。 |

总体评价是：**团队对上一轮“不要把 Stage‑1A 审成成稿论文、不要提前冻结实验预算”的纠偏基本响应正确；但把“整合得更完整”误当成了“检索协议已经足以签字”。** 当前主要问题不是实验做得不够，而是 survey 的可计算边界和概念论证仍不够严密。

我没有发现足以支持“捏造、篡改、剽窃或选择性隐瞒实验结果”的证据。原因很简单：本轮没有新实验，也没有新 query 执行。但是，若将目前尚不能重放的协议描述成“任意执行者得到字节一致的 universe”，或将未归档的内部 hostile review 当作已经可核验完成，就构成**科研治理表述失真风险**。这必须在对外形成可信记录前改正，但目前不能越证据指控为学术欺诈。

---

## 1. Stage‑1A 的正确审查标尺

本轮不应要求大样本、显著性、冻结 SESOI、统一算力预算、完整后端或发表级消融。Stage‑1A 要回答的是：

1. 研究对象是否被说清楚，核心术语是否与相邻学科可区分；
2. survey 能否覆盖足以推翻当前身份假设的文献，而非只覆盖支持材料；
3. 候选科学问题是否真的开放，还是已被叙事暗中锁定；
4. 每个核心主张是否标清“已有文献支持、团队历史方向性材料、还是尚待调查的假设”；
5. 未来工程是否有可配置、可替换、可回放的纸面接口，但不在此阶段抢跑实现；
6. survey 本身是否可审计：检索宇宙、纳排、冲突、负结果和每次修订均能追溯。

据此，v3 中以下做法是正确的：

- 明确 Stage‑1A 仍在进行，并保持本轮 0 query、0 数据集/模型/API 实验；
- 不再给模型数、数据集数、GPU 时长等探索性预算设置过早硬 cap；
- 将 omni agentic system 放在第一创新假设位置，将 training‑free RL 作为牵引系统设计的北极星，而非假定它已经被证明；
- 使用严格黑盒与 TF‑Strict 作为当前待调查身份，并保留 survey 证伪后改名或退回 TF‑Core 的出口；
- 承认 selector 只是系统控制平面中的一个算子，而不是整个系统；
- 工程工作限定为 ADR、开源 harness 比较、配置契约和可选 mock/schema，不开展真实 adapter、数据接入或实验；
- 把 Stage‑1B 运行蓝图标记为未来素材，不赋予现时执行效力。

这些不是“宽松”，而是阶段纪律。严格审查不等于用错误阶段的指标惩罚团队。

---

## 2. 对团队回复的逐项判定

### 2.1 已充分吸收的部分

#### A. 阶段身份已经纠正

v3 没有把 Stage‑1A 写成论文验收，也没有声称已选定唯一科学问题。五个 RQ 仍作为调查轴，最终输出仍是 3–5 个候选问题供 Stage‑1C 选择。这是正确的。

#### B. 不再把探索预算 cap 当成 Stage‑1A 治理中心

“不在 Stage‑1A 冻结统一模型/数据/算力上限”是合理修正。后文要求处理 query 返回超过 75 条时的规则，属于**检索全集完整性规则**，不是限制学术探索宽度的 compute cap，两者不得混淆。

#### C. 工程披露比此前诚实

v3 明确当前 Hydra 入口的 RL 主体仍为 stub，既有 custom scripts 也不能自动等价为通用配置实验平台。这个披露与静态工程核查一致，没有以目录或 YAML 的存在冒充已经完成平台化。

#### D. TF‑Strict 与信息边界已经开始拆开

v3 正确认识到：不训练权重/结构并不能自动防止 golden answer、qrel 或答案性检索证据泄漏。TF‑Strict 是更新机制约束，information boundary 是信息来源约束，二者正交。这一修正正确且重要。

### 2.2 只部分吸收的部分

#### E. “系统优先”仍然带有输出级证据向轨迹级结论外推

v3 以 best‑of‑N 和历史方向性观察支持“池内/轨迹内潜在能力大幅高于默认输出”。这里至少混合了两个不同命题：

- **已有一定文献和方向材料支持的命题**：在特定任务、特定能力供给 `c` 和特定采样设置下，输出池可能存在 oracle headroom；
- **尚待 Stage‑1A 调查的命题**：在有状态、工具交互、跨模态的 agent trajectory 中，也存在可由无训练控制平面稳定兑现的 trajectory headroom。

前者不能直接推出后者。建议将原句拆成“已观察到的 output‑pool 现象”和“待调查的 system/trajectory hypothesis”，并且每次写 headroom 都带上供给 `c`、任务、采样和 oracle 信息边界。

#### F. “reward 影响下一动作”不足以自动把系统定义成 RL

这是当前 proposal 最重要的概念风险之一。reward 参与后续动作选择，说明它不是纯 terminal reranking，但它仍可能属于：

- online search / tree search；
- planning 或 model predictive control；
- metareasoning / resource allocation；
- bandit-style adaptive sampling；
- sequential decision process，但没有可辨认的 policy/value/behavior update。

因此，“training‑free RL”可以保留为 owner 的北极星和内部待证身份；在 survey 收敛前，对外的中性描述应优先使用 **reward‑guided inference‑time sequential control**。协议必须提取：状态、动作、反馈、策略表示、跨步更新对象、信用分配、停止规则，以及该方法的作者是否自称 RL。最终由谱系比较决定是否足以保留 RL 名称，而不是靠项目内部定义宣布成立。

#### G. “激活预训练知识”与外部工具注入尚未完成因果归因拆分

如果系统可用检索、工具、环境反馈和记忆，那么性能提升可能来自新信息进入，而非预训练知识被读出。Stage‑1A 应先建立信息来源分类，而不是现在做实验：

1. task‑native observation；
2. pretrained‑knowledge read‑out；
3. deterministic transformation / computation；
4. 由 agent 动作引起的 endogenous environment feedback；
5. exogenous answer‑bearing retrieval / new information；
6. evaluation gold（严格禁止进入决策路径）。

未来每个候选机制都要标明使用了哪一类信息。没有这层分解，不得把由外部答案性信息带来的增益概括成“激活预训练知识”。

#### H. 独立 proposal 的引用定位仍不够

v3 把大量证据放进 manifest 是好事，但正文仍出现“coverage‑vs‑K 对数线性律”“Stechly line”“audio TTC”等承重表达，而没有在同一处给出论文名、稳定 ID 和证据等级。proposal 是科学论证文件，不能要求读者先猜代号再翻 manifest。

最低要求不是扩写长篇 related work，而是给每个承重句附一个短引用块：`论文/报告名 + arXiv/DOI + 支持什么 + 不支持什么 + 当前证据等级`。尤其必须明确：best‑of‑N coverage 证据不自动支持 agentic trajectory control。

### 2.3 尚未吸收或新暴露的部分

- protocol 所谓 48 条 exact query 实际是 48 个检索片段与一段带条件占位符的拼装说明，不是冻结的 48 条最终 API 请求；
- 主检索类别缺少 `cs.CV`、`cs.RO`，与“system‑first / omni agentic”研究对象不相称；
- `max_results=75` 没有总结果数审计、分页或溢出处理；
- 16 个二级来源只冻结了关键词路线，未冻结接口、排序、页数/条数、筛选和导出格式；
- 2022 起始日期覆盖不了该问题依赖的 metareasoning、POMDP、options、UCT 等基础谱系；
- proposal 声称做过 hostile review，但当前 bundle 中没有可定位的 proposal‑v3 hostile review 归档；
- proposal 没有固定其六件配套工件的 commit/blob，未来单独打开 v3 不能确定它引用的是哪一版协议和 manifest。

---

## 3. 引用与文献覆盖审查

### 3.1 当前引用结构的优点

当前 seed manifest 已经从随意列论文进步到带身份、类别和 scope‑pending 状态的结构化种子。对 TF‑Strict 也没有把 IRO、VeGAS、AuTAgent 等含训练方法错误归入严格无训练集合；Training‑Free GRPO 保留 `scope_pending`，而非强行收编。这些处理是严谨的。

同时，v3 不再宣称“首个”“唯一”或“已经达到业界最优”，这显著降低了不当 novelty claim 的风险。

### 3.2 近期直接相关工作仍有实质漏项

以下不是为了堆论文数，而是它们分别能直接挑战 RQ‑OMNI、RQ‑CTRL、TF‑Strict 和系统基座身份：

| 工作 | 为什么必须进入高优先级筛查 | 初步身份，不得预判最终纳入 |
|---|---|---|
| [OmniAgent: Native Active Perception as Reasoning for Omni‑Modal Understanding](https://arxiv.org/abs/2606.19341) | 以 POMDP、迭代 Observation‑Thought‑Action、按需音视频感知和持续文本记忆构造 native omni agent，并报告 test‑time scaling；是 RQ‑OMNI/RQ‑CTRL 的直接上界型竞争工作。 | 使用 Agentic SFT 与 RL，属于 trained comparator，不是 TF‑Strict。 |
| [Cognitive‑structured Multimodal Agent / CMA‑Harness](https://arxiv.org/abs/2607.08497) | 同时覆盖 episodic visual memory、retrieval、multimodal executive controller、工具与 web harness；直接挑战“系统第一创新点”的组件组合新颖性。 | 其抽象/检索策略含 RL 训练，初判为 trained system comparator。 |
| [UCT: Evolving from Tool User to Creator via Training‑Free Experience Reuse in Multimodal Reasoning](https://arxiv.org/abs/2602.01983) | training‑free、推理期自更新、工具创建、经验复用与记忆巩固的组合，对“黑盒外围系统如何持续改善”非常接近。 | 可能是高威胁 in‑scope 或近邻工作，须全文判定其更新对象与信息边界。 |
| [ConMem: Training‑Free Structured Memory for Multi‑Agent Adaptation](https://arxiv.org/abs/2606.08702) | training‑free 结构化记忆卡片/图式用于 agent 适应，可能覆盖系统记忆和 experience reuse 子机制。 | 优先作为 component‑level comparator，是否进入核心威胁池取决于全文。 |
| [Argos: Agentic Multimodal Verification](https://arxiv.org/abs/2512.03438) | multimodal agentic verifier/reward 与控制反馈直接相关，可帮助区分 evaluator、verifier 与 controller。 | 训练型邻近比较，优先级可低于前四项。 |

此外，现有 seed 已包含 Affordance Agent Harness 与 FineVerify，但它们没有进入当前“首批 13 篇双人全文抽取”核心集合。若 protocol 把核心威胁集合限制在 13，可能反而排掉最 system‑first 的工作。建议把这两篇加入初始核心池，与上面至少前四篇一起重新排序；“15 篇”最多只能是**初始核心批**，不能是不可增长的硬上限。

### 3.3 缺失的不是几篇论文，而是一整条基础谱系

当前检索从 2022 年开始、且高度围绕 LLM/agent 术语，会系统性漏掉用来判断本工作究竟是 RL、planning、search 还是 metareasoning 的基础工作：

- Russell & Wefald, [Principles of metareasoning](https://doi.org/10.1016/0004-3702(91)90015-C)（1991）：把计算动作本身纳入效用与资源分配；
- Kaelbling, Littman & Cassandra, [Planning and acting in partially observable stochastic domains](https://doi.org/10.1016/S0004-3702(98)00023-X)（1998）：部分可观测序列决策的基本语义；
- Sutton, Precup & Singh, [Between MDPs and semi‑MDPs: A framework for temporal abstraction in reinforcement learning](https://doi.org/10.1016/S0004-3702(99)00052-1)（1999）：options 与时间抽象；
- Kocsis & Szepesvári, [Bandit Based Monte‑Carlo Planning](https://doi.org/10.1007/11871842_29)（2006）：UCT/带反馈的规划搜索谱系。

这些文献不应与 2022–2026 的直接 novelty pool 混为同一统计集合，但必须增加一条 **foundational lineage lane**：不受 2022 时间窗限制，目标是定义概念和寻找祖先，不用来制造“近期工作数量”。后续还应沿引用链补 value of information、anytime computation、algorithm selection 和 active perception 的代表工作。

### 3.4 新颖性目前只能怎样表述

当前可接受：

> 我们调查一种严格黑盒、权重与结构冻结的 omni agentic control plane，候选机制由 reward 在推理期影响序列行为；其系统组合、适用边界及与既有 planning/search/RL/memory/tool‑use 工作的差异尚待 Stage‑1A survey 判定。

当前不可接受：

> training‑free RL for omni agentic system 本身已构成足够创新，只需效果对标或超过 SOTA。

原因不是否认创新潜力，而是上述直接工作已经表明“omni agent + test‑time control + memory/tool/reward”是拥挤且快速变化的组合空间。创新单元必须在 survey 后落到可比较的系统契约、控制机制或边界定理，不能仅凭口号组合成立。

---

## 4. Gate S1 检索协议：为什么现在不能签字

### 4.1 P0：arXiv 类别宇宙与研究对象不匹配

主协议默认类别为 `cs.CL OR cs.AI OR cs.LG`，语音层追加 `cs.SD OR eess.AS`，但没有系统覆盖 `cs.CV` 和 `cs.RO`。这会漏掉以视觉主动感知、具身控制、机器人 agent/harness 为主类且未交叉到前三类的工作。现有 Affordance Agent Harness 本身就是这种漏检风险的实证例子：手工 seed 能碰到它，不代表系统检索可召回它。

**签字前要求：** 至少在 omni/system/active‑perception/tool‑agent 相关层加入 `cs.CV`、`cs.RO`，并记录每条 query 的实际 category expression。是否加入 `eess.IV` 等类别可由一次纸面 sensitivity audit 决定，但不得靠执行后“看到缺什么再偷偷加”。

### 4.2 P0：48 个片段不是 48 条 exact executable queries

当前协议仍有条件占位符，例如某层“及语音类追加……”；没有逐条冻结完整 `search_query`、URL 编码、`start`、`sortBy`、`sortOrder` 等。按照 [arXiv API User’s Manual](https://info.arxiv.org/help/api/user-manual.html)，这些字段共同决定请求与返回顺序，布尔表达式、引号和括号还需要正确 URL 编码。

“任何执行者将得到字节一致的 universe”在当前状态下是过度承诺。即便同一请求，API 返回时间、元数据更新也未必天然字节一致；真正可保证的是：**请求定义一致、原始响应留存、解析器版本一致、派生集合可由原始响应重建。**

**签字前要求：** 在不调用 API 的前提下，增加离线 query compiler，生成并冻结 `queries.jsonl`。每行至少包含：

```text
query_id
decoded_search_query
url_encoded_search_query
categories
date_from/date_to
start
max_results
sortBy
sortOrder
compiler_version
record_sha256
```

然后对整个文件记录 git blob 与 SHA‑256。这个动作是 Stage‑1A 的协议编译与静态验证，不是执行 survey，更不是 Stage‑1B 实验。

### 4.3 P0：75 条截断没有 overflow/paging 规则

若某查询的 `opensearch:totalResults > 75`，按 relevance 只保留前 75 会系统性删除尾部文献，而且删除机制可能偏向热门措辞。后续 snowball 不能证明被截断部分得到恢复。

**签字前要求：** 冻结以下规则之一并说明选择理由：

1. 分页抓取到 `totalResults`；或
2. 当溢出时按时间段/类别确定性拆分查询，直到每片不溢出；或
3. 若因接口限制不能全取，预先声明分层抽样与其对 completeness claim 的降级。

所有执行均须保存 `totalResults`、每页 `start/max_results` 和原始响应哈希。不得把该规则叫“预算 cap”；这是防止无声截断的完整性控制。

### 4.4 P0：16 条二级来源路线尚不可回放

目前仅有来源名、关键词和人工筛选说明，没有固定：入口 URL/API、排序、时间戳、结果页范围、最大页数/停止规则、登录/地区差异、导出字段和原始证据保存方式。因此它们只能算“检索意图”，不能算可回放路线。

**签字前要求：** 每个二级来源生成稳定 route ID，并冻结：访问接口、完整查询、排序、时间窗口、页码/游标、停止条件、导出 schema、原始截图或响应保存规则。对于无法确定性导出的网页，必须标记 `discovery-only`，其命中文献回到 DOI/arXiv/OpenAlex/Semantic Scholar 等稳定标识核验，不能把网页排序当完整 universe。

### 4.5 P0：基础谱系 lane 缺失

新增独立 lane，至少覆盖：metareasoning/resource‑bounded computation、POMDP/active perception、options/temporal abstraction、bandit/Monte‑Carlo planning、value of information/anytime decision。该 lane 允许从经典 seed 做 backward/forward chaining，并单独报告停止规则。

### 4.6 P0：威胁池与近期扫描必须可增长

首批双人全文抽取应优先覆盖最可能杀死系统新颖性或 TF‑Strict 身份的工作。建议：

- 把 OmniAgent、CMA‑Harness、UCT、ConMem 加入待判定；
- 将 Affordance Agent Harness、FineVerify 移入初始核心威胁池；
- Argos 放入次优先比较；
- 不以 13 或 15 作为最终硬上限，只作为首轮工作队列；
- 每次新增必须记录发现路线，不得仅把支持己方的文献提升优先级。

---

## 5. 工程基座审查：方向正确，但不要把纸面计划写成已具备能力

### 5.1 当前事实判断

静态核查显示：W1 的 Hydra `main.py` 仍有 `TODO: implement the RL loop`；当前配置主要覆盖 model/dataset/rl/experiment 的基础组合；现有 smoke test 与若干定制脚本尚不能证明存在通用 Runner、Controller、StageGuard、TrajectoryRecorder 或可替换的 model/dataset/tool/reward adapters。

因此，v3 所说“现有基座是 stub + custom scripts，需要在后续平台化”是正确的。当前没有伪装实现完成，也不需要在 Gate S1 前补齐这些组件。

### 5.2 Stage‑1A 应完成的工程工作

建议只交付一页 ADR/decision matrix 与 schema mock，比较现有开源 harness 或最小自建薄层能否满足：

| 维度 | Stage‑1A 要问的问题 |
|---|---|
| Backend/provider | 能否通过配置切换本地/远程黑盒模型，且不让 provider 特性渗入科学逻辑？ |
| Multimodal payload | 音频、图像、视频、文本的输入与时间对齐怎样被统一描述？ |
| Dataset/task adapter | item、task metadata、gold、retrieval corpus 是否在 schema 上物理分区？ |
| Controller | reward 如何进入下一步动作；终止、回退、abstain、工具调用由谁管理？ |
| Evaluator/selector/verifier | 评分、验证、候选选择是否拆成不同职责，避免同名异构？ |
| State/memory/tool | 短期状态、长期记忆、外部工具和环境反馈怎样记录来源？ |
| Trace/replay | 每一步 observation/action/reward/config/provider response 是否可重放或至少可审计？ |
| Config export | 一次运行能否导出解析后的完整配置、版本、hash 与随机性来源？ |
| Training‑free guard | 是否能静态/运行时禁止反向传播、optimizer、参数写回、持久化策略更新？ |
| License/maintenance | 依赖是否允许研究分发，维护活跃性和锁版本成本如何？ |

此处的目标是**决定抽象边界**，不是选定最终库，更不是现在写一个大平台。

### 5.3 Stage‑1A 不应做的工程工作

- 不接真实数据集和真实模型跑指标；
- 不实现完整的 GRPO/selector/agent loop；
- 不为了展示进度写某个数据集/模型的一次性定制路径；
- 不用 mock 结果支持科学 claim；
- 不把文本中的 `StageGuard` 当成已经存在的运行时执法；
- 不冻结 Stage‑2 计算资源、数据规模或 SESOI。

因此，当前工程范围本身没有明显越界；风险在于后续团队若把“ADR/接口草图”误当成“可以开始跑实验”。Gate S1 签字也只允许 survey 执行，不授权 Stage‑1B。

---

## 6. 当前研究范畴是否超越 Stage‑1A

### 6.1 合法且必要的 Stage‑1A 工作

- 扩展和重放 survey；
- 建立 RL/search/planning/metareasoning 的概念分类；
- 建立 omni、agentic、TF‑Strict、information boundary 的纳排契约；
- 提出多个候选科学问题和 kill/pivot 条件；
- 做开源 harness 的纸面比较、ADR、配置 schema 和无数据 mock；
- 审查既有历史方向性数字的来源与证据等级，但不重新升级其结论。

### 6.2 已经接近越界、必须继续标红的内容

- “系统创新点已足够，只需超过 SOTA”——这是提前完成 novelty 判决；
- “轨迹潜在能力大幅高于默认”——这是由输出池证据提前外推系统轨迹；
- `RQ‑SYS` 使用“显著高于”——Stage‑1A 尚无冻结统计语义，建议改为“实质性且可复核地高于”；
- “13 篇双人独立全文抽取”若用完成时表达——当前尚未执行，应改为“计划抽取”；
- future blueprint 若出现模型清单、数据清单或运行矩阵，不得被解释为实验排期或授权。

### 6.3 明确越界、现在不得发生的动作

- survey 协议未签字即执行 query；
- 使用 query 结果反复调整关键词而不登记每次改动和理由；
- 跑任何新模型/数据集/API 来选择研究问题；
- 依据方向性小样宣布 SOTA、显著性或确定身份；
- 将 Stage‑1A 自动滚入 Stage‑1B；
- 冻结唯一技术方案、唯一 evaluator/selector 或唯一 harness。

---

## 7. 科研诚信与可回放性审查

### 7.1 当前没有证据支持“学术欺诈”指控

本轮未发现：

- 虚构的新实验或新 query 结果；
- 对照组、失败尝试或样本的选择性删除；
- 将 golden label 进入 selector/reward 的新证据；
- 对论文方法训练状态的明知误分类；
- 抄袭或伪造引用。

所以结论必须写为：**未发现 FFP（fabrication/falsification/plagiarism）证据，不等于所有治理表述均已可信。** Stage‑1A 的主要诚信任务是降低未来不可审计和选择性报告的机会。

### 7.2 四个必须修复的治理风险

#### I. hostile review 声称缺少可定位归档

v3 frontmatter/正文描述已做内部 hostile review，但当前可找到的是 protocol hostile review 报告，未找到与 proposal‑v3 对应的独立记录。若确实做过，应补充最小归档：reviewer/agent 身份、时间、输入快照、问题列表、处置矩阵和产物 hash；若没有可恢复记录，应降级为“内部自检”，不得保留不可核验的完成式。

#### II. “字节一致 universe”超出当前协议能力

未冻结最终请求、分页和二级来源路线时不能承诺 byte‑identical universe。应改成分层承诺：request definition reproducible、raw response preserved、derived corpus replayable。接口侧实时变化必须作为外部不确定性记录。

#### III. 配套 bundle 未在 v3 中固定

建议增加 bundle manifest，逐一记录 proposal、protocol、seed manifest、manifest report、templates、own sweep、protocol hostile review 的 path、commit、git blob、SHA‑256 和角色。以后任何单项更正另加 dated correction，不覆盖历史 hash。

#### IV. 完成时态与计划时态混用

“将双人抽取”“计划执行”与“已完成抽取/复核”必须严格区分。没有 replay 目录与执行记录时，一律使用计划时态。这个问题目前是 provenance 缺陷，不是实验造假；若不修，未来会成为审计争议源。

---

## 8. 给研究团队及其 AI 的强制整改清单

以下工作均属于 Stage‑1A。按顺序完成，不得边修边执行 query。

### P0‑A：科学表述 errata

- [ ] 将 output‑pool headroom 与 system/trajectory headroom 拆成证据和假设两层；
- [ ] 将对外中性术语设为 reward‑guided inference‑time sequential control，RL 身份留待 survey；
- [ ] 增加六类信息来源分解，禁止把 new‑info 增益概括为 pretrained knowledge activation；
- [ ] 将“显著高于”改为 Stage‑1A 可用的“实质性且可复核地高于”；
- [ ] 所有尚未执行的抽取、查询和复核改为计划时态；
- [ ] 给承重概念补最小可定位引用与“支持/不支持”说明。

### P0‑B：检索协议编译

- [ ] 把 48 个片段编译为最终 `queries.jsonl`，不得保留条件占位符；
- [ ] 显式冻结 `start/max_results/sortBy/sortOrder`、日期、类别和 URL 编码；
- [ ] 加入 `cs.CV`、`cs.RO` 的确定性覆盖；
- [ ] 预注册 `totalResults > max_results` 的分页或拆分规则；
- [ ] 为 16 个二级来源建立稳定 route ID、接口、排序、停止和原始证据规则；
- [ ] 对 compiler、query file、route file 记录版本与 hash；
- [ ] 仅运行离线静态测试：ID 唯一、无空字段、无占位符、布尔括号平衡、日期与分页有效。不得联网执行查询。

### P0‑C：文献宇宙补全

- [ ] 加入 OmniAgent、CMA‑Harness、UCT、ConMem 的待判定 seed，并保留发现来源；
- [ ] 将 Affordance Agent Harness、FineVerify 提升到初始核心威胁池；
- [ ] 将 Argos 纳入 verifier 邻近比较；
- [ ] 建立不受 2022 时间窗约束的 foundational lineage lane；
- [ ] 不把初始核心池数量写成最终 hard cap；
- [ ] 对每篇记录 `direct/system/component/foundational`、训练状态、黑盒状态、reward 使用位置和最可能推翻的 RQ。

### P0‑D：审计 bundle 闭合

- [ ] 新建 bundle manifest，固定全部配套工件 commit/blob/hash；
- [ ] 归档 proposal‑v3 hostile review，或诚实降级相关表述；
- [ ] 明确 protocol amendment 的 supersession 关系，不重写旧记录；
- [ ] 由独立 reviewer 只审静态编译产物与上述 P0，不执行 query；
- [ ] 完成后重新申请 **Gate S1 search‑design signoff**。

### Gate S1 签字后，仍然只是 survey 执行许可

获签后才可以：

- 按冻结查询执行并保存 raw response、时间、工具版本和 hash；
- 记录 dedup 前后集合、每篇发现路线和纳排理由；
- 双人独立筛查核心威胁池并保存分歧与裁决；
- 执行 backward/forward chaining，按预注册饱和规则停止；
- 显式报告 null、负结果、身份冲突和被文献杀死的候选方向。

获签后仍然不可以：开始模型/数据集实验、确定唯一技术方案、宣布创新成立、进入 Stage‑1B。

---

## 9. 下一次签字所需的最小证据包

| ID | 必需工件 | 验收问题 |
|---|---|---|
| S1‑E1 | v3 errata / 引用附录 | 是否拆开 headroom、RL 身份与信息来源归因？ |
| S1‑E2 | compiled `queries.jsonl` + hash | 是否逐条可执行、无占位符、字段完整？ |
| S1‑E3 | category/overflow specification | 是否覆盖 CV/RO，并消除 75 条无声截断？ |
| S1‑E4 | secondary routes manifest | 16 条路线是否可回放或诚实标为 discovery‑only？ |
| S1‑E5 | updated seed + foundational lane | 是否补入直接威胁与概念祖先，且未强行归类？ |
| S1‑E6 | bundle manifest | proposal 与所有伴随工件是否被唯一固定？ |
| S1‑E7 | hostile review archive/erratum | hostile review 的完成式是否有证据？ |
| S1‑E8 | offline validation report | 是否只做静态验证、仍保持 query execution count = 0？ |

签字判据：S1‑E1 至 S1‑E8 全部可定位、hash 可复核、无 query 执行、没有用“新增文档数量”替代实质修复。若只补论文名字而不修查询宇宙和溢出规则，仍不签字。

---

## 10. 最终导师意见

v3 相比前版的最大进步，是终于把**研究阶段、系统身份假设、工程诚实披露和未来实验蓝图**放回了正确层级。研究团队没有必要现在证明系统有效，更没有必要现在接受一个会扼杀调研宽度的实验预算 cap。

但 Stage‑1A 的“宽”必须是**可审计的宽**，不是靠 48 个检索片段、若干手工 seed 和“之后 snowball”来代替完整性设计。当前协议对 CV/robotics 的系统性盲区、对 API 截断的沉默、对二级来源的不确定描述，以及对基础决策理论谱系的缺失，足以改变最终选题与 novelty 判断，因此属于大修项，而非文字小修。

我的建议不是再生产一份更长的 proposal，而是用一个小而硬的 protocol amendment 完成上述 P0，并提交编译后的确定性检索工件。做到这一点，Gate S1 才值得签；签完也只是允许团队认真做 survey。**Stage‑1A 仍应保持开放，系统第一与 training‑free RL 都是值得调查的强假设，但目前都不是已经成立的结论。**
