---
title: "Owner consolidated execution contract: speech-aware evidence acquisition"
record_id: "SAEA-OWNER-CONSOLIDATED-EXECUTION-CONTRACT-2026-08-04"
date: "2026-08-04"
issued_by: "research owner (in-session directives, 2026-08-04)"
semantic_research_object: "speech-aware evidence acquisition"
source_candidate_provenance: "R2 (system-first-stage1c-v2; audit provenance only)"
authorization: "OWNER_GO_AND_EXECUTION_CONTRACT"
carrier_class: "Stage-2 study repository (Decision-Log-2026-08 续91)"
paper_gate: "OWNER_GO_AND_PAPER_EXECUTION_CONTRACT"
entry_contract: "docs/superpowers/specs/2026-08-02-speech-aware-evidence-acquisition-stage2a-entry.md"
formal_opening: "wiki/audit/system-first-stage1c-v2/round-22/2026-08-02-audio-aware-evidence-acquisition-formal-opening-permission-note.md"
---

# Owner 合并有效合同：speech-aware evidence acquisition

本合同是本 study **当前唯一自包含的执行权威**。它把 2026-08-03 GO、2026-08-04 speech-only
范围/身份合同与 2026-08-04 Stage‑3 边界合同合并为一份可独立阅读的有效规范；三份来源合同保留为
历史/来源记录（§9），其事实不回写。

## 1. 生效身份与授权

Owner 已签发 `OWNER_GO_AND_EXECUTION_CONTRACT`（2026-08-03），研究对象于 2026-08-04 收窄并
重命名为 **speech-aware evidence acquisition**。本仓是 **Stage‑2 study 载体**（续91）。

- GitHub：`https://github.com/chaosxingxc-orion/speech-aware-evidence-acquisition.git`；
- 本地 checkout：`studies/speech-aware-evidence-acquisition/`；
- Python distribution/package：`speech-aware-evidence-acquisition` /
  `speech_aware_evidence_acquisition`；
- 实验命名空间：`SAEA-E-<nnn>`；
- 实验台账：`wiki/experiments/speech-aware-evidence-acquisition/README.md`。

R2 等候选编号只是审计溯源，不承担工程身份。创新与最终方法在 Stage‑2 收敛为合格 paper
candidate，其最终验证属 Stage‑3（§7）。

## 2. 域边界：speech 不等于 general audio

研究对象只限**人类言语及其语言内容**：ASR、实体识别/纠错、contextual biasing、spoken QA、
会议语音理解及与语音理解直接相关的证据使用。WAV/MP3 等音频文件是 speech signal 的合法载体；
声景/事件/音乐/动物声等 general/environmental audio 任务不在范围内。对声学编码器、adapter 或
核心模型的参数训练被 TF-Strict 禁止。

FSD50K、AudioSet、ESC-50 不得进入本 study 的训练、开发、测试、baseline、消融或结论外推；其已
下载字节按 `docs/datasets.lock.json` 记录为跨域留存资产，保留不等于采纳。

## 3. 研究问题与四轴分离

主问题：在不修改冻结 speech-capable omni 核参数/结构/训练范式、不引入第二个答题 LLM 的条件下，
外部 reward-guided 控制平面能否通过改善语音观察与外部知识证据的组织、供给和使用，稳定提高
speech-domain 任务表现，并降低"误听实体 → 检索到相关但错误证据 → 错误被强化"的系统性风险？

四个必须分离的对象：`OBS`（语音观察与重解析）、`ORG`（知识组织/索引/来源）、`SUPPLY`
（证据选择/数量/顺序/时机）、`USE`（证据准入/核验/迭代/停止）。所有实验 trace 分别记录四轴的
输入、动作、结果、版本与 hash；四轴同改而只报总分的实验不足以支持机制结论。引入外部知识服务
可访问性、时效/专名、可验证性三个可检验缺口，同时必须报告相关但错误证据带来的
correct-to-wrong 回归、上下文污染与 reward hacking 风险。

## 4. 数据与 baseline 绑定

数据身份、磁盘状态、revision、size 和 checksum 的唯一当前信息源是 `docs/datasets.lock.json`；
本合同只冻结实验角色，不复制易漂移的哈希。

| 层级 | lock 键 | Stage-2 角色 | 当前义务 |
|---|---|---|---|
| Core | `earnings21-original`, `earnings22-original`, `conec` | 实体密集 ASR/上下文纠错主载体、dev/confirmatory 与证据层 | E0 必须关闭 identity、leakage、scoring、trace |
| Diagnostic | `prism-public`, `rare5k-reconstruction`, `buzzword` | 稀有词、专名和 contextual biasing 诊断 | 只回答对应诊断问题，不替代 core 结论 |
| Secondary speech | `slue-sqa-5`, `contextasr-bench`, `ami-meeting-corpus` | spoken QA、双语 contextual ASR、会议语音迁移/压力测试 | 在 core 路径成立后按预注册顺序启用 |
| Optional speech | `ted-el-annotations`, `atco2-test-1h`, `eka-medical-asr-eval`, `librisqa-metadata` | 实体标注、领域语音和低成本相邻验证 | 非开工门；使用前冻结具体假设 |
| Retained cross-domain | `fsd50k`, `audioset-metadata-features`, `esc-50` | 无本 study 实验角色 | 保留本地，不加载、不引用为支持性实验 |

