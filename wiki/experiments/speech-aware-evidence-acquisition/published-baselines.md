---
title: "Published baselines per carrier: speech-aware evidence acquisition"
study_slug: "speech-aware-evidence-acquisition"
source_surveys: "study repo docs/readiness/2026-08-07-*.md (R0.1, model-free)"
maintained: "living page — 'ours' rows filled in place after each probe's ledger row lands"
---

# Published baselines per carrier (living table)

Purpose: the **published numbers** extracted by the R0.1 survey, laid out as a comparison table by carrier.
After each small probe (study repo `docs/readiness/2026-08-07-r1-replan-reproduction-plan.md` P1–P2)
completes, the corresponding "ours" row is filled in place, and subsequent improvement work proceeds
against this table as its baseline surface.

Discipline: this page registers only summary values plus pointers; numeric authority lives in the study
repo receipts/MLflow and in each paper's original text. **Rows are not directly comparable across the
table** unless the protocol column matches — different papers use different front-end ASR, subsets and
scorers; an "ours" row is meaningful only against a comparison row sharing its protocol and sample.
Probe samples are always the discovery/dev split (split freeze receipt: discovery 44 / dev 10 /
confirmatory 115, study `docs/receipts/splits.json`).

Legend: `[abl]` = the difference is supported by an ablation/controlled comparison in the source paper;
`(t)` = obtained by training (outside our boundary, kept only as a structural-gap comparison);
**ours** rows start empty and carry a ledger row id when filled in.

## Comparability error budget (2026-08-09, measurement first; read before citing any ours number on this page)

When placing our WER alongside published numbers, **the error is not ±2% but the sum of the items below**;
the largest is sampling, and the most easily overlooked is the normalization convention.

| Item | Magnitude | Nature | Basis |
|---|---|---|---|
| Sampling (E-001 uses 10/125 calls) | **±2.5pp** | Random, the largest item | Measured per-call WER variance (SD≈3.6, SEM≈1.14) |
| Number-normalization convention | **1.3–1.8pp** | Systematic, against us | Measured: rescoring the same outputs with number expansion moves corpus-level WER 26.70%→24.93% (expanded to words) / 25.42% (collapsed to digits) |
| Aggregation (macro vs micro average) | 0.04pp | Negligible | Measured: 26.74% vs 26.70% |
| fstalign synonym transforms | Not measured, estimated <0.5pp | Systematic | The Earnings-21 paper reports an effect on roughly 0.3% of disputed tokens |
| Corpus difference (E-21 vs E-22) | Not quantified | Against us | Earnings-22's whole thesis is "accented speech is harder" |
| System class (dedicated ASR vs frozen omni + agentic loop) | Not quantifiable | — | — |

**Root cause**: this repository's frozen `normalize_text_v1` explicitly performs no number expansion
("no number expansion"), whereas the fstalign used by the Earnings-21/22 papers applies text-normalization
transforms (affecting roughly 5% of reference tokens, typically `2021 ↔ twenty twenty one`). The earnings
domain is number-dense and our core verbalizes numbers, so the frozen metric records **spelling-convention
differences** as recognition errors.

**Rules of use**: (1) this study's conclusions rest on **paired-arm comparisons at the same model and the
same protocol**, where only sampling limits them; (2) any comparison with published numbers must state the
table above; (3) when numeric comparability is needed, prefer the **same-metric calibration** below over
the paper numbers.

### Same-metric calibration: rescoring published systems with this repository's frozen scorer (2026-08-09)

The Earnings-21 release package ships locally with each system's **raw transcription outputs**
(`earnings21/output/{amazon,google,microsoft,rev,speechmatics,kaldi_org}`, `.nlp` format, isomorphic to the
reference). Rescoring them with **this repository's frozen `normalize_text_v1` + alignment**, over the same
10 calls as the R4 mini sample:

| System | Paper value (fstalign, all 44 calls) | This repository's metric (same 10 calls) | Difference |
|---|---|---|---|
| Amazon | 17.0% | **15.70%** | −1.3pp |
| Google | 17.8% | **16.36%** | −1.4pp |
| Microsoft | 15.8% | **17.95%** | +2.2pp |
| Speechmatics | 16.0% | **17.07%** | +1.1pp |

(Rev and Kaldi are not included: Rev's directory structure differs from the rest and Kaldi is in `.ctm`
format; 4 systems are enough to calibrate, and under the "take an approximate conclusion at the verification
step" policy this is not extended further.)

**Conclusion**: this repository's metric reproduces published numbers to within **±1.3–2.2pp** (which
already contains both the 10/44 sampling and the normalization sources). This repository's E-21 numbers
can therefore **be placed alongside published tables**, provided a ±2pp tooling-convention tolerance is
declared; that is far stronger than "ordinal comparison only". **Same-sample, same-metric target band:
15.70% (Amazon, best) – 17.95% (Microsoft).** The R4 no-context arm's output can be compared directly
against that band.

