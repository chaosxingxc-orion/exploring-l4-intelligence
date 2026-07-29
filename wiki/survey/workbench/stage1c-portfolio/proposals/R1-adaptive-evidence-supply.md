---
proposal_id: "R1"
title: "冻结 Speech/Omni 模型的语音/音频上下文学习方法复现与比较研究"
role: "Stage-1C 研究内容分析报告；供 owner 作方向判断"
stage: "STAGE_1C_DIRECTION_CONFIRMATION"
status: "OWNER_CONFIRMED_SUNSET_2026-07-29"
recommendation: "NO_GO_AS_STANDALONE_DIRECTION__SUNSET_BEFORE_STAGE2"
evidence_cut: "2026-07-28"
execution_authority: "WITHHELD"
---

# R1 — 冻结 Speech/Omni 模型的语音/音频上下文学习方法复现与比较研究

## 0. 结论先行

**Owner 裁决（2026-07-29 确认，Decision-Log 续76）：R1 不具备独立研究方向潜力——它只提出了基础要
探索的内容，不构成可对比的研究问题——不作为独立研究方向进入 Stage-2，原 Stage-2B 名额撤销。**

R1 在 Stage‑1C 的正确定位不是发明新的多源上下文控制器，也不是证明一个尚未被研究的创新点，而是：

> 在项目选定的冻结 Speech/Omni 核心上，复用参考论文的数据集、数据划分、方法、基线和评价指标，
> 系统复现并比较语音/音频 in-context learning（ICL）及相关 inference-time context 方法，归纳它们在
> 通用 ASR 与通用音频理解/推理任务中的适用条件、收益、负迁移和复现边界。

现有文献已经覆盖 audio few-shot、speech demonstration retrieval、acoustic reranking、inverse-inference
selection、audio tool use 和 modality topology。严格复现这些方法仍有实验价值，但它们是任何实际消费
context action 的 Stage-2 方向都应完成的 baseline，不构成一项独立研究问题。若把这些方法重新组合成新的
selector、controller、oracle ceiling 或综合指标，又会越过当前“只分析归纳、不创造创新”的边界。

因此本报告保留为文献、数据、基线和指标的归纳记录；相关基线由 R3–R8 在实际需要时按原论文协议复用，
不再为 R1 单独建立实验包、执行合同或 Stage-2 阶段。

## 1. 本阶段的三条硬边界

### 1.1 只做研究方向确认

当前工作等价于开题报告：确认研究内容、研究对象、参考方法、实验基线、数据集和评价体系。允许做文献归纳、
协议对齐、边界识别和推进判断；不做创新点搜索、技术路线发明或系统实现。

### 1.2 数据只复用参考论文

- 只选参考论文实际使用并可合法取得的公开数据集及其既有划分。
- 不采集、不合成、不标注、不扩增新的研究数据集。
- 论文作者创建但已正式发布的数据集可以原样复用；没有发布的作者自建数据集不得由本项目按 recipe 重建后
  冒充同一 benchmark。
- 因此，TwS 的 MELD-Hard1k 在官方可核验资产发布前只作为论文证据，不进入 R1 数据计划；原始 MELD 可以
  作为论文方法的既有载体，但不由本项目制造新的扰动版。

### 1.3 指标只复用参考论文

- ASR 使用 WER；中文、日文、泰文按 TICL 的做法使用 CER。
- AU/AR 与单标签分类使用 accuracy，并按参考论文已有类别/模态分组报告。
- 只有在复现相应任务时，才使用论文中的 BLEU、CIDEr、F1、BLEU4 或 ROUGE-L。
- 可以复用论文已报告的 relative WER reduction 或 absolute accuracy gain 作为辅助呈现。
- 不新造跨任务综合分数、context headroom、selection opportunity、recovery ratio 或自定义 utility。

## 2. 研究内容

### 2.1 总研究问题

> 参考论文已经提出的语音/音频上下文学习与 inference-time context 方法，在冻结、API-only 的
> Qwen3-Omni-30B 项目核心上，能否按照其原始数据、基线和指标得到可复现、可比较、边界清楚的结果？

该问题拆成三个研究内容，三者都是归纳与复现，不构成新方法：

1. **通用 ASR 的 demonstration 方法比较。** 比较 direct/zero-shot、uniform random、声学 embedding
   retrieval、TICL semantic retrieval 等参考论文已经定义的条件，分析不同语言、口音和示例数下的 WER/CER。
2. **通用音频理解/推理的 few-shot 复现。** 在 MMAU、MMAR 等论文使用的数据集上，比较 direct 与
   Vanilla SICL；只有在论文或官方代码能够闭合 demonstration pool 来源时才运行 few-shot 条件。
