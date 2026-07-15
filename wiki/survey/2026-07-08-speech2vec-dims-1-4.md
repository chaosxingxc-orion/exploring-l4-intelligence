# 2026-07-08 · speech2vec 调研附录 A：维度 1–4 明细（ssl-general / audio-text-align / speech-sentence-retrieval / task-specialized）

> **来源**：8-finder Opus workflow（run wf_1d75e256-bf9）的结构化产出，经 40 条对抗验证
> （34 CONFIRMED / 6 PARTIAL / 0 REFUTED）。**已按验证结果内联修正**（标 ⚠PARTIAL 处）。
> 主文档：`2026-07-08-speech2vec-survey-2025plus.md`（结论以主文档为准，本附录保留证据明细）。

## 1. ssl-general — 通用语音表征 2025+

| 模型 | 日期 | 来源 | 规模/显存 | License | 粒度 | 关键证据 |
|---|---|---|---|---|---|---|
| MERaLiON-SpeechEncoder-2 | 2025-09 | HF `MERaLiON/MERaLiON-SpeechEncoder-2` | 630M/~2.5GB | MERaLiON Public License | frame 50Hz | SUPERB: SID 88.96, ER 68.80, IC 98.95, SF-F1 89.50, ASR-WER 4.96；zh+en+code-switch ✅#7 |
| XEUS | 2024-07 | HF `espnet/xeus` | 577M | **cc-by-nc-sa-4.0（非商用）** | frame | 4057 语；ML-SUPERB 综合分第一 ⚠#23：ASR-CER 子项 MMS-1B(30.8) 反超 XEUS(34.1)；ESPnet-only 提取 |
| emotion2vec+ | 2023-12 | HF `emotion2vec/emotion2vec_plus_large` | 90–300M | model-specific | utt+frame 50Hz | IEMOCAP linear-probe WA 71.79% 胜 SSL 基线 ✅#34 |
| SenseVoice-Small | 2024-07 | HF `FunAudioLLM/SenseVoiceSmall` | ~234M | custom | utt | ASR+LID+SER+AED 50+ 语；zh/yue 相对 Whisper >50% 增益；15× 快 |
| Dasheng 0.6B/1.2B | 2025-08 | HF `mispeech/dasheng-1.2B` | 90M–1.2B | **Apache-2.0** | frame 1280d | HEAR 赢 CREMA-D/VoxLingua/SpeechCommands；ASR 内容保真未证 |
| Codec2Vec | 2025-11 | arXiv 2511.16639（无权重） | ~95M 级 | 未确认 | token+768d frame | SUPERB IC 97.1/SD 5.5/ER 65.4/ASR 7.2%ER，存储省 16.5×；en-only |
| S-JEPA | 2026-06 | github gioannides/s-jepa | <90M | CC-BY-4.0(code) | frame | <90M 档 SUPERB ASR 最低 WER（仅摘要）；无 zh、无权重 → watch-list |
| Qwen3-Omni AuT 编码器 | 2025-09 | 内嵌于 Qwen3-Omni | 宿主 30B | Apache-2.0 | frame ~12.5Hz | 20M h、80% zh/en；32/22 基准 SOTA/近 SOTA；无独立 checkpoint |
| TS-SUPERB（基准） | 2025-05 | arXiv 2505.06660 | — | — | frame | 多说话人场景 WavLM Base+/Large 领先；无单模型全胜 |
| ML-SUPERB 2.0（基准） | 2025-09 | arXiv 2509.07139 | — | — | frame | 200+ 语/56 方言；2025 最佳提交 CER −18%/方言 −30.2% |

**⚠PARTIAL #11（重要修正）**：MERaLiON-SE2 的数字准确，但"全任务族 competitive-to-SOTA"过强
——其自家对照表中 **WavLM-large 五项全部胜过它**；SID 88.96 是表中四模型最低（低于 HuBERT-large
90.33 和自家 v1 的 91.09，属回退），ASR-WER 4.96 也是四者最差。其真实价值 = **zh+en 覆盖**（WavLM
是 en-only），不是单项精度。

**pre-2025 背景**：WavLM（2021，en-only，多说话人场景至今最稳 speaker 键）；HuBERT（2021）；
w2v-BERT 2.0/SeamlessM4T 编码器（2023，被 XEUS/MERaLiON 超越）。

**开放问题**：无 2025 年同协议 head-to-head SUPERB 榜（MERaLiON vs XEUS vs WavLM vs Dasheng）；
MERaLiON/XEUS 隐层维度未文档化（推断 ~1024）；Codec2Vec/S-JEPA/Dasheng 无 zh 数字；
Qwen3-Omni AuT 塔能否经 llama.cpp GGUF 取出、12.5Hz 帧是否保留 speaker/emotion 结构未验证。

