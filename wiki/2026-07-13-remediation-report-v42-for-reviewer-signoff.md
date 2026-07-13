---
title: "v4.2 博导级对抗审查 · 整改报告（呈外部审查者盖章）"
date: 2026-07-13
stage: 1-problem-definition
responds_to: "2026-07-13-v42-doctoral-adversarial-integrity-review.md"
remediated_object: "2026-07-12-research-proposal-v42-external-review.md（post-fix 快照）"
owner_ruling: "Decision-Log 续28（五项裁决）"
self_check_round: "续28-⑤ systematic self-check"
nature: "REMEDIATION REPORT（逐 finding 处置表 + 证据指针），非 rebuttal；本文不作任何科学有效性/收敛/确证宣称"
verdict_requested: "外部审查者复核处置表 → 盖章（scoped sign-off）或退回残余发现"
integrity_stance: "FFP NOT ESTABLISHED / QRP 高风险 / 独立诚实审计已在 Stage-1 采纳（续28④）——本报告是其交付物之一，非其替代"
---

# v4.2 博导级对抗审查 · 整改报告（呈外部审查者盖章）

## 0. 一句话

对 2026-07-13 博导级审查的 **每一条 F/M 发现**，我们要么**已结构性修复并留机器可核证据**，要么**如实登记为 stage-gated 待决项（指明所属门）**，要么**由 owner 裁决保留为 contested 敞口（附引用）**——无一条被静默消解或改写。本报告不请求"科学已闭合"的判断；它请求审查者**核对处置表与证据指针是否属实、待决项是否正确挂门**，据此盖章或退回残余。审查者的完整性裁决（**FFP 未成立、QRP 高风险、需独立审计**）我们**照单接受并已在 Stage-1 落地为 P0 登记册 + 本报告**，而非用整改抵消它。

## 1. 本轮核验统计（我方对审查的独立复核）

按 reviewer-response protocol，先对审查的可核主张做逐条独立复核（Opus，vs 被审快照），再出本处置报告：

- **36 / 42 CONFIRMED · 6 PARTIAL · 0 REFUTED**（连续第三轮零驳回；审查引用文献全真、数学全对）。
- 6 项 PARTIAL **全部是范围收窄（narrowing），非推翻**。唯一触及**现行代码路径**的是 F-7；其余五项为 §1「可复核事实」层面的收窄（如"文件日期 2026-07-12 vs 首次 git 提交 2026-07-13 01:42:28"确为事实、但审查者自陈"不足以证明倒签"→ 收窄为需补双时间戳；"143 passed"实测成立但已被 live **159 passed** 取代；"29,000/57,638 checkpoint"为构建中移动量；"checker 12/12 PASS"其 scope 免责本就诚实）。逐主张 verdict 存于本轮核验 pass；此处只把**载荷性的** F-7 展开：

  **F-7 = latent（潜伏），非现行害（owner 续28 明裁）。数据流实证**：生产建库/评分路径**不向 `scrub` 传入 downstream `eval_golds`**，故 `scrub=True` 在确证/资格路径上**空转（no-op）**，**没有任何合法答案 span 被从开放语料里删除**，磁盘上无受损工件。F-7 描述的"把'答案存在是预期'实现成'答案必须被清除'"是一个**若未来调用方把 `eval_golds` 接进来才会引爆的雷**，不是当前发生的害。故降级为 PARTIAL，修复挂 **M1**（open-corpus 不 scrub 合法答案；per-item 注入 context 硬失败；`answer_presence_expected` 只描述性报告 overlap）。

## 2. Owner 续28 五项裁决（verbatim-faithful）

