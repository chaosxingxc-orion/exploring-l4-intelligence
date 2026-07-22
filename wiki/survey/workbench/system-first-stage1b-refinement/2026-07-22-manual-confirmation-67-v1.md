# Manual reproducibility confirmation: 67 papers

> **Priority status: RESOURCE AUDIT ONLY.** The three-axis facts remain available, but reproduction
> routing is superseded by
> [`2026-07-22-speech-omni-agent-reproduction-routing-v2.md`](2026-07-22-speech-omni-agent-reproduction-routing-v2.md).
> For text-only and visual-only papers, data and baseline notes are archival; absorb the method and stop.

Date basis: 2026-07-22. Scope: the exact 67 v4 `MANUAL_REVIEW_ACCESS_AMBIGUOUS` papers.
Ratings are `A` executable, `B` conditional, `C` exact reproduction blocked, and `N` not an
experimental reproduction target. “Local/API” satisfies the requested baseline criterion; exact
historical endpoint drift is disclosed separately. This ledger judges reproducibility and then states
project routing, so a technically reproducible training paper may still be excluded from the frozen
black-box lane.

## 01 — 2303.11366 — Reflexion: Language Agents with Verbal Reinforcement Learning

**Verdict: A — executable; project route: generic transfer.**

- **Technique — YES:** episodic verbal feedback is written into agent memory; no weight update is
  required. The released code and logs are live at `https://github.com/noahshinn/reflexion` (the URL in
  the PDF used an obsolete account path).
- **Data — YES:** HumanEval, MBPP, HotPotQA, and ALFWorld are public; the repository includes the
  paper-specific assets.
- **Baseline — PARTIAL:** local environments and current LLM APIs can run the baseline and Reflexion;
  exact GPT-4-era numbers may drift because the historical endpoint is not frozen.
- **Confirmation:** reproduce the mechanism, not the old API score. Strong transfer prior for external
  feedback/memory, but it needs an audio/omni task adapter.

## 02 — 2309.07701 — Semantic Reconstruction of Continuous Language from MEG Signals

**Verdict: B — conditional; project route: vertical/model-training boundary.**

- **Technique — PARTIAL:** the paper specifies MEG preprocessing, contrastive continuous-word-
  embedding reconstruction, nucleus candidates, and beam search, but releases no decoding code.
- **Data — PARTIAL:** the 3-participant, 10-hour-per-participant Donders narrative MEG collection is
  downloadable with code under the RU-DI-HD-1.0 identifiable-human-data agreement, not frictionless
  public access.
- **Baseline — PARTIAL:** ridge/subject-specific linear baselines are locally implementable; exact GPT
  checkpoint, MEG preprocessing, and compute must be reconstructed.
- **Confirmation:** feasible as a controlled neuro/speech reproduction after DUA approval; it trains
  neural decoders and therefore does not satisfy the frozen-model black-box boundary.

## 03 — 2310.04406 — Language Agent Tree Search Unifies Reasoning, Acting, and Planning in Language Models

**Verdict: A — executable; project route: generic transfer.**

- **Technique — YES:** MCTS, LM value estimates, environment feedback, and self-reflection are fully
  external to the base model; official code is live.
- **Data — YES:** HumanEval, HotPotQA, WebShop, and their environment assets are public.
- **Baseline — YES:** the same agent with no tree search plus local/open or API LMs can be run; exact
  historical API scores may differ.
- **Confirmation:** a good search/control-plane reference. Reuse the search contract, not its text/web
  task assumptions.

## 04 — 2402.15610 — Selective “Selective Prediction”: Reducing Unnecessary Abstention in Vision-Language Reasoning

**Verdict: A — executable; project route: transfer.**

- **Technique — YES:** ReCoVERR asks targeted follow-up questions, gathers high-confidence visual
  evidence, and overrides unnecessary abstention without modifying VLM weights; author code is live.
- **Data — YES:** VQAv2 and A-OKVQA are public.
- **Baseline — PARTIAL:** BLIP-2/InstructBLIP/LLaVA baselines are local; the paper's historical GPT-3.5
  helper can be replaced by a current API, but exact numbers may drift.
- **Confirmation:** directly useful as a selective-evidence/abstention transfer prior, not a speech result.

## 05 — 2403.08978 — AutoGuide: Automated Generation and Selection of Context-Aware Guidelines for Large Language Model Agents

**Verdict: B — conditional; project route: generic transfer.**

- **Technique — PARTIAL:** trajectory failures are converted into context-aware guidelines and selected
  at inference time; the algorithm is clear, but no complete author release was confirmed.
- **Data — YES:** WebArena and the named interactive-task environments are public, although setup is
  container- and credential-heavy.
- **Baseline — PARTIAL:** API agents can reproduce baseline policies, but the exact offline trajectories,
  prompt templates, and historical models need reconstruction.
- **Confirmation:** suitable for a clean-room guideline-memory ablation, not an exact-score target.

## 06 — 2405.16334 — Devil’s Advocate: Anticipatory Reflection for LLM Agents

**Verdict: B — conditional; project route: generic transfer.**

- **Technique — YES:** pre-action “devil’s advocate” reflection is a zero-shot prompting layer and can
  be reimplemented from the paper.
- **Data — YES:** WebArena is public.
- **Baseline — PARTIAL:** the no-reflection agent can run locally or through an API, but GPT-4-0613 is
  no longer an exact stable endpoint and the promised code release was not found.
- **Confirmation:** reproduce as a prompt-level mechanism with a current model and report it as an
  approximate replication.

## 07 — 2405.16854 — Knowing What Not to Do: Leverage Language Model Insights for Action Space Pruning in Multi-Agent Reinforcement Learning

