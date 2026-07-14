---
protocol_id: SURVEY-PROTO-2026-07-15-01
title: Round-2 可回放检索协议 v2（实例化预注册——零查询执行；press-check 待过）
date: 2026-07-15
stage: Stage-1A（P1 序列 round-2 protocol instantiation；Gate B 门 G2–G5）
status: PREREGISTERED_PRESS_REVISED_PENDING_SIGNOFF
press_feedback: "docs/checks/2026-07-15-round2-press-feedback.md（PRESS review 2026-07-15 → PRESS_REVISE；7 fixes HIGH-1/HIGH-2/MOD-3/MOD-4/MINOR-5/6/7 已全部应用于本版，见 §13.3）"
supersedes: wiki/2026-07-14-round2-search-protocol-v1.md（SURVEY-PROTO-2026-07-14-02，骨架；本件为其实例化）
instantiates_gates: [ROUND2-G2, ROUND2-G3, ROUND2-G4, ROUND2-G5]
gate_dependencies:
  ROUND2-G1: SIGNED  # δ_corr identity-contract amendment №1 EFFECTIVE @ 0a5e108（见 candidate_definitions 段）
  ROUND2-G6: PASSING_BLOCKING_PREFLIGHT  # P0-R8 validator scripts/integrity/p0r8_state_gate.py exit 0（coordinator run 2026-07-15，docs/checks/2026-07-15-p0r8-gate-run-coordinator.txt）；§14 阻断性前置，执行首日复跑
queries_executed: 0
queries_executed_note: "ZERO QUERIES EXECUTED. 本文件仅为预注册；任何 exact_query 均未运行，无 raw response、无 search_results、无 screening_decision 产生。press-check 已于 2026-07-15 执行（PRESS_REVISE→7 fixes 已应用）；第一条查询须在 reviewer search-design 签署 + owner 资源批准 + G6 validator 复跑 exit 0 之后，且执行首日回填 date_range.to 与 run manifest。"
candidate_definitions_commit: dce5c79
candidate_definitions:
  frozen_source: wiki/2026-07-14-identity-contracts-v1.md
  frozen_commit: dce5c79
  frozen_blob_sha256: 1338f6b16f5409022b0a8193c5e71729dcf65ba78f1fa41b3645e642efc208b1
  verify_cmd: "git show dce5c79:wiki/2026-07-14-identity-contracts-v1.md | sha256sum"
  amendment: wiki/2026-07-14-identity-contracts-amendment-1.md
  amendment_id: CONTRACT-AMEND-2026-07-14-01
  amendment_effective_commit: 0a5e108
  amendment_blob_sha256: d9e2ab5e3b34ecaac0d4e9920831964d234ebe0d00a93b7f45310407baae23b8
  amendment_effect: "δ_corr 拆名（selection_overlap≠error_corr≠complementary_gain）；strict-I2 kill-if 重写为两独立测试；same-selector contract 不再覆盖 UMBRELLA 环内动作。检索期身份定义只读，任何新增限定词走合同 §8 日志 + 本协议 RETROSPECTIVE 双登记。"
preregistration_note: "本协议在任何 round-2 查询执行前写就并提交。PRESS 六项（PRISMA-S 留存 + PRESS 敌意预检）已于 2026-07-15 执行，返回 PRESS_REVISE，7 fixes 已全部应用（§13.3）；reviewer search-design 签署与 owner 批准之前，status 不得升为 ACTIVE；沉默不等于批准（复审 §8.2 缺陷 2）。"
deviations: []
generated_by: "Claude Fable 5 主会话子代理（依 round2-search-protocol-v1 骨架 + 复审 §8.2 十缺陷 + §8.3 门 G2–G5 实例化）"
verified_by: []
---

# Round-2 可回放检索协议 v2（实例化预注册）

> 本件把 v1 骨架（SURVEY-PROTO-2026-07-14-02）逐条实例化，兑现博导第三轮复审
> `2026-07-14-p0r-progress-submission-doctoral-adversarial-rereview.md` §8.2 的**十条缺陷**与
> §8.3 的执行门 **ROUND2-G2…G5**。**未执行任何查询**——所有 `planned_queries` 均为预注册字符串。

## 0. 预注册宣誓（零查询）

- **`queries_executed: 0`。** 本文件是冻结意图，不是执行记录：无 `search_events.jsonl`、无
  `search_results.jsonl`、无 `screening_decisions.jsonl`、无 raw capture 产生。
- **执行首日回填项**（运行前登记，晚填=RETROSPECTIVE，禁）：每 lane `date_range.to`、`run_id`、
  `agent_id`、frozen run manifest hash。`date_range.from = null`（开放下界）；`date_range.to = 2026-07-15`
  为预注册占位，执行首日以实际日期覆盖并登记。
- **`deviations: []`**：执行期任何偏离本协议逐条追加于此（含身份限定词变更须同步合同 §8 日志）。

## 1. 研究问题（对齐冻结合同 + 修正案 №1）

- **RQ1**：strict-I2 / I3-combined / I4 / UMBRELLA 的**合取对象**是否存在未登记的单一实例直接占据者？
  （合取量词规则：单一实例实现完整合取才算占据；分立组件各自被占不构成合取占据。）
- **RQ2**：I4 的「label-free × 供给轴 × 音频域」收窄空白，是否被 test-time-scaling / VLA 邻域的新工作
  （L-NEW 八篇）侵入？特别针对 2606.02981（labeled predictor）对 I4「label-free 增量预测」检查点的威胁。
- **RQ3**：Proposal E（供给选择作为决策问题）的最近邻 CoVer(2602.12281) 之外还有多近的邻居？
- **RQ4（新增，反收方偏置）**：把团队自造术语（ρ/headroom/供给/兑现率）**全部去掉**后，method-family
  是否已在标准名下（test-time scaling / best-of-N / verifier-guided decoding / prompt-context selection）
  被占据？（→ 三条 disconfirming lanes L-DIS-A/B/C。）

## 2. 冻结身份定义（只读引用，检索中不修改）

唯一定义源 = `2026-07-14-identity-contracts-v1.md`（FROZEN，续41，**commit dce5c79**，git-blob
sha256 `1338f6b16f5409022b0a8193c5e71729dcf65ba78f1fa41b3645e642efc208b1`）**叠加**修正案 №1
（`2026-07-14-identity-contracts-amendment-1.md`，`CONTRACT-AMEND-2026-07-14-01`，EFFECTIVE @ 0a5e108，
blob sha256 `d9e2ab5e3b34ecaac0d4e9920831964d234ebe0d00a93b7f45310407baae23b8`）。

检索期对任何身份**新增/收窄/放宽限定词** = 违规 → 合同 §8 日志 + 本协议 `deviations` 双登记。
`δ_corr` 语义以修正案 A 节为准（`selection_overlap` 仅描述量、不作 kill 判据；`error_corr` /
`complementary_gain` 为独立价值判据）——本协议筛选不据此改身份。

## 3. 引擎与领域 venue 覆盖表（修正 §8.2 缺陷 4 + 缺陷 3）

**可复现性两分类（缺陷 3——web 检索只可 trace-replay，绝不可 rerunnable-identical）**：

