---
amendment_id: "SF-PROTO-AMENDMENT-6"
date: 2026-07-17
trigger: "博导复审 P0-R8 再裁 WITHHOLD（3 MAJOR + 2 MINOR,《2026-07-16-gate-s1-p0r8-rereview-doctoral-review.md》）+ owner 四点裁决（2026-07-16/17:CV 参考域与 learning 方法域受控道 / 独立代理 held-out / 调研退出机制三层架构 / 全文强制）+ agent-era 时代裁决"
scope: "correction #4B gate 整改合同——P0-1..P0-4 全项 + owner 裁决落地;执行期合同（退出机制/全文纪律细则）另见 amendment-7（非本 gate 阻断项）"
independent_verification: "评审 5 项 finding 由研究执行方逐条独立复现后全盘接受:2-seed/空 route 证据/同行 marker/手写 verdict/cross-wire/空 D2 block/threat 标签删除全部在 C4A 门禁下复现 false-green;评审外部引文 7/7 反幻觉核验通过（TimeLogic/Seg-Agent + §7 表五篇）"
---

# Amendment-6：correction #4B gate 整改合同

## §0 定性与合同重申

评审五项 finding **全部成立、全盘接受、零异议**。本轮性质 = 验收 oracle 强度系统性弱于完成态
散文（连续第三轮同构失败）；根因 = oracle 由声称完成的同一方设计且缺 mutation 测试。本批为
每个门禁引入「**该陈述为假时必失败**」的机器检查 + 已落盘负例证明其确实失败。

两处措辞精确重述（事实句，非异议）：① 申请书原文为「92/55/50 **全唯一**」——字面为唯一性
声称，但其在签署包中承载的功能确为正典计数背书，且 bundle 基数错误（声称 31、实际 33）证明
缺失精确重数有实害；② 「D2 全字段机器强制」非申请书逐字原文，但「V1–V13 机器强制、不再是
纸面承诺」在空 `{}` 可过的现实下同等不成立。两处均按评审实质裁定整改。

双向合同维持：一轮窄幅复核 0 新 MAJOR / 0 新 MINOR 且旧项 locator 可重放 → 签署；签署不背书
novelty 或科学效果；签署后仍需 owner 执行批准。

## §1 P0-1：package summary v2（fail-closed）

正典 = `wiki/survey/2026-07-17-sf-canon.json`（期望值单一来源；更新走 dated correction）。
`scripts/survey/sf_package_summary.py` v2 合同：

1. **正典精确计数**：seeds 92 / queries 61 / routes 50 / sentinels 26 / held-out 5、类目并集、
   编译器版本分层——canon 逐项相等，任何偏差非零退出（不再以唯一性冒充计数）。
2. **producer 隔离重跑**：八个确定性 producer 逐一子进程重跑，**新鲜输出字节 == 持久化证据
   字节**方可承重；不一致即恢复原件并 FAIL——手写/陈旧 verdict 不再可能继承绿灯。
3. **route collector 降格**：外部状态审计证据件只报 `EVIDENCE_PRESENT`；裁定层 =
   `scripts/survey/sf_t1_routes_adjudication_validate.py`（R1–R7：50×50 一一对齐、冻结状态==
   裁定状态、tier 与探针在场性互证、200 必有 body 哈希、无探针必有知识依据注记）。
4. **bundle 对账**：manifest #4B 段 `MACHINE_COUNT: files=N fixtures=M` 与表内路径机器枚举、
   磁盘在场性三方相等（杀 31-vs-33 类基数错误）；活跃扫描面自 manifest 机器派生 + 最小必含集，
   **缺文件 = FAIL（不再静默跳过）**。
5. **陈旧口径扫描**：豁免只认结构化历史块（HTML 注释围栏）或 `〔HIST:...〕` 包裹的单个
   occurrence；同行 marker 不再豁免整行。**活跃面历史件政策**：dated 更正合同/评审件/回应信/
   申请书/append-only 审计层按文件名模式豁免——其规范性数字一律折入协议本体与热层（受扫描）。
6. **负例**：`scripts/survey/sf_package_summary_test.py` 落盘 mutation harness——2-seed 截断/
   空 route 证据行/同行 marker+禁词/手写 verdict 篡改/删活跃文件/前缀字节翻转/MACHINE_COUNT
   偏一——全部必须非零退出。

