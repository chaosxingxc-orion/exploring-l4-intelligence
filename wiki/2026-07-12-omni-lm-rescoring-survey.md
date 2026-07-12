---
title: "后融合 / LM 重排序如何引入 omni 模型：四透镜综合调研（omni 二遍解码研究现状裁定 + 存量池离线重排序实验设计）"
date: 2026-07-12
stage: 1-problem-definition
status: "调研综合（Lens1 经典后融合 / Lens2 LLM-GER training-free / Lens3 omni 二遍解码研究现状 / Lens4 空）；claim 逐条 VERIFIED(source)/UNVERIFIED；owner 定向：后端=数据集无关 reward 供给，不立后融合研究线"
supersedes: null
feeds: ["2026-07-12-retrieve-discover-use-analysis.md §2-3（『重排序调研在途』的落地）", "Proposal-B（deployable selector 跨 cohort/model/corpus）"]
---

# 后融合 / LM 重排序如何引入 omni 模型

> **本文定位（owner 定向，2026-07-12）**：这是 retrieve-discover-use 分析里挂账的「重排序调研（在途）」。
> owner 已裁定：**后端（重排序/验证器）不作为独立研究方向**，只收割「哪些信号数据集无关、且与生成器误差
> 去相关（δ_corr）」，供**前端**发现段触发 / 使用段信任校准。因此本调研的任务不是论证「要不要做后融合」，
> 而是：(a) 把这条已成熟、已拥挤的研究线**认账**（谁已做、做到什么程度，避免误称新颖）；(b) 提炼**唯一
> 可移植的 training-free 原语**；(c) 用存量池给出一张**离线重排序实验的臂表**，把 Proposal-B 的 endpoint
> 选择与 δ_corr 验证器臂钉死。
>
> Lens4 未返回（null）；本文由 Lens1（经典后融合/rescoring）、Lens2（LLM-GER training-free）、
> Lens3（omni 二遍解码研究现状）三份透镜合成，每条 load-bearing 事实标 VERIFIED(来源) 或 UNVERIFIED。

---

## §1 owner 的问题：后融合 / LM 重排序如何引入 omni 模型；谁已研究

**问题拆成三问：**

1. **机制问**：把一个「LM 第二遍」挂到端到端 omni chat 模型上，有哪些接法？——四类（全部 training-free 除非注明）：
   (a) **shallow fusion**（beam search 内在线融合 n-gram/NNLM 分数）；(b) **N-best / lattice 重排序**
   （二遍对 k-best 或 lattice 重打分，LSTM/Transformer/BERT-PLL）；(c) **generative error correction (GER)**
   （把 N-best 喂 LLM 让它重写出转写，可越过 N-best oracle）；(d) **internal-LM 扣除 / density-ratio**
   （减掉声学模型自带的语言先验再融合外部 LM）。判据见 §2–§3。
2. **裁定问**：这套机器**已经**被挂到 omni chat 模型自己的 N-best 池上、做过 training-free 系统研究了吗？
   ——**没有；这是空白**（§4 裁定）。整条 GER/rescoring 正典的 N-best 来源都是**经典 ASR**（Whisper/Conformer/RNN-T），
   纠错器是**独立文本 LLM**；把它跑在 Qwen3-Omni 自己的 25 候选池上、training-free、带显式 δ_corr 去相关约束，是未占格。
3. **归属问（owner 直令：给出主导团队名单）**：见 §4。一句话——**NTU-新加坡⟷NVIDIA⟷IBM 的 GER 集群**
   （连接人 Chao-Han Huck Yang / NVIDIA）是最深的一条线；**剑桥 CUED（Ma/Gales/Knill）**拥有 training-free/冻结分析线；
   **ROVER/Fiscus(1997)** 是 δ_corr 的正典祖先。

**为什么这问题现在才问**：我们的存量池（`_repro/asr_bon_v2_*.json`）已在冻结 Qwen3-Omni-30B Q8 GGUF 上
生成了 test.other 的 25/8 候选池并跑了 deployable-selector battery（§5、§6）。后融合文献恰好告诉我们
**这些候选能被重排榨出多少、榨不出多少、以及在什么 WER 区间会反伤**——这是把 Proposal-B endpoint 钉死
所需的先验。

