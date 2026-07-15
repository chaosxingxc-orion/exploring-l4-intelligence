# L3 探索知识库入口 — Survey Archive & Paper Registry

> **本目录 = 探索知识层（L3）的稳定检索库**（知识四层规约见 [[AI-Collaboration]] §记录规约，
> 续47）。**正典种子 = census v2（95 works，canonical ID + 版本钉，94 RESOLVED + 1 如实
> UNRESOLVED）+ claim-ledger v2（62 行，claim×work×span，五级证据等级），@28ad858，验收
> @b1af8c6。** 登记规约（从严）：凡 FETCH/精读过的论文必须按此 schema 登记，不登记不算读过；
> 判决层修订必须带伴随 token。
>
> **登记 token（system-first proposal v1 起用）**：`AS_CITED_BY_REVIEW`（评审点名、未做可回放
> 核查）/ `RETAINED_RECORDS@census-v2`（在 94 记录簇→95 works 保留记录内,@28ad858）/
> `ROUND2_PREREGISTERED_TARGET`（round-2 预注册待查目标,零执行,题录级 AS_GIVEN_BY_REVIEW）/
> `TRAINED_COMPARATOR`（带训练组件的对照臂,TF-Strict 下永不承重）。
> **流程/状态 token（重校准评审提供,proposal v2 起用）**：`PROVISIONAL_STAGE1A_TAXONOMY`
> （五合同现阶段身份=暂定分类学,survey 证据可修订）/ `candidate_kill_logic_for_stage1b_design`
> （kill 表现阶段身份=1B 设计候选逻辑,非冻结实验）/ `OUT_OF_SCOPE_WEIGHT_UPDATED`（test-time
> 权重更新类,边界对照）/ `PROTOCOLIZATION_AUTHORIZED / QUERY_EXECUTION_STILL_PENDING`
> （Gate S1 两段式状态）/ `TO_VERIFY_FULLTEXT`（delta 叙述待全文核验）/ `KNOWN`（survey 执行
> 期去重标记:命中 census v2 既有 work,仍全量登记）。
> **信息来源六类分解（v3 外审 §2.2-G 起用,系 read-out/new-info 二分的直系升级——抽取轴与
> 归因纪律共用）**：①task-native observation ②pretrained-knowledge read-out ③deterministic
> transformation/computation ④endogenous environment feedback（agent 动作引致）⑤exogenous
> answer-bearing retrieval / new-info ⑥evaluation gold（禁入决策路径）。每个候选机制标注
> 所用类别;⑤类增益不得概括为「激活预训练知识」。**manifest 策展期中文值 = 登记 token 的
> 显示形**：题录AS_GIVEN↔AS_CITED_BY_REVIEW、census在库(题录+)↔RETAINED_RECORDS@census-v2、
> delta待全文核验↔TO_VERIFY_FULLTEXT（协议 §3 有映射表,执行期升级改记五级英文标尺）。
>
> **勿再引已撤回口径**（"~93 papers" / "305 queries" / "I4 最干净 whitespace"——现行结论一律
> 按身份索引表：RESP-02 §3.3 与 [[Research-Objective]] §4/§5）。Survey v2 状态 =
> ROUND1_SCOUT_COMPLETE。工件：[[2026-07-14-neighbor-matrix-v2]] ·
> [[2026-07-14-coverage-and-kill-matrix-v2]] · [[2026-07-14-sota-cards-v2]] ·
> `2026-07-14-scout-ledger-round2.json` · `2026-07-14-search-query-log.jsonl` ·
> round-1 前身 `2026-07-13-scout-ledger-round1.json`（其检索宇宙永久缺失，已如实签
> REPLAY_FAILED）。

> Part of the **Step-2 survey** for [[2026-06-26-training-free-rl-for-speech-omni-research-proposal]] (see [[Research-Proposal-Template]] §3). Produced by a multi-agent survey workflow (5 lanes -> per-lane adversarial verification -> synthesis), run `wf_d76b4901-23c`, 2026-06-26. Every source below was adversarially checked to resolve to a real paper; only `keep=true` claims are archived. Links are real and verifiable.


