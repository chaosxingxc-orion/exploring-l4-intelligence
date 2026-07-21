---
artifact_id: "SF-STAGE1A-REVIEWER-PROPOSAL-DRAFT-2026-07-21-02"
title: "System-first research proposal and Stage-1A remediation disclosure"
date: 2026-07-21
audience: "independent doctoral reviewer and research owner"
lifecycle: "WORKBENCH_REVIEW_DRAFT"
promotion_target: "wiki/audit/system-first-stage1a/round-16/research-proposal-and-stage1b-signoff-request.md"
promotion_trigger: "H5 second independent seven-field coding and disagreement adjudication complete; evidence-v7 contract-4 NT/POSIX leaves and aggregate PASS; exact proposal source manifest and package gate PASS"
current_stage: "STAGE_1A_FINAL_REMEDIATION"
formal_review_status: "NOT_YET_SUBMITTED_AS_IMMUTABLE_ROUND_16"
stage1b_status: "UNSTARTED_AND_UNAUTHORIZED"
systematic_discovery_queries_in_this_repair: 0
research_model_or_smoke_calls_in_this_repair: 0
remediation_evidence_commit: "eea03330f626c9979841ae60eef82a022ab01d9b"
---

# 给独立评审人的研究提案与整改说明

## 0. 请先读这一页

我们研究的对象不是一个新的声学编码器、一个更大的 verifier，或一条孤立的 reranking 技巧，而是围绕冻结黑盒 omni foundation model 的 **external reward-guided control plane**：系统在不改变核心模型权重和内部结构的条件下，管理上下文供给、外部记忆、工具与检索、候选生成、评估、选择、预算和停止动作。内部简称 training-free RL；对外表述为 *weight-frozen reward-guided inference-time optimization*。

本文件同时承担两个任务：

1. 请评审研究问题本身是否值得继续做 systematic mapping；
2. 把上一轮严厉审查之后的实际整改、仍未闭合的证据门以及 reviewer 需要完成的动作一次讲清楚。

本文件不是 reviewer verdict，也不是 Stage-1B 启动令。当前仍是 Stage-1A。第一条 systematic discovery query、任何研究模型调用、任何 smoke、指标实验或 prototype 都尚未执行且仍被禁止。

round-16 precheck 对 Track A 给出 `ADEQUATE`，但对 Track B 给出 major revision，并明确维持 search-design `WITHHOLD`。该报告对前三条修正给出 `AGREE`，对原 19 条 active negatives 给出 18 条肯定判断（16 `AGREE`、2 `AGREE_WITH_CAUTION`），同时对 DeepVerifier closed path 的 `human_or_dev_label_model_selection=false` 给出 `DISAGREE`。我们已接受该反例，把该字段改为 `unknown`，形成 **exactly 4/22 semantic corrections**。版本化库存现在是 **`22 = 4 + 18`**：`negative-evidence-semantic-corrections-v2.json` 有 4 个 correction rows、4 个 reviewer rows；`absence-evidence-adjudication-v3.json` 有 18 个 proof rows、18 个 reviewer rows，coverage 18/18。语义门在当前工作树中闭合，但这不是对未来 exact package 的 reviewer SIGN。

precheck 新识别的真实发布阻塞项是 H5 校准和提取环境可复现性。三篇校准全文已按 SHA 本地冻结，implementer coder A 完成 21 个字段赋值；**H5 calibration status=PENDING_SECOND_INDEPENDENT_CODER**，planned denominator=21，observed comparable denominator=0。第二位独立 coder 未完成前，任何 H5 值都不承重。PDF 提取契约已冻结为 NT Python 3.14.3 / pypdf 6.14.0 与 POSIX Python 3.12.3 / pypdf 6.14.2，并要求两端重放 ToolGate p11。因 H5 仍为红门，正式 v7 leaves/aggregate、immutable round-16 包、同包独立签署和 owner 授权均尚未发生。

## Track A — 科学提案

## 1. 中心问题

