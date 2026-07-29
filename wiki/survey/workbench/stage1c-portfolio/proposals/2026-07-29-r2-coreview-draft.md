---
artifact_id: "SF-STAGE1C-R2-COREVIEW-V5"
role: "R2 开题报告 v5：关闭 round-05 复审 3 新 MAJOR + MAJOR-C 残留 + 5 MINOR"
status: "V5_DRAFT_PENDING_ROUND06_SUPERVISOR_COREVIEW"
template: "2026-07-29-direction-coreview-template.md (V2)"
reviews_closed: "round-03/04/05 (均 MAJOR_REVISION), wiki/audit/system-first-stage1c-v2/"
rulings: "Decision-Log 续76/续77/续78"
evidence_cut: "2026-07-29"
supersedes: "V4（同文件 git 历史，blob f3063b46）；本件自足，不以任何已取代 blob 承重"
execution_authority: "STAGE2A_WITHHELD"
---

# R2 开题报告 v5：音频驱动的外部知识获取

## §0-bis round-05 整改对照（新增于 v5）

| round-05 条目 | 本版修复 | 位置 |
|---|---|---|
| MAJOR-A 差分含义未定 | 信号分层三声明：感知不确定性信号（α1/β 路）**只进 A4b**，A4a 的 V̂(SEARCH) 显式去掉 α1 项；A4a 固定 re-resolve 档的选取规则声明；audCons/disp 给可实现定义并入时序合法性枚举 | §4.1/§5.1/§3.2/§6 |
| MAJOR-B 载体近地板无灵敏度保护 | K 判据加 assay-sensitivity 前置（未过灵敏度检定不得触发任何判死）；§3.4 补载体风险与三级回退 | §5.4/§3.4 |
| MAJOR-C（=04-MAJOR-5 残留） | §5.2 四层评价与九维成本向量全文回填件内，自足性声明恢复为真 | §5.2 |
| MINOR-a..e | readiness 第四行按列义重填并升为承重行；A1′ 声明开放检索模式构造（避免退化为第 2 类信息）；K2 改称"判官抽样复核估计"并给抽样框/判官输入/CI 覆盖对象；oracle 三数标注仅 Gemini-3-Pro 且 A1 严格强于论文 oracle；admission 信号开销入等预算条款 | §3.4/§5.1/§5.4/§2.1/§5.2 |

## §0 双轮评审整改对照（v4 存档）

**round-03 十二项**：#2/#3/#5/#6/#8/#9 已于 v3 关闭（round-04 复核确认）；#1/#4/#7/#10/#11/#12
六项按 round-04 裁定在本版关闭（对应下表）。**round-04 五项 MAJOR + 六项 MINOR**：

| round-04 条目 | 本版修复 | 位置 |
|---|---|---|
| MAJOR-1 音频特有机制无臂识别 | A4 拆 A4a/A4b，独立性主张、K1 与 §6 MERGE 触发全部改挂 `A4b−A4a` 差分 | §5.1/§5.4/§6 |
| MAJOR-2 A1 资产不存在 | A1 改回 gold-entity+gold-path ceiling（对齐论文 oracle）；新设 A1′ 受限 gold-evidence 诊断，仅在官方 gold passage 真实存在的锚数据集上构造；覆盖缺口与图像态证据如实声明 | §5.1 |
| MAJOR-3 决策量缺席 | 前瞻估计量 V̂ 的函数族 + 输入时序合法性在 proposal 层声明；选型与标定列入 authorization 清单；"不合成总分"限定为评价层纪律 | §4.1/§7 |
| MAJOR-4 K2 不可离线判定 | K2 改写为只依赖已授权落盘量（答案轨迹 + rank/hash 轨迹 + 抽样判官复核），如实声明为抽样估计；正文落盘扩展仅作为可选请求单列，不默认 | §5.4 |
| MAJOR-5 方法卡未施加于承重载体/继承已取代 blob | 三篇承重载体六字段卡就地重编码；§2.1/§2.2 恢复；引用枚举与 readiness 表回填件内；全文无"见 v2"承重 | §1.5/§2/§3.4 |
| MINOR-1..6 | 按篇分述归因并降级"context placement"为本项目候选解释；两表 gold-entity 对齐；探针成本计入 A4 预算+双读数；A5 生成器身份声明；模板验收项件内回填；WavRAG 消融改按内容引用 | 各节 |

## §1 概念词典、主张对象与证据底座

### §1.1 三种知识形式的互斥定义（按被改变的系统对象）

