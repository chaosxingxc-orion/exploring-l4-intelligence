# 2026-07-09 · 模型覆盖矩阵合集（覆盖阶段材料——只铺全景，不做收敛）

> **性质**：Stage-1 覆盖文档。Owner 2026-07-09 纠正"模型调研未充分覆盖、嵌入器选型未详细覆盖"后
> 的三路 Opus 覆盖产出之综合：①本地 18 模型全角色矩阵（逐目录实核）；②本地外跨模型验证器底座
> （web 核实，每条 GGUF 声称附实开来源）；③嵌入器全候选选型矩阵（调研正文+两附录点名的全部
> 系统，**67 条目全入账：在盘 14 / 可下载 13 / 方法型 15 / 未确认 11 / 已否决 8 / 空白类 6**；
> Kiwano 为工具类）。**收敛留待 owner 收敛门**——本文一切"候选/推荐"仅为选型材料。
> 原始产出存档（已入库）：`survey/2026-07-09-model-role-matrix-local18.json`、
> `survey/2026-07-09-verifier-backbones-beyond-local.md`、
> `survey/2026-07-09-embedder-selection-matrix-full.md`。

## 0. 运营级发现（需先修）

1. **emotion2vec-s 在盘 checkpoint 是 PARTIAL**：仅 ~1MB / 应 1.13GB，遗留 `checkpoint.pt.aria2`
   断点文件——"候选模型 12/12 全齐"的底数声明被戳破一角（false-COMPLETE 陷阱在模型侧重演，
   数据集侧的 `hf_complete.py` 字节校验没有覆盖模型目录）。→ **P3：重取 + 给模型目录补字节校验**。
2. **LCO-3B "可与 30B llama-server 共驻"是 manifest 声称**，30B `-ngl 28` 已近占满 24GB → 共驻
   VRAM 预算必须实测（P3 核查项）。
3. emotion2vec-plus-large license 为非 SPDX 自定义条款，发表前须核 NC 与否（manifest 已挂旗）。

## 1. 本地 18 模型全角色矩阵

### 1.1 生成/验证底座（lock 6）

| 模型 | 角色 | 24GB 可跑性 | license | δ_corr 谱系评估 |
|---|---|---|---|---|
| qwen3-omni-30b GGUF | **主生成器**（在跑，W1 best-of-N 出处）；H-b 自身隐态键候选 | ✅ 已证路径（Q8_0+mmproj，-ngl 28，常驻 ~2.8s/gen）；**占满卡** → 其余全部 CPU 或分时 | Apache-2.0 | —（主体） |
| qwen3-omni-30b HF | H-b 隐态导出备选源 | ⚠ int4 AutoRound 目录；裸 transformers 加载 OOM（MoE 专家重初始化 fp32 ~58GB 实测）→ 需 AutoRound-aware 加载或改走 GGUF embedding 路线（P3 未验证） | Apache-2.0 | — |
| moss-audio-8b | 跨模型验证器 / 第二生成器 | HF bf16 ~17GB 单驻可跑（分时）；custom arch 加载未实测；无 GGUF | Apache-2.0 | ⚠ **Qwen3 文本基座** → 谱系部分重叠，去相关弱于预想（音频编码器自有） |
| nemotron3-nano-omni | 跨模型验证器——**架构分歧最大候选**（Mamba2 混合 + parakeet 编码器 + radio 视觉） | ❓ **P3 头号障碍**：NVFP4 需 TRT-LLM 或 vLLM+modelopt，本机均未验证（vLLM 0.14 对 omni 处理器已知崩）；无 GGUF；21GB 分时 | **NVIDIA Open Model Agreement（可商用！与 omni-embed 的 NC 不同）** | ✅ 若跑通 = 最佳 δ_corr 验证器 |
| minicpm-o-4.5 | 跨模型验证器 / 第二生成器 | HF bf16 ~19GB 单驻（紧）；custom arch 未实测；4.5 无 GGUF（2.6 代曾有上游支持） | Apache-2.0 | ✅ 独立谱系（MiniCPM 文本 + whisper-medium 音频）→ 强于 moss、架构分歧弱于 nemotron |
| omni-embed-nemotron-3b | H-b 对照键（仅对照） | CPU 可跑（8.8GB bf16）；loader 待按官方非对称 API 修 | **NVIDIA OneWay NC** | 音频零样本弱（AudioCaps R@1 20.5） |

### 1.2 嵌入器/特化键（候选 12）

| 模型 | 角色 | 运行 | license 注 |
|---|---|---|---|
| glap（3.2GB） | **H-a 内容主键候选**（zh+en 双确证） | trust_remote_code + encode_audio()；CPU 共驻 | Apache |
| lco-embedding-omni-7b GGUF | H-b 单空间键（F2 最强证据 MAEB #1） | llama.cpp --embedding --pooling last，dim 3584，mmproj 必需；**不可与 30B 共驻**（分时） | Apache |
| lco-embedding-omni-3b GGUF | 同上（共驻候选） | 共驻声称待实测（§0.2） | Apache |
| meralion-speech-encoder-2 | H-a 内容/意图候选（zh+en）；SSL 基线 | trust_remote_code（best-rq conformer），2.4GB CPU 共驻 | **MERaLiON PL = MIT+署名，商研皆可**（此前"候补"顾虑解除） |
| eres2netv2-zh（69MB） | H-a speaker 主键候选（zh） | ModelScope/3D-Speaker loader（非 transformers），CPU 自由共驻 | Apache |
| campplus-zh（27MB） | H-a speaker 键（zh） | 同上 FunASR 系 loader | Apache |
| redimnet-b6（58MB） | H-a speaker 键（en） | 裸 .pt——须 clone IDRnD/ReDimNet 钉 commit 9438b1e 实例化 | MIT |
| emotion2vec-s | H-a emotion 主键候选 | FunASR loader；**在盘 PARTIAL 须重取（§0.1）** | Apache |
| emotion2vec-plus-large（1.9GB） | H-a emotion 备选 + 9 类自动 value 生成器 | FunASR loader，完整在盘 | ⚠ 非 SPDX，发表前核 |
| wavlm-large / base+ | SSL 基线（speaker 稳健） | WavLMModel 平凡 loader，CPU 共驻 | MIT（上游；HF 卡未声明） |
| clap-htsat-unfused | **负对照**（协议有效性：好协议必须杀死它）+ 声音事件域键 | 已接通（现 KB 唯一真键） | Apache |

