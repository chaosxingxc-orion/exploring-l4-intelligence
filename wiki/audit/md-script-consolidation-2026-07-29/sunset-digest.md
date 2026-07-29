# MD 与脚本整编战役 sunset digest（2026-07-29）

Authority：owner 2026-07-29「应删尽删」＋三级处置规则（无关直接移除/弱关系摘要后归档/只留
强关系），spec = `docs/superpowers/specs/2026-07-29-md-script-consolidation.md`。逐件恢复命令
见同目录 `sunset-ledger.jsonl`（每行 `git show <last_commit>:<path>`）。

## Wave A（umbrella 非门禁绑定件，189 件 / 5.51 MB）

**链 1 · system-first-stage1b（31 件）**：Stage-1B systematic mapping 执行链（题录筛查、bounded
sampling 合同、batch closeout）。终局：226 篇 registry + 320-work 校准并集，冻结为 v5 release
`38fb943`；结论由 current 层 `stage1b-transition-reference-appendix.md` 与 mapping-release 表
完整承接。教训：过程叙事与冻结结论分层，前者可清。

**链 2 · stage1b-refinement（10 件）**：全文二次处理（451 篇抢救、67 篇人工确认）。终局：
复现锚点=0（无一篇同时满足 KEEP_CORE+本地任务匹配+可运行仓库）；分析快照在数据盘
`survey-fulltext-secondary-analysis/2026-07-22-v4/`。

**链 3 · stage1b-capability-delta（11 件）**：07-23 能力向增量（14 篇）。承重遗产：「知识/技能
=内容资产、记忆=持久化机制」——此结论直接流入五维划分。状态停 RELEASE_CANDIDATE 未签，被
07-26 五维 replan 取代。

**链 4 · stage1b-targeted-anchor-scan（5 件）**：定向锚点扫描（26 篇全文）。终局：282/306/320
三层计数可辨；registry shard `stage1b-targeted-anchor-scan-2026-07-24-papers.jsonl` 保留在盘。

**链 5 · stage1a working-brief（1 件）**：研究对象定义「冻结黑盒 omni 外的 external
reward-guided control plane」已被 Research-Objective 逐字承接并升级 API-only；round-16 晋升
从未达成。签署链在 `wiki/audit/system-first-stage1a/`（不动）。

**链 6 · stage1c-v2 + agentic-calibration-r1（21 件）**：stage1c-v2 时代残件与双隔离 coder
（gpt-5.6-sol/terra，N=56）编码一致性战役。终局：FAIL——13 条论文级 critical path 只过 5，
object_match_key 共同键=0；已入 Research-Objective legacy 段（R1 agreement FAIL、R2R1
RETIRED_WITHOUT_DISTRIBUTION_OR_INDEPENDENT_ACCEPTANCE）。

**链 7 · fixtures-c4a/c4b（41 件）**：校验 fixture，唯一消费者 `sf_record_validator_test.py`
已于 0276848 退役，零引用孤儿。

**链 8 · papers/agent-level-tfrl（31 件）**：agent-level TFRL 论文冲刺全目录。击杀史：07-02
三轴敌意评审（qstar_product 重言式 / purpose VoI≈0 / 跨会话基准不可建）→ POMDP 重构塌缩为
单模型诚实论文 → 四轮零重大发现收敛。**承重遗产（本役唯一必须记住的数字组）**：冻结
Qwen3-Omni-30B（llama.cpp GGUF）真 best-of-N：oracle-WER headroom **+0.042 [0.029,0.056]
@N=8**（N=4 起显著），而可部署 label-free MBR **在每个 N 都不显著**——realized-vs-headroom
缺口正是 R6/R8 的攻击对象；冻结编码器探针 content≈1.0 / speaker≈chance / emotion NULL；
reward-spread 透镜 `gain=β·KL ≤ spread²/8β` 两条 sorry-free Lean 引理。原始数据在 W1
`_repro/asr_bon_llamacpp_snr5.json`（保留）。

**链 9 · docs/checks 7 件**：内审环/press 反馈/查询静态校验叙事/v42 conformance/provisional
复现序列。机读正典（`2026-07-15-sf-queries.jsonl`）仍在门禁校验；v42 报告自陈不得引用。

**链 10 · docs/integrity 5 件**：C1/C4 普查 DRAFT 与 discrepancy register。承重教训已上收：
负结果只存会话日志=UNRECORDED（进 AI-Collaboration 记录规约）；v4.2 三处不一致判为发布快照
协调失败非造假。

**链 11 · docs/superpowers 6 件**：已实施完毕的 Stage-1A/1B 整编计划与设计（07-19/20 五件）+
07-22 过渡计划。保留：07-26 replan（d0-d6/T1-T3 唯一 provenance）、07-27 consolidation、
07-28/29 两 spec。相应的 Task8/9 契约测试（ManifestRefreshPlanContractTests）同批退役。

