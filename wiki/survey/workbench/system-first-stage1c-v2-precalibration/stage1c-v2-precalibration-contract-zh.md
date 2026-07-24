# Stage-1C v2：320-work 候选输入整合与 pre-calibration 合同

## 0. 当前裁决

本合同承接 `AUTHORIZE_STAGE1C_V2_CALIBRATION_PREPARATION`，但不承接或伪造任何 reviewer signature。
当前已有一个 **320-work signed calibration input**，但没有 320-work full-mapping authority。

两个 Stage-1B overlays 已分别取得：

- `SIGN_STAGE1B_CAPABILITY_DELTA_RELEASE`；
- `SIGN_STAGE1B_TARGETED_ANCHOR_SCAN_RELEASE`。

两者分别绑定各自 reviewed RC1 精确字节，确定性 release-merge manifest 形成唯一 320-work
calibration 输入身份，不需要第三个 Stage-1B 科学签名；但 full mapping 仍必须等待 calibration 通过后的
`SIGN_STAGE1C_V2_EXPERIMENT_MAPPING`。

## 1. 研究组织原则

Stage-1C 继续按实验与 claim 统合，不按论文、年份、数据集名称或 D0-D4 投票。

- problem node 回答“要解释或修复什么目标失败”；
- intervention axis 回答“通过什么系统/知识/技能/记忆/控制变量干预”；
- claim 回答“在什么 scope 内有哪些可证伪主张”；
- experiment family 只有在完成 run cell、outcome、access 和 comparison compatibility 编码后才形成。

三个旧 problem bundles 只保留为未排序 candidate problem nodes。新增三个 hypotheses 同样只是未排序
candidate nodes，不预注册为独立研究方向：

1. `ACTIVE_MULTIMODAL_EVIDENCE_ACQUISITION_UNDER_BUDGET`；
2. `SKILL_ACCESS_MAINTENANCE_AND_NEGATIVE_TRANSFER`；
3. `MEMORY_RETRIEVAL_TO_USE_AND_ACTION_GAP`。

D0-D4 始终是 intervention axes，不是五个自动成立的博士课题。

## 2. 输入身份

| 层 | 数量 | 当前状态 |
|---|---:|---|
| frozen Stage-1B v5 | 226 | 已冻结 |
| CURRENT 去重继承并集 | 282 | 已有当前证据层 |
| capability delta | 14 | reviewed RC1 已冻结并独立签署；仅进入 calibration |
| targeted-anchor overlay | 24 | reviewed RC1 已冻结并独立签署；仅进入 calibration |
| combined calibration input | 320 | 已签署；不是 full-mapping authority |

`release-merge-manifest-v1.json` 为 320 个 canonical IDs 逐条保存 source-layer membership。任何 overlay
manifest 字节变化都必须生成新 manifest，不能沿用旧 reviewer 建议。

## 3. Claim-level 去重

Paper identity 去重不能替代 claim 去重。本合同先为 38 个 overlay records 建立 13 个 synthesis claims，
覆盖多模态因果必要性、relevance/utility、主动证据获取、技能 access/lifecycle、memory retrieval-to-use、
memory update、TTS 非单调性、评价器分歧、交互目标拆分、access boundary、系统归因与 knowledge-to-skill。

Claim scope 至少包含：

`problem/outcome × task × dataset revision/split × model × access × input condition × intervention ×
budget/horizon × evaluator`

当前 claim 只用于去重和 calibration，不产生 family conclusion。跨域综合 claim 使用
`CROSS_PAPER_SYNTHESIS`，不会强迫某篇论文成为虚假的 owner paper。

## 4. 参考、借鉴、复现与 translation

- `REFERENCE_CONTEXT`：只支撑边界与背景；
- `BORROWED_PROTOCOL_ANALOGUE`：必须完成 translation contract 才能承重；
- `REPRODUCTION_ANCHOR`：必须闭合 data/code/model/evaluator/access/deviation，当前仍为 0。

远域 translation contract 必须记录借用的决策结构、source→speech/omni 的变化、可比变量、最强 transfer
failure 和拒绝迁移的 observation。在完成前统一为 `WITHHELD_PENDING_TRANSLATION`。

## 5. 旧八个 family 的降格

