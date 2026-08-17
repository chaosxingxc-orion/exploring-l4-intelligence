# Meeting datasets beyond the local holdings — external scan

Workbench note. Date: 2026-08-17 (local, UTC-4). Web research only; nothing downloaded, nothing
installed, no logins, no paid APIs. Fetch provenance in `fetch-log.md`. English-only record.

Scope: the **meeting domain specifically**. A parallel audit covers the LOCAL holdings (AMI,
earnings21/22) in `local-audit.md`; a separate agent covers SLU/SQA/agentic-speech broadly. This
file covers external meeting corpora plus 2025–2026 newcomers.

**Program boundary applied to every record.** In-boundary is human speech and its linguistic content
(ASR, entities, contextual biasing, spoken QA, meeting speech understanding). FSD50K, AudioSet and
ESC-50 are forbidden categories — none is relevant here, and no corpus below carries
environmental-audio classification labels. Stated for completeness, as required. Paid resources are
auto-excluded.

**The single most important column is modality.** Several of the best-known "meeting" resources are
transcript-only. We need speech-grounded evaluation, so those are flagged loudly and are usable only
as text-side references.

---

## 0. Verdict summary

| Corpus | Modality | Language | Free? | Minutes/summary gold | QA gold | Verdict |
|---|---|---|---|---|---|---|
| **ICSI Meeting Corpus** | audio + transcript (headset + tabletop far-field) | **English** | **CC BY 4.0, ungated** | **abstractive + extractive** | no | **ADMIT — top pick** |
| **MeetingBank** | **audio + video + transcript** | **English** | HF/Zenodo, licence unconfirmed | **professional human minutes** | no (QA-based scoring) | **ADMIT — top pick for minutes gold** |
| **M3-SLU** | **audio + transcript** | English (AMI/CHiME-6-derived) | release status unverified | no | **speaker-attributed QA** | **ADMIT — top pick for QA gold** |
| **NOTSOFAR-1** | audio + transcript (SC + MC arrays) | **English** | **CC BY 4.0** (free HF token) | no | no | **ADMIT** |
| **CHiME-6** | audio + transcript | English | CC BY-SA 4.0 (OpenSLR 150) | no | no | ADMIT — genre caveat (dinner party) |
| **DiPCo** | audio + transcript | English | CDLA-Permissive, ungated | no | no | ADMIT (low weight, tiny) |
| **MeetBench-XL / MeetAll** | **audio + transcript** | EN + Mandarin (EN ≈ 40 h) | **CC BY-NC 4.0** | no | **1180 agent QA turns** | ADMIT with NC caveat |
| **MISP-Meeting** | audio + video + transcript | **Mandarin** | CC BY-NC-ND 4.0, gated | **brief + detailed summaries** | no | Secondary (language) |
| **AliMeeting / M2MeT** | audio + transcript | **Mandarin** | CC BY-SA 4.0 | no | no | Secondary (language) |
| **AISHELL-4** | audio + transcript | **Mandarin** | CC BY-SA 4.0 | no | no | Secondary (language) |
| **SLT 2026 SmartGlasses** | audio (4-ch egocentric) | **Mandarin** | challenge registration | no | **3509 SLU MCQs** | Secondary (language) — but see §3.1 |
| **MSU-Bench** | audio (60–120 s clips) | EN + Mandarin | GitHub released | no | 1232 open-ended | Secondary (clip length) |
| **QMSum** | **transcript-only** | English | see §2 | query-focused summaries | query-summary pairs | Text-side reference only |
| **ELITR / AutoMin** | **transcript-only, name-redacted** | English + Czech | registration | **minutes** | ELITR-Bench 271 QA | Text-side reference; see the redaction warning |
| **TCR** | **transcript-only** | English (implied) | **CC BY 4.0** | no (topic relevance) | no | Text-side reference |
| **VCSUM** | transcript-only (audio unconfirmed) | **Chinese** | MIT (repo) | **headlines + segment + overall summaries + salient sentences** | no | Secondary (language) — best annotation template |
| **MediaSum** | **transcript-only** | English | repo, licence unstated | derived overviews | no | **Out of scope — interviews, not meetings** |
| **Mixer 6** | audio | English | **LDC-gated / paid** | no | no | **EXCLUDED — fails zero-cost rule** |
| **Ego4D / Ego-Exo4D** | audio + video | English | approval-gated agreement | no | no | **DO NOT PURSUE** — not meeting-style, heavy ambient audio |

---

## 1. Audio-bearing meeting corpora

### 1.1 ICSI Meeting Corpus — **the top pick**

- **Modality**: audio + transcript. Per-speaker **close-talk headset** (lapel in early meetings)
  **plus 6 tabletop far-field mics** (4 omnidirectional PZM down the table centre + 2 elements on a
  mock PDA). A single mixed headset WAV per meeting is also offered.
  - *Verified subtlety*: the free Edinburgh download chooser labels its two options "Headset mix"
    (~120 MB/mtg) and "Individual channel headsets" (~350 MB/mtg), implying no far-field. But the
    per-meeting SPH directories contain **chan0, chan1, chan6, chan7, chan8 AND chanC, chanD, chanE,
    chanF** — letter channels, i.e. non-headset channels **are** present in the free release. The
    exact letter→microphone mapping is **unverified** (no official map found); the *presence* of
    extra non-headset channels is verified.
