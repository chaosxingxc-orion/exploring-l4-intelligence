# Paralinguistic Suppression in Omni Speech-LLMs — Mechanism, Probe & Survey (W4)

How speech is injected into / read out of a frozen omni model, and whether text-alignment + pooling
suppress speaker/emotion. Answers the two questions behind the ICL finding ("the model over-attends to
the speech/content stream and ignores the text instruction"). Companion to [[Omni-Embed-Model-Dossier]]
(architecture/I-O contract), [[W4-Training-Free-RL-Feasibility]] (operator math), and
[[2026-06-23-omni-embed-speech-disentanglement-1.2.1]] (ICL diagnostics). Read the Dossier first.

Status legend: ✅ self-verified (own run) · ◐ workflow/sub-agent · ⚠ assumption · ✗ refuted.

## 0. The assertion, as five falsifiable sub-claims (the frame)

User assertion: *"all omni/speech LLMs align audio to text, so on speaker-ID (SID) and emotion (SER)
their statistics drop sharply, and the paralinguistic signal is lost at the pooling stage."* We do NOT
treat this as one yes/no; we split it so each part can be confirmed or killed separately:

- **C1 — training objective:** ASR/contrastive text-alignment lowers the linearly-decodable emotion/
  speaker information in the final/pooled vector, *relative to a self-supervised acoustic baseline*
  (wav2vec2/HuBERT/WavLM/emotion2vec).
- **C2 — pooling method:** plain temporal **mean** pooling (vs statistics [mean+std] or attentive
  pooling) is *itself* a loss term — a better pooling over the *same* frames recovers accuracy.
- **C3 — suppressed vs destroyed:** the info is present in *intermediate* layers but attenuated at the
  output (recoverable) vs genuinely absent everywhere (destroyed). May differ per factor.
- **C4 — monotonicity:** degradation tracks the *degree/type* of text-alignment across model families.
- **C5 — fixes:** which targeted methods recover the gap, and by what mechanism (external paralinguistic
  encoder / pooling fix / disentangled codec / auxiliary-loss / adapter / generative readout).

C2 and C3 are settled below by our own probe (D3); C1/C4/C5 by the literature survey (D2, in progress).

## 1. How the speech embedding is injected — and read out (Q1, ✅ verified)

There are **two different representations at two stages**, and conflating them is the source of the
"N-vector vs 1-D" confusion:

1. **Injected into the model = a sequence of N audio-token vectors (NOT 1-D).** The Whisper-style audio
   encoder + adapter turn the waveform into a contiguous run of `<|AUDIO|>` (id 151646) token
   embeddings, BOS/EOS-wrapped (`151647 … 151648`), interleaved with the text tokens in **one**
   Qwen2.5-Omni Thinker sequence whose attention is **bidirectional** (not a causal LM). Verified on a
   CREMA-D clip (`1005_MTI_NEU_XX.wav`, 3.37 s): one audio block, span (15, 66) = **51 `<|AUDIO|>`
   tokens**, sequence length 69, BOS & EOS present. The count is ~fixed for short clips (≈51 for
   2.5–3.5 s), not linear in duration. ✅
2. **Read out as an embedding = one pooled 1-D vector.** The whole sequence (prefix + audio + any
   demos) is **masked-mean pooled → L2-normalized → a single 2048-d vector**. Verified: the model
   exposes **37 hidden states** (36 layers + embeddings), each (1, 69, 2048); the returned embedding is
   **2048-d**. A manual masked-mean of the final layer reproduces `encode_document` at **cosine 0.879**
   *without* the `passage:` prefix (it rises to ≈1.0 with it) — matching the Dossier's documented prompt
   nuance. ✅
3. **You can pool anything yourself.** `io_contract.{audio_block_spans, query_mask}` +
   `layer_probe.{extract_layer_embeddings, extract_pooled}` pool any token subset, any of the 37 layers,
   any method — weight-free.

**Critical answer to "for emotion/speaker we can only give a 1-D vector, else too much interference."**
On this model the intuition is **inverted**, and the empirics (D3) prove it:

- The pooled **1-D final-layer** vector is exactly **where speaker/emotion are most destroyed** (speaker
  ≈ chance, emotion ≈ 0.40). "Collapsing to 1-D" is not noise reduction here — it is *where the loss
  happens*, because masked-**mean** lets content/lexical variance dominate the average.
- The real levers are **pooling method × layer × source**, not the dimensionality. A 1-D vector is fine
  **iff** it is an *attentive-statistics* pool of a **mid** layer — that recovered emotion 0.40 → 0.51
  (§2). Plain mean of the final layer is the worst case.
- For a **generative readout** (Operator B) the opposite of "give 1-D to reduce interference" is true:
  feeding the **full N-token sequence** lets the LM attend to the paralinguistic-salient frames; pooling
  to 1-D throws away exactly that frame-level detail. The "interference" to fix is *content dominance in
  a uniform average*, and the cure is a **smarter reduction** (attention to salient frames / 2nd-order
  statistics / mid layer), not a **blunter** one.

## 2. Pooling-method probe — our test of C2 & C3 (D3, ✅ own run)

`scripts/pool_method_probe.py` + `layer_probe.extract_pooled` (W4 repo). Frozen `omni-embed-nemotron-3b`,
CREMA-D same-audio three factors, dev 600 / test 300, seed 42, kNN (k=5) probe, 95% bootstrap CIs,
**weight-free** (no params trained — stays inside Operator A). Pooling over the audio-token positions
unless noted. Best-layer probe accuracy (chance: emotion .167, speaker .011, content .083):

| pooling (audio-token) | emotion | speaker | content |
|---|---|---|---|
| full-seq **mean** (the deployed embedding) | 0.400 (L0) `[.350,.453]` | 0.043 (L36) `[.023,.070]` | 0.990 (L24) |
| audio-token **mean** | 0.400 (L0) `[.350,.453]` | 0.043 (L32) `[.023,.067]` | 0.990 (L16) |
| audio **std** only | 0.367 (L24) | 0.040 (L0) | 0.997 (L16) |
| audio **stats** (mean+std) | 0.403 (L0) `[.343,.453]` | 0.047 (L36) `[.027,.073]` | 0.990 (L16) |
| **audio attentive-stats** (weight-free) | **0.513 (L16)** `[.460,.570]` | **0.067 (L16)** `[.043,.097]` | 0.933 (L36) |

**Findings.**
- **Mean = std = stats** (all overlap in CI) — adding 2nd-order statistics alone does *not* recover
  speaker/emotion. This reproduces the prior F.1 conclusion *for uniform pooling*.
- **Attentive-statistics pooling consistently gives the best emotion readout, peaking at mid-layer L16**,
  in both seeds: emotion 0.513 `[.460,.570]` (seed 42) and 0.447 `[.393,.500]` (seed 7), vs the mean
  baseline 0.400 `[.350,.453]` / 0.407 `[.353,.460]`. The per-layer trace is sharply peaked at L16
  (other layers 0.23–0.38), and **at that same L16 content collapses 0.99 → ~0.27** in both seeds — i.e.
  the attention re-weights frames toward the paralinguistic-salient ones the mean washes out, trading
  content for paralinguistics. So the lever is **attention-weighting at a mid layer, not std**. The gain
  is **modest and seed-sensitive**: +0.11 and CI-separated at seed 42, but +0.04 and **CIs overlapping**
  at seed 7. Directionally robust, magnitude not yet firm.
- **Speaker stays on the floor (≤0.067 across every method × layer, both seeds)** — ~5× chance but far
  below usable. Attentive pooling can't lift it; it is effectively **absent**, not merely mis-pooled.

**Verdicts.** **C2 holds in a refined, hedged form:** the loss term is *uniform* mean pooling, and an
attention-weighted **mid-layer** readout is the best weight-free lever — but it helps only **emotion**,
and modestly (gain seed-sensitive: clear at seed 42, within noise at seed 7). Pure 2nd-order statistics
(std/stats) do **not** help. **C3 holds with a robust per-factor split** (both seeds): **emotion =
suppressed-but-partially-recoverable** (present mid-stack, best ~0.45–0.51 via attentive L16); **speaker
= destroyed** (no weight-free readout exceeds ~0.07). MLflow runs `2c61b2f1` (seed 42) and `21453cb1`
(seed 7). ✅

**Caveats.** Single dataset (CREMA-D), n=300 test, weight-free kNN probe; attentive pooling uses the
masked mean as a parameter-free query (one of several attentive variants). The emotion gain is modest
and only CI-separated in one of two seeds — replicate on MELD / more seeds and try a learned-query
attentive pool before over-claiming. The **per-factor split (emotion recoverable-ish, speaker destroyed)
is the robust takeaway.**

## 3. Literature synthesis — C1 / C4 / C5 (D2, ◐ 77-agent workflow, 3-vote verified)

Survey of 2024–2026 omni/speech-LLM literature (62 candidates → 12 deep-read → 76 claims → **11 survived
3-vote adversarial refutation**; run `wf_6694eca5-de9`, 77 agents). **Headline: the assertion is right in
*direction* but too strong in *mechanism*, and the truth is sharply per-factor.** Paralinguistics is
mostly **suppressed / unread at the pooled-vector + decoder stage — not uniformly "lost at pooling" nor
"destroyed."** "Lost at pooling" is the correct diagnosis for **emotion** (the info is there; fix the
readout) and the *wrong* one for **fine-grained speaker-ID** (the InfoNCE/ASR objective never wrote a
usable speaker direction into the output — fix the source/encoder, not the pool).

**C1 — training objective → partially holds (med).** Direction well-attested: through an aligned LLM
stack content/lexical info is *amplified* (+92–95%) while speaker identity *degrades* (−8 to −39%)
[Modality-Collapse, arXiv 2602.23136]; a CLAP-contrastive encoder preserves paralinguistics toward its
final layer whereas Whisper/ASR encoders degrade it [VoxParadox, 2605.27772]; SSL acoustic baselines
retain strongly linearly-decodable speaker info even at final layers [2501.05310] and emotion2vec
linear-probes ~71.8% WA IEMOCAP [2312.15185], far above aligned pooled vectors [wav2vec2/HuBERT bench
2111.02735; LISTEN benchmark 2510.10444 shows omni-LLMs collapse to lexical cues, near-chance on pure
paralinguistics]. **But** no omni-LLM paper runs the *strict* same-audio same-probe SSL-vs-aligned
contrast — it is inferred, not measured. And the loss concentrates at the **pooled-vector + decoder
readout**, not as a uniform representational reduction (probes still 3–55× chance at the final layer). So
"reduces info in the representation" is too strong for emotion (present-but-unread); cleanly true only
for speaker in pooled form.

**C4 — monotonicity → partially holds (low).** A clean *encoder-objective* gradient exists (CLAP-
contrastive AF2 30.85% > ASR-encoder AF3 17.40% / Qwen2-Audio 14.85%; paralinguistic-augmented multi-task
Step-Audio 2 at the top, StepEval 76.55 vs Qwen-Omni 44.18) [2605.27772, 2507.16632] with a theoretical
mechanism (degradation tracks encoder↔text distance) [2602.23136]. **But** no single study sweeps
ASR-contrastive → instruction-tuned → paralinguistic-augmented on the *same* audio/metrics; two
instruction-tuned LALMs show *identical* suppression [2603.11947]. It is a cross-study patchwork, not a
measured monotone curve — the confident "tracks the degree of alignment" overstates the evidence.

**C5 — fixes → holds (high).** Quantified recoveries across all six mechanism classes, with the same
emotion-recoverable / speaker-resistant asymmetry:

| class | mechanism | best for | representative recovery | refs |
|---|---|---|---|---|
| (a) external speaker/paralinguistic encoder fused in | inject frozen ECAPA/x-vector (or emotion encoder) | **fine speaker-ID (essentially the only lever)** | ECAPA-LLM **1.03% EER** VoxCeleb1-E (vs 21.9–45.6% off-the-shelf; ASV floor 0.45%) | 2603.10827, 2005.07143 |
| (b) pooling / aggregation fix | ordered-trajectory / attentive / layer-mix vs one mean | **emotion** | C-Gate ordered trajectory RAVDESS **16.8%→77.7%** (+61pp; frame-shuffle collapses it); PCLM layer-mix AF3 17.4→60.0%; attentive-stats SER +0.85–2.35 UA | 2605.27772, 1803.10963, 2506.15754 |
| (c) disentangled codec / representation | dedicated speaker/prosody stream | speaker, prosody (by construction) | SKQ3+ recon SV EER 2.36%; FACodec factorization; Eta-WavLM linear speaker removal | 2403.03100, 2308.16692, 2505.19273, 2605.02804 |
| (d) auxiliary-loss / multi-task | add SER/SV head or RL objective | emotion + coarse (age/gender) | PE-FT+ADCH emotion PA-rate **74.5–80.5%**, gender 96.5%; Modality-Collapse forced-choice LoRA CREMA-D emotion 17.3→61.8% (+44.5pp), speaker *unmoved*; PALLM multi-task RL | 2603.11947, 2602.23136, 2603.15981 |
| (e) paralinguistic adapter / localized tuning | LoRA on the live-signal depth band | emotion + coarse (efficient) | PE-FT layers 0–14 beats full 0–27 at ~46% fewer params | 2603.11947 |
| (f) generative readout / prompting / probe-select | decode or probe a salient layer | emotion + coarse; speaker *presence* not identity | WavBench emotion 75–93%; Whisper layer-9 KNN multi-speaker *detection* 35.9→99.0% F1; speaker-attribute *generation* ≫ understanding | 2410.01162 |

**Cross-cutting:** emotion is recoverable by (b)(d)(e)(f) on the same frozen frames; **fine-grained
speaker-identity is recovered only by (a) or (c)** — no pooling/layer/readout choice on an ASR-aligned
pooled vector surfaces it (convergent across our anchor, Modality-Collapse, PCLM, ECAPA-LLM).

**Synergy with our D3 (the missing ablation).** The two dedicated layer-wise omni studies [2603.11947,
2602.23136] use **mean pooling only and run no mean-vs-stats-vs-attentive ablation** — exactly the gap
D3 fills. Our result agrees with the C2 picture: a single-vector attentive/stats pool gives only a
*modest, seed-sensitive* emotion gain (+0.04–0.11) while speaker stays floored — consistent with "the big
emotion lever is **ordered-trajectory / multi-vector** readout, not a smarter single vector" (C-Gate
+61pp ≫ our +0.04–0.11). I.e. **one pooled vector structurally caps emotion**; the large win needs a
multi-vector / late-interaction readout. (Provenance: 11 verified survivor claims; full ledger + 62-source
pool archived in the run transcript `wf_6694eca5-de9`.)

