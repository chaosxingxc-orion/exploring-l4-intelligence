---
title: "R2 开题报告 v3：博导视角隔离复审（round-03 清单关闭度裁定）"
date: "2026-07-29"
artifact_type: "DOCTORAL_SUPERVISOR_COREVIEW"
campaign: "system-first-stage1c-v2"
round: "round-04"
review_target: "wiki/survey/workbench/stage1c-portfolio/proposals/2026-07-29-r2-coreview-draft.md"
review_target_commit: "865d2cfac2270613ef12b526cdf08e6b09e31509"
review_target_git_blob: "1397f87645ef5e8741b69d88252ff6777193eb7f"
review_target_worktree_sha256: "22881daaef75c221f2c0bb136bd6bcd473b299b0f5b2c945dddb1e028a0cdb58"
verdict: "MAJOR_REVISION_REQUIRED"
authority_effect: "WITHHOLD_ONLY_NO_OWNER_DECISION_NO_EXECUTION_GRANT"
human_signature_claimed: false
model_or_metric_execution_authorized: false
stage2a_authorized: false
novelty_verdict: "NOT_ISSUED"
---

# R2 v3 复审：证据层显著变强，识别层仍未闭合

## 一、评审结论

**裁决：`MAJOR_REVISION_REQUIRED`。**

v3 不是表面填空。它做了三件 v2 没有做的真实工作：把三种知识形式按"被改变的系统对象"重铸成互斥
词典并主动撤回 v2 的三处错误（§1.2）；补上组织轴本域三篇的全文深读，其承重数字经本评审逐条比对
LaTeX 源**全部准确**；把评价面拆成不合成总分的四层并把复放合同落到续77① 的授权范围内。就
"文献与证据底座"而言，v3 已达到开题报告标准。

但 round-03 的失败合同是 **identifiability（可识别性）**，不是证据充分性。v3 在概念层与叙述层
回答了每一项，却在**实验层**留下同一个缺口：被宣称为独立性核心论据的音频特有机制（`re-resolve
audio` 与 `search external facts` 的预算分配）没有任何一个实验臂能把它与通用 query/hop/stop 调度
分开；作为整条因果阶梯上界锚的 A1 gold-evidence 臂，其所依赖的官方资产经本评审直接核验**并不
存在**；驱动整个 policy 的"估计边际价值"这一决策量在 proposal 与 authorization 两层均未落位。
这三处合起来意味着：**v3 描述的研究对象是唯一的，但 v3 设计的实验无法把它识别出来**——包括无法
判定 v3 自己 §6 下半表写的 MERGE 触发条件。

因此续77 的生效条件（"关闭评审 §十四 全部清单项"）尚未满足：12 项中 CLOSED 6 项、
PARTIALLY_CLOSED 5 项、NOT_CLOSED 1 项。所需整改集中且有界——五项 MAJOR 中四项是设计与措辞级
修订，唯一需要新决定的是 A1 的资产处置。

本文是 AI 生成的博导视角隔离复审，不冒充自然人签字，不授予模型/API 调用、数据获取、指标运行、
原型、Stage-2A、创新性结论、push 或 wiki 发布权限。owner 的独立/合并生效裁定继续 withheld。

## 二、审查对象、范围与本轮实际核验动作

审查对象为 front matter 所绑定的 blob，`git rev-parse` 已独立复核：commit
`865d2cfac2270613ef12b526cdf08e6b09e31509`、blob `1397f87645ef5e8741b69d88252ff6777193eb7f`、
worktree 与 blob 的 sha256 一致（`22881daa…0cdb58`，无 CRLF 偏差）。

本轮不咨询送审方的写作过程，只依据送审件与其绑定证据。除阅读 round-03 评审、Decision-Log
续76/77/78、模板 v2、`Research-Objective.md` 与 `survey/current/research-directions.md` 外，本评审
执行了以下**本地证据抽验**（零网络、零模型调用、零指标运行）：

