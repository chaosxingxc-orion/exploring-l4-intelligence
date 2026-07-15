---
protocol_id: SURVEY-PROTO-2026-07-15-02
title: "System-first Survey 检索协议 v1+amendments 1–3——八 lanes + 基础谱系道 SF-L9 / arXiv-primary 语料+免费官方源救援·51 条编译冻结查询（48+3,A3-8）/ 梯队先验+质量三轴 / BFS→触发式 DFS / 74 列名种子（计数正典 = manifest 枚举）"
date: 2026-07-15
status: "DRAFT — 内审环后送 reviewer 签署;签署前零查询执行（queries_executed: 0,本行为 attestation）"
authorization: "重校准评审 Gate S1 = PROTOCOLIZATION_AUTHORIZED / QUERY_EXECUTION_STILL_PENDING;proposal v2（STAGE1A-PROPOSAL-2026-07-15-03,已转交）§11 为规格来源"
quality_bar: "严评 P0-LIT-3 八项最低规格全采 + 重校准 Checkpoint A–D 判据 + 开放抽取字段(Checkpoint B) + v2 评审修正案 A–F 全采（种子快照措辞/增量扫描/领域源/chaining 续行规则/选文留痕/范围多轴+TF 审计子字段）"
relation_to_survey_b: "SURVEY-B（selector 组件线 round-2 协议 SURVEY-PROTO-2026-07-15-01,21 lanes/105 查询）独立维持零执行、另行签署——本协议不修改不吸收它"
first_query_gate: "reviewer search-design 签署 + owner 批准 + P0-R8 状态门复跑三条件齐备后,才允许执行第一条查询"
hostile_review: "R1 双镜头（①事实/计数/一致性〔机器重数级〕;②术语+查询语法纸面可执行性,各 Opus 独立）：镜头1=0 MAJOR+3 MINOR（报告正文表系裁决前快照;『12 条挂标』为沿抄误计,机器 grep=10）;镜头2=2 MAJOR（arXiv exact-query 装配规则缺失——cat:/submittedDate 必须折入查询串,否则执行者自由度复现 round-1 检索宇宙分叉;manifest 字段词汇与 §3 自声明 schema 不对齐）+5 MINOR+NIT;星号通配符陷阱零命中（显式 OR 枚举）。修复后 R2=8/8 FIXED 但新鲜扫描 2 NEW-MINOR（窗口例外代入串不全;报告 §8 陈旧 21）→ NOT_CONVERGED;再修后 R3=2/2 FIXED+邻接零矛盾 → PROTOCOL_INTERNAL_LOOP_CONVERGED〔历史环记录,A3-10 立规前的裸 CONVERGED 于 2026-07-16 补锚〕（三轮,环上限内;环内判定≠外部签署）。原始报告归档 docs/checks/2026-07-15-gate-s1-protocol-hostile-review-lenses.md。**A3 批敌意环（2026-07-16,双镜头各 Opus 独立:①计数/一致性机器重数②G1–G6 闭合完备性）**：R1 = 1 MAJOR（Research-Methodology 阶段称谓残留）+ 4 MINOR + 2 NIT,零措辞违规、零越权宣称、G1–G6/P0-1..6 实质全闭合（bundle correction #3 与 occupancy version-pin 为已披露延后项）;修复后 R2 窄幅机器复检 = 全部 fix 落位、词表 73 项零通配符、schema 三处逐字对齐 → A3_BATCH_LOOP_CONVERGED@workingtree（钉定待 correction #3）"
---

# System-first Survey 检索协议 v1

## §0 目的与授权链

按 proposal v2 §11 实例化 Gate S1 检索协议：为 system-first 研究纲领（黑盒 omni agentic
system × training-free reward-guided external control,S0 已签）完成**可回放**的占据/机制
survey。授权链：重校准评审授权协议化 → v2 评审
`APPROVE_GATE_S1_PROTOCOL_DRAFTING_WITH_REQUIRED_AMENDMENTS`（修正案 A–F 已并入本稿）→
本协议成稿送签 → 签署后执行。round-1「检索宇宙永久缺失」教训 = 全部查询构造性可回放（§9）。

**引用钉死（v2 评审 §7.3）**：proposal v1 = `cf54f1b:wiki/2026-07-15-system-first-research-
proposal-v1.md`（blob `d60aa669…`）;proposal v2 = `cf54f1b:wiki/2026-07-15-system-first-
research-proposal-v2.md`（blob `20e5bd55…`）;暂定 taxonomy = v1 §2（随上述 blob 钉定）;
seed manifest 与本协议以各自提交后的 (commit, path, blob) 三元组互引。

## §1 覆盖判据与核心 topic（Checkpoint A + owner 裁决④,A2-4）

- **核心 topic（owner 钉定）**：**how to build omni agentic system**（包括但不限于多模态知识
  系统）;主研究方向 = **语音模态**;其他模态与单模态成果 = **技术要素参考**。每篇编码
  `topic_relevance ∈ {core, element}`——本裁决管优先级/编码/报告侧重,**不收窄检索广度**。
- **系统域**：text-agent ∧ VLM/omni-agent ∧ audio-agent ∧ compound AI system 四域全查。
- **机制轴**：search / reflection / memory / tool-routing / verification / non-parametric
  adaptation 全覆盖。
- **两侧查**：training-free 同口径 ∧ 训练型最强上界（TRAINED_COMPARATOR）都纳入,不做同温层
  检索。
- 每篇按开放字段抽取（§7）,允许新类别出现并版本化修订 taxonomy（§10）。

## §2 检索宇宙与承重源（A2-1..A2-3 重写,owner 裁决①②③——取代原多库设计）

