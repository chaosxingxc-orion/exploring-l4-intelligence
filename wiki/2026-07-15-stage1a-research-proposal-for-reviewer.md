---
proposal_id: STAGE1A-PROPOSAL-2026-07-15-01
title: Stage-1A 探索总结与研究提案（提交 reviewer）—— 冻结 omni 上 label-free 选择算子的供给条件兑现面
date: 2026-07-15
stage: Stage-1A（问题界定收尾）；本件性质 = 问题定义提案，非 Stage-2 确证协议（未来计划部分适用 PRE_STAGE2_BLUEPRINT 纪律：结构草图，无现时效力）
stage_claim: ROUND1_SCOUT_COMPLETE；决策包 = PRE_STAGE1C_DECISION_DRAFT（P0-R+P1 门控后才提请选题）
evidence_discipline: "全部数字 directional-only / hypothesis-grade；证据等级逐行登记于 claim-ledger v2（单遍 AI + 独立抽样验收级，人类双审待 E2）；否定性结论一律按身份索引 + 强制伴随 token；无任何确证宣称"
number_reconciliation: "本件全部承重数字由协调者逐条对账 claim-ledger-v2（CL2 行号在文中标注）；对账中纠正草稿一处错误（KIT ST 兑现实为小幅为正，见 §5.1）"
generated_by: "Claude Fable 5 主会话协调者亲笔（非委托）；素材=三轮博导评审整改后的正典工件（census v2 / ledger v2 / 冻结合同+修正案 №1 / 预注册协议 / C1C4 census / P0-R8 机检）"
verified_by: "机械层=P0-R8 校验器 exit 0 + 协调者数字对账；敌意内审环=提交前执行（结果见 frontmatter hostile_review 行）；科学双审/独立盲审 = 待 E2（如实声明）"
hostile_review: "DONE_PRE_COMMIT（2026-07-15）：敌意预检对初稿抓 8 缺陷+2 警示（最重=引用了 0 字节验收工件——该工件已据会话内代理全文重建并带事故注入库）；协调者重写版自愈 D1–D4，残余 D5–D8+C-a/C-b 已修（机器拦截措辞/C1 精确 token/bundle 钉定/E2 括注/论文全称）；P0-R8 机器门复跑 OVERALL PASS exit 0"
owner_transmission: PENDING — owner 审阅后转交 reviewer
---

# Stage-1A 探索总结与研究提案

> **给 reviewer 的一句话**：这是一份问题定义提案。它报告我们探索了什么、什么死了、什么以何种
> 限定幸存、我们对自己纠了哪些错、以及下一步以何种可证伪判据继续。它不主张任何已证结论。
> 对 reviewer 的具体请求集中在 §9。

## 0. 一页速览

- **研究对象**：一个 label-free、供给条件的选择算子，在冻结 omni〔模型×任务〕矩阵上的兑现面
  ρ(c)/H(c)/regret（§1）。
- **本轮做了什么**：两轮调研（round-1 scout + Survey v2 敌意猎杀）→ 三轮博导对抗评审与整改
  （P0 → P0-R → Gate A）→ 证据台账工程（census v2 / ledger v2 / 验收抽样）→ 身份合同冻结 +
  修正案 №1 → 诚信核查 C1/C4 → 机器状态门 P0-R8 → round-2 检索协议预注册 + PRESS 预检（§3）。
- **现状一句话**：五个候选身份中，I1 已被直接占据（kill 方向保持）、bare-I2 机制级被占、
  strict-I2/I3-combined/UMBRELLA 在保留记录集中无直接匹配（各带强制伴随 token）、I4 方法族被占
  但音频/omni 供给分层实例化 undersearched（§4）。**尚未选题**——Stage-1C 由 owner 基于
  调研+探针双证据收官。
- **下一步**：round-2 可回放检索（协议已预注册，零查询执行，待 reviewer search-design 签署）→
  Stage-1B 四探针（协议 v2 待 Gate C）→ 决策包 v2 → owner 选题（§6）。
- **GPU 运行至今为零**；round-2 检索至今零查询。全部现有证据为文献台账级。

## 1. 研究对象（冻结定义，续34 锁定 + 续41 合同冻结）

**一个 label-free、供给条件的选择算子在冻结 omni〔模型×任务〕矩阵上的兑现面。**

记号与冻结口径（完整合同 = `2026-07-14-identity-contracts-v1.md`，FROZEN@dce5c79，git-blob
sha256 `1338f6b1…`；叠加修正案 №1 EFFECTIVE@0a5e108）：

- **供给 c（capability supply）**：喂给冻结核心的上下文与外挂能力总和——prompt、检索证据、
  工具输出、解码参数。rollout 分布条件于 c。
