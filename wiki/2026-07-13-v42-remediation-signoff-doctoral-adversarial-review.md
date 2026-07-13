---
review_id: V42-REMEDIATION-SIGNOFF-ADR-2026-07-13
date: 2026-07-13
timezone: Asia/Singapore
stage: Stage-1 problem-definition / remediation-signoff audit
reviewed_object: wiki/2026-07-13-remediation-report-v42-for-reviewer-signoff.md
reviewed_object_git_commit: c7528fe05f9d44bfb1d377d2939a6fd206eb6926
reviewed_object_sha256: cd987ff0fc2b0f81e5576a7a6586f4d093f263555f06a31b9fdd2f50e5a431cd
reviewer_roles:
  - strict_external_reviewer
  - doctoral_supervisor
  - research_integrity_red_team
  - reproducibility_auditor
decision: RETURN_WITH_RESIDUAL_FINDINGS
scoped_signoff: REFUSED
scientific_readiness: NO_GO_FOR_M2_UNFREEZE_OR_M3_CONFIRMATORY_REGISTRATION
integrity_verdict:
  fabrication: NOT_ESTABLISHED
  falsification: NOT_ESTABLISHED
  plagiarism: NOT_ASSESSED_NO_SIGNAL_FOUND
  qrp_risk: HIGH
  misleading_governance_risk: HIGH
  independent_integrity_audit: REQUIRED_NOT_OPTIONAL
confidence: HIGH_ON_REPOSITORY_FACTS_MODERATE_HIGH_ON_METHOD_JUDGMENT
mutation_statement: 仅新增本日期审查报告；未修改整改报告、proposal、代码、测试、登记册或实验工件
---

# v4.2 整改签署审查：退回残余发现，不予 scoped sign-off

## 0. 终局意见先行

**结论：退回，不签字。**

本轮不能在整改报告所提供的方框——“整改忠实 + 全部待决项正确挂门”——上盖章。原因不是团队的所有
工作都不真实，也不是我发现了已经成立的数据捏造。恰恰相反，我独立复核确认了若干重要正面事实：

- 整改报告附录列出的 23 个文件 SHA-256 与字节数全部匹配；
- 伞仓证据表所列 `016a789` 是当前报告提交 `c7528fe` 的直接父提交，W1 当前为 `ab1c680`；
- 在指定 WSL2 `Ubuntu-24.04`、Python 3.12 venv 中，W1 标准入口 fresh rerun 为
  **159 passed / 3 warnings / 0 failed / 0 errors**；
- 对最终 proposal 只读 fresh rerun 的 conformance checker 确实仍为 **22/22 PASS**；
- 用正确的根仓路径核验真实 FiQA 本地快照，`corpus_lock.py --verify` 确实得到 57,638 docs、三组哈希匹配；
- F-7 的合法答案 scrub 反转已经在代码契约与正负 golden test 中被纠正；
- F-8 的“缺 group manifest 硬失败、confirmatory 禁 `force_supersede`、曝光清单全路径覆盖”三项局部修复真实存在；
- 报告明确承认 P0 为 NOT_PASS、FFP 未成立、QRP 高风险，这比伪装成全部闭合要诚实。

但是，签署请求不是“是否做了一些真实修复”，而是更强的合取命题：

> 所有声称已修的内容均有与最终发布对象一致的证据，且所有未修项都被放在不会污染后续推断的正确门前。

这个合取命题为假。至少存在 **7 个 FUNDAMENTAL、6 个 MAJOR** 残余，其中四个可直接否决 scoped sign-off：

1. **阶段门序倒置**：研究问题身份、主估计量、最强基线原子、跨集复现与生成方差被允许在 M2 数据/选择
   之后到 M3 再定；这不是“避免 Stage-1 过度预注册”，而是把载重设计自由度留到已经接触方案验证信息之后。
2. **最终发布快照不事务一致**：`release_manifest.json` 记录的是较早、dirty 的两仓状态，不是本整改包最终
   HEAD；它内部的多个关键工件哈希也已陈旧。因此 M-8 的“发布事务一致性已修复”不成立。
3. **提交的 checker JSON 不是对最终 proposal 的运行**：final proposal 的 SHA-256 为 `3f0ac5...`，而已提交
   `v42-conformance-output.json` 记录的输入是 `182f09...`。fresh rerun 仍通过只能证明规则当前可通过，不能把陈旧
   JSON 称为最终发布证据。
4. **语料官方性仍由团队自锁提前标 PASS**：当前代码可在只有本地自算锁、没有上游公开 checksum 独立锚时把
   `query_independent_corpus` 标为 PASS；这与 proposal §6.4 自己规定的“自算 hash 只证 replayability，不能证
   officialness/query-independence”冲突。

所以本轮的准确裁决是：

```text
REMEDIATION_WORK_REAL_BUT_NOT_SIGNABLE
SCOPED_SIGNOFF = REFUSED
FFP = NOT_ESTABLISHED
QRP_RISK = HIGH
M2_UNFREEZE = STOP
NEXT_ACTION = CORRECT_GATES + REBUILD_FINAL_EVIDENCE_SNAPSHOT + INDEPENDENT_AUDIT
```

---

## 1. 审查范围、标准与限制

### 1.1 我审的是什么

本轮只审四类命题：

1. 整改报告引用的文件、提交、哈希、测试、登记册是否真实存在；
2. 声称 FIXED / ADDRESSED / DELIVERED 的事项是否真的达到该标签；
3. DEFERRED 项是否被挂在**任何数据敏感动作之前**的正确门；
4. 当前证据是否支持“存在学术欺诈”的指控，或只支持方法缺陷/有害研究实践风险。

本轮不替团队实现修复，不修改其 proposal、源代码、测试或登记册，也不替机构研究诚信办公室作正式裁决。

### 1.2 诚信术语标准

采用保守、可证据化的区分：

- **Fabrication**：编造并记录/报告不存在的数据或结果；
- **Falsification**：操纵研究材料、过程或省略/改变数据，使研究记录不能准确表示真实研究；
- **Plagiarism**：未经适当归属挪用他人思想、过程、结果或文字；
- **QRP / detrimental research practice**：未达到 FFP 的证据门槛，但足以损害研究可靠性的选择性报告、
  事后定规则、重复使用 holdout、夸大证据等级、不完整记录等。