1. **M4 等级命名之争 → 推迟**："没必要纠结未来论文应该如何写"，当前聚焦数据集采样与工程基座夯实；等级标签依方法学须在 M4 **开火前**落定（非发表时），**具体选择推迟至 M3 签字**，此前不作 confirmatory 宣称。
2. **SESOI → 外部锚点设定**：Q-B 两支数值由 owner 从**外部锚点**（效用/文献惯例；Lakens 等价检验谱系 / MCID）设定，口径如实采用 **post-observation but externally justified** + prior-exposure register 公开全部先验效应观测（C-ASR-V2 电池等）。
3. **管理用词 → "就还好"**：不搞 DRAFT 重标运动，仅修事实陈旧处（如"4 errors"）。
4. **独立诚实审计 → 采纳，且 Stage-1 即重要**："稍微有一些学术欺诈和作弊，会导致后面几个月的工作被大量浪费掉"；形式 = P0 四登记册 + 修复后系统自检 + **详细整改报告呈外部 reviewer 盖章**。
5. **执行令**：先把本轮全部已识别问题修复完 + 系统性自检，**高质量锁定阶段性工作**，再出报告。另：全语料构建维持封存至 M2 选型落定（stage-gated artifact 纪律）；F-7 为潜伏雷非现行害。

## 3. 逐 finding 处置表

图例：**FIXED** = 结构性修复 + 机器可核证据；**FIXED\*** = 部分修复（框架/工件到位，剩余闭合挂门）；**DEFERRED@门** = 如实登记待决、挂明所属门（续29 SAP 冻结：estimand 重定义/新增确证原子一律推迟至 M3）；**OWNER-RULED** = owner 裁决保留/推迟（附引用）。

