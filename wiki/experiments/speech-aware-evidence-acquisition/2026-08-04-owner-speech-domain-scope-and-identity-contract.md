---
title: "Owner effective contract: speech-aware evidence acquisition"
record_id: "SAEA-OWNER-SPEECH-SCOPE-AND-IDENTITY-2026-08-04"
date: "2026-08-04"
issued_by: "research owner (in-session directives, 2026-08-04)"
semantic_research_object: "speech-aware evidence acquisition"
source_candidate_provenance: "R2 (system-first-stage1c-v2; audit provenance only)"
authorization: "OWNER_GO_AND_EXECUTION_CONTRACT"
entry_contract: "docs/superpowers/specs/2026-08-02-speech-aware-evidence-acquisition-stage2a-entry.md"
formal_opening: "wiki/audit/system-first-stage1c-v2/round-22/2026-08-02-audio-aware-evidence-acquisition-formal-opening-permission-note.md"
supersedes_effective_scope_of: "wiki/experiments/speech-aware-evidence-acquisition/2026-08-03-owner-go-and-execution-contract.md"
---

# Owner 有效合同：speech-aware evidence acquisition

## 1. 生效决定

Owner 于 2026-08-04 将已获 GO 的研究对象从 **audio-aware evidence acquisition** 收窄并重命名为
**speech-aware evidence acquisition**。Stage-1C 的 R2 编号和原开题许可文件名只保留审计溯源，
不再承担工程身份。

本合同是当前自包含的执行权威：

- GitHub：`https://github.com/chaosxingxc-orion/speech-aware-evidence-acquisition.git`；
- 本地 checkout：`studies/speech-aware-evidence-acquisition/`；
- Python distribution/package：`speech-aware-evidence-acquisition` /
  `speech_aware_evidence_acquisition`；
- 实验命名空间：`SAEA-E-<nnn>`；
- 实验台账：`wiki/experiments/speech-aware-evidence-acquisition/README.md`。

2026-08-03 原合同仍是当时 owner GO、预算和授权来源的历史证据；本合同继承其 GO，并取代其中
旧研究名称、旧路径、旧远端、旧命名空间及过宽的 audio-domain 表述。它不回写正式开题审计件，
也不改变“创新与最终方法在 Stage-2A/2B 收敛”的原裁定。

## 2. 域边界：speech 不等于 general audio

本研究处理的输入仍可由 WAV/MP3 等音频文件承载，但研究对象只限于**人类言语及其语言内容**：
ASR、实体识别/纠错、上下文偏置、spoken QA、会议语音和与语音理解直接相关的证据使用。

以下概念必须分开：

| 概念 | 本研究含义 | 是否在范围内 |
|---|---|---|
| speech signal | 承载词、实体、说话轮次和语义内容的人类言语声学信号 | 是 |
| speech task | ASR、spoken QA、会议语音理解、语音实体与上下文纠错 | 是 |
| general/environmental audio | 声景、事件、音乐、动物声、非语言声源的识别或问答 | 否 |
| audio-model training | 对声学编码器、adapter 或核心模型做参数训练 | 否；TF-Strict 禁止 |

因此，FSD50K、AudioSet 和 ESC-50 不得进入本 study 的训练、开发、测试、baseline、消融或结论外推。
它们已经下载的字节不删除：继续由 `docs/datasets.lock.json` 记录为本地完整、跨域留存资产，未来若有
另一个经过 owner GO 的 general-audio study，可复用这些字节。保留不等于本研究采纳。

## 3. 研究问题与可证伪结构

### 3.1 主问题

在不修改冻结 speech-capable omni 核的参数、内部结构和训练范式、且不引入第二个答题 LLM 的条件下，
外部 reward-guided 控制平面能否通过改善**语音观察**与**外部知识证据**的组织、供给和使用，稳定提高
speech-domain 任务表现，并降低“误听实体 → 检索到相关但错误证据 → 错误被强化”的系统性风险？

### 3.2 四个必须分离的对象

| 轴 | 被改变的对象 | 典型动作 | 不得混入的解释 |
|---|---|---|---|
| OBS：语音观察 | 从同一 speech signal 得到的候选转写、实体跨度、时间边界或重解析结果 | 重解码、候选生成、实体片段重听 | 不能把 gold transcript 当作运行时观察 |
| ORG：知识组织形式 | 外部知识如何被切分、索引、链接、标注来源和置信度 | passage/entity/graph、层级粒度、时间或说话人绑定 | 不能把“检索到更多文本”等同于组织更好 |
| SUPPLY：知识供给形式 | 哪些证据、以何种数量、顺序、上下文模板和时机进入冻结核 | top-k、source selection、ordering、citation envelope | 不能把模型最终采用证据等同于已经供给 |
| USE：知识使用形式 | 控制器如何准入、拒绝、核验、迭代、停止以及把证据用于最终回答 | accept/reject/re-query/abstain、reward-guided next action | 不能把一次 rerank 冒充完整的序列控制 |

所有实验 trace 必须分别记录 `OBS`、`ORG`、`SUPPLY` 和 `USE` 的输入、动作、结果、版本与 hash。
任何把四轴同时改变、却只报告一个总分的实验，不足以支持机制结论。

### 3.3 黑盒条件下为什么引入知识

引入外部知识不是因为冻结核“没有任何知识”，也不是为了以检索器代替核心模型。它服务三个可检验缺口：

1. **可访问性缺口**：模型可能在预训练中见过相关知识，但当前语音观察和上下文未能可靠激活它；
2. **时效/专名缺口**：公司名、人名、产品名和当期会议材料可能不在参数记忆中，或没有可靠的语音到实体映射；
3. **可验证性缺口**：外部证据提供来源、时间与引用边界，使系统能区分“模型猜测”与“有证据支持”。

