# Step-1 delta scan D2 — speech agent memory/skills; cross-session corpus re-check (r1)

> Step-1 rationality campaign lane · 2026-07-03 · workflow `wf_68e2556d-7a7` ·
> pre-registration: [[2026-07-03-agentic-tfrl-step1-preregistration]] @ freeze b19bff2. Ground rules: the 2026-07-02 verdict is the null hypothesis;
> claims tagged `delta_vs_archive` against the 17-file survey archive; every URL adversarially
> verified (0-hallucination bar). 

### D2-01 — [new] axis: a-change-q0 · bears on: M3, P1

FlowEdit (arXiv 2606.20518, submitted 2026-06-18) is a speech-native, training-free lifelong-memory existence proof: a FROZEN flow-matching TTS model is given a Modern Hopfield associative memory that stores pronunciation corrections as latent conditioning edits (token-level perturbations in text-embedding space; no weight updates), retrieved at inference via soft attention with a similarity gate; it reports 92.7% relative phoneme-error-rate reduction over zero-shot on a curated benchmark of 312 multilingual proper nouns (18 language families), with corrections persisting across inference sessions. Caveats: TTS pronunciation (not ASR), small benchmark, code/data release not confirmed, and 'latent conditioning edits' sit at the edge of the prompt-state fence (state lives in an external memory, weights untouched). Fast-follower signal on the archive's A4-12 open moat.