- **检索语料 = arXiv-primary + 免费官方源救援（A3-1,取代 A2-1「非 arXiv 不参考」条）**：
  全部预注册检索经 arXiv API（51 条编译查询）;Semantic Scholar/OpenAlex 仅作引文图谱发现层,
  **其一切命中回 arXiv 题名检索解析**;无 arXiv 版的直接相关工作走**免费官方开放获取源救援**
  （ACL Anthology/NeurIPS proceedings/PMLR/OpenReview/CVF/ISCA Archive 等,venue-native ID/
  DOI + 本地备份 + sha256 纳入承重）;**付费且无任何免费版本 → `REMOVED_PAYWALLED_UNOBTAINABLE`**
  （计数移除记账——移除事件+ID+题名+venue 入 flow report,凡占据类/NO_DIRECT_MATCH 结论必须
  披露移除计数）。最终产出自称「arXiv-primary systematic mapping（免费开放获取救援+显式移除
  记账）」,不称 comprehensive universe。原 16 条副源路线整体退役
  （`2026-07-15-sf-secondary-routes.md` 留档）。
- **venue 三梯队（注解步骤,非检索路线;A3-2 修订为「先验非终裁」）**：`venue_tier`——**T1** =
  {ACL, EMNLP, NeurIPS, ICML, ICLR, CVPR, ICCV, ACM MM, ICASSP, INTERSPEECH} 正会（清单冻结,
  扩充走版本化增补）;**T2** = 其他（未发表 preprint/期刊/非 T1 会议）;**T3** = workshop——
  **不再按 venue 默认排除,按相关性/质量裁决**,EXCLUDED 必须记相关性/质量理由（A3-2）。
  判定依据 = arXiv comments/journal-ref + 题名交叉核对。
- **T1 定向发现道（A2-7,防高价值顶会论文淹没于泛 relevance 排序;A3-3 已实例化）**：T1 十会
  × 2022–2026 proceedings **题录扫描**（发现层,题目级;每会每年一 route ID——proceedings
  目录静态,可回放）,topic 关键词过滤 → 命中回 arXiv 题名解析或救援流程。**route 正典 =
  `2026-07-16-sf-t1-proceedings-routes.md`**（50 route ID/入口/track 界定/词表 v1/归一化与
  模糊匹配/五计数字段）,执行日志模板 = REC-7。
- **梯队证据权重（A2-8,经 A3-2 修订为「先验+质量双向覆盖」）**：`venue_tier` = **默认先验
  权重,非终裁**。T1 实验结论默认承重,study_quality 低者 `T1_DEMOTED`（登记理由降权）;T2 =
  创新/机制描述可承重,实验数字默认带 `T2_UNREVIEWED` 限定（不得单独支撑 kill/proceed）,
  **高质者（代码+复现+充分消融）经协调者裁决 `T2_PROMOTED` 可承重**（登记理由,限定语保留
  加注 override）;逐篇三轴分立 = `verification_depth / publication_status / study_quality`
  （schema 正典 = REC-2 evidence_axes）;**threat/novelty 判定不看梯队**（未发表工作同样可
  摧毁首创宣称）;**梯队管证据先验,不管阅读优先级**（优先级 = §4bis 排序键）。
- **T1 获取规则**：题名检索回链 arXiv;不在 arXiv → 免费官方源原文备份
  `$SPEECHRL_DATA_DIR/survey-backups/`（永不进 git;sha256+来源 URL 入 §9 日志）;付费且无
  任何免费版本 → `REMOVED_PAYWALLED_UNOBTAINABLE`;其他不可得 → `REMOVED_UNOBTAINABLE`
  （两类均登记计数——覆盖代价显式报告,不静默;A3-1）。SF-L9 经典同适用。
- **承重源与全文强制（A2-9,owner:「一定要读原始论文的全文」）**：arXiv 钉版本 vN（或本地
  备份件+哈希）;**凡被引用为差异点/借鉴点/占据判断依据的工作,必须全文在手且全文读过**;
  摘要级只作存在性登记、不支撑任何承重结论（五级分级沿用：DISCOVERED / ABSTRACT_VERIFIED /
  FULLTEXT_OPENED / CLAIM_VERIFIED / REPRODUCED）;SF-L9 经典同等适用,无全文即移除,不设
  二手转述例外。

## §3 Mandatory seeds——预协议种子快照（snapshot 2026-07-15;允许检索扩展）

**措辞纪律（v2 评审风险一）**：survey 完成前禁用「全集/完整占据图」表述——本表是**带截止日的
预协议快照**,执行起按 §5bis 增量批次滚动。

