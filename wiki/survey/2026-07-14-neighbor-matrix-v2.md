# Neighbor Matrix — Stage-1A Survey v2

> **Coordinator-verified header (2026-07-14, Survey v2 round-1, wf_c6ed06f2).** Evidence-grade honesty: the workflow`s WebFetch was blocked, so per-paper `[FT]` tags in this file are workflow cite-checks via **WebSearch, not fulltext** — treat them as **SCOUT/ABSTRACT** unless listed here. **COORDINATOR-VERIFIED (personal WebSearch this session):** mbr-asr 2510.19471 (Jinnai, real), READ 2606.04680 (real), scaling-auditory 2503.23395 (Dang et al, real), AudioToolAgent 2510.02995 (Wijngaard et al, real, agent does NOT access audio → tool-orchestration not reward-guided selection), jia-SER 2602.03873 (real). **UNVERIFIED-CITATION (network NOT_RESOLVED this round):** 2512.10170, 2512.10403. Future-dated arXiv ids (2602–2606) are plausibly real (current month = 2026-07) but not all personally checked. Raw per-query trail: `wiki/survey/2026-07-14-search-query-log.jsonl` (305 queries). Kill-matrix vocab only; no `EMPTY` cells.
> Every number tagged `[paper — url]` or `[ours-directional]`. No invented numbers.
> Cite-check failures are flagged **UNVERIFIED-CITATION** inline (2 total: `semantic-confidence-aac-2512.10170`, `brace-2512.10403` — both `NOT_RESOLVED_THIS_ROUND`, network/socket failure, not confirmed fabrication).

**Our research object (recap).** Weight-frozen, label-free, reward-guided **inference-time selection over K-sample pools** on a frozen speech/omni core (Qwen3-Omni-30B Q8_0 GGUF primary; nemotron3-nano-omni; omni-embed-nemotron), studied as a **supply-conditional selection operator's realization surface** — ρ(c) / H(c) / regret across the frozen-omni **[model × task]** matrix.
Candidate identities: **I1** general label-free N-best selector · **I2** audio-grounded frozen-omni-native selector · **I3** constrained/abstaining/Goodhart-detecting selector · **I4** (supply c, selector) pair / cross-matrix realization surface · **UMBRELLA** training-free RL + frozen omni + agentic loop.

---

## Section A — Ontology table, grouped by lane

Columns: **id** · **venue/yr** · **model_state** · **operator** · **audio@dec** · **gold@inf** · **train** · **our-dataset match** · **kills** · **strength** · **grade**.
Grade key: FT = FULLTEXT_VERIFIED · AB = ABSTRACT_VERIFIED · SC = SCOUT.
Cross-lane duplicates carry a `↔` note; canonical row is the highest-grade appearance.

### Lane 1 — ser-selection-abstention (7 rows)
| id | venue/yr | model | operator | audio@dec | gold@inf | train | our-data | kills | str | grade |
|---|---|---|---|---|---|---|---|---|---|---|
| sridhar2019reject | Interspeech'19 | trained | reject-option over trained DNN posterior | y | n | y | — | I3 | PARTIAL | AB |
| chou2023calibration | Interspeech'23 | trained | post-hoc ECE calibration (scorer only) | y | n | y | — | I3 | ANALOGY | AB |
| schrufer2024areyousure | Interspeech'24 | trained | UQ abstention / OOD-fault detection | y | n | y | — | I3 | PARTIAL | AB |
| coverageguaranteed2025conformalSER (2503.22712) | arXiv'25/EAAI'25 | trained | conformal prediction sets, coverage≥1−α | y | **y** | y | — | I3 | PARTIAL | AB ↔L13 |
| jia2602decodingambiguous (2602.03873) | arXiv'25/26 | **frozen** | test-time BoN/W-BoN/ALM-verifier over K samples | y | n | n | **crema-d** | I1,I2 | **DIRECT** | FT |
| emotta2025 (2509.25495) | arXiv'25 | frozen | training-free TTA (EM stats + CLAP/gen fusion) | y | n | n | — | I2,I3 | PARTIAL | AB |
| mmcalibration2024erc | ACM MM'24 | trained | multimodal ERC calibration | unclear | n | y | **meld** | I3 | ANALOGY | SC |

### Lane 2 — slu-nbest-reject (7 rows)
| id | venue/yr | model | operator | audio@dec | gold@inf | train | our-data | kills | str | grade |
|---|---|---|---|---|---|---|---|---|---|---|
| li2020-slu-exploit-nbest (2001.05284) | arXiv'20 | trained | trained N-best fusion (oracle 27.04%, realized 14.29%) | n | n | y | — (slurp/minds14 analogue) | I1 | PARTIAL | FT |
| li2020-coling-mtl-nbest-ham | COLING'20 | trained | HAM N-best integration + MTL | n | n | y | — | I1 | PARTIAL | AB |
| caubriere2020-slu-concept-confidence | Interspeech'20 | mixed | trained probe on frozen CTC-SLU internals → reject | y | n | partial | — | I2,I3 | PARTIAL | AB |
| slu-clarify-asru2021 (2109.12451) | ASRU'21 | trained | trained abstain-to-clarify over hyp pool | n | n | y | — | I3 | PARTIAL | AB |
| stengeleskin2023-didyoumean (2303.16857) | EMNLP'23 | mixed | label-free seq-confidence risk-coverage over frozen parser | n | n | partial | — | I3 | PARTIAL | FT |
| dong2018-confidence-neural-parsing | ACL'18 | trained | post-hoc uncertainty → reject (text) | n | n | partial | — | I3 | ANALOGY | AB |
| morbini2012-rerank-speech-classification | IEEE SLT'12 | trained | learned reranker over multi-ASR k-best | n | n | y | — | I1 | PARTIAL | SC |

### Lane 3 — st-rerank-qe (8 rows)
| id | venue/yr | model | operator | audio@dec | gold@inf | train | our-data | kills | str | grade |
|---|---|---|---|---|---|---|---|---|---|---|
| quan2005-integrated-nbest-slt | Interspeech'05 | frozen | log-linear ASR+SMT N-best reweight | y | n | partial | covost2,fleurs-r | I1 | DIRECT | AB |
| ng2015-2016-slt-qe-kbest | IS'15/ICASSP'16 | mixed | trained QE reranker (~117 feats, +0.80 BLEU) | y | n | y | covost2,fleurs-r | I1 | PARTIAL | AB |
| speechqe-han2024-emnlp (2410.21485) | EMNLP'24 | fine-tuned | audio-grounded QE **scorer** (not selector) | y | n | y | covost2,fleurs-r | I2 | PARTIAL | AB |
| hydraqe-iwslt2026 (2606.08748) | IWSLT'26 | fine-tuned | audio-grounded QE metric (29.8 vs CometKiwi 28.5) | y | n | y | covost2,fleurs-r | I2 | PARTIAL | AB |
| freitag2022-mbr-neural-metrics (2111.09388) | TACL'22 | frozen | MBR over K frozen-NMT samples (text) | n | n | n | — | I1 | DIRECT | AB |
| mbr-metric-bias-wmt2024 (2411.03524) | WMT'24 | frozen | metric-bias/Goodhart study + ensemble MBR (text) | n | n | n | — | I3 | PARTIAL | AB |
| fernandes2022-quality-aware-decoding (2205.00978) | NAACL'22 | mixed | QE-rerank + MBR framework (text) | n | n | partial | — | I1 | DIRECT | AB |
| qe-rerank-doclevel-2025 (2510.08870) | arXiv'25 | frozen | QE-rerank N=32, +5 BLEURT-20 (text) | n | n | n | — | I1 | ANALOGY | SC |

### Lane 4 — aac-captioning-select (8 rows) — *challenger/analogy lane; AudioCaps/Clotho NOT in our on-disk set*
| id | venue/yr | model | operator | audio@dec | gold@inf | train | our-data | kills | str | grade |
|---|---|---|---|---|---|---|---|---|---|---|
| slam-aac-2410.09503 | ICASSP'25 | mixed | CLAP-Refine best-of-7 (frozen CLAP cosine) | y | n | partial | — | I1,I2 | DIRECT | FT |
| enclap-aux-retrieval-2409.01160 | DCASE'24 | mixed | nucleus-30 + CLAP + log-lik rerank | y | n | partial | — | I1,I2 | DIRECT | FT |
| enclap-plusplus-2409.01201 | DCASE'24 | mixed | nucleus-30 hybrid rerank | y | n | partial | — | I1,I2 | PARTIAL | FT |
| merl-finegrained-aac-2309.17352 | ICASSP'24 | mixed | nucleus + likelihood/audio-sim hybrid rerank | y | n | partial | — | I1,I2 | PARTIAL | SC |
| **semantic-confidence-aac-2512.10170** | arXiv'25 | fine-tuned | trained confidence head + conf-guided beam | y | n | y | — | I3 | PARTIAL | **UNVERIFIED-CITATION** |
| mace-2411.00321 | ICASSP'25 | frozen | frozen audio-grounded eval metric (uses refs) | y | **y** | n | — | I2 | ANALOGY | AB |
| **brace-2512.10403** | NeurIPS'25 | frozen | ref-free scorer reliability benchmark | y | n | n | — | I3 | ANALOGY | **UNVERIFIED-CITATION** |
| caf-score-2603.19615 | arXiv'26 | frozen | frozen CLAP+LALM ref-free scorer | y | n | n | — | I2 | ANALOGY | AB |

### Lane 5 — audio-understanding-ttc (6 rows)
| id | venue/yr | model | operator | audio@dec | gold@inf | train | our-data | kills | str | grade |
|---|---|---|---|---|---|---|---|---|---|---|
| scaling-auditory-cognition-2025 (2503.23395) | arXiv'25 | **frozen** | majority + BS-W + audio-grounded LLM-verifier over K | y | n | n | — (custom cognition set) | I1,I2 | **DIRECT** | FT ↔L6,7,11,12,15 |
| mugen-multiaudio-2026 (2603.09714) | arXiv'26 | frozen | audio-permutational self-consistency K=10 | y | n | n | — | I1,I2 | DIRECT | FT |
| aqa-ttrl-2025 (2510.05478) | arXiv'25 | **trained** | maj-vote pseudo-label → GRPO weight update | y | n | y | mmau-mini,mmar,mmsu | I1,UMB | PARTIAL | AB ↔L6,12 |
| walking-through-uncertainty-2026 (2604.25591) | arXiv'26 | **frozen** | semantic-entropy / P(True) selective prediction | y | n | n | **mmau-mini,mmar,mmsu** | I3 | **DIRECT** | FT ↔L9,13 |
| audio-mind-agentic-2026 (2605.28480) | arXiv'26 | frozen | planner tool-routing / re-listen (38 tools, ≤15 steps) | y | n | n | mmar,mmsu | UMB | PARTIAL | FT ↔L10 |
| audio-cot-2025 (2501.07246) | arXiv'25 | frozen | 5-sample CoT self-consistency (MMAU 58.10%) | y | n | n | mmau-mini | I1 | PARTIAL | SC |

### Lane 6 — audio-judge-multi (8 rows)
| id | venue/yr | model | operator | audio@dec | gold@inf | train | our-data | kills | str | grade |
|---|---|---|---|---|---|---|---|---|---|---|
| AudioJudge-EACL2026 (2507.12705) | EACL'26 | frozen | prompted frozen audio-LLM pairwise judge (gen quality) | y | n | n | — | I2 | PARTIAL | FT |
| SpeakerSleuth-ACL2026 (2601.04029) | ACL'26 | **frozen** | frozen LALM ranks K=3 acoustic variants — **benchmarks Qwen3-Omni-30B** | y | n | n | — | I2 | PARTIAL | FT |
| AQA-TTRL-2510.05478 | arXiv'25 | trained | test-time GRPO (weights change) | y | n | y | mmau/mmar/mmsu | UMB,I1 | PARTIAL | FT ↔L5,12 |
| JudgeBoN-Recovery-2603.12520 | arXiv'26 | frozen | **defines Recovery = ρ** (text best-of-N) | n | n | n | — | I1,I4 | ANALOGY | FT ↔L11 |
| AuditoryTTC-2503.23395 | arXiv'25 | frozen | (= scaling-auditory-cognition) | y | n | n | — | I1,I2 | DIRECT | FT ↔L5 |
| SpeakingStyleJudge-2506.05984 | arXiv'25/EMNLP'25 | frozen | frozen audio judge on speaking style (≈human agreement) | y | n | n | — | I2 | PARTIAL | AB |
| ParaPairAudioBench-IS2026 (2606.24648) | Interspeech'26 | frozen | paralinguistic pairwise judge; diagnoses Tie miscalib | y | n | n | — | I2,I3 | PARTIAL | AB |
| ProGRes-2409.00217 | IEEE SLT'24 | frozen | prompted generative rescoring, ASR N-best + oracle-WER | unclear | n | n | — | I1 | DIRECT | AB ↔L11 |

### Lane 7 — candidate-support-diversity (8 rows) — *the upstream H(c) determinant*
| id | venue/yr | model | operator | audio@dec | gold@inf | train | our-data | kills | str | grade |
|---|---|---|---|---|---|---|---|---|---|---|
| novosad2026-ctc-oracle-gap (2606.23306) | arXiv'26 | mixed | CTC N-best pool-size vs realizable headroom (ρ collapse) | y | n | partial | **librispeech** | I2,I4 | PARTIAL | FT |
| ma2024-asr-ec-nbest-oracle (2409.09554) | TASLP'24 | mixed | beam N-best oracle vs compositional oracle | n | n | y | **librispeech** | I1,I4 | PARTIAL | FT |
| brown2024-large-language-monkeys (2407.21787) | arXiv'24 | frozen | coverage-vs-K law; selector plateau (text) | n | n | n | — | I1,I4 | ANALOGY | AB |
| freitag2023-epsilon-sampling-mbr (2305.09860) | EMNLP-F'23 | frozen | pool-construction strategy governs ref-free MBR (text) | n | n | n | — | I1,I4 | PARTIAL | AB |
| divsampling2025 (2502.11027) | arXiv'25 | frozen | diverse-supply → lower BoN error (text) | n | n | n | — | I1,I4 | ANALOGY | AB |
| wu2025-temperature-tts-coverage (2510.02611) | NeurIPS'25 | frozen | supply-config (temperature) bounds coverage (text) | n | n | n | — | I4 | ANALOGY | AB |
| dang2025-auditory-cognition-ttc (2503.23395) | arXiv'25 | frozen | audio-native pool by temp/beam (= scaling-auditory) | y | n | n | — | I2,I4,UMB | PARTIAL | FT ↔L5 |
| vijayakumar2016-diverse-beam-search (1610.02424) | AAAI'18 | frozen | diverse decoding sets coverage ceiling | n | n | n | — | I1,I4 | ANALOGY | AB |

### Lane 8 — contextual-supply-retrieval (7 rows)
| id | venue/yr | model | operator | audio@dec | gold@inf | train | our-data | kills | str | grade |
|---|---|---|---|---|---|---|---|---|---|---|
| siskos2025rag-context-asr (2509.19567) | EMNLP'25 | **frozen** | supply-conditional (none/retr/LLM/oracle) → ~69-77% oracle WER realized | y | n | n | — | I4 | PARTIAL | FT |
| gong2025brasr (2505.19179) | Interspeech'25 | mixed | trained bias retriever + frozen speech-LLM ASR | y | n | partial | **librispeech** | I4,I2 | PARTIAL | AB |
| cb-hotword-rl-2512.21828 | arXiv'25 | fine-tuned | GLCLAP retrieval + GRPO fine-tune | y | n | y | — | UMB,I2 | ANALOGY | AB |
| li2024larag (2409.08597) | ICASSP'25 | mixed | speech-token retrieval → ICL for frozen LLM-ASR | y | n | partial | — | I4,I2 | PARTIAL | AB |
| yang2024rasu | Interspeech'24 | trained | retrieval → generative SLU decoder | y | n | y | — | I4 | ANALOGY | SC |
| chen2025wavrag (2502.14727) | arXiv'25 | mixed | audio-native retriever (bypass ASR) → spoken dialogue | y | n | partial | — | I2,I4 | PARTIAL | AB |
| spoken-dialog-rag-2402.01828 | ICASSP'24 | trained | retrieval-augmented E2E spoken dialog (JGA 38.6 vs 32.7) | y | n | y | — | I4 | ANALOGY | AB |

### Lane 9 — selective-prediction-conformal (8 rows)
| id | venue/yr | model | operator | audio@dec | gold@inf | train | our-data | kills | str | grade |
|---|---|---|---|---|---|---|---|---|---|---|
| kamath2020-selective-qa | ACL'20 | frozen | trained calibrator threshold abstention (text) | n | n | y | — | I3 | PARTIAL | AB |
| lee2024-selective-generation (2307.09254) | NeurIPS'24 | frozen | selective generation, FDR-E control (frozen LM) | n | n | partial | — | I3 | PARTIAL | FT |
| quach2024-conformal-lm (2306.10193) | ICLR'24 | frozen | conformal stop+reject over sample pool (text) | n | n | n | — | I1,I3 | PARTIAL | AB |
| mohri2024-conformal-factuality (2402.10978) | ICML'24 | frozen | conformal claim back-off abstention (text) | n | n | n | — | I3 | PARTIAL | AB |
| tayebati2025-conformal-abstention-rl (2502.06884) | arXiv'25 | frozen | REINFORCE policy sets conformal thresholds (text+vision) | n | n | y | — | I3,UMB | PARTIAL | FT |
| ernez2023-conformal-asr | COPA'23 | **frozen** | conformal risk control on frozen wav2vec2 (WER<2%@80%) | y | **y** | n | **librispeech** | I2,I3 | **DIRECT** | AB ↔L13 |
| kuan2026-allm-uncertainty (2604.25591) | arXiv'26 | frozen | (= walking-through-uncertainty) | y | n | n | mmau/mmar/mmsu | I2,I3 | PARTIAL | AB ↔L5,13 |
| jin2025-selection-conditional-conformal (2403.03868) | JRSS-B'25 | frozen | selection-conditional coverage (stats tool for ρ(c)) | n | n | n | — | I4,I3 | ANALOGY | FT |

### Lane 10 — agentic (8 rows)
| id | venue/yr | model | operator | audio@dec | gold@inf | train | our-data | kills | str | grade |
|---|---|---|---|---|---|---|---|---|---|---|
| AudioToolAgent-2510.02995 | arXiv'25 | frozen(tools) | text-orchestrator over frozen audio tools; MMAU 77.5 | n | n | n | mmau-mini,mmar,big-bench-audio | UMB | PARTIAL | AB |
| AuTAgent-2602.13685 | arXiv'26 | mixed | **GRPO-trained** tool-policy on frozen backbone; **oracle 66.1 vs 50.0** | n | n | y | mmau-mini,mmar | I2,UMB | PARTIAL | FT |
| JitRL-2601.18510 | arXiv'26 | frozen | training-free advantage → logit modulation, KL closed-form (text) | n | unclear | n | tau2-bench,eva-bench | UMB,I1 | PARTIAL | SC ↔L15 |
| MAV-2502.20379 | arXiv'25 | frozen | multi-verifier BoN aggregation (text) | n | n | n | — | I1 | ANALOGY | AB |
| SampleScrutinizeScale-2502.01839 | arXiv'25/ICML'25 | frozen | sample + self-verify selection, implicit scaling (text) | n | n | n | — | I1 | ANALOGY | AB |
| AudioMind-2605.28480 | arXiv'26 | frozen | planner bounded evidence acq.; Goodhart cliff >10 calls | y | n | n | mmar,mmsu | I3,UMB | PARTIAL | FT ↔L5 |
| EChO-Agent-2606.15141 | arXiv'26/IS'26 | **frozen** | **Qwen3-Omni** Tool→Evidence→Reason→Verify; +2.3 acc | y | n | n | mmar | UMB,I3 | ANALOGY | SC |
| AgentOmni-2511.02834 | arXiv'25 | frozen | master coordinates frozen Qwen2.5-Omni expert (test-time) | n | n | n | meld,vocalbench | UMB | PARTIAL | SC |

### Lane 11 — kill-I1 (7 rows)
| id | venue/yr | model | operator | audio@dec | gold@inf | train | our-data | kills | str | grade |
|---|---|---|---|---|---|---|---|---|---|---|
| mbr-asr-2510.19471 | TMLR'26 | **frozen** | **MBR K=64 on frozen Whisper**; LS WER .042→.033 (oracle .013) | n | n | n | **librispeech,fleurs-r,covost2** | I1 | **DIRECT** | FT ↔L12,14,15 |
| tap-ger-2309.15649 | ASRU'23 | frozen | frozen InstructGPT rescoring **beats N-best oracle** (WSJ 8.72<9.78) | n | n | n | — | I1 | DIRECT | FT |
| progres-2409.00217 | IEEE SLT'24 | frozen | prompted generative rescoring, 5-25% rel WERR | y | n | n | — | I1 | DIRECT | AB ↔L6 |
| auditory-ttc-2503.23395 | arXiv'25 | frozen | (= scaling-auditory) | y | n | n | — | I1,I2 | DIRECT | FT ↔L5 |
| thinking-listening-2509.19676 | arXiv'25 | mixed | frozen majority vote 88.3 vs FT-UB 88.8 (ESC-50, non-speech) | y | n | partial | — | I1,I2 | PARTIAL | FT |
| hyporadise-2309.15701 | NeurIPS'23 D&B | fine-tuned | defines n-best oracle vs compositional oracle; GER trains | n | n | y | librispeech | I1 | PARTIAL | SC |
| judge-bon-fail-2603.12520 | arXiv'26 | frozen | Recovery 21%→61% (text) | n | n | n | — | I1,I4 | ANALOGY | FT ↔L6 |

### Lane 12 — kill-I2 (7 rows)
| id | venue/yr | model | operator | audio@dec | gold@inf | train | our-data | kills | str | grade |
|---|---|---|---|---|---|---|---|---|---|---|
| read-2026 (2606.04680) | arXiv'26 | frozen | analysis-by-synthesis: frozen **external TTS** NLL rerank; ~70-85% oracle | **y** | n | n | librispeech | I2,I1 | PARTIAL | FT |
| ttc-audio-2025 (2503.23395) | arXiv'25 | frozen | frozen omni-native beam log-lik BoN (+ ext GPT-4o verifier) | y | n | n | — | I2,UMB | DIRECT | FT ↔L5 |
| mbr-asr-2025 (2510.19471) | TMLR'26 | frozen | text-only MBR (no audio at decision — I1 boundary) | n | n | n | librispeech,fleurs-r | I1 | NONE | FT ↔L11 |
| sttfm-rescore-2024 (2409.16654) | arXiv'24 | unclear | joint speech-text FM rescoring likelihood | y | n | unclear | — | I2 | PARTIAL | SC |
| mmconsist-dataselect-2026 (2602.13263) | arXiv'26 | frozen | frozen SONAR audio-text consistency (DATA selection, not inference) | y | n | partial | — | I2 | ANALOGY | AB |
| aqa-ttrl-2025 (2510.05478) | arXiv'25 | trained | test-time RL (weights change) | y | n | y | mmau/mmar/mmsu | I2,UMB | ANALOGY | SC ↔L5,6 |
| omni-reward-2025 (2510.23451) | arXiv'25 | trained | learned omni-modal reward model / judge (trained) | y | n | y | — | I2 | ANALOGY | SC |

### Lane 13 — kill-I3 (8 rows)
| id | venue/yr | model | operator | audio@dec | gold@inf | train | our-data | kills | str | grade |
|---|---|---|---|---|---|---|---|---|---|---|
| I3-01 walking-through-uncertainty (2604.25591) | arXiv'26 | **frozen** | **Qwen2.5-Omni selective prediction / abstention on MMAU/MMAR/MMSU** | y | n | n | **mmau-mini,mmar,mmsu** | I3,UMB | **DIRECT** | FT ↔L5,9 |
| I3-02 RAS (2604.24278) | Interspeech'26 | fine-tuned | abstaining ASR w/ verifiable reward (SFT+RL) | y | n | y | — | I3 | PARTIAL | AB |
| I3-03 coverage-guaranteed-SER (2503.22712) | arXiv'25 | trained | conformal SER prediction sets | y | y | y | — | I3 | PARTIAL | FT ↔L1 |
| I3-04 ernez-conformal-asr | COPA'23 | **frozen** | conformal risk control on frozen ASR (LibriSpeech) | y | y | n | **librispeech** | I3 | **DIRECT** | AB ↔L9 |
| I3-05 inference-time-reward-hacking (2506.19248) | NeurIPS'25 | frozen | **HedgeTune/Best-of-Poisson Goodhart-aware selection** (text) | n | unclear | n | — | I3,UMB | ANALOGY | FT |
| I3-06 CICC (2403.18973) | NAACL-F'24 | frozen | conformal clarify/OOS abstention (text intent) | n | y | n | — | I3 | ANALOGY | AB |
| I3-07 NoRefER (2306.12577) | Interspeech'23 | fine-tuned | trained ref-free ASR ranker (no abstention) | n | n | y | — | I3 | ANALOGY | SC |
| I3-08 interfacing-LLM-ASR (2407.21414) | Interspeech'24 | frozen | confidence-gated selective correction (thr 0.7, LibriSpeech) | y | n | n | **librispeech** | I3 | PARTIAL | SC |

### Lane 14 — kill-I4 (8 rows)
| id | venue/yr | model | operator | audio@dec | gold@inf | train | our-data | kills | str | grade |
|---|---|---|---|---|---|---|---|---|---|---|
| KIT-IWSLT2026 (2606.04730) | IWSLT'26 | **mixed** | per-task oracle+realized across ASR/SQA/SSUM/ST (LoRA LLM cascade) | n | n | partial | ASR/ST/SQA analogues | I4,I1 | PARTIAL | FT |
| MBR-ASR-2510.19471 | TMLR'26 | frozen | per-task/lang oracle (best-of-64) ASR/ST | n | n | n | librispeech,fleurs-r | I4,I1 | PARTIAL | AB ↔L11 |
| GenRM-2408.15240 | ICLR'25 | mixed | realized-fraction-of-Pass@N across task×model-size grid (text) | n | n | y | — | I4,I1 | ANALOGY | AB |
| XLingRetrieval-2509.14749 | EMNLP-F'25 | frozen | ρ = realized/PRI; pool-vs-ordering split (text) | n | n | n | — | I4 | ANALOGY | AB |
| ColdStart-Retrieval-2606.29947 | arXiv'26 | mixed | **supply-type-stratified** realized headroom (17-61% vs 5-7%) | n | n | partial | — | I4 | ANALOGY | SC |
| RMOveropt-2210.10760 | ICML'23 | mixed | ρ-vs-budget (KL/N) Goodhart curve, BoN vs RL (text) | n | n | partial | — | I4,I3 | ANALOGY | AB ↔L15 |
| TextSQL-Nbest-2210.10668 | IEEE SLT'22 | mixed | oracle 10-best headroom stratified by difficulty (text) | n | n | y | — | I4,I1 | ANALOGY | AB |
| TwoRate-ErrorFlow-2604.18245 | arXiv'26 | frozen | items stratified by pool-supply (headroom present/absent) (text) | n | n | n | — | I4 | ANALOGY | SC |

### Lane 15 — kill-UMBRELLA (8 rows)
| id | venue/yr | model | operator | audio@dec | gold@inf | train | our-data | kills | str | grade |
|---|---|---|---|---|---|---|---|---|---|---|
| reflexion-2303.11366 | NeurIPS'23 | frozen | verbal-RL memory loop (reward→next action, text) | n | n | n | — | UMB | PARTIAL | AB |
| training-free-grpo-2510.08191 | arXiv'25 | frozen | **"Training-Free GRPO"** semantic advantage → token prior (text) | n | n | partial | — | UMB,I1 | PARTIAL | AB |
| jitrl-2601.18510 | arXiv'26 | frozen | gradient-free advantage → logit modulation, KL (text) | n | unclear | n | tau2-bench,eva-bench | UMB,I1 | PARTIAL | SC ↔L10 |
| iro-2506.17828 | arXiv'25 | mixed | RL on frozen base via trained value-fn + BoN search (text) | n | n | partial | — | UMB,I1 | PARTIAL | AB |
| iad-2504.01931 | arXiv'25 | frozen | **loop vs one-shot BoN adjudicator** (+3-4 pts, front-loaded, text) | n | n | n | — | UMB | PARTIAL | FT |
| auditory-ttc-2503.23395 | arXiv'25 | frozen | one-shot omni K-pool selection (no loop) | y | n | n | — | I2,UMB | PARTIAL | FT ↔L5 |
| reward-overopt-2210.10760 | ICML'23 | mixed | over-optimization budget N* / Goodhart (text) | n | n | partial | — | I3 | ANALOGY | AB ↔L14 |
| mbr-asr-2510.19471 | TMLR'26 | frozen | one-shot frozen-ASR selection, ~31% oracle realized | n | n | n | librispeech | I1 | PARTIAL | FT ↔L11 |

---

## Section B — The 5–8 CLOSEST works to our exact object (per-paper delta paragraphs)

Ranked by proximity to *"weight-frozen, label-free, reward-guided K-pool selection on frozen omni, studied as a supply-conditional realization surface."*

### 1. Scaling Auditory Cognition via Test-Time Compute — 2503.23395 [FT] `https://arxiv.org/abs/2503.23395`
**What they already did:** the tightest omni-mechanism occupant. Frozen audio-LLMs (Qwen2-Audio, Audio-Flamingo-2, Gemini, GPT-4o), label-free, no training, K-sample selection by (a) majority vote, (b) **audio-conditioned beam log-likelihood best-of-N** — a genuine frozen-omni-*native* audio-grounded signal — and (c) an audio-grounded verifier. Gains **9–150%**; Qwen2-Audio 36.7→50.0 (+36.2%), Audio-Flamingo-2 40.0→66.7 (+66.8%) [2503.23395]. This DIRECTLY occupies bare I1/I2 mechanism.
**What we add:** (i) an **oracle-over-pool ceiling and realized fraction ρ** — they report raw gains only, no headroom accounting; (ii) **supply-conditioning c → H(c)/regret surface** (they use fixed temp/beam on 3 bespoke cognition tasks, none of our benchmarks); (iii) the strongest scorer they use is an **external GPT-4o**, not the same frozen omni core error-decorrelated against itself; (iv) **no abstention/Goodhart** guard.
**Renaming risk:** HIGH on mechanism — if we pitch "frozen audio best-of-N works," we are re-skinning this. Survival = the realization-surface + same-core-verifier + abstention.

