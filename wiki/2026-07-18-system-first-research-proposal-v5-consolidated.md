---
artifact_id: "STAGE1A-PROPOSAL-2026-07-18-06"
title: "System-first Research Proposal v5——整改后合并送审版（Stage-1B survey-execution 签署申请随附件）"
date: 2026-07-18
addressee: "Gate S1 评审人 / 评委"
relation: "v3-consolidated 之 working-thesis 裁定不重开;v4（调研证据呈报版,审 @6bfa17f → WITHHOLD → 更正版已随批入库,修订记录 7 项在案）之全部整改内容**并入本件成一自包含送审件**;v4 复审回应信（survey/2026-07-18-gate-s1-v4-response.md）为逐项对账载体;本件不新增签署对象——签署对象 = 阶段正典 v2 + 整改批 @0817ba6 + 九项门禁重绿"
stage_account: "四字段（阶段正典 v2,2026-07-18 dated supersession,owner 签署）:current_activity_stage = Stage-1A survey-ready gate;new_model_touches_since_gate_freeze = 0（起算 af96a89）;cumulative_model_touches = 非零（27 历史事件,见 §2.2）;legacy_experiments = INHERITED_PRIOR_EXPOSURE（正典 = wiki/2026-07-18-inherited-prior-exposure-union.md）"
evidence_discipline: "逐 claim 五值证据模式（amendment-9 §2）;矩阵 = v4 矩阵（wiki/survey/2026-07-18-sf-v4-claim-evidence-matrix.md,scope=v4）+ **v5 增补矩阵**（wiki/survey/2026-07-18-sf-v5-claim-evidence-matrix.md——本件全部新数字与量词逐 claim ID）;占据合取量词一律引用 identity taxonomy v2 机器重算（docs/checks/2026-07-18-sf-identity-taxonomy-v2-test.json,含独立语义反例区）;外部论文数字一律 SOURCE_REPORTED_TRACEABLE（可定位未复算,效力限该论文设置内);占据/空位陈述 = directional-only,创新点未锁定（owner 裁决,任何『成立/不成立』定性两侧皆为时过早）"
---

# Research Proposal v5（整改后合并送审版）

## §0 导读

**是**：v4 复审（WITHHOLD,P0-1..4/P1-1..3）整改完毕后的**自包含**送审件——治理基座（§2）、
调研基础设施（§3）、预映射证据基座详呈（§4,含七篇组件级普查与八项 system-control
13 轴普查）、Stage-1B 执行计划（§5）与 Stage-2A 冻结草案预告（§6）。**不是**：survey 结果
报告（systematic mapping 查询 = 0,执行即 Stage-1B 起点）;不是创新点声明。**申请**：签署
**Stage-1B survey execution**（双向合同:0 新 MAJOR/0 新 MINOR → 签;签署后仍需 owner 执行
批准,三方分立）。

## §1 研究纲领（v3 正典摘引,一页版）

**北极星**：weight-frozen reward-guided inference-time optimization（TFRL）——不改权重、
不改结构,用外部控制平面激活冻结 speech/omni 多模态 LLM 的预训练知识。**身份三轴（S0 已签,
TF-Strict）**：严格黑盒（只见文本输出）/ 全系统零训练（含外部组件）/ 单一冻结 omni 核心。
**信息边界**：read-out（允许）/new-info（禁止）;test-item gold 永不入任何路径。

**研究问题树（据 v3 §3 摘引,正典以 v3 原文为准,全部为待证伪假设）**：RQ-SYS（外部
reward-guided sequential control 能否在**相同初始任务信息与显式记录的 decision rights**下,
获得终态-only 选择不能获得的**实质性且可复核**的额外效用——天花板依供给/候选构造/调用权/
信息边界条件化定义,两侧 headroom 分别报告,不宣称「打破同一 oracle ceiling」）/ RQ-CTRL
（增量归因于奖励引导而非更多采样/调用）/ RQ-OMNI（非文本模态是否因果参与）/ RQ-SAFE
（reward hacking/过优化拐点与停止）/ RQ-MEASURE（label-free observables 预测头空与失败
regime）。Stage-1C 收敛为 3–5 候选问题卡（每卡:支持证据/反证证据/单观察 kill 判据/未决
替代解释 四行强制）。

## §2 治理与诚信基座（v4 复审整改的制度化产物）

### §2.1 阶段正典 v2（dated supersession,owner 签署）