## 2. audio-text-align — 音频-文本对齐嵌入 2025+

| 模型 | 日期 | 来源 | 规模/显存 | License | 粒度 | 关键证据 |
|---|---|---|---|---|---|---|
| **GLAP** | 2025-06 | HF `mispeech/GLAP` | 0.9B/<2GB | **Apache-2.0** | utt | **LibriSpeech test-other R@1=93.8 vs MS/LAION-CLAP ~0.1** ✅#10；**AISHELL-2(zh) R@1=98.5** ✅#9；Clotho/AudioCaps 事件检索与 CLAP 持平 ✅#28；`encode_audio()` ✅#14 |
| LCO-Embedding-Omni-7B | 2025-10 | HF `LCO-Embedding/LCO-Embedding-Omni-7B` | 9B/~18GB fp16（有 3B GGUF） | **Apache-2.0** | utt | **MAEB 53 模型第一（52.2% avg）** ✅#35；未做音频对比训练即达 SOTA——frozen thinker 本身可检索；clustering 仅 1.7%（k-NN 几何偏弱） |
| MAEB（基准） | 2026-02 | arXiv 2602.16008 | — | open | utt | CLAP 系在 MInDS-14 意图近随机、多语跨模态检索 <3%；**无模型七类别全胜** |
| SEAL | 2025-02 | arXiv 2502.02603（无公开权重） | Whisper-L-v3+piccolo-zh | 未声明 | utt | zh KB Top-1 86.36 vs 级联 79.45（+8%）、延迟 −54%；轻适配层即可 |
| SLAP | 2026-01 | arXiv 2601.12594 | ~250M | 未声明 | utt | AudioCaps A2T R@1 63.4（胜 LAION-CLAP 45.0）；**零语音内容评测**——同患 CLAP 词汇盲区风险 |
| CLSP | 2026-01 | HF `yfyeung/CLSP` | ~0.7B | Apache-2.0 | multi-vector | 风格/副语言检索专用（FCaps 47k h 风格描述）；非内容键 |
| Omni-Embed-Audio | 2026-06 | ACL2026 | 未披露 | 未披露 | utt | 意图查询+难负例 +34.7% rel TFR@10；无语音词汇评测 |
| MSEB（基准） | 2026-02 | arXiv 2602.07143 | — | open | utt | 佐证 CLAP=事件类别键非词汇键；含 speaker-clustering 任务 |
| e5-omni | 2026-01 | HF `Haon-Chen/e5-omni-7B` | 7B/~14GB | **CC-BY-4.0** | utt | AudioCaps R@1 37.7 胜 Nemotron 20.5（p<0.05）；无语音词汇数字 |

**pre-2025 背景**：LAION-CLAP / MS-CLAP —— 2025-26 基准一致证实为 audio-EVENT 模型，
语音词汇内容检索 R@1≈0.1%（**这就是我们现有 KB 键的模型**）。

**开放问题**：强内容键（GLAP/LCO/SEAL）全部只发布 utterance 级数字，无 segment 级；
无模型同时在词汇+speaker+emotion 上联合评测；SEAL 权重/英文支持未确认；
7–9B LALM 嵌入器与生成模型在 24GB 上共驻的预算问题（回退 = 0.9B GLAP）。

## 3. speech-sentence-retrieval — 语音语义句向量与 speech-RAG 2025+

| 系统 | 日期 | 来源 | 规模 | License | 粒度 | 关键证据 |
|---|---|---|---|---|---|---|
| SENSE | 2025-09 | HF `LIA-AvignonUniversity/SENSE` | ~600M | cc0-1.0 | utt | VoxPopuli fr-en R@1 96.55 vs SONAR 91.91 ✅#3；对齐 BGE-M3 文本空间、纯 cosine ✅#5 ⚠#21：无所谓 "speech2vec pipeline"，卡片近空 |
| OmniSONAR | 2026-03 | arXiv 2603.16606（发布未确认） | ~1B 级? | CC-BY-SA-4.0（基座 SONAR NC） | utt | 单 checkpoint 177 语入文本 SONAR 空间 ✅#31；相似搜索误差 −43% ✅#36 |
| SEAL | 2025-02 | （见维度 2） | — | — | utt | zh KB 检索 +8% Top-1、延迟减半——最接近我们 KB 的公开蓝图 |
| WavRAG | 2025-02 | ACL2025 (2025.acl-long.613) | Qwen2-Audio ~8.4B | Apache 系 | utt | frozen-MLLM last-token 作键：R@1 T2S(SpokenSQuAD) .684、S2S(SLUE-SQA-5) .339（S2S 弱）；比 ASR 级联快 5–8× |
| SpeechRAG | 2024-12 | arXiv 2412.16500 | HuBERT-L+E5-Mistral-7B | 未见 | segment | SpokenSQuAD R@5 .970；冻结文本检索器、只蒸馏语音 adapter |
| VoxRAG | 2025-05 | arXiv 2505.17326 | CLAP ~150M | Apache-2.0 | segment | **CLAP 作 S2S 键：nDCG@10 仅 0.03（strict）** —— 反面教材 |
| Multi-Axis Factor-Partitioned | 2026-05 | github jimregan/spoken-sentence-transformers | frozen WavLM-base+ ~95M | CC-BY-4.0 | multi-vector | 冻结 WavLM 分解为语义/说话人/方言子空间、带符号加权 k-NN：跨库 P@1 65.5% vs 纯语义 0.3%（小规模） |
| GLM-Voice-RAG | 2025-05 | EMNLP2025 | SONAR 检索器 | SONAR NC | utt | 集成研究；放出 zh 语音 HotpotQA 数据集（可复用基准） |
| H-QuEST | 2025-08 | Interspeech2025 | wav2vec2+HNSW | 未确认 | token | 免转写子句 QbE 检索（数字见附录 B 维度 7 ✅#8/#12/#18） |