**构成（74 条列名 = 快照 51 + 增量批次1 九条 + 增量批次2 十四条〔A3-7,v3 收官就绪度评审
delta scan〕;另 22 条执行时裁决;计数正典 = `2026-07-15-sf-seed-manifest.jsonl` 逐行枚举,
零 ID 重复——此前草稿的「57/16」为协调者算术口径,按 P0-R8 原则以机器枚举更正;历史口径
「60」= 批次2 前）**：
⑥ **v3 外审 delta scan 5 项**（增量批次1,AS_GIVEN）：OmniAgent 2606.19341 / CMA-Harness
2607.08497 / UCT-ToolCreator 2602.01983（scope_pending=Y,更新对象待全文）/ ConMem
2606.08702 / Argos 2512.03438——初判多为训练型对照,不预判最终纳入;
⑦ **基础谱系 4 项**（增量批次1,SF-L9 专用,DOI 题录）：Russell-Wefald metareasoning 1991 /
Kaelbling POMDP 1998 / Sutton options 1999 / Kocsis UCT 2006。**执行期注记（A2-9 联动）**：
本 4 条现为题录级在册,全文/备份获取是执行首步;不可得者按 REMOVED_UNOBTAINABLE 移除——
「在册」≠「已接受」。
快照期五分类如下：
① v1 §4 表内 15 项（blob 见 §0 钉定）;
② 评审补充机制族 10 项（AWM/ExpeL/Self-Refine/CRITIC/TPO/HuggingGPT/AudioGPT/DSPy/TextGrad/
TTRL;题录 AS_GIVEN,执行时解析,失败标 UNRESOLVED）;
③ 自库反扫已列名 4 项（training-free-grpo / inference-time-reward-hacking /
walking-through-uncertainty / scaling-auditory,见 v2 §4）;
④ 自库反扫 STRONG 15 项（`2026-07-15-gate-s1-own-library-sweep.md`）;
⑤ **v2 评审 delta scan 新增 7 项**（AS_GIVEN_BY_REVIEW,执行时解析）：
**Omni-Decision (2607.11433)**——最高优先威胁:training-free omni-modal QA evidence-state
system（confirmed evidence/conflicts/依赖/停止的共享状态驱动闭环）,2026-07-13 提交;
**Affordance Agent Harness (2605.00663)**——verification-gated skill orchestration 闭环
runtime（evidence store/episodic memory/router/verifier/retry/cost control）;
**FineVerify (2606.00660)**——可验证子问题分解 + 轨迹细粒度自验证聚合;
**Effective Feedback Compute (2605.29682)**——「有效反馈算力」:资源轴的候选描述语言（§7）;
**MUSE-Autoskill (2605.27366)**——技能生命周期;**自库在案**（2026-06-30 归档 survey +
`papers/agent-level-tfrl/references.bib`,专职反扫亦漏——检索失效第四例,反扫范围已补
references.bib）;
**ACE (2510.04618)**——自反扫 MEDIUM 升列名（自库 06-30 系列在案,评审独立点名）;
**VeGAS (2605.12620)**——trained-verifier 边界对照:「测试时不改 policy ≠ 全系统
training-free」的典型反例。
执行时裁决层 = 反扫 MEDIUM 其余 22 项。

**种子定性备注（v2 评审 §2.2–2.3 收紧,全文核验前生效）**：training-free-grpo (2510.08191)
标「术语/机制威胁,**TF-Strict 归属待核**」（其外设经 ground-truth 多轮学习 token prior——
冻结核心 ≠ TF-Strict）;IRO (2506.17828) 标「frozen core + trained value fn 边界」;
walking-through-uncertainty 按 §6 范围多轴拆编（组件直接 ≠ 系统直接）;scaling-auditory
「最紧 omni 机制占据者」系**团队自评待全文核验**,协议内表述 =「音频域 TTC 强边界」。

**seed manifest（签署包组成部分,修正案 A;字段 enum 与 manifest 实值对齐——内审 MAJOR-2
闭合）**：`2026-07-15-sf-seed-manifest.jsonl` 每行 =
`{id, name, source ∈ {reviewer点名, 自库继承, 自库反扫, 评审delta-scan, 评审点名-基础谱系}
（执行期可扩: 数据库发现/chaining/作者页）, first_found_at(文件:定位), verification_level ∈
{题录AS_GIVEN, 题录AS_GIVEN|delta待全文核验, census在库(题录+), 摘要级}, lanes[]⊆{SF-L1..L9},
rationale, initial_tag[]?（A3-7,批次2 起用旧行不补——多值 ∈ {DIRECT_THREAT,
TRAINED_COMPARATOR, METHOD_LINEAGE, COMPONENT_ANALOGY},仅管阅读优先级不预判纳排结论）,
exclusion_reason?, scope_pending(Y/N), snapshot_date}`。**与登记 token 的映射**：题录AS_GIVEN
↔ AS_CITED_BY_REVIEW（题录级）;census在库(题录+) ↔ RETAINED_RECORDS@census-v2;
delta待全文核验 ↔ TO_VERIFY_FULLTEXT;执行期证据升级一律改记 §2 五级英文标尺
（DISCOVERED→…→REPRODUCED）,策展期中文值不再新增。快照截止 2026-07-15。

**已知工作处理**：命中 census v2 既有 works 者标 KNOWN（执行期去重标记,登记于 survey/README
token 块）仍全量登记（dedup 不丢日志）;新工作即读即登记 census/ledger schema（L3 规约,续47）;
**自库反扫范围永久包含 `papers/*/references.bib`**（MUSE 教训）。**attestation 边界声明
（内审 MINOR-5）**：manifest 内 `[lane 协调者已核]`/`既往 grep` 类注记 = 种子策展与历史
census 记录,发生于本协议 §4 查询之外且之前,不构成查询执行。

## §4 八条 lanes 与 51 条编译冻结查询（48 原批 + 3 条 A3-8 增补,append-only）

**通用规格**：默认引擎 = arXiv API;默认窗口 2022-10-01→2026-07-15（例外行内注明）;
max_results = 75（SF-L7-Q3 为 50）——**语义 = 每页大小,非结果上限**（溢出规则见下）;按
relevance 排序。**类目映射（amendment-1 确定性冻结,v3 外审 4.1）**：SF-L1/L2/L4/L5 =
cs.CL+cs.AI+cs.LG+**cs.CV+cs.RO**（agent/感知/记忆-技能/验证层——CoVer/Affordance/具身
agent 均属视觉-机器人域,类目盲区实证在案）;SF-L3 = 前五类 + cs.SD+eess.AS;SF-L6/L7/L8 =
cs.CL+cs.AI+cs.LG（黑盒优化/Goodhart/评测经济学文献集中于此三类——纸面敏感性依据见
amendment-1,snowballing 与 SF-L9 兜异类溢出;执行中发现反例即走版本化增补扩类）。
查询编号 = SF-L{n}-Q{m}（arXiv）。**各 lane 的 S1/S2 副源行已按 A2-1 整体退役**（下文保留
作历史记录,不执行）。允许执行中对拼写变体做**登记后**微调（原查询照跑,变体新增编号,禁替换）。

