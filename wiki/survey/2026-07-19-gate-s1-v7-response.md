---
artifact_id: "GATE-S1-V7-RESPONSE-2026-07-19-01"
title: "v7 复审回应信（三 Gate MAJOR 清零整改包;Stage-1B 签署第五次申请）"
date: 2026-07-19
addressee: "Gate S1 评审人 / 评委"
review_ref: "wiki/2026-07-18-system-first-research-proposal-v7-stage1a-doctoral-review.md（審 v7@87877f1,被审件 blob e2d0d7b9）"
remediation_commits: "f15a4a5(评审归档+核验台账) → 4e760b4(Step A1 v6 恢复) → 56496f0(Step A2 immutability) → 7dd11ca(Step B–D 基础设施) → 3facbcc(裁决闭环+CE-v2 补丁) → 1d8bd29(记录批;本信所引 blob 钉定于此)"
stage_account: "current_activity_stage = Stage-1A survey-ready gate（尾门）;new_model_touches_since_gate_freeze = 0（起算 af96a89）;cumulative_model_touches = 非零（四仓 union v2 在册）;legacy_experiments = INHERITED_PRIOR_EXPOSURE"
attestation: "本整改批 discovery_queries_executed = 0;research-model/smoke 运行 = 0（联网活动仅评审供给引文核验,access log = survey/2026-07-19-sf-access-log-v7-review-verification.jsonl）"
format_note: "逐 finding 采用评审 §10.3 八字段;DISPUTE 计数 = 0（本信 finding 集合内——九轮首次零异议轮,三 MAJOR 全部我方亲手复现成立）"
---

# v7 复审回应信

## 0. 一览

| Finding | Disposition | 状态 |
|---|---|---|
| GATE MAJOR-1（RQ-SYS 无因果边） | ACCEPT | 清零（taxonomy v4 control_edges;killer K4–K7;11/11 测试） |
| GATE MAJOR-2（lineage=presence check） | ACCEPT | 清零（sidecar 单写链前置 Stage-1A 收口;七类突变 fail-closed） |
| GATE MAJOR-3（v6 被原位改写） | ACCEPT（我方违规,如实登记） | 清零（原字节恢复+immutability registry/check） |
| P1 §7.3/§7.4/§7.5/§7.6/§7.1 | ACCEPT ×5 | 全部落地（开局表 v2/表 D/NEG-P10/拆轴/claim key） |
| §8.2 完成态语言 | ACCEPT | dated correction+内审环新镜头（amendment-13 §5） |

**主动披露**：我方非实现者反例代理在本批内**击穿了 taxonomy v4 的初版派生**（白名单
`select→branch` 边套在 terminal 终答锦标赛上仍判 rq=True,EXPECTED_TO_FAIL 标记如实交付）——
当日补丁（terminal 边只准指向终态权 {synthesize, stop},killer K7）,反例六案并入合同测试 V5。
这是评审所要求「非实现者提出新语义反例」制度的实际产出,一并呈报。

## 1. Finding GATE-MAJOR-1 — RQ-SYS 派生缺因果边

- **Disposition**: ACCEPT（评审 disjoint 构造经我方亲手重放坐实:select+memory_write 无关联
  → `is_project_method_candidate=True`）。
- **Root cause**: v3 派生式 `rq = reward ∧ sequential ∧ decision_rights≠∅` 只测集合非空,
  字段之间的因果关系从未成为机器对象——同型失败第九层（字段关系语义）。
- **Changed artifact + commit + git blob**:
  `wiki/survey/2026-07-19-sf-identity-taxonomy-v4.json` @1d8bd29 blob `75c7f5037f15`;
  `scripts/survey/sf_identity_taxonomy_v4_test.py` @1d8bd29 blob `40ef1ea8ff56`。
  变更:control_edges 一等记录 {signal_use, decision_right, signal_lifecycle, source_locator,
  edge_semantics} 逐边强制;allowed_relations 白名单（种子=评审 §4.3 表;四条证据驱动新增各带
  锚定行,隔离裁决代理判 LEGIT 并附 `stop_budget→tool_call` 不可泛化警示,已录入 taxonomy）;
  派生式 = `rq = reward ∧ sequential ∧ count(LIVE 有效边)≥1`,LIVE = online_step 或
  (terminal ∧ 右端∈{synthesize,stop})。**old/new 字段 diff**:新增 control_edges/
  candidate_pool_exists/selection_policy/field_evidence/load_bearing/adjudication_status
  六字段;派生新增 reward_guided_selection/n_valid_live_edges;其余字段名与枚举与 v3 一致。