现代 omni / multimodal LLM 在预训练中吸收了大量跨模态、跨任务、不同粒度的知识，但默认推理并不总能稳定地把这些知识转化为正确的语音和音频任务行为。本项目的中心问题是：

> 在核心模型保持黑盒、权重冻结且内部结构不变时，reward-guided 的外部控制系统能够在多大程度上激活其已有知识，并把这种提升做成可验证、可归因、可停止且不越过信息边界的推理过程？

这里的 “RL” 指 reward/advantage 对下一步外部动作的控制，而不限定为权重更新。best-of-N、MBR 和 reranking 是终端动作空间退化后的特例；完整研究对象还包括观察与供给构造、状态、记忆、工具、候选扩展、验证、回退、停止和风险控制。

## 2. 为什么要先做 system-first mapping

直接相邻的 speech/omni agent、工具编排和 trained speech reward 工作已经存在。当前 reviewer bibliography 已显式路由 AudioToolAgent、Audio-Mind、Agent-Omni、EChO-Agent、AuTAgent、Speech-Copilot、VoxMind、Thinking While Listening、Native Active Perception、Llasa、OmniGAIA、WavReward、GSRM、Omni-RRM 和 Multimodal RewardBench 2；本轮又处置了 Sandboxed Coding Agents are Competitive Omni-modal Task Solvers、Inference-Time Scaling for Joint Audio-Video Generation、Agentic Reward Modeling、TMAS 与 AgentTTS。reward/verification 与 training-free/trained boundary 也分别形成可见链条。它们证明这一问题空间并不空白，也因此使任何 “first-ever” 或已确立 novelty 的说法都不成立。

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

执行只使用现已冻结的 query/compiler、T1 route、seed/citation-chaining 入口、REC-0 至 REC-7 模板和 current protocol。方法适配由 `wiki/survey/current/mapping-methods-adaptation.md` 冻结；H5 编码由 `wiki/survey/current/modality-specificity-codebook.md` 冻结，校准状态由 `wiki/survey/current/data/modality-specificity-calibration-v1.json` 单独承载；PDF 解析环境由 `wiki/survey/current/data/pdf-extractor-environment-v1.json` 精确约束。现有 query 文件保持在 `wiki/survey/2026-07-15-sf-queries.jsonl`；本轮整改没有增加 lane、改写 query term 或执行任何一条 query。

当前共登记 15 reviewer-known items。已知论文、reviewer-known items 和历史 corpus 只能作为带 provenance 的入口或 comparator，`query_recall_credit=false`；它们不得被反向计作 frozen query 的召回结果。

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
| `f3923c1`, `32e4c52` | 接受第四条 reviewer `DISAGREE`、迁移为 `22 = 4 + 18`、增加 counterevidence 合同、H5 三篇校准与双平台 extractor contract、处置 5 条 reviewer-known works，并修复审计登记表的原子追加 | 语义审查、环境合同与 82-row audit immutability PASS；H5 仅 coder A 完成 |
| `3e42565`, `d8e5b90` | 将可编辑 reviewer brief 与 immutable audit artifact 分离；workbench 文件名不再冒充 proposal/review 审计件 | AI 默认加载面不再把工作稿误判为冻结评审产物 |
| `23129f4`, `2060109` | 切断 current-package report → current/AI manifest → current-package report 的 SHA 自引用，并按无环依赖顺序重冻 source/package/current reports | deterministic current-package `--check` PASS；不再以无法存在的哈希固定点制造假绿 |
| `eea0333` | 移除热层中的旧 v6 commit 与事故叙事，更新 Per-Work 到 round-16 precheck 的 H5/v7/authorization 真相 | AI context manifest 与 122 项加载面政策测试 PASS；事故细节仍在冷审计证据中 |

## 11. GM-1：claim/work 去重和旧库无损桥接

