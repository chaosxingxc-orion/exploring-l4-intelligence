---
review_id: V6-RESPONSE-AND-ASEL-DRAFT-ADR-2026-07-13
date: 2026-07-13
timezone: Asia/Singapore
stage: Stage-1 closure / pre-Stage-2 gate audit
primary_reviewed_object: wiki/2026-07-13-response-v6-to-signoff-adversarial-review.md
primary_reviewed_git_commit: 311689818e6650674fac2cc1c19dbe4ee94baa29
primary_reviewed_sha256: beddc2609ddbddfb8943048df6301e024f58f2dc8f666109efc5ae5dc5117146
prior_review_sha256: 64389f7fee45ea2aad4c9880fffe9293b621e52c492b79eca28d206290f761cf
supplementary_in_progress_object: wiki/2026-07-13-stage2-proposal-ASEL-v0.1-for-reviewer-verification.md
supplementary_git_commit: 84c6cf64d0a979a5d4f8222a00b9eb746378f270
supplementary_snapshot_status: INITIALLY_UNTRACKED_THEN_COMMITTED_UNCHANGED_DURING_REVIEW
supplementary_snapshot_sha256: 300ccfb24006b2b49aeafbc16db7fecede5ccd2b766d58339bca5f3c75abeefa
response_adjudication: SUBSTANTIVELY_ACCEPTABLE_BUT_REQUIRES_RECORD_CORRECTIONS
p0a_adjudication: VERIFIED_CLOSED_FOR_DESIGNATED_SNAPSHOT
stage2_draft_structure_verification: REFUSED_RETURN_FOR_RECONSTRUCTION
m2_unfreeze: PROHIBITED
scoped_signoff_requested_by_team: false
integrity_verdict:
  fabrication: NOT_ESTABLISHED
  falsification: NOT_ESTABLISHED
  plagiarism: NOT_ASSESSED_NO_NEW_SIGNAL
  qrp_risk: HIGH_UNTIL_P0_CONFIG_HISTORY_AND_INDEPENDENT_AUDIT_CLOSE
  disclosure_behavior_change: IMPROVED
  independent_integrity_audit: STILL_REQUIRED
mutation_statement: 仅新增本日期审查报告；未修改 v6、proposal、代码、测试、登记册、草稿或实验工件
---

# 对 Response v6 与正在起草的 A-SEL Stage-2 方案的博导级对抗审查

## 0. 终局裁决

本轮必须分开裁定两个对象，不能用一个“通过/不通过”混在一起：

1. **对 v6 回复本身：实质上大体接受，但要求更正记录。** 团队接受上一轮退回、不申请立即重签、
   不把 checker 当科学证明，并把真正未完成的科学项继续标 OPEN。这是正确方向。P0-A 中 release
   manifest 与 conformance output 的事务修复，我方 fresh 核验可以复现。
2. **对当前正在起草的 A-SEL Stage-2 v0.1：结构验证不通过，退回重构。** 草稿保持
   `DRAFT / NOT-FROZEN / authorizes_data_sensitive_work=false` 是正确的；但它尚未解决 A-SEL 的博士级
   新颖性、最强比较、同一 ρ 对象、跨任务效用尺度与具体 selector 对象等载重问题。
3. **M2 继续冻结。** 当前没有理由怀疑团队已暗中恢复 M2：W1 `_repro` 可见文件的最近修改时间仍停在
   2026-07-12，v6 之后观察到的是文档草稿，而不是新实验工件。但这只是有限的磁盘表面证据，不能替代
   session/shell/MLflow/外部路径的独立完整性审计。
4. **仍没有证据建立 FFP。** v6 主动把 `c7528fe` 提交信息与实际提交内容不符登记为 discrepancy，
   这是降低“故意掩盖”怀疑的正面行为。与此同时，v6 又产生了新的 snapshot/hash 元数据错误，说明
   证据治理尚未稳定；它们目前是可纠正的记录/QRP 问题，不是已证 falsification。

压缩成机器式裁决：

```text
V6_RESPONSE_SUBSTANCE = MOSTLY_CORRECT
V6_RESPONSE_RECORD = CORRECTIONS_REQUIRED
P0_A_TRANSACTION = VERIFIED_CLOSED_FOR_13b5a10/a532da0 + WRAPPER_7b895b5
P0_B = OPEN
ASEL_V0_1_STRUCTURE = FAIL_RETURN
M2_UNFREEZE = NO
FFP = NOT_ESTABLISHED
INDEPENDENT_AUDIT = STILL_REQUIRED
```

---

## 1. 审查对象、快照与限制

### 1.1 主对象：v6 回复

- 文件：`wiki/2026-07-13-response-v6-to-signoff-adversarial-review.md`
- 实际首次进入 Git 的提交：`311689818e6650674fac2cc1c19dbe4ee94baa29`
- 该提交的直接父提交：`7b895b5bebc8b92a4f37dfa9fdc43289b140806b`
- 文件 SHA-256：`beddc2609ddbddfb8943048df6301e024f58f2dc8f666109efc5ae5dc5117146`

### 1.2 补充对象：正在处理的 Stage-2 草稿

用户不仅问 v6 的回复，也问团队“正在处理的工作是否正确”。审查开始时，根仓 HEAD 为 `3116898`，
工作树存在一个未跟踪文件：

```text
wiki/2026-07-13-stage2-proposal-ASEL-v0.1-for-reviewer-verification.md
```

审查快照 SHA-256 为：

```text
300ccfb24006b2b49aeafbc16db7fecede5ccd2b766d58339bca5f3c75abeefa
```

审查收尾时，团队已将**完全相同的字节**提交并推送为
`84c6cf64d0a979a5d4f8222a00b9eb746378f270`；SHA-256 未漂移。它因此不再是 untracked，但仍明确是
`DRAFT-v0.1 / NOT-FROZEN`。本报告只裁定上述固定字节快照，不把它当团队终稿，也不要求团队停止正常的
文档修订；但在这些结构问题闭合前，不得把草稿冻结为 v1.0 或解冻 M2。

### 1.3 本轮没有做什么

- 没有修改 v6、A-SEL 草稿、v4.2、代码、登记册或实验工件；
- 没有访问可能位于未保存对话、删除文件、外部 notebook 或其他磁盘路径的尝试；
- 没有对 574 个历史工件做逐项数值重算；
- 没有替机构研究诚信办公室判断人员主观故意；
- 没有把“当前可见目录未出现新实验 mtime”表述为“证明绝无秘密实验”。

---

## 2. Fresh 证据对账

### 2.1 P0-A 的正面核验

