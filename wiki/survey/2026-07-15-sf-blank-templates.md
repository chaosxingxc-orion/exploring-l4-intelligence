# Gate S1 签署包：空白记录模板（v2 外审 §6.2 六件套之五）

（本文件 = 执行期各类记录的空白骨架。字段语义见协议 §6/§7/§9 与 amendments 3–4;哈希正典 =
git blob。**编号纪律（amendment-3 A3-4,消同名异构）**：模板编号 = `REC-0..REC-7`——原
`T1–T6` 编号与 venue 梯队 `T1/T2/T3` 冲突,自 A3-4 起废止;历史文件中的旧编号不改写,读旧件时
按「模板语境 T{n} = REC-{n}」映射;`REC-0` 为 correction #4 C4-4 新增的工作级主账,编号取 0
因其在管线上游于一切现有模板。）

## REC-0 工作级筛选/去重/裁决主账行（每个 canonical work 一行,不限 INCLUDED;correction #4 C4-4 新增）

```json
{"canonical_id":"<arXiv ID|DOI>","title":"",
 "source_hits":[{"source":"query:SF-L1-Q1|route:SF-T1R-ACL-2024|citation_graph:<父节点>|seed:manifest行号","hit_ref":"<REC-1 行/REC-7 resolution 项回指>"}],
 "dedup":{"merged_from":["<被并 ID/表述变体>"],"merge_basis":"same_arxiv_id|doi_match|title_normalized_exact|fuzzy_adjudicated:<裁决人>"},
 "screening_stage":"TITLE|ABSTRACT|FULLTEXT",
 "decision":"INCLUDED|EXCLUDED|DUPLICATE|UNOBTAINABLE",
 "reason_code":"NOT_RELEVANT|WRONG_OBJECT|DUPLICATE_OF:<id>|REMOVED_PAYWALLED_UNOBTAINABLE|REMOVED_UNOBTAINABLE|INFO_BOUNDARY_FAIL|OTHER:<登记后使用>",
 "reason_text":"<一句理由;EXCLUDED/UNOBTAINABLE 必填>",
 "screener":"<初筛人/代理>","screened_at":"<ISO8601>",
 "second_reviewer":"<复核人;无=null>","adjudicator":"<分歧裁决人;无分歧=null>","adjudication_note":null,
 "fulltext_version_ref":"<vN/正式版页;FULLTEXT 阶段起必填>",
 "extraction":{"rec2_backref":"<REC-2 行回指;仅 INCLUDED>","extractor":"","extracted_at":""},
 "coding_depth":"D0|D1|D2"}
```

（**完整纳排链条正典**：任何命中工作无论终态都必须有一行——同一 work 被多少查询/route/引文
边命中、如何合并、在哪一阶段因何排除、谁筛谁核谁裁、抽取回指哪个固定版本,全部可由本表回放;
`coding_depth` = amendment-4 编码深度纪律〔D0=本行即全部;D1=INCLUDED 精简核;D2=承重全合同〕,
承重 claim 必须回指 `coding_depth:"D2"` 的 REC-2 行。**validator 已实装〔C4A/P0-R3〕** =
`scripts/survey/sf_record_validator.py`（V1–V13,正负 fixtures =
`wiki/survey/fixtures-c4a/`,固定输出 = `docs/checks/2026-07-16-sf-record-validator-test.json`）;
**INCLUDED ⇒ `reason_code` 必为 null（机器强制,消模板歧义）**,EXCLUDED/UNOBTAINABLE ⇒
枚举 reason_code + 非空 reason_text,DUPLICATE ⇒ `DUPLICATE_OF:<id>`;flow 五计数由本表
机器导出,手填不一致 = FAIL。）

## REC-1 检索日志行（每次查询一行,JSONL;原 T1）

```json
{"query_id":"SF-L1-Q1","engine":"arxiv_api","query_ref":"2026-07-15-sf-queries.jsonl#record_sha256",
 "page_start":0,"max_results":75,"totalResults":0,"sortBy":"relevance","sortOrder":"descending",
 "timestamp":"<ISO8601>","raw_response_ref":"<文件/可重建ID清单>","response_sha256":"<本页>",
 "n_hits_page":0,"included":[],"excluded":[{"id":"","reason":""}],"failed_request":null}
```

