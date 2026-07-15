---
proposal_id: STAGE1A-PROPOSAL-2026-07-15-04
title: "System-first 研究提案 v3（合并全篇,致 reviewer 评审）—— 黑盒 omni agentic system × training-free RL"
date: 2026-07-15
nature: "应 owner 指令撰写的**完整独立成篇**研究提案：把分散于 v1（十一节骨架）/ v2（修订史式送审件）/ 检索协议（操作件）/ S0（身份页）的内容整合为一份可整体评审的科学文本。**meta-process 披露**：v2 外审曾下元流程停止令（续52 口径——「不要求 proposal v3/应停止元流程膨胀」）;owner 行使流程定夺权指令本件成篇——本件不改变任何已收敛结论,检索协议包仍是 Gate S1 的签署对象,本件是其科学上下文"
stage: "Stage-1A（问题定义,进行中）;申请事项 = ①本提案整体评审 ②Gate S1 检索协议包 search-design 签署（包件见 §13）"
identity_authority: "Gate S0 已签署（续48）：TF-Strict（全系统零训练）"
evidence_discipline: "零新执行;既有数字 directional-only/hypothesis-grade;先行工作状态按登记 token,占据结论以可回放 survey 为准;无确证宣称、无「首个」宣称"
generated_by: "Claude Fable 5 主会话协调者亲笔"
hostile_review: "R1 双镜头（①整合忠实度;②新叙事 claim-creep+术语,各 Opus 独立）：镜头1=0 MAJOR+4 MINOR（『预登记坍缩风险』token 误挂 Omni-Decision——该 token 系 IAD 独占,等于把外审迟发现的遗漏洗成团队前瞻,已改两类分述;training-free-grpo 待核状态被静默定案;『由 owner』归属脱落;停止令软化为『建议』）;镜头2=1 MAJOR（**C-T7 锚点失实**——其真实机制为检索供给侧泄漏而非训练泄漏,且 TF-Strict 不阻止该类,原文暗示了不存在的保护——已改为如实分述两道防线）+6 MINOR（四篇受训对象误一概而论/『窗口在收窄』预判占据/『显著』骑 in-house 数字/『四行 vs 三条』计数漂移/机制-报告纪律标签冲突/否定语境字面词——末项保留）。修复后 R2=8/8 FIXED+1 新残留（『预登记』越出 IAD 语境）→ NOT_CONVERGED;单词修复后机器 grep 核验=全文仅 IAD 行 1 处 → CONVERGED（判据纯机械,以 grep 为 R3;环内判定≠外部评审通过）"
owner_transmission: PENDING
---

# System-first 研究提案 v3（合并全篇）

## §0 导读：这份文件是什么、和已有件什么关系

给 reviewer：你已审过 v1（RETURN→重校准 ACCEPTABLE_TO_PROCEED）与 v2
（APPROVE_GATE_S1_PROTOCOL_DRAFTING_WITH_REQUIRED_AMENDMENTS）,你的修正案 A–F 与七条新种子
已全部并入检索协议包（三轮内审环收敛）。本件把**科学叙事补全成篇**——动机、问题树、方法论
的完整表述此前散落各件——供你对研究方案整体评审;操作层的签署对象仍是协议包六件套（§13）。
凡与 v1/v2/协议冲突处,以已收敛工件为准并视为本件笔误。

## §1 研究纲领与身份（S0 已签,正典效力现行）

**Primary program**：在严格黑盒、核心模型权重与内部架构不变的条件下,能否通过一个外部
reward-guided 控制平面（agentic system）,把冻结 omni foundation model 组织成能感知多模态
环境、维护状态、调用工具、利用反馈并选择下一步动作的系统,从而把预训练潜藏能力**激活到
尽可能高**。

S0 八行合同（签署 via 会话指令,授权原文续48,亲笔补签位保留）：primary_object = 黑盒 omni
agentic system;north_star_method = training-free reward-guided external control（reward/
advantage 决定下一步动作,池内选择是退化特例）;selector/evaluator = 组件;resource_posture =
全力摸高→持续整合→成本压降;black_box_contract = 严格黑盒（本地 llama.cpp =
GRAY_BOX_DIAGNOSTIC 永不承重）;**training_free_scope = TF-Strict（全系统零训练）**;
core_structure_policy = 核心冻结、外部结构显式版本化;innovation_status = **owner 选择的创新
假设**,占据核查完成前不宣称任何「首个」。

