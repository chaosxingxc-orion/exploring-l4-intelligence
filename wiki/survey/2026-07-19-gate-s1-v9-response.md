---
artifact_id: "GATE-S1-V9-RESPONSE-2026-07-19-01"
title: "v9 复审回应信（MAJOR-2 尾项窄整改包;Stage-1B 签署申请——按评审 §10-10 立即申请）"
date: 2026-07-19
addressee: "Gate S1 评审人 / 评委"
review_ref: "wiki/2026-07-19-system-first-research-proposal-v9-stage1a-doctoral-review.md（審 v9@bb3e2c3,被审件 blob 80bd820722）"
remediation_commits: "2e13d5e(评审归档+第十一轮核验台账) → 本批窄整改 commit（blob 见 §5;无新 proposal——遵评审 §10-1「不要宏大重写」）"
stage_account: "current_activity_stage = Stage-1A survey-ready gate（尾门）;new_model_touches_since_gate_freeze = 0（起算 af96a89）;cumulative_model_touches = 非零（四仓 union v2 在册）;legacy_experiments = INHERITED_PRIOR_EXPOSURE"
attestation: "本整改批 discovery_queries_executed = 0;research-model/smoke 运行 = 0（联网活动仅评审供给十篇引文核验,access log = survey/2026-07-19-sf-access-log-v9-review-verification.jsonl）"
format_note: "八字段逐 finding;DISPUTE 计数 = 0（本信 finding 集合内——连续第三轮零实质异议;另附一条 provenance 澄清小事实项 §2-d）"
---

<!-- release_binding: {"source": "docs/checks/2026-07-19-sf-identity-taxonomy-v5-test.json", "reward_guided": "6/11", "rq_sys_compatible": "5/11", "method_candidate": "0/11", "reward_guided_selection": "4/11", "trajectory_pool": "2/11"} -->

# v9 复审回应信（窄整改包）

## 0. 一览与机器数字（读者可见表 = 生成块,由 checker 重渲染整块比对——E5 子门由此关闭）

<!-- generated_headline_begin -->
| 派生量 | method-path 分母 | unique-work 分母 |
|---|---|---|
| is_reward_guided | 6/11 | 4/8 |
| is_rq_sys_control_compatible | 5/11 | 4/8 |
| is_project_method_candidate | 0/11 | 0/8 |
| reward_guided_selection | 4/11 | 3/8 |
| strict∧reward∧pool (trajectory) | 2/11 | 1/8 |
<!-- generated_headline_end -->

| Finding | Disposition | 状态 |
|---|---|---|
| 单一 Gate MAJOR（本轮 finding 集合内;MAJOR-2 尾项:E1–E5） | ACCEPT（5/5 亲手复现,含 REQ_FIELDS=14 计数错误） | 清零（P0-A/B/C 逐项,验收全红→修复后全绿） |
| P1 四篇 carry-forward | ACCEPT | 开局表 v4（含 SDiaReward「看过但遗忘」第六例登记） |
| §5.1 GEM 去重 / §5.2 书目自包含 | ACCEPT | GEM↔arXiv 绑定;书目改生成件（65 条,重跑零 diff） |
| §7.2 措辞降级 | ACCEPT | 采评审给定表述;计数以机器 REQ_FIELDS 为源 |
| P2 双平台留痕 | ACCEPT | 平台戳双副本+聚合相等断言 CONFIRMED |

## 1. Finding Gate MAJOR（E1–E5）— 八字段

- **Disposition**: ACCEPT。五反例全部亲手复现（内存内新行流程,零文件改动）;「15 承重字段」
  确为计数错误（机器实数 14）。
- **Root cause**: 行级合同被散文外推为全字段合同;行哈希被误当 schema validator（它只防
  盖章后漂移,不防盖章前错入）;突变集未覆盖「新行第一次编码即错」的正常流程。
- **Changed artifact + schema**（受影响 = `sf_identity_taxonomy_v5_test.py`/
  `sf_release_binding_check.py`/schema-v2 sidecars ×8/coding v6 生成件/
  `sf_dual_platform_check.py` 新增）:
  - **P0-A**:validator 强制边结构合同（use∈signal.uses / right∈row.rights / 白名单——
    失败=承重行红,`valid_live_edges` 不再静默独裁 occupancy）;
  - **P0-B**:12 信号 × {form,lifecycle,uses} 显式字段绑定（同 quote 可复用,绑定显式+
    程序值绑定）;signal evidence 纳入页码检查;**pN 必附非空锚点**;`pdf_page` kind 落实;
  - **P0-C**:读者可见 headline 表 = 生成块（本信 §0）,checker 用 `render_headline()` 从
    持久化输出重渲染整块比对;双负 fixture 自测。
