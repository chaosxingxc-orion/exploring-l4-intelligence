---
artifact_id: "SF-S1-C4A-RESPONSE-2026-07-16-01"
title: "Correction #4A 回应信——对博导复审 WITHHOLD（8 项 P0）的核验、承认与交付"
date: 2026-07-16
addressee: "Gate S1 评审人（search-design 签署权持有者）"
supersedes: "correction #4 回应信 §5 签署清单中 C4-4/C4-5/C4-6 三行的 ✅ 状态表述（本信 §2 收回并更正;原件 append-only 保留）"
trigger: "《Gate S1 Correction #4 执行前博导式对抗复审》裁决 WITHHOLD — CORRECTION #4A REQUIRED；owner 三裁决 = Decision-Log 续62"
attestation: "discovery_queries_executed = 0 维持；本轮联网活动双计数分类留痕（amendment-5 §6 + 2026-07-16-sf-access-log-c4a-review-verification.jsonl,26 行 append-only）"
---

# Correction #4A 回应信

## §1 总立场：核验先行，认错认准

我方对复审的承重断言**亲自逐条独立核验（不委托）**，结论：

1. **仓内事实断言全部属实**——child splitter 宣称 YEAR→MONTH→DAY 实则 ROOT 直拆月、真实
   冻结行必 KeyError（`query_sha256` 在 53 行冻结件中出现 0 次）；amendment-4 §2 白纸黑字
   承诺的 record validator 在 `scripts/survey/` 不存在；sentinel 脚本硬编码 "51 rows" 且
   EXPLAINED_MISS 机制不可证伪；查询类目集确缺 cs.MM/cs.MA；协议/README 陈旧口径共存；
   Decision-Log 续61 Supersedes 与 amendment-4 的 token 退役语义直接冲突；TF-TTCL 确在
   2026-07-14 检索日志第 241 行被我方发现而 87 seed 与 census-v2 均 0 转录。
2. **复审新引 7/7 引文零幻觉**——逐 ID dereference + verbatim 摘要核验，题名/类目/内容特征
   与复审描述完全一致（含 MAR3 主类目 cs.MM 唯一、VQQA 含 cs.MA、AMC 学习型 value function
   的编码警告）。留痕 = `2026-07-16-sf-access-log-c4a-review-verification.jsonl`。**特此致谢：
   两轮共 21 篇点名文献零幻觉，评审的引文可信度记录无瑕疵。**
3. **外部事实属实**——ACL 2026 会期 2026-07-02~07 已过、Anthology 六卷已出版（我方直连
   audit 亦取得 acl-2026 事件页 HTTP 200，title=「64th Annual Meeting…」）：
   `SF-T1R-ACL-2026` 的 `NOT_YET_PUBLISHED` 属**冻结当时即错**（wrong-at-freeze），不是事后
   过时——该定性我方完全接受；PMLR v267 = ICML 2025 已出版，ENTRY_TO_RESOLVE 有确定入口。

## §2 完成态收回（premature closure 复发的正式承认）

correction #4 回应信 §5 中以下三行的 ✅ **超出了行内证据等级，正式收回**：

| 原行 | 原状态 | 更正 |
|---|---|---|
| 「child query 可精确重放」 | ✅（证据仅合成 9/9） | 当时**不成立**——真实冻结行进不了规范函数（KeyError），YEAR 层未实装。现状见 §4（真实行 dry-run 17/17） |
| 「工作级 screening/dedup/adjudication 记录可用」 | ✅（证据仅模板+三合成案例） | 当时**不成立**——承诺的 validator 不存在，无任何机器约束。现状见 §4（V1–V13 实装 + 负例 16/16） |
| 「至少一组 sentinel recall 结果已落盘」 | ✅（9 HIT + 5 EXPLAINED_MISS） | 落盘属实但**测试不可证伪**（自由文本即过），不构成召回诊断。现状见 §4（四分法零 UNRESOLVED） |

这是 G3 同型惯性（结论动词越过证据等级）的第三次复发。我方接受复审 §5.2「premature closure
仍存在」定性，**结构性防复发措施 = 机械化状态动词**（owner 裁决③，见 §5）：本信 §4 清单即
其首次应用——每个状态由 `sf_package_summary.py` 从持久化证据文件推导，人工不再手填完成态。

## §3 两点分层陈述（非异议；裁决我方均接受）

1. **QRP-4（网络访问总量）**：复审所引「约 25 次先前访问」出自我方 dereference log header 的
   **主动聚合披露**——准确定性是「顶层 attestation 句未携带双计数」，而非隐瞒未披露。此语义
   套利空间我方承认并已消除：双计数正典见 amendment-5 §6，本信 frontmatter 起采用。
