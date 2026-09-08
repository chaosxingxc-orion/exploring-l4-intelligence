# Proposal §11 citation re-verification — fetch log and findings

- **Date of session**: 2026-08-16 (all timestamps UTC).
- **Target**: Section 11 survey table (14 works + 3 named artifacts) of
  `docs/superpowers/specs/2026-08-16-speech-aware-evidence-acquisition-continuation-extension-and-correction-proposal.md`
  (GPT-5.6-authored proposal).
- **Trigger**: prior adversarial audit found 13/14 rows without local receipts, 2 works not locally
  attested, 1 URL with a fabrication signature.
- **Method**: WebSearch + WebFetch only. No paid APIs, no logins. No writes outside this directory.
  `studies/` was not touched (live GPU experiment).
- **Status of this file**: workbench material, not a registry receipt. A later session may consolidate
  it into `wiki/survey/registry/` without redoing the searches below.

## 1. Fetch log (every query and URL, in order)

Timestamps are batch-level; the session ran 16:54Z–17:12Z.

### Batch 0 — local orientation (no network)

| # | Time (UTC) | Action | Result |
|---|---|---|---|
| 0.1 | 16:54 | Read proposal lines 795–844 (§11 table verbatim) | Extracted the 14 cited rows exactly as written. |

### Batch 1 — primary citation URLs

| # | Time (UTC) | Action | Result |
|---|---|---|---|
| 1.1 | 16:56 | WebFetch `https://aclanthology.org/2024.lrec-main.328/` | FAILED (socket hang up); retried in Batch 2. |
| 1.2 | 16:56 | WebFetch `https://aclanthology.org/2025.findings-emnlp.768/` | REAL. True title "Retrieval Augmented Generation based context discovery for ASR"; Siskos et al.; DOI 10.18653/v1/2025.findings-emnlp.768. Proposal title is wrong. |
| 1.3 | 16:56 | WebFetch `https://arxiv.org/abs/2603.16411` | REAL. RECOVER; Abhishek Kumar, Aashraya Sachdeva; 2026-03-17; "Under review for Interspeech 2026"; no code link. |
| 1.4 | 16:56 | WebFetch `https://arxiv.org/abs/2607.26410` | REAL. "Voice Memory for Agentic Speech Recognition"; Yang et al. (NVIDIA); 2026-07-29; release at huggingface.co/huckiyang/voice-memory. |
| 1.5 | 16:56 | WebFetch `https://arxiv.org/abs/2506.07510` | REAL. DeRAGEC; Im et al.; ACL 2025 Findings; code github.com/solee0022/deragec. |

### Batch 2 — ConEC retry + four more rows

| # | Time (UTC) | Action | Result |
|---|---|---|---|
| 2.1 | 16:58 | WebFetch `https://aclanthology.org/2024.lrec-main.328/` (retry) | REAL. ConEC; Huang et al.; LREC-COLING 2024; pp. 3700–3706. |
| 2.2 | 16:58 | WebFetch `https://arxiv.org/abs/2512.23686` | REAL. "PROFASR-BENCH: A Benchmark for Context-Conditioned ASR in High-Stakes Professional Speech"; Deepak Babu Piskala (single author); 2025-12-29; HF dataset + GitHub released. |
| 2.3 | 16:58 | WebFetch `https://aclanthology.org/2025.acl-long.613/` | REAL. WavRAG; Chen et al.; ACL 2025 Long; DOI 10.18653/v1/2025.acl-long.613. |
| 2.4 | 16:58 | WebFetch `https://aclanthology.org/2025.acl-long.319/` | REAL. "Adaptive Retrieval Without Self-Knowledge? Bringing Uncertainty Back Home"; Moskvoretskii et al.; ACL 2025 Long. |
| 2.5 | 16:58 | WebFetch `https://proceedings.neurips.cc/.../1f09e1ee5035a4c3fe38a5681cae5815-Paper-Conference.pdf` | URL RESOLVES — real 1.5MB PDF returned (binary; text not extractable by the fetch tool). Title obtained in 3.1. |

### Batch 3 — suspects and artifacts

