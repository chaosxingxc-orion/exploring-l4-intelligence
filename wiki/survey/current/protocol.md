---
protocol_id: SF-SYSTEM-FIRST-STAGE1B
protocol_version: 3
effective_date: 2026-07-21
stage: Stage-1B systematic mapping
execution_authorized: true
authorization_commit: c01fba751b56588ed2f62cb6d01f6c25f3e95539
h5_load_bearing_use: WITHHOLD
supersedes_effective_chain: protocol-v1 plus amendments 1 and 3-15
audit_index: wiki/audit/system-first-stage1a/INDEX.md
---

> **Stage closeout note (2026-07-25):** Stage‑1B is closed and this protocol is retained as the
> evidence/provenance basis for its fixed v5 release. Its historical execution authority does not
> describe the current gate. Stage‑1C selected `C1_DECISION_CALIBRATED_REWARD`; current authority and
> the Stage‑2A boundary are self-contained in `status.md` and
> `tables/stage1c-common-rubric-comparison.md`.

# System-first systematic-mapping protocol v3

This file is the complete effective specification for the system-first mapping campaign. Historical
transactions are provenance, not operating prerequisites. The rules below are sufficient to decide
scope, compile the frozen query set, screen and code records, account for exposure, produce reports,
correct errors, and determine who may authorize execution or sign-off.

## §0 Authority, current gate, and prohibited execution

The current state is **Stage-1B systematic-mapping execution**. The independent 2026-07-21 fast-
convergence review signed the search design against commit
`c01fba751b56588ed2f62cb6d01f6c25f3e95539`; the owner then explicitly directed Stage-1B planning and
research execution on 2026-07-21. The authorization is deliberately split:

- frozen discovery queries, T1 routes, identity/deduplication, REC-0 screening, citation traversal,
  non-H5 method-path coding, D2 full-text work, and ordinary mapping synthesis are authorized;
- H5 calibration may continue in parallel, but `H5_LOAD_BEARING_USE=WITHHOLD` until the independent
  blind coder-B pass and third-party adjudication finish;
- the older fresh-v7/package-promotion work remains a record-layer closeout and does not block the
  authorized non-H5 mapping operations.

This v3 authority rule supersedes the v2 requirement that the full H5/package-release chain pass
before the first query. It implements the independent review's scoped sign-off rather than treating
a non-load-bearing calibration as a global search-recall gate. It does not weaken any H5 conclusion:
before calibration closes, H5 values may not enter an occupancy denominator, headline, gap claim, or
Stage-1C input.

Stage-1B means systematic-mapping execution. **Stage-1B runs no research model or smoke** and, more
explicitly, no research-model call, model smoke, dataset inference/metric experiment, headroom test,
or directional prototype may run anywhere in this stage. The execution receipt must bind the
authorization commit, frozen protocol/query hashes, actor, platform, exposure declaration, and
`H5_LOAD_BEARING_USE=WITHHOLD` before the first discovery request.

No document, generated PASS, correction, internal review, or protocol consolidation may self-grant
execution authority. The authority here comes from the independent search-design `SIGN` plus the
owner's subsequent execution direction; internal convergence and machine PASS remain non-authority.

The historical Stage-1B meaning of directional prototyping is retired. Directional prototype work is
**Stage-2A reproduction-first** work and this protocol gives it **no present execution force**.
Stage-1C owns problem selection and candidate gap hypotheses, not technical-innovation convergence.
Stage-1A performs identity, routing, and protocol-coverage checks; Stage-1B maps method-path facts and
proximity. Neither stage may turn those facts into an innovation verdict or require a technical-
difference matrix. Technical-approach innovation converges only after nearest-prior reproduction and
exploration in Stage-2A, and is validated in Stage-2B.

The package attestation at this gate is `discovery_queries_executed = 0` and
`research_model_or_smoke_executions = 0` for this remediation. Those scoped counts do not erase the
nonzero historical exposure defined in §8.

## §1 Research questions and scope

The core topic is **how to build omni agentic system**, including multimodal knowledge systems, with
**speech** as the primary modality. Every record receives `topic_relevance ∈ {core, element}`:
`core` covers speech/omni agentic systems themselves; `element` covers transferable results from
other modalities or single-modality systems. This priority affects reading and reporting, not search
breadth.

The mapping covers four system domains—text agents, VLM/omni agents, audio agents, and compound AI
systems—and the mechanism families search, reflection, memory, tool routing, verification, and
non-parametric adaptation. It includes training-free methods and the strongest trained comparators.
The research-question frame is:

- `RQ-SYS`: what external control-plane structures can turn feedback into a causally linked next-step
  action while the core stays frozen;
- `RQ-CTRL`: what matched-control, alternative-explanation, and negative-result evidence can falsify
  claimed controller gains;
- `RQ-OMNI`: where modality-native observation, action, tool I/O, and causal grounding matter;
- `RQ-SAFE`: where Goodhart effects, judge drift, abstention, stopping, and reward hacking constrain
  inference-time control;
- `RQ-MEASURE-MAP`: which papers report candidate-supply conditions, pool construction, verifier
  evidence, selector baselines, budgets, and modality coverage, and at what evidence grade. Stage-1B
  maps these reported constructs; it does not measure new headroom or run attribution experiments.

The empirical questions—whether a fixed supply has oracle headroom, whether a label-free selector
beats equal-K MBR, and how gain decomposes across generator/verifier/selector—are Stage-2 questions.
They may be recorded as future falsifiers in Stage-1B evidence bundles but cannot be answered by this
mapping or presented as Stage-1B outputs.

Each included method path records `most_threatened_rq` as one or more of those identifiers; `none`
requires a reason. Mapping reports must separate system-level occupancy, component priors, measurement
instruments, trained comparators, boundary cases, and negative-result priors. A term being occupied is
not a kill result: only a method with no valuable improvement space can support a pivot. No
intersection-novelty conclusion is an output of this protocol.

The program umbrella is weight-frozen reward-guided inference-time optimization around an external
control plane. Candidate identities are analysis labels until Stage-1C:

- `UMBRELLA`: frozen omni core plus an advantage/feedback signal that affects a next-step action;
- `I1`: a general label-free selector, treated as an occupied terminal-selection baseline;
- `bare-I2`: an audio-grounded evaluator mechanism; coverage may be mixed or under-searched;
- `strict-I2`: the post-hoc `I2 ∩ I4` component hypothesis, never described as a survivor;
- `I3`: safety, Goodhart, abstention, and stopping mechanisms;
- `I4`: an occupied method family whose audio/omni supply-layer instantiation remains a measurement
  question.

## §2 Unit of analysis and method-path identity

The bibliographic work is the deduplication unit; the **method path** is the coding and occupancy unit.
One paper may yield multiple method paths when training, information access, topology, lifecycle, or
selection behavior differs. A mixed-path paper must be split rather than averaged. Counts always state
both path and unique-work denominators, and a `selection_object` analysis is never aggregate across
pool types such as output, trajectory, tool, branch, or synthesis-input pools.

Every path has stable `paper_work_id`, `method_path_id`, `canonical_record_id`, source lineage, and a
full-text binding. Component paths used only inside a pipeline carry `component_path_ids`; they are not
also counted as independent deployed methods unless the evidence supports that unit. The work ledger
retains all source hits and dedup provenance even when a path is excluded.