**Verdict: A — executable; project route: exclude from direct lane.**

- **Technique — YES:** eSpark generates and evolves exploration/action-pruning functions, but then
  trains MARL policies; official code is live.
- **Data — YES:** the inventory and traffic scenarios are obtainable with the code/environment stack.
- **Baseline — YES:** standard MARL baselines and an LLM generator can be run locally/API, subject to
  substantial training cost.
- **Confirmation:** reproducible, but it operates on trainable policies and is a boundary comparator,
  not frozen-model inference control.

## 08 — 2406.12304 — COT: A Generative Approach for Hate Speech Counter-Narratives via Contrastive Optimal Transport

**Verdict: B — conditional; project route: vertical/model-training boundary.**

- **Technique — PARTIAL:** OTK features, self-contrastive learning, and target-oriented decoding are
  described, but no complete author implementation was found.
- **Data — YES:** the Reddit and MultiTarget counter-narrative benchmarks are obtainable from their
  original releases, subject to social-media-content terms.
- **Baseline — PARTIAL:** pretrained generation baselines can be fine-tuned locally; exact preprocessing,
  checkpoint, and hyperparameter choices require reconstruction.
- **Confirmation:** a reproducible research direction, not a black-box method; data governance must be
  documented before use.

## 09 — 2407.01476 — Tree Search for Language Model Agents

**Verdict: A — executable; project route: generic transfer.**

- **Technique — YES:** best-first search over actions uses real environment feedback and keeps the base
  model unchanged; code/models are linked from `https://jykoh.com/search-agents/`.
- **Data — YES:** WebArena and VisualWebArena are public, though operationally heavy.
- **Baseline — YES:** a same-agent greedy/no-search baseline is runnable with local models or APIs.
- **Confirmation:** strong test-time search reference; port only after an audio/omni action and verifier
  interface is frozen.

## 10 — 2407.21787 — Large Language Monkeys: Scaling Inference Compute with Repeated Sampling

**Verdict: A — executable; project route: generic transfer.**

- **Technique — YES:** repeated sampling plus selection/verifiers is simple and released in code.
- **Data — YES:** GSM-style math, MATH, CodeContests, MiniF2F, and the released “monkey business”
  artifacts are public.
- **Baseline — YES:** single-sample and best-of-N baselines run with vLLM/open models or APIs.
- **Confirmation:** exact large-N curves are expensive, but a bounded local reproduction is valid and
  directly informs inference-budget scaling.

## 11 — 2410.16670 — CoPS: Empowering LLM Agents with Provable Cross-Task Experience Sharing

**Verdict: A — executable; project route: generic transfer.**

- **Technique — YES:** experiences are extracted, selected, and reused across tasks without changing
  model weights; author code is live.
- **Data — YES:** ALFWorld, WebShop, and HotPotQA are public.
- **Baseline — YES:** no-sharing/memory baselines can run with open Llama-family models or APIs.
- **Confirmation:** a useful external-memory comparator; speech/omni evidence needs a new experience
  schema.

## 12 — 2410.20285 — SWE-Search: Enhancing Software Agents with Monte Carlo Tree Search and Iterative Refinement

**Verdict: A — executable; project route: generic transfer.**

- **Technique — YES:** the MCTS and iterative refinement system is released with the moatless-tools
  stack.
- **Data — YES:** SWE-bench Lite is public with reproducible repository snapshots/containers.
- **Baseline — YES:** standard coding-agent baselines work with open models or external APIs.
- **Confirmation:** operationally heavy but artifact-complete. Use as a search-system engineering prior,
  not as modality evidence.

## 13 — 2501.09732 — Inference-Time Scaling for Diffusion Models beyond Scaling Denoising Steps

**Verdict: B — conditional; project route: non-speech transfer.**

- **Technique — PARTIAL:** candidate/noise search and verifier-based selection are specified, but there
  is no complete paper-specific implementation.
- **Data — YES:** DrawBench-style prompts and ImageNet evaluation resources are obtainable.
- **Baseline — PARTIAL:** open diffusion models can run locally, but some paper configurations rely on
  internal/proprietary generators or reward models and high GPU budgets.
- **Confirmation:** reproduce the scaling law on an open diffusion stack; do not claim the exact paper
  result where the generator/verifier differs.

## 14 — 2502.08266 — Dealing with Annotator Disagreement in Hate Speech Classification

**Verdict: C — exact reproduction blocked; project route: vertical evidence only.**

- **Technique — PARTIAL:** majority/weighted/tie-handling strategies and BERTurk classification are
  sufficiently described.
- **Data — NO:** the exact 11,021 Turkish tweets with per-annotator multi-label/strength annotations are
  described as part of an ongoing project, but no complete exact release was found.
- **Baseline — PARTIAL:** BERTurk can be fine-tuned locally only after obtaining the exact annotations.
- **Confirmation:** reproduce the method on a different disagreement dataset if useful, but the paper's
  tables cannot be independently reproduced from public artifacts.

## 15 — 2502.12110 — A-MEM: Agentic Memory for LLM Agents

**Verdict: A — executable; project route: generic transfer.**

- **Technique — YES:** dynamic note creation, linking, evolution, and retrieval are implemented at
  `https://github.com/WujiangXu/A-mem`.
- **Data — YES:** LoCoMo and the repository examples are public.
- **Baseline — YES:** memory baselines can use Ollama/local models or LiteLLM/API backends.
- **Confirmation:** artifact-complete external memory prior; an audio evidence object and retention
  policy would still be project-specific.

