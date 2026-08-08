---
title: "Published baselines per carrier: speech-aware evidence acquisition"
study_slug: "speech-aware-evidence-acquisition"
source_surveys: "study repo docs/readiness/2026-08-07-*.md (R0.1, model-free)"
maintained: "living page — 'ours' rows filled in place after each probe's ledger row lands"
---

# Published baselines per carrier (living table)

用途：R0.1 调查提取的**已发表数字**按载体列成对照表；小型探测（study 仓
`docs/readiness/2026-08-07-r1-replan-reproduction-plan.md` P1–P2）完成后，
在对应 "ours" 行就地回填，之后的提升工作以本表为基线面展开。

纪律：本页只登记摘要数值 + 指针；数字权威在 study 仓收据/MLflow 与各论文
原文。**跨行不可直接比较**，除非 protocol 列相同——不同论文的前端 ASR、
子集、判分器都不同；"ours" 行必须与其对照行同 protocol 同样本才有意义。
探测样本一律 discovery/dev split（split 冻结收据：discovery 44 / dev 10 /
confirmatory 115，study `docs/receipts/splits.json`）。

图例：`[abl]` = 该差值有原文消融/受控对照支撑；`(t)` = 训练所得（边界外，
仅作结构缺口对照）；**ours** 行初始为空，回填时附 ledger 行 id。

## earnings21 / earnings22 / conec（Family A）

| system / condition | protocol | metric | value | source |
|---|---|---|---|---|
| ConEC conventional ASR, no-bias floor | ConEC LREC-COLING 2024 | WER | 10.41（bias 条件带 10.29–10.66，聚合不敏感）| ConEC paper |
| Siskos black-box ASR, no-context | Siskos EMNLP-F 2025, E21 | WER | 35.9 | arXiv:2509.19567 |
| Siskos + CB-RAG context `[abl]` | 同上 | WER | 31.1 | 同上 |
| Siskos + CB-LLM context `[abl]` | 同上 | WER | 31.8 | 同上 |
| Siskos + oracle context `[abl]` | 同上 | WER | 29.7 | 同上 |
| RECOVER correction (t? — LLM 纠错管线，声称黑盒) | RECOVER preprint, E21 among 5 sets | rel. E-WER ↓ / recall ↑ | 8–46% rel / 最高 +22pp | arXiv:2603.16411（未评审，无码）|
| **ours: no-context / matched-ConEC / mismatched（R4=P2b=SAEA-E-002；T4 扩展=ConEC bias-list 实体类注入）** | 3-arm，earnings21-discovery 冻结 44 样本（2026-08-08 Route-1 重定标：e22 subset10 无注册 ConEC 证据层）；三臂 dry-run 已 FINALIZED | WER（实体级 WER 待 owner 钉 wer_tags 适配器）| — | 待回填 |

## slurp（Family B）

| system / condition | protocol | metric | value | source |
|---|---|---|---|---|
| Multi-ASR + HerMiT pipeline (t) | SLURP EMNLP 2020 官方 | IC-comb / SLU-F1 | 76.68 / 69.53 | arXiv:2011.13205 |
| 最优 adapted pipeline (t) | 同上 | 同上 | 78.33 / 70.84 | 同上 |
| gold-transcript NLU 上界 (t) | 同上 | 同上 | 84.84 / 78.19 | 同上 |
| CTI E2E (t) | CTI 2021 | IC / SLU-F1 | 82.93 / 71.12 | arXiv:2104.07253 |
| SFT Qwen2-Audio-7B (t) | ICASSP 2026 | IC / SLU-F1 | 88.13 / 76.75 | arXiv:2509.15389 |
| UniverSLU (t) | NAACL 2024 | IC | ~90.3（检索归因，冻结前复核）| arXiv:2310.02973 |
| zero-shot SF：ZS-Whisper-SLU → WHISMA (t) | 各自论文 | SLU-F1 | 50.0 → 63.3（监督参照 69.9）| arXiv:2408.16423 |
| AIR-Bench 直答（8 系统，最好 Qwen-Audio-Chat）| AIR-Bench 1k 子集，GPT-4 judge | acc | 77.8（最差 NExT-GPT 25.6）| arXiv:2402.07729 |
| AIR-Bench 级联 Whisper+GPT-4 `[abl]` | 同上 | acc | 87.7 | 同上 |
| **ours: direct vs self-cascade（R3=P2a）** | AIR-Bench 200 题配对，确定性判分 | acc | — | 待回填 |
| **ours: prompt-only slot filling（T3，plan P3 类比轨道）** | 官方 scorer，样本经 sample-once manifest 登记 | SLU-F1 | —（文献零先例；对位 ZS 线 50.0→63.3）| 待回填 |

## speech-massive（Family B）