Core topology is coded explicitly. Under topology policy A, repeated calls or multiple roles backed by
the **same frozen core** count as a single-core external orchestration; a federation of distinct model
weights does not. Reports also persist a **strict-topology sensitivity** column so Stage-1C can inspect
the alternative interpretation without recoding source facts.

System identity is not inferred from titles such as “training-free,” “RL,” or “agentic.” The coding
records weights, component training, signal lifecycle, action and state definitions, decision rights,
information access, topology, modality, and causal control edges. A terminal selector is a degenerate
control mechanism, not evidence of sequential control by itself. Unknown values never satisfy a
strict conjunction.

Speech/omni specificity uses the separate current codebook
`wiki/survey/current/modality-specificity-codebook.md`. Its seven mandatory fields are modality
topology, temporal regime, observation granularity, acoustic evidence provenance, latency/action
timing, output/action modality, and state persistence. Each has explicit `UNKNOWN` and
`NOT_APPLICABLE` handling, field-level dual coding, and disagreement adjudication. A generic
`core_native_modality` value cannot substitute for this H5-specific coding.

## §3 Sources, dates, coverage lanes, and access logging

The methodological adaptation is frozen in
`wiki/survey/current/mapping-methods-adaptation.md`: Petersen supplies mapping/classification
discipline, Wohlin supplies snowballing and stop logic, PRISMA 2020 supplies flow transparency, PRESS
2015 supplies pre-execution search peer review, and PRISMA-S supplies reproducible search reporting.
The adaptation table states every adopted element, AI/CS/arXiv/T1 deviation, rationale, and artifact.

The discovery universe is an **arXiv-primary systematic mapping** with **free official source rescue**.
The 65 frozen Boolean requests use arXiv API metadata. T1 proceedings and citation indexes are
discovery layers; every candidate is resolved to arXiv by title or, when no arXiv version exists, to a
free venue-native official source with DOI/ID, local backup, URL, and SHA-256. A paywalled item with no
free full text becomes `REMOVED_PAYWALLED_UNOBTAINABLE`; other inaccessible full text becomes
`REMOVED_UNOBTAINABLE`. Both remain in flow accounting, and occupancy or no-direct-match claims state
the corresponding **removal counts**.

The default submitted-date window is the closed interval 2022-10-01 through 2026-07-15. The frozen
exceptions are SF-L2-Q3 and SF-L3-Q3 from 2023-01-01, and SF-L7-Q3 from 2020-01-01. The foundational
lineage is not date-limited and is reported outside the recent novelty pool. Current category mapping
is:

- SF-L1/L2/L4/L5: `cs.CL`, `cs.AI`, `cs.LG`, `cs.CV`, `cs.RO`;
- SF-L3: those five plus `cs.SD`, `eess.AS`;
- SF-L6/L7/L8: `cs.CL`, `cs.AI`, `cs.LG`;
- SF-L10: `cs.SE`, `cs.HC`; SF-L11: `cs.MM`, `cs.MA`;
- SF-L12: `cs.CV`, `cs.AI`; SF-L13: `cs.LG`, `stat.ML`, `cs.NE`;
- SF-L14/L15: the full frozen union of 13 categories.

Date coverage is incremental and replayable. **First execution searches through the execution date.**
**Before synthesis freeze, scan from the first-execution date through the freeze date.** If Stage-1A
spans more than one period, **cross-period incremental batches are append-only** and carry their own
dates and source provenance; **old decisions change only by dated supersession**.

The ten-conference **T1 proceedings** title scan has **50 routes**. Each machine route has a stable
`route_id`, exact or explicitly unresolved entry point, frozen **wordlist**, status, and replay fields.
Venue tier is discovery metadata and a queue tie-break only; it has zero evidence weight. The T1/T2/T3
label never overrides `publication_status` or per-study quality.

Only the frozen compiler profile's ordered lane declarations and backtick query literal declarations
in §4 are normative compiler input. The canonical compiled result is exactly the current frozen
JSONL's 65 ordered records and their `record_sha256` values; compiler output is append-prefix stable,
and raw byte equality, not semantic JSON equality, is the release condition.

All other byte-preserved §4 narrative is **NON-NORMATIVE** historical annotation, including old
55/61/other counts, dated JSONL canonical claims, amendment/batch labels, and Decision-Log references.
It does not override §§0–3 or §§5–10, create an external dependency, or require opening a legacy file.
The interpretation fence and §§0–3 and §§5–10 have priority over non-normative §4 narrative.

`max_results` is a page size, never a result cap. Every page records `totalResults`; overflow is split
deterministically **year → month → day** with `parent_query_sha256`, child window, ordinal, decoded and
encoded request, and hashes. One day still above 2000 stops as
`API_LIMIT_SINGLE_DAY_OVER_2000`. Pagination must make **no silent truncation**. Store raw responses
when permitted, otherwise the complete reconstructible ID set; upstream API drift is recorded as
**external uncertainty**.

Known-ID verification is `ID_DEREFERENCE`: it checks existence, title, and cited identity, is **not a
discovery query**, and records access, UTC, transport status, attempts, and `HIT|MISMATCH|UNRESOLVED`.
`MISMATCH` and `UNRESOLVED` do not enter the seed or guarantee set. A fresh pre-registered held-out
paper records `used in query design = false`; held-out sourcing results are confined to the sentinel
pool. A vocabulary drift queue triggers a controlled lane evaluation after **three examples on the
same axis**; it cannot rewrite the frozen prefix.

The seed manifest, route registry, sentinel registry, paper census, access ledger, and full-text ledger
are append-only data sources. Counts come from their enumerated rows, never narrative arithmetic.

## §4 检索 lanes 与 65 条编译冻结查询（48 原批 + 3 条 A3-8 增补 + 2 条 C4-6 受控类目道 + 2 条 C4A 受控类目道 + 6 条 C4B 受控类目道,append-only）

**通用规格**：默认引擎 = arXiv API;默认窗口 2022-10-01→2026-07-15（例外行内注明）;
max_results = 75（SF-L7-Q3 为 50）——**语义 = 每页大小,非结果上限**（溢出规则见下）;按
relevance 排序。**类目映射（amendment-1 确定性冻结,v3 外审 4.1）**：SF-L1/L2/L4/L5 =
cs.CL+cs.AI+cs.LG+**cs.CV+cs.RO**（agent/感知/记忆-技能/验证层——CoVer/Affordance/具身
agent 均属视觉-机器人域,类目盲区实证在案）;SF-L3 = 前五类 + cs.SD+eess.AS;SF-L6/L7/L8 =
cs.CL+cs.AI+cs.LG（黑盒优化/Goodhart/评测经济学文献集中于此三类——纸面敏感性依据见
amendment-1,snowballing 与 SF-L9 兜异类溢出;执行中发现反例即走版本化增补扩类）。
查询编号 = SF-L{n}-Q{m}（arXiv）。**各 lane 的 S1/S2 副源行已按 A2-1 整体退役**（下文保留
作历史记录,不执行）。允许执行中对拼写变体做**登记后**微调（原查询照跑,变体新增编号,禁替换）。