## 16 — 2503.12434 — A Survey on the Optimization of Large Language Model-based Agents

**Verdict: N — not an experimental reproduction target; project route: instrument.**

- **Technique — N/A:** taxonomy/survey, not a new executable method.
- **Data — N/A:** bibliography rather than a released experiment dataset.
- **Baseline — N/A:** no single paper baseline to reproduce.
- **Confirmation:** retain for method vocabulary and backward citation routing only.

## 17 — 2505.18079 — Deep Video Discovery: Agentic Search with Tool Use for Long-form Video Understanding

**Verdict: A — executable; project route: video transfer.**

- **Technique — YES:** official code, a reproduction guide, tool calls, and caption assets are live.
- **Data — YES:** the named long-video benchmarks are obtainable, with source-video licenses and large
  downloads to manage.
- **Baseline — YES:** the agent can use an OpenAI/o-series API or local substitutes; no-tool/search
  controls are implementable.
- **Confirmation:** strong long-context perception/search prior, but video acquisition and API cost make
  it a second-wave transfer.

## 18 — 2506.12721 — Strategic Scaling of Test-Time Compute: A Bandit Learning Approach

**Verdict: B — conditional; project route: generic transfer.**

- **Technique — YES:** the bandit allocation policy is compact enough for clean-room implementation.
- **Data — YES:** MATH-500, AIME 2025, and LiveCodeBench are public; relevant math assets also exist in
  the local corpus inventory.
- **Baseline — YES:** fixed-budget, self-consistency, Qwen, and DeepSeek-family baselines are obtainable.
- **Confirmation:** no author code was found, so implementation equivalence must be checked against the
  paper's pseudocode and allocation schedule.

## 19 — 2506.17417 — Aha Moment Revisited: Are VLMs Truly Capable of Self Verification in Inference-time Scaling?

**Verdict: B — conditional; project route: evaluation instrument.**

- **Technique — YES:** majority sampling, self-verification, and judge-based checks are standard and
  reimplementable.
- **Data — YES:** the visual reasoning benchmarks used by the study are public.
- **Baseline — YES:** open R1-style VLMs and a GPT-4o-class judge/API can be run, with version drift.
- **Confirmation:** no complete paper-specific pipeline was confirmed; reproduce as a diagnostic study,
  not an exact leaderboard score.

## 20 — 2508.01186 — A Survey on Agent Workflow — Status and Future

**Verdict: N — not an experimental reproduction target; project route: instrument.**

- **Technique — N/A:** survey taxonomy only.
- **Data — N/A:** no paper-specific experimental dataset.
- **Baseline — N/A:** no single executable baseline.
- **Confirmation:** use for workflow decomposition and references, not the reproduction queue.

## 21 — 2508.19322 — AT-CXR: Uncertainty-Aware Agentic Triage for Chest X-rays

**Verdict: A — executable; project route: medical/trained-model boundary.**

- **Technique — YES:** the released system combines a trained CXR classifier, Mahalanobis uncertainty,
  and an agentic router.
- **Data — YES:** NIH ChestXray14 is obtainable through its public distribution/Kaggle route, subject to
  the dataset terms.
- **Baseline — YES:** classifier, zero-shot open VLM, and API baselines are runnable.
- **Confirmation:** technically reproducible but depends on supervised medical modeling and does not
  establish a frozen black-box speech/omni control result.

## 22 — 2509.22601 — Learn the Ropes, Then Trust the Wins: Self-imitation with Progressive Exploration for Agentic Reinforcement Learning

**Verdict: A — executable; project route: exclude from direct lane.**

- **Technique — YES:** SPEAR's progressive exploration/self-imitation training code and checkpoints are
  released.
- **Data — YES:** ALFWorld, WebShop, Sokoban, and related environments are public.
- **Baseline — YES:** open agent/RL baselines can run locally, at significant training cost.
- **Confirmation:** artifact-complete training work; retain as a comparator, not a frozen-model method.

## 23 — 2510.13804 — Generative Universal Verifier as Multimodal Meta-Reasoner

**Verdict: A — executable; project route: verifier/training boundary.**

- **Technique — YES:** `https://github.com/Cominclip/OmniVerifier` now contains inference, evaluation,
  training, data-construction, and sequential TTS code.
- **Data — YES:** ViVerBench is public on Hugging Face (3.59k rows, Apache-2.0); the repository contains
  supporting data/pipelines.
- **Baseline — YES:** rule-based and GPT-4.1 model-based evaluation plus open Qwen-family backbones are
  runnable.
- **Confirmation:** fully reproducible as a verifier system, but OmniVerifier itself is trained and is a
  comparator/plugin rather than a pure frozen-black-box control method.

## 24 — 2510.14900 — Mapping Smarter, Not Harder: A Test-Time Reinforcement Learning Agent That Improves Without Labels or Model Updates

**Verdict: C — exact reproduction blocked; project route: conceptual transfer.**

- **Technique — YES:** schema mapping, execution feedback, and test-time experience accumulation are
  external to the LLM and can be prototyped without weight updates.
- **Data — NO:** the load-bearing Trend Micro schemas/logs and production task stream are proprietary
  and were not released.
- **Baseline — YES:** a generic schema-matching agent and GPT-4o/API baseline are implementable on a
  substitute dataset.
- **Confirmation:** the mechanism is copyable, but the paper's empirical result is not independently
  reproducible; any local study would be a transfer experiment.

## 25 — 2511.01082 — GeoToken: Hierarchical Geolocalization of Images via Next Token Prediction

**Verdict: B — conditional; project route: trained-vision boundary.**

- **Technique — PARTIAL:** hierarchical location-token prediction is clear, but the live repository
  explicitly says components and documentation will be updated.