| # | Time (UTC) | Action | Result |
|---|---|---|---|
| 3.1 | 17:01 | WebFetch `https://proceedings.neurips.cc/paper_files/paper/2025/hash/1f09e1ee5035a4c3fe38a5681cae5815-Abstract-Conference.html` | REAL. "Retrieval is Not Enough: Enhancing RAG through Test-Time Critique and Optimization" (AlignRAG); Jiaqi Wei et al.; NeurIPS 2025. Hash matches the cited PDF. |
| 3.2 | 17:01 | Read saved PDF page 1 | FAILED (poppler/pdftoppm not installed). Not needed — 3.1 resolved it. |
| 3.3 | 17:01 | WebFetch `https://openreview.net/forum?id=9U51rOnGko` | BLOCKED by OpenReview browser-verification interstitial. Resolved via 3.4. |
| 3.4 | 17:01 | WebFetch `https://arxiv.org/abs/2406.16020` | REAL. AudioBench; Bin Wang et al.; v1 2024-06-23, v5 2025-05-06; arXiv comments do NOT state a venue; code github.com/AudioLLMs/AudioBench. |
| 3.5 | 17:01 | WebFetch `https://arxiv.org/abs/2604.22821` | REAL. "Audio2Tool: Speak, Call, Act -- A Dataset for Benchmarking Speech Tool Use"; Pahwa et al.; v1 2026-04-17, v2 2026-04-28; project page audio2tool.github.io. |

### Batch 4 — MMSU URL authenticity + remaining identifications

| # | Time (UTC) | Action | Result |
|---|---|---|---|
| 4.1 | 17:03 | WebFetch `https://proceedings.iclr.cc/paper_files/paper/2026/hash/34e278fbbd7d6d7d788c98065988e1a9-Abstract-Conference.html` | REAL. "MMSU: A Massive Multi-task Spoken Language Understanding and Reasoning Benchmark"; Dingdong Wang et al.; ICLR 2026. |
| 4.2 | 17:03 | **CONTROL TEST** WebFetch same path with bogus all-zero hash | **HTTP 404 Not Found.** Proves the host does not fabricate pages for arbitrary hashes, so 4.1 is a genuine record. |
| 4.3 | 17:03 | WebFetch `https://proceedings.iclr.cc/` | Site is real; hosts ICLR 2024/2025/2026 electronic proceedings using the same `paper_files/paper/<year>` layout as the NeurIPS proceedings site. The "NeurIPS-shaped path" is the shared proceedings software, not a fabrication signature. |
| 4.4 | 17:03 | WebSearch `"Counterfactual RAG" ICLR 2026 openreview 9U51rOnGko` | REAL. True title "Counterfactual Reasoning for Retrieval-Augmented Generation"; Huaiyu Qin, Chunyu Wei, Yueguo Chen, Yunhai Wang (Renmin University); ICLR 2026 poster (iclr.cc/virtual/2026/poster/10011109). Forum id in the proposal is correct. |
| 4.5 | 17:03 | WebSearch `MMSU benchmark spoken language understanding ... paper` | MMSU = arXiv 2506.04779 (2025-06); HF dataset ddwang2000/MMSU; GitHub dingdongwang/MMSU; 47 tasks / 5,000 triplets; best model 60.68% accuracy. |
| 4.6 | 17:05 | WebSearch `AlignRAG "Retrieval is Not Enough" ... code github` | arXiv 2504.14858 (title there carries "RAG **Reasoning**"); code github.com/upup-wei/RAG-ReasonAlignment. |
| 4.7 | 17:05 | WebSearch `AudioBench ... NAACL 2025 aclanthology` | CONFIRMED venue: aclanthology.org/2025.naacl-long.218/, NAACL 2025 Long, pp. 4297–4316; dblp `conf/naacl/WangZLSLZLAC25`. The proposal's venue claim is correct even though arXiv does not state it. |
| 4.8 | 17:05 | WebFetch `https://audio2tool.github.io/` | Page exists ("Audio2Tool: Benchmark Demo") but is JS-rendered; no extractable release/license/link info. |

### Batch 5 — code/data availability

