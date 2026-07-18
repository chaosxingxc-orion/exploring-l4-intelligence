---
artifact_id: "GATE-S1-V8-RESPONSE-2026-07-19-01"
title: "v8 复审回应信（三 Gate MAJOR 清零整改包;Stage-1B 签署第六次申请）"
date: 2026-07-19
addressee: "Gate S1 评审人 / 评委"
review_ref: "wiki/2026-07-19-system-first-research-proposal-v8-stage1a-doctoral-review.md（審 v8@a4ed640,被审件 blob 8761914971）"
remediation_commits: "cfe8a87(评审归档+第十轮核验台账) → 9f5b3d8(P0-A/B/C 基础设施) → 10b3632(再裁决闭环+CE-v3 补丁;本信所引 blob 钉定于此)"
stage_account: "current_activity_stage = Stage-1A survey-ready gate（尾门）;new_model_touches_since_gate_freeze = 0（起算 af96a89）;cumulative_model_touches = 非零（四仓 union v2 在册）;legacy_experiments = INHERITED_PRIOR_EXPOSURE"
attestation: "本整改批 discovery_queries_executed = 0;research-model/smoke 运行 = 0（联网活动仅评审供给六篇引文核验,access log = survey/2026-07-19-sf-access-log-v8-review-verification.jsonl）"
format_note: "逐 finding 采用八字段;DISPUTE 计数 = 0（本信 finding 集合内——连续第二个零异议轮,五反例+WSL 复放全部我方亲手复现）"
---

<!-- release_binding: {"source": "docs/checks/2026-07-19-sf-identity-taxonomy-v5-test.json", "reward_guided": "6/11", "rq_sys_compatible": "5/11", "method_candidate": "0/11", "reward_guided_selection": "4/11", "trajectory_pool": "2/11"} -->

# v8 复审回应信

## 0. 一览

| Finding | Disposition | 状态 |
|---|---|---|
| Gate MAJOR-1（因果边未绑定同一信号实例） | ACCEPT | 清零（signals[] 存在量词派生;A1–A8;12/12） |
| Gate MAJOR-2（条件式 presence 非完备性） | ACCEPT | 清零（required-evidence 合同+裁决行哈希+locator 真解析+release binding） |
| Gate MAJOR-3（WSL2 正典 10/11） | ACCEPT | 清零（canonical resolver;双端 12/12 同 occupancy） |
| P1 三篇 / P2 三篇 | ACCEPT | 开局表 v3（含 TF-TTCL 转录失败二次复发诚信登记）/表 E 首批队列 |
| §9.2 措辞降级 | ACCEPT | dated correction（amendment-14 §5）;本信措辞以机器输出为源 |

**主动披露**：本批内我方非实现者反例代理（CE-v3）**再次击穿了 v5 的初版派生**（信号内跨
用途拼接:惰性 reward 用途+纯 synthesize 活边伪造 rq=True,EXPECTED_TO_FAIL 如实交付）——
当日补丁（活边自身用途必须 ∈ reward_uses,验收 A8）,不破坏任何现有正例。评审 §12-2 所令
「先通过作者外反例」由此双重满足:您的五反例 + 我方隔离代理的新反例,全部并入合同测试。

## 1. Finding Gate MAJOR-1 — 信号实例身份

- **Disposition**: ACCEPT（三子反例全部亲手复现:lifecycle 矛盾 11/11 照绿/异信号拼接
  candidate=True/offline_calibration+scored_select 得 rgs=True）。
- **Root cause**: 行级扁平 signal 字段是**数据模型表达力缺口**——多信号系统被平均成单信号,
  reward 性与控制边各自求真再合取。
- **Changed artifact + commit + blob**: `wiki/survey/2026-07-19-sf-identity-taxonomy-v5.json`
  与 schema-v2 sidecars ×8、`scripts/survey/sf_identity_taxonomy_v5_test.py`、coding v6
  （生成件）——均 @10b3632。**受影响 schema**:新增 `signals[].signal_id`（form/source/
  lifecycle/uses/evidence 逐信号）;边引用 signal_id 且 `signal_use ∈ 该信号.uses`;边可选
  lifecycle 若在必须等于所引信号;**派生存在量词化**:`rq = sequential ∧ ∃ 同一信号 s ∧
  ∃ LIVE 边 e(reward(s) ∧ e.signal_id=s.id ∧ e.signal_use ∈ reward_uses)`（末项 =
  CE-v3 补丁）;`rgs = 池 is True ∧ policy∈{scored,tournament} ∧ object≠none ∧ ∃ reward
  信号含 select|prune`。
