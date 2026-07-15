# 嵌入器全候选选型矩阵（Opus agent 终报存档，2026-07-09，覆盖材料非选型）

范围：调研主文档 + 两附录点名的全部系统，交叉核对 models.candidates.json / lock / E 盘 18 目录。
既有裁定已应用：e5-omni OUT；nemotron NC=仅对照；CLAP=声音事件+负对照。

## 计数总表
- **ON-DISK 14**：GLAP, LCO-3B/7B, WavLM-B+/L, E2V-S, e2v+large, ERes2NetV2, CAM++, ReDimNet-b6, CLAP(控), MERaLiON-SE2, nemotron(对照), Qwen3-Omni-GGUF(宿主)
- **DL 13**：SENSE(cc0,~1.2G), Dasheng(Apache,~2.4G), CLSP(~1.5G), SenseVoice-S(~1G), XEUS(NC), ECAPA2(NC), SONAR(NC), Mimi, WavTokenizer, X-Codec-2.0(NC), Kanade, FineLAP, Kiwano(工具)
- **METHOD 15**：CLAR(CIF 词级键,M-H), BR-ASR(H,参照), RECAST(M-H,最接近"frozen 自身状态键"), **M2R-Whisper(M,唯一 training-free 词+句双尺度先例,高杠杆)**, kNN-CTC, kNN-Whisper(门控负对照协议), phonetic-retrieval(设计注), H-QuEST(M-H,无代码), MARS(M), 两级检索(L,默认), SEAL(适配器=对照类), SpeechRAG(对照类), WavRAG(L-M,frozen-own-states 直接先例), Beyond-Gen-Decoding(L-M,H-b 证据线), **Multi-Axis Factor-Partitioned(L,WavLM 在盘,H-b 直接先例,最高杠杆廉价复现)**
- **UNCONF 11**：OmniSONAR, SLAP, Omni-Embed-Audio, WavLink, ReDimNet2, wav2tok2.0, PairAlign, Codec2Vec, S-JEPA, FLAM, H-PRM
- **REJECTED 8**：e5-omni(owner), CLAP-as-content-key(F1,留控), VoxRAG-as-key(nDCG .03,蓝图可用), Hotword+GRPO(改权重), Dynamic-Model-bank-TTA(非 training-free), ICL-emotion-retrieval / RAG-context-discovery(文本键反例,支持音频键论题), MMS(仅提及无法核)
- **调研空白类 6**：Whisper-encoder-as-key、Paraformer/FunASR-zh 键、LID-as-retrieval、zh-ST 跨语检索、MMS 细节、MOSS/MiniCPM 宿主状态键

## 分任务族要点
1. **内容 zh+en**：GLAP(93.8/98.5 双确证) + LCO-3B/7B(MAEB 榜一,聚类弱) + Qwen3-Omni 自身隐态(空白 niche,压 P3 llama.cpp embedding 导出核查)；SEAL=最接近我们 KB 的公开蓝图(zh Top-1 79.45→86.36,无权重,适配器=训练对照类)；WavRAG(frozen Qwen2-Audio last-token, Spoken-SQuAD R@10 .9023)=direct 先例；SLAP/Omni-Embed-Audio/WavLink 均无词汇内容证据(UNCONF)。
2. **ASR 困难样本**：词级键无在盘模型——最廉价填法=先复现 M2R-Whisper 式 training-free 双尺度，CLAR-CIF 第二波；RECAST 模式套 frozen Qwen3-Omni 状态=空白 niche 的 on-thesis 赌注；kNN-Whisper=强制门控负对照。zh 声学键（Paraformer/SenseVoice 编码器）=调研空白，需 mini-survey+小探针。
3. **SER**：E2V-S(Emo-Emilia+12.6 但 M3ED-zh 仅+1.8=主要空缺) + e2v+large(IEMOCAP 71.79,license 非 SPDX 待核) + Dasheng(DL,HEAR 赢 CREMA-D,Apache 通才挑战者) + WavLM 基线；CLSP=风格轴可选。
4. **SID**：ERes2NetV2(Vox1-O 0.61%) + CAM++ + ReDimNet-b6(MIT,0.58%) + WavLM-L 全在盘=齐；ECAPA2 仅 NC 对照行；**omni 原生 speaker 嵌入器=调研确认不存在**（W4 目标 cell）。
5. **SLU intent**：内容键 + MERaLiON-SE2(IC 98.95)=齐；CLAP 负对照。
6. **SLU slot**：两级检索默认(免费)；CLSP=唯一可下载多粒度 frozen 嵌入器(段级模型填法)；H-QuEST 无代码；MARS 的 retrieve-AND-select=TFRL 选择器挂点；FLAM/FineLAP 仅声音事件。
7. **ST/多语**：SENSE(cc0,VoxPopuli R@1 96.55>SONAR)=最廉价跨语填法；OmniSONAR 发布未确认；XEUS/SONAR=NC 对照行；zh 侧 ST 检索即便下了 SENSE 仍是空白。
8. **LID**：Dasheng(VoxLingua)=唯一直接证据；或零成本=T11 里作既有键的 readout。
9. **声音事件（对照域）**：CLAP 在盘=齐；"好协议必须杀死 CLAP"。
10. **codec/离散 token（F4 低优先）**：Mimi(CC-BY)/WavTokenizer(MIT,内容 WER 28.69 反例)/X-Codec-2.0(NC)/Kanade(CC-BY-SA,内容/说话人/韵律分离量化=W4 关注项)/FACodec 系(仅提及)。
11. **W4 挂钩**：Multi-Axis Factor-Partitioned 复现(L,在盘 WavLM,P@1 65.5% vs 0.3%)、Kanade、omni-native-speaker 缺失 cell。

## 空格清单（cell → 最廉价填法）
- ASR×词级键 → M2R-Whisper 复现(M) → CLAR 第二波；无下载可填
- zh ASR×声学键 → 调研空白：mini-survey + SenseVoice-S(~1G,兼 LID/value 生成)小探针
- slot×段级模型 → 协议填法=两级检索(免费)；模型填法=CLSP(~1.5G)
- SER×zh → 无需下载：在盘 E2V-S/e2v+ 跑 esd/csemotions 评测(⚠#26 空缺必测)
- ST×多语 → SENSE(cc0 ~1.2G)；zh-ST 仍空白
- LID → Dasheng(~2.4G,兼 SER-en) 或零成本 readout
- SID×omni 原生 → 不可下载填补=W4 目标 cell
- 解码器/LLM 状态键 → P3 工程核查(L)：llama.cpp embedding 导出；MOSS/MiniCPM 备选宿主(调研沉默=空白非证据)
- frame/多向量×语音内容 → F5 后备；仅激活时下 FineLAP

## 若批准的净新增下载
SENSE + Dasheng + CLSP (+SenseVoice-S 可选) ≈ **5-6GB**——其余 shortlist 全在盘或为方法复现。

（引用锚：主文档 F1-F7/§2-§4/§6 行号、App-A/App-B 行号、manifests、E 盘 18 目录实核；调研沉默处一律标空白未造证。）
