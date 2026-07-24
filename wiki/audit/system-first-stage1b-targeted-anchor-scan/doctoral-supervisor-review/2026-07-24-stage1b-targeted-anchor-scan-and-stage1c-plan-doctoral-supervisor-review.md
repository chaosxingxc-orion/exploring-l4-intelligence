---
title: "Stage-1B targeted-anchor scan and Stage-1C research-plan doctoral-supervisor review"
date: "2026-07-24"
artifact_type: "REVIEWER_FACING_DOCTORAL_SUPERVISOR_ASSESSMENT"
campaign: "system-first-stage1b-targeted-anchor-scan"
round: "doctoral-supervisor-review"
review_target: "SF-STAGE1B-TARGETED-ANCHOR-SCAN-REVIEW-PACKAGE-RC1"
review_package_manifest_sha256: "d70de83e36b4d2c07ae0ab02506b60269620bd5d5768d6ca7b8366d11818e0e6"
stage1c_plan_sha256: "bdf2b62de1495e7b8380052990d1b268e5e8c6b1343dd2950313f48589846c51"
capability_delta_manifest_sha256: "ee8f0564069475f58f9be313a7978db662665d1d379b213d3005507c59dea3a6"
frozen_stage1b_v5_release: "38fb9435d0c35e226ad62b16015a6dbee054e6c2"
recommended_targeted_overlay_verdict: "RECOMMEND_SIGN_STAGE1B_TARGETED_ANCHOR_SCAN_RELEASE_AFTER_GIT_BYTE_FREEZE"
team_execution_recommendation: "CONTINUE_WITH_BOUNDED_CONSOLIDATION_AND_CALIBRATION_PREPARATION"
stage1c_scaleout_recommendation: "WITHHOLD_320_PAPER_SCALEOUT_PENDING_CONSOLIDATED_METHOD_CONTRACT_AND_CALIBRATION"
research_execution_authorized: false
authority_effect: "NONE_REVIEWER_FACING_ADVICE"
human_signature_claimed: false
novelty_verdict: "NOT_REQUESTED_AND_NOT_ISSUED"
---

# Stage-1B 定向锚点扫描与 Stage-1C 调研计划博导级审查

## 一、导师裁决

本次审查必须把三个问题分开回答。

### 1. 是否接受新识别的 24 篇论文

**建议接受，并建议 independent reviewer 在精确 RC1 文件集完成 Git 字节冻结后签发：**

`SIGN_STAGE1B_TARGETED_ANCHOR_SCAN_RELEASE`

这个建议仅针对 manifest SHA-256 为
`d70de83e36b4d2c07ae0ab02506b60269620bd5d5768d6ca7b8366d11818e0e6` 的十项 RC1 文件。
它认可的是一个有界、可审计的 24-work Stage-1B overlay，不是对文献宇宙完整性的签名。

给出正面建议的理由是：26 篇候选均有 PDF、arXiv e-print 和提取文本的本地哈希绑定；24 篇纳入和两篇
`SCANNED_NOT_PROMOTED` 的身份及理由明确；24 条记录与冻结 226、CURRENT 继承并集及 14-work capability
delta 均无 canonical identity 重复；reference、borrowed protocol 与 reproduction 三种关系没有混写；所有新增
记录都保留了论文实验设置、对照、全文 locator 和最强限制；没有把本地全文存在误写成代码、数据、许可或
复现已经闭合。

审查时该 RC 仍位于未提交工作区，尚无可引用的 Git commit/blob。因此，本文件给出的是“达到科学签署条件，
待字节冻结后可签”的 reviewer 建议，而不是代替 independent reviewer 的签名。

### 2. 是否同意研究团队继续执行

**同意，而且建议尽快继续。** 但“继续”应严格解释为：

- 冻结并分别完成 14-work capability delta 与 24-work targeted-anchor overlay 的独立 release review；
- 停止无边界扩种子，不再为每个发现写一份 amendment；
- 将新增证据一次性合并到一个自洽的 Stage-1C pre-calibration 方案；
- 修复仍然存在的四项方法合同缺口；
- 建立并执行 bounded calibration packet，然后再请求 Stage-1C full mapping signature。

