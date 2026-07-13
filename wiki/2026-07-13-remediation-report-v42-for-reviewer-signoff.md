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

> **给协作审查者的阅读说明**：§3 现分两层——先是 20 行**索引表**（每条一行，供快速定位），随后是每条发现的**详情小节**（三段式 What / Why / How）。索引表判定与详情小节判定一致；索引给结论，详情给"问题是什么、为什么重要、修复机制与第三方核验配方"。凡首次出现的项目内部术语（estimand、K 池、SESOI、Holm、group manifest、force_supersede、ρ……）在详情小节首次使用处均附一句话释义——假定审查者精于方法学但不熟我方内部行话。

## 1. 本轮核验统计（我方对审查的独立复核）

按 reviewer-response protocol，先对审查的可核主张做逐条独立复核（Opus，vs 被审快照），再出本处置报告：

- **36 / 42 CONFIRMED · 6 PARTIAL · 0 REFUTED**（连续第三轮零驳回；审查引用文献全真、数学全对）。
- 6 项 PARTIAL **全部是范围收窄（narrowing），非推翻**。唯一触及**现行代码路径**的是 F-7（详见下方独立段）；其余五项均为 §1「可复核事实」层面的收窄，逐条一句话 What/Why 如下：

  1. **倒签存疑（chronology）**——What：审查发现根仓 proposal 首次进入 Git 的时间（2026-07-13 01:42:28 +08:00）晚于 frontmatter 标注日期（2026-07-12）。Why：审查者自陈"不足以证明倒签"，故收窄为**发布记录与文件日期不一致**这一记录纪律问题，处置为补 `created_at`/`released_at` 双时间戳（discrepancy register item 3），不构成任何倒签指控。
  2. **"143 passed"已被取代**——What：审查实测 `PYTHONPATH=src pytest -q` = 143 passed 属实。Why：该数字本身真实，只是被本轮 live **159 passed** 的运行取代，故为 narrowing 而非缺陷（旧数为过时快照，非错误）。
  3. **"checker 12/12 PASS"scope 免责本就诚实**——What：审查确认 12/12 PASS 的 scope 免责语是诚实的。Why：故收窄为"不是缺陷"，且已被 22/22 的 live run 取代（叙事版陈旧已如实登记，见 §5）。
  4. **"29,000/57,638 checkpoint"是构建中移动量**——What：审查所见 29,000/57,638 docs 为 embedding 构建进行中的 in-flight checkpoint。Why：它**证明真实构建在进行**、但**不证明 officialness 或完整性**，与 owner "全语料封存至 M2 选型落定"的裁决一致，故为收窄。
  5. **七项签字待定 + 未交付项系诚实自陈**——What：审查列出 v4.2 七项签字全待定、K-trajectory harness / live cross-modal smoke / corpus lock / REPRODUCE / 完整 SAP / operator-linked theory 未交付。Why：这些**本就写在 proposal 正文**，审查的作用是确认其真实而非揭露隐藏缺陷，故 verdict 为 PARTIAL(narrowing)，处置为维持为如实登记的门禁待办。

  **F-7 = latent（潜伏），非现行害（owner 续28 明裁）。数据流实证**：生产建库/评分路径**不向 `scrub` 传入 downstream `eval_golds`**，故 `scrub=True` 在确证/资格路径上**空转（no-op）**，**没有任何合法答案 span 被从开放语料里删除**，磁盘上无受损工件。F-7 描述的"把'答案存在是预期'实现成'答案必须被清除'"是一个**若未来调用方把 `eval_golds` 接进来才会引爆的雷**，不是当前发生的害。故降级为 PARTIAL，修复挂 **M1**（open-corpus 不 scrub 合法答案；per-item 注入 context 硬失败；`answer_presence_expected` 只描述性报告 overlap）。

## 2. Owner 续28 五项裁决（verbatim-faithful）

1. **M4 等级命名之争 → 推迟**："没必要纠结未来论文应该如何写"，当前聚焦数据集采样与工程基座夯实；等级标签依方法学须在 M4 **开火前**落定（非发表时），**具体选择推迟至 M3 签字**，此前不作 confirmatory 宣称。
2. **SESOI → 外部锚点设定**：Q-B 两支数值由 owner 从**外部锚点**（效用/文献惯例；Lakens 等价检验谱系 / MCID）设定，口径如实采用 **post-observation but externally justified** + prior-exposure register 公开全部先验效应观测（C-ASR-V2 电池等）。
3. **管理用词 → "就还好"**：不搞 DRAFT 重标运动，仅修事实陈旧处（如"4 errors"）。
4. **独立诚实审计 → 采纳，且 Stage-1 即重要**："稍微有一些学术欺诈和作弊，会导致后面几个月的工作被大量浪费掉"；形式 = P0 四登记册 + 修复后系统自检 + **详细整改报告呈外部 reviewer 盖章**。
5. **执行令**：先把本轮全部已识别问题修复完 + 系统性自检，**高质量锁定阶段性工作**，再出报告。另：全语料构建维持封存至 M2 选型落定（stage-gated artifact 纪律）；F-7 为潜伏雷非现行害。

## 3. 逐 finding 处置表

图例：**FIXED** = 结构性修复 + 机器可核证据；**FIXED\*** = 部分修复（框架/工件到位，剩余闭合挂门）；**DEFERRED@门** = 如实登记待决、挂明所属门（续29 SAP 冻结：estimand 重定义/新增确证原子一律推迟至 M3）；**OWNER-RULED** = owner 裁决保留/推迟（附引用）。

### 3.0 索引表（每条一行；finding-id 对应下方同名详情小节）