它也引入明确风险：错误观察会诱导相关但错误的检索，证据过量会污染上下文，控制器可能追逐代理 reward。
所以“加知识后分数提高”不是充分结论；必须同时证明证据相关、信息边界合法、改进来自预注册路径，并报告
correct-to-wrong 回归。

## 4. 数据与 baseline 绑定

数据身份、磁盘状态、revision、size 和 checksum 的唯一当前信息源是 `docs/datasets.lock.json`；本合同只
冻结实验角色，不复制易漂移的哈希。

| 层级 | lock 键 | Stage-2 角色 | 当前义务 |
|---|---|---|---|
| Core | `earnings21-original`, `earnings22-original`, `conec` | 实体密集 ASR/上下文纠错主载体、dev/confirmatory 与证据层 | E0 必须关闭 identity、leakage、scoring、trace |
| Diagnostic | `prism-synthetic`, `rare5k-reconstruction`, `buzzword` | 稀有词、专名和 contextual biasing 诊断 | 只回答对应诊断问题，不替代 core 结论 |
| Secondary speech | `slue-sqa-5`, `contextasr-bench`, `ami-meeting-corpus` | spoken QA、双语 contextual ASR、会议语音迁移/压力测试 | 在 core 路径成立后按预注册顺序启用 |
| Optional speech | `ted-el-annotations`, `atco2-1h`, `eka-medical`, `librisqa` | 实体标注、领域语音和低成本相邻验证 | 非开工门；使用前冻结具体假设 |
| Retained cross-domain | `fsd50k`, `audioset-metadata-features`, `esc-50` | 无本 study 实验角色 | 保留本地，不加载、不引用为支持性实验 |

closest-prior 复现仍以 ConEC/contextual ASR、RECOVER-style 1-best correction、Siskos 实体消解及
FlexCTC/TurboBias 等同边界语音偏置线为候选。每个 baseline 在首次 run 前必须冻结 runnable revision、
可见字段和失败语义；不可运行时报告 `INCONCLUSIVE_BASELINE_NOT_READY`，不得静默换弱对手。

## 5. 评价合同

### 5.1 有效性：是否改善任务结果

- 任务指标：预注册的 WER/CER、entity-WER/entity recall/F1、QA EM/F1 或 carrier 原生指标；
- 状态转移：wrong-to-correct、correct-to-wrong、unchanged-wrong、unchanged-correct；
- 稳定性：分 speaker/domain/entity-frequency/noise 条件报告均值、方差、尾部和置信区间；
- 证据指标：retrieval recall/precision、证据覆盖、引用正确性和最终答案支持率。

### 5.2 合理性：为什么改善、是否允许这样改善

- 预注册 `OBS × ORG × SUPPLY × USE` 的最小因子对照，一次只改变可归因的轴；
- bare core、固定合法 context、随机/错配 evidence、oracle evidence（只作上界）和 no-use 负对照；
- gold/reference/test/future-turn 不得越过 runtime boundary；所有来源、query、时间和版本可追溯；
- 证据被 supply 与证据被 use 分开判定，报告相关但错误证据导致的回归；
- discovery/confirmatory 隔离；阈值、停止条件和选择规则在读取 confirmatory 结果前冻结。

### 5.3 效率：为改进付出了什么

同时报告绝对成本和单位收益，禁止只报“省了百分之多少”：

- 冻结核调用次数、工具/检索调用次数、输入/输出 token；
- 端到端 latency、GPU-hours、CPU-hours、峰值显存、处理的 speech-audio seconds；
- 检索候选数、实际供给证据数/bytes、被模型实际采用的证据数；
- 每 1 个 WER/entity-WER 绝对点或每 1 个 QA 分数点的增量成本；
- Pareto 前沿：任务效用、correct-to-wrong 风险、延迟和调用成本。

## 6. 冻结字段与执行序列

| 字段 | 当前冻结值 |
|---|---|
| Core/runtime | `qwen3-omni-30b-a3b-instruct-gguf`；llama.cpp build commit 与 GGUF 逐文件 SHA-256 在首次模型调用前落 runtime receipt |
| Information boundary | gold/reference/test annotation/future turn 永不进入 runtime；各臂可见字段与 prompt/config hash 入账 |
| Resources | 首切片 ≤3,000 次冻结核调用、≤40 GPU-hours、≤20 小时 speech audio、付费 API=0；非零支出需 dated amendment |
| Exposure | `docs/exposure-ledger.md` 在读取结果前登记；声明包含 scope/date/counts/inherited |
| Sequence | E0（D1–D4）→ R0 纵向链 → R1 closest-prior reproduction → X 定向探索 |
| Stop line | 泄漏、scorer 不一致、样本身份漂移、许可失效、未登记 exposure、同边界更强 runnable prior 未处理 |

E0 与 runtime receipt 关闭前不得触达模型。周度文献 delta 只更新 prior/threat queue；除非新证据推翻
研究问题、数据合法性、信息边界或可复现合同，否则不得重新打开无界 Stage-1 扫描来阻塞工程。

## 7. 数据保留与删除规则

本次身份迁移不删除 `SPEECHRL_DATA_DIR` 下任何已验证数据。今后也不得因为“未进入当前 study”就删除
完整资产；删除需独立的 owner 指令、精确目标、可恢复性说明和 lock amendment。当前只改变实验绑定：
speech-domain 数据进入可验证清单，general-audio 数据进入跨域留存清单。
