# Spoken QA — candidate notes (2026-08-17)

Scope note carried into every verdict below: human speech and its linguistic content only.
General/environmental audio and music are out of boundary. Where a candidate mixes speech with
non-speech audio, the section says so explicitly and the verdict is scoped to the speech subset.

Every factual claim traces to a numbered row in `fetchlog-spoken-qa.md`.

---

## Spoken-SQuAD (original release)

- **Name**: Spoken-SQuAD — "Spoken SQuAD: A Study of Mitigating the Impact of Speech Recognition
  Errors on Listening Comprehension"
- **arXiv ID**: 1804.00320
- **Official page**: https://github.com/Chia-Hsuan-Lee/Spoken-SQuAD
- **HF/GitHub id**: `Chia-Hsuan-Lee/Spoken-SQuAD` (GitHub, canonical)
- **already-local / not-local**: **already-local via mirror only** — the program holds
  `spoken-squad` = `AudioLLMs/spoken_squad_test` (3.4 GB, test split only). The original
  train split (37,111 pairs) and the Noise V1/V2 test variants are **not local**.
- **Task shape and I/O**: In: spoken *document* (TTS audio of a SQuAD Wikipedia paragraph) +
  *text* question. Out: an answer that is always a contiguous span of the document. The released
  package also ships the CMU Sphinx ASR transcription of each document, so the practical text-side
  shape is (ASR transcript, text question) -> span.
- **Size**: 37,111 QA pairs train / 5,351 QA pairs test. Audio archive ~50 GB. #speakers: not
  stated (single Google TTS voice implied, not enumerated). Hours: not stated.
- **Language coverage**: English only.
- **Speech provenance**: **TTS/synthetic.** Google text-to-speech over SQuAD articles, then CMU
  Sphinx ASR. This is decisive — there is no real human speech anywhere in this corpus.
- **License**: verbatim from `LICENSE.md` — "This dataset is licensed under the terms of the
  CC-BY-SA-4.0 license, available below or at this canonical URL:
  https://creativecommons.org/licenses/by-sa/4.0/."
- **Obtainability**: direct download (plain HTTP zip from
  `speech.ee.ntu.edu.tw/~chiahsuan/Spoken-SQuAD/Spoken-SQuAD_audio.zip`); the mirror is ungated HF.
  Zero cost.
- **Rough download size**: ~50 GB for the full audio archive; 3.4 GB for the test split we already
  hold via the mirror.
- **Eval metric as published**: EM and F1 (SQuAD span metrics), reported alongside WER. Published
  WER: 22.77% train / 22.73% test on clean audio; 44.22% on Test Noise V1; 54.82% on Test Noise V2.
- **Published baselines for omni-style/frozen-LLM models**: none in the original paper (2018,
  BiDAF-era). See the AEG section below for 2026 Qwen3-Omni numbers on a *re-synthesized* spoken
  SQuAD, which is not byte-identical to this release.
- **Knowledge-coupling potential**: **MEDIUM, with a leakage hazard.** The per-item `context` field
  is the gold passage that literally contains the answer span. Injecting evidence into that slot is
  trivially answer-revealing, so the honest coupling experiment is *retrieval over a document pool*
  where the gold passage must be found, or *entity-roster injection* against the ASR-corrupted
  transcript (the 22.7% WER means named entities are frequently mangled — that is the real,
  non-leaking coupling slot). Flagged: shipping the gold passage makes naive "inject the context"
  a leakage artefact, not a capability gain.
- **G1' admission verdict**: **CONDITIONAL.** Passes (1) in-boundary, (2) zero cost, (3)
  adapter-mappable, (4) pinnable metric (EM/F1 deterministic). Fails cleanly on nothing, but is
  weak on (5): the coupling slot is confounded by gold-passage leakage, and the corpus is fully
  synthetic speech, which caps external validity for a study whose claim is about *speech
  observation*. Admit only as a leakage-controlled contrast arm, never as the headline set.

### Sub-note: the deleted-question issue and `squad-v11-dev`

The original construction states verbatim: "If the answer of a question did not exist in the ASR
transcriptions of the associated article, we removed the question-answer pair from the dataset."
This is a **survivorship filter keyed on ASR success**: the released test set is biased toward
questions the 2018 CMU Sphinx system happened to transcribe correctly. Any measurement on
Spoken-SQuAD alone therefore *understates* the difficulty of the entity-recovery problem this
program cares about. The locally held `squad-v11-dev` text reference is the correct instrument for
reconstructing the deleted questions and quantifying that bias; doing so is a prerequisite to using
Spoken-SQuAD as evidence for anything.

---

## Spoken-SQuAD (AudioLLMs mirror)

- **Name**: `AudioLLMs/spoken_squad_test`
- **arXiv ID**: derives from 1804.00320; distributed under the AudioBench harness (NAACL 2025,
  `aclanthology.org/2025.naacl-long.218`)
- **Official page**: https://huggingface.co/datasets/AudioLLMs/spoken_squad_test
- **already-local / not-local**: **already-local** (3.4 GB, 5,351 rows).
- **Task shape and I/O**: In: audio (11.6–305 s) + `instruction` text. Out: free-text `answer`.
  Columns: `context`, audio, `instruction`, `answer`. Note the reshaping — AudioBench turns the
  span task into an open-ended generation task.
- **Size**: 5,351 rows, test split only. Audio duration range 11.6–305 s; total hours not stated.
- **Language coverage**: English only.
- **Speech provenance**: **TTS/synthetic** (inherited from the 2018 release).
- **License**: `CC-BY-SA-4.0`.
- **Obtainability**: ungated HF, zero cost.
- **Rough download size**: 3.4 GB (already held).
- **Eval metric as published**: AudioBench scores this set with `llama3_70b_judge` and
  `gpt4o_judge` — **model-as-judge, not EM/F1**.
- **Published baselines**: AudioBench maintains a live leaderboard; no Qwen-Omni numbers for this
  set were retrievable from the README (not retrieved). A reported WavLLM figure of 83.92 exists
  for the sibling SLUE-P2-SQA5 set, not for this one.
- **Knowledge-coupling potential**: **MEDIUM** — same `context` gold-passage slot and the same
  leakage caveat as the original.