- **正/负控输入与预期-实际输出**: 您的验收七例逐项——①边/信号 lifecycle 失配 → validator
  红+派生不计（实测 A1 ✓）;②terminal reward+在线非 reward route 边 → rq False（A2 ✓,
  您的 §4.3 构造现判 False）;③在线 reward revise→retry → True（A3 ✓）;④terminal reward
  select 只达 synthesize/stop（A4/K7 ✓）;⑤多信号身份不丢失——AutoTTS 拆 s_state（在线状态
  观测,form=none,新 enum state_observation）+s_consensus（终态 Agg）,STTS 拆 s_stage_judge
  （在线 prune→branch）+s_final_judger（终态 select 无边）（A5 ✓,再裁决双向确认:该拆的拆、
  不该拆的 DREAM 单 PRM 三用途不拆）;⑥rgs 同信号（A6 ✓）;⑦offline calibration 永不 rgs
  （A7 ✓）。另 K1–K7 全数保持。
- **New derived numbers**（机器重算,数值不变,自此 edge+use 双粒度背书）: reward 6/11、
  rq_sys 5/11（works 4/8）、candidate 0/11、轨迹池 2/11（1/8）、rgs 4/11——本信头部
  release_binding 块与持久化输出机器对账。
- **Residual / 未覆盖限制**: 信号拆分粒度本身仍是编码判断（由独立裁决承载——本批 11 行
  再裁决 11 AGREE/0 DISAGREE,七条非致改观察全数登记于 provenance）。

## 2. Finding Gate MAJOR-2 — 承重证据完备性

- **Disposition**: ACCEPT（两假绿亲手复现——horizon 翻转改 headline 仍 11/11〔十轮最重〕、
  `p9999` 假页码照过;release 数字无对账亦属实）。
- **Root cause**: reconciliation 只验「已填证据的一致性」,从不验「必须存在的证据在不在」;
  突变集从上轮评审清单继承而非派生公式敏感面推导。
- **Changed artifact + commit + blob**: 同 @10b3632;新增
  `scripts/survey/sf_release_binding_check.py`。**受影响 schema**:①**required-evidence
  合同**——15 承重字段（七 strict 位+visibility/topology/modality/horizon/rights/pool/
  policy）逐行强制条目,三类证据:canon/tex 逐字引文（机器核验）、pdf_page（页码∈钉定 PDF
  页数范围+邻接 ASCII anchor 于 N±1 页文本,pypdf）、absence adjudication（负命题:note+
  已检视 scope;本批 8 条全数经独立裁决判 honest）;缺条目=字段 unknown/not_adjudicated,
  **strict 位三态化,unknown 永不默认 False**;②**裁决行哈希**:`adjudication_row_sha256`
  绑定裁决与行内容——**裁决后任何行变更（含您的单独 horizon 翻转与值+证据双翻转）即裁决
  失效 fail-closed**;③release binding:日期送审件带机器可读块,headline 与生成输出逐键
  对账（本信与 v9 均带;负 fixture 自测）。
- **正/负控输入与预期-实际输出**: 您的三精确反例现全部触发失败——horizon 翻转 →
  `adjudication-row-hash-mismatch`+`evidence-value-mismatch`;双翻转 → row-hash;
  `p9999` → `page-out-of-range:p9999/29`;lifecycle 失配 → validator。**敏感面突变集
  13 类**（wrong horizon/双翻转/假页码/lifecycle 失配/边-信号身份失配/wrong right/wrong
  policy/wrong work/wrong modality/wrong sha/wrong kind/nonsense locator/编码手改）在
  **模拟盖章副本**上跑,断言盖章基线为净（反空洞:脏基线会让任何突变空洞变红）,每类必须
  产生基线外新失败——13/13 实测,持久化 `mutation_results`。
- **New derived numbers**: 同 §1;release_binding 对账 PASS。
- **Residual / 未覆盖限制**: absence 条目的语义真值机器不可判——由「存在性+值绑定+裁决
  行哈希+独立裁决」四层承载,如实declared;值与证据同翻转若发生于裁决之前则机器不可见
  （裁决后被行哈希拦截）——该残差由 coder≠adjudicator 双人独立性承载。

