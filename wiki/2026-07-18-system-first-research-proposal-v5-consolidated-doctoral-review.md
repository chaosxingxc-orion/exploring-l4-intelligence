---
artifact_id: "STAGE1A-V5-DOCTORAL-REVIEW-2026-07-18-01"
title: "System-first Research Proposal v5 合并送审版——Stage-1A 尾门博导复审、文献红队与诚信裁决"
date: 2026-07-18
reviewed_artifact: "wiki/2026-07-18-system-first-research-proposal-v5-consolidated.md"
reviewed_commit: "c2b9299be4e0c662fcedbfdd18cf7df1430a7fd7"
reviewed_git_blob_sha256: "2ad5434f8be754621367b0067d44a0eca5828433489e23446258137ade8cbcd4"
review_role: "严格审稿人 / 博导 / 学术诚信敌意复核"
verdict: "WITHHOLD_STAGE1B_SURVEY_EXECUTION_PENDING_MAJOR_REVISION"
stage_verdict: "CURRENT_STAGE = Stage-1A survey-ready gate；申请进入 Stage-1B systematic mapping；任何模型复现、smoke 或任务指标运行均属 Stage-2A"
integrity_verdict: "FFP_NOT_ESTABLISHED；MATERIAL_COMPLETION_STATE_AND_CLASSIFICATION_QRP_ESTABLISHED；若已知缺口经本轮指出后仍继续以“全量/唯一/零项”对外陈述，应升级为疑似故意隐瞒调查"
change_policy: "本评审只新增日期审查报告；未修改被审提案、台账、脚本或任何研究仓文件"
---

# System-first Research Proposal v5 合并送审版复审

## 0. 执行摘要与裁决

**裁决：暂缓签署 Stage-1B survey execution。** 本件相较 v4 有实质进步：阶段正典已纠正，Stage-1B
明确为不触模型的 systematic mapping；system-control 13 轴已经建立；known-item 八项完成全文 DFS；
Stage-2A 被明确写成无执行力预告；九项 bundle-only 门禁在被审 commit 的干净 archive 中由本评审
独立重放为 **9/9 PASS**。因此，本轮**不以“尚未完成系统综述”或“没有实验结果”退稿**，也不要求
团队在 Stage-1B 前运行任何模型。

但是，签署前仍有三项 Gate MAJOR：

1. 提案把一个 frontmatter 明载“W4 未扫描”的 exposure union 称为“项目历史模型触碰全量登记”；
   W4 独立仓实际存在大量未入 union 的模型实验与更正记录，故 `27` 不是项目全集，只能是下界。
2. 已检视八项中，Selective TTS 明确以 LLM judger 产生的不可验证 reward 信号对显式候选池分阶段
   剪枝，本件却同时写它“全系统零训练、label-free LLM-judge 对 K 池选优”，又写“零项做
   training-free reward 信号引导冻结核 K 池选择”。这不是术语偏好，而是直接自相矛盾并会虚增
   新颖性空位。
3. v5 声称其“全量 claim-evidence 矩阵”是 v4 矩阵，但该矩阵 frontmatter 明确只覆盖 v4，且没有
   v5 新增的 ATLAS、ToolGate、Selective TTS、DREAM 等承重数字和系统级综合结论。

这三项均可在 **Stage-1A 内通过文档、台账和编码修订关闭**，不需要模型调用。关闭后，本评审倾向
批准进入 Stage-1B；在关闭前，门禁脚本全绿不能替代科学语义正确性。

## 1. 当前究竟处于哪个阶段

### 1.1 现行阶段正典

依 `wiki/Research-Methodology.md` 2026-07-18 dated supersession 与
`wiki/Research-Objective.md` 的当前状态，阶段应按活动目的与证据用途判定：