- **Data — PARTIAL:** Im2GPS3k and YFCC4k are obtainable; the MP-16M/MP-16-Pro construction and image
  licensing/preparation are much heavier and not fully turnkey.
- **Baseline — YES:** open geolocation/VLM models and a Gemini/API comparator are available.
- **Confirmation:** evaluation can be approximated now; exact training reproduction remains conditional
  on a complete repository, released splits, and checkpoints.

## 26 — 2511.11793 — MiroThinker: Pushing the Performance Boundaries of Open-Source Research Agents via Model, Context, and Interactive Scaling

**Verdict: A — executable; project route: research-agent/model boundary.**

- **Technique — YES:** agent code and released 72B weights implement model, context, and interactive
  scaling.
- **Data — YES:** GAIA, HLE, BrowseComp, and related benchmarks are obtainable, with benchmark-specific
  licenses/access rules.
- **Baseline — PARTIAL:** open/API research-agent baselines work, but the 72B model, browsing tools, and
  search APIs impose high GPU and service cost.
- **Confirmation:** artifacts exist; reproduce a bounded subset rather than the full model/tool matrix.
  The trained model is outside the direct frozen-black-box method lane.

## 27 — 2511.20297 — Improving Language Agents through BREW: Bootstrapping experientially-learned Environmental knoWledge

**Verdict: B — conditional; project route: generic transfer.**

- **Technique — PARTIAL:** recipe memory and experience-guided MCTS are described well enough for a
  clean-room build, but no author code release was confirmed.
- **Data — YES:** OSWorld, tau2, and SpreadsheetBench are public; each requires a substantial interactive
  environment setup.
- **Baseline — PARTIAL:** agent-memory baselines and APIs are available, but exact environment versions,
  trajectories, and prompts must be reconstructed.
- **Confirmation:** valuable memory/search transfer, not a first exact reproduction target.

## 28 — 2512.11109 — Limits and Gains of Test-Time Scaling in Vision-Language Reasoning

**Verdict: B — conditional; project route: VLM transfer.**

- **Technique — YES:** prompting, best-of-N, self-consistency, refinement, and beam-style inference are
  standard and sufficiently specified.
- **Data — YES:** MathVista, MMMU, MMBench, and the named visual benchmarks are public.
- **Baseline — YES:** open VLMs and API models can run the complete comparison.
- **Confirmation:** no paper-specific code was found and the full model×method matrix is expensive;
  reproduce a preregistered subset with frozen model revisions.

## 29 — 2512.19433 — dMLLM-TTS: Self-Verified and Efficient Test-Time Scaling for Diffusion Multi-Modal Large Language Models

**Verdict: B — conditional; project route: generative-model transfer.**

- **Technique — PARTIAL:** self-verification and adaptive test-time scaling are described, but the paper
  points to the base Lumina-DiMOO stack rather than a complete separate release.
- **Data — YES:** GenEval and the named evaluation prompts are public.
- **Baseline — YES:** Lumina-DiMOO, MMaDA/Muddit-style open models and API comparators are obtainable.
- **Confirmation:** method reproduction is feasible with high GPU cost; exact equivalence depends on
  reconstructing the unreleased orchestration/configuration layer.

## 30 — 2512.20745 — AgentMath: Empowering Mathematical Reasoning for Large Language Models via Tool-Augmented Agent

**Verdict: C — exact reproduction blocked; project route: training boundary.**

- **Technique — PARTIAL:** the SFT, tool-use, and RL stages are described conceptually, but not as a
  complete executable recipe.
- **Data — PARTIAL:** AIME/HMMT-style evaluation sets are public; the synthetic training corpus and
  exact trajectories are not fully released.
- **Baseline — YES:** open math models and external APIs can run evaluation baselines.
- **Confirmation:** inference evaluation may be approximated, but full paper reproduction is blocked by
  missing training artifacts and large-scale training cost.

## 31 — 2512.21815 — High-Entropy Tokens as Multimodal Failure Points in Vision-Language Models

**Verdict: B — conditional; project route: gray-box boundary.**

- **Technique — PARTIAL:** entropy localization and PGD-style attacks are described, but require token
  probabilities/gradients and no complete author release was confirmed.
- **Data — YES:** COCO/TextVQA-derived subsets are public.
- **Baseline — YES:** Qwen-VL, InternVL, and LLaVA-family models can be run locally.
- **Confirmation:** locally reproducible with model internals and GPU resources, but it violates the
  strict output-only black-box assumption and should remain a falsifier/comparator.

## 32 — 2601.05777 — EET: Experience-Driven Early Termination for Cost-Efficient Software Engineering Agents

**Verdict: A — executable; project route: generic stopping transfer.**

- **Technique — YES:** early-termination logic, prompts, and experience features are released in code.
- **Data — YES:** SWE-bench Verified and the repository's evaluation assets are public.
- **Baseline — YES:** underlying software agents and local/API model backends are supported.
- **Confirmation:** artifact-complete reference for stopping and cost control; modality/environment
  adaptation is still required.

## 33 — 2601.05930 — Can We Predict Before Executing Machine Learning Agents?

**Verdict: A — executable; project route: predictor/instrument transfer.**

- **Technique — YES:** FOREAGENT's pre-execution success prediction and features are released.
- **Data — YES:** the 18,438-run corpus is public with the code; MLE-Bench/Kaggle tasks are obtainable
  under their competition licenses.
- **Baseline — YES:** agent-framework/API baselines can be executed.
- **Confirmation:** reproducible but operationally expensive; use the released run corpus first rather
  than rerunning every Kaggle task.

## 34 — 2601.09667 — Collaborative Multi-Agent Test-Time Reinforcement Learning for Reasoning

**Verdict: B — conditional; project route: generic multi-agent transfer.**

- **Technique — YES:** MATTRL's textual experience exchange and test-time collaboration can be rebuilt
  from the paper without weight updates.
- **Data — YES:** RareBench, SuperGPQA, and the named reasoning benchmarks are obtainable.
- **Baseline — YES:** single-agent/multi-agent baselines can use open models or APIs.
- **Confirmation:** the linked repository was README-only/one-commit in this audit, so this is a
  clean-room reproduction despite a reachable GitHub URL.

## 35 — 2601.15625 — Robust Tool Use via Fission-GRPO: Learning to Recover from Execution Errors

**Verdict: A — executable; project route: training boundary.**

- **Technique — YES:** the GRPO training and execution-error recovery recipe is released.
- **Data — YES:** BFCL v4 is public and a matching benchmark asset exists in the local inventory.
- **Baseline — YES:** Qwen3-family local models and Claude/API comparisons are available.
- **Confirmation:** technically reproducible with high RL/GPU cost, but it changes model weights and is
  not a direct frozen black-box method.

## 36 — 2602.00028 — ELLMPEG: An Edge-based Agentic LLM Video Processing Tool

**Verdict: A — executable; project route: tool-system transfer.**

- **Technique — YES:** `https://github.com/zoha-az/ELLMPEG` releases the edge agent/tool pipeline.
- **Data — YES:** the prompt/task set is released or reconstructable from the repository; FFmpeg/VVenC
  tools and documentation are public.
- **Baseline — YES:** Qwen local and GPT/API baselines can run.
- **Confirmation:** reproducible edge/tool orchestration prior; not speech-specific, but useful for
  constrained tool execution and cost accounting.

## 37 — 2602.01070 — What If We Allocate Test-Time Compute Adaptively?

**Verdict: B — conditional; project route: generic allocation transfer.**

- **Technique — YES:** verifier-conditioned adaptive allocation is specified sufficiently for a
  clean-room implementation.
- **Data — YES:** MATH, AIME, and olympiad-style benchmarks are public.
- **Baseline — YES:** Llama/Qwen-family models, PRMs, fixed-budget sampling, and self-consistency are
  locally reproducible.
- **Confirmation:** no complete author code was found; freeze all thresholds and verifier revisions
  before comparing allocation curves.

## 38 — 2602.01331 — A-MapReduce: Executing Wide Search via Agentic MapReduce

**Verdict: A — executable; project route: generic search transfer.**

- **Technique — YES:** wide-search decomposition, map, and reduce orchestration are released in code.
- **Data — YES:** WideSearch/DeepWideSearch-style tasks and prompts are obtainable; live-web results
  require a dated search snapshot or service logging.
- **Baseline — YES:** o3/Gemini-class APIs and alternative local/API agents can run.
- **Confirmation:** code-complete but network/API dependent; preserve query, result, and model receipts
  to make the reproduction auditable.

## 39 — 2602.03219 — Beyond Quantity: Trajectory Diversity Scaling for Code Agents

**Verdict: C — exact reproduction blocked; project route: conceptual transfer.**

- **Technique — PARTIAL:** the diversity-scaling hypothesis and selection measures are understandable,
  but the full generation/training pipeline is not released.
- **Data — NO:** the synthetic trajectory corpus and custom MCP business-task cluster are unavailable.
- **Baseline — PARTIAL:** BFCL, tau2, and BIRD evaluation tasks are public, but they do not reconstruct
  the missing training distribution.
- **Confirmation:** test the hypothesis on a new corpus if desired; do not claim the paper's training or
  scaling result is reproducible.

## 40 — 2602.13218 — Scaling the Scaling Logic: Agentic Meta-Synthesis of Logic Reasoning

**Verdict: A — executable; project route: generic/meta-synthesis transfer.**

- **Technique — YES:** the repository releases the meta-synthesis pipeline and quick-start path.
- **Data — YES:** its 400 seeds, 953 generated families, and roughly 21k instances are available through
  the project pipeline/assets.
- **Baseline — YES:** OpenAI-compatible APIs or other model backends can run; downstream GRPO is
  optional and compute-heavy.
- **Confirmation:** reproduce the inference/data-construction path separately from any weight-updating
  downstream experiment.

## 41 — 2602.16485 — Team of Thoughts: Efficient Test-time Scaling of Agentic Systems through Orchestrated Tool Calling

**Verdict: A — executable; project route: generic transfer.**

- **Technique — YES:** official code implements role/team orchestration and tool calling.
- **Data — YES:** the math/code reasoning benchmarks are public.
- **Baseline — YES:** the supported open/API model matrix and single-agent controls are runnable.
- **Confirmation:** a strong external orchestration comparator; API cost and model-version receipts are
  the main reproducibility controls.

## 42 — 2602.22406 — Towards Autonomous Memory Agents

**Verdict: B — conditional; project route: memory transfer.**

- **Technique — PARTIAL:** U-Mem's memory actions and autonomous maintenance loop are described, but the
  anonymized repository exposed very little verifiable content in this audit.
- **Data — YES:** HotPotQA, AIME, and AdvancedIF-style evaluations are public.
- **Baseline — YES:** Qwen/Gemini/API memory-agent baselines can run.
- **Confirmation:** clean-room implementation is possible; wait for a stable non-anonymous release for
  exact artifact reproduction.

## 43 — 2603.01692 — Reasoning as Gradient: Scaling MLE Agents Beyond Tree Search

**Verdict: A — executable; project route: research-agent transfer.**

- **Technique — YES:** the Gome/RD-Agent implementation and example traces are live.
- **Data — YES:** MLE-Bench/Kaggle competitions are obtainable under their licenses.
- **Baseline — YES:** frontier-model APIs and comparable research agents can run.
- **Confirmation:** artifact-complete but expensive and environment-sensitive; use a bounded competition
  subset with frozen containers and API receipts.

## 44 — 2603.09821 — One-Eval: An Agentic System for Automated and Traceable LLM Evaluation

**Verdict: A — executable; project route: evaluation instrument.**

- **Technique — YES:** active repository includes evaluation orchestration, tracing, tests, and a
  reusable skill/interface.
- **Data — YES:** public benchmarks are automatically downloaded or linked by the project.
- **Baseline — YES:** local and API models are supported.
- **Confirmation:** high-value reproducible evaluation infrastructure, but not itself a control-plane
  method to compare for scientific effect.

## 45 — 2603.12109 — On Information Self-Locking in Reinforcement Learning for Active Reasoning of LLM Agents

**Verdict: A — executable; project route: training boundary.**

- **Technique — YES:** the T3 repository releases the active-reasoning/RL implementation.
- **Data — YES:** PE, MediQ, FloDial, and associated task assets are available through the project or
  their original releases.
- **Baseline — YES:** open Qwen-family models and o-series/API comparators are available.
- **Confirmation:** reproducible with substantial training cost, but it updates weights and remains a
  boundary comparator rather than direct frozen-model control.

## 46 — 2604.06066 — From Hallucination to Structure Snowballing: The Alignment Tax of Constrained Decoding in LLM Reflection

**Verdict: B — conditional; project route: diagnostic transfer.**

- **Technique — YES:** structured self-critique/constrained-decoding comparisons are described and can
  be implemented without training the evaluated model.
- **Data — YES:** BIG-Bench Mistake and the reported evaluation inputs are public.
- **Baseline — YES:** unconstrained reflection/Reflexion-style baselines can use current local or API
  models.
- **Confirmation:** the PDF claims code/raw logs, but the linked GitHub page was not reliably readable in
  this audit. Treat as conditional until a commit and assets are cloned; API drift still affects exactness.

## 47 — 2604.11025 — Test-time Scaling over Perception: Resolving the Grounding Paradox in Thinking with Images

**Verdict: B — conditional; project route: VLM transfer.**

- **Technique — PARTIAL:** perception-grounded scaling is sufficiently described for reimplementation,
  but no complete author code release was confirmed.
- **Data — YES:** the named visual reasoning/perception benchmarks are public.
- **Baseline — YES:** open VLMs and API models support no-scaling and standard TTS controls.
- **Confirmation:** feasible as a bounded clean-room VLM study; it is not speech evidence and the full
  model/benchmark matrix is compute-heavy.

## 48 — 2604.16529 — Scaling Test-Time Compute for Agentic Coding

**Verdict: B — conditional; project route: generic scaling transfer.**

- **Technique — YES:** repeated attempts/search/budget scaling over coding agents can be reconstructed
  from the experimental protocol.
- **Data — YES:** SWE-bench Verified and Terminal-Bench are public but container-heavy.
- **Baseline — PARTIAL:** current Claude, Gemini, and GPT APIs can run analogous agents; the exact dated
  proprietary checkpoints in the paper may no longer be callable.
- **Confirmation:** reproduce trends with frozen current endpoints, not exact historical scores; no
  complete paper-specific code was confirmed.

## 49 — 2605.06457 — Beyond Task Success: Measuring Workflow Fidelity in LLM-Based Agentic Payment Systems

**Verdict: C — exact reproduction blocked; project route: evaluation instrument only.**

- **Technique — YES:** the workflow-fidelity metric and scoring logic are simple to reimplement.
- **Data — NO:** the load-bearing HMASP collection of roughly 90k payment-task instances/workflows was
  not released.
- **Baseline — YES:** Ollama/open models and official OpenAI APIs can run on a substitute payment suite.
- **Confirmation:** the metric is reusable, but the paper's empirical tables cannot be reproduced
  without HMASP and its execution environment.

## 50 — 2605.12894 — Beyond Cooperative Simulators: Generating Realistic User Personas for Robust Evaluation of LLM Agents

**Verdict: C — exact reproduction blocked; project route: environment-design evidence.**

- **Technique — PARTIAL:** evolutionary persona/program search is conceptually reproducible.
- **Data — NO:** evolved persona programs, human annotations, and key generation traces were not
  released.
- **Baseline — PARTIAL:** tau2 retail/airline environments and LLM APIs are public, but they do not
  reconstruct the missing persona distribution.
- **Confirmation:** a new persona study can test the idea; the published effect size is not exactly
  reproducible.

## 51 — 2605.12978 — Useful Memories Become Faulty When Continuously Updated by LLMs

**Verdict: C — exact reproduction blocked; project route: memory-risk evidence.**

- **Technique — PARTIAL:** repeated memory-update and erosion tests are understandable, but no complete
  author implementation was found.
- **Data — PARTIAL:** ALFWorld, ScienceWorld, WebShop, AppWorld, and Mind2Web are public; the synthetic
  ARC-AGI Stream and exact update traces were not confirmed as released.
- **Baseline — PARTIAL:** current local/API models can run an analogous study, but the paper's dated
  GPT-5.4-class configuration is not a stable reproducible endpoint.
- **Confirmation:** reproduce the failure mode on a newly frozen stream; exact paper replication remains
  blocked.

## 52 — 2605.22511 — Search-E1: Self-Distillation Drives Self-Evolution in Search-Augmented Reasoning