| 证据 ID | 对象 | fresh 结果 | 裁定 |
|---|---|---|---|
| V6-E01 | 根仓时间线 | 审查开始为 `3116898`，A-SEL 草稿 untracked；收尾变为 `84c6cf6`，草稿以相同 hash 提交并推送；除本审查报告外工作树无其他未提交项 | v6 与草稿均有 Git 谱系；manifest 的 designated HEAD 仍是更早 `13b5a10` |
| V6-E02 | W1 当前 HEAD | `a532da06296681b3bbb30446a6fa285ca5bed508`，clean，远端同步 | v6 所列 W1 快照成立 |
| V6-E03 | release manifest | 记录 umbrella `13b5a10`、W1 `a532da0`，两者 `dirty=false`；manifest-only wrapper 为 `7b895b5` | 上一轮 F-S2 的 P0-A 事务已正确重做 |
| V6-E04 | manifest 7 个关键工件 | 7/7 当前 SHA-256 与 manifest 一致 | “零漂移”主张成立，但范围仅限这 7 项 |
| V6-E05 | stored checker output | proposal 记录 hash 与最终 v4.2 均为 `3f0ac5b6...` | F-S3 已按要求关闭 |
| V6-E06 | fresh checker | 22/22 PASS，0 failed，输入 proposal hash=`3f0ac5b6...` | 当前自洽规则仍可复现；不证明科学有效性 |
| V6-E07 | W1 fresh standard entry | 159 passed，3 warnings，0 failed，83.58s | manifest 的 159 passed 不是虚构 |
| V6-E08 | P0 registry | `pass_conditions_met=false`；配置选择轨迹与独立只读审计仍未闭合 | v6 把 P0-B 保持 OPEN 是正确的 |
| V6-E09 | W1 `_repro` 可见 mtime | 最新可见工件为 2026-07-12；v6/P0-A 后未见新实验工件 | 没有发现违反冻结的正面信号，但证据覆盖有限 |

P0-A 因此可以被精确表述为：

```yaml
p0a_release_transaction:
  designated_umbrella_snapshot: 13b5a10235cc544cd0577948ce255ccc765c8e0a
  designated_w1_snapshot: a532da06296681b3bbb30446a6fa285ca5bed508
  manifest_wrapper_commit: 7b895b5bebc8b92a4f37dfa9fdc43289b140806b
  manifest_key_hashes: 7_of_7_match
  checker_final_input_hash: match
  verdict: CLOSED_FOR_THAT_DESIGNATED_SNAPSHOT
  does_not_mean:
    - current_worktree_is_clean_forever
    - v6_response_itself_is_inside_7b895b5
    - P0B_or_science_is_closed
```

### 2.2 v6 新产生的 provenance 不一致

#### V6-E10：`reviewed_snapshot_responded_to` 引错了报告哈希

v6 frontmatter 写：

```text
reviewed_snapshot_responded_to: umbrella c7528fe / report sha256 cd987ff0…
```

但 v6 的 `responds_to` 是上一轮审查报告
`2026-07-13-v42-remediation-signoff-doctoral-adversarial-review.md`。该审查报告当前及入库 SHA-256 是：

```text
64389f7fee45ea2aad4c9880fffe9293b621e52c492b79eca28d206290f761cf
```

`cd987ff0...` 是上一轮审查报告内部所审的**整改报告旧快照**的 SHA-256，而不是 reviewer report 的
SHA-256。也就是说，v6 把“被回复的审查报告”和“审查报告所审的对象”混成一个 `report sha256`。

正确写法应同时固定两层：

```yaml
responds_to_reviewer_report:
  path: wiki/2026-07-13-v42-remediation-signoff-doctoral-adversarial-review.md
  sha256: 64389f7fee45ea2aad4c9880fffe9293b621e52c492b79eca28d206290f761cf
reviewer_report_reviewed_snapshot:
  umbrella_commit: c7528fe05f9d44bfb1d377d2939a6fd206eb6926
  remediation_report_sha256_at_that_snapshot: cd987ff0fc2b0f81e5576a7a6586f4d093f263555f06a31b9fdd2f50e5a431cd
```

#### V6-E11：`this_response_snapshot` 指向一个不存在该回复的父提交

v6 写：

```text
this_response_snapshot: umbrella 7b895b5 / W1 a532da0
```

但 `git cat-file -e 7b895b5:wiki/2026-07-13-response-v6-to-signoff-adversarial-review.md` 返回不存在；
v6 只在下一提交 `3116898` 中出现。`7b895b5` 是 response commit 的父提交和 P0-A evidence snapshot，
不是 `this_response_snapshot`。

正确字段应是：

```yaml
evidence_snapshot_before_response:
  umbrella: 7b895b5bebc8b92a4f37dfa9fdc43289b140806b
  w1: a532da06296681b3bbb30446a6fa285ca5bed508
this_response_git_commit: 311689818e6650674fac2cc1c19dbe4ee94baa29
```

这两处错误没有改变任何效应量，也没有把失败改成成功，故当前不构成 falsification 证据；但在团队刚刚承认
`c7528fe` 提交信息与内容不符之后，马上再次写错快照层级，说明 provenance 生成仍依赖手工叙事，尚未达到
可签署的稳定性。

### 2.3 v6 的 YAML 实际上不是 13 项可机读记录

v6 有两个 YAML fenced blocks：FUNDAMENTAL 段连续写了 7 个同名顶层键 `response_item:`，MAJOR 段连续
写了 6 个。机械核验结果：

```text
literal response_item occurrences = 13
YAML block 1 parsed top-level keys = [response_item]
surviving finding_id = F-S7
YAML block 2 parsed top-level keys = [response_item]
surviving finding_id = M-S6
```

常见 PyYAML 会静默让后项覆盖前项；严格 YAML parser 则会把重复键判错。于是人眼看到 13 项，团队 AI
实际只能可靠读到 2 项。这直接违反“让对方 AI 充分理解”的交付目标。

应改成列表：

```yaml
response_items:
  - finding_id: F-S1
    # ...
  - finding_id: F-S2
    # ...
```

或每项用独立 YAML 文档并以 `---` 分隔。修复后必须有 checker 断言：ID 集精确等于 13 项、无重复、无缺失。

---

## 3. 六轮对抗式评审

### Round 1：最大善意审查——v6 是否真正接受了退回，而不是换词争辩？

是。v6 做对了以下关键动作：

