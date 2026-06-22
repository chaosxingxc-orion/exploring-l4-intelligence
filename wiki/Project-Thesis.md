# Project Thesis

The single, canonical statement of what this repo is for. Everything else — the four works, the
shared library, the experiments — serves this thesis. Read this first, then [[Per-Work-Status]].

## Thesis (north star)

A modern multimodal / omni LLM has already absorbed broad, **cross-modal, multi-granularity task
knowledge** during pretraining — speech recognition, speaker identity, content understanding,
dialogue, translation — from large-scale unsupervised and parallel corpora. This series asks one
question:

> **How far can _training-free RL_ — reward-guided optimization that changes no weights and no model
> structure — go to _activate_ that latent knowledge and lift a frozen model's out-of-the-box
> performance on specific speech tasks?**

We treat the pretrained model as **fixed** and search, at inference time, over its own behaviors
(decoding, candidate selection, task-conditioning, representation read-out) under **verifiable
rewards**. No fine-tuning, no LoRA, no gradient on the base model.

## Three terms (defined once, used everywhere)

- **Training-free RL** — reward-guided, gradient-free optimization performed at inference time
  (best-of-N, reward-guided decoding, reranking, task-conditioning, inference-time representation
  search) that leaves the base model's weights and architecture untouched. W1 is the mature reference
  implementation of this *pattern*.
- **Activation of pretrained knowledge** — eliciting capabilities the base model already holds but
  does not surface out-of-the-box, by steering it with verifiable task rewards rather than re-training.
- **Speech disentanglement** — for an omni / embedding model, steering a *single* audio input's
  representation so that **task-conditioned views** (content/ASR+ST, speaker-ID, emotion/SER,
  language+intent) become separable and each yields strong, task-specific downstream performance —
  i.e. different task conditioning produces different, individually-better representations of the same
  audio *without changing the model*.

## Flagship claim (W4)

> Training-free RL can steer a **frozen omni-embedding model** so that **different task-conditioned
> embeddings of the same audio yield different, individually-better downstream performance** across
> content/ASR+ST, speaker-ID, emotion/SER, and language+intent — demonstrating disentanglement of a
> frozen model's representation purely by reward-guided activation.

The flagship backbone is `omni-embed-nemotron-3b` (NVIDIA, ~4.7B, output = dense vector dim 2048; a
bi-encoder retrieval model built on the Qwen2.5-Omni Thinker). The exact inference-time *operator*
(where the reward-guided search acts) and its mathematical convergence conditions for the speech
modality are argued in [[W4-Training-Free-RL-Feasibility]].

## How the four works relate

The series is a progression, all grounded in training-free / lightweight RL that does not update base
weights. **W4 is the flagship first study**; **W1 is the mature training-free *pattern* reference**
whose verifiable-reward and evaluation machinery the others reuse.

| # | Work (repo) | Role | Focus |
|---|---|---|---|
| **W4** | `speech-mllm-omni-embedding-rl` | **Flagship** | training-free RL to disentangle a frozen omni model's embeddings across content/ASR+ST, speaker-ID, emotion/SER, language+intent |
| **W1** | `speech-mllm-training-free-rl` | **Pattern reference** | the mature, reusable training-free reward/eval machinery (best-of-N, reward-guided decoding, reranking) |
| W2 | `speech-mllm-efficient-rl-alignment` | Supporting | efficient GRPO/DPO (LoRA) for speech↔language alignment |
| W3 | `speech-mllm-multitask-rl` | Supporting | one policy, RL across ASR/ST/SID/SER via verifiable rewards |

See [[Architecture]] for the repo model and shared library, [[Data-and-Assets]] for models/datasets,
and [[Decision-Log]] for why the series was re-centered on this thesis.

---

## 中文

本仓存在的唯一、权威目的陈述。四部曲、共享库、所有实验都服务于这个主旨。请先读本页，再读
[[Per-Work-Status]]。

### 主旨（北极星）

现代多模态 / omni 大模型在预训练阶段，已经从大规模无监督数据与平行语料中吸收了**跨模态、多粒度的
任务知识**——语音识别、说话人识别、语音内容理解、语音对话、翻译。本系列只问一个问题：

> **仅靠「免训练 RL」——不改权重、不改结构、由奖励引导的推理时优化——能在多大程度上「激活」这些潜藏
> 知识，从而提升一个冻结模型在特定语音任务上的开箱即用表现？**

我们把预训练模型视作**固定**，在推理时、在**可验证奖励**下，搜索模型自身的行为（解码、候选选择、
任务条件化、表示读出）。不微调、不 LoRA、不对基座求梯度。

### 三个术语（只定义一次，全仓通用）

- **免训练 RL（training-free RL）**：推理时进行的、免梯度、奖励引导的优化（best-of-N、奖励引导解码、
  重排、任务条件化、推理时表示搜索），不动基座的权重与结构。W1 是该范式的成熟参考实现。
- **预训练知识激活**：用可验证的任务奖励引导模型，把它「已具备但开箱不显现」的能力 surface 出来，
  而非重新训练。
- **语音解耦（speech disentanglement）**：对 omni / 嵌入模型，引导同一段音频的表示，使其在不同
  **任务条件**下（内容/ASR+ST、说话人、情感/SER、语言+意图）变得可分离、且各自在对应下游任务上更强
  ——即不改模型、仅靠不同条件化即可得到不同且更好的表示。

### 旗舰科学主张（W4）

> 免训练 RL 可以引导一个**冻结的 omni 嵌入模型**，使**同一段音频在不同任务条件下的嵌入产生不同、且
> 各自更优的下游表现**，覆盖内容/ASR+ST、说话人、情感/SER、语言+意图——从而证明：仅靠奖励激活，就能
> 解耦一个冻结模型的表示。

旗舰底座是 `omni-embed-nemotron-3b`（NVIDIA，约 4.7B，输出 2048 维稠密向量；基于 Qwen2.5-Omni Thinker
的双编码器检索模型）。免训练 RL 究竟作用在哪一层（算子形态），以及它对语音模态的数学收敛条件，见
[[W4-Training-Free-RL-Feasibility]]。

### 四部曲如何关联

整个系列是一条递进线，全部建立在「不更新基座权重」的免训练 / 轻量 RL 之上。**W4 是旗舰首发工作**，
**W1 是成熟的免训练「范式」参考**，其可验证奖励与评测机制被其余工作复用。各工作的角色与重心见上方
英文表（不重复表格）。仓库结构与共享库见 [[Architecture]]，模型与数据见 [[Data-and-Assets]]，系列为何
重定到此主旨见 [[Decision-Log]]。