分界依据 = **活动目的与证据用途**：1A 问题与 survey 设计 → **1B systematic mapping 执行
（全程不得运行研究模型,含 smoke——owner 签署在案）** → 1C 证据综合与选题（2A 合同冻结不
执行）→ **2A 复现最近邻先行 + 方案探索（方向性原型/小样自此在此）** → 2B 方案验证 → 3
发表。旧「1B=方向性原型」语义入墓碑;正典全文 = `wiki/Research-Methodology.md`。

### §2.2 exposure union v2（四仓覆盖;历史不归零;「全量」称谓已按 v5 复审 P0-1 撤回重立）

**四仓考古完成**（union v2 dated supersession）：W1+umbrella = 27 事件（30B 真 best-of-N
n=144、oracle-WER、七集 n=150 头空扫描、Wave-1 双底座 224 格网格、KB 嵌入等）;**W4 =
≈70 事件**（二轮考古收敛,changelog 4172 行全通读;omni-embed-nemotron-3b 主力 + jina/
Gemma-4-E4B/12B/Voxtral/Qwen3-ASR/API-verifier 等 **8 个实际推理研究模型**,CoVoST2
val1758+locked test1695、HeySQuAD、URO、SLURP、MInDS 等 **14 数据集**;**选择决策污染面
≥11 处**〔模型推理级选择运行 5 条 + 离线选择器决策〕= 最高优先隔离面;MInDS 手工 JSON
事故→clean redo 全链与 R2 oracle-artifact 更正**并列入账**,评审点名七族全部映射零排除;
**W4 计数证据模式 = 考古估计**〔组级行含多运行,粒度异构——REVIEWER_INFERENCE +
TEAM_ATTESTATION 级,规范化 event ledger 延至 Stage-2 held-out 冻结前,re-review P1-3〕）;
W2/W3 = 零实验骨架（直验）;仓外边界 =
owner attestation（TEAM_ATTESTATION,不称机器证明）。计数按表行机器可数、粒度异构不作单一
聚合;两仓 omni-embed 同源战役已去重注记。**全部历史数字 =
PRE-METHODOLOGY_DIRECTIONAL_EVIDENCE**;union v2 落盘前冻结的 fresh/held-out 切分无效,自
v2 起解除冻结。正典 = `wiki/2026-07-18-inherited-prior-exposure-union.md`（v2）。

### §2.3 证据模式与完成态语言纪律

五值互斥枚举逐 claim 标注（MACHINE_RECOMPUTED_LOCAL / MACHINE_REPLAYED_STRUCTURE /
SOURCE_REPORTED_TRACEABLE / REVIEWER_INFERENCE / TEAM_ATTESTATION）;**完成态语言必须与所引
验证机制的能力包络相等**（敌意内审环新增强制镜头）;九项门禁 = MACHINE_REPLAYED_STRUCTURE
级,**不覆盖外部论文数字**。矩阵 = v4 矩阵 + **v5 增补矩阵**（`survey/2026-07-18-sf-v5-
claim-evidence-matrix.md`,scope 各自 frontmatter 明载——量词级称谓仅当矩阵实际覆盖被引文件的完整 claim 集合时可用）。

### §2.4 评审轨（双向诚信记录）

五轮对抗复审（correction #4→#4A→#4B→#4C→v4 批）全档留痕;P0-R9 轮我方**首次有据部分异议**
（0-hit 表 2/7 不成立,matcher 复现 + PRESS 独立收敛）,v4 复审**正式撤回该误判**并独立重放
九项门禁 9/9——异议成立与错误撤回双向在案。PRESS 式独立查询复核已制度化（隔离代理 + owner
抽查;首轮 HARDCODING NO,其 MAJOR〔steering 词族〕冻结前采纳,思想实验 3/3 命中）。

## §3 调研基础设施（冻结、机器可回放、零执行）

