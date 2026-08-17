# Task/dataset expansion scan for the SLU → SQA → agentic capability ladder

Date: 2026-08-17. Campaign: `2026-08-17-task-dataset-expansion`.
Prepared for: `studies/speech-aware-evidence-acquisition` (frozen Qwen3-Omni-30B-A3B, API-shaped
boundary, zero training, prompt-level supply only).
Status: **workbench material, not a registry receipt and not an acquisition authorization.** Nothing
was downloaded. Acquisition happens only through the umbrella lock-registration flow
(`docs/datasets.lock.json` + `scripts/data/`).

## 1. Why this scan exists

The 2026-08-17 owner GO pivoted the study from an ASR-anchored claim surface to a **capability
ladder**. `docs/superpowers/specs/2026-08-17-saea-standard-scheme-v1.md` §3 freezes it as:

| Level | Task family | Carriers named in the spec | Supply-leverage expectation |
|---|---|---|---|
| L1 | ASR / entity transcription | earnings21/22 (calibration substrate only) | ~0 (measured copy trap; zero anchor) |
| L2 | Context-conditioned entity ASR | contextasr-bench | transitional |
| L3 | SLU (slots/intent) | SLURP | medium |
| L4 | Spoken QA / meeting understanding | slue-sqa-5, librisqa, AMI | high |
| L5 | Agentic speech (tool use) | Audio2Tool (+ survey candidates) | measured headroom: tool-acc 84.6% vs EM 15.6% |

The primary claim surface is the **supply-benefit-versus-task-level curve**. That makes L3–L5 the
load-bearing rungs, and it makes *knowledge-coupling* — whether a task even has a slot where
externally supplied evidence can change the outcome — the ranking axis for any new carrier. This
scan asks, per family: what exists, is it obtainable at zero cost, and does it couple to supply?

## 2. Method, coverage and hygiene

- WebSearch + WebFetch only. **Nothing was downloaded**; no `git clone`, no `hf download`.
- Four parallel family scouts, each required to verify identity against the official paper/page
  (arXiv ID, ACL Anthology, official GitHub or HF org) rather than a single aggregator, and to
  record discrepancies rather than resolve them by guess.
- Per-fetch log in `fetch-log.md` (**224 logged rows**); every claim in the family notes traces to a
  row. Family detail: `notes-spoken-qa.md`, `notes-agentic.md`,
  `notes-voice-assistant-and-meeting.md`.
- Licence text quoted verbatim where short; "not stated" means the card is silent, not that the
  value is unknown to the world. Paid access is an automatic exclusion — program spend stays 0.

### Coverage note — PARTIAL

Three of four families completed: **spoken QA (17 candidates)**, **agentic/tool-use (24)**, and
**voice-assistant eval + meeting/long-form (32)**. Roughly 68 distinct candidates carry a verdict.

The **SLU / spoken-semantic-parsing family scout was descoped mid-campaign and did not deliver**.
This is a deliberate, bounded gap rather than an omission:

- **SLURP is RESOLVED-LOCAL, not surveyed.** While this scan ran, SLURP's label side was acquired
  and reconciled locally at 100.00%, the lock was updated, and a `SlurpAdapter` was implemented. L3's
  named carrier is settled and needs no survey verdict.
- The highest-value *new* SLU-shaped candidates were caught anyway by the other scouts —
  **SpokenWOZ** (real human-to-human task-oriented dialogue with an entity DB and slot ontology) and
  **Speech-MASSIVE** (already local) both carry full verdicts below.
- Still **UNSURVEYED, and the honest residue of this campaign**: STOP (spoken task-oriented
  parsing), SLUE Phase-1, the SLUE Phase-2 non-SQA tasks (HVB dialog acts, HVAC, VoxCeleb NEL, TED
  summarization), and MSNER. These are the first targets for any follow-up scan.
- If `notes-slu.md` / `fetchlog-slu.md` appear later, they are a late artifact from the stopped
  scout and should be reviewed and committed separately, not assumed to be part of this deliverable.

