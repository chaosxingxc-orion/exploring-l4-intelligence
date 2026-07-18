---
artifact_id: "SF-PROTOCOL-AMENDMENT-13-2026-07-19-01"
title: "Amendment 13 — v7 复审(WITHHOLD,3 Gate MAJOR)整改合同:审计层不可改写/因果 control edges/sidecar 单写链"
date: 2026-07-19
review_ref: "wiki/2026-07-18-system-first-research-proposal-v7-stage1a-doctoral-review.md（審 v7@87877f1,blob e2d0d7b9）"
owner_ruling: "2026-07-19「按你的建议走」——全盘 ACCEPT,按评审 §10.2 Step A→E 顺序执行;actor 方案=隔离代理裁决+owner 抽查"
stage_account: "current_activity_stage = Stage-1A survey-ready gate（尾门）;new_model_touches_since_gate_freeze = 0（起算 af96a89）;cumulative_model_touches = 非零（四仓 union v2 在册）;legacy_experiments = INHERITED_PRIOR_EXPOSURE;本批 discovery_queries_executed = 0"
---

# Amendment 13：v7 复审整改合同

## §1 Gate MAJOR-3 — 审计层恢复与不可改写检查（Step A,已闭合）

**事故（我方违规,如实登记）**：v6-consolidated 于 `04cf987`（blob `2af5131`）被评审;续68 整改提交
`70c1b04` 将其原位改写（39+/26−:taxonomy v2→v3、3/11→2/11、lineage 完成态声明）,同时 v7 又宣告
`v6@04cf987` 为被审历史态——违反本仓自订「审计层 append-only;更正走 dated supersession」。根因:
批量执行时把已评审日期件误当工作层（supersede-in-place)处理。

**修复**：
- `4e760b4` 恢复 v6 当前路径为原字节（`git hash-object` 复核 = `2af5131830e2a50a579658c8163f96b87524bb81`）;
  `70c1b04` 保留不擦除（无 rebase/reset）;改写内容仅存活于 superseding artifact v7;
- `56496f0` 上线 **audit-artifact immutability registry**（`wiki/survey/sf-audit-artifact-registry.json`,
  69 件审计层日期件 blob 钉定,登记表自身 append-only）+ fail-closed 检查
  `scripts/survey/sf_audit_immutability_check.py`（blob 改动/删除/重复登记/工作树漂移四类失败;
  内存负 fixture + 活体突变测试双验证先红后绿）;
- 范围纪律：登记范围 = 评审报告/送审 proposal/回应信（审计层）;工作层（队列/矩阵/编码表/schema）
  维持 supersede-in-place + dated 墓碑,新语义走新日期件（本批开局表 v2、taxonomy v4、coding v5 均为
  新日期件,v1/v3/v4 原件字节不动）;
- 引用纪律：后续引用被审历史态一律 `v6@04cf987` 形式,不写裸路径。

## §2 Gate MAJOR-1 — RQ-SYS 因果 control edges（Step B,已闭合）

**缺陷（评审 Round 3 杀伤实验,我方亲手复现坐实）**：v3 派生式 `rq = reward ∧ sequential ∧
decision_rights≠∅` 允许「select 信号 + 无关 memory_write 权」拼接成 method candidate。

**修复（taxonomy v4,`wiki/survey/2026-07-19-sf-identity-taxonomy-v4.json`）**：
- `control_edges` 一等公民记录：{signal_use, decision_right, signal_lifecycle, source_locator,
  edge_semantics}——**逐边 locator + 因果语义句强制**;
- **allowed_relations 白名单**（种子=评审 §4.3 关系表;四条证据驱动新增各带锚定行与论证:
  select→supply/prune→supply〔选择条件化下一轮供给,Agentic Coding pipeline〕、
  stop_budget→tool_call〔ATLAS explore-or-stop 单决策〕、stop_budget→branch〔DREAM 补采〕;
  扩展白名单必须新日期 supersession + 裁决,禁字段名相等猜测）;
- 派生式：`rq = reward ∧ sequential ∧ count(有效边,lifecycle∈{online_step,terminal}) ≥ 1`;
- killer 扩充（合同测试 V3）：**K4 disjoint 无边必假**（评审原构造）、**K5 伪造边越白名单必假**、
  **K6 terminal-only 终答选择+无关序贯权必假**、P1 revise→retry / P2 stop_budget→stop 正控必真;
  另 V3b 增「有边但非 reward 形式不升格」两例（ATLAS consensus / ToolGate gate——边不救非 reward 信号）;
