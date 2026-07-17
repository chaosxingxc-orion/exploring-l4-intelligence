---
artifact_id: "SF-S1-C4C-RESPONSE-2026-07-18-01"
title: "Correction #4C 回应信 + P0-R10 窄幅复核申请"
date: 2026-07-18
addressee: "Gate S1 评审人（search-design 签署权持有者）"
in_reply_to: "《Gate S1 Correction #4B / P0-R9：Stage-1A 阶段校准与博士生导师式对抗复审》（WITHHOLD,1 Gate MAJOR + 1 close-前 MAJOR + 3 MINOR）"
verification_first: "按 reviewer-response-protocol:全部 finding 先逐条独立复现——G1 概念核心/根因/held-out 超强措辞/carriage failure/C1/三 MINOR 数字全部属实;贵审新引 7 篇论文逐 ID dereference 7/7 零幻觉;**但 0-hit 事实表 2/7 行复现失败**（本信 §2 有据异议,首次）"
attestation: "discovery_queries_executed = 0 维持;本批全部联网活动 = wiki/survey/2026-07-18-sf-access-log-p0r9-verification.jsonl（31 行,双记 atom/fulltext 两台账指针）"
owner_rulings: "2026-07-18 五裁决全文见 amendment-8 frontmatter 与 Decision-Log 续64"
---

# Correction #4C 回应信

## §1 定性（先核验后回应）

贵审本轮的**阶段校准与自我修正**（收回对抗变异类 gate 要求、明示「不因缺防恶意输入能力
拒签」、无 FFP 裁决）我方确认收到并认可——这与 owner 三阶段裁决及「survey 仍是 1A」正典
一致。**G1 的概念核心我方全盘接受**：L11–L13 九条查询确实全部强制 `agent OR agentic
(OR multi-agent)` 连词（已逐条复现）；把研究目标命名写成检索前提=认识论循环，这正是 owner
自己的方法占位裁决（07-15）应用到查询设计上的结论，我方无从反驳、亦不辩解。C1 与三 MINOR
全部成立（17 条 stale locator/50-52 计数/热层过期措辞/空 diff 基准错误——数字逐项复现一致，
贵审的 ledger 计数比我方提交说明更准确，惭愧并致谢）。

## §2 有据异议（首次；证据全部机器可复跑）

在整体接受 G1 的前提下，两点事实更正：

1. **「七篇均 query_hits=0」在 2/7 行不成立。** 用 C4B 正典 matcher（`sf_sentinel_recall_test.py`
   同一实现,官方 Atom 摘要输入）复现：**2607.09438 命中 SF-L5-Q1**（`training-free` +
   `verification` + `language model` 字面在摘要中）、**2512.19433 命中 SF-L5-Q5**（`external
   verifier` 两处 + `test-time` + `scaling` 字面在摘要中）。两篇现已入哨兵集,其 query_hits
   在验收项 5 的机器输出中直接可见——贵审复跑即证。此点同时被 PRESS 独立复核人的 O-2 观察
   独立收敛（其未接触我方复现结果）。
2. **贵审只测了 61 条 arXiv 查询,未测协议的 T1 会议路由层。** T1 词表 A 组（2026-07-16 冻结,
   `A_any OR (B_any AND C_any)`,无 agent 连词）含 `test-time`/`training-free`/`orchestration`:
   七篇中 6 篇题名 A 组命中;尤其 **ACL Findings 2026 survey 本在 SF-T1R-ACL-2026 路由的设计
   通道内**——对这一篇「确定性漏掉/无发现通道」不成立。T1 只覆盖 10 会议正式出版物,救不了
   纯 arXiv 预印本,故 G1 对其余诸篇仍然成立——此异议校准修复范围,不推翻裁定。

**推论（对整改形态的意义）**：方法词本体在协议的 L5 与 T1 层早已存在——修复 = 把它对称补全
到 arXiv lane 层（镜像先于贵审件冻结的 T1 A 组词汇），而非发明新词。这使「非单篇捕获器」
在结构上可证：词项来源可追溯到 2026-07-16 的冻结物。