| # | Time (UTC) | Action | Result |
|---|---|---|---|
| 5.1 | 17:07 | WebSearch `ConEC ... github ... data release` | Points to ACL Anthology + Amazon Science mirror; repo located in 6.1. |
| 5.2 | 17:07 | WebFetch `https://arxiv.org/abs/2509.19567` | CONFIRMED same work as the EMNLP row: "Retrieval Augmented Generation based context discovery for ASR"; Siskos et al.; v1 2025-09-23, v2 2025-11-19; comments "Accepted at EMNLP 2025"; **no code/data URL**. |
| 5.3 | 17:07 | WebSearch `WavRAG ... github code release` | arXiv 2502.14727. **No public code repository found** as of this check. |
| 5.4 | 17:07 | WebSearch `RECOVER ... github code` | **No code repository found.** Confirms the local audit's finding. |
| 5.5 | 17:07 | WebFetch `https://arxiv.org/abs/2509.08031` | REAL. "AU-Harness: An Open-Source Toolkit for Holistic Evaluation of Audio LLMs"; Hoang Nguyen et al. (ServiceNow); v1 2025-09-09, v3 2026-05-11; claims up to 151% speedup. |

### Batch 6 — artifact-level checks

| # | Time (UTC) | Action | Result |
|---|---|---|---|
| 6.1 | 17:09 | WebFetch `https://github.com/huangruizhe/ConEC` | EXISTS (14 stars, 5 commits). Ships corrected Earnings-21/22 transcriptions, slides/press releases (PDF), participant names/affiliations, extracted biasing word lists, word-level timestamps. **License not stated in the README** — must be resolved before reuse. |
| 6.2 | 17:09 | WebFetch `https://huggingface.co/datasets/prdeepakbabu/ProfASR-Bench` | EXISTS. Apache-2.0. 3,200 rows, single `default` subset, **train split only — no held-out test split**. Audio is **synthetic Kokoro-TTS**, 4 voices (af_heart, am_michael, bf_emma, bm_george). Confirms the proposal's caveat. |
| 6.3 | 17:09 | WebFetch `https://huggingface.co/huckiyang/voice-memory` | EXISTS. 39 optimized memory `.md` files (<1.5KB each), inference + optimizer code. **License CC-BY-NC-SA-4.0 (non-commercial)**. Local baselines on HyPoradise v0 need no API key, but the main corrector path expects a MiniMax API key or equivalent LLM service. **Caveat**: the fetch summary asserted "arXiv:2401.10446 (January 2024)", which contradicts the verified arXiv record 2607.26410 (2026-07-29) — treat that one field as fetch-tool noise, not evidence. |
| 6.4 | 17:09 | WebSearch `Audio2Tool dataset release huggingface ... license` | No HF/GitHub artifact and **no license** surfaced. Dataset uses zero-shot voice-cloning TTS plus noise profiles. Release status: **announced project page only**. |
| 6.5 | 17:09 | WebSearch `"Adaptive Retrieval Without Self-Knowledge" ... github` | Code EXISTS: github.com/s-nlp/AdaRAGUE ("[ACL 2025]"); arXiv 2501.12835. |
| 6.6 | 17:01 | WebFetch `https://github.com/ServiceNow/AU-Harness` | EXISTS. **Apache-2.0**, ~70 stars, 36 commits. 50+ datasets, 380+ subsets, 21 audio tasks, 9 metrics; includes ASR/long-form ASR, intent classification, spoken QA, function calling, diarization, safety. Backends: **OpenAI (paid) OR vLLM (self-hosted) OR custom FastAPI**. LLM-judge metrics need a judge model but accept a vLLM backend → **no hard paid-service dependency**. |

### Batch 7 — bonus sweep (6 searches, as budgeted)

