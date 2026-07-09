# 2026-07-09 · 数据集类型学与评测方案统一表（覆盖阶段材料——只铺全景，不做收敛）

> **性质**：Stage-1 覆盖文档，落实 owner 要求③（数据验证覆盖全部本地数据集）与"评测方案跟着
> survey 和 lock 走、按数据集类型给具体方案"。**底数 = E 盘机器盘存 39 个在盘数据集**（lock 28 +
> gap 候选 7 + WS-D 4）+ 6 个不在盘候选（各有由）。**方法**：三个 Opus agent 实地开盘勘察
> （lock 前/后各 14 + 候选 11），逐集验证 schema、给出切片配方与可验证奖励。勘察存档：
> `survey/2026-07-09-datasets-lock-first14.md`、`survey/2026-07-09-datasets-lock-second14.md`、
> `survey/2026-07-09-datasets-candidates11.json`。
> **Stage-1 统一切片纪律**：每集 dev n≈40（校准）+ test n≈60（方向性评测），kb_snapshot 冻结
> item-id，SLICE_SEED=20260705，revision 钉扎，paired-bootstrap 方向性 CI，全部结果标
> `[directional | small-n | not significance-bearing]`。**不展开大数据方案。**

## 0. 实地勘察推翻先前记录的发现（内容级 false-COMPLETE 普查）

字节级"COMPLETE"≠内容级可用——四例：

1. **covost2 盘上没有音频**（仅 tsv；mp3 属 Common Voice、不在 lock）→ 结构性排除。
2. **mmsu 盘上没有 gold**（仅 wav；全树无 question/choices/answer）→ 排除；HF 补元数据后转
   include（将是最强音频推理集之一）。
3. **fleurs-r 盘上仅 12 个语言、无 en/zh、无翻译目标** → "zh/en ST 切片"不成立；改判
   LID + 多语 ASR + gender。
4. （模型侧）emotion2vec-s checkpoint 仅 ~1MB/1.13GB（见模型矩阵文档 §0）。

**连锁后果：ST 任务族在全部 39 集中没有可跑音频源**——空格 cell（最廉价填法 = 补取 covost2
的 CV mp3 子集，超本轮范围，留收敛门裁决）。
**P3 新增工程项：给全部数据集+模型建内容级完备性校验**（gold 字段存在性 + 音频存在性抽查，
纳入 inventory 工具）。

## 1. 总判定：39 在盘 → **29 纳入（全量或子集）/ 10 结构性排除**

对比 07-08 盘点的"17 纳入/11 排除"：复评把 uro-bench（40 子集逐个开盘分桶）、vocalbench、
voicebench、voiceassistant-eval、air-bench、seed-tts-eval（改判）翻为 include-subset，
audiocaps-qa/audio2tool/squtr（WS-D 实勘）新入，excl 仅留结构性不可能。

### 1.1 纳入 29（按最终类型学分组）

**K1 内容/ASR-en**：librispeech（eval=test.clean 长度分层；pool=train960≠eval）+
seed-tts-eval-en（**改判**：audio↔text 对 = 干净 ASR 对，WER 锚）+ voicebench/sd-qa
（口音方言分层）+ uro/Repeat-en（echo→WER）。

**K2 内容/ASR-zh**：aishell-1（parquet 就绪；train=记忆池/dev+test=评测天然划分）+
thchs-30（朗读多样性池，需解压）+ seed-tts-eval-zh + uro/Repeat-zh。

**K3 多语 LID(+gender)**：fleurs-r（12 语平衡切片；LID 12-way EM + 每语 WER + gender）。

**K4 SER**：crema-d（**标签用文件名码**，train/test.csv 的 classname 有 ~54% 冲突已记 gotcha；
同句异人/同人异情天然对比对=解缠对照）+ meld（mp4→wav，7 类 macro-F1）+ esd/csemotions
（zh，情感×说话人分层）+ **改判再切**：uro/UnderEmotion-en/zh（emotion 列）、
vocalbench/emotion（Question_emo 列）。

**K5 SID/SV**：crema-d（91 人 ID）+ cn-celeb1（官方 trial 对 + genre 标签；cn-celeb2 = 备用池）
+ voxceleb1-test（en 锚，40 人）+ 属性副测：speech-massive speaker_sex/age、
voiceassistant-eval/listening_speech（gender）。