2. **P0-R4 时点**：route 冻结件预注册的合同是「零联网静态判断 + **执行首步**逐条核验 + 差异走
   版本化增补」；复审将核验时点提前至**签署前**，属对已签合同的时点收紧。我方如实点破此合同
   演化**并接受**：ACL 2026 证明静态判断可以 wrong-at-freeze，而签署对象不应包含已知为假的
   冻结事实——收紧有据。当日核验已执行完毕（39 个 URL 探针 + 8 佐证检索，amendment-5 §5）。

## §4 八项 P0 交付与机器清单

交付合同全文 = `2026-07-16-sf-protocol-amendment-5.md`（P0 对照表 §1、splitter 合同 §2、
validator V1–V13 §3、SF-L11+四分法+批次4 §4、route 裁定表 §5、双计数 §6、续62 指针 §7、
机械化动词纪律 §8）。

**签署清单（`docs/checks/2026-07-16-sf-package-summary.json` 机器生成，逐项证据文件回指）：**

| # | 项 | 机器状态 | 证据 |
|---|---|---|---|
| 1 | child splitter 合成回放（首 overflow=SPLIT_YEAR） | PASS（10/10） | `docs/checks/2026-07-16-sf-child-query-replay-test.json` |
| 2 | child splitter 真实冻结行集成 dry-run + 负测试 | PASS（17/17，55/55 真实行） | `docs/checks/2026-07-16-sf-child-query-realrow-dryrun.json` |
| 3 | REC-0/REC-2/claim-lineage validator（正例 0 退出+全负例子进程非零退出） | PASS（16/16） | `docs/checks/2026-07-16-sf-record-validator-test.json` |
| 4 | routes 结构 validator（v2 为 active 输入） | PASS（12/12） | `docs/checks/2026-07-16-sf-t1-routes-validation.json` |
| 5 | routes 外部状态审计证据件（39 个 URL 探针：200×28/404×3/403×1/CONN_FAIL×7；11 行无具体 URL 如实标注） | PASS（50 路全覆盖） | `docs/checks/2026-07-16-sf-t1-routes-status-audit.json` |
| 6 | sentinel 四分法（21 哨兵：QUERY_HIT×14/SEED×7/UNRESOLVED×0；held-out×2 均纯查询召回） | PASS | `docs/checks/2026-07-16-sf-sentinel-recall.json` |
| 7 | 陈旧口径扫描（active 签署面 forbidden token 零命中） | PASS | `docs/checks/2026-07-16-sf-package-summary.json` |
| 8 | 机器重数一致（92 seed/55 query/50 route 全唯一；prefix53 哈希钉定） | PASS | 同上 |

补充交付：Decision-Log 续62（owner 三裁决 + token 退役语义澄清，P0-R7）；routes v2
（ACL-2026→READY 唯一状态改判、ICML-2025 入口→v267 唯一入口改判，v1 不改写）；种子批次4
（含 TF-TTCL 旧日志行 241 转录失败在案登记，不称本轮首次发现）；SF-L11 词项 provenance
（全部复用既有词族，held-out VQQA 命中 5 条查询独立验证类目补救）。

## §5 owner 三裁决披露（Decision-Log 续62，2026-07-16）

- **裁决①**：接受 correction #4A 全部 8 项 P0，含 P0-R4 时点收紧（如实记录合同演化）。
- **裁决②**：D2 触发集扩张（`topic_relevance:"core"` 强制 D2）**直接接受**，不做前置吞吐
  估算——吞吐影响在执行中如实呈报 owner，不作为谈判筹码。
- **裁决③**：**机械化状态动词**——签署清单状态一律由 `sf_package_summary.py` 从证据文件
  推导，手填完成态废止（治本：G3 型夸张在结构上不再可能）。
- 执行选项：P0-R2 取选项 1（实装 `_year_windows`，三层合同保留——协议文本已冻结该语义且
  年层 API 探针更省）。

## §6 双向合同与窄幅复核申请（P0-R8）

复审 P0-R8 承诺「一轮窄幅复核 0 新 MAJOR、0 新 MINOR 且旧项全有可重放 evidence locator 即
签署」，与 correction #4 时的「全过即签、不再以可更完善为由延期」双向合同一并维持。我方
申请对象 = **本批提交后的新 commit + git blob bundle manifest**（两段提交：工件批 →
manifest 钉 blob，与 correction #3/#4 同构）。复核最低验收集七项（machine counts/旧 replay+
真实行集成/REC validator 正负/route 双层审计/sentinel holdout/双计数 reconciliation/历史件
未回写）逐项证据已在 §4 清单与 amendment-5 §1 给出 locator。

在签署 + owner 批准 + P0-R8 复跑三前置齐备之前：**discovery query 维持 0，模型触碰维持 0。**

—— 申请人：研究执行方（W1）。本件随提交入 git，blob 以提交为准；更正走 dated correction。