## 4. Verdicts on C1–C5 (rolling)

| sub-claim | verdict | basis |
|---|---|---|
| C2 pooling method | **holds (refined, hedged)** — uniform mean is the loss; attentive mid-layer best for *emotion* (modest, seed-sensitive); std/stats don't help | D3 ✅ |
| C3 suppressed vs destroyed | **holds, per-factor (both seeds)** — emotion suppressed-but-recoverable; speaker destroyed | D3 ✅ |
| C1 training objective | **partially holds (med)** — direction yes (content↑ speaker↓; CLAP>ASR; SSL baselines retain emotion/speaker); loss is at the **readout**, not a uniform representational reduction; strict same-audio SSL contrast unrun | D2 ◐ |
| C4 monotonicity | **partially holds (low)** — encoder-objective gradient real; no controlled cross-paradigm curve; "blanket tracks alignment" overstated | D2 ◐ |
| C5 fixes | **holds (high)** — 6 mechanism classes quantified; emotion recoverable broadly, fine speaker-ID **only** via external encoder (a) / disentangled codec (c) | D2 ◐ |

## 5. Implication for W4 (D1+D2+D3 converged)

The three legs agree and **sharpen the per-factor operator routing**:

- **Emotion → Operator A is viable, but NOT via the current single mean vector.** D3 shows a weight-free
  *attentive mid-layer* pool moves emotion modestly (0.40 → ~0.45–0.51); D2 explains why the ceiling is
  there — the single masked-mean vector is near-degenerate (per-frame outputs sit within cos~0.98 of the
  LLM mean token), so the *big* emotion lever is an **ordered-trajectory / multi-vector / late-interaction
  readout** (C-Gate 16.8→77.7%), plus layer selection (live signal in layers 0–14) and generative
  readout — all W1-pattern-compatible (best-of-N / reranking / probe-selection). **Tension to resolve:**
  a single retrieval vector and emotion-trajectory preservation conflict; W4 likely needs a multi-vector
  / per-factor pooled head rather than forcing one vector to carry content+emotion+speaker.
