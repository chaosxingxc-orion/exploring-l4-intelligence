# Omni-Embed-Nemotron-3B — Model Dossier

The durable, verified reference for the flagship backbone. Facts here were confirmed by reading the
checkpoint and by the diagnostic probes in [[2026-06-23-omni-embed-speech-disentanglement-1.2.1]].
Read this before writing any code that touches the model.

## 1. Architecture & provenance

`NVOmniEmbedModel` (`model_type: nvomniembed`) extends `Qwen2_5OmniThinkerForConditionalGeneration`.
~4.7B params, bf16, 2 safetensors shards (9.4 GB). Components: **Thinker text LLM** (36 layers, hidden
2048, 16 heads / 2 KV, intermediate 11008, RMSNorm, **32,768** context) + **Whisper-style audio
encoder** (32 layers, 128 mel, 16 kHz, output_dim 2048) + vision encoder. **Talker absent** (embedding
only) but **`lm_head` weight is present** (generation is latent — the substrate for Operator B).
Training: bi-encoder InfoNCE contrastive retrieval (NV-Retriever-style hard negatives), LoRA on the
LLM, frozen audio/vision encoders.

## 2. Pooling, normalization, the bidirectional twist

Pipeline (`modules.json`): **Transformer → masked-mean Pooling → L2 Normalize** → 2048-d cosine vector.
**Attention is made bidirectional** (`BidirectQwen2_5OmniThinkerTextModel` sets `is_causal=False` on
every layer + a `_prepare_4d_attention_mask` override) — so this is **not** a causal LM; ICL behavior
must be measured, not assumed. Pooling collapses the *entire* sequence (prompt + all demos + query)
into one vector → to read a specific clip under multi-audio input you must pool its token span (§5).

## 3. I/O contract — SentenceTransformer path (use this)

`model = SentenceTransformer(path, trust_remote_code=True, model_kwargs={"torch_dtype": torch.bfloat16,
"attn_implementation": "sdpa"}, device="cuda")` (flash-attn unavailable on sm_120 → **sdpa**). Prompts
auto-prepended: `query: ` / `passage: `; cosine similarity.
- **Text query:** `model.encode_query([str, ...]) → (N, 2048)`.
- **Single audio document:** `model.encode_document([{ "audio": wav_1d_16k[, "text": prompt] }, ...])`.
- **Multi-audio (few-shot) document:** one document = a **messages list**
  `[{"role":"user","content":[ {"type":"text","text":...} | {"type":"audio","audio":wav}, ... ]}]`,
  passed as `model.encode_document([ that_list ])`. Forms `{audio:[...]}`, `{message:...}`,
  `{content:...}` are **rejected**.
Helpers: `speechrl_common.models.omni_embed.{load_omni_embedder, embed_batch, embed_queries}`.

## 4. I/O contract — manual forward (for custom pooling)

To pool a custom token subset (e.g. query-only), forward the underlying model and pool yourself:
`feats = model[0].tokenize([doc]); auto = model[0].auto_model; out = auto(**{input_ids, attention_mask,
feature_attention_mask, input_features}, output_hidden_states=True)`. **Parity:** masked-mean of
`out.hidden_states[-1]` over `attention_mask` equals `encode_document` at **cosine 1.0000 only if the
document includes the `"passage: "` prompt** (omit it → 0.88). Helpers:
`omni_embedding_rl.icl_forward.{build_doc, query_embedding}`.

## 5. Audio-token layout

Per clip: `<|audio_bos|>=151647`, then a contiguous run of `<|AUDIO|>=151646` (~51 for a ~2.5–3.5 s
CREMA-D clip; the count is roughly fixed, not linear in duration), then `<|audio_eos|>=151648`. A
multi-audio input has one such run per clip. `omni_embedding_rl.io_contract.{audio_block_spans,
query_mask, n_audio_blocks}` locate runs and isolate the last (query) block. (Vision tokens: image
151655 / video 151656; bos/eos 151652/151653.)

## 6. Conditioning & in-context-learning effects (measured)