- 13 项全部 ACCEPT，没有用 owner 权威否定仓库事实；
- 明确“不申请立即重签”；
- F-S1/F-S4/F-S5/F-S7 与 M-S2 至 M-S6 保持 OPEN/PARTIAL；
- 把 F-S6 只关成 `CLOSED-as-record`，没有声称独立审计已完成；
- 把 M-S1 关闭为“证据路线已选择”，并接受 public deterministic 的 development/controlled-benchmark 等级帽；
- 主动登记 `c7528fe` 不真实的提交信息；
- 没有拿 159 passed 或 22/22 回答科学有效性。

**Round 1 裁决：回复的研究诚信姿态有实质改善，不是表演式接受。**

### Round 2：证据事务红队——声称 CLOSED 的项目是否真的关闭？

F-S2/F-S3 可以关闭：clean designated commits、manifest wrapper、7/7 hashes、最终 proposal checker hash
均可复核。叙事版 12/12 已明确移出发布证据集。错误 CLI 路径也在 W1 `a532da0` 修正。

但 v6 自己的 frontmatter 又写错了 reviewer report hash 与 response commit。这里应采用“科学事实修复已闭合，
回复工件 provenance 仍需勘误”的双层结论，不能因为 P0-A 成功就称整个回复记录完美。

**Round 2 裁决：P0-A 事务通过；v6 文件自身需要两项 append-only/直接勘误。**

### Round 3：状态机红队——13 项的 after-status 是否诚实？

逐项审后，团队没有把实质未完成项偷偷判 CLOSED。唯一需要语义收窄的是 M-S1：

```text
CLOSED-AS-ROUTE-DECISION
IMPLEMENTATION-IN-FRESH-PROPOSAL = OPEN_UNTIL_FROZEN
```

因为 owner 已选 public deterministic + 等级帽，路线选择本身可关闭；但 canonical Thesis/Per-Work-Status 与
最终 v1.0 的 title/abstract/claim ledger 还没有完全同步。v6 中 `scientific_claim_enabled: none` 已防止该标签
被立即外推，故不把它升级为新的 FUNDAMENTAL。

**Round 3 裁决：13 项实质状态基本正确；状态名还需更细的“决策关闭/执行开放”区分。**

### Round 4：领域新颖性红队——A-SEL 真的是未被解决的问题吗？

当前草稿的最近邻表把重心放在 WavRAG/VoxRAG/AudioRAG/SQuTR 与通用 BoN reward hacking，却漏掉了
与 A-SEL **直接同构**的 ASR hypothesis selection/rescoring 文献：

- 1997 年已有在 N-best 上显式最小化期望 WER、从候选中选择输出；
- 2000 年已有 N-best ROVER/segmental MBR，把投票解释为最小 Bayes 风险；
- 2022 年已有利用全 N-best、BERT confidence 与 learning-to-rank 的 rescoring；
- 2023 年 NoRefER 已做 reference-free ASR quality/ranking；
- 2024 年 HypR 系统比较 N-best reranking/error correction；
- 2024 年 ProGRes 已做 zero-shot LLM + confidence + sequence scoring 的 N-best 扩展和重排；
- 2025 年 Li & Niehues 已直接研究 LLM-based ASR hypothesis selection，并比较概率/指令方法；
- 2026 年 READ 更直接：无需额外训练，用语音—假设 acoustic discrepancy 做 reference-free hypothesis
  evaluation/refinement，并报告在噪声条件下的 ASR 改善。

因此，“冻结模型、多采样、label-free proxy、从 K 个候选选一个”不是新研究对象，而是历史悠久的
N-best rescoring / quality estimation / MBR 决策问题在 speech/omni LLM 上的一个实例。

**Round 4 裁决：A-SEL 可以成为测量研究，但目前未建立博士级方法新颖性；`在语音 MLLM 上没有先例`
不得保留为无证据陈述。**

### Round 5：方法对象红队——即使 A-SEL 值得测，当前主门能证明贡献吗？

不能。草稿把 selector vs pool-mean 设为 H1/H2 的 primary，而把 MBR 设成 secondary H3，pessimistic/hedged
甚至没有 primary 原子。这样会允许以下结果被宣布 Go：

```text
selector > random pool expectation on two selected task families
BUT selector <= MBR / READ / NoRefER / a reasonable confidence reranker
```

这只能证明 selector 不是随机选，不能证明它相对已有方法有科学增量。pool-mean 是必要 sanity baseline，
不是 closest-neighbor novelty baseline。

**Round 5 裁决：最强 comparator 必须进入 load-bearing primary gate；当前 H1/H2 结构不通过。**

### Round 6：诚信反向审查——这些新问题是否证明作假？

不证明。支持谨慎而非指控的事实包括：

- v6 主动接受全部负面事实并登记前一提交信息不实；
- 当前草稿明确标 DRAFT/NOT-FROZEN，不授权数据工作；
- 没有发现新 M2 工件或虚构的测试结果；
- P0 仍诚实保持 NOT_PASS；
- 新问题主要是快照字段、YAML schema、设计/新颖性不足。

但继续保持高 QRP 警戒的理由是：

- 刚修复证据事务又写错两层 snapshot provenance；
- 配置搜索轨迹仍无法完整回溯；
- A-SEL 如果用“training-free RL 新范式”包装经典 reference-free reranking，而不披露最接近文献，会构成
  严重的新颖性夸大风险；
- 若强 comparator 继续被放在 secondary，成功判定会系统性偏向正结果；
- 同一 ρ 名称被用于不同低锚和不同聚合，会造成指标身份漂移。

**Round 6 裁决：FFP_NOT_ESTABLISHED；QRP 风险仍高，但团队当前披露行为改善。独立审计仍为 REQUIRED。**

---

## 4. 对 v6 原 13 项回复的逐项裁定

| finding | v6 after-status | 本轮裁定 | 说明 |
|---|---|---|---|
| F-S1 阶段门序 | OPEN | **ACCEPT** | 门已改 BEFORE_STAGE2_UNFREEZE；fresh proposal 正在起草但未通过 |
| F-S2 release manifest | CLOSED | **ACCEPT-CLOSED** | 指定快照、wrapper、祖先与 7/7 hashes 均复核通过 |
| F-S3 checker final input | CLOSED | **ACCEPT-CLOSED** | stored 与 fresh 均指向 `3f0ac5...` |
| F-S4 upstream corpus | PARTIAL | **ACCEPT-PARTIAL** | 标签已诚实；clean fetch 与代码语义仍 P0-B |
| F-S5 group-disjoint | OPEN | **ACCEPT-OPEN** | 契约正确，代码/负例尚未交付 |
| F-S6 independence wording | CLOSED-as-record | **ACCEPT-CLOSED-AS-RECORD** | 独立审计本体仍 OPEN，不得混淆 |
| F-S7 P0 NOT_PASS | OPEN | **ACCEPT-OPEN** | registry fresh 仍为 false |
| M-S1 evidence grade | CLOSED | **ACCEPT-AS-ROUTE-DECISION** | public deterministic 等级帽已选；canonical/final proposal 执行仍待同步 |
| M-S2 SESOI dossier | OPEN | **ACCEPT-OPEN** | 草稿 FG-1 仍是待交付，不是数值依据 |
| M-S3 estimand | OPEN | **ACCEPT-OPEN; NEW_IDENTITY_CONFLICT_FOUND** | 草稿改 ρ 低锚，须新裁定，见 F-D3 |
| M-S4 generation/comparator | OPEN | **ACCEPT-OPEN; DRAFT_NOT_YET_VALID** | 多池原则已写，强 comparator 仍未进 primary |
| M-S5 δ_corr | OPEN | **ACCEPT-OPEN** | 四臂已写，具体阈值/信号/branch 尚未冻 |
| M-S6 small-cluster simulation | OPEN | **ACCEPT-OPEN** | DGP 要素已列，完整可执行契约尚未交付 |

