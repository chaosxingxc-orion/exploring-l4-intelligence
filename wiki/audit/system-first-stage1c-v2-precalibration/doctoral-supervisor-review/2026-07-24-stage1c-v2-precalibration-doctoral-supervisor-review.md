---
title: "Stage-1C v2 pre-calibration doctoral-supervisor review"
date: "2026-07-24"
artifact_type: "REVIEWER_FACING_DOCTORAL_SUPERVISOR_ASSESSMENT"
campaign: "system-first-stage1c-v2-precalibration"
round: "doctoral-supervisor-review"
review_target: "SF-STAGE1C-V2-PRECALIBRATION-REVIEW-PACKAGE-RC1"
review_package_manifest_sha256: "ae73a8adc02bc07926c3bcee98172cd2426b7720e6549c1d94d41fd6a2b178bd"
review_package_commit: "4eecb37440ecdf096b8a5e66fbeb7b698f54b633"
recommended_verdict: "WITHHOLD_CALIBRATION_EXECUTION_PENDING_BOUNDED_RC2_REPAIR"
team_execution_recommendation: "CONTINUE_IMMEDIATE_BOUNDED_METHOD_REPAIR_AND_READ_ONLY_CLOSURE"
stage1c_full_mapping_recommendation: "WITHHOLD_SIGN_STAGE1C_V2_EXPERIMENT_MAPPING"
research_execution_authorized: false
signature_provenance_clarification_required: true
authority_effect: "NONE_REVIEWER_FACING_ADVICE"
human_signature_claimed: false
novelty_verdict: "NOT_REQUESTED_AND_NOT_ISSUED"
---

# Stage-1C v2 pre-calibration 调研计划博导级审查

## 一、导师裁决

本次审查的对象已经不再是“是否还缺一批论文”，而是：团队能否用当前 320-work input 和 56-work packet，
可靠地校准后续 Stage-1C 实验映射方法。

结论如下。

### 1. 是否同意研究团队继续

**同意继续，而且建议快速继续。** 团队已经完成了上一轮最重要的结构性修复：

- 两个 Stage-1B overlay 已分别绑定精确 RC1 字节并登记 release token；
- 226/282/14/24/320 的输入层级没有再混写；
- 三个旧问题包和三个新增假设均保持未排序 candidate nodes；
- D0-D4 被固定为 intervention axes，不再静默替代 problem nodes；
- 38 个 overlay records 已尝试收敛为 13 个 synthesis claims，避免一篇论文生成一个重复种子；
- 八个旧 family 已降格为可 merge/split/unrouted protocol templates；
- 23 个远域 analogue 在 translation 完成前统一 withheld；
- 五个 speech/omni reproduction candidates 仍诚实地保持 non-anchor；
- 56-work calibration packet 与以后至少 64-work blind sample 被明确分开。

这些进展说明团队可以停止无边界扩充论文，转入方法校准与只读实验基座 closure。

### 2. 是否同意立即把 56-work packet 交给两名 coder 执行

**暂不同意。** 建议 verdict 为：

`WITHHOLD_CALIBRATION_EXECUTION_PENDING_BOUNDED_RC2_REPAIR`

这不是要求再开展一轮大型方法工程，也不是否定当前 RC。阻断项集中在四个可在一次小修中关闭的合同缺口：

1. coder response 没有覆盖 agreement contract 声称要校准的字段；
2. coder packet 没有绑定 56 篇全文的精确版本与哈希；
3. 13 个“canonical claims”目前是跨异质 strata 的主题性 synthesis headings，不是 scope-compatible claims；
4. coder 独立性、暴露、agreement 计算和失败后的停止规则仍未形成可执行 transaction。

在这些问题修复前启动双编码，会得到一份看似精确的 agreement report，却不能支撑后续 320-paper experiment
mapping。越早修复，返工越少。

### 3. 是否同意进入 320-paper full mapping 或研究实验

**不同意。** `SIGN_STAGE1C_V2_EXPERIMENT_MAPPING` 仍应保持关闭。模型/API、benchmark metric、论文复现、
prototype、问题排名、方向选择和 novelty verdict 同样保持未授权。

### 4. 对“新识别的问题基本完成”的判断

在当前声明的有界文献面上，**足以停止 broad discovery，开始方法校准准备**。但不能声称 literature universe
closed。以后的检索只在三类触发条件出现时进行：改变方法路径、推翻承重前提或填补 task-matched direct/
reproduction anchor。

## 二、审查对象与独立核验

### 2.1 精确对象

本文件绑定：

