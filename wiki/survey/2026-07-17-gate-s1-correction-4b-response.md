---
artifact_id: "SF-S1-C4B-RESPONSE-2026-07-17-01"
title: "Correction #4B 回应信 + P0-R9 窄幅复核申请"
date: 2026-07-17
addressee: "Gate S1 评审人（search-design 签署权持有者）"
in_reply_to: "《Gate S1 P0-R8：Stage-1A mapping 执行前窄幅博士生导师式对抗复审》（WITHHOLD,3 MAJOR + 2 MINOR）"
verification_first: "按 reviewer-response-protocol:五项 finding 先逐条独立复现（七个变异在 C4A 门禁下全部亲手复现 false-green）、评审外部引文 7/7 反幻觉核验通过,然后才逐点回应——全盘接受,零异议"
attestation: "discovery_queries_executed = 0 维持;本批全部联网活动 = wiki/survey/2026-07-17-sf-access-log-c4b.jsonl + 两台账（atom/fulltext ledger）"
---

# Correction #4B 回应信

## §1 定性（先核验后回应）

贵审五项 finding **全部成立**。我方在接受前逐条独立复现：2-seed 截断 / 空 route 证据 /
同行 marker 绕过 / 手写 `{"verdict":"PASS"}` / REC cross-wire / 空 D2 block / threat 标签
删除——在 C4A 门禁下**全部复现 false-green**；贵审新引外部论文（TimeLogic / Seg-Agent /
§7 表五篇）经逐 ID dereference **7/7 零幻觉**（access log seq1–7）。

根因承认：连续第三轮「工件真实但完成态语言超出 oracle 强度」——oracle 由声称完成的同一方
设计且缺 mutation 测试。本批修复原则 = **每个完成态陈述配一个「该陈述为假时必失败」的机器
检查 + 已落盘负例证明其确实失败**；我方敌意内审环新增强制 mutation 镜头（本信 §4.3）。

两处措辞精确重述（事实句，非异议；amendment-6 §0 同文登记）：① 申请书原文为「92/55/50
全唯一」，其在签署包中的功能确为正典计数背书且 bundle 基数错误证明实害——按贵审实质裁定
整改；② 「D2 全字段机器强制」非逐字原文，但「V1–V13 机器强制、不再是纸面承诺」在空 `{}`
可过的现实下同等不成立——同样按实质整改。

## §2 逐项回应（P0-1..P0-4 × 交付 × 机器证据）