### 2. Re-evaluating MBR Decoding for ASR — 2510.19471 [FT] `https://arxiv.org/abs/2510.19471`
**What they already did:** the single most dangerous I1 kill on *our* tasks. Frozen Whisper, label-free, no training, K=64 reference-free MBR selection; **LibriSpeech WER 4.2→3.3 with oracle 1.3 (~31% of the gap realized)**; FLEURS En-Ja BLEU 8.24→11.68 [2510.19471]. Uses **our covost2/fleurs-r/librispeech families** and even reports a realized-fraction number.
**What we add:** (i) the risk metric is **text-only BLEU over hypotheses — audio is NOT used at the decision** (`uses_audio_at_decision=no`), so I2 audio-grounding survives; (ii) **single ASR/ST operator, not a [model×task] surface**; (iii) one-shot, no advantage-driven loop, no abstention; (iv) N treated as fixed, not swept as supply c. The ~31%-realized figure is precisely the *wide residual gap* our operator claims to close.
**Renaming risk:** HIGH for a plain I1-on-ASR/ST pitch — bare I1 will **not** survive an equal-K comparison here. Move to I2/I3/I4.

### 3. Walking Through Uncertainty (ALLM UQ) — 2604.25591 [FT] `https://arxiv.org/abs/2604.25591`
**What they already did:** the closest I3-abstention occupant on our exact core+data. Frozen **Qwen2.5-Omni-3B/7B + Audio Flamingo 3**, K=10 samples, semantic/discrete-semantic entropy + P(True) for selective prediction / unanswerable-QA abstention / hallucination detection on **MMAU/MMAR/MMSU** (AUROC 0.84-0.85; AQUA-Bench P(True) 0.79; AURAC 0.73-0.92) [2604.25591].
**What we add:** (i) selection is driven by **self-uncertainty, not a verifiable/audio-grounded reward** over the pool; (ii) it **abstains/routes**, it does not *select the best member to raise accuracy*; (iii) **no Goodhart/over-optimization** framing; (iv) reports AUROC/token-savings, **never ρ = realized/oracle fraction** across a supply matrix.
**Renaming risk:** MEDIUM — "abstention on frozen omni" is now occupied; our I3 must be the *reward-guided, Goodhart-aware, realization-surface* variant, not confidence estimation.

### 4. Decoding Ambiguous Emotions with Test-Time Scaling — 2602.03873 [FT] `https://arxiv.org/abs/2602.03873`
**What they already did:** the sole SER occupant of I1/I2 on **our crema-d**. Frozen Qwen2-Audio/Qwen2.5-Omni family, label-free, no training, BoN/Weighted-BoN/ALM-verifier over K=3-5; **CREMA-D 36.70→51.26 (+14.56pt)**, IEMOCAP 29.13→36.69, MSP-Podcast 38.30→42.25 [2602.03873].
**What we add:** (i) **no oracle ceiling → no ρ/regret**; (ii) fixed beams, **no supply-conditional c sweep → no I4 surface**; (iii) verifier is external **GPT-4o (text-side)**, not a self-contained frozen-omni audio-grounded scorer; (iv) **no I3 abstention/Goodhart**.
**Renaming risk:** HIGH for SER I1/I2 specifically. Our SER cell survives only via I3+I4.

### 5. KIT's IWSLT 2026 Long-Form Speech Instruction Following — 2606.04730 [FT] `https://arxiv.org/abs/2606.04730`
**What they already did:** the closest I4-*ingredient* occupant — measures **per-task oracle headroom AND fraction realized across 4 speech tasks**: ASR oracle −32.1 WER (Likelihood realizes −24.9; Likelihood+MBR −19.3), SQA +14.4, SSUM +3.9, ST +2.0 [2606.04730]. This is the H(c)+ρ empirical object, measured per task.
**What we add:** (i) it is a **Whisper→LoRA-LLM→TTS cascade — the LLM is fine-tuned, not weight-frozen**; (ii) tasks are **not a capability-supply-TYPE design axis** (they just have different headroom); (iii) **one system across four tasks = a task vector, not a supply-stratified model×task surface**; (iv) reranking scores are **text-only** (audio not at decision).
**Renaming risk:** LOW-MEDIUM — it shows the per-task ρ idea exists in speech but never as a frozen-omni supply-conditional *surface*; I4 remains defensible.