- **Machine check and exact result**: `sf_identity_taxonomy_v4_test.py` → **11/11 PASS**
  （持久化 `docs/checks/2026-07-19-sf-identity-taxonomy-v4-test.json`）。V3 killer:
  **K4 disjoint 无边=False（评审原构造）/K5 伪造 select→memory_write 边越白名单=False/
  K6 terminal-only 终答+无关序贯权=False**;正控 P1 revise→retry=True、P2 stop_budget→stop
  =True;**K7（terminal 边指向前向权必假）由 CE-v2 fixture 经 V5 强制**（killer 合同载于
  taxonomy v4）;V3b 另含「有边但非 reward 形式不升格」两例（ATLAS consensus/ToolGate
  gate——边不救非 reward 信号）。
- **Adversarial negative control**: K4/K5/K6 即负控;另 CE-v2 六案（非实现者作者）含
  confidence 诱饵、synthesize_input∉reward_uses 探针、edge-dropped 成对 fixture（v3 洞回归
  哨兵:同行去边必须翻 False）。
- **New derived numbers**（机器重算,先冻结语义后看数字——数值不变,自此全部 edge 背书）:
  reward 6/11;**rq_sys_compatible 5/11（works 4/8）**;method_candidate 0/11;
  strict∧reward∧pool 轨迹 2/11（works 1/8）;新增 reward_guided_selection 4/11。
- **11 path control-edge 对账表**（全边 locator 逐字核验入测试;`canon:`=DFS 正典节内逐字,
  `tex:`=钉定 eprint 逐字）:

| method_path | 边（signal_use→right,lifecycle） | rq_sys |
|---|---|---|
| 2602.16485#calibrated-orchestration | route→route(pre-context 文档边)+synthesize_input→synthesize(terminal) | False（text_critique/pre-context） |
| 2604.16529#pdr-random-k | **无边**（random supply 非信号控制,如实空） | False |
| 2604.16529#rtv | **无边**（terminal 终答,K6 真实样例） | False |
| 2604.16529#rtv-pdr-pipeline | select→supply+prune→supply(online;tex 'apply RTV to obtain a high-quality subset of K summaries') | **True** |
| 2605.08083#discovered-controller | prune→branch+stop_budget→stop(online,状态驱动如实注) | False（consensus 形式） |
| 2606.01667#agentic-orchestration | stop_budget→stop+stop_budget→tool_call(online,explore-or-stop 单决策)+synthesize_input→synthesize(terminal) | False（consensus 形式） |
| 2606.03054#trained-gate | execute_skip_gate→execute_skip(online) | False（binary_gate 形式） |
| 2026.findings-acl.1243#closed-prompt-only | revise→retry+stop_budget→stop(online);tool_call 权**如实无边**（分解 agent 决定查什么,非 judge 分控制——裁决代理专项确认） | **True** |
| 2026.findings-acl.1243#open-sft-variant | 同上两边 | **True** |
| 2026.findings-acl.1724#pipeline | prune→branch(online);**rights dated correction ['stop']→['branch']**（预算=固定值非信号控制,stop 权撤回——裁决代理专项确认 branch 正确） | **True** |
| 2026.findings-acl.511#prm-guided-search | prune→branch+stop_budget→stop+stop_budget→branch(补采,裁决代理专项确认非 retry) | **True** |

- **Residual risk / unresolved**: 白名单关系类型的语义正确性最终仍依赖逐边裁决（机器只验
  白名单+成员+locator 非空+引文逐字）;缓解 = 扩展纪律（新关系必须新日期 supersession+锚定
  行+裁决）+ `stop_budget→tool_call` 不可泛化警示已入 taxonomy。

## 2. Finding GATE-MAJOR-2 — lineage reconciliation 是 presence check

- **Disposition**: ACCEPT（评审三重语义破坏实验我方亲手重放坐实:bogus-work/模态翻转/
  nonsense locator 后 9/9 仍 PASS 且 occupancy 不变）;**§5.5 顺序论证采纳——sidecar 单写链
  从「Stage-1B 首周」前置到 Stage-1A 收口**（双来源体系风险成立）。
- **Root cause**: 数据流中不存在「源记录字段→投影字段」的可比对象:coding 是手写正典,检查
  只能查字符串存在;V6=字面量 `True` 假检查、`/11` 硬编码、unique work 由 `split('#')` 推导、
  V1 快照断言、actor=W1 群组标签——五项子指控全部在案属实。
- **Changed artifact + commit + git blob**:
  sidecars ×8（如 `wiki/survey/sidecars/2604.16529.sidecar.json` @1d8bd29 blob
  `823934acf17a`）;`scripts/survey/sf_coding_generator.py` blob `49a72d056a7c`;
  `wiki/survey/2026-07-19-sf-known-item-coding-v5.json`（GENERATED）blob `7893c68e51aa`;
  合同测试 blob `40ef1ea8ff56`。
