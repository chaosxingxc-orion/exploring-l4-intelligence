# Voice-assistant eval + meeting/long-form understanding — candidate notes (2026-08-17)

Scout family: voice-assistant / spoken-LLM evaluation suites, and meeting / long-form speech
understanding. Scouted by web evidence only (WebSearch / WebFetch); nothing was downloaded.

**Hard scope boundary applied to every verdict below.** Human speech and its linguistic content
only. General/environmental audio and music are out of scope. Where a candidate is a *mixed* audio
benchmark (MMAU, AIR-Bench, AudioBench, Dynamic-SUPERB, AudioMarathon, BLAB, AudioRAG), the verdict
is scoped to the enumerated speech-linguistic configs and the sound/music configs are named as
excluded. A mixed benchmark is never admitted whole.

**G1' criteria** used for every verdict: (1) in-boundary, (2) zero-cost obtainable, (3)
adapter-mappable for a frozen turn-based omni core reached over an API-shaped boundary, (4) pinnable
metric — deterministic and reproducible offline; paid-judge-only scoring is a failure because
program spend is 0, (5) non-trivial knowledge-coupling — a concrete field where externally supplied
evidence could change the outcome.

**Evidence-quality note.** Where a number could not be retrieved from an official page it is written
"not retrieved". Where an aggregator and an official page disagree, both are recorded.

---

# Part A — voice-assistant / spoken-LLM eval suites

## VoiceBench

- **Name / IDs**: VoiceBench: Benchmarking LLM-Based Voice Assistants. arXiv **2410.17196**;
  TACL 2026. Official GitHub `https://github.com/MatthewCYM/VoiceBench`; leaderboard
  `https://matthewcym.github.io/VoiceBench/`; official HF dataset `hlt-lab/voicebench`.
- **Local status**: **already-local** (modelscope mirror `lmms-lab/voicebench`, 11.2 GB).
  *Discrepancy*: the local mirror is `lmms-lab/voicebench`; the paper's own dataset id is
  `hlt-lab/voicebench`. Treat `hlt-lab/voicebench` as the identity authority.
- **Speech subset enumeration**: VoiceBench is speech-only — there are no sound/music configs, so
  no subset carve-out is required for boundary reasons. Configs, per the official README table:
  `alpacaeval` (199, Google TTS), `alpacaeval_full` (636, Google TTS), `commoneval` (200, human),
  `wildvoice` (1000, human), `sd-qa` (553, human), `openbookqa` (455, Google TTS), `mmsu` (3074,
  Google TTS), `mtbench` (46, Google TTS), `ifeval` (345, Google TTS), `bbh` (1000, human),
  `advbench` (520, Google TTS).
- **Task shape and I/O**: single-turn spoken instruction in, text response out (`mtbench` is
  multi-turn). Directly adapter-mappable to a turn-based frozen omni core.
- **Size**: ~8,000 items across configs; hours not stated; #speakers not stated (TTS voices plus
  crowd recordings).
- **Language coverage**: English. `sd-qa` covers regional English dialects.
- **Speech provenance**: mixed and config-dependent — Google TTS for `alpacaeval`, `openbookqa`,
  `mmsu`, `mtbench`, `ifeval`, `advbench`; real human speech for `commoneval`, `wildvoice`,
  `sd-qa`, `bbh`.
- **License**: Apache-2.0 (GitHub repository badge).
- **Obtainability**: ungated HF; already local.
- **Download size**: n/a (already local, 11.2 GB).
- **Eval metric**: split. Deterministic configs — `openbookqa`, `mmsu` (MCQ accuracy), `ifeval`
  (rule-based instruction-following), `bbh`, `advbench` (harm-string matching). **Paid-judge
  configs** — `alpacaeval`, `alpacaeval_full`, `commoneval`, `wildvoice`, `sd-qa` are scored by
  **GPT-4o** as judge. No local open-weight judge is sanctioned by the benchmark.
- **Published omni baselines**: extensive leaderboard covering Qwen2-Audio and Qwen2.5-Omni;
  exact Qwen3-Omni row not retrieved.
- **Knowledge-coupling**: **LOW**. The knowledge probed (`openbookqa`, `mmsu`) is parametric and
  the items carry no external evidence slot. `sd-qa` is the only partial exception — its
  region-conditioned answers form a small "locale fact" slot — and that is incidental, not
  designed. Honest read: this is a general assistant-capability suite, not an evidence-acquisition
  testbed.
- **G1' verdict**: **CONDITIONAL**, scoped to the deterministic configs only. Passes (1) (2) (3)
  (4-partial). **Fails (5)**. Use as a capability-regression guard so a control plane can be shown
  not to damage general assistant behaviour; do not use it as a primary claim surface. The
  GPT-4o-judged configs must be excluded outright — paid judge, spend must stay 0.

## AudioBench

- **Name / IDs**: AudioBench: A Universal Benchmark for Audio Large Language Models. arXiv
  **2406.16020** (NAACL 2025). Official GitHub `https://github.com/AudioLLMs/AudioBench`; HF org
  `https://huggingface.co/AudioLLMs`.
- **Local status**: **not-local** as a suite. Several of its speech component corpora are already
  local by other routes (earnings21, earnings22).
- **SPEECH SUBSET ENUMERATION** (this is a mixed benchmark; official README dataset list):
  - *Speech-linguistic — ADMISSIBLE region*:
    - ASR: `librispeech_test_clean`, `librispeech_test_other`, `common_voice_15_en_test`,
      `peoples_speech_test`, `gigaspeech_test`, `tedlium3_test`, `tedlium3_long_form_test`,
      **`earnings21_test`**, **`earnings22_test`**, `aishell_asr_zh_test`, `imda_part1..6_asr_test`
      (Singlish), `seame_dev_man`, `seame_dev_sge`, `gigaspeech2_thai/indo/viet`, `ASCEND`.
    - Speech translation: `covost2_*` (en-id, en-zh, en-ta, id-en, zh-en, ta-en), `fleurs`.
    - Speech QA: `cn_college_listen_mcq_test`, `slue_p2_sqa5_test`, `dream_tts_mcq_test`,
      `public_sg_speech_qa_test`, **`spoken_squad_test`**.
    - Speech instruction following: `openhermes_audio_test`, `alpaca_audio_test`, `spoken-mqa_*`,
      `audiollm_instructionfollowing` (IFEval-Audio).
    - Speech summarization: `imda_*_summarization` variants.
    - Paralinguistic *over human speech* (in-boundary but low value here):
      `iemocap_emotion_test`, `meld_sentiment_test`, `meld_emotion_test`, `voxceleb_accent_test`,
      `imda_ar_*`, `voxceleb_gender_test`, `iemocap_gender_test`.
  - *Sound / music — EXCLUDED, out of boundary*: `wavcaps_test`, `wavcaps_qa_test`,
    `audiocaps_test`, `audiocaps_qa_test`, `clotho_aqa_test`, `muchomusic_test`, and the imported
    `mmau_mini` and AIR-Bench sound/music tasks.
- **Task shape and I/O**: audio + text instruction in, text out. Fully adapter-mappable.
- **Size**: paper states 8 tasks / 26 datasets, 400+ hours, 100,000+ samples; the live repo states
  "50+ datasets". *Discrepancy recorded* — the paper and the current repo disagree on scale
  because the suite grew after publication.
- **Language coverage**: English is a first-class slice (LibriSpeech, People's Speech, GigaSpeech,
  TED-LIUM3, Earnings21/22, Spoken-SQuAD). Substantial Singlish, Mandarin, Thai, Indonesian,
  Vietnamese, Tamil slices exist and are optional.
- **Speech provenance**: real human speech for ASR/translation/paralinguistic subsets;
  `dream_tts_mcq_test` and `alpaca_audio_test` / `openhermes_audio_test` are TTS-synthesized.
- **License**: **not stated** on the README page fetched; per-component licenses are inherited from
  the source corpora and differ (LibriSpeech CC BY 4.0, Common Voice CC0 + DUA, TED-LIUM3 CC BY-NC-ND,
  IMDA NSC own terms). This is a per-subset licence problem, not a suite-level one.
- **Obtainability**: ungated HF for the AudioLLMs-hosted derivatives (e.g.
  `AudioLLMs/spoken_squad_test`, `AudioLLMs/openhermes_instruction_test`). Note that several
  underlying corpora are separately blocked for this program (common-voice-22 DUA, ted-lium3 404).
- **Download size for the slice we would consume**: not retrieved as a single figure. The narrow
  slice worth taking (`spoken_squad_test`, `slue_p2_sqa5_test`, `earnings21/22_test`) is small —
  earnings21/22 are already local; Spoken-SQuAD test is on the order of a few GB. Estimate
  **~3–6 GB**, not verified.
- **Eval metric**: WER for ASR (deterministic, pinnable); BLEU for translation (deterministic);
  **judge-model** for speech QA / instruction following / paralinguistic. Critically, AudioBench
  **officially sanctions a local open-weight judge**: the README serves **Llama-3-70B via vLLM on
  port 5000** as the judgement model, with GPT-4o as an optional alternative. This is the only
  candidate in the family that ships a sanctioned local judge — it converts an otherwise
  paid-judge metric into a pinnable one, at the cost of hosting a 70B judge.
- **Published omni baselines**: leaderboard covers Qwen2-Audio and the Qwen2.5-Omni family; exact
  Qwen3-Omni rows not retrieved.
- **Knowledge-coupling**: **HIGH — but concentrated in two named configs.**
  `spoken_squad_test` is document-grounded spoken QA: the *passage is an explicit evidence slot*,
  and a control plane that decides which passage to supply, and how, directly changes the outcome.
  `slue_p2_sqa5_test` is likewise document-grounded. `earnings21_test` / `earnings22_test` carry the
  entity-lexicon coupling this program already exploits. Everything else in the suite is LOW.
- **G1' verdict**: **ADMIT — scoped to `spoken_squad_test` + `slue_p2_sqa5_test`** (with
  earnings21/22 already covered locally). Passes all five criteria for that slice, and its
  sanctioned Llama-3-70B local judge resolves the metric problem. **REJECT** the audio-scene and
  music configs (`wavcaps_*`, `audiocaps_*`, `clotho_aqa_test`, `muchomusic_test`, imported
  `mmau_mini`) as out-of-boundary. Treat the multilingual and paralinguistic configs as neutral —
  in-boundary but coupling-LOW.

## AIR-Bench

- **Name / IDs**: AIR-Bench: Benchmarking Large Audio-Language Models via Generative Comprehension.
  arXiv **2402.07729**; ACL 2024. Official GitHub `https://github.com/OFA-Sys/AIR-Bench`.
- **Local status**: **already-local** (modelscope `qfq/AIR-Bench_24.09`, 43.8 GB — the whole
  suite, sound and music included).
- **SPEECH SUBSET ENUMERATION** (mixed benchmark; foundation track = 19 tasks):
  - *Speech — ADMISSIBLE (9 tasks)*: speech grounding; spoken language identification; speaker
    gender recognition; emotion recognition; speaker age prediction; **speech entity recognition**;
    **intent classification**; speaker number verification; synthesized voice detection.
  - *Sound — EXCLUDED (4 tasks)*: audio grounding; vocal sound classification; acoustic scene
    classification; sound question answering.
  - *Music — EXCLUDED (6 tasks)*: music instruments classification; music genre classification;
    music note analysis-pitch; music note analysis-velocity; music question answering; music
    emotion detection.
  - *Chat track*: Speech 800 instances (admissible), Sound 400 (excluded), Music 400 (excluded),
    Mixed Audio 400 — **excluded**, because the 400 mixed items are explicitly 200 speech+sound
    and 200 speech+music, i.e. they require non-speech audio reasoning by construction.