- review package：`SF-STAGE1C-V2-PRECALIBRATION-REVIEW-PACKAGE-RC1`；
- manifest SHA-256：
  `ae73a8adc02bc07926c3bcee98172cd2426b7720e6549c1d94d41fd6a2b178bd`；
- package 首次提交：`4eecb37440ecdf096b8a5e66fbeb7b698f54b633`；
- 当前输入：320 个 calibration identities；
- exact calibration packet：56 条，其中 38 条 overlay、18 条 inherited sentinels；
- calibration-only outside-union sentinel：`arxiv:2505.17862`。

### 2.2 核验结果

本次执行并核验：

- `python -m unittest scripts.survey.test_sf_stage1c_v2_precalibration -v`：15/15 tests 通过；
- package checker 报告 320 identities、13 claims、74 claim links、23 pending translations、15 closed
  pending routes、8 protocol templates、56 calibration items、0 reproduction anchors；
- 56/56 个 `fulltext_locator` 在本地数据根目录真实存在；
- blind packet 的 56 个 IDs 与 calibration manifest 一致；
- blind response 没有预填既有 role、primary direction 或 family labels；
- 两个 Stage-1B release receipts 均绑定各自 reviewed RC1；
- 当前 Git 工作树在审查开始时 clean，review target 可重复定位。

这些检查证明 RC1 是确定性的准备包，但现有 tests 主要验证“文件存在、数量正确、权限没有越界”。它们没有证明
coder response 能覆盖完整 schema，也没有实现或验证实际 agreement 计算。

## 三、当前方案已经做对的事情

### 3.1 输入身份和权限终于分开

当前合同正确地区分：

- 320 是 signed calibration input；
- 320 不是 full-mapping authority；
- calibration 不是 model/metric/reproduction execution；
- 两个 overlay release token 不等于 `SIGN_STAGE1C_V2_EXPERIMENT_MAPPING`。

这消除了上一版“准备 calibration”和“实际 full mapping”授权重叠的问题。

### 3.2 问题、干预、claim 与 family 的层级更合理

当前六个 problem nodes 回答“什么失败值得解释”，D0-D4 回答“改变什么变量”，claim 回答“在哪个 scope 内有
什么可证伪命题”，family 等待可比实验结构后再涌现。这套层级比按知识/技能/记忆或论文主题直接开分支更适合
博士研究。

15 个 pending labels 被逐项路由，同时全部保留 `candidate_problem_promoted=false`。其中 14 条进入三个新增
candidate nodes，1 条回到 `BUDGET_STOP_REPAIR`。这意味着团队承认问题空间可能扩张，但没有提前完成选择。

### 3.3 claim-level 去重方向正确

将 38 个 overlay records 通过 74 links 汇入 13 个中心命题，是对“不要做多个重复种子”的直接响应。论文可以
同时作为 support、instrument、boundary 或 falsifier 挂接到命题，而不是各自创建一个研究分支。

当前实现的问题不是“去重太多”，而是 claim 与 claim template 尚未分层。修复后应保留这套中心化组织方式。

### 3.4 calibration 与 full-audit blind review 被正确分开

N=56 是目的性 codebook calibration，不被描述为分布估计；以后 64-work blind sample 排除 calibration items。
这比把讨论过的样本重新称为 blind sample 更可信。

### 3.5 远域迁移和复现状态保持克制

23 个 text/VLM/GUI analogue 全部为 `WITHHELD_PENDING_TRANSLATION`，并记录 transfer failure 与 rejection
observation。五个 speech/omni candidates 均为 `CANDIDATE_NOT_ANCHOR`。没有因本地 PDF 存在就虚构数据、代码、
许可或 evaluator 已闭合。

## 四、阻断 calibration execution 的四项 P0

### P0-1：coder response 与 agreement contract 不同构

`agreement-contract-v1.json` 把以下字段列为 critical：

- `lineage_relation`；
- `core_member_compatibility`。

但 `calibration-blind-packet-v1.json` 的 `blank_response` 没有这两个字段。反过来，packet 含
`claim_links` 和 `protocol_template_links`，agreement contract 却没有说明如何计算这两个字段的一致性。

此外，codebook 把 claim merge/split 和 trained/gray-box/TF-Strict access 列为必须裁决的 critical
disagreements，但 agreement critical-field list 与 blank response 都没有独立字段表示它们。

因此，当前 agreement contract 要求计算一部分不存在的数据，同时遗漏一部分 codebook 自己声明为 critical 的
数据。这是可执行性错误，不是表述偏好。

**最小修复：** 生成一个唯一 `calibration_response_schema`，由 blind packet、agreement contract、codebook 和
checker 共同引用。critical fields 必须是 response schema 字段的严格子集；多标签、单标签、枚举、NA 和缺失值
规则逐项一致。

