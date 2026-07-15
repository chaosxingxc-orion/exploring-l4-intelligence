# Gate S1 签署包：空白记录模板（v2 外审 §6.2 六件套之五）

（本文件 = 执行期各类记录的空白骨架。字段语义见协议 §6/§7/§9;哈希正典 = git blob。）

## T1 检索日志行（每次查询一行,JSONL）

```json
{"query_id":"SF-L1-Q1","engine":"arxiv_api","exact_query":"<逐字>","window":"2022-10-01..2026-07-15",
 "cap":75,"sort":"relevance","timestamp":"<ISO8601>","raw_response_ref":"<文件/可重建ID清单>",
 "n_hits":0,"included":[],"excluded":[{"id":"","reason":""}],"failed_request":null}
```

## T2 纳排记录行（每篇 INCLUDED 一行,JSONL）

```json
{"id":"","name":"","version_pin":"vN/正式版页","lanes":[],
 "matrix":{"core_access":"weights|logits|API-text","parameter_update":"none|prompt|adapter|full",
  "external_state_update":"none|memory|skill|tree","reward_type":"gold|verifier|self|env|none",
  "policy_update":"none|nonparametric|trained","modality_path":"text|audio-native|audio-tool|vision|omni",
  "tool_use":"none|fixed|routed|learned","budget_horizon":"单步|固定K|多轮|任意","task":"",
  "trained_comparator":"Y|N"},
 "tf_audit":{"base_model_updated":"Y|N","external_component_trained":"Y|N:<对象>",
  "ground_truth_used":"无|预先|开发集|测试时","learned_object":"token-prior|value-fn|verifier|prompt|none",
  "learning_time":"test前|test中","test_time_readonly":"Y|N"},
 "proximity":{"system_level":"","component_level":"","modality":"","tf_strict_compliance":"",
  "black_box_compliance":"","reward_control":"","persistence_state":""},
 "extraction":{"core_access":"","modality_path":"","external_components":"","feedback_type":"",
  "what_changes_at_test_time":"","persistence_scope":"","compute_scaling":"","claimed_mechanism":"",
  "strongest_result":"","failure_mode":"","reusable_implementation":""},
 "resource_axes":{"model_calls":"","tool_calls":"","tokens":"","latency_cost":"","horizon":"","stopping":""},
 "evidence_grade":"DISCOVERED|ABSTRACT_VERIFIED|FULLTEXT_OPENED|CLAIM_VERIFIED|REPRODUCED",
 "claim_locators":[{"claim":"","locator":"vN §/p./Table/Eq.","span":""}]}
```

## T3 census 增量行 / T4 ledger 增量行

沿用 census v2 / ledger v2 现行 schema（`wiki/survey/2026-07-14-canonical-census-v2/` 为骨架
正典）：census = canonical ID + 版本钉 + 全作者 + venue;ledger = 一 claim × 一 work × 一 span
+ 五级 discrepancy。新增行标 `batch:"SF-SURVEY-2026"`。

## T5 threat 双人抽取对照表（每篇一份）

```
paper: <ID name>   extractor_A: <代理标识>   extractor_B: <代理标识>（互不见对方产出）
| 字段(T2 全字段) | A 编码 | B 编码 | 一致? | 协调者裁决+理由 |
候选池全集与两评审排序/分歧记录:见 threat-pool-provenance 文件（修正案 E）
```

## T6 taxonomy 修订记录（版本化增补,§10）

```
amendment_id / date / 触发证据(论文+locator) / 旧类别 → 新类别 / 影响面(需重编码的记录数) / 生效批次
```
