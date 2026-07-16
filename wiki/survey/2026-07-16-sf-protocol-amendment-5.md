---
artifact_id: "SF-PROTOCOL-AMENDMENT-5-2026-07-16-01"
title: "检索协议 amendment-5——correction #4A（博导复审 8 项 P0 的合同化交付）"
date: 2026-07-16
trigger: "《Gate S1 Correction #4 执行前博导式对抗复审》裁决 WITHHOLD — CORRECTION #4A REQUIRED；owner 三裁决 = Decision-Log 续62"
supersedes: "amendment-4 中『validator 规则（纸面承诺）』段——自本件起为已实装引用；协议 §4 计数口径 53→55；seed 构成 87→92；routes 正典 v1→v2（v1 保留为历史件不改写）"
attestation: "discovery_queries_executed = 0 维持；本轮全部联网活动分类留痕（§6 双计数）"
---

# Amendment-5：correction #4A 八项 P0 交付与合同化

## §1 P0 对照表（状态动词一律由 `sf_package_summary.py` 机器推导，本表只给合同与证据指针）

| P0 | 交付 | 合同/证据 locator |
|---|---|---|
| P0-R1 | 单一正典合同：协议 title/§1/§4/§4bis/§5/§12 陈旧口径清理（74→92 种子、53→55 查询、REC-1..7→REC-0..7、amendments 1–3→1–5）；历史数字全部移入带「历史口径/HISTORICAL_SUPERSEDED」标注段 | stale-token 扫描 + 机器重数 = `docs/checks/2026-07-16-sf-package-summary.json`（`scripts/survey/sf_package_summary.py`） |
| P0-R2 | splitter 真实输入合同（§2） | `docs/checks/2026-07-16-sf-child-query-replay-test.json` + `docs/checks/2026-07-16-sf-child-query-realrow-dryrun.json` |
| P0-R3 | REC-0/REC-2/claim-lineage validator 实装（§3） | `scripts/survey/sf_record_validator.py` + `wiki/survey/fixtures-c4a/` + `docs/checks/2026-07-16-sf-record-validator-test.json` |
| P0-R4 | 50 route 当日外部状态复核 + v2 supersession（§5） | `docs/checks/2026-07-16-sf-t1-routes-status-audit.json` + `wiki/survey/2026-07-16-sf-t1-routes-v2.jsonl` + 结构 validator 输出 |
| P0-R5 | sentinel 四分法 + SF-L11 受控道 + 种子批次4（§4） | `docs/checks/2026-07-16-sf-sentinel-recall.json` + queries 55 行（前 53 字节不变）+ manifest 92 行 |
| P0-R6 | 网络访问双计数 attestation + access class 追认（§6） | `wiki/survey/2026-07-16-sf-access-log-c4a-review-verification.jsonl`（26 行 append-only） |
| P0-R7 | Decision-Log supersession 矛盾消除 | Decision-Log **续62**（token 退役语义澄清段） |
| P0-R8 | 新 commit/blob bundle 窄幅复核申请 | 回应信 + bundle manifest dated correction #4A（两段提交后钉定） |

## §2 P0-R2：child splitter 真实输入合同（选项 1，owner 批准）

- **三层合同保留并实装**：`ROOT→YEAR→MONTH→DAY`，新增 `_year_windows`（日历年窗口，clip 到
  闭区间父窗口）；**真实跨多年 root 的第一个 overflow event 必为 `SPLIT_YEAR`**（验收原文，
  realrow dry-run check C1）。
- **冻结行适配**：执行器必须经 `parent_from_frozen_row` 进入 `split_query`——由
  `decoded_search_query` 计算 `query_sha256`（decoded 串哈希）；`record_sha256`（整记录哈希）
  仅以 `frozen_record_sha256` 名义保留为 provenance，**两类哈希机器强制分离**（声明不符 =
  硬错误）。compiler 输出格式不变（无破坏性 vNext）。
