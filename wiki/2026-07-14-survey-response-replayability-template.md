---
title: "Survey Response 可回放审计模板（Stage-1A 强制版）"
date: 2026-07-14
stage: "Stage-1A — problem definition / survey"
document_type: "review-response-template"
status: "TEMPLATE — 必须复制为新的定日期 response；禁止直接覆盖原调查记录"
owner_decision: "not requested by this template"
---

# Survey Response 可回放审计模板（Stage-1A 强制版）

> 本模板供研究团队或其 AI 在回复 Survey 审查时逐项填写。它不要求 Stage-1A 立刻达到论文发表级系统综述，
> 但只要团队使用 **complete / closed / saturated / no direct match / whitespace / novel /
> decision-ready** 等强结论，就必须达到本模板规定的可回放门槛。

## 0. 不可协商的提交规则

1. **新建定日期 response 和 replay bundle，不覆盖旧记录。** 如执行 hot/cold 迁移，必须保留旧版本的
   commit、blob hash、迁移映射和 supersession 关系。
2. **不得补造历史日志。** 找不到原始事件时填写 `RAW_EVENT_UNAVAILABLE`，说明缺失范围和影响；禁止根据
   最终论文清单反推一份看似完整的检索日志。
3. **不得把“搜索次数、抓取次数、论文数、证据数”混成一个数。** 四类计数必须分列，且都能由机器重新计算。
4. **每个结论必须回链到证据。** 不能只给论文 URL；必须给论文版本、主张、页/节/表/行定位和核验状态。
5. **一篇论文不能因标题或摘要相似就被标成 full-text verified。** `source_resolves`、
   `abstract_matches`、`fulltext_opened`、`claim_verified`、`result_reproduced` 是五个不同字段。
6. **选择与改写必须拆分。** in-pool selector、candidate generator、revision/correction、tool-use loop、
   weight update 分别编码；不得用“rerank/selection”笼统吞并。
7. **搜索失败、负结果、重复项和冲突均须保留。** 失败不得从分母消失。
8. **任何 AI 生成的结论都必须由指定责任人签名。** `generated_by` 与 `verified_by` 不得是同一无监督代理。

## 1. Response 首页：身份、范围与快照

请原样复制并填写：

```yaml
response_id: SURVEY-RESP-YYYY-MM-DD-NN
response_date: YYYY-MM-DD
responds_to_review: "<review path + canonical commit + sha256>"
survey_snapshot:
  repository: "<repo>"
  commit: "<40-char commit>"
  dirty_worktree: false
  included_paths:
    - path: "<path>"
      git_blob_sha256: "<sha256 of git-show bytes>"
stage: "Stage-1A"
stage_claim: "ROUND1_SCOUT_COMPLETE | CLAIM_AUDIT_COMPLETE | LOCALLY_SATURATED | ..."
candidate_definitions_commit: "<commit that froze I1/I2/I3/I4 definitions>"
search_window:
  started_at_utc: "YYYY-MM-DDThh:mm:ssZ"
  ended_at_utc: "YYYY-MM-DDThh:mm:ssZ"
databases_and_engines: []
generated_by: []
verified_by: []
known_missing_raw_events: []
owner_decision_requested: false
stage1b_authorized: false
```

如工作树不是 clean，必须附 `git diff --name-status`，并说明本次审查究竟固定在哪一份字节快照上。

## 2. 必须提交的 replay bundle

建议目录：

```text
wiki/survey/replay/<response_id>/
├── README.md
├── manifest.yaml
├── protocol.yaml
├── search_events.jsonl
├── search_results.jsonl
├── screening_decisions.jsonl
├── papers.jsonl
├── claim_evidence.jsonl
├── dedup_report.json
├── flow_report.yaml
├── coverage_matrix.md
├── comparator_cards.md
├── validation_report.txt
└── survey_response.md
```

每个文件都必须在 `manifest.yaml` 中登记字节数、行数、SHA-256、生成命令和上游依赖。manifest 本身的
canonical hash 写入 response 首页。

### 2.1 `protocol.yaml`：检索前或本轮开始时冻结的规则

