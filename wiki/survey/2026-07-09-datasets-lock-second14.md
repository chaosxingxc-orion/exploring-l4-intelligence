# lock 后 14 数据集实地勘察存档（Opus 终报，2026-07-09；补 F5 存档缺口）

> 复评结论：**7/14 从排除翻为 include-subset**（uro-bench、vocalbench、vocalbench-zh(原就绪)、
> voicebench、voiceassistant-eval、air-bench、seed-tts-eval 改判）；6 个维持结构性排除
> （audiomc、soulx-duplug、eva、tau2、aime×3）。逐集 schema 盘上验证。

## uro-bench（MIT）——40 子集逐个开盘分桶
**bucket-A 可验证子集（纳入，~15 个）**：
| 子集 | n | 语言 | 参考形式 |
|---|---|---|---|
| SQuAD-zh | 153 | zh | 抽取式答案（loader 已有） |
| OpenbookQA-zh | 189 | zh | MCQ 字母（loader 已有） |
| **Gsm8kEval** | **582** | en | reference 列=数值答案（"5"/"75"）——最净 |
| GaokaoEval | 303 | en | 单字母 A–D |
| HSK5-zh | 100 | zh | 单字母（选项内嵌 source_text） |
| APE-zh | 190 | zh | 数值数学答案 |
| MuChoEval-en | 311 | en | 音乐 QA 短答（"Guitar"） |
| MLC / MLC-zh | 177/145 | en/zh | 事实包含 |
| MLCpro-en / -zh | 91/64 | en/zh | 口语算术数值包含 |
| Repeat / Repeat-zh | 252/127 | en/zh | 复述→WER/EM |
| UnderEmotion-en / -zh | 137/79 | en/zh | **emotion 列→改切 SER 分类**（可验证） |
| TruthfulEval | 470 | en | 可接受答案列表→包含（弱；标准是 judge） |

**bucket-B 排除（open/judged）**：AlpacaEval(-zh)、CommonEval、Wildchat(-zh)、Claude-zh、
Multilingual、Summary、LCSTS-zh、StoralEval、ClothoEval-en、CodeSwitching-en/zh、MtBenchEval
（多轮 source_wav0..4）。**bucket-C 排除（需模型发声输出）**：GenEmotion/GenStyle/SRT/
SpeakerAware（多音频输入）各 en/zh。
Gaokao/HSK5 选项内嵌解析同 OpenbookQA-zh；Gsm8kEval 走 reference 列。

## vocalbench（Apache-2.0）——轴级 parquet 已核
纳入 = **knowledge（2000 条短事实 QA，顶级 KB 检索源）/ reasoning（1000）/ multi_round（400，
Context 为内联文本可单轮跑）/ emotion（500，按 Question_emo 标签作 SER 分类）**；
排除 = creativity/instruction/robust_*（无参考）/safety（judged）。loader 镜像 load_vocalbench_zh。

## voicebench（ModelScope lmms-lab，各子集继承上游 license）
纳入 = **openbookqa（455 字母）/ mmsu-spoken（按域，MMLU 口语版字母）/ sd-qa（每方言 ~553 短答
——口音 ASR 鲁棒分层器）/ bbh（23 shard，Yes/No）/ ifeval（345，instruction_id_list+kwargs =
**程序化规则检查，无需参考无需 judge**）**；+ advbench（520，拒答探针）。
排除 = alpacaeval 系/commoneval/wildvoice/mtbench（open judged）。ifeval 需移植 IFEval checker。

## voiceassistant-eval（MIT）——宽 schema：user_audio_0..6 / ref_answers / image_0..4
纳入 = **listening/{general,music,sound,speech}**（单音频+短 ref_answers；listening/speech =
性别/说话人属性可验证分类）+ speaking/reasoning（1199，含 ref）可选。
排除 = viewing/multi_discipline（依赖 image_0——结构性）、speaking/{emotion,roleplay,safety,
robustness,multi_round,assistant,instruction_following}（发声输出/空 ref/judged）。
loader：audio=user_audio_0 bytes，gold=ref_answers[0]，滤掉 user_audio_1 非空行（保单轮）。

## air-bench（24.09；上游 Apache，底层音频各有 license）
纳入 = **Foundation 轨 MCQ**（Foundation_meta.json：question/choice_a..d/answer_gt/task_name；
14 任务目录，**Speech_Grounding 为唯一语音原生任务优先**，其余=声/乐感知探针）；
排除 = Chat 轨（GPT-4 judged）。loader 读 meta.json 非 parquet，路径解析到任务目录。

## seed-tts-eval（ModelScope-manual，research）——**改判 ASR 锚**
原生 TTS 任务不可用（需发声）。改判：（audio/ans 目标 wav ↔ text）= 干净 zh(404)+en(363)
ASR 对 → **zh+en ASR/内容读出鲁棒锚**（WER vs text）。
⚠ 前置核查：确认 audio 列是**目标** wav（读 text 内容）而非 prompt 说话人 wav——`ans` 路径
（wavs/<pair>.wav）是无歧义目标；若 audio 是 prompt 音则对 prompt_text 配对。

## 维持排除的 6 个（理由钉死）
- **audiomc**（MIT）：**排除理由修正**——历史转写已固化（parquet user_turn_1..8 +
  assistant_turn 转写），单轮切片可构造、离线可跑；真障碍 = 整体性多准则 rubric-judge 评分、
  无离散答案键、无保构造的 EM/包含归约。kb_registry 的 "needs interactive rollout" 标注不准确。
  建成 omni-as-judge 后可复活为 judged 记忆探针。
- soulx-duplug：全双工 owner 已裁出 + 无离散答案键（测 turn-taking 时序）。
- eva-bench（MIT）：确定性核 = 终态 DB SHA-256 对金标，但需活体用户模拟器+声明式工具执行器
  （D3 隔离审计：确定性件 HIGH、复合 MED）——离线不可跑。
- tau2-bench（τ² MIT）：需 DB 环境+LLM 用户模拟器；仅作可验证机制模板。
- aime24/25/26：无音频、文本自足；TTS 合成=新数据工程（超范围）；口语数学已由
  uro Gsm8kEval/APE-zh/MLCpro 覆盖。可选=文本推理天花板对照（不入语音键计数）。

## 本半类型学补充（并入统一表 K8/K4/K11/K1 等）
- 口语可验证 QA（audio-key→离散答案）= Stage-1 主力面（最大最廉价最净 headroom 信号）
- 副语言分类改切（emotion/Question_emo/gender 列→可验证分类）——把"散文参考/发声输出"任务
  抢救回可验证域，喂 omni 的非 commodity 感知面
- 程序/规则可验证（ifeval/advbench）——无 judge 无答案键的最廉价加项
- ASR/内容读出鲁棒（seed-tts 改判 + sd-qa 口音分层 + Repeat）
- 结构排除类：judge 依赖/活体模拟器/无音频/需发声——deferred ≠ deleted