| 概念 | 必答问题 | 所属模块 | 不得混入 |
|---|---|---|---|
| 组织形式 | 知识以什么单元/schema/关系/索引/版本/provenance 存在 | source registry、corpus、chunk/schema、index、snapshot | 跨实例经验效用、检索触发、答案仲裁 |
| 供给形式 | 何时取、从哪取、以什么 query 取、取多少、何时停、如何排序压缩送入上下文 | query builder、retriever、search planner、budget/stop policy、context composer | 证据进入后的融合、最终答案选择 |
| 使用形式 | 已获证据如何被接纳/融合/冲突处理/归因/引用/修订/拒用 | result admission、grounding/fusion、answerer、arbiter、abstention | 索引结构、搜索预算、跨实例写入 |

**两门拆分**：pre-call acquisition gate（未见工具输出，决定是否购买调用；信号=先验/预算/历史）
≠ post-retrieval admission gate（已见结果、未进核上下文，决定接纳/拒绝/压缩/标冲突；信号=
corroboration/来源质量/冲突）。

### §1.2 v2/v3 表述更正存档

继承 v3 §1.2 三处撤回（组织轴"无组织"表述、stop/admission 归轴错误、A-MEM/MemRL 论据撤回）；
本版新增撤回：v3 A1 的 "gold-evidence 用官方 golden_path 文档本体"（资产核验不成立，round-04
MAJOR-2）；v3 §2.3 小结"瓶颈共同落在 context placement（作者自归因）"（三篇归因异质，见 §2.3）。

### §1.3 四类信息作用

1 external new information（R2 研究对象）；2 observation re-representation（R2 预算的竞争对手）；
3 latent-knowledge elicitation（归 R1 证据包/R6）；4 verification/provenance（R2 的审计面）。
任务结构前提：`audio observation → entity/event hypothesis → external fact → grounded answer`。

### §1.4 主张对象与红线（owner 已裁）

北极星 system-level task capability；**最终作答权在冻结 omni 核**。红线（续77③/续78）：不改参数；
不为任务新训练模型；不新增 LLM 代答。工具级冻结组件（embedding 检索器/frozen judge/DSP/搜索引擎）
可用，按 C1 记录版本成本。与 AudioRAG（新增 Qwen3-8B 代答、增益不可归因）的设计对照差异由此确立。

### §1.5 证据底座与可回溯枚举（件内自足，MINOR-5/模板验收项 1）

- **深读层（dossier/深读条目在册）**：AudioRAG 2602.10656、Omni-DeepSearch 2605.08762、
  VoiceAgentRAG 2603.02206（d1/d4 dossier + §2.1 方法卡）；SpeechDPR 2401.13463、SpeechRAG
  2412.16500、WavRAG 2502.14727（§2.3，LaTeX 源核对，round-04 抽验 15 项全 ✓）；donor 深读
  （ToolGate 2606.03054、FOVEA 2605.01345、CTA 2602.16699、VOI-search 2605.05701、PRA 2604.09482、
  Decocted 2604.04373、MemRL 2601.03192、AdaCompute 2604.14853、WebThinker 2504.21776、Reflexion
  2303.11366，d6 dossier）。
- **登记未深读（只作机制定位，不引数字）**：2605.13277/2605.15019/2604.25122/2508.21475/
  2605.05185/2605.16481/2605.14906/2605.10848。
- **补抓层（机制级定位，PENDING_DEEP_READ）**：19 篇入引用集（含 pre-2024 例外 6 篇），12 篇仅
  存档——清单与时效规则见 git 历史 v2 §1（此处为记账指针非承重继承）。
- 全部承重引用回溯 `wiki/survey/2026-07-17-sf-fulltext-ledger.jsonl`（sha256+本地路径）。
- **累计 exposure（件内自足）**：文献检索/fetch/全文与 PDF 表格阅读发生（31 篇 known-ID 抓取
  62 行 ledger 全 200；3 次 web 题名→id 解析；三篇检索线全文深读含 LaTeX 源解包；round-04 评审
  执行本地资产读取）。零模型/API 执行、零指标运行、零数据集下载、零复现、零原型。

## §2 方法调研（统一方法卡，全部件内）

### §2.1 agentic 线三篇（承重载体，六字段卡就地重编码）