| 层 | 现值 | 正典 |
|---|---|---|
| arXiv 冻结查询 | **65 条 / 14 查询 lane**（版本链 sfqc-1.0.0→1.5.0;SF-L9 谱系道零查询;prefix61 逐字节不变,sha256 入 canon）;**SF-L14/L15 方法占位轴零 agent 连词、13 类类目全并集** | queries.jsonl + 协议 §4 |
| T1 会议路由 | 50 routes（10 会×2022–2026）+ 词表 73 项零通配符 | routes v3 + wordlist v1 |
| 种子 / 哨兵 | 92 列名种子;**34 哨兵 / held-out 6**（held-out 6/6 纯查询召回〔离线 matcher 复现〕、era≥2025 机器强制;存量含 3 篇 SEED_GUARANTEED） | manifest + sentinel-data + recall 检查件（outcome_counts） |
| known-item 保证队列 | **共 8 项,全部评审供给**（Team of Thoughts 在内;其 65 查询零命中身份 = 我方 matcher 复现的主动补充披露〔评审未测〕）;零命中者（ToolGate/Team-of-Thoughts）保留反例身份;drift 3 例阈值只管未知漂移 | amendment-9 §4 |
| 退出机制 | E1 BFS 干涸 ∧ E2 引文闭包 K=2（饱和宣称前置 = work-level identifier resolution,债务 D-1）∧ E3 哨兵清零;逐轮饱和表 PRISMA-S 兼容 | amendment-7/8 |
| 门禁 | fail-closed 全绿 + mutation harness 10/10 + validator 26/26;可回放性三级（bundle-only/local-data/network-dependent） | #4C 回应信 §5 九项 |

## §4 预映射证据基座（调研结果详呈;hypothesis-grade）

### §4.1 组件级普查（七篇威胁集,全文 DFS,引文抽查 11/12）

| 论文 | 重合 | 关键身份差异（事实） | 角色 |
|---|---|---|---|
| MLLM Orchestration (2508.10016) | training-free 编排/omni 含 speech/黑盒/read-out;memory-routing-verification-stopping 模板 | **专家联邦非单核**;无候选池/无 selector/无 reward;自称仅 "training-free integration and control" | component-prior |
| ThinkOmni (2602.23306) | training-free/omni 含 audio | **logits 融合+外部 LRM(new-info)** 双重出界 | boundary-comparator |
| Limits & Gains (2512.11109) | BoN/SC/verifier/refinement 全谱实证 | VL-only 无 speech;confidence 变体用 logits | component-prior |
| MM TTS Survey (2606.08231/ACL 383) | TTS 形式化与 TFRL 同构;三范式骨架 | **明文不覆盖 audio**（范围边界事实,不单独构成空位证明） | navigation-only |
| Small-VLM TTS (2607.09438) | 供给/选择归因方法论 | 视觉 MCQ;log-prob+guided decoding;PRM trained（结果 null） | component-prior |
| On TTS for VLMs (2606.28864) | zero-shot 严格对齐 TF-Strict/单核/SC | 视觉;诊断层 attention/KV | component-prior |
| dMLLM-TTS (2512.19433) | **单核兼任生成与验证**;self-verification 作 reward | 文生图;yes-logit | component-prior |

组件级事实：七篇零篇同占「黑盒+单核+speech/omni+候选选择」四轴——**此四轴自 v4 更正版起
仅作组件级普查**,系统级判断见 §4.2。

### §4.2 系统级普查（known-item 8 项,system-control 13 轴全文 DFS,引文抽查 11/11）

13 轴 = 核心身份/访问级别/**全系统训练范围**/控制时域/**decision rights**/状态记忆/工具/
反馈奖励来源/候选生成与选择/停止预算/终态合成/信息边界/模态任务（amendment-9 §3;逐篇
逐轴记录 = `survey/2026-07-18-sf-known-item-dfs-systemcontrol.md`）。

| 工作 | 控制器形态 | 训练/标签轴 | 选择信号 | 停止/预算 | speech |
|---|---|---|---|---|---|
| ATLAS (2606.01667) | 自适应 agentic orchestrator（explore-or-stop） | 零训练、label-free | orchestrator 共识/直接合成 | **自适应停机**（88.9% 轨迹恰在收敛点停——**GPQA-Diamond 单基准,Fig 7a 有可定义正确多数收敛点的轨迹子集**,非跨基准总体比例） | 无 |
| AutoTTS (2605.08083) | 离线发现的代码 controller | 零权重更新,**发现用 gold 搜索集** | 答案共识 Agg | controller 自适应 width×depth | 无 |
| Agentic Coding (2604.16529) | **固定调度**(N=16,T=2) | 零训练、**选择显式不触 gold/测例** | LLM 比较投票（RTV 锦标赛,摘要为基质） | 固定预算 | 无 |
| Team of Thoughts (2602.16485) | orchestrator 选择性激活工具 agent | 零梯度,**校准/自审用 gold** | 画像匹配+聚合 | 选择性激活 | 无 |
| ToolGate (2606.03054) | 逐调用 execute/skip 门 | 核冻结,**控制器两变体皆 supervised-trained** | 无 K 池（二值门） | execute-skip 成本控制 | 无 |
| DeepVerifier (ACL 1243) | rubric 验证器+迭代反馈 | 主实验零训练;开源变体 SFT;验证 agent **检索 new-info** | 序贯精修非 K 池 | 验证器接受即停（3–4 轮见顶后回落） | 无 |
| Selective TTS (ACL 1724) | 分阶段剪枝流水线 | **全系统零训练**（9 路径中 2 条 strict-identity 之外最接近者——judger 选择用人类偏好 = dev-label 轴） | **llm_judge 分数对 K 池选优 = reward-guided**（taxonomy v1;其论文自框架 "guided by reward signals";人对齐选 judger τ=0.55） | **固定预算+剪枝重分配**（α=0.6 最优） | 无 |
| DREAM (ACL 511) | plan/exec 双相位树搜索 | 核冻结,**PRM 微调**（trained comparator） | **trained-PRM 引导 K 池** | 双阈值早停+补采 | 无 |