This directory archives the verified citations behind the **Survey & Positioning (§3)** of [[2026-06-26-training-free-rl-for-speech-omni-research-proposal]]. Five lanes, each adversarially verified; a claim is archived only if its source(s) resolved to a real paper (`sources_resolve=true`, `keep=true`).

> **归档约定（2026-07-11 起）**：战役收官即归档——一个调研/实验战役被裁定收官（GO/NO-GO、被后续战役取代、
> 或结论已改判）后，其过程调研件迁入 `archive/survey/<campaign>/` 子目录，PREPEND 🗄 ARCHIVED 状态横幅，
> 原文按 append-only 不改写。已迁移：2026-06-26 提案期调研（5 件）→ `archive/survey/2026-06-26-proposal/`；
> 2026-06-30 agent-level 调研（11 件）→ `archive/survey/2026-06-30-agent-level/`；2026-07-03 NO-GO 战役
> （11 件）→ `archive/survey/2026-07-03-nogo-campaign/`；2026-07-06 omni-agentic 调研（16 件）→
> `archive/survey/2026-07-06-omni-agentic/`。裁定见 [[2026-07-11-stage1-audit-response-and-rulings]]。
> 2026-07-04/07/08/09 前缀的调研件仍为现行 LOG/active，不在此列。

## Lanes


| # | Lane | File | Kept claims |
|---|---|---|---|
| 1 | Omni pretrained-capability map & the two model classes | [capability-map](../archive/survey/2026-06-26-proposal/2026-06-26-survey-capability-map.md) | 20/20 |
| 2 | ICL / few-shot / explicit task-definition & label-sensitivity in audio LLMs | [icl-fewshot](../archive/survey/2026-06-26-proposal/2026-06-26-survey-icl-fewshot.md) | 15/15 |
| 3 | Training-free / inference-time RL methods & convergence theory | [tfrl-theory](../archive/survey/2026-06-26-proposal/2026-06-26-survey-tfrl-theory.md) | 15/15 |
| 4 | Verifiable rewards, evaluation & leakage/reproducibility pitfalls | [rewards-eval](../archive/survey/2026-06-26-proposal/2026-06-26-survey-rewards-eval.md) | 18/18 |
| 5 | Novelty-delta vs the closest prior work | [novelty-delta](../archive/survey/2026-06-26-proposal/2026-06-26-survey-novelty-delta.md) | 12/12 |

**Totals:** 80 kept claims · 93 unique verified sources.


## Agent-level survey — S1 (2026-06-30)

Strategic direction probe for [[2026-06-30-agent-level-synthesis]] (run `wf_8452c9ae-a11`). 41 verified
claims / 51 sources; verdict: **GO — add-new-layer, speech-grounded** (domain-transfer, not mechanism-novel).
Each claim is scope-tagged (no-gradient = in scope vs weight-updating = out).

| Lane | File | Kept |
|---|---|---|
| A4 — speech/omni agents & the moat (B3) | [agent-speech-agents](../archive/survey/2026-06-30-agent-level/2026-06-30-survey-agent-speech-agents.md) | 15 |
| A5 — model classes as components + novelty (B5/B7) | [agent-components-novelty](../archive/survey/2026-06-30-agent-level/2026-06-30-survey-agent-components-novelty.md) | 13 |
| A3-headroom — does it compound? (B1/B4) | [agent-does-it-compound](../archive/survey/2026-06-30-agent-level/2026-06-30-survey-agent-does-it-compound.md) | 13 |

Living strategic memo: [agent-level-synthesis](../archive/survey/2026-06-30-agent-level/2026-06-30-agent-level-synthesis.md).

## Agent-level survey — S2 deepening: memory + skills design (2026-06-30)

