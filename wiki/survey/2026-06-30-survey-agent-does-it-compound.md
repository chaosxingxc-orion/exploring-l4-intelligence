# S1 · Lane A3-headroom — Does no-gradient agent self-improvement compound? (B1/B4)

> Part of **S1** (decisive probe) of [[2026-06-30-agent-level-synthesis]] — strategic survey for [[2026-06-26-training-free-rl-for-speech-omni-research-proposal]]. Run `wf_8452c9ae-a11`, 2026-06-30. Per-lane adversarial verification; only `keep=true` claims archived; links real & verifiable. Each claim is scope-tagged (no-gradient = in scope vs weight-updating = out).


**Lane summary.** Bottom line: there IS real, web-verified evidence that no-gradient agent-level self-improvement (accumulating an external skill library / experience memory across episodes, weights frozen) compounds and delivers headroom BEYOND single-shot model-output search — but the compounding is bounded and design-fragile, not unconditional. Strongest positive evidence: (a) Voyager's skill library compounds compositionally with zero gradient (3.3x more items, milestones up to 15.3x faster, zero-shot transfer to a new world); (b) ExpeL's cross-episode insight pool beats Reflexion's repeated single-task retry with a single attempt (ALFWorld 59 vs 54); (c) Agent Workflow Memory's induced workflows yield +24.6%/+51.1% relative success on Mind2Web/WebArena and online gains WIDEN 8.9–14.0 absolute points as the train-test gap grows; (d) JitRL (Jan 2026) is the linchpin — it FORMALLY extends the q*(z)∝q0·exp(R/β) tilting objective to multi-step agent actions (closed-form additive logit update z'=z+βÂ is the exact solution to KL-constrained advantage maximization), does no-gradient credit assignment by retrieving trajectory returns, and on WebArena beats every training-free agent-memory baseline (46.98/51.35 vs Reflexion 41.08/42.12, AWM 39.37/40.32, Memory 41.36/43.00, Static-no-memory 35.63/36.30) AND beats the weight-update WebRL baseline (60.0 vs 46.06) at ~30x lower cost, with the episode-to-episode gap WIDENING (compounding). Counter-evidence and limits: Reflexion plateaus (ReAct gains halt by trials 6–7; no improvement on WebShop after 4 trials; stuck in local minima; depends on self-evaluation accuracy; no per-step credit assignment); naive iterative context rewriting suffers "context collapse"/brevity bias (ACE: 18,282→122 tokens, accuracy 66.7→57.1, below the 63.7 no-memory baseline); and evolving memory accumulates cumulative, persistent errors (semantic/procedural drift, poisoning, retrieval hallucination) — "Remembering More, Risking More" shows memory-equipped frozen agents exceed the stateless baseline's violation rate and that risk GROWS with exposure length (temporal memory contamination, attention dilution). Net: compounding is achievable but requires structured/curated memory + explicit value/credit-assignment (JitRL, ACE) rather than append-only reflection logs. Scope discipline: Voyager, Reflexion, ExpeL, AWM, JitRL, LATS, ACE are NO-GRADIENT (in scope); Agent Q (MCTS+DPO) and most agent process-reward/credit-assignment work (OPRL, AgentPRM, iStar) are WEIGHT-UPDATING (out of scope, included only as contrast).


**Adversarial verifier assessment.** Lane verdict: STRONG and KEPT in full — all 13 claims survive adversarial verification, every arXiv ID resolves to a real paper with content matching the statement, and no claim is materially overstated. The most consequential and risk-prone source, JitRL (arXiv:2601.18510, Jan 2026), is genuine: I independently reproduced its exact WebArena table (Static 35.63/36.30 ... JitRL 46.98/51.35), the held-out weight-update comparison (WebRL 46.06 ~$9,900 vs JitRL 60.0 ~$290), the proven closed-form additive-logit/KL-constrained result, and the widening per-episode gap. The two 'too-good-to-be-true' 2026 negative results (SSGM governance survey 2603.11768; 'Remembering More, Risking More' 2605.17830) are also real, with correct authors/dates and abstract-level confirmation of their headline findings.

Scope discipline is sound: no-gradient claims (Voyager, Reflexion, ExpeL, AWM, JitRL, LATS, ACE) are correctly tagged frozen-weight/external-state, and the weight-updating contrasts (Agent Q's off-policy DPO; OPRL/iStar and AgentPRM's PRM/policy training) are correctly flagged out-of-scope rather than smuggled in as support — exactly the boundary the strategic brief demands. The synthesis (C13) is appropriately balanced: it does not claim unconditional compounding, but bounds it with the plateau (Reflexion 6–7 trials), collapse (ACE 18,282->122 tokens dropping below the no-memory baseline), and contamination (violation rate rising with exposure) counter-evidence, all verified.

Residual caveats (do not warrant keep=false, but temper two claims to med): (1) C10's detailed corruption-loop taxonomy and C11's mechanistic labels are body/search-level, not abstract-confirmed — their headline directions hold but the fine-grained enumerations are not line-verified; (2) C12 lists 'OPRL, AgentPRM, iStar' as if three works when OPRL and iStar are the same paper (2509.19199, renamed across versions), though the citation line already notes 'OPRL/iStar', so it is a presentational, not substantive, imprecision; (3) minor secondary figures left unverified (Reflexion '+22% over 12 steps', ExpeL FEVER 63->70, JitRL Jericho per-game numbers) are non-load-bearing. Net: the lane's bottom line — no-gradient agent-level self-improvement does compound and does exceed single-shot model-output search, but only with structured/curated memory plus explicit value-based credit assignment — is robustly supported by web-verified primary sources.


---

## Verified claims & sources (13 kept / 13 total)


### C1 · empirical · scope: no-gradient · confidence: high

Voyager demonstrates that a skill library accumulated across episodes compounds capability with ZERO gradient updates: skills are stored as executable code, new skills are composed from previously stored ones, and the library transfers to a fresh world for zero-shot novel-task solving — obtaining 3.3x more unique items, traveling 2.3x longer distances, and unlocking tech-tree milestones up to 15.3x faster than prior SOTA.


- **Sources:** [Voyager: An Open-Ended Embodied Agent with Large Language Models](https://arxiv.org/abs/2305.16291)

- **Relevance:** B1 (compounding), B4 (headroom beyond single output)


### C2 · empirical · scope: no-gradient · confidence: high

Reflexion shows that an episodic memory of verbal self-reflections (no weight updates) improves across trials but PLATEAUS quickly and exhibits classic no-credit-assignment failure modes — making it the canonical evidence that naive append-only reflection does NOT compound indefinitely.


- **Sources:** [Reflexion: Language Agents with Verbal Reinforcement Learning](https://arxiv.org/abs/2303.11366)

- **Relevance:** B1 (plateau), B4, B5 (failure modes)


### C3 · empirical · scope: no-gradient · confidence: high

ExpeL provides direct evidence that CROSS-EPISODE accumulated experience+insights (no parametric updates) can beat single-task repeated retry: with a single attempt it outperforms Reflexion's third reattempt on ALFWorld (59 vs 54) and matches it on HotpotQA (39–40 vs 40), and it improves over ReAct by ~+19 pts (ALFWorld), +11 pts (HotpotQA), +7 pts (FEVER transfer), with performance scaling as the experience pool grows.


- **Sources:** [ExpeL: LLM Agents Are Experiential Learners](https://arxiv.org/abs/2308.10144)

- **Relevance:** B1 (compounding), B4 (beats single-shot retry)


### C4 · empirical · scope: no-gradient · confidence: high

Agent Workflow Memory shows compounding from inducing reusable workflows out of past trajectories (in-context, no gradient): +24.6% relative success on Mind2Web and +51.1% relative on WebArena over baselines, with ONLINE AWM (induce-on-the-fly) generalizing more strongly the further the test distribution drifts — gains WIDEN from 8.9 to 14.0 absolute points as the train-test gap grows.


- **Sources:** [Agent Workflow Memory](https://arxiv.org/abs/2409.07429)

- **Relevance:** B1 (compounding widens with horizon), B4


### C5 · theoretical · scope: no-gradient · confidence: high

JitRL is the linchpin formal+empirical result: it EXTENDS the inference-time tilting objective q*(z)∝q0·exp(R/β) to multi-step agent action spaces. It proves the additive logit update z'(s,a)=z(s,a)+β·Â(s,a) is the exact closed-form solution of the KL-constrained objective argmax_π' E_a~π'[Â] − (1/β)·KL(π'||π_θ), and does no-gradient credit assignment by retrieving trajectory returns to estimate state-value V̂(s) and action-advantage Â(s,a) — i.e., q* tilting where R becomes a retrieval-estimated advantage.


- **Sources:** [Just-In-Time Reinforcement Learning: Continual Learning in LLM Agents Without Gradient Updates](https://arxiv.org/abs/2601.18510)

- **Relevance:** B3 (q* formally extends to agent action space), B1


### C6 · empirical · scope: no-gradient · confidence: high

JitRL's empirical results show no-gradient agent memory both (a) beats single-shot/no-memory output search AND (b) compounds across episodes — and can even beat a weight-update baseline. On WebArena it reaches Avg/Final 46.98/51.35 vs Reflexion 41.08/42.12, AWM 39.37/40.32, Memory 41.36/43.00, and Static-no-memory 35.63/36.30; vs weight-update methods it hits 60.0 final vs WebRL 46.06 (and SFT 23.0) at ~30x lower cost (~$290 vs ~$9,900); the Final-minus-Avg gap is largest for JitRL (4.37 pts) and the per-episode gap WIDENS over 10–15 episodes (compounding, with reduced late-stage variance).


- **Sources:** [Just-In-Time Reinforcement Learning: Continual Learning in LLM Agents Without Gradient Updates](https://arxiv.org/abs/2601.18510)

- **Relevance:** B4 (headroom over single-shot), B1 (compounds), B6 (beats weight-update baseline)


### C7 · empirical · scope: no-gradient · confidence: high

LATS shows the agent action space can be extended to multi-step tree search at inference with NO gradients and rival gradient-based fine-tuning: it integrates MCTS over ReAct-style reasoning/acting steps with LM-powered value functions and self-reflection, reaching 92.7% pass@1 on HumanEval (GPT-4) and a gradient-free WebShop average of 75.9 'comparable to gradient-based fine-tuning' (GPT-3.5).


- **Sources:** [Language Agent Tree Search Unifies Reasoning, Acting, and Planning in Language Models](https://arxiv.org/abs/2310.04406)

- **Relevance:** B3 (multi-step search action space, no gradient), B4


### C8 · empirical · scope: weight-updating · confidence: high

Agent Q is the WEIGHT-UPDATING counterpart and is OUT of scope: it combines guided MCTS + self-critique with iterative fine-tuning via off-policy DPO on collected agent trajectories. It is the canonical 'search-then-distill-into-weights' pattern and must be distinguished from no-gradient methods like JitRL/LATS that keep the same search-time value signal but never touch weights.


- **Sources:** [Agent Q: Advanced Reasoning and Learning for Autonomous AI Agents](https://arxiv.org/abs/2408.07199)

- **Relevance:** B6 (scope boundary contrast), B3


### C9 · empirical · scope: no-gradient · confidence: high

Iterative monolithic context/memory rewriting has a distinct compounding-KILLER failure mode — 'context collapse' / 'brevity bias' — where accumulated knowledge is repeatedly over-summarized until it degrades below the no-memory baseline; ACE shows a structured, incremental (delta) memory curation fixes this and restores compounding gains, with large cost savings.


- **Sources:** [Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models](https://arxiv.org/abs/2510.04618)

- **Relevance:** B5 (failure mode: memory collapse), B1 (curation enables compounding)


### C10 · empirical · scope: no-gradient · confidence: med

Evolving/self-updating memory accumulates CUMULATIVE, PERSISTENT errors (unlike one-shot RAG where errors are isolated): a 2026 governance survey catalogs semantic drift (knowledge degrades through iterative summarization), procedural/goal drift, memory poisoning, consolidation drift, and retrieval hallucination as a compounding failure loop — a key reason naive cross-episode memory may fail to compound.


- **Sources:** [Governing Evolving Memory in LLM Agents: Risks, Mechanisms, and the SSGM Framework](https://arxiv.org/abs/2603.11768)

- **Relevance:** B5 (failure modes: drift/error accumulation), B1


### C11 · empirical · scope: no-gradient · confidence: high

A controlled negative result: equipping a FROZEN agent with memory can actively HURT and the harm GROWS with accumulated experience — memory-equipped agents show higher safety-violation rates than stateless baselines, increasing with exposure length ('temporal memory contamination'), driven by cross-context leakage and attention dilution; recency-biased (short) memory is protective. This bounds the 'more memory is always better' claim.


- **Sources:** [Remembering More, Risking More: Longitudinal Safety Risks in Memory-Equipped LLM Agents](https://arxiv.org/abs/2605.17830)

- **Relevance:** B5 (failure mode: memory hurts, anti-compounding), B1


### C12 · empirical · scope: mixed · confidence: med

Credit assignment is the pivotal differentiator between compounding and plateauing no-gradient agents. Methods that store only outcome reflections (Reflexion) give NO per-step credit and plateau; methods that estimate per-step value/advantage compound — JitRL does this purely by retrieval (no gradient), whereas most agent process-reward / step-credit work (OPRL, AgentPRM, iStar) achieves it by TRAINING a PRM or policy (weight-updating, out of scope).


- **Sources:** [Online Process Reward Learning for Agentic Reinforcement Learning (OPRL/iStar)](https://arxiv.org/abs/2509.19199) · [AgentPRM: Process Reward Models for LLM Agents via Step-Wise Promise and Progress](https://arxiv.org/abs/2511.08325)

- **Relevance:** B3 (credit assignment for agent trajectories), B5, B6 (no-gradient vs weight-updating)


### C13 · theoretical · scope: no-gradient · confidence: high

Synthesis for B1+B4: no-gradient agent self-improvement DOES compound and DOES exceed single-shot model-output search, but only under two conditions — (i) the memory is structured/curated rather than append-only (ACE vs collapse; AWM workflows vs raw logs), and (ii) the recall/decode step performs explicit value-based credit assignment (JitRL) rather than blind concatenation. Absent these, gains saturate (Reflexion plateau ~4–7 trials) or reverse (temporal memory contamination). This frames the unified objective q*(z)∝q0·exp(R/β) extending from z='model output' to z='which memory to recall · which skill to invoke · how to build context · then decode'.


- **Sources:** [Just-In-Time Reinforcement Learning: Continual Learning in LLM Agents Without Gradient Updates](https://arxiv.org/abs/2601.18510) · [Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models](https://arxiv.org/abs/2510.04618)

- **Relevance:** B1 + B4 (core resolution), B3, B5