**K6 SLU-intent**：minds14（loader 有，zh 就绪扩 en-US）+ slurp（~60 intent，18 scenario 分层）
+ speech-massive（60 intent，validation 为评测；**CC-BY-NC-SA eval-only**）。

**K7 SLU-slot**：slurp + speech-massive（slot F1，slue-toolkit 在盘）——两级检索方案的验证场。

**K8 口语可验证 QA/MCQ（Stage-1 主力面，zh+en）**：heysquad（**scrub 门承重**，
answer_in_own_KB=1.0 前科）、spoken-squad（WavRAG R@10 .9023 = frozen 隐态键对决先例场）、
big-bench-audio、mmau-mini、mmar（解压+category 分层）、uro-bench **bucket-A ~15 子集**
（SQuAD-zh/OpenbookQA-zh/**Gsm8kEval 582 数值答案最净**/GaokaoEval/HSK5-zh/APE-zh/MuChoEval/
MLC×4/TruthfulEval-弱）、vocalbench{knowledge 2000 事实/reasoning/multi_round}、vocalbench-zh
（就绪）、voicebench{openbookqa/mmsu-spoken/bbh}、voiceassistant-eval/listening×4
（+speaking/reasoning 可选）、air-bench/Foundation MCQ（Speech_Grounding 优先，余为声乐感知探针）、
audiocaps-qa（声音事件 QA——CLAP 合法域）。

**K9 语音查询→文本检索（原生检索基准）**：**squtr**（SIGIR-2026，BEIR/MTEB 协议、gold qrels、
**4 档噪声梯度 = τ/召回下界现成量表**；Stage-1 取 fiqa + MedicalRetrieval 迷你语料
= gold + 采样干扰）——**全集合唯一原生检索基准，检索质量测评的支柱**。

**K10 口语工具调用（离线可验证）**：audio2tool（expected_tool_call + 参数字典精确匹配；
取 tier1_direct 等最净层；152 工具注册表=knowledge source；CC-BY-NC eval-only）——
补上 tau2 被排除留下的工具调用空缺。

**K11 规则可验证**：voicebench/ifeval（IFEval 规则检查器，无需 judge 无需答案键）+
advbench（拒答率探针）。

### 1.2 排除 10 + 不在盘 6（每条带理由；deferred ≠ deleted）

| 数据集 | 理由 |
|---|---|
| covost2 | 盘上无音频（结构性；可恢复=CV mp3 子集补取） |
| mmsu | 盘上无 gold（结构性；可恢复=HF 元数据补取） |
| audiomc | **理由修正**：非"需交互 rollout"（历史转写已固化、离线可跑），真障碍=整体性 rubric-judge 评分、无离散答案键；建 omni-as-judge 后可复活 |
| soulx-duplug | 全双工 owner 已裁出 + 无知识/QA 键 |
| eva-bench | 需活体用户模拟器+工具执行器（确定性 SHA 校验部分无法离线复用） |
| tau2-bench | 需 DB 环境+模拟器；仅作可验证机制模板 |
| aime24/25/26 | 无音频、文本自足（口语数学已由 uro Gsm8kEval/APE-zh/MLCpro 覆盖）；可选角色=文本推理天花板对照（不入语音键计数） |
| auditorybench++ | 实勘 0 音频文件（设计上纯文本） |
| m3ed（不在盘） | 百度盘手动，owner 已豁免 |
| slue-sqa-5 / esc-50 / fsd50k（不在盘） | 未取的开放候选 |
| mlc-slm / full-duplex-bench-v3（不在盘） | gated / 渠道不稳，owner 已弃 |

另：uro/voiceassistant 的 open-judged 与音频输出子集（GenEmotion/GenStyle/SRT/SpeakerAware、
AlpacaEval 系等）按子集级排除，理由=judge 依赖或需模型发声（text-out 冻结解码域外）。

## 2. 类型 → 评测方案（每类的具体协议，survey 锚定）