- **K 池**：冻结模型在供给 c 下对同一输入采样的 K 个候选输出。**算子类别 = 仅池内选择**；
  扩池/改写/工具环/权重更新是不同对象，禁混写（P0-R7 分类法——本轮两条 CRITICAL 更正即源于
  此前混写，见 §5.1）。
- **oracle 头空 H(c)** = 池内最优 − 默认输出（事后用真值度量）。**供给条件量**：只在给定 c 下
  有定义，换供给必须重测；文献对应 best-of-N 理论的 coverage 条件。
- **selector**：不读 gold、只凭无标签信号从 K 池挑输出的算子。打分信号须显式登记输入模态
  （纯文本 vs 音频接地）与来源（same-core / external-frozen / external-trained）——此轴即
  I1↔bare-I2↔strict-I2 的分界。
- **兑现率 ρ(c)** 拆双锚并与绝对量四量并列：rho_greedy（锚=部署默认输出）/ rho_pool（锚=池均值）/
  delta_mbr / regret；**cellwise-only**（禁无权重跨任务总平均）；分母过小标 `HEADROOM_TOO_SMALL`
  只报绝对量。部署用 label-free proxy `S`、评估用 `U`，二者不混。
- **硬约束**：weight-frozen（不改权重/结构）；**信息边界**（test-item gold 不入
  selector/reward/prompt/检索/候选构造；read-out 杠杆允许、new-info 杠杆禁止）；对比一律**等 K**，
  **MBR 同 K 为强制基线**。
- **δ_corr 语义（修正案 №1 拆名后）**：理论符号 δ_corr 仅保留 TH2a 原义=残余误差相关；经验四量
  `selection_overlap`（仅描述，不作 kill 判据）/ `error_corr` / `conditional_error_mi` /
  `complementary_gain`（router 上界增益）。「选择重合」永久移出 δ_corr 语义——此前的操作化被
  第三轮复审裁定为构念替换，已由修正案根治（§5.2）。

## 2. 方法论与证据纪律（reviewer 可据此校准每个数字的分量）

- **三阶段制**：Stage-1 问题定义（当前，1A 收尾）→ Stage-2 方案验证（预注册冻结判据）→
  Stage-3 论文发表。**Stage-1 证据永为 hypothesis-grade**，只能作方向材料，绝不自动升级。
  1A→1B→1C 排序系 owner 裁决（续40）：工单关闭 + 1B 四探针 → STAGE1C_DECISION_READY →
  owner 双证据选题。
- **append-only**：记录不改写，更正走 dated supersession；哈希正典 = git blob 字节
  （核验命令 `git show <commit>:<path> | sha256sum`）。
- **三线分签**（本轮建立，续39）：①字节可重建 ②文献身份/检索宇宙可审计 ③科学 claim 被原文支持
  ——三条线永久分开签署，完成度永不聚合上标。当前：①已达（INTERNAL_BUILD_CONSISTENCY_12/12）；
  ②census v2 单遍 AI+验收抽样级；③ledger v2 单遍 AI+验收抽样级，人类双审待 E2（E2 = P1 序列
  的人类双审+独立盲重建批次代号；勿与历史勘误编号 E1–E3 混同——收词纪律括注）。
- **证据等级五级**：DISCOVERED / ABSTRACT_VERIFIED / FULLTEXT_OPENED / CLAIM_VERIFIED /
  REPRODUCED；snippet 不升全文级；综合行不继承最强子级。ledger v2 分布：CLAIM_LOCATED_FULLTEXT
  35 / ABSTRACT_ONLY 20 / FULLTEXT_UNREACHABLE 2 / SYNTHESIS_PENDING_REVIEW 5（分桶报告，禁求和）。
- **机器状态门 P0-R8**：八规则 fail-closed 的 repo 级校验器（`scripts/integrity/p0r8_state_gate.py`
  v2）——headline 数字只出自机器重算，机器拦截协调者三次「字段计数升格为结论」的同构失误
  （是否根治以后续轮次为证）；
  合成 fail-closed 探针 11/11 正确。
- **敌意内审环**：每个发布件（含本件）提交前过多镜头敌意内审，修复后复审直到一轮零新发现。

## 3. 本轮探索完整轨迹（含失败与被拦截的错误——按时间序）

### 3.1 两轮调研

- **round-1 scout**（07-13）：8 族 / 57 条 / 46 独立来源，SCOUT 级。**round-1 检索的 raw response
  宇宙永久缺失**（当时未捕获；模板规则禁补造）——检索本身不可重放，已如实签
  REPLAY_FAILED(search-replay)，状态钉在 ROUND1_SCOUT_COMPLETE。这是本轮最大的不可修复缺口，
  round-2 协议的「构造性可回放」硬约束即为其教训（§6.2）。