### G1' admission criteria

ADMIT requires all five: (1) **in-boundary** — human speech and its linguistic content; general
audio/music out (FSD50K, AudioSet, ESC-50, Clotho, AudioCaps), mixed benchmarks admissible only via
explicitly named speech subsets; (2) **obtainable at zero cost** — paid is auto-excluded,
gated/request-form is CONDITIONAL at best; (3) **adapter-mappable** — a frozen, turn-based, API-only
core drops in with no training and no second answering LLM; (4) **pinnable metric** — deterministic
scoring the study can freeze, so a paid-judge-only metric fails; (5) **non-trivial
knowledge-coupling** — a concrete field where supplied evidence could change the outcome.

## 3. Baseline: what the program already holds

Marked against `docs/datasets.lock.json` (schema `speechrl-asset-lock-v2`). This matters because a
large fraction of the owner's candidate list is **already on disk** — the expansion problem is mostly
one of *activation*, not acquisition.

| Ladder level | Already local and COMPLETE | Not local |
|---|---|---|
| L1 | earnings21/22-original, conec, halas, ted-el-annotations, prism-public, rare5k-reconstruction, buzzword, librispeech, atco2-test-1h, eka-medical-asr-eval | — |
| L2 | contextasr-bench, slideasr-bench | ProfASR-Bench |
| L3 | **slurp** (RESOLVED-LOCAL: labels reconciled 100.00%, adapter built), speech-massive (32.5 GB, NC), minds14 | **SpokenWOZ**, STOP, SLUE Phase-1, SLUE Phase-2 non-SQA, MSNER |
| L4 | slue-sqa-5 (118 GB, all splits), spoken-squad (mirror 3.4 GB), squad-v11-dev, heysquad (14.6 GB), librisqa-metadata (171 MB), ami-meeting-corpus (11.6 GB), mmsu, big-bench-audio, squtr | **ICSI, MeetingQA, SpokenNativQA, SD-QA**, NMSQA, MeetingBank, QMSum |
| L5 | **audio2tool** (10.47 GB; loader+scorer already built), voiceagentbench (5.83 GB), eva-bench (263 KB), tau2-bench (text, 26 MB), ihbench, full-duplex-bench-v3, soulx-duplug, omni-deepsearch | **WearVox**, ToolVoice, τ-Voice, VAmoS, DuplexWorld, ProVoice-Bench |
| eval suites | voicebench (11.2 GB), air-bench (43.8 GB), uro-bench (12.1 GB), mmau-mini, mmar, vocalbench(+zh), voiceassistant-eval, audiomc, unisrm-bench | AudioBench, VoxEval, OpenAudioBench, Dynamic-SUPERB v2, ADU-Bench, AudioMarathon |

**Blocked in the lock, do not re-propose:** `voxpopuli` (owner-excluded >1 TB), `spgispeech` (Kensho
terms), `common-voice-22` (Mozilla DC terms), `ted-lium3` (OpenSLR 404), `mlc-slm` (DUA),
`msp-podcast` (application), `m3ed` (Baidu Pan), `indicvoices`, `grga-longaudioqa` (never released).
**Retained but out of boundary:** fsd50k, audioset-metadata-features, esc-50 — never to enter a
loader, test or config in this study.

### Two discrepancies against today's frozen spec

1. **L3 "SLURP (acquisition pending)" is stale.** SLURP is COMPLETE, re-verified in place
   (72,395 real FLAC recordings reconciling one-for-one against the official jsonl indexes, with
   per-utterance entity/slot spans and per-recording `wer`/`ent_wer`), and since this scan began its
   label side was reconciled at 100.00% with an adapter built. **L3 is ready to run today.**