## §2 P0-2：record validator v2（V1–V15）

`scripts/survey/sf_record_validator.py` v2-c4b；语义收紧与新增：

- **V4/V7 双向一一对应**：INCLUDED REC-0 ↔ REC-2 互指必须闭合同一 work；cross-wire、
  many-to-one、orphan REC-2 全部 FAIL（评审 4.2.1 交换变异已入负例）。
- **V14 种子联结（fail-closed）**：validator 必须绑定冻结 seed manifest；seed 侧
  `DIRECT_THREAT` 在 REC-2 转录中消失 = FAIL；威胁触发以 REC-2 标签 ∪ seed 标签为准。
- **V9/V10 内层 schema**：matrix/tf_audit/source_axes/extraction/proximity 为 D2 必含全键块，
  omni_axes/rl_identity/resource_axes/method_occupation 为「全键块 或 类型稳定 NA 对象」；
  全部键位枚举/非空规则以 blank-templates REC-2 模板为 schema 正典——空 `{}` 不再是 block；
  D1 允许部分填充但已填键必须合法。
- **V15 单正典位**：`publication_status` 唯一居所 = `evidence_axes.publication_status`；
  顶层复写 = FAIL（C4A positive fixture 中的双位置实例已修）。
- **V5 后缀**：`OTHER:`/`DUPLICATE_OF:` 后缀非空且 DUPLICATE 目标必须解析到已知 canonical_id。
- **V13 类型稳健**：`disagreements` 非法类型产出结构化 violation，绝不崩溃。
- **fixtures**：`wiki/survey/fixtures-c4b/`（1 正例 + 25 负例，生成器 =
  `scripts/survey/sf_fixtures_c4b_gen.py`——mutation 函数源码即负例文档）；
  `scripts/survey/sf_record_validator_test.py` 子进程级 26/26。fixtures-c4a 保留为历史件，
  不再对 v2 oracle 断言绿灯（v2 刻意更严）。

## §3 P0-3：coverage 补救与哨兵重组

1. **SF-L12（cs.CV+cs.AI）**：SF-L11 词族逐字镜像（零新词）——Seg-Agent 2605.12953
   （MAJOR-3 确定漏检反例）的确定性补救；离线复验 = SF-L12-Q1/Q2 双命中。
2. **SF-L12-Q3 / SF-L13-Q3（SF-L10-Q2 词族逐字镜像）**：预注册 matcher 运行发现第二个结构性
   近失例 **DVD 2505.18079**（frozen-LLM agentic search，59 查询零命中——agent 时代
   **词汇漂移轴**：agentic/autonomous/tool-use 取代 training-free/test-time 自述）；主动披露
   并同批补救，DVD 转标 query-regression counterexample（held-out 资格因参与补救裁定烧毁）。
3. **SF-L13（cs.LG+stat.ML+cs.NE）**：owner 裁决落地——learning 方法域受控投放；arXiv 无独立
   deep-learning 类目，DL 即落本组。编译层 sfqc-1.4.0 append-only，**61 行文件前 55 行逐字节
   不变**（prefix55 哈希钉于 canon）。
4. **声称更正（P0-3.2）**：VQQA 仅独立验证 SF-L11 的 cs.MA 一侧（其类目无 cs.MM）；MAR3 =
   seeded regression，不得称 held-out——两处已写入 sentinel 数据 reviewer_role。
5. **TimeLogic 2606.01631**：reviewer-supplied primary-cs.MM held-out，raw Atom 先冻结后运行，
   实测 SF-L11-Q1 QUERY_HIT（P0-3.1 验收达成）。
6. **fresh held-out ×2（P0-3.4）**：由不接触修订 diff 与词项的隔离代理独立选取，era≥2025
   （owner 时代裁决），预注册后运行——L12 侧 = 2602.21497（cs.CV，2026-02，QUERY_HIT via
   SF-L3-Q7）；L13 侧 = 2605.11374（cs.LG，2026-05，QUERY_HIT via SF-L2-Q6 + **SF-L13-Q2**，
   新方法域道被其自身 held-out 直接验证）。代理检索词与访问逐条入 access log（§5）。