1. 解压 `E:/…/survey-fulltext/{2401.13463, 2412.16500, 2502.14727}/*.eprint` 三份 arXiv LaTeX 源，
   逐条比对 v3 §2.3 的承重数字与结构事实；
2. 读取 `E:/…/datasets/omni-deepsearch/merged.json`（640 条）核验 v3 §5.1 A1 臂所依赖的
   `golden_path` 字段语义与覆盖率；
3. 取 v2 blob `062c253…` 核验 v3 §2 的"继承 v2 §3.1-§3.2/§4.2/§6"三处继承声明。

### 2.1 §2.3 三篇深读的抽验结果：全部准确

| 断言（v3 §2.3） | 源核对 | 判定 |
|---|---|---|
| SpeechDPR top-20 检索 19.73%，级联 teacher 19.94% | `main.tex` L348/L350 表行 | ✓ |
| 去蒸馏崩至 0.04% | L351 row (d) `00.04` | ✓ |
| gold passage 下 reader 上限 11.17 FF1 | L292 逐字 | ✓ |
| 集成 28.88% | L355 | ✓ |
| WER>40% 时端到端显著优于级联 | L405 "significantly outperforms … when WER exceeds 40\%" | ✓ 逐字 |
| 40s 切段、~39k 条、427h、768 维、内积索引 | L235/L236/L188/L122 | ✓ 全部 |
| HuBERT/SSL 编码器冻结、UASR+TDR teacher 蒸馏 | L179/L194-L202 | ✓ |
| SpeechRAG 检索 0.9702 vs GT 0.9707 | L448/L452 | ✓ |
| 生成 EM 0.3522 vs GT 0.7514 vs 低 WER 级联 0.5019 | L527/L530/L537 | ✓ |
| VoxPopuli ~45% WER：0.7106→0.9952 | L458/L459 | ✓ |
| adapter 与语音编码器一并解冻、SLM 完全不微调 | L343 "Both the speech encoder and adapter are unfrozen"；L106 "Without fine-tuning of the SLM" | ✓ |
| WavRAG 零训练下限 Spoken-SQuAD R@1 0.3407、自建集 0.0675 | 消融表 `Ours`/`Spoken-SQuAD` 行 | ✓ |
| top-2→top-3 反降 0.6408→0.5129 | L454/L455 | ✓ |
| 8.35×/14.38× 加速；1.5M 样本 / 4×A800 | L277/L324/L407/L672 | ✓ |
| 组织 schema（provenance/abstain）三篇逐字段为零 | 三份 tex 中 `provenance`=0/0/0、`abstain`=0/0/0、`conflict`=0/0/1（偶发词） | ✓ 支持 |

**结论：§2.3 的数字层无一处失真，"三篇全有训练环节→红线下只能作方法论基线、组件不可搬"这一
定位结论成立且重要。** 这是 v3 相对 v2 最实质的增量，应完整保留。唯一的越界在该节末尾的因果
归因句（见 MINOR-1）。

## 三、round-03 §十四 12 项复核表