## 3. Finding Gate MAJOR-3 — WSL2 正典环境重放

- **Disposition**: ACCEPT（我方在 `wsl -d Ubuntu-24.04`+`~/.venvs/speechrl`（Python
  3.12.3）精确复现 10/11 与全部失败行）。
- **Root cause**: 台账 `stored_at` 存抓取平台的 Windows 盘符路径,消费方未做平台解析。
- **Changed artifact + commit + blob**: `scripts/survey/sf_asset_path.py` @10b3632——单一
  canonical resolver（盘符 ↔ `/mnt/<drive>/` 双向,六用例自测退出码非零可证伪）;TeX/PDF
  读取全部经其解析（评审 §6.3 方案 2）。
- **Windows/WSL 双环境输出（§12-8 要求）**:
  - Windows: os=nt, Python 3.14.3, `python scripts/survey/sf_identity_taxonomy_v5_test.py`
    → **12/12 PASS**;generator `--check` OK;
  - WSL2: `wsl -d Ubuntu-24.04` + `source ~/.venvs/speechrl/bin/activate`（Python 3.12.3),
    同命令 → **12/12 PASS**;generator `--check` OK;
  - 两端 occupancy 完全一致（数字见 §1）;持久化快照 = 正典 posix 运行（platform 字段
    在档:`docs/checks/2026-07-19-sf-identity-taxonomy-v5-test.json`）。
- **Residual / 未覆盖限制**: resolver 只处理盘符↔mnt 双向映射（相对路径透传）;不防伪造
  路径攻击（与评审范围一致——「正确指令下正确完成任务」）。

## 4. Finding P1/P2 — 开局文献补齐

- **Disposition**: ACCEPT ×6（六篇 6/6 反幻觉核验,access log seq 1–6）。
- **Changed artifact**: 开局表 v3（新日期件,v1/v2 字节不动）@9f5b3d8。P1 三项各带角色/
  去重 ID/预期 route/边界假设:**Reinforced Agent**（2604.27233,表 A,RQ-SYS 直接近邻——
  reviewer 于执行前评价 provisional tool calls,其优化态必须拆 path 编码）;**TF-TTCL**
  （2026.findings-acl.1482↔2604.13552,表 A——**诚信登记:correction-4 已登记「转录失败」
  事故的第二次复发,「看过但遗忘」类第五例,按您的前令登记 provenance 不称首次发现**）;
  **Training-Free GRPO**（2510.08191,表 D 边界——multi-epoch gold 蒸馏 token prior ≠
  TF-Strict,名称碰撞防同名同定义,仓内 v2 复审定性在案）。P2 三项入新表 E 首批发现/筛选
  队列（TRACE/LWE/Min-Seek,各带首批检查点）。
- **Residual**: 六篇均只定队列位置,占据判定留给 Stage-1B sidecar 单写链编码。

## 5. Finding §9.2 — 措辞降级

- **Disposition**: ACCEPT。v8 的「真 reconciliation/七类突变 fail-closed/三重破坏已全
  拦截」相对当时检查覆盖为超额保证——dated correction 载于 amendment-14 §5（v8 钉定件
  不改字节）;整改期采用您给定的降级表述;本批完成后的新真值一律以 v5 测试持久化输出为
  措辞来源（禁止散文自数;本信完成态语句皆可回指机器输出）。**内审环第十层镜头**:突变集必须从派生
  公式敏感面推导,不从上轮评审清单继承（已实现为 V8 的 13 类集合）。
- **Residual**: 无。

## 6. 签署声明与放行请求

- `discovery_queries_executed = 0` 维持;`new_model_touches_since_gate_freeze = 0`
  （起算 af96a89;本批零研究模型/零 smoke）;
- 独立制度本轮产出:再裁决 11 AGREE/0 DISAGREE（批 A 6/0+批 B 5/0,任务标识入行,行哈希
  盖章）;CE 语料 v1+v2+v3 = 17 案全并入 V5;CE-v3 击穿与当日补丁如实披露（§0）;
- 按 §11 放行矩阵:三项 FAIL 门禁验收逐项闭合（identity-bound signals+killer tests /
  required evidence+true locator+headline binding / Ubuntu-24.04 Python3.12 双端一致）;
  请求复核并签署 **Stage-1B survey execution（第六次申请）**;签署后 owner 执行批准
  （owner 承重行抽查权于签署时行使）,第一条 systematic query 即 Stage-1B 起点。
