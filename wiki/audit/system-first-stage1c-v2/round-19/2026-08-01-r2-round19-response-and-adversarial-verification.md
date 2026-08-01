---
title: "R2 round-19 逐项回应与对抗核验：20/20 引文属实（2 件定性纠错）、5 MAJOR 采 3 半采 2、TFRL 条款按续82③ 不采"
date: "2026-08-01"
artifact_type: "RESPONSE"
campaign: "system-first-stage1c-v2"
round: "round-19"
response_target: "wiki/audit/system-first-stage1c-v2/round-19/2026-08-01-r2-v17-1-multiround-adversarial-doctoral-supervisor-review.md（边界纠偏版=操作版）"
superseded_initial_version: "同目录 *-initial-version-sidecar.md（7 MAJOR 初版；提交前被协同纠偏原位改写，sidecar=会话转录级重建留痕，无裁决效力）"
review_target: "proposals/2026-07-29-r2-coreview-draft.md @ 2d2cf52 blob bbc41c9e（工作树逐字节亲验一致）"
verification_channels: "①blob/正文指控=主会话亲验（git hash-object+逐行定位）；②20 件引文=隔离 Opus 代理一手 WebFetch/arXiv API；③本地读集覆盖=隔离 Sonnet 代理扫 registry+stage1c-portfolio"
citation_verdict: "20/20 真实存在、零虚构；2 件定性错误（AgenticASR、G-SPIN，详见 §2）"
acceptance: "MAJOR-1 采；MAJOR-2 采（最硬：提案自身词典内部不一致）；MAJOR-3 采（带三点修正）；MAJOR-4 半采；MAJOR-5 半采且其 TFRL 条款按 Decision-Log 续82③/续85 不采；MINOR-1..5 全采"
owner_rulings: "Decision-Log 续85（round-19 边界纠偏生效+TFRL 身份维持+v18 重构授权+对抗自检基线要求）"
authority_effect: "RESPONSE_ONLY_NO_EXECUTION_GRANT；不授予 Stage-2A/模型/指标/数据集获取/push"
exposure: "本件核验含：隔离代理对 20 件论文官方页/PDF/arXiv API 的 WebFetch/WebSearch（引文核验目的，owner 指示范围内）；零模型调用、零指标运行、零数据集（研究数据）获取；继承 v17.1 之前全部已披露 exposure"
---

# R2 round-19 逐项回应与对抗核验

## §1 核验方法与证据边界

按评审回应协议先逐条独立核验、再逐点回应。三通道：

1. **对象绑定与正文指控（主会话亲验）**：`git hash-object` 复算工作树提案=blob
   `bbc41c9e`=HEAD `2d2cf52`，与评审 frontmatter 绑定一致；评审对提案正文的每条指控逐行
   定位核对（行号见 §3）。
2. **引文真实性（隔离 Opus 代理，一手源）**：20 件逐件 WebFetch 官方页/PDF；4 个 arXiv id
   经 arXiv API 交叉验证（id→题名/一作全部对应）；8 件承重新近邻做全文级定性核对。
3. **本地读集覆盖（隔离 Sonnet 代理）**：20 件对 `wiki/survey/registry/` 与
   `wiki/survey/workbench/stage1c-portfolio/` 双目录扫描，判 REGISTERED/ABSENT。

版本处置：初版评审（7 MAJOR、新颖性驱动尺度）在提交前被 owner 与评审方协同纠偏为
「边界纠偏版」（`novelty_review_in_scope: false`、5 MAJOR 全报告层）。初版以 sidecar
重建留痕（见 frontmatter），纠偏版为唯一操作版。本回应针对纠偏版。

## §2 引文核验：20/20 真实、2 件定性纠错

**零虚构、零链接错配**：全部 20 件 URL 解析到题名/作者/年份/发表处一致的真实论文。承重
四件（PlanRAG-Audio、GRGA、ATIR、MARS）定性**准确**——特别地 GRGA 原文逐字含
"training-free"、"without parameter updates"、POMDP（6 处）与五段管线；ATIR 自述
"train our ATIR model"（确非 training-free）；MARS 检索选择对象确为对话历史上下文。
PlanRAG-Audio Table 1 逐字含 transcript/speaker/emotion/sound_event 多流。