## 2. 本地外跨模型验证器底座（web 核实，摘录；全文见存档）

**llama.cpp 音频输入现状**（2026-04）：Voxtral、Ultravox、Qwen2.5-Omni、**MERaLiON-2**（PR
#21756，一方 GGUF）、Gemma-4 audio E2B/E4B、Qwen3-ASR；Qwen2-Audio 被官方标 unusable。

- **空缺 cell**："zh-first × 非 Qwen 文本谱系 × GGUF 即插"无单模型满足。最接近 = **MERaLiON-2
  3B/10B**（Gemma-2 解码器 + 一方 GGUF + zh 可用；编码器仍 Whisper 谱系；license 需核）。
- zh 强者（Kimi-Audio / GLM-4-Voice / Step-Audio-2 / Baichuan / Ming-Lite）各缺一轴：
  或 Qwen 谱系（去相关弱）、或无 GGUF（破 resident-server 模式、与 llama-server 抢卡）。
- **编码器去相关的更优解 = 非 Whisper ASR ensemble 作独立二意见**（zh：SenseVoice/FireRedASR/
  Paraformer；en：Parakeet/Canary；**CrispASR** = 36 后端 C++ ggml hub 含 CTC 强制对齐，与主底座
  同 ggml 模式）——比再找一个 omni 更强的 δ_corr 素材，且是可部署奖励信号（ASR 一致性）。
- whisper.cpp（large-v3 / turbo / Belle-zh 微调版）= 中等去相关的廉价二意见（Whisper 谱系与主
  底座编码器部分共享）。
- **信息边界旗标**：任何验证器只准喂部署可得音频，绝不喂 golden 转写。

## 3. 嵌入器全候选选型矩阵（67 条目，摘要；全文见 `survey/2026-07-09-embedder-selection-matrix-full.md`）

**计数**：ON-DISK 14 · 可下载 13 · 方法型 15 · 未确认 11 · 已否决 8 · 调研空白类 6 = 67。

**任务族 × 空格 → 最廉价填法**：

| 空格 cell | 填法 |
|---|---|
| ASR × 词级键 | **复现 M2R-Whisper**（唯一 training-free 词+句双尺度先例，effort M）→ CLAR-CIF 第二波；无下载可填 |
| zh ASR × 声学键 | 调研空白：mini-survey + SenseVoice-S（~1GB，兼 LID/value 生成）小探针 |
| slot × 段级模型 | 协议填法 = 两级检索（免费）；模型填法 = **CLSP**（~1.5GB，唯一可下载多粒度 frozen 嵌入器） |
| SER × zh | 无需下载：在盘 E2V-S（重取后）/e2v+ 跑 esd/csemotions（⚠#26 空缺必测） |
| ST × 多语 | **SENSE**（cc0，~1.2GB，VoxPopuli R@1 96.55 > SONAR）；zh-ST 仍空白 |
| LID | **Dasheng**（~2.4GB，HEAR 赢 VoxLingua+CREMA-D，兼 SER-en 通才挑战者）或零成本 readout |
| SID × omni 原生 | 调研确认**不存在** → 不可下载填补 = W4 目标 cell |
| 解码器/LLM 状态键 | P3 工程核查（L）：llama.cpp embedding 导出；MOSS/MiniCPM 备选宿主（调研沉默=空白非证据） |

**高杠杆方法复现**（无需下载）：M2R-Whisper（词+句双尺度）、**Multi-Axis Factor-Partitioned**
（frozen WavLM 子空间分解 + 带符号 kNN，P@1 65.5% vs 0.3%——H-b 直接小规模先例，WavLM 在盘，
effort L）、WavRAG 模式（frozen 音频 LLM last-token 键）、Beyond-Generative-Decoding（frozen
omni 状态判别读出）。

**若批准的净新增下载**：SENSE + Dasheng + CLSP（+SenseVoice-S 可选）≈ **5–6GB**。

**已否决重申**（带理由，不再提案）：e5-omni（owner 裁定）、CLAP-as-content-key（F1，留负对照）、
VoxRAG-as-key（nDCG .03）、Hotword+GRPO / Dynamic-Model-bank-TTA（非 training-free）、
文本转写空间键（丢韵律，困难样本恰恰失效——反例支持音频键论题）。

## 4. 与其余覆盖线的接口

数据集类型学统一表：`2026-07-09-coverage-dataset-taxonomy.md`（成文中）；理论方案台账：
`2026-07-09-theory-scheme-coverage.md`（成文中）；战役设计书（约束项台账/loop 协议）：
`2026-07-09-stage1-dual-track-campaign.md`。收敛门材料 = 本文 + 上述三份。