| 维度 | 本轮判断 | 理由 |
|---|---|---|
| 当前活动 | **Stage-1A survey-ready gate** | 问题树、协议、查询、路由、哨兵、编码 schema、定向全文核验与静态门禁准备 |
| 尚未开始 | **Stage-1B systematic survey/mapping** | systematic discovery query 仍声明为 0；第一条正式查询才是 1B 起点 |
| Stage-1B 禁止 | 模型 smoke、任务指标、headroom、accuracy/WER、方法比较 | Stage-1B 只生产文献与知识证据 |
| Stage-1C | 证据综合、3–5 候选问题卡、owner 选题、冻结复现清单 | 不用临时实验为候选方向“拉票” |
| Stage-2A 起点 | **先复现最近邻，再做方向性原型** | 即使只跑一个 item 或 smoke，也算实验与 exposure |

因此，历史模型已经被触碰并不把**当前活动**自动改名为 Stage-2；它要求的是 exposure 诚实记账、
后续验证集隔离和证据降级。反过来，“本轮新增模型触碰为 0”也不能抹掉历史触碰。

### 1.2 是否越阶段

**未发现本件本轮越阶段运行研究模型的证据。** §4 的定向全文 DFS、离线 matcher 压力测试、引用
解引用和 §6 的纸面复现草案均可在 Stage-1A 合法进行。§6 明写“现无执行力”，没有提前实施
Stage-2A。§5 也正确禁止 Stage-1B 触碰模型。当前不应加入预算 cap，也不应要求等预算实验；资源
记录与预算约束不是一回事。

本轮的问题不是“做得太多”，而是**部分前置知识账和分类账尚不可信，不能带病进入正式 mapping**。

## 2. 审查对象、方法与可回放核验

### 2.1 冻结对象

- 被审 commit：`c2b9299be4e0c662fcedbfdd18cf7df1430a7fd7`。
- 被审文件 git-blob SHA-256：`2ad5434f8be754621367b0067d44a0eca5828433489e23446258137ade8cbcd4`。
- exposure union git-blob SHA-256：`7ed9e57e04fc5aa966b38db4a058b4f7e7ae8dcccbfe9eb8974e4c39e56b71f8`。
- 评审未把当前工作树内容当作 hash 正典。

### 2.2 独立回放

在 `git archive HEAD` 生成的干净副本 `/tmp/l4-v5-review.KbFRDH` 中，使用 WSL2
`Ubuntu-24.04`、Python 3.12.3，零联网运行九项 bundle-only 命令：

| 检查 | 独立结果 |
|---|---|
| package summary / fail-closed gate | PASS |
| mutation harness | PASS，10/10 |
| record validator | PASS，26/26 |
| route adjudication | PASS，50 routes、0 violations |
| sentinel recall | PASS，34 项、0 unresolved |
| query compiler | PASS，65 queries / 14 lanes |
| child-query replay | PASS，10/10 |
| real-row dry-run | PASS，17/17 |
| route validator | PASS，12/12 |

该结果只证明协议结构、计数、matcher 与 validator 在其能力包络内可回放；不证明文献分类正确、
外部数字已复算，也不证明不存在未纳入扫描面的历史事件。

### 2.3 文献复核范围

本评审复核了 v5 的七篇 component prior、八篇 system-control known item、v4 的 18 条参考文献，
并用官方 arXiv/ACL Anthology 页面对额外直接邻近工作做压力 survey。补充项用于检验“检索协议能否
发现”和“当前空位措辞是否稳健”，不冒充 Stage-1B 已完成的系统综述。

## 3. 多轮对抗式评审

### Round A：阶段攻击

**攻击：**团队已经全文深读多篇论文并写出 Stage-2A 候选，实际上已经越过 Stage-1A。

**对团队最有利的反驳：**不成立。Stage-1A 必须做定向校准和 known-item 深读，否则无法知道正式
mapping 的 schema 是否能编码最近邻；纸面复现 shortlist 也可以提前准备，只要不执行。

**再裁：**本件在阶段边界上通过。不得因为本轮被退回而要求团队补跑 smoke；那会制造真正的阶段
污染。