- **续跑/查重规范函数**：`remaining_after`（未知恢复点=硬错误）、`assert_unique_ids`
  （落账前重复 child ID=硬错误）。
- **负测试集**（全部真实触发非零语义）：缺 submittedDate / 缺 decoded / 声明 hash 不符 /
  跨 2022–2026 root overflow（首事件 SPLIT_YEAR,年窗口=5）/ 月 overflow（拆日 31）/ 单日
  overflow（`API_LIMIT_SINGLE_DAY_OVER_2000` 硬停止登记）/ 闭区间边界 clip 保界 / 重复
  child ID / 恢复点续跑精确后缀 / 两次运行逐字相同。
- REC-1 模板 `split_level` 枚举同步为 `YEAR|MONTH|DAY`（blank-templates 已改）。

## §3 P0-R3：record validator 合同（V1–V13，不再是纸面承诺）

`scripts/survey/sf_record_validator.py` 机器强制（正负 fixtures 落盘
`wiki/survey/fixtures-c4a/`，负例经**子进程**验证非零退出）：

V1 REC-0 canonical_id 唯一；V2 source_hits 非空且 source 可解析、hit_ref 非空；V3
screening_stage/decision 枚举漂移=FAIL；**V4 INCLUDED ⇒ rec2_backref 可解析回指 + reason_code
必为 null（消模板歧义）**；V5 EXCLUDED/UNOBTAINABLE ⇒ 枚举 reason_code+非空 reason_text，
DUPLICATE ⇒ `DUPLICATE_OF:<id>`；V6 coding_depth 枚举 + INCLUDED 不得 D0 + REC-0/REC-2 深度
一致；V7 REC-2 id 唯一 + rec0_backref 回指 INCLUDED 行；**V8 D2 触发 = 被承重 claim 引用 ∨
initial_tag 含 DIRECT_THREAT ∨ `topic_relevance:"core"`（评审扩张，owner 续62 直接接受，
吞吐执行中如实呈报）**；V9 D2 全合同（必需块为真对象、七维 study_quality 每维 verdict 枚举+
reason、非 NA 必带 locator、coder 非空、claim_locators 非空）；**V10 NA 折叠唯一合法形态 =
`{"status":"NA","reason":"<非空>"}`——裸字符串 `"NA:..."` 与空字符串伪装完成 = FAIL**；
V11 承重 claim 只能回指 D2 行；**V12 flow 五计数由 REC-0 机器导出，手填不一致 = FAIL**；
V13 DIRECT_THREAT 行必带 `threat_dual_coding`（双抽取人相异 + rec5_ref + 有分歧必有裁决人）。

## §4 P0-R5：SF-L11 受控道、sentinel 四分法、种子批次4

- **SF-L11（cs.MM + cs.MA）**：Q1/Q2 见协议 §4；**词项 provenance——逐词复用主 lanes 既有
  词族**（身份族 training-free/test-time/inference-time/tuning-free/without fine-tuning ←
  SF-L1/L2；agent/agentic/multi-agent ← SF-L1/L6；模态族 multimodal/audio/video/visual/omni ←
  SF-L3/L5；反馈族 prompt optimization/self-reflection/feedback/self-improving/self-correction/
  self-evaluation ← SF-L1/L4），**未参照任何 sentinel 摘要挑词**（防循环验收）；编译层
  sfqc-1.3.0 append-only，55 行文件前 53 行逐字节不变（package summary 钉 prefix53 哈希）。
- **sentinel 四分法（取代 EXPLAINED_MISS）**：`QUERY_HIT / SEED_GUARANTEED /
  EXACT_ROUTE_GUARANTEED / REGISTERED_BOUNDARY(须回指 dated amendment) / UNRESOLVED_MISS=FAIL`；
  `coverage_note` 仅注释绝不转换 outcome；输入计数从 JSONL 实时读取；**held-out 纪律**：
  held_out 哨兵不得入种子（污染=FAIL）、其摘要不得参与词项设计。当前 21 哨兵结果：
  14 QUERY_HIT + 7 SEED_GUARANTEED + 0 UNRESOLVED；**两个 held-out（VQQA 2603.12310 /
  Useful-Memories 2605.12978）均纯查询召回通过——VQQA 命中 5 条（含 SF-L11 两条），cs.MM/
  cs.MA 盲区补救获独立验证**。