### 6. When LLM Judge Scores Look Good but Best-of-N Fails — 2603.12520 [FT] `https://arxiv.org/abs/2603.12520`
**What they already did:** **formalizes our ρ.** Recovery = (E[O_judge]−E[O_random])/(E[O_oracle]−E[O_random]) = **21.0% pointwise best-of-4 → 61.2% pairwise**; r_within 0.27 vs global 0.47; tie 66.5% [2603.12520]. Legitimizes the realization-rate lens and demonstrates the pointwise-selector failure mode.
**What we add:** (i) **TEXT-only (Chatbot Arena)** — no audio, no frozen speech/omni; (ii) N=4, single dataset, **no [model×task] matrix**, no supply-conditioning; (iii) no abstention/Goodhart. It **supports** (does not kill) our speech-side realization-surface object.
**Renaming risk:** MEDIUM on the *metric* — we must cite this as the origin of the recovery/ρ metric and claim only the audio + supply-surface specialization, never the metric itself.

### 7. Inference-Time Reward Hacking in LLMs — 2506.19248 [FT] `https://arxiv.org/abs/2506.19248`
**What they already did:** **owns the Goodhart-detecting selector concept.** Frozen policy + verifiable reward at inference; Best-of-N / Soft-BoN / **Best-of-Poisson + HedgeTune** root-finds the tipping point θ* where true reward peaks then collapses; Theorem 1: ≤1 interior extremum under TP2 [2506.19248]. Exactly an over-optimization-aware selection operator (our I3 solution shape + N* constraint).
**What we add:** (i) **TEXT-only**, reward is a learned text RM — **no audio-grounded reward, no speech**; (ii) no [model×task] realization surface. The "Goodhart-detecting selector ON SPEECH with an audio-grounded reward" cell has **no occupant**.
**Renaming risk:** HIGH on the *concept* — it kills conceptual novelty of "inference-time Goodhart-aware selection over a frozen model." Survival = the speech/audio-grounded instantiation + the supply-conditional surface. Import its N*/over-optimization constraint into our convergence proof.