| 贵审项 | 交付 | 机器证据 |
|---|---|---|
| **MAJOR-1 / P0-1** package summary false-green | v2 重写：canon 精确计数（92/61/50/26/5 逐项相等）+ prefix87/prefix55 哈希钉定 + **八个确定性 producer 子进程重跑、新鲜字节==持久化证据字节**（杀手写/陈旧 verdict）+ route collector 降格 `EVIDENCE_PRESENT` + 独立 adjudication validator + manifest `MACHINE_COUNT` 三方对账（杀 31-vs-33 类错误）+ occurrence 级历史豁免 + 缺活跃文件=FAIL | `scripts/survey/sf_package_summary.py` + `wiki/survey/2026-07-17-sf-canon.json` + `docs/checks/2026-07-16-sf-package-summary.json`；mutation harness = `scripts/survey/sf_package_summary_test.py`（贵审五类变异+前缀翻转+基数偏一全部非零退出） |
| **MAJOR-1.2 路由裁定** | 新增 `sf_t1_routes_adjudication_validate.py`（R1–R7:50×50 一一对齐/冻结==裁定/tier-探针互证/200 必有 body 哈希/无探针必有知识依据） | `docs/checks/2026-07-16-sf-t1-routes-adjudication.json` = PASS,0 violations |
| **MAJOR-2 / P0-2** validator 合同弱于声称 | v2（V1–V15）：REC0↔REC2 **双向一一对应**（cross-wire/orphan/many-to-one 全 FAIL）+ **V14 冻结种子联结 fail-closed**（DIRECT_THREAT 转录丢失=FAIL）+ 内层 schema（枚举正典=blank-templates,空 `{}` 非 block）+ **V15 publication_status 单正典位** + OTHER:/DUPLICATE_OF: 非空后缀与目标解析 + disagreements 非法类型→结构化 violation | `scripts/survey/sf_record_validator.py`；fixtures = `wiki/survey/fixtures-c4b/`（1 正 + 25 负,生成器 `sf_fixtures_c4b_gen.py` 的 mutation 函数即负例文档）；`docs/checks/2026-07-16-sf-record-validator-test.json` = **26/26 子进程级** |
| **MAJOR-3 / P0-3** coverage 反例 | SF-L12（cs.CV/cs.AI,SF-L11 词族逐字镜像）→ Seg-Agent 离线复验 **QUERY_HIT×2**；TimeLogic 冻结为 reviewer-supplied cs.MM held-out → **SF-L11-Q1 QUERY_HIT**；VQQA 声称更正为「仅验证 cs.MA 侧」、MAR3 改标 seeded regression；fresh held-out ×2 由隔离代理独立选取（不见词项/diff,era≥2025）：2602.21497（L12 侧）/ 2605.11374（L13 侧,同时命中新道 SF-L13-Q2）——**两者均纯查询召回**；哨兵 26/held-out 5/UNRESOLVED 0 | queries = 61 行,**前 55 行逐字节不变**（prefix55 sha256 钉于 canon）；`docs/checks/2026-07-16-sf-sentinel-recall.json`；选取隔离与预注册纪律 = amendment-6 §3.6 + access log seq8–10 |
| **MINOR-1 / P0-4.1** verbatim 用词 | 26 哨兵 raw Atom XML 字节+sha256 落盘（`docs/survey-provenance/atom/` + append-only 台账）；「verbatim」从此仅指 raw 字节；匹配文本字段更名 `source_normalized_abstract`,规范化规则登记于 sentinel 数据 `abstract_provenance` 块 | atom-ledger.jsonl（27 行,含 1 次 TLS 瞬断如实留痕）；runner 逐哨兵校验 atom 哈希,缺失/不符=FAIL |
| **MINOR-2 / P0-4.2** boundary 只查存在 | `REGISTERED_BOUNDARY` 须命中该论文的机器可读 `BOUNDARY_REG {paper/boundary/reason/adjudicator/date}` 全字段行；`os.path.exists` 语义废止；一正一负 fixture 入 harness | `scripts/survey/sf_sentinel_recall_test.py`（boundary_registered()）+ `sf_package_summary_test.py` boundary 用例 |

## §3 超出贵审要求的增项（owner 裁决触发,非 gate 重谈）

1. **SF-L13（cs.LG+stat.ML+cs.NE）**：owner 裁决「learning 相关域 = 重要方法域」——SF-L11
   词族对称镜像；其 held-out 2605.11374 直接命中 SF-L13-Q2。
2. **SF-L12-Q3/L13-Q3（DVD 词汇漂移补救,主动披露）**：预注册 matcher 运行发现第二个结构性
   近失例 DVD 2505.18079（frozen-LLM agentic search,**59 查询〔补救道加入前〕零命中**——
   agent 时代词汇漂移轴;补救后 61 查询集下命中 SF-L12-Q3,即补救有效性的机器证明）。
   按贵审 P0-3.3 同法：**SF-L10-Q2 既有词族逐字镜像,零新词**;DVD 转标 query-regression
   counterexample。既已知之,不签署前修复即 premature closure——贵审 §7 原则我方自我适用。
3. **owner 时代裁决登记**（amendment-6 §6.1）：held-out 一律 era≥2025（runner 机器强制）;
   检索窗口/冻结前缀不动;时代先验不进 study_quality。
4. **执行期合同**（amendment-7,**非 gate 阻断项**）：调研退出机制 E1–E3（BFS 干涸 ∧ 引文闭包
   K=2 收敛 ∧ 哨兵清零,饱和表落盘）、全文强制细则（26 哨兵全文双份已入台账）、Seg-Agent
   引文校准实验预注册。**贵审 §12 反无限延长条款我方主动遵守**——amendment-7 不新增签署前义务。

