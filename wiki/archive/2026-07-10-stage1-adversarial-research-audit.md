---
title: "Stage-1 对抗式研究审计：训练免费语音/Omni 推理优化的主张、证据与改进路线"
date: 2026-07-10
stage: 1-problem-definition-audit
status: "审计完成；owner decision pending；不自动推进 Stage 2"
scope: "umbrella + W1–W4 + proofs/tfrl + 当前 Step-1/2/3 实验战役"
---

# 2026-07-10 · Stage-1 对抗式研究审计

> **先给结论。** 这个工程的研究对象有价值，工程纪律也明显强于普通原型；但截至本审计，
> **W4 旗舰“任务条件化解耦”主张没有被当前实验支持，W1 只有 oracle candidate headroom、没有
> deployable selector gain，Step-2 Phase-A 也尚不可执行。** Lean 全库确实构建成功，但当前所谓
> “收敛”大多是对抽象序列施加结论本身所需前提，并未从实际 Python 更新算子推出。
>
> 建议不是删除既有工作，而是 **stop-the-line**：暂停新的 Phase-A/Step-3 GPU 批跑，先完成
> 本文 G0–G2。已完成的 Stage-1 数字继续作为 hypothesis-grade 方向性证据保留；不得升级为
> 解耦、部署改进或系统收敛的证据。

## 1. 我理解的工程：它实际在研究什么

项目北星是：冻结 speech/omni 模型的权重与结构，在推理时搜索 prompt、candidate、readout、
retrieval 或 selection，以可验证奖励激活预训练能力。

实际工作分成三条不同的科学对象，当前文档把它们写成了一条连续故事，但它们并不等价：

| 对象 | 当前载体 | 真正测到的东西 | 当前证据等级 |
|---|---|---|---|
| 冻结生成模型的 candidate support 与选择 | W1 | Qwen3-Omni ASR 的 N-sample pool 中存在更好答案；oracle WER headroom 随 N 增长 | **有效的 support/headroom 证据**；deployable MBR 为 null |
| 冻结 embedding 的因素可读性/任务选择性 | W4 | CREMA-D 12 句 ID 易读、emotion 部分可读、speaker 近 chance；instruction 行基本平坦 | **有效的 probing/negative 证据**；不是 task-conditioned disentanglement |
| 冻结 omni + speech-keyed KB 的 RAG/agentic 组织与 TFRL | 当前 W1 Step-2/3 | Step-1 baseline 已大规模铺开；Step-2 仍是部分 plan-only skeleton | **方案与基建阶段**；尚无可执行全网格或有效系统增益 |

W2/W3 仍是 LoRA/GRPO/DPO 与 multi-task RL skeleton。它们会更新参数，因此应作为核心
“no-weight-update”论题的 **trained comparison/upper bound**，不能与 W1/W4 共用同一个
“training-free”科学结论。

## 2. 审计方法与证据边界

### 2.1 本地证据

本审计逐项读取了：root/四个 work repo 的状态、Wiki 主张链、W1/W4 脚本与 committed artifacts、
Step-1/2 freeze 与 Decision Log、`proofs/tfrl` 全部关键定理。只读验证结果：

- `common`: **21 passed, 1 skipped**；
- W4: **31 passed, 4 skipped**；
- W1: venv 未 editable-install 时唯一 smoke test import 失败；`PYTHONPATH=src` 后 **1 passed**，
  根因是安装契约，不是包源码损坏；但 W1 也确实只有这一个版本号 import test；
- Lean: `lake build` **8574 jobs success**；全库 `sorry=0`，但有一个具名 axiom，见 §6。

### 2.2 论文 survey

当前 Codex 会话没有暴露仓库说明中所称的 `academic-research-skills` 技能条目；本机插件缓存也未
发现可调用包。因此没有伪称调用成功，而是使用已暴露的 `deep-research` + `tavily-research`
工作流，独立发起三条检索：

1. frozen-model test-time compute / best-of-N / MBR / verifier / reward overoptimization；
2. speech representation disentanglement / probing / layer-pooling / recoverability；
3. speech/audio/multimodal RAG 与 agentic attribution。

独立检索返回 **43 个不重复来源条目，其中 31 个是论文或官方技术报告**。此外，针对现有 survey
遗漏，单独核验了 Locatello、Hewitt–Liang、Voita–Titov、TRPO、reward-model overoptimization 等
基础文献。仓库自身的 07-09 survey 另有 81 + 92 条 claims，speech2vec survey 有 40 条承重核验；
本审计审的是它们的覆盖与验证协议，不假装逐篇重读了历史 171 篇参考文献。

### 2.3 对现有 survey 的质量审计

