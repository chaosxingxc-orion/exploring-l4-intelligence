# Speech-Semantic Task Datasets — Public Catalog (SLU · Spoken-QA · ST · Agentic)

A curated, **verified-public** dataset set for the semantic axis our flagship omni **embedding** is
strong on. Companion to [[Paralinguistic-Suppression-Survey]] (why the embedding is semantic-specialized)
and [[Data-and-Assets]] (the full asset inventory). These sets are now **downloaded and FROZEN** — see
`docs/datasets.lock.json` for the authoritative local inventory (§2); the fetch scripts were retired.

## 0. The conclusion that motivates this page (adversarial)

**Claim.** `omni-embed-nemotron-3b` (contrastive InfoNCE retrieval bi-encoder, masked-mean → one 2048-d
vector) is a **semantically-specialized speech embedding**, so its best use is semantic tasks: SLU,
Spoken-QA, Speech-Translation, speech-agentic.
- **For:** measured on the same audio — content ≈1.00, language/intent near-semantic-strong, emotion
  ≈0.40 (capped), speaker ≈0.04 (chance). Trained to align audio↔**text semantics**.
- **Against:** "only semantic" overstates — it keeps *partial* emotion (0.40 ≫ chance 0.17) and coarse
  paralinguistics; and the verdict is scoped to the **embedding/retrieval class**, not generative omni
  models (which can read out paralinguistics). "Semantic" is itself multi-faceted (content, language,
  translation-equivalence, intent).
- **Verdict.** HOLDS, scoped: leaning onto semantic tasks plays to a *measured* strength and is
  complementary to (not a reversal of) the disentanglement thesis — content/language were always the
  Operator-A-native factors. **Open:** full pivot vs. a second track (affects whether the starter set
  optimizes for breadth or for Spoken-QA depth, our biggest local gap).

## 1. Provenance & verification

Workflow `wf_bb9e0de5-93c` (6 agents): 36 candidates → 16 core picks → **adversarial link-check
re-fetched all 16** → **0 hallucinated, 0 access-gated; license/source caveats flagged below.** Two
candidate names from the original ask did not survive: "Spoken-SQuAD-NER" (does not exist → replaced by
**MSNER**) and SLUE-Phase-1 (listed OPEN but is actually **GATED** → demoted).

## 2. Status: downloaded & FROZEN (fetch scripts retired)

These datasets are **downloaded and locked**. The dataset set is frozen to the snapshot in
`docs/datasets.lock.json` — the authoritative record of what is local, with pinned revisions. Audit it
with `bash scripts/data/inventory.sh`; the full inventory is in [[Data-and-Assets]] / `docs/data.md`.

The two one-off fetch scripts that originally pulled these (`fetch-semantic-modelscope.sh`,
`fetch-semantic-manual.sh`) have been **removed**. The **local?** column in §3 below is historical and
is superseded by `datasets.lock.json`.

*(Historical note: of this catalog, only VoiceBench and FLEURS were on ModelScope; the rest came via
hf-mirror or a direct source, e.g. SLURP audio from Zenodo 4274930.)*

## 3. Core sets per family

Columns: name · subtype · langs · license · **ModelScope?** · source id · local? · fetch.

### Speech Translation (strongest semantic axis; 2/4 already local)
| dataset | subtype | langs | license | ModelScope | source | local | fetch |
|---|---|---|---|---|---|---|---|
| **CoVoST 2** | X↔en S2T (36 dir) | 21→en + 15 en→X | CC-BY-NC | ✗ | hf `facebook/covost2` | ✅ | (local) |
| **FLEURS** | n-way parallel ST + LID | 102 | CC-BY | **✓ `pengzhendong/fleurs`** | hf `google/fleurs` | ✅ | (local) |
| **FLEURS-R** | restored-audio FLEURS | 102 | CC-BY | ✗ | hf `google/fleurs-r` | ✗ | manual `fleurs-r` |
| **CVSS** | S2**S**T | 21→en | CC-BY | ✗ | hf `google/cvss` | ✗ | manual `cvss` |

### SLU (intent / slot / parse — native fit for a content embedder)
| dataset | subtype | langs | license | ModelScope | source | local | fetch |
|---|---|---|---|---|---|---|---|
| **MINDS-14** | intent | 14 | CC-BY | ✗ | hf `PolyAI/minds14` | ✅ | (local) |
| **Speech-MASSIVE** | intent+slot (multiling.) | 12 | CC-BY-NC-SA (eval-only) | ✗ | hf `FBK-MT/Speech-MASSIVE` | ✗ | manual `speech-massive` |
| **SLURP** | intent+slot (18 domains) | en | audio CC-BY-NC | ✗ | Zenodo 4274930 / GitHub | ✗ | manual `slurp` (direct) |
| **STOP** | compositional parse | en | CC-BY-SA | ✗ | fbaipublicfiles / GitHub | ✗ | manual `stop` (direct) |