- **Task shape and I/O**: foundation = audio + single-choice question in, letter out. Chat =
  audio + open question in, free text out. Both adapter-mappable.
- **Size**: foundation ~19k single-choice questions across 19 tasks; chat 2k open-ended instances.
  Hours not stated; #speakers not stated.
- **Language coverage**: English-dominant; spoken language identification is multilingual by design.
- **Speech provenance**: real human speech drawn from LibriSpeech, Common Voice, MELD, IEMOCAP,
  SLURP and VoxCeleb1; the FoR corpus supplies synthetic speech deliberately, as the positive class
  for the synthesized-voice-detection task.
- **License**: verbatim — *"AIR-Bench is released under Apache License Version 2.0."*
- **Obtainability**: already local; ungated upstream.
- **Download size for the speech slice**: not retrieved separately; the local full bundle is
  43.8 GB and the speech portion is a fraction of it.
- **Eval metric**: foundation track is single-choice → deterministic accuracy, **pinnable**. Chat
  track is scored by **GPT-4 Turbo, `gpt-4-0125-preview`**, reference-based with position-swapped
  rounds — **paid judge, no local alternative sanctioned → not pinnable for this program.**
- **Published omni baselines**: leaderboard shows Speech / Sound / Music / Mixed-Audio columns for
  Qwen-Audio-family models; Qwen3-Omni row not retrieved.
- **Knowledge-coupling**: **MEDIUM, concentrated in two tasks.** `speech entity recognition` and
  `intent classification` (SLURP-derived) expose a real slot — an entity roster or an intent/slot
  ontology supplied at prompt time can plausibly move accuracy. The other seven speech tasks
  (gender, age, emotion, speaker count, language ID, synthesized-voice detection, speech grounding)
  are acoustic-attribute tasks with essentially **LOW** coupling: no external evidence changes them.
- **G1' verdict**: **CONDITIONAL — foundation-track speech tasks only, and in practice only
  `speech entity recognition` + `intent classification`.** Passes (1)(2)(3)(4)(5) for that pair.
  **REJECT the chat track on criterion (4)** (GPT-4 Turbo judge only). **REJECT all sound, music and
  mixed-audio tasks on criterion (1)**. Note SLURP slot-SLU is already admitted to this program
  through the entity clause of the 2026-08-15 owner amendment, so AIR-Bench's intent/entity tasks
  overlap work already authorized rather than opening new ground.

## OpenAudioBench

- **Name / IDs**: OpenAudioBench, released with Baichuan-Omni-1.5 / Baichuan-Audio. Official HF
  dataset `baichuan-inc/OpenAudioBench`; official GitHub `https://github.com/baichuan-inc/Baichuan-Audio`.
  No standalone arXiv ID — it is a dataset release accompanying the Baichuan-Omni-1.5 report.
- **Local status**: **not-local**.
- **Speech subset enumeration**: speech-only, no sound/music configs. Five sub-datasets:
  `Reasoning QA` (202, in-house logical reasoning), `Llama Questions` (300), `Web Questions`
  (1000), `TriviaQA` (1000), `AlpacaEval` (199). Card totals **2,701** in the README text but the
  viewer reports **2,900 rows** — *discrepancy recorded, not resolved.*
- **Task shape and I/O**: spoken question in, text (or speech) answer out. Adapter-mappable.
- **Size**: ~2.7–2.9k items; hours not stated; #speakers not stated.
- **Language coverage**: not stated on the card. The source sets (Llama Questions, WebQuestions,
  TriviaQA, AlpacaEval) are English; the Baichuan release is bilingual zh/en, so a Chinese slice is
  likely. Not verified.
- **Speech provenance**: **not stated** on the dataset card. The source sets are text corpora, so
  the audio is near-certainly TTS-synthesized — but this was not confirmed on an official page and
  must be verified before use.
- **License**: **not stated** on the dataset card fetched.
- **Obtainability**: ungated HF, direct.
- **Download size**: **666 MB** (~0.65 GB) — the smallest serious candidate in Part A.
- **Eval metric**: per-component — "Accuracy" for Llama Questions / Web Questions / TriviaQA
  (open-domain factoid, string/EM-style), "Score" for Reasoning QA and AlpacaEval. Whether the
  "Score" components require GPT-4 was **not stated** on the card; the AlpacaEval lineage implies a
  judge model. Treat the two Score components as **judge-dependent and not yet pinned**.
- **Published omni baselines**: Baichuan-Omni-1.5 results are produced by the repo's `./output`
  path; specific numbers not retrieved. No Qwen-Omni row on the card.
- **Knowledge-coupling**: **MEDIUM.** Spoken TriviaQA and WebQuestions are the classic open-domain
  factoid shape: the answer is a named entity that a retrieved KB snippet can supply, so SUPPLY and
  USE are genuinely exercised. But OBS and ORG are not — nothing in the audio needs an entity
  roster to be *heard* correctly, because the questions are short and clean. Half the control
  plane goes untested.
- **G1' verdict**: **CONDITIONAL.** Passes (1)(2)(3) and (5-partial). **Fails (4) for the two
  "Score" components** until the judge is pinned; the three Accuracy components are pinnable and
  usable today. Blocking gap: licence not stated and provenance not stated — both must be resolved
  on an official page before acquisition. Cheap enough (0.65 GB) to be worth resolving.

## VoxEval

- **Name / IDs**: VoxEval: Benchmarking the Knowledge Understanding Capabilities of End-to-End
  Spoken Language Models. arXiv **2501.04962**; ACL 2025 main. Official GitHub
  `https://github.com/dreamtheater123/VoxEval`; official HF dataset `qqjz/VoxEval`.
- **Local status**: **not-local**.
- **Speech subset enumeration**: speech-only; no sound/music configs. Organized by MMLU-style
  subject (e.g. `abstract_algebra`, …) crossed with speaker voice.
- **Task shape and I/O**: **speech in, speech out** — both question and reference answer are
  audio. For a frozen omni core that emits text, the intended S2S protocol must be relaxed to
  speech-in/text-out, which departs from the published setting.
- **Size**: **408,764 rows** on the HF card (subject × voice × audio-condition cross product);
  hours not stated; speakers = 6 TTS voices plus style/quality perturbations.
- **Language coverage**: not explicitly stated on the card; the MMLU lineage makes it English.
- **Speech provenance**: **fully TTS** — voices `alloy`, `echo`, `fable`, `nova`, `onyx`,
  `shimmer`, with additional variation in speaking style (speed, pitch) and audio quality (noise,
  environmental acoustics). No real human speech.
- **License**: verbatim — *"Creative Commons Attribution 4.0"*.
- **Obtainability**: ungated HF, direct.
- **Download size**: **88.1 GB**. This is the largest Part A candidate by a wide margin and is
  disproportionate to its value here.
- **Eval metric**: ASR-then-match — the pipeline transcribes model speech output with
  **Whisper large-v3** and compares. Deterministic given a pinned Whisper build, so **pinnable**,
  and **no paid judge**. Good metric hygiene.
- **Published baselines**: SpeechGPT, TWIST, SPIRIT-LM, Moshi, GLM-4-Voice; GLM-4-Voice best at
  0.3763 average across speaker variations. **No Qwen-Omni baseline.**
- **Knowledge-coupling**: **LOW.** VoxEval measures whether knowledge *already inside the model*
  survives the speech channel. There is no evidence slot in the item — no document, no roster, no
  KB entry. One could bolt a retrieval slot on, but that would be our construction, not the
  benchmark's, and the benchmark's own axis (robustness to audio conditions) is an OBS-robustness
  axis rather than a knowledge axis.
- **G1' verdict**: **REJECT on criterion (5)**, with a note. Passes (1)(2)(4) cleanly and has an
  unusually honest metric. Fails (3) partially — its S2S protocol does not fit a text-emitting
  frozen core without modification — and fails (5) outright. 88.1 GB for a LOW-coupling suite is a
  poor trade. Reconsider only if an OBS-robustness ablation (timbre / noise / speed) becomes a
  named claim, in which case take a single-subject slice, not the full 88 GB.

## MMSU

- **Name / IDs**: MMSU: A Massive Multi-task Spoken Language Understanding and Reasoning Benchmark.
  arXiv **2506.04779**. Official HF dataset `ddwang2000/MMSU`.
- **Local status**: **already-local** (`ddwang2000/MMSU`, 1.66 GB, mit).
- **Speech subset enumeration**: speech-only by construction — 47 tasks spanning phonetics,
  prosody, rhetoric, syntactics, semantics, paralinguistics. No sound or music configs. No carve-out
  needed.
- **Task shape and I/O**: audio + question in, multiple-choice answer out. Adapter-mappable.
- **Size**: **5,000** audio-question-answer triplets across 47 tasks. Hours not stated; #speakers
  not stated.
- **Language coverage**: not stated on the abstract page; English-centric with code-switching QA
  among the tasks.
- **Speech provenance**: not stated on the pages fetched — must be confirmed per task before use.
- **License**: `mit` per the local record.
- **Obtainability**: ungated HF; already local.
- **Download size**: n/a (1.66 GB local).
- **Eval metric**: multiple-choice accuracy → deterministic, **pinnable, no paid judge**.
- **Published omni baselines**: 14 advanced SpeechLLMs evaluated; specific Qwen-Omni rows not
  retrieved. Note VoiceBench re-hosts a 3,074-item `mmsu` config, so there is partial double-count
  risk against the local VoiceBench copy.
- **Knowledge-coupling**: **LOW.** Pun interpretation, disfluency detection, intonation-based
  reasoning and homophone reasoning are intrinsic-signal tasks. There is no field where an entity
  roster, document or KB entry would legitimately change the answer — supplying one would be
  leakage, not evidence. This is the clearest LOW-coupling case in the family and should be
  stated as such rather than hedged.
- **G1' verdict**: **REJECT on criterion (5)** as a claim surface; **retain as an in-boundary,
  zero-cost, deterministic capability probe** since it is already local. Passes (1)(2)(3)(4).

## MMAU (speech subset only)

- **Name / IDs**: MMAU: A Massive Multi-Task Audio Understanding and Reasoning Benchmark. arXiv
  **2410.19168**. Official GitHub `https://github.com/Sakshi113/MMAU`; homepage
  `https://sakshi113.github.io/mmau_homepage/`; official HF `gamma-lab-umd/MMAU-test-mini` and
  `gamma-lab-umd/MMAU-test`.
- **Local status**: **already-local** (`TwinkStart/MMAU`, 2.8 GB). *Discrepancy*: the official
  `gamma-lab-umd/MMAU-test-mini` card reports **1.21 GB / 1,000 rows**, while the local mirror is
  2.8 GB — the mirrors differ and the official card is the identity authority.
