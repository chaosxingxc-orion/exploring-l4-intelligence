---
title: "Agentic-RAG landscape + baselines + omni-speech applicability (WS-1/2/3)"
date: 2026-07-07
stage: 1-argumentation
status: "Stage-1 T1/WS-1-2-3 deliverable (workflow wf_8b59da73, 9 research + 2 verify + 2 synth). Effect-over-novelty; citation-verified; hypothesis-grade. Owner review pending; wiki-sync deferred."
---

> **LOG** — Stage-1 过程记录（hypothesis-grade），非现行真源；现行结论以 [[Decision-Log]] 与 [[Per-Work-Status]] 为准。

# Agentic-RAG Landscape, Baselines, and Omni-Speech Applicability

Stage-1 problem-definition deliverable · WS-1 / WS-2 / WS-3 · 2026-07-06
Evidence grade: **Stage-1 / hypothesis-grade** (literature argumentation; NOT this project's large-sample validation). Every baseline below cites a real, session-verified id (~45 unique arXiv/OpenReview ids checked, including all future-dated ones past the Jan-2026 cutoff — none fabricated).
Framing (owner stance, load-bearing): we do **not** chase novelty. Object = find EXISTING baselines and determine HOW a training-free-RL lever (frozen weights; inference-time reward selection/gating/injection) plugs into each to **measurably raise effect**. All applicability claims carry a model-generation caveat: the "frozen speech-LLM must fine-tune to consume a retrieved element" gap (MARS/RASST/VoxMind) was observed on 2025→2026-04 models; our base is Qwen3-Omni (2026-04/05), so consumption may be materially better — that is the crux to test, not assume.

Column legend
- **Train status:** `FROZEN` = training-free at inference (no weight update, no trained component) · `COMPONENT` = trains a sub-module (retriever/evaluator/reranker) but generator frozen · `FT` = fine-tunes the generator · `MIXED` = has both a frozen path and a weight-updating path.
- **Applicability to frozen-omni-speech:** `PORTS-CLEAN` = control flow + consumption transfer with no training · `PORTS-FRAGILE` = loop ports but the audio/query seam (ASR-loss into query, uncertainty mis-calibration, latency) degrades it · `TRAINED-DEP` = the audio-native version found requires a trained piece · `EMPTY` = no baseline surfaced (opportunity, not proven-absent).

---

## 1. The landscape table (technique family → baseline → benchmark → metric → trained/frozen → applicability)

### 1a. Adaptive / when-to-retrieve gating

| Representative baseline (id) | Benchmark | Headline metric | Train status | Applicability to frozen-omni-speech |
|---|---|---|---|---|
| **FLARE** (arXiv:2305.06983) | 2WikiMultihopQA | EM 51.0 vs 39.4 single-retrieval | FROZEN | PORTS-FRAGILE — gates on token probability; raw-probability trigger tuned on a 2023 model and likely UNDER-fires on a strong 2026 omni; >50–60% retrieval rate HURTS. |
| **TARG** (arXiv:2511.09803) | NQ-Open / TriviaQA (+PopQA, MuSiQue, ASQA) | EM/F1 57.6/54.7 @ 0.8% retrieval (NQ); 62.2/62.6 @ 33.8% (TriviaQA) | FROZEN | PORTS-FRAGILE — logit-margin gate; validated on **Qwen2.5-7B / Llama-3.1-8B (prior-generation, text-only)** — NOT our Qwen3-Omni generation or modality. Directional finding "margin > entropy as backbones sharpen" is a lever to validate, not same-generation confirmation. |
| **SeaKR** (arXiv:2406.19215; OpenReview NhIaRz9Qf5) | 2WikiMultihopQA / HotpotQA | EM / F1 (uncertainty-gated) | FROZEN | PORTS-FRAGILE — gates on internal-state (Gram-determinant) uncertainty; readable on a frozen omni but conflates knowledge-gap vs perception-gap uncertainty. |
| **Adaptive-RAG** (arXiv:2403.14403) | HotpotQA/MuSiQue/2Wiki; SQuAD/NQ/TriviaQA | F1/EM/Acc + steps/time Pareto | COMPONENT | PORTS-FRAGILE — trains a t5-large complexity router over TEXT queries; does not transfer to spoken queries without transcribing (ASR-loss) or retraining. TFRL re-cast = reward-guided escalation. |
| **Decide-Then-Retrieve** (arXiv:2601.03908) | multi-hop QA | EM/F1 | FROZEN | PORTS-FRAGILE — normalized-NLL uncertainty trigger; same dual-source-uncertainty break as SeaKR. |
| **Self-RAG** (arXiv:2310.11511) | PopQA 54.9 / PubHealth 74.5 / ARC 73.1 / Bio FactScore 81.2 / ASQA cite-prec 66.9 | FT | Reflection tokens (Retrieve/IsRel/IsSup/IsUse) are SFT'd into the generator vocabulary — **does not port training-free**; what ports is the 4-decision DECOMPOSITION, each externalizable as a reward-scored gate. |

### 1b. Corrective RAG

| Representative baseline (id) | Benchmark | Headline metric | Train status | Applicability to frozen-omni-speech |
|---|---|---|---|---|
| **CRAG** (arXiv:2401.15884) | PopQA / Biography | PopQA 37.7 (std-RAG floor) → 39.8; Bio FactScore 44.9 → 47.7 | COMPONENT | PORTS-CLEAN scaffold — pipeline wrapper around a FROZEN generator; only the T5-large retrieval evaluator (0.77B) is trained. Its Correct/Ambiguous/Incorrect router + decompose-recompose refinement is the natural TFRL scaffold; the trained evaluator is exactly the piece a reward or frozen omni-as-judge replaces. |
| **Self-CRAG** (arXiv:2401.15884) | PopQA / Biography | PopQA 54.9 → 61.8 (+6.9); Bio 81.2 → 86.2 (+5.0) | MIXED | Sets the UPPER expectation (size-of-prize at the retrieval-quality + routing decision points) but obtained with a **fine-tuned** Self-RAG generator — not frozen-achievable; the standard-RAG-on-frozen-LLaMA2 37.7 PopQA is the true training-free floor. |

### 1c. Iterative / multi-hop interleaved reason-retrieve

| Representative baseline (id) | Benchmark | Headline metric | Train status | Applicability to frozen-omni-speech |
|---|---|---|---|---|
| **ReAct** (arXiv:2210.03629) | HotpotQA/FEVER; ALFWorld/WebShop | task success +34pp ALFWorld, +10pp WebShop | FROZEN | PORTS-FRAGILE — modality-agnostic scaffold; runs on a frozen omni only via ASR→text in the loop. |
| **IRCoT** (arXiv:2212.10509) | HotpotQA/2Wiki/MuSiQue/IIRC | retrieval recall +21, answer F1/EM +15 | FROZEN | PORTS-FRAGILE — each CoT step builds the next query from the model's own text → a mis-transcribed spoken entity poisons the sub-query and error COMPOUNDS across hops. |
| **Self-Ask** (arXiv:2210.03350) | Bamboogle / 2Wiki | Bamboogle 60.0%; 2Wiki 30.0→40.1 (with search) | FROZEN | PORTS-FRAGILE — same query-formulation-from-ASR-text break. |
| **DRAGIN** (arXiv:2403.10081) | 2Wiki/HotpotQA/StrategyQA/IIRC | EM/F1/acc, beats fixed-rule dynamic RAG | FROZEN | PORTS-FRAGILE — entropy + self-attention (QFS) trigger/query from frozen internals; acoustic uncertainty not captured by token-level signals. |
| **Search-o1** (arXiv:2501.05366) | HotpotQA 45.2 vs 34.2 RAG; 2Wiki 58.0 vs 35.6; GPQA 63.6 | FROZEN | PORTS-FRAGILE — strongest MEASURED "frozen reasoner uses retrieval agentically" evidence (frozen QwQ-32B; Reason-in-Documents condensation); latency compounds badly for real-time voice. Model-generation caveat: won on a strong text LRM, not an audio omni. |
| **Search-R1** (arXiv:2503.09516) | 7 QA sets | EM +41% (Qwen2.5-7B) / +20% (3B) over RAG | FT | Trained CONTRAST — "what training buys"; the price a TFRL lever must chase without weights. Same decision points (retrieve/query/stop) being LEARNED vs SELECTED. |

### 1d. Graph / structured / hierarchical organization + traversal

| Representative baseline (id) | Benchmark | Headline metric | Train status | Applicability to frozen-omni-speech |
|---|---|---|---|---|
| **RAPTOR** (arXiv:2401.18059) | QuALITY / QASPER / NarrativeQA | QuALITY 82.6% (+20pt SOTA); QASPER F1 55.7 | FROZEN | PORTS-CLEAN index — recursive embed→cluster→summarize tree; dense-embeds the (noisy) spoken query, so most ASR-robust of the three. Index built offline over TEXT, no weight change. |
| **HippoRAG** (arXiv:2405.14831) | 2Wiki / MuSiQue / HotpotQA | 2Wiki R@5 89.1; HotpotQA F1 55.0; 6–13× faster than IRCoT | FROZEN | PORTS-FRAGILE (most fragile) — "all components used off-the-shelf, no extra training", but PPR seeds from query entities → an ASR error on a rare/OOV entity seeds the wrong node and multi-hop retrieval collapses (the CB-RAG failure mode). |
| **GraphRAG** (arXiv:2404.16130) | global sensemaking (podcast+news) | LLM-judge win-rate vs vector RAG: comprehensiveness 72–83%, diversity 62–82% | FROZEN | PORTS-CLEAN retrieval / latency-break — global map-reduce is query-agnostic (ASR-robust for recall) but seconds-to-minutes of LLM calls breaks a voice budget; local (entity-anchored) search is the deployable variant. Its built-in 0–100 map-step self-judge carries documented position/length bias → replace with a decorrelated verifier. |

### 1e. Agentic frameworks / deep-research / self-improving RAG

| Representative baseline (id) | Benchmark | Headline metric | Train status | Applicability to frozen-omni-speech |
|---|---|---|---|---|
| **Agentic Reasoning** (arXiv:2502.04644) | GPQA + PhD-level deep-research | pass@1 accuracy | FROZEN | PORTS-FRAGILE — web-search + code + Mind-Map KG agent on a frozen LRM; the persistent Mind-Map would become cross-session memory (collides with the 2026-07-03 NO-GO) → keep the store within-episode. |
| **Auto-RAG** (arXiv:2411.19443) | NQ/TriviaQA/PopQA/HotpotQA/2Wiki | EM/F1 | FT | Fine-tunes the LLM on synthesized reason-retrieve trajectories — trained contrast, not a frozen path. |
| **Agentic RAG: A Survey** (arXiv:2501.09136) | — (taxonomy) | — | n/a | Taxonomy source (single/multi-agent, corrective, adaptive, graph-based; reflection/planning/tool-use). |

### 1f. Speech-primary retrieval (WS-2 audio-native cell)

| Representative baseline (id) | Benchmark | Headline metric | Train status | Applicability to frozen-omni-speech |
|---|---|---|---|---|
| **CB-RAG** — Siskos et al., "RAG-based context discovery for ASR" (arXiv:2509.19567); "CB-RAG" is our shorthand | contextual-biasing ASR (rare/OOV) | WER ↓ up to 17% rel (24.1% @ oracle) at 1.02–1.36× latency | FROZEN | PORTS-CLEAN — the clean training-free SPEECH positive; MiniLM lexical retrieval over a 466k-word vocab injected into frozen ASR context, plug-and-play/black-box. |
| **VoxRAG** (arXiv:2505.17326) | speech-to-speech podcast QA (50 queries) | R@10 0.34/0.60; nDCG@10 0.03/0.27 (weak) | FROZEN | PORTS-FRAGILE — the ONLY fully training-free audio-native indexer (CLAP+FAISS), but retrieval quality is poor. Proves audio-keying can be frozen; not that it retrieves well. |
| **SpeechRAG** (arXiv:2412.16500) | spoken open-QA (ASR-noise) | direct speech retrieval matches text baseline; beats cascade under high WER | COMPONENT | TRAINED-DEP — trains a speech adapter aligned to the text-retriever space; NOT "frozen speech-RAG". |
| **WavRAG** (arXiv:2502.14727) | spoken-dialogue audio-text QA | ~10× speed vs ASR→text-RAG at comparable quality | COMPONENT | TRAINED-DEP — trains a contrastive WavRetriever; hybrid audio-text KB keying. |
| **SpeechDPR** (arXiv:2401.13463) | open-domain spoken-passage retrieval | passage recall; robust when ASR poor | FT | TRAINED-DEP — HuBERT bi-encoder trained by distillation from a UASR+text-DR cascade. |
| **wav2graph** (arXiv:2408.04174) | KG node-classification / link-prediction from speech | GNN acc/F1 | FT | Confirms KG-from-speech is TRANSCRIPT-based + supervised — NOT audio-native. |
| audio-native KG / GraphRAG | — | — | — | **EMPTY** — no baseline surfaced in this scan (searched wav2graph, M3KG-RAG 2512.20136 [video-centric, directional/post-cutoff], and the speech-RAG family). Frame as under-explored, not provably empty; watch HippoRAG-2 (arXiv:2502.14802) and speech-KG follow-ons. |

### 1g. Vision comparator (mature multimodal-RAG organization)

| Representative baseline (id) | Benchmark | Headline metric | Train status | Applicability / role |
|---|---|---|---|---|
| **IBA / Ground-Then-Rank** (arXiv:2606.23881) | Encyclopedic-VQA / InfoSeek | IBA-Qwen 43.6 / 37.2; IBA-LLaVA 43.2 / 37.8 (per-variant) | FROZEN | **Pivotal** — fully training-free (frozen Qwen2.5-VL + off-the-shelf BGE-M3 reranker + frozen EVA-CLIP) and BEATS fine-tuned EchoSight (41.9/33.8) and ReflectiVA (38.6/36.4). Proves a frozen MLLM can CONSUME retrieved knowledge without FT and outperform fine-tuned systems — the vision analog of CB-RAG. |
| **KIRA** (OpenReview IlleFmPNb6) | Encyclopedic-VQA / InfoSeek | VQA acc, no task-specific FT | FROZEN | Second training-free vision positive (CLIP + question-relevance verification). |
| **EchoSight** (arXiv:2407.12735) | Encyclopedic-VQA / InfoSeek | rerank lifts R@1 13.3→36.5% (E-VQA); own abstract acc 41.8/31.3 (IBA's table reports 33.8 for InfoSeek) | MIXED | Trained reranker, frozen LLM — shows reranking is where the KB-VQA gain lives. |
| **ReflectiVA** (arXiv:2411.16863) | E-VQA / InfoSeek | E-VQA 38.6 / InfoSeek 36.4 | FT | Learned retrieve/no-retrieve reflection tokens — the trained gating contrast. |
| **Wiki-LLaVA** (arXiv:2404.15406) | E-VQA / InfoSeek | VQA acc | FT | Entity→article→passage hierarchical RAG (the MMWiki organization). |
| **ColPali** (arXiv:2407.01449) | ViDoRe | NDCG@5 81.3 vs 67.0 text+OCR | COMPONENT | Vision-native page-IMAGE late-interaction — preserves layout but REQUIRES a trained retriever (less training-free-clean than entity→text). |
| **VisRAG** (arXiv:2410.10594) | InfographicsVQA | end-to-end 25%→51% | MIXED | VLM-embedding page-image retrieval. |
| **mKG-RAG** (arXiv:2508.05318) | E-VQA 36.3 / InfoSeek 40.5 | COMPONENT | Multimodal KG + query-aware dual-stage retriever — best for multi-hop/schema-bound. |
| **MMGraphRAG** (arXiv:2507.20804) | CMEL/DocBench/MMLongBench | reported SOTA | unknown | Visual scene-graph + text-KG fusion via spectral-clustering entity linking. |
| **MuRAG** (arXiv:2210.02928) / **RA-VQA+FLMR** (arXiv:2309.17133) / **PreFLMR** (arXiv:2402.08327) | WebQA/MMQA; OK-VQA ~61%; M2KR | FT / FT / COMPONENT | The trained-retriever + fine-tuned-generator mainstream (baseline lineage). |

---

## 2. Multimodal knowledge-organization forms — which best supports a FROZEN omni consuming knowledge

The literature splits knowledge organization into keying regimes with very different frozen-consumption fit. The load-bearing inversion: **the RETRIEVER is the trained bottleneck across nearly every speech system; the frozen model's CONSUMPTION of a retrieved element (reading a text snippet / audio clip in-context) is the training-free-easy part.** So the TFRL budget belongs on utilization (gate/select/inject), not on making the frozen omni retrieve.

### Speech-primary forms (target)
1. **Lexical / text-keyed flat index** (CB-RAG/Siskos: MiniLM over a 466k-word vocab; SpeechRAG: text-query → audio-passage in a shared text-retriever space). **Strongest fit today.** Retrieval is fully training-free (CB-RAG) or near-frozen (SpeechRAG's small adapter), it currently RETRIEVES BEST, and the delivered element is a short text snippet the frozen omni reads natively.
2. **Audio-embedding-keyed index** (VoxRAG: CLAP+FAISS, training-free but weak R@10 0.34; SpeechDPR: HuBERT bi-encoder, trained). The truly audio-native, transcription-free form; preserves paralinguistic/acoustic content the transcript discards. Right long-horizon target, but retrieval-quality-limited unless the retriever is trained.
3. **Audio-native KG / GraphRAG** — **empty cell** (no baseline surfaced; under-explored, not proven-absent). wav2graph builds a symbolic KG from transcripts+NER; M3KG-RAG is video-centric via transcription. Nothing keys or reasons over graph structure on acoustic content.

### Vision comparator (mature; shows the achievable pattern)
- **Entity-keyed Wikipedia (the "MMWiki" pattern):** entity→article→section TEXT with an associated entity image (OVEN/InfoSeek/Encyclopedic-VQA; Wiki-LLaVA, EchoSight, ReflectiVA, mKG-RAG). A frozen omni consumes this MOST CLEANLY because the delivered element is TEXT (its native input) while the hard, modality-specific identification+reranking is offloaded to a DECORRELATED off-the-shelf retriever. IBA and KIRA prove this is training-free-consumable and can beat fine-tuned baselines.
- **Multimodal KG / GraphRAG** (mKG-RAG, MMGraphRAG): best for multi-hop / schema-bound queries where flat vector RAG collapses; consumption needs text-serialized traversal paths.
- **Vision-native page-image retrieval** (ColPali, VisRAG): preserves layout but requires a trained retriever — less training-free-clean.

### Ranking of forms by frozen-consumption cleanliness (speech-primary)
1. **Entity-keyed → text-section delivery** — cleanest, provably training-free-consumable (IBA/KIRA + CB-RAG evidence).
2. **Multimodal KG / GraphRAG** — best for multi-hop; needs a traversal element + text-serialized paths.
3. **Vision-native page-image** — layout-preserving but trained-retriever-dependent.
4. **Audio-native keying** — the on-thesis long-horizon form but immature (training-free = weak retrieval; strong retrieval = trained).

### Verdict on the best form for a frozen omni
Keep the external store as **entity-keyed TEXT sections**; drive retrieval / entity-ID / reranking from a **decorrelated off-the-shelf module** whose key can be the image, the omni's own transcript, or an audio embedding; deliver the retrieved TEXT into the frozen omni. For speech-primary, organize as a **hybrid text-audio store keyed text-primary for recall but preserving the audio payload** so the omni can extract paralinguistic content the transcript lost — and spend the TFRL budget on the injection-modality choice (text snippet vs raw audio) per query. Residual uncertainty / model-generation dependence: whether a 2026 frozen omni (a) needs the STRUCTURE at all vs a long-context flat dump, and (b) consumes structured in-context text well while its attention is split with the audio channel — both untested for this generation.

---

## 3. WS-3 same-principle verdict + closest baselines to benchmark

**Verdict: OCCUPIED-in-TEXT / ADJACENT-overall / ABSENT-in-speech-omni.** The exact principle — a FROZEN model whose external-knowledge USE is optimized at inference by a reward/selection/gating loop, no weight update, no retriever training — is well-populated in text but no single work occupies our strict intersection (**verifiable-reward × strictly-frozen × external-knowledge-selection**), and the speech/omni instantiation is an empty cell.

Why not a clean "occupied," after folding in verification corrections:
- **RTTC** (arXiv:2508.10024) — the closest text analog (a reward gates direct/RAG/TTT per query over a frozen model + frozen Qwen3-Embedding retriever), but **MIXED, not frozen**: its flagship gains route 60–76% of queries to a Test-Time-Training branch that LoRA-updates weights, and its reward is a **learned** reward model (Skywork-Reward-V2), not a verifiable reward. Benchmark against **only its frozen RAG-vs-direct routing branch**.
- **AdaRewriter** (arXiv:2506.01381) — Best-of-N reward-scored query reformulation over a frozen/black-box policy LLM, but it **TRAINS a contrastive reward model** → reclassify **trains-a-component**, not clean same-principle. It validates the best-of-N-over-frozen-policy SHAPE; our contribution must recover its lift with a verifiable/decorrelated reward that trains nothing.
- The **retrieval-gating cluster** (TARG 2511.09803, Decide-Then-Retrieve 2601.03908, SeaKR arXiv:2406.19215 / DRAGIN) is training-free and frozen but gates on **uncertainty**, not a reward selecting/injecting external knowledge — so the "reward-guided" half of the lever is under-occupied even in text.
- **Multimodal:** reward-guided best-of-N exists for reasoning (VL-PRM, arXiv:2509.23250) but **not** for RAG/knowledge-injection.
- **Speech/omni:** ABSENT. MARS and RASST train and rank by similarity (below).

### Closest baselines we would benchmark against (per lever)
- **Query-reformulation:** AdaRewriter (arXiv:2506.01381) — as a trains-a-component reference; ablate its trained RM → verifiable/decorrelated reward.
- **Retrieval-decision / gating:** RTTC (arXiv:2508.10024, frozen branch only) as head-to-head; TARG (arXiv:2511.09803) and Decide-Then-Retrieve (arXiv:2601.03908) as training-free-gating baselines.
- **Frozen multi-criteria reranking:** REBEL (arXiv:2504.07104).
- **Reward/feedback-selects-external-source, reader frozen:** Market-Feedback Adaptive Retrieval for Frozen LLMs (arXiv:2605.31201).
- **Multimodal reward-guided best-of-N reference point:** VL-PRM (arXiv:2509.23250).
- **Lower-bound lever:** plain best-of-N / RLVR selector (W1's mature machinery) — note this is oracle@N-bounded and was empirically null on this project's own tested surfaces, so treat pure best-of-N read-out over a fixed candidate set as a CONTROL, not the primary lever.
- **Speech contrasts (the cells we RAISE, not instances of our lever):** MARS (arXiv:2508.01166, conversational LLM-ASR context selection — FT, similarity-ranked); RASST (arXiv:2601.22777, **simultaneous speech TRANSLATION** with terminology retrieval — trains a cross-modal retriever; not ASR); CB-RAG/Siskos (arXiv:2509.19567) + VoxRAG (arXiv:2505.17326) as the frozen, **no-reward-loop** speech-RAG baselines our reward layer must beat.
- **Trained counterpoints (out-of-fence, cited as "what training buys"):** Search-R1 (arXiv:2503.09516), RRPO/RAG-reranker-RL (arXiv:2604.02091), RAG-Reward (arXiv:2501.13264 v1; **retitled OpenGenAlign in v2**), DynamicRAG.

---

## TFRL-controllable decision points (synthesis across families) + constraint check

Recurring decision points where a training-free reward lever plugs in, ranked by leverage for a frozen omni speech agent:
1. **Retrieve-or-not gate** (Self-RAG Retrieve / FLARE θ / TARG margin / SeaKR internal-state / CRAG router) — reward-select {retrieve, abstain}; adapts the trigger per item (FLARE proves a fixed high rate HURTS) and can withhold retrieval when low confidence is PERCEPTUAL not knowledge-based.
2. **Query / seed formulation** (IRCoT/Self-Ask/DRAGIN query; HippoRAG PPR seed selection) — **highest speech-specific leverage**: reward-select among ASR-hypothesis / entity-normalized variants to buffer the ASR-corrupted-query failure that otherwise compounds across hops.
3. **Injection-modality choice** (audio passage vs transcribed text) — the genuine multimodal-form lever; maps to the perception-delta object (serve text for lexical queries, raw audio for paralinguistic).
4. **Relevance grading / admission gate** (CRAG evaluator; Self-RAG IsRel) — replace the trained T5 with a frozen omni-as-judge / reward filtering distractors upstream — directly attacks the frozen-consumption bottleneck.
5. **Corrective-action routing** (CRAG Correct/Incorrect/Ambiguous → refine/web-search/both) — the lever that literally crosses the ceiling by bolting on external knowledge the frozen omni never had.
6. **Stop / iteration-depth** — reward-gated halting near an over-optimization budget N* (convergence-constraint frame); caps the latency that is the binding real-time constraint for voice.
7. **Support/utility rerank + final best-of-N** (Self-RAG IsSup/IsUse) — W1 machinery; weakest/oracle-bounded, and on the spoken half the audio judge is unreliable (LALM judges lag humans ~32pp).

Constraint check against the three project constraints
- **(1) Training-free:** every decision point is inference-time selection/gating/routing; no weights touched.
- **(2) Boundary-clean — CONDITIONAL, not categorical.** Boundary-cleanness holds ONLY IF the selection reward is a proxy / decorrelated verifier and NEVER the test gold answer or golden transcript. Two distinct failure modes to exclude per item (Information-Boundary Guard): **(a) gold leakage** — a hard boundary breach that manufactures fake gains (the owner's documented over-reach failure mode); **(b) self-reward decorrelation collapse** — a same-model self-judge on the same context is decorrelation-unsafe even with no gold peek (GraphRAG's own LLM-as-judge position/length bias is a live warning). Read the per-baseline "boundary-clean" tag as **conditional-on-proxy-reward**.
- **(3) New-info crosses the ceiling:** the external index injects information the frozen omni lacks; the reward selects/gates/injects it.

### Residual uncertainty and model-generation dependence (the crux)
The make-or-break Stage-1 question, flagged consistently across all findings: **whether a frozen 2026 omni (Qwen3-Omni) consumes in-context retrieved text/audio well enough that a training-free reward suffices where 2025-era speech-LLMs needed LoRA (MARS/RASST/VoxMind).** The vision comparator (IBA/KIRA beating fine-tuned systems) is an encouraging existence proof that a frozen strong MLLM CAN consume retrieved knowledge untrained — but it is vision, prior-generation, and text-query. The ASR-loss-into-query break is milder on a 2026 omni than the 2024-era survey evidence implies (Qwen3-Omni transcribes far better); the **latency and reward-reliability breaks are model-generation-independent**. TARG's "margin > entropy" is a directional hypothesis on prior-generation TEXT models (Qwen2.5/Llama-3.1), NOT same-generation confirmation for an audio-conditioned omni. All numbers here keep Stage-1 hypothesis grade until re-established at Stage 2.
