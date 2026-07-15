---
title: Multimodal (Speech/Omni) Knowledge Systems — Post-2025.01 Survey & Baseline Alignment
date: 2026-07-07
stage: 1-argumentation
lane: knowledge-backbone
supersedes_extends: 2026-07-06-knowledge-backbone.md
method: Workflow fan-out (3 lanes × find → adversarial-verify → synthesize), 46 works → 38 unique
---

# Multimodal Knowledge Systems — Baseline Alignment (2025.01+)

Extends `2026-07-06-knowledge-backbone.md` (16 claims) into a paper-grade related-work with **dataset
+ metric alignment** against our local 28-dataset set. Produced by a bounded multi-agent workflow
(3 lanes: RAG-for-speech / audio-native knowledge / agentic voice knowledge; each find → adversarial
URL+data-obtainability verify → synthesize). 46 works found → **38 unique after dedup**.

## Three anchors (owner-set, hard constraints)

1. **Multimodal (speech/omni) knowledge systems only** — audio+text; no image (project boundary).
2. **Prefer overlap with our local on-disk datasets** — each work tagged with which local set it touches.
3. **Data-obtainability = admissibility gate.** `A` local-already / `B` public-obtainable / `C` numbers-only
   (citation-level, not reproducible) / `D` neither (excluded). **Only A/B are usable baselines.**

## Headline conclusions

- **24 admissible (A/B) baselines; only 1 hard-D excluded** (Speculative Interaction Agents 2605.13360 —
  voice is motivation only, evaluated on TEXT tool-calling; fails Anchor-1).
- **7 A-graded works map to a local dataset**: WavRAG→spoken-squad, BR-ASR→librispeech,
  Attention-Grounding→spoken-squad, VoxMind→voicebench(+mmsu sub), τ-Voice→tau2-bench,
  EVA-Bench→eva-bench, Audio-MultiChallenge→audiomc.
- **19 of 26 local datasets are EMPTY CELLS** — no admissible baseline touches them.
- **The whitespace the project's training-free-RL thesis must occupy** (two intersecting gaps):
  - `{audio-native ∩ training-free ∩ local-mapped}` = **EMPTY**. The only audio-native RAG mapping to a
    local set (WavRAG→spoken-squad) is **fine-tuned**; the training-free audio-native works (VAT-KG,
    M3KG-RAG, PlanRAG-Audio) map to no local QA set.
  - **No admissible, local-mapped, training-free METHOD baseline exists.** The A-graded training-free
    works (τ-Voice, EVA-Bench, Audio-MultiChallenge) are **evaluation harnesses** measuring frozen
    models, not methods that raise a baseline; the A-graded methods (WavRAG, BR-ASR, Attention-Grounding,
    VoxMind) are all fine-tuned/mixed.

## Alignment matrix (38 unique works, sorted A>B>C>D)

> Dedup collapsed WavRAG×4, MoshiRAG×3, Stream-RAG×2, PlanRAG-Audio×2, Enhancing-S2S×2, LA-RAG×2;
> grade conflicts reconciled and flagged (CONTESTED noted).

