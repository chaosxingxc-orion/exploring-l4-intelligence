# Coverage & Kill Matrix — Stage-1A Survey v2

> **Coordinator-verified header (2026-07-14, Survey v2 round-1, wf_c6ed06f2).** Evidence-grade honesty: the workflow`s WebFetch was blocked, so per-paper `[FT]` tags in this file are workflow cite-checks via **WebSearch, not fulltext** — treat them as **SCOUT/ABSTRACT** unless listed here. **COORDINATOR-VERIFIED (personal WebSearch this session):** mbr-asr 2510.19471 (Jinnai, real), READ 2606.04680 (real), scaling-auditory 2503.23395 (Dang et al, real), AudioToolAgent 2510.02995 (Wijngaard et al, real, agent does NOT access audio → tool-orchestration not reward-guided selection), jia-SER 2602.03873 (real). **UNVERIFIED-CITATION (network NOT_RESOLVED this round):** 2512.10170, 2512.10403. Future-dated arXiv ids (2602–2606) are plausibly real (current month = 2026-07) but not all personally checked. Raw per-query trail: `wiki/survey/2026-07-14-search-query-log.jsonl` (305 queries). Kill-matrix vocab only; no `EMPTY` cells.
> Verdict vocabulary is fixed: **DIRECT_OCCUPIED** · **PARTIAL_ANCESTOR** · **ANALOGY_ONLY** · **UNDERSEARCHED** · **NO_DIRECT_MATCH_WITHIN_LOGGED_SCOPE**. **No cell is ever EMPTY.**
> Every UNDERSEARCHED cell explicitly states it *withstood the challenger hunt* (a targeted probe was run and found no direct occupant, but coverage was thin — distinct from NO_DIRECT_MATCH, where the probe was adequate).
> Per-cell headroom-existence tag: **HAS_HEADROOM** / **NO_HEADROOM** / **UNKNOWN**. Numbers tagged `[id — url]` or `[ours-directional]`.

Our on-disk tasks: **ASR** (librispeech/aishell/thchs) · **ST** (covost2/fleurs-r) · **SER** (crema-d/meld/esd/csemotions) · **SLU-intent** (minds14/slurp/speech-massive) · **spoken-QA/agent** (voicebench/spoken-squad/uro-bench/vocalbench/voiceassistant-eval/audiomc/eva-bench/tau2-bench/heysquad[gold-leak]) · **audio-understanding** (mmau-mini/mmar/air-bench/mmsu/big-bench-audio).

---

## Part 1 — Coverage grid: our-datasets × method-families

Cell = `VERDICT · headroom · [lead paper]`. Method families (columns):
- **M1** label-free text-scored N-best/MBR/BoN selection (I1)
- **M2** audio-grounded frozen-omni-native K-pool selection (I2)
- **M3** conformal/UQ/abstention selective prediction (I3-abstain)
- **M4** Goodhart / reward-overoptimization-aware selection (I3-goodhart)
- **M5** supply-conditional realization surface ρ(c)/H(c)/regret (I4)
- **M6** agentic reward-loop where reward changes next action (UMBRELLA)

| Task | M1 (I1) | M2 (I2) | M3 (I3-abstain) | M4 (I3-goodhart) | M5 (I4) | M6 (UMBRELLA) |
|---|---|---|---|---|---|---|
| **ASR** | **DIRECT_OCCUPIED** · HAS_HEADROOM · mbr-asr 2510.19471 (LS 4.2→3.3, oracle 1.3) | PARTIAL_ANCESTOR · HAS_HEADROOM · read-2606.04680 (external-TTS, ~70-85% oracle) | **DIRECT_OCCUPIED** · HAS_HEADROOM · ernez-conformal (WER<2%@80%) | NO_DIRECT_MATCH · UNKNOWN · (nearest mbr-metric-bias, text) | PARTIAL_ANCESTOR · HAS_HEADROOM · KIT-IWSLT 2606.04730 / novosad CTC-gap 2606.23306 | NO_DIRECT_MATCH · UNKNOWN · (agentic lane is audio-understanding-only) |
| **ST** | **DIRECT_OCCUPIED** · HAS_HEADROOM · mbr-asr 2510.19471 (FLEURS 8.24→11.68) / quan2005 | NO_DIRECT_MATCH · HAS_HEADROOM · (SpeechQE/HydraQE are trained scorers, not frozen selectors) | NO_DIRECT_MATCH · UNKNOWN · (SpeechQE=scorer; no ST conformal/abstain) | NO_DIRECT_MATCH · UNKNOWN · (mbr-metric-bias text-only) | PARTIAL_ANCESTOR · HAS_HEADROOM · KIT-IWSLT (ST oracle +2.0, little headroom) | NO_DIRECT_MATCH · UNKNOWN |
| **SER** | **DIRECT_OCCUPIED** · UNKNOWN · jia2602.03873 (CREMA-D 36.7→51.26 realized; no oracle-over-pool reported) | **DIRECT_OCCUPIED**† · UNKNOWN · jia2602.03873 (†verifier external GPT-4o; realized gain, no oracle) | **DIRECT_OCCUPIED** · HAS_HEADROOM · coverage-guaranteed-SER 2503.22712 (trained) | NO_DIRECT_MATCH · UNKNOWN | NO_DIRECT_MATCH · UNKNOWN · (no SER frozen-omni ρ surface) | UNDERSEARCHED · UNKNOWN · *withstood hunt* (no SER agentic paper surfaced) |
| **SLU-intent** | PARTIAL_ANCESTOR · HAS_HEADROOM · li2020-2001.05284 (oracle 27.04%, realized 14.29%, trained fusion) | NO_DIRECT_MATCH · UNKNOWN · (Caubriere trains a probe on one system) | PARTIAL_ANCESTOR · UNKNOWN · slu-clarify-ASRU21 / CICC 2403.18973 (text) | NO_DIRECT_MATCH · UNKNOWN | UNDERSEARCHED · UNKNOWN · *withstood hunt* (N-best-SLU exists but no ρ surface) | UNDERSEARCHED · UNKNOWN · *withstood hunt* |
| **spoken-QA/agent** | UNDERSEARCHED · UNKNOWN · *withstood hunt* (VoiceBench eval-only; Soft-SC weak in agentic) | PARTIAL_ANCESTOR · UNKNOWN · (WavRAG/AudioJudge audio-grounded but not answer-pool selection) | PARTIAL_ANCESTOR · UNKNOWN · walking-through-uncertainty 2604.25591 (AQUA-Bench P(True) 0.79; abstention-confidence, not an oracle) | ANALOGY_ONLY · UNKNOWN · inference-time-reward-hacking 2506.19248 (text) | NO_DIRECT_MATCH · UNKNOWN | PARTIAL_ANCESTOR · UNKNOWN · Audio-Mind 2605.28480 / Agent-Omni 2511.02834 / JitRL (text; agentic-accuracy, no oracle-over-pool) |
| **audio-understanding** | **DIRECT_OCCUPIED** · HAS_HEADROOM · scaling-auditory 2503.23395 / MUGEN 2603.09714 / Audio-CoT (MMAU 58.10%) | **DIRECT_OCCUPIED** · HAS_HEADROOM · scaling-auditory 2503.23395 (audio-grounded verifier +66.8%) | **DIRECT_OCCUPIED** · HAS_HEADROOM · walking-through-uncertainty 2604.25591 (MMAU AUROC 0.85) | ANALOGY_ONLY · UNKNOWN · (verifier-hacking 2508.02391, text 2603.15377) | NO_DIRECT_MATCH · UNKNOWN · (per-task acc only; no oracle/ρ surface) | **DIRECT_OCCUPIED**‡ · HAS_HEADROOM · AudioToolAgent 2510.02995 (MMAU 77.5) ‡occupies *system* not *object* |

**Coverage reading.** Rows ASR and audio-understanding are the most crowded (M1–M3 DIRECT). ST, SER, SLU-intent thin out to PARTIAL/NO_DIRECT past M1. **M4 (Goodhart-on-speech), M5 (frozen-omni ρ surface) are almost entirely NO_DIRECT_MATCH across all six tasks** — the clearest whitespace. M6 is DIRECT only for audio-understanding-QA and only as tool-orchestration systems, not reward-guided K-pool selection.

---

## Part 2 — Task × Method × Model KILL MATRIX

Model axis: **[F-omni?]** = does the challenger run on a *weight-frozen omni* core (Qwen-Omni / Audio-Flamingo / omni-LLM), and does it touch **our** primary model? Cell = `VERDICT · [F-omni? y/n/partial] · lead paper`.

### I1 — general label-free N-best/K-sample selector
| Task | Verdict · F-omni? · lead |
|---|---|
| ASR | DIRECT_OCCUPIED · n (frozen Whisper, text-scored) · mbr-asr-2510.19471 |
| ST | DIRECT_OCCUPIED · n · mbr-asr-2510.19471 / quan2005 |
| SER | DIRECT_OCCUPIED · y (frozen Qwen2-Audio) · jia2602.03873 |
| SLU-intent | PARTIAL_ANCESTOR · n (trained fusion) · li2020-2001.05284 |
| spoken-QA/agent | UNDERSEARCHED · n · *withstood hunt* — VoiceBench/SOVA eval-only, no frozen-omni K-pool selector logged |
| audio-understanding | DIRECT_OCCUPIED · y (frozen audio-LLMs) · scaling-auditory-2503.23395 / MUGEN-2603.09714 |

### I2 — audio-grounded frozen-omni-native selector (omni core's OWN signal at decision)
| Task | Verdict · F-omni? · lead |
|---|---|
| ASR | PARTIAL_ANCESTOR · n (external TTS scorer) · read-2606.04680 |
| ST | NO_DIRECT_MATCH · n · SpeechQE/HydraQE are trained scorers, not frozen selectors |
| SER | DIRECT_OCCUPIED† · y (frozen omni) · jia2602.03873 (†decision verifier external GPT-4o) |
| SLU-intent | NO_DIRECT_MATCH · n · Caubriere trains external probe |
| spoken-QA/agent | PARTIAL_ANCESTOR · partial · WavRAG-2502.14727 (audio retrieval, not pool selection) |
| audio-understanding | DIRECT_OCCUPIED · y · scaling-auditory-2503.23395 (audio-conditioned beam log-lik BoN) |
| **strict I2 (SAME frozen core = generator+scorer, as ρ surface)** | **NO_DIRECT_MATCH_WITHIN_LOGGED_SCOPE** · — · all occupants use external TTS / GPT-4o / trained reward model |

### I3 — constrained / abstaining / Goodhart-detecting selector
| Task | Verdict · F-omni? · lead |
|---|---|
| ASR | DIRECT_OCCUPIED · n (frozen wav2vec2) · ernez-conformal / I3-08-2407.21414 |
| ST | NO_DIRECT_MATCH · n · no ST conformal/abstain selector logged |
| SER | DIRECT_OCCUPIED · n (trained CNN, conformal) · coverage-guaranteed-SER-2503.22712 |
| SLU-intent | PARTIAL_ANCESTOR · n (text) · CICC-2403.18973 / slu-clarify-ASRU21 |
| spoken-QA/agent | PARTIAL_ANCESTOR · y · walking-through-uncertainty-2604.25591 (AQUA-Bench P(True) 0.79) |
| audio-understanding | DIRECT_OCCUPIED (abstain axis) · y · walking-through-uncertainty-2604.25591 (MMAU AUROC 0.85) |
| **Goodhart-detection ON SPEECH (any task)** | **NO_DIRECT_MATCH** · — · owned only in text (inference-time-reward-hacking-2506.19248) |
| **combined reward-guided + abstain + Goodhart on frozen omni** | **NO_DIRECT_MATCH** · — · no occupant |

### I4 — (supply c, selector) cross-matrix realization surface ρ(c)/H(c)/regret
| Task | Verdict · F-omni? · lead |
|---|---|
| ASR | PARTIAL_ANCESTOR · n · KIT-IWSLT-2606.04730 (per-task oracle+realized) / novosad-CTC-gap-2606.23306 |
| ST | PARTIAL_ANCESTOR · n · KIT-IWSLT-2606.04730 (ST oracle +2.0) |
| SER | NO_DIRECT_MATCH · — · no SER frozen-omni ρ surface |
| SLU-intent | UNDERSEARCHED · — · *withstood hunt* — N-best-SLU exists but never as ρ surface |
| spoken-QA/agent | NO_DIRECT_MATCH · — · per-task accuracy deltas only |
| audio-understanding | NO_DIRECT_MATCH · — · scaling-auditory 5×3×5 grid shows winner is model-dependent but computes no ρ/regret |
| **supply-TYPE stratification as design axis (any task)** | ANALOGY_ONLY · — · text/recsys only (ColdStart-2606.29947: 17-61% vs 5-7%; GenRM-2408.15240) |
| **frozen-omni [model×task] realization surface (whole I4)** | **NO_DIRECT_MATCH_WITHIN_LOGGED_SCOPE** · — · the survey's single clearest whitespace |

### UMBRELLA — training-free RL + frozen omni + agentic loop (reward changes next action)
| Task | Verdict · F-omni? · lead |
|---|---|
| ASR/ST/SER/SLU-intent | NO_DIRECT_MATCH · — · agentic lane targets audio-understanding QA + text only |
| spoken-QA/agent | PARTIAL_ANCESTOR · y · Audio-Mind-2605.28480 / Agent-Omni-2511.02834 (coordination/routing, no reward-guided K-pool) |
| audio-understanding | DIRECT_OCCUPIED (system) · y/partial · AudioToolAgent-2510.02995 (text orchestrator over frozen audio tools) |
| **loop-vs-one-shot: does the loop beat one-shot BoN?** | PARTIAL_ANCESTOR · n (text) · iad-2504.01931 (loop +3-4pts, front-loaded) — **pre-registered collapse risk** |
| **full intersection {training-free RL} ∩ {frozen OMNI} ∩ {advantage→next action}** | **NO_DIRECT_MATCH_WITHIN_LOGGED_SCOPE** · — · every component occupied separately, never jointly |

---

## Part 3 — Real kills vs genuinely-open (post-hunt ledger)

### DIRECT_OCCUPIED (real kills — do NOT claim as novelty)
1. **I1 on ASR/ST** — mbr-asr-2510.19471 (frozen, label-free, K=64, on our LibriSpeech/FLEURS/CoVoST; ~31% oracle realized). Bare I1 dead for ASR/ST.
2. **I1/I2 on SER** — jia2602.03873 (frozen Qwen2-Audio BoN/verifier on CREMA-D, +14.56pt).
3. **I1/I2 on audio-understanding** — scaling-auditory-2503.23395 (+9-150%), MUGEN-2603.09714 (+6.28-6.74%), Audio-CoT (MMAU 58.10%).
4. **I3-abstain on audio-understanding + frozen omni** — walking-through-uncertainty-2604.25591 (MMAU/MMAR/MMSU, AUROC 0.85). On our exact core+data.
5. **I3-conformal on ASR (frozen) and SER (trained)** — ernez-conformal-ASR; coverage-guaranteed-SER-2503.22712.
6. **I1/I2 on AAC (challenger/analogy corpus)** — slam-aac-2410.09503 (CLAP-Refine best-of-7). Not our datasets, but proves the audio-grounded selection *mechanism* is live.
7. **UMBRELLA as a SYSTEM on audio-understanding** — AudioToolAgent-2510.02995 (MMAU 77.5). Occupies the training-free+frozen+agentic *system*, not the reward-guided-selection *object*.
8. **The recovery/ρ metric itself (text)** — judge-bon-fail-2603.12520 (Recovery 21%→61%). The metric is prior art we build on.

### Genuinely OPEN after the challenger hunt (survivable ground)
- **I4** — the frozen-omni **supply-conditional [model×task] realization surface** ρ(c)/H(c)/regret. NO_DIRECT_MATCH in every lane. **Strongest single differentiator.**
- **Strict I2** — the **same frozen omni core** as both generator and audio-grounded scorer, characterized as a realization surface (all occupants use external TTS / GPT-4o / trained reward). NO_DIRECT_MATCH.
- **I3 combined** — reward-guided **+ abstaining + Goodhart-detecting** selector on frozen speech/omni with a ρ surface. Abstention is occupied; Goodhart-on-speech is NO_DIRECT_MATCH; the combination is NO_DIRECT_MATCH.
- **UMBRELLA intersection** — {training-free RL} ∩ {frozen OMNI at decision} ∩ {advantage→next action} jointly. NO_DIRECT_MATCH; must clear the IAD loop-vs-BoN bar on omni.
- **SER / SLU-intent frozen-omni reward-guided selection** — NO_DIRECT_MATCH / UNDERSEARCHED.
- **spoken-QA/agent frozen-omni label-free K-pool selection** — UNDERSEARCHED (VoiceBench eval-only).

### Headroom-existence honesty
- **HAS_HEADROOM confirmed** where an oracle/upper-bound is reported: ASR (mbr-asr oracle 1.3 vs realized 3.3; ma2024 5/10-best oracle 33.5/38.4% [2409.09554]), ST (KIT ST oracle +2.0 — small), audio-understanding (AuTAgent oracle 66.1 vs 50.0 [2602.13685]), contextual ASR (siskos ~69-77% oracle realized [2509.19567]).
- **Gain-demonstrated but oracle-UNMEASURED (headroom UNKNOWN)**: SER (jia CREMA-D +14.56pt *realized*, no oracle-over-pool); spoken-QA/agent M3/M6 (abstention-confidence / agentic-accuracy, no oracle). A realized gain is not an oracle ceiling — these are UNKNOWN, consistent with the M4/M5 + all-spoken-QA UNKNOWN rule below.
- **UNKNOWN headroom** dominates M4/M5 across tasks and all of spoken-QA/agent — because no paper computes an oracle-over-pool ceiling there. This UNKNOWN is itself the case for our ρ-measurement contribution.
- **No NO_HEADROOM cells asserted** — no logged paper demonstrates a task where the frozen-omni pool provably contains no better candidate; the closest is KIT's ST (+2.0 oracle, *small* but nonzero headroom).
