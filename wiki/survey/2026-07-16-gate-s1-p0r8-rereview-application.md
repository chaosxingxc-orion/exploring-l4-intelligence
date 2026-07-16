---
artifact_id: "SF-S1-P0R8-APP-2026-07-16-01"
title: "Gate S1 P0-R8 窄幅复核申请书——correction #4A 送签件"
date: 2026-07-16
addressee: "Gate S1 评审人（search-design 签署权持有者）"
review_request_scope: "P0-R8 窄幅复核（复审 §7 P0-R8 原定范围）——不开 proposal 轮次，不重审科学件"
signature_object: "correction #4A 不可变集合：bundle manifest dated correction #4A（commit b7fd74b）钉定 31 件 + fixtures 树 @ commit af96a89；两 commit 均已推送 origin 并合入 master（merge 47f5a02）"
science_carrier: "科学件不在本次复核范围：proposal v3-consolidated 维持 ACCEPT AS WORKING THESIS（收档 @705b69a 轮），本申请不改动其一字"
attestation: "discovery_queries_executed = 0 维持；联网活动双计数 = amendment-5 §6 + access log（26 行 append-only）"
---

# Gate S1 P0-R8 窄幅复核申请书

## §1 申请范围与签署对象

按贵审《Correction #4 执行前博导式对抗复审》§7 P0-R8 约定，申请**一轮窄幅复核**。

- **复核输入 = 新 commit + git blob manifest，非工作树口头状态**（P0-R8 原文要求）：
  签署对象 = `wiki/survey/2026-07-15-sf-bundle-manifest.md` 的 **dated correction #4A 段**
  （commit `b7fd74b`），逐件钉定 31 个工件 blob + fixtures 树（`d930f3c17184`，15 件）
  @ commit `af96a89`。核验命令：`git rev-parse af96a89:<path>`。
- 两个 commit 已推送 `origin/research/stage1-directional-validation` 并以 merge `47f5a02`
  合入 `origin/master`——复核可在任意 checkout 上进行。
- **双向合同重申**：一轮复核 **0 个新 MAJOR、0 个新 MINOR，且所有旧项有可重放 evidence
  locator** → 签署；「全过即签、不再以可更完善为由延期」（correction #4 双向合同）继续有效。
  签署本身不背书 novelty 或科学效果（P0-R8 原文），签署后仍需 owner 执行批准，三方分立。

## §2 八项 P0 → 交付 → 机器证据（状态动词全部由脚本推导，无手填完成态）

| P0 | 交付 | blob @af96a89 | 机器证据 |
|---|---|---|---|
| R1 陈旧口径 | 协议/README/伴随报告口径统一（92 种子/55 查询/REC-0..7/amendments 1–5）；历史数字全部移入带标注段 | 协议 `6d6adf6c2dbf` | stale-token 扫描零命中 + 机器重数：`docs/checks/2026-07-16-sf-package-summary.json`（`55a66d9df0e8`） |
| R2 splitter | `_year_windows` 实装（三层合同保留，owner 选项1）+ `parent_from_frozen_row` 适配器（两类哈希机器分离）+ 续跑/查重规范函数 | `21422f672ca5` | 合成回放 **10/10**（首 overflow=SPLIT_YEAR，`ce71ae27af41`）+ 真实行 dry-run **17/17**（55/55 冻结行零 KeyError、负例全硬错误，`91378a4f9691`） |
| R3 validator | V1–V13 实装（含 D2-core 触发扩张、NA 类型稳定、INCLUDED⇒reason_code=null、flow 机器导出、threat 双人编码） | `f7a7c55812e9` | **16/16**，14 个负例**子进程级**非零退出（`2b1b7c53651e`）；fixtures 15 件落盘（tree `d930f3c17184`） |
| R4 routes | 当日外部状态审计（39 URL 探针：200×28/404×3/403×1/CONN_FAIL×7 失败码留痕）+ v2 supersession：**ACL-2026→READY（唯一状态改判，直连 200 A 级实证）、ICML-2025 入口→PMLR v267（唯一入口改判）**；v1 不改写 | v2 `8e0a5d3ebcee`，audit `6494ede500fd` | 结构 validator 对 v2 **12/12**（`3efef48872c1`）；裁定表 = amendment-5 §5（逐 route 机器形式 = v2 `status_audit_c4a` 块） |
| R5 sentinel | 四分法（QUERY_HIT/SEED/EXACT_ROUTE/REGISTERED_BOUNDARY/UNRESOLVED=FAIL）；coverage_note 仅注释；SF-L11（cs.MM/cs.MA）受控道，词项全复用既有词族；种子批次4（含 TF-TTCL 旧日志行 241 转录失败在案登记） | 数据 `d5b09fd62ba6`，测试 `79a16a3061f0` | 21 哨兵 **0 UNRESOLVED**；**两 held-out 均纯查询召回（VQQA×5 条含 SF-L11 两条——类目补救独立验证）**（`63b3d300a3b3`）；查询 55 行前 53 字节不变（prefix53 sha256 `75a59b2bf5ca…` 钉于 package summary）；种子 92 行前 87 字节不变 |
| R6 双计数 | `discovery=0`；`id_dereference = 21 canonical + ~25 aggregate-disclosed + 14 C4A 逐条`；新 access class 注册（VENUE_STATUS_CHECK / WEB_SEARCH_STATUS） | access log `483538082912` | amendment-5 §6（`f4e118051ee7`）；26 行 append-only，时间戳粒度如实声明 |
| R7 supersession | 续62 专段：三 token 权重职能全退役、登记职能迁入七维 reason/locator、venue_tier 仅存三职能；续61 不改写 | Decision-Log `6f179510f1cb` | `git diff 5cde3e3 b7fd74b -- wiki/Decision-Log.md` = 纯追加（0 删除行） |
| R8 本件 | 窄幅复核申请（新 commit + blob manifest 为对象） | 本件（自指钉定不可能，如实声明；blob 随提交外部可查） | —— |