- `trace_reconstructable`：结果因个性化/本地化/索引更新不可字节复现，但**原始响应存档 + 事件登记**
  可回放当时轨迹。
- `query_rerunnable`：同 query 在稳定 API/结构化索引上可返回近似同一结果集（版本随索引更新仍标注）。

| 引擎 / venue | 接口 | operation 用途 | 复现分类 | 可达性说明（v1 §4 继承） |
|---|---|---|---|---|
| WebSearch（主广度） | UI | SEARCH（发现） | **trace_reconstructable** | 个性化/时效——永标 trace-only，绝不称 rerunnable |
| arXiv listing + HTML 镜像（ar5iv / arxiv HTML / hf papers） | api + FETCH | SEARCH（listing）/ FETCH（全文） | query_rerunnable（listing）/ trace（镜像抓取） | arxiv.org/abs 直连 WebFetch 常 Socket-closed——失败登记 FAILED，换镜像补查 |
| Semantic Scholar（Graph API/页） | api | SEARCH / CITATION_BACKWARD / CITATION_FORWARD | query_rerunnable | references/citations 端点供 chase；空闲免费额度 |
| dblp | api | SEARCH（书目/venue 消歧） | query_rerunnable | 作者/venue 精确 |
| OpenReview | api | SEARCH（ICLR/NeurIPS/COLM 投稿+评审） | query_rerunnable | 预印/在审 venue |
| **ACL Anthology**（aclanthology.org 检索） | UI/静态 | SEARCH（*CL/EMNLP/Interspeech-adjacent NLP） | query_rerunnable | 领域 venue，v1 缺——本轮补 |
| **ISCA Archive**（isca-archive.org） | UI/静态 | SEARCH（Interspeech/SLT-adjacent 语音） | query_rerunnable（静态页） | 语音领域 venue；直连偶阻，WebSearch site: 兜底 |
| **IEEE Xplore**（经 WebSearch `site:ieeexplore.ieee.org`） | UI（间接） | SEARCH（ICASSP/TASLP） | **trace_reconstructable** | 无免费 API——只经 WebSearch site: 查询，标 trace-only；**已操作化路由（PRESS HIGH-2b）**：L-SAT-1、L-SAT-5、L-SAT-6 各含 ≥1 条 site: 查询 |
| **Crossref REST**（free tier） | api | SEARCH（DOI 解析/书目补全）/ MANUAL_IMPORT | query_rerunnable | 免费无 key；venue-native DOI 补全 |
| ~~OpenAlex API~~ | — | **排除** | — | 2026-01 起 key 门控 + 计费（续37 评审核验事实）——不使用 |

**每 lane 引擎下限（缺陷 7 停轮前提）**：每条 keyword/alias 查询至少在 **≥2 个独立 query_rerunnable
引擎**执行；chase 用 Semantic Scholar references/citations 为主、dblp/Crossref 补书目。
IEEE/WebSearch 的 trace-only 结果不得单独支撑饱和判定。

## 4. 纳排规则 + 裁决样例（修正 §8.2 缺陷 6——主观词须各带 2 正 2 反 + 冲突规则）

> 样例一律用本项目台账真实论文（claim-ledger-v2 / census-v2）。

### IN-01 —— 冻结模型 K 池上的 label-free 选择/验证/弃权/供给操作 → 入格评

- **正例 1**：`mbr-asr 2510.19471`——冻结 Whisper 上 label-free MBR 固定 K=64 池内选择（CL2-0002）。**纳入**。
- **正例 2**：`scaling-auditory 2503.23395`——冻结 audio-LLM 自身 audio-conditioned beam log-lik 池内选择
  （CL2-0003）。**纳入**。
- **负例 1**：`ProGRes 2409.00217`——候选**扩池**（生成新候选）而非固定池内选择（CL2-0060 reanchor）→
  归 **comparator，不作占据者**（EX 见 §3.4 分类法：扩池≠池内选择）。
- **负例 2**：`TAP-GER 2309.15649`——生成池外纠错文本（out-of-pool generation，CL2-0062 reanchor）→
  **comparator，不作 I1 占据**。

### IN-02 —— test-time-scaling 规律类 + 含 oracle-vs-realized 或供给/条件轴 → 入 I4 邻域

- **正例 1**：`JudgeBoN 2603.12520`——定义 Recovery = oracle-over-random 兑现比（= 我方 rho_pool，CL2-0010）。**纳入 I4 邻域**。
- **正例 2**：`Snell compute-optimal TTS 2408.03314`（L-NEW-1）——compute-optimal 分配的 scaling 规律。**纳入 I4 邻域**。
- **负例 1**：`2606.02981`（labeled validation predictor，L-NEW-6）——预测量**用标签**；触发 I4 合同级
  检查点（label-free 增量预测）→ 标 **THREATENS_I4_CHECKPOINT**，入邻域但非 label-free 占据者。
- **负例 2**：纯难度/K/温度单轴 scaling 曲线（无供给类型轴，如 divsampling 2025 类）→ **邻域而非 I4 对象**（合同 §5 负测试）。

### EX-01 —— 核心方法需权重更新（LoRA/FT/RL 训练）→ 排除（保留为 comparator，标注）

- **正例 1（正确排除）**：`AQA-TTRL 2510.05478`——test-time RL **改权重**（CL2-0030）→ 排除，标 comparator。
- **正例 2（正确排除）**：`AuTAgent 2602.13685`——GRPO **训练** tool policy（CL2-0032）→ 排除，标 comparator。
- **反例 1（不得误排）**：`inference-time-reward-hacking 2506.19248`——"reward/RL" 措辞指**代理奖励模型**，
  策略 π_ref **冻结**、推理时 BoN/HedgeTune 选择（CL2-0001）→ **不排除**，是 Goodhart-概念占据者。
- **反例 2（不得误排）**：`slam-aac 2410.09503`——**选择器**是冻结 CLAP（captioner 带 LoRA 但非选择器，
  CL2-0020）→ **不排除**，作 external-frozen 机制占据者，标注「生成器 LoRA、选择器冻结」。

### EX-02 —— 纯文本且无可迁移机制主张 → 记 RELATED_ONLY，不入 kill 格

- **正例 1（正确 RELATED_ONLY）**：`Reflexion 2303.11366`——纯文本自反思，无音频/选择机制迁移（CL2-0025）。
- **正例 2（正确 RELATED_ONLY）**：`Training-Free-GRPO 2510.08191`——纯文本、与我方**名字碰撞**但机制不迁移（CL2-0026）。
- **反例 1（不得降 RELATED_ONLY）**：`JudgeBoN 2603.12520`——虽纯文本，但 Recovery=rho **度量可直接迁移**
  → 保留为 metric ancestor（入格）。
- **反例 2（不得降 RELATED_ONLY）**：`IAD 2504.01931`——虽纯文本，但 loop-vs-BoN 坍缩风险机制**可迁移**
  到 UMBRELLA → 保留为 collapse-risk ancestor（入格）。

### 冲突规则

任一结果被两个规则拉扯，或单审判 `UNCERTAIN` → **不即时裁定**：进入 §5 第二审
（独立 agent），仍分歧 → 写 `adjudication_log.jsonl`（`result_id / rule_a / rule_b /
screener_1 / screener_2 / adjudicator / resolution / reason`），保留待 owner/reviewer。
排除一律带 reason code（IN-01/IN-02/EX-01/EX-02 或 UNCERTAIN）。

