---
title: "Stage-1C v2 Agentic RC2 independent method review"
date: "2026-07-24"
artifact_type: "REVIEWER_FACING_DOCTORAL_SUPERVISOR_ASSESSMENT"
campaign: "system-first-stage1c-v2-precalibration"
round: "agentic-rc2-independent-method-review"
review_target_commit: "74cf8e4b565a9e53ff40f9dbc34961ede853dd57"
review_package_manifest_path: "wiki/survey/workbench/system-first-stage1c-v2-precalibration/review-package-manifest-rc2.json"
review_package_manifest_git_blob: "090a66455e9afa52c794ba7109f62381bca32802"
review_package_manifest_sha256: "9abdb94fd35b7eb8f1f9255b8616e7934b06e9fc0eae054b52fea2d4eae46e8f"
recommended_verdict: "WITHHOLD_WITH_BOUNDED_DEFECTS"
authority_effect: "NONE_REVIEWER_FACING_ADVICE"
human_signature_claimed: false
reviewer_is_calibration_coder: false
coder_distribution_authorized: false
research_execution_authorized: false
novelty_verdict: "NOT_REQUESTED_AND_NOT_ISSUED"
---

# Stage-1C v2 Agentic RC2 博导级独立方法复审

## 一、审查对象与独立性声明

审查对象固定为 commit `74cf8e4b565a9e53ff40f9dbc34961ede853dd57` 中的 RC2 exact package，
其 manifest Git blob 为 `090a66455e9afa52c794ba7109f62381bca32802`，SHA-256 为
`9abdb94fd35b7eb8f1f9255b8616e7934b06e9fc0eae054b52fea2d4eae46e8f`。Manifest 声明
22 个 artifacts，提交时状态为 `AGENTIC_RC2_CODER_READY_NOT_DISTRIBUTED`。

本审查由无先前讨论上下文的独立 AI doctoral-supervisor advisory reviewer 完成。Reviewer：

- 只以 `git show <commit>:<path>` 定位 commit-bound 证据；
- 未修改被审 commit，未联网发现新论文；
- 未运行 coder、研究模型/API、benchmark、复现或 prototype；
- 不冒充人类签名、domain expert 或 calibration coder；
- 不产生 coder、mapping、研究执行、branch selection 或 novelty 权限。

## 二、定向核验结论

### 2.1 N=56 与 Duplex 排除基本闭合

- calibration、source、assignment 和 blind packet 均为 56 个唯一对象；
- 样本保持 38 overlays + 18 sentinels；
- FDB-v3 `arxiv:2604.04847` 已移除，Active Perception Agent `arxiv:2512.23646` 已加入；
- FDB-v2 `arxiv:2510.07838` 仅保留为 specialized-system exclusion boundary；
- active problem enum 不再包含 `INTERACTIVE_FULL_DUPLEX_OBJECTIVES`；
- FDB-v2、Audio MultiChallenge 和 Audio2Tool 均不能成为 method anchor。

因此 Duplex 范围和样本分母不是本轮阻断原因。

### 2.2 Coder/reviewer 分离与身份声明基本闭合

Coder-visible allowlist 只含 response schema、source manifest、label-hidden assignment、blind packet、
中性 coder codebook、中性 claim-template view 和 agreement contract。Calibration rationale、完整 prior
claim links、schema bundle、coder transaction 和 readiness 保留为 reviewer-only。两个 coder slot 未绑定，
计划使用隔离 Sol/Terra 上下文和同一 shared-content hash；合同不宣称 provider-independent 或 human
inter-rater independence。Owner adjudicator 仍未绑定，并要求完整 prior-exposure disclosure。

Exact coder-visible artifacts 中没有发现 selection rationale、prior label、origin/link 或 candidate
readiness 的直接注入。但 known-label value scanner 的覆盖范围仍窄于报告声明，列为 P1-2。

### 2.3 Schema 字段存在，但 agreement 与语义门没有完全实现合同

Response schema 已强类型化 paper labels、agentic scope、run cells、primary intervention、paired status、
dataset relation、claim merge/split、compatibility decision、source locator 和 absence reason。
`DIRECT_AGENTIC` 与 specialized-system exclusion 的 semantic guard 也存在。

阻断点不在“字段缺失”，而在 agreement intake、逐 critical-field gate 以及 BORROW/REPRODUCE 语义门
没有忠实实现这些声明。

### 2.4 Source bytes 为 exact local binding，但两个 ACL receipt 较弱

56 个 source records 均绑定 revision、字节数、PDF SHA-256、official URL 和可用 alternate rendition。
54 个 arXiv 项具有 fulltext-ledger locator；两个 ACL Anthology 项仅使用 `RC2_LOCAL_SOURCE_RECEIPT`，
没有同等级的 ledger path/line/fetch timestamp 或独立 receipt artifact。这不推翻 local-byte identity，
但不足以让 reviewer 仅凭 package 独立重放 official-publication provenance。

### 2.5 Reference / borrow / reproduce 概念清楚，anchor 状态 fail closed

合同正确区分 REFERENCE、BORROW_PROTOCOL 和 REPRODUCTION_CANDIDATE；所有 15 个 candidate 的
`method_anchor_eligible`、`reproduction_eligible` 和 `research_execution_performed` 都保持 false，primary/
fallback selection withheld，reproduction anchor 数为 0。问题是 completed-response validator 没有实施
BORROW/REPRODUCE 的承重前置条件。