机器报告 `docs/checks/system-first-stage1a/context-v2/existing-corpus-disposition-check.json` 当前为 PASS：494 个物理 source rows 被恰好路由到 250 个 canonical work nodes；其中 census 95、seed 92、bibliography 65、claim 62、version-pin 30、fulltext events 135、reviewer-known 15。相对 precheck 冻结点只增加 5 条 reviewer-known source rows、6 条三篇校准论文的 PDF/eprint 本地访问事件和 5 个 canonical nodes。两条 source-metadata row 仍保留为 source metadata，不伪装成 work。GM-1 的语义严格限于 **seven registered active corpora 的 lossless union**，不是 archive 或全部历史语料已经完备利用的声明。

claim 去重采用“work node + claim hyperedge”，不是“每个 claim 复制一个种子”：62 条 claim row 保留 75 个 work references，去重后为 44 个 work references、31 个 unique claim works，且没有 claim target 游离在 census 之外。92 条 seed 是 92 个 unique works，没有 duplicate seed source row；其中 13 条复用已经存在的 census canonical work，generated seed rows 为 0。

异质性没有被 best/worst 聚合吞掉：16 个 work 有多个 claim，15 个 work 有多个 evidence grade，12 个 work 有多个 discrepancy status，5 条 claim edge 指向多个 work。一个非承重旧 IEEE identity 保持 unresolved；load-bearing unresolved 为 0。`unexplained_orphans=0` 只表示每条 source row 有解释，不表示全部论文已验证或深读。

## 12. GM-2：negative evidence 合同与尚未完成的独立复核

旧实现允许 `absence` 与任意字段值组合，理论上能让正向类别依靠“未见反证”通过。现合同只允许七个实际观察到的负值组合，并强制：proof obligation、检查位置、reason、全文 identity/SHA、owner method path、owner sidecar、coder、owner row SHA 和 adjudication row ID。

cross-binding validator 会拒绝 wrong fulltext hash、wrong sidecar、wrong row hash、artifact 缺 row、非肯定 verdict、URL 代替全文版本、弱 `not contradicted`、空缺/unknown 冒充 absence，以及 coder/adjudicator actor collision。每条 negative proof 现在还必须登记 counterevidence search scope、counterevidence locators、时间顺序是否解析，以及反证为何不改变结论；`AGREE_WITH_CAUTION` 被保留为肯定但带限制的独立判断，不被静默改写成无条件 `AGREE`。

机器只能证明绑定一致，不能自行制造人员独立性。round-16 precheck 已对前三条修正给出 `AGREE`，并对原 19 条 active proof rows 给出 18 条肯定与 1 条 `DISAGREE`。我们没有把该 `DISAGREE` 强行转成同意：DeepVerifier closed path 的旧 `false` 被退役并按 reviewer 要求改为 `unknown`。`negative-evidence-semantic-corrections-v2.json` 逐条绑定四个旧 ID、旧/新 row hash、全文 SHA、证据 locator、退役原因和作者外决定；`absence-evidence-adjudication-v3.json` 只保留 18 条 active proofs 与对应 18 条 review rows。当前恒等式为 `22 = 4 + 18`，两边 coverage 均完整，v7 的 `SEMANTIC_CORRECTION_REVIEW` 与 `ABSENCE_REVIEW` 已关闭。

这些决定绑定的是 precheck 冻结对象，不等于未来正式发布包的 search-design SIGN。final exact-package reviewer 仍须验证 recode、row hash、counterevidence 字段和 reviewer decisions 在正式 commit 中未漂移，但不得要求把第四条退役命题重新放回 active absence 库。

## 13. GM-3：真实双平台证据 DAG

旧流程在 POSIX 输出前生成所谓 aggregate，实际上只是第二次 Windows 运行。现在两端 runner 只能各写自己的 leaf，独立 aggregator 必须最后读取两份 exact bytes，并核对 input snapshot、runner hash、contract version、platform stamp、named failures、occupancy 和 output semantics。删除或替换任何 leaf、改变输入 hash、平台角色或 occupancy 都会 fail closed。