- **G1' admission verdict**: **CONDITIONAL.** The blocker is criterion (4): the published metric is
  a judge model. `gpt4o_judge` is paid and therefore excluded outright; `llama3_70b_judge` is
  self-hostable but is a 70B second LLM in the loop, which collides with the study's "no second
  answering LLM" boundary unless it is pinned strictly as a *scoring* tool with logged weights.
  Recommendation: keep the audio, discard the AudioBench metric, and re-derive EM/F1 against the
  original span answers.

---

## HeySQuAD (human + machine)

- **Name**: HeySQuAD — A Spoken Question Answering Dataset
- **arXiv ID**: 2304.13689
- **Official page**: https://arxiv.org/abs/2304.13689
- **HF id**: `yijingwu/HeySQuAD_human` (human split, held locally); a machine/TTS split also exists
- **already-local / not-local**: **already-local** for the human split (14.6 GB). The 97k
  machine-generated split is **not local**.
- **Task shape and I/O**: In: spoken **question** audio + text `context` passage. Out: text answer
  span. Note the inversion relative to Spoken-SQuAD — here the *question* is spoken and the
  *document is text*.
- **Size**: 76,000 human-spoken questions (local card: 72,000 train + 4,160 validation =
  76,148 rows) and 97,000 machine-generated questions. Audio clips 1.37–26.4 s. Hours: not stated.
  #speakers: not stated.
- **Language coverage**: English only.
- **Speech provenance**: **Real human speech** for the 76k human split (recorded readers);
  **TTS** for the 97k machine split. The human split is the valuable half for this program.
- **License**: `CC-BY-4.0` (HF card); the paper is likewise CC BY 4.0.
- **Obtainability**: ungated HF, zero cost.
- **Rough download size**: 14.6 GB (human split, already held).
- **Eval metric as published**: EM and F1 (SQuAD span metrics). The paper's headline claim is a
  12.51% improvement from training on transcribed human-spoken plus original SQuAD questions —
  a *training* result, therefore not directly comparable to a frozen-core setting.
- **Published baselines for omni-style/frozen-LLM models**: none retrieved.
- **Knowledge-coupling potential**: **HIGH.** Unlike Spoken-SQuAD, the noise here lives in the
  *question*, and the `context` passage is a legitimate, separately-supplied evidence field. A
  mis-heard entity in the spoken question (e.g. a proper noun) is exactly the failure an injected
  entity roster or KB entry repairs, and the passage stays a fair, non-leaking retrieval target
  because the question audio is what is degraded. The concrete carrier field is the question-side
  entity roster, with `context` as the ORG/SUPPLY slot.
- **G1' admission verdict**: **ADMIT.** (1) in-boundary — human speech, linguistic content;
  (2) zero cost, ungated; (3) clean adapter shape for a turn-based omni core (one audio question +
  one text passage per turn); (4) EM/F1 are deterministic and pinnable; (5) genuine coupling with
  the leakage hazard structurally avoided. Already local, so no acquisition needed. Strongest
  member of this family on the coupling axis.

---

## SLUE-SQA-5

- **Name**: SLUE-SQA-5 (SLUE Phase-2 spoken QA task)
- **arXiv ID**: 2212.10525
- **Official page**: https://huggingface.co/datasets/asapp/slue-phase-2 (`sqa5` config)
- **already-local / not-local**: **already-local** — all splits including train (118 GB).
- **Task shape and I/O**: In: **spoken question audio + spoken document audio**. Out: the
  *temporal span* in the document audio containing the answer. This is the only candidate in the
  family where both sides are real speech and the answer is a time interval rather than text.
  Columns include `document_audio`, question audio, and `raw_document_text`.
- **Size**: train 46,186 / validation 1,939 / test 2,382 / verified_test 408. The HF viewer reports
  50.9k rows for the config. Hours: not retrieved. #speakers: not stated (Spoken Wikipedia readers
  plus crowdsourced question speakers).
- **Language coverage**: English only.
- **Speech provenance**: **Real human speech on both sides.** Documents come from the Spoken
  Wikipedia corpus (volunteer human readers); question audio was obtained by crowdsourcing human
  speakers. Question *text* is sourced from five text-QA datasets: SQuAD v1.1, Natural Questions,
  TriviaQA, WebQuestions, CuratedTREC.
- **License**: mixed, per the dataset card — "Apache License 2.0 as TriviaQA" for TriviaQA-derived
  questions; "Creative Commons Attribution-ShareAlike 4.0 International license" for SQuAD, NQ,
  WebQuestions and CuratedTREC; "Creative Commons (CC BY-SA 4.0)" for the Spoken Wikipedia content.
  All permissive; no paid or gated component.
- **Obtainability**: ungated HF, zero cost.
- **Rough download size**: 118 GB (already held).
- **Eval metric as published**: **frame-F1 (FF1)** — a frame-level adaptation of token F1, where
  predicted and ground-truth answer spans are converted to time intervals and precision/recall are
  computed over frames. Deterministic; no judge model.
- **Published baselines for omni-style/frozen-LLM models**: AudioBench reports the set as
  `slue_p2_sqa5_test` with a WavLLM score of 83.92 (under a model-as-judge reformulation, not
  frame-F1). No Qwen-Omni number retrieved.
- **Knowledge-coupling potential**: **HIGH.** `raw_document_text` is a real, separately addressable
  evidence field, and the question text originates from open-domain QA sets (TriviaQA,
  NQ, WebQuestions) whose answers are entity-heavy and *not* guaranteed to be recoverable from the
  audio alone. The concrete carrier: an entity roster or retrieved KB entry supplied alongside
  `raw_document_text` to disambiguate proper nouns in the spoken document. Leakage is bounded
  because the native metric scores a *time span in audio*, so supplying text evidence does not
  hand over the answer's location.
- **G1' admission verdict**: **ADMIT.** All five criteria pass. This is the family's reference set:
  real speech on both sides, a deterministic non-judge metric, a genuine document field, and it is
  already local with train data available for discovery-side work. The one caution is that
  frame-F1 presumes a localization output, which a turn-based text-emitting omni core does not
  natively produce — the adapter must either map text answers back to time intervals via forced
  alignment or the study must declare a text-side EM/F1 variant and pin it explicitly.

