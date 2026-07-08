# 2026-07-08 · speech2vec 调研附录 B：维度 5–8 明细（codec-tokens / omni-mllm-embed / multivector-segment / asr-hard-sample-memory）

> **来源**：8-finder Opus workflow（run wf_1d75e256-bf9），经 40 条对抗验证内联修正（标 ⚠PARTIAL）。
> 主文档：`2026-07-08-speech2vec-survey-2025plus.md`。

## 5. codec-tokens — 语义/声学 codec 与离散 token 2025+

**维度结论**：现成 codec token 为重建优化，作检索键系统性弱于连续表征；token 只有在
显式度量训练目标下才可用作键。**截至 2025-06 无任何文献把离散 token 当检索/相似度键**
（✅#39，领域空白）。

| 条目 | 日期 | 来源 | License | 关键证据 |
|---|---|---|---|---|
| DASB（基准） | 2024-06 | arXiv 2406.14294 | Apache-2.0 | ASR WER：连续 2.26 vs WavLM-disc 4.32 vs SpeechTokenizer 12.69 vs EnCodec/DAC 16.29 vs WavTokenizer 28.69；SV EER：连续 2.10 vs 最好离散 10.45 ✅#27 ✅#40（差 ~2pt WER/~8pt EER）；语义 token >> 声学 codec ✅#15（⚠情感差距仅 ~10pt，"远胜"过强）⚠#24：DASB 生成任务确实用 decoder，且**无检索任务类别**——"检索无用"是外推 |
| Discrete Audio Tokens Survey | 2025-06 | arXiv 2506.10274v3 | — | 领域空白确认 ✅#39；FACodec/TiCodec/LSCodec 已做 content/timbre/prosody 分离 |
| X-Codec-2.0 | 2025-02 | HF `HKUSTAudio/xcodec2` | CC-BY-NC | 单码本 65536 FSQ@50tok/s；无检索/probe 数字；说话人+内容纠缠 |
| WavTokenizer | 2024-08 | HF WavTokenizer-large-v2 | MIT | 重建 UTMOS SOTA 但 DASB 最差内容 token（WER 28.69）——保真 ≠ 键值 |
| Mimi (Kyutai) | 2024-09 | HF `kyutai/mimi` | CC-BY | 12.5Hz，1 semantic+31 acoustic 量化器；WER 13.52/EER 18.68 中游 |
| wav2tok 2.0 | 2026-06 | arXiv 2606.26824（无权重） | — | 度量训练（contrastive+VQ+CTC/DTW）后 token 串可作内容键（编辑距离检索非 cosine k-NN）——存在性证明 |
| PairAlign | 2026-05 | arXiv 2605.06582 | — | 检索导向 tokenizer 存在（2026），自认未全面胜过 SSL tokenizer |
| Kanade | 2026-02 | github frothywater/kanade-tokenizer | CC-BY-SA | content/speaker/prosody 分流量化——与 W4 解缠论题最对齐；质量未验证 |

**开放问题**：wav2tok/PairAlign 的 mAP 对连续 SSL/omni 无对照；无任何来源把 codec token
当 frozen k-NN 键测过；Kanade/FACodec 解缠质量未量化。

## 6. omni-mllm-embed — omni/MLLM 原生嵌入 2025+