跨平台 Git preflight 已证明 Windows 与 WSL2 Ubuntu-24.04 能直接解析同一 linked worktree；不再依靠临时 wrapper。v7 已升级为 contract-4，输入快照纳入 H5 calibration 与 extractor contract；平台 stamp 记录精确 Python、pypdf 和 extractor identity，并在每片 leaf 显式重放 ToolGate p11。当前本地 probe 除 `H5_CALIBRATION` 外为 7/8 PASS。正式 leaves 尚未生成，因为第二位 H5 独立 coder 和分歧裁决未完成；我们不会把带 FAIL 的运行包装成双平台发布证据。

## 14. GM-4：书目证据、系统主线和本地优先

旧 bibliography 的 title/authors 常量同时充当 generator 输入和 test oracle，存在一起写错却全绿的循环。现在每一条由官方 raw payload、SHA-256、access time/class、source version 和 normalized receipt 生成。

当前共有 90 个 unique works：72 个 arXiv、17 个 ACL、1 个 GitHub identity。相对上一版只为 5 个 reviewer 明示 arXiv ID 获取小型 OAI metadata；其余 85 个 receipt 全部复用本地缓存。随后全部 90 项在 `network=0` 下重建，receipt SHA 与 raw bytes 一致。

`reviewer-bibliography-selection-v1.json` 对 250 个 active-union nodes 逐项执行可见谓词，结果为 90 个 selected：15 个 `SELECTED_LOAD_BEARING_OR_D2`、14 个 `SELECTED_DIRECT_SYSTEM_NEIGHBOR`、11 个 `SELECTED_P1_OR_REVIEWER_KNOWN_THREAT` 与 50 个冻结 carry-forward；另有 159 个 `NOT_SELECTED_NONPRIORITY_KNOWN_QUEUE`、1 个 `NOT_SELECTED_UNRESOLVED_IDENTITY`。书目只是 reviewer orientation subset，不是 Stage-1B map denominator。新增五项中，Sandboxed Coding Agents 完成 D1 direct/H5 threat 路由；Inference-Time Scaling for Joint Audio-Video Generation 与 Agentic Reward Modeling 作为 measurement/reward comparators；TMAS 与 AgentTTS 为非阻塞 P2 queue，且五项全部 `query_recall_credit=false`。

`year_basis` 年份规则也已冻结：仅有 arXiv identity 时用首次提交年 `initial_preprint`；绑定正式 venue identity 时用 `formal_venue`；GitHub 等滚动资源用 `current_version`。AudioToolAgent、VoiceAgentBench、LATS、PiCSAR 与 Trajectory Optimal Control 的已知年份错配已由 receipt 重建纠正。

这一过程不是零网络：最初一次 20-ID arXiv Atom batch 在三次尝试后收到 429；之后 endpoint probe 发现 OAI exact-ID 可用，累计只获取 50 份 arXiv OAI、17 份 ACL BibTeX 和 1 份 GitHub JSON。所有成功 known-ID access 的 `query_recall_credit=false`。失败的 429/probe 也必须进入最终 hostile ledger，不得被“离线重放成功”覆盖。

全文采用本地优先：当前 ledger 有 41 个成功 arXiv ID、41 份 PDF 与 39 份 e-print，均由 SHA 绑定；H5 三篇校准论文的 PDF/eprint 已一次性缓存到 E: 数据层。后续 D2 优先解析本地 e-print/LaTeX，源不可用或需要页码证据时才用本地 PDF。网络只在精读队列 cache miss 时访问，不为书目元数据批量下载论文，也不反复访问官网。

## 15. 记录层与总包验证修复

precheck 之后的回归暴露了两处与研究结论无关、却会污染发布证据的工具链错误。第一处是 audit registry 虽声明允许 `HEAD+1`，实际却要求新增 review 已经存在于 HEAD，导致 review、registry 和 anchor 无法在同一提交原子落地。现在只有在完整保留 HEAD prefix、只追加一个 suffix、且该 suffix 的 stage-0 blob 与工作树字节精确一致时，新增 review 才可 staged-only；旧行改写、重排、删行、一次增长两行和 pin mutation 仍全部 fail closed。

