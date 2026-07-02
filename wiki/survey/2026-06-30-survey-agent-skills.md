# S2 · A2 — Agent skills (deep design + speech instantiation)

> Part of **S2 deepening** (memory + skills design) of [[2026-06-30-agent-level-synthesis]]. Run `wf_a066da37-c09`, 2026-06-30. Per-lane adversarial verification; only `keep=true` archived; links real. Each claim tagged **scope** (no-gradient = in / weight-updating = out) · **open_source** · design_relevance.


**Lane summary.** Deep design survey of the SKILL component for a no-gradient (frozen-weights + evolving external skill/memory state) L4 speech agent. The 2026 evidence converges on a sharp empirical fact that reframes the design: skills only compound if they pass a verifiable acceptance gate. SkillsBench (2602.12670) shows CURATED skills lift agent pass rate +16.2pp but SELF-GENERATED skills give ~0 net benefit (16/84 tasks NEGATIVE) — "models cannot reliably author the procedural knowledge they benefit from consuming." The SoK on agentic skills (2602.20867) formalizes a skill as a (C,π,T,R) tuple — applicability Condition, execution Policy, Termination, Reusable interface — and gives 7 system-level packaging patterns + a representation×scope taxonomy + a 7-stage lifecycle, and confirms self-generation only works where deterministic verification exists (Voyager, Eureka). The fix is a co-evolving verifier acceptance gate: CoEvoSkills/EvoSkills (2604.01687) pairs a Skill Generator with a Surrogate Verifier and lifts SkillsBench 32%→75% with no ground-truth tests, on frozen Claude Code/Codex. For SELECTION at scale, SkillRouter (2603.22455) shows the full skill BODY — not name/description — is the decisive retrieval signal (removing it costs 29-44pp); retrieve-and-rerank over bodies hits 74% Hit@1 at 1.2B params. Skill REPRESENTATION spans NL (Anthropic SKILL.md open standard) ↔ code-as-skill (Voyager, CRAFT) ↔ hybrid macros ↔ meta-skills; tool CREATION (CREATOR 2305.14318, CRAFT 2309.17428 with validate+dedup+multi-view retrieval, training-free) is the canonical "make a new verified skill" loop. No-gradient skill IMPROVEMENT = program optimization: AFlow MCTS over code workflows (2410.10762), AgentSquare module evolution+recombination (2410.06153), Trace/OptoPrime (2406.16218), and GEPA reflective Pareto prompt evolution that beats GRPO with 35x fewer rollouts (2507.19457) — GEPA's Pareto front doubles as theta2's beta-KL trust region against ACE context-collapse. SPEECH instantiation: a speech "skill" is a verified ASR-correction routine (GER, 2505.17410/2509.04392), a voice tool-use/dialogue behavior (AURA 2506.23049, Full-Duplex-Bench-v3 2604.04847), or a paralinguistic S2S behavior; the acceptance gate is a verifiable speech reward — WER drop, intent/slot accuracy, ParaS2SBench style-appropriateness (2511.08723) + GSRM naturalness (2602.13891), with the frozen omni bi-encoder providing SpeechBERTScore-style semantic-consistency proxy rewards and the shared speech+text embedding index for body-level retrieval keyed on paralinguistic state. Recommendation: a hybrid NL+code skill folder with a (C,π,T,R) header keyed on speaker-ID/emotion/turn-phase, admitted only on positive verifiable-reward delta vs no-skill baseline (SkillsBench protocol), retrieved body-first (SkillRouter) over the omni bi-encoder index, improved by GEPA/AFlow under a Pareto/beta-KL trust region, deduped via CRAFT, abstracted via PolySkill, and deprecated when running reward-delta turns negative.


**Adversarial verifier assessment.** Strong lane. Every source resolves to a real paper or repo — all 2026-dated arXiv IDs (2602.12670 SkillsBench, 2602.20867 SoK, 2604.01687 CoEvoSkills, 2603.22455 SkillRouter, 2602.13891 GSRM, 2605.05726 SkillRet, 2605.10114 SkillRAE, 2604.24026 SSL, 2604.03964 SkillFoundry, 2604.04847 FDB-v3, 2603.13686 tau-Voice, 2605.12039 SkillGraph) web-verify, as do the established anchors (Voyager, CREATOR, CRAFT, AFlow, AgentSquare, AWM, GEPA, PolySkill) with their exact headline numbers (Voyager 73% self-verification ablation; AFlow +5.7%/4.55% cost ICLR25 Oral; AgentSquare +17.2%; AWM +24.6%/+51.1%; GEPA 35x fewer rollouts ICLR26 Oral). The lane's central empirical thesis — curated skills compound (+16.2pp) but self-generated skills give ~0 net benefit (16/84 negative), so a verifiable acceptance gate is mandatory — is robustly supported by three independent 2026 papers (SkillsBench, SoK, CoEvoSkills). The scope tagging is notably honest: the surveyor tags 'mixed' precisely where weight-updating RL is involved downstream (A2-05 SkillRouter's trained 0.6B retriever/reranker, A2-13 fine-tuned/RL GER variants, A2-15 ParaS2S/GSRM RL) while keeping the base policy frozen, and tags 'no-gradient' only for genuinely frozen-policy methods. No claim is unverifiable or egregiously overstated; all 17 kept. Minor imprecisions worth flagging, none refutation-level: (1) A2-04's '32%->75%' conflates the round-5 evolution-dynamics peak (75%) with the headline deployed result, which is actually 30.6%->71.1% (+40.5pp); (2) A2-09's GEPA 'up to 19%' vs the paper's 'up to 20%'; (3) the 'GEPA Pareto-front = beta-KL trust region' and 'co-evolving surrogate verifier = frozen omni bi-encoder SpeechBERTScore proxy' equivalences in A2-09/A2-04/A2-17 are the surveyor's design analogies, not results claimed by those papers (correctly placed in design_relevance, not asserted as findings); (4) A2-11's SkillGraph (2605.12039) is literally a 'Skill-Augmented Reinforcement Learning' framework whose policy co-evolves via training feedback — a weight-updating flavor — but it is only a secondary 'Related' cite for the typed-dependency-graph idea, and the primary support (PolySkill) is genuinely no-gradient, so the claim's no-gradient design recommendation stands.


---

## Verified claims (17 kept / 17 total)


### A2-01 · empirical · scope: no-gradient · OSS: yes (skillsbench.ai; HF papers/2602.12670)

Curated agent skills substantially raise success rates but SELF-GENERATED skills give ~zero net benefit and frequently regress — the single most important constraint on a no-gradient skill library.