### 8. AuTAgent — 2602.13685 [FT] `https://arxiv.org/abs/2602.13685`
**What they already did:** the only in-lane agentic paper reporting the exact headroom+realized quantity: **oracle 66.1% vs baseline 50.0% on MMAU Test-mini (16.1-pt tool-selection ceiling)**, realized **+4.20 (open Qwen2-Audio-7B) / +9.80 (closed GPT-4o-Audio)** on MMAU-mini, +6.20/+8.00 on MMAR (≈26%/61% of ceiling) [2602.13685]; K=6 tools; backbone frozen.
**What we add:** (i) it **TRAINS the tool-selection policy via GRPO (~2k samples) — not weight-frozen overall**; it argues *prompt-based/training-free selection under-realizes*, so it **contests** our training-free claim rather than occupying our identity; (ii) decision is over **text tool-outputs**, not audio-grounded K-pool of the omni's own generations; (iii) no supply-conditional surface.
**Renaming risk:** LOW for our identity, but this is the **strongest empirical adversary** to the thesis that a *purely training-free* selector can close the gap — we must demonstrate loop/selection gains **without** its weight updates.

---

## Section C — Closest challenger per identity (verified papers only)

| Identity | Verdict overall | Closest verified challenger | One-liner |
|---|---|---|---|
| **I1** general label-free N-best selector | **DIRECT_OCCUPIED** (ASR/ST) | **mbr-asr-2510.19471** (TMLR'26) | Frozen Whisper, label-free K=64 MBR on **our** LibriSpeech/FLEURS/CoVoST; LS WER 4.2→3.3 vs oracle 1.3 — bare I1 will not survive an equal-K comparison; audio is text-scored only, so I2 survives. |
| **I2** audio-grounded frozen-omni-native selector | **PARTIAL** (mechanism split across ancestors) | **scaling-auditory-cognition-2503.23395** (arXiv'25) | Frozen audio-LLM's own audio-conditioned beam log-lik BoN (+9-150%) is the true omni-native signal, but strongest scorer is external GPT-4o, custom tasks, no ρ surface. READ (2606.04680) does audio-grounded rerank but via an *external TTS*, not the core. Exact "same frozen core's own signal as a supply-conditional surface" = **NO_DIRECT_MATCH**. |
| **I3** constrained/abstaining/Goodhart-detecting | **PARTIAL** (abstention occupied; Goodhart-on-speech open) | abstain: **walking-through-uncertainty-2604.25591**; Goodhart: **inference-time-reward-hacking-2506.19248** | Frozen-omni selective prediction on MMAU/MMAR/MMSU is DIRECT; Goodhart-aware inference-time selection is DIRECT but **text-only**. The *combined* reward-guided + abstaining + Goodhart selector on frozen speech omni = **NO_DIRECT_MATCH**. |
| **I4** (supply c, selector) realization surface | **NO_DIRECT_MATCH_WITHIN_LOGGED_SCOPE** | **KIT-IWSLT2026-2606.04730** (partial ancestor, speech) | Per-task oracle+realized across 4 speech tasks exists, but on a LoRA cascade (not weight-frozen), task-vector not supply-type surface. Supply-type-stratified ρ exists only in **recsys/retrieval text** (ColdStart 2606.29947: 17-61% vs 5-7%). The frozen-omni supply-conditional cross-matrix surface is **genuinely open**. |
| **UMBRELLA** training-free RL + frozen omni + agentic loop | **NO_DIRECT_MATCH** (intersection) | omni half: **scaling-auditory-cognition-2503.23395**; loop-risk: **iad-2504.01931** | Every component is occupied *somewhere*: training-free RL over frozen model (Reflexion, Training-Free GRPO, JitRL — all text), frozen-omni K-pool selection (Scaling Auditory Cognition — one-shot, no loop), frozen-omni agentic (Agent-Omni/EChO/Audio-Mind — no reward-guided selection). **No single work does all three together.** IAD is the pre-registered risk: on text the agentic loop beats one-shot BoN by only **~3-4 pts, front-loaded in rounds 1-2** — we must prove loop≫BoN on frozen omni or the umbrella collapses to best-of-N. |

**Boundary note.** Papers on the *wrong side of the freeze line* (contest but do not occupy): AQA-TTRL (2510.05478, test-time GRPO **weights change**), AuTAgent (2602.13685, trains tool policy), R1-Omni (trains), RAS (2604.24278, SFT+RL abstention), cb-hotword-rl (2512.21828, LoRA-GRPO). These are the training-based cousins our weight-frozen stance explicitly rejects and must out-compete.
