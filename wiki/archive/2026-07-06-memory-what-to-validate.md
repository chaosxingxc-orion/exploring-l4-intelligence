---
title: "From comparison to what-we-must-validate — assumptions + validation claims (WS-B seed)"
date: 2026-07-06
stage: 1-argumentation
status: "Stage-1 WS-A deliverable (workflow wf_fbbba6a0, 11 system + 2 verify + 2 synth agents; recovered via resume after a mid-run agent hang). Adversarial + citation verified; hypothesis-grade. Owner review pending; wiki-sync deferred."
---

> **LOG** — Stage-1 过程记录（hypothesis-grade），非现行真源；现行结论以 [[Decision-Log]] 与 [[Per-Work-Status]] 为准。

> ⚠️ **概念归档更正(2026-07-06).** 本文是**知识(Knowledge)元件**的验证契约(H0 headroom / H1 音频 key vs 转写 key / pillar-d 训练无关 RL 选择),曾错标为"记忆"。见 [[2026-07-06-capability-taxonomy-knowledge-skill-memory]] §5。**记忆(③ 实例召回)与技能(② 任务模板)未在此覆盖,需在新 taxonomy 下另立。**

I have everything needed: the locked design, the Information-Boundary Guard's four questions, the in-house perception-delta result (n=60: SQuAD-zh +0.283 SIG, MMAU-mini +0.117 n.s., VocalBench-zh 0.0 n.s.), and the 11-system comparison with its verification corrections. Here is the deliverable.

---

title: "From comparison to what-we-must-validate — the omni multimodal-memory WS-B seed"
date: 2026-07-06
stage: 1-design → 2-seed (argumentation; seeds the Stage-2 validation plan)
purpose: "Turn the 11-system organizational-form comparison into the explicit assumptions our locked memory design relies on, the validation claims (hypotheses) we must test in priority order with concrete measurable outcomes, and — per claim — the cleanest controls separating a genuine multimodal-memory effect from a text/lexical-retrieval effect (audio-distinctness) and from leakage (external knowledge vs the test answer)."
references: ["2026-07-05-omni-multimodal-memory-design", "Information-Boundary-Guard", "2026-07-06-omni-agentic-systems-survey"]

---

# From comparison to what-we-must-validate (WS-B seed)

> **Frame.** The comparison ([[2026-07-05-omni-multimodal-memory-design]] + the 11-system survey) tells us *where the field organizes memory* and *where our locked cell differs*. This doc converts that into a validation contract: (A) the assumptions our design silently rests on, (B) the claims we must test in priority order with measurable outcomes, and (C) for each, the control that isolates a real cross-modal-memory effect from plain text retrieval and from leakage. It **seeds** the Stage-2 plan; every number below is a target to be established at Stage-2 power (paired-bootstrap CIs, prereg), not a result. All 11 systems are cited by real arXiv ID / repo in the appendix.

## 0. Where the field's memory sits vs our locked cell (comparison, corrected)

Every surveyed store selects and writes memory by **LLM heuristic** (mem0 `2504.19413`; MemGPT/Letta `2310.08560`; Zep/Graphiti `2501.13956`; Generative Agents `2304.03442`; LangMem `github.com/langchain-ai/langmem`; A-MEM `2502.12110`, primary repo `agiresearch/A-mem`, eval repo `github.com/WujiangXu/A-mem`; Cognee/Memary) **or by supervised contrastive/distillation training** (WavRAG `2502.14727` — InfoNCE; SpeechRAG `2412.16500` — cosine-distillation). Two of the eleven are **benchmarks that persist nothing** (AudioMC `2512.14865`; MTalk-Bench `2508.18240`) and are therefore **excluded from store-level adjudication** — they re-enter only as downstream knowledge-floor yardsticks (§C).