**SLU — more public, benchmarking-permitted options** (none on ModelScope; all via hf-mirror/GitHub):
- **Google Speech Commands v2** · CC-BY-4.0 · keyword spotting (borderline SLU) · hf `google/speech_commands` · script `speech-commands`
- **Fleurs-SLU** (2025) · CC-BY-SA · topical-classification + listening-comprehension over the **102-lang FLEURS we already have** · hf/GitHub `fdschmidt93/fleurs-slu`
- **Timers and Such** · **CC0** (fully open) · timer/alarm/unit/math commands · Zenodo 4623772
- **ProSLU** · GPL-2.0 · Mandarin intent+slot with profile/KG context · GitHub `looperxx/proslu`
- **INJONGO** (2025) · GPL-3.0 · 16 African languages, intent+slot · hf `McGill-NLP/Injongo`
- **MSNER** · multilingual spoken NER (nl/fr/de/es) · GitHub `qmeeus/MSNER` · **SLUE Phase-2** · dialog-act/NER/spoken-QA/summarization · hf `asapp/slue-phase-2`

**SLU — known but NOT usable as a benchmark (the "what about FSC?" answer):**
- **Fluent Speech Commands (FSC)** — famous, but **CC-BY-NC-ND-4.0 explicitly forbids "training, testing,
  benchmarking, or developing a product"** → excluded for any benchmark use (this is the license blocker).
- **SNIPS / SmartLights (Sonos)** — audio is request-form-gated + academic-only.
- **ATIS** — LDC-licensed (paid; LDC93S5/94S19/95S26), not freely public.
- **CATSLU** (Mandarin) — license + full-data access undocumented / challenge-gated.
- **Skit-S2I** (Indian English) — CC-BY-NC (research-only; commercial unclear).

### Spoken-QA (extractive QA = semantic matching; our biggest local gap)
| dataset | subtype | langs | license | ModelScope | source | local | fetch |
|---|---|---|---|---|---|---|---|
| **HeySQuAD (human)** | extractive, gold spans | en | CC-BY | ✗ | hf `yijingwu/HeySQuAD_human` | ✗ | manual `heysquad` |
| **VoiceBench (QA)** | MCQ + open QA | en (+accents) | Apache-2.0 | **✓ `lmms-lab/voicebench`** | hf `hlt-lab/voicebench` | ✗ | **ms `voicebench`** |
| **MMSU** | multi-skill reasoning MCQ | en | MIT | ✗ | hf `ddwang2000/MMSU` | ✗ | manual `mmsu` |
| **Spoken-SQuAD** | extractive, ASR-noise | en | CC-BY-SA (re-host) | ✗ | hf `AudioLLMs/spoken_squad_test` | ✗ | manual `spoken-squad` |

### Speech-agentic (mostly generative/behavioural; embedding eval = intent clustering)
| dataset | subtype | langs | license | ModelScope | source | local | fetch |
|---|---|---|---|---|---|---|---|
| **VoiceBench** | instruction/safety/agentic | en | Apache-2.0 | **✓ `lmms-lab/voicebench`** | hf `hlt-lab/voicebench` | ✗ | **ms `voicebench`** |
| **URO-Bench** | EN+ZH spoken dialogue | en, zh | MIT | ✗ | hf `Honggao/URO-Bench` | ✗ | manual `uro-bench` |
| **VocalBench** | 9-axis conversational | en (+zh) | Apache-2.0 | ✗ | hf `VocalNet/VocalBench` | ✗ | manual `vocalbench` |
| **Big Bench Audio** | spoken reasoning | en | MIT | ✗ | hf `ArtificialAnalysis/big_bench_audio` | ✗ | manual `big-bench-audio` |