**Sources:** [FlowEdit: Associative Memory for Lifelong Pronunciation Adaptation in Flow-Matching TTS](https://arxiv.org/abs/2606.20518) (2026-06-18) · verified: True

### D2-02 — [new] axis: a-change-q0 · bears on: M3

IndicContextEval (arXiv 2606.19157, submitted 2026-06-17, accepted Interspeech 2026) is a new benchmark measuring exactly whether frozen audio LLMs USE injected context: a seven-level prompting framework (metadata, natural-language descriptions, entity lists in English and native script, and adversarial prompts with intentionally incorrect entities) over 56 hours of natural speech, 555 speakers, 8 Indic languages, 23 domains, across 5 models; it finds substantial cross-model differences in context-utilisation behaviour. This is a ready-made external template for M3's phase design (entity-list injection = memory injection; adversarial-wrong-entity condition = a poisoned-memory control).

**Sources:** [IndicContextEval: A Benchmark for Evaluating Context Utilisation in Audio Large Language Models Across 8 Indic Languages](https://arxiv.org/abs/2606.19157) (2026-06-17) · verified: True

### D2-03 — [new] axis: a-change-q0 · bears on: M3, P4

PROFASR-BENCH (arXiv 2512.23686, submitted 2025-12-29; dataset on HuggingFace prdeepakbabu/ProfASR-Bench, code on GitHub) is a context-conditioned ASR benchmark (finance/medical/legal/tech, entity-rich utterances, no-context / profile / domain+profile / oracle / adversarial prompt conditions) whose headline finding is a 'context-utilization gap': lightweight textual context produces little to no change in average WER even with ORACLE prompts, i.e. current ASR and audio-LLM systems (Whisper, Qwen-Omni) underutilize injected side information. This is risk evidence AGAINST M3's Phase-1 with-memory gain being large on frozen models (the injection channel exists but models may ignore it), while simultaneously confirming context-injection headroom is a recognized open problem.

**Sources:** [PROFASR-BENCH: A Benchmark for Context-Conditioned ASR in High-Stakes Professional Speech](https://arxiv.org/abs/2512.23686) (2025-12-29) · verified: True

### D2-04 — [new] axis: background · bears on: S1, U2

mem0's industry report 'State of AI Agent Memory 2026' (published 2026-07-02) names only TEXT benchmarks (LoCoMo, LongMemEval, BEAM) as the field's memory evaluations, while simultaneously shipping three dedicated VOICE integrations (ElevenLabs, LiveKit, Pipecat) with no corresponding voice-memory benchmark — i.e., as of 2026-07-02 the memory-systems industry itself evaluates cross-session memory exclusively on text, even for voice-agent deployments.

**Sources:** [AI Agent Memory 2026: Progress Benchmark Report Evaluations (mem0)](https://mem0.ai/blog/state-of-ai-agent-memory-2026) (2026-07-02) · verified: True

### D2-05 — [new] axis: background · bears on: S1

M3Exam (arXiv 2606.07402, submitted 2026-06-05) is a new CROSS-SESSION multimodal memory benchmark for realistic user-agent interactions (cross-modal grounding, cross-session reasoning, implicit-information inference), but its abstract mentions no audio or speech modality — the cross-session multimodal-memory frontier advanced in June 2026 without adding audio, leaving the speech gap (archive claims A1-23/A1-24) intact.

**Sources:** [M3Exam: Benchmarking Multimodal Memory for Realistic User-Agent Interactions](https://arxiv.org/abs/2606.07402) (2026-06-05) · verified: True

### D2-06 — [new] axis: background · bears on: S1

SMMBench (arXiv 2605.15710, submitted 2026-05-15) benchmarks source-distributed multimodal agent memory over 'conversations, profiles, screenshots, tables, images, and documents' (1,877 samples, 264 sources) — again with no audio/speech modality in the abstract; together with WorldMemArena (arXiv 2605.29341, 2026-05-28, vision+text, 400 multi-session tasks), the May-June 2026 wave of multimodal agent-memory benchmarks uniformly excludes speech.

**Sources:** [SMMBench: A Benchmark for Source-Distributed Multimodal Agent Memory](https://arxiv.org/abs/2605.15710) (2026-05-15) · [WorldMemArena: Evaluating Multimodal Agent Memory Through Action-World Interaction](https://arxiv.org/abs/2605.29341) (2026-05-28) · verified: True

### D2-07 — [new] axis: a-change-q0 · bears on: M3, S1

AFA (arXiv 2604.25022, submitted 2026-04-27) is the first found system entering the speaker-keyed-memory territory the 06/30 survey called an open moat (archive A4-12): voice-embedding speaker identification routes multi-user spoken dialogue to ISOLATED per-user memory stores, raising Persona Attribution Accuracy from 35.7% to 61.3% across five LLM backends. Caveats: its PAT dataset is SYNTHETIC (58,289 persona-grounded dialogue turns, 133 user profiles, 12 scenarios — not real same-speaker multi-session audio, so it does not satisfy r1/S1), and its best-performing configuration fine-tunes LLaMA-2-70B (that variant is outside the training-free fence); the routing+memory mechanism itself is frozen-model-compatible. Fast-follower signal on the moat.

**Sources:** [AFA: Identity-Aware Memory for Preventing Persona Confusion in Multi-User Dialogue](https://arxiv.org/abs/2604.25022) (2026-04-27) · verified: True

### D2-08 — [new] axis: b-estimate-R · bears on: M5

VARS — Vector-Adapted Retrieval Scoring (arXiv 2603.20939, submitted 2026-03-21) — demonstrates, in the TEXT domain, reward-driven cross-session memory-state accumulation on a FROZEN backbone: each user is represented by long-term and short-term vectors in a shared preference space, updated online from weak scalar reward feedback, which bias retrieval scoring over a structured preference memory — personalization without any per-user fine-tuning. This is a mechanism-level existence proof for M5's falsifiable question (no-gradient cross-session accumulation improving selection), with the fence nuance that the accumulated state is learned vectors rather than pure text/retrieval structures, and it is not speech.

**Sources:** [User Preference Modeling for Conversational LLM Agents: Weak Rewards from Retrieval-Augmented Interaction](https://arxiv.org/abs/2603.20939) (2026-03-21) · verified: True

### D2-09 — [new] axis: background · bears on: S1

RAIL (arXiv 2606.11260, submitted 2026-06-09), a CHC-psychometrics-grounded benchmark for large audio-language models, includes an auditory Memory dimension and reports (verified against the paper's results text) that models are weakest on non-speech audio memory — on Memory for Sound Patterns 'no model exceeds 60' — while speech-based short-term memory is near-ceiling for frontier models (Gemini reaching 100); but the memory tested is WITHIN-episode short-term recall (Memory Span / Working Memory over a single spoken stream), not cross-session — even the newest audio-LLM cognitive benchmarks do not touch cross-session memory.

**Sources:** [RAIL: Rethinking Auditory Intelligence in Large Audio-Language Models with a CHC-Grounded Benchmark](https://arxiv.org/abs/2606.11260) (2026-06-09) · verified: True

### D2-10 — [new] axis: background · bears on: S1

The new full-duplex/voice-agent benchmark wave since the archive freeze — EchoChain (arXiv 2604.16456, submitted 2026-04-08; state-update reasoning under interruptions, failure modes: contextual inertia, interruption amnesia, objective displacement) and the ICASSP 2026 HumDial full-duplex challenge (arXiv 2604.21406, 2026-04-23; dual-channel REAL human-recorded conversations) — contains no cross-session memory component; τ-Voice (arXiv 2603.13686, already in archive via the design synthesis) is likewise explicitly single-episode task completion (pass@1 over 278 tasks). The HumDial dual-channel human-recorded dataset is a new real-speech dialogue resource, but nothing indicates same-speaker multi-session structure.

**Sources:** [EchoChain: A Full-Duplex Benchmark for State-Update Reasoning Under Interruptions](https://arxiv.org/abs/2604.16456) (2026-04-08) · [Full-Duplex Interaction in Spoken Dialogue Systems: A Comprehensive Study from the ICASSP 2026 HumDial Challenge](https://arxiv.org/abs/2604.21406) (2026-04-23) · [τ-Voice: Benchmarking Full-Duplex Voice Agents on Real-World Domains](https://arxiv.org/abs/2603.13686) (2026-03-14) · verified: True

### D2-11 — [new] axis: background · bears on: S1

MSP-Podcast (corpus paper arXiv 2509.09791, 2025-09-11; corpus existing since ~2019) is the nearest PRE-EXISTING public-ish candidate to S1's corpus requirement: 400+ hours of naturalistic, emotion-annotated (primary/secondary categories + valence/arousal/dominance, >=5 raters) speech with speaker identification for most samples. However, the paper does not document same-speaker CROSS-SESSION structure (temporally separated recordings per speaker), access is via a free institution-signed academic license agreement rather than open download (per the MSP lab distribution page), and no SV-EER admission-band validation exists — so it does not, on current evidence, satisfy r1/S1; it was simply never adjudicated on 7/02 (the deep review checked only the 28 frozen datasets).

**Sources:** [The MSP-Podcast Corpus](https://arxiv.org/abs/2509.09791) (2025-09-11) · [MSP-Podcast corpus — Multimodal Speech Processing (MSP) Laboratory (academic-license access page)](https://www.lab-msp.com/MSP/MSP-Podcast.html) · verified: True

## Negative findings (verified empty searches — decision-relevant)

- r1 NOT MET as of 2026-07-03: across 12 web searches (cross-session same-speaker speech corpus/benchmark; multi-session spoken dialogue dataset; audio long-term memory benchmark; 'across sessions' voice agent memory; longitudinal same-speaker emotional corpus releases incl. Interspeech 2026 sweep; HuggingFace multi-session spoken conversation datasets), NO public cross-session, same-speaker, multi-session SPEECH corpus or benchmark was found to have appeared. The closest new items (AFA's PAT dataset, HumDial dual-channel dialogues, the MM-Lifelong day/week/month video dataset arXiv 2603.05484) are respectively synthetic, single-session, and video-centric.
- No spoken/TTS-audio version of LoCoMo, LongMemEval, or any other multi-session conversational-memory benchmark was found (targeted search for speech/TTS variants of these benchmarks came up empty; the mem0 07/02 industry report still lists only text benchmarks).
- No speech-native self-improving agent (Reflexion/Voyager-style frozen-model skill/memory accumulation across episodes) found in post-2026-06-26 literature: the 2026 self-evolving skill-library wave (SAGE 2512.17102, OpenSkill 2606.06741, SkillForge 2604.08618, SkillAudit 2606.14239, MemSkill, Evo-Memory 2511.20857) remains text/code/embodied — archive claim A4-12 (open moat) still stands, though AFA (D2-07) shows adjacent territory being entered.
- All 2026 multimodal agent-memory benchmarks checked (M3Exam 2606.07402, SMMBench 2605.15710, WorldMemArena 2605.29341, plus archived Mem-Gallery/Omni-SimpleMem) exclude audio/speech modalities — archive claims A1-23/A1-24 (multimodal memory frontier is vision+text; no audio cross-session paralinguistically-keyed benchmark) remain true as of 2026-07-03 (verifier re-confirmed the four 2026 benchmark abstracts individually).
- No benchmark named in the 'SpeechMem/VoiceMem/AudioMem' pattern exists on arXiv; search returned only within-episode audio benchmarks (RAIL's short-term auditory memory, Audio MultiChallenge's 3-8-turn memory).
- New full-duplex and voice-assistant benchmarks since the 06/30 archive (τ-Voice, EchoChain, HumDial ICASSP 2026 challenge, EVA-Bench) all evaluate single-episode capability; none contains a cross-session memory component.
- Cross-session dialogue-memory benchmarks that DID newly appear (EvolMem 2601.03543, MemoryArena 2602.16313, PersonaMem-v2 2512.06688, MedMemoryBench 2605.11814, EvoMemBench 2605.18421) are text-based per their abstracts — no audio mentioned in any.
- LOGIC (arXiv 2601.15397), the one found decode-time (logit-space) contextual-biasing method for speech LLMs claiming 9% relative entity-WER reduction without prompting, was WITHDRAWN by its author on 2026-02-04 for institutional-approval reasons — it cannot be cited as standing evidence.
- Verifier note: the MSP-Podcast arXiv abstract alone does NOT document license terms or cross-session structure; the license-agreement access mode had to be sourced separately from the MSP lab distribution page (added as a second source on D2-11), and no evidence of same-speaker temporally-separated session metadata was found in either source.