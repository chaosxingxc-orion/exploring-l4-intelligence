---
response_id: SURVEY-RESP-2026-07-14-01
title: 对《Survey v2 与 Stage-1C 决策包博导级对抗复审》的正式回应 + P0 整改
date: 2026-07-14
responds_to_review: "wiki/2026-07-14-survey-v2-and-stage1c-decision-package-doctoral-adversarial-review.md @ commit b41f9f85db359fa5b13cadbcb4024c130d43542e"
survey_snapshot:
  repository: exploring-l4-intelligence (umbrella)
  commit: 233dc7eb9224b5d7bc8df7bfd81a616ab15c6917
  note: "评审 §2 六项 git-blob SHA-256 已由核验镜头逐一重算，6/6 一致；且工作树六文件与该 commit blob 逐字节相同（git hash-object 核验）——不存在『审错版本』抗辩。"
stage: Stage-1A
stage_claim: ROUND1_SCOUT_COMPLETE
generated_by: "Claude Fable 5 主会话（编排+综合+本信撰写）；核验=五镜头工作流 wf_2c70bfda-dac（5 agents / 557k tokens / 139 tool calls）；replay bundle=代码代理构建、主会话核数"
verified_by: "Claude Fable 5 主会话（亲验清单见 §1；与镜头非同一无监督代理）；载重更正的人类双审 = P1 排期项"
adjudicated_by: "owner（2026-07-14 亲答：P0 核验完即执行=已执行；接受 Stage-1C 门控=P0+P1 关闭前不提请选题）"
known_missing_raw_events:
  - "305 次检索/抓取的原始返回（raw response）——当时未捕获，按模板规则 2 永不补造：RAW_EVENT_UNAVAILABLE"
  - "search_results 结果宇宙、screening decision 轨迹、日内时间戳、逐查询 agent 身份：RAW_EVENT_UNAVAILABLE"
owner_decision_requested: false
stage1b_authorized: false
evidence_archive: docs/checks/2026-07-14-surveyv2-review-fivelens-verification.json
replay_bundle: wiki/survey/replay/SURVEY-RESP-2026-07-14-01/
---

# 对 Survey v2 博导级对抗复审的正式回应（P0 整改随附）

## 0. 一页结论（模板 §3.1）

```text
本轮状态：ROUND1_SCOUT_COMPLETE（接受评审状态纠偏；「Survey v2 complete/调研收官」措辞由本信 supersede）
已完成：P0 全八项（详 §3/§6/§7）；五镜头独立核验（详 §1-§2）
未完成：P1 全部（9 个饱和目标 + 本轮新增 8 篇、identity contract 冻结、comparator 重建、C1/C4、独立盲重建）
本轮允许的最强结论：NO_DIRECT_MATCH_WITHIN_LOGGED_SCOPE（带 §5 收窄措辞）；5 kill 方向保持、证据级封顶 ABSTRACT_VERIFIED 待双审
本轮明确不允许的结论：novel / saturated / decision-ready / SOTA / strongest-differentiator（无限定形式）
是否请求 owner 做 Stage-1C 选择：NO（owner 已裁决接受门控：P0+P1 关闭、STAGE1C_DECISION_READY 后才提请）
是否请求 Stage-1B 放行：NO
```

**总处置：ACCEPT_MAJOR_REVISION_WITH_FOUR_EVIDENCED_CONTESTS。** 评审的机械重算、事实纠错、
证据等级、状态纠偏全部接受并已执行；「合取洗白」时序叙事、I3/UMBRELLA 合取指控、「I4 方法学对象
已被占据」措辞、「bare-I2 身份级 DIRECT_OCCUPIED」整改令四处以日期链与格级证据抗辩（§4）。

## 1. 核验方法与 provenance

五镜头独立核验（机械重算/论文事实/I4 占据/身份时序/证据等级），全文存档 `evidence_archive`。
主会话亲验：query log 305 行 engine 二分 **WebSearch 218 + WebFetch 87**（评审 P0.3 逐字复现）；
六 blob 哈希由镜头以 `git show 233dc7eb:<path> | sha256sum` 重算 6/6 一致。四篇涉事论文均一手抓取
（2606.04680 与 2510.19471 HTML 全文、2309.15649 PDF、2409.00217 abs）。

