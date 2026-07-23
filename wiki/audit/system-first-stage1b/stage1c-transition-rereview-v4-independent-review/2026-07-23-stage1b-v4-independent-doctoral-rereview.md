---
review_type: "independent doctoral adversarial rereview"
review_date: "2026-07-23"
campaign: "system-first-stage1b"
review_target: "stage1b-v4-targeted-repair-and-stage1c-transition-rereview"
review_target_commit: "f11a2b1fd0b6d81b08caefc5d576fe13ed579883"
stage_diagnosis: "STAGE_1B_LATE_CLOSEOUT; STAGE_1C_NOT_YET_AUTHORIZED"
verdict: "WITHHOLD_WITH_BOUNDED_DEFECTS"
stage1c_authority: "NOT_GRANTED"
model_or_benchmark_execution_performed: false
source_delivery_modified: false
---

# Stage-1B v4 独立博导级复审：Stage-1C 转段暂缓，缺陷已收敛为两个结构性闭环

## 一、最终裁决

**裁决：`WITHHOLD_WITH_BOUNDED_DEFECTS`。当前仍是 Stage-1B 后期收尾，不得把本报告解释为
Stage-1C 已经开始，也不得据此开展模型调用、benchmark 计分、方案原型、候选排序或技术路线
选择。**

这不是对 v4 的全面否定。相反，v4 已经真实修复 v3 的四项既知 P0：固定提交有效、60 项
manifest 可回放、70 个全文路由均能解析到本地字节并通过 SHA-256、九个指定先验完成身份复用、
三层资产快照也不再把冻结 baseline 冒充整盘实时清单。团队对不可获得资产的陈述总体诚实，
没有把相邻数据集替代成目标数据集，也没有制造模型实验结果。

但在准备签署 Stage-1C 时，本次复审发现了两个新的、可复现的结构性缺陷：

1. **既有论文全集在“发现/读过”到“current bibliography / strict supplement / 本地全文账本”之间
   发生信息丢失。** AudioJudge、SpeakerSleuth、ParaPairAudioBench、Audio-Aware LLM Judges 等
   已经出现在团队 2026-07-14 的检索与全文阅读日志中，并且部分已经进入 canonical corpus
   disposition；然而它们没有进入当前 bibliography、39-row strict supplement、转段 reference
   appendix 或本地全文 ledger。UniSRM 也在早期审查和搜索记录中出现，却未被 v4 的九篇
   reconciliation 吸收。这会直接使 evaluator/reward-reliability bundle 的 Stage-1C 输入失真。
2. **同一 release 中两个“官方”资产清单生成器语义不一致。** PowerShell 生成器能在当前磁盘
   回放出 31 个 frozen baseline、33 个 candidate、5 个 auxiliary，与冻结 JSON 完全一致；Python
   生成器却输出 frozen 30、candidate 34，并把实际存在且已锁定的
   `repos/slurp/scripts/audio` 报为 missing。仓库规定 WSL2 是标准运行环境，因此“Windows 版本正确、
   portable Python 版本错误”不能被当作无关紧要的跨平台细节。

只要团队完成本文第十一节的窄修复，不需要重启大规模 survey，也不需要跑任何模型实验；修复后
可以进行一次仅针对这些 gate 的独立复核。

## 二、阶段判断

当前阶段是 **late Stage-1B closeout / Stage-1C transition candidate**，不是 Stage-1C。

依据如下：

- `wiki/Research-Objective.md` 明确把当前状态写成 late Stage-1B closeout，并规定正式 Stage-1C
  仍需独立审稿人签名；
- v4 proposal 自身只请求 `SIGN_STAGE1C_COMMON_RUBRIC_COMPARISON`，没有请求模型或实验执行权；
- 本轮交付物的实质是 method-path、evidence depth、prior reconciliation 与 asset feasibility，
  没有产生项目自己的 benchmark 指标、复现结果、原型结果或技术方案优胜结论；
