---
artifact_id: "SF-STAGE1C-R2-COREVIEW-V3"
role: "R2 开题报告 v3：关闭 round-03 博导评审全部清单项，履行续77 有条件 GO 的生效条件"
status: "V3_DRAFT_PENDING_ROUND04_SUPERVISOR_COREVIEW"
template: "2026-07-29-direction-coreview-template.md (V2)"
review_closed: "wiki/audit/system-first-stage1c-v2/round-03/2026-07-29-r2-doctoral-supervisor-coreview.md (MAJOR_REVISION)"
rulings: "Decision-Log 续76/续77/续78"
evidence_cut: "2026-07-29"
supersedes: "V2（同文件 git 历史，blob 062c253）"
execution_authority: "STAGE2A_WITHHELD"
---

# R2 开题报告 v3：音频驱动的外部知识获取

## §0 整改对照表（round-03 §十四 清单 → 关闭位置与层级）

| # | 清单项 | 关闭位置 | 层级 |
|---|---|---|---|
| 1 | 组织/供给/使用互斥定义 + 统一方法卡重编码 | §1 词典 + §2 方法卡 | proposal |
| 2 | 四类信息作用分开 | §1.3 | proposal |
| 3 | 主张对象声明 | §1.4（续77/78 已裁） | proposal |
| 4 | state/action/reward/transition/policy 实例化 | §4.1 | proposal（数值校准归 authorization） |
| 5 | 模块 FIXED/BASELINE/INNOVATION/EVALUATOR 标注 | §4.2 | proposal |
| 6 | 收窄主张 vs 负控制二选一 | §3.3（选收窄） | proposal |
| 7 | A0–A6 因果阶梯 + gold-entity≠gold-evidence | §5.1 | proposal |
| 8 | 四层评价不合成总分 | §5.2 | proposal |
| 9 | live retrieval 复放矛盾 | §5.3（trace-logging 已放行，续77①） | proposal |
| 10 | 量词收窄 + 深读组织轴本域论文 | §2.3（三篇深读条目已入 §2 方法卡） | proposal |
| 11 | K1–K4 可执行化（定义/power/judge 保真/多重比较） | §5.4 | 定义=proposal；数值=authorization |
| 12 | R2 独立于 R6/R8 的判据回答 | §6 | proposal |

## §1 概念词典与主张对象

### §1.1 三种知识形式的互斥定义（按被改变的系统对象）

| 概念 | 必答问题 | 所属模块 | 不得混入 |
|---|---|---|---|
| 组织形式 | 知识以什么单元/schema/关系/索引/版本/provenance 存在 | source registry、corpus、chunk/schema、index、snapshot | 跨实例经验效用、检索触发、答案仲裁 |
| 供给形式 | 何时取、从哪取、以什么 query 取、取多少、何时停、如何排序压缩后送入上下文 | query builder、retriever、search planner、budget/stop policy、context composer | 证据进入后的融合、最终答案选择 |
| 使用形式 | 已获证据如何被接纳/融合/冲突处理/归因/引用/修订/拒用 | result admission、grounding/fusion、answerer、arbiter、abstention | 索引结构、搜索预算、跨实例写入 |

**两门拆分**（v2 混淆处，本版起严格分用）：**pre-call acquisition gate** = 未见工具输出前决定
是否购买一次调用（信号=先验/预算/历史）；**post-retrieval admission gate** = 已见检索结果、
结果尚未进入冻结核上下文时决定接纳/拒绝/压缩/标冲突（信号=结果与音频实体的 corroboration、
来源质量、与现有证据的冲突）。二者成本与可识别实验不同。

### §1.2 v2 表述更正

- "语音域组织轴=向量库/无组织"更正为：检索表征线拥有**单向量+定长切段+固定 top-k** 的组织
  （见 §2.3 三篇深读），缺的是多粒度单元、音频锚点、跨模态关系、时间版本、provenance、
  conflict/citation/abstain 字段（三篇读集内**逐字段核对为零**）；agentic 线（AudioRAG/
  Omni-DeepSearch）则无持久组织（live web、无快照）。
