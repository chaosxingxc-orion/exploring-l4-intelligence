# Local data audit vs the meeting-minutes agent requirements matrix

Campaign: `2026-08-17-meeting-agent-direction`
Date: 2026-08-17
Scope: read-only audit of LOCAL holdings only. No downloads, no model contact, no installs, CPU only.
Data root: `$SPEECHRL_DATA_DIR` = `/mnt/e/chao_workspace/exploring-l4-intelligence/speechrl-data`
Identity source: umbrella `docs/datasets.lock.json` (28 `datasets` entries + 69 `asset_catalog` entries).

Direction under audit: a meeting-minutes agent performing speaker decomposition, per-speaker
content, coreference/relations, and an episode-local keyword/glossary table maintained for static
prompt injection.

This document is an exploration workbench note, not a decision record. It states what is on disk
and what is not; it does not authorize acquisition, execution, or any model contact.

---

## 1. Requirements matrix

Requirements: (1) multi-speaker audio; (2) speaker labels / diarization gold or per-speaker
channels; (3) minutes/summary gold; (4) meeting-QA gold; (5) entity/keyword annotations;
(6) topic segmentation / dialogue acts; (7) English; (8) length and domain.

Legend: `YES` = present and usable as gold; `PART` = present but materially limited;
`NO` = absent on disk.

| Corpus (on disk) | 1 multi-spk audio | 2 speaker labels | 3 minutes/summary gold | 4 meeting-QA gold | 5 entity/keyword | 6 topic seg / DA | 7 English | 8 length + domain |
|---|---|---|---|---|---|---|---|---|
| **AMI** (`datasets/ami`) | YES 171 meetings, 4-5 spk, single Mix-Headset mixdown | YES per-speaker `segments` with `transcriber_start/end`, 171/171 meetings; PART no per-speaker channels (Mix-Headset only) | **YES 142 meetings** abstractive, 4 sections; 137 extractive | **NO** | PART 117 meetings, 16,347 typed NE, but scenario-object ontology | YES topics 139, dialogue acts 139, adjacency pairs 139 | YES | 100.0 h, mean 35.1 min; scenario design meetings (remote-control task) + 33 non-scenario |
| **Earnings21 + ConEC-e21** | YES 44 calls, mean 10.6 speakers/call | **YES** RTTM diarization gold 44/44 + `speaker-metadata.csv` 410 real names / 56 placeholders | **NO** | **NO** | **YES** ConEC per-call biasing lists (mean 790 lines) + participant names with affiliations + `wer_tags` entity classes | NO (no section field; `Operator` heuristic in 35/44) | YES | 39.26 h, mean 53.5 min (18.3-95.7); earnings calls, 9 sectors |
| **Earnings22 + ConEC-e22** | YES 125 calls, speaker index 0..26 | PART speaker index + force-aligned timestamps; no names, no RTTM | **NO** | **NO** | PART ConEC corrected transcripts + 100 PDFs only; no biasing lists, no participant names | NO | YES (accented, global) | 118.89 h, mean 57.1 min; earnings calls, global accents |
| **ContextASR-Dialogue English** | YES 5,273 dialogues, 3-5 named roles | YES per-turn `role` + `start`/`end` | **NO** | **NO** | **YES** per-episode `entity_list`, mean 11.1 entities | PART `movie_name` topic anchor; no DA | YES | 221.9 h, mean 151.5 s; TTS-synthesized casual chat |
| **ContextASR-Speech English** | NO single speaker | NO | NO | NO | YES `entity_list` + `domain_label` | PART `domain_label` | YES | 15,326 clips; synthetic monologue |
| **SLUE-SQA-5** | NO single-speaker documents | PART `document_speaker_id` | NO | PART spoken QA with `answer_spans` + `word2time`, but NOT meetings | NO | NO | YES | 110 GB, 299 parquet |
| **SlideASR-Bench** | NO | NO | NO | NO | PART slide images as context | NO | mixed | 8,467 wav + 8,467 jpg |
| all other local corpora | see section 5 | | | | | | | |

**One-sentence read of the matrix.** Exactly one local corpus (AMI) carries minutes gold, exactly
one local corpus family (Earnings21+ConEC) carries a real per-episode glossary with speaker
identity, and **no local corpus carries meeting-QA gold at all**.

---

## 2. AMI deep dive

### 2.1 What is on disk