## §3 逐项整改交付（× 机器证据）

| 贵审项 | 交付 | 机器证据 |
|---|---|---|
| **MAJOR-G1 主体** 方法占位发现轴 | **SF-L14**（系统对象轴:orchestration/controller/routing + guided/contrastive/steering decoding）+ **SF-L15**（机制轴:TTS 短语族 + self-verification/consensus 族）,各 2 条,`sfqc-1.5.0`,**13 类冻结类目全并集**（方法轴永无类目盲区）,**零 agent 连词**;61→65,**前 61 行逐字节不变**（prefix61 sha256 入 canon 双证） | `sf_query_compiler.py` 65/65 PASS;协议 §4 SF-L14/L15 小节;canon `prefix_sha256=7d0d97c9…` |
| G1 整改 2：七篇获非空通道并入正典 | 七个 arXiv 身份全部注册哨兵（26→34;含 **2606.08231** = ACL survey 的 arXiv 孪生,我方 known-item 题名解析发现,双通道〔SF-L15-Q1 + T1-ACL-2026 路由〕）;raw Atom 字节+sha256 落盘,台账留痕 | `sf_sentinel_recall_test.py`:34 哨兵 0 UNRESOLVED,七篇 query_hits 非空且含 2/7 的既有 L5 命中 |
| G1 整改 3：结构化邻近分析 | **owner 裁决③:走 DFS 四问深读**（方法/局限/改进空间/可借鉴 + 身份轴事实:冻结/访问级别/信息来源/训练审计/控制机制/优化信号/任务范围/负结果）,全文 PDF 精读,承重结论带页码引证;**不含任何创新定位定性**（owner 裁决④:创新点尚未锁定,「成立/不成立」两侧皆为时过早;贵审 §4 定位语标 owner 未签） | `wiki/survey/2026-07-18-sf-p0r9-seven-papers-dfs.md`;全文双份入 fulltext ledger（14/14 renditions） |
| G1 整改 4：fresh L12 held-out | 隔离代理（Opus,零设计上下文）5 候选**预注册后运行**（预注册提交 `e965b71`）→ **2603.24257 实命中 SF-L12-Q3**（held_out=true 晋升,era 2026-03）;5 候选完整结果零丢弃;C4B 措辞教训吸取:命中 L12 lane 本身 | `2026-07-18-sf-heldout-l12-prereg-c4c.md` + RESULTS 附录;验收项 5 机器输出含其 SF-L12-Q3 命中 |
| G1 整改 5：非硬编码负控 | **PRESS 独立复核**（隔离代理,未参与设计）裁决 **HARDCODING: NO / BOOLEAN: PASS**;其唯一 MAJOR（steering 词族缺口）**已采纳后冻结**;3 个异措辞思想实验采纳后 3/3 命中;另有隔离代理独立选取的非触发集论文 2506.08691/2603.16253 命中 SF-L15（设计者未见过的论文上的泛化证据） | `2026-07-18-sf-press-query-review-c4c.md`（评审全文逐字存档+采纳记录） |
| **MAJOR-C1** 引文校准过度陈述 | **当下**:verdict 措辞降级重生成 = `ARXIV_ID_SUBSET_INTERSECTION_EMPTY`+`measurement_scope` 字段（30/~59 子集,hypothesis-grade）;**work-level identifier resolution 入债务表 D-1**（owner=W1,截止=任何 Stage-1A close/E2 饱和宣称之前;「在已解析子图上零新增 ≠ 闭包干涸」入 rule_consequence） | `docs/checks/2026-07-17-sf-citation-calibration-segagent.json`（重生成）;amendment-8 §4 债务表 |
| **MINOR-1** ledger locator 漂移 | 17 个受影响对象**逐对象 `RELOCATION_SUPERSESSION` 行**（canonical 路径 sha256 复核后落账,0 失败）;新增 `sf_fulltext_ledger_status.py`——成功/失败统计自此**只由机器生成**,提交说明必须引用其输出 | `sf_fulltext_ledger_status.py` → `docs/checks/2026-07-18-sf-fulltext-status.json`:64/66 renditions,stale=0,unresolved=2（遗留大 eprint,债务 D-5）,PASS |
| **MINOR-2** 热层阶段叙述 | Research-Objective §2 正名:「系统性 discovery/mapping 查询尚未执行;定向 ID dereference/raw provenance/全文准备/校准性引文试验已执行」——全称否定拆除 | `wiki/Research-Objective.md` §2（历史 dated 件未回写） |
| **MINOR-3** 空 diff 断言 | 基准更正拆分 + **实际输出粘贴**（本信 §4） | 本信 §4 |