3. **query-side context 方法的独立复现边界。** TwS 与 CoM 分别说明 waveform tool use 和 modality
   topology 会改变结果。R1 只把它们作为独立论文方法记录或复现，不与 demonstration retrieval 拼成新机制。

### 2.2 研究问题

- **RQ1：** 在通用 ASR 上，Vanilla SICL 是否稳定优于 direct/zero-shot？
- **RQ2：** 在论文已经比较的条件内，random、声学检索和语义检索的相对排序是否可复现？
- **RQ3：** 参考方法的收益或损害如何随语言、口音、任务、模态子类和示例数变化？
- **RQ4：** 在 MMAU/MMAR 上，参考论文的 direct 与 Vanilla SICL 差异能否在严格 split fence 下复现？
- **RQ5：** 对 TwS/CoM，论文的原始任务、资产和接口是否足以支持独立复现；哪些环节因数据或实现未发布而
  只能保留为文献结论？

RQ1–RQ5 都不询问“如何发明一个更好的选择器”。如果未来需要研究新控制方法，必须在参考方法复现完成、
Stage‑1C 另行立项后再讨论。

## 3. 直接参考论文的研究要素矩阵

| 论文 | 已有研究问题与方法 | 论文数据集 | 论文基线 | 论文指标 | 对 R1 的正确用途与边界 |
|---|---|---|---|---|---|
| Audio Flamingo, 2402.01831 | 经过 ICL/RAG 专门训练的 audio LM；检索 audio-text demonstrations | CREMA-D、RAVDESS、UrbanSound8K、GTZAN、Medley-solos-DB；AudioCaps | 自身 zero-shot；已有 zero-shot SOTA；AudioCaps 上 RECAP | 分类 accuracy；caption CIDEr；其他任务按论文使用 F1、BLEU4、ROUGE-L | 证明 audio few-shot 已被占据；可复用数据/指标，但专门训练模型的结果不能外推到任意冻结 API core |
| MiMo-Audio, 2512.23808 | MiMo-Audio-7B-Base 的 5-shot/16-shot 能力评估 | 已发布 SpeechMMLU；MMAU；若进入 Instruct 评估还包括 MMSU、MMAR、MMAU-Pro 等 | Baichuan-Audio-Base、Kimi-Audio-Base、Step-Audio2-mini-Base | SpeechMMLU/MMAU accuracy；ASR 使用 WER/CER | 证明大规模预训练可产生 few-shot 能力；Base 与 Instruct 不得混写，不作为 Qwen3 的直接实验结果 |
| MetaSICL, 2601.18904 | Vanilla SICL；主方法 MetaSICL 为 LoRA post-training | MyST、RSR、MMAU、MMAR、Common Voice de/zh/fr、CoVoST2 | no few-shot；Vanilla SICL；MetaSICL1/2/3；direct fine-tuning | WER、CER、accuracy、BLEU | 只复用原始 checkpoint 的 direct 与 Vanilla SICL；LoRA 行是合同外文献对照。论文未充分写清 MMAU/MMAR 的 demonstration pool，必须先补协议证据 |
| TICL, 2509.13395 | Whisper pseudo-label + text-embedding KNN 选择 speech demonstrations | Common Voice 15.0、GLOBE-V2、L2-ARCTIC、MyST、OGI、ENNI、RSR | k=0；uniform random；Whisper、HuBERT、ECAPA-TDNN、WavLM retrieval；TICL | WER；zh/ja/th 使用 CER；relative WER reduction；pseudo-label WER | R1 通用 ASR 主参考：数据、split、shots、检索基线和指标都可直接复用；论文也提供明确负结果 |
| TICL+, 2512.18263 | TICL top-300 semantic candidates 后用 Whisper acoustic embedding rerank | MyST、OGI、ENNI、RSR | zero-shot；TICL k=1–4；TICL+ k=1–4 | WER；相对 zero-shot/TICL 的 WER reduction | 已有声学重排方法；仅在原儿童 ASR 数据上作参考复现，不把儿童 ASR重新升为 R1 主线 |
| ByCS, 2404.14716 | 基于 inverse inference 的 Bayesian example selection | RASC863 重庆/广州方言词；CORAAL <15s | random；KATE+；ByCS；gold-owned oracle ByCS | WER；中文按字符计算 | 提供更重的示例选择边界基线；oracle 只作离线论文对照，不能进入 runtime；Whisper encoder-decoder 结果不能直接视为 Omni API 结果 |
| Thinking with Sound, 2509.21749 | 冻结 LALM 在推理中调用音频处理工具并重新编码 waveform | MELD；作者构造的 MELD-Hard1k | baseline LALM；TwS；operator leave-one-out | emotion classification accuracy；absolute accuracy gain | 说明 query-side audio processing 已有直接工作。MELD-Hard1k 未正式发布前不得由本项目重建为自己的数据资产 |
| Chain of Modality, 2604.14520 | Planner 选择 modality subset、顺序和 parallel/sequential/interleaved topology；intuitive 路径 training-free | Music-AVQA、AVHBench、OmniBench、DailyOmni、WorldSense；分析任务另有 AV-Odyssey、AV-Counting | 固定 sequential/parallel/interleaved；Qwen/Ola direct；ThinkOmni；专用模型 | accuracy | 说明输入顺序/拓扑效果具有任务异质性；仅作为 audio-visual omni 的独立参考。PRD 分析路径使用 SFT，不属于 R1 training-free 复现 |