- **Size**: 75 meetings, ~72 h (LDC) / "approximately 70 hours" (Edinburgh); ~1 h per meeting;
  **53 unique speakers** (40 M / 13 F — reported by secondary sources; the primary Janin et al. 2003
  page would not load).
- **Language**: English.
- **Licence / obtainability**: **CC BY 4.0**, verbatim from the official page: *"All of the signals
  and transcription, and some of the annotations, have been released publicly under the Creative
  Commons Attribution 4.0 International Licence (CC BY 4.0)."* **Free, direct download, no login, no
  form**, from `groups.inf.ed.ac.uk/ami/icsi/download/` and `.../ICSIsignals/SPH/`. A paid LDC route
  exists (LDC2004S02 + LDC2004T04) and is **not needed**.
- **Gold layers — the richest of any audio meeting corpus found**: orthographic transcription;
  **MRDA dialogue acts**; **topic segmentation** (shallow hierarchical, with subtopics);
  **abstractive summaries**; **extractive summaries**; **named entities**; individual actions;
  person location; focus of attention; hotspots. Packaged as `ICSI_core_NXT.zip` (19 MB),
  `ICSI_plus_NXT.zip` (53 MB, contributed layers), `ICSI_original_transcripts.zip` (4 MB, MRT).
  Not released: AmiEmotion, Twente argumentation.
- **Verdict**: **ADMIT — top pick.** English, free, permissive, pure human speech, and the only
  corpus carrying summaries + named entities + topic segmentation on top of ASR-grade transcripts.
- ⚠️ **Protocol caution**: ICSI meetings run ~1 h, which **exceeds the 40-minute per-instance audio
  limit stated in the Qwen3-Omni technical report**. Chunking is mandatory for our core.
- ⚠️ **Discrepancy to note**: the EMNLP 2025 speech-summarization survey's dataset table marks ICSI
  as *not* audio-bearing. That is inconsistent with the CC BY 4.0 signal release verified above; the
  survey column most likely means "audio not shipped in the summarization-benchmark packaging".
  Resolve before citing the survey table.

### 1.2 NOTSOFAR-1 (Microsoft)

- **Modality**: audio + transcript. **Both** single-channel (SC) and known-geometry **multi-channel
  (MC)** devices; MC is a 7-mic circular array. 5 SC + 4 MC devices per meeting. Close-talk
  reference audio appears present in the HF layout (**unverified**).
- **Size**: paper — **315 meetings**, ~6 min average, **30 conference rooms**, **35 unique
  speakers**, 4–8 attendees. CHiME-8 Task 2 released subset — ~280 meetings, ~150 h SC / ~110 h MC.
  As bundled into CHiME-8 DASR: **92.4 h train / 13.4 h dev / 20 h eval**. Plus a **simulated**
  training set of ~1000 h (or a 200 h subset) from 15,000 real acoustic transfer functions.
- **Language**: **English** (stated explicitly on the CHiME-8 Task 2 page).
- **Licence / obtainability**: **CC BY 4.0** (confirmed verbatim in the repo `LICENSE.txt`, licensor
  Microsoft). **Free.** The HF repo shows **no gating banner**, but the official download script
  requires an **`HF_TOKEN`** (free account, read scope) — so: free, no approval form, but a free
  account is expected by the sanctioned path. Also via `chime-utils dgen notsofar1 --download`.
- **Gold layers**: transcripts + **speaker attribution** ground truth (SegLST JSON in the CHiME-8
  packaging) + segment timestamps. **No summaries, QA, entities, or topic segmentation.**
- **Baselines**: official repo, dev-set-1, **tcpWER / tcORC-WER**: SC **46.8 / 38.5**;
  MC **32.4 / 26.7**. Interspeech 2024 paper (2401.08887) reports tcpWER **14.265%** MC /
  **22.989%** SC on CHiME-8 Dev-set-2.
- **Boundary note**: the ~1000 h simulated set is front-end acoustic simulation, **not**
  environmental-audio classification. Use only the real recorded subsets to stay clean.
- **Verdict**: **ADMIT.** English, free, permissive, modern office-meeting speech with
  speaker-attributed transcripts and published baselines. Best modern complement to ICSI. Weakness:
  very short meetings (~6 min) and no semantic layers — it cannot support a minutes claim.

### 1.3 CHiME-7 / CHiME-8 DASR bundle

- **CHiME-7 DASR** = CHiME-6 + DiPCo + Mixer 6. **CHiME-8 DASR** = those three **+ NOTSOFAR-1**.