总体上，v6 **没有通过状态标签偷关科学问题**。这点应明确肯定。新退回主要来自 v6 自身记录格式，以及 v6
之后出现的 A-SEL 草稿结构，而不是因为 13 项回复全部错误。

---

## 5. v6 回复工件的新发现

### R6-M1：被回复报告 hash 与其被审对象 hash 混淆

**严重度：MAJOR / PROVENANCE**

证据见 V6-E10。修复不需要实验，只需把两层对象明确命名并写全 hash。以后所有 response frontmatter 必须由
脚本读取 Git/object hash 生成，不再手填缩写。

### R6-M2：`this_response_snapshot` 指向父提交

**严重度：MAJOR / PROVENANCE**

证据见 V6-E11。若一个 response 要自指其 commit，会有“文件内容在提交前不知道最终 commit”的循环问题。
正确方法是：frontmatter 固定 `evidence_snapshot_before_response`；提交后由 wrapper manifest 或下一条
append-only receipt 记录 response commit，不在文件里伪装自洽。

### R6-M3：13 项 YAML 因重复键退化为 2 项

**严重度：MAJOR / MACHINE-READABILITY**

这是确定性 parser failure，不是样式偏好。必须改成列表并加 schema test。任何下游 AI 在修复前不得把 v6
YAML 当完整 finding registry。

### R6-M4：canonical status 尚未同步 A-SEL 唯一 headline

**严重度：MAJOR / GOVERNANCE CONSISTENCY**

`Project-Thesis.md` 与 `Per-Work-Status.md` 仍主要描述“RDU + selector、v4.2 待签”，而续32 已把 A-SEL 设为
唯一 headline、RDU 降为 secondary、v4.2 归档。Decision Log 的 append-only 记录是真实的，但 canonical
north star/status board 还不是当前单一视图。

团队不应在草稿未通过时把 Stage-2 状态写成已进入；正确同步语义是：

```text
Stage 1 identity selected = A-SEL
fresh Stage-2 proposal = draft / not frozen / gate not passed
RDU = secondary/ablation
M2 = frozen
```

---

## 6. 当前 A-SEL Stage-2 v0.1 的 FUNDAMENTAL 问题

### F-D1：新颖性 survey 漏掉了真正同构的 ASR selector 文献

**严重度：FUNDAMENTAL / SCIENTIFIC IDENTITY**

草稿 §S1 最近邻主要列 RAG 数据/系统与通用 BoN；§3.1 断言所提测量与判死结构“在语音 MLLM 上没有先例”。
但 A-SEL 的方法对象是：生成 N/K 个 speech hypotheses，以无参考或 proxy 分数选一个。这与 N-best rescoring、
confidence/QE ranking、MBR 和 recent LLM hypothesis selection 直接同构。

Stage-1 closure 必须重新回答：

1. 本研究提出的是**新 selector**、新 proxy、还是只是更严格的评测协议？
2. 相对 READ/NoRefER/ProGRes/MBR，究竟新增哪个数学或工程对象？
3. 若唯一新意是“同协议跨两个 speech task families 测量”，贡献应定位为 benchmark/measurement study，
   而不是新 RL 方法。
4. 若 selector 是一次性 fixed-score argmax，应在标题/摘要并列写
   `reference-free N-best reranking / test-time selection`，不能只用 `training-free RL` 重新命名旧问题。

### F-D2：随机期望是 primary，最强近邻却是 secondary

**严重度：FUNDAMENTAL / CLAIM-BASELINE MISMATCH**

H1/H2 只要求 selector 超过 pool-mean 并跨两个被选中的任务族；H3 对 MBR 的比较是 secondary，
pessimistic/hedged selector 没有可杀死 headline 的原子。这个门会奖励“略好于随机但不如已有方法”的结果。

最低可接受结构是：

```yaml
primary_gate:
  required:
    - selector_minus_pool_mean_lower_CI_gt_family_SESOI
    - selector_minus_strongest_frozen_baseline_lower_CI_gt_delta_novelty
    - positive_replication_on_second_preregistered_family
  strongest_baseline_family:
    - MBR
    - READ_or_acoustic_grounded_reference_free_metric
    - NoRefER_or_best_reproducible_QE_reranker
    - pessimistic_or_hedged_selector
  selection_rule_for_strongest_baseline: frozen_before_M2
```

如果资源不允许跑全部，必须在数据前用可辩护规则选一个 strongest baseline，而不是把所有强基线降 secondary。

### F-D3：草稿把 ρ 换了对象，却声称与 owner 原 ρ 一致

**严重度：FUNDAMENTAL / METRIC IDENTITY DRIFT**

项目 canonical G0/Thesis 的 ρ 是：

```text
rho_greedy = (U_selector - U_greedy) / (U_oracle - U_greedy)
```

草稿 H4 改成：

```text
rho_pool = (U_selector - U_pool_mean) / (U_oracle - U_pool_mean)
```

并且是先逐 group/generation 算 ratio 再取期望；此前 v4.2 使用 aggregate-ratio。三者不是同一个 estimand。
pool-mean 作为 equal-K 低锚比 greedy 更公平，这个设计可能更好，但必须**改名并重新裁决**，不能在文字上仍称
“与 2026-07-11 唯一主问题 ρ 一致”。

要求同时报告但只选一个 primary：

```yaml
rho_greedy:
  purpose: deployment_budget_unmatched_realization
rho_pool:
  purpose: equal_K_selection_realization
aggregation:
  primary: ratio_of_expectations | expectation_of_ratios
  choice_reason: preregistered
  denominator_floor: family_specific
```