```yaml
protocol_id: SURVEY-PROTO-YYYY-MM-DD-NN
research_questions:
  - id: RQ1
    text: "<问题>"
candidate_identities:
  - id: I2
    frozen_definition: "<必要条件；不得在看到邻居后追加条件>"
    positive_test: "<什么算占据>"
    negative_test: "<什么不算占据>"
    boundary_cases: []
lanes:
  - lane_id: L01
    purpose: "<lane 要排除什么>"
    databases: []
    date_range: {from: null, to: "YYYY-MM-DD"}
    languages: [en]
    planned_queries: []
inclusion_criteria:
  - id: IN-01
    rule: "<可机械执行的条件>"
exclusion_criteria:
  - id: EX-01
    rule: "<可机械执行的条件>"
dedup_priority: [doi, arxiv_base_id, acl_anthology_id, title_author_year]
saturation_rule:
  kind: "predeclared"
  test: "<例如连续两轮 backward/forward chase 无新增 DIRECT/PARTIAL 邻居>"
  applies_to: []
deviations: []
```

如规则是在搜索之后才写，必须标 `RETROSPECTIVE_PROTOCOL`，不得称 preregistered。

### 2.2 `search_events.jsonl`：实际执行过的每一次检索/抓取事件

一行一个事件：

```json
{"event_id":"SE-000001","run_id":"RUN-01","agent_id":"agent-or-human-id","timestamp_utc":"2026-07-14T01:23:45Z","lane_id":"L01","operation":"SEARCH","engine":"arXiv","endpoint_or_ui":"api","exact_query":"all:\"minimum Bayes risk\" AND all:speech","filters":{"from":"2020-01-01","to":"2026-07-14","language":"en"},"requested_limit":100,"cursor":null,"tool_version":"<version>","raw_response_path":"raw/SE-000001.json","raw_response_sha256":"<sha256>","status":"SUCCESS","error":null}
```

强制字段：

- `event_id/run_id/agent_id/timestamp_utc/lane_id/operation/engine/exact_query`；
- `operation` 只能是 `SEARCH | FETCH | CITATION_BACKWARD | CITATION_FORWARD | MANUAL_IMPORT`；
- URL 抓取必须记作 `FETCH`，不得计入 search query 数；
- `requested_limit` 不是 `returned_count`；后者由 `search_results.jsonl` 计算；
- 失败事件使用 `status=FAILED` 并保存错误类型；不得删除或用成功事件替代。

### 2.3 `search_results.jsonl`：每次检索实际返回的结果宇宙

```json
{"event_id":"SE-000001","rank":1,"result_id":"SR-000001-001","title_as_returned":"<title>","url":"https://...","provider_id":"<id|null>","snippet":"<optional>","returned_at_utc":"...","raw_record_sha256":"<sha256>","paper_id":"P-000123"}
```

必须能回答：每次检索返回了多少条、哪几条、排序如何、哪些后来被筛除。只保留 query 而不保留结果列表，
**不构成可回放检索**。

### 2.4 `screening_decisions.jsonl`：纳入/排除轨迹

```json
{"decision_id":"SD-000001","result_id":"SR-000001-001","paper_id":"P-000123","stage":"TITLE_ABSTRACT","decision":"INCLUDE","reason_code":"IN-01","reason_text":"meets frozen inference-time selector definition","reviewer_id":"R1","timestamp_utc":"...","conflict_id":null}
```

规则：

- `decision` 为 `INCLUDE | EXCLUDE | UNCERTAIN | DUPLICATE`；
- 排除必须使用协议中的 reason code；
- load-bearing 论文至少双人/双代理独立筛选，冲突有显式 resolution；
- 同一结果的决定若改变，追加新记录并引用 `supersedes_decision_id`。

### 2.5 `papers.jsonl`：规范论文身份与去重

```json
{"paper_id":"P-000123","canonical_title":"...","authors":["..."],"year":2025,"doi":null,"arxiv_base_id":"2503.23395","version":"v1","acl_anthology_id":null,"canonical_url":"https://arxiv.org/abs/2503.23395v1","fulltext_sha256":"<sha256|null>","aliases":["AuditoryTTC","scaling-auditory-cognition-2025"],"merged_from_result_ids":["SR-..."],"dedup_basis":"arxiv_base_id","record_status":"ACTIVE"}
```

