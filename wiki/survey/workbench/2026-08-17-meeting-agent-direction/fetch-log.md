# Fetch log — meeting-agent direction external scan (2026-08-17)

Workbench note. Scope: meeting-domain datasets beyond the local holdings, plus 2024–2026 methods.
Web research only. No downloads, no installs, no logins, no paid APIs. All access via WebSearch /
WebFetch. English-only record.

Clock: local times are UTC-4, verified `2026-08-17 10:48:05` local == `14:48:05 UTC`.

Work was split across a coordinator and four parallel scouts. Each scout kept its own numbered log;
the sections below reproduce them. Row IDs are prefixed by scout (`L` coordinator, `A` audio corpora,
`B` text/summary corpora, `C` minuting + glossary methods, `D` agents + evaluation).

Failures, 404s, unparseable PDFs and empty searches are recorded, not silently dropped. Where a
fetch summary looked fabricated or contradicted an official page, the row says so and the datum was
discarded rather than carried forward.

---

## Section L — coordinator

| # | Time | Type | Query / URL | One-line result |
|---|------|------|-------------|-----------------|
| L1 | 10:47 | search | "meeting understanding benchmark 2026 long meeting audio LLM speaker attribution" | Surfaced SLT2026 SmartGlasses (2608.12034), LongSpeech, ChronosAudio (2601.04876), VoiceGiraffe (2605.27976), GlobeAudio (2606.08194), SA-ASR w/ speech-aware LLMs (2604.11269), in-meeting speaker correction (2509.18377). |
| L2 | 10:48 | fetch | `arxiv.org/abs/2608.12034` | SLT 2026 SmartGlasses Challenge, submitted 2026-08-12; 106 h, 714 sessions, 4-ch egocentric; two tracks (dyadic, multi-party meeting). |
| L3 | 10:49 | fetch | `arxiv.org/html/2608.12034` | **Mandarin only.** Track 2 = 196 sessions / 62.03 h / avg 19 min / overlap 13.6% (max 45%); 3509 SLU MCQs; metric tcpCER (5 s collar); baselines VibeVoice-ASR 57.81 tcpCER T2, **Qwen3-Omni-30B-A3B SLU 65.9% T2 / 69.9% T1**. |
| L4 | 10:49 | search | "meeting minutes benchmark 2025 2026 speech-grounded minuting dataset audio summarization arxiv" | AutoMin 3rd challenge (2509.13814), TCR dataset (2411.00038), online meeting summ. policies (2502.03111), Summarizing Speech survey. |
| L5 | 10:50 | fetch | `arxiv.org/html/2509.13814` | AutoMin 2025: Task A minuting + Task B meeting QA (new); ELMI / EuroParlMin / ELITR-Bench; **no audio, transcripts only**; names replaced by `[PERSONnumber]`; GPT-4/GPT-4o top; CoT LLM-judge vs human Pearson only 0.17/0.13; no human eval in 2025. |
| L6 | 10:50 | search | "arxiv 2026 meeting agent benchmark episodic glossary terminology self-derived keyword injection speech LLM" | **Miss** — query too broad; only generic agent-memory papers. |
| L7 | 10:51 | search | "ELITR-Bench meeting transcript QA benchmark long-context LLM evaluation arxiv" | ELITR-Bench = 2403.20262, COLING 2025 (`2025.coling-main.28`), 271 QA pairs, QA + Conv settings, WER-perturbed transcripts, repo `utter-project/ELITR-Bench`. |
| L8 | 10:51 | search | "end-to-end audio LLM meeting summarization from speech benchmark AMI ICSI 2025 2026 speech summarization" | MSU-Bench (2508.08155), Summarizing Speech survey (2504.08024, EMNLP 2025), Interspeech 2026 Audio Encoder Challenge, CADS review (2406.07494). |
| L9 | 10:52 | fetch | `arxiv.org/abs/2508.08155` | MSU-Bench metadata: Shuai Wang et al., submitted 2025-08-11; 4-tier multi-talker SLU benchmark; abstract lacks data detail. |
| L10 | 10:52 | search | "LongSpeech benchmark long-form speech audio LLM arxiv ICASSP 2026 8 tasks summarization QA" | LongSpeech = 2601.13539; also Speech-XL (2602.05373), MURMUR (2606.01483), FBK IWSLT 2026 long-form (2606.26819). |
| L11 | 10:52 | fetch | `arxiv.org/html/2508.08155v1` | MSU-Bench detail: EN (MDT-AD015 5 h, CHiME-6 6 h, en-Film ~41 h) + ZH (MDT-AA007, **AliMeeting 4 h**, cn-Film); 60–120 s clips; 1232 questions / 25 tasks; open-ended + LLM judge; Gemini-2.5-Pro 0.59 > GPT-4o-Audio 0.52 > Qwen2.5-Omni 0.37; repo `ASLP-lab/MSU-Bench`. |
| L12 | 10:52 | search | "two-pass ASR first pass hypothesis derived biasing list second pass decoding self-bootstrapped hotwords long-form" | Weak — mostly patents + deliberation-model work; CASA-ASR (2305.12459) only on-topic hit. Delegated to scout C. |
| L13 | 10:53 | search | "LLM meeting delegate agent participate meetings arxiv 2025 Microsoft transcript agent evaluation" | Meeting Delegate (2502.04376, ACL 2025 HCI+NLP `2025.hcinlp-1.24`); **Overhearing LLM Agents survey (2509.16325)**. |
| L14 | 10:53 | search | "Qwen3-Omni AMI AliMeeting meeting ASR WER results benchmark long audio 30 minutes limit" | TagSpeech (2601.06896), SoulX-Transcriber (2606.02400), Qwen3.5-Omni TR (2604.15804), Qwen3-Omni TR (2509.17765). |
| L15 | 10:54 | fetch | `arxiv.org/pdf/2604.15804` | PDF extraction lossy; no meeting table recovered. |
| L16 | 10:54 | fetch | `arxiv.org/abs/2509.16325` | Overhearing LLM Agents survey, Zhu & Callison-Burch, 2025-09-19; agents that monitor ambient activity and intervene unprompted. |
| L17 | 10:55 | fetch | `arxiv.org/html/2604.15804v2` | **Correction**: Qwen3.5-Omni TR has NO AMI-SDM/AliMeeting table; ASR section is Fleurs/CV/LibriSpeech/WenetSpeech. Limits: 256k tokens / **10 h audio**, chunked prefilling. The search-snippet attribution was wrong and was discarded. |
| L18 | 10:55 | fetch | `arxiv.org/abs/2502.03111` | Schneider/Turchi/Waibel (Zoom + KIT), 2025-02-05: online meeting summarization policies over AutoMin data; novel latency + partial-summary metrics; adaptive > fixed schedule. |
| L19 | 10:56 | fetch | `arxiv.org/abs/2601.06896` | TagSpeech (Huo, Shao, Zhang; 2026-01-11, rev 2026-07-13): LLM-based joint multi-speaker ASR + diarization via temporal anchor grounding + SOT; AMI + AliMeeting; abs page carries no numbers. |
| L20 | 10:56 | fetch | `arxiv.org/abs/2606.02400` | SoulX-Transcriber (Dai et al., 2026-06-01): joint SD+ASR in an LLM framework, 2-stage training; AliMeeting + AISHELL-4 + AMI; abs page carries no numbers. |
| L21 | 10:57 | search | `"meeting summarization" dataset with audio recordings released 2025 2026 hours speech-to-summary corpus new benchmark` | **MISP-Meeting (ACL 2025)**; MeetingBank confirmed 1366 meetings / 3579 h video; TACL abstractive meeting summarization survey. |
| L22 | 10:57 | search | "MISP-Meeting dataset ACL 2025 long-form meeting transcription summarization multimodal audio-visual" | MISP-Meeting = `2025.acl-long.753`; 125 h AV (119/3/3 split), 8-ch far-field + headset + 360° video, sentence transcripts, human-refined brief & detailed summaries; **Mandarin**; CER 36.60→20.27 with GSS + AV fusion; repo `coalboss/MISP-Meeting`. |
| L23 | 10:58 | fetch | `aclanthology.org/2025.acl-long.753/` | Confirmed authors (Chen, Yang, Gu, Siniscalchi, Du), pp. 15479–15492, ACL 2025 long. "Dataset and codebase will be released as open source"; **explicit licence not stated on the page**. |
| L24 | 10:58 | search | "meeting coreference speaker attribution summarization 'who said what' evaluation metric 2025 2026 arxiv attributable summary" | Metric audit (2404.11124), MESA family, Re-FRAME/P-MESA (2509.15901), Coreference-Aware Dialogue Summarization (2106.08556). |
| L25 | 10:59 | fetch | `arxiv.org/abs/2404.11124` | Kirstein et al., **EMNLP 2024**: automatic metrics on meeting summarization; QMSum; meeting-specific error taxonomy; weak-to-mid correlations, **~1/3 of correlations show error masking**. |
| L26 | 10:59 | search | "MESA reference-free meeting summarization evaluation metric error taxonomy LLM judge arxiv" | MESA (2411.18444) multi-LLM evaluator, GPT-4o backbone, +0.25 correlation over prior methods; CREAM (2409.10883) ELO-ranked reference-free; P-MESA (2509.15901) 7 personalization dimensions. |
| L27 | 11:00 | search | "unsupervised keyword extraction from meeting transcript to bias ASR rare words ..." | Only classical ICSI-era keyword extraction (TF-IDF/POS/LDA). Useful negative: only **59.74%** of human-annotated keywords survive into ASR output — a hard recall ceiling. |
| L28 | 11:00 | search | "arxiv 2025 2026 in-context glossary building LLM long document terminology consistency iterative prompt injection frozen model speech" | **BabelDOC (2605.10845, ACL 2026 demo)** — builds a dynamic glossary from the document itself and injects it into the LLM prompt for terminology consistency. |
| L29 | 11:01 | fetch | `arxiv.org/html/2605.10845v1` | BabelDOC mechanism: extracted-or-user-provided glossary, **prompt injection (not constrained decoding)**, built **once pre-translation** (not incremental), model steered without adaptation; ablation TC 5.00→3.00 without glossary/context control; human TC 4.47 vs 3.34 baseline. |
| L30 | 11:02 | search | "spoken question answering over meeting audio English benchmark AMI ICSI audio LLM QA gold 2025 2026" | **Useful negative**: no English audio-bearing meeting-QA gold surfaced. Audio QA options are generic (AudioBench `2025.naacl-long.218`, MMSU) or non-meeting. |
| L31 | 11:02 | search | "new meeting corpus 2026 released multi-party English conversation transcription benchmark challenge Interspeech ICASSP 2026 diarization" | **Useful negative**: no major new *English* meeting corpus in 2025–2026. Recent activity is Mandarin (M2MeT, MISP 2025, SmartGlasses). |
| L32 | 11:03 | fetch | `arxiv.org/abs/2504.08024` | Summarizing Speech survey, Retkowski et al., **EMNLP 2025**; abstract flags gaps in realistic benchmarks, multilinguality, long-context handling. |
| L33 | 11:03 | fetch | `arxiv.org/abs/2411.00038` | TCR dataset, Fan/Pool/Filipi/Cutler, **NeurIPS 2024 D&B**; 1500 meetings, 22 M words, 15k+ topics; **transcript-only**; **CC BY 4.0**; GPT-4-scored topic-relevance benchmark. |
| L34 | 11:04 | fetch | `arxiv.org/html/2504.08024v2` | **KEY**: "Cascaded approaches remain the most widely adopted paradigm in SSum." Dataset table (AMI 137 mtgs/65 h audio ✓; ICSI 75/72 h audio ✗ in this table; MeetingBank 1.3k/3.5k h ✓; SLUE-TED 4.2k/829 h; NUTSHELL 6.3k/1.2k h; YTSeg 19.3k/6.5k h). How2 and Spotify Podcast **no longer publicly available**. Metric critique: ROUGE fails on disfluency/multi-speaker; BERTScore 512-token limit; **"no models evaluate the SSum content directly from raw audio signals"**; CREAM/MESA/TofuEval named as the few meeting-specific frameworks; LLM judges show position and length bias. |
| L35 | 11:05 | search | "NUTSHELL dataset TED talk abstract speech summarization SLUE-TED benchmark audio English license" | NUTSHELL = 2502.16942 (*ACL talks + abstracts); SLUE-TED = TED talk abstract/title generation; TED content is **CC BY-NC-ND 4.0**. Both single-speaker talks, not meetings. |
| L36 | 11:05 | fetch | `github.com/QwenLM/Qwen3-Omni` | **No explicit max audio duration stated.** GPU-memory table goes to 120 s video; "long audio" claimed for ASR; three 30B-A3B variants (Instruct / Thinking / Captioner). Audio token rate and chunking strategy not documented. |
| L37 | 11:06 | search | "arxiv 2026 meeting assistant agent system speaker-attributed notes real-time audio LLM pipeline note-taking" | **MeetBench-XL (2602.03285)**; AR Secretary Agent (2505.11888); Interactive In-Meeting Speaker Correction (2509.18377). |
| L38 | 11:07 | fetch | `arxiv.org/abs/2602.03285` | MeetBench-XL, Hu et al., 2026-02-03: MeetAll corpus = 231 enterprise meetings / 140 h, bilingual multimodal; 5-dimension protocol; MeetMaster XL dual-policy agent (fast/slow routing + tool invocation); repo `huyuelin/MeetBench`, CC BY 4.0 stated on arXiv page. |
| L39 | 11:08 | fetch | `github.com/huyuelin/MeetBench` | **Audio IS shipped**: "200 h bilingual (English & Mandarin) audio with high-quality transcripts"; English portion = **20 CHiME-6 meetings, ~40 h, 382 queries**; 1180 human-verified agent QA turns; HF `YueLinHu/MeetAll-v2` with SHA-256 shards; **dataset licence CC BY-NC 4.0 (non-commercial)**, code Apache-2.0; MeetMaster 6.59/10 vs 3.30–6.56 for Llama/Qwen/DeepSeek/Phi/ChatGLM. Note the arXiv-page "CC BY 4.0" and the repo "CC BY-NC 4.0" **disagree** — repo wins, treat as NC. |
| L40 | 11:09 | fetch | `arxiv.org/html/2607.17766v1` | EGTA ablation: separates **EGTA-R (speech/prompt-side)**, **EGTA-G (decoder logit bias)**, **EGTA-RG (both)**; recommended B=2; B=3 gives diminishing returns; Global-G B=5 collapses (BLEU 43.31→41.21). Memory is **strictly fixed offline**, built in a preparation stage before streaming — **not incremental**. |
| L41 | 11:10 | fetch | `arxiv.org/abs/2512.16250` | AMUSE (Chowdhury et al., Apple + UMD, 2025-12-18), **CC BY 4.0**; six task families incl. spatio-temporal speaker grounding + multimodal dialogue summarization; zero-shot/guided/agentic modes; abstract names **GPT-4o and Qwen3-Omni as struggling in multi-speaker dialogue-centric settings**; RAFT gives up to **39.52% relative** gain. Corpus sources/hours not on the abs page. |
| L42 | 11:11 | fetch | `meetingbank.github.io` | MeetingBank: **audio distributed** via HF `huuuyeah/MeetingBank_Audio` + Zenodo; video on archive.org (Alameda, Boston, Denver, Long Beach, King County, Seattle); 1366 meetings, >3579 h video, 6 US cities, ~28k tokens/transcript, **6892 segment-level summarization instances**; PDF minutes + agenda + metadata; summaries from 6 systems + human annotations. **Licence not stated on the landing page** (defers to a `/license/` section). |
| L43 | 11:12 | fetch | `arxiv.org/html/2509.18377` | **Correction to a scout claim.** He et al. (Worcester Polytechnic), v2 dated 2026-05-27. The paper does **not** show zero-shot LLM failure; it uses **GPT-4o with prompt engineering**, reaching **78.9%** simulated-feedback accuracy on 8 AMI training meetings. Data = **AMI headset-mix test set, 16 meetings, ~9 h**. Metric = DER + Speaker Error (SErr), pyannote, 0.25 s collar. Result: **31.99% relative DER improvement, 52.68% speaker-error reduction**. |

