---
artifact_id: "SF-PROTOCOL-AMENDMENT-4-2026-07-16"
title: "检索协议 amendment-4（correction #4）——博导复审 WITHHOLD 六项窄幅整改"
date: 2026-07-16
trigger: "《Gate S1 再送签申请的 Stage-1A 博导级对抗复审》裁决 WITHHOLD SIGNATURE — TARGETED CORRECTION #4 REQUIRED（G2/G3/G4-ledger/G6 未闭 + cs.SE/cs.HC 盲区）；owner 四裁决 = Decision-Log 续61"
mutation_policy: "一修正案一件（A3 后纪律）；协议本体同步折入处逐处标 C4-n；被取代语义按 dated supersession 留读法注记，不改写历史件"
attestation: "联网检索查询执行数 = 0 维持不变。ID_DEREFERENCE 访问类（本件 §1 注册,owner 裁决②）：21 次访问（14 目标正典 pass + 传输错误重试 + 投稿日补取）,16 HIT / 5 传输错误重试后全部闭合,逐次留痕 = 2026-07-16-sf-id-dereference-log.jsonl（22 行含表头）"
---

# 检索协议 amendment-4（correction #4）

## §0 六项对照表

| # | 内容 | 取代（dated supersession） | 依据 |
|---|---|---|---|
| C4-1 | 完成性表述分层更正——由独立回应信承载（`2026-07-16-gate-s1-correction-4-response.md`）：G3 完成态夸张认错更正;G4/G6 记「原要求已闭+本轮新增要求接受并交付」;G2 记「披露偏离经评审驳回、owner 改判」;每个完成态动词带 artifact+hash+复跑命令 | 续60 申请书的「G1–G6 全闭合」表述 | 评审 §2.2/§12/C4-1 |
| C4-2 | **venue_tier 零证据权重**：只承载 T1 手扫范围标记 + §4bis 排序键平局 + coverage 分层描述;`T2_UNREVIEWED`/`T1_DEMOTED`/`T2_PROMOTED` 三 token 退役;`publication_status` 独立表达同行评审状态;`study_quality` **七维结构化**（每维 verdict+reason+locator,总评仅可导出/裁决登记）——协议 §2/§6 已折入,REC-2 模板已改版,三合成验收案例 = 本件 §3 | A3-2「默认先验+双向覆盖」权重语义（owner 裁决① 续61,取代续59 裁决②对应部分） | 评审 G2/C4-2 + owner 裁决① |
| C4-3 | **50 route 逐条序列化**：`2026-07-16-sf-t1-routes.jsonl`（50 行,逐行唯一 route_id/exact URL 或显式 ENTRY_TO_RESOLVE\|NOT_HELD\|NOT_YET_PUBLISHED/判断依据与时点/词表 hash 钉定/执行期字段占位）+ 词表机器正典 `2026-07-16-sf-t1-wordlist-v1.json`（raw 73 / **双侧归一化后有效 71**,合并对显式登记）+ 仓内只读 validator `scripts/survey/sf_t1_routes_validate.py` + 持久化输出 `docs/checks/2026-07-16-sf-t1-routes-validation.json`（**12/12 PASS**） | routes.md §6「脚本证据在会话记录」的验证职能（该 md 表述保留作历史;机器正典自此 = jsonl+validator） | 评审 G3/C4-3 |
| C4-4 | **REC-0 工作级筛选/去重/裁决主账**（每 canonical work 一行不限 INCLUDED,含 source_hits/dedup provenance/stage/reason_code/screener/adjudicator/版本 ref/REC-2 回指）+ schema 三修（`proximity` 键名与协议 §6 逐字统一;`evidence_grade` 移出填写模板、正典=verification_depth;`information_source_classes` 真枚举数组）——三合成 lineage 验收案例 = 本件 §4 | REC-2「仅 INCLUDED 建行」的纳排链断裂;A3-5 兼容字段并存语义 | 评审 G4/C4-4 |
| C4-5 | **派生查询可重放**：REC-1 派生行强制字段（date_from/date_to/GMT/闭区间语义/decoded/encoded/query_sha256/parent_sha256/split_level/split_ordinal/trigger_totalresults）;单日 >2000 = 硬停止 `API_LIMIT_SINGLE_DAY_OVER_2000`;节流 ≥3s/指数退避/断点续跑;**规范实现** = `scripts/survey/sf_child_query_split.py`（执行器必须调用）,离线合成 replay test = `scripts/survey/sf_child_query_replay_test.py` → `docs/checks/2026-07-16-sf-child-query-replay-test.json`（**9/9 PASS**:同父+同计数→逐字相同子查询与 hash） | A3-6 只记 `<父ID>-W<n>`+父 hash 的不可重建态 | 评审 G6/C4-5 |
| C4-6 | **类目盲区补救 + sentinel recall**：① `ID_DEREFERENCE` 前置核验（§1;14/14 HIT 零幻觉,含 AgentEval cs.SE 零 cross-list、v1=2026-07-08 在窗内的坐实）② **SF-L10 受控类目道**（cs.SE+cs.HC 两类,2 条查询;编译器 sfqc-1.2.0 append-only,**53 条,前 51 行逐字节不变**——前缀 sha256 `4e406580…` 两侧一致）③ 离线 sentinel recall `scripts/survey/sf_sentinel_recall_test.py` → `docs/checks/2026-07-16-sf-sentinel-recall.json`（**9 HIT + 5 EXPLAINED_MISS,零 unexplained**）④ 种子批次3 +13 = **87 条**（74 前缀不变;入册前置 = ID 核验,owner 裁决②） | A3-8「51 条」计数口径;batch-2 VideoAgent「存在性待核」遗留项（已闭合） | 评审 §9.2/§9.3/C4-6 + owner 裁决② |