- **Instruction conditioning is a weak lever:** swapping the task instruction barely moves accuracy
  (1.1.1 flat columns) — expected for a retriever trained with only `query:`/`passage:`.
- **In-context demos strongly move the representation but are label-insensitive:** `move(no-demo →
  k=4-demo) = 0.336` on the query token, yet `label_sensitivity(correct → wrong labels) = 0.047`. The
  query in-context-attends to the demo **audio/context**, not the **labels**.
- **Few-shot does not help (hurts) factor classification:** emotion query-token probe no-demo 0.217 →
  k=4 demos 0.150 (Δ −0.067). See 1.2.1.

## 7. Generation latent (Operator B substrate)

`lm_head` is present (vocab 151,936 × 2048); generation is disabled by the embedding/contrastive
deployment but the Thinker can produce tokens — this is the substrate for Operator B (generative
best-of-N / MBR readout) for factors Operator A cannot recover.

## 8. Few-shot verdict & per-factor decision

**Does this generation support few-shot?** Structurally **yes**; mechanically **yes** (demos reshape
the query rep); but functionally, as a *label-conditioned activation lever for suppressed factors*,
**no** (label-insensitive; hurts emotion). **Per-factor (evidence-backed):** content → **Operator A**
(~1.0); emotion → **Operator B** or accept ~0.40 ceiling (no weight-free A lever, incl. ICL, exceeds
it); speaker → **Operator B** (absent from the representation across all 37 layers); language →
**provisional A** (mechanism validated, test on FLEURS). Full evidence:
[[2026-06-23-omni-embed-speech-disentanglement-1.2.1]] and [[W4-Training-Free-RL-Feasibility]].

---

## 中文

旗舰底座的长期、已验证参考。以下事实由通读 checkpoint + 诊断探针（见
[[2026-06-23-omni-embed-speech-disentanglement-1.2.1]]）确认。动模型相关代码前先读本页。

**架构（§1）：** `NVOmniEmbedModel` 继承 Qwen2.5-Omni Thinker；约 4.7B；Thinker 36 层/隐藏 2048/上下文
32768 + Whisper 音频编码器（32 层/128 mel/16kHz）+ 视觉编码器；Talker 无，但 **lm_head 在**（生成潜能 =
Operator B 基质）；双编码器 InfoNCE 对比检索 + LLM 上 LoRA。**§2 池化：** Transformer→均值池化→L2 归一化，
2048 维 cosine；**注意力被改为双向**（`is_causal=False`），故非因果 LM，ICL 须实测；池化把整条序列（前缀+所有
示范+query）压成一个向量，多音频下要读某条音频必须池化它的 token 区段（§5）。

**§3 I/O（ST 路径，推荐）：** sdpa（sm_120 无 flash-attn）；`encode_query([str])`；单音频
`encode_document([{audio:wav[,text:prompt]}])`；**多音频（few-shot）= 把一个 messages 列表当 document**：
`[{"role":"user","content":[文本/音频块...]}]`，其余形式被拒。**§4 手动前向（自定义池化）：** `tokenize`→
`auto_model(...,output_hidden_states=True)`→对 `hidden_states[-1]` 按 mask 均值；**仅当包含 "passage: "
前缀时**与 encode_document 完全一致（cosine 1.0000，否则 0.88）。**§5 音频 token：** `151647 <|AUDIO|>151646×~51
151648`，每条音频一段连续 run；`io_contract` 定位并隔离 query 块。

**§6 条件化与 ICL（实测）：** 指令是弱杠杆（1.1.1 各列近乎不变）；上下文示范强烈改变表示（move 0.34）但对
标签不敏感（0.047）——关注示范音频而非标签；few-shot 不仅没帮助反而降低情感准确率（0.217→0.150）。
**§7：** lm_head 在 = Operator B 基质。**§8 few-shot 结论与逐因子决策：** 结构支持、机制上有效、但作为「被压制
因子的标签条件化激活手段」无效；内容→A（~1.0），情感→B（或接受 ~0.40 上限），说话人→B（37 层全随机），语言
→暂定 A（待 FLEURS）。证据见 1.2.1 与 [[W4-Training-Free-RL-Feasibility]]。