两条 owner 裁决约束全文：**身份层不立法指标**（具体指标绑定任务×数据集,各研究协议定义、
Stage-2 冻结;度量纪律以硬约束存在——headroom 归因、cellwise、四量并列）;**摸高阶段预算
不设 cap**（照实记录;等预算类判据 = PHASE-3_TOOL,归因对照用结构匹配而非预算归一）。

## §2 科学背景与动机（为什么是这个问题）

**起点观察（两层命题,证据等级分立——v3 外审 §2.2-E 拆分）**：

- **已有支持的「输出池」命题**：在特定任务、供给 c 与采样设置下,冻结模型的**输出池**存在
  大幅 oracle 头空。文献锚（附支持边界）：Large Language Monkeys（arXiv 2407.21787——支持
  coverage 随采样数对数线性增长;**不支持** agentic 轨迹控制结论）;compute-optimal TTS
  （Snell,arXiv 2408.03314——支持测试时算力分配→输出池收益;同样不支持轨迹级结论）;
  audio TTC（scaling-auditory,arXiv 2503.23395——支持音频域输出级 TTC 存在收益;证据级 =
  census 在库题录+）。自家组件线 directional 数字（hypothesis-grade,census/ledger v2 在案）
  仅作方向性佐证,不作量级依据。
- **待调查的「系统/轨迹」假设**：在有状态、工具交互、跨模态的 agent **轨迹**中,是否存在
  可由零训练控制平面稳定兑现的 trajectory headroom——**此命题不由前者自动推出**,系本
  survey 与未来 1B 探针的调查对象;每次书写 headroom 均带供给 c、任务、采样与 oracle 信息
  边界限定。

北极星问题据此表述：不改一个权重,外部系统能把潜藏能力兑现到多高——其中「轨迹级潜藏能力的
存在性」本身即待查项之一。

**为什么是「系统」而不是「选择器」**：本项目曾把研究对象收缩为固定 K 池 label-free selector
的兑现面（可测性压力下的目标置换,已由 owner 澄清纠偏并墓碑退役）。组件线的诚实结论是：
终态选择只触及兑现问题的一角——供给 c 的构造、反馈是否改变下一步动作、状态与工具的组织,
才是天花板的主要杠杆候选（此为**假设**,survey+探针裁决）。

**为什么黑盒**：跨模型/API 可迁移性与部署现实;同时把「读内部信号」类捷径（logit/hidden
state——JitRL〔2601.18510〕式「方法最近、接口不合」边界）排除出承重路径,使结论对闭源前沿
模型同样有意义。
本地部署保留为低成本校验环节。

**为什么 TF-Strict（全系统零训练）**：①与北极星同构——问「预训练已有什么」而非「再学一点
能到哪」;②信息边界纪律的延伸——任何在任务数据上训练的外部组件都会扩大泄漏面、使
read-out/new-info 判别更难审计（本项目对边界的警觉源自 C-T7 教训：**检索供给侧泄漏**,KB 含
gold 致 +0.517 判 INVALID——如实注明:该类泄漏 TF-Strict 本身**不**阻止,由信息边界守卫独立
拦截,两道防线各司其职）;③文献边界清晰——冻结核心+训练外设自成一类作 TRAINED_COMPARATOR
上界对照（IRO 训 value function / VeGAS 训 verifier / AuTAgent 训 tool policy,三者已坐实;
training-free-grpo 学 token prior,**TF-Strict 归属待核**——60 种子中 2 条 scope_pending
之一,另一条 = UCT-ToolCreator 2602.01983〔批次1〕）。
**代价如实登记**：若
label-free 冻结信号普遍太弱（Self-Verification Limitations,arXiv 2402.08115——支持「无
sound verifier 时自验证不可靠」;**不支持**「一切 label-free 信号必然失败」）,TF-Strict
headline 将承压——出口在
合同里（转 TF-Core 须 owner 新签+改名）,这是本提案**登记在案的首要风险**。

**为什么现在**：2025–2026 的 agent/test-time-control 文献爆发（IAD 的 sampling–evaluation–
feedback 三分、Omni-Decision 的 evidence-state 闭环、audio agent 系）**可能**压缩系统创新的
剩余空间——剩余空间到底还有多少,必须用可回放 survey 尽快标定（占据结论以 survey 为准,
不在 survey 前预判）,这正是本阶段唯一申请执行的事。

## §3 研究问题树（全部为待证伪假设,Stage-1C 由 owner 双证据选题）

