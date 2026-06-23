# Decision Log

> Append-only, lightweight ADRs — the team's durable **memory**. Newest on top. One entry per
> decision: date · what we decided · why · consequences. Humans and AIs both append here (see
> [[AI-Collaboration]]), then publish with `scripts/wiki-sync.sh`.

---

### 2026-06-23 · Pivot toward semantic tasks (omni-embed is semantic-specialized) + public dataset catalog
**Decision.** The flagship omni-**embedding** (`omni-embed-nemotron-3b`, contrastive InfoNCE bi-encoder →
one pooled 2048-d vector) is **semantically specialized** (content ≈1.00, language/intent strong, emotion
≈0.40, speaker ≈0.04), so we lean onto the semantic axis it is *measured*-strong on: **SLU / Spoken-QA /
Speech-Translation / speech-agentic**, and curate a verified public dataset set for it (new
[[Speech-Semantic-Task-Datasets]]). Adversarial caveats kept on the record: "only semantic" overstates
(partial emotion retained); the verdict is scoped to the embedding/retrieval class, **not** generative
omni; this is *complementary* to the disentanglement thesis (content/language were always Operator-A
native), not a reversal. OPEN: full pivot vs. a second track (affects breadth-vs-Spoken-QA-depth in the
starter set).
**Why.** [[Paralinguistic-Suppression-Survey]] established that fine speaker-ID is destroyed and emotion
only partially recoverable in the pooled vector; the high-fidelity, native axis is semantic. Playing to
that measured strength is the highest-confidence near-term use of the frozen embedding.
**Consequences.** New [[Speech-Semantic-Task-Datasets]] (16 core datasets across 4 families;
adversarially link-checked — **0 hallucinated, 0 gated**; license/source flags recorded). New umbrella
scripts `scripts/data/fetch-semantic-modelscope.sh` + `fetch-semantic-manual.sh` (`--list`/`--dry-run`,
user runs them). **ModelScope reality (web-verified):** only VoiceBench (`lmms-lab/voicebench`) + FLEURS
(`pengzhendong/fleurs`, already local) are on ModelScope; everything else goes via hf-mirror or direct
(SLURP→Zenodo 4274930, STOP→dl.fbaipublicfiles.com/stop). Minimal starter = VoiceBench + HeySQuAD (2 new
fetches; CoVoST2/FLEURS/MINDS-14 already local). Next: a semantic-eval harness (retrieval/probe +
generative readout) on the starter set — the positive complement to the survey's speaker/emotion negatives.

### 2026-06-23 · Paralinguistic-suppression survey (D2) + pooling-method probe (D3) — emotion routing upgraded to "Operator A with a richer readout"
**Decision.** Two converging results refine the per-factor routing. **(D3, own run)** a weight-free
pooling-METHOD sweep (`scripts/pool_method_probe.py` + `layer_probe.extract_pooled`; CREMA-D, seeds 42
& 7) shows **mean = std = stats** (no gain), while a **weight-free attentive-statistics pool at mid-layer
L16 modestly lifts emotion** (0.40 → 0.51 seed-42 CI-separated, → 0.45 seed-7 CIs overlap) and **speaker
stays floored (≤0.067) across every method × layer × seed**. **(D2, 77-agent 3-vote-verified survey,
`wf_6694eca5-de9`)** the assertion "omni models lose paralinguistics at pooling" is **right in direction,
too strong in mechanism, and sharply per-factor**: paralinguistics is **suppressed/unread at the
pooled-vector + decoder readout, not destroyed** (final-layer probes still 3–55× chance); the single
masked-mean vector is **near-degenerate** (per-frame outputs cos~0.98 to the LLM mean token), so the big
emotion lever is an **ordered-trajectory / multi-vector readout** (C-Gate 16.8→77.7%, +61pp) not a smarter
single vector; **fine-grained speaker-ID is never written to the output** and is recovered **only** by an
external speaker encoder (ECAPA-LLM 1.03% EER) or a disentangled codec — both non-training-free. Net:
**emotion → Operator A is viable but needs a richer readout (multi-vector/trajectory/layer/generative)
before B; speaker → Operator B / external-channel (the natural boundary of the training-free thesis).**
Full evidence + citations: [[Paralinguistic-Suppression-Survey]].
**Why.** D3 supplies the **mean-vs-stats-vs-attentive ablation the literature lacks** (the two dedicated
layer-wise omni studies use mean pooling only); its modest single-vector emotion gain + floored speaker
match D2's mechanism exactly. D2 corrects the earlier "emotion → B or accept ~0.40" by separating *info
present-but-unread* (emotion, fix the readout) from *info never written* (speaker, fix the source).
**Consequences.** New durable [[Paralinguistic-Suppression-Survey]] (D1 injection mechanism verified:
51-token sequence in, pooled 2048-d out; D2 C1–C5 verdicts + 6-class fix taxonomy; D3 table). New W4 code:
`layer_probe.extract_pooled` (mean/std/stats/attentive, weight-free) + `scripts/pool_method_probe.py`
(MLflow `2c61b2f1` seed42, `21453cb1` seed7). [[Per-Work-Status]] emotion verdict updated. Next
experiments: (1) strict same-audio SSL baseline (emotion2vec/WavLM/ECAPA on the CREMA-D split), (2) a
multi-vector / ordered-trajectory emotion readout, (3) emotion2vec-fusion (emotion analogue of ECAPA-LLM),
(4) the W1→W4 RL-on-speaker bridge (PALLM-style, proposed-only in the literature).

### 2026-06-23 · Model-understanding phase (1.2.1) — ICL tested; per-factor verdict now evidence-backed
**Decision.** After understanding the model thoroughly and **measuring in-context learning** (the lever
1.1.1 omitted), the per-factor operator decision is upgraded from provisional to evidence-backed:
**content → Operator A** (~1.0); **emotion → Operator B** or accept a ~0.40 ceiling; **speaker →
Operator B**; **language → provisional A** (mechanism validated, test on FLEURS). Few-shot is
structurally and mechanically supported but **not a useful label-conditioned activation lever** for the
suppressed factors. See [[Omni-Embed-Model-Dossier]] and [[2026-06-23-omni-embed-speech-disentanglement-1.2.1]].
**Why.** Probes (frozen, training-free) established: native text-query retrieval recovers content (0.99)
but not emotion (0.27 < 0.36 probe); in-context demos strongly move the query representation
(move=0.336) yet are label-insensitive (0.047) and **few-shot demos reduce emotion accuracy**
(0.217→0.150). So no weight-free Operator-A lever (instruction, layer, pooling, native retrieval, ICL)
exceeds ~0.40 for emotion, and speaker is ~chance across all 37 layers — the contrastive Whisper-ASR
backbone has discarded it. This is the rigorous version of the 1.1.1 conclusion (which was withdrawn for
not testing ICL).
**Consequences.** New durable [[Omni-Embed-Model-Dossier]] (architecture + I/O contract + token
mechanics + few-shot verdict). New W4 diagnostic code: `io_contract.py`, `icl_forward.py`,
`scripts/diag/*`; `embed_queries` in `common`. Next: 1.3 Operator B (generative `lm_head` readout) for
emotion/speaker; 1.4 content/language fan-out. Also fixed an infinite derangement-loop bug in the P7
control (had hung for hours) — model forwards are ~0.11s.

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
