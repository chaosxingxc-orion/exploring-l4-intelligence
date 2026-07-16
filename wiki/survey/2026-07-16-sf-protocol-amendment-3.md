# 检索协议 amendment-3（v3 收官就绪度评审 G1–G6 整改 + owner 2026-07-16 四裁决——签署前设计修订,零查询状态下并入）

（性质：变更记录,独立日期件——**自本件起恢复「一修正案一独立日期件」落盘纪律**;amendment-2
在 `2026-07-15-sf-protocol-amendment-1.md` 文件内追加的历史位置按 append-only 不迁移,由
bundle correction #3 一并钉定。协议本体 supersede-in-place 已同步,旧字节在 git 历史。触发 =
`wiki/2026-07-15-system-first-research-proposal-v3-stage1a-closeout-readiness-review.md`
（Gate S1 = WITHHOLD SIGNATURE — TARGETED MAJOR REVISION）+ owner 2026-07-16 四裁决
（Decision-Log 续59）。**attestation：本批并入时联网检索查询执行数 = 0。**）

| # | 变更 | 取代 | 依据 |
|---|---|---|---|
| A3-1 | **来源政策：arXiv-primary + 免费官方源救援 + 付费计数废弃**。检索引擎维持 arXiv API 唯一（预注册查询全部经 arXiv）;发现层（T1 题录道/引文图/种子解析）命中的直接相关工作若无 arXiv 版：**免费官方开放获取源**（ACL Anthology/NeurIPS proceedings/PMLR/OpenReview/CVF/ISCA Archive 等）以 venue-native ID/DOI + 本地备份 + sha256 纳入承重（A2-3 备份规则的扩展);**付费且无任何免费版本 → `REMOVED_PAYWALLED_UNOBTAINABLE`**——记录退出语料、不承重（owner:「付费就废弃这条记录,因为我们获取不到原文」——与全文强制 A2-9 同构）,但**移除事件+ID+题名+venue+计数入 flow report,凡占据类/NO_DIRECT_MATCH 结论必须伴随移除计数披露**（外审「不从存在性记录中消失」由计数记账满足）。最终产出命名 = 「arXiv-primary systematic mapping（免费开放获取救援+显式移除记账）」,不自称 comprehensive universe | A2-1 的「非 arXiv 可得的信息源不参考」条 | 评审 G1（来源限制与结论强度须匹配,方案 A）+ owner 裁决①（07-16）。成本事实核查：T1 十会 8/10 免费官方开放获取,真付费仅 ICASSP（IEEE）与 ACM MM——方案 A 实际零成本 |
| A3-2 | **梯队权重降为默认先验 + 研究质量三轴分立**。`venue_tier` 保留为**默认先验权重**,非终裁;逐篇新增 `verification_depth`（五级标尺,与 evidence_grade 同标尺）/ `publication_status`（preprint/peer-reviewed/withdrawn/retracted）/ `study_quality`（HIGH/MEDIUM/LOW + 一句理由:数据边界/对照公平/统计不确定性/消融/复现性/代码可得/claim-evidence match）三轴;**study_quality 可双向覆盖先验**——T1 低质降权（`T1_DEMOTED:<理由>`）,T2 高质（代码+复现+充分消融）经协调者裁决登记后可承重（`T2_PROMOTED:<理由>`,`T2_UNREVIEWED` 限定语保留并加注 override）;**T3 从「默认不参考」改为按相关性/质量裁决**——venue 不再自动排除任何论文,EXCLUDED 必须给相关性/质量理由;**novelty/priority 威胁判定与实验可信度分离**——未发表工作同样可摧毁首创宣称,threat 判定不看梯队 | A2-2/A2-8 的「T1 实验结论可直接承重」「T3 默认不参考」终裁语义（梯队框架保留） | 评审 G2 + owner 裁决②（07-16「按你的逻辑走」= 先验+覆盖折中,拒绝把 tier 全降元数据的矫枉过正） |
| A3-3 | **T1 proceedings 发现道实例化**：50 条 route ID 冻结于 `2026-07-16-sf-t1-proceedings-routes.md`（入口/track 界定/词表 v1〔A∨(B∧C) 规则,显式枚举零通配符〕/归一化与模糊匹配规则/raw 题录哈希/解析流程/五计数字段）+ 执行日志模板 REC-7;venue-year 不举办（ICCV 偶数年 3 条）标 NOT_HELD,未出版标 NOT_YET_PUBLISHED 由 §5bis 承接;付费会场题录扫描免费可行,全文按 A3-1 分流 | A2-7 的散文承诺（「每会每年一 route ID」无实例化） | 评审 G3（「A2-7 仍是 prose promise,无法执行或重放」） |
| A3-4 | **同名异构消除**：空白模板编号 `T1–T6` → `REC-1..REC-6`(+新增 REC-7);`T` 前缀自此为 venue 梯队独占;历史文件不改写,读旧件按「模板语境 T{n}=REC-{n}」映射 | 模板旧编号 | 评审 G3 末段 + 本项目收词纪律（同名绝不承载两个定义） |
| A3-5 | **schema 传播（五份合同 → 数据结构）**：REC-2 增设 `source_axes`（信息来源六类/answer_bearing_external_info/gold_path_audit/activation_attribution〔readout/new_info/mixed/not_claimed〕）、`omni_axes` 五轴（core_model_modal_capability/observation_seen_by_core/tool_input_output_modalities/action_modality/multimodal_causal_grounding_evidence——modality_path 降为粗标签）、`rl_identity` 九字段（state_definition/action_definition/feedback_definition/transition_or_controller/policy_representation/cross_step_update_object/credit_assignment/stopping_rule/authors_call_it_rl）、`tf_audit` 扩展四字段（component_pretrained/method_specific_parameter_training/test_time_parameter_update/nonparametric_persistence）、`learned_object` 扩枚举（+memory/skill/tool/code/workflow/graph/index/exemplar/other〔登记后使用〕）、`core_access` 扩枚举（+hidden-state/attention/API-multimodal）、`evidence_axes`（A3-2 三轴+quality_override） | REC-2（原 T2）旧骨架 | 评审 G4/P0-4（「prose 已修、schema 未传播」——2.2-A/B/C/D 四项全闭合） |
| A3-6 | **分页递归 fallback**：totalResults>2000 的确定性拆分补递归规则——**年 → 月 → 日**逐级细分至每片 ≤2000;派生查询 `query_id = <父ID>-W<窗口序号>`,REC-1 行内记 `parent_query_sha256`;拆分事件全留痕 | A1-4 的「按年度子窗拆分」(单年>2000 时规则不可终止) | 评审 G6 |
| A3-7 | **种子批次2（+14 = 74）**：v3 收官就绪度评审 §4 delta scan 14 条入 manifest（AFlow/ADAS/GPTSwarm/RAP/ToT/PromptAgent/Magentic-One/Agent-S/AutoGen/Chameleon/Socratic-Models/AVIS/Visual-Sketchpad/VideoAgent-2026,source=评审delta-scan）;新字段 `initial_tag[]`（多值枚举 DIRECT_THREAT/TRAINED_COMPARATOR/METHOD_LINEAGE/COMPONENT_ANALOGY——仅管阅读优先级,不预判纳排结论,批次2 起用旧行不补）;VideoAgent-2026 存在性执行首步核验（不可解析标 UNRESOLVED）;Socratic-Models 窗外靠列名进入 | 计数 60（历史口径保留作 lineage） | 评审 §4/P0-5;§5bis 增量批次机制第二次使用 |
| A3-8 | **查询敏感性审计 + 3 条增补查询（append-only）**：离线纸面审计（Opus 独立,零联网）结论——48 条可稳召回 AFlow/RAP/PromptAgent,评审点名 7 短语全为真盲区;增补 **SF-L1-Q7**（agentic system 设计/多 agent 编排道）、**SF-L1-Q8**（可优化图道）、**SF-L3-Q7**（信息获取/多模态组合道）,均默认窗口、沿用所挂 lane 类目集,查询串见协议 §4 增补节;**48 条原批逐字节不变,新批追加于 jsonl 末尾**;compiler 升版重编译+静态验证复跑（`docs/checks/2026-07-16-sf-queries-static-validation-rerun.md`);现行查询计数 = **51**（历史口径 48 保留作 lineage）;ToT/Socratic-Models 不为其加查询（种子+引文图兜底,审计 §3 留痕） | 「48 条」现行计数 | 评审 §4 末段（query vocabulary 盲区)+P0-5;敏感性审计报告随批归档 |
| A3-9 | **v3 proposal errata 第二批登记（协议侧指针）**：Snell=TRAINED/GRAY-BOX MECHANISM ANALOGY;HedgeTune=输出级过优化控制类比非已验证 agent 停止规则;「存在大幅头空」→条件化「可出现」;RQ-SYS ceiling 条件化（相同初始信息+显式 decision rights,两侧 headroom 分别报告）;摸高/matched-control/成本效率三拆名（ceiling-seeking resource posture / causal matched-control entitlement / cost-efficiency comparison——matched control 不推迟,否则 RQ-CTRL 不可证伪）;候选问题卡效用归因四行分立+单反例可杀性要求。全文见 v3 修订记录 errata-2 节 | —（proposal 侧变更,此处登记） | 评审 P0-6 + §6.1–6.4 |
| A3-10 | **「CONVERGED」使用纪律**：凡 convergence 声明必须带对象与锚（`TEXT_CONSISTENCY_CONVERGED@blob`、`QUERY_STATIC_VALIDATION_PASS@blob` 等）;裸 `CONVERGED` 停用;内部一致性收敛 ≠ 检索无偏 ≠ 引用正确 ≠ schema 充分 ≠ 外部签署 | 既往裸 CONVERGED 用法（历史件不改写） | 评审 §8.2 |
| A3-11 | **阶段称谓重校准**：现状 = **Stage-1A 收官准备末段（survey-ready / closeout-preparation gate）**——问题框架接近稳定,外部证据工作（检索/全文抽取/引文链/饱和/候选问题）尚未开始;「Stage-1A 收尾/尾声」表述废止;真正的 Stage-1A close 从可回放 survey 完成、3–5 候选问题形成起算 | 热层「Stage-1A 收尾」 | 评审 §1 + owner 裁决③（07-16 GO） |
| A3-12 | **hostile 迟归档定名**：既有迟归档敌意环记录统一标 `LATE_RECONSTRUCTED_REVIEW_SUMMARY`（问题/修复复盘可用,不等同原始 replay、不独立证明当时全过程） | 「迟归档=完整归档」的模糊语义 | 评审 §8.2 |

**S1-E 验收影响**：E2（queries.jsonl）→ 51 条口径+复跑报告;E4 → A3-1 语义再修;E6（bundle）→
correction #3 待本批提交后钉定;其余 E 项不变。**签署包组成不变（六件套）**,routes manifest
归入件③（数据源与检索字符串）、本件归入件①（协议+amendments）。

**再申请动作**：本批全部落盘+敌意环收敛+correction #3 钉定后,重新申请 Gate S1 search-design
**窄幅复核**（评审自定:只查 G1–G6 闭合与 bundle 一致性,不再开 proposal 轮次）。
