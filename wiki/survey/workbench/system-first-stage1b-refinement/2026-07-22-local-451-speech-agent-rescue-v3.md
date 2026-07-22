# Local 451 speech-agent rescue v3

## Decision

The second rescue pass changes the reproduction outlook materially. After inheriting the existing
decisions for papers that train models, alter model structure, or require model-internal state, the local
corpus contains **four additional artifact-backed speech/omni external-control systems** that were
under-ranked by the v4 resource router:

1. Audio-Mind (`2605.28480`)
2. Agent-Omni (`2511.02834`)
3. AURA (`2506.23049`)
4. Agentic ASR (`2605.29430`)

It also contains one immediately usable audio-driven agent benchmark, Omni-DeepSearch (`2605.08762`),
and two conditional direct candidates, LongShOTAgent (`2512.16978`) and MIST (`2605.06897`). This page
supersedes the execution queue in
[`2026-07-22-speech-omni-agent-reproduction-routing-v2.md`](2026-07-22-speech-omni-agent-reproduction-routing-v2.md).
It does not reopen D0 discovery and does not authorize model runs.

## Audit scope and no-repeat rule

- Source: every PDF under `SPEECHRL_DATA_DIR/survey-fulltext`.
- Inventory: **451/451 unique PDFs present and extracted** in the v4 analysis snapshot.
- Inherited hard exclusions: **105 `EXCLUDE_MODEL_OPERABLE` + 17
  `EXCLUDE_MODEL_INTERNAL_ACCESS` = 122 papers**. These were not re-analysed as candidates.
- Rescue nets on the remaining corpus:
  - 107 papers matched an early-page audio/speech/omni plus agent/control signal;
  - 71 papers independently matched speech-primary plus external-control signals.
- Human audit then required load-bearing speech/audio input, an agent or externally composable control
  loop, and compatibility with a frozen black-box backbone. Text-only and visual-only work remained
  method transfer, even when its dataset and code were excellent.
- Live artifact checks were performed on 2026-07-22. "Code promised" is not counted as code available.

## Revised executable queue

### P0 - artifact-backed system smoke and small-slice reproduction

| Order | Paper | Why it survives the root gate | Data state | Baseline state |
|---:|---|---|---|---|
| 1 | Audio-Mind | Native audio questions; external planner, conditional tool acquisition, evidence fusion, validation, and stopping; no backbone update. | MMAR is already local; MSU-Bench is not yet locked. | Official MIT repository, API-compatible planner/frontend, local tool wrappers, setup and verification scripts. |
| 2 | AudioToolAgent | Existing exact audio tool-orchestration prior. | MMAR and compatible MMAU material are local. | Existing author artifact remains the first matched-paper reproduction. |
| 3 | Agent-Omni | Audio is one of four first-class inputs; master agent delegates to modality agents and iteratively fuses outputs without fine-tuning. | No dataset is needed for a smoke test; exact paper leaderboard inputs still need a manifest. | Official repository supports OpenAI-compatible APIs, Bedrock, and local/vLLM backends. |
| 4 | AURA | Speech-to-speech, multi-turn, tool-using assistant with calendar, contacts, email, and web search. | VoiceBench evaluation code exists; human-evaluation data are external. | Official repository has runnable agent/UI paths. Optional ASR/DST fine-tuning folders are outside the reproduction scope. |
| 5 | Agentic ASR | Speech recognition is converted from one-shot decoding into correction, intent-routing, semantic judging, and iterative repair. | Minimal JSONL and example audio are included; full paper benchmark releases are incomplete or separately constrained. | Official orchestration/evaluation code runs against external ASR, TTS, and OpenAI-compatible LLM endpoints. |
| 6 | EChO-Agent | Existing direct clean-room target for staged audio evidence orchestration. | MMAR is local. | No author repository was confirmed; retain as clean-room rather than artifact reproduction. |

The first practical experiment should compare **Audio-Mind vs AudioToolAgent vs no-tool direct
inference on the same MMAR slice and same backbone**. Agent-Omni, AURA, and Agentic ASR then test
coordination, task execution, and correction-loop generality rather than competing on a mismatched
leaderboard.

### I0 - executable evaluation instrument