ORI 明确把 FFP 与 honest error / difference of opinion 区分；NASEM 也把 FFP 之外、明确伤害研究过程的做法
单列为 detrimental research practices。因此，**严重方法错误不自动等于欺诈；但已被指出后继续用容易造成
错误印象的标签，也不能再当作普通排版瑕疵**。参见 [ORI 定义](https://ori.hhs.gov/definition-research-misconduct)
与 [NASEM《Fostering Integrity in Research》](https://www.nationalacademies.org/read/21896/chapter/4)。

### 1.3 证据边界

我没有声称完成以下工作：

- 对 574 个 `_repro` 工件逐一重算所有效应量；
- 访问不存在于仓库/磁盘上的已删除 notebook、未保存提示或人工会话；
- 证明 owner 或任何成员的主观故意；
- 证明 HF 上游快照从未变化或本地 `.hfd` 元数据不可能被修改；
- 完成人员级、组织隔离的正式独立调查。

这些限制正是为什么结论是 **FFP_NOT_ESTABLISHED + INDEPENDENT_AUDIT_REQUIRED**，而不是“已证明造假”或
“已证明完全清白”。

---

## 2. 可复核事实：我方 fresh rerun 与证据对账

### 2.1 仓库状态

| 证据 ID | 核验对象 | fresh 结果 | 审查含义 |
|---|---|---|---|
| E-01 | 伞仓当前 HEAD | `c7528fe05f9d44bfb1d377d2939a6fd206eb6926`，工作树核验时 clean，已跟踪远端同名分支 | 报告最终版本有 Git 祖先链 |
| E-02 | W1 当前 HEAD | `ab1c68017671f37b302ba4b27d69859d32b42c62`，工作树核验时 clean，`master` 跟踪 `origin/master` | W1 整改代码已提交并推送 |
| E-03 | 证据表祖先关系 | 伞仓 `016a789` 是 `c7528fe` 的直接父提交；W1 表列 HEAD 与当前一致 | 报告附录的“直接后继”陈述成立 |
| E-04 | 附录 23 个文件 | 每行 SHA-256 与 bytes 均匹配 | 附录本身不是伪造清单 |

### 2.2 代码与机械检查

| 证据 ID | 命令/对象 | fresh 结果 | 能证明 | 不能证明 |
|---|---|---|---|---|
| E-05 | W1 `PYTHONPATH=src pytest -q` | 159 passed，3 warnings，111.71s，return code 0 | 当前代码满足现有测试契约 | 科学主张有效、测试覆盖完整、无数据选择偏差 |
| E-06 | 最终 proposal 上只读运行 `v42_conformance.py` | 22/22 PASS | 最终文档仍满足这 22 条规则 | 已提交 JSON 是最终运行、科学自洽、理论/统计成立 |
| E-07 | `corpus_lock.py --verify` 对真实 FiQA | verified=true，57,638 docs，IDs/content/archive member hash 匹配 | 当前本地语料字节与自锁文件一致 | 该锁的源头一定是官方上游、query-independence 已由第三方锚证成 |
| E-08 | 报告给出的 `../../../docs/corpus.lock.json` CLI 示例 | 从 W1 根运行会找错目录并失败；正确相对路径是 `../../docs/corpus.lock.json`，默认函数路径本身正确 | 文档核验配方有一处真实路径错误 | 不推翻默认代码路径或真实锁内容 |

### 2.3 两个不能忽略的发布快照不一致

#### E-09：release manifest 不是最终发布快照

`docs/integrity/release_manifest.json` 当前记录：

- umbrella SHA = `56364eb...`，`dirty=true`；
- W1 SHA = `159b525...`，`dirty=true`；
- key artifact hash 中 prior exposure = `dc76ca...`，而最终文件为 `7d1a33...`；
- experiment attempts = `22a05a...`，而最终文件为 `7ea5ef...`；
- discrepancy register = `90da3d...`，而最终文件为 `504404...`。

这不是一个“字段小差异”。整改报告把 M-8 判为 **FIXED（机制）**，并说 release manifest 通过 live SHA、dirty、
pytest、checker “机械防止快照失真”。实际情况是：脚本确实能采集 live 状态，但最终发布时没有重新生成。一个
没有被发布流程强制执行的脚本，不能关闭“发布快照与实际仓库脱节”的 finding。

正确标签应为：

```yaml
M-8:
  current_status: PARTIAL
  mechanism_exists: true
  final_release_transaction_executed: false
  gate: before_any_signoff_or_release
```

#### E-10：提交的 conformance JSON 对应旧 proposal

最终 proposal 实际 SHA-256：

```text
3f0ac5b6e5c5e021ffc9b85c10f7b8b9f07a4bd6395de6350bcd8c87e1ba18e0
```

但 `docs/checks/v42-conformance-output.json` 的 `meta.inputs` 记录 proposal SHA-256：

```text
182f093aeafe635fab864a2939e9566d3d4ea18d2779fb82a14f710f8aad4260
```

我 fresh rerun 后最终 proposal 仍为 22/22 PASS，这说明**结果可复现**；但仓库提交的 JSON 不是这个 fresh run，
所以报告中“live JSON 已针对 final proposal 生成”的证据指针仍然不真实。应把“可复跑通过”与“已提交最终运行
证据”分开写，不能用前者洗掉后者的事务缺陷。

### 2.4 登记册内部仍有陈旧叙事

`prior_exposure_registry.json` 已正确把 P0 标为 NOT_PASS，并列出未持久化配置轨迹、自由提示、仓库外运行与
未来 draw registry 对账等待办；这是诚实的。

但 `discrepancy_register.md` 的 “Open items” 仍说 prompt/metric enumeration outstanding、erratum 不在盘，
而这些后来已经落地。追加区只修正了 12/12 vs 22/22 的陈旧叙事，没有对这些 open items 逐条追加“resolved at
commit X”。因此登记册不是假的，但也不能称为当前状态的一致视图。

---

## 3. 多轮对抗式评审记录

### Round 1：最大善意解释——团队是否只是谨慎地把未来工作延后？

最有利于团队的解释是：

- 当前严格处于 Stage 1，只需要定义问题，不应把 proposal 打磨成临床试验级 SAP；
- 报告没有把 P0 写成 PASS，也没有宣称已经获得 confirmatory result；
- 多数残余都具名进入缺口表，未来 M3 开火前再冻结即可；
- 工程测试与哈希能复现，说明团队不是凭空造一个整改包；
- F-7 被判 latent 有真实数据流依据，不能把潜伏 bug 夸大成已经污染数据；
- owner 有权在研究资源约束下拒绝过重 custody 仪式。

**Round 1 结论：上述辩护部分成立。** 它足以排除“看到几个错误就直接认定数据造假”的草率结论，也支持把
F-7 从“现行数据受损”收窄为“潜伏设计缺陷，现已修复”。

### Round 2：方法学红队——延后是否真的发生在正确的数据边界之前？

答案是否定的。项目自己的 `AGENTS.md` 明确规定：

- Stage 1 结束于 owner 讨论并选择**具体研究问题**；
- Stage 2 方案验证必须新建一份 **fresh Research-Proposal-Template**；
- Stage 2 才使用大样本、冻结标准与完整 controls；
- Stage-1 小样方向性结果不能自动升级。

而整改包/续29 的安排是：保留当前 v4.2，不出 fresh v4.3，把 estimand、原子、generation resampling、
comparator 等到 M3 再定；同时 M2 已承担 dataset eligibility、embedder 选择、selector 权重/阈值标定、误差
相关测量、推断模拟与 q2q 审计。

这形成一个不可接受的时间序列：

```text
M2 看见 eligibility / selector / embedder / correlation / simulation 信息
    ↓
M3 再决定 primary estimand / primary atom / strongest baseline / generation seeds / comparator
    ↓
M4 开火
```

“在 M4 结果之前定”只排除了最粗糙的结果后改规则，并没有排除**利用 M2 的效应、方差、可行性和赢家信息来
设计最容易成功的 M3 确证问题**。Dwork 等关于 adaptive data analysis 的结论正是：分析/假设随前次数据反馈
自适应时，传统 holdout 解释会失效；Cawley & Talbot 也说明优化有限样本上的 model-selection criterion 会产生
selection bias，其量级可与算法差异相当。参见
[Reusable Holdout](https://pubmed.ncbi.nlm.nih.gov/26250683/) 与
[Cawley & Talbot 2010](https://www.jmlr.org/papers/v11/cawley10a.html)。

**Round 2 结论：核心待决项挂错门。** Stage 1 不需要填所有数值，但必须决定“究竟研究什么、什么比较承载新颖性、
什么估计量对应头条”。进入 Stage 2 前必须用 fresh proposal 冻结；不能用“避免过度预注册”作为保留关键自由度
到 M3 的理由。

### Round 3：工程/证据红队——绿色测试和哈希能否支撑“整改忠实”？

结论是部分能、部分不能：

- 能：代码测试、附录文件哈希、真实本地 corpus lock、F-7/F-8 局部代码门均是真实的；
- 不能：最终 release manifest 与 checker output 都不是最终对象的发布事务；
- 不能：conformance 规则多为 phrase/file-existence 规则，`H_RDU_VS_STRONGEST` 出现四次只证明“被写到了”，
  不证明它成为 load-bearing atom；
- 不能：`query_independent_corpus` 的当前 PASS 来自团队自锁，无法证明官方性；
- 不能：159 passed 不检查所有研究选择、被删会话、未保存配置、M2/M3 时间边界或人员独立性。

**Round 3 结论：机械证据是真证据，但证据等级被错误外推。** 报告的 scope disclaimer 是必要的，却不能抵消正文
里 `FIXED*`、`live`、`独立性未取消` 等更强陈述。

### Round 4：诚信红队——这些不一致是否已经构成 falsification？

支持“可能接近 falsification 风险”的事实：

- 已被审查明确指出的快照问题在“修复机制”后仍复发；
- self-pinned corpus 在未有第三方锚时仍可得到语义强烈的 PASS；
- 报告把“外审盖章 + 机器登记册”称为独立性的制度替代，但同一报告又承认它不是 independent oversight；
- P0 缺完整配置轨迹，不能排除 winner-only 保存；
- 大量关键设计自由度被允许留到 M2 信息可见后；
- `FIXED*` 视觉标签容易让管理层只看索引表时高估闭合度。

反对现在就认定 falsification 的事实：

- 报告公开列出 P0 NOT_PASS、M-6 不可完全回溯、多个 DEFERRED/CONTESTED；
- 目前没有 confirmatory result 被报告；
- 159 测试与文件哈希可独立重现；
- 没有发现凭空生成的样本结果或人为改数的直接证据；
- release/checker 快照错误可由发布顺序失控解释，不足以单独证明故意或 reckless disregard；
- 真实本地语料确实与自锁一致，问题在“来源证明等级”，不是内容哈希造假。

**Round 4 结论：FFP 仍未成立，但 QRP 与误导性治理风险高。** 若团队在收到本报告后仍把本轮称为“全部已识别
问题修完/独立审计完成/M1 高质量锁定”，或据此放行 M2，再在论文里省略这些边界，届时会显著增加“明知记录不
准确仍对外表示”的 falsification 风险。

### Round 5：反向审稿——即使只签极窄范围，能否签？

不能。团队请求的 scoped sign-off 明确包含“全部待决项被正确挂门”。即便完全不判断科学有效性，E-09/E-10
已足以证明最终证据事务不闭合；F-S1/F-S4/F-S5 则证明挂门不正确。签字后再在脚注里说“非科学通过”不能修复
签字合取命题本身为假的问题。

---

## 4. FUNDAMENTAL 残余发现

### F-S1：Stage 1 → Stage 2 → M3 的顺序被实质倒置

**严重度：FUNDAMENTAL / STOP-THE-LINE**

**问题。** 整改报告 §4 把 F-1/F-4/F-5/M-3/M-4/M-7 等 SAP 编辑回退，并称所有 estimand/新增原子在
M3 冻结；proposal §9 与附录 A 也明确“confirmatory-protocol DRAFT，M3 才生效”。与此同时，M2 要进行：

- eligibility 数据集筛选与 focus/rep 命名；
- embedder 选型与全语料构建；
- selector weights/K/threshold/prompt 探索；
- same-weight error correlation 测量；
- design-specific inference simulation；
- q2q overlap 审计；
- holdout supply/power 表。

这些都不是纯工程；它们会给出效应大小、方差、任务可行性、最佳组件与最有利比较的信息。允许之后再选择
primary atom/estimand/baseline 会打开明显的研究者自由度。

**为什么不是“Stage 1 不应预注册”的合理反驳。** Stage 1 的确不应假装已经有完整数值 SAP，但必须交付三样：

1. 唯一、具体的科学问题；
2. 能证伪该问题的 load-bearing comparison；
3. 与头条文字相同的 estimand 类型。

完整数值参数可以在 fresh Stage-2 proposal 中冻结；科学身份不能到 M2 之后再定。Nosek 等强调预注册的作用是
把 prediction 与 postdiction 区分；Registered Reports 的 Stage 1 review 发生在 outcomes 已知之前。参见
[Nosek et al. 2018](https://pmc.ncbi.nlm.nih.gov/articles/PMC5856500/) 与
[Chambers & Tzavella 2022](https://www.nature.com/articles/s41562-021-01193-7)。

**要求。** 立即把以下门统一改为 `BEFORE_STAGE2_UNFREEZE`：F-1、F-3、F-4 设计、F-5、F-8 跨组隔离、F-9、
M-1、M-2、M-3、M-6 搜索空间定义、M-7 overlap 规则/阈值。Stage 1 owner 只能选择研究问题；随后新建 fresh
Stage-2 proposal，不直接把 v4.2 在 M3 变成确证注册。

### F-S2：M-8 的最终发布事务没有执行，不能判 FIXED

**严重度：FUNDAMENTAL / EVIDENCE MISMATCH**

证据见 E-09。manifest 记录的两仓 SHA 与 dirty 状态都不是最终签署包，关键工件哈希也陈旧。整改报告的附录
哈希表本身是新的，但它没有替代 `release_manifest.json` 所承诺的发布事务，因为后者才是 M-8 的固定机制。

**要求。** 发布顺序必须机械化为：

```text
finalize all source artifacts
→ commit both repos
→ verify clean worktrees
→ run pytest + checker against exact final inputs
→ generate release manifest from those clean HEADs
→ commit only the manifest/report wrapper
→ verify manifest-recorded commits are ancestors and every recorded artifact hash still matches
```

任何 dirty=true 或输入 hash 漂移均应让 release gate FAIL，而不是只记录后继续签署。

### F-S3：提交 checker JSON 的输入不是 final proposal

**严重度：FUNDAMENTAL / EVIDENCE MISMATCH**

证据见 E-10。fresh rerun 22/22 是有利证据，但不能倒填到旧 JSON。报告附录已经知道 final proposal hash 是
`3f0ac5...`，却仍把输入为 `182f09...` 的 JSON 称为 live authority，这构成内部可复核矛盾。

**要求。** 重新运行并提交 output；output 的 proposal hash 必须等于报告附录与当前文件哈希。叙事版 12/12
应同次重建或明确移出发布证据集，而不是“下一发布周期”。

### F-S4：F-6 把 self-pinned replayability 错标为 upstream-anchored officialness

**严重度：FUNDAMENTAL / CORPUS PROVENANCE**

正面事实：`corpus.lock.json` 确实从真实本地 57,638-doc 快照生成，当前本地字节核验通过。

残余问题：

- `hf_revision_sha` 是硬编码值，来源说明为本地 `.hfd/repo_metadata.json`；`verify_corpus_lock` 不会重新向上游
  或受信任的下载 manifest 验证该 revision；
- `EXPECTED_DOC_COUNT=57638` 来自团队自己的 loader docstring/field verification，不是上游签名元数据；
- archive member hash 是团队第一次见到本地文件后计算的 self-pin；
- proposal §6.4 明确要求“上游第三方可验证 revision + 上游公开 checksum/doc_count”，并说自算 hash 单独
  不能证明 officialness/query-independence；
- 但 `kb_batch_build._corpus_lock_verification` 只要本地 docs 与 self-lock 匹配就 `verified=True`，随后
  `query_independent_corpus=PASS`。

所以当前系统证明的是：

```text
THIS_BUILD_MATCHES_THE_TEAM_PINNED_LOCAL_SNAPSHOT
```

并没有证明：

```text
THIS_IS_INDEPENDENTLY_VERIFIED_OFFICIAL_UPSTREAM_CORPUS
```

**要求。** 在第三方锚未闭合前，把轴改成 `SELF_PIN_MATCH / UPSTREAM_NOT_VERIFIED` 或
`NOT_EVALUATED`，绝不能 PASS。上游 revision 需通过下载 manifest/remote commit 复核；若上游无公开 member
checksum，就保存从该 revision 下载的完整 archive hash、下载日志、LFS pointer/OID 与第二人复算，不得把
“上游没有给 checksum”静默变成“团队自算值等价于上游 checksum”。

### F-S5：F-8 仍未证明跨 split 的 group-disjointness

**严重度：FUNDAMENTAL / DATA ISOLATION**

当前实现做对了：每次 draw 内按 group 整组抽；group manifest 必须覆盖 remaining items；confirmatory 排除
此前 manifest 的全部 **item IDs**。

但它没有做：把先前 draw 中 item 的 **group keys** 扩展为整组排除。代码先从 prior manifests 读取 IDs，
仅以 `iid not in excluded` 过滤；随后才对 remaining items 按 group 抽。如果 prior eligibility 有 speaker S 的
item A，confirmatory pool 仍有同 speaker S 的 item B，A 被 ID 排除，B 仍可被抽中。

测试 `test_disjointness_proof_correct_when_group_manifest_and_prior_draws_both_real` 也只断言 item-ID intersection
为零；而且 prior eligibility/dev 使用 identity group manifest，未构造“不同 item 同一 group 跨 split”负例。

因此报告的“跨 split group-disjoint proof 余项挂 P2/M2”虽然承认残余，但门挂错：**必须在任何真实 split draw
之前关闭**，不能在已经产生 eligibility/exploration draw 后再补。

**要求。** prior manifest 必须记录所用 group key 或可重放 group manifest；confirmatory exclusion 先取 prior
groups 的并集，再删除当前 pool 中属于这些 groups 的所有 items；新增最小反例测试 A/B 同 speaker、不同 ID、
跨 manifest，预期硬失败或 B 被整组排除。

### F-S6：“外审盖章 + 机器登记册”不能被定义成独立审计

**严重度：FUNDAMENTAL / GOVERNANCE**

整改报告 §6.3 说独立性以“外审盖章 + 机器可核登记册”落地，称这是制度形态差异而非取消独立性；但 §7 的
scope 声明又承认该报告不是 independent oversight，也不是 completed independent integrity audit。这两句不能
同时作为 P0 的闭合依据。

独立性至少需要：

- 审核者未参与生成被审对象、未参与阈值/赢家选择；
- 审核者读取冻结的只读原始工件，而不是只读团队自述；
- 复跑脚本与结果对账由审核者自己完成；
- 审核结论不能被 owner 以“形式太重”为由改写证据标准；
- 有冲突时保留 reviewer finding 与 owner exception 两条记录，不把 exception 写成方法学关闭。

本报告可以是外部审查意见，但不能因“有人在签字位写字”自动变成人员隔离的独立完整性审计。人员级独立评分
也不能保留为 M4 前“可选升级”；对于 public deterministic evaluation，它是高等级确证主张的必要条件之一。

### F-S7：P0 NOT_PASS 与“阶段高质量锁定”不能并存为放行信号

**严重度：FUNDAMENTAL / STOP-THE-LINE**

P0 未满足的不是装饰项，而是 load-bearing 的配置选择轨迹与独立快照。`manual_completion_todo` 还列出自由提示、
仓库外运行、未保存 sweep、draw registry 对账。只要这些缺口存在，无法证明 registry 包含“所有尝试”，也无法
排除只保存 winner 的选择性通道。

因此：

- 可以说“已创建并充实四册”；
- 可以说“P0 honest status = NOT_PASS”；
- 不可以把报告送达审查者自动视为独立快照条件完成；
- 不可以在 P0 NOT_PASS 时恢复任何会进一步产生选择性信息的 M2 搜索；
- 不可以在 Decision Log 用“全部已识别问题修复完、高质量锁定阶段性工作”概括当前状态。

---

## 5. MAJOR 残余发现

### M-S1：F-3 的证据等级不是 M3 前随意选择的标签

public deterministic evaluation 的问题不只是结果出来后才能不能改名。若 M2 持续用公开 IDs、公开种子、公开
benchmark 来选数据集、组件、prompt 与停止规则，那么到 M3 再说“我们把它叫 confirmatory 还是 exploratory”
已经无法恢复盲性。等级由信息流事实决定，不由 owner 签字选择。

**要求：** Stage-2 fresh proposal 开始前二选一：

1. public deterministic 路线：预先接受其为 development/controlled benchmark evidence，不做强 confirmatory；
2. strong-confirmatory 路线：独立保管的新数据/新版本、冻结后一次评分、人员隔离。

### M-S2：F-2 只修复了诚实命名，没有修复 SESOI 的独立依据

把 Q-B SESOI 改称 `post-observation but externally justified` 是必要诚实修复，应予肯定。但“等价检验传统 / MCID
传统”不是具体 external anchor。Lakens 等明确讨论了多种 SESOI 确定路径，并指出只依赖 benchmark 是最弱的理由。
当前没有：具体效用函数、外部研究效应分布、专家 elicitation 记录、量纲换算、为什么这个阈值对语音任务有最小
实质价值的推导。

因此 F-2 最多是：

```yaml
disclosure_fixed: true
substantive_threshold_justification: not_delivered
```

参见 [Lakens, Scheel & Isager 2018](https://journals.sagepub.com/doi/10.1177/2515245918770963)。

### M-S3：主 estimand 与固定绝对 margin 仍是不同问题

proposal 已诚实承认 anti-conservative 区域，但把真正相对 estimand 只作 sensitivity 仍然不能承载“≥10% 相对
错误率下降”的主张。ICH E9(R1) 的基本原则是 planning/design/conduct/analysis/interpretation 围绕同一个 estimand
对齐；不同问题的 supplementary analysis 不能证明主分析对原问题稳健。

建议直接定义：

```text
theta_rel = (E[error_bare] - E[error_system]) / E[error_bare]
```

在每个 paired group/bootstrap replicate 内联合重算分子与分母并注册 denominator floor；主判据对
`theta_rel > 0.10`。固定绝对 margin 可作为补充可解释性分析，不应反过来。

参见 [ICH E9(R1)](https://www.ema.europa.eu/en/documents/scientific-guideline/ich-e9-r1-addendum-estimands-and-sensitivity-analysis-clinical-trials-guideline-statistical-principles-clinical-trials-step-5_en.pdf)。

### M-S4：生成随机性与 random comparator 都必须在 selector 开发前冻结原则

多 K-pool seed、outer group / inner generation replicate、pool-mean comparator 不是论文收尾格式，而是决定：

- 估计对象是 conditional-on-one-pool 还是 marginal-over-generation；
- 需要多少调用预算与多少独立生成；
- selector 增益是否只是幸运 pool；
- random comparator 是否额外注入 Monte-Carlo 噪声。

Bouthillier 等表明数据采样、初始化与超参数来源的方差会显著改变 ML benchmark 比较；Best-of-N 文献进一步表明
imperfect reward 下 N 增大可导致 reward hacking。因此原则与预算必须在 Stage-2 proposal 前冻结，M2 只能用
单独 pilot/simulation 标定预先列出的候选设计，不能在同一信息上选设计又作后续证明。

参见 [Bouthillier et al. 2021](https://proceedings.mlsys.org/paper_files/paper/2021/file/0184b0cd3cfb185989f858a1d9f5c1eb-Paper.pdf)、
[Gao et al. 2023](https://proceedings.mlr.press/v202/gao23h.html) 与
[Huang et al. 2025](https://arxiv.org/abs/2503.21878)。

### M-S5：同权重异 prompt 的 δ_corr 门需要独立模型对照

把“跨源”改成 context-differentiated 是正确修复；但只测两个同权重 prompt 的 error correlation 不足以说明
有独立证据。应至少同时比较：

- same model / same prompt / different sample；
- same model / different prompt；
- different model family / frozen external verifier；
- non-model deterministic verifier。

阈值与删除规则在看结果前冻结。2025 年研究显示 self-consistent errors 可随规模稳定甚至增加，跨模型 probe 更能
打破共同错误；大规模模型比较也发现不同 LLM 间仍有显著 correlated errors。参见
[Too Consistent to Detect](https://aclanthology.org/2025.emnlp-main.238/) 与
[Correlated Errors in LLMs](https://proceedings.mlr.press/v267/kim25e.html)。

### M-S6：小 cluster 极端尾部方法选择仍缺可执行模拟契约

“BCa / studentized-t / wild cluster / randomization 按 simulation 选”方向正确，但仍缺：DGP 网格、cluster-size
分布、ICC、缺失机制、离散 endpoint、模拟次数、允许 Type-I 上限、coverage/power tradeoff、选择规则与独立
simulation seed。没有这些，M2 simulation 本身也可被多次试验后选择。

MacKinnon & Webb 还指出即使 wild cluster bootstrap，在 treated clusters 很少时也可能失败。因此不能把“用了
wild bootstrap”当自动安全。参见
[MacKinnon & Webb 2018](https://onlinelibrary.wiley.com/doi/abs/10.1111/ectj.12107)。

---

## 6. 对原 19 项处置的重新裁定

| 原项 | 团队标签 | 本轮裁定 | 正确门 | 理由摘要 |
|---|---|---|---|---|
| F-1 | DEFERRED@M3 | **WRONG-GATE / OPEN** | before fresh Stage-2 proposal | 主张与 estimand 身份不能在 M2 后定 |
| F-2 | FIXED | **PARTIAL** | external-anchor dossier before Stage 2 | 诚实名称修复；具体 SESOI 依据未交付 |
| F-3 | OWNER-RULED/M3 | **WRONG-GATE / OPEN** | before Stage-2 data access | 证据等级由信息流决定，不是未来标签选择 |
| F-4 | M2→M3 | **WRONG-GATE / OPEN** | design before Stage 2; pilot only on separate data | generation-marginal estimand/预算影响设计 |
| F-5 | M3 contested | **WRONG-GATE / OPEN** | Stage-1 owner problem selection | 是否证明 RDU 归因就是研究问题身份 |
| F-6 | FIXED* | **PARTIAL + SEMANTIC OVERCLAIM** | upstream anchor before eligibility/build PASS | self-pin 可复现但不能证 officialness |
| F-7 | latent/M1 | **CLOSED-AS-CODE-FIX; CURRENT-HARM-NOT-SHOWN** | keep regression gate | 此轮可接受团队的收窄解释 |
| F-8 | FIXED* + M2 | **PARTIAL / WRONG-GATE** | before any real split draw | item-disjoint 未推出 group-disjoint |
| F-9 | M3 | **WRONG-GATE / EASY-NOW** | before fresh Stage-2 proposal | 状态机是一次性证据语义，不应拖到开火前 |
| F-10 | M2 theory | **OPEN** | Stage 1 决定是否载重；Stage 2 同对象实现 | 若保留理论贡献，必须 Lean correctness+convergence |
| M-1 | M3 | **WRONG-GATE / OPEN** | Stage-1 claim-scope decision | no-harm 不是正向复现 |
| M-2 | M3 | **WRONG-GATE / OPEN** | Stage-1 claim-scope decision | 单集不能承载一般 TFRL 价值 |
| M-3 | M3 | **WRONG-GATE / OPEN** | before selector Stage-2 evaluation | comparator 定义影响效应和方差 |
| M-4 | M2 | **PLAUSIBLE STAGE, INCOMPLETE CONTRACT** | before signal inclusion; separate calibration split | δ_corr 阈值与删除规则须预先写 |
| M-5 | M2 | **PLAUSIBLE STAGE, INCOMPLETE CONTRACT** | simulation plan pre-registered before simulation | 方法候选表不等于选择算法 |
| M-6 | M2 incomplete | **P0 BLOCKER** | before M2 unfreeze | winner-only 风险不能边跑边补 |
| M-7 | M2 | **SPLIT-GATE** | rule/threshold before generation; audit after generation | 规则可先冻，审计可在 M2 做 |
| M-8 | FIXED | **PARTIAL / FAILED FINAL TRANSACTION** | before sign-off | manifest/checker 快照仍陈旧 |
| M-9 | ADDRESSED | **PARTIAL** | final output must match final input | scope 免责正确；提交证据陈旧 |
| P0 | DELIVERED/NOT_PASS | **REGISTERS DELIVERED; GATE NOT PASS** | before any data-sensitive continuation | 团队此项真状态标注基本诚实 |

---

## 7. 学术欺诈/作假嫌疑的专项裁决

### 7.1 是否发现 fabrication？

**没有建立。** 没有发现凭空产生的 confirmatory 样本、虚构的 159 测试、伪造的 23 个文件哈希，或不存在的
corpus 字节。相反，测试、哈希与本地语料均能复核。

### 7.2 是否发现 falsification？

**尚未建立，但存在需要调查的风险指标。** 当前最严重的不是发现某个数被人为改大，而是研究记录的证据等级与
实际状态不完全一致：final manifest 陈旧、checker JSON 输入陈旧、self-pin 被解释成 upstream officialness、独立
审计被重新定义、配置轨迹不全。要认定 falsification 仍需证明：相关人员明知这些陈述会使记录不准确，仍故意或
recklessly 用于研究报告/发表，并排除发布顺序失控等合理解释。

### 7.3 是否发现 plagiarism？

**本轮未作完整文本相似性审计，也未见直接信号。** 不应从“引用不充分”或“沿用通用方法”推定 plagiarism。

### 7.4 已经成立的 QRP/有害实践风险

下列风险已经由仓库事实支持：

1. **事后设计自由度**：已观察 selector 效应，M2 后仍可改 primary atom/estimand/comparator；
2. **不完整尝试账本**：未持久化的 prompt/weight/threshold/K/embedder sweep 无法回溯；
3. **public benchmark 适应性**：公开 IDs/seed 与反复迭代无法保留强 holdout 解释；
4. **状态膨胀**：`FIXED*`、`live`、`independent` 等标签强于底层事实；
5. **来源等级混淆**：self-pinned corpus 被代码轴标 PASS；
6. **随机性遗漏**：单 K-pool、单 random draw、少 cluster 尾部在当前草案仍未解决；
7. **正向复现不足**：no-harm 被放在 headline 合取里，但不能替代正向效果复制；
8. **近邻基线不足**：RDU-vs-strongest 仍不是 load-bearing primary。

### 7.5 如果团队要真正排除“作假嫌疑”，必须查什么

不要做 Benford 定律或“看曲线像不像造假”这类低质量侦测。应做以下可证据化检查：

| 审计包 | 对象 | 方法 | 通过标准 |
|---|---|---|---|
| IA-1 尝试完整性 | 574 `_repro` + shell/MLflow/Git/session logs | 按预先随机抽样 15% 工件，双人核对运行命令、输入 hash、输出、时间线 | 未登记尝试率上限预注册；所有赢家有完整前驱搜索链 |
| IA-2 效应重算 | 所有对外引用的 claim-ledger 数字 | 从 per-item 原始输出 fresh recompute，不读汇总字段 | 数值、方向、CI、样本数逐项一致；差异全部登记 |
| IA-3 手填字段 | 曾经出现“手工填 CI”的谱系 | 搜索生成脚本与 artifact provenance，检查汇总是否由脚本产生 | 每个统计字段有代码路径、输入 hash 与运行日志 |
| IA-4 重复/缓存 | 音频、生成轨迹、seed | 检查不同 seed 输出 hash、mtime、waveform/content identity | 不同独立 realization 不得实际复用同一缓存；例外具名 |
| IA-5 选择性删除 | Git 历史、superseded、临时文件、日志 | 比对创建/删除/重命名事件与 registry | 所有被丢弃运行有原因与结果，不只保留赢家 |
| IA-6 语料来源 | HF revision、zip/LFS、member | 第二人从固定 revision clean fetch，比较 archive/member/content hashes | 与团队锁逐字节一致，下载链可重放 |
| IA-7 split 污染 | eligibility/dev/confirmatory | 以统一 group manifest 重算 item 与 group 交集 | item intersection=0 且 group intersection=0 |
| IA-8 外部评分 | 最终冻结系统 | 非开发人员在只读新数据上一次评分 | 评分前无结果反馈，失败不重开同 program ID |

独立审计的结果必须允许三种输出：`NO_EVIDENCE_OF_FFP`、`INCONCLUSIVE`、`REFER_FOR_FORMAL_INQUIRY`；不能把
“未查到”写成“证明绝无造假”。

---

## 8. 文献 survey 对当前工作意味着什么

### 8.1 研究设计与预注册

- [Nosek et al. 2018](https://pmc.ncbi.nlm.nih.gov/articles/PMC5856500/)：预注册的核心是用新观测检验预先问题，
  清楚区分 prediction 与 postdiction。对本项目的含义：M2 信息可见后才选 primary atom 只能是开发性选择。
- [Chambers & Tzavella 2022](https://www.nature.com/articles/s41562-021-01193-7)：Registered Reports 在研究
  实施前审 question/theory/methods。含义：Stage-2 fresh proposal 不能由当前 v4.2 到 M3 自动升级替代。
- [Dwork et al. 2015](https://pubmed.ncbi.nlm.nih.gov/26250683/)：适应性重复查询 holdout 会过拟合；需要受控
  reusable holdout 机制。含义：public deterministic 只提供 replayability，不恢复未见信息。
- [Cawley & Talbot 2010](https://www.jmlr.org/papers/v11/cawley10a.html)：有限样本 model-selection criterion
  本身会被过拟合。含义：完整 config-selection ledger 和 nested/separate evaluation 是主证据，不是运维附件。

### 8.2 estimand、SESOI 与推断

- [ICH E9(R1)](https://www.ema.europa.eu/en/documents/scientific-guideline/ich-e9-r1-addendum-estimands-and-sensitivity-analysis-clinical-trials-guideline-statistical-principles-clinical-trials-step-5_en.pdf)：
  estimand 应贯穿问题、设计、分析和解释。含义：固定绝对 margin 不能作为“10% 相对”主张的替代问题。
- [FDA Non-Inferiority Guidance](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/non-inferiority-clinical-trials)：
  margin 需要预设并有可解释来源。含义：owner 口头“从 MCID 传统”不等于具体外部锚。
- [Lakens et al. 2018](https://journals.sagepub.com/doi/10.1177/2515245918770963)：SESOI 有多种确定方式，
  应报告理由。含义：F-2 的诚实名称只是第一步。
- [MacKinnon & Webb 2018](https://onlinelibrary.wiley.com/doi/abs/10.1111/ectj.12107)：少 treated clusters 下
  常规与 wild cluster 方法都可失败。含义：M-5 必须用冻结 DGP 的模拟，不得按结果挑方法。

### 8.3 ML 随机性、选择与 reward overoptimization

- [Bouthillier et al. 2021](https://proceedings.mlsys.org/paper_files/paper/2021/file/0184b0cd3cfb185989f858a1d9f5c1eb-Paper.pdf)：
  数据抽样、初始化、超参等多来源方差会显著影响 benchmark。含义：单 K-pool 不足以支撑部署期 selector 主张。
- [Gao et al. 2023](https://proceedings.mlr.press/v202/gao23h.html)：proxy reward 过度优化会损害真效用，BoN 也会
  出现。含义：必须限制 N/K、测 reward-utility divergence、报告 generation-marginal 曲线。
- [Huang et al. 2025](https://arxiv.org/abs/2503.21878)：BoN 在现实 coverage 条件下可 reward hack，pessimism
  可提供不随 N 退化的理论路径。含义：理论轨应围绕 constrained/pessimistic selector，而非 generic 2ε lemma。
- [Khalaf et al. 2025](https://proceedings.neurips.cc/paper_files/paper/2025/file/590a0cc0306c1c63e2d66a51a407718f-Paper-Conference.pdf)：
  inference-time reward hacking 呈先升后降。含义：N*、hedging/abstention 与真实 U 审计应成为负控。

### 8.4 同模型错误相关与污染

- [Tan et al. 2025](https://aclanthology.org/2025.emnlp-main.238/)：self-consistent error 不会因多采样自动消失，
  跨模型 probe 更有效。含义：同权重异 prompt 不是独立 verifier。
- [Kim et al. 2025](https://proceedings.mlr.press/v267/kim25e.html)：大规模 LLM 比较仍见显著 correlated errors。
  含义：即使换模型，也必须实测 error dependence。
- [Yao et al. 2024](https://aclanthology.org/2024.emnlp-main.990/)：污染可跨语言边界逃过浅表匹配。含义：q2q
  审计必须包含语义/跨语言变体，且阈值先冻。
- [Deng et al. 2024](https://aclanthology.org/2024.naacl-long.482/)：公开 benchmark 污染在黑盒模型上也可检测到。
  含义：固定公开 benchmark 不能自动获得强外推解释。

### 8.5 近邻工作与新颖性压力

- [WavRAG, ACL 2025](https://aclanthology.org/2025.acl-long.613/) 已做原生 audio retrieval 与 text/audio hybrid KB；
- [VoxRAG, MAGMaR 2025](https://aclanthology.org/2025.magmar-1.3/) 已做 transcription-free speech-to-speech retrieval；
- [AudioRAG 2026](https://arxiv.org/abs/2602.10656) 已把 audio reasoning + external retrieval 作为 benchmark 与 agentic
  baseline；
- [SQuTR 2026](https://arxiv.org/abs/2602.12783) 本身就是 spoken-query-to-text retrieval 的噪声鲁棒 benchmark。

因此，“冻结模型 + audio/text RAG + 多样本选择”本身已经不足以构成博士级新颖性。项目必须在 Stage 1 选择并
载重证明至少一个明确 delta：

1. RDU 因子化设计在 strongest comparable baseline 上跨 SESOI；或
2. proxy selector 在 equal-K、generation-marginal、跨任务复现上兑现 oracle headroom；或
3. constrained inference-time selector 有同对象 Lean 收敛定理且工程上优于合理 pessimistic/MBR baseline。

这再次说明 F-5/M-1/M-2 不能推到 M3：它们不是统计附录细节，而是“这项研究究竟新增了什么”。

---

## 9. 建议的研究 proposals 与探索检查点

### Proposal A：Stage-1 Scientific Identity Closure

目标不是继续打磨 SAP，而是在 owner 会议上只选一个 primary identity。

#### A1. 三选一主问题

| 路径 | 主问题 | load-bearing comparison | 最小杀死条件 |
|---|---|---|---|
| A-RDU | RDU 组织是否超越“只是多给知识” | RDU vs strongest of long-context / own-ASR text-RAG / frozen retriever，预算与上下文可比 | 不越外部锚定 SESOI → 不主张 RDU 新颖性 |
| A-SEL | reward-guided selector 是否兑现覆盖头空 | selector vs pool-mean random expectation + MBR/pessimistic baseline，equal-K，跨 generation seeds | 单集/单池或仅 >0 → 不主张一般 TFRL 价值 |
| A-THEORY | 受约束推断时优化是否有收敛优势 | unconstrained failure vs constrained pessimistic selector，Python=Lean 同对象 | 无收敛或只剩 generic 2ε → 删除理论贡献 |

Owner 不得选“全部都是 primary”；最多选一条 headline，其他为 ablation/secondary。Stage-1 closure 文档应列出：
problem statement、closest-neighbor table、load-bearing comparison、falsifier、资源上限、是否进入 Stage 2。

#### A2. 新颖性 checkpoint

```yaml
novelty_checkpoint:
  nearest_neighbors_required:
    - WavRAG
    - VoxRAG
    - AudioRAG
    - SQuTR
    - strongest_text_RAG_or_inference_time_selector
  pass_if:
    - claimed_delta_is_measurable
    - baseline_directly_instantiates_nearest_alternative
    - delta_has_primary_atom
    - failure_would_kill_or_downgrade_claim
  fail_if:
    - novelty_is_only_conjunction_of_existing_components
    - strongest_baseline_is_prose_only
    - no_harm_is_called_replication
```

### Proposal B：Fresh Stage-2 Preregistered Validation Program

Stage-1 owner 选题后，新建 program ID 和 fresh proposal；不得把 v4.2 原地升级。

#### B1. 最小结构

1. 冻结 problem/claim/estimand/baseline family；
2. 建立 eligibility、development、confirmatory 三份 **group-disjoint** 池；
3. 完整列出搜索空间及预算；
4. development 只在预定空间内选择；
5. confirmatory 数据不向开发者返回细粒度结果；
6. 预注册所有 generation seeds 或其抽样分布；
7. 预注册缺失、失败、重试、缓存与超时语义；
8. M4 一次开火，失败进入吸收态；
9. 偏离协议时保留原分析并将新分析标 exploratory。

#### B2. 估计量建议

```yaml
primary_estimands:
  rdu_relative_error_reduction:
    theta: "(E[error_strongest] - E[error_RDU]) / E[error_strongest]"
    threshold: externally_justified_SESOI
    resampling: paired_group_bootstrap_recompute_numerator_and_denominator
    denominator_floor: preregistered
  selector_equal_k_gain:
    theta: "E_generation,E_group[U_selected - mean_k(U_candidates)]"
    comparator_secondary: MBR_or_pessimistic_selector
    seeds: at_least_3_to_5_independent_K_pools_per_group_or_power_justified
  realization_ratio:
    theta: "E_generation[(U_selected-U_low_anchor)/(U_oracle-U_low_anchor)]"
    report: mean_and_lower_quantile
```

#### B3. 复现与泛化 checkpoint

- 至少一个不同任务族或不同核心上的正向、equal-K、越 SESOI 复制；
- no-harm 只叫 safety/generalization guard，不叫 replication；
- 如果只有单一 focus，论文题目与摘要必须明确 case study；
- responder cohort 的选择规则、总体边界和外推限制预先冻结。

### Proposal C：Proxy-Reward Stress and Overoptimization Map

这是当前方案最值得探索、也最可能形成真正贡献的方向之一。

对每个 K/N 报告：

- proxy reward `Û`；
- true task utility `U`；
- `corr(Û,U)`、rank AUROC、top-tail calibration；
- selected-vs-oracle regret；
- generation-marginal mean 与 lower quantile；
- self-consistent-error rate；
- abstention/pessimistic selection 的收益；
- 随 K 增大是否出现 `Û↑` 但 `U↓` 的 Goodhart turning point。

预注册一个 N*：在任何方向性结果前定义预算上限；若 turning point 早于 N*，则把理论对象改为受约束/hedged
selector，而不是继续提高 K。

### Proposal D：Corpus Provenance and Contamination Challenge

为每个 corpus 建三层状态，而不是一个 PASS：

```yaml
corpus_provenance:
  byte_identity:
    status: PASS_FAIL
    evidence: archive_member_hash_content_hash_doc_count
  upstream_identity:
    status: PASS_FAIL_NOT_AVAILABLE
    evidence: remote_revision_lfs_oid_published_checksum_second_fetch
  evaluation_independence:
    status: PASS_FAIL_NOT_EVALUATED
    evidence: construction_does_not_read_queries_qrels_labels
  model_pretraining_contamination:
    status: DESCRIPTIVE_RISK
    evidence: exact_fuzzy_semantic_crosslingual_overlap_and_behavioral_probe
```

只有前三层中 byte/upstream/evaluation 全 PASS 才能叫 query-independent corpus；pretraining contamination 另作风险
分析，不能由路径清白推出不存在。

### Proposal E：Independent Integrity Replication

独立人员接手只读 commit，完成 IA-1 至 IA-8。建议盲抽：

- 所有对外正效应 claim 的 100%；
- 无效/撤回 claim 的 25%；
- 其余 574 工件的固定随机 15%；
- 所有手工编辑过的汇总工件 100%；
- 所有 seed/caching bug 邻近工件 100%。

审核者先提交抽样 seed、检查脚本 hash 与判定表，再打开工件。团队只能提交事实澄清，不得替审核者改结论。

---

## 10. 分阶段整改计划与签署重提条件

### P0-A：24 小时内，仅修发布与标签，不跑任何新实验

1. 把 M-8 改为 PARTIAL，重建 final clean release manifest；
2. 对 final proposal 重跑并提交 checker output，三处 proposal hash 一致；
3. 给 discrepancy register 追加 resolution entries；
4. 修正文档中的错误 `../../../docs` CLI 路径；
5. F-6 标签改为 `SELF-PIN VERIFIED / UPSTREAM ANCHOR OPEN`；
6. 删除“送达审查者即满足独立快照/独立性未取消”的推论；
7. 将 FIXED* 拆为 `mechanism_fixed` 与 `scientific_gate_open`。

### P0-B：任何 M2 行为前

1. 完成配置搜索空间重建；不可回溯部分明确列 UNKNOWN，不得编造；
2. group-disjoint 跨 split 机制与负例测试闭合；
3. 上游 corpus provenance 第二人 clean fetch；
4. 明确 public-development 或 independently-scored-confirmatory 路线；
5. owner 完成 Stage-1 Scientific Identity Closure；
6. 新建 fresh Stage-2 proposal；
7. 独立 reviewer 对 fresh proposal 而非本 v4.2 签 Stage-2 gate。

### P1：Stage-2 pilot/calibration

只允许预先列出的 pilot：generation variance、δ_corr、small-cluster simulation、q2q contamination、预算标定。
每项用独立 calibration split；结果可以选择预先列出的 design branch，但 branch rule 必须先写。

### P2：M3 preregistration

M3 只把 fresh Stage-2 proposal 中已经预先规定的 branch 具体化，不得新增 primary claim。要求：

- exact estimand；
- primary atoms；
- SESOI dossier；
- strongest baseline selection rule；
- generation seeds/distribution；
- inference method chosen by frozen simulation rule；
- immutable state machine；
- independent scoring/custody；
- clean release manifest。

### P3：M4 fire

一次运行、一次 program ID、无 force supersede；输出先封存再评分；失败为吸收态。任何 bug 修复导致重跑都创建
新 program ID，原 run 仍保留且解释。

### 重新申请 scoped sign-off 的硬条件

```yaml
reapply_signoff_if_and_only_if:
  - final_release_manifest_matches_clean_designated_HEADs
  - stored_checker_output_hash_matches_final_proposal_hash
  - discrepancy_register_has_append_only_resolutions
  - corpus_axis_does_not_call_self_pin_upstream_verified
  - group_disjointness_is_proven_across_splits_not_only_item_ids
  - P0_config_history_is_complete_or_unknowns_are_frozen_and_scoped
  - independent_audit_is_not_redefined_as_internal_checker_plus_signature
  - stage1_owner_selects_one_scientific_identity
  - fresh_stage2_proposal_exists_before_stage2_data_sensitive_work
  - all_findings_use_CLOSED_PARTIAL_OPEN_WRONG_GATE_without_FIXED_star_ambiguity
```

---

## 11. 供团队 AI 直接消费的机读裁决

```yaml
review_decision:
  id: V42-REMEDIATION-SIGNOFF-ADR-2026-07-13
  decision: RETURN_WITH_RESIDUAL_FINDINGS
  signoff: REFUSED
  reasons:
    - final_release_manifest_is_stale_and_dirty_snapshot
    - stored_checker_output_targets_nonfinal_proposal_hash
    - critical_scientific_design_items_are_gated_after_M2_information
    - corpus_self_pin_is_misinterpreted_as_upstream_officialness
    - cross_split_group_disjointness_is_not_implemented
    - independent_audit_is_redefined_without_personnel_or_data_custody_independence
    - P0_is_honestly_NOT_PASS_and_must_stop_M2_unfreeze

verified_positive_evidence:
  appendix_hash_rows: 23_of_23_match
  w1_standard_tests: 159_passed_3_warnings_0_failures
  final_proposal_checker_fresh_rerun: 22_of_22_pass
  local_fiqa_self_lock: 57638_docs_verified
  f7_current_data_damage: not_shown
  f7_code_contract_fix: verified
  f8_partial_code_hardening: verified

integrity:
  FFP:
    fabrication: NOT_ESTABLISHED
    falsification: NOT_ESTABLISHED
    plagiarism: NO_SIGNAL_NOT_FULLY_ASSESSED
  QRP: HIGH_RISK
  formal_inquiry_trigger_now: NO_ON_CURRENT_EVIDENCE
  independent_forensic_audit: REQUIRED
  escalation_trigger:
    - use_this_package_to_claim_all_findings_closed
    - unfreeze_M2_before_P0_and_stage_gate_correction
    - omit_known_selection_or_snapshot_discrepancies_in_public_reporting
    - discover_unregistered_runs_or_manual_result_edits_affecting_claims

finding_status:
  F_S1_stage_inversion: FUNDAMENTAL_STOP
  F_S2_release_manifest_stale: FUNDAMENTAL_STOP
  F_S3_checker_output_stale: FUNDAMENTAL_STOP
  F_S4_corpus_officialness_overclaim: FUNDAMENTAL_STOP
  F_S5_cross_split_group_leak: FUNDAMENTAL_STOP
  F_S6_independence_redefinition: FUNDAMENTAL_STOP
  F_S7_P0_not_pass: FUNDAMENTAL_STOP
  M_S1_evidence_grade_late_choice: MAJOR
  M_S2_SESOI_anchor_missing: MAJOR
  M_S3_estimand_mismatch: MAJOR
  M_S4_generation_and_comparator: MAJOR
  M_S5_error_correlation: MAJOR
  M_S6_small_cluster_simulation: MAJOR

allowed_next_actions:
  - documentation_and_evidence_snapshot_correction
  - read_only_independent_audit
  - stage1_literature_survey_and_owner_problem_selection
  - synthetic_unit_tests_and_design_simulation_with_frozen_rules
blocked_next_actions:
  - new_data_sensitive_M2_search
  - eligibility_or_confirmatory_draw
  - M3_primary_atom_or_estimand_choice_after_M2_results
  - any_confirmatory_or_M1_closed_claim
```

---

## 12. 给研究团队的正式 reviewer response 要求

下一轮不要再写一篇以“我们已修了很多”为中心的长叙事。请按以下格式逐项回复：

```yaml
response_item:
  finding_id: F-Sx_or_M-Sx
  accept_reject_partial: ACCEPT|REJECT_WITH_EVIDENCE|PARTIAL
  exact_fact_disputed: null_or_one_sentence
  evidence:
    frozen_commit: sha
    files: []
    commands: []
    expected_outputs: []
  status_before: OPEN|PARTIAL|CLOSED|WRONG_GATE
  status_after: OPEN|PARTIAL|CLOSED
  gate_before_any_data_action: explicit_event
  scientific_claim_enabled: none_or_exact_claim
  integrity_implication: none|record_corrected|formal_inquiry_needed
```

不接受以下回复方式：

- 用 owner 裁决替代方法学证据；
- 用“checker PASS”回答科学有效性；
- 用“报告已披露”回答错误挂门；
- 用 `FIXED*` 混合“代码局部修复”和“科学门仍未闭合”；
- 用未来时承诺关闭当前发布证据不一致；
- 把本报告签字本身当独立审计已完成。

**最终决定保持：退回。** 当且仅当 §10 的重提条件全部满足，才重新审 scoped sign-off；即便届时签署，也只会
签“整改事实与门控一致”，不会替代 Stage-2 proposal 评审、独立完整性审计或 M4 科学结论审稿。
