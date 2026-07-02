# S2 · A1 — Agent memory (deep design + speech instantiation)

> Part of **S2 deepening** (memory + skills design) of [[2026-06-30-agent-level-synthesis]]. Run `wf_a066da37-c09`, 2026-06-30. Per-lane adversarial verification; only `keep=true` archived; links real. Each claim tagged **scope** (no-gradient = in / weight-updating = out) · **open_source** · design_relevance.


**Lane summary.** Deep design survey for the MEMORY component of a training-free (no-gradient, frozen-weights) L4 speech agent whose external state evolves under verifiable speech rewards. Findings organized in four blocks. (1) ARCHITECTURES: the field has converged from flat append-only buffers toward STRUCTURED, TEMPORALLY-SCOPED stores. The canonical taxonomy is episodic / semantic / procedural over a write–manage–read loop (survey 2603.07670). Concrete instantiations span OS-paging (MemGPT/MemoryOS), forgetting-curve decay (MemoryBank), self-linking note graphs (A-MEM/Zettelkasten), knowledge-graph world models with episodic vertices (AriGraph), hippocampal index + Personalized PageRank (HippoRAG/HippoRAG 2), bi-temporal validity graphs (Zep/Graphiti), and delta-curated fact stores (Mem0). Almost all are no-gradient and open-source. (2) RETRIEVAL & RANKING: the Generative-Agents score = recency(exp-decay) + importance(LLM 1–10) + relevance(cosine) remains the reference weighting; production systems add a two-stage retrieve-then-rerank cascade (ANN recall → cross-encoder or ColBERT late-interaction). The frozen vector-omni bi-encoder (Omni-Embed-Nemotron) is the natural multimodal INDEX supporting cross-modal and joint text+audio retrieval. (3) CURATION / ANTI-COLLAPSE: theta2's four failure modes are all grounded in real work — Reflexion's append-only verbal buffer plateaus; ACE names "context collapse" + "brevity bias" and fixes them with incremental delta items; Mem0/Memory-R1 use selective ADD/UPDATE/DELETE/NOOP; MemoryBank adds Ebbinghaus decay; AgentPoison/MemoryGraft/2601.05504 demonstrate memory poisoning and motivate provenance + trust-scored, time-decayed retrieval. The "Anatomy of Agentic Memory" audit (2602.19320) warns that benchmarks are underscaled and metrics misaligned. (4) SPEECH-SPECIFIC: audio-native retrieval already exists (WavRAG, SpeechRAG, SEAL, VoxRAG) and keeps paralinguistic content that ASR-then-text discards; MoshiRAG shows full-duplex async retrieval that hides memory lookup inside the turn-taking gap. But memory KEYED by paralinguistic state (speaker-ID/emotion/turn) and a SPEECH cross-session memory BENCHMARK do not yet exist: LongMemEval/LoCoMo are text, Mem-Gallery/Omni-SimpleMem are vision+text, A-MBER is text-emotion. Recommendation (final claim): a three-tier structured store (episodic turns / per-speaker semantic persona / procedural skills) over a bi-temporal KG, indexed by a FROZEN omni bi-encoder on JOINT audio+ASR embeddings, KEYED by speaker-ID/SER/turn, retrieved two-stage with recency×importance×relevance + rerank, curated by non-destructive delta ops + Ebbinghaus decay + provenance, with verifiable-reward (WER/ASR/ST/SER/SID/intent) best-of-N SELECTION over memory-writes replacing Memory-R1-style gradient training, and a β-KL trust region on memory-mutation rate to satisfy JitRL's slow-drift convergence precondition; consolidation runs off the critical path (Letta sleep-time / MoshiRAG gap).


**Adversarial verifier assessment.** Strong, well-sourced lane — all 26 claims KEPT. I web-verified every high-risk source, especially the future-dated 2026 arXiv IDs that warranted skepticism: 2603.07670 (memory survey), 2602.19320 (Anatomy of Agentic Memory), 2604.12928 (MoshiRAG, with real Kyutai author list + github.com/kyutai-labs/moshi-rag + HF weights), 2604.07017 (A-MBER), 2601.03515 (Mem-Gallery), 2604.01007 (Omni-SimpleMem), 2512.16962 (MemoryGraft), 2601.05504 (memory-poisoning defense) — ALL resolve to real papers with content matching the claims. The well-known anchors (Reflexion, Generative Agents, ColBERT, Mem0, MemoryBank, A-MEM, AriGraph, HippoRAG, Zep/Graphiti, MemoryOS, Letta, LongMemEval, LoCoMo, Omni-Embed-Nemotron, WavRAG, SpeechRAG, SEAL, VoxRAG, x-vector, Personal VAD) are all real and accurately characterized.

Scope tagging is notably disciplined: Memory-R1 is correctly flagged weight-updating (out-of-lane) and its design-relevance honestly proposes replacing the trained manager with no-gradient reward-selection; the speech-retrieval methods (WavRAG/SpeechRAG/SEAL) and ColBERT are tagged 'mixed' because a thin retriever/adapter is trained while the base model stays frozen — accurate. The one scope I'd scrutinize most is MoshiRAG ('mixed'): it actually fine-tunes Moshi to emit retrieval-trigger tokens, so the policy side is weight-updating; the claim survives because it cites MoshiRAG only as a turn-taking TIMING pattern, not as a no-gradient existence proof.

Residual caveats (none rising to keep=false): a handful of fine-grained numbers are the papers' own headline figures that I confirmed at the abstract level but did not re-derive digit-by-digit (AgentPoison's 82%/63% per-stage split, Zep's +18.5%/90%/'20k stars', ACE's 86.9% latency, Memory-R1's '152 QA pairs', Mem-Gallery's '13 systems' which I could not independently confirm). Two claims are time-bounded negative existentials (A1-24's 'no speech paralinguistic benchmark') — defensible now but the lane should re-check before publication given the fast 2026 cadence of memory benchmarks. Minor repo-URL nits: Reflexion's canonical repo is noahshinn024/reflexion (cited noahshinn/reflexion), and github.com/ace-agent/ace resolves but the canonical ACE release is SambaNova/Stanford. None of these undermine the underlying claims. Overall the lane is rigorous, honestly hedged, and the synthesis (A1-26) is a properly grounded, buildable design spec rather than an overclaimed result.


---

## Verified claims (26 kept / 26 total)


### A1-01 · definitional · scope: n/a · OSS: no

Agent memory is now formalized as a write–manage–read loop along three orthogonal axes — temporal scope, representational substrate, and control policy — with the standard functional taxonomy being episodic (timestamped concrete experiences), semantic (de-contextualized abstracted facts), and procedural (reusable skills/plans); crucially, episodic→semantic consolidation is rarely automatic in current systems.


- **Sources:** [Memory for Autonomous LLM Agents: Mechanisms, Evaluation, and Emerging Frontiers](https://arxiv.org/abs/2603.07670) · [Types of AI Agent Memory: Episodic, Semantic, Procedural and More (Atlan)](https://atlan.com/know/types-of-ai-agent-memory/)

- **Design relevance:** Sets the skeleton for the speech-agent store: implement three explicit tiers (episodic spoken-turn stream / semantic per-speaker persona / procedural skill library) and do NOT assume consolidation is free — schedule it as an explicit curation step.


### A1-02 · empirical · scope: no-gradient · OSS: yes — github.com/zhongwanjun/MemoryBank-SiliconFriend

MemoryBank gives a no-gradient long-term-memory mechanism with three parts (storage / retriever / updater) where the updater implements Ebbinghaus-forgetting-curve decay so memories strengthen on re-access and decay with elapsed time; it powers the SiliconFriend companion.


- **Sources:** [MemoryBank: Enhancing Large Language Models with Long-Term Memory](https://arxiv.org/abs/2305.10250) · [MemoryBank (AAAI 2024 proceedings)](https://ojs.aaai.org/index.php/AAAI/article/view/29946)

- **Design relevance:** Adopt Ebbinghaus-style time-decay as the FORGETTING primitive for the speech store; re-access (a memory used to answer correctly under reward) should boost retention strength — a no-gradient analog of consolidation.


### A1-03 · empirical · scope: no-gradient · OSS: yes — github.com/agiresearch/A-mem

A-MEM (Zettelkasten 'agentic memory') stores each memory as a structured note (context description, keywords, tags) and builds an interconnected network via dynamic linking; adding a new note triggers MEMORY EVOLUTION — it can update the attributes/links of existing historical notes — giving curation without destructive rewriting.


- **Sources:** [A-MEM: Agentic Memory for LLM Agents](https://arxiv.org/abs/2502.12110) · [A-MEM code](https://github.com/agiresearch/A-mem)

- **Design relevance:** A linked-note graph is a concrete anti-collapse structure: new spoken-turn memories augment and re-tag existing notes (e.g., link all turns from the same speaker/topic) instead of summarizing-over-and-losing detail.


### A1-04 · empirical · scope: no-gradient · OSS: yes — github.com/AIRI-Institute/AriGraph

AriGraph builds a knowledge-graph world model that integrates SEMANTIC and EPISODIC memory in one structure (semantic KG plus episodic vertices/edges), enabling associative retrieval of interconnected concepts relevant to the agent's current state — and beats flat-RAG agents in interactive text-game environments.


- **Sources:** [AriGraph: Learning Knowledge Graph World Models with Episodic Memory for LLM Agents](https://arxiv.org/abs/2407.04363) · [AriGraph code](https://github.com/AIRI-Institute/AriGraph)

- **Design relevance:** Validates a single graph holding both episodic (this turn happened) and semantic (this speaker's stable profile) memory with associative (multi-hop) retrieval — the substrate for 'who said what, when, and how did they feel' queries.


### A1-05 · empirical · scope: no-gradient · OSS: yes — github.com/OSU-NLP-Group/HippoRAG

HippoRAG / HippoRAG 2 implement a neurobiological hippocampal-index design — LLM-extracted open-KG triples + Personalized PageRank over a phrase/passage graph with synonym detection — giving non-parametric continual learning and superior multi-hop ASSOCIATIVE memory (up to +20% multi-hop QA; +7% associative over the best embedding model) without any base-model updates.


- **Sources:** [HippoRAG: Neurobiologically Inspired Long-Term Memory for LLMs](https://arxiv.org/abs/2405.14831) · [From RAG to Memory: Non-Parametric Continual Learning for LLMs (HippoRAG 2)](https://arxiv.org/abs/2502.14802)

- **Design relevance:** Personalized-PageRank-over-a-graph is the associative-retrieval engine for linking a current spoken query to distant prior sessions; the 'index = embeddings seed PPR' pattern maps directly onto using the frozen omni bi-encoder as the seed scorer.


### A1-06 · empirical · scope: no-gradient · OSS: yes — github.com/getzep/graphiti

Zep/Graphiti is a temporal (bi-temporal) knowledge-graph memory layer that records WHEN each fact was true and where it came from, updates non-lossily with validity intervals, and beats MemGPT on Deep Memory Retrieval (94.8% vs 93.4%) and improves LongMemEval accuracy up to +18.5% while cutting latency ~90%.


- **Sources:** [Zep: A Temporal Knowledge Graph Architecture for Agent Memory](https://arxiv.org/abs/2501.13956) · [Graphiti (temporal KG engine)](https://github.com/getzep/graphiti)

- **Design relevance:** Bi-temporal validity intervals are the principled defense against theta2's temporal-contamination/knowledge-update failure: a speaker's old preference is marked invalid-after rather than overwritten, so stale facts neither vanish nor corrupt current answers.


### A1-07 · empirical · scope: no-gradient · OSS: yes — github.com/mem0ai/mem0

Mem0 is a production no-gradient memory architecture whose pipeline is EXTRACT (LLM pulls salient facts) then UPDATE via a fixed operation set {ADD, UPDATE, DELETE, NOOP}; a graph variant (Mem0g) adds relational structure; it reports ~91% lower p95 latency and >90% token savings vs full-context baselines on LoCoMo.


- **Sources:** [Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory](https://arxiv.org/abs/2504.19413) · [Mem0 code](https://github.com/mem0ai/mem0)

- **Design relevance:** The {ADD/UPDATE/DELETE/NOOP} operation set is the exact write-API for the speech store; selective DELETE/UPDATE (not append-only) is what makes memory compound rather than plateau — directly answers theta2's 'naive append-only does not compound.'


### A1-08 · empirical · scope: no-gradient · OSS: yes — github.com/BAI-LAB/MemoryOS

MemoryOS applies an OS-paging metaphor with THREE tiers — short-term, mid-term, and long-term persona memory — plus automated user-profile and knowledge updating, generalizing MemGPT's two-tier main/external context into a hierarchical store with store/update/retrieval/response modules.


- **Sources:** [Memory OS of AI Agent (MemoryOS)](https://arxiv.org/abs/2506.06326) · [MemoryOS code](https://github.com/BAI-LAB/MemoryOS)

- **Design relevance:** The persona-memory tier is the natural home for per-SPEAKER state in a speech agent; hierarchical paging (hot turns in-context, warm session summaries mid-term, cold persona/profile long-term) bounds context cost for long full-duplex conversations.


### A1-09 · empirical · scope: no-gradient · OSS: yes — github.com/letta-ai/letta

Letta (MemGPT successor) introduces 'sleep-time compute': memory consolidation runs ASYNCHRONOUSLY in a separate sleep-time agent that holds the core-memory-editing tools, while the primary agent (which lacks those tools) answers in real time — improving both response latency and memory quality.


- **Sources:** [Sleep-time Compute (Letta)](https://www.letta.com/blog/sleep-time-compute/) · [Agent Memory: How to Build Agents That Learn and Remember (Letta)](https://www.letta.com/blog/agent-memory/)

- **Design relevance:** Critical for a REAL-TIME speech agent: keep curation/consolidation off the response critical path so memory maintenance never stalls turn-taking; the read path stays a fast retrieval, writes/consolidation batch asynchronously.


### A1-10 · empirical · scope: no-gradient · OSS: yes — github.com/joonspk-research/generative_agents

The Generative-Agents memory stream defines the reference retrieval-scoring formula: score = α_recency·recency + α_importance·importance + α_relevance·relevance, where recency is exponential decay over elapsed time, importance is an LLM-assigned 1–10 poignancy rating stored at write time, and relevance is cosine similarity between the memory and query embeddings (all α=1 in the original).


- **Sources:** [Generative Agents: Interactive Simulacra of Human Behavior](https://arxiv.org/abs/2304.03442) · [Generative Agents memory scoring (implementation reference)](https://github.com/joonspk-research/generative_agents)

- **Design relevance:** Adopt this exact weighted score as the speech store's first-pass ranker, but compute relevance with the omni bi-encoder over AUDIO+text and set importance from verifiable reward signals (e.g., a turn that resolved a high-WER ambiguity is high-importance).


### A1-11 · empirical · scope: mixed · OSS: yes — github.com/stanford-futuredata/ColBERT

State-of-the-art retrieval is a two-stage CASCADE: a cheap bi-encoder/ANN recall stage followed by a precision reranker — either a cross-encoder (joint query-doc transformer, accurate but expensive) or ColBERT-style LATE INTERACTION (per-token embeddings + MaxSim), which recovers most cross-encoder accuracy at far lower latency.


- **Sources:** [ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT](https://arxiv.org/abs/2004.12832) · [Reranking & Cross-Encoders for RAG (2026 practitioner guide)](https://localaimaster.com/blog/reranking-cross-encoders-guide)

- **Design relevance:** Use the frozen omni bi-encoder as stage-1 recall over the audio-keyed index, then a lightweight reranker (cross-encoder or late-interaction) for precision; this two-stage split keeps the real-time speech read path fast while improving top-k quality.


### A1-12 · empirical · scope: no-gradient · OSS: yes — huggingface.co/nvidia/omni-embed-nemotron-3b

Omni-Embed-Nemotron is a single FROZEN-usable bi-encoder that embeds text, image, AUDIO, and video into one space, supporting both cross-modal (text→audio) and joint-modal (text→audio+video) retrieval — i.e., a drop-in multimodal INDEX for an audio-native memory store.


- **Sources:** [Omni-Embed-Nemotron: A Unified Multimodal Retrieval Model for Text, Image, Audio, and Video](https://arxiv.org/abs/2510.03458) · [nvidia/omni-embed-nemotron-3b (model weights)](https://huggingface.co/nvidia/omni-embed-nemotron-3b)

- **Design relevance:** This is the concrete vector-omni that serves as the speech MEMORY INDEX: store raw-audio embeddings (preserving paralinguistics) alongside ASR-text in one space so a spoken query can retrieve by content AND acoustic similarity; it is the 'agent memory' half of the frozen bi-encoder + frozen thinker-talker design.


### A1-13 · empirical · scope: no-gradient · OSS: yes — github.com/ace-agent/ace

ACE empirically names and fixes two of theta2's failure modes: 'brevity bias' (iterative summarization drops domain detail) and 'context collapse' (iterative rewriting erodes accumulated knowledge); its fix is to treat context as an evolving playbook curated by Generator/Reflector/Curator roles that merge small DELTA items incrementally rather than rewriting the whole context (+10.6% AppWorld, +8.6% finance, ~86.9% lower adaptation latency).


- **Sources:** [Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models](https://arxiv.org/abs/2510.04618) · [ACE code](https://github.com/ace-agent/ace)

- **Design relevance:** Mandates INCREMENTAL DELTA writes over destructive summarization for the speech store's curation step — never collapse a speaker's history into a terse summary; append structured, reversible deltas. This is the operational anti-collapse rule.


### A1-14 · empirical · scope: no-gradient · OSS: yes — github.com/noahshinn/reflexion

Reflexion grounds theta2's 'plateau': it improves agents purely by maintaining self-reflective text in an APPEND-only episodic buffer (a 'verbal/semantic gradient'), with no weight updates — effective early but the append-only verbal memory gives diminishing returns and does not compound indefinitely.


- **Sources:** [Reflexion: Language Agents with Verbal Reinforcement Learning](https://arxiv.org/abs/2303.11366) · [Reflexion code](https://github.com/noahshinn/reflexion)

- **Design relevance:** Baseline to beat: a speech agent that only appends verbal reflections will plateau. The design must add STRUCTURE (graph/tiers), CURATION (delete/dedup), and value-based selection on top of Reflexion-style feedback.


### A1-15 · empirical · scope: weight-updating · OSS: yes (authors release code; exact repo URL not verified here)

Memory-R1 shows that LEARNED memory management (an RL-trained Memory Manager choosing ADD/UPDATE/DELETE/NOOP + an Answer Agent) beats static heuristic curation with only 152 training QA pairs across LoCoMo/MSC/LongMemEval — but it does so by fine-tuning the manager with PPO/GRPO, i.e., it is weight-updating, not pure no-gradient.


- **Sources:** [Memory-R1: Enhancing LLM Agents to Manage and Utilize Memories via Reinforcement Learning](https://arxiv.org/abs/2508.19828)

- **Design relevance:** Proves value-based credit assignment over memory OPERATIONS is what makes memory compound (theta2's claim) — but to stay no-gradient we REPLACE its trained manager with verifiable-reward best-of-N SELECTION over candidate memory-writes (reusing W1's reward machinery), getting the credit-assignment benefit without touching weights.


### A1-16 · empirical · scope: no-gradient · OSS: yes — github.com/BillChan226/AgentPoison

Memory poisoning/contamination is a demonstrated attack surface on no-gradient memory: AgentPoison backdoors RAG/agent memory with no training, achieving 82% retrieval and 63% end-to-end attack success at <0.1% poison ratio with <1% benign drop; MemoryGraft achieves persistent compromise via poisoned EXPERIENCE retrieval; defenses use temporal decay + multi-signal trust scoring + memory sanitization.


- **Sources:** [AgentPoison: Red-teaming LLM Agents via Poisoning Memory or Knowledge Bases](https://arxiv.org/abs/2407.12784) · [MemoryGraft: Persistent Compromise of LLM Agents via Poisoned Experience Retrieval](https://arxiv.org/abs/2512.16962) · [Memory Poisoning Attack and Defense on Memory-Based LLM-Agents](https://arxiv.org/abs/2601.05504)

- **Design relevance:** Grounds theta2's 'poisoning' failure as real and cheap. The speech store must attach PROVENANCE + a trust/verification score to every write (only reward-verified turns become high-trust memories) and apply temporal decay, so an adversarial or self-generated bad memory cannot dominate retrieval.


### A1-17 · empirical · scope: n/a · OSS: no

An independent 2026 audit ('Anatomy of Agentic Memory') finds the empirical foundations of memory systems are fragile: benchmarks are underscaled and saturating, metrics (often LLM-judge) are misaligned with semantic utility and judge-sensitive, accuracy is strongly backbone-dependent, and the latency/throughput cost of memory MAINTENANCE is routinely overlooked.


- **Sources:** [Anatomy of Agentic Memory: Taxonomy and Empirical Analysis of Evaluation and System Limitations](https://arxiv.org/abs/2602.19320)

- **Design relevance:** Forces evaluation discipline for the speech-memory benchmark we must build: use VERIFIABLE rewards (WER/SID/SER accuracy) not LLM-judge where possible, report maintenance latency, and test across multiple frozen backbones to avoid backbone-specific artifacts.


### A1-18 · empirical · scope: mixed · OSS: yes (code released by ZJU/Alibaba; base SDM kept frozen, retriever trained)

Audio-native retrieval that bypasses ASR already works: WavRAG embeds and retrieves directly from raw audio over a text-audio hybrid knowledge base (its 'WavRetriever'), achieving retrieval comparable to ASR→text RAG with ~10x acceleration while preserving acoustic information that transcription discards.


- **Sources:** [WavRAG: Audio-Integrated Retrieval Augmented Generation for Spoken Dialogue Models](https://arxiv.org/abs/2502.14727)

- **Design relevance:** Confirms the core speech-memory premise: index on AUDIO embeddings, not ASR text, so paralinguistics (who/emotion/prosody) survive into the memory key. WavRAG's hybrid text-audio KB is the template for the joint index built on omni-embed-nemotron.


### A1-19 · empirical · scope: mixed · OSS: no (SpeechRAG = Amazon; SEAL code not confirmed public)

Speech retrieval can keep the base LLM FROZEN by training only a small alignment component: SpeechRAG fine-tunes a speech encoder into an adapter feeding a frozen LLM-based retriever (text query → audio passage), and SEAL adds a shared scaling layer aligning speech and text embedding spaces; both stay robust and even surpass cascaded ASR pipelines when WER is high, cutting pipeline latency ~50%.


- **Sources:** [Speech Retrieval-Augmented Generation without Automatic Speech Recognition (SpeechRAG)](https://arxiv.org/abs/2412.16500) · [SEAL: Speech Embedding Alignment Learning for Speech LLM with RAG](https://arxiv.org/abs/2502.02603)

- **Design relevance:** Shows the frozen-policy-compatible recipe: only a thin speech↔text alignment layer is learned (or, in our no-gradient setting, we use omni-embed-nemotron which is already aligned), so the generative thinker-talker stays frozen and reads retrieved audio passages directly.


### A1-20 · empirical · scope: no-gradient · OSS: no (no confirmed public repo)

VoxRAG is a fully transcription-free speech-to-speech retrieval pipeline that already composes the paralinguistic primitives a speech memory needs: silence-aware segmentation, SPEAKER DIARIZATION, CLAP audio embeddings, and FAISS cosine retrieval — retrieving semantically relevant audio segments directly from spoken queries.


- **Sources:** [VoxRAG: A Step Toward Transcription-Free RAG Systems in Spoken Question Answering](https://arxiv.org/abs/2505.17326)

- **Design relevance:** Concrete proof that diarization can segment audio into per-SPEAKER memory units before indexing — exactly the paralinguistic KEYING the speech agent needs; CLAP/omni embeddings + FAISS is the minimal retrieval stack.


### A1-21 · empirical · scope: mixed · OSS: yes — github.com/kyutai-labs/moshi-rag

MoshiRAG shows turn-taking-aware, ASYNCHRONOUS retrieval for real-time full-duplex speech: it detects knowledge-demanding queries and runs retrieval in parallel, exploiting 'the natural temporal gap between response onset and delivery of core information' so the lookup completes without breaking conversational flow.


- **Sources:** [MoshiRAG: Asynchronous Knowledge Retrieval for Full-Duplex Speech Language Models](https://arxiv.org/abs/2604.12928) · [MoshiRAG code](https://github.com/kyutai-labs/moshi-rag)

- **Design relevance:** The speech analog of Letta sleep-time on the READ path: memory retrieval (and writes) hide inside turn-taking gaps/backchannels, so the frozen thinker-talker keeps real-time interactivity while consulting external memory — turn-taking itself becomes a memory-timing signal.


### A1-22 · empirical · scope: n/a · OSS: no (benchmark; code/data availability not confirmed)

A-MBER is the closest existing benchmark to paralinguistic-keyed cross-session memory: given an interaction trajectory and an anchor turn, a model must infer the user's CURRENT affective state, cite historically relevant evidence, and justify it — and accuracy rises monotonically as the system gets broader, more selective, and more STRUCTURED access to history (biggest gains on long-range implicit affect and adversarial items). It is, however, text-grounded emotion, not acoustic SER.


- **Sources:** [A-MBER: Affective Memory Benchmark for Emotion Recognition](https://arxiv.org/abs/2604.07017)

- **Design relevance:** Directly validates EMOTION-as-memory-key and that structured/selective memory beats flat access for affect inference — but it operates on conversation TEXT, leaving an open gap for an ACOUSTIC-SER-grounded version, which the speech agent should target.


### A1-23 · empirical · scope: no-gradient · OSS: yes — github.com/aiming-lab/SimpleMem ; github.com/YuanchenBei/Mem-Gallery

Long-term multimodal memory benchmarks/systems exist but cover VISION+text, not audio: Mem-Gallery benchmarks multimodal long-term conversational memory over visual+textual sessions across 13 memory systems, and Omni-SimpleMem (autoresearch-discovered) reaches SOTA with +411% F1 on LoCoMo (0.117→0.598) and +214% on Mem-Gallery — confirming that lifelong memory benefits enormously from architecture/pipeline design, not hyperparameters.


- **Sources:** [Mem-Gallery: Benchmarking Multimodal Long-Term Conversational Memory for MLLM Agents](https://arxiv.org/abs/2601.03515) · [Omni-SimpleMem: Autoresearch-Guided Discovery of Lifelong Multimodal Agent Memory](https://arxiv.org/abs/2604.01007)

- **Design relevance:** Establishes the multimodal-memory frontier is vision+text and that ARCHITECTURE dominates tuning — so the speech-agent contribution (audio/paralinguistic memory) is genuinely novel, and effort should go to structure/pipeline, not hyperparameters.


### A1-24 · empirical · scope: n/a · OSS: yes — github.com/xiaowu0162/LongMemEval ; github.com/snap-research/locomo

No SPEECH/audio cross-session, paralinguistically-keyed memory benchmark currently exists: the established long-term memory benchmarks (LongMemEval — 5 abilities incl. multi-session/temporal reasoning, ~30% accuracy drop for long-context/commercial assistants; LoCoMo — ~300 turns/up to 35 sessions, single/multi-hop/temporal QA) are TEXT-only, and the multimodal ones are vision+text — leaving an open gap the speech agent must define and fill.


- **Sources:** [LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory](https://arxiv.org/abs/2410.10813) · [Evaluating Very Long-Term Conversational Memory of LLM Agents (LoCoMo)](https://arxiv.org/abs/2402.17753)

- **Design relevance:** A SPEECH cross-session memory benchmark must add: (a) raw-audio multi-session dialogue (not transcripts); (b) queries keyed by speaker-ID and acoustic emotion ('what did the angry caller from last week ask for?'); (c) verifiable acoustic labels (SID/SER) as ground truth; (d) knowledge-update + temporal-contamination + poisoning probes — extending LongMemEval's 5 abilities into the paralinguistic domain.


### A1-25 · empirical · scope: no-gradient · OSS: yes — e.g. github.com/pyannote/pyannote-audio (diarization); SpeechBrain x-vector/ECAPA models

Speaker diarization + speaker-embedding extraction (d-vector / x-vector, 'who spoke when' via clustered segment embeddings) provides ready, no-gradient paralinguistic KEYS for memory; combined with an SER label and a turn/session id, each spoken memory can be indexed by a composite (speaker, emotion, time, content) key.


- **Sources:** [X-Vectors with Multi-Scale Aggregation for Speaker Diarization](https://arxiv.org/abs/2105.07367) · [Personal VAD: Speaker-Conditioned Voice Activity Detection (d-vector speaker embeddings)](https://arxiv.org/abs/1908.04284)

- **Design relevance:** Operationalizes paralinguistic memory keys: run frozen diarization + speaker-embedding + SER at write time, store the embedding as the memory KEY (enabling speaker-scoped retrieval), and surface SID/SER mismatch as both a retrieval filter and a verifiable reward signal.


### A1-26 · theoretical · scope: no-gradient · OSS: yes (composed from open components: omni-embed-nemotron, Mem0, ACE, Graphiti, HippoRAG, pyannote/SpeechBrain)

DESIGN RECOMMENDATION (speech-agent memory component): a STRUCTURED, three-tier, temporally-scoped store — never a flat append buffer — indexed by the frozen omni bi-encoder on JOINT audio+ASR embeddings, KEYED by paralinguistic state, retrieved two-stage, curated by non-destructive deltas with decay + provenance, and governed by verifiable-reward selection under a β-KL trust region; consolidation runs off the critical path.


- **Sources:** [Memory for Autonomous LLM Agents (taxonomy)](https://arxiv.org/abs/2603.07670) · [Omni-Embed-Nemotron (multimodal index)](https://arxiv.org/abs/2510.03458) · [Agentic Context Engineering (anti-collapse delta curation)](https://arxiv.org/abs/2510.04618) · [Memory-R1 (credit-assignment over memory ops)](https://arxiv.org/abs/2508.19828) · [Zep / Graphiti (bi-temporal validity)](https://arxiv.org/abs/2501.13956)

- **Design relevance:** This is the buildable spec for the speech-agent MEMORY component: it makes memory COMPOUND (structure + delete + value-selection) instead of plateau/collapse, resists contamination/poisoning (validity + provenance + decay), keys on paralinguistics (speaker/emotion/turn), uses the frozen vector-omni as the index, keeps the generative policy frozen, and inherits JitRL's convergence guarantee via the β-KL trust region on memory mutation.