## 4. 文献归纳出的稳定事实

### 4.1 已经成立的事实

1. **语音/音频 few-shot ICL 不是空白。** Audio Flamingo、MiMo-Audio、MetaSICL、TICL/TICL+ 和 ByCS
   已分别覆盖能力展示、vanilla SICL、语义检索、声学重排和 inverse-inference selection。
2. **示例是否有益具有明显异质性。** MetaSICL Table 2 中，Qwen2.5-Omni 的 Vanilla SICL 在
   Common Voice de/fr 上降低 WER，却把 zh 的 CER 从 7.29 提高到 8.07；TICL 在 Common Voice 的
   de/es/zh 上也出现退化。
3. **示例数量不是越多越好。** TICL 在 GLOBE-V2 上测试 `k∈{1,2,3,4,10,15,20}`，论文报告超过约
   4 个 demonstration 后收益有限且可能下降。
4. **选择方法的收益依赖任务和候选池。** ByCS 在小 `k` 时相对 KATE+ 更明显，随着 `k` 增加优势缩小；
   论文也明确指出短答案、候选多样性不足和 inverse-inference 成本是限制。
5. **query-side 操作已有方法证据，但不能与 demo 方法自动合并。** TwS 在 clean MELD 上只提升
   0.43–1.56 个百分点，却在作者的 perturbed set 上提升 11.38–36.61 个百分点；CoM 的收益也随模型、
   子任务和 topology 变化，存在负增益单元格。

### 4.2 仍待复现而不是待“创新”的问题

- Qwen3-Omni-30B 的本地 llama.cpp serving lane 是否支持论文所需的多 audio demonstration 输入与稳定解析。
- TICL 在 Qwen3 核心、参考数据和原始检索器上的结果是否保持原论文排序。
- MMAU/MMAR 的合法 demonstration pool 是否能从论文补充材料或官方代码中被唯一还原。
- 不同论文使用的模型、prompt、split、shots 和指标口径能否形成同模型、同数据的可比矩阵。
- TwS/CoM 的官方实现与作者自建数据是否发布到足以做原方法复现的程度。

这些都是复现与可比性问题。答案可能是“不能复现”或“只在部分条件成立”，仍然构成有效研究结论。

## 5. 数据集方案

### 5.1 R1 主数据集

| 优先级 | 数据集 | 复用的论文协议 | 指标 | R1 决定 |
|---|---|---|---|---|
| P0 | Common Voice 15.0 | TICL：validated split 作 demonstration pool，official test 作评估；1–15 秒 utterances；覆盖 de/en/es/fr/it/ja/pt/zh/nl/pl/ru/th/tr | WER；zh/ja/th 用 CER | **采用，通用 ASR 主载体** |
| P0 | GLOBE-V2 | TICL：train+validation 作 demonstration pool，official test 评估；`k=0..4` | WER、relative WER reduction | **采用，口音 ASR 载体** |
| P0 | L2-ARCTIC | TICL：train+validation 作 demonstration pool，official test 评估；`k=0..4` | WER、relative WER reduction | **采用，非母语口音 ASR 载体** |
| P1 | MMAU | MiMo-Audio 5-shot；MetaSICL public test + official scripts | accuracy，含 speech/sound/music 分项 | **采用为 AU 评估载体；few-shot pool 未闭合前只确认 direct 协议** |
| P1 | MMAR | MetaSICL public test + official scripts | accuracy，按 modality/subcategory 分项 | **采用为 AR 评估载体；few-shot pool 未闭合前只确认 direct 协议** |

### 5.2 只用于原论文复现或边界检查的数据集

