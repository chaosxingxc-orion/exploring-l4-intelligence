# W4 — Research Plan & Technical Scheme

The durable, team-visible plan for the flagship study. Pairs with [[Project-Thesis]] (the *why*) and
[[W4-Training-Free-RL-Feasibility]] (the *math*). This page is the *how*: the technical scheme and the
wave-by-wave execution plan, each wave with a verification **gate** and a **commit route**. Status is
mirrored on [[Per-Work-Status]]; decisions on [[Decision-Log]].

## Goal

Show that **training-free RL** (frozen weights, no structure change; reward-guided inference-time
optimization) can **disentangle** a frozen omni-embedding model's representation: different
task-conditioned embeddings of the *same* audio give different, individually-better downstream
performance across content/ASR+ST, speaker-ID, emotion/SER, language+intent.

## Technical scheme

- **Backbone (frozen):** `omni-embed-nemotron-3b` — a SentenceTransformer (`Transformer → mean Pooling
  → L2 Normalize`, dim 2048, cosine) built on the Qwen2.5-Omni Thinker; ~4.7B. Loaded via
  `speechrl_common.models.omni_embed.load_omni_embedder` (frozen, `eval`, no grad; flash-attn → sdpa
  fallback for Blackwell sm_120). API: `encode_document([{ "text": instruction, "audio": wav_1d_16k }])
  → (N, 2048)`. The **task-conditioning hook** is the `text` instruction paired with the audio.
- **Operators (decided per factor by the survey + pilot):**
  - **A — embedding-layer inference-time search:** optimize a search distribution over conditioning /
    pooling / inference-time linear-subspace projection / candidate selection; reward = verifiable
    downstream signal (retrieval hit@k via `rl.embedding_metrics`, probe accuracy via `rl.probe`). No
    weight update. *Novel.*
  - **B — generative-omni-end search:** best-of-N / MBR / reward-guided decoding on a generative omni
    model, then export an embedding. *Reuses existing math; for factors the embedder suppresses.*
- **Verifiable rewards/metrics (in `common/`, lazy-imported):** `rl.reward` (WER/ASR/exact-match),
  `rl.embedding_metrics` (recall@k / MRR / retrieval), `rl.probe` (linear/kNN accuracy),
  `rl.disentanglement` (separation / silhouette / cross-axis leakage), `rl.metrics`
  (accuracy / macro-F1 / BLEU / chrF / EER). All label-derived (verifiable), never model-judged.
- **Eval harness:** `speechrl_common.eval.probing` (build embedding matrix → probe/retrieval →
  task×conditioning matrix). Proof artifact = a **diagonal-dominant conditioning×probe accuracy
  matrix** with seeded bootstrap CIs.
- **First-proof substrate:** **CREMA-D** — two orthogonal verifiable factors on the same audio
  (6 balanced emotions from the filename code; 91 speakers from the filename prefix). VoxCeleb is gated
  /not-downloaded, so speaker is proxied by CREMA-D for the proof.
- **Tracking / config / compute:** local MLflow file store; Hydra per work; WSL2 + RTX 5090, py3.12
  venv, torch cu128. The Operator-A embedding proof needs **no verl/vLLM**.

## Execution plan (waves)

