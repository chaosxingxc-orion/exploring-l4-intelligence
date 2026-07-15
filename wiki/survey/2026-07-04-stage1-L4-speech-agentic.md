# Stage-1 lane L4 — Speech-Agentic tasks

> Stage-1 problem-definition campaign lane · 2026-07-04 · workflow `wf_d7b939e9-c37` · methodology:
> CLAUDE.md three-stage section (Stage 1: survey-grounded argumentation; in-house numbers
> directional-only). Yardstick: [[2026-07-04-sufficiency-yardstick-memo]]. Every claim carries
> origin-domain (llm/vlm/speech), transfer-status, fence, ladder-condition and problem-anchor
> tags; every URL adversarially verified; P0 gate enforced (anchor-less claims struck).

## Open problems (P0-compliant: task-level, metric-named, literature-anchored)

### P1-voice-task-completion-collapse — ladder: mixed

Full-duplex voice agents complete far fewer verifiable-reward customer-service tasks than same-generation text agents: text SOTA (GPT-5 reasoning) 85% pass@1 vs 31-51% under clean audio and 26-38% under realistic audio (30-45% retention of text capability under realistic audio), with 79-90% of failures agent-driven — logical errors despite accurate transcription, hallucinated tool completions, and going silent — i.e., the deficit sits in the agent loop, not merely the ASR front-end.

**Metric:** pass@1 / pass^k task success verified by database state change (tau-bench-style env assertion)