- **Survey v2 敌意猎杀**（07-14）：15 条敌意 lane（含专杀自家候选的 disconfirming 视角），
  SEARCH 218 + FETCH 87 次事件（chase 事件与 SEARCH 分开计数——续38「305 查询」混数教训），
  产出 94 记录簇 + coverage/kill matrix v2 + neighbor matrix v2 + SOTA cards v2。

### 3.2 三轮博导对抗评审与 P0/P0-R 整改（全部收档、逐条回应）

- **初审**（对 Survey v2 + Stage-1C 决策包草案）：MAJOR_REVISION——可回放性、去重、证据等级
  上标等 → 开出 **P0 八项**。
- **再复审**（对我方 P0 整改回应 RESP-01）：拒签，坐实**六项 QRP 指控**——完成度聚合上标
  （「P0 八项全部执行」）、假精确「94 篇」（canonical ID/version/hash 0/94）、claim_evidence
  名实不符（claim_text/verified_by 0/118）、12/12 校验语义混写、**owner 签署位失实**（把治理
  裁决扩写为 integrity 签署）、无界定的全称可溯源宣称。**全部逐字亲验后承认**（RESP-02 §2），
  P0 计分接受 2 CLOSED + 6 PARTIAL；同时提出四处有据抗辩。
- **第三轮复审**（收档 a06a498，RETURN_FOR_MAJOR_REVISION，续42 零抗辩接受）：五承重缺陷坐实
  （「43 条 discrepancy」实为非空字段计数、其中 11 条以 "None" 开头；「35 全文」含 5 行摘要级；
  「92 resolved」含 6 条无 canonical ID + 56 条版本未钉；送审快照字段语义误导——证据锚与送审锚
  须拆分；**δ_corr 构念替换**——选择重合推不出误差相关）；我方四处旧抗辩**全部获裁〔半〕胜**
  （身份索引 token 方案获采纳）。外部抽核证实我方四项自我纠错全真且多数损害我方原叙事——
  **三轮评审均未建立 FFP（造假/篡改/剽窃）指控**，此为关键反证。科学修正同时接受：P-γ 改测
  条件互补性、P-β 主臂改文献可比 BLEU、P-δ 签批前冻结 c1、**Stage-1B 改用 dev split**
  （test-other 系 publication holdout，探索触碰即污染）。

### 3.3 Gate A：证据台账工程（零 GPU）

- **census v2**（28ad858）：94 记录簇解析为 **95 works** 双表（P-0016 判拆二 work）；
  **94 RESOLVED + 1 如实 IDENTITY_UNRESOLVED**（W-0014，fail-closed 不计数）；ID 分布
  arxiv 83 / doi 6 / venue-native 5 / NONE 1；**83/95 版本钉定**；95/95 全作者；
  P-0084 借 Table 3 数字指纹落定为 2606.04730。
- **ledger v2**（28ad858）：**62 行**，一 claim×一 work×一 span（v1 44 行中 5 复合行拆 18 分件行
  + 5 综合行，综合行不继承最强子级）；claim_id 全局唯一；verbatim/structured/inference 三分字段；
  **discrepancy 五级枚举 NONE 20 / MINOR 19 / MATERIAL 15 / CRITICAL 2 / UNVERIFIED 6**
  （取代已撤回的「43 discrepancies」headline）。
- **11 条提取期丢弃明细**：从存档的 extract-agent workflow journal 逐条恢复（verbatim raw_claim +
  drop_reason_code），**零不可恢复**——分母缺口闭合。
- **版本 pin 收尾**（b594820）：16 行 PIN_PENDING 全部经 cluster→work 映射钉定（29 个
  claim×work pin，100%）。
- **独立验收抽样**（b1af8c6）：另一 reviewer 镜头抽 10/10 census + 17/17 MATERIAL/CRITICAL +
  7/7 摘要级承重裁决，**零同类错误 → ACCEPTANCE_PASS**（纪律：发现 1 个同类错即扩全量复筛）。
- **当轮拦截实例**：两条构建代理散文夸大（「94/95 版本钉定」「95 全 resolved」）被协调者数据
  重算当场拦截并以更正节入档——do_not_claim 纪律的当轮实践。

### 3.4 身份合同冻结 + 修正案 №1

- **合同 v1**（dce5c79，owner 治理签核，续41）：六份身份合同（I1 / bare-I2 / strict-I2 / I3 /
  I4 / UMBRELLA，每份=冻结定义+量词规则+正负测试+kill/pivot/proceed 判据+出处日期链）+
  **same-selector contract**（跨任务共享算子冻结面：池内选择、信号登记轴、信息边界、等 K+MBR
  强制基线、四量并列）+ **post-hoc 条件日志**（冻结后任何限定词变更必须登记——合取洗白防线）。
  冻结先于 round-2 检索与 1B 探针：**先冻结定义，再看新邻居**。