closest-prior 复现以 ConEC/contextual ASR、RECOVER-style 1-best correction、Siskos 实体消解及
FlexCTC/TurboBias 等同边界语音偏置线为候选。每个 baseline 首次 run 前必须冻结 runnable
revision、可见字段和失败语义；不可运行时报告 `INCONCLUSIVE_BASELINE_NOT_READY`，不得静默换弱
对手。

## 5. 评价合同

- **有效性**：预注册 WER/CER、entity-WER/recall/F1、QA EM/F1 或 carrier 原生指标；
  wrong-to-correct / correct-to-wrong / unchanged 状态转移；分 speaker/domain/entity-frequency/
  noise 条件的均值、方差、尾部与置信区间；retrieval recall/precision、证据覆盖、引用正确性。
- **合理性**：预注册 `OBS × ORG × SUPPLY × USE` 最小因子对照，一次只改可归因的轴；bare core、
  固定合法 context、随机/错配 evidence、oracle evidence（只作上界）与 no-use 负对照；gold/
  reference/test/future-turn 不越过 runtime boundary；证据被 supply 与被 use 分开判定；
  discovery/confirmatory 隔离，阈值与选择规则在读取 confirmatory 结果前冻结。
- **效率**：同时报告绝对成本与单位收益——冻结核/工具调用次数、token、端到端 latency、
  GPU/CPU-hours、峰值显存、处理 speech seconds、供给与被采用证据量、每 1 个指标点的增量成本、
  Pareto 前沿。禁止只报"省了百分之多少"。

## 6. 冻结字段、预算与执行序列

| 字段 | 当前冻结值 |
|---|---|
| Core/runtime | `qwen3-omni-30b-a3b-instruct-gguf`；llama.cpp build commit 与 GGUF 逐文件 SHA-256 在首次模型调用前落 runtime receipt |
| Information boundary | gold/reference/test annotation/future turn 永不进入 runtime；各臂可见字段与 prompt/config hash 入账 |
| Resources | 首切片 ≤3,000 次冻结核调用、≤40 GPU-hours、≤20 小时 speech audio、付费 API=0；非零支出需 dated amendment |
| Exposure | study 仓 `docs/exposure-ledger.md` 在读取结果前登记；声明含 scope/date/counts/inherited；正式台账行必须带 split role、split identity hash 与 consumed 标记 |
| Sequence | E0（D1–D4）→ R0 纵向链 → R1 closest-prior reproduction → X bounded 定向探索 |
| Execution scope | 本仓只接受 `model-free-check` / `baseline-reproduction` / `bounded-discovery-probe` 执行 profile；`paper-scale-confirmatory` 一律 fail closed（§7） |
| Stop line | 泄漏、scorer 不一致、样本身份漂移、许可失效、未登记 exposure、同边界更强 runnable prior 未处理 |

E0 与 runtime receipt 关闭前不得触达模型。周度文献 delta 只更新 prior/threat queue；除非新证据
推翻研究问题、数据合法性、信息边界或可复现合同，否则不得重开无界 Stage‑1 扫描阻塞工程。

## 7. Study 终点与 Stage‑3 停止线（续91）

本 study 的 Stage‑2 终点是形成一个或多个可证伪、可复现的 **qualified paper candidate**
（改进主张与零假设、机制、baseline 收据、实验与统计设计、未读 confirmatory 声明），而不是完成
最终论文实验。以下动作默认禁止，须先经 `OWNER_GO_AND_PAPER_EXECUTION_CONTRACT` 晋级建立
`papers/<slug>` 独立仓：

- production-scale 方法实现与大规模 confirmatory campaign；
- 最终优越性/泛化结论；bounded probe 结果不得写成论文级 claim；
- manuscript、submission、publication release。

零/负结果是合法的 study 完成形态；candidate 之间不得共享未登记的 test exposure；某一 candidate
获 paper GO 不授权本 study 的其他 candidate。在程序级 confirmatory reservation 台账落地前
（触发器见续92），任何 confirmatory 样本读取前必须在实验台账与 exposure ledger 登记 split
identity hash 并标记消耗；跨 study/paper 的继承 exposure 单调不减。

## 8. 数据保留与删除规则

本合同不删除 `SPEECHRL_DATA_DIR` 下任何已验证数据；"未进入当前 study"不构成删除理由。删除需
独立 owner 指令、精确目标、可恢复性说明和 lock amendment。

## 9. 来源记录（历史，不回写）

| 记录 | 路径 | Git blob |
|---|---|---|
| 2026-08-03 GO 合同（预算与授权来源） | `2026-08-03-owner-go-and-execution-contract.md` | `e059b6257fad4be45f3014297a26c4a40257b9af` |
| 2026-08-04 speech-only 范围/身份合同 | `2026-08-04-owner-speech-domain-scope-and-identity-contract.md` | `57bf8e23f7282162d06936b5ea484ea6fb5bdea8` |
| 2026-08-04 Stage‑3 边界/paper-gate 合同 | `2026-08-04-owner-stage3-boundary-and-paper-gate-contract.md` | `5f91226f25d6bfd5c5cd427c57fecc635eb43066` |

本合同取代上述三份合同的"当前有效"地位（其签发事实、历史 exposure、预算与授权事实全部继承、
不回写）。失效条件：owner 修改 study 范围、身份、预算、载体绑定或 paper gate。

## Owner acceptance

Accepted by owner on 2026-08-04 (session direction; recorded in Decision-Log-2026-08 续91/续92).
