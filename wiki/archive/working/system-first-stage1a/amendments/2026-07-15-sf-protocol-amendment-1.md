# 检索协议 amendment-1（v3 外审 P0-B/C 整改记录——取代关系与理由,不重写旧记录）

（性质：变更记录。协议本体为工作层文件已 supersede-in-place 更新;本件按 v3 外审 P0-D-III
要求显式登记每处取代关系与理由,旧字节在 git 历史。触发 = v3 外审
`2026-07-15-system-first-research-proposal-v3-stage1a-doctoral-review.md` 的 Gate S1 退回大修。）

| # | 变更 | 取代 | 理由（v3 外审条目） |
|---|---|---|---|
| A1-1 | 类目映射确定性冻结：SF-L1/L2/L4/L5 增补 cs.CV+cs.RO;SF-L3 再加 cs.SD+eess.AS;SF-L6/L7/L8 维持 CL/AI/LG | 原「默认 CL+AI+LG,SF-3 加语音类」散文规格 | 4.1——CV/RO 盲区有实证（Affordance Harness 手工种子命中、系统检索召不回）。**L6–L8 不扩的纸面敏感性依据（数字机器重数更正,内审 MAJOR-3）**：黑盒优化/prompt 优化/Goodhart/评测经济学的发表重心在 *CL/*LG/*AI——seed 集内触及该三 lane 的种子 = **19 条**（60 行现值;快照期 18;机器重数,初稿「16」为口算已废）,**题录级初判**无一主类为 CV/RO（主类未逐条登记,此为题录级初判非登记证据,执行期解析校正,判错即扩类）;**eess.IV 敏感性（外审 4.1 点名,补裁决）**：同口径题录级初判零主类命中,不预扩,执行中出现即版本化增补;溢出由 snowballing+SF-L9 兜底,不静默 |
| A1-2 | 48 条查询离线编译冻结为 `2026-07-15-sf-queries.jsonl`（compiler `scripts/survey/sf_query_compiler.py`,逐行 decoded/URL-encoded/分页字段/行哈希,零占位符）+ 静态验证报告 | 原「装配规则」散文模板（含条件占位符） | 4.2——「48 片段≠48 条最终请求」;编译属 Stage-1A 静态工作,非查询执行 |
| A1-3 | 可回放承诺分层：请求定义可复现+原始响应留存+派生集合可重建;撤回「逐字节一致 universe」表述 | v3 §7 与协议早稿的字节级承诺 | §7.2-II——API 返回不保证字节一致,过度承诺=治理表述失真风险 |
| A1-4 | 溢出/分页规则：max_results=每页大小;分页抓全 totalResults;>2000 按年度子窗确定性拆分;全程留痕禁无声截断 | 原 75 条 cap 无溢出语义 | 4.3——完整性控制,与 owner「不设预算 cap」裁决显式区分 |
| A1-5 | 16 条副源路线 manifest（`2026-07-15-sf-secondary-routes.md`:route ID/接口/停止/导出/证据;OpenReview API 类=REPLAYABLE_API,网页类如实标 DISCOVERY_ONLY 并回稳定 ID 锚） | 原「关键词串」级描述 | 4.4——检索意图≠可回放路线 |
| A1-6 | 新增 SF-L9 foundational lineage 道（4 经典 DOI 种子,chaining 为主,无 2022 窗限,统计隔离,独立停止规则）——RL 命名裁决依据 | 原八道皆 2022 窗 | 4.5/3.3——基础谱系缺失则 RL vs planning/metareasoning 无从裁决 |
| A1-7 | seed manifest 增量批次1（+9=60）：v3 外审 delta 5 条（OmniAgent/CMA-Harness/UCT-ToolCreator〔scope_pending=Y〕/ConMem/Argos）+ 基础谱系 4 条;§5bis 增量批次机制首次实际使用 | 快照 51 | 3.2/P0-C——直接威胁与概念祖先补入,发现路线全留痕 |
| A1-8 | threat 首轮队列 13→15（Affordance/FineVerify 晋升）;OmniAgent/CMA/UCT-ToolCreator/ConMem 待判定入池;Argos 次优先;「非硬上限」明文化;增删须记发现路线,禁只提升利己文献 | 原「首批 13 篇（可增至 15）」 | 4.6——核心威胁池必须优先覆盖最可能杀死身份的工作 |
| A1-9 | 纳排 schema 增设每篇 `most_threatened_rq` 字段（多值枚举 = RQ-SYS/RQ-CTRL/RQ-OMNI/RQ-SAFE/RQ-MEASURE/none〔none 须附一句理由〕,问题树定义锚 = v3 提案 §3;§11 kill matrix 按此聚合;协议 §6 与 T2 模板同步） | 原 §6 十轴+TF 审计+范围多轴 schema 无该字段 | P0-C 末项「对每篇记录…最可能推翻的 RQ」——首轮整改遗漏,签署级亲验复核（续55）发现补录 |

**S1-E 验收映射**：E1=v3 errata（v3 修订记录节）;E2=queries.jsonl+哈希;E3=A1-1+A1-4;
E4=A1-5;E5=A1-6+A1-7;E6=bundle manifest（另件,提交后钉哈希）;E7=v3 内审补归档
（docs/checks/2026-07-15-proposal-v3-hostile-review-lenses.md,含迟归档如实说明）;
E8=静态验证报告（联网查询数=0）。八件齐备后重新申请 Gate S1 search-design 签署。
---

# amendment-2（owner 检索策略四裁决,续57——签署前设计变更,零查询状态下并入）

| # | 变更 | 取代 | 依据 |
|---|---|---|---|
| A2-1 | **检索宇宙 = arXiv 唯一**：48 条编译查询不变;16 条副源路线整体退役（文件挂退役横幅留档）;chaining/种子解析发现的一切候选回 arXiv 题名检索;SS/OpenAlex 仅作引文图谱发现层,其命中同样回 arXiv 解析 | 协议 §2 多库设计 + 副源路线 manifest;**同时取代 v3 外审 4.4（副源可回放路线）与修正案 C（CVF/ISCA/PMLR 回链义务）——owner 设计定夺,冲突已披露,reviewer 签署时可表态** | owner 裁决①:单一可复现宇宙;可回放性升级（arXiv API 全程 REPLAYABLE）;覆盖代价以 REMOVED_UNOBTAINABLE 计数显式报告,不静默 |
| A2-2 | **venue 三梯队字段** `venue_tier`：T1 = {ACL, EMNLP, NeurIPS, ICML, ICLR, CVPR, ICCV, ACM MM, ICASSP, INTERSPEECH} 正会（冻结清单,「等」的扩充走版本化增补,AAAI/IJCAI 等暂归 T2）——第一优先参考;T2 = 其他（未发表 preprint/期刊/非 T1 会议）;T3 = workshop——**默认不参考**,例外须登记理由（EXCLUDE_DEFAULT_LOGGED_EXCEPTION）。venue 判定 = arXiv comments/journal-ref 字段 + 题名交叉核对,系**注解步骤**非检索路线 | §6 纳排矩阵（无梯队字段） | owner 裁决② |
| A2-3 | **顶会获取规则**：T1 论文一律题名检索回链 arXiv;不在 arXiv → 原文**备份本地** `$SPEECHRL_DATA_DIR/survey-backups/`（永不进 git,sha256+来源 URL 入 L3 日志）;无法备份 → `REMOVED_UNOBTAINABLE`（登记计数）。**SF-L9 四篇经典同适用**（非 arXiv 经典 = 备份 fallback,默认处置待 owner 如有异议再改） | ——（新增规则） | owner 裁决③ |
| A2-4 | **核心 topic 钉定入协议 §1**：how to build omni agentic system（包括但不限于多模态知识系统）;主研究方向 = **语音模态**;其他模态与单模态成果 = **技术要素参考**。新字段 `topic_relevance ∈ {core(语音/omni agentic 本体), element(技术要素参考)}`。检索广度不收窄（Checkpoint A 四域维持）,本裁决管**优先级/编码/报告侧重** | §1（无 topic 优先级表述） | owner 裁决④前半 |
| A2-5 | **执行策略 = BFS→触发式 DFS**：BFS pass = 全部查询命中做题录/摘要级编码（DISCOVERED/ABSTRACT_VERIFIED）;**DFS 触发三判据** = topic 很相似 ∨ 工作目的相似 ∨ 解题方法可借鉴（`dfs_trigger` 字段登记触发理由,多值）;DFS = 全文抽取（FULLTEXT_OPENED+）+ backward/forward chaining。**60 列名种子 = 预判定 DFS 集**（满足外审 P0-LIT-3-③ 种子 chaining 要求）;threat 首轮 15 篇维持;饱和判据不变（连续两轮零新增 DIRECT） | §5 全种子+全命中均匀 chaining 的隐含语义 | owner 裁决④后半:全文精读预算集中到真正相邻的工作 |

**S1-E 验收影响**：E4（副源路线）→ 语义变更为「A2-1 退役声明 + 备份规则」;其余 E 项不变。
**attestation**：amendment-2 并入时联网检索查询执行数 = 0。

## amendment-2 增补行（owner 批复与规则系统定稿,同日续57 后半）

| # | 变更 | 依据 |
|---|---|---|
| A2-6 | **方法占据编码（批复③研究观）**：DFS 每篇四问强制（方法是什么/局限在哪/**改进空间**/可借鉴）;占据结论禁止只写 occupied;改进空间**三小问**判有效（哪条轴/为何现有方法到不了/到了对哪个 RQ 或阈值有实质影响）;候选问题输出每个附「改进空间+为什么值得占」;kill/pivot 重述:名词被占≠kill,方法被占且**无有价值改进空间**才触发 pivot | owner:「不关注名词是否被占用,聚焦方法是否被占用…改进空间…渐进式提升边界」 |
| A2-7 | **T1 定向发现道**：十会（T1 清单）× 2022–2026 proceedings 题录扫描（发现层,题目级,每会每年一 route ID——proceedings 目录静态,可回放优于网页搜索）,topic 关键词过滤 → 回 arXiv 题名解析/备份流程 | owner 批复②:「高价值论文被淹没在海量搜索」——泛 relevance 排序的信号稀释盲区 |
| A2-8 | **梯队证据权重规则**：T1 实验结论直接承重;T2 创新/机制可承重、**实验数字强制带 `T2_UNREVIEWED` 限定**（不得单独支撑 kill/proceed,须 T1 佐证或 1B 探针自证）;**梯队管证据权重不管阅读优先级**（优先级=排序键:威胁度↓/core-element/时新↓/梯队平局裁决） | owner 批复②:「T2 创新性足够但缺同行评议,实验或不充分」 |
| A2-9 | **全文强制**：凡承重引用（差异点/借鉴点/占据判断）必须全文在手（arXiv/本地备份）且读过;摘要级只作存在性登记;SF-L9 经典同等适用,无全文即移除,不设二手转述例外 | owner 批复③:「可复现+可获取,一定要读原文全文」 |
| A2-10 | **DFS 触发第四判据 + 排序键**：T-d 结论冲突/威胁反证（`most_threatened_rq≠none` 锚）;队列字典序 = (威胁度↓, core/element, 时新性↓, 梯队↑) | owner 批复④:「你的想法没有错…总得有一套规则,不能随机游走」 |
| A2-11 | **引文图遍历五层防爆栈**（§5 重写）：只从 DFS 节点扩展/边过滤（方法谱系边+对比引用边,背景引用不遍历）/COMMON_NODE 剪枝（≥3 图共现且不触发=登记不扩展,触发者全局只析一次）/visited-set 全局去重/饱和停止;边价值排序 forward-对比最优先 | owner:「不想半径爆炸…深度遍历=引文图结构…公共部分不纠结,重点是方法论相同或对比引用的论文」 |

**attestation**：上述并入时联网检索查询执行数 = 0。