**exact-query 冻结正典（amendment-1,v3 外审 4.2 闭合;A3-8 后 51 条;C4-6 后 53 条;C4A 后
55 条）**：55 条查询（48 原批 +3 A3-8 增补 +2 C4-6 受控类目道 +2 C4A 受控类目道——**前 53
行逐字节不变、增补层层追加于文件末尾**,原批行保留 compiler_version sfqc-1.0.0,A3-8 增补行
标 sfqc-1.1.0,C4-6 道行标 sfqc-1.2.0,C4A 道行标 sfqc-1.3.0,C4B 道行标 sfqc-1.4.0）
已由离线编译器
`scripts/survey/sf_query_compiler.py` 装配为 **`2026-07-15-sf-queries.jsonl`**——逐行含
decoded/URL-encoded 串、类目、date_from/to、start/max_results/sortBy/sortOrder、compiler
版本与行哈希,**零占位符**;静态验证报告 `docs/checks/2026-07-15-sf-queries-static-validation.md`
+ 复跑报告 `docs/checks/2026-07-16-sf-queries-static-validation-rerun.md`（A3-8——证明
「当前协议 → 当前 compiler → 当前 queries.jsonl」链与原批 48 行字节前缀不变）。
**执行以 jsonl 为正典,本节文字仅人读参考**。窗口例外（SF-L2-Q3/SF-L3-Q3 = 2023-01 起;
SF-L7-Q3 = 2020-01 起）已折入各行。日期界约定：submittedDate 双闭区间,以 arXiv v1 提交时间
为准。**可回放承诺分层（v3 外审 §7.2-II）**：请求定义可复现 + 原始响应留存 + 派生集合可由
原始响应重建;不承诺 API 返回逐字节一致,接口侧漂移记为外部不确定性。

**溢出/分页规则（v3 外审 4.3——完整性控制,非预算 cap;A3-6 补递归 fallback）**：执行时读取
每查询 `opensearch:totalResults`,以 start 递增**分页抓取至全量**;若 totalResults > 2000
（arXiv API 实用界限）,按 **年 → 月 → 日** 子窗对该查询做**确定性递归拆分**直至每片 ≤2000
（单一子窗仍超限即降级到下一时间粒度,粒度穷尽则如实登记为接口极限）;派生查询
`query_id = <父ID>-W<窗口序号>`,REC-1 行内记 `parent_query_sha256`;每页保存 start/max_results
与原始响应哈希,totalResults 全程留痕——**禁止无声截断**。

**副源路线——已退役（A2-1）**：原 16 条副源路线（`2026-07-15-sf-secondary-routes.md`,曾为
v3 外审 4.4 的闭合方案）按 owner 裁决①**整体退役留档,不执行**;其发现职能由 §2 的 T1 十会
题录扫描道（可回放性更强）与引文图承接。对 v3 外审 4.4 与修正案 C 的取代已在 amendment-2
A2-1 披露,reviewer 签署时可表态。

### SF-L1 reasoning+acting 与环境反馈（ReAct/Reflexion/LATS 族）
- Q1 `abs:"language agent" AND abs:feedback AND (abs:"test-time" OR abs:"inference-time" OR abs:"training-free")`
- Q2 `ti:agent AND (abs:"self-reflection" OR abs:"verbal reinforcement" OR abs:reflexion)`
- Q3 `(abs:"reasoning and acting" OR abs:"interleaved reasoning" OR abs:"act and reason") AND abs:agent`
- Q4 `(abs:"tree search" OR abs:MCTS) AND (abs:"language model" OR abs:LLM) AND (abs:agent OR abs:planning)`
- Q5 `(abs:"environment feedback" OR abs:"execution feedback") AND (abs:LLM OR abs:"language model") ANDNOT abs:RLHF`
- Q6 `abs:"language agent" AND (abs:search OR abs:planning) AND abs:value`
- Q7 `(abs:"agentic workflow" OR abs:"agentic system" OR abs:"agentic systems" OR abs:"multi-agent") AND (abs:orchestration OR abs:orchestrator OR abs:conversation OR abs:"automated design" OR abs:generation) AND (abs:LLM OR abs:"language model")`（A3-8 增补 2026-07-16——agentic 系统设计/多 agent 编排盲区道,预期召回 ADAS/AutoGen/Magentic-One）
- Q8 `(abs:"computational graph" OR abs:"optimizable graph" OR abs:"agent graph" OR abs:"graph optimization") AND (abs:agent OR abs:LLM OR abs:"language model")`（A3-8 增补 2026-07-16——可优化图盲区道,预期召回 GPTSwarm/VideoAgent-2026）
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
- Q7 `(abs:"information seeking" OR abs:"active perception" OR abs:"compositional reasoning" OR abs:"plug-and-play" OR abs:"visual chain of thought" OR abs:"visual chain-of-thought") AND (abs:tool OR abs:module OR abs:visual OR abs:multimodal) AND (abs:LLM OR abs:"language model")`（A3-8 增补 2026-07-16——信息获取/主动感知/多模态组合盲区道,预期召回 AVIS/Chameleon/Visual-Sketchpad）
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
- Q3 `abs:Goodhart`（窗口 2020-01 起,每页 50）
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

**计数（correction #4A P0-R5 后现行口径）**：8 lanes × 6 + 3 条 A3-8 增补（SF-L1-Q7/Q8、
SF-L3-Q7）+ 2 条 C4-6 受控类目道（SF-L10-Q1/Q2）+ 2 条 C4A 受控类目道（SF-L11-Q1/Q2）=
**65 条预注册查询**（历史口径「55」见 C4A、「53」见 C4-6、「51」见 A3-8、「48」见 A3-8 前、「64」见
amendment-2;16 条副源路线已退役）。
预算/调用量等资源轴不是查询过滤器,是抽取轴（§7,重校准 §2.1 口径）。**增补查询的敏感性审计
留痕**：离线纸面审计（Opus 独立,零联网）结论与逐篇召回表随 amendment-3 批次归档于
Decision-Log 续59;审计明确 ToT/Socratic-Models 不为其加查询（种子+引文图兜底）。

### SF-L9 foundational lineage（基础谱系道——amendment-1 新增,v3 外审 4.5;不受 2022 窗限）

- **种子** = manifest 增量批次1 的 4 条经典（metareasoning / POMDP / options / UCT,DOI 题录）;
- **方法** = 自经典种子 backward/forward chaining（SS/OpenAlex 发现层,承重回正式版）,沿链补
  value of information / anytime computation / algorithm selection / active perception 代表作;
- **目标** = 建立 RL/search/planning/metareasoning 概念分类与本研究对象的谱系定位——**「RL」
  命名保留与否的裁决依据**（RL 控制合同命名纪律引用处）;
- **统计隔离**：本道产出**不计入** 2022–2026 近期 novelty 池,单独报告;
- **停止规则**：连续**两轮** chaining 零新增概念祖先即停（与主道饱和判据对齐——内审 MINOR-8
  更正）,单独留痕;
- 无预注册 Boolean 查询（经典文献 arXiv 覆盖不全,以 chaining + DOI 锚为主;Google Scholar
  仅 DISCOVERY_ONLY）。