| # | 清单项 | 判定 | 依据（v3 节号 / 核验事实） |
|---|---|---|---|
| 1 | 组织/供给/使用互斥定义 + 统一方法卡重编码 | **PARTIALLY_CLOSED** | §1.1 词典按"被改变的系统对象"定义、三列"不得混入"齐备，§1.2 主动撤回 v2 三处错误，两门拆分在 §4.1 动作集中被真实实例化；但 round-03 §四"最小修复"要求的六组卡片字段只在 §2.3 对检索线三篇部分施加，承重载体 AudioRAG/Omni-DeepSearch/VoiceAgentRAG 未按新词典重编码（MAJOR-5） |
| 2 | 四类信息作用分开 | **CLOSED** | §1.3 四类齐备，并给出 R2 的归属（第1类=对象、第4类=审计面、第2类=预算竞争者、第3类归 R1/R6）；§4.1 动作集逐项回标类别 |
| 3 | 主张对象声明 | **CLOSED** | §1.4 明确 system-level task capability + 作答权留冻结核，与续77③/续78 一致；与 AudioRAG 用 Qwen3-8B 代答的归因对照建立得干净 |
| 4 | state/action/reward/transition/policy 实例化 | **PARTIALLY_CLOSED** | §4.1 的 state/action/transition 实例化到位（H_t、E_t、分维预算、ADMIT 才进核上下文）；reward 只给信号族且与"不合成总分"自相矛盾，policy 依赖的"估计边际价值"函数形式两层皆缺（MAJOR-3） |
| 5 | 模块 FIXED/BASELINE/INNOVATION/EVALUATOR 标注 | **CLOSED** | §4.2 六模块全标注，附"单次只动一个 INNOVATION、同动 planner 与 admission 须析因"约束（MINOR-2 为表间一致性瑕疵，不影响本项关闭） |
| 6 | 收窄主张 vs 负控制二选一 | **CLOSED** | §3.3 明确选收窄；A5 定位为污染/盲从测量而非 need 检测；A0 由 v2 的"贡献"降为实验卫生并显式撤回 v2 表述 |
| 7 | A0–A6 因果阶梯 + gold-entity≠gold-evidence | **NOT_CLOSED** | 七臂齐备，但 A1 所依赖的"官方 golden_path 文档本体"在载体资产中不存在：`merged.json` 640 条里 480 条 `golden_path` 为实体名链、**0 条含 URL 或文档正文**，另 160 条（`trace/*` 四类全部）**无该字段**；v2 §5 L4 把同一资产称作 gold-**entity** 臂，v3 改称 gold-**evidence** 而资产未变（MAJOR-2） |
| 8 | 四层评价不合成总分 | **CLOSED** | §5.2 有效性/合理性/可靠性/效率四层齐备，成本保持九维向量，"等预算指哪一维"显式留执行合同，合理性层明标"不进主 leaderboard" |
| 9 | live retrieval 复放矛盾 | **CLOSED** | §5.3 按续77① 逐项落地，并明标"这是复放日志，不是数据集，不冒充参考论文资产"，v2 的"阻断项 vs 不补快照"矛盾闭合（该日志范围不足以支撑 K2 一事计入 MAJOR-4，不重复扣本项） |
| 10 | 量词收窄 + 深读组织轴本域论文 | **PARTIALLY_CLOSED** | 三篇深读为真且数字全部经核（§二 2.1），§2.4 量词纪律与读集边界成立；但同节小结新引入一条同型过强断言"端到端瓶颈共同落在 context placement（作者自归因）"（MINOR-1） |
| 11 | K1–K4 可执行化 | **PARTIALLY_CLOSED** | K1 的 +2.0pt 降为占位并改挂 power analysis、K3 预注册 replication criterion、K2 引入 non-inferiority margin、全局多重比较修正——四项均落位；但 K2 的**可离线判定性**在现行日志合同下不成立（MAJOR-4） |
| 12 | R2 独立于 R6/R8 的判据回答 | **PARTIALLY_CLOSED** | §6 逐条给出回答且保留 MERGE 路由表；但支持独立的第 2、3 行的 ✓ 是"已描述"而非"可识别"，无任一臂分离音频特有分配与通用调度（MAJOR-1），致使同表下半的 MERGE 触发条件在设计上不可判定 |

**计数：CLOSED 6 / PARTIALLY_CLOSED 5 / NOT_CLOSED 1。**

## 四、新发现问题（分级）

### MAJOR-1：音频特有机制没有任何实验臂能识别它——§6 的 MERGE 判据因此不可判定

§3.1 把"预算在 `re-resolve audio` 与 `search external facts` 两个不同信息源之间分配"立为
**独立性的核心论据**，§6 第 2、3 行据此打 ✓。但检查实验设计：

- §5.1 的 A4 定义为"同 store 同 answerer 等成本 adaptive **query/re-resolve/hop/stop**"——把音频
  特有的 re-resolve/search 分配与通用的 query/hop/stop 调度**捆在同一臂**；
- §4.2 给 planner 的"最低对照"是 `best fixed budget / random matched-cost / always与never 角点`
  ——三者全是通用预算对照，无一能把分配机制从调度机制里剥出来；
