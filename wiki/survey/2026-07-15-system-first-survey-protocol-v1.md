---
protocol_id: SURVEY-PROTO-2026-07-15-02
title: "System-first Survey 检索协议 v1（Gate S1 实例化）——八 lanes / 64 条预注册精确查询 / 57 列名种子快照"
date: 2026-07-15
status: "DRAFT — 内审环后送 reviewer 签署;签署前零查询执行（queries_executed: 0,本行为 attestation）"
authorization: "重校准评审 Gate S1 = PROTOCOLIZATION_AUTHORIZED / QUERY_EXECUTION_STILL_PENDING;proposal v2（STAGE1A-PROPOSAL-2026-07-15-03,已转交）§11 为规格来源"
quality_bar: "严评 P0-LIT-3 八项最低规格全采 + 重校准 Checkpoint A–D 判据 + 开放抽取字段(Checkpoint B) + v2 评审修正案 A–F 全采（种子快照措辞/增量扫描/领域源/chaining 续行规则/选文留痕/范围多轴+TF 审计子字段）"
relation_to_survey_b: "SURVEY-B（selector 组件线 round-2 协议 SURVEY-PROTO-2026-07-15-01,21 lanes/105 查询）独立维持零执行、另行签署——本协议不修改不吸收它"
first_query_gate: "reviewer search-design 签署 + owner 批准 + P0-R8 状态门复跑三条件齐备后,才允许执行第一条查询"
hostile_review: "PENDING — 本件送签前须过双镜头内审环;本字段实测后更新"
---

# System-first Survey 检索协议 v1

## §0 目的与授权链

按 proposal v2 §11 实例化 Gate S1 检索协议：为 system-first 研究纲领（黑盒 omni agentic
system × training-free reward-guided external control,S0 已签）完成**可回放**的占据/机制
survey。授权链：重校准评审授权协议化 → v2 评审
`APPROVE_GATE_S1_PROTOCOL_DRAFTING_WITH_REQUIRED_AMENDMENTS`（修正案 A–F 已并入本稿）→
本协议成稿送签 → 签署后执行。round-1「检索宇宙永久缺失」教训 = 全部查询构造性可回放（§9）。

**引用钉死（v2 评审 §7.3）**：proposal v1 = `cf54f1b:wiki/2026-07-15-system-first-research-
proposal-v1.md`（blob `d60aa669…`）;proposal v2 = `cf54f1b:wiki/2026-07-15-system-first-
research-proposal-v2.md`（blob `20e5bd55…`）;暂定 taxonomy = v1 §2（随上述 blob 钉定）;
seed manifest 与本协议以各自提交后的 (commit, path, blob) 三元组互引。

## §1 覆盖判据（Checkpoint A 落实）

- **系统域**：text-agent ∧ VLM/omni-agent ∧ audio-agent ∧ compound AI system 四域全查。
- **机制轴**：search / reflection / memory / tool-routing / verification / non-parametric
  adaptation 全覆盖。
- **两侧查**：training-free 同口径 ∧ 训练型最强上界（TRAINED_COMPARATOR）都纳入,不做同温层
  检索。
- 每篇按开放字段抽取（§7）,允许新类别出现并版本化修订 taxonomy（§10）。

## §2 发现源与承重源

- **发现源**：arXiv API（主）;ACL Anthology / OpenReview / IEEE Xplore / ACM DL（副,按 lane
  路由）;**领域正式版本覆盖（修正案 C）**：CVF Open Access（CVPR/ICCV 视觉与 embodied
  agent）、ISCA Archive（Interspeech 系语音）、PMLR/NeurIPS proceedings、必要时 AAAI/IJCAI
  正式页——机制结论回链作者版/正式版义务;Semantic Scholar / OpenAlex **仅作发现与引文追踪**。
