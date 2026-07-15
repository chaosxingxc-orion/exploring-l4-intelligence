---
title: Stage-1 survey lane — memory components (mem0/Letta/Zep/A-MEM/Generative-Agents/LangMem + audio-native RAG)
date: 2026-07-06
stage: 1-argumentation
lane: memory-components
---

> **🗄 ARCHIVED (2026-07-11)** — 已收官战役过程件（2026-07-06 omni-agentic 调研），仅作历史，非现行真源。

> Stage-1 argumentation lane, part of the omni-agent-systems survey wave (2026-07-06). Scope:
> memory systems used in LLM/speech agents, 2025-01..2026-07 (older items tagged as genealogy
> roots), tested against the ORGANIZING FRAMEWORK — element | usage-pattern | constraint — and
> delta-tagged against the prior archive: S1 ([[2026-06-30-agent-level-synthesis]]), S2
> ([[2026-06-30-agent-memory-skills-design]] + [[2026-06-30-survey-agent-memory]]), L4
> ([[2026-07-04-stage1-L4-speech-agentic]]), and the r1 delta scan
> ([[2026-07-03-step1-delta-speech-agent-memory]]). Every URL WebFetch/WebSearch-verified.

## Headline verdict

Every general-purpose memory system surveyed here (Mem0, Letta/MemGPT, Zep/Graphiti, A-MEM,
Generative Agents, LangMem) is, in the framework's terms, an **ELEMENT** — a persistent external
store that survives context-window truncation and injects information the frozen model's weights
did not contain — **not** a usage pattern. The *orchestration* wrapped around that store (an
LLM prompted to play "memory manager," "reflection" self-summarization, retrieve-then-rerank
cascades) is usage-pattern machinery layered on top of the element; it doesn't do the new-info
work itself. This is a clean instance of the framework holding up: strip the persistent store and
these systems degrade to a plain long-context LLM (which is exactly the ablation each paper runs).
The most direct test of the thesis in this lane is **Memory-R1** (arXiv:2508.19828): the same
ADD/UPDATE/DELETE/NOOP role that Mem0 fills by *prompting* a frozen LLM is, in Memory-R1, filled by
a **PPO/GRPO-trained** policy — and it beats the prompted version. That is a usage-pattern
(prompted memory-manager role) failing to match a genuinely weight-updated alternative doing the
*same job*, which is evidence FOR the thesis, not against it (Memory-R1 is explicitly out-of-fence
for a training-free program). On the audio side, the picture is different and is the lane's
sharpest finding: **no surveyed audio/omni system implements cross-session, paralinguistically-keyed
memory MUTATION** (write-time ADD/UPDATE/DELETE analogous to Mem0/A-MEM) — WavRAG, MoshiRAG and
VoxRAG are all **single-session, static-knowledge-base retrieval**, not accumulating personal
memory; AFA is the closest approach (speaker-ID-keyed routing) but keys route to **text**
transcript stores, not audio-native memory objects, and its best configuration fine-tunes
LLaMA-2-70B. This CONFIRMS and sharpens the S2/archive gap claim (A1-23/A1-24, D2-05/06/07) from a
benchmark-level gap into a **mechanism-level** gap.

---

## Claims

### C1 — Mem0: prompted ADD/UPDATE/DELETE/NOOP as the memory-mutation control law

**Problem:** LLMs lose conversational coherence across sessions because context windows discard
history; naive full-context replay is slow and expensive. **Genealogy:** LLM-native; descends from
retrieval-augmented dialogue systems, formalizes the "write" side that RAG usually leaves implicit.
**Training-free:** yes — a frozen LLM is prompted to extract candidate facts, then a second prompted
call inspects the top-k similar existing memories and classifies the operation as one of
ADD/UPDATE/DELETE/NOOP; nothing is fine-tuned. A graph variant (Mem0^g) adds a Neo4j-backed relational
layer. **Axis/verdict:** ELEMENT — the dense vector store (and graph store) is the new-info carrier;
the LLM-router call is usage-pattern machinery deciding how to mutate that element, not itself a
source of new information. **Fence:** cross-session-accumulating (evaluated on LOCOMO, a multi-session
benchmark; ships production voice integrations per ElevenLabs/LiveKit/Pipecat per the mem0 2026
industry report). **Omni role:** n/a (text-only memory layer; no audio/omni model in the loop).