| # | Time (UTC) | Action | Result |
|---|---|---|---|
| 7.1 | 17:11 | WebSearch `training-free frozen speech LLM retrieved entity evidence audio verification abstention 2026` | No gap-occupying hit. Nearest: TRACE (2604.01083, training-free deepfake detection — different task), SpeakerLLM (2605.15044, speaker verification, trained). |
| 7.2 | 17:11 | WebSearch `ASR error correction harmful edit rate abstention retrieval evidence re-listening audio grounded verification 2026` | Neighbors surfaced: Error-Aware TF-IDF RAG for ASR EC (2606.24915); Ontology Memory-Augmented ASR Correction (2606.13464); "Proactive for Uncertainty: Cause-Aware Error Diagnosis and Interactive Clarification" (2605.25404); survey 2508.07285. Edit-quality metrics (Edit Rate, Improve@Edit, Worsen@Edit) already exist in this literature. None combines all five SAEA elements. |
| 7.3 | 17:11 | WebSearch `agentic speech recognition inference-time black-box frozen omni model retrieval contextual biasing no training 2026` | Top hit is Voice Memory (already row 4). Note: Voice Memory is explicitly **inference-only, no training, and uses no audio** at correction time — it abstains but does not re-listen. Also surfaced "Listen, Do Not Copy" (2607.21943). |
| 7.4 | 17:11 | WebSearch `speech LLM selective prediction abstain when uncertain retrieved evidence entity correction benchmark 2025 2026` | Abstention literature is text/VLM-side (Know Your Limits survey; BalanceRAG 2605.20084; ReCoVERR; 2607.20090 RL selective evidence adoption). No speech-side equivalent found. |
| 7.5 | 17:11 | WebSearch `re-listen audio segment verify hypothesis entity retrieval agent frozen audio language model 2026` | Surfaced EChO-Agent (2606.15141) and the Interspeech 2026 Audio Reasoning Challenge (2602.14224), whose **Agent Track** covers "multi-modal, tool-using, self-verification systems" — an adjacent evaluation venue worth watching. |
| 7.6 | 17:11 | WebSearch `"AgenticASR" ... 2607.28175 code` | AgenticASR (2607.28175, code github.com/InteractiveASR/AgenticASR) is **disfluency/readability refinement**, not evidence acquisition. Also surfaced Speech-Hands (2601.09413), a *fine-tuned* self-reflection voice agent. |

### Batch 8 — threat adjudication (2 targeted fetches)

| # | Time (UTC) | Action | Result |
|---|---|---|---|
| 8.1 | 17:12 | WebFetch `https://arxiv.org/abs/2606.15141` | EChO-Agent; Siyuan Zhang et al.; 2026-06-13; **Interspeech 2026**. Modular agent: planning → tool execution → evidence integration → answer verification, for complex **audio QA**. Abstract does not establish a frozen backbone, external entity retrieval, span-localized re-listening, or abstention/harmful-edit accounting. **Neighbors the gap; does not occupy it.** No code URL on the abstract page. |
| 8.2 | 17:12 | WebFetch `https://arxiv.org/abs/2607.21943` | "Listen, Do Not Copy: Internalizing Audio-Grounded Scaffold Context..."; Pengfei Zhang et al.; 2026-07-24/29. **Requires parameter training** (joint GDPO objective; clues "scaffold training"). No external retrieval — clues are built from audio. **Out of scope by the training-free boundary.** |

## 2. Findings table

Legend for availability class: RB = reproducible-baseline, RA = runnable-arm, ER = external-reference,
RW = related-work-only.

| # | Cited as | EXISTS? | Corrected citation (when it differs) | Code/data | Gap relation | Verdict | Class |
|---|---|---|---|---|---|---|---|
| 1 | ConEC, LREC-COLING 2024 | VERIFIED | (as cited) Huang, Yarmohammadi, Trmal, Liu, Raj, García, Ivanov, Ehlen, Yu, Rastrow, Povey, Khudanpur. LREC-COLING 2024, pp. 3700–3706 | github.com/huangruizhe/ConEC — data ships (corrected transcripts, slides, press releases, participant lists, biasing lists). **License unstated.** No paid service | Occupies the *evaluation carrier*, not the method gap. Supplies real (noisy) contexts for Earnings-21/22, exactly SAEA's OBS/SUPPLY substrate | MUST-CITE | RB |
| 2 | "Retrieval-Augmented Context Discovery for ASR", Findings EMNLP 2025 | DIFFERENT-THAN-CITED (title) | **"Retrieval Augmented Generation based context discovery for ASR"**, Siskos, Papadopoulos, Peso Parada, Zhang, Saravanan, Drosou. Findings of ACL: EMNLP 2025, 2025.findings-emnlp.768, DOI 10.18653/v1/2025.findings-emnlp.768, arXiv 2509.19567 | **No code/data** on either the anthology page or arXiv | Nearest published context-ladder prior on Earnings-21; retrieval selects context but there is no audio-grounded verification or abstention | MUST-CITE | ER (behavioral arm only) |
| 3 | RECOVER, 2026 | VERIFIED (preprint) | RECOVER: Robust Entity Correction via agentic Orchestration of hypothesis Variants for Evidence-based Recovery. Kumar & Sachdeva. arXiv 2603.16411, 2026-03-17. **Not peer-reviewed — "Under review for Interspeech 2026"** | **No code released** (recheck confirms local audit) | Closest method opponent: black-box, entity retrieval, LLM correction over N-best. But evidence is *text/hypothesis* (1-Best, Entity-Aware Select, ROVER, LLM-Select), with no localized audio verification, no legal-source control, no harmful-edit accounting | MUST-CITE | RW |
| 4 | Voice Memory, 2026 | VERIFIED (preprint) | Voice Memory for Agentic Speech Recognition. Yang, Chen, Żelasko, Chen, Balam, Ginsburg (NVIDIA). arXiv 2607.26410, 2026-07-29 | huggingface.co/huckiyang/voice-memory — 39 memory files + inference/optimizer code. **CC-BY-NC-SA-4.0 (non-commercial)**. Local HyPoradise baselines need no key; main corrector path expects an LLM service | Strongest overlap on *frozen + inference-only + abstain*, and the source of HER/RIR-style metrics. Critically it **uses no audio** at correction time — the localized-audio-verification half of the gap is untouched | MUST-CITE | ER |
| 5 | DeRAGEC, Findings ACL 2025 | VERIFIED | DeRAGEC: Denoising Named Entity Candidates with Synthetic Rationale for ASR Error Correction. Im, Lee, An, Kim, Ok, Lee. ACL 2025 Findings, arXiv 2506.07510 | github.com/solee0022/deragec. CommonVoice + STOP | Occupies candidate denoising (SUPPLY quality); no audio verification, no abstention, no harmful-edit ledger | MUST-CITE | RB |
| 6 | ProfASR-Bench, 2025 | VERIFIED (preprint) | PROFASR-BENCH: A Benchmark for Context-Conditioned ASR in High-Stakes Professional Speech. **Deepak Babu Piskala (single author)**. arXiv 2512.23686, 2025-12-29 | HF `prdeepakbabu/ProfASR-Bench` (Apache-2.0, 3,200 rows) + github.com/prdeepakbabu/ProfASR-Bench. **Synthetic Kokoro-TTS, train split only, no held-out test** | Reports the "context-utilization gap" on Qwen-Omni — directly the phenomenon SAEA attacks. Synthetic speech disqualifies it as headline validation | USEFUL-REFERENCE | RA (adversarial/secondary only) |
| 7 | WavRAG, ACL 2025 | VERIFIED | WavRAG: Audio-Integrated Retrieval Augmented Generation for Spoken Dialogue Models. Chen, Ji, Wang, Wang, Chen, He, Xu, Zhao. ACL 2025 Long, 2025.acl-long.613, arXiv 2502.14727 | **No public code found** | Audio-native retrieval prior, but the retriever is **trained** — outside SAEA's training-free boundary | USEFUL-REFERENCE | RW |
| 8 | "Adaptive Retrieval Without Self-Knowledge?", ACL 2025 | VERIFIED (subtitle omitted) | Adaptive Retrieval Without Self-Knowledge? **Bringing Uncertainty Back Home**. Moskvoretskii et al. ACL 2025 Long, 2025.acl-long.319, arXiv 2501.12835 | github.com/s-nlp/AdaRAGUE. Text-only QA | Text-domain; justifies SAEA's mandatory zero-retrieval / fixed-top-k / cost-normalized controls | USEFUL-REFERENCE | ER |
| 9 | "Retrieval Is Not Enough", NeurIPS 2025 | VERIFIED — **real, truncated title** | Retrieval is Not Enough: Enhancing RAG **Reasoning** through Test-Time Critique and Optimization (AlignRAG). Jiaqi Wei, Hao Zhou, Xiang Zhang, Di Zhang, Zijie Qiu, Noah Wei, Jinzhe Li, Wanli Ouyang, Siqi Sun. NeurIPS 2025; arXiv **2504.14858**. PDF hash in the proposal resolves correctly | github.com/upup-wei/RAG-ReasonAlignment. Trains an 8B Critic LM | Text-only, and its remedy is a **trained** critic — the exact thing SAEA forbids. Good foil for "measure evidence admission without a trained critic" | USEFUL-REFERENCE | RW |
| 10 | "Counterfactual RAG", ICLR 2026 | VERIFIED — **real, shortened title** | **Counterfactual Reasoning for Retrieval-Augmented Generation** (CF-RAG). Huaiyu Qin, Chunyu Wei, Yueguo Chen, Yunhai Wang (Renmin University). ICLR 2026 (poster 10011109); openreview.net/forum?id=9U51rOnGko | Not established in this pass (OpenReview blocked by bot challenge) | Text-only "Correlation Trap" + parallel arbitration. Motivates SAEA's wrong-reference and matched-irrelevant controls | OPTIONAL | RW |
| 11 | MMSU, ICLR 2026 | VERIFIED — **URL genuine** | MMSU: A Massive Multi-task Spoken Language Understanding and Reasoning Benchmark. Dingdong Wang, Junan Li, Jincenzi Wu, Dongchao Yang, Xueyuan Chen, Tianhua Zhang, Helen Meng. **ICLR 2026**; arXiv **2506.04779**; 47 tasks, 5,000 triplets, best model 60.68% | HF `ddwang2000/MMSU` + github.com/dingdongwang/MMSU | Task-value carrier for semantic speech tasks; not a method. Needs a human/synthetic-speech and license audit before use | USEFUL-REFERENCE | RA |
| 12 | AudioBench, NAACL 2025 | VERIFIED — **venue claim correct** | AudioBench: A Universal Benchmark for Audio Large Language Models. Bin Wang, Xunlong Zou, Geyu Lin, Shuo Sun, Zhuohan Liu, Wenyu Zhang, Zhengyuan Liu, AiTi Aw, Nancy F. Chen. **NAACL 2025 Long, 2025.naacl-long.218, pp. 4297–4316**; arXiv 2406.16020 (v5 2025-05-06) | github.com/AudioLLMs/AudioBench, open toolkit + leaderboard | Evaluation carrier. **Scope hazard**: includes audio-scene understanding, which is outside SAEA's speech-only boundary — adapters must be cherry-picked | USEFUL-REFERENCE | RA (deterministic adapters only) |
| 13 | Audio2Tool, 2026 | VERIFIED (preprint) | Audio2Tool: Speak, Call, Act — A Dataset for Benchmarking Speech Tool Use. Pahwa, Beedu, Priye, Gandhi, Takawale, Baijal, Yang. arXiv 2604.22821 (v2 2026-04-28). **No venue stated** | Project page audio2tool.github.io only (JS-rendered). **No HF/GitHub artifact and no license found.** ~30k queries, voice-cloned TTS + noise | Task-conversion probe surface (owner-admitted bounded leverage probe). Synthetic speech; unreleased artifact caps it | OPTIONAL | RW until an artifact lands |
| 14 | AU-Harness (artifact) | VERIFIED | AU-Harness: An Open-Source Toolkit for Holistic Evaluation of Audio LLMs. Hoang Nguyen et al. (ServiceNow). arXiv **2509.08031** (v3 2026-05-11). github.com/ServiceNow/AU-Harness | **Apache-2.0**. 50+ datasets, 380+ subsets, 21 tasks, 9 metrics. Backends OpenAI **or vLLM or custom FastAPI** → **no hard paid dependency**; LLM-judge metrics can run on a self-hosted judge | Pure tooling. Covers ASR/long-form ASR, intent, spoken QA, function calling — reusable adapters for SAEA's task conversion | MUST-CITE | RA (adapters only) |

