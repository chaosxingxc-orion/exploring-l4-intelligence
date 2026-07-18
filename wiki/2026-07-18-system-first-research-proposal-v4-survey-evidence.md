---
artifact_id: "STAGE1A-PROPOSAL-2026-07-18-05"
title: "System-first Research Proposal v4——Stage-1A 调研证据呈报版（预映射证据基座 + 映射执行计划）"
date: 2026-07-18
addressee: "Gate S1 评审人 / 评委"
stage_position: "阶段正典 v2（2026-07-18 dated supersession,owner 裁决①）下的四字段记账:current_activity_stage = Stage-1A survey-ready gate（问题与 survey 设计;Gate 签署后第一条 systematic query 进入 Stage-1B = mapping 执行,全程禁研究模型含 smoke——owner 已签署）;new_model_touches_since_gate_freeze = 0（起算 = S0 签署后的 gate 冻结链,af96a89 起）;cumulative_model_touches = 非零（2026-07-05..10 战役等,见 exposure union）;legacy_experiments = INHERITED_PRIOR_EXPOSURE（正典 = wiki/2026-07-18-inherited-prior-exposure-union.md,后续 held-out/预注册显式排除或分层）;创新点未锁定（owner 裁决:现在只锁研究方向与内容）"
relation_to_v3: "v3-consolidated（STAGE1A-PROPOSAL-2026-07-15-04,blob 见 bundle manifest correction #3/#4 链）之「ACCEPT AS WORKING THESIS」裁定**不重开**;本件新增 = §3 预映射证据基座（C4B/C4C 两批产出的可回放证据）与 §4 执行计划现值;研究纲领/RQ 树/五合同/蓝图以 v3 为正典,本件只引不改"
evidence_grade: "本件所有占据/空位/机制陈述 = directional-only / hypothesis-grade（Stage-1 证据等级,永不自动升级);证据模式逐 claim 五值枚举标注（amendment-9 §2）,全量矩阵 = wiki/survey/2026-07-18-sf-v4-claim-evidence-matrix.md——协议包的本地结构与计数可机器重放（九项门禁,MACHINE_REPLAYED_STRUCTURE 级）,外部论文数字仅可追溯到来源页/表（SOURCE_REPORTED_TRACEABLE,未独立复验）,两者永不混称"
integrity: "凡「已占据/空白」句均为对**已检视集合**的普查事实,不外推为文献全集结论——系统性 mapping 尚未执行,这正是本 proposal 申请执行的工作"
---

# Research Proposal v4——Stage-1A 调研证据呈报版

## §0 导读：这是什么、不是什么

**是**：向评委完整呈报截至 2026-07-18 的**预映射调研证据基座**（种子景观、34 哨兵、七篇
直接邻近工作的全文深读普查、负结果先验、发现机制的实证教训），以及据此冻结的**可回放
mapping 执行计划**。**不是**：survey 结果报告（mapping 一条查询未跑）；不是创新点声明
（owner 未锁定，任何「创新点成立/不成立」定性在现阶段两侧皆为时过早——含 P0-R9 评审 §4
的定位代拟，标 owner 未签）。

**阶段自答（阶段正典 v2,四字段）**：`current_activity_stage` = **Stage-1A survey-ready
gate**（问题与 survey 设计）。已发生 = 协议冻结 + 定向 ID dereference/raw provenance/全文
准备/校准性引文试验 + 哨兵工程；`new_model_touches_since_gate_freeze` = **0**（起算
af96a89）、系统性 discovery 查询 = **0 条**；`cumulative_model_touches` = **非零**——项目
历史含 2026-07-05..10 战役的真实模型实验（frozen Qwen3-Omni-30B 真 best-of-N n=144、
oracle-WER、224-cell grid 等），全部登记 `INHERITED_PRIOR_EXPOSURE`（正典 =
[[2026-07-18-inherited-prior-exposure-union]]，不删除、不降格、不归零——是后续 held-out/
预注册必须显式排除或分层的 exposure union）。Stage-1B（= mapping 执行）未放行;模型实验
自阶段正典 v2 起属 **Stage-2A**（复现先行），更未放行。

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

**普查结论（对已检视集合的事实,非文献全集结论;编码轴层级按 v4 复审 P0-3 + owner 裁决④
更正）**：上表四轴（黑盒/单核/speech-omni/候选选择）自本更正版起降格为**组件级**普查——
「候选选择」不是 RQ-SYS（sequential external control）的充分判据轴。**系统级**占据判断改用
amendment-9 §3 的 **system-control 13 轴 schema**（decision rights/控制时域/状态记忆/工具/
停止预算/终态合成/信息边界…）,已对评审供给的 8 项 system-level 直接近邻执行（known-item
DFS,见 [[2026-07-18-sf-known-item-dfs-systemcontrol]]）。组件级事实维持：七篇零篇同占四轴;
主流多模态 TTS 综述明文不覆盖 audio（此为该综述的范围边界事实,不单独构成空位证明）。
**系统级空位是否成立、值不值得占据 = Stage-1B mapping + 13 轴编码要回答的问题,本件不预判。**

