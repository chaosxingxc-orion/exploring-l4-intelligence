---
title: "Stage-1C v2 Agentic 校准 R1：Owner 分歧裁决与 codebook consolidation 决策包"
date: "2026-07-25"
artifact_type: "PRE_ADJUDICATION_OWNER_PACKAGE"
status: "AGREEMENT_FAILED_OWNER_CONSOLIDATION_DECISION_REQUIRED"
adjudication_applied: false
---

# Stage-1C v2 Agentic 校准 R1：Owner 决策包

## 1. 结论先行

N=56 两份独立模型编码已经完成、通过 exact-intake 与语义校验，并在计算一致性之前冻结原始
bytes。首轮 pre-adjudication agreement 的结果是 **FAIL**，不能签出 calibration release，也不能
进入 320-work mapping。

失败由两类问题共同造成：

1. 论文级判定规范仍不够确定。13 个论文级 critical paths 中只有 5 个通过 0.85，8 个失败；
2. 对象身份规范存在结构性缺陷。两名 coder 为同一论文构造了不同形式的
   `object_match_key`，九类对象均为 0 个共同键，导致对象 segmentation 失败、对象字段全部无法
   校准。`dataset_edges` 与 `reproduction_evidence` 还同时是双方零正例。

这不是可由 owner 逐项挑一个标签后“修复”的一致率问题。Owner 裁决可以形成最终证据记录，但
不能回写 raw agreement，也不能把 `NOT_CALIBRATED` 伪装为通过。当前推荐动作是授权唯一一次
codebook consolidation，并用两个**新的**隔离上下文全量重编 N=56。

## 2. 输入、隔离与冻结证据

方法合同是 commit `ee12a3a79bd578df996c44c4bdb2dbc709e2f616`，独立方法复审结论是
`ACCEPT_AGENTIC_RC2R3_METHOD_CONTRACT_FOR_CODER_INTAKE`。两名 coder 收到相同的八件内容包：

- bundle SHA-256：`03674710223ad3c457e6568bdc83b66c1491abd84dd4e6d2c16495065e3ead64`；
- prompt SHA-256：`88fca5a601bc49b946e2c29fcac35ba212dec38af5625c312a964535201aaa8e`；
- 135 份 source renditions 均按 manifest 复核 byte length 与 SHA-256；
- A/B 使用不同 coder、transaction、process/task 和无 `.git` 隔离目录；
- 两者是 isolated model coders，不声称 provider-independent 或 human inter-rater independence。

冻结结果如下：

| Slot | 模型 | 原始响应 | Bytes | SHA-256 |
|---|---|---:|---:|---|
| A | `gpt-5.6-sol` | 56 | 354559 | `154c091a4727f2461a70dda4b1b3179bb004a14cee6ab1a04c3859dc495389b5` |
| B | `gpt-5.6-terra` | 56 | 716610 | `ff922386cdf89617604209d30e63834151efb94941404b85a32a0da420f1e0c2` |

冻结顺序是：两份输出各自完整校验 → 两份 raw bytes 同时冻结 → 计算 agreement。Agreement 的
SHA-256 是 `9e3f0a6afc969236c68590c0bf5372d7ecaea5f62adae8bc8acfdaf7cdf45d92`，完整分歧包
SHA-256 是 `6de80624d94bfe93d0e58988c3bdb9a9ed97183c8e25fd6ef5640b1d58a45bc2`。

Fail-closed intake 发生过两类合规修正，均在冻结前、各自原隔离上下文内完成：

- A 的首份实质性输出有 9 项 specialized-scope invariant 冲突，校验拒绝后只修正这些冲突；
- B 的 BOM 文件先因非 UTF-8 exact JSON 被拒绝，随后一份 56/56 空 locator/空实证对象的占位式
  输出又被语义校验拒绝，最终重新基于冻结 source bytes 完成实质编码。

这两类过程已写入各自 submission metadata。A/B 在提交前后都没有读取另一 coder 输出。

## 3. 论文级一致性

固定门槛为 0.85，调用方不能覆盖。多标签字段以 exact-set agreement 为 gate，Jaccard 仅为诊断。

| Critical path | 一致数/分母 | Exact agreement | 状态 |
|---|---:|---:|---|
| `paper_disposition` | 49/56 | 0.8750 | PASS |
| `paper_role` | 35/56 | 0.6250 | FAIL |
| `mm_level` | 49/56 | 0.8750 | PASS |
| `reference_borrow_reproduce` | 38/56 | 0.6786 | FAIL |
| `access_regime` | 33/56 | 0.5893 | FAIL |
| `empirical_experiment_present` | 55/56 | 0.9821 | PASS |
| `agentic_scope.scope_status` | 37/56 | 0.6607 | FAIL |
| `agentic_scope.core_dependency` | 28/56 | 0.5000 | FAIL |
| `agentic_scope.control_role` | 50/56 | 0.8929 | PASS |
| `problem_nodes` | 37/56 | 0.6607 | FAIL |
| `intervention_axes` | 18/56 | 0.3214 | FAIL |
| `agentic_scope.loop_components` | 20/56 | 0.3571 | FAIL |
| `agentic_scope.capability_assets` | 47/56 | 0.8393 | FAIL |