## 5. 第二审计划（修正 §8.2 缺陷 8）

**强制独立第二 agent 复筛的三类**：

1. **全部**潜在 `DIRECT` / `PARTIAL` 裁决（占据/近占据——最高杠杆，无一例外双审）；
2. **全部** fulltext 阶段的排除（防止把不利占据者在全文阶段静默排掉）；
3. title/abstract 阶段排除的 **10% 随机样本**（seed 预登记；查有无系统性误排）。

- 第二 agent 的 `agent_id` 与首筛 `agent_id` 不同（模板 §0.8：`generated_by ≠ verified_by`）。
- 分歧 → `adjudication_log.jsonl` 记录 + resolution；**发现一处同类误判 → 该 strata 扩至全量复筛**
  （对齐 Gate A 验收「发现 1 个即扩全量」纪律）。
- 第二审样本 seed、随机抽样命令与结果均入 replay bundle，机器可重算。

## 6. 机械停轮规则 + yield curve（修正 §8.2 缺陷 7）

**一轮的定义**（预声明，可机械执行）：
> 某 lane 的**完整 `planned_queries` 集**在 **≥2 个独立引擎**上执行一遍（§3 引擎下限），
> 且其 backward/forward chase 种子各追一层。

**停轮判据**：
- 某 lane 连续**一整轮**产出 **0 条新 DIRECT/PARTIAL 候选**，且 `yield_curve`（每轮 new-candidate 计数）
  已登记 → 该 lane 标 `LOCALLY_SATURATED_WITHIN_PROTOCOL`。
- `yield_curve` 逐轮记入 `flow_report.yaml`：`{lane_id, round_n, new_direct, new_partial, new_related, engines_hit}`。
  停轮必须展示 yield 单调降至 0；**无 yield 曲线不得声称饱和**。
- **引擎不可达**（API 漏索引/网络失败）→ **换独立引擎补查 + 记 gap note**，**绝不写 saturated**
  （防 API 漏索引伪饱和）。失败事件保留在分母。
- **收方偏置禁令**：找到支持「空白」的结果后**不得**提前停轮；找到占据者后**不得**加限定词续命
  （合同 §8 + 修正案）。
- 全局收轮：全部 lane 达 `LOCALLY_SATURATED_WITHIN_PROTOCOL` **或**显式 gap 登记后。最强允许结论
  = `NO_DIRECT_MATCH_WITHIN_LOGGED_SCOPE`@94簇（+ 强制伴随 token），**不得**写裸 `saturated`/`novel`/`complete`。

## 7. 语言规则（修正 §8.2 缺陷 9）

- 默认 `languages: [en]`（Stage-1A 预算所限）；**例外 L-SAT-7 = multilingual**（non-English SER 是其对象）。
- **非英文命中 → `awaiting_classification`，绝不静默丢弃**：记入 `screening_decisions.jsonl`
  （`decision: UNCERTAIN, reason_code: LANG_AWAITING_CLASSIFICATION`），保留 title/URL/venue，
  留待有语言能力的后续 pass 或 Stage-2。非英文记录消失 = 分母缺陷，禁止。

## 8. 版本冻结与 content-hash 继承 census v2（修正 §8.2 缺陷 10）

- 新 work **一律经 census v2 schema 入格**（`paper_works.jsonl` 字段）：
  `work_id, cluster_id, ledger_key, status, arxiv_id, doi, venue_native_id, title, first_author,
  authors_full, year, latest_version, version_date, canonical_url, venue, resolution_source,
  resolution_basis, content_hash, review_status, corrections, notes`。
- **fail-closed**：canonical ID（arxiv_id / doi / venue_native_id 至少一）缺失 → work 状态
  `IDENTITY_UNRESOLVED`，**不得计入任何 exact-works 数**，不得进 kill/coverage 矩阵
  （对齐 census-v2 W-0014 处置）。
- **版本必须 pin**：`latest_version` + `version_date` 双非空方可支撑 CLAIM_VERIFIED；版本变化产生新证据，
  不静默覆盖。`content_hash = UNFETCHED_THIS_ROUND` 的行不得升 FULLTEXT_OPENED。
- 与 census v1 的 94 簇 join 用 `paper_id`/`cluster_id`（辅 `ledger_key`）；P-0016 一对二、
  P-0084=2606.04730（NUMERIC_FINGERPRINT_TABLE3）等既有解析继承。
- 证据等级沿用模板 §2.6 五级（DISCOVERED / ABSTRACT_VERIFIED / FULLTEXT_OPENED / CLAIM_VERIFIED /
  REPRODUCED）；snippet-only 不得升 FULLTEXT/CLAIM_VERIFIED；综合行不继承最强子证据等级
  （取最低必要证据或 `SYNTHESIS_PENDING_REVIEW`）。

## 9. 事件捕获（构造性可回放——继承 v1 §6 硬约束）

每次检索/抓取一行 `search_events.jsonl`（模板 §2.2 全字段；`operation ∈
{SEARCH | FETCH | CITATION_BACKWARD | CITATION_FORWARD | MANUAL_IMPORT}`；chase 事件用 CITATION_*，
不混入 SEARCH 计数——续38「305 查询」混数教训）；raw response 存
`wiki/survey/replay/ROUND2-2026-07/raw/` + sha256；结果宇宙 `search_results.jsonl`（含 rank）；
筛选轨迹 `screening_decisions.jsonl`（决定 + reason code + screener_id）。**失败事件保留在分母；
无 raw capture 的查询 = 不存在（不得计数）。**

---

## 10. Lane 块（嵌入 YAML；全 lane 实例化）

> 计数：**21 lanes** = 7 L-SAT 检索 + 2 L-SAT 核验 + 8 L-NEW + 1 L-CHASE + 3 L-DIS。
> **105 条预注册 exact query strings = 102 mandatory + 3 optional 单语 native-language probes（L-SAT-7）**
> （核验型 lane 无 query，代之以 item 清单 + 完成判据）。PRESS 修订前基线 82 条
> （+16 arXiv cat-filter，+3 IEEE site: 路由，+1 MOD-4 供给查询；HIGH-1 对 mandatory 净零）。
> 每检索型 lane 4 类基础查询：keyword family / alias family / backward-chase seed / forward-chase seed；
> **engines 含 arXiv_listing 的检索 lane 另有 1 条 cat-filter 变体**（`cat:eess.AS OR cat:cs.SD OR cat:cs.CL`，
> PRESS HIGH-2a；核验型 L-SAT-8/9 无 keyword query，不适用）。
>
> **查询卫生规则（PRESS MINOR-7）**：
> 1. 复合专名在支持 exact-phrase 的引擎上加引号："best-of-N"、"AIR-Bench"、"URO-Bench"、"Spoken-SQuAD"。
> 2. **bare "TTS" 永不作查询词**（与 text-to-speech 冲名）——一律写全 "test-time scaling"；
>    本条把既有纪律显式化，chase 注释中的旧缩写已同步改写。
> 3. **Qwen 代际消歧**：Qwen-Audio（2023 初代）≠ Qwen2-Audio（2024）≠ Qwen2.5-Omni（2025）≠ Qwen3-Omni——
>    查询点名某代模型须用精确代际名；命中其他代际仍按 §4 规则筛选，不因代际错配丢弃。