- §4.2 只要求 planner × admission 的**跨模块**析因（A3×A4），不要求 planner **模块内**析因。

后果是决定性的：若 A4 胜出最优固定档，该增益既可归于音频特有分配，也可归于通用自适应 hop/stop
——而后者正是 §6 下半表列的第一条 MERGE 触发条件（"唯一新内容=通用 query/hop/stop policy"）。
**即：v3 的实验无法产生任何能区分"应独立"与"应合并"的观测量。** 一个开题报告若其判死条件与其
成立条件落在同一个实验读数上，该设计对研究问题不可证伪。

*最小修复（不需要新研究，只需拆臂）*：把 A4 拆为 A4a（re-resolve 固定为某一确定策略，只对
SEARCH 做自适应 query/hop/stop）与 A4b（A4a 之上再加 audio-conditioned 的 re-resolve/search 分配）。
独立性主张改挂 `A4b − A4a` 这一差分，并把它写进 §5.4 作为 K1 的判据对象；§6 的 MERGE 触发条件
同步改写为"`A4b − A4a` 的 95% 下置信界 ≤0"。

### MAJOR-2：A1 gold-evidence 臂在载体资产上不可构造；gold-entity/gold-evidence 之分被"改名"关闭

round-03 §七 的原话是"`gold-entity` 只隔离音频实体识别，不能替代 `gold-evidence`"。v3 §5.1 的
回应是把 A1 写成"gold-**evidence** + fixed use ……用官方 golden_path **文档本体**"。本评审直接
读取载体资产核验该前提：

```text
merged.json：640 条
  含 golden_path：480 条（image/* 160、single/* 160、multi/* 160）
  无 golden_path：160 条（trace/BIO、trace/ENV、trace/MUSIC、trace/SPEECH 各 40，即全部 trace 类）
  golden_path 中含 http/URL 的：0 条
  golden_path 中含文档正文的：0 条
  形态：实体名链，长度 3–10 跳（众数 5）
  实例：'Mantled howler -> Pallium -> 1917 Code of Canon Law'
```

三点结论：

1. **"官方 golden_path 文档本体"不是一项已存在的资产。** `golden_path` 是维基实体名链，既无 URL
   也无正文。要得到"文档本体"必须另行按实体名抓取并冻结一份 gold 语料——这是一次语料构建，既
   不在 §7 的 authorization 义务清单里，也超出续77① 放行的"落盘检索返回"范围。
2. **该资产的语义恰恰是 gold-entity（加 gold 推理路径），不是 gold-evidence。** v2 §5 L4 对同一
   字段的用法是"复用官方 golden_path 构造 **gold-entity** 臂"。v3 未更换资产、只更换了臂的名字，
   而 round-03 要求的正是这两者**在资产层**分离。这是本轮唯一一处符合"表面填空"特征的整改。
3. **即使补建语料，覆盖率与可达性都不足。** `trace/*` 共 160 条（占 25%，且是四个音频内容分层
   的完整一层）根本没有 golden_path；而上引实例的答案（`MCMXVIII`）是印在某文献扉页**图像**上的
   罗马数字，其 gold 证据根本不是可检索的文本文档。A1 作为整条阶梯的"可恢复上界"锚，其覆盖面
   与证据模态都必须如实声明。

*最小修复（三选一，须在 v4 内定）*：(i) 把 A1 诚实改回 `gold-entity + gold-path ceiling`，并直接
对齐 Omni-DeepSearch 自报的 oracle 分解（entity-only 33.76 / 端到端 43.44 / gold-entity 50.00），
不再宣称它是证据上界；(ii) 保留 gold-evidence 命名，但把它降级为 480 条子集上的受限诊断，写明
构建方式、冻结日期、图像类证据的处置与 25% 的覆盖缺口；(iii) 放弃 A1，改由 A6 承担 headroom
角色并相应削弱 SQ1 的诊断主张。三者都可接受，"沿用现措辞"不可接受。

### MAJOR-3：policy 所需的决策量既未定义，也未被分配到任何一层