## earnings21 / earnings22 / conec (Family A)

| system / condition | protocol | metric | value | source |
|---|---|---|---|---|
| ConEC conventional ASR, no-bias floor | ConEC LREC-COLING 2024 | WER | 10.41 (bias conditions span 10.29–10.66; insensitive to aggregation) | ConEC paper |
| Siskos black-box ASR, no-context | Siskos EMNLP-F 2025, E21 | WER | 35.9 | arXiv:2509.19567 |
| Siskos + CB-RAG context `[abl]` | same as above | WER | 31.1 | same as above |
| Siskos + CB-LLM context `[abl]` | same as above | WER | 31.8 | same as above |
| Siskos + oracle context `[abl]` | same as above | WER | 29.7 | same as above |
| RECOVER correction (t? — LLM correction pipeline, claimed black-box) | RECOVER preprint, E21 among 5 sets | rel. E-WER ↓ / recall ↑ | 8–46% rel / up to +22pp | arXiv:2603.16411 (not peer-reviewed, no code) |
| **ours: SAEA-E-001 bare-core reference floor (e22 dev subset10, 10 calls)** | obs-agent-loop segmentation protocol (60s buffer, model segmentation + VAD snapping + bounded stepping), INT4 Qwen3-Omni, openJiuwen executor, frozen asr-wer | WER | **0.2674** (per call 0.2157–0.3252; 795 slices / 47,393 audio-s / 2.53 GPU-hours) | filled in 2026-08-09; ledger row SAEA-E-001; **comparison evidence**: the same model under the whole-call protocol produced only 2–106 words (retired), while after segmentation it produces 7,556–11,036 words |
| **ours: no-context / matched-ConEC / mismatched (R4=P2b=SAEA-E-002; T4 extension = ConEC bias-list entity-class injection)** | 3-arm, a frozen 10-of-44 mini subset of earnings21-discovery (sample-once receipt, manifest-bound); each of the three arms has 610 slices with exactly identical audio seconds (paired design) | WER (entity-level WER pending an owner-pinned wer_tags adapter) | running (2026-08-09) | the analysis convention was pre-registered before results were seen: paired exact Wilcoxon + median difference + bootstrap CI, unit = call |

## slurp (Family B)

| system / condition | protocol | metric | value | source |
|---|---|---|---|---|
| Multi-ASR + HerMiT pipeline (t) | SLURP EMNLP 2020 official | IC-comb / SLU-F1 | 76.68 / 69.53 | arXiv:2011.13205 |
| Best adapted pipeline (t) | same as above | same as above | 78.33 / 70.84 | same as above |
| gold-transcript NLU upper bound (t) | same as above | same as above | 84.84 / 78.19 | same as above |
| CTI E2E (t) | CTI 2021 | IC / SLU-F1 | 82.93 / 71.12 | arXiv:2104.07253 |
| SFT Qwen2-Audio-7B (t) | ICASSP 2026 | IC / SLU-F1 | 88.13 / 76.75 | arXiv:2509.15389 |
| UniverSLU (t) | NAACL 2024 | IC | ~90.3 (attributed via retrieval; re-verify before freezing) | arXiv:2310.02973 |
| zero-shot SF: ZS-Whisper-SLU → WHISMA (t) | respective papers | SLU-F1 | 50.0 → 63.3 (supervised reference 69.9) | arXiv:2408.16423 |
| AIR-Bench direct answering (8 systems, best Qwen-Audio-Chat) | AIR-Bench 1k subset, GPT-4 judge | acc | 77.8 (worst NExT-GPT 25.6) | arXiv:2402.07729 |
| AIR-Bench cascade Whisper+GPT-4 `[abl]` | same as above | acc | 87.7 | same as above |
| **ours: direct vs self-cascade (R3=P2a)** | AIR-Bench 200 paired questions, deterministic scoring | acc | — | to be filled in |
| **ours: prompt-only slot filling (T3, the plan P3 analogue track)** | official scorer, samples registered through the sample-once manifest | SLU-F1 | — (no precedent in the literature; the corresponding ZS line is 50.0→63.3) | to be filled in |

## speech-massive (Family B)