| # | 发现（一句话） | 处置 | 修复位置 / 门 | 核验证据（test / checker rule / register） |
|---|---|---|---|---|
| **F-1** | 主 estimand（相对降）与检验对象（固定绝对 margin）不一致、已知偏松 | DEFERRED@M3 | proposal §3.1（anti-conservative 已如实披露 + 敏感性比率 estimand） | 续29 SAP 冻结；`remediation_evidence.yaml:deferred_not_closed F-1`；owner 续28①聚焦 Stage-1 |
| **F-2** | SESOI 冻结不能称盲法/pre-observation | **FIXED** | proposal §3.2 / §9.3 / §14；改称 post-observation but externally justified，明文 disavow blindness | checker `BANNED-PREOBSERVATION-BLINDNESS`=PASS、`REQUIRED-POST-OBSERVATION-EXTERNALLY-JUSTIFIED`=PASS；`prior_exposure_registry.json`；owner 续28② |
| **F-3** | public deterministic evaluation 不能保留强 confirmatory 等级 | OWNER-RULED / DEFERRED@M3 | proposal §11 replayability-not-blindness；M4 等级推迟至 M3 | checker `BANNED-M4-CONFIRMATORY-GRADE`=PASS；owner 续28①（"此前不作 confirmatory 宣称"） |
| **F-4** | 单次 K-pool 条件推断遗漏生成随机性 | DEFERRED@M2→M3 | proposal §13.4 缺口表（generation-robust ρ：跨 seed 期望+下分位、外层 group/内层 replicate） | checker `REQUIRED-GENERATION-ROBUST-RHO`=PASS（tracked, not adopted）；续29 冻结 |
| **F-5** | 无 load-bearing RDU-vs-strongest 归因原子 | DEFERRED@M3（contested） | proposal §3.1（H_RDU_VS_STRONGEST 具名登记为 UNRESOLVED/contested，m=6 不变） | checker `REQUIRED-RDU-VS-STRONGEST-ATOM`=PASS（named/tracked）；续29 冻结不新增原子 |
| **F-6** | full-corpus 审计由 mode 字符串自证、无 upstream corpus lock | **FIXED\*** | `docs/corpus.lock.json`（content_hash+doc_count+upstream identity）+ `corpus_lock.py:verify_corpus_lock`（fail-closed）；57,638 全建 + datasets.lock 上游 revision/checksum pin 仍属 **M1 gap** | checker `REQUIRED-CORPUS-LOCK-EXISTS`=PASS；`test_corpus_lock.py`、`test_corpus_audit_axes.py`；proposal §6.4 L234 |
| **F-7** | `answer_presence_expected` 的 scrub 语义与开放语料任务相反 | OWNER-RULED latent / DEFERRED@M1 | 生产路径未传 `eval_golds`（scrub 空转，无数据受损）；修复挂 M1 | 续28 明裁 latent；数据流实证见 §1、§6①；`deferred_not_closed F-7` |
| **F-8** | group-aware draw 三隔离漏洞 + "fixed seed equally tamper-evident"错述 | **FIXED\***（框架）/ DEFERRED@M2（结构门） | `deterministic_draw.py:14-15,34` 头部改写为 "replayable, not selection-blind"，具名撤回"equally tamper-evident"；100% coverage / singleton / force_supersede 三门挂 P2/M2 | checker `BANNED-EQUALLY-TAMPER-EVIDENT`=PASS；response v5 §3b/§3e 撤回 |
| **F-9** | 一次性 M4 状态机与 §13.3 M5 迭代自相矛盾 | DEFERRED@M3 | 机器可读状态机待落（M4_FAIL_FINAL 终局） | `deferred_not_closed F-9`；续29 冻结 |
| **F-10** | 无博士级 load-bearing theorem（finite-sample ε_n、同对象） | DEFERRED@M2/理论轨 | 现仅 generic argmax-mismatch lemma（§10.2 已诚实标注非收敛） | `deferred_not_closed F-10`；#27 同对象绑定待闭合 |
| **M-1** | 两个 no-harm 原子不是正向复制 | DEFERRED@M3 | proposal §3.1：头条如实限定单焦点集 | `deferred_not_closed M-1` |
| **M-2** | Q-B 单数据集不能支撑一般 TFRL 身份 | DEFERRED@M3 | proposal §3.2：身份主张显式限定单焦点、跨集泛化推迟 | `deferred_not_closed M-2` |
| **M-3** | random comparator 应用条件期望（pool mean-U），非一次幸运抽签 | DEFERRED@M3 | proposal §13.4 缺口表（primary 比 selector U vs pool-mean；实际抽签仅留部署模拟） | checker `REQUIRED-POOL-MEAN-COMPARATOR`=PASS（tracked, not adopted）；m=6 不变 |
| **M-4** | 同权重异 prompt 不是 weight-independent 跨源 | DEFERRED@M2 | proposal §4.2 L157：改称 context-differentiated，收益须为 MEASURED δ_corr | `deferred_not_closed M-4`（selector 纳入前须实测误差去相关） |
| **M-5** | 小簇尾部推断未证成 | DEFERRED@M2 | BCa/studentized-t vs wild-cluster vs randomization，M2 按 simulation 选 | `deferred_not_closed M-5` |
| **M-6** | 配置多重性账本不全（search space） | DEFERRED@M2（现 INCOMPLETE） | `experiment_attempt_registry.jsonl` 现为浅扫描，未捕获 config-selection 轨迹 | `deferred_not_closed M-6`；`prior_exposure_registry.json:p0_gate_status`（OUTSTANDING） |
| **M-7** | q2q 预训练回生 test query 盲点 | DEFERRED@M2 | proposal §6.4 L238：规则冻结后 exact/fuzzy/semantic overlap 审计（描述性交付） | `deferred_not_closed M-7` |
| **M-8** | 提交状态与发布文字不事务一致（"4 errors"陈旧、"converged/0 residual"） | **FIXED**（机制） | `build_release_manifest.py` 记 live SHA+dirty+pytest+checker verdict（永不复制旧报告）；§13.4 更新为 159 passed/0 errors 并标旧快照陈旧 | checker `BANNED-STALE-FOUR-ERRORS`=PASS；`release_manifest.json`；`discrepancy_register.md` item 1&2 |
| **M-9** | conformance checker 通过 ≠ proposal 自洽 | **ADDRESSED** | checker 加 10 条新规则（12→22 条：8 semantic + 2 file-existence）；报告全程 scope 免责、人工/独立审查与机械 lint 分栏 | `v42-conformance-report.md` §Nature；`remediation_evidence.yaml:scope_disclaimer` |
| **P0** | P0_INTEGRITY_FREEZE 四登记册（续28④） | **DELIVERED / 内容实质充实；gate 如实 NOT_PASS** | 四册全部在盘（含 `append_only_erratum_for_v42.md`，19 行处置表）；prior_exposure 机采充实：C-ASR-V2 selector 效应量明示（realized fraction ~24%/~42%、MBR/random/length 结果）、17 个提示模板、K1-K11 指标族自 464 工件、5 个 dev 暴露事件（含 LOCKED_HOLDOUT 11.20% 永久降级）；experiment_attempt 574 行带 status/claim_id/inferred 逐行标注 | `prior_exposure_registry.json:p0_gate_status` = **NOT_PASS（如实）**：config-selection 轨迹（M-6）仅部分可自盘面回溯（未持久化的废弃扫描入 manual_completion_todo）；"独立评审者收到只读快照"为流程步骤——本报告送达审查者即满足该项 |