---

## LibriSQA

- **Name**: LibriSQA — A Novel Dataset and Framework for Spoken Question Answering with Large
  Language Models
- **arXiv ID**: 2308.10390
- **Official page**: https://github.com/ZihanZhaoSJTU/LibriSQA;
  https://huggingface.co/datasets/ZihanZhao/LibriSQA
- **already-local / not-local**: **already-local as metadata only** (171 MB); audio resolves against
  the locally held `librispeech`.
- **Task shape and I/O**: Two parts. Part I (free-form): In: speech segment + text question. Out:
  open-ended text answer. Part II (multiple choice): In: speech segment + question with four
  options. Out: option label plus an "analysis" rationale. Columns: `speech_path`, `question`,
  `answer`, `text`, `duration` (+ `answer_and_analysis` in Part II).
- **Size**: 107k QA pairs in Part I and 107k in Part II (214k total). Hours: derived from
  LibriSpeech `train-clean-360`, so ~360 h of source audio; exact QA-covered hours not retrieved.
  #speakers: inherited from LibriSpeech `train-clean-360` (not restated by the authors).
- **Language coverage**: English only.
- **Speech provenance**: **Real human speech** — LibriSpeech `train-clean-360` audiobook readers.
  The authors state explicitly that recordings are from authentic human narrators rather than
  synthesized TTS. However, the **QA pairs themselves are ChatGPT-generated** from the transcripts,
  with human verification claimed.
- **License**: `CC BY 4.0` (per the paper).
- **Obtainability**: ungated HF + GitHub, zero cost.
- **Rough download size**: 171 MB metadata (already held) + LibriSpeech audio (already held).
- **Eval metric as published**: ASR sub-task WER; Part I scored with BLEU, ROUGE and BERT
  similarity; Part II with macro accuracy, F1, BLEU, ROUGE and BERT similarity.
- **Published baselines for omni-style/frozen-LLM models**: none retrieved.
- **Knowledge-coupling potential**: **LOW.** There is no document/passage field — the "document" is
  the audiobook segment itself, and the LLM-generated questions were explicitly constructed to be
  answerable *without external knowledge*. That prompt constraint is precisely what removes the
  slot this study needs. Part II's `analysis` field is a rationale, not evidence.
- **G1' admission verdict**: **REJECT** on criterion (5), non-trivial knowledge-coupling. It also
  strains criterion (4): Part I's published metrics are BLEU/ROUGE/BERTScore over free-form text,
  which are weak and noisy for a capability claim. Passes (1), (2), (3). Keep as a spoken-instruction
  smoke set only; it cannot carry an evidence-acquisition result.

---

## SD-QA

- **Name**: SD-QA — Spoken Dialectal Question Answering for the Real World
- **arXiv ID**: 2109.12072 · **Anthology ID**: 2021.findings-emnlp.281
- **Official page**: https://aclanthology.org/2021.findings-emnlp.281/;
  https://github.com/ffaisal93/SD-QA
- **already-local / not-local**: **not-local**
- **Task shape and I/O**: In: spoken **question** audio (a dialect speaker reading a TyDi QA
  question aloud) + the TyDi QA passage/context. Out: text answer span. Built by augmenting TyDi QA
  along a speech dimension and a dialect dimension.
- **Size**: >68,000 audio prompts, 24 dialects, 255 speakers, 5 languages. English slice: the same
  ~1,000 questions recorded across English accent regions. **Discrepancy recorded**: one source
  states "1k questions in the dev set and 1k in the test set are recorded in 11 English dialects";
  another states "the same 1000 questions spoken and recorded by speakers in 10 accent regions."
  The dialect count (10 vs 11) and whether the 1k applies per split are unresolved from the sources
  fetched; the paper appendix was not machine-readable through WebFetch. Total hours: not retrieved.
- **Language coverage**: Arabic, Bengali, **English**, Kiswahili, Korean. English is one of five,
  and the English slice is small in absolute terms (~1k questions × ~10–11 dialects), so English is
  a *minority slice by question count but a full dialect matrix*.
- **Speech provenance**: **Real human speech** — native dialect speakers reading questions aloud.
  This is the corpus's whole point and its main value.
- **License**: `Apache License 2.0` (GitHub repository).
- **Obtainability**: **direct download, but friction-heavy** — the repository distributes data via
  Google Drive folders rather than a package registry or HF. Zero cost, no gate, no request form.
  No official HF mirror was found.
- **Rough download size**: not retrieved. The English-only slice would be a small fraction of the
  68k prompts; order-of-magnitude single-digit GB, but this is an estimate, not a retrieved figure.
- **Eval metric as published**: F1/EM in the TyDi QA gold-passage convention, with WER reported on
  the ASR outputs. The repository ships a `tydiqa_evaluation.ipynb` and references "WER based
  evaluation on ASR outputs."
- **Published baselines for omni-style/frozen-LLM models**: none — this is a 2021 paper predating
  audio LLMs. Baselines are cascaded ASR + extractive QA.
- **Knowledge-coupling potential**: **HIGH.** Inherits TyDi QA's gold passage as a real evidence
  field, and — critically — the *dialect* dimension creates systematic, speaker-attributable ASR
  entity errors. That is the cleanest available setting for testing whether an injected entity
  roster repairs speech-observation failures, because the failure rate varies by dialect while the
  question text is held constant across all speakers. The constant-question, varying-speaker design
  is a natural controlled experiment for the OBS component specifically.
- **G1' admission verdict**: **ADMIT (English subset only)**, with one caveat. (1) in-boundary;
  (2) zero cost; (3) adapter-mappable; (4) F1/EM pinnable; (5) high coupling with a built-in
  controlled contrast. Caveat: Google Drive distribution is fragile for a lock-registration flow
  that pins hashes — verify file-level stability at acquisition time and mirror the exact bytes.
  Scope the verdict to the English dialect subset; the Arabic/Bengali/Kiswahili/Korean slices are
  out of the program's English-only working language even though they are in-boundary as speech.

---

## NMSQA

