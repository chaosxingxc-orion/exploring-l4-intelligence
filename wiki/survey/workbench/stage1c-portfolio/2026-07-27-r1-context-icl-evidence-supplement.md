---
campaign: "stage1c-portfolio"
artifact_id: "R1-CONTEXT-ICL-EVIDENCE-SUPPLEMENT-V1"
role: "workbench full-text evidence supplement for the owner-approved R1 problem definition"
evidence_cut: "2026-07-27"
execution_authority: "WITHHELD"
---

# R1 多源上下文：相邻工作、数据集与实验载体补充证据

## 1. 结论

2026 年不能再把“speech/audio 模型是否具备 few-shot ICL”或“如何选择 speech demonstrations”作为 R1
的主创新问题。直接占据来自 Audio Flamingo、MiMo-Audio、MetaSICL、TICL、TICL+ 和 ByCS。仍可检验的
组合假设是：在同一个冻结 API core 上，联合改变 demonstration、当前 query representation 和供给拓扑，
测量给定菜单内经验上界及其交互/异质性，再判断训练自由 selector 能否恢复选择机会。

## 2. Full-text 占位矩阵

| ID | 论文与全文位置 | 承重事实 | 对 R1 的边界 |
|---|---|---|---|
| 2402.01831 | Audio Flamingo，PDF pp.1-2、§5.3/Table 4、Appendix C.1 | 经过 ICL/RAG 训练的 audio LM 在 CREMA-D、RAVDESS、UrbanSound8K、GTZAN 和 unseen labels 上展示 few-shot 能力 | 是专门训练的模型，不支持任意 frozen API core；没有 demo × query-view 因子 |
| 2512.23808 | MiMo-Audio，PDF p.1、§3.3.1/Tables 4-6 | 系统评估 speech/audio few-shot；模型和 eval suite 已发布 | 原论文主要建立模型能力；Base 与 Instruct 载体不得混写 |
| 2601.18904 | MetaSICL，PDF pp.2-5、Table 2、Limitations | vanilla SICL 在 MiMo-Audio/Qwen2.5-Omni 上覆盖 MyST、RSR、MMAU、MMAR；例如 MiMo MyST WER 14.25→11.55、RSR 31.39→16.84、MMAU 66.9→72.6、MMAR 54.7→58.2 | MetaSICL 主方法更新 LoRA，超出 TF-strict；固定 retrieval choices、未完整分析 inference scaling、固定设置单次运行 |
| 2509.13395 | TICL，PDF pp.1-4、Tables 1-4 | text-embedding KNN 选择 demos；口音、多语和儿童 ASR 最高报告 84.7% relative WER reduction | query view 固定，主要是 ASR，不能占据统一上下文问题 |
| 2512.18263 | TICL+，PDF pp.1-3/Table 1 | acoustic reranking 叠加 semantic retrieval；四个儿童语音 corpus，最高 53.3% relative WER reduction over zero-shot、37.6% over TICL | 仍是 demo retrieval，不研究 AU/AR 与 query re-representation |
| 2404.14716 | ByCS，PDF pp.1-7/Tables 1-4、Limitations | speech/text/vision 的 inverse-inference example selection；speech 使用 RASC863、CORAAL 与 Whisper | 候选逐项 inverse inference 较重；假设逐 demo interaction，未覆盖联合 context composition |

以上六篇的 PDF/e-print 均已放在仓库外 `speechrl-data/survey-fulltext/<id>/`，Git 只保存 fulltext ledger 的
12 条新增哈希记录和长期 registry 元数据。论文数字是原论文占位证据，不是本项目实验结果。

## 3. MetaSICL 对 R1 的直接启示

MetaSICL Table 2 已使“vanilla speech/audio ICL 有效”失去新颖性，但其结果同时展示异质性：不同模型、
任务和子类别的增益不一致，论文 limitations 也明确指出 fixed benchmark/retrieval choices、未完整研究长
context inference cost、缺少广泛 qualitative failures，且固定 checkpoint/config 多为单次运行。这些缺口
支持研究“上下文配置为什么按样本变化”，不支持重新宣称 vanilla ICL。

MetaSICL 的 `+MetaSICL1/2/3` 需要 LoRA，全部属于合同外 train-time evidence。R1 只能把原始模型的
`+Vanilla SICL` 行作为冻结推理基线。

## 4. 数据集可承载性

| 数据对象 | 可承载问题 | 不能直接承载 | 必需的执行前审计 |
|---|---|---|---|
| MyST | 儿童会话 ASR、demo selection、query view、domain heterogeneity | 通用 sound/music 推理 | official train/dev/test、speaker overlap、许可、音频/文本近重复 |
| RSR | 儿童朗读 ASR、与 MyST 的 distribution contrast | 开放式音频推理 | official training split 与 test fence；诊断数据使用条件 |
| MMAU Test-mini | sound/music/speech AU/AR、query-view/topology | 未核实独立 pool 前的 few-shot demo claim | benchmark split 语义、来源数据与 demo pool 的污染/去重 |
| MMAR | 16 类音频推理、query-view/topology | test answer/CoT 作为 runtime demo 或 reward | 1k benchmark 的 split、gold CoT fence、来源音频许可 |
| MELD/MELD-Hard1k | clean/perturbed paired mechanism、SER、query transformation | 广泛 AU/AR 泛化 | MELD split/license；Hard1k recipe 重建、随机种子、非 byte-identical 声明 |

没有一个现成 benchmark 同时提供“合法 demo pool、同 query 的多视图、ASR+AU/AR 广度和完整声学条件
标签”。因此 R1 的实验对象是叠加在现有数据集上的 **context intervention protocol**，不是一个被假定
已经完整的数据集。MMAU/MMAR 若无法闭合独立 demo pool，只运行 query-view 部分，不做 test leave-one-out。

## 5. 模型载体可承载性

- `Qwen/Qwen2.5-Omni-7B`：主载体；官方实现支持 interleaved audio/image/video 输入，足以表达多个 audio
  demonstrations，但 exact checkpoint、服务栈与最大上下文仍须在 Stage-2 合同冻结。
- `XiaomiMiMo/MiMo-Audio-7B-Instruct`：独立家族复核；官方 checkpoint/evaluation suite 已发布。原论文
  系统 few-shot 表主要承载 Base 能力，因此本项目的 Instruct 复核必须重新运行，不引用 Base 数字代替。
- Audio Flamingo：外部 prior/baseline，不作为主要复核 core；其专门 ICL 训练会混淆“模型已有能力”与
  “系统上下文构造”的归因。
- Whisper/ByCS：示例选择的 architecture-specific 边界基线；Whisper encoder-decoder ICL 不等同于
  decoder-style Omni API 的多源上下文构造。

## 6. 失效条件

本补充证据在论文版本改变关键实验设置、官方代码/模型资产撤回、数据 split 审计推翻 demo-pool 合法性，
或新的直接工作同时联合 demonstration、query representation、menu ceiling 和 sample-adaptive construction
时失效并需要追加 superseding registry row。它不构成技术 novelty verdict，也不授权数据/模型实验。