- **Speaker → the hard wall, and the natural boundary of the training-free thesis.** The anchor ~0.04 is
  the *expected* result, not a bug: convergent evidence (Modality-Collapse pooling ±2.1%, PCLM speaker
  stuck 30–37%, our 37-layer × 4-pooling sweep at the floor) says **no** pooling/layer/readout choice on
  an ASR-aligned pooled vector surfaces fine-grained speaker-ID. The speaker subspace is ~orthogonal to
  content (|cos|~0.13, matching [2305.12464]) so the geometry is favorable, but the objective never wrote
  a usable speaker direction. The only working levers are **not** training-free: fuse an external speaker
  encoder (ECAPA-LLM 1.03% EER) or a disentangled codec — or take the **W1→W4 RL bridge** (a light
  RL/adapter rewarding use of the orthogonal speaker subspace; PALLM-style multi-task RL is proposed-only
  and is the highest-value unmeasured fix for our own thesis).
- **Net correction to the framing:** "lost at pooling" is the right diagnosis for **emotion** (fix the
  pool/readout) and the wrong one for **speaker** (fix the source/encoder). This updates [[Per-Work-Status]]
  emotion from "Operator B or accept ~0.40" toward "**Operator A with a richer readout** (multi-vector /
  trajectory / layer / generative) before B"; speaker stays **Operator B / external-channel**.