| Corpus | Setting | Train / Dev / Eval | Speakers | Devices |
|---|---|---|---|---|
| CHiME-6 | dinner party, homes | 40 h / 4.4 h / 5.2 h | 32 | 6 Kinect far-field arrays (4 mics each) + binaural close-talk |
| DiPCo | dinner party | 1.2 h / 1.5 h / 2.6 h | 8 | 5 far-field 7-mic circular arrays + close-talk |
| **Mixer 6** | 1-to-1 interview | 234 h / 8.9 h / 5.75 h | 81 / 77 | 13 heterogeneous (3 close-talk + 10 far-field) |
| NOTSOFAR-1 | office meeting | 92.4 h / 13.4 h / 20 h | 14 (this packaging) | distant circular array (+ SC data) |

- **Language**: English throughout. **Metadata released as CC0 1.0.**
- **Obtainability**: `chime-utils dgen {chime6,dipco,notsofar1} --download` fetches all three
  **free**. ⚠️ **Mixer 6 Speech is NOT free** — licensed from **LDC (LDC2013S03)** via a PDF request
  form emailed to `ldc@ldc.upenn.edu`. **PAID / LDC-GATED → AUTO-EXCLUDED.** Any CHiME-7/8
  macro-average that includes Mixer 6 is therefore **not reproducible for us**.
- **CHiME-6 specifically**: now on **OpenSLR 150 under CC BY-SA 4.0** — train 97 G / dev 11 G /
  eval 12 G / transcriptions 2.4 M JSON / floorplans 1.4 M; free, direct, no form.
  ⚠️ **Licence conflict to resolve**: the legacy CHiME-6 site still routes CHiME-5 audio through a
  **Sheffield licence portal** (free for not-for-profits, **£2,000 commercial**), and a snippet
  claims `chime-utils` downloading implies agreeing to it — **not verified in the README itself**.
  Free for non-commercial research either way, but settle the governing licence before any
  redistribution or commercial use.
- **Gold layers**: transcripts + speaker labels + timestamps (JSON / SegLST). **No summaries, QA,
  entities, or topic segmentation** anywhere in the bundle.
- **Baselines (CHiME-8)** — extracted by automated page summarization, **treat as approximate**:
  tcpWER % (ESPnet) dev/eval — CHiME-6 88.6/99.1, DiPCo 98.3/56.6, Mixer 6 23.9/43.8,
  NOTSOFAR-1 46.2/50.7; (NeMo) — CHiME-6 56.5/73.8, DiPCo 75.8/57.1, Mixer 6 19.4/23.1,
  NOTSOFAR-1 61.0/72.0. The DiPCo dev 98.3 / eval 56.6 asymmetry looks anomalous — **flagged as
  suspect, re-verify before citing.**
- **Genre caveat**: CHiME-6 and DiPCo are **dinner-party / home conversational speech, not
  meetings** — in-boundary as human speech, but a genre mismatch for meeting understanding.
- **Verdict**: **ADMIT the free three; EXCLUDE Mixer 6.**

### 1.4 DiPCo (Dinner Party Corpus, Amazon)

- **Modality**: audio + transcript; close-talk mic per participant + **5 far-field 7-mic arrays**.
- **Size**: **10 sessions**, 15–45 min each, 4 participants each (8 unique speakers in the CHiME-8
  packaging), ≈5.3 h raw. Small.
- **Language**: English. **Licence**: **CDLA-Permissive 1.0**, free, **ungated**, direct from Zenodo
  (`DipCo.tgz`, 13.4 GB). Paper: arXiv 1909.13447, Interspeech 2020.
- **Gold layers**: human transcripts with speaker labels and timestamps. Nothing semantic.
- **Verdict**: **ADMIT (low weight).** Clean provenance, but tiny and dinner-party genre.

### 1.5 AliMeeting / M2MeT (+ M2MeT 2.0) — Mandarin

- **Modality**: audio + transcript; far-field **8-channel circular array** AND near-field headset.
- **Size**: 118.75 h (104.75 Train / 4 Eval / 10 Test); 212 / 8 / 20 sessions; 2–4 speakers/session;
  15–30 min sessions.
- **Language**: **Mandarin only** → not usable for the English primary path.
- **Licence**: **CC BY-SA 4.0**, free direct download, OpenSLR 119 (Train far 73.24 G, Train near
  22.85 G, Eval 3.42 G, Test 8.90 G) + Alibaba OSS mirror. No account, no form.
- **Gold layers**: TextGrid transcripts, speaker labels, segment timestamps, RTTM for VAD/diarization.
  Lhotse's recipe parses TextGrid for Train, Eval **and** Test. **No summaries, QA, entities, topics.**
- **Baselines**: DER **15.24%** on Eval-Ali-far (0.25 s collar, 8-ch) — secondary sources only,
  **needs verification**. ASR-track CER unverified.