- **SPEECH SUBSET ENUMERATION** (mixed benchmark — this carve-out is mandatory):
  - *Speech — ADMISSIBLE*: the speech third of test-mini and test. Sources visible on the official
    card for speech items include **MUSTARD** (sarcasm / speech-based emotion interpretation).
  - *Sound / environmental — EXCLUDED*: sourced from **AudioSet** and `AudioSet_SL`, plus
    `Synthetic` temporal-event items. AudioSet is on this program's permanent exclusion list, so
    this portion is hard-blocked, not merely deprioritized.
  - *Music — EXCLUDED*.
  - **Counts**: the corpus is described as balanced so that speech, sound and music each account
    for roughly one third, i.e. ~333 speech questions in test-mini and ~3,000 in the full test.
    An exact official per-domain table was **not retrieved** (the arXiv PDF fetch returned
    corrupted bytes and the HTML v2/v3 URLs 404'd). Treat "~333 / ~3,000" as approximate.
- **Task shape and I/O**: audio + four-way multiple-choice question in, letter out.
- **Size**: 10,000 items total (test-mini 1,000; test 9,000), 27 skills. Hours not stated.
- **Language coverage**: English.
- **Speech provenance**: real human speech for the speech third (MUSTARD is TV-show audio);
  synthetic items exist in the sound third.
- **License**: **discrepancy recorded** — the official GitHub states **Apache-2.0**; the official
  HF card for `MMAU-test-mini` states **cc-by-nc-4.0**. These conflict. Do not pick one; treat the
  more restrictive (cc-by-nc-4.0) as binding until the maintainers clarify.
- **Obtainability**: test-mini is ungated and direct. **The full test set's answers are withheld**
  — scoring requires submission to the MMAU Eval HF Space / EvalAI leaderboard.
- **Download size for the speech slice**: ~0.4 GB of the 1.21 GB test-mini, estimated by the
  one-third split; not verified.
- **Eval metric**: micro-average accuracy via the repo's `evaluation.py` on test-mini →
  deterministic, **pinnable, no paid judge**. The full test set is **not pinnable offline** because
  answers are withheld.
- **Published omni baselines**: Qwen2-Audio 55.4% overall (best open-source at publication). No
  Qwen-Omni row on the homepage.
- **Knowledge-coupling**: **LOW.** MMAU speech items test perception and reasoning over the audio
  itself (sarcasm, emotion, content inference). There is no document, roster or KB field, and
  supplying one would not legitimately change the answer.
- **G1' verdict**: **REJECT as a claim surface — CONDITIONAL as an in-boundary probe.** The speech
  third alone passes (1)(2)(3)(4-on-test-mini) but **fails (5)**. The sound third **fails (1)
  hard** via AudioSet and must never be loaded. The full test set **fails (4)** (withheld answers,
  leaderboard-only). Since it is already local, the only action is to ensure the loader filters to
  the speech third and physically cannot touch the AudioSet-derived items.

## Dynamic-SUPERB and Dynamic-SUPERB Phase-2

- **Name / IDs**: Dynamic-SUPERB (Phase-1, ICASSP 2024) and **Dynamic-SUPERB Phase-2: A
  Collaboratively Expanding Benchmark … with 180 Tasks**, arXiv **2411.05361**, ICLR 2025.
  Official GitHub `https://github.com/dynamic-superb/dynamic-superb`; official HF org
  `https://huggingface.co/DynamicSuperb`.
- **Local status**: **not-local**.
- **SPEECH SUBSET ENUMERATION** (mixed benchmark): Phase-2 spans **180 tasks** across three
  declared domains — **speech processing** (admissible), **music analysis** (excluded), **general
  sound / environmental audio** (excluded). A per-task speech/music/sound breakdown with counts
  was **not retrieved** from the abstract or the repo landing page; the task registry in the
  GitHub repo would have to be enumerated file-by-file to produce it. **This is the single largest
  open item in this family** — Dynamic-SUPERB cannot be admitted until each of the 180 task
  directories is classified, because sound/music tasks are interleaved with speech tasks in one
  registry and one HF org.
- **Task shape and I/O**: natural-language instruction + audio in, text out. Phase-1 was
  classification-only; Phase-2 adds regression and sequence generation. Adapter-mappable.
- **Size**: 180 tasks; per-task item counts and total hours not stated on the pages fetched.
- **Language coverage**: English-dominant with multilingual community contributions.
- **Speech provenance**: mixed — contributed tasks draw on both real corpora and synthesized audio;
  varies per task and is not summarized centrally.
- **License**: **not stated** on the abstract or repo landing page. Per-task licences are inherited
  from contributors' source corpora and are heterogeneous by construction.
- **Obtainability**: ungated HF org, direct — but 180 separate dataset repos.
- **Download size for the speech slice**: not retrieved.
- **Eval metric**: accuracy for classification tasks, plus regression and sequence-generation
  metrics in Phase-2; the exact per-task metric registry was **not retrieved**. No evidence that a
  paid judge is required — but also no positive confirmation.
- **Published omni baselines**: SALMONN-13B strong on English ASR; Qwen2-Audio-7B-Instruct strong on
  emotion recognition. No Qwen-Omni row retrieved.
- **Knowledge-coupling**: **MEDIUM at best, and diluted.** Among 180 tasks there will be a handful
  with genuine evidence slots (entity/lexicon-conditioned recognition, instruction-conditioned
  extraction), but the great majority are attribute-classification tasks with LOW coupling. The
  suite's value proposition is breadth, which is orthogonal to what this program needs.
- **G1' verdict**: **CONDITIONAL, blocked on enumeration.** Cannot be admitted or rejected
  responsibly until (a) the 180 tasks are classified speech vs music vs sound, (b) per-task licences
  are checked, and (c) per-task metrics are confirmed judge-free. Given (5) is MEDIUM-at-best and
  the enumeration cost is high, recommend **deprioritize** rather than spend the enumeration budget
  now.

## URO-Bench

- **Name / IDs**: URO-Bench: A Comprehensive Benchmark for End-to-End Spoken Dialogue Models.
  arXiv **2502.17810**. Official GitHub `https://github.com/Ruiqi-Yan/URO-Bench`.
  *Discrepancy*: the task brief quoted arXiv 2501-series for adjacent items; the ADS record gives
  **2502.17810** for URO-Bench. Use 2502.17810.
- **Local status**: **already-local** (`Honggao/URO-Bench`, 12.1 GB, mit).
- **Speech subset enumeration**: speech-only; no sound/music configs.
- **Task shape and I/O**: speech-to-speech dialogue. Basic track and pro track, 20 test sets each,
  40 datasets / 20 task types, covering Understanding, Reasoning and Oral conversation, plus
  multilingualism, multi-round dialogue and paralinguistics.
- **Size**: 40 datasets; item counts and hours not retrieved.
- **Language coverage**: multilingual by design (English and Chinese at minimum).
- **Speech provenance**: mixed; per-set provenance not retrieved.
- **License**: `mit` per the local record.
- **Obtainability**: already local.
- **Download size**: n/a (12.1 GB local).
- **Eval metric**: **GPT-based assessment** across much of the suite (GPT-4o-Audio-Preview appears
  in the paper's own miniset evaluation). No sanctioned local open-weight judge found →
  **paid-judge dependency for the open-ended sets.**
- **Published omni baselines**: GLM-4-Voice (strongest), LLaMA-Omni, SLAM-Omni, Mini-Omni, plus a
  Whisper+LLM cascade reference. No Qwen-Omni row retrieved.
- **Knowledge-coupling**: **LOW.** The axes are understanding, reasoning and oral quality — there
  is no evidence slot in the item design. Oral-quality axes are additionally near-meaningless for a
  text-emitting frozen core.
- **G1' verdict**: **REJECT on criteria (4) and (5)**; partially fails (3) because its S2S oral
  axes do not map onto a text-emitting turn-based core. Already local, so no acquisition cost is at
  stake — simply do not build a claim on it.

## ADU-Bench

- **Name / IDs**: Benchmarking Open-ended Audio Dialogue Understanding for Large Audio-Language
  Models. arXiv **2412.05167**; ACL 2025 (`aclanthology.org/2025.acl-long.237/`). Official GitHub
  `https://github.com/KuofengGao/ADU-Bench`; site `https://adu-bench.github.io/`; official HF
  `KuofengGao/ADU-Bench`.
- **Local status**: **not-local**.
- **Speech subset enumeration**: speech-only — four datasets, **ADU-General**, **ADU-Skill**,
  **ADU-Multilingual**, **ADU-Ambiguity**. No sound/music configs. The ambiguity set is
  paralinguistic-over-speech (intonation, pause position, homophones), which stays in boundary.
- **Task shape and I/O**: spoken open-ended dialogue turn in, free-text response out.
  Adapter-mappable.
- **Size**: **20,715** open-ended audio dialogues, of which **over 8,000 are real-world
  recordings**, the remainder synthetic. Coverage: 3 general scenarios, 12 skills, 9 languages,
  4 ambiguity categories. *Discrepancy*: the official HF card viewer shows only **210 rows /
  2.21 GB** in a single `default/train` split, which is irreconcilable with 20,715 dialogues — the
  HF repo appears to host a sample or a differently-structured release. **Resolve before
  acquisition.**
- **Language coverage**: 9 languages; English is present but is one of nine, so it is a minority
  slice of the multilingual set (the General/Skill/Ambiguity sets are English-centric).
- **Speech provenance**: **mixed and explicitly so** — >8,000 real human recordings alongside
  synthetic audio. Per-dataset provenance breakdown not retrieved.
- **License**: **not stated** on either the GitHub landing page or the HF card.
- **Obtainability**: ungated HF, direct. 2.21 GB as hosted.
- **Download size**: **2.21 GB** as hosted (but see the size discrepancy above).
- **Eval metric**: open-ended dialogue scoring via `evaluation.sh`; whether GPT-4 is the judge was
  **not confirmed** on the official pages. The open-ended format makes a judge model near-certain.
  **Treat as judge-dependent and unpinned.**
- **Published omni baselines**: 16 LALMs evaluated; no Qwen-Omni row retrieved.
- **Knowledge-coupling**: **LOW.** The stated difficulty axes are mathematical symbols, roleplay,
  multilinguality and phonetic ambiguity. None of these has a field where an entity roster,
  document or KB entry would change the answer — the ambiguity axis is intrinsic to the acoustics.
- **G1' verdict**: **REJECT on criterion (5)**, with (4) also unresolved and licence not stated.
  Passes (1)(2)(3). The >8,000 real recordings are a genuine asset, but not for this program's
  question.

## Audio2Tool (2026 — new)

- **Name / IDs**: Audio2Tool: Speak, Call, Act — A Dataset for Benchmarking Speech Tool Use.
  arXiv **2604.22821**. Site `https://audio2tool.github.io/`.
- **Local status**: **ALREADY-LOCAL — CORRECTED 2026-08-17 by the campaign lead.** The family scout
  recorded this candidate as unreleased, reading the arXiv v1 statement "We will release the dataset
  and benchmark upon acceptance". That statement was superseded: the dataset **was** released as
  Hugging Face `RVtech/Audio2Tool` (RVtech = Rivian & Volkswagen Technologies), public and ungated.
  The program holds it at pinned revision `f1388da9a3189541ab82adac88824a0661670c43`,
  **10,474,543,420 bytes / 72,062 files**, recorded in `docs/datasets.lock.json` `asset_catalog` as
  LOCAL_CANDIDATE / COMPLETE. The 2026-08-15 owner amendment approves a single bounded, probe-scoped
  Audio2Tool leverage probe, and the study repo already carries a loader
  (`data/audio2tool.py`), a scorer (`reproduction/a2t_scorer.py`), gold extraction and a
  sample-400 config. **Every "unreleased" claim in this section is void.**
- **Speech subset enumeration**: speech-only. Three domains: Smart Car, Smart Home, Wearables.
- **Task shape and I/O**: spoken command in, structured function call out (tool name + arguments)
  against a supplied tool schema. Maps cleanly onto a turn-based frozen core with a tool-catalog
  prompt.
- **Size**: ~**30,000** queries; **152 verified functions** in **23 categories**. Hours not stated;
  #speakers = the voice-cloning voice pool, count not stated.
- **Language coverage**: not explicitly stated; English-only based on the example queries.
- **Speech provenance**: **fully TTS** — zero-shot voice cloning via **Qwen3TTS** and
  **CosyVoice-3**. The authors state the benchmark "currently relies on generated speech" and defer
  real recordings to future work. This is a real weakness for OBS-side claims.
- **License**: **licence conflict, recorded not resolved.** The paper carries a CC BY 4.0 badge; the
  Hugging Face card and the program's lock entry both record **`cc-by-nc-4.0`**. Treat as
  non-commercial until resolved in writing; this blocks no research use but must be flagged for any
  Stage-3 publication claim.
- **Obtainability**: **already held — ungated public Hugging Face repo.** Not blocked. (The scout's
  "BLOCKED — not yet released" finding was based on the superseded v1 release statement; see the
  corrected local-status entry above.)
- **Download size**: **10.47 GB**, already on disk; no new acquisition required.
- **Eval metric**: **Tool Accuracy** (exact tool-name match), **Exact Match** (tool + all
  arguments), **Slot F1** (parameter-level P/R). Fully deterministic, **no judge required** — the
  best metric hygiene in Part A.
- **Published omni baselines**: **Qwen3-Omni-30B is a headline baseline** — 92.4% on simple
  commands, dropping to **41.7% on complex multi-turn scenarios**. This is the exact model class
  this program runs, and the 50-point drop is a large, well-located headroom band.
- **Knowledge-coupling**: **HIGH.** The tool catalog *is* the injected evidence. Which of the 152
  functions and 23 categories are placed in context, in what order, at what granularity, is
  precisely a SUPPLY/USE decision, and the Exact-Match / Slot-F1 metrics respond to it
  deterministically. Named field: the **function schema list** (and per-function argument
  enumerations) supplied in the prompt.
- **G1' verdict**: **ADMIT (corrected from CONDITIONAL).** Passes all five criteria: in-boundary,
  zero-cost (already held), adapter-mappable and already adapted, deterministic judge-free metrics,
  and HIGH knowledge-coupling through the tool schema. Weakness that must travel with any claim:
  audio is **TTS-only**, so OBS-side findings will not transfer to real human speech without a
  companion corpus — WearVox (real human speech, tool-calling with judge-free AST match) is the
  natural companion for exactly this reason.
- **Baseline reconciliation note**: this scout records Qwen3-Omni-30B at 92.4% on simple commands
  falling to 41.7% on complex multi-turn; the agentic-family scout records ">75% on Tier-1" falling
  to "under 55% EM/F1 on Tiers 5-7"; and the study's own measurement on the local copy is
  **tool-acc 84.6% vs EM 15.6%**. These are three different slices (command tier, metric, and
  split), not three estimates of one quantity. Do not average or cite interchangeably — cite the
  study's own local measurement for internal headroom claims and the paper's numbers only with
  their exact tier/metric qualifiers.

## AudioCRAG (Stream RAG, 2025)

- **Name / IDs**: AudioCRAG, introduced in *Stream RAG: Instant and Accurate Spoken Dialogue Systems
  with Streaming Tool Usage*, arXiv **2510.02044**. Derived from Meta's CRAG benchmark.
- **Local status**: **not-local**.
- **Speech subset enumeration**: speech-only (spoken queries). No sound/music.
- **Task shape and I/O**: spoken factual query in; the system may call **mock web-search and
  knowledge-graph APIs** inherited from CRAG; text answer out. Extremely close fit to a
  SUPPLY/USE control-plane study.
- **Size**: **AudioCRAG-Synthetic 1,862** spoken queries; **AudioCRAG-Human 618** spoken queries
  (2,480 total). Hours not stated; #speakers "a diverse pool of participants", count not stated.
- **Language coverage**: English only.
- **Speech provenance**: **split** — Synthetic is in-house TTS with intelligibility/quality
  filtering; **Human is real human recordings** capturing natural accent and prosody variation.
  Having both halves over the same query set is unusually valuable: it isolates OBS effects.
- **License**: not stated for the benchmark release.
- **Obtainability**: **BLOCKED / partial.** The paper states "We will release Audio CRAG Human
  benchmark upon acceptance." No permanent repository link is given. The underlying CRAG text
  benchmark and its mock APIs are separately available (Meta / KDD Cup 2024), so the knowledge
  substrate is obtainable even if the audio is not.
- **Download size**: not retrieved (unreleased).
- **Eval metric**: CRAG-style three-way scoring — **+1 accurate, −1 incorrect, 0 missing** —
  adjudicated by the **Llama 4 Maverick** LLM evaluator. Open-weight judge, so **no paid API**;
  pinnable given a pinned judge build and decode settings. **The mock web-search and KG APIs are
  simulated, not paid services** — explicitly confirmed.
- **Published omni baselines**: tool integration reported to more than double factual QA accuracy;
  streaming RAG reported at ~20% tool-latency reduction. Specific Qwen-Omni rows not retrieved.
- **Knowledge-coupling**: **HIGH — the highest-fidelity match in Part A.** The item design contains
  an explicit external-evidence slot (mock web search results, KG triples), the answer is a fact
  that the model cannot be assumed to hold, and the scoring rewards abstention (0 for missing)
  rather than only correctness — which is exactly the shape a SUPPLY/USE policy should be measured
  on. Named fields: **retrieved web snippets** and **KG entity records**.
- **G1' verdict**: **CONDITIONAL — ADMIT on release.** Passes (1)(3)(4)(5) strongly, and the
  open-weight Llama-4-Maverick judge plus mock APIs mean zero spend. **Fails (2) today** — audio not
  released. Fallback worth costing: reconstruct an AudioCRAG-equivalent locally from the public CRAG
  text benchmark, which would forfeit the human-recorded half but preserve the knowledge slot.

## AudioRAG (2026)

- **Name / IDs**: AudioRAG: A Challenging Benchmark for Audio Reasoning and Information Retrieval.
  arXiv **2602.10656**. Official GitHub `https://github.com/jingru-lin/AudioRAG`.
- **Local status**: **not-local**.
- **SPEECH SUBSET ENUMERATION**: **predominantly out of boundary.** Source corpora are **FMA** and
  **MusicNet** (music), **iNaturalist** (animal/environmental sound), and **CinePile** (film clips,
  the only partly speech-linguistic source). The benchmark's own framing is "speech, sound, music
  understanding" with the emphasis on sound and music. There is no cleanly separable
  speech-linguistic config.
- **Task shape and I/O**: audio + question in, retrieval-augmented answer out via an agentic loop.
- **Size**: **500** samples. Hours not stated.
- **Language coverage**: not explicitly stated; English-centric from the examples.
- **Speech provenance**: not stated; source corpora are mostly non-speech.
- **License**: CC BY 4.0.
- **Obtainability**: GitHub, direct.
- **Download size**: not retrieved; small (500 items).
- **Eval metric**: accuracy, with **GPT-4o as judge** using structured error categorization →
  **paid judge**. Retrieval uses the **Google Search API** → **paid search**. Reference compute is
  4× A100-40GB.
- **Published omni baselines**: **Qwen3-Omni + Qwen3-8B in an agentic pipeline reaches 46.2%**, a
  reported 24.9% relative improvement over the raw model; best raw model Gemini-2.5-Flash at 45%.
  The Qwen3-Omni pipeline result is directly relevant evidence that agentic evidence supply lifts
  this exact core — worth citing even though the dataset is unusable.
- **Knowledge-coupling**: **HIGH by design** — but the coupling is over environmental sound and
  music, not speech.
- **G1' verdict**: **REJECT.** Fails (1) — the audio is music and environmental sound, which this
  repository must never consume. Fails (2) and (4) — Google Search API and GPT-4o judge are both
  paid. Cite its Qwen3-Omni pipeline result as related work; never acquire the data.

## SpokenWOZ

- **Name / IDs**: SpokenWOZ: A Large-Scale Speech-Text Benchmark for Spoken Task-Oriented Dialogue
  Agents. arXiv **2305.13040**; NeurIPS 2023 Datasets & Benchmarks. Official site
  `https://spokenwoz.github.io/`.
- **Local status**: **not-local**. Not on the candidate list supplied — surfaced during the sweep
  and included because it scores highest on the ranking axis outside Audio2Tool/AudioCRAG.
- **Speech subset enumeration**: speech-only, human-to-human telephone-style conversation. No
  sound/music.
- **Task shape and I/O**: multi-turn spoken task-oriented dialogue over **8 domains**, with dialogue
  state tracking (slot-value prediction) and response generation against a **backing entity
  database**. Turn-based, so adapter-mappable — though multi-turn state must be carried by our
  control plane, which is episode-local and therefore inside the knowledge-not-memory boundary.
- **Size**: **249 hours** of audio, **5,700 dialogues**, **203,000 turns**. #speakers not stated.
- **Language coverage**: English.
- **Speech provenance**: **real human speech** — genuine human-to-human spoken conversations with
  natural disfluency, not TTS and not read speech. This is the strongest provenance in the family
  after AMI/ICSI.
- **License**: **CC BY-NC 4.0** (non-commercial). Research use is fine; note the NC clause.
- **Obtainability**: free and ungated via HuggingFace, with audio and text train/dev/test hosted
  separately.
- **Download size**: not retrieved; 249 hours of telephony-band audio implies roughly **10–25 GB**
  depending on encoding — **not verified**.
- **Eval metric**: **Joint Goal Accuracy** for dialogue state tracking, and **INFORM / SUCCESS /
  BLEU** plus a combined score for response generation. All deterministic, computed by the official
  scripts. **No judge model, no paid API.** Excellent metric hygiene.
- **Published baselines**: best dialogue state tracker reaches only **25.65% joint goal accuracy**;
  the SOTA end-to-end model completes the user request in only **52.1%** of dialogues. Very large
  headroom. **No omni-model baselines published** — nobody has run a Qwen-Omni-class model on it,
  which is both an opportunity and an unknown.
- **Knowledge-coupling**: **HIGH.** Task-oriented dialogue is definitionally knowledge-coupled: the
  correct answer depends on an **entity database** (venues, times, identifiers) that the model
  cannot hold parametrically, and the slot ontology is an explicit **ORG** artifact. Named fields:
  the **domain entity database records** and the **slot/value ontology**. Uniquely among Part A
  candidates, it exercises all four axes — OBS (real disfluent telephony speech, where an entity
  lexicon changes what is heard), ORG (ontology structure), SUPPLY (which DB records to inject),
  USE (whether the injected record is actually used in the response) — and scores each
  deterministically.
- **G1' verdict**: **ADMIT.** Passes all five criteria. In-boundary real human speech; free and
  ungated; turn-based and adapter-mappable; fully deterministic metrics with no judge; and the
  highest genuine knowledge-coupling of any obtainable candidate in Part A. Caveats to record: the
  NC licence, the unverified download size, the absence of any omni baseline (we would be
  establishing it), and the multi-turn state requirement, which must be kept episode-local to
  respect the knowledge-not-memory boundary.

## tau-Voice

- **Name / IDs**: τ-Voice: Benchmarking Full-Duplex Voice Agents on Real-World Domains. arXiv
  **2603.13686**. Code at `sierra-research/tau2-bench` (branch `dev`, path `tau3`).
- **Local status**: **not-local**.
- **Speech subset enumeration**: speech-only.
- **Task shape and I/O**: full-duplex voice customer-service agent over three τ²-bench domains —
  **Retail (114 tasks), Airline (50), Telecom (114); 278 total** — inheriting τ²-bench's
  instructions, tools, databases and domain policies. **Full-duplex is a poor fit** for a
  turn-based frozen core reached over an API-shaped boundary.
- **Size**: 278 tasks; hours not stated.
- **Language coverage**: English only, stated explicitly as a limitation.
- **Speech provenance**: **TTS only** — seven personas via **ElevenLabs v3** at 24 kHz. The authors
  state plainly: "We evaluate English only using TTS rather than recorded speech."
- **License**: CC BY 4.0.
- **Obtainability**: **PAID → automatic exclusion.** Evaluation as published requires subscriptions
  to **OpenAI Realtime, Google Gemini Live and xAI Grok** voice APIs.
- **Download size**: not retrieved.
- **Eval metric**: **Pass@1 via deterministic database-state comparison** against gold — an
  excellent, judge-free metric — plus voice-interaction quality measures (responsiveness, latency,
  interrupt rate, selectivity) and manual error annotation.
- **Published omni baselines**: proprietary realtime voice APIs; no open-weight omni baseline
  retrieved.
- **Knowledge-coupling**: **HIGH.** Domain policy documents and tool/database schemas are supplied
  in the system prompt and the outcome is a database state change — a textbook evidence slot. The
  paper even documents voice-specific policy guidance (spelling names letter-by-letter), which is
  an explicit OBS↔evidence interaction.
- **G1' verdict**: **REJECT.** Fails (2) — paid realtime voice APIs are required by the published
  protocol, and paid access is an automatic exclusion. Fails (3) — full-duplex does not map to a
  turn-based frozen core. Passes (1)(4)(5). Note for the record: its **deterministic DB-state
  Pass@1 metric is the design worth borrowing**, and its text ancestor τ²-bench is free — if a
  knowledge-coupled agentic surface is ever needed, τ²-bench plus our own TTS would be the
  zero-cost route, at the cost of losing the "real benchmark" provenance.

## VCB Bench

- **Name / IDs**: VCB Bench: An Evaluation Benchmark for Audio-Grounded Large Language Model
  Conversational Agents. arXiv **2510.11098**. Official GitHub `https://github.com/Tencent/VCB-Bench`.
- **Local status**: **not-local**.
- **Speech subset enumeration**: speech-only. Three dimensions: **Instruction Following** (3,625),
  **Knowledge** (2,414), **Robustness** (1,415); ~**6,405** total.
- **Task shape and I/O**: spoken instruction/question in, text or speech out. Adapter-mappable.
- **Size**: ~6,405 items; hours not stated; speakers not stated.
- **Language coverage**: bilingual Chinese/English, but **primarily Chinese-centric with English as
  a secondary dimension** — English is a minority slice.
- **Speech provenance**: **exclusively real human speech** — third-party professional recordings,
  variety-show Q&A segments, and an internally curated two-person conversational set. Strong
  provenance.
- **License**: not stated beyond the arXiv perpetual non-exclusive licence for the paper; the
  dataset licence is **not stated**.
- **Obtainability**: GitHub, direct; gating status not confirmed.
- **Download size**: not retrieved.
- **Eval metric**: automatic scoring by **GPT-4o and Gemini-2.5-Pro** (1–5 scales / binary), plus
  subjective MOS from eight expert human raters. **Paid judge, no local open-weight alternative
  sanctioned.**
- **Published omni baselines**: not retrieved.
- **Knowledge-coupling**: **LOW-to-MEDIUM.** The "Knowledge" dimension probes general knowledge and
  reasoning parametrically; there is no supplied-evidence field in the item design.
- **G1' verdict**: **REJECT.** Fails (4) — dual paid-judge scoring with no local alternative. Fails
  (5). English being a minority slice further weakens fit. Passes (1)(3). Real-human provenance is
  its one notable asset.

## Audio MultiChallenge (audiomc)

- **Name / IDs**: Audio MultiChallenge: A Multi-Turn Evaluation of Spoken Dialogue Systems on
  Natural Human Interaction. arXiv **2512.14865**. Official HF `ScaleAI/audiomc`.
- **Local status**: **already-local** (`ScaleAI/audiomc`).
- **Speech subset enumeration**: speech-only, though the Audio-Cue items for Inference Memory
  deliberately require recalling **ambient sounds** alongside paralinguistic signals — those
  specific items graze the boundary and should be excluded on principle even though the carrier is
  a speech conversation.
- **Task shape and I/O**: multi-turn spoken conversation; axes are Inference Memory, Instruction
  Retention, Self Coherence and a new **Voice Editing** axis (mid-utterance repairs, backtracking).
- **Size**: **452 conversations, 47 speakers, 1,712 instance-specific rubrics.**
- **Language coverage**: English.
- **Speech provenance**: **real human speech**, unscripted, with preserved natural disfluencies —
  collected through a hybrid audio-native agentic and human-in-the-loop pipeline.
- **License**: MIT.
- **Obtainability**: ungated HF; already local.
- **Download size**: n/a.
- **Eval metric**: instance-specific **rubrics** → rubric adjudication requires a judge model;
  which judge, and whether an open-weight one is sanctioned, was **not retrieved**. Treat as
  unpinned. (Note the adjacent 2026 literature on reward hacking in rubric-based scoring — rubric
  judges are a known fragility.)
- **Published omni baselines**: not retrieved.
- **Knowledge-coupling**: **LOW for this program's purposes.** The axes are memory and coherence
  across turns. Per the owner's knowledge-not-memory ruling, cross-turn memory is explicitly out of
  this study's object — SAEA studies knowledge, and memory gets its own future study. Measuring
  Inference Memory would be measuring the wrong thing.
- **G1' verdict**: **REJECT on criterion (5)**, and on the standing knowledge-not-memory boundary.
  (4) is unresolved. Already local, so no acquisition decision is at stake; the real-human
  disfluent 47-speaker audio may be worth remembering as an OBS stress source later.

## Scanned 2025–2026 releases set aside (brief)

Surfaced during the sweep, checked against the boundary and the ranking axis, and set aside without
a full schema. Each line states the disqualifying or deprioritizing reason.

- **WavBench** (arXiv 2602.12135) — end-to-end spoken dialogue reasoning/colloquialism/
  paralinguistics. In-boundary; coupling LOW (paralinguistic axes). Deprioritized.
- **MMAR** — already-local (`BoJack/MMAR`); mixed audio-reasoning, sound/music heavy. Boundary
  carve-out required; coupling LOW.
- **SAKURA** (arXiv 2505.13237) — multi-hop reasoning on speech *and audio* information. Mixed;
  coupling LOW.
- **TELEVAL** (arXiv 2507.18061) — Chinese interactive spoken LM benchmark. English absent →
  fails our English requirement as a primary surface.
- **RealTalk-CN** (arXiv 2508.10015) — Chinese speech-text dialogue. Same reason.
- **ParaS2S** (arXiv 2511.08723) — paralinguistic-aware S2S alignment. Coupling LOW; S2S protocol
  mismatch.
- **MULTI-Bench** (arXiv 2511.00850) — multi-turn emotional intelligence for spoken dialogue.
  Coupling LOW.
- **EchoChain** (arXiv 2604.16456) — full-duplex state-update reasoning under interruptions.
  Full-duplex → protocol mismatch with a turn-based frozen core.
- **KVoiceBench / KOpenAudioBench / KMMAU** (arXiv 2605.27984) — Korean ports. English absent.
- **PolySpeech-100** (arXiv 2606.01016) — 100+ languages/dialects speech understanding. English is
  a minority slice; coupling LOW-MEDIUM. Possible future OBS-breadth asset only.
- **GlobeAudio** (arXiv 2606.08194) — multilingual/multicultural naturalistic LALM eval. Same shape.
- **Interspeech 2026 Audio Reasoning Challenge** (arXiv 2602.14224) — MMAR-Rubrics reasoning-process
  quality, agent/model tracks. Rubric scoring; MMAR lineage is mixed audio. Set aside.
- **DCASE 2026 Task: Audio-Dependent Question Answering (ADQA)** — derived from AudioMCQ (570k+),
  StrongAC split, CoT labels generated by **Gemini 3.1 Pro**. **Out of boundary** (audio-dependent
  by construction means environmental sound) and the CoT labels are proprietary-model-derived.
  Reject.
- **Full-Duplex-Bench-v3** (arXiv 2604.04847) — already-local; real human speech + multi-step tool
  use, disfluency-annotated. **Coupling is HIGH** (tool schemas), but full-duplex protocol conflicts
  with a turn-based frozen core. Worth a second look if a turn-based subset can be extracted.
- **SQuTR** (arXiv 2602.12783) — already-local; spoken-query-to-text retrieval robustness under
  acoustic noise. Retrieval is central, so coupling is genuinely MEDIUM-HIGH; already held locally.
- **SpeechRAG** (arXiv 2412.16500, ICASSP 2025) — a *method*, not a benchmark. Cite, do not acquire.
- **Attention-guided Evidence Grounding for Spoken QA** (arXiv 2603.16292) — method paper, directly
  adjacent to this program's thesis. Cite in survey; no data.

---

# Part B — meeting and long-form speech understanding

## AMI Meeting Corpus

- **Name / IDs**: AMI Meeting Corpus. Official site `https://groups.inf.ed.ac.uk/ami/corpus/`.
- **Local status**: **already-local** — 171 Mix-Headset WAVs, manual annotations v1.6.2,
  cc-by-4.0, 11.6 GB.
- **Speech subset enumeration**: speech-only, real multi-party meetings. No carve-out needed.
- **Task shape and I/O**: long-form multi-party meeting audio; supports ASR, diarization,
  summarization, extractive QA (via MeetingQA), topic segmentation, dialogue acts.
- **Size**: ~100 hours; 171 Mix-Headset recordings locally.
- **Language coverage**: English (mixed native and non-native speakers — a genuine accent stressor).
- **Speech provenance**: **real human speech**, spontaneous, multi-party, far-field and headset.
- **License**: CC BY 4.0.
- **Obtainability**: already local.
- **Eval metric**: task-dependent; WER for ASR is deterministic and pinnable. Summarization metrics
  (ROUGE) are deterministic but weak.
- **Knowledge-coupling**: **HIGH.** AMI's scenario meetings revolve around a fixed product-design
  vocabulary, a known participant roster with assigned roles, and a per-meeting agenda. Named
  fields: **participant/role roster**, **project term lexicon**, **agenda item list**. Each is a
  legitimate externally supplied artifact that is not a gold label and that plausibly changes both
  OBS (entity WER) and USE (answer grounding).
- **G1' verdict**: **ADMIT.** Passes all five. Already local, CC BY 4.0, deterministic WER, and the
  richest legitimate evidence-slot structure of any speech corpus this program holds. This is the
  natural Part B anchor.

## ICSI Meeting Corpus

- **Name / IDs**: ICSI Meeting Corpus. **Free Edinburgh distribution**
  `https://groups.inf.ed.ac.uk/ami/icsi/` and `.../icsi/download/`. LDC catalog entries exist
  separately: **LDC2004S02** (speech) and **LDC2004T04** (transcripts).
- **Local status**: **not-local**.
- **KEY FINDING — obtainability**: the corpus is **freely and ungatedly downloadable** from the
  Edinburgh AMI group under an explicit open licence. Verbatim: *"All of the signals and
  transcription, and some of the annotations, have been released publicly under the Creative Commons
  Attribution 4.0 International Licence (CC BY 4.0)."* The LDC route is **not** required. This
  corrects the common assumption that ICSI is LDC-gated.
- **Speech subset enumeration**: speech-only, real multi-party meetings. No carve-out needed.
- **Task shape and I/O**: long-form multi-party technical meeting audio; ASR, diarization, dialogue
  acts (MRDA), summarization, extractive QA.
- **Size**: **~70–72 hours of speech across ~75 meetings** (Bdb, Bed, Bmr, Bns, Bro, Bsr, Btr, Buw
  series). The LDC record counts 922 files / 883 raw channel-hours representing 72 hours of speech.
  #speakers not stated on the Edinburgh page (ICSI research-staff meetings, ~50 distinct speakers
  in the literature — not verified).
- **Language coverage**: English, with a high proportion of non-native speakers.
- **Speech provenance**: **real human speech**, spontaneous, unscripted technical discussion.
- **License**: CC BY 4.0 (verbatim above).
- **Obtainability**: **direct, ungated download.** No request form, no DUA.
- **Download size**: **~9 GB** for all headset-mix files (120 MB/meeting, single WAV) or
  **~26.25 GB** for all individual-channel SPH files (350 MB/meeting). The 9 GB mix-headset route
  mirrors exactly how AMI is already held locally.
- **Eval metric**: WER for ASR — deterministic and pinnable. Annotations include orthographic
  transcription, dialogue acts and speech-quality assessments. Summaries/topics were **not
  confirmed** on the page fetched.
- **Published omni baselines**: none retrieved for omni-class models.
- **Knowledge-coupling**: **MEDIUM-HIGH.** ICSI meetings are dense with technical jargon,
  acronyms, project codenames and researcher surnames — precisely the class of tokens where a
  supplied lexicon or participant roster measurably moves entity WER. Named fields: **speaker/
  participant roster** and **project acronym-and-jargon lexicon**. It is somewhat weaker than AMI
  because there is no scripted agenda structure.
- **G1' verdict**: **ADMIT.** Passes all five criteria. This is the strongest *new acquisition*
  in Part B: real human long-form meeting speech, genuinely free and ungated under CC BY 4.0,
  ~9 GB at the mix-headset level, deterministic WER, and it is the natural second domain for any
  entity-lexicon result currently resting on AMI alone. Acquiring it converts a single-corpus
  meeting finding into a two-corpus one at ~9 GB of cost.

## MeetingBank (+ MeetingBank_Audio)

- **Name / IDs**: MeetingBank: A Benchmark Dataset for Meeting Summarization. arXiv **2305.17529**;
  ACL 2023. Site `https://meetingbank.github.io/`. Official HF `huuuyeah/meetingbank` (text) and
  `huuuyeah/MeetingBank_Audio` (audio).
- **Local status**: **not-local**.
- **Speech subset enumeration**: speech-only — city council meeting recordings. No sound/music.
- **Task shape and I/O**: long-form meeting audio/transcript in, summary (minutes) out. Also
  supports ASR and segment-level QA.
- **Size**: text repo **6,892 rows** (train 5,170 / val 861 / test 862), 115 MB. Audio repo
  **1,366 meetings**, **2,708 audio files**, described as "over 3,579 hours of video".
  *Discrepancy*: the 3,579-hour figure is stated as video duration; the corresponding audio-only
  hours were not separately stated.
- **Language coverage**: English.
- **Speech provenance**: **real human speech** — actual municipal proceedings spanning over a
  decade, far-field and public-address conditions. Genuinely hard, genuinely real.
- **License**: **cc-by-nc-sa-4.0** on both the text and audio repos. Non-commercial **and
  share-alike** — the SA clause propagates to derivatives and is stricter than AMI/ICSI CC BY 4.0.
- **Obtainability**: ungated HF, direct, on both repos.
- **Download size**: text **115 MB**; audio **198 GB**. The audio repo is prohibitively large to
  take whole — a per-meeting subset would be mandatory.
- **Eval metric**: summarization against professionally written minutes (ROUGE-family,
  deterministic but weak); ASR WER on the audio is deterministic and pinnable. No judge required.
- **Published omni baselines**: none retrieved.
- **Knowledge-coupling**: **HIGH.** City council proceedings are the most roster-dependent speech
  this family offers: **council member names**, **agenda item numbers**, **ordinance / resolution
  identifiers**, and the published **agenda document** are all externally available, all
  non-gold, and all directly determine whether an entity is transcribed and used correctly. The
  dataset explicitly ships "agenda and other metadata" alongside transcripts — the evidence slot is
  literally distributed with the corpus.
- **G1' verdict**: **ADMIT — CONDITIONAL on taking a bounded audio subset.** Passes (1)(3)(4)(5)
  strongly and (2) in principle. The blocking practicality is the **198 GB** audio repo: a
  meeting-level subset (say 30–60 meetings, on the order of 5–10 GB) must be specified before
  acquisition. Also record the **NC-SA** licence, which is stricter than the corpora already held.
  On the knowledge-coupling axis this is the best-shaped meeting corpus found — the agenda and
  roster are shipped as first-class metadata rather than being something we would have to invent.

## QMSum

- **Name / IDs**: QMSum: A New Benchmark for Query-based Multi-domain Meeting Summarization.
  ACL Anthology **2021.naacl-main.472**; arXiv 2104.05938. Official GitHub
  `https://github.com/Yale-LILY/QMSum`.
- **Local status**: **not-local**.
- **Speech subset enumeration**: **transcript-only — no audio is distributed.** The underlying
  meetings are 137 AMI + 59 ICSI + 36 Parliament committee meetings.
- **Task shape and I/O**: query + meeting transcript in, focused summary out.
- **Size**: **1,808 query-summary pairs over 232 meetings** across three domains
  (`data/Academic`, `data/Product`, `data/Committee`, plus `data/ALL`).
- **Language coverage**: English.
- **Speech provenance**: n/a for the distributed artifact (transcripts). The *source* audio is real
  human speech and, critically, **AMI audio is already local and ICSI audio is freely obtainable**
  (see above) — so QMSum's queries can be re-attached to real audio for 196 of its 232 meetings.
- **License**: **not stated** on the pages fetched; must be read from the repository LICENSE file
  before use.
- **Obtainability**: GitHub, direct, ungated.
- **Download size**: negligible (text only, well under 100 MB).
- **Eval metric**: ROUGE against reference summaries — deterministic, **pinnable, no judge**.
- **Published omni baselines**: none (it predates omni models and is text-only).
- **Knowledge-coupling**: **MEDIUM.** The query itself is a supplied field, and relevant-span
  selection is exactly a SUPPLY decision. But the evidence (the transcript) is given in full rather
  than retrieved, so the interesting question becomes *organization* (ORG) rather than acquisition.
- **G1' verdict**: **CONDITIONAL — ADMIT as an annotation layer, not as a corpus.** Its real value
  is that it supplies **query-summary pairs that can be re-attached to already-local AMI audio and
  to freely obtainable ICSI audio**, turning held audio into a query-focused long-form task at
  near-zero acquisition cost. Passes (1 via re-attachment)(2)(3)(4)(5-medium). Blocking gap: licence
  not stated. Alone it fails (1) — text without speech is not in this repository's object.

## MeetingQA

- **Name / IDs**: MeetingQA: Extractive Question-Answering on Meeting Transcripts. ACL Anthology
  **2023.acl-long.837**. Official GitHub `https://github.com/adobe-research/meetingqa`
  (Adobe Research + UNC).
- **Local status**: **not-local**.
- **Speech subset enumeration**: **transcript-only — no audio.** Derived from **AMI** transcripts
  (repo path `Annotated-AMI-QA`, plus `ProcessedTranscripts` and `SyntheticDataset` folders).
- **Task shape and I/O**: question asked *by a meeting participant* + transcript in, extracted
  answer span(s) out. Answers may be multi-span and distributed across multiple speakers, and some
  questions are genuinely unanswered — a realistic abstention signal.
- **Size**: #questions and #meetings **not retrieved** from the official pages.
- **Language coverage**: English.
- **Speech provenance**: n/a for the artifact; **the source AMI audio is already local**, so this
  annotation layer can be re-attached to real speech directly.
- **License**: a LICENSE file exists in the repository but its terms were **not retrieved**.
- **Obtainability**: GitHub, direct, ungated.
- **Download size**: negligible (text).
- **Eval metric**: extractive QA — **F1 / exact match**. Reported model F1 **57.3** against human
  **84.6**, a 27-point gap. Deterministic, **pinnable, no judge**. Very good metric hygiene and a
  large, well-located headroom band.
- **Published omni baselines**: none — no omni-class model has been run on it.
- **Knowledge-coupling**: **MEDIUM-HIGH.** Two real slots. First, the **participant/speaker
  roster**: answers are distributed across speakers and the model must attribute correctly, so a
  supplied roster is legitimate non-gold evidence. Second, the **abstention** structure —
  unanswered questions mean a SUPPLY policy that over-supplies can be penalized, which is exactly
  the behaviour a control plane should be measured on. The transcript itself is given, so this is
  more ORG/USE than acquisition.
- **G1' verdict**: **ADMIT — as an annotation layer over already-local AMI audio.** Passes
  (1 via AMI audio)(2)(3)(4)(5). This is the highest-value zero-cost move in Part B: it converts
  the 11.6 GB of AMI audio already on disk into a deterministic, abstention-aware, extractive QA
  task with a published 27-point human gap, for the cost of a text download. Blocking gap: read the
  repository LICENSE and retrieve the item counts before committing.

## MeeQA

- **Name / IDs**: MeeQA: Natural Questions in Meeting Transcripts. arXiv **2305.08502**.
- **Local status**: **not-local**.
- **Speech subset enumeration**: **transcript-only — no audio.**
- **Task shape and I/O**: real participant-asked questions over meeting transcripts; many remain
  unanswered.
- **Size**: **48,000 question-answer pairs from 422 meeting transcripts**, multiple domains.
- **Language coverage**: English.
- **Speech provenance**: n/a. Source corpora **not specified** in the paper abstract — so, unlike
  MeetingQA and QMSum, **it cannot be reliably re-attached to audio we hold**. This is the decisive
  difference.
- **License**: Creative Commons Attribution 4.0 (CC BY 4.0).
- **Obtainability**: via the paper; a canonical repository link was not retrieved.
- **Download size**: negligible (text).
- **Eval metric**: the paper proposes a "Flat Hierarchical Loss" for unanswered-question handling;
  the *evaluation* metric was not stated on the abstract page. Presumably F1/EM, **not confirmed**.
- **Published omni baselines**: none.
- **Knowledge-coupling**: MEDIUM in principle (same roster/abstention shape as MeetingQA).
- **G1' verdict**: **REJECT.** Fails (1) — text-only with **unidentified source corpora**, so
  there is no route to attach it to in-boundary speech. Fails (4) as stated (metric unconfirmed).
  MeetingQA dominates it on every axis that matters here because MeetingQA's source is AMI, which
  we already hold.

## AutoMin 2025 (Third Automatic Minuting Challenge)

- **Name / IDs**: Findings of the Third Automatic Minuting (AutoMin) Challenge. arXiv
  **2509.13814**. Site `https://ufal.github.io/automin-2025/`. Co-located with SIGDIAL 2025.
- **Local status**: **not-local**.
- **Speech subset enumeration**: transcript-centric. **Whether audio is distributed was not
  confirmed** on the pages fetched — the challenge is framed around transcripts.
- **Task shape and I/O**: (a) minuting — transcript in, structured minutes out; (b) **new QA task**
  — question + ~1-hour meeting transcript in, answer out, in monolingual English and cross-lingual
  (Czech question over English meeting) settings.
- **Size**: item counts **not retrieved**. Meetings are ~1 hour, requiring >16k-token contexts.
  Domains: project meetings and European Parliament sessions.
- **Language coverage**: English and Czech. English is a first-class slice for both tasks.
- **Speech provenance**: real human meetings (project meetings, parliamentary sessions), but the
  distributed artifact appears to be transcripts.
- **License**: **not stated** on the pages fetched.
- **Obtainability**: challenge distribution; availability outside the shared task **not confirmed**.
- **Download size**: not retrieved.
- **Eval metric**: minuting scored by automatic **and manual** metrics; the QA task is scored by
  **LLM-as-a-judge** — the judge model was **not identified**, so it is **unpinned** and may be paid.
- **Published omni baselines**: organizers ran LLM baselines; participation was very low (one team
  on minuting, two on QA), so the comparison base is thin.
- **Knowledge-coupling**: **MEDIUM.** ~1-hour meeting QA with a supplied agenda and participant
  roster would be a real evidence slot, and the European Parliament domain has canonical external
  metadata (session agendas, MEP rosters). But the transcript is given in full, so this is ORG/USE.
- **G1' verdict**: **CONDITIONAL, blocked.** Fails (1) as currently understood — no confirmed audio
  distribution, and this repository's object is speech, not text. (4) is unresolved (unidentified
  LLM judge). (2) unconfirmed. Worth one follow-up to determine whether audio exists for the
  project-meeting portion; if it does, the ~1-hour QA task becomes interesting. Otherwise reject.