第二处更严重：`current-package-check.json` 曾同时被 current manifest 和 AI manifest 当作输入，而 current-package 自己又运行这两个 manifest 的检查。这构成 cryptographic self-reference——报告哈希改变 manifest，manifest 改变报告，因而不存在可验证固定点。继续“重刷哈希”只能得到暂时假绿。修复后，总包报告不再作为自身命令图的输入；它仍由 deterministic `sf_current_package_check.py --check` 对 exact code graph 与命令输出独立验证。current manifest、AI manifest、proposal source manifest 和 proposal package report 按有向无环顺序生成并在提交后只读重放。

总包命令也已从会覆盖冻结 v6 输出的 legacy runner 升级为只读 v7/H5/PDF、active-union、bibliography 与当前 manifest tests。最终 Windows current package、proposal source manifest、proposal construction、AI context、current manifest 与 audit immutability 全部 PASS；WSL2 Ubuntu-24.04 在 Python 3.12.3 / pypdf 6.14.2 下的 PDF、H5 和 v7 harness 共 21 项测试 PASS。v7 probe 的唯一 named failure 仍是 `H5_CALIBRATION`，这正是预期的诚实红门。

记录层同时完成语义清理：可编辑文件保留在 `wiki/survey/workbench/`，只有冻结且登记的正式评审件进入 `wiki/audit/`；旧 commit、旧 v6 gate 和 publication-incident 细节不再占用默认热层，但对应 evidence 未被删除。该清理减少 AI 上下文中的限定语堆叠，不改变任何历史事实。

## 16. 相对 v10 的 claim diff

| v10 claim/section | Disposition | 原因 | 当前证据 | Stage force |
|---|---|---|---|---|
| §0/§7 “E1–E5 全部关闭，可签署 Stage-1B” | `WITHDRAWN` | 后续作者外反例证明 evidence-kind compatibility、旧库 union、双平台 aggregate 和 metadata oracle 仍有假绿 | round-13/14 reviews；本表 §11–14 | readiness only |
| §2.2 absence 可由结构化字段闭合 | `CORRECTED` | 非空字段不足以证明 field-specific negative semantics；新增七字段 obligation 与 cross-binding | `sf_evidence_contract.py`; absence artifact | readiness only |
| §2.2 双平台一致 | `CORRECTED` | Windows rerun 不能代表 NT/POSIX DAG；改为两 leaf 后聚合 | preflight receipt；v7 runner/aggregator | readiness only |
| §3/§4 旧 corpus 已被当前 proposal 充分利用 | `CORRECTED` | 数量存在不等于逐 source-row routing；现改为 494-row、250-node active-corpora union，并显式否认 archive 完备性 | union graph + machine check | readiness only |
| §5.2 65-entry bibliography 足以自包含 | `CORRECTED` | 旧书目缺 direct neighbors、selection oracle 与 metadata/year oracle；现为 90-work receipt bibliography + 250-node selection disposition | receipts + bibliography + selection receipt | readiness only |
| §1 系统本身是第一创新假设 | `UNCHANGED` | 仍是待 mapping 验证的 founding hypothesis，不是 novelty claim | Project-Thesis；三条 citation chain | hypothesis only |
| §5 Stage-1B 只做 systematic mapping、禁模型/smoke | `UNCHANGED` | 阶段边界没有被技术整改改变 | current protocol/status | readiness only |
| 本文件 RQ-SUPPLY/RQ-VERIFY 的 generator-verifier-selector 分解 | `NEW` | 将 reviewer-known verification work 提出的归因风险纳入待检验问题，不改变 frozen query | bibliography roles；不计 recall | hypothesis only |

## 17. Exposure 与事故披露

本次 narrow repair 的 systematic discovery-query execution 为 0，research-model calls 为 0，smoke 为 0，dataset metric/headroom/prototype 为 0。`INHERITED_PRIOR_EXPOSURE` 保持非零，不因本轮 scoped zero 被覆盖。

known-ID metadata/provenance access 非零，详见 §14；这些访问用于身份、书目和 reviewer claim verification，不是 systematic discovery。当前 frozen query bytes 与 experiment attempt registry 相对 evidence-v6 release anchor 未改。