- **M2MeT 2.0**: **ASRU 2023** (not ICASSP 2024), speaker-attributed ASR. New **Test-2023**: 10 h,
  10 sessions, 5 rooms, **58 speakers**, no speaker overlap with AliMeeting. Baselines **8.84%
  cpCER** (modular) vs **41.55% cpCER** (SA-Transformer end-to-end) — a striking modular-beats-e2e
  result. **Public availability of Test-2023 is unverified.**
- **Verdict**: in-boundary and free, **Mandarin-only → contrastive/secondary use only.**

### 1.6 AISHELL-4 — Mandarin

- **Modality**: audio + transcript; **8-channel circular array** (far-field); near-field headset
  references mentioned in secondary descriptions (**unverified** — the spec PDF would not parse).
- **Size**: **211 sessions, 120 h**, 4–8 speakers/session, 10 venues in three size classes
  (7×3×3 m to 15×7×3 m). Unique speaker count **unverified**.
- **Language**: **Mandarin only.** **Licence**: **CC BY-SA 4.0**, free direct download, OpenSLR 111
  (train_L 7.0 G, train_M 25 G, train_S 14 G, test 5.2 G).
- **Gold layers**: Praat **TextGrid** — anonymized speaker-id, gender, segment timestamps,
  character-level transcription with punctuation, non-speech markers (`[laugh]`, `[cough]`,
  `[breath]`), overlap flags; per-channel **VAD at 10 ms**; ~3 annotators/session. Nothing semantic.
- **Boundary note**: the non-speech tags are transcription markers inside human speech, **not** an
  audio-event classification task — in-boundary.
- **Verdict**: in-boundary and free, **Mandarin-only → secondary use only.**

### 1.7 MISP-Meeting — Mandarin, but the only corpus pairing meeting audio with human minutes

- **Paper**: *MISP-Meeting: A Real-World Dataset with Multimodal Cues for Long-form Meeting
  Transcription and Summarization*, Chen, Yang, Gu, Siniscalchi, Du — **ACL 2025 long**,
  `2025.acl-long.753`, pp. 15479–15492.
- **Modality**: audio + video + transcript. **8-channel far-field array + per-speaker headset +
  360° video.**
- **Size**: **125.15 h**, **163 real meetings**, **274 speakers**, **23 rooms**. (The paper text also
  describes a 119/3/3 h train/dev/eval split.)
- **Language**: **Mandarin.** (CER is the reported metric — 36.60% → **20.27%** via GSS +
  fine-tuning + audio-visual fusion.)
- **Licence / obtainability**: **CC BY-NC-ND 4.0**, "research-only, free upon authorisation".
  **Free but gated** — requires signing a licence agreement at `challenge.xfyun.cn/misp_dataset`
  before OSS download. Repo: `coalboss/MISP-Meeting`.
- **Gold layers**: sentence-level transcripts (>99% accuracy, ±100 ms boundaries), **human-refined
  brief summaries AND detailed summaries** (2-pass expert review), speaker demographics metadata.
  Explicit diarization labels not confirmed in the repo text.
- **Why it matters**: it is the **only** corpus found that pairs real long-form meeting audio with
  human-refined summaries at both granularities. The paper also reports an explicit link between ASR
  quality and summary coherence — directly our thesis.
- **Verdict**: **secondary because Mandarin**, but the single best structural template for what a
  speech-grounded minuting benchmark should contain. The ND clause restricts redistributing
  derivatives — check before publishing any derived glossary artifacts.

---

## 2. Transcript-only meeting resources — flagged, and why the flag matters

All records below were verified first-hand against the official paper, the authors' repository, or
the dataset's own landing page — never a single aggregator.

### 2.1 MeetingBank — English, and it DOES ship audio

- **Paper**: Hu, Ganter, Deilamsalehy, Dernoncourt, Foroosh, Liu — **ACL 2023**,
  `2023.acl-long.906` / arXiv 2305.17529.
- **Modality**: **audio + video + transcript.** This is the correction that matters most in this
  file — MeetingBank is widely treated as a text benchmark, but audio **is** distributed via
  HuggingFace (`huuuyeah/MeetingBank_Audio`) and Zenodo, and full video sits on archive.org in
  per-city collections (Alameda, Boston, Denver, Long Beach, King County, Seattle).
- **Size**: **1,366 meetings**, **>3,579 hours** of video, **6 major U.S. cities**, ~2.6 h per
  council meeting, >28 k tokens per transcript, **6,892 segment-level summarization instances**.
- **Language**: **English.**
- **Gold layers**: **professionally written human meeting minutes** (PDF), agenda, other metadata;
  divide-and-conquer alignment of minute passages to specific meeting segments; summaries from 6
  systems plus human annotations. Content scored with a **QA-based metric** rather than text overlap
  *(QAEval originates with Deutsch et al., TACL 2021 — do not attribute it to MeetingBank)*.
- **Licence**: **not stated on the landing page** (it defers to a `/license/` section that was not
  reachable in this sweep). ⚠️ **Must be confirmed before acquisition.** City-council proceedings are
  public record in the US, which is why the corpus exists, but that is not a licence statement.