要求：

- `paper_id` 稳定且唯一；跨 lane 只引用同一 `paper_id`；
- arXiv 版本必须固定。版本变化产生新 evidence，不得静默覆盖；
- DOI、arXiv、会议版本若为同一工作，明确 work-level 与 version-level 关系；
- `dedup_report.json` 给出原始结果数、候选记录数、合并数、人工冲突数和最终 exact unique 数；
- 禁止写 `~93`、`about 100` 后又把它当成精确覆盖率分母。

### 2.6 `claim_evidence.jsonl`：逐条主张核验

```json
{"claim_id":"CL-000321","paper_id":"P-000123","claim_text":"same frozen audio model scores K candidates with audio-conditioned likelihood","claim_type":"METHOD","source_resolves":true,"abstract_matches":true,"fulltext_opened":true,"evidence_grade":"CLAIM_VERIFIED","locator":{"version":"v1","section":"3.2","page":4,"table":null,"figure":null,"quoted_fragment":"<不超过必要长度>"},"supports":"I2_OCCUPIED","verification_notes":"...","verified_by":["R1","R2"],"verified_at_utc":"..."}
```

证据等级只允许：

| 等级 | 最低要求 | 允许支持的结论 |
|---|---|---|
| `DISCOVERED` | 仅发现标题/URL | 只能列入待查清单 |
| `ABSTRACT_VERIFIED` | 官方摘要已读，身份和摘要主张一致 | 方向性邻居，不得核对具体方法边界/数字 |
| `FULLTEXT_OPENED` | 固定版本全文已打开和存档 | 仍不等于某一主张已核实 |
| `CLAIM_VERIFIED` | 对具体主张给出页/节/表定位 | 可进入 kill/coverage 矩阵 |
| `REPRODUCED` | 代码、数据、配置和结果由团队重跑 | 可声称重现实验，仍须说明偏差 |

禁止把 `WebSearch snippet`、聚合页或既有记忆标成 `FULLTEXT_OPENED/CLAIM_VERIFIED`。

### 2.7 `flow_report.yaml`：机器重算的流量账本

```yaml
events:
  search_success: 0
  search_failed: 0
  fetch_success: 0
  fetch_failed: 0
results:
  returned_records: 0
  duplicate_result_records: 0
screening:
  title_abstract_included: 0
  title_abstract_excluded: 0
  fulltext_assessed: 0
  fulltext_excluded: 0
papers:
  exact_unique_works: 0
  exact_unique_versions: 0
evidence:
  abstract_verified: 0
  fulltext_opened: 0
  claim_verified: 0
  reproduced: 0
unresolved:
  citations: 0
  screening_conflicts: 0
  dedup_conflicts: 0
```

所有数值必须由脚本从 JSONL 生成；禁止手填后宣称“可重建”。

## 3. Survey Response 正文模板

### 3.1 一页结论

```text
本轮状态：<唯一状态 token>
已完成：<可由 bundle 重算的事项>
未完成：<明确事项>
本轮允许的最强结论：<例如 NO_DIRECT_MATCH_WITHIN_LOGGED_SCOPE>
本轮明确不允许的结论：<例如 novel / saturated / decision-ready>
是否请求 owner 做 Stage-1C 选择：YES/NO
是否请求 Stage-1B 放行：YES/NO（Stage-1A response 默认必须为 NO）
```

### 3.2 对审查意见的逐项处置表

| Finding ID | Disposition | 证据工件 | 改了什么 | 没改什么 | 剩余风险 | 责任人 | 截止时间 |
|---|---|---|---|---|---|---|---|
| F-01 | `ACCEPTED / PARTIAL / DISPUTED_WITH_EVIDENCE / NOT_STARTED` | commit + path + hash |  |  |  |  |  |

`DISPUTED_WITH_EVIDENCE` 必须给出可检验证据；“我们认为”“AI 复核过”不是证据。

### 3.3 关键主张审计表