| system / condition | protocol | metric | value | source |
|---|---|---|---|---|
| 级联 Whisper+mT5，跨语零样本 (t) | Interspeech 2024 官方 | IC avg / slot-F1 avg | 69.10 / 43.15 | arXiv:2408.03900 |
| 级联全量微调 (t) | 同上 | 同上 | 83.04 / 61.21 | 同上 |
| gold-NLU 上界（全量微调）(t) | 同上 | IC avg | 86.73 | 同上 |
| E2E Whisper FR (t) | 同上 | IC (FR) | 85.87 | 同上 |
| SFT Qwen2-Audio FR (t) | ICASSP 2026 | IC / SLU-F1 | 87.39 / 74.86（指标定义≠slot-micro-F1）| arXiv:2509.15389 |
| **ours（若立探测）** | — | — | —（prompt-only 多语 SLU 文献空白）| — |

## minds14（Family B — 诊断载体）

| system / condition | protocol | metric | value | source |
|---|---|---|---|---|
| LaBSE translate-to-EN + MLP (t) | Gerz 2021，3-fold 随机 60/40（**无规范 split**）| acc avg | 95.9 | arXiv:2104.08524 |
| MAEB embedding probe | MAEB 2026 | probe score | Qwen2-Audio 25.51 / Whisper-medium 48.30 | arXiv:2602.16008 |

## slue-sqa-5 / spoken-squad / heysquad（Family C）

| system / condition | protocol | metric | value | source |
|---|---|---|---|---|
| SLUE-SQA-5 pipeline-oracle：gold 转写+DeBERTa (t) | SLUE Phase-2 ACL 2023 | frame-F1 (test/verified) | 62.3 / 70.3 | arXiv:2212.10525 |
| SLUE-SQA-5 最佳真实 pipeline（NeMo ASR+DeBERTa）(t) | 同上 | frame-F1 (test/verified) | 43.3 / 45.9（w2v2 39.6/40.1；whisper 32.7/35.7）| 同上 |
| SpeechDPR (t) | ICASSP 2024 | Top-20 retr. / OpenSQA frame-F1 | 19.73 / 0.558（级联师生 19.94-19.90 / 0.561-0.565；WER>40% 时 SpeechDPR 显著占优 `[abl]`）| arXiv:2401.13463 |
| Spoken-SQuAD 2018 floor：最佳 FusionNet (t) | Interspeech 2018，ASR WER 22.7 | EM / F1 | 46.51 / 60.06（clean-text 均值上界 64.41/74.54）| arXiv:1804.00320 |
| Su & Fung 2020 文献天花板 (t) | ICASSP 2020 | F1 | 77.67 | IEEE 9053979 |
| HeySQuAD 微调 (t) | arXiv:2304.13689 | 相对增益 | +12.51%（人声转写参与训练）/ +2.03%（更高质量转写评测）`[abl]`；绝对 EM/F1 原文表待录（可选）| 同左 |
| AudioBench 直答行（slue_p2_sqa5）| AudioBench，LLM-judge 0-100 | judge score | SALMONN 83.92；Qwen2-Audio-Inst 82.99；Qwen-Audio-Chat 80.05；WavLLM 76.12；**级联 Whisper+Llama3 76.12 —— 此处直答＞级联（闭卷文档 QA 反向数据点）**；spoken_squad 行不在论文 v4 表内（leaderboard 侧，冻结时再核）| arXiv:2406.16020 |
| **ours: AudioBench 协议重跑（A1，判分替换）** | 采样 + pinned 开源 judge | judge/EM-F1 | — | 待回填 |
| **ours: T1 SpeechDPR 类比（training-free 检索）** | 核转写 + pinned BM25，有界池（与原文全库不可等比） | Top-N / frame-F1 | —（方向对照 19.73 / 0.558）| 待回填 |
| **ours: T2 SpeechRAG 类比（检索阶梯 closed-book/retrieved/oracle）** | 核转写段落 + pinned 检索器（spoken-squad）| EM/F1 | —（对照 "不劣化" 声明；兼作 C 族 SUPPLY 灵敏度阶梯）| 待回填 |

## ami-meeting-corpus（Family E）

| system / condition | protocol | metric | value | source |
|---|---|---|---|---|
| QMSum 训练基线 (t) | NAACL 2021 | ROUGE | 数值待提取（仅存档用；指标对证据不敏感 `[abl]` MS-AMI）| Yale-LILY/QMSum |
| MeetingQA 微调抽取器 (t) | ACL 2023 | span-F1 | 57.3（human 84.6）| adobe/meetingqa |
| CMT-LLM (t) | Interspeech 2025 | WER (AMI SDM, 1k distractors) | 32.9 | arXiv:2506.12059 |
| PlanRAG-Audio | ACL-F 2026，未放码 | ROUGE-L / DER（自建任务）| 不可独立评分 | arXiv:2605.20414 |

## audio2tool（Family D）