| 条目 | 日期 | 来源 | 规模/License | 关键证据 |
|---|---|---|---|---|
| NVIDIA Omni-Embed-Nemotron-3B | 2025-10 | HF `nvidia/omni-embed-nemotron-3b` | 4.7B bf16 ~9-10GB；**NVIDIA OneWay Noncommercial**（非商用）✅#19 | Qwen2.5-Omni-3B **Thinker-only** + 双向注意力 + pooling，输出 2048d ✅#1；audio-only NDCG@10 0.8238(LPM)；但 AudioCaps R@1 仅 20.5（音频近零样本 ✅#17——主训练是 text-image） |
| e5-omni | 2026-01 | HF `Haon-Chen/e5-omni-7B` | 7B ~15GB；**CC-BY-4.0** | AudioCaps R@1 37.7 胜 Nemotron 20.5/Tevatron 34.0（p<0.05）；MMEB-V2 66.4 vs Nemotron 51.5 |
| WAVE | 2025-09 | github TCL606/WAVE | Qwen2.5-Omni-7B+LoRA | AudioCaps R@1 44.2（本维度最高）✅#29；多层 last-token 拼接 + prompt-aware |
| OmniSONAR | 2026-03 | arXiv 2603.16606 | CC-BY-SA（发布未确认） | 1024d 固定、177 语语音+文本同空间；相似搜索误差 −43% ✅#36 |
| WavRAG | 2025-02 | ACL2025 | Qwen2-Audio-7B | **frozen last-token hidden state 直接作键、免 ASR**；R@10 Spoken-SQuAD 0.9023；比 ASR-then-text 快 ~10× |
| SEAL | 2025-02 | arXiv 2502.02603 | 未公开权重 | 冻结 Whisper→zh 文本空间轻适配：KB Top-1 79.45→86.36 |
| Beyond Generative Decoding | 2026-06 | arXiv 2606.05713 | — | frozen Qwen2.5-Omni-7B（4bit NF4）last-token+MLP 判别式读出胜同模型生成式解码（MOSI MAE 0.551 vs 0.667）——**frozen omni 隐态是强 affect 嵌入** |
| Hearing More with Less (MARS) | 2025-08 | arXiv 2508.01166 (AAAI2026) | — | 音频相似检索+**选择**两级：1.5K h 系统胜 179K h SOTA（MLC-SLM）✅#37 |
| X-ARES（基准） | 2025-05 | github jimbozhang/xares | — | 22 任务（VoxCeleb1 SID、CREMA-D/RAVDESS SER、ASR、intent）统一测 13 编码器——**T11 的现成骨架** |

### omni-embed-nemotron-3b 官方用法（修 loader 的依据，✅#13）

```python
model = SentenceTransformer('nvidia/omni-embed-nemotron-3b',
    trust_remote_code=True, model_kwargs={'attn_implementation': 'flash_attention_2'})
model[0].processing_kwargs.update({'audio': {'max_length': 2048000}})  # ~128s @16kHz
docs = [{'text': ..., 'audio': <path_or_url>}]      # dict 而非裸路径；模态可组合
doc_embeddings = model.encode_document(docs)         # -> (N, 2048)
query_embedding = model.encode_query(q)              # 非对称 API，勿混用
```

要点：必须 `trust_remote_code=True` + flash_attention_2 + SentenceTransformer 包装
（不是裸 AutoModel/AutoProcessor）；KB 侧用 `encode_document`、查询侧用 `encode_query`。
**当前 W1 loader 的错法**：把 wav 路径列表直接喂 `encode()`——既错在输入形态（应为
`{'audio': path}` dict），也错在 API 对称性。**未解**：音频路径的 pooling（mean vs
last-token）从已审的 `modeling_nv_omni_embed.py` 片段无法确认。
**关键警示**：主对比训练为 text-image，音频近零样本（R@1 20.5 为同类最弱）+ 非商用
license —— 其"KB 主键"候选地位需在讨论中重估。

**开放问题**：Nemotron 音频 pooling 未确认；nemotron/e5-omni/WAVE 均无 speaker-ID/SER
评测；**无 omni 原生 speaker 嵌入器**（大概率仍需 ECAPA/ERes2Net 专化键）；
纯 frozen（零训练）omni 骨干作键是否够好未解——Nemotron 零样本弱，而 e5-omni/WAVE/SEAL
都靠 LoRA/adapter 才起效。

## 7. multivector-segment — 片段级/多向量/late-interaction 2025+

| 条目 | 日期 | 来源 | 关键证据 |
|---|---|---|---|
| H-QuEST | 2025-06 | Interspeech2025（无代码） | VQ-token+TF-IDF+HNSW：MAP TIMIT 0.648 / LibriSpeech 0.747 ✅#8（⚠系 best-case 单元格非均值）；Smith-Waterman 子句重排 O(KL²) ✅#12；免转写 ✅#18 |
| MARS | 2025-08 | arXiv 2508.01166 | frame-DTW + utterance-cosine 层级键：会话 ASR MER 9.60→8.35 ✅#25；1.5K h 胜 179K h SOTA |
| CLSP | 2026-01 | github yfyeung/CLSP（CC-BY-4.0） | 唯一一次冻结前向同时出 frame/word/utterance 层级嵌入；SER/SV 竞争级 |
| VoxRAG | 2025-05 | arXiv 2505.17326 | diarize+VAD→逐段 CLAP→FAISS 蓝图；**strict nDCG@10 仅 0.03**——单向量 CLAP 段键失败案例 |
| FLAM | 2025-05 | Adobe (arXiv 2505.05335) | frame 级预计算+仅查询侧编码（ColBERT 式非对称成本）；**只在声音事件上验证** |
| FineLAP | 2026-04 | GitHub+HF FineLAP-100k | clip+dense frame 双键 SOTA（AudioCaps R@1 45.7 T→A）；同样只测声音事件 |
| VocSim（基准） | 2025-12 | arXiv 2512.10120 | **training-free** 的内容同一性保持基准（cosine 检索协议）——T11 键选型可直接复用协议 |
| MetaEmbed | 2025-09 | arXiv 2509.18095 | Matryoshka multi-vector + MaxSim（视觉域）——可控长度多向量键的设计模板 |