**exact-query 冻结正典（amendment-1,v3 外审 4.2 闭合;A3-8 后 51 条）**：51 条查询（48 原批
+3 增补——**原批 48 行逐字节不变、增补追加于文件末尾**,原批行保留 compiler_version
sfqc-1.0.0,增补行标 sfqc-1.1.0）已由离线编译器
`scripts/survey/sf_query_compiler.py` 装配为 **`2026-07-15-sf-queries.jsonl`**——逐行含
decoded/URL-encoded 串、类目、date_from/to、start/max_results/sortBy/sortOrder、compiler
版本与行哈希,**零占位符**;静态验证报告 `docs/checks/2026-07-15-sf-queries-static-validation.md`
+ 复跑报告 `docs/checks/2026-07-16-sf-queries-static-validation-rerun.md`（A3-8——证明
「当前协议 → 当前 compiler → 当前 queries.jsonl」链与原批 48 行字节前缀不变）。
**执行以 jsonl 为正典,本节文字仅人读参考**。窗口例外（SF-L2-Q3/SF-L3-Q3 = 2023-01 起;
SF-L7-Q3 = 2020-01 起）已折入各行。日期界约定：submittedDate 双闭区间,以 arXiv v1 提交时间
为准。**可回放承诺分层（v3 外审 §7.2-II）**：请求定义可复现 + 原始响应留存 + 派生集合可由
原始响应重建;不承诺 API 返回逐字节一致,接口侧漂移记为外部不确定性。

**溢出/分页规则（v3 外审 4.3——完整性控制,非预算 cap;A3-6 补递归 fallback）**：执行时读取
每查询 `opensearch:totalResults`,以 start 递增**分页抓取至全量**;若 totalResults > 2000
（arXiv API 实用界限）,按 **年 → 月 → 日** 子窗对该查询做**确定性递归拆分**直至每片 ≤2000
（单一子窗仍超限即降级到下一时间粒度,粒度穷尽则如实登记为接口极限）;派生查询
`query_id = <父ID>-W<窗口序号>`,REC-1 行内记 `parent_query_sha256`;每页保存 start/max_results
与原始响应哈希,totalResults 全程留痕——**禁止无声截断**。

**副源路线——已退役（A2-1）**：原 16 条副源路线（`2026-07-15-sf-secondary-routes.md`,曾为
v3 外审 4.4 的闭合方案）按 owner 裁决①**整体退役留档,不执行**;其发现职能由 §2 的 T1 十会
题录扫描道（可回放性更强）与引文图承接。对 v3 外审 4.4 与修正案 C 的取代已在 amendment-2
A2-1 披露,reviewer 签署时可表态。

### SF-L1 reasoning+acting 与环境反馈（ReAct/Reflexion/LATS 族）
- Q1 `abs:"language agent" AND abs:feedback AND (abs:"test-time" OR abs:"inference-time" OR abs:"training-free")`
- Q2 `ti:agent AND (abs:"self-reflection" OR abs:"verbal reinforcement" OR abs:reflexion)`
- Q3 `(abs:"reasoning and acting" OR abs:"interleaved reasoning" OR abs:"act and reason") AND abs:agent`
- Q4 `(abs:"tree search" OR abs:MCTS) AND (abs:"language model" OR abs:LLM) AND (abs:agent OR abs:planning)`
- Q5 `(abs:"environment feedback" OR abs:"execution feedback") AND (abs:LLM OR abs:"language model") ANDNOT abs:RLHF`
- Q6 `abs:"language agent" AND (abs:search OR abs:planning) AND abs:value`
- Q7 `(abs:"agentic workflow" OR abs:"agentic system" OR abs:"agentic systems" OR abs:"multi-agent") AND (abs:orchestration OR abs:orchestrator OR abs:conversation OR abs:"automated design" OR abs:generation) AND (abs:LLM OR abs:"language model")`（A3-8 增补 2026-07-16——agentic 系统设计/多 agent 编排盲区道,预期召回 ADAS/AutoGen/Magentic-One）
- Q8 `(abs:"computational graph" OR abs:"optimizable graph" OR abs:"agent graph" OR abs:"graph optimization") AND (abs:agent OR abs:LLM OR abs:"language model")`（A3-8 增补 2026-07-16——可优化图盲区道,预期召回 GPTSwarm/VideoAgent-2026）
- S1 ACL Anthology: `language agent environment feedback`；S2 OpenReview(ICLR/NeurIPS/ICML 2023–2026): `LLM agent test-time feedback`

### SF-L2 test-time agent feedback/control（IAD 族必查——UMBRELLA 坍缩风险主查道）
- Q1 `(abs:"test-time scaling" OR abs:"inference-time scaling") AND (abs:agent OR abs:agentic OR abs:workflow)`
- Q2 `abs:sampling AND abs:evaluation AND abs:feedback AND (abs:agentic OR abs:agent)`
- Q3 `(abs:"inference-time alignment" OR abs:"decoding-time alignment" OR abs:"test-time alignment")`（窗口 2023-01 起）
- Q4 `(abs:"reward-guided" OR abs:"reward guided") AND (abs:decoding OR abs:search OR abs:control OR abs:planning)`
- Q5 `(abs:"verifier-guided" OR abs:"value-guided" OR abs:"feedback-guided") AND (abs:"language model" OR abs:LLM)`
- Q6 `abs:"test-time compute" AND (abs:allocation OR abs:budget OR abs:optimal OR abs:adaptive)`
- S1 OpenReview: `agentic test-time alignment feedback`；S2 ACM DL: `inference-time control language model agent`