- **Name**: NMSQA (Natural Multi-speaker Spoken QA), released with DUAL / textless spoken QA
- **arXiv ID**: 2203.04911
- **Official page**: https://huggingface.co/datasets/voidful/NMSQA
- **already-local / not-local**: **not-local**
- **Task shape and I/O**: In: spoken question + spoken context passage. Out: answer span with
  timing metadata, given in both text and audio domains. Columns include context passages (text +
  audio segments), question (text + audio), answers with timing, audio paths, speaker identifiers,
  and normalized text.
- **Size**: train 87.6k / dev 10.6k / test 171 rows (98.3k total). Hours: not retrieved.
  #speakers: multiple named TTS voices (Justin, Joey, Emma, Kendra, Amy, ...); the "multi-speaker"
  in the name refers to TTS voice diversity, not human speakers.
- **Language coverage**: English only.
- **Speech provenance**: **TTS/synthetic** — 22,050 Hz audio across multiple Amazon Polly-style
  voices. Note the naming trap: "Natural Multi-speaker" does not mean human speech.
- **License**: **not stated** on the HF card.
- **Obtainability**: ungated HF, zero cost.
- **Rough download size**: not retrieved (not stated on the card).
- **Eval metric as published**: frame-level F1 / AOS in the textless-QA convention; the card
  exposes answer span positions in both text and audio domains. Exact metric name not retrieved
  from an official source in this pass.
- **Published baselines for omni-style/frozen-LLM models**: none retrieved. NMSQA is the standard
  evaluation set for SpeechDPR (arXiv 2401.13463, end-to-end spoken passage retrieval), which makes
  it the field's default *spoken retrieval* testbed.
- **Knowledge-coupling potential**: **MEDIUM-HIGH.** It ships a per-question spoken context passage
  *and* is already established as a spoken-passage-retrieval benchmark, so the SUPPLY component has
  a ready-made, literature-comparable slot. Downgraded from HIGH because the test split is only 171
  rows — far too small to carry a claim on its own — and the speech is synthetic.
- **G1' admission verdict**: **CONDITIONAL.** Fails nothing outright but is weak on two counts:
  the **license is not stated**, which blocks the program's lock-registration flow until clarified,
  and the 171-row test split forces evaluation onto the dev split (10.6k), which is a protocol
  decision that must be pre-registered rather than chosen after seeing results. Synthetic speech
  further caps external validity. Admit only if the licence is resolved and the split choice is
  fixed in advance.

---

## ODSQA

- **Name**: ODSQA — Open-Domain Spoken Question Answering Dataset
- **arXiv ID**: 1808.02280
- **Official page**: https://github.com/Chia-Hsuan-Lee/ODSQA
- **already-local / not-local**: **not-local**
- **Task shape and I/O**: In: spoken document + spoken question (a text-question variant is also
  shipped). Out: text answer that is a span in the document. Reference texts come from DRCD, a
  traditional Chinese machine reading comprehension dataset.
- **Size**: 3,654 questions in the test set, of which 1,465 have corresponding audio. 20 speakers
  (7 male, 13 female for the audio portion). Hours: not stated.
- **Language coverage**: **Traditional Chinese only. No English.**
- **Speech provenance**: **Real human speech** — 20 recruited speakers read the DRCD dev-set
  questions and paragraphs aloud. Described by its authors as the largest *real* SQA dataset of its
  time.
- **License**: **not stated** in the repository. The arXiv paper itself is CC BY 4.0, which does
  not automatically extend to the data.
- **Obtainability**: direct download (plain HTTP zip from
  `speech.ee.ntu.edu.tw/~chiahsuan/ODSQA/audio_data.zip`); zero cost. File size not stated.
- **Rough download size**: not retrieved.
- **Eval metric as published**: EM/F1 span metrics in the DRCD convention. Exact metric names not
  retrieved from the official PDF in this pass.
- **Published baselines for omni-style/frozen-LLM models**: none — 2018 paper, subword-unit and
  data-augmentation baselines only.
- **Knowledge-coupling potential**: **MEDIUM** in principle (spoken document field present, real
  ASR errors on entities), but moot for this program.
- **G1' admission verdict**: **REJECT** on the program's English-only working-language requirement.
  It is *in scope* as human speech and would be scientifically interesting (real speech, both sides
  spoken, genuine ASR-error coupling), but no English slice exists, and the licence is unstated —
  a second, independent blocker for lock registration. Recorded here for completeness and as a
  possible future cross-lingual replication target if the program's language constraint ever moves.

---

## SpokenNativQA

- **Name**: SpokenNativQA — Multilingual Everyday Spoken Queries for LLMs
- **arXiv ID**: 2505.19163 · **Venue**: Interspeech 2025
- **Official page**: https://huggingface.co/datasets/QCRI/SpokenNativQA
- **already-local / not-local**: **not-local**
- **Task shape and I/O**: In: spoken question audio (an everyday, culturally-situated query). Out:
  free-text answer. Columns: `lang`, `data_id`, `file_name`, `file_path`, `question`, `answer`,
  `location`, `asr_text`. Each question ships transcriptions from **multiple ASR systems** (Azure,
  Google, Fanar-Aura, Whisper), which is an unusual and useful feature.
- **Size**: ~33,081 spoken questions, ~30 hours of audio in the paper's description; the HF card's
  released test split shows 13,234 rows total — English subsets 2,320 rows each across three ASR
  variants, Arabic subsets 988 rows each (985 for Whisper). **Discrepancy recorded**: the paper's
  33k/30h figure and the card's 13,234 released rows do not reconcile from the sources fetched;
  the released artefact is the smaller one. #speakers: not stated.
- **Language coverage**: Arabic and English. English is roughly 2,320 questions per ASR variant —
  a genuine but modest English slice, and English is *not* a minority here (it is the larger of the
  two languages by row count).
- **Speech provenance**: **Real human speech** — naturally spoken user queries, not TTS.
- **License**: `CC BY-NC-SA 4.0` (Creative Commons Attribution-NonCommercial-ShareAlike).
- **Obtainability**: ungated HF, zero cost. Note the **NonCommercial** clause — acceptable for
  research use but must be recorded in the lock file.
- **Rough download size**: 364 MB total. Very cheap.
- **Eval metric as published**: not specified on the dataset card; the paper benchmarks via the
  LLMeBench framework (`llmebench.qcri.org`). Metric not retrieved.
