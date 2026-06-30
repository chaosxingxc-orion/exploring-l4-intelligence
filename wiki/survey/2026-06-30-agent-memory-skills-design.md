# S2 deepening — Memory & Skills design for a training-free speech agent

> Design synthesis from the **S2 deepening** survey (memory + skills lanes; run `wf_a066da37-c09`,
> 2026-06-30; 43 verified claims / 70 sources). Lanes:
> [agent-memory](2026-06-30-survey-agent-memory.md) · [agent-skills](2026-06-30-survey-agent-skills.md).
> Companion: [[2026-06-30-agent-level-synthesis]] (S1 GO) · [[2026-06-30-survey-agent-convergence]] (θ2).
> **Survey-first / design-only — not a thesis change.** All links real & adversarially verified.

## The one control law (the key S2 finding)
**A verifiable-reward acceptance gate is the single most important mechanism for BOTH memory and skills.**
θ2 showed append-only memory doesn't compound; **SkillsBench** (arXiv:2602.12670) now proves the same for
*skills* — self-generated skills give **~0 net benefit (16/84 negative-delta)**, curated-through-a-gate give
**+16.2pp**. And θ2's abstract **β-KL trust region** has two concrete no-gradient instantiations: bound the
**memory-mutation rate** (Mem0 `{ADD/UPDATE/DELETE/NOOP}` op-count) and **GEPA Pareto-front non-regression**
for skill-text updates. Both reuse the project's existing assets — **frozen Omni-Embed-Nemotron as the index,
W1's verifiable speech rewards (WER/ASR/ST/SER/SID/intent) as the gates.**

## Memory component (design)
**Frozen omni bi-encoder = index; external curated store = what compounds, mutated under verifiable rewards.**
- **Three-tier structured store** (never a flat append buffer; consolidation is *not* automatic, arXiv:2603.07670):
  episodic spoken-turn stream · semantic per-speaker persona (MemoryOS paging, 2506.06326) · procedural skill
  library (→ skills). Hold episodic+semantic in **one bi-temporal KG** (AriGraph 2407.04363; Zep/Graphiti
  validity-intervals 2501.13956) with A-MEM linked notes (2502.12110) so a new turn re-tags rather than
  summarizes-over.
- **Index on AUDIO, not ASR text** (WavRAG 2502.14727; VoxRAG 2505.17326) via the frozen **Omni-Embed-Nemotron**
  (2510.03458). **Composite key = (speaker-ID, emotion/SER, turn, content)** from frozen diarization + x-vector +
  SER (pyannote/SpeechBrain) — keys are **dual-use**: retrieval keys *and* verifiable reward signals.
- **Two-stage retrieval** (omni bi-encoder recall → cross-encoder/ColBERT rerank), first-pass score =
  `recency(decay) × importance × relevance`, with **importance set from verifiable reward** (a turn that
  resolved a high-WER ambiguity is high-importance) not an LLM rating (Generative-Agents 2304.03442).
- **Anti-collapse curation** (each θ2 failure mode → a no-gradient fix): non-destructive `{ADD/UPDATE/DELETE/
  NOOP}` (Mem0 2504.19413) vs plateau; incremental deltas (ACE 2510.04618) vs context collapse; bi-temporal
  `invalid-after` (Zep) vs contamination; **provenance + trust score + decay** vs poisoning (AgentPoison
  2407.12784) — only reward-verified turns become high-trust memories.
- **Credit assignment without gradients:** replace Memory-R1's PPO-trained manager (2508.19828, out-of-scope)
  with **verifiable-reward best-of-N selection over candidate memory-writes** (W1 reward machinery); **bound the
  mutation rate with a β-KL trust region** (JitRL slow-drift). Consolidation runs **off the critical path**
  (Letta sleep-time; MoshiRAG hides it in the turn-taking gap, 2604.12928).
