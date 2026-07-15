---
review_id: SURVEY-P0R-PROGRESS-DOCTORAL-ADVERSARIAL-REREVIEW-2026-07-14
title: P0-R 整改进展提交的博导级对抗复审（Stage-1A 口径）
date: 2026-07-14
reviewed_submission: wiki/2026-07-14-p0r-progress-review-submission.md
reviewed_submission_commit: f5c736e9a9dffd9ddc3312a789291f9f3e110d6c
reviewed_evidence_anchor_claimed_by_team: 78d048550080bb3131b3d1db9646ff4dfbf0c0f0
stage: Stage-1A（问题界定；不是成型论文审查）
reviewer_role: strict external reviewer + doctoral supervisor + research-integrity examiner
verdict: RETURN_FOR_MAJOR_REVISION
required_next_state: P0_REMEDIATION_IN_PROGRESS
round2_search_authorized: false
stage1b_authorized: false
integrity_finding: FFP_NOT_ESTABLISHED__SURVEY_RECORD_QRP_RISK_HIGH
p0r_score: "2 CLOSED_FOR_PRIOR_DEFECT + 5 PARTIAL/REOPENED + 1 NOT_DONE"
source_edit_policy: "仅新增本日期化独立审查；未修改团队任何既有源文件、协议、台账或热状态"
---

# P0-R 整改进展提交的博导级对抗复审

> **审查对象**：`2026-07-14-p0r-progress-review-submission.md` 及其指向的 census、claim ledger、
> C1/C4、身份合同、Round-2 协议和 Stage-1B 四探针协议。
>
> **阶段校准**：当前仍是 Stage-1A 收尾整改，不以论文发表标准要求统计确证、完备实验或最终 SOTA；
> 但只要团队要据 survey 排除候选问题、冻结身份、决定是否投入 GPU，承重文献、分母、版本、判据和
> 诚信状态就必须可审计。Stage-1A 不是降低真实性标准，而是降低实验结论等级。

---

## 0. 总裁定

本轮不是失败。团队相较上一轮有实质进步：

- 没有把 Round-2 或 Stage-1B 偷跑；
- census、claim ledger、三线状态和身份合同均已有真实工件；
- 对 KIT、JudgeBoN、Ernez、Audio-Mind 等承重材料主动发现了不利于自己的错误；
- 明确保留 `SINGLE_PASS_AI`、双审待做、独立审查待做、P0-R8 未做；
- §1 所列 11 个工件哈希前 16 位，我按 `git show 78d0485:<path> | sha256sum` 重算，全部相符。

但是，**本轮仍不得签署 P0-R 闭环，也不得批准 Round-2 或 Stage-1B 执行**。主要原因不是团队还没有
做“大样本实验”，而是当前证据对象仍存在五个承重缺陷：

1. census 没有达到上一轮明示 schema：缺全作者、source content hash；56 个 `RESOLVED` work 未固定
   版本；6 个 `RESOLVED` work 没有要求的 arXiv/DOI/OpenAlex ID；
2. claim ledger 缺 `source_content_hash / verified_by / verification_status`，5 行版本未固定，且把多篇
   paper 合成一行后赋一个 evidence grade；
3. “43 条 discrepancy”是错误计数：43 只是非空字符串数，其中 **11 条逐字以 `None` 或
   `None material` 开头**，另外还有多条只是轻微补充或“确认原说法”；
4. 11 个 “extract-stage drops” 只有总数，没有 item ID、内容和 reason code，无法排除选择性丢弃；
5. strict-I2 的 `δ_corr` 在冻结合同与探针中发生同名异义，P-γ 以“选择重合 >90%”代替误差去相关，
   因而当前 kill-if 在数学和构念上不可执行。

因此本轮 P0-R 计分为：

```text
P0-R1  CLOSED_FOR_PRIOR_DEFECT（但本提交新增 snapshot provenance 缺陷）
P0-R2  PARTIAL
P0-R3  PARTIAL — MATERIAL SCHEMA/COUNT DEFECTS
P0-R4  CLOSED_STRUCTURE_ONLY（三线已拆；两条科学线未通过）
P0-R5  PARTIAL（热层正确；可复用模板/机器旧 token 尚会回灌）
P0-R6  REOPENED_PARTIAL（post-hoc 标注正确；δ_corr 合同自相矛盾）
P0-R7  PARTIAL
P0-R8  NOT_DONE
```

**最终 verdict：`RETURN_FOR_MAJOR_REVISION`。** 这不是要求团队继续无限整理文档；本报告给出的 P0
动作均可在零 GPU 条件下完成，完成后才值得消耗检索和原型预算。

---

## 1. 三轮对抗式审查如何进行

### Round A — 先假设团队的完成度标签不可信

我没有用提交稿中的 `CLOSED/ADVANCED` 反推事实，而是直接检查：

- git commit 是否真的包含被审稿；
- §1 哈希是否对应 78d0485 的 git blob；
- census/ledger 的实际字段、空值、版本、ID、复合行和丢弃分母；
- 热层、旧模板和机器工件中的状态 token 是否一致；
- C1/C4 的正文、addendum 和 owner pending 是否一致。

这一轮证实哈希真实，但推翻了 92 resolved、35 fulltext、43 discrepancy 等数字被当作“接近闭环”的
含义。

### Round B — 再假设记录都是真的，但科学对象仍可能测错

我把身份合同和四探针逐项反演：每个观测是否真能推出合同里的 proceed/pivot/kill，是否存在同样
观测但相反科学解释。P-γ 和 P-δ 均没有通过这一步；MBR、shuffle-audio、选择重合、供给移动都存在
替代解释。

### Round C — 最后假设最坏动机，再寻找反证