| # | 发现（一句话） | 处置 | 修复位置 / 门 | 核验证据（test / checker rule / register） |
|---|---|---|---|---|
| **F-1** | 主 estimand（相对降）与检验对象（固定绝对 margin）不一致、已知偏松 | DEFERRED@M3 | proposal §3.1（anti-conservative 已如实披露 + 敏感性比率 estimand） | 续29 SAP 冻结；`remediation_evidence.yaml:deferred_not_closed F-1`；owner 续28①聚焦 Stage-1 |
| **F-2** | SESOI 冻结不能称盲法/pre-observation | **FIXED** | proposal §3.2 / §9.3 / §14；改称 post-observation but externally justified，明文 disavow blindness | checker `BANNED-PREOBSERVATION-BLINDNESS`=PASS、`REQUIRED-POST-OBSERVATION-EXTERNALLY-JUSTIFIED`=PASS；`prior_exposure_registry.json`；owner 续28② |
| **F-3** | public deterministic evaluation 不能保留强 confirmatory 等级 | OWNER-RULED / DEFERRED@M3 | proposal §11 replayability-not-blindness；M4 等级推迟至 M3 | checker `BANNED-M4-CONFIRMATORY-GRADE`=PASS；owner 续28①（"此前不作 confirmatory 宣称"） |
| **F-4** | 单次 K-pool 条件推断遗漏生成随机性 | DEFERRED@M2→M3 | proposal §13.4 缺口表（generation-robust ρ：跨 seed 期望+下分位、外层 group/内层 replicate） | checker `REQUIRED-GENERATION-ROBUST-RHO`=PASS（tracked, not adopted）；续29 冻结 |
| **F-5** | 无 load-bearing RDU-vs-strongest 归因原子 | DEFERRED@M3（contested） | proposal §3.1（H_RDU_VS_STRONGEST 具名登记为 UNRESOLVED/contested，m=6 不变） | checker `REQUIRED-RDU-VS-STRONGEST-ATOM`=PASS（named/tracked）；续29 冻结不新增原子 |
| **F-6** | full-corpus 审计由 mode 字符串自证、无 upstream corpus lock | **FIXED\*** | `docs/corpus.lock.json`（content_hash+doc_count+upstream identity）+ `corpus_lock.py:verify_corpus_lock`（fail-closed）；57,638 全建 + datasets.lock 上游 revision/checksum pin 仍属 **M1 gap** | checker `REQUIRED-CORPUS-LOCK-EXISTS`=PASS；`test_corpus_lock.py`、`test_corpus_audit_axes.py`；proposal §6.4 L234 |
| **F-7** | `answer_presence_expected` 的 scrub 语义与开放语料任务相反 | OWNER-RULED latent / DEFERRED@M1 | 生产路径未传 `eval_golds`（scrub 空转，无数据受损）；修复挂 M1 | 续28 明裁 latent；数据流实证见 §1、§3-F-7；`deferred_not_closed F-7` |
| **F-8** | group-aware draw 三隔离漏洞 + "fixed seed equally tamper-evident"错述 | **FIXED\***（框架）/ DEFERRED@M2（结构门） | `deterministic_draw.py:14-15,34` 头部改写为 "replayable, not selection-blind"，具名撤回"equally tamper-evident"；100% coverage / singleton / force_supersede 三门挂 P2/M2 | checker `BANNED-EQUALLY-TAMPER-EVIDENT`=PASS；response v5 §3b/§3e 撤回 |
| **F-9** | 一次性 M4 状态机与 §13.3 M5 迭代自相矛盾 | DEFERRED@M3 | 机器可读状态机待落（M4_FAIL_FINAL 终局）；M5 文档限定语已加 | `deferred_not_closed F-9`；续29 冻结 |
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
| **P0** | P0_INTEGRITY_FREEZE 四登记册（续28④） | **DELIVERED / 内容实质充实；gate 如实 NOT_PASS** | 四册全部在盘 + 机采充实；config-selection 轨迹（M-6）与独立只读快照未齐 | `prior_exposure_registry.json:p0_gate_status` = **NOT_PASS（如实）** |

### 3.1 详情小节（What / Why / How）

以下按 **F-1..F-10 → M-1..M-9 → P0** 顺序，每条三段。**What（问题与处置）**说清审查发现与我方处置；**Why（为什么重要、为什么这样处置）**说清科学利害与处置选择理由；**How（机制与验证配方）**对 FIXED 项给出修复机制 + 第三方可复跑核验配方，对 DEFERRED 项给出所属门将交付什么、以何工件为证、今日追踪于何处。

#### F-1（DEFERRED@M3）

**What（问题与处置）**：审查发现主 estimand（estimand = 统计上要推断的那个总体真值/目标量）写作"相对错误率下降 10%"，但实际检验的是用冻结 dev 基线换算出的一个**固定绝对 margin**；proposal 自己也承认当确证基线错误率更高时，这个替代量对"10% 相对"主张偏松（anti-conservative，即系统性地更易通过）。处置：**推迟至 M3**，估计量操作化不在 Stage-1 落地。

**Why（为什么重要、为什么这样处置）**：一个已知偏松的 surrogate 挂在同一 headline 下，会让确证检验系统性地更容易"通过"，任何正结果的证据等级都被高估。选推迟而非现在重写，是因 owner 续29 明裁"关键是 10% 相对下降是我们的目标啊，我们为什么会把目标接入当前这个阶段？目标只是在学术调研过程中充当验收标准和门禁"——estimand 操作化属 M3 签字才冻结生效的确证机械，Stage-1 强行施工会重演 stage 错位。SAP 附录已整章改标"确证协议草案（M3 冻结生效，Stage-1 无操作效力）"。

**How（门将交付什么、以何为证、今日何处追踪）**：

- **M3 将交付（二选一）**：headline 改为"绝对错误率下降超预注册固定 margin"；或直接检验 aggregate paired 相对下降、联合重采样分子与分母、并为近零分母与 baseline drift 预注册处理。
- **关闭证据工件**：模拟覆盖率 + 机读 estimand + analysis-code golden test 三者一致。
- **今日追踪**：`remediation_evidence.yaml:deferred_not_closed F-1`（gate M3，status "SAP DRAFT 续29"）；proposal §3.1 的 anti-conservative 已如实披露。

#### F-2（FIXED）

**What（问题与处置）**：审查指出把 Q-B 的 SESOI（smallest effect size of interest，最小有意义效应量：预设的"小到不值得当真效应"的阈值）说成"在任何 selector dev 观测之前盲设/pre-observation"在时间上已不可能——项目已跑过 C-ASR-V2 selector 电池等 dev 结果。处置：**就地修复**——改称 "post-observation but externally justified"（观测后设定、但由外部锚点证成），并明文撤回盲法措辞。

**Why（为什么重要、为什么这样处置）**：盲法是核心诚信主张；若在已知效应值后仍自称盲设，等于用重命名抹掉已知信息、把较弱的设计伪装成较强。选此路径由 owner 续28②裁定——数值由 owner 从外部锚点（Lakens 等价检验谱系 / MCID 传统）设定、口径如实标 post-observation but externally justified、并以 prior-exposure register 公开**全部**先验效应观测。这是"较轻但诚实"的选项（详见 §6②）。

**How（机制 + 核验配方）**：