- 11 行逐行 edge 证据复核（unknown 不满足）:边证据全部锚定 canon（DFS 正典节逐字引文）或 tex
  （钉定 eprint 逐字句,TeX 命令剥离后规范化匹配）;
- **发现并更正一处 v4 可发现错码**：Selective TTS `decision_rights` 原 `["stop"]` 与证据不符——
  stage-local α 剪枝控制的是候选晋级（branch 权）,预算为固定值非信号控制;dated correction 载于
  sidecar `adjudication_provenance`;
- **另一处 locator 转述清除**：pipeline 行原 locator『Iter 0…selection via RTV…』为省略号转述非
  TeX 逐字,换为可机器核验原句 `'apply RTV to obtain a high-quality subset of K summaries'`;
- **非实现者反例代理击穿 v4 初版并被修补（第九层防线当场生效）**：CE-v2 代理构造
  `__fixture__terminal_select_branch_miscat`——白名单 `select→branch` 边套在 terminal 终答
  锦标赛上,初版 derive 仍判 rq=True（EXPECTED_TO_FAIL 标记如实交付）;补丁 = **terminal
  生命周期的边只准指向终态权 {synthesize, stop}**（不破坏任何现有正控;killer 合同增 K7）;
  CE-v2 共 6 案并入合同测试 V5（另含 confidence 诱饵/synthesize_input∉reward_uses 探针/
  edge 承重成对 fixture/AutoTTS 实行断言）;
- **重算结果（机器,先冻结语义后看数字）**：rq_sys_compatible = 5/11（works 4/8）、
  method_candidate = 0/11、strict∧reward∧pool 轨迹 = 2/11（works 1/8）、reward = 6/11——
  与 v3 数值相同但全部 edge 背书;新增 `reward_guided_selection = 4/11`（§7.6 拆轴:
  candidate_pool_exists/selection_policy 分离,PDR random-K 保留池事实而永不计入 reward 选择）。

## §3 Gate MAJOR-2 — sidecar 单写链与真 reconciliation（Step C,已闭合;评审 §5.5 顺序论证采纳——前置到 Stage-1A 收口）

**数据流**：`wiki/survey/sidecars/<work>.sidecar.json`（8 件正典集合内的单一手写层;sha256 由 ledger 机器注入）
→ `scripts/survey/sf_coding_generator.py`（确定性投影,重复运行零 diff,`--check` 模式验字节等同）
→ `wiki/survey/2026-07-19-sf-known-item-coding-v5.json`（GENERATED,手改=失败）
→ `scripts/survey/sf_identity_taxonomy_v4_test.py` V7 真 reconciliation → occupancy。

**V7 真 reconciliation 逐项**（全部 fail-closed）：
1. 单写：coding 与 generator(sidecars) 输出**字节等同**;
2. ledger 绑定：{id, kind, sha256} 必须命中**同一行**（版本绑定 = 字节级 sha256,强于 arXiv vN）;
3. `canonical_record_id` 解析到真实 `## <work-id>` 节标题（非任意子串）;
4. locator 语法 + 引文核验：canon 引文必须逐字出现在**该 work 自己的正典节内**;tex 引文在钉定
   eprint 规范化全文内;无引文则须结构 token（pN/Fig/Table/Algorithm/Eq/§）;`nonsense` 类必拒;
5. work-id 三向一致：paper_work_id = 正典锚 = method_path 前缀（断言而非推导源）;
6. `field_evidence`：承重字段（模态/信号形式/信号源）绑定证据引文,字段翻转即值-证据失配;
7. actor 纪律：稳定 actor id（`W1` 禁用）;承重行 `coder ≠ semantic_adjudicator` 且必须
   `adjudicated_agree`;分歧只进 conflict_queue 不进完成态 occupancy。