| system / condition | protocol | metric | value | source |
|---|---|---|---|---|
| Cascade Whisper+mT5, cross-lingual zero-shot (t) | Interspeech 2024 official | IC avg / slot-F1 avg | 69.10 / 43.15 | arXiv:2408.03900 |
| Cascade, full fine-tuning (t) | same as above | same as above | 83.04 / 61.21 | same as above |
| gold-NLU upper bound (full fine-tuning) (t) | same as above | IC avg | 86.73 | same as above |
| E2E Whisper FR (t) | same as above | IC (FR) | 85.87 | same as above |
| SFT Qwen2-Audio FR (t) | ICASSP 2026 | IC / SLU-F1 | 87.39 / 74.86 (metric definition ≠ slot-micro-F1) | arXiv:2509.15389 |
| **ours (if a probe is opened)** | — | — | — (prompt-only multilingual SLU is a gap in the literature) | — |

## minds14 (Family B — diagnostic carrier)

| system / condition | protocol | metric | value | source |
|---|---|---|---|---|
| LaBSE translate-to-EN + MLP (t) | Gerz 2021, 3-fold random 60/40 (**no canonical split**) | acc avg | 95.9 | arXiv:2104.08524 |
| MAEB embedding probe | MAEB 2026 | probe score | Qwen2-Audio 25.51 / Whisper-medium 48.30 | arXiv:2602.16008 |

## slue-sqa-5 / spoken-squad / heysquad (Family C)