我外部抽核团队本轮最强调的四个自我纠错，并检查是否出现编造论文、捏造表格、选择性只纠正有利项。
四个关键纠错均被原文支持，且其中多项明显损害团队原叙事。这构成“目前更像诚实但失控的记录工程，
而非有证据的 FFP”的反证。随后我再用 ORI 的 FFP 门槛检验是否足以指控造假；结论是不足，但 QRP
风险仍然高。

---

## 2. 提交稿自身的 provenance 缺陷

### 2.1 §1 哈希是真的

提交稿列出的 RESP-02、身份合同、两份协议、census 两件、ledger 两件、C1/C4 三件，其 sha256 前
16 位均与 78d0485 的 git blob 相符。这里没有发现伪造哈希。

### 2.2 但提交稿不是 78d0485 的一部分

frontmatter 写：

```text
survey_snapshot.commit = 78d0485...
“本稿与三份 ... banner 同一 commit 提交”
```

实际检查：

- `git cat-file -e 78d0485:wiki/2026-07-14-p0r-progress-review-submission.md` → 不存在；
- 该稿及三份 banner 是在后续 commit `f5c736e` 才加入；
- 78d0485 只包含两份协议。

所以，这是**错误的自我快照声明**，不是哈希造假。修复方式不是改旧稿，而是新增 dated correction，
明确：`evidence_artifacts_anchor=78d0485`，`submission_artifact_anchor=f5c736e`，并给本稿自身的 git-blob
hash。团队过去已经因 snapshot 混写受过审查，本次复发应提升为机器校验项。

### 2.3 工作流 provenance 仍不可审

提交稿称 census/ledger 来自两个 workflow、合计 19 agents；仓库中没有对应工作流日志、逐项 agent
输出、merge script 或 11 个 drop 的明细。现有工件只能审结果，不能审生成轨迹。因此：

```text
“single-pass AI output exists” = TRUE
“workflow can be independently replayed” = FALSE
“extract-stage exclusions are auditable” = FALSE
```

Stage-1A 不要求保存每个模型思维过程，但必须保存输入清单、结构化输出、丢弃日志和确定性 merge
规则；否则多 agent 数量只是过程描述，不是证据。

---

## 3. P0-R2 canonical census 复核

### 3.1 已经做对的部分

- 94 被正确降级为 `record_clusters`，没有再直接叫 94 papers；
- 92/2/0、36 versions pinned 分列，没有聚合成一个完成度分数；
- P-0016 和 P-0084 被如实暴露；
- arXiv/DOI 非空值之间的碰撞检查可重算；
- 记录里没有为了填满字段而虚构 DOI 或版本。

这些都应保留。

### 3.2 为什么不能 CLOSED

上一轮 P0-R2 明确要求 `canonical ID + title + authors + version + date + URL + content hash`。当前
`census_records.jsonl` 只有：

```text
paper_id, ledger_key, status, confidence, title, first_author, year,
arxiv_id, doi, latest_version, version_date, canonical_url, venue,
resolution_source, notes
```

承重缺口如下：

| 缺口 | 实测 |
|---|---:|
| 全作者字段 | 0/94（只有 `first_author`） |
| source/content hash | 0/94（schema 中不存在） |
| 版本与日期同时存在 | 36/94 |
| `RESOLVED` 但版本未 pin | 56 |
| `RESOLVED` 但 arXiv 和 DOI 均空 | 6 |
| `resolution_source` 空 | 9 |

6 个无审查所要求 canonical ID、却被计为 `RESOLVED` 的 work 是：P-0001、P-0002、P-0009、
P-0014、P-0054、P-0062。它们可能真实且可唯一识别，但在当前验收规则下，必须二选一：

1. 补 OpenAlex ID/DOI/arXiv ID；或
2. 正式修订 ID 规则，允许 ACL Anthology/ISCA/PMLR 原生 work ID，并把这次规则变化记录为 protocol
   amendment。

在未做其中任一项前，`identity_resolved_works=92` 和 `resolved_unique_works=92` 不是按上一轮规则得到的
精确数。

### 3.3 对 P-0084 的裁决

**接受将 P-0084 解析为 arXiv:2606.04730，但只能在 census v2 中生效。** 理由不是题名猜测，而是
claim ledger 中 ASR −32.10、SQA +14.42、SSUM +3.85、ST +6.11 这一组数与该论文 Table 3 唯一对齐。
论文原文同时给出 likelihood 在 SQA/SSUM 的 −11.06/−8.60，以及 Likelihood+MBR 的 −3.33/−2.19，
支持团队本轮纠错。来源：[KIT IWSLT 2026, Table 3](https://arxiv.org/html/2606.04730)。

要求：记录 `resolution_basis=NUMERIC_FINGERPRINT_TABLE3`、核验人、版本 v1、source hash；不得只在
claim ledger 里“事实解决”，却让 census 继续 AMBIGUOUS。

### 3.4 对 P-0016 的裁决

**接受拆成两个 work；不接受二选一。** 原 alias 本身覆盖 ICASSP 2015 与 ICASSP 2016 两篇，正确
数据模型是：

```text
source_cluster P-0016  --maps_to--> work W-2015
                         maps_to--> work W-2016
```

这说明 `record_cluster` 与 `paper_work` 不是同一张表。若 P-0084=1 work、P-0016=2 works，则 94 个
source clusters 在结构上可映射到 95 个 candidate works；但在 6 个无合规 ID 和人工双审未清前，
不得把“95 papers”作为 exact headline。

这与证据综合中“records 与 studies 必须分开计数”的成熟做法一致；Cochrane Handbook 也要求把多个
report 归并到 study，并分别记录 records→studies 的流转。这里借用的是数据建模原则，不是要求团队
把 Stage-1A 做成医学系统综述。[Cochrane Handbook §4.5–4.6](https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-04)

---

## 4. P0-R3 / P0-R7 claim ledger 复核

### 4.1 这不是“假台账”，但也还不是真正的可签 claim ledger

44 行均有 `exact_claim_text / team_interpretation / operator_type / source_locator /
support_relation / generated_by`，并且明确 `double_review_pending=true`。作为一次 AI 承重抽取，它比上一版
强很多。

但是，它没有满足上一轮列出的最小字段：

- 没有稳定、逐行唯一的 `claim_id`；`claim_key` 有 3 组重复；
- 没有 `source_content_hash`；
- 没有 `verified_by`；
- 没有独立的 `verification_status`；
- 34/44 行没有显式 `claim_class`；
- 5 行 `paper_version_used` 仍写 unversioned/latest/current；
- 5 行把多篇 work 合成一个 row，导致一个 evidence grade 覆盖多种证据深度。

所以 `CLAIM_LEDGER_V1_SINGLE_PASS_AI` 这个 token 是诚实的，`44 承重行带 verbatim quote` 则不是。
不少 `exact_claim_text` 是表格数值的整理、计算或多文献综合，并非逐字引文。可以保留这些内容，但字段
必须拆成 `verbatim_span`、`structured_extraction` 和 `reviewer_inference`。

### 4.2 “43 discrepancies”必须撤回

机械事实是：

```text
44 rows
43 non-empty discrepancy strings
11 strings begin with “None” or “None material”
1 empty string
```

因此“43”只能叫 `nonempty_discrepancy_field_count`，不能叫 43 条 discrepancy，更不能全部叫
“candidate corrections”。其中至少 11 条明示没有实质 discrepancy；另有若干只是 minor note、确认原
纠错正确或提供额外细节。

这不是微小命名问题。把“检查过且无问题”计成“发现 1 个问题”，会人为放大纠错环路产出，属于典型
completion/status inflation。建议 schema 强制：

```text
discrepancy_status ∈ {NONE, MINOR, MATERIAL, CRITICAL, UNVERIFIED}
discrepancy_text
affects_identity_verdict: true|false
affects_numeric_claim: true|false
requires_upstream_correction: true|false
```

headline 必须分别报五类数，禁止以非空字符串代替问题计数。

### 4.3 11 个 extract-stage drops 是当前最危险的分母缺口

`ledger_report.md` 只写 “Items dropped at extract stage: 11”，全仓库没有这 11 项的 ID、原内容、
被丢原因或责任 agent。commit message 却称 “11 extract-stage drops logged (no silent caps)”。两者不相符。

在无法看到 drop 明细时，审查者不能排除：

- 不利于 novelty 的 claim 被丢；
- 无法核验的 claim 被丢，从而抬高 fulltext 比例；
- 相同论文的冲突 claim 被选择性保留；
- 只是格式失败，还是科学排除。

必须补 `claim_extract_exclusions.jsonl`，最少字段：`source_claim_id / source_artifact /
paper_work_id / raw_claim / drop_reason_code / dropped_by / timestamp / recoverable`。历史信息若确实遗失，
逐项标 `RAW_DROP_DETAIL_UNAVAILABLE`，不能只留总数 11。

### 4.4 evidence grade 有内部冲突

至少以下行把 `CLAIM_LOCATED_FULLTEXT` 用在自身 locator 明示仅摘要或部分文献未读的情形：

- `occupy-umbrella-system-audiotoolagent`：version 与 locator 均写 abstract；
- `occupy-text-training-free-rl`：三篇的 locator 主要是 abstracts；
- `open-umbrella-intersection`：五篇合成，locator 明写 component abstracts；
- `reanchor-coordinator-verified-depth-cap`：自身说明 5 篇中仅 2 篇本轮 fulltext reached；
- `occupy-i3-conformal-ser-trained`：locator 只钉 abstract。

这足以推翻“35 全文定位”的精确计数。正确做法是**证据跨度一行一个 grade**，综合 claim 不得继承
最强子证据等级；其 grade 应取支撑链的最低必要证据，或干脆写 `SYNTHESIS_PENDING_REVIEW`。

### 4.5 operator census 有价值，但还不能关闭 R7

44 行确实全部有 operator/pool/verifier 字段，这是实质进步。仍不能关闭的理由：

- 上述 evidence grade 和复合行会污染 operator 计数；
- 5 行版本未固定；
- 14 行 `oracle_definition_note` 空，虽非每行都需要 oracle，但目前没有结构化 `not_applicable_reason`；
- 数值行的 model/dataset/split/K/budget/metric 尚未全部拆成机器字段；
- 上一轮要求的“另一 reviewer 随机复核；发现错误即扩大范围”未发生。

因此团队自报 R7=PARTIAL 是正确的；R3 的 `ADVANCED` 可作为进度描述，但不能升级为验收状态。

---

## 5. 外部论文抽核：团队哪些纠错是真的

| 团队本轮纠错 | 外部抽核 | 裁定 |
|---|---|---|
| KIT ST oracle = +6.11；SQA/SSUM label-free 选择为负 | Table 3 给出 Oracle +6.11，Likelihood −11.06/−8.60，Lik.+MBR −3.33/−2.19 | **正确** |
| JudgeBoN Recovery 以 random choice 为锚，21.1%→61.2% | 论文把 Recovery 定义为相对 random 与 oracle 的恢复，并报告 matched pair 21.1%→61.2% | **正确** |
| Ernez 的 80% 不是 answer coverage，且平均集合 29 句 | PMLR 摘要写 WER<2%、confidence level 80%、average set size 29 | **正确** |
| Audio-Mind “>10 call cliff”只有 n=6 | Appendix B.4 明写 six questions，50.0%→16.7%，不足可靠解释 | **正确** |

来源：

- [KIT IWSLT 2026](https://arxiv.org/html/2606.04730)
- [When LLM Judge Scores Look Good but Best-of-N Decisions Fail](https://arxiv.org/html/2603.12520)
- [Ernez et al., PMLR 204](https://proceedings.mlr.press/v204/ernez23a.html)
- [Audio-Mind](https://arxiv.org/html/2605.28480)

这四项中，KIT、Ernez、Audio-Mind 都削弱团队先前叙事，说明本轮 claim audit 至少在抽核样本上不是
“只改有利错误”。这也是本报告不支持直接指控 FFP 的重要依据。

但四项抽核通过不能外推到 44 行，更不能外推到 94 clusters。它只说明 `sampled_corrections_supported`。

---

## 6. P0-R4 / R5 / R6 / R8 的逐项裁定

### 6.1 P0-R4：结构关闭，科学审计未关闭

提交稿 §6 已把 build、bibliographic、scientific 三线分开，且没有用 12/12 覆盖后两条。我接受
`R4=CLOSED_STRUCTURE_ONLY`。但：

```text
build_reproducibility = internal counts/hash check
bibliographic_audit = unsigned single-pass state
scientific_claim_audit = unsigned single-pass state
```

不能把“分了三栏”理解成三条线均通过。

### 6.2 P0-R5：身份索引方案正确，但操作面尚未彻底止血

RESP-02 按 identity 索引最大允许结论，是对上一轮 global token 逻辑洞的正确修复；热层也已明确
I1/bare-I2 occupied、strict-I2 等仅 AMONG_RETAINED_RECORDS。

但仍有两个主动回灌源：

- `2026-07-14-survey-response-replayability-template.md` 仍把
  `NO_DIRECT_MATCH_WITHIN_LOGGED_SCOPE` 当示例/规则；
- `scout-ledger-round2.json` 等机器工件仍保留 global token，而没有机器可读 superseded_by。

鉴于 owner 已要求减少上下文噪音，本报告不要求批量改历史文件。最低成本做法是新增一个 successor
template/overlay，旧模板顶部或外部 manifest 标 `SUPERSEDED_FOR_MAX_CLAIM_TOKEN`，所有新 agent 默认只读
successor。完成前 R5=PARTIAL；不是因为旧史料存在，而是因为它仍是可复用操作入口。

### 6.3 P0-R6：post-hoc 标注合格，但 `δ_corr` 使合同必须重开

strict-I2 被诚实标成 `POST_HOC_NARROWED_CANDIDATE, post_hoc_created_at=2026-07-14`，这一点接受。

不可接受的是同一符号承载两套相反语义：

- `Theory-Convergence-and-Constraints.md`：`δ_corr` 是 achievable error-decorrelation，且
  “convergence → oracle as δ_corr → 0”；
- v4.2 整改记录：要求实测 error-correlation / conditional mutual information；
- 身份合同/探针：`δ_corr≈0` 被操作化为 same-core 与 external 选择重合 >90%，并判 kill。

“选择相同”不是“错误相关”，更不是条件互信息。两个 scorer 可能 100% 选择相同且都正确，也可能
100% 相同且都错；仅凭 overlap 无法判断独立价值。JudgeBoN 也明确说明全局 agreement/correlation
不能识别 within-prompt decision utility，应报告 within-prompt signal、Recovery 与 PCS。

必须拆名：

```text
selection_overlap = P(argmax S_same == argmax S_external)
error_corr = Corr(1[sel_same wrong], 1[sel_external wrong])
conditional_error_mi = I(E_same; E_external | item/headroom/difficulty)
complementary_gain = U(best router/combiner) - max(U_same, U_external)
```

若旧理论中的 `δ_corr` 是残余错误相关，越小越好；若团队想表达“去相关量”，应换新符号并规定越大越好。
在符号方向、估计对象和 kill threshold 三者统一前，身份合同虽有 owner 治理签核，仍不能作为科学执行
合同。修改会改变 kill-if，必须走合同 amendment + owner 重新签核，不能记作执行层小参数。

另一个合同缺口是：same-selector contract 把 UMBRELLA “环内每一步”也强制成 K 池内选择，但 UMBRELLA
定义只说 advantage→next action，并未定义每步固定 K action pool。要么为 UMBRELLA 单独冻结 action
proposal pool，要么明确 same-selector contract 不覆盖 tool-loop 的生成/扩池阶段；不能靠一句“仍受约束”
把不同 operator 变成同一对象。

### 6.4 P0-R8：团队自报 NOT_DONE 正确

当前没有 repo-level fail-closed validator 读取 response、hot status、decision package、census、ledger、
signoff。R8 维持 NOT_DONE。它必须在 Round-2 前完成最小版，因为本轮新发现的 snapshot 错配、43
discrepancy 误计和 owner pending/prerequisites_met 冲突都适合机器拦截。

---

## 7. 对 RESP-02 四处抗辩的正式裁决

### 抗辩 1：`WITHIN_LOGGED_SCOPE` 是上一轮 reviewer 的处方

**抗辩成立。** 团队当时采用该词有善意遵从的合理解释，不应追溯性定为“故意制造全局空白”的
FUNDAMENTAL 诚信行为。正确裁定是：

```text
prior use = reviewer-induced ambiguous wording / process QRP
forward use = prohibited after ambiguity was exposed
```

团队已前瞻修为 identity-indexed token，应保留。旧模板回灌问题另行修复。

### 抗辩 2：永久缺失的 flow counts 应与 replay failure 同逻辑

**大体成立。** returned/screened/included/excluded 若历史确实不可恢复，应以
`CLOSED_WITH_PERMANENT_FLOW_COUNT_FAILURE` 收档，不能把“不可能完成的数字”永远列成可执行 blocker。
但由此不会自动关闭 canonical work/version census；后者是可执行、且本轮仍未合规完成的 R2。

### 抗辩 3：前审 Round 6/7/8 标题比实际分歧更强

**部分成立。** 前审确有“标题像驳回、结论却采纳收窄”的修辞失衡。应降低对团队动机的指控强度，
但不改变科学结论：bare-I2 mechanism occupied、I4 method family occupied、strict-I2 post-hoc、全局 token
有逻辑洞。

### 抗辩 4：全局 token 本身不完备

**成立，且团队的 identity-indexed 修复优于前审原先的单一替代 token。** 本轮不再要求恢复一个全局
maximum claim。机器规则应检查每个 identity 的合法 token，而不是寻找唯一全局字符串。

---

## 8. Round-2 检索协议预审

### 8.1 可保留的设计

- 查询前锁定身份合同 commit/hash；
- 每次 SEARCH/FETCH/CHASE 分枚举，失败也在分母；
- raw response、rank、筛选决定、reason code 分件保存；
- 合取占据要求单一实例完成合取；
- 已知目标、forward/backward chase、方法别名均进入计划；
- gap 存在时禁止写 saturated。

这套骨架明显优于 Round-1。

### 8.2 当前协议不能称完整 preregistration 的原因

1. **真正的 query strings 尚不在被审协议中。** 第 41–42 行把它推迟到未来 `protocol.yaml`；因此当前
   文档只预注册了“以后会预注册”。必须在第一条查询前把实例化 query 文件提交并纳入 reviewer
   审查/hash。
2. **`DRAFT — 无 owner 异议即生效` 不合格。** 沉默不是批准。应由 reviewer 对 search design
   signoff，owner 只做资源/治理批准；至少需要显式 active commit。
3. **WebSearch raw capture 只能提供 trace replay，不能保证 rerunnable search。** 搜索引擎会个性化、
   本地化、更新索引；Cochrane 也明确指出 web search 的结果不可能达到 bibliographic database 的
   同等可重复性。协议应把 `trace_reconstructable` 与 `query_rerunnable` 分开报告。
4. **数据源覆盖不够贴合语音/多模态领域。** 至少显式加入 ACL Anthology、ISCA Archive、IEEE Xplore
   或其可检索替代、Crossref；arXiv/Semantic Scholar/dblp/OpenReview 不能完整替代领域 venue。
5. **RQ 仍偏向寻找“完整合取占据者”。** 需要同时预注册 disconfirming lanes：去掉团队自造术语、
   搜 method-family 同构、搜 trainable 邻域、搜 supply selection/verification/reranking 的替代名称；
   否则可能通过不断求交制造空白。
6. **IN/EX 的主观词没有 adjudication examples。** “可迁移机制”“供给操作”“纯文本无迁移主张”需各给
   至少 2 个正例、2 个反例和冲突处理规则。
7. **“连续两轮 chase 无新增”不是稳定停止规则。** 必须定义一轮、种子集、每个 citation source、
   最低独立引擎数、查询族覆盖、yield curve；否则 API 漏索引也会制造局部饱和。
8. **筛选只有 agent_id，没有独立复核设计。** 对所有潜在 DIRECT/PARTIAL、所有 exclusion at fulltext、
   以及随机样本必须第二 reviewer 复核；冲突进 adjudication log。
9. **语言限制需说明。** Stage-1A 可因预算以英文为主，但必须保留 `awaiting_classification`，不能让
   非英文记录直接消失。
10. **版本冻结与 content hash 必须继承 census v2。** 新 work 不能只写“走 canonical 流程”，要写
    schema version 和 fail-closed 条件。

PRISMA-S 要求把各数据源的完整检索式按实际运行内容保存；PRESS 要求同行检查 research question
translation、Boolean/proximity、subject headings、text words、拼写/语法和 limits/filters。当前 Stage-1A
不必宣称符合医学系统综述，但可以直接借用这两个最低成本检查表做 query preregistration 的敌意预检。
来源：[PRISMA-S](https://pmc.ncbi.nlm.nih.gov/articles/PMC7839230/)、
[PRESS 2015](https://pubmed.ncbi.nlm.nih.gov/27005575/)。

### 8.3 Round-2 执行门

```text
ROUND2-G1  identity contract amendment（δ_corr）已签
ROUND2-G2  instantiated protocol.yaml + exact queries 已提交/hash
ROUND2-G3  database/venue coverage 表已补
ROUND2-G4  inclusion examples + second-screen plan 已补
ROUND2-G5  stop rule 可机械执行
ROUND2-G6  P0-R8 最小 validator 已通过
```

六门全绿后才执行第一条查询。无需等 Stage-1B；Round-2 本身仍属于 Stage-1A。

---

## 9. Stage-1B 四探针协议预审

### 9.1 值得保留的设计

- 零运行、owner pending 如实；
- K 池共享、单次触碰、失败保留、gold 只在事后 U；
- H(c) 与 selector 失败分开归因；
- MBR 作为强基线；
- 全部数字 directional-only，不做显著性结论；
- C-T7 前科被显式写入检索供给门。

这些是正确的 Stage-1B 纪律。

### 9.2 P-γ 目前测错对象，是阻断级缺陷

#### 缺陷 A：audio-conditioned continuation logprob 可能只是已占据的 self-likelihood

协议没有定义与生成角色不同的 verifier prompt/context，也没有定义新的音频接地 correctness score。
用同一模型、同一音频/提示给既有 continuation 求 logprob，最自然的解释就是重新读取生成概率——这正是
bare-I2 已被 scaling-auditory 占据的 mechanism，不足以测试 TH2a 的 context-differentiated dual-role
假设。

必须先写清：generator context、verifier context、输出 score、长度归一、candidate formatting、是否
要求模型判断“音频是否支持该答案”。若只做 likelihood，应把探针改名为 `same-core likelihood baseline`，
不得称 strict-I2 独立信号。

#### 缺陷 B：selection overlap 不能代替 error decorrelation

`overlap>90% → δ_corr≈0 → kill` 无逻辑效力。需要在有 oracle headroom 的 item 上构造两个 selector 的
错误指示，并至少报告：

```text
overlap / rank correlation
each selector's Recovery/PCS/rho/regret
error Q-statistic or phi correlation
conditional error MI（可选，样本小只作描述）
oracle-complement cases：A错B对 / A对B错 / 都错 / 都对
router upper bound and complementary gain
```

只有“高度同错 + 无 complementary gain”才能支持“无独立价值”。JudgeBoN 的直接教训就是：aggregate
agreement 不能推出 within-prompt decision validity，应以 Recovery/PCS 等终端量收口。

#### 缺陷 C：shuffle flip-rate 不是充分的音频接地检验

候选池可能文本上高度同质，音频被换后 argmax 不变，并不代表 score 不依赖音频；反之，极小 score
扰动也可能在 margin 很小时翻转 argmax。至少增加 matched controls：

- correct audio；
- item-permuted audio；
- silence/masked audio；
- 同说话人/同长度 hard negative audio；
- score delta、rank correlation、winner margin、最终 U，而不只 winner flip。

### 9.3 P-β MBR 的效用定义与“复现 31%”不兼容

协议用 `1-WER` 做候选两两效用，却拿文献约 31% 当方向锚。该文献实际使用 BLEU/sacreBLEU，并明确
说明没有把 WER/CER 作为 MBR utility，因为 MBR 会膨胀所优化指标；论文也提醒 pairwise utility 常不
对称。[Re-evaluating MBR for ASR](https://arxiv.org/html/2510.19471)

因此当前结果即使偏离 31%，也不能归因为 I4 的 supply dependence，因为同时变了模型、噪声、dataset
split、K、sampling、utility 和 normalization。改进方案：

1. 主 baseline 严格复现文献 BLEU utility；
2. `1-WER` 作为预注册 sensitivity arm，明确有向 pseudo-reference 顺序或对称化规则；
3. 把“约 31%”改为 external reference，不设 replicate expectation；
4. MBR 自身的 `delta_mbr` 恒为 0，不把它当信息量指标；报告 rho/regret/PCS 即可。

### 9.4 P-δ 目前只能测“发生变化”，不能支持 I4 科学贡献

`c1=检索上下文或任务指令增强，运行前择一` 是承重 researcher degree of freedom。两者的信息机制、
泄漏风险、成本和候选分布完全不同，不能签批后再选。且只比较 c0/c1 出现 H 或 rho 移动，最多证明
“更改生成条件会改变生成池/选择表现”——这是定义上预期的，不是 I4 的增量预测规律。

必须：

- 在 owner 签批前固定 c1 类型、来源、模板、budget 和 hash；
- 若为 retrieval，零 exact-gold intersection 不够，还要查近重复、paraphrase、answer-bearing chunk、
  benchmark contamination 和索引构造 lineage；
- 分解 `supply changes pool` 与 `selector changes realization`：同报池多样性、pool overlap、H(c)、
  fixed-selector rho、cost；
- 将结果只解释为 “I4 necessary condition probe”，不得写成预测 law 或 novelty support；
- 真正的 I4 候选应提出至少一个相对 difficulty/entropy/K/model-size 的增量预测，并留到后续验证。

### 9.5 其余必须在 owner 签批前冻结的参数

当前把下列项留到运行前登记，不足以防止结果导向选择：

- n=60–100 的具体 n；
- item IDs、抽样 seed、排序和排除规则；
- temperature/top-p/top-k/seed/max tokens；
- c1；
- SER “提示不稳”后切模型的客观触发条件；
- greedy 是否包含在 K 池，rho anchor 如何处理；
- invalid output/parse failure/timeout 的计分；
- shuffle 配对 seed；
- code commit、model file hash、llama-server build、prompt hash。

“运行前登记”只有在任何研究 item 未被生成、任何输出未被观察前完成，且生成不可修改的 frozen run
manifest，才等价于预注册。建议先对不进入研究样本的 dev smoke item 验证 API，再冻结研究 manifest。

### 9.6 不要用未来的 publication holdout 做 Stage-1B 方向探索

C-ASR 直接选 `LibriSpeech test-other`。若 Stage-1B 的结果将影响 selector、c1、阈值或候选身份选择，
这些 test items 此后不再是 untouched evaluation。Stage-1B 应使用 dev-other 或专门的 exploration split；
CREMA-D/MMAU 也应建立 subject/item-disjoint exploration manifest。所有被碰过的 item 进入 exposure
registry，Stage-2/3 另留未触碰 holdout。

### 9.7 C1/C4 与 owner 协议签批不能绑成一个动作

协议 frontmatter 写 `prerequisites_met=C1/C4 complete`，正文又说 owner 将在签探针时终验 C1/C4。
这是循环状态：前置尚未终验，却已标 prerequisites met。且让 owner 一次签字同时承担诚信 census
验收和实验授权，未来难以区分签署语义。

应拆成两个 exact-hash block：

```text
Integrity gate: owner acknowledges C1 permanent gap + accepts C4 census
Protocol gate: owner authorizes exact frozen probe manifest
```

前者先完成，后者后完成；同一人可以签，但不能同一栏混签。

---

## 10. 是否涉嫌学术欺诈：严格但不越权的结论

ORI/美国联邦常用定义将 research misconduct 限定为 fabrication、falsification、plagiarism，并要求
显著偏离领域实践、主观上故意/明知/鲁莽、且以优势证据证明；honest error 与意见分歧不自动构成
misconduct。[ORI definition](https://ori.hhs.gov/definition-research-misconduct)、
[ORI requirements](https://ori.hhs.gov/policies-regulations-qa)。本项目未必受该法规管辖；这里只把它
用作避免随意扣“造假”帽子的严格判定框架。

### 10.1 当前不能成立的指控

- **Fabrication：未成立。** 本提交没有新实验数据；抽核论文与数值均存在；§1 哈希真实。
- **Falsification：未达到可裁定门槛。** 有错误状态/计数，但尚无证据证明故意、明知或鲁莽地改变/遗漏
  记录以误导；团队同时主动披露大量不利结果和 pending 状态。
- **Plagiarism：无证据。** 本轮未发现无署名挪用。

因此不得写“团队已学术造假”或“已证欺诈”。

### 10.2 已成立的高风险 QRP / research-record 缺陷

| 风险 | 本轮证据 | 严重度 |
|---|---|---|
| 完成度膨胀 | 43 non-empty fields 写成 43 discrepancies；11 个 None 也计问题 | 高 |
| 证据等级膨胀 | abstract/composite rows 写 `CLAIM_LOCATED_FULLTEXT` | 高 |
| 分母不可审 | 11 extract drops 无逐项记录 | 高 |
| 身份计数越规则 | 6 个无约定 canonical ID 仍计 RESOLVED | 中高 |
| provenance 复发 | 提交稿声称与 banner 同在 78d，实际在 f5 | 中高 |
| 前置状态提前 | owner 终验 pending，却写 `prerequisites_met` | 中 |
| 构念替换 | selection overlap 被命名为 `δ_corr` | 高（科学有效性） |

这些问题暂时更适合定性为 **systematic semantic/status inflation + inadequate audit trail**。
但本报告已经明确通知后，若团队仍继续使用“43 discrepancies / 35 fulltext / 92 resolved / prerequisites
met”而不加本报告指出的限定，或无法解释 11 个 drops，则风险会从 honest error/QRP 升级为“可能的
reckless misrepresentation”，届时应由独立 integrity reviewer 而非项目协调者判断是否启动正式调查。

### 10.3 为什么我没有把风险降成“只是写作问题”

这些标签直接控制：哪些身份被 kill、哪些方向进入 GPU 探索、是否宣称 novelty whitespace、owner 是否
签批。因此它们会改变研究决策，不是排版瑕疵。Stage-1A 同样必须严肃处理。

---

## 11. 建议保留并深化的 proposal / 探索方向

本轮不应只剩“继续补表”。下面五个方向能把整改转化为真正的 Stage-1 知识增益。

### Proposal A — 从 scorer agreement 转向 conditional complementarity

核心问题：在存在 H(c) 的 item 上，同核音频信号是否提供外部文本信号没有的**正确性增量**？

检查点：

- A/B 各自的 Recovery、PCS、rho、regret；
- A错B对/B错A对的条件概率；
- 在 difficulty、score margin、headroom 分层后的 error correlation；
- 一个不读 gold 的 router 是否能用可观测特征预测“该信谁”；
- router upper bound 与可部署 router 的差距。

这比“两个选择是否一样”更接近 strict-I2 的科学生死问题。

### Proposal B — Audio-grounding sensitivity surface

不要只做一次 shuffle。构造 correct/mismatched/silence/hard-negative audio 的分层曲线，观察 scorer rank、
margin、Recovery 和最终 U 如何变化。目标不是证明模型“听见了”，而是判断音频信息是否**因果性改变了
候选质量排序**。

### Proposal C — Supply-response decomposition，而非两点移动

固定 selector、固定预算，分解：

```text
c -> candidate coverage/diversity -> H(c)
c -> proxy validity -> rho(c)
c -> cost/latency
```

先在 Stage-1B 用少量、预先固定的 supply levels 检查是否存在非平凡趋势；若只有任意两点差异，不足以
成为 I4。后续 proposal 应问“哪类 supply 属性可增量预测 H/rho”，而不是只问“换 c 会不会变”。

### Proposal D — Exact occupancy 与 method-family occupancy 双层 survey

每个候选同时维护：

- exact conjunction occupant；
- operator-family occupant；
- domain-transfer ancestor；
- metric/accounting ancestor；
- negative/failure neighbor。

这能防止一方面把分立组件拼成“已占据”，另一方面又用过窄合取制造“空白”。最终 novelty 必须说明
相对 method family 的新预测/新约束，而不是仅说明完整字符串没出现。

### Proposal E — Agentic loop vs one-shot selector 的等预算判别

这是 UMBRELLA 最值得保留的问题：在相同模型调用、token、工具调用和候选预算下，advantage-guided next
action 是否比一次性 BoN/MBR/rerank 多产生效用；增益来自扩池、修订、工具新信息还是更好的选择？
它不属于当前四探针，但应在 Stage-1C dossier 中作为独立候选，而不是被 same-selector contract 强行
压成池内选择。

---

## 12. 详细整改计划（不改旧史料，新增 successor 工件）

### Gate A — 零 GPU、先修 research record

1. 新增 submission provenance correction：拆分 evidence anchor 与 submission anchor。
2. 产出 census v2：`source_cluster` 与 `paper_work` 分表；P-0016 一对二；P-0084 数字指纹解析；补作者、
   canonical ID policy、版本、URL、content hash、review status。
3. 产出 claim ledger v2：一 claim×一 work×一 evidence span；综合推理另表；禁止复合行继承最高 grade。
4. 产出 11 个 extract drops 清单；不可恢复的逐项标记。
5. 把 discrepancy 改为枚举状态并重算 headline。
6. 产出 identity-contract amendment：拆 `selection_overlap/error_corr/decorrelation`，重写 P-γ kill-if；
   owner 重新签 exact hash。
7. C1/C4 owner integrity acknowledgement 与 probe authorization 分签。

**Gate A 验收**：另一 reviewer 随机抽 10 个 census works + 全部 MATERIAL/CRITICAL discrepancy + 全部
unreachable/abstract-only 承重行；发现 1 个同类错误则扩大到对应 strata 全量。

### Gate B — Round-2 查询前

1. 提交实际 query strings、数据库接口、日期、limit、语言和 seed papers；
2. 用 PRESS 六项检查查询，保存 reviewer 反馈；
3. 增加 domain-native venues 与 disconfirming/alias lanes；
4. 冻结筛选规则例子、双审样本、冲突处理；
5. 冻结机械 stop rule 和 trace-vs-rerun 状态；
6. 运行 P0-R8 最小 validator。

### Gate C — Stage-1B 开机前

1. 用非研究 dev item 完成 echo-logprob/API smoke；
2. 冻结 model/build/prompt/code/item IDs/n/seeds/temperature/c1/parse/failure manifest；
3. 改 P-γ 为 audio-grounding + conditional complementarity；
4. MBR 主臂使用可比 utility，WER 只作 sensitivity；
5. P-δ 固定一个 c1，并明确只是 necessary-condition probe；
6. 从 publication holdout 移走 Stage-1B 样本；
7. owner 对 exact manifest 单独签批。

### Gate D — 运行后、Stage-1C 前

1. 全部尝试、失败、fallback、timeout、invalid parse 入 attempt registry；
2. 报告每格 H/rho/regret/Recovery/PCS 与输入敏感性，不做显著性结论；
3. 任何未预注册分支标 `EXPLORATORY_POST_HOC`；
4. 将 survey 与 probe 的证据分开评级；
5. Stage-1C dossier 对每个候选给 proceed/pivot/kill 和反事实解释，不自动滚入 Stage-2。

---

## 13. 给下一位 AI/协调者的机器可读验收块

```yaml
review_verdict: RETURN_FOR_MAJOR_REVISION
current_stage: Stage-1A
required_next_state: P0_REMEDIATION_IN_PROGRESS

round2_search:
  authorized: false
  reason:
    - instantiated_queries_not_frozen
    - stop_rule_not_mechanical_enough
    - second_screen_plan_absent
    - identity_contract_delta_corr_invalid

stage1b:
  authorized: false
  reason:
    - owner_signoff_pending
    - integrity_prerequisites_bundled_with_protocol_signoff
    - p_gamma_construct_invalid
    - p_delta_c1_unfrozen_and_inference_overbroad
    - exact_run_manifest_absent
    - publication_holdout_contamination_risk

p0r_status:
  R1: CLOSED_FOR_PRIOR_DEFECT_WITH_NEW_PROVENANCE_FINDING
  R2: PARTIAL
  R3: PARTIAL_MATERIAL_DEFECTS
  R4: CLOSED_STRUCTURE_ONLY
  R5: PARTIAL_OPERATIONAL_SUPERSESSION
  R6: REOPENED_PARTIAL_DELTA_CORR
  R7: PARTIAL
  R8: NOT_DONE

integrity:
  fabrication: NOT_ESTABLISHED
  falsification: NOT_ESTABLISHED
  plagiarism: NO_EVIDENCE_FOUND
  intent: NOT_ASSESSABLE
  qrp_risk: HIGH
  independent_integrity_signoff: PROHIBITED_UNTIL_GATES_A_B

accepted_reviewer_dispositions:
  P0084: "map to arXiv:2606.04730 in census v2 using Table-3 numeric fingerprint"
  P0016: "split one source cluster into two paper works"
  within_logged_scope_contest: ACCEPTED_RETROSPECTIVELY_AS_GOOD_FAITH_REVIEWER_INDUCED_WORDING
  permanent_flow_counts_contest: ACCEPTED_AS_PERMANENT_FAILURE_NOT_ETERNAL_ACTION_ITEM
  rounds_6_7_8_rhetoric_contest: PARTIALLY_ACCEPTED
  global_token_logic_contest: ACCEPTED_IDENTITY_INDEXED_SOLUTION_PREFERRED

do_not_claim:
  - P0_R_COMPLETE
  - 92_EXACT_RESOLVED_WORKS_UNDER_PRIOR_RULE
  - 35_FULLTEXT_VERIFIED_LOAD_BEARING_CLAIMS
  - 43_DISCREPANCIES
  - PREREQUISITES_MET_FOR_STAGE1B
  - DELTA_CORR_MEASURED_BY_SELECTION_OVERLAP
  - SCIENTIFIC_SATURATION
  - NOVELTY_ESTABLISHED
```

---

## 14. 最终博导意见

团队这一轮最值得肯定的，不是工件数量，而是他们确实发现并公开了会伤害自己论证的错误；这使“有意
造假”目前缺少证据。最需要严厉否定的，也不是 Stage-1A 尚未收敛，而是又一次把**字段非空、单遍
AI、owner 待签、部分全文**包装成接近闭环的数字。这个习惯若不通过 schema 和 validator 根治，后续
再多 survey 只会生产更多不可依赖的精确数字。

正确路线不是停止探索，而是先把“paper 是谁、claim 是什么、证据在哪、谁核过、哪些被丢、哪个观测
能推出哪个判据”六件事彻底分开。完成 Gate A/B 后，Round-2 值得运行；完成 Gate C 后，四探针也值得
运行。当前版本则不应获准执行。