- **修正案 №1**（0a5e108 生效；owner 两次独立 AskUserQuestion 分栏签署，未混栏）：
  A) δ_corr 四量拆名；B) strict-I2 kill-if 重写为**两独立测试**（matched-controls 音频因果检验 /
  「高同错 且 无互补」独立价值检验——单一 shuffle winner-flip 与选择重合判据作废）；
  C) same-selector contract 对 UMBRELLA 环内动作的覆盖撤回（环是不同算子对象）；
  D) C1/C4 终验与探针授权拆两个 exact-hash 签字块（根治循环签署）。随生效：探针协议 v1 作废
  （v2 于 Gate C 重写）。

### 3.5 诚信核查 C1/C4 + 机器状态门

- **C1 尝试普查**：registry vs raw run 集合差——补登 E 盘运行树 + W4 outputs + MLflow
  （376 行聚合登记）；**config-selection 历史轨迹 = 永久缺口**（禁补造，如实登记，1B 起由
  探针尝试登记前瞻关闭）。**C4 负结果普查**：29 行台账（GLAP 全量构建 PARKED 31000/57638、
  vLLM/int4 OOM 等）。精确 token：C1 = **CENSUS_COMPLETE_WITH_REGISTERED_PERMANENT_GAP**、
  C4 = **CENSUS_COMPLETE**；owner 于 Integrity gate 独立签栏终验（正式关闭）。
- **P0-R8 状态门 v2**（fcd1c57）：见 §2；Gate B 门 G6 以其 OVERALL PASS exit 0 关闭
  （9 条 R3_MIXED_LOCATOR WARN = 公开双审队列，不隐藏）。

### 3.6 Gate B：round-2 检索协议预注册 + PRESS 预检（零查询执行）

- **协议 v2**（SURVEY-PROTO-2026-07-15-01）：21 lanes = 9 饱和目标 + 8 新篇必查 + 1 全占据者
  forward-chase + 3 条 **disconfirming lanes**（去自造术语的方法族搜索 / 可训练邻域 comparator /
  供给选择替代名——反收方偏置）；**105 条精确查询串 = 102 mandatory + 3 optional 单语探针**
  全部内联预注册；引擎/venue 表补 ACL Anthology / ISCA Archive / IEEE Xplore(site:) / Crossref
  （OpenAlex 因 key 门控排除）；trace-reconstructable vs query-rerunnable 显式分类；纳排规则
  各带 2 正 2 反真实论文样例 + 冲突裁决规则；全 DIRECT/PARTIAL 双审 + 全 fulltext 排除双审 +
  10% 随机抽样复筛；机械停轮规则 + yield curve（无曲线不得声称饱和）；新 work 经 census v2
  schema fail-closed 入格。
- **PRESS 2015 六要素敌意预检**：裁定 PRESS_REVISE，7 项修复（多语 mega-query 拆分、arXiv
  cat-filter 16 条、IEEE site: 路由 3 条、十项 text-word 变体、音频接地供给查询、G6 阻断前置、
  查询卫生规则）——全部应用（18056f1）+ 协调者逐字亲验残留清扫（aaffe4c，5 处缺口兜齐）+
  机械重数工件 exit-code 门控 PASS。
- **边界**：`queries_executed: 0`。首条查询前仍需 ①reviewer search-design 显式签署（**即 §9
  请求 1**；沉默≠批准）②owner 资源批准 ③G6 执行首日复跑。

## 4. 主要发现与身份候选现状

### 4.1 身份索引总表

否定性结论的记录集钉定为 RETAINED_RECORDS = papers.jsonl 94 簇 @ SURVEY-RESP-2026-07-14-01
bundle（字节可重建）；任何否定性结论
**强制并列伴随 token**：`SEARCH_RESULT_UNIVERSE_UNAVAILABLE` ·
`SCIENTIFIC_SATURATION_NOT_ASSESSABLE`。全局 token 已停用（两个逻辑洞：与 bare-I2 机制级占据
裁定矛盾；可字面为真而最大压力恰在指称集之外——RESP-02 §4.4，建设性修复即本表）。
证据级封顶 ABSTRACT_VERIFIED 待双审。

| 身份 | 现状 token | 一句话 |
|---|---|---|
| I1 一般 label-free selector | DIRECT_OCCUPIED | 存在性身份已被直接实现占据；kill 方向保持，MBR 更正后更强。不作独立新颖性 |
| bare-I2 音频接地 selector（宽式） | 机制级 DIRECT_OCCUPIED；任务格覆盖 MIXED/UNDERSEARCHED | 同核 audio-conditioned 打分机制已被占；ST/SLU 格暂无同类但不恢复宽式新颖性 |
| strict-I2 同核曲面选择器（=I2∩I4 合取） | POST_HOC_NARROWED_CANDIDATE（post_hoc_created_at=2026-07-14）；保留记录中无直接匹配 | 构件出处早于猎杀，合取身份系 07-14 合成——如实标注，不得以「经攻击幸存」框架引用 |
| I3 约束/可弃权/Goodhart selector | abstain 分量已占；I3-combined 无匹配 | Goodhart-on-speech 拐点是其生死检查点 |
| I4 供给条件兑现面 | METHOD_FAMILY_OCCUPIED；音频/omni 供给分层实例化 UNDERSEARCHED；增量预测贡献 NOT YET SHOWN | 可辩护空白收窄为 label-free × 供给轴 × 音频域的可预测规律 |
| UMBRELLA 伞式交集（第五候选） | 保留记录中无直接匹配；IAD 预登记坍缩风险 | 等预算 loop vs one-shot 判别是其保留问题 |