### SF-L3 multimodal / omni tool agents（AudioToolAgent/EChO-Agent 族必查;+cs.SD,eess.AS）
- Q1 `(abs:audio OR abs:speech OR abs:auditory) AND (abs:agent OR abs:agentic) AND (abs:tool OR abs:orchestration)`
- Q2 `(abs:omni OR abs:multimodal) AND abs:agent AND (abs:tool OR abs:expert OR abs:routing)`
- Q3 `(ti:audio OR ti:speech OR ti:voice) AND (ti:agent OR ti:copilot OR ti:assistant)`（窗口 2023-01 起）
- Q4 `(abs:"audio question answering" OR abs:"audio reasoning" OR abs:"auditory reasoning") AND (abs:tool OR abs:agent OR abs:"chain of thought")`
- Q5 `(abs:"audio-language model" OR abs:"audio language model" OR abs:"speech language model") AND (abs:"tool use" OR abs:"function call" OR abs:"tool calling")`
- Q6 `(abs:vision OR abs:video) AND abs:agent AND (abs:"training-free" OR abs:frozen) AND abs:tool`（跨模态类比道）
- Q7 `(abs:"information seeking" OR abs:"active perception" OR abs:"compositional reasoning" OR abs:"plug-and-play" OR abs:"visual chain of thought" OR abs:"visual chain-of-thought") AND (abs:tool OR abs:module OR abs:visual OR abs:multimodal) AND (abs:LLM OR abs:"language model")`（A3-8 增补 2026-07-16——信息获取/主动感知/多模态组合盲区道,预期召回 AVIS/Chameleon/Visual-Sketchpad）
- S1 IEEE Xplore(ICASSP/SLT/ASRU): `audio agent tool use LLM`；S2 OpenReview: `omni agent multimodal tool`

### SF-L4 external memory / skill acquisition（Voyager/AWM/ExpeL 族）
- Q1 `(abs:"skill library" OR abs:"skill acquisition" OR abs:"skill discovery") AND (abs:agent OR abs:LLM)`
- Q2 `(abs:"episodic memory" OR abs:"external memory" OR abs:"workflow memory") AND (abs:agent OR abs:LLM)`
- Q3 `abs:"experiential learning" AND abs:LLM AND (abs:"in-context" OR abs:"training-free" OR abs:API)`
- Q4 `(abs:"memory management" OR abs:"memory operations") AND (abs:"language model" OR abs:agent) AND (abs:"test-time" OR abs:lifelong OR abs:continual)`
- Q5 `(abs:"self-evolving" OR abs:"self-improving") AND abs:agent AND (abs:memory OR abs:skill OR abs:context)`
- Q6 `(abs:"context engineering" OR abs:"context adaptation" OR abs:"context evolution") AND (abs:agentic OR abs:agent)`
- S1 ACL Anthology: `agent memory skill library`；S2 OpenReview: `LLM agent experiential memory no training`

### SF-L5 training-free verification / control（LLM-as-Verifier/PRM 族 + 负结果道）
- Q1 `(abs:"training-free" OR abs:"tuning-free" OR abs:"without fine-tuning") AND (abs:verifier OR abs:verification OR abs:reward) AND (abs:LLM OR abs:"language model")`
- Q2 `(abs:"LLM-as-judge" OR abs:"LLM as a judge" OR abs:"LLM-as-verifier") AND (abs:agent OR abs:action OR abs:trajectory)`
- Q3 `(abs:"process reward" OR abs:"process supervision") AND (abs:"training-free" OR abs:"off-the-shelf" OR abs:frozen)`
- Q4 `(abs:"self-verification" OR abs:"self-evaluation" OR abs:"self-correction") AND (abs:limitation OR abs:fail OR abs:cannot)`（负结果/边界道）
- Q5 `abs:verifier AND (abs:"test-time" OR abs:"inference-time") AND (abs:scaling OR abs:granularity OR abs:budget)`
- Q6 `(abs:"generative verifier" OR abs:"generative reward model")`
- S1 ACL Anthology: `training-free verifier LLM judge agent`；S2 OpenReview: `process reward training-free verification`

### SF-L6 black-box / API-only 优化（GEPA/OPRO/DSPy 族 + 接口可得性道）
- Q1 `(abs:"black-box" OR abs:blackbox) AND (abs:"language model" OR abs:LLM) AND (abs:optimization OR abs:adaptation OR abs:agent)`
- Q2 `(abs:"API-only" OR abs:"closed-source" OR abs:"API access") AND (abs:adaptation OR abs:optimization OR abs:alignment)`
- Q3 `(abs:"gradient-free" OR abs:"derivative-free" OR abs:"zeroth-order") AND (abs:"language model" OR abs:LLM) ANDNOT abs:"soft prompt"`
- Q4 `(abs:"prompt optimization" OR abs:"prompt evolution" OR abs:"instruction optimization") AND (abs:"black-box" OR abs:LLM)`
- Q5 `(abs:"compound AI" OR abs:"compound system" OR abs:"LM program" OR abs:"language model program") AND abs:optimization`
- Q6 `(abs:logit OR abs:logprob OR abs:"log-probability") AND abs:access AND abs:"language model"`（接口可得性——JitRL 类「方法最近、接口不合」边界道）
- S1 OpenReview: `black-box LLM optimization API-only`；S2 ACM DL: `compound AI system optimization`

### SF-L7 reward hacking / verifier gaming / loop over-optimization（Goodhart 族;Q3 窗口 2020-01 起）
- Q1 `(abs:"reward hacking" OR abs:"reward gaming" OR abs:"specification gaming") AND (abs:LLM OR abs:"language model" OR abs:"test-time" OR abs:inference)`
- Q2 `(abs:"reward overoptimization" OR abs:"over-optimization" OR abs:overoptimization) AND (abs:reward OR abs:verifier)`
- Q3 `abs:Goodhart`（窗口 2020-01 起,每页 50）
- Q4 `(abs:"verifier gaming" OR abs:"judge hacking" OR abs:"evaluation gaming" OR abs:"benchmark gaming")`
- Q5 `(abs:"best-of-n" OR abs:"best-of-N") AND (abs:KL OR abs:overoptimization OR abs:distribution)`
- Q6 `(abs:"stopping rule" OR abs:abstention OR abs:"early stopping") AND (abs:"test-time" OR abs:inference) AND (abs:reward OR abs:verifier OR abs:confidence)`
- S1 OpenReview: `reward hacking inference time best-of-n`；S2 ACL Anthology: `verifier gaming overoptimization`

