---
artifact_id: "STAGE1A-PROPOSAL-2026-07-18-05"
title: "System-first Research Proposal v4——Stage-1A 调研证据呈报版（预映射证据基座 + 映射执行计划）"
date: 2026-07-18
addressee: "Gate S1 评审人 / 评委"
stage_position: "Stage-1A survey-ready gate（研究流程三阶段之 Stage-1 内;1B 标志 = 触碰模型,未发生）;系统性 mapping 查询执行数 = 0（attestation,机器可查）;创新点未锁定（owner 裁决 2026-07-18:现在只锁研究方向与内容）"
relation_to_v3: "v3-consolidated（STAGE1A-PROPOSAL-2026-07-15-04,blob 见 bundle manifest correction #3/#4 链）之「ACCEPT AS WORKING THESIS」裁定**不重开**;本件新增 = §3 预映射证据基座（C4B/C4C 两批产出的可回放证据）与 §4 执行计划现值;研究纲领/RQ 树/五合同/蓝图以 v3 为正典,本件只引不改"
evidence_grade: "本件所有占据/空位/机制陈述 = directional-only / hypothesis-grade（Stage-1 证据等级,永不自动升级);全部承重数字机器可复跑（复跑表 = correction #4C 回应信 §5 九项)"
integrity: "凡「已占据/空白」句均为对**已检视集合**的普查事实,不外推为文献全集结论——系统性 mapping 尚未执行,这正是本 proposal 申请执行的工作"
---

# Research Proposal v4——Stage-1A 调研证据呈报版

## §0 导读：这是什么、不是什么

**是**：向评委完整呈报截至 2026-07-18 的**预映射调研证据基座**（种子景观、34 哨兵、七篇
直接邻近工作的全文深读普查、负结果先验、发现机制的实证教训），以及据此冻结的**可回放
mapping 执行计划**。**不是**：survey 结果报告（mapping 一条查询未跑）；不是创新点声明
（owner 未锁定，任何「创新点成立/不成立」定性在现阶段两侧皆为时过早——含 P0-R9 评审 §4
的定位代拟，标 owner 未签）。

**阶段自答**：当前 = Stage-1A（Stage-1 三段之 A：问题界定）。已发生 = 协议冻结 + 定向 ID
dereference/raw provenance/全文准备/校准性引文试验 + 哨兵工程；未发生 = 系统性 discovery
查询（0 条）、模型触碰（0 次）、Stage-1B 实验（未放行）。

## §1 研究纲领（引 v3 正典,一页版）

**北极星**：weight-frozen reward-guided inference-time optimization（内部简称 TFRL）——
不改权重、不改结构，用外部控制平面激活冻结 speech/omni 多模态 LLM 的预训练知识。
**身份三轴（S0 已签,TF-Strict）**：①严格黑盒（只见文本/输出,不碰 logits/hidden state）；
②全系统零训练（含外部组件）；③单一冻结 omni 核心（非专家联邦）。**信息边界**：杠杆分
read-out（允许）/new-info（禁止）；test-item gold 永不入任何路径。

**研究问题树（据 v3 §3 摘引——正典以 v3 原文为准,全部为待证伪假设）**：RQ-SYS（外部
reward-guided sequential control 能否在**相同初始任务信息与显式记录的 decision rights**下,
获得终态-only 选择不能获得的**实质性且可复核**的额外效用——天花板依供给/候选构造/调用权/
信息边界**条件化定义**,两侧 headroom 分别报告,不宣称「打破同一 oracle ceiling」〔errata-2
④〕）/ RQ-CTRL（增量归因于奖励引导而非更多采样/更多调用）/ RQ-OMNI（非文本模态是否因果
参与）/ RQ-SAFE（reward hacking/过优化拐点与停止）/ RQ-MEASURE（label-free observables
预测头空与失败 regime）。survey 收官时收敛为 3–5 个
system-level candidate problems（每卡效用归因四行分立,可被单一反例杀死）供 Stage-1C 选题。

## §2 调研基础设施（已冻结、机器可回放、零执行）