### 4.2 逐身份 dossier（关键证据带 ledger 行号；全部 directional-only）

**I1**（一般 label-free N-best/K-sample selector，存在性量词）——**DIRECT_OCCUPIED**：
mbr-asr 2510.19471 在冻结 Whisper-large-v3 上 label-free MBR 固定 K=64 池内选择（CL2-0002：
LibriSpeech WER Beam 0.042 / MBR 0.033 / Oracle 0.013——MBR 兑现约 31% 头空）。杀伤在更正后
**更强**：其 Table 9 中 Llama-3 打分变体 0.043 反而输给纯 MBR 0.033（CL2-0059）。但兑现率
数据依赖显著：ReazonSpeech(JA) 0.305/0.291/0.149，兑现仅约 9%（CL2-0002/0035）——这一供给/
数据条件性本身是 I4 方向的素材。

**bare-I2**（音频接地，宽式）——**机制级占据**：scaling-auditory 2503.23395 用同核
audio-conditioned beam log-likelihood 做池内选择（CL2-0003）；jia-SER 2602.03873 在 SER 上
做 test-time scaling（CL2-0007）。量词拆分（再复审裁定采纳）：新颖性按存在性判——机制已占；
任务格覆盖单独报告为 MIXED/UNDERSEARCHED（SER/SLU/ST 若干格无同类）。

**strict-I2**（同一冻结 omni 双角色 + 自身音频接地信号 + ρ(c) 曲面刻画）——合取身份，
保留记录中无单一实例实现完整合取（合取量词规则：分立组件各自被占不构成合取占据，也不得反向
拆分自证开放）。**诚实标注**：POST_HOC_NARROWED_CANDIDATE——构件出处均早于 Survey v2 猎杀
（同核双系统+δ_corr=TH2a 2026-07-05；ρ 面=owner 07-11 签署；own-signal 条件=07-13），但合取
**命名与合成系 2026-07-14**。其生死系于修正案 №1 的两独立测试（§7）。

**I3**（弃权/Goodhart/风险-覆盖约束）——拆分现状：abstain 分量被 walking-through-uncertainty
2604.25591 占据（CL2-0008）；Goodhart 概念在文本侧被 2506.19248 占据（CL2-0001——注意其
"reward/RL" 措辞实指代理奖励模型，策略冻结、推理时 BoN/HedgeTune 选择，**不得误排**）；
**Goodhart-on-speech 拐点在保留记录中无匹配**。既有方向性线索 audio-mind cliff 仅 n=6
（台账更正后如实降格）。conformal 侧：ernez23a（PMLR v204）占 conformal-ASR，其「80%」系
置信水平而非经验覆盖率（我方引用已更正）。

**I4**（供给条件〔model×task〕兑现面）——**METHOD_FAMILY_OCCUPIED**：scaling-surface 方法学族
已被 text/VLA 占据（Snell 2408.03314 compute-optimal、VG-Search 2505.11730 验证粒度、
《The Art of Scaling Test-Time Compute》(2512.02008) 2512.02008、RoboMonkey 2506.17811 VLA scaling law）。**但音频/omni 的供给分层实例化
undersearched，且我方必须兑现合同级强制检查点**：给出相对 difficulty/entropy/agreement/length
等通用 baseline 的**增量预测力**，且预测量 **label-free**（对抗 2606.02981 的 labeled
predictor）——否则降级为工程实例化，不得作科学新颖性。最近邻 KIT 2606.04730 的兑现面数据
（CL2-0014，全文定位）恰示这一对象非平凡：oracle 头空（17 候选 N-best）ASR −32.10 WER /
SQA +14.42 BERTScore / SSUM +3.85 / ST +6.11 COMET；label-free 兑现 ASR 达 77.6%（Likelihood）
/ 60.0%（Lik+MBR），ST 小幅为正（+0.93 / +1.09），**SQA/SSUM 为负**（Likelihood −11.06 / −8.60；
Lik+MBR −3.33 / −2.19）——「规律」可能主要是**何时失效**的规律，这是 I4 的核心素材而非尴尬。
供给轴祖先：siskos 2509.19567 contextual-biasing 供给梯（CL2-0019：TED-LIUM 18.9→16.4，
oracle 15.4）。度量祖先：JudgeBoN 2603.12520 的 Recovery = oracle-over-random 兑现比
（只 formalize 我方 rho_pool 锚；21.0% pointwise → 61.2% pairwise，CL2-0010，摘要级）。
READ（P-0075）Table 1 兑现率 7.7%–68.5%（ASRU 7.7%、SWBD 68.5%；LibriSpeech 仅 12–17%，
CL2-0061）——我方此前「~70–85% oracle」引用已更正。