### 10.1 L-SAT-1…9（scout-ledger-round2.json `round2_saturation_targets` 九条，逐条照录不改写）

```yaml
- lane_id: L-SAT-1
  verbatim_target: "SER + SLU-intent selective-prediction / self-consistency oracle curves on frozen omni (crema-d/meld/esd/minds14/slurp/speech-massive) — UNDERSEARCHED cells"
  purpose_disconfirm: "若存在冻结 omni 上 SER/SLU-intent 的 label-free 自洽/选择性预测 oracle 曲线占据者，则 I1/I2 的 SER/SLU 未占格与 I4 SER/SLU 空白被推翻。"
  engines: [WebSearch, semantic_scholar, ISCA_archive, ACL_anthology, dblp]
  date_range: {from: null, to: 2026-07-15}
  languages: [en]
  planned_queries:
    - 'speech emotion recognition SER "selective classification" self-consistency selection frozen audio language model oracle CREMA-D MELD accuracy'
    - 'spoken language understanding intent "best-of-N" BoN best-of-n sampling confidence calibration frozen SLURP MINDS-14 MINDS14 no fine-tuning'
    - 'site:ieeexplore.ieee.org speech emotion recognition spoken language understanding N-best selection re-ranking frozen ICASSP TASLP'  # PRESS HIGH-2b：IEEE 路由
    - "CITATION_BACKWARD seed=2602.03873 via Semantic Scholar references (jia decoding-ambiguous SER test-time-scaling ancestors)"
    - "CITATION_FORWARD seed=2602.03873 via Semantic Scholar citations (who extends jia SER BoN to SLU/intent)"

- lane_id: L-SAT-2
  verbatim_target: "spoken-QA/dialogue/agent frozen-omni self-consistency / K-pool selection on VoiceBench/spoken-squad/uro-bench/vocalbench — thinnest F2 cell"
  purpose_disconfirm: "若冻结 omni 在 spoken-QA/对话基准上 label-free K 池选择已被占据，则 F2 最薄格（spoken-QA frozen-omni selection）非 undersearched。"
  engines: [WebSearch, semantic_scholar, ACL_anthology, arXiv_listing, dblp]
  date_range: {from: null, to: 2026-07-15}
  languages: [en]
  planned_queries:
    - 'spoken question answering frozen audio LLM self-consistency majority vote VoiceBench VocalBench "URO-Bench" UROBench'
    - 'speech dialogue "best-of-N" BoN best-of-n sampling selection re-ranking "Spoken-SQuAD" frozen omni without training rerank'
    - '(cat:eess.AS OR cat:cs.SD OR cat:cs.CL) AND all:"spoken question answering" AND all:"self-consistency" AND all:selection'  # PRESS HIGH-2a：arXiv cat-filter
    - "CITATION_BACKWARD seed=2604.25591 via Semantic Scholar references (walking-through-uncertainty spoken-QA ancestors)"
    - "CITATION_FORWARD seed=2604.25591 via Semantic Scholar citations (spoken-QA selective-prediction / K-pool extensions)"

- lane_id: L-SAT-3
  verbatim_target: "per-benchmark oracle-over-pool + rho curves on our exact audio benchmarks (MMAU/MMAR/AIR-Bench/MMSU/BBAudio) on a WEIGHT-FROZEN omni"
  purpose_disconfirm: "若已有论文在 MMAU/MMAR/AIR-Bench/MMSU/BBAudio 上对冻结 omni 报 oracle-over-pool + 兑现率曲线，则 I4 audio 实例化不再 undersearched。"
  engines: [WebSearch, semantic_scholar, arXiv_listing, ACL_anthology, dblp]
  date_range: {from: null, to: 2026-07-15}
  languages: [en]
  planned_queries:
    - 'MMAU MMAR "AIR-Bench" "AIR Bench" MMSU BBAudio "Big Bench Audio" oracle accuracy best-in-pool sampling frozen audio language model coverage'  # PRESS MOD-3：BBAudio 补入（承重数据集）
    - 'audio understanding pass@k oracle upper bound realized fraction frozen Qwen2-Audio MMAU BBAudio no training'
    - '(cat:eess.AS OR cat:cs.SD OR cat:cs.CL) AND (all:MMAU OR all:MMAR OR all:MMSU OR all:"AIR-Bench" OR all:BBAudio) AND all:oracle'  # PRESS HIGH-2a
    - "CITATION_BACKWARD seed=2503.23395 via Semantic Scholar references (scaling-auditory TTC ancestors)"
    - "CITATION_FORWARD seed=2503.23395 via Semantic Scholar citations (audio test-time-compute follow-ups on MMAU/MMAR)"

- lane_id: L-SAT-4
  verbatim_target: "inference-time reward-overoptimization / Goodhart over SPEECH/omni N-best or K-sample pools (M4 cells nearly all NO_DIRECT_MATCH)"
  purpose_disconfirm: "若 Goodhart/over-optimization 拐点已在 speech/omni N-best 或 K 池上被检测，则 I3 的 Goodhart-on-speech 空白被推翻。"
  engines: [WebSearch, semantic_scholar, arXiv_listing, dblp, OpenReview]
  date_range: {from: null, to: 2026-07-15}
  languages: [en]
  planned_queries:
    - 'reward over-optimization Goodhart "best-of-N" BoN best-of-n speech audio N-best caption selection inference-time tipping point'
    - 'reward hacking inflection "best-of-N" ASR "automatic speech recognition" "speech recognition" audio LLM proxy reward frozen policy over-optimization'
    - '(cat:eess.AS OR cat:cs.SD OR cat:cs.CL) AND (all:"reward hacking" OR all:"over-optimization" OR all:Goodhart) AND (all:"best-of-N" OR all:"N-best")'  # PRESS HIGH-2a
    - "CITATION_BACKWARD seed=2506.19248 via Semantic Scholar references (inference-time reward-hacking / HedgeTune ancestors)"
    - "CITATION_FORWARD seed=2506.19248 via Semantic Scholar citations (HedgeTune/BoP applied to speech or audio)"

- lane_id: L-SAT-5
  verbatim_target: "ST-specific conformal / abstention bound to ST N-best selection (M3 ST = NO_DIRECT_MATCH)"
  purpose_disconfirm: "若已有 ST 专属 conformal/弃权绑定到 ST N-best 选择，则 I3 的 ST-abstain 空白被推翻。"
  engines: [WebSearch, semantic_scholar, ACL_anthology, arXiv_listing, dblp]
  date_range: {from: null, to: 2026-07-15}
  languages: [en]
  planned_queries:
    - 'speech translation "speech recognition" conformal prediction abstention N-best selection COMET quality estimation risk control'
    - 'spoken translation selective prediction reject option "best-of-N" BoN best-of-n CoVoST FLEURS uncertainty bound "automatic speech recognition"'
    - '(cat:eess.AS OR cat:cs.SD OR cat:cs.CL) AND all:"speech translation" AND (all:conformal OR all:abstention) AND all:"N-best"'  # PRESS HIGH-2a
    - 'site:ieeexplore.ieee.org speech translation conformal prediction abstention "N-best" selection ICASSP TASLP'  # PRESS HIGH-2b：ST conformal（PRESS 原文编号 L-SAT-6，本协议为 L-SAT-5）
    - "CITATION_BACKWARD seed=2510.19471 via Semantic Scholar references (mbr-asr ST/MBR ancestors)"
    - "CITATION_FORWARD seed=2410.21485 via Semantic Scholar citations (SpeechQE ST QE + abstention extensions)"

- lane_id: L-SAT-6
  verbatim_target: "audio-specific conformal prediction on GENERATION (not classification) applied to Qwen-Audio/omni"
  purpose_disconfirm: "若音频生成式（非分类）conformal 已应用于 Qwen-Audio/omni，则 I3 conformal-on-generation-frozen-omni 非空白。"
  engines: [WebSearch, semantic_scholar, arXiv_listing, ISCA_archive, dblp]
  date_range: {from: null, to: 2026-07-15}
  languages: [en]
  planned_queries:
    - 'conformal prediction generative sequence ASR "automatic speech recognition" "speech recognition" captioning audio language model coverage guarantee WER'
    - "risk-controlling prediction set open-ended audio generation Qwen-Audio conformal risk control"
    - '(cat:eess.AS OR cat:cs.SD OR cat:cs.CL) AND all:"conformal prediction" AND (all:generative OR all:generation) AND (all:audio OR all:speech)'  # PRESS HIGH-2a
    - 'site:ieeexplore.ieee.org conformal prediction generative speech recognition audio risk control ICASSP TASLP'  # PRESS HIGH-2b（字面编号 L-SAT-6 亦路由，覆盖两种读法）
    - "CITATION_BACKWARD seed=ernez23a (PMLR v204 pp.16-35) via Crossref+Semantic Scholar references (conformal ASR ancestors)"
    - "CITATION_FORWARD seed=ernez23a conformal-ASR via Semantic Scholar citations (generative-audio conformal follow-ups)"

- lane_id: L-SAT-7
  verbatim_target: "non-English SER selection venues; 2026 speech-LLM 'listen-then-rerank' self-consistency preprints"
  purpose_disconfirm: "若非英文 SER 选择或 2026 'listen-then-rerank' 自洽预印占据 SER/audio selection 格，则相关未占格被推翻；multilingual 例外防语言盲区。"
  engines: [WebSearch, semantic_scholar, ISCA_archive, ACL_anthology, arXiv_listing]
  date_range: {from: null, to: 2026-07-15}
  languages: [multilingual]  # v1 §3 明示例外：non-English SER 是本 lane 对象
  planned_queries:
    - 'non-English multilingual speech emotion recognition SER "selective classification" rerank re-ranking selection frozen audio LLM 2026 listen-then-rerank'
    - "Mandarin German Spanish French speech emotion recognition reranking selection frozen audio LLM non-English"  # PRESS HIGH-1(a)：英文点名目标语言（取代混语 mega-query）
    - '(cat:eess.AS OR cat:cs.SD OR cat:cs.CL) AND all:"speech emotion" AND (all:multilingual OR all:Mandarin OR all:German OR all:Spanish) AND (all:rerank OR all:selection)'  # PRESS HIGH-2a
    - "CITATION_BACKWARD seed=2602.03873 via Semantic Scholar references (multilingual SER test-time-scaling refs)"
    - "CITATION_FORWARD seed=2602.03873 via Semantic Scholar citations (non-English SER test-time-scaling citations)"
  optional_native_language_probes:  # PRESS HIGH-1(b)：WebSearch 单语探针——一条仅一种语言，optional（不计 mandatory；命中走 §7 awaiting_classification 流程）
    - "语音情感识别 冻结模型 重排序 选择"  # zh
    - "Emotionserkennung aus Sprache Reranking"  # de（PRESS 更正：Emotionserkennung，非 Spracherkennung）
    - "reconocimiento de emociones en el habla reranking selección modelo congelado"  # es

# ——— 核验型 lane（v1 §3 例外：chase 与饱和规则不适用；完成判据 = FULLTEXT_OPENED/CLAIM_VERIFIED 或 RAW_EVENT_UNAVAILABLE）———

- lane_id: L-SAT-8
  lane_type: VERIFICATION
  verbatim_target: "full-text re-verify of ABSTRACT/SCOUT rows before Stage-2 lock"
  purpose_disconfirm: "把 9 篇 AB/SC 承重行升级为 FULLTEXT/CLAIM_VERIFIED（或如实标不可达），防止摘要级证据支撑占据/无匹配裁决。"
  engines: [arXiv_listing, WebSearch, semantic_scholar, ISCA_archive, ACL_anthology]
  date_range: {from: null, to: 2026-07-15}
  languages: [en]
  item_list:  # 逐篇 FETCH 全文；无 planned_queries
    - {id: AudioToolAgent-2510.02995, current_grade: AB}
    - {id: Agent-Omni-2511.02834, current_grade: SC}
    - {id: JitRL-2601.18510, current_grade: SC}
    - {id: IRO-2506.17828, current_grade: AB}
    - {id: AQA-TTRL-2510.05478, current_grade: AB/FT-mixed}
    - {id: Audio-CoT-2501.07246, current_grade: SC}
    - {id: sttfm-rescore-2409.16654, current_grade: SC}
    - {id: Omni-Reward-2510.23451, current_grade: SC}
    - {id: ProGRes-2409.00217, current_grade: AB}
  completion_criteria: "每 item：固定版本全文 FETCH+存档 → FULLTEXT_OPENED；对承重主张给页/节/表定位 → CLAIM_VERIFIED；不可达则 RAW_EVENT_UNAVAILABLE + 缺失范围/影响。综合行不继承最强子证据等级。"

- lane_id: L-SAT-9
  lane_type: VERIFICATION
  verbatim_target: "RE-VERIFY the 2 failed citations (both NOT_RESOLVED_THIS_ROUND due to network)"
  purpose_disconfirm: "确认两条 UNVERIFIED-CITATION 是真实论文还是不可解析；区分『网络失败未决』与『引文确认不可解析』。"
  engines: [WebSearch, semantic_scholar, Crossref, arXiv_listing]
  date_range: {from: null, to: 2026-07-15}
  languages: [en]
  item_list:
    - {id: semantic-confidence-aac-2512.10170, prior_status: NOT_RESOLVED_THIS_ROUND}
    - {id: brace-2512.10403, prior_status: NOT_RESOLVED_THIS_ROUND}
  completion_criteria: "≥2 独立引擎确认 source_resolves true/false。resolves=true → ABSTRACT_VERIFIED 或 CLAIM_VERIFIED；resolves=false（≥2 引擎均不解析）→ CITATION_UNRESOLVED_CONFIRMED（区别于网络失败的 NOT_RESOLVED）；仍仅网络失败 → RAW_EVENT_UNAVAILABLE。"
```