（**每页一行**——A1-4 分页语义;totalResults 每页复记;查询定义一律以 queries.jsonl 行哈希
回指。**分页递归拆分（A3-6;correction #4 C4-5 补全可重放字段）**：totalResults>2000 时按
年→月→日 确定性递归拆分,单日仍 >2000 = **硬停止**并登记 `API_LIMIT_SINGLE_DAY_OVER_2000`
（绝不静默截断）。派生行沿用本模板,**另须逐字段携带**：`date_from / date_to /
timezone:"GMT" / boundary_semantics(闭区间分钟粒度) / decoded_search_query /
url_encoded_search_query / query_sha256(decoded 串哈希) / parent_query_sha256 /
split_level(YEAR|MONTH|DAY,C4A/P0-R2 年层实装) / split_ordinal / trigger_totalresults`;
`query_id` = `<父ID>-W<窗口序号>` 逐级递归适用。**拆分规范实现 =
`scripts/survey/sf_child_query_split.py`**——执行器必须经 `parent_from_frozen_row` 适配冻结
行（`record_sha256`=整记录哈希,`query_sha256`=decoded 串哈希,两类哈希机器强制分离）后调用
其 `split_query`,派生记录逐字取其输出;断点续跑 = `remaining_after`、落账前查重 =
`assert_unique_ids`（均为规范函数）。确定性证据 = 离线合成 replay test
`docs/checks/2026-07-16-sf-child-query-replay-test.json`（10/10 PASS,首个 overflow 必为
SPLIT_YEAR）+ 真实行集成 dry-run
`docs/checks/2026-07-16-sf-child-query-realrow-dryrun.json`（17/17 PASS,全部冻结行无
KeyError 进入规范函数,负例逐项触发硬错误）。**执行纪律**：调用间隔 ≥3s、失败指数退避、断点自最后完整落账窗口
续跑（均入 REC-1,arXiv API 手册口径）。）

## REC-2 抽取记录行（每篇 INCLUDED 一行,JSONL;原 T2——A3-5 扩展 + correction #4 C4-2/C4-4 修订;工作级纳排主账 = REC-0）

```json
{"id":"","name":"","version_pin":"vN/正式版页","lanes":[],"coding_depth":"D1|D2","rec0_backref":"<REC-0 行回指>",
 "matrix":{"core_access":"weights|logits|hidden-state|attention|API-text|API-multimodal",
  "parameter_update":"none|prompt|adapter|full",
  "external_state_update":"none|memory|skill|tree","reward_type":"gold|verifier|self|env|none",
  "policy_update":"none|nonparametric|trained","modality_path":"text|audio-native|audio-tool|vision|omni",
  "tool_use":"none|fixed|routed|learned","budget_horizon":"单步|固定K|多轮|任意","task":"",
  "trained_comparator":"Y|N"},
 "tf_audit":{"base_model_updated":"Y|N","external_component_trained":"Y|N:<对象>",
  "component_pretrained":"Y|N:<哪些组件系既有预训练参数>",
  "method_specific_parameter_training":"Y|N:<是否为本任务/系统新训参数>",
  "test_time_parameter_update":"Y|N",
  "nonparametric_persistence":"within_item|across_items|none",
  "ground_truth_used":"无|预先|开发集|测试时",
  "learned_object":"token-prior|value-fn|verifier|prompt|memory|skill|tool|code|workflow|graph|index|exemplar|none|other:<登记后使用>",
  "learning_time":"test前|test中","test_time_readonly":"Y|N"},
 "source_axes":{"information_source_classes":["TASK_NATIVE","PRETRAINED_READOUT","DETERMINISTIC_COMPUTE","ENDOGENOUS_ENV_FEEDBACK","EXOGENOUS_ANSWER_BEARING","EVALUATION_GOLD"],
  "answer_bearing_external_info":"Y|N|UNCLEAR",
  "gold_path_audit":"<gold 是否以任何路径进入 selector/reward/prompt/检索/候选构造;一句证据>",
  "activation_attribution":"readout|new_info|mixed|not_claimed"},
 "omni_axes":{"core_model_modal_capability":"<核心模型本身的模态能力>",
  "observation_seen_by_core":"<冻结核心亲见的观察:原始模态|表征|文字摘要>",
  "tool_input_output_modalities":"<工具的输入/输出模态>",
  "action_modality":"<agent 行动作用的模态/环境>",
  "multimodal_causal_grounding_evidence":"<非文本模态因果改变决策的证据;无则 none>"},
 "rl_identity":{"state_definition":"","action_definition":"","feedback_definition":"",
  "transition_or_controller":"","policy_representation":"","cross_step_update_object":"",
  "credit_assignment":"","stopping_rule":"","authors_call_it_rl":"Y|N"},
 "proximity":{"system_level_proximity":"","component_level_proximity":"","modality_proximity":"",
  "tf_strict_compliance":"","black_box_compliance":"","reward_control_proximity":"",
  "persistence_state_proximity":""},
 "extraction":{"core_access":"","modality_path":"","external_components":"","feedback_type":"",
  "what_changes_at_test_time":"","persistence_scope":"","compute_scaling":"","claimed_mechanism":"",
  "strongest_result":"","failure_mode":"","reusable_implementation":""},
 "resource_axes":{"model_calls":"","tool_calls":"","tokens":"","latency_cost":"","horizon":"","stopping":""},
 "most_threatened_rq":["RQ-SYS|RQ-CTRL|RQ-OMNI|RQ-SAFE|RQ-MEASURE|none(须附一句理由)"],
 "venue_tier":"T1|T2|T3","topic_relevance":"core|element",
 "evidence_axes":{"verification_depth":"DISCOVERED|ABSTRACT_VERIFIED|FULLTEXT_OPENED|CLAIM_VERIFIED|REPRODUCED",
  "publication_status":"preprint|peer-reviewed|withdrawn|retracted",
  "study_quality":{
   "data_boundary":{"verdict":"PASS|PARTIAL|FAIL|UNCLEAR|NA","reason":"","locator":""},
   "control_fairness":{"verdict":"PASS|PARTIAL|FAIL|UNCLEAR|NA","reason":"","locator":""},
   "uncertainty_reporting":{"verdict":"PASS|PARTIAL|FAIL|UNCLEAR|NA","reason":"","locator":""},
   "ablation_attribution":{"verdict":"PASS|PARTIAL|FAIL|UNCLEAR|NA","reason":"","locator":""},
   "reproducibility":{"verdict":"PASS|PARTIAL|FAIL|UNCLEAR|NA","reason":"","locator":""},
   "artifact_availability":{"verdict":"PASS|PARTIAL|FAIL|UNCLEAR|NA","reason":"","locator":""},
   "claim_evidence_match":{"verdict":"PASS|PARTIAL|FAIL|UNCLEAR|NA","reason":"","locator":""},
   "summary_rating":"HIGH|MEDIUM|LOW(仅由分维导出或人工裁决登记,不得替代分维)","coder":""}},
 "dfs_trigger":["T-a对象|T-b问题|T-c要素|T-d结论冲突(空=仅BFS)"],
 "method_occupation":{"method_gist":"","method_limitations":"",
  "improvement_space":"三小问齐备才有效:①哪条轴②为何到不了③对哪个RQ/阈值有实质影响",
  "borrowable":""},
 "claim_locators":[{"claim":"","locator":"vN §/p./Table/Eq.","span":""}]}
```