- **机制**：proposal §3.2/§9.3/§14 全部改标为 post-observation but externally justified 并明文 disavow blindness；`prior_exposure_registry.json` 机采公开 C-ASR-V2 selector 电池的 8 项观测与 oracle-headroom 实现率（~24% snr5 / ~42% clean）。
- **核验配方**：`python scripts/checks/v42_conformance.py` → **22/22 PASS**，其中 `BANNED-PREOBSERVATION-BLINDNESS`=PASS（2 处 pre-observation 命中全在撤回/否定语境）、`REQUIRED-POST-OBSERVATION-EXTERNALLY-JUSTIFIED`=PASS（proposal 内 20 处）。

#### F-3（OWNER-RULED / DEFERRED@M3）

**What（问题与处置）**：审查裁定 public deterministic evaluation（公开确定性评测：公开候选池 + 公开固定种子，任何人在配置冻结前即可算出最终 confirmatory item ID）不能保留强 confirmatory 等级——adaptive holdout 文献表明对已知 holdout 的自适应选择会过拟合 holdout 本身。处置：**M4 等级标签推迟至 M3 签字前落定**，此前不作任何 confirmatory 宣称；等级争议具名登记为 UNRESOLVED/contested。

**Why（为什么重要、为什么这样处置）**：若现在就贴强确证标签，会把"可重放"误当"选择盲"，一个尚不能排除自适应选择的评测被当作博士级确证证据。选推迟依 owner 续28①"没必要纠结未来论文应该如何写……具体选择推迟至 M3 签字，此前不作 confirmatory 宣称"——方法学要求等级须在开火前定，而"发表前届时再定"太晚，因为 M4 的科学解释在开火当时即已形成。

**How（门将交付什么 + 今日何处追踪）**：

- **M3 前二选一**：第三方冻结后一次性外部评分（升级为 blinded confirmatory）；或名称降为 `preregistered fixed-public-benchmark evaluation`、证据等级不高于强 development/quasi-confirmatory。
- **owner 裁定引用**：续28①"没必要纠结未来论文应该如何写……具体选择推迟至 M3 签字，此前不作 confirmatory 宣称"。
- **今日追踪**：proposal §11 已标 replayability-not-blindness、§9.8 把公开种子下的 selection-blindness 残余登记为 contested 敞口；checker `BANNED-M4-CONFIRMATORY-GRADE`=PASS（唯一 "blinded confirmatory" 命中在 deferral/future 语境）。

#### F-4（DEFERRED@M2→M3）

**What（问题与处置）**：审查指出 CI 只条件于**一次已实现的 K 池**（K 池 = 对同一输入采样生成的 K 个候选轨迹构成的候选池），把多池设为"可选"——但对一个靠随机采样产生候选的 selector，生成随机性是 estimand 的组成部分而非可选局限。处置：§13.4 新增 **generation-robust ρ**（ρ = selector 实现率，即 (R_selector − R_greedy)/(R_oracle − R_greedy)，度量 selector 兑现 oracle 头空的比例；generation-robust 指跨多个独立 K 池种子取期望与下分位，而非条件于单池）诚实缺口行，门禁@M2→M3，本版不操作化。

**Why（为什么重要、为什么这样处置）**：若只重采样 task item 而不重采样 generation，报出的"部署期 selector 优越"可能只是一次幸运抽样、跨种子不可复现。推迟是续29 SAP 冻结纪律（新增确证机械属 M3）；本版只登记 world-robust 的 landing point，不冒充已实现。

**How（门将交付什么、以何为证、今日何处追踪）**：

- **M2→M3 将交付**：每 item/group ≥3–5 个独立 K 池种子，外层重采样 group、内层重采样 generation replicate，同时报 conditional-on-pool 与 marginal-over-generation 两个 estimand。
- **关闭证据工件**：跨种子重采样的 ρ 期望 + 下分位表（预算不允许时结论严格限定该固定 pool，不主张部署期 selector 优越）。
- **今日追踪**：checker `REQUIRED-GENERATION-ROBUST-RHO`=PASS（proposal 1 处，tracked, not adopted）；`remediation_evidence.yaml:entries` 的 F-4 条目（`disposition: deferred_tracked`——因其带活体 checker 规则盯守，记录于 entries 块而非 deferred_not_closed 块；gate M2→M3，续29 冻结）。

#### F-5（DEFERRED@M3，contested）

**What（问题与处置）**：审查发现六个 primary 确证原子里没有 RDU-vs-strongest 的承载归因原子（RDU = 本项目的 frozen-core 知识前端；strongest baseline = long-context 全塞 / 自家 ASR 文本 RAG / frozen retriever 中的最强者）——系统可能只因"多给了知识"就击败裸核心，无法证明收益来自 RDU 设计。处置：`H_RDU_VS_STRONGEST` **具名注册为显式 contested/deferred**（非静默降为散文/丢弃），m=6 primary family 依续29 冻结不变，promotion 决定推迟 M3。

**Why（为什么重要、为什么这样处置）**：缺此原子，headline 的因果归因是空的——WavRAG/PlanRAG/RECAST 已在做音频 RAG，"冻结模型 + RAG + 多样本选择"本身不够博士级新颖。选"具名登记而非现在加原子"是续29 冻结（不新增确证原子）+ owner Stage-1 聚焦：具名保证它不被遗忘，冻结保证不越 stage 施工。

**How（门将交付什么、今日何处追踪）**：

- **M3 将交付**：把 H_RDU_VS_STRONGEST 提升为 primary 或置换弱原子；strongest baseline 在 dev 按预注册规则从 long-context / own-ASR text-RAG / frozen retriever 中选出，RDU 须在预算/上下文长度可比条件下越 SESOI。
- **今日追踪**：checker `REQUIRED-RDU-VS-STRONGEST-ATOM`=PASS（named/tracked，4 处，m=6 未变）；proposal §3.1 的 UNRESOLVED 登记 + §13.4 M3 缺口行；`remediation_evidence.yaml:entries` 的 F-5 条目（`disposition: deferred_tracked`，同 F-4 记录于 entries 块）。

#### F-6（FIXED\*）

**What（问题与处置）**：审查发现全语料审计此前由 `query_independent_corpus = PASS iff corpus_mode=="full"` 这一**模式字符串**自证——一个不完整/替换过/错误来源的 `corpus.jsonl` 仍可被标成 query-independent（查询无关）。处置：**部分就地修复**——新增 `docs/corpus.lock.json`（上游语料 identity）+ W1 `corpus_lock.py:verify_corpus_lock` 的 fail-closed（失败即拒绝）验证契约 + 审计轴测试；余"57,638 全建 + `datasets.lock.json` 上游 revision/checksum pin"为如实登记的 **M1 gap**。