- 按本项目阶段定义，Stage-1B 负责方法路径和相近性地图，Stage-1C 才能在候选 gap hypothesis
  之间做统一量表比较与问题选择，Stage-2A 才以复现作为方案探索的第一步。

因此，本轮下载公开论文、数据与代码用于可得性核验不构成越级实验；但在 Stage-1C 签署前，任何
以这些资产运行模型、计算任务指标、做 smoke benchmark 或据此选择问题的行为都仍然越界。

## 三、审查方法与证据边界

本次复审遵循“仓内全集优先、官方源反查、固定提交与本地字节直接回放”的顺序：

1. 读取当前研究状态、项目 thesis、v4 proposal 和 manifest-bound 交付物；
2. 验证完整提交
   `f11a2b1fd0b6d81b08caefc5d576fe13ed579883` 是真实 Git commit 且为当前 HEAD 祖先；
3. 从固定提交逐项读取 manifest 中 52 个 Git blobs，并核对 8 个 external artifacts，共 60/60；
4. 对 81-row coverage、70 个全文路由、九个 reconciliation prior、39-row supplement 和
   25-row direct-control basis 做独立交叉检查；
5. 在当前标准数据根直接核对 PDF、代码 commit、HF revision、文件数、字节数和 archive hash；
6. 在 WSL2 `Ubuntu-24.04` 的项目 venv 下复跑相关测试和 v4 evidence contract；
7. 用团队既有 corpus/search log 反查知识是否进入 current layer，再用 arXiv、ACL Anthology 等
   官方论文页做有边界的外部反查。

本轮没有执行模型/API、没有生成数据集指标、没有 smoke benchmark、没有复现论文结果，也没有
修改团队的 proposal、current survey、脚本或任何现有源文件。本文件是新增的独立审查记录。

## 四、v4 已经通过的部分

### 4.1 Release identity 与 manifest：通过

- 完整 SHA `f11a2b1fd0b6d81b08caefc5d576fe13ed579883` 存在，不再复现 v3 的非法 SHA；
- manifest 自身 SHA-256 为
  `458150815673ce13ce31ea55214234e226ba512a19a209dca1dee9b457c59ecf`；
- 60 个条目由 52 个 Git artifacts 和 8 个 external artifacts 构成；独立逐项回放为 60/60，
  无 missing、byte mismatch 或 hash mismatch；
- 固定提交到当前 HEAD 之间，manifest-bound 科学交付物没有发生静默漂移；后来生成的
  `release-replay.json` 是针对固定提交的外部回放收据，而不是用自包含 hash 制造循环证明。

### 4.2 81-row evidence depth：通过

- 81 个原始 coverage rows 中，70 个为 `FULLTEXT_ROUTED`，11 个为 `ABSTRACT_ROUTED`；
- 对 70 个全文项，按 ledger 的实际 `stored_at` 路径解析后，70/70 PDF 均存在，文件长度和
  SHA-256 一致；
- v3 中七个被错误标深的对象现在均有 PDF 与 e-print 本地字节，不能再复现“只有 abstract 却称
  full text”的问题；
- 九个 known-prior reconciliation rows 均有本地 PDF 与声明 hash；
- 39-row strict supplement 的 39 个 `fulltext_ref` 均能解析到本地 PDF 且 hash 一致。

这里必须说明一个审查细节：OpenOmni `2408.03047` 和 SpeechRole `2508.02013` 不在
`survey-fulltext/<id>/` 顶层，而在 batch4 子目录。若忽略 ledger 的 `stored_at` 会误报 68/70；按
账本路径回放后为 70/70。团队在这一点上的最终证据是成立的。

### 4.3 九个指定先验的 identity reconciliation：就其声明范围而言通过

Speech-Copilot、AudioGPT、MM-ReAct、EchoChain、From Text to Voice、AuTAgent、WavReward、
SDiaReward、GSRM 均以既有 canonical work identity 被复用，没有为同一论文制造第二个 claim
work。MM-ReAct 与 AuTAgent 只做 routed-only boundary，也没有被计入 25 个 direct methods。

