# Frozen-D0 speech-agent retrospective rescue v4

## Decision

A root-aware retrospective pass over the frozen Stage-1B D0 changes the executable queue again.
Relative to the earlier 451-local-PDF rescue, it recovers **five new P0 systems**, **four conditional
P1 systems**, and **seven immediately useful speech-agent evaluation resources**. The strongest new
reproduction targets are:

1. VoiceAgentRAG (`2603.02206`)
2. Enterprise Realtime Voice Agent tutorial (`2603.05413`)
3. Pepper Realtime AI Assistant (`2603.21013`)
4. Langbar / MCP-driven speech-enabled GUI (`2510.06223`)
5. Thinking with Sound (`2509.21749`)

These are better aligned with the project root than many high-scoring Stage-1B papers because the
speech/audio input is load-bearing, the control loop stays outside a frozen model, and a useful smoke
can be run locally or through external APIs without training. This pass does **not** reopen discovery,
make a novelty claim, or authorize model/API experiments.

The previous local-corpus rescues—Audio-Mind, Agent-Omni, AURA, Agentic ASR, Omni-DeepSearch,
LongShOTAgent, and MIST—remain valid and are not duplicated here. See
[`2026-07-22-local-451-speech-agent-rescue-v3.md`](2026-07-22-local-451-speech-agent-rescue-v3.md).

## Coverage and no-omission account

- Frozen source: **20,727 unique arXiv IDs**, 55,080,637 bytes, SHA-256
  `afc3d85eab383f81c96d293b13d053767500baec485c89ce03aeff32f3425883`.
- A deterministic, deliberately permissive speech-input plus agent/control gate matched **614** D0
  papers.
- **85** of those already belonged to the previously analysed 451-PDF local corpus.
- The remaining **529/529** were written to a full candidate ledger, preserving title, complete
  abstract, lexical evidence, old Stage-1B disposition/reason, and sampling lane.
- Score bands among the 529 were: 3 at `>=40`, 43 at `30-39`, 215 at `20-29`, and 268 below 20.
  Manual review deliberately entered the low-score tail; VoiceAgentRAG scored 18, i-Code Studio 10,
  and FAM-HRI 14.
- Old routing among these 529 was 293 `EXCLUDE_ABSTRACT`, 203 `DEFER_ABSTRACT`, 30
  `DEFER_REPRO_CHECK`, and 3 without a canonical sampling decision. This is why the old score or
  disposition could not be reused as a reproduction decision.
- The final audit contains **529 unique rows**: 53 named manual decisions and 476 explicitly retained
  as `NOT_PROMOTED_THIS_PASS`. No row that entered the retrospective gate disappeared between
  candidate generation and reporting.

This is a high-recall root-aware rescreen, not a proof of zero lexical false negatives. Its bounded
claim is: every frozen D0 record was processed, every record that passed the disclosed root gate was
accounted, and the reproduction shortlist was human-reviewed against the three requested criteria.

External evidence is stored under
`SPEECHRL_DATA_DIR/survey-fulltext-secondary-analysis/2026-07-22-d0-rescue-v1/`:

- `lexical-candidates.jsonl`: 529 rows, SHA-256
  `ad4e530be32e089971288d2d7ba4d788c3b6b86a8f61cb3c0739f47dfe33d1c9`;
- `rescue-audit.jsonl`: 529 rows, SHA-256
  `63992b1e141fa0170675b2fab5243710d375bbda4c79923a33bc752a7a48fe02`;
- `rescue-summary.json`: counts and coverage assertion;
- `fulltext-analysis-selected39/`: 39/39 selected PDFs extracted, zero failures; analysis-ledger
  SHA-256 `1ed1dedeb7bc6bf4d4cd9774afdf0cea36f991908f3252051dcf76aa457a76c0`.

## Revised rescue summary