**Why（为什么重要、为什么这样处置）**：若审计只信任调用方布尔值/mode 字符串，一个被掉包或截断的语料文件会静默通过"查询无关"，任何检索结果都建立在**未经核验的对象**上——这正是本项目"对象错误"假增益史的谱系。选"证据锁 + fail-closed"而非"更强的 mode 字符串"，因为唯有从真实字节重算的证据才能证明语料官方性；全建封存至 M2 选型是 owner 的 stage-gated-artifact 纪律（续28），非回避。

**How（机制 + 核验配方）**：

- **机制（`corpus_lock` 四检全匹配才通过，`verify_corpus_lock` fail-closed）**：(1) archive 成员**原始字节** sha256；(2) **有序 doc-ID hash**（对重排敏感——即便 id 全在也能抓到 reshuffle）；(3) NFKC 归一化 title+text 的**内容 hash**（抓静默改字）；(4) `doc_count` 同时对 lock 文件与硬编码 `EXPECTED_DOC_COUNT["fiqa"]=57638` **双锚**（手改 lock 文件也放松不了此不变量）。
- **写前硬断言**：`build_squtr_corpus_source` 在 persist 前对 doc_count 硬断言，不符即 `raise ValueError`、**写盘为空**（"incomplete checkpoint must never persist as a full source"）；`query_independent_corpus` 轴现从 `corpus_lock_verification.verified` 取值，不再从 `corpus_mode` 字符串取值。
- **核验配方①**：`PYTHONPATH=src pytest scripts/knowledge/test_corpus_lock.py -q` → **1 passed**（依赖无数据根，9 个内部 case：内容突变→`normalized_content_hash` 失配；重排→`ordered_doc_id_hash` 失配而 `doc_count` 仍匹配；57637/57639→引 `EXPECTED_DOC_COUNT` 锚失败；`raise_on_mismatch=True` 实抛 `CorpusLockError`；`generate` 遇错写 NOTHING）。
- **核验配方②**：`PYTHONPATH=src pytest scripts/knowledge/test_corpus_audit_axes.py -q`（numpy venv）→ **1 passed**（改一字节 corpus → `query_independent_corpus`=FAIL、`corpus_lock_verification.verified`=False）。
- **核验配方③**：`python scripts/checks/v42_conformance.py` → `REQUIRED-CORPUS-LOCK-EXISTS`=PASS。
- **仍属 M1 gap**：57,638 全建 + 上游 revision/公开 checksum pin 进 `datasets.lock.json`（proposal §13.4 明列）。

#### F-7（OWNER-RULED latent / DEFERRED@M1）

**What（问题与处置）**：审查发现 `answer_presence_expected` 轴（"答案是否出现"轴）的 scrub 语义与开放语料任务相反——builder 曾把 downstream `eval_golds`（评测标准答案）交给 `scrub=True`，并以 scrub 后 CLEAN 判该轴 PASS，即"删除合法证据、把'答案存在是预期'实现成'答案必须被清除'"。处置：owner 裁定为**潜伏雷非现行害**（生产路径未传 `eval_golds`、scrub 空转、磁盘无受损工件）；纠正机制已在 M1 落地。

**Why（为什么重要、为什么这样处置）**：若未来调用方把 `eval_golds` 接进来，合法答案 span 会被从开放语料删除、静默改变研究任务——这是必须修的轴设计错误。判 latent 是数据流实证：生产建库/评分路径不向 scrub 传 `eval_golds`，`scrub=True` 在确证/资格路径上空转、无任何合法答案 span 被删、磁盘无受损工件，与审查 §5.1"未见凭空编造 confirmatory result"一致（owner 续28 明裁）。

**How（机制 + 核验配方；今日 latent）**：

- **机制（M1 已落地，Decision-Log 续31）**：open-corpus 的 `build_squtr_corpus_source` 恒 `scrub=False`/`enforce_leakage_gate=False`；`answer_presence_expected` 改为**纯描述**（NOT_EVALUATED/PRESENT/ABSENT，除 `n_golds=0→NOT_EVALUATED` 外永不 gate overall）；新增第六轴 `no_injected_gold_context` 作为**唯一**能因 per-item 注入 gold 而硬 FAIL 的轴。
- **核验配方**：`PYTHONPATH=src pytest scripts/knowledge/test_corpus_audit_axes.py -q`（numpy venv）→ **1 passed**——含合法 answer span 正向 golden（持久化 value 未被 scrub、gold 文本 verbatim 仍在）+ per-item 注入负向 golden（`no_injected_gold_context`=FAIL，压过其余全清轴）。
- **今日追踪**：`deferred_not_closed F-7`（gate M1，status latent："生产路径未传 eval_golds、无数据受损，fix tracked"）。

#### F-8（FIXED\* 框架 / DEFERRED@M2 结构门）

**What（问题与处置）**：审查发现 group-aware 确定性抽签有三条隔离漏洞——(1) eligibility/exploration 缺 group manifest（组清单：把同说话人/会话样本归为一组、以防跨 split 泄漏的映射表）只 warning、(2) manifest 缺 item 时静默退化为 `gid=iid` 单例、(3) confirmatory 只要 exclusion path 非空即过门，且 `force_supersede`（强制顶替旧抽签文件的开关）仍可用——外加代码头"fixed seed equally tamper-evident"错述。处置：**就地修复框架**（头改"replayable, not selection-blind"、具名撤回"equally tamper-evident"，三隔离门代码已落 W1）；跨 split 结构门余项挂 P2/M2。

**Why（为什么重要、为什么这样处置）**：若不修，恶意或疏忽的抽签能让同 speaker 跨 split、缺组 ID 静默降级、confirmatory 被覆盖重抽——都能在**不伪造任何数据**的情况下取得有利 final IDs。"equally tamper-evident"错述尤其危险：它把一个可编辑的本地 append-only JSONL 说成与 beacon+co-signer+burn 仪式**同等防篡改**，夸大证据等级。就地修复 + 具名撤回是因这是事实性错误必须立即纠正；完整跨 split group-disjoint proof 属 P2/M2 抽样门。

**How（机制 + 核验配方）**：

- **措辞修复**：`deterministic_draw.py:14-15,34` 头改"replayable, not selection-blind"，并**具名撤回**"equally tamper-evident"（点名为 prior/retracted framing）。
- **三隔离门（代码已落 W1）**：`_validate_group_manifest_coverage` 对全部三种 draw type 硬要求 100% 组覆盖，缺/空/无效组键即 `ValueError`（移除 `gid=iid` 静默单例）；confirmatory 机验其 `exclusion_manifest_paths` 覆盖 exposure_registry 的**全并集**，且 `force_supersede` 对 confirmatory 恒 `ValueError`（create-once）；每 manifest 记 `group_manifest_hash`/`exclusion_definition_hash`/`pool_hash`/`code_sha`。
- **核验配方**：`python scripts/checks/v42_conformance.py` → `BANNED-EQUALLY-TAMPER-EVIDENT`=PASS（4 处命中全在撤回语境）；`PYTHONPATH=src pytest scripts/baselines/test_deterministic_draw.py -q`（三 draw 两两 disjoint + 100% coverage 门 end-to-end 验证）。
- **今日追踪**：response v5 §3b/§3e 撤回 tamper-evident；跨 split group-disjoint proof 结构门余项挂 P2/M2。

#### F-9（DEFERRED@M3）

**What（问题与处置）**：审查发现一次性 M4 状态机在正文内部自相矛盾——§9.5/§13.2/DAG 写 M4 fail 后终局，但 §13.3 的 M5 又写"不达标→development 迭代或 owner 复盘"，给"失败后迭代"留了文本授权口。处置：**门禁@M3**（机读状态机——`M4_FAIL_FINAL` 为吸收态——待落）；文档侧 M5 已加限定语。

**Why（为什么重要、为什么这样处置）**：若留此口，一次 M4 失败可被"再迭代一版"绕过，等于对同一 holdout 反复开火、破坏单一最终确证版本制的 Type-I 控制。推迟机读状态机是续29 SAP 冻结（机械化属 M3）；本版先用文档限定语堵口，是 stage-appropriate 的最小诚实处置。

**How（门将交付什么、今日何处追踪）**：

- **M3 将交付**：机读 state machine（`states`/`allowed_transitions`，`M4_FAIL_FINAL` 为无出边吸收态）；任何新数据复制必须是**新 program ID**、不复用原 family/seed/confirmatory 标签。
- **今日追踪**：`deferred_not_closed F-9`（gate M3，续29 冻结）；`append_only_erratum_for_v42.md` §2.5 的 M5 文档限定语已加（M4 FAIL 终局堵口）。

#### F-10（DEFERRED@M2 / 理论轨）

**What（问题与处置）**：审查确认理论"正确命名"有进步（§10.2 已诚实标 `U(τ*)−U(τ̂)≤2ε` 是 generic argmax-mismatch 而非收敛），但仍无博士级承载定理——真正第二定理依赖 finite-sample `ε_n→0`，而 n 的定义、`Û_n` 如何更新、对 adaptive candidate set 的 uniform high-probability bound、分布漂移下 ε 如何保持、Python↔Lean 逐例一致均未定义。处置：**门禁@M2/理论轨**；#27 同对象绑定待闭合。

**Why（为什么重要、为什么这样处置）**：若只假设 `ε_n→0` 再推 regret→0，等于把结论写进前提——这正是 2026-07-02 review 杀掉旧理论的"tautology-where-proven"病；BoN（best-of-N）文献真正难处在 imperfect reward 的 coverage/tail/over-optimization 约束，而非二行 argmax bound。推迟是因承载定理须与 Python selector **同对象**（dual-track），属理论轨的实质工作，不能在 Stage-1 用散文补。

**How（门将交付什么、今日何处追踪）**：

- **理论轨将交付**：证明 finite-sample `ε(n,δ,complexity)` 再推 regret bound；先证 UNCONSTRAINED 过程不收敛、再证 CONSTRAINED 过程收敛；实现与之同对象的 pessimistic/uncertainty-set selector，并给 Python-Lean golden（含 ties/early-stop/K-cap/abstention）。
- **fallback**：若只剩 generic 2ε lemma，则明确降级为验证基建、删"理论贡献"。
- **今日追踪**：`deferred_not_closed F-10`（baseline argmax-mismatch lemma only）；§10.2 已诚实标注非收敛；#27 同对象绑定待闭合。

#### M-1（DEFERRED@M3）

**What（问题与处置）**：审查指出两个 no-harm 原子（non-inferiority 下受益与平凡无害都可通过）不是正向复制——"1 正效应 focus + 2 no-harm"不能称多数据集效果复制。处置：**门禁@M3**，headline 如实限定为单焦点集。

**Why（为什么重要、为什么这样处置）**：若把 no-harm 当复制，会把"在别处没变坏"包装成"在别处也变好"、虚构泛化。推迟是续29 冻结不新增/重定义 primary 原子；本版只把 headline scoped 到单 focus 保持诚实。

**How（门将交付什么、今日何处追踪）**：

- **M3 将交付**：至少一个预定外部数据集通过正向 SESOI；或 headline 明确改为单数据集 case study。
- **今日追踪**：proposal §3.1 已把头条如实限定单焦点集；`deferred_not_closed M-1`（gate M3）。

#### M-2（DEFERRED@M3）

**What（问题与处置）**：审查指出 Q-B 只有单数据集不能支撑一般 TFRL（training-free RL）身份价值——算法身份可由定义成立，但"selector 有科学价值"不能靠一个 responder focus。处置：**门禁@M3**，身份主张显式限定单焦点、跨集泛化推迟。

**Why（为什么重要、为什么这样处置）**：若用单集撑一般价值，任何跨任务失效都被掩盖。推迟是续29 冻结 + owner Stage-1 聚焦；本版据实说"在 `<FOCUS>` 上观测到 selector effect"，不外推。

**How（门将交付什么、今日何处追踪）**：

- **M3 将交付**：一个不同任务族或不同核心的正向 equal-K 复制。
- **今日追踪**：proposal §3.2 已把身份主张显式限定单焦点、跨集泛化推迟；`deferred_not_closed M-2`（gate M3）。

#### M-3（DEFERRED@M3）

**What（问题与处置）**：审查指出 random 对照应用**条件期望**——给定同一 K 池，random-pick 的条件期望真效用就是 K 个候选 U 的均值（pool-mean），不应再抽一次幸运 random index 引入无意义 Monte-Carlo 方差。处置：**门禁@M3**，§13.4 缺口行改比 selector U vs pool-mean，实际抽签仅留部署模拟；m=6 不变。

**Why（为什么重要、为什么这样处置）**：若用一次 seeded random pick 当对照，comparator 自带随机噪声、削弱统计功效，且可被幸运抽签利用。推迟是续29 SAP 冻结；本版登记正确 estimand 而不操作化。

**How（门将交付什么、今日何处追踪）**：