### Round B：历史 exposure 全量性攻击

**攻击：**§2.2 的“项目历史模型触碰全量登记：27 事件”不成立。

**对团队最有利的反驳：**union frontmatter 与正文主动写了“W4 仓未扫描”的 known gap，说明团队
没有删除该缺口，且 W4 最新实验 commit 早于 gate-freeze commit `af96a89`；本评审未发现
2026-07-16 冻结后 W4 新实验提交。故“本轮新增触碰为 0”的 attestation 未被现有证据推翻。

**再攻击与裁决：攻击成立，Gate MAJOR。** “披露一个缺口”和“完成全集”不能同时为真。W4 仓
`projects/speech-mllm-omni-embedding-rl` 在本机可访问且工作树干净；其
`docs/experiment_inventory.md` 至少记录了以下未被 27 行 union 逐件覆盖的实验族：SLURP 500
formal selector、MInDS formal selector 与 low-margin verifier、URO-Bench 200 多种 selector、
HeySQuAD 200/109、CoVoST2 1758 validation 与 1695 locked test、Jina omni-small 跨模型检查、
WenetSpeech-Wu 路由等。W4 还保存了 MInDS 旧 JSON 手工组装、数值不匹配、同池 exemplar 污染和
后续 clean redo 的更正链。这些恰是未来 held-out 设计必须知道的 exposure。

因此：

- `27` 目前只能写成 `known lower bound >=27`，不能写“项目全量”；
- “~11 模型 / ~72 键”同样不能当全集；
- `new_model_touches_since_gate_freeze=0` 只能保留为覆盖四个独立仓与外部运行面的团队签字
  attestation，不能由 W1/umbrella 在场日志推导成机器证明；
- W4 全量考古完成前，不得冻结后续 fresh/held-out 切分。

### Round C：证据矩阵能力包络攻击

**攻击：**v5 frontmatter 所称“全量矩阵”并不覆盖 v5。

**对团队最有利的反驳：**v5 大量内容来自 v4 更正版和 known-item DFS，读者可以沿指针追到原文件；
外部数字也被统一声明为 `SOURCE_REPORTED_TRACEABLE`，没有声称独立复算。

**再裁：攻击成立，Gate MAJOR。** `2026-07-18-sf-v4-claim-evidence-matrix.md` 的 artifact title、
scope 与表格均明确只覆盖 v4。其 §3 没有逐项列出 v5 的以下数字或 locator：

- ATLAS 的 `88.9%`；
- ToolGate 的 `60.0` 及工具调用变化；
- Selective TTS 的 `τ=0.55`、`α=0.6/0.8`、顶部 `τ=-0.15`、`61.64→65.86`；
- DREAM 的早停比例；
- “八项中五次冻结核心不等于 TF-Strict”“唯一 reward-guided K 池”等综合结论。

指向 DFS 文件不是逐 claim 矩阵。v5 必须有自己的 matrix，或把 frontmatter 改成准确的“v4 矩阵+
v5 补充矩阵”。每个数字至少给出 paper/version、page/table/figure/section、证据模式、是否复算、适用
任务/模型/样本条件；每个跨论文占据判断标 `REVIEWER_INFERENCE` 并列出参与运算的逐篇编码。

### Round D：reward/训练/信息边界新颖性攻击

**攻击：**“八项中零项做 training-free reward 信号引导冻结核 K 池选择；唯一 reward-guided K 池
是 trained-PRM DREAM”通过术语重命名排除了 Selective TTS。

**对团队最有利的反驳：**团队可能把 `reward` 狭义定义为 verifiable scalar reward 或显式 trained
reward model，而把 LLM-as-judge 叫“选择信号”；Selective TTS 又是多 agent、视觉数据分析、过程
剪枝，并非本项目的单一 frozen speech/omni 核。