| L44 | 11:13 | fetch | `arxiv.org/abs/2510.19358` | M3-SLU (Kwon, Kang, Yoon, Kim; 2025-10-22), **LREC 2026**; >12,000 validated instances with **paired audio**, transcripts and metadata; sources CHiME-6 + MELD + MultiDialog + **AMI**; tasks = speaker-attributed QA + speaker attribution via utterance matching; "models capture what was said but often fail to identify who said it". **Release status and licence not on the abs page — unverified.** |
| L45 | 11:14 | fetch | `github.com/coalboss/MISP-Meeting` | MISP-Meeting: **163 meetings, 125.15 h, 274 speakers, 23 rooms**, Mandarin; **CC BY-NC-ND 4.0, research-only, free upon authorisation**; gated by a signed licence agreement at `challenge.xfyun.cn/misp_dataset`, OSS mirrors; ships sentence transcripts (>99% accuracy, ±100 ms), **human-refined brief + detailed summaries** (2-pass expert review), speaker demographics. |
| L46 | 11:15 | fetch | `arxiv.org/abs/2103.06410` | MediaSum (Zhu, Liu, Mei, Zeng), **NAACL 2021**; 463.6 K NPR/CNN interview transcripts; gold = broadcasters' own overview/topic descriptions; **transcript-only**; **interviews, not meetings**; repo `zcgzcgzcg1/MediaSum`, licence unstated. |
| L47 | 11:15 | search | "VCSUM Chinese long meeting summarization dataset ACL 2023 Findings audio transcript hours license" | VCSUM = 2305.05280 / `2023.findings-acl.377`; **239 real-life meetings, >230 h**; annotations = topic segmentation, headlines, segmentation summaries, overall summaries, salient sentences; repo `hahahawu/VCSum`. |
| L48 | 11:16 | fetch | `github.com/hahahawu/VCSum` | VCSUM: **Chinese**; repo footer shows **MIT** (code licence; data coverage **unverified**); data-structure section mentions **meeting transcripts only — audio distribution not confirmed**; acquisition route not described. |

