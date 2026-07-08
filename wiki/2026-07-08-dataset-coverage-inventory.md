# 2026-07-08 · 28 个 lock 数据集的覆盖度盘点（讨论材料）

> **用途**：为"覆盖最广的数据方案"讨论提供底表（owner 2026-07-08 指示：Stage-1 最高优先 =
> 数据集覆盖度，所有小规模数据集完成验证）。来源：`docs/datasets.lock.json` +
> `docs/data.md` + W1 `scripts/knowledge/kb_registry.py` + `scripts/p2_baselines.py`。
> lock ↔ kb_registry 已交叉核对：28/28 双向对齐，无孤儿。
> **性质**：盘点，非选型。检索评测适配性一列是初判，待 2025+ 表征调研 + owner 讨论后定夺。

| 数据集 | 任务族 | 语言 | 体量 | 标注字段 | p2 loader | 小规模检索评测适配性（初判） |
|---|---|---|---|---|---|---|
| librispeech | ASR | en | 115.2G | transcript | 无 | 取 dev/test 小切片可用；960h 训练集只作困难样本记忆的**来源池** |
| covost2 | ST | 多语 | 282.9M | translation | 无 | 小体量，可直接用 |
| fleurs-r | ST/LID | 102 语 | 17.3G | translation + 语言标签 | 无 | 取 zh/en 子集切片 |
| crema-d | SER+SID | en | 578.4M | speaker-id + 6 类情感 | 无 | **双因子金标**（12 句 × 91 人）：同句异人/同人异句/同情异句的正负对天然可构造，解缠测评首选 |
| meld | SER | en | 32.4G | 情感标签（对话上下文） | 无 | 取切片；上下文情感与 crema-d 互补 |
| minds14 | SLU-intent | 14 语 | 1.1G | 14 类银行意图 | **有**（zh） | 就绪，意图检索评测首选 |
| slurp | SLU-intent+slot | en | 12.6G | intent + slot spans（BIO） | 无 | **slot 粒度唯一英文金标**，需新 loader |
| speech-massive | SLU-intent+slot | 12 语 | 30.3G | intent + slot spans | 无 | 多语 slot 金标（eval-only license，注意条款） |
| mmau-mini | 音频理解 MCQ | 混合 | 2.6G | MCQ 答案 | **有** | 就绪 |
| mmar | 音频推理 | 混合 | 2.8G | 文本答案 | 无 | 可用，需 loader |
| air-bench | 音频基准 | 混合 | 40.8G | 异构 | 无 | 异构、非检索结构——倾向排除，仅备查 |
| mmsu | 口语推理 MCQ | 混合 | 1.6G | MCQ 答案 | 无 | 可用，需 loader |
| big-bench-audio | 口语推理 QA | en | 304.6M | 文本答案 | **有** | 就绪（1000 条，快评优选） |
| voicebench | 口语 QA/agentic | 混合 | 10.4G | 混合应答 | 无 | 评分复杂——取其 QA 子集或排除 |
| heysquad | 口语 QA | en | 13.6G | 抽取式答案 | 无（T7/T8 有内联加载） | 可用但 **value 含 gold 泄露**，必须 scrub（T8 先例） |
| spoken-squad | 口语 QA | en | 3.2G | 文本答案 | **有** | 就绪 |
| uro-bench | 口语对话 | en+zh | 11.3G | 子集各异 | **有**（SQuAD-zh、OpenbookQA-zh 子集） | SQuAD-zh 子集就绪；其余子集逐个评估 |
| vocalbench | 口语对话 | en | 4.6G | 会话应答 | 无 | 9 轴会话评测，检索评测价值待定 |
| vocalbench-zh | 口语对话 | zh | 3.7G | QA 答案 | **有** | 就绪 |
| voiceassistant-eval | 语音助手 | 混合 | 8.8G | 13 类任务应答 | 无 | 超出简单 QA——倾向排除，仅备查 |
| audiomc | 语音助手多轮 | 混合 | 4.9G | 多轮应答 | 无 | kb_registry 已标 **deferred**（需交互 rollout）→ 排除 |
| soulx-duplug | 全双工对话 | en+zh | 316.7M | 无离散答案结构 | 无 | **非知识任务** + 全双工已出局 → 排除 |
| eva-bench | 语音 agent | 混合 | 257K | agent 应答 | 无 | 需模拟器 → **deferred/排除** |
| tau2-bench | 语音 agent 工具 | 混合 | 25M | 工具调用 | 无 | 需外部 DB 环境 → **deferred/排除** |
| seed-tts-eval | TTS 评测 | 混合 | 357.4M | 参考转写 | 无 | 非检索任务 → 排除（TTS 侧另议） |
| aime24/25/26 | 纯文本数学 | — | ~65K | 数学答案 | 无 | **非语音键** → 排除（3 条） |

## 任务族覆盖计数（28 条全列，无 silent cap）

- 建议**纳入**检索评测的：ASR 切片（librispeech dev/test）、ST（covost2、fleurs-r 子集）、
  SER+SID（crema-d、meld 切片）、SLU-intent（minds14、slurp、speech-massive）、
  SLU-slot（slurp、speech-massive）、音频理解/推理（mmau-mini、mmar、mmsu、big-bench-audio）、
  口语 QA（heysquad-scrubbed、spoken-squad、uro-bench/SQuAD-zh、vocalbench-zh）≈ **17 个**。
- 建议**显式排除**（各带理由，上表）：air-bench、voicebench(整体)、voiceassistant-eval、
  audiomc、soulx-duplug、eva-bench、tau2-bench、seed-tts-eval、aime24/25/26 ≈ **11 个**。
- 现成 p2 loader：7 个（big-bench-audio、mmau-mini、vocalbench-zh、SQuAD-zh、spoken-squad、
  minds14-zh、OpenbookQA-zh）；纳入清单中其余 ~10 个需补 loader（多为 parquet/清单读取，工作量低）。

## 覆盖缺口提示（供讨论）

1. **slot 粒度**只有 slurp / speech-massive 两源，且都无现成 loader——若 slot 方案要评测，
   loader 是前置工程。
2. **说话人任务**只有 crema-d（91 人）规模偏小；纯说话人验证任务（VoxCeleb 类）不在 lock 内
   ——是否补充属 lock 增补决定，留讨论。
3. **ASR 困难样本记忆**需要"来源池 ≠ 评测集"的划分：librispeech train(960h) 作记忆池、
   dev/test 作评测是天然划分；zh 侧 ASR 缺对应资源（fleurs-r zh 子集可代）——留讨论。
4. 多语覆盖集中在 minds14/speech-massive/fleurs-r；zh 内容型任务靠 uro-bench 子集 +
   vocalbench-zh，规模中等。