## 2. 逐项处置表（模板 §3.2）

| Finding | Disposition | 核验裁定 | 证据/整改工件 |
|---|---|---|---|
| R1 阶段一致性（complete 上标） | **ACCEPTED** | 旁证坐实（commit 信息自称 complete+自检合规，后者被 L95 证伪） | §7 状态纠偏 |
| R2 检索不可回放 | **ACCEPTED** | CONFIRMED（218/87、无 raw/无结果宇宙/无时间戳） | bundle `search_events.jsonl`（历史标 RAW_EVENT_UNAVAILABLE） |
| R3 去重不可重建（~93） | **ACCEPTED（评审自身数字纠正）** | PARTIAL：93 确不可机械重现；但评审的 107 应为 **110**（107=大小写折叠副产物）；_est 后缀原本在档 | bundle `papers.jsonl`+`dedup_report.json`（精确值见 §3.6） |
| R4 证据等级系统性上标 | **ACCEPTED（强度=QRP 非造假）** | CONFIRMED：39/39 FT 无定位器（抽查 8/8 降级）；5 kill 深度=WebSearch 存在性；但膨胀系**自我披露**（三 header 明写 treat-as-SCOUT/ABSTRACT），下游裸 [VERIFIED] 继承属实 | bundle `claim_evidence.jsonl` 全量机器降级 |
| R5.1 READ ~70-85% 上夸 | **ACCEPTED** | CONFIRMED：Table 1 重算 7.7–68.5%，LS 仅 11.9–16.5%；v2 相对 round-1 ledger 系退化 | §3.1 更正 + bundle 更正行 |
| R5.2 MBR/Llama-3 焊接 | **ACCEPTED** | CONFIRMED：MBR=成对 BLEU（sacrebleu）；Llama-3 只属 ProGRes comparator 且 0.043 **败于** MBR 0.033——更正后 I1 kill 更强 | §3.2 |
| R5.3 TAP-GER | **PARTIAL ACCEPT** | 落点对（生成式纠错越过池 oracle ≠ 池内选择）；但评审支撑句与原文 Table 3 矛盾（frozen 8.72<9.78 无需 fine-tuning） | §3.3 + §4 勘误 |
| R5.4 ProGRes 扩池混写 | **ACCEPTED** | CONFIRMED（另坐实 ledger 内部 PARTIAL/DIRECT 不一致） | §3.4 |
| R6 I2 理由行自相矛盾 | **ACCEPTED** | CONFIRMED（package §I2/kill-matrix L58「all external」与自家 L57/L198 矛盾） | §3.5 |
| R6 合取洗白（FUNDAMENTAL） | **DISPUTED_WITH_EVIDENCE（部分）** | PARTIAL：程序缺陷（未登记/未标 post-hoc）接受并已整改；「见近邻才加限定词」时序叙事被日期链反驳 | §4.1 |
| R7 I4 遗漏更广 TTS 文献 | **ACCEPTED（覆盖面）** | CONFIRMED：4/5 篇矩阵级零命中、饱和目标未自认缺口 | §5 + bundle `round2_new_targets.jsonl` |
| R7 「同一方法学对象已被占据」 | **DISPUTED_WITH_EVIDENCE（措辞）** | PARTIAL：五篇全为相邻对象（难度/粒度/策略/personalization/K 轴），无一有供给轴 c 或 ρ(c)/H(c) 分解 | §4.3 |
| R8 SOTA cards 可比性 | **ACCEPTED** | 未单独开镜头；随 P1 comparator 重建执行（降名 comparator seed cards） | P1-4 |
| R9 禁词/自检失效 | **ACCEPTED** | CONFIRMED：sota-cards L95 实质 EMPTY 与自家 header+commit 自检声明矛盾；86 处裸 NO_DIRECT_MATCH vs 9 处带限定 | §3.7 + bundle 校验器禁词扫描 |
| R10 QRP 高风险/非造假 | **ACCEPTED（原文强度）** | 与 R4 核验一致：标签层膨胀+下游继承=流程控制缺陷；一手数字全部可溯源到真实论文真实表格 | 全信 |