**Verdict: C — exact reproduction blocked; project route: training boundary.**

- **Technique — PARTIAL:** self-distillation/search-augmented GRPO is described, but the PDF only says
  code will be released and no live author release was found.
- **Data — YES:** public QA/search-reasoning evaluation benchmarks are obtainable.
- **Baseline — YES:** Qwen 3B/7B and standard search/RL baselines are available.
- **Confirmation:** evaluation concepts are reproducible, but full training needs missing code,
  trajectories, and large compute; recheck the release before any execution plan.

## 53 — 2605.23989 — Towards Trustworthy Agentic AI: A Comprehensive Survey of Safety, Robustness, Privacy, and System Security

**Verdict: N — not an experimental reproduction target; project route: safety instrument.**

- **Technique — N/A:** survey/taxonomy rather than a new executable system.
- **Data — N/A:** no paper-specific experiment dataset.
- **Baseline — N/A:** no single baseline to reproduce.
- **Confirmation:** retain for threat-model, falsifier, and bibliography coverage.

## 54 — 2605.24481 — OmniEgo-R2: A Routed Reasoning Framework for the 1st Cross-Domain EgoCross Challenge at CVPR 2026

**Verdict: B — conditional; project route: omni/competition boundary.**

- **Technique — YES:** released code implements routing and reasoning over the challenge domains.
- **Data — PARTIAL:** EgoCross challenge data and splits require the competition's access route; not all
  assets are in the local lock.
- **Baseline — YES:** Qwen3-VL-family checkpoints and API/open comparators are obtainable.
- **Confirmation:** deployment is reproducible if challenge data/weights are granted; the pipeline
  depends on domain SFT checkpoints and is not a pure frozen-foundation-model method.

## 55 — 2605.28192 — Agentic Active Omni-Modal Perception for Multi-Hop Audio-Visual Reasoning

**Verdict: C — exact reproduction blocked; project route: high-priority conditional direct-like watch.**

- **Technique — YES:** AOP-Agent's hierarchical omni-memory and observe–reflect–replan loop are
  training-free, use open Omni-LLMs, and are detailed enough for a prototype.
- **Data — NO:** the newly introduced 519-question MOV-Bench was not found as a downloadable author
  release; it is not in the local lock. OmniVideoBench alone cannot reproduce the main result.
- **Baseline — YES:** open Omni-LLMs and a no-active-perception baseline can run locally.
- **Confirmation:** method fit is high, artifact readiness is not. Keep on the direct-neighbor watchlist,
  but do not schedule exact reproduction until MOV-Bench/code appear.

## 56 — 2605.29568 — DeepTool: Scaling Interleaved Deliberation in Tool-Integrated Reasoning via Process-Supervised Reinforcement Learning

**Verdict: C — exact reproduction blocked; project route: training boundary.**

- **Technique — PARTIAL:** SFT plus process-supervised RL and interleaved tool deliberation are
  described, but no complete code/model/data release was found.
- **Data — NO:** MOSAIC process traces and the load-bearing training corpus are unavailable; public math
  evaluation sets do not replace them.
- **Baseline — YES:** Qwen base models, tool agents, and math benchmarks are obtainable.
- **Confirmation:** baseline evaluation is possible, but the trained DeepTool result cannot be recreated
  from released resources.

## 57 — 2606.01667 — ATLAS: Agentic Test-time Learning-to-Allocate Scaling

**Verdict: B — conditional; project route: generic allocation transfer.**

- **Technique — YES:** prompts, allocation logic, and implementation details in the appendix are enough
  for a clean-room build; no weight update is required.
- **Data — YES:** HLE-Verified, LiveCodeBench, GPQA, and BabyVision-style evaluations are obtainable.
- **Baseline — YES:** Claude Sonnet 4.6/API and alternative model backends can run fixed-budget controls.
- **Confirmation:** no live author code was found; exact results remain sensitive to endpoint/version,
  prompt, and API cost, but the method itself is reproducible.

## 58 — 2606.01770 — Adaptive Auto-Harness: Sustained Self-Improvement for Agentic System Deployment on Open-Ended Task Streams

**Verdict: C — exact reproduction blocked; project route: deployment evidence.**

- **Technique — PARTIAL:** harness adaptation and sustained self-improvement are described, but the PDF's
  “Code is available in Link” text did not resolve to a usable release.
- **Data — NO:** prediction/security/event streams depend on proprietary endpoints, credentials, and
  human steering; the exact task stream is unavailable.
- **Baseline — PARTIAL:** a substitute open stream and API agent could test the concept, not the paper's
  deployment result.
- **Confirmation:** retain as an environment/rollback design reference only until code and a replayable
  stream are released.

## 59 — 2606.08231 — Test-Time Scaling in Multimodal Foundation Models: A Comprehensive Survey of Generation and Reasoning

**Verdict: N — not an experimental reproduction target; project route: TTS instrument.**

- **Technique — N/A:** survey/taxonomy.
- **Data — N/A:** no unique experimental dataset.
- **Baseline — N/A:** no single baseline implementation.
- **Confirmation:** use to normalize terminology and route primary papers.

## 60 — 2606.08450 — GIFT: LLM-Guided State-Reward Interface for Financial Reinforcement Learning

**Verdict: A — executable; project route: finance/RL boundary.**

- **Technique — YES:** live code includes the LLM-guided state/reward interface, configs, and tests.
- **Data — YES:** the repository does not bundle data but provides a downloader for the public FINSABER
  Hugging Face price dataset.