- "stop/admission/预算是使用形式收敛点"更正为：stop/预算属**供给**，admission 是供给-使用
  边界，grounding/conflict/citation/修订才是**使用**。
- A-MEM/MemRL/经验效用演化属 D2 外部记忆生命周期，不作为 R2 组织空位论据（撤回）。

### §1.3 四类信息作用（每个实验臂/杠杆必须声明其作用类别）

1. **external new information**：web/corpus 提供 waveform 与当前上下文中不存在的事实；
2. **observation re-representation**：ASR/重听/分段/换 query 只是重表达已有信号；
3. **latent-knowledge elicitation**：prompt/分解/采样激发冻结核参数内已有知识；
4. **verification/provenance**：外部证据用于确认/反驳/给出可审计来源。

R2 的研究对象限定为第 1 类（含第 4 类作为其审计面）；第 2 类是 R2 预算的**竞争对手**（见
§3.1 主研究问题），第 3 类归 R1 证据包与 R6。任务结构前提：
`audio observation → entity/event hypothesis → external fact → grounded answer`。

### §1.4 主张对象与红线（owner 已裁，续77③/续78）

主张对象 = **北极星 system-level task capability**；**最终作答权在冻结 omni 核**（原音 +
被接纳证据上作答）。红线：①模型参数不可修改；②不得为任务**新训练模型**（任何训练环节出界）；
③不得**新增 LLM 代答**。工具级冻结组件（embedding 检索器、frozen judge、DSP、搜索引擎）可用，
版本与成本按 C1 合同记录。**与 AudioRAG 的设计对照差异由此确立**：AudioRAG 把作答权交给新增的
Qwen3-8B 文本控制器（其 +9.2pt 无法归因），本系统的控制平面只做证据供给与取舍，作答权不外移
——归因天然干净。

## §2 方法调研（统一方法卡）

每篇承重论文按固定字段卡编码（组织/供给/使用/changed-vs-held/信号/数据-基线-指标-成本）。
篇幅所限，卡片全文如下三层分布：**agentic 线三篇**（AudioRAG/Omni-DeepSearch/VoiceAgentRAG）
的卡片字段已在 v2 §3.1-§3.2 逐项还原（基线表、数据构造、消融、失效轨迹），本版继承并按
§1.1 词典重新归轴；**跨域 donor**（ToolGate/FOVEA/CTA/VOI-search/PRA/AdaCompute 等）继承 v2
§4.2 M1-M8 机制位表；**检索表征线三篇**深读条目如下（2026-07-29 全文深读，数字自 LaTeX 源核对）。

### §2.3 检索表征线三篇（组织轴本域证据，深读层）

**SpeechDPR 2401.13463**（ICASSP 2024）：组织=Spoken Wikipedia 定长 40s 切段（~39k 条/427h）、
单 768 维向量、flat 内积索引，version/provenance 无；供给=无触发判据每查必检、语音波形 query、
单跳、固定 K=20；使用=top-20 无准入全量入 reader，conflict/citation/abstain 全无。**有训练**
（UASR+TDR teacher 蒸馏进双编码器；HuBERT 冻结）。关键数：top-20 检索 19.73%（级联 teacher
19.94%）；去蒸馏崩至 0.04%；gold passage 下 reader 上限也仅 11.17 FF1；WER>40% 时端到端显著
优于级联；集成（teacher+SpeechDPR）28.88% 显示误差不相关。