round-03 §六 的要求是"必须说明它们如何组合成**决策量**、如何在不使用 test gold 的条件下校准、
阈值由谁拥有、估计器错误如何进入可靠性声明"。v3 §4.1 的回应：

```text
reward_t  = 部署可见信号的显式组合（不合成总分，分量各自报告）：r_consistency / r_corroboration / r_cost
policy    : 阈值化 advantage 规则……每步比较 估计边际价值(候选动作) vs 动作单价
```

三个问题叠加：

1. **自相矛盾。** 同一行里既说"显式组合"又说"不合成总分、分量各自报告"。"不合成总分"是 §5.2
   **评价层**的正确纪律（round-03 §八），被误搬到 §4.1 **方法层**；而阈值化 advantage 规则要与
   "动作单价"比较，在数学上必须有一个标量。决策量因此被这句话取消了。
2. **函数形式缺失且时序不成立。** 三个 reward 分量全部是**动作执行后**才可观测的量（一致性变化
   需已采样、corroboration 需已拿到检索结果），而 policy 需要的是**未执行动作**的前瞻价值估计
   ——这正是 §1.1 自己定义的 pre-call acquisition gate（信号=先验/预算/历史）。从 state 到"候选
   动作的估计边际价值"的映射，v3 全文未给。
3. **两层皆未认领。** §4.1 只把"数值校准"归 authorization；§7 的 authorization 义务清单列了
   K1-K4 数值、judge 保真合同、数据集 lock 与切分、检索服务 pin、检查点核查——**没有**估计量
   设计。于是它既不在 proposal 层，也不在 authorization 层。

这一项的分量不同于其余：SQ2 的研究贡献**就是**"估计一次外部证据动作的边际价值"（§3.1 主研究
问题原话）。贡献的核心构件不能同时缺席于两层。就评审 brief 的具体问题——**§4.1 的 policy 与
"自由生成 controller"的差异是否成立**——本评审的回答是：**架构层成立，估计量层不成立**。确定性
逻辑、外显阈值、预注册归属、可消融、无新增 LLM，这些相对 AudioRAG 式自由生成控制器都是真实且
可审计的差异；但只要决策量本身未定义，"边际价值估计"就还只是一个名字。

*最小修复*：给出估计量的函数形式（哪怕是一个待标定系数的线性/规则族）与其输入的时序合法性
（只用 t 步及以前可见的量），并把"估计量族的选型与标定"明确写入 §7 的 authorization 义务清单；
同时把 §4.1 的"不合成总分"改为"评价层不合成总分，决策层的标量组合式在此声明"。

### MAJOR-4：K2 的 over-search 定义在现行日志合同下不可离线判定

K2 定义为：`t*` = 首个"E_t 已含 answer-bearing 证据（离线以 gold 判定）且当步候选答案正确"的步。
要在离线判定"E_t 是否含 answer-bearing 证据"，必须持有**该步检索返回的正文**。而 §5.3 落地的
日志合同（照抄续77① 的授权范围）是：

> 逐次落盘返回的 **URL/document ID/rank/content hash**；……adaptive 独有查询保留完整 trace 与
> **内容 hash**。

内容 hash 只能证明"内容有没有变过"，**不能**支撑"内容里有没有答案"的离线判定；而 live web 在
实验后必然漂移（§5.3 自己单列了 reachability strata 正是承认这一点）。同时 gold 不得进 controller
（§7），所以该判定也不能改到在线做。结论：K2 目前不可执行——而 K2 是 SQ2 主杠杆的两条判死线之一。

需要注意这不是纯文书问题：把"返回正文"纳入落盘会**扩展 owner 续77① 已批的日志范围**（存储、
版权、污染面均变），属于需要 owner 一句话的边界，不能由执行合同自行扩张。