- **种子批次4（87→92）**：评审 §4.2 五篇 P0 直接近邻入 manifest（AMC/TF-TTCL/EvoLib/
  MappingSmarter-TTRL/MAR3，逐条带 ID_DEREFERENCE 留痕与威胁编码标签）；**TF-TTCL 行如实登记
  『2026-07-14 旧日志行 241 首次发现、未转录』的知识组织失败 provenance（评审 QRP-5），不称
  本轮首次发现**。§4.3 两篇 P1（Useful-Memories/VQQA）列为 **execution-early priority**（执行
  BFS 首轮即精读），兼任 held-out 哨兵故**不入种子**。

## §5 P0-R4：route 状态复核裁定表（结构 validator 与外部审计分立报告）

**分层证据**：A=直连 HTTP（`docs/checks/2026-07-16-sf-t1-routes-status-audit.json` 逐行
URL/UTC/HTTP 或显式失败码/正文 sha256）；B=代理取回信号；C=官方页 web-search 佐证（access
log seq 引用）；D=直连被区域性拦截（显式失败码留痕，状态裁定依托家族级 B/C 证据）。逐 route
机器形式 = v2 每行 `status_audit_c4a` 块。**本地网络对 aclanthology/nips/openreview/thecvf/
isca 存在按连接随机的 TLS 拦截（同域名同日有的连接 200、有的被 reset）——失败码如实留痕，
不冒充 venue 侧事实。**

**直连实测分布（audit 工件 39 个 URL 探针 = 35 exact_url + 4 家族 hub）**：HTTP 200 ×28、
HTTP 404 ×3（恰为 EMNLP/NeurIPS/IS 的 2026 行——404 即 NOT_YET 的当日实证）、HTTP 403 ×1
（dl.acm bot 拦截）、CONN_FAIL ×7（全部 CVF 域 TLS 区域性拦截）；另 11 行无具体 URL（3
NOT_HELD + MM/ICASSP 2023–26 八条 pattern 行）如实标注 `NO_CONCRETE_URL`，状态由家族证据
裁定。

| venue | 裁定 | 证据 |
|---|---|---|
| ACL 2022–26 | READY×4 维持；**ACL-2026 NOT_YET_PUBLISHED → READY（唯一状态改判，wrong-at-freeze 更正）** | **A：五个事件页直连全 200，acl-2026 title=「64th Annual Meeting…」**；+C（seq11 会期 7/2–7 已过；seq12 `2026.acl-long.0` 六卷已出版）；另 B 信号（代理取回超 10MB 内容上限） |
| EMNLP 2022–26 | 维持（READY×4 / NOT_YET×1） | A：2022–25 直连 200 ×4；**emnlp-2026 直连 404 = NOT_YET 当日实证**；+C（seq21：2026-10-24~29 布达佩斯） |
| NeurIPS 2022–26 | 维持（READY×4 / NOT_YET×1） | A：2022–25 直连 200 ×4；**paper/2026 直连 404 = NOT_YET 当日实证**；+C（seq20：2026-12-06~12 悉尼） |
| ICML 2022–26 | 维持 READY×4 / NOT_YET×1；**ICML-2025 入口 ENTRY_TO_RESOLVE → EXACT_URL v267（唯一入口改判）** | A：卷页+索引直连 200 ×5，v267 = 42nd ICML（2025-10-06 出版，seq9）；索引无 2026 卷 = NOT_YET 实证 |
| ICLR 2022–26 | 维持 READY×5 | A：openreview group 直连 200 ×5（含 ICLR 2026，会期 2026-04 已过） |
| CVPR 2022–26 | 维持 READY×5 | D+C：CVF 域 TLS 握手超时（区域性，失败码 ×5 逐行留痕）；seq24：CVPR2026 proceedings 2026-05-23 出版、4090 篇 |
| ICCV | 维持（READY 2023/2025；NOT_HELD 2022/2024/2026） | D+C：held 年直连被 reset（失败码留痕）；seq25：双年制奇数年，2026 无会 |
| ACM MM 2022–26 | 维持（READY×4 / NOT_YET×1；入口仍 ENTRY_TO_RESOLVE 属预注册合同） | D+C：dl.acm.org 403（bot 拦截，失败码留痕）；seq23：MM2026 = 2026-11-10~14 里约 |
| ICASSP 2022–26 | 维持 READY×5（per-year punumber 仍 ENTRY_TO_RESOLVE，合同不变） | A：ieeexplore conhome hub 直连 200 |
| Interspeech 2022–26 | 维持（READY×4 / NOT_YET×1） | A：2022–25 直连 200 ×4；**interspeech_2026 直连 404 = NOT_YET 当日实证**；+C（seq22：2026-09-28~10-01 悉尼） |