- **Verdict**: **ADMIT — top pick for speech-grounded minutes gold**, conditional on confirming the
  licence. It is the only English corpus found that pairs real meeting audio at scale with
  professional human-written minutes.

### 2.2 ELITR Minuting Corpus + AutoMin — **transcript-only AND name-redacted**

- **Data**: ELITR Minuting Corpus 1.0 (ELMI) — 120 English meetings (109 h) + 59 Czech meetings
  (53 h); EuroParlMin 1.0 — ~2000 transcript–minute pairs; ELITR-Bench — 271 manually crafted QA
  pairs, professionally translated into Czech.
- **Modality**: **TRANSCRIPT-ONLY.** Verbatim from the AutoMin 2025 findings: *"No audio provided;
  only ASR-generated meeting transcripts supplied."* The hour figures describe the underlying
  meetings, not distributed audio.
- **Obtainability**: registration-based, de-identified.
- ⚠️ **The disqualifying detail for our direction**: names are replaced with `[PERSONnumber]`,
  `[ORGANIZATIONnumber]`, `[PROJECTnumber]`, `[LOCATIONnumber]`. **De-identification destroys exactly
  the signal an episode-local glossary is built from.** Entity work on ELITR is structurally
  impossible; only the minuting-format and QA-protocol lessons transfer.
- **Verdict**: **text-side reference only.** Valuable for protocol design (AutoMin's task
  definitions, its QA setting, its evaluation failures), useless as entity/glossary evaluation data.

### 2.3 ELITR-Bench (the QA layer)

- **Paper**: arXiv 2403.20262, **COLING 2025** (`2025.coling-main.28`); repo
  `utter-project/ELITR-Bench`.
- **Content**: 271 manually crafted questions + ground-truth answers over ELITR meeting transcripts,
  plus **noisy transcript variants targeting different WER levels** — a built-in ASR-robustness axis.
  Two settings: **ELITR-Bench-QA** (stand-alone questions) and **ELITR-Bench-Conv** (questions in a
  fixed conversational sequence). Question types: Who / What (incl. Why) / When / How many, with the
  **answer position annotated** (Beginning / Middle / End / Several passages).
- **Findings**: 12 long-context LLMs evaluated; models differ markedly in **robustness to transcript
  noise**.
- **Verdict**: **transcript-only**, but the WER-perturbation axis and answer-position annotation are
  directly reusable protocol ideas. Inherits the `[PERSONnumber]` redaction.

### 2.4 TCR (Topic-Conversation Relevance)

- **Paper**: Fan, Pool, Filipi, Cutler — **NeurIPS 2024 Datasets & Benchmarks**, arXiv 2411.00038.
- **Content**: **1,500 unique meetings**, 22 M words of transcripts, **>15,000 meeting topics**;
  built from newly collected Speech Interruption Meeting (SIM) data plus existing public datasets;
  ships scripts for generating synthetic/augmented meetings.
- **Modality**: **transcript-only.** Language not explicitly stated; context implies English
  (**unverified**).
- **Licence**: **CC BY 4.0**, open source.
- **Verdict**: text-side reference. Useful only if we need topic-segmentation gold at scale.

### 2.5 QMSum — text-side, audio upstream

- **Paper**: NAACL 2021, arXiv 2104.05938. 1,808 query–summary pairs over **232 meetings**, built
  over AMI, ICSI and committee/parliamentary meetings.
- **Modality**: **transcript-only as distributed.** Because its sources are AMI and ICSI, the
  underlying **audio is separately recoverable** — and, per §1.1, ICSI audio is now CC BY 4.0 and
  free. Whether QMSum's segment offsets realign cleanly to the source audio timeline is
  **unverified** and is the key engineering question if we want to make QMSum speech-grounded.
- **Scoring practice**: still primarily **ROUGE-L F1** — the practice `methods.md` recommends
  refusing as a headline.
- **Derived resource**: **QMSum Mistake** (COLING 2025, 2407.11919) — 200 summaries, 169 erroneous +
  31 controls, human-annotated over **nine error types**, spanning ICSI + AMI + parliament,
  Krippendorff's α = 0.793. This is the most directly reusable meeting-summary error taxonomy found.
- **Verdict**: **text-side reference with a real path to speech-grounding** via its ICSI/AMI
  ancestry. Confirm alignment recoverability before relying on it.

### 2.6 MediaSum — large, but not meetings

- **Paper**: *MediaSum: A Large-scale Media Interview Dataset for Dialogue Summarization*, Zhu, Liu,
  Mei, Zeng — **NAACL 2021**, arXiv 2103.06410. Repo: `zcgzcgzcg1/MediaSum`.
- **Content**: **463.6 K transcripts** with abstractive summaries, from **NPR and CNN** interview
  programs. Gold summaries are the broadcasters' own **overview and topic descriptions**, not
  purpose-written human annotations.
- **Modality**: **transcript-only**; no audio distribution mentioned. Licence not stated on the
  paper page.