- **承重源**：论文原文（arXiv 钉版本 vN / 正式 proceedings 页）;摘要级证据不升全文级
  （五级证据分级沿用：DISCOVERED / ABSTRACT_VERIFIED / FULLTEXT_OPENED / CLAIM_VERIFIED /
  REPRODUCED）。

## §3 Mandatory seeds——预协议种子快照（snapshot 2026-07-15;允许检索扩展）

**措辞纪律（v2 评审风险一）**：survey 完成前禁用「全集/完整占据图」表述——本表是**带截止日的
预协议快照**,执行起按 §5bis 增量批次滚动。

**快照构成（57 条列名 + 22 条执行时裁决）**：
① proposal v2 §4 表内 15 项（blob 见 §0 钉定）;
② 评审补充机制族 16 项（题录 AS_GIVEN,执行时解析,失败标 UNRESOLVED）;
③ 自库反扫 STRONG 15 项（`2026-07-15-gate-s1-own-library-sweep.md`）;
④ **v2 评审 delta scan 新增 7 项**（AS_GIVEN_BY_REVIEW,执行时解析）：
**Omni-Decision (2607.11433)**——最高优先威胁:training-free omni-modal QA evidence-state
system（confirmed evidence/conflicts/依赖/停止的共享状态驱动闭环）,2026-07-13 提交;
**Affordance Agent Harness (2605.00663)**——verification-gated skill orchestration 闭环
runtime（evidence store/episodic memory/router/verifier/retry/cost control）;
**FineVerify (2606.00660)**——可验证子问题分解 + 轨迹细粒度自验证聚合;
**Effective Feedback Compute (2605.29682)**——「有效反馈算力」:资源轴的候选描述语言（§7）;
**MUSE-Autoskill (2605.27366)**——技能生命周期;**自库在案**（2026-06-30 归档 survey +
`papers/agent-level-tfrl/references.bib`,专职反扫亦漏——检索失效第四例,反扫范围已补
references.bib）;
**ACE (2510.04618)**——自反扫 MEDIUM 升列名（自库 06-30 系列在案,评审独立点名）;
**VeGAS (2605.12620)**——trained-verifier 边界对照:「测试时不改 policy ≠ 全系统
training-free」的典型反例。
执行时裁决层 = 反扫 MEDIUM 其余 22 项。

**种子定性备注（v2 评审 §2.2–2.3 收紧,全文核验前生效）**：training-free-grpo (2510.08191)
标「术语/机制威胁,**TF-Strict 归属待核**」（其外设经 ground-truth 多轮学习 token prior——
冻结核心 ≠ TF-Strict）;IRO (2506.17828) 标「frozen core + trained value fn 边界」;
walking-through-uncertainty 按 §6 范围多轴拆编（组件直接 ≠ 系统直接）;scaling-auditory
「最紧 omni 机制占据者」系**团队自评待全文核验**,协议内表述 =「音频域 TTC 强边界」。

**seed manifest（签署包组成部分,修正案 A）**：`seed_manifest.jsonl` 每行 =
`{id, name, source(评审点名/自库继承/数据库发现/chaining/作者页), first_found_at(文件:定位),
verification_level(题录/摘要/全文), lanes[], rationale, exclusion_reason?, scope_pending(Y/N),
snapshot_date}`;快照截止 2026-07-15。

**已知工作处理**：命中 census v2 既有 works 者标 KNOWN 仍全量登记（dedup 不丢日志）;新工作
即读即登记 census/ledger schema（L3 规约,续47）;**自库反扫范围永久包含
`papers/*/references.bib`**（MUSE 教训）。

## §4 八条 lanes 与 64 条预注册精确查询

**通用规格**：默认引擎 = arXiv API;默认窗口 2022-10-01→2026-07-15（例外行内注明）;默认
cap = 75 条/查询、按 relevance 排序;默认类目 cs.CL+cs.AI+cs.LG（SF-3/语音类加 cs.SD+eess.AS）。
每 lane 附 2 条副源路由查询（关键词串,窗口同 lane）。查询编号 = SF-L{n}-Q{m}（arXiv）/
SF-L{n}-S{m}（副源）。允许执行中对拼写变体做**登记后**微调（原查询照跑,变体新增编号,禁替换）。

