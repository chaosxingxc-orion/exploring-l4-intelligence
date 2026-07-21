---
artifact_id: "SF-STAGE1A-REVIEWER-PROPOSAL-DRAFT-2026-07-21-01"
title: "System-first research proposal and Stage-1A remediation disclosure"
date: 2026-07-21
audience: "independent doctoral reviewer and research owner"
lifecycle: "WORKBENCH_REVIEW_DRAFT"
promotion_target: "wiki/audit/system-first-stage1a/round-16/research-proposal-and-stage1b-signoff-request.md"
promotion_trigger: "3/3 semantic-correction reviews and 19/19 active negative-evidence adjudications recorded; evidence-v7 NT/POSIX leaves and aggregate PASS; proposal source manifest and package gate PASS"
current_stage: "STAGE_1A_FINAL_REMEDIATION"
formal_review_status: "NOT_YET_SUBMITTED_AS_IMMUTABLE_ROUND_16"
stage1b_status: "UNSTARTED_AND_UNAUTHORIZED"
systematic_discovery_queries_in_this_repair: 0
research_model_or_smoke_calls_in_this_repair: 0
remediation_evidence_commit: "044bb557c6174ec4600c9cd47f69a5ba9529eb2c"
---

# 给独立评审人的研究提案与整改说明

## 0. 请先读这一页

我们研究的对象不是一个新的声学编码器、一个更大的 verifier，或一条孤立的 reranking 技巧，而是围绕冻结黑盒 omni foundation model 的 **external reward-guided control plane**：系统在不改变核心模型权重和内部结构的条件下，管理上下文供给、外部记忆、工具与检索、候选生成、评估、选择、预算和停止动作。内部简称 training-free RL；对外表述为 *weight-frozen reward-guided inference-time optimization*。

本文件同时承担两个任务：

1. 请评审研究问题本身是否值得继续做 systematic mapping；
2. 把上一轮严厉审查之后的实际整改、仍未闭合的证据门以及 reviewer 需要完成的动作一次讲清楚。

本文件不是 reviewer verdict，也不是 Stage-1B 启动令。当前仍是 Stage-1A。第一条 systematic discovery query、任何研究模型调用、任何 smoke、指标实验或 prototype 都尚未执行且仍被禁止。

目前四项 implementation gate 中，GM-1、GM-3 的执行地基和 GM-4 已经由本地机器证据闭合。评审冻结点不是含糊的“至少一个 concern”，而是 **exactly 3/22 implementer concerns**、`0/22 independent decisions`。原文复核后，这三条负证据已退出 active absence 库：DREAM 的 controller-label 字段改为 `true`，DREAM 的 human/dev model-selection 与 DeepVerifier 的外围更新字段改为 `unknown`，相关 method path 均降为非承重 conflict queue。当前库存恒等式为 **`22 = 3 + 19`**：3 条修正各需一个独立确认，19 条 active absence 各需一个独立语义裁决；当前分别为 `0/3` 与 `0/19`。因此 evidence-v7 会同时返回 `SEMANTIC_CORRECTION_REVIEW` 与 `ABSENCE_REVIEW`，没有生成伪造的双平台 PASS aggregate。

## Track A — 科学提案

## 1. 中心问题

现代 omni / multimodal LLM 在预训练中吸收了大量跨模态、跨任务、不同粒度的知识，但默认推理并不总能稳定地把这些知识转化为正确的语音和音频任务行为。本项目的中心问题是：

> 在核心模型保持黑盒、权重冻结且内部结构不变时，reward-guided 的外部控制系统能够在多大程度上激活其已有知识，并把这种提升做成可验证、可归因、可停止且不越过信息边界的推理过程？

这里的 “RL” 指 reward/advantage 对下一步外部动作的控制，而不限定为权重更新。best-of-N、MBR 和 reranking 是终端动作空间退化后的特例；完整研究对象还包括观察与供给构造、状态、记忆、工具、候选扩展、验证、回退、停止和风险控制。

## 2. 为什么要先做 system-first mapping

直接相邻的 speech/omni agent、工具编排和 trained speech reward 工作已经存在。当前 reviewer bibliography 已显式路由 AudioToolAgent、Audio-Mind、Agent-Omni、EChO-Agent、AuTAgent、Speech-Copilot、VoxMind、Thinking While Listening、Native Active Perception、Llasa、OmniGAIA、WavReward 和 GSRM；reward/verification 与 training-free/trained boundary 也分别形成可见链条。它们证明这一问题空间并不空白，也因此使任何 “first-ever” 或已确立 novelty 的说法都不成立。

仍值得继续 mapping 的理由不是“没有人做过 agent”，而是现有工作横跨了不同的研究边界：

- 有些系统训练核心或外围组件；有些只在推理期操作；
- 有些奖励只做终端选择；有些信号拥有 retry、revise、route、tool-call 或 stop 权；
- 有些方法读取检索、工具或环境的新信息；有些只重排冻结输入条件下的候选；
- 有些工作研究 generator coverage，有些研究 verifier discrimination，有些研究 selector 或搜索；这些杠杆不能被一个最终分数混为同一原因；
- speech reward model 可以是重要的 measurement instrument，但 trained RM 本身不应被误记为 TF-Strict 方法占据。