### SF-L8 等预算 agent 评测 / trajectory credit（Kapoor/tau-bench 族）
- Q1 `(abs:"agent evaluation" OR abs:"agent benchmark") AND (abs:cost OR abs:budget OR abs:compute OR abs:efficiency)`
- Q2 `(abs:"matched compute" OR abs:"compute-matched" OR abs:"budget-matched" OR abs:"cost-controlled" OR abs:"equal compute")`
- Q3 `abs:"credit assignment" AND (abs:trajectory OR abs:agent) AND (abs:LLM OR abs:"language model")`
- Q4 `abs:Pareto AND abs:agent AND (abs:cost OR abs:accuracy)`
- Q5 `abs:"test-time compute" AND (abs:"scaling law" OR abs:predict OR abs:"when to")`
- Q6 `(abs:overthinking OR abs:"give up" OR abs:"premature termination") AND (abs:agent OR abs:"long-horizon")`
- S1 OpenReview: `agent evaluation cost budget pareto`；S2 ACM DL: `LLM agent cost-controlled evaluation`

**计数（A3-8 后现行口径）**：8 lanes × 6 + 3 条增补（SF-L1-Q7/Q8、SF-L3-Q7）= **51 条
预注册查询**（历史口径「48」见 amendment-3 A3-8,「64」见 amendment-2;16 条副源路线已退役）。
预算/调用量等资源轴不是查询过滤器,是抽取轴（§7,重校准 §2.1 口径）。**增补查询的敏感性审计
留痕**：离线纸面审计（Opus 独立,零联网）结论与逐篇召回表随 amendment-3 批次归档于
Decision-Log 续59;审计明确 ToT/Socratic-Models 不为其加查询（种子+引文图兜底）。

### SF-L9 foundational lineage（基础谱系道——amendment-1 新增,v3 外审 4.5;不受 2022 窗限）

- **种子** = manifest 增量批次1 的 4 条经典（metareasoning / POMDP / options / UCT,DOI 题录）;
- **方法** = 自经典种子 backward/forward chaining（SS/OpenAlex 发现层,承重回正式版）,沿链补
  value of information / anytime computation / algorithm selection / active perception 代表作;
- **目标** = 建立 RL/search/planning/metareasoning 概念分类与本研究对象的谱系定位——**「RL」
  命名保留与否的裁决依据**（RL 控制合同命名纪律引用处）;
- **统计隔离**：本道产出**不计入** 2022–2026 近期 novelty 池,单独报告;
- **停止规则**：连续**两轮** chaining 零新增概念祖先即停（与主道饱和判据对齐——内审 MINOR-8
  更正）,单独留痕;
- 无预注册 Boolean 查询（经典文献 arXiv 覆盖不全,以 chaining + DOI 锚为主;Google Scholar
  仅 DISCOVERY_ONLY）。

## §4bis 执行策略：广度优先 → 触发式深度遍历（A2-5,owner 裁决④）

- **BFS pass**：51 条查询的全部命中先做题录/摘要级编码（DISCOVERED / ABSTRACT_VERIFIED,
  含 §6 矩阵可从摘要判定的轴 + venue_tier + topic_relevance）——不做全文、不做 chaining。
- **DFS 触发四判据**（满足任一即入队,`dfs_trigger` 多值登记理由;A2-10）：**T-a 对象重合**
  （omni agentic system/多模态知识系统/语音本体）**T-b 问题重合**（回答我们任一 RQ,即使对象
  不同）**T-c 要素重合**（方法/组件可迁移进控制平面）**T-d 结论冲突**（结论若真会削弱我们的
  假设——负结果/评测批判/方法论攻击,锚 = most_threatened_rq ≠ none;防「相似性判据漏掉
  不相似但致命的工作」）。
- **队列排序键（确定性字典序,不随机游走）**：`(威胁度↓, core>element, 时新性↓, 梯队↑)`——
  威胁最优先（占据核查是第一使命）;新先于旧（创新空间是时间递减资源）;梯队只作平局裁决。
- **DFS**：全文抽取（FULLTEXT_OPENED 及以上,§6/§7 全字段含方法占据四问）+ §5 引文图遍历。
- **预判定 DFS 集**：74 列名种子（选入即因相邻性,天然满足触发判据——外审 P0-LIT-3-③ 的
  种子 chaining 要求由此满足）+ threat 首轮 15 篇（双人独立全文抽取,§8）。

## §5 引文图遍历与半径控制（owner 裁决⑤重写——深度遍历 = 引文图结构分析,五层防爆栈）

**遍历对象**：DFS 节点的**双向引文图**——backward（它引用的,全文抽取时天然获得引用上下文）
+ forward（引用它的,经 SS/OpenAlex 发现层取元数据）,综合分析。

**五层防爆（半径不爆炸的结构保证）**：
1. **只从 DFS 节点扩展**：BFS 级节点登记不扩展;扩展资格 = 该节点自身触发 §4bis 四判据之一。
2. **边过滤（核心防爆条款,owner 裁决）**：只沿两类边扩展——**方法谱系边**（方法论同族:
   继承/改进/变体,来源=目标论文 method/related-work 的方法来源引用）与**对比引用边**
   （作为 baseline/对比方法被引,来源=实验表格与对比段）;背景/概念/数据集/通用工具引用边
   **不扩展**（登记不遍历）。边功能判定:backward 方向在全文抽取时顺带完成;forward 方向先对
   引用者做 BFS 编码,其触发 DFS 后打开全文时回判。
3. **公共节点剪枝（owner:「公共的论文部分就不纠结」）**：在 ≥3 个 DFS 节点的引文图中共现、
   且自身不触发四判据的高频文献标 `COMMON_NODE`——登记共现计数,不扩展;若其自身触发判据,
   全局只裁决与扩展**一次**（visited-set）,绝不逐图重复分析。
