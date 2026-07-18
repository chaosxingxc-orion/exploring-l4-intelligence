---
artifact_id: "SF-V4-CLAIM-EVIDENCE-MATRIX-2026-07-18-01"
title: "Proposal v4 承重 claim 全量证据模式矩阵（amendment-9 §2 五值枚举）"
date: 2026-07-18
discipline: "五值互斥:MACHINE_RECOMPUTED_LOCAL / MACHINE_REPLAYED_STRUCTURE / SOURCE_REPORTED_TRACEABLE / REVIEWER_INFERENCE / TEAM_ATTESTATION;「独立复验」列只对本项目自己的复核动作作真——SOURCE_REPORTED 类永远填「否（引文定位抽查≠数字复算）」"
scope: "覆盖 v4 更正版全部承重数字与综合性结论;v4 散文自此只引本矩阵不重复 locator"
---

# v4 claim-evidence 矩阵

## §1 MACHINE_REPLAYED_STRUCTURE（九项门禁能力包络内;干净 archive + py3 stdlib 零联网可重放）

| claim | 复跑入口 | 独立复验 |
|---|---|---|
| 65 条冻结查询 / 14 查询 lane / prefix61 sha256 = 7d0d97c9… / 版本分层 48+3+2+2+6+4 | `sf_query_compiler.py` + canon | 是（评审 P0-R10 轮 9/9 + 我方多轮） |
| 92 种子 / prefix87 | `sf_package_summary.py`（canon 对账） | 是 |
| 34 哨兵 / held-out 6 / 0 UNRESOLVED / 四分法计数 | `sf_sentinel_recall_test.py` | 是 |
| 2607.09438→SF-L5-Q1、2512.19433→SF-L5-Q5（P0-R9 0-hit 表 2/7 异议之证） | 同上（哨兵 query_hits 机器输出） | 是（评审已独立确认并撤回原判） |
| 2603.24257→SF-L12-Q3（fresh L12 held-out 验收） | 同上 | 是 |
| ATLAS 5 命中（含 L14-Q1/L15-Q1）/ AutoTTS·Agentic-Coding 各中 SF-L2-Q1 / Team of Thoughts·ToolGate 零命中 | 离线 matcher（同实现;known-item DFS 件附复跑注记） | 是（与 v4 复审方双向复现一致） |
| 50 routes / 73 词表项 / 路由裁定 0 violations | `sf_t1_routes_validate.py` + `sf_t1_routes_adjudication_validate.py` | 是 |
| validator 26/26 / mutation harness 10/10 / 门禁全绿 | `sf_record_validator_test.py` + `sf_package_summary_test.py` + `sf_package_summary.py` | 是 |

## §2 MACHINE_RECOMPUTED_LOCAL（需 E: 本地数据;bundle 外）

| claim | 复跑入口 | 独立复验 |
|---|---|---|
| 引文校准:30 可解析 arXiv-ID × 107 存量交集空（ARXIV_ID_SUBSET_INTERSECTION_EMPTY,hypothesis-grade） | `sf_citation_calibration.py`（Seg-Agent eprint） | 是（本方重生成;识别覆盖缺口=债务 D-1） |
| fulltext 台账机器计数（known-item 批后 = 74/76 renditions / stale=0 / unresolved 2;数字以脚本最新输出为准,散文不冻结） | `sf_fulltext_ledger_status.py` → `docs/checks/2026-07-18-sf-fulltext-status.json` | 是 |

## §3 SOURCE_REPORTED_TRACEABLE（外部论文报告值——**九项门禁不覆盖;未独立复算**;效力限该论文报告的模型/任务/设置内）

| claim（v4 §3.2） | 来源 locator | 独立复验 |
|---|---|---|
| 可解析性修复 +~6pp;「~9% 链推理对不提交答案字母」 | 2607.09438 p.3–4 | 否（引文定位抽查过,数字未复算） |
| token 预算 1k→2k +3.7pp vs 8→16 链 +0.15pp | 2607.09438 p.4 | 否 |
| PRM-BAS vs flat SC:−0.39pp / 8.7× 成本;71.9% 题全 beam 同字母 | 2607.09438 p.4 | 否 |
| 换策略模型 +11.4pp;selector 双池 null(critic 精确 null/PRM +0.45pp n.s./转负) | 2607.09438 p.6–7 Table 4 | 否 |
| SC 高相关池回退（Chinese −2.8pp;22.3% 8/8 一致） | 2607.09438 p.7 | 否 |
| SC 把 Qwen3-VL-2B WeMath 35%→64%;4B+CoT 超 32B baseline | 2606.28864 p.8 | 否 |
| 指令遵循差→TTS 全失效;300-token 截断 perception 反升;>200 步丢 image-KV 几乎无影响 | 2606.28864 p.8–13 | 否 |
| SVF<GPT-4o（0.92 vs 0.95 / 0.66 vs 0.71 / 0.67 vs 0.74);HTS 5–6× 提速;弱模型增益更大(+20.2%/+16.8% vs +8.8%) | 2512.19433 p.7–8 Table 2 | 否 |
| 外部 verifier>内部 confidence 一致成立;弱开源 VLM self-refinement 退化 | 2512.11109 p.4–8 | 否 |
| ACL survey 明文不覆盖 audio | 2606.08231 p.10（两段拼接引,分别逐字核验） | 引文逐字核验=是;（此为范围陈述非数字） |
| ToolGate "learned controller"+"matched-domain trajectory training" | 2606.03054 abstract（逐字核验） | 引文逐字核验=是 |

（引文抽查覆盖声明：DFS 七篇批 11/12 + 本批 ToolGate/audio-exclusion 逐字命中——**只声称抽中
项的定位质量**,不代表全部事实逐字复核。）

## §4 REVIEWER_INFERENCE（跨论文综合/身份判断——我方编码产物,非机器事实）

| claim | 依据 |
|---|---|
| 组件级普查:七篇零篇同占「黑盒+单核+speech/omni+候选选择」四轴 | DFS 七篇件逐轴事实的集合运算;各轴引证在 DFS 件 |
| 「供给侧主导/选择侧边界」= 异质案例共同提示（非独立复制） | v4 §3.2 三栏综合;单观察 kill 判据同节 |
| 各篇角色建议（component-prior/boundary-comparator/navigation-only） | DFS 件逐篇「与本项目关系」节 |
| 系统级占据判断 = 13 轴 schema 编码产物（known-item DFS 件） | amendment-9 §3 + `2026-07-18-sf-known-item-dfs-systemcontrol.md` |

## §5 TEAM_ATTESTATION（签字承诺——台账在场性不能机器证明完整性,不称机器证明）

| claim | 载体 |
|---|---|
| discovery query = 0;systematic mapping 未执行 | 各批 access log + 本件签字 |
| new_model_touches_since_gate_freeze = 0（起算 af96a89） | exposure union §3 + 本件签字 |
| 联网活动全量入三本台账（access/atom/fulltext） | 台账文件 + 本件签字 |
| 未执行未登记的查询/模型调用 | 本件签字（TEAM_ATTESTATION 的定义域） |