## §1 `ID_DEREFERENCE` 访问类注册（owner 裁决② 续61）

- **定义**：按已知 arXiv ID / DOI 取对应元数据页（abs 页）,核验存在性 + 题名与引用描述一致性
  （可附带捕获类目/摘要/投稿日作离线测试输入）。**无查询串、无结果排序、无发现行为**。
- **与零查询边界的关系**：不计入 `queries_executed`——「联网检索查询执行数 = 0」语义保持为真;
  但**逐次留痕**（id / 时刻 UTC / 工具 / HTTP 状态 / 裁决 HIT|MISMATCH|UNRESOLVED）入机器可读
  日志,且 attestation 文字必须显式披露访问类与次数（本件 frontmatter 即范例）。
- **触发场景**：外部点名论文（评审/owner/合作者）入种子清单前的反幻觉核验（裁决②：「错误
  或者幻觉会累积」→ 前置强制）;既有 UNVERIFIED 条目的闭合。
- **MISMATCH/UNRESOLVED 处置**：不入种子、留痕、在对点名方的回应中指明。本轮 14/14 HIT。

## §2 编码深度纪律（D0/D1/D2 + 承重时点编码;owner 裁决④——预注册,请评审在窄幅复核中一并裁决）

- **D0（REC-0 主账行）**：每个 canonical 命中一行,书目字段允许脚本自 API 元数据预填,人只填
  裁决字段。**任何命中工作的最低记录义务。**
- **D1（REC-2 精简核,INCLUDED 即触发）**：身份元数据 + `topic_relevance` + `proximity` 全轴 +
  `publication_status` + `venue_tier` + `dfs_trigger` + `verification_depth`;其余块可整块
  `"NA:<理由>"` 折叠（如无 RL 宣称的工作免填 rl_identity 九字段——折叠留痕,非留空）。
- **D2（承重全合同）**：工作被用于**支撑/摧毁/占据任何 claim**（mapping 报告引用其数字/结论,
  或 initial_tag 含 DIRECT_THREAT）即强制全字段 + `study_quality` 七维完整。