### SF-L10 SE/HCI agent-systems 受控类目道（correction #4 C4-6 增补 2026-07-16——cs.SE/cs.HC 类目盲区补救）
- Q1 `(abs:"black-box" OR abs:blackbox) AND (abs:LLM OR abs:"language model") AND (abs:agent OR abs:testing OR abs:optimization)`（C4-6 增补——SE/HC 类目 × 黑盒 agent 身份词族;sentinel AgentEval 2607.06873〔主类目 cs.SE 零 cross-list,v1=2026-07-08 在窗内〕离线词项级已匹配 L6-Q1 族、仅被类目拦截,本道即其确定性补救）
- Q2 `(abs:agent OR abs:agentic) AND (abs:workflow OR abs:orchestration OR abs:"tool use" OR abs:evaluation OR abs:testing) AND (abs:LLM OR abs:"language model" OR abs:"foundation model")`（C4-6 增补——SE/HC 类目 × agent workflow/评测词族,承接 HCI 侧 agent 系统工作〔哨兵 2508.01186 双类目 cs.AI+cs.HC〕）

（本道类目 = **cs.SE + cs.HC 两类受控投放**,不重复扫描主 lanes 的 cs.AI/cs.CL/cs.LG 等类;
命中编码/承重规则与主 lanes 完全一致;编译层 = sfqc-1.2.0 **append-only**——53 行文件的前
51 行逐字节不变;道名取 SF-L10 因 SF-L9 已被基础谱系道占用〔收词纪律:同名不承载两定义〕。）

### SF-L11 MM/MA multimodal-agent 受控类目道（correction #4A P0-R5 增补 2026-07-16——cs.MM/cs.MA 类目盲区补救）
- Q1 `(abs:"training-free" OR abs:"test-time" OR abs:"inference-time" OR abs:"tuning-free" OR abs:"without fine-tuning") AND (abs:agent OR abs:agentic OR abs:"multi-agent") AND (abs:multimodal OR abs:audio OR abs:video OR abs:visual OR abs:omni)`（C4A 增补——MM/MA 类目 × 冻结身份词族 × 模态词族;词项**全部复用主 lanes 既有词族**〔身份族+模态族,见 amendment-5 词项 provenance〕,未参照任何 sentinel 摘要挑词,防循环验收;确定反例 = MAR3 2603.27706〔主类目 cs.MM 唯一,ACM MM 2026,training-free 多代理 audio-visual〕）
- Q2 `(abs:LLM OR abs:"language model" OR abs:"foundation model") AND (abs:agent OR abs:agentic OR abs:"multi-agent") AND (abs:"prompt optimization" OR abs:"self-reflection" OR abs:feedback OR abs:"self-improving" OR abs:"self-correction" OR abs:"self-evaluation")`（C4A 增补——MM/MA 类目 × agent 反馈/自改进词族〔全部复用 SF-L1/L4 既有词项〕;held-out 哨兵 VQQA 2603.12310〔cs.MA cross-list〕作本道独立验收,其摘要未参与词项设计）

（本道类目 = **cs.MM + cs.MA 两类受控投放**,与 SF-L10 同构;命中编码/承重规则与主 lanes 完全
一致;编译层 = sfqc-1.3.0 **append-only**——55 行文件的前 53 行逐字节不变。）

### SF-L12 CV/AI vision-agent 受控类目道（correction #4B P0-3.3 增补 2026-07-16——SF-L11 词族跨类目镜像,Seg-Agent 漏检补救）
- Q1 `(abs:"training-free" OR abs:"test-time" OR abs:"inference-time" OR abs:"tuning-free" OR abs:"without fine-tuning") AND (abs:agent OR abs:agentic OR abs:"multi-agent") AND (abs:multimodal OR abs:audio OR abs:video OR abs:visual OR abs:omni)`（C4B 增补——词项 = **SF-L11-Q1 逐字镜像,零新词**〔评审 P0-3.3:不得从 Seg-Agent 摘要发明词项〕;确定反例 = Seg-Agent 2605.12953〔cs.CV 主类目+cs.AI,training-free 视觉反馈环,离线词项级已匹配 L11-Q1/Q2、仅被类目拦截 = UNRESOLVED_MISS,博导复审 #4A MAJOR-3〕,本道即其确定性补救）
- Q2 `(abs:LLM OR abs:"language model" OR abs:"foundation model") AND (abs:agent OR abs:agentic OR abs:"multi-agent") AND (abs:"prompt optimization" OR abs:"self-reflection" OR abs:feedback OR abs:"self-improving" OR abs:"self-correction" OR abs:"self-evaluation")`（C4B 增补——SF-L11-Q2 逐字镜像;held-out 独立验收 = 隔离代理选取〔不接触修订 diff/词项,era≥2025 按 owner 时代裁决〕,预注册后运行）
- Q3 `(abs:agent OR abs:agentic) AND (abs:workflow OR abs:orchestration OR abs:"tool use" OR abs:evaluation OR abs:testing) AND (abs:LLM OR abs:"language model" OR abs:"foundation model")`（C4B 增补——**SF-L10-Q2 逐字镜像,零新词**;触发 = 预注册 matcher 运行发现 DVD 2505.18079 近失例〔Deep Video Discovery,cs.CV/cs.AI/cs.CL,frozen-LLM agentic search,59 查询零命中、SF-L10-Q2 词项级已匹配仅被类目拦截〕——agent 时代词汇漂移轴〔agentic/autonomous/tool-use 取代 training-free/test-time 自述〕的确定性补救;词项未参照 DVD 摘要）
- （本道类目 = **cs.CV + cs.AI 两类受控投放**;与主 lanes 的 cs.CV/cs.AI 存在类目交叠但词族格不同——主 lanes 词族此前漏检 Seg-Agent 即为证据;去重由 REC-0 多源命中合并承接。）

### SF-L13 LG/ML learning-methods 受控类目道（correction #4B owner 裁决增补 2026-07-16——learning 方法域受控投放）
- Q1 `(abs:"training-free" OR abs:"test-time" OR abs:"inference-time" OR abs:"tuning-free" OR abs:"without fine-tuning") AND (abs:agent OR abs:agentic OR abs:"multi-agent") AND (abs:multimodal OR abs:audio OR abs:video OR abs:visual OR abs:omni)`（C4B 增补——SF-L11-Q1 逐字镜像;owner 裁决 2026-07-16:learning 相关域 = 重要方法域,cs.LG 主 lanes 已开但词族格未铺,本道补齐〕）
- Q2 `(abs:LLM OR abs:"language model" OR abs:"foundation model") AND (abs:agent OR abs:agentic OR abs:"multi-agent") AND (abs:"prompt optimization" OR abs:"self-reflection" OR abs:feedback OR abs:"self-improving" OR abs:"self-correction" OR abs:"self-evaluation")`（C4B 增补——SF-L11-Q2 逐字镜像;held-out 独立验收 = 隔离代理选取,同 SF-L12 纪律）
- Q3 `(abs:agent OR abs:agentic) AND (abs:workflow OR abs:orchestration OR abs:"tool use" OR abs:evaluation OR abs:testing) AND (abs:LLM OR abs:"language model" OR abs:"foundation model")`（C4B 增补——SF-L10-Q2 逐字镜像,与 SF-L12-Q3 同触发〔DVD 词汇漂移近失例〕,方法域对称铺设）
- （本道类目 = **cs.LG + stat.ML + cs.NE 三类受控投放**——stat.ML/cs.NE 为残差兜底〔该两类相关论文几乎均交叉挂 cs.LG,边际成本≈0〕;arXiv 无独立 deep-learning 类目,DL 工作即落本组类目;Q2 词族在 cs.LG 下命中体量可能较大,75-cap 溢出走 YEAR/MONTH splitter,筛查量执行期如实呈报〔全力摸高阶段不预设 cap〕。）

