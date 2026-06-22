# Decision Log

> Append-only, lightweight ADRs — the team's durable **memory**. Newest on top. One entry per
> decision: date · what we decided · why · consequences. Humans and AIs both append here (see
> [[AI-Collaboration]]), then publish with `scripts/wiki-sync.sh`.

---

### 2026-06-22 · F.1 finding (PROVISIONAL) — single-instruction + layer/pooling don't recover speaker; ICL untested
**Decision.** From the CREMA-D layer/pooling sweep (weight-free Operator A, *single-instruction*
conditioning): **speaker stays at chance (~0.03) across all 37 Thinker layers AND audio-token pooling**;
**emotion plateaus at ~0.40**. **Important correction (per review):** this is a *weak* intervention —
it does not exploit the model's strongest weight-free lever, **in-context learning / activation heads**
(native text-query cross-modal retrieval, few-shot demonstrations with target-token pooling, rich
activation prompts). So the negative falsifies only "single-instruction + architectural axes," **not**
"training-free activation." The earlier "speaker/emotion are Operator-B-mandatory" claim is **withdrawn
and downgraded to provisional (A(ICL)→B)**, pending experiment 1.2. content remains a clean Operator-A
win (~1.0). See report `2026-06-22-omni-embed-speech-disentanglement-1.1.1` and
[[W4-Training-Free-RL-Feasibility]] §0.1.
**Why.** A single short instruction has little leverage over ~50 content-oriented audio tokens under
mean pooling, and the model was contrastively trained with only `query:`/`passage:` prompts (weak
instruction-following) — but its Qwen2.5-Omni backbone has strong ICL, which reshapes the actual
forward pass and was not tested. Whether ICL survived the retrieval LoRA tuning is an empirical
question, not an assumption.
**Consequences.** Next: **experiment 1.2** — activation heads / ICL (text-query zero-shot + few-shot
with target-token pooling) for speaker/emotion BEFORE any Operator-B claim; then Operator B only for
factors that stay flat under ICL; then content/language fan-out. New W4 code so far: `layer_probe.py`
(mid-layer / audio-token pooling) + `scripts/layer_sweep.py`, `scripts/audio_pool_probe.py`.

### 2026-06-22 · W4 per-factor operator decision (from the algorithm-survey workflow)
**Decision.** Use **Operator A** (embedding-layer inference-time search: instruction/pooling/layer/
projector + verifiable-reward argmax) for **content** and **language**; **Operator B** (generative
Qwen2.5-Omni best-of-N/MBR, frozen weights, GRPO update dropped) for **emotion**; **hybrid** for
**speaker** (A's layer/pooling/LEACE-RLACE projector search, with B readout if the recovered probe
margin is too low). Any consensus/B path must gate the per-class plurality separatrix on a held-out
calibration set; prefer verifiable rewards over majority-vote pseudo-rewards everywhere a ground-truth
signal exists. Full analysis + sources: [[W4-Training-Free-RL-Feasibility]] §0/§4/§5.
**Why.** A multi-agent survey (11 agents, arXiv-cited, mostly self-verified) established: (a) Operator
A has real inference-time DoF on a vector-output model (instruction deltas up to ~55pp; closed-form
LEACE/RLACE/whitening projections); (b) the binding risk is weak steerability, fixed by reward-guided
selection; (c) omni-embed-nemotron-3b's Whisper-ASR backbone + contrastive mean-pooling **suppress
speaker/emotion** in the pooled vector (raw emotion probe ~31%), so those factors need layer/pooling
recovery or the generative readout; (d) consensus pseudo-rewards are Condorcet-fragile on near-chance
paralinguistic factors.
**Consequences.** The CREMA-D proof (E.4) tests the falsifiable cross-probe inequality
`A_t(e_t) > A_t(e_{t'})` per factor with non-target factors held fixed; a flat row for emotion/speaker
is a valid negative result (factor below the frozen model's separatrix), not a failure. The W4
`rl/embed_search` config implements Operator A first; Operator B is a future switch behind the same
interface.

### 2026-06-22 · Re-center the umbrella on training-free knowledge activation; W4 becomes flagship
**Decision.** Frame the whole series around one thesis: use training-free RL (no weight or structure
change) to *activate* the cross-modal, multi-granularity task knowledge an omni/multimodal LLM absorbed
in pretraining, lifting out-of-box performance on speech tasks. Promote **W4** (omni-embedding speech
disentanglement) to the flagship first work; keep **W1** as the mature training-free *pattern* reference
whose reward/eval machinery W4 reuses. No git repo or package is renamed — repositioning is by docs,
ordering, and a Role column. The flagship's first proof runs on CREMA-D (speaker + emotion on the same
audio). See [[Project-Thesis]] and [[W4-Training-Free-RL-Feasibility]].
**Why.** The docs stated the series only generically; the real thesis was unwritten, "disentanglement"
appeared nowhere, and omni-embed was listed as an asset with no motivation. Disentangling a frozen omni
model purely by reward activation is the strongest, most novel claim, and W1's existing training-free
machinery is exactly the shared foundation it needs.
**Consequences.** New canonical page `wiki/Project-Thesis.md`; four-work table reordered W4-first with a
Role column across README(_CN)/CLAUDE/AGENTS/docs/wiki; `common/` gains an omni-embedding loader +
embedding/probe/disentanglement reward & metric modules + an eval/probing harness (lazy imports
preserved); registry adds VoxCeleb/MELD/CREMA-D/CoVoST2/FLEURS/MINDS14/SLURP. The earlier "W1 first"
seed decision is superseded (W1 stays the pattern reference). W4-specific code/configs/README live in
W4's own repo.