7. **哨兵花名册**：26 哨兵 = 21 + 5 新增；held-out 5（VQQA/Useful-Memories/TimeLogic/
   2602.21497/2605.11374）；结果 QUERY_HIT 23 / SEED 3 / UNRESOLVED 0——L12/L13 道使四篇
   原种子兜底件转为查询直接召回。
8. **routes v3（自查披露）**：强化后的 adjudication validator 抓到 C4A 工件内部真实标注错误
   （ICASSP-2023..2026 `evidence_tier:"A"` 与其 collector 行自述 NO_CONCRETE_URL 矛盾）——
   走 dated supersession `wiki/survey/2026-07-17-sf-t1-routes-v3.jsonl`（四行 tier A→C，
   逐行更正注记，record_sha256 重算；v2 字节冻结不改写），生成器 =
   `scripts/survey/sf_t1_routes_v3_gen.py`。

## §4 P0-4：provenance 强化

1. **raw Atom 正典**：26 哨兵逐篇原始 Atom API 字节落盘
   `docs/survey-provenance/atom/<id>.xml` + append-only 台账 `atom-ledger.jsonl`（含一次
   TLS 瞬断失败行，如实留痕后重试成功）。**「verbatim」从此仅指 raw Atom 字节（sha256 钉定）**；
   匹配用文本字段更名 `source_normalized_abstract`，规范化规则登记于 sentinel 数据
   `abstract_provenance` 块（遗留 21 条 = abs 页渲染文本；新增 5 条 = Atom summary 仅空白折叠）。
2. **REGISTERED_BOUNDARY 强校验**：注册文件必须含该论文的机器可读行
   `BOUNDARY_REG {"paper","boundary","reason","adjudicator","date"}` 全字段非空方可通道成立；
   `os.path.exists` 语义废止。
3. **held-out 时代纪律机器化**：runner 强制 held-out 哨兵 v1 ≥ 2025-01（owner 时代裁决），
   Atom provenance 缺失/哈希不符 = FAIL。

## §5 访问类注册与双计数（attestation 维持）

新访问类（全部 known-ID 或哨兵池专用，**协议 mapping 查询执行数维持 0**）：

- `ID_DEREFERENCE/PROVENANCE_FETCH`：Atom 原文采集（台账 = atom-ledger.jsonl）。
- `ID_DEREFERENCE/FULLTEXT_FETCH`：全文双份采集（PDF+e-print；台账 =
  `wiki/survey/2026-07-17-sf-fulltext-ledger.jsonl`；存储 = 数据盘
  `$SPEECHRL_DATA_DIR/survey-fulltext/`，永不进 git）。
- `REVIEW_CLAIM_VERIFICATION`：评审引文反幻觉核验（协调者 2 次 + 核验代理 5 篇）。
- `HELD_OUT_SENTINEL_SOURCING`：隔离代理为哨兵池选题的 web 检索——检索词逐字登记；其结果
  **只允许进入哨兵池，永不进种子/语料**（防以 sourcing 之名行 discovery 之实）。

批次访问总账 = `wiki/survey/2026-07-17-sf-access-log-c4b.jsonl`（append-only；代理时间戳为
近似值，粒度如实声明）。

## §6 owner 裁决登记（2026-07-16/17）

1. **agent-era 时代裁决**：基模约 2025 年进入 agent 时代，2025 前工作参考价值有限——落地为
   held-out 选取约束（机器强制）、深读/队列优先级、过时性裁定输入（forward 引文存活度）；
   **检索窗口与冻结前缀不动，不作 study_quality 证据维度**（与 venue_tier 零证据权重裁决同构）。
2. **CV = 重要参考域、learning 相关 = 重要方法域** → SF-L12/SF-L13。
3. **独立代理 held-out 安排批准**（P0-3.4 实施如 §3.6）。
4. **引文链退出机制三层架构确认**：发现层 = 检索算法（冻结查询）；相关性廉价筛/退出判据 =
   引文链（backward 自存档全文离线抽取、forward 经学术索引）——细则见 amendment-7。
5. **全文强制**：承重阅读对象 = 论文全文（PDF+e-print 双份），abs 摘要页不再作为承重文本源。