### SF-L14 方法占位·系统对象轴（correction #4C P0-R9 MAJOR-G1 增补 2026-07-18——orchestration/guidance 方法族,零 agent 连词）
- Q1 `(abs:orchestration OR abs:orchestrator OR abs:controller OR abs:routing) AND (abs:multimodal OR abs:"multi-modal" OR abs:omni OR abs:audio OR abs:speech OR abs:video OR abs:visual OR abs:"vision-language") AND (abs:"training-free" OR abs:"tuning-free" OR abs:"off-the-shelf" OR abs:"without fine-tuning" OR abs:"test-time" OR abs:"inference-time" OR abs:frozen)`（C4C 增补——orchestration 词族取自 2026-07-16 冻结的 T1 词表 A 组;abs:frozen = PRESS 复核 MINOR 采纳〔北极星用语,低噪声〕〔先于 P0-R9 评审件存在,天然非单篇捕获器〕;机器证据:接住 2508.10016〔61 查询确定性零命中的 system-occupancy 反例〕）
- Q2 `(abs:decoding) AND (abs:guidance OR abs:guide OR abs:guided OR abs:contrastive OR abs:steering OR abs:steer OR abs:"controlled decoding") AND (abs:multimodal OR abs:"multi-modal" OR abs:omni OR abs:audio OR abs:speech OR abs:video OR abs:visual OR abs:"vision-language")`（C4C 增补——guided/contrastive/steering decoding = 文献通用方法族〔非项目命名〕;机器证据:接住 2602.23306〔外部 LRM guidance 反例,61 查询+T1 词表双零命中的最深盲区〕;steering/controlled-decoding 词族 = PRESS 独立复核唯一 MAJOR 的采纳〔2026-07-18,思想实验 TE-2 证明缺口〕）
- （本道类目 = **13 类冻结类目全并集受控投放**〔cs.CL/cs.AI/cs.LG/cs.CV/cs.RO/cs.SD/eess.AS/cs.SE/cs.HC/cs.MM/cs.MA/stat.ML/cs.NE〕——方法占位轴对整个已冻结类目宇宙对称生效,杜绝「方法轴自身再现类目盲区」类 finding;P0-R9 根因 = L11–L13 把 agent 词组写成检索前提〔认识论循环〕,本道零 agent 连词。）

### SF-L15 方法占位·机制轴（correction #4C P0-R9 MAJOR-G1 增补 2026-07-18——test-time scaling / self-verification 方法族,零 agent 连词）
- Q1 `(abs:"test-time scaling" OR abs:"inference-time scaling" OR abs:"test-time compute" OR abs:"inference-time compute" OR abs:"inference compute" OR abs:"test-time optimization") AND (abs:multimodal OR abs:"multi-modal" OR abs:omni OR abs:audio OR abs:speech OR abs:video OR abs:visual OR abs:"vision-language" OR abs:VLM OR abs:MLLM)`（C4C 增补——TTS 短语族 = 文献通用机制命名;机器证据:接住 2512.11109/2606.28864/2606.08231〔含 ACL survey 的 arXiv 孪生〕）
- Q2 `(abs:"self-verification" OR abs:"self-verified" OR abs:"self-consistency" OR abs:"majority voting" OR abs:"majority vote" OR abs:"best-of-n" OR abs:"self-refinement" OR abs:"self-refine" OR abs:"self-correction") AND (abs:multimodal OR abs:"multi-modal" OR abs:omni OR abs:audio OR abs:speech OR abs:video OR abs:visual OR abs:"vision-language" OR abs:VLM OR abs:MLLM) AND (abs:"test-time" OR abs:"inference-time" OR abs:sampling OR abs:search OR abs:scaling)`（C4C 增补——self-verification/consensus 词族镜像 T1 词表 A 组;机器证据:接住 2512.19433/2607.09438;abs:"multi-modal" 连字符表面变体 = 2512.19433 暴露的归一化词面缺口〔DVD 词汇漂移同类,vocabulary-drift 队列第 3 例同轴触发受控增补——本增补即该机制的首次执行〕）
- （本道类目同 SF-L14 = 13 类全并集;两道均为「方法占位」发现轴——`agentic` 自此仅是 screening/coding 的编码结果,不再是任何发现通道的入场券〔P0-R9 整改原则〕;与既有 lanes 的命中交叠由 REC-0 多源合并去重承接。）

## §5 Deduplication, screening, conflicts, and stopping

Every canonical work receives **one REC-0 row per canonical work**. REC-0 keeps all query, route,
known-item, and citation source hits, dedup provenance, screening stage, decision, reason, screener,
second reviewer, adjudicator, full-text version, and REC-2 back-reference. Duplicate IDs, title
variants, and venue/arXiv twins merge without losing hit lineage. Included REC-0 and REC-2 rows form an
exact one-to-one link; an orphan, cross-wire, many-to-one link, or unknown duplicate target fails.

Screening is breadth-first then triggered depth-first:

1. **BFS** records all frozen-query and route hits at title/abstract level in REC-0.
2. A record enters **triggered DFS** when it has object overlap (`T-a`), question overlap (`T-b`), a
   transferable element (`T-c`), or a conclusion conflict (`T-d`). The deterministic priority is
   threat, then 2025+ recency and core relevance, with venue tier only a final tie-break.
3. The threat queue is **not a hard cap**. Additions and removals retain discovery provenance and may
   not preferentially promote supportive work.
4. Claim-bearing, direct-threat, and core paths require **full text** and D2 extraction. Abstract-only
   evidence can establish existence but cannot support a claim-bearing conclusion.
5. `REVIEWER_KNOWN_ITEM` entries receive a guaranteed DFS entrance, do not alter the frozen queries,
   and never masquerade as query recall. Each batch emits a **carry-forward ledger** for prior direct
   neighbors, current hits, citation additions, and zero-hit known items.

Known items are encoded against the current **taxonomy before prioritization**; this guarantee
**does not alter the frozen queries**. The agent-era rule makes 2025+ work a queue priority, while
pre-2025 work remains eligible for lineage or continued-citation reasons; recency is **not
study_quality** and never changes an evidence verdict.

Citation traversal expands only DFS nodes. It follows method-lineage and comparison edges; background,
dataset, and generic-tool citations are registered but not expanded. A work present in at least three
DFS graphs and not independently triggered is `COMMON_NODE`; the global **visited-set** expands any
work at most once. Queue priority is **forward-comparison**, forward-lineage, backward-lineage, then
backward-comparison.

A zero core-citation intersection permits a cheap screen with reason
`OTHER:NO_CORE_CITATION_OVERLAP`, but citation overlap **cannot be the discovery entrance**. Cross-field
communities are a known counterexample. Screening conflicts are independently coded; unresolved
load-bearing disagreements enter a conflict queue and no occupancy denominator.

Mapping exit is the conjunction of:

- **E1**: all frozen queries and registered routes are complete and every hit has a **REC-0** decision;
- **E2**: backward references extracted from archived e-print plus date-stamped **forward** citation
  snapshots produce zero new INCLUDED works for **K=2** consecutive closure rounds; and
- **E3**: every registered sentinel and supplied counterexample has a disposition and zero
  `UNRESOLVED` items remain.

The saturation report records per round new hits, new included works, closure edges, remaining queue,
removed-unobtainable counts, and conflict counts. A new counterexample after closure is classified by
the same contract and corrected by dated supersession; it does not silently alter an old round.

E2 identifier resolution is an **OPEN** precondition until its report closes. **Before any E2 claim,
resolve every entry by DOI, ACL ID, OpenReview ID, or normalized title.** The report gives the four
work-level counts **total / resolved / ambiguous / unresolved**, includes a **DOI-only mutation
fixture**, and freezes a **pre-registered unresolved ceiling** before resolution results are inspected.
**K=2 zero growth on the resolved subgraph is not closure exhaustion** and cannot be described as
closure dryness or a complete citation graph.

## §6 Coding schema, signal and edge identity, and information boundary

Coding depth is **code-on-use**:

- `D0`: bibliographic REC-0 lineage and screening decision for every work;
- `D1`: REC-2 identity, relevance, proximity, publication status, venue metadata, DFS trigger,
  verification depth, and typed `NA` blocks with reasons;
- `D2`: the complete contract for every claim-bearing, direct-threat, or core path.

The **INCLUDED REC-0 ↔ REC-2** link is one-to-one. `DIRECT_THREAT` survives seed-to-REC-2 transfer.
Machine-derived **flow counts** must equal the REC-0 population. A missing, orphaned, invalid, or
unadjudicated load-bearing row fails the whole report; it is never silently dropped to improve an
occupancy number. A permitted NA has one **typed NA** object shape with a nonempty reason.

The canonical taxonomy is a projection of source schemas, not a second independently edited schema.
This **canonical projection** is:
REC-2 matrix facts, 13-axis system-control facts, `omni_axes`, `rl_identity`, signals, and control
edges. Mixed-path papers are split by **method path**. Core system coding uses a **13-axis** view:
core identity, access level, training scope, horizon, **decision rights**, state/memory, tools,
feedback, candidate generation/selection, stopping/budget, terminal synthesis, **information
boundary**, and modality/task.

Supporting blocks include `source_axes`, `omni_axes`, `rl_identity`, TF audit, resource axes,
method-occupation fields, and `evidence_axes`. `publication_status` is independent of `venue_tier`.
`study_quality` has **seven dimensions**—data boundary, control fairness, uncertainty reporting,
ablation attribution, reproducibility, artifact availability, and `claim_evidence_match`—each with a
verdict, reason, locator, and coder. The summary rating cannot replace those dimensions.
`venue_tier` has **zero evidence weight**.

The method-occupation extraction records `method_gist`, limitations, `improvement_space` (axis,
structural obstacle, and material RQ/threshold effect), and `borrowable` elements. `selection_object`
defines the analysis stratum and results **never aggregate across pool types**.
Each path also records `most_threatened_rq`; `none requires a reason`.

A `random-K` path may have a real candidate pool while having **no selection signal**. Pipeline rows
carry `component_path_ids` so a component is not copied into the denominator as an independent path.

Signals are instance-level: `signals[].signal_id` is unique within a path and binds `form`, `source`,
`lifecycle`, `uses`, and evidence. Reward status is existential over a signal, not inferred from a row
label. Sequential compatibility requires a live valid edge from the **same signal**, and the edge's
use must be in that signal's `reward_uses`. Offline calibration never becomes online control.

Every `control_edges[]` item names a signal instance, `signal_use`, `decision_right`, lifecycle, source
locator, and causal semantics. The validator rejects `edge-use-not-in-signal`,
`right-not-declared`, and `relation-not-allowed`; invalid edges are errors, not silently filtered.
Allowed relations are evidence-backed and versioned. Terminal-lifecycle edges may target terminal
synthesis or stop only. An unrelated right cannot be spliced to a reward signal.

The information boundary is absolute: test-item gold may not enter prompt, retrieval, candidate
construction, selector, reward, verifier, tool routing, memory, or stopping. `read-out` uses information
already supplied to the frozen core; `new-info` injects answer-bearing information and is excluded from
strict identity. Dev-gold method selection is exposure, not test leakage, and must be isolated and
reported. Trained reward instruments remain comparators or measurement tools and never enter the
all-components-weight-frozen occupancy.

The final derivations use the following frozen names and semantics. `seven_strict_bits_all_false`
means that each of `core_weight_update`, `external_component_weight_update`,
`controller_program_or_config_optimized_on_labels`, `human_or_dev_label_model_selection`,
`deployment_label_access`, `test_item_gold_access`, and `inference_external_new_information` is exactly
false. Topology policy A admits `single_core` and `single_core_multi_call`. Native speech is represented
by `audio_native`; the native speech/audio/omni set is therefore `{audio_native, omni_native}`.
For a signal, `s.reward_uses` is the intersection of `s.uses` with the frozen reward-use set. A
`qualifying_reward_signal(s)` has lifecycle in `{online_step, terminal}`, form in `reward_forms`, and a
nonempty `s.reward_uses`. A valid LIVE edge passes the structural, allowed-relation, locator, lifecycle,
terminal-right, signal-identity, signal-use, and declared-right checks above.

```text
data_access_strict_bits = seven_strict_bits_all_false AND internal_visibility == api_only
is_s0_core_compatible = data_access_strict_bits AND core_topology IN {single_core, single_core_multi_call} AND core_native_modality IN {audio_native, omni_native}
is_reward_guided = EXISTS qualifying_reward_signal(s)
is_rq_sys_control_compatible = control_horizon == sequential AND EXISTS valid LIVE edge e driven by the same qualifying reward signal s AND e.signal_use IN s.reward_uses
is_project_method_candidate = is_s0_core_compatible AND is_rq_sys_control_compatible
reward_guided_selection = candidate_pool_exists == true AND selection_policy IN {scored_select, tournament_select} AND selection_object != none AND EXISTS qualifying reward signal s used for select or prune
```

The canonical policy label is `tournament_select`; “tournament” is only a noncanonical shorthand.
**offline_calibration signals never qualify** for `is_reward_guided`, RQ-SYS control, or
reward-guided selection.

`DIRECT_THREAT` requires `threat_dual_coding`, **two distinct extractors**, and a resolvable
`rec5_ref`; **disagreements > 0 requires a nonempty adjudicator**. A missing actor, duplicate extractor,
missing REC-5 link, or unresolved disagreement fails before the row can support a claim.

## §7 Schema-v3 evidence, adjudication, and strong PDF anchors

The active **per-paper sidecar** files use schema v3 and are the **single handwritten layer**. The
committed coding artifact is **generated**, never independently edited. The deterministic generator
must produce coding bytes that are **byte-identical** to the committed coding artifact; then structure,
bound-value, source, row-hash, and adjudication **reconciliation** run before derivation.

Each load-bearing path binds **16 row-level** values:

1. seven strict bits;
2. `internal_visibility`;
3. `core_topology`;
4. `core_native_modality`;
5. `control_horizon`;
6. `decision_rights`;
7. `candidate_pool_exists`;
8. `selection_policy`;
9. `selection_object`; and
10. `explicit_candidate_pool_selection`.