2. **L4 names `librisqa` as a carrier, but LibriSQA scores LOW coupling and is REJECTED.** Its QA
   pairs were explicitly generated to be answerable without external knowledge, which removes the
   very slot this study's mechanism acts on. It should be replaced in the spec's L4 row by AMI
   (already local, HIGH coupling via roster/lexicon/agenda) plus ICSI or MeetingQA.

## 4. Consolidated survey table

Verdicts are G1'. "Coupling" is the knowledge-coupling rating. Sizes are the slice we would actually
consume. `UNVERIFIED` marks a value the scouts could not confirm from an official source.

### L3/L4 — SLU and spoken QA

| Candidate | Local? | Real speech? | Size | Licence | Obtainable | Gold layers | Coupling | Verdict |
|---|---|---|---|---|---|---|---|---|
| SLURP | **RESOLVED-LOCAL** | Yes | 12.6 GB | text CC BY 4.0 / audio NC | held | intent, slot spans, `ent_wer` | HIGH | **ADMIT** (settled) |
| SLUE-SQA-5 | already-local | Yes (both sides) | 118 GB | Apache-2.0 + CC BY-SA 4.0 | held | `raw_document_text`, answer spans, `word2time` | HIGH | **ADMIT** |
| HeySQuAD (human) | already-local | Yes (questions) | 14.6 GB | CC-BY-4.0 | held | `context` passage | HIGH | **ADMIT** |
| Speech-MASSIVE | already-local | Yes | 32.5 GB | cc-by-nc-sa-4.0 | held | intent + slots, 12 langs | HIGH | **ADMIT** (NC flag) |
| **SpokenWOZ** | not-local | **Yes, human-to-human 249 h** | ~10–25 GB `UNVERIFIED` | CC BY-NC 4.0 | ungated HF | dialogue state, entity DB, slot ontology | **HIGH** | **ADMIT** |
| **SpokenNativQA** | not-local | Yes | 364 MB | CC BY-NC-SA 4.0 | ungated HF | open-domain answers; **no passage** | **HIGH** | **ADMIT** (EN subset) |
| **SD-QA** | not-local | Yes (dialect speakers) | `UNVERIFIED`; ~1k EN questions | Apache-2.0 | Google Drive, ungated | answers × ~10–11 EN dialects | HIGH | **ADMIT** (EN subset) |
| NSF-QA | not-local | Yes (real meetings) | 305 GB | CC BY-NC 4.0 | ungated HF | entity-type QA over far-field meetings | HIGH | CONDITIONAL — fails (4) judge, size |
| NMSQA | not-local | No (TTS) | `UNVERIFIED` | not stated | ungated HF | SQuAD `context` | MED-HIGH | CONDITIONAL — licence, 171-row test |
| Spoken-SQuAD (mirror) | already-local | No (TTS) | 3.4 GB | CC-BY-SA-4.0 | held | `context` (contains answer) | MEDIUM | CONDITIONAL — leakage hazard |
| VoxEval | not-local | No (TTS ×6) | 88.1 GB | CC BY 4.0 | ungated HF | closed-book MMLU answers | LOW | REJECT (5); MMLU contamination risk |
| LibriSQA | already-local (metadata) | Yes | 171 MB + LibriSpeech | CC BY 4.0 | held | QA pairs | **LOW** | **REJECT (5)** — no-external-knowledge by design |
| ODSQA / ViSQA | not-local | mixed | — | not stated | direct | — | MEDIUM | REJECT — non-English |
| LA-RAG / CASTELLA-QA | not-local | **environmental audio** | — | CC BY 4.0 | — | — | n/a | **REJECT (1)** — out of boundary |

### L4 — meeting and long-form understanding

