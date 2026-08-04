---
artifact_id: "SAEA-SPEECH-DATA-SCOPE-2026-08-04"
title: "Speech-domain dataset scope, Stage-2 roles and local retention plan"
date: "2026-08-04"
status: "CURRENT__DOWNLOAD_WAVE_CLOSED__SPEECH_BINDINGS_FROZEN__NO_DATA_DELETION"
authority: "owner directives 2026-08-04"
canonical_state_source: "docs/datasets.lock.json"
---

# Speech-domain 数据范围、Stage-2 角色与本地保留计划

## 1. 结论

当前下载波次已经结束，Stage-2A 不再等待新增数据。五个本轮重点收尾数据均已按 canonical lock 标为
`COMPLETE`：`audioset-metadata-features`、`ami-meeting-corpus`、`slue-sqa-5`、`fsd50k`、
`contextasr-bench`。

下载完成与研究采纳是两个不同判断：

- AMI、SLUE-SQA-5、ContextASR-Bench 是 speech-domain，可进入后续预注册实验；
- FSD50K、AudioSet 是 general/environmental audio，不进入本 study；
- ESC-50 同属 general audio，虽然此前已在本地，也不进入本 study；
- 所有已经下载的数据均保留，不删除、不重复下载；其身份、size、revision、checksum 与状态继续只由
  `docs/datasets.lock.json` 维护。

这消除了过去“论文里出现 → 下载 → 默认成为 R2 实验集”的隐式链条。今后必须先有研究问题或 baseline
角色，再产生数据绑定。

## 2. 适用域判定

### 2.1 纳入

数据的主要可评价目标必须是人类言语及其语言内容，包括 ASR、实体识别/纠错、contextual biasing、
spoken QA、会议语音理解。噪声条件可以作为 speech robustness 的扰动，但环境声音分类本身不是任务。

### 2.2 排除但保留

主要标签为声学事件、声景、音乐或非语言声源的数据不进入 study，即使 omni 模型能接受这种输入。
排除原因是 research question 的 domain，不是本地字节无效，也不是对模型训练史作未经验证的断言。

### 2.3 禁止的推理

- “文件扩展名是音频”不能判定为 general-audio；speech 也由音频文件承载；
- “已经下载”不能判定为必须实验；
- “论文引用了数据集”不能判定为必须复现；
- “模型是 omni”不能把所有模态任务自动纳入同一个研究对象。

## 3. 唯一事实源与保留政策

`docs/datasets.lock.json` 是唯一 live source，负责：上游身份、revision、来源、local path、精确 size、
验证方法、checksum/hash、状态、lifecycle 与 profile。本文只说明本 study 的实验角色，不复制哈希。

本轮不删除任何数据。未来清理必须满足全部条件：owner 明确授权、精确路径已解析、无活跃/计划实验
引用、lock 有带日期 amendment、删除后有可恢复性或重新获取说明。当前 FSD50K、AudioSet、ESC-50
均不满足删除条件，因为 owner 已明确要求保留下载成果。

## 4. Stage-2 数据层级

| 层 | 数据 | 研究问题 | 启用条件 | 可支持的结论 |
|---|---|---|---|---|
| Core-main | Earnings21 + ConEC | 实体误听、上下文证据和错误强化 | E0 identity/leakage/scorer/trace 关闭 | 主机制与任务效用 |
| Core-dev | Earnings22 + ConEC | 阈值、候选宽度、停止策略与 source policy 标定 | 与 confirmatory 隔离 | 配置选择，不作最终确认 |
| Diagnostic | PRISM synthetic、Rare5k reconstruction、BuzzWord | 稀有词、专名、biasing 的局部失效模式 | 对应 scorer 和 slice 预注册 | 诊断，不外推总体 |
| Secondary-SQA | SLUE-SQA-5 | speech observation 与外部文本证据在 spoken QA 中的交互 | core 最小路径成立 | 跨任务 speech 复制 |
| Secondary-context | ContextASR-Bench | 双语 contextual ASR、上下文供给形式 | 同边界 baseline 可运行 | 跨语言/上下文复制 |
| Secondary-meeting | AMI meeting corpus | 多说话人、长上下文与会议实体压力 | 固定 mixed-headset 条件、明确切分 | 条件迁移/压力测试 |
| Optional | TED-EL annotations、ATCO2-1h、Eka-Medical、LibriSQA | 特定实体/领域/低成本相邻问题 | 每项另有 protocol hash | 仅限预注册局部问题 |
| Cross-domain retained | FSD50K、AudioSet metadata/features、ESC-50 | 无 | 本 study 永不启用 | 不支持本 study 结论 |