**Omni-DeepSearch (`2605.08762`)** is not a method reproduction, but it is the cleanest new root-aligned
evaluation asset. Its 640 examples begin with one or more audio clips, require models to formulate
queries and invoke text/image/video search, and include answer and optional golden-path fields. The
[official repository](https://github.com/yutao1024/Omni-DeepSearch) provides generation/evaluation code,
and the [Hugging Face dataset](https://huggingface.co/datasets/Kirito-Lab/Omni-DeepSearch) is currently
available as 640 rows and about 632 MB. Use a bounded speech-bearing slice first; do not regenerate the
benchmark.

### P1 - direct fit with a material execution blocker

| Paper | Technical fit | Data/resource blocker | Route |
|---|---|---|---|
| LongShOTAgent (`2512.16978`) | Training-free search-refine-verify agent over visual, speech, and ambient-audio evidence. | The repository is complete, but the full benchmark spans 274 long videos and about 188 hours; raw media depend on YouTube availability/cookies and the stack needs several specialist models. | Reproduce only a small audio/speech-dependent slice after P0. |
| MIST (`2605.06897`) | Synthetic multi-turn speech tool-calling with device state, mixed initiative, clarification, and physical constraints. | The paper says data and generator are released, but the linked project page currently exposes examples only; no public repository or downloadable dataset was found. | Keep as `WAIT_ARTIFACT`; do not implement from prose yet. |

## One-by-one rescue reports

### 1. Audio-Mind (`2605.28480`) - P0

- **Technical solution reproducible:** Yes. The system is an explicit state graph: initial native-audio
  perception, evidence-gap planning, bounded external tool calls or targeted re-listening, evidence
  fusion, answer generation, and format validation. Training mentions in the PDF refer to related work,
  not the proposed method.
- **Data obtainable:** Partly and sufficiently for a first reproduction. MMAR is in the local lock;
  MSU-Bench still needs a source/lock check. Individual tools may require gated or non-commercial
  weights.
- **Baseline locally reproducible:** Yes for smoke and a matched MMAR slice. The
  [official repository](https://github.com/DELTA-DoubleWise/Audio-Mind) provides an API route needing no
  local planner/LALM GPU, an OpenAI-compatible frontend, a local Qwen frontend example, MCP tool
  environments, model download, and verification scripts. Exact paper scores remain conditional on
  tool weights, API versions, and MSU-Bench.
- **Main value:** Closest operational prior to W1: preserve the frozen audio model's own judgment and
  escalate only when an evidence gap justifies the tool cost.

### 2. Agent-Omni (`2511.02834`) - P0

- **Technical solution reproducible:** Yes. A master agent detects modalities, decomposes the request,
  delegates to text/image/audio/video agents, and iteratively fuses structured outputs. The paper and
  repository explicitly state no fine-tuning or retraining.
- **Data obtainable:** A smoke test needs only user-supplied multimodal inputs. Reproducing every paper
  number requires a still-unfrozen benchmark manifest.
- **Baseline locally reproducible:** Yes. The
  [official repository](https://github.com/huawei-lin/Agent-Omni) includes vanilla and agent test
  entrypoints and independently configurable OpenAI-compatible, Bedrock, or local model backends.
- **Main value:** A direct black-box baseline for testing whether heterogeneous specialist coordination
  beats a single omni model under equal API/model access.

### 3. AURA (`2506.23049`) - P0

- **Technical solution reproducible:** Yes, with a scoped path. The inference system is a modular
  ASR -> ReAct-style LLM agent -> tools -> TTS cascade with multi-turn state. The repository also contains
  optional accent-ASR and dialogue-state fine-tuning; those directories must be excluded from W1.
- **Data obtainable:** VoiceBench evaluation scripts are present. The human task set/annotations are
  linked externally and are not necessary for a tool-call smoke test.
- **Baseline locally reproducible:** Yes. The
  [official repository](https://github.com/Sentientia/Aura) supplies environment setup, a Gradio speech
  interface, action handlers, and LLM/API configuration. Calendar/email demonstrations require user
  credentials, while chat and mock/local tools do not.
- **Main value:** End-to-end speech-agent engineering baseline and a test of whether the control-plane
  result survives ASR/TTS boundaries.

### 4. Agentic ASR (`2605.29430`) - P0, partial paper-number reproduction

- **Technical solution reproducible:** Yes. It treats a current transcript, semantic error signal, user
  correction, and revised hypothesis as an external multi-turn state; no ASR/LLM weight update is part of
  the public artifact.
- **Data obtainable:** The repository includes example audio and a minimal JSONL contract. The full
  GigaSpeech/WenetSpeech/NER/code-switch experiment package is not completely bundled.
- **Baseline locally reproducible:** Yes for the minimal closed loop and S2ER evaluation. The
  [official repository](https://github.com/InteractiveASR/AgenticASR) expects external ASR, TTS, and
  OpenAI-compatible LLM endpoints and publishes stage-0, one-loop, and evaluation commands. Full paper
  tables are conditional on the original service stack and benchmark access.
- **Main value:** A cheap, directly speech-grounded repair/continue/stop testbed for the control plane.

### 5. Omni-DeepSearch (`2605.08762`) - I0

- **Technical solution reproducible:** The benchmark pipeline and evaluator are reproducible; the paper
  contributes the benchmark rather than a new control algorithm.
- **Data obtainable:** Yes, immediately: 640 audio-bearing examples across single/multi-audio,
  audio-to-image, and audio-to-video-search routes.
- **Baseline locally reproducible:** Yes with external search/model APIs, but a small fixed slice is the
  right first contract because open-web results drift.
- **Main value:** Tests the exact chain audio clue -> query -> external cross-modal evidence ->
  verification, which local MMAR does not cover.

### 6. LongShOTAgent (`2512.16978`) - P1

- **Technical solution reproducible:** Yes. It builds a searchable multimodal store and exposes
  `search_video`, `refine_video`, and `verify_claim` in a training-free ReAct loop.
- **Data obtainable:** Metadata and code are public, but full raw-video recovery depends on source media
  still being available. The complete 188-hour corpus is unnecessarily expensive for W1.
- **Baseline locally reproducible:** A bounded slice is reproducible from the
  [official repository](https://github.com/mbzuai-oryx/LongShOT). Full reproduction needs Audio Flamingo,
  VLM/LLM servers, preprocessing, and raw videos.
- **Main value:** Strong method analogue for evidence stores and modality-specific re-inspection. It is
  not ahead of P0 because long-video visual work would dominate the experiment.

### 7. MIST (`2605.06897`) - P1 wait

- **Technical solution reproducible:** The task and state transitions are described well enough to
  understand, but clean-room implementation would precede artifact confirmation.
- **Data obtainable:** Not currently confirmed. The linked
  [project page](https://billyzhang24kobe.github.io/mist-smarthome/) displays example dialogues but no
  download or code link.
- **Baseline locally reproducible:** Not yet as a paper reproduction. Frontier API baselines could be
  rebuilt only after the dataset/generator appears.
- **Main value:** Excellent future testbed for spoken mixed initiative, clarification, stateful tool
  calls, and execution correctness.

### 8. CarMem (`2501.09645`) - method/component only

- **Technical solution reproducible:** Yes: external category-bounded preference extraction,
  maintenance, contradiction handling, and retrieval.
- **Data obtainable:** Yes. The [official repository](https://github.com/johanneskirmayr/CarMem) contains
  the dataset, generator, and experiment code.
- **Baseline locally reproducible:** Yes with OpenAI/Azure API and a local Milvus instance.
- **Route reason:** The scientific method operates on conversation text after speech has been removed;
  under the root contract, absorb the memory schema and maintenance tests instead of reproducing its
  text dataset scores.

### 9. OpenOmni (`2408.03047`) - engineering platform only

- **Technical solution reproducible:** Yes as a modular data/client/API/agent platform for audio/video
  conversational systems, latency logging, annotation, and component swapping.
- **Data obtainable:** It is infrastructure, not a canonical evaluation dataset.
- **Baseline locally reproducible:** The
  [official repository](https://github.com/AI4WA/OpenOmniFramework) supports all-local, private-network,
  and cloud deployment, but the full Django/Neo4j/PostgreSQL stack is heavier than the P0 harness.
- **Route reason:** Reuse selected observability and pipeline ideas; do not treat platform deployment as
  a research-paper reproduction.

### 10. Multi-agent Auditory Scene Analysis (`2507.02755`) - systems analogue only

- **Technical solution reproducible:** Yes. Localization, separation, and classification agents exchange
  feedback in a public ROS2/JACK system.
- **Data obtainable:** It relies on live or supplied audio scenes rather than a hidden vertical corpus.
- **Baseline locally reproducible:** Likely yes from the
  [official repository](https://github.com/balkce/masa), but the audio middleware setup is non-trivial.
- **Route reason:** It is a useful control-topology analogue, not an omni foundation-model agent.

### 11. AMUSE (`2512.16250`) - instrument/method only

- **Technical solution reproducible:** The zero-shot, guided, and agentic evaluation protocols are
  conceptually reproducible, including calls to ASR, diarization, and face tools. The proposed RAFT
  improvement updates cross-modal layers and is excluded.
- **Data obtainable:** No public code/data artifact was linked in the local PDF or found in the live
  verification.
- **Baseline locally reproducible:** Not currently as an exact benchmark. Individual tool-mode ideas can
  be ported to a local speech-bearing evaluation set.
- **Route reason:** Keep its three-mode evaluation design; do not reproduce RAFT or pursue a visual-heavy
  leaderboard.

### 12. SpeechRole (`2508.02013`) - instrument only

- **Technical solution reproducible:** The evaluation dimensions and cascaded vs end-to-end comparison
  are clear, but this is role-playing evaluation rather than external reward-guided control.
- **Data obtainable:** Release/access and source-media licensing were not sufficiently confirmed for an
  immediate local lock.
- **Baseline locally reproducible:** API models can be queried, but without a frozen public release it is
  not an exact baseline reproduction.
- **Route reason:** Retain speech-interaction metrics only.

### 13. MAR3 (`2603.27706`) - visual transfer only

- **Technical solution reproducible:** The training-free consensus -> reasoning -> segmentation -> check
  and prompt-correction loop is externally composable.
- **Data obtainable:** Ref-AVSBench is named and public-facing, but no author implementation was linked.
- **Baseline locally reproducible:** A clean-room version is possible but would reproduce an
  audio-visual segmentation task and its visual stack.
- **Route reason:** Absorb Delphi-style consensus and reflective correction; do not reproduce the visual
  dataset or baseline.

### 14. TRIAGE (`2604.12647`) - vertical method only

- **Technical solution reproducible:** Yes: frozen audio-text embeddings, confidence exit, descriptor
  matching, then retrieval plus LLM reasoning for unresolved cases.
- **Data obtainable:** The paper uses five public respiratory-audio corpora; exact prepared splits and an
  external code repository were not confirmed.
- **Baseline locally reproducible:** The algorithm is straightforward, but the target is medical sound
  classification, not a speech/omni agent.
- **Route reason:** Absorb the adaptive escalation and equal-budget tests; do not reproduce its vertical
  datasets.

## Important negative findings

The rescue did not promote the following classes:

- **Previously recognized trainable/model-structure work:** inherited and skipped, including Native
  Active Perception and the broader 122-paper hard-exclusion set.
- **New false training-free labels:** UITron-Speech trains the LLM and grounding/planning stages;
  Phoenix-VAD trains an adapter and LoRA; AMUSE's RAFT updates multimodal layers. Only their separable
  inference/evaluation ideas survive.
- **Gray-box decoding:** Audio-Aware Decoding needs token logits with and without audio and therefore
  violates the black-box root despite public code.
- **Generation/captioning/localization:** AudioGenie, Audio-Oscar, AuDirector, StoryTeller, SCORE, sound
  localization, caption calibration, and similar papers remain method-adjacent; their target outputs are
  not speech/omni-agent evidence seeking.
- **Text/visual keyword false positives:** ReAct, MMA, Team of Thoughts, OmniVerifier, VLM test-time
  scaling, payment workflows, and other non-speech works remain method cards only.

## Next contract, not yet executed

1. Freeze one small MMAR slice and a no-tool direct-inference control.
2. Pin Audio-Mind and AudioToolAgent repository commits, model/API IDs, tool inventory, and output
   schema.
3. Run the same backbone under direct, always-tool, and conditional-tool policies with equalized maximum
   calls and logged cost/latency.
4. Use Agentic ASR example audio as the first repair/stop smoke test.
5. Add a bounded speech-bearing Omni-DeepSearch slice only after the local closed-set control works.

No repository clone, model load, dataset download, API call, or experimental run was performed in this
rescue pass.