```
$SPEECHRL_DATA_DIR/datasets/ami/
  amicorpus/<MEETING>/audio/<MEETING>.Mix-Headset.wav     171 files, 11 GB
  annotations/ami_public_manual_1.6.2.zip                 22,887,865 B, 5,183 entries
  annotations/ami_public_auto_1.5.1.zip                   71,762,278 B, 4,312 entries
  CCBY4.0.txt, ami-all-meetings-mix-headset-20260802.manifest.txt, .speechrl-asset.json
```

Audio, measured from WAV headers (no decode): 171 files, **100.0 h total**, mean 35.1 min,
median 35.6 min, min 8.0 min (`IS1002b`-class short sessions), max 90.3 min. 170 files are
mono 16 kHz 16-bit PCM, 1 is stereo. Meeting families: ES 60, TS 40, IS 38, EN 16, IN 10, IB 7.

**Audio variants: Mix-Headset ONLY.** Individual headsets (IHM), lapel microphones, microphone
arrays and video were deliberately excluded at acquisition time; the lock records this as a
scope decision, not missing bytes ("This catalog identity intentionally excludes individual
headsets/lapels, microphone arrays and video"). Consequence for this direction: **there are no
per-speaker channels on disk.** Speaker decomposition against AMI must be done from the mixdown,
with the `segments` layer as gold. If per-speaker channels are wanted, IHM is a re-fetch.

### 2.2 The annotation release WAS fetched

This was the open question. Answer: **yes, both official annotation zips are present**, and they
were verified at acquisition (CRC PASS on both, recorded in the lock). They are **still archived,
not extracted** - the `ami/` tree contains only `amicorpus/` and `annotations/`, no unpacked
annotation directory. Everything below was read directly out of the zips with `zipfile`.

### 2.3 Per-layer presence, with file evidence

Manual release `ami_public_manual_1.6.2.zip`. "meetings" = distinct meeting IDs carrying that
layer; "on disk" = of those, how many have their Mix-Headset WAV present.

| Layer | zip path pattern | meetings | on disk | orphaned |
|---|---|---|---|---|
| Word-level transcript | `words/<M>.<S>.words.xml` | 171 | 171 | 0 |
| Speaker segments (turn times) | `segments/<M>.<S>.segments.xml` | 171 | 171 | 0 |
| **Abstractive summary** | `abstractive/<M>.abssumm.xml` | **142** | 142 | 0 |
| **Extractive summary** | `extractive/<M>.extsumm.xml` | **137** | 137 | 0 |
| Extractive-to-abstractive link | `extractive/<M>.summlink.xml` | 137 | 137 | 0 |
| **Topic segmentation** | `topics/<M>.topic.xml` | **139** | 139 | 0 |
| **Dialogue acts** | `dialogueActs/<M>.<S>.dialog-act.xml` | **139** | 139 | 0 |
| Adjacency pairs | `dialogueActs/<M>.adjacency-pairs.xml` | 139 | 139 | 0 |
| **Named entities** | `namedEntities/<M>.<S>.ne.xml` | **117** | 117 | 0 |
| Participant summaries | `participantSummaries/<M>.<S>.summ.xml` | 89 | 89 | 0 |
| Decisions | `decision/manual/<M>.decision.xml` | 47 | 47 | 0 |
| Argument structures | `argumentation/**/<M>.<S>.argumentstructs.xml` | 95 | 95 | 0 |
| Discussions | `argumentation/**/<M>.discussions.xml` | 95 | 95 | 0 |
| Participant roles | `participantRoles/<M>.<S>.role.xml` | 5 | 5 | 0 |
| "You" usages (partial reference resolution) | `youUsages/<M>.<S>.you.xml` | 16 | 16 | 0 |
| Disfluency | `disfluency/` | 40 | 40 | 0 |
| Gesture / head / movement / focus | `handGesture/`, `headGesture/`, `movement/`, `focus/` | 14-125 | - | - |
| Corpus resources | `corpusResources/meetings.xml`, `participants.xml` | all | - | - |

**Zero orphans on every layer.** Every annotated meeting has its audio locally. The fetch closed
cleanly.

**Coreference is absent.** The 1.6.2 manual release ships no coreference layer: top-level
components are exactly `dialogueActs, segments, words, argumentation, movement, namedEntities,
participantSummaries, extractive, headGesture, disfluency, abstractive, topics, corpusdoc,
youUsages, handGesture, focus, decision, participantRoles, ontologies, configuration,
corpusResources`. The closest local proxy is `youUsages` (16 meetings) which resolves second-person
pronoun reference only. Since the direction names coreference/relations explicitly, this is a
real gap - see section 6.

Automatic release `ami_public_auto_1.5.1.zip` adds: ASR output (`ASR/ASR_AS_CTM_v1.0_feb07`,
169 meetings, all on disk), automatic word alignment (169), phonemes (169), automatic dialogue
acts (43 meetings x 4 speakers), automatic disfluency (275 x 4), and
`PlainText-format/AutomaticTopicSegmentation` (170 meetings, 169 on disk) plus
`PlainText-format/ExtractiveSummaries`. This is a ready-made *automatic* baseline layer to
compare an agent against, without running any model.

### 2.4 The summary gold is shaped like minutes

`abstractive/<M>.abssumm.xml` is not a flat paragraph. All 142 files carry **all four sections**:

- `<abstract>` - narrative summary
- `<actions>` - action items / assignments
- `<decisions>` - decisions taken
- `<problems>` - open problems

Mean 288 words per meeting summary (median 288, min 84, max 652). Example (`ES2002a`):
decisions include "The remote will sell for 25 Euro."; actions include "The industrial designer
will work on the working design of the remote."

This maps almost one-to-one onto a minutes schema. It is the single most valuable local asset for
this direction.

`extractive/<M>.extsumm.xml` selects gold dialogue-act units, and `summlink.xml` links extractive
units to abstractive sentences - i.e. **sentence-level provenance from each minutes sentence back
to the utterances that justify it**. That is directly usable as evidence-grounding gold.

### 2.5 Speaker, topic and entity layers

- `segments`: per-speaker XML with `transcriber_start` / `transcriber_end` in seconds. Speakers
  per meeting: 4 in 168 meetings, 5 in 3. This is diarization/attribution gold on the mixdown.
- `corpusResources/meetings.xml`: per meeting `type` (scenario 138 / nonscenario 33), `dateOnly`,
  `duration`, and per speaker `nxt_agent` (A-D), `channel`, `global_name`, and **`role`**
  (`PM` project manager / `ID` industrial designer / `ME` marketing expert / `UI` user-interface
  designer, 138 meetings each). Participant-role metadata is therefore free.
- `corpusResources/participants.xml`: `sex`, `age_at_collection`, `native_language`, and an
  `english_language` region/residency element.
- `topics/<M>.topic.xml`: hierarchical topic segments carrying a free-text `other_description`
  (e.g. "introduction of participants and their roles", "project goals and design process") plus a
  pointer into a scenario topic-type ontology. Segments are stand-off word-ID ranges spanning
  multiple speakers.
- `namedEntities`: 16,347 instances across 117 meetings (mean 140/meeting, min 14, max 536);
  18.3% are multi-word spans.

**Caveat on the AMI entity layer, and it matters.** The NE ontology is dominated by
scenario-object classes, not proper nouns:

```
CARDINAL 24.8%  DRAWING 14.4%  MEANS_OF_WORKING 7.3%  MATERIALS 6.8%  MEASURE 6.6%
COLOUR 5.9%  CONSTRUCTED 5.5%  SHAPE 4.4%  MONEY 4.0%  DURATION 3.5%  OTHER 3.4%
... LOCATION 1.2% (196)  ORGANIZATION 1.0% (168)  DATE 1.0%  TIME 0.3%
participant-role PERSON classes (PM/ID/ME/UI) ~1,101 combined
```

A "glossary / keyword table" claim measured on AMI's NE layer would largely be measuring numbers,
colours and shapes - a different construct from the rare proper-noun / jargon terminology that
motivates episode-local glossaries. AMI is the right corpus for **minutes**, and a weak corpus for
**glossary-loop entity accuracy**.

### 2.6 Partitions: two conventions, do not conflate

- Yesterday's carrier manifest
  `derived/carrier-manifests/2026-08-17/ami-dev-partition.manifest.json` uses the
  **AMI full-corpus ASR partition (train 135 / dev 18 / eval 16)**: dev = 18 meetings,
  34,801.8 s = 9.667 h, 0 missing, and it records that all 16 eval meetings are also on disk.
  Its own `partition_provenance` field is honest that the list was
  "published-standard-list-transcribed; NOT sourced from a shipped file".
- `corpusResources/meetings.xml` inside the manual zip carries a *different* field, `seen_type`:
  training 98 / development 20 / unmarked 53.

These two do not agree and are not meant to. Any split used for this direction must name which
convention it follows. Because the manifest's list is transcribed rather than shipped, a
machine-checkable derivation of the ASR partition from local bytes alone is not currently possible.

### 2.7 Usable subsets

| Subset | meetings | hours |
|---|---|---|
| All Mix-Headset audio | 171 | 100.0 |
| + abstractive summary | 142 | 75.1 |
| + abssumm AND topics AND NE AND dialogue acts (full stack) | **109** | **54.9** |

The 29 audio meetings without any abstractive summary are the EN/IB/IN non-scenario sessions
(`EN2001a`, `EN2002a`, `IB4001`, `IN1001`, ...).

### 2.8 AMI verdict

**AMI is a genuine, complete, locally-resident minutes corpus and the prime candidate is
confirmed.** Both official annotation zips were fetched and CRC-verified; every annotation layer
this direction needs for minutes - abstractive (structured as abstract/actions/decisions/problems),
extractive with provenance links, topic segmentation, dialogue acts, per-speaker turn timing,
participant roles and demographics - is present with zero orphans, on 142 meetings / 75.1 h
(109 / 54.9 h for the full stack).

Three qualifications, all material:

1. **No per-speaker channels.** Mix-Headset only, by acquisition design. Speaker decomposition is
   a mixdown problem here.
2. **No coreference layer, and no QA layer.** The direction names both; AMI 1.6.2 supplies neither.
3. **The NE layer is scenario-object-centric**, so it is not a good proving ground for the
   glossary/terminology loop.

One engineering note: the annotations are **NXT stand-off XML**. A summary points at dialogue acts,
dialogue acts point at word-ID ranges (`<nite:child href="ES2002a.A.words.xml#id(...)..id(...)"/>`),
and words carry the times. Producing a speaker-attributed, time-aligned transcript plus aligned
minutes therefore requires a pointer-resolution pass over the ID ranges. That is real work; it is
not a `load_dataset` call. Extracting the zips costs ~90 MB.

---

## 3. Earnings21 / Earnings22 / ConEC as meeting-like data

### 3.1 Earnings21 (`datasets/earnings21-22/earnings21`) - 44 calls, 39.26 h, mean 53.5 min

Domain spread is deliberately balanced: 9 sectors, 5 calls each except Conglomerate with 4
(Utilities, Technology, Services, Industrial Goods, Healthcare, Financial, Consumer Goods,
Basic Materials, Conglomerate).

Speaker attribution is unusually strong for a public ASR corpus:

- `rttms/` - **44 RTTM files, i.e. diarization gold** with time-aligned speaker turns. Speakers
  per call: min 2, max 20, **mean 10.6**. These are genuinely many-party sessions. The count is
  corroborated independently by the `unique_speakers` column of `earnings21-file-metadata.csv`
  (mean 10.6, max 20), which was derived without reading the RTTMs.
- `speaker-metadata.csv` - 465 rows of `file_id, speaker_id, speaker_name`, mapping the transcript
  speaker index to a **real name**. 410 rows are real names ("Larry Culp", "Carolina Dybeck Happe");
  56 are placeholders (`Speaker N`, `Operator`). So roughly 88% of speaker slots are name-resolved.
- `earnings21-file-metadata.csv` - `company_name`, `financial_quarter`, `sector`,
  `speaker_switches`, `unique_speakers`, `audio_length`, `sample_rate`, `curator_id`.
- `transcripts/nlp_references/*.nlp` - pipe-delimited, columns
  `token|speaker|ts|endTs|punctuation|case|tags|wer_tags`. The `speaker` column is populated;
  `ts`/`endTs` are **empty** in the references (time comes from the RTTMs, or from ConEC's
  `timestamps/` variant, or from the vendor outputs).
- `transcripts/wer_tags/*.wer_tag.json` (44) - entity-type per tag id.
- `transcripts/normalizations/*.norm.json` (44) - normalization candidates with probabilities.
- `bias_lists/` - `oracle_list.txt` (1,013 lines) and `distractor_list.txt` (1,782 lines):
  a ready-made contextual-biasing evaluation setup.
- `output/` - 6 commercial/open ASR system outputs (`amazon`, `google`, `kaldi_org`, `microsoft`,
  `rev`, `speechmatics`, 444 files) **with** per-token timestamps. Free external baselines.

Entity annotation reality check. The tag vocabulary over all 44 reference transcripts is:

```
CONTRACTION 10,177   FALLBACK 2,549   ABBREVIATION 2,062   CARDINAL 1,994   PERCENT 1,402
YEAR 1,212   ALPHANUMERIC 912   MONEY 847   ORDINAL 85   WEBSITE 50   RANGE 13   TIME 6   TWITTER 2
```

These are **normalization / WER-scoring classes, not proper-noun NER**: there is no PERSON,
ORGANIZATION or PRODUCT class in the `tags` column. The proper-noun terminology for these calls
comes from ConEC and from `bias_lists`, not from the `tags` column.

### 3.2 Earnings22 - 125 calls, 118.89 h

- `transcripts/nlp_references` (125) and `transcripts/force_aligned_nlp_references`
  (with real `ts`/`endTs`, ~5.1k timestamped tokens in the files sampled). Speaker index present
  (observed 0..26 in one call).
- `metadata.csv` columns are `File ID, Ticker Symbol, Country by Ticker, UN Defined,
  Major Dialect Family, Language Family + Area Based, File Length (seconds), Sampling Rate` -
  accent/geography metadata, **no speaker names, no sector, no participant list**.
- **No RTTM, no `speaker-metadata.csv`, no bias lists.** The lock already records the limitation:
  "No Earnings21-equivalent token entity annotations."

So E22 gives scale and accent diversity with speaker *indices*, but not speaker *identity*.

### 3.3 ConEC (`datasets/conec`) - the glossary substrate

| | ConEC/earnings21 | ConEC/earnings22 |
|---|---|---|
| corrected `nlp_references` | 44 | 125 |
| `timestamps/` | 45 | **0** |
| `wer_tags/` | 44 | **0** |
| context biasing `*.txt` | **44** | **0** |
| `participant_names/` | **45** | **0** |
| `pdfs/` (slides + press releases) | 66 | 100 |

ConEC's earnings21 side is complete and is exactly the shape this direction needs:

- **Per-call biasing word lists**: mean 790 lines, median 700, min 104, max 2,252. Extracted from
  the call's own slides/press release, stopwords and numerics removed, participant names appended.
  This *is* an episode-local keyword/glossary table, supplied as gold.
- **Participant names with affiliations**: 990 lines over 45 files (mean 22, median 9, max 564),
  formatted `Name - Role/Affiliation`, e.g. `Brett Ponton - President and CEO`,
  `Brian Nagel - Oppenheimer`. Combined with Earnings21's `speaker-metadata.csv`
  (index to name) this closes the loop from a diarized turn to a named, affiliated participant.
- **Corrected references**: ConEC fixes `<unk>`/`<inaudible>` and homophone errors on named
  entities in the original Rev transcripts - i.e. the entity gold is cleaner than upstream.
- **Slide/press-release PDFs**: the raw external-evidence documents, per call.

Lock caveat retained: ConEC construction "relied partly on non-public S&P transcripts and cannot be
independently regenerated".

### 3.4 Q&A-section structure

There is **no explicit section field** anywhere in the E21/E22 formats; the `.nlp` header is
`token|speaker|ts|endTs|punctuation|case|tags|wer_tags` with no segment column. Evidence for
structure is only lexical: the literal string "question-and-answer" appears in 4/44 E21 reference
transcripts, and "Operator" appears in 35/44. So prepared-remarks vs Q&A can only be *heuristically*
inferred (operator-turn boundaries), never read off gold. Anyone claiming a Q&A-structure result
would have to build and defend that segmenter.

### 3.5 Verdict on the glossary-loop MECHANISM substrate

**Yes - Earnings21 + ConEC-e21 is sufficient, and it is the best local substrate for the
mechanism, precisely because no minutes gold is needed to measure it.**

It supplies, per episode, all four things the loop needs: (i) real multi-party speech
(mean 10.6 speakers, 44 calls, 39.26 h); (ii) gold speaker turns (RTTM) plus named, affiliated
participants (`speaker-metadata.csv` + ConEC `participant_names`); (iii) a gold episode-local
glossary (ConEC biasing list, mean 790 terms) with an oracle/distractor split already built
(`bias_lists/`); and (iv) a corrected entity-bearing reference to score against. Entity accuracy
delta with vs without the injected glossary is directly computable, and the program has already
built the harness for it - `derived/entity-inventory/v1/` (per-call), `derived/speech-lexicon/v1,v2`
(478 MB of word indexes over earnings21/22), and `derived/entity-wer/` (23 per-arm result files
from prior SAEA runs).

Earnings22 extends this to 118.89 h for scale and accent stress, but only with speaker indices and
without ConEC glossaries, so it is a generalization arm, not a primary mechanism arm.

Two honest limits: an earnings call is a *structured broadcast* (prepared remarks then moderated
Q&A), not a free-form meeting, so speaker decomposition there is easier than in a real meeting;
and there is no minutes or QA gold on this family at all.

---

## 4. Already-built derived assets relevant to this direction

`$SPEECHRL_DATA_DIR/derived/` (not in Git):

- `speech-lexicon/v1`, `v2` - 478 MB, 50 files, including
  `word_index.earnings21-original.json` and `word_index.earnings22-original.json`.
- `entity-inventory/v1/` - 34 per-call JSON inventories (`4341191.json`, ...).
- `entity-wer/<arm>/` - 23 per-attempt entity-WER result files from prior SAEA arms
  (`SAEA-BENCH-b90base-ctxinstr`, `SAEA-E-003R-retlex`, ...).
- also present: `obs-slices`, `obs-slices-precut`, `audio-features`, `offline-asr-wer`,
  `retrieval-bench`, `reachability-partition`, `evidence-candidates`, `exemplar-pairs`,
  `flag-eval`, `carrier-manifests/2026-08-17`.

Nothing equivalent exists for AMI: there is no derived AMI asset of any kind on disk.

---

## 5. Every other lock entry, scanned for meeting-adjacent utility

61 dataset directories exist under `datasets/`. One line each for the meeting-relevant question.

**Useful**

- `contextasr-bench` **Dialogue English** - 5,273 multi-speaker dialogues, 221.9 h, 3-5 distinct
  named roles per dialogue (122 distinct names corpus-wide), per-turn `role`/`start`/`end`/`text`,
  and a per-episode `entity_list` (mean 11.1 entities). Closest local analogue to the target task
  shape. **Two caveats: it is TTS-synthesized casual conversation (movie chat), not meeting speech;
  and its audio is NOT extracted** - it sits in 6 tars (~25.6 GB English, ~25.7 GB Mandarin) while
  only ContextASR-Speech English (15,326 wav) has been unpacked.
- `conec` - covered in section 3; the glossary/participant-metadata layer for Earnings21.
- `earnings21-22` - covered in section 3.
- `prism` (lock name `prism-public`, on-disk dir `prism`, 449 MB) - PRISM entity-rich sets
  (Location small/large, City, Drugs) with entity inventories plus synthetic carrier sentences.
  Useful as **entity/distractor list material** for glossary stress tests; single-speaker synthetic
  sentences, so not meeting data.
- `rare5k` (lock name `rare5k-reconstruction`, 988 KB) - derived LibriSpeech frequency split
  (`common-top5000.tsv`, `rare-after-top5000.tsv`). Useful only as a rare-word frequency prior for
  glossary construction.
- `slue-sqa-5` (110 GB) - spoken QA with `answer_spans`, `word2time`, `document_audio`,
  `document_speaker_id`. Real spoken-QA gold, but over **single-speaker documents**, not meetings.
  It is the closest local template for how a meeting-QA set would have to be shaped - not a
  substitute for one.
- `halas` (6.9 MB) - Earnings22-derived hallucination labels with `corrected_reference_text` and
  per-model hallucination spans for 3 Whisper variants. Useful as an OBS-failure diagnostic on the
  earnings family; not meeting data.

**Marginal**

- `ihbench` (207 MB, 45 conversations) - synthetic two-party agent-vs-caller phone calls with
  interruption types, per-turn rubrics, `knowledge_base` and `domain`. Two-party service calls, not
  meetings; the per-turn rubric design is worth reading as evaluation-protocol prior art.
- `mmsu` - contains 106 `long_speech_summarization_*` clips, but as multiple-choice items, not
  generative summary gold.
- `slideasr-bench` (11 GB, 8,467 wav + 8,467 jpg) - slide images as visual context for ASR;
  the "external document as context" pattern matches, the task does not.
- `ted-el` (77 MB) - TED entity-linking annotations plus a KB, shipped as two `.rar` archives.
  Blocked twice over: its audio source `ted-lium3` is **absent** on disk (lock lifecycle
  `SOURCE_UNSTABLE`), and the lock already records "complete use is blocked by the TED-LIUM3 audio
  source and incomplete method release". Single-speaker talks anyway.
- `full-duplex-bench-v3`, `soulx-duplug` - turn-taking / full-duplex; two-party interaction
  dynamics only, no minutes or entity layer.
- `audio2tool` (9.9 GB), `omni-deepsearch`, `voiceagentbench`, `tau2-bench`, `eva-bench` -
  agentic/tool-use; relevant to the control plane, not to meeting content.
- `voicebench`, `audiomc`, `uro-bench`, `vocalbench`, `heysquad`, `spoken-squad` - spoken QA /
  assistant dialogue on single-speaker or two-party audio; no meeting structure.

**Not useful for this direction**

- `atco2-test-1h` (127 MB, still as `.tgz`/`.tar.gz`) - air-traffic control, multi-party radio with
  callsign entities, but 1 h, unextracted, lock lifecycle `DEFERRED`, and the domain is
  transactional radio traffic, not meetings.
- `eka-medical-asr-eval` (269 MB, en/hi parquet) - single-speaker medical ASR; `DEFERRED`;
  no speaker or summary layer.
- `librispeech`, `aishell-1`, `thchs-30`, `fleurs-r`, `covost2`, `spoken-squad` - read speech / ST.
- `slurp`, `speech-massive`, `minds14` - single-turn SLU intent+slot.
- `meld`, `crema-d`, `esd`, `csemotions`, `iemocap`-like - emotion; MELD is multi-party TV dialogue
  with speaker labels but no minutes, no entities, and it is an emotion carrier.
- `cn-celeb1/2`, `voxceleb1-test-split` - speaker recognition.
- `air-bench`, `mmau-mini`, `mmar`, `big-bench-audio`, `auditorybench-plusplus`, `audiocaps-qa` -
  general/environmental audio understanding; several are out of this program's research boundary.
- `esc-50`, `fsd50k`, `audioset` - environmental audio, **prohibited by the study boundary**.
- `aime24/25/26`, `squad-v1.1-dev`, `seed-tts-eval`, `squtr`, `buzzword`, `librisqa-metadata` -
  text reasoning, TTS eval, or non-meeting speech.
- Absent on disk entirely (registered but not fetched): `ted-lium3`, `voxpopuli`, `spgispeech`,
  `mlc-slm`, `m3ed`, `msp-podcast`, `common-voice-22`, `indicvoices`, `speakersleuth`,
  `parapair-audio-bench`, `private-production-750h`, `prism-enterprise-medical`,
  `grga-longaudioqa`.

---

## 6. Gap analysis against the three evaluation surfaces

### (a) Glossary-loop mechanism - entity accuracy delta: **COVERED**

Primary: **Earnings21 + ConEC-e21**. 44 calls / 39.26 h, mean 10.6 speakers, gold RTTM turns,
88% name-resolved speakers, gold per-call glossary of mean 790 terms with an oracle/distractor
split, corrected entity-bearing references, and an existing derived harness
(`entity-inventory`, `speech-lexicon`, `entity-wer`).
Secondary: **ContextASR-Dialogue English** (5,273 episodes, per-episode `entity_list`,
speaker-attributed turns) - but requires extracting ~25.6 GB from 6 tars, and is TTS, not real
meeting speech.
Scale arm: Earnings22 (118.89 h) without glossaries.

Residual gap, minor: no *real, non-synthetic, multi-party meeting* corpus with proper-noun glossary
gold. AMI cannot fill it (its NE layer is scenario objects, section 2.5). Everything real is
earnings calls.

### (b) Minutes quality - needs summary gold: **PARTIALLY COVERED, single corpus**

Covered by AMI alone: 142 meetings / 75.1 h with four-section abstractive gold, 109 / 54.9 h with
the full annotation stack, plus extractive gold with sentence-level provenance links.

Precise gaps:

1. **Single corpus, single domain, single scenario.** 138 of 171 AMI meetings are the same scripted
   remote-control design scenario, recorded 2004-2005, with the same four roles (PM/ID/ME/UI). Any
   minutes-quality result on AMI alone is one domain deep. **No second English meeting corpus with
   summary gold exists on disk** - ICSI, MeetingBank, ELITR minuting, AutoMin: all absent.
2. **No query-focused or aspect-based summarization gold.** AMI's summaries are whole-meeting.
   There is nothing local that asks for a summary *of a specific query, speaker or topic*, which is
   what a per-speaker-content requirement implies.
3. **Reference multiplicity unverified.** Whether AMI ships more than one abstractive reference per
   meeting was not established in this audit (annotator IDs appear in the `nite:id` strings, e.g.
   `ES2002a.rdhillon.abstract.1`, but a clean per-meeting annotator count was not extracted). Without
   multiple references there is no human-agreement ceiling for reference-based metrics. **Flagged as
   unverified, not as absent.**
4. **Domain distance from the mechanism arm.** Minutes evidence would come from 2005 British/EU
   design meetings while glossary evidence comes from US earnings calls. No local corpus carries
   both surfaces, so a joint claim would be cross-corpus by construction.

### (c) Meeting QA: **NOT COVERED - total gap**

There is **no meeting-QA gold anywhere on disk.** Confirmed by exhaustive scan: AMI 1.6.2 ships no
QA layer; no dataset directory name matches summary/minutes/QMSum/ICSI patterns; the only
`*summ*` hits corpus-wide are `mmsu` MCQ audio filenames and unrelated `air-bench` sound clips.

The nearest local assets are all the wrong shape: `slue-sqa-5` is spoken QA over **single-speaker**
documents; `heysquad` and `spoken-squad` are read-speech QA over written passages; `voicebench`
`sd-qa` and `audiomc` are assistant-dialogue QA. None involves a multi-party meeting.

### (d) Cross-cutting gaps

- **Coreference / relations gold: absent.** The direction names coreference explicitly. AMI 1.6.2
  has no coreference layer (section 2.3); `youUsages` covers second-person pronouns on 16 meetings
  only. Nothing else local carries coreference over speech.
- **Per-speaker audio channels: absent.** AMI IHM/lapel/array were excluded at acquisition. Only
  Earnings has no channel separation either. So every speaker-decomposition experiment is
  mixdown-only unless AMI IHM is re-fetched.
- **Meeting-domain diversity: absent.** Local real multi-party English speech is exactly two
  domains - AMI scenario design meetings and earnings calls.

---

## 7. Acquisition targets this audit implies (for the parallel web-survey agent)

Ordered by how much of the gap each closes. Nothing here is a recommendation to fetch; it is the
target list the gaps point at.

1. **Meeting QA + query-focused summarization gold** - closes gap (c) entirely and gap (b.2)
   simultaneously, and is the single highest-leverage acquisition. The canonical candidate is a
   query-focused meeting summarization set built over AMI/ICSI-style meetings, which would reuse
   AMI audio already on disk. Survey should confirm licence, whether queries are gold, and whether
   the underlying meeting IDs intersect the 171 AMI meetings held locally.
2. **A second English meeting corpus with summary gold** - closes gap (b.1). Candidates to survey:
   ICSI (with its own dialogue-act and summary layers), MeetingBank (city-council meetings with
   summaries), ELITR/AutoMin (real minutes, closest to a true minutes task). Priority to any corpus
   whose domain is *not* scripted design meetings.
3. **AMI individual-headset (IHM) audio** - closes gap (d.2) with no new licensing question, since
   AMI is already CC-BY-4.0 and locally held; it is a re-fetch of a deliberately excluded variant
   from the same official mirror, and it would turn speaker decomposition from a mixdown problem
   into a channel-separation problem with gold.
4. **Coreference-annotated multi-party speech** - closes gap (d.1). Survey whether an AMI
   coreference layer is distributed separately from `ami_public_manual_1.6.2`, since that would be
   the cheapest possible close.
5. **Real multi-party meetings with proper-noun / jargon glossaries** - closes the residual in (a):
   an enterprise/technical meeting corpus with terminology lists, so the glossary loop is not
   evidenced only on earnings calls and synthetic TTS chat.

Also worth flagging to the survey agent as *local work rather than acquisition*: extracting the
ContextASR-Dialogue English tars (~25.6 GB, already paid for) would add 5,273 speaker-attributed,
entity-listed episodes to surface (a) at zero acquisition cost, and extracting the two AMI
annotation zips (~90 MB) is a precondition for any AMI work at all.

---

## Method and reproducibility

All disk facts were read in WSL2 `Ubuntu-24.04` (the tree carries WSL-only symlinks). Annotation
zips were read in place with `zipfile` without extracting. AMI durations come from WAV headers
(`wave.getnframes()/getframerate()`), not decoding. Entity counts come from regex over the NXT XML
resolved against `ontologies/ne-types.xml`. Parquet schemas were read with `pyarrow` from
`~/.venvs/speechrl`. No dataset bytes were modified, moved, or extracted; no model was contacted.