| Claim ID | 当前措辞 | 证据等级 | 论文/版本 | 定位 | 审查后措辞 | 状态 |
|---|---|---|---|---|---|---|
| CL-... |  |  |  |  |  | `KEEP / DOWNGRADE / RETRACT / UNRESOLVED` |

至少覆盖：

- 每个 identity 的 closest challenger；
- 每个 `DIRECT_OCCUPIED`；
- 每个数值比较；
- 每个 `NO_DIRECT_MATCH_WITHIN_LOGGED_SCOPE`；
- 每个 `SOTA` 或 “超过业内最优”主张；
- 每个可能改变 owner 选题的 load-bearing claim。

### 3.4 Identity 冻结与防“合取洗白”表

| Identity | 搜索前冻结定义 | 现有直接占据者 | 搜索后新增限定词 | 新限定词是否事先登记 | 结论 |
|---|---|---|---|---|---|
| I2 |  |  |  |  |  |

判定纪律：

- 如果 bare identity 已被占据，必须写 `BARE_IDENTITY_OCCUPIED`；
- 追加“同一核心 + 供给曲面 + Goodhart + 跨任务”等条件只能产生新的**合取身份**，不能倒推 bare identity 未占据；
- “没有单篇论文同时满足五个条件”只能证明精确交集未在已检索范围发现，不能自动证明方法贡献；
- 每个合取身份都要回答：去掉哪一项后科学结论不成立？若任意一项只是包装或工程场景，则 novelty 不成立。

### 3.5 Comparator/SOTA 卡模板

在未满足下列字段前，文件只能叫 `comparator seed cards`，不得叫 `SOTA cards`：

| 字段 | 必填说明 |
|---|---|
| task/data/split | 完全一致，或明确非同分布 |
| input/output protocol | 输入信息和输出约束一致 |
| model/backbone/version | 固定版本；参数量另列，禁止用模型名代参数量 |
| weight update | none / prompt-only / memory / LoRA / full FT / test-time update |
| candidate construction | beam/sample/tool/revision，K 与温度 |
| decision operator | in-pool selection / revision / generation / loop |
| information boundary | 是否使用 label/ref/qrel/外部新信息 |
| metric implementation | 名称、方向、脚本版本 |
| compute budget | calls、tokens/audio seconds、latency、GPU-hours、美元成本 |
| reported result | 原论文值、表号、统计不确定性 |
| reproduction status | claim-verified / reproduced |
| comparability verdict | exact / controlled-adjustment / contextual-only |

只有 `exact` 或有预先声明控制调整的比较，才允许写 “match/beat SOTA”。跨模型、跨 split、跨预算的数字
只能做 contextual reference。

### 3.6 Survey 漏项与下一轮目标

| Gap ID | 缺失文献族/方法族 | 为什么可能推翻结论 | 查询与 citation chase 计划 | 完成判据 | 结果 |
|---|---|---|---|---|---|
| G-01 | general test-time scaling laws | 可能占据 I4 方法对象 |  |  |  |

每个 lane 至少执行：关键词检索、最近邻 backward chase、forward chase、作者/方法别名检索。若某引擎无法
访问，登记失败并使用独立引擎补查；仍不可用则保留 gap，不得写 saturated。

### 3.7 负结果与异常表

| Event/Claim ID | 异常 | 首次发现时间 | 是否影响结论 | 处置 | 未解决原因 |
|---|---|---|---|---|---|

必须包括：网络失败、解析失败、无法取全文、数字冲突、版本变化、重复身份、编码损坏、自动检查漏报、
reviewer disagreement。

## 4. 状态 token 与放行门槛

只允许使用以下状态：

1. `IN_PROGRESS`：原始事件或筛选仍未完成。
2. `ROUND1_SCOUT_COMPLETE`：广度扫描结束；允许形成候选地图，不允许 claim “饱和/唯一/决策就绪”。
3. `CLAIM_AUDIT_COMPLETE`：所有 load-bearing claim 已达 `CLAIM_VERIFIED`，计数与去重可重建。
4. `LOCALLY_SATURATED_WITHIN_PROTOCOL`：满足预注册 saturation rule，所有已知 gap 有处置。
5. `STAGE1C_DECISION_READY`：identity 已冻结、关键比较可比、诚信核查完成、reviewer 签字；owner 仍须亲自选。
6. `CLOSED`：仅用于 owner 已作 Stage-1C 决策且 response 明确记录选题/kill/pivot；Survey AI 无权自行赋值。