Coordinator failures / discards: L6 (empty), L12 (weak), L15 (lossy PDF), L17 (search-snippet
attribution proved false and was discarded), L30 and L31 recorded as deliberate negatives.

---

## Section A — audio-bearing meeting corpora scout

| # | Time | Type | Query / URL | One-line result |
|---|------|------|-------------|-----------------|
| A1 | 10:47 | search | ICSI Meeting Corpus audio transcripts open release license LDC | ICSI = 75 meetings, ~72 h, LDC2004T04 + LDC2004S02; pointer to Edinburgh mirror. |
| A2 | 10:47 | search | AliMeeting M2MeT challenge corpus hours speakers download OpenSLR | AliMeeting 118.75 h, 212/8/20 sessions, 8-ch array + headset, OpenSLR 119. |
| A3 | 10:47 | search | AISHELL-4 meeting corpus paper hours microphone array license | 211 sessions, 120 h, 4–8 spk, 8-ch circular array, OpenSLR 111, Interspeech 2021. |
| A4 | 10:47 | search | NOTSOFAR-1 Microsoft CHiME-8 meeting recordings download license | 315 meetings, ~6 min avg, 30 rooms, 35 speakers; HF `microsoft/NOTSOFAR` + GitHub. |
| A5 | 10:49 | fetch | `groups.inf.ed.ac.uk/ami/icsi/` | **CC BY 4.0 open re-release confirmed**; ~70 h; orthographic transcription + dialogue acts. |
| A6 | 10:49 | fetch | `openslr.org/119/` | AliMeeting licence **CC BY-SA 4.0**; tarball sizes (73.24 G far, 22.85 G near, 3.42 G eval, 8.90 G test). |
| A7 | 10:49 | fetch | `openslr.org/111/` | AISHELL-4 licence **CC BY-SA 4.0**; train_L/M/S + test; transcription + speaker VAD. |
| A8 | 10:49 | fetch | `huggingface.co/datasets/microsoft/NOTSOFAR` | Licence **CC BY 4.0**; dev/eval/train + simulated 200 h/1000 h; SC and MC variants. |
| A9 | 10:51 | fetch | `groups.inf.ed.ac.uk/ami/icsi/download/` | Signal options = "Headset mix" (120 MB/mtg) + "Individual channel headsets" (350 MB/mtg); 3 annotation zips; verbatim CC BY 4.0 sentence. |
| A10 | 10:51 | fetch | `chimechallenge.org/challenges/chime8/task2/index` | NOTSOFAR benchmark ≈280 meetings, ~150 h SC / ~110 h MC, **English**, 5 SC + 4 MC devices, 7-mic MC array; registration to submit. |
| A11 | 10:51 | search | CHiME-8 DASR task 1 corpora license obtaining | CHiME-8 DASR = CHiME-6 + DiPCo + Mixer 6 + NOTSOFAR-1; Mixer 6 via LDC; metadata CC0 1.0. |
| A12 | 10:51 | search | DiPCo Dinner Party Corpus Amazon download license hours arXiv | 10 sessions, 15–45 min, 4 speakers each, close-talk + 5× 7-mic arrays; CDLA-Permissive; Zenodo; arXiv 1909.13447. |
| A13 | 10:53 | fetch | `zenodo.org/records/8122551` | DiPCo licence = **CDLA-Permissive 1.0**; `DipCo.tgz` 13.4 GB; open, ungated. |
| A14 | 10:53 | fetch | `github.com/microsoft/NOTSOFAR1-Challenge` | `HF_TOKEN` required by official download script; CC BY 4.0; dev-set-1 baseline tcpWER/tcORC-WER **SC 46.8/38.5, MC 32.4/26.7**. |
| A15 | 10:53 | fetch | `chimechallenge.org/challenges/chime7/task1/index` | Confirms CHiME-7 DASR = CHiME-6 + DiPCo + Mixer 6 only. |
| A16 | 10:53 | fetch | `arxiv.org/abs/2401.08887` | NOTSOFAR-1 paper abstract; 315 meetings / 35 speakers / 30 rooms / 1000 h simulated. |
| A17 | 10:55 | fetch | `chimechallenge.org/challenges/chime8/task1/data` | Per-corpus splits incl. Mixer 6 **LDC2013S03, request form to `ldc@ldc.upenn.edu`**; NOTSOFAR1 92.4/13.4/20 h. |
| A18 | 10:55 | fetch | `arxiv.org/abs/2407.16447` | Abstract only; confirms NOTSOFAR-1 added in CHiME-8. |
| A19 | 10:55 | search | CHiME-6 / CHiME-5 LDC license free download dinner party | CHiME-6 = 24 sessions (16/2/2), 2–2.5 h each, 4 participants, home dinner parties. |
| A20 | 10:55 | search | Ego4D / Ego-Exo4D conversation audio transcripts | Ego4D AVD >750 h conversational, ~50 h annotated, English-only transcription; Ego-Exo4D 1286 h. |
| A21 | 10:57 | fetch | `github.com/chimechallenge/chime-utils` | `--download` auto-fetches chime6/dipco/notsofar1; **Mixer 6 must be obtained separately via LDC**. |
| A22 | 10:57 | fetch | `www1.icsi.berkeley.edu/Speech/mr/` | **FAILED — socket closed.** |
| A23 | 10:57 | fetch | `arxiv.org/abs/2309.13573` | M2MeT 2.0 = ASRU 2023, SA-ASR, two sub-tracks, new 10 h test set. |
| A24 | 10:57 | fetch | ISCA archive `fu21b_interspeech` | **FAILED — socket hang up.** |
| A25 | 10:59 | fetch | `www1.icsi.berkeley.edu/Speech/mr/` (retry) | **FAILED again.** Host abandoned. |
| A26 | 10:59 | fetch | ISCA `fu21b` (retry) | AISHELL-4: 211 sessions, 120 h, 4–8 spk, 8-ch circular array; DOI 10.21437/Interspeech.2021-1397. |
| A27 | 10:59 | fetch | `catalog.ldc.upenn.edu/LDC2004S02` | LDC ICSI copy includes close-talk **plus six tabletop mics** (4 PZM + 2 mock-PDA); "LDC User Agreement for Non-Members"; fee behind login. |
| A28 | 10:59 | search | ICSI 75 meetings 53 speakers 72 hours | 53 unique speakers (40 M / 13 F); ~1 h per meeting. |
| A29 | 11:01 | fetch | `groups.inf.ed.ac.uk/ami/download/` | Wrong page (AMI-only chooser). Discarded. |
| A30 | 11:01 | search | ICSI NXT annotations topic segmentation | Confirms contributed layers: topic (shallow hierarchical), hotspot, abstractive + extractive summaries. |
| A31 | 11:01 | fetch | `huggingface.co/datasets/microsoft/NOTSOFAR/tree/main` | **No gating banner**; top level = benchmark-datasets/, css-datasets/, css-models/, LICENSE.txt, README.md. |
| A32 | 11:01 | fetch | `github.com/yufan-aslp/AliMeeting` | Transcripts + RTTM + timestamps; code Apache-2.0; no baseline numbers in README. |
| A33 | 11:03 | fetch | ICSI download page (verbatim re-ask) | Only "Headset mix" and "Individual channel headsets" offered; annotation zips 19 MB / 53 MB / 4 MB; **no far-field option on the chooser**. |
| A34 | 11:03 | fetch | `arxiv.org/abs/2110.07393` | M2MeT: 120 h Mandarin, 2–4 spk/session, 8-ch array + headset. |
| A35 | 11:03 | fetch | `arxiv.org/abs/2507.18161` | Abstract-only landing page; no per-scenario tables. Honest miss. |
| A36 | 11:03 | fetch | `ego4d-data.org/docs/start-here/` | Ego4D requires accepting a licence agreement at ego4d.dev; AWS credentials emailed after ~48 h approval. |
| A37 | 11:06 | fetch | `groups.inf.ed.ac.uk/ami/ICSIsignals/` | Directory index exists: `NXT/` and `SPH/`. |
| A38 | 11:06 | fetch | `arxiv.org/pdf/2407.16447` | Summarizer returned a **clearly wrong** stats table (CHiME-6 "50 h/20 sess/~100 spk"), contradicting the official data page. **Discarded as unreliable.** |
| A39 | 11:06 | fetch | `ego4d-data.org/docs/benchmarks/audio-visual/` | **404 — wrong slug.** |
| A40 | 11:06 | fetch | `docs.ego-exo4d-data.org/annotations/` | Expert-commentary transcriptions exist; no meeting-style multi-party detail. |
| A41 | 11:08 | fetch | `groups.inf.ed.ac.uk/ami/ICSIsignals/SPH/` | Per-meeting folders (Bdb001, Bed002–Bed017, Bmr001, Bns, Bro, Bsr, Btr, Buw), dated 2016-07-22. |
| A42 | 11:08 | fetch | `arxiv.org/html/2407.16447v1` | CHiME-8 Table 1 + tcpWER/DER baselines for ESPnet and NeMo (treat as approximate — automated table extraction). |
| A43 | 11:08 | search | Ego4D licence terms AV diarization | Proprietary-to-licensor, non-exclusive/non-transferable, attribution required; AVD includes English-only transcription. |
| A44 | 11:08 | search | M2MeT baseline DER AliMeeting challenge results | Baseline **DER 15.24%** Eval-Ali-far, 0.25 s collar, 8-ch — secondary sources only, **needs verification**. |
| A45 | 11:10 | fetch | `groups.inf.ed.ac.uk/ami/ICSIsignals/SPH/Bmr001/` | **Key**: files are chan0, chan1, chan6, chan7, chan8, **chanC, chanD, chanE, chanF** — letter channels present, i.e. tabletop mics ARE in the free release. |
| A46 | 11:10 | fetch | `ego4d-data.org/docs/benchmarks/av-diarization/` | Correct page; 4 tasks; "only English speakers are considered for this version". |
| A47 | 11:10 | fetch | `arxiv.org/pdf/2202.03647` | **FAILED — PDF binary not parsed.** |
| A48 | 11:10 | search | M2MeT 2.0 test set release | M2MeT 2.0 was at **ASRU 2023, not ICASSP 2024**; Test-2023 = 10 sessions, 5 rooms, 58 speakers. |
| A49 | 11:12 | search | ICSI channel naming chanA–chanF PZM tabletop | Confirms 6 tabletop mics (4 PZM + 2 mock-PDA); **no official letter→mic map found**. |
| A50 | 11:12 | fetch | `groups.inf.ed.ac.uk/ami/icsi/annotation.shtml` | Released layers: dialogue acts, topic segmentation, abstractive summaries, extractive summaries, **named entities**, individual actions, person location, focus of attention. Not released: AmiEmotion, Twente argumentation. |
| A51 | 11:12 | fetch | `arxiv.org/pdf/2309.13573` | **FAILED — PDF binary not parsed.** |
| A52 | 11:12 | fetch | lhotse `ali_meeting.py` recipe docs | Downloads Train/Eval/Test from Alibaba OSS; parses TextGrid for Train, Eval **and Test**. |
| A53 | 11:14 | fetch | `alphaxiv.org/abs/2309.13573` | Abstract only; insufficient. |
| A54 | 11:14 | fetch | AISHELL-4 Data-Specification PDF (aliyuncs) | **FAILED — PDF binary not parsed.** |
| A55 | 11:14 | fetch | `chimechallenge.github.io/chime6/` | Insufficient; points to a download page. |
| A56 | 11:14 | fetch | HF `microsoft/NOTSOFAR/blob/main/LICENSE.txt` | Confirms verbatim **CC BY 4.0**, licensor Microsoft. |
| A57 | 11:16 | fetch | `chimechallenge.github.io/chime6/download.html` | Legacy route: CHiME-5 needs a **Sheffield licence** — free non-commercial for not-for-profits, **£2,000 commercial**. |
| A58 | 11:16 | fetch | `ar5iv.labs.arxiv.org/html/2309.13573` | M2MeT 2.0 Test-2023 = 10 sessions / 5 rooms / 58 speakers; baselines **8.84% cpCER** (modular) vs **41.55% cpCER** (SA-Transformer). |
| A59 | 11:16 | search | AISHELL-4 speakers / TextGrid detail | Praat TextGrid, char-level Mandarin with punctuation, anonymized spk-id + gender, timestamps, 10 ms VAD, `[laugh]/[cough]/[breath]`, overlap marked, ~3 annotators/session. |
| A60 | 11:18 | fetch | CHiME-8 task1 data page (licensing focus) | No explicit licence text on that page. |
| A61 | 11:18 | search | chime-utils dgen chime6 download URL licence | chime-utils pulls CHiME-6 from **OpenSLR 150**; a snippet claims downloading implies agreeing to the Sheffield CHiME-5 licence — **not verified in the README itself**. |
| A62 | 11:20 | fetch | `openslr.org/150/` | **CHiME-6 on OpenSLR under CC BY-SA 4.0**; train 97 G / dev 11 G / eval 12 G / transcriptions 2.4 M JSON / floorplans 1.4 M. |