- **正/负控输入与预期-实际输出（评审验收逐项）**:
  - E1（边用途翻转,合法重算行哈希）→ validator `edge-use-not-in-signal` **红** ✓（修复前
    validate=0/reconcile=0 复现在案）;
  - E2（signal evidence `p9999`）→ `page-token-without-anchor`/页码检查 **红** ✓;
  - E3（范围内裸 `p1`）→ `page-token-without-anchor` **红** ✓;
  - E4（signal form 翻转留原 locator）→ `evidence-value-mismatch:signal:…:form` **红** ✓
    ——三者均在 restamp 新行流程下由证据/schema 检测器拦截,**不依赖行哈希**（评审 §10-2）;
  - E5'（隐藏块不动、生成块内数字手改）→ `generated headline block differs` **红** ✓;
  - **第 12 行通用测试**（评审 §10-3):无逐 ID 期望的合成新行——好行净/E1 式坏边行被通用
    validator 单独拒绝 ✓;
  - V8 敏感面突变集扩至 **17 类**全红（模拟盖章副本+基线净断言维持）。
- **Machine check and exact result**: 合同测试 **12/12 双平台**（nt/Py3.14.3 与
  posix/Py3.12.3,occupancy 相等经 `sf_dual_platform_check.py` 断言 CONFIRMED——平台戳
  双副本互不覆盖,评审 P2 建议照办）;release binding（含生成块合同）PASS;单写字节等同 OK。
- **New derived numbers**: 无变化（§0 生成块 = 机器渲染;本信散文不另手抄数字）。
- **Residual / 未覆盖限制**: 锚点检索窗为 N±1 页（arXiv 封面页偏移容差,如实declared）;
  absence 条目语义真值仍由「存在性+值绑定+行哈希+独立裁决」四层承载;信号拆分粒度judgment
  由裁决制度承载。

## 2. Finding P1/P2 — 文献 carry-forward（八字段要点）

- **Disposition**: ACCEPT ×4（P1）+ ACCEPT ×6（P2）;十篇 10/10 官方页反幻觉核验。
- **Changed artifact**: 开局表 v4（新日期件,v1–v3 字节不动）:
  a) **Mapping Smarter**（2025.emnlp-industry.75）→ 表 D new-info 边界（仓内
  correction-4/p0r8 在案坐实）;b) **ASR-TRA**（2603.05231）→ 表 D 测试时权重/prompt 更新
  边界（07-13 scout ledger 在案坐实,含作者元数据）;c) **Dual-Axis GRM**（2026.acl-long.6）
  + **SDiaReward**（2603.14889）→ 表 B 新增 **B-2 trained speech reward instrument 分节**
  （按您的明令标注 trained RM,永不入 TF-Strict 占据;SDiaReward 系我方 07-06 archive
  `eval-methodology.md` §13 全文裁定在案——**「看过但遗忘」第六例（归档件）,如实登记不称
  首次发现**）;d) P2 六篇 → 表 E 首批队列（各带首批检查点）;e) Reinforced Agent
  **GEM↔arXiv 去重绑定**（`2026.gem-main.13` 官方页核验一致,ACL 正式链接优先）。
- **（d）provenance 澄清（小事实项,非异议）**: Dual-Axis 论文真实、角色定性我方完全认同;
  唯您所称「仓内 2026-07-06 reward survey 已读过」经我方定向检索未能坐实——07-06/07-14
  在案的是同聚簇 SpeechJudge-GRM/GSRM/UniSRM/SDiaReward,未见本篇。已照登记
  （provenance = REVIEWER_KNOWN_ITEM）,请您确认或给 locator,我方即按实改注。
- **Residual**: 表 D/E 新增项元数据于 Stage-1B fetch 时按 sidecar 链补全。

## 3. Finding §5.2 — 书目自包含

- **Disposition**: ACCEPT（「自包含」名不副实属实——A.1/A.2/A.4 回查 v8）。
- **Changed artifact**: `scripts/survey/sf_bibliography_generator.py` →
  `wiki/survey/2026-07-19-sf-bibliography-v1.md`——**机器生成**（从 v8/v9 钉定 blob 抽取+
  本轮核验补充;URL 级去重;65 条七角色;重跑零 diff）。与 P0-C 同一新纪律：**读者可见内容
  机器生成,散文只指向生成件**。
- **Residual**: 队列条目（登记待读）作者元数据于 fetch 时补全,生成器如实标注。

## 4. Finding §7.2 — 措辞降级

- **Disposition**: ACCEPT。整改期措辞采您给定表述;修复完成后的新真值 = 本信 §1 逐项验收
  +机器输出;「15」计数错误以 amendment-15 §2 为更正正典（v9 钉定件不改字节）。
- **Residual**: 无。

## 5. 签署申请（按您 §10-10 立即申请,不再延迟）

- `discovery_queries_executed = 0` 维持;`new_model_touches_since_gate_freeze = 0`;
- 修复 commit 与逐文件 blob 见随附 registry 更新与本批 commit 记录;信号绑定 delta 经隔离
  非实现者代理增量裁决（结果载于 amendment-15 §6 与 sidecar provenance）;
- 按 §9 放行矩阵:四项 FAIL 子门（E1 schema/E2·E4 值绑定/E3 锚点/E5 正文绑定）验收证据
  逐项在案（修复前红的复现记录 + 修复后绿的机器输出）;P1 四项已登记;
- **申请签署 Stage-1B survey execution**。签署后 owner 执行批准（owner 承重行抽查权于
  签署时行使）,第一条 systematic query 即 Stage-1B 起点;Stage-1B 全程不运行研究模型或
  smoke,产出仅限检索/去重/获取/证据分级/编码/裁决/占据图/负结果地图/饱和记录（您 §6.2
  边界逐字采纳）。