## 3. Bonus sweep — systems that would threaten the gap claim

Searched for any 2025–2026 published system combining **localized audio verification + retrieved entity
evidence + abstention/harmful-edit control on a frozen speech-LLM**.

**Result: none found that occupies the full combination.** Closest misses, none of which the §11 table
lists, and all of which should enter the corrected survey as neighbors:

| Work | ID | Why it is close | Why it does not occupy the gap |
|---|---|---|---|
| EChO-Agent: Evidence Chain Orchestration Agent for Audio Reasoning | arXiv 2606.15141, Interspeech 2026 | Modular agent — planning, tool execution, evidence integration, **answer verification** — over audio | Targets general audio QA, not speech-entity repair. Frozen-backbone status unestablished; no external entity retrieval, no span-localized re-listening, no abstention/harmful-edit accounting |
| Listen, Do Not Copy (AGSC) | arXiv 2607.21943 | Audio-grounded context to defeat "perception bypass" on omni models; runs leakage/silence probes | **Requires parameter training** (joint GDPO). Clues derived from audio, no external retrieval. Out of boundary |
| Error-Aware TF-IDF RAG for ASR Error Correction | arXiv 2606.24915 | Retrieval-augmented post-ASR correction | Text-side retrieval only |
| Ontology Memory-Augmented ASR Correction | arXiv 2606.13464 | Memory + correction for long interleaved conversations | No audio verification or abstention |
| Proactive for Uncertainty: Cause-Aware Error Diagnosis and Interactive Clarification | arXiv 2605.25404 | Grounds clarification decisions in ASR-derived evidence — nearest abstention analogue on the speech side | Clarification via user interaction, not evidence retrieval + harmful-edit control |
| AgenticASR | arXiv 2607.28175, code github.com/InteractiveASR/AgenticASR | Agentic post-ASR refinement with released code | Disfluency/readability cleanup; no evidence acquisition |
| Speech-Hands | arXiv 2601.09413 | Self-reflection voice agent over an omni model | Fine-tunes the omni model (Voice Memory cites it as the trained contrast) |
| Interspeech 2026 Audio Reasoning Challenge | arXiv 2602.14224 | **Agent Track** evaluates "multi-modal, tool-using, self-verification systems" | An evaluation venue, not a system — but it is the arena where a competing system would appear. Worth monitoring |