| system / condition | protocol | metric | value | source |
|---|---|---|---|---|
| SLUE-SQA-5 pipeline-oracle: gold transcript + DeBERTa (t) | SLUE Phase-2 ACL 2023 | frame-F1 (test/verified) | 62.3 / 70.3 | arXiv:2212.10525 |
| SLUE-SQA-5 best real pipeline (NeMo ASR+DeBERTa) (t) | same as above | frame-F1 (test/verified) | 43.3 / 45.9 (w2v2 39.6/40.1; whisper 32.7/35.7) | same as above |
| SpeechDPR (t) | ICASSP 2024 | Top-20 retr. / OpenSQA frame-F1 | 19.73 / 0.558 (cascaded teacher-student 19.94-19.90 / 0.561-0.565; SpeechDPR is clearly ahead when WER>40% `[abl]`) | arXiv:2401.13463 |
| Spoken-SQuAD 2018 floor: best FusionNet (t) | Interspeech 2018, ASR WER 22.7 | EM / F1 | 46.51 / 60.06 (clean-text mean upper bound 64.41/74.54) | arXiv:1804.00320 |
| Su & Fung 2020 literature ceiling (t) | ICASSP 2020 | F1 | 77.67 | IEEE 9053979 |
| HeySQuAD fine-tuning (t) | arXiv:2304.13689 | relative gain | +12.51% (human-voice transcripts included in training) / +2.03% (evaluated on higher-quality transcripts) `[abl]`; absolute EM/F1 from the source table still to be recorded (optional) | same as at left |
| AudioBench direct-answering row (slue_p2_sqa5) | AudioBench, LLM-judge 0-100 | judge score | SALMONN 83.92; Qwen2-Audio-Inst 82.99; Qwen-Audio-Chat 80.05; WavLLM 76.12; **cascade Whisper+Llama3 76.12 — here direct answering > cascade (a counter-direction data point for closed-book document QA)**; the spoken_squad row is not in the paper's v4 table (leaderboard side; re-verify at freeze time) | arXiv:2406.16020 |
| **ours: AudioBench protocol rerun (A1, scorer replacement)** | sampling + pinned open-source judge | judge/EM-F1 | — | to be filled in |
| **ours: T1 SpeechDPR analogue (training-free retrieval)** | core transcript + pinned BM25, bounded pool (not proportionally comparable to the paper's full corpus) | Top-N / frame-F1 | — (directional comparison 19.73 / 0.558) | to be filled in |
| **ours: T2 SpeechRAG analogue (retrieval ladder closed-book/retrieved/oracle)** | core-transcribed passages + pinned retriever (spoken-squad) | EM/F1 | — (compared against the "no degradation" claim; doubles as the Family C SUPPLY sensitivity ladder) | to be filled in |

## ami-meeting-corpus (Family E)

| system / condition | protocol | metric | value | source |
|---|---|---|---|---|
| QMSum training baseline (t) | NAACL 2021 | ROUGE | values still to be extracted (archival only; the metric is insensitive to evidence `[abl]` MS-AMI) | Yale-LILY/QMSum |
| MeetingQA fine-tuned extractor (t) | ACL 2023 | span-F1 | 57.3 (human 84.6) | adobe/meetingqa |
| CMT-LLM (t) | Interspeech 2025 | WER (AMI SDM, 1k distractors) | 32.9 | arXiv:2506.12059 |
| PlanRAG-Audio | ACL-F 2026, no code released | ROUGE-L / DER (self-defined task) | cannot be independently scored | arXiv:2605.20414 |

## audio2tool (Family D)

| system | protocol | Tier1 | Tier3 multi-intent | Tier8 blending | source |
|---|---|---|---|---|---|
| **Qwen-3-Omni-30B (the same core) direct answering** | paper protocol, deterministic metric | 92.4 | 74.7 | 41.7 | arXiv:2604.22821 |
| Whisper-v3 + Gemma-27B cascade | same as above | 87.9 | — | 50.5 | same as above |
| **ours: GGUF runtime rerun (R1=P1)** | 50×8 tier sampling, reimplemented scorer | — | — | — | to be filled in (all tier columns) |

## voiceagentbench (Family D)

| system | protocol | EN PF avg | Indic PF avg | source |
|---|---|---|---|---|
| Whisper + Llama3-70B (t backend) | VAB official | 60.64 | 39.21 | arXiv:2510.07978 |
| Whisper + Gemma3-27B | same as above | 59.28 | 35.28 | same as above |
| KimiAudio-7B direct answering | same as above | 57.57 | 28.21 | same as above |
| Qwen2.5-Omni-7B direct answering | same as above | 1.70 (format collapse) | 0.29 | same as above |
| one-shot gain `[abl]` | ablation in the same paper | +10–17pp (complex tasks) | — | same as above |
| **ours: zero-shot vs one-shot (R5=P2c)** | 150 EN complex questions, paired | — | — | to be filled in |

## full-duplex-bench-v3 (adjacent to Family D)

| system | Pass@1 | self-correction Pass@1 | source |
|---|---|---|---|
| GPT-Realtime | 0.600 | 0.588 | arXiv:2604.04847 |
| Cascade Whisper→GPT-4o→TTS | 0.450 | 0.176 (counter-example `[abl]`) | same as above |

## voicebench / voiceassistant-eval / uro-bench / big-bench-audio (Family F)

| system / condition | protocol | metric | value | source |
|---|---|---|---|---|
| VoiceBench #1 Nemotron-3-Nano-Omni (t) | VoiceBench full suite | overall | 89.39 | official leaderboard |
| VoiceBench cascade Whisper-v3+GPT-4o | same as above | overall | 87.80 (rank 4) | same as above |
| GPT-4o-Audio | same as above | overall | 86.75 | same as above |
| Qwen2-Audio | same as above | overall | 55.80 | same as above |
| URO-Bench EN-basic cascade Whisper+GPT-4o | URO-Bench | overall | 89.33 | Ruiqi-Yan/URO-Bench |
| URO-Bench EN-basic best open-source E2E GLM-4-Voice (t) | same as above | overall | 69.09 | same as above |
| VoiceAssistant-Eval GPT-4o-Audio | VAE, gpt-oss-20b judge | listening / speaking | 39.78 / 51.26 | arXiv:2509.22651 |
| VoiceAssistant-Eval Qwen2.5-Omni-7B | same as above | listening / speaking / viewing | 33.56 / 41.27 / 34.27 | same as above |
| BBA GPT-4o text upper bound | BBA, Claude judge | acc | 92 | HF blog 2024-12 |
| BBA GPT-4o-Realtime speech direct answering `[abl]` | same as above | acc | 66 | same as above |
| BBA Whisper→GPT-4o cascade `[abl]` | same as above | acc | ≈ the text level | same as above |
| BBA Gemini-2.5 Native-Audio-Thinking (t) | same as above | acc | 92 (2025-10) | Artificial Analysis |
| **ours: BBA direct vs self-cascade (R2=P2a)** | 200 paired questions, pinned scoring | acc | — | to be filled in |
| **ours: VoiceBench deterministic subset (A2)** | MCQ/rule subset sampling | per-subset | — | to be filled in |

## P0 number-backfill list (the bulk was completed 2026-08-07)

Already added: SLUE-SQA-5 frame-F1 (including the oracle upper bound); the two levels of SpeechDPR
values; the Spoken-SQuAD 2018 floor; the HeySQuAD relative gain; the AudioBench slue_p2_sqa5 row.
Remaining (low priority, to be handled before freezing): re-verifying UniverSLU 90.3 against the source
table; the AudioBench spoken_squad leaderboard row; HeySQuAD absolute EM/F1; (optional) the QMSum ROUGE
archival values. The counter-direction data point that was found is already in the table: in the
AudioBench closed-book document-QA setting, direct answering > cascade, which together with the FDB-v3
self-correction counter-example is evidence that "cascading is not superior everywhere".

## Backfill rules

1. Land the study-repo exposure-ledger row and receipt first, then edit this page;
2. An "ours" row must state: the ledger row id, the sample size, the split role, the protocol hash short
   prefix, and the scorer (deterministic / pinned judge and its hash);
3. A result under a protocol different from a published row **starts a new row** and must never overwrite
   the comparison row;
4. This page is updated in place row by row; history is preserved through git.
