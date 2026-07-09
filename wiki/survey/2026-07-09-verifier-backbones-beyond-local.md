# 本地外跨模型验证器/第二底座覆盖（Opus agent 终报存档，2026-07-09）

双去相关轴：text-backbone lineage × audio-encoder lineage（共享 Qwen 文本权重或 Whisper 编码器 = 弱 δ_corr）。

## llama.cpp 音频输入支持现状（承重事实，全部附实开来源）
- Ultravox v0.5（PR #13623；ggml-org 1B/8B GGUF）
- Voxtral Mini 3B / Small 24B（ggml-org / bartowski GGUF）
- Qwen2.5-Omni 3B/7B（PR #13784）
- Qwen2-Audio/SeaLLM-Audio（PR #13760，官方标 problematic/unusable）
- MERaLiON-2 3B/10B（PR #21756，b8762，2026-04-11，一方 GGUF，WER 距 BF16 0.002）
- Gemma-4 audio E2B/E4B（PR #21421，b8766；mmproj 只能 BF16；26B/31B 无音频）
- Qwen3-Omni + Qwen3-ASR 0.6B/1.7B（PR #19441，b8769；仅理解侧，Talker 未实现）
来源：llama.cpp docs/multimodal.md、discussion #13759、HF ggml-org 卡片。

## Table A — GGUF 即插即用层（与主底座同 resident-server 模式）
| 模型 | 规模/量化 | zh | lineage→δ_corr |
|---|---|---|---|
| Voxtral Mini 3B | Q8≈4GB | ✗（无官方 zh） | 强（Mistral 文本） |
| Voxtral Small 24B | Q4≈15GB | ✗ | 强；24GB 可装 |
| Ultravox v0.5 8B/1B | 6-9GB/2GB | 弱 | 中强（Llama 文本+Whisper 编码器） |
| Ultravox v0.6 Gemma-3-27B | Q4≈17GB | 弱 | 中强（社区 GGUF） |
| **MERaLiON-2 10B/3B** | 7-11GB/3GB | **✓ Mandarin** | **最强 zh 可用即插层**（Gemma-2 解码器非 Qwen；Whisper-v3 编码器共享编码谱系）；MERaLiON PL license 需核条款 |
| Gemma-4 audio E4B/E2B | 4-8GB | 音频 zh 覆盖不确定 | **双轴最强**（Gemma 文本 + USM/Conformer 非 Whisper 编码器） |
| Qwen3-ASR 0.6/1.7B | 1-2GB | ✓ 强 | 弱（同 Qwen 谱系；廉价 zh ASR 但错误相关） |
| Qwen2.5-Omni 7B/3B | 8GB | ✓ 强 | 弱（主底座直系前代） |
| Qwen2-Audio-7B | — | ✓ | 最弱（同谱系 + GGUF 被官方标坏） |

## Table B — 重栈层（无 llama.cpp 音频，需 transformers/vLLM，破 resident-server 模式，与 llama-server 抢 24GB）
Kimi-Audio-7B（zh 强，Qwen2.5 基座→弱去相关）· GLM-4-Voice-9B（zh 强，GLM 非 Qwen→文本强去相关，无 GGUF）· Step-Audio-2 mini 8B（zh/en SOTA：CER 3.08/WER 3.14，Apache，自有架构→强，无 GGUF）· Baichuan-Audio（Qwen+Whisper→弱）· Ming-Lite-Omni 16B-A3B（MIT，Ling MoE 非 Qwen→强，无 GGUF）· VITA-1.5（Mixtral，24GB 勉强）· Ola-7B（Qwen+Whisper→弱）· Audio-Flamingo 3（NVIDIA 疑 NC，en 为主）· Phi-4-multimodal 5.6B（MIT，zh ✓，Phi 文本强，无 llama.cpp 音频，可 ONNX/mistral.rs）· Granite-Speech-3.3-8B（Granite+Conformer 双轴强，zh 仅翻译目标；CrispASR 可 ggml 跑）· LFM2-Audio-1.5B（非 transformer LFM2+FastConformer→谱系新颖度最强，en 为主）· DeSTA2.5（Llama，en）· SALMONN 7/13B（Vicuna+Whisper+BEATs，2023 旧）· SeaLLMs-Audio（Qwen2-Audio 系）· Typhoon2-Audio（Llama，泰语）· Aero-1-Audio 1.5B（Qwen2.5 小）

## Table C — verifier-as-tool 轴（非 LLM 二意见，最大去相关，全本地）
- whisper.cpp large-v3 3.1G / turbo 1.62G（zh 多语；Whisper 谱系与主底座编码器部分共享→中等去相关）
- Belle-whisper-large-v3-zh（zh 相对 CER 降 24-65%；需 GGML 转换）
- **SenseVoice-Small**（sherpa-onnx int8，CPU 可跑；SAN-M 非 Whisper 非自回归→**高去相关**，zh 优秀）
- **Paraformer / FireRedASR**（zh SOTA，CER 3.05 / AISHELL-1 0.76；Conformer 非 Whisper→高）
- Parakeet TDT/CTC、Canary、Canary-Qwen-2.5B（FastConformer；NeMo 或 CrispASR ggml）
- **CrispASR**（C++ ggml hub：36 个 ASR 后端 incl Parakeet/Canary/Voxtral/Qwen3-ASR/Granite/Wav2Vec2/Moonshine/Gemma-4-E2B + CTC 强制对齐 `--align-only`——同 ggml 模式跑非 Whisper 去相关 ensemble 的基础设施）
- MFA 3.x 强制对齐（<15ms 边界误差，Kaldi，phonetic 合理性检查，与任何 LLM 正交）
- WhisperX / ctc-forced-aligner（wav2vec2 音素对齐，廉价时间戳/一致性 oracle）

## 空格结论
**空缺 cell = "zh-first × 非 Qwen 文本谱系 × llama.cpp GGUF 即插"——无单模型全满足。**
最近者 = **MERaLiON-2**（唯一 GGUF 一方支持 + 非 Qwen 解码器 + zh 可用；编码器仍 Whisper 谱系；license 需核）。
编码器去相关 gap 更优解 = Table C 非 Whisper ASR ensemble（zh: SenseVoice/FireRedASR/Paraformer；en: Parakeet/Canary via CrispASR）作独立 oracle——与 Whisper 编码器 omni 最大错误去相关、同 ggml 运行模式。
第二 omni 底座槽位今日唯一强 GGUF 候选 = MERaLiON-2。

## 信息边界旗标（agent 自带）
任何验证器只准喂部署可得的音频，绝不喂 golden 转写——"看过参考答案的 ASR 二意见"是经典假增益陷阱。
