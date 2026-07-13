---
title: "Response v6 · 对签署审查（V42-REMEDIATION-SIGNOFF-ADR-2026-07-13）的逐项回复"
date: 2026-07-13
responds_to: "2026-07-13-v42-remediation-signoff-doctoral-adversarial-review.md"
reviewed_snapshot_responded_to: "umbrella c7528fe / report sha256 cd987ff0…"
this_response_snapshot: "umbrella 7b895b5 / W1 a532da0"
verification_mode: "协调者本人逐条核验（owner 指令：不委托）；零驳回"
owner_rulings: "Decision-Log 续32（四项：全盘接受 / A-SEL 唯一 headline / 修订续29 / public-deterministic 等级帽）"
stance: "全部 13 项 ACCEPT；无一项 REJECT_WITH_EVIDENCE；退回裁决接受，不申请立即重签"
---

# Response v6 · 逐项回复（按审查 §12 强制格式）

## 0. 总立场

退回裁决**接受**。我方对审查全部可核事实指控逐条独立核验（本人执行，非委托）：**零驳回**。
另主动补充一条审查未点名的加重事实并已登记：`c7528fe` 提交信息声称 "conformance JSON
regenerated / evidence snapshot refreshed"，但该提交实际只改动整改报告一个文件
（`git show --stat c7528fe` 可复核）——已入 `discrepancy_register.md` P0-A 追加节第 3 条。

本回复**不申请立即重签**。P0-A（发布事务与标签）已完成并可复核；P0-B（M2 前置门）逐项列出
负责事件与门位。按审查 §10 重提条件，重签申请将在 P0-B 全部闭合后提出。

P0-A 完成证据（第三方一条命令可复核）：

```text
umbrella HEAD 7b895b5（manifest wrapper commit，仅含 manifest）
  ← 13b5a10（gitignore 卫生：settings.local.json 系 dirty=true 唯一来源）
  ← c16900c（P0-A 主提交：报告修订+登记册追加+checker 重跑+续32）
W1 HEAD a532da0（E-08 路径修复）
release_manifest.json：umbrella 13b5a10 dirty=false / W1 a532da0 dirty=false，
  live pytest 159 passed，live checker 22/22；
  记录 SHA 均为最终 HEAD 祖先（git merge-base --is-ancestor 退出码 0×2）；
  key_artifact_hashes 7/7 与当前文件逐字节一致（零漂移）。
v42-conformance-output.json：meta.inputs 记录 proposal sha256
  3f0ac5b6e5c5e021ffc9b8… ——与报告附录、盘上文件三处一致。
```

（注：上行哈希全文为 `3f0ac5b6e5c5e021ffc9b85c10f7b8b9f07a4bd6395de6350bcd8c87e1ba18e0`。）

## 1. FUNDAMENTAL 项

```yaml
response_item:
  finding_id: F-S1   # 阶段门序倒置
  accept_reject_partial: ACCEPT
  exact_fact_disputed: null
  evidence:
    frozen_commit: c16900c (umbrella)
    files: [wiki/Decision-Log.md#续32, docs/integrity/discrepancy_register.md]
    commands: ["git show c16900c:wiki/Decision-Log.md | grep -A6 '续32'"]
    expected_outputs: ["设计身份类待决项（F-1/F-3/F-4/F-5/F-9/M-1/M-2/M-3）门位由 M3 改 BEFORE_STAGE2_UNFREEZE"]
  status_before: WRONG_GATE
  status_after: OPEN   # 门已改正；Stage-1 Identity Closure 文档与 fresh Stage-2 proposal 为 P0-B 交付物
  gate_before_any_data_action: BEFORE_STAGE2_UNFREEZE（fresh Stage-2 proposal 冻结；owner 已选唯一
    headline = A-SEL：reward-guided selector 兑现 ρ/oracle headroom，equal-K、跨 generation seeds、
    跨集复现；RDU-vs-strongest 降为 secondary/ablation。续29 的"不出 fresh proposal"部分废止，
    append-only 记录于续32）
  scientific_claim_enabled: none
  integrity_implication: record_corrected

response_item:
  finding_id: F-S2   # release manifest 最终事务未执行
  accept_reject_partial: ACCEPT
  exact_fact_disputed: null
  evidence:
    frozen_commit: 7b895b5 (umbrella, manifest-only wrapper commit)
    files: [docs/integrity/release_manifest.json]
    commands:
      - "git -C <umbrella> merge-base --is-ancestor 13b5a10 HEAD && echo ancestor-ok"
      - "git -C <W1> merge-base --is-ancestor a532da0 HEAD && echo ancestor-ok"
      - "对 manifest key_artifact_hashes 逐项 sha256 复算比对当前文件"
    expected_outputs: ["dirty=false×2；159 passed；22/22；7/7 哈希零漂移"]
  status_before: OPEN
  status_after: CLOSED   # 事务按 finalize→commit→clean→rerun→manifest→wrapper-commit→verify 顺序重执行；该顺序立为发布门（违反即 FAIL）
  gate_before_any_data_action: before_any_signoff_or_release（永久性发布门）
  scientific_claim_enabled: none
  integrity_implication: record_corrected

response_item:
  finding_id: F-S3   # checker JSON 输入非最终 proposal
  accept_reject_partial: ACCEPT
  exact_fact_disputed: null
  evidence:
    frozen_commit: c16900c (umbrella)
    files: [docs/checks/v42-conformance-output.json, docs/checks/v42-conformance-report.md]
    commands: ["python - <<'EOF' … json.load→meta.inputs proposal sha256 EOF", "sha256sum wiki/2026-07-12-research-proposal-v42-external-review.md"]
    expected_outputs: ["两处均为 3f0ac5b6…；叙事版顶部标注'正式移出发布证据集'"]
  status_before: OPEN
  status_after: CLOSED   # 重跑并提交；"可复跑通过"与"已提交最终运行证据"今后分开表述；叙事版 12/12 移出证据集（未选"下一发布周期"）
  gate_before_any_data_action: before_any_signoff_or_release
  scientific_claim_enabled: none
  integrity_implication: record_corrected

response_item:
  finding_id: F-S4   # 语料自锁被解释为上游官方性
  accept_reject_partial: ACCEPT   # 附一条 scope 说明，不构成异议：corpus_mode='full'+自锁确实排除"团队建库时按查询过滤（相对首见快照）"这一主要污染通道；接受的点是它不能证明上游官方性，而 proposal §6.4 自己承诺的正是上游锚标准
  exact_fact_disputed: null
  evidence:
    frozen_commit: c16900c (umbrella) + a532da0 (W1)
    files: [wiki/2026-07-13-remediation-report-v42-for-reviewer-signoff.md#F-6, projects/…/scripts/knowledge/corpus_lock.py]
    commands: ["grep -n 'SELF-PIN VERIFIED / UPSTREAM ANCHOR OPEN' wiki/2026-07-13-remediation-report-*.md"]
    expected_outputs: ["F-6 标签改判；hf_revision_sha 本地元数据来源、EXPECTED_DOC_COUNT 自家 docstring 来源均已在报告中如实点名"]
  status_before: PARTIAL（标签超陈述）
  status_after: PARTIAL   # 标签/记录已改正；实质闭合挂 P0-B
  gate_before_any_data_action: P0-B——第二人从 pinned revision clean fetch 逐字节比对 + revision/LFS-OID
    复核；`query_independent_corpus` 轴代码语义收紧为 SELF_PIN_MATCH/UPSTREAM_NOT_VERIFIED（锚未闭合时
    绝不 PASS）；均在任何 eligibility/build 该轴 PASS 之前
  scientific_claim_enabled: none
  integrity_implication: record_corrected

response_item:
  finding_id: F-S5   # 跨 split group-disjoint 未实现
  accept_reject_partial: ACCEPT
  exact_fact_disputed: null
  evidence:
    frozen_commit: c16900c (umbrella；契约与门位记录)
    files: [wiki/2026-07-13-remediation-report-v42-for-reviewer-signoff.md#F-8, docs/integrity/discrepancy_register.md]
    commands: ["grep -n 'not in excluded' projects/…/scripts/baselines/deterministic_draw.py"]
    expected_outputs: ["我方复核确认：excluded 集只装 item id；测试仅断言 item 交集为零且 prior 用 identity grouping"]
  status_before: WRONG_GATE（原挂 P2/M2）
  status_after: OPEN
  gate_before_any_data_action: 任何真实 split draw 之前（P0-B）。修复契约已冻结并入报告：prior manifest
    持久化所用 group manifest（或 hash+路径）；confirmatory 先取 prior groups 并集、再整组排除当前 pool
    中属这些 groups 的 items；负例测试 = A/B 同 speaker、不同 ID、跨 manifest，预期硬失败或 B 整组被排
  scientific_claim_enabled: none
  integrity_implication: record_corrected

response_item:
  finding_id: F-S6   # 独立审计再定义
  accept_reject_partial: ACCEPT
  exact_fact_disputed: null
  evidence:
    frozen_commit: c16900c (umbrella)
    files: [wiki/2026-07-13-remediation-report-v42-for-reviewer-signoff.md#§6.3, wiki/Decision-Log.md#续32]
    commands: ["grep -n '本条商榷于 P0-A 撤回' wiki/2026-07-13-remediation-report-*.md"]
    expected_outputs: ["§6.3 撤回；'送达即满足独立快照流程步'推论删除；两类记录并存不混称"]
  status_before: OPEN
  status_after: CLOSED-as-record   # 记录已更正；实质独立审计（IA-1..IA-8）为独立工作流，未以本回复冒充
  gate_before_any_data_action: 独立只读审计完成前，P0 独立性条件保持 OPEN；等级主张按 M-S1 路线自我设限
  scientific_claim_enabled: none
  integrity_implication: record_corrected

response_item:
  finding_id: F-S7   # P0 NOT_PASS 与"高质量锁定"不能并存
  accept_reject_partial: ACCEPT
  exact_fact_disputed: null
  evidence:
    frozen_commit: c16900c (umbrella)
    files: [docs/integrity/prior_exposure_registry.json#p0_gate_status, wiki/Decision-Log.md#续32]
    commands: ["python -c \"import json;print(json.load(open('docs/integrity/prior_exposure_registry.json'))['p0_gate_status']['pass_conditions_met'])\""]
    expected_outputs: ["false；续32 明记'M2 维持冻结直至 P0-B 闭合'"]
  status_before: OPEN
  status_after: OPEN   # 如实保持；配置轨迹重建（不可回溯处冻结列 UNKNOWN）为 P0-B 交付物
  gate_before_any_data_action: before_any_data_sensitive_continuation——P0 NOT_PASS 期间不解冻任何
    会新增选择性信息的 M2 搜索；"全部修完/高质量锁定"类语言停用（escalation trigger 已知悉）
  scientific_claim_enabled: none
  integrity_implication: record_corrected
```

## 2. MAJOR 项

```yaml
response_item:
  finding_id: M-S1   # 证据等级由信息流决定
  accept_reject_partial: ACCEPT
  exact_fact_disputed: null
  evidence: {frozen_commit: c16900c, files: [wiki/Decision-Log.md#续32], commands: [], expected_outputs: []}
  status_before: OPEN
  status_after: CLOSED   # owner 已二选一：public-deterministic 路线 + 如实等级帽（development/controlled benchmark evidence，不作强 confirmatory 宣称；title/abstract 如实定位）
  gate_before_any_data_action: 已在 fresh Stage-2 proposal 之前落定（续32④）
  scientific_claim_enabled: none
  integrity_implication: none

response_item:
  finding_id: M-S2   # SESOI 外部锚档案未交付
  accept_reject_partial: ACCEPT
  exact_fact_disputed: null
  evidence: {frozen_commit: c16900c, files: [docs/integrity/discrepancy_register.md], commands: [], expected_outputs: []}
  status_before: PARTIAL（诚实命名已修，实质依据未交付）
  status_after: OPEN
  gate_before_any_data_action: BEFORE_STAGE2_UNFREEZE——external-anchor dossier（效用推导/外部效应分布/
    专家 elicitation 记录/量纲换算，Lakens et al. 2018 谱系）随 fresh proposal 冻结
  scientific_claim_enabled: none
  integrity_implication: none

response_item:
  finding_id: M-S3   # 主 estimand 与固定绝对 margin 不同问题
  accept_reject_partial: ACCEPT
  exact_fact_disputed: null
  evidence: {frozen_commit: c16900c, files: [wiki/Decision-Log.md#续32], commands: [], expected_outputs: []}
  status_before: OPEN
  status_after: OPEN
  gate_before_any_data_action: BEFORE_STAGE2_UNFREEZE——headline=A-SEL 后，primary estimand 取审查 B2 的
    selector_equal_k_gain / realization_ratio 族（联合重采样、denominator floor 预注册）；RDU 的
    theta_rel（分子分母逐 replicate 联合重算）为 secondary；固定绝对 margin 仅作补充可解释性分析
  scientific_claim_enabled: none
  integrity_implication: none

response_item:
  finding_id: M-S4   # 生成随机性与 comparator 原则须先冻
  accept_reject_partial: ACCEPT
  exact_fact_disputed: null
  evidence: {frozen_commit: c16900c, files: [wiki/Decision-Log.md#续32], commands: [], expected_outputs: []}
  status_before: WRONG_GATE（原 M2→M3）
  status_after: OPEN
  gate_before_any_data_action: BEFORE_STAGE2_UNFREEZE——原则（≥3–5 独立 K 池/组或 power-justified、
    外层 group/内层 generation replicate、pool-mean 与 MBR/pessimistic comparator、预算上限 N*）随
    fresh proposal 冻结；M2 仅可在独立 calibration split 上按预列 branch rule 标定
  scientific_claim_enabled: none
  integrity_implication: none

response_item:
  finding_id: M-S5   # δ_corr 需独立模型对照
  accept_reject_partial: ACCEPT
  exact_fact_disputed: null
  evidence: {frozen_commit: c16900c, files: [wiki/Decision-Log.md#续32], commands: [], expected_outputs: []}
  status_before: PLAUSIBLE_STAGE_INCOMPLETE_CONTRACT
  status_after: OPEN
  gate_before_any_data_action: BEFORE_STAGE2_UNFREEZE——对照族冻结为四臂（same-model/same-prompt/diff-sample、
    same-model/diff-prompt、diff-family frozen verifier、non-model deterministic verifier）；阈值与
    删除规则看结果前冻结（Tan 2025 / Kim 2025 依据接受）
  scientific_claim_enabled: none
  integrity_implication: none

response_item:
  finding_id: M-S6   # 小簇模拟缺可执行契约
  accept_reject_partial: ACCEPT
  exact_fact_disputed: null
  evidence: {frozen_commit: c16900c, files: [wiki/Decision-Log.md#续32], commands: [], expected_outputs: []}
  status_before: PLAUSIBLE_STAGE_INCOMPLETE_CONTRACT
  status_after: OPEN
  gate_before_any_data_action: BEFORE_STAGE2_UNFREEZE——模拟契约（DGP 网格、cluster-size 分布、ICC、缺失
    机制、离散 endpoint、模拟次数、Type-I 上限、coverage/power tradeoff、选择规则、独立 simulation seed）
    预注册后 M2 才可跑模拟（MacKinnon & Webb 2018 warning 接受：wild bootstrap 不自动安全）
  scientific_claim_enabled: none
  integrity_implication: none
```