## LongSpeech (Marco-LongSpeech)

- **Name / IDs**: LongSpeech: A Scalable Benchmark for Transcription, Translation and Understanding
  in Long Speech. arXiv **2601.13539**; ICASSP 2026. Released by AIDC-AI; HF
  `ATH-MaaS/Marco_Longspeech`.
- **Local status**: **not-local**.
- **Speech subset enumeration**: speech-only — no sound/music configs. Tasks: **ASR, speech
  translation, summarization, language detection, speaker counting, content separation, question
  answering** (the abstract enumerates seven of the eight advertised tasks; emotion analysis is the
  eighth per secondary sources — *discrepancy recorded*).
- **Task shape and I/O**: ~10-minute speech segment + instruction in, text out. Adapter-mappable,
  but 10-minute segments are a serious context-length demand on a frozen core.
- **Size**: **100,000+ segments, each ~10 minutes** — implying on the order of 16,000+ hours, which
  is far beyond anything this program should ingest whole. Total hours not stated explicitly.
- **Language coverage**: not detailed in the abstract; multilingual given the translation and
  language-detection tasks. English presence assumed, not confirmed.
- **Speech provenance**: **not stated** in the abstract. Must be confirmed.
- **License**: **CC BY-NC-ND 4.0** (indicated on the arXiv listing). The **ND** clause is unusually
  restrictive for a benchmark and warrants care — derivative preprocessed forms may be constrained.