---

## §2 经典后融合对 2% 量级的贡献账（clean / other 分列）

**核心裁决（load-bearing）：把 LibriSpeech 打到 ~2% 的是声学 / E2E 模型本身，不是 LM 第二遍。** 逆律
非常锐利、可复现：**第一遍越强，外部 LM 越无用**。强第一遍上，training-free 外部 LM 只买到 **~9–16% 相对** WER；
著名的「30% 相对」是在 2019 年**弱基线**（~7% test-clean 地板）上测的，落点 ~5% 而非 ~2%。

| 系统（第一遍） | 团队 / 出处 | 无外部 LM (clean/other) | 有外部 LM (clean/other) | LM | 相对增益 | 状态 |
|---|---|---|---|---|---|---|
| Conformer-L transducer (118M) | Gulati+, Google, IS2020 (2005.08100) | **2.1 / 4.3** | **1.9 / 3.9** | 3-layer LSTM w4096 | 9.5% / 9.3% | VERIFIED(Lens1: PDF Table 2) |
| Conformer-S (10M) | 同上 | 2.7 / 6.3 | 2.1 / 5.0 | 同上 | 22% / 21% | VERIFIED(Lens1) |
| Zipformer pruned-transducer (icefall) | k2-fsa/icefall docs | **3.11 / 7.93** | SF 2.77/7.08；**LODR 2.61/6.74** | RNNLM SF + bi-gram | SF 11%；LODR 16%/15% | VERIFIED(Lens1: LODR.rst) |
| Zipformer n-best rescore（同模型） | icefall | 3.11 / 7.93 | beam4 2.93 → beam12 **2.59/6.86** | RNNLM n-best | ≤17%/13% | VERIFIED(Lens1: rescoring.rst) |
| wav2vec2 LARGE (LV-60k, 960h) | Baevski+, FAIR, NeurIPS2020 (2006.11477) | ~2.2 / 4.5（近似） | **1.8 / 3.3** | 20-block Transformer LM | ~18% / ~27% | 有 LM VERIFIED(Lens1)；**无 LM 数 UNVERIFIED**（不在 camera-ready 表内） |
| Attention enc-dec (AED, LS-960) | Zeineldeen+, RWTH, IS2021 (2104.05544) | **4.10 / 10.88** | SF 2.90/7.59；**best-ILM 2.63/6.74** | 24-layer Transformer LM | SF 29%/30%；ILM 再 ~10% | VERIFIED(Lens1: PDF Table 2 文本抽取) |
| ESPnet BLSTMP（弱 2019 E2E） | Salazar+, Amazon, ACL2020 (1910.14659) | **7.26 / 20.37**（100-best base） | RoBERTa-large **5.05 / 16.79** | RoBERTa-large PLL | **30% / 18%** | VERIFIED(Lens1: PDF Table 2) |

**三条对我们最要命的读数：**
- **强 transducer 上 LM 只值 ~9–16% 相对**（Conformer 2.1/4.3→1.9/3.9；Zipformer LODR ~15%）。→ 我们若已在
  强第一遍上，重排的天花板就是这个量级，不会有 30%。
- **AED 的 30% 是它自带内部 LM 弱/失配**：外部 Transformer LM + 扣内部 LM（ILM/density-ratio）才拿到大增益。
  Qwen3-Omni 是自回归解码器，自带极强内部 LM——所以外部文本 LM 对它更像 AED 里「已经扣过」的状态，
  预期外部 LM 增益**偏弱端**（<10% 相对）。UNVERIFIED（无 omni × 外部 LM 直接测量）。
- **oracle 头空大但生成式 LM 只兑现一小部分**：Salazar 100-best oracle 2.81/12.85 vs 实现 5.05/16.79——
  **头空是选择/去相关问题**，正是 δ_corr / deployable-selector 的靶。经典文献的话：单个生成式 LM 把大部分
  oracle 头空留在桌上。