**链 12 · 散件**：step2a/3a 机读 json（叙事版在 wiki/archive/）、v4-v6 评审轮访问日志（v7 现行
保留）、registry 两个中间批次视图（现行合并视图 `stage1b-bounded-exhaustive-2026-07-22.json`
保留）、`proofs/tfrl/OptSpace-notes.md`（绑已废 B8 轴；Lean 模块本体与审计角色保留）。

**Wave A 反向保留裁定**：`portfolio-synthesis-and-stage2a-package.md`（虽零引用，但为
Research-Objective §Stage-2A 的原文来源）；`docs/superpowers/plans/2026-07-26-stage1c-portfolio-replan.md`
（d0-d6 证据链唯一 provenance）；W1 `_repro/LOCKED_HOLDOUT/`（append-only 诚信事故取证现场，
删=毁证）。

## Wave D（umbrella 脚本，17 件删除 + 143 件上一役欠账回填）

脚本普查终判（普查面 293 件：umbrella 61 / W1 129 / W2+W3 4 / W4 99）：MUST_GATE 49、
MUST_INFRA 75、MUST_PYTEST 22、NOT_MUST 141。本波删 umbrella NOT_MUST 17 件（Stage-1B
closeout 工具组、双语言孪生 .ps1、红测试三件、已合并的 fetch-candidate-* 两件、一次性
lockfile/verify/probe/mlflow 包装）；另 12 件 gitignored `.tmp_*` 游离脚本物理删除（未入库
无台账代价）。**保留两件普查建议删除的**：`test_sf_archive_candidates.py`（活门禁 cmd 7 的
oracle，17/25 红因 fixture 未跟进 strict-JSON 硬化——待修不删，删=让门禁成员裸奔）、
`scripts/lean_axiom_gate.sh`（Lean 审计线在 Research-Objective 与各 R proposal 仍活跃，删=
公理足迹失去机器校验；接线或退役待 owner 一句话）。

**143 件回填**：07-28 清理波无台账退役的脚本（survey 135 / checks 5 / data 2 / 根 1）以
`reason_class=SUNSET_TOOLING_BACKFILL` 补入本台账，blob 全量核验可达；恢复父分别为
48f495b(97)/3d4381f(27)/ed9c7f5(16)/2346cd8(3)。上一役"暗资产不可控"主扣分项就此闭合。

**scripts/tools/ 裁定落地说明**：owner 要求的常驻日用工具目录以"缺了才建"为准——fetch/
登记四件套（sf_fulltext_fetch / sf_official_metadata_fetch / sf_fulltext_ledger_status(已删,
被状态查询需求淘汰) / sf_atom_provenance_fetch(已删,被取代)）中活跃两件留在 scripts/survey/
（在 code_graph 保护内，迁出反而降保护面）；被删发现道工具需要时按台账恢复到 scripts/tools/。

## Wave B（legacy 冷层收官，84 件删除 + 10 件反向保留）

manifest legacy_cold_paths 94 件中 84 件删除：AUDIT_LEGACY 冷链（gate-s1 v4-v9 响应与
corrections、protocol amendment 1/3-8、census/claim-ledger 报告、v3/v9/v10 提案、博士评审、
法证、s0 签署、denoise 提案、replay 事务等——判决已由 wiki/audit 各 campaign INDEX 与
Decision-Log 承接，协议正典 07-28 wave-E 已 historicize）+ REGISTRY_LEGACY 冻结中间表
（stage1 L1-L4/X1-X3、speech2vec、embedder 矩阵、coverage/kill/neighbor/sota v2、opening-tables
v1-v4、claim-evidence v4/v5、bibliography-v1、taxonomy-v5/coding-v6 json、identity-contracts、
W4 系列参考文档、提案模板——被 Stage-1B v5 release 38fb943、current 层与 coreview 模板 v2
取代）。其中 26 件为已注册审计工件，走 registry sunset 数组（blob=注册 pin 逐件核对，
incident_log 已追加）；58 件未注册走本台账。**反向保留 10 件**：
`wiki/2026-07-18-inherited-prior-exposure-union.md`（owner 07-18 裁决②正典载体，held-out
设计强制约束面）；`wiki/survey/2026-07-15-system-first-survey-protocol-v1.md` 与
`wiki/survey/2026-07-19-sf-bibliography-v1.md`（GATE_BOUND：分别被 sf_protocol_contract 读
字节、sf_bibliography_generator 消费）；protocol amendment 1/3-8 七件（GATE_BOUND：
test_sf_query_compiler_profiles 的修正案覆盖矩阵 oracle 读原件短语——首轮删除后门禁 cmd1/
cmd3 变红，当场恢复；这九件的最终退役属引擎 3 的合同外置决策，不属清理决策）。配套：build_ai_context_manifest 四元组清空/收缩、sf_release_binding_check
的 --legacy-regression 死分支随对象退役。

后续波次（B2=CLAUDE/AGENTS 瘦身+过期口径重写、C 收尾、E 收尾）按各自 commit 追加到本 digest。配置化方案（293→约 107 件，合同引擎/资产引擎/薄壳统一）已由普查
报告备好，实施待 owner 在方案上裁定。