**开放问题**：OmniSONAR 可得性未确认；SENSE 维度推断 1024 未验证；
2025-26 无成熟语音 multi-vector/late-interaction 检索器；
无模型同时编码 speaker-ID/emotion —— 单键 vs 多子键仍未解。

## 4. task-specialized — 任务特化表征 2025+

| 模型 | 日期 | 来源 | 规模 | License | 关键证据 |
|---|---|---|---|---|---|
| **Emotion2Vec-S** | 2025-02 | HF `ASLP-lab/Emotion2Vec-S` | ~300M/<2GB | **Apache-2.0** ✅#6 | Emo-Emilia UA 80.66 vs emotion2vec 68.02（+12.6）✅#26 前半 ⚠#26：**M3ED-zh 真实增益仅 +1.8（23.82 vs 22.04）**——原 62.95/47.58 是 CASIA 错标；768d utt+50Hz frame 双粒度 ✅#22；emotion2vec drop-in ✅#38 |
| emotion2vec+ 系列 | 2024-05 | HF `emotion2vec/emotion2vec_plus_*` | ~90–300M | 未声明（核） | IEMOCAP linear-probe 胜 WavLM/data2vec ✅#34；带 9 类 SER 头（可自动产 KB value） |
| ReDimNet2 | 2026-03 | github PalabraAI/redimnet2 | 1.1–12.3M | 未确认 | Vox1 EER 0.29/0.52/0.99（B6, 12.3M）；权重可得性未核 |
| ReDimNet v1 | 2024-07 | torch.hub `IDRnD/ReDimNet` | 1–15M | **MIT** | Vox1-O ~0.58%（B6 无后处理）；192d；许可最干净的 speaker 键 |
| ECAPA2 | 2024-01 | HF `Jenthe/ECAPA2` | ~30M | **CC-BY-NC**（非商用） | EER 0.66/0.67/1.19 |
| **ERes2NetV2 / CAM++（3D-Speaker）** | 2024-06 | ModelScope `iic/speech_eres2netv2_sv_zh-cn` | 10–20M | **Apache-2.0** | Vox1-O 0.61%（全）/0.98%（3s）；**200k 说话人 zh + CN-Celeb 训练** —— zh speaker 键首选 |
| Vox-Profile（基准） | 2025-05 | github tiantiaf0627/vox-profile-release | 复用 WavLM/Whisper | permissive | 冻结通用编码器+线性头赢多数副语言维度；自然场景分类情感最佳仅 F1 0.416 → 专化模型在 SER 上仍有位置 |
| Kiwano（工具箱） | 2026-06 | github kiwano-toolkit/kiwano | 15–83M | Apache-2.0 | 统一 API + AS-Norm/QMF；fwSE-ResNet-200 全管线 0.34% EER |
| SenseVoice-Small | 2024-07 | （见维度 1） | ~234M | custom | 一次前向出 emotion+事件+多语 ASR **标签**——更适合当 value 生成器而非度量空间键 |

**pre-2025 背景**：ECAPA-TDNN（2020，至今默认 speaker 基线）；x-vector（2017）；
emotion2vec（2023-12，通用 SER 表征源头）。

**开放问题**：特化 vs 通用的裁决按任务分裂——SID 特化以 ~25× 更少参数打平/胜过通用、
curated SER 特化明显占优、自然场景副语言偏向通用，无单一来源一次裁决；
Emotion2Vec-S 无 MSP-Podcast 自然场景 head-to-head；zh 情感增益经验证只有 +1.8（⚠#26）
——**zh SER 键的实证空缺比调研初稿显示的更大**。
