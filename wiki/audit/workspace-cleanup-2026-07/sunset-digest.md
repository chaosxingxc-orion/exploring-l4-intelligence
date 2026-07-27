# Sunset Digest —— 71 份 wiki-root 定日期记录 + 6 代 retired workbench 的知识蒸馏

按**链**组织。每链五节：尝试 / 死因（引判决词原文）/ 终局与锚点 / 教训 / 被删清单。字节仍在 git 历史，本文只留"为什么"。

---

## A · pre-system-first（06-23 → 07-04）：agent 级问题被自己的预注册判据杀死

**尝试。** W4 在冻结 omni 池化嵌入上做 training-free ICL/few-shot 解耦探针；一场预注册的 agent 级 TFRL 合理性战役（M1–M5 五条机制车道各带冻结 kill 阈值）；战役失败后转语义层，产出 174KB 跨域综述（充分性标尺 H_prompt−H_fix、F1–F11 方法族谱）并蒸馏 CP-1..CP-8，K2 由 owner 选定 CP-1/3/8/4。

**死因。** `recommended: NO-GO`；`owner_verdict: "NO-GO (ratified by owner in-session, 2026-07-04; the elective V4 amendment fork was declined)"`。M3 实测 `F = 0.38108 vs the frozen 0.01 kill threshold`（"a genuine, informative kill"）；M5 = `NO PASS, exact zero — an inert-instrument null`；M2/M4 design-only → inconclusive。敌意面板：`all six charges stand, 24 of 24 argued objections stand`。W4 向量类前提自证退役：`"speaker never written to the pooled vector" is RETIRED`。综述被后续法证审计降为 hypothesis-grade 背景。

**终局与锚点。** NO-GO 是关闭而非推迟，仅在外生条件 r1–r3 下重开。wiki 根**无保留件**，锚点为 `wiki/Decision-Log.md` 与 `Per-Work-Status.md`——这正是 07-15 重开 system-first 时必须补"07-04 NO-GO → 07-06 amendment → 07-15 S0"引用链的原因（v1 审查 P1-GOV-3 点名）。

**教训。** ①kill 阈值先冻结再测（M3 之所以 informative 全在于此）；②inert-instrument null ≠ 效应不存在，负结果按失败形态入账；③**closure fence**：关闭的问题须给可外生检验的重开条件，否则以改名复活（今天"碰撞项标注"直系继承）；④**grade vocabulary**（settled/scoped/hypothesis-grade/directional）+ confirms/establishes/demonstrates/significant 四动词禁用于自产数字。

**被删（4）**
```
2026-06-23-omni-embed-speech-disentanglement-1.2.1.md
2026-07-03-omni-agentic-tfrl-go-no-go-decision.md
2026-07-04-stage1-problem-definition.md
2026-07-04-stage1-semantic-tfrl-survey.md
```

---

## B · 07-11 法证审计 / STOP-THE-LINE：实验层整体停线

**尝试。** 外部 34 项对抗审计 → 6 个独立核验代理对 HEAD 逐条重验（实跑 dry-run、读 273 个结果 JSON、复算 CREMA-D 切分重叠 91/91 speaker & 827/827 sentence 对、逐行读 Lean）→ 过夜"全实验清白重做" → Proposal-R 预注册草案 + 89 条 survey 主张核验。

**死因。** 核验结论：审计几乎全对，`32 CONFIRMED / 1 STALE / 1 PARTIAL / 0 REFUTED`。硬事实：Phase-A 无 `--execute`、6 臂 PLAN ONLY；宏平均 WER 冒充 corpus WER；MBR `+0.0037` CI 跨 0；`8 池均只有 4.19 个不同候选、14.6% 八条全同`；W4 判据未过而文档写 "thesis holds"；`operator-linked 定理数 = 0`。回信 v1 被击穿：`verdict: RESPONSE PARTIALLY ACCEPTED; REMEDIATION CLOSURE REJECTED; STOP-THE-LINE REMAINS`、`publication_readiness: RED`——最不可原谅之处是**在承认"按报告入账、未经验证"的同一封信里把 DECIDED/TICKETED 写成"已执行"**。清白重做直接证伪自己：旧 MInDS "+0.126 增益"全由 card 因子驱动且 transductive，真 zero-shot 是**显著回归 −0.245 [−0.286, −0.201]**。Proposal-R 停在 `DRAFT — owner signature required`，Phase-B 未解封。

