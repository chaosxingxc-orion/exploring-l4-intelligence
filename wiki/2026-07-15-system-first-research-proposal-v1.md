---
proposal_id: STAGE1A-PROPOSAL-2026-07-15-02
title: "System-first Stage-1A 研究提案 v1 —— 黑盒 omni agentic system × training-free RL"
date: 2026-07-15
stage: "Stage-1A（问题定义）；本件 = system-first 问题定义提案（v2 博导评审 §11 强制次序）；未来计划部分适用 PRE_STAGE2_BLUEPRINT 纪律（结构草图,无现时效力）"
supersedes: "STAGE1A-PROPOSAL-2026-07-15-01（selector-first）作为主提案的地位——该件降级为组件 dossier / SURVEY-B 素材,其内容效力不变（v2 评审 P0-SYS-1 处置）"
identity_authority: "Gate S0 已签署（续48,via 会话指令）：primary_object=黑盒 omni agentic system;north_star_method=training-free reward-guided external control;training_free_scope=TF-Strict（全系统零训练）"
evidence_discipline: "全部既有数字 directional-only / hypothesis-grade;否定性结论按身份索引+强制伴随 token;先行工作占据状态一律 AS_CITED_BY_REVIEW / RETAINED_RECORDS@census-v2 / ROUND2_PREREGISTERED_TARGET（token 登记于 wiki/survey/README.md）,待可回放 system-first survey 核验;无任何确证宣称、无任何「首个」宣称"
generated_by: "Claude Fable 5 主会话协调者亲笔（签署级工件不委托）"
hostile_review: "R1 三镜头（授权合规/事实指针/术语纪律,各 Opus 独立并行）：镜头A=0 MAJOR+2 MINOR（agentic 合同缺 v2 §3.4 第六条件;P0-SYS-2 处置未披露）,十一节次序/七禁句/首个宣称全过;镜头B=1 MAJOR（CoVer 误标 census token——paper_works.jsonl 实测 grep 0 命中,实为 round-2 零执行预注册目标,与提案自身零执行口径自相矛盾）,数字/commit 锚/十条 arXiv 编号/owner 裁决转述全过;镜头C=2 MAJOR（同 CoVer 且与 RESP-02 §3.3 集外声明矛盾;自造 C-BB…C-OM 五码未登记+「C」命名空间第三次同形）+3 MINOR。合并=2 独立 MAJOR+5 MINOR;协调者逐项亲验后全部修复（五合同弃短代号改描述名/CoVer 改 ROUND2_PREREGISTERED_TARGET/补 agentic 第六条件/补 P0-SYS-2 披露/token 复数对齐并登记 L3 库入口/census 计数带溯源/Proposal E 限定语）;R2 独立复检=7/7 FIXED+零新发现 → CONVERGED（**环内判定**=一轮零新发现,不等于外部评审通过——重校准评审 §6 措辞建议已采）。原始镜头报告归档 docs/checks/2026-07-15-proposal-v1-hostile-review-lenses.md。过程教训：草稿曾预写虚构审计块,提交前自纠,新硬规=审计字段先 PENDING 实测后更新（续49）"
external_review: "同日两轮：严评（RETURN_FOR_MAJOR_REVISION,六承重缺陷）→ 重校准评审（ACCEPTABLE_TO_PROCEED_WITH_STAGE1A_SURVEY_PROTOCOLIZATION——撤回预算 cap 前置/RL 二选一前置/轨迹 headroom 冻结/选择性遗漏 QRP 红旗/完整工程平台要求,判其为阶段错位;Gate S1=PROTOCOLIZATION_AUTHORIZED / QUERY_EXECUTION_STILL_PENDING）。严评**仍成立**四项已按勘误批次修复：①Reflexion/LATS/Voyager/LLM-as-Verifier 四行 delta 过度乐观→改写并标 TO_VERIFY_FULLTEXT;②P0-LIT-1 自库强近邻遗漏→5 条自 census v2 检回补入 §4（L3 检索失效实例,新规:写表先查自库）;③CONVERGED 加环内限定;④内审原始工件归档。协议质量标准采严评 P0-LIT-3 八项最低规格"
owner_transmission: PENDING — owner 审阅后转交 reviewer
---

# System-first Stage-1A 研究提案 v1