**不同意**把“团队继续执行”解释成现在就开展 320-paper scale-out、模型/API 调用、benchmark metric、论文复现、
prototype、方向排名、问题选择或技术 novelty 收敛。这些均未被当前 authority 授权。

### 3. 是否已经足够进入 Stage-1C 全量调研

**尚不足以立即进入 320-paper 全量映射，但已经足以停止继续广泛找论文并转入一次有界的方法整合。**

这一区分很重要。新扫描显著修复了典型 speech/omni、多轮语音记忆、全双工评价、主动感知、音频
training-free decoding、多模态技能和 memory-to-action 文献缺口。问题空间在“支持做 pre-calibration”的意义上
已经基本识别完成；但现有 Stage-1C proposal 仍绑定 296-paper surface，且前一轮指出的四项 P0 尚未被修改。
因此，文献发现已经不再是当前主阻塞项，方法合同才是。

建议采用以下分段裁决：

- targeted overlay：`RECOMMEND_SIGN_AFTER_GIT_BYTE_FREEZE`；
- 团队下一步：`APPROVE_BOUNDED_CONSOLIDATION_AND_CALIBRATION_PREPARATION`；
- 320-paper full mapping：`WITHHOLD_PENDING_CONSOLIDATED_METHOD_CONTRACT_AND_CALIBRATION`。

本裁决不讨论技术方案创新性。整个 Stage-1 的任务仍是把综述、问题结构、实验协议和复现基座做扎实；技术
创新的收敛留到 reproduction-first Stage-2A，并在 Stage-2B 验证。

## 二、审查对象与独立核验

### 2.1 精确对象

本审查绑定：

- targeted-anchor RC1 manifest：
  `wiki/survey/workbench/system-first-stage1b-targeted-anchor-scan/review-package-manifest.json`；
- manifest SHA-256：
  `d70de83e36b4d2c07ae0ab02506b60269620bd5d5768d6ca7b8366d11818e0e6`；
- Stage-1C v2 proposal：
  `wiki/survey/workbench/system-first-stage1b-capability-delta/stage1c-v2-capability-research-program-zh.md`；
- proposal SHA-256：
  `bdf2b62de1495e7b8380052990d1b268e5e8c6b1343dd2950313f48589846c51`；
- capability-delta RC1 manifest SHA-256：
  `ee8f0564069475f58f9be313a7978db662665d1d379b213d3005507c59dea3a6`；
- 冻结 Stage-1B v5 release commit：
  `38fb9435d0c35e226ad62b16015a6dbee054e6c2`。

proposal 的字节与上一轮博导审查时相同。换言之，新扫描改变了可用证据，却尚未改变研究计划本身。前一轮
对 proposal 的四项方法学保留意见因此继续有效，不能因新增 24 篇论文而自动消失。

### 2.2 机器核验

本次独立执行：

- `python -m unittest scripts.survey.test_sf_stage1b_targeted_anchor_scan -v`：7/7 tests 通过；
- `python scripts/survey/sf_stage1b_targeted_anchor_scan.py`：确认 26 scanned、24 promoted、320 combined
  unsigned candidate union；
- 78/78 个 PDF、e-print、extracted-text 文件哈希通过；
- 52 个 PDF/e-print rendition 与全局 full-text ledger 对账，冲突哈希为 0；
- capability-delta RC1 manifest 的 15 项既有文件保持逐字节一致；
- 24 条新增身份与继承面及 capability delta 无 canonical 重复。

还对六个会显著影响研究计划的承重事实做了全文抽查：

1. Audio MultiChallenge 的 452 conversations、47 speakers、1,712 rubrics 与 fixed-context final-turn
   protocol；
2. Full-Duplex-Bench-v2 的 WebRTC examiner、Daily/Correction/Entity Tracking/Safety 任务族；
3. Temporal Contrastive Decoding 对原音频和 temporal-blur 音频 next-token logits 的训练免费对比；
4. VISUALSKILL 的 177 tasks、matched text-only control 与 `load_topic` skill access；
5. Utility-Oriented Visual Evidence Selection 对 relevance、utility、surrogate 与 oracle arms 的区分；
6. MultiVox 的 1,000 个真人标注/录制 speech+visual questions。