## 3. 已执行的更正登记（全部为 supersession——不改写被审工件的历史字节）

1. **READ 2606.04680**（三处载体：neighbor-matrix L147、kill-matrix L24、ledger L1223）：
   「~70-85% oracle」→ **Table 1 兑现率 7.7%–68.5%**（LS-clean 16.5 / LS-other 11.9 / VCTK 17.3 /
   ASRU 7.7 / TALCS 67.5 / SWBD 68.5 / TED3 54.3 / SPGI 43.5）；该行 our_data=librispeech 而 LS 实际
   仅 11.9–16.5%，原搭配尤其误导。正题《Read What You Hear: Reference-Free Hypotheses Evaluation
   with Acoustic Discrepancy》。可能的混淆源：Table 2 segment-level system combination（组合式改写
   算子，非 NLL rerank）。
2. **mbr-asr 2510.19471**（sota-cards L20 F2 行）：系统列「Whisper-lv3 + Llama-3 scorer」→ MBR 效用
   =成对 BLEU（sacrebleu），O(N²)，管线内无 LLM；0.042→0.033（Table 6/7）、oracle 0.013（Table 1）；
   Llama-3 只给 ProGRes comparator 打分且 0.043 败于 MBR（Table 9）。**更正后 I1 kill 更强。**
3. **TAP-GER 2309.15649**：8.72<9.78（Table 3，frozen，无 fine-tuning）数字属实，但算子=生成式纠错、
   产池外文本（Table 1：correction 使池 oracle 9.78→8.41；frozen GPT-2 29.56 远劣 first-pass 11.87，
   纯池内选择不可能）→ 从「kill-I1 DIRECT」重分类为**扩池/改写算子，挑战 oracle 锚语义**。
4. **ProGRes 2409.00217**：LLM 生成新假设扩池再评分 → 同上重分类；并修正 ledger 同一论文两 lane
   strength 不一致（PARTIAL vs DIRECT）。
5. **I2 理由行**：package §I2 与 kill-matrix L58「所有占据者均用 external TTS/GPT-4o/trained reward」
   → 更正为：scaling-auditory 2503.23395 的**同核** audio-conditioned beam log-lik 已占 bare-I2
   **机制**（自家 L57/L198 原有记载）；开放格=同核∧曲面（strict-I2=I2∩I4，已登记术语表）。
6. **~93 去重**：113 行 → exact-unique id 110 → arXiv-id 归组 104 → 别名合并后精确值 **94**
   （11 个多成员簇吸收 30 个源行、83 个单簇；uncertain_pairs 清空且留有证据链；`~93 (_est)` 与
   110/104/94 任何机械检查点均不重合——最近 94、差 1，登记为**无法解释**而非硬调和；逐簇依据见
   bundle `dedup_report.json`）。今后一律引用精确值 94。
7. **禁词**：sota-cards L95 实质 EMPTY 违规承认；本信及 bundle 一律使用带限定词表
   （NO_DIRECT_MATCH_WITHIN_LOGGED_SCOPE 等），bundle 校验器含禁词扫描并 fail-fast；对 86 处历史
   裸 NO_DIRECT_MATCH 以本条 supersession 声明统一追加限定语义（历史字节不改）。
8. **5 个 COORDINATOR-VERIFIED kill**：记录深度=WebSearch 存在性核验 → 证据级封顶
   ABSTRACT_VERIFIED；kill **方向**保持（其中 mbr-asr 经本轮全文重算反而加强）；固定版本+定位器
   +人类双审 = P1 排期。

## 4. 有据抗辩（DISPUTED_WITH_EVIDENCE）

### 4.1 「合取洗白」时序叙事——以日期链反驳其强形式