> **给 reviewer 的一句话**：这是按你 v2 审查 §11 十一节强制次序重写的 system-first 问题定义
> 提案。身份已由 owner 签署（S0）；五份系统级合同给出可证伪骨架；先行工作占据状态全部如实
> 标注「未经可回放核查」；不主张任何已证创新。对 reviewer 的请求集中在 §11。

## §1 Owner-signed program identity（已签署）

Gate S0（`2026-07-15-s0-program-identity-signoff.md`，SIGNED 2026-07-15 via 会话指令，授权
原文存 Decision-Log 续48）：

```text
primary_object        = 面向冻结黑盒 omni foundation model 的外部 reward-guided agentic system
                        （外部控制平面：观察/供给构造 · 状态与外部记忆 · 工具/检索 · 候选生成 ·
                          评估 · 选择 · 预算/风险/停止 · 溯源与信息边界守卫）
north_star_method     = training-free reward-guided external control——reward/advantage 决定
                        下一步动作；固定池内选择是其退化特例
selector / evaluator  = supporting components（既有工件降级为组件 dossier,效力不变）
resource_posture      = 全力摸高（预算不设 cap、照实记录）→ 持续整合 → 成本压降
training_free_scope   = TF-Strict（全系统零训练）
black_box_contract    = 严格黑盒 headline；本地 llama.cpp = GRAY_BOX_DIAGNOSTIC,永不承重
core_structure_policy = 核心权重/内部架构冻结；外部系统结构显式设计并版本化
innovation_status     = 系统级创新 = owner 选择的创新假设；占据核查完成前不宣称任何「首个」
```

两条 owner 追加裁决约束全文：①**身份层不立法指标**——具体指标绑定任务×数据集，在各研究协议
中定义、Stage-2 预注册冻结（度量纪律以硬约束存在：headroom 归因、cellwise、四量并列，见热层
§3）；②**三阶段资源姿态**——本提案处于「全力摸高」阶段：主问题是天花板高度，不是等预算效率
（等预算类判据 = `PHASE-3_TOOL`，见 §5 的归因/效率二分）。

## §2 五份系统级合同与术语降级规则

组件层合同（六份身份合同 + same-selector contract，FROZEN@dce5c79 + 修正案 №1 @0a5e108）
继续有效，不在此重开。以下五份**系统级**合同为 v1 骨架（正/反例充实与冻结 = Gate S2）。
**五合同不设短代号**（收词纪律：避免与诚信核查 C1–C5、论文贡献 C1–C3 的「C」命名空间第三次
同形撞名），一律以描述名引用：

### 黑盒合同（black-box contract）
- **允许接口**：`generate(multimodal_context, tool_schema, sampling_controls) → text |
  structured_message | tool_call | multimodal_output`。
- **禁止承重依赖**：weights / gradients / hidden states / attention / 保证可得的 logprobs /
  修改 tokenizer/adapter/内部结构。本地 llama.cpp 的 logprob/白盒信号 = `GRAY_BOX_DIAGNOSTIC`
  （低成本校验，只解释本地实现，不支持跨闭源 API 的系统 claim）。
- **组件标注**：每个组件标 `BLACK_BOX_CORE | API_OPTIONAL | GRAY_BOX_DIAGNOSTIC | OUT_OF_SCOPE`。
- **kill-black-box**：关闭内部信号后核心增量消失 ⇒ headline 降为 API-accessible gray-box。

### training-free 合同（TF-Strict 已签）
- 核心模型与全部外部组件（evaluator/controller/router/memory 写入规则）**零可训练参数**；
  适应只经上下文、外部状态/记忆、搜索树、工具轨迹、非参数统计。
- 带训练组件的对照实验允许存在，但**永不承重**且显式标注 `TRAINED_COMPARATOR`；转向 TF-Core
  须 owner 新签署并改名 frozen-core agent optimization。
- **kill-training-free**：任何承重增量依赖为当前任务训练的新参数/LoRA/policy/reward
  model/verifier。

### RL 控制合同（reward-guided sequential control）
- 最小对象组：`state s_t`（观察史/记忆/检索证据/工具态/候选/奖励史/剩余预算）、
  `action a_t ∈ {observe, prompt, retrieve, call_tool, sample, evaluate, select, revise,
  abstain, stop}`、`feedback r_t`（可观察执行结果/验证信号/一致性/环境反馈——**不含 gold**）、
  `transition s_{t+1}=F(s_t,a_t,obs,r_t)`、`controller a_t=π_ext(s_t, reward 史, budget)`。