### §3.2 负结果与异质性先验（对后续实验设计的直接约束;异质案例共同提示——P1-1 更正:非同一假设的独立复制）

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

**对本纲领的直接落点（双向证据综合,P1-1 更正——三篇为异质案例〔任务/模型/信号/目的均
不同,非同一假设的独立复制〕,以下为「共同提示」而非「独立收敛证明」;各条限定于该论文
报告的模型/任务/设置内）**：

- **支持列**（何者被加强）：MBR/majority 等 K 强制基线纪律、headroom 归因纪律（无头空
  null 只否定供给配置）、供给条件量 H(c) 换供给必重测——三者与上述观察方向一致。
- **反证列**（何者被削弱）：「复杂 evaluator/selector 优于简单基线」的预期价值被三个案例
  削弱（PRM null/self-refinement 退化/SVF 封顶）;若我们的 reward-guided control 在有头空
  池上仍不敌 majority vote,即直接反证 RQ-CTRL。
- **单观察 kill 判据**：在验证过头空存在（oracle−默认 > SESOI 量级）且 rollout 误差独立性
  达标的池上,reward-guided 选择仍稳定 ≤ 等 K majority——该单一观察即杀死「奖励引导承载
  增量」假设的当前形态。
- **未决替代解释**：上述三案例的 selector null 也可能由「MCQ 短答案域的选择空间过小」「PRM
  域失配」「自评偏差」解释——speech/omni 生成域是否同构,待 Stage-2A 复现裁决。

STAGE2A_REPRODUCTION_AND_PROTOTYPE_BACKLOG（P0-1 更正:此为 Stage-2A 待办,非 Stage-1B——
Stage-1B 只从文献编码这些轴）：rollout 误差独立性作头空前置、可解析性修复先于 selector
比较、selector 强度≤核心理解强度、over-compute 拐点、指令遵循前提。

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

## §4 映射执行计划（= **Stage-1B**,阶段正典 v2;签署后即可执行,全程可回放,**全程不运行
研究模型**）

0. **开局 = known-item 保证性 DFS 队列**（amendment-9 §4:评审供给 8 项 + Team of Thoughts/
   ToolGate 零命中身份保留;每轮产出 known-item carry-forward ledger——归档不是遗忘许可）。
1. **BFS**：65 条冻结查询 + 50 T1 路由全量执行,命中做题录/摘要级编码（REC-0 落账,五计数
   机器导出;75-cap 溢出走 YEAR/MONTH splitter）。
2. **DFS 触发**（四判据:对象/问题/要素/结论冲突重合）→ 全文精读（方法占据四问 + D2 八轴,
   validator V1–V15 机器强制）;队列排序 =（威胁度↓, core>element, 时新性↓, 梯队平局）,
   2025+ 先于前时代（agent-era 裁决;窗口不砍、时代先验不进 study_quality）。
3. **退出** = E1∧E2∧E3 + 逐轮饱和表（PRISMA-S 兼容);E2 饱和宣称前必须完成 work-level
   identifier resolution（债务 D-1,否则只能说「已解析子图上零新增」）。
4. **产出**：system-level（13 轴）+ component-level 双层 occupancy 普查 → 负结果与冲突
   证据 → 饱和轨迹 → legacy exposure union 复核 → 3–5 candidate problem cards（v3 §3 卡
   纪律 + P1-1 四行:支持/反证/单观察 kill/未决替代解释）→ **Stage-2A prior reproduction
   shortlist**（复现先行合同 = amendment-9 §5,Stage-1C 冻结不执行）→ Stage-1C owner 选题。
   债务表 D-1..D-5 带 owner 与截止 gate（amendment-8 §4）。

## §5 诚信声明与请求

**声明（逐条标证据模式,amendment-9 §2）**：①协议包的本地结构/计数/前缀哈希/matcher/
validator 可用回应信 §5 九条命令零联网重放（`MACHINE_REPLAYED_STRUCTURE`——该能力包络
**不含**外部论文数字）;②本件引用的外部研究数字 = `SOURCE_REPORTED_TRACEABLE`（可定位到
来源论文,未独立复验;逐条见 claim-evidence 矩阵）;③「联网活动全量入台账、discovery
query = 0、未执行未登记的查询/模型调用」= `TEAM_ATTESTATION`（签字承诺——台账在场性不能
机器证明不存在未登记活动,不称机器证明）;④证据等级 directional-only 不升级;⑤创新点未
锁定,本件不含任何占据/空位的终局定性。

**向评委的请求**：①按 P0-R10 验收表复核 correction #4C（双向合同:0 新 MAJOR/0 新 MINOR
→ 签署 Gate S1 mapping-execution）;②本件作为随附呈报阅览,**不新增签署对象、不重开 v3
working-thesis 裁定**;③签署后仍需 owner 执行批准（三方分立）,首条查询才会执行。

—— 研究执行方（W1）,2026-07-18。本件随提交入 git;更正走 dated correction。

## 附录 A：参考文献（自包含引用表,P1-2）

