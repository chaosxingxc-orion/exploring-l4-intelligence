# SOTA Cards — Stage-1A Survey v2

> **Coordinator-verified header (2026-07-14, Survey v2 round-1, wf_c6ed06f2).** Evidence-grade honesty: the workflow`s WebFetch was blocked, so per-paper `[FT]` tags in this file are workflow cite-checks via **WebSearch, not fulltext** — treat them as **SCOUT/ABSTRACT** unless listed here. **COORDINATOR-VERIFIED (personal WebSearch this session):** mbr-asr 2510.19471 (Jinnai, real), READ 2606.04680 (real), scaling-auditory 2503.23395 (Dang et al, real), AudioToolAgent 2510.02995 (Wijngaard et al, real, agent does NOT access audio → tool-orchestration not reward-guided selection), jia-SER 2602.03873 (real). **UNVERIFIED-CITATION (network NOT_RESOLVED this round):** 2512.10170, 2512.10403. Future-dated arXiv ids (2602–2606) are plausibly real (current month = 2026-07) but not all personally checked. Raw per-query trail: `wiki/survey/2026-07-14-search-query-log.jsonl` (305 queries). Kill-matrix vocab only; no `EMPTY` cells.
> Every number tagged `[id — url]` or `[ours-directional]`. No invented numbers. Where no logged datapoint exists, the field reads **UNKNOWN** or **round-2 target** — never a guessed value.
> Card fields: **train-state** (frozen / partial / trained) · **params** · **K** (pool/samples) · **tools** · **info at decision** (audio? gold? external model?) · **cost** · **data** · **metric**.

**The four comparable frontiers** (so a gain is never compared across incomparable regimes):
- **F1 · frozen single-pass** — one weight-frozen forward, no selection.
- **F2 · frozen inference-time SOTA** — weight-frozen, label-free K-pool selection / reranking / abstention (OUR regime).
- **F3 · frozen agentic-with-tools SOTA** — weight-frozen core + external tools / evidence loop.
- **F4 · unrestricted task SOTA** — any regime incl. weight updates (fine-tune / RL / distillation).

---

## Card: ASR (librispeech / aishell / thchs)

| Frontier | train-state | params | K | tools | info@decision | cost | data | metric |
|---|---|---|---|---|---|---|---|---|
| **F1 frozen single-pass** | frozen | Whisper-large-v3 | 1 | none | audio only | 1 decode | LibriSpeech | **WER 4.2** (beam) [mbr-asr — 2510.19471] |
| **F2 frozen inference-time** | frozen | Whisper-lv3 + Llama-3 scorer | 64 | none | text hyps (no audio@dec) | O(N²) MBR | LibriSpeech | **WER 3.3** (MBR, oracle 1.3 → ~31% realized) [mbr-asr — 2510.19471]; READ audio-grounded: LS-clean 2.06→**1.91** [read — 2606.04680]; frozen InstructGPT rescoring **8.72 < oracle 9.78** on WSJ [tap-ger — 2309.15649] |
| **F3 frozen agentic-with-tools** | — | — | — | — | — | — | — | **round-2 target** — no frozen-agentic ASR card logged (agentic lane is audio-understanding-only) |
| **F4 unrestricted SOTA** | trained | LoRA-GER LLM | 5-10 | none | text N-best | train+infer | LibriSpeech/CHiME | GER **surpasses n-best reranking oracle** [hyporadise — 2309.15701]; ma2024 realized 7.7% WERR vs oracle 33.5-38.4% [2409.09554] |

**Headroom note:** oracle-over-pool = 1.3 WER vs realized 3.3 → **large residual (~31% realized) on frozen ASR** [mbr-asr — 2510.19471]. This is the flagship ρ gap our operator targets.

---

## Card: ST (covost2 / fleurs-r)

| Frontier | train-state | params | K | tools | info@decision | cost | data | metric |
|---|---|---|---|---|---|---|---|---|
| **F1 frozen single-pass** | frozen | Whisper family | 1 | none | audio only | 1 decode | FLEURS En-Ja | **BLEU 8.24** [mbr-asr — 2510.19471] |
| **F2 frozen inference-time** | frozen | Whisper + text utility | 64 | none | text hyps | O(N²) | FLEURS En-Ja / Ja-En | **BLEU 11.68 / 8.08** (MBR) [mbr-asr — 2510.19471]; quan2005 log-linear ASR+SMT rerank sig. BLEU gain [Interspeech'05] |
| **F3 frozen agentic-with-tools** | — | — | — | — | — | — | — | **round-2 target** — none logged |
| **F4 unrestricted SOTA** | fine-tuned | Qwen3-ASR backbone QE | scorer | none | audio+hyp | train | multi-pair | HydraQE ref-free QE seg-level **29.8 > gold-transcript CometKiwi 28.5** [hydraqe — 2606.08748]; SpeechQE E2E>cascaded [2410.21485] (QE **scorers**, not selectors) |

**Headroom note:** KIT reports ST oracle only **+2.0** across N-best [KIT-IWSLT — 2606.04730] → **HAS_HEADROOM but small**; realized-vs-oracle for frozen-omni ST is unmeasured (round-2).

---

## Card: SER (crema-d / meld / esd / csemotions)

| Frontier | train-state | params | K | tools | info@decision | cost | data | metric |
|---|---|---|---|---|---|---|---|---|
| **F1 frozen single-pass** | frozen | Qwen2-Audio-7B | 1 | none | audio only | 1 decode | CREMA-D | **acc 36.70** [jia — 2602.03873] |
| **F2 frozen inference-time** | frozen | Qwen2-Audio / Qwen2.5-Omni | 3-5 | ext GPT-4o verifier | audio + text (+ ext verifier) | K decodes | CREMA-D / IEMOCAP / MSP-Podcast | **CREMA-D 51.26** (ALM-v, +14.56pt); IEMOCAP 29.13→36.69; MSP 38.30→42.25 [jia — 2602.03873]; EMO-TTA training-free TTA gains on 6 OOD sets [2509.25495] |
| **F3 frozen agentic-with-tools** | — | — | — | — | — | — | — | **UNDERSEARCHED / round-2 target** — no SER agentic card surfaced (withstood hunt) |
| **F4 unrestricted SOTA** | trained | omni + RLVR | — | none | audio | train | emotion sets | R1-Omni (RLVR, weights change) [2503.05379]; conformal SER coverage≥1−α, acc ~40-45% [coverage-guaranteed-SER — 2503.22712] |

**Headroom note:** CREMA-D realized +14.56pt via frozen BoN/verifier [jia — 2602.03873]; **no oracle ceiling reported → ρ UNKNOWN**. SER frozen-omni ρ surface = NO_DIRECT_MATCH.

---

## Card: SLU-intent (minds14 / slurp / speech-massive)

| Frontier | train-state | params | K | tools | info@decision | cost | data | metric |
|---|---|---|---|---|---|---|---|---|
| **F1 frozen single-pass** | frozen | 1-best NLU pipeline | 1 | none | text (ASR 1-best) | 1 pass | commercial VA | baseline 1-best (relative-only) [li2020 — 2001.05284] |
| **F2 frozen inference-time** | — | — | — | — | — | — | — | **UNDERSEARCHED / round-2 target** — no *frozen* label-free SLU K-pool selector logged (withstood hunt) |
| **F3 frozen agentic-with-tools** | — | — | — | — | — | — | — | **round-2 target** — none logged |
| **F4 unrestricted SOTA** | trained | BiLSTM/HAM fusion | N=5 | none | ASR N-best + conf | train | 23-domain VA | oracle domain RErr **27.04%**, realized **14.29%** (~53%) [li2020 — 2001.05284]; HAM **+19% domain / +37% intent** [li2020-coling] |

**Headroom note:** oracle 27.04% vs realized 14.29% (trained fusion) [li2020 — 2001.05284] → **HAS_HEADROOM**, but on a trained integrator; frozen-omni intent selection = UNDERSEARCHED.

---

## Card: spoken-QA / dialogue / agent (voicebench / spoken-squad / uro-bench / vocalbench / tau2-bench / …)

| Frontier | train-state | params | K | tools | info@decision | cost | data | metric |
|---|---|---|---|---|---|---|---|---|
| **F1 frozen single-pass** | frozen | Qwen2.5-Omni | 1 | none | audio only | 1 decode | VoiceBench / MMAU | Qwen2.5-Omni **VoiceBench 74.12 / MMAU 71.5** [ours-directional, per kill-I4 lane note] |
| **F2 frozen inference-time** | — | — | — | — | — | — | — | **UNDERSEARCHED / round-2 target** — VoiceBench/SOVA are eval-only; Soft-SC reports self-consistency weak in agentic settings (withstood hunt) |
| **F3 frozen agentic-with-tools** | frozen | Qwen3.5-Omni + planner | ≤15 steps | 38 tools | audio + evidence log | multi-step | MMAR / MSU-Bench | Audio-Mind **MMAR 80.40** (vs 78.90), MSU-Bench 0.828 [audio-mind — 2605.28480]; Agent-Omni test-time coordination MMAU 73.20 [2511.02834]; JitRL (text) tau2/WebArena SOTA-among-training-free [2601.18510] |
| **F4 unrestricted SOTA** | trained | Qwen-Omni + RL | — | varies | audio | train | MMAU family | Omni-R1 **MMAU 75.3** [ours-directional, per kill-I4 note]; AQA-TTRL test-time GRPO +4.42%/+11.04% [2510.05478] |

**Headroom note:** spoken-QA/agent frozen inference-time selection is the **thinnest cell** — F2 largely empty; ρ UNKNOWN. High-value round-2 target on our exact benchmarks.

---

## Card: audio-understanding (mmau-mini / mmar / air-bench / mmsu / big-bench-audio)

| Frontier | train-state | params | K | tools | info@decision | cost | data | metric |
|---|---|---|---|---|---|---|---|---|
| **F1 frozen single-pass** | frozen | Qwen2-Audio / Audio-Flamingo-2 | 1 | none | audio only | 1 decode | MMAU / custom | Audio-Flamingo-2 baseline **40.0**; Qwen2-Audio 36.7 [scaling-auditory — 2503.23395]; Audio-CoT MMAU 58.10% w/ SC+CoT [2501.07246] |
| **F2 frozen inference-time** | frozen | frozen audio-LLMs | 3-11 | ext verifier (some) | audio + text | K decodes | MMAU / MMAR / MMSU / custom | scaling-auditory **+9-150%** (Qwen2-Audio +36.2%, Audio-Flamingo-2 +66.8%) [2503.23395]; MUGEN APSC **+6.28-6.74%** (Gemini-3-pro) [2603.09714]; Walking-Uncertainty AURAC **0.73-0.92** [2604.25591] |
| **F3 frozen agentic-with-tools** | frozen | text orchestrator + frozen audio tools | multi-tool | many | text tool-outputs (+audio in some) | multi-step | MMAU / MMAR / MMAU-Pro | AudioToolAgent **MMAU 77.50 / MMAR 77.00 / MMAU-Pro 61.90** [2510.02995]; Audio-Mind MMAR 80.40 [2605.28480]; EChO-Agent (Qwen3-Omni) MMAR 71.0, +2.3 [2606.15141] |
| **F4 unrestricted SOTA** | trained | Qwen2.5-Omni + test-time RL | 64 (pseudo) | none | audio | test-time train | MMAU / MMAR / MMSU | AQA-TTRL Qwen2.5-Omni-7B **+4.42%**, 3B **+11.04%** [2510.05478]; AuTAgent trained tool-policy realizes ~26-61% of oracle 66.1 vs 50.0 [2602.13685] |

**Headroom note:** AuTAgent gives the cleanest in-domain ceiling — **oracle 66.1 vs baseline 50.0 (16.1-pt tool-selection headroom)**, realized ~26-61% [2602.13685]. But this is *tool-selection* headroom on a trained policy; a **frozen-omni K-pool oracle/ρ for audio-understanding is unmeasured** (round-2).

---

## Cross-card synthesis

- **F2 (our regime) is populated for ASR, ST, SER, audio-understanding but EMPTY/UNDERSEARCHED for SLU-intent and spoken-QA/agent** — the two thinnest F2 cells are exactly where a first frozen-omni-selection result would be least contested.
- **No task has a logged F3 frozen-agentic card outside audio-understanding** — agentic + frozen-omni is concentrated on MMAU/MMAR.
- **Oracle ceilings exist for ASR (1.3 WER), SLU (27.04% RErr), audio-understanding (66.1 tool), contextual-ASR (~69-77% realized) but NOT for frozen-omni SER/ST/spoken-QA** — so a per-cell **oracle-over-pool + ρ measurement on the frozen-omni matrix is unclaimed** and is the survey's recommended Stage-1A deliverable.
- **The comparison discipline that must be enforced:** never report an F2 gain against an F4 baseline (e.g., don't compare our frozen selection to AQA-TTRL's weight-updated numbers) and never score realized quality with the same metric used as the selection utility [freitag2022 — 2111.09388; mbr-metric-bias — 2411.03524].