| Candidate | Local? | Real speech? | Size | Licence | Obtainable | Gold layers | Coupling | Verdict |
|---|---|---|---|---|---|---|---|---|
| **AMI** | already-local | Yes, multi-party | 11.6 GB | CC BY 4.0 | held | transcripts, roster, annotations v1.6.2 | **HIGH** | **ADMIT** — Part B anchor |
| **ICSI** | not-local | Yes, ~70–72 h / ~75 meetings | **~9 GB** mix-headset | **CC BY 4.0 (verbatim)** | **direct, ungated — NOT LDC-gated** | transcripts, roster, jargon lexicon | MED-HIGH | **ADMIT** |
| **MeetingQA** | not-local | re-attachable to held AMI audio | negligible | `UNVERIFIED` (LICENSE exists) | GitHub direct | extractive QA, F1/EM (57.3 vs human 84.6) | MED-HIGH | **ADMIT** |
| MeetingBank | not-local | Yes, municipal | text 115 MB; **audio 198 GB** | cc-by-nc-sa-4.0 | ungated HF | **agenda + council roster as metadata** | HIGH | CONDITIONAL — bounded audio subset only |
| QMSum | not-local | source = AMI(137)+ICSI(59) | <100 MB | not stated | GitHub direct | query-based summaries, ROUGE | MEDIUM | CONDITIONAL — annotation layer |
| AudioMarathon | not-local | Yes (RACE-derived QA `UNVERIFIED`) | ~20–40 GB full; speech slice a fraction | cc-by-nc-4.0 | ungated HF | **speech subset: ASR/SER/SCR/QA; exclude ASC/SED/MC** | MED-HIGH | CONDITIONAL — ADMIT scoped |
| MeeQA | not-local | source corpora unidentified | negligible | CC BY 4.0 | via paper | transcript QA | MEDIUM | REJECT — no route to speech |
| AutoMin 2025 | not-local | audio existence unconfirmed | `UNVERIFIED` | not stated | shared task | minutes/QA | MEDIUM | CONDITIONAL — blocked on verification |
| LongSpeech (Marco) | not-local | not stated | very large | **CC BY-NC-ND 4.0** | HF 401 | — | MEDIUM | REJECT — ND blocks derived artifacts |
| BLAB | not-local | **mixed YouTube carriers** | 535 MB meta + 833 h via URLs | cc-by-4.0 | **URLs only, not byte-pinnable** | — | MEDIUM | **REJECT (1)(2)(3)** |
| LiveLongBench | not-local | transcript-only | `UNVERIFIED` | not stated | **signed request form** | — | MEDIUM | REJECT (2) |

### L5 — agentic / tool-use speech