**UMBRELLA**（training-free RL ∩ 冻结 omni ∩ advantage→下一步动作；2026-06-26 立项对象，
非 Survey v2 新造）——保留记录中无单一占据实例（须同时满足 frozen core + agent 实际接触音频 +
reward/advantage 引导下一步动作；AudioToolAgent 2510.02995 占 system 格但 agent 不接触音频、
无 reward-guided K-pool selection，CL2-0029 摘要级）。**预登记坍缩风险**：IAD 2504.01931
（agentic loop 胜 one-shot BoN：Sketch2Code/Text2SQL 约 3–4pt，WebShop 达 8–10%——数据集依赖，
禁只引低端）。其算子对象与池内选择已按修正案 §C 分离；等预算 loop vs 一次性 rerank 判别留
Stage-1C。

### 4.3 已知集外压力（诚实登记——最强压力恰在保留记录集之外）

三篇尚未入台账、已列 round-2 必查（L-NEW lanes）：**2606.02981**（labeled BoN-gain predictor，
Spearman ρ=0.90 量级——逼迫 I4 差异化必须 label-free）；**2607.05391**（text-agent 上 verifier
兑现 oracle 头空——I1/I4 度量占据风险）；**2602.12281 CoVer**（verifier 选择改写指令+动作块——
供给侧选择决策形态的最近邻威胁）。round-2 的 8 条 L-NEW lane 与 3 条 disconfirming lane 即为
此设计（含「去掉我方全部自造术语后 method-family 是否已被标准名占据」的 RQ4）。

## 5. 我们对自己纠了什么错（可信度证据）

### 5.1 数字与标签级更正（全表 = ledger v2 的 15 MATERIAL + 2 CRITICAL）

- **两条 CRITICAL 推翻我方旧标签**（CL2-0060/0062）：ProGRes 2409.00217 系候选**扩池**、
  TAP-GER 2309.15649 系池外生成纠错（8.72 < 9.78 n-best oracle）——均非池内选择，撤回其
  kill-I1 DIRECT 占位（独立抽样验收核验重分类方向 RIGHT）。
- **KIT 2606.04730**：我方误写 ST oracle +2.0，实为 **+6.11 COMET**（CL2-0014，MATERIAL）。
  其兑现符号结构照实登记：ASR 正（77.6%/60.0%）、ST 小幅正（+0.93/+1.09）、SQA/SSUM 负。
  〔本件起草过程中协调者对账又拦下一处草稿错误——草稿曾写「仅 ASR 正兑现」，漏了 ST 的小幅
  正兑现；已改正。〕
- **MBR ~31% 兑现系 LibriSpeech 特定**（ReazonSpeech ~9%，CL2-0002/0035）；**JudgeBoN Recovery
  锚=池均值**（只对应 rho_pool，非 rho_greedy，CL2-0010）；**ernez「80%」=置信水平非覆盖率**；
  **audio-mind Goodhart cliff 系 n=6**；**READ 兑现 7.7–68.5%**（撤「~70–85%」旧引用，CL2-0061）。
- 外部抽核（第三轮复审）证实四项抽查纠错均真且**多数损害我方原叙事**——三轮评审均未建立
  FFP 指控的关键反证。

### 5.2 过程级承认与根治（六项 QRP → 机制化修复）

本轮我方文本行为被评审坐实六项 QRP（§3.2），全部承认。根治映射：完成度聚合上标 → 三线分签 +
逐项计分；假精确 → canonical census（fail-closed：无 ID 不计数）；证据名实不符 → ledger v2
三分字段 + 五级 discrepancy；校验语义混写 → `INTERNAL_BUILD_CONSISTENCY` 前缀强制；签署位失实
→ owner 裁决与审计签署分离（治理裁决≠integrity 签署）；全称外推 → 「已抽查者可溯源，未审
数字=未核验」。**δ_corr 构念替换**（同名承载三套语义、kill-if 数学不可执行）→ 修正案 №1
四量拆名 + 两独立测试。协调者三次同构「计数升格」失误 → P0-R8 机器状态门（headline 只出自
机器重算）。**残余风险如实声明**：以上多为单遍 AI + 抽样验收级，人类双审（E2）未做。