## 4. 我们**没有**做什么，以及为什么

- **未把 v4.2 重写成 v4.3**。owner 续28③"就还好"——不搞 DRAFT 重标运动；且 Stage-1 聚焦问题定义与数据集/工程基座，SAP 设计迭代（estimand 重定义、新增确证原子）**一律冻结推迟至 M3**（续29）。故本轮**不新增 primary 原子、m=6 不变**，只落地"修事实陈旧处 + F-2 SESOI 改称 + 双时间戳 + 机器可核工件"这批**非 SAP** 修复。曾一度半应用的 SAP 前向编辑（F-1/F-4/F-5/M-3/M-4/M-7/PF3）已**回退**并改登记为缺口表待决项。
- **未完成全语料构建**。全语料（FiQA 57,638 docs）建库**维持封存**至 M2 embedder 选型落定（stage-gated artifact 纪律，续28）；上游 revision + 公开 checksum pin 进 `datasets.lock.json` 是明列的 **M1 gap**。当前只交付 `corpus.lock.json` 的**验证契约**（fail-closed），不冒充"已建成官方全语料"。
- **未确定 M4 证据等级**。按 owner 续28①**推迟至 M3 签字前**落定（方法学要求：等级须在开火前定、非发表时定）；在此之前**不作 confirmatory 宣称**。这是一条**开火前承诺（before-fire commitment）**，非事后择定。
- **P0 未标 PASS**。四登记册仅 existence 满足、内容未齐（见处置表 P0 行）；本报告**如实呈 P0 为 INCOMPLETE**，绝不因 checker 的 existence-PASS 而报 P0 已闭合。

## 5. 系统性自检结果（续28-⑤）

- **一致性 checker（live）**：`scripts/checks/v42_conformance.py` vs `docs/checks/v42-rules.yaml` → **22 / 22 PASS，0 failed**，verdict = *DOCUMENT PACKAGE READY FOR EXTERNAL REVIEW*（`v42-conformance-output.json`，含 12 条原规则 + 10 条本轮新增规则：8 条 remediation semantic rules〔banned/required phrase〕+ 2 条 file-existence 检查〔`REQUIRED-CORPUS-LOCK-EXISTS`、`REQUIRED-FOUR-INTEGRITY-REGISTERS`，type=file_exists〕）。注：`docs/checks/v42-conformance-report.md` 正文仍记 12/12，是**前一规则集**的 run，被 22 条 live JSON 取代；`discrepancy_register.md`（generated_at 2026-07-13T03:25:43Z）**在 22 条 run（run_utc 2026-07-13T03:52:27Z）之前生成，故尚未收录此 12/12-vs-22/22 不一致**——此处即为该不一致的首次显式披露，登记入册作为 M1 待办（本报告不隐藏，只是尚未落进 register）。**checker 只验文档包自洽 + 工件存在，certifies nothing about 科学有效性**（M-9 免责，全程分栏）。
- **标准测试入口（live）**：`PYTHONPATH=src pytest -q`（W1）→ **159 passed, 0 failed, 0 errors, 3 warnings**（returncode 0；`release_manifest.json:standard_test_entry`）。取代审查所见 143、及更早"4 errors"。诚实注：需 `SPEECHRL_DATA_DIR`（如部署）；缺失时 4 个数据依赖测试以显式 `RuntimeError` 失败（环境非代码）。
- **P0 登记册已建**：`prior_exposure_registry.json`（扫 574 件 `_repro` 工件）、`experiment_attempt_registry.jsonl`、`discrepancy_register.md`、`release_manifest.json`（`build_registers.py` / `build_release_manifest.py` 播种）——内容完整度如 §4 / 处置表 P0 行如实标注。

## 6. 三处对审查者的敬意商榷（如实提出，非抵赖）