| Candidate | Local? | Data released? | Level | Real speech? | Size | Licence | Duplex? | Coupling | Verdict |
|---|---|---|---|---|---|---|---|---|---|
| **Audio2Tool** | **already-local** | Yes (public subset) | A | No (voice-cloned TTS) | 10.47 GB; 16,843 q / 59.6 h | `cc-by-nc-4.0` (HF+lock) vs CC BY 4.0 (paper badge) — **conflict** | No | **HIGH** — tool registry + arg slots | **ADMIT** — L5 anchor |
| **WearVox** | not-local | **Yes, ungated HF `zlinao/WearVox`** | A (AST) | **Yes — real human, AI-glasses, multichannel** | **59.4 GB**; 1,125 tool-calling | CC BY-NC-SA 4.0 (paper) vs cc-by-nc-4.0 (HF) — **conflict** | No | **HIGH** — 8-tool registry + CRAG evidence join + multichannel OBS lever | **ADMIT** |
| ToolVoice (From Text to Voice) | not-local | audio-vs-script `UNVERIFIED` | A | No (Gemini/GPT TTS) | 613 × 5 noise conds | CC BY 4.0 | No | HIGH — schema + abstention | CONDITIONAL (2) — **benchmarks our exact core** |
| Full-Duplex-Bench-v3 | already-local | Yes (Google Drive, no hash) | A+E | **Yes — real, disfluent, 12 spk** | 100 scenarios | CC BY-SA 4.0 | cascaded baseline published | HIGH — tool set + Argument Accuracy | CONDITIONAL (2) — pinnability |
| VoiceAgentBench | already-local | Yes | A | No (TTS) | 5.83 GB | Krutrim Community License v1.0 | No | HIGH — tool list + params | CONDITIONAL (4) + licence review |
| tau2-bench (text) | already-local | Yes | E | n/a (text) | 26 MB | MIT | No | HIGH — policy doc + DB | CONDITIONAL (1) — no speech |
| EVA-Bench | already-local | **50 of 213 scenarios, no audio** | E | No (bot-to-bot) | 263 KB | MIT | No | HIGH — scenario DB | CONDITIONAL (2)(4) — harness needs 5 paid services |
| IHBench | already-local | Yes | A | No (TTS) | 45 convs | cc-by-4.0 | No | MEDIUM | CONDITIONAL (4)(5) |
| aiewf-eval | not-local | Yes (code + audio) | A | `UNVERIFIED` | 30 turns × 2 KB sizes | **MIT** | No (local CLI) | **HIGH — `kb_grounding` is a scored dimension** | CONDITIONAL (4) — too small to headline |
| Stream RAG / AudioCRAG | not-local | **Not released** (promised) | A | **Yes, 618 human** + 1,862 TTS | 2,480 q | not stated | No | **HIGH — retrieved evidence** | **REJECT (blocked)** — best author-contact target |
| τ-Voice | not-local | Code only | E | No (bot-to-bot) | 278 tasks | MIT (code) | **YES** | HIGH | REJECT (2)(3) — paid realtime APIs |
| VAmoS | not-local | Code only; scenarios proprietary | E | No | 100 scenarios | MIT (code) | **YES** | HIGH but unreachable | REJECT (2)(3) |
| DuplexWorld | not-local | None found (6 days old) | E | `UNVERIFIED` | 156 scenarios / 350+ h | `UNVERIFIED` | Likely YES | not assessable | REJECT — **best re-scout target** |
| BFCL v4 | not-local | Yes (text) | A | **n/a — NO AUDIO TIER** | text only | Apache-2.0 | No | HIGH (text) | **REJECT (1)** |
| BFCL Audio | not-local | **No public artifact** | A | No | `UNVERIFIED` | `UNVERIFIED` | No | HIGH — entity dictation | REJECT (blocked) |
| arcada-labs/audio-agent-bench-suite | not-local | **Card exists, bytes empty** | A | Yes (2 voice actors) | ~221 turns | CC BY 4.0 | No | HIGH — kb grounding | REJECT (blocked) |
| ProVoice-Bench / FOCAL / EchoChain / DuplexSLA-Bench | not-local | **Not released** | A/E | mostly TTS | — | mostly not stated | mixed | LOW-MED | REJECT (2) |
| AURA | not-local | System, not a dataset | E | n/a | — | CC BY 4.0 (paper) | No | LOW | REJECT (4)(5) |

### Eval suites — admissible only via named speech subsets

