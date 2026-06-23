# 2026-06-23 · Omni-Embed Speech Disentanglement · Experiment 1.2.1 — Model understanding & few-shot/ICL

> Naming `yyyy-mm-dd-{purpose}-{a.b.c}`: **a=1** (training-free activation/disentanglement of the frozen
> omni-embedding), **b=2** (model-understanding / ICL probes on CREMA-D), **c=1**. Follows 1.1.1; the
> durable architecture reference is [[Omni-Embed-Model-Dossier]]. Purpose: *understand the model before
> running more experiments* (owner directive) and answer **"does this generation support few-shot?"**

## Question

After 1.1.1 found single-instruction conditioning + layer/pooling did not recover speaker/emotion, the
open question was whether the model's strongest weight-free lever — **in-context learning** — works
here, and what the exact I/O mechanics are. All probes are frozen-weights, training-free, MLflow
experiment `omni-embed-model-understanding`, seed 42, CREMA-D.

## Mechanics established (P0–P3)

- **Multi-audio input form (P0):** `encode_document([ doc ])` where a doc is a **messages list**
  `[{"role":"user","content":[ {"type":"text",...} | {"type":"audio","audio":wav}, ... ]}]`. The
  `{audio:[...]}`, `{message:...}`, `{content:...}` forms are rejected. Multiple audios in one doc →
  multiple audio blocks (verified: 2 demos + query → 3 blocks).
- **Token layout (P1):** one clip → exactly one `<|AUDIO|>` block of ~51 tokens (`<|audio_bos|>151647
  <|AUDIO|>151646×n <|audio_eos|>151648`); 12/12 consistent.
- **Query isolation (P2):** `audio_block_spans` finds N blocks; `query_mask(...,"last")` exactly
  isolates the query clip's tokens (the last block).
- **Forward parity (P3):** a manual `auto_model(..., output_hidden_states=True)` masked-mean of the
  final layer equals `encode_document` at **cosine 1.0000 iff the `"passage: "` document prompt is
  included** (without it, 0.88). This is the faithful recipe for query-token pooling.

## ICL diagnostics (P5, P7, P6)

**P5 — native text-query zero-shot retrieval** (classify audio doc by nearest label-text query;
test N=300):

| factor | accuracy | note |
|---|---|---|
| content (12 sentence-text queries) | **0.990** | positive control — the text-query mechanism works |
| emotion ("a {e} sounding voice") | 0.270 | best of 4 templates; "plain" = 0.173 ≈ chance |
| emotion (chance / 1.1.1 probe) | 0.167 / 0.360 | native retrieval is *below* the trained probe |
| speaker | N/A | text queries meaningless for 91 ids |

**P7 — ICL control** (does conditioning move the query embedding, and does it depend on demo *labels*?;
emotion, k=4, N=30): `move(no-demo → correct-demo) = 0.336`; `label_sensitivity(correct → wrong-label) =
0.047`. → Demonstrations **strongly** reshape the query-token representation (bidirectional attention
works), but the shift keys on the demo **audio/context**, only weakly on the **labels**.

**P6 — few-shot probe accuracy** (emotion, k=4, query-token pool, fit 60 / test 120): no-demo 0.217,
**k=4 demos 0.150 (Δ = −0.067, demos HURT)**, difference-vector 0.192.

## Answer: does this generation support few-shot?

- **Structurally: YES** — 36-layer **bidirectional** Thinker, 32k context, multi-audio chat template,
  `lm_head` present.
- **Mechanically: YES** — in-context demos measurably reshape the query representation (move 0.34).
- **Functionally (as a label-conditioned activation lever): NO, for the suppressed factors** — the
  representation is label-insensitive (0.047) and few-shot demos *reduce* emotion accuracy. The model
  in-context-attends to the demo audio, not to the task labels, so few-shot does not act as a useful
  classification-activation mechanism here. (Consistent with a contrastive, bidirectional, mean-pooled
  retriever rather than a causal LM.)

## Per-factor readout summary (all weight-free levers tried)

