---
title: "Memory-system organizational-form comparison (text + multimodal) vs our locked design"
date: 2026-07-06
stage: 1-argumentation
status: "Stage-1 WS-A deliverable (workflow wf_fbbba6a0, 11 system + 2 verify + 2 synth agents; recovered via resume after a mid-run agent hang). Adversarial + citation verified; hypothesis-grade. Owner review pending; wiki-sync deferred."
---

> ⚠️ **概念归档更正(2026-07-06).** 本文实为**知识(Knowledge)元件**分析,曾错标为"记忆":对比的 11 个系统里 7 个是"召回自身历史"的 episodic 系统(那是**记忆**的对标类),被用来判一个**知识**设计的净新——属对标错类(详见本文 §2 轴 #7 与 [[2026-07-06-capability-taxonomy-knowledge-skill-memory]] §5)。**记忆(实例召回)与技能(任务模板)本文并未覆盖。**

# Memory-System Organizational-Form Comparison

*Stage-1 deliverable (problem-definition / 问题定义). Hypothesis-grade: this is an argumentation survey, not an experiment — every cell is grounded in a real arXiv ID or repo, and residual uncertainty is flagged inline. Verification corrections have been folded in (see the "Verification folded in" note at the end).*

**Purpose.** Characterize the *organizational form* of representative memory systems (text and multimodal) against a fixed set of primitives, so we can locate our locked design precisely and adjudicate its novelty adversarially.

**Our locked design (the reference point — its novelty is judged in §3, not assumed):**
- **KEY** = a *compressed unified speech embedding* derived from the **query audio** (fallback: W4-disentangled per-task sub-keys). Frozen, untrained.
- **VALUE** = a **dict `{(task, language) → external-knowledge TEXT}`**; no speech stored.
- **Action space** = three *training-free* strategies selected by a **verifiable reward** signal: **Compression, Retrieval, Usage/Injection.**
- **Boundary rule**: inject *external* knowledge only — never the test item's own transcript/answer (leakage).

---

## 1. Comparison table

Two parts, same row order (S1–S11). **Benchmarks (S9, S10) are not memory engines** — they persist nothing; they are included for the multimodal-memory-demand landscape and are *excluded* from the store-level novelty adjudication in §3.

### Part A — the 7 primitives

| # | System (source) | ENCODE | CONSOLIDATE | RETRIEVE | REFLECT | INJECT | FORGET | SCOPE |
|---|---|---|---|---|---|---|---|---|
| S1 | **mem0 / mem0ᵍ** (arXiv 2504.19413; `mem0ai/mem0`) | LLM extraction of salient facts from recent msg-pair + rolling summary | UPDATE phase: LLM tool-call picks ADD/UPDATE/DELETE/NOOP vs top-s=10 similar | Dense semantic top-k (Qdrant); mem0ᵍ = triplet graph traversal | None (rolling summary + consolidation only) | Prepend top-k NL facts to prompt (RAG) | LLM DELETE on contradiction; no decay | Episodic, cross-session; user/agent/run/app ids |
| S2 | **MemGPT / Letta** (arXiv 2310.08560; `letta-ai/letta`) | LLM self-write via function calls + auto event log | Context-pressure recursive summarization + FIFO eviction | LLM-invoked archival semantic search + conversation_search | Inline "inner-monologue" self-edit; no offline insight pass | Always-in-context core blocks + paged function returns | Eviction to recall store (not deletion); bounded core blocks | Agent-scoped, persistent; optional shared blocks |
| S3 | **Zep / Graphiti** (arXiv 2501.13956; `getzep/graphiti`) | Ingest episode → LLM entity+edge extraction; bi-temporal stamps; 1024-d embeds | Entity resolution (cosine+BM25+LLM merge) + label-prop community summaries | Hybrid cosine + BM25 + BFS; RRF/MMR/cross-encoder rerank (<200 ms p95) | LLM contradiction detection + community/entity summaries | Return fact/entity/community text to context | Soft temporal invalidation (t_invalid); no hard delete | Persistent per-user/session/group graph |
| S4 | **Generative Agents** (arXiv 2304.03442; `joonspk-research/generative_agents`) | Append-only memory-stream nodes (NL + timestamps + poignancy + SPO) | Reflection tree + recursive plan decomposition (abstract, not merge) | Score = recency(0.995 decay)+importance+relevance(cosine), all α=1 | **YES — headline**: importance>150 → 3 questions → ~5 cited insights | Serialize top nodes into prompt | None hard; soft recency-decay demotion | Per-agent, long-lived, cross-episode |
| S5 | **LangMem** (`langchain-ai/langmem`) | LLM memory-manager extracts (hot-path tool or background); embed content (1536-d) | Enrichment: create/update/invalidate/delete/consolidate; debounced ReflectionExecutor | Top-k cosine over BaseStore + UUID lookup + metadata filter | Background reflection + prompt-optimizer (metaprompt/gradient) | Prepend retrieved text; procedural memory = rewritten system prompt | Explicit LLM delete/invalidate; no TTL | Hierarchical namespaces, multi-tenant, cross-session |
| S6 | **A-MEM** (arXiv 2502.12110; `agiresearch/A-mem`) | LLM authors structured note (content+kw+tags+context); embed concat (all-MiniLM-L6-v2, 384-d; ChromaDB) | Link generation: bidirectional links to top-k=10 neighbors (Zettelkasten graph growth) | Top-k cosine kNN (search default k=5) | **YES — "memory evolution"**: new note triggers LLM rewrite of neighbors' context/tags | Concat retrieved notes' text into prompt | None in paper (manual delete API only) | Per-agent episodic self-history (LoCoMo) |
| S7 | **Cognee / Memary** (`topoteretes/cognee`; `kingjulio8238/Memary`) | Cognee cognify() LLM entity/rel → DataPoints; Memary auto-captures ReAct entities + stamps | Cognee 3 stores (relational+vector+graph) + memify ontology; Memary Memory Stream + Entity KB (freq/recency) | Cognee auto-routed vector+graph; Memary recursive multi-hop subgraph (depth 2) | Cognee improve()/memify ontology refine; Memary freq/recency salience | Graph triples + vector hits into prompt (graph-RAG) | Cognee first-class forget(); Memary recency decay + history compression | Persistent per-agent/user KG; Cognee session vs permanent modes |
| S8 | **AFA** (arXiv 2604.25022) | Dual encode: ECAPA-TDNN voiceprint (identity) + ASR transcript (content); only text persists | Per-user isolated store {persona, history}; write pipeline **not documented** | 2-stage: cosine speaker-ID match → discrete **User ID** → **exact-key** store route | **Not documented** | User's persona+history into prompt (template not documented) | **Not documented** (no eviction/TTL stated) | Per-user / identity-scoped, multi-user, cross-session |
| S9 | **AudioMC** *(benchmark)* (arXiv 2512.14865; `ScaleAI/audiomc`) | n/a — cue planted in early-turn audio; model's own front-end | n/a — transient in-context only | n/a — in-context recall, no store | n/a | n/a — full history in context only | n/a — single session ≤8 turns | Single-session multi-turn, ephemeral |
| S10 | **MTalk-Bench** *(benchmark)* (arXiv 2508.18240; `FreedomIntelligence/MTalk-Bench`) | n/a — 3-turn dialogue fed to frozen S2S | n/a | n/a — implicit attention over context | n/a (judge meta-analysis only) | n/a — prior turns as history | n/a | Single 3-turn dialogue, ephemeral |
| S11 | **Audio-native RAG**: WavRAG (arXiv 2502.14727) + SpeechRAG (arXiv 2412.16500) | **Trained** encoders: WavRAG LoRA Qwen2-Audio (r=8, audio-encoder frozen) last-token vec; SpeechRAG HuBERT+adapter, text query via frozen E5-Mistral | Offline static index build; no online writes/merging | Cosine top-k kNN; WavRAG S→T/T→S/S→S; SpeechRAG text-query→audio-passage | None at memory level (WavRAG adds gen-time CoT + self-consistency) | Concat retrieved + query → **frozen** generator (GPT-4o / Qwen2-Audio / Qwen-Audio-Chat) | None (static corpus) | Global corpus-level KB, not episodic |

### Part B — key / value / modality / training-free / verifiable-reward

| # | System | KEY structure | VALUE structure | Modality | Training-free | Verifiable-reward |
|---|---|---|---|---|---|---|
| S1 | mem0 / mem0ᵍ | Dense **text**-embedding vector (mem0ᵍ: entity nodes + (src,rel,dst) triplets) | Canonical NL fact + metadata (mem0ᵍ: labeled triplet) | text-only | **yes** (frozen LLM+embedder; prompt-engineered) | **no** |
| S2 | MemGPT / Letta | Symbolic **label** (core blocks) + **text** embedding (archival) | Free-form text blocks / passages / event records | text-only | **yes** | **no** |
| S3 | Zep / Graphiti | Text-derived triple index: 1024-d embeds + BM25 + graph topology | Bi-temporal **typed KG** (episodes/entities/facts-as-SPO/communities) | text-only | **yes** | **na** (no optimization loop) |
| S4 | Generative Agents | **Composite**: text embedding + recency scalar + importance scalar | Autobiographical memory object (NL + poignancy + SPO + evidence links) | text-only | **yes** | **no** (poignancy = LLM self-rating) |
| S5 | LangMem | UUID (storage) + **text** embedding 1536-d (retrieval) | JSON/Pydantic text, typed by kind (semantic/episodic/procedural) | text-only | **yes** | **no** (optional human/LLM feedback, not RL) |
| S6 | A-MEM | 384-d **text** embedding over the note's *own* concatenated text | Structured self-note (content+kw+tags+context+links) | text-only | **yes** | **no** |
| S7 | Cognee / Memary | **Text** embeddings + LLM-extracted **entity graph** nodes | Property/knowledge **graph** (retains ingested source) | text-only¹ | **yes** | **no** |
| S8 | AFA | Speaker **voiceprint** → collapsed to a **discrete User ID** (exact-match) | Per-user {persona, dialogue history} — the user's *own* text | audio-in → text-out | **partial** (top config LoRA-tunes LLaMA-2-70B) | **no** (PAA is eval-only) |
| S9 | AudioMC *(bench)* | None (implicit conversation position) | None (per-instance rubrics = grading ground-truth only) | cross-modal | **yes** (eval, frozen) | **no** (LLM-judge rubric grading) |
| S10 | MTalk-Bench *(bench)* | None | None (hierarchical binary rubrics; grading only) | cross-modal | **yes** (eval, frozen) | **no** (Arena Elo + rubric, subjective) |
| S11 | Audio-native RAG | **Audio/text dense vector** in a shared space (**trained** retriever) | The retrieved corpus item — **includes raw AUDIO** (SpeechRAG value = audio; WavRAG = audio/text/multimodal) | cross-modal (audio-native) | **partial** (retriever trained; generator/injection frozen) | **no** (supervised InfoNCE / cosine-distillation, not RL) |

¹ *Cognee documents audio among ingestible input formats but processes it into text/graph — it has no speech-native retrieval key, so it is not speech-keyed in our cross-modal sense.*

---

## 2. Design axes the field varies along

Across these systems the organizational form decomposes into ~9 orthogonal axes; every surveyed system is one point in this space:

1. **Write / consolidation policy** — *append-only* (Generative Agents, A-MEM) → *LLM-adjudicated reconcile* (mem0's ADD/UPDATE/DELETE/NOOP, LangMem enrichment, Zep entity resolution) → *context-pressure summarization + eviction* (MemGPT) → *offline static index* (Audio-native RAG). This is the most-varied axis.

2. **Key structure** — *single dense vector* (mem0, A-MEM, LangMem) → *composite score* (Generative Agents: embedding + recency + importance) → *symbolic label* (MemGPT core) → *graph topology / hybrid lexical+dense+BFS* (Zep, Cognee) → *discrete-ID exact-match route* (AFA) → *none / positional* (benchmarks). **Every non-benchmark key is ultimately derived from TEXT, except AFA's, which is a speaker voiceprint collapsed to an ID.**

3. **Value structure** — *flat NL fact* (mem0) → *free-text blocks/passages* (MemGPT, LangMem) → *typed bi-temporal KG* (Zep, Cognee/Memary) → *structured self-note* (A-MEM) → *autobiographical object with links* (Generative Agents) → *raw audio document* (SpeechRAG). **No surveyed system organizes the value as a `{(task, language) → text}` dict.**

4. **Retrieval mechanism** — pure dense kNN → multi-signal score (Generative Agents) → hybrid dense+lexical+graph with reranking (Zep) → exact-key ID route (AFA).

5. **Reflection** — *none* → *inline self-edit* (MemGPT) → *insight synthesis* (Generative Agents) → *note evolution / neighbor rewrite* (A-MEM) → *prompt optimization* (LangMem). Where present it is always **LLM-heuristic**, never reward-driven.

6. **Forgetting** — *none / append-only* → *contradiction-driven delete* (mem0) → *soft temporal invalidation* (Zep) → *eviction+compression* (MemGPT) → *recency-decay demotion* (Generative Agents) → *first-class forget()* (Cognee).

7. **Provenance of stored content (leakage-relevant axis)** — *self-history / personalization* (mem0, MemGPT, Generative Agents, A-MEM, LangMem, AFA, Cognee/Memary — the memory is the user's/agent's own past) vs. *external corpus knowledge* (Audio-native RAG; Zep partial). **Only the RAG family injects outside knowledge**; all the agent-memory systems recall self-content by design — the opposite pole from our external-knowledge goal.

8. **Modality** — *text-only* (S1–S7) → *audio-front-end → text store* (AFA) → *cross-modal audio-native store* (Audio-native RAG) → *cross-modal benchmark, no store* (AudioMC, MTalk-Bench).

9. **Optimization signal for memory actions** — *LLM heuristic* (S1–S8) vs. *supervised contrastive/distillation* (S11) vs. *verifiable-reward / RL* (**none — an empty column across the entire survey**).

---

## 3. Novel-cell judgment for our design (adversarially checked)

Our design is a **conjunction** of four elements. Adjudicating each against the survey (benchmarks S9/S10 excluded — they persist nothing):

| Element of our design | Verdict | Grounds |
|---|---|---|
| (a) Cross-modal **audio-query → text-knowledge** retrieval, *as a bare capability* | **REFUTED as novel** | WavRAG's Speech→Text scenario already retrieves TEXT knowledge from an audio query with a **frozen generator** (arXiv 2502.14727). Generic "cross-modal speech-key → text-value store" is **not** the novel cell; we must not claim it. |
| (b) A **frozen, untrained** speech key | **Survives (absence-of-evidence)** | WavRAG LoRA-tunes its retriever (Qwen2-Audio, projection+LLM, r=8; audio-encoder frozen); SpeechRAG trains a HuBERT adapter via cosine-distillation. AFA's ECAPA-TDNN is pretrained/frozen but is a **speaker** encoder collapsed to a discrete ID, not a content/task retrieval key. No surveyed system has a fully-frozen, untrained *content* speech key mapping to a text-knowledge store. |
| (c) VALUE = **`{(task, language) → text}` dict** with **W4-disentangled per-task sub-keys** | **Survives (absence-of-evidence)** | No surveyed system — text or audio — structures its value as a task×language dictionary or decomposes the key into disentangled per-task sub-keys. Values are flat facts, free-text blocks, typed KGs, self-notes, or raw audio. |
| (d) **Reward-guided, training-free (RL)** selection among Compression/Retrieval/Usage | **Survives — cleanest, wholly-unrefuted differentiator** | The verifiable-reward column is empty across all 11 systems. Memory actions are chosen either by **LLM heuristic** (S1–S8) or by **supervised** contrastive/distillation training (S11, WavRAG/SpeechRAG) — never by a verifiable-reward/RL loop. Since the project thesis is literally *training-free RL*, this is the lead novelty pillar. |

**Overall verdict — ABSENCE-OF-EVIDENCE for the full conjunction (not "confirmed novel").**
No surveyed system refutes the *complete* locked design: frozen/untrained speech key **+** `{(task,language)→text}` dict with disentangled sub-keys **+** reward-guided training-free action selection. But this is *element-oriented* search over named systems — it supports "no counterexample found for the specific conjunction," and cannot prove non-existence of an unpublished or differently-named system. State it at that altitude.

**Two nearest non-refuting precedents (name these, don't hand-wave):**
- **AFA (arXiv 2604.25022) — closest *structural* precedent** (a speech-derived-key → text-value store, mostly frozen). Non-refuting for three verified reasons: (i) it keys by **speaker identity collapsed to a discrete User ID** (exact-match route, confirmed in the PDF), not a continuous content/task embedding; (ii) its value is the user's **own history** (personalization), not external knowledge; (iii) its top config **LoRA-tunes LLaMA-2-70B**, so it is only *partially* training-free.
- **WavRAG (arXiv 2502.14727) — closest *cross-modal retrieval* precedent** (audio-query → text-knowledge, frozen generator). Non-refuting because its **retriever is LoRA-trained (r=8)**, not frozen, and it has no `(task,language)` value structure, no compression action, and no reward loop.

**Lead the novelty argument with pillar (d)** — reward-guided training-free selection — flanked by (b) frozen key and (c) task×language dict. Do *not* headline generic cross-modality; that cell is refuted.

---

## Residual uncertainty (flagged, not papered over)

- **AFA**: memory *write/consolidation* pipeline, the "adaptive-persona" update rule, the injection prompt template, and any forget/eviction policy are **not documented** in the paper; no code/dataset release URL stated. The discrete-User-ID keying and LoRA-partial training *are* confirmed at PDF body level.
- **MTalk-Bench**: the "9 Tier-1 capabilities (incl. Understanding & Memory)" and "~270 dialogues / 3-turn" figures are **full-paper-only claims** (HTML/GitHub), possibly conflating "9 scenarios" with "9 capabilities" — re-verify before citing. Does not affect the §3 verdict (benchmark, stores nothing).
- **WavRAG**: the load-bearing "retriever LoRA-tuned, r=8; audio-encoder frozen" fact is sourced from the full-paper HTML, not the abstract — it is what preserves pillar (b), so cite it from the paper body / repo, not the abstract.
- **AudioMC**: the "Scale AI / SEAL" attribution derives from the `ScaleAI/audiomc` dataset namespace + `scale.com/leaderboard/audiomc` provenance, not from an explicit statement in the arXiv abstract.
- **A-MEM**: the correct evaluation repo is `github.com/WujiangXu/A-mem` (or `WujiangXu/A-mem-sys`); the primary implementation `agiresearch/A-mem` is confirmed (ChromaDB + all-MiniLM-L6-v2 + Zettelkasten linking).
- **Search-scope limit**: element-oriented counterexample hunting cannot establish global non-existence; the §3 verdict is bounded to the surveyed, named systems.

---

*Verification folded in: broken A-MEM eval-repo URL corrected; Cognee "no audio" softened to "audio ingested but transcribed, no speech-native key"; AudioMC attribution marked inferred-from-provenance; novelty claim narrowed from generic cross-modality (refuted by WavRAG) to the frozen-key + task×language-dict + reward-guided conjunction; reward/RL axis promoted to lead pillar; AFA and WavRAG named as the two nearest non-refuting precedents; benchmarks excluded from store-level adjudication. All 10 cited arXiv IDs and all listed repos were confirmed to exist and match the attributed mechanisms; the three future-dated IDs (AFA 2604.*, AudioMC 2512.*, MTalk-Bench 2508.*) are real relative to today (2026-07-06), not hallucinated.*