**V8 突变闭环（反空洞设计:每类突变必须产生基线之外的新失败）**：wrong work / wrong modality /
wrong signal / nonsense locator / wrong SHA / wrong kind 六类 sidecar 侧突变 + 编码手改第七类,
7/7 fail-closed。**V9 扩容正确性**：分母 = len(rows) 与 paper_work_id 去重（`/11` 硬编码与
`split('#')` 推导已清除）;合成第 12 行→报表自动 `/12`;重复 method_path_id 拒收。V6 换真断言
（重算两次同构+分母一致性,原字面量 `True` 假检查清除——该假检查同时过了我方内审环,内审环
新增「新检查 oracle 等强审计」镜头,见 §5）。

**actor 方案（owner 2026-07-19 批准）**：`claude-fable-main:s-ea4f0926`（首编）/
`claude-opus-iso-adj-{A,B}:task-…`（隔离裁决代理,非实现者,任务标识入行）/ `owner`（抽查+
签署）/`ext-reviewer`。**裁决结果**：批 A 5 AGREE/1 DISAGREE（AutoTTS 拓扑
single_core→single_core_multi_call,证据成立采纳;另录 ATLAS 池位张力与 ToT 缺文档边两观察,
均无门禁影响、如实入注）;批 B 4 AGREE/1 DISAGREE（open-sft-variant 核=SFT Qwen3-8B 纯文本,
原 vision_native 为闭源行任务级引文误继承,采纳更正）——两处 DISAGREE 均非改果错码但如实
更正,DISAGREE→采纳链载于 sidecar `adjudication_provenance`;11/11 行 `adjudicated_agree`,
coder≠adjudicator 全行成立。非实现者新反例由第三隔离代理作者
（`2026-07-19-sf-independent-counterexamples-v2.json`,合同测试 V5 并入,其中 1 案击穿初版
派生并催生 K7 补丁——见 §2）。

**Stage-1B 批次入链合同**：新论文 = fetch(ledger 登记 sha)→DFS/canonical 记录→sidecar（编码+
edge+field_evidence+locator 前置）→generator→reconciliation→occupancy;首编与裁决分角色;
未裁决承重行不进任何报表。

## §4 P1 文献补链（Step D,已闭合;四项均 2026-07-19 反幻觉核验,access log 在案）

- **Step-level Verifier-guided Hybrid TTS**（2025.emnlp-main.931,Chang et al.）→ 开局表 v2 表 A
  最高优先新增,编码时拆两条 method path（conditional sequential refinement / hybrid composition）;
- **RFG**（2509.25604）+ **DEGS**（2607.09693）→ 开局表 v2 新表 D（BOUNDARY:implicit-reward /
  internal-state 边界检验件,不因 training-free 标题计入 project method）;
- **legal-verifier 负结果**（2025.nllp-1.15）→ 表 C **NEG-P10** 回链（仓内早期在案
  `wiki/2026-07-11-survey-full-verification.md:59,229`,v7 附录漏收更正）;
- 表 C 逐行加 **claim key**（集合 = NEG-P1..P10,§7.1 可追踪性要求——每条承重先验绑定表内单行定位）。

## §5 完成态语言更正与内审环升级（评审 §8.2/§9.2）

**dated correction**：v7 与 amendment-12 中「lineage reconciliation fail-closed」「P0-3 可发现
错码已解决」两类陈述在其落笔日为**超前完成态**（当时实为 presence-only check——
`LINEAGE_FIELDS_PRESENT / SEMANTIC_RECONCILIATION_PENDING`）。该错误保证由本批真实实现取代;
v7 为钉定审计件不改字节,更正以本节为正典。**内审环新镜头（第九层防线）**：每条新增机器检查
必须通过「oracle 等强审计」——检查条件不得为常量/重言式,必须存在使其失败的输入并演示之
（V6 字面量 `True` 假检查即此类;V8 反空洞设计同源）。

## §6 门禁现值（本批收口时）

- audit immutability：PASS（69 pins,0 failures;活体突变先红后绿）;
- taxonomy v4 合同测试：11 检查——V7 于裁决完成前唯余 `load-bearing-not-adjudicated`（时序性,
  fail-closed 正确行为）,其余全绿;裁决闭合后全绿快照持久化 `docs/checks/2026-07-19-sf-identity-taxonomy-v4-test.json`;
- 量词 lint：FILES 已指向本批 actives,0 未限定命中;
- systematic query = 0;research-model/smoke 运行 = 0。