Two structural observations for the gap statement:
1. Edit-quality accounting is **not novel** — Edit Rate / Improve@Edit / Worsen@Edit already circulate in
   the post-ASR-refinement literature (survey 2508.07285). SAEA's HER/RIR framing must cite that lineage
   rather than present harmful-edit accounting as new.
2. Voice Memory (frozen, inference-only, abstains, no training) plus RECOVER (black-box, retrieves
   entities, orchestrates hypotheses) together cover everything in the SAEA combination **except
   localized audio verification and legal-source/provenance control**. Those two elements now carry
   essentially the whole differentiation load and must be the isolated variables in the design.

## 4. Aggregate verdict on the §11 table

- **14 of 14 rows point at real works.** No row is fabricated. The prior audit's "fabrication
  signature" on the MMSU URL is **disproved** by the 404 control test at 4.2 — `proceedings.iclr.cc` is
  the genuine ICLR proceedings host and shares path software with the NeurIPS site.
- **4 rows carry citation defects**: row 2 (wrong title), row 9 (title dropped a word), row 10 (title
  shortened to a non-title), row 11 (arXiv id and dataset identity absent). Row 6 also omits that the
  work is single-author and preprint-only.
- **3 rows are preprints presented without that status**: rows 3, 4, 13. Row 3 is explicitly
  *under review*, which the proposal's phrase "the closest black-box entity-repair prior" obscures.
- **Availability reality**: no code for rows 2, 3, 7; no released artifact for row 13; unstated license
  for row 1; non-commercial license for row 4; synthetic-speech-only carriers for rows 6 and 13.