**Concrete next experiments (from D2 residual unknowns):** (1) the strict **same-audio SSL baseline** —
emotion2vec / WavLM / ECAPA probed on the *same* CREMA-D split as the omni vector (settles C1 head-to-head,
a natural W4 baseline); (2) a **multi-vector / ordered-trajectory** emotion readout vs the single pooled
vector; (3) **emotion2vec-fusion** as the emotion analogue of ECAPA-LLM; (4) the **RL-on-speaker** bridge.

---

## 中文

冻结 omni 模型如何「注入/读出」语音表征，以及文本对齐+池化是否压制说话人/情感——回答 ICL 结论
（模型过度关注语音/内容流、忽略文本指令）背后的两个问题。配套 [[Omni-Embed-Model-Dossier]]、
[[W4-Training-Free-RL-Feasibility]]、[[2026-06-23-omni-embed-speech-disentanglement-1.2.1]]。

**§0 五个可证伪子命题：** C1 训练目标（ASR/对比对齐降低末层情感/说话人线性可解码信息，对照声学
SSL）；C2 池化方法（均值池化本身是丢失项，更好的池化能在同一批帧上找回）；C3 压制 vs 销毁（中层在
场、末层衰减=可恢复 ↔ 全程缺失=销毁，逐因子不同）；C4 单调性（随对齐强度变化）；C5 修复（哪些方法、
靠什么机制）。C2/C3 由自有探针（D3）裁定，C1/C4/C5 由文献综述（D2，进行中）裁定。