Each signal binds **4 signal-level** values—`form`, `source`, `lifecycle`, and `uses`. Each edge binds
**2 edge-level** values—`signal_use` and `decision_right`. Binding values are type tagged: booleans and
integers do not compare equal, including inside lists. Missing fields and malformed containers yield
stable failures rather than exceptions. Supported evidence kinds are `canon`, `tex`, `pdf_page`, and
structured `absence`; unknown kinds fail.

A structured absence states the encoded value, inspected scope, reason, source version, coder, and
adjudicator. It is not a silent default. Every row has an **adjudication row hash** over its canonical
load-bearing content excluding adjudication metadata; **any load-bearing change invalidates** the hash
and requires independent adjudication. Finalization is bound to the reviewed raw sidecar snapshot and
adjudication artifact bytes, with no caller-supplied trust-root override.

Lineage requires `paper_work_id`, `fulltext_ref`, `canonical_record_id`, source locator, coder, and
semantic adjudicator. The full-text ledger line must bind kind and SHA-256; the canonical record ID
must resolve to the correct work heading. A **stable actor ID** is required, coder must differ from
semantic adjudicator for load-bearing rows (`coder ≠ semantic_adjudicator`), accepted rows say
`adjudicated_agree`, and disagreement
goes to the **conflict queue**.

Bibliographic identity provenance preserves **raw Atom** bytes and their hash. A
`REGISTERED_BOUNDARY` is valid only when its machine-readable paper, boundary, reason, adjudicator, and
date fields are complete. A **held-out** record requires frozen provenance, date eligibility, and proof
that it did not supply query terms.

Free page locators and `pdf_page` evidence use the exact grammar
`pN anchor='multi-word phrase'`. After Unicode normalization, case-folding, punctuation removal, and
whitespace collapse, an anchor has at least two lexical tokens, at least twelve alphanumeric
characters, appears in the page window **N-1 through N+1**, and occurs no more than three times in the
complete PDF. Required failures are `page-token-without-anchor`, `page-anchor-too-weak`,
`page-anchor-missing`, `page-anchor-not-discriminative`, `page-out-of-range`, and
`pdf-unreadable-for-page-check`. A `pdf_page` claim separately checks page range and anchor presence.

```text
anchor_lexical_tokens >= 2
anchor_alphanumeric_characters >= 12
anchor_page_window = N-1..N+1
complete_pdf_occurrences <= 3
```

The mutation suite is derived from the **derived-formula sensitive surface**, not merely the last
review's examples. It starts from a **clean stamped baseline**, legitimately recomputes row hashes for
new-row tests, and proves each bad mutation creates a named failure. It covers row, signal, edge,
locator, actor, ledger, generator, adjudication, and headline binding. Independent semantic
counterexamples are authored by a **non-implementer** and enter an **append-only fixture** library.
Every new oracle must undergo an **oracle-strength audit** with a **demonstrated failing input**.

A path with any required-evidence, locator, source, structure, adjudication, or generator failure is
excluded from all load-bearing derivations and makes the overall evidence contract FAIL.

## §8 Systematic-mapping execution and exposure accounting

When and only when §0's three authorizations are present, Stage-1B proceeds in this order:

1. record the execution commit, frozen protocol/query hashes, current registries, platform, actor,
   and exposure declaration;
2. run the first-step interface and phrase-behavior checks without a research model;
3. execute each frozen query with pagination and deterministic overflow splitting, logging every page;
4. scan registered T1 routes and resolve candidates without discarding duplicate provenance;
5. create REC-0 rows, screen BFS, then run the triggered DFS and citation-closure procedure in §5;
6. fetch and register **PDF + e-print** for included, core, sentinel, or claim-bearing work—**FETCH is
   registered immediately** and an unregistered fetch does not count as read;
7. create per-paper sidecars during coding—the **locator is recorded during coding**, never appended
   after interpretation; a row without a locator does **not enter an occupancy denominator**;
8. generate coding, reconcile evidence, complete independent adjudication, and only then derive tables;
9. rerun E1/E2/E3, release binding, immutability, context, and dual-platform gates before synthesis.

Machine query execution uses `REC-1`; canonical screening/dedup uses `REC-0`; extraction uses `REC-2`;
conflicts and threat dual-coding use their registered records; selection-process records and T1 route
logs complete the `REC-0` through `REC-7` family. Child splitting enters through
`parent_from_frozen_row`: `record_sha256` is frozen-record provenance and `query_sha256` hashes the
decoded request. The splitter contract is **ROOT → YEAR → MONTH → DAY**, supports exact
**checkpoint resume**, rejects duplicate child IDs, uses at least 3 seconds between network requests,
and records backoff and retry attempts.

Access accounting is dual and classed: `discovery_queries_executed`, `id_dereference_accesses`, venue
status checks, provenance fetches, full-text fetches, reviewer-claim verification, and
`HELD_OUT_SENTINEL_SOURCING` are separate. Registered classes include `PROVENANCE_FETCH` and
`FULLTEXT_FETCH`. A web or index access is classified by intent and use; discovery cannot be relabeled
as verification. Every access class has a stable name and an append-only event record.

Every stage statement includes `current_activity_stage`, `new_model_touches_since_gate_freeze` with
its starting commit, cumulative model touches, and `legacy_experiments = INHERITED_PRIOR_EXPOSURE`.
The exposure union is **four-repository scoped**; heterogeneous event counts are not aggregated.
Previously exposed datasets, splits, configurations, and selection decisions are excluded from fresh
or held-out claims or explicitly stratified. No later zero count erases inherited exposure.

Executable checks have three replay classes: `bundle-only` (stdlib and repository bytes),
`local-data` (registered full text on the data drive), and `network-dependent` collectors. Network
collectors are not used as release-gate replay. Evidence tests run on **Windows** and
**WSL2 Ubuntu-24.04** against the same committed bytes and must report the **same occupancy**. The
release requires **two platform-stamped reports** and **both PASS**.

## §9 Outputs, denominators, occupancy, negative results, and release binding

All completion claims are **machine-derived** from committed evidence. Missing evidence fails and
checks **fail closed**; a green state cannot inherit from an absent artifact. Every deterministic
**producer replay** runs in isolation, compares raw bytes, must be **byte-identical** to persisted
outputs, and cannot inherit a prior green status. A claim states its evidence mode:
`MACHINE_RECOMPUTED_LOCAL`, `MACHINE_REPLAYED_STRUCTURE`, `SOURCE_REPORTED_TRACEABLE`,
`REVIEWER_INFERENCE`, or `TEAM_ATTESTATION`. Machine structural replay never upgrades a paper's
reported number to local recomputation.

Every table states population, inclusion rule, path denominator, work denominator, task/modality cell,
selection-object stratum, and missing/unobtainable/conflict counts. The **prose lint** catches unscoped
quantifier tokens, but semantic safety comes from explicit set, **denominator**, **analysis unit**,
taxonomy derivation, and review. Cross-task occupancy is cellwise; no unweighted omnibus average is
reported.