- **Obtainability**: HF `ATH-MaaS/Marco_Longspeech`; gating status not confirmed.
- **Download size**: not retrieved; at 100k × 10 minutes it is very large. A subset is mandatory.
- **Eval metric**: not specified in the abstract. ASR/translation components are deterministic
  (WER/BLEU); summarization and QA components are likely judge-dependent. **Unpinned.**
- **Published omni baselines**: "state-of-the-art models" with significant gaps; no Qwen-Omni row
  retrieved.
- **Knowledge-coupling**: **MEDIUM.** Long-form ASR over 10-minute segments is genuinely
  entity-lexicon-coupled (the same mechanism that makes earnings21/22 valuable), and the QA and
  summarization tasks admit an agenda/roster slot. But nothing in the design supplies such a field,
  so we would be constructing it.
- **G1' verdict**: **CONDITIONAL.** Passes (1)(3, with context caveats)(5-medium). Unresolved on
  (2) (scale, gating) and (4) (metric unspecified). The **CC BY-NC-ND** licence plus the sheer scale
  make this a poor near-term acquisition. Revisit only if a long-form ASR entity-coupling claim
  needs a third corpus beyond earnings21/22 and AMI/ICSI.

## BLAB (Brutally Long Audio Bench)

- **Name / IDs**: BLAB: Brutally Long Audio Bench. arXiv **2505.03054**. Official GitHub
  `https://github.com/orevaahia/brutally_long_audio_bench`; official HF `oreva/blab_long_audio`.