4. **visited-set 全局去重**：任何节点整个 survey 至多被扩展一次（图遍历标准语义,防环防重复）。
5. **饱和停止**：连续两轮扩展零新增触发节点即停;新簇出现重启该簇计数。

**边价值不对称（协调者补充,占据核查用）**：**forward-对比边最优先**——「引用目标论文作
baseline 并声称超越它」的新工作,是占据格局变动的最强信号（它们标出了邻居已被谁超越、
改进空间被谁吃掉）;backward-对比边（目标打败过谁）价值次之。遍历队列内 forward-对比 >
forward-方法谱系 > backward-方法谱系 > backward-对比。

- **任何 NO_DIRECT_MATCH 类结论**须满足预注册饱和：连续两轮遍历零新增触发节点 +
  **双评审独立同意**;伴随 token 制度沿用（按身份索引,禁全局 token）。

## §5bis 时新性增量扫描（修正案 B——Omni-Decision 已证明此非形式主义）

① 首次执行时检索至执行当日;② synthesis 冻结前做「首执行日 → 冻结日」增量扫描;③ Stage-1A
跨长时段则维护**带日期的增量批次**（seed manifest 追加行,永不改旧行）;④ 新文献按同一 schema
编码,不静默改写旧判决（判决修订走 §10 版本化）。

## §6 纳排矩阵（十轴,P0-LIT-3-④）

每条 INCLUDED 记录编码：`core_access(weights/logits/hidden-state/attention/API-text/
API-multimodal——A3-5 扩枚举) | parameter_update(none/prompt/
adapter/full) | external_state_update(none/memory/skill/tree) | reward_type(gold/verifier/
self/env/none) | policy_update(none/nonparametric/trained) | modality_path(text/audio-native/
audio-tool/vision/omni) | tool_use(none/fixed/routed/learned) | budget_horizon(单步/固定K/
多轮/任意) | task(域) | trained_comparator(Y/N)`。EXCLUDED 必须记排除理由（§9 日志字段）。

**TF-Strict 审计子字段（标题驱动漂移防护,v2 评审风险二;A3-5 扩展）**：`base_model_updated(Y/N) |
external_component_trained(Y/N,对象) | component_pretrained(Y/N,哪些组件系既有预训练参数) |
method_specific_parameter_training(Y/N,是否为本任务/系统新训参数) |
test_time_parameter_update(Y/N) | nonparametric_persistence(within_item/across_items/none) |
ground_truth_used(无/预先/开发集/测试时) |
learned_object(token-prior/value-fn/verifier/prompt/memory/skill/tool/code/workflow/graph/
index/exemplar/none/other〔登记后使用〕) | learning_time(test 前/test 中) |
test_time_readonly(Y/N)`——「冻结核心 ≠ TF-Strict」（Training-Free GRPO / IRO / VeGAS 类
必经此审计）;扩展四字段防「冻结通用工具」与「为本任务新训组件」混为一类,扩枚举防
UCT/AFlow/ADAS/GPTSwarm/Voyager/ConMem 类更新对象无处登记致 scope_pending 不可裁决。

**梯队与策略字段（A2-2/A2-4/A2-5;A3-2 修订）**：`venue_tier(T1/T2/T3——默认先验非终裁,
T3 按相关性/质量裁决,EXCLUDED 记理由) |
topic_relevance(core=语音/omni agentic 本体, element=技术要素参考) | dfs_trigger(T-a对象重合/T-b问题重合/
T-c要素重合/T-d结论冲突, 多值;空=仅 BFS——四值与 §4bis/A2-10/REC-2 模板/README 一致)`。

**A3-5 新增字段组（schema 正典 = REC-2 空白模板,字段语义见该件补注）**：
`source_axes`（信息来源六类 / answer_bearing_external_info / gold_path_audit /
activation_attribution〔readout/new_info/mixed/not_claimed〕）| `omni_axes` 五轴
（core_model_modal_capability / observation_seen_by_core / tool_input_output_modalities /
action_modality / multimodal_causal_grounding_evidence——modality_path 降为粗标签,承重判断
以五轴为准）| `rl_identity` 九字段（state_definition/action_definition/feedback_definition/
transition_or_controller/policy_representation/cross_step_update_object/credit_assignment/
stopping_rule/authors_call_it_rl——SF-L9 谱系裁决「RL/planning/search/bandit/metareasoning」
的记录基础）|
`evidence_axes`（verification_depth / publication_status / study_quality / quality_override）。

**范围多轴（修正案 F——不用单一 DIRECT/OUT 压平）**：`system_level_proximity |
component_level_proximity | modality_proximity | tf_strict_compliance | black_box_compliance |
reward_control_proximity | persistence_state_proximity | evidence_grade` 各轴独立编码
（如 walking-through-uncertainty：组件直接、系统不直接）。

**RQ 威胁标注（v3 外审 P0-C 末项;amendment-1 A1-9 补录）**：每条 INCLUDED 记录另标
`most_threatened_rq`（多值;枚举 = RQ-SYS/RQ-CTRL/RQ-OMNI/RQ-SAFE/RQ-MEASURE/none,问题树
定义见 v3 提案 §3）——该工作**最可能推翻或占据**的研究问题;标 none 须附一句理由。§11 的
coverage/kill matrix v3 按本字段逐 RQ 聚合。

## §7 抽取字段与证据分级