| 类型 | 可验证奖励 | 检索评测协议 | 键空间 | 特殊纪律 |
|---|---|---|---|---|
| K1/K2 内容 ASR | 1−WER（jiwer，norm 与 kb_audit 同空间） | VocSim 内容同一性 cosine；困难样本记忆=pool→eval 门控曲线（kNN-Whisper 负对照协议） | 内容键（GLAP/LCO/自身隐态）；**CLAP 必死**（协议有效性） | pool≠eval 天然划分；zh 侧 aishell-1 |
| K3 LID | 语言 EM + gender EM | MAEB 式跨模态语言探针 | 内容键 + Dasheng（唯一 LID 直接证据） | CLAP 多语 <3% 负对照 |
| K4 SER | 情感 EM / macro-F1 | X-ARES SER probe+kNN + VocSim 同情感 | E2V-S/e2v+/Dasheng vs 单空间读出（**H-a vs H-b 副语言战场**） | crema-d 解缠对比对；zh 空缺必测（⚠#26） |
| K5 SID/SV | 说话人 EM + trial-pair EER | X-ARES speaker-kNN + 开集 EER | ERes2NetV2/CAM++/ReDimNet/WavLM-L | omni 原生 speaker 键=确认不存在（W4 cell） |
| K6 intent | intent EM | 同意图样例 R@k → few-shot 注入增益 | 内容键 + MERaLiON-SE2 | CLAP 意图近随机负对照 |
| K7 slot | slot F1（slue scorer） | **两级检索默认**（utt 键检标注整句→ICL 定位）；frame/多向量后备 | 内容键（+CLSP 若批准） | F5：无成熟 late-interaction |
| K8 QA/MCQ | EM/数值/containment | 知识注入 τ/α/δ_corr 测量主面 + 内容键 R@k | 内容键三候选对决 | heysquad scrub 门；T0 ceiling 标签纪律 |
| K9 原生检索 | R@1/R@10/nDCG@10 vs gold qrels | **BEIR/MTEB 标准协议 + 4 档噪声 = τ/召回下界曲线** | 全部内容键候选正面对决 | H-a/H-b 主裁决场；迷你语料=gold+采样干扰 |
| K10 工具调用 | tool EM + 参数 dict 匹配 | 意图→工具注册表检索 | 内容键 | NC eval-only |
| K11 规则 | checker 通过率 / 拒答率 | —（生成面） | — | 无 judge 无答案键，最廉价加项 |

**约束项测量落点映射**（战役 P5 对齐）：τ→K8+K9（selector-oracle 差 + qrels 检索质量）；
τ* 门控曲线→K1/K2 困难样本记忆 + K9 噪声梯度；N*→W1 既有 best-of-N（K1）+K8 MCQ；
δ_corr→K8（双系统/跨模型验证器）；R→K6/K7 few-shot 影响；α→K8 反事实采纳（T9 协议扩展+补 CI）；
召回下界→K9 原生 qrels。

## 3. loader 工程量清单（P3 输入）

现成 7（minds14-zh/mmau/bba/spoken-squad/SQuAD-zh/OpenbookQA-zh/vocalbench-zh）+ T7/T8 内联
（heysquad，需抽公共）。需新建（全部薄层，parquet/json/文件名解析）：librispeech、fleurs-r
（解压）、crema-d（文件名码）、meld（ffmpeg）、slurp（jsonl+flac）、speech-massive、mmar（解压）、
uro bucket-A ~10 个薄 loader、vocalbench×4 轴、voicebench×5 子集（ifeval 需移植 checker）、
voiceassistant-eval（宽 schema）、air-bench（Foundation_meta.json）、seed-tts-eval（**先核 audio
列是 target 还是 prompt 音**）、aishell-1/thchs-30/cn-celeb1/voxceleb1-test/esd/csemotions、
audiocaps-qa、audio2tool、squtr（zipfile 直读）≈ **28 个薄 loader**。

## 4. 与其余覆盖线的接口

模型矩阵：`2026-07-09-coverage-model-matrix.md`；理论台账：`2026-07-09-theory-scheme-coverage.md`；
战役设计书（约束项/loop）：`2026-07-09-stage1-dual-track-campaign.md`。
勘察原始档：session scratchpad `coverage/`（datasets-candidates11.json、datasets-lock-first14.md、
第二半在本文成文时直接吸收）。**本文不做选型；纳入/排除按结构性标准执行，键选型与 T11 设计
留收敛门。**