- **M3 将交付**：primary equal-budget 对照 = selector U vs pool 均值 U 的条件期望；实际 seeded 抽签仅保留为部署模拟。
- **今日追踪**：checker `REQUIRED-POOL-MEAN-COMPARATOR`=PASS（1 处，tracked, not adopted，m=6 不变）；proposal §13.4 缺口行。

#### M-4（DEFERRED@M2）

**What（问题与处置）**：审查指出同权重异 prompt 不是 weight-independent 跨源独立——self-consistent error 文献显示同一模型会稳定重复相同错误，改 prompt 不能预设为独立证据。处置：**门禁@M2**，proposal §4.2 改称 context-differentiated（上下文差异化），收益须为 **MEASURED δ_corr**（误差去相关度：两套系统错误间可去相关的量）。

**Why（为什么重要、为什么这样处置）**：若把同模型异 prompt 当独立验证器，两套系统的共同盲点会被误当"交叉确认"、selector 收益是假的。推迟到 M2 是因 δ_corr 须实测（error-correlation / 条件互信息）后才能决定该信号是否纳入 selector——这是 omni-verifier 去相关约束谱系的落点，属方案验证阶段。

**How（门将交付什么、今日何处追踪）**：

- **M2 将交付**：预注册 error-correlation / 条件互信息（CMI）阈值；达不到阈值则删该信号或换独立模型。
- **今日追踪**：`deferred_not_closed M-4`（gate M2，selector 纳入前须 MEASURED δ_corr）；proposal §4.2 L157 已把"跨源"改称 context-differentiated。

#### M-5（DEFERRED@M2）

**What（问题与处置）**：审查指出小簇尾部推断未证成——effective clusters 可能仅 20–45，却要估计 Holm（Holm-Bonferroni 多重比较校正：按序调整显著性阈值以控制族错误率）后约 0.008 的尾部；"BCa 或 bootstrap-t 二选一"未经设计特定模拟。处置：**门禁@M2**，BCa / studentized-t vs wild-cluster vs randomization 按 simulation 的 Type-I/coverage/power 选。

**Why（为什么重要、为什么这样处置）**：若凭方法名而非模拟选推断法，少簇 + 非均衡 group + 离散 endpoint 下标准方法可能过度拒绝、尾部 p 值不可信、Type-I 失控。推迟到 M2 是因选择须靠 design-specific simulation（实际 cluster size / ICC〔组内相关系数〕/ missingness / seed variance），属方案验证阶段工作。

**How（门将交付什么、今日何处追踪）**：

- **M2 将交付**：至少比较 studentized cluster bootstrap / wild cluster bootstrap / cluster-level randomization（其 exchangeability 条件成立时），以 Type-I / coverage / power 定稿，而非凭方法名选。
- **今日追踪**：`deferred_not_closed M-5`（gate M2，choose via simulation）。

#### M-6（DEFERRED@M2，现 INCOMPLETE）

**What（问题与处置）**：审查指出配置多重性账本不全——modality×form×delivery×selector weights×K×threshold×embedder×prompts 的 dev winner 被称 `best_frozen_rdu`，但 `experiment_attempt_registry.jsonl` 现为**浅扫描**，未捕获完整 config-selection 轨迹（所有尝试过的配置 + 放弃理由）。处置：**门禁@M2（现 INCOMPLETE）**——已增行级 status/claim_id/inferred 标注，完整轨迹仍 OUTSTANDING。

**Why（为什么重要、为什么这样处置）**：若只保存赢家配置，选择性通道无法被审计——public IDs 又破坏了独立 test 的保护，等于给"择优后报告"开后门。判 INCOMPLETE 而非 PASS 是诚实审计要求：未持久化到 `_repro/` 的废弃扫描不能自动回溯。

**How（门将交付什么、今日何处追踪）**：

- **M2 将交付**：完整 search space（modality×form×delivery×weights×K×threshold×embedder×prompts）+ 所有尝试结果 + selection rule，避免只保存赢家。
- **今日已做**：`experiment_attempt_registry.jsonl` 574 行已增行级 status/claim_id/inferred 标注。
- **今日追踪（仍 OUTSTANDING）**：`deferred_not_closed M-6`（gate M2）；`prior_exposure_registry.json:p0_gate_status`（unmet：未持久化到 `_repro/` 的废弃扫描不可全量回溯）；`append_only_erratum_for_v42.md` M-6 行（入 `manual_completion_todo[0]`）。

#### M-7（DEFERRED@M2）

**What（问题与处置）**：审查指出 q2q（query-to-query，用文档回生成伪查询的桥接）有预训练回生盲点——即使 build script 不读 query 文件，生成 q2q 的公开预训练模型可能训练中见过 benchmark queries 并从文档回生高度相似问题；污染可跨表面转换/语言边界，exact path audit 不够。处置：**门禁@M2**，proposal §6.4 规则冻结后做 exact/fuzzy/semantic query-overlap 审计（描述性交付）。

**Why（为什么重要、为什么这样处置）**：若不做语义级污染审计，form-bridge 的"收益"可能来自 benchmark question 回生而非真实检索能力，是隐蔽的数据污染。推迟到 M2 是因审计须在规则冻结后做、报告分布而非事后按结果调阈值；q2q 与 raw-doc/q2a 须同时保留对照。

**How（门将交付什么、今日何处追踪）**：

- **M2 将交付**：规则冻结后做 exact/fuzzy/semantic query-overlap 审计，报告分布而非事后按结果调阈值；q2q 与 raw-doc/q2a 同时保留对照。
- **今日追踪**：`deferred_not_closed M-7`（gate M2）；proposal §6.4 L238 已登记冻结后描述性审计交付。

#### M-8（FIXED，机制）

**What（问题与处置）**：审查发现提交状态与发布文字不事务一致——W1 `159b525` 已使标准测试 143 passed，但同次发布仍写"现有 4 errors"；同时 commit subject 写"converged (2 rounds, 0 residual)"而同一 proposal 明列 K-harness/live smoke/lock/REPRODUCE 未完成。处置：**就地修复机制**——`build_release_manifest.py` 记 live SHA+dirty+pytest+checker verdict（永不复制旧报告），§13.4 更新为 159 passed/0 errors 并标旧快照陈旧。

**Why（为什么重要、为什么这样处置）**：若发布文字与仓库真状态脱钩，"converged/locked/0 residual"会被误读为 M1 已闭合——即便这更像发布快照协调失败而非造假，也足以否决"lock/converged"。选机械化 release manifest 是因唯有从 SHA fresh 重建的状态表才能防快照再度失真。

