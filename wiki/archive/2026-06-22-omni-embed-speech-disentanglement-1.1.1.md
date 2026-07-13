# 2026-06-22 · Omni-Embed Speech Disentanglement · Experiment 1.1.1

> Archival experiment report. Naming: `yyyy-mm-dd-{purpose}-{a.b.c}` where **a** = experiment family
> (1 = training-free activation/disentanglement of the frozen omni-embedding), **b** = experiment &
> dataset variant under that family (1 = CREMA-D, single-instruction conditioning + layer/pooling),
> **c** = minor version (1). Companion: [[W4-Training-Free-RL-Feasibility]], [[Per-Work-Status]].

**Status of conclusions: PROVISIONAL.** The headline negative ("speaker/emotion unrecoverable by
Operator A") is **scoped to a weak intervention** and is *not* a refutation of training-free
activation — see §4. The strongest weight-free lever for this model class (in-context learning /
activation heads) was **not tested** in 1.1.x and is the subject of experiment 1.2.

## 1. Question

Can a frozen omni-embedding model (`omni-embed-nemotron-3b`; Qwen2.5-Omni Thinker → mean-pool →
L2-norm; 2048-d; bi-encoder contrastive retriever) be made — *without changing weights or structure* —
to expose different speech factors (content / emotion / speaker) of the same audio, so that "different
(task-conditioned) embeddings yield different downstream performance"?

## 2. Setup

Frozen model (sdpa; flash-attn unavailable on sm_120). CREMA-D, filename ground truth (content =
sentence-ID 12 classes; emotion 6; speaker 91). Seeded balanced split dev 600 / test 300, seed 42.
Verifiable reward/metric = kNN (k=5) probe accuracy; 1000-bootstrap CIs. Operator A tested in two
forms: **(i)** single task instruction paired with the audio (`encode_document({text, audio})`);
**(ii)** weight-free architectural axes — masked-mean pooling of each of the 37 Thinker layers, and
audio-token-only pooling. Reproducible: `bash scripts/train.sh seed=42 run_name=cremad_three_factor_v1`;
layer/pooling via `scripts/layer_sweep.py`, `scripts/audio_pool_probe.py`. Tracked in MLflow.

## 3. Results

**3a. Conditioning × factor (test probe accuracy):**

| conditioning \ factor | content (chance 0.083) | emotion (0.167) | speaker (0.011) |
|---|---|---|---|
| baseline (no instruction) | 0.997 | 0.360 | 0.040 |
| content instruction | 1.000 | 0.333 | 0.043 |
| emotion instruction | 1.000 | 0.367 | 0.037 |
| speaker instruction | 1.000 | 0.367 | 0.033 |

**3b. Layer / pooling sweep (best layer per factor):**

| pooling | content | emotion | speaker |
|---|---|---|---|
| full sequence, best layer | 0.990 (L24/36) | 0.400 (L0) | 0.043 (L36) |
| audio-tokens, best layer | 0.990 (L16) | 0.403 (L0) | 0.043 (L32/36) |

## 4. Analysis (incl. the critique that resets the conclusion)

**What 3a–3b *do* show.** (P1, intrinsic readout) The same frozen vector yields content ≈1.00, emotion
≈0.36–0.40, speaker ≈chance — the embedding is content-dominated, retains partial emotion, and carries
almost no recoverable speaker identity *under the readouts tested*. This matches the
retrieval-contrastive training profile.

**What they do NOT show — and why the earlier "B-mandatory" conclusion is withdrawn.** The conditioning
in 3a is a single short instruction; in 3b only the pooling layer/mask changes. **None of this changes
the *input* in the way this model class is most responsive to.** Qwen2.5-Omni-class models' strongest
capability is **in-context learning**: their forward pass (and therefore the pooled embedding) is
reshaped by *demonstrations and rich context*, not by a 5-word instruction prefix that a contrastive
retriever was never trained to obey (it shipped with only `query:`/`passage:`). A flat conditioning
column (3a) and a flat layer profile (3b) therefore falsify only **"single-instruction + architectural
axes,"** not **"training-free activation."** The genuinely strong, still-untested weight-free lever is
ICL / activation heads (§5). So: speaker/emotion are **not yet** shown to require Operator B — that
claim is downgraded to *provisional, pending experiment 1.2*.

**Mechanistic reading.** Mean-pooling over ~50 content-oriented audio tokens is dominated by the
content direction the contrastive objective optimized; a few instruction tokens have little leverage to
re-weight it, and LoRA-on-the-LLM retrieval tuning may damp—but does not necessarily destroy—the base
model's ICL. Whether ICL survived is an empirical question 1.2 must answer, not assume.

## 5. Do we need activation heads / ICL? (analysis → experiment 1.2)

Yes — this is the correct next intervention, and it is still training-free (input construction +
readout only, no weight/structure change). Candidate "activation heads" (each = a conditioning +
readout operator that aims to surface one factor), in increasing faithfulness to the model's native
abilities:

1. **Text-query zero-shot / cross-modal retrieval (native mode, cheapest, highest-priority).** The
   model is a *retriever*: encode the target audio as a document and a set of label-describing **text
   queries** (e.g. "a recording of an angry voice", "speaker number 12 talking") with `encode_query`;
   classify by max cosine. This uses the exact query↔document geometry the model was built for, which
   1.1.x bypassed (we ran kNN probes on document embeddings only). This is the most likely route to
   recover emotion (and a per-speaker enrolment query for speaker).
2. **Few-shot in-context demonstrations.** Build a document with k labelled audio examples followed by
   the target (`[demo_audio→label] × k, [target_audio]`). The demos define the task in-context and can
   shift the target's representation. **Complication:** full-sequence mean-pooling blends demos and
   target — mitigate by pooling only the *target* audio-token positions (we already have audio-token
   pooling), or by the difference vector `e(target | demos) − e(target | none)`. Sweep k∈{2,4,8},
   balanced demos from dev, target from test (no leakage).
3. **Rich / structured activation prompts.** Beyond a task name: attribute-eliciting prompts ("attend
   only to vocal tone, pitch and affect; ignore the words"), paraphrase ensembles, multi-turn framing.
4. **Activation-head bank + verifiable-reward selection.** Treat {query-set, demo-set, prompt, readout,
   pooling} as the Operator-A action variable z; select per factor by the verifiable probe/retrieval
   reward. This is exactly the formal `q*(z) ∝ q0(z)·exp(R/β)` — now over the **ICL action space**, a
   far more faithful instantiation of "training-free RL activation" than swapping one instruction.

Risk: heavy contrastive LoRA tuning may have attenuated ICL; design 1 (native retrieval) is robust to
that, designs 2–3 are the real test of residual ICL. Decision rule: if emotion/speaker rise materially
under any weight-free activation head (esp. design 1), Operator A is viable and the B-mandatory claim is
refuted; only if *all* ICL/activation forms also stay flat do we conclude Operator B is required.

## 6. Limitations

Content factor = sentence-ID over 12 fixed sentences (small closed set, easy for a content-native
model). Speaker = 91-way closed set with ~6.6 dev samples/speaker (hard probe; but flatness across
layers+pooling indicates genuine low signal, not only probe weakness). kNN probe (a stronger probe or
the native retrieval readout may extract more — see §5.1). Single dataset (CREMA-D, acted speech);
VoxCeleb/MELD untested. Operator B not yet implemented (so any "B" claim is inference, not evidence).

## 7. Next experiments

- **1.2.1** — Activation heads / ICL on CREMA-D: design 1 (text-query zero-shot) + design 2 (few-shot
  with target-token pooling) for emotion & speaker; re-test the cross-probe inequality.
- **1.3.x** — Operator B (generative Qwen2.5-Omni best-of-N / MBR readout) for factors that survive ICL
  as still-suppressed.
- **1.4.x** — content/language fan-out on real tasks (LibriSpeech WER, CoVoST2/FLEURS BLEU, MINDS14
  intent), and a natural-speech speaker set (VoxCeleb/MELD) for external validity.

---

## 中文

> 归档实验报告。命名 `yyyy-mm-dd-{目的}-{a.b.c}`:**a**=实验大类(1 = 冻结 omni 嵌入的免训练激活/解耦),
> **b**=该大类下不同实验与数据集(1 = CREMA-D,单指令条件化 + 层/池化),**c**=小版本(1)。

**结论状态:暂定。** "speaker/emotion 无法被 Operator A 恢复 / 需 B"这一负面结论**只适用于一次很弱的干预**,
**不构成对免训练激活的否证**(见 §4)。本类模型最强的免训练杠杆——in-context learning / 激活头——在 1.1.x
中**未被检验**,留作实验 1.2。

**问题(§1)、设置(§2)、结果(§3)** 见英文区两张表(不重复)。要点:同一冻结向量在 content / emotion /
speaker 上分别约 0.99 / 0.36–0.40 / 接近随机;指令条件化各列近乎不变;层与音频-token 池化也无法把 speaker
抬离随机。

**分析与结论重置(§4):** 上述只证明了 P1(内禀读出):嵌入内容主导、情感部分保留、说话人在所测读出下几乎不可
恢复。**但它没有真正"改变输入"。** 我只换了一句任务指令、只动了池化层——而 Qwen2.5-Omni 类模型最强的是
**ICL**:真正能重塑 forward、进而移动 pooled 向量的是**上下文示范与富语境**,不是一句话前缀(况且这是个只用
`query:`/`passage:` 训练过的检索器,本就弱于服从指令)。所以"列平/层平"只证伪了"单指令+架构轴",**没有**证伪
"免训练激活"。因此"需 B"被降级为**暂定,待 1.2 检验**。

**是否需要激活头 / ICL(§5)——需要,且仍是免训练(只构造输入+读出,不动权重):**
(1)**文本-query 零样本 / 跨模态检索(原生模式,最便宜,最高优先)**:把目标音频作 document、把各标签描述作
text query(`encode_query`),按最大余弦分类——这是模型被训练来做的事,而 1.1.x 完全绕过了它(只在 document
向量上跑 kNN)。这是恢复情感/说话人最可能的路径。(2)**few-shot 上下文示范**:`[示范音频→标签]×k, [目标音频]`,
注意全序列均值池化会把示范和目标混在一起——用**只池化目标音频 token**或**差向量** `e(目标|示范)−e(目标|无)`
来隔离。(3)**富结构激活提示**(描述要关注的声学属性/释义集成)。(4)**激活头库 + 可验证奖励选择**:把
{query集、示范集、提示、读出、池化} 当作 Operator-A 的动作变量 z,按可验证奖励逐因子选——这正是
`q*(z)∝q0(z)·exp(R/β)` 在 **ICL 动作空间**上的实例,远比换一句指令更忠实于"免训练 RL 激活"。判定规则:只要任一
免训练激活头(尤其是设计 1)显著抬高情感/说话人,则 Operator A 可行、"需 B"被否证;只有当所有 ICL/激活形式也都
平坦,才能下"需 Operator B"的结论。

**局限(§6):** content 因子是 12 固定句的小闭集(对内容原生模型偏易);speaker 91 类、每人约 6.6 dev 样本(探针
偏难,但跨层跨池化都平说明确实信号弱);kNN 探针(原生检索读出或更强探针可能更高);仅 CREMA-D(表演语音),
VoxCeleb/MELD 未测;Operator B 未实现(故任何"B"说法目前是推断而非证据)。

**下一步(§7):** 1.2.1 = CREMA-D 上的激活头/ICL(设计1 文本-query 零样本 + 设计2 few-shot 目标-token 池化)重测
情感/说话人交叉探针不等式;1.3.x = 对经 ICL 仍被压制的因子上 Operator B;1.4.x = content/language 真实任务
fan-out(LibriSpeech WER、CoVoST2/FLEURS BLEU、MINDS14 intent)+ 自然语音说话人集做外部效度。