### SF-L1 reasoning+acting 与环境反馈（ReAct/Reflexion/LATS 族）
- Q1 `abs:"language agent" AND abs:feedback AND (abs:"test-time" OR abs:"inference-time" OR abs:"training-free")`
- Q2 `ti:agent AND (abs:"self-reflection" OR abs:"verbal reinforcement" OR abs:reflexion)`
- Q3 `(abs:"reasoning and acting" OR abs:"interleaved reasoning" OR abs:"act and reason") AND abs:agent`
- Q4 `(abs:"tree search" OR abs:MCTS) AND (abs:"language model" OR abs:LLM) AND (abs:agent OR abs:planning)`
- Q5 `(abs:"environment feedback" OR abs:"execution feedback") AND (abs:LLM OR abs:"language model") ANDNOT abs:RLHF`
- Q6 `abs:"language agent" AND (abs:search OR abs:planning) AND abs:value`
- S1 ACL Anthology: `language agent environment feedback`；S2 OpenReview(ICLR/NeurIPS/ICML 2023–2026): `LLM agent test-time feedback`

### SF-L2 test-time agent feedback/control（IAD 族必查——UMBRELLA 坍缩风险主查道）
- Q1 `(abs:"test-time scaling" OR abs:"inference-time scaling") AND (abs:agent OR abs:agentic OR abs:workflow)`
- Q2 `abs:sampling AND abs:evaluation AND abs:feedback AND (abs:agentic OR abs:agent)`
- Q3 `(abs:"inference-time alignment" OR abs:"decoding-time alignment" OR abs:"test-time alignment")`（窗口 2023-01 起）
- Q4 `(abs:"reward-guided" OR abs:"reward guided") AND (abs:decoding OR abs:search OR abs:control OR abs:planning)`
- Q5 `(abs:"verifier-guided" OR abs:"value-guided" OR abs:"feedback-guided") AND (abs:"language model" OR abs:LLM)`
- Q6 `abs:"test-time compute" AND (abs:allocation OR abs:budget OR abs:optimal OR abs:adaptive)`
- S1 OpenReview: `agentic test-time alignment feedback`；S2 ACM DL: `inference-time control language model agent`

### SF-L3 multimodal / omni tool agents（AudioToolAgent/EChO-Agent 族必查;+cs.SD,eess.AS）
- Q1 `(abs:audio OR abs:speech OR abs:auditory) AND (abs:agent OR abs:agentic) AND (abs:tool OR abs:orchestration)`
- Q2 `(abs:omni OR abs:multimodal) AND abs:agent AND (abs:tool OR abs:expert OR abs:routing)`
- Q3 `(ti:audio OR ti:speech OR ti:voice) AND (ti:agent OR ti:copilot OR ti:assistant)`（窗口 2023-01 起）
- Q4 `(abs:"audio question answering" OR abs:"audio reasoning" OR abs:"auditory reasoning") AND (abs:tool OR abs:agent OR abs:"chain of thought")`
- Q5 `(abs:"audio-language model" OR abs:"audio language model" OR abs:"speech language model") AND (abs:"tool use" OR abs:"function call" OR abs:"tool calling")`
- Q6 `(abs:vision OR abs:video) AND abs:agent AND (abs:"training-free" OR abs:frozen) AND abs:tool`（跨模态类比道）
- S1 IEEE Xplore(ICASSP/SLT/ASRU): `audio agent tool use LLM`；S2 OpenReview: `omni agent multimodal tool`