**How（机制 + 核验配方）**：

- **机制**：`build_release_manifest.py` 记 umbrella+W1 的 SHA/dirty、live `standard_test_entry`（159 passed / returncode 0）、live checker verdict（22 规则 / 0 failed）——**永不复制旧报告**，故快照失真可机械发现；`discrepancy_register.md` item 1&2 记陈旧"4 errors"与"converged/0 residual"措辞范围。
- **核验配方**：`python scripts/checks/v42_conformance.py` → `BANNED-STALE-FOUR-ERRORS`=PASS（唯一"4 errors"命中在 stale-flagged 语境）；核对 `release_manifest.json:standard_test_entry` = 159 passed / returncode 0。

#### M-9（ADDRESSED）

**What（问题与处置）**：审查指出 conformance checker 通过 ≠ proposal 自洽——12 条规则未检查 F-1..F-10 任何核心问题，"12/12 PASS"不该出现在无相邻限定语的管理汇报中。处置：**ADDRESSED**——checker 加 10 条新规则（12→22：8 条 remediation semantic + 2 条 file-existence），报告全程 scope 免责、人工/独立审查与机械 lint 分栏。

**Why（为什么重要、为什么这样处置）**：若把"绿色 checker"当科学有效性，会把一个只验文档自洽 + 工件存在的机械 lint 误当博士级确证——这正是审查警告的最易被滥用通道。选"加语义规则 + 永久 scope 免责分栏"而非"宣称 checker 已覆盖科学性"，是把 checker 严格限定在它能证明的范围内。

**How（机制 + 核验配方）**：

- **新增规则（12→22）**：8 条 semantic——banned〔pre-observation-blindness / equally-tamper-evident / stale-4-errors / M4-confirmatory-grade〕+ required〔post-observation-externally-justified / generation-robust-rho / pool-mean-comparator / H_RDU_VS_STRONGEST〕；2 条 `file_exists`〔corpus.lock / 四登记册〕。
- **核验配方**：`python scripts/checks/v42_conformance.py` → **22/22 PASS**；`v42-conformance-output.json:self_scope` 明记 "certifies package self-consistency only, not scientific validity"。
- **今日追踪**：`remediation_evidence.yaml:scope_disclaimer` + checker meta `self_scope`；报告全程人工/独立审查与机械 lint 分栏（§5、§7 范围声明）。

#### P0（DELIVERED / 内容实质充实；gate 如实 NOT_PASS）

**What（问题与处置）**：审查 §6 `P0_INTEGRITY_FREEZE` 要求四登记册（prior_exposure / experiment_attempt / discrepancy / release_manifest）+ 把 v4.2 标 DRAFT/NOT LOCKED + 独立评审者收到只读快照。处置：**四册全部在盘且机采实质充实**，但 **gate 如实 NOT_PASS**——绝不因 checker 的 existence-PASS 而报 P0 已闭合。

**Why（为什么重要、为什么这样处置）**：若把 P0 报 PASS，就等于用 existence-PASS 冒充内容闭合——owner 续28④"稍微有一些学术欺诈和作弊，会导致后面几个月的工作被大量浪费掉"，故独立诚实审计在 Stage-1 即重要，P0 必须按真状态报。选如实 NOT_PASS 是因 config-selection 轨迹（M-6）仅部分可自盘回溯、"独立评审者收到只读快照"是本文件无法自证的流程步骤。

**How（已充实内容 + 未闭合项 + 何处追踪）**：

- **已机采充实**：prior_exposure 明示 C-ASR-V2 selector 效应量（oracle-headroom 实现率 ~24% snr5 / ~42% clean，MBR/random/length 结果）；**17** 个提示模板；K1-K11 指标族自 **464** 工件（0 读错）；**5** 个 dev 暴露事件（含 LOCKED_HOLDOUT 11.20% overlap 永久降级）；experiment_attempt **574** 行带 status/claim_id/inferred 逐行标注。
- **未闭合项（gate 如实 NOT_PASS）**：`prior_exposure_registry.json:p0_gate_status` = **NOT_PASS**（`pass_conditions_met=false`）；unmet = config-selection 轨迹（M-6，入 `manual_completion_todo[0]`）+ "独立评审者收到只读快照"（**本报告送达审查者即满足该流程步**）。
- **核验**：checker `REQUIRED-FOUR-INTEGRITY-REGISTERS`=PASS——**仅验四册存在，绝不断言内容完整**。

## 4. 我们**没有**做什么，以及为什么

- **未把 v4.2 重写成 v4.3**。owner 续28③"就还好"——不搞 DRAFT 重标运动；且 Stage-1 聚焦问题定义与数据集/工程基座，SAP 设计迭代（estimand 重定义、新增确证原子）**一律冻结推迟至 M3**（续29）。故本轮**不新增 primary 原子、m=6 不变**，只落地"修事实陈旧处 + F-2 SESOI 改称 + 双时间戳 + 机器可核工件"这批**非 SAP** 修复。曾一度半应用的 SAP 前向编辑（F-1/F-4/F-5/M-3/M-4/M-7/PF3）已**回退**并改登记为缺口表待决项。**Why**：续29 明裁 estimand 操作化属 M3 才冻结生效的确证机械，Stage-1 强行施工会把 proposal 逼向预注册级、重演 stage 错位（同 stage-gated-artifact 教训谱系）；只落地非 SAP 修复才是 stage-appropriate 的诚实选择。
- **未完成全语料构建**。全语料（FiQA 57,638 docs）建库**维持封存**至 M2 embedder 选型落定（stage-gated artifact 纪律，续28）；上游 revision + 公开 checksum pin 进 `datasets.lock.json` 是明列的 **M1 gap**。当前只交付 `corpus.lock.json` 的**验证契约**（fail-closed），不冒充"已建成官方全语料"。**Why**：选型未定就全建等于把一个待作废的工件当"官方全语料"报——封存与只交付验证契约，是让工件与其 stage 匹配、避免既成事实倒逼选型。
- **未确定 M4 证据等级**。按 owner 续28①**推迟至 M3 签字前**落定（方法学要求：等级须在开火前定、非发表时定）；在此之前**不作 confirmatory 宣称**。这是一条**开火前承诺（before-fire commitment）**，非事后择定。**Why**：等级一旦在"看见结果之后"再定，就为"按结果挑等级"开了口——把承诺锁在开火前，才能让等级选择独立于结果、堵住这条选择性通道。
- **P0 未标 PASS**。四登记册仅 existence 满足、内容未齐（见 §3 P0 详情）；本报告**如实呈 P0 为 INCOMPLETE**，绝不因 checker 的 existence-PASS 而报 P0 已闭合。**Why**：独立诚实审计（续28④）的全部价值在于按真状态报——把 existence-PASS 说成内容闭合，正是它要防的那类自我美化；如实 NOT_PASS 才让待办（M-6 轨迹 + 独立快照）保持可见、可被追责。