**系统级普查事实（对已检视集合;非文献全集结论;定性留待 mapping 与 owner;量词一律引用
identity taxonomy **v2** 的机器重算输出〔`docs/checks/2026-07-18-sf-identity-taxonomy-v2-test.json`,
**11 条 method path**——mixed/composed 路径分行:Agentic Coding 拆 RTV/PDR/pipeline 三行,
DeepVerifier 拆双行;taxonomy v2 = 正典投影版,v1 缩减 schema 已 dated supersession〕）**：
① **项目身份候选 = 0/11**〔机器推导:strict 位 ∧ 单核拓扑 ∧ 原生 audio/omni 进核——
unknown 不满足;此为 v1 被撤回量词句经正典投影后的合法重立〕;core_native_modality ∈ {audio,omni} = 0/11
（数据集含音频位与原生模态轴已分离——benchmark/ASR 级联不再可能混入方法占据）;
② **占据合取（按 selection_object 分层,不跨池聚合）**：strict-bits∧reward-guided∧K 池 =
**轨迹池 3/11**——且三条路径全部来自**同一篇** Agentic Coding（RTV/PDR/pipeline）;
工具-agent 池（Team-of-Thoughts,终态=合成）与输出池（Selective TTS）各有占据但不满足
strict 位（dev-label 轴）;trained-PRM∧K 池 = 1/11（DREAM,机器持久化断言）;
**待检验候选空位坐标 = strict 位 ∧ reward-guided ∧ K 池 ∧ 原生 audio/omni 单核——已检视
集合 0/11,待 Stage-1B mapping 检验**;③ 权重轴〔机器重算〕：all_components_weight_frozen =
8/11;data_access_strict_bits = 4/11——「冻结核心 ≠ 全系统数据/访问严格」由本表承载;
ToolGate 经 Round C 更正为 trained binary gate（非 RM/PRM,is_reward_guided=false）;
④ 五种互补停止/预算机制（自适应停机/双阈值/剪枝重分配/execute-skip/验证器早停）入
Stage-2A 组件候选池;⑤ 两条外部控制平面实证约束：「外部控制器优于模型自调节」（ToolGate:
prompt 自调节把精度降到 60.0 且反增工具量）与「stage 评估器与终 judger 失配则过剪退化」
（Selective TTS α=0.8）。构念防线 = 作者反例 + **独立语义反例区**（P1-4:非实现者代理自
官方全文供给 4 例,含联邦拓扑/benchmark 角色/trained-gate 三类,6/6 PASS）。

### §4.3 负结果先验（双向三栏;异质案例共同提示,非独立复制;各条限于该论文设置内）

**供给侧主导**：可解析性修复先于一切（+~6pp,「看似推理失败实为抽取失败」）;单链 token
预算≫链数（+3.7pp vs +0.15pp）;策略模型本身主导（+11.4pp）;指令遵循能力是供给生效前提;
over-compute 失焦（感知任务截断反升）。**选择侧边界**：trained PRM 与 training-free critic
均不敌多数投票（池准确率越高近平衡选择器净转负）;弱模型 self-refinement 退化;
self-verification 封顶于核心理解力（SVF<GPT-4o）;外部 verifier>内部 confidence;SC 适用
边界=各链独立犯错。