**终局与锚点。** 实验线自此未真正重启（后续全部零 GPU）。树上三件：`2026-07-11-step1-completion-forensic-integrity-review.md`（终判 `REJECT STEP-1 CLOSEOUT；保持 STOP-THE-LINE`）、`…-group-split-statistics-design.md`（#26，DESIGN — NOT IMPLEMENTED）、`…-W4-fresh-proposal-draft.md`（DRAFT 未预注册）。

**教训。** ①**六级状态制** ACKNOWLEDGED→DECIDED→TICKETED→IMPLEMENTED→VERIFIED→PUBLISHED，状态词是合同不是修辞；②**完成度永不聚合上标 + 三线分签**（PENDING 就写 PENDING）；③cell 级与 item 级口径强制分列（"65/65 零失败"在 item 级有 510/4439 未评分）；④macro-WER ≠ corpus-WER，同 cohort 噪声差分才能拆种子混杂；⑤claim ledger 机器化——人类横幅不够，机器状态须同步撤回；⑥核验代理"既不为仓库辩护、也不为审计辩护"＝多镜头内审环的原型；⑦理论同对象门：Lean 与 operator 脱节 ⇒"系统收敛已被证明"永久禁用。

**被删（7）**
```
2026-07-11-adversarial-review-of-stage1-audit-response.md
2026-07-11-overnight-remediation-report.md
2026-07-11-proposal-R-prereg-draft.md
2026-07-11-response-to-reviewer-stage1-audit.md
2026-07-11-response-v2-erratum-and-forensic-reply.md
2026-07-11-stage1-audit-response-and-rulings.md
2026-07-11-survey-full-verification.md
```

---

## C · RDU 提案 v4 → v4.1 → v4.2（07-12 → 07-13）：三连拒

**尝试。** 对象定为**前端多模态知识体系**（Retrieve–Discover–Use 三段），后端 reward 仅作数据集无关信号供给，reward-guided 轨迹选择算子作 TFRL 身份锚；配两份四透镜调研（热词偏置、后融合/LM 重排序）作证据底账。三版各带 5 路独立复核。

**死因（三轮）。** v4：`REJECT/NO-GO`，四 FUNDAMENTAL + QRP；核验 `37 CONFIRMED / 5 PARTIAL / 0 REFUTED`，无一被驳。v4.1：回信 `ACCEPT WITH SERIOUS RESERVATIONS` + 方案 **`MAJOR RECONSTRUCTION / REJECT FOR STAGE 2`**；核验 `39/3/0`——连续第二轮无一被驳。五个 F′ 中最致命：`squtr mini-corpus 使用 test qrels 构建，违背 KB 独立性`（310 文档＝110 test-qrels 全部正例＋200 干扰，正例密度较官方 57,638 文档抬升约 ×186）、`proxy reward 被误称为 verifiable reward`、`owner 可以拒绝 custodian，但不能靠裁决改变统计事实`。v4.2：`verdict: "MAJOR RECONSTRUCTION；NO-GO for M3/M4；不得称 locked/converged/confirmatory-ready"`、`integrity_verdict: "FFP_NOT_ESTABLISHED；QRP_RISK_HIGH；INDEPENDENT_AUDIT_REQUIRED"`；F-2「pre-M2 SESOI 冻结在时间上已不可能成立」（只能称 post-observation but externally justified）、F-6「full-corpus audit 由模式字符串自证」。整改报告呈盖章后**再被退回**（P0-A 七项），并暴露"提交信息声称 conformance JSON regenerated，实际只改一个文件"的自查勘误。

**终局与锚点。** RDU 前端方案作为主提案死亡，降为 Stage-1 问题定义交付物（续32③）。树上：`2026-07-12-research-proposal-v42-external-review.md`、`2026-07-13-v42-remediation-signoff-doctoral-adversarial-review.md`。

**教训。** ①**信息边界 guard 的诞生现场**：用 test qrels 构语料＝把部署没有的信息喂进检索路径 → 每个杠杆过 read-out / new-info 判别；②proxy vs verifiable reward 命名纪律，真效用 U 与代理 Û 分写；③K=1 不能同时是等预算对照，不等预算差无法归因；④custody 只能诚实命名为 `public deterministic evaluation`；⑤"independent conformance checker"具名撤回——同工作流内可改信件的检查者只能叫 internal consistency check；⑥起草流程解释是因果非免责，"AI 参与不构成任何减责事由"；⑦两条调研硬结论仍有效：chat-API omni 下传统偏置技术**逐族结构性失效**（prompt 实体列表是唯一原生存活形态但随规模退化）；`把 LibriSpeech 打到 ~2% 的是声学/E2E 模型本身，不是 LM 第二遍`，受约束 N-best 选择是唯一可移植 training-free 原语。