Design-oriented deepening (run `wf_a066da37-c09`); 43 verified claims / 70 sources. **Design synthesis:**
[agent-memory-skills-design](../archive/survey/2026-06-30-agent-level/2026-06-30-agent-memory-skills-design.md).

| Lane | File | Kept |
|---|---|---|
| A1 — agent memory (deep design + speech) | [agent-memory](../archive/survey/2026-06-30-agent-level/2026-06-30-survey-agent-memory.md) | 26 |
| A2 — agent skills (deep design + speech) | [agent-skills](../archive/survey/2026-06-30-agent-level/2026-06-30-survey-agent-skills.md) | 17 |

Key finding: a **verifiable-reward acceptance gate** is the one control law for both components (SkillsBench:
curated skills +16.2pp vs self-generated ~0); θ2's β-KL trust region instantiates as Mem0 mutation-rate (memory)
+ GEPA Pareto non-regression (skills). Both run on existing frozen assets (Omni-Embed-Nemotron index + W1
verifiable speech rewards). Open contribution: no audio cross-session paralinguistically-keyed memory benchmark.

## Agent-level survey — θ2 convergence (2026-06-30)

Convergence-focused survey grounding the OptSpace proof **OSA-3** (`proofs/tfrl/OptSpace-notes.md`; run
`wf_14ef3acb-2a3`). 43 verified claims / 54 sources. **Synthesis + convergence map:**
[agent-convergence](../archive/survey/2026-06-30-agent-level/2026-06-30-survey-agent-convergence.md).

| Lane | File | Kept |
|---|---|---|
| CV1 — output-level convergence theory | [output-convergence](../archive/survey/2026-06-30-agent-level/2026-06-30-survey-agent-output-convergence.md) | 14 |
| CV2 — agent-level convergence & stability | [agent-stability](../archive/survey/2026-06-30-agent-level/2026-06-30-survey-agent-agent-stability.md) | 15 |
| CV3 — algorithm-level stabilization | [stabilization](../archive/survey/2026-06-30-agent-level/2026-06-30-survey-agent-stabilization.md) | 14 |