此前 `wiki-sync` malformed wrapper 曾进入 publish path，在临时 wiki clone 中创建 local commit 并尝试 push；push 非零失败，后续 read-only verification 证明 remote master 未改变。root cause 已修复，原生 dry-run 不再 commit/push。事故证据保存在 context-v1，不能因后续工具 PASS 被删除。

## 18. 当前 gate 状态

| Gate | 状态 | 解释 |
|---|---|---|
| cross-platform Git substrate | PASS | Windows/WSL root、HEAD、blob 和 gitfile policy 已对齐 |
| GM-2 field-specific contract | PASS | 结构、binding 与 mutation tests 已实现 |
| GM-1 lossless corpus union | PASS | 494 source rows / 250 nodes exactly-once；claim/work 去重且异质性保留 |
| GM-2 contradicted negatives | CORRECTED 4/4 | 一条改 `true`、三条改 `unknown`；全部退出 active absence |
| GM-2 correction decisions | PRECHECK RECORDED 4/4 | 三条 `AGREE`、一条 `DISAGREE_RECODE_REQUIRED` 已原样绑定；正式同包核验仍待未来 reviewer |
| GM-2 active semantic review | PRECHECK RECORDED 18/18 | 16 `AGREE`、2 `AGREE_WITH_CAUTION`；counterevidence 字段已加入合同 |
| H5 three-paper calibration | **PENDING CODER B** | coder A 21/21；第二位独立 coder、agreement 21-field denominator 与分歧裁决尚缺 |
| PDF extractor replay contract | PASS | NT pypdf 6.14.0 / POSIX pypdf 6.14.2 exact-match；ToolGate p11 为双叶强制 probe |
| GM-3 v7 contract-4 code/DAG tests | PASS | 当前单平台 probe 仅 H5 红；leaf/aggregate fail-closed 反例已实现 |
| GM-3 formal NT/POSIX leaves + aggregate | **WITHHELD** | 等待 H5 dual coding 完整后在同一 commit 生成 |
| GM-4 official-receipt bibliography | PASS | 90 unique works，可完全离线重建；250-node selection complement 已记账 |
| audit/context lifecycle | PASS | 82-row registry 原子追加、workbench/audit 分流、AI context surface 0 failures |
| deterministic current package | PASS | 自引用已切断；提交后 Windows `--check` 可只读重放 |
| proposal source manifest/package gate | **construction=PASS / release=BLOCKED** | `proposal-source-manifest-v1.json` 绑定本提案、协议、compiler/routes/templates、H5、extractor 与账本；`proposal-package-check.json` 只证明预审包内部一致，不替代 H5、formal review 或 owner authorization |
| formal immutable round-16 proposal | NOT YET | round-16 precheck 是外部输入；本文件仍是 workbench brief，不冒充同包正式 review |
| independent search-design signoff | NOT YET | 实现者不得创建或预填 |
| owner same-package authorization | NOT YET | 必须在 reviewer SIGN 后单独发生 |
| Stage-1B | UNSTARTED / UNAUTHORIZED | 第一条 query 仍禁止 |

## 19. 给 reviewer 的明确请求

剩余动作必须按以下顺序完成：

1. 第二位独立 coder 在看不到 coder A 值的条件下，对 `modality-specificity-calibration-v1.json` 绑定的三篇冻结全文完成 3×7 字段编码；
2. 计算 exact field agreement；每个 disagreement 由不属于两位 coder 的 adjudicator 给出 final value、理由和 locator；
3. H5 完成后，由团队在冻结同一 commit 上分别生成 NT/POSIX contract-4 leaves；两端必须精确匹配各自 extractor contract 并重放 ToolGate p11，再生成 aggregate；
4. 重建 source manifest/package report，通过敌意内审后才晋升为 immutable round-16 proposal；
5. final exact-package reviewer 复核第四条 recode、18 条 active decisions、五条 reviewer-known dispositions、H5 和双平台 receipts，再决定 search design 是否可以签署；
6. reviewer SIGN 之后，owner 才对 exact package 单独决定是否授权 Stage-1B。

正式独立报告只应在未来 round-16 写入以下实际值：