**Speech-agentic — recent additions (2024-2026, web-verified, 0 hallucinated)** (none on ModelScope except tau2 → otherwise hf-mirror):
| dataset | year | subtype | langs | license | source | fetch |
|---|---|---|---|---|---|---|
| **VoiceAssistant-Eval** | 2025 | listen/speak/view, 13 categories (incl. roleplay, safety, S2S quality) | en | MIT | hf `MathLLMs/VoiceAssistant-Eval` | manual `voiceassistant-eval` |
| **VocalBench-zh** | 2025 | **Mandarin** spoken-interaction (11 subsets, +dialect/code-switch) | zh | Apache-2.0 | hf `VocalNet/VocalBench-zh` | manual `vocalbench-zh` |
| **Audio MultiChallenge** | 2025 | multi-turn instruction retention | en | MIT | hf `ScaleAI/audiomc` | manual `audiomc` |
| **SoulX-Duplug-Eval** | 2026 | **full-duplex** turn-taking (EN + **ZH**) | en, zh | Apache-2.0 | hf `Soul-AILab/SoulX-Duplug-Eval` | manual `soulx-duplug` |
| **EVA-Bench** | 2026 | voice-agent task-accuracy + experience (airline) | en | MIT | hf `ServiceNow-AI/eva` | manual `eva-bench` |
| **tau2-bench (voice)** | 2026 | tool-use agent | en | MIT | **✓ ms `evalscope/tau2-bench-data`** | **ms `tau2-bench`** |
| VoiceAgentBench | 2025 | voice tool-use / function-calling | en,hi,bn+ | **Krutrim community (gated)** | hf `krutrim-ai-labs/VoiceAgentBench` | gated — accept license |

Also (agentic): SpeechInstructBench (en/zh IF + noise/accent robustness, Apache), Speech-IFEval (IF + catastrophic-forgetting probe), MMAU-Pro (2025 harder MMAU successor, NC), **AudioJailbreak** (`MBZUAI/AudioJailbreak`, safety/refusal, Apache), Full-Duplex-Bench-v2, MultiDialog (emotional face-to-face), RealTalk-CN (150h zh, **gated**, NC).

### Speech-Retrieval (2024-2026) — the bi-encoder's native eval surface
Our flagship embeds `query:` text and `passage:` audio into one space, so **retrieval benchmarks are the most direct way to score it.** (none on ModelScope → hf-mirror / harness):
| dataset | year | subtype | langs | license | source | fetch |
|---|---|---|---|---|---|---|
| **MAEB** (Massive Audio Embedding Benchmark) | 2026 | audio-embedding suite, 30 tasks (MTEB ecosystem) | 100+ | Apache-2.0 (per-task vary) | MTEB / arXiv `2602.16008` | harness (`mteb`) |
| **MSEB / SVQ** | 2026 | spoken-query retrieval/rerank under 4 noise conditions, 177k queries | 17 | CC-BY-4.0 | hf `google/svq` | manual `svq` |
| **FLEURS-Retrieval** (XTREME-S) | 2022* | cross-lingual speech↔text retrieval (fixed-size utterance embedding) | 102 | CC-BY-4.0 | hf `google/xtreme_s` | manual `xtreme-s` |
| **SLUE-SQA-5** | 2022* | spoken-document retrieval (answer span in spoken passage) | en | mixed CC-BY-SA | hf `asapp/slue-phase-2` | manual `slue-phase-2` |
| **WavCaps** | 2023* | large text↔audio retrieval, 403k clips / 820 GB | en | CC-BY **academic-only** | hf `cvssp/WavCaps` | (huge; academic-only) |
| **SpeechBrown** (CLASP) | 2024 | contrastive speech-text retrieval (**synthetic TTS**) | en | MIT | hf `llm-lab/SpeechBrown` | (verify id) |

`*` older but still the reference for that axis (year marked). **MAEB (arXiv 2602.16008, MTEB-ecosystem) and MSEB
(arXiv 2602.07143, Google) are TWO separate benchmarks** despite near-identical names — don't conflate. For
omni-embed-nemotron-3b, **MAEB + MSEB/SVQ are the primary surface** (run via the MTEB harness our text side
already knows); FLEURS-Retrieval / WavCaps / SLUE-SQA-5 add cross-lingual / text↔audio / spoken-document axes.
Also: MSEB 8-task framework (`google-research/mseb`), SpeechMatrix (S2S mining, NC), **Auto-ACD** (CC0, 1.9M
audio-text pairs), AudioSetCaps, AudioCaps/Clotho (foundational test sets), SQuTR (2026, niche), OmniSONAR (watch).

## 4. Multi-family bridges (one fetch, several tasks)

- **VoiceBench** — Spoken-QA *and* agentic in one repo (the cheapest two-family cover); on ModelScope.
- **Speech-MASSIVE** — SLU *and* derivable X→en ST (parallel to English MASSIVE text); 12 langs.
- **FLEURS** — ST (any-to-any, n-way parallel) *and* language-ID; already local.
- **AudioBench** (`AudioLLMs/AudioBench`) — an *umbrella harness* aggregating 50+ ASR/ST/SQA/SLU sets;
  treat as the evaluation runner, not a single dataset to fetch (per-subset licenses vary).

## 5. Adversarial flags & exclusions (carry these forward)

- **NonCommercial / ShareAlike (eval-only-safe, no commercial release):** Speech-MASSIVE (NC-SA),
  CoVoST 2 (NC), Spoken-SQuAD (SA), MMAU-Pro (NC), mTEDx/Europarl-ST/GigaST (NC).