*最小修复（二选一）*：(i) 在 v4 里显式请求把"检索返回正文单向落盘至离线诊断槽（controller 不可
读）"加入日志合同，作为续77① 的一处受限扩展交 owner 裁；(ii) 把 K2 改写成只依赖已授权可落盘量
的形式（例如以"答案翻转 + rank/hash 轨迹 + 事后对 t* 的判官抽样复核"定义，并如实声明其为抽样
估计而非全量判定）。

### MAJOR-5：统一方法卡未施加于承重载体；件内自足性被"继承已被取代的同路径 blob"打破

§2 用一段话代替了对三篇承重载体的重编码：

> agentic 线三篇（AudioRAG/Omni-DeepSearch/VoiceAgentRAG）的卡片字段**已在 v2 §3.1-§3.2 逐项
> 还原**（基线表、数据构造、消融、失效轨迹），本版继承并按 §1.1 词典重新归轴；跨域 donor……
> **继承 v2 §4.2** M1-M8 机制位表。

本评审取 v2 blob `062c253…` 核验，两点不成立：

1. **该继承声明不准确。** v2 §3.1 是 DFS 四问表（方法/局限/改进空间/可借鉴），§3.2 是数据集
   批判四问；round-03 §四 规定的六组卡片字段中，至少三组在 v2 中对这三篇**根本不存在**——全文
   grep `held-constant`=0、`runtime-visible`=0、`gold-only`=0，`provenance` 仅 1 处且出现在视觉域
   句子里而非任何一篇的字段位。括号里列举的四样（基线表、数据构造、消融、失效轨迹）确实在 v2
   中，但它们不是卡片字段。而"changed / held-constant 模块"与"runtime-visible / gold-only 信号"
   恰恰是**归因纪律**最吃紧的两组。
2. **被继承的对象是同一路径的已取代版本。** v3 front matter 自称 `supersedes: V2（同文件 git
   历史，blob 062c253）`。一份送审件不能一边宣告取代 v2，一边把自己的实质主体寄存在 v2 里；
   读者必须 `git show` 一个已被声明作废的 blob 才能看到承重载体的轴定位。§7 的"累计 exposure
   记账继承 v2 §6"同理。附带地，§2 的小节编号从正文直接跳到 §2.3/§2.4，§2.1/§2.2 在件内不存在
   ——交叉引用悬空。

按 `CLAUDE.md`"Active truth must be self-contained"，以及模板 v2 验收清单（§2 两域三轴演进、§3
数据集批判四问与 readiness 表、§1 引用可回溯枚举），v3 作为 owner 生效裁定的**唯一送审载体**在
件内已无法自证这些项。

*最小修复*：把三篇承重载体按 §1.1 词典 + round-03 六字段卡就地重编码（约一页），并把 §1 元信息/
证据可回溯、readiness 表以现状回填；不得以"见 v2"承重。

### MINOR-1：§2.3 小结把三种异质成因聚合成"共同瓶颈=context placement"，并误挂作者自归因

v3 §2.3 小结：`端到端瓶颈共同落在 context placement——这恰是纯 prompt 级、training-free、无需
新模型即可介入的位置`，且在 SpeechRAG 条目里标注"（作者自归因）"。核对源文：

- **2412.16500**（SpeechRAG）作者原文为：`This is **possibly** due to the difference in the
  durations of the retrieved audios … since SLMs are typically not trained to handle multiple,
  long-context audios.` 作者的归因是**长音频上下文容量**且带 possibly 限定词，**未提 placement**。
- **2401.13463**（SpeechDPR）把 11.17 FF1 的上界明确归因于**下游 SQA 模块能力**（并引 SLUE-SQA-5：
  最佳无配对语音模型仅 21.8 FF1）——这是模型能力天花板，恰恰是 training-free 上下文干预**不能**
  解决的那一类。
- 只有 **2502.14727**（WavRAG）的 top-2→top-3 反降支持"多证据编排"读法。

三种成因被聚合成一个恰好落在本方案可介入位置的"共同瓶颈"，并据此在 §4.2 给 context/use 模块
定性（"三篇深读证明这是共同瓶颈"）。这是 round-03 §十 所批评的同一失败形态在整改稿内的再现。
改法：按篇分述各自的作者归因与限定词，把"context placement"降为**本项目提出的候选解释**而非
读集共识，并撤下"作者自归因"的标注。