**§1 注入形态（Q1，已自验证）：** 两个阶段两种表征——**注入进模型 = 排列的 N 个音频 token 向量**
（实测 3.37s 片段 = 51 个连续 `<|AUDIO|>`，BOS/EOS 包裹，与文本交错进同一条双向 Thinker 序列）；
**读出 = pooled 1 维向量**（masked-mean→L2→2048 维；37 个 hidden states；手动末层均值 vs
`encode_document` 余弦 0.879，缺 `passage:` 前缀，与 Dossier 记录一致）。**对「情感/说话人只能给 1
维、否则干扰太多」的批判性回答：在本模型上直觉是反的**——pooled 1 维末层正是说话人/情感被销毁最狠
处（均值让内容方差主导）；真正杠杆是**池化方法 × 取层 × 来源**而非维度；1 维若是**中层 attentive-
统计池化**则能把情感从 0.40 拉到 0.51；生成式读出则应喂**完整 N 序列**让 LM 注意到副语言显著帧——
要修的「干扰」是均值里的内容主导，解法是**更聪明的降维**（注意力/二阶统计/中层），不是**更粗暴的**。

**§2 池化方法探针（D3，自验证）：** 冻结 omni-embed，CREMA-D 同音频三因子，dev600/test300，seed42，
kNN(k=5)，bootstrap CI，**免权重**。均值=std=stats（CI 重叠，二阶统计单独救不回）；**attentive-统计
池化在中层 L16 给出最佳情感读出**（seed42=0.513 `[.460,.570]`、seed7=0.447 `[.393,.500]`，均高于均值
0.40/0.407；同层内容 0.99→~0.27，即注意力把帧重加权到副语言显著处）；增益**温和且 seed 敏感**（seed42
CI 分离、seed7 CI 重叠）；**说话人全方法全层 ≤0.067（两 seed 一致）**，基本销毁。**C2 修正成立但需打
折**（损失项是*均值*，attentive 中层是最佳免权重杠杆，但只对情感、且温和）；**C3 逐因子稳健成立（两
seed）**（情感=被压制可部分恢复 ~0.45–0.51；说话人=销毁）。MLflow `2c61b2f1`(seed42)/`21453cb1`(seed7)。
注意：单数据集、n=300、免权重探针、attn 以均值为无参 query；情感增益仅一个 seed CI 分离，需 MELD/多
seed + 可学习 query 复现。**稳健结论=逐因子分裂（情感可恢复、说话人销毁）。**