## §3 P0-R8 最低验收集七项——逐项 locator 与复跑命令

复跑环境：WSL2 Ubuntu-24.04 + `~/.venvs/speechrl`（Python 3.12），与贵审 correction #4 重放
环境一致；全部脚本 stdlib-only、零网络（唯一例外见第 4 项说明）。从伞仓根目录：

| # | 验收项 | 复跑命令 | 预期 | 持久化证据 |
|---|---|---|---|---|
| 1 | machine counts / package consistency | `python scripts/survey/sf_package_summary.py` | PASS（八项全绿；92/55/50 全唯一；prefix53 哈希一致；stale-token 零命中） | `docs/checks/2026-07-16-sf-package-summary.json` |
| 2a | 编译链 | `python scripts/survey/sf_query_compiler.py` | OVERALL PASS（55 行；前 53 行 byte-identical 可 `git diff 5cde3e3 af96a89 -- wiki/survey/2026-07-15-sf-queries.jsonl` 目视为纯 +2 行） | queries jsonl `4cfd3b9063f0` |
| 2b | 旧 replay + 真实行集成/负测试 | `python scripts/survey/sf_child_query_replay_test.py && python scripts/survey/sf_child_query_realrow_dryrun.py` | 10/10 + 17/17；首 overflow event = `SPLIT_YEAR`；两次运行 bytes 一致（run_sha256 打印） | `ce71ae27af41` / `91378a4f9691` |
| 3 | REC/claim validator 正例+负例 | `python scripts/survey/sf_record_validator_test.py` | 16/16；正例 exit 0、14 负例子进程 exit≠0 | `2b1b7c53651e` + fixtures 树 |
| 4 | route live-status audit | 证据已持久化：`docs/checks/2026-07-16-sf-t1-routes-status-audit.json`（39 探针逐行 URL/UTC/HTTP 或失败码/正文 sha256）+ amendment-5 §5 裁定表 + `python scripts/survey/sf_t1_routes_validate.py`（对 v2 结构复验 12/12）。审计脚本本身联网、非确定性，**复跑可选**（`python scripts/survey/sf_t1_routes_status_audit.py`，约 15–30 分钟，将产生新的当日证据行） | 12/12 PASS | `6494ede500fd` / `3efef48872c1` |
| 5 | sentinel holdout outcome | `python scripts/survey/sf_sentinel_recall_test.py` | PASS：`UNRESOLVED_MISS=0`，`held_out_outcomes` = {2605.12978: QUERY_HIT, 2603.12310: QUERY_HIT}，held-out 未被种子污染（污染=FAIL 已编码） | `63b3d300a3b3` |
| 6 | network attestation reconciliation | 目视核对：access log 26 行（seq1–25+header）↔ amendment-5 §6 双计数 ↔ 回应信 frontmatter | 三处口径一致；discovery=0 | `483538082912` / `f4e118051ee7` / `96886f96c8f3` |
| 7 | 历史审计件未回写 | `git diff 5cde3e3 b7fd74b -- wiki/survey/2026-07-16-sf-t1-routes.jsonl wiki/survey/2026-07-16-gate-s1-correction-4-response.md wiki/survey/2026-07-16-sf-id-dereference-log.jsonl wiki/survey/2026-07-16-gate-s1-rereview-application.md wiki/survey/2026-07-16-sf-protocol-amendment-4.md` | **空 diff**（本方已预验证）；Decision-Log 为纯追加（0 删除行） | git 历史本身 |

## §4 主动披露（评审不必自行挖掘的诚实面）

1. **held-out 哨兵 n=2**——数量薄是事实；两篇均未入种子、未参与词项设计，且均以纯查询召回
   通过（非弱通道兜底）。执行期实测后可扩充 held-out 池。
2. **离线匹配器是 HIT 方向保守近似**（无词干化）：执行期须以真实 API 实测复核离线 QUERY_HIT
   （义务已写入 sentinel 报告 matching_caveat）。
3. **区域网络限制**：本机对 CVF/dl.acm/anthology 存在按连接随机的 TLS 拦截（audit 已实证并
   逐行留痕失败码）——执行期 T1 手扫需代理/OA 镜像预案，已列为执行前风险登记项。
4. **D2-core 吞吐未预估**（owner 裁决：直接接受、执行中呈报）——core 触发 D2 的实际篇数与
   耗时将在执行期如实报告，不作为重谈判据。
5. **5 个 NOT_YET route**（EMNLP/NeurIPS/IS/ICML/MM 2026）执行期间可能上线：走版本化增补
   （v3），不改写 v2。
6. **等待期计划**（评审 §6 允许范围自查）：arXiv 执行器/REC-7 写入器/ledger 骨架将离线实装
   （合成 oracle 干跑，零联网）——不构成提前执行；首条真实查询仍严格在签署 + owner 批准之后，
   且将生成 REC-1 事件。

## §5 请求

请按 §3 七项验收集执行窄幅复核。若一轮 0 新 MAJOR / 0 新 MINOR 且旧项 locator 可重放，
按双向合同签署 Gate S1 search-design gate（Stage-1A mapping execution）；签署不背书 novelty
或科学效果。签署后路径不变：reviewer 签署 → owner 执行批准 → 首条查询（REC-1 事件）。
在此之前：**discovery query = 0，模型触碰 = 0，维持不变。**

—— 申请人：研究执行方（W1）。本件随提交入 git，blob 以提交为准；更正走 dated correction。