- ⚠️ **These are broadcast interviews, not meetings.** Multi-party, but hosted, turn-regulated, and
  professionally produced — none of the overlap, disfluency or far-field conditions that make
  meetings hard.
- **Verdict**: **out of scope for our direction.** Listed because the mission named it and because
  it is frequently mislabelled as meeting data. Its scale makes it a text-side pretraining resource
  at best; the derived-summary provenance also makes its gold weak.

### 2.7 VCSUM — the richest annotation stack, wrong language

- **Paper**: *VCSUM: A Versatile Chinese Meeting Summarization Dataset*, Wu, Zhan, Tan, Hou, Liang,
  Song — **ACL 2023 Findings**, `2023.findings-acl.377` / arXiv 2305.05280. Repo: `hahahawu/VCSum`.
- **Content**: **239 real-life meetings, >230 hours** — larger in duration than AMI and ICSI
  combined.
- **Language**: **Chinese.**
- **Gold layers — the most complete of any meeting summarization corpus found**: **topic
  segmentation, headlines, segmentation summaries, overall meeting summaries, and salient
  sentences.** Explicitly designed to support segmentation-based, multi-granularity, and
  retrieve-then-generate summarization.
- **Modality**: the 230-hour figure describes the meetings; the repo's data structure section
  mentions **meeting transcripts only**, and **audio distribution is not confirmed** (unverified —
  this is the deciding question for any speech-grounded use).
- **Licence**: repository shows **MIT** (likely the code licence; whether it governs the data is
  **unverified**). Acquisition route not described on the repo page.
- **Verdict**: **secondary on language**, but its multi-granularity annotation design is the best
  available template for what our minutes gold should look like — headline + segment summary +
  overall summary + salient sentences is exactly the decomposition a minutes agent should be scored
  on.

---

## 3. 2025–2026 newcomers

This was the highest-value part of the sweep. Two structural findings frame it:

- **No major new *English* meeting corpus appeared in 2025–2026.** The new meeting-domain corpora
  are Mandarin (MISP-Meeting, SmartGlasses) or bilingual with a small English slice (MeetBench-XL).
- **There is no English audio-bearing meeting-QA gold benchmark in wide use.** A direct search for
  one returned nothing; the audio QA benchmarks that exist are either generic short-clip
  (AudioBench, MMSU, MMAU) or Mandarin. **M3-SLU is the closest thing to an exception** and is
  therefore disproportionately important to us.

### 3.1 SLT 2026 SmartGlasses Challenge — arXiv 2608.12034 (2026-08-12)

- **Modality**: audio only, **4-channel MEMS array** on customized smart glasses (left/right
  temples), 16 kHz / 16-bit. **Language: Mandarin only.**
- **Size**: **106.98 h, 714 sessions, 88 speakers** (42 M / 46 F).
  - Track 1 (dyadic): 518 sessions, 44.95 h, avg 312.4 s, overlap 7.5% (max ~35%), 1560 QA pairs.
  - **Track 2 (multi-party meeting): 196 sessions, 62.03 h, avg 1139.3 s (~19 min), overlap 13.6%
    (max ~45%), 1949 QA pairs.**
- **Gold layers**: time-stamped speaker-attributed transcription + **3,509 four-option SLU MCQs**,
  balanced across acoustic / semantic / joint categories (speaker ID, intent, key-information
  retrieval, sarcasm, sentiment, pragmatic disambiguation).
- **Metrics**: **tcpCER** (time-constrained polyphonic CER, 5 s collar) + MCQ accuracy.
- **Obtainability**: official challenge website; licence/cost not stated in the paper. Informed
  consent and pseudonymous speaker IDs.
- **Why it matters to us despite being Mandarin**: its SLU baseline is **Qwen3-Omni-30B-A3B — our
  exact core** — scoring **69.9%** (Track 1) and **65.9%** (Track 2, 19-min multi-party meetings).
  That is a published, third-party, meeting-scale number for our frozen model on a
  speaker-centric understanding task. Top submission (MOSS Transcribe Diarize: Whisper-large-v3
  encoder + Qwen3-8B decoder) reached 5.23% tcpCER and 88.8% SLU on Track 1; the VibeVoice-ASR
  baseline degraded to **57.81% tcpCER** on Track 2, showing how hard multi-party meeting length is.
- **Verdict**: secondary on language, but **cite the Qwen3-Omni baseline** — it is the cleanest
  public evidence of our core's meeting-understanding ceiling.

### 3.2 M3-SLU — arXiv 2510.19358, **LREC 2026** — the meeting-QA gold candidate

- **Title**: *M3-SLU: Evaluating Speaker-Attributed Reasoning in Multimodal Large Language Models*
  (Kwon, Kang, Yoon, Kim; submitted 2025-10-22).
- **Modality**: **audio + transcript + metadata** — "over **12,000 validated instances** with paired
  audio, transcripts, and metadata". Not transcript-only.