- Step-2a：81 claims，62 条 load-bearing，只验证 20 条，结果 **16 confirmed / 4 partial**；
- Step-3a：92 claims，64 条 load-bearing，只验证 20 条，结果 **12 confirmed / 8 partial**；
- 即便验证样本是最承重条目，partial 比例也分别为 20% 与 40%。这足以说明“20 条抽验后宣称
  exhaustive”不成立；其余承重 claim 必须继续验证。
- W4 主文献链在仓库全文搜索中没有 Locatello 的不可辨识性反例、Hewitt–Liang control task、
  Voita–Titov MDL probing，也几乎没有 probe capacity/selectivity 文献。这个遗漏正好会导致
  “probe 可读 = representation disentangled”的过度解释。

## 3. 对抗评审 Round 1：科学主张、可证伪性与因果解释

### R1-P0 · W4 的正式判据与“首结果证明 thesis”互相矛盾

W4 自己把可证伪条件写成：对同一音频生成 task-conditioned `e_t`，且 matched task probe
满足 `A_t(e_t) > A_t(e_t')`。但首结果的 condition × factor matrix 明确得到
`diagonal_dominant=False`，instruction 条件化列基本平坦。

随后文档用“同一个 frozen embedding 在 content≈1.0、emotion≈0.36、speaker≈0.04”声称
“thesis holds”。这只说明三个标签任务难度/可读性不同，**不说明不同 task conditioning 产生了
不同且 individually-better 的表示**。按本文建议的 claim ladder，它最多是 L0/L1，不是 L3：

| 层级 | 可声称内容 | 当前是否满足 |
|---|---|---|
| L0 · factor decodability | 某 probe 能从某层读出标签 | content/emotion 部分满足 |
| L1 · accessible readout | 低复杂度 probe 在 group-held-out 上稳定 | 尚未严格满足 |
| L2 · task selectivity | matched conditioning 比所有 mismatched conditioning 好 | **当前否** |
| L3 · disentanglement | target 增、nuisance leakage 降，并过 counterfactual intervention | **未测** |
| L4 · deployable activation | label-free per-instance selector 能实现稳定增益 | **未测** |

**裁定：** 当前 W4 主张应降级为“frozen omni embedding 的 factor availability / suppression /
selective-readout limits”。除非 L2–L3 通过，标题和摘要都不应使用 disentanglement。

### R1-P0 · 当前活跃工作偏离旗舰

W4 repo 最近实质提交停在 07-01；当前 GPU 与工程主力在 W1 的 76-dataset baseline、speech-keyed
KB、agentic mock 和 Step-3 selector。与此同时，Stage-1 07-04 已由 owner 选择 CP-1/3/8/4 进入
Stage-2，并明确要求每个问题创建 fresh Research-Proposal-Template；仓库没有找到这些 fresh
proposal，反而又开启一套标为 Stage-1 的三步大规模实验战役。

这形成四个同时移动的研究对象：W4 解耦、CP-1/3/8/4、07-06 GAP-4/5/7、07-09 knowledge-agentic
三步走。问题不是“方向太多”本身，而是每次新方向都复用前一轮 test、theory 和 headline，形成
移动靶与 HARKing 风险。

**裁定：** 必须由 owner 重新指定一个 primary paper question；其他方向降为 supporting control 或
独立 work，不得继续共享同一个旗舰主张。

### R1-P1 · oracle reward、offline model selection、deployable inference 被混成一个 operator

当前文档至少有三种行为：

1. 在 labeled dev 上全局选 instruction/layer/pooling；这是 **offline hyperparameter selection**；
2. 在 test candidate pool 上用 ground-truth WER/label 选最优；这是 **oracle upper bound**；
3. 用 MBR/confidence/cross-model verifier 在每个 test item 上 label-free 选择；这才是
   **deployable inference-time selector**。

三者的统计对象与部署含义不同。W1 ASR 的 oracle WER reduction +0.0418 是有效 headroom；但 MBR
reduction +0.0037，CI 跨 0。因此当前最诚实 headline 是：

> Frozen Qwen3-Omni pools contain exploitable ASR support, but the tested label-free selector realizes
> no statistically reliable fraction of it.

不能写成“deployment 已被 training-free RL 改善”。对 ASR，reference transcript 在部署时不存在。

### R1-P1 · CREMA-D 不是当前宏大 claim 的充分 substrate

- content label 是 **12 条固定句子的 sentence-ID**，不是 open-vocabulary ASR/ST；接近 1.0 很容易，
  不能外推为 content knowledge activation。
- emotion dev/test 允许同一 speaker、同一 sentence 跨 split；这会让 probe 利用 actor/channel/content
  shortcut。emotion 结论至少要 speaker-disjoint；content 结论至少要 speaker-disjoint 且改用真实
  transcript/WER。
- speaker closed-set SID 需要同一 speaker 有 enrollment/test，当前设计在这个任务上合理；但应报告
  EER/minDCF/retrieval，而不是只报告 91-way kNN accuracy。
