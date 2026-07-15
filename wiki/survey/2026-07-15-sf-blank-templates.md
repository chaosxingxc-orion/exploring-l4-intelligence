# Gate S1 签署包：空白记录模板（v2 外审 §6.2 六件套之五）

（本文件 = 执行期各类记录的空白骨架。字段语义见协议 §6/§7/§9 与 amendment-3;哈希正典 =
git blob。**编号纪律（amendment-3 A3-4,消同名异构）**：模板编号 = `REC-1..REC-7`——原
`T1–T6` 编号与 venue 梯队 `T1/T2/T3` 冲突,自本版起废止;历史文件中的旧编号不改写,读旧件时
按「模板语境 T{n} = REC-{n}」映射。）

## REC-1 检索日志行（每次查询一行,JSONL;原 T1）

```json
{"query_id":"SF-L1-Q1","engine":"arxiv_api","query_ref":"2026-07-15-sf-queries.jsonl#record_sha256",
 "page_start":0,"max_results":75,"totalResults":0,"sortBy":"relevance","sortOrder":"descending",
 "timestamp":"<ISO8601>","raw_response_ref":"<文件/可重建ID清单>","response_sha256":"<本页>",
 "n_hits_page":0,"included":[],"excluded":[{"id":"","reason":""}],"failed_request":null}
```

（**每页一行**——A1-4 分页语义;totalResults 每页复记;查询定义一律以 queries.jsonl 行哈希
回指。**分页递归拆分（A3-6）**：totalResults>2000 时按 年→月→日 确定性递归拆分,派生查询
`query_id` = `<父ID>-W<窗口序号>`,行内另记 `parent_query_sha256`——派生行沿用本模板。）

## REC-2 纳排记录行（每篇 INCLUDED 一行,JSONL;原 T2——amendment-3 A3-5 扩展后骨架）

```json
{"id":"","name":"","version_pin":"vN/正式版页","lanes":[],
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
 "source_axes":{"information_source_classes":["①task-native|②pretrained-readout|③deterministic-compute|④endogenous-env-feedback|⑤exogenous-answer-bearing|⑥evaluation-gold"],
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
 "proximity":{"system_level":"","component_level":"","modality":"","tf_strict_compliance":"",
  "black_box_compliance":"","reward_control":"","persistence_state":""},
 "extraction":{"core_access":"","modality_path":"","external_components":"","feedback_type":"",
  "what_changes_at_test_time":"","persistence_scope":"","compute_scaling":"","claimed_mechanism":"",
  "strongest_result":"","failure_mode":"","reusable_implementation":""},
 "resource_axes":{"model_calls":"","tool_calls":"","tokens":"","latency_cost":"","horizon":"","stopping":""},
 "most_threatened_rq":["RQ-SYS|RQ-CTRL|RQ-OMNI|RQ-SAFE|RQ-MEASURE|none(须附一句理由)"],
 "venue_tier":"T1|T2|T3","topic_relevance":"core|element",
 "evidence_axes":{"verification_depth":"DISCOVERED|ABSTRACT_VERIFIED|FULLTEXT_OPENED|CLAIM_VERIFIED|REPRODUCED",
  "publication_status":"preprint|peer-reviewed|withdrawn|retracted",
  "study_quality":{"rating":"HIGH|MEDIUM|LOW","reason":"<数据边界/对照公平/统计不确定性/消融/复现性/代码可得/claim-evidence match 一句裁决>"},
  "quality_override":"none|T2_PROMOTED:<理由>|T1_DEMOTED:<理由>"},
 "dfs_trigger":["T-a对象|T-b问题|T-c要素|T-d结论冲突(空=仅BFS)"],
 "method_occupation":{"method_gist":"","method_limitations":"",
  "improvement_space":"三小问齐备才有效:①哪条轴②为何到不了③对哪个RQ/阈值有实质影响",
  "borrowable":""},
 "evidence_grade":"DISCOVERED|ABSTRACT_VERIFIED|FULLTEXT_OPENED|CLAIM_VERIFIED|REPRODUCED",
 "claim_locators":[{"claim":"","locator":"vN §/p./Table/Eq.","span":""}]}
```

（**A3-5 字段语义补注**：`evidence_grade` 与 `evidence_axes.verification_depth` 同标尺——
前者为兼容保留,冲突时以 `evidence_axes` 为准;`source_axes.information_source_classes` 按
信息来源六类分解登记（README token 块）,⑤类增益禁概括为「激活预训练知识」;`rl_identity`
九字段供 SF-L9 谱系裁决「RL/planning/search/bandit/metareasoning」;`omni_axes` 五轴对应
omni 合同五轴分离——`modality_path` 为粗标签保留,承重判断以五轴为准;`tf_audit` 扩展四字段
区分「冻结通用工具」与「为本任务新训组件」;`study_quality`/`quality_override` 按 A3-2 梯队
先验+质量覆盖规则使用。）

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