**方法族**（全 training-free 除非注明；VERIFIED(Lens1) 除另注）：shallow fusion（Kannan+ 2018 Google 分析）；
N-best/lattice 重排序（RWTH Beck/Irie/Ney）；**MLM/BERT-PLL 重排序（Salazar 2020，training-free，最贴我们）**；
internal-LM 扣除族——DR(2002.11268)/HAT(2003.07705)/ILME(2011.01991, 报 8.1–15.5% 相对跨域、2.4–6.8% 同域)/
**LODR(2203.16776, 清华 SPMI+美团，bi-gram 廉价替代)**；**MWER 判别式重排（RescoreBERT 2202.01094，需训练——出界，但界定了「训练能比冻结 PLL 多榨多少」= LibriSpeech clean/other 6.6%/3.4% 相对）**。

**LM 要多大？** Salazar RoBERTa-**base**(125M) 已达 5.25/17.18，large(355M) 只挪到 5.05/16.79——**多数增益在 base 规模**；
Gu+ 2023(2306.15815) 判别式重排 WER 随数据/模型 2+ 数量级幂律，**边际递减快**。→ 我们若引外部文本 LM，
不需要大模型；但强第一遍上任何规模都只买小增益。

---

## §3 LLM 重排序与 GER 的 training-free 可用部分

**核心裁决（load-bearing）：off-the-shelf 冻结 LLM 的生成式纠错（GER）只在高-WER/含噪区间可靠有用；在强、低-WER
基线上通常中性到有害——过度纠错并幻觉（3–12% 输出词无音频/无 N-best 支撑）。** 安全的 training-free 工作点是
**N-best 受约束的选择/重排**（closest-mapping / rerank）：受 oracle 上界封顶、不能幻觉、正是我们的 deployable-selector。
自由改写才是 WER 反伤与幻觉的所在。

**冻结/zero-shot 下站得住的（可移植）：**
- **N-best 受约束 closest-mapping**（剑桥 Ma/Gales/Knill, 2307.04172, IS2023, 冻结 ChatGPT）：1-shot closest =
  **6.24%**（test-other），逼近有监督 T5(6.15%)，优于 baseline 6.90%；oracle 5-best = 4.59%。**「大 N 对 zero-shot
  很重要」——我们 N=25 远超他们的 5，有利**。VERIFIED(Lens2)。
- **冻结 in-context 重打分**（Amazon TAP, 2309.15649, ASRU2023）：冻结 LLM in-context rescoring 在 OOD 上与
  域内调优 LM 相当；「task-activating prompting」= 先让 LLM 复述任务再打分。**这是纯 prompted 冻结管线能打平的最强证据——
  但注意它是 rescoring，不是自由改写**。VERIFIED(Lens2)。

**冻结/zero-shot 下站不住的（不可移植，勿误引）：**
- HyPoradise / RobustGER / GenSEC 的 −40%~−77% 大数**全是 fine-tuned**（LoRA/adapter/full-FT）。
  VERIFIED(Lens2)。就连 HyPoradise 旗舰在**强低-WER 的 LibriSpeech test-other 上 fine-tuned GER 仍不涨**
  （3.7→3.8，+2.7% 反而更差）。VERIFIED(Lens2: 2309.15701)。
- **Apple 最强负面结果**（Gu+, 2405.15216）：冻结 LLM GER 灾难性劣化强基线——LibriSpeech 2.2/5.3 →
  Llama-70B 0-shot **8.8/13.0**；Mistral-7B 0-shot 32/37。「所有 LLM 都劣化基线」；**幻觉率 LLM 3–12%，
  专用 ECLM 0%**；结论「LLM 从根本上不适合纠正已经准确的 ASR」（30→20 行，5→3 崩）。VERIFIED(Lens2)。
- 剑桥#2(2409.09554)：unconstrained generation → 幻觉、可能升 WER。定性 VERIFIED；数字 UNVERIFIED(未抽表)。

**天花板 vs 安全的取舍：** fine-tuned **生成式**纠错能越过 N-best oracle（GenSEC 8.33 < oracle 9.32，靠外部知识）——
但那是他们的地盘且需训练。**选择/重排受 oracle 硬封顶、永不幻觉、可 training-free**——对强 ASR 的正确 training-free
原语。自由改写只该放在弃权门（Conservative Data Filtering, 2407.13300, EMNLP2024：不可从源音素/上下文推得就不改）之后。