上述抽查与 records/map 的核心表述一致。抽查不等于对 24 篇论文所有数值做了二次复算；本阶段签署的是论文
证据映射，不是论文结果复现。

## 三、新扫描带来的实质进步

### 3.1 典型 speech/omni 漏项得到明显修复

新增事实地图不再主要依赖视觉或纯文本 agent analogy。它加入了：

- 多轮自然语音对话与 semantic/audio-cue memory 的分层测量；
- 用 paired voice attributes 检验模型是否真的利用语音信息；
- audio-grounded conversational instruction/knowledge/robustness；
- 自然 disfluency、speaker/domain 和 modality switching；
- full-duplex examiner、turn-taking 与 task-objective 分离；
- 语音 agent action token、自反思与训练边界；
- 直接作用于 audio logits 的 training-free decoding boundary；
- audio process reward、omni active perception 与 omni retrieval 的 trained upper boundaries。

这使“典型语音相关论文缺失”从不可接受的结构性缺口，降为“仍需资产闭合和后续持续触发式更新”的可控风险。

### 3.2 不再把多模态、训练免费和外部控制混为一谈

24 条记录的 multimodality 分布为：

- `MM3_CAUSALLY_MULTIMODAL`：2；
- `MM2_MULTIMODAL_ASSET`：12；
- `MM1_MULTIMODAL_TASK_ONLY`：4；
- `MM0_TEXT_ONLY`：6。

只有两项达到 matched 去模态/换模态意义上的因果多模态证据，说明当前文件没有把“任务包含音频/图像”夸大为
“该模态已经被证明不可替代”。同样，Temporal Contrastive Decoding 被标为需要 logits 的 gray-box boundary，
trained reward/policy 系统也没有被包装成 TF-Strict 黑盒外部控制。

### 3.3 证据关系保持克制

24 条记录中：

- `BORROWED_PROTOCOL_ANALOGUE`：18；
- `REFERENCE_CONTEXT`：6；
- `REPRODUCTION_ANCHOR`：0。

这个结果不是失败。Stage-1B 的任务是识别方法路径、相邻协议和边界；没有闭合 data/code/model/evaluator/access
时坚持 reproduction anchor 为 0，比为了“看起来完整”而制造假锚点更可信。

### 3.4 正面证据、仪器和边界没有被混成一个投票池

role 分布为 11 instrument、7 boundary、4 component path、1 direct path、1 negative/falsifier。它揭示了一个重要
事实：这批新证据主要强化了“怎样测量、怎样设计对照、哪里会失效”，而不是新增大量可直接搬用的本项目方法。
因此，后续 Stage-1C 不能按论文数量或最新年份投票，也不能因为某个主题论文多就自动升级为主线。

## 四、仍然存在的内容与方案遗漏

### P0-1：Stage-1C proposal 的输入身份已经过时

现有 proposal 仍写 296 个 canonical works：282 inherited union + 14 capability delta。新增 targeted overlay 形成
三种必须保持区分的计数：

- 282：CURRENT 继承并集；
- 296：继承并集 + 未签名 14-work capability delta；
- 306：继承并集 + 未签名 24-work targeted overlay；
- 320：两个未签名 overlay 都叠加后的候选并集。

320 现在只是 candidate union，不是 signed Stage-1C denominator。proposal 不能直接把 296 改成 320 然后继续；
它必须先绑定两个独立 signature，再生成一个唯一的 release-merge manifest，明确每一层来源、签名、hash、去重和
authority。

### P0-2：前一轮四项方法缺口仍未修复

由于 proposal 字节未变，以下问题仍然阻断 full scale-out：

1. 三个原始问题轴与 D0-D4 intervention axes 没有形成强制 crosswalk；
2. calibration preparation 的 owner token 与 full mapping 的 reviewer signature 仍有授权重叠；
3. calibration 与 20% blind review 仍缺 exact IDs、N、抽样 seed、coder blinding、字段级 agreement 阈值、
   recoding 和 adjudication 规则；
4. post-sign 320-paper package 仍缺统一的 paper/run/observation/comparison/dataset/family/review-event schemas 和
   whole-package validator。

