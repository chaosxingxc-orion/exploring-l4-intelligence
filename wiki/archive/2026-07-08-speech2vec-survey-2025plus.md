# 2026-07-08 · 2025-01 之后语音向量化（speech2vec 类）方案调研 — 主文档

> **性质**：Stage-1 调研 / **讨论材料**。按 owner 2026-07-08 指示"充分调研先行、规划后置"产出：
> **本文档给出候选矩阵，不做选型**——嵌入器选型、T11 实验设计、lock 增补均留待 owner 讨论。
> **方法**：多代理 workflow（run `wf_1d75e256-bf9`）：8 个 Opus finder 分维度 web 检索
> （窗口 2025-01→2026-07；arXiv/ICASSP/Interspeech/ACL/EMNLP/NeurIPS/ICLR 25-26/HF 模型卡），
> 40 条 load-bearing 声称逐条 Opus 对抗验证：**34 CONFIRMED / 6 PARTIAL / 0 REFUTED**，
> PARTIAL 修正已内联（§6）。Fable 终审综合。明细：`survey/2026-07-08-speech2vec-dims-1-4.md`
> 与 `survey/2026-07-08-speech2vec-dims-5-8.md`。
> **配套**：三锚点审计 `2026-07-08-three-anchors-critical-audit.md`；
> 数据集覆盖盘点 `2026-07-08-dataset-coverage-inventory.md`。

## 1. 七条主发现（全部经对抗验证 gate）

**F1 — CLAP 作词汇内容键正式失效（硬数字确证审计"洞3"）。**
LibriSpeech test-other 语音内容检索 R@1：MS-CLAP/LAION-CLAP ≈ **0.1%**，GLAP **93.8%**、
中文 AISHELL-2 **98.5%**（✅#9/#10）；MAEB/MSEB 独立佐证（CLAP 在 MInDS-14 意图近随机、多语跨
模态 <3%）；VoxRAG 用 CLAP 段键 strict nDCG@10 仅 0.03。**我们现有 KB 唯一接通的真嵌入器
（laion/clap-htsat-unfused）对主任务族（spoken-QA/SLU/ASR 内容型）不可用**，仅在声音事件域有效。

**F2 — "frozen omni 隐态可直接作检索键"获得 2025-26 独立外部支持（利好 W4 论题）。**
LCO-Embedding-Omni-7B **未做音频对比训练**即登 MAEB 53 模型总分第一（52.2%，✅#35）——frozen
thinker 本身编码了可检索的语音内容；WavRAG 用 frozen Qwen2-Audio last-token 作键（R@10
Spoken-SQuAD 0.9023）；Beyond-Generative-Decoding 证明 frozen omni last-token 是强 affect
嵌入（判别读出胜同模型生成解码）。**但注意**：纯零样本的 Nemotron 音频检索弱（AudioCaps R@1
20.5，✅#17——主训练是 text-image），起效的 e5-omni/WAVE/SEAL 都加了 LoRA/轻适配——
"零训练 frozen 键够不够好"仍是待实验的开放问题。

**F3 — 无任何单一模型全任务族最优 → "统一主键 + 特化例外"的结构获文献支持，但主键人选换了。**
MAEB 明示"无模型七类别全胜"；TS-SUPERB 无模型全胜；WavLM-large 在 SUPERB 五项反超 MERaLiON-SE2
（⚠#11）；speaker 键上特化小模型（ERes2NetV2 zh、ReDimNet）以 ~25× 更少参数打平/胜过通用编码器；
curated SER 上 emotion 特化占优、自然场景副语言反而通用编码器占优（Vox-Profile）。
**结构性结论：内容键、speaker 键、emotion 键大概率是不同的空间；关键的选型问题是"内容主键用谁"
+"哪几个任务族值得特化键"。**

**F4 — codec/离散 token 作检索键 = 文献空白 + 系统性劣势 → 低优先。**
DASB：连续表征全面胜过所有离散 tokenizer（WER 差 ~2pt、EER 差 ~8pt，✅#27/#40）；2025-06 综述
确认无文献把 token 当检索键（✅#39）。度量训练后的 token 键（wav2tok 2.0/PairAlign）只是存在性
证明。⚠注意 DASB 本身无检索任务类别（#24）——"检索无用"是外推而非实测，但方向一致。

**F5 — 语音域不存在成熟 late-interaction/多向量检索器 → slot 任务"两级检索"是合理默认。**
子句检索现存方案用 Smith-Waterman/DTW 而非 ColBERT-MaxSim（H-QuEST MAP 0.648/0.747 ✅#8、
MARS 层级键 MER 9.60→8.35 ✅#25）；frame 级 CLAP 家族（FLAM/FineLAP）只在声音事件上验证过。
utterance 主键 + 检回带标注整句作 few-shot、span 定位交给 frozen 模型 ICL，是当前证据下最稳的
slot 方案；frame/多向量键列为后备实验。

