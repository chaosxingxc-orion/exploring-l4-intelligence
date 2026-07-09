# lock 前 14 类型学（Opus 终报存档，2026-07-09）

## 三个推翻先前盘存的实地发现
1. covost2 无音频（仅 tsv/；mp3 在 Common Voice，不在 lock）→ exclude 结构性；可恢复=拉 CV mp3（超 Stage-1 范围）
2. mmsu 无 gold（仅 audio/*.wav 任务前缀名；全树无 question/choices/answer）→ exclude；可恢复=HF 补元数据（补后为最强音频推理集之一）
3. fleurs-r 仅 12 语言（af/am/ar/as/ast/az/be/bg/bn/bs/ca/ceb）无 en/zh、TSV 无翻译目标 → include-subset 改判 LID+多语ASR+gender；音频 tar 未解压
→ **ST 任务族在本半无可跑音频源**（covost2 无音频 + fleurs-r 无翻译）

## 判定表（12 include / 2 exclude）
| 数据集 | 判定 | loader | 要点 |
|---|---|---|---|
| librispeech | include | 建（易） | eval=test.clean n40/60 长度分层；memory-pool=train960（pool≠eval 天然划分）；1−WER 奖励；CLAP 必死负对照 |
| covost2 | **exclude** | — | 无音频 |
| fleurs-r | include-subset | 建+解压 | 12 语平衡 5/语；LID 12-way EM + 每语 WER + gender 二元；CLAP 多语 <3% 负对照 |
| crema-d | include | 建（易） | **标签用文件名码**（train/test.csv 的 classname 中性偏斜 ~54% 且与文件名冲突~54%——已记 gotcha）；6 情感×91 说话人×12 句×4 强度；同句异人/同人异情天然对比对=解缠对照 |
| meld | include-subset | 建+ffmpeg | mp4→wav；7 情感不平衡→分层+macro-F1 |
| minds14 | include | **有** | zh 就绪；扩 en-US；CLAP 意图近随机负对照；MERaLiON IC 98.95 强键参照 |
| slurp | include-subset | 建 | test.jsonl 按 18 scenario 分层；slurp_real 每 id 取一录音（prefer non-headset）；intent EM ~60 类 + slot F1（slue/slurp scorer，repos/slue-toolkit 在盘）；pool=train.jsonl |
| speech-massive | include | 建 | 无 test split→validation 为评测；train_115=few-shot 池；**CC-BY-NC-SA eval-only**；speaker_sex/age = 附赠说话人属性金标（多语 SID 副测） |
| mmau-mini | include | **有** | 就绪 |
| mmar | include-subset | 建+解压 | MMAR-meta.json + 音频 tar；按 category 分层（Signal/Perception/Semantic/Cultural） |
| mmsu | **exclude** | — | 无 gold（MIT；补元数据后转 include） |
| big-bench-audio | include | **有** | 就绪，快评首选 |
| heysquad | include eval-only | T7/T8 内联→抽公共 | **高泄露风险**：context 含答案 answer_in_own_KB=1.0；KB 用途必须 kb_audit scrub + verdict==CLEAN 门 |
| spoken-squad | include | **有** | WavRAG R@10 .9023 = frozen-omni 隐态键 vs GLAP/LCO 的对决先例场 |

## 类型学（前半 7 类，方案摘要）
- T-A 内容/ASR（librispeech）：1−WER 可验证奖励；VocSim 内容同一性检索；CLAP 负对照；pool/eval 分离；paired-bootstrap CI n60
- T-B 多语 LID+gender（fleurs-r 12 语）：12-way EM + 每语 WER；MAEB 式跨模态语言探针
- T-C 副语言 SER+SID（crema-d, meld, +speech-massive 属性, fleurs-r gender）：X-ARES SER+SID probe+kNN（CREMA-D 原生任务）+ VocSim 同一性；同句异人 vs 同人异情=**解缠对照**；键=ERes2NetV2/E2V-S/Dasheng/CLAP 弱基线；MELD macro-F1
- T-D SLU intent+slot（minds14, slurp, speech-massive）：intent EM + slot F1；slot 走 F5 两级检索；CLAP 意图负对照
- T-E 音频理解/推理 MCQ（mmau-mini, mmar）：MCQ EM；主为生成/best-of-N 面（greedy→oracle headroom）
- T-F 口语 QA（bba, spoken-squad, heysquad）：QA EM/substring；WavRAG 先例场；**信息边界承重**（heysquad scrub 门）
- 共通复现底座：kb_snapshot 冻结 id + SLICE_SEED=20260705 + revision 钉扎 + paired-bootstrap 方向性 CI + [directional|small-n] 分级

## 其他要点
- speech-massive license CC-BY-NC-SA-4.0 → 内部评测 only，不随发布
- meld GPL-3.0 再分发注意
- slurp/slue scorer 在盘（repos/slue-toolkit）