**Named by:** [tau-Voice: Benchmarking Full-Duplex Voice Agents on Real-World Domains](https://arxiv.org/abs/2603.13686) (2026-03) · [Full-Duplex-Bench-v3: Benchmarking Tool Use for Full-Duplex Voice Agents Under Real-World Disfluency](https://arxiv.org/abs/2604.04847) (2026-04) · [tau2-bench voice README (sierra-research)](https://github.com/sierra-research/tau2-bench/blob/main/src/tau2/voice/README.md) (2025)

### P2-spoken-instruction-following-reasoning-gap — ladder: b2

End-to-end speech LLMs lose instruction-following and reasoning relative to their own text backbones: GPT-4o drops from 92% (text) to 66% (speech-to-speech) on Big Bench Audio; URO-Bench finds open-source spoken dialogue models 'lag behind their backbone LLMs in terms of instruction-following ability and also suffer from catastrophic forgetting'; VoiceBench shows speaker, environment, and content variations degrade all LLM voice assistants while a naive ASR cascade outperforms all open-source end-to-end models by over 20 points on spoken instructions (proprietary GPT-4o-Audio still slightly lags its pipeline counterpart).

**Metric:** accuracy on spoken versions of text tasks (Big Bench Audio, IFEval/AlpacaEval-audio, URO-Bench basic/pro tracks) vs the text-input baseline of the same backbone

**Named by:** [Evaluating Audio Reasoning with Big Bench Audio (Artificial Analysis / HF blog)](https://huggingface.co/blog/big-bench-audio-release) (2024-12) · [VoiceBench: Benchmarking LLM-Based Voice Assistants](https://arxiv.org/abs/2410.17196) (2024-10) · [URO-Bench: Towards Comprehensive Evaluation for End-to-End Spoken Dialogue Models](https://arxiv.org/abs/2502.17810) (2025-02) · [S2SBench: A Benchmark for Quantifying Intelligence Degradation in Speech-to-Speech LLMs](https://arxiv.org/abs/2505.14438) (2025-05)

### P3-dialog-state-under-interruption — ladder: b2

Voice agents cannot maintain and update dialog state under full-duplex phenomena (interruptions, self-corrections, mid-utterance repairs): no evaluated model exceeds 50% pass on EchoChain's 200 interrupted conversations (best 47.5%), and a paired half-duplex control removes 40.2% of failures — isolating state-update-under-interruption as the cause; FDB-v3 names self-correction handling and multi-step reasoning under disfluency the most consistent failure modes (best Pass@1 0.600); Audio MultiChallenge's best model passes 54.65% with Self-Coherence degrading as audio context grows. All of this is WITHIN-session state — no cross-session memory involved.

**Metric:** pass rate on interrupted conversations (EchoChain); Pass@1 on chained tool calls under disfluency (FDB-v3); rubric pass rate incl. Instruction Retention / Self Coherence / Voice Editing axes (AudioMC)

**Named by:** [EchoChain: A Full-Duplex Benchmark for State-Update Reasoning Under Interruptions](https://arxiv.org/abs/2604.16456) (2026-04) · [Full-Duplex-Bench-v3](https://arxiv.org/abs/2604.04847) (2026-04) · [Audio MultiChallenge: A Multi-Turn Evaluation of Spoken Dialogue Systems on Natural Human Interaction](https://arxiv.org/abs/2512.14865) (2025-12)

### P4-spoken-argument-fidelity — ladder: mixed

Tool-call argument values are corrupted by the speech channel: converting text tool benchmarks to audio costs 1.8-4.8 points on Confetti with 'misunderstandings of argument values in the speech' the primary failure mode; the best ASR-LLM pipelines reach only 60.6% average parameter-filling accuracy in English with sharper degradation in Indic languages; SpeechLM tool use degrades significantly under compositional plus acoustic challenge (Audio2Tool); tau-Voice localizes failures at name-spelling/authentication turns ('agents fail to transcribe names and emails even when spelled letter-by-letter, blocking all downstream actions').

**Metric:** parameter-filling / argument-value accuracy of tool calls issued from spoken queries (vs text-input annotations)

**Named by:** [From Text to Voice: A Reproducible and Verifiable Framework for Evaluating Tool Calling LLM Agents](https://arxiv.org/abs/2605.15104) (2026-05) · [VoiceAgentBench: Are Voice Assistants ready for agentic tasks?](https://arxiv.org/abs/2510.07978) (2025-10) · [Audio2Tool: Speak, Call, Act — A Dataset for Benchmarking Speech Tool Use](https://arxiv.org/abs/2604.22821) (2026-04)

### P5-speech-robust-verifiable-reward — ladder: c

Voice-agent task success is only half-verifiable: environment/database assertions transfer natively from tau-bench, but the communicate-to-user half must be judged from speech, and prompted (training-free) audio judges lag human judgment by 32 percentage points on average with severe calibration failures on ties, high numeric-scoring MSE (~1.8-3.5 across datasets), and only 53.4% objective accuracy for prompted Qwen2.5-Omni — so the reward any selection/reranking method would optimize is itself unreliable on the spoken side.

**Metric:** judge-human agreement (%), evaluator objective accuracy, calibration on tie/abstain cases

**Named by:** [ParaPairAudioBench: Paralinguistic Pairwise Audio Benchmark for LALM-as-a-Judge](https://arxiv.org/pdf/2606.24648) (2026-06) · [AudioJudge: Understanding What Works in Large Audio Model Based Speech Evaluation](https://arxiv.org/html/2507.12705) (2025-07) · [WavReward: Spoken Dialogue Models With Generalist Reward Evaluators](https://arxiv.org/abs/2505.09558) (2025-05)


## Approach genealogy & evidence claims (cross-domain mandatory)

### C01-tau-voice-gap-measured — [update] origin: **speech** · transfer: native · fence: training-free · ladder: background · anchor: P1-voice-task-completion-collapse

tau-Voice provides the first verifiable-reward quantification of the voice-vs-text agent gap on identical tasks: GPT-5 (reasoning) text 85% pass@1 vs voice agents 31-51% (clean) and 26-38% (realistic; gpt-realtime-1.5, gemini-live-2.5-flash-native-audio, grok-voice-agent), success deterministically evaluated by comparing end-of-episode database state to a gold standard; 79-90% of failures are agent-driven (logical errors despite accurate transcription, hallucinated completions — 'I've updated your shipping address' without any tool call — and VAD/unresponsive silence), and accents alone cost up to -18pp (xAI on Retail; Google nearly unaffected).

**Sources:** [tau-Voice: Benchmarking Full-Duplex Voice Agents on Real-World Domains](https://arxiv.org/abs/2603.13686) (2026-03) · [tau-Voice (HTML, results tables)](https://arxiv.org/html/2603.13686v1) (2026-03) · verified: True

*Origin-domain evidence:* Speech-native benchmark; abstract numbers (85% vs 31-51%/26-38%, 79-90% agent failures) and body details (model names Table 3, DB-state pass@1, -18pp accent ablation, hallucinated completions, VAD/Unresponsive) all re-fetched and verified verbatim this verification pass (2026-07-04).
*Speech-domain evidence:* Native (this is the speech-domain deficiency measurement itself).

### C02-taubench-passk-verifiable-reward — [update] origin: **llm** · transfer: native · fence: training-free · ladder: background · anchor: P1-voice-task-completion-collapse

tau-bench (LLM origin) supplies the reward design the whole family inherits: task success verified by comparing database state to an annotated goal state plus the pass^k reliability metric; frontier function-calling agents (like gpt-4o) succeed on <50% of tasks and are inconsistent (pass^8 <25% on retail). tau-Voice transplants this env to full-duplex audio unchanged — the verifiable task-success reward transfers natively to speech.

**Sources:** [tau-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains](https://arxiv.org/abs/2406.12045) (2024-06) · [tau-Voice](https://arxiv.org/abs/2603.13686) (2026-03) · verified: True

*Origin-domain evidence:* tau-bench abstract verified verbatim this pass: 'state-of-the-art function calling agents (like gpt-4o) succeed on <50% of the tasks', 'pass^8 <25% in retail', 'compares the database state at the end of a conversation with the annotated goal state'. Also archived (A4 lane).
*Speech-domain evidence:* tau-Voice adopts the same DB-state assertion over voice channels ('We report pass@1'); pass^k on voice agents itself remains unreported (see negative findings).

### C03-react-scaffold-genealogy — [new] origin: **llm** · transfer: partial · fence: training-free · ladder: b2 · anchor: P1-voice-task-completion-collapse

ReAct (LLM origin) is the prompt-scaffold that created the agent class under test: interleaved reasoning+acting via prompting alone improves success over imitation/RL baselines by +34pp (ALFWorld) and +10pp (WebShop) with only one or two in-context examples — no gradient updates. Voice agents inherit ReAct-style loops only via the cascade (ASR text in the loop); no audio-native ReAct evaluation surfaced.

**Sources:** [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629) (2022-10) · verified: True

*Origin-domain evidence:* Abstract verified verbatim this pass: 'ReAct outperforms imitation and reinforcement learning methods by an absolute success rate of 34% and 10% respectively, while being prompted with only one or two in-context examples.'
*Speech-domain evidence:* Partial: cascaded voice stacks (FDB-v3's Cascaded baseline; production voice-agent architectures) run the loop over ASR transcripts; no end-to-end audio-token ReAct result found.

### C04-cascade-regrounding-recovery — [new] origin: **speech** · transfer: native · fence: training-free · ladder: b2 · anchor: P2-spoken-instruction-following-reasoning-gap

The largest measured training-free lift in this family is re-grounding audio to text: a Whisper->GPT-4o->TTS pipeline shows minimal reasoning degradation vs text (~92%) where native S2S GPT-4o scores 66% (Big Bench Audio); VoiceBench's naive cascade outperforms all open-source end-to-end assistants by >20 points on spoken instructions, with end-to-end models more susceptible to noise; ASR-LLM pipelines beat end-to-end SpeechLMs on agentic parameter filling (up to 60.6%, VoiceAgentBench). Genuine-accuracy (b2) movement from pure input-conditioning on frozen models — at latency cost (cascade 10.12s vs ~4-5s native, FDB-v3).

**Sources:** [Evaluating Audio Reasoning with Big Bench Audio](https://huggingface.co/blog/big-bench-audio-release) (2024-12) · [VoiceBench: Benchmarking LLM-Based Voice Assistants](https://arxiv.org/abs/2410.17196) (2024-10) · [VoiceAgentBench](https://arxiv.org/abs/2510.07978) (2025-10) · verified: True

*Origin-domain evidence:* Speech-native measurements across three independent benchmarks re-verified this pass: BBA blog (92% text / 66% S2S / pipeline 'minimal performance degradation'), VoiceBench body ('naive pipeline-based voice assistant significantly outperforms all open-source end-to-end models... exceeding 20 points'), VoiceAgentBench abstract ('ASR-LLM pipelines outperform end-to-end SpeechLMs, achieving up to 60.6%').
*Speech-domain evidence:* Native.

### C05-vlm-gui-agent-trajectory — [new] origin: **vlm** · transfer: untransferred · fence: training-free · ladder: b2 · anchor: P1-voice-task-completion-collapse

The VLM/GUI-agent lineage is the closest cross-domain precedent for the voice-agent deficit: prompt-scaffolded multimodal agents opened at 12.24% vs human 72.36% on OSWorld (2024) and reached the low 70s by late 2025 (72.6% via multi-model rollout ensembles, surpassing the human baseline); the decisive training-free move was a grounding scaffold — Set-of-Mark prompting lets zero-shot GPT-4V outperform the fully-FINETUNED referring segmentation SOTA on RefCOCOg. No audio-native analog of mark-injection (acoustic anchors surfaced as tokens) exists; voice agents sit at the '12% stage' with only the full-cascade scaffold available.

**Sources:** [OSWorld: Benchmarking Multimodal Agents for Open-Ended Tasks in Real Computer Environments](https://arxiv.org/abs/2404.07972) (2024-04) · [Set-of-Mark Prompting Unleashes Extraordinary Visual Grounding in GPT-4V](https://arxiv.org/abs/2310.11441) (2023-10) · verified: True

*Origin-domain evidence:* OSWorld abstract verified verbatim: 'humans can accomplish over 72.36% of the tasks, the best model achieves only 12.24% success'; SoM abstract verified verbatim: 'GPT-4V with SoM in zero-shot setting outperforms the state-of-the-art fully-finetuned referring expression comprehension and segmentation model on RefCOCOg'; low-70s late-2025 figure re-verified via Agent S3 / behavior best-of-N reports (72.6% with GPT-5 + Opus 4.5).
*Speech-domain evidence:* none found — no audio-native grounding-mark scaffold surfaced (negative finding N4).

### C06-repeated-sampling-coverage — [new] origin: **llm** · transfer: untransferred · fence: training-free · ladder: a · anchor: P1-voice-task-completion-collapse

Large Language Monkeys (LLM origin) establishes condition (a) for agentic tasks: repeated sampling scales coverage over four orders of magnitude — SWE-bench Lite solved fraction rises 15.9% -> 56% at 250 samples (DeepSeek-Coder-V2-Instruct, beating the 43% single-sample SOTA) — and where automatic verifiers exist selection is free, while without them majority voting and reward models plateau beyond several hundred samples. No pass@k/oracle-over-sampling measurement exists on any voice-agent benchmark (verified empty), so H_fix/SUPPORT for speech-agentic is an unoccupied measurement cell.

**Sources:** [Large Language Monkeys: Scaling Inference Compute with Repeated Sampling](https://arxiv.org/abs/2407.21787) (2024-07) · verified: True

*Origin-domain evidence:* Abstract verified verbatim this pass: coverage 'scales with the number of samples over four orders of magnitude'; '15.9% with one sample to 56% with 250 samples, outperforming the single-sample state-of-the-art of 43%'; 'majority voting and reward models plateau beyond several hundred samples'.
*Speech-domain evidence:* none found — targeted searches for pass@k/best-of-N on voice-agent benchmarks returned empty; independently re-run and re-confirmed empty by this verifier (2026-07-04).

### C07-bon-agent-test-time-scaling — [new] origin: **llm** · transfer: untransferred · fence: training-free · ladder: c · anchor: P5-speech-robust-verifiable-reward

Scaling Test-time Compute for LLM Agents (LLM origin) shows best-of-N parallel sampling gives the best test-time gains for tool-using agents (~+8pp over baseline on GAIA, SOTA on levels 1-2), with list-wise verification the best merge strategy (+2-3 points over scoring/majority vote) and rollout diversification positive — i.e., condition (c) selection over agent rollouts is realizable in the origin domain when a verifier/judge exists. Untransferred to voice agents, where the tau2-style DB-state reward would make selection trivially verifiable inside benchmark envs.

**Sources:** [Scaling Test-time Compute for LLM Agents](https://arxiv.org/pdf/2506.12928) (2025-06) · [Scaling Test-time Compute for LLM Agents (abs)](https://arxiv.org/abs/2506.12928) (2025-06) · verified: True

*Origin-domain evidence:* Re-verified this pass: abstract confirms parallel sampling / verifiers+merging / diversified rollouts studied, 'the list-wise method performs best', diversified rollouts positive; results reporting confirms BoN gives the best gains with an eight-point improvement over baseline on GAIA (draft's '+7pp' corrected to ~+8pp).
*Speech-domain evidence:* none found on any voice-agent benchmark (negative finding N1).

### C08-gepa-prompt-space-headroom — [update] origin: **llm** · transfer: partial · fence: training-free · ladder: b2 · anchor: P1-voice-task-completion-collapse

GEPA (LLM origin, ICLR 2026 Oral) quantifies prompt-space headroom for agent scaffolds: reflective prompt evolution on frozen models outperforms GRPO weight training by 6% average (up to 20%) with up to 35x fewer rollouts, and beats the leading prompt optimizer MIPROv2 by over 10% — the strongest existing evidence that H_prompt exceeds gradient-trained gains at matched budgets. Speech-side transfer exists only as a non-peer-reviewed engineering demo (APE loop over Gemini Live voice function calling with audio test suites); zero published quantification on any voice-agent benchmark.

**Sources:** [GEPA: Reflective Prompt Evolution Can Outperform Reinforcement Learning](https://arxiv.org/abs/2507.19457) (2025-07) · [voice-assistant-prompt-optimization (APE for Gemini Live, sample app)](https://github.com/heiko-hotz/voice-assistant-prompt-optimization/) (2025) · verified: True

*Origin-domain evidence:* Abstract (v2, 2026-02-14, ICLR 2026 Oral) verified verbatim this pass: 'GEPA outperforms GRPO by 6% on average and by up to 20%, while using up to 35x fewer rollouts' (draft's 'up to 19pp' corrected to 20%); 'outperforms the leading prompt optimizer, MIPROv2, by over 10%'.
*Speech-domain evidence:* Engineering demo only, repo verified live: APE iteratively optimizing a Gemini Live voice assistant's function-calling system prompt against TTS-audio test suites; explicitly a sample/educational project (archived 2025-08), no peer-reviewed numbers.

### C09-speech-copilot-program-agent — [new] origin: **llm** · transfer: native · fence: training-free · ladder: b2 · anchor: P2-spoken-instruction-following-reasoning-gap

The task-decomposition/program-generation agent scaffold (HuggingGPT/code-as-policy class, LLM origin) transfers natively to speech: Speech-Copilot builds speech-specific toolsets by analyzing pre-collected task instructions and has an LLM-based agent perform tasks through program generation over speech modules, achieving state-of-the-art performance on the Dynamic-SUPERB benchmark (~55 tasks) 'without additional training processes required by end-to-end approaches'. Direct speech-native evidence that prompt-scaffold agents can out-reach end-to-end models on spoken-instruction task families.

**Sources:** [Speech-Copilot: Leveraging Large Language Models for Speech Processing via Task Decomposition, Modularization, and Program Generation](https://arxiv.org/abs/2407.09886) (2024-07) · [tau2-bench voice README (sierra-research)](https://github.com/sierra-research/tau2-bench/blob/main/src/tau2/voice/README.md) (2025) · verified: True

*Origin-domain evidence:* Scaffold genealogy: LLM-orchestrates-tools (HuggingGPT/AudioGPT lineage) and program generation from code-agent work.
*Speech-domain evidence:* Native instantiation verified from abstract this pass: toolset built from task instructions, program-generation agent, 'state-of-the-art performance on the Dynamic-SUPERB benchmark', explicitly no additional training.

### C10-audio-cot-mixed-transfer — [new] origin: **llm** · transfer: partial · fence: training-free · ladder: b2 · anchor: P2-spoken-instruction-following-reasoning-gap

CoT-scaffold transfer to audio is real but bounded: Audio-CoT (first systematic study) finds CoT prompting significantly improves easy/medium audio tasks but encounters challenges on hard tasks where reasoning chains can confuse the model rather than improve accuracy, with a positive correlation between reasoning-path length and accuracy; Thinking-with-Sound extends the chain with audio tool operations (interleaved acoustic analysis: noise suppression, source separation, temporal alignment) and its gains scale with model capacity (+24.73pp small models up to +36.61pp larger). Reachability via reasoning scaffolds is measured, positive-but-capped — the b2 evidence for spoken reasoning.

**Sources:** [Audio-CoT: Exploring Chain-of-Thought Reasoning in Large Audio Language Model](https://arxiv.org/abs/2501.07246) (2025-01) · [Thinking with Sound: Audio Chain-of-Thought Enables Multimodal Reasoning in Large Audio-Language Models](https://arxiv.org/abs/2509.21749) (2025-09) · verified: True

*Origin-domain evidence:* CoT and self-consistency genealogy (Wei et al.; self-consistency archived in survey bibliography).
*Speech-domain evidence:* Both abstracts verified verbatim this pass: Audio-CoT 'significantly improve performance on easy and medium tasks but encounter challenges with hard tasks, where reasoning chains can confuse the model' + 'positive correlation between reasoning path length and accuracy'; TwS 'small models gain 24.73% absolute accuracy, with improvements scaling consistently up to 36.61% for larger models'.

### C11-echochain-state-update — [update] origin: **speech** · transfer: native · fence: training-free · ladder: background · anchor: P3-dialog-state-under-interruption

EchoChain isolates dialog-state failure causally: across 200 interrupted conversations no model exceeds a 50% pass rate (GPT-realtime 44.0%, Grok Voice 47.5%, Gemini Live 16.5%, Nova Sonic 2 26%), while in a paired HALF-duplex control total failures drop by 40.2% relative to interrupted runs — proving the deficit is state-update reasoning under interruption, not task difficulty; named failure patterns: contextual inertia, interruption amnesia, objective displacement. Entirely within-session state (no closure-fence collision).

**Sources:** [EchoChain: A Full-Duplex Benchmark for State-Update Reasoning Under Interruptions](https://arxiv.org/abs/2604.16456) (2026-04) · [Introducing EchoChain (Labelbox blog)](https://labelbox.com/blog/introducing-echochain-an-audio-benchmark-for-reasoning-under-pressure-in-full-duplex-dialogue/) (2026-04) · verified: True

*Origin-domain evidence:* Speech-native controlled benchmark; abstract verified this pass ('no system exceeds a 50% pass rate', 'total failures drop by 40.2%', three failure patterns verbatim); per-model numbers (44.0/47.5/16.5, 200-row set) verified against the Labelbox post.
*Speech-domain evidence:* Native.

### C12-fdbv3-audiomc-disfluency — [update] origin: **speech** · transfer: native · fence: training-free · ladder: background · anchor: P3-dialog-state-under-interruption

Under real human disfluency, chained tool use degrades with self-correction handling and multi-step reasoning the most consistent failure modes: FDB-v3 best Pass@1 is 0.600 (GPT-Realtime) with the cascaded baseline achieving a perfect turn-take rate at 10.12s latency; Audio MultiChallenge (452 conversations from 47 speakers, 1,712 instance-specific rubrics) tops out at 54.65% pass (Gemini 3 Pro Preview Thinking) with models failing most on the new Voice-Editing axis and Self-Coherence degrading with longer audio context.

**Sources:** [Full-Duplex-Bench-v3](https://arxiv.org/abs/2604.04847) (2026-04) · [Audio MultiChallenge](https://arxiv.org/abs/2512.14865) (2025-12) · verified: True

*Origin-domain evidence:* Speech-native benchmarks; all result numbers verified verbatim from both abstracts this pass ('GPT-Realtime leads on Pass@1 (0.600)', 'perfect turn-take rate, incurs the highest latency (10.12 s)', '452 conversations from 47 speakers with 1,712 instance-specific rubrics', '54.65% pass rate', 'Self Coherence degrades with longer audio context').
*Speech-domain evidence:* Native.

### C13-argument-value-fidelity — [new] origin: **speech** · transfer: native · fence: training-free · ladder: background · anchor: P4-spoken-argument-fidelity

Argument-value fidelity is a distinct, named deficiency: dataset-agnostic text->voice conversion of tool benchmarks (Confetti, When2Call) costs 1.8 (Qwen3-Omni) to 4.8 (GPT-Realtime-1.5) points on Confetti with 'misunderstandings of argument values in the speech' the dominant failure; VoiceAgentBench's best pipelines reach 60.6% parameter-filling (English) with sharper Indic degradation; Audio2Tool (~30K queries, zero-shot voice cloning + diverse noise) shows strong simple-command performance with significant degradation under compositional and acoustic challenges.

**Sources:** [From Text to Voice: A Reproducible and Verifiable Framework for Evaluating Tool Calling LLM Agents](https://arxiv.org/abs/2605.15104) (2026-05) · [VoiceAgentBench](https://arxiv.org/abs/2510.07978) (2025-10) · [Audio2Tool: Speak, Call, Act](https://arxiv.org/abs/2604.22821) (2026-04) · verified: True

*Origin-domain evidence:* Three independent speech-native measurements all re-fetched and verified verbatim this pass: 'On Confetti, the text-to-voice gap ranges from 1.8 points for Qwen3-Omni to 4.8 points for GPT-Realtime-1.5' + argument-value failure sentence; '60.6% average parameter-filling accuracy on English' + Indic degradation; Audio2Tool 30K queries / voice cloning / compositional+acoustic degradation.
*Speech-domain evidence:* Native.

### C14-verifiable-reward-instruments — [new] origin: **llm** · transfer: native · fence: training-free · ladder: c · anchor: P5-speech-robust-verifiable-reward

In-fence verifiable-reward instruments for voice agents already exist and are cheap: tau2/tau-Voice environments assert success from database state (label-free at selection time inside the env, LLM assessment only for the communicate-info half); From Text to Voice converts any annotated text tool benchmark to audio WITHOUT re-annotation ('preserving the original dataset annotations') and shows open-source Qwen3 judges with at least 8B parameters exceed 80% agreement with proprietary judges. This makes speech-agentic the family where the yardstick's condition (c) is cheapest to instrument — the reward exists before any selector research starts.

**Sources:** [tau-Voice](https://arxiv.org/abs/2603.13686) (2026-03) · [From Text to Voice: A Reproducible and Verifiable Framework for Evaluating Tool Calling LLM Agents](https://arxiv.org/abs/2605.15104) (2026-05) · verified: True

*Origin-domain evidence:* DB-state assertion reward originates in tau-bench (2406.12045, verified); annotation-preserving conversion is dataset-agnostic (verified verbatim from 2605.15104 abstract).
*Speech-domain evidence:* Native transfer demonstrated: tau-Voice runs the reward over audio ('success is deterministically evaluated by comparing the end state of the environment... against a gold standard'); 2605.15104 runs it over TTS-converted benchmarks with speaker variation and environmental noise.

### C15-prompted-audio-judges-weak — [new] origin: **llm** · transfer: partial · fence: training-free · ladder: c · anchor: P5-speech-robust-verifiable-reward

Training-free (prompted) audio judges — the label-free selector instrument the house thesis would need for the non-verifiable half of voice-agent reward — measure weak: LALM judges lag human judgment by 32%p on average with severe calibration failures particularly in Tie cases where the correct decision is to abstain (ParaPairAudioBench, 5,175 pairs); pointwise numeric scoring shows high MSE (~1.8-3.5 across datasets), leading AudioJudge to find pairwise evaluation consistently more reliable and to recommend pairwise-only protocols; prompted Qwen2.5-Omni reaches only 53.4% objective accuracy as a dialogue evaluator (WavReward baseline). LLM-as-judge pathologies (position/self-preference bias, archived) carry over and worsen in audio.

**Sources:** [ParaPairAudioBench: Paralinguistic Pairwise Audio Benchmark for LALM-as-a-Judge](https://arxiv.org/pdf/2606.24648) (2026-06) · [AudioJudge: Understanding What Works in Large Audio Model Based Speech Evaluation](https://arxiv.org/html/2507.12705) (2025-07) · [WavReward: Spoken Dialogue Models With Generalist Reward Evaluators](https://arxiv.org/abs/2505.09558) (2025-05) · verified: True

*Origin-domain evidence:* LLM-as-judge genealogy with documented position bias / self-preference bias (both in the 2026-06-26 archive bibliography: arXiv 2406.07791, 2410.21819).
*Speech-domain evidence:* Speech-native measurements verified this pass: ParaPairAudioBench abstract verbatim ('lag behind human judgments by 32%p on average and exhibit severe calibration failures, particularly in Tie cases'); AudioJudge pairwise>pointwise finding verified, MSE values ~1.80-3.46 (TMHINTQ 3.46->1.80, SOMOS 3.31->2.81; draft's '3.60' upper bound tightened); WavReward abstract 53.4% prompted Qwen2.5-Omni.

### C16-trained-evaluator-ceiling — [new] origin: **speech** · transfer: native · fence: gradient-trained · ladder: c · anchor: P5-speech-robust-verifiable-reward

Out-of-fence positioning for condition (c): a gradient-trained audio reward model (WavReward, RL-trained on the ChatReward-30K preference dataset) lifts spoken-dialogue evaluation from 53.4% (prompted Qwen2.5-Omni) to 91.5% objective accuracy and leads subjective A/B testing by a margin of 83% — establishing that the judge deficit is trainable-away, and pricing what any training-free judge scaffold must chase; it is a trained-evaluator result, not evidence for in-fence selection.

**Sources:** [WavReward: Spoken Dialogue Models With Generalist Reward Evaluators](https://arxiv.org/abs/2505.09558) (2025-05) · verified: True

*Origin-domain evidence:* Abstract verified verbatim this pass: 'achieving a substantial improvement about Qwen2.5-Omni in objective accuracy from 53.4% to 91.5%'; 'multi-sample feedback via the reinforcement learning algorithm'; 'In subjective A/B testing, WavReward also leads by a margin of 83%'; ChatReward-30K confirmed.
*Speech-domain evidence:* Native.


## Training-free vs fine-tuned SOTA positioning

# L4-speech-agentic — training-free vs fine-tuned positioning (verified 2026-07-04)

**Task family.** Voice tool-use, dialog-state instruction following, and task completion over audio (tau-Voice / FDB-v3 / VoiceAgentBench / EchoChain / AudioMC / VoiceBench-class).

**Where the training-free frontier sits.** Every leaderboard number in this family is already a *frozen-model, prompt-scaffolded* measurement: the evaluated agents are frozen commercial S2S models (GPT-Realtime, Gemini Live, Grok Voice) driven by system prompts and tool schemas. The strongest measured training-free lever is **re-grounding audio to text** (cascade): Whisper->GPT-4o recovers reasoning to near text parity (~92% vs 66% native S2S on Big Bench Audio), beats all open-source end-to-end SpeechLMs by >20 points on spoken instructions (VoiceBench) and on agentic parameter filling (VoiceAgentBench, 60.6% best), and achieves a perfect turn-take rate on FDB-v3 — at a latency price (10.12s vs ~4-5s native). The cascade is this family's Set-of-Mark: the modality surfaced as text tokens makes the task reachable by prompting.

**Where the gradient-trained frontier sits.** (i) *Model level:* native S2S reasoning has now largely closed the Big Bench Audio gap by weight training — per [Artificial Analysis](https://artificialanalysis.ai/speech-to-speech) (checked 2026-07-04): GPT Realtime 83% (vs GPT-4o Realtime's 66% a year earlier), GPT-Realtime-2 (High) 97%, Gemini 2.5 Flash native-audio thinking 91%, Qwen3.5 Omni Plus Realtime 99% — i.e., on *pure spoken reasoning* the frontier native models now match or exceed the classic pipeline; [Step-Audio 2](https://arxiv.org/abs/2507.16632) (2025-07, verified) trains reasoning-centric RL + native tool calling (web/audio search) end-to-end. (ii) *Reward level:* the trained evaluator WavReward hits 91.5% objective accuracy where the prompted judge gets 53.4%. So the fine-tuned SOTA narrative is \"train the modality gap away\" — and on single-turn spoken reasoning it has visibly worked; but the *agentic* deficits measured in 2026 (tau-Voice 26-51% vs 85% text with 79-90% agent-driven failures; EchoChain <50% under interruption; FDB-v3 0.600 Pass@1) persist in exactly those newest realtime models, and the residual deficits (dialog-state under interruption, argument-value fidelity, agent-loop logical errors) are *unmeasured* for sampling/prompt-space headroom — the (a)/(b) fractions of the yardstick have literally never been computed here.

**The in-fence unoccupied cells (this lane's positioning claim).** (1) No pass@k / best-of-N / oracle-over-sampling number exists on any voice-agent benchmark — condition (a) unmeasured, exactly as the yardstick §6 predicted for Speech-Agentic (re-confirmed empty by the verifier, 2026-07-04). (2) No peer-reviewed APE/OPRO/GEPA-class prompt-optimization result on voice agents (H_prompt − H_fix: zero published quantification; only a non-peer-reviewed engineering demo exists, repo verified). (3) Condition (c) is *cheapest here of all families*: tau2-style DB-state rewards are verifiable ('success is deterministically evaluated by comparing the end state of the environment against a gold standard'), and From Text to Voice makes any annotated text tool benchmark a verifiable audio benchmark without re-annotation — the reward instrument pre-exists the selector research, unlike ASR where every deployable selector measured null. The text-domain recipe to transplant is now concrete: best-of-N over agent rollouts with list-wise verification gives ~+8pp on GAIA (arXiv 2506.12928), and on OSWorld behavior-level best-of-N ensembles pushed GUI agents past the human baseline (72.6% vs 72.36%) — both untransferred to voice.

**Closure fence (quoted, binding).** The agent-level question is CLOSED: \"The agent-level program this paper deferred is now closed under the frozen contract — by frozen procedure plus one genuine kill — rather than by scoping... the question is therefore closed, not merely deferred, unless re-open conditions r1–r3 obtain\" (2026-07-03 NO-GO decision §10; owner-ratified 2026-07-04 — consistent with the survey archive README). Re-open conditions verbatim (§9): **r1** — a public cross-session, same-speaker speech corpus appears; **r2** — a peer-reviewed non-separable decomposition bound appears; **r3** — a mechanism-lane kill is overturned by new literature. Everything in this lane is **single-session scaffolding** (in scope): all five problems are single-episode task deficiencies; the dialog-state problem (P3) is within-conversation state, not cross-session accumulation. No candidate here requires skills/memory accumulation across episodes; none collides with the closed question. tau2-bench-class envs also do NOT satisfy r1 (synthetic personas, no cross-session same-speaker audio corpus).

## Negative findings (verified-empty searches & P0 strikes — first-class results)

- N1 (verified empty; original 2 searches 2026-07-04 + independent verifier re-search 2026-07-04): no published pass@k / best-of-N / oracle-over-sampling measurement on any voice-agent benchmark (tau-Voice, FDB-v3, VoiceAgentBench, Audio2Tool, VoiceBench, EchoChain). tau-Voice explicitly reports only pass@1. Test-time-scaling-for-agents literature (BoN ~+8pp on GAIA, arXiv 2506.12928) is text-only; a fresh targeted search returned only the benchmarks themselves and engineering blogs. Condition (a) SUPPORT for speech-agentic is an unoccupied measurement cell — matching the yardstick §6 prediction 'likely unmeasured -> itself a named gap'.
- N2 (verified empty, 2026-07-04): no peer-reviewed APE/OPRO/GEPA-class prompt-optimization result on any voice-agent or spoken-instruction benchmark. Closest artifacts: a non-peer-reviewed Google-engineer sample repo (heiko-hotz/voice-assistant-prompt-optimization — verifier confirmed it exists, is explicitly a demo/educational project, archived 2025-08, APE over Gemini Live function calling with TTS-audio test suites) and DD-GEPA (arXiv 2606.07894, text dialogue disentanglement). H_prompt − H_fix for this family: zero published quantification.
- N3 (verified empty, 2026-07-04): no self-consistency / majority-vote selection result over ReAct-style voice-agent trajectories; even in the text origin domain, SC over open-ended agent trajectories is called 'underexplored' (RCAgent, arXiv 2310.16340), so the speech transfer has no origin-complete recipe to copy — the trajectory-aggregation gap is upstream of the modality.
- N4 (verified empty within session searches, 2026-07-04): no audio-native analog of Set-of-Mark prompting — no training-free scaffold that surfaces acoustic anchors (time-aligned events, speaker marks, spelled-out entity spans) as in-context tokens for a frozen omni model on agentic tasks; the only re-grounding scaffold in measured use is the full ASR cascade. (Absence-of-evidence grade, two-search depth.)
- N5 (closure-fence audit, not a search): no problem in this lane reduces to cross-session accumulating memory; all five problems are single-episode/single-session task deficiencies. The closed NO-GO question ('cross-session accumulating agent', 2026-07-03 decision recorded in the survey archive README, re-open only on r1: public cross-session same-speaker speech corpus; r2: peer-reviewed non-separable decomposition bound; r3: a mechanism-lane kill overturned by new literature) is not re-entered by any claim above; P3's dialog-state is within-conversation by construction.
- VERIFIER-AUDIT (2026-07-04, this pass): all 28 unique source URLs resolved and matched their citations; zero dead links, zero fabricated papers, zero P0 strikes (all 16 claims anchor to listed problem ids). Corrections applied rather than strikes: (1) C01 and C11 delta_vs_archive corrected new->update — tau-Voice and EchoChain already sit in the survey archive (D2-10 in 2026-07-03-step1-delta-speech-agent-memory.md, which names EchoChain's three failure patterns and tau-Voice's single-episode pass@1 design); only the result numbers are post-archive. (2) C07: '+7pp on GAIA' corrected to ~+8pp (paper reports an eight-point BoN improvement over baseline). (3) C08: 'up to 19pp' corrected to 'up to 20%' per GEPA v2 abstract. (4) VoiceBench cascade claim scoped to 'all open-source end-to-end models (>20 points)' — GPT-4o-Audio only slightly lags its pipeline counterpart. (5) From-Text-to-Voice 1.8-4.8-point gap scoped to Confetti. (6) AudioJudge MSE range tightened to ~1.8-3.5 (verified: TMHINTQ 3.46->1.80, SOMOS 3.31->2.81). (7) positioning_md Artificial Analysis numbers refreshed (GPT Realtime 83%, GPT-Realtime-2 High 97%, Gemini 2.5 native-audio thinking 91%, Qwen3.5 Omni Plus Realtime 99%) — the native-S2S catch-up on Big Bench Audio is further along than drafted, which strengthens the point that the remaining in-fence opportunity is agentic (tau-Voice-class), not single-turn spoken reasoning.