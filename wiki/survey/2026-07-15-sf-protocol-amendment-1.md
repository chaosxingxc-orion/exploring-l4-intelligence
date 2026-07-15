# 检索协议 amendment-1（v3 外审 P0-B/C 整改记录——取代关系与理由,不重写旧记录）

（性质：变更记录。协议本体为工作层文件已 supersede-in-place 更新;本件按 v3 外审 P0-D-III
要求显式登记每处取代关系与理由,旧字节在 git 历史。触发 = v3 外审
`2026-07-15-system-first-research-proposal-v3-stage1a-doctoral-review.md` 的 Gate S1 退回大修。）

| # | 变更 | 取代 | 理由（v3 外审条目） |
|---|---|---|---|
| A1-1 | 类目映射确定性冻结：SF-L1/L2/L4/L5 增补 cs.CV+cs.RO;SF-L3 再加 cs.SD+eess.AS;SF-L6/L7/L8 维持 CL/AI/LG | 原「默认 CL+AI+LG,SF-3 加语音类」散文规格 | 4.1——CV/RO 盲区有实证（Affordance Harness 手工种子命中、系统检索召不回）。**L6–L8 不扩的纸面敏感性依据**：黑盒优化/prompt 优化/Goodhart/评测经济学的发表重心在 *CL/*LG/*AI（seed 集内该三 lane 的 16 条种子无一主类为 CV/RO）;溢出由 snowballing+SF-L9 兜底;执行中发现主类 CV/RO 的直接命中即走版本化增补扩类,不静默 |
| A1-2 | 48 条查询离线编译冻结为 `2026-07-15-sf-queries.jsonl`（compiler `scripts/survey/sf_query_compiler.py`,逐行 decoded/URL-encoded/分页字段/行哈希,零占位符）+ 静态验证报告 | 原「装配规则」散文模板（含条件占位符） | 4.2——「48 片段≠48 条最终请求」;编译属 Stage-1A 静态工作,非查询执行 |
| A1-3 | 可回放承诺分层：请求定义可复现+原始响应留存+派生集合可重建;撤回「逐字节一致 universe」表述 | v3 §7 与协议早稿的字节级承诺 | §7.2-II——API 返回不保证字节一致,过度承诺=治理表述失真风险 |
| A1-4 | 溢出/分页规则：max_results=每页大小;分页抓全 totalResults;>2000 按年度子窗确定性拆分;全程留痕禁无声截断 | 原 75 条 cap 无溢出语义 | 4.3——完整性控制,与 owner「不设预算 cap」裁决显式区分 |
| A1-5 | 16 条副源路线 manifest（`2026-07-15-sf-secondary-routes.md`:route ID/接口/停止/导出/证据;OpenReview API 类=REPLAYABLE_API,网页类如实标 DISCOVERY_ONLY 并回稳定 ID 锚） | 原「关键词串」级描述 | 4.4——检索意图≠可回放路线 |
| A1-6 | 新增 SF-L9 foundational lineage 道（4 经典 DOI 种子,chaining 为主,无 2022 窗限,统计隔离,独立停止规则）——RL 命名裁决依据 | 原八道皆 2022 窗 | 4.5/3.3——基础谱系缺失则 RL vs planning/metareasoning 无从裁决 |
| A1-7 | seed manifest 增量批次1（+9=60）：v3 外审 delta 5 条（OmniAgent/CMA-Harness/UCT-ToolCreator〔scope_pending=Y〕/ConMem/Argos）+ 基础谱系 4 条;§5bis 增量批次机制首次实际使用 | 快照 51 | 3.2/P0-C——直接威胁与概念祖先补入,发现路线全留痕 |
| A1-8 | threat 首轮队列 13→15（Affordance/FineVerify 晋升）;OmniAgent/CMA/UCT-ToolCreator/ConMem 待判定入池;Argos 次优先;「非硬上限」明文化;增删须记发现路线,禁只提升利己文献 | 原「首批 13 篇（可增至 15）」 | 4.6——核心威胁池必须优先覆盖最可能杀死身份的工作 |

**S1-E 验收映射**：E1=v3 errata（v3 修订记录节）;E2=queries.jsonl+哈希;E3=A1-1+A1-4;
E4=A1-5;E5=A1-6+A1-7;E6=bundle manifest（另件,提交后钉哈希）;E7=v3 内审补归档
（docs/checks/2026-07-15-proposal-v3-hostile-review-lenses.md,含迟归档如实说明）;
E8=静态验证报告（联网查询数=0）。八件齐备后重新申请 Gate S1 search-design 签署。