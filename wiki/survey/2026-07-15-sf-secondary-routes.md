# 副源检索路线 manifest（16 条）——🗄 已退役（amendment-2 A2-1,owner 裁决①）

> **退役声明（2026-07-15）**：检索宇宙收敛为 **arXiv 唯一**（+T1 十会题录扫描发现道 + 备份
> 规则,见协议 §2 现行版）;本 16 条路线整体退役,留档作历史记录,**不执行**。原 v3 外审 4.4
> 的多库要求由 owner 设计裁决取代,冲突已在 amendment-2 披露。

（可回放等级三类：`REPLAYABLE_API`=接口可确定性重放;`DETERMINISTIC_WEB`=URL 参数化、结果可
导出复核;`DISCOVERY_ONLY`=网页排序不可确定性重放——**其命中一律回 DOI/arXiv/OpenAlex 稳定
标识核验,网页排序不作 universe**。全部路线:执行时保存查询时间戳、结果页原始 HTML 或逐条
转录清单、以及命中→稳定 ID 的映射表。）

**通用字段**：route_id / 源 / 接口 / 完整查询 / 排序 / 时间窗(2022-10→2026-07-15;SF-L9 无
副源路线,不适用) / 页码与停止 / 导出 schema(title/authors/venue/year/stable_id) / 可回放等级。
**REPLAYABLE_API 分页冻结（内审 MINOR-9）**：OpenReview notes API 以 offset 分页抓至全量
（limit=1000/页）,时间窗按 note cdate 过滤,原始 JSON 全存;每页记 offset/limit/total 与
响应哈希。

| route_id | 源与接口 | 完整查询（逐字） | 停止规则 | 等级 |
|---|---|---|---|---|
| SF-L1-S1 | ACL Anthology 站内检索（anthology 搜索框） | `language agent environment feedback` | 前 5 页或 100 条,取先到 | DISCOVERY_ONLY |
| SF-L1-S2 | OpenReview API（notes 搜索,venue ∈ ICLR/NeurIPS/ICML 2023–2026） | `LLM agent test-time feedback` | API 全量返回（记录 total） | REPLAYABLE_API |
| SF-L2-S1 | OpenReview API（同上 venue 集） | `agentic test-time alignment feedback` | 同上 | REPLAYABLE_API |
| SF-L2-S2 | ACM DL 站内检索 | `inference-time control language model agent` | 前 5 页或 100 条 | DISCOVERY_ONLY |
| SF-L3-S1 | IEEE Xplore 站内检索,限 ICASSP/SLT/ASRU | `audio agent tool use LLM` | 前 5 页或 100 条 | DISCOVERY_ONLY |
| SF-L3-S2 | OpenReview API | `omni agent multimodal tool` | API 全量 | REPLAYABLE_API |
| SF-L4-S1 | ACL Anthology | `agent memory skill library` | 前 5 页或 100 条 | DISCOVERY_ONLY |
| SF-L4-S2 | OpenReview API | `LLM agent experiential memory no training` | API 全量 | REPLAYABLE_API |
| SF-L5-S1 | ACL Anthology | `training-free verifier LLM judge agent` | 前 5 页或 100 条 | DISCOVERY_ONLY |
| SF-L5-S2 | OpenReview API | `process reward training-free verification` | API 全量 | REPLAYABLE_API |
| SF-L6-S1 | OpenReview API | `black-box LLM optimization API-only` | API 全量 | REPLAYABLE_API |
| SF-L6-S2 | ACM DL | `compound AI system optimization` | 前 5 页或 100 条 | DISCOVERY_ONLY |
| SF-L7-S1 | OpenReview API | `reward hacking inference time best-of-n` | API 全量 | REPLAYABLE_API |
| SF-L7-S2 | ACL Anthology | `verifier gaming overoptimization` | 前 5 页或 100 条 | DISCOVERY_ONLY |
| SF-L8-S1 | OpenReview API | `agent evaluation cost budget pareto` | API 全量 | REPLAYABLE_API |
| SF-L8-S2 | ACM DL | `LLM agent cost-controlled evaluation` | 前 5 页或 100 条 | DISCOVERY_ONLY |

**领域正式版本回链义务（协议 §2,修正案 C）**：CVF Open Access / ISCA Archive / PMLR-NeurIPS
proceedings / AAAI-IJCAI 不设独立检索路线（其内容经 arXiv 主道 + chaining + 上表命中的回链
覆盖）——任何承重 claim 若正式版在上述库,locator 必须指向正式版页;若执行中发现某库有主道
覆盖不到的独立文献群,走版本化增补新开路线。

**排序与地区差异**：DISCOVERY_ONLY 路线记录检索时的排序设置与登录/地区状态;OpenReview API
按默认相关性并保存原始 JSON。