程序指控**接受**（strict-I2 未登记、未标 post-hoc、身份未冻结——已以术语表登记+本信整改）。但
「看到近邻才追加限定词保 novelty」的叙事与仓库日期链不符：同核生成器+验证器+δ_corr 出自
**2026-07-05** 理论文档 TH2a（commit 9b71a64，早于 READ/scaling-auditory 入档 8 天）；ρ 兑现面 =
**07-11 owner 签署** + 续34（07-13）研究对象锁定；I2 拟名当刻（07-13 重校准审查 L245）即自带
own-signal 生存条件；round-1 ledger 盲点(b)（07-13，猎杀前）已明写「acoustic scorer 从不是冻结 omni
自身信号」。记录中不存在「先有干净 I2、后见占据者、再加限定词」的序列。

### 4.2 I3-combined 与 UMBRELLA 合取指控——REFUTED

I3 的弃权+Goodhart 组合是**拟名时的原始定义**（术语表 07-13 登记；round-1 ledger L796 在猎杀前已把
该合取登记为目标格）；UMBRELLA 是 **2026-06-26 立项对象**（提案/06-30 survey/07-03 go-no-go/
Project-Thesis 全早于 v2），AudioToolAgent 07-06 已在档，且 v2 对新见的 IAD 2504.01931 做的是
**登记坍缩风险**而非定义排除——与洗白操作方向相反。

### 4.3 「I4 的方法学对象已被占据」——措辞过强

评审五篇引文全部真实、且 4/5 确系矩阵级遗漏（接受，全部进 round-2 目标）；但逐篇核验其条件轴为
难度（2408.03314）/验证粒度（2505.11730）/策略选择（2512.02008）/personalization RM 诊断
（2605.10991）/K 轴 VLA（RoboMonkey）——**无一实现供给类型轴 c 或 ρ(c)/H(c)/regret 分解**；survey
已在档的 siskos-2509.19567、ColdStart、KIT、JudgeBoN 反而更近。正确表述（接受为收窄）：
**scaling-surface 方法学族已被 text/VLA 广泛占据 → I4 可辩护空白收窄为「供给类型轴 × 冻结 omni
域实例化 × 从描述曲面升级为 label-free 可预测规律」；不构成 I4 的 DIRECT_OCCUPIED**。
决策包「single clearest whitespace」与 ledger「strongest differentiator」无限定修辞由本条 supersede。

### 4.4 「bare-I2 应写 DIRECT_OCCUPIED」整改令——按格级证据修正为「机制级占据、格局混合」

自家 kill matrix 中 bare-I2 的 ST/SLU 格为 NO_DIRECT_MATCH_WITHIN_LOGGED_SCOPE；身份级全格
DIRECT_OCCUPIED 与证据不符。采表述：「bare-I2 **机制**已被同核 beam log-lik 占据（audio-understanding
/SER 格 DIRECT_OCCUPIED），格局混合」。

### 4.5 评审自身勘误（礼貌登记，均不影响其实质结论）

107 应为 110（大小写折叠副产物）；READ 标题误写为「READ: Reversible Textual Rescoring for ASR」；
R5.3 支撑句「低于 oracle 须 prompting+fine-tuning」与原文 Table 3 frozen 行矛盾；2605.10991 标题系
意译（原题《Test-Time Personalization: A Diagnostic Framework and Probabilistic Fix for Scaling
Failures》）；其八个 READ 重算值中四个与我方重算有舍入级出入。

## 5. 双方共漏的三篇（本轮核验新查获，全部进 round-2 kill matrix）

1. **2606.02981**（Predicting Inference-Time Scaling Gains from Labeled Validation-Set Output
   Statistics）：**部分占据评审自己给 I4 开的升级药方**（小预算测量预测 held-out 收益，但
   label-assisted、纯文本）→ I4 升级版差异化必须显式= **label-free 预测量 × 供给轴 × 音频域**。
2. **2607.05391**（LLM-as-a-Verifier）：text agent 域「recovers a significant proportion of the
   oracle headroom」——头空兑现表述已入邻域。