### SF-L4 external memory / skill acquisition（Voyager/AWM/ExpeL 族）
- Q1 `(abs:"skill library" OR abs:"skill acquisition" OR abs:"skill discovery") AND (abs:agent OR abs:LLM)`
- Q2 `(abs:"episodic memory" OR abs:"external memory" OR abs:"workflow memory") AND (abs:agent OR abs:LLM)`
- Q3 `abs:"experiential learning" AND abs:LLM AND (abs:"in-context" OR abs:"training-free" OR abs:API)`
- Q4 `(abs:"memory management" OR abs:"memory operations") AND (abs:"language model" OR abs:agent) AND (abs:"test-time" OR abs:lifelong OR abs:continual)`
- Q5 `(abs:"self-evolving" OR abs:"self-improving") AND abs:agent AND (abs:memory OR abs:skill OR abs:context)`
- Q6 `(abs:"context engineering" OR abs:"context adaptation" OR abs:"context evolution") AND (abs:agentic OR abs:agent)`
- S1 ACL Anthology: `agent memory skill library`；S2 OpenReview: `LLM agent experiential memory no training`

### SF-L5 training-free verification / control（LLM-as-Verifier/PRM 族 + 负结果道）
- Q1 `(abs:"training-free" OR abs:"tuning-free" OR abs:"without fine-tuning") AND (abs:verifier OR abs:verification OR abs:reward) AND (abs:LLM OR abs:"language model")`
- Q2 `(abs:"LLM-as-judge" OR abs:"LLM as a judge" OR abs:"LLM-as-verifier") AND (abs:agent OR abs:action OR abs:trajectory)`
- Q3 `(abs:"process reward" OR abs:"process supervision") AND (abs:"training-free" OR abs:"off-the-shelf" OR abs:frozen)`
- Q4 `(abs:"self-verification" OR abs:"self-evaluation" OR abs:"self-correction") AND (abs:limitation OR abs:fail OR abs:cannot)`（负结果/边界道）
- Q5 `abs:verifier AND (abs:"test-time" OR abs:"inference-time") AND (abs:scaling OR abs:granularity OR abs:budget)`
- Q6 `(abs:"generative verifier" OR abs:"generative reward model")`
- S1 ACL Anthology: `training-free verifier LLM judge agent`；S2 OpenReview: `process reward training-free verification`

### SF-L6 black-box / API-only 优化（GEPA/OPRO/DSPy 族 + 接口可得性道）
- Q1 `(abs:"black-box" OR abs:blackbox) AND (abs:"language model" OR abs:LLM) AND (abs:optimization OR abs:adaptation OR abs:agent)`
- Q2 `(abs:"API-only" OR abs:"closed-source" OR abs:"API access") AND (abs:adaptation OR abs:optimization OR abs:alignment)`
- Q3 `(abs:"gradient-free" OR abs:"derivative-free" OR abs:"zeroth-order") AND (abs:"language model" OR abs:LLM) ANDNOT abs:"soft prompt"`
- Q4 `(abs:"prompt optimization" OR abs:"prompt evolution" OR abs:"instruction optimization") AND (abs:"black-box" OR abs:LLM)`
- Q5 `(abs:"compound AI" OR abs:"compound system" OR abs:"LM program" OR abs:"language model program") AND abs:optimization`
- Q6 `(abs:logit OR abs:logprob OR abs:"log-probability") AND abs:access AND abs:"language model"`（接口可得性——JitRL 类「方法最近、接口不合」边界道）
- S1 OpenReview: `black-box LLM optimization API-only`；S2 ACM DL: `compound AI system optimization`