**§3 文献综述（D2，77-agent workflow，3 票对抗核验；62→11 条存活）：** **结论=你的论断方向对、机制太
强、且强烈逐因子。** 副语言主要在「pooled 向量 + 解码读出」阶段被**压制/未读出**，而非「池化丢失」或
「销毁」。**C1 部分成立(中)**：方向有据（过 LLM 栈内容 +92~95%、说话人 −8~−39%；CLAP 对比保留 vs ASR
退化；SSL 基线即便末层仍线性可解码 emotion/speaker，emotion2vec IEMOCAP ~71.8%）[2602.23136, 2605.27772,
2501.05310, 2312.15185, 2111.02735, 2510.10444]，但无 omni 论文做严格同音频同探针 SSL 对照，且丢失集中
在**读出**层（末层探针仍 3–55× chance）。**C4 部分成立(低)**：编码器目标梯度真实（CLAP>ASR；Step-Audio2
多任务居顶）但无受控跨范式曲线、同层两个生成式 LALM 压制相同——拼凑而非单调测得。**C5 成立(高)**：六类
修复均有量化，且情感可恢复 / 细粒度说话人难恢复的不对称一致：(a) 外接说话人/副语言编码器=**唯一**能救
细粒度说话人（ECAPA-LLM **1.03% EER**）；(b) 池化修复(有序轨迹/attentive/层混)=**情感**（C-Gate
16.8→77.7%，+61pp）；(c) 解耦 codec（FACodec/SKQ3+/Eta-WavLM）；(d) 辅助/多任务（PE-FT+ADCH 情感
74.5–80.5%、强制选择 LoRA CREMA-D 情感 17.3→61.8% 而说话人不动；PALLM 多任务 RL）；(e) 副语言 adapter；
(f) 生成/探针读出（情感 75–93%，说话人仅**存在性**非身份）。**与 D3 的协同：文献两篇逐层 omni 研究只用
均值池化、从不做 mean/stats/attentive 消融——这正是 D3 填的空白**，且结论一致（单向量 attentive 仅温和
提升情感、说话人到底；大杠杆是有序轨迹/多向量读出）。

**§5 对 W4 的含义（D1+D2+D3 收敛）：** **情感→Operator A 可行，但不能靠当前单一均值向量**（均值向量近
退化：逐帧 cos~0.98 于 LLM mean token）——大杠杆是**有序轨迹/多向量/late-interaction 读出**（C-Gate）+
层选择（0–14 层）+ 生成读出，均 W1 兼容；张力：单检索向量与情感轨迹保留冲突，W4 或需多向量/逐因子池化
头。**说话人→硬墙、训练自由命题的天然边界**：~0.04 是预期；任何免权重池化/层/读出都救不回细粒度身份；
说话人子空间与内容近正交（|cos|~0.13，[2305.12464]）但目标从未写出可用说话人方向；可行杠杆**非训练自由**
（外接 ECAPA / 解耦 codec），或走 **W1→W4 RL 桥**（轻量 RL/adapter 奖励使用正交说话人子空间）。**框架修
正：「池化丢失」对情感对（修池化/读出）、对说话人错（修来源/编码器）。** 据此把 [[Per-Work-Status]] 情感
由「Operator B 或接受 ~0.40」改为「**先 Operator A 富读出**（多向量/轨迹/层/生成）再 B」；说话人仍 B/外接
通道。**下一步实验**：①同音频 SSL 基线（emotion2vec/WavLM/ECAPA 同 CREMA-D split）②多向量/轨迹情感读出
③emotion2vec 融合 ④RL-on-speaker 桥。