- 五个 seed 的 300-item test slice 来自同一个 1489-item pool，pairwise overlap 为 16%–21%；把五个
  delta 当独立样本做 `n=5` t-CI 不严谨。

### R1-P1 · 单模型、专用 retrieval checkpoint 限制外推

`omni-embed-nemotron-3b` 不是未经任务化的原始 omni pretraining checkpoint，而是基于
Qwen2.5-Omni Thinker、经 bi-encoder contrastive retrieval 训练的专用模型；官方模型卡也明确其
research/non-commercial 限制。它适合做 case study，但不能单独证明“现代 omni LLM 普遍已具备
这些 latent factors”。必须同时测原始 omni hidden state 与至少一个不同谱系模型。

## 4. 对抗评审 Round 2：实验统计、泄漏、可复现性与工程可执行性

### R2-P0 · Step-2 Phase-A 当前不能开跑

Decision Log 最新条目写“工程前置 ①–⑤ 已全部完成，签字即可开跑；Phase-A 35 臂/140 格”。实际代码：

- `phase_a_cells.py --dry-run` 输出 **34 臂/136 格**、0 checkpoint，并明确没有 execute path；
- `run_mock.py` 把 ASR→text query、asymmetric query、HyDE、BM25+dense RRF、IRCoT、LLMLingua-2
  标成 `PLAN ONLY`，真实调用抛 `NotImplementedError`；
- `two-stage` 只是对同一个 index 再按同一个 similarity 截断，不是真正两级检索；
- `kb_batch_build.py` 只构建单 utterance audio-key + 单 value，未实现 multi-granularity、H-a/H-b、
  RAPTOR-lite 或 audio+text value；
- runner 的 source 命名是 `dataset__embedder__key_org__value_org`，builder 的 source 命名却是
  `dataset__embedder__pool_split`；
- run_mock 用 `qwen3-omni-hidden`，embed registry 用 `qwen3-omni-own`；
- `kb_retrieve._query_embedder` 对 GLAP/LCO/SENSE/MERaLiON 等新 embedder 回退到 `auto`，可能用 CLAP
  生成 query，而 index 是另一空间/另一维度；这不是可比较的 retrieval。

**裁定：** Phase-A 是 P0 工程阻塞。冻结过的 protocol 不能反过来把未实现 arm 变成“完成”。

### R2-P0 · 大规模选择将持续过拟合“test”

当前计划是 Phase-A 35 臂 × 4 dataset 的 dev 扫描，再取 top-1/top-2 组成 Phase-B，并在后续 Step-3
多轮 debate/verify/improve。即使 dev/test item-id 不重叠，许多数据只有一个官方 test pool，被拆成
内部 dev/test；它不是独立 benchmark test。反复用同一 test 决策会产生 reusable-holdout 失效。

此外：

- 35 arm × 4 dataset 的 winner selection 有明显 winner's curse；
- 当前没有 family-wise error/FDR 方案；
- one-factor-at-a-time 固定在一个 ref-config 会漏掉 key×retrieval、query×delivery 等交互；
- Phase-B 只验少量“赢家组合”不能证明全局优；
- n=40/60 的 bootstrap CI 只量化 sampling error，不修正 arm selection error。

**裁定：** Stage-1 可以保留方向性 mapping，但任何方法优越性必须在新建的 calibration/locked-test/
external-test 层重新建立。

### R2-P1 · 划分单位错误会制造伪增益

“item-id 不重叠”不等于独立：

- SER：按 speaker/session/dialogue group 划分；
- ASR/ST：按 speaker/book/recording family 划分，噪声增强版本必须同组；
- spoken QA：同一原始 text question 的 TTS/human/rephrased 版本同组；
- SLU：同一 template/intent surface form 或 speaker 同组；
- tool/agent：同一 scenario seed/template 同组。

统计 bootstrap 也必须以这些 cluster 为单位，而不是把所有 clip 当独立 Bernoulli。

### R2-P1 · W1 best-of-N 的指标与随机性仍需修复

有效部分：artifact 与 E-drive 原始 artifact SHA256 完全一致；144 utterances 无重复；oracle climb
确实存在。

未解决部分：

- 脚本报告的是 **per-utterance WER 的宏平均**，不是标准 corpus WER；二者都应报告；
- 三个“generation seed”同时改变 utterance sample 与 generation pool，无法分别估计 data variance 与
  generation variance；应在同一固定 utterance set 上重复 pool seed；
- pool=8 的平均 unique candidate 只有 **4.17**，14.6% utterance 的 8 个 candidate 完全相同；
  应报告 effective N/semantic diversity；
- 只对 greedy，没有 beam/diverse-beam、temperature/top-p sweep、ROVER、classical ASR LM/ensemble；
- llama.cpp audio 路径由上游标为 experimental，且仅 Q8_0 GGUF；至少要对一个小子集用官方
  runtime/BF16 或另一独立实现做 parity check。