```text
SCIENTIFIC_RATIONALE_FOR_CONTINUING_MAPPING = ADEQUATE|REVISE|INADEQUATE
SEARCH_DESIGN_SIGNOFF = SIGN|WITHHOLD
```

本 proposal 不预填答案。

## 20. 证据索引（Git blob 字节）

下列 SHA-256 都按 `git show HEAD:<path>` 的 blob bytes 计算，不使用 Windows 工作树 CRLF 变体：

| Evidence | Git blob | SHA-256 |
|---|---|---|
| `wiki/Project-Thesis.md` | `64e847f566c83b4b0f1ec9c2a6032afb8dc1a020` | `5aafddb9d32d085462f619e739cb3d1f8b47740d39d88b0cfc6b38f99e7f9623` |
| `wiki/Research-Objective.md` | `4ae23baec5f8a51672fdfc60329972df0e99a27e` | `aa836540d210ca406c69eacb2f7b7b6490ff2aca85c516892174a4bd3369badc` |
| v10 proposal | `686129ee41cdf08c294114fc29c93a9c63408dc5` | `94ddfd282950ae10ca113e32e9a4ccfc702a6fa74dcd13572662e4f717b66085` |
| round-14 adversarial review | `dde66b8c50a8100eff24a2117e04966651bde3bc` | `ac61d727878d9c90ec173c4c2e12cbc6cc9ed13b60f5b8478f6d01e8fbfa28b9` |
| round-15 independent review | `d7901f85c7804bd2176aa76a0ea05bc2d79729c2` | `4068b8e5fe5590d894db93d8cf5dc7a93c827bef9c9c9aac1072873ae0a9a98e` |
| round-16 precheck rereview | `f8b173afba280fb97220bd29c66cb5418022e3db` | `7aec58152c3d57826d230551eab3d0c409f49394a660fd268a6ba58c826fcc1a` |
| revised release design | `67ec749bd5fe7c50b9f0151d1cbb7689ccd40516` | `be2d20900093ccd070211c6083714d53e7331d05c0baa9e9e77c3899a5b23b68` |
| revised implementation plan | `a3ba7e862cac559fcce70d92b935745a662bbdc8` | `985949e178f5cef9e0e94b96629a5d9828bee70c3c82ac2074740dbde81fe840` |
| negative-evidence review artifact | `372cb60c3936cdf9ba40452d749fb31c88b735fc` | `4f96dc55f4e7c8cd6eef4df700e0e73807f6d25748fc23479b24cf11bf8bf264` |
| semantic-correction artifact | `a5c963098cd8a7ef8a8e60febd9a231da45fa7e0` | `6b48a26212a0593abfc8e7b0a762826676ee6118f6313c47626f5f876bd349a3` |
| lossless union graph | `f4c97f2264bb180f51cc952e5fa88d3f135883f4` | `2e562049f8589aedb38a881b041b42e19278d77f4d0614e6ac830f84bce76024` |
| union machine check | `1c19671f3b731946f34670ad94cbbb2b1e043716` | `67d6795e3ce0e851a320e6f85ba50ab05c6a2f8ddd98128d4d28ce711054cab4` |
| reviewer-known items | `44e5bc36db70d0de551934e02fc8e9ff5bea222b` | `7439bc0bd6f9e4bb834f27fac0939535c499f5f6755d57964d6d369a8c6f5a24` |
| official metadata receipts | `af93661d7abc640de68a7fa5c81b533aac5c6c50` | `9c3ca6f466940e964fe05961d06d55ed45630b3c44bba441289424e18f4e3468` |
| generated 90-work bibliography | `1adab73af8f80efd9db7f7559d00e6e606f12b4c` | `23ab2bf25e4e11607ddf8475862d96849729c5643ba347e2e3379b01cd3e92c9` |
| bibliography selection receipt | `93edab407964d2d478dad1b33bab4f1114034d1c` | `faf78d691cfc1200571a60b526d767c0975b7538b487b28f4fecd1320fd7f032` |
| mapping methods adaptation | `786c579113cf318e3a0ea254cd5cce233b5c96a3` | `86325cffecad237fb772d1e3a456494ada3e90635e6f370af3ac8189864d2827` |
| speech/omni specificity codebook | `9bda0d76328de360b9b0851d0f50b579af79a7b1` | `db860023cb42a9deb6dc789b8cb3a93e7a10bc791568bc0c8bc8a70880018999` |
| H5 calibration artifact | `4e699b9565e9ed88e4400cc78725fa1dfb8eda11` | `72f70bccf23287a62bda43f3b386effcaecf439e5a8a4a0225f75a534bbee361` |
| PDF extractor environment | `0bfe53b1a72268e315630c4050809c1bb9e10987` | `d982a22e2702cc670ac9a3b90d3dfeaab33e1cde2df3518dc98f1a55b9845a19` |
| current protocol | `bca3c0a661d69ee53625d73797c90d969d5cdc95` | `e5ee5c7f47ca881a1d1a66a48b9bd0f72b93631016526fb8164fde997e8a2585` |
| current status | `fc461f1d649f177c8cd6b3cd5b6056270fbcb660` | `7a9af855bb1b374a978b9564d69ea3791d6fea14b2daf0ec654904fb4ac19499` |
| frozen evidence-v6 aggregate | `d3b1c67018fa9ce99dfff56af3b9404747504936` | `3a3d95cf596fbe42a763e0ba11f5e8301ddf4fb3da599d93c8c12eaadaf0a1cd` |
| frozen query bytes | `9e143e5b0054fbba9ddd65a835880bb4b66bad6d` | `645b6ffde763d554f3a7771686f054c00fb6c84a949d442a2d4f43ed885c9aab` |
| attempt registry | `9bcac7ce3681d82fd1479589d126cccc761c340e` | `f05e0efb590bf349b124dded10b682d317301c32d6911d591c3bfd12940a6ffe` |
| wiki dry-run incident | `a7f4619e8ee9de7a69dd7e37740e64f9fc5eb9d2` | `297325a2471d3d20e4a000cf88ab02122b460ae6ca6e3528fc807d929a018393` |