- **Local status**: **not-local**.
- **SPEECH SUBSET ENUMERATION** (mixed content): configs are **Word Localization**, **Named Entity
  Localization**, **Advertisement Localization**, **Speaker Number Estimation**, **Event Duration**,
  **Entire Duration**, **Emotion Reasoning**, **Emotion Ranking**.
  - *Speech-linguistic — admissible*: **Named Entity Localization** and **Word Localization** are
    genuinely linguistic; Speaker Number Estimation is speech-attribute.
  - *Excluded / boundary risk*: **Emotion Ranking** explicitly involves **non-verbal sound**, and
    the source clips are full-length YouTube audio that mixes speech with **environmental sound and
    music** (comedy specials, panel sessions). The *carrier* is not separable per item, so even the
    admissible configs arrive embedded in mixed audio. This is a boundary problem BLAB cannot
    cleanly solve.
- **Task shape and I/O**: ~51-minute audio + question in, text/timestamp out. **51-minute inputs are
  well beyond a practical frozen-core context** without chunking machinery.
- **Size**: **833+ hours**; 200 CC-licensed audio files per task; average clip 51 minutes.
- **Language coverage**: **not stated** on the dataset card.
- **Speech provenance**: real human speech from YouTube, embedded in mixed audio.
- **License**: **cc-by-4.0** on the HF card; the paper states audio was collected from permissively
  licensed sources with human-assisted filtering.
- **Obtainability**: **structurally awkward** — the HF repo is **535 MB** and ships **YouTube URLs
  plus time-aligned metadata (`event_timestamps`), not the audio itself.** Users must download 833
  hours from YouTube separately. That is a link-rot-exposed, TOS-exposed, non-reproducible
  acquisition path, and it conflicts with this program's byte-pinning discipline.
- **Download size**: 535 MB metadata; the actual audio is 833+ hours fetched from YouTube.
- **Eval metric**: not specified on the card; localization tasks use millisecond-precision
  timestamps, which would be deterministic if a scoring script is provided.
- **Published omni baselines**: not retrieved.
- **Knowledge-coupling**: **MEDIUM.** Named Entity Localization is a real entity task and a supplied
  roster would plausibly help. But localization-in-time is a different capability from
  evidence-grounded answering.
- **G1' verdict**: **REJECT.** Fails (1) — inseparably mixed speech/sound/music carriers. Fails (2)
  in the sense that matters — the bytes are not distributed, only YouTube URLs, so acquisition is
  neither reproducible nor hash-pinnable. Fails (3) — 51-minute inputs do not map to a frozen
  turn-based core without substantial chunking machinery that would itself confound the claim.
  Passes (4-probably) and (5-medium).

## AudioMarathon

- **Name / IDs**: AudioMarathon: A Comprehensive Benchmark for Long-Context Audio Understanding and
  Efficiency in Audio LLMs. arXiv **2510.07293**. Official GitHub
  `https://github.com/DabDans/AudioMarathon`; official HF `Hezep/AudioMarathon`.
- **Local status**: **not-local**.
- **SPEECH SUBSET ENUMERATION** (mixed benchmark):
  - *Speech-linguistic — ADMISSIBLE*: **ASR** (automatic speech recognition), **SCR** (speech
    content reasoning), **SER** (speech entity recognition), **QA** (multi-hop reasoning adapted
    from RACE).
  - *Speech-attribute — in boundary, low value*: **ER** (emotion recognition), **SD** (speech
    detection), **SAR** (speaker age recognition), **SGR** (speaker gender recognition).
  - *Sound / music — EXCLUDED*: **ASC** (audio scene classifier), **SED** (sound event detection),
    **MC** (music classifier).
- **Task shape and I/O**: 90–300 second audio + question in, text out. **2,250–7,500 audio tokens**
  per item — long but far more tractable than BLAB's 51 minutes, and plausibly within reach of a
  frozen omni core.
- **Size**: **6,567 instances, 392 hours total.** Per-subset item counts **not retrieved**.
- **Language coverage**: not stated; English-centric based on the source tasks.
- **Speech provenance**: real human speech for the speech subsets (RACE-derived QA implies
  synthesized or read audio for that config — **not confirmed**).
- **License**: **cc-by-nc-4.0**.
- **Obtainability**: ungated HF, direct.
- **Download size**: not retrieved; 392 hours implies roughly **20–40 GB**, and the speech-only
  subset would be a fraction. **Not verified.**
- **Eval metric**: task-dependent — ASR is WER (deterministic); SCR/SER/QA appear to be
  choice/extraction based, hence deterministic. No evidence of a paid judge requirement, but this
  was **not positively confirmed**.
- **Published omni baselines**: not retrieved.
- **Knowledge-coupling**: **MEDIUM-HIGH for `SER` specifically.** Speech entity recognition over
  90–300 second spans is precisely the regime where a supplied entity roster changes the outcome,
  and it sits at a duration between the short-clip benchmarks and unusable hour-scale ones. Named
  field: **entity roster / lexicon**. SCR and QA are MEDIUM (multi-hop over a long span, where ORG
  matters). The attribute tasks are LOW.
- **G1' verdict**: **CONDITIONAL — ADMIT scoped to `ASR` + `SER` + `SCR` + `QA`.** Passes
  (1-scoped)(2)(3)(5). (4) is probable but unconfirmed — verify the scoring scripts are judge-free
  before committing. **REJECT `ASC`, `SED`, `MC`** as out of boundary. Record the **NC** licence.
  This is the best-shaped long-context *speech* candidate found, because its 90–300s window is the
  only long-form regime in Part B that a frozen turn-based core can plausibly consume whole.

## ChronosAudio

- **Name / IDs**: ChronosAudio: A Comprehensive Long-Audio Benchmark for Evaluating Audio-Large
  Language Models. arXiv **2601.04876**.
- **Local status**: **not-local**.
- **Speech subset enumeration**: **not retrieved** — the abstract does not state whether the corpus
  is speech-only or mixed. Given the "long-audio" framing and the six task categories, a mixed
  composition must be assumed until proven otherwise. **Cannot be admitted without this.**
- **Task shape and I/O**: six task categories stratified by length (short / middle / long-form),
  spanning 3–10 minutes.
- **Size**: **36,000 test instances, over 200 hours** of audio.
- **Language coverage**: not disclosed.
- **Speech provenance**: not disclosed.
- **License**: the *paper* is CC BY 4.0; the **dataset licence is not stated**.
- **Obtainability**: **no repository link found** — neither GitHub nor HuggingFace was given on the
  arXiv page. Effectively unobtainable as of 2026-08-17.
- **Download size**: not retrieved.
- **Eval metric**: not specified.
- **Published omni baselines**: not retrieved. Headline findings: up to **90% degradation** from
  short to long contexts; attention mechanisms fail to maintain temporal information; mitigation
  strategies recover only ~50%.
- **Knowledge-coupling**: **not assessable** without the task breakdown.
- **G1' verdict**: **REJECT (unresolvable).** Fails (2) — no release link. Fails (1) — boundary
  cannot be verified. Its finding that long-context degradation reaches 90% is worth citing as
  motivation for chunked OBS strategies; the data is not acquirable.

## VoiceGiraffe

- **Name / IDs**: VoiceGiraffe: A Benchmark for Extreme Long-Context Audio-Language Understanding.
  arXiv **2605.27976**. GitHub referenced as "VoiceGiraffe" project page.
- **Local status**: **not-local**.
- **Speech subset enumeration**: **not retrieved.** The abstract references "diverse real-world
  scenarios, modalities, and languages" without a speech/sound/music breakdown. Boundary
  unverifiable.
- **Task shape and I/O**: dual-level taxonomy — **single-hop perception** and **multi-hop
  reasoning** over extreme-long-context audio.
- **Size**: **1,500 curated triplets.** Hours not stated.
- **Language coverage**: multilingual, specific languages not stated.
- **Speech provenance**: not stated.
- **License**: the paper carries CC0; the dataset licence was **not stated**.
- **Obtainability**: GitHub project page referenced but no verified link retrieved.
- **Download size**: not retrieved.
- **Eval metric**: not described; whether a paid judge is required is **not stated**.
- **Published omni baselines**: open-source and proprietary LALMs versus human performance;
  no specific model rows retrieved.