- **数据流（§10.2 Step C 要求的说明）**: sidecar（8 件正典集合内的单一手写层;sha256 由
  ledger 机器注入,绝不手抄）→ generator（确定性排序,重复运行零 diff,`--check` 验字节等同）
  → coding v5（生成件,手改即失败）→ reconciliation → occupancy。V7 真 reconciliation 七项:
  ①单写字节等同;②ledger {id,kind,sha256} **同一行**绑定（版本绑定=字节级 sha256）;
  ③canonical_record_id 解析到真实 `## <work-id>` 节标题;④locator 语法+引文核验（canon 引文
  必须在该 work 自己的正典节内逐字出现;tex 引文在钉定 eprint 全文内,TeX 命令剥离规范化;
  nonsense 必拒）;⑤work-id 三向一致断言（paper_work_id=正典锚=method_path 前缀,不再推导）;
  ⑥field_evidence 值-证据对（承重字段翻转即失配）;⑦actor 纪律（稳定 id,W1 禁用;承重行
  coder≠adjudicator 且必须 adjudicated_agree;分歧只进 conflict_queue）。
- **Machine check and exact result**: **V8 七类突变全 fail-closed 且反空洞**（每类必须产生
  基线之外的**新**失败——评审的六类:wrong work/wrong modality/wrong signal/nonsense locator/
  wrong SHA/wrong kind,第七类=编码手改重演评审实验,由单写字节等同拦截）;**V9 扩容**:分母
  = len(rows)+paper_work_id 去重（`/11` 与 `split('#')` 已清除）,合成第 12 行→报表自动
  `/12`,重复 method_path_id 拒收;V6 换真断言（重算两次同构+分母一致）。结果全在持久化
  check JSON `mutation_results` 字段。
- **Adversarial negative control**: 上述七类突变即负控;此外**过程中真实抓到三处旧错码**
  （STTS rights、pipeline 转述 locator、open-sft 模态误继承——第三处由隔离裁决代理发现）,
  证明链条对真实错码同样有发现力,非仅 fixture。
- **actor/独立裁决（§10.2 D 项）**: coder=`claude-fable-main:s-ea4f0926`;隔离 Opus 双代理
  批 A 5 AGREE/1 DISAGREE（AutoTTS 拓扑 single_core→single_core_multi_call,采纳）、批 B
  4 AGREE/1 DISAGREE（open-sft 核=SFT Qwen3-8B 纯文本,采纳）——DISAGREE→更正→agree 链全部
  载于 sidecar `adjudication_provenance`;11/11 行 `adjudicated_agree`,coder≠adjudicator
  全行成立;AI 代理任务标识入行;owner 抽查权保留（签署时行使）。
- **New derived numbers**: 同 §1（重算不变）。
- **Residual risk / unresolved**: field_evidence 的「值与证据同时翻转」仍非机器可判——由
  独立裁决层承接（已文档化于 taxonomy `field_evidence_schema`）;canon 引文核验依赖 DFS
  正典节的稳定性（DFS 件为工作层,更正走 dated 墓碑不动锚句）。

## 3. Finding GATE-MAJOR-3 — 已评审 v6 被原位改写（我方违规）

- **Disposition**: ACCEPT。这是我方真实流程违规,如实登记:续68 批次把已评审的
  v6@04cf987 当作工作层文档级联改写（70c1b04,39+/26−换血）,同时 v7 又宣告其为被审历史态。
- **Root cause**: 归层判断错误——「已被评审钉定的送审件」在批量级联更正中被误当现行工作层
  （supersede-in-place）;规则本身早在 CLAUDE.md,缺的是机器强制。
- **Changed artifact + commit + git blob**: **恢复证明**:`4e760b4` 将
  `wiki/2026-07-18-system-first-research-proposal-v6-consolidated.md` 恢复为原字节——
  `git hash-object` 复核 = `2af5131830e2a50a579658c8163f96b87524bb81`,与评审 §6.3 给定
  恢复目标逐字节一致;`70c1b04` 保留不擦除（无 rebase/reset,事故与恢复动作均可审计）;改写
  内容仅存活于 superseding artifact v7。**防线**:
  `wiki/survey/sf-audit-artifact-registry.json` @1d8bd29 blob `126a679179c5`（69 件审计层
  日期件 blob 钉定,登记表自身 append-only）+ `scripts/survey/sf_audit_immutability_check.py`
  blob `a0eb30f74533`。