- **三道防走样闸**：① validator 规则——报告中任何承重 claim 必须回指 `coding_depth:"D2"` 的
  REC-2 行,缺失即 FAIL;② NA 折叠必须带理由,禁无痕留空;③ 本纪律预注册于此、向评审明示,
  非事后偏离。
- **方法学依据**：PRISMA 系质量评估惯例即只对进入综合（synthesis）的研究执行——code-on-use
  与之同构;吞吐粗估 ~30h（≈300 命中×1.5min + ≈80 INCLUDED×8min + ≈30 承重×25min）对全员
  全合同 ≈53h+,承重处记录密度不降反升。**若评审坚持全部 INCLUDED 七维编码,按评审裁决执行**
  （吞吐差额如实呈报 owner）。

## §3 C4-2 验收：三合成编码案例（评审验收标准原文——「三者能得到不矛盾的编码」）

```json
{"case":"A 高质量非T1同行评审(合成TMLR式)","venue_tier":"T2","publication_status":"peer-reviewed",
 "study_quality":{"data_boundary":{"verdict":"PASS"},"control_fairness":{"verdict":"PASS"},
  "uncertainty_reporting":{"verdict":"PASS"},"ablation_attribution":{"verdict":"PASS"},
  "reproducibility":{"verdict":"PASS"},"artifact_availability":{"verdict":"PASS"},
  "claim_evidence_match":{"verdict":"PASS"},"summary_rating":"HIGH"},
 "承重结论":"实验数字可承重——tier 不构成障碍;旧制下会被误标 T2_UNREVIEWED 的病例,新制消除"}
{"case":"B 低质量T1(合成)","venue_tier":"T1","publication_status":"peer-reviewed",
 "study_quality":{"data_boundary":{"verdict":"FAIL","reason":"测试集泄漏疑点无消解"},
  "control_fairness":{"verdict":"PARTIAL"},"uncertainty_reporting":{"verdict":"FAIL"},
  "ablation_attribution":{"verdict":"UNCLEAR"},"reproducibility":{"verdict":"FAIL"},
  "artifact_availability":{"verdict":"FAIL"},"claim_evidence_match":{"verdict":"PARTIAL"},
  "summary_rating":"LOW"},
 "承重结论":"实验数字不承重——T1 身份不提供任何默认可信度;旧制下需显式 T1_DEMOTED,新制默认即不承重"}
{"case":"C 未审preprint带priority threat(合成)","venue_tier":"T2","publication_status":"preprint",
 "study_quality":{"summary_rating":"MEDIUM","claim_evidence_match":{"verdict":"PARTIAL"},
  "data_boundary":{"verdict":"UNCLEAR"},"control_fairness":{"verdict":"UNCLEAR"},
  "uncertainty_reporting":{"verdict":"PARTIAL"},"ablation_attribution":{"verdict":"UNCLEAR"},
  "reproducibility":{"verdict":"PARTIAL"},"artifact_availability":{"verdict":"PASS"}},
 "threat判定":"tier-blind——novelty/priority 威胁成立(其方法宣称先占我方身份组合)",
 "承重结论":"威胁判定与实验可信度分离：可摧毁首创宣称,其实验数字按七维不足不承重——三案例互不矛盾"}
```

## §4 C4-4 验收：三合成 lineage 案例（评审验收标准原文——「完整 lineage」）