开放字段（Checkpoint B 全采,允许新增列并版本化）：`core access / modality path / external
components / feedback type / what changes at test time / persistence scope / compute scaling /
claimed mechanism / strongest result / failure mode / reusable implementation`。
**方法占据四问（A2-6,DFS 强制——owner:聚焦方法是否被占用而非名词）**：`method_gist(方法是
什么) / method_limitations(局限在哪) / improvement_space(改进空间——三小问齐备才有效:①哪条
轴〔精度/鲁棒/成本/模态覆盖/理论保证〕②为何现有方法到不了〔结构障碍还是没人做〕③到了对
哪个 RQ/任务阈值有实质影响) / borrowable(可借鉴什么)`。占据结论禁止只写 occupied——必须跟
改进空间与其价值评估;kill/pivot 重述:**名词被占 ≠ kill,方法被占且无有价值改进空间才触发
pivot**。资源六轴
`{model calls, tool calls, tokens, latency/cost, horizon, stopping}` 作为文献抽取轴观察
收益饱和/退化。承重 delta 须 version pin + section/page/table/equation locator + 必要长度
span（P0-LIT-3-⑥）;L3 即读即登记（census/ledger schema）。

## §8 Threat papers 双人独立全文抽取（P0-LIT-3-⑧;amendment-1 重排,v3 外审 4.6）

**首轮队列 15 篇（可增长,非硬上限——「15」是首轮工作队列而非封顶）**：
**Omni-Decision 2607.11433（最高优先）** / IAD 2504.01931 / AudioToolAgent 2510.02995 /
EChO-Agent 2606.15141 / Agent-Omni 2511.02834 / Audio-Mind 2605.28480 / JitRL 2601.18510 /
training-free-grpo 2510.08191 / LATS 2310.04406 / Voyager 2305.16291 / Kapoor 2407.01502 /
Speech-Copilot 2407.09886 / inference-time-reward-hacking 2506.19248 /
**Affordance-Agent-Harness 2605.00663（晋升）** / **FineVerify 2606.00660（晋升）**。
**待判定入池**：OmniAgent 2606.19341 / CMA-Harness 2607.08497 / UCT-ToolCreator 2602.01983 /
ConMem 2606.08702;**次优先**：Argos 2512.03438。每次增删记录发现路线与理由——**不得只把
支持己方的文献提升优先级**。两名独立抽取者（不同 agent 会话,互不见对方产出）
按 §6/§7 编码,冲突由协调者亲验裁决并留痕。**选文过程留痕（修正案 E）**：候选池**完整登记
清单**、两名评审各自的排序与理由、分歧与最终合并规则全部归档——选文环节零无记录筛选。

## §9 日志与可回放（P0-LIT-3-⑦;round-1 宇宙缺失的构造性防复发）

**每页一行**（A1-4 分页语义,消除 cap 歧义）：`{query_id, engine, query_ref(=queries.jsonl
行 record_sha256), page_start, max_results, totalResults, sortBy, sortOrder, timestamp,
raw_response_ref 或可重建结果 ID 清单, response_sha256, n_hits_page, included[],
excluded[{id, reason}], failed_request(如有)}`——totalResults 每页复记留痕;存
`wiki/survey/replay/SF-SURVEY-2026/`。原始响应能存则存,不能存
（接口条款）则记录可重建 ID 集。快照/哈希按哈希正典（git blob）。

## §10 Taxonomy 版本化修订

五合同 = PROVISIONAL_STAGE1A_TAXONOMY：survey 证据要求修改分类时,走**版本化增补**
（amendment 文件 + 修订理由 + 生效日期）,禁静默改写;新类别按收词纪律先登记后使用。

## §11 停止规则与产出

- 查询停止 = 全部 51 条编译查询执行完毕（含分页抓全,总数口径非每 lane;历史口径 48 见
  A3-8）+ T1 题录道 50 route 扫描完毕（可执行数以 routes manifest 状态列机器计数为准）
  + 引文图遍历达饱和（§5）;整体停止不设时间 cap,以覆盖判据（§1）与饱和为准。
- 产出：coverage/kill matrix v3 + SOTA cards v3 + 更新的 census/ledger + **3–5 个
  system-level candidate problems**（Checkpoint D;候选池含重校准 §4 六类;**每个候选附
  「改进空间 + 为什么值得占」两栏**——A2-6 渐进式研究观的输出落点）——供 Stage-1C owner
  双证据选题;不做 intersection-novelty 论证（Checkpoint C）。

## §12 签署流与签署区

1. 本协议过内审环 → owner 过目 → 送 reviewer **search-design 签署**;
2. 执行前置三条件 = §12.1 的 reviewer 签署 + owner 批准 + P0-R8 状态门复跑（缺一不可,
   frontmatter first_query_gate）;
3. 执行期间任何查询/种子/判据变更走 §10 版本化增补并即时可见于 replay 目录;
4. survey 完成 → 综合 → 届时才谈 Stage-1A close（与 1B 放行分立两签）。

**签署包清单（v2 外审 §6.2 六件套;A3 后组成映射）**：① 本协议 + amendments 1–3
（amendment-3 独立件 `2026-07-16-sf-protocol-amendment-3.md`）;② seed manifest
（`2026-07-15-sf-seed-manifest.jsonl` 74 条 + 伴随报告）;③ 数据源与检索字符串（本协议
§2/§4 + T1 routes manifest `2026-07-16-sf-t1-proceedings-routes.md`）;
④ 纳排/抽取 schema（本协议 §6/§7）;⑤ 空白记录模板（`2026-07-15-sf-blank-templates.md`
REC-1..REC-7,A3-4——原 T1–T6 编号废止）;⑥ 本签署区。各件以提交后 (commit, path, blob)
三元组互引,签署对象 = 六件整包。

**签署区（三方分立,任一空缺不得执行首条查询）：**

```text
[ ] reviewer search-design 签署：signature ______________  date ______  签署 commit ______
    （签署语义 = 检索设计合格可执行;不构成对研究方案科学成立或 novelty 的背书）
[ ] owner 执行批准：signature ______________  date ______
[ ] P0-R8 状态门复跑：exit code ____  运行工件路径 ______________  执行人 ______
queries_executed_at_signoff: 0（attestation——签署时刻查询执行数必须为零）
```