## 5. 系统性自检结果（续28-⑤）

- **一致性 checker（live）**：`scripts/checks/v42_conformance.py` vs `docs/checks/v42-rules.yaml` → **22 / 22 PASS，0 failed**，verdict = *DOCUMENT PACKAGE READY FOR EXTERNAL REVIEW*（`v42-conformance-output.json`，含 12 条原规则 + 10 条本轮新增：8 条 remediation semantic〔banned/required phrase〕+ 2 条 file-existence〔`REQUIRED-CORPUS-LOCK-EXISTS`、`REQUIRED-FOUR-INTEGRITY-REGISTERS`〕）。**这条检查覆盖什么**：它验证文档包**自洽**（禁用词只出现在撤回语境、必需短语在场、原子数与 m= 一致、被声明存在的工件确在盘）。**它不能证明什么**：不证明科学有效性、语料官方性、抽样隔离、统计充分性或理论——凡 F-1/F-9/F-10/M-1/M-2/M-4/M-5/M-6/M-7 的实质均仍 DEFERRED/CONTESTED、tracked-not-closed。注：`docs/checks/v42-conformance-report.md` 正文仍记 12/12，是**前一规则集**的 run，被 22 条 live JSON 取代；该 12/12-vs-22/22 不一致**已登记在案**——见 `discrepancy_register.md` 的"2026-07-13 追加（#39 收尾，协调者）"一节（该册主体 generated_at 2026-07-13T03:25:43Z，追加节为其后的 append-only 补录），并同时在叙事版顶部加注"以机读 JSON 为权威"；叙事版完整重写排入下一发布周期。
- **标准测试入口（live）**：`PYTHONPATH=src pytest -q`（W1）→ **159 passed, 0 failed, 0 errors, 3 warnings**（returncode 0；`release_manifest.json:standard_test_entry`）。**这条检查覆盖什么**：它证明代码层测试套件在部署环境下全绿、取代审查所见 143 与更早"4 errors"。**它不能证明什么**：不证明任何科学主张——绿测只说代码按其自身契约运行，不说 selector/RDU 有效。诚实注：需 `SPEECHRL_DATA_DIR`（如部署）；缺失时 4 个数据依赖测试以显式 `RuntimeError` 失败（环境非代码）。
- **P0 登记册已建**：`prior_exposure_registry.json`（扫 574 件 `_repro` 工件）、`experiment_attempt_registry.jsonl`（574 行）、`discrepancy_register.md`、`release_manifest.json`（`build_registers.py` / `build_release_manifest.py` 播种）。**这条检查覆盖什么**：它把"迄今 OBSERVED 的一切"（数据集/提示模板/指标族/效应量/dev 暴露事件）机采落盘，供第三方查阅。**它不能证明什么**：不证明 P0 已闭合——内容完整度如 §3 P0 详情如实标注，gate 权威状态 = `p0_gate_status` NOT_PASS（M-9 scope 纪律：机械登记≠独立监督）。
- **总口径**：**checker 只验文档包自洽 + 工件存在，certifies nothing about 科学有效性**；绿色 checker、159 passed、22/22 PASS 均**不得**被读作 M1 闭合或确证就绪（全程分栏，见 §7 范围声明）。

## 6. 三处对审查者的敬意商榷（如实提出，非抵赖）

1. **F-7 应为 latent 而非现行害**。数据流实证（§1）：生产路径未向 scrub 传 `eval_golds`，scrub 空转、零合法答案被删、磁盘无受损工件。我们**接受该轴设计错误必须修**（机制已在 M1 落地），但请求把它记为**潜伏雷（若未来接线才引爆）**而非"当前已改变研究任务"的现行害——这与审查 §5.1 "未见凭空编造的 confirmatory result"一致。
2. **E2（SESOI）采较轻但诚实的选项（owner 裁决）**。审查建议由未接触效应值的独立统计人员盲设 SESOI、或改用一套全新数据确证；owner 续28②采**较轻**路径：数值由 owner 从**外部锚点**（Lakens 等价检验 / MCID 传统）设定、口径如实标 **post-observation but externally justified**、并以 prior-exposure register 公开**全部**先验效应观测。我们**如实承认这比盲法轻**、公开种子下的 selection-blindness 残余仍是 contested 敞口（§9.8/§11），不冒充已消解。
3. **独立性以"外审盖章 + 机器可核登记册"落地，而非人员隔离**。审查建议独立 custodian / 两名非开发者复跑 / 第三方冻结后评分；owner 续24 已否决全员锁死路线（"我们是在做研究而不是做复杂的系统工程"），续28④采**诚实审计**形式 = P0 登记册 + 系统自检 + **本报告呈外部审查者盖章**。我们据实说明：这是**制度形态的差异**，不是把独立性取消；人员级独立评分作为 M4 前的**可选**升级保留（F-3 blinded confirmatory 选项）。

## 7. 请求（盖章位）

请审查者**核对 §3 索引表与详情小节的每一行/每一节**：修复项的证据指针（test 名 / checker rule / register 路径）是否属实、DEFERRED 项是否**正确挂门**（续29 SAP 冻结、P2/M2/M3 门）、OWNER-RULED 项引用是否忠实、P0 是否被**如实呈为 INCOMPLETE**。据此二选一：

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

> 生成方式：对下表每一文件计算 SHA-256（脚本逻辑等价于 `Get-FileHash -Algorithm SHA256` / `sha256sum`）；两仓 HEAD 以 `git rev-parse HEAD` 取得。**审查者核验路径**：clone 两仓至下列 HEAD → 对每行重算哈希 → 与本表逐行比对；任何不符即构成"证据不符"退回理由（§7）。**本报告自身不在表内**（追加/扩写本文都会改变自身哈希——**其权威版本以伞仓 git 历史为准**，此排除为设计使然）。

（HEAD 为本证据表生成时点的两仓提交；本报告定稿提交为伞仓 HEAD 的直接后继——核验者以 git 祖先关系确认即可，表内其余文件在定稿提交中字节不变。）

伞仓 HEAD: `016a789b0e70` · W1 HEAD: `ab1c68017671`

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