Folding the verification pass, we must **not** state the novel cell at the altitude of "a cross-modal speech-key → text-value store": that bare element is **already realized** by WavRAG's Speech→Text scenario with a **frozen generator**. The cell that survives an element-oriented counterexample hunt is the narrow **conjunction** of three properties, none of which any surveyed system holds together:

1. **A frozen, *untrained* speech key.** WavRAG LoRA-tunes its Qwen2-Audio retriever (rank 8) and SpeechRAG trains a HuBERT adapter — so *training-free keying* is the true load-bearing distinction, not cross-modality per se.
2. **Value organized as a `{(task, language) → external-knowledge text}` DICT** with W4-disentangled per-task sub-keys as fallback — no surveyed system (audio or text) has task×language addressing.
3. **Reward-guided, training-free (RL) selection** among Compression / Retrieval / Usage — **the single wholly-unrefuted differentiator**: no system, heuristic or supervised-trained, uses a verifiable-reward loop to choose memory actions. Given the project thesis is literally "training-free RL," this **leads** the novelty argument.

**Two nearest non-refuting precedents to keep in view:**
- **AFA (`2604.25022`) — closest *structure*.** A speech-derived key → text store, mostly training-free. It does **not** refute us, on three verified grounds: (i) it keys by **speaker identity collapsed to a discrete User-ID** (exact-match route, not a continuous content/task embedding); (ii) its value is the **user's own history** (personalization), not external knowledge; (iii) its top config **LoRA-tunes LLaMA-2-70B** (partial training-free). It is a "who"-keyed personalization memory, orthogonal to our "what/which-task"-keyed external-knowledge memory — and its persona-confusion failure mode is a useful cautionary analog for our leakage boundary.
- **WavRAG (`2502.14727`) / SpeechRAG (`2412.16500`) — closest *cross-modal retrieval*.** They establish, importantly for us, that **audio-native retrieval beats the ASR→text cascade specifically in high-WER / noisy / paralinguistic-dependent regimes, and only reaches near-parity in clean, low-WER speech.** This makes our central audio-distinctness claim (H1) *conditional*, and its operating regime is the thing to map. SpeechRAG's lock-in fact — retriever adapter is *trained*, generator frozen — is a full-paper/GitHub citation, not abstract-level; it is what preserves our training-free distinction and must be cited directly.

Minor corrections folded: Cognee documents audio as an *ingestible* format but processes it to text/graph — it has **no speech-native retrieval key**, so it remains text-keyed in our sense. The AudioMC "Scale AI / SEAL" attribution is **provenance-inferred** (dataset namespace + leaderboard), not stated in the abstract. MTalk-Bench's "9 capabilities / ~270 dialogues / 3-turn" details are **full-paper-only** and to be re-verified before citation.

**Novelty verdict, stated honestly:** *no existing system refutes the full locked conjunction* — this is **absence-of-evidence under element-oriented search limits**, not a proof of non-existence. It cannot be upgraded to "confirmed novel" here.

## A. Explicit assumptions our design relies on that are not yet established