### SF-L7 reward hacking / verifier gaming / loop over-optimization（Goodhart 族;Q3 窗口 2020-01 起）
- Q1 `(abs:"reward hacking" OR abs:"reward gaming" OR abs:"specification gaming") AND (abs:LLM OR abs:"language model" OR abs:"test-time" OR abs:inference)`
- Q2 `(abs:"reward overoptimization" OR abs:"over-optimization" OR abs:overoptimization) AND (abs:reward OR abs:verifier)`
- Q3 `abs:Goodhart`（窗口 2020-01 起,cap 50）
- Q4 `(abs:"verifier gaming" OR abs:"judge hacking" OR abs:"evaluation gaming" OR abs:"benchmark gaming")`
- Q5 `(abs:"best-of-n" OR abs:"best-of-N") AND (abs:KL OR abs:overoptimization OR abs:distribution)`
- Q6 `(abs:"stopping rule" OR abs:abstention OR abs:"early stopping") AND (abs:"test-time" OR abs:inference) AND (abs:reward OR abs:verifier OR abs:confidence)`
- S1 OpenReview: `reward hacking inference time best-of-n`；S2 ACL Anthology: `verifier gaming overoptimization`

### SF-L8 等预算 agent 评测 / trajectory credit（Kapoor/tau-bench 族）
- Q1 `(abs:"agent evaluation" OR abs:"agent benchmark") AND (abs:cost OR abs:budget OR abs:compute OR abs:efficiency)`
- Q2 `(abs:"matched compute" OR abs:"compute-matched" OR abs:"budget-matched" OR abs:"cost-controlled" OR abs:"equal compute")`
- Q3 `abs:"credit assignment" AND (abs:trajectory OR abs:agent) AND (abs:LLM OR abs:"language model")`
- Q4 `abs:Pareto AND abs:agent AND (abs:cost OR abs:accuracy)`
- Q5 `abs:"test-time compute" AND (abs:"scaling law" OR abs:predict OR abs:"when to")`
- Q6 `(abs:overthinking OR abs:"give up" OR abs:"premature termination") AND (abs:agent OR abs:"long-horizon")`
- S1 OpenReview: `agent evaluation cost budget pareto`；S2 ACM DL: `LLM agent cost-controlled evaluation`

**计数**：8 lanes × (6 arXiv + 2 副源) = **64 条预注册查询**。预算/调用量等资源轴不是查询
过滤器,是抽取轴（§7,重校准 §2.1 口径）。

## §5 Snowballing 与饱和判据

- 57 列名种子 + 每条 INCLUDED-DIRECT 命中：backward（参考文献）+ forward（引文,经 SS/OpenAlex
  发现层）各一轮。**「一轮」是最低动作,不是停止条件（修正案 D）**：每轮产生的新 DIRECT 邻居
  继续 chaining,直至**连续两轮零新增 DIRECT**（饱和）才停;新簇出现即重启该簇计数。
- **任何 NO_DIRECT_MATCH 类结论**须满足预注册饱和：连续两轮 snowballing 零新增直接邻居 +
  **双评审独立同意**;伴随 token 制度沿用（按身份索引,禁全局 token）。

## §5bis 时新性增量扫描（修正案 B——Omni-Decision 已证明此非形式主义）

① 首次执行时检索至执行当日;② synthesis 冻结前做「首执行日 → 冻结日」增量扫描;③ Stage-1A
跨长时段则维护**带日期的增量批次**（seed manifest 追加行,永不改旧行）;④ 新文献按同一 schema
编码,不静默改写旧判决（判决修订走 §10 版本化）。

## §6 纳排矩阵（十轴,P0-LIT-3-④）

每条 INCLUDED 记录编码：`core_access(weights/logits/API-text) | parameter_update(none/prompt/
adapter/full) | external_state_update(none/memory/skill/tree) | reward_type(gold/verifier/
self/env/none) | policy_update(none/nonparametric/trained) | modality_path(text/audio-native/
audio-tool/vision/omni) | tool_use(none/fixed/routed/learned) | budget_horizon(单步/固定K/
多轮/任意) | task(域) | trained_comparator(Y/N)`。EXCLUDED 必须记排除理由（§9 日志字段）。

**TF-Strict 审计子字段（标题驱动漂移防护,v2 评审风险二）**：`base_model_updated(Y/N) |
external_component_trained(Y/N,对象) | ground_truth_used(无/预先/开发集/测试时) |
learned_object(token-prior/value-fn/verifier/prompt/none) | learning_time(test 前/test 中) |
test_time_readonly(Y/N)`——「冻结核心 ≠ TF-Strict」（Training-Free GRPO / IRO / VeGAS 类
必经此审计）。