- **Sources:** [SkillsBench: Benchmarking How Well Agent Skills Work Across Diverse Tasks](https://arxiv.org/abs/2602.12670)

- **Design relevance:** Directly reinforces theta2: naive append-only skill accrual does NOT compound. Mandates a verifiable-reward ACCEPTANCE GATE (admit a skill only if it beats the no-skill baseline by a positive delta) and per-skill deprecation when delta turns negative — the core control law for the speech skill bank.


### A2-02 · definitional · scope: n/a · OSS: no

An agentic skill is formally a (C, π, T, R) tuple — applicability Condition, execution Policy, Termination criterion, Reusable interface — distinct from a single tool call; 7 system-level packaging patterns and a representation×scope taxonomy organize the design space.


- **Sources:** [SoK: Agentic Skills — Beyond Tool Use in LLM Agents](https://arxiv.org/abs/2602.20867)

- **Design relevance:** Gives the speech-skill schema directly: each speech skill = (C: paralinguistic/state trigger e.g. emotion=angry∧lang=en, π: verified ASR-correction/tool-use/dialogue routine, T: turn/utterance-complete check, R: typed I/O). Picks the packaging pattern for speech: hybrid NL+code macro inside a self-evolving library with progressive disclosure.


### A2-03 · empirical · scope: n/a · OSS: no

SoK confirms self-generated skills only reliably help in environments with DETERMINISTIC automated verification (Voyager, Eureka); without it they encode 'incorrect or overly specific heuristics' that degrade performance — and notes the library lacks mature dedup/deprecation mechanisms.


- **Sources:** [SoK: Agentic Skills — Beyond Tool Use in LLM Agents](https://arxiv.org/html/2602.20867v1)

- **Design relevance:** Speech is verification-rich (WER/intent/SER/SID are deterministic-ish reward fns) — exactly the regime where self-generated skills CAN compound. Justifies code-as-skill or hybrid (testable) over pure-NL skills, and motivates building the dedup/deprecation machinery SoK says is missing.


### A2-04 · empirical · scope: no-gradient · OSS: yes (github.com/Zhang-Henry/CoEvoSkills)

A co-evolving Surrogate Verifier is the concrete mechanism that converts failing self-generated skills into compounding ones WITHOUT weight updates or ground-truth tests.


- **Sources:** [CoEvoSkills: Self-Evolving Agent Skills via Co-Evolutionary Verification](https://arxiv.org/abs/2604.01687)

- **Design relevance:** Template for the speech acceptance gate when ground-truth speech labels are scarce: co-evolve a speech Surrogate Verifier (e.g., the frozen omni bi-encoder scoring semantic/paralinguistic consistency) alongside the skill generator, so a new ASR-correction or dialogue skill is gated on a learned reward proxy, not just on labeled WER.


### A2-05 · empirical · scope: mixed · OSS: yes (github.com/zhengyanzhao1997/SkillRouter)

At scale, the decisive signal for skill SELECTION is the full skill BODY (implementation text), not its name or description — overturning the conventional metadata-only routing assumption.


- **Sources:** [SkillRouter: Retrieve-and-Rerank Skill Selection for LLM Agents at Scale](https://arxiv.org/abs/2603.22455)

- **Design relevance:** The speech skill index must embed full skill bodies, not just NL summaries. The frozen omni bi-encoder (omni-embed-nemotron) becomes the retrieval encoder so a SPOKEN query and a stored skill body share one space; paralinguistic state (speaker-ID bucket, emotion, language) acts as a retrieval FILTER on top of body-level retrieve-and-rerank. (Router components are small trained models; the base policy stays frozen.)


### A2-06 · empirical · scope: no-gradient · OSS: yes (github.com/minedojo/voyager)

Voyager established the canonical no-gradient executable-skill-library loop: generate code skill → verify via environment feedback + self-verification critic → store in an embedding-indexed library → retrieve by similarity; self-verification is the load-bearing component.


- **Sources:** [Voyager: An Open-Ended Embodied Agent with Large Language Models](https://arxiv.org/abs/2305.16291)

- **Design relevance:** Reference architecture for the speech skill component, but the self-verification critic should be REPLACED/augmented by verifiable speech rewards (WER/intent/SER) which are objective and cheaper than an LLM critic — the speech analogue of Voyager's 'item obtained?' environment check.


### A2-07 · empirical · scope: no-gradient · OSS: yes (github.com/lifan-yuan/CRAFT)

Tool/skill CREATION via the four-stage Creation→Decision→Execution→Rectification loop (CREATOR) and create→abstract→VALIDATE→DEDUP→multi-view-retrieve (CRAFT) are the canonical training-free recipes for minting a new verified skill.


- **Sources:** [CREATOR: Tool Creation for Disentangling Abstract and Concrete Reasoning of LLMs](https://arxiv.org/abs/2305.14318) · [CRAFT: Customizing LLMs by Creating and Retrieving from Specialized Toolsets](https://arxiv.org/abs/2309.17428)

- **Design relevance:** CRAFT's validate+dedup+multi-view retrieval is the off-the-shelf bloat-control for the speech skill bank: validate a new speech skill against a verifiable reward before admission, dedup near-identical routines (e.g., per-accent ASR-correction) via embedding similarity, and retrieve by (task, skill-name, docstring) multi-view. CREATOR's Rectification stage = the refine-on-reward inner loop.


### A2-08 · empirical · scope: no-gradient · OSS: yes (github.com/FoundationAgents/AFlow; github.com/tsinghua-fib-lab/AgentSquare)

No-gradient skill/system IMPROVEMENT is achievable by searching over code-represented workflows: AFlow (MCTS over code workflows) and AgentSquare (module evolution + recombination over a 4-module design space) both outperform hand-crafted agents with zero base-model gradient.


- **Sources:** [AFlow: Automating Agentic Workflow Generation](https://arxiv.org/abs/2410.10762) · [AgentSquare: Automatic LLM Agent Search in Modular Design Space](https://arxiv.org/abs/2410.06153)

- **Design relevance:** The speech skill component can be improved as an AgentSquare-style module (ASR-correct / tool-call / dialogue-policy / paralinguistic-style as recombinable modules) and skill workflows optimized by AFlow MCTS with a verifiable speech reward as the search objective — all on frozen base weights.


### A2-09 · empirical · scope: no-gradient · OSS: yes (integrated in DSPy; gepa-ai/gepa)

GEPA — reflective Pareto prompt evolution — is the strongest no-gradient skill-text optimizer and its Pareto front is the practical realization of theta2's beta-KL trust region against context collapse.


- **Sources:** [GEPA: Reflective Prompt Evolution Can Outperform Reinforcement Learning](https://arxiv.org/abs/2507.19457)

- **Design relevance:** Use GEPA to optimize the NL portion of hybrid speech skills (correction prompts, dialogue policies) against verifiable speech rewards. Accept a skill UPDATE only if it does not regress the Pareto front of held-out speech-reward instances — this Pareto-front non-regression IS the trust region that prevents ACE-style 'context collapse' / append-only drift identified in theta2.


### A2-10 · empirical · scope: no-gradient · OSS: yes (github.com/zorazrw/agent-workflow-memory)

Workflow-memory abstraction (AWM) shows verified routines COMPOSE hierarchically with a measurable 'snowball effect' — simple skills compose into complex ones — validating cross-episode transfer for a curated (not append-only) library.


- **Sources:** [Agent Workflow Memory](https://arxiv.org/abs/2409.07429)

- **Design relevance:** Justifies HIERARCHICAL composition for speech: low-level verified routines (denoise→ASR-correct→intent-parse) compose into multi-turn dialogue workflows. AWM's selective injection (curate, not dump-all) is the antidote to skill-library bloat and mirrors the curated>self-generated SkillsBench finding.


### A2-11 · empirical · scope: no-gradient · OSS: no

Skills should be organized by polymorphic/typed abstraction hierarchies (abstract parent skill + concrete per-domain implementations) to control bloat and improve continual transfer — a concrete dedup/merge strategy.


- **Sources:** [PolySkill: Learning Generalizable Skills Through Polymorphic Abstraction For Continual Learning](https://arxiv.org/html/2510.15863) · [SkillGraph: Skill-Augmented RL for Agents via Evolving Skill Graphs](https://arxiv.org/html/2605.12039v1)

- **Design relevance:** Per-accent / per-speaker / per-language ASR-correction skills should be CONCRETE implementations of an abstract parent (e.g., AbstractASRCorrection, AbstractParalinguisticResponse). This deduplicates the library, lets a new accent inherit the parent's verified scaffold, and keeps the bank from exploding as paralinguistic state space grows.


### A2-12 · definitional · scope: no-gradient · OSS: yes (github.com/anthropics/skills; agentskills.io)

The Anthropic Agent Skills SKILL.md format is the de-facto open standard for packaging a skill as a progressive-disclosure folder (NL metadata → instructions → bundled scripts/refs), now adopted across multiple agent products.


- **Sources:** [Equipping agents for the real world with Agent Skills (Anthropic)](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) · [anthropics/skills (Public repository for Agent Skills)](https://github.com/anthropics/skills)

- **Design relevance:** Adopt SKILL.md as the on-disk speech-skill container: YAML frontmatter holds the (C,π,T,R) header + paralinguistic trigger keys (cheap to preload for routing), the body holds the verified routine (retrieved per SkillRouter's body-first finding), and scripts/ hold the executable correction/tool code. Standard format = interoperable with the W1/W4 reward machinery and external marketplaces.


### A2-13 · empirical · scope: mixed · OSS: no

A SPEECH 'skill' has a concrete instantiation as a verifiable ASR-correction routine: LLM generative error correction (GER) over N-best hypotheses, gated by WER reduction; multiple training-free / in-context variants exist.


- **Sources:** [LLM-based Generative Error Correction for Rare Words with Synthetic Data and Phonetic Context](https://arxiv.org/abs/2505.17410) · [Denoising GER: A Noise-Robust Generative Error Correction with LLM for Speech Recognition](https://arxiv.org/abs/2509.04392)

- **Design relevance:** The prototypical speech skill: an in-context GER routine over the omni model's N-best hypotheses, ADMITTED to the library only if it reduces WER on held-out probes for its trigger condition (accent/noise/domain). The training-free in-context GER variant is the in-scope (no-gradient) instantiation; WER-delta is the acceptance gate.


### A2-14 · empirical · scope: no-gradient · OSS: no

Speech tool-use / dialogue behaviors are a second concrete speech-skill type, with dedicated 2025-2026 benchmarks measuring verifiable task success — providing ready acceptance-gate rewards.


- **Sources:** [AURA: Agent for Understanding, Reasoning, and Automated Tool Use in Voice-Driven Tasks](https://arxiv.org/pdf/2506.23049) · [Full-Duplex-Bench-v3: Benchmarking Tool Use for Full-Duplex Voice Agents Under Real-World Disfluency](https://arxiv.org/pdf/2604.04847)

- **Design relevance:** Defines the 'tool-use speech skill' class: a verified (spoken-intent → tool-call sequence → spoken-confirmation) routine. Intent/slot accuracy and tool-call-correctness are the verifiable acceptance rewards; AURA's cascaded ASR→ReAct→tools is the concrete π for these skills under a frozen thinker-talker policy.


### A2-15 · empirical · scope: mixed · OSS: no

Paralinguistic state (emotion/tone/speaker attributes) yields BOTH skill trigger-keys AND verifiable reward signals: automatic paralinguistic judges already act as scalable, human-correlated verifiers for S2S behavior.


- **Sources:** [ParaS2S: Benchmarking and Aligning Spoken Language Models for Paralinguistic-aware S2S Interaction](https://arxiv.org/abs/2511.08723) · [GSRM: Generative Speech Reward Model for Speech RLHF](https://arxiv.org/abs/2602.13891)

- **Design relevance:** Paralinguistic state is the speech analogue of Voyager's environment state: emotion/speaker-ID/turn-phase become (a) the skill applicability Condition C and retrieval keys, and (b) via ParaS2SBench/GSRM, a verifiable style-appropriateness reward that gates admission of paralinguistic dialogue skills — using these judges frozen, no base-model gradient.


### A2-16 · empirical · scope: no-gradient · OSS: no

Skill retrieval/representation is itself an active 2026 design axis beyond plain embedding lookup — structured skill representations, dedicated skill-retrieval benchmarks, and skill-based context compilation are emerging.


- **Sources:** [SkillRet: A Large-Scale Benchmark for Skill Retrieval in LLM Agents](https://arxiv.org/html/2605.05726) · [SKILLFOUNDRY: Building Self-Evolving Agent Skill Libraries from Heterogeneous Scientific Resources](https://arxiv.org/pdf/2604.03964)

- **Design relevance:** Signals the skill component should expose a structured representation (typed I/O, dependencies, scheduling) not just an embeddable string — enabling logical composition of speech skills (ASR-correct depends-on denoise; dialogue-skill schedules tool-skill) and benchmarkable retrieval, future-proofing the W4 design against the body-first / structure-first retrieval trend.


### A2-17 · theoretical · scope: no-gradient · OSS: n/a (composes the open-source components above: CoEvoSkills, SkillRouter, AFlow, AgentSquare, Trace, anthropics/skills, CRAFT)

RECOMMENDED DESIGN for the speech-agent skill component: a verifiable-reward-gated, trust-region-bounded, body-indexed hybrid skill library over a frozen omni policy + frozen omni bi-encoder memory.


- **Sources:** [SkillsBench (curated>self-generated, deterministic verifiers)](https://arxiv.org/abs/2602.12670) · [CoEvoSkills (co-evolving verifier acceptance gate)](https://arxiv.org/abs/2604.01687) · [SkillRouter (body-first retrieve-and-rerank)](https://arxiv.org/abs/2603.22455) · [GEPA (Pareto trust-region no-gradient optimization)](https://arxiv.org/abs/2507.19457) · [ParaS2S (paralinguistic verifiable reward judge)](https://arxiv.org/abs/2511.08723)

- **Design relevance:** This is the concrete blueprint for W4's skill component: frozen weights + evolving curated skill state, verifiable speech rewards as the acceptance gate, body-level retrieval over the omni bi-encoder, and a Pareto/beta-KL trust region — satisfying S1's 'add-new-layer, speech-grounded' GO and theta2's convergence preconditions (structured/curated memory + value-based acceptance + trust region).