```json
{"case":"① 查询+venue双命中合并","canonical_id":"9901.00001",
 "source_hits":[{"source":"query:SF-L1-Q1","hit_ref":"REC-1#L42"},{"source":"route:SF-T1R-ACL-2024","hit_ref":"REC-7#resolution[7]"}],
 "dedup":{"merged_from":["9901.00001v1标题变体"],"merge_basis":"title_normalized_exact"},
 "screening_stage":"FULLTEXT","decision":"INCLUDED","reason_code":null,"reason_text":null,
 "screener":"coder-A","second_reviewer":"coder-B","adjudicator":null,
 "fulltext_version_ref":"v2","extraction":{"rec2_backref":"REC-2#L17","extractor":"coder-A"},"coding_depth":"D2"}
{"case":"② 摘要期排除","canonical_id":"9902.00002",
 "source_hits":[{"source":"query:SF-L7-Q3","hit_ref":"REC-1#L98"}],
 "dedup":{"merged_from":[],"merge_basis":"same_arxiv_id"},
 "screening_stage":"ABSTRACT","decision":"EXCLUDED","reason_code":"NOT_RELEVANT",
 "reason_text":"Goodhart 计量经济学语境,无 LLM/agent 触点","screener":"coder-A",
 "second_reviewer":null,"adjudicator":null,"fulltext_version_ref":null,
 "extraction":null,"coding_depth":"D0"}
{"case":"③ 全文不可得","canonical_id":"DOI:10.1145/9999999",
 "source_hits":[{"source":"route:SF-T1R-MM-2023","hit_ref":"REC-7#resolution[12]"}],
 "dedup":{"merged_from":[],"merge_basis":"doi_match"},
 "screening_stage":"FULLTEXT","decision":"UNOBTAINABLE","reason_code":"REMOVED_PAYWALLED_UNOBTAINABLE",
 "reason_text":"无 arXiv 版无免费官方版;ID+题名+venue 入 flow report 计数披露","screener":"coder-A",
 "second_reviewer":null,"adjudicator":null,"fulltext_version_ref":null,
 "extraction":null,"coding_depth":"D0"}
```

## §5 工件与复跑清单（每个完成态动词的证据锚）

| 工件 | path | 复跑命令 | 状态 |
|---|---|---|---|
| routes 序列化 | `wiki/survey/2026-07-16-sf-t1-routes.jsonl`（50 行） | — | 落盘 |
| 词表机器正典 | `wiki/survey/2026-07-16-sf-t1-wordlist-v1.json`（73/71） | — | 落盘 |
| routes validator | `scripts/survey/sf_t1_routes_validate.py` → `docs/checks/2026-07-16-sf-t1-routes-validation.json` | `python scripts/survey/sf_t1_routes_validate.py` | 12/12 PASS |
| 拆分规范实现 | `scripts/survey/sf_child_query_split.py` | —（被 test 调用） | 落盘 |
| replay test | `scripts/survey/sf_child_query_replay_test.py` → `docs/checks/2026-07-16-sf-child-query-replay-test.json` | `python scripts/survey/sf_child_query_replay_test.py` | 9/9 PASS |
| 编译器 sfqc-1.2.0 | `scripts/survey/sf_query_compiler.py` → `wiki/survey/2026-07-15-sf-queries.jsonl`（53 行） | `python scripts/survey/sf_query_compiler.py` | 13/13 PASS;51 行前缀 sha256 两侧一致 |
| ID 核验留痕 | `wiki/survey/2026-07-16-sf-id-dereference-log.jsonl`（22 行） | —（网络访问,不复跑;裁决可独立重核验） | 14/14 HIT |
| sentinel 数据 | `wiki/survey/2026-07-16-sf-sentinel-data.json` | — | 落盘 |
| sentinel recall | `scripts/survey/sf_sentinel_recall_test.py` → `docs/checks/2026-07-16-sf-sentinel-recall.json` | `python scripts/survey/sf_sentinel_recall_test.py` | PASS（9 HIT/5 EXPLAINED） |
| 种子批次3 | `wiki/survey/2026-07-15-sf-seed-manifest.jsonl`（87 行,74 前缀不变）+ report 批次3 节 | — | 落盘 |
| REC-0 模板与 REC-1/REC-2 修订 | `wiki/survey/2026-07-15-sf-blank-templates.md` | — | 落盘 |
| 协议折入处 | `2026-07-15-system-first-survey-protocol-v1.md`（标 C4-n 各处） | — | 落盘 |

（offline recall 的匹配近似口径——无词干化+轻量复数容忍+连字符折叠——已写入 recall 报告
`matching_caveat`;HIT 方向保守可信,终证以执行期实测为准。）