Waves marked **[WF]** run via multi-agent `Workflow`; others are edit→test→commit (TDD where code is
involved). Each wave names a **gate** (how we know it works) and a **route** (which repo it commits to:
umbrella / W1 / W4 — the #1 routing rule).

| Wave | What | Gate | Route |
|---|---|---|---|
| **0.1** | Load + encode omni-embed in the venv; pin transformers/sentence-transformers; fa2→sdpa | prints `(1,2048)` query+doc embeddings + finite cosine | W4 (scratch) |
| **0.2** | Validate CREMA-D labels & split contract | ✅ emotion=filename code (balanced ~1000/class), speaker=prefix (91); CSV classname unreliable (54% neutral) | — |
| **A.1–A.3** | Thesis page; reposition four-work table (W4 flagship); data motivation + Decision-Log | ✅ CLAUDE↔AGENTS parity; thesis links resolve | umbrella |
| **B.1–B.8** | `common/` extensions (omni-embed loader, embedding/probe/disentanglement/metrics, eval harness, registry+prompts) | ✅ `pytest common/tests` 21 pass/1 skip pre-stack; lazy-import guard green | umbrella |
| **C.1** | W1 script hygiene (env-drive paths, drop `model_env/`) | ✅ `bash -n` clean; W1 status only intended | W1 |
| **D.1** | Feasibility formalism doc + claim schema | ✅ objective + tilting + inequality + P/L/S written | umbrella |
| **D.2** [WF] | Survey workflow (5 lanes → adversarial verify → synth) | every claim tagged + ≥1 source; survey table filled | umbrella |
| **D.3** | Per-factor operator decision + Decision-Log | explicit A/B/hybrid per factor with evidence | umbrella |
| **E.1–E.3** | W4 configs (omni_embed/cremad/embed_search/experiment); data_cremad + conditioning + probes; eval harness + real `main.py` | composed config prints; split determinism test; dry-run writes MLflow run | W4 |
| **E.4** | CREMA-D two-factor disentanglement proof run | `train.sh seed=42` logs speaker×emotion matrix + baseline-vs-guided Δ + CIs; `eval.sh` reproduces | W4 |
| **F.1–F.3** [WF] | Operator lock-in (speaker) → parallel fan-out (content/ASR, ST, language/intent) → aggregate four-family matrix | each family logs a conditioning×probe result; cross-family matrix published | W4 + umbrella |

## Dependencies

```
0.1 ─┐                          A (docs) ── independent
0.2 ─┘── gates ── E, F          B (common) ── gates ── E, F code
                                C (W1) ── independent
D.1 → D.2[WF] → D.3 ── gates ── F fan-out
B + 0.1 + 0.2 → E.1→E.2→E.3→E.4 ── gates ── F
```

## Commit routing

Umbrella PR (`docs/recenter-omni-flagship`): `common/` + tests, `docs/*`, `wiki/*`, root `*.md`,
feasibility + this plan. W1 PR (`chore/script-hygiene`): the four hygiene fixes only. W4 PR: configs +
`main.py` proof loop + W4 README reframe. `projects/*` is gitignored by the umbrella — never commit W4
files into the umbrella.

## Risks (and the wave that resolves each)

Model load / version / no-flash-attn on sm_120 → **0.1**. Factor suppression (retrieval embedder may
discard speaker/emotion) → **E.4 / D.2** (flat matrix ⇒ Operator B for that factor — a result, not a
failure). Steerability of conditioning → tested in 0.1/E.2. CREMA-D label mismatch → **0.2**. License:
NVIDIA OneWay Noncommercial + Qwen Research — research/eval only.

## Definition of done

1. `pytest common/tests` green pre-stack. 2. CLAUDE↔AGENTS parity; thesis + feasibility + this plan
publish via `wiki-sync.sh`. 3. Feasibility doc has per-claim tags + a per-factor operator decision.
4. `bash scripts/train.sh seed=42` logs the CREMA-D matrix + Δ + CIs; `eval.sh` reproduces. 5. Three
clean PRs (umbrella / W1 / W4), each only what it owns.

---

## 中文

旗舰工作的「研究计划 + 技术方案」团队留档。与 [[Project-Thesis]]（为什么）、
[[W4-Training-Free-RL-Feasibility]]（数学）配套；本页是「怎么做」：技术方案 + 逐波次（wave）执行计划，
每个波次都有验证关卡（gate）与提交去向（umbrella / W1 / W4，遵守头号路由规则）。状态镜像在
[[Per-Work-Status]]，决策在 [[Decision-Log]]。

**目标。** 证明免训练 RL（冻结权重、不改结构、奖励引导的推理时优化）能解耦一个冻结 omni 嵌入模型的表示：
同一段音频在不同任务条件下的嵌入，在内容/ASR+ST、说话人、情感/SER、语言+意图上产生不同且各自更优的下游表现。

**技术方案。** 底座（冻结）= `omni-embed-nemotron-3b`（SentenceTransformer：Transformer→均值池化→L2
归一化，2048 维，cosine；基于 Qwen2.5-Omni Thinker）。通过 `speechrl_common.models.omni_embed` 加载
（冻结、eval、无梯度；flash-attn 在 sm_120 上回退 sdpa）；调用
`encode_document([{"text":指令,"audio":16k波形}])→(N,2048)`，**任务条件化钩子＝随音频附带的 text 指令**。
**算子**（由综述+试点逐因子决定）：A＝嵌入层推理时搜索（条件化/池化/子空间投影/候选选择，奖励=可验证下游
信号，不改权重，新颖）；B＝生成式 omni 端搜索（best-of-N/MBR/奖励引导解码后导出嵌入，复用现成数学，
用于被压制的因子）。**可验证奖励/指标**集中在 `common/`（惰性导入）。**评测**＝`eval.probing` 产出
条件×探针准确率矩阵（对角占优即解耦成立）。**首验证底座＝CREMA-D**（同音频双因子：文件名情感码 6 类均衡、
文件名前缀 91 说话人；VoxCeleb 受限未下载，说话人用 CREMA-D 代理）。算力 WSL2 + RTX 5090 + cu128；
A 类嵌入验证**无需 verl/vLLM**。

**执行波次、依赖图、提交路由、风险、完成定义**见英文区表格与列表（不重复）。要点：每波次都有 gate 与提交
去向；umbrella 负责 `common/`+`docs/`+`wiki/`+根 `*.md`，W1 只收脚本清理，W4 收配置+证明闭环+README；
`projects/*` 被 umbrella gitignore，W4 文件绝不进 umbrella。