但是，“九篇指定先验已闭环”不等于“既有 corpus 已充分利用”；后者正是本轮新的 gate defect，
见第六节。

### 4.4 25-row control basis：基本通过

团队明确区分了 `DIRECT_CONTROL_METHOD` 与 reward-guided selection：

- external orchestration only：9；
- state/event gated：9；
- evaluator/verifier gated：7；
- reward-guided selection：0。

这个结论比早期把 selector/evaluator/reward 混为一谈严谨得多。25 个 direct rows 都没有项目所称
核心模型权重更新，且没有把“接受音频输入”自动等同于“可靠 evaluator”。

有一个低等级术语问题：`reward_or_evaluator_identity` 在 orchestration rows 中被填入
“ChatGPT coordinator”“modular speech tools”等并非 reward/evaluator 的组件。由于每行还有
`control_basis` 和 boundary note，这暂时不会改变计数，但下版 schema 应改成更中性的
`control_signal_or_decision_component_identity`，或按 control basis 使用分类型字段。

### 4.5 主资产快照与当前磁盘：通过，但生成器不一致

使用 manifest 声明的 PowerShell producer 对当前数据根重放：

| Layer | 冻结 JSON | 2026-07-23 当前磁盘重放 | 结果 |
|---|---:|---:|---|
| `FROZEN_BASELINE` | 31 | 31 | 一致，0 missing |
| `LOCAL_CANDIDATE_UNFROZEN` | 33 | 33 | 一致 |
| `SURVEY_AND_REPRO_AUXILIARY` | 5 | 5 | 一致 |

所有 entry 的 path、file count、byte total、source identity、revision/fingerprint 与冻结 JSON 一致。
因此，不能再维持“v4 冻结资产数量与磁盘对不上”的指控；v4 的主快照本身是可重放的。

## 五、引用是否合理

### 5.1 已进入 39-row supplement 的引用：总体合理

`stage1b-transition-reference-appendix.md` 对 39 个 supplement rows 提供了 39 个唯一 arXiv ID、
稳定链接、作者/年份、role 与全文定位 anchor；39 个 supplement IDs 无缺失，也没有额外 ID 混入。
VoiceAgentBench、tau-Voice、Full-Duplex-Bench v3、Audio2Tool、Omni-DeepSearch、EVA-Bench、
IHBench、WavReward、GSRM、SDiaReward、EchoChain、From Text to Voice 等引用身份与官方论文页
一致。v4 没有把论文报告结果写成项目复现结果。

### 5.2 引用层仍有两个问题

1. **reference appendix 只覆盖 39-row supplement，没有覆盖 reconciliation 中 routed-only 的
   MM-ReAct `2303.11381` 与 AuTAgent `2602.13685`。** AuTAgent 在 current bibliography 有稳定
   链接，MM-ReAct 甚至没有进入 current bibliography。既然 v4 proposal 正文点名二者，reviewer-
   facing appendix 应提供二者的稳定引用与 boundary role。
2. **引用闭包对“已发现但未提升到 current layer”的论文失明。** 这不是单条 citation 格式错误，
   而是 corpus-to-current 知识组织断裂；见下一节。

## 六、P0：既有论文全集没有被充分利用，且会影响 Stage-1C 比较输入

### 6.1 这是信息丢失，不是外部检索召回不足

团队自己的 `2026-07-14-search-query-log.jsonl` 已经记录：

- AudioJudge `2507.12705`，并记录读取了 EACL 2026 全文；
- SpeakerSleuth `2601.04029`，并记录 K=3 acoustic-variant discrimination 的全文结果；
- Audio-Aware LLMs as Judges for Speaking Styles `2506.05984`；
- ParaPairAudioBench `2606.24648`，并记录 tie-case calibration failure；
- UniSRM 与 SpeechJudge 所在 trained audio-judge/reward-model cluster。