完整书目由 `wiki/survey/current/bibliography.md` 提供，选择账本为 `wiki/survey/current/data/reviewer-bibliography-selection-v1.json`。它们是 receipt-derived artifacts；本文件不复制 90 条引用，以避免形成第二份书目正典。

本提案的完整输入集合由 `wiki/survey/current/data/proposal-source-manifest-v1.json` 精确绑定；预审包报告为 `docs/checks/system-first-stage1a/context-v3/proposal-package-check.json`。当前报告的 `construction=PASS` 只表示输入、生成器和诚实红门可复现；`release=BLOCKED` 才是 Stage-1B 权限语义。两者不得合并为一个含糊 PASS。

## 21. 本次请求的最小结论

precheck 已判断继续 systematic mapping 的科学理由充分；当前请求不是重复评审 Track A，而是完成唯一尚缺的 H5 coder-B／adjudication，生成精确 v7 双平台证据，再让独立 reviewer 对同一 immutable package 作最终 search-design SIGN/WITHHOLD。任何一步都不能由实现者自签替代。

在此之前，正确状态只有：

```text
STAGE_1A_FINAL_REMEDIATION
ROUND16_PRECHECK_TRACK_A_ADEQUATE_TRACK_B_MAJOR_REVISION
NEGATIVE_EVIDENCE_VERSIONED_INVENTORY_22_EQUALS_4_PLUS_18
NEGATIVE_EVIDENCE_PRECHECK_DECISIONS_RECORDED_4_PLUS_18
H5_CALIBRATION_CODER_A_COMPLETE_CODER_B_PENDING
PDF_EXTRACTOR_ENVIRONMENT_FROZEN
FRESH_V7_DUAL_PLATFORM_RELEASE_EVIDENCE_PENDING
FORMAL_ROUND_16_SUBMISSION_NOT_YET_REGISTERED
STAGE_1B_UNSTARTED_AND_UNAUTHORIZED
```