Key finding: proven *finite-N* convergence lives at the **output level** (soft-BoN O(1/N), MBR, GSI, HedgeTune
N*); the **agent level** has only **JitRL**'s *asymptotic* consistency under a trust-region/slow-drift
precondition — the trust region is the hinge that links naive non-convergence (OSA-3a) to credit-assigned
convergence (OSA-3b). Open-source: [JitRL](https://github.com/liushiliushi/JitRL), HedgeTune, GSI, ACE, AWM, LATS.

## Step-1 rationality campaign — agentic-TFRL GO/NO-GO (2026-07-03/04)

> Pre-registered decision campaign (freeze anchor b19bff2), null hypothesis = the 2026-07-02
> deep-review verdict. Outcome: **NO-GO ratified by owner 2026-07-04** — the agent-level question is
> CLOSED absent re-open conditions r1-r3. Decision doc: [[2026-07-03-omni-agentic-tfrl-go-no-go-decision]];
> pre-registration: [[2026-07-03-agentic-tfrl-step1-preregistration]]. Runs: wf_a68f9164-b3c (Phase 0),
> wf_68e2556d-7a7 (delta/Part-A/mechanisms), wf_f6d37987-df5 (B-lanes/panel/synthesis),
> wf_e5dd317b-9cb (/ars-reviewer fresh-adversary panel).

- [[2026-07-03-step1-delta-headroom-theory]] — D1: decomposition/headroom theory delta (10 verified claims; r2 EMPTY)
- [[2026-07-03-step1-delta-speech-agent-memory]] — D2: speech agent memory/skills delta (11 claims; r1 NOT MET, 12 empty searches)
- [[2026-07-03-step1-delta-selector-learning]] — D3: selector learning / reference-free QE delta (12 claims)
- [[2026-07-03-step1-part-a-memo]] — Part-A: single-model TFRL rationality (RATIONAL-AND-CONTINUING)
- [[2026-07-03-step1-mechanism-support-expansion]] — M3 dossier + Phase-0 KILL (F=0.38108 vs 0.01)
- [[2026-07-03-step1-mechanism-selector-accumulation]] — M5 dossier + confirmatory NO-PASS (exact zero, inert instrument)
- [[2026-07-03-step1-mechanism-cross-block-dependence]] — M2 dossier (design-only)
- [[2026-07-03-step1-mechanism-sampling-isolation]] — M4 dossier (design-only)
- [[2026-07-03-step1-blanes-memos]] — B3 task-family / B4 VoI / B5 feasibility memos (post-outcome compilation)
- [[2026-07-03-step1-hostile-panel-verdicts]] — 6-charge panel: all stands; steelman-NO-GO; briefs record
- [[2026-07-03-step1-ars-reviewer-panel]] — /ars-reviewer 5-persona panel: sound-with-corrections (C1-C12 applied)

W1-repo pilot artifacts: `_repro/m3_phase0_selection.json`, `_repro/m3_phase0_zero_support.json`,
`_repro/m5_selector_dev.json`, `_repro/m5_confirmatory_slice_ids.json`, `_repro/m5_selector_confirmatory.json`,
`_repro/m5_memo_censuses.json` (12/12 memo numbers reproduced).

## Stage-1 problem-definition campaign — semantic-layer TFRL/ICL (2026-07-04)

> Three-stage methodology now in CLAUDE.md (current stage: 1). Question: is the instruct-prompt
> rollout optimization space of a frozen omni speech model sufficient for the semantic layer
> (ASR/SLU/SQA/agentic)? Deliverable: a strict-reviewed survey + a ranked problem-definition doc for
> the owner's K2 discussion. Runs: wf_d7b939e9-c37 (survey lanes), wf_f2b71475-290 (paper draft),
> wf_707e82fb-c2a (D5b strict review → MAJOR REVISION), wf_fab1d8d1-ccc (re-review → all-P1-resolved).

- [[2026-07-04-stage1-evidence-regrade]] — D1: prior work re-graded under the Stage-1 lens
- [[2026-07-04-paralinguistic-premise-consolidation]] — D2: shallow-signal premise (vector settled / generative lit-only)
- [[2026-07-04-sufficiency-yardstick-memo]] — D3: the H_fix/H_prompt/ρ yardstick (SNR +5 dB corrected)
- [[2026-07-04-stage1-L1-asr-st]] · [[2026-07-04-stage1-L2-slu]] · [[2026-07-04-stage1-L3-sqa-reasoning]] · [[2026-07-04-stage1-L4-speech-agentic]] — D4 family lanes
- [[2026-07-04-stage1-X1-prompt-space-quantification]] · [[2026-07-04-stage1-X2-paralinguistic-delta]] · [[2026-07-04-stage1-X3-llm-vlm-testtime-map]] — D4 cross-cutting lanes
- [[2026-07-04-stage1-3w-crossdomain-comparisons]] — D4 cross-domain WHY/HOW/WHAT triples
- **[[2026-07-04-stage1-semantic-tfrl-survey]]** — D5a the survey paper (16k words, 171 refs; REVISED-POST-D5B)
- [[2026-07-04-stage1-survey-d5b-review]] · [[2026-07-04-stage1-survey-d5b-rereview]] — D5b strict review (MAJOR REVISION → all-P1-resolved)
- **[[2026-07-04-stage1-problem-definition]]** — D5c ranked candidates (top-3: CP-1 H_prompt quantification / CP-3 selector anatomy / CP-8 calibration+PMI); FOR-OWNER-DISCUSSION-K2

W1-repo Stage-1 probe artifact: `_repro/probe_hprompt_vs_hfix.json` (Δ_BM matched-budget, ASR, n=50 [directional-only]);
scripts `probe_hprompt_vs_hfix.py`, mini-prereg pre-committed at bae2184.

## Consolidated bibliography (Step-2 model-output survey; all verified, deduplicated)

- [A Large-Scale Probing Analysis of Speaker-Specific Attributes in Self-Supervised Speech Representations](https://arxiv.org/abs/2501.05310)
- [A Meta-Analysis of Overfitting in Machine Learning (Roelofs et al., NeurIPS 2019)](https://papers.nips.cc/paper/9117-a-meta-analysis-of-overfitting-in-machine-learning)
- [AIR-Bench: Benchmarking Large Audio-Language Models via Generative Comprehension](https://arxiv.org/abs/2402.07729)
- [ALICE: A Multifaceted Evaluation Framework of Large Audio-Language Models' In-Context Learning Ability](https://arxiv.org/abs/2603.20433)
- [Aligning Paralinguistic Understanding and Generation in Speech LLMs via Multi-Task Reinforcement Learning](https://arxiv.org/abs/2603.15981)
- [Answer is All You Need: Instruction-following Text Embedding via Answering the Question (InBedder)](https://arxiv.org/abs/2402.09642)
- [ASR Error Correction using Large Language Models](https://arxiv.org/abs/2409.09554)
- [Asymptotics of Language Model Alignment](https://arxiv.org/abs/2404.01730)
- [Attentive Statistics Pooling for Deep Speaker Embedding](https://arxiv.org/abs/1803.10963)
- [Benchmark Data Contamination of Large Language Models: A Survey](https://arxiv.org/abs/2406.04244)
- [Benchmarking Contextual and Paralinguistic Reasoning in Speech-LLMs](https://arxiv.org/abs/2509.16589)
- [Best-of-N through the Smoothing Lens: KL Divergence and Regret Analysis](https://arxiv.org/abs/2507.05913)
- [BoNBoN Alignment for Large Language Models and the Sweetness of Best-of-n Sampling](https://arxiv.org/abs/2406.00832)
- [Bootstrap estimates for confidence intervals in ASR performance evaluation (Bisani & Ney, ICASSP 2004)](https://ieeexplore.ieee.org/document/1326009)
- [Can Generative Large Language Models perform ASR error correction?](https://arxiv.org/abs/2307.04172)
- [CLAP: Learning Audio Concepts From Natural Language Supervision](https://arxiv.org/abs/2206.04769)
- [Comparative layer-wise analysis of self-supervised speech models](https://arxiv.org/abs/2211.03929)
- [Controlled Decoding from Language Models](https://arxiv.org/abs/2310.17022)
- [Deep Reinforcement Learning that Matters](https://arxiv.org/abs/1709.06560)
- [Defining and Characterizing Reward Hacking](https://arxiv.org/abs/2209.13085)
- [Diffusion vs. Autoregressive Language Models: A Text Embedding Perspective](https://arxiv.org/abs/2505.15045)
- [Discovering and Causally Validating Emotion-Sensitive Neurons in Large Audio-Language Models](https://arxiv.org/abs/2601.03115)
- [Do Audio LLMs Listen or Read? Analyzing and Mitigating Paralinguistic Failures with VoxParadox](https://arxiv.org/abs/2605.27772)
- [Do Audio LLMs Really LISTEN, or Just Transcribe? Measuring Lexical vs. Acoustic Emotion Cues Reliance](https://arxiv.org/abs/2510.10444)
- [Dynamic-SUPERB Phase-2 (180 tasks)](https://arxiv.org/abs/2411.05361)
- [Dynamic-SUPERB: A Dynamic, Collaborative, Comprehensive Instruction-Tuning Benchmark for Speech](https://arxiv.org/abs/2309.09510)
- [ECAPA-TDNN: Emphasized Channel Attention, Propagation and Aggregation in TDNN Based Speaker Verification](https://arxiv.org/abs/2005.07143)
- [EmoSLLM: Parameter-Efficient Adaptation of LLMs for Speech Emotion Recognition](https://arxiv.org/abs/2508.14130)
- [Exploring In-Context Learning of Textless Speech Language Model for Speech Classification Tasks](https://arxiv.org/abs/2310.12477)
- [Few-shot Personalization via In-Context Learning for Speech Emotion Recognition based on Speech-Language Model](https://arxiv.org/abs/2509.08344)
- [Frozen Large Language Models Can Perceive Paralinguistic Aspects of Speech](https://arxiv.org/abs/2410.01162)
- [FSA-GRPO: Teaching Auditory LLMs to Use Few-shot Demonstrations](https://arxiv.org/abs/2606.02615)
- [Function Vectors in Large Language Models](https://arxiv.org/abs/2310.15213)
- [Generative Speech Recognition Error Correction with LLMs and Task-Activating Prompting](https://arxiv.org/abs/2309.15649)
- [Ground-Truth Labels Matter: A Deeper Look into Input-Label Demonstrations](https://arxiv.org/abs/2205.12685)
- [How do Multimodal Foundation Models Encode Text and Speech? An Analysis of Cross-Lingual and Cross-Modal Representations](https://arxiv.org/abs/2411.17666)
- [Improving Reproducibility in Machine Learning Research (NeurIPS 2019 Reproducibility Program)](https://arxiv.org/abs/2003.12206)
- [In-Context Learning in Speech Language Models: Analyzing the Role of Acoustic Features, Linguistic Structure, and Induction Heads](https://arxiv.org/abs/2604.06356)
- [Inference-Time Reward Hacking in Large Language Models](https://arxiv.org/abs/2506.19248)
- [INSTRUCTIR: A Benchmark for Instruction Following of Information Retrieval Models](https://arxiv.org/abs/2402.14334)
- [Judging the Judges: A Systematic Study of Position Bias in LLM-as-a-Judge](https://arxiv.org/abs/2406.07791)
- [Just-In-Time Reinforcement Learning: Continual Learning in LLM Agents Without Gradient Updates](https://arxiv.org/abs/2601.18510)
- [Larger language models do in-context learning differently](https://arxiv.org/abs/2303.03846)
- [Layer-wise Analysis of a Self-supervised Speech Representation Model](https://arxiv.org/abs/2107.04734)
- [LEACE: Perfect linear concept erasure in closed form](https://arxiv.org/abs/2306.03819)
- [Making Text Embedders Few-Shot Learners (bge-en-icl)](https://arxiv.org/abs/2409.15700)
- [MiMo-Audio: Audio Language Models are Few-Shot Learners](https://arxiv.org/abs/2512.23808)
- [MMAU: A Massive Multi-Task Audio Understanding and Reasoning Benchmark](https://arxiv.org/abs/2410.19168)
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595)
- [New Skills or Sharper Primitives? A Probabilistic Perspective on the Emergence of Reasoning in RLVR](https://arxiv.org/abs/2602.08281)
- [NV-Embed: Improved Techniques for Training LLMs as Generalist Embedding Models](https://arxiv.org/abs/2405.17428)
- [Omni-Embed-Nemotron: A Unified Multimodal Retrieval Model for Text, Image, Audio, and Video](https://arxiv.org/abs/2510.03458)
- [One Embedder, Any Task: Instruction-Finetuned Text Embeddings (INSTRUCTOR)](https://arxiv.org/abs/2212.09741)
- [Qwen-Audio: Advancing Universal Audio Understanding](https://arxiv.org/abs/2311.07919)
- [Qwen2-Audio Technical Report](https://arxiv.org/abs/2407.10759)
- [Qwen2.5-Omni Technical Report](https://arxiv.org/abs/2503.20215)
- [Qwen3-Omni Technical Report](https://arxiv.org/abs/2509.17765)
- [Re-evaluating Minimum Bayes Risk Decoding for Automatic Speech Recognition](https://arxiv.org/abs/2510.19471)
- [Rethinking the Role of Demonstrations: What Makes In-Context Learning Work?](https://arxiv.org/abs/2202.12837)
- [RL with KL penalties is better viewed as Bayesian inference](https://arxiv.org/abs/2205.11275)
- [RLVR Implicitly Incentivizes Correct Reasoning in Base LLMs](https://arxiv.org/abs/2506.14245)
- [Robust Speech Recognition via Large-Scale Weak Supervision (Whisper)](https://arxiv.org/abs/2212.04356)
- [SALMONN: Towards Generic Hearing Abilities for Large Language Models](https://arxiv.org/abs/2310.13289)
- [Scaling Laws for Reward Model Overoptimization](https://arxiv.org/abs/2210.10760)
- [Seamless: Multilingual Expressive and Streaming Speech Translation](https://arxiv.org/abs/2312.05187)
- [SeamlessM4T: Massively Multilingual & Multimodal Machine Translation](https://arxiv.org/abs/2308.11596)
- [Self-Consistency Improves Chain of Thought Reasoning in Language Models](https://arxiv.org/abs/2203.11171)
- [Self-Preference Bias in LLM-as-a-Judge](https://arxiv.org/abs/2410.21819)
- [Show Your Work: Improved Reporting of Experimental Results](https://arxiv.org/abs/1909.03004)
- [SimCSE: Simple Contrastive Learning of Sentence Embeddings](https://arxiv.org/abs/2104.08821)
- [SLURP: A Spoken Language Understanding Resource Package](https://aclanthology.org/2020.emnlp-main.588/)
- [Soft Best-of-n Sampling for Model Alignment](https://arxiv.org/abs/2505.03156)
- [Speaker Verification with Speech-Aware LLMs: Evaluation and Augmentation](https://arxiv.org/abs/2603.10827)
- [Spurious Rewards: Rethinking Training Signals in RLVR](https://arxiv.org/abs/2506.10947)
- [SUPERB: Speech processing Universal PERformance Benchmark](https://arxiv.org/abs/2105.01051)
- [Task Contamination: Language Models May Not Be Few-Shot Anymore](https://ojs.aaai.org/index.php/AAAI/article/view/29808)
- [Task Vectors in In-Context Learning: Emergence, Formation, and Benefits](https://arxiv.org/abs/2501.09240)
- [Test-Time Preference Optimization: On-the-Fly Alignment via Iterative Textual Feedback](https://arxiv.org/abs/2501.12895)
- [The Debate on RLVR Reasoning Capability Boundary: Shrinkage, Expansion, or Both?](https://arxiv.org/abs/2510.04028)
- [The Hitchhiker's Guide to Testing Statistical Significance in NLP](https://aclanthology.org/P18-1128/)
- [The reusable holdout: Preserving validity in adaptive data analysis (Dwork et al., Science 2015)](https://doi.org/10.1126/science.aaa9375)
- [Theoretical Guarantees for Minimum Bayes Risk Decoding (ACL 2025)](https://arxiv.org/abs/2502.12685)
- [Theoretical guarantees on the best-of-n alignment policy](https://arxiv.org/abs/2401.01879)
- [tinyBenchmarks: evaluating LLMs with fewer examples](https://arxiv.org/abs/2402.14992)
- [True Few-Shot Learning with Language Models](https://arxiv.org/abs/2105.11447)
- [TTRL: Test-Time Reinforcement Learning](https://arxiv.org/abs/2504.16084)
- [Tulu 3: Pushing Frontiers in Open Language Model Post-Training](https://arxiv.org/abs/2411.15124)
- [Understanding Contrastive Representation Learning through Alignment and Uniformity on the Hypersphere](https://arxiv.org/abs/2005.10242)
- [UniAudio 1.5: LLM-driven Audio Codec is a Few-shot Audio Task Learner](https://arxiv.org/abs/2406.10056)
- [We Need to Talk about Standard Splits](https://aclanthology.org/P19-1267/)
- [What do self-supervised speech and speaker models learn? New findings from a cross model layer-wise analysis](https://arxiv.org/abs/2401.17632)
- [What Should Not Be Contrastive in Contrastive Learning](https://arxiv.org/abs/2008.05659)
- [With Little Power Comes Great Responsibility](https://arxiv.org/abs/2010.06595)