- **Published baselines for omni-style/frozen-LLM models**: not retrieved.
- **Knowledge-coupling potential**: **HIGH — and it is the purest case in this family.** There is
  **no passage/context field at all**, which means there is *zero* leakage hazard: the questions are
  open-domain, culturally- and region-specific everyday queries whose answers are simply not
  recoverable from the audio. The concrete carrier is a retrieved KB entry or web snippet supplied
  as the SUPPLY slot; the `location` field additionally lets evidence be conditioned on region.
  This is a closed-book set that *demands* external evidence, which is exactly the shape the study
  wants. The multi-ASR `asr_text` columns are a bonus: they give a free, pre-computed OBS-quality
  axis without running any ASR.
- **G1' admission verdict**: **ADMIT (English subset).** (1) in-boundary — human speech, linguistic
  content; (2) zero cost, ungated, 364 MB; (3) trivially adapter-mappable — one audio question per
  turn; (5) highest clean coupling in the family. The soft spot is (4): the published metric was not
  retrievable, and open-domain free-text answers usually invite a judge. The study must pin its own
  deterministic scorer (normalized EM / token-F1 against the `answer` field, or a fixed answer-set
  match) and pre-register it. Do that and this is a strong ADMIT. Recommend acquiring.

---

## VoxEval

- **Name**: VoxEval — Benchmarking the Knowledge Understanding Capabilities of End-to-End Spoken
  Language Models
- **arXiv ID**: 2501.04962 · **Anthology ID**: 2025.acl-long.818 (ACL 2025)
- **Official page**: https://github.com/dreamtheater123/VoxEval;
  https://huggingface.co/datasets/qqjz/VoxEval
- **already-local / not-local**: **not-local**
- **Task shape and I/O**: In: spoken multiple-choice knowledge question (audio). Out: spoken or
  text answer. Both question and answer are kept in speech format to allow end-to-end evaluation.
  Source text benchmark is **MMLU**.
- **Size**: HF card reports validation 858 rows / test 408,000 rows (408,764 total), 88.1 GB. The
  large test count reflects the full cross-product of MMLU items × 6 voices × speaking styles ×
  audio conditions. Number of *distinct* questions: not retrieved. Hours: not retrieved.
- **Language coverage**: English only.
- **Speech provenance**: **TTS/synthetic** — six OpenAI TTS voices (Alloy, Echo, Fable, Nova, Onyx,
  Shimmer), plus 3 speaking-style conditions (linguistic, speed, pitch) and 2 audio-quality
  conditions (noise, environmental acoustics).
- **License**: verbatim — "The dataset is licensed under the Creative Commons Attribution 4.0."
  (`cc-by-4.0` on the HF card.)
- **Obtainability**: ungated HF, zero cost.
- **Rough download size**: 88.1 GB for the full cross-product. A single-voice slice would be
  roughly 1/6 of that; the study would almost certainly consume a condition subset, not the whole.
- **Eval metric as published**: **accuracy**, computed by the repository's `metric_calculation.py`.
  Deterministic multiple-choice accuracy — no judge model. This is a real strength.
- **Published baselines for omni-style/frozen-LLM models**: yes, but for spoken LMs rather than
  omni cores — GLM-4-Voice, Moshi, SPIRIT-LM, TWIST, SpeechGPT, with per-voice accuracies (e.g.
  GLM-4-Voice 0.3763 on the Alloy condition) alongside the underlying models' text MMLU scores.
  The paper's headline finding is that current SLMs perform *poorly* and are sensitive to audio
  conditions. No Qwen-Omni number retrieved.
- **Knowledge-coupling potential**: **HIGH.** VoxEval is a *closed-book knowledge* test delivered
  over speech, with no passage field — so injected evidence has a clean, uncontaminated slot, and
  the paper's own result (large text-MMLU vs spoken-MMLU gap) is direct evidence that the knowledge
  is present in the text channel but lost through the speech channel. That gap is the exact
  quantity a knowledge-injection control plane would attack. The carrier field is a retrieved
  MMLU-topic KB entry supplied as text alongside the audio question.
- **G1' admission verdict**: **ADMIT (condition subset).** (1) in-boundary — synthetic but
  unambiguously human-language speech; (2) zero cost, ungated, CC BY 4.0; (3) multiple-choice maps
  perfectly onto a turn-based core; (4) plain accuracy, fully deterministic and pinnable —
  the best metric hygiene in this family; (5) high, leakage-free coupling. The two reservations are
  synthetic speech (caps OBS-side external validity) and the 88.1 GB full size, which mandates
  pre-registering a specific voice/condition subset rather than sampling opportunistically.
  Note the strong MMLU contamination risk that attends any MMLU derivative — the frozen core may
  have memorized items, so a *knowledge-injection* gain must be separated from recall.

---

## NSF-QA

- **Name**: NSF-QA — QA and summarization benchmark over NOTSOFAR-1 meeting audio, released with
  "Grounding Spoken LLMs in Multi-Speaker Audio via Diarization Conditioning"
- **arXiv ID**: 2606.18134 (June 2026)
- **Official page**: https://huggingface.co/datasets/popcornell/NSF-QA
- **already-local / not-local**: **not-local**
- **Task shape and I/O**: In: long-form, far-field, **multi-speaker meeting audio** with a target
  speaker, plus a question. Out: free-text answer. Question categories: Content QA (entity, topic,
  yes/no, detail), Paralinguistic/Emotion QA, and Summarization. Columns: `session_id`, `speaker`,
  `question`, `answer`, `category`, `type`, `ct_wav`.
- **Size**: train 29,700 / validation 6,710 / test 14,140 rows (50,574 total); ~1,100–1,500
  training examples per QA category. 305 GB. Hours: not retrieved (inherited from NOTSOFAR-1).
  #speakers: not stated.
- **Language coverage**: English only.
- **Speech provenance**: **Real human speech** — genuine recorded multi-speaker meetings from the
  NOTSOFAR-1 distant meeting transcription corpus (CHiME-8 Task 2). Far-field, overlapping,
  acoustically hard. The *questions and reference answers*, however, are **synthetic**: generated by
  Google Gemini 2.5 Flash from ground-truth transcripts.
- **License**: "Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)", with
  upstream CC BY 4.0 obligations from the NOTSOFAR-1 source data.
- **Obtainability**: ungated HF, zero cost. Generation scripts and judge prompts are open-sourced.
- **Rough download size**: **305 GB** for the full release — by far the heaviest candidate here.
  A test-split-only consumption would still be substantial; exact test-split bytes not retrieved.
- **Eval metric as published**: Summarization uses **ROUGE-L against five references per speaker**.
  Content QA scoring is judge-prompt-based (the release ships judge prompts), so the QA metric is
  **model-as-judge**, not deterministic. Exact QA metric name not retrieved.
- **Published baselines for omni-style/frozen-LLM models**: not retrieved; the paper's own baselines
  concern diarization-conditioned spoken LLMs.
- **Knowledge-coupling potential**: **HIGH.** It carries an explicit **entity** question type over
  real, acoustically degraded multi-speaker speech — entity recovery under far-field overlap is
  precisely the OBS failure mode an injected entity roster is meant to repair. Ground-truth
  transcripts exist as a separately addressable field. This is the most *realistic* coupling setting
  in the family and the closest in character to the program's existing earnings-call assets.
  Leakage caution: the reference answers were LLM-generated *from* the transcripts, so supplying the
  full transcript as evidence is near-total leakage; the legitimate injection is a roster or KB
  entry, never the transcript.
- **G1' admission verdict**: **CONDITIONAL.** Passes (1) in-boundary, (2) zero cost, (3)
  adapter-mappable, (5) high coupling. Two blockers: criterion (4) — the QA metric is judge-based,
  so the study must substitute a pinnable scorer (the entity-QA subtype is the most amenable, since
  entity answers admit normalized exact match); and the **305 GB** footprint plus CC BY-NC, which
  make this an acquisition decision rather than a casual add. Recommend acquiring **only the
  entity-category test slice** if the maintainers expose one. Genuinely the most interesting new
  release for this program.

---

## LongSpeech

- **Name**: LongSpeech — A Scalable Benchmark for Transcription, Translation and Understanding in
  Long Speech
- **arXiv ID**: 2601.13539 (submitted 2026-01-20) · **Venue**: ICASSP 2026
- **Official page**: https://arxiv.org/abs/2601.13539; HF org AIDC-AI
- **already-local / not-local**: **not-local**
- **Task shape and I/O**: In: ~10-minute speech segment + task instruction. Out: task-dependent
  text. Eight tasks: ASR, speech translation, summarization, language detection, speaker counting,
  content separation, question answering, and temporal issue localization.
- **Size**: >100,000 segments of ~10 minutes each ≈ **~16,667 hours**. The QA-adjacent Temporal
  Issue Localization task has 8,000 examples (5,800 train / 1,200 dev / 1,200 test). #speakers:
  not stated.
- **Language coverage**: English, French, German, Spanish, Japanese, Korean, Mandarin Chinese.
  English is present and prominent (LibriSpeech, TED-LIUM v3, SPGISpeech sources) but is one of
  seven.
- **Speech provenance**: **Mostly real human speech** — sourced from LibriSpeech, TED-LIUM v3,
  SPGISpeech, VoxPopuli, CommonVoice, AISHELL-2, and IWSLT — **plus a synthesized component**: a
  custom movie-dialogue corpus rendered with TTS for multi-speaker conversations. Mixed provenance;
  a study using it must scope to the real-speech sources.
- **License**: `BY-NC-ND 4.0` (Creative Commons Attribution-NonCommercial-**NoDerivatives**).
- **Obtainability**: **BLOCKED / unresolved.** The paper says the benchmark "will be made publicly
  available"; no HuggingFace id is given in the paper, and a direct fetch of
  `huggingface.co/datasets/AIDC-AI/LongSpeech` returned **HTTP 401 Unauthorized**, indicating the
  repository is gated or not yet public. Flag, do not auto-exclude.
- **Rough download size**: not retrieved; ~16,667 hours of audio implies a multi-terabyte footprint,
  which would collide with the owner's >1 TB exclusion already applied to VoxPopuli.
- **Eval metric as published**: task-dependent. Temporal Issue Localization uses **Strict Accuracy**
  (ratio of YES judgments) and **Relaxed Accuracy** (ratio of YES-or-PARTIALLY judgments), adjudicated
  by **GPT-4-Turbo** — a paid judge. Other task metrics not retrieved.
- **Published baselines for omni-style/frozen-LLM models**: not retrieved. Speech-XL (arXiv
  2602.05373) evaluates against LongSpeech and AudioMarathon but releases no data of its own.
- **Knowledge-coupling potential**: **MEDIUM.** Long-form speech with derived transcripts offers a
  plausible SUPPLY slot, but the QA construction is undocumented in the paper and the tasks lean
  toward transcription/localization rather than external-knowledge use. Cannot be rated higher
  without seeing the actual QA items.
- **G1' admission verdict**: **REJECT (for now), on three criteria.** (2) obtainability — HF returns
  401, no confirmed public location; (4) the localization metric is **GPT-4-Turbo-judged**, i.e.
  paid-judge-only, which is an automatic metric failure and brushes the zero-spend rule; and the
  **NoDerivatives** licence term is hostile to a pipeline that produces derived, hashable artefacts
  from the data, which is a core requirement of this program's tracing discipline. Multi-terabyte
  scale is a fourth practical blocker. Revisit only if an ungated, deriv-permissive release appears.

---

## ChronosAudio

- **Name**: ChronosAudio — A Comprehensive Long-Audio Benchmark for Evaluating Audio-Large Language
  Models
- **arXiv ID**: 2601.04876 (v1 2026-01-08; v2 2026-05-27)
- **Official page**: https://arxiv.org/abs/2601.04876; code/data behind an anonymous review link,
  `anonymous.4open.science/r/ChronosAudio-D49A`
- **already-local / not-local**: **not-local**
- **Task shape and I/O**: In: long synthesized speech + task prompt. Out: text. Six task categories:
  Dictation (last-word identification), Localization (temporal grounding), Transcription,
  Multi-Speaker (speaker-attributed transcription), Comprehension (QA over audio content), and
  Summary.