| Candidate | Local? | Speech subset rule | Paid judge? | Coupling | Verdict |
|---|---|---|---|---|---|
| **AudioBench** | not-local | **speech configs only; exclude `wavcaps`, `audiocaps`, `clotho_aqa`, `muchomusic`, `mmau_mini`** | **No — local Llama-3-70B judge sanctioned** | **HIGH** (`spoken_squad_test`, `slue_p2_sqa5_test`) | **ADMIT** scoped |
| AIR-Bench | already-local | **9 speech foundation tasks; exclude 4 sound, 6 music, all mixed-audio, and the GPT-4-judged chat track** | yes (chat track only) | MEDIUM (`speech entity recognition`, `intent classification`) | CONDITIONAL — foundation speech only |
| MMAU | already-local | **speech third only — the sound third is AudioSet-derived and HARD-BLOCKED** | no (test-mini) | LOW | REJECT as claim surface; filter loader |
| AudioMarathon | not-local | **ASR/SER/SCR/QA only; exclude ASC/SED/MC** | probable no `UNVERIFIED` | MED-HIGH | CONDITIONAL — ADMIT scoped |
| Dynamic-SUPERB (+Phase-2) | not-local | **NOT YET ENUMERATED — 180 tasks span speech/music/environmental** | `UNVERIFIED` | MEDIUM, diluted | CONDITIONAL — **inadmissible until classified** |
| VoiceBench | already-local | speech-only | yes, 5 of 11 configs (GPT-4o) | LOW | CONDITIONAL — deterministic configs as regression guard |
| URO-Bench | already-local | speech-only | **yes (GPT-based)** | LOW | REJECT (4)(5) |
| MMSU | already-local | speech-only | no | LOW | REJECT as claim surface; keep as probe |
| OpenAudioBench | not-local | speech-only | `UNVERIFIED` | MEDIUM | CONDITIONAL — 0.67 GB, resolve licence first |
| ADU-Bench | not-local | speech-only | likely `UNVERIFIED` | LOW | REJECT (5); **size conflict** 2.21 GB / 210 rows vs 20,715 dialogues claimed |
| AudioRAG | not-local | **NO — FMA/MusicNet/iNaturalist** | yes + paid search | HIGH but out-of-boundary | **REJECT (1)(2)(4)** |
| Audio MultiChallenge | already-local | audio-cue items graze boundary | rubric judge | LOW (memory axis) | REJECT (5) + knowledge-not-memory boundary |

## 5. Ranked top-10 acquisition shortlist

Only **not-local** candidates appear here. Total for items 1–10 is roughly **100–160 GB**, dominated
by WearVox; items 1, 5, 7 and 10 together are under 1 GB.

| # | Candidate | Rough size | Why it earns the slot |
|---|---|---|---|
| 1 | **MeetingQA** | <50 MB | Best value-per-byte in the entire scan: a negligible text download converts the 11.6 GB of AMI audio we already hold into deterministic extractive QA (F1 57.3 vs human 84.6), with speaker-roster and abstention slots. |
| 2 | **SpokenWOZ** | ~10–25 GB `UNVERIFIED` | The only large **real human-to-human** task-oriented dialogue corpus available free and ungated; entity DB + slot ontology are genuine evidence slots, metrics (JGA/INFORM/SUCCESS/BLEU) are fully deterministic, and it exercises OBS/ORG/SUPPLY/USE together. Fills the real-dialogue gap SLURP cannot. |
| 3 | **WearVox** | 59.4 GB | The only **real-human-speech** agentic tool-calling corpus that exists; judge-free AST metric, 8-tool registry, a CRAG evidence join, and multichannel audio giving an OBS lever. It is the real-speech companion Audio2Tool structurally lacks. |
| 4 | **ICSI** | ~9 GB | CC BY 4.0 and **not LDC-gated** (contrary to common belief); ~70 h of real multi-party meetings turns every AMI-only result into a two-corpus result at trivial cost. |
| 5 | **SpokenNativQA** | 364 MB | Cheapest high-value spoken-QA acquisition. Coupling is clean *because* it ships no passage — open-domain queries unanswerable from audio alone, so evidence injection carries zero leakage hazard. Ships free multi-ASR transcripts as an OBS-quality axis. |
| 6 | **AudioBench** (scoped) | ~3–6 GB `UNVERIFIED` | Uniquely sanctions a **local Llama-3-70B judge**, converting a judge metric into a pinnable one; its `spoken_squad_test` and `slue_p2_sqa5_test` slices are document-grounded. Must exclude the five non-speech configs named above. |
| 7 | **SD-QA** (EN subset) | `UNVERIFIED`, small | Constant questions × ~10–11 English dialects is a built-in controlled OBS experiment; Apache-2.0. Caveat: Google-Drive distribution is fragile for hash pinning. |
| 8 | **MeetingBank** (bounded subset) | text 115 MB + bounded audio slice | Agenda and council roster ship **as metadata** — the best-shaped meeting coupling found. Requires a bounded subset decision; the full 198 GB audio repo is not acquirable under our policy, and NC-SA is stricter than what we hold. |
| 9 | **AudioMarathon** (speech slice) | fraction of ~20–40 GB | The only long-form regime (90–300 s) a turn-based frozen core can plausibly consume whole; admit ASR/SER/SCR/QA only. |
| 10 | **QMSum** | <100 MB | Pairs with #1 and #4: an annotation layer over AMI (137) + ICSI (59) audio we would then hold, at negligible cost. |