- **RQ-SYS（主）**：严格黑盒+全系统零训练下,外部 reward-guided sequential control 能否把
  冻结 omni 组织成真实多模态感知/工具行动/状态维护/反馈适应的 agentic system,并把任务效用
  推到**实质性且可复核地**高于 one-shot 与终态选择的天花板?（统计语义 Stage-2 才冻结）
- **RQ-CTRL**：增量是否归因于 reward/advantage→下一步动作（对反馈阻断/随机化与无奖励搜索的
  结构匹配对照）,而非单纯更多采样/更多调用?
- **RQ-OMNI**：非文本模态是否因果地改变评估、计划与工具选择（模态移除/置换探针）,还是系统
  实质为文本 agent + 音频工具（AudioToolAgent 邻域,须降名）?
- **RQ-SAFE**：反馈闭环下的 reward hacking/错误累积/过优化拐点何时出现,悲观评价/弃权/停止
  能否控制（Goodhart 线锚 = inference-time-reward-hacking,arXiv 2506.19248——其提出的
  HedgeTune 即停止机制候选）?
- **RQ-MEASURE**：哪些 label-free observables 预测头空、轨迹改进与失败 regime（组件线四量
  记账在终态选择子问题继续可用,不上升为身份）?
- survey 收官时以上收敛为 **3–5 个 system-level candidate problems**（每个带:已占据部分/
  未解决 failure/可行原型方向/最强反对证据/尚缺信息）,供 Stage-1C。

## §4 五份系统级合同（PROVISIONAL_STAGE1A_TAXONOMY——检索与编码用,survey 证据可修订）

（全文 = v1 §2,五合同不设短代号;此处收录判据行）

- **黑盒合同**：允许接口 `generate(multimodal_context, tool_schema, sampling_controls)`;禁止
  承重依赖 weights/gradients/hidden states/attention/保证 logprobs;组件四态标注。
  kill-black-box：关内部信号后核心增量消失 ⇒ 降 API-accessible gray-box。
- **training-free 合同（TF-Strict 已签）**：全部外部组件零可训练参数;适应仅经上下文/外部
  状态/搜索/非参数统计;TRAINED_COMPARATOR 永不承重。kill-training-free：任何承重增量依赖
  为任务训练的新参数。
- **RL 控制合同**：state/action/feedback/transition/controller 五元组;reward 只排终态 =
  reranking 不得称 RL。kill-RL：reward 不影响 next action。**命名纪律（v3 外审 §2.2-F）**：
  「reward 影响下一动作」仍可能是 search/planning/metareasoning/bandit——对外中性术语 =
  **reward-guided inference-time sequential control**（与 S0 north_star_method 同义）;「RL」
  为 owner 北极星与内部待证身份,保留与否由 foundational lineage lane（协议 SF-L9）的谱系
  比较裁决,survey 抽取字段含:状态/动作/反馈/策略表示/跨步更新对象/信用分配/停止规则/
  作者是否自称 RL。
- **agentic 合同**：≥2 步因果反馈链/持久外部状态/真实工具或观察获取/budget·stopping·
  abstention/轨迹 provenance/与固定池终态选择结构匹配可区分。kill-agentic：可等价重写为
  「生成 K 候选取 argmax」。
- **omni 合同**：模型能力≠agent 观察≠工具模态≠行动模态≠因果接地,五轴分离;核心要求 =
  冻结 omni 核心自身在环接触原始/表征级多模态观察。kill-omni：移除非文本模态后计划与效用
  不变。
- **术语降级规则**：任一合同 kill ⇒ headline 删该词并降名,不得用其余四词替代;七句禁句
  （v2 评审 §11）为机器可查项。
- **信息来源六类分解（v3 外审 §2.2-G,登记于 survey/README;系既有 read-out/new-info 二分的
  直系升级）**：①task-native observation ②pretrained-knowledge read-out ③deterministic
  transformation/computation ④endogenous environment feedback（agent 动作引致）
  ⑤exogenous answer-bearing retrieval / new information ⑥evaluation gold（**严格禁入决策
  路径**）。未来每个候选机制须标注所用类别;**由⑤带来的增益不得概括为「激活预训练知识」**。

## §5 系统架构与形式对象

外部控制平面（观察/供给构造 → 状态+外部记忆 → 工具/检索注册表 → 候选生成 → 评估/验证/
奖励估计 → 选择/controller → 预算+风险+停止/弃权 → 溯源+信息边界守卫）⇄ 仅经冻结接口的
黑盒 omni 核心 ↺ 环境反馈。固定 K 池终态选择 = 单步/无工具/无状态特例,组件线全部结果按此
嵌入。预算四轴 {model_calls, tool_calls, tokens, latency} 照实记录不设 cap。Stage-1A 全部
对象仅纸面/schema/mock（StageGuard: stage1a 连真实 backend 即 fail）。

