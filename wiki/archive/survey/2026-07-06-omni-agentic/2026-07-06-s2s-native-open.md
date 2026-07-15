---
title: "Lane survey — open end-to-end speech-to-speech / native-audio agent models (architecture, element vs usage-pattern, brain vs sensor)"
date: 2026-07-06
stage: 1-argumentation
lane: s2s-native-open
---

> **🗄 ARCHIVED (2026-07-11)** — 已收官战役过程件（2026-07-06 omni-agentic 调研），仅作历史，非现行真源。

# S2S native-open lane — architecture landscape, element/usage-pattern/brain-sensor classification

**Scope note:** this lane surveys *how* open native audio-in/audio-out (or omni) models are **built**
— not their duplex/turn-taking behavior (that is `2026-07-06-duplex-realtime.md`'s job; cross-referenced
below where the same system appears in both). The organizing question here is: for each system, is its
capability contributed by a genuinely new **element** (a new pretrained model, a new connector/tool, a
new trained module) or merely a **usage pattern** (a role/prompt/orchestration trick) layered over one
frozen set of weights — and does the "omni" component act as **brain** (does the reasoning), **sensor**
(perceives audio in), **actuator** (renders speech out), or some explicit **hybrid** split of these.

## Up front: the field decomposes into two build strategies, and they are directly comparable

Reading across all 14 systems below, there are exactly two architectural strategies for getting a text
LLM to speak, and every system in this lane is one or the other:

1. **Fuse-and-retrain**: take a text LLM (or train one from scratch) and continue pretraining /
   fully fine-tune it jointly with speech tokens, so the *same* weights that reason also emit audio
   tokens (Moshi, GLM-4-Voice, Kimi-Audio, Qwen2.5-/Qwen3-Omni, MiniCPM-o, Baichuan-Audio, Step-Audio 2,
   Ola). Here the omni model plays **brain+sensor+actuator in one artifact** (a "hybrid" role in this
   template's vocabulary) and the *entire model* is the new element — weights change, so by
   construction this path is never training-free.
2. **Freeze-and-bolt-on**: keep a pretrained text LLM's weights literally untouched and attach new,
   separately-trained speech encoder/decoder (and sometimes a duplex-state classifier) modules around
   it (Freeze-Omni, and — with a partial-freeze variant — LLaMA-Omni2, SLAM-Omni). Here the omni's
   speech modules are explicitly **sensor + actuator**, and the frozen LLM is explicitly the **brain**;
   the paper's own claim is that speech-domain "intelligence" is capped at, and inherited unchanged
   from, the frozen backbone's text-domain ceiling — i.e., the connector is the new element, and the
   ceiling is the old model's ceiling. This is the cleanest confirmation in the whole survey of the
   project's "oracle ceiling" idea, just demonstrated architecturally rather than via a verifier-prompt
   usage pattern.

A third, cross-cutting observation: **when these systems need agentic tool-use (web search, hanging up
a call, invoking an API), every case found bolts on a literal external connector** — Kyutai's Unmute
(cascaded LLM + tool-calling, built explicitly *because* native Moshi cannot function-call) and
Step-Audio 2's built-in RAG/web-search/audio-search tool calls. No system in this lane gets tool-use
"for free" out of decoding tricks over the frozen audio-native weights; it is added as a real connector
element every time this was checked — a second confirmation of the main thesis's element/usage-pattern
line, generalized from "verifier" to "tool" more broadly.

---

## Claims

### 1. Moshi (Kyutai) — single fused model is simultaneously brain+sensor+actuator
- **Recognized problem:** cascaded ASR→LLM→TTS serializes each stage, precluding real-time
  full-duplex, overlapping dialogue.
- **Genealogy:** speech-native Temporal Transformer (7B, initialized from Kyutai's own Helium text LM)
  + a small Depth Transformer for inter-codebook dependence, plus "Inner Monologue" (time-aligned text
  token prefix before semantic/acoustic audio tokens) to preserve factuality/linguistic quality.
  Origin-domain: speech, with an LLM-pretraining root (Helium) that is **ported** into the fused
  architecture, then **native** from there. Source: [arXiv:2410.00037](https://arxiv.org/abs/2410.00037)
  (Défossez et al., Kyutai; code [github.com/kyutai-labs/moshi](https://github.com/kyutai-labs/moshi)).
- **Training-free vs fine-tuned:** fine-tuned/continually trained in four stages (text pretrain → audio
  pretrain → multi-stream post-training → instruction FT); the Temporal Transformer starts from
  pretrained Helium weights, so it is emphatically **not frozen, not training-free**.
- **Class + verdict:** **element** — Moshi is a whole new pretrained artifact; the Inner-Monologue
  text-prefix trick is trained into pretraining, not an inference-time usage pattern over a frozen
  checkpoint. No tool-use/retrieval is architected in — an acknowledged limitation (confirmed below).
- **Fence tag:** single-session (no cross-session memory/accumulation claimed).
- **Omni role:** **hybrid** — one artifact is sensor (continuously consuming user audio), brain
  (dialogue reasoning), and actuator (speech synthesis) at once.
- **Delta vs archive:** NEW. Cross-ref: this system is also analyzed for its duplex mechanism in
  `2026-07-06-duplex-realtime.md`#1 — CONFIRMS that lane's "fully retrained, not frozen" finding; this
  lane adds the element/brain-sensor framing on top.

### 2. Kyutai Unmute — the tool-use gap in Moshi is closed by adding a real connector element, not a prompt trick
- **Recognized problem:** Moshi's native fused architecture has no function-calling, in-context tool
  use, or up-to-date external knowledge — Kyutai's own framing: *"While Moshi provides unmatched
  latency and naturalness, it doesn't yet match the extended abilities of text models such as
  function-calling, stronger reasoning capabilities, and in-context learning."*
- **Genealogy:** Unmute is **not** Moshi — it is an explicitly **cascaded** system (Kyutai
  STT → any external text LLM → Kyutai TTS) built precisely to recover tool-use/reasoning by
  reintroducing a text-based LLM that already has those abilities. Origin-domain: speech I/O
  (native) wrapping an interchangeable text-LLM brain (ported, LLM-domain). Source:
  [kyutai.org/unmute](https://kyutai.org/unmute/).
- **Training-free vs fine-tuned:** the cascade itself requires no new training of the LLM (the "brain"
  is whatever off-the-shelf LLM is plugged in) — but the STT/TTS models are themselves trained speech
  elements, and tool integration is via literal API calls (a hang-up command, a live news API), not a
  role/prompt trick over one frozen omni checkpoint.
- **Class + verdict:** **element** — the fix for the capability gap is adding a genuine external
  connector (an API/tool-call interface plus an independent text LLM), matching the framework's
  "verifier-as-tool = a real element" fork generalized to tool-use broadly. This is a direct,
  citable, real-world instance of the main thesis: crossing this capability boundary required a
  new-info element, not an orchestration/prompting change over Moshi's frozen weights.
- **Fence tag:** single-session (tool calls are per-turn; no persistent cross-session memory
  documented).
- **Omni role:** in Unmute's design the speech models are pure **sensor+actuator** (STT in, TTS out);
  the **brain** is the swappable external text LLM — an explicit architectural sensor/brain split,
  contrasted directly with Moshi's fused hybrid (#1).
- **Delta vs archive:** NEW — a concrete case study supporting the main thesis fork, not previously in
  the archive.

### 3. Freeze-Omni — frozen text LLM + trained speech connector; ceiling = backbone's own ceiling
- **Recognized problem:** naively fine-tuning an LLM to add speech I/O induces catastrophic forgetting
  / degrades the backbone's original text-domain intelligence.
- **Genealogy:** any frozen instruction-tuned text LLM (backbone) + a new streaming speech encoder,
  a new streaming speech decoder, and a new classification head (for interruption/duplex state) —
  all newly trained; the backbone LLM's parameters are **never updated**. Source:
  [arXiv:2411.00774](https://arxiv.org/abs/2411.00774) (Wang et al., VITA-MLLM/Tencent; code
  [github.com/VITA-MLLM/Freeze-Omni](https://github.com/VITA-MLLM/Freeze-Omni)).
- **Training-free vs fine-tuned:** the **backbone LLM is literally frozen** throughout — only the new
  peripheral modules (~60K text Q&A pairs, 8 GPUs) are trained. This is the strongest "frozen brain +
  trained connector" case in the lane.
- **Class + verdict:** **element** (the new speech encoder/decoder/classifier are the entire source of
  new capability) applied to an unmodified pre-existing element (the frozen LLM). Explicit textual
  claim: *"can effectively ensure that the intelligence of the Freeze-Omni in the speech modality is at
  the same level compared with that in the text modality of its backbone LLM"* — i.e., the speech-domain
  competence ceiling is architecturally *inherited*, unchanged, from the frozen backbone. This is the
  cleanest empirical instance in this lane of the "oracle ceiling bounded by the frozen model's own
  competence" idea, demonstrated by construction rather than by a verifier-prompt A/B.
- **Fence tag:** single-session.
- **Omni role:** **explicit split** — new speech modules = sensor (encoder) + actuator (decoder);
  frozen backbone LLM = brain. The cleanest sensor/brain decomposition in the survey.
- **Delta vs archive:** NEW; cross-ref `2026-07-06-duplex-realtime.md`#2 covers the same system's duplex
  classifier — CONFIRMS the "frozen brain, bolt-on element" framing from that lane, this entry adds the
  explicit "ceiling inherited from backbone" quote.

### 4. GLM-4-Voice — the opposite strategy from Freeze-Omni for the *same* stated problem (preserve intelligence), at a much higher cost
- **Recognized problem:** stated identically to Freeze-Omni's — preserve the backbone's intelligence
  while adding speech, plus real-time controllability (emotion/dialect/rate).
- **Genealogy:** ultra-low-bitrate (175 bps), single-codebook, 12.5 Hz speech tokenizer fine-tuned from
  Whisper-large-v3 (an ASR model repurposed as a discretizing sensor) + continued pretraining of GLM-4-9B
  on synthesized speech-text interleaved data at **1 trillion tokens** + a CosyVoice-retrained streaming
  decoder. Source: [arXiv:2412.02612](https://arxiv.org/abs/2412.02612) (Zeng et al., Zhipu/Tsinghua;
  tokenizer: [huggingface.co/zai-org/glm-4-voice-tokenizer](https://huggingface.co/zai-org/glm-4-voice-tokenizer)).
- **Training-free vs fine-tuned:** the GLM-4-9B backbone is **not frozen** — it is *continually
  pretrained* on the interleaved corpus, i.e. weights change extensively (contrast directly with
  Freeze-Omni's frozen-backbone route to the identical stated problem).
- **Class + verdict:** **element** — a new pretrained-weights artifact. Direct genealogy fork versus
  Freeze-Omni: same recognized problem, two incompatible architectural answers (freeze-and-bolt-on vs.
  fuse-and-retrain-at-scale), and — per claim #5 below — a third paper (LLaMA-Omni2) found the
  data-hungry route beatable with ~1000x less data via a bolt-on strategy, suggesting the
  freeze/bolt-on family is the more sample-efficient of the two for this specific problem.
- **Fence tag:** single-session.
- **Omni role:** **hybrid** (fused single model; sensor/brain/actuator collapse into one weight set,
  as with Moshi).
- **Delta vs archive:** NEW.

### 5. LLaMA-Omni2 — reusing a strong pretrained LLM's existing competence beats continued pretraining at scale, on 1000x less data
- **Recognized problem:** build a real-time SpeechLM cheaply, without the massive speech-text
  pretraining budget that native fused models (e.g. GLM-4-Voice) require.
- **Genealogy:** Qwen2.5 (0.5B–14B) LLM backbone + frozen Whisper-large-v3 encoder + a trained speech
  adapter + a gate-fusion module + a Qwen2.5-0.5B-initialized autoregressive streaming TTS LM + a
  chunk-aware flow-matching vocoder, with a configurable read/write ratio for streaming. Source:
  [arXiv:2505.02625](https://arxiv.org/abs/2505.02625) (ACL 2025; ICTNLP; code
  [github.com/ictnlp/LLaMA-Omni2](https://github.com/ictnlp/LLaMA-Omni2) — corrected by verifier; the
  lane previously linked the v1 `LLaMA-Omni` repo, a different, earlier system by the same group).
- **Training-free vs fine-tuned:** staged — Stage I(a) **fully fine-tunes** the LLM jointly with the
  new speech adapter; Stage II then **freezes** the encoder/adapter/LLM and trains only the new gate
  fusion + TTS modules. So the LLM is fine-tuned once, then frozen for the rest of training — a hybrid
  of the two strategies, not purely frozen like Freeze-Omni.
- **Class + verdict:** **element** — new adapter/gate/decoder modules, but the headline empirical
  result is genealogical: *"LLaMA-Omni 2 demonstrates strong performance ... surpassing previous
  state-of-the-art SpeechLMs like GLM-4-Voice, which was trained on millions of hours of speech data"*
  while itself using only **200K** multi-turn speech dialogue samples — i.e., leveraging a strong
  existing pretrained LLM's competence (an already-existing element) via a small amount of new
  connective tissue outperforms training a huge amount of new speech-text data into the weights from
  scratch. This directly parallels the archive's S2 finding (curated-small beats brute-scale
  self-generated) in a completely different modality/task — a cross-domain confirmation worth noting.
- **Fence tag:** single-session.
- **Omni role:** **explicit split** — Whisper encoder = sensor, Qwen2.5 LLM = brain, TTS LM + vocoder =
  actuator; gate-fusion module explicitly mediates the sensor→brain handoff.
- **Delta vs archive:** CONFIRMS S1/S2's "curated/targeted beats brute scale" pattern, in a new
  modality (speech-native architecture design, not agent memory/skills) — NEW instance, same
  underlying law.

### 6. Step-Audio 2 — native fused audio LLM, with hallucination fixed by bolting on RAG/web-search as a real element
- **Recognized problem:** unify ASR + paralinguistic (emotion/tone) reasoning + speech generation in
  one architecture without cascaded latency/error propagation, and reduce hallucination.
- **Genealogy:** a latent audio encoder feeding a single LLM that natively does ASR, translation, sound
  reasoning, and voice-to-voice dialogue; a streaming Controller coordinates VAD, tokenization, the LM,
  and the decoder with speculative generation and 14:1 text-context compression. Source:
  [arXiv:2507.16632](https://arxiv.org/abs/2507.16632) (StepFun Audio Team; code
  [github.com/stepfun-ai/Step-Audio2](https://github.com/stepfun-ai/Step-Audio2)).
- **Training-free vs fine-tuned:** SFT + reasoning-centric RL (weight-changing; **not** training-free,
  **not** frozen) — note this RL is the classic weight-updating kind, not the project's inference-time
  training-free RL.
- **Class + verdict:** the native audio LM itself is an **element** (fused, fine-tuned model, brain+
  sensor+actuator); *separately*, the paper states: *"Step-Audio 2 integrates retrieval-augmented
  generation (RAG) and is able to call external tools such as web search to mitigate hallucination and
  audio search to switch timbres"* — this tool/RAG layer is a second, independent **element**
  (a real connector to external, non-parametric knowledge), and it is specifically credited with
  reducing hallucination, i.e., the knowledge-grounding gain here is explicitly attributed to a new
  connector, not to better reasoning-prompting over the same frozen weights.
- **Fence tag:** single-session (tool calls are per-turn/per-query; no cross-session accumulation
  claimed).
- **Omni role:** **hybrid** for the core LM (brain+sensor+actuator fused); the RAG/web-search tool acts
  as an additional external **sensor** (real-world grounding) layered on top.
- **Delta vs archive:** NEW — a second, independent confirmation (alongside Unmute, #2) that tool/RAG
  connectors, not usage-pattern prompting, are what closes hallucination/knowledge gaps in native S2S
  systems.

### 7. Step-Audio-R1 / R1.5 — in the audio domain, chain-of-thought reasoning as a usage-pattern actively *hurts*; only weight-level RL fixed it
- **Recognized problem:** text/vision reasoning models benefit from extended chain-of-thought;
  Step-Audio-R1's own framing states the opposite holds for audio: *"a perplexing phenomenon persists
  in audio language models: they consistently perform better with minimal or no reasoning."*
- **Genealogy:** frozen audio encoder + audio adaptor + a high-capacity LLM, with a "Modality-Grounded
  Reasoning Distillation" (MGRD) framework combining self-distillation, SFT, and RL to teach the model
  *when and how* to reason over audio. Sources: [arXiv:2511.15848](https://arxiv.org/abs/2511.15848)
  (Step-Audio-R1) and [arXiv:2604.25719](https://arxiv.org/abs/2604.25719) (Step-Audio-R1.5 — corrected
  by verifier: this paper does **not** simply add RLHF on top of RLVR; its own framing is a critique of
  RLVR itself — *"[while] RLVR yields remarkable scores on standardized objective benchmarks, it
  systematically degrades the real-world conversational feel"* — and it describes Step-Audio-R1.5 as
  *"a paradigm shift toward Reinforcement Learning from Human Feedback (RLHF) in audio reasoning,"*
  i.e. moving away from over-reliance on verifiable rewards, not layering RLHF additively on top of
  RLVR).
- **Training-free vs fine-tuned:** explicitly **weight-changing** — RLVR/RLHF training, i.e. exactly the
  kind of RL this project's "training-free RL" framing is *not*; the whole point of these papers is that
  naive prompted/usage-pattern CoT reasoning is insufficient and must be trained into the weights. Note
  R1.5 adds a further nuance beyond R1's CoT-length finding: even weight-level RLVR training itself can
  produce a "verifiable reward trap" that hurts real-world quality despite benchmark gains, requiring a
  *different* weight-level intervention (RLHF) to fix — still consistent with the section's core point
  (usage-pattern-only levers don't reach the fix; only further weight-level training does), but the
  R1-vs-R1.5 mechanisms are not identical and should not be conflated.
- **Class + verdict:** this is a **negative result for usage-pattern-only levers, on the audio modality
  specifically** — extended reasoning as a pure inference-time usage pattern (more CoT text before the
  answer) is reported to actively *degrade* audio-task performance unless the capability to reason well
  over audio is separately trained in via RL. Read together with the project's main thesis, this
  strengthens (rather than weakens) the claim that usage patterns over a frozen model are bounded: here
  the usage pattern (CoT) doesn't even reach the frozen baseline, and only a weight-level change (which
  is out of scope for training-free RL) recovers/exceeds it.
- **Fence tag:** single-session.
- **Omni role:** hybrid (fused audio LLM does its own reasoning-then-answering).
- **Delta vs archive:** NEW, and a useful qualifier/negative for L4's "instruction/reasoning gap"
  problem — it shows at least one place where the gap is *not* closed by any documented inference-time
  usage-pattern lever, only by RL fine-tuning (out of this project's frozen-model scope).

### 8. Qwen2.5-Omni / Qwen3-Omni — Thinker-Talker gives an explicit brain/actuator split, with a built-in hook for tool-calling
- **Recognized problem:** unify text/image/audio/video perception with real-time streaming speech
  generation in one open model, without the Talker's speech decoding blocking or degrading the
  Thinker's reasoning.
- **Genealogy:** Qwen2.5-Omni's Thinker (a text-generating LLM) hands its hidden representations to a
  Talker (*"a dual-track autoregressive model"* that *"directly utilizes the hidden representations
  from the Thinker to produce audio tokens"*) — [arXiv:2503.20215](https://arxiv.org/abs/2503.20215).
  Qwen3-Omni upgrades both Thinker and Talker to MoE and replaces the Whisper encoder with AuT (Audio
  Transformer, trained from scratch on 20M hours of supervised audio), reaching open-source SOTA on
  32/36 audio and audio-visual benchmarks — [arXiv:2509.17765](https://arxiv.org/abs/2509.17765)
  (Qwen Team; code [github.com/QwenLM/Qwen3-Omni](https://github.com/QwenLM/Qwen3-Omni)).
  Separately, on tool-calling specifically: *"The Thinker-Talker architecture...lets external
  systems — including function calls — intervene between the two stages before speech synthesis
  begins."*
- **Training-free vs fine-tuned:** fully pretrained/fine-tuned end-to-end (both stages); **not**
  frozen.
- **Class + verdict:** **element** (a new pretrained model); architecturally notable is the explicit
  three-way split — AuT/Whisper encoder = **sensor**, Thinker = **brain** (reasoning, decides on tool
  calls), Talker = **actuator only** (speech rendering, no independent reasoning). This is the most
  explicit sensor/brain/actuator trichotomy documented anywhere in the lane, and the architecture is
  specifically designed so external tool-call logic sits at the brain/actuator seam rather than
  requiring a prompt trick.
- **Fence tag:** single-session (tool-calling and Qwen-Agent orchestration are per-session; no
  persistent cross-session memory element evidenced in the technical reports).
- **Omni role:** **explicit split** (sensor/brain/actuator), as above — the cleanest such case alongside
  MiniCPM-o (#9) and Kimi-Audio (#10).
  A quantified capability-gap data point relevant to this project's eval lanes: verified by verifier
  via WebSearch (uncited in the original draft — added here) —
  [arXiv:2605.15104](https://arxiv.org/abs/2605.15104) ("From Text to Voice: A Reproducible and
  Verifiable Framework for Evaluating Tool Calling LLM Agents") reports on its Confetti benchmark that
  *"Qwen3-Omni loses 1.8 points from clean text to direct voice (62.2 to 60.4), representing the
  smallest text-to-voice gap among the models tested"* (range 1.8–4.8 points across models) — i.e.,
  voice-modality tool-calling slightly underperforms the same model's text-modality tool-calling,
  a directly measured (if small, and comparatively the *best-in-class* small) perception/modality tax,
  distinct from a reasoning-capability tax.
- **Delta vs archive:** NEW (explicit brain/actuator architectural split + a measured modality-transfer
  tax on tool-use, both absent from the archive).

### 9. Kimi-Audio — continual pretraining from Qwen2.5-7B, hybrid tokenizer as the sensor bridge
- **Recognized problem:** unify audio understanding, generation, and conversation in one model trained
  at very large scale (13M+ audio hours).
- **Genealogy:** *"We initialize the audio LLM of Kimi-Audio from the pre-trained Qwen2.5 7B model and
  extend its vocabulary with semantic audio tokens and special tokens"* — a hybrid tokenizer combining
  discrete 12.5 Hz semantic tokens with continuous Whisper-derived acoustic features feeds the LLM;
  a chunk-wise flow-matching detokenizer renders audio. Source:
  [arXiv:2504.18425](https://arxiv.org/abs/2504.18425) (Kimi Team, Moonshot AI; code
  [github.com/MoonshotAI/Kimi-Audio](https://github.com/MoonshotAI/Kimi-Audio)).
- **Training-free vs fine-tuned:** continual pretraining + SFT on the LLM — weights are **modified**
  extensively, in contrast to Freeze-Omni's genealogically-similar "start from a pretrained text LLM"
  root that instead keeps it frozen. This is a second direct fork (alongside GLM-4-Voice vs. Freeze-Omni,
  #3/#4) of the same starting point (a strong pretrained text LLM) into two incompatible strategies.
- **Class + verdict:** **element** (new pretrained weights).
- **Fence tag:** single-session.
- **Omni role:** **explicit split** — hybrid tokenizer = sensor, audio LLM = brain, flow-matching
  detokenizer = actuator.
- **Delta vs archive:** NEW.

### 10. MiniCPM-o 4.5 — most explicit sensor/brain/actuator trichotomy, fully end-to-end differentiable
- **Recognized problem:** real-time full-duplex omni-modal interaction (simultaneous seeing, listening,
  speaking, without one stream blocking another) on a compact, deployable model.
- **Genealogy:** SigLip2 (vision sensor) + Whisper-medium (audio sensor) + Qwen3-8B (brain) + an
  interleaved speech-token decoder and a streaming flow-matching decoder built on CosyVoice2 (actuator),
  all **differentiably connected end-to-end** at the token level (~9B parameters total). Source:
  [arXiv:2604.27393](https://arxiv.org/abs/2604.27393) (OpenBMB; model:
  [huggingface.co/openbmb/MiniCPM-o-4_5](https://huggingface.co/openbmb/MiniCPM-o-4_5)); abstract
  confirms: *"With a total of 9B parameters, MiniCPM-o 4.5 ... can see, listen, and speak simultaneously
  in real-time."*
- **Training-free vs fine-tuned:** fully fine-tuned, end-to-end gradient propagation across every
  component — the explicit opposite of the freeze-and-bolt-on strategy (Freeze-Omni, #3).
  **Not frozen, not training-free.**
- **Class + verdict:** **element** (new integrated pretrained model); the vision+audio+LLM+speech
  four-component naming (sensor, sensor, brain, actuator) is the most explicit version of this
  decomposition anywhere in the survey, useful as a reference vocabulary case for the project's own
  "omni role" taxonomy.
- **Fence tag:** single-session.
- **Omni role:** **explicit split** (two sensors, one brain, one actuator).
- **Delta vs archive:** NEW.

### 11. Baichuan-Audio — multi-codebook discretization + independent audio head, two-stage pretraining
- **Recognized problem:** a unified, real-time, end-to-end speech-interaction framework combining
  semantic and acoustic fidelity.
- **Genealogy:** a Baichuan-Audio-Tokenizer (Whisper-encoder-derived + RVQ multi-codebook
  discretization, a sensor) feeding an audio LLM with an independent audio head, trained via a two-stage
  pretraining strategy, plus an audio decoder (actuator). Source:
  [arXiv:2502.17239](https://arxiv.org/abs/2502.17239) (Baichuan Inc.).
- **Training-free vs fine-tuned:** fine-tuned/pretrained (two-stage); **not frozen**.
- **Class + verdict:** **element** (new pretrained weights + tokenizer design); the multi-codebook
  discretization is a trained architectural choice (baked in at pretraining), not an inference-time
  usage pattern.
- **Fence tag:** single-session.
- **Omni role:** **hybrid** (fused model with a distinguishable tokenizer-sensor/decoder-actuator
  around a brain LLM).
- **Delta vs archive:** NEW.

### 12. VITA-Audio — a latency fix (MCTP) implemented as a trained element, not a training-free decoding trick
- **Recognized problem:** first-audio-token latency in autoregressive speech-LLMs (waiting a full
  forward pass, or more, before any audio streams out).
- **Genealogy:** a lightweight "Multiple Cross-modal Token Prediction" (MCTP) module — conceptually a
  speculative-decoding-style idea ported from the LLM inference-acceleration literature into speech —
  that predicts several audio tokens per forward pass; four-stage progressive training teaches the MCTP
  heads. Source: [arXiv:2505.03739](https://arxiv.org/abs/2505.03739) (NeurIPS 2025; code
  [github.com/VITA-MLLM/VITA-Audio](https://github.com/VITA-MLLM/VITA-Audio)). Confirmed: *"a
  lightweight Multiple Cross-modal Token Prediction (MCTP) module that efficiently generates multiple
  audio tokens within a single model forward pass"*, giving a *"3~5x"* inference speedup at 7B scale.
- **Training-free vs fine-tuned:** the MCTP heads are **trained** (progressive multi-stage); this is the
  key genealogical nuance — the same underlying idea (predict-multiple-tokens-per-step) exists in the
  text-LLM literature as a purely **training-free, usage-pattern** technique (plain speculative decoding
  with an off-the-shelf draft model, no new weights). VITA-Audio instead chose to bake the multi-token
  prediction capability into new trained weights (an **element**) rather than leave it as an inference-
  time usage pattern — evidence that, in the audio-token domain specifically, the field has found it
  necessary to move latency tricks from the usage-pattern column into the element column to get the
  reported 3-5x win.
- **Class + verdict:** **element** (trained acceleration module), with the explicit contrast to the
  training-free-usage-pattern version of the same idea noted above.
- **Fence tag:** single-session.
- **Omni role:** **hybrid**, with the MCTP module functioning as an accelerator woven into the brain's
  own decoding loop (not a separate sensor/actuator).
- **Delta vs archive:** NEW — a useful boundary case showing the element/usage-pattern line is a design
  *choice*, not a law of nature, for at least one specific technique (multi-token speculative
  prediction).

### 13. SLAM-Omni — timbre/content decoupling via architecture, and extreme training-data efficiency
- **Recognized problem:** cheap (15 GPU-hours-class), timbre-controllable voice interaction without
  separate large-scale TTS/ASR pretraining stages.
- **Genealogy:** semantic-token spoken-language modeling with speaker/timbre information explicitly
  **decoupled to a separate vocoder**, giving zero-shot voice control without retraining the LM; plus
  "historical text prompting" to compress multi-turn dialogue history. Source:
  [arXiv:2412.15649](https://arxiv.org/abs/2412.15649) (ACL 2025 Findings). Confirmed: *"SLAM-Omni
  achieves zero-shot timbre control by modeling spoken language with semantic tokens and decoupling
  speaker information to a vocoder"*, and *"requiring only 15 hours of training on 4 GPUs with limited
  data"*.
- **Training-free vs fine-tuned:** fine-tuned (single-stage, but still a real training run, just
  extremely data-efficient) — a second cross-domain instance of the "curated small data beats brute
  scale" pattern (alongside LLaMA-Omni2, #5), this time on the timbre-control problem rather than
  dialogue quality.
- **Class + verdict:** **element** — but architecturally notable for this project's own thesis: the
  content/speaker (semantic-token/timbre) **disentanglement** is achieved here via an architectural
  design choice (route speaker identity to the vocoder, keep the LM's tokens speaker-agnostic) rather
  than via any inference-time RL over embeddings. This is directly relevant prior art for W4's flagship
  goal (disentangling a frozen omni model's content/speaker/emotion embeddings without weight changes)
  — SLAM-Omni shows one way to get partial disentanglement, but only by baking the separation into the
  architecture/training, not by acting training-free on a frozen model's existing embedding space. Worth
  a cross-reference in W4 planning as a "what training-time disentanglement already buys you" baseline.
- **Fence tag:** single-session.
- **Omni role:** **hybrid**, with an explicit sensor(semantic tokenizer)/actuator(timbre-conditioned
  vocoder) split around the LM brain.
- **Delta vs archive:** NEW; flags a concrete cross-reference opportunity for W4 (disentanglement via
  training-time architecture vs. the project's training-free RL goal over a frozen model).

### 14. Ola — progressive modality-alignment curriculum ported from VLM training methodology, true bidirectional S2S
- **Recognized problem:** extend a strong image/text LLM to audio and video without the joint
  omni-modal alignment-data explosion of training all modalities together from scratch.
- **Genealogy:** a progressive training curriculum — starts image-text (VLM-domain root, **ported**),
  then adds speech (using video as, per the paper, *"a central bridge"* connecting language and audio),
  then video — plus a CosyVoice-based speech decoder for genuine bidirectional output (confirmed:
  *"Ola supports user-friendly real-time streaming decoding for texts and speeches thanks to the text
  detokenizer and the speech decoder,"* with *"a sentence-wise decoding solution for streaming speech
  generation"* and ASR performance of 3.1 WER on LibriSpeech / 6.41 on AIR-Bench). Source:
  [arXiv:2502.04328](https://arxiv.org/abs/2502.04328) (code
  [github.com/Ola-Omni/Ola](https://github.com/Ola-Omni/Ola)).
- **Training-free vs fine-tuned:** fully fine-tuned across all progressive stages; **not frozen**.
- **Class + verdict:** **element** (new integrated model); the *progressive-alignment curriculum
  ordering* itself is a **training-time methodology transfer from the VLM literature** (curriculum
  learning / progressive modality introduction) into omni-modal LLM construction — a genealogy point
  (origin-domain VLM, transfer status **ported**) distinct from, and orthogonal to, the
  element/usage-pattern axis, since it operates at pretraining time rather than inference time.
- **Fence tag:** single-session.
- **Omni role:** **hybrid**, with CosyVoice as an explicit actuator and audio/video encoders as sensors
  feeding a shared brain.
- **Delta vs archive:** NEW.

---

## Negatives and empty-measurement cells (first-class)

- **No system in this lane reports inference-time best-of-N, reward-guided decoding, or
  self-consistency reranking as its method for improving voice-agent capability.** All capability gains
  documented above come either from (a) new pretraining/fine-tuning (weight changes) or (b) new bolted-on
  connector elements (tool-calling, RAG) — never from a training-free usage-pattern lever applied to a
  frozen native-S2S checkpoint at inference time. This extends the archive's N1/N2 negative (no
  published pass@k or prompt-opt on any voice-agent benchmark) specifically into the native-S2S
  architecture literature: the gap is not merely unmeasured, it is architecturally unaddressed by the
  field so far.
- **Step-Audio-R1/R1.5 is the one documented case where a usage-pattern-shaped lever (chain-of-thought
  reasoning) was tried and *failed* on audio** (reported to hurt performance) **and the field's fix was
  weight-level RL, not a better prompt/role usage pattern** — this is a first-class negative for
  "usage-pattern over one frozen model" specifically in the audio/S2S modality, distinct from (and
  arguably stronger than) the archive's existing critic/verifier-prompt negative.
- **Partial fill of an empty cell:** most of this lane's systems (Moshi, GLM-4-Voice, Kimi-Audio,
  Qwen2.5-Omni, Step-Audio-2-mini/130B, MiniCPM-o-2.6, Baichuan-Omni, LLaMA-Omni2) *are* jointly
  evaluated on one of this project's owned benchmarks,
  **VoiceAssistant-Eval** ([arXiv:2509.22651](https://arxiv.org/abs/2509.22651), confirmed by direct
  fetch to include exactly these model variants) — but that benchmark measures listening/speaking/
  viewing QA-style capability, not verifiable tool-use pass@k. tau2-bench itself has an experimental
  voice/full-duplex extension
  ([sierra-research/tau2-bench, voice README](https://github.com/sierra-research/tau2-bench/blob/main/src/tau2/voice/README.md))
  but no result was found (search-budget-limited, not confirmed absent) showing any system in this
  lane's roster evaluated through tau2-bench's voice mode specifically — this remains an empty cell for
  verifiable, DB-state-checked, pass@k tool-use evaluation of native S2S models as of this survey.

---

## Synthesis against the main thesis

This lane's evidence is uniformly **CONFIRMS**: every genuine capability addition documented above —
speech I/O itself (element: encoder/decoder), tool-use/RAG (element: connector), even a latency
optimization (element: trained MCTP module in preference to a training-free speculative-decoding
usage pattern) — traces to a new-info **element**, never to a usage pattern over an unchanged, frozen
set of weights. The one place a pure usage-pattern lever (CoT reasoning) was tried in isolation
(Step-Audio-R1's stated starting condition) it *failed* until weight-level RL was added. The Freeze-Omni
/ GLM-4-Voice and Freeze-Omni / Kimi-Audio pairs additionally show that even among systems starting from
the *same* frozen text LLM, only the freeze-and-bolt-on family keeps the claim "speech ceiling = text
ceiling" architecturally provable — the fuse-and-retrain family gives up that guarantee for (sometimes
better, sometimes not — cf. LLaMA-Omni2 vs. GLM-4-Voice, claim #5) raw capability at large compute/data
cost.

---

## Verifier notes (adversarial pass, 2026-07-06)

**Spot-checked 15 cited sources** (WebFetch to the arXiv abstract/HTML page, GitHub repo, or org page;
plus one WebSearch to trace an uncited claim): Moshi (arXiv:2410.00037), Kyutai Unmute
(kyutai.org/unmute), Freeze-Omni (arXiv:2411.00774 + GitHub), GLM-4-Voice (arXiv:2412.02612 + GitHub +
HF tokenizer card), Step-Audio-R1 (arXiv:2511.15848), Step-Audio-R1.5 (arXiv:2604.25719, abstract +
PDF), Step-Audio 2 (arXiv:2507.16632), Qwen3-Omni (arXiv:2509.17765 abstract + HTML full text),
LLaMA-Omni2 (arXiv:2505.02625 + GitHub), Kimi-Audio (arXiv:2504.18425), VITA-Audio (arXiv:2505.03739),
VoiceAssistant-Eval (arXiv:2509.22651 HTML, Table 3), and tau2-bench's voice README. All arXiv IDs
resolved to the correct paper and title, including the two forward-dated 2026 entries
(arXiv:2604.25719, Step-Audio-R1.5, submitted April 2026; arXiv:2604.27393, MiniCPM-o 4.5, submitted
April 2026) — neither is invented; both exist and match the claims made about them.

**Fixed in this pass:**
1. **Wrong URL (claim #5, LLaMA-Omni2):** the source link pointed to `github.com/ictnlp/LLaMA-Omni`
   (the earlier, different v1 system) instead of `github.com/ictnlp/LLaMA-Omni2`. Corrected in place.
2. **Mischaracterized claim (claim #7, Step-Audio-R1.5):** the draft said R1.5 "adds RLHF ... on top of
   RLVR." The paper's actual framing is a critique of RLVR (a "verifiable reward trap" that "degrades
   the real-world conversational feel" despite good benchmark scores) and an explicit "paradigm shift
   toward RLHF" — i.e., moving away from RLVR-only training, not additively combining the two. Corrected
   in place with the exact quotes; the section's overall framework verdict (usage-pattern CoT failed,
   only weight-level training fixed it) still holds, since RLHF is also weight-changing, but the R1 vs.
   R1.5 technical stories are distinct and were previously conflated.
3. **Uncited-but-true claim (claim #8, Qwen3-Omni "Confetti" 1.8-point gap):** this number is real and
   accurately stated, but the draft supplied no source. It comes from a different paper than the two
   already cited for Qwen3-Omni — [arXiv:2605.15104](https://arxiv.org/abs/2605.15104) (May 2026, not
   the Qwen3-Omni technical report itself, which does not mention "Confetti" anywhere in its full HTML
   text). Citation added in place.

**Framework-verdict check (element vs. usage-pattern, new-info vs. read-out):** spot-checked all 14
per-claim verdicts against the "usage pattern over ONE frozen model = read-out" rule. All 14 element
verdicts are defensible: every one traces to either a new/continued-pretrained weight set or a
literal new connector (STT/TTS/tool-call glue in Unmute; RAG/web-search in Step-Audio 2), never to a
prompt/role/orchestration trick over an unmodified single checkpoint. The one edge case worth flagging
explicitly: Kyutai Unmute (#2) composes *three* already-existing frozen systems (Kyutai STT, an
off-the-shelf text LLM, Kyutai TTS) via a cascade plus tool-call glue code — this is defensibly called
an "element" only because the new integration code is what enables capabilities (hang-up-on-command,
live news lookup) that exist in none of the three components alone, not because any of the three
components' weights changed. Worth keeping in mind for W4/L4 as the closest analogue in this lane to a
"pure orchestration" case; the lane's own verdict text already flags this nuance ("matching the
framework's verifier-as-tool = a real element fork") and does not overclaim it as a trained element.

**Recency:** the task's window is 2025-01 to 2026-07. Four sources predate it: Moshi
(arXiv:2410.00037, Oct 2024), Freeze-Omni (arXiv:2411.00774, Nov 2024), GLM-4-Voice
(arXiv:2412.02612, Dec 2024), and SLAM-Omni's preprint (arXiv:2412.15649, Dec 2024, though its
ACL 2025 Findings publication is 2025). All four are foundational/heavily-cited precursor systems that
the rest of the lane's 2025-2026 systems are directly compared against or forked from (Freeze-Omni vs.
GLM-4-Voice vs. Kimi-Audio is a genealogical throughline the lane itself builds on) — excluding them
would remove necessary context rather than tighten scope. Flagged here rather than removed; if the
lane is meant to be strictly 2025+, these four should be marked as "included for genealogy, pre-window"
rather than silently included.

**Minor, non-blocking:** claim #4 (GLM-4-Voice) states the tokenizer is "fine-tuned from
Whisper-large-v3." Direct sources confirm the base is Whisper (GitHub README: "在 Whisper 的 Encoder
部分增加 Vector Quantization") but do not independently confirm the specific "-large-v3" variant in the
text checked (arXiv abstract says only "an ASR model"). Plausible but not independently pinned down by
this pass — not changed, flagged for anyone who wants to verify against the paper's implementation
section directly.

**Negatives/recency otherwise:** the "Negatives and empty-measurement cells" section is well-formed —
it states a real negative (no lane system uses inference-time best-of-N/reward-guided decoding/reranking
to improve voice-agent capability), a genuine documented failure of a usage-pattern lever
(Step-Audio-R1's CoT result), and an honestly-hedged empty cell (tau2-bench voice mode) rather than a
false "confirmed absent." The VoiceAssistant-Eval claim that exactly the 8 named model families are
evaluated was independently re-verified against the paper's Table 3 and is accurate (Freeze-Omni is
also evaluated there but not called out in the lane text — a harmless omission, not an error).
