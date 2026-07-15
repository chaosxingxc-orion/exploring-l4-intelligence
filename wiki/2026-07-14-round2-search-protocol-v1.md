---
protocol_id: SURVEY-PROTO-2026-07-14-02
title: Round-2 可回放检索协议 v1（预注册——检索开始前冻结）
date: 2026-07-14
stage: Stage-1A（P1 序列 round-2 protocol freeze 步骤）
status: DRAFT — 提交即冻结意图；检索开始前若无 owner 异议即生效（非 owner 签批件，但先于任何查询提交入 git 以取得预注册时戳）
preregistration_note: "本协议在任何 round-2 查询执行前写就并提交；若有事后修订必须标 RETROSPECTIVE 并登记"
generated_by: "Claude Fable 5 主会话（基于可回放模板 §2.1 + 冻结身份合同）"
---

# Round-2 可回放检索协议 v1

## 1. 研究问题（对齐冻结合同）

- RQ1：strict-I2/I3-combined/I4/UMBRELLA 的合取对象是否存在未登记的直接占据者？（合取量词规则：
  单一实例实现完整合取才算占据）
- RQ2：I4 的「label-free × 供给轴 × 音频域」收窄空白是否被 test-time scaling/VLA 邻域的新工作侵入？
- RQ3：Proposal E（供给选择作为决策问题）的最近邻 CoVer 之外还有多近的邻居？

## 2. 身份定义（冻结引用，不在检索中修改）

以 `2026-07-14-identity-contracts-v1.md` 为唯一定义源（FROZEN，续41；
**candidate_definitions_commit = dce5c79**，git-blob sha256
`1338f6b16f5409022b0a8193c5e71729dcf65ba78f1fa41b3645e642efc208b1`）；检索期间对任何身份新增
限定词 = 违规（合同 §8 日志 + 本协议 RETROSPECTIVE 标记双重登记）。`deviations: []`（占位，
执行期偏离逐条登记于此）。

## 3. Lanes（9 既有饱和目标 + 8 新篇 + 追链）

- L-SAT-1..9：scout-ledger-round2.json 的 9 个 round2_saturation_targets（逐条照录，不改写）。
- L-NEW-1..8：`wiki/survey/replay/SURVEY-RESP-2026-07-14-01/round2_new_targets.jsonl` 的 8 篇（Snell 2408.03314 矩阵级入格、
  VG-Search 2505.11730、TTPersonalization 2605.10991、Art-of-TTS 2512.02008、RoboMonkey 2506.17811、
  2606.02981、LLM-as-a-Verifier 2607.05391、CoVer 2602.12281）——每篇：摘要级入格 + forward/backward
  citation chase 一层 + 方法别名查询。
- L-CHASE：对 claim-ledger v1 中全部 DIRECT 占据者做 forward chase（谁引用了它们做同类事）。
- **检索型 lane** 至少执行：关键词检索、backward chase、forward chase、作者/方法别名检索（模板
  §3.6）。**核验型 lane 例外**（L-SAT-8 九篇全文复核、L-SAT-9 两条失败引文复查）：完成判据=目标
  记录达 FULLTEXT_OPENED/CLAIM_VERIFIED（或登记不可达），chase 与饱和规则不适用。
- **全 lane 共享参数**：date_range = {from: null（开放）, to: 执行首日日期（运行前登记）}；
  languages = [en]（**L-SAT-7 例外：multilingual**——non-English SER 是其对象）；
  planned_queries：每 lane 首批种子查询在**任何查询执行之前**登记入运行实例 protocol.yaml
  （晚于执行才写=RETROSPECTIVE，禁）。

## 4. 数据库与引擎（登记可达性）

WebSearch（主）、arXiv listing/HTML 镜像（ar5iv/hf papers；arxiv.org 直连 WebFetch 常被阻断——
失败按事件如实登记 FAILED，换镜像补查）、Semantic Scholar 页、dblp、openreview。
**OpenAlex API 排除**（2026-01 起 key 门控+计费——续37 评审核验事实）。

## 5. 纳排规则（可机械执行）

- IN-01：提出/评测「冻结模型 K 池上的 label-free 选择/验证/弃权/供给操作」→ 纳入格评。
- IN-02：test-time scaling 规律类工作且含 oracle-vs-realized 或供给/条件轴 → 纳入 I4 邻域。
- EX-01：需权重更新的核心方法（LoRA/FT/RL 训练）→ 排除（保留为 comparator 候选，标注）。
- EX-02：纯文本且无可迁移机制主张 → 记 RELATED_ONLY 不入 kill 格。
- 排除必须带 reason code；UNCERTAIN 保留待双审。

## 6. 事件捕获（构造性可回放——本轮硬约束）

每次检索/抓取一行 `search_events.jsonl`（模板 §2.2 全字段：event_id/run_id/agent_id/
timestamp_utc 到秒/operation 按模板五枚举 **SEARCH | FETCH | CITATION_BACKWARD |
CITATION_FORWARD | MANUAL_IMPORT**（chase 事件用 CITATION_* 类,不得混入 SEARCH 计数——
续38「305 查询」混数教训）/exact_query/raw_response_path+sha256/status）；
raw response 原文存 `wiki/survey/replay/ROUND2-2026-07/raw/`；结果宇宙 `search_results.jsonl`
（每条返回结果含 rank）；筛选轨迹 `screening_decisions.jsonl`（决定+reason code+执行者）。
**失败事件保留在分母。** 无 raw capture 的查询 = 不存在（不得计数）。

## 7. 去重与身份

dedup 优先级：doi > arxiv_base_id > acl_anthology_id > title_author_year（模板 §2.5）；
新 work 一律先过 canonical census 流程（arXiv id+版本+日期）再入格；与 census v1 的 94 簇
join 用 **paper_id**（辅 ledger_key；census_records.jsonl 的实际字段——canonical_key 非字段名）。

## 8. 停止规则（预声明）

每 lane：连续两轮 backward/forward chase 无新增 DIRECT/PARTIAL 邻居 → 该 lane 标
LOCALLY_SATURATED_WITHIN_PROTOCOL；引擎不可达 → 换独立引擎补查，仍不可达则保留 gap，
**不得写 saturated**。全局：全部 lane 达标或显式 gap 登记后收轮。
**禁止**：找到支持空白的结果后提前停止（收方偏置）；找到占据者后加限定词续命（合同 §8）。

## 9. 产出与验收

replay bundle ROUND2（模板 §2 全件）+ 更新 kill/coverage matrix v3（带限定词表）+
comparator seed cards（12 字段，达严格可比性前不称 SOTA cards）。验收 = 模板 §5 十二项自动校验 +
独立 reviewer 盲重建五项（模板 §6）。检索执行者与筛选者身份逐事件登记（AI agent id）。