- **Size**: 36,000 test instances, >200 hours of audio, stratified into short/middle/long duration
  bands. #speakers: not stated (synthetic voices).
- **Language coverage**: English-centric; the paper concedes the limitation verbatim — "our
  benchmark is predominantly English-centric and from relatively clean acoustic environments."
- **Speech provenance**: **Fully TTS/synthetic** — all 200+ hours generated with the F5-TTS engine
  from SQuAD (Wikipedia) text. No real human speech anywhere. Clean acoustics by construction.
- **License**: `CC BY 4.0`.
- **Obtainability**: **BLOCKED / unresolved** — the only release pointer found is an anonymous
  review link; no permanent HF or GitHub location was retrievable. Flag as not-yet-obtainable
  rather than paid.
- **Rough download size**: not retrieved; >200 hours of TTS speech is order-of-magnitude tens of GB.
- **Eval metric as published**: per task — Dictation Accuracy, Localization Score (0.1 s tolerance),
  Transcription Score (mixed WER + BERTScore), Multi-Speaker Score (WER + speaker F1),
  **Comprehension Score (exact match minus a hallucination penalty)**, Summary Score (coverage
  recall + factuality precision). Scoring uses an **LLM-as-a-Judge framework** with ground-truth
  transcripts. The Comprehension Score's EM core is the most pinnable part.
- **Published baselines for omni-style/frozen-LLM models**: 16 state-of-the-art models evaluated;
  specific Qwen-Omni figures not retrieved.
- **Knowledge-coupling potential**: **LOW-MEDIUM.** It is SQuAD-derived, so the underlying passage
  is the gold answer container — the same leakage hazard as Spoken-SQuAD, compounded by the fact
  that the benchmark's stated purpose is long-context *attention persistence*, not knowledge use.
  Ground-truth transcripts exist but function as scoring references, not injectable evidence.
- **G1' admission verdict**: **REJECT.** Fails (2) obtainability — no permanent public release
  location found, only an anonymous review URL; and is weak on (4), since the headline scoring is
  LLM-as-a-Judge, and on (5), since the coupling slot is leakage-confounded SQuAD passage text.
  Fully synthetic clean speech also makes it a poor instrument for a speech-observation claim.
  Re-check after camera-ready, when a permanent release may appear.

---

## VoiceGiraffe

- **Name**: VoiceGiraffe — A Benchmark for Extreme Long-Context Audio-Language Understanding
- **arXiv ID**: 2605.27976 (submitted 2026-05-27)
- **Official page**: https://arxiv.org/abs/2605.27976; GitHub `LivingFutureLab/VoiceGiraffe`
- **already-local / not-local**: **not-local**
- **Task shape and I/O**: In: hour-scale audio + question. Out: text answer. Organized as a dual-level
  taxonomy of **single-hop perception** and **multi-hop reasoning** over 1,500 curated triplets.
- **Size**: 1,500 curated triplets. Targets the hour scale. Total hours: not stated. #speakers:
  not stated.
- **Language coverage**: "diverse scenarios and languages"; the specific language count is not
  stated and the size of the English slice is **not retrieved**.
- **Speech provenance**: **Real-world audio, not TTS** — described as podcasts and lengthy speeches,
  i.e. predominantly human speech. It is a *speech*-oriented long-context set rather than a general
  audio set, but the exact domain inventory was not retrievable, so residual non-speech content
  cannot be ruled out.
- **License**: `Creative Commons Zero 1.0` (CC0) — the most permissive licence in this family.
- **Obtainability**: **BLOCKED** — the GitHub repository cited in the paper
  (`github.com/LivingFutureLab/VoiceGiraffe`) returned **HTTP 404 Not Found**. Not yet public.
- **Rough download size**: not retrieved.
- **Eval metric as published**: not retrieved.
- **Knowledge-coupling potential**: **MEDIUM (provisional).** Multi-hop reasoning over hour-scale
  podcast speech is a natural place for retrieved evidence to matter, and 1,500 curated items is a
  workable evaluation size. Cannot be rated confidently without seeing whether items ship a
  document/transcript field.
- **G1' admission verdict**: **CONDITIONAL, pending release.** Fails (2) obtainability today — the
  official repo 404s. Criterion (4) is unassessable (metric not retrieved) and (5) is provisional.
  CC0 and real podcast speech make it attractive enough to re-check in a few weeks; if it lands with
  a per-item transcript field and a deterministic metric, it would be a strong long-form candidate.
  Track, do not plan around it.

---

## AEG evaluation suite (reference point, not a dataset candidate)

- **Name**: "Attention-guided Evidence Grounding for Spoken Question Answering" (AEG + LFE)
- **arXiv ID**: 2603.16292
- **already-local / not-local**: n/a — **no dataset is released.** Audio queries are synthesized
  from existing text benchmarks (SQuAD v1.1, HotpotQA, MuSiQue) using Higgs Audio TTS.
- **Why it is recorded here**: it is the only source found in this sweep that publishes **frozen
  Qwen3-Omni baselines on spoken QA**, which is directly relevant to this program's core. Reported
  baseline accuracies (Table I):

  | Model | HotpotQA | MuSiQue | SQuAD |
  |---|---|---|---|
  | GPT-4o Audio | 79.07 | 51.51 | 88.49 |
  | Qwen3-Omni Flash | 73.44 | 44.72 | 79.51 |
  | **Qwen3-Omni-30B-A3B** | **75.02** | **45.88** | **88.37** |
  | LongCat-Flash-Omni | 74.36 | 49.57 | 84.32 |

  AEG+LFE adds 0.87–4.42 points absolute. Two cautions: the method **fine-tunes attention** (LFE),
  so it is not a frozen-core result and is not a like-for-like comparator for this program; and the
  audio is TTS-synthesized, so these numbers do not transfer to real-speech sets.
- **Usefulness to the study**: it establishes that (a) Qwen3-Omni-30B-A3B is already measurable on
  spoken multi-hop QA, (b) MuSiQue-style multi-hop is where the frozen core is weakest (45.88),
  which is the largest available headroom for an evidence-supply intervention, and (c) a spoken
  multi-hop set can be constructed by TTS over an existing text multi-hop benchmark — a route the
  study could take if no suitable real-speech multi-hop set exists. It also confirms the absence of
  a public real-speech multi-hop spoken QA benchmark as of this sweep.