## 三、P0 阻断项

### P0-1：Agreement engine 对 exact N=56 与逐 critical-field gate fail open

`compute_agreement()` 只要求 coder A/B 的 paper-ID 集合相等，没有要求：

- paper count 等于 56；
- IDs 等于 frozen calibration manifest 的 exact canonical set；
- 每条 response 已通过 schema 和 completed semantic validation；
- response status 为 `CODER_SUBMITTED` 且不含 `NOT_CODED`；
- transaction、packet 和 source binding 有效。

两名 coder 同时遗漏相同论文、提交相同子集或提交相同未完成 response，仍可能进入 agreement 计算。

同时，agreement contract 声明逐 critical-field `RAW_AGREEMENT_PER_CRITICAL_FIELD`，实现却把同一 object
array 的全部共同字段聚合成 `matched_field_raw_agreement`。这会让 primary intervention、access、paired
status、dataset relation、claim merge/split 或 compatibility 等承重字段的系统性分歧被其他非关键字段
的一致稀释。故 report 中 `response_agreement_isomorphic=true` 尚无充分实现证据。

最低修复要求：

1. intake 绑定 exact manifest ID、N=56 和 exact canonical-ID set；
2. agreement 前逐条运行 schema 和 completed semantic validation；
3. 每个 critical path 单独生成 denominator、agreement 和 gate；
4. overall pass 要求所有已校准 critical paths 分别通过；
5. 增加双方共同遗漏、共同 blank/NOT_CODED、primary-axis 全分歧但其他字段一致的负向测试。

### P0-2：BORROW_PROTOCOL / REPRODUCTION_CANDIDATE 未机器化 fail closed

`validate_completed_response()` 目前只对 direct agentic 和 specialized-system exclusion 实施语义约束。
它没有要求：

- BORROW_PROTOCOL 必须有 translation decision、source→target mapping 和 rejection observation；
- REPRODUCTION_CANDIDATE 必须结构化闭合 task、dataset revision、entrypoint、access、license 和 evaluator；
- supporting objects 必须通过 source locator 绑定当前 source bytes。

因此 coder 可选择 BORROW 或 REPRODUCE，同时把 supporting objects 留空并填写一般 absence reason，仍
通过 validation。Report 的 `reference_borrow_reproduce_distinction_operationalized=true` 超出实现证据。

最低修复要求：增加 schema conditional 或 semantic validator、结构化 reproduction evidence、locator
binding，以及缺 translation/rejection/license/entrypoint/evaluator 的负向测试。

## 四、P1 缺陷

### P1-1：两个 ACL source receipt 不具备同等级可重放 provenance

应在 distribution 前为两个 ACL 项增加 append-only acquisition receipt，绑定 official URL、retrieval
timestamp、publication revision、exact PDF SHA-256 和 receipt artifact path/hash。

### P1-2：Known-label scanner 实际覆盖窄于报告

Forbidden-key scanner 会递归检查全部 coder-visible artifacts，但 named-expectation scanner 只扫描
`coder_codebook` 和 `claim_template_coder_view`。应把全部非-source-content coder-visible metadata 纳入
value scan，并为 source title/正文保留明确、窄化的 identity/content exception。

### P1-3：Commit 内 transaction status 是提交前快照

Report 仍记录 `local_commit_created=false`、`independent_review_submitted=false` 和
`CREATE_LOCAL_COMMIT_WITHOUT_PUSH`。这是首次提交前的正确快照，但不能继续充当当前 transaction 状态。
当前事实应由本 append-only review transaction 和 HOT/CURRENT 层补充，不得倒写被审 commit。

## 五、审查限制

本审查没有重新读取 320-work union、外部 56 份 PDF 或既有 reviewer 意见，没有重算 external source
bytes，也没有运行全量测试、agreement、模型、benchmark 或 reproduction。因此 source 结论限于 commit
内 contract，而非对外部 PDF 内容的独立复核；同样不判断 novelty、问题优先级、branch 或 anchor。

## 六、Verdict

`WITHHOLD_WITH_BOUNDED_DEFECTS`

决定性原因是：

1. agreement engine 未绑定 exact N=56/completed-response intake；
2. object-level critical fields 没有逐字段 gate，承重分歧可以被聚合稀释；
3. BORROW_PROTOCOL 与 REPRODUCTION_CANDIDATE 的前置证据未被机器合同 fail closed。

这些缺陷位于 coder intake 后不可逆地产生 calibration result 的承重路径，不能降级为事后 adjudication。

## 七、后续权限边界

本 verdict 是 AI advisory，不产生执行授权。Coder distribution、coder/adjudicator 实际绑定、agreement、
320-work mapping、`SIGN_STAGE1C_V2_EXPERIMENT_MAPPING`、模型/API/benchmark/reproduction/prototype、anchor/
problem/family/branch selection、novelty verdict、push 和 publication 全部保持关闭。

若 owner 接受本审查，应另行授权一次 bounded RC2 method-contract repair。修复后应生成新的 exact
commit-bound manifest，并交由不兼任 coder 的独立 advisory reviewer 复审。