新增论文不能修复这些研究设计问题。继续搜论文只会扩大待编码面，不会让方法学自动可靠。

### P0-3：15 条 `NEW_PROBLEM_HYPOTHESIS_PENDING_OWNER` 尚未完成路由

24 条新记录对 problem axes 的多标签计数为：

- `BUDGET_STOP_REPAIR`：14；
- `EVALUATOR_REWARD_RELIABILITY`：10；
- `INTERACTIVE_FULL_DUPLEX_OBJECTIVES`：5；
- `NEW_PROBLEM_HYPOTHESIS_PENDING_OWNER`：15。

15 个 pending 标签说明新扫描确实提出了现有三类问题包之外的可能研究问题，例如主动多模态证据获取、skill
library 维护与负迁移、memory retrieval-to-use gap。它们现在只能是未排序的 candidate hypotheses。团队必须逐条
决定：

- 可路由到现有问题包；
- 只是 D1-D3 intervention/asset，不构成独立 problem；
- 保持 unassigned boundary；或
- 提交 owner 作为 candidate-set expansion。

如果不做这一步，D0-D4 会静默替代问题轴，博士课题会从一个 program question 扩张成五个互相竞争的项目。

### P0-4：仍没有 task-matched speech/omni reproduction anchor

本次新增了五个有价值的 speech/omni instrument 或 nearest-prior candidates：Audio MultiChallenge、MultiVox、
VCB Bench、RealTalk-CN 和 Full-Duplex-Bench-v2。但 candidate 不等于 anchor。目前仍缺：

- 精确 data/code/model/judge 版本；
- 许可和 access closure；
- loader 与最小 task slice；
- evaluator 可执行性及与 reward 的独立性；
- 与 TF-Strict 黑盒合同的 access 对齐；
- 计划复现时允许偏离原论文的 deviation ledger。

这不阻断 Stage-1B overlay 的签署，但阻断把“实验基座已夯实”写成完成态。Stage-1C 应选一个 primary
reproduction candidate 和一个 fallback，先做不运行模型的资产/协议 closure；真正运行复现仍留到 Stage-2A。

### P1-1：定向扫描缺少可重放的发现过程

RC1 精确记录了 26 个被扫描 ID，却没有记录检索数据库、query strings、检索日期、候选池大小、初筛过程、各层
排除数量和停止/饱和规则。因此它可以被签署为“对这 26 个指定身份的有界全文扫描”，不能被用于声称：

- 相关文献宇宙已经 closed；
- 所有典型论文都已发现；
- 24/26 是可解释的系统综述纳入率；
- 当前主题的相对论文密度代表研究重要性。

最快修复不是重跑大规模检索，而是补一个轻量 discovery provenance record：列出本轮来源、query family、日期、
进入 26 个 exact IDs 的规则，以及从现在起只在“新论文改变方法路径、推翻承重前提或填补直接锚点”时触发增量
检索。

### P1-2：canonical paper 去重不等于 claim work 去重

RC1 已证明 24 个 paper IDs 与其他 surface 不重复，但多个论文仍可能支持同一个实验主张。例如“被动相关性不等于
决策效用”“检索到 memory 不等于使用 memory”“增加采样预算不保证提升”会在不同论文、不同模态中反复出现。
如果每篇论文都生成一个独立 family/branch/seed，会重新造成团队此前明确反对的重复 claim work。

建议建立最小 claim registry：

```text
claim_id
claim_text
scope = task × model × access × budget/horizon
primary_owner_work_id
supporting_work_ids[]
falsifying_or_boundary_work_ids[]
evidence_level
transfer_status
decision_impact
```

同一 claim 只有一个 owner；其他论文作为 support、boundary 或 falsifier 挂接。paper 可以支持多个 claim，但不得因
论文数量重复创建多个种子或把同一主张多次计权。

### P1-3：远域 protocol analogue 仍需显式 translation contract

24 条记录中有 6 个 text-only、若干 VLM/GUI analogue。它们可以贡献对照结构，却不能直接继承到 speech/omni。
每个进入 Stage-1C 的远域协议至少应声明：