| Route | Count | Meaning |
|---|---:|---|
| `P0_RESCUE_SYSTEM` | 5 | Direct speech-agent system; training-free smoke is executable now. |
| `P1_CONDITIONAL_SYSTEM` | 4 | Direct system fit, but exact paper reproduction has an artifact, hardware, data, or dependency blocker. |
| `I0_EVALUATION_RESOURCE` | 7 | Released speech-agent tool/workflow or judge-audit resource; not a method reproduction. |
| `I1_CONDITIONAL_INSTRUMENT` | 5 | Useful environment/benchmark, but visual/omni-heavy or superseded. |
| `WAIT_ARTIFACT` | 6 | Root-relevant paper whose executable code/data could not be confirmed. |
| `METHOD_ONLY` | 12 | Transfer the control idea; do not reproduce its vertical task/data. |
| `EXCLUDE_TRAIN_OR_MODEL` | 11 | Newly encountered load-bearing training/model intervention; not promoted. |
| `NOT_PROMOTED_THIS_PASS` | 479 | Accounted in the ledger; no stronger root-fit and reproducibility signal survived. |

## P0 — reproduce or smoke first

### 1. VoiceAgentRAG (`2603.02206`)

- **Technical solution reproducible:** Yes. It is an external five-part control plane: memory router,
  conversation event stream, asynchronous slow thinker, foreground fast talker, and semantic cache.
  No backbone update is required.
- **Data obtainable:** Yes. The repository includes a synthetic NovaCRM knowledge base (12 documents,
  76 chunks) and scenario material sufficient for an end-to-end smoke; exact latency claims still
  depend on the chosen services and machine.