### 10.2 L-NEW-1…8（round2_new_targets.jsonl 八篇；摘要级入格 + backward/forward chase 一层 + 方法别名）

```yaml
- lane_id: L-NEW-1
  target_id: "2408.03314"
  target_title: "Snell — compute-optimal test-time scaling (title AS_GIVEN_BY_REVIEW, 待独立核)"
  purpose_disconfirm: "根族 compute-optimal TTS 若已含供给/条件轴 oracle-realized，则 I4 method-family 更强占据（RQ2/RQ4）。"
  engines: [arXiv_listing, semantic_scholar, WebSearch, dblp]
  date_range: {from: null, to: 2026-07-15}
  languages: [en]
  planned_queries:
    - "Snell 2024 Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters"
    - "compute-optimal test-time scaling verifier tree search sequential revision budget allocation"
    - '(cat:eess.AS OR cat:cs.SD OR cat:cs.CL) AND all:"test-time compute" AND all:compute-optimal'  # PRESS HIGH-2a
    - "CITATION_BACKWARD seed=2408.03314 via Semantic Scholar references"
    - "CITATION_FORWARD seed=2408.03314 via Semantic Scholar citations (audio/speech applications of compute-optimal test-time scaling)"

- lane_id: L-NEW-2
  target_id: "2505.11730"
  target_title: "VG-Search: Rethinking Optimal Verification Granularity (AS_GIVEN_BY_REVIEW)"
  purpose_disconfirm: "验证粒度最优化若覆盖冻结模型 audio-grounded 选择的粒度轴，则 strict-I2/I3 判据被邻域侵入。"
  engines: [arXiv_listing, semantic_scholar, WebSearch, OpenReview]
  date_range: {from: null, to: 2026-07-15}
  languages: [en]
  planned_queries:
    - 'VG-Search Rethinking Optimal Verification Granularity "best-of-N" process reward'
    - "verification granularity process reward model step-level vs outcome-level test-time selection"
    - '(cat:eess.AS OR cat:cs.SD OR cat:cs.CL) AND all:"verification granularity" AND all:"best-of-N"'  # PRESS HIGH-2a
    - "CITATION_BACKWARD seed=2505.11730 via Semantic Scholar references"
    - "CITATION_FORWARD seed=2505.11730 via Semantic Scholar citations"

- lane_id: L-NEW-3
  target_id: "2605.10991"
  target_title: "Test-Time Personalization: Diagnostic Framework and Probabilistic Fix for Scaling Failures (AS_GIVEN_BY_REVIEW)"
  purpose_disconfirm: "最近方法学：BoN 曲线分解 + oracle-vs-realized。若其分解=我方兑现率对象，则 I4 度量/分解贡献非新（RQ2）。"
  engines: [arXiv_listing, semantic_scholar, WebSearch, OpenReview]
  date_range: {from: null, to: 2026-07-15}
  languages: [en]
  planned_queries:
    - 'Test-Time Personalization Diagnostic Framework Probabilistic Fix Scaling Failures "best-of-N"'
    - '"best-of-N" curve decomposition oracle realized selection failure probabilistic diagnostic'
    - '(cat:eess.AS OR cat:cs.SD OR cat:cs.CL) AND all:"test-time personalization" AND all:"scaling failures"'  # PRESS HIGH-2a
    - "CITATION_BACKWARD seed=2605.10991 via Semantic Scholar references"
    - "CITATION_FORWARD seed=2605.10991 via Semantic Scholar citations"

- lane_id: L-NEW-4
  target_id: "2512.02008"
  target_title: "The Art of Scaling Test-Time Compute for Large Language Models (AS_GIVEN_BY_REVIEW)"
  purpose_disconfirm: "TTC scaling 配方若含供给类型分层的兑现规律，则 I4 增量预测贡献被占据（RQ2/RQ4）。"
  engines: [arXiv_listing, semantic_scholar, WebSearch, dblp]
  date_range: {from: null, to: 2026-07-15}
  languages: [en]
  planned_queries:
    - "The Art of Scaling Test-Time Compute for Large Language Models recipe verifier"
    - "test-time compute scaling recipe verifier sampling budget allocation predictor"
    - '(cat:eess.AS OR cat:cs.SD OR cat:cs.CL) AND all:"test-time compute" AND all:recipe'  # PRESS HIGH-2a
    - "CITATION_BACKWARD seed=2512.02008 via Semantic Scholar references"
    - "CITATION_FORWARD seed=2512.02008 via Semantic Scholar citations"

- lane_id: L-NEW-5
  target_id: "2506.17811"
  target_title: "RoboMonkey — VLA inference scaling law (CoRL 2025, PMLR v305 pp.3200-3217)"
  purpose_disconfirm: "VLA 推理 scaling law 属 UMBRELLA 邻域（advantage→action）；若其 = 冻结策略 reward-guided next-action，则 UMBRELLA 组件邻域更近。"
  engines: [semantic_scholar, WebSearch, Crossref, dblp]
  date_range: {from: null, to: 2026-07-15}
  languages: [en]
  planned_queries:
    - "RoboMonkey vision-language-action inference scaling law CoRL 2025 verifier best-of-N action"
    - "VLA action selection test-time scaling verifier robot manipulation frozen policy"
    - "CITATION_BACKWARD seed=2506.17811 (PMLR v305) via Crossref+Semantic Scholar references"
    - "CITATION_FORWARD seed=2506.17811 via Semantic Scholar citations"

- lane_id: L-NEW-6
  target_id: "2606.02981"
  target_title: "Predicting Inference-Time Scaling Gains from Labeled Validation-Set Output Statistics"
  purpose_disconfirm: "THREATENS_I4_CHECKPOINT：labeled predictor 迫使 I4 兑现 label-free 增量预测检查点（合同 §5）。若 label-free 变体已存在→I4 增量贡献被占。"
  engines: [arXiv_listing, semantic_scholar, WebSearch, OpenReview]
  date_range: {from: null, to: 2026-07-15}
  languages: [en]
  planned_queries:
    - "Predicting Inference-Time Scaling Gains from Labeled Validation-Set Output Statistics"
    - 'predict "best-of-N" gain label-free output statistics scaling predictor difficulty entropy agreement'
    - '(cat:eess.AS OR cat:cs.SD OR cat:cs.CL) AND all:"inference-time scaling" AND all:predict AND all:gains'  # PRESS HIGH-2a
    - "CITATION_BACKWARD seed=2606.02981 via Semantic Scholar references"
    - "CITATION_FORWARD seed=2606.02981 via Semantic Scholar citations (label-free predictor variants)"

- lane_id: L-NEW-7
  target_id: "2607.05391"
  target_title: "LLM-as-a-Verifier — recovers oracle headroom, text agents (AS_GIVEN_BY_REVIEW)"
  purpose_disconfirm: "文本 agent 上 verifier 兑现 oracle 头空 = I1/I4 度量占据。若迁移到音频/omni→strict-I2/I4 邻域更近。"
  engines: [arXiv_listing, semantic_scholar, WebSearch, dblp]
  date_range: {from: null, to: 2026-07-15}
  languages: [en]
  planned_queries:
    - 'LLM-as-a-Verifier recover oracle headroom text agents "best-of-N" 2026'
    - "verifier recovers oracle gap selection language model judge realized fraction agent"
    - '(cat:eess.AS OR cat:cs.SD OR cat:cs.CL) AND all:verifier AND all:oracle AND all:"best-of-N"'  # PRESS HIGH-2a
    - "CITATION_BACKWARD seed=2607.05391 via Semantic Scholar references"
    - "CITATION_FORWARD seed=2607.05391 via Semantic Scholar citations"

- lane_id: L-NEW-8
  target_id: "2602.12281"
  target_title: "CoVer — verifier selects rephrased instruction + action chunks (NEAREST NEIGHBOR to Proposal E)"
  purpose_disconfirm: "Proposal E 最近邻威胁：供给侧选择（指令改写 + 动作块）。若 CoVer = 供给选择作为决策问题的通用形态→Proposal E/I4 供给选择贡献被占（RQ3）。"
  engines: [arXiv_listing, semantic_scholar, WebSearch, OpenReview]
  date_range: {from: null, to: 2026-07-15}
  languages: [en]
  planned_queries:
    - "CoVer verifier selects rephrased instruction action chunks supply-side selection test-time"
    - "instruction rephrasing selection verifier action chunk test-time policy improvement frozen"
    - '(cat:eess.AS OR cat:cs.SD OR cat:cs.CL) AND all:verifier AND all:rephrased AND all:instruction'  # PRESS HIGH-2a
    - "CITATION_BACKWARD seed=2602.12281 via Semantic Scholar references"
    - "CITATION_FORWARD seed=2602.12281 via Semantic Scholar citations (supply-side selection at inference — Proposal E neighbors)"
```

