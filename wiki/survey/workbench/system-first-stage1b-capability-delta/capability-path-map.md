---
artifact_id: "SF-STAGE1B-CAPABILITY-PATH-MAP-V1"
date: "2026-07-23"
status: "RELEASE_CANDIDATE_AWAITING_INDEPENDENT_REVIEW"
evidence_mode: "SOURCE_REPORTED_TRACEABLE"
project_results: false
novelty_verdict: false
---

# Capability path map

## Evidence outcome

The delta strengthens the case for organizing Stage-1C by causal intervention rather than dataset or
task label, but it also shows that `knowledge / skill / memory` cannot be treated as three symmetric
containers. Knowledge and skills are content assets; memory is the persistence and update mechanism
that may store either content. D0 system construction and D4 reward-guided control remain separate
axes.

| Work | Primary path | Stage-1B role | MM gate | Project-use relation | Decisive evidence or boundary |
|---|---|---|---|---|---|
| RMR (2405.20834) | D1 knowledge | component | MM2 | borrowed protocol | paired no/retrieval and modality/k arms; strong text-only result blocks MM necessity |
| M2A (2602.07624) | D3 memory | direct | MM2 | borrowed protocol | long-term dual-layer/tri-path ablations; derived LoCoMo and system confounding remain |
| XSkill (2603.12056) | D2 skill, D3 persistence | direct | MM2 | borrowed protocol | experience/skill ablations and cross-model transfer; training labels construct external assets |
| GEMS (2603.28088) | D0 system bundle | component | MM2 | reference | agent, memory and skills enter sequentially; attribution is unresolved |
| SRA (2604.24594) | D2 instrument, D4 boundary | instrument | MM0 | borrowed protocol | separates retrieval, loading and actual utility under hard negatives |
| MMSkills (2605.13527) | D2 skill | direct | MM2 | borrowed protocol | text/state/image/loading arms; text-only regression shows interference |
| Anything2Skill (2606.09316) | D1→D2 compilation | component | MM0 | borrowed protocol | Base/RAG/Skill/Skill+RAG isolates compilation value in text command-line tasks |
| RESOURCE2SKILL (2606.29538) | D2 skill | direct | MM2 | borrowed protocol | matched briefs, same backends and selection ablations; raw-resource RAG control absent |
| AutoSkill (2603.01145) | D2 skill, D3 persistence | component | MM0 | reference | explicit lifecycle and versioned artifacts; descriptive counts do not establish task gain |
| SKILLFOUNDRY (2604.03964) | D2 skill | component | MM1 | reference | scientific workflows improve with generated skills; domain/tool stack is distant |
| SkillFlow (2604.17308) | D2 skill, D3 persistence | falsifier | MM0 | borrowed protocol | benefits are selective; bad skills, inflation and failed repair can cause negative transfer |
| SkillsBench (2602.12670) | D2 instrument | instrument | MM0 | borrowed protocol | 87-task paired efficacy; 13 negative tasks and harness dependence challenge universal benefit |
| LoCoMo (2402.17753) | D3 instrument | instrument | MM2 | borrowed protocol | long-range/temporal/adversarial outcomes; QA replaces images with captions |
| Memory-R1 (2508.19828) | D3 trained boundary, D4 boundary | boundary | MM0 | reference | learned memory actions and reward disagreement; PPO/GRPO weight updates violate TF scope |

No row is a `REPRODUCTION_ANCHOR`. A proposed speech/omni experiment derived from these works must
be labeled `PROPOSED_BY_PROTOCOL_ANALOGY` until an independently signed, task-matched speech/omni
anchor is found.

## D0 — multimodal agent system

GEMS supports the importance of a carrier system, while simultaneously demonstrating why whole-
system improvement cannot be distributed across memory and skill components without factorial
controls. The D0 minimum protocol is therefore a frozen-core, same-tool, same-budget comparison
between a single-call baseline and a system harness, followed by K/S/M additions one at a time. If
topology, tools and K/S/M all change together, the result remains `CAUSAL_ATTRIBUTION_UNRESOLVED`.

## D1 — multimodal knowledge

RMR supplies a useful retrieval protocol but weak evidence for the necessity of multimodal knowledge:
its text-only stratum can be very strong, and answer-bearing exemplars create leakage alternatives.
Anything2Skill adds the crucial `raw source access versus compiled skill` edge, but it is text-only.
The residual is not “does retrieval help?”; it is whether non-text evidence contributes beyond an
information-matched transcript/caption and whether compilation changes action quality beyond source
access.

Required future controls are no external knowledge, text-only evidence, multimodal evidence,
modality-shuffled evidence, matched-token irrelevant evidence, raw-source RAG and oracle evidence.

## D2 — multimodal skills

This is the densest new evidence path, but not uniformly positive. MMSkills and RESOURCE2SKILL show
that state cards, images/keyframes and executable resources can improve visual/tool agents.
SkillsBench shows broad paired benefits from curated skills, while SkillFlow shows that self-evolved
skills can regress under some model/harness stacks. SRA explains part of the discrepancy: retrieval or
loading is not equivalent to correct incorporation. AutoSkill and XSkill further show that “frozen
core” can still involve substantial external learning, supervision and lifecycle maintenance.

The correct experimental object is therefore a skill contract with applicability, preconditions,
state/milestone evidence, action/tool procedure, verification, failure and fallback. Required arms are
no skill, information-matched source, text procedure, multimodal state-conditioned skill, oracle skill,
wrong-but-plausible skill, and—where online evolution is studied—create/retrieve/use/repair metrics
separately.

## D3 — multimodal memory

LoCoMo and M2A give concrete long-range, temporal, adversarial and visual-centric protocols, but the
evidence is not yet clean enough for a general multimodal-memory claim. Original LoCoMo QA replaces
images with captions; M2A uses a derived dataset and changes storage, retrieval and iteration together.
Memory-R1 supplies an informative learned-policy boundary, not a training-free prior.

Memory experiments must therefore separate stored content from persistence policy: no memory/current
context, raw history, text-compressed memory, evidence-preserving multimodal memory, stale/conflicting
memory and oracle memory. Outcomes must include not only final accuracy but evidence recall, temporal
consistency, conflict resolution, harmful retrieval, update correctness and unnecessary writes.

## D4 — training-free reward-guided orchestration

The delta does not close a new direct training-free RL path. SRA is a selection instrument, and
Memory-R1 is a trained RL boundary. The project hypothesis remains conditional: a frozen-core
controller may use a live reward/value/advantage signal to choose the next external action, candidate,
K/S/M asset, stop or repair action. Static top-k, similarity retrieval, reflection, majority vote and
offline scoring are not automatically RL.

The future comparison must include a static policy, heuristic retrieval/routing, reward-guided online
control and oracle policy under equal candidate supply and budget. It must report selection utility,
regret, unnecessary calls, harmful action rate and stopping/repair decisions—not just final task score.

## Cross-path falsifiers retained

1. More context may explain apparent skill/knowledge gains.
2. Answer-bearing exemplars or benchmark contamination may explain retrieval gains.
3. Skill retrieval and invocation may be high while use is wrong.
4. Self-generated skills may be worse than no skills.
5. Incorrect persistent assets can create negative transfer and compounding error.
6. Whole-system changes can masquerade as K/S/M effects.
7. Automatic judges can prefer verbose outputs that lexical metrics penalize.
8. A multimodal task can be solved through a text shortcut; MM2 is not MM3.
9. Frozen core weights do not imply zero learning when external assets use labels or trajectories.
10. A trained PPO/GRPO policy is a boundary, not training-free inference-time control.