- **Machine check and exact result**: `sf_audit_immutability_check.py` → **PASS（69 pins,
  0 failures）**,持久化 `docs/checks/2026-07-19-sf-audit-immutability-check.json`;检查四类
  失败:blob 改动/删除/重复登记/工作树漂移。
- **Adversarial negative control**: ①内存负 fixture（错误 pin 必须被抓,oracle-can-fail
  自证）;②**活体突变测试**:对注册的 v6 追加一行→检查 FAIL(exit 1)→复原→PASS(exit 0),
  先红后绿全程留痕于 Step A 执行记录。
- **New derived numbers**: 不适用（治理项）。
- **Residual risk / unresolved**: 检查只保证正确工作流下的审计语义,不防恶意元数据篡改
  （与评审 §6.3 范围一致）;后续引用纪律 = `v6@04cf987` 形式,不写裸路径（本信遵行）。

## 4. Finding P1（§7.3/§7.4/§7.5/§7.6/§7.1）— 文献与编码轴补链

- **Disposition**: ACCEPT ×5。四篇新供给引文 4/4 反幻觉核验为真（access log seq 1–4）。
- **Changed artifact**: `wiki/survey/2026-07-19-sf-stage1b-opening-tables-v2.md` @1d8bd29
  blob `6e1305f728ed`（新日期件,v1 字节不动）。
  - §7.3 **Step-level Verifier-guided Hybrid TTS**（2025.emnlp-main.931）→ 表 A 最高优先
    新增,编码时拆两条 method path（conditional sequential refinement / hybrid composition）,
    P1 carry-forward,不从摘要判占据;
  - §7.4 **RFG**（2509.25604）+ **DEGS**（2607.09693）→ 新表 D（BOUNDARY:implicit-reward/
    internal-state 边界检验件,恰检验 api_only 轴一致性）;
  - §7.5 **legal-verifier**（2025.nllp-1.15）→ 表 C **NEG-P10** 回链——评审判断属实:该文
    早在我方 `wiki/2026-07-11-survey-full-verification.md:59,229` 在案而 v7 附录漏收,已更正;
  - §7.6 拆轴:`candidate_pool_exists` + `selection_policy` 新字段（PDR random-K 保留池事实,
    `random_sample` 永不计入 reward_guided_selection——派生 4/11 见 §1）;
  - §7.1 表 C 逐行 claim key（集合 = NEG-P1..P10）,承重先验→表行→DFS 载体可跳转。
- **Machine check**: 开局表 v2 在量词 lint FILES 集合内,0 未限定命中;四项登记均带核验
  provenance。
- **Residual risk**: EMNLP 931 的 verifier 训练性/control edge 细节待 Stage-1B 首批编码时
  按 sidecar 链落定（本轮只定队列位置,不预判占据——遵评审 §10.1-5）。

## 5. Finding §8.2 — 完成态语言超前

- **Disposition**: ACCEPT。v7 与 amendment-12 中「fail-closed reconciliation」「P0-3 已
  解决」在落笔日为超前完成态（当时实态 = `LINEAGE_FIELDS_PRESENT /
  SEMANTIC_RECONCILIATION_PENDING`）。
- **Changed artifact**: dated correction 载于 amendment-13 §5（blob `126c4dc93d1f`）;v7 为
  钉定审计件不改字节,更正以该节为正典。**内审环新镜头（第九层防线）**:每条新增机器检查过
  「oracle 等强审计」——必须演示存在使其失败的输入（V6 字面量 `True` 假检查通过了我方内审环
  = 本镜头的直接动因;V8 反空洞设计同源）。
- **Residual risk**: 无（该类陈述本轮起一律引用机器 check 输出,禁止散文自数）。

## 6. 签署声明与放行请求

- `discovery_queries_executed = 0` 维持（SURVEY-B 21 lanes/105 查询零执行;第一条 systematic
  query 仍是 Stage-1B 正式起点）;
- `new_model_touches_since_gate_freeze = 0`（起算 af96a89;本批零研究模型/零 smoke）;
- 复审包清单（评审 §10.2 Step E 逐项）:新 dated response=本信;修复 commit+blob=frontmatter
  与各节;old/new 字段 diff=§1;11 path edge 对账表=§1;数据流说明=§2;七类突变+N≠11=§2;
  occupancy 机器重算=§1（散文零手数）;v6 恢复证明=§3;签署声明=本节。
- 按 §11 放行矩阵,三项 FAIL 门禁的验收条件已逐项闭合（§4.4 八项/§5.6 A–D/§6.3 六项——
  逐项对照见 amendment-13 §1–§3）,请求复核并签署 Stage-1B（第五次申请）。三项通过机器反例
  复核后仍需 owner 签署（owner 抽查承重行权保留于签署时）。