**F6 — ASR 困难样本记忆有强 2025-26 先例，且我们瞄准的空白真实存在。**
BR-ASR：200k 偏置词只降 0.3/2.9% abs、99.99% 剪枝、~20ms/查询（✅#2）——**规模化可行性已被
证明**；CLAR 的 CIF 词定位声学键（B-WER 12.9→2.78 ✅#32/#33）；RECAST 用 frozen 解码器自身
状态空间作键。警示：kNN-Whisper 证明 kNN 检索 OOD 会伤害、对超参敏感 → **注入必须门控**（与
我们 δ_corr/τ 理论直接呼应，且"门控阈值"无人量化——理论-实验缺口就是我们的空间）。
**2025-26 无任何工作用 frozen omni-LLM 自身音频嵌入作检索键**——与 38-work 综述 EMPTY-niche
结论一致。⚠#20：BR-ASR 检索器本身是对比训练的——"完全 training-free 的检索键"在文献里同样缺位。

**F7 — omni-embed-nemotron-3b 官方 API 澄清，loader 错因确诊，但其主键候选地位动摇。**
正确用法 = `SentenceTransformer(..., trust_remote_code=True)` + `encode_document([{'audio':
path}])` / `encode_query`（非对称，2048d，✅#1/#13）——现有 loader 把裸 wav 路径喂 `encode()`
双重错误。但：音频近零样本（R@1 20.5 同类最弱）+ **NVIDIA OneWay Noncommercial license**
（✅#19，与 effect-over-novelty 的开源立场冲突）→ 它更适合作对照候选而非默认主键。

## 2. 任务族 × 候选表征矩阵（候选 ≠ 选型；本地 24GB 可跑性已核）

| 任务族 | 粒度 | 第一梯队候选（license） | 对照/后备 | 证据状态 |
|---|---|---|---|---|
| spoken-QA / 内容检索 (zh+en) | utt | **GLAP 0.9B**（Apache）；**LCO-Omni**（Apache，3B GGUF） | SENSE（cc0，en 系）、e5-omni 7B（CC-BY）、Qwen3-Omni 自身隐态（Apache，需自测） | GLAP zh+en 双确证✅；LCO 榜一✅但 clustering 弱；omni 自身隐态零训练效果未知 |
| ASR 困难样本记忆 | utt+词级 | 内容键同上 + **CLAR 式词定位键**（复现） | BR-ASR 双编码器模式；kNN-CTC/M2R-Whisper（pre-2025 底座） | 规模化✅（BR-ASR 200k）；frozen-omni 自键 = 文献空白 = 我们的空间 |
| SER (zh+en) | utt | **Emotion2Vec-S**（Apache）；emotion2vec+ | Dasheng（Apache，HEAR 赢 CREMA-D）；CLSP（风格键） | ⚠#26：**zh(M3ED) 增益仅 +1.8**——zh SER 键实证空缺大，T11 必测 |
| Speaker-ID | utt | **ERes2NetV2/CAM++ 3D-Speaker**（Apache，zh 200k 说话人） | ReDimNet v1（MIT）；ECAPA2（NC，仅对照） | 特化以 ~25× 少参胜通用✅；无 omni 原生 speaker 嵌入器（空白确认） |
| SLU intent | utt | 内容键（GLAP/LCO）+ 意图 few-shot value | MERaLiON-SE2（IC 98.95，zh+en）；minds14 实测定 | MAEB 显示 CLAP 意图近随机；omni 隐态 intent 检索未测 |
| SLU slot | segment | **两级检索**（utt 键检整句带槽标注 → ICL 定位） | H-QuEST 式 token 子句重排；CLSP 层级嵌入；frame 键（后备） | F5：无成熟 late-interaction 语音检索器——两级方案证据最稳 |
| ST/多语 | utt | SENSE / OmniSONAR（发布待确认） | fleurs-r 切片实测 | OmniSONAR −43% 误差✅但可得性未确认 |

**结构含义（供讨论）**：矩阵指向「内容主键（1 个）+ speaker 特化键 + emotion 特化键」的
**2–3 键空间架构**，而非"每任务一键"（7 键）或"单键打天下"（1 键）。这与 W4 的
"一个 frozen 空间多读出"论题的关系是竞争假设 H-a（多外部特化键）vs H-b（omni 单空间+
任务条件化读出，Multi-Axis Factor-Partitioned 的 P@1 65.5% vs 0.3% 是其小规模先例）——
**T11 的头号实验问题**。

## 3. 本地可跑性与 lock 增补需求（讨论后定，不预执行）