| 数据集 | 用途 | 限制 |
|---|---|---|
| RASC863、CORAAL | ByCS 原方法复现 | 保持论文候选池、`k` 和 WER 口径；不替代通用 ASR 主线 |
| MyST、OGI、ENNI、RSR | TICL/TICL+ 原方法复现 | 儿童 ASR 只作支持证据，不承担 R1 主结论 |
| CREMA-D、RAVDESS、UrbanSound8K、GTZAN、Medley-solos-DB、AudioCaps | Audio Flamingo 方法/指标对照 | 结果来自专门训练的 Audio Flamingo，不能作为 Qwen3 的已知基线 |
| SpeechMMLU | MiMo 5-shot 复现候选 | 只使用作者正式发布版本；不自行 TTS 合成新的 SpeechMMLU |
| MELD | TwS 原始 clean 任务载体 | 只在复现 TwS 时使用原始公开数据和原标签 |
| Music-AVQA、AVHBench、OmniBench、DailyOmni、WorldSense | CoM training-free 路径复现候选 | 属于 audio-visual omni 支线，不承担 speech 主结论 |

### 5.3 明确排除

- 自采、自标、自合成或自行扩增的新数据集。
- 未发布的 MELD-Hard1k 本地重建版。
- 用 test item 互相充当 demonstrations 的 leave-one-out 伪 few-shot。
- 为了让方法工作而重新划分且无法对应参考论文的私有 split。
- 将 Common Voice、MMAU、MMAR 等不同论文版本的数字直接混在一张无版本说明的表中。

## 6. 实验基线方案

### 6.1 通用 ASR 主线：完整复用 TICL

| 编号 | 基线 | 来源 | 条件 |
|---|---|---|---|
| A0 | direct / zero-shot，`k=0` | TICL | 同模型、同 prompt、同 decoding |
| A1 | uniform random demonstrations | TICL | 与检索方法同 `k`、同 pool |
| A2 | Whisper embedding retrieval | TICL | 原论文声学/内容检索基线 |
| A3 | HuBERT retrieval | TICL | 原论文 content-oriented baseline |
| A4 | ECAPA-TDNN retrieval | TICL | 原论文 speaker-oriented baseline |
| A5 | WavLM retrieval | TICL | 原论文 speaker/content baseline |
| A6 | TICL text-embedding KNN | TICL | Whisper-large-v3-turbo pseudo-label；单语/多语 MPNet 按论文切换 |

示例数先严格复用 `k=1,2,3,4`；TICL 的 `k=10,15,20` 只用于 GLOBE-V2 的 paper-defined shot ablation。

### 6.2 AU/AR 主线：完整复用 direct 与 Vanilla SICL

| 编号 | 基线 | 来源 | 条件 |
|---|---|---|---|
| U0 | direct / no few-shot | MetaSICL、MiMo-Audio | MMAU/MMAR 官方评估脚本 |
| U1 | Vanilla SICL | MetaSICL | 仅在 demonstration pool、retrieval 和 prompt 能由论文/官方代码唯一还原后运行 |

MetaSICL1/2/3 是 LoRA post-training，不是 R1 的可执行 baseline；它们只保留为“训练后可达到什么结果”的
文献对照。MiMo-Audio-7B-Base 的数字也只用于论文背景，不替代 Qwen3 核心上的本地结果。

### 6.3 独立边界基线

- **TICL+：** zero-shot、TICL、TICL+，只按其儿童 ASR 原协议复现。
- **ByCS：** random、KATE+、ByCS；oracle ByCS 只作 gold-owned 离线论文对照。
- **TwS：** baseline LALM、TwS、operator leave-one-out；只有官方方法资产和数据闭合后才进入复现。
- **CoM：** fixed sequential、parallel、interleaved 与 training-free CoM；分析任务的 SFT PRD 路径不进入 R1。

上述方法之间不做未经参考论文定义的“全组合菜单”，不增加自适应路由器，也不把多个方法拼成一个新系统。

## 7. 评价指标与报告体系

| 任务 | 主指标 | 参考来源 | 报告要求 |
|---|---|---|---|
| 通用/口音 ASR | WER ↓ | TICL、MetaSICL、ByCS | 按 dataset/language 单独报告；可附 relative WER reduction |
| 中文/日文/泰文 ASR | CER ↓ | TICL；MetaSICL 对中文使用 CER | 不与 WER 直接平均 |
| 儿童 ASR | WER ↓ | TICL/TICL+；MetaSICL | 若复现 MetaSICL，保留其 utterance-level WER cap-at-1 口径并单独标记 |
| AU/AR、单标签分类 | accuracy ↑ | MetaSICL、MiMo-Audio、Audio Flamingo、TwS、CoM | 报告总体值和论文已有 subgroup/category 值 |
| SpeechMMLU | accuracy ↑ | MiMo-Audio | 四种输入/输出模态分别报告，不混成未定义综合分数 |
| Speech Translation | BLEU ↑ | MetaSICL | 仅在复现 CoVoST2 支线时使用 |
| Audio Captioning | CIDEr ↑ | Audio Flamingo | 仅在复现 AudioCaps 支线时使用 |
| Multi-label classification | F1 ↑ | Audio Flamingo | 仅对论文定义的 multi-label 任务使用 |
| Dialogue | CIDEr、BLEU4、ROUGE-L ↑ | Audio Flamingo | 仅对原 dialogue 任务使用 |

所有主结论保留任务原始指标。论文未使用的跨任务平均分、utility、headroom、oracle recovery 或新阈值不进入
R1 评价体系。

## 8. 研究方法与后续复现顺序

### 8.1 Stage‑1C：本报告已经完成的工作

1. 对八篇直接论文逐篇抽取研究问题、方法、数据、split、baseline、metric、主要发现和限制。
2. 用 PDF 原页核验 Audio Flamingo、MetaSICL、TICL、ByCS、TwS、CoM 的关键实验表。
3. 把儿童 ASR 从主线降为支持性复现，把 Common Voice 15.0、GLOBE-V2、L2-ARCTIC 确认为通用 ASR 主载体。
4. 删除旧稿的自建数据、MELD-Hard1k 本地重建和自定义指标设计。
5. 把“是否创新”改为“是否值得做严格复现与比较”的推进判断。

### 8.2 日落后的复用原则

1. 不为 R1 单独冻结 Stage-2B 协议，也不要求在其他方向之前完整复现八篇方法。
2. 某个保留方向若使用 speech demonstrations，只复现与该方向实验直接相关的 direct/random/TICL 等基线。
3. TICL/TICL+/ByCS 的检索与信用线索按需进入 R3/R4/R6/R8；TwS/CoM 的工具动作与模态拓扑按需进入
   R4/R5/R6/R8。
4. 数据、split 和指标继续遵守本报告第 5–7 节，不因重路由而允许自建数据或自定义总分。
5. Audio Flamingo、MiMo-Audio、MetaSICL 的训练贡献只保留为模型能力上界或合同外边界。

## 9. 是否值得独立推进：审计判断

### 9.1 日落理由

- **没有独占研究问题。** “模型是否有 ICL”已被回答；“哪种已发表方法更好”是基线复现。
- **基线义务重复。** 任何实际使用 context action 的保留方向都必须在自己的数据与预算下运行相应基线。
- **方法类别并不统一。** demonstration retrieval、inverse inference、active audio tool use 和 modality topology
  改变的是不同系统变量，强行并入 R1 会遮蔽它们对 R3–R8 的真正作用。
- **剩余空间会越过当前边界。** 只有设计新的 selector/controller 或统一评价体系才能让 R1 重新成为独立
  方法问题，而 Stage-1C 明确不做这些事情。

### 9.2 最终判定

**`NO_GO_AS_STANDALONE_DIRECTION__SUNSET_BEFORE_STAGE2`。**

R1 的高质量报告价值在于完成方向淘汰：文献归纳、数据、基线和指标继续保留；R1 task ID、独立实验包与
Stage-2B 路线终止。后续方向不得把“先完整执行 R1”设为进入条件。

## 10. Provenance、目的链与失效条件

**目的链。** 项目总目标 → Stage‑1C 研究方向确认 → R1 研究内容/数据/基线/指标闭合 → owner 判断 →
R1 日落并把可复用基线重路由到保留方向。

**Provenance。** 直接证据为仓外 hash-registered PDF：2402.01831、2512.23808、2601.18904、
2509.13395、2512.18263、2404.14716、2509.21749、2604.14520；前六篇登记在
`wiki/survey/registry/stage1c-r1-context-icl-2026-07-27-papers.jsonl`，TwS/CoM 由 Stage‑1C D1 dossier
记录。关键表格在本次分析中通过 PDF 原页复核。论文数字是原论文结果，不是本项目实验结果。

**失效条件。** 以下任一情况触发原位修订：论文新版本改变关键协议或结果；官方资产证明 dataset/split 与
本报告不同；Qwen3-Omni 服务的接口能力与假设不符；owner 改变通用 ASR 主线或“只复用参考数据/指标”的
边界；新的直接论文使当前方法矩阵明显不完整。任何修订仍不得自动授予实验执行或创新探索权限。