| factor | full-pool probe (1.1.1) | layer/pool best | native text-query | query-token pool | few-shot ICL k=4 | chance |
|---|---|---|---|---|---|---|
| content | ~1.00 | 0.99 | **0.99** | — | — | 0.083 |
| emotion | 0.36 | 0.40 (L0) | 0.27 | 0.217 | 0.150 (hurts) | 0.167 |
| speaker | ~0.04 | ~0.04 (all 37 L) | N/A | — | — | 0.011 |

## Conclusion (now evidence-backed, upgrading the 1.1.1 provisional)

- **content → Operator A** — fully exposed (~1.0), trivially activated; native text-query also ~0.99.
- **emotion → Operator B (or accept ~0.40 ceiling)** — no weight-free Operator-A lever (instruction,
  layer, pooling, native retrieval, **or ICL**) exceeds ~0.40; **ICL actively hurts**. The strongest
  lever has now been tested, so this is no longer provisional.
- **speaker → Operator B** — ~chance across all 37 layers + pooling; text-query N/A; ICL cannot add
  information that is absent. The contrastive Whisper-ASR backbone has discarded speaker identity.
- **language → provisional Operator A** — not on CREMA-D; the native text-query mechanism works
  (content control 0.99), so test on FLEURS in the fan-out.

## Limitations

ICL tested for emotion with one demo format (audio→label, query-token pool) and k≤4; the weak
label_sensitivity (0.047) bounds the upside, but other formats (label verbalization, ordering, larger
k, generative `lm_head` readout = Operator B) are untested. Speaker ICL needs an enrollment design
(demos of the candidate speakers), which reduces to audio-enrollment kNN (≈chance per 1.1.1). Single
dataset (CREMA-D, acted speech).

## Next

1.3 — Operator B (generative best-of-N / MBR via the live `lm_head`) for emotion & speaker. 1.4 —
content/language fan-out (LibriSpeech / CoVoST2 / FLEURS / MINDS14) where Operator A is expected to win.

---

## 中文

> 命名 `yyyy-mm-dd-{目的}-{a.b.c}`：a=1（冻结 omni 嵌入的免训练激活/解耦），b=2（CREMA-D 上的模型理解 /
> ICL 探针），c=1。承接 1.1.1；模型架构的长期参考见 [[Omni-Embed-Model-Dossier]]。目的：按 owner 要求
> **先把模型理解透彻再做实验**，并回答**「这一代模型是否支持 few-shot」**。

**机制（P0–P3）：** 多音频输入＝把一个 messages 列表作为 document 传给 `encode_document`（其他形式被拒）；
单条音频＝一个约 51 token 的 `<|AUDIO|>` 块；`query_mask` 可精确隔离最后一个块（query）；手动 `auto_model`
前向（末层 masked-mean）在**包含 "passage: " 文档前缀时**与 `encode_document` 完全一致（cosine 1.0000，否则
0.88）——这是 query-token 池化的可信配方。

**ICL 诊断：** P5 原生文本-query 零样本检索——内容（12 句子文本作 query）0.99（正对照，机制有效），情感最佳
0.27（< 0.36 探针，plain 0.17≈随机），说话人不适用。P7 控制（情感，k=4）——move(无示范→正确示范)=0.336（示范
确实强烈改变 query 表示，双向注意力有效），label_sensitivity(正确→错误标签)=0.047（很弱：模型关注示范音频而非
标签）。P6 few-shot 准确率（情感，k=4，query-token 池化）——无示范 0.217，k=4 示范 **0.150（Δ−0.067，示范反而
更差）**，差向量 0.192。

**结论——是否支持 few-shot：** 结构上支持（36 层双向 Thinker、32k 上下文、多音频模板、lm_head 在）；机制上
支持（示范确实改变 query 表示，move 0.34）；但**作为「标签条件化的激活手段」对被压制因子无效**——表示对标签
不敏感（0.047），few-shot 反而降低情感准确率。即模型会上下文关注示范的**音频**而非**标签**,故 few-shot 不能
当作有用的分类激活机制。逐因子结论（现已有 ICL 证据,升级 1.1.1 的暂定）：内容→A（~1.0）；情感→B（或接受
~0.40 上限），因为指令/层/池化/原生检索/ICL 都不超过 ~0.40 且 ICL 反伤；说话人→B（37 层全随机，表示中已无
说话人信息）；语言→暂定 A（机制有效，待 FLEURS 验证）。详见英文区表格与「Next」。
