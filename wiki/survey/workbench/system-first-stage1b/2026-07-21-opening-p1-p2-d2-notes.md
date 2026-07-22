---
title: "Stage-1B opening P1/P2 D2 method and measurement notes"
date: 2026-07-21
role: "WORKBENCH local-fulltext analysis; not a novelty or Stage-1B completion claim"
stage: "STAGE_1B_SYSTEMATIC_MAPPING"
evidence_policy: "D1 selection preceded external download; D2 reading used only hash-bound local files"
---

# Stage-1B opening P1/P2 D2 method and measurement notes

## Evidence boundary

These twelve papers were first selected from title/abstract evidence in
`2026-07-21-opening-abstract-screening.md`, then downloaded as both PDF and e-print to the external
survey store, independently re-hashed against the ledger, and only then read at D2. P1 papers are
method/boundary comparators; P2 papers are measurement instruments and do not enter a method
occupancy denominator.

| Paper | Local PDF SHA-256 | Local e-print SHA-256 |
|---|---|---|
| [AudioGenie, 2505.22053](https://arxiv.org/abs/2505.22053) | `78763e0ad105ac2076907f21c89bb8d6383b1a4083a51b7d7345a2850faa4308` | `2a5cadb297e8036972cb45fc6bdcc6ae15318a1942809957f9ed170a96cbbc27` |
| [DeSRPA, 2606.17669](https://arxiv.org/abs/2606.17669) | `a9e7cbd6b51183dfcc05a4b3d23d1007136125fd08fbd2d85da28bb82c2629ef` | `409a6f11a393f837ed64a649c737c96e367c78755c2d0b0da4d20a86230a1fd6` |
| [PolarMem, 2602.00415](https://arxiv.org/abs/2602.00415) | `c12627326387f41b2b98186feb51d5399b7a761f6ab8516561f4058523120a9c` | `e143994d55cb176e0939a41ceb5a17adccf6f5c6ff0b2e5aaaf621081da95bde` |
| [UCT, 2602.01983](https://arxiv.org/abs/2602.01983) | `136bac3299afed14fd526c7b82a17ed8fccde54b486a0ec5ec04d6316fe92266` | `74818980fb64e92aabf9bfa43ef773fced56ff38ea272df253db47a8c6d95d43` |
| [VISA, 2606.07264](https://arxiv.org/abs/2606.07264) | `1f2034563aef4ba168cd2a09ffe43ba05fca21c6993ba9d071f69b00dcc14a6e` | `a455082738153d1b852a990d00c01323de23b9d78739173cbde5c59148b7d87d` |
| [OmniRAG-Agent, 2602.03707](https://arxiv.org/abs/2602.03707) | `7c58b6540b07a3bde7efa0600a08f8d934a95f939e3c2512032d9f6b98ea1a18` | `9cc2da671e8d6a6ff53b5a86dc31db1b1ec59fa54c0cca275d58ddafbd2b5597` |
| [ReAct, 2210.03629](https://arxiv.org/abs/2210.03629) | `f285b0971ae4a790e402fb93966bed3adde2cf0a04977d08b2b40d6ab0cace69` | `c81c6344ddae91fc0a36ea830c414ca72e3736ec02f84ccbd81ed7d7f67c0293` |
| [Agent-Omni, 2511.02834](https://arxiv.org/abs/2511.02834) | `0244630c596dab967a569b114582eb83b1fe33843c68ef538ddd09c255f10d51` | `f2c2b346d380fa72e1c477ac8ccbba1aa19af037df0607a232e9750d333b8498` |
| [Multi-Agent Verification, 2502.20379](https://arxiv.org/abs/2502.20379) | `6559b772a9f1da8b8110c5e48cefa0d078221003c591535b8328ffe97417fa15` | `4add0662ab783e47cc8d9b2ec79a8036ffe6ebe5de81d8cf2aab524483a374ae` |
| [ROBON, 2512.05542](https://arxiv.org/abs/2512.05542) | `4583078c92948c862eb1881412794ccc945b030c9d53d8c5bf0f31639affb004` | `241634ca5ae59b3e46e7a737a5daf2c6262665c4587834c5f4627ee45e11de21` |
| [MIST, 2605.06897](https://arxiv.org/abs/2605.06897) | `b42ab288a69c53cd0a5bfd4604d5c6d8d51f43264a4d02ab295f0d5e6a27f810` | `7227a05ca958fe55c0f9f10e500bdcaf7f925ce5ef14cb5ceecc510828a5cfe8` |
| [From Text to Voice, 2605.15104](https://arxiv.org/abs/2605.15104) | `e0638bda7ae0dbd8f14f342829c358c1bfb4252558468aad03aaa29a32049e47` | `30089ba1282bc43b7440d34da2b8639c4863fa9b7671777d69f73a8fde6fc0f5` |

## P1 method and boundary comparison

| Paper | Deployed path and signal-to-action right | Stop/budget and training boundary | Stage-1B interpretation |
|---|---|---|---|
| AudioGenie | A generation team decomposes multimodal input, selects domain experts/models, and builds an audio-generation tree. Stage-specific supervisors evaluate plan quality, model choice, and generated audio. Quality/alignment/aesthetics feedback sends fixable errors to post-processing children and major mismatches to sibling regeneration/model switching (pp. 3–5). | Stop when criteria pass; otherwise limit tree depth and retry branches, then return the best explored result (p. 5). The framework orchestrates existing models without additional training. | Direct training-free evaluator→repair/regenerate/select path, but for multi-model audio generation rather than understanding with one frozen omni core. It confirms that audio-specific supervisory branching is already occupied. |
| DeSRPA | A frozen Qwen LLM has layer-specific personality/language vectors injected into its residual stream; emotion labels steer a frozen StyleTTS2 latent style through an acoustic vector bank (pp. 2–3). | No runtime feedback loop or adaptive stop was located. Despite the “training-free” label, personality vectors are optimized against target/opposing centroids, acoustic vectors are estimated from filtered emotion samples, and coefficient sweeps calibrate injection (pp. 2–3). | Frozen-weight but white-box internal intervention. It violates the black-box hidden-state boundary and demonstrates why “no fine-tuning” cannot be used as a synonym for TF-Strict. |
| PolarMem | Frozen-VLM concept proposals are verified through ensemble prompts using `P("Yes")`, adaptively split into `HAS`, `NOT_HAS`, and `Uncertain`, stored in a polarized graph, and retrieved with logical constraints before semantic similarity (pp. 4–6). | One construction/retrieval/inference path rather than sequential action control. It is training-free in weights, but requires probability/latent-memory access; missed candidate concepts cannot be recovered later (p. 6). | Strong negative-memory/retrieval comparator outside the guaranteed black-box interface. The proposal-coverage limit is a supply bottleneck that can masquerade as memory/control value. |
| UCT | A ReAct task loop can answer, call a core/created tool, or open a build ticket. The isolated build loop generates code/tests, consumes sandbox and critic feedback until approval, registers the tool, and resumes the task. Offline consolidation later merges/prunes the reusable library (pp. 4–6). | The task loop has a maximum `n` rounds; build acceptance controls registration. Core weights are not trained, but executable supply and persistent cross-task configuration evolve. | Training-free tool creation is a direct control-plane neighbor but crosses the within-item boundary. Security, rollback, validation leakage, and cross-item adaptation must be coded separately from frozen-core weights. |
| VISA | Multiple audio models each sample three answers, apply within-model majority/consistency, then a 27-category router selects among model outputs using audio, event, spectral/visual, and category-specific evidence (pp. 2–4). | One-shot ensemble selection rather than a sequential observe/repair loop. No method-specific weight update is described in the inspected method; category/model routing is a static engineered policy. | Audio evidence-consensus/routing comparator. Improvements mix feature/tool supply, portfolio diversity, and routing, so it cannot isolate a reward-guided controller effect. |
| OmniRAG-Agent | An OmniLLM maintains summarized interaction history and repeatedly emits a plan, image/audio retrieval queries, and a continue/stop decision. The main policy is optimized with format and ground-truth answer rewards (pp. 3–5). | Stop on the learned decision or maximum rounds. The principal open-model path uses end-to-end GRPO; reported `+RAG+Agent` rows without RL provide a separable frozen-policy ablation (pp. 5–8). | Direct omni retrieval/state/action topology, but the main controller is trained and outside TF-Strict. The frozen ablation matters for reproduction-first attribution between RAG supply, agent loop, and learned policy. |
| ReAct | Few-shot prompting interleaves free-form thoughts, task actions, and environment observations. Thoughts update plans, track subgoals, and handle exceptions; observations ground later thoughts/actions (pp. 3–8). | The environment/task determines termination and supplies sparse success feedback, but no distinct evaluator, tree policy, or persistent cross-trial memory is part of base ReAct. The presented prompting path updates no weights. | Foundational observation→reasoning→action lineage and an essential negative control: interactive behavior is not automatically reward-guided selection. Prompt demonstrations and best-of-trial reporting remain supply/budget factors. |
| Agent-Omni | A master agent performs perception, query decomposition, model-pool execution, integration, and a decision step that emits `is_final` plus suggestions. If incomplete, the suggestions generate targeted follow-up subquestions for another multi-model loop (pp. 3–4). | Stop on `is_final=true` or a maximum of three loops. Existing foundation models are coordinated without additional training (pp. 4, 6). | Direct no-training omni evaluator→follow-up→reintegrate neighbor, structurally closer than static delegation. It uses heterogeneous models rather than a single frozen omni core, but materially narrows broad system-path claims. |
| Multi-Agent Verification | Sample `n` candidates, ask a domain subset of heterogeneous off-the-shelf aspect verifiers for binary approvals, sum approvals, and select the candidate with the highest score (pp. 2–5). | One-shot best-of-n selection; verifier count and candidate count are the budgets. Verifiers need no new training, but domain-specific verifier engineering/selection is a calibration step (pp. 5–7). | Verifier-supply and candidate-supply comparator, not a sequential controller. It shows that scaling evaluator diversity alone can change outcomes and must be matched before attributing gains to policy adaptation. |
| ROBON | With a fixed `n`-sample budget and model portfolio, each step scores current model-head candidates using reward plus normalized-answer agreement, commits one, advances only its source model, and reuses unchosen heads. The final answer is best-of-n over committed samples (pp. 2–4). | Exact sample-count parity with single-model best-of-n. No router training, but per-model reward normalization uses an empirical CDF estimated from a precomputed response/reward corpus; some tasks degrade as `n` grows, attributed to reward hacking (pp. 5–6). | Direct sequential reward-guided model-routing neighbor outside omni. It demonstrates both a degenerate control plane and why pre-test calibration plus reward hacking must be explicit rather than hidden by “training-free”. |

## P2 measurement-path comparison

| Paper | Measurement object and invariants | What it can and cannot support |
|---|---|---|
| MIST | Synthetic multi-turn smart-home conversations combine speech requests with text home layout/state/history, executable IoT tools, dynamic state updates, clarifications, no-op rejection, status requests, disfluencies, accent/prosody, and injected noise. It reports execution match, code exact match, dialogue-action macro-F1/accuracy, and a human audit of 300 examples with over 92% label/tool correctness and over 90% annotator agreement (pp. 3–4). | Strong instrument for speech-specific state, mixed initiative, over-triggering, wrong-device/value, and physical-action risk. It cannot establish controller value by itself; inputs are synthetic/TTS, much context stays textual, and the paper evaluates models rather than a matched reward-control intervention. |
| From Text to Voice | Converts verified text tool-calling benchmarks into paired text/TTS-audio instances while preserving tool schemas and gold labels; varies TTS provider, voice, and SNR; compares seven omni models; and decomposes paired text-success/audio-failure cases into decision, tool, argument-schema, and argument-value errors (pp. 4–10). | Useful counterfactual modality-shift instrument and an optimistic first-stage proxy. It does not substitute for spontaneous speech or interaction; reference-free judge results need separate calibration, and model/task ranking changes rule out architecture-wide conclusions. |

## Cross-paper implications

1. **The direct omni loop is crowded.** Agent-Omni joins OmniAgent, AOP-Agent, AudioGenie-Reasoner,
   and Omni-Decision as a no-training sufficiency/completeness-feedback loop. Remaining distinctions are
   exact core topology, state ownership, signal source, failure semantics, and information access.
2. **“Training-free” has at least four incompatible meanings.** ReAct/Agent-Omni prompt frozen APIs;
   DeSRPA optimizes and injects hidden-state vectors; PolarMem consumes probabilities and latent graph
   state; UCT changes the executable tool library across items. Paper-level labels would erase the
   black-box and configuration boundaries.
3. **Selection is already sequential.** ROBON uses a reward/agreement signal to allocate later samples
   across models at exact sample parity. It is not omni observation control, but it occupies the broad
   reward-guided next-action mechanism and exposes dataset-calibration and reward-hacking risks.
4. **Supply and evaluator diversity are major confounders.** AudioGenie, VISA, Multi-Agent Verification,
   Agent-Omni, and OmniRAG change model/tool/evidence supply as well as decision logic. Stage-1B must
   retain matched-pool/equal-budget and frozen-policy ablation availability as mapped facts.
5. **Speech measurement can now be made causal later, but not in Stage-1B.** The two P2 papers provide
   paired text/audio, dynamic-state, argument-level, clarification, and physical-risk axes. They are
   Stage-2 measurement candidates only after Stage-1C problem selection and protocol freezing.

These implications remain method-path and measurement-readiness facts. They are not a novelty verdict,
gap selection, benchmark endorsement, or authorization to run any model/dataset/prototype experiment.