- **判别底线**：reward 若只对终态 K 个答案排序、不改变任何下一步动作 ⇒ 只是 reward-model
  reranking，不得称 RL/agentic control。「为什么是 RL 而非 inference-time search」由 §5 的
  归因对照与 §6 的因果消融回答，不靠术语声明。
- **kill-RL**：reward 不影响 next action；或反馈阻断/随机化后行为与效用无差异。

### agentic 合同
- 最低成立条件：≥2 时间步且第一步结果因果改变第二步动作；持久外部状态；至少一类真实
  工具调用/检索/记忆操作/显式观察获取；有 budget、stopping、abstention 或 failure recovery；
  对**轨迹**（非仅终态）定义 provenance；与固定池终态选择在**结构匹配对照**下可区分
  （v2 §3.4 第六项原文为「等预算下与 one-shot selector 可区分」——可区分性判据保留，
  等预算效率轴按 owner 裁决归 PHASE-3_TOOL，见 §5）。
- **kill-agentic**：系统可等价重写为「生成 K 候选后取 argmax」，或工具序列先验固定、反馈
  不改路径。

### omni 合同
- 五轴分离登记：model modality capability ≠ agent observation ≠ tool modality ≠ action
  modality ≠ causal grounding。核心要求：**冻结 omni 核心本身在环内接触原始/表征级多模态
  观察**——若全部音频先被转写为文本、中央控制只见文本，则最多是 audio-tool orchestration
  （AudioToolAgent 邻域），必须降名。
- **kill-omni**：移除/置换非文本模态后计划、工具选择与效用无变化。

**术语降级规则**：headline 中的每个词（black-box / training-free / RL / omni / agentic）与
其合同一一对应；任一合同 kill 触发即从 headline 删除该词并按上表降名——**不得用其余四词的
成立替代**。禁句清单（v2 §11 全部七句）作为敌意内审环的机器可查项。

## §3 系统架构与形式对象

```text
多模态环境/观测 → 外部控制平面（观察/供给构造 → 状态+外部记忆 → 工具/检索注册表 →
候选动作/轨迹生成 → 评估/验证/奖励估计 → 选择规则/controller → 预算+风险+停止/弃权 →
溯源+信息边界守卫）⇄（仅经冻结接口）黑盒 omni 核心 Mθ → 外部动作/工具执行/新观测/反馈 ↺
```

- **退化特例**：固定 K 池 + 终态选择 = 本系统在「单步、无工具、无状态」设定下的特例——
  selector 线全部已有结果按此嵌入（作为该特例格的组件证据，见 §7）。
- **预算对象**：`{model_calls, tool_calls, tokens, latency}` 四轴照实记录（摸高阶段不设 cap；
  cap 机制设计保留为 §8 schema 字段，供 ②③阶段启用）。
- **Stage-1A 边界**：本节全部对象仅纸面/schema/mock——`stage=stage1a` 连接真实 backend、
  数据路径或 API 即 fail（StageGuard，§8）。

## §4 系统级最近邻与机制 delta（PRELIMINARY——待可回放 survey 核验）

> 状态口径（token 登记于 `wiki/survey/README.md`〔L3 库入口〕）：`AS_CITED_BY_REVIEW` = v2 评审
> 点名、我方未做可回放核查；`RETAINED_RECORDS@census-v2` = 已在 census v2（94 记录簇→95 works，
> @28ad858）保留记录内；`ROUND2_PREREGISTERED_TARGET` = round-2 预注册待查目标（零执行，
> 题录级 AS_GIVEN_BY_REVIEW）。**本表不构成占据结论**；结论以 Gate S1 survey 为准。