**Watch list, not acquisitions:** ToolVoice (CC BY 4.0 and benchmarks our exact core — acquire the
moment the audio-vs-script question resolves), DuplexWorld (six days old, re-scout), Stream
RAG/AudioCRAG (618 *human* spoken queries; worth author contact), aiewf-eval (metric design worth
copying even if the corpus is too small).

**Explicitly not recommended:** VoxEval (88 GB for LOW coupling), NSF-QA (305 GB + judge metric),
LongSpeech (ND licence), Dynamic-SUPERB (inadmissible until its 180 tasks are classified).

## 6. Blocked, unverified and conflicting

**Blocked — data not obtainable at zero cost today:** Stream RAG/AudioCRAG (promised, not released),
DuplexWorld (none found), VAmoS (scenarios proprietary to the authors' platform), ProVoice-Bench,
FOCAL, EchoChain, DuplexSLA-Bench ("coming soon" vs paper's "publicly available" — contradiction
recorded), BFCL Audio (canonical blog 403s), `arcada-labs/audio-agent-bench-suite` (complete card,
**zero bytes**), EVA-Bench (50 of 213 scenarios, no audio, harness needs five paid services),
LongSpeech (HF 401 + NoDerivatives), VoiceGiraffe (GitHub 404), ChronosAudio (anonymous review link),
LiveLongBench (signed request form), BLAB (YouTube URLs, not bytes), τ-Voice (paid realtime APIs).

**Licence / size conflicts recorded, not resolved:** Audio2Tool (`cc-by-nc-4.0` on HF and in our lock
vs CC BY 4.0 paper badge); WearVox (CC BY-NC-SA 4.0 paper vs `cc-by-nc-4.0` HF; 3,842 paper rows vs
4,000 HF rows); MMAU (Apache-2.0 GitHub vs `cc-by-nc-4.0` HF); ADU-Bench (2.21 GB / 210 HF rows vs
20,715 dialogues claimed); Audio2Tool released `public/` subset ~16.8k queries vs the paper's ~30k.

**Resolved open question from the prior survey:** **BFCL v4 has no audio tier.** The phrase in
arXiv:2605.15104 cites reference [42], a **Salesforce blog post** ("BFCL Audio", Salesforce AI
Research + Berkeley, 2025-08-22) — a separate artifact, not a Gorilla leaderboard tier. The official
Gorilla blog index has six posts, none audio; the V4 leaderboard shows no audio category; nothing on
the gorilla GitHub or HF. BFCL Audio's own published failure mode is worth citing regardless: a
~10–20% drop "largely because models fail to correctly handle entity dictation".

**Negative results worth keeping:** no spoken **MCP** benchmark exists (that space is entirely text);
no level-E agentic benchmark uses **real human speech**; and per arXiv:2603.16292 no public
real-speech **multi-hop** spoken QA set exists. That paper also publishes frozen **Qwen3-Omni-30B-A3B**
spoken-QA baselines — 75.02 HotpotQA / 45.88 MuSiQue / 88.37 SQuAD — on our exact core, with
MuSiQue's 45.88 the largest supply headroom surfaced by this scan.

**Baseline reconciliation caution:** three different Qwen3-Omni numbers circulate for Audio2Tool
(92.4%→41.7% by command complexity; >75% Tier-1 falling under 55% EM/F1 on Tiers 5–7; and the
study's own local measurement tool-acc 84.6% vs EM 15.6%). These are different slices, not competing
estimates of one quantity — never average or interchange them.