**两件定性错误（入矩阵前须按本节更正，不得继承评审行描述）**：

- **AgenticASR（2607.28175）**：评审称其含 "intent routing"——全文 0 命中（"routing"
  0 命中）。该特性属同一第一作者（Zixuan Jiang）另一篇 2605.29430（其摘要明列
  intent routing）。评审串写了两篇同作者 2026 论文。其余两点（流式 active-context
  revision、不含外部知识检索）核验属实。
- **G-SPIN（2026.acl-industry.151）**：评审称其做 "entity description/世界知识消歧发音
  候选"——"entity description" 在其 PDF 仅出现一次且在**参考文献**（引 DANCER 题名）；
  "world knowledge/external knowledge/knowledge base" 全部 0 命中。G-SPIN 实为
  音素级 GNN 候选邻域+masked-LM 句内上下文评分+LLM 受限重排，**无外部知识源**（另注：
  其 GNN 有离线训练阶段，"inference-time" 仅指部署形态）。「世界知识消歧发音候选」的
  占据者是 DANCER（2024），不是 G-SPIN。

**读集覆盖分层（本地扫描结果）**：ConEC/PRISM/RECOVER/WavRAG 已在提案证据底座；
Contextual Earnings-22 已在提案 §8「应登记九件」（评审第五线引用不构成漏检指控）；
**Interactive ASR 2605.29430 已在 stage1b registry（shard 行 62）+D1 dossier**——属
R2 矩阵路由缺口而非发现缺口；Pundak/DANCER/Wang2026 在项目更大语料面存在但未入 R2
读集。对全项目均为新件的：PlanRAG-Audio、GRGA、ATIR、MARS、AgenticASR、G-SPIN、
FineCoS、CB-Whisper、Liu-Trie、Chan 2023、Modica（约 11 件）。

## §3 MAJOR 逐项回应

### MAJOR-1（总问题/子问题/主张层级不唯一）——采

指控属实：现稿能力上界主张（§0/§6.2 H-SYS）、双源承重腿（§0/§8）、机制核发音库（§2.3）、
组织优化支柱（§3.4）并立无层级。v18 动作：采一句话总问题+RQ0–RQ4 层级；技术模块降为
RQ 候选方案；「能力上界」改「预注册配置族内最佳已测系统效果」（并入 MINOR-2）且不再统领
章节。与续83①（三支柱维持、开题不预判收敛）兼容性声明：RQ/WP 化是**重排非收窄**，三支柱
全部保留为 WP 内容，无一退场。

### MAJOR-2（ORG/SUPPLY/USE 定义层清楚、运行层混层）——采（本轮最硬指控）

核验确认这是**提案自身词典的内部不一致**而非评审外加口径：§1.3（137–138 行）已把重听归
「②对已有观测的重表达」、把准入归「使用」形式；而 §6.3（584–585 行）把
`RE_RESOLVE/RE_SLICE/ADMIT/REJECT/ANSWER/STOP` 全部装进「对统一知识接口的查询族」。
另核实：SRC-sel 绑 K5（559 行）、档 B 在阶段二组织标题下做运行期动作选择（347–350 行）、
O-config 锚 SLUE-SQA-5 与 NB 主载体分离（365/554 行）——五处错位全部属实。v18 动作：
唯一词典贯穿（OBS/CONTROL 独立出知识三形式；统一动作空间保留但逐动作打层标签）；新增
全篇唯一「模块→RQ→形式→变量→判据→失败出口」映射表；跨层臂只答整体读数。该修正同时
**锐化**双源叙事：一源=观测、一源=外部知识，正是「双源」对比的语义基础。

### MAJOR-3（现状非问题地图+2026 组织/规划检索遗漏）——采，带三点修正