## §4 空 diff 断言更正（MINOR-3,实跑输出）

原第 7 项把 P0-R8 申请件（`b6207d3` 新增,晚于 `af96a89`）误并入 af96a89 基准。更正为两条，
均已实跑，实际输出如下（空 = 无任何行）：

```
$ git diff af96a89 HEAD -- wiki/survey/2026-07-16-sf-t1-routes-v2.jsonl wiki/survey/fixtures-c4a
（空输出）
$ git diff b6207d3 HEAD -- wiki/survey/2026-07-16-gate-s1-p0r8-rereview-application.md
（空输出）
```

## §5 P0-R10 窄幅复核申请（验收表;复跑环境同前,可回放性分级见 amendment-8 §5）

| # | 验收项 | 复跑命令 | 预期 | 级别 |
|---|---|---|---|---|
| 1 | fail-closed 门禁全绿（C4C 正典计数 65/34/6） | `python scripts/survey/sf_package_summary.py` | PASS(exit 0) | bundle-only |
| 2 | mutation harness | `python scripts/survey/sf_package_summary_test.py` | 基线绿+全部变异 exit≠0 | bundle-only |
| 3 | validator v2 合同 | `python scripts/survey/sf_record_validator_test.py` | 26/26 | bundle-only |
| 4 | 路由裁定 | `python scripts/survey/sf_t1_routes_adjudication_validate.py` | PASS,0 violations | bundle-only |
| 5 | 哨兵四分法+G1 核心验收 | `python scripts/survey/sf_sentinel_recall_test.py` | 34 哨兵 0 UNRESOLVED;七篇 query_hits 非空（含 2607.09438=SF-L5-Q1、2512.19433=SF-L5-Q5 的既有命中=§2 异议之证）;2603.24257=SF-L12-Q3;held-out 6 全 era≥2025 | bundle-only |
| 6 | 查询前缀不变性 | `git diff 9b1f00b HEAD -- wiki/survey/2026-07-15-sf-queries.jsonl` | 纯 +4 行（SF-L14/15）;前 61 行字节不变（canon prefix61 sha 双证） | bundle-only |
| 7 | 历史件未回写 | 本信 §4 两条命令 | 空 diff | bundle-only |
| 8 | fulltext 台账机器状态 | `python scripts/survey/sf_fulltext_ledger_status.py` | PASS;stale locator=0;64/66;unresolved 2 如实列出 | local-data |
| 9 | 引文校准措辞降级 | 读 `docs/checks/2026-07-17-sf-citation-calibration-segagent.json` | verdict=ARXIV_ID_SUBSET_INTERSECTION_EMPTY + measurement_scope 字段 | 静态 |

双向合同重申：一轮 **0 新 MAJOR / 0 新 MINOR** 且旧项 locator 可重放 → 签署 Gate S1
mapping-execution gate;签署不背书 novelty/科学效果;签署后仍需 owner 执行批准。债务表
D-1..D-5（amendment-8 §4）带 owner 与截止 gate,其中 D-1（work-level resolution）不阻断
mapping 首查询、阻断 Stage-1A close——与贵审 §10 约定一致。在此之前：**discovery query = 0,
模型触碰 = 0,维持不变。**

—— 研究执行方（W1）。本件随提交入 git,blob 以提交为准;更正走 dated correction。