（**A3-5/C4 字段语义补注**：`evidence_grade` **已从填写模板移除**——正典 =
`evidence_axes.verification_depth`,兼容字段仅在导出层生成〔C4-4〕;
`source_axes.information_source_classes` = **多选枚举数组**,示例列出全枚举域,填写时仅留
实际适用类〔①..⑥ 圆圈序号映射:①TASK_NATIVE ②PRETRAINED_READOUT ③DETERMINISTIC_COMPUTE
④ENDOGENOUS_ENV_FEEDBACK ⑤EXOGENOUS_ANSWER_BEARING ⑥EVALUATION_GOLD〕,⑤类增益禁概括为
「激活预训练知识」;`rl_identity` 九字段供 SF-L9 谱系裁决;`omni_axes` 五轴对应 omni 合同
五轴分离——`modality_path` 为粗标签保留,承重判断以五轴为准;`tf_audit` 扩展四字段区分
「冻结通用工具」与「为本任务新训组件」;`study_quality` = **七维结构化**〔C4-2,owner 裁决①:
venue_tier 零证据权重,承重全由本块决定;`quality_override` 已退役〕;`proximity` 键名与协议
§6 范围多轴列表逐字一致〔C4-4〕;**编码深度**〔amendment-4;C4A/P0-R3 类型稳定修订〕：D1 行必填 = 身份元数据 +
topic_relevance + proximity + publication_status + venue_tier + dfs_trigger +
verification_depth,其余块可整块折叠,**折叠唯一合法形态 = 类型稳定对象
`{"status":"NA","reason":"<非空理由>"}`——裸字符串 `"NA:<理由>"` 自 C4A 起为 validator
FAIL（同字段异类型消除）**;D2〔承重;触发 = 被 claim 引用 ∨ initial_tag 含 DIRECT_THREAT ∨
`topic_relevance:"core"`（评审扩张,owner 2026-07-16 接受）〕= 全字段 + study_quality 七维
完整（非 NA 维必带 locator）+ claim_locators 非空;DIRECT_THREAT 行另须
`threat_dual_coding`（双抽取人相异 + rec5_ref + 有分歧必有裁决人）。承重 claim 只能回指
D2 行——以上全部由 `sf_record_validator.py` 机器强制,不再是纸面承诺。）

## REC-3 census 增量行 / REC-4 ledger 增量行（原 T3/T4）

沿用 census v2 / ledger v2 现行 schema（`wiki/survey/2026-07-14-canonical-census-v2/` 为骨架
正典）：census = canonical ID + 版本钉 + 全作者 + venue;ledger = 一 claim × 一 work × 一 span
+ 五级 discrepancy。新增行标 `batch:"SF-SURVEY-2026"`。

## REC-5 threat 双人抽取对照表（每篇一份;原 T5）

```
paper: <ID name>   extractor_A: <代理标识>   extractor_B: <代理标识>（互不见对方产出）
| 字段(REC-2 全字段) | A 编码 | B 编码 | 一致? | 协调者裁决+理由 |
候选池完整登记清单与两评审排序/分歧记录:见 threat-pool-provenance 文件（修正案 E）
```

## REC-6 taxonomy 修订记录（版本化增补,§10;原 T6）

```
amendment_id / date / 触发证据(论文+locator) / 旧类别 → 新类别 / 影响面(需重编码的记录数) / 生效批次
```

## REC-7 T1 proceedings route 日志（每 route 一份,JSON;amendment-3 A3-3 新增）

```json
{"route_id":"SF-T1R-ACL-2024","venue":"ACL","year":2024,
 "entry_url_resolved":"<执行时实际入口;与 routes manifest 冻结入口的差异须注明>",
 "route_status_at_execution":"READY|NOT_YET_PUBLISHED|NOT_HELD|ENTRY_TO_RESOLVE",
 "keyword_vocab_version":"v1","raw_title_list_sha256":"<本地备份件哈希>",
 "n_titles_total":0,"n_matched":0,"n_resolved_arxiv":0,"n_rescued_oa":0,"n_paywalled_removed":0,
 "resolution":[{"title":"","match_method":"exact_normalized|fuzzy_adjudicated|manual",
  "resolved_id":"<arXiv ID|DOI|UNRESOLVED>",
  "full_text_status":"arxiv|oa_backup|REMOVED_PAYWALLED_UNOBTAINABLE"}],
 "timestamp":"<ISO8601>","notes":""}
```

（route 定义正典 = `2026-07-16-sf-t1-proceedings-routes.md`;五计数字段机器汇总禁口算;
`n_paywalled_removed` 明细进 flow report——占据类结论的移除计数披露义务锚点。）