在不知道直接 prior 占据哪些 cell 之前进入 prototype，会把研究目标倒置为“先做出一个系统，再寻找空位”。Stage-1B systematic mapping 的首要价值是识别真正被占据、仍为空缺以及因证据不足而不可判定的区域。

## 3. 研究边界

### 3.1 TF-Strict 核心合同

候选方法只有在下列边界可被清楚编码时才可能进入项目核心候选集：

- 核心模型权重不更新；
- 核心内部结构不改变；
- 方法不依赖 gradients、hidden states、attention 或保证可得的 logprobs；
- test-item gold 不进入 prompt、reward、selector、retrieval、candidate construction 或 stopping；
- 外部组件训练、controller 的 label optimization、human/dev model selection 与 new-information channel 必须单独编码，不能被“核心冻结”一句话吞掉；
- 每个 reward/signal 必须绑定其 form、source、lifecycle、uses，并沿 LIVE causal edge 绑定到真实 decision right。

外部工具或 retrieval 并非一概禁止，但必须明确区分 read-out 与 new-info。后者可以是重要 comparator，却不能静默进入严格闭集的同一分母。

### 3.2 阶段边界

- Stage-1A：冻结研究问题、系统综述设计、纳排/编码/证据合同和放行机制；
- Stage-1B：只执行 systematic mapping，全程禁止研究模型与 smoke；
- Stage-1C：综合证据、形成候选问题卡并由 owner 选题；
- Stage-2A：先复现最接近且公开可复现的 prior，再做方向性原型；
- Stage-2B：冻结假设、SESOI、指标和信息边界后做方案验证；
- Stage-3：投稿与发布。

## 4. Research questions

### RQ-SYS — 系统占据与空缺

现有 speech/omni inference-time systems 中，哪些工作真正构成 reward-guided external control plane？它们控制哪些动作，是否满足黑盒与 TF-Strict 边界，哪些 cell 已被直接 prior 占据？

### RQ-MECH — 信号如何改变系统行为

信号的 form、source、lifecycle 和 uses 分别是什么？信号是否沿可验证的 causal edge 控制 candidate selection、retry、revision、routing、tool use、memory update、budget 或 stopping？

### RQ-SUPPLY-MAP — 候选供给如何被既有工作构造和报告

既有工作用了哪些 prompt、retrieval、tool output、sampling、candidate pool 与 budget 条件？是否报告 pool coverage、oracle/upper-bound 或供给失败证据？Stage-1B 只映射来源、条件与证据等级，不新测 oracle headroom。

### RQ-VERIFY-MAP — 既有 generator、verifier 与 selector 证据如何分离

既有工作是否分别报告 generator coverage、verifier discrimination、selector/control、等 K MBR、oracle 上界与相应 ablation？Stage-1B 记录可归因证据和缺失项，不用论文最终分数反推因果贡献。

### RQ-BOUND — 哪些结果依赖越界资源

哪些增益依赖核心或外围权重更新、label-optimized controller、human/dev 选择、test gold、new-information retrieval 或白盒内部状态？这些依赖如何改变研究结论的适用域？

### RQ／Hypothesis 阶段责任矩阵

| RQ/Hypothesis | answering_stage | Stage-1B evidence product | later empirical test | falsifier |
|---|---|---|---|---|
| RQ-SYS + H1 | Stage-1B mapping；Stage-1C synthesis | method-path occupancy、拓扑、状态、动作权与 direct-prior proximity | Stage-2 复现最近系统并检查分类是否预测真实控制差异 | 直接 prior 在相同边界与动作权下已经等价占据 |
| RQ-MECH + H2 | Stage-1B mapping；Stage-2 causal validation | signal/edge/decision-right evidence bundle；terminal-vs-sequential 分层 | matched ablation 移除或替换 LIVE edge | 在线信号不改变任何后续动作，或 terminal-only 模型同样解释证据 |
| RQ-SUPPLY-MAP + H3 | Stage-1B 映射 reported supply；Stage-2 回答新 headroom | supply condition、pool construction、reported upper bound、missingness | 在冻结 `c` 下测 oracle headroom；换 `c` 必须重测 | 合理预注册供给族持续无 headroom |
| RQ-VERIFY-MAP + H3 | Stage-1B 映射 reported attribution；Stage-2 回答因果分解 | generator/verifier/selector/MBR/oracle/ablation availability matrix | 等 K MBR、verifier ROC／校准与 selector matched controls | 有 headroom但 label-free selector 稳定不超过等 K MBR |
| RQ-BOUND + H4 | Stage-1B mapping | 七个 strict bits、new-info/read-out、trained comparator 与 unresolved table | Stage-2 在冻结边界下做 matched rerun | 所有表面收益仅在越界资源可用时存在 |
| H5 speech/omni specificity | Stage-1B 七字段 mapping；Stage-2 复现 | modality topology 等七字段与 dual disagreement report | 对 text-only 与 speech/omni matched paths 比较时序、证据与状态预测 | 七字段不能产生区别于 text-only control 的可测预测 |