F0、FK1、FK2、FS1、FS2、FM1、FM2、FR1 全部改称
`CANDIDATE_PROTOCOL_TEMPLATE`。它们只提供变量、arm 和 falsifier 的候选设计：

- 不预注册 family membership；
- 不创建 branch；
- calibration/full mapping 后允许 merge、split 或完全无人路由；
- 不得用 template 迫使 experiment cell 进入预设方向。

## 6. 统一数据合同

`schema-bundle-v1.json` 物化以下对象：

1. `paper_audit`；
2. `run_cell`；
3. `observation`；
4. `paired_comparison`；
5. `dataset_node`；
6. `dataset_lineage_edge`；
7. `dataset_relation_edge`；
8. `claim_record`；
9. `family_record`；
10. `family_membership`；
11. `review_event`；
12. `translation_contract`。

一次 run cell 的身份必须冻结 dataset revision/split、model/access、input condition、intervention 和
budget/horizon。多个 metric 是同一 cell 的 observations。Lineage 必须有来源 locator；语义相似只能登记
relation。Family 仍以问题、outcome、environment/access 与 paired comparison compatibility 为门。

## 7. Exact calibration packet

Calibration 固定 N=56：

- 全部 38 个新 overlay records；
- 18 个 CURRENT/inherited sentinels，覆盖三个旧 problem nodes、direct/instrument/boundary、speech/omni、
  v2/v3 lineage、reproduction hard cases、MM3 与 evaluator disagreement。其中 H5 withheld sentinel
  `2505.17862` 明确位于 320 calibration input 之外，只用于检验 codebook 的 withheld 处理，不得借此扩充
  320 输入。

这是有目的的 codebook calibration，不是全量分布估计，也不是后续 20% blind review。

两名 coder 必须在看到彼此标签前独立编码。给 secondary coder 的 packet 不含既有 role、primary direction、
problem/family 标签；若 coder 已接触仓库标签，必须在 review event 中申报 exposure。

关键字段逐字段要求 pre-adjudication raw agreement ≥85%，并同时报告：

- nominal：Gwet AC1；
- ordinal：weighted Gwet AC2；
- multi-label：exact match、Jaccard、micro/macro F1。

未达门只允许一次 codebook consolidation，之后完整 56 条全部重编码。所有分歧必须裁决，尤其是
reproduction、lineage、MM3、paired status 与 core-member compatibility。

Calibration records 永久排除在后续 blind sample 外。320 已成为 signed calibration input；若后续取得
full-mapping authority，full mapping 至少盲审
64 个 unique works；抽样算法与 seed 已在 agreement contract 中预注册，但 exact sample 只在有效 mapping
signature 后生成。

## 8. Reproduction candidate closure

当前只建立只读检查顺序，不选择 primary/fallback：

1. Full-Duplex-Bench-v2；
2. Audio MultiChallenge；
3. MultiVox；
4. VCB Bench；
5. RealTalk-CN。

必须闭合 data/code/model/judge revision、license/terms、loader/minimal slice、evaluator independence、TF-Strict
access fit 和 Stage-2A deviation ledger。全部检查有证据后只选一主一备；未闭合者保持
`CANDIDATE_NOT_ANCHOR`。

Online reward、primary task outcome、secondary diagnostic 与 human audit 必须分开。同一个 judge 不得既决定
下一动作，又成为唯一最终 outcome。

## 9. 发现过程和持续更新

本轮搜索日志只能部分重建，因此它可以证明 26 exact IDs 的有界全文扫描，不能证明系统综述召回率或
literature-universe closure。不重跑大规模搜索。以后只在下列触发条件下做增量：

- 新论文改变方法路径；
- 推翻承重前提；
- 填补 task-matched direct/reproduction anchor。

任何新增仍回到 Stage-1B delta，不得直接插入 signed Stage-1C input。

## 10. 当前停止条件

本包准备完成后必须停止在 calibration gate：

- 两个 Stage-1B release signatures 已闭合；calibration coding 只能由两名独立 coder 执行；
- 两名 coder 和 adjudication 未完成时不得声称 calibration 通过；
- `SIGN_STAGE1C_V2_EXPERIMENT_MAPPING` 缺失时不得进行 320-paper full mapping；
- 全流程不得产生研究模型/API 调用、benchmark metric、reproduction、prototype、problem winner、owner
  selection 或 novelty verdict。