owner 必须明确签署“哪个 ρ 承载 A-SEL headline”，并同步 Thesis、Decision Log 与 proposal。

### F-D4：被检验的 selector 仍是一个巨大搜索家族，不是具体方法对象

**严重度：FUNDAMENTAL / RESEARCHER DEGREES OF FREEDOM**

草稿说 M2 将枚举/搜索 `weights/K/threshold/prompt/embedder`，还允许 diff-family verifier 与
non-model verifier。可是在 FG-1..FG-10 中，没有一个明确冻结：

- proxy feature 公式与输入字段；
- selector architecture；
- 每个权重/阈值/prompt/embedder 的有限候选集合；
- shared-across-task 还是 task-specific；
- 搜索算法、预算与 tie-break；
- 某一 verifier 失败后到底“剔除”还是“换独立族”的唯一 branch；
- 选出的 winner 如何在第二任务族复现，是否允许重新调参。

若每个任务族都独立调一套 selector，再把两次成功叫“跨任务复现”，复现的是调参流程，不是同一个方法。

必须新增 `FG-SELECTOR-OBJECT`，在解冻前冻结 operator schema、搜索空间、跨任务共享参数和 winner transfer
规则。否则 confirmatory split 再干净，也只是在验证一个开发集上选出的高自由度赢家。

### F-D5：H1/H2 共用 `SESOI_sel`，但 U 跨任务没有同一量纲

**严重度：FUNDAMENTAL / ESTIMAND SCALE**

草稿候选任务包括：ASR `U=-WER`、QA `U=EM/F1`、retrieval-QA “正确率”。它们虽然都可写成数字差，
但一个绝对百分点在三个构念上的成本/价值不同。用同一个 `SESOI_sel` 检验 H1 和 H2，没有量纲与效用依据。

可接受方案二选一：

1. 为每个 family 外部锚定 `SESOI_ASR / SESOI_QA / SESOI_RETRIEVAL`，H1/H2 分别用各自阈值；或
2. 预先定义可解释的共同 normalized utility（含成本），证明单元变换不随观测结果调整。

同时必须明确 H2 是：

- 同一 frozen selector 零再调参迁移；
- 还是同一 selector family、任务内重新标定；
- 还是完全独立方法复现。

三种证据强度不同，不能都叫“跨任务正向复现”。

---

## 7. 当前 A-SEL 草稿的 MAJOR 问题

### M-D1：假设、CI 与“双侧”规则不一致

草稿写 `θ ≥ SESOI`，Go 条件却是 CI lower bound `> SESOI`，同时写 `α=0.05，双侧`。需要明确：

- null/alternative：`H0: θ ≤ SESOI` vs `H1: θ > SESOI`；
- 使用单侧 α=.05，还是双侧 95% CI 的下界（相当于更保守的一侧判定）；
- Holm 校正作用于 p 值还是同时构造的 family-wise CIs；
- equality 落在 kill、pivot 还是 fail-to-reject。

当前文字足以让两个统计实现给出不同 verdict。

### M-D2：Research-Proposal-Template §4 被错误映射为“未来 M2 标定协议”

模板 §4 要求 baseline reproduction + method pilot + Repro Manifest + held-out validity + 独立复跑。
草稿映射表把它替换成 §4 M2 标定协议 + §5，实际没有交付：

- 经典/最近邻 selector 的可复现 baseline 数字和 tolerance；
- 当前 selector 的小规模 pilot 复现计划；
- data/code/env/seeds/reproduce/run-ID manifest；
- baseline reproduction 失败时的停止规则；
- independent rerunner identity 与 tolerance。

Stage-1 旧数字可以是动机，但不能代替 fresh Stage-2 instance 的 baseline reproduction contract。

### M-D3：`stage=2`、`Mode=confirmatory` 与证据等级帽冲突

草稿尚未过 Stage-2 gate，却在 frontmatter 写 `stage: 2-solution-validation`；同时说不作 strong confirmatory，
又在 §2 写 `Mode: confirmatory`、M4“确证开火”。建议改为：

```yaml
current_stage: PRE_STAGE2_ENTRY_DRAFT
internal_analysis_mode_after_freeze: protocol_confirmatory_within_public_benchmark
external_evidence_grade: development_controlled_benchmark
strong_confirmatory_claim: prohibited
```

否则“confirmatory”会再次被管理层或摘要读者当成强证据等级。

### M-D4：`N* 在任何方向性结果前预注册` 与 P-gen 后才填值矛盾

FG-7 说 N* 由 P-gen 方差 + 成本锚决定；P-gen 本身会观察 calibration data 的 generation/U 结构。
因此能预注册的是 **N* 的映射规则**，不是事先未知的 N* 数值。应改为：

```text
Nstar_selection_rule frozen before M2
Nstar_value instantiated once from P-gen calibration
Nstar frozen before any selector-effect comparison
```

不要继续写“数值在任何方向性结果之前已定”。

### M-D5：P-corr 与 P-sim branch 仍不是确定性算法

P-corr 写“剔除或换独立族 verifier”，这是两个动作，不是 branch rule；P-sim 写 Type-I 合格且 coverage 最优，
但没有规定：无方法达标怎么办、coverage 差异容忍度、power 最低线、Monte-Carlo error、DGP weighting。

必须把每个 branch 写成输入→唯一输出的纯函数，并用 synthetic table 单测所有边界。

### M-D6：任务族与 group/endpoint 仍过于含糊

- HeySQuAD 的开放共享语料/合法知识对象历史上尚未闭合，不能只列作候选；
- SQuTR/FiQA 的 endpoint 被写成“检索-QA 正确率”，需区分 retrieval metric 与 downstream QA utility；
- `query-topic×speaker` 的 topic 如何定义、是否使用 qrels/labels、是否在 split 前冻结尚不清楚；
- ASR speaker-level group 与 QA source-doc/speaker group 的目标总体不同，power 与 bootstrap 不能共享一句模板。

每个 task family 需要独立 data card：sampling unit、group key provenance、U、missingness、corpus axis、SESOI、
confirmatory population 与排除规则。

### M-D7：最强 baseline 的训练历史与“training-free”比较公平性未定义

NoRefER/LTR 类 baseline 可能在外部数据上训练，READ/MBR 可在推理时直接使用。项目不能因为自己强调“不改
权重”就排除强训练型 frozen baseline；部署时它们同样可以冻结使用。应分别报告：

- inference-time weight update = none；
- external component pretrained/fine-tuned history；
- per-item compute、额外模型参数、延迟与能耗；
- same K-pool 与 same information boundary。

公平比较是“部署时同信息/同预算”与“训练历史透明”，不是只允许与自己同哲学的方法参赛。