**被删（10）**
```
2026-07-12-omni-hotword-biasing-survey.md
2026-07-12-omni-lm-rescoring-survey.md
2026-07-12-retrieve-discover-use-analysis.md
2026-07-12-research-proposal-v41-external-review.md
2026-07-12-response-v3-to-forensic-completion-review.md
2026-07-12-response-v4-to-adversarial-integrity-review.md
2026-07-12-response-v4-and-v41-doctoral-adversarial-review.md
2026-07-12-response-v5-to-doctoral-adversarial-review.md
2026-07-13-remediation-report-v42-for-reviewer-signoff.md
2026-07-13-v42-doctoral-adversarial-integrity-review.md
```

---

## D · 07-13 阶段重校准 + 预检：A-SEL 死于阶段错位而非科学缺陷

**尝试。** 另起 Stage-2 提案 **A-SEL**（全新 program ID `W1-ASEL-S2-001`，不复用 v4.2 任何 family/seed），同时请一次 15–20 分钟 **survey 覆盖设计预检**（Q1–Q6）并通报记录闭环（自检环 21→7→1→0）。

**死因。** 结构层：`stage2_draft_structure_verification: REFUSED_RETURN_FOR_RECONSTRUCTION`、`m2_unfreeze: PROHIBITED`；`Round 4 裁决：A-SEL 可以成为测量研究，但目前未建立博士级方法新颖性`；F-D1 漏掉同构的 ASR selector 文献，F-D3「草稿把 ρ 换了对象，却声称与 owner 原 ρ 一致」。阶段层（决定性）：重校准审查判定根本不是 Stage-2，`stage: 2` 标签本身是身份错误。预检件判 `overall_verdict: "RETURN_WITH_MANDATORY_REVISIONS"`、`record_closure_verdict: "NOT_ACCEPTED_AS_CLOSED"`、`i4_novelty_verdict: "NARROW_PLAUSIBLE_WHITESPACE_NOT_ESTABLISHED"`；最锋利两句：`裁决。RECORD_CLOSURE_NOT_ACCEPTED。「21 → 7 → 1 → 0」至多说明既有 checker 命中归零，不说明审计语义空间归零`；`Q3 verdict：REJECT_CURRENT_WORDING`。八类 family 覆盖判 `FAIL_MAJOR`。

**终局与锚点。** A-SEL 作为 Stage-2 对象终止，工作面回落 1A/1B/1C 三分制，团队九项 `ACCEPT_IN_FULL`。树上：`2026-07-13-response-v6-stage1-recalibrated-review.md`。

**教训。** ①**Stage-1A/1B/1C 三分法**在此定型（1A 广泛 survey+候选构造+纸面原型；1B 方向性原型须 owner 显式放行；1C owner 选唯一问题 kill/pivot/proceed/engineering-only，**绝不自动滚入 Stage-2**）——今天 stage taxonomy 的直系祖先；②**checker 归零 ≠ 语义闭环**（自动检查只覆盖被编码的不变量）——"oracle 等强/能力包络"防线的首次提出；③**provenance 三元组**：`evidence_snapshot` 与 `artifact_snapshot` 分栏，canonical hash = **git blob 字节**（流通的 `cd987ff0…` 是 CRLF 变体，正典 `6c6adba2…`）——今天写在 CLAUDE.md；④文档不可能记录含它自己的未来提交；重复 YAML 顶层键使 13 项机读记录退化为 2 项 → 机读块入库前须实测解析；⑤更正走独立更正件，被审原文一字不动、错误保持可见。

**被删（8）**
```
2026-07-13-precheck-provenance-correction.md
2026-07-13-reviewer-precheck-survey-design-and-record-closure.md
2026-07-13-reviewer-precheck-survey-design-and-record-closure-doctoral-review.md
2026-07-13-response-v6-to-signoff-adversarial-review.md
2026-07-13-response-v6-doctoral-adversarial-review.md
2026-07-13-response-v6-correction.md
2026-07-13-stage1a-position-and-recalibration-response.md
2026-07-13-stage2-proposal-ASEL-v0.1-for-reviewer-verification.md
```

---

## E · 07-14 Survey-v2 / P0-R / 知识栈 / 决策包：selector-first 身份体系的建立与瓦解