- **Unofficial re-uploads (license unconfirmable from the card — prefer the official source):** the
  `qmeeus/slurp` mirror (use Zenodo 4274930), `AudioLLMs/spoken_squad_test` (benchmark re-host).
- **Usability caveats (data downloads fine, HF viewer/repo state degraded):** FLEURS-R viewer errors;
  STOP repo archived/read-only (LICENSE present, verify before redistribution).
- **EXCLUDE — Fluent Speech Commands:** its license (CC-BY-NC-ND) explicitly forbids
  testing/benchmarking. **GATED (need agreement):** SLUE-Phase-1, MuST-C, SNIPS-Audio, VoxCeleb.
- **Unverified license (usable, treat with care):** NMSQA, LibriSQA, Spoken-MQA, CN-College-Listen.
- **Agentic/retrieval recency batch (2024-2026):** VoiceAgentBench **gated** (Krutrim Community License,
  not OSI); RealTalk-CN **gated** + NC; **WavCaps** academic-only + 820 GB (kept out of the fetch script);
  **SpeechBrown** is synthetic TTS — verify `llm-lab/SpeechBrown` loads before relying on it; MMAU-Pro /
  SpeechMatrix are NC. **ModelScope:** only `evalscope/tau2-bench-data` is hosted there — all other recent
  sets are hf-mirror-only.

## 6. Status & next

Catalog + two fetch scripts committed; downloads are the user's to run. **Next once fetched:** wire a
semantic-eval harness (retrieval/probe + generative readout) on the starter set and report the
embedding's per-task numbers — the positive complement to the [[Paralinguistic-Suppression-Survey]]
negatives (speaker/emotion). Decision: full pivot vs. second track (see §0).

---

## 中文

为旗舰 omni **嵌入**所擅长的语义轴curate 的**已核验公开**数据集（SLU/Spoken-QA/ST/agentic）。配套
[[Paralinguistic-Suppression-Survey]]（为何嵌入是语义特化）与 [[Data-and-Assets]]。这些集已**下载并冻结**——以 `docs/datasets.lock.json` 为本地权威清单（§2）；抓取脚本已退役。

**§0 动因结论（对抗）：** 断言=omni-embed 是语义特化嵌入，最佳用途是语义任务。支持：同音频实测内容≈1.00、
语言/意图近语义强、情感≈0.40(上限)、说话人≈0.04(随机)。反驳：「仅语义」过强（仍留部分情感+粗粒度副语言）、
范围限嵌入/检索类（生成式 omni 不同）、语义本身多面。裁决：成立（限定）——转向语义任务是顺measured 强项，
与解耦论点互补。**待定**：全面转向 vs 第二条 track（影响启动集求广还是求 Spoken-QA 深度）。

**§1 来源与核验：** workflow `wf_bb9e0de5-93c`（6 agent）36→16，**对抗式逐一重抓 16 个链接：0 臆造、0
gated**；许可/来源风险见 §5。两个原始候选未存活：「Spoken-SQuAD-NER」不存在（→ MSNER）、SLUE-1 实为 GATED。

**§2 状态：已下载并冻结（抓取脚本已退役）。** 这些数据集已本地化并锁定，集合冻结于
`docs/datasets.lock.json`（本地权威清单，含锁定版本）。用 `bash scripts/data/inventory.sh` 审计；完整清单见
[[Data-and-Assets]] / `docs/data.md`。原先用于抓取的两个一次性脚本（`fetch-semantic-modelscope.sh`、
`fetch-semantic-manual.sh`）已删除；§3 的「local?」列为历史信息，以 `datasets.lock.json` 为准。

**§3 各族 core set** 见英文表（含 **ModelScope 可获得性列** + 本地状态 + fetch 名）。**§4 多族桥**：
VoiceBench(QA+agentic)、Speech-MASSIVE(SLU+ST)、FLEURS(ST+LID)、AudioBench(harness)。**§5 对抗标记**：
NC/SA 仅 eval（Speech-MASSIVE/CoVoST2/Spoken-SQuAD…）；社区 re-upload 许可不可证（qmeeus/slurp→官方 Zenodo、
AudioLLMs/spoken_squad_test）；FLEURS-R viewer 坏但可下、STOP repo 归档；**排除 FSC**（许可禁基准）；**gated**：
SLUE-1/MuST-C/SNIPS/VoxCeleb。**§6 下一步**：启动集到位后接语义评测 harness（检索/探针 + 生成读出），报告
嵌入逐任务数字——作为 [[Paralinguistic-Suppression-Survey]] 负面（说话人/情感）的正面互补。