1. **F-7 应为 latent 而非现行害**。数据流实证（§1）：生产路径未向 scrub 传 `eval_golds`，scrub 空转、零合法答案被删、磁盘无受损工件。我们**接受该轴设计错误必须修**（挂 M1），但请求把它记为**潜伏雷（若未来接线才引爆）**而非"当前已改变研究任务"的现行害——这与审查 §5.1 "未见凭空编造的 confirmatory result"一致。
2. **E2（SESOI）采较轻但诚实的选项（owner 裁决）**。审查建议由未接触效应值的独立统计人员盲设 SESOI、或改用一套全新数据确证；owner 续28②采**较轻**路径：数值由 owner 从**外部锚点**（Lakens 等价检验 / MCID 传统）设定、口径如实标 **post-observation but externally justified**、并以 prior-exposure register 公开**全部**先验效应观测。我们**如实承认这比盲法轻**、公开种子下的 selection-blindness 残余仍是 contested 敞口（§9.8/§11），不冒充已消解。
3. **独立性以"外审盖章 + 机器可核登记册"落地，而非人员隔离**。审查建议独立 custodian / 两名非开发者复跑 / 第三方冻结后评分；owner 续24 已否决全员锁死路线（"我们是在做研究而不是做复杂的系统工程"），续28④采**诚实审计**形式 = P0 登记册 + 系统自检 + **本报告呈外部审查者盖章**。我们据实说明：这是**制度形态的差异**，不是把独立性取消；人员级独立评分作为 M4 前的**可选**升级保留（F-3 blinded confirmatory 选项）。

## 7. 请求（盖章位）

请审查者**核对 §3 处置表的每一行**：修复项的证据指针（test 名 / checker rule / register 路径）是否属实、DEFERRED 项是否**正确挂门**（续29 SAP 冻结、P2/P4/P5 门）、OWNER-RULED 项引用是否忠实、P0 是否被**如实呈为 INCOMPLETE**。据此二选一：

- **盖章（scoped sign-off）** —— 明确其范围：认可"**本整改包忠实兑现了其所声明的修复、且全部待决项被正确挂门并如实披露**"。**盖章不等于** M1 闭合、不等于 confirmatory 就绪、不等于科学有效性通过（这些仍是 owner §14 签字、全语料建成、K-harness、live cross-modal smoke 等 STOP-THE-LINE 门）。
- **退回残余发现** —— 指出处置表中任何**证据不符、错误挂门、或应现修却被推迟**之处；我们按 reviewer-response protocol 逐条再处置。

盖章位：

```
外部审查者签字：____________________   日期：__________
□ 盖章（scoped：整改忠实 + 待决正确挂门；非 M1 闭合/非确证就绪）
□ 退回（附残余发现清单）
```

> **范围声明（按 M-9 设计重复）**：本报告 + 其引用的 checker / 登记册是**机器辅助的内部第二遍 + 呈外审盖章**，**不是**独立监督、**不是**已完成的独立完整性审计。审查的完整性裁决（FFP 未成立、QRP 高风险、需独立审计）**依然成立并被采纳**；绿色 checker、159 passed、22/22 PASS 均**不得**被读作科学有效性、M1 闭合或确证就绪。

---

## 附录 · 只读证据快照（机器生成，供第三方核验）

> 生成方式：对下表每一文件计算 SHA-256（脚本逻辑等价于 `Get-FileHash -Algorithm SHA256` / `sha256sum`）；两仓 HEAD 以 `git rev-parse HEAD` 取得。**审查者核验路径**：clone 两仓至下列 HEAD → 对每行重算哈希 → 与本表逐行比对；任何不符即构成"证据不符"退回理由（§7）。本报告自身不在表内（追加本附录会改变自身哈希）；其权威版本以伞仓 git 历史为准。

伞仓 HEAD: `e01c0c02ce22` · W1 HEAD: `ab1c68017671`