## 6. 下一步研究计划（Gate 制，全部预注册后执行；本节属 PRE_STAGE2_BLUEPRINT 纪律）

### 6.1 Gate 路线（现状：A、B 已收口）

**Gate A**（台账工程）✅ → **Gate B**（round-2 查询前）✅ 六门全绿（G1 修正案签署 / G2 协议
实例化 / G3 venue 覆盖 / G4 纳排样例+双审 / G5 机械停轮 / G6 P0-R8 校验器）——**执行零查询**，
待 reviewer search-design 签署 + owner 批准 → **Gate C**（探针开机前：探针协议 v2 + frozen run
manifest + dev-split 替换 + 修正案 §D Protocol gate 独立签字）→ **Gate D**（运行后：结果如实
入决策包 v2，不自动裁决）。

### 6.2 Round-2 可回放检索（协议已预注册，§3.6）

执行期硬约束：每检索/抓取一行 `search_events.jsonl` + raw response 存档 + sha256（**无 raw
capture 的查询=不存在**）；失败事件保留在分母；非英文命中 `awaiting_classification` 不静默丢弃；
找到「空白」不得提前停轮、找到占据者不得加限定词续命（收方偏置禁令 + post-hoc 日志）；
round-2 后的否定性结论仍**按身份索引** + 记录集版本钉定 + 强制伴随 token（协议 §6），不得写裸
saturated/novel/complete。

### 6.3 Stage-1B 四探针（协议 v2 待 Gate C 重写签批；v1 已作废）

设计要点（已按第三轮复审科学修正更新）：**共享池纪律**——四探针共用 P-α 池（c0=裸 prompt，
K=16，单次触碰，失败保留在分母）；**格**：C-ASR（LibriSpeech **dev-other**——test-other 系
publication holdout 不触碰）/ C-SER（CREMA-D 子集）/ C-AU（mmau-mini），每格 n=60–100；
模型 = 锁内 Qwen3-Omni-30B GGUF（llama-server 常驻）。

- **P-α 头空**：每格 (U_greedy, E[U_pool], U_oracle) → H(c)。**全格 H(c)≈0 → 停线上报 owner**
  （动摇整个 selector 纲领，不自行解释）。
- **P-β MBR 基线**：主臂 = 文献可比 BLEU 成对效用（1−WER 降为 sensitivity 臂）；检验能否重现
  LibriSpeech ~31% 量级与数据依赖性。
- **P-γ 同核信号 → 条件互补性**（修正案 §B 判读框架）：matched controls（correct /
  item-permuted / silence / hard-negative audio）测音频因果；有头空 item 上 error_corr ×
  complementary_gain 测独立价值；**若实现仅为 likelihood 打分，强制命名
  `same-core likelihood baseline`，不得称 strict-I2 独立信号**。开机前置：echo-logprob 打分
  路径 1-item smoke（从未验证过，不通过不开机）。
- **P-δ 供给对比**：c0 vs c1（签批前冻结 c1；仅 read-out 类供给）重测 H(c)/ρ(c)；若 c1 选
  检索，C-T7 式机检边界审计不得豁免（前科：+0.517 检索佐证因 gold 泄漏判 INVALID）。
- 探针纪律：不做显著性结论、不跨任务平均、全部尝试（含失败）入 attempt registry、结果只作
  Stage-1C 方向材料。

### 6.4 决策包 v2 与 Stage-1C 收官

决策包 v2 = 调研 + 探针**双证据**（owner 续40 裁决）：I1–I4/UMBRELLA 逐身份 kill/pivot/proceed
dossier + 供给收益/selector 收益分解 + 预算公平性 + 可证伪三结局判据。→ 独立盲重建 + 申请
STAGE1C_DECISION_READY → **owner 亲自选题，绝不自动滚入 Stage-2**。开放的 Stage-1C 问题：
agentic-loop vs 一次性 rerank（UMBRELLA 判别）。

### 6.5 理论轨道（standing 背景，非本轮交付）

Lean 4 机检轨道既有成果（2026-07-07，先于本轮）：`Realization.lean`（sorry-free）——选择器在
奖励估计误差 τ→0 时收敛到 oracle（realized ≥ oracle − 2τ）；`Iterate.lean`——约束迭代的单调
有界收敛 + 预算上界 N* + 无约束发散负结果。与本轮对象的对接点：ρ(c) 兑现面的经验研究即为
定理前提（τ 的大小与来源）的测量学；Stage-2 前须按「先证无约束发散、再证受约束收敛」纲领
扩展（`Theory-Convergence-and-Constraints.md`）。

## 7. 可证伪承诺（合同冻结判据摘录；裁决人=owner，Stage-1C）