**尝试。** 一天四线并行：Survey v2 广度 scout（~94 论文簇）+ 邻居/kill 矩阵 + Stage-1C 决策包（I1/I2/I3/I4/UMBRELLA 五身份 dossier）；可回放审计模板（replay bundle 七文件：protocol / search_events / search_results / screening_decisions / papers / claim_evidence / flow_report）；身份合同 v1 冻结（FROZEN@dce5c79）+ 修正案 №1；四探针协议 v1 与 Round-2 协议 v1；一份 AI 协同知识栈选型审查。

**死因（三轮递进）。** 初审 `verdict: "MAJOR_REVISION"`、`SURVEY_COMPLETE / 调研收官 = NOT_ACCEPTED`、决策包 `DOWNGRADE_TO_PRE_STAGE1C_DECISION_DRAFT`；最重一条 Round 6 `裁决：FUNDAMENTAL` — **moving-goalpost / conjunctional novelty laundering**（看到近邻后才给身份加限定词）；另 `裁决：BLOCKING`（"这是 query narrative log，不是 replay log"）、`~93 只能叫人工估计，不能做精确分母`。再复审 `RETURN_FOR_MAJOR_REVISION_P0_SIGNOFF_REJECTED`，**拒绝签收"P0 八项全部执行"**并开 P0-R1..R8；判定 `owner 的治理裁决应被尊重，但不能被扩写成未发生的审计签署`（团队把 owner 执行授权写进 `integrity_reviewer` 位）。第三轮 `p0r_score: "2 CLOSED_FOR_PRIOR_DEFECT + 5 PARTIAL/REOPENED + 1 NOT_DONE"`，**阻断级**判定 `P-γ 目前测错对象`：`δ_corr` 同名异义（理论＝误差去相关；探针＝选择重合 >90%）——"两个 scorer 可以 100% 同选且全对，也可以 100% 同选且全错"，四探针协议 v1 作废。同日预检重评 `ACCEPT_DIRECTION_WITH_TARGETED_RECORD_AND_SURVEY_CORRECTIONS`，接受 breadth-first 对象但判 `CELLWISE_ONLY_UNTIL_JUSTIFIED`——**禁止无权平均的总 rho**。

**终局与锚点。** Survey v2 从未被签收；Round-2 一条查询未跑；四探针零 GPU；决策包永停 `PRE_STAGE1C_DECISION_DRAFT`。整套 selector-first 身份体系次日被 system-first 重定向降为组件 dossier。树上：`2026-07-14-identity-contracts-v1.md`（FROZEN，六身份三结局判据 + 合取量词规则 + same-selector contract）、`2026-07-14-response-to-knowledge-stack-evaluation.md`。

**教训（纪律密度最高的一链）。** ①**合取洗白禁令**：身份定义须检索前冻结，事后加限定词须事先登记；每个合取身份要回答"去掉哪一项后科学结论不成立"→ 今天的方法占据渐进主义与 identity freeze；②最强允许结论 token **按身份索引、无全局 token**，须带强制伴随 token（`SEARCH_RESULT_UNIVERSE_UNAVAILABLE` / `SCIENTIFIC_SATURATION_NOT_ASSESSABLE`）并钉记录集版本；`NO_DIRECT_MATCH_WITHIN_LOGGED_SCOPE` 被裁为"把查询被记下偷换为结果宇宙被完整审阅"而停用；③**不得补造历史日志**——写 `RAW_EVENT_UNAVAILABLE`，"诚实降级是合格 response"；④四类计数分列（搜索/抓取/论文/证据）且机器可重算，证据五级状态机不得跳级；⑤**owner 裁决 ≠ 审计签署**，治理授权与诚信签署永久分栏 → 今天 reviewer-drift-guard 与三线分签；⑥一符号三语义会让 kill-if 数学上不可执行，**拆名**是唯一解；⑦信任分层 T0–T4，AI 生成层不得反污染事实层，`generated_by` ≠ `verified_by`；"没有单一开源项目同时成立；组合必要，但组合必须只有一个正典"＝今天 wiki 唯一正典、web 为镜像的依据；⑧签字块不得混签。