### 10.3 L-CHASE（对 claim-ledger-v2 全部 DIRECT 占据者做 forward chase：谁引用它们做同类事）

```yaml
- lane_id: L-CHASE
  lane_type: FORWARD_CHASE
  purpose_disconfirm: "对每个已登记 DIRECT 占据者做 forward citation chase；若后继工作把该占据者的机制推进到我方合取身份（如 frozen-omni 同核曲面 / supply 分层 / Goodhart-on-speech），则相应『无匹配』裁决被推翻。"
  engines: [semantic_scholar, WebSearch, dblp]  # chase 主用 Semantic Scholar citations 端点
  date_range: {from: null, to: 2026-07-15}
  languages: [en]
  seed_occupants_from_claim_ledger_v2:
    - {id: "2510.19471", role: "I1 ASR/ST DIRECT (mbr-asr, CL2-0002/0017)"}
    - {id: "2503.23395", role: "I1/I2 audio-understanding DIRECT (scaling-auditory, CL2-0003)"}
    - {id: "2602.03873", role: "I1/I2 SER DIRECT (jia decoding-ambiguous, CL2-0007)"}
    - {id: "2604.25591", role: "I3-abstain DIRECT (walking-through-uncertainty, CL2-0008)"}
    - {id: "ernez23a (PMLR v204)", role: "I3-conformal ASR DIRECT (CL2-0009)"}
    - {id: "2410.09503", role: "AAC mechanism DIRECT (slam-aac / CLAP-Refine, CL2-0020)"}
    - {id: "2603.12520", role: "rho/Recovery metric DIRECT-text (JudgeBoN, CL2-0010)"}
    - {id: "2503.22712", role: "conformal SER OCCUPANCY-trained (CL2-0021)"}
    - {id: "2506.19248", role: "Goodhart concept DIRECT-text (CL2-0001)"}
    - {id: "2510.02995", role: "UMBRELLA-as-system OCCUPANCY (AudioToolAgent, CL2-0029)"}
  planned_queries:
    - "CITATION_FORWARD seed=2510.19471 via Semantic Scholar citations (label-free ASR/ST selection successors)"
    - "CITATION_FORWARD seed=2503.23395 via Semantic Scholar citations (frozen audio-LLM K-pool selection successors)"
    - "CITATION_FORWARD seed=2602.03873 via Semantic Scholar citations (frozen-ALM SER BoN/verifier successors)"
    - "CITATION_FORWARD seed=2604.25591 via Semantic Scholar citations (frozen-omni selective-prediction successors)"
    - "Crossref DOI-resolution first: resolve ernez23a (PMLR v204 pp.16-35) to its DOI via Crossref REST, then CITATION_FORWARD via Semantic Scholar citations using the resolved DOI (conformal ASR successors; PMLR key not directly feedable to S2 — PRESS MINOR-6)"
    - "CITATION_FORWARD seed=2410.09503 via Semantic Scholar citations (CLAP-Refine audio-grounded selection successors)"
    - "CITATION_FORWARD seed=2603.12520 via Semantic Scholar citations (Recovery/rho-metric successors incl. audio)"
    - "CITATION_FORWARD seed=2503.22712 via Semantic Scholar citations (conformal SER successors)"
    - "CITATION_FORWARD seed=2506.19248 via Semantic Scholar citations (Goodhart/HedgeTune successors incl. speech)"
    - "CITATION_FORWARD seed=2510.02995 via Semantic Scholar citations (audio agentic orchestration successors)"
  note: "本 lane 与 L-SAT-* thematic forward-chase 有意重叠（同一占据者可被两 lane 追）；dedup_priority 处理结果重复，不重复计数占据者。"
```