**区间可预测、可在我们池上测**：预期选择/GER 在 **snr5**（高 WER、oracle 头空大）有用、在 **clean test-other**
（低 WER、过纠区）中性到有害。**必须 clean/snr5 分列报**，平均会掩盖效应。这与我们池的实测一致（§5）。

**再听（re-listening）= 当前前沿**：ClozeGER(2405.10025)/AVGER 把源音频喂回纠错器攻「盲纠错器」失效模式；
Qwen3-Omni 天然能再听——这是最强杠杆，但让 reward 变成音频接地，**Information-Boundary Guard 适用**（验证器不得见 golden 转写）。

---

## §4 omni 模型二遍解码的研究现状裁定 + 主导团队名单（owner 直令）

### 裁定：部分覆盖，owner 的确切配置是空白（PARTIALLY covered; the exact cell is OPEN）

- **已研究（须认账、勿称新颖）**：二遍重排 / N-best 重排 / GER 作为**范式**；错误去相关/互补系统作为组合增益的必要条件
  （ROVER）；self-consistency/best-of-N 作为 test-time 原语（通用 LLM，及 audio-LLM 上的 **QA**）。
- **空白（我们的开口）**：(1) 在 omni chat 模型**自己的 N-best 池**上做**ASR** 自/交叉重排——整条正典用**经典 ASR**
  作 N-best 源、**独立文本 LLM** 作纠错器，没人跑在 omni 自池上；(2) 带**形式化 δ_corr** 约束的跨模型验证——
  ROVER 有直觉、无现代 audio-LLM 实例、无绑定收敛证明的去相关界；(3) **ASR 的 self-consistency 本身欠研究**——
  多数投票假设离散答案，ASR 是开放序列，naive SC 不适用，需 ROVER 式词对齐或验证器/选择器（= 我们的 deployable-selector）。
- **一手负面基线（可直接对打）**：**Qwen3-Omni 的 Thinking 模式在 ASR 上劣于 Instruct**（更易幻觉）——
  Qwen 团队自己的内部 CoT「第二遍」使 ASR 变差。VERIFIED(Lens3: 2509.17765 §9.1 逐字引)。→「内部推理二遍失败、
  外部误差去相关验证成功」是干净、对比、可发表的框架，且 Qwen 报告替我们准备了负面 baseline。

### 主导团队名单（ranked by 占有深度，含最新立场）

1. **NTU-新加坡 ⟷ NVIDIA ⟷ IBM —— 现代 GER 主导线（THE team）。** 核心复现作者：**Yuchen Hu, Chen Chen,
   Eng Siong Chng (NTU); Chao-Han Huck Yang (Georgia Tech→NVIDIA Research); Pin-Yu Chen (IBM/MIT-IBM);
   Sabato Marco Siniscalchi**。同一集群产出 HyPoradise(NeurIPS2023, 2309.15701)、RobustGER(ICLR2024, 2401.10446)、
   UADF(ICLR2024, 2402.05457)、ClozeGER(ACL2024 Findings, 2405.10025)、GenTranslate，并办 GenSEC(SLT2024, 2409.09785)。
   **Chao-Han Huck Yang (NVIDIA) 是连接人**（几乎每篇+Amazon TAP+GenSEC Task1 chair）。最新立场（2025）：转向
   audio-LLM-as-evaluator（ICLR2025）与多模态/再听 GER——**从纯文本 N-best 转向把音频喂回纠错器**。VERIFIED(Lens2+3)。
2. **剑桥 CUED —— Rao Ma, Mark Gales, Kate Knill。** training-free/prompting 分析线；提出 N-best T5 与 constrained
   vs unconstrained 区分、黑箱 ASR 无权重域适配（2307.04172 / 2409.09554）。**最贴我们「冻结模型 + logprob/PLL
   training-free 选择」的团队**。VERIFIED(Lens2+3)。
3. **Google —— 两遍/deliberation 谱系（Sainath 等）。** 两遍 E2E（RNN-T + LAS/deliberation rescorer）、
   Neural Oracle Search；density-ratio/HAT/ILM（McDermott, Sak, Variani；Meng 在 MS 延续 ILME）。**「第一遍出 N-best、
   二遍重排」的神经 E2E 正典源头**。VERIFIED(Lens1+3)。