- **G1' admission verdict**: n/a (not a dataset). Retain as a **baseline and protocol reference**.

---

## Out-of-boundary and out-of-language candidates (recorded for completeness)

- **LA-RAG / CASTELLA-QA** (arXiv 2602.14612, "Event-Grounded Question Answering over Long Audio via
  Structured Retrieval"). **REJECT — out of boundary.** Its audio is general/environmental sound:
  alarms, door knocks, machinery, welders, forklifts, sourced from proprietary sound libraries and
  Freesound. The Home-IoT and Industrial-IoT benchmarks are synthetic 24-hour environmental
  recordings. CASTELLA-QA (~200 questions) is real-world audio moment retrieval, still
  environmental. No speech subset is separable. Fails criterion (1) outright. Noted because its
  *structured-retrieval* architecture is methodologically adjacent to this study's SUPPLY component
  even though its data is not admissible.
- **ViSQA** (Vietnamese Spoken QA, >13,000 QA pairs, extends UIT-ViQuAD via a TTS+ASR pipeline).
  **REJECT** — Vietnamese only, no English slice; additionally TTS-derived. In-boundary as speech.
- **CLSR** (arXiv 2511.09282, end-to-end contrastive language-speech retriever for long-form spoken
  QA). **No dataset released** — evaluates on four existing cross-modal retrieval sets. Method
  reference only.
- **Speech-XL** (arXiv 2602.05373). **No dataset released** — a model paper evaluating on LongSpeech
  and AudioMarathon.
- **SpeechRAG** (arXiv 2412.16500, ICASSP 2025). **No dataset released** — a method that retrieves
  audio passages from text queries without ASR, evaluated on Spoken-SQuAD and VoxPopuli. Relevant as
  the closest published prior on the SUPPLY axis; note that its two eval sets are, for this program,
  respectively synthetic and owner-excluded (>1 TB).
- **AudioBench** (NAACL 2025, `AudioLLMs/AudioBench`). **Harness, not a dataset.** Its SQA slate is
  `slue_p2_sqa5_test`, `spoken_squad_test`, `clotho_aqa_test`, `public_sg_speech_qa_test`,
  `dream_tts_mcq_test`. **`clotho_aqa_test` is out of boundary** (Clotho is environmental audio) and
  must never be pulled in through the harness. All AudioBench SQA metrics are `llama3_70b_judge` or
  `gpt4o_judge`; the latter is paid. If the harness is used at all, it must be used for data loading
  only, with metrics re-derived.

---

## Family summary

| Candidate | Local? | Real speech? | Size | License | Obtainable | Knowledge-coupling | Verdict |
|---|---|---|---|---|---|---|---|
| SLUE-SQA-5 | already-local | Yes (both sides) | 118 GB; 46,186/1,939/2,382/408 | Mixed: Apache-2.0 + CC BY-SA 4.0 | ungated HF | HIGH | ADMIT |
| HeySQuAD (human) | already-local | Yes (questions) | 14.6 GB; 76,148 rows | CC-BY-4.0 | ungated HF | HIGH | ADMIT |
| SpokenNativQA | not-local | Yes | 364 MB; 13,234 rows (~2,320 EN/ASR) | CC BY-NC-SA 4.0 | ungated HF | HIGH (no passage = no leakage) | ADMIT (EN subset) |
| SD-QA | not-local | Yes (dialect speakers) | not retrieved; 68k prompts, ~1k EN questions | Apache-2.0 | Google Drive, ungated | HIGH | ADMIT (EN subset) |
| VoxEval | not-local | No (OpenAI TTS ×6) | 88.1 GB; 408,764 rows | CC BY 4.0 | ungated HF | HIGH (closed-book) | ADMIT (condition subset) |
| NSF-QA | not-local | Yes (real meetings) | 305 GB; 50,574 rows | CC BY-NC 4.0 | ungated HF | HIGH (entity QA) | CONDITIONAL (metric 4, size) |
| NMSQA | not-local | No (TTS) | not retrieved; 98.3k rows | not stated | ungated HF | MEDIUM-HIGH | CONDITIONAL (license, 171-row test) |
| Spoken-SQuAD (orig.) | mirror only | No (Google TTS) | ~50 GB; 37,111/5,351 | CC-BY-SA-4.0 | direct download | MEDIUM (leakage hazard) | CONDITIONAL (5) |
| Spoken-SQuAD (AudioLLMs) | already-local | No (TTS) | 3.4 GB; 5,351 rows | CC-BY-SA-4.0 | ungated HF | MEDIUM (leakage hazard) | CONDITIONAL (metric 4) |
| VoiceGiraffe | not-local | Yes (podcasts/speeches) | not retrieved; 1,500 triplets | CC0 1.0 | **404 — not released** | MEDIUM (provisional) | CONDITIONAL (2) |
| LibriSQA | already-local (metadata) | Yes (LibriSpeech) | 171 MB + LibriSpeech; 214k pairs | CC BY 4.0 | ungated HF | LOW | REJECT (5) |
| LongSpeech | not-local | Mixed (real + TTS movie corpus) | ~16,667 h; 8,000 TIL items | CC BY-NC-**ND** 4.0 | **401 — gated/unreleased** | MEDIUM | REJECT (2,4 + ND) |
| ChronosAudio | not-local | No (F5-TTS) | >200 h; 36,000 items | CC BY 4.0 | **anonymous link only** | LOW-MEDIUM | REJECT (2,4,5) |
| ODSQA | not-local | Yes (20 speakers) | not retrieved; 3,654 q / 1,465 with audio | not stated | direct download | MEDIUM | REJECT (English-only rule) |
| ViSQA | not-local | No (TTS) | >13,000 pairs | not retrieved | not retrieved | MEDIUM | REJECT (language) |
| LA-RAG / CASTELLA-QA | not-local | **No — environmental audio** | ~200 questions + 2×24 h synthetic | CC BY 4.0 (paper) | not retrieved | n/a | REJECT (out of boundary) |