**被删（17）**
```
2026-07-14-1b-probe-protocol-v1.md
2026-07-14-ai-assisted-survey-knowledge-stack-open-source-evaluation.md
2026-07-14-identity-contracts-amendment-1.md
2026-07-14-p0r-progress-review-submission.md
2026-07-14-p0r-progress-submission-doctoral-adversarial-rereview.md
2026-07-14-p0r-response-to-remediation-rereview.md
2026-07-14-resp04-gate-a-execution.md
2026-07-14-response-to-precheck-doctoral-review.md
2026-07-14-response-to-precheck-doctoral-review-adversarial-reassessment.md
2026-07-14-response-v2-to-reassessment.md
2026-07-14-round2-search-protocol-v1.md
2026-07-14-stage1c-decision-package.md
2026-07-14-survey-response-replayability-template.md
2026-07-14-survey-v2-and-stage1c-decision-package-doctoral-adversarial-review.md
2026-07-14-survey-v2-p0-remediation-response-doctoral-adversarial-rereview.md
2026-07-14-survey-v2-response-and-p0-remediation.md
2026-07-15-replayability-template-token-overlay.md
```

---

## F · 07-15 selector-first 收尾提案：被"零 GPU 声明"击穿

**尝试。** 把三轮整改收敛成 Stage-1A 提案（对象＝label-free、供给条件的选择算子在冻结 omni〔模型×任务〕矩阵上的兑现面 ρ(c)/H(c)/regret），带三轮敌意内审环，请签 round-2 检索设计。

**死因。** `decision: "RETURN_FOR_MAJOR_REVISION — 不签 round-2 search design；不放行 Stage-1B"`。第一条即致命：**"GPU 运行至今为零、全部证据为文献台账级"与同仓库已登记的 574 个历史运行工件、ASR selector battery、MMAU selector 和已触碰的 dev/test 数据直接冲突** —`重大 QRP/记录准确性缺陷`。另四条：Hydra 主入口是 stub，"当前基座是可运行但分裂的原型资产，不是配置驱动、可组合、可批量复放的实验基座"；canonical survey 丢失项目自己早已掌握的核心 prior（"已知文献遗忘"）；I1–I4 共同算子在邻近文献有标准名（不是 RL）；UMBRELLA 须独立 dossier 不共享 headline。

**终局与锚点。** 被 owner 以 system-first 取代（S0 签署，续48），本件降为组件 dossier，内容效力不变。树上：`2026-07-15-stage1a-research-proposal-doctoral-adversarial-review-v2-owner-clarified.md`、`2026-07-15-s0-program-identity-signoff.md`、`2026-07-15-record-system-denoise-and-rationale-survey-proposal.md`。

**教训。** ①**exposure 记账必须带范围**，禁止无范围的"0 次"→ 四字段记账诞生，正典载体 `2026-07-18-inherited-prior-exposure-union.md`；②"已知文献遗忘"是知识组织故障不是检索故障 → 提炼步须解决"看过但遗忘"（后固化为"FETCH 即登记，不登记不算读过"）；③脚本集合 ≠ 配置化实验图，逐探针写脚本会让实验差异与代码差异纠缠；④citation acceptance rule：承重引用须带版本/主张/定位器/核验状态方可进入结论。

**被删（2）**
```
2026-07-15-stage1a-research-proposal-for-reviewer.md
2026-07-15-stage1a-research-proposal-doctoral-adversarial-review.md
```

---

## G · Stage-1A system-first 十轮（07-15 → 07-19）：Gate S1 十次未签

**尝试。** owner 重定向后对象抬回"冻结黑盒 omni 核心之外的 reward-guided agentic control plane"（S0：primary_object＝黑盒 omni agentic system；north_star＝training-free reward-guided external control；TF-Strict 全系统零训练；selector 降组件）。十轮提案 v1→v10 + 十份博导审查 + 四轮 Gate S1 correction（#3/#4/#4A/#4B）+ P0-R8/P0-R9 窄幅复核，目标唯一：签下 Gate S1、执行第一条 systematic mapping 查询。

**死因（判决序列＝"失败形态逐层上移"的原始数据集）。**