| 候选 | HF/来源 | 体量 | license | lock 状态 |
|---|---|---|---|---|
| GLAP | `mispeech/GLAP` | 0.9B/<2GB | Apache-2.0 | **需增补**（小） |
| Emotion2Vec-S | `ASLP-lab/Emotion2Vec-S` | ~1.13GB | Apache-2.0 | **需增补**（小） |
| ERes2NetV2 zh | ModelScope `iic/speech_eres2netv2_sv_zh-cn` | ~百 MB | Apache-2.0 | **需增补**（小） |
| WavLM Base+/Large | `microsoft/wavlm-*` | 95M/316M | MIT | **需增补**（小；TS-SUPERB 佐证的 speaker 稳健基线） |
| MERaLiON-SE2 | `MERaLiON/MERaLiON-SpeechEncoder-2` | 630M | MERaLiON PL（核条款） | 候补 |
| e5-omni-7B | `Haon-Chen/e5-omni-7B` | ~14GB fp16 | CC-BY-4.0 | 候补（与 llama-server 共驻预算紧张） |
| LCO-Embedding-Omni | `LCO-Embedding/…-7B`（有 3B GGUF） | 7B/3B | Apache-2.0 | 候补 |
| omni-embed-nemotron-3b | 已在 lock | 4.7B bf16 ~10GB | **NC** | 已有；修 loader 后作对照 |
| CLAP | 已用 | ~150M | Apache | 保留为声音事件域 + 反面对照 |
| Qwen3-Omni 自身隐态 | 已在 lock（GGUF） | 宿主 30B | Apache-2.0 | 需探明 llama.cpp 能否导出 embedding（未验证） |

## 4. T11 的现成测评工具（设计时直接复用，避免自造协议）

- **X-ARES**（github jimbozhang/xares）：22 任务含 VoxCeleb1 SID、CREMA-D/RAVDESS SER、ASR、
  intent，统一 linear-probe+kNN 协议——**最贴合 T11 的骨架**。
- **VocSim**（2512.10120）：training-free 内容同一性 cosine 检索协议——键选型专用。
- **MAEB/MSEB**（2602.16008/2602.07143）：跨模态检索/聚类/分类大盘对照。
- **DASB**：若讨论决定纳入离散 token 对照。
- kb 侧：我们自己的 `kb_snapshot` item-id 冻结 + `kb_audit` 泄露审计（T11 从第一天接入）。

## 5. 与理论/审计线的接口

- kNN 检索会伤害（kNN-Whisper）+ 无人量化门控阈值 → **δ_corr/τ 邻域收敛理论（Stage-2 定理
  目标）恰好有实验落点**：T11 可顺带产出"检索质量 vs 注入收益"的经验曲线。
- MARS 的 retrieve-AND-select 两级模式 = 我们 training-free RL 选择器的天然挂点（reward-guided
  selection over retrieved candidates）——与 t10"交付形式是杠杆"发现同向。
- F2 的 frozen-omni-隐态证据链直接支持 W4；Multi-Axis Factor-Partitioned（frozen WavLM 分解
  子空间带符号 k-NN）是 W4 解缠读出的 2026 小规模同行先例。

## 6. 对抗验证 PARTIAL 修正清单（6/40，其余 34 条 CONFIRMED，0 REFUTED）

1. **#11 MERaLiON-SE2**：数字准确但"全任务族 competitive-to-SOTA"过强——WavLM-large 五项全胜；
   SID 88.96 为四模型最低（低于自家 v1 91.09）。真实卖点 = zh+en 覆盖。
2. **#20 BR-ASR**："免调优"仅指 ASR 后端，检索器本身是对比训练的；FAISS 具体索引型号系外推。
3. **#21 SENSE**：cc0 权重确认，但"ships a speech2vec pipeline"不实（与 Speech2Vec 2018 无关）。
4. **#23 XEUS**：赢的是 ML-SUPERB 综合分；ASR-CER 子项 MMS-1B(30.8) 反超 XEUS(34.1)。
5. **#24 DASB**：生成任务确实用 decoder；且 DASB 无检索任务类别——F4 的"检索无用"是方向性外推。
6. **#26 Emotion2Vec-S**：Emo-Emilia +12.6 确认；**M3ED-zh 增益实为 +1.8**（62.95/47.58 是
   CASIA 错标）——zh SER 键的实证空缺比初稿显示的大。

## 7. 开放问题 → owner 讨论议程

1. **内容主键选型**：GLAP（轻、双语确证、Apache）vs LCO-Omni（榜一、重、聚类几何弱）vs
   Qwen3-Omni 自身隐态（最 on-thesis、零证据）——是否三者同入 T11？
2. **H-a vs H-b**（多特化键 vs omni 单空间多读出）：T11 是否设计成能直接裁决这对竞争假设？
3. **特化键去留**：speaker（ERes2NetV2 zh）与 emotion（Emotion2Vec-S，注意 zh 增益仅 +1.8）
   是否各设一键？SER 的 zh 空缺是否让 crema-d(en)+meld(en) 先行、zh 情感另补数据？
4. **lock 增补清单**（§3 的"需增补"4 项小模型）是否批准走 candidates→lock 修订流程？
5. **Nemotron 的角色**：NC license + 音频零样本弱——降级为对照候选？（loader 仍按官方 API 修）
6. **slot 方案**：接受"两级检索"为默认、frame/多向量键列后备实验？
7. **T11 骨架**：以 X-ARES 协议 + VocSim 内容同一性协议 + 我们 kb_snapshot/kb_audit 为底座，
   覆盖盘点表的 17 个纳入数据集——prereg 判据冻结会（owner+Fable）何时开？
8. **共驻预算**：7B 级嵌入器与 llama-server 无法同卡共驻——T11 阶段嵌入器独占 GPU（llama-server
   停）或嵌入器全走 CPU/分时——工程取舍待定。