- **支持列**：MBR/majority 等 K 强制基线、headroom 归因纪律、供给条件量 H(c) 换供给必重测。
- **反证列**：「复杂 evaluator/selector 优于简单基线」的预期价值被三案例削弱;若我们的
  reward-guided control 在有头空池上仍不敌 majority,直接反证 RQ-CTRL。
- **单观察 kill 判据**：验证过头空且 rollout 误差独立性达标的池上,reward-guided 选择仍
  稳定 ≤ 等 K majority——即杀死「奖励引导承载增量」假设当前形态。
- **未决替代解释**：selector null 可能由 MCQ 短答案域/PRM 域失配/自评偏差解释;speech/omni
  生成域是否同构,待 Stage-2A 复现裁决。

（数字全部 SOURCE_REPORTED_TRACEABLE,页/表 locator = claim-evidence 矩阵 §3。）

### §4.4 发现机制实证教训

词汇漂移两例实证（DVD 59 查询零命中/ToolGate 65 查询零命中——均离线 matcher 复现非联网
执行）→ 方法占位轴 L14/L15 + drift 观察队列;引文交集校准（30 可解析 arXiv-ID×107 存量=
空交集,ARXIV_ID_SUBSET_INTERSECTION_EMPTY,hypothesis-grade）→ 发现层由冻结查询承载、
闭包只作退出层;0-hit 声称必须机器复现（评审 0-hit 表 2/7 复现不成立→评审撤回）——完成态
语言与 oracle 等强对双方适用。「看过但遗忘」两例（2512.11109/X3、ATLAS/07-03 归档）→
known-item carry-forward ledger 纪律（归档不是遗忘许可）。

### §4.5 种子景观现值

92 列名种子维持（最高优先威胁 = Omni-Decision 2607.11433);C4B/C4C 新增 13 哨兵 = 反例/
held-out 工程件;execution-early 队列（四篇 FULLY_TRAINING_FREE + MemoPilot 直接威胁样本）
维持 amendment-7 §4.3。

## §5 Stage-1B 执行计划（签署后即行;全程禁研究模型;产出只含知识证据）

0. **开局**：三张互不混分母的保证表（`survey/2026-07-18-sf-stage1b-opening-tables.md`——
   re-review P0-2）：表 A system/control method paths（已深读 8 项〔11 路径,coding-v3〕+
   Round E 10 项〔附录 A 第二表〕+ **6 项晋升**:2506.12928〔三重 provenance,含我方复现的
   3 条查询命中〕/IAD/LATS/TreeSearch/JitRL/Omni-Decision）;表 B **speech/omni 测量工具**
   （τ-Voice/FDB-v3/**EchoChain〔零命中+无种子→保证入口+drift 队列 full-duplex 轴〕**/
   From-Text-to-Voice/VoiceAgentBench/Audio2Tool/tau 族——MEASUREMENT_INSTRUMENT 角色,
   不入方法占据分母）;表 C evaluator/reward 负结果先验。先按 taxonomy v2 编码再入正常
   BFS/DFS 排序,不冒充 query recall 成果;每轮 known-item
   carry-forward ledger（旧 survey 近邻/当前命中/引文新增/零命中已知项四列账）。
1. **BFS**：65 查询 + 50 路由逐条执行,REC-0 落账,五计数机器导出,75-cap 溢出 splitter。
2. **DFS**：四判据触发,全文精读（D2 八轴 + 13 轴,validator 机器强制）;队列排序
   （威胁度↓,core>element,时新性↓,梯队平局）,2025+ 优先。
3. **退出**：E1∧E2∧E3 + 逐轮饱和表;E2 饱和前置 = 债务 D-1（work-level resolution）。
4. **产出**：system-level（13 轴）+ component-level 双层 occupancy → 负结果与冲突证据 →
   饱和轨迹 → exposure union 复核 → 3–5 候选问题卡（四行强制）→ **Stage-2A prior
   reproduction shortlist** → Stage-1C owner 选题。债务 D-1..D-5 带 owner 与截止 gate。

## §6 Stage-2A 预告（冻结草案,现无执行力）

复现最近邻先行（候选池至少含 ATLAS/AutoTTS 类系统控制、MLLM Orchestration 类免训编排、
majority/BoN/Selective-TTS 类强组件基线）→ 复现合同（版本钉定/容忍区间/退出条件）→ 配置化
工程合同 → 复现先于改进 → 证据隔离（exposure union 从验证集排除或显式降级）→ 资源纪律
（不设 cap 全记账）。全文 = amendment-9 §5。

## §7 声明与请求