| 层 | 现值 | 正典件 |
|---|---|---|
| arXiv 冻结查询 | **65 条 / 14 条查询 lane**（48 基础 + 版本化增补链 sfqc-1.0.0→1.5.0;另有 SF-L9 基础谱系道 = 零查询、chaining 专用;前缀逐字节不变纪律,prefix61 sha256 钉入 canon） | `wiki/survey/2026-07-15-sf-queries.jsonl` + 协议 §4 |
| 方法占位轴（P0-R9 整改核心） | SF-L14（orchestration/controller/routing + guided/contrastive/steering decoding）+ SF-L15（test-time scaling 短语族 + self-verification/consensus 族）——**零 agent 连词,13 类类目全并集**;修复「把研究目标命名写成检索前提」的认识论循环 | amendment-8 §1 |
| T1 会议题录路由 | 50 routes（10 会 × 2022–2026）+ 冻结词表 v1（A_any OR (B_any AND C_any),73 项零通配符） | routes v3 + wordlist v1 |
| 种子 | 92 条列名（manifest 逐行枚举 = 计数正典） | seed-manifest.jsonl |
| 哨兵 | **34 篇 / held-out 6**（held-out 6/6 纯查询召回〔离线 matcher 复现,非联网执行〕、era≥2025 机器强制——两限定语均只钉 held-out;存量另含 3 篇 SEED_GUARANTEED 种子兜底;raw Atom 字节+sha256 台账） | sentinel-data.json + 召回测试 |
| 独立查询复核 | PRESS 式制度化（隔离代理+owner 抽查;首轮已执行:HARDCODING NO,其 MAJOR 冻结前采纳） | `2026-07-18-sf-press-query-review-c4c.md` |
| 退出机制 | E1（BFS 干涸）∧ E2（引文闭包 K=2,backward 自存档 e-print 离线抽取）∧ E3（哨兵清零）;E2 饱和前置 = work-level identifier resolution（债务 D-1） | amendment-7/8 |
| 门禁 | fail-closed 机器门禁全绿 + mutation harness 10/10 + validator 26/26;可回放性三级分类（bundle-only/local-data/network-dependent） | 回应信 §5 九项复跑表 |
| 评审轨 | 四轮博导对抗复审（correction #4→#4A→#4B→#4C 触发链）全档留痕;P0-R9 我方**首次有据部分异议**（0-hit 表 2/7 不成立,机器证据） | 各 dated review/response 件 |

## §3 预映射证据基座（调研结果详呈;全部 hypothesis-grade）

### §3.1 直接邻近工作身份轴普查（七篇全文深读,DFS 四问 + 承重引文抽查 11/12 逐字命中〔批次 A 5/6,第 6 条为改写差异;批次 B 6/6〕）

全文正典 = `wiki/survey/2026-07-18-sf-p0r9-seven-papers-dfs.md`（每篇:方法/局限/改进空间/
可借鉴 + 八项身份轴事实 + 页码引证）。普查表（一行一篇,身份轴差异为事实陈述）：

| 论文 | 与本纲领的重合 | 关键身份差异（逐轴事实） | 角色 |
|---|---|---|---|
| Training-Free MLLM Orchestration (2508.10016) | training-free 编排、omni 含 speech、黑盒文本级、read-out-only、memory/routing/verification/stopping 四机制模板 | **多模型专家联邦非单核**;无候选池/无 selector/无 reward(纯确定性路由);自称仅 "training-free integration and control"(原文逐字核verified) | component-prior |
| ThinkOmni (2602.23306) | training-free、冻结模型、omni 含 audio、per-step 自适应 | **logits 级融合 + 外部 LRM 注入(new-info)**——双重越出黑盒/read-out 边界;需共享词表;无候选池 | boundary-comparator |
| Limits & Gains of TTS in VLR (2512.11109) | BoN/SC/verifier/refinement 全谱实证,与 selector 设计空间高度重合 | 纯 vision-language 无 speech;confidence 变体用 logits;外部 verifier=另一强模型 | component-prior |
| Multimodal TTS Survey (2606.08231, ACL Findings 2026) | TTS 形式化(θ fixed+预算+效用)与 TFRL 同构;三范式导航骨架 | **明文排除 audio**:"focuses on vision-language modalities" + "does not cover audio"(p10,两段分别逐字核验的拼接引);含训练 PRM/logits/RAG 子集 | navigation-only |
| Small-VLM TTS (2607.09438) | 采样-选择-验证平面、training-free critic、供给/选择归因方法论 | 视觉 MCQ 无 speech;log-prob+guided decoding 越黑盒;PRM 组件 trained(结果恰为 null) | component-prior |
| On TTS for VLMs (2606.28864) | zero-shot 严格对齐 TF-Strict、单核、SC+多数投票 | 视觉无 speech;诊断层用 attention/KV;回路内无 reward/learned selector | component-prior |
| dMLLM-TTS (2512.19433) | **单核兼任生成与验证**、self-verification 作 reward、探索-剪枝-精化平面 | 文生图生成域;yes-logit 越黑盒;扩散架构非自回归 | component-prior(兼边界) |

**普查结论（对已检视集合的事实,非文献全集结论）**：七篇中**零篇**同时满足「严格黑盒 +
单一冻结核心 + speech/omni + 候选选择」四轴;各差至少一轴。主流多模态 TTS 综述明文不覆盖
audio。**该交集是否为真空位、值不值得占据 = 系统性 mapping 要回答的问题,本件不预判。**

### §3.2 负结果与异质性先验（对后续实验设计的直接约束;三篇独立收敛）

**供给侧主导**（TTS 增益大头不在复杂 selector）：①输出**可解析性**先于一切——修 prompt
格式即 +~6pp,「看似推理失败实为抽取失败」（2607.09438）；②**单链 token 预算 >> 链数**
（+3.7pp vs +0.15pp）；③**策略模型本身主导**（换模型 +11.4pp > 任何推理时策略）；④冻结
核心的**指令遵循能力是供给生效前提**（弱核心下 TTS 全失效,null 只否定该核心）；⑤
**over-compute 失焦**（感知型任务上冗长供给累积幻觉,截断反升,GPT-5.2 亦不免疫）。