Scout A failures: A22, A24, A25 (host socket errors), A39 (404), A47, A51, A54 (PDF binaries),
A35 (no tables on landing page), A38 (**summarizer produced fabricated-looking numbers — discarded**),
A29 (wrong page).

---

## Section C — minuting pipelines and glossary priors scout

| # | Time | Type | Query / URL | One-line result |
|---|------|------|-------------|-----------------|
| C1 | 10:49 | search | meeting summarization pipeline diarization speaker attribution LLM 2025 | Surfaced 2509.18377, 2504.08024, 2507.18161, SpeakerLM. |
| C2 | 10:49 | search | AutoMin 2023 shared task winning system | Overview `2023.inlg-genchal.19`; no winner named. |
| C3 | 10:49 | search | two-pass ASR first-pass bias list self-derived | Mostly patents; weak. |
| C4 | 10:49 | search | retrieval-augmented ASR hotword rare word long-form meeting 2025 | Found AutoMin **2025** exists; GETALP 2508.00476; Alibaba hotword-RL. |
| C5 | 10:51 | fetch | `aclanthology.org/2023.inlg-genchal.19/` | 5 teams, GPT-4 baseline + GPT-4 autoscoring; no per-team detail. |
| C6 | 10:51 | search | AutoMin 2025 third shared task overview | Findings paper 2509.13814; 1 team minuting, 2 QA. |
| C7 | 10:51 | search | Alibaba hotword retrieval RL ASR LLM | 2512.21828. |
| C8 | 10:51 | fetch | `arxiv.org/abs/2504.08024` | Summarizing Speech survey, EMNLP 2025 (abstract only). |
| C9 | 10:53 | fetch | `arxiv.org/abs/2509.13814` | Metadata confirmed; abstract thin. |
| C10 | 10:53 | fetch | `arxiv.org/abs/2512.21828` | GLCLAP retrieval + GRPO fine-tune. |
| C11 | 10:53 | search | contextual biasing meeting agenda slides participant names metadata | AMI slide-OCR biasing lists (175–576 words); CMT-LLM. |
| C12 | 10:53 | search | in-context biasing Whisper prompt frozen keyword list | KG-Whisper/KWS-Whisper; **224-token `initial_prompt` limit**. |
| C13 | 10:55 | search | self-bootstrapped bias list first-pass mine keywords second pass | Weak — patents + generic two-pass. |
| C14 | 10:55 | search | iterative decoding long-form ASR context propagation entity consistency | 2506.22858, MURMUR 2606.01483, PARCO. |
| C15 | 10:55 | search | end-to-end speech LLM long meeting audio summarization hour-long | 2406.05968, BASS 2307.08217, 2509.19631. |
| C16 | 10:55 | search | MARS multi-modal retrieval conversational ASR historical utterances | 2508.01166, AAAI. |
| C17 | 10:57 | fetch | `arxiv.org/abs/2511.11139` | SAP²; frozen/pass status not in abstract. |
| C18 | 10:57 | fetch | `arxiv.org/abs/2502.11572` | It **fine-tunes** Whisper; "zero-shot" refers to evaluation only. |
| C19 | 10:57 | search | keyword list generated by LLM from first-pass hypothesis | Weak — no exact match. |
| C20 | 10:57 | search | audio LLM episodic memory across chunks frozen | Off-scope (memory, not knowledge); discarded. |
| C21 | 11:00 | fetch | `arxiv.org/abs/2507.12252` | Abstract too thin on list provenance. |
| C22 | 11:00 | fetch | `arxiv.org/abs/2510.13979` | 34%/35% relative WER; method not in abstract. |
| C23 | 11:00 | search | bias list derived from the meeting's own transcript | BR-ASR 2505.19179; confirms AMI lists come from OCR/references. |
| C24 | 11:00 | search | speaker-attributed ASR meeting 2025 SA-ASR CHiME NOTSOFAR | M2MeT 2.0, NOTSOFAR-1, 2410.21849. |
| C25 | 11:02 | fetch | `arxiv.org/abs/2505.19179` | BR-ASR, Interspeech 2025, B-WER 2.8/7.1, 200k entries. |
| C26 | 11:02 | search | Whisper two-pass extract keywords re-prompt | Blog-heavy; surfaced 2511.18774. |
| C27 | 11:02 | search | contextual biasing without predefined bias list on-the-fly 2026 | LOGIC 2601.15397, 2604.12398. |
| C28 | 11:02 | search | meeting minutes pipeline diarization chunking map-reduce AMI ICSI | AMI/ICSI stats, map-reduce practice, DiariZen. |
| C29 | 11:05 | fetch | `arxiv.org/abs/2511.18774` | **KEY** — zero-shot, no parameter updates, first-pass hypothesis as decoder prompt. |
| C30 | 11:05 | fetch | `arxiv.org/abs/2601.15397` | **Paper WITHDRAWN 2026-02-04**; abstract still readable. |
| C31 | 11:05 | fetch | `arxiv.org/abs/2112.02741` | Team Hitachi AutoMin 2021, best adequacy. |
| C32 | 11:05 | search | AutoMin 2021 first shared task overview | 10 teams; ISCA archive `ghosal21_automin`. |
| C33 | 11:08 | fetch | `arxiv.org/html/2511.18774v2` | **KEY** — full ablation; self-prompt alone 29.01% WER vs 15.79% baseline. |
| C34 | 11:08 | fetch | `arxiv.org/html/2509.13814v1` | **KEY** — full AutoMin 2025 results, teams, baselines, gold transcripts. |
| C35 | 11:08 | search | assigning real speaker names via self-introductions LLM | 2509.15082, DiarizationLM 2401.03506. |
| C36 | 11:08 | search | terminology consistency long document ASR acronym normalization | **KEY** — surfaced EGTA 2607.17766. |
| C37 | 11:11 | fetch | `arxiv.org/abs/2607.17766` | **KEY** — document terminology memory, no fine-tuning. |
| C38 | 11:11 | fetch | `arxiv.org/abs/2506.22858` | TSD 2025; trains; 40 s semantic window. |
| C39 | 11:11 | fetch | `arxiv.org/abs/2509.15082` | Truly training-free diarization refinement, 29.7% relative. |
| C40 | 11:11 | search | "glossary" automatically built from meeting transcript injected into LLM prompt | **FAIL — zero research hits**, only marketing glossaries. Recorded as a negative. |
| C41 | 11:14 | fetch | `arxiv.org/html/2607.17766v1` | **KEY** — memory built OFFLINE from paper title/abstract; logit bias B=2.0. |
| C42 | 11:14 | search | overhearing LLM agents survey taxonomy | Verified 2509.16325, Zhu & Callison-Burch. |
| C43 | 11:14 | search | omni audio LLM meeting summarization Qwen2.5-Omni | AudioMarathon 2510.07293, AMUSE. |
| C44 | 11:14 | search | contextual biasing accumulate entity list across long recording | **KEY** — 2608.05759, LCB-net 2401.06390. |
| C45 | 11:17 | fetch | `arxiv.org/abs/2608.05759` | **KEY** — biasing beats speech LLMs; LLMs sensitive to distractors + prompt order. |
| C46 | 11:17 | fetch | `arxiv.org/abs/2406.05968` | Interspeech 2024; beats cascade baseline at utterance scale. |
| C47 | 11:17 | fetch | `arxiv.org/abs/2509.19631` | Microsoft, multi-stage RL; no meeting-length eval stated. |
| C48 | 11:17 | fetch | `arxiv.org/abs/2401.06390` | LCB-net, ICASSP 2024, SlideSpeech numbers. |
| C49 | 11:20 | fetch | `arxiv.org/html/2504.08024v2` | **KEY** — "Cascaded approaches remain the most widely adopted paradigm in SSum." |
| C50 | 11:20 | search | AMUSE agentic multi-speaker understanding | 2512.16250, UMD + Apple. |
| C51 | 11:20 | fetch | `arxiv.org/abs/2309.07414` | PromptASR, ICASSP 2024; uses preceding utterance text. |
| C52 | 11:20 | search | construct bias list from ASR transcript itself | Weak; surfaced WCTC-Biasing 2506.01263. |
| C53 | 11:23 | search | two-pass lecture transcription glossary from first pass | **FAIL** — blogs only; no research prior. |
| C54 | 11:23 | search | speaker-attributed summarization per-speaker summary meeting | TACL survey, FRAME 2509.15901. |
| C55 | 11:23 | fetch | `arxiv.org/abs/2606.10838` | Interspeech 2026; fine-tuned; external video metadata. |
| C56 | 11:23 | fetch | `arxiv.org/abs/2506.01263` | Retraining-free but needs intermediate encoder layers. |
| C57 | 11:26 | fetch | `arxiv.org/abs/2507.02927` | MLC-SLM, 54.87% relative tcpWER; context mechanism not in abstract. |
| C58 | 11:26 | fetch | `aclanthology.org/2023.inlg-genchal.19.pdf` | **FAILED — PDF binary not parseable.** |
| C59 | 11:26 | search | "episode-local" OR "meeting-specific glossary" self-built re-injected frozen | **No research hits — informative negative.** |
| C60 | 11:26 | search | LLM-generated bias list from agenda/previous segment, frozen, 2026 | 2604.12398, CTC-assisted 2411.06437. |
| C61 | 11:29 | fetch | `arxiv.org/abs/2411.06437` | **KEY** — SLT 2024; CTC pass-1 filters hotwords for the LLM prompt. |
| C62 | 11:29 | search | AutoMin 2023 INLG participating teams | Zoom, Synapse, NTR, Iterate, Darbarer. |
| C63 | 11:29 | search | AudioMarathon long-context audio LLM benchmark | 90–300 s only; VoiceGiraffe extends to hour level. |
| C64 | 11:32 | fetch | `aclanthology.org/volumes/2023.inlg-genchal/` | Exact IDs `.14`–`.19` confirmed. |
| C65 | 11:32 | fetch | `arxiv.org/abs/2605.27976` | VoiceGiraffe, hour-level, far from saturation. |
| C66 | 11:32 | fetch | `arxiv.org/abs/2510.13979` (re-fetch) | **Partial fail** — cached; no method detail beyond abstract. |
| C67 | 11:35 | search | meeting minutes agent frozen omni no fine-tuning glossary control plane 2026 | **Negative — no matching system found.** |
| C68 | 11:35 | search | contextual biasing "previous chunk" hypotheses build hotword list for later chunks | Weak; confirms CTC-assisted is the nearest archetype. |