### P0-2：paper-level 空白表不能校准 experiment mapping

当前 `blank_response` 只有：paper disposition/role、problem/intervention、MM level、一个
`run_cell_boundary`、一个 `paired_status`、claim/template links 和 notes。

但后续 full mapping 声称要生产并依赖：

- 多个 `run_cell`；
- 每个 cell 的多个 `observation`；
- `paired_comparison`；
- dataset nodes；
- lineage/relation edges；
- translation contracts；
- family compatibility；
- review events。

一篇论文往往包含多个数据集、模型、access 条件、预算、baseline 和 intervention。把 run-cell boundary 与
paired status 压成每篇论文一个 scalar，无法检验 coder 是否会一致地切分 cell，也无法检验 observation 是否被
重复、comparability keys 是否完整、lineage 是否有来源。

如果现在完成 56 篇双编码，最多能证明高层 paper triage 的一致性，不能证明 experiment mapping codebook 已经
校准。

**最小修复：** 不需要让 calibration 先做完整论文复刻，但 56 个 response 至少要支持：

```text
paper_labels
run_cells[]
observations[]
paired_comparisons[]
dataset_nodes[]
dataset_edges[]
claim_decisions[]
translation_or_compatibility_decisions[]
source_locators[]
```

对明确没有某类对象的论文允许空数组并要求 `NONE_WITH_REASON`。agreement 在 paper-level 与 object-level 分开
计算，不能用一个总体百分比替代。

### P0-3：56 个 coder 输入没有绑定精确全文版本

本次核验确认 56/56 个 `fulltext_locator` 都能解析到本地文件，这是好事。但 packet item 只有 canonical ID、title
和路径，没有：

- arXiv/version 或出版版本；
- PDF SHA-256；
- e-print/提取文本 SHA-256；
- ledger row 或 source receipt；
- 当多个 rendition 存在时的优先级。

路径存在不等于两名 coder 读了相同字节。论文版本更新、重新下载或 PDF 与 proceedings 版本差异都可能改变
页码、表格和方法细节。agreement 若没有 source-byte identity，就不能区分“编码分歧”和“输入版本分歧”。

**最小修复：** 为 56 个 packet items 增加 `source_revision`、`primary_rendition`、`sha256`、`ledger_binding` 和
可选 alternate rendition。分发给 coder 的 isolated packet 也必须绑定同一 manifest。

### P0-4：13 个 canonical claims 目前并不满足自身的 scope-compatible 规则

`claim-registry-v1.json` 的 13 个 claims 全部：

- `claim_origin=CROSS_PAPER_SYNTHESIS`；
- `evidence_level=CALIBRATION_REQUIRED`；
- `transfer_status=WITHHELD_PENDING_SCOPE_AND_TRANSLATION_REVIEW`；
- 九个 scope fields 全部填同一个
  `DECLARED_HETEROGENEOUS_STRATA_NO_NUMERIC_POOLING`。

这诚实地说明证据异质，但也说明这些对象现在是 synthesis topics 或 claim templates，而不是“scope-compatible
propositions”。如果 task、dataset、model、access、budget 和 evaluator 都异质，就不能仅靠文字相似把它们视为
一个可承重 claim。

过度合并与重复种子同样危险：前者会抹掉语音/视觉、黑盒/灰盒、instrument/direct、trained/training-free 的
差别，并可能让远域论文数量制造虚假的支持强度。

**最小修复：** 保留 13 个中心 ID，但将其类型改为 `CLAIM_TEMPLATE` 或 `SYNTHESIS_QUESTION`。双编码时产生
`SCOPED_CLAIM_INSTANCE`：只有九维 scope 兼容且命题等价的实例才合并；template 下可同时挂多个 scoped instances、
support、boundary、contradiction 和 transfer analogue。不得按 paper link 数量投票。

## 五、需要在 calibration 前澄清的治理与独立性问题

### 5.1 owner release 与 independent review 的角色表述矛盾

两个 signature artifacts 的 `artifact_type` 都是 `OWNER_RELEASE_SIGNATURE_RECORD`，正文又写 owner supplied the
exact independent release verdict。此前 review request 和两份博导意见则明确要求 independent reviewer 签署。

本报告不撤销 owner 已登记的 token，也不质疑 owner 的最终授权权力；但“owner acceptance”和“independent
scientific review”不是同一个角色。如果治理模型是：AI advisory 提供独立科学意见，owner 接受建议并签发权限，
就应如实写成：

`INDEPENDENT_ADVISORY_REVIEW + OWNER_ACCEPTED_RELEASE`

