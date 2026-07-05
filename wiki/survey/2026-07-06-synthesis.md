---
title: "Stage-1 Survey Synthesis + Claim Ledger — training-free frozen-omni agentic systems (14-lane sweep, 2026-07-06)"
date: 2026-07-06
stage: 1-argumentation
role: synthesis
---

# Synthesis: does a usage-pattern over ONE frozen omni model ever cross a verifiable capability boundary?

This document synthesizes the fourteen Stage-1 survey lanes dated 2026-07-06
(`duplex-realtime`, `xdomain-vlm-gui`, `verification-reward`, `voice-cascade`,
`eval-benchmarks-ondisk`, `s2s-native-open`, `memory-components`, `knowledge-backbone`,
`s2s-proprietary`, `tools-skills-harness`, `eval-methodology`, `planning-control`,
`eval-benchmarks-field`, `perception-delta`). All lanes were verifier-passed; per-lane URL and
number checks live in each lane file and are not re-derived here.

**Organizing framework under test.** Every system is scored on three axes —
**element** (a genuinely new information source: a different model, a trained module, a
tool/knowledge/memory connector) vs **usage-pattern** (a role/prompt/orchestration/routing move
over *one* frozen model, which reads out but cannot exceed that model's own oracle ceiling) vs
**constraint** (a base-architecture / inference-substrate property — real-time/full-duplex,
perception fidelity, context/token budget, safety/alignment — not reachable by prompting). The
central Stage-1 question: **does any usage-pattern-only lever cross a hard, verifiable capability
boundary on a frozen model?** The answer, across 14 lanes, is **no** (see §3).

**Delta convention.** Prior archive tags used throughout: **S1** = `2026-06-30-agent-level-synthesis`,
**S2** = `2026-06-30-agent-memory-skills-design` / `2026-06-30-survey-agent-memory`, **L4** =
`2026-07-04-stage1-L4-speech-agentic` (P1–P5, N1–N5), **X2** = `2026-07-04-stage1-X2-paralinguistic-delta`,
**X3** = `2026-07-04-stage1-X3-llm-vlm-testtime-map`.

---

## 1. Claim ledger

Columns: **system/method** · **recognized problem** · **origin-domain** · **training-free?** ·
**axis + verdict** · **fence** · **omni-role** · **url/id**. `TF` = training-free under the strict
"no weight AND no structure change over one frozen system" bar (a frozen *backbone* with a trained
bolt-on is **not** TF). Cross-lane duplicates are consolidated to one row.

### A. Full-duplex / turn-taking systems & bolt-on control modules (lane: duplex-realtime, +cascade/eval)

| system/method | problem | origin | TF? | axis + verdict | fence | omni-role | id |
|---|---|---|---|---|---|---|---|
| Moshi | cascade can't be full-duplex | speech(LLM root) | no (retrained) | constraint — CONFIRMS | single | hybrid | [2410.00037](https://arxiv.org/abs/2410.00037) |
| dGSLM | textless 2-channel dialogue | speech | no | constraint | single | hybrid | [2203.16502](https://arxiv.org/abs/2203.16502) |
| LSLM | interrupt mid-generation | speech | no (per-layer fusion) | constraint | single | hybrid | [2408.02622](https://arxiv.org/abs/2408.02622) |
| SyncLLM | text LLM has no time sense | LLM→speech (ported) | no | constraint — prompt-a-frozen-LLM-into-duplex fails | single | brain→hybrid | [2409.15594](https://arxiv.org/abs/2409.15594) |
| Freeze-Omni | add duplex w/o retraining LLM | speech (ported) | **no** (frozen LLM + trained classifier head/adapters) | constraint (system-level) — "frozen LLM" ≠ frozen system | single | explicit split | [2411.00774](https://arxiv.org/abs/2411.00774) |
| OmniFlatten | text LLM → duplex via flattening | LLM (ported) | no (weights change, no new struct) | constraint (weight-level) — separates "no new structure" from "no weight change" | single | hybrid | [2410.17799](https://arxiv.org/abs/2410.17799) |
| VITA-1.5 | GPT-4o-style vision+speech realtime | VLM→speech | no | constraint | single | hybrid | [2501.01957](https://arxiv.org/abs/2501.01957) |
| VITA-Audio (MCTP) | first-token latency | speech (ported spec-decode) | no (new trained heads) | constraint — latency baked into element, not TF decode trick | single | hybrid | [2505.03739](https://arxiv.org/abs/2505.03739) |
| Mini-Omni2 | open GPT-4o omni + interruption | speech | no | constraint | single | hybrid | [2410.11190](https://arxiv.org/abs/2410.11190) |
| **FlexDuo** | decouple duplex *control* from backbone | speech (ported) | no (trained 3-state module, frozen backbone) | **element (boundary case)** — turn-policy is separable/modular; −24.9% false interrupts | single | sensor/controller | [2502.13472](https://arxiv.org/abs/2502.13472) |
| **SoulX-Duplug** | plug-in semantic-VAD state predictor | speech | no (0.6B trained module, frozen backbone) | **element** — crossing came from a new trained connector | single | sensor | [2603.14877](https://arxiv.org/abs/2603.14877) |
| TurnGuide | dialogue quality within duplex | speech (ported inner-monologue) | plausible TF (unconfirmed) | usage-pattern-like refinement *assuming* a duplex base already paid | single | hybrid | [2508.07375](https://arxiv.org/abs/2508.07375) |
| TEN Turn Detection | endpointing beyond VAD | speech | no (Qwen2.5-7B fine-tune) | element — 90.6% vs 71.6% accuracy | single | sensor | [HF](https://huggingface.co/TEN-framework/TEN_Turn_Detection) |

### B. Native open end-to-end S2S / omni models (lane: s2s-native-open)

| system/method | problem | origin | TF? | axis + verdict | fence | omni-role | id |
|---|---|---|---|---|---|---|---|
| **Kyutai Unmute** | Moshi can't function-call | speech I/O + text-LLM brain | no (STT/TTS trained; glue) | **element** — tool-use gap closed by a real connector, not a prompt | single | sensor+actuator / swappable brain | [kyutai.org/unmute](https://kyutai.org/unmute/) |
| GLM-4-Voice | preserve intelligence + add speech | LLM (continual pretrain) | no | element (new weights) | single | hybrid | [2412.02612](https://arxiv.org/abs/2412.02612) |
| LLaMA-Omni2 | cheap SpeechLM, reuse strong LLM | LLM+speech | no (stage-I FT, then frozen) | element — reuse of an existing element beats brute-scale (S2 parallel) | single | explicit split | [2505.02625](https://arxiv.org/abs/2505.02625) |
| Step-Audio 2 | fused audio LM + reduce hallucination | speech | no (SFT+RL) | element (LM) + element (RAG/web-search fixes hallucination) | single | hybrid + external sensor | [2507.16632](https://arxiv.org/abs/2507.16632) |
| **Step-Audio-R1 / R1.5** | does CoT help on audio? | speech | no (RLVR/RLHF) | **negative for usage-pattern** — CoT *hurts* audio; only weight-level RL fixed it | single | hybrid | [2511.15848](https://arxiv.org/abs/2511.15848) · [2604.25719](https://arxiv.org/abs/2604.25719) |
| Qwen2.5-/Qwen3-Omni | unify perception + streaming speech | LLM/VLM | no | element; explicit Thinker(brain)/Talker(actuator) split, tool-call seam; 1.8pt voice tax | single | explicit split | [2503.20215](https://arxiv.org/abs/2503.20215) · [2509.17765](https://arxiv.org/abs/2509.17765) |
| Kimi-Audio | unify audio understand/gen at scale | LLM (Qwen2.5-7B) | no (continual pretrain) | element | single | explicit split | [2504.18425](https://arxiv.org/abs/2504.18425) |
| MiniCPM-o 4.5 | realtime full-duplex omni, compact | VLM+speech | no (E2E FT) | element; cleanest sensor/sensor/brain/actuator naming | single | explicit split | [2604.27393](https://arxiv.org/abs/2604.27393) |
| Baichuan-Audio | unified real-time speech interaction | speech | no | element | single | hybrid | [2502.17239](https://arxiv.org/abs/2502.17239) |
| SLAM-Omni | cheap timbre-controllable voice | speech | no (15 GPU-h) | element; content/speaker disentangle via *architecture* — W4 baseline | single | hybrid | [2412.15649](https://arxiv.org/abs/2412.15649) |
| Ola | image/text LLM → audio/video | VLM (ported curriculum) | no | element; progressive-alignment curriculum ported from VLM | single | hybrid | [2502.04328](https://arxiv.org/abs/2502.04328) |

### C. Proprietary S2S / realtime stacks (lane: s2s-proprietary)

| system/method | problem | origin | TF? | axis + verdict | fence | omni-role | id |
|---|---|---|---|---|---|---|---|
| OpenAI gpt-realtime | replace cascade Standard Voice | LLM (GPT-4o) | no (base) | element — gain = audio-centric pretraining, not orchestration | n/a | hybrid | [blog](https://openai.com/index/introducing-gpt-realtime/) |
| OpenAI Realtime + remote MCP | live external tool access | LLM (ported MCP) | TF (runtime config) | **element (connector)** — cleanest vendor proof of thesis | single | hybrid | [docs](https://developers.openai.com/api/docs/guides/realtime-mcp) |
| OpenAI Realtime memory | cross-session continuity | LLM (RAG-style) | TF | element — but developer API is **stateless** (60-min cap); persistent memory only in consumer ChatGPT | single API / cross-session product | n/a | [C3](https://help.openai.com/en/articles/8590148-memory-faq) |
| OpenAI safety classifier | police live audio | LLM (moderation) | TF (separate weights) | element — decorrelated verifier-as-tool | n/a | sensor-like | [docs](https://developers.openai.com/api/docs/guides/safety-best-practices) |
| Gemini Live (native audio) | cascade latency + grounding | LLM/VLM (+ported tools) | no base / TF tool layer | element — Search + code-exec chained | single | hybrid | [docs](https://ai.google.dev/gemini-api/docs/live-guide) |
| Gemini Live context compression | "infinite" sessions | LLM (sliding-window) | TF | **usage-pattern** — discards/compresses info; manages a constraint, crosses nothing | session-only | n/a | [C6](https://ai.google.dev/gemini-api/docs/live-session) |
| Realtime token-budget vs stream | duplex rate limit | speech | n/a | **constraint** — ~85 min @128k tokens; 60-min wall-clock | n/a | n/a | C6b |
| xAI Grok Voice Agent | in-house native stack | speech | no base / TF tools | element (tools); weakest architecture disclosure | single (30-min cache) | hybrid | [docs](https://docs.x.ai/developers/model-capabilities/audio/voice-agent) |
| Amazon Nova (2) Sonic | unified single model + tools | speech | no base / TF tools | element (RAG/function-call); async dispatch = usage-pattern | single | hybrid | [blog](https://aws.amazon.com/blogs/aws/introducing-amazon-nova-sonic-human-like-voice-conversations-for-generative-ai-applications/) |
| Microsoft Copilot Voice / MAI | ASR+LLM+TTS named separately | speech | no | **unclear disclosure** — only vendor not confirming native S2S | n/a | sensor + output | [MAI](https://microsoft.ai/news/mai-voice-2/) |

### D. Cascade / orchestration frameworks (lane: voice-cascade)

| system/method | problem | origin | TF? | axis + verdict | fence | omni-role | id |
|---|---|---|---|---|---|---|---|
| Pipecat / LiveKit / Vocode / TEN | wire STT→LLM→TTS realtime | speech (+ported MCP) | TF | **usage-pattern** — orchestration is commodity plumbing; capability = plugged-in element | single | n/a / hybrid | [pipecat](https://github.com/pipecat-ai/pipecat) |
| LiveKit sequential-pipeline latency | 5-stage cascade cost | speech | n/a | constraint — total ≈ `max(stages)` under streaming | n/a | n/a | [blog](https://livekit.com/blog/sequential-pipeline-architecture-voice-agents) |
| VoiceAgentRAG | RAG latency breaks flow | LLM (ported) | TF | usage-pattern (dual-agent) + **element (prefetch cache)** — gain is the cache | single | n/a | [2603.02206](https://arxiv.org/abs/2603.02206) |
| From Text to Voice | cascade-vs-native gap | LLM (ported) | TF eval | **element-attributable** — REFUTES naive "cascade worse"; gap = ASR-element fidelity | single | hybrid | [2605.15104](https://arxiv.org/abs/2605.15104) |
| X-Talk (position paper) | modular case for S2S | speech | mixed | element — CONFIRMS; capability from swappable specialist elements | single | n/a | [2512.18706](https://arxiv.org/abs/2512.18706) |
| Enterprise Realtime Voice Agents | reproducible cascade recipe | speech | TF | constraint (deployability) — 755ms TTFA; rejects self-hosted Qwen3-Omni | single | n/a | [2603.05413](https://arxiv.org/abs/2603.05413) |
| Retell / Vapi / Bland | package cascade for non-ML teams | speech | TF | usage-pattern — variance bounded to latency/UX, not capability | single | sensor+actuator | [blog](https://www.retellai.com/blog/retell-vs-bland-vs-vapi-vs-elevenlabs) |

### E. Verification / reward / judge methods (lane: verification-reward, +eval-methodology)

| system/method | problem | origin | TF? | axis + verdict | fence | omni-role | id |
|---|---|---|---|---|---|---|---|
| WavReward | no S2S reward model | LLM (ported) | no (trained RM) | element — 53.4%→91.5% objective acc (CONFIRMS L4-P5) | single | hybrid | [2505.09558](https://arxiv.org/abs/2505.09558) |
| AudioJudge | training-free audio judging | LLM (ported) | TF | **usage-pattern/read-out** — inherits verbosity/position bias | single | hybrid | [2507.12705](https://arxiv.org/abs/2507.12705) |
| SpeechJudge | zero-shot audio naturalness judge | LLM (ported) | TF baseline | usage-pattern/read-out — <70% human agreement (insufficient) | single | hybrid | [2511.07931](https://arxiv.org/abs/2511.07931) |
| SQ-LLM / AnyAudio-Judge / Dual-Axis GRM | reliable speech judges | LLM (ported) | no (trained) | element/new-info — every reliable judge is a trained element | single | hybrid | [2510.14664](https://arxiv.org/abs/2510.14664) · [2606.03116](https://arxiv.org/abs/2606.03116) · [2604.14920](https://arxiv.org/abs/2604.14920) |
| τ-Voice / τ²-bench (DB-state) | verifiable agentic tool-use | LLM/agentic | TF eval | **element (symbolic verifier-as-tool)** — ~100% reliable by construction | single | n/a | [2603.13686](https://arxiv.org/abs/2603.13686) · [2506.07982](https://arxiv.org/abs/2506.07982) |
| τ²-bench pass^k | reliability of repeated sampling | LLM/agentic | TF | **usage-pattern/read-out** — 90%→57% (retail); resampling exposes inconsistency, adds no info | single | n/a | [2506.07982](https://arxiv.org/abs/2506.07982) |
| Delay/Plateau/Collapse | verifier-noise → RL dynamics | LLM/agentic | n/a | **constraint** — reward-estimation-error bound (feeds theory-track convergence) | n/a | n/a | [2605.02909](https://arxiv.org/abs/2605.02909) |
| GenRM | trained verifier vs prompted judge | LLM (root) | no | element — beats LLM-as-judge by 16–40% (element > usage-pattern) | single | n/a | [2408.15240](https://arxiv.org/abs/2408.15240) |
| Self-Certainty BoN | reward-free BoN signal | LLM | TF | usage-pattern/read-out — approaches, not shown to exceed, an external RM | single | n/a | [2502.18581](https://arxiv.org/abs/2502.18581) |
| Self-Preference Bias / Cannot-Self-Correct | same-weights judging is confounded / fails | LLM (root) | TF | usage-pattern/read-out — genealogy roots of the thesis negative | single | n/a | [2410.21819](https://arxiv.org/abs/2410.21819) · [2310.01798](https://arxiv.org/abs/2310.01798) |
| **Self-check ASR correction** | LLM ASR-correction over-hallucinates | LLM (ported) | **TF** | **usage-pattern/read-out — requires-nuance (STRONGEST CANDIDATE)** — real 9–21% CER/WER gains but vs a naive baseline, no oracle-ceiling control → likely reads out the model's own ceiling; Stage-2 re-test parked | single | brain | [2505.24347](https://arxiv.org/abs/2505.24347) |
| SDiaReward / ESDR-Bench | spoken-dialogue reward model | LLM (ported) | no (trained RM) | element/new-info — but only benchmarked on preference acc, not deployed in best-of-N | single | hybrid | [2603.14889](https://arxiv.org/abs/2603.14889) |
| Talking Turns | turn-taking judge | speech | no (trained classifier) | element (verifier-as-tool) | single | n/a | [2503.01174](https://arxiv.org/abs/2503.01174) |

### F. Memory / knowledge / RAG components (lanes: memory-components, knowledge-backbone)

| system/method | problem | origin | TF? | axis + verdict | fence | omni-role | id |
|---|---|---|---|---|---|---|---|
| Mem0 / Letta / Zep / A-MEM / LangMem / O-Mem / Mem-PAL | cross-session persistence | LLM | TF | element (persistent store); reflection/router = usage-pattern | cross-session | n/a | [2504.19413](https://arxiv.org/abs/2504.19413) etc |
| Generative Agents / Reflexion | reflect-and-store | LLM (roots) | TF | element (persistence) / **usage-pattern (reflection)** — reflection gain only on soft LLM/human believability, not a verifiable ceiling | cross-session | n/a | [2304.03442](https://arxiv.org/abs/2304.03442) · [2303.11366](https://arxiv.org/abs/2303.11366) |
| **Memory-R1** | can the memory-manager role be improved? | LLM | **no (PPO/GRPO)** | **weight-updated role beats the identical prompted role** (+28% F1) — direct thesis confirmation | cross-session | n/a | [2508.19828](https://arxiv.org/abs/2508.19828) |
| WavRAG / MoshiRAG / VoxRAG | audio-native RAG | speech | mixed | element (static KB), **not** cross-session personal memory | single | hybrid | [2502.14727](https://arxiv.org/abs/2502.14727) · [2604.12928](https://arxiv.org/abs/2604.12928) · [2505.17326](https://arxiv.org/abs/2505.17326) |
| AFA | multi-user persona confusion | speech(routing)/text(memory) | mixed (best config FT) | element — closest audio-*keyed* memory, but keys route to **text** objects; synthetic data | cross-session (synthetic) | hybrid | [2604.25022](https://arxiv.org/abs/2604.25022) |
| **CB-RAG** | ASR mistranscribes rare terms | LLM (ported) | **TF** | **element/new-info — the clean training-free positive** (frozen ASR + retrieval, ≤17% WER↓) | single | n/a (ASR) | [2509.19567](https://arxiv.org/abs/2509.19567) |
| MARS / RASST | speech-RAG needing FT to consume element | LLM (ported) | no (LoRA/FT) | element exists, but speech-LLMs need weight change to *use* it well | single | hybrid | [2508.01166](https://arxiv.org/abs/2508.01166) · [2601.22777](https://arxiv.org/abs/2601.22777) |
| Stop Overvaluing MAD | is debate gain real? | LLM | TF | **usage-pattern (homogeneous debate) = read-out**; heterogeneous (different model) = element | single | n/a | [2502.08788](https://arxiv.org/abs/2502.08788) |
| Don't-Pick-Highest / InferenceDynamics / FusionFactory | multi-model ensemble/routing | LLM | TF (routing) | routing = usage-pattern; the *distinct model* it selects = element | single/cross | n/a | [2602.08003](https://arxiv.org/abs/2602.08003) · [2505.16303](https://arxiv.org/abs/2505.16303) · [2507.10540](https://arxiv.org/abs/2507.10540) |
| KARMA / Youtu-GraphRAG | frozen-LLM KG enrichment | LLM | TF | element (external corpus/graph); 9-role structure = usage-pattern over one frozen model | cross-session | n/a | [2502.06472](https://arxiv.org/abs/2502.06472) · [2508.19855](https://arxiv.org/abs/2508.19855) |
| KCR / FuseChat | conflict reconciliation / "knowledge fusion" | LLM | **no (RLVR / weight-merge)** | negative — field's default answer is retraining; "knowledge fusion" = weight merging (terminology trap) | single | n/a | [2508.01273](https://arxiv.org/abs/2508.01273) · [2408.07990](https://arxiv.org/abs/2408.07990) |
| VoxMind | agentic omni still needs SFT + aux model | speech | no (SFT) | negative — most recent agentic omni crosses knowledge boundary via SFT, not TF orchestration | single | hybrid | [2604.15710](https://arxiv.org/abs/2604.15710) |

### G. Cross-domain VLM / GUI transfer references (lane: xdomain-vlm-gui)

| system/method | problem | origin | TF? | axis + verdict | fence | omni-role | id |
|---|---|---|---|---|---|---|---|
| AppAgent / AWM / VerificAgent | persistent skill/workflow/memory-audit | VLM/web | TF | element (connector) — transfer candidates for a voice skill/workflow store | cross-session | n/a | [2408.11824](https://arxiv.org/abs/2408.11824) · [2409.07429](https://arxiv.org/abs/2409.07429) · [2506.02539](https://arxiv.org/abs/2506.02539) |
| GTA1 / Visual Confused Deputy | test-time action selection / grounding veto | VLM | mixed | element (separate judge/classifier) — working defense is verifier-as-tool, not verifier-as-role | single | n/a | [2507.05791](https://arxiv.org/abs/2507.05791) · [2603.14707](https://arxiv.org/abs/2603.14707) |
| **RegionFocus** | dense-UI grounding on frozen VLM | VLM | **TF** | **ambiguous — input-transformation element, not pure re-query** — zoom injects new higher-res visual info (+28%/+24%); supports thesis under its own logic | single | sensor-side | [2505.00684](https://arxiv.org/abs/2505.00684) |
| Naive Visual Memory / Honest Lying | does added memory / self-reflection help? | VLM/LLM | TF | element-with-negative / **usage-pattern that actively degrades** (confabulation compounds) | single/cross | n/a | [2606.14106](https://arxiv.org/abs/2606.14106) · [2605.29463](https://arxiv.org/abs/2605.29463) |
| OSWorld / UI-TARS-2 / Illusion-of-Progress | execution-based eval / FT SOTA / over-optimism | VLM | n/a / FT | methodology confirms verifiable-reward > model-judge; SOTA jumps = FT elements; reported gains contested | n/a | n/a | [2404.07972](https://arxiv.org/abs/2404.07972) · [2509.02544](https://arxiv.org/abs/2509.02544) · [2504.01382](https://arxiv.org/abs/2504.01382) |

### H. Planning / multi-agent / debate (lane: planning-control, +tools)

| system/method | problem | origin | TF? | axis + verdict | fence | omni-role | id |
|---|---|---|---|---|---|---|---|
| AURA | speech agent w/ real tools | LLM (ported ReAct) | TF | element (calendar/email/search tools); **no non-agentic ablation** — ReAct-vs-tools unquantified | single | hybrid | [2506.23049](https://arxiv.org/abs/2506.23049) |
| VoxMind / OmniAtlas | boundary crossing in voice agents | speech/omni | no (SFT/DPO) | large gains (+39.7pp / +7.5pp) require fine-tuning, not orchestration | single | brain | [2604.15710](https://arxiv.org/abs/2604.15710) · [2602.22897](https://arxiv.org/abs/2602.22897) |
| Full-Duplex-Bench-v3 | tool-use under disfluency | speech | TF eval | cascaded text-LLM controller wins **only Easy**; capped by ASR-finalization **constraint** (+decorrelated Whisper element) | single | hybrid | [2604.04847](https://arxiv.org/abs/2604.04847) |
| LongShOTAgent / ThinkOmni | "training-free" omni agents | omni | TF orchestration | **element-decomposed** — gains trace to a 2nd model / retrieval / expert models, not usage-pattern alone | single | hybrid | [2512.16978](https://arxiv.org/abs/2512.16978) · [2602.23306](https://arxiv.org/abs/2602.23306) |
| Homogeneous MAD / Debate-or-Vote | does same-weights debate help? | LLM | TF | **usage-pattern — does NOT cross**; martingale proof debate can't improve expected correctness; majority voting explains most "MAD gains" | single | n/a | [2605.00914](https://arxiv.org/abs/2605.00914) · [2508.17536](https://arxiv.org/abs/2508.17536) |
| AudioToolAgent | LALMs lack tool-calling | speech+LLM | TF | **element (verifier/coordinator-as-tool)** — text-only coordinator never touches audio; SOTA 77.5 MMAU | single | sensor | [2510.02995](https://arxiv.org/abs/2510.02995) |

### I. Tools / skills / harness & the paralinguistic-delta systems (lanes: tools-skills-harness, perception-delta)

| system/method | problem | origin | TF? | axis + verdict | fence | omni-role | id |
|---|---|---|---|---|---|---|---|
| VoiceAgentBench | agentic voice tool-calling | speech | TF eval | **element** — decorrelated ASR-LLM cascade beats one frozen SpeechLM (up to 60.6%) | single | hybrid | [2510.07978](https://arxiv.org/abs/2510.07978) |
| Audio2Tool | compositional speech tool-calling | speech | TF eval | element gated by constraint — 92.4%→41.7% across tiers; element availability ≠ crossing | single | hybrid | [2604.22821](https://arxiv.org/abs/2604.22821) |
| Stream RAG / SAGE | streaming tool-timing / skill-library reward | speech / GUI | **no (FT/GRPO)** | practitioners judged TF insufficient → fine-tuned; SAGE = S2's reward gate as a *training* signal | single/cross | hybrid/n/a | [2510.02044](https://arxiv.org/abs/2510.02044) · [2512.17102](https://arxiv.org/abs/2512.17102) |
| MCP-for-voice / Agent Skills (SKILL.md) | standard tool/skill formats | LLM | TF | element (connector format) — but **not yet ported to a deployed voice runtime**; MCP still text-transcript-mediated | single/cross | n/a | [2511-25 spec](https://modelcontextprotocol.io/specification/2025-11-25) |
| IHBench | resume a workflow after interruption | speech | TF eval | **usage-pattern/read-out** — declared workflow does not confer interruption-recovery | single | hybrid | [2606.19595](https://arxiv.org/abs/2606.19595) |
| CP-Bench | contextual vs direct paralinguistic reasoning | speech | TF eval | element load-bearing for *contextual* (67–69% vs 51–56% cascade), weak for *direct* recognition (~30%) | single | hybrid | [2509.16589](https://arxiv.org/abs/2509.16589) |
| Cascade Equivalence Hypothesis | is E2E > cascade tested? | speech | TF (probing) | constraint — E2E ≈ cascade by default; **worse under noise** (advantage reverses up to 7.6pp @0dB); "training objectives, not architectures, are the bottleneck" | single | hybrid→degenerate | [2602.17598](https://arxiv.org/abs/2602.17598) |
| S2S-Arena / Just-ASR+LLM? | does raw-audio access pay off? | speech | TF eval | negative — cascades often beat E2E on paralinguistic instruction-following; −15/−19pp on identity-critical Qs | single | hybrid | [2503.05085](https://arxiv.org/abs/2503.05085) · [2409.04927](https://arxiv.org/abs/2409.04927) |
| ParalinGPT / ParaS2S / X-Talk / EmotionThinker / Dual-Info-SLM / Resurfacing-Paralinguistic | beyond-transcript wins | speech | no (adapter/RL/FT) | element — **every confirmed >transcript win required a trained component** | single | hybrid/split | [2312.15316](https://arxiv.org/abs/2312.15316) · [2511.08723](https://arxiv.org/abs/2511.08723) · [2512.18706](https://arxiv.org/abs/2512.18706) · [2508.08095](https://arxiv.org/abs/2508.08095) · [2603.11947](https://arxiv.org/abs/2603.11947) |
| **Reflecting Twice (empathy)** | reason about emotion before replying | speech | **TF (inference-time)** | **unresolved** — "reflect twice" over one frozen model; is it same-model re-reasoning (counterexample) or an implicit label-extraction element? controls unconfirmed | single | hybrid | [2601.18281](https://arxiv.org/abs/2601.18281) |
| Talker-Reasoner / ConvFill | fast Talker + slow Reasoner | LLM→speech | mixed | **off-target** for the frozen-model fork — Talker & Reasoner are *disjoint* models (not one backbone, two roles) | single | hybrid | [2410.08328](https://arxiv.org/abs/2410.08328) · [2511.07397](https://arxiv.org/abs/2511.07397) |

### J. Benchmarks & eval instruments (lanes: eval-benchmarks-ondisk, eval-benchmarks-field, eval-methodology)

| benchmark | measures | verifier type | pass@k? | human topline | on-disk | id |
|---|---|---|---|---|---|---|
| τ²-bench / τ-Voice | verifiable tool-use, voice gap | DB-state (tool) + LLM-judge (user/content) | pass^k (text) / **pass@1 only (voice)** | — | yes | [2506.07982](https://arxiv.org/abs/2506.07982) · [2603.13686](https://arxiv.org/abs/2603.13686) |
| **EVA-Bench** | task-success + experience | SHA-256 DB hash (tool) + LLM/LALM-judge | **pass@1/pass@k/pass^k measured** (k=5/k=3); 0.44 median gap; prompts NOT optimized | — | yes (ServiceNow-AI/eva) | [2605.13841](https://arxiv.org/abs/2605.13841) |
| VoiceBench / VocalBench / URO-Bench | multi-task voice assistant | exact-match/rule (tool) + GPT-judge (role) | no | — | yes | [2410.17196](https://arxiv.org/abs/2410.17196) · [2505.15727](https://arxiv.org/abs/2505.15727) · [2502.17810](https://arxiv.org/abs/2502.17810) |
| AudioMC | multi-turn retention | 1,712 rubrics (hybrid) | no | — | yes | [2512.14865](https://arxiv.org/abs/2512.14865) |
| VoiceAssistant-Eval | listen/speak/view + safety | UTMOS/WER (tool) + LLM-judge | no | — | yes | [2509.22651](https://arxiv.org/abs/2509.22651) |
| SoulX-Duplug-Eval | duplex turn-taking | scenario metrics | no | — | yes | [2603.14877](https://arxiv.org/abs/2603.14877) |
| EchoChain | state-update under interruption | deterministic vs half-duplex control | no | — | no | [2604.16456](https://arxiv.org/abs/2604.16456) |
| MMAU-Pro | auditory general intelligence | accuracy | no | **77.9% (18.7pp gap)** — the field's only quantified human topline | no | [2508.13992](https://arxiv.org/abs/2508.13992) |
| SpeechR / MMAR / ADU-Bench / SD-Eval | speech reasoning / perception fidelity | MCQ + LLM-judge | no | — (mostly) | no | [2508.02018](https://arxiv.org/abs/2508.02018) · [2505.13032](https://arxiv.org/abs/2505.13032) |
| AJailBench / JALMBench / Jailbreak-AudioBench | safety under audio attack | attack-success rate | no | — | no | [2505.15406](https://arxiv.org/abs/2505.15406) · [2505.17568](https://arxiv.org/abs/2505.17568) |

---

## 2. The sensor-vs-brain landscape of 2025+ systems

**Two build strategies, and every system is one or the other** (s2s-native-open synthesis):

1. **Fuse-and-retrain (hybrid role).** Continue-pretrain or fully fine-tune one weight set so the
   *same* weights reason and emit audio (Moshi, GLM-4-Voice, Kimi-Audio, Qwen2.5-/Qwen3-Omni,
   MiniCPM-o, Baichuan-Audio, Step-Audio 2, Ola; **all proprietary vendors** claim this). The omni
   model is **hybrid** = sensor+brain+actuator in one artifact; the whole model is the new element;
   by construction it is never training-free.
2. **Freeze-and-bolt-on (explicit sensor/brain split).** Keep the text LLM's weights untouched and
   attach separately-trained speech encoder/decoder/duplex-classifier modules (Freeze-Omni, and
   partial-freeze LLaMA-Omni2/SLAM-Omni), or chain fully-separate ASR→LLM→TTS elements
   (Unmute, every cascade framework, AURA, AudioToolAgent). Here the omni's speech modules are
   **sensor + actuator** and the frozen LLM is the **brain**.

**Which class dominates?** The field is **bifurcated**, and the split is the crux for this project.
The research/vendor prestige race is dominated by **fuse-and-retrain hybrids** (all five proprietary
stacks, the open SOTA leaderboards). But on **verifiable agentic tasks**, the **sensor/brain-split
cascade** class is competitive-to-superior:

- **VocalBench**: Cascade(GPT-4o) 82.68% > Qwen3-Omni 78.78% (omni).
- **URO-Bench**: training-free Whisper+GPT-4o cascade 89.33/79.27 EN/ZH **>> best fine-tuned SDM**
  GLM-4-Voice 69.09/66.90; open SDMs "lag their backbone LLMs … catastrophic forgetting."
- **VoiceAgentBench / Audio2Tool**: ASR-LLM cascade (two decorrelated elements) beats one frozen
  end-to-end SpeechLM on tool-calling.
- **From Text to Voice**: when the ASR element is strong (GPT-4o-Transcribe), "neither architecture
  uniformly dominates" — the residual gap localizes to **sensor-element fidelity**, not the
  cascade-vs-native choice.

...but this is **model/benchmark-specific, not a law** (eval-benchmarks-ondisk cross-cut B):
**VoiceBench** has a unified omni (Nemotron-3-Nano-Omni, 89.39) topping the board just ahead of a
cascade. The honest reading: **capability tracks the quality of the elements, not the wiring.**

**The load-bearing tradeoff.** τ-Voice / L4-P1: native-audio hybrids retain only **30–45% of their
own text-mode capability** on identical verifiable tasks, and "reasoning and grounding challenges
persist independently of audio quality." So the hybrid's collapse is **not** primarily a perception
problem — the bottleneck sits at the **audio-facing sensor/interface and the modality-fused
reasoning**, not the orchestration. Tradeoffs, then:

| | fuse-and-retrain (hybrid) | freeze-and-bolt-on (sensor/brain split) |
|---|---|---|
| latency | lowest (single forward pass) | stacks (mitigated by streaming ≈ `max`) |
| paralinguistic signal | preserved end-to-end | lost through the ASR-text bottleneck |
| text-brain ceiling | given up (catastrophic forgetting; measurable capability tax) | **provably inherited unchanged** (Freeze-Omni: "speech ceiling = text ceiling") |
| element swappability | none (monolith) | full (swap ASR/LLM/TTS/tools freely) |
| training-free? | never | the frozen-brain layer is; bolt-ons usually are not |

**Why this matters for the thesis.** The freeze-and-bolt-on / sensor-brain-split architecture is
**exactly the "frozen omni brain + added elements" shape** the project's thesis is built on — it is
the class where a provable oracle ceiling exists (Freeze-Omni demonstrates it architecturally) and
where the training-free opportunity lives. The empirical fact that this class is competitive-to-best
on verifiable tasks is a strong tailwind for W1/W4. Delta vs S1/S2: this generalizes S1's
"curated/targeted beats brute-scale" law into a new modality (LLaMA-Omni2 vs GLM-4-Voice; SLAM-Omni)
and grounds it architecturally.

---

## 3. Framework-test result

Scanned all lanes for a **usage-pattern-only** crossing (role/prompt/multi-agent/routing over one
frozen model, no added element) of a **hard verifiable** capability boundary, measured against the
frozen model's **own oracle/ceiling** (not a naive baseline). The formal result:

```json
{"anyUsageOnlyCrossing":false,"elementSetVerdict":"closed-supported","reasoning":"Scanned all 15 lanes for a usage-pattern-only (role/prompt/multi-agent/routing over one frozen model, no added element) crossing of a hard verifiable capability boundary. Twelve lanes report none. The remaining candidates each fail the evidentiary bar (hard verifiable boundary AND measured against the frozen model's OWN oracle/ceiling, not a naive baseline AND usage-pattern the sole lever with no smuggled element). STRONGEST CANDIDATE: arXiv 2505.24347 same-model self-check ASR correction — real same-weights CER/WER gains (21/11/9/11.4%) with no external verifier/second model — but the gain is measured against a naive direct-correction baseline (which over-hallucinates), NOT the model's own ceiling; most parsimoniously it recovers/reads out the existing ceiling rather than crossing a boundary. It lacks exactly the oracle-ceiling control needed, so it is requires-nuance/Stage-2-parked, not a REFUTES. RegionFocus (+28%/+24% on frozen VLM via zoom/crop) actively injects new higher-resolution visual information, so it is better classed as an input-transformation ELEMENT, not a pure re-query — it supports the thesis under the thesis's own logic. AURA's ReAct loop lacks a non-agentic ablation and separately draws its gain from real tool connectors (elements). Full-Duplex-Bench-v3's cascaded controller wins only on Easy tasks, is capped by an ASR-finalization CONSTRAINT, and adds a decorrelated Whisper element. Generative Agents' reflection rests on soft LLM/human believability scoring, failing the verifiable-boundary bar. Talker-Reasoner/ConvFill is unresolved on weight-sharing. The two perception-delta candidates are contested/unresolved (that lane's pass=false is a verification-process failure, not a discovered refutation). Against these, multiple lanes give affirmative confirmation: homogeneous same-weights debate does not beat self-consistency (martingale proof); tau-Voice shows a harness change alone retains only 30-45% of text capability; Memory-R1 shows a weight-updated role beats the identical prompted role; tau2-bench pass^k decay (90%->57%) shows resampling exposes inconsistency, not new information; Step-Audio-R1 shows CoT fails on audio. Net: zero candidate survives as a genuine counterexample and there is direct positive evidence, so the closed-element-set claim is supported — at Stage-1 grade, with arXiv 2505.24347 explicitly flagged for a Stage-2 oracle-ceiling re-test.","strongestCounterexamples":["arXiv 2505.24347 training-free same-model self-check ASR correction (same-weights pre-detection->CoT-correction->self-verification; real CER/WER gains but measured vs a naive baseline, no oracle-ceiling control -> plausibly reads out the model's own ceiling, not a boundary crossing; Stage-2 re-test parked)","RegionFocus frozen-VLM test-time zoom/crop (+28% ScreenSpot-Pro / +24% WebVoyager; the zoom injects new higher-res visual info -> better classed as an input-transformation element than a pure usage pattern)","AURA cascaded ReAct voice agent (90% task success but NO non-agentic ablation; gain independently traced to real calendar/email/search tool connectors = elements)","Full-Duplex-Bench-v3 cascaded text-LLM controller (beats end-to-end only on Easy tasks; capped by an ASR-finalization constraint and already adds a decorrelated Whisper ASR element)","Generative Agents reflection step (improves only soft LLM/human believability scores, not a verifiable ceiling; the persistent memory stream is the real element)","Talker-Reasoner / ConvFill 'Thinking While Speaking' dual-process (unresolved whether Talker and Reasoner share weights; no benchmark demonstrates the crossing)","perception-delta contested pair: 'Resurfacing Paralinguistic Awareness' and 'Reflecting Twice before Speaking with Empathy' training-free variants (controls/ablations unverifiable; lane pass=false)"],"examplesIfAny":[]}
```

**Plain-language reading.** `anyUsageOnlyCrossing = false`; `elementSetVerdict = closed-supported`.
No usage-pattern-only lever crossed a hard verifiable boundary against the frozen model's own
ceiling. The seven strongest candidates each fail the bar for a specific, named reason (naive-baseline
comparison; injected input-information; missing non-agentic ablation; smuggled decorrelated element;
soft-metric scoring; unresolved weight-sharing; unverifiable controls). Against them stand five
**direct positive confirmations**: martingale proof that same-weights debate cannot raise expected
correctness; τ-Voice's harness-only 30–45% retention; Memory-R1's weight-updated-role > prompted-role;
τ²-bench pass^k decay (resampling exposes inconsistency, adds no info); Step-Audio-R1's CoT-hurts-audio.
**The one live risk is [2505.24347]** — flagged for a Stage-2 oracle-ceiling-controlled re-test (also
GAP-6 below). Grade: **Stage-1 hypothesis** (argumentation, not this project's own large-sample
validation).

---

## 4. Evaluation-methodology map + the empty cells

**The verification fork is a live, already-adopted design choice, not a hypothesis.** Three on-disk
benchmarks mix a deterministic **verifier-as-tool** (element) with an LLM-judge **verifier-as-role**
(usage-pattern) *inside one instrument*:

| instrument | verifier-as-tool (element) | verifier-as-role (usage-pattern) |
|---|---|---|
| τ²-bench / τ-Voice | DB-state diff | LLM-simulated user + content parsing |
| EVA-Bench | SHA-256 scenario-DB hash | Faithfulness / Progression / Conciseness LLM+LALM judge |
| VoiceBench | MCQ exact-match, AdvBench rule classifier | GPT-4o-mini judge on open-ended subsets |

Reliability tracks the fork exactly: symbolic checks ≈100% (τ²-bench/EVA hash); trained judges
(WavReward 91.5%, GenRM +16–40%, Talking Turns) are reliable; **prompted zero-shot audio judges are
not** (AudioJudge bias; SpeechJudge <70% human agreement; VocalBench LLM-judge ~88% ceiling). Every
speech team that needed a *reliable* judge trained a new element — revealed-preference confirmation.

**The N1/N2 empty cell — refined, not closed** (eval-methodology headline; delta vs L4-N1/N2):

1. `pass@k`/`pass^k` terminology **has entered** voice-agent eval (τ²-bench carries τ-bench's `pass^k`;
   **EVA-Bench actually measures pass@1/pass@k/pass^k** with k=5/k=3 and reports a 0.44 median
   peak-vs-reliable gap). This **refutes the letter** of L4-N1 ("no pass@k measurement exists") — a
   miss in the 2026-07-04 sweep, since EVA-Bench (2605.13841) predates it.
2. But in **every** case it is used as a **reliability/consistency lens over one frozen system**,
   **never as a selection mechanism** (an oracle/verifier picking best-of-k to raise a deployed score).
   The measured ceiling exists; **no training-free selector reaches it.**
3. **EVA-Bench explicitly disclaims prompt optimization** ("system prompts were not optimized … would
   likely yield higher scores") — first-party confirmation that prompt-opt is unattempted, not absent.
4. τ²-bench voice submissions are **Pass^1-only by documented convention** (multi-trial audio eval is
   "expensive") — a *cost* barrier, leaving the cell open rather than closed.
5. The identical toolkit (best-of-N, self-consistency, reward reranking) is a **thriving 2025–26
   text-LLM area** (2604.12196, 2502.18581, 2604.07666) with **zero confirmed crossover** to any of
   the nine voice-agent benchmarks checked. SDiaReward is the closest candidate element (a trained
   spoken-dialogue reward model) but is benchmarked only on its own preference accuracy, not deployed
   in a best-of-N loop.

**Other first-class empty cells:**
- **No cross-session benchmark** — all instruments are single-session; the harness to *score* a
  curated cross-session memory method does not yet exist (CONFIRMS S1/S2 at the infrastructure level).
- **No human topline** for almost the entire field — **MMAU-Pro (77.9%) is the sole quantified human
  anchor**; "how far below human" is unanswerable from the record, routinely conflated with
  "how far below the frozen-model oracle ceiling."
- **No cascade-vs-native head-to-head** on live verifiable tasks (τ²-bench-voice / τ-Voice support
  both but Sierra "have not yet published" it) — only the TTS-synthesized From Text to Voice has.
- **The project's own lever (training-free best-of-N / reward-guided decoding / prompt-opt) has never
  been searched for *positively* on a voice benchmark** — the central axis is empirically empty (see
  completeness gap §6.3).

---

## 5. Gap map → candidate Stage-1 research problems

Six candidates for a **training-free frozen-omni agentic system**, each tagged single/cross-session
and mapped to a framework axis. All are Stage-1 problem-definition candidates for the owner
discussion — none rolls over automatically.

**GAP-1 — Training-free reward-guided best-of-N that actually *reaches* the measured pass^k ceiling
on a verifiable voice-agent benchmark.** *(single-session; axis: usage-pattern (selection) gated by
an element (decorrelated reward/symbolic DB-state verifier)).* The flagship empty cell: EVA-Bench /
τ²-bench-voice publish the pass@k *ceiling*; nobody has built a selector that attains it. This is the
one axis that is both central to the thesis and completely empty (§4, §6.3). The decisive design
choice is the reward source — a **symbolic DB-state check** or a **trained/decorrelated reward model**
is an element (allowed and reliable); a same-model self-reward is a usage-pattern (bounded, and the
self-preference-bias risk N2 is empirically unstudied for audio). Delta: directly closes L4-N1/N2 and
the verification-reward N3/N5 cells.

**GAP-2 — Audio-native, paralinguistically-keyed, cross-session memory MUTATION.** *(cross-session;
axis: element (persistent store) + constraint (verifiable-reward admission gate)).* memory-components
C14: no system combines (a) Mem0-style ADD/UPDATE/DELETE mutation, (b) keys on **raw
audio/speaker-ID/SER** not transcribed text, and (c) accumulates across **real** multi-session
same-speaker interaction with verifiable admission. AFA is the closest (speaker-ID routing) but keys
route to *text* objects on *synthetic* data. This is a **mechanism-level** gap (not just a
missing benchmark) and the single most decision-relevant surface for W4. Delta: sharpens S2's
A1-23/A1-24 and the D2 delta scan from benchmark-level to mechanism-level.

**GAP-3 — Omni-as-decorrelated-verifier for training-free best-of-N.** *(single-session; axis:
element (verifier-as-tool via context/error decorrelation) vs the bounded usage-pattern of
same-context self-reward).* AudioToolAgent proves the shape (a text-only coordinator that never
touches the audio, arbitrating over audio-LM tools, wins SOTA). The open Stage-1 question: can two
**context-differentiated** views of the *same* frozen omni (per the mem0 omni-verifier-decorrelation
note) act as a genuine element, and what achievable error-decorrelation δ_corr is the binding
constraint? Directly tests the self-preference-bias empty cell (N2). Delta: operationalizes the
mem0 "omni-verifier decorrelation" memory into a Stage-1 problem.

**GAP-4 — Active audio "zoom" / re-sensing as a training-free input-transformation element.**
*(single-session; axis: element (input-transformation connector), sharpening the RegionFocus
boundary case).* RegionFocus (+28%/+24% on a frozen VLM) works because the zoom *injects new
higher-resolution information* — an input-transformation element, not a pure re-query. The audio
analog is **re-segmenting / source-separating / re-sampling the raw signal** (isolate a speaker,
re-sample a suspected entity span at higher resolution) before re-querying the frozen omni. This is
the concrete, thesis-consistent way to distinguish a smuggled element ("extract new signal") from a
hollow usage-pattern ("re-attend the same transcript"). Untested in speech in either direction.

**GAP-5 — Paralinguistic-conditioned *agentic decision* with a verifiable-reward pass@k measure.**
*(single-session; axis: element (paralinguistic channel as connector) gated by constraint
(verifiable reward)).* perception-delta empty cell: every >transcript study measures response/quality
or instruction-following, **none** measures a paralinguistic cue changing a *downstream verifiable
tool-use decision* (e.g. escalate-to-human on detected frustration; alter a DB-query plan on detected
urgency) with a τ²-bench/EVA-style pass@k. This bridges the perception-delta and eval lanes and is a
clean Stage-1 problem with a verifiable ground truth. Delta: sharpens L4-N1/N2 into the
paralinguistic-agentic setting.

**GAP-6 — Oracle-ceiling-controlled re-test of same-model self-check, generalized to a frozen omni.**
*(single-session; axis: usage-pattern (same-model self-verification) — is it a crossing or a read-out
toward the model's own ceiling?).* The framework-test's **STRONGEST CANDIDATE** [2505.24347] reports
real same-weights ASR-correction gains but only vs a naive baseline. A Stage-1 directional re-test
with the missing **oracle-ceiling control** (does structured self-check exceed the frozen model's own
best-achievable output, or merely recover it?) would settle whether the closed-element-set claim
survives at Stage-2. This is the single highest-value re-test target and the load-bearing risk to the
whole verdict. Delta: promotes the framework-test's parked risk into an explicit experiment design.

*(Cross-cutting note: GAP-1/3/6 are the same axis — "does a usage-pattern reach the frozen model's
own ceiling?" — probed as selection, decorrelated-verifier, and self-check respectively. GAP-2/5 are
the element-side cross-session and paralinguistic-agentic surfaces. All are `directional-only`,
single-touch quick validations at Stage-1; small-n settles nothing.)*

---

## 6. Completeness critique — gaps worth a second pass

The synthesis inherits the following coverage gaps (delta-tagged vs archive S1/S2/L4 where relevant).

### 6.1 Notable systems missing (2025–26, in scope)
- **Open S2S/omni not surveyed as systems:** Kimi-Audio (Moonshot), MiniCPM-o 2.6, VITA-1.5 (Tencent),
  Baichuan-Omni/-Audio, Meta SpiritLM (interleaved speech-text) and Seamless/SeamlessM4T,
  Mini-Omni/Mini-Omni2, SpeechGPT, AudioPaLM. **GLM-4-Voice appears only as a beaten baseline** — never
  surveyed on its own despite being a canonical open S2S. SALMONN (a CLAUDE.md swap target) and base
  Qwen2-Audio are also never given a system-level entry. *(Partial: some appear as beaten baselines in
  s2s-native-open / eval lanes; none gets a first-class entry.)*
- **Proprietary lane names only OpenAI / Google / xAI** among the "five vendors" for tool/architecture
  depth — verify Amazon Nova Sonic, Microsoft Copilot Voice, ByteDance Doubao are all covered (Nova/
  Microsoft are, at low disclosure; **Doubao is absent**). **Hume EVI** (empathic voice) and **Sesame
  CSM** are absent and directly relevant to the failing perception-delta lane.
- **Cascade lane vendor coverage is thin:** only Pipecat/LiveKit/Vocode/Salesforce/Retell/Vapi/Bland/
  Deepgram. Missing the dominant commercial stack — **ElevenLabs Conversational AI, Cartesia Sonic,
  AssemblyAI** (Retell/Vapi/Deepgram are present).

### 6.2 Benchmarks missing
Eval lanes are dense but omit widely-cited audio-understanding / spoken-dialogue benches: **AIR-Bench,
AudioBench, Dynamic-SUPERB** (cited via Speech-Copilot but never a benchmark entry), **SD-Eval**
(present in eval-benchmarks-field/perception-delta as a genealogy root only), **VoxEval,
Speech-IFEval, ContextASR-Bench, SpokenWOZ, Big Bench Audio** (present only as a vendor-race number,
not a benchmark entry), and base **MMAU / MMAR** (MMAR is covered; MMAU scored inside AudioToolAgent
but not surveyed as a benchmark).

### 6.3 Modalities of search not run
- **Chinese-ecosystem sources under-searched** — company tech reports/blogs for Doubao, Kimi, Step,
  MiniCPM, GLM, VITA. The survey skews English/arXiv; the China S2S wave is largely invisible.
- **No refutation/adversarial search pass.** Every lane reports `usage-only-crossing = none` — a
  near-monoculture that suggests confirmation-biased querying (hunting thesis-confirming element cases,
  not usage-pattern wins). Worth one lane that actively hunts the counterexample.
- **The project's own lever is never searched for *positively* on voice:** no lane looked for a
  *training-free best-of-N / reward-guided decoding / prompt-optimization WIN on a voice benchmark*.
  The repeated N1/N2 negative may be a **search gap, not a true absence** — this is the central axis
  (GAP-1) and it is empty. Delta vs L4-N1/N2: the negative should be re-graded "unsearched-positive,"
  not "confirmed-absent."

### 6.4 Claims left unverified / contested (highest-value re-test targets)
- **Entire perception-delta lane's `pass=false`** is a verification-process failure, not a discovered
  refutation — reopen it. "Resurfacing Paralinguistic Awareness" was corrected to a fine-tuned/element
  case (not a training-free crossing); "Reflecting Twice before Speaking with Empathy" remains a
  genuinely unresolved training-free candidate (controls unconfirmed).
- **Self-check ASR correction (2505.24347)** — the one apparent usage-pattern crossing; no oracle-
  ceiling control → gain-vs-ceiling unresolved. **Explicitly flagged for Stage-2 (= GAP-6).**
- **Talker-Reasoner / ConvFill** — resolved in eval-benchmarks-field as *disjoint* models (off-target
  for the frozen-model fork), still listed as a dangling test case elsewhere; reconcile.
- **AURA** — cited across 3 lanes (90–92% numbers) with **no non-agentic ablation**; ReAct-format vs
  tool-access attribution unquantified.
- **RegionFocus** — element/usage-pattern boundary genuinely ambiguous; treated here as an
  input-transformation element (GAP-4), but the call deserves consolidation.
- **Citation integrity:** several 2026 arXiv IDs (2603/2604/2605/2606 ranges) carry an arXiv-side
  month/ID mismatch quirk (e.g. 2605.02909 announced 2026-04); each lane's verifier confirmed
  resolution, but confirm before any single ID anchors a Stage-2 claim.

### 6.5 Framework axes thinly covered
- **Cost/economics & the latency↔capability tradeoff** — only LiveKit's `max()` note; no
  compute-normalized cross-system comparison.
- **Multilingual/low-resource tax** — only Indic (VoiceAgentBench) and EN/ZH (URO-Bench,
  VocalBench-zh); no systematic non-English capability-delta despite heavy Chinese-model presence.
- **Multi-party / diarization / overlapping-speaker** operation — essentially absent as a constraint.
- **Constraint axis is breadth-limited:** real-time context/session caps are well covered, but other
  substrate constraints (streaming-ASR finalization — appears once via Full-Duplex-Bench-v3;
  audio-token-rate; codec/tokenizer bottleneck) are under-developed.
- **Element/usage-pattern boundary stress-tests** (RegionFocus, FlexDuo's gating-only element,
  "actively changing the input" cases) surfaced but were never consolidated into a sharpened decision
  rule — the framework's own edge cases deserve one dedicated synthesis. *(GAP-4 is the concrete
  audio instance of exactly this.)*

---

## 7. Net Stage-1 reading

Across 14 verifier-passed lanes and ~120 systems: **zero usage-pattern-only crossings of a hard
verifiable boundary survive scrutiny; the closed-element-set claim is supported at Stage-1 grade**,
with [2505.24347] the one parked risk. Every genuine capability crossing traced to an **element** (a
different model, a trained module, a tool/knowledge/memory connector) or required **weight change**;
usage-pattern levers either read out the frozen model's existing ceiling (self-certainty BoN,
same-model self-check) or actively failed (homogeneous debate — martingale-proved; CoT-on-audio;
reflection-confabulation; declared-workflow interruption-recovery). The sensor/brain-split
(freeze-and-bolt-on) architecture — the thesis's native shape — is competitive-to-best on verifiable
agentic tasks, and the central lever (training-free reward-guided best-of-N on a **voice-agent** benchmark)
remains **empty** — the strongest single Stage-2 opportunity (GAP-1, re-scoped per §8). This ends Stage-1;
the owner discussion selects the problem. **Read §8 first — three verification passes materially sharpened
the claims above.**

---

## 8. Second-pass hardening (adversarial + positive-search + citation-integrity, 2026-07-06)

Three targeted verification agents were run against this synthesis's central claims. All three materially
sharpened it; the net is a **stronger, more precisely-stated** thesis. **These corrections supersede the
looser statements in §3–§5 and §7.**

**8.1 Citation integrity — CLEAN.** All 21 load-bearing arXiv IDs resolve to real papers with matching
titles; no hallucinations, no dead links, no topic mismatches. Two are our own shorthand labels ("CB-RAG"
= 2509.19567 "RAG-based context discovery for ASR"; "same-model self-check" = 2505.24347) — wording tweaks,
not citation errors.

**8.2 The framework-test's "strongest candidate" (2505.24347) DISSOLVES → thesis strengthened.** On
inspection 2505.24347 = *"Fewer Hallucinations, More Verification: A Three-Stage LLM-Based Framework for ASR
Error Correction"* uses an **external GPT-4o** in a detect→correct→verify loop — a **second model
(element)**, not same-model self-check. It was never a clean usage-pattern candidate; its gains come from
GPT-4o's language prior (new-info). The one parked risk is thus largely resolved: it is an **element** case.
(An in-house oracle-ceiling re-test of self-check *without* a second model remains a clean Stage-1 probe =
GAP-6.)

**8.3 The empty cell was OVER-CLAIMED — corrected.** "No training-free best-of-N/self-consistency/prompt-opt
win on ANY audio benchmark" is **FALSE**: MMAU has several training-free positives — Audio-CoT (2501.07246:
55.6→58.1 via CoT + 5-vote self-consistency), Scaling Auditory Cognition via TTC (2503.23395: +9–150% via
majority / beam-reranking / verifier on frozen ALMs), AQA-TTRL DIMV baseline (2510.05478: 64-vote majority).
**These are READ-OUT gains** — measured vs the model's own **greedy**, bounded above by pass@N oracle
(consistent with, not contradicting, the thesis). The **defensible empty cell narrows** to: *no training-free
reward-guided selection reaching the verifiable **pass^k ceiling** on an **interactive voice-agent** benchmark
(τ²-voice / EVA-Bench).* **GAP-1 is re-scoped to the voice-agent setting** (the MMAU cell is occupied; L4-N1/N2
must be re-graded "occupied on audio-understanding QA, empty on voice-agent verifiable tasks").

**8.4 State the ORACLE-READING explicitly.** The strict verdict HOLDS (no usage-pattern-only crossing *above
the model's own oracle* survives four gates), but it is near-tautological under its own bar and must be
stated precisely: **a usage pattern can move the DEPLOYED (greedy) score UP TOWARD the model's own oracle@N
— 2503.23395 proves large such gains on audio — but it cannot EXCEED that oracle.** The thesis is about the
**ceiling** (crossing the capability/knowledge boundary), not "usage patterns are useless." Conflating "beats
greedy" with "crosses a boundary" would wrongly read the thesis as false. (This is exactly
`TfrlProofs.InfoBoundary.readout_acc_le_oracle`.)

**8.5 "Element set is closed" is OVER-CLAIMED — a FOURTH lever family exists.** The taxonomy {elements /
usage-patterns / constraints} omits **inference-computation edits**: decoding-algorithm or forward-pass
restructuring that is training-free, single-model, and info-clean, yet changes the model's own output
**distribution** (not just its prompt). Clean case: **EGLR (Entropy-Gated Latent Recursion, 2606.16620)** —
provably expands a frozen model's verifiable **oracle** by **+8.2pp** beyond the temperature-only oracle
(MATH-500, Qwen2.5-3B) with **no new external info**; audio analog: Temporal Contrastive Decoding
(2604.15383). This is neither an element (no new info) nor a usage-pattern (not a role/prompt) — a **distinct
class**. It changes inference **structure/computation**, so it is **EXCLUDED by this project's "no weight AND
no structure change" frozen contract** (Project-Thesis) — but the framework must NAME it. Corrected claim:
*closed among **prompt/orchestration-level** usage patterns over a **fixed inference computation**;
decoding/inference-compute edits are a separate, structure-touching family, out of scope for the frozen
contract, and the most plausible site of an info-free ceiling-expansion.*

**8.6 In-house perception-delta datapoint** (supplements the perception-delta lane, which failed external
verification). Boundary-clean probe (same frozen omni: audio vs its own ASR transcript; p6, n=60):
**SQuAD-zh +0.283 SIG** CI[0.13,0.43]; mmau +0.117 n.s.; vocalbench-zh +0.000. The omni's direct-audio path
carries info its own transcript loses, **task-dependent** — validates omni-as-perception-element (D0 item i).
Caveat: vs its **own** ASR; the strong-external-ASR control is the Stage-2 target (GAP-5). See
`2026-07-06-exp-perception-delta`.

**8.7 Net.** All three passes leave the thesis **intact and sharper**: usage patterns are oracle-bounded
(read-out) — confirmed and precisely stated; the one parked counterexample dissolves into an element; the
empty cell is correctly narrowed to voice-agent verifiable tasks (GAP-1); a fourth lever family
(decoding-compute, excluded by our contract) is named. Remaining second-pass debts for the paper: missing
system entries (Kimi-Audio, MiniCPM-o, Doubao, Hume EVI, Sesame CSM), missing benches (AIR-Bench, AudioBench,
SpokenWOZ), and the Chinese-ecosystem search gap (§6). Grade: **Stage-1 hypothesis, second-pass-hardened.**