| 轮 | 判决 token / 核心缺陷 | 被击穿的层 |
|---|---|---|
| v1 严评 | `RETURN_FOR_MAJOR_REVISION`；`stage1b_execution_gate: NO-GO`；`survey_execution_gate: NO-GO_UNTIL_SEARCH_PROTOCOL_SIGNED` | 科学身份/引用真实性 |
| v1 重校准 | `ACCEPTABLE_TO_PROCEED_WITH_STAGE1A_SURVEY_PROTOCOLIZATION`（撤回预算 cap 前置、RL 二选一、轨迹 headroom 冻结、QRP 红旗四项**阶段错位**判罚） | 评审自我校准 |
| v2 | 有条件批准协议实例化，**不批准执行首条真实查询** | 协议成熟度 |
| v3 | `Gate S1 暂不能签字`：类别宇宙盲区 / 48 条非可逐字执行查询 / 75 条截断无溢出规则 / 谱系 lane 缺失 | 查询可执行性 |
| v3 收官就绪 | v3 = `ACCEPT AS WORKING THESIS`；Gate S1 `WITHHOLD SIGNATURE — TARGETED MAJOR REVISION`（arXiv-only 不能冒充文献宇宙；venue tier ≠ study quality） | 来源边界/证据权重 |
| #4 再送签 | `WITHHOLD SIGNATURE — TARGETED CORRECTION #4 REQUIRED`（REC-2 只记 INCLUDED） | 记录完整性 |
| #4 prelaunch | `WITHHOLD SIGNATURE — CORRECTION #4A / PRE-LAUNCH INTEGRATION FIX REQUIRED` | 门禁 soundness |
| P0-R8 | `WITHHOLD SIGNATURE — 3 MAJOR + 2 MINOR；P0-R8 零新发现合同未满足`：package summary 可复现 **false-green**；validator 宣称强于实际约束 | 验收 oracle 强度 |
| C4B/P0-R9 | `WITHHOLD — 1 项 Gate 阻断 MAJOR`：**发现机制仍按术语召回，无法覆盖直接占据方法空间的工作** | 发现机制本身 |
| v4 | `WITHHOLD_STAGE1B_SURVEY_EXECUTION_PENDING_MAJOR_REVISION`：阶段本体错、"全部承重数字可机器复跑"超出九条命令能力、system-first 滑回 selector 交集 | 能力包络 |
| v5 | 同 token：exposure union 非项目全集（"披露一个缺口"与"完成全集"不能同时为真）、reward/训练/信息边界分类不封闭 | 量词/分类完备性 |
| v5-response | `WITHHOLD_STAGE1B_LARGE_SCALE_SURVEY_PENDING_NARROW_STRUCTURAL_REMEDIATION`：identity/occupancy **构念效度**不完整 + carry-forward 采样失衡 | 构念 |
| v6 | `WITHHOLD_STAGE1B_PENDING_NARROW_SEMANTIC_REMEDIATION`（2 GATE MAJOR）：身份派生未编码 RQ-SYS；**PDR 被事实性误编码致 3/11 占据数字失真**（"12/12 PASS 没挡住它"） | source-to-code 保真 |
| v7 | `WITHHOLD_STAGE1B`（3 Gate MAJOR）：RQ-SYS 未表达"信号实际控制权利"；**lineage 只是 presence check**；**v6 日期件被改写，审计层 append-only 失守** | 因果边/lineage/审计不可变 |
| v8 | `WITHHOLD_STAGE1B`（3 Gate MAJOR）：因果边未绑定**同一信号实例**（lifecycle 自相矛盾仍 11/11 PASS）；reconciliation 有"完整"之名无**证据完备性**之实（改 horizon 改 headline 仍全绿；不存在的页码也算 locator 已解析）；**WSL2 未实现 11/11 重放** | 信号实例/完备性/环境 |
| v9 | `WITHHOLD_STAGE1B_NARROW_REMEDIATION`——v8 MAJOR-1/-3 **CLOSED**、MAJOR-2 PARTIALLY_OPEN；三门收缩为一项窄整改 E1–E5 | 收敛 |

诚信裁决十轮恒定 `FFP NOT ESTABLISHED`，反复出现的是 `MATERIAL QRP / false-assurance RISK`——核心指控始终是**完成态措辞超过机器能力包络**，而非造假。

**终局与锚点。** 链在 v10 收口（v9 复审 §10-10 明写"窄整改完成后应立即签署，不得再延迟"；v10 是薄型重钉件：E1–E5 四个 FAIL 子门清零 + P1 四篇 carry-forward）。树上四件：`2026-07-15-system-first-research-proposal-v3-consolidated.md`（`ACCEPT AS WORKING THESIS`，唯一未被重开的科学纲领裁定）、`2026-07-19-…-v9-consolidated.md` + `…-v9-stage1a-doctoral-review.md`（三门→一门的收敛拐点）、`2026-07-19-…-v10-consolidated.md`、`2026-07-18-inherited-prior-exposure-union.md`。

**教训（全部在用）。** ①**失败形态逐层上移元规律**（动词→能力引用→量词→构念→lineage→字段关系→数据模型表达力/完备性/环境）；②**八防线**：oracle 等强审计、mutation testing（改能改变科学结论的字段后重生成，而非只跑作者预写的 mutation）、能力包络声明、量词扫描、单写 lineage（sidecar 链，coder≠adjudicator）、因果 edge 一等记录、信号实例正规化、完备合同（按派生 claim 定义必需证据集）；③**审计层不可变纪律**的事故现场就是 v7 MAJOR-3，修复＝恢复被审原字节 + 70 件日期件 blob 钉定 + 机器防线；④**阶段正典 v2（dated supersession）**：Stage-1B＝systematic mapping，全程禁研究模型含 smoke；方向性原型下沉 Stage-2A 复现先行；**以活动事实而非文档标题判定阶段**；⑤venue_tier 与 study_quality 拆分，tier 只作发现优先级/DFS 排序键，`T2_UNREVIEWED` 退役；⑥arXiv-only 诚实降名为 `arXiv-primary systematic mapping`；⑦**修发现空间比补几篇论文重要**；⑧agent-era 时新先验（2025+ 优先，窗口不砍、时代先验不进 study_quality）；⑨owner 未签时"创新点成立/不成立"两侧皆为时过早，评审代拟定位语一律标 `owner 未签`。

**被删（23）**
```
2026-07-15-system-first-research-proposal-v1.md
2026-07-15-system-first-research-proposal-v1-doctoral-adversarial-review.md
2026-07-15-system-first-research-proposal-v1-stage1a-recalibrated-review.md
2026-07-15-system-first-research-proposal-v2.md
2026-07-15-system-first-research-proposal-v2-stage1a-doctoral-review.md
2026-07-15-system-first-research-proposal-v3-stage1a-doctoral-review.md
2026-07-15-system-first-research-proposal-v3-stage1a-closeout-readiness-review.md
2026-07-16-c4-prep-owner-rulings-and-coding-depth-proposal.md
2026-07-16-gate-s1-rereview-application-stage1a-doctoral-review.md
2026-07-16-gate-s1-correction-4-prelaunch-doctoral-review.md
2026-07-16-gate-s1-p0r8-rereview-doctoral-review.md
2026-07-18-gate-s1-correction-4b-stage1a-doctoral-adversarial-review.md
2026-07-18-gate-s1-v5-response-stage1a-doctoral-rereview.md
2026-07-18-system-first-research-proposal-v4-survey-evidence.md
2026-07-18-system-first-research-proposal-v4-survey-evidence-doctoral-review.md
2026-07-18-system-first-research-proposal-v5-consolidated.md
2026-07-18-system-first-research-proposal-v5-consolidated-doctoral-review.md
2026-07-18-system-first-research-proposal-v6-consolidated.md
2026-07-18-system-first-research-proposal-v6-stage1a-doctoral-review.md
2026-07-18-system-first-research-proposal-v7-consolidated.md
2026-07-18-system-first-research-proposal-v7-stage1a-doctoral-review.md
2026-07-19-system-first-research-proposal-v8-consolidated.md
2026-07-19-system-first-research-proposal-v8-stage1a-doctoral-review.md
```

---

## H · stage1c-v2 precalibration 六代（RC2→RC2R1→RC2R2→RC2R3→R2→R2R1，07-24 → 07-25）

**尝试。** Stage-1C v2 要对 320-work union 做 agentic 实验映射，前置＝一次双盲双编码者校准：N=56（38 已签 overlay + 18 purposive sentinel），两名全新无 fork 隔离 model coder 各出 paper labels/cells/dataset edges/claim decisions/source locators，在**不可变 0.85 阈值**上算 agreement 后由 owner 裁决。六代 workbench 全是方法合同的**不可变后继**，每代只修上轮独立复审复现的有界缺陷：**RC2** 冻结共享接口 `observation → external state → signal/evaluator → decision right → action/tool → feedback → update/repair/stop`，`DIRECT_AGENTIC` 须至少 `DECIDE + ACT_OR_TOOL`，每 cell 只允许一个 `primary_intervention_axis`，双包隔离 + 递归 forbidden-key scanner，readiness 全 fail closed；**RC2R1** exact N=56/canonical-ID/provenance 绑定的 agreement intake、三类证据互斥；**RC2R2** frozen-package SHA-256 **作字面常量编译进 agreement v4**、receipt 记实收 8 件 artifact 的 bytes/hash；**RC2R3** 0.85 改**编译期常量**、receipt 由接收方**实际字节**重算、allowlist 改**类型化 key/index path**；**R2** coder 不再自报 `object_match_key`（改编译器派生）、未匹配对象进 union 分母、**论文可见 support 与 reviewer-only readiness 拆开**、新增 positive-support preflight；**R2R1** 对象 ID 强类型、复现支持拆十项事实四值枚举（十项全 `OBSERVED_IN_SOURCE` 才允许 `CLOSED_PAPER_SUPPORT`，`main/HEAD/latest` 不能冒充 pinned revision）、agreement 绑定**冻结的响应字节**。

**死因（两个独立死因叠加）。** 科学层：R1 实跑 `agreement_status: "FAIL"` — `Five of thirteen paper-level critical paths pass and eight fail`；`All nine object types have zero shared exact match keys`；两名 coder 都产出 **zero `dataset_edges` 与 zero `reproduction_evidence`**。preflight 判 `FAIL_WITH_BOUNDED_CONTRACT_DEFECTS` 并证明这**不是样本没有正例而是 codebook 缺陷**：TRACE 第 3 页明确供出两个 dataset-edge 正例而两 coder 都漏；`reproduction_evidence` 要求 `local_asset_state` 而包里显式扣留 repo 访问——**该字段对任一 coder 都不可观测**；强制 `closure_status=CLOSED` + 空 blocker 使该必填类"零可表达正例"。治理层：R2 方法包独立复审 `verdict: "WITHHOLD_WITH_BOUNDED_DEFECTS"`、`NO_CODER_DISTRIBUTION`；R2R1 修完后**在获得新的独立接受之前**，owner 把 Stage-1C 重定向为 literature-first 选题并终止非必要稳健性扩张。

**终局与锚点。** 收官处置逐字：`R1 remains FAIL with no adjudication; R2 and R2R1 remain immutable method artifacts. R2R1 was never independently accepted or distributed and is closed as RETIRED_WITHOUT_DISTRIBUTION_OR_INDEPENDENT_ACCEPTANCE, not as a valid calibration release. H5 remains non-load-bearing.` 树上锚点 `wiki/audit/system-first-stage1c-v2-calibration/INDEX.md`（六轮 append-only 交易 + 收官处置）；现行权威在 `wiki/Research-Objective.md` 与 `wiki/survey/current/tables/stage1c-common-rubric-comparison.md`。

**教训。** ①**agreement 之前先冻结原始字节**（先过 schema/semantic/identity/source-manifest 检查再算一致性；顺序反了就分不清"编码分歧"与"事后调和"）；②**零正例须先证明是样本零而非仪器零**——preflight 是其可执行形态；③**不可观测字段不得进入必填合同**（与信息边界 guard 同源、方向相反：这次是要求了 deployment 没有的信息）；④阈值须编译期常量、hash 须字面量、路径须类型化——凡"调用者可替换"的护栏都不是护栏；⑤**不可变后继模式**：RC2 绑 commit `74cf8e4b…`，后代不改写不迁移，只 append；⑥readiness fail closed，`primary_selection`/`fallback_selection` 全程 withheld；⑦一 cell 只允许一个 `primary_intervention_axis`——防组合收益被多轴重复归因；⑧**代价教训**：六代方法迭代（7 个 agreement contract、6 个 schema bundle）科学产出为零，literature-first 重定向本质是对"方法学完美主义吞噬研究预算"的裁决。

**被删目录（6，按战役目录整体计）**
```
wiki/survey/workbench/system-first-stage1c-v2-precalibration/
wiki/survey/workbench/system-first-stage1c-v2-precalibration-rc2r1/
wiki/survey/workbench/system-first-stage1c-v2-precalibration-rc2r2/
wiki/survey/workbench/system-first-stage1c-v2-precalibration-rc2r3/
wiki/survey/workbench/system-first-stage1c-v2-precalibration-r2/
wiki/survey/workbench/system-first-stage1c-v2-precalibration-r2r1/
```

---

## 跨链元结论

1. **没有一次死亡来自"实验做失败了"**：唯一真正的实验判决是链 A 的 M3/M5（一次真 kill、一次仪器 null），其余全部死于**记录、构念、协议与完成态语言**——这解释了为何正典把绝大部分纪律投在证据链而非实验设计上。
2. **评审制度两次具名自我纠偏因此有效**：07-15 重校准撤回四项"用论文标准审 Stage-1A"的判罚；07-14 重评撤回 scope 塌缩到 ASR 的要求。价值不在总对，在会撤回。
3. **每条链的终局是"锚点 + 禁令"而非"结论"**：树上 16 份保留件是判决书与冻结合同，被删的 71 份是推演过程。本 digest 让"为什么这样禁"不随字节离开工作面。
