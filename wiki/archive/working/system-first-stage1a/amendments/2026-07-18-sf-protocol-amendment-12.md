---
amendment_id: "SF-PROTO-AMENDMENT-12"
date: 2026-07-18
scope: "v6 复审整改合同——taxonomy v3(RQ-SYS control edition)/coding v4 源文忠实重编码/拓扑政策 A+敏感列/ToT 裁决/lineage 最小实现/Stage-1B 批量编码工具链合同/文献补入与引文钉定"
owner_ruling: "2026-07-18 六裁决:①拓扑政策 A（共享权重多调用∈单核）+严格拓扑敏感列全程双算;②P0-1 三分派生采纳;③P0-2 重编码 GO;④ToT 按全文裁决 OK;⑤P0-3 最小 lineage OK+工具链扩展性分析;⑥文献登记与引文钉定 GO"
---

# Amendment-12：v6 复审整改合同

## §1 taxonomy v3（P0-1;dated supersession of v2）

三分派生（诚实命名,能力包络内）：`is_s0_core_compatible`（严格位∧拓扑政策∧原生 audio/omni）
/ `is_rq_sys_control_compatible`（**在线** reward/评价反馈〔signal_lifecycle∈{online_step,
terminal}∧形式∈{scalar,pairwise,verifiable_outcome}〕∧序贯时域∧decision_rights≠∅——reward
可作用于 route/retry/branch/tool/memory/supply/stop/execute-skip 任一下一步动作权）/
`is_project_method_candidate` = 两者合取。**K 池降为机制分层**（终态 selector = 序贯控制的
退化特例,空位坐标重立为 method_candidate 本身）。新增 `signal_lifecycle`（离线校准标量
永不冒充在线 reward）。**拓扑政策 A 冻结**（owner 裁决:同一冻结核心多调用/多角色编排∈单核
——这正是 RQ-SYS 机制形态）+ **严格拓扑敏感列全程双算持久化**（CE-1b 拓扑蕴含在敏感列中
由拓扑轴本身判定,非空洞;Stage-1C owner 选解释）。killer fixtures 三例（旧规则红/新规则
绿）+ PDR 错码负控入合同测试（9/9 PASS）。

## §2 coding v4（P0-2;源文忠实重编码）

**#pdr → #pdr-random-k**：TeX 一手源（eprint sha256 137d5a93… 与评审钉定逐字节一致）明写
"For random-K, we follow PDR and **randomly sample** K previous summaries"——无选择信号
（form/source/lifecycle = none;v3 的 pairwise/llm_judge 系 pipeline 信号误继承,Gate
MAJOR-2 更正）;#rtv-pdr-pipeline 带 `component_path_ids` 防独立复制误计。**ToT 裁决执行**
（P1-1）：该文定义的仅有标量 = 离线校准分 Eq.3;推理期 "Evaluation" = 合成内定性评估;无部署期
独立 reward 定义 → **profile-conditioned orchestration boundary,移出 reward 集合**（证据句
入行注）。**机器新正典（policy A;全部双分母）**：reward-guided **6/11**;rq_sys_compatible
**5/11**（paths;works 4/8——DeepVerifier×2/STTS/DREAM/pipeline,其中三者 strict 位不满足）;
strict∧reward∧K 池（机制分层）= **轨迹池 2/11（unique work 1/8）**;s0_core_compatible
0/11;**method_candidate 0/11**。

## §3 lineage 最小实现（P0-3）+ Stage-1B 批量编码工具链分析（owner 裁决⑤附加问）

**本批落地**：每行强制 paper_work_id / fulltext_ref（台账定位,sha256 在案）/
canonical_record_id（DFS 件+anchor）/ source_locator / coder / semantic_adjudicator;
reconciliation V7 fail-closed（台账无 sha 行、正典文件缺、anchor 不在文内均 FAIL）。

**工具链扩展性分析（后续论文按此流水线,防 MAJOR-2 类错误再生）**：
1. **单写原则**：Stage-1B 起,每篇 DFS 精读时同步产出**机器可读 per-paper sidecar JSON**
   （13 轴字段+逐轴 locator）——coding 行由 sidecar **生成**而非手抄,消灭「散文→手填行」
   这条 MAJOR-2 错误通道;sidecar 生成器 = Stage-1B 首周工具（零查询可建,登记执行合同）。
2. **双角色**：承重行 coder ≠ semantic_adjudicator（组合路径/裁决类行强制;普通行抽查）。
3. **fixture 库 append-only**：每轮评审产出的 killer/错码 fixture 永久入合同测试,批量编码
   前必须全绿。
4. **reconciliation 入门禁**：Stage-1B 期间 V7 类校验并入九项门禁复跑集。
5. **locator 前置**：source_locator 在编码时填写,不允许事后补——无 locator 的行不得进入
   occupancy 分母。

## §4 文献补入与引文钉定（P1-2/P1-3）

开局表 A 补 **PDR 原始论文**（Rethinking Thinking Tokens, Madaan et al., 2510.01123——
inference orchestration 与 trained-8B 两路径分行编码,正好检验 TF-Strict 拆分）与
**SWE-Replay**（Ding et al., 2601.22129——轨迹复用/branch decision rights/无显式 reward
selector 边界）;表 C 补 **TRT**（Zhuang et al., 2602.03094——RQ-CTRL 强反例:无外部反馈的
自条件化增益替代解释）。三项均为 Agentic Coding TeX 引文键一手可见（pdr-paper/
swe-replay-paper/test-time-recursive-thinking-paper）,3/3 反幻觉过。引文钉定：ToT 全题名
（…through Orchestrated Tool Calling）;DeepVerifier 全副标题注记;tau2-bench 于**证据性
使用前**钉 release/commit;DEEPLY_READ 绑定 = 台账 sha（atom+fulltext ledger 逐行）,附录
分节名不再独立承担。