**再裁：攻击成立，Gate MAJOR。** 官方论文把 Selective TTS 明确描述为由 reward signals 引导的
TTS，并以 process-specific judgers 对分阶段候选池剪枝；本项目自己的 DFS 又把它编码为“全系统
零训练”“label-free LLM-judge 对显式 K 池选优”“镜像本项目 label-free proxy S”。在未预先冻结
reward taxonomy 的情况下，不能在总结句中临时把同一个 judge score 从 reward 集合中排除。

这不会证明本项目没有创新：Selective TTS 仍是多异构模型、非 speech、主观不可验证 reward、过程
剪枝；项目的 single-core black-box omni system 交集仍可能稀疏。错误在于把**交集差异**写成
**reward 轴无人占据**。

同时，现有 13 轴还混淆了三个不同问题：

1. **训练依赖**：核心权重、外部 evaluator/reward model、controller 参数是否被更新；
2. **开发标签依赖**：controller 搜索、prompt/配置选择、judger 选择是否用独立 dev/calibration gold；
3. **测试信息边界**：当前 test item 的 gold 是否进入推理回路，或推理期是否主动取得新外部信息。

AutoTTS 用独立搜索集 gold 发现 controller、Team of Thoughts 用交叉 calibration gold 建画像，可以
被编码为 `development_label_dependent` 或不满足项目的严格 all-system-data-free 身份；但在 held-out
test gold 被隔离时，不能写成 `test-item new-info leakage`。DeepVerifier 也必须按“主实验 prompt-only
零训练路径”和“开源 SFT 变体”分行，不能以整篇论文为一个混合身份后计数。

最低限度应把 `reward_source` 拆为：verifiable utility、rule reward、learned RM/PRM、LLM judge、
consensus/MBR、self-confidence/log-likelihood、human-aligned proxy；并把“是否 reward-guided”作为
该预注册 taxonomy 的派生字段，而非人工自由文本裁决。

### Round E：漏文攻击与检索协议反证

**初始攻击：**known-item 只有八项，漏掉多篇直接工作，故 65 查询协议失败。

**对团队最有利的反驳：部分成立。** v5 已明确八项只是已检视集合，不是文献全集；Stage-1B 尚未
执行。对五篇 arXiv 直接邻近工作的官方摘要使用当前冻结 matcher 做离线压力测试，结果均有非空
命中：CATTS→`SF-L2-Q1`；General AgentBench→`SF-L2-Q1`,`SF-L12-Q3`；PiCSAR→`SF-L5-Q1`；
Sampling for Quality 与 EBD→`SF-L2-Q4`,`SF-L5-Q1`。因此，“现在没列”不能直接推出检索协议漏检。
ACL 2026 项也有 READY venue route，题名含 test-time/agent/agentic 等冻结词项。

**再裁：不把漏文整体升级为新的 pre-Gate MAJOR，但建立 Stage-1B 首批强制队列。** 下列工作已由
本轮评审成为 reviewer-known item；不得在正式 mapping 中依赖偶然排序后才阅读，也不得据当前八项
继续写全域“唯一/零项”：