总计保存了 232 个逐论文/逐字段分歧。最严重的不是边界附近的 K/S/M 资产字段，而是
`intervention_axes`、loop、core dependency、access 和 paper role：这些字段直接决定哪些工作能
抽取 experiment cell、如何归因 primary intervention，以及能否进入 agentic family。

## 4. 对象级一致性

| 对象类型 | A | B | 共同键 | 结果 |
|---|---:|---:|---:|---|
| `run_cells` | 59 | 56 | 0 | segmentation FAIL；11 fields NOT_CALIBRATED |
| `observations` | 59 | 56 | 0 | segmentation FAIL；6 fields NOT_CALIBRATED |
| `paired_comparisons` | 4 | 0 | 0 | segmentation FAIL；10 fields NOT_CALIBRATED |
| `dataset_nodes` | 55 | 56 | 0 | segmentation FAIL；4 fields NOT_CALIBRATED |
| `dataset_edges` | 0 | 0 | 0 | segmentation/6 fields NOT_CALIBRATED |
| `claim_decisions` | 56 | 56 | 0 | segmentation FAIL；13 fields NOT_CALIBRATED |
| `translation_or_compatibility_decisions` | 18 | 0 | 0 | segmentation FAIL；5 fields NOT_CALIBRATED |
| `protocol_transfer_evidence` | 18 | 0 | 0 | segmentation FAIL；8 fields NOT_CALIBRATED |
| `reproduction_evidence` | 0 | 0 | 0 | segmentation/14 fields NOT_CALIBRATED |

典型例子是同一篇 `2026.acl-long.1615`：A 使用
`run:2026.acl-long.1615:main`，B 使用 `run:acl:2026.acl-long.1615`。两者可能指向同一抽取对象，
但 agreement engine 只能看到不同键，因此不能比较任何内部字段。这个缺陷属于 codebook 的对象
身份合同，不应归咎于某一个 coder，也不能通过模糊匹配补救，否则会把 adjudication 偷渡到
pre-adjudication agreement 中。

另外，A 抽取了 18 份 transfer/compatibility evidence，B 为 0；A 仅抽取 4 个 paired comparisons，
B 为 0。这里既有匹配键问题，也有“何时必须建对象”的触发规则分歧。

## 5. 对 Stage-1C 承重结论的影响

当前失败会直接污染四个后续层级：

1. **320/320 paper audit**：`scope_status`、dependency 与 empirical gate 不稳定，会造成 cell
   eligibility 漂移；
2. **experiment cells**：primary intervention、run identity、observation 与 paired comparison 不可
   稳定复现；
3. **experiment families**：problem/outcome/access 与 baseline→intervention 比较可能错误合并；
4. **K/S/M × control 与 branches**：能力资产接近但未过门，reproduction evidence 又完全未校准，
   无法可靠判断 nearest-prior anchor 与五项 branch gate。

因此现在直接启动 320-work mapping 只会把 56 篇的编码分歧放大到全量数据，并在 family synthesis
阶段产生不可审计的人工修补。

## 6. 建议的唯一一次 codebook consolidation

建议修订必须有界，只修正首轮已经证明的歧义，不新增研究假设或宽泛文献发现：

### 6.1 冻结对象身份

- 所有对象键由 packet/compiler 预生成或按唯一公式生成，不允许 coder 自由命名；
- 推荐形式：`<object-type>:<完整 canonical paper ID>:<source-order zero-padded ordinal>`；
- canonical ID 不得丢弃 `acl:`/`arxiv:` 等命名空间，不得嵌入 coder/transaction；
- 跨对象引用使用同一套预生成 ID；对象是否存在和对象内部字段分开编码；
- agreement 只按 exact key 比较，继续禁止事后 fuzzy matching。

### 6.2 冻结对象触发与最小抽取量

- `empirical_experiment_present=YES` 时，必须抽取所有可定位的 material run cells、observations、
  dataset nodes；不能默认“一篇一个”；
- baseline 与 intervention 可解释且 comparability key 可闭合时必须建立 paired comparison；否则记录
  不成对理由，而不是静默省略；
- `BORROW_PROTOCOL` 必须同时建立 translation decision 与 protocol-transfer evidence；
- `REPRODUCTION_CANDIDATE` 应建立 reproduction evidence，即便 closure 是 `BLOCKED`，并完整列出
  blockers；只有字段全部闭合才能升级 anchor；