- **Baseline — YES:** PPO/local RL and an LLM endpoint can be run.
- **Confirmation:** technically reproducible after data fetch; it trains an RL policy in a finance
  vertical and is not a direct frozen-omni experiment.

## 61 — 2606.08728 — Artificial Intelligence for Mathematical Reasoning: An Integrated Survey of Language Models, Neuro-symbolic Systems, and Verified Discovery

**Verdict: N — not an experimental reproduction target; project route: instrument.**

- **Technique — N/A:** integrated survey rather than a new method.
- **Data — N/A:** bibliography/taxonomy only.
- **Baseline — N/A:** no single experimental baseline.
- **Confirmation:** retain for formal-verification and math-tool references.

## 62 — 2606.08850 — Intrinsic Selection and Particle Resampling for Inference-Time Scaling Beyond Domain Verifiability

**Verdict: B — conditional; project route: gray-box transfer.**

- **Technique — PARTIAL:** adjusted tail entropy and particle resampling are implementable, but require
  token log-probabilities/model internals not exposed by every black-box API; no author code was found.
- **Data — YES:** math, GPQA, and CAD-style evaluation tasks are public.
- **Baseline — PARTIAL:** open local models support log-probabilities and self-consistency baselines;
  output-only APIs may not.
- **Confirmation:** reproducible on local/open models, but it is a gray-box comparator unless the chosen
  external API exposes stable logprobs.

## 63 — 2606.11543 — SkillJuror: Measuring How Agent Skill Organization Changes Runtime Behavior

**Verdict: A — executable; project route: evaluation/KB instrument.**

- **Technique — YES:** the live repository implements skill-bundle construction and runtime-behavior
  measurement.
- **Data — YES:** controlled skills/tasks are provided or generated through the repository workflow.
- **Baseline — YES:** unorganized/alternative skill layouts can be evaluated with supported APIs.
- **Confirmation:** reproducible and relevant to knowledge/skill organization, but it measures an agent
  system rather than serving as the core inference-control method.

## 64 — 2606.15141 — EChO-Agent: Evidence Chain Orchestration Agent for Audio Reasoning

**Verdict: A — executable clean-room; project route: conditional direct candidate.**

- **Technique — PARTIAL:** no author repository was found, but the PDF fully specifies the external
  Tool → Evidence → Reason → Verify pipeline, static question-conditioned dispatch, retries, structured
  evidence operations, two reasoning passes, and arbitration; no weight update is used.
- **Data — YES:** MMAR is present in the local data inventory.
- **Baseline — YES:** the same Qwen3-Omni-Instruct backbone without tools is the primary baseline;
  YAMNet, Whisper, SpeechBrain SER, Essentia, DeepSeek-V3, and Qwen3-Omni are open or API-accessible.
- **Confirmation:** this is the only 67-paper item promoted into the direct reproduction queue. Label the
  first build “clean-room” and freeze inferred prompts/tool thresholds separately from paper-specified choices.

## 65 — 2606.19341 — Native Active Perception as Reasoning for Omni-Modal Understanding

**Verdict: A — executable; project route: trained-omni boundary.**

- **Technique — YES:** OmniAgent code plus SFT/RL weights are released; the active-perception behavior
  is native to the trained model.
- **Data — YES:** the training mix is constructed from five named obtainable datasets and evaluation uses
  ten public benchmarks.
- **Baseline — YES:** Qwen base/open omni models and published checkpoints can be run.
- **Confirmation:** deployment/evaluation is reproducible from released weights; reproducing training is
  costly, and the core method modifies weights, so use it as a comparator rather than direct control.

## 66 — 2606.28864 — On Test-Time Scaling for Vision-Language Models

**Verdict: B — conditional; project route: VLM transfer.**

- **Technique — YES:** nine standard inference-time methods are fully enumerated and require no weight
  changes.
- **Data — YES:** MMStar, RealWorldQA, HallusionBench, WeMath, LogicVista, and A-OKVQA are public.
- **Baseline — YES:** Qwen2.5/3-VL, InternVL3.5, and Molmo2 families are open; the full 13-model matrix is
  GPU-heavy.
- **Confirmation:** no paper-specific code was confirmed, but a bounded local replication is sound. Its
  `TTS` acronym is test-time scaling, not text-to-speech; it adds no speech-specific evidence.

## 67 — 2606.30774 — What Drives Interactive Improvement from Feedback?

**Verdict: B — conditional; project route: feedback-evaluation transfer.**

- **Technique — YES:** the controlled student–teacher framework separates feedback benefit from retry,
  format correction, and extra-compute effects; the paper links a project-page release.
- **Data — YES:** Omni-MATH, the Competitive-Coding-Benchmark/Codeforces assets, and BBEH Linguini are
  public.
- **Baseline — YES:** repeated attempts, self-refinement, open Gemma/Llama/Qwen/GPT-OSS models, and API
  teachers are runnable.
- **Confirmation:** strong evaluation prior for any feedback controller, but this audit did not verify a
  cloneable source repository behind the project page. Treat as clean-room/conditional, freeze endpoints,
  and use a bounded model subset rather than the costly full matrix.

## Ledger totals

- A — executable: **28** (`01, 03, 04, 07, 09–12, 15, 17, 21–23, 26, 32–33, 35–36, 38,
  40–41, 43–45, 60, 63–65`).
- B — conditional: **23** (`02, 05–06, 08, 13, 18–19, 25, 27–29, 31, 34, 37, 42, 46–48,
  54, 57, 62, 66–67`).
- C — exact blocked: **11** (`14, 24, 30, 39, 49–52, 55–56, 58`).
- N — not an experiment target: **5** (`16, 20, 53, 59, 61`).