**Sources:** [Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory (arXiv:2504.19413)](https://arxiv.org/abs/2504.19413) (2025-04-28, verified via WebFetch) · [AI Agent Memory 2026: Progress Benchmark Report (mem0)](https://mem0.ai/blog/state-of-ai-agent-memory-2026)

**Delta vs archive:** CONFIRMS (S2 design doc already names Mem0's ADD/UPDATE/DELETE/NOOP as the
"anti-collapse curation" primitive and the mem0-2026-voice-integrations claim is already D2-04); this
claim adds the explicit element/usage-pattern split and the training-free/fine-tuned tag.

---

### C2 — Letta/MemGPT: OS-style paging + 2025 sleep-time background consolidation

**Problem:** a single LLM context window cannot hold an extended conversation or a large document;
naive truncation loses information. **Genealogy:** LLM-native, root paper 2023 (tagged as genealogy
root per recency rule), actively evolving through 2025 as the Letta product. **Training-free:** yes
— MemGPT's "virtual context management" moves data between in-context "core memory" (RAM analog) and
external "archival"/"recall" memory (disk analog) via the LLM's own tool calls, using OS-style
interrupts for control flow; the 2025 evolution adds **sleep-time agents** — a background agent
sharing memory blocks with the primary agent that consolidates fragmented memories, deduplicates,
and prunes during idle periods, entirely through memory-state edits, never weight updates (per
Letta's own framing, corroborated across the sleep-time-compute blog post, docs.letta.com's
sleep-time architecture page, and the Letta developer forum: the base LLM stays fixed and dedup/
prune/reorganize happens in the memory substrate — **verifier correction:** no single verbatim
sentence stating "neither agent's weights are altered" exists on the cited blog page itself; the
original wording here over-claimed a direct quote from that one URL where the claim is in fact a
true synthesis across several Letta sources). **Axis/verdict:**
ELEMENT — the paged core/archival/recall memory tiers are the persistent new-info store; paging
policy and sleep-time scheduling are usage-pattern control logic over that store. **Fence:**
cross-session-accumulating (the original paper's second demonstrated domain is explicitly
"multi-session chat" where the agent "remembers, reflects, and evolves... through long-term
interactions with their users"). **Omni role:** n/a (text-only; model-agnostic backend, no audio
modality in the core architecture).

**Sources:** [MemGPT: Towards LLMs as Operating Systems (arXiv:2310.08560)](https://arxiv.org/abs/2310.08560) (2023-10-12) · [Sleep-time Compute (Letta blog)](https://www.letta.com/blog/sleep-time-compute/) (2025-04-21, verified via WebFetch) · [MemGPT Is Now Part of Letta](https://www.letta.com/blog/memgpt-and-letta/)

**Delta vs archive:** CONFIRMS + adds detail (S2 doc mentions "Letta sleep-time" only in passing as
a where-consolidation-runs note; this claim spells out the paging-tier + sleep-time mechanism and
explicitly confirms no weight update occurs).

---

### C3 — Zep/Graphiti: bi-temporal knowledge-graph memory

**Problem:** flat vector-store memory cannot represent *when* a fact became true, was updated, or
was invalidated, which breaks temporal reasoning in long-running agent deployments.
**Genealogy:** LLM-native; descends from GraphRAG/knowledge-graph-RAG lineage, adds an explicit
temporal dimension. **Training-free:** yes — an LLM extracts entities/relationships from ingested
conversational "episodes" and Graphiti stores them as a **bi-temporal** graph (event-time + ingestion
-time), with every edge carrying explicit validity intervals; updates are non-lossy (old facts are
marked invalid, not deleted). **Axis/verdict:** ELEMENT — the temporal graph is the persistent
new-info substrate; retrieval/extraction prompting is usage-pattern. **Fence:**
cross-session-accumulating (94.8% vs MemGPT's 93.4% on the Deep Memory Retrieval benchmark; up to
18.5% accuracy gain / 90% latency reduction on LongMemEval, both explicitly cross-session evals).
**Omni role:** n/a in the base architecture — but vendor material explicitly markets Graphiti for
**voice agents** ("Graphiti: How Temporal Knowledge Graphs Give AI Voice Agents Persistent Memory"),
which given Graphiti's own mechanism (LLM extraction over ingested "episodes") implies the graph is
keyed on **transcribed text**, not raw audio/paralinguistic features — real-world voice deployments
of this architecture still route through ASR text.

**Sources:** [Zep: A Temporal Knowledge Graph Architecture for Agent Memory (arXiv:2501.13956)](https://arxiv.org/abs/2501.13956) (2025-01-20, verified via WebFetch) · [Graphiti: Knowledge graph memory for an agentic world (Neo4j blog)](https://neo4j.com/blog/developer/graphiti-knowledge-graph-memory/) · [Graphiti for AI Voice Agents (CallSphere blog, title-verified 2026)](https://callsphere.ai/blog/graphiti-temporal-knowledge-graph-ai-agents-2026)

**Delta vs archive:** CONFIRMS (S2 doc already cites Zep/Graphiti's bi-temporal validity-intervals
mechanism as an anti-contamination fix); the voice-agent vendor-positioning + text-keying inference
is a NEW supporting detail for the audio-gap argument.

---

### C4 — A-MEM: Zettelkasten-style self-linking memory evolution

**Problem:** flat or purely hierarchical memory stores don't capture the associative, evolving
structure of how humans actually reuse past experience. **Genealogy:** LLM-native, explicitly
imports the Zettelkasten note-taking method (a pre-digital knowledge-management technique) into
agent memory. **Training-free:** yes — when a new memory is added, a prompted LLM generates a
structured note (contextual description, keywords, tags), the system searches for related existing
notes and creates links, and — the distinctive step — **adding a new memory can trigger an update to
the attributes/links of OLD memories** (memory evolution), all via prompting, no fine-tuning.
**Axis/verdict:** ELEMENT (the linked-note graph) with a usage-pattern nuance: the "evolution" step
that rewrites old notes is pure LLM recombination of already-stored information — it adds
organizational structure but not new facts, so *that specific step* is usage-pattern-only; the
new-info work is done at note-creation time when a new observation first enters the store. **Fence:**
cross-session-accumulating (evaluated head-to-head with Mem0/LangMem-class systems on
LoCoMo-style benchmarks per O-Mem's comparison, see C13). **Omni role:** n/a (text-only).

**Sources:** [A-MEM: Agentic Memory for LLM Agents (arXiv:2502.12110)](https://arxiv.org/abs/2502.12110) (2025-02-17, latest rev 2025-10-08, verified via WebFetch) · [agiresearch/A-mem (GitHub)](https://github.com/agiresearch/A-mem)

**Delta vs archive:** CONFIRMS (already cited in S2 doc as the "linked notes" anti-summarization
fix); this claim adds the explicit element-vs-usage-pattern split on the "evolution" step.

---

### C5 — Generative Agents: the memory-stream/reflection/retrieval lineage root

**Problem:** believable long-horizon agent behavior needs a record of experience plus a way to
abstract and reuse it, not just a rolling context window. **Genealogy:** LLM-native (2023 root,
tagged as genealogy per recency rule) — this is the paper essentially every later memory system
(Mem0, A-MEM, LangMem, MemGPT's "reflect and evolve" phrasing) cites as ancestor. **Training-free:**
yes — three components: a **memory stream** (complete natural-language log of observations), a
**retrieval** function scoring `recency(exp-decay) + importance(LLM 1-10) + relevance(cosine)`, and
**reflection** — an LLM periodically synthesizes stored memories into higher-level abstractions,
which are themselves stored back into the stream. **Axis/verdict:** mixed, and this is the cleanest
illustration of the framework's distinction in the whole lane: the memory stream's *persistence*
(surviving past what any single context window could hold) is the ELEMENT; the reflection step is a
**usage pattern** — an LLM recombining information it (or an identical-weights copy) already
produced, with no new external fact entering the system. The paper's own ablation shows removing
reflection degrades believability, but that metric is an LLM/human-judge score, not a verifiable
task-completion ceiling — exactly the "verifier-as-role, weak" case the framework's main thesis
flags as unable to demonstrate a crossed capability boundary. **Fence:** effectively
single-continuous-session (one persistent simulated world, not discrete resumed user sessions) —
the *ancestor* of the cross-session pattern rather than a demonstration of it. **Omni role:** n/a.

**Sources:** [Generative Agents: Interactive Simulacra of Human Behavior (arXiv:2304.03442)](https://arxiv.org/abs/2304.03442) (2023-04-07, rev 2023-08-06, verified via WebFetch)

**Delta vs archive:** CONFIRMS the citation (S2 doc already cites the recency×importance×relevance
formula); the reflection-as-usage-pattern-vs-persistence-as-element split and the LLM-judge caveat
are NEW analysis for this lane.

---

### C6 — LangMem: typed (semantic/episodic/procedural) memory + namespace scoping

**Problem:** different kinds of persisted information (facts, episodes, learned procedures) need
different storage/retrieval treatment, and memory needs to be scoped so one user's history doesn't
leak into another's. **Genealogy:** LLM-native, LangChain-ecosystem-native; formalizes the
semantic/episodic/procedural taxonomy (echoing the cognitive-science taxonomy also used in the S2
memory-survey's "write-manage-read" framing) as first-class SDK primitives. **Training-free:** yes —
`create_manage_memory_tool` / `create_search_memory_tool` let an agent extract and later search
memories; memories are namespaced (commonly per-user-id) to prevent cross-user contamination; native
LangGraph `BaseStore` integration persists across server restarts. **Axis/verdict:** ELEMENT — the
namespaced persistent store is the new-info carrier; tool-based extraction/search is usage-pattern.
**Fence:** cross-session-accumulating by explicit design ("maintain consistent behavior across
sessions," persists "across server restarts"). **Omni role:** n/a. **Contrast data point:**
independent benchmarking reports LangMem's p95 LOCOMO search latency at 59.82s vs Mem0's 0.2s and
Zep's sub-second figures — a concrete illustration that "element present" is not sufficient; the
retrieval-engineering quality of the usage-pattern layer around the same class of element still
produces order-of-magnitude different deployability. **Verifier correction:** this stat was
originally cited to the vectorize.io "Mem0 vs Letta" article, but that page contains no LangMem
content and no latency figures at all (WebFetch-checked) — it only compares Mem0/Letta/Hindsight on
LongMemEval accuracy. The 59.82s/0.2s figures trace instead to a different 2026 comparison post (Y.
Yadav, "AI Agent Memory Systems in 2026: Mem0, Zep, Hindsight, Memvid..." on Dev Genius/Medium);
WebSearch corroborates the exact numbers there, but the Medium page itself could not be directly
WebFetched (paywall/redirect block), so treat this specific contrast stat as WebSearch-corroborated,
not independently WebFetch-verified — flagged rather than silently kept as a wrongly-sourced claim.

**Sources:** [langchain-ai/langmem (GitHub)](https://github.com/langchain-ai/langmem) (verified via
WebFetch) · [LangMem SDK for agent long-term memory (LangChain blog)](https://www.langchain.com/blog/langmem-sdk-launch) · [AI Agent Memory Systems in 2026: Mem0, Zep, Hindsight, Memvid and Everything In Between — Compared (Y. Yadav, Dev Genius/Medium)](https://blog.devgenius.io/ai-agent-memory-systems-in-2026-mem0-zep-hindsight-memvid-and-everything-in-between-compared-96e35b818da8) (corrected source for the latency contrast stat; not yet WebFetch-verified directly, see note above) · ~~[Mem0 vs Letta (MemGPT): AI Agent Memory Compared (2026)](https://vectorize.io/articles/mem0-vs-letta)~~ (removed — does not support the latency claim it was originally cited for)

**Delta vs archive:** **NEW** — LangMem does not appear in the S2 design doc, the S2 memory survey,
or the D2 delta scan; this is a genuinely new system added to the archive by this lane.

---

### C7 — Reflexion: the genealogy root of "usage-pattern writes new text back into an element"

**Problem:** language agents need to improve across repeated attempts at the same or similar tasks
without gradient updates, using only linguistic self-feedback. **Genealogy:** LLM-native, 2023 root
(tagged per recency rule) — the earliest clean instance of the pattern every later memory system
generalizes: an LLM **verbally reflects** on an outcome (success/failure signal), and that reflection
text is appended to an **episodic memory buffer** carried into the next trial. **Training-free:**
yes, explicitly framed as an alternative to gradient-based RL ("reinforce... not by updating
weights, but through linguistic feedback"). **Axis/verdict:** mixed — the reflection-generation step
is a usage pattern (the same frozen LLM critiquing its own prior attempt), but the buffer that
persists the resulting text **across trials** is an element (the next trial's context could not
otherwise contain last trial's outcome). The already-archived observation that "Reflexion's
append-only verbal buffer plateaus" (S2 memory survey) is the mechanism-level reason this
lineage needed Mem0/A-MEM/Zep-style curated, mutating stores rather than simple appending. **Fence:**
cross-episode/cross-session (persists across distinct task trials, not within one trial). **Omni
role:** n/a.

**Sources:** [Reflexion: Language Agents with Verbal Reinforcement Learning (arXiv:2303.11366)](https://arxiv.org/abs/2303.11366) (2023-03-20) · [noahshinn/reflexion (GitHub)](https://github.com/noahshinn/reflexion)

**Delta vs archive:** CONFIRMS (already cited by name in the S2 memory-survey's plateau claim); this
lane adds the explicit element/usage-pattern split on the reflect-vs-persist distinction.

---

### C8 — Memory-R1: the field's own evidence that a usage pattern hits a ceiling a weight update clears

**Problem:** heuristic/prompted memory-op selection (Mem0-style ADD/UPDATE/DELETE/NOOP by prompting)
may not be optimal; can the memory-manager decision itself be improved? **Genealogy:** LLM-native;
directly descends from Mem0's op taxonomy. **Training-free: NO — this is the lane's explicit
fine-tuned contrast case.** A Memory Manager and an Answer Agent are both **fine-tuned with PPO/GRPO**
outcome-driven RL (as few as 152 QA pairs) to learn when to ADD/UPDATE/DELETE/NOOP and what to
retrieve; reported gains over the prompted baseline are +28% F1 / +34% BLEU-1 / +30%
LLM-judge (LLaMA-3.1-8B backbone). **Axis/verdict:** this is the single cleanest test of the
framework's MAIN THESIS available in the memory lane: the *usage pattern* (an LLM prompted to play
"memory manager," i.e. Mem0's role) is measurably surpassed by the *same role, same job, but now
weight-updated* — which is exactly the predicted failure mode if usage-patterns over one frozen
model are bounded and crossing further requires a genuine element/weight change. Memory-R1 is
explicitly OUT of a training-free program's fence (already noted this way in the S2 design doc,
which proposes replacing its trained manager with reward-selection over candidate writes instead).
**Fence:** cross-session-accumulating (evaluated in the same LOCOMO-class multi-session memory-QA
setting as Mem0). **Omni role:** n/a.

**Sources:** [Memory-R1: Enhancing LLM Agents to Manage and Utilize Memories via Reinforcement Learning (arXiv:2508.19828)](https://arxiv.org/abs/2508.19828) (2025-08-27)

**Delta vs archive:** CONFIRMS (already named and scoped out in the S2 design doc); the explicit
"usage-pattern-ceiling-vs-weight-update" framing as direct support for the omnibus thesis is NEW
analysis this lane contributes.

---

### C9 — WavRAG: audio-native RAG is a static knowledge base, not accumulating personal memory

**Problem:** ASR-then-text RAG pipelines for spoken dialogue discard paralinguistic information,
risk transcription errors, and add latency. **Genealogy:** speech-native (audio origin domain),
transfer status untransferred-from-text in the sense that it solves a speech-specific problem (audio
RAG) rather than porting a text memory design. **Training-free:** the WavRetriever component and
audio-text joint embedding likely require their own training, but at deployment the dialogue LLM
itself is used frozen with retrieval bolted on — a "mixed" case (thin retriever trained, backbone
frozen), consistent with how the S2 memory survey already scoped WavRAG/SpeechRAG/SEAL/VoxRAG.
**Axis/verdict:** ELEMENT in the narrow sense (the audio-text knowledge base injects information the
frozen dialogue model didn't have), but **important scope caveat**: the knowledge base described is a
general text-audio hybrid corpus retrieved per-turn, not a **personalized, cross-session accumulating
user memory** — WavRAG is a knowledge-retrieval connector, not a memory-of-past-interactions system.
This distinction matters directly for the lane's "what NEW info do they add" question: WavRAG adds
KB facts per-turn; it does not accumulate anything about the specific user or conversation over time.
**Fence:** single-session (retrieval is a stateless per-query operation against a static corpus).
**Omni role:** hybrid — an audio encoder/CLAP-style component acts as sensor (embeds raw audio for
retrieval, "bypassing ASR"), the dialogue LLM acts as brain (chain-of-thought reasoning over
retrieved text+audio).

**Sources:** [WavRAG: Audio-Integrated Retrieval Augmented Generation for Spoken Dialogue Models (arXiv:2502.14727)](https://arxiv.org/abs/2502.14727) (2025-02-20, verified via WebFetch) · [ACL Anthology version](https://aclanthology.org/2025.acl-long.613/)

**Delta vs archive:** CONFIRMS the system's existence and audio-native mechanism (already cited in
S2 doc/memory-survey); the explicit "static KB, not cross-session personal memory" scope distinction
is NEW and directly motivates the negative finding in C14.

---

### C10 — MoshiRAG: async retrieval hidden in the turn-taking gap — again knowledge, not memory

**Problem:** full-duplex (always-listening, real-time) speech LMs sacrifice factuality because
scaling model size to add world knowledge breaks real-time responsiveness. **Genealogy:**
speech-native, built on the Moshi full-duplex speech LM (Kyutai); transfer status: ports the general
RAG idea into a full-duplex-specific timing mechanism that has no clean text-agent analog.
**Training-free:** mixed/contested — the front-end Moshi model provides real-time conversation and
the retrieval back-end runs asynchronously; the already-archived S2 memory-survey verifier note
flags that MoshiRAG's actual release **fine-tunes Moshi to emit retrieval-trigger tokens**, so the
policy side is weight-updating even though the retrieval-timing PATTERN (exploit the "keyword delay"
between response onset and informational content) is itself no-gradient and reusable. **Axis/
verdict:** the retrieval knowledge base is an ELEMENT; the turn-taking-gap exploitation is a
usage-pattern/scheduling trick for WHEN to consult that element without breaking real-time
interactivity — it does not itself add information. As with WavRAG, the retrieved content is drawn
from a **general knowledge/web source**, not an accumulating record of this specific user's past
sessions — no cross-session personalization is described. **Fence:** single-session (per-turn
retrieval against external knowledge/search, no persistent user-memory state). **Omni role:** hybrid
— Moshi is both sensor (full-duplex audio in) and brain (real-time response generation + interruption
handling); the async retrieval backend supplies the element.

**Sources:** [MoshiRAG: Asynchronous Knowledge Retrieval for Full-Duplex Speech Language Models (arXiv:2604.12928)](https://arxiv.org/abs/2604.12928) (2026-04-14, accepted ICML 2026, verified via WebFetch) · [kyutai-labs/moshi-rag (GitHub)](https://github.com/kyutai-labs/moshi-rag)

**Delta vs archive:** CONFIRMS (already deeply verified in the S2 memory-survey, including the
fine-tuning caveat, which this claim reuses); the "knowledge not personal memory" scope framing
parallel to C9 is this lane's contribution.

---

### C11 — VoxRAG: transcription-free speech-to-speech RAG, same scope caveat

**Problem:** ASR transcription errors and information loss degrade spoken question answering before
retrieval even starts. **Genealogy:** speech-native. **Training-free:** the pipeline (silence-aware
segmentation, speaker diarization, CLAP embeddings, FAISS cosine retrieval) uses pretrained,
off-the-shelf components at inference — no fine-tuning of a backbone LLM is described for the
retrieval path itself. **Axis/verdict:** ELEMENT (the indexed audio corpus), same scope caveat as
C9/C10: this is retrieval over a fixed audio corpus for spoken QA, not a system that accumulates
memory of a specific user across sessions. **Fence:** single-session. **Omni role:** hybrid — CLAP
audio embeddings (sensor) feed FAISS retrieval, an LLM-as-judge/answer-generator (brain) scores and
composes answers.

**Sources:** [VoxRAG: A Step Toward Transcription-Free RAG Systems in Spoken Question Answering (arXiv:2505.17326)](https://arxiv.org/abs/2505.17326) (2025-05-23, ACL 2025 Workshop MAGMaR)

**Delta vs archive:** CONFIRMS (already named in the S2 design doc's benchmark-gap paragraph); the
single-session/no-personalization scope note is this lane's addition.

---

### C12 — AFA: the closest thing to "audio-keyed memory" — and where it still falls short

**Problem:** in multi-user spoken dialogue (e.g., a shared smart-home device), an agent must avoid
attributing one resident's stated preferences to another ("persona confusion"). **Genealogy:**
speech-native problem, text-native memory solution — voice-based speaker identification is used only
as a **routing key**, and the memory objects it routes to are per-user **text** dialogue histories.
**Training-free:** mixed — the routing+memory mechanism itself is frozen-model-compatible, but the
paper's best-performing configuration **fine-tunes LLaMA-2-70B**, which is out-of-fence.
**Axis/verdict:** ELEMENT (per-user isolated memory store) gated by a usage-pattern-adjacent routing
signal (speaker embedding comparison, not itself an LLM role); raises Persona Attribution Accuracy
from 35.7% to 61.3% across five LLM backends. **Caveat carried from the r1 delta scan (D2-07):** the
PAT dataset is **synthetic** (58,289 turns, 133 profiles, 12 scenarios) — no real same-speaker,
multi-session audio was used. **Fence:** cross-session-accumulating by design intent (persistent
per-user stores), though validated only on synthetic single-dataset dialogues. **Omni role:** hybrid
— a voice/speaker-ID embedding model is the sensor that supplies the routing key; the per-user LLM is
the brain. **Precise gap this leaves open:** AFA keys memory *routing* on audio (who is speaking) but
the memory *objects* and *mutation operations* are text, not audio-native or paralinguistically keyed
(no SER/emotion key, no raw-audio memory object) — this is the sharpest concrete illustration of the
"closest attempt, still short" finding elaborated in C14.

**Sources:** [AFA: Identity-Aware Memory for Preventing Persona Confusion in Multi-User Dialogue (arXiv:2604.25022)](https://arxiv.org/abs/2604.25022) (2026-04-27, verified via WebFetch)

**Delta vs archive:** CONFIRMS (already logged as D2-07 in the r1 delta scan, same caveats
reproduced here); this lane's addition is the explicit "keys route to text, not audio objects"
framing under the element/usage-pattern template.

---

### C13 — O-Mem and Mem-PAL: the text-memory lineage keeps evolving in 2025-11 with no audio counterpart

**Problem:** semantic-grouping-based retrieval (the Mem0/A-MEM/LangMem-style default) can overlook
semantically-unrelated-but-critical user facts and introduces retrieval noise; existing systems also
under-capture users' subjective/behavioral characteristics for service-style personalization.
**Genealogy:** LLM-native, both directly benchmarked against Mem0/A-MEM/LangMem lineage.
**Training-free:** yes for both — O-Mem uses **active user profiling** (dynamically extracting/
updating user characteristics and event records from proactive interactions) plus **hierarchical,
user-centric retrieval** (persona attributes then topic-context), all via prompting; Mem-PAL
contributes **PAL-Bench** (a new benchmark: Requirement Restatement / Solution Proposal / Multi-turn
Dialogue Interaction tasks), **PAL-Set** (100 users, Chinese-language, avg. 29 sessions/user, 996
behavioral logs, 401 dialogue turns), and **H2Memory**, a hierarchical+heterogeneous RAG memory
framework. **Axis/verdict:** ELEMENT (the profile/event store and hierarchical memory framework);
usage-pattern is the retrieval hierarchy and profiling-extraction prompts. Reported gains: O-Mem
51.67% on LoCoMo (~+3pp over LangMem) and 62.99% on PERSONAMEM (+3.5pp over A-Mem). **Fence:**
cross-session-accumulating (both explicitly target "long horizon" personalization across many
sessions; Mem-PAL's PAL-Set averages 29 sessions per user). **Omni role:** n/a — both are
text/dialogue-only; **neither extends this active-profiling/hierarchical-retrieval design to audio
or paralinguistic user signals**, which is itself evidence that the text-memory research frontier is
still moving in late 2025 while no audio-native equivalent has appeared.

**Sources:** [O-Mem: Omni Memory System for Personalized, Long Horizon, Self-Evolving Agents (arXiv:2511.13593)](https://arxiv.org/abs/2511.13593) (2025-11-17) · [Mem-PAL: Towards Memory-based Personalized Dialogue Assistants for Long-term User-Agent Interaction (arXiv:2511.13410)](https://arxiv.org/abs/2511.13410) (2025-11-17, AAAI 2026)

**Delta vs archive:** **NEW** — neither O-Mem nor Mem-PAL appears in the S2 design doc, the S2
memory survey, or the D2 delta scan; both post-date the 2026-06-30/07-03 archive sweeps in spirit
even though their arXiv dates (2025-11) precede those sweeps, meaning they were simply missed
earlier and are added here. Note: despite the name "O-Mem" ("Omni Memory"), the system is **not**
multimodal/audio — "Omni" here refers to omni-purpose personalization scope, not the omni-model
sense used elsewhere in this project; flagging explicitly to avoid a false-positive audio hit.

---

### C14 — Negative finding: no system implements audio-native, cross-session memory MUTATION keyed on paralinguistic features

Across C9-C12 (WavRAG, MoshiRAG, VoxRAG, AFA) plus the r1 delta scan's independent 12-search sweep
(step1-delta-speech-agent-memory.md), **no published system combines** (a) a persistent, mutable
memory store analogous to Mem0's ADD/UPDATE/DELETE/NOOP or A-MEM's linked-note evolution, (b) keys
on **raw audio or paralinguistic features** (speaker embedding, SER/emotion, prosody) rather than
transcribed text, and (c) accumulates **across real (not synthetic) multi-session** same-speaker
interactions with verifiable ground truth (SID/SER accuracy) for admission/curation. The three
audio-native RAG systems retrieve from **static knowledge corpora** (general audio-text KBs or
web/LLM search), not from an evolving personal-memory object; the one system that keys anything on
speaker audio (AFA) routes to **text** memory objects and validates only on synthetic dialogue. This
is a **mechanism-level sharpening** of the benchmark-level gap already recorded in the archive
(S2's A1-23/A1-24: "no audio cross-session, paralinguistically-keyed memory benchmark exists"; D2-05/
06: the 2026 multimodal-memory-benchmark wave — M3Exam, SMMBench, WorldMemArena — uniformly excludes
audio) — the gap holds not only at the evaluation-benchmark level but at the **system/mechanism**
level: even setting benchmarks aside, no one has published the write-time mutation machinery over
audio-keyed objects that the text-memory lineage (Mem0→A-MEM→O-Mem) has iterated on for two years.

**Sources:** (aggregating already-cited items above) [WavRAG](https://arxiv.org/abs/2502.14727) ·
[MoshiRAG](https://arxiv.org/abs/2604.12928) · [VoxRAG](https://arxiv.org/abs/2505.17326) ·
[AFA](https://arxiv.org/abs/2604.25022) · cross-checked against [[2026-07-03-step1-delta-speech-agent-memory]]'s independent negative-search sweep (12 searches, r1 not met).

**Delta vs archive:** **NEW** framing (mechanism-level, not benchmark-level) built on CONFIRMED
underlying facts; this is the lane's single most decision-relevant finding for W4 — it identifies an
open contribution surface (a training-free, audio/paralinguistically-keyed memory-mutation
mechanism) that the existing archive had only located at the benchmark layer.

---

## Negative / empty-measurement-cells (first-class)

- No arXiv/vendor system found implementing Mem0/A-MEM-style write-time memory mutation
  (ADD/UPDATE/DELETE/NOOP or Zettelkasten-style evolution) keyed on raw audio or paralinguistic
  features, with real (non-synthetic) cross-session same-speaker data (C14).
- "O-Mem" (omni memory) is a false-positive on a name search — it is a text-only personalization
  system, not an audio/omni-modal one (C13 note); flagged to prevent citation error.
- No evidence found of any surveyed general-purpose memory system (Mem0, Letta, Zep, A-MEM, LangMem)
  natively indexing or keying on audio/paralinguistic features — all are text-first; where they are
  marketed for voice deployments (Zep/Graphiti per the CallSphere vendor post), the underlying key is
  still transcribed text (C3).
- Reflection/consolidation steps (Generative Agents' reflection; A-MEM's memory evolution) are, on
  inspection, usage-pattern recombination of already-stored facts, not new-info injection — the only
  hard evidence for a capability gain from reflection specifically is an LLM/human-judge believability
  score (soft, not a verifiable task ceiling), which the framework's own caution about verifier-as-role
  flags as weak evidence (C5).

## Summary table

| System | Origin domain | Training-free? | Axis / verdict | Fence | Omni role | Delta |
|---|---|---|---|---|---|---|
| Mem0 | LLM | yes | element | cross-session | n/a | CONFIRMS |
| Letta/MemGPT | LLM | yes | element | cross-session | n/a | CONFIRMS |
| Zep/Graphiti | LLM | yes | element | cross-session | n/a | CONFIRMS |
| A-MEM | LLM | yes | element (+usage-pattern evolution step) | cross-session | n/a | CONFIRMS |
| Generative Agents | LLM | yes | element (persistence) / usage-pattern (reflection) | single-continuous | n/a | CONFIRMS |
| LangMem | LLM | yes | element | cross-session | n/a | **NEW** |
| Reflexion | LLM | yes | element (buffer) / usage-pattern (reflect step) | cross-episode | n/a | CONFIRMS |
| Memory-R1 | LLM | **NO (fine-tuned)** | element, usage-pattern ceiling cleared by weight update | cross-session | n/a | CONFIRMS |
| WavRAG | speech | mixed | element (KB), not personal memory | single-session | hybrid | CONFIRMS |
| MoshiRAG | speech | mixed (fine-tuned trigger tokens) | element (KB), not personal memory | single-session | hybrid | CONFIRMS |
| VoxRAG | speech | yes (frozen at inference) | element (KB), not personal memory | single-session | hybrid | CONFIRMS |
| AFA | speech (routing) / text (memory) | mixed (best config fine-tuned) | element, closest audio-keyed attempt | cross-session (synthetic) | hybrid | CONFIRMS |
| O-Mem / Mem-PAL | LLM | yes | element | cross-session | n/a | **NEW** |

---

## Verifier notes (adversarial pass, 2026-07-06)

**URLs spot-checked (12 WebFetch + 2 WebSearch calls):** arXiv:2604.12928 (MoshiRAG, abstract page +
PDF + HTML full-text — 3 separate fetches), arXiv:2604.25022 (AFA), arXiv:2508.19828 (Memory-R1),
arXiv:2511.13593 (O-Mem), arXiv:2511.13410 (Mem-PAL), arXiv:2502.14727 (WavRAG), arXiv:2501.13956
(Zep), arXiv:2502.12110 (A-MEM), callsphere.ai Graphiti-voice-agents post, mem0.ai state-of-memory-2026
post, vectorize.io mem0-vs-letta, letta.com/blog/sleep-time-compute, github.com/langchain-ai/langmem,
plus WebSearch corroboration for the LangMem latency stat and the Letta no-weight-update framing.

**Findings:**

1. **Fixed — C6 miscitation.** The "LangMem p95 LOCOMO latency 59.82s vs Mem0 0.2s" contrast stat was
   sourced to `vectorize.io/articles/mem0-vs-letta`, but that page (WebFetch-confirmed, fetched twice)
   discusses only Mem0 vs Letta vs Hindsight and contains **no LangMem content and no latency
   figures**. The actual numbers trace to a different 2026 comparison post (Dev Genius/Medium, Y.
   Yadav) per WebSearch, which could not be independently WebFetched (Medium paywall/redirect block).
   Corrected the source citation in place and downgraded the claim's confidence tag to
   "WebSearch-corroborated, not WebFetch-verified" rather than deleting a plausibly-true stat outright.
2. **Fixed — C2 fabricated verbatim quote.** The claim that Letta's sleep-time-compute blog post
   contains the literal sentence "neither agent's weights are altered through this process" does not
   hold — two independent WebFetch passes over that exact URL found no such sentence. The underlying
   fact (base LLM weights are never touched; consolidation happens purely in the memory substrate) is
   true and well corroborated across docs.letta.com's sleep-time architecture page and the Letta
   developer forum, so the claim itself survives, but it was mis-presented as a single-source direct
   quote. Corrected to an honest multi-source paraphrase with the correction flagged inline.
3. **MoshiRAG fine-tuning claim (C10) — checked and CONFIRMED, initially appeared to fail.** A first
   PDF-based WebFetch pass reported "no fine-tuning, frozen heuristic-based" for MoshiRAG, which would
   have contradicted C10's "fine-tunes Moshi to emit retrieval-trigger tokens" claim. A follow-up fetch
   of the arXiv HTML rendering (better text extraction than the raw PDF) found the paper explicitly
   states "we initialize MoshiRAG with the original Moshi and make all parameters trainable" and
   introduces a special `⟨ret⟩` retrieval-trigger token learned via training on synthetic
   retrieval-augmented dialogue data. **C10's claim is correct as written; no edit needed** — logging
   this because it's a reminder that PDF-only extraction is not reliable for tool-generated summaries
   and a second-source check mattered here.
4. **All other spot-checked facts confirmed:** MoshiRAG and AFA are real, non-hallucinated arXiv papers
   at the cited (future-looking, but pre-"today") 2026-04 dates; Memory-R1's 152-QA-pair/PPO-GRPO/
   three-benchmark claims match its abstract; O-Mem's LoCoMo/PERSONAMEM numbers and text-only modality
   (the "Omni" name is confirmed not to mean audio/multimodal) match its abstract; Mem-PAL's H²Memory/
   PAL-Bench/AAAI-2026-oral status match (exact PAL-Set sub-statistics — 100 users, 29 sessions/user,
   996 logs, 401 turns — were not independently visible in the abstract-page extraction, so remain
   unverified-but-plausible pending a full-text check); WavRAG's ASR-bypass/WavRetriever claims match;
   Zep's 94.8%/93.4% DMR and 18.5%/90% LongMemEval numbers match; A-MEM's Zettelkasten/evolution
   mechanism and v1 2025-02-17/latest-rev 2025-10-08 dates match exactly; the mem0.ai 2026 report page
   and its ElevenLabs/LiveKit/Pipecat voice-integration claims are real and current (published
   2026-07-03); the CallSphere Graphiti-for-voice-agents post exists under the cited title (full body
   not rendered by the fetch, so its content beyond the headline is not independently confirmed — low
   materiality, it's cited only for a vendor-positioning point already hedged as inference in the text).
5. **Framework-verdict defensibility check (element vs usage-pattern, new-info vs read-out):** every
   verdict in the lane is internally consistent with "usage-pattern over one frozen model = read-out."
   The self-recombination cases (A-MEM's evolution step, Generative Agents' reflection, Reflexion's
   verbal self-critique, Letta's sleep-time consolidation, Mem0's router call) are all correctly a
   single frozen LLM re-reading its own already-stored content, with no outside fact entering — all
   correctly called usage-pattern. The genuine-new-info cases (Mem0/Letta/Zep/LangMem/A-MEM/O-Mem's
   persistent stores; WavRAG/MoshiRAG/VoxRAG's retrieved KB content) all inject content the frozen
   model's weights did not contain — correctly called ELEMENT, appropriately hedged where the element
   is a static KB rather than personalized memory (C9-C11) or where routing is audio-keyed but the
   memory object itself is text (C12). Memory-R1 (C8) is the one case doing real weight updates and is
   correctly flagged out-of-fence rather than mislabeled a usage-pattern. No mislabeled verdicts found.
6. **Recency and negatives check:** all non-genealogy-root sources fall in 2025-01..2026-07 (Zep
   2025-01-20 at the window's edge, MoshiRAG/AFA 2026-04 at the other edge); the three tagged genealogy
   roots (Generative Agents 2023-04, MemGPT 2023-10, Reflexion 2023-03) are explicitly labeled as such
   per the lane's own recency rule rather than silently included. The "Negative / empty-measurement-
   cells" section is present and substantive (4 first-class negatives, not an afterthought), and C14's
   negative finding is the lane's central result — negatives are not an afterthought here.

**Net assessment:** two real citation-fidelity errors found and fixed in place (a wrong-URL stat
attribution in C6, a fabricated verbatim quote in C2); both survived as true claims once corrected —
neither was an invented fact, both were sourcing/quotation-fidelity failures. No framework-verdict
miscalls found. No dead links found among the 12 URLs fetched. Recency and negative-finding coverage
both pass.