- 被借用的决策结构是什么；
- 哪些 task/data/model/access 发生变化；
- 哪个变量在 speech/omni 中具有对应物；
- 最强 transfer failure 是什么；
- 什么观察结果会拒绝迁移，而不是只确认迁移。

没有 translation contract 的 analogue 只能留作参考，不应进入承重 family conclusion。

### P1-4：新证据高度偏向近期论文与评价协议

24 篇均来自 2025–2026，且 11/24 是 instruments，只有 1/24 被编码为 direct path。这个构成对于修复近期漏项是
合理的，却不能单独支撑历史路径完整性或方法成熟度。冻结 Stage-1B v5 和 CURRENT 继承面仍必须作为较早方法、
直接路径和反证的来源；targeted overlay 不能取代它们。

## 五、新证据应如何改变 research proposal

### 5.1 不改变的部分

以下内容不应改变：

- Project Thesis：研究冻结黑盒 omni core 外部的 reward-guided control plane；
- Stage-1C 的目标：做问题与实验结构映射，不做技术 novelty verdict；
- D0-D4 作为 intervention axes，而非五个自动成立的研究方向；
- reference、borrowed protocol 与 reproduction 的三分合同；
- Stage-2A reproduction-first，Stage-2B 再验证创新性和有效性。

### 5.2 必须改变的部分

proposal 至少需要一次 in-place consolidation：

1. 输入从固定的 296 改为“两个 overlay 分别签署后才成立的 320-work signed candidate surface”；
2. 加入 24 条新记录及两条 scanned-not-promoted 的 provenance；
3. 把 15 个 pending problem hypotheses 路由到现有问题、intervention-only、boundary 或 owner expansion；
4. 把八个 experiment families 明确降格为 `CANDIDATE_PROTOCOL_TEMPLATE`，允许 merge/split/unrouted；
5. 在 calibration strata 中加入 task-matched speech/omni、MM3 matched control、instrument/direct/boundary、
   gray-box/train-based boundary、retrieval-to-use 与 evaluator disagreement；
6. 加入 claim-level dedupe，防止 38 条 overlay 生成重复 seeds；
7. 增加 reproduction-candidate closure table，并选 primary/fallback；
8. 将所有 296/60 等旧计数更新为签名后 320/至少 64，且保留来源层含义。

这不是写一份 amendment。应直接改写当前 proposal，使它成为唯一 self-contained active contract；旧版留在 Git/audit
provenance 中，不继续进入 AI 默认浏览面。

### 5.3 建议保留的三个 problem bundles 与新增候选

当前三个 problem bundles 仍然有效：

| Problem bundle | 新证据带来的加强 | 主要 intervention axes |
|---|---|---|
| `BUDGET_STOP_REPAIR` | active evidence、test-time strategy、RegionFocus、TTS falsifier | D0、D1、D3、D4 |
| `EVALUATOR_REWARD_RELIABILITY` | audio judge disagreement、utility vs relevance、process reward、unsupported claim | D0、D1、D4 |
| `INTERACTIVE_FULL_DUPLEX_OBJECTIVES` | fixed-context memory、duplex examiner、disfluency、modality switching | D0、D3、D4 |

建议提交 owner 但暂不排名的 candidate hypotheses 是：

- `ACTIVE_MULTIMODAL_EVIDENCE_ACQUISITION_UNDER_BUDGET`；
- `SKILL_ACCESS_MAINTENANCE_AND_NEGATIVE_TRANSFER`；
- `MEMORY_RETRIEVAL_TO_USE_AND_ACTION_GAP`。

这三项是否升级为独立 problem bundles，应由 Stage-1C evidence mapping 和 owner 决策决定；当前不得因近期论文多或
主题听起来新颖就升级。

## 六、最小且快速的方法修复包

目标是在不扩张对抗式代码工程的情况下，把团队最快送到可签署的 Stage-1C mapping gate。

### Gate A — 冻结并释放两个 Stage-1B overlays

1. 将 targeted-anchor RC1 十项 manifest 内容按当前 SHA-256 冻结到 Git；
2. independent reviewer 分别处理：
   `SIGN_STAGE1B_CAPABILITY_DELTA_RELEASE` 与 `SIGN_STAGE1B_TARGETED_ANCHOR_SCAN_RELEASE`；