## §6 相关工作与种子景观（snapshot 2026-07-15;占据结论以 survey 为准）

**60 条列名种子（快照 51 + amendment-1 增量批次1 九条;manifest 枚举正典）**（快照五来源:
近邻表 15/评审机制族 10/自库反扫 4/反扫 STRONG
15/评审 delta 7）+ 22 条执行时裁决 + 9 桶 WEAK。**计划**对 threat 首轮队列（15 篇,
可增长非硬上限——协议 amendment-1 重排后口径）执行双人独立全文抽取,最高优先 =
**Omni-Decision (2607.11433)**：training-free omni evidence-state 闭环,逐项命中
本纲领大半表达,其未必占据的是「reward/advantage 决定下一步动作」——**本 survey 第一个要
回答的问题就是它到底占了多少**（威胁优先级第一位——系 v2 外审迟发现的最严重遗漏;IAD
2504.01931 为**立项即登记**的「预登记坍缩风险」,优先级第二——两者 token 谱系不同,如实分述）。

**候选 delta（机制 = ①②,报告纪律 = ③;全部为假设——邻居表相关四行〔Reflexion/LATS/
Voyager/LLM-as-Verifier〕已标 TO_VERIFY_FULLTEXT）**：①冻结黑盒 omni 核心自身在环
接触原始多模态观察（vs 中央文本体编排工具——MM-ReAct/AudioToolAgent/Agent-Omni 线）;
②TF-Strict 全系统零训练的 reward-guided 序列控制（vs Reflexion/LATS/Voyager 的黑盒零训练
——delta 只能落在 omni 接地与兑现记账,不得以「未用我方术语」造差）;③以「相对冻结核心自身
天花板的兑现」为报告纪律的系统研究（文献多报绝对分——此为报告纪律差异,非机制差异,如实
定位）。**自警**：不以合取缺席论证新颖性;bare-I2 机制已被 scaling-auditory 同核 beam
log-lik 占据在案。

## §7 方法论：Stage-1A 可回放 survey（当前唯一申请执行的工作）

签署对象 = 协议包六件套（`wiki/survey/2026-07-15-system-first-survey-protocol-v1.md` 及
manifest/模板/报告/签署区,三轮内审环 CONVERGED）。规格要点：八 lanes + foundational lineage lane（SF-L9,无 2022 窗限）/ 48 条 arXiv 查询已
**离线编译冻结**为 `2026-07-15-sf-queries.jsonl`（逐行含 URL 编码/分页字段/行哈希）。
**可回放承诺分层（v3 外审 §7.2-II 更正,撤回「逐字节一致」表述）**：请求定义可复现（编译
冻结）+ 原始响应留存 + 派生集合可由原始响应重建;接口侧实时漂移作为外部不确定性记录。
+ 16 条副源路由（route manifest 逐条冻结或如实标 discovery-only）（ACL/OpenReview/IEEE/ACM + CVF/ISCA/PMLR 回链义务）;60 种子
snowballing 至连续两轮零新增 DIRECT;§5bis 时新性增量扫描;十轴纳排 + TF 审计六字段 + 范围
八轴 + 11 开放抽取字段;NO_DIRECT_MATCH 须预注册饱和+双评审;全量日志/排除理由/失败请求入
L3 replay;taxonomy 修订版本化。执行前置三条件：reviewer search-design 签署 + owner 批准 +
P0-R8 状态门复跑;**签署前零查询（attestation 双处 = 0）**。

## §8 基线与归因对照（摸高框架）

候选五臂：one-shot / 等 K BoN·MBR（组件线冻结基线）/ 反馈阻断-随机化 workflow / 无奖励
启发式搜索 / reward-guided controller。**用途二分**：主问题 = 臂 5 的天花板高度（预算照实
记录不设 cap）;归因诊断 = 臂 3/4 与臂 5 的结构匹配对照（RL/agentic 合同的证伪工具）;
等预算效率比较 = PHASE-3_TOOL 延后。当前不冻结实验设计、不裁决先跑哪臂（Stage-1B 探针协议
届时另行预注册+owner 签批）。

## §9 系统级 candidate_kill_logic_for_stage1b_design