| 引用 | 作者/年份 | 稳定链接 |
|---|---|---|
| Training-Free Multimodal Large Language Model Orchestration | Tianyu Xie et al., 2025 | https://arxiv.org/abs/2508.10016 |
| ThinkOmni: Lifting Textual Reasoning to Omni-modal Scenarios via Guidance Decoding | Yiran Guan et al., 2026 | https://arxiv.org/abs/2602.23306 |
| Limits and Gains of Test-Time Scaling in Vision-Language Reasoning | Mohammadjavad Ahmadpour et al., 2025 | https://arxiv.org/abs/2512.11109 |
| Test-Time Scaling in Multimodal Foundation Models: A Comprehensive Survey (ACL Findings 2026) | Cong Wan et al., 2026 | https://arxiv.org/abs/2606.08231 · https://aclanthology.org/2026.findings-acl.383/ |
| Test-Time Scaling for Small VLMs on Multilingual Visual MCQ | Spiros Baxevanakis et al., 2026 | https://arxiv.org/abs/2607.09438 |
| On Test-Time Scaling for Vision-Language Models | Fawaz Sammani et al., 2026 | https://arxiv.org/abs/2606.28864 |
| dMLLM-TTS: Self-Verified and Efficient Test-Time Scaling for Diffusion Multi-Modal LLMs | Yi Xin et al., 2025 | https://arxiv.org/abs/2512.19433 |
| Deep Video Discovery (DVD) | Xiaoyi Zhang et al., 2025 | https://arxiv.org/abs/2505.18079 |
| Seg-Agent: Test-Time Multimodal Reasoning | Chao Hao et al., 2026 | https://arxiv.org/abs/2605.12953 |
| Memory-Augmented Vision-Language Agents（fresh L12 held-out） | Tommaso Galliena et al., 2026 | https://arxiv.org/abs/2603.24257 |
| ToolGate: Token-Efficient Pre-Call Control for Tool-Augmented VL Agents | Anjie Liu et al., 2026 | https://arxiv.org/abs/2606.03054 |
| ATLAS: Agentic Test-time Learning-to-Allocate Scaling | Peijia Qin et al., 2026 | https://arxiv.org/abs/2606.01667 |
| LLMs Improving LLMs: Agentic Discovery for Test-Time Scaling（AutoTTS） | Tong Zheng et al., 2026 | https://arxiv.org/abs/2605.08083 |
| Scaling Test-Time Compute for Agentic Coding | Joongwon Kim et al., 2026 | https://arxiv.org/abs/2604.16529 |
| Team of Thoughts: Efficient Test-time Scaling of Agentic Systems | Jeffrey T. H. Wong et al., 2026 | https://arxiv.org/abs/2602.16485 |
| Inference-Time Scaling of Verification（DeepVerifier, ACL Findings 2026） | ACL Anthology 记录, 2026 | https://aclanthology.org/2026.findings-acl.1243/ |
| Scaling Unverifiable Rewards: A Case Study on Visual Insights（ACL Findings 2026） | ACL Anthology 记录, 2026 | https://aclanthology.org/2026.findings-acl.1724/ |
| A Reward-Guided Dual-Phase Framework for Adaptive Inference-Time Reasoning（ACL Findings 2026） | ACL Anthology 记录, 2026 | https://aclanthology.org/2026.findings-acl.511/ |

（arXiv 条目作者/日期取自本仓正典 raw Atom 字节〔`docs/survey-provenance/atom/`,sha256 台账〕;
ACL 条目以 Anthology 页为准,PDF 已官方源救援入 `survey-backups/`。§3.2 各外部数字的页/表
locator = claim-evidence 矩阵逐条给出,本件散文不重复。）

## 修订记录（v4 复审整改批,2026-07-18——审 @6bfa17f 态,WITHHOLD → 本更正版）

1. **P0-1**：frontmatter 与 §0 改四字段阶段账（阶段正典 v2 dated supersession;
   cumulative_model_touches 如实非零 + INHERITED_PRIOR_EXPOSURE 指针）;§3.2 实验轴改标
   STAGE2A_REPRODUCTION_AND_PROTOTYPE_BACKLOG;§4 冠名 Stage-1B 并加禁模型条款。
2. **P0-2**：「全部承重数字可机器复跑」两处删除,改五值证据模式逐条声明 + claim-evidence
   矩阵;attestation 降为 TEAM_ATTESTATION 措辞。
3. **P0-3**：§3.1 四轴普查降组件级,系统级改 13 轴 schema + known-item DFS 件。
4. **P0-4**：ToolGate 与 Team of Thoughts 获保证性 DFS 入口（八项全为评审供给;后者零命中
   身份 = 我方 matcher 复现的主动补充披露）,零命中身份保留。
5. **P1-1**：§3.2 改双向三栏 + 单观察 kill + 未决替代解释;「独立收敛」改「异质案例共同提示」。
6. **P1-2**：本附录 A + 引文作用域限定 + 拼接引标注。
7. **P1-3**：known-item carry-forward ledger 纪律入 §4 与 amendment-9 §4。
   原 @6bfa17f blob 保留于 git 历史,不改写。