- **Baseline locally/API reproducible:** Yes. The
  [Apache-2 repository](https://github.com/SalesforceAIResearch/VoiceAgentRAG) includes code, tests,
  examples, FAISS/Qdrant choices, OpenAI/Gemini routes, and a fully local Ollama route.
- **Why rescue it:** It gives W1 a clean asynchronous retrieval/prefetch baseline for testing whether
  background work reduces voice latency without changing the speech model.

### 2. Building Enterprise Realtime Voice Agents from Scratch (`2603.05413`)

- **Technical solution reproducible:** Yes. The nine progressive chapters cover streaming STT, LLM
  streaming and function calls, streaming TTS, pipelining, WebSockets, VAD/interruption, browser
  audio, enterprise tools, and latency measurement.
- **Data obtainable:** No benchmark dataset is required for the system smoke. Microphone audio and
  included domain-tool examples are enough; exact reported latency is provider- and hardware-bound.
- **Baseline locally/API reproducible:** Yes. The
  [Apache-2 repository](https://github.com/SalesforceAIResearch/enterprise-realtime-voice-agent)
  supports Deepgram and ElevenLabs with an OpenAI API or a local OpenAI-compatible vLLM endpoint.
  Its documented local option is Qwen2.5-7B; the API path avoids GPU dependence.
- **Why rescue it:** This is the best engineering control baseline for measuring what comes from
  streaming, overlap, state management, and tool execution before adding reward-guided selection.

### 3. Pepper Realtime AI Assistant (`2603.21013`)

- **Technical solution reproducible:** Yes for the control plane. Native speech-to-speech APIs act as
  the frozen planner; function calls drive navigation, gaze, vision, touch, search, weather, and UI
  actions. An event-rule layer distinguishes interrupt, append-and-respond, and silent context update.
- **Data obtainable:** No task dataset is needed for a functional smoke. Exact robot behaviour needs
  a Pepper v1.8 and its sensors, but the conversation/tool logic does not.
- **Baseline locally/API reproducible:** Yes. The
  [MIT repository](https://github.com/studerus/pepper-android-realtime-chat) has a standalone Android
  build flavor that simulates robot-only actions and supports OpenAI Realtime, Gemini Live, xAI, and
  Azure routes. Full embodied reproduction remains hardware-conditional.
- **Why rescue it:** It is an unusually concrete reference for translating asynchronous sensor events
  into bounded model interrupts and tool actions.

### 4. Langbar / MCP-driven speech-enabled GUI (`2510.06223`)

- **Technical solution reproducible:** Yes. ViewModels expose current-view and application-global
  tools, while the GUI router provides explicit semantics through MCP. This is external, typed,
  inspectable control rather than screenshot-only computer use or model modification.
- **Data obtainable:** No external dataset is needed for the demo. The paper's multilingual
  tool-selection evaluation is not required for a smoke and is not packaged as a frozen benchmark.
- **Baseline locally/API reproducible:** Yes. The mature
  [MIT Flutter repository](https://github.com/hansvdam/langbar) includes examples, tests, Android/iOS/
  desktop targets, MCP integration, speech I/O, and OpenAI, Groq, Ollama, and OpenRouter providers.
- **Why rescue it:** It supplies a practical MCP tool-surface design for speech agents where the action
  space is scoped by current application state.

### 5. Thinking with Sound (`2509.21749`)

- **Technical solution reproducible:** Yes at method level. TwS is explicitly training-free and
  model-agnostic: the LALM iteratively selects from 21 audio operators for denoising, enhancement,
  normalization, and acoustic analysis, then reconsiders the transformed audio.
- **Data obtainable:** Partly. MELD is public, but the paper-specific MELD-Hard1k perturbation set was
  not found as a released dataset in the official artifact. A clean-room perturbation slice is easy to
  construct but is not an exact benchmark reproduction.
- **Baseline locally/API reproducible:** Yes for a smoke. The
  [public implementation](https://github.com/Eric2i/Think-with-Sound) exposes the operator registry,
  prompt templates, and inference engine for an arbitrary instruction-following LALM wrapper. The
  repository currently has no declared license and does not package an exact model wrapper or full
  benchmark runner, so paper-score reproduction is conditional.
- **Why rescue it:** It is the clearest direct prior for inference-time audio manipulation selected by
  a frozen audio-language model.

## P1 — direct fit with a material blocker

### 6. Audio-Maestro (`2510.11454`)

- **Technical solution reproducible:** Yes as a clean-room/API baseline. It uses zero-shot prompting
  to select same-audio tools and return structured temporal evidence without task-specific tuning.
- **Data obtainable:** Yes for a bounded test. MMAU material is already local; exact full evaluation
  still depends on the paper's chosen services and tool implementations.
- **Baseline locally/API reproducible:** Partly. The
  [official repository](https://github.com/gary920209/Audio-Maestro) contains code and environment
  material, but its README still marks several model, tool-interface, and evaluation scripts as TODO,
  and no license is declared. Reproduce the interface from the paper rather than treating the repo as
  a turnkey artifact.

### 7. Unit-Based Agent (`2601.20230`)

- **Technical solution reproducible:** Yes. The frozen MLLM decides among `keep listen`,
  `listen-to-speak`, `keep speak`, and `speak-to-listen`, with asynchronous ASR context and no
  additional training.
- **Data obtainable:** Conditional. The HumDial challenge data must be obtained and placed manually;
  it is not bundled in the code repository.
- **Baseline locally/API reproducible:** A reduced smoke is feasible, but exact reproduction is heavy.
  The [Apache-2 repository](https://github.com/yu-haoyuan/fd-badcat) supplies Docker, setup, inference,
  and evaluation paths, while the paper stack uses Qwen3-Omni-30B-A3B plus separate ASR and TTS and
  reports multi-A100 execution. Use API/substitute components before attempting the exact stack.

### 8. i-Code Studio (`2305.13738`)

- **Technical solution reproducible:** Yes. It composes frozen AI skills into configurable DAGs and is
  explicitly finetuning-free; speech, vision, and language services are replaceable nodes.
- **Data obtainable:** A smoke needs only example inputs. Exact historic demonstrations rely on the
  original service configurations rather than a packaged evaluation dataset.
- **Baseline locally/API reproducible:** Conditional. The
  [released implementation](https://github.com/microsoft/i-Code/tree/main/i-Code-Studio) includes
  agent/web-app code, but the old Azure Speech/Vision/OpenAI dependencies and sparse documentation
  make dependency repair likely.

### 9. FAM-HRI (`2503.16492`)

- **Technical solution reproducible:** The external orchestration of fixed foundation models and the
  fusion of speech plus gaze are reproducible in principle.
- **Data obtainable:** Not as an exact local benchmark; evaluation depends on recorded multimodal HRI
  sessions and physical setup.
- **Baseline locally/API reproducible:** Conditional. The
  [public repository](https://github.com/laiyuzhi/FAM-HRI) exists, but no license was confirmed and
  exact execution requires Meta Aria glasses and robot hardware. Retain the fusion/control method,
  not a near-term exact reproduction.

## I0 — executable speech-agent evaluation resources

These are evaluation instruments, not claims that their paper methods should be reproduced.

### 10. Audio2Tool (`2604.22821`)

- **Technical scheme:** Direct spoken-command-to-tool-call and parameter evaluation across eight
  difficulty tiers; no model training is necessary to use the benchmark.
- **Data:** The [Hugging Face release](https://huggingface.co/datasets/RVtech/Audio2Tool) has 30,733
  rows, about 59.6 hours of audio and roughly 10.4 GB, under CC BY-NC 4.0.
- **Baseline:** A low-tier bounded slice can run locally or against a speech/omni API. Full-corpus use
  is unnecessary for the first comparison.

### 11. VoiceAgentBench (`2510.07978`)

- **Technical scheme:** More than 6,000 spoken queries covering tool calls, workflows, multi-turn
  interaction, safety, English, and six Indic languages.
- **Data:** Public through the
  [dataset release](https://huggingface.co/datasets/krutrim-ai-labs/VoiceAgentBench); verify the custom
  Krutrim Community License before redistribution.
- **Baseline:** The [evaluation repository](https://github.com/ola-krutrim/VoiceAgentBench) supports
  speech/omni models and cascades; exact judging uses external APIs, which is acceptable but adds cost.

### 12. Full-Duplex-Bench v3 (`2604.04847`)

- **Technical scheme:** Real disfluent human audio, overlap, multi-step tools, and strict full-duplex
  behaviour expose control failures hidden by clean turn-based speech.
- **Data:** Released from the
  [official repository](https://github.com/DanielLin94144/Full-Duplex-Bench), with data hosted through
  its documented download route.
- **Baseline:** The repository includes v1 through v3 code/data and API-facing evaluation. Prefer v3;
  v1.5 (`2507.23159`) is retained only as a historical/smaller instrument.

### 13. tau-Voice (`2603.13686`)

- **Technical scheme:** Voice/full-duplex extension of a policy-and-tool benchmark with 278 tasks in
  retail, airline, and telecom domains.
- **Data:** Tasks, policies, tools, and simulators are released in
  [tau2-bench](https://github.com/sierra-research/tau2-bench).
- **Baseline:** Reproducible through OpenAI, Gemini, or xAI routes; the limiting resource is API usage,
  not private data or model training.

### 14. EVA-Bench (`2605.13841`)

- **Technical scheme:** End-to-end voice-agent evaluation over 213 scenarios, 121 tools, and three
  domains.
- **Data:** Public in the
  [ServiceNow dataset](https://huggingface.co/datasets/ServiceNow-AI/eva-bench).
- **Baseline:** The [open framework](https://github.com/ServiceNow/EVA-Bench) is suitable for an API
  smoke; freeze a small scenario subset before use.

### 15. IHBench (`2606.19595`)

- **Technical scheme:** Tests whether a voice agent resumes structured work correctly after an
  interruption, rather than merely detecting barge-in.
- **Data:** The [released dataset](https://huggingface.co/datasets/bosonai/IHBench) contains 45
  synthetic conversations and 428 interruption points across ten domains and is only about 217 MB.
- **Baseline:** The [official repository](https://github.com/boson-ai/ihbench) makes this the cheapest
  new interruption smoke in the rescued set.

### 16. LALM audio-judge reliability for full-duplex voice agents (`2607.07985`)

- **Technical scheme:** It validates two raw-stereo-audio judges against three calibrated humans over
  eight speech and interaction dimensions, then probes six controlled DSP defects. This is directly
  relevant to deciding whether an audio-native reward/evaluator can safely drive inference-time
  selection.
- **Data:** The
  [CC-BY-4.0/Apache-2 release](https://huggingface.co/datasets/armaan-sayyad/lalm-judge-validation-full-duplex)
  includes anonymized ratings, prompts, schemas, analysis scripts, and figures. The 209 production
  recordings remain private; the paper says adversarial WAV release is pending data clearance.
- **Baseline:** Every published table can be regenerated locally from the released CSVs. Re-running
  the judges requires Gemini/Vertex API access; reproducing raw-audio correlations is conditional on
  released audio or a replacement corpus. Treat its identified audio-clarity failures as a warning
  against using a single LALM judge as the sole reward.

## I1 — use selectively, not as primary speech reproduction

| Paper | Technical transfer | Data/resource state | Baseline route |
|---|---|---|---|
| Full-Duplex-Bench v1.5 (`2507.23159`) | Overlap handling | Released in the same Full-Duplex-Bench repository | Use only if v3 compatibility fails. |
| OmniGAIA (`2602.22897`) | Native-omni web search and code-use evaluation | [Code/data/media released](https://github.com/RUC-NLPIR/OmniGAIA), 360 QA | Benchmark/base agent separable, but visual/web load dominates; proposed OmniAtlas trains. |
| OmniPlay (`2508.04361`) | Audio-visual environment feedback | [Apache-2 platform](https://github.com/fuqingbie/omni-game-benchmark), five games | Use as an environment design reference; it is not speech-primary. |
| OmniGUI (`2605.18758`) | Audio/video/image smartphone trajectories | [Project page](https://omni-gui.github.io/), 709 episodes and 2,579 steps | Evaluation-method transfer only; visual GUI control dominates. |
| TOBench (`2605.16909`) | Closed-loop execute-inspect-revise with grounded verifiers and 27 MCP servers | [Open repository](https://github.com/Pi3AI/TOBench), 100 executable tasks and 324 tools | Audio appears among many asset modalities; use verifier/MCP design, not as a speech-primary leaderboard. |

## WAIT_ARTIFACT — recheck release status, do not implement from prose

| Paper | Technical reproducibility | Data availability | Baseline status |
|---|---|---|---|
| AudioRAG (`2602.10656`) | Audio plus web retrieval and agentic baseline are root-aligned. | Paper benchmark is described, but no official downloadable release was confirmed. | No paper-specific repository confirmed; unrelated packages named AudioRAG do not count. |
| WearVox (`2601.02391`) | Multichannel wearable voice assistant with search-grounded QA and tool calling. | 3,842 real recordings are described; official downloadable artifact not confirmed. | Wait for the authors' code/data rather than rebuilding the collection. |
| ContextDialog (`2502.19759`) | Voice-agent conversational-memory evaluation is relevant. | Public benchmark artifact not confirmed. | No exact runnable baseline confirmed. |
| Interactive ASR (`2604.09121`) | LLM-driven multi-turn correction and semantic judging fit external control. | Standard ASR datasets are public. | Abstract promises a future code release; no artifact was verified. |
| VCB Bench (`2510.11098`) | Real-speech conversational-agent evaluation is relevant. | Real Chinese speech is described. | Reproducible code/data release was not confirmed in this pass. |
| ProVoice-Bench (`2604.15037`) | 1,182 samples test implicit tool triggers, latent-topic monitoring, corrective interruption, and environmental-sound sensing. | The paper gives a complete synthesis recipe and public source datasets, but no official benchmark download was found. | Strong root fit; wait for the authors' packaged data/evaluator rather than rebuilding synthetic speech. |

## Full-text rechecked but not promoted as agent reproductions

Three released speech capability benchmarks were deliberately not promoted: SpokenWOZ (`2305.13040`)
provides 249 hours of task-oriented human dialogue, VoiceBench (`2410.17196`) tests general voice
assistant knowledge/instruction/safety robustness, and MultiVox (`2507.10859`) adds speech-plus-visual
paralinguistic grounding. Their data are useful for component diagnostics, but none exercises an
external tool/action/control loop. Under the root contract, reproducing their dataset leaderboards
would spend effort on speech capability rather than multimodal-agent control.

## Method-only vertical systems

The following twelve papers remain useful for architecture ideas but should not become dataset or
baseline reproduction tasks under the speech-agent root:

| Paper(s) | What transfers | Why not reproduce |
|---|---|---|
| AI-Care (`2605.08480`), care-home smart speaker (`2603.23625`), VOICE stroke assessment (`2507.22898`) | Stateful safety gates, clarification, confidence-aware deferral, human oversight | Private/simulated clinical or care workflows and safety-critical task definitions dominate. |
| VISA surgical agent (`2511.07392`) | Voice-triggered multi-agent routing over CT/3D state | Surgical data, 3D stack, and artifact access are not established. |
| Talk2Data (`2511.18405`) | Sandboxed execution and spoken front end | The load-bearing task is table analysis, not speech reasoning. |
| Rhetor (`2606.30294`) | Rehearsal loop for live voice Q&A | No code or evaluation data confirmed; web/visual demo is dominant. |
| One Supervisor (`2603.11545`) | Adaptive modality-tool orchestration | Generic omni method without verified speech-specific artifact. |
| RECOVER (`2603.16411`) | Multi-hypothesis ASR correction/retrieval | Exact artifact/data route not verified; retain as a correction policy. |
| VoicePilot (`2404.04066`) | Speech interface for physical assistance | Robot and human-study infrastructure dominate. |
| AI glasses (`2601.06235`) | Dual voice agent, MCP tools, RAG, and message-bus topology | No reusable code/evaluation artifact confirmed. |
| JANUS (`2602.00675`) | Typed factored controller, persistent memory, sufficiency and grounding gates | Dialogue control is valuable, but raw speech/audio is not demonstrated as load-bearing. |
| Y-BotFrame (`2606.13049`) | Plug-in speech/vision/LiDAR embodied modules | Quadruped and LiDAR hardware dominate exact reproduction. |

## Inherited and newly confirmed non-promotions

The pass did not recycle already known model-training or model-structure papers into the candidate
queue. It newly encountered eleven such records and preserved them only in the audit ledger. Examples
include Stream RAG (post-training), DuplexSLA and VoxMind (native model architectures), HEAR (world
model and policy training), SpeechAgents (Multi-Agent Tuning), PRISM (fine-tuned responder),
FireRedChat (trained pVAD/EOT components), LTS-VoiceAgent (fine-tuned semantic trigger), and
Thinking While Speaking (large synthetic training set). Their orchestration ideas may be cited, but
they are not reproduction candidates under the frozen black-box contract.

## Recommended execution order

No execution is authorized by this report. If Stage-2A authority is granted, the lowest-risk sequence
is:

1. run the Enterprise Realtime Voice Agent API path as the control/latency sanity baseline;
2. run VoiceAgentRAG on its bundled NovaCRM material, first fully local and then with the same API
   model used in step 1;
3. run a one-audio Thinking-with-Sound operator trace, then a bounded public MELD slice;
4. build Langbar's example app and inspect MCP tool scoping without reproducing the paper leaderboard;
5. build Pepper's standalone Android flavor, leaving physical robot actions simulated;
6. freeze one small cross-system evaluation slice from Audio2Tool, IHBench, or Full-Duplex-Bench v3;
7. attempt Audio-Maestro, Unit-Based Agent, i-Code Studio, or FAM-HRI only after their named blockers
   are deliberately accepted.

This ordering tests the project's external-control thesis while keeping model choice, API access,
speech input, and evaluation scope explicit.

## Evidence boundary

- Thirty-nine PDFs were downloaded by known arXiv ID and extracted without failure; no new discovery
  query expanded D0.
- Official project/repository/dataset pages were checked on 2026-07-22 for the named manual decisions.
- No repository was cloned, no dataset was downloaded, no model/API was called, and no benchmark was
  executed.
- "Public repository" means the page and declared contents were verified; it does not imply that every
  paper number has been independently reproduced.