### R2-P1 · 指标 bug 不是偶发，而是测试体系不足

Wave-1 的 60 格 MCQ gold 解析错误、Wave-2 的 12 格 K4/K7 metric wiring 错误都被后续审计抓到，
且坏格没有静默伪造数字——这是优点。但 W1 只有一个 import test，也解释了为什么 schema 漂移只有在
跑完大网格后才暴露。

必须把每次审计发现转成 fixture/golden/property test，而不是继续依赖每波人工抽验。

### R2-P1 · artifact provenance 不完整

Step-1 JSON 有 command、model 描述与 per-item，但普遍缺：代码 git SHA、dirty flag、模型文件 hash、
llama.cpp build SHA、dataset revision/hash、manifest hash、环境 lock hash。W4 MInDS committed summary
也不是 reproducer 直接写出的文件；脚本只在 data root 写中间报告，repo JSON 是另行整理。

**裁定：** 以后 committed summary 必须由同一脚本原子写出；禁止手工转录 headline 数字。

### R2-P1 · KB leakage guard 仍有语义与同项泄漏盲区

当前 guard 主要做 normalized exact substring；它不能发现 paraphrase/entailment 泄漏。更关键的是，
`kb_batch_build.build_one` 用 **build rows 自己的 gold** 审计 source，而不是传入 future eval rows 的
gold；runner 也没有按 `from_item_id` 自动排除 own item。必须把 source-pool 与 eval-pool 的结构分离
写成机器不变量，并增加 semantic entailment/embedding overlap 的辅助审计。

## 5. 对抗评审 Round 3：理论、术语与新颖性

### R3-P0 · Lean “构建成功”不等于“系统收敛已证明”

Lean build 成功是真事实；当前定理的 scope 也必须照实写：

- `Iterate.monotone_bounded_converges`：假设序列单调且有界，推出收敛；
- `improve_budget`：假设每步至少增益 `δ>0` 且终值有界，推出步数上界；
- `Realization.realized_tendsto_oracle`：假设 uniform reward-estimation error `τ_n→0`，推出
  oracle gap→0；
- `BestOfNConvergence` 同样把 `τ_n→0` 当外部前提；
- `MBR.mbr_consistency` 只证明 **固定 candidate** 的 sample mean 收敛，不证明对候选 argmin 的一致性，
  更不覆盖随 N 增长的 candidate set；
- `Reachability` 是 reweighting ratio 的代数等价式，没有从实际 prompt operator 导出 reach bound。

尤其值得纠正：KL trust region 是步长/分布漂移的 **上界**，不能“等价地给出每步正增益下限 δ”。
真实 monotonic improvement 还需要 surrogate-quality、reward-estimation、acceptance rule 等条件。

因此当前 theory 更适合标记为：

- verified algebra/bound；
- convergence conditional on assumed error decay；
- framing-only；
- operator-linked theorem（当前为空）。

### R3-P0 · Best-of-N 的关键 KL 结论仍是 imported axiom

`BestOfN.lean` 定义了 opaque `klBoNActual : ℕ → ℝ`，然后用具名 axiom
`beirami_thm_3_1` 假设它满足上界。这样做比隐藏 `sorry` 诚实，也保持逻辑一致；但它没有在 Lean 中
定义实际 BoN distribution，也没有 machine-check Beirami 的 order-statistics 证明。

**裁定：** 可以写“the cited theorem is imported as one named axiom”，不能写“BoN KL theorem has
been formalized/proved in Lean”。

### R3-P1 · “training-free RL”是高风险定位词

独立文献审计显示：self-consistency、MBR、best-of-N、verifier-guided decoding 通常被称为
test-time compute、decoding、search、selection 或 inference-time alignment。TTRL 则通常真的在
test time 更新权重。当前工程把不更新权重的 validation selection、oracle selection、per-instance
selection 都统一叫 RL，会同时遭到两类 reviewer 质疑：

1. 没有 environment/state/action/trajectory/policy update，为什么不是黑盒搜索/模型选择？
2. 若用 gold WER 作 reward，部署如何得到？

建议主术语改为 **weight-frozen reward-guided inference-time optimization/search**；只有在明确定义
sequential decision process、feedback 与 policy update 的子模块中保留 RL。项目内部可继续使用
TFRL 缩写，但摘要第一处必须给出这个非标准定义并与 test-time RL 区分。

### R3-P1 · 新颖性不能靠“把 90 个文本方法搬到 speech”

现有 Step-3 候选表覆盖很广，但 breadth 不是 contribution。新颖性必须落在一个可证伪机制：

- audio-conditioned candidate geometry 与文本有何不同？
- error decorrelation 如何决定 selector realized fraction？
- task-conditioning 是否真的改变 factor-selective subspace？
- speech-keyed KB 的 granularity/organization 如何改变 retrieval-to-generation 因果链？

如果只是 port MBR/HyDE/RAPTOR/LLMLingua 到 speech，贡献上限是工程 transfer study。可以发表，但应
诚实定位，不应再附加“L4 intelligence / RL convergence / representation disentanglement”三层宏大主张。

## 6. 对抗评审 Round 4：为项目作最强辩护后，哪些结论仍然成立

本轮故意替项目辩护，避免只做破坏性审稿。

### 能站住的资产

1. **负结果记录是可信资产。** emotion +0.097 被跨 seed 修正为 null，M3 gold-transcript 被判定
   越界，T7 answer lookup 被作废，坏格保留 `.broken`；这种自我纠错应成为论文方法贡献的一部分。
2. **W1 support/headroom 是真实的。** 同一 frozen model 的 stochastic pool 在 N=8 有 oracle
   WER headroom；这证明研究 selector realization 有必要。
3. **边界纪律正在变成机器约束。** `kb_audit`、CLEAN gate、stored replies rescore、disjoint redraw
   都是正确方向。
4. **Lean 能检查“你究竟证明了什么”。** 虽然 theorem 当前过于抽象，但它已经暴露了 assumed
   `τ→0`、opaque axiom、docstring-only dual track；这是重写理论的好底座。
5. **工程运行能力强。** 单卡 5090、断点续跑、llama-server resident/batching、统一资产锁、per-item
   artifacts 已足够支撑一次严谨的窄问题研究。

### 最终 meta-verdict

- **NO-GO（当前版本）**：以现有证据发表“training-free RL disentangles frozen omni embeddings”；
- **NO-GO（当前版本）**：把 W1 oracle ASR headroom 写成 deployable performance gain；
- **NO-GO（当前版本）**：立即开跑 Step-2 140 格；
- **GO（推荐）**：把 W4 改成“frozen omni speech representation 的可读性、可选择性与极限”；
- **GO（支持线）**：把 W1 收窄为“label-free selector 能实现多少 oracle headroom”；
- **PARK/独立 paper**：speech-keyed knowledge/agentic RAG，等实现与 clean causal protocol 完成后再开。

## 7. 推荐的新问题定义

### 7.1 旗舰推荐（W4）

> **How far can weight-frozen, task-conditioned readout make an omni speech representation
> selective for content, speaker, emotion, and intent—and where does the frozen representation
> impose an irreducible ceiling?**

这比“已能解耦”更强，因为正负结果都可发表；也与现有数据一致：content strong、emotion partial、
speaker pooled-output weak、instruction steering null。

预注册四个假设：

- H1：final pooled embedding 的 content readout 显著强于 speaker/emotion；
- H2：mid-layer/trajectory readout 能稳定提升 emotion，但不能稳定恢复 fine-grained speaker；
- H3：instruction-only conditioning 不产生跨 dataset/backbone 的 target selectivity；
- H4：H-a 多特化键在副语言任务胜 H-b 单 omni 空间，而 H-b 在 content/intent 保持竞争力。

### 7.2 支持线推荐（W1）

> **Can a label-free selector realize a non-zero, calibrated fraction of the oracle candidate
> headroom of a frozen omni speech model under a fixed inference budget?**

主指标：

`ρ = (R_selector − R_greedy) / (R_oracle − R_greedy)`，同时报告 absolute task delta、CI、risk-coverage
与 GPU cost。oracle denominator≤0 的 item/dataset 单独处理，禁止制造无限/负 ρ。

### 7.3 暂缓线（Step-2 RAG）

如果 owner 仍把它设为 primary，应独立成一个 work/research proposal，问题限定为：

> 在 frozen reader、clean KB 和 audio-only query 下，speech-key granularity 与 retrieval/delivery
> 的哪个交互能带来超越 static RAG 的可复现增益？

它不再同时承担 W4 解耦、W1 selector、agent convergence 三种主张。

## 8. 详细改进计划

### Phase 0 · Stop-the-line 与真源修复（1–2 天）

1. owner 选择一个 primary question：推荐 W4 §7.1；W1 §7.2 为 supporting。
2. 暂停 Phase-A/Step-3 新 GPU run；保留当前 artifacts，不回滚。
3. 统一真源：`Per-Work-Status`、Step-2 grid、Decision Log、W1 `FREEZE_SHEET` 对齐；旧文档加
   `SUPERSEDED/STALE` 横幅，不重写历史。
4. 把所有主张标上 L0–L4 与 `directional / powered / replicated`。
5. W1 状态从“mature implementation”改为“mature experimental machinery”；其 Hydra `main.py`
   仍是 stub，不能暗示 package 主入口已完成。

**G0 gate：** owner 签署一页 claim tree：primary estimand、secondary estimands、kill criteria、
不再追逐的对象。未签不进入 Phase 1。

### Phase 1 · Fresh Stage-2 预注册（3–5 天）

每个被选问题创建独立 Research-Proposal-Template；不得沿用 Stage-1 freeze 当 Stage-2 prereg。

必须冻结：

- primary outcome、MCID、样本量/功效方法；
- model/dataset/runtime 与 license；
- group split unit；
- arm family 与多重比较方法；
- calibration/test/external-test 边界；
- oracle/offline/deployable 三类 operator；
- 何时停止、何时降级 claim。

推荐 split：

| Task | 开发/校准 | locked test | 外部复现 |
|---|---|---|---|
| content/ASR | LibriSpeech official dev | test-clean/test-other + noise strata | AISHELL/FLEURS 或另一模型 |
| ST | CoVoST2 official dev | official test，按 speaker/source group | 第二语言对 |
| emotion | CREMA-D speaker-grouped nested CV | IEMOCAP leave-one-session-out 或预留 actor fold | MELD/另一自然情感集 |
| speaker | VoxCeleb1 official enrollment/test | EER/minDCF protocol | CN-Celeb1/CREMA diagnostic |
| intent | MInDS/SLURP official train/dev | official test，speaker/template group check | 第二语言/第二 corpus |

**G1 gate：** hostile reviewer 对 prereg 给出 0 fundamental/major；test manifest 加密/权限隔离或至少
由独立脚本锁死，在所有 arm 选定前不打开。

### Phase 2 · 工程与统计地基（约 1 周）

#### W1/Step-2 必修

1. 给 `phase_a_cells` 真正的 execute/checkpoint path；每个 frozen arm 都必须 real-run 或从 grid 删除。
2. 统一 embedder token 与 source naming；manifest 必须精确重建同一个 query embedder，禁止 `auto`。
3. 实现真实 multi-granularity/H-a/H-b/RAPTOR-lite/audio+text；`two-stage` 必须是两个 index/stage。
4. `build_one` 接收 `eval_manifest`，机器验证 `source_ids ∩ eval_ids = ∅`；retrieve 时再次 own-item 排除。
5. leakage = exact + normalized n-gram + semantic/entailment auxiliary audit；所有 retrieved passages
   写入 result artifact 供复核。

#### 测试矩阵

- 每个 K-type 一个真实 row-schema golden fixture；
- 每个 dataset loader 至少一条 schema contract test；
- MCQ gold 解析做 property tests（裸字母、`A. text`、`answer_gt`、list gold）；
- K7 official scorer 与独立小 fixture parity；
- group split invariant 与 duplicate-family detector；
- 所有 Phase-A arm 用 fake model + tiny real index 跑完整 E2E，任何 `PLAN ONLY` 直接 fail；
- artifact schema 测试：git SHA、dirty、model hash、engine SHA、dataset revision、manifest hash、env hash。

#### 统计实现

- paired **cluster bootstrap**，cluster=task 对应 speaker/session/question-family；
- arm selection 用 nested CV 或独立 calibration；
- 同一 family 用 Holm 或 max-T 控制；跨 dataset 用 hierarchical/random-effects 汇总；
- seed 只作随机效应，不把重叠 test slice 当独立 n；
- 报告 effect+CI+cost，不以单个 `p<.05` 作为通过。

**G2 gate：** 全部 frozen arm E2E green；Phase-A 数量、文档、代码完全一致；无 `NotImplementedError`
进入已冻结网格；独立复核能从 result JSON 重建每个数字。

### Phase 3 · W4 claim ladder 实验（方向性 2–3 天；通过后 powered）

#### 3.1 控制矩阵

每个 factor 至少比较：

1. final pooled raw；
2. random/format-matched instruction；
3. target instruction 与 mismatched instructions；
4. layer × mean/stats/attentive/trajectory readout；
5. random projection + PCA/whitening control；
6. specialized frozen encoder（ContentVec/WavLM/Emotion2Vec/ERes2NetV2）；
7. small trained probe/LoRA upper bound（明确 out-of-scope comparison）；
8. no-audio/audio-blind control。

#### 3.2 真正的 disentanglement 证据

对每个 conditioned view 同时测：

- target sufficiency：target task performance；
- nuisance leakage：其他 factor 的 linear、MLP、kNN、MDL probe；
- selectivity：`target_gain − max(off_target_gain)` 的 paired CI；
- counterfactual invariance：同 sentence 换 speaker/emotion、同 speaker 换 sentence/emotion；
- cross-group/OOD：unseen speaker/session/language；
- representation geometry：CKA/subspace angle 只作描述，不能替代 causal test。

只有“target 提升 + nuisance 不升或下降 + counterfactual 过关”才能晋级 L3。单纯 probe acc 不再称
disentanglement。

**W4 kill：** 若 target selectivity 的 powered CI 在至少两个 dataset 或两个 backbone 上都不超过
预注册 MCID，则放弃“task-conditioned disentanglement”，转投“limits/suppression”论文；这仍是成功
收官，不继续换 prompt 直到显著。

### Phase 4 · W1 selector-realization 实验（约 1 周）

1. 固定同一 utterance set、同一 candidate pools，所有 selector 只重放 stored pools；
2. N∈{1,2,4,8,16,32} × temperature/top-p diversity sweep；报告 unique/effective N；
3. baseline：greedy、beam/diverse beam、random pick、ROVER、edit-MBR、semantic-centroid/RCS、
   self-certainty、calibrated confidence、independent ASR ensemble、cross-model verifier、oracle；
4. calibration 只用 calibration set；test 上不再调 threshold/utility；
5. 指标：corpus WER + macro utterance WER、ρ、risk-coverage、ECE/Brier、latency/energy/VRAM；
6. 同一 item 重复 ≥3 个 pool seeds，使用 crossed item×pool 随机效应；
7. OOD：clean/noisy、LibriSpeech→另一英语集、中文单独 replication。

**W1 kill：** 若 deployable selector 在两个独立 test surface 上 `ρ` 的 CI 不高于 0，结论定为
“support exists but realization fails”；若仅一个模型/一个 runtime 有效，定位为 case study。

### Phase 5 · 如果保留 Step-2 RAG（实现后 1–2 周）

不要直接跑 140-cell OAT。推荐：

1. primary=一个 clean knowledge task，replication=一个不同结构 task；
2. 预注册 D-optimal/fractional factorial 设计，覆盖 main effects + 指定两阶交互；
3. 固定 non-agentic RAG baseline；agentic 只作为额外 factor；
4. retrieval 与 generation 分开报：R@k/MRR/nDCG、answer EM/F1/fidelity；
5. 必带 no-retrieval、random retrieval、oracle retrieval、long-context stuffing、gold-transcript
   **upper bound（只作上界）**、own-ASR cascade；
6. random retrieval 若等于 best arm，或 oracle retrieval 也无 gain，则停止优化 retrieval；
7. final test 只跑预注册的一个 winner + controls，不进行多轮“debate-improve”后再次看同一 test。

### Phase 6 · 理论重写与 Lean 双轨（1–2 周，可与 powered run 并行）

先定义代码实际 operator，再证明：

1. **Coverage theorem**：有限 action set 下，若最优 action 在 base support 中质量为 `p*`，BoN miss
   probability=`(1-p*)^N`；这直接对应 stored pool；
2. **Selector theorem**：在明确的 calibration/error model 下给出 realized regret；`τ` 必须由校准
   数据或 estimator 机制推出/上界，而非自由假设 `τ→0`；
3. **Exponential-weights/bandit theorem**：对代码中的 `q_{t+1}∝q_t exp(η_t Rhat_t)`，在 bounded
   unbiased noise、可检验 step-size 下给 finite-time regret/convergence；
4. **Negative result**：构造 biased proxy 或固定大 step 的实际 counterexample；
5. **No-universal-N\***：若没有 proxy-error-vs-N 假设，先证明普适 interior optimum 不存在；再在
   明确 error-growth model 下证明 N*；
6. 把 `klBoNActual` 换成 finite distribution 的真实定义；若短期做不到，继续列为 imported axiom，
   不把它计入 formalized contribution；
7. CI 中运行 `#print axioms` whitelist；Python/Lean 对同一有限 rational test vector 输出 parity。

**Theory kill：** theorem 若只在 docstring 指向 Python、或承重前提无法由实验估计，就标
`framing-only`，不进入 contribution list。

### Phase 7 · Survey 与论文质量门（全程）

1. 所有 load-bearing claims 全量 primary-source verify，不再只抽 20 条；
2. source ledger 增：paper version/date、primary/secondary、exact support、counterevidence、核验者；
3. “empty niche/exhaustive”必须附数据库、query、日期、语言、纳排标准；否则改成“we found no ...”；
4. 补入 probing/disentanglement 基础反例与 test-time search 的标准术语；
5. 外部 fresh reviewer 分四轮：claim validity → stats/leakage → theory/operator → reproducibility；
6. 每轮只允许修 pre-registered protocol/表述，禁止看 test 后增加新 arm。

## 9. 总门控与建议时间线

| Gate | 必须交付 | 失败动作 |
|---|---|---|
| G0 scope | 一个 primary question + claim tree + kill criteria | 停止 GPU 扩张 |
| G1 prereg | fresh Stage-2 proposal + group split + stats | 回 Stage 1 讨论 |
| G2 executable | 冻结臂全 E2E + provenance + tests | 删除/实现 arm，不运行 |
| G3 directional | 不开 locked test 的小样本机制检查 | 机制 null 则 kill |
| G4 powered | powered locked-test run | 降级 claim，不换题追显著 |
| G5 replication | 第二 dataset/backbone/runtime | 限定为 case study |
| G6 theory | 同一 operator、可估假设、axiom ledger | theory 仅 framing |
| G7 paper | 四轮 hostile review 0 major | 不投稿 |

单卡现实时间线：Week 0 scope+真源；Week 1 prereg+测试；Week 2 W4 grouped baselines；Week 3 W1
selector；Week 4 replication；Week 5 theory；Week 6 paper assembly。Step-2 RAG 若保留，另开 2–3 周，
不要与 W4/W1 powered run 抢同一个 scientific headline。

## 10. 论文 survey 的核心锚点（精选，不是完整 bibliography）

### Test-time search / BoN / MBR / overoptimization

- [Scaling LLM Test-Time Compute Optimally Can Be More Effective than Scaling Model Parameters](https://arxiv.org/abs/2408.03314)
- [Large Language Monkeys: Scaling Inference Compute with Repeated Sampling](https://arxiv.org/abs/2407.21787)
- [Self-Consistency Improves Chain of Thought Reasoning](https://openreview.net/forum?id=1PL1NIMMrw)
- [Is Best-of-N the Best of Them?](https://proceedings.mlr.press/v267/huang25c.html)
- [Theoretical Guarantees on the Best-of-n Alignment Policy](https://arxiv.org/abs/2401.01879)
- [Scaling Laws for Reward Model Overoptimization](https://arxiv.org/abs/2210.10760)
- [Re-evaluating Minimum Bayes Risk Decoding for ASR](https://arxiv.org/abs/2510.19471)
- [mbrs: A Library for Minimum Bayes Risk Decoding](https://arxiv.org/abs/2408.04167)
- [Controlling Multimodal LLMs via Reward-guided Decoding](https://openaccess.thecvf.com/content/ICCV2025/html/Manas_Controlling_Multimodal_LLMs_via_Reward-guided_Decoding_ICCV_2025_paper.html)
- [Trust Region Policy Optimization](https://arxiv.org/abs/1502.05477)

### Speech representation / disentanglement / probing

- [Challenging Common Assumptions in Unsupervised Disentanglement](https://arxiv.org/abs/1811.12359)
- [Designing and Interpreting Probes with Control Tasks](https://arxiv.org/abs/1909.03368)
- [Information-Theoretic Probing with Minimum Description Length](https://arxiv.org/abs/2003.12298)
- [ContentVec](https://arxiv.org/abs/2204.09224)
- [CCSRD: Content-Centric Speech Representation Disentanglement](https://aclanthology.org/2023.findings-emnlp.394/)
- [A Large-Scale Probing Analysis of Speaker-Specific Attributes](https://arxiv.org/abs/2501.05310)
- [Disentangling Textual and Acoustic Features of Neural Speech Representations](https://arxiv.org/abs/2410.03037)
- [Towards the Next Frontier in Speech Representation Learning Using Disentanglement](https://arxiv.org/abs/2407.02543)
- [Omni-Embed-Nemotron](https://arxiv.org/abs/2510.03458)
- [Qwen2.5-Omni](https://arxiv.org/abs/2503.20215)

### Speech/audio RAG 与 frozen-reader attribution

- [Speech Retrieval-Augmented Generation without ASR](https://arxiv.org/abs/2412.16500)
- [WavRAG](https://arxiv.org/abs/2502.14727)
- [End-to-End S2S RAG on GLM-Voice](https://arxiv.org/abs/2505.00028)
- [Stream RAG](https://arxiv.org/abs/2510.02044)
- [Audiopedia](https://arxiv.org/abs/2412.20619)
- [REPLUG: Retrieval-Augmented Black-Box Language Models](https://aclanthology.org/2024.naacl-long.463/)
- [Lost in the Middle](https://arxiv.org/abs/2307.03172)
- [RAPTOR](https://arxiv.org/abs/2401.18059)
- [HippoRAG 2](https://arxiv.org/abs/2502.14802)
- [RAGChecker](https://arxiv.org/abs/2408.08067)

### 统计与可复现性

- [The Hitchhiker's Guide to Testing Statistical Significance in NLP](https://aclanthology.org/P18-1128/)
- [The Reusable Holdout](https://arxiv.org/abs/1506.02629)
- [Statistical Comparisons of Classifiers over Multiple Data Sets](https://jmlr.org/papers/v7/demsar06a.html)

## 11. 一句话交付

当前项目最值得发表的不是“我们已经用 training-free RL 解耦了 frozen omni”，而是：

> **我们系统测量了 frozen omni speech model 在 support、readout、task selectivity 与 deployable
> realization 四个层级上的能力边界，并证明哪些增益是真实的、哪些只存在于 oracle、哪些被
> representation suppression 与 selector error 封顶。**

这条叙事与现有正负证据一致，也能让后续真正的正结果有清楚、可信的落点。
