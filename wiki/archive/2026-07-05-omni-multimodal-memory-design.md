---
title: "Omni multimodal memory system — operation primitives (referencing mem0 & advanced memory components)"
date: 2026-07-05
stage: 1-design (argumentation)
purpose: "A multimodal MEMORY system (NOT RAG) to augment/compensate the frozen omni's KNOWLEDGE boundary (the TH2a shared-knowledge floor), respecting the information-boundary discipline (external knowledge, never the test item's transcript)."
---

# Omni multimodal memory — operation primitives (reference-informed design)

> **Frame (owner 2026-07-05).** Not RAG — a **multimodal memory system** that augments/compensates the
> omni's **knowledge boundary**. Legitimate (vs the retracted M3): it injects **external knowledge keyed
> by the input**, never the test item's golden transcript. We reference **mem0** and better memory
> components for the operation primitives rather than inventing them. Continues
> [[2026-07-05-A-realization-conclusion]] (Q1b) and the parked W4 bridge (task #37).

## 1. Reference primitive taxonomy (mem0 + advanced components)

| Primitive | mem0 | MemGPT/Letta | Zep/Graphiti | Generative Agents | LangMem |
|---|---|---|---|---|---|
| **ENCODE/EXTRACT** (write) | LLM distills raw → atomic facts (not append) | — | entity/relation extraction | observation → memory | typed extraction |
| **CONSOLIDATE** (update) | **ADD/UPDATE/DELETE/NOOP** vs similar (dedup/conflict) | self-edit via tools | temporal invalidation of superseded facts | — | background consolidation |
| **RETRIEVE** (search) | vector semantic | tiered paging (core↔archival) | graph + temporal | **relevance × recency × importance** | typed retrieval |
| **REFLECT/ABSTRACT** | — | — | — | **synthesize higher-level memories** | procedural distillation |
| **INJECT/USE** | context | function-call return | context | context | context |
| **FORGET/DECAY** | delete | paging-out | **bi-temporal invalidation** | recency decay | — |
| **SCOPE/TYPE** | user/agent/run + **mtype** | core/archival tiers | graph namespaces | — | **semantic/episodic/procedural** |
| **normalization** | **→ canonical English text** | — | — | — | — |

**Synthesized reference skeleton (7 primitives):** ENCODE · CONSOLIDATE · RETRIEVE · REFLECT · INJECT ·
FORGET · SCOPE/TYPE. mem0 is strongest on ENCODE+CONSOLIDATE+normalization; borrow REFLECT (Gen-Agents),
self-editing/tiering (MemGPT), temporal invalidation (Zep), and the semantic/episodic/procedural TYPING.

## 2. Multimodal deltas — how each primitive changes when the input is AUDIO

| Primitive | Text-memory (mem0) | **Omni multimodal adaptation** |
|---|---|---|
| **ENCODE** | text → atomic fact | (audio, answer) → **key = W4-disentangled speech sub-key(s)**; **value = LLM-extracted text knowledge / handling-pattern** (cross-modal distillation: audio understanding → symbolic knowledge) |
| **CONSOLIDATE** | dedup on text fact | **dedup on the VALUE (knowledge) semantics, NOT the acoustic key** — two different audios can carry the same knowledge. Key-space = retrieval; value-space = dedup/conflict. Clean separation. |
| **RETRIEVE** | query text → vector | query audio → **W4 sub-key → key-space similarity, task-relevant sub-key** (content-key for content tasks, intent-key for SLU…). Cross-modal: audio-key → text-value |
| **REFLECT** | — | abstract "**this class of audio-question → this handling pattern**" = the persistent form of the task-definition few-shot (procedural memory) |
| **INJECT** | text context | **text-value into the frozen omni's context** — external knowledge, **NOT the input's transcript** (the legitimacy line vs M3). Optimize the injection FORMAT. |
| **FORGET** | delete | temporal invalidation for evolving domains (Zep-style); a static knowledge base mostly ADDs |
| **SCOPE/TYPE** | mtype | **semantic** (facts) / **episodic** (specific experiences) / **procedural** (task-handling patterns), partitioned by task family |

## 3. The KV design decision (LOCKED by owner 2026-07-05)

- **key = a COMPRESSED speech embedding from a UNIFIED encoder (try unified FIRST).** Speech signals are
  long → **compression is mandatory** (owner): the long query audio → a compact key vector. Start with
  **one unified encoder**; only if retrieval is not task-relevant enough do we split (→ W4-disentangled
  per-task sub-keys as the FALLBACK read-out lever, not the starting point). The key is derived from the
  QUERY audio (legitimate — processing the input, not leaking the answer).
- **value = a DICT, NOT a single canonical string** (owner). One memory entry's value = `{(task, language)
  → text content}` — a multi-faceted store so **different tasks and different languages each access the
  corresponding content**. No speech kept in the value (owner: 不保留语音). This dissolves the
  normalization question: don't force one canonical form — store multiple views, let the usage strategy
  pick the right facet. The text content is **EXTERNAL knowledge** (from training/a source), **never the
  test input's transcript** — the M3 line; it is the **NEW-INFO lever** that beats the TH2a knowledge floor.
- So the entry is: **key = unified compressed speech vector · value = dict{(task,lang) → external-knowledge text}.**

## 4. The THREE core strategies (owner 2026-07-05) — the training-free-RL action space, step by step
Owner reduces the 7 primitives to the **three that matter**, explored **step by step**; each is a
training-free-RL-optimizable strategy (reward-guided selection, no weight change) — the concrete form of
the "adjust A" object from Phase-2:

1. **压缩策略 · Compression** (mandatory — speech is long): query audio → **compact key**; and knowledge →
   a **compressed value dict**. Sub-questions: unified encoder feasible? how much compression? what to keep.
2. **检索策略 · Retrieval**: compressed query key → memory search — k, similarity, task/language filtering.
3. **使用策略 · Usage/Injection**: pick the **(task, language) facet** from the retrieved value dict and
   inject it — format, position, how many, when to trust it.

**Step-by-step exploration plan (Stage-1, small legitimate probes; memory built ONLY from training data,
never the test item):**
- **Step 1 — Compression feasibility (unified key).** Build a compact **unified** speech-key index over a
  training pool; test whether it retrieves **task-relevant** neighbors (not just acoustically similar). If
  yes → unified encoder is enough; if no → fall back to W4-disentangled per-task sub-keys. Also fix a
  value-compression (mem0-style extract of the knowledge into the dict).
- **Step 2 — Retrieval strategy.** Given the compressed keys, tune k / similarity / (task,language)
  filtering; measure retrieval hit-rate for the knowledge a query needs.
- **Step 3 — Usage strategy.** Inject the retrieved (task,language) facet into the frozen omni; does it
  recover the **knowledge-gap** headroom (the T5 component)? Optimize the injection by reward.
Each step reports on the knowledge-gap headroom, with the information-boundary audit (no test-item leakage).

## 5. Division of labor (theory-aligned)
- **W4-disentangled key** = READ-OUT lever → better retrieval / perception-facing (cannot add knowledge).
- **external-knowledge value** = NEW-INFO lever → beats the TH2a knowledge floor.
- Both respect the information boundary (external knowledge, input-keyed, no answer leakage).

## 6. Design decisions — RESOLVED (owner 2026-07-05)
1. **value = text only, NO speech kept.** ✓
2. **key: try a UNIFIED encoder first**; split per-task (→ W4 disentangled sub-keys) only if unified
   retrieval is not task-relevant enough. ✓
3. **Compression is mandatory** (speech is long) — must compress before use; ENCODE = compress. ✓
4. **CONSOLIDATE key/value separation: not locked — proceed with the current idea** (value-space dedup). ✓
5. **Three core strategies, step by step: compression · retrieval · usage** — these are the heart. ✓
6. **value = a DICT** `{(task, language) → text content}` — different tasks/languages access their facet;
   this replaces "normalize to one canonical form." ✓

## 7. Reference reading (to study for the fuller design — Stage-1 survey)
mem0 (extract + ADD/UPDATE/DELETE/NOOP consolidation + normalize) · MemGPT/Letta (tiered self-editing
memory-as-tool) · Zep/Graphiti (bi-temporal knowledge graph + invalidation) · Generative Agents
(relevance×recency×importance + reflection) · LangMem (semantic/episodic/procedural typing) · A-MEM
(linked evolving notes). **Multimodal-specific gap:** none of these handle a **speech key → text-knowledge
value** cross-modal store with **disentangled task-relevant keys** — that is our novel contribution surface.
