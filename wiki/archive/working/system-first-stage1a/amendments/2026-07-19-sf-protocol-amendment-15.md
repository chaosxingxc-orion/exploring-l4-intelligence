---
artifact_id: "SF-PROTOCOL-AMENDMENT-15-2026-07-19-01"
title: "Amendment 15 — v9 复审(窄幅 WITHHOLD:MAJOR-1/-3 CLOSED,MAJOR-2 尾项)窄整改合同"
date: 2026-07-19
review_ref: "wiki/2026-07-19-system-first-research-proposal-v9-stage1a-doctoral-review.md（審 v9@bb3e2c3,blob 80bd820722）"
owner_ruling: "2026-07-19「Go」——全盘 ACCEPT;正文表生成块方案;Dual-Axis provenance 记 REVIEWER_KNOWN_ITEM 如实说明;书目生成式重复(集合=v8/v9 钉定附录闭包+本轮补充);窄整改后立即申请签署"
stage_account: "current_activity_stage = Stage-1A survey-ready gate（尾门）;new_model_touches_since_gate_freeze = 0（起算 af96a89）;cumulative_model_touches = 非零;legacy_experiments = INHERITED_PRIOR_EXPOSURE;本批 discovery_queries_executed = 0"
---

# Amendment 15：v9 复审窄整改合同

## §1 P0-A — 通用 validator 真正执行 signal/edge schema（已闭合）

**缺陷（E1,亲手复现）**：validate() 只查 signal 存在与可选 lifecycle 失配;`edge.signal_use
∉ signal.uses`、`right ∉ row.rights`、关系不在白名单三类结构矛盾被 `valid_live_edges()`
静默跳过——改变 occupancy 却不告诉编码者。**修复**：三类检查全部入 validator（失败=承重行
红,非静默降数）;**验收 E1**:STTS 边用途翻转在合法重算行哈希（新行流程）下由 validator 以
`edge-use-not-in-signal` 明确拒绝;**第 12 行通用测试**:无逐 ID 期望的合成新行——好行净、
E1 式坏边行被通用 validator 单独拒绝（评审 §10-3）。

## §2 P0-B — signal 证据从自由 locator 升级为字段绑定（已闭合）

**缺陷（E2/E3/E4,亲手复现）**：signal 的一个自由 locator 被散文宣称「同时支撑
form/lifecycle/uses」但程序只查文本存在;signal evidence 不走页码检查（`p9999` 可过）;
pN 锚点可选（范围内错误裸页码可过）;`pdf_page` kind 声明未实现。**修复**：
- 每信号 `claim_evidence{form,lifecycle,uses}` 显式声明「哪条引文支撑哪个值」（同 quote
  可复用,绑定必须显式）+ 程序值绑定（12 信号 × 3 字段全部落地）;
- signal evidence 与全部 locator 统一过页码检查;**pN 必附非空 ASCII 锚点**（无锚=红;
  锚点于 N±1 页文本内检索）;
- `pdf_page` evidence kind 落实（page∈范围+anchor 命中,含 incomplete/unreadable/
  out-of-range/anchor-missing 四类失败）;
- **计数更正**：行级 required 字段实数 = **14**（七 strict 位+visibility/topology/modality/
  horizon/rights/pool/policy）——v9 等件中「15」为计数错误,以本节为更正正典;信号级另有
  12 信号 × 3 字段绑定与逐边合同,总承重面以机器 `REQ_FIELDS`+validator 输出为措辞来源;
- **验收 E2/E3/E4**:全部在新行流程（restamp,行哈希合法）下由证据/schema 检测器拦截
  （`page-token-without-anchor`/`page-out-of-range`/`evidence-value-mismatch`）,不依赖
  行哈希;V8 敏感面突变集扩至 **17 类**。

## §3 P0-C — release binding 覆盖读者可见数字（已闭合）

**缺陷（E5,亲手复现）**：checker 只读隐藏机器块;正文 6/11 改 99/11 照过——「散文数字不可能
过期而不红」为超额保证。**修复（评审方案 2）**：读者可见 headline 表改为
`generated_headline_begin/end` 生成块,由 `render_headline()` 从持久化测试输出渲染（禁止手写数字入块）;
checker 对每个带块工件**重渲染并整块比对**;负 fixture 双份自测（错误声明值+手改块数字均
必须红）。**验收 E5'**:隐藏块不动、块内数字手改 → FAIL。

## §4 P1/P2 — 文献 carry-forward 与呈现（已闭合）

- **开局表 v4**（新日期件,v1–v3 字节不动）:表 D +Mapping Smarter（new-info 边界;仓内
  correction-4/p0r8 在案）+ASR-TRA（测试时权重/prompt 更新边界;07-13 scout ledger 在案）;
  表 B 新增 **B-2 trained speech reward instrument 分节**（Dual-Axis GRM+SDiaReward,
  评审明令标注 trained RM 永不入 TF-Strict 占据——SDiaReward 为 07-06 archive 在案的
  「看过但遗忘」第六例,如实登记）;表 A Reinforced Agent GEM↔arXiv 去重绑定;表 E +6
  （TangramSR/OrchRM/ToolRM/Agent-RRM/DuplexPO/Multi-Faceted,各带首批检查点）。十篇
  10/10 反幻觉核验（access log v9-review-verification）。
- **provenance 澄清（对评审的小事实项）**：Dual-Axis「仓内 07-06 已读」经定向检索未坐实
  （在案为同聚簇 SpeechJudge-GRM/GSRM/UniSRM/SDiaReward）——登记照做,provenance 记
  REVIEWER_KNOWN_ITEM,待评审确认或给 locator。
- **书目自包含（§5.2 required correction）**：`sf_bibliography_generator.py` 从 v8/v9
  **钉定 blob** 机器抽取 + 本轮核验补充 → `2026-07-19-sf-bibliography-v1.md`（65 条七角色,
  确定性重跑零 diff;读者可见书目自此为生成件——与 §3 同一纪律:**读者可见内容机器生成**）。

## §5 P2 双平台留痕（已闭合）

合同测试输出平台戳副本（`…-v5-test.{nt|posix}.json`,互不覆盖）+
`sf_dual_platform_check.py` 聚合断言（双份存在∧双 PASS∧occupancy 相等）。实测:nt/Py3.14.3
与 posix/Py3.12.3 → **CONFIRMED**。

## §6 增量裁决与门禁现值（收口时更新）

信号字段绑定 delta（12 信号 × 3 绑定+锚点化 locator）经隔离非实现者代理增量裁决——结果
并入本节;11 行行哈希随 delta 重盖章,provenance 载明 delta 裁决链。门禁现值:合同测试
**12/12 双平台**（V8=17 类敏感面突变,E1–E4 走新行流程由指定检测器拦截）;release binding
（生成块合同）PASS;dual-platform PASS;immutability/lint/单写字节等同全绿;
systematic query = 0;research-model/smoke = 0。