4. **Amazon Alexa —— 判别式 + 生成式重排。** RescoreBERT(2202.01094)；TAP(2309.15649)；大语音-文本基座重排(2409.16654)。
   **工业级二遍重打分的规模化拥有者**；最贴我们「冻结模型 + logprob/PLL」framing。VERIFIED(Lens1+2)。
5. **NIST/ROVER —— Fiscus 1997 = δ_corr 正典祖先。** 「成功的系统组合要求构造具**互补错误**的多系统，否则组合不会
   超过任一单系统」——**这就是 δ_corr，被本领域 28 年前预注册**。给我们的收敛边界（相关错误⇒无增益）与可引正典。VERIFIED(Lens3)。
6. **Matsuo Lab, U-Tokyo —— test-time compute ON omni（最近邻，但 QA 非 ASR、非 training-free）。** AQA-TTRL
   (2510.05478, IS2026)：base = **Qwen2.5-Omni 7B/3B**，多数投票伪标签 + 置信加权 + 多次采样，**喂入 GRPO 权重更新（非 training-free）**，
   目标离散答案 QA（MMAU/MMAR/MMSU）。**同基座家族、同 self-consistency 原语，但更新权重且做 QA**。VERIFIED(Lens3: abstract fetch)。
7. **Meta/FAIR（wav2vec2/HuBERT + Transformer LM 解码）、k2/icefall+小米、清华 SPMI(Zhijian Ou)+美团（LODR）、
   JHU/ESPnet（Watanabe）** —— 强 AM + 廉价 LM 集成的实用线。VERIFIED(Lens1)。

**可锚 related-work 的综述**：「When LLMs Meet Speech: A Survey」(2502.19548)、「Non-Intrusive ASR Refinement: A Survey」
(2508.07285)——两者都把 rescoring/GER 归为**级联在经典 ASR 之后**，反证 omni-自池的空白。UNVERIFIED（综述具体数未抽）。

---

## §5 Qwen3-Omni 官方 ASR 数字 vs 我们 Q8 GGUF 的差距分解 + parity 可行性判定

### 两组数字（都 VERIFIED，但口径不同——这正是差距的来源）