| work | lane | year | datasets | metrics | reported | training? | adm. | local map | usable |
|---|---|---|---|---|---|---|---|---|---|
| WavRAG (2502.14727) | audio-native RAG | 2025-02 | Spoken-SQuAD, SLUE-SQA-5, HotpotQA | R@k,NDCG,EM,FactScore | Spoken-SQuAD R@10=0.90; HotpotQA EM 0.40 vs text-RAG 0.31; ~10× faster | fine-tuned | **A** | spoken-squad | ✅ |
| BR-ASR (2505.19179) | contextual-ASR retrieval | 2025-05 | LibriSpeech clean/other | WER,B-WER,latency | B-WER 2.8/7.1% @2k bias, 45% rel↑; 20ms/q; 0.3/2.9% degr @200k | mixed | **A** | librispeech | ✅ |
| Attention-Grounding (2603.16292) | E2E SpeechLLM QA | 2026-03 | SQuAD/HotpotQA/MuSiQue (spoken) | F1/EM,halluc,latency | beats Whisper-v3+reranker, fewer halluc, ~62% latency↓ | fine-tuned | **A** | spoken-squad | ✅ |
| VoxMind (2604.15710) | agentic spoken-dialogue | 2026-04 | AgentChat(prop.),VoiceBench,MMSU-sub | tool acc,VoiceBench | task 34.9→74.6 (prop., citation-only); VoiceBench 64.21 vs 64.15 | fine-tuned | **A** | voicebench;mmsu(sub) | ✅ (VoiceBench cmp only) |
| τ-Voice (2603.13686) | voice tool-use eval | 2026-03 | τ-Voice = τ²-bench+duplex audio (278) | pass@1,latency,interrupt | pass@1 clean/real: xAI 51/38, OpenAI 49/35; GPT-5 text 85/85 | training-free (eval) | **A** | tau2-bench | ✅ |
| EVA-Bench (2605.13841) | enterprise voice-agent eval | 2026-05 | EVA-Bench 213 scenarios | EVA-A/X,pass@1/k | none clears 0.5 on both; cascade 0.28-0.58 vs S2S 0.82 | training-free (eval) | **A** | eva-bench | ✅ |
| Audio-MultiChallenge (2512.14865) | multi-turn memory eval | 2025-12 | 452 convs,1712 rubrics | rubric pass-rate | best Gemini-3-Pro 54.65%; fails on audio-native axes | training-free (eval) | **A** | audiomc | ✅ |
| SEAL (2502.02603) | speech-RAG embedding align | 2025-02 | CMTEB(pub),custom KB(priv) | Top-1/3,CMTEB,latency | CMTEB 65.95 vs 60.78; KB Top-1 86.36% (priv); ~50% latency↓ | fine-tuned | **B** | none | ✅ (weak) |
| Enhancing-S2S RAG (2505.00028) | S2S speech-QA RAG | 2025-05 | HotpotQA(TTS),RGB(zh) | Recall,cEM,F1 | HotpotQA gain but ~9% below cascade; RGB-zh large gain; ~4× faster | mixed | **B** | none | ✅ |
| MARS (2508.01166) | conversational LLM-ASR retrieval | 2025-08 | MLC-SLM (~1604h) | WER/CER | 1.5K h beats 179K-h top system | fine-tuned | **B** | none | ✅ |
| RAG-context-discovery ASR (2509.19567) | contextual-ASR | 2025-09 | TED-LIUMv3,Earnings21,SPGISpeech | WER | up to ~17% rel WER↓ (oracle 24.1%) | unknown | **B** | none | ✅ |
| RASST (2601.22777) | ST retrieval (simultaneous) | 2026-01 | ACL60/60,ESO,3 dirs | BLEU,term-acc | term up to ~40%; +3 BLEU | fine-tuned | **B** | none | ✅ (NOT covost2/fleurs) |
| SQuTR (2602.12783) | spoken-query retrieval robustness | 2026-02 | SQuTR 37,317 q (6 public sets) | Recall/nDCG vs SNR | degradation curves | benchmark | **B** | none | ✅ (testbed) |
| MoshiRAG (2604.12928) | full-duplex async RAG | 2026-04 | Llama/Web-Q,TriviaQA(spoken),HaluEval,OOD-math | LLM-judge,latency | Gemma-3-27B: Llama-Q 80.3, HaluEval 36.3 vs vanilla 10.5 | mixed | **B** (contested C) | none | ✅ (contested) |
| PlanRAG-Audio (2605.20414) | long-form audio planning-RAG | 2026-05 | LibriSQA,AMI,MSP-Podcast,VoxPopuli,AudioSet | ROUGE-L,MCQA,DER,F1 | reasoning↑, stable 10-540min | training-free | **B** | librispeech (LibriSQA-derived) | ✅ |
| iKnow-audio (EMNLP-2025.1759) | audio KG rerank | 2025-11 | ESC-50,UrbanSound8K,TUT2017,FSD50K,AudioSet,DCASE17 | zero-shot cls acc | consistent gains over CLAP ×6; code+AKG released | mixed | **B** | none | ✅ |
| VAT-KG (2506.21556) | audio-inclusive MMKG-RAG | 2025-06 | AudioCaps-QA,AVQA,VALOR,VCGPT | Model-as-Judge,human | Qwen2.5-Omni: AudioCaps-QA 51.30, AVQA 93.07 | **training-free** | **B** | none | ✅ |
| M3KG-RAG (2512.20136) | multi-hop MMKG-RAG | 2025-12 | AudioCaps-QA,VCGPT,VALOR | Model-as-Judge,win-rate | AudioCaps-QA 60.77 vs 51.30 (VAT-KG) | **training-free** | **B** | none | ✅ |
| AudioRAG+ (2511.01091) | text-to-AUDIO gen RAG | 2025-11 | AudioCaps,RiTTA-Count,AudioSet | FD,KL,IS,CLAP | TangoFlux-RAG: KL 1.20, CLAP 58.6% | fine-tuned | **B** | none | ✅ (tangential) |
| AuditoryBench++ (2509.17641) | auditory-knowledge probe | 2025-09 | AuditoryBench++ (pitch/animal/instrument) | per-cat acc | text-only LMs lack auditory commonsense; AIR-CoT↑ | mixed | **B** | none | ✅ |
| wav2graph (2408.04174) | speech→KG (genealogy root) | 2024-08 | speech-sourced KG (VietMed-style) | node/link F1 | LLM-embedding gains; code+data released | fine-tuned | **B** | none | ✅ (pre-2025 root) |
| Audio2Tool (2604.22821) | audio-native function-calling | 2026-04 | Audio2Tool ~30k q | Tool-Acc,EM,Slot-F1 | Qwen3-Omni-30B 92.4(T1)/74.7(T3)/41.7(T8) | training-free (eval) | **B** | none | ✅ (strongest non-local audio-native tool-use) |
| Full-Duplex-Bench-v3 (2604.04847) | full-duplex tool-use (real audio) | 2026-04 | FDB-v3 100 real recs | Tool-Sel-F1,Pass@1,latency | GPT-Realtime 0.60, Gemini-Live 0.54, Cascade 0.45 | training-free (eval) | **B** | none | ✅ (real audio) |
| From-Text-to-Voice tool eval (2605.15104) | voice tool-calling eval | 2026-05 | Confetti(313),When2Call(300)→TTS | AST-acc,F1,UTMOS,WER | Gemini-3.1-Flash-Live 70.4%, Qwen3-Omni 60.4% | training-free (eval) | **B** | none | ✅ (reproducible from TTS) |
| VoxRAG (2505.17326) | transcription-free spoken-QA | 2025-05 | custom 50-q (LLM-judge) | R@10,nDCG,ans 0-2 | R@10 0.34; weak POC | training-free | C | none | — |
| Stream-RAG (2510.02044) | streaming tool-use RAG | 2025-10 | AudioCRAG(1862 synth+618 human) | acc,latency | +200% rel (11.1→34.2); -20% tool latency | fine-tuned | C (contested B) | none | — (weights+human-audio unreleased) |
| CLSR (2511.09282) | contrastive lang-speech retrieval | 2025-11 | 4 unnamed cross-modal sets | retrieval,SQA acc | improved (body only); data unidentifiable | fine-tuned | C | none | — |
| Contextual-Bias Hotword+RL (2512.21828) | contextual-ASR + GRPO | 2025-12 | unspecified hotword sets | KER,sent-acc | KER↓ (no abstract numbers) | fine-tuned (GRPO) | C | none | — (on-thesis for RL, data unobtainable) |
| AudioRAG benchmark (2602.10656) | audio-reasoning RAG bench | 2026-02 | AudioRAG (new) | QA acc | SOTA LALMs struggle; release unconfirmed | mixed | C | none | — (adjacent mmau/mmar; →B if released) |
| LA-RAG (2602.14612) | structured event-DB RAG | 2026-02 | Home/Industrial-IoT(prop.),CASTELLA-QA | acc,latency,temporal-F1 | Home-IoT 76.88%; primary data Qualcomm-internal | training-free | C | none | — |
| CLAR (2603.25460) | contextual-ASR (CIF) | 2026-03 | unspecified | CER,B-WER | improves (no abstract numbers) | fine-tuned | C | none | — |
| VoiceAgentRAG (2603.02206) | voice-agent latency system | 2026-03 | paper-specific | QA acc,latency | latency↓ (no named data) | unknown | C | none | — |
| SpeechRAG (2412.16500) | audio-native RAG (genealogy root) | 2024-12 | spoken-QA (Amazon-internal) | retrieval,QA vs WER | beats cascade at high WER | mixed | C | none | — (root; data gated) |
| VoiceAgentBench (2510.07978) | agentic voice eval | 2025-10 | BFCL/API-Bank/AgentHarm+Indic | TS,TCS,PF,RR | EN PF: Whisper+Llama3-70B 60.6% | training-free (eval) | C | none | — (release unconfirmed; →B if released) |
| SHANKS (2510.06917) | simultaneous hear-and-think | 2025-10 | custom math-correction+tool dialogue | interrupt acc,tool | 56.9% tool calls pre-finish; +37.1% interrupt | training-free | C | none | — (on-thesis; no released bench) |
| OutboundEval (2510.21244) | outbound-call eval | 2025-10 | OutboundEval (6 domains) | task-exec+fluency | 12 LLMs; body only | training-free (eval) | C | none | — (weak Anchor-1) |
| EchoChain (2604.16456) | full-duplex state-tracking eval | 2026-04 | EchoChain overlapping-speech | state-update acc | failures -40.2% rel; no model >50% | training-free (eval) | C | none | — |
| Speculative Interaction Agents (2605.13360) | latency (TEXT-only) | 2026-05 | TEXT tool-calling benches | latency,acc | 1.3-2.2× speedup; voice=motivation only | mixed | **D** | none | ❌ EXCLUDED |