## 3. 不再采用的回复方式（对照审查 §12 负面清单的自我声明）

- 本回复无一处以 owner 裁决替代方法学证据（owner 裁决只出现在"选路线/选身份"这类本就属 owner 的决定）；
- 无一处以 checker PASS 回答科学有效性；
- 无一处以"报告已披露"回答错误挂门（挂门错误全部改判并给出新门）；
- `FIXED*` 记法已废止（拆 mechanism_fixed / scientific_gate_open）；
- 已提交证据不一致处（F-S2/F-S3）以**已完成的事务**回答，非未来时承诺；
- 本回复及其送达**不被声称**为独立审计的完成。

## 4. 重签申请条件对账（审查 §10）

| 硬条件 | 状态 |
|---|---|
| final_release_manifest_matches_clean_designated_HEADs | ✅ 7b895b5（dirty=false×2、祖先√、7/7 哈希√） |
| stored_checker_output_hash_matches_final_proposal_hash | ✅ 3f0ac5b6… 三处一致 |
| discrepancy_register_has_append_only_resolutions | ✅ P0-A 追加节 4 条 |
| corpus_axis_does_not_call_self_pin_upstream_verified | 🔶 记录层已改；代码轴语义收紧挂 P0-B |
| group_disjointness_is_proven_across_splits_not_only_item_ids | ⬜ P0-B（任何真实 split draw 之前） |
| P0_config_history_is_complete_or_unknowns_are_frozen_and_scoped | ⬜ P0-B |
| independent_audit_is_not_redefined_as_internal_checker_plus_signature | ✅ §6.3 撤回、推论删除 |
| stage1_owner_selects_one_scientific_identity | ✅ A-SEL（续32②）；Identity Closure 文档 P0-B 落笔 |
| fresh_stage2_proposal_exists_before_stage2_data_sensitive_work | ⬜ P0-B（续29 已修订授权） |
| all_findings_use_CLOSED_PARTIAL_OPEN_WRONG_GATE_without_FIXED_star_ambiguity | ✅ 本回复全程 |

全部 ⬜/🔶 闭合后再提重签；在此之前 M2 维持冻结。
