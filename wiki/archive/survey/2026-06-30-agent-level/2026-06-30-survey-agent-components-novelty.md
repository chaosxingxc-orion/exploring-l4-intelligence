> **🗄 ARCHIVED (2026-07-11)** — 已收官战役过程件（2026-06-30 agent-level 调研），仅作历史，非现行真源。

# S1 · Lane A5 — Model classes as agent components + novelty-delta (B5/B7)

> Part of **S1** (decisive probe) of [[2026-06-30-agent-level-synthesis]] — strategic survey for [[2026-06-26-training-free-rl-for-speech-omni-research-proposal]]. Run `wf_8452c9ae-a11`, 2026-06-30. Per-lane adversarial verification; only `keep=true` claims archived; links real & verifiable. Each claim is scope-tagged (no-gradient = in scope vs weight-updating = out).


**Lane summary.** Lane A5 surveys the two model classes as agent components and benchmarks the novelty of a training-free, no-gradient, self-evolving SPEECH/omni agent that pairs an embedding-memory with a generative-policy.

(1) EMBEDDING/RETRIEVAL models as MEMORY: the RAG pattern (Lewis 2020) established embeddings as "non-parametric memory" via a dense vector index + neural retriever. Frozen-LLM agent-memory architectures built on this — Generative Agents (observation→reflection→importance-weighted embedding retrieval), MemGPT (LLM-as-OS hierarchical paging) — are no-gradient and already split episodic vs semantic memory. Crucially, the "vector/embedding omni → agent memory" component is now a real, off-the-shelf model class: Omni-Embed-Nemotron and Omni-Embed-Audio are bi-encoder retrieval models over text/image/audio/video, and WavRAG does native-audio RAG with Qwen-Audio embeddings. So B5's claim that a vector/embedding omni is a natural agent MEMORY is directly supported by deployed models.

(2) GENERATIVE LLMs as POLICY/skill: Voyager (skill library of executable code, GPT-4 blackbox, no fine-tuning), Reflexion (verbal RL, episodic reflection buffer, no weight update), and ExpeL (cross-task experience pool + extracted insights, no parameter updates) are the canonical no-gradient "generative LLM as self-improving policy + skill/experience store" works. ADAS (meta-agent programs new agents over a code archive), DSPy (declarative pipeline compilation; mostly prompt-level), and TextGrad (textual "gradients") show the composition/optimization layer, all without gradients on the base model.

(3) COMPOSITION + the no-gradient/weight-updating line: the Self-Evolving Agents survey (2507.21046) formalizes evolution across components (model/memory/tools/architecture) and separates in-context/memory evolution (IN scope) from parameter evolution (OUT). Very recent general-domain frameworks — MUSE-Autoskill, MemSkill — already implement the EXACT recipe of training-free memory + skill-library + verifiable (unit-test) triggers, and even cross-agent skill transfer.

NOVELTY-DELTA (honest): The MECHANISM (frozen weights + evolving external memory/skill state + verifiable reward) is NOT novel — it is a crowded, fast-moving frontier in text/code/embodied agents (Reflexion 2023 → MUSE-Autoskill/MemSkill 2026). What is UNOCCUPIED is the DOMAIN + COMPONENT-PAIRING instantiation: (a) doing it in SPEECH/omni with paralinguistic state (speaker/emotion/turn-taking/full-duplex) as both memory keys AND reward signals; (b) literally pairing a VECTOR-OMNI embedding model (e.g. Omni-Embed-Nemotron) as the agent memory bi-encoder with a GENERATIVE thinker-talker omni as the policy — a two-omni-model agent; (c) driving accumulation with verifiable SPEECH rewards (WER/ASR/ST/SER/SID) instead of text unit-tests. Speech agents today are EVALUATED (EVA-Bench's EVA-X "Experience" metric, VoiceAssistant-Eval multi-round) but as STATIC systems; speech retrieval (WavRAG, omni-embed) is single-shot RAG, not a self-evolving episodic memory closed-looped to a self-improving policy. No work was found that closes that loop in speech. VERDICT: the combination is novel as a transfer-and-specialize contribution (B7 = moderately novel, defensible), NOT as a new mechanism. B5 is resolved positively: both omni model classes map cleanly onto memory and policy roles, and both component types already exist for audio. The framing should claim "first to instantiate the no-gradient self-evolving agent recipe in speech/omni with a vector-omni memory + generative-omni policy and verifiable speech rewards," and must explicitly cite the general-agent prior art to avoid over-claiming mechanism novelty.


**Adversarial verifier assessment.** All 13 claims' sources web-resolve to real papers — including the future-dated 2026 arXiv IDs (Omni-Embed-Audio 2604.18360, MUSE-Autoskill 2605.27366, MemSkill 2602.02474, EVA-Bench 2605.13841), which are genuine in this timeline, not fabricated. The lane's core thesis (B5 component-mapping + B7 transfer-novelty) is well-supported and, importantly, HONEST: it repeatedly self-flags that the mechanism is not novel and that audio components exist only separately, and it correctly tags weight-updating priors (RAG, the omni-embedders' training, DSPy) as mixed rather than no-gradient. One scope error: A5-11 mischaracterizes MemSkill as "training-free / no-gradient." MemSkill's full text states it trains a lightweight MLP controller via PPO ("We train the controller with reinforcement learning"; base LLM/executor frozen) — so it is a MIXED method (frozen base LLM + gradient-trained auxiliary controller), exactly the weight-updating line the program rules OUT. The claim's load-bearing point (the recipe is already implemented in general-domain agents, bounding novelty) still stands via MUSE-Autoskill, which IS genuinely training-free ("a single training-free framework"), so A5-11 is kept but with supported=false pending the MemSkill correction. Minor non-fatal caveats: A5-4 says "Qwen-Audio" where WavRAG actually builds on Qwen2-Audio; A5-10 attributes the Self-Evolving survey to "Su et al." while the resolved paper's lead authors are Gao/Geng/Hua et al. (title+ID correct, so resolution unaffected). The novelty-delta verdict (A5-13) is appropriately hedged ("first, to our knowledge"; transfer-and-specialize, not mechanism-novel) and does not depend on the MemSkill error. Net: B5 resolves positively (both omni classes map to memory/policy and off-the-shelf audio components exist); B7's "moderately novel via domain+component-pairing, must cite general-agent prior art" is defensible.


---

## Verified claims & sources (13 kept / 13 total)


### A5-1 · definitional · scope: mixed · confidence: high

The RAG pattern established embeddings as agent MEMORY: a model combines parametric (seq2seq) memory with non-parametric memory = a dense vector index accessed by a neural retriever (bi-encoder), the foundational 'embedding-as-external-memory' template every agent-memory architecture reuses.


- **Sources:** [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401)

- **Relevance:** B5 (vector/embedding model as the memory component)


### A5-2 · empirical · scope: no-gradient · confidence: high

Frozen-LLM agent MEMORY architectures already implement episodic+semantic memory via embedding retrieval with NO weight updates, validating that an embedding store is a drop-in agent memory: Generative Agents use an observation→reflection→importance-weighted embedding-retrieval memory stream; MemGPT manages hierarchical OS-style memory tiers around a frozen LLM.


- **Sources:** [Generative Agents: Interactive Simulacra of Human Behavior](https://arxiv.org/abs/2304.03442) · [MemGPT: Towards LLMs as Operating Systems](https://arxiv.org/abs/2310.08560)

- **Relevance:** B5 (memory component is no-gradient and already episodic/semantic)


### A5-3 · empirical · scope: mixed · confidence: high

The 'vector/embedding OMNI → agent memory' component of B5 is now a real, off-the-shelf model class: Omni-Embed-Nemotron and Omni-Embed-Audio are bi-encoder retrieval models that embed text/image/audio/video into a shared space for RAG, i.e. exactly an omni agent MEMORY encoder.


- **Sources:** [Omni-Embed-Nemotron: A Unified Multimodal Retrieval Model for Text, Image, Audio, and Video](https://arxiv.org/abs/2510.03458) · [Omni-Embed-Audio: Leveraging Multimodal LLMs for Robust Audio-Text Retrieval](https://arxiv.org/abs/2604.18360)

- **Relevance:** B5 (vector-omni is a deployable MEMORY component)


### A5-4 · empirical · scope: no-gradient · confidence: high

Speech-modality retrieval already exists but only as SINGLE-SHOT RAG, not as a self-evolving episodic memory: WavRAG does native-audio retrieval-augmentation of spoken dialogue using Qwen-Audio embeddings, bypassing ASR. This is augmentation, not an accumulating agent memory closed-looped to a self-improving policy.


- **Sources:** [WavRAG: Audio-Integrated Retrieval Augmented Generation for Spoken Dialogue Models](https://arxiv.org/abs/2502.14727)

- **Relevance:** B5 (audio memory exists) / B7 (but not self-evolving — a gap)


### A5-5 · empirical · scope: no-gradient · confidence: high

Voyager is the canonical 'generative LLM as POLICY + growing SKILL library' done no-gradient: a frozen GPT-4 queried as a blackbox accumulates an ever-growing library of executable-code skills that are retrieved and composed, with no parameter fine-tuning — the direct template for a generative-omni policy with a skill store (B5).


- **Sources:** [Voyager: An Open-Ended Embodied Agent with Large Language Models](https://arxiv.org/abs/2305.16291)

- **Relevance:** B5 (generative model as policy + skill library)


### A5-6 · empirical · scope: no-gradient · confidence: high

Reflexion establishes verbal/no-gradient reinforcement with VERIFIABLE reward: an agent reflects on task feedback and stores the reflection in an episodic memory buffer that conditions later trials — no weight update — and it works precisely when feedback is verifiable (e.g. unit tests pass/fail).


- **Sources:** [Reflexion: Language Agents with Verbal Reinforcement Learning](https://arxiv.org/abs/2303.11366)

- **Relevance:** B5/B7 (no-gradient policy improvement via memory + verifiable reward)


### A5-7 · empirical · scope: no-gradient · confidence: high

ExpeL shows CROSS-EPISODE skill/experience accumulation with no parameter updates: an experience pool gathered by trial-and-error is distilled into reusable natural-language insights and successful trajectories that augment a frozen agent on unseen tasks — off-policy-style learning entirely in external state.


- **Sources:** [ExpeL: LLM Agents Are Experiential Learners](https://arxiv.org/abs/2308.10144)

- **Relevance:** B5/B7 (experience/skill accumulation, no-gradient)


### A5-8 · empirical · scope: no-gradient · confidence: high

ADAS extends the no-gradient frontier to AGENT-SYSTEM design: a meta-agent programs new agentic systems in code over an ever-growing archive (Meta Agent Search), discovering prompts/tools/workflows that beat hand-designed agents — composition/architecture is the evolving state, base weights are frozen.


- **Sources:** [Automated Design of Agentic Systems](https://arxiv.org/abs/2408.08435)

- **Relevance:** B5/B7 (architecture/composition as evolving no-gradient state)


### A5-9 · empirical · scope: mixed · confidence: high

DSPy and TextGrad are the optimization layer over compound LLM systems. DSPy compiles declarative LM pipelines, optimizing mainly demonstrations/prompts (no-gradient core, with OPTIONAL finetuning → mixed); TextGrad backpropagates textual 'gradients' (LLM feedback) to improve components of a compound AI system without any real gradient on the base model.


- **Sources:** [DSPy: Compiling Declarative Language Model Calls into Self-Improving Pipelines](https://arxiv.org/abs/2310.03714) · [TextGrad: Automatic "Differentiation" via Text](https://arxiv.org/abs/2406.07496)

- **Relevance:** B5/B7 (system-level optimization; DSPy mixed, TextGrad no-gradient)


### A5-10 · definitional · scope: mixed · confidence: high

The Self-Evolving Agents survey formalizes exactly the scope line this program needs: evolution can target model / memory / tools / architecture, and methods split into IN-CONTEXT/memory/tool/architecture evolution (no-gradient, IN scope) versus PARAMETER evolution (weight-updating, OUT of scope). This gives a citable taxonomy for the no-gradient frontier.


- **Sources:** [A Survey of Self-Evolving Agents: What, When, How, and Where to Evolve on the Path to Artificial Super Intelligence](https://arxiv.org/abs/2507.21046)

- **Relevance:** B5/B7 (taxonomy anchoring the no-gradient vs weight-updating boundary)


### A5-11 · empirical · scope: no-gradient · confidence: med

HONEST NOVELTY CHECK: the precise recipe (training-free + accumulating MEMORY + SKILL library + VERIFIABLE/unit-test triggers + cross-agent transfer) is ALREADY implemented in general-domain agents by 2026 — e.g. MUSE-Autoskill and MemSkill — so the mechanism itself is not novel; the program must cite these to avoid over-claiming.


- **Sources:** [MUSE-Autoskill: Self-Evolving Agents via Skill Creation, Memory, Management, and Evaluation](https://arxiv.org/abs/2605.27366) · [MemSkill: Learning and Evolving Memory Skills for Self-Evolving Agents](https://arxiv.org/abs/2602.02474)

- **Relevance:** B7 (mechanism already done in general agents — bounds the novelty claim)


### A5-12 · empirical · scope: n/a · confidence: high

Speech/omni agents today are EVALUATED but treated as STATIC systems: EVA-Bench scores voice agents including an EVA-X 'Experience' metric (conversation progression, conciseness, turn-taking) and VoiceAssistant-Eval covers multi-round dialogue/speaker/paralinguistics — but neither tests, nor any surveyed system implements, a frozen voice agent that SELF-EVOLVES a memory/skill store by verifiable reward across episodes.


- **Sources:** [EVA-Bench: A New End-to-end Framework for Evaluating Voice Agents](https://arxiv.org/abs/2605.13841) · [VoiceAssistant-Eval: Benchmarking AI Assistants across Listening, Speaking, and Viewing](https://arxiv.org/abs/2509.22651)

- **Relevance:** B7 (the speech-agent self-evolution slot is measured but unfilled)


### A5-13 · theoretical · scope: no-gradient · confidence: med

NOVELTY-DELTA VERDICT (B7): the proposed 'training-free, no-gradient, self-evolving SPEECH/omni agent pairing an embedding-memory with a generative-policy, improving by verifiable reward' is NOT mechanism-novel (Reflexion/Voyager/ExpeL/ADAS/TextGrad + MUSE-Autoskill/MemSkill already own that recipe), but IS novel as a DOMAIN-TRANSFER + COMPONENT-PAIRING: (a) speech/omni domain with paralinguistic state (speaker/emotion/full-duplex/turn-taking) as memory keys AND reward signals; (b) literally pairing a VECTOR-OMNI bi-encoder (Omni-Embed-Nemotron) as memory with a GENERATIVE thinker-talker omni as policy — a two-omni-model agent; (c) verifiable SPEECH rewards (WER/ASR/ST/SER/SID) instead of text unit-tests. Frame the contribution as 'first to instantiate the no-gradient self-evolving-agent recipe in speech/omni,' not as a new learning mechanism.


- **Sources:** [Reflexion: Language Agents with Verbal Reinforcement Learning](https://arxiv.org/abs/2303.11366) · [Voyager: An Open-Ended Embodied Agent with Large Language Models](https://arxiv.org/abs/2305.16291) · [Omni-Embed-Nemotron: A Unified Multimodal Retrieval Model](https://arxiv.org/abs/2510.03458) · [MUSE-Autoskill: Self-Evolving Agents via Skill Creation, Memory, Management, and Evaluation](https://arxiv.org/abs/2605.27366)

- **Relevance:** B7 (final novelty verdict) + B5 (component mapping confirmed)