**官方**（Qwen3-Omni Tech Report, arXiv 2509.17765, Table 6 / §5.1.2；VERIFIED(Lens3: HTML fetch)）：
`Qwen3-Omni-30B-A3B-Instruct` LibriSpeech **test-clean 1.22 / test-other 2.48 WER**；Flash 1.27/**2.44**。
对照 Qwen2.5-Omni 1.74/3.45；GPT-4o-Transcribe 1.39/3.75；Seed-ASR 1.58–2.84。**解码法未披露**——全报告无 beam/温度/LM
融合/N-best 字样，SOTA 2.48 用**朴素 direct/greedy 生成**取得。→ **官方 SOTA 把重排杠杆留着没用**。

**我们**（`_repro/asr_bon_v2_*.json`；VERIFIED(工件): 结果文件）：`qwen3-omni-30b-a3b-instruct **Q8_0 GGUF**
(llama.cpp, **-ngl 28**; audio **EXPERIMENTAL upstream**)`，LibriSpeech **test.other 子集 96 utts**，3 pool seeds，pool=8：

| 条件 | greedy corpus WER | oracle@8（非部署上界） | 最佳可部署 selector@8 | MBR@8 |
|---|---|---|---|---|
| clean 音频 | **5.79%**（macro 6.71%） | **3.57%** | **logprob@8 = 4.86%**（sig，−0.94pp） | 5.59%（ns） |
| snr5 | **9.73%** | **6.36%** | **logprob@8 = 8.91%**（sig，−0.82pp） | 9.24%（ns） |

（delta 约定：正=改善。clean logprob@8 从 5.79→4.86，n=96 下 corpus_sig=True；snr5 同。random/length selector 反伤。）

### 差距分解：official test-other 2.48% vs 我们 clean-音频 5.79%（≈3.3pp / 2.3×相对）

| 分量 | 方向/量级 | 状态 |
|---|---|---|
| **(a) 模型/checkpoint 身份** | 同权重（30B-A3B-Instruct）→ 贡献 ~0 | VERIFIED(model 字段一致) |
| **(b) 量化 Q8_0** | Q8_0 是最高保真量化，ASR WER 退化通常 <5% 相对（<~0.1–0.2pp）→ **不足以解释 3.3pp** | UNVERIFIED（无我们自测的 Q8 vs fp16 对照；先验来自通用量化文献） |
| **(c) 音频路径（llama.cpp omni audio EXPERIMENTAL + -ngl 28 部分 offload）** | **最可能的主导项**：上游 omni 音频前端仍实验性（mel/特征抽取、重采样、音频编码器移植保真度）→ 系统性抬高 WER | UNVERIFIED（未做 vLLM 参考路径 A/B；但 EXPERIMENTAL 标签 + 量级排除法指向此项） |
| **(d) 样本/测量** | 96-utt 子集 vs 官方 full test-other(2939 utts)；小-n 噪声 + 可能更难子集 | VERIFIED(n_utts=96) —— 方向已知、幅度 UNVERIFIED |
| **(e) 解码** | 官方很可能也 greedy → 非差异项 | UNVERIFIED（官方未披露） |

### parity 可行性判定（load-bearing）

**重排**不可能把我们的 Q8 GGUF 打到官方 2.48%：**存量池 oracle@8 = 3.57%（clean）> 官方 2.48%**——
连**违反信息边界的 oracle 上界**都够不着官方数。→ **差距由模型/量化/音频路径主导，不是解码选择问题；training-free
重排最多把 5.79→3.57 之间的头空兑现一部分（实测 logprob 兑现到 4.86）。** parity 是**工程修复**（修音频路径 /
换 vLLM 参考路径 / Q8→fp16 对照定位）而非 TFRL 结果。

**方法论后果**：TFRL 重排研究**不该以 parity 为目标**（结构性够不着）；应以「在给定第一遍（Q8 GGUF）上，
training-free 选择相对 greedy 的**可部署、跨条件增益**」为 endpoint——即 Proposal-B。parity 差距应作为**独立
engineering ticket**（修音频路径）挂出，不与 TFRL 效应混算。

---

## §6 存量池离线重排序实验设计（= Proposal-B；臂表 / 边界 / CPU 预算 / 与 δ_corr 的关系）

**这是 retrieve-discover-use §2-3 挂账的落地，也是 forensic 复审 Proposal-B 的实现。** 池已存
（`asr_bon_v2_clean.json` / `asr_bon_v2_snr5.json`：test.other 96 utts × pool8 × 3 seeds），**离线重排近乎免费**。

### 6.1 臂表（endpoint 预注册 = N=8 logprob；oracle 只作 headroom）

| 臂 | 类型 | 部署性 | 来源/依据 | 预期（先验） |
|---|---|---|---|---|
| greedy | 基线 | 部署 | 现状 | clean 5.79 / snr5 9.73 |
| **logprob@8** | 自模型置信 | **部署（THE endpoint）** | 现有 v2 | clean 4.86 / snr5 8.91（n=96 已 sig） |
| MBR@8 | 自一致（N-best 内互评 WER） | 部署 | 现有 v2 | 中性（ns） |
| random / length | 阴性对照 | 部署 | 现有 v2 | 反伤（must 反伤，验证选择器非平凡） |
| oracle@8 | 用 reference 选 | **非部署上界** | 现有 v2 | clean 3.57 / snr5 6.36（headroom 天花板） |
| **δ_corr 交叉验证器@8**（新） | 第二个 context-differentiated 冻结 omni 打分候选 | 部署 | §4-ROVER + omni-verifier memory | **本调研的新楔子**；开放问题=是否 > logprob | 
| 外部文本-LM PLL 重排@8（新，可选） | 冻结 BERT/小 LM 的 PLL（Salazar 式） | 部署 | §2 Salazar / §3 剑桥 | 强第一遍上先验偏弱（<10% 相对） |
| N-best-constrained closest-mapping（新，可选，弃权门后） | 冻结 LLM 受约束选择 | 部署 | §3 剑桥 6.24 vs 6.90 | 只在 snr5 试；clean 预期中性/有害 |

**明确不做**（owner 定向 + §3 证据）：自由改写 GER 作为研究对象、beam 级融合、任何需训练的接入（RescoreBERT/LoRA GER）。

### 6.2 边界（Information-Boundary Guard + 报告纪律）

- **信息边界**：选择/验证器**不得见 golden 转写**；oracle 臂显式标「非部署、违边界、只作 headroom」。
  δ_corr 验证器再听音频时，验证器 prompt 里绝不放参考。（回应 memory 里「信息边界过界=假增益」的失败模式。）
- **clean/snr5 分列**（§3 区间律：平均会掩盖）；**双分母 corpus_wer + macro_wer**；
- paired cluster（按 utterance group）bootstrap CI；预冻 **SESOI**；报 error-type S/D/I、**pool-collapse rate**、
  proxy-vs-oracle rank 相关（连 Proposal-C over-optimization）；
- **跨条件泛化门**（Proposal-B 判据）：至少再一 speech corpus + 另一语言/口音 + 另一 runtime/backbone；
  **若只在 clean 或单模型成立，不得称通用 TFRL**。

### 6.3 CPU 预算

- **logprob/MBR/random/length/PLL 重排**：纯离线、**CPU-only**，在存量候选上打分——**近零边际成本**（候选与 per-utt
  logprob 已存于 v2 工件）。外部文本-LM PLL 可在 CPU 跑小 BERT（Salazar 显示 base 规模已够）。
- **δ_corr omni 验证器臂**：需 GPU（llama-server resident），对存量音频+候选做二遍打分——重于 CPU 臂，但仍是
  **对已生成池的一遍推理**，不重生成。遵守 [[wsl-detached-run-gotchas]]（`python -u`、`HF_HUB_OFFLINE=1`、
  embedder 上 CPU 让 GPU 给 llama-server、按路径 kill 不自杀）。
- 与 GPU 会话协调：launch 前查 pgrep + gpu_session lock（[[concurrent-sessions-coordination]]）。

### 6.4 与 Proposal-B / δ_corr 的关系

- **这就是 Proposal-B**：endpoint 不变（logprob@8），但按 retrieve-discover-use 重定位为**「reward 信号的跨域标定」**，
  服务前端发现段触发 / 使用段信任校准——**换数据集不换信号定义**（数据集无关性正是「更通用」的兑现）。
- **δ_corr 是唯一新研究内容**：logprob@8 = 单系统自置信；δ_corr 臂 = 两个 context-differentiated 冻结 omni
  （生成器-agent + 验证器-agent，同权重、异 system-prompt）→ ROVER 意义上的互补错误。**开放问题**（本调研提出、
  存量池可低成本回答）：**context-differentiated omni 验证器是否比 n-gram/BERT/logprob 关掉更多 oracle 头空
  （5.79→3.57 的那段）？** 收敛：δ_corr→0 时 realized_gap→oracle（C4 `realized_gap_le_two_tau`）；
  残余不可约地板 = 共享知识盲点（PARKED → W4 omni-embedding 作 M-无关信号）。

---

## §7 Claim ledger（逐条状态）

| # | Claim | 状态 / 来源 |
|---|---|---|
| C1 | 强第一遍上 training-free 外部 LM 只买 ~9–16% 相对 WER（Conformer 2.1/4.3→1.9/3.9；Zipformer LODR ~15%） | **VERIFIED**(Lens1: 2005.08100 Table2; icefall LODR.rst) |
| C2 | 「30% 相对」是弱基线现象（Salazar 7.26/20.37→5.05/16.79，落点 5% 非 2%） | **VERIFIED**(Lens1: 1910.14659 Table2) |
| C3 | oracle 头空大但单生成式 LM 只兑现一小部分（Salazar oracle 2.81 vs 实现 5.05） | **VERIFIED**(Lens1) |
| C4 | wav2vec2 无 LM 数 ~2.2/4.5 | **UNVERIFIED**（不在 camera-ready 表；有 LM 1.8/3.3 VERIFIED） |
| C5 | 冻结 LLM 自由改写 GER 在强低-WER 上灾难性劣化（Apple: 2.2/5.3→70B 8.8/13.0；幻觉 3–12%） | **VERIFIED**(Lens2: 2405.15216) |
| C6 | GER 大数（−40~−77%）全是 fine-tuned；LibriSpeech test-other 上连 fine-tuned 也不涨（HyPo 3.7→3.8） | **VERIFIED**(Lens2: 2309.15701) |
| C7 | 冻结 N-best-constrained closest-mapping training-free 可小赢（剑桥 6.24 vs 6.90，N=5；oracle 4.59） | **VERIFIED**(Lens2: 2307.04172) |
| C8 | 冻结 in-context 重打分 OOD 与调优 LM 相当（Amazon TAP） | **VERIFIED**(Lens2: 2309.15649) |
| C9 | GER/rescoring 正典 N-best 源=经典 ASR、纠错器=独立文本 LLM；omni-自池 training-free 二遍解码=空白 | **VERIFIED**(Lens2+3 交叉：三份综述 + 全部一手论文均级联结构) |
| C10 | Qwen3-Omni 官方 test-clean 1.22 / test-other 2.48（Instruct）；解码法未披露（朴素 greedy） | **VERIFIED**(Lens3: 2509.17765 Table6/§5.1.2 HTML) |
| C11 | Qwen3-Omni Thinking 模式在 ASR 上劣于 Instruct 且更易幻觉（内部 CoT 二遍失败） | **VERIFIED**(Lens3: 2509.17765 §9.1 逐字引) |
| C12 | 我们 Q8_0 GGUF (llama.cpp -ngl28, audio EXPERIMENTAL) test.other 96utt clean greedy=5.79%；oracle@8=3.57%；logprob@8=4.86%(sig) | **VERIFIED**(工件 asr_bon_v2_clean.json) |
| C13 | snr5：greedy 9.73%；oracle@8 6.36%；logprob@8 8.91%(sig) | **VERIFIED**(工件 asr_bon_v2_snr5.json) |
| C14 | parity 不可由重排达成：oracle@8(3.57%) > 官方(2.48%)——差距由音频路径/量化/子样主导 | **VERIFIED**(算术: C10 vs C12) — 各分量归因幅度 **UNVERIFIED**（无 Q8-vs-fp16 / vLLM-vs-llama.cpp A/B） |
| C15 | Q8_0 量化对 ASR WER 退化通常 <5% 相对，不足以解释 3.3pp | **UNVERIFIED**（无自测；通用量化文献先验） |
| C16 | llama.cpp omni 音频路径 EXPERIMENTAL 是差距最可能主导项 | **UNVERIFIED**（量级排除法 + EXPERIMENTAL 标签；未 A/B） |
| C17 | ROVER(Fiscus 1997) 的「互补错误」要求 = δ_corr 的正典祖先 | **VERIFIED**(Lens3) |
| C18 | AQA-TTRL(Matsuo, IS2026) = 最近邻但权重更新 + QA 非 ASR | **VERIFIED**(Lens3: 2510.05478 abstract) |
| C19 | δ_corr context-differentiated omni 验证器是否 > 单模型 logprob | **OPEN**（本调研提出；存量池 §6.1 可低成本回答） |
| C20 | Lens4 未提供（null） | **N/A** |

---

### 一句话结论

omni 二遍解码是**部分覆盖、owner 确切格空白**：THE team = **NTU⟷NVIDIA⟷IBM GER 集群（连接人 Huck Yang）**
+ 剑桥 CUED + ROVER/Fiscus 祖先；**唯一可移植 training-free 原语 = N-best-受约束选择（logprob@8 / closest-mapping / PLL），
不是自由改写 GER**；存量池离线重排（Proposal-B + δ_corr 臂）是**每 CPU-小时信息量最高**的一步——池已存、CPU 近免费，
且能同时裁定「logprob 增益是否可部署跨条件」与「δ_corr omni 验证器是否比单模型多关头空」这两个未决问题。
**parity 由重排够不着（oracle 3.57% > 官方 2.48%），是工程 ticket 不是 TFRL 结果。**