**pre-2025 背景**：ColBERT/v2（late-interaction 源头，语音无先例）；MGA-CLAP（ACM MM 2024，
frame 级 CLAP 开山）；SSL 声学词嵌入（2022-24，segment 定长键先例）。

**开放问题**：**语音内容域不存在 ColBERT 式 MaxSim 检索器**（现有全用 Smith-Waterman/DTW）；
frame 级 CLAP 家族从未在词汇/说话人/情感判别上验证；VocSim 逐模型排名未提取到；
frozen omni 编码器能否零训练输出可用 per-segment 多向量键未验证。

## 8. asr-hard-sample-memory — ASR/SLU 困难样本记忆与 contextual biasing 2025+

| 条目 | 日期 | 来源 | 关键证据 |
|---|---|---|---|
| BR-ASR | 2025-05 | Interspeech2025 (arXiv 2505.19179) | B-WER 2.8/7.1%@2000 词、45% rel ✅#4；**扩到 200k 偏置词只降 0.3/2.9% abs、99.99% 剪枝、~20ms/查询** ✅#2 ⚠#20：检索器本身是对比**训练**出来的（"免调优"仅指 ASR 后端）；FAISS 具体索引型号系外推 |
| CLAR | 2026-03 | arXiv 2603.25460 | CIF 免时间戳的词级语音↔文本对齐 ✅#32：**词定位声学键**；B-WER 12.9→2.78% ✅#33（Step-Audio2-mini） |
| RECAST | 2025-11 | EMNLP2025 Findings | **frozen 解码器自身状态空间作键**（需训练对比头）：实体 WER −54.3% rel、4000 关键词、跨语言 |
| Hotword+GRPO | 2025-12 | arXiv 2512.21828 | GLCLAP 检索前端可复用；核心增益靠 GRPO 改权重——**与我们 no-weight-change 约束相斥**（对照组价值） |
| WavLink | 2026-01 | arXiv 2601.15118 | 84M 轻量检索导向音频-文本嵌入器；Matryoshka 768→96d；AudioCaps R@1 46.7 |
| kNN-Whisper | 2024-10/rev2025-02 | arXiv 2410.18850 | **警示锚**：kNN 语音检索在 OOD 上会伤害、对 k/τ/λ 高度敏感 → 必须门控（与 δ_corr 理论呼应） |
| ICL Emotion retrieval | 2025-06 | arXiv 2506.20199 | 示例检索提升 LLM 会话情感识别——但键在**文本转写空间**（丢韵律，键型对我们是反例） |
| RAG context discovery | 2025-09 | EMNLP2025 Findings | 键=首轮转写假设——**恰在困难样本上最脆**（支持"键应是音频不是文本"论点） |
| H-PRM | 2025-11 | CIKM'25 | 可插拔热词预检索模块，架构上最像我们 ops 层；数字未提取到（低置信） |
| Dynamic Model-bank TTA | 2025-11 | EMNLP2025 | 存**权重**、测试时梯度更新——定义性对照：非 training-free |

**pre-2025 背景**：kNN-CTC（ICASSP2024，检索式 ASR datastore 源头）；M2R-Whisper（2024-09，
**training-free 双尺度检索**，多粒度语音键直接先例）；phonetic retrieval（2024-09，实体键应
是语音学的而非语义的）。

**开放问题**：**2025-26 无任何工作用 frozen omni-LLM 自身音频嵌入作检索键**（都是外挂编码器
或训练对比头）——与我们 38-work 综述的 EMPTY niche 结论一致，空白即机会；
音频键的 speaker/emotion 困难样本召回是未填补象限；BR-ASR/CLAR/RECAST/H-PRM 权重可得性未确认；
无来源量化"检索质量低于何阈值时注入应被门控"（正是我们 δ_corr/τ 理论的实验缺口）。