### 2026-06-22 · Establish the README + Wiki knowledge base
**Decision.** Make the root README the single canonical onboarding doc (English `README.md` + 中文
`README_CN.md`), and stand up this Wiki (sourced from `wiki/`, synced by `scripts/wiki-sync.sh`) as
shared team memory. Sync `CLAUDE.md`/`AGENTS.md` to point here.
**Why.** Knowledge was scattered across per-tool files and people's heads; humans and their AIs need
one consistent understanding.
**Consequences.** Edit wiki content in `wiki/`, not the web Wiki; record notable decisions here.

### (template) · <short title>
**Decision.** …  **Why.** …  **Consequences.** …

---

## Seed decisions (context already baked into the repo)

- **WSL2-only compute.** RTX 5090 (Blackwell sm_120) lacks stable native-Windows torch wheels;
  verl/vLLM/flash-attn are Linux-only. All training runs in WSL2.
- **Python pinned to 3.12.** System Python 3.14 is too new for ML wheels.
- **Four separate work repos under one umbrella.** Independent history/issues per work, shared code
  via editable `common/`. Keeps each paper's repo publishable on its own.
- **Data never in git.** ~281 GB lives in `speechrl-data/` (WSL ext4); `.gitignore` guards it.
- **verl for RL; Qwen2-Audio as default base** (swappable via `models/` + config).
- **W1 first.** Training-free RL is the most mature work and the reference pattern for W2–W4.
  *(Superseded 2026-06-22: W4 is now the flagship first study; W1 remains the training-free pattern reference.)*

---

## 中文

> 追加式的轻量 ADR——团队的持久**记忆**。最新在最上。每条：日期 · 决定了什么 · 为什么 · 影响。人和 AI
> 都往这里追加（见 [[AI-Collaboration]]），再用 `scripts/wiki-sync.sh` 发布。

**条目格式：** 日期 · 标题；**决定**……**为什么**……**影响**……（英文区已有 2026-06-22 的两条与模板）。

**2026-06-22 · 把系列重定到「免训练知识激活」主旨，W4 升为旗舰：** 全系列围绕一个主旨——用免训练 RL
（不改权重/结构）激活 omni/多模态 LLM 预训练中习得的跨模态多粒度任务知识，提升语音任务开箱表现。把
**W4**（omni 嵌入语音解耦）升为旗舰首发工作，**W1** 保持为成熟的免训练「范式」参考、其奖励/评测机制被
W4 复用；不改任何仓/包名，仅靠文档、排序与「角色」列重定位；首个验证在 CREMA-D（同音频的说话人+情感）。
下方「先做 W1」的初始决策被本条取代。详见 [[Project-Thesis]]。

**已固化在仓库里的初始决策：** 仅用 WSL2 算力（RTX 5090 无稳定原生 Windows torch；verl/vLLM 仅 Linux）；
Python 锁 3.12（系统 3.14 太新）；一个伞仓下四个独立工作仓库（各自历史/issue，靠可编辑 `common/` 共享
代码）；数据绝不进 git（≈281 GB 在 `speechrl-data/`，`.gitignore` 兜底）；RL 用 verl、基座默认
Qwen2-Audio（可换）；**先做 W1**（免训练 RL 最成熟，是 W2–W4 的参考范式）。