采：PlanRAG-Audio/GRGA 真实存在且如其所述，§3.3「语音域读集内全部缺席」（322 行）与
§3.4「读集内无人做」（352 行）不可维持，必须重写；五条研究线骨架采纳为 v18 现状结构。
三点修正随回应记录：①现稿排他句均带「读集内」限定语，属诚实限定下的读集不完整，非表述
失真；②Interactive ASR/Contextual E-22 两件的「遗漏」定性降级为路由/义务欠账（见 §2）；
③新件入矩阵不得继承评审行描述（AgenticASR/G-SPIN 已证有串写），一律按本地全文引用约定
fetch+hash+自读后入表。

### MAJOR-4（为何引知+如何评价未成闭环）——半采

采：参数知识/外部知识/音频观测三者边界、主载体可支持结论的如实声明、Need→Access→Use→
Outcome→Cost 五段链作为叙事主轴，进 v18。顶回其「未形成完整问题链」的缺席定性：现稿已有
H0/H-SUPPLY/H-USE/H-ORG/H-SYS 可证伪假设链（546–549 行）与四层评价（§6.5，不合成总分），
纠偏版 §6.2 自己亦承认五段链「可以自然对应现稿的 oracle、消融、诊断和成本向量」——v18 的
工作是**重述与补边界**，不是新建。第二类载体（后 cutoff/私域）在开题层面**具名为义务**、
不作为签字前完成项（纠偏版 §2 边界一致）。

### MAJOR-5（阶段/模块/产出不一一对应）——半采；TFRL 条款不采

采：三工作包（WP1 组织/WP2 供给与控制/WP3 使用与评价）+每包最低学术产出+失败出口的表述
结构，进 v18。顶回其「失败时如何调整没有说明」的缺席定性：现稿 K-NB 判死→能力上界放弃、
K5-t 判死权、§5.3 回退梯①–④、§8 MERGE 触发均为既有失败出口，v18 将其归位到各 WP 而非
新建。**不采条款**：「TFRL、bandit 或配置搜索……不应在开题阶段成为必须证明的身份主张」
与 Decision-Log 续82③ 正面冲突（owner 已裁：TFRL 身份保留、档 B 为身份承载形态、须按
MDP/bandit 对象正式化）。续85 重申该裁决：v18 保留档 B 身份主张及其 K-RL 判据，同时按
纠偏版要求把它定位为 WP2/WP3 内的**方法身份主张**而非总研究问题。

## §4 MINOR 回应（全采）

1. "ASR-free"→「无独立专用 ASR 前端」（运行时定义 §0 保留，术语改名）。
2. "能力上界"→「预注册配置族内最佳已测系统效果」（判据/降级条款不变）。
3. "双源知识动作"→「双源信息获取/控制动作」。
4. `V̂`→校准前称 heuristic action score。
5. frontmatter/review_chain 同步 v18/round-19（含签字表 companion）。

## §5 v18 整改承诺清单（对应纠偏版 §10 最低条件）

- [ ] 一句话总问题+RQ0–RQ4 固定（骨架已授权，措辞 owner 签字栏生效）；
- [ ] 参数知识/外部知识/音频观测/重解析动作边界成节；
- [ ] 唯一词典贯穿动作/模块/假设/评价；OBS/CONTROL 独立；
- [ ] 现状改五条研究线+代表工作入 ORG/SUPPLY/USE/CONTROL 矩阵；
- [ ] 删「无人做/全部缺席/唯一空位」排他句（新颖性判决出域，双向不作）；
- [ ] 模块→RQ 唯一映射+独立评价+失败解释；
- [ ] 五段评价链成节；有效性/合理性/可靠性/效率分立指标族；
- [ ] 三工作包+载体适用边界+最低学术产出+失败出口；
- [ ] 签字表一页内可复述新结构；
- [ ] 文献收编义务：11 件 fetch+hash+ledger；PlanRAG-Audio/GRGA/ATIR/MARS D2 深读；
      AgenticASR/G-SPIN 带 §2 纠错定性登记；Interactive ASR/Pundak/DANCER/Wang2026 路由入
      R2 读集。

本件为回应与核验记录，不授予任何执行权限；v18 交付后按 owner 基线要求跑多轮隔离对抗
自检环（隔离上下文面板+重新搜索+监督核验，至一轮零新发现）再送窄面复审。