| 仓 | 工件 | SHA-256 | bytes |
|---|---|---|---|
| 伞仓 | `docs/corpus.lock.json` | `192dd2d0c9a5b5a0fc35b9f7b6a07cd0eb8b1dcdf9452fe4b032c63957ea0c79` | 1541 |
| 伞仓 | `docs/integrity/prior_exposure_registry.json` | `7d1a33dae9dee0367986392a74fac82ab581254f470cffd4605432f09586b3c2` | 77790 |
| 伞仓 | `docs/integrity/experiment_attempt_registry.jsonl` | `7ea5ef199a3376bb61a9e25beb6873cfbe2a10b43f9442f9dfb8171f749f7a49` | 250595 |
| 伞仓 | `docs/integrity/discrepancy_register.md` | `50440434d0ccc822d51ac100accbcdac7e537554dfd5f7057655aa722adb6dde` | 4222 |
| 伞仓 | `docs/integrity/release_manifest.json` | `8bf43ab147a8542cdbec931bb2131fd5ab5a5fc1b685fe430dcf9e7e4f194163` | 4497 |
| 伞仓 | `docs/integrity/append_only_erratum_for_v42.md` | `230c1b6ce6403648db10a98e122070a425c763a42725033bec0dae7281de59fd` | 6025 |
| 伞仓 | `docs/integrity/remediation_evidence.yaml` | `100925458507618295124076f21c57ff13070733a15d8d8429435b11ac033e23` | 15395 |
| 伞仓 | `docs/checks/v42-rules.yaml` | `b71d92fad60af6ccf657b771fd0e1f81ff75d1eeedb003a17ddb47d0f6d8f45a` | 19052 |
| 伞仓 | `docs/checks/v42-conformance-output.json` | `2d30c98ca71a17add09dc545f72d5932acc39dc0ae42574caecfd212586a5833` | 13088 |
| 伞仓 | `docs/checks/v42-environment.txt` | `ff931aad7326d5baee2a5742aecb828d4c4cea9da86196afa99c2df32b326c6e` | 752 |
| 伞仓 | `docs/checks/v42-conformance-report.md` | `7aa4a996361c536218a446a6fdad8b8ce84e5481851d270e55eea20d2444ba85` | 14428 |
| 伞仓 | `scripts/checks/v42_conformance.py` | `ab5cad5f04899e04124d10e35e15e25555f8219cc23da0d7cb05cb1d084e57ce` | 27241 |
| 伞仓 | `scripts/checks/build_registers.py` | `1e49981442775895b90d8affbc31e51e0e0f897ec8cfefc589ec27eadff163f9` | 39863 |
| 伞仓 | `scripts/checks/build_release_manifest.py` | `da8bfb36ba477473c2426d1d1498e0b01775e3b4fa860075abf88b24aa61a4e0` | 10615 |
| 伞仓 | `wiki/2026-07-12-research-proposal-v42-external-review.md` | `3f0ac5b6e5c5e021ffc9b85c10f7b8b9f07a4bd6395de6350bcd8c87e1ba18e0` | 126124 |
| 伞仓 | `wiki/2026-07-13-v42-doctoral-adversarial-integrity-review.md` | `df594f546d3fd263994eb6009274e30392181909d3babaf73a5deaec3324b10b` | 32416 |
| W1 | `scripts/knowledge/corpus_lock.py` | `f9ab4bc3836275cf01090ebec1d0451e7aec090267e55037cdd895e5f17aaf48` | 19626 |
| W1 | `scripts/knowledge/test_corpus_lock.py` | `c220d5512eb73f9f9516fa8e3d232e2e7e680d46ac5207fb71ce8b977226e01c` | 11279 |
| W1 | `scripts/knowledge/test_corpus_audit_axes.py` | `eb974f39a1fcfaacb7356e813d563c456dce70d92b4e59a99bb942359798d371` | 14747 |
| W1 | `scripts/knowledge/kb_batch_build.py` | `7569a1569c0b2c89762d2a579b4642f53a85ac408ca6fa5cdc881cb87d4df5c3` | 84989 |
| W1 | `scripts/knowledge/kb_embed.py` | `fbd838b6bf2e5927c2b19b88852cf8d88098b70dad643038c756f9f9e503588d` | 54293 |
| W1 | `scripts/knowledge/build_full_corpus.py` | `f1330d7e7c1fe48293fa9f09a151098a4efc7d0aad95a1f5b4ddeb8a1feec16f` | 13734 |
| W1 | `scripts/baselines/deterministic_draw.py` | `7e6444ddf8ebbb10d883296bf302a5a26a6c36b42b32302fead9af3eb3835fe0` | 54936 |