3. **2602.12281**（CoVer，VLA）：verifier 同时选 rephrased instruction（=供给侧）与 action chunks——
   **Proposal E（供给选择作为决策问题）的最近邻威胁**，双方均漏。

连同评审五篇共 8 项新目标：`replay bundle/round2_new_targets.jsonl`。

## 6. Replay bundle（P0.2/P0.3/P0.4/P0.5 的机器工件）

`wiki/survey/replay/SURVEY-RESP-2026-07-14-01/`：`build_and_validate.py` 一键重建+校验（fail-fast，
含禁词扫描）；`search_events.jsonl`（305 事件，SEARCH/FETCH 分列，历史缺失全部显式
RAW_EVENT_UNAVAILABLE）；`papers.jsonl`+`dedup_report.json`（精确去重+逐簇依据）；
`claim_evidence.jsonl`（113 行全量机器降级 + 5 条更正行，更正行核验状态=单遍 AI 全文重算、人类双审
待 P1）；`flow_report.yaml`（全部脚本重算）；`manifest.yaml`（逐文件 bytes/lines/sha256/生成命令）。
**永久缺失**（规则 2 禁补造）：raw responses、结果宇宙、screening 轨迹、日内时间戳。独立盲重建者
可重建：事件数、计数、去重、更正后 claim 定位；**不可重放**：round-1 检索本身——该项按模板 §6 将
如实签 REPLAY_FAILED(search-replay)，这正是状态停在 ROUND1_SCOUT_COMPLETE 的原因。

## 7. 状态纠偏与 supersession 声明（P0.1）

- 「Survey v2 complete / 调研收官」（commit 233dc7e 提交信息、续36、Research-Objective open item 1）
  → **ROUND1_SCOUT_COMPLETE**。
- 「Stage-1C 决策包待 owner 选题」→ **PRE_STAGE1C_DECISION_DRAFT**；owner 已接受门控：P0+P1 关闭、
  申请并通过 STAGE1C_DECISION_READY 后方提请选题。
- 5 kill 的方向性裁决保持（I1 机制占据的证据经全文重算后**更强**），证据等级按 §3.8 封顶。
- 协调者更正自身记录：2026-07-14 早间「关键路径=Stage-1C 选题，随时可开始」的表述**错误**，由本信
  与续38 supersede。

## 8. P1 承诺（Stage-1C 提请前必须关闭；不自动滚入）

9 个既有饱和目标 + §5 的 8 篇新目标（backward/forward chase + 方法别名查询，**按模板 §2.2/2.3 全程
捕获 raw response——未来轮次构造性可回放**）；I1–I4/strict-I2/UMBRELLA 冻结 identity contract + post-hoc
条件日志；SOTA cards 降名重建为同协议 comparator cards；C1 尝试普查 + C4 负结果普查；载重更正与
5 kill 的固定版本+定位器人类双审；未参与生成的独立 reviewer 从 bundle 盲重建五项。

## 9. 签署

```yaml
signoff:
  survey_lead: { id: "Claude Fable 5 (coordinator session 5b49a62b)", verdict: "ACCEPT_MAJOR_REVISION_WITH_FOUR_EVIDENCED_CONTESTS; P0 executed; P1 committed", signed_at_utc: "2026-07-14" }
  independent_reviewer: { id: "PENDING (P1-6 盲重建后签署)", verdict: "", signed_at_utc: "" }
  integrity_reviewer: { id: "owner (Bambipns) — adjudications of record: P0 authorized post-verification; Stage-1C gating accepted", verdict: "recorded via AskUserQuestion 2026-07-14", signed_at_utc: "2026-07-14" }
  unresolved_blockers: ["P1 全部", "round-1 raw responses 永久缺失（REPLAY_FAILED(search-replay) 如实保留）", "2 UNVERIFIED cites (2512.10170/2512.10403)"]
  maximum_permitted_claim: "NO_DIRECT_MATCH_WITHIN_LOGGED_SCOPE（附 §4.3 收窄措辞）；全部 directional-only/hypothesis-grade"
```