**v2 supersession 纪律**：v1（`2026-07-16-sf-t1-routes.jsonl`）原件不改写；v2 由
`scripts/survey/sf_t1_routes_v2_gen.py` 确定性生成并重算逐行 record_sha256；结构 validator
自动以 v2 为 active 输入复跑；执行期字段保持全 null（V11 零扫描态不受影响）。

## §6 P0-R6：网络访问双计数 attestation 与 access class 追认

**双计数正典（自本件起唯一口径）**：

- `discovery_queries_executed = 0`（维持；本轮零发现性检索）。
- `id_dereference_accesses = 21 canonical logged + ~25 prior aggregate-disclosed`
  （correction #4 口径，log header 原文即为该 ~25 次的主动聚合披露）**+ 14 C4A 逐条留痕**
  （7 次评审引文核验 + 7 次 verbatim 摘要，access log seq1–7/13–19，重试次数逐条登记）。
- **新 access class 追认**（此前未注册，本件补注册；均为事实核查用途、无发现意图、结果不入
  语料）：`VENUE_STATUS_CHECK`（按已知 venue URL 核验出版/会期状态；逐 URL 留痕于 audit
  工件，预探脚本 `probe_hosts_c4a.sh` 入库）、
  `WEB_SEARCH_STATUS`（web 搜索仅核验会期/出版事实；本轮 8 次，检索词逐字登记 access log
  seq11/12/20–25，返回结果未用于扩充语料——与 discovery query 的区分 = 检索意图与结果用途
  双重判据，登记后接受审计）。`VENUE_STATUS_CHECK` 本轮总量更正口径 = 预探 14 次（probe
  脚本 8 + urllib 6）+ 审计脚本 39 个 URL 探针（重试逐行 attempts 登记）。
- **时间戳粒度如实声明**：C4A access log 首批 12 次为窗口级时间戳（header 声明，不称逐次）；
  此后事件逐条 append-only。未来每次 access 自发生时写事件行，transport retry 记 attempts。

## §7 P0-R7：Decision-Log supersession 矛盾

已由 **续62** 专段消除（`T2_UNREVIEWED`/`T1_DEMOTED`/`T2_PROMOTED` 权重 token 全退役；
「双向登记」职能迁入七维 reason/locator 与 REC-0 reason；旧 token 仅作历史 provenance；
venue_tier 仅存排序键/发现层三职能）。续61 原文不改写。

## §8 P0-R1：机械化状态动词纪律（owner 批准，防复发结构）

签署清单/回应信中的每个状态动词一律由 `scripts/survey/sf_package_summary.py` 从持久化证据
文件推导（PASS/FAIL/EVIDENCE_MISSING 如实显示），人工手填完成态自本件起废止——G3 型完成态
夸张在结构上不再可能：**没有证据文件就没有绿灯**。stale-token 扫描（forbidden tokens +
历史标注豁免）纳入同一脚本，active 签署面旧口径零命中为签署前置条件。