### 10.4 Disconfirming lanes（新增≥3，反收方偏置；RQ4）

```yaml
- lane_id: L-DIS-A
  disconfirming_type: "method-family occupancy WITHOUT our coined terms"
  purpose_disconfirm: "去掉团队自造术语（ρ/headroom/供给/兑现率），用标准名（test-time scaling / best-of-N / self-consistency / verifier-guided decoding）搜 method-family。若 method-family 已在 speech/audio 上被占，则我方 novelty 只能是 method 内的新预测/新约束，不能靠术语求交造空白。"
  engines: [WebSearch, semantic_scholar, arXiv_listing, ACL_anthology, dblp]
  date_range: {from: null, to: 2026-07-15}
  languages: [en]
  planned_queries:
    - '"best-of-N" BoN best-of-n verifier-guided decoding test-time scaling speech audio without training accuracy gain oracle'
    - 'self-consistency sampling reranking re-ranking inference-time compute audio LLM PRM ORM "process reward model" coverage gap upper bound'  # alias family: 我方术语的同义替换
    - '(cat:eess.AS OR cat:cs.SD OR cat:cs.CL) AND (all:"best-of-N" OR all:"test-time scaling" OR all:"self-consistency") AND (all:speech OR all:audio)'  # PRESS HIGH-2a
    - "CITATION_BACKWARD seed=2408.03314 via Semantic Scholar references (test-time-scaling method-family root, no-our-terms lens)"
    - "CITATION_FORWARD seed=2503.23395 via Semantic Scholar citations (audio TTC named as test-time scaling / best-of-N)"

- lane_id: L-DIS-B
  disconfirming_type: "trainable-neighborhood (RL/FT versions of our objects — comparator candidates)"
  purpose_disconfirm: "枚举 I1–I4 选择器的 RL/FT/LoRA 训练版对应物。它们非冻结占据者，但必须登记为 comparator，否则会把『冻结版无匹配』误当成 method 空白（EX-01 保留纪律）。"
  engines: [WebSearch, semantic_scholar, arXiv_listing, ACL_anthology, OpenReview]
  date_range: {from: null, to: 2026-07-15}
  languages: [en]
  planned_queries:
    - "test-time reinforcement learning audio LLM reward speech GRPO fine-tune selection reranker trained PRM ORM"
    - 'LoRA reranker re-ranking trained verifier "process reward model" PRM "outcome reward model" ORM speech N-best generative error correction reward model audio'  # alias family
    - '(cat:eess.AS OR cat:cs.SD OR cat:cs.CL) AND (all:"reinforcement learning" OR all:GRPO OR all:"reward model") AND (all:speech OR all:audio) AND all:rerank'  # PRESS HIGH-2a
    - "CITATION_BACKWARD seed=2510.05478 via Semantic Scholar references (AQA-TTRL trained-audio ancestors)"
    - "CITATION_FORWARD seed=2602.13685 via Semantic Scholar citations (AuTAgent trained tool-policy audio successors)"

- lane_id: L-DIS-C
  disconfirming_type: "supply-selection alternative names (prompt/context/instruction selection at inference)"
  purpose_disconfirm: "供给侧选择的替代名（prompt selection / context selection / demonstration selection / instruction optimization / RAG context ranking）在冻结模型上是否已占据 I4 供给轴与 Proposal E 的决策形态（RQ3/RQ4）。"
  engines: [WebSearch, semantic_scholar, ACL_anthology, arXiv_listing, dblp]
  date_range: {from: null, to: 2026-07-15}
  languages: [en]
  planned_queries:
    - "prompt selection context selection instruction optimization inference-time frozen model without training"
    - "demonstration selection exemplar selection in-context learning ICL example retrieval retrieval-augmented generation RAG context ranking test-time no gradient supply"  # alias family (PRESS MOD-3: full forms + ICL/exemplar)
    - "contextual biasing prompt selection context selection ASR speech frozen inference-time supply"  # PRESS MOD-4: audio-grounded supply family, aligns with 2509.19567 forward-chase
    - "CITATION_BACKWARD seed=2602.12281 via Semantic Scholar references (CoVer instruction-rephrase-selection ancestors)"
    - "CITATION_FORWARD seed=2509.19567 via Semantic Scholar citations (siskos contextual-biasing supply-ladder ASR successors)"
```

---

## 11. 去重与身份（继承 v1 §7）

`dedup_priority: [doi, arxiv_base_id, acl_anthology_id, venue_native_id, title_author_year]`
（模板 §2.5 + census-v2 venue_native_id）。新 work 先过 §8 census v2 canonical 流程再入格；跨 lane
只引同一 `paper_id`；与 census v1 94 簇 join 用 `paper_id`/`cluster_id`（辅 `ledger_key`）。

## 12. 产出与验收（继承 v1 §9）

replay bundle `ROUND2-2026-07`（模板 §2 全件）+ 更新 kill/coverage matrix v3（带限定词表）+
comparator seed cards（模板 §3.5 十二字段，达严格可比性前不称 SOTA cards）。验收 = 模板 §5 十二项
自动校验 + 独立 reviewer 盲重建五项（模板 §6）。检索执行者与筛选者身份逐事件登记。

## 13. Gate B 门 G2–G5 与 §8.2 十缺陷可追溯性

### 13.1 §8.3 门映射

| Gate | 要求 | 本协议落点 | 状态 |
|---|---|---|---|
| ROUND2-G1 | δ_corr 合同 amendment 已签 | 前置（修正案 №1 EFFECTIVE @0a5e108），本协议 §2 引用 | SATISFIED（外部） |
| ROUND2-G2 | instantiated protocol.yaml + exact queries 提交/hash | §10 全 lane 嵌入 YAML；104 exact query strings（PRESS 修订前基线 82，修订净增 22：cat-filter 变体/site: 路由/分语言探针/L-DIS-C 补族）；提交后取 blob hash | THIS_DOC |
| ROUND2-G3 | database/venue coverage 表已补 | §3（ACL Anthology / ISCA / IEEE / Crossref 补入；OpenAlex 排除；trace vs rerun 分类） | THIS_DOC |
| ROUND2-G4 | inclusion examples + second-screen plan 已补 | §4（IN/EX 各 2 正 2 反真实论文样例 + 冲突规则）+ §5（三类第二审） | THIS_DOC |
| ROUND2-G5 | stop rule 可机械执行 | §6（一轮定义 + yield curve + 引擎不可达换查 + 收方偏置禁令） | THIS_DOC |
| ROUND2-G6 | P0-R8 最小 validator 已通过 | 独立工件，非本协议（gate_dependencies: OUT_OF_SCOPE） | 外部待办 |

### 13.2 §8.2 十缺陷修复映射

| # | 缺陷（复审 §8.2） | 本协议修复 |
|---|---|---|
| 1 | 真正 query strings 不在被审协议中（推迟到未来 yaml） | §10 全 104 条 exact query 预注册入本件（含 PRESS 修订增补）；无推迟 |
| 2 | `DRAFT—无异议即生效` 不合格 | frontmatter `status: PREREGISTERED_PENDING_PRESS_CHECK`；§0/§1 明示需 press-check + reviewer 签署，沉默≠批准 |
| 3 | WebSearch 只 trace-replay 非 rerunnable | §3 每引擎 `trace_reconstructable` vs `query_rerunnable` 分类（WebSearch/IEEE=trace-only） |
| 4 | 数据源覆盖不贴语音/多模态 | §3 补 ACL Anthology / ISCA Archive / IEEE Xplore(site:) / Crossref；OpenAlex 排除 |
| 5 | RQ 偏向找完整合取占据者 | §1 RQ4 + §10.4 三条 disconfirming lanes（无术语 method-family / trainable 邻域 / 供给选择替代名） |
| 6 | IN/EX 主观词无 adjudication examples | §4 IN-01/IN-02/EX-01/EX-02 各 2 正 2 反真实论文样例 + 冲突规则 |
| 7 | 「连续两轮 chase 无新增」非稳定停止规则 | §6 定义一轮 = 完整 planned_queries×≥2 引擎；yield curve 登记；引擎不可达换查不写 saturated |
| 8 | 筛选只有 agent_id，无独立复核 | §5 全 DIRECT/PARTIAL + 全 fulltext 排除 + 10% 随机 title/abstract 排除 → 第二 agent；分歧入 adjudication log |
| 9 | 语言限制未说明 | §7 非英文 → `awaiting_classification` 不静默丢弃；L-SAT-7 multilingual 例外 |
| 10 | 版本冻结与 content hash 须继承 census v2 | §8 census v2 schema 入格 + fail-closed（canonical ID 缺→IDENTITY_UNRESOLVED 不计数） |

---

## 14. 执行前置（本协议不自我放行）

```yaml
preflight_gates_before_first_query:
  - press_check: "PRISMA-S 检索式留存 + PRESS 六项（RQ translation / Boolean-proximity / subject-headings / text-words / spelling / limits）敌意预检；reviewer 反馈存档"
  - reviewer_search_design_signoff: "独立 reviewer 对 search design 显式 active 签署（非沉默生效）"
  - owner_resource_approval: "owner 资源/治理批准（非科学终审）"
  - run_manifest_freeze: "执行首日冻结 run_id / agent_id / date_range.to / raw-capture 目录，回填后方可发首条 SEARCH"
status_gate: "以上未全绿前 status 不得升 ACTIVE；本文件 queries_executed 恒为 0 直至另开执行 bundle。"
```