## Local-dataset coverage (7/26 covered; 19 EMPTY CELLS)

| local dataset | task | admissible (A/B) works | 
|---|---|---|
| librispeech | ASR | **BR-ASR** (A, WER/B-WER); PlanRAG-Audio (B, LibriSQA-derived, not raw ASR) |
| spoken-squad | spoken-QA | **WavRAG** (A); **Attention-Grounding** (A) |
| voicebench | spoken-QA+agentic | **VoxMind** (A, no-regression check) |
| mmsu | spoken-reasoning MCQ | VoxMind (A, WEAK — only via VoiceBench-MMSU sub) |
| audiomc | multi-turn | **Audio-MultiChallenge** (A — the work IS audiomc) |
| eva-bench | voice-agent | **EVA-Bench** (A — the work IS eva-bench) |
| tau2-bench | voice tool-use | **τ-Voice** (A — extends τ²-bench w/ duplex audio) |
| covost2, fleurs-r | ST/LID | **EMPTY** (RASST on ACL60/60, MARS on MLC-SLM) |
| crema-d, meld | SER+SID | **EMPTY** ← largest strategic gap (= W4 flagship target) |
| minds14, slurp, speech-massive | SLU | **EMPTY** |
| mmau-mini, mmar, air-bench, big-bench-audio | audio-reasoning | **EMPTY** (AudioRAG bench adjacent but C) |
| heysquad | extractive spoken-QA | **EMPTY** (sibling Spoken-SQuAD is best-covered) |
| uro-bench, vocalbench, vocalbench-zh | dialogue/ZH | **EMPTY** (ZH works SEAL/Enhancing-S2S don't map) |
| voiceassistant-eval, soulx-duplug | assistant/duplex | **EMPTY** |
| seed-tts-eval, aime24/25/26 | TTS/text-math | **EMPTY** |

## Key gaps (the training-free-RL whitespace)

1. **SER/SID (crema-d, meld) = ZERO baseline** — exactly the W4 disentanglement target (emotion/speaker).
   No surveyed knowledge system retrieves/reasons over emotion/speaker on our SER/SID sets.
2. **SLU intent/slot (minds14, slurp, speech-massive) = ZERO.** Entire lane uncovered.
3. **ST on our sets (covost2, fleurs-r) = ZERO** (RASST/MARS use other corpora).
4. **Audio-reasoning MCQ (mmau-mini, mmar, air-bench, big-bench-audio) = ZERO** admissible (AudioRAG bench C).
5. **ZH/bilingual dialogue (uro-bench, vocalbench-zh) = ZERO** despite ZH works existing.
6. **`{audio-native ∩ training-free ∩ local-mapped}` = EMPTY** (WavRAG is the only local-mapped
   audio-native and it is fine-tuned).
7. **No admissible, local-mapped, training-free METHOD baseline** — A-graded training-free = eval harnesses;
   A-graded methods = fine-tuned. **This is the project's whitespace.**
8. **RL-on-thesis gap** — the only retrieval+RL-reward work (Contextual-Bias Hotword+RL, GRPO) is C
   (unobtainable). No reproducible reward-guided training-free baseline to compare against.

## Metric alignment vs our four verifiable rewards

Our `common/src/speechrl_common/rl/` exposes four reward families: `asr_reward` (1−normWER),
`exact_match_reward` (normalized full-string equality; SQuAD-containment layered for open QA),
`retrieval_reward` (recall@k), `probe_reward` (linear-probe acc). Mapping:

- **Drops straight in**: WER on **librispeech** (BR-ASR) → `asr_reward`; EM/F1 on **spoken-squad**
  (WavRAG, Attention-Grounding, **via SQuAD-containment EM** — softer than strict equality) →
  `exact_match_reward`; MCQ/pass@1 on **voicebench/tau2-bench/eva-bench/mmsu** (VoxMind, τ-Voice,
  EVA-Bench) → `exact_match_reward`/pass@1 gate. Tool-use/agentic benches are the **best-aligned** non-QA class.
- **Partial**: retrieval-only (WavRAG R@10, SEAL Top-1/3, SQuTR, VoxRAG) → `retrieval_reward`, but nDCG/MRR
  and private-KB Top-k do not, and they score a RETRIEVER not the answer — not an end-to-end effect baseline.
- **Misaligned (needs a judge/rubric)**: VAT-KG/M3KG-RAG Model-as-Judge; **Audio-MultiChallenge rubric**
  (our only audiomc baseline needs 1712 rubrics + a judge); MoshiRAG LLM-judge; VocalBench. Cannot reduce
  to substring/MCQ/WER without loss.
- **Separate metric**: RASST BLEU (ST); `probe_reward` is the natural reward for SER/SID/attribute + iKnow-audio
  classification — but that lane has NO admissible local baseline, so the reward exists with nothing to compare to.

## Datasets to add (obtainable, not local) → see `docs/datasets.candidates.json`

Per owner: B-grade datasets that are obtainable but not on disk are queued for download (not added to the
frozen `datasets.lock.json`; kept in a separate candidates manifest for owner review + fetch). The
highest-value picks (fill an empty cell or enable an admissible-baseline comparison): SLUE-SQA-5, AudioCaps-QA,
Audio2Tool, AuditoryBench++, MLC-SLM, SQuTR, Full-Duplex-Bench-v3, ESC-50/FSD50K (audio-event knowledge).
See the candidates file for source + rationale + which gap each fills.

## Provenance

Workflow run `wf_bfd8ebb7-8d5` (7 agents, 0 errors, adversarial URL + obtainability verification per lane).
All 38 works cite 2025.01+ primary sources except wav2graph (2408) and SpeechRAG (2412), flagged as
genealogy roots. Stage-1 / hypothesis-grade per methodology.
