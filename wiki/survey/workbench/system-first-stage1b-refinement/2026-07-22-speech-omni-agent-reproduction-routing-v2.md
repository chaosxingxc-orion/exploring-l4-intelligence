# Speech/omni agent reproduction routing v2

> **Superseded for execution routing:** the full 451-paper rescue in
> [`2026-07-22-local-451-speech-agent-rescue-v3.md`](2026-07-22-local-451-speech-agent-rescue-v3.md)
> adds Audio-Mind, Agent-Omni, AURA, Agentic ASR, Omni-DeepSearch, LongShOTAgent, and MIST after
> inheriting the 122 trainable/model-internal exclusions. This v2 page remains the audit of the original
> 67-paper reroute.

## Decision

Reproduction priority is now rooted in **speech/audio as a load-bearing input to a multimodal agent**.
Pure-text and image/video-only work is retained for method absorption, but its datasets, baselines,
leaderboards, and historical API configurations are no longer reproduction targets.

The ordered contract is:
[`screening-contract-v2-speech-omni-agent-root.md`](screening-contract-v2-speech-omni-agent-root.md).

## What changed

The v1 result, `28 executable + 23 conditional + 11 blocked + 5 surveys`, remains a correct resource
availability audit. It is **not** the active experiment queue. Applying the modality-first root to the
same 67 papers yields:

| Root route | Count | Experiment consequence |
|---|---:|---|
| `R0_REPRODUCE_SPEECH_AGENT` | 1 | Reproduction remains worthwhile: EChO-Agent. |
| `R1_WAIT_SPEECH_AGENT` | 1 | Direct method fit, but wait for code/data: AOP-Agent. |
| `B_SPEECH_NON_AGENT` | 1 | Speech input, but trains a MEG decoder rather than an agent. Method boundary only. |
| `B_TRAINED_OMNI_AGENT` | 1 | Omni/audio-video agent, but behavior comes from SFT/RL. Comparator only. |
| `M_TEXT_METHOD_ONLY` | 40 | Absorb control method; stop dataset and baseline work. |
| `M_VISUAL_METHOD_ONLY` | 15 | Absorb control method; stop dataset and baseline work. |
| `M_OTHER_METHOD_ONLY` | 3 | Non-speech MARL/ML/finance method only. |
| `N_SURVEY_INSTRUMENT` | 5 | Taxonomy and bibliography only. |

Therefore, only **2/67** remain in the direct speech/omni-agent lane, and only **1/67** is ready for a
clean-room reproduction plan. The earlier 51/67 artifact-reproducible count must not be used as a
reproduction workload.

## Cross-corpus reproduction queue

This queue also includes already audited direct papers outside the 67-row ambiguous denominator.

### P0 - first reproduction targets

1. **AudioToolAgent (`2510.02995`)** - training-free audio tool orchestration; author code and
   reproduction materials exist; MMAR and a compatible MMAU subset are local. This is the first exact
   artifact reproduction.
2. **EChO-Agent (`2606.15141`)** - training-free-compatible audio evidence orchestration over local
   MMAR; no author repository was found. This is the first clean-room reproduction and should share the
   same backbone/no-tool control as AudioToolAgent where possible.

### P1 - direct speech/omni methods, artifact check before execution

- **AudioGenie-Reasoner (`2509.16971`)** - audio-to-evidence refinement with explicit
  sufficient/insufficient routing; local MMAU-mini/MMAR, but no released code was confirmed.
- **VISA (`2606.07264`)** - audio reasoning with frozen experts, routing, voting, and disagreement
  resolution; MMAR is local, author code was not confirmed.
- **Omni-Decision (`2607.11433`)** - closest explicit evidence-state, critic, repair, readiness, and
  stopping topology for omni-modal QA; recheck code, exact audio-bearing splits, and baseline access.
- **AOP-Agent (`2605.28192`)** - training-free audio-visual observe-reflect-replan agent; wait for
  MOV-Bench and an author implementation.
- **Active Perception Agent / OmniAgent (`2512.23646`)** - training-free audio/video tool loop with
  memory and reflection; keep behind the open-artifact candidates because it uses a proprietary planner
  and a more complex multi-tool environment.