### MINOR-2：§4.2 与 §5.1 两表不一致

§4.2 给 `audio→query` 模块的最低对照含 `gold-entity ceiling`，但 §5.1 的 A0–A6 中没有任何一臂
承载 gold-entity（A1 已被指定为 gold-evidence）。两表须对齐——若按 MAJOR-2 的修复 (i) 执行，此项
自动消解。

### MINOR-3：探针调用的成本未计入等预算合同，可能使主杠杆自败

`r_consistency`（同一假设下候选答案的 counts-only 一致性）与 K2 的"当步候选答案正确"都要求
**逐步向冻结核索取候选答案**，这是 A4 独有而固定档基线不需要的 core-call 开销。§5.2 的成本向量
含 `core calls` ✓，但"等预算是逐实例 hard cap 还是平均预算、在哪一维"被整体推给执行合同。若
hard cap 落在 core calls 维，主杠杆的信号采集会吃掉自身预算。建议在执行合同中把探针调用显式
计入 A4 预算并预注册，同时报告"扣除探针成本前后"的双读数。

### MINOR-4：A5 扰动臂的 conflicting evidence 生成器身份未声明

§3.3 称 A5 的扰动"不新增标注"——就标注而言正确。但 shuffled/irrelevant 可由重排与跨题采样得到，
`conflicting` 证据通常需要生成对抗性内容。若由某个 LLM 生成，其身份、版本与成本须按 C1 记录，并
在件内声明它不参与作答（续78 的红线只禁"新增 LLM **代答**"，故合规，但须显式说明以免执行期被
误读）。

### MINOR-5：模板 v2 验收项在 v3 中不可核验

模板 v2 验收清单第 1（引用 100% 本地 hash 可回溯）、2（两域三轴演进）、3（数据集批判四问）、
6（readiness 表无散文代替）在 v3 件内均已不存在（与 MAJOR-5 同根）。若 owner 的生效裁定以 v3 为
唯一载体，则资产就绪度与引用可回溯性无法在件内核验。单列以便一并回填。

### MINOR-6：WavRAG 零训练下限的表号未在源中确认

v3 记作"Table 3"。该消融在 2502.14727 源码中位于对比 `pre-fine-tuned Qwen2-Audio-7B-Instruct`
的章节，表号未能在 LaTeX 源中确认（数字 0.3407 / 0.0675 本身核对无误）。属定位纪律，改为按章节
或表题引用即可。

## 五、关于"proposal/authorization 分层是否被滥用为逃避答题"的专项判断

**总体判断：分层本身未被滥用，但有一处关键内容从两层之间漏掉。**

- **合规的分层**（本评审认可，不要求提前）：K1–K4 的数值（须先有 test n、baseline rate、
  discordant 对数与 judge noise 才能做 power analysis）、judge 保真合同、数据集 lock 与分层切分、
  检索服务 pin、三篇检查点发布状态核查。这些都是"必须先有执行环境才能定"的量，v3 标
  `TBD_AT_AUTHORIZATION` 并列入 §7 义务清单的做法正确，round-03 §十一 也只要求"授权前修复"。
- **不合规的一处**：MAJOR-3 的价值估计量。它既不是数值标定（proposal 层可给形式），也未进
  §7 的 authorization 义务清单，属于**落在两层之间**而非被合法推迟。这是本轮唯一一处分层
  被用来绕过答题的实例，且落在贡献的核心构件上。
- **另一种形态的越界**：MAJOR-5 的"继承已被取代的同路径 blob"不是 proposal/authorization 分层，
  而是**版本分层**，其规避效果更强（读者需 `git show` 一个自称作废的对象），须一并纠正。

## 六、裁决与复审最短路径

**裁决：`MAJOR_REVISION_REQUIRED`。** 续77② 的生效条件尚未满足。