如果协议真的要求签名者本身独立于 owner/team，则当前仍需一个独立 reviewer signature。必须在 coder 开始前
澄清，避免以后用词争议反向污染 320 input identity。

### 5.2 pre-calibration campaign index 已经陈旧

审查开始时，`wiki/audit/system-first-stage1c-v2-precalibration/INDEX.md` 仍写“两项 Stage-1B release
signatures remain absent”，而 HOT/CURRENT 和两个上游 campaign indexes 都写 signatures 已存在。本次 review
transaction 已同步修正 cold router 为“随后已登记”，并明确 full-mapping signature 仍缺失；历史 owner
authorization 原文保持不改。

### 5.3 两名 coder 的“独立”尚未操作化

blind packet 声明 `repository_access_should_be_withheld=true`，但没有 coder intake/distribution transaction。至少
还需冻结：

- coder A/B 的 actor type、身份或模型/版本；
- prompt/codebook/response-schema/packet hash；
- 是否接触过已有 records、claim links、problem routes 或本仓库；
- 开始和提交时间；
- coder 间不得交流的窗口；
- adjudicator 身份与其可见信息；
- AI coder 的 sampling/configuration；
- 同一模型的两次运行不得被默认写成独立研究者。

为快速推进，可以让两名隔离 coder 使用相同的 label-hidden packet；但至少一个 human/domain-expert adjudicator
应处理 reproduction、lineage、MM3、EXACT_PAIRED 和 TF-Strict access 等承重分歧。

## 六、P1 方法改进

### P1-1：JSON Schema 目前只保证“有字符串”，没有保证“符合 codebook”

12 个 schema definitions 都存在，但 categorical fields 普遍只是 `type=string, minLength=1`，enum 值总数为 0；
`claim_record.scope` 只是无约束 object。`source_locators` 允许空数组，`review_event.prior_event_id` 又要求首个事件
必须有非空前驱。

最小强化应包括：

- codebook enums；
- required scope keys；
- array `minItems/uniqueItems`；
- ID pattern 与 cross-reference；
- first review event 允许 `prior_event_id=null`；
- `NONE/UNKNOWN/NOT_APPLICABLE` 的互斥规则；
- source locator 对承重对象至少一条。

不需要开发通用 schema 平台，只需使 coder response 和未来 mapping output 无法用拼写不同的自由字符串悄悄
绕过合同。

### P1-2：agreement pass/fail 规则仍不完整

当前只给出 critical-field raw agreement ≥85%。还需在编码前声明：

- multi-label 的“raw agreement”究竟指 exact match、Jaccard 还是其他量；
- AC1/AC2、Jaccard、micro/macro F1 是门还是诊断；
- NA/UNKNOWN 如何进入分母；
- 一个类别在 56 条中没有正例时如何标记“未校准”；
- object extraction 中一方多切/少切 run cell 时如何匹配对象；
- 第二轮仍未达阈值时必须停止并请求新 review，而不是继续全量 mapping。

建议实现一个小型、确定性的 agreement script，在 coder 开始前用合成 fixture 验证计算规则。这里不需要 fuzzing
或对抗式鲁棒性工程。

### P1-3：18 个 inherited sentinels 是目的样本，不代表 320 的自然分布

当前合同已经承认这一点，应继续保持。未来不能把 calibration agreement 外推为“320 篇所有类别都同样可靠”。
对低频且未在 56 条出现的对象，应标记 `NOT_CALIBRATED`，在 full mapping 中通过 100% second review 或新增
targeted calibration 处理。

### P1-4：五个 reproduction candidates 仍只是待办清单

read-only closure 是当前 owner token 已授权的工作，但五项目前都没有 evidence-bound completion。它不阻断
codebook repair，可与 RC2 并行；但在 Stage-1C closeout 前至少应：

1. 完成 Full-Duplex-Bench-v2 与 Audio MultiChallenge 的公开资产/许可/evaluator closure；
2. 若第一候选不可闭合，按预注册顺序切换；
3. 只选一主一备；
4. 保留 `CANDIDATE_NOT_ANCHOR`，直到 Stage-2A 真正具备复现条件。

## 七、建议的一次性 RC2 修复清单

为了避免继续堆 amendment，建议直接原位 supersede 当前 pre-calibration workbench，生成一个 RC2 manifest。只做
以下必要修复：