### Method or boundary only

- **Native Active Perception / OmniAgent (`2606.19341`)**, Light-Omni, LatentOmni, Speech-Hands, and
  other learned policies: absorb observation actions, memory, rewards, and failure modes; do not
  reproduce SFT/RL/adapters for W1.
- **Thinking While Listening (`2509.19676`)**: speech test-time sampling/aggregation, but not an
  adaptive agent loop; retain as an equal-compute comparator.
- **AudioGenie (`2505.22053`)**: training-free and audio-related, but its primary task is
  multimodality-to-audio generation rather than speech/audio evidence-seeking by an omni agent. Keep as
  modality-adjacent method evidence, not an initial reproduction target.
- Pure-text and pure-visual agents such as Reflexion, LATS, ReCoVERR, Tree Search, A-MEM,
  OmniVerifier, EET, A-MapReduce, Kestrel, and VReST contribute method cards only.

## Data scope after the root gate

Data work is now narrow:

- keep local MMAR/MMAU task and split compatibility for AudioToolAgent, EChO-Agent,
  AudioGenie-Reasoner, and VISA;
- check MOV-Bench only because it blocks AOP-Agent;
- check OmniGAIA/WorldSense audio-bearing subsets only if Omni-Decision enters an executable plan;
- retain speech/voice evaluation instruments such as EchoChain when they test agent state-update
  behavior;
- do not fetch or reproduce WebArena, SWE-bench, VQAv2, A-OKVQA, vision-only, text-only, code-only,
  finance, medical-image, or other vertical datasets for the W1 reproduction stage.

## One-by-one rerouting of the 67-paper queue

For every `M_*` row below, the data/baseline action is `STOP`: keep the method abstraction and do not
build a reproduction environment.