3. 任一 overlay 改字节都必须形成新 manifest，不能沿用旧建议；
4. 两个签名互不替代，也都不自动激活 Stage-1C。

### Gate B — 一次性形成 320-work pre-calibration contract

只新增或改写以下必要产物：

1. 一个 release-merge manifest：逐层绑定 226、282、14、24、320 的来源与 hash；
2. problem-axis × intervention-axis crosswalk；
3. claim registry 与 paper-to-claim links；
4. 320-paper bootstrap 与 source-layer provenance；
5. paper audit、run cell、observation、comparison、dataset、family、review-event schemas；
6. exact calibration manifest 与 agreement contract；
7. reproduction-candidate asset/readiness table；
8. 一个 whole-package checker。

不需要为此开发 fuzzing、故障注入、复杂恢复或通用工作流框架。checker 只验证 count、identity、provenance、schema、
referential integrity、claim dedupe、authority 和 required fields。

### Gate C — bounded calibration

建议 calibration packet 采用以下最小设计：

- 纳入全部 38 条新 overlay records，因为它们引入了新 ontology、MM levels、远域 transfer 和 pending problems；
- 再加入 exact-ID inherited sentinel set，覆盖三个原问题包、H5/withheld、direct/instrument/negative/boundary、
  speech/omni、lineage 和 reproduction-candidate hard cases；
- 在 packet manifest 中冻结最终 N 与 canonical IDs，不能只写“分层小批量”；
- 两名 coder 在看到彼此标签前独立编码；secondary coder 尽量不见既有 role、primary direction 和 family；
- critical categorical fields 的 pre-adjudication raw agreement 至少 85%，并预注册一个适合低频/偏斜类别的
  chance-corrected 指标；
- 未达阈值只允许一次 codebook consolidation，然后对完整 calibration packet 重编码；
- 全部分歧 adjudicate，不能用总平均掩盖 reproduction、lineage、MM3 或 core-member 分歧。

### Gate D — 请求 Stage-1C full mapping signature

calibration 通过后，才请求 `SIGN_STAGE1C_V2_EXPERIMENT_MAPPING`。若 320 成为 signed input，full mapping 的 20%
blind review 必须是至少 64 条 unique works，并预先冻结分层算法和 random seed。calibration 后讨论过的记录不能冒充
未见标签的 blind sample；`CORE_MEMBER`、lineage、reproduction anchor、family evidence state 和 branch card 继续
100% second review。

该签名允许 paper disposition、承重 experiment extraction、dataset graph、evidence-led family synthesis 和
unexecuted branch dossiers；仍不授权研究模型/API、metric、reproduction、prototype、problem winner、owner selection
或 novelty verdict。

## 七、实验基座的最小补强建议

### 7.1 reproduction candidate 只选一主一备

不建议同时为五个 speech/omni candidates 建复现分支。建议按以下顺序完成只读 closure：

1. Full-Duplex-Bench-v2：最邻近 interactive system problem，但需逐项闭合 v2/v3 lineage、WebRTC examiner、data、
   code 和 evaluator；
2. Audio MultiChallenge：适合 memory/evaluator instrument，需闭合数据、rubric/judge、许可与最后一轮 protocol；
3. MultiVox：适合 MM3 causal instrument，需闭合 paired assets 和 speech/visual matching；
4. VCB Bench：适合 evaluator-disagreement instrument；
5. RealTalk-CN：适合中文 disfluency/modality-switching stress test，但 domain transfer 更强。

资产和许可核验后，只选择一个 primary、一个 fallback。若 Full-Duplex-Bench-v2 的公开资产或 evaluator 不能闭合，
不应无限等待，应切换到 Audio MultiChallenge 或 MultiVox。Temporal Contrastive Decoding 可保留为 gray-box diagnostic
boundary，不宜作为 TF-Strict 主复现锚点。

### 7.2 reward 与 outcome 不得共用唯一 judge

新文献进一步暴露 evaluator disagreement 和 utility proxy 风险。Stage-1C protocol 必须区分：