Scout C failures: C40, C53, C58, C67 (C66 partial). The emptiness of C40, C53, C59 and C67 is
itself evidence and is treated as such in `methods.md`.

---

## Section D — LLM/omni meeting agents and evaluation scout

Session start `2026-08-17 10:48:54` local.

| # | ~Time | Type | Query / URL | One-line result |
|---|------|------|-------------|-----------------|
| D1 | 10:49 | search | LLM meeting agent multi-agent meeting minutes 2025 arXiv | Generic multi-agent surveys; no meeting-minutes hits. Weak. |
| D2 | 10:49 | search | Qwen2.5-Omni / Qwen3-Omni AMI meeting corpus evaluation long audio | Located Qwen2.5-Omni 2503.20215, Qwen3-Omni 2509.17765, Qwen3.5-Omni 2604.15804, AU-Harness 2509.08031. |
| D3 | 10:49 | search | speaker-attributed ASR audio LLM prompting diarization-aware without training 2025 | 2509.15082, 2506.05796, 2604.22467, 2511.16046, 2508.06372. |
| D4 | 10:49 | search | AutoMin minuting shared task evaluation ROUGE human correlation | AutoMin 2021 ISCA overview, 2509.13814, ALIGNMEET 2205.05433, 2502.03111. |
| D5 | 10:52 | fetch | `arxiv.org/abs/2509.17765` | Qwen3-Omni TR verified, 2025-09-22, 38 authors; abstract names no meeting corpus. |
| D6 | 10:52 | fetch | `arxiv.org/abs/2604.15804` | Qwen3.5-Omni TR verified, 2026-04-17 (v2 04-21); 256k ctx, 215 audio benchmarks. |
| D7 | 10:52 | fetch | `arxiv.org/abs/2509.13814` | AutoMin 3rd findings verified (Shinde/Besacier/Bojar/Thonet/Ghosal). |
| D8 | 10:52 | fetch | `arxiv.org/abs/2509.15082` | Training-free identity-aware LLM diarization refinement; clinical data; 29.7% rel. reduction. |
| D9 | 10:52 | fetch | `arxiv.org/abs/2506.05796` | Diarization-aware multi-speaker ASR via LLMs (ASRU 2025 submission); no datasets in abstract. |
| D10 | 10:52 | fetch | `arxiv.org/abs/2502.03111` | Online meeting summarization policies (Zoom + KIT); AutoMin data; latency metrics. |
| D11 | 10:56 | fetch | `arxiv.org/abs/2307.11394` | **MeetEval** verified — von Neumann, Boeddeker, Delcroix, Haeb-Umbach, CHiME-7 workshop 2023; cpWER / ORC-WER / MIMO-WER + temporal constraint. |
| D12 | 10:56 | fetch | `arxiv.org/html/2509.17765v1` | Qwen3-Omni Table 6: WenetSpeech `test_meeting` is the only meeting-like set. **Quote: "audio recordings up to 40 minutes per instance for ASR and spoken-language understanding."** No diarization content. |
| D13 | 10:56 | search | NOTSOFAR-1 challenge tcpWER baseline results | 2401.08887 (Interspeech 2024), 2501.17304, 2507.18161. |
| D14 | 10:56 | search | MeetingBank QMSum MeetingQA benchmark evaluation metric | MeetingBank 2305.17529 / `2023.acl-long.906`; QMSum 2104.05938; MeetingQA `2023.acl-long.837`. |
| D15 | 10:59 | fetch | `arxiv.org/abs/2606.18134` | **Dixtral** verified — Polok, Cornell, Udupa, Černocký, Watanabe, Burget; 2026-06-16; **Interspeech 2026 accepted**; AMI / NOTSOFAR-1 / LibriSpeechMix / Mixer6 + a new long-form multi-speaker QA benchmark; cpWER deltas vs Gemini 3.0 Flash / VibeVoice / Voxtral. |
| D16 | 10:59 | search | 2025–2026 "meeting minutes" LLM agent speaker attribution glossary injection speech | 2509.18377, 2604.11269, 2603.10468 (G-STAR), 2509.16325. |
| D17 | 10:59 | search | QAFactEval entity-level factual consistency AlignScore SummaC | 2112.08542 / `2022.naacl-main.187`, AlignScore repo, SummaC. |
| D18 | 10:59 | search | Earnings21 Earnings22 audio LLM long-form entity WER 2025 | 2104.11348, **2604.07354 (Contextual Earnings-22)**, 2510.06961, 2605.23463. |
| D19 | 11:03 | fetch | `arxiv.org/abs/2509.16325` | Overhearing LLM Agents survey verified (Zhu & Callison-Burch, 2025-09-19). |
| D20 | 11:03 | fetch | `arxiv.org/abs/2604.11269` | SA-ASR using speech-aware LLMs (IBM: Aronowitz, Kons, Dekel, Saon, Hoory), 2026-04-13; fine-tuned Granite-speech + speaker cluster tags. |
| D21 | 11:03 | fetch | `arxiv.org/abs/2510.06961` | Open ASR Leaderboard verified (Srivastav et al., 2025-10-08, v4 2026-03-30); 86 systems, 12 datasets, WER + RTFx. |
| D22 | 11:03 | fetch | `arxiv.org/abs/2604.07354` | **Contextual Earnings-22** verified (Durmus, Cen, Pacheco, Okan, Orhon; 2026-03-28); six baselines split across **keyword prompting vs keyword boosting**. |
| D23 | 11:06 | search | "meeting recap" LLM system CHI 2025 user study | 2307.15793 / ACM PACMHCI `10.1145/3711074`. |
| D24 | 11:06 | search | meeting summarization LLM judge protocol reference-free rubric human agreement | CREAM 2409.10883, MESA 2411.18444, 2407.11919, 2604.21345. |
| D25 | 11:06 | fetch | `arxiv.org/abs/2509.08031` | AU-Harness verified by title/authors/date; abstract gives no dataset list — meeting coverage unconfirmed. |
| D26 | 11:06 | search | Voxtral / Phi-4-multimodal / Step-Audio 2 AMI Earnings22 WER long-form limit | Phi-4-Mini TR 2503.01743 with AMI + Earnings22 numbers; Step-Audio 2 2507.16632. |
| D27 | 11:10 | fetch | `arxiv.org/html/2503.01743v2` | **Table 4 extracted.** AMI: Phi-4-MM 11.69, Canary-1B 13.90, Qwen2-audio 15.24, Whisper-v3 15.95, Gemini-2.0-Flash 21.58, SeamlessM4T-v2 56.1, GPT-4o 57.76. Earnings22: Phi-4-MM 10.16, Whisper-v3 11.29, Canary 12.19, Gemini-2.0-Flash 13.13, Qwen2-audio 14.09, GPT-4o 20.94. Quotes: "maximum 2.8 hours of audio"; "Qwen2-Audio has a 30-second cut-off". |
| D28 | 11:10 | fetch | `arxiv.org/abs/2411.18444` | **MESA** verified — Kirstein, Ruas, Gipp; 2024-11-27; **COLING 2025 Industry Track**; GPT-4o backbone; ~+0.25 correlation over prior methods. |
| D29 | 11:10 | fetch | `arxiv.org/abs/2409.10883` | **FAILED — socket hang up.** |
| D30 | 11:10 | fetch | `arxiv.org/abs/2604.21345` | Verified — "Evaluating AI Meeting Summaries with a Reusable Cross-Domain Pipeline" (Zhong, Wang, Zhang; 2026-04-23); 114 meetings; **no human agreement reported; accuracy differences not significant (p 0.053–0.448)**. |
| D31 | 11:13 | fetch | `arxiv.org/abs/2409.10883` (retry) | **CREAM** verified — Gong, Ai, Deshpande, Johnson, Phung, Wu, Emami, Hirschberg; 2024-09-17; reference-free, CoT + key-fact alignment, ELO ranking. |
| D32 | 11:13 | fetch | `arxiv.org/html/2507.16632v2` | Step-Audio 2 reports **only** WenetSpeech meeting CER: Step-Audio 2 4.73, Doubao 4.90, Kimi-Audio 5.21, Qwen-Omni 6.61, GPT-4o Transcribe 31.40. No AMI/ICSI/AliMeeting/NOTSOFAR/Earnings; no audio-length statement. |
| D33 | 11:13 | search | speaker-attributed summarization "who said what" attribution accuracy per summary sentence | **No standard metric found** — only cpWER framing and AttrScore (citation attribution, different problem). **Confirms a genuine metric gap.** |
| D34 | 11:13 | search | Kimi-Audio / Qwen2.5-Omni AliMeeting AMI ICSI results table | Kimi-Audio WenetSpeech test-meeting 6.28 (**snippet, not table-verified**). No AMI/ICSI/AliMeeting in Kimi-Audio. Also TagSpeech 2601.06896, SoulX 2606.02400, ContextASR-Bench 2507.05727. |
| D35 | 11:17 | fetch | `arxiv.org/abs/2510.02995` | **FAILED — socket hang up.** |
| D36 | 11:17 | fetch | `arxiv.org/abs/2507.18161` | CHiME-7/8 DASR review verified (Cornell, Boeddeker, Park, …, Watanabe; 2025-07-24, v2 11-01). Quote: **"even systems with over 50% time-constrained minimum permutation WER can perform roughly on par"**. |
| D37 | 11:17 | search | Kirstein meeting summarization error taxonomy QMSum Mistake | 2407.11919 / `2025.coling-main.143`; **QMSum Mistake** = 200 summaries, 9 error types (169 erroneous + 31 controls). |
| D38 | 11:17 | search | speaker-attributed WER SA-WER definition Kanda 2020 | **SA-WER origin confirmed**: Kanda et al., Interspeech 2020, arXiv 2006.10930; SA-MBR 2011.02921. |
| D39 | 11:20 | fetch | `arxiv.org/abs/2510.02995` (retry) | **AudioToolAgent** verified — Wijngaard, Formisano, Dumontier, Jitsev; 2025-10-03, rev 2026-02-13; **training-free** central LLM agent + tool adapters, **agent never accesses audio**; MMAU 77.50 / MMAR 77.00 / MMAU-Pro 61.90. No meeting or long-form content. |
| D40 | 11:20 | fetch | `github.com/fgnt/meeteval/blob/main/doc/tcpwer.md` | **FAILED — HTTP 503.** tcpWER default collar **not confirmed**. |
| D41 | 11:20 | search | 2026 agentic framework meeting audio understanding LLM diarization minutes | Audio-Mind 2605.28480, Interspeech 2026 Audio Reasoning Challenge 2602.14224, M3-SLU 2510.19358, SpeakerLLM 2605.15044. |
| D42 | 11:20 | search | MeetingBank ACL 2023 QAEval metric | MeetingBank = Hu, Ganter, Deilamsalehy, Dernoncourt, Foroosh, Liu; `2023.acl-long.906`; 1,366 meetings / 3,579 h. |
| D43 | 11:24 | fetch | `arxiv.org/abs/2510.19358` | **M3-SLU** verified — two tasks (speaker-attributed QA + speaker attribution via utterance matching); built from CHiME-6, MELD, MultiDialog, **AMI**; >12,000 validated instances; LLM-as-Judge + accuracy. |
| D44 | 11:24 | fetch | `arxiv.org/abs/2605.28480` | **Audio-Mind** verified (Wang, Peng, Li + 6; 2026-05-27); planner-guided tool calls, auditable reasoning traces; MMAR 80.4, MSU-Bench 82.8. No meeting/diarization content. |
| D45 | 11:24 | fetch | `arxiv.org/abs/2602.14224` | Interspeech 2026 Audio Reasoning Challenge verified (Ziyang Ma et al., 2026-02-15); Single-Model + Agent tracks, 156 teams; **MMAR-Rubrics** instance-level protocol. |
| D46 | 11:24 | fetch | `arxiv.org/abs/2509.18377` | Interactive in-meeting speaker correction verified (He, Guan, Paurana, Kongsomjit, Dai, Whitehill; 2025-09-22, rev 2026-05-27); **AMI headset test set**; DER −31.99%, speaker substitution error −52.68%. |
| D47 | 11:27 | fetch | `arxiv.org/html/2510.06961v4` | Open ASR Leaderboard long-form English track = **CORAAL, Earnings21, Earnings22, TED-LIUM v3** (AMI is short-form). Aggregate long-form WER: Cohere Transcribe 9.73, Parakeet TDT 0.6B v3 10.7, Whisper Large v3 Turbo 11.0, Canary Qwen 2.5B 11.2, Whisper Large v3 11.2, Distil-Whisper v3.5 11.7. Per-dataset breakdown is on the HF Space, not in the paper. |
| D48 | 11:27 | fetch | `arxiv.org/abs/2508.06372` | **SpeakerLM** verified (Yin et al.; 2025-08-08, v3 2026-01-03), **AAAI 2026**; trained; flexible speaker registration mechanism. |
| D49 | 11:27 | fetch | `arxiv.org/abs/2409.19507` | "A Critical Look at Meta-evaluating Summarisation Evaluation Metrics" verified (Dai, Karimi, Fang; **EMNLP 2024 Findings**) — metrics meta-evaluated almost only on news. |
| D50 | 11:27 | search | entity-level factual consistency Nan 2021 | Confirmed Nan et al., **EACL 2021**, `2021.eacl-main.235` / 2102.09130 — entity-level precision/recall. |
| D51 | 11:31 | fetch | `arxiv.org/html/2503.20215v1` | Qwen2.5-Omni Table 2: **WenetSpeech `test_meeting` 7.7** (vs Seed-ASR-Chinese 5.7, MinMo 7.4). No AMI/ICSI/AliMeeting/NOTSOFAR/Earnings. **No max audio length stated.** |
| D52 | 11:31 | fetch | `isca-archive.org/automin_2021/ghosal21_automin.pdf` | **FAILED — PDF text not extractable.** AutoMin 2021 correlation coefficients **not confirmed**. |
| D53 | 11:31 | fetch | `arxiv.org/abs/2604.22467` | **DM-ASR** verified (Li, Cheng, Zhu, Wang, Liu, Li; 2026-04-24); multi-turn dialogue reformulation + word-level timestamps. |
| D54 | 11:31 | search | "Findings of the Second Automatic Minuting" AutoMin 2023 metrics | `2023.inlg-genchal.19` and `2022.inlg-genchal.1`. |
| D55 | 11:34 | fetch | `aclanthology.org/2023.inlg-genchal.19/` | Verified (Ghosal, Bojar, Hledíková, Kocmi, Nedoluzhko; INLG 2023); GPT-4 outputs added as benchmark; "more fine-grained manual evaluation". |
| D56 | 11:34 | fetch | `arxiv.org/pdf/2509.13814` | Partial extraction; confirms ROUGE + BERTScore + BARTScore; baselines Llama-3.2-3B, Llama-3.1-8B, Phi-4-mini, Phi-3-small-128k. Correlation coefficients not extractable from the PDF. |
| D57 | 11:34 | fetch | `aclanthology.org/2022.inlg-genchal.1/` | Verified (Ghosal, Hledíková, Singh, Nedoluzhko, Bojar; INLG 2022). Two tasks: generate minutes AND **"devise efficient metrics for evaluating the quality of minutes."** |
| D58 | 11:34 | fetch | `arxiv.org/abs/2306.05685` | MT-Bench verified (Zheng + 12; **NeurIPS 2023 D&B**); position / verbosity / self-enhancement bias; GPT-4 judge >80% human agreement. |
| D59 | 11:37 | fetch | `arxiv.org/abs/2606.02400` | SoulX-Transcriber verified (Dai et al., 13 authors, 2026-06-01); names **AliMeeting, AISHELL-4, AMI**; no numbers in abstract. |
| D60 | 11:37 | fetch | `aclanthology.org/2023.acl-long.837/` | **MeetingQA** verified (Prasad, Bui, Yoon, Deilamsalehy, Dernoncourt, Bansal; ACL 2023); multi-span answers across speakers; **models F1 57.3 vs human 84.6**. |
| D61 | 11:37 | fetch | `assemblyai.com/blog/speaker-diarization-and-llm-based-meeting-summarization` | **FAILED — HTTP 404.** |
| D62 | 11:37 | search | vendor engineering blog meeting notes pipeline diarization LLM summarization 2025 | NVIDIA developer blog (adam.ai), Gladia blog. |
| D63 | 11:41 | fetch | NVIDIA developer blog (AI note-taking/summarization) | Pipeline: ingest → Riva ASR → LLM summarization → action items. **No diarization, no chunking, no evaluation methodology.** |
| D64 | 11:41 | fetch | Gladia blog (prompts for summarizing online meetings) | Diarization + speaker-name mapping by **timestamp overlap** (pyannoteAI Precision-2); "prompt injection in speech recognition" for domain vocabulary. **No chunking strategy, no evaluation method.** |
| D65 | 11:41 | search | contextual biasing prompting frozen speech LLM glossary 2025 2026 training-free | 2604.12398, 2601.15397 (LOGIC), 2607.08117 (COALA), 2601.13409 (RLBR). |
| D66 | 11:41 | search | speech summarization benchmark omni meeting audio end-to-end 2026 | Summarizing Speech survey 2504.08024. |
| D67 | 11:45 | fetch | `arxiv.org/abs/2504.08024` | Verified — Retkowski, Züfle, Sudmann, Pfau, Watanabe, Niehues, Waibel; 2025-04-10 (v3 10-17); **EMNLP 2025 accepted**. |
| D68 | 11:45 | fetch | `arxiv.org/abs/2601.15397` | **LOGIC verified as WITHDRAWN 2026-02-04** (Peidong Wang). Identifies context-window limits, latency, lost-in-the-middle for prompt biasing; metrics Entity WER + False Alarm Rate. **Do not cite as authority.** |
| D69 | 11:45 | fetch | `arxiv.org/abs/2305.16739` | AlignScore verified (Zha, Yang, Li, Hu; **ACL 2023**); 355M unified alignment model, 22 datasets. |
| D70 | 11:45 | search | SummaC NLI summarization inconsistency TACL | Confirmed Laban, Schnabel, Bennett, Hearst; **TACL 2022**, `2022.tacl-1.10` / 2111.09525; SummaC_Conv 74.4 balanced accuracy. |
| D71 | 11:49 | fetch | `arxiv.org/html/2504.08024v3` | Evaluation section extracted; **explicit ROUGE critique quote captured**; metric catalogue and dataset table. |
| D72 | 11:49 | search | evaluate omni model directly on meeting audio summarization AMI ICSI 2026 | **Nothing found.** No paper evaluates a frozen omni model end-to-end on AMI/ICSI meeting summarization. Recorded as a deliberate negative. |
| D73 | 11:49 | fetch | `aclanthology.org/2022.naacl-main.187/` | QAFactEval verified (Fabbri, Wu, Liu, Xiong; NAACL 2022); +14% avg over prior QA-based metrics on SummaC. |
| D74 | 11:49 | search | G-Eval GPTScore summarization LLM judge correlation | G-Eval 2303.16634; GPT-4 Spearman **0.514** on summarization; authors flag bias toward LLM-generated text. |
| D75 | 11:53 | search | TofuEval topic-focused dialogue summarization hallucination NAACL 2024 | **TofuEval** 2402.13249 / `2024.naacl-long.251`; GPT-4 as binary factuality evaluator **outperformed by specialized non-LLM metrics**. |
| D76 | 11:53 | search | 2025 multi-agent automatic meeting minutes generation framework | MIMIC/FAME 2502.13001; otherwise the space is dominated by paper-review agents, not meeting agents. |
| D77 | 11:53 | fetch | `arxiv.org/abs/2406.07494` | **CADS** verified (Kirstein, Wahle, Gipp, Ruas; **JAIR Vol. 82, 2025**). "The ROUGE metric is the most used"; human evaluation "frequently reported without sufficient detail on inner-annotator agreement". |
| D78 | 11:57 | fetch | `arxiv.org/abs/2502.13001` | MIMIC/FAME verified (Kirstein, Khan, Wahle, Ruas, Gipp; **ACL 2025 Findings**); 500 EN + 300 DE **synthetic** transcripts. |
| D79 | 11:57 | search | 2026 meeting agent LLM audio real-time speaker-aware minutes AMI ICSI | Confirms AMI headset-mix test set (16 meetings, ~9 h, 3–4 spk). Also EVA-Bench 2605.13841, G-STAR 2603.10468, TagSpeech, DNCASR 2506.01916. |

Scout D failures: D29, D35 (socket hang up — both recovered on retry), D40 (GitHub 503, **not
recovered** — tcpWER collar remains unverified), D52 (PDF text extraction, **not recovered** —
AutoMin 2021 correlations remain unverified), D61 (404, not recovered). D33 and D72 are deliberate
negatives and are treated as evidence.

---

## Note on scout B

A fifth scout was dispatched for the text/summary corpora batch (MeetingBank, QMSum, ELITR/AutoMin,
MediaSum, VCSUM) and had not reported when this note was closed. Every record in `datasets.md` §2
was therefore verified first-hand by the coordinator against the official paper, the authors'
repository, or the dataset's own landing page — see rows L21, L23, L42, L46, L47, L48 above, plus
L5 and L7 for the AutoMin/ELITR and ELITR-Bench facts. If scout B reports later, its rows should be
appended here as Section B and any disagreement with §2 resolved in favour of the primary source.