**范围多轴（修正案 F——不用单一 DIRECT/OUT 压平）**：`system_level_proximity |
component_level_proximity | modality_proximity | tf_strict_compliance | black_box_compliance |
reward_control_proximity | persistence_state_proximity | evidence_grade` 各轴独立编码
（如 walking-through-uncertainty：组件直接、系统不直接）。

## §7 抽取字段与证据分级

开放字段（Checkpoint B 全采,允许新增列并版本化）：`core access / modality path / external
components / feedback type / what changes at test time / persistence scope / compute scaling /
claimed mechanism / strongest result / failure mode / reusable implementation`。资源六轴
`{model calls, tool calls, tokens, latency/cost, horizon, stopping}` 作为文献抽取轴观察
收益饱和/退化。承重 delta 须 version pin + section/page/table/equation locator + 必要长度
span（P0-LIT-3-⑥）;L3 即读即登记（census/ledger schema）。

## §8 Threat papers 双人独立全文抽取（P0-LIT-3-⑧）

首批 13 篇（执行中可增至 15,增须登记理由）：**Omni-Decision 2607.11433（最高优先）** /
IAD 2504.01931 / AudioToolAgent 2510.02995 / EChO-Agent 2606.15141 / Agent-Omni 2511.02834 /
Audio-Mind 2605.28480 / JitRL 2601.18510 / training-free-grpo 2510.08191 / LATS 2310.04406 /
Voyager 2305.16291 / Kapoor 2407.01502 / Speech-Copilot 2407.09886 /
inference-time-reward-hacking 2506.19248。两名独立抽取者（不同 agent 会话,互不见对方产出）
按 §6/§7 编码,冲突由协调者亲验裁决并留痕。**选文过程留痕（修正案 E）**：候选池全集、两名
评审各自的排序与理由、分歧与最终合并规则全部归档——选文环节零无记录筛选。

## §9 日志与可回放（P0-LIT-3-⑦;round-1 宇宙缺失的构造性防复发）

每次查询写 JSONL 一行：`{query_id, engine, exact_query, window, cap, sort, timestamp,
raw_response_ref 或可重建结果 ID 清单, n_hits, included[], excluded[{id, reason}],
failed_request(如有)}`——存 `wiki/survey/replay/SF-SURVEY-2026/`。原始响应能存则存,不能存
（接口条款）则记录可重建 ID 集。快照/哈希按哈希正典（git blob）。

## §10 Taxonomy 版本化修订

五合同 = PROVISIONAL_STAGE1A_TAXONOMY：survey 证据要求修改分类时,走**版本化增补**
（amendment 文件 + 修订理由 + 生效日期）,禁静默改写;新类别按收词纪律先登记后使用。

## §11 停止规则与产出

- 每 lane 停止 = 64 条查询全执行 + snowballing 达饱和;整体停止不设时间 cap,以覆盖判据（§1）
  与饱和（§5）为准。
- 产出：coverage/kill matrix v3 + SOTA cards v3 + 更新的 census/ledger + **3–5 个
  system-level candidate problems**（Checkpoint D;候选池含重校准 §4 六类）——供 Stage-1C
  owner 双证据选题;不做 intersection-novelty 论证（Checkpoint C）。

## §12 签署流

1. 本协议过内审环 → owner 过目 → 送 reviewer **search-design 签署**;
2. 签署后执行前置：owner 批准 + P0-R8 状态门复跑（三条件缺一不可,frontmatter first_query_gate）;
3. 执行期间任何查询/种子/判据变更走 §10 版本化增补并即时可见于 replay 目录;
4. survey 完成 → 综合 → 届时才谈 Stage-1A close（与 1B 放行分立两签）。