**AudioRAG 2602.10656**
组织：无持久库；开放 live web（付费 Google Search），无快照/版本/provenance 字段。
供给：文本 controller（Qwen3-8B）Think-Call-Answer 自由生成决定 tool/query/hop；无界 hops、无
显式 stop；两工具 = WebThinker 式 deep explorer + 冻结 omni 作"可查询观察源"。
使用：检索结果与音频回答无条件进 controller 上下文；无 admission/冲突处理/citation/abstain。
changed=新增文本控制器与全 pipeline；held-constant=冻结 omni 本体。
runtime-visible=工具返回文本、omni 回答；gold-only=GPT-4o judge 用的参考答案（评测期）。
数据/基线/指标/成本：500 题（80% 由 GPT-4o 从八个公开集元数据生成，过滤器与错误判官均见 gold
audio attribute）；六裸模型基线（Qwen3-Omni raw 37.0）+ 两 agentic 臂（Qwen3-Omni+Qwen3-8B
46.2）；GPT-4o judge 三次平均 + A/B/C/D 错误分类；无成本记账、无工具消融（+9.2pt 不可归因）；
wrapper 自增 type-D 无效答案（无限循环）。

**Omni-DeepSearch 2605.08762**
组织：无持久库；开放网三工具（text/image/video search）；`golden_path` 仅为实体名链（无 URL/
正文，trace/* 160 条无该字段——round-04 实测），作离线诊断不作运行时组织。
供给：冻结模型自持 query/工具选择/重试/放弃；每步一 query、每步必搜（禁内部知识）；预算=固定档
(X,Y)；video 两阶段 verify-then-densify。
使用：检索结果无条件进上下文；UNKNOWN abstain token 存在但零 coverage 分析；无 admission。
changed=统一 tool-augmented pipeline；held-constant=各评测模型本体。
runtime-visible=检索返回、模型中间答案；gold-only=answer 与 golden_path（构造与诊断期）。
数据/基线/指标/成本：640 题/15 类（五道过滤+人工唯一性复核，构造纪律三篇最严）；12 模型横比
（Gemini-3-Pro 43.44 最强；本项目核 Qwen3-Omni-30B Thinking 6.56）；三 LLM judge 多数投票；预算
消融 (5,1)=29.06→(10,3)=43.44→(15,5)=44.06 且类别强非均匀（IMAGE/SPEECH 升、VIDEO/AMBIENT 降）；
A.6 over-search 完整轨迹（"(10,3) 停下答对，(15,5) 耗尽预算答错"）；oracle 分解 entity-only
33.76/端到端 43.44/gold-entity 50.00；无成本记账、无 no-tool 直读行、单 split 无快照。

**VoiceAgentRAG 2603.02206**
组织：纯文本合成 KB（NovaCRM 12 文档/76 chunk）+ 内存 FAISS 缓存（document-embedding 建索引，
TTL 300s；prediction-query embedding 版本曾致语义错误命中——工程教训）。
供给：预期式——LLM 预测 3–5 后续话题异步预取；数量全为常数；无停止概念（时间驱动）。
使用：单一全局 τ=0.40 决定信缓存或回落；无答案质量轴、无 admission/abstain。
changed=双 agent 预取缓存架构；held-constant=底层向量库与生成模型。
runtime-visible=hit/latency；gold-only=无（全程不评答案质量）。
数据/基线/指标/成本：200 条 scripted 文本轮次；唯一基线 Traditional RAG；hit 75%、110.4ms→
0.35ms、316×；单次运行无方差。处置：仅作 R9 latency/cache 参考，不承担 R2 能力结论。

### §2.2 跨域机制位（donor，只借形状不外推效果）

M1 pre-call gate（ToolGate：11.8/9.9/78.3 基率；prompt 级怀疑无效）｜M2 value-per-budget+双硬
预算（VOI-search：中预算有时胜高预算）｜M3 校准先验判取（CTA：closed-form retrieve-iff；
"always acquire 是默认失效模式"）｜M4 margin-shift VoI 免负类标签（PRA；黑箱可行性待评）｜
M5 forced-answer 四分类离线探针（ToolGate）｜M6 负信息增益/"更相关≠更好"（Decocted）｜
M7 oracle/headroom 行成为标准协议（M3-VQA 四臂；FOVEA selector ablation）｜M8 类别级预算再分配
（AdaCompute Lagrange 单价；Omni-DeepSearch 自证最优预算随类别异而统一封顶）。

### §2.3 检索表征线三篇（组织轴本域证据，深读层；数字经 LaTeX 源核对）

【继承 v3 全部三条目与数字——round-04 抽验 15 项全 ✓——此处保留原文字段卡】
**SpeechDPR 2401.13463**：组织=Spoken Wikipedia 40s 定长切段（~39k/427h）单 768 维向量 flat 内积，
version/provenance 无；供给=无判据每查必检、语音 query、单跳、固定 K=20；使用=top-20 无准入，
conflict/citation/abstain 无。有训练（UASR+TDR teacher 蒸馏；HuBERT 冻结）。top-20 19.73%（级联
19.94%）；去蒸馏 0.04%；gold passage 下 reader 上限 11.17 FF1；WER>40% 端到端显著优于级联；集成
28.88%。**作者对低上限的归因是下游 SQA 模块能力天花板**——此类瓶颈恰非 training-free 上下文干预
可解（MINOR-1 更正）。
**SpeechRAG 2412.16500**：组织=预切段单向量（E5-Mistral 冻结）；供给=文本 query→音频段单跳
top-5；使用=拼 prompt 无准入。有训练（adapter+语音编码器解冻；SLM 完全不微调——生成侧
training-free 与红线同形）。检索几乎无损（0.9702 vs 0.9707）而生成 EM 0.3522 vs 0.7514（低 WER
级联 0.5019 亦胜）；仅高 WER 反超（45% WER：0.7106→0.9952）。**作者归因为长音频上下文容量且带
"possibly" 限定**（MINOR-1 更正）。
**WavRAG 2502.14727**：组织=文本-音频混合 KB（Gemini 生成扩展知识）单向量（Qwen2-Audio LoRA）；
供给=单跳固定 top-k；使用=CoT+USC（纯 prompt 级）。有训练（LoRA 1.5M/4×A800；generator GPT-4o
属"新增 LLM 代答"形态不可搬）。8.35–14.38× 加速；**零训练下限消融**（按内容引用，表号未在源中
确认——MINOR-6）：不训练直接拿 Qwen2-Audio 当 embedder，Spoken-SQuAD R@1 0.3407、自建集 0.0675；
top-2→top-3 反降 0.6408→0.5129——**多证据编排反降是三篇中唯一直接支持"上下文编排是瓶颈"的证据**。

**读集内小结（归因按篇分述，MINOR-1 修复）**：(a) 绕过 ASR 的音频检索在检索段可行且高 WER 区
占优；(b) 三篇全有训练环节→红线下只作方法论基线，组件不可搬（检查点发布状态核查=authorization
义务）；(c) 组织 schema（version/provenance/conflict/citation/abstain）三篇逐字段为零，供给全为
"无判据+单跳+固定 top-k"；(d) 端到端损失的作者归因**三篇异质**——reader 能力天花板（SpeechDPR）/
长音频容量（SpeechRAG，possibly）/多证据编排（WavRAG）。据此，"上下文侧（placement/编排/容量
管理）存在未被系统处理的损失"是**本项目提出的候选解释**，其中仅 WavRAG 一篇直接支持编排读法；
该候选解释通过 A3（同证据集、换使用策略）接受检验，不作为读集共识引用。

### §2.4 量词纪律

全部"缺席/空位/瓶颈"断言的量词范围=本地已登记且完成相应深读的读集（agentic 3 + 检索线 3 +
donor 73 + D1 读集 6），cut 2026-07-29。跨域机制位只产生 candidate hypothesis；独立性论证必须
来自 §3.1 的音频特有结构并由 §5.1 的 A4b−A4a 差分识别。

## §3 待开展研究的内容

### §3.1 主研究问题

> 在"音频先确定实体/事件、答案依赖外部事实"的任务上，冻结黑盒 omni 系统能否仅凭部署可见信号，
> 估计一次外部证据动作的边际价值，并在固定知识环境、等资源条件下，相对最优固定检索策略，同时
> 提高任务效用、降低 evidence-induced correct→wrong、减少无效检索？

**音频特有结构**：外部检索 query 依赖可能听错的实体假设；错误实体产生高度相关但完全错误的证据
（文本域 query 不会"听错"）；系统须区分 perceptual uncertainty 与 external-knowledge
uncertainty，把预算在 `re-resolve audio` 与 `search external facts` 间分配。证据：Omni-DeepSearch
oracle 分解（实体修复与检索改进是两个独立 headroom）与 A.6 over-search 轨迹。
**该机制的实验识别（MAJOR-1 修复）**：由 §5.1 的 **A4b−A4a 差分**唯一承载——A4a 只含通用
自适应 SEARCH 调度（re-resolve 固定），A4b 在其上加 audio-conditioned 双源分配；差分为正且过
K1b 才支持"音频特有"主张，否则按 §6 路由 MERGE。

三个有序子问题：SQ1 Necessity（诊断层，A0/A1/A1′ 差分，离线）；SQ2 Supply（主创新候选，A4a/A4b）；
SQ3 Use（次创新候选，A3）。**明确不研究**：部署期 need detection（无负类）；知识组织层=FIXED
实验合同（除非实验证明现有索引无法承载 audio anchor/provenance/多假设 query）。

### §3.2 管辖界线

R2=外部知识 action family 的专用调度与证据取舍。**"通用调度"在本件中的定义=不见任何感知
不确定性信号的获取调度（V̂_gen）**；"音频特有"=把感知不确定性路由进获取决策（α1/β 路 +
RE_RESOLVE + 双源分配）。R6 消费其 action 定义；R8 消费其可靠性阈值。判据均匀适用：若
A4b−A4a 不显著而 A4a 显著，即"唯一新内容=通用调度"，按 §6 路由 R6/R8。

### §3.3 载体主张收窄

只研究 external-required 分布内的 search depth、双源分配、stop 与 admission；不宣称通用
need-detection。A5 扰动在官方数据上构造、不新增标注；A0 no-tool direct=必要基线与实验卫生，
非立项贡献。

### §3.4 载体 readiness（件内回填，MINOR-5/模板验收项 6）

| 资产 | 本地 | lock | split | 评测依赖 | 缺口/如实声明 |
|---|---|---|---|---|---|
| Omni-DeepSearch-640 | 有（LOCAL_CANDIDATE_UNFROZEN；merged.json 640 条实测可读） | 未入 | 官方仅 train | 三 LLM judge（外部 API） | 无检索快照/负类/dev-test；golden_path=实体链（480 条），trace/* 160 条（25%）无该字段；部分 gold 证据为图像态（如扉页罗马数字例） |
| AudioRAG-500 | 未落盘 | 未入 | 论文未给 | GPT-4o judge | 无 frozen corpus/工具消融；构造期 gold 泄漏入过滤器与判官 |
| VoiceAgentRAG-200 | 未落盘 | 未入 | scripted | — | 无语音/答案质量轴（仅 R9 参考） |
| Spoken-SQuAD / SLUE-SQA-5（**A1′ 承重行**） | 未落盘（公开第三方资产，获取=authorization 义务） | 未入 | 官方 split | gold passage=官方文本/口语段资产（SLUE-SQA-5 的 gold 为 40s 口语段，非纯文本——A1′ 判定协议须按段处理） | A1′ **在开放检索模式下构造**：证据取自该锚的官方 passage 池（外部语料条目=第 1 类信息），非对本题音频的重表达（避免退化为第 2 类）；语音为 TTS/朗读态，作诊断锚不作主载体 |

**载体风险与回退梯（round-05 MAJOR-B）**：项目核 Qwen3-Omni-30B（Thinking）在主载体论文表中仅
6.56，且同表显示弱模型从 search-guided refinement 获益有限（Mimo-V2.5 给定 gold entity 也只有
22.03，论文作者明写）——主载体对本核存在**近地板风险**，correct→wrong 判定的样本基数亦小
（约 40 题量级）。回退梯（触发条件=未过 §5.4 assay-sensitivity 检定）：①按官方 pipeline 校核
本核 prompt/思维链配置后重测灵敏度；②分层收缩到本核有牵引力的类别子集（如 SPEECH/SINGLE），
主张范围同步收窄；③仍地板则主载体降级为方向性可行性证据、AudioRAG-500 升为主载体（其 raw
37.0 远离地板），并如实改写全部 K 判据的载体绑定。判死永不在未过灵敏度检定的载体上宣布。
judge-API 依赖与 split 冻结方案属 Stage-2 执行合同问题，此处登记不解决。

## §4 方法合同

### §4.1 五元组（decision quantity 落位，MAJOR-3 修复）

```text
state_t   = { H_t 实体/事件假设集（含各假设自一致性计数 agree(h)）,
              E_t 已接纳证据（含来源、与 H_t 的 corroboration 标记 corr(e,h)）,
              b_t 分维预算余额（core calls / search calls / audio seconds）,
              动作历史 A_{1..t-1} 与各动作后的候选答案漂移记录 }
action_t  ∈ { RE_RESOLVE_AUDIO, SEARCH(q), ADMIT(e)/REJECT(e), ANSWER, STOP/ABSTAIN }

decision quantity（前瞻估计量族，proposal 层声明；选型与权重标定=authorization 义务）：

  **信号分层声明（round-05 MAJOR-A 修复，差分含义在此唯一定义）**：
  感知不确定性信号（disp/audCons 及 α1 项）**只允许进入 A4b**。A4a（通用调度臂）的估计量为
    V̂_gen(SEARCH(q)|s_t) = α2·gapCorr(E_t, ĥ_t) + α3·nov(q|A_{1..t-1})     ← 无任何 H_t 离散度输入
  A4b 在 V̂_gen 之上新增两件事：
    V̂_aud(SEARCH(q)|s_t) = V̂_gen + α1·(1 − maxAgree(H_t))
    V̂(RE_RESOLVE|s_t)    = β1·disp(H_t) + β2·(1 − audCons(ĥ_t))            ← A4a 中 RE_RESOLVE 不可用
  于是 `A4b − A4a` 的含义被唯一钉住：**把感知不确定性路由进获取决策（含双源分配）的净价值**。
  §3.2/§6 的措辞与此对齐：通用调度=不见感知不确定性的调度。

  可实现定义（入时序合法性枚举）：
    maxAgree(H_t) = 已采样候选答案中实体槽众数占比；disp(H_t) = 1 − maxAgree(H_t)；
    audCons(ĥ_t) = 截至 t 步已执行的音频重呈现（RE_RESOLVE 产出的重听/重询变体）中，首选假设
    ĥ_t 被复现的比例（t 步前无重呈现时定义为 1，即无证据怀疑感知）。
  V̂(ADMIT(e) | s_t) = γ1·corr(e, ĥ_t) + γ2·srcQual(e) − γ3·confl(e, E_t)
  时序合法性：上述全部输入（agree/maxAgree/disp/audCons/gapCorr/nov/srcQual/confl/预算余额）仅
  依赖 t 步及以前已观测量——是"前瞻估计"而非"事后回报"；执行后的实际回报仅用于 §5.2 合理性层的
  离线 calibration（对 delta_E），不进在线决策。
  评价层不合成总分（§5.2 纪律）；决策层的标量组合式即上式（在此显式声明，不再两层缺席）。

policy    : 阈值化规则（确定性逻辑，不新增 LLM）：argmax_a [ V̂(a|s_t) − λ·c(a) ]，且
            max_a [V̂−λc] ≤ 0 时 ANSWER/STOP；阈值 λ 与权重 α/β/γ 归属=执行合同预注册（dev 上
            离线标定，禁 test gold）。与自由生成 controller 的可识别差异：决策量/阈值/记账全部
            外显可审计，且 A4 臂族直接与"prompt 自由决定"对照臂对比。
transition: SEARCH 输出先进 E_t 候选区（不进核上下文）；仅 ADMIT 的证据进入核上下文；
            RE_RESOLVE 更新 H_t；一切写入带 provenance。
```

### §4.2 模块标注表（与 §5.1 对齐，MINOR-2 修复）

| 模块 | 状态 | 最低对照 |
|---|---|---|
| 知识源与索引 | FIXED（执行合同冻结；trace-logging 复放） | 不静默变化 |
| audio→query | BASELINE VARIABLE | **gold-entity ceiling（=A1）**、single-、multi-hypothesis |
| retrieval planner | **PROPOSED INNOVATION（主）**，内部析因 A4a/A4b | best fixed / random matched-cost / always与never 角点 / **A4a（通用调度）** |
| evidence processor + admission | PROPOSED INNOVATION（次） | raw top-k / relevance-only / admission |
| context/use | BASELINE VARIABLE（§2.3 候选解释的检验位） | 同一 evidence set 下 unconditional vs structured |
| controller/evaluator | OFFLINE EVALUATOR（frozen judge 可选，续78 合规） | hand rule / terminal-only / offline oracle |

单次实验只动一个 INNOVATION 模块；planner 与 admission 同动须 A3×A4 析因；planner 模块内
A4a/A4b 析因强制。

## §5 实验与评价

### §5.1 因果阶梯（MAJOR-1/-2 修复后）

| 臂 | 识别对象 |
|---|---|
| A0 audio-only direct | incumbent（实验卫生基线） |
| A1 gold-entity + gold-path ceiling | 音频实体/路径修复的可恢复上界；对齐论文 oracle 分解（33.76/43.44/50.00——**仅 Gemini-3-Pro 口径**，本核数值须自测；A1 因含 gold-path 严格 ≥ 论文 entity-only oracle，是"上界的上界"，如实标注）。覆盖：480/640；trace/* 160 条无 golden_path，单列不计入 |
| A1′ gold-evidence 受限诊断 | 外部证据对冻结核的可恢复上界；**仅构造于官方 gold passage 真实存在的锚数据集**（Spoken-SQuAD/SLUE-SQA-5）；证据"被使用"以 removal/swap 反事实判定，不以出现在上下文为准；如实声明其载体与主载体分布不同 |
| A2 retrieved + unconditional concat | 检索管线总收益与 evidence-induced harm |
| A3 同 A2 evidence set + admission/fusion | 使用机制独立贡献（SQ3；§2.3 候选解释检验位） |
| A4a 同 store 同 answerer 等成本、通用自适应 SEARCH 调度（估计量=V̂_gen，**无任何感知不确定性输入**；re-resolve 为固定档：从 {0, 每题至多 1 次前置重听} 中按 dev 预注册选定，选取规则与档位强度=authorization 预注册项，且 K1a 的对照措辞与之对齐为"最优固定 SEARCH 档 × 选定 re-resolve 固定档"） | 通用 query/hop/stop 的贡献（=MERGE 情形的全部内容） |
| A4b = A4a + 感知不确定性路由（α1 项 + RE_RESOLVE 动作 + 双源分配） | **音频特有机制的唯一识别臂：主张挂 A4b−A4a** |
| A5 shuffled/irrelevant/conflicting evidence | 盲从/污染/拒绝/correct→wrong。生成器：shuffled/irrelevant=同类别跨题确定性重排与采样（无 LLM）；conflicting=跨题证据置换构造（无 LLM 生成内容）；若执行期改用 LLM 生成，按 C1 记录且声明不参与作答（MINOR-4） |
| A6 offline oracle over executed pool | 已执行菜单的 recoverable headroom（A1 缺位处的替补上界） |

载体：主=Omni-DeepSearch-640 + 次=AudioRAG-500（继承）；A1′ 锚=Spoken-SQuAD/SLUE-SQA-5。

### §5.2 四层评价（全文件内，round-05 MAJOR-C 修复；不合成总分）

**有效性**：反事实边际效用 `delta_E = U(M(x,q,E),y) − U(M(x,q),y)`；报 official accuracy、
paired delta、bootstrap 95% CI、McNemar、SESOI、wrong→correct/correct→wrong、按任务类别/音频
类别/hop 深度分桶。
**合理性**（离线诊断量，不进主 leaderboard）：retrieve-skip、continue-stop、admit-reject 混淆
矩阵；V̂ 各分量（含 V̂_gen/V̂_aud/ADMIT 式）对离线 delta_E 的 calibration 与误差界（MAJOR-3
标定义务落点）；answer-bearing coverage、provenance、unsupported claim；A5 下拒绝率与稳定性；
removal/swap 反事实。
**可靠性**：seed/run 方差、correct→wrong、worst-group/尾部、coverage-quality、跨音频类型与
检索模态符号一致性；abstain 不得靠压 coverage 造安全。
**效率**：成本保持向量 `(retrieval hops, result bytes, core calls, audio seconds, controller
tokens, judge calls, wall-clock, API currency, index/snapshot amortized)`；报均值与 P95、超预算
失败率、等成本最优质量、等质量最低成本、accuracy-cost Pareto、每 hop 边际效用；"等预算"指
逐实例 hard cap 还是平均预算、落在哪一维=执行合同预注册。
**探针与信号开销入等预算（MINOR-3 + round-05 MINOR-e）**：`r_consistency`/K2 所需逐步候选答案
探针（A4 独有 core-call）与 admission 侧 `confl/srcQual` 的计算调用，全部显式计入对应臂的等
预算（维度与 cap 形式预注册），并报告"扣除探针成本前/后"双读数。

### §5.3 复放与污染审计（续77① 范围内，未请求扩展）

pin 服务/日期/query/参数；逐次落盘 URL/document ID/rank/content hash；共享查询跨臂复用同一返回；
adaptive 独有查询保留完整 trace 与内容 hash；单列 reachability/contamination strata。**可选请求
（不默认、owner 未裁前不生效）**：将"检索返回正文单向落盘至离线诊断槽（controller 不可读）"作为
续77① 的受限扩展交 owner——若获批，K2 由抽样估计升级为全量判定，§5.4 相应升级。

### §5.4 击杀阈值（定义=本版；数值=authorization 前 power analysis）

**Assay-sensitivity 前置（round-05 MAJOR-B 修复）**：任何 K 判死只在载体通过灵敏度检定后有效。
检定（authorization 预注册数值）：①A1（gold-entity ceiling）− A0 在项目核上 ≥ 预注册最小可检
余量；②固定预算档曲线在项目核上斜率非零；③correct→wrong 事件的可用样本基数 ≥ 预注册下限。
未通过者不触发判死，改走 §3.4 载体回退梯；"判死"与"载体无分辨力"由此可区分。

- **K1a（通用调度有效性）**：等预算 A4a vs 最优固定档，paired delta 95% 下置信界 ≤0 → 调度类
  杠杆整体判死，R2 回落 MERGE-或-kill 讨论。
- **K1b（音频特有性，独立性判据）**：`A4b − A4a` 的 paired delta 95% 下置信界 ≤0 → 音频特有
  主张判死，按 §6 路由 MERGE（即使 K1a 通过）。SESOI 数值=authorization 前 power analysis 预注册。
- **K2（over-search，判官抽样复核估计版；仅依赖已授权落盘量）**：t* = 首个"当步候选答案（离线
  与 gold 比对）正确"的步；over-search 事件 = 最终答案错误 ∧ t>t* 存在 SEARCH。判定输入=已落盘
  答案轨迹与 rank/hash 轨迹；**判官抽样复核**的抽样框=全部 over-search 候选 episode（非全轨迹
  池），判官输入=该 episode 的答案轨迹与动作序列（不含检索正文），CI 覆盖对象=over-search
  事件率的估计；抽样率与判官协议预注册。如实标注：这是"答案轨迹级判定+抽样复核"的事件率估计，
  非证据内容级全量判定。A4b 未把该率相对最优固定档降低（non-inferiority margin 预注册）→
  调度杠杆判死（受 assay-sensitivity 前置约束）。若 §5.3 可选请求获批则升级证据内容级全量版。
- **K3（复制判据）**：AudioRAG-500 上按预注册 replication criterion 判方向一致性（无分辨力的
  轻微负值不自动算翻转）。
- **K4（admission）**：A3 未降 Knowledge-error 且 type-D 不增 → admission 判死，留 R5/R8 组件。
- 多杠杆×多数据集×多分桶按预注册 multiplicity correction（Holm/max-T，复用 W1 统计基建）。

## §6 独立性判据（可判定版）

| 支持独立 | 判定载体 |
|---|---|
| 对象=外部知识 action family 专用 | §3.2 定义 + A4 臂族只含检索域动作 |
| 音频特有机制可识别 | **K1b：A4b−A4a 下置信界 >0** |
| 检索特有状态/动作/风险可识别 | §4.1 V̂ 的 β 分量（音频特有）与 γ 分量（admission）各有独立臂（A4b/A3） |
| 至少一实验单独归因 R2 模块 | A3、A4a/A4b 各自独立归因 |
| 与 incumbent 和 SOTA 闭合比较 | A0 + 固定档复现 + 官方协议 |

| MERGE 触发（任一成立即路由 R6/R8） | 判定载体 |
|---|---|
| 唯一新内容=通用 query/hop/stop | **K1b 不显著而 K1a 显著** |
| 信号/状态/阈值与其他 action family 完全同形 | V̂ 的 β 分量在标定中权重归零 |
| 音频只是输入载体 | A4b−A4a 在全部音频类别分桶中无一显著 |
| 无法独立消融 | A3/A4 析因在执行期不可实施（如实报告即触发） |

## §7 边界、暴露与处置

- 红线与合规：§1.4；API-only；test gold 永不进 controller（K2/A1′ 的 gold 判定=离线诊断单列
  记账）；数据/指标复用官方口径；H5 withheld。
- **authorization 前义务清单**：K1-K4 数值（power analysis）；**V̂ 估计量族选型与权重/阈值标定
  协议**（MAJOR-3 落点）；judge 保真合同（判官 prompt/重复性/异质复核）；数据集 lock 与分层
  切分；检索服务 pin；三篇检索线检查点发布状态核查；探针成本的预算维度与 cap 形式；A5 扰动
  构造的确定性种子协议。
- 本版 exposure：新增=round-04 评审的本地资产读取与本响应的核验（零网络/零模型执行/零指标/零
  下载/零原型）；累计记账见 §1.5。
- **处置**：本版关闭 round-04 全部 5 MAJOR + 6 MINOR 与 round-03 遗留 6 项；送 round-05 隔离
  复审；零 MAJOR 后连同两轮评审与逐条回应交 owner 做续77 生效裁定。

**owner 裁定栏（续77 已录，生效待复审通过后确认）**：`CONDITIONAL_GO_STANDALONE_PENDING_
V3_CHECKLIST`（清单载体已更替为 round-04 §六 三问）/ 2026-07-29 / Decision-Log 续77；红线细化=
续78。