| 优先级 | 工作 | 必须回答的占据/边界问题 | 当前协议压力测试 |
|---|---|---|---|
| P0 | [Agentic Test-Time Scaling for WebAgents / CATTS](https://arxiv.org/abs/2602.12276) | 多步 web agent、vote uncertainty 驱动动态 compute；和 ATLAS/停止轴的关系 | `SF-L2-Q1` 命中 |
| P0 | [Benchmark Test-Time Scaling of General LLM Agents](https://arxiv.org/abs/2602.18998) | sequential context ceiling、parallel verification gap；是 RQ-SYS 的强负结果 prior | `SF-L2-Q1`,`SF-L12-Q3` 命中 |
| P0 | [PiCSAR](https://arxiv.org/abs/2508.21787) | training-free K-pool selection，但依赖 joint log-likelihood，属 gray-box comparator | `SF-L5-Q1` 命中 |
| P0 | [Sampling for Quality](https://arxiv.org/abs/2604.16453) | training-free reward-guided SMC decoding；需内部概率/前缀 reward，非严格黑盒 agent | `SF-L2-Q4`,`SF-L5-Q1` 命中 |
| P0 | [Energy-Based Decoding](https://arxiv.org/abs/2605.28020) | frozen model + external reward model 的 training-free 声称；必须审外部 RM 的训练来源 | `SF-L2-Q4`,`SF-L5-Q1` 命中 |
| P0 | [BrowseConf](https://aclanthology.org/2026.findings-acl.21/) | verbalized confidence 驱动 retry/stop，直接覆盖 agent 时序控制 | ACL 2026 route |
| P1 | [Agentic Rubrics as Contextual Verifiers](https://aclanthology.org/2026.acl-long.697/) | 上下文化 verifier 为并行 TTS 提供 reward signal；非 speech | ACL 2026 route |
| P1 | [AgentV-RL](https://aclanthology.org/2026.findings-acl.1156/) | tool-augmented agentic verifier，但 verifier 经 RL 训练，是 trained comparator | ACL 2026 route |
| P1 | [Timely Machine](https://aclanthology.org/2026.acl-long.211/) | wall-clock budget、工具延迟与策略适配；方法含 SFT+RL | ACL 2026 route |
| P1 | [FS-Researcher](https://aclanthology.org/2026.acl-long.288/) | 文件系统外部记忆、跨 session 状态、长程 agent TTS | ACL 2026 route |

上述队列是 **Stage-1B 的阅读/编码任务，不是 Stage-2A 复现实验清单**。首批全文编码后再由证据强度
和与本项目身份的距离决定是否进入 Stage-2A reproduction shortlist。

## 4. 引用与事实逐项审计

### 4.1 做对的部分

- 已抽查的论文 ID、题名和稳定链接未发现虚构；八项 known-item 的基本身份均可由官方来源确认。
- ToolGate 是 trained controller、DREAM 使用 trained PRM、DeepVerifier 主实验有零额外训练路径、
  Selective TTS 使用 LLM judger 等大方向编码基本有据。
- 外部数字被降为 `SOURCE_REPORTED_TRACEABLE`，没有再声称九项脚本可以独立复算论文实验。
- “八项零 speech/audio”明确限定为已检视集合，没有直接冒充文献全集结论。

### 4.2 必须更正的引用问题

1. **ATLAS 88.9% 缺条件。** 该值不是无条件“88.9% 轨迹恰在收敛点停”。应至少写明它来自
   GPQA-Diamond，并限定于有可定义正确多数收敛点的 790 条轨迹；否则读者会把一个条件子集统计误读
   为跨基准总体比例。
2. **v5 不自包含。** frontmatter/§0 称“自包含”，末尾却写“参考文献见 v4 附录 A，本件不重复”。
   二者只能保留一个。正式 reviewer-facing 合并件应内含自己的完整 references，或删除“自包含”。
3. **v4 附录仍不完全满足作者要求。** 三条 ACL 记录的作者栏只写“ACL Anthology 记录”，不是作者；
   合并件应从官方条目补齐作者、年份、venue/DOI 或稳定链接。
4. **数字 locator 不得只写“见矩阵 §3”。** 在矩阵尚未包含 v5 新数字时，该指针是空承诺。修订后
   可以保持散文简洁，但矩阵必须逐 claim 可定位。
5. **论文级身份必须改成方法路径级身份。** 一篇论文同时含 prompt-only 主方法和 SFT 变体时，
   `paper = trained/untrained` 的单值编码会制造假计数。

## 5. 阻断问题与验收条件

### P0-1：exposure union 不是项目全集

**风险：**未来验证集可能复用已看过的 item、任务、模型或调参轨迹；历史负结果和诚信更正可能在
Stage-1B 综合中消失；后续“预注册/held-out”只剩形式。

**通过条件：**扫描 W1–W4 四个独立仓的 git 历史、`_repro/`、实验 inventory、MLflow/运行清单和
archive；以“事件”而非散文结果行去重；逐件记录日期、模型、数据 item/split、配置选择用途、结果
工件、commit/blob、是否 superseded、是否存在信息泄漏。W4 旧 MInDS 手工 JSON 与 clean redo 必须
并列保留。完成前把计数写为下界；完成后由团队签字 attest 外部未入仓运行面的边界。

### P0-2：reward、训练与信息边界分类不封闭

**风险：**同一个 LLM judge 可以在逐篇表中叫 reward/proxy，在新颖性总结中又被排除；dev gold
依赖可以被误报成 test leakage；论文混合路径可以被计成对项目有利的单一身份。最终 occupancy map
将不可复核。

**通过条件：**先发布机器可读 taxonomy，再重编码八项与本轮新增 P0 邻近项。至少包含：

- `core_weight_update`；
- `external_component_weight_update`；
- `controller_program_or_config_optimized_on_labels`；
- `human_or_dev_label_model_selection`；
- `deployment_label_access`；
- `test_item_gold_access`；
- `inference_external_new_information`；
- `score_type`；
- `model_access_level`；
- `method_path_id`。

修订后不得保留“已检视八项零 training-free reward-guided K-pool”原句；应写成按 reward 类型和项目
身份合取后的精确占据表。

### P0-3：v5 claim-evidence matrix 缺失

**风险：**下一位 AI 会把 v4 矩阵错误当作 v5 全量证据，并把没有 locator 的综合判断升级为已核验
事实。

**通过条件：**新增 v5 supplement 或完整 v5 matrix；自动检查 proposal 中全部百分比、区间、倍数、
“唯一/零项/五次”等量词均有 claim ID；每一 claim 的 source locator、证据模式、适用范围、复算
状态与推导输入齐全。矩阵版本必须在 frontmatter 明确指向 v5。

## 6. 重要但不单独阻断的修订

### P1-1：补全自包含 references 与 ATLAS 限定语

按 §4.2 修订。若保留“自包含”，引用表必须随 v5 在同一文件中；不能要求评审先找 v4 再找 DFS
再找矩阵才能知道一个数字来自哪里。

### P1-2：Stage-1B 首轮 carry-forward 队列

把 Round E 的十项登记为 `REVIEWER_KNOWN_ITEM`，分别记录 query/route guarantee 和发现 provenance。
这不要求修改冻结查询，也不把 reviewer-known item 冒充 query recall 成果。执行首轮先编码、再进入
正常 BFS/DFS 排序。

### P1-3：把空位语言降到正确证据等级

在 Stage-1B mapping 收敛前，只允许写：

- “在当前已检视集合中未见……”；
- “该交集仍是待检验候选空位”；
- “Selective TTS / PiCSAR / SMC / EBD 已占据哪些组件轴，但未占据哪些 system/speech/black-box 轴”。

禁止写无集合限定的“唯一”“零项”“持续缺位”，也禁止从“现有多模态 TTS survey 不含 audio”推出
全领域 speech/omni 空位。

## 7. 学术诚信裁决

### 7.1 已建立的事实

- exposure union 明知 W4 未扫描，却在 v5 被称为“项目历史全量登记”；这是可证实的完成态误报。
- v5 的全量证据矩阵声明超出该矩阵实际 scope；这是可证实的证据包络误报。
- Selective TTS 的逐篇编码与跨篇总结自相矛盾；这是可证实的分类/新颖性表述缺陷。
- W4 历史中确有手工组装结果文件、数字不一致和 transductive exemplar 污染；但 W4 inventory 已主动
  标记 superseded 并保留 clean redo，故该历史事件本身不能被本评审倒推出当前团队仍在伪造。

### 7.2 尚未建立的指控

本轮没有发现伪造论文、虚构作者/ID、篡改原论文、删除 W4 更正记录或 gate-freeze 后秘密新跑模型的
直接证据；也没有证据证明 exposure 漏登出于故意。因此当前裁决是：

**`FFP_NOT_ESTABLISHED`，但 `MATERIAL_COMPLETION_STATE_AND_CLASSIFICATION_QRP_ESTABLISHED`。**

不能因为“缺口在别处披露过”就免除 v5 的错误，也不能仅凭错误直接指控 fraud。下一步关键是行为：
若团队在收到本报告后仍不扫描可访问的 W4，却继续用“全量”；或在 reward taxonomy 已明确后仍通过
重命名排除 Selective TTS/PiCSAR/SMC/EBD 等先例，则应启动有意隐瞒/新颖性操纵的独立调查，而不再
把它当普通写作疏漏。

## 8. 严格整改计划（全部在 Stage-1A 内，无模型运行）

| 顺序 | 动作 | 交付物 | 机器/人工验收 | 截止门 |
|---|---|---|---|---|
| 1 | W1–W4 exposure 考古与去重 | dated union v2 + 四仓扫描清单 + 未入仓边界 attestation | 随机抽查证据指针；W4 inventory 每个实验族均有映射或排除理由 | Stage-1B signoff 前 |
| 2 | 冻结 reward/training/info taxonomy | schema + 枚举定义 + 冲突规则 | Selective TTS、AutoTTS、Team of Thoughts、DeepVerifier 四个反例单测 | signoff 前 |
| 3 | 按 method path 重编码 known 8 | system-control DFS v2 / dated correction | 派生计数可由表自动重算；无自由文本“唯一” | signoff 前 |
| 4 | 建 v5 claim-evidence matrix | v5 matrix + proposal claim IDs | 全部数字/量词零 orphan；locator 抽查 | signoff 前 |
| 5 | 修正引用 | v5 自包含参考文献、ATLAS 条件、ACL 作者 | 官方链接/作者/年份/DOI 抽查 | signoff 前 |
| 6 | 登记 reviewer-known 首批 | Stage-1B first-batch ledger | 五篇 arXiv matcher 命中留痕；ACL route guarantee 留痕 | 可随 signoff 批提交 |
| 7 | 干净 archive 复跑 | 新 commit 的 9 项复跑记录 | 9/9 exit 0；明确仅为结构重放 | 最终重申请时 |

明确禁止把整改扩展为模型实验、smoke、复现结果或预算对比。Stage-1B 获签后仍只做 survey；
Stage-1C 才冻结复现对象；Stage-2A 才实际复现。

## 9. 重新签署的最小清单

- [ ] exposure union 不再同时出现“全量”和“W4 未扫描”；W4 已完整映射，或计数明确写下界；
- [ ] W4 的历史诚信更正、污染样本与 supersession 全部进入 exposure；
- [ ] reward/training/dev-label/test-gold/new-info 分轴定义并机器可读；
- [ ] Selective TTS 不再被从 reward-guided 轴无定义排除；
- [ ] AutoTTS/Team of Thoughts 不再被误写成 test-item gold leakage；
- [ ] DeepVerifier 主路径与 SFT 变体分行；
- [ ] v5 新数字和综合结论全部进入 v5 claim-evidence matrix；
- [ ] ATLAS 88.9% 补 GPQA-Diamond/790 条有定义收敛点的条件；
- [ ] v5 真正自包含，或删除“自包含”声明；
- [ ] Round E reviewer-known item 进入 Stage-1B 首批保证队列；
- [ ] 新冻结 commit 的九项 bundle-only 门禁仍为 9/9 PASS；
- [ ] owner 重申：Stage-1B 全程不得运行研究模型或 smoke。

在上述清单关闭前，裁决维持 **WITHHOLD**。关闭后，不应以“还没得到实验效果”继续阻断 Stage-1B；
此门只批准系统综述执行，不背书创新性成立、方法有效或任何 SOTA 声明。