### M-D8：独立复现不能只放在 on-accept 收尾

模板要求 baseline/method result 的独立 clean-checkout rerun。P0 的诚信审计也仍 OPEN。独立性应分三层：

1. **设计审查独立性**：冻结前 reviewer 不参与赢家选择；
2. **实现复现独立性**：M2/M4 工件由不同人员/独立 agent 从 clean checkout 重跑；
3. **证据等级独立性**：若坚持 public deterministic 路线，可不主张 blinded strong-confirmatory，但必须保留
   其等级帽。

“不做强确证”不能变成“不需要独立复现/完整性审计”。

---

## 8. 新增文献 survey：A-SEL 的真实最近邻

### 8.1 经典 N-best / MBR 不是背景噪声，而是方法祖先

- [Stolcke, König & Weintraub 1997](https://www.isca-archive.org/eurospeech_1997/stolcke97_eurospeech.html)
  已在 N-best 上近似后验并选择最小期望 word error 的 hypothesis。含义：pool 内选择和 oracle headroom 不是新范式。
- [Goel, Kumar & Byrne 2000](https://www.isca-archive.org/icslp_2000/goel00_icslp.html)
  把 N-best ROVER/voting 放入 segmental MBR。含义：MBR 必须是载重基线，不是次级附录。
- [Wu, Chen & Gandhe 2022](https://www.isca-archive.org/interspeech_2022/wu22_interspeech.html)
  用整个 N-best、BERT confidence 与 learning-to-rank 做 ASR rescoring。含义：完整候选池信息与 confidence ranking
  已有直接先例。

### 8.2 Reference-free quality estimation 已直接覆盖“label-free reward”核心

- [NoRefER, Interspeech 2023](https://www.isca-archive.org/interspeech_2023/yuksel23_interspeech.html)
  明确做 referenceless ASR quality/ranking。含义：任何 label-free proxy 都必须与可复现 QE metric 对照。
- [HypR, Interspeech 2024](https://www.isca-archive.org/interspeech_2024/wang24j_interspeech.html)
  给出跨 AISHELL/TED-LIUM/LibriSpeech 的 50-hypothesis benchmark，并比较 reranking/revision。含义：团队可以
  先在 HypR 型固定候选基准复现最近邻，再声称 omni 自采样的新增价值。
- [READ 2026](https://arxiv.org/abs/2606.04680)
  无额外训练、直接从语音与文本 hypothesis 的 acoustic discrepancy 做 reference-free evaluation/refinement。
  它是当前 ASR 分支最危险的未列强基线；若不比较，A-SEL 新颖性无法成立。

### 8.3 LLM hypothesis selection/rescoring 已经存在

- [ProGRes 2024](https://arxiv.org/abs/2409.00217)
  用 instruction-tuned LLM 扩展 N-best，并结合 confidence/LLM sequence scoring 重排。含义：prompt + LLM score
  + candidate selection 不是空白。
- [Li & Niehues, Interspeech 2025](https://www.isca-archive.org/interspeech_2025/li25ca_interspeech.html)
  直接研究 LLM-based ASR hypothesis selection，比较 instruction/probability/acoustic 方案。含义：当前 proposal
  的“语音 MLLM 无先例”至少需要被严格收窄，而不能直接陈述。

### 8.4 通用 BoN / Goodhart 文献仍然必要，但不是唯一最近邻

- [Gao et al. 2023](https://proceedings.mlr.press/v202/gao23h.html)、
  [Huang et al. 2025](https://arxiv.org/abs/2503.21878)、
  [Khalaf et al. 2025](https://proceedings.neurips.cc/paper_files/paper/2025/file/590a0cc0306c1c63e2d66a51a407718f-Paper-Conference.pdf)
  支持 N*/pessimism/过优化负控；但它们不能替代 speech-domain 的 MBR/QE/reranking baseline survey。

### 8.5 设计与诚信规范仍然约束这轮

- [Nosek et al. 2018](https://pmc.ncbi.nlm.nih.gov/articles/PMC5856500/) 与
  [Dwork et al. 2015](https://pubmed.ncbi.nlm.nih.gov/26250683/) 支持 prediction/postdiction 与适应性数据边界；
- [Cawley & Talbot 2010](https://www.jmlr.org/papers/v11/cawley10a.html) 支持把完整 selector 搜索家族视为
  model-selection bias 的来源；
- [ICH E9(R1)](https://www.ema.europa.eu/en/documents/scientific-guideline/ich-e9-r1-addendum-estimands-and-sensitivity-analysis-clinical-trials-guideline-statistical-principles-clinical-trials-step-5_en.pdf)
  支持 claim/design/estimand/interpretation 同对象；
- [Lakens et al. 2018](https://journals.sagepub.com/doi/10.1177/2515245918770963) 支持 SESOI 的具体外部理由，
  不能用一个无量纲阈值跨任务偷渡；
- [ORI 定义](https://ori.hhs.gov/definition-research-misconduct) 与
  [NASEM](https://www.nationalacademies.org/read/21896/chapter/4) 支持把 FFP 与 detrimental practices 分开判断。

本轮新 survey 的关键改变不是“再加八篇引用”，而是改变 A-SEL 的 scientific burden：**团队不再只需证明
selector 比随机好，而需证明它相对几十年 N-best/MBR/QE 与最新 READ/LLM rescoring 有明确、可测、载重的 delta。**

---

## 9. 建议团队执行的研究 proposals

### Proposal R：Response Artifact Schema Repair

目标：先让 reviewer response 成为真正机器可读的证据对象。

```yaml
response_schema_v1:
  responds_to:
    reviewer_report_path: required
    reviewer_report_sha256: full_64_hex
    reviewed_evidence_snapshot_commit: full_40_hex
    reviewed_object_sha256: full_64_hex
  response_commit:
    recorded_by_post_commit_receipt: true
  response_items:
    type: list
    required_ids: [F-S1,F-S2,F-S3,F-S4,F-S5,F-S6,F-S7,M-S1,M-S2,M-S3,M-S4,M-S5,M-S6]
    unique: true
    exact_count: 13
  checker:
    fail_on_duplicate_yaml_key: true
    fail_on_missing_or_extra_id: true
```

### Proposal N：ASEL Novelty Kill Test

在继续填写统计细节前，先做一个**不跑新研究结果**的最近邻复现/设计挑战：

1. 在既有公开 N-best 工件上复现 MBR、NoRefER/可替代开源 QE、ProGRes 可行变体、READ；
2. 固定同一候选池、同一可见信息、同一调用预算；
3. 列 selector family 的参数量、外部训练史、运行时成本；
4. 预先定义 `delta_novelty`；
5. 如果团队方法不能超过 strongest reproducible baseline，A-SEL 降为 benchmark/negative-result study；
6. 如果团队方法仅因使用额外模型或额外信息胜出，必须改成预算/信息不匹配部署研究，不能称纯选择算法优势。

### Proposal O：冻结一个真正的 Operator Object

新增一份 `selector_object.yaml`：

```yaml
selector_object:
  inputs_allowed: []
  proxy_features: []
  scoring_formula: null
  tie_rule: null
  abstention_rule: null
  K_grid: []
  Nstar_rule: null
  prompt_set_hash: null
  embedder_set_hash: null
  verifier_families: []
  search_algorithm: null
  search_budget: null
  shared_across_tasks: null
  task_specific_fields: []
  winner_transfer_to_replication_family: null
  code_entrypoint: null
  lean_object_if_theory_retained: null
```

任何 null 在 v1.0 前必须填实或删除对应自由度。

### Proposal E：Dual-rho Estimand Audit

用 synthetic pools 做一个无数据争议的单元研究：

- 构造 greedy、pool-mean、oracle 不同的池；
- 比较 `rho_greedy` 与 `rho_pool`；
- 比较 ratio-of-expectations 与 expectation-of-ratios；
- 构造分母趋零、负增益、oracle ties、全候选相同、heavy-tail group；
- 明确每个估计量在哪些边界可解释；
- owner 只选一个 primary，其他均改名 secondary。

### Proposal X：Cross-task Replication Contract

把“跨任务复现”拆成三个预先互斥等级：

| 等级 | 定义 | 可支持的主张 |
|---|---|---|
| X1 strict transfer | 同一 selector/权重/阈值零再调参迁移第二任务族 | 可复用 operator 的强证据 |
| X2 family transfer | 同一 feature/operator family，按预冻小范围在 replication dev 重标定 | 可复用 recipe 的中等证据 |
| X3 independent retuning | 第二任务重新全搜索 | 两个 case studies，不是 operator replication |

H2 必须选择 X1 或 X2；X3 不得叫 co-primary replication。

### Proposal I：Independent Integrity Completion

继续执行上一轮 IA-1..IA-8，特别是：

- 尝试完整性与 config-selection trajectory；
- 所有正效应从 per-item 输出重算；
- cache/seed 独立性；
- group-level cross-split intersection；
- reviewer 抽样 seed 与脚本 hash 先登记；
- 允许 `NO_EVIDENCE_OF_FFP / INCONCLUSIVE / REFER_FOR_FORMAL_INQUIRY` 三结局。

---

## 10. 分阶段改进计划

### P0-R：先修 v6 记录，不跑实验

1. 更正 reviewer report SHA 与 response/evidence snapshot 字段；
2. 将 13 项改成 `response_items` list；
3. 增加 duplicate-key + exact-ID-set checker；
4. 将 canonical Thesis/Per-Work-Status 同步为“A-SEL selected, Stage-2 draft not passed, M2 frozen”；
5. 下一 release manifest 重新生成，因为当前 HEAD 已新增草稿提交 `84c6cf6`，不得继续把 13b5a10 叫当前 HEAD。

### P0-N：A-SEL Stage-1 identity 再关闭

1. 加入 Stolcke/Goel/Wu/NoRefER/HypR/ProGRes/Li/READ 最近邻；
2. 明确贡献类型：new method / new proxy / measurement protocol / benchmark，四选一 primary；
3. 把 strongest baseline 置入 primary kill gate；
4. 决定 one-shot reranking 是否仍在对外标题使用 RL；
5. owner 重新签 scientific delta，而不是只签 A-SEL 三个字母。

### P0-S：fresh Stage-2 v1.0 结构冻结

1. 修正 ρ 身份；
2. 增加 selector object freeze gate；
3. 定义 cross-task replication level；
4. 使用 family-specific SESOI 或共同 normalized utility；
5. 补齐 Template §4 baseline reproduction/method pilot/repro manifest；
6. 明确假设方向、CI、Holm、equality；
7. 把 P-corr/P-sim/N* branch 写成确定性算法；
8. 每个 task family 单独 data/estimand/group card；
9. reviewer 对 v1.0 重新审，而非把本报告当自动许可。

### P0-E：工程与诚信门

1. group-union exclusion + 同组不同 item 负例测试；
2. corpus upstream second clean fetch + 代码轴语义收紧；
3. config history 重建；不可回溯项列 UNKNOWN 并冻结污染范围；
4. independent audit plan 冻结；
5. 所有门完成前，不运行 P-gen/P-corr/P-sim/P-q2q/P-power 以外的任何数据敏感动作；实际上这些 pilot
   也只有在 v1.0 branch rules 签字后才能执行。

### P1：只在全部前门闭合后解冻 M2

M2 仅执行预列 calibration branch；任何新增 selector feature、prompt、verifier、K、task family 或 endpoint
都创建新 proposal version，在看相应 calibration 结果前审批。不得边看结果边把搜索空间补到 registry。

---

## 11. 重新申请结构验证与 scoped sign-off 的必要条件

```yaml
reapply_v6_record_acceptance_if_and_only_if:
  - reviewer_report_and_reviewed_object_hashes_are_separate_and_correct
  - response_commit_is_not_mislabeled_as_its_parent
  - all_13_response_items_parse_without_duplicate_keys
  - exact_finding_id_set_checker_passes

reapply_ASEL_structure_verification_if_and_only_if:
  - closest_neighbor_table_includes_classic_MBR_QE_LLM_rescoring_and_READ
  - novelty_delta_selects_one_contribution_type
  - strongest_reproducible_selector_is_in_primary_kill_gate
  - rho_greedy_and_rho_pool_are_distinct_and_one_is_owner_selected_primary
  - selector_object_and_search_space_are_frozen_before_M2
  - cross_task_replication_level_is_explicit
  - SESOI_is_family_specific_or_common_utility_is_justified
  - hypothesis_CI_Holm_and_equality_rules_are_executable
  - template_section4_baseline_reproduction_contract_is_present
  - stage_and_evidence_grade_labels_do_not_conflict
  - deterministic_branch_rules_exist_for_Pcorr_Psim_Nstar
  - per_family_data_estimand_group_cards_exist

M2_unfreeze_if_and_only_if:
  - all_P0B_engineering_gates_closed
  - config_history_complete_or_UNKNOWNs_frozen_and_scoped
  - independent_audit_plan_frozen
  - fresh_stage2_v1_0_committed_clean_and_reviewer_signed
  - release_manifest_rebuilt_for_that_exact_snapshot
```

---

## 12. 学术欺诈/作假嫌疑的更新裁决

### 12.1 Fabrication

**未建立。** fresh tests、checker、manifest hashes 都能复核；未发现不存在的样本或虚构实验结果。

### 12.2 Falsification

**未建立。** v6 的两项 snapshot 错误使研究记录不精确，但它们没有改变科学结果、方向或 gate；当前更符合
手工 provenance 管理失效。团队主动登记 `c7528fe` 的错误提交信息，是反对“持续故意掩盖”的证据。

升级条件包括：

- 明知 reviewer report hash/response commit 错误仍用于对外证明独立签署；
- 在 M2 冻结期间发现未登记的 selector/data-sensitive runs；
- 将 READ/MBR/QE 等直接最近邻从论文中有选择地删除，以维持“无先例”主张；
- 把不如 strongest baseline 的结果只与 random 比较后宣称方法成功；
- 在 `rho_greedy` 与 `rho_pool` 间按结果切换而不披露。

### 12.3 Plagiarism

本轮未做全文相似性审计，未见新信号。遗漏引用首先是 novelty/survey 缺陷，不自动等于 plagiarism；但收到
本报告后，最近邻文献必须进入 citation registry。

### 12.4 QRP 风险

仍评为 **HIGH UNTIL P0 CLOSES**，但要记录改善：

- 改善：接受负面事实、主动登记错误、保持 P0 NOT_PASS、未申请立即签署、草稿不授权实验；
- 残余：配置轨迹缺失、provenance 再次写错、强 baseline 降 secondary、指标同名漂移、novelty survey 漏掉
  直接祖先、独立审计未完成。

准确口径是：

```text
NO_EVIDENCE_ESTABLISHING_FFP
NOT_CLEARED_OF_ALL_INTEGRITY_CONCERNS
DISCLOSURE_BEHAVIOR_IMPROVED
METHOD_AND_RECORD_GOVERNANCE_STILL_NOT_READY_FOR_STAGE2
```

---

## 13. 供团队 AI 直接消费的机读裁决

```yaml
review_decision:
  id: V6-RESPONSE-AND-ASEL-DRAFT-ADR-2026-07-13
  response_v6:
    substance: MOSTLY_CORRECT
    p0a_transaction: VERIFIED_CLOSED_FOR_DESIGNATED_SNAPSHOT
    record_acceptance: CORRECTIONS_REQUIRED
    new_findings:
      - R6_M1_wrong_reviewer_report_hash
      - R6_M2_response_snapshot_points_to_parent_commit
      - R6_M3_duplicate_yaml_keys_destroy_13_item_machine_readability
      - R6_M4_canonical_status_not_synced
  stage2_draft:
    observed_sha256: 300ccfb24006b2b49aeafbc16db7fecede5ccd2b766d58339bca5f3c75abeefa
    git_commit: 84c6cf64d0a979a5d4f8222a00b9eb746378f270
    status: DRAFT_NOT_FROZEN_COMMITTED_DURING_REVIEW_WITH_UNCHANGED_BYTES
    structure_verification: REFUSED
    fundamental_findings:
      - FD1_novelty_survey_omits_direct_ASR_selector_ancestors
      - FD2_pool_mean_primary_but_strongest_baselines_secondary
      - FD3_rho_anchor_and_aggregation_identity_drift
      - FD4_selector_object_and_search_family_not_frozen
      - FD5_cross_task_utility_and_replication_object_incoherent
    major_findings:
      - MD1_hypothesis_CI_sidedness_and_Holm_inconsistent
      - MD2_template_section4_not_instantiated
      - MD3_stage_confirmatory_and_evidence_grade_labels_conflict
      - MD4_Nstar_timing_statement_false_as_written
      - MD5_calibration_branch_rules_not_deterministic
      - MD6_task_family_group_and_endpoint_cards_incomplete
      - MD7_strong_baseline_training_history_and_budget_fairness_undefined
      - MD8_independent_reproduction_deferred_too_late
  gating:
    M2_unfreeze: PROHIBITED
    fresh_stage2_v1_freeze: PROHIBITED_UNTIL_FINDINGS_CLOSE
    immediate_scoped_signoff: NOT_REQUESTED_AND_NOT_GRANTED
  integrity:
    fabrication: NOT_ESTABLISHED
    falsification: NOT_ESTABLISHED
    plagiarism: NOT_ASSESSED_NO_SIGNAL
    qrp_risk: HIGH_UNTIL_P0_CLOSES
    independent_audit: REQUIRED
  verified_positive_evidence:
    release_manifest_designated_snapshot: PASS
    manifest_key_hashes: 7_OF_7_MATCH
    stored_checker_final_proposal_hash: MATCH
    fresh_checker: 22_OF_22_PASS
    fresh_w1_tests: 159_PASS_3_WARNINGS_0_FAIL
    no_visible_post_freeze_w1_repro_mtime_signal: true_limited_scope
  allowed_next_actions:
    - response_metadata_and_yaml_schema_correction
    - literature_survey_and_novelty_reconstruction
    - proposal_only_design_revision
    - synthetic_estimand_and_branch_rule_tests
    - P0B_group_corpus_config_engineering
    - read_only_independent_integrity_audit
  blocked_next_actions:
    - any_new_selector_effect_search
    - any_real_split_draw_before_group_union_fix
    - any_corpus_PASS_before_upstream_anchor
    - any_claim_that_ASEL_is_novel_RL_without_direct_reranking_comparison
    - any_M2_or_M4_execution
```

---

## 14. 给团队下一轮回复的强制格式

请不要只回复“全部接受、会在 v1.0 修”。下一轮交付两个独立对象：

1. **Response v6 correction receipt**：列旧值、新值、commit、parser test 输出；
2. **ASEL v0.2 structural response**：逐项回答 F-D1..F-D5、M-D1..M-D8。

机读格式必须是列表：

```yaml
response_items:
  - finding_id: F-D1
    disposition: ACCEPT|PARTIAL|REJECT_WITH_EVIDENCE
    exact_change: null
    evidence_files: []
    evidence_commit: null
    machine_check: null
    status_after: OPEN|PARTIAL|CLOSED
    data_sensitive_work_authorized: false
```

任何 `CLOSED` 必须包含当前已存在的 commit/file/check 输出；未来承诺只能标 OPEN。下一轮如果只修文字而不把
strong comparator、ρ、selector object 与 cross-task estimand 放进 load-bearing gate，结构验证仍将退回。

**最终决定：v6 的接受姿态与 P0-A 事务予以认可；v6 记录需更正；A-SEL v0.1 结构验证拒绝；M2 继续冻结。**
