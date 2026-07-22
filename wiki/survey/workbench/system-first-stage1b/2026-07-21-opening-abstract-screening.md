---
title: "Stage-1B opening abstract screening"
date: 2026-07-21
role: "D1 abstract-screening record; not a full-text or novelty claim"
stage: "STAGE_1B_SYSTEMATIC_MAPPING"
decision_vocabulary: [SELECT_FULLTEXT, DEFER, EXCLUDE]
fulltext_gate: "Only SELECT_FULLTEXT records may enter local download and D2 reading"
---

# Stage-1B opening abstract screening

## Gate and interpretation limits

This record applies the user-required sequence to newly discovered papers:

1. inspect title and abstract only (`D1`);
2. record `SELECT_FULLTEXT`, `DEFER`, or `EXCLUDE` with a reason;
3. for `SELECT_FULLTEXT`, download the PDF and source archive to the external survey store and append
   their hashes to the full-text ledger; and
4. begin `D2` method-path reading only from those local, hash-bound files.

An abstract can justify further reading but cannot establish a method-path classification. Terms such
as “training-free”, “frozen”, “verification”, and “self-correction” remain author claims at D1. This
screening therefore does not assign novelty, gap, or final in-scope status.

## Priority P0: download and read first

| arXiv | D1 abstract analysis | Decision and reason | D2 questions |
|---|---|---|---|
| [2606.30774](https://arxiv.org/abs/2606.30774) | Separates useful feedback from unguided retry and extra test-time computation. Reports that self-feedback often adds little beyond self-refinement, while strong external teachers can add feedback-specific gains. | `SELECT_FULLTEXT / P0`. Directly supplies controls for RQ-CTRL and may invalidate favorable readings that omit repeated-attempt baselines. | Exact equal-compute controls; interaction protocol; signal producer; whether feedback changes candidate supply, selection, or both; failure strata. |
| [2604.27233](https://arxiv.org/abs/2604.27233) | A reviewer evaluates provisional tool calls before execution and can correct or degrade them. The abstract also reports a GEPA prompt-optimization variant. | `SELECT_FULLTEXT / P0`. Direct inference-time signal-to-action neighbor, but deployment paths must be split because the optimized-reviewer path may differ from the unoptimized frozen path. | Reviewer input/output; veto/rewrite rights; frozen versus optimized variants; stopping; helpfulness/harmfulness denominator and controls. |
| [2509.16971](https://arxiv.org/abs/2509.16971) | Claims a training-free audio system with evolving textual evidence and iterative search until sufficient information is gathered. | `SELECT_FULLTEXT / P0`. Direct RQ-SYS/RQ-OMNI/RQ-SAFE neighbor whose sufficiency and stopping mechanism cannot be resolved from the abstract. | Operational sufficiency test; planner and critic identities; persistent state; tool visibility; budgets; whether any component was adapted. |
| [2512.23646](https://arxiv.org/abs/2512.23646) | Claims a no-training omnimodal agent that dynamically plans unimodal tool use and uses audio cues to guide later perception. | `SELECT_FULLTEXT / P0`. Direct black-box-ish active-perception neighbor; the abstract does not show an explicit evaluative signal or stop policy. | Exact topology and APIs; observation-to-next-action causal link; audio-specific state; termination; static orchestration versus feedback-guided control. |
| [2606.15141](https://arxiv.org/abs/2606.15141) | Describes planning, tool execution, evidence integration, and answer verification for audio QA; evidence integration is reported as the key ablation factor. | `SELECT_FULLTEXT / P0`. Direct audio verification neighbor, with training boundary and verifier decision rights unresolved at D1. | Component training status; evidence schema; verifier rubric/signal; repair or reject actions; benchmark leakage and stopping. |
| [2601.09413](https://arxiv.org/abs/2601.09413) | A voice agent learns when to trust itself versus consult external audio perception through a “learnable reflection primitive”. | `SELECT_FULLTEXT / P0`. Highly relevant speech-specific routing evidence, but the learnable primitive likely places the primary path outside TF-Strict. | What is trained; whether a frozen deployed variant exists; reflection signal; routing action; oracle/candidate access; generalization controls. |
| [2303.11366](https://arxiv.org/abs/2303.11366) | Uses task feedback signals to create linguistic reflections, persists them in episodic memory, and changes decisions in later trials without weight updates. | `SELECT_FULLTEXT / P0`. Foundational no-weight-update feedback-to-memory-to-action lineage; directly tests signal source and cross-trial persistence. | External versus simulated feedback; evaluator access; retry budget; memory reset boundary; ablations against retry and extra context. |
| [2310.04406](https://arxiv.org/abs/2310.04406) | Combines MCTS, LM value functions, self-reflection, and external environmental feedback in a gradient-free language-agent search process. | `SELECT_FULLTEXT / P0`. Foundational search/value/feedback controller needed to distinguish branch selection from omni observation control. | Node value and backup; environment signal; branching/candidate supply; equal-search controls; termination and failed branches. |
| [2601.15808](https://arxiv.org/abs/2601.15808) | A rubric-based outcome verifier returns detailed feedback for iterative test-time refinement without additional agent training; the abstract separately releases verifier SFT data. | `SELECT_FULLTEXT / P0`. Direct rubric-reward and iterative-feedback neighbor, with a necessary split between closed-model plug-in and trained verifier artifacts. | Verifier construction/training; rubric visibility; response-only versus trajectory feedback; iteration cap; same-compute retry baseline; verifier error. |
| [2505.19768](https://arxiv.org/abs/2505.19768) | A training-free multimodal misinformation agent uses MCTS over a selected tool subset and a dual reward for trajectory quality and confidence. | `SELECT_FULLTEXT / P0`. Direct multimodal reward→tree-policy→evidence-acquisition path surfaced by REC-1. | Reward computation and access; node/edge semantics; tool-subset supply effects; backups; equal-tool/equal-search controls; stop condition. |
| [2506.08691](https://arxiv.org/abs/2506.08691) | A training-free LVLM method uses MCTS and a multimodal self-reward over sub-question utility, answer correctness, and clue relevance. | `SELECT_FULLTEXT / P0`. Direct frozen multimodal self-reward/search path; “answer correctness” may conceal privileged or self-judged information. | Correctness source; visual clue access; value backup; branching budget; answer leakage; tree-search ablations. |
| [2603.16664](https://arxiv.org/abs/2603.16664) | A training-free grounding agent gathers structured visual evidence, an LVLM judge checks it, and answers iteratively self-refine from verified evidence. | `SELECT_FULLTEXT / P0`. Direct evidence-verification→repair loop and potential judge-drift boundary. | Judge input and calibration; evidence rejection/repair rights; iteration cap; over-correction controls; same-compute retry baseline. |
| [2605.30698](https://arxiv.org/abs/2605.30698) | Multiple VLM agents expose grounding regions, mutually verify visual evidence, and use evidence consistency in the final decision without training. | `SELECT_FULLTEXT / P0`. Direct multimodal-consensus signal with non-text evidence grounding; valuable RQ-OMNI/RQ-CTRL case. | Region extraction; mutual-verification protocol; consistency aggregation; agent independence; text-only and answer-agreement controls. |
| [2607.09438](https://arxiv.org/abs/2607.09438) | Reports that prompt parseability and token budget dominate test-time gains; PRM beam search and critics do not consistently beat majority vote under the studied policies. | `SELECT_FULLTEXT / P0`. High-value negative/control paper that challenges attribution of gains to search or verification machinery. | Exact compute parity; repair intervention; policy differences; selector calibration; uncertainty; whether conclusions hold by language/task stratum. |
| [2605.30639](https://arxiv.org/abs/2605.30639) | Formalizes active instance verification and reports no reliable gain from the tested next-best-view policies, while a trained agent performs better. | `SELECT_FULLTEXT / P0`. Direct negative prior for active observation selection and a clean training-free/trained boundary comparison. | Finite horizon and rewards; view topology/traps; NBV policies; power/uncertainty; oracle view value; why active selection fails. |

## Priority P1: download after P0, before any D2 claim

| arXiv | D1 abstract analysis | Decision and reason | D2 questions |
|---|---|---|---|
| [2505.22053](https://arxiv.org/abs/2505.22053) | Claims a training-free multimodal-to-audio generation system with trial-and-error refinement plus supervisor feedback loops. | `SELECT_FULLTEXT / P1`. Strong signal/action architecture neighbor, but generation and supervisor access may differ materially from frozen-core understanding. | Supervisor observations; feedback representation; regeneration/selection loop; budgets; model updates; answer-bearing information. |
| [2606.17669](https://arxiv.org/abs/2606.17669) | Claims frozen backbones and training-free speech role play, but controls behavior through internal cognitive steering and external expressive rendering vectors. | `SELECT_FULLTEXT / P1`. Important boundary case for frozen-but-internal intervention; relevance depends on hidden-state and learned-vector access. | Vector construction; calibration/training data; activation access; persistence; causal signal; whether any black-box-compatible path exists. |
| [2602.00415](https://arxiv.org/abs/2602.00415) | Converts frozen-VLM perceptual signals into positive, negative, and uncertain latent graph memories and suppresses conflicting retrievals. | `SELECT_FULLTEXT / P1`. Strong verification/memory boundary case, but latent access may violate the intended black-box topology. | Logit/embedding/activation access; partition calibration; cross-item memory; verifier false positives; comparable non-latent path. |
| [2602.01983](https://arxiv.org/abs/2602.01983) | Claims training-free creation and self-updating of reusable tools from reasoning experience, including cross-problem memory consolidation. | `SELECT_FULLTEXT / P1`. Tests the line between within-item control, cross-item adaptation, and configuration change. | What persists across items; executable-code creation; validation signal; rollback; leakage; whether the base and tool-selection policies remain fixed. |
| [2606.07264](https://arxiv.org/abs/2606.07264) | Uses multimodal evidence, model voting, consistency checking, and category-aware routing for audio reasoning. | `SELECT_FULLTEXT / P1`. Relevant selection/verification path, but the abstract does not show whether consistency scores change sequential actions or only final aggregation. | Sequential versus one-shot voting; score definition; model/tool budget; routing calibration; trained components; stopping. |
| [2602.03707](https://arxiv.org/abs/2602.03707) | Combines budgeted retrieval and an agent loop with GRPO optimization of tool use and answer quality. | `SELECT_FULLTEXT / P1`. Explicitly trained comparator needed to separate runtime architecture from learned policy effects. | Pre-GRPO baseline; reward definition; runtime controller; equal-retrieval controls; trained and frozen-path ablations. |
| [2210.03629](https://arxiv.org/abs/2210.03629) | Interleaves reasoning traces and environment actions so observations can update plans and handle exceptions. The abstract does not specify a distinct evaluator or reward-guided selection step. | `SELECT_FULLTEXT / P1`. Foundational observation-action lineage and a negative control against treating all interactive loops as reward-guided. | Exact prompt/action protocol; environment observations; task success signal; update rights; stopping; whether any verifier is present. |
| [2511.02834](https://arxiv.org/abs/2511.02834) | A master agent interprets intent, delegates to modality-specific foundation models, and integrates outputs without retraining. The abstract describes coordination but no explicit feedback/verification loop. | `SELECT_FULLTEXT / P1`. Direct training-free omni system neighbor and useful static-coordination comparator. | Master inputs and state; sequential versus one-shot delegation; conflict handling; verifier/signal presence; tool budget; stop rule. |
| [2502.20379](https://arxiv.org/abs/2502.20379) | Scales the number of off-the-shelf aspect verifiers and combines them with best-of-n without additional training. | `SELECT_FULLTEXT / P1`. General verifier-portfolio comparator needed to separate verifier supply from controller adaptation. | Score aggregation; verifier correlation; candidate-pool parity; self-verification leakage; weak-to-strong setup; cost scaling. |
| [2512.05542](https://arxiv.org/abs/2512.05542) | Sequentially routes best-of-n generations across multiple LLMs using reward-model scores and agreement, claiming compute parity and no additional training. | `SELECT_FULLTEXT / P1`. Direct reward-guided routing path in text reasoning; useful mechanism neighbor outside the omni modality. | Online state/action; reward and agreement combination; compute-parity accounting; model-portfolio supply effect; stopping. |

## Priority P2: measurement-path reading after the method batch

| arXiv | D1 abstract analysis | Decision and reason | D2 questions |
|---|---|---|---|
| [2605.06897](https://arxiv.org/abs/2605.06897) | Introduces a synthetic multi-turn speech tool-calling dataset with dynamic state, mixed initiative, and physical-world constraints. | `SELECT_FULLTEXT / P2`. It is a measurement instrument rather than a method candidate, but it can map what speech-specific state and interaction failures are observable. | Dataset construction; state-transition checks; audio perturbations; tool correctness; contamination; what it cannot measure about control attribution. |
| [2605.15104](https://arxiv.org/abs/2605.15104) | Converts verified text tool-calling benchmarks into paired speech evaluations and adds noise, ambiguity, and judge validation. | `SELECT_FULLTEXT / P2`. Useful RQ-MEASURE-MAP instrument; not evidence for a controller method. | Pairing invariants; voice/noise factors; judge agreement; argument-value failures; limits of TTS-derived audio. |

## Batch result

The opening targeted batch contains 27 `SELECT_FULLTEXT` records: 15 P0, 10 P1, and 2 P2. The
selection rate is intentionally not a prevalence estimate: these records were chosen from an
adversarial proximity queue, not sampled uniformly from REC-1. Broad BFS screening must retain
`DEFER` and `EXCLUDE` outcomes separately before Stage-1B can report route-level counts.

The acquisition gate is now closed for this batch: all 27 selected papers have both PDF and e-print
in the external survey store and all 54 unique renditions re-hash to their ledger rows. All 15 P0
papers subsequently received local D2 reading. P0 method notes and P1/P2 method/measurement notes are
kept in separate records so the abstract rows above remain auditable D1 decisions rather than being
silently rewritten from later evidence.