1. 建立唯一、强类型 `calibration_response_schema`；
2. 将 12 类 mapping objects 中需要校准的对象加入 56-work response；
3. 统一 codebook、packet、agreement critical fields 和 checker；
4. 为 56 个全文输入增加版本、SHA-256 和 ledger binding；
5. 把 13 个对象重命名为 claim templates，并允许 scoped instances；
6. 定义 coder intake、隔离分发、exposure 与 adjudicator transaction；
7. 实现并 fixture-test agreement computation；
8. 明确第二轮仍失败时的 stop/escalation；
9. 澄清 owner release 与 independent advisory 的角色；
10. 更新陈旧的 pre-calibration campaign index；
11. 并行完成两个最高优先 reproduction candidates 的只读 closure。

这些修复不需要：

- 新一轮 broad discovery；
- 再增加 seed；
- 重新编码 320 篇；
- 运行模型或 benchmark；
- 创建 research branch；
- 讨论技术 novelty；
- 建设复杂的通用鲁棒性框架。

## 八、推荐的快速执行顺序

### Gate A — RC2 method closure

关闭本报告四项 P0，生成新 manifest 和 deterministic contract report。此阶段可同时完成两个 reproduction
candidate 的只读 closure。

### Gate B — independent calibration

1. 冻结 coder identities/exposure 与 isolated source-byte manifest；
2. 两名 coder 独立完成 56 条；
3. 计算 paper-level 与 object-level agreement；
4. 公布 pre-adjudication metrics；
5. 全部分歧 adjudicate；
6. 若首次未达门，只允许一次 codebook consolidation + 全 56 重编码；
7. 若第二次仍未达门，停止并返回 reviewer，不得进入 full mapping。

### Gate C — calibration review

独立 reviewer 核查 coder provenance、agreement denominator、分字段结果、未校准类别、adjudication log 和最终
codebook。只有通过后才考虑 `SIGN_STAGE1C_V2_EXPERIMENT_MAPPING`。

### Gate D — full mapping

取得 signature 后才允许 320-paper disposition、experiment extraction、dataset graph、evidence-led family
synthesis 和未执行 branch dossiers。至少 64 个未参与 calibration 的 unique works 进入预注册 blind review；承重
lineage、reproduction、family evidence state 和 branch card 继续 100% second review。

模型、metric、reproduction 与 prototype 仍需后续独立 authority。

## 九、对研究团队是否继续执行的明确意见

**同意团队继续，并建议立即执行一次有界 RC2 修复。**

同意的工作：

- response/schema/agreement 对齐；
- source-byte binding；
- claim template/scoped instance 分层；
- coder isolation 与 agreement fixture；
- read-only reproduction closure；
- index/provenance 澄清。

暂不同意的工作：

- 立即启动正式 56-work calibration；
- 把当前 15 tests 通过解释为方法已经校准；
- 把 13 个异质 synthesis headings 当作 13 个已证实 claims；
- 把 owner release 自动描述为 independent reviewer signature；
- 开始 320-paper full mapping；
- 运行研究模型、metric、复现或 prototype；
- 选择问题、方向或讨论 novelty。

这不是回到 Stage-1B，也不是继续打补丁。当前距离 calibration 很近，最合理的做法是在 coder 尚未投入之前把
输入、输出和 agreement 单位对齐，随后一次完成真正可承重的双编码。

## 十、给 reviewer 的建议 verdict 文本

建议 reviewer 返回：

`WITHHOLD_CALIBRATION_EXECUTION_PENDING_BOUNDED_RC2_REPAIR`

并附：

> The 320-work calibration input, problem/intervention separation, bounded discovery stop rule,
> protocol-template demotion and reproduction boundaries are acceptable. Calibration execution is
> temporarily withheld because the coder response does not cover all agreement-critical or
> experiment-mapping objects, the 56 source texts are not version/hash-bound in the coder packet, the
> 13 synthesis headings are not yet scoped claim instances, and coder/agreement transactions are not
> fully operationalized. The team is authorized to perform one bounded RC2 method repair and
> read-only reproduction-candidate closure. This verdict does not authorize full mapping, research
> execution, problem selection or a novelty verdict.

## 十一、权限、provenance 与失效条件

- 本文件是 AI 生成的 reviewer-facing 博导级建议，不声称人类或 independent reviewer 签名；
- 本文件不撤销或签发 owner token；
- 本文件不改变 `wiki/Research-Objective.md` 的当前 authority；
- 本文件没有运行研究模型、API、benchmark metric、复现或 prototype；
- 本文件不作问题选择、branch selection 或 novelty verdict；
- 本文件只对 manifest SHA-256
  `ae73a8adc02bc07926c3bcee98172cd2426b7720e6549c1d94d41fd6a2b178bd` 有效；
- 若 RC2 关闭四项 P0，则本文件的 withholding 应由针对 RC2 exact manifest 的新 review supersede；不得通过
  amendment 修改本文件。