| # | arXiv | Paper | Root route | Active use |
|---:|---|---|---|---|
| 01 | `2303.11366` | Reflexion | `M_TEXT_METHOD_ONLY` | Verbal feedback and external memory method card. |
| 02 | `2309.07701` | Semantic Reconstruction from MEG | `B_SPEECH_NON_AGENT` | Speech/neural-decoding boundary; no agent reproduction. |
| 03 | `2310.04406` | LATS | `M_TEXT_METHOD_ONLY` | MCTS, value, reflection, and retry controls. |
| 04 | `2402.15610` | ReCoVERR | `M_VISUAL_METHOD_ONLY` | Selective evidence acquisition and abstention method. |
| 05 | `2403.08978` | AutoGuide | `M_TEXT_METHOD_ONLY` | Failure-to-guideline memory method. |
| 06 | `2405.16334` | Devil's Advocate | `M_TEXT_METHOD_ONLY` | Anticipatory reflection method. |
| 07 | `2405.16854` | eSpark | `M_OTHER_METHOD_ONLY` | Action pruning/exploration idea; MARL training excluded. |
| 08 | `2406.12304` | COT Counter-Narratives | `M_TEXT_METHOD_ONLY` | Target-conditioned decoding idea only. |
| 09 | `2407.01476` | Tree Search for LM Agents | `M_VISUAL_METHOD_ONLY` | Actual-environment tree search method. |
| 10 | `2407.21787` | Large Language Monkeys | `M_TEXT_METHOD_ONLY` | Repeated sampling and verifier scaling method. |
| 11 | `2410.16670` | CoPS | `M_TEXT_METHOD_ONLY` | Cross-task experience selection method. |
| 12 | `2410.20285` | SWE-Search | `M_TEXT_METHOD_ONLY` | Search/refinement engineering method. |
| 13 | `2501.09732` | Diffusion Inference-Time Scaling | `M_VISUAL_METHOD_ONLY` | Candidate/noise search and verifier method. |
| 14 | `2502.08266` | Annotator Disagreement in Hate Speech | `M_TEXT_METHOD_ONLY` | Disagreement handling only; no dataset pursuit. |
| 15 | `2502.12110` | A-MEM | `M_TEXT_METHOD_ONLY` | Dynamic memory/linking method. |
| 16 | `2503.12434` | Optimization of LLM Agents Survey | `N_SURVEY_INSTRUMENT` | Taxonomy/bibliography only. |
| 17 | `2505.18079` | Deep Video Discovery | `M_VISUAL_METHOD_ONLY` | Long-video search/tool method. |
| 18 | `2506.12721` | Strategic Test-Time Compute | `M_TEXT_METHOD_ONLY` | Bandit allocation method. |
| 19 | `2506.17417` | VLM Self-Verification Study | `M_VISUAL_METHOD_ONLY` | Self-verification falsifier. |
| 20 | `2508.01186` | Agent Workflow Survey | `N_SURVEY_INSTRUMENT` | Workflow taxonomy only. |
| 21 | `2508.19322` | AT-CXR | `M_VISUAL_METHOD_ONLY` | Uncertainty routing method; medical-image data ignored. |
| 22 | `2509.22601` | SPEAR | `M_TEXT_METHOD_ONLY` | Exploration/self-imitation boundary method. |
| 23 | `2510.13804` | OmniVerifier | `M_VISUAL_METHOD_ONLY` | Verifier and repair topology; no visual reproduction. |
| 24 | `2510.14900` | Mapping Smarter, Not Harder | `M_TEXT_METHOD_ONLY` | Test-time experience/evidence accumulation method. |
| 25 | `2511.01082` | GeoToken | `M_VISUAL_METHOD_ONLY` | Hierarchical routing/tokenization idea. |
| 26 | `2511.11793` | MiroThinker | `M_TEXT_METHOD_ONLY` | Model/context/tool scaling method. |
| 27 | `2511.20297` | BREW | `M_TEXT_METHOD_ONLY` | Recipe memory and experience-guided search. |
| 28 | `2512.11109` | VLM Test-Time Scaling Limits/Gains | `M_VISUAL_METHOD_ONLY` | TTS control comparisons only. |
| 29 | `2512.19433` | dMLLM-TTS | `M_VISUAL_METHOD_ONLY` | Self-verification/adaptive scaling method. |
| 30 | `2512.20745` | AgentMath | `M_TEXT_METHOD_ONLY` | Tool-use training boundary. |
| 31 | `2512.21815` | High-Entropy VLM Failure Points | `M_VISUAL_METHOD_ONLY` | Entropy/gray-box falsifier. |
| 32 | `2601.05777` | EET | `M_TEXT_METHOD_ONLY` | Early stopping and cost-control method. |
| 33 | `2601.05930` | Predicting ML Agents Before Execution | `M_OTHER_METHOD_ONLY` | Pre-execution success prediction instrument. |
| 34 | `2601.09667` | MATTRL | `M_TEXT_METHOD_ONLY` | Multi-agent textual experience sharing. |
| 35 | `2601.15625` | Fission-GRPO | `M_TEXT_METHOD_ONLY` | Execution-error recovery boundary. |
| 36 | `2602.00028` | ELLMPEG | `M_VISUAL_METHOD_ONLY` | Edge video tool orchestration method. |
| 37 | `2602.01070` | Adaptive Test-Time Compute | `M_TEXT_METHOD_ONLY` | Verifier-conditioned budget allocation. |
| 38 | `2602.01331` | A-MapReduce | `M_TEXT_METHOD_ONLY` | Wide-search decomposition method. |
| 39 | `2602.03219` | Trajectory Diversity Scaling | `M_TEXT_METHOD_ONLY` | Diversity metric/hypothesis only. |
| 40 | `2602.13218` | Scaling the Scaling Logic | `M_TEXT_METHOD_ONLY` | Agentic meta-synthesis method. |
| 41 | `2602.16485` | Team of Thoughts | `M_TEXT_METHOD_ONLY` | Team/tool orchestration method. |
| 42 | `2602.22406` | Autonomous Memory Agents | `M_TEXT_METHOD_ONLY` | Autonomous memory maintenance method. |
| 43 | `2603.01692` | Reasoning as Gradient | `M_TEXT_METHOD_ONLY` | Research-agent iterative improvement method. |
| 44 | `2603.09821` | One-Eval | `M_TEXT_METHOD_ONLY` | Traceable evaluation infrastructure. |
| 45 | `2603.12109` | Information Self-Locking | `M_TEXT_METHOD_ONLY` | Active-reasoning failure mode; RL path excluded. |
| 46 | `2604.06066` | Structure Snowballing | `M_TEXT_METHOD_ONLY` | Constrained-reflection failure mode. |
| 47 | `2604.11025` | Test-Time Scaling over Perception | `M_VISUAL_METHOD_ONLY` | Perception-grounded scaling method. |
| 48 | `2604.16529` | Agentic Coding Test-Time Compute | `M_TEXT_METHOD_ONLY` | Budget-scaling method. |
| 49 | `2605.06457` | Payment Workflow Fidelity | `M_TEXT_METHOD_ONLY` | Workflow-fidelity metric only. |
| 50 | `2605.12894` | Realistic User Personas | `M_TEXT_METHOD_ONLY` | Adversarial persona/environment design. |
| 51 | `2605.12978` | Continuously Updated Memories | `M_TEXT_METHOD_ONLY` | Memory erosion falsifier. |
| 52 | `2605.22511` | Search-E1 | `M_TEXT_METHOD_ONLY` | Search/self-distillation boundary. |
| 53 | `2605.23989` | Trustworthy Agentic AI Survey | `N_SURVEY_INSTRUMENT` | Safety taxonomy only. |
| 54 | `2605.24481` | OmniEgo-R2 | `M_VISUAL_METHOD_ONLY` | Video-only routing/verification method; name is not omni-audio evidence. |
| 55 | `2605.28192` | AOP-Agent | `R1_WAIT_SPEECH_AGENT` | Direct audio-visual agent; wait for MOV-Bench/code. |
| 56 | `2605.29568` | DeepTool | `M_TEXT_METHOD_ONLY` | Process-supervised tool reasoning boundary. |
| 57 | `2606.01667` | ATLAS | `M_TEXT_METHOD_ONLY` | Test-time allocation method only. |
| 58 | `2606.01770` | Adaptive Auto-Harness | `M_TEXT_METHOD_ONLY` | Deployment/self-improvement method only. |
| 59 | `2606.08231` | Multimodal TTS Survey | `N_SURVEY_INSTRUMENT` | Taxonomy only; TTS is test-time scaling. |
| 60 | `2606.08450` | GIFT | `M_OTHER_METHOD_ONLY` | Finance RL interface method only. |
| 61 | `2606.08728` | AI for Mathematical Reasoning Survey | `N_SURVEY_INSTRUMENT` | Math/verification bibliography only. |
| 62 | `2606.08850` | Intrinsic Selection and Resampling | `M_TEXT_METHOD_ONLY` | Selection/resampling and gray-box boundary. |
| 63 | `2606.11543` | SkillJuror | `M_TEXT_METHOD_ONLY` | Skill-organization evaluation method. |
| 64 | `2606.15141` | EChO-Agent | `R0_REPRODUCE_SPEECH_AGENT` | Direct clean-room audio-agent reproduction on local MMAR. |
| 65 | `2606.19341` | Native Active Perception | `B_TRAINED_OMNI_AGENT` | Audio-video agent topology only; SFT/RL path excluded. |
| 66 | `2606.28864` | VLM Test-Time Scaling | `M_VISUAL_METHOD_ONLY` | Visual TTS method only; not speech. |
| 67 | `2606.30774` | Interactive Improvement from Feedback | `M_TEXT_METHOD_ONLY` | Feedback-vs-retry evaluation contract. |

## Immediate next artifact work

Before any model execution, freeze only the P0 contracts:

1. AudioToolAgent repository commit, environment, model/API IDs, MMAR/MMAU split, and no-tool baseline.
2. EChO-Agent clean-room specification: four stages, tool versions, evidence schema, verifier rights,
   retry/stop rules, and the same-backbone baseline on the same MMAR slice.

All other text/vision papers feed a method-component matrix. They do not create dataset downloads,
baseline runs, or reproduction tickets.