## §4 自查披露（评审不必自行挖掘）

1. **routes v3（我方强化 oracle 自查出的 C4A 数据错误）**：新 adjudication validator 抓到
   ICASSP-2023..2026 四行 `evidence_tier:"A"` 与其 collector 行自述（NO_CONCRETE_URL,
   tier-B/C）矛盾——共享 hub 探针只记录于 2022 行。走 dated supersession
   `2026-07-17-sf-t1-routes-v3.jsonl`（四行 tier A→C+更正注记,record_sha256 重算;v2 字节
   不改写）。这是 v2 阶段的标注失实,如实登记。
2. **fixtures-c4a 在 v2 oracle 下不再断言绿灯**（v2 刻意更严:种子未绑定/双位置
   publication_status 等在旧正例中即命中）——历史件保留,新正典 = fixtures-c4b。
3. **确定性证据全量重生成**：61 行冻结查询下 replay 10/10、真实行 dry-run 17/17（61/61 行
   零 KeyError）、routes 结构 12/12——旧证据 blob 留存 git 历史。
4. **哨兵摘要文本层级如实声明**：遗留 21 条为 abs 页渲染文本（规范化规则已登记）,新增 5 条
   自 raw Atom 派生;匹配结论不受影响（HIT 方向保守近似不变）。

## §5 P0-R9 窄幅复核申请

按贵审 §10 P0-5 约定申请一轮窄幅复核。复跑环境同前（WSL2/Python3.12 或任意 py3,全部
stdlib-only 零联网——采集类脚本不在复跑集内）。从伞仓根目录：

| # | 验收项 | 复跑命令 | 预期 |
|---|---|---|---|
| 1 | fail-closed 门禁全绿 | `python scripts/survey/sf_package_summary.py` | PASS(exit 0);正典精确计数/前缀哈希/八 producer 字节一致/manifest 对账/陈旧扫描 |
| 2 | 贵审 mutations 全部非零退出 | `python scripts/survey/sf_package_summary_test.py` | PASS:基线绿 + 全部变异（2-seed/空 route 证据/同行 marker/手写 verdict/删活跃文件/前缀翻转/基数偏一/boundary 负例）exit≠0 |
| 3 | validator v2 合同 | `python scripts/survey/sf_record_validator_test.py` | 26/26;含贵审三组对抗 fixture（cross-wire/空 D2/threat 删除）非零退出 |
| 4 | 路由裁定 | `python scripts/survey/sf_t1_routes_adjudication_validate.py` | PASS,0 violations（v3 输入） |
| 5 | 哨兵四分法 | `python scripts/survey/sf_sentinel_recall_test.py` | 26 哨兵 0 UNRESOLVED;held-out 5 全纯查询召回;atom provenance 哈希全过;TimeLogic=SF-L11-Q1;Seg-Agent=SF-L12 命中 |
| 6 | 前缀不变性 | `git diff af96a89 HEAD -- wiki/survey/2026-07-15-sf-queries.jsonl` 目视 = 纯 +6 行 | 前 55 行字节不变（canon prefix55 哈希双证） |
| 7 | 历史件未回写 | `git diff af96a89 HEAD -- wiki/survey/2026-07-16-sf-t1-routes-v2.jsonl wiki/survey/fixtures-c4a wiki/survey/2026-07-16-gate-s1-p0r8-rereview-application.md` | 空 diff |

双向合同重申：一轮 **0 新 MAJOR / 0 新 MINOR** 且旧项 locator 可重放 → 签署 Gate S1
mapping-execution gate;签署不背书 novelty/科学效果;签署后仍需 owner 执行批准（三方分立）。
在此之前：**discovery query = 0,模型触碰 = 0,维持不变。**

—— 研究执行方（W1）。本件随提交入 git,blob 以提交为准;更正走 dated correction。