| 身份 | kill-if | pivot-if | proceed-if |
|---|---|---|---|
| strict-I2 | 测试一：matched-controls 下同核 score 对音频无系统响应（delta/rank corr/winner margin/U 均无——坍缩为文本选择器，不必等测试二）。测试二：有头空 item 上高同错 **且** complementary_gain≈0（仅 selection_overlap 高不构成任何 kill 证据） | 仅外部 scorer 有效 → 坍缩回 I1 | 双信号分离且同核兑现为正 |
| I3 | 预算内测不到 speech N-best Goodhart 拐点 | 仅弃权分量有效（该分量已被占据，失去独立性） | 拐点可检测 / risk-coverage 优于 conformal 基线 |
| I4 | ρ(c) 实测为噪声，或矩阵级无头空（H(c)≈0 across cells） | 无增量预测力 → 降为工程实例化（不得作科学新颖性） | 曲面升级为相对通用 baseline 有**label-free 增量预测力**的规律 |
| UMBRELLA | 等预算 loop ≤ one-shot BoN/MBR/rerank | loop ≈ 一次性 rerank（只是 test-time compute） | 等预算下 loop 有真增量且 agent 实际接触音频 |
| 全局停线 | 探针全格 H(c)≈0 → 停线上报 owner——动摇整个 selector 纲领，不自行解释 | — | — |

强制报告清单（每次 selector 运行）：双 selector 各自 Recovery/PCS/rho/regret、rank correlation、
2×2 同错四格计数、selection_overlap（描述）、router 上界与 complementary_gain（修正案 §B）。

## 8. 诚实边界（本提案不含什么）

无任何已证新颖性主张（「空白」全部限定于 94 簇保留记录集且带强制伴随 token；检索宇宙缺失、
科学饱和不可评估）；round-1 检索宇宙**永久缺失**；census/ledger 均为单遍 AI + 独立抽样验收级
（人类双审=E2 待办；9 条 R3_MIXED_LOCATOR 在公开双审队列）；探针结果尚不存在（**GPU 零运行**）；
round-2 尚未发出任何查询；C1 的 config-selection 历史轨迹为已登记永久缺口；理论轨道的收敛
定理只覆盖 τ→0/预算约束的理想化前提，未触及供给条件化。本件按 P0-R8 状态门机检通过后提交。

## 9. 对 reviewer 的具体请求

1. **round-2 协议 v2 的 search-design 签署**（Gate B preflight 阻断项）：对 21 lanes / 105 条
   预注册查询、venue 覆盖、纳排样例、停轮规则做显式 active 裁决（PRESS 预检反馈与修复映射见
   协议 §13.3；沉默不生效）。
2. **身份合同压力测试**：六份合同的 kill/pivot/proceed 判据是否仍有不可执行或可被弹性解释的
   缝隙（尤其 strict-I2 两独立测试与 I4 增量预测检查点）。
3. **盲区点名**：您认为我们的 venue/查询/身份定义还漏了哪些邻域（特别是 2606.02981 /
   2607.05391 / 2602.12281 之外的集外压力）。
4. **探针设计预审**（Gate C 前非正式）：P-γ 条件互补性设计与 P-δ 供给对比是否存在我们未见的
   混杂；dev-split 与共享池纪律是否足够。

## 10. Provenance（工件 → commit 锚）

| 工件 | 锚 |
|---|---|
| 身份合同 v1（FROZEN） | dce5c79（blob sha256 `1338f6b1…`，核验 `git show dce5c79:wiki/2026-07-14-identity-contracts-v1.md \| sha256sum`） |
| 修正案 №1（EFFECTIVE） | 0a5e108（blob `d9e2ab5e…`） |
| census v2 + ledger v2 | 28ad858；版本 pin 收尾 b594820；验收抽样 b1af8c6 |
| RESP-01..04（三轮评审回应链） | RESP-02（现行有效）= `2026-07-14-p0r-response-to-remediation-rereview.md`；RESP-04 = `2026-07-14-resp04-gate-a-execution.md`（5db6cc4） |
| 第三轮复审（收档原文） | a06a498 |
| C1/C4 census | `docs/integrity/2026-07-14-c{1,4}-*-census-draft.md`（0a5e108 关闭） |
| P0-R8 校验器 v2 | fcd1c57（`scripts/integrity/p0r8_state_gate.py`） |
| round-2 协议 v2 + PRESS | 18056f1 + aaffe4c；PRESS feedback = `docs/checks/2026-07-15-round2-press-feedback.md`；机械重数 = `docs/checks/2026-07-15-round2-query-recount.txt` |
| replay bundle（round-1/Survey v2） | `wiki/survey/replay/SURVEY-RESP-2026-07-14-01/`（INTERNAL_BUILD_CONSISTENCY_12/12——仅字节线） |
| 决策日志 | Decision-Log 续34–续44 |

本件 blob hash 以提交 commit 为准（核验命令 `git show <commit>:<path> | sha256sum`）。