## 5. 下载波次收尾解释

### 5.1 本轮五项如何处置

| lock 键 | 本地状态 | 新裁定 | 是否进入 Stage-2 清单 |
|---|---|---|---|
| `slue-sqa-5` | COMPLETE | speech secondary carrier | 是，core 后启用 |
| `contextasr-bench` | COMPLETE | speech secondary carrier | 是，core 后启用 |
| `ami-meeting-corpus` | COMPLETE | speech meeting stress/transfer carrier | 是，需独立 protocol |
| `fsd50k` | COMPLETE | cross-domain retained | 否 |
| `audioset-metadata-features` | COMPLETE | cross-domain retained | 否 |

下载队列的完成收据不等于实验完成。对前三项，Stage-2 仍需 loader、split、information boundary、
metric 和 baseline readiness；对后两项，不再产生本 study 工程任务。

### 5.2 不重复下载

任何 fetch 前先由 `asset_lock.py` 查询 lock entry，并核对本地 `verification` 与 partial marker。
`COMPLETE` 资产默认只校验，不重新拉取。仅当 checksum drift、缺文件或 owner 选择新 revision 时，才
创建带日期的续传/升级计划；续传复用已有 `.aria2`/cache 和完整文件，禁止先删后下。

## 6. Baseline 与数据消费矩阵

| baseline/对照 | 首选 carrier | 目的 | 最低 readiness |
|---|---|---|---|
| bare frozen core | Earnings21/22 | 测定无外部知识的真实基线 | runtime pin + fixed prompt |
| legal fixed context | Earnings + ConEC | 区分 context availability 与控制收益 | 可见字段 hash，无 gold 泄漏 |
| ConEC/contextual ASR | Earnings + ConEC | closest-prior 主复现 | runnable revision、scorer 对齐 |
| RECOVER-style 1-best correction | Earnings | 强制纠错对照 | 同输入边界、无第二答题 LLM |
| entity resolution/context biasing | Earnings、ContextASR、diagnostics | 实体与稀有词对照 | 词表来源与注入时机冻结 |
| random/mismatched evidence | 每个启用 carrier | 检查提升是否只是上下文长度/提示效应 | 与真实 evidence 等预算 |
| oracle evidence bound | discovery only | 估计供给上界 | 明示 oracle，不进入 confirmatory runtime |

SLUE-SQA-5、ContextASR 和 AMI 不应在第一周同时展开。推荐顺序：Earnings core → 一个 closest prior →
SLUE-SQA-5 或 ContextASR 二选一复制 → AMI 压力测试。这样能用最少变量定位失败原因。

## 7. 实验清单刷新规则

每发现一篇新论文，先填四个问题：

1. 它是否改变当前 speech-domain research question 或同边界 closest prior？
2. 它的数据是否被一个具体 baseline、replication 或诊断假设消费？
3. 数据是否公开、许可可接受、单项小于 1 TB、能固定 revision？
4. 本地已有数据能否回答同一问题？

只有前两项为“是”、后三项通过且 owner 接受边际成本时，才向 lock 增加 acquisition proposal。否则只
更新文献/威胁清单。新论文不能自动扩大实验表。

## 8. Stage-2A 立即任务

1. 关闭 Earnings21/22 + ConEC 的 E0 D1–D4；
2. 固化 `OBS/ORG/SUPPLY/USE` 四轴 trace schema；
3. 完成 bare core、fixed legal context 和一个 closest-prior vertical slice；
4. 冻结 effectiveness/reasonableness/efficiency 联合评价表；
5. 在 core stop/go 后选择 SLUE-SQA-5 或 ContextASR 作为首个 secondary carrier；
6. 检查依赖图和测试发现路径不含 FSD50K、AudioSet、ESC-50。

在上述任务完成前，不再新增下载。这样既保留已取得的数据资产，也把工程注意力收敛回 speech-domain
研究问题。