本评审同时明确：**不建议**回退到 MERGE，也**不**给出 novelty verdict。v3 的证据底座、词典、评价
四层与复放合同已达标；缺口全部落在"把已写清楚的研究对象翻译成能识别它的实验"这一步，且五项
MAJOR 中四项（1/3/4/5）是设计与措辞级修订，只有 MAJOR-2 需要一次资产处置决定（三个可接受选项
已在该条给出）。

v4 复审只需判定三件事：

1. 是否存在一个实验差分能把音频特有的 re-resolve/search 分配与通用调度分开，且 §6 的 MERGE
   触发条件挂在该差分上（MAJOR-1）；
2. A1 的名称与其实际资产是否一致，覆盖缺口是否如实声明（MAJOR-2、MINOR-2）；
3. 决策量的函数形式与时序合法性是否落在 proposal 层，其标定是否落在 authorization 清单
   （MAJOR-3）；K2 是否只依赖已授权可落盘量，或是否已把日志扩展作为一项请求交 owner（MAJOR-4）。

MAJOR-5 与全部 MINOR 属文书与一致性修订，随 v4 一并核验即可，不单独构成复审门。

## 七、目的链、Provenance 与失效条件

**结论：** R2 v3 未关闭 round-03 §十四 全部清单项（CLOSED 6 / PARTIALLY_CLOSED 5 /
NOT_CLOSED 1），续77 有条件 GO 的生效条件尚未成就，owner 的生效裁定继续 withheld。本文不改变
R2 的既有状态标记，不授予任何执行权限。

**推理摘要：** v3 在证据层完成了实质工作——组织轴三篇深读的承重数字经逐条核源无一失真，"三篇
全有训练环节、组织 schema 逐字段为零"的定位结论成立且对红线合规有真实约束力。但 round-03 的
失败合同是可识别性：音频特有机制被写进研究问题却未被任何实验臂分离，A1 的资产前提经直接读取
载体数据被证否，policy 的决策量在两层之间缺席，K2 的判定所需信息不在已授权的落盘范围内。因此
不能从"研究对象已写清楚"推出"独立立项的实验设计已成立"。

**目的链：** 为了让 owner 在"R2 独立 / 合并入 R6-R8"之间落笔时，其裁定能被后续实验证实或证否；
所以 Stage-1C 必须保证独立性主张挂在一个**可被实验读数区分**的量上，而不是挂在一段可信的机制
叙述上；所以本轮把裁定条件精确定位到"是否存在识别该机制的实验差分"，而不再重复审查文献充分性。

**Provenance：** 本文只审查 front matter 所绑定的 Git blob `1397f876…`（commit `865d2cf…`，
worktree sha256 `22881daa…` 与 blob 一致，已独立 `git rev-parse` 复核）。判断依据为：round-03
评审 `wiki/audit/system-first-stage1c-v2/round-03/2026-07-29-r2-doctoral-supervisor-coreview.md`；
owner 裁决 `wiki/Decision-Log.md` 续76/续77/续78；模板
`…/proposals/2026-07-29-direction-coreview-template.md`；正典 `wiki/Research-Objective.md` 与
`wiki/survey/current/research-directions.md`；以及本轮实际执行的三项本地证据抽验（三篇 arXiv
LaTeX 源、`omni-deepsearch/merged.json` 640 条、v2 blob `062c253…`）。本轮 exposure：零网络检索、
零模型/API 调用、零指标运行、零数据集下载、零原型；新增动作仅为本地已落盘资产的读取与比对。

**失效条件：** 若 v4 或其回应关闭本文第三节的 6 项非 CLOSED 条目与第四节五项 MAJOR，并由新的
review transaction 判定音频特有机制可被实验差分识别、A1 名实相符、决策量已落层，则本
withholding 仅作为历史审计事实保留。若 owner 直接裁定改变研究对象定义、载体或红线边界（对象
定义权归 owner），本文中依赖旧口径的条目按新裁决作废，但**已核验的证据事实**（三篇论文的数字、
`golden_path` 的字段语义与覆盖率、v2 blob 的字段缺失）独立于处置结论继续有效。本文为审计层
记录，不得原位改写。