结论词的门槛：

| 词语 | 最低状态 |
|---|---|
| `NO_DIRECT_MATCH_WITHIN_LOGGED_SCOPE` | `ROUND1_SCOUT_COMPLETE`，且必须列 scope/gaps |
| `locally saturated` | `LOCALLY_SATURATED_WITHIN_PROTOCOL` |
| `SOTA` | comparator card 满足同任务/协议/预算可比性 |
| `novel` | 不仅 exact intersection 未命中，还要证明 method/conclusion contribution |
| `decision-ready` | `STAGE1C_DECISION_READY` |

禁用裸词：`EMPTY`、无范围限定的 `NO_DIRECT_MATCH`、`unique`、`complete`、`novel`、`SOTA`、
`verified`。必须使用上表中的限定形式。

## 5. 最低自动校验

`validation_report.txt` 必须记录命令、退出码和完整摘要，至少检查：

1. 所有 JSON/JSONL/YAML 可解析；ID 全局唯一；外键无悬挂；
2. `search_events` 的成功/失败、SEARCH/FETCH 分开计数；
3. 每个成功 SEARCH 都有原始响应 hash 和结果行；
4. 每个 included result 都有 screening decision 和 canonical paper；
5. exact unique work 数由 `papers.jsonl` 重算，与 flow report 完全一致；
6. 每个 matrix claim 都有 `claim_id`，每个 `claim_id` 有 version+locator；
7. `FULLTEXT/CLAIM_VERIFIED` 不得由 snippet-only 记录产生；
8. `DIRECT_OCCUPIED` 和数值主张至少双审；
9. 禁词扫描：`EMPTY`、裸 `NO_DIRECT_MATCH`、无门槛 `SOTA/novel/complete`；
10. selection/revision、weight-frozen/trained、same-core/external-verifier 不得同字段混用；
11. 所有 manifest hash 与 git canonical bytes 匹配；
12. response 的状态不高于证据链能够支持的最高状态。

任何一项失败，最终状态自动降为 `IN_PROGRESS` 或 `ROUND1_SCOUT_COMPLETE`；不得由人工写一段解释后忽略。

## 6. Reviewer sign-off

```yaml
signoff:
  survey_lead:
    id: ""
    verdict: ""
    signed_at_utc: ""
  independent_reviewer:
    id: ""
    verdict: ""
    signed_at_utc: ""
  integrity_reviewer:
    id: ""
    verdict: ""
    signed_at_utc: ""
  unresolved_blockers: []
  maximum_permitted_claim: ""
```

独立 reviewer 必须尝试从空环境只凭 manifest 和说明重建以下五项：

1. SEARCH 与 FETCH 的精确事件数；
2. returned/screened/included/excluded 数；
3. exact unique work 数及所有 alias merge；
4. 五个 load-bearing claims 的原文定位；
5. coverage/kill matrix 的生成输入和最终状态。

任一项无法重建，就签 `REPLAY_FAILED`，不得签 `SURVEY_COMPLETE`。

## 7. 给执行 AI 的最终指令

```text
你的任务不是让 response 看起来“都处理完了”，而是让第三方能够发现哪些处理完、哪些没处理完。
不要为满足计数补造事件；不要把摘要核验升级为全文核验；不要把 URL 抓取算成搜索；不要把候选生成或
改写写成选择；不要在看到直接邻居后给 identity 追加限定词并倒称原 identity 仍开放；不要把 exact
intersection 未命中写成科学新颖性；不要把不同模型、数据、split、预算的数字写成 SOTA 比较。

当原始材料缺失时，明确写 RAW_EVENT_UNAVAILABLE，并把允许结论降级。诚实降级是合格 response；
不可回放却声称 complete/verified/decision-ready 是阻断性失败。
```