| # | Assumption | Why it is load-bearing | Current status |
|---|---|---|---|
| **A1 — Headroom** | A boundary-clean knowledge gap exists (the TH2a floor / T5 knowledge-gap component) that *prompt-injected external text* can close — the omni fails items for lack of a fact/handling-pattern, not for lack of perception it already has. | If the gap is small, or the model "knows but can't express" (a read-out problem, not a knowledge problem), the whole new-info engine is pointless. | **Unestablished.** T5 posits the gap; its *closable-by-injection* size is unmeasured. |
| **A2 — Audio-distinctness (cross-modal necessity)** | The compressed **speech** key carries retrieval-relevant signal *beyond* the omni's **own deployable transcript** — audio-keying retrieves better knowledge than transcript-keying. | This is what separates us from ordinary ASR→text RAG (WavRAG/SpeechRAG). If false, "multimodal memory" collapses to text retrieval. | **Conditional / weakly directional.** Field says advantage concentrates at high WER. In-house perception-delta (n=60, Stage-1) is *consistent but task-dependent*: SQuAD-zh +0.283 SIG, MMAU-mini +0.117 n.s., VocalBench-zh 0.0 n.s. |
| **A3 — Retrievability** | For a query, a relevant external entry *exists* in the store and the compressed key retrieves it at usable precision@k (task-relevant neighbors, not merely *acoustically* similar ones — the design doc's own worry). | Retrieval is the middle link; noise here caps everything downstream. | **Unestablished.** Corpus coverage and key discriminability untested. |
| **A4 — Compression fidelity** | Compressing the long speech embedding to a compact key preserves the task/knowledge-relevant signal (compression is *mandatory* per owner). | Compression is strategy #1; if it destroys the retrieval signal, the unified-key path fails. | **Unestablished.** Degradation-vs-ratio curve unknown. |
| **A5 — Injection utility** | Prepending the retrieved facet nets **positive** — the frozen omni reads and uses correct knowledge and is not derailed by imperfect/irrelevant hits. | Usage is strategy #3; retrieval noise can make injection net-negative. | **Unestablished.** |
| **A6 — (task,language) addressability** | Knowledge is well-organized as `{(task,language)→text}` and the query's facet is **inferable from audio** to route retrieval; partitioning beats a flat store. | This is the value's whole structure and the routing assumption. | **Unestablished.** Facet-inference accuracy and partition benefit unmeasured. |
| **A7 — Disentanglement fallback** | If the unified key is not task-relevant enough, W4-disentangled per-task sub-keys recover task-relevant retrieval. | This is the declared fallback lever; it must actually help. | **Unestablished** (W4 sub-key separability is itself a W4 open item). |
| **A8 — Reward-guided selection (thesis pillar)** | A **verifiable, leakage-free** reward can guide training-free selection over {compress, retrieve, inject} and beat the best fixed policy — *without over-optimization*. | This is our sole unrefuted differentiator and the "training-free RL" thesis. Per the Theory track it needs explicit constraint terms (KL trust-region / N* budget) to *converge*, not merely to exist (`proofs/tfrl/`). | **Unestablished** (design-stage). |
| **A9 — Separability (external ≠ answer)** | Helpful external knowledge exists that is genuinely distinct from the test item's transcript/answer — knowledge specific enough to help is *not* automatically specific enough to leak. | The Information-Boundary Guard's whole legitimacy rests here; my documented failure mode is fake gains from boundary over-reach. | **Unestablished empirically** — the line's location is exactly what a leakage control must find. |

## B & C. Validation claims in priority order — with measurable outcomes and controls

**Reusable control primitives** (defined once; referenced per claim). The first three isolate **audio-distinctness**; the last four isolate **leakage**.

- **CP-Transcript-key (audio-distinctness).** Identical store + retrieval + injection, but the **key = embedding of the omni's *own deployable* transcript** (never the gold transcript — Guard Q1/Q3). This is the deployable analog of the perception-delta harness. *If the audio key does not beat this, the effect is lexical/text retrieval, not cross-modal.*
- **CP-Acoustic-swap / WER-strata (audio-distinctness).** Hold transcript content fixed, vary the acoustics (different speaker, added noise, TTS re-render) and **stratify results by ASR WER band**. Invariance to acoustics ⇒ no audio-distinct signal beyond content; a helpful, acoustics-tracking delta concentrated in high-WER/paralinguistic strata ⇒ the cross-modal signal is real (matches WavRAG/SpeechRAG's predicted regime).
- **CP-Mismatched-injection placebo (audio-distinctness + retrieval-specificity + leakage).** Inject a value retrieved for a **different** query. If accuracy still rises, the gain is generic priming / prompt-format / leakage, **not** query-specific cross-modal retrieval.
- **CP-Provenance firewall (leakage).** Store built **only** from training/source corpora with all eval items *and their answers/transcripts* held out; audited so no eval golden entered the store. Operationalizes Guard Q3.
- **CP-Answer-overlap audit (leakage).** Measure n-gram / entailment overlap between each injected value and the gold answer; flag+remove high-overlap entries; **re-run** — the gain must survive removal.
- **CP-Gold-answer-injection ceiling (leakage bound).** Inject the gold answer text directly = the **leakage upper bound**. Our external-knowledge gain must be a *fraction* of this **and** achieved with the answer string absent from the injected value.
- **CP-Oracle-retrieval ceiling (headroom, not leakage).** Inject the *known-correct* external entry (perfect retrieval) = upper bound on what any retrieval could deliver; separates "no headroom" (A1 fails) from "retrieval too weak" (A3 fails). This is a diagnostic ceiling, not a deployable lever.

All end-task deltas are reported as **paired-bootstrap 95% CIs on ≥150 held-out items** (the M3-powered n), plus retrieval **precision@k / recall@k of the gold knowledge entry** where retrieval is under test. Candidate surfaces: SQuAD-zh, MMAU-mini, VocalBench-zh (in-house perception-delta sets), Spoken-SQuAD & SLUE-SQA-5 (WavRAG surfaces), MINDS-14 (SLU).

---

**Claim H0 — Headroom exists and is closable by injection.** *(prerequisite; if it fails, stop.)*
Injecting the correct external-knowledge entry raises the frozen omni's accuracy on items it otherwise fails.
- **Measurable:** accuracy(oracle-retrieval injection) − accuracy(no injection) > 0 with a CI excluding 0, on a boundary-clean held-out set; report the *fraction of the T5 knowledge-gap* it recovers.
- **Audio-distinctness control:** none needed yet — H0 is modality-agnostic (it establishes *whether there is anything to win*).
- **Leakage control:** **CP-Provenance firewall** + **CP-Answer-overlap audit** + **CP-Gold-answer-injection ceiling**. The oracle entry is *external knowledge*, not the answer; the gold-answer ceiling bounds how much of any gain is mere answer-containment. Uses **CP-Oracle-retrieval ceiling** as its own instrument.

**Claim H1 — Audio-distinctness / cross-modal necessity.** *(the crux; distinguishes us from ASR→text RAG.)*
Keying on the compressed **speech** embedding improves answers **more** than keying on the omni's own **deployable transcript**, over the same store.
- **Measurable:** [accuracy(audio-key) − accuracy(transcript-key)] CI > 0 **and** precision@k(audio-key) > precision@k(transcript-key); report the delta **per WER band** to map the operating regime (we *predict* the advantage concentrates at high WER, near-parity in clean speech).
- **Audio-distinctness control:** **CP-Transcript-key** is the primary comparator; **CP-Acoustic-swap / WER-strata** confirms the delta is driven by acoustics, not residual content; **CP-Mismatched-injection placebo** rules out generic priming.
- **Leakage control:** the transcript baseline must use the **system's own ASR, never the gold transcript** (Guard Q1/Q2 — a gold-transcript baseline would both leak and *understate* audio's value, the exact M3 trap). Plus **CP-Provenance firewall**.
- **Directional prior (Stage-1, hypothesis-grade):** perception-delta harness `scripts/p6_perception_delta.py` (n=60) — SQuAD-zh +0.283 (CI [0.133, 0.433], SIG), MMAU-mini +0.117 (n.s.), VocalBench-zh 0.0 (n.s.). This tests the **perception floor** (omni reads audio vs its own transcript), which is *upstream of and distinct from* retrieval-key distinctness — supportive but not a substitute for H1's retrieval test, and non-significant on 2/3 sets.

**Claim H2 — Compression preserves the retrieval signal.** *(feasibility of strategy #1.)*
A compressed unified speech key retrieves acceptably close to the full/uncompressed embedding.
- **Measurable:** precision@k and end-task accuracy as a function of compression ratio; locate the knee where the CI first excludes parity with the uncompressed key.
- **Audio-distinctness control:** re-run **CP-Transcript-key** at each compression level — the audio-vs-transcript advantage (H1) must persist post-compression, else compression has thrown away exactly the cross-modal signal.
- **Leakage control:** **CP-Provenance firewall** (unchanged); compression is a key-side operation and adds no new leakage surface, but the audit is repeated because a lossy key could collapse distinct items and *route* to a leaking neighbor — check via **CP-Answer-overlap audit** on what is actually retrieved.

**Claim H3+H4 — Retrieval hits and injection nets positive (end-to-end mechanism).** *(strategies #2–#3 working together.)*
The compressed key retrieves the needed `(task,language)` facet at usable precision, and injecting it improves the frozen omni **net of retrieval noise**.
- **Measurable:** recall@k of the gold entry ≥ target; and accuracy(retrieve-and-inject) − accuracy(no injection) CI > 0 — crucially **larger than 0 even when averaged over misses** (net-positive, not just conditional-on-hit).
- **Audio-distinctness control:** **CP-Transcript-key** end-to-end; **CP-Mismatched-injection placebo** (injecting a *wrongly-retrieved* facet must **not** help — if it does, the "gain" is format/priming, not retrieval).
- **Leakage control:** **CP-Answer-overlap audit** on the *actually injected* text (re-run after removing high-overlap entries); **CP-Gold-answer-injection ceiling** to bound the injected-content contribution; **CP-Provenance firewall**.

**Claim H5 — Reward-guided training-free selection beats the best fixed policy.** *(the thesis pillar / novelty lead; validation-dependent on H0–H4.)*
A verifiable-reward selector over {compress, retrieve, inject} beats (a) always-retrieve-and-inject, (b) never-inject, and (c) random action selection, on held-out data.
- **Measurable:** accuracy(reward-guided) − accuracy(best fixed policy) CI > 0 on **held-out** items (not the reward-tuning split); plus a stability check that gains do **not** collapse under an over-optimization budget cap (ties to the Theory track's required KL trust-region / N* constraint — a *convergence* result, not a static identity, per `proofs/tfrl/`).
- **Audio-distinctness control:** the fixed-policy comparators must run on the **same audio-keyed store**, so any selector gain is attributable to *selection*, not to re-introducing the cross-modal signal; keep **CP-Transcript-key** as an orthogonal check that the selector isn't merely learning "prefer transcript."
- **Leakage control:** **the reward must be verifiable *without* the gold** (math re-check / format / consistency / KB-agreement — Guard's ✅ examples), computed at deploy-time; confirm the reward never reads the test item's answer. Report the reward's own answer-correlation to prove it isn't a disguised oracle (**CP-Answer-overlap audit** applied to the reward signal).

**Claim H6 — Disentanglement fallback and (task,language) partition add value.** *(conditional; test only if H1 holds but the *unified* key under-performs on task-relevance.)*
W4-disentangled per-task sub-keys and `(task,language)` partitioning+routing beat the flat unified store.
- **Measurable:** per-task accuracy(sub-key routing) vs (unified key); accuracy(partitioned+audio-inferred routing) vs (flat store); plus standalone **(task,language)-from-audio inference accuracy**, with an **oracle-routing ceiling** to separate "partition helps" from "we can infer the partition."
- **Audio-distinctness control:** sub-keys and facet-routing must be derived from **audio only** (Guard Q1); compare each against its **CP-Transcript-key** analog (transcript-derived facet inference) to show the routing benefit is cross-modal, not lexical.
- **Leakage control:** **CP-Provenance firewall** + **CP-Answer-overlap audit** on the facet actually injected.

**Priority rationale.** H0 is logically prior (no headroom ⇒ no project). H1 is the **crux** and the field's evidence says it is *conditional* — so it is the highest-information test and the one most likely to force a scope decision (which task/WER regime we own). H2–H4 verify the three strategies actually work end-to-end and net-positive. H5 is our **novelty lead** but is only meaningful once H0–H4 establish a working, boundary-clean mechanism to select over. H6 is a conditional fallback, gated on H1 holding while the *unified* key disappoints.

## Residual uncertainty (marked)

- **Novelty is absence-of-evidence, not proof.** The element-oriented counterexample hunt cannot exclude an unpublished or differently-named system; the surviving cell is the *conjunction* (frozen-untrained key + `(task,language)` dict + disentangled sub-keys + reward-guided selection), with AFA (`2604.25022`) and WavRAG (`2502.14727`) as the nearest non-refuting precedents.
- **A2/H1 is the fragile assumption.** External evidence makes the audio-key advantage *regime-dependent* (high-WER/paralinguistic), and the in-house perception-delta is **n=60, Stage-1, significant on only 1 of 3 sets** — hypothesis-grade only. A negative or clean-speech-only H1 result would rescope the engine, not kill it (it would still own the noisy/paralinguistic regime).
- **Two "systems" are benchmarks, not stores** (AudioMC `2512.14865`, MTalk-Bench `2508.18240`) — excluded from store-level adjudication; usable only as downstream knowledge-floor / multi-turn-recall eval targets. MTalk-Bench's capability/dialogue-count details are full-paper-only and unre-verified.
- **Minor citation notes folded:** A-MEM eval repo is `github.com/WujiangXu/A-mem` (not `.../AgenticMemory`); Cognee ingests audio but has no speech-native key; AudioMC's "Scale AI" attribution is provenance-inferred. WavRAG's frozen-encoder/LoRA-retriever (r=8) and SpeechRAG's trained-adapter/frozen-generator facts are the load-bearing training-free distinctions and must be locked to full-paper/GitHub citations.
- **H5 convergence is a theory obligation, not just an empirical one** — the reward-guided selector must be paired with an explicit constraint (KL trust-region / N* budget) and a *convergence* proof under the Theory track, or it reduces to a tautology-where-proven.

## Appendix — system → source (all real; on-topic verified)

| System | arXiv / repo | Role in adjudication |
|---|---|---|
| mem0 / mem0^g | `2504.19413` · `github.com/mem0ai/mem0` | text store; heuristic ADD/UPDATE/DELETE/NOOP |
| MemGPT / Letta | `2310.08560` · `letta-ai/letta` | text; tiered self-editing memory-as-tool |
| Zep / Graphiti | `2501.13956` · `getzep/graphiti` | text; bi-temporal knowledge graph |
| Generative Agents | `2304.03442` · `joonspk-research/generative_agents` | text; relevance×recency×importance + reflection |
| LangMem | `github.com/langchain-ai/langmem` | text; semantic/episodic/procedural typing |
| A-MEM | `2502.12110` · `agiresearch/A-mem` · eval `WujiangXu/A-mem` | text; Zettelkasten linking + evolution |
| Cognee / Memary | `topoteretes/cognee` · `kingjulio8238/Memary` | text/graph; **audio ingested but no speech key** |
| **AFA** | `2604.25022` | **closest structure**; speaker-ID→own-history, LoRA-partial — non-refuting |
| **WavRAG** | `2502.14727` (ACL 2025 Long #613) | **closest cross-modal retrieval**; frozen generator, **LoRA-trained retriever (r=8)** |
| **SpeechRAG** | `2412.16500` (ICASSP 2025, Amazon) | text-query→audio-value; **trained adapter**, frozen generator; audio-RAG beats ASR→text at high WER |
| AudioMC | `2512.14865` | benchmark (no store) — excluded; downstream eval target |
| MTalk-Bench | `2508.18240` | benchmark (no store) — excluded; downstream eval target |

Internal: locked design [[2026-07-05-omni-multimodal-memory-design]]; [[Information-Boundary-Guard]]; perception-delta `scripts/p6_perception_delta.py` → `_repro/p6_perception_delta.json`; theory `proofs/tfrl/`.