**选择/验证侧边界**：①trained PRM 与 training-free critic **均不敌多数投票**,池准确率越高
近平衡选择器净转负（2607.09438）；②弱模型 self-refinement 常退化（2512.11109/2606.28864）；
③self-verification 有效但**封顶于核心自身理解力**（SVF<GPT-4o,2512.19433）；④外部
verifier > 内部 confidence 一致成立、内部 confidence 不是 correctness 可靠指标（2512.11109）；
⑤SC 适用边界 = 各链独立犯错,高相关池放大共同错误（8/8 一致仍错→回退）。

**对本纲领的直接落点**：这组先验**支持而非削弱**我们既有的度量纪律——MBR/majority = 等 K
强制基线、headroom 归因纪律（无头空 null 只否定供给配置）、供给条件量 H(c) 换供给必重测。
Stage-1B 探索维度据此登记：rollout 误差独立性作头空前置、可解析性修复先于 selector 比较、
selector 强度≤核心理解强度、over-compute 拐点、指令遵循前提。

### §3.3 发现机制的实证教训（为什么现在的检索协议长这样）

①**词汇漂移是真实威胁轴**：DVD（59 查询零命中,agentic search 词汇）、ToolGate（65 查询
零命中,gating/pre-call control 词汇,vocabulary-drift 队列 1/3）两例实证〔「X 查询零命中」
均为离线 matcher 对冻结查询的召回复现,非联网执行——零查询 attestation 不受影响〕——方法占位轴
（L14/L15）+ 漂移观察队列由此而来,`agentic` 降为编码结果不再是发现前提。②**引用交集筛
不能当唯一发现入口**：预注册校准实验（Seg-Agent,30 个可解析 arXiv-ID × 107 存量 = 空交集,
verdict = ARXIV_ID_SUBSET_INTERSECTION_EMPTY,hypothesis-grade）——跨社区平行谱系在结构上
引不到核心集,发现层必须由冻结查询承载,引文闭包只作退出/相关性层。③**0-hit 声称必须机器
复现**：P0-R9 评审 0-hit 表 2/7 行经正典 matcher 复现不成立（两篇实中 SF-L5）——完成态
语言与 oracle 等强的纪律对评审侧同样适用,我方以证据提出部分异议并被 PRESS 独立收敛。

### §3.4 种子景观现值（v3 §6 快照的滚动更新,只列增量）

92 列名种子维持（快照 51 + 增量批次 1–4;最高优先威胁 = Omni-Decision 2607.11433 不变）;
C4B/C4C 新增 13 哨兵（C4B 5 反例 + C4C 7 反例 + fresh L12 held-out 1）全部为**反例/held-out
工程件**（query-regression/coverage-omission/held-out）,
不改变种子威胁排序;execution-early 队列（WorldEvolver/PolarMem/AudioGenie/
Dopamine-Audiobook 四篇 FULLY_TRAINING_FREE + MemoPilot TF-Strict 直接威胁样本）维持
amendment-7 §4.3 登记,BFS 首轮优先精读。

## §4 映射执行计划（签署后即可执行,全程可回放）

1. **BFS**：65 条冻结查询 + 50 T1 路由全量执行,命中做题录/摘要级编码（REC-0 落账,五计数
   机器导出;75-cap 溢出走 YEAR/MONTH splitter）。
2. **DFS 触发**（四判据:对象/问题/要素/结论冲突重合）→ 全文精读（方法占据四问 + D2 八轴,
   validator V1–V15 机器强制）;队列排序 =（威胁度↓, core>element, 时新性↓, 梯队平局）,
   2025+ 先于前时代（agent-era 裁决;窗口不砍、时代先验不进 study_quality）。
3. **退出** = E1∧E2∧E3 + 逐轮饱和表（PRISMA-S 兼容);E2 饱和宣称前必须完成 work-level
   identifier resolution（债务 D-1,否则只能说「已解析子图上零新增」）。
4. **产出**：occupancy 普查（§3.1 表的全语料版）→ 3–5 candidate problem cards（v3 §3 卡
   纪律）→ Stage-1C owner 选题。债务表 D-1..D-5 带 owner 与截止 gate（amendment-8 §4）。

## §5 诚信声明与请求

**声明**：联网活动全量入访问台账（三本:access log/atom ledger/fulltext ledger,双计数）;
discovery query = 0;全部承重数字可用回应信 §5 九条命令零联网复跑;证据等级 directional-only
不升级;创新点未锁定,本件不含任何占据/空位的终局定性。

**向评委的请求**：①按 P0-R10 验收表复核 correction #4C（双向合同:0 新 MAJOR/0 新 MINOR
→ 签署 Gate S1 mapping-execution）;②本件作为随附呈报阅览,**不新增签署对象、不重开 v3
working-thesis 裁定**;③签署后仍需 owner 执行批准（三方分立）,首条查询才会执行。

—— 研究执行方（W1）,2026-07-18。本件随提交入 git;更正走 dated correction。
