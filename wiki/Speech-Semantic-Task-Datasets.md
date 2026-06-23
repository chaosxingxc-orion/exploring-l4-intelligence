# Speech-Semantic Task Datasets — Public Catalog (SLU · Spoken-QA · ST · Agentic)

A curated, **verified-public** dataset set for the semantic axis our flagship omni **embedding** is
strong on. Companion to [[Paralinguistic-Suppression-Survey]] (why the embedding is semantic-specialized)
and [[Data-and-Assets]] (the full asset inventory). Fetch with the two scripts in §2 — you run them
yourself in WSL.

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

## 2. How to fetch (you run these; downloads are large)

**ModelScope reality (web-verified):** of the catalog, **only VoiceBench (`lmms-lab/voicebench`) and
FLEURS (`pengzhendong/fleurs`, already local) are on ModelScope.** Everything else is **not** on
ModelScope → hf-mirror, or a direct source (SLURP→Zenodo, STOP→fbaipublicfiles). Two scripts split this:

- `scripts/data/fetch-semantic-modelscope.sh` — the ModelScope-hosted sets. `--list` / `--dry-run` / `all` / `<name>`.
- `scripts/data/fetch-semantic-manual.sh` — the rest, via hf-mirror (`HF_ENDPOINT=https://hf-mirror.com`,
  prefers `hfd`+aria2c) + direct (SLURP, STOP print manual instructions). Same flags.

Both honor `SPEECHRL_DATA_DIR`, `SPEECHRL_SKIP_EXISTING=1` (skip already-local), `SPEECHRL_MS_WORKERS`,
`SPEECHRL_HFD_THREADS`; dirs land in `speechrl-data/datasets/<hyphenated-name>`. Run in the speechrl venv.

**Minimal starter (covers all four families, only 2 new fetches):**
```
bash scripts/data/fetch-semantic-modelscope.sh voicebench    # QA + agentic (ModelScope)
bash scripts/data/fetch-semantic-manual.sh    heysquad        # clean extractive spoken-QA (hf-mirror)
# CoVoST2 + FLEURS (ST) and MINDS-14 (SLU) are already local.
```

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

## 6. Status & next

Catalog + two fetch scripts committed; downloads are the user's to run. **Next once fetched:** wire a
semantic-eval harness (retrieval/probe + generative readout) on the starter set and report the
embedding's per-task numbers — the positive complement to the [[Paralinguistic-Suppression-Survey]]
negatives (speaker/emotion). Decision: full pivot vs. second track (see §0).

---

## 中文

为旗舰 omni **嵌入**所擅长的语义轴curate 的**已核验公开**数据集（SLU/Spoken-QA/ST/agentic）。配套
[[Paralinguistic-Suppression-Survey]]（为何嵌入是语义特化）与 [[Data-and-Assets]]。用 §2 两个脚本自行下载。

**§0 动因结论（对抗）：** 断言=omni-embed 是语义特化嵌入，最佳用途是语义任务。支持：同音频实测内容≈1.00、
语言/意图近语义强、情感≈0.40(上限)、说话人≈0.04(随机)。反驳：「仅语义」过强（仍留部分情感+粗粒度副语言）、
范围限嵌入/检索类（生成式 omni 不同）、语义本身多面。裁决：成立（限定）——转向语义任务是顺measured 强项，
与解耦论点互补。**待定**：全面转向 vs 第二条 track（影响启动集求广还是求 Spoken-QA 深度）。

**§1 来源与核验：** workflow `wf_bb9e0de5-93c`（6 agent）36→16，**对抗式逐一重抓 16 个链接：0 臆造、0
gated**；许可/来源风险见 §5。两个原始候选未存活：「Spoken-SQuAD-NER」不存在（→ MSNER）、SLUE-1 实为 GATED。

**§2 下载（你手动跑）：ModelScope 现实**——本目录仅 **VoiceBench(`lmms-lab/voicebench`) 与
FLEURS(`pengzhendong/fleurs`，已本地)** 在 ModelScope；其余须 hf-mirror 或直链。两脚本：
`fetch-semantic-modelscope.sh`（ModelScope 可下）与 `fetch-semantic-manual.sh`（hf-mirror + SLURP/STOP
直链）。均支持 `--list/--dry-run/all/<name>`，`SPEECHRL_SKIP_EXISTING=1` 跳过已在。**最小启动集（仅 2 个新
下载）**：`voicebench`(ModelScope) + `heysquad`(hf-mirror)，CoVoST2/FLEURS/MINDS-14 已本地。

**§3 各族 core set** 见英文表（含 **ModelScope 可获得性列** + 本地状态 + fetch 名）。**§4 多族桥**：
VoiceBench(QA+agentic)、Speech-MASSIVE(SLU+ST)、FLEURS(ST+LID)、AudioBench(harness)。**§5 对抗标记**：
NC/SA 仅 eval（Speech-MASSIVE/CoVoST2/Spoken-SQuAD…）；社区 re-upload 许可不可证（qmeeus/slurp→官方 Zenodo、
AudioLLMs/spoken_squad_test）；FLEURS-R viewer 坏但可下、STOP repo 归档；**排除 FSC**（许可禁基准）；**gated**：
SLUE-1/MuST-C/SNIPS/VoxCeleb。**§6 下一步**：启动集到位后接语义评测 harness（检索/探针 + 生成读出），报告
嵌入逐任务数字——作为 [[Paralinguistic-Suppression-Survey]] 负面（说话人/情感）的正面互补。