- **Sources**: **CHiME-6, MELD, MultiDialog, AMI.** Per-corpus instance counts not stated in the
  abstract (**unverified**). Language not explicitly stated; sources are English (**unverified**).
- **Tasks**: (1) **Speaker-Attributed Question Answering**; (2) **Speaker Attribution via Utterance
  Matching**. Scored by accuracy plus LLM-as-Judge.
- **Headline finding**: models "capture what was said [but] often fail to identify **who** said it" —
  our thesis, stated by a third party, on public data.
- **Release status / licence**: **unverified** — no repo or licence found on the abstract page. This
  is the single most important open question in this file.
- **Verdict**: **ADMIT as the primary task-level benchmark if release is confirmed.** Audio-bearing,
  AMI-derived, English, speaker-attributed, and scoreable without gold labels at runtime. Nothing
  else found fills the meeting-QA-gold gap.

### 3.3 MeetBench-XL / MeetAll — arXiv 2602.03285 (2026-02-03)

- **Modality**: **audio + transcript** — "200 h bilingual (English & Mandarin) audio with
  high-quality transcripts"; agent utterances synthesized with F5-TTS voice cloning.
- **Size**: **231 enterprise meetings, 140 h** (paper) / 200 h audio (repo — figures disagree,
  **flagged**). English slice = **20 CHiME-6 meetings, ~40 h, 382 queries**; the remaining ~160 h is
  Mandarin. **1,180 human-verified agent QA turns.**
- **Gold layers**: transcripts, speaker context, QA turns; evaluation over **factuality, user-need
  satisfaction, conciseness, structure, completeness**; corpus designed along cognitive load,
  temporal context span, domain expertise, actionable task execution.
- **Licence**: ⚠️ **conflicting** — the arXiv page states CC BY 4.0, the repo states **CC BY-NC 4.0
  (non-commercial research only)** for the MeetAll data (code Apache-2.0). **Treat as NC.** Hosted at
  HF `YueLinHu/MeetAll-v2` with SHA-256 shard checksums; direct download, not obviously gated.
- **System**: MeetMaster XL, a **learned dual-policy agent** routing between fast and slow reasoning
  paths and invoking tools (retrieval, cross-meeting aggregation, web search). Scores 6.59/10 vs
  3.30–6.56 for Llama/Qwen/DeepSeek/Phi/ChatGLM variants.
- **Verdict**: **ADMIT with the NC caveat.** The English slice is small (~40 h, and it is CHiME-6
  again rather than new meeting audio), but the 1,180 QA turns and the real-time agent framing are
  directly on our direction. Note it is a *learned* agent — a trained baseline we would be
  positioning a zero-training system against.

### 3.4 MSU-Bench — arXiv 2508.08155 (2025-08-11)

- **Modality**: audio-bearing, but **60–120 s clips only**, each with ≥2 speakers.
- **Sources**: English — MDT-AD015 (telephone, 5 h), **CHiME-6** (6 h sampled), en-Film (~41 h);
  Mandarin — MDT-AA007 (5.2 h), **AliMeeting** (4 h sampled), cn-Film.
- **Structure**: four tiers — single-speaker static attributes → single-speaker dynamic attributes →
  multi-speaker background → **multi-speaker interaction** (multi-speaker transcription with accurate
  attribution, paralinguistic/social interaction analysis, cross-speaker reasoning). **1,232
  questions across 25 tasks**, open-ended with an LLM judge scoring relevance, accuracy, causal
  soundness (0–1 scaled).
- **Results**: Gemini-2.5-Pro 0.59 > Gemini-2.5-Flash 0.55 > GPT-4o-Audio 0.52 > **Qwen2.5-Omni
  0.37** > Kimi-Audio 0.35. All models decline sharply as tier complexity rises; Tier 4 is the worst
  for every model.
- **Release**: `github.com/ASLP-lab/MSU-Bench` + demo page; licence stated only as the arXiv
  perpetual non-exclusive licence (**dataset licence effectively unverified**).
- **Verdict**: secondary — clip length (≤2 min) makes it a multi-talker SLU probe, not a meeting
  benchmark. But Tier 4 is a clean, published measurement of exactly the capability we target, and
  the Qwen-family number is a useful positioning anchor.

### 3.5 AutoMin 2025 (third challenge) — arXiv 2509.13814

Covered in §2.2 and in `methods.md` §1.1/§4.1. Headline dataset facts: **transcript-only**,
name-redacted, English + Czech, project meetings + European Parliament, and it added a **meeting QA
task** (monolingual + cross-lingual) built on ELITR-Bench.

### 3.6 Adjacent long-audio benchmarks (not meetings, tracked for context)