| 先行工作 | 占据什么 | 候选机制 delta（假设,待核查） | 状态 |
|---|---|---|---|
| ReAct (2210.03629) | 推理×行动交织,反馈→下一步 | 文本域;delta 只能落在 native omni 在环与系统化控制,非「有无 agent loop」 | AS_CITED_BY_REVIEW |
| Reflexion (2303.11366) | 语言反馈+情节记忆迭代改进——原文明确**不更新权重**、可由黑盒 API 实现 | delta 候选仅剩 omni 感知环+兑现记账;**不得以「未声明严格黑盒」造差**（严评 §2.2 更正,TO_VERIFY_FULLTEXT） | AS_CITED_BY_REVIEW |
| LATS (2310.04406) | gradient-free MCTS + LM value/self-reflection + 环境反馈——与外部 reward-guided controller **高度相邻** | delta 候选仅剩 omni 接地与黑盒接口约束（严评 §2.2 更正,TO_VERIFY_FULLTEXT） | AS_CITED_BY_REVIEW |
| IAD (2504.01931) | agentic test-time 的 sampling–evaluation–feedback 三分 | **UMBRELLA 预登记坍缩风险**（立项即登记）——最直接的框架级占据者,必查 | RETAINED_RECORDS@census-v2 |
| MM-ReAct (2303.11381) | 中央 LLM 编排视觉专家 | 中央体纯文本;omni 核心不在环 | AS_CITED_BY_REVIEW |
| ViperGPT (2303.08128) | 代码生成+模块执行的视觉推理 | 同上;无 reward-guided 序列控制 | AS_CITED_BY_REVIEW |
| Voyager (2305.16291) | GPT-4 **黑盒调用、零微调**、环境反馈+自验证+技能库——直接占据 black-box+无权重更新+持久外部技能 | delta 候选=omni 感知与语音任务格（严评 §2.2 更正,TO_VERIFY_FULLTEXT） | AS_CITED_BY_REVIEW |
| AudioToolAgent (2510.02995) | 中央 LLM 编排 audio-language tools | **音频 agentic 组合空间的直接占据者**;delta 候选=omni 核心自身在环接触音频（非工具转述）——若不成立即降名（omni 合同 kill 即坍缩到其邻域） | AS_CITED_BY_REVIEW |
| LLM-as-Verifier (2607.05391) | 免训练通用验证+agentic feedback（含 task-progress proxy/dense feedback 用法） | evaluator 组件层先行;「不占系统身份」**待全文核验**（严评:该判断过早,TO_VERIFY_FULLTEXT） | AS_CITED_BY_REVIEW |
| CoVer (2602.12281) | test-time verification 作用于指令+动作（**训练型** verifier→TRAINED_COMPARATOR 边界对照,不承重 TF-Strict） | 已预注册为对 Proposal E（survey-v2 §8 A–E 提案集之 E,活代号——勿与知识栈评审死「方案 A」族混同）的最近邻威胁;系统层重查 | ROUND2_PREREGISTERED_TARGET |
| **JitRL (2601.18510)** | 非参数经验记忆估计 advantage、调制 action logits——**training-free RL 最直接机制近邻** | 需 logit access,不满足严格黑盒→「方法最近、接口不合」的主边界论文 | RETAINED_RECORDS@census-v2 |
| **Audio-Mind (2605.28480)** | 冻结 omni 前端 + planner-guided 有界工具使用/重听 | 直接压力测试 frozen-omni agentic system 与长链退化（ledger 有 full-text locator） | RETAINED_RECORDS@census-v2 |
| **Agent-Omni (2511.02834)** | 不重训协调 text/image/audio/video 专家 | system-level omni orchestration 直接竞争者;delta 候选=omni 核心自身在环 vs 专家路由 | RETAINED_RECORDS@census-v2 |
| **EChO-Agent (2606.15141)** | 冻结 Qwen3-Omni 的 Tool→Evidence→Reason→Verify 音频推理工作流 | **native audio/omni agent 直接近邻**;delta 候选=reward→下一步动作的控制回路 | RETAINED_RECORDS@census-v2 |
| **AuTAgent (2602.13685)** | 训练 tool policy 决定「何时调用哪个音频工具」并报告 tool-selection 上界 | TRAINED_COMPARATOR 边界对照,不承重 TF-Strict | RETAINED_RECORDS@census-v2 |

**表末五行的登记说明（勘误性补入）**：JitRL/Audio-Mind/Agent-Omni/EChO-Agent/AuTAgent 五条系
外审 v1 严评 P0-LIT-1 指出后自我方 census v2 **检回**（grep 实证五条均在库）——首版遗漏即 L3
探索知识「检索失效」的当日实例（新规：**写任何最近邻/占据表前必须先查自库**）。协议 mandatory
seeds 另含评审补充、待题录解析的：AWM (2409.07429) / ExpeL (2308.10144)（外部记忆/经验学习占据）、
Self-Refine / CRITIC / TPO（黑盒反馈修订族）、HuggingGPT / AudioGPT（复合系统编排族）、
DSPy / TextGrad（compound-system optimization 族）、TTRL (2504.16084)（test-time **权重更新**
边界对照,归 OUT_OF_SCOPE_WEIGHT_UPDATED）。

**候选 delta 的诚实陈述**：以上第三列全部是**待证伪假设**。特别声明两条自警：①不以「无单篇
同时含全部组件」式合取缺席论证新颖性（禁句 §2）；②bare-I2 机制已被 scaling-auditory
（2503.23395）同核 beam log-lik 占据（DIRECT_OCCUPIED_AT_MECHANISM_LEVEL，census 在案）——
「omni 核心自打分」不是新机制，系统级 delta 必须落在**控制回路**（反馈→下一步动作）与
**模态因果接地**上，否则降级。

## §5 基线与归因对照（摸高框架下）

五臂（v2 §3.3 结构，按 owner 三阶段裁决重新定位）：

1. one-shot prompting（部署默认）；
2. 等 K 的 BoN / MBR / rerank（组件线冻结基线，含 MBR 强制基线）；
3. 反馈阻断/随机化的 agent workflow（结构同 5、反馈不进下一步）；
4. 无奖励启发式搜索（等结构、无 reward/advantage 信号）；
5. reward-guided sequential controller（本提案对象）。

**用途二分（owner 07-15 裁决的落实）**：
- **主问题（摸高）**：臂 5 能把任务效用推到多高——预算照实记录、不设 cap；报告相对臂 1 的
  绝对增量与（可测处）相对冻结核心自身天花板的兑现程度。
- **归因诊断**：臂 3/4 与臂 5 的对照回答「增量是否归因于 reward→下一步动作」（RL/agentic
  合同的证伪工具）——对照要求**结构匹配**而非预算归一；
- **等预算效率比较 = `PHASE-3_TOOL`**，本阶段不作设计门槛、不作 kill 判据。

## §6 系统级 kill / pivot / proceed

| 探针（1B 蓝图,§10） | kill 触发 | 后果（术语降级） | pivot 选项 |
|---|---|---|---|
| 反馈因果消融（阻断/随机化） | 与臂 5 无差异 | 删 RL+agentic ⇒ inference-time search/rerank | 组件线（SURVEY-B 对象）继续 |
| 模态移除/置换 | 计划/工具/效用不变 | 删 omni ⇒ text agent + audio tools（AudioToolAgent 邻域） | 转文本域系统或降组件研究 |
| 奖励移除/随机化 | 效用不降 | 删 reward-guided ⇒ heuristic workflow | 研究反馈结构本身 |
| 外部状态移除 | 无差异 | 删 agentic 的记忆分量 | 无状态控制面 |
| 黑盒接口能力移除（关灰盒信号） | 核心增量消失 | 降 API-accessible gray-box | 改研究对象为灰盒可得性 |
| 工具/检索必要性 | 无工具臂等效 | 供给侧组件降级 | 供给设计问责登记后再试 |
| 停止/弃权/恢复失效 | 预算失控或错误累积 | I3 类 safety 子系统前置 | Goodhart/停止研究先行 |
| 头空前置检查（各格） | 池/轨迹级无头空 | 该格 `HEADROOM_TOO_SMALL`,只报绝对量 | 换格,供给设计问责登记 |

任何 kill 都**不自动**否定其余谓词；每次触发按 §2 降级规则处置并入台账。

## §7 支撑 dossiers（组件层,效力不变）

- **SURVEY-B（selector/evaluator 组件线）**：census v2（94 记录簇→95 works,@28ad858）+
  ledger v2（62 行,五级
  discrepancy 在案）+ 承重更正（KIT ST / JudgeBoN=rho_pool / ernez）+ round-2 检索协议 v2
  （21 lanes/105 预注册查询,零执行,待 search-design 签署）。现行有效回应 = RESP-02（含按身份
  索引的最强结论表与 do_not_claim 机器块）。
- **测量 dossier**：原 I4 → 系统诊断层（哪些 label-free observables 预测头空/轨迹改进/失败
  regime）;四量记账（rho_greedy/rho_pool/delta_mbr/regret,cellwise-only）在终态选择子问题上
  继续可用——按 S0,不上升为身份。
- **L3 论文库规约（续47,已生效）**：本提案后全部检索/精读按 census/ledger schema 即读即登记,
  不登记不算读过;库入口 `wiki/survey/README.md`。

## §8 配置化工程 qualification

- **现状（如实,v1 评审 P0 维持）**：Hydra 主入口为 stub;历史实验以定制脚本为主;现状**不得
  称**「基于配置的实验基座」。
- **目标 schema（设计承诺,v2 §7 为种子）**：单一 agent runner——`CoreModelBackend /
  EnvironmentAdapter / ObservationBuilder / MemoryStore / Tool·Evaluator·SelectionRule
  registries / Controller / BudgetManager / StoppingPolicy / TrajectoryRecorder / StageGuard`;
  换 task/model/tool/reward/memory/controller 只换配置,不复制主循环。
- **Stage-1A 只做**：schema 冻结 + 合成 fail-closed 测试（v2 §7.3 清单:含 stage1a 连真实
  backend 即 fail、evaluator 见 gold 即 fail、固定池 selector 作为退化特例可复现等）。
- **建设节奏受 stage-gated 三问约束（owner 纪律）**：mock 层通过 + 1B 探针协议签批后才写
  真实 backend 适配;不预建。

## §9 Stage-1A 零新执行声明与 inherited exposure

- **本提案新执行 = 零**：无任何新的模型推理、数据 item 读取、logprob 获取或 smoke（含 1 item）。
- **历史暴露如实继承**（v1 评审裁定,更正维持）：既往 574 运行工件、ASR selector battery、
  MMAU selector、已触碰 dev/test = `INHERITED_PRIOR_EXPOSURE / hypothesis-grade`;不得表述为
  「项目历史 GPU 零运行」;已暴露 split 不得称 untouched holdout。
- 1B 任何 item manifest 必须先扣除 exposure union（`docs/integrity/prior_exposure_registry.json`
  + C1 E 盘补登）;诚信更正义务（MATERIAL QRP）继续履行。

## §10 Stage-1B 蓝图（PRE_STAGE2_BLUEPRINT——无现时效力,开机须 owner 签批）

B0 接口冒烟（第一条真实调用即登记 attempt #1,证严格黑盒路径可运行）→ **B1 agenticity 因果
探针**（反馈开/阻断/随机化;若 null:立即停用 agentic RL 称谓）→ **B2 omni 接地探针**（正确/
置换/遮蔽模态）→ **B3 reward-control 探针**（对臂 4 启发式搜索）→ **B4 safety 探针**
（reward 压力/预算增大下的 Goodhart、错误累积、停止合理性）→ **B5 测量探针**（label-free
observables 预测何时值得继续）。失败不跳过：B1 败即撤 agentic、B2 败降文本 agent、B3 败降
通用 scaffold——不得用 B5 找正面叙事。

**续40 已签四探针的映射（对齐裁决仍待 owner,推荐案）**：P-α 头空 → B1/B3 各格的前置检查
（无头空则该格无物可兑现）;P-β MBR → §5 臂 2 基线;P-γ 同核 logprob 信号 → 仅
`GRAY_BOX_DIAGNOSTIC` 本地校验臂（不入承重路径,黑盒合同合规）;P-δ 供给对比 → B2/供给轴。
全部 directional-only、单次触碰、尝试全登记;C1/C4 于 1B-0 由 owner 终验。

## §11 Owner gates 与对 reviewer 的请求

- **Gate S1（下一步）**：system-first survey 协议预注册——八条 lanes（①reasoning+acting 与
  环境反馈 ②test-time agent feedback/control（IAD 族必查） ③multimodal/omni tool agents
  （AudioToolAgent 族必查） ④external memory/skill acquisition ⑤training-free
  verification/control ⑥black-box/API-only 优化 ⑦reward hacking/verifier gaming/loop
  over-optimization ⑧等预算 agent evaluation 与 trajectory credit）+ SURVEY-B 子包维持;
  构造性可回放（round-1 宇宙缺失教训）;L3 即读即登记。**请求 reviewer 签署 search design 后
  才执行第一条查询。**
- Gate S2：五合同正/反例冻结;S3：runner schema + 合成测试;S4：暴露清算入 1B manifest;
  S5：Stage-1A close（与 1B 放行分立两签）。
- **对 reviewer 的四点披露**：①owner 三阶段裁决对 v2 等预算框架的修改（§5 归因/效率二分）;
  ②S0 以会话指令签署（授权原文续48,亲笔补签位保留）;③本提案先行工作表未经可回放核查,
  占据结论以 S1 survey 为准;④**P0-SYS-2 已处置于正典而非本提案**——Project-Thesis 与
  Research-Objective 已按 owner 裁决重写为 system-first（续46）且 S0 已签署（续48）,
  selector-first 旧正典已墓碑退役。