- source locator 至少绑定支撑该对象身份与承重字段的页/段/表，禁止只用标题页摘要替代实验 locator。

### 6.3 冻结论文级决策表

- `paper_role`：方法主张、evaluation/instrument、negative/falsifier、boundary/reference 的优先顺序；
- `REFERENCE` / `BORROW_PROTOCOL` / `REPRODUCTION_CANDIDATE`：分别以是否迁移协议、是否闭合任务与
  资产合同判定；
- `access_regime` 与 `core_dependency`：明确 external orchestration、generic frozen core、trained
  controller、specialized model 的互斥边界；
- `scope_status`：只有同时含 `decide + act/tool` 且不依赖 specialized Duplex core/trained controller
  才能进入 direct agentic；
- `intervention_axes`、loop 与 K/S/M：给出 inclusion/exclusion 表，并强制唯一
  `primary_intervention_axis`，其余为 secondary assets。

### 6.4 处理零正例 gate

`dataset_edges` 与 `reproduction_evidence` 双方都为 0，当前不能校准。Consolidation 应先明确：

- lineage/relation 只有论文存在来源证据时建 edge，不能为了校准伪造；
- reproduction candidate 即使未闭合也要建立 typed evidence，anchor 才要求全闭合；
- 若按新触发规则全量重编后仍无正例，第二轮必须继续标记 `NOT_CALIBRATED` 并停止，不可降门槛；
- 若 owner 希望在重编前保证正例覆盖，需要另行授权有界 positive-sentinel sample repair 和新的方法
  复审；当前授权不包含替换 N=56。

### 6.5 R1 reviewer-only positive-support preflight

在不修改 R1、N=56 或 coder packet 的前提下，新增的可重放检查得到三个确定结果：

1. `dataset_edges` 并非真的没有正例。TRACE 第 3 页明确使用 S2S-Arena 的 English subset，并对
   既有 SpeakBench/S2S-Arena 数据重新标注，分别支持 `SUBSET_OF` 与 `REANNOTATED_FROM`；A/B 均
   抽取为 0，证明对象触发规则漏检；
2. 当前 `reproduction_evidence` 要求 blind coder 填 `local_asset_state`，但 packet 同时明确禁止
   repository access；字段在观测上不可获得；
3. schema 又强制 `closure_status=CLOSED` 且 `blockers` 为空，因此“候选但尚有 blocker”无法表达，
   使该 mandatory class 的正例覆盖结构性为零。

因此不建议为了过门而替换 sentinel。更严格的修复是拆分：paper-visible
`REPRODUCTION_CANDIDATE` 可以是 `OPEN_WITH_BLOCKERS`；reviewer-only local readiness 全闭合且经
100% 复核后，才能晋升 `REPRODUCTION_ANCHOR`。R2 exact schema 冻结后必须重新运行 positive-support
preflight；只有届时仍无 paper-visible 正例，才请求独立的 source/sentinel repair。

## 7. Owner 需要决定什么

推荐授权：

`AUTHORIZE_STAGE1C_V2_AGENTIC_CALIBRATION_R1_CODEBOOK_CONSOLIDATION`

该授权仅允许：把上述有界规则、candidate/anchor 可观测性拆分和 positive-support preflight 编译进
codebook/schema/packet，先写失败测试，重新通过独立方法复审，
然后由两个新的无 fork 隔离上下文全量重编同一 N=56。它不授权：

- 对 R1 raw 输出或 agreement 做回写；
- owner 裁决后把原始一致率改成 PASS；
- 替换 sentinel、宽泛新增调研或 Stage-1B 回退；
- 320-work mapping、研究模型、benchmark、复现、prototype、novelty verdict、Stage-2A 或 push。

如果 owner 不授权 consolidation，本轮应以 `CALIBRATION_R1_FAILED_STOP` 关闭并返回独立方法复审。
如果 owner 认为 N=56 必须先补正例，应明确另行授权 bounded positive-sentinel repair；不能把它隐含在
codebook 修订中。

## 8. Exact artifacts

- `frozen-r1/coder-a-responses.json`：A 原始冻结输出；
- `frozen-r1/coder-b-responses.json`：B 原始冻结输出；
- `frozen-r1/pre-adjudication-agreement.json`：99 条 critical-path gate；
- `frozen-r1/disagreement-package.json`：232 条论文字段分歧、全部对象键和双方对象原文；
- `frozen-r1/freeze-manifest.json`：freeze-before-agreement 证据；
- `pre-adjudication-run-manifest.json`：当前 fail-closed 状态。

当前事实：literature-coding model calls 已发生且结束；research model、benchmark metric、paper
reproduction、prototype、novelty verdict、320-work mapping、owner adjudication 和 push 均为零。