- **Benchmark gap (open contribution):** no audio cross-session, paralinguistically-keyed memory benchmark
  exists (LongMemEval/LoCoMo text; Mem-Gallery/Omni-SimpleMem vision+text; A-MBER text-emotion 2604.07017). A
  speech one needs raw-audio multi-session dialogue + speaker/SER-keyed queries + verifiable SID/SER ground
  truth + contamination/poisoning probes; report maintenance latency + multi-backbone (Anatomy audit 2602.19320).

## Skills component (design)
**A speech skill = `(applicability Condition, execution Policy, Termination, Reusable I/O)`** (SoK 2602.20867),
packaged as a **SKILL.md** progressive-disclosure folder (frontmatter = paralinguistic trigger keys; body =
verified routine; scripts/ = correction/tool code). Speech `π` instantiations: in-context **GER ASR-correction**
over N-best (2505.17410), voice **tool-use/dialogue** (AURA 2506.23049; Full-Duplex-Bench-v3 2604.04847;
τ-Voice 2603.13686), **paralinguistic S2S** (ParaS2S 2511.08723).
- **The verification gate (core control law):** admit a skill only if a **verifiable speech reward** beats the
  no-skill baseline by a positive delta on held-out trigger probes; **deprecate** when running reward-delta goes
  negative (SkillsBench 2602.12670). Replaces Voyager's LLM self-critic (2305.16291) with cheaper objective
  rewards. **When labels are scarce**, co-evolve a **surrogate verifier** (CoEvoSkills 30.6→71.1%, no ground
  truth, 2604.01687) — instantiate as the **frozen omni bi-encoder** scoring SpeechBERTScore-style consistency.
- **Selection = body-first** retrieve-and-rerank (full skill BODY is decisive; removing it costs 29–44pp,
  SkillRouter 2603.22455) over the omni bi-encoder index, with paralinguistic state as a **filter**.
- **No-gradient improvement + trust region:** **GEPA** reflective Pareto prompt evolution (beats GRPO, 35×
  fewer rollouts, 2507.19457) — accept an UPDATE only on **Pareto-front non-regression** (= the β-KL trust
  region against context collapse); **AFlow/AgentSquare** MCTS workflow search over recombinable speech modules
  (2410.10762/2410.06153).
- **Bloat control:** hierarchical composition with **selective injection** (AWM snowball, 2409.07429); dedup via
  **polymorphic abstraction** (per-accent skills → one AbstractASRCorrection parent, PolySkill 2510.15863) +
  CRAFT validate+dedup (2309.17428); deprecate on negative reward-delta.

## Open-source map (frozen, no-gradient, usable)
**Memory:** Omni-Embed-Nemotron (index) · Mem0 (write-API) · Graphiti/Zep (bi-temporal KG) · HippoRAG (PPR
retrieval) · pyannote+SpeechBrain (paralinguistic keys) · A-MEM (linked notes) · MemoryOS (paging) · AgentPoison
(red-team). **Skills:** CoEvoSkills (surrogate gate) · SkillRouter (body-first select) · anthropics/skills
(SKILL.md) · CRAFT (dedup) · Voyager (library ref) · GEPA (text opt) · AFlow+AgentSquare (workflow opt) · AWM
(composition).

## Belief updates (→ strategic memo)
- **A1/A2 resolved (design-ready):** both components have buildable no-gradient designs on the project's existing
  frozen assets; the verifiable-reward gate + β-KL trust region are the shared control law.
- **The benchmark gap is the concrete novel-contribution surface** (a speech cross-session, paralinguistically-
  keyed memory benchmark — none exists).
- **Top open questions:** one fused vs two independent trust regions (memory-rate + skill-Pareto) under JitRL's
  single-state slow-drift precondition; whether the omni-bi-encoder surrogate verifier correlates tightly enough
  with true WER/intent/SER; and the paralinguistic-state feedback loop (a mis-estimated SER label mis-routes
  memory/skills *and* mis-rewards admission).
