> **🗄 ARCHIVED (2026-07-11)** — 已收官战役过程件（2026-06-30 agent-level 调研），仅作历史，非现行真源。

# S1 · Lane A4 — Speech/omni agents & the moat (B3)

> Part of **S1** (decisive probe) of [[2026-06-30-agent-level-synthesis]] — strategic survey for [[2026-06-26-training-free-rl-for-speech-omni-research-proposal]]. Run `wf_8452c9ae-a11`, 2026-06-30. Per-lane adversarial verification; only `keep=true` claims archived; links real & verifiable. Each claim is scope-tagged (no-gradient = in scope vs weight-updating = out).


**Lane summary.** VERDICT: There is an open moat. Training-free, no-gradient, self-improving SPEECH/omni agents that accumulate skills+memory across episodes are essentially UNEXPLORED, even though (a) the generic text/embodied frontier for this exact recipe is mature, and (b) the speech-agent stack is now heavily benchmarked.

Three findings: (1) The no-gradient self-improving-agent frontier — Reflexion (verbal RL, episodic reflection buffer), Voyager (frozen GPT-4 + growing executable skill library, in-context lifelong learning), ExpeL (cross-trajectory lessons), and 2026 memory-skill banks (MemSkill, Memoria, Jarvis KV-cache retrieval) — is well-developed and genuinely frozen-weights, but lives almost entirely in TEXT / web / embodied (Minecraft) / general conversational AI. None are speech-native. (2) The SPEECH-agent domain is now richly BENCHMARKED — URO-Bench, VoiceBench, VoiceAssistant-Eval, VocalBench (capability); tau2-bench voice + Full-Duplex-Bench-v3 (voice tool-use); SoulX-Duplug + Full-Duplex-Bench (turn-taking); AudioMC + MULTI-Bench (multi-turn memory/EQ); EVA-Bench (end-to-end voice agents) — but these evaluate SINGLE-EPISODE capability or WITHIN-conversation memory (AudioMC = 3–8 turns), NOT cross-episode skill/memory accumulation. Even EVA-Bench's "experience" metric (EVA-X) measures conversational fluency/turn-taking timing, not lifelong learning. (3) The METHODS that actually advance speech agents are overwhelmingly WEIGHT-UPDATING (CORTIS text-only fine-tuning; SoulX-Duplug's trained streaming state predictor; the base omni models themselves). The few training-free speech contributions are narrow RETRIEVAL/memory-injection for personalization (Jarvis, Memoria are text-centric; expressive-speech-retrieval is one speech-native bi-encoder example), not full Reflexion/Voyager-style closed loops.

MOAT JUDGMENT: Not crowded. No speech-native Voyager/ExpeL/Reflexion system was found. Cross-session memory benchmarks (LoCoMo, LongMemEval, PrefEval, PersonaMem, Mem-PAL, VehicleMemBench) are all TEXT. The natural component mapping the program proposes — vector/embedding omni as agent MEMORY (bi-encoder retrieval) and generative thinker-talker omni as agent POLICY/skill — is conceptually clean but has no end-to-end frozen, verifiable-reward, self-improving SPEECH instantiation in the literature surveyed. This is the clearest open territory of the expansion. Caveat: absence-of-evidence; benchmarks exist to MEASURE such agents the moment one is built, which is itself a moat-enabler.

Note on sources: several cited arXiv IDs are 2026-dated (2602–2606); all were surfaced directly from arxiv.org / HuggingFace / GitHub in live search and are web-verified, not fabricated.


**Adversarial verifier assessment.** Strong lane. I web-verified every cited arXiv ID, including all the suspicious 2026-dated ones (2602.02474 MemSkill, 2603.14877 SoulX-Duplug, 2603.23840 VehicleMemBench, 2604.04847 FDB-v3, 2605.13841 EVA-Bench, 2606.21453 CORTIS) — none are fabricated; all resolve to real arxiv.org abstract pages matching their stated titles. Foundational IDs (Reflexion 2303.11366, Voyager 2305.16291, tau-bench 2406.12045, VoiceBench 2410.17196, URO-Bench 2502.17810, Full-Duplex-Bench 2503.04721, VoiceAssistant-Eval 2509.22651, VocalBench 2505.15727, AudioMC 2512.14865, MULTI-Bench 2511.00850, Mem-PAL 2511.13410, Memoria 2512.12686, Jarvis 2510.22765, Expressive Speech Retrieval 2508.11187, VerifiAgent 2504.00406) all resolve and match. The central moat thesis — that the no-gradient self-improving-agent recipe (Reflexion/Voyager/ExpeL/MemSkill) is mature but lives in text/embodied, while the speech-agent domain is richly benchmarked but only at single-episode/within-session scope, with no speech-native frozen self-improving closed loop — is well-supported and the scope tagging is mostly accurate (notably A4-09 correctly fences CORTIS/SoulX-Duplug as weight-updating/OUT of scope). I keep all 15 claims. Minor overstatements flagged but none fatal: (a) A4-04's VocalBench figures (9,400 instances / 16 skills) match an earlier version; the current abstract states ~24k instances / 14 characters — decorative, the single-episode thesis stands; (b) A4-03 calls Jarvis "text-centric" but it is actually a vision-language (image) personalization framework, and "training-free" is unconfirmed for both Jarvis and Memoria from their abstracts — yet the load-bearing point (neither is speech-native) holds; (c) A4-07's "3-8 turns" and A4-11/A4-14's inference-time "training-free" quotes are not in the abstracts but are plausibly in the paper bodies and consistent with the core claims; (d) A4-08's VehicleMemBench modality (text vs voice) is unconfirmed from its abstract, though Mem-PAL is confirmed text. A4-12 (the decisive moat finding) is correctly self-caveated as absence-of-evidence and kept at med.


---

## Verified claims & sources (15 kept / 15 total)


### A4-01 · empirical · scope: no-gradient · confidence: high

Reflexion establishes the canonical no-gradient self-improving-agent recipe: an agent writes verbal self-critiques after each trial into an episodic long-term memory buffer and conditions future actions on it, with NO weights updated and NO model fine-tuned — 'the learning lives entirely in the context window'.


- **Sources:** [Reflexion: Language Agents with Verbal Reinforcement Learning](https://arxiv.org/abs/2303.11366)

- **Relevance:** B3 (defines the no-gradient self-improving template); B5


### A4-02 · empirical · scope: no-gradient · confidence: high

Voyager is the canonical training-free LIFELONG SKILL-LIBRARY agent: a frozen GPT-4 (blackbox queries, no parameter fine-tuning) grows an ever-expanding library of executable, embedding-indexed skills and composes them via in-context lifelong learning — but the domain is embodied Minecraft, NOT speech/voice.


- **Sources:** [Voyager: An Open-Ended Embodied Agent with Large Language Models](https://arxiv.org/abs/2305.16291)

- **Relevance:** B3 (skill-library template; absence of speech variant = moat); B4


### A4-03 · empirical · scope: no-gradient · confidence: med

The 2025–2026 no-gradient memory/skill-bank frontier (MemSkill 'evolving skill bank', Memoria agentic memory for personalized conversational AI, Jarvis personal KV-cache retrieval) explicitly externalizes evolving state at inference time without weight updates — but all are TEXT / general conversational AI, not speech-native.


- **Sources:** [MemSkill: Learning and Evolving Memory Skills for Self-Evolving Agents](https://arxiv.org/pdf/2602.02474) · [Memoria: A Scalable Agentic Memory Framework for Personalized Conversational AI](https://arxiv.org/html/2512.12686v1) · [Jarvis: Towards Personalized AI Assistant via Personal KV-Cache Retrieval](https://arxiv.org/pdf/2510.22765)

- **Relevance:** B3 (frontier is no-gradient but text-only → speech moat); B5


### A4-04 · empirical · scope: mixed · confidence: high

The SPEECH/omni agent CAPABILITY layer is densely benchmarked by frozen-model evaluations — URO-Bench (first S2S benchmark with multilingual, multi-round, paralinguistic axes), VoiceBench (LLM voice assistants), VoiceAssistant-Eval (10,497 examples, listening/speaking/viewing), VocalBench (9,400 instances, 16 vocal skills) — but every one scores SINGLE-EPISODE capability, none measures cross-episode self-improvement.


- **Sources:** [URO-Bench: Towards Comprehensive Evaluation for End-to-End Spoken Dialogue Models](https://arxiv.org/abs/2502.17810) · [VoiceBench: Benchmarking LLM-Based Voice Assistants](https://arxiv.org/abs/2410.17196) · [VoiceAssistant-Eval: Benchmarking AI Assistants across Listening, Speaking, and Viewing](https://arxiv.org/abs/2509.22651) · [VocalBench: Benchmarking the Vocal Conversational Abilities for Speech Interaction Models](https://arxiv.org/abs/2505.15727)

- **Relevance:** B3 (eval coverage exists but only single-episode → measurement moat is half-open)


### A4-05 · empirical · scope: mixed · confidence: high

Voice TOOL-USE / function-calling is now benchmarked (tau2-bench voice = full-duplex audio user-simulator + agent with realistic audio degradation; Full-Duplex-Bench-v3 = chained API calls across 4 domains under real human disfluency), but these evaluate fixed agents' tool-calling competence, not a frozen agent that accumulates a tool/skill library over episodes.


- **Sources:** [tau2-bench voice README (sierra-research/tau2-bench)](https://github.com/sierra-research/tau2-bench/blob/main/src/tau2/voice/README.md) · [tau-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains](https://arxiv.org/abs/2406.12045) · [Full-Duplex-Bench-v3: Benchmarking Tool Use for Full-Duplex Voice Agents Under Real-World Disfluency](https://arxiv.org/pdf/2604.04847)

- **Relevance:** B3 (voice tool-use evals exist; skill-accumulation agent absent → moat)


### A4-06 · empirical · scope: mixed · confidence: high

EVA-Bench, the end-to-end voice-agent framework whose name evokes 'experience', defines EVA-X as conversational EXPERIENCE = progression, spoken conciseness, and turn-taking TIMING — i.e. within-conversation fluency, explicitly NOT cross-episode experiential learning or skill/memory accumulation; its abstract tests no training-free self-improving agent.


- **Sources:** [EVA-Bench: A New End-to-end Framework for Evaluating Voice Agents](https://arxiv.org/abs/2605.13841) · [EVA-Bench (ServiceNow blog)](https://huggingface.co/blog/ServiceNow-AI/eva)

- **Relevance:** B3 (even the 'experience' eval is within-episode → confirms moat)


### A4-07 · empirical · scope: mixed · confidence: high

Multi-turn MEMORY for speech is benchmarked only at WITHIN-conversation scope: AudioMC (Audio MultiChallenge, Scale AI) tests Inference Memory / Instruction Retention / Self-Coherence + a new Voice-Editing axis over just 3–8-turn human-speech conversations; MULTI-Bench tests multi-turn emotional intelligence of spoken dialogue models. Neither tests cross-session memory of a frozen self-improving agent.


- **Sources:** [Audio MultiChallenge: A Multi-Turn Evaluation of Spoken Dialogue Systems on Natural Human Interaction](https://arxiv.org/abs/2512.14865) · [MULTI-Bench: A Multi-Turn Interactive Benchmark for Assessing Emotional Intelligence ability of Spoken Dialogue Models](https://arxiv.org/pdf/2511.00850)

- **Relevance:** B3 (speech memory eval is within-session only → cross-session moat); B4 (emotion/speaker memory)


### A4-08 · empirical · scope: no-gradient · confidence: high

Cross-SESSION long-term memory — the continuity dimension a self-improving agent needs — is benchmarked richly but ENTIRELY in TEXT (LoCoMo ~35 sessions, LongMemEval ~500 sessions, PrefEval, PersonaMem, Mem-PAL, VehicleMemBench, OP-Bench); no speech-to-speech / omni cross-session memory benchmark surfaced.


- **Sources:** [Mem-PAL: Towards Memory-based Personalized Dialogue Assistants for Long-term User-Agent Interaction](https://arxiv.org/pdf/2511.13410) · [AI Memory Benchmarks 2026: LoCoMo, LongMemEval & BEAM (mem0)](https://mem0.ai/blog/ai-memory-benchmarks-in-2026) · [VehicleMemBench: An Executable Benchmark for Multi-User Long-Term Memory in In-Vehicle Agents](https://arxiv.org/pdf/2603.23840)

- **Relevance:** B3 (cross-session memory is text-only → speech moat is open)


### A4-09 · empirical · scope: weight-updating · confidence: high

The methods that actually IMPROVE speech agents are predominantly WEIGHT-UPDATING (out of scope): CORTIS fine-tunes the SLM's LLM component on text task-supervision (keeping only speech modules frozen); SoulX-Duplug trains a streaming state-prediction module with an ASR objective for full-duplex turn-taking. These are not no-gradient self-improvement.


- **Sources:** [CORTIS: Text-Only Adaptation of Spoken Language Models for Task-Oriented Voice Agents](https://arxiv.org/abs/2606.21453) · [SoulX-Duplug: Plug-and-Play Streaming State Prediction Module for Realtime Full-Duplex Speech Conversation](https://arxiv.org/abs/2603.14877)

- **Relevance:** B3 (mainstream speech-agent progress is gradient-based → contrast with the no-gradient moat)


### A4-10 · empirical · scope: mixed · confidence: med

Full-duplex turn-taking — a defining speech-agent capability — is advanced by TRAINED modules (SoulX-Duplug state predictor) and measured by frozen-model benchmarks (Full-Duplex-Bench v1/v3); turn-taking is treated as a learned/streaming-control problem, NOT as an externally-accumulated skill, so no training-free self-improving turn-taking agent exists.


- **Sources:** [Full-Duplex-Bench: A Benchmark to Evaluate Full-Duplex Spoken Dialogue Models on Turn-taking Capabilities](https://arxiv.org/abs/2503.04721) · [Awesome-Full-Duplex-SDM (curated list)](https://github.com/Ruiqi-Yan/Awesome-Full-Duplex-SDM)

- **Relevance:** B3 (full-duplex is gradient/model-centric → training-free angle unclaimed)


### A4-11 · empirical · scope: no-gradient · confidence: med

The few NO-GRADIENT speech-native contributions are narrow RETRIEVAL/memory-injection for personalization, not closed-loop self-improvement: e.g. expressive-speech retrieval caches speech-style embeddings and retrieves by text-prompt cosine similarity at inference (a speech bi-encoder = agent MEMORY component), and speaker/emotion profiles are injected at inference to keep style consistent.


- **Sources:** [Expressive Speech Retrieval using Natural Language Descriptions of Speaking Style](https://arxiv.org/pdf/2508.11187) · [Memory-Augmented AI Assistants Actually Remember You](https://aicompetence.org/memory-augmented-ai-assistants-remember-you/)

- **Relevance:** B3/B6 (vector-omni-as-memory is plausible but only narrow components exist → moat); B4


### A4-12 · empirical · scope: no-gradient · confidence: med

DECISIVE MOAT FINDING: no speech-native instantiation of the Reflexion/Voyager/ExpeL recipe (frozen weights + verifiable reward + episode-spanning skill/memory accumulation) was found across targeted searches; the recipe and the speech-agent evals exist independently but have not been joined. The expansion's target is an open, uncrowded moat.


- **Sources:** [Voyager: An Open-Ended Embodied Agent with Large Language Models](https://arxiv.org/abs/2305.16291) · [Reflexion: Language Agents with Verbal Reinforcement Learning](https://arxiv.org/abs/2303.11366) · [EVA-Bench: A New End-to-end Framework for Evaluating Voice Agents](https://arxiv.org/abs/2605.13841)

- **Relevance:** B3 (the core resolution: speech self-improving no-gradient agents = open moat)


### A4-13 · theoretical · scope: no-gradient · confidence: med

The program's two-component mapping is literature-supported as natural building blocks: a VECTOR/embedding omni model functions as a retrieval bi-encoder = agent MEMORY (cf. speech-style retrieval, cached speech embeddings, vector-DB memory layers), and a GENERATIVE thinker-talker omni functions as the POLICY/skill executor — but no work composes both into one frozen, verifiable-reward, self-improving SPEECH agent.


- **Sources:** [Expressive Speech Retrieval using Natural Language Descriptions of Speaking Style](https://arxiv.org/pdf/2508.11187) · [From Human Memory to AI Memory: A Survey on Memory Mechanisms in the Era of LLMs](https://arxiv.org/pdf/2504.15965)

- **Relevance:** B6 (component decomposition feasibility); B3


### A4-14 · empirical · scope: no-gradient · confidence: med

Frozen-model, no-training verifier/test-time-scaling agentry is established generically (e.g. VerifiAgent: 'does not require any training process... leveraging frozen LLMs... integrated into test-time compute scaling'), reinforcing that the no-gradient agent paradigm is mature in text — making its near-total absence in speech a domain gap rather than a paradigm gap.


- **Sources:** [VerifiAgent: a Unified Verification Agent in Language Model Reasoning](https://arxiv.org/pdf/2504.00406)

- **Relevance:** B3/B5 (paradigm is mature in text → transplant opportunity to speech)


### A4-15 · empirical · scope: no-gradient · confidence: low

Commercial/production voice-agent practice uses explicit external memory (short-term conversational + long-term working state, read before reasoning and written after) with frozen LLMs, confirming the no-gradient + external-state pattern is already the deployed norm — but it is engineering, not a verifiable-reward self-improving research loop, leaving the research moat intact.


- **Sources:** [Building a Fully Local LLM Voice Assistant: A Practical Architecture Guide](https://pub.towardsai.net/building-a-fully-local-llm-voice-assistant-a-practical-architecture-guide-6a506aee6020) · [On-Device Voice AI for LLM Voice Agents (Sensory)](https://sensory.com/solution/llm-voice-agents/)

- **Relevance:** B3 (industry uses external memory but not the research loop → moat is research-open)