这里的 mapping 与 empirical 答案不可互换。Stage-1B 可以记录论文报告过的 headroom/ablation，但新 headroom、WER、EM、selector 与因果归因结果只能从 Stage-2 产生。

## 5. 贡献假设，而不是预先写好的结论

H1 — **System hypothesis**：相比把生成、reward 和选择视为孤立模块，用显式状态、动作权和停止规则描述 external control plane，能够揭示已有方法之间被最终指标掩盖的结构差异。

H2 — **Sequential-control hypothesis**：真正拥有 retry、revise、route、tool-call 或 stop 权的在线信号，与只在固定 K 池上做终端 reranking 的方法属于不同控制能力层级；后者是前者的退化特例，而非完整定义。

H3 — **Conditional-headroom hypothesis**：可兑现提升受 `c` 条件下 oracle headroom 限制。没有 headroom 的 null 主要否定供给配置；有 headroom 但 selector 长期无法超过等 K MBR，才构成对选择机制的有力否证。

H4 — **Boundary hypothesis**：一部分看似 training-free 的收益实际依赖 trained peripheral reward、label-tuned controller 或 new-information channel。显式编码后，方法占据与贡献边界会显著收缩。

H5 — **Speech/omni specificity hypothesis**：speech/omni 系统的实时性、长序列、音频证据、turn-taking 和工具编排使其控制问题不能完全由 text-only verifier/reranking 结论代替。Stage-1B 按 `modality-specificity-codebook.md` 的七字段映射并处理 dual disagreement；Stage-2 才检验这些字段能否产生可测预测。

这些全部是 hypothesis-grade。Stage-1A 没有给出 novelty 或 effectiveness verdict。

## 6. Stage-1B systematic mapping 方案

### 6.1 冻结输入

执行只使用现已冻结的 query/compiler、T1 route、seed/citation-chaining 入口、REC-0 至 REC-7 模板和 current protocol。方法适配由 `wiki/survey/current/mapping-methods-adaptation.md` 冻结；H5 编码由 `wiki/survey/current/modality-specificity-codebook.md` 冻结。现有 query 文件保持在 `wiki/survey/2026-07-15-sf-queries.jsonl`；本轮整改没有增加 lane、改写 query term 或执行任何一条 query。

已知论文、reviewer-known items 和历史 corpus 只能作为带 provenance 的入口或 comparator，`query_recall_credit=false`；它们不得被反向计作 frozen query 的召回结果。

正式执行所用 search design 可压缩为下表；细则仍以 current protocol、compiler/profile 与模板字节为准：

| 项目 | Stage-1B 冻结规则 |
|---|---|
| databases/routes | 冻结 query lanes、T1 proceedings routes、预注册 backward/forward snowballing；逐 route 留 receipt |
| 时间窗／语言／文献类型 | 使用 compiler/profile 和 T1 manifest 中的窗口与类型；任何偏差只能走 dated amendment |
| inclusion/exclusion | REC-0 至 REC-7；每个 EXCLUDE 留 REC-0 reason，UNRESOLVED 不伪装成排除 |
| screening | canonical work 去重后双人筛选；claim 作为 hyperedge 保留 |
| 全文深度 | D0 metadata、D1 abstract/official page、D2 local fulltext；承重结论必须达到所需 D2 |
| 编码／裁决 | coder 与 adjudicator 分离；字段级 disagreement 进入队列，不做 work-level 覆盖 |
| quality/evidence grade | 证据保持产生阶段等级；metadata existence 不升级为 mechanism evidence |
| exit/reopen | 按预注册 exit mechanism 停止；只有触发条件成立才 reopen，且 amendment 不回写 frozen query |
| exposure | query、known-ID metadata、全文 fetch、模型调用分别记账；Stage-1B 模型/smoke 恒为禁用 |

### 6.2 检索与筛选流程

1. 按冻结顺序执行 discovery routes，逐次写 attempt/receipt；
2. exact identity、显式 alias 与 unresolved identity 分开，canonical work 去重；
3. 同一 work 只形成一个 canonical node，seed 不重复制造 work；
4. claim 是指向 work 的 hyperedge，多 claim、多 evidence grade 和多 discrepancy status 保留，不压扁成一个 work-level scalar；
5. REC-0 排除必须记录理由；INCLUDE、EXCLUDE、UNRESOLVED 与 reference role 分离；
6. 只在 code-on-use 时提高全文深度，非承重 P2 不因“可能有用”而阻塞开门；
7. coder 与 adjudicator 分离，承重 row 未 adjudicate 不进入 headline 或 gap claim；
8. 到达预注册 exit mechanism 后停止，而不是因不断出现新论文无限延长 Stage-1B。

### 6.3 编码单元

每个 method path 至少编码：核心拓扑和原生模态、内部可见性、核心/外围更新、label 与 new-info 边界、signals、control horizon、decision rights、control edges、candidate pool、selection object、terminal operator、全文版本与字段级证据。核心 speech/omni path 另编码 modality topology、temporal regime、observation granularity、acoustic evidence provenance、latency/action timing、output/action modality 与 state persistence。

negative evidence 不是“没看到”。对于七个允许的 absence 字段，必须完成各自 proof obligation；`unknown`、missing、unreachable、not-coded 和 not-applicable 不具备承重资格。

### 6.4 Stage-1B 产出

- 一张无重复 canonical-work map；
- system-first / reward-verification / boundary 三条 evidence chain；
- 逐 cell 的 occupancy 与 unresolved accounting；
- negative-prior 和 falsifier 表；
- 直接 prior 的 proximity、可复现性和 reproduction-readiness evidence；
- **Stage-1B eligible inputs**：供 Stage-1C 使用的证据包，不含最终卡片、排名或 owner 选择。

Stage-1B 不产生模型效果、headroom、WER、EM 或 prototype 结果。

## 7. Stage-1C 与 Stage-2 方法预告

**Stage-1C owns the final 3–5 candidate cards**、候选排名、owner 选题和 reproduction-list freeze；这些不再写成 Stage-1B 产出。Stage-1C 依据映射结果选择研究问题，而不是选择最容易实现的模块。每张最终候选问题卡必须包含最近 direct prior、尚未占据的最小差异、可证伪假设、信息边界、最小复现、资源需求与终止条件。

Stage-2A 的第一动作是复现最接近公开 prior。只有复现可用后才允许方向性原型。若进入 selector/headroom 路线，报告必须 cellwise 同列：`delta_mbr`、`regret`、`rho_greedy`、`rho_pool`；分母过小时标 `HEADROOM_TOO_SMALL`，不报告误导性比率。部署代理 `S` 与 gold utility `U` 严格分开。

## 8. 证伪条件

以下任何结果都应改变或终止对应假设，而不是通过换名词继续保留：

- systematic mapping 找到与拟议系统在核心边界、信号、动作权和用途上等价的 direct prior：撤回或缩窄 novelty hypothesis；
- 在合理且预注册的供给族中重复观察不到 oracle headroom：停止该任务/供给路线；
- 有稳定 headroom，但 label-free selector 无法超过等 K MBR：否定当前 selector hypothesis；
- 增益只在 test gold、new-info、核心/外围训练或 white-box state 可用时出现：结论移出 TF-Strict；
- 同一方法的关键信息无法从不可变全文证据解析：保持 `UNRESOLVED`，不得通过作者意图猜测承重；
- speech/omni specificity 不能产生区别于 text-only control 的可测预测：合并或撤回该专门化假设。

## 9. 风险、限制与博士价值

主要风险是术语膨胀、邻近工作漏检、异构 claim 被去重时压扁、negative evidence 假绿、把内部机器 PASS 写成 reviewer sign-off，以及把 metadata fetch 当作 systematic recall。当前整改主要针对这些风险建立可执行约束。

Stage-1A 的 known-item evidence 仍是 hypothesis-grade，不是完整 mapping。official metadata receipt 只证明身份和书目信息，不证明论文方法主张；只有达到所需 D2/fulltext grade 的来源才能支持承重 gap/boundary claim。现有 direct-neighbor bibliography 的多数条目仍是 queue/comparator，因此本提案只用它们证明“邻近工作存在且必须系统比较”，不据此宣称方法空白。

若研究成功，其博士价值不在堆叠一个新 agent 名称，而在形成并验证一套关于冻结 omni 模型外部控制的理论与经验框架：供给条件下的可兑现空间、reward signal 的实际动作权、generator/verifier/selector 的可分归因、信息边界和可停止性。如果 mapping 证明核心系统假设已经被直接 prior 完整占据，该负结论同样有价值，因为它会阻止重复造轮子并把后续工作转向仍可证伪的最小差异。

## Track B — 对严厉审查的逐项整改

## 10. 最近修复的提交链

| Commit | 修复内容 | 当前证据状态 |
|---|---|---|
| `3fdd1d5`, `7077faa` | 修复 linked-worktree 跨 Windows/WSL Git 解析，生成双平台 preflight receipt | PASS；两端解析同一 root/HEAD/blob，relative gitdir，shared `core.worktree=null` |
| `e8b845c` | 建立七个 `(field, encoded value)` 的 negative-evidence compatibility 和跨 artifact binding | 合同与 mutation tests PASS |
| `337a84b` | 为原始 22 条 absence 建 proof obligation、全文 SHA、owner row/sidecar 和稳定 adjudication ID | 后续原文复核识别 3 条 concern；不能继续作为 22 条 active negatives |
| `c3441e7` | 实现 NT/POSIX leaf + final aggregator 的 evidence-v7 DAG | DAG 和反例测试 PASS；正式 leaves/aggregate 因上项按规则暂缓 |
| `763bfcd` | 将 census/seed/bibliography/claim/version/fulltext/reviewer-known 合并为无损 canonical-work union graph | PASS；不再为 claim 或 seed 生成重复 work |
| `035cd19` | 从官方 raw receipt 生成 77-work bibliography，恢复 system-first/reward/boundary 三条链 | PASS；Windows/WSL 可离线重建，known-ID recall credit=false |
| `c2739d4` | 撤下 3 条与全文冲突或证据不足的负结论，建立 `22 = 3 + 19` 修正台账 | PASS；一条改 `true`、两条改 `unknown`，均退出承重 absence |

## 11. GM-1：claim/work 去重和旧库无损桥接

机器报告 `docs/checks/system-first-stage1a/context-v2/existing-corpus-disposition-check.json` 当前为 PASS：483 个物理 source rows 被恰好路由到 245 个 canonical work nodes；其中 census 95、seed 92、bibliography 65、claim 62、version-pin 30、fulltext events 129、reviewer-known 10。两条 source-metadata row 仍保留为 source metadata，不伪装成 work。GM-1 的语义严格限于 **seven registered active corpora 的 lossless union**，不是 archive 或全部历史语料已经完备利用的声明。

claim 去重采用“work node + claim hyperedge”，不是“每个 claim 复制一个种子”：62 条 claim row 保留 75 个 work references，去重后为 44 个 work references、31 个 unique claim works，且没有 claim target 游离在 census 之外。92 条 seed 是 92 个 unique works，没有 duplicate seed source row；其中 13 条复用已经存在的 census canonical work，generated seed rows 为 0。

异质性没有被 best/worst 聚合吞掉：16 个 work 有多个 claim，15 个 work 有多个 evidence grade，12 个 work 有多个 discrepancy status，5 条 claim edge 指向多个 work。一个非承重旧 IEEE identity 保持 unresolved；load-bearing unresolved 为 0。`unexplained_orphans=0` 只表示每条 source row 有解释，不表示全部论文已验证或深读。

## 12. GM-2：negative evidence 合同与尚未完成的独立复核

旧实现允许 `absence` 与任意字段值组合，理论上能让正向类别依靠“未见反证”通过。现合同只允许七个实际观察到的负值组合，并强制：proof obligation、检查位置、reason、全文 identity/SHA、owner method path、owner sidecar、coder、owner row SHA 和 adjudication row ID。

cross-binding validator 会拒绝 wrong fulltext hash、wrong sidecar、wrong row hash、artifact 缺 row、非 `AGREE` verdict、URL 代替全文版本、弱 `not contradicted`、空缺/unknown 冒充 absence，以及 coder/adjudicator actor collision。

但是机器只能证明绑定一致，不能证明语义负结论或人员独立。独立报告在旧 22 条库存中识别出 exactly 3/22 implementer concerns；团队没有把它们强行 `AGREE`，而是依照冻结全文立即修正。`negative-evidence-semantic-corrections-v1.json` 逐条绑定旧 ID、旧/新 row hash、全文 SHA、证据 locator 与退役原因，并为三条修正保留独立确认槽。active absence artifact 仍为 19 个 proof rows、0 个 reviewer rows，且明确登记 `22 = 3 + 19`。当前 v7 probe 因此诚实返回 `SEMANTIC_CORRECTION_REVIEW` 与 `ABSENCE_REVIEW`。

请独立 reviewer 先对三条修正逐条确认 `AGREE|DISAGREE`，再对剩余 19 条 active proof rows 逐条检查冻结全文和 obligation；两类判断都必须给出具体理由、身份、未参与范围、时间和 conflict declaration。修正确认行与 active absence adjudication 行分属两个 schema，不得把退役负命题重新塞回 active absence 库。任何 `DISAGREE` 都应触发字段更正或 row 降级；不能为了保持旧 occupancy 强行同意。

## 13. GM-3：真实双平台证据 DAG

旧流程在 POSIX 输出前生成所谓 aggregate，实际上只是第二次 Windows 运行。现在两端 runner 只能各写自己的 leaf，独立 aggregator 必须最后读取两份 exact bytes，并核对 input snapshot、runner hash、contract version、platform stamp、named failures、occupancy 和 output semantics。删除或替换任何 leaf、改变输入 hash、平台角色或 occupancy 都会 fail closed。

跨平台 Git preflight 已证明 Windows 与 WSL2 Ubuntu-24.04 能直接解析同一 linked worktree；不再依靠临时 wrapper。正式 v7 leaves 尚未生成，因为 GM-2 未通过。先生成一个带 FAIL 的 aggregate 再称为“跨平台一致”没有研究价值，因此流程选择等待真实 reviewer input。

## 14. GM-4：书目证据、系统主线和本地优先

旧 bibliography 的 title/authors 常量同时充当 generator 输入和 test oracle，存在一起写错却全绿的循环。现在每一条由官方 raw payload、SHA-256、access time/class、source version 和 normalized receipt 生成。

当前共有 85 个 unique works：65 条历史保留项和 20 条 reviewer-directed additions。67 个 arXiv、17 个 ACL、1 个 GitHub identity；17 个既有 Atom raw 被复用，68 个 current raw payload 可从本地精确重放。新增 8 项只按明确 arXiv ID 获取官方 OAI 元数据，没有 discovery query；随后全部 85 项在 `network=0` 下重建，receipt SHA 与 raw bytes 一致。

`reviewer-bibliography-selection-v1.json` 对 245 个 active-union nodes 逐项执行可见谓词：所有 15 个 load-bearing/D2 works、13 个 direct system neighbors、15 个 speech/omni measurement instruments、20 个 P1/reviewer-known threats，以及 65 个冻结 carry-forward 项均有 selection basis（类别可重叠）。结果为 85 个 selected、159 个 `NOT_SELECTED_NONPRIORITY_KNOWN_QUEUE`、1 个 `NOT_SELECTED_UNRESOLVED_IDENTITY`；书目只是 reviewer orientation subset，不是 Stage-1B map denominator。此前遗漏的 Multi-Agent Verification、Thinking While Listening、Omni-Reward、Native Active Perception 已显式入书目；Llasa 进入 P1 reviewer-known，OmniGAIA、Omni-RRM、Multimodal RewardBench 2 进入不阻塞队列。

`year_basis` 年份规则也已冻结：仅有 arXiv identity 时用首次提交年 `initial_preprint`；绑定正式 venue identity 时用 `formal_venue`；GitHub 等滚动资源用 `current_version`。AudioToolAgent、VoiceAgentBench、LATS、PiCSAR 与 Trajectory Optimal Control 的已知年份错配已由 receipt 重建纠正。

这一过程不是零网络：最初一次 20-ID arXiv Atom batch 在三次尝试后收到 429；之后 endpoint probe 发现 OAI exact-ID 可用，累计只获取 50 份 arXiv OAI、17 份 ACL BibTeX 和 1 份 GitHub JSON。所有成功 known-ID access 的 `query_recall_credit=false`。失败的 429/probe 也必须进入最终 hostile ledger，不得被“离线重放成功”覆盖。

全文采用本地优先：当前已有 38 个 arXiv ID 的 38 份 PDF 与 36 份 e-print，均由 ledger SHA 绑定；后续 D2 优先解析本地 e-print/LaTeX，源不可用或需要页码证据时才用本地 PDF。网络只在精读队列 cache miss 时访问，不为书目元数据批量下载论文，也不反复访问官网。

## 15. 相对 v10 的 claim diff

| v10 claim/section | Disposition | 原因 | 当前证据 | Stage force |
|---|---|---|---|---|
| §0/§7 “E1–E5 全部关闭，可签署 Stage-1B” | `WITHDRAWN` | 后续作者外反例证明 evidence-kind compatibility、旧库 union、双平台 aggregate 和 metadata oracle 仍有假绿 | round-13/14 reviews；本表 §11–14 | readiness only |
| §2.2 absence 可由结构化字段闭合 | `CORRECTED` | 非空字段不足以证明 field-specific negative semantics；新增七字段 obligation 与 cross-binding | `sf_evidence_contract.py`; absence artifact | readiness only |
| §2.2 双平台一致 | `CORRECTED` | Windows rerun 不能代表 NT/POSIX DAG；改为两 leaf 后聚合 | preflight receipt；v7 runner/aggregator | readiness only |
| §3/§4 旧 corpus 已被当前 proposal 充分利用 | `CORRECTED` | 数量存在不等于逐 source-row routing；现改为 483-row、245-node active-corpora union，并显式否认 archive 完备性 | union graph + machine check | readiness only |
| §5.2 65-entry bibliography 足以自包含 | `CORRECTED` | 旧书目缺 direct neighbors、selection oracle 与 metadata/year oracle；现为 85-work receipt bibliography + 245-node selection disposition | receipts + bibliography + selection receipt | readiness only |
| §1 系统本身是第一创新假设 | `UNCHANGED` | 仍是待 mapping 验证的 founding hypothesis，不是 novelty claim | Project-Thesis；三条 citation chain | hypothesis only |
| §5 Stage-1B 只做 systematic mapping、禁模型/smoke | `UNCHANGED` | 阶段边界没有被技术整改改变 | current protocol/status | readiness only |
| 本文件 RQ-SUPPLY/RQ-VERIFY 的 generator-verifier-selector 分解 | `NEW` | 将 reviewer-known verification work 提出的归因风险纳入待检验问题，不改变 frozen query | bibliography roles；不计 recall | hypothesis only |

## 16. Exposure 与事故披露

本次 narrow repair 的 systematic discovery-query execution 为 0，research-model calls 为 0，smoke 为 0，dataset metric/headroom/prototype 为 0。`INHERITED_PRIOR_EXPOSURE` 保持非零，不因本轮 scoped zero 被覆盖。

known-ID metadata/provenance access 非零，详见 §14；这些访问用于身份、书目和 reviewer claim verification，不是 systematic discovery。当前 frozen query bytes 与 experiment attempt registry 相对 evidence-v6 release anchor 未改。

此前 `wiki-sync` malformed wrapper 曾进入 publish path，在临时 wiki clone 中创建 local commit 并尝试 push；push 非零失败，后续 read-only verification 证明 remote master 未改变。root cause 已修复，原生 dry-run 不再 commit/push。事故证据保存在 context-v1，不能因后续工具 PASS 被删除。

## 17. 当前 gate 状态

| Gate | 状态 | 解释 |
|---|---|---|
| cross-platform Git substrate | PASS | Windows/WSL root、HEAD、blob 和 gitfile policy 已对齐 |
| GM-1 lossless corpus union | PASS | 483 source rows / 245 nodes exactly-once；claim/work 去重且异质性保留 |
| GM-2 field-specific contract | PASS | 结构、binding 与 mutation tests 已实现 |
| GM-2 contradicted negatives | CORRECTED 3/3 | 一条改 `true`、两条改 `unknown`；均非承重且有修正台账 |
| GM-2 correction confirmation | **PENDING 0/3** | 必须由 non-implementer 核对全文 locator 与 before/after binding |
| GM-2 fresh semantic review | **PENDING 0/19 active** | 必须由 non-implementer 完成，当前阻塞 |
| GM-3 v7 code/DAG tests | PASS | leaf/aggregate 架构和 fail-closed 反例已实现 |
| GM-3 formal NT/POSIX leaves + aggregate | **WITHHELD** | 等待 3/3 corrections + 19/19 active reviewer rows 后生成 |
| GM-4 official-receipt bibliography | PASS | 85 unique works，可完全离线重建；245-node selection complement 已记账 |
| proposal source manifest/package gate | **construction=PASS / release=BLOCKED** | `proposal-source-manifest-v1.json` 绑定本提案、协议、compiler/routes/templates 与账本；`proposal-package-check.json` 只证明预审包内部一致，明确保留四个 release blockers |
| formal immutable round-16 proposal | NOT YET | round-15 已登记当前 WITHHOLD review；本文件仍是 workbench draft |
| independent search-design signoff | NOT YET | 实现者不得创建或预填 |
| owner same-package authorization | NOT YET | 必须在 reviewer SIGN 后单独发生 |
| Stage-1B | UNSTARTED / UNAUTHORIZED | 第一条 query 仍禁止 |

## 18. 给 reviewer 的明确请求

请按下列顺序作出作者外判断：

1. 在 `negative-evidence-semantic-corrections-v1.json` 的独立确认 schema 中核对三条退役修正，逐条给出 `AGREE|DISAGREE`；
2. 对 `absence-evidence-adjudication-v2.json` 的 19 条 active proof rows 做逐条 semantic adjudication；
3. 若存在 `DISAGREE`，先退回更正或将相关 row 降级，不评估旧 occupancy 是否“好看”；
4. `3/3 + 19/19` 闭合后，由团队生成 NT/POSIX leaves 和 final aggregate，并在同一 commit 上重建 final source manifest/package report；
5. 评估 Track A 是否提供了继续 systematic mapping 的充分科学理由；
6. 评估同一冻结包的 search design 是否可以签署；
7. reviewer SIGN 之后，owner 再对 exact package 单独决定是否授权 Stage-1B。

正式独立报告只应在未来 round-16 写入以下实际值：

```text
SCIENTIFIC_RATIONALE_FOR_CONTINUING_MAPPING = ADEQUATE|REVISE|INADEQUATE
SEARCH_DESIGN_SIGNOFF = SIGN|WITHHOLD
```

本 proposal 不预填答案。

## 19. 证据索引（Git blob 字节）

下列 SHA-256 都按 `git show HEAD:<path>` 的 blob bytes 计算，不使用 Windows 工作树 CRLF 变体：