其中前四篇还已经存在于
`wiki/survey/current/data/existing-corpus-disposition-v1.json` 的 canonical work records，状态为
`KNOWN_QUEUE` / `INCLUDE`。但它们在以下四个转段表面上全部缺席：

- `wiki/survey/current/bibliography.md`；
- `stage1b-speech-direct-prior-supplement-v2.json`；
- `stage1b-transition-reference-appendix.md`；
- 本地 fulltext ledger / `survey-fulltext` 字节。

这说明当前知识组织流程只能证明“某次检索找到过”，不能保证“被确认相关的工作一定进入后续比较
输入或以明确理由被排除”。对于项目先前强调的整套论文集复用要求，这是一个 gate-level defect。

### 6.2 最少必须重新对账的论文

以下不是要求无界扩张 survey，而是一个封闭的 reconciliation set：

| 工作 | 官方来源 | 为什么会影响当前 bundle | 初始建议角色 |
|---|---|---|---|
| AudioJudge | [arXiv 2507.12705](https://arxiv.org/abs/2507.12705)，[EACL 2026](https://aclanthology.org/2026.eacl-long.168/) | frozen/prompted audio judge、pairwise evaluation、位置与冗长偏差，直接影响 evaluator reliability | `MEASUREMENT_INSTRUMENT`; 未接入 action 前不是 direct controller |
| Audio-Aware LLMs as Judges for Speaking Styles | [arXiv 2506.05984](https://arxiv.org/abs/2506.05984) | 语音风格/角色扮演的人机一致性，覆盖当前 bundle 中缺失的 paralinguistic judge 轴 | `MEASUREMENT_INSTRUMENT` |
| SpeakerSleuth | [arXiv 2601.04029](https://arxiv.org/abs/2601.04029) | 多轮说话人一致性与 K-variant discrimination，揭示 text-over-acoustics bias | `MEASUREMENT_INSTRUMENT`; 可作为 selection-adjacent comparator |
| ParaPairAudioBench | [arXiv 2606.24648](https://arxiv.org/abs/2606.24648) | pairwise、tie/abstention、校准失败，直接约束“evaluator 可靠即可控制”的假设 | `MEASUREMENT_INSTRUMENT` |
| UniSRM | [arXiv 2605.23261](https://arxiv.org/abs/2605.23261)，[ACL 2026](https://aclanthology.org/2026.acl-long.2150/) | 多维 speech reward、reasoning consistency、UniSRM-Data/Bench；团队早期已点名 | `TRAINED_MEASUREMENT_BOUNDARY` |
| VideoFDB | [arXiv 2605.30256](https://arxiv.org/abs/2605.30256) | 首个 full-duplex AV2AV benchmark；当前“omni”证据几乎全部是 audio-only | `MULTIMODAL_MEASUREMENT_BOUNDARY`，必要时进入 interactive bundle |

另外，SpeechJudge `2511.07931`、SpeechLLM-as-Judges `2510.14664`、From Scores to Preferences、
NoRefER、SpeechQE、MACE、BRACE、CAF-Score、MUGEN 等应进入一个有理由的 route table。它们不必
全部进入 strict supplement，但不得继续以“存在于历史日志或 disposition，所以等于已经利用”来
代替当前 route 决定。

### 6.3 为什么这会阻断 Stage-1C，而不只是成为以后补 citation

Stage-1C 即将比较的三个 eligible bundles 之一就是 evaluator/reward reliability。AudioJudge、
SpeakerSleuth 与 ParaPairAudioBench 分别提供了 frozen audio judge、跨轮声学一致性和 tie/
calibration failure 的关键证据。缺失它们会让 common rubric 低估：

- evaluator 已有能力边界；
- pairwise 相对判断与 pointwise 评分的差异；
- lexical dominance、position bias、verbosity bias；
- tie/abstention 的错误校准；
- “judge-human correlation”与“judge 能否改进下一步 action”的差别。

这不必然推翻 `REWARD_GUIDED_SELECTION = 0`，因为这些论文多数没有把 judge 结果接入下一步控制。
但它会改变 Stage-1C 对 evaluator bundle 的可行性、风险与测量设计，因此必须先进入比较输入。

## 七、语音与多模态智能体覆盖是否完备

结论是：**语音 agent 与 audio-only full-duplex 覆盖已达到 Stage-1B 可用水平；evaluator 轴和真正
audio-visual omni 轴不完备，不能称“覆盖完备”。**

| 覆盖轴 | 当前评价 | 依据与缺口 |
|---|---|---|
| speech tool/agent orchestration | 较强 | Speech-Copilot、AudioGPT、AudioToolAgent、AURA、Audio2Tool、Omni-DeepSearch 等已路由 |
| audio-only full-duplex/task agent | 较强 | tau-Voice、VoiceAgentBench、FDB-v3、EVA-Bench、EchoChain、IHBench 等覆盖 task success、interrupt、latency、state update |
| speech reward/evaluator | 有基础但结构性缺项 | WavReward、GSRM、SDiaReward 已在；AudioJudge、UniSRM、SpeakerSleuth、ParaPairAudioBench 等未进入 current comparison layer |
| training-free external control | 有多类近邻 | orchestration、event/state gate、verifier gate 都有；真正 reward-guided action selection 仍为 0，团队陈述诚实 |
| audio-visual omni/full-duplex | 明显不足 | VideoFDB 未进入 corpus/current/local assets；现有“omni”大多仍是 audio/text/tool，而非 AV2AV interaction |
| evaluator-to-action causal utility | 未闭环 | 当前主要是评价相关性或 benchmark 表现，尚未证明 evaluator 提高下一 action 的真实任务效用；这是 Stage-1C 应比较的问题，不应在 Stage-1B 宣称解决 |

这里不要求 Stage-1B 把所有视觉 agent、GUI agent、robotics agent 都纳入；那会造成范围失控。最低
要求只是：如果 thesis 继续使用 “omni agentic system”，必须把 “omni” 的操作性范围写清楚，
并把 VideoFDB 这类直接 AV2AV 边界纳入或给出可审计的排除理由。

## 八、论文、代码、数据是否已经锁定并下载到本地

### 8.1 论文全文

- 原 81-row coverage：70 个全文本地锁定，11 个明确保持 abstract-only；
- 39-row supplement：39/39 PDF 本地存在且 hash 一致；
- 九个指定 reconciliation prior：9/9 PDF 本地存在且 hash 一致；
- 本报告第六节的 gate reconciliation set：当前均未进入 fulltext ledger，本地标准路径中没有
  对应 PDF。故“相关工作已经全部下载到本地”的回答是 **否**。

### 8.2 代码与数据

v4 的 13 项 asset matrix 对下列资产的陈述可复核：

| 资产 | 本地状态 | 独立核验 |
|---|---|---|
| VoiceAgentBench | 数据 revision-pinned；代码 commit-pinned | 7,663 个远端内容文件、5,833,663,134 bytes；代码 commit 匹配 |
| Full-Duplex-Bench v3 | 数据 content-pinned；代码 commit-pinned | archive 736,136,419 bytes，SHA-256 `37545bd8...d672f`；解压 203 文件、947,535,966 bytes；代码 commit 匹配 |
| Audio2Tool | 数据 revision-pinned；代码仅 remote verified | HF metadata revision 匹配；71,441 个远端内容文件、10,410,773,494 bytes 全部存在 |
| Omni-DeepSearch | 数据 revision-pinned；代码 commit-pinned | 911 个远端内容文件、632,178,405 bytes；代码 commit 匹配 |
| IHBench | 数据 revision-pinned；代码 commit-pinned | 4 个远端内容文件、216,559,546 bytes；代码 commit 匹配 |
| EVA-Bench | baseline locked；代码仅 remote verified | baseline revision 与冻结记录一致；尚无 evaluator code commit pin |
| MMAR / MMAU-mini / SoulX-Duplug | baseline locked | 本地存在，但后者不是 tau-Voice 或 FDB-v3 的替代物 |
| tau-Voice | 仅 tau2-bench code commit-pinned | **精确 voice dataset contract 未锁定** |
| LALM audio-judge study | 论文在现有 supplement | production recordings private，部分 adversarial audio pending |
| EchoChain | 论文在本地 | **未核实公开 code/data** |
| From Text to Voice | generator code commit-pinned | **精确生成语音 corpus 未打包** |

因此，“关键公开可得资产有一部分已经锁定”成立；“所有相关研究内容和数据均已下载”不成立。后者也
不应成为 Stage-1C 的硬要求：不可公开、未打包或许可不清楚的资产应被诚实标记，并作为 rubric 的
feasibility / reproduction blocker，而不是用相邻资产冒充。

### 8.3 Audio2Tool 的额外本地文件不是计数造假，但会污染后续数据加载

Audio2Tool 的固定 HF revision 有 71,441 个正式内容文件，合计 10,410,773,494 bytes；这些文件
全部存在，v4 表内数字正确。当前目录另外存在 610 个非远端清单文件、1,158,458 bytes，主要是
并行下载冲突产生的 `generation_results.1.csv`、`.2.csv`、重复 metadata 与 README 副本；`.hfd`
中还有校验与下载清单。

因此不应把全目录物理文件数 72,062 与远端内容数 71,441 直接比较并指控伪造。但在 Stage-2 前，
数据 loader 必须只读取固定 remote manifest，或把 610 个 extras 隔离；否则递归 glob 可能把重复
记录当成额外样本。此项不阻断 Stage-1C 文献比较，但阻断“可直接复现”的更强表述。

## 九、P1：Python 与 PowerShell 清单生成器不等价

manifest 把冻结 layered inventory 的 producer 标为
`scripts/data/stage1c-asset-inventory.ps1`，该 producer 在当前磁盘能精确复现 31/33/5。与此同时，
release 也纳入了 `scripts/data/stage1c_asset_inventory.py`，并把它描述为 portable implementation。

Python 实现的错误可直接定位到：

```text
locked key = row["local_subdir"]                         # repos/slurp/scripts/audio
observed key = f"{row['kind']}s/{row['name']}"          # datasets/audio
```

它丢失原始 relative path，导致这两个键永远不相等。磁盘上
`${SPEECHRL_DATA_DIR}/repos/slurp/scripts/audio` 实际存在，141,656 files、13,507,477,690 bytes，
且 lock 中 revision 为 `8eb16545762be97ace75334109d73824217311f1`；Python 仍把它列为 missing，
并将其挪入 candidate layer。

当前测试只用 `datasets/<name>` 形式的人工 fixture，未覆盖 `repos/...` 这样的合法 lock path。
团队 receipt 所称的 53 项测试，以及复审在正确 WSL2 venv 下运行八个相关模块得到的 54 项测试，
都能通过；这恰恰说明现有 fixture 没有覆盖真实缺陷，而不是说明真实清单语义正确。

这不是数据伪造，而是 replay contract 不完整。修复前不得宣称两个生成器等价或 Python 版本可在
标准 WSL 环境复现冻结 inventory。

## 十、是否有越过本阶段的探索尝试

**未发现实质越级。**

- 下载公开论文、数据与代码、记录 revision/commit/hash、检查 license/access，属于 Stage-1B
  末期的 feasibility preparation；
- 对 acquisition scripts 和 evidence contracts 做单元测试，不是模型实验；
- v4 没有生成项目自己的 benchmark 分数，没有比较模型优劣，没有宣布 gap 已选择，也没有宣称
  技术创新已验证；
- `DIRECT_CONTROL_METHOD` 与 training-free RL / reward-guided selection 已明确拆开。

需要继续约束的措辞是：

- “complete and pinned”只能指固定远端清单中的内容齐全，不得暗示目录是 clean checkout；
- “coverage”必须带 corpus/route 边界，不得写成 literature-universe closure；
- “omni”必须声明是否包括 AV2AV、GUI、robotics 或只包括 speech/audio/text/tool；
- asset acquisition 不产生 Stage-2 reproduction authority。

## 十一、学术诚信判断

### 11.1 未发现可支持“学术欺诈/故意造假”的证据

本轮没有项目实验结果可供伪造；固定提交、manifest、PDF hash、代码 commit、HF revision、FDB-v3
archive hash 和 PowerShell 主 inventory 都能被独立复核。团队还主动保留了 tau-Voice、LALM、
EchoChain、From Text to Voice 的 unavailable/private/unpackaged 状态，没有使用近似资产替代精确
资产。Audio2Tool 的计数差异也可以由“remote content 与 local auxiliary/extraneous files”解释。

### 11.2 仍存在高风险的学术过程缺陷

如果团队在被指出后仍让已经发现和读过的反例消失在 current layer，并继续用不完整表格支持
“evaluator/reward 方向已有工作不足”或 novelty 叙事，这会升级为选择性引用和证据压制风险。当前
证据更支持“知识组织/提升规则失败”，还不足以断言主观故意。

同样，Python inventory 的错误目前是测试设计遗漏，不是元数据篡改。但修复后必须把真实非标准
路径纳入回归测试，避免以后只用能通过的 fixture 证明自身正确。

## 十二、Stage-1C 放行前的最小修复计划

### Gate A — 既有 corpus 到 current layer 的闭环（P0，必须）

1. 从 `existing-corpus-disposition-v1.json` 与全部既有 search/fulltext logs 生成一个封闭的
   `stage1b-eligible-bundle-reconciliation`，而不是再手工挑九篇；
2. 至少对第六节六篇 gate set 给出 canonical identity、官方 metadata、local PDF/hash、role、
   control basis、bundle impact、asset availability 与 route reason；
3. AudioJudge、Audio-Aware Judges、SpeakerSleuth、ParaPairAudioBench 不得只留在历史日志；
4. UniSRM 必须解释为何此前已知却未进入 current layer；
5. VideoFDB 必须进入 multimodal boundary，或以明确的 omni scope 给出排除理由；
6. 对其余 12 个“既有 corpus 中 speech/audio evaluator 相关但不在 current bibliography”的工作
   给出 INCLUDE/BOUNDARY/EXCLUDE route；不要求全部 D2，但禁止 silent drop；
7. 重新物化 bibliography、strict supplement、reference appendix、mapping 和 eligible inputs，
   并明确说明 direct-control 25 与 reward-guided 0 是否改变。不得为了保持旧计数而强行分类。

验收点：从 canonical corpus 中任一 `INCLUDE` 且命中某个 eligible bundle 的工作，都能机器追踪到
current route 或明确 exclusion；不再依赖审稿人逐个 `rg` 才发现丢失。

### Gate B — inventory producer parity（P0，必须）

1. Python generator 使用原始 `local_subdir` 作为分类键，不得由 kind/name 反推路径；
2. 新增真实结构 fixture：至少包含一个 `repos/...` locked asset、一个 `datasets/...` locked asset、
   一个同名 candidate mirror 和一个辅助目录；
3. 在 WSL2 Python 与 Windows PowerShell 上对同一 fixture 生成规范化 JSON，除 producer/date 外必须
   语义等价；
4. 对当前真实数据根重放，两个 producer 都必须给出 frozen 31、candidate 33、auxiliary 5、
   missing 0；
5. 将运行环境写入 receipt。Windows Python 因 Bash path、依赖和 CRLF 失败不能被误写成脚本逻辑
   失败；标准权威执行环境仍是 WSL2 `Ubuntu-24.04`。

### Gate C — asset content 与目录卫生分层（P1，随 Gate B 完成）

1. 资产表拆分 `remote_content_files/bytes`、`auxiliary_files/bytes`、
   `extraneous_files/bytes`；
2. Audio2Tool 固定记录 71,441 个远端内容文件与 610 个 extras，不删除用户资产；
3. 在 Stage-2 loader 设计中强制使用 revision-bound allowlist，或在获得授权后隔离 extras；
4. 对 HF 数据集说明 `.hfd`、`.cache` 不计入 remote content totals；对 FDB-v3 说明 archive 与
   extracted content 分开计数。

### Gate D — reviewer-facing citation closure（P1，必须随新 release 一起交付）

1. appendix 覆盖全部 reconciliation rows，包括 routed-only MM-ReAct 与 AuTAgent；
2. 新引入论文使用 arXiv/ACL/正式 venue 稳定链接、作者、年份、角色和本地 hash locator；
3. 明确区分 prompted frozen judge、trained reward model、benchmark/instrument 与把 evaluator 接入
   next-action 的 direct controller；
4. 不得把相关性、pairwise accuracy 或 benchmark ranking 直接当成 selection utility。

### Gate E — 一次窄复核，而不是再启动一轮无限 survey

新 release 只需接受以下复核：

- 完整 commit 与 manifest 逐项回放；
- Gate A 的 canonical-to-current 追踪；
- 六篇 gate set 的官方身份、本地全文和分类；
- 两个 inventory producers 的真实数据根 parity；
- 更新后的三个 eligible bundles 是否仍然 unranked，且无 model execution。

若这些点通过，可签署 `SIGN_STAGE1C_COMMON_RUBRIC_COMPARISON`；不应再因为低价值的脚本对抗性、
元数据恶意篡改假设或无限文献扩张继续拖延转段。

## 十三、Stage-1C 获准后建议的 common-rubric checkpoints

这些是 Stage-1C proposal 输入，不是本轮实验任务：

### 13.1 Evaluator / reward reliability

- judge 是否真正访问 load-bearing audio，而不是主要依赖 transcript；
- pointwise、pairwise、listwise 的校准差异；
- tie/abstention 能力、position/verbosity/self-preference bias；
- 跨任务、跨语言、跨噪声与跨模型稳定性；
- judge-human agreement 与 judge-guided next-action utility 分开测量；
- 同核 self-evaluator、外部 frozen evaluator、trained reward model 三类不可混合平均。

### 13.2 Interactive / full-duplex

- task success 与 interaction quality 双主轴，不用单一自然度分数替代；
- interruption detection、state update、resume/recovery、self-correction、barge-in、latency；
- clean audio 到 realistic noise/accent/disfluency 的退化；
- audio-only 与 AV2AV 分层，防止以显式视觉 QA 代表持续视觉流 grounding；
- evaluator 失败是否会诱导错误修复、过早停止或无限循环。

### 13.3 Budget / stop / repair

- budget 是固定次数、时间、费用还是风险预算；
- stop signal 是 terminal environment state、heuristic、uncertainty 还是 evaluator；
- repair 是否真的改变下一 action，还是只做事后解释；
- oracle headroom、realized gain、regret 与 harm 同时报告；
- 在黑盒 core 假设下，外设 controller 的 observation/action boundary 必须可配置和可记录。

## 十四、给研究团队 AI 的最终执行指令

1. 不要跑模型，不要跑 benchmark，不要宣布 Stage-1C 已开始；
2. 不要改写或删除本轮 audit 历史；新建窄 repair release；
3. 先修 corpus promotion closure，再修 inventory producer parity；
4. 不要把所有漏项强塞进 direct-method count，必须按论文真实方法分类；
5. 不要下载不可公开资产来“做齐数字”，只记录 unavailable/private/license blocker；
6. 不要删除 Audio2Tool extras；先做 manifest allowlist 与卫生报告；
7. 提交新完整 SHA、manifest、local PDF/hash receipts、producer-parity receipt；
8. 申请一次 bounded independent rereview，只请求 Stage-1C common-rubric comparison 权限。

在上述修复完成之前，本审稿人不签署 Stage-1C。修复完成后，预期剩余工作量是一个小型结构性
闭环，而不是新一轮大规模 survey。