| Benchmark | ID | Content | Relevance |
|---|---|---|---|
| **VoiceGiraffe** | 2605.27976 | **Hour-level** audio-language understanding, 1500 triplets, single/multi-hop; podcasts and long speeches | The motivating citation for episode-local state: "far from saturation", **long-range memory persistence is the named bottleneck** |
| **LongSpeech** | 2601.13539 | 100 k+ segments of ~10 min, 8 tasks (ASR, translation, summarization, language ID, speaker counting, content separation, QA); ICASSP 2026 | Largest long-form pipeline; **speaker counting** and **content separation** are meeting-adjacent |
| **AudioMarathon** | 2510.07293 | 90–300 s, 10 sub-tasks | Evidence that the field's "long" audio is 5 minutes |
| **ChronosAudio** | 2601.04876 | long-audio LALM benchmark | not verified in depth |
| **Speech-XL** | 2602.05373 | long-form speech understanding | not verified in depth |
| **GlobeAudio** | 2606.08194 | multilingual/multicultural LALM benchmark | not verified in depth |
| **AMUSE** | 2512.16250 | Agentic multi-speaker audio-visual, 6 task families incl. multimodal dialogue summarization; **CC BY 4.0** | Names GPT-4o and **Qwen3-Omni** as struggling in multi-speaker dialogue settings |
| **Contextual Earnings-22** | 2604.07354 | Earnings-22 + realistic custom-vocabulary contexts; six baselines split across **keyword prompting vs keyword boosting** | **Directly the glossary-injection evaluation vehicle**, and our program already pins `earnings22-original` |
| **NUTSHELL / SLUE-TED** | 2502.16942 / SLUE-2 | Talk audio + abstracts (ACL talks; TED talks 829 h) | English audio + summary gold, but **single-speaker talks, not meetings**. TED content is CC BY-NC-ND 4.0. Fallback only |

---

## 4. Acquisition shortlist and what each fills

Ranked by what gap it closes for a speech-grounded meeting-minutes agent.

1. **MeetingBank** — English, audio + video + transcript, 1,366 meetings / 3,579 h, professional
   human-written minutes with segment alignment. **Fills: speech-grounded minutes gold in English.**
   Nothing else does. Blocker: confirm the licence.
2. **ICSI Meeting Corpus** — English, CC BY 4.0, ungated, 75 meetings / ~72 h / 53 speakers, with
   abstractive + extractive summaries, **named entities**, topic segmentation, dialogue acts.
   **Fills: the only free permissive corpus with entity and summary gold on real meeting audio.**
   Caveat: ~1 h meetings exceed our core's 40-minute window.
3. **M3-SLU** — audio-bearing speaker-attributed QA over AMI/CHiME-6, >12,000 instances, LREC 2026.
   **Fills: meeting-QA gold with speaker attribution** — the one benchmark whose headline finding is
   our thesis. Blocker: confirm public release and licence.
4. **NOTSOFAR-1** — English, CC BY 4.0, modern office meetings, SC + MC, speaker-attributed
   transcripts, published tcpWER baselines. **Fills: a modern, permissive, speaker-attributed
   transcription substrate with a comparable public baseline.** No semantic layers.
5. **Contextual Earnings-22** — Earnings-22 with realistic custom-vocabulary contexts and published
   keyword-prompting vs keyword-boosting baselines. **Fills: a named, published baseline for
   glossary injection**, on a corpus the program already pins — turning "keyword prompting" from an
   ad-hoc idea into a beatable prior.

**Runners-up**: MeetBench-XL (agent QA turns, but NC and only ~40 h English); MISP-Meeting (the best
structural template for minutes gold, but Mandarin and ND); CHiME-6 + DiPCo (free English audio,
wrong genre); SLT 2026 SmartGlasses (Mandarin, but carries the Qwen3-Omni meeting baseline).

**Excluded**: Mixer 6 (LDC/paid), Ego4D and Ego-Exo4D (approval-gated, not meeting-style, heavy
ambient audio at the edge of our boundary), and any How2 / Spotify Podcast route (**both are no
longer publicly available**, per the EMNLP 2025 survey).

## 5. Open verification debts

1. **MeetingBank licence** — not stated on the landing page; must be confirmed before acquisition.
2. **M3-SLU release status and licence** — no repo/licence found; the whole of recommendation #3
   depends on it.
3. **ICSI far-field channel map** — chanC–chanF verified present, letter→microphone mapping not.
4. **ICSI audio column in the EMNLP 2025 survey table** contradicts the CC BY 4.0 signal release.
5. **CHiME-6 governing licence** — OpenSLR CC BY-SA 4.0 vs the legacy Sheffield CHiME-5 agreement.
6. **MeetBench-XL size and licence conflicts** — 140 h (paper) vs 200 h (repo); CC BY 4.0 (arXiv)
   vs CC BY-NC 4.0 (repo).
7. **QMSum → AMI/ICSI audio realignment** — whether segment offsets survive back to the audio
   timeline is unverified and decides whether QMSum can be made speech-grounded.
8. **M2MeT 2.0 Test-2023 public availability** — no release location found.
9. **AliMeeting DER 15.24% and AISHELL-4 baselines** — secondary sources only.
10. **CHiME-8 baseline table** — automated extraction, with a suspect DiPCo dev/eval asymmetry.