**SpeechRAG 2412.16500**（ICASSP 2025）：组织=SpokenSQuAD/VoxPopuli 预切段、单向量
（E5-Mistral 冻结）；供给=文本 query→音频段（方向与 SpeechDPR 相反）、单跳固定 top-5；使用=
top-5 音频拼进 SLM prompt，无准入。**有训练**（adapter 且语音编码器一并解冻；SLM 完全不微调
——生成侧 training-free 与我们红线同形）。关键数：检索几乎无损（SpokenSQuAD 0.9702 vs GT
0.9707），但生成 EM 仅 0.3522 vs GT 文本 0.7514，低 WER 级联 0.5019 也胜之；仅高 WER 区反超
（VoxPopuli 45% WER：检索 0.7106→0.9952）。**检索持平≠端到端持平；瓶颈在 context placement
与长音频上下文容量**（作者自归因）。

**WavRAG 2502.14727**（2025，ARR 在审）：组织=文本-音频混合 KB（Gemini 生成扩展知识）、单向量
（Qwen2-Audio LoRA 后末 token）；供给=instruction+query 单跳固定 top-k；使用=CoT+Universal
Self-Consistency（纯 prompt 级）。**有训练**（LoRA 1.5M 样本/4×A800；generator GPT-4o 只
prompt——但其角色属"新增 LLM 代答"形态，红线下不可搬）。关键数：8.35–14.38× 检索加速；
**Table 3 零训练下限**：不训练直接拿 Qwen2-Audio 当 embedder，Spoken-SQuAD R@1 仅 0.3407、
自建集 0.0675；top-2→top-3 反降（0.6408→0.5129）——多条异质证据的**编排**是真瓶颈。

**三篇读集内小结**：(a) 绕过 ASR 的音频检索在检索段可行且高 WER 区显著占优——组织轴不是空地；
(b) 三篇**全有训练环节**→红线下只能作方法论基线/对照，组件不可搬（未找到任何已发布检查点，
资产核查列 authorization 义务）；(c) 组织 schema（版本/provenance/conflict/citation/abstain）
三篇逐字段为零、供给全是"无判据+单跳+固定 top-k"、**端到端瓶颈共同落在 context placement**
——这恰是纯 prompt 级、training-free、无需新模型即可介入的位置，与 agentic 线的 over-search
失效面（v2 §3.2）拼成 R2 的完整台阶。可复用公共评测锚：SLUE-SQA-5 与 Spoken-SQuAD（各被两篇
使用，可跨篇对齐）；混合模态方向无可复用官方资产。

### §2.4 量词纪律（v2 P1 整改）

本版全部"缺席/空位/瓶颈"断言的量词范围 = 本地已登记且完成相应深读的读集（agentic 线 3 篇深读
+ 检索线 3 篇深读 + donor 73 条 + D1 读集 6 篇），cut 2026-07-29。不作"整个领域"断言。跨域
机制位（M1-M8）只产生 candidate hypothesis；其博士级成立必须来自 §3.1 的音频特有结构，而非
"文本域较早出现"。

## §3 待开展研究的内容

### §3.1 主研究问题（round-03 §十/§十二 采纳）

> 在"音频先确定实体/事件、答案依赖外部事实"的任务上，冻结黑盒 omni 系统能否仅凭部署可见
> 信号，估计一次外部证据动作的边际价值，并在**固定知识环境、等资源**条件下，相对最优固定
> 检索策略，同时提高任务效用、降低 evidence-induced correct→wrong、减少无效检索？

**音频特有结构（独立性的核心论据）**：外部检索 query 依赖一个**可能听错的实体假设**；错误
音频实体会产生**高度相关但完全错误**的外部证据（文本域 RAG 无此失效形态——文本 query 不会
"听错"）；系统必须区分 **perceptual uncertainty**（该重听/换 query 表达）与
**external-knowledge uncertainty**（该多搜外部事实），并把预算在 `re-resolve audio` 与
`search external facts` 两个不同信息源之间分配（§1.3 的第 2 类 vs 第 1 类信息作用之争）。
证据支撑：Omni-DeepSearch oracle 分解（entity-only 33.76 / 端到端 43.44 / gold-entity 50.00
——实体修复与检索改进是两个独立的 headroom）与 A.6 over-search 轨迹。

**三个有序子问题**（不同时宣称全部创新）：
- SQ1 **Necessity**（诊断层）：逐实例的缺口归类——音频感知、外部知识、还是推理（离线诊断，
  用 A0/A1 臂差分，不做部署 need-detection——v2 对 H1 的判死继承）；
- SQ2 **Supply**（主创新候选）：固定 store/固定 use 下，audio-conditioned 的
  query/re-resolve/hop/stop 调度是否优于 best-fixed 预算；
- SQ3 **Use**（次创新候选）：固定 evidence set 下，admission/grounding 是否优于无条件拼接。

**明确不研究**：部署期 need detection（无负类，继承）；知识组织层本版为**冻结实验合同**
（FIXED），只有当实验证明现有索引无法承载 audio anchor/provenance/多假设 query 时才升级为
方法变量（round-03 §十二 建议采纳）。

### §3.2 与其他 R 的管辖界线（判据均匀适用）

R2 = 外部知识 action family 的**专用**调度与证据取舍：其状态含实体假设不确定性、其动作含
re-resolve/search 二选、其风险含相关-错误证据污染——这些是检索特有的，不与 R6 的通用轨迹
控制同形。R6 消费 R2 产出的 action 定义；R8 消费其可靠性阈值。若审查发现 v3 方法退化为
"通用 VoI/stop 换个 benchmark"，按 round-03 §十三 合并判据路由 R6/R8（§6 逐条对照）。

### §3.3 载体主张收窄（round-03 P0-4 二选一：选收窄）

只研究 **external-required 分布内**的 search depth、re-resolve/search 分配、stop 与
admission；不宣称解决通用 knowledge-need detection。负控制不自建：A5 臂（shuffled/irrelevant/
conflicting evidence）在官方数据上构造扰动**不新增标注**，用于测盲从与污染，不用于 need
检测主张。`no-tool direct`（A0）定位为**必要基线与实验卫生**，不作为立项贡献（v2 表述撤回）。

## §4 方法合同

### §4.1 五元组实例化（proposal 级；数值校准=authorization 级）

```text
state_t   = { 音频实体/事件假设集 H_t（含各假设的自一致性计数）,
              evidence_state E_t（已接纳证据+来源+与 H_t 的 corroboration 标记）,
              预算余额 b_t（分维：core calls / search calls / audio seconds）,
              动作历史与各动作后的候选答案漂移记录 }
action_t  ∈ { RE_RESOLVE_AUDIO（重听/换 query 表达；第2类信息作用）,
              SEARCH(q)（外部检索；第1类）,
              ADMIT(e)/REJECT(e)（post-retrieval admission gate）,
              ANSWER（冻结核在原音+E_t 上作答）, STOP/ABSTAIN }
reward_t  = 部署可见信号的显式组合（不合成总分，分量各自报告）：
            r_consistency（同一假设下候选答案的 counts-only 一致性变化）
            r_corroboration（检索结果与音频实体假设的相互印证，frozen judge 可选）
            r_cost（按 AdaCompute 形状的分维成本记账）
            ——校准义务：授权前对离线 delta_E 做 calibration 与误差界（§5.2 合理性层）
transition: SEARCH 的输出先进 E_t（不进核上下文）；仅 ADMIT 的证据进入核上下文；
            RE_RESOLVE 更新 H_t；一切写入带 provenance。
policy    : 阈值化 advantage 规则（确定性逻辑，不新增 LLM）：每步比较
            估计边际价值(候选动作) vs 动作单价，低于单价即 STOP/ANSWER；
            阈值归属=执行合同预注册，禁止用 test gold 调。
            与"prompt 让 LLM 自行决定 stop"的可识别差异：决策量、阈值与记账全部
            外显、可审计、可消融（A4 臂 vs 自由生成 controller 臂直接对比）。
```

### §4.2 模块标注表（round-03 P0-3）

| 模块 | 本版状态 | 最低对照 |
|---|---|---|
| 知识源与索引 | **FIXED**（执行合同冻结一种；trace-logging 复放） | 不静默变化 |
| audio→query | **BASELINE VARIABLE**（single- vs multi-hypothesis） | gold-entity ceiling / single / multi |
| retrieval planner（含 re-resolve/search 分配、hop、stop） | **PROPOSED INNOVATION（主）** | best fixed budget / random matched-cost / always与never 角点 |
| evidence processor + admission | **PROPOSED INNOVATION（次）** | raw top-k / relevance-only / admission |
| context/use（placement、结构化 grounding、原音 re-anchor） | **BASELINE VARIABLE**（三篇深读证明这是共同瓶颈，先测固定策略族） | 同一 evidence set 下 unconditional vs structured |
| controller/evaluator | **OFFLINE EVALUATOR**（frozen judge 可选，续78 合规） | hand rule / terminal-only / offline oracle |

单次实验只动一个 INNOVATION 模块；同时动 planner 与 admission 时必须做析因（A3×A4）。

## §5 实验与评价

### §5.1 因果阶梯 A0–A6（每臂的识别对象）

| 臂 | 识别对象 |
|---|---|
| A0 audio-only direct | incumbent；无外部证据的核表现（SQ1 诊断输入） |
| A1 gold-**evidence** + fixed use | 外部知识对该冻结核的可恢复上界（≠gold-entity：用官方 golden_path 文档本体；证据是否被"使用"以 removal/swap 反事实检验，不以"出现在上下文"为准） |
| A2 retrieved + unconditional concat | 检索管线总收益与 evidence-induced harm |
| A3 同 A2 evidence set + admission/fusion | **使用机制**独立贡献（SQ3） |
| A4 同 store 同 answerer 等成本 adaptive query/re-resolve/hop/stop | **供给策略**独立贡献（SQ2，主杠杆） |
| A5 shuffled/irrelevant/conflicting evidence | 盲从、污染、拒绝与 correct→wrong 风险 |
| A6 offline oracle over executed pool | 已执行 action menu 的 recoverable headroom |

载体：主=Omni-DeepSearch-640（官方三判官协议；四个标准基线阻断项继承 v2 §3.2 如实声明），
次=AudioRAG-500（A/B/C/D 错误分类学+方向一致性）；SLUE-SQA-5/Spoken-SQuAD 作检索线对齐锚
（§2.3）。数据集切分/judge 复现方案/资产 lock=authorization 义务。

### §5.2 四层评价（不合成总分）

**有效性**：反事实边际效用 `delta_E = U(M(x,q,E),y) − U(M(x,q),y)`；报 official accuracy、
paired delta、bootstrap 95% CI、McNemar、SESOI、wrong→correct/correct→wrong、按任务类别/
音频类别/hop 深度分桶。**合理性**（离线诊断量，不进主 leaderboard）：retrieve-skip、
continue-stop、admit-reject 混淆矩阵；reward 估计量对离线 delta_E 的 calibration 与误差界；
answer-bearing coverage、provenance、unsupported claim；A5 下拒绝率与稳定性；removal/swap
反事实。**可靠性**：seed/run 方差、correct→wrong、worst-group/尾部、coverage-quality、跨
音频类型与检索模态符号一致性；abstain 不得靠压 coverage 造安全。**效率**：成本保持向量
`(retrieval hops, result bytes, core calls, audio seconds, controller tokens, judge calls,
wall-clock, API currency, index/snapshot amortized)`；报均值与 P95、超预算失败率、等成本最优
质量、等质量最低成本、accuracy-cost Pareto、每 hop 边际效用；"等预算"在执行合同中指明是
逐实例 hard cap 还是平均预算、在哪一维。

### §5.3 复放与污染审计（续77① trace-logging 已放行）

pin 搜索服务/日期/query/参数；逐次落盘返回的 URL/document ID/rank/content hash；共享查询
跨臂复用同一返回；adaptive 独有查询保留完整 trace 与内容 hash；单列 source-page
reachability/metadata contamination strata。如实标注：这是复放日志，不是数据集，不冒充参考
论文资产。v2 的"阻断项 vs 不补快照"矛盾就此闭合。

### §5.4 击杀阈值可执行化（定义=本版；数值=authorization 前 power analysis 定）

- K1（主杠杆）：等预算 A4 vs 最优固定档，paired delta 95% 下置信界 ≤0 → 杀 SQ2 独立主张，
  回落 MERGE。SESOI 数值以实际 test n、baseline rate、discordant 对数与 judge noise 做
  power analysis 后预注册（`TBD_AT_AUTHORIZATION`，v2 的 +2.0pt 降为占位参考）。
- K2（over-search 可执行定义）：设 t* = 首个"E_t 已含 answer-bearing 证据（离线以 gold 判定）
  且当步候选答案正确"的步；若最终答案错误且 t>t* 有额外 SEARCH，计一次 over-search 失效。
  判定者=离线 judge 协议（judge prompt、重复性、异质 judge 复核进 metric contract）。A4 未
  把该率相对最优固定档降低（non-inferiority margin 预注册，非点估计相等）→ 调度杠杆判死。
- K3（复制判据）：AudioRAG-500 上按预注册 replication criterion 判方向一致性（无统计分辨力
  的轻微负值不自动算符号翻转）。
- K4（admission）：A3 未降低 Knowledge-error 且 type-D 不增 → admission 判死，仅留 R5/R8
  组件。
- 全部多杠杆×多数据集×多分桶比较按预注册 multiplicity correction（Holm/max-T，复用 W1 已有
  统计基建）。

## §6 独立性判据逐条回答（round-03 §十三）

| 支持独立的条件 | v3 的回答 |
|---|---|
| 对象限定为外部知识 action family | §3.2 ✓（含检索特有风险面） |
| 利用音频特有 query/entity 不确定性 | §3.1 核心机制 ✓（re-resolve vs search 预算分配） |
| 同一 controller 形状下可识别检索特有状态/动作/风险/成本 | §4.1 state 含 H_t 与 corroboration ✓ |
| 至少一个实验单独归因 R2 模块 | A3/A4 各自独立归因 ✓ |
| 与 incumbent 和 SOTA 同任务闭合比较 | A0 + 固定档复现 + 官方协议 ✓ |

| 应合并的条件 | 触发即路由 |
|---|---|
| 唯一新内容=通用 query/hop/stop policy | round-04 及执行期任一审查确认 → MERGE 至 R6/R8 |
| 信号/状态/阈值与其他 action family 完全同形 | 同上 |
| 音频只是输入载体 | 同上 |
| 只能整条 wrapper 运行无法独立消融 | 同上 |

## §7 边界、暴露与处置

- 红线与合规：§1.4；API-only；test gold 永不进 controller（K2 的 gold 判定属离线诊断，单列
  记账）；数据/指标复用官方口径；H5 withheld，跨域只借形状。
- 本版 exposure（2026-07-29）：新增=检索线三篇全文深读（LaTeX 源核对）；无新检索、无模型/API
  执行、无指标运行、无下载、无原型。累计 exposure 记账继承 v2 §6。
- authorization 前义务清单：K1-K4 数值（power analysis）、judge 保真合同、数据集 lock 与
  切分、检索服务 pin、三篇检索线论文的检查点发布状态核查。
- **处置**：续77 有条件 GO 的生效条件即本版关闭 §0 清单；按 owner 流程，本版先送 round-04
  隔离博导评审，零 MAJOR 后连同评审与回应一并交 owner 做生效裁定。

**owner 裁定栏（续77 已录，生效待 round-04 后确认）**：`CONDITIONAL_GO_STANDALONE_PENDING_
V3_CHECKLIST` / 2026-07-29 / Decision-Log 续77；红线细化=续78。