| Evidence | Git blob | SHA-256 |
|---|---|---|
| `wiki/Project-Thesis.md` | `64e847f566c83b4b0f1ec9c2a6032afb8dc1a020` | `5aafddb9d32d085462f619e739cb3d1f8b47740d39d88b0cfc6b38f99e7f9623` |
| `wiki/Research-Objective.md` | `6b608c1b22b200a67376ba0cd95eadaa27c5c0ef` | `e6746c3666bbc6d8b56368d89ba0fa7710c40fa25df88a4a832c52ed64da5d95` |
| v10 proposal | `686129ee41cdf08c294114fc29c93a9c63408dc5` | `94ddfd282950ae10ca113e32e9a4ccfc702a6fa74dcd13572662e4f717b66085` |
| round-14 adversarial review | `dde66b8c50a8100eff24a2117e04966651bde3bc` | `ac61d727878d9c90ec173c4c2e12cbc6cc9ed13b60f5b8478f6d01e8fbfa28b9` |
| round-15 independent review | `d7901f85c7804bd2176aa76a0ea05bc2d79729c2` | `4068b8e5fe5590d894db93d8cf5dc7a93c827bef9c9c9aac1072873ae0a9a98e` |
| revised release design | `67ec749bd5fe7c50b9f0151d1cbb7689ccd40516` | `be2d20900093ccd070211c6083714d53e7331d05c0baa9e9e77c3899a5b23b68` |
| revised implementation plan | `a3ba7e862cac559fcce70d92b935745a662bbdc8` | `985949e178f5cef9e0e94b96629a5d9828bee70c3c82ac2074740dbde81fe840` |
| negative-evidence review artifact | `815f0f78924d7814c0ae0611fdf8e56a234e94ce` | `c62ce59a3047269fdc22e85b0bad60b3d71454cb82a9cadb2a9d7b57bfc8391f` |
| semantic-correction artifact | `b0d4fafb7ed4b5fa1f7f6e34607646168f160ca6` | `37b862ade5f3b278c52bcd1cb11f760e5d20aea8d8124ac1b1a8d21798fbcc8f` |
| lossless union graph | `ad7626092f6929890f3dbbb5b6e898e9002831e2` | `8c02bff4c4d6ec2a9c3aa096a68fd50904e94bdb7ab3da7821a4559e3db22866` |
| union machine check | `c2960fafe1a9b7818b5ca105a7d1f8f29a9c668e` | `a9dbe83115ce6ee371552764f71942767804f5de2e8ee0c9c23e77622624cfa6` |
| reviewer-known items | `2ca7c917aab1aff4bb84417276b94b54d7033f42` | `c31e924554c26be854ff469fd9a830068568bc75990721669f6e9442cdf04fd2` |
| official metadata receipts | `f34dec9703c1f11e813bbd27ab711f8d22cd4b95` | `b218bdcd13215c5b37173cca30fe5a20a4a20175035089ca1f3d84b554642778` |
| generated 85-work bibliography | `32ab190a72f0265397757377c4e6c070481a8f97` | `17670aebf8d3c80a43a3ee213bcc1169f094722efc9d1967b4e55c80f84771f6` |
| bibliography selection receipt | `87de00a3e4d8527226b1b05bd3ead330c564b974` | `deaf913d73bfe77721c651b132859c4faeead4440090bfadabfcbc14beaed1c8` |
| mapping methods adaptation | `786c579113cf318e3a0ea254cd5cce233b5c96a3` | `86325cffecad237fb772d1e3a456494ada3e90635e6f370af3ac8189864d2827` |
| speech/omni specificity codebook | `b2dcd16c08bfc53b4d7fbb5ec216a6d1c2fd1019` | `48250720ebd670156baf644cef1562ee58028d7aeb48c3d3dc7344866fa5e769` |
| current protocol | `788622b909e31e785a142fcfea51cd9d163c6970` | `0e23c262375c24cb71b2bd7aacfc5edb175ff40ab1a9900205f766fa39f3f78a` |
| current status | `cc5eff1dc12090e2ebad71479b81f18bce538f3c` | `6d3d062b45a95774c82ba588eb0a7fb08a4a7e4a8f22de43051e1d89bdda133f` |
| frozen evidence-v6 aggregate | `d3b1c67018fa9ce99dfff56af3b9404747504936` | `3a3d95cf596fbe42a763e0ba11f5e8301ddf4fb3da599d93c8c12eaadaf0a1cd` |
| frozen query bytes | `9e143e5b0054fbba9ddd65a835880bb4b66bad6d` | `645b6ffde763d554f3a7771686f054c00fb6c84a949d442a2d4f43ed885c9aab` |
| attempt registry | `9bcac7ce3681d82fd1479589d126cccc761c340e` | `f05e0efb590bf349b124dded10b682d317301c32d6911d591c3bfd12940a6ffe` |
| wiki dry-run incident | `a7f4619e8ee9de7a69dd7e37740e64f9fc5eb9d2` | `297325a2471d3d20e4a000cf88ab02122b460ae6ca6e3528fc807d929a018393` |

完整书目由 `wiki/survey/current/bibliography.md` 提供，选择账本为 `wiki/survey/current/data/reviewer-bibliography-selection-v1.json`。它们是 receipt-derived artifacts；本文件不复制 85 条引用，以避免形成第二份书目正典。

本提案的完整输入集合由 `wiki/survey/current/data/proposal-source-manifest-v1.json` 精确绑定；预审包报告为 `docs/checks/system-first-stage1a/context-v3/proposal-package-check.json`。当前报告的 `construction=PASS` 只表示输入、生成器和诚实红门可复现；`release=BLOCKED` 才是 Stage-1B 权限语义。两者不得合并为一个含糊 PASS。

## 20. 本次请求的最小结论

请不要因为技术包尚有一个诚实红门，就把研究问题本身与证据门混为同一裁决。我们请求的是：先判断继续 systematic mapping 的科学理由是否充分；核对三条语义修正并完成剩余 19 条独立 negative-evidence adjudication；再在同一冻结包上决定 search-design SIGN/WITHHOLD。

在此之前，正确状态只有：

```text
STAGE_1A_FINAL_REMEDIATION
THREE_IMPLEMENTATION_FOUNDATIONS_VERIFIED
NEGATIVE_EVIDENCE_CORRECTIONS_3_OF_3_RECORDED
NEGATIVE_EVIDENCE_CORRECTION_REVIEW_PENDING_0_OF_3
NEGATIVE_EVIDENCE_SEMANTIC_REVIEW_PENDING_0_OF_19_ACTIVE
FORMAL_ROUND_16_SUBMISSION_NOT_YET_REGISTERED
STAGE_1B_UNSTARTED_AND_UNAUTHORIZED
```