八行候选 kill 逻辑（反馈因果消融/模态移除/奖励移除随机化/外部状态移除/黑盒接口能力移除/
工具必要性/停止弃权恢复/头空前置检查）——现阶段身份 = 告诉 survey 找哪些替代解释 + 1B 探针
设计候选;任何 kill 触发按 §4 降级规则处置,不自动否定其余谓词。

## §10 工程基座计划（并行不承重）

现状如实：Hydra stub + 定制脚本,**不称**配置化基座。Stage-1A 只做：一页 runner/config ADR +
开源 harness 复用比较矩阵（黑盒 API 支持/统一多模态消息/工具生命周期/状态持久/可插拔
controller/trace 回放/许可证等十轴）+ 旧 GRPO 训练型配置隔离（防与 TF-Strict 身份冲突）+
可选 mock/schema 验证。不接真实 backend、不读数据、不以代码量计进度;真实 adapter 留给另行
授权的 Stage-1B。

## §11 诚信、暴露与零执行

本提案周期新执行 = 零。历史暴露 = INHERITED_PRIOR_EXPOSURE 如实继承（574 工件等,registry
在案）;1B item manifest 先扣 exposure union;既有 MATERIAL QRP 更正义务照常履行,不因任何
新裁决冲销。记录纪律：append-only 审计层+哈希正典 git blob;审计字段先 PENDING 实测后更新;
承重计数只出自机器重数（本周期五例计数教训全部登记于 docs/checks 归档与 Decision-Log）。

## §12 Stage-1B 蓝图（PRE_STAGE2_BLUEPRINT——无现时效力,每步 owner 签批）

B0 接口冒烟 → B1 agenticity 因果探针（败即撤 agentic 称谓）→ B2 omni 接地（败降文本 agent）
→ B3 reward-control vs 启发式搜索（败降通用 scaffold）→ B4 safety/Goodhart → B5 测量。
已签四探针映射推荐案：P-α 头空 → 各格前置检查;P-β MBR → 基线臂;P-γ 同核 logprob → 仅
GRAY_BOX_DIAGNOSTIC 本地校验臂;P-δ 供给对比 → B2/供给轴——**探针序对齐仍待 owner 裁决**。
全部 directional-only、单次触碰、尝试全登记;C1/C4 于 1B-0 **由 owner** 终验。

## §13 门与时间线

S0 已签 → 本提案评审 + **协议包 search-design 签署**（六件套:协议+amendment-1/manifest 60/
模板 T1–T6/报告/检索串与 schema/签署区）→ 三条件 preflight → survey 执行（threat 首轮 15 篇
优先、非硬上限,Omni-
Decision 第一）→ §5bis 增量扫描 → 综合 = 3–5 候选问题 → Stage-1A close（独立签字）→ 1B
放行（再一签字）→ 探针 → Stage-1C owner 双证据选题 → Stage-2 预注册。

## §14 对 reviewer 的请求

1. 对本提案整体评审（科学动机 §2、问题树 §3、候选 delta §6 的表述纪律尤请压力测试）;
2. 协议包 search-design 签署（或开列修订项——协议签署区在协议 §12）;
3. 如认为本合并成篇与你「停止元流程」建议冲突,请直接向 owner 提出——本件系 owner 流程
   定夺权下的指令产物,已如实披露于 frontmatter。

---

## 修订记录（errata,v3 外审 P0-A 整改——2026-07-15）

按 v3 外审（`...-v3-stage1a-doctoral-review.md`,v3=有条件接受须澄清）逐项执行,原字节在
git 历史：①§2 起点观察拆为「输出池命题（有据,附三个文献锚与支持边界）/系统轨迹假设（待查,
不由前者推出）」两层;②§4 RL 控制合同加命名纪律（对外中性术语=reward-guided inference-time
sequential control,RL 名称由 SF-L9 谱系裁决）;③§4 新增信息来源六类分解（⑤类增益不得概括为
激活预训练知识,登记于 survey/README）;④RQ-SYS「显著」→「实质性且可复核地」（统计语义
Stage-2 冻结）;⑤§6 threat 抽取改计划时态并按 amendment-1 更新为首轮 15 篇非硬上限;
⑥§7 撤回「逐字节一致」,改分层承诺并指向编译冻结件;⑦§2 Stechly 锚补全（arXiv 2402.08115,
附支持/不支持边界）。配套:检索协议 amendment-1（八项变更）、seed manifest 增量批次1（+9=60）、
v3 内审报告补归档（含迟归档如实说明）、bundle manifest（提交后钉哈希）。