| system | protocol | Tier1 | Tier3 multi-intent | Tier8 blending | source |
|---|---|---|---|---|---|
| **Qwen-3-Omni-30B（同款核）直答** | 论文协议，确定性指标 | 92.4 | 74.7 | 41.7 | arXiv:2604.22821 |
| Whisper-v3 + Gemma-27B 级联 | 同上 | 87.9 | — | 50.5 | 同上 |
| **ours: GGUF 运行时重跑（R1=P1）** | 50×8 tier 采样，重实现 scorer | — | — | — | 待回填（tier 全列）|

## voiceagentbench（Family D）

| system | protocol | EN PF avg | Indic PF avg | source |
|---|---|---|---|---|
| Whisper + Llama3-70B (t backend) | VAB 官方 | 60.64 | 39.21 | arXiv:2510.07978 |
| Whisper + Gemma3-27B | 同上 | 59.28 | 35.28 | 同上 |
| KimiAudio-7B 直答 | 同上 | 57.57 | 28.21 | 同上 |
| Qwen2.5-Omni-7B 直答 | 同上 | 1.70（格式崩溃）| 0.29 | 同上 |
| one-shot 增益 `[abl]` | 同上消融 | +10–17pp（复杂任务）| — | 同上 |
| **ours: zero-shot vs one-shot（R5=P2c）** | 150 EN 复杂题配对 | — | — | 待回填 |

## full-duplex-bench-v3（Family D 邻接）

| system | Pass@1 | self-correction Pass@1 | source |
|---|---|---|---|
| GPT-Realtime | 0.600 | 0.588 | arXiv:2604.04847 |
| 级联 Whisper→GPT-4o→TTS | 0.450 | 0.176（反例 `[abl]`）| 同上 |

## voicebench / voiceassistant-eval / uro-bench / big-bench-audio（Family F）

| system / condition | protocol | metric | value | source |
|---|---|---|---|---|
| VoiceBench #1 Nemotron-3-Nano-Omni (t) | VoiceBench 全套 | overall | 89.39 | 官方 leaderboard |
| VoiceBench 级联 Whisper-v3+GPT-4o | 同上 | overall | 87.80（rank 4）| 同上 |
| GPT-4o-Audio | 同上 | overall | 86.75 | 同上 |
| Qwen2-Audio | 同上 | overall | 55.80 | 同上 |
| URO-Bench EN-basic 级联 Whisper+GPT-4o | URO-Bench | overall | 89.33 | Ruiqi-Yan/URO-Bench |
| URO-Bench EN-basic 最佳开源 E2E GLM-4-Voice (t) | 同上 | overall | 69.09 | 同上 |
| VoiceAssistant-Eval GPT-4o-Audio | VAE，gpt-oss-20b judge | listening / speaking | 39.78 / 51.26 | arXiv:2509.22651 |
| VoiceAssistant-Eval Qwen2.5-Omni-7B | 同上 | listening / speaking / viewing | 33.56 / 41.27 / 34.27 | 同上 |
| BBA GPT-4o 文本上界 | BBA，Claude judge | acc | 92 | HF blog 2024-12 |
| BBA GPT-4o-Realtime 语音直答 `[abl]` | 同上 | acc | 66 | 同上 |
| BBA Whisper→GPT-4o 级联 `[abl]` | 同上 | acc | ≈文本水平 | 同上 |
| BBA Gemini-2.5 Native-Audio-Thinking (t) | 同上 | acc | 92（2025-10）| Artificial Analysis |
| **ours: BBA direct vs self-cascade（R2=P2a）** | 200 题配对，pinned 判分 | acc | — | 待回填 |
| **ours: VoiceBench 确定性子集（A2）** | MCQ/rule 子集采样 | per-subset | — | 待回填 |

## P0 数字补录清单（2026-08-07 已完成主体）

已补：SLUE-SQA-5 frame-F1（含 oracle 上界）；SpeechDPR 两级数值；
Spoken-SQuAD 2018 floor；HeySQuAD 相对增益；AudioBench slue_p2_sqa5 行。
残留（低优先，冻结前处理）：UniverSLU 90.3 原文表复核；AudioBench
spoken_squad leaderboard 行；HeySQuAD 绝对 EM/F1；（可选）QMSum ROUGE
存档值。发现的反向数据点已入表：AudioBench 闭卷文档 QA 场景直答＞级联，
与 FDB-v3 self-correction 反例同属"级联并非处处占优"证据。

## 回填规则

1. 先落 study 仓 exposure-ledger 行与收据，后改本页；
2. "ours" 行必须写明：ledger 行 id、样本量、split role、protocol hash 短
   前缀、判分器（确定性 / pinned judge 及其 hash）；
3. 与发表行不同 protocol 的结果**另起新行**，不得覆盖对照行；
4. 本页按行就地更新，历史经 git 保留。