- online reward/score：用于决定下一步动作；
- primary outcome：独立、task-grounded 的成功指标；
- secondary diagnostic：judge、confidence、process score；
- human audit：只对高风险或争议 strata 抽样。

如果同一个 LLM judge 同时决定控制动作又作为唯一最终 outcome，任何“控制有效”结论都会有 reward hacking 或
self-confirmation 的替代解释。

### 7.3 先摸高，再做成本公平比较

按 Project Thesis，Stage-2 的资源顺序应是：先在预算照实记录的条件下探索冻结模型 headroom；确认存在可重复提升
后，再做 consolidation 和 equal-budget comparison。Stage-1C 只负责把 budget/horizon、停止、额外调用、工具成本
和 evaluator 成本写进 run cell，不应提前用严格等预算门排除可能的控制路径。

## 八、对“新问题基本识别完成”的严格表述

建议团队与 reviewer 使用以下措辞：

> 在冻结 Stage-1B v5、CURRENT 继承面、14-work capability delta 和本次 24-work targeted overlay 所声明的
> 有界范围内，影响 Stage-1C 方法设计的主要问题类型已经基本识别，可以停止无边界扩种子并转入
> pre-calibration consolidation。该结论不是 literature-universe closure；后续只接受会改变方法路径、推翻承重
> 前提或填补 task-matched direct/reproduction anchor 的触发式增量。

不应使用“全部问题已经识别”“相关论文已经穷尽”或“320 篇代表完整文献宇宙”。

## 九、给 independent reviewer 的建议文本

针对 targeted overlay，建议 reviewer 在 Git 字节冻结后返回：

`SIGN_STAGE1B_TARGETED_ANCHOR_SCAN_RELEASE`

并附带以下不扩权说明：

> This signature releases only the exact 24-work targeted-anchor Stage-1B overlay bound by manifest
> SHA-256 d70de83e36b4d2c07ae0ab02506b60269620bd5d5768d6ca7b8366d11818e0e6. It does not claim
> literature-universe closure, sign the separate 14-work capability delta, create a reproduction
> anchor, activate the 320-work Stage-1C surface, authorize research execution, rank or select a
> problem, or issue a novelty verdict. The research team may proceed only with a bounded consolidated
> pre-calibration contract and calibration packet until a separate Stage-1C mapping signature is
> issued.

## 十、最终导师意见

**同意研究团队继续执行，并建议快速继续。** 新扫描在内容上是有价值的，尤其修复了此前不可接受的典型
speech/omni 漏项，并把多模态因果、训练边界、评价器与 protocol analogue 的关系处理得较克制。继续扣留这个
有界 Stage-1B overlay 不会提高研究质量。

但不建议用“再找一批论文”替代方法整合，也不建议把 24 篇新论文直接变成 24 个种子或分支。现在最需要的是：

1. 分别签署两个 overlay；
2. 以 claim 为单位去重；
3. 一次性改写当前 proposal；
4. 关闭 problem/intervention、authority、calibration 和 schema 四个 P0；
5. 完成 bounded calibration；
6. 再申请 320-paper Stage-1C mapping signature。

做到这些，团队就不是“继续打补丁”，而是在把 Stage-1B 的证据积累转换成一个可重复、可审计、能真正进入
Stage-1C 的研究方法。

## 十一、权限、provenance 与失效条件

- 本文件是 AI 生成的 reviewer-facing 博导级建议，不声称人类签名；
- 本文件不改变 `wiki/Research-Objective.md` 中的当前 authority；
- 本文件没有运行研究模型、API、benchmark metric、复现或 prototype；
- 本文件不签发 owner token、reviewer token、Stage-1C execution 或 Stage-2A authority；
- 本文件不作项目 novelty verdict；
- 若 targeted RC1 manifest 或其任一承重 artifact 字节变化，本文件的正面 release 建议失效；
- 若 capability delta 或 targeted overlay 未取得独立签名，320 不得称为 signed Stage-1C input；
- 若后续 consolidated pre-calibration package 已关闭本文件的 P0，本文件对 scale-out 的 withholding 应由针对新
  manifest 的独立 review supersede，而不是通过 amendment 修改本文件。