Reader-visible headline tables are generated. A released artifact carries
`generated_headline_begin` and `generated_headline_end`; the checker must **re-render** from the
persisted evidence report and compare the **whole-block** bytes. Hidden binding values cannot excuse a
hand-edited visible number. The release manifest binds protocol, queries, taxonomy, coding,
adjudication, platform reports, current tables, and reviewer-facing artifacts by raw hash.

Mapping outputs are the coverage/kill matrix, system-control occupancy and sensitivity tables,
SOTA/method cards, updated census and ledger, saturation/flow report, factual direct-prior proximity
and reproduction-readiness evidence, and **eligible Stage-1C inputs**. This proximity map is not an
innovation-difference matrix or verdict. Stage-1B does not create or rank the
final candidate cards and does not freeze a reproduction list. Stage-1C owns the final 3–5 candidate
problem/gap-hypothesis cards, ranking, owner problem selection, and reproduction-list freeze; it does
not freeze a technical innovation. Each eligible input supplies the
supporting evidence and contradicting evidence, a single-observation kill criterion, unresolved alternatives,
method limitations, improvement space, and value needed for that later synthesis. “Not found” is
always scoped to the inspected set and carries removal and unresolved counts.

The opening package keeps separate tables for **method paths**, speech/omni **measurement instruments**,
evaluator/reward **negative-result priors**, and boundary/comparator work. A **trained reward
instrument** never enters the frozen-system method denominator. Reference roles include `DEEPLY_READ`,
`KNOWN_QUEUE`, `MEASUREMENT_INSTRUMENT`, and `BOUNDARY_COMPARATOR`. Bibliography and opening tables are
generated or manifest-bound. The known-item **carry-forward** ledger prevents an archived neighbor
from disappearing in later batches.

Reports may make a no-direct-match statement only after E1/E2/E3, independent agreement, and complete
denominator disclosure. Negative results and conflicting evidence are first-class outputs, not filtered
exceptions. Persistent evidence is the only basis for a completion claim.

Every reviewer-facing artifact has a self-contained reference appendix with **author, year, and stable
link**. **Numeric claims require a page, table, or figure locator.** A **non-contiguous quotation is
explicitly marked as stitched** rather than presented as one continuous span. **Consistent, dominant,
or ceiling claims are limited to the model, task, and setting reported by the paper**; evidence from one
reported setting cannot silently become a universal statement.

## §10 Document lifecycle, correction, re-review, and sign-off authority

The effective protocol lives at this stable path and is superseded in place with a version change. A
review submission, report, response, correction, or sign-off snapshot is created directly at
`wiki/audit/<campaign>/<round>/`, entered in the **audit registry**, and is **immutable from first
commit**. Historical errors are corrected by **dated supersession**; registered audit bytes and paths
are not edited or moved. Current pages link to the campaign audit index, not individual cold rounds,
except the one declared active review transaction.

Workbench material is mutable and noncanonical. Effective rules are distilled into `current/` with a
same-commit manifest update. At campaign close, unregistered superseded working files absent from the
current manifest move with `git mv` after reference and script checks. Registered audit artifacts stay
path-pinned and become cold by routing only.

Consolidation is mandatory when a third correction would otherwise accumulate on one effective
document; that third item is frozen as audit evidence and its surviving rule is folded into the
effective file immediately. A fourth amendment is forbidden before consolidation. The same immediate
consolidation applies at a context-budget breach, executable-contract review, stage boundary, sign-off
request, competing current claims, or handoff that cannot determine the next action from current
protocol plus status.

Query terms receive an **independent query review** before every **term freeze** and sign-off
application. The reviewer is isolated from implementation history; findings and owner disposition are
stored in the audit round. Open debt has a named **owner**, **deadline gate**, and status such as
`OPEN`; no debt is hidden by a general PASS. A `LATE_RECONSTRUCTED_REVIEW_SUMMARY` is useful history but
does not prove the original review process.

Corrections state the false-green or false claim, withdraw the old completion wording, identify exact
machine outputs, give discovery/model/smoke exposure counts, and request independent re-review. Each
new check must include a failing fixture. Completion claims are bounded by **persistent evidence** and
the checker's actual capability.

Every convergence label is **object-and-anchor-qualified**; internal convergence is not sign-off.
Every new checker receives an **oracle-strength audit** and a **demonstrated failing input** before its
PASS may support a release claim.

Search-design sign-off belongs only to an independent reviewer. Execution approval belongs only to
the owner. P0-R8 rerun evidence belongs to the named gate actor. These are three separate records; an
empty or stale one forbids execution. Scientific/novelty selection is a later owner decision and is not
implied by search-design sign-off.

## Appendix A — Legacy disposition routing (not an interpretive dependency)

Each row routes a cold transaction identifier to the self-sufficient normative section(s) above.
Status means the legacy file is superseded as an effective instruction but retained unchanged for
audit provenance. Exact physical paths are resolved only through the named cold index on demand; neither index nor any legacy artifact is part of default context.

| Legacy transaction | Cold index route | Status | Sufficient v2 carrier |
|---|---|---|---|
| Amendment 1 | campaign audit index / A1 | LEGACY / SUPERSEDED_EFFECTIVE_CHAIN_COLD | §1, §3, §4, §5, §6, §9 |
| Amendment 3 | campaign audit index / A3 | LEGACY / SUPERSEDED_EFFECTIVE_CHAIN_COLD | §0, §3, §4, §6, §8, §10 |
| Amendment 4 | campaign audit index / A4 | LEGACY / SUPERSEDED_EFFECTIVE_CHAIN_COLD | §3, §6, §8, §9 |
| Amendment 5 | campaign audit index / A5 | LEGACY / SUPERSEDED_EFFECTIVE_CHAIN_COLD | §3, §6, §8, §9 |
| Amendment 6 | campaign audit index / A6 | LEGACY / SUPERSEDED_EFFECTIVE_CHAIN_COLD | §3, §5, §6, §7, §9 |
| Amendment 7 | campaign audit index / A7 | LEGACY / SUPERSEDED_EFFECTIVE_CHAIN_COLD | §3, §5, §7, §8 |
| Amendment 8 | campaign audit index / A8 | LEGACY / SUPERSEDED_EFFECTIVE_CHAIN_COLD | §3, §4, §5, §8, §10 |
| Amendment 9 | working archive index / A9 | LEGACY / SUPERSEDED_EFFECTIVE_CHAIN_COLD | §0, §5, §6, §8, §9 |
| Amendment 10 | working archive index / A10 | LEGACY / SUPERSEDED_EFFECTIVE_CHAIN_COLD | §0, §5, §6, §8, §9 |
| Amendment 11 | working archive index / A11 | LEGACY / SUPERSEDED_EFFECTIVE_CHAIN_COLD | §6, §7, §9 |
| Amendment 12 | working archive index / A12 | LEGACY / SUPERSEDED_EFFECTIVE_CHAIN_COLD | §0, §6, §7, §9 |
| Amendment 13 | working archive index / A13 | LEGACY / SUPERSEDED_EFFECTIVE_CHAIN_COLD | §6, §7, §10 |
| Amendment 14 | working archive index / A14 | LEGACY / SUPERSEDED_EFFECTIVE_CHAIN_COLD | §6, §7, §8, §9 |
| Amendment 15 | working archive index / A15 | LEGACY / SUPERSEDED_EFFECTIVE_CHAIN_COLD | §6, §7, §8, §9 |
