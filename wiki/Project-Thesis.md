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

## 2026-07-12 supersession note — primary study & flagship framing

> **What changed (owner ruling, Decision-Log 续24 / G0 2026-07-11).** The **series thesis above is
> unchanged** — training-free, **weight-frozen reward-guided inference-time optimization** of a frozen
> speech/omni MLLM. What is re-centered is *which work carries the primary study*:
>
> - **W1 (`speech-mllm-training-free-rl`) now carries the current PRIMARY study** — a front-end
>   **Retrieve–Discover–Use (RDU)** knowledge subsystem over a frozen omni core **plus a reward-guided
>   trajectory-selection operator**; primary metric = **selector realization rate
>   ρ = (R_selector − R_greedy)/(R_oracle − R_greedy)** (G0). Proposal **v4.1** is drafted and
>   **pending external review + owner signature** — not yet a passed / Stage-2 plan.
> - **W4 (`speech-mllm-omni-embedding-rl`) remains a SEPARATE work, repositioned per G0.** The
>   task-conditioned **disentanglement** headline is dropped/downgraded to **L0/L1 embedding-utility
>   studies** (readout availability / suppression / selective-readout limits); a fresh proposal is
>   **pending ticket #29**. W4 still studies the omni's **own embedding space** — untouched by W1's
>   demotion of the core 2048d hidden state to a white-box diagnostic arm.
>
> Lineage: G0 ruling [[2026-07-11-stage1-audit-response-and-rulings]] §4 · Decision-Log 续24 (2026-07-12)
> · proposal [[2026-07-12-research-proposal-v41-external-review]]. Passages below tagged
> **[superseded 2026-07-12 → see note]** are kept for history; this note is the current statement.

## Flagship claim (W4) [superseded 2026-07-12 → see note above]

> Training-free RL can steer a **frozen omni-embedding model** so that **different task-conditioned
> embeddings of the same audio yield different, individually-better downstream performance** across
> content/ASR+ST, speaker-ID, emotion/SER, and language+intent — demonstrating disentanglement of a
> frozen model's representation purely by reward-guided activation.

> **2026-07-11 更正**：W4「task-conditioned disentanglement」主张按 [[2026-07-11-stage1-audit-response-and-rulings]] 降级为 L0/L1（readout availability/suppression；matched>mismatched 判据未过）；disentanglement 措辞在 L2–L3 判据通过前废止；W4 将按 §7.1 问法重新立项（#29）。G0 现行 primary question 见该文档 §4。

The flagship backbone is `omni-embed-nemotron-3b` (NVIDIA, ~4.7B, output = dense vector dim 2048; a
bi-encoder retrieval model built on the Qwen2.5-Omni Thinker). The exact inference-time *operator*
(where the reward-guided search acts) and its mathematical convergence conditions for the speech
modality are argued in [[W4-Training-Free-RL-Feasibility]].

## How the four works relate

The series is a progression, all grounded in training-free / lightweight RL that does not update base
weights. **W4 is the flagship first study**; **W1 is the mature training-free *pattern* reference**
whose verifiable-reward and evaluation machinery the others reuse. [superseded 2026-07-12 → see note]
**Current framing (2026-07-12):** W1 carries the primary study — RDU + reward-guided selector, ρ per
G0; W4 is a separate work repositioned to L0/L1 embedding-utility studies. See the supersession note
above.

| # | Work (repo) | Role | Focus |
|---|---|---|---|
| **W4** | `speech-mllm-omni-embedding-rl` | **Flagship** [superseded 2026-07-12 → see note]; now a **separate work, repositioned per G0** | training-free RL on a frozen omni model's own embeddings — disentanglement headline dropped → L0/L1 embedding-utility studies (fresh proposal pending #29) |
| **W1** | `speech-mllm-training-free-rl` | **Pattern reference → now carries the primary study** (2026-07-12) | mature, reusable training-free reward/eval machinery (best-of-N, reward-guided decoding, reranking); primary study = RDU front-end knowledge system + reward-guided trajectory selector (ρ per G0), proposal v4.1 pending signature |
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

### 2026-07-12 取代说明 — primary study 与旗舰框架

> **变更（owner 裁决，Decision-Log 续24 / G0 2026-07-11）。** 上文**系列主旨不变**——免训练、
> **权重冻结的 reward-guided 推理时优化**。改变的是**哪个工作承载 primary study**：
>
> - **W1（`speech-mllm-training-free-rl`）现承载当前 primary study**——冻结 omni 核心之上的前端
>   **检索–发现–使用（RDU）**知识子系统 **+ 一个 reward-guided 轨迹选择算子**；primary 指标 =
>   **selector 实现率 ρ = (R_selector − R_greedy)/(R_oracle − R_greedy)**（G0）。提案 **v4.1** 已起草，
>   **待外审 + owner 签字**，尚未通过评审、未进 Stage-2。
> - **W4（`speech-mllm-omni-embedding-rl`）仍为独立工作、按 G0 重定位。** task-conditioned
>   **disentanglement** 头条已弃/降级为 **L0/L1 嵌入效用研究**（readout availability / suppression /
>   selective-readout limits）；fresh proposal **待票 #29**。W4 研究对象仍是 omni **自身嵌入空间**，
>   不受 W1 把核心 2048d 隐态降为白盒诊断臂影响。
>
> lineage：G0 [[2026-07-11-stage1-audit-response-and-rulings]] §4 · Decision-Log 续24（2026-07-12）·
> 提案 [[2026-07-12-research-proposal-v41-external-review]]。下文标 **[superseded 2026-07-12 → see note]**
> 者保留作历史，本说明为现行陈述。

### 旗舰科学主张（W4）[superseded 2026-07-12 → 见上方取代说明]

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

> **现行框架（2026-07-12，取代上文"W4 是旗舰首发"表述）**：W1 承载 primary study（RDU + reward-guided
> selector，ρ per G0，提案 v4.1 待签字）；W4 为独立工作、按 G0 重定位为 L0/L1 嵌入效用研究（fresh
> proposal 待 #29）。详见本页顶部 2026-07-12 取代说明。