**声明（逐条标模式）**：①协议包本地结构/计数/哈希/matcher/validator 可九条命令零联网重放
（MACHINE_REPLAYED_STRUCTURE——能力包络不含外部论文数字）;②外部研究数字 =
SOURCE_REPORTED_TRACEABLE（矩阵逐条 locator）;③「discovery query = 0、联网活动逐次入三本
台账、未执行未登记的查询/模型调用」= TEAM_ATTESTATION（签字承诺,不称机器证明）;④阶段四
字段见 frontmatter;⑤证据 directional-only 不升级;⑥创新点未锁定,本件零终局定性。

**请求**：①按 v4 复审 §7 验收清单复核整改批（回应信逐项对账）;②签署 **Stage-1B survey
execution**;③签署后 owner 执行批准,首条 systematic query 即 Stage-1B 起点。

—— 研究执行方（W1）,2026-07-18。更正走 dated correction。

## 附录 A：参考文献（本件自包含;arXiv 作者/日期取自仓内正典 raw Atom,ACL 作者取自 Anthology 官方页 citation 元数据）

**正文两级 DFS 集合 15 条（§4.1 七篇 + §4.2 八项）+ 机制/held-out 校准件 3 条（DVD/
Seg-Agent/Memory-Augmented VL Agents——角色 = CALIBRATION/HELD_OUT,非正文普查成员;
P1-2 更正:原「18 条已深读」算术表述拆分）**：

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
| Inference-Time Scaling of Verification（DeepVerifier, ACL Findings 2026） | Yuxuan Wan et al., 2026 | https://aclanthology.org/2026.findings-acl.1243/ |
| Scaling Unverifiable Rewards: A Case Study on Visual Insights（ACL Findings 2026） | Shuyu Gan et al., 2026 | https://aclanthology.org/2026.findings-acl.1724/ |
| A Reward-Guided Dual-Phase Framework for Adaptive Inference-Time Reasoning（DREAM, ACL Findings 2026） | Yingqian Cui et al., 2026 | https://aclanthology.org/2026.findings-acl.511/ |

**Stage-1B 首批 reviewer-known 队列（v5 复审 Round E 供给;登记待读,尚未深读;10 条）**：

| 引用 | 作者/年份 | 稳定链接 | 发现保证 |
|---|---|---|---|
| Agentic Test-Time Scaling for WebAgents（CATTS） | Nicholas Lee et al., 2026 | https://arxiv.org/abs/2602.12276 | 冻结查询 SF-L2-Q1（我方复现） |
| Benchmark Test-Time Scaling of General LLM Agents | Xiaochuan Li et al., 2026 | https://arxiv.org/abs/2602.18998 | SF-L2-Q1 + SF-L12-Q3 |
| PiCSAR: Probabilistic Confidence Selection And Ranking | Joshua Ong Jun Leang et al., 2025 | https://arxiv.org/abs/2508.21787 | SF-L5-Q1 |
| Sampling for Quality: Training-Free Reward-Guided SMC Decoding | Jelena Markovic-Voronov et al., 2026 | https://arxiv.org/abs/2604.16453 | SF-L2-Q4 + SF-L5-Q1 |
| Reward-Guided Decoding for Pre-trained Model Evaluation（EBD） | Shaobo Wang et al., 2026 | https://arxiv.org/abs/2605.28020 | SF-L2-Q4 + SF-L5-Q1 |
| BrowseConf: Confidence-Guided Test-Time Scaling for Web Agents | Litu Ou et al., 2026 | https://aclanthology.org/2026.findings-acl.21/ | T1-ACL-2026 路由 |
| Agentic Rubrics as Contextual Verifiers for SWE Agents | Mohit Raghavendra et al., 2026 | https://aclanthology.org/2026.acl-long.697/ | T1-ACL-2026 路由 |
| AgentV-RL: Scaling Reward Modeling with Agentic Verifier | Jiazheng Zhang et al., 2026 | https://aclanthology.org/2026.findings-acl.1156/ | T1-ACL-2026 路由 |
| Timely Machine: Awareness of Time Makes Test-Time Scaling Agentic | Yichuan Ma et al., 2026 | https://aclanthology.org/2026.acl-long.211/ | T1-ACL-2026 路由 |
| FS-Researcher: TTS for Long-Horizon Research with File-System Memory | Chiwei Zhu et al., 2026 | https://aclanthology.org/2026.acl-long.288/ | T1-ACL-2026 路由 |