- **Knowledge-coupling**: **not assessable.** The reported finding — that LALMs handle salient
  causal cues better than sustained tracking of sparse events across long audio — is a
  *retrieval-over-long-audio* weakness, which is conceptually adjacent to what an OBS/SUPPLY policy
  would address.
- **G1' verdict**: **CONDITIONAL, blocked on information.** Too little is verifiable to pass (1),
  (2) or (4). The "sparse events across long audio" finding is worth one follow-up if a long-form
  OBS claim is ever pursued; otherwise deprioritize.

## LiveLongBench

- **Name / IDs**: LiveLongBench: Tackling Long-Context Understanding for Spoken Texts from Live
  Streams. ACL Anthology **2026.findings-acl.1485**; OpenReview `TyIpcbiCi5`. Official GitHub
  `https://github.com/Yarayx/livelongbench`.
- **Local status**: **not-local**.
- **Speech subset enumeration**: speech-derived *text* from live streams. The distributed artifact
  is spoken **transcripts**, not audio — so the speech signal itself is absent.
- **Task shape and I/O**: three task families — **retrieval-dependent**, **reasoning-dependent**,
  and **hybrid** — over redundancy-rich, unevenly informative spoken long text.
- **Size**: not retrieved.
- **Language coverage**: not confirmed; the live-stream domain and the `163.com` contact address
  strongly suggest a Chinese-language corpus. **Not verified**, but English being a first-class
  slice is doubtful.
- **Speech provenance**: real human live-stream speech, transcribed.
- **License**: not stated.
- **Obtainability**: **REQUEST FORM — gated.** Access requires sending a signed form to
  `livelongbench@163.com` and awaiting review and approval.
- **Download size**: not retrieved.
- **Eval metric**: not retrieved.
- **Knowledge-coupling**: **MEDIUM in principle** — the explicit "retrieval-dependent" task family
  is exactly the shape of a SUPPLY axis, and the redundancy-rich input makes ORG matter. That is
  the one genuinely attractive property here.
- **G1' verdict**: **REJECT.** Fails (2) — signed-form request gating, which this program treats as
  a blocking obtainability class alongside DUA/application corpora. Fails (1) — transcripts, not
  speech. Likely fails the English requirement. Note the **retrieval-dependent / reasoning-dependent
  / hybrid** task taxonomy as a *design* worth borrowing when constructing our own splits.

---

## Family summary

| Candidate | Local? | Speech subset only? | Real speech? | Size | License | Obtainable | Paid judge? | Knowledge-coupling | Verdict |
|---|---|---|---|---|---|---|---|---|---|
| **Part A** | | | | | | | | | |
| VoiceBench | already-local | n/a (speech-only) | mixed (7 TTS / 4 human) | 11.2 GB local | Apache-2.0 | already-local | yes, 5 of 11 configs (GPT-4o) | LOW | CONDITIONAL (deterministic configs only; regression guard) |
| AudioBench | not-local | **YES — speech configs only; exclude wavcaps/audiocaps/clotho_aqa/muchomusic/mmau_mini** | real (ASR/QA); TTS for dream/alpaca/openhermes | ~3–6 GB est. for target slice | not stated (per-component) | ungated HF | **no — Llama-3-70B local judge sanctioned** | **HIGH** (`spoken_squad_test`, `slue_p2_sqa5_test`) | **ADMIT** (scoped to spoken_squad + slue_p2_sqa5) |
| AIR-Bench | already-local | **YES — 9 speech foundation tasks + speech chat; exclude 4 sound, 6 music, all mixed-audio** | real (LibriSpeech/CV/MELD/IEMOCAP/SLURP/VoxCeleb1); FoR synthetic by design | 43.8 GB local (full) | Apache-2.0 (verbatim) | already-local | yes for chat track (gpt-4-0125-preview) | MEDIUM (`speech entity recognition`, `intent classification`) | CONDITIONAL (foundation speech only; reject chat track) |
| OpenAudioBench | not-local | n/a (speech-only) | not stated (likely TTS) | 0.67 GB | not stated | ungated HF | unresolved (2 "Score" components) | MEDIUM | CONDITIONAL (cheap; resolve licence + provenance first) |
| VoxEval | not-local | n/a (speech-only) | **TTS only** (6 voices) | **88.1 GB** | CC BY 4.0 (verbatim) | ungated HF | no (Whisper large-v3 pipeline) | LOW | REJECT on (5); S2S protocol mismatch |
| MMSU | already-local | n/a (speech-only) | not stated | 1.66 GB local | mit | already-local | no | LOW | REJECT as claim surface; keep as probe |
| MMAU | already-local | **YES — speech third only; sound third is AudioSet = hard-blocked; music excluded** | real (MUSTARD) for speech third | ~0.4 GB of 1.21 GB test-mini | **conflict: Apache-2.0 (GitHub) vs cc-by-nc-4.0 (HF)** | test-mini direct; full test answers withheld | no (test-mini) | LOW | REJECT as claim surface; filter loader to speech third |
| Dynamic-SUPERB (+Phase-2) | not-local | **required but NOT YET DONE — 180 tasks span speech/music/environmental** | mixed, per-task | not retrieved | not stated | ungated HF (180 repos) | not confirmed | MEDIUM at best, diluted | CONDITIONAL, blocked on enumeration → deprioritize |
| URO-Bench | already-local | n/a (speech-only) | mixed | 12.1 GB local | mit | already-local | **yes (GPT-based)** | LOW | REJECT on (4)+(5) |
| ADU-Bench | not-local | n/a (speech-only) | mixed (>8,000 real) | 2.21 GB as hosted (**size conflict vs 20,715 dialogues**) | not stated | ungated HF | likely (unconfirmed) | LOW | REJECT on (5) |
| **Audio2Tool** | **already-local (corrected)** | n/a (speech-only) | **TTS only** (Qwen3TTS, CosyVoice-3) | **10.47 GB on disk** | `cc-by-nc-4.0` per HF+lock (paper badge says CC BY 4.0 — conflict) | **already held, ungated HF `RVtech/Audio2Tool`** | **no** (exact match / slot F1) | **HIGH** (tool schema) | **ADMIT** — L5 anchor, loader+scorer already built |
| **AudioCRAG** (Stream RAG) | not-local | n/a (speech-only) | **split: 1,862 TTS + 618 real human** | not released | not stated | **BLOCKED — human half unreleased** | **no** (Llama-4-Maverick, open weights) | **HIGH** (web snippets + KG records) | CONDITIONAL — ADMIT on release; CRAG-text fallback exists |
| AudioRAG | not-local | **NO — FMA/MusicNet/iNaturalist = music + environmental** | mostly non-speech | small (500 items) | CC BY 4.0 | GitHub | **yes (GPT-4o) + paid Google Search** | HIGH but out-of-boundary | **REJECT** on (1)(2)(4) |
| **SpokenWOZ** | not-local | n/a (speech-only) | **real human-to-human, 249 h** | ~10–25 GB est. (unverified) | CC BY-NC 4.0 | **free, ungated HF** | **no** (JGA / INFORM / SUCCESS / BLEU) | **HIGH** (entity DB + slot ontology) | **ADMIT** — best obtainable Part A carrier |
| tau-Voice | not-local | n/a (speech-only) | **TTS only** (ElevenLabs v3) | not retrieved | CC BY 4.0 | **PAID** (OpenAI/Gemini/Grok realtime) | no judge, but paid APIs | HIGH | **REJECT** on (2)(3) |
| VCB Bench | not-local | n/a (speech-only) | **all real human** | not retrieved | not stated | GitHub | **yes (GPT-4o + Gemini-2.5-Pro)** | LOW-MEDIUM | REJECT on (4)(5); English is minority slice |
| Audio MultiChallenge | already-local | n/a (audio-cue items graze boundary) | **real, unscripted, 47 speakers** | local | MIT | already-local | rubric judge, unidentified | LOW (memory axis, out of study object) | REJECT on (5) + knowledge-not-memory boundary |
| **Part B** | | | | | | | | | |
| **AMI** | already-local | n/a (speech-only) | **real multi-party** | 11.6 GB local | CC BY 4.0 | already-local | no (WER) | **HIGH** (roster, term lexicon, agenda) | **ADMIT** — Part B anchor |
| **ICSI** | not-local | n/a (speech-only) | **real multi-party, ~70–72 h, ~75 meetings** | **~9 GB** (mix-headset) / 26.25 GB (channels) | **CC BY 4.0 (verbatim)** | **direct, ungated — NOT LDC-gated** | no (WER) | **MEDIUM-HIGH** (roster, acronym/jargon lexicon) | **ADMIT** — strongest new acquisition |
| **MeetingBank** (+Audio) | not-local | n/a (speech-only) | **real municipal proceedings** | text 115 MB; **audio 198 GB** → subset required | **cc-by-nc-sa-4.0** | ungated HF | no | **HIGH** (agenda + council roster shipped as metadata) | **ADMIT — CONDITIONAL** on a bounded audio subset |
| QMSum | not-local | transcript-only | source is AMI(137)+ICSI(59)+Parliament(36) | <100 MB | not stated | GitHub, direct | no (ROUGE) | MEDIUM | CONDITIONAL — admit as annotation layer over held AMI/ICSI audio |
| **MeetingQA** | not-local | transcript-only (**source = AMI, already local**) | re-attachable to real AMI audio | negligible | not retrieved (LICENSE exists) | GitHub, direct | **no** (F1/EM; 57.3 vs human 84.6) | **MEDIUM-HIGH** (speaker roster + abstention) | **ADMIT** — best zero-cost move in Part B |
| MeeQA | not-local | transcript-only, **source corpora unidentified** | cannot re-attach | negligible | CC BY 4.0 | via paper | not confirmed | MEDIUM in principle | **REJECT** — no route to speech |
| AutoMin 2025 | not-local | transcript-centric; audio **not confirmed** | real meetings, artifact is text | not retrieved | not stated | shared-task distribution | **yes — unidentified LLM judge** | MEDIUM | CONDITIONAL, blocked — verify audio existence |
| LongSpeech (Marco) | not-local | n/a (speech-only) | not stated | 100k × ~10 min → very large | **CC BY-NC-ND 4.0** | HF, gating unconfirmed | metric unspecified | MEDIUM | CONDITIONAL — poor near-term trade (ND + scale) |
| BLAB | not-local | **NO — mixed YouTube carriers; Emotion Ranking uses non-verbal sound** | real, but embedded in mixed audio | 535 MB metadata + 833 h from YouTube | cc-by-4.0 | **URLs only — not byte-pinnable** | not specified | MEDIUM | **REJECT** on (1)(2)(3) |
| **AudioMarathon** | not-local | **YES — ASR/SCR/SER/QA admissible; exclude ASC, SED, MC** | real (RACE-derived QA unconfirmed) | ~20–40 GB est. full; speech slice a fraction | cc-by-nc-4.0 | ungated HF | probable no (unconfirmed) | **MEDIUM-HIGH** (`SER` entity roster, 90–300 s) | **CONDITIONAL — ADMIT** scoped to ASR/SER/SCR/QA |
| ChronosAudio | not-local | **unverifiable** | not stated | 36k items / 200 h | dataset licence not stated | **no release link** | not specified | not assessable | **REJECT (unresolvable)** |
| VoiceGiraffe | not-local | **unverifiable** | not stated | 1,500 triplets | not stated (paper CC0) | link not verified | not stated | not assessable | CONDITIONAL, blocked on information |
| LiveLongBench | not-local | transcript-only | real live-stream speech, transcribed | not retrieved | not stated | **signed request form** | not retrieved | MEDIUM in principle | **REJECT** on (2)(1); likely non-English |
