# 2026-07-11 · Survey Full Verification Pass (Ticket #28)

> **Nature**: Append-only verification-ledger update. Input = 89 new adversarial verification
> results (Opus web-finder pass) covering claims already catalogued in the step-2a (multimodal
> knowledge organization) and step-3a (training-free RL implementable candidates) survey decks.
> Ledgers updated: `wiki/survey/2026-07-09-step2a-verifications.json` (+42, now 63 entries incl.
> 1 batch-header) and `wiki/survey/2026-07-09-step3a-verifications.json` (+47, now 68 entries
> incl. 1 batch-header). **Existing entries preserved byte-for-byte** (git diff on both files is
> pure insertion, 0 deletions). **Not committed** — left for the owner/caller to commit.
>
> Track assignment for the 42 vs 47 split was by content match against the sibling
> `2026-07-09-step{2a,3a}-d{1..5}-*.json` claim decks (the input's `id` field, e.g. `d1-5`, is a
> per-file index that **collides across the two ledgers** — step2a's `d1..d4` and step3a's
> `d1..d5` are independent numbering spaces, not a single namespace). All 89 ids in this batch are
> disambiguated below by track prefix (`step2a-` / `step3a-`).

## 1. Counts by verdict per track

### This pass (89 new, 2026-07-11)

| Track | CONFIRMED | PARTIAL | REFUTED | UNVERIFIABLE | Total |
|---|---|---|---|---|---|
| step2a (d1 mmrag-systems / d2 knowledge-org / d3 loading-retrieval / d4 agentic-primitives) | 29 | 11 | 2 | 0 | 42 |
| step3a (d1 selection-topn / d2 verifier-rerank / d3 gating / d4 search / d5 rl-positioning) | 37 | 9 | 0 | 1 | 47 |
| **Combined (this pass)** | **66** | **20** | **2** | **1** | **89** |

### Ledger totals (prior 2026-07-09 pass + this pass)

| Track | CONFIRMED | PARTIAL | REFUTED | UNVERIFIABLE | Total |
|---|---|---|---|---|---|
| step2a | 16 + 29 = 45 | 4 + 11 = 15 | 0 + 2 = 2 | 0 | 62 (+ 1 batch-header entry = 63 array items) |
| step3a | 12 + 37 = 49 | 8 + 9 = 17 | 0 | 0 + 1 = 1 | 67 (+ 1 batch-header entry = 68 array items) |

Net effect: no REFUTED verdicts existed in either ledger before this pass; this pass introduces
the first 2 (both step2a) and the first UNVERIFIABLE (step3a). The prior pass's 0-REFUTED record
(loudly noted in both survey decks' headers, e.g. step3a's "0 REFUTED") **no longer holds** as a
combined-ledger statement — see §3 for whether either REFUTED claim was load-bearing anywhere.

## 2. Every REFUTED and PARTIAL claim, with its correction

Ordered by track, then id. "Support (gist)" is truncated; full evidence text is in the ledger
JSON under the matching `id`.

### 2.1 step2a track — 2 REFUTED

**step2a-d2-12 — REFUTED.** Claim: agent-memory frameworks have converged on an
episodic/semantic/procedural three-tier taxonomy.
> **Correction**: The two cited primary surveys do NOT converge on this triad. "Rethinking Memory
> Mechanisms of Foundation Agents..." (arXiv 2602.06052) uses a **5-type** cognitive taxonomy
> (sensory/working/episodic/semantic/procedural) crossed with substrate/subject axes. "Anatomy of
> Agentic Memory..." (arXiv 2602.19320) explicitly **rejects** the cognitive framing for a
> **4-category structure-oriented** taxonomy (lightweight-semantic / entity-centric /
> episodic-reflective / structured-hierarchical). The triad is a real cognitive-science construct
> but not what the field's surveys organize around.

**step2a-d4-18 — REFUTED.** Claim: prompting-based/training-free verifiers beat self-consistency
at lower k and cut tokens 1-3x, per arXiv:2510.25623.
> **Correction**: The cited source's finding is the **opposite**. 2510.25623 ("Evaluating the Role
> of Verifiers in Test-Time Scaling for Legal Reasoning Tasks") finds majority-vote/self-consistency
> **remains a strong baseline**, and verifier-guided selection gives **no benefit or a decrease**
> for larger generator models ("diminishing return of verification as the generator model's power
> increases"). It evaluates only **trained** reward models (ORMs/PRMs), not prompting-based
> verifiers, and reports no "1-3x fewer tokens" figure. Only the claim's secondary clause (Reason-
> and-Verify / FVA-RAG add faithfulness/falsification passes over RAG outputs) is accurate.

### 2.2 step2a track — 11 PARTIAL

**step2a-d1-11 (RASST simultaneous ST).** Correction: terminology-translation accuracy improves by
**up to ~16% absolute, not ~40%**. Multi-scale retrieval, train-to-decide-whether/when, +up-to-3
BLEU, and negligible retriever overhead all hold.

**step2a-d1-18 (Multimodal RAG survey audio section).** Correction: the audio-centric section
lists **11 papers, not exactly 5**. The five named (RECAST, WavRAG, SpeechRAG, SEAL, contextual-
ASR-with-RAG) are real and are the first five entries, but the section also includes RECAP,
Audiobox TTA-RAG, DRCap, P2PCAP, LA-RAG, CA-CLAP.

**step2a-d2-7 (NodeRAG).** Correction: the ~89% accuracy figure is NodeRAG's **HotpotQA** score
(89.50%), **not MuSiQue** (NodeRAG scores 46.29% on MuSiQue, with ~5,960 retrieval tokens). The
claim conflated the two datasets' numbers.

**step2a-d2-19 (HiRAG/ArchRAG cost tradeoff).** Correction: the offline-heavy/online-~zero-token
tradeoff is solid (primary), but the specific "$10-15 to index 800KB with GPT-4.1" figure is an
unconfirmed blog estimate, and "LightRAG 757M tokens on HotpotQA vs 62M naive" is unconfirmed in
any primary source and **inconsistent** with the closest primary measurement (TERAG reports
LightRAG ~44.6M tokens on HotpotQA, not 757M). Treat both numbers as unverified estimates.

**step2a-d2-20 (WavRAG / PlanRAG-Audio "flat hybrid indexes").** Correction: WavRAG is indeed a
flat hybrid text-audio index, but **PlanRAG-Audio is not** — it is a structured, time-aligned,
modality-partitioned relational store (SQL/CTE joins over transcript/speaker/emotion/sound-event
streams), not a flat index.

**step2a-d3-7 (LLMLingua-2 "training-free").** Correction: **LLMLingua-2 is not training-free** —
it is a token classifier **trained** via LLM-distillation (arXiv 2403.12968). The original
LLMLingua (perplexity-based) is the training-free method; LLMLingua-2 requires training (by its
own authors, upstream of any use here). The 3-6x speed, OOD robustness, and LongLLMLingua's
+17.1%@~4x (v1) figures are correct. **See §3 — this is a named step-2 grid arm.**

**step2a-d3-9 (Online-Optimized RAG for Tool Use gains).** Correction: gains are **not** a uniform
+3-9%; they range roughly **+1% to +9.5%**, with ToolRet-Web and FiQA at only ~+1-2%, and
MultiHopRAG's improvement is an end-to-end QA-accuracy delta (0.55→0.68), not a Recall@10/NDCG@10
number.

**step2a-d3-11 (hybrid search convex-blend vs RRF).** Correction: convex/linear score blending
**requires normalized (e.g. min-max) scores** — the claim had this backwards ("uses raw scores").
Mixing raw scores is the documented failure mode (BM25 unbounded vs cosine ∈[-1,1]). RRF's
no-calibration-needed property is correctly stated.

**step2a-d3-15 (agentic RAG retrieval-as-tool-call, "+15-20% quality lift").** Correction: the
mechanism (retrieval exposed as an agent tool-call; retrieval strategy as a learned RL policy) is
confirmed, but the specific "15-20% retrieval-quality lift over static configs" figure traces only
to vendor/blog syntheses — **no primary paper reports it**. Treat the magnitude as unsubstantiated.

**step2a-d4-12 (Deep Research survey "plan→search→synthesize→verify").** Correction: the cited
survey (arXiv 2508.12752) defines **four** stages — Planning / Question-Developing /
Web-Exploration / Report-Generation — with **no distinct verify stage** and **no citations agent**;
citation/attribution appears only as a future direction. Step-DeepResearch's atomic-capabilities
claim (planning, information-gathering, reflection, report-writing) is confirmed.

**step2a-d4-13 (RAGCap-Bench "~50x faster than WebThinker").** Correction: **no ~50x (or any)
speed/cost multiplier appears in the paper** — efficiency is asserted only qualitatively. Drop or
qualify the 50x figure; the four-capability taxonomy and correlation-with-downstream-QA findings
are supported.

### 2.3 step3a track — 9 PARTIAL (0 REFUTED)

**step3a-d1-13 (temperature/seed diversity collapse).** Correction: the "too-low temperature
collapses samples" mechanism is **misattributed** to arXiv 2502.11027 (DivSampling), which actually
proposes prompt-perturbation diversity and makes no temperature-collapse claim. The correct
attribution is arXiv 2510.02611 ("On the Role of Temperature Sampling in Test-Time Scaling"). The
calibration-is-the-bottleneck conclusion itself is correct.

**step3a-d2-4 (Pairwise/PairJudge RM knockout tournament).** Correction: the knockout mechanism
(n-1 comparisons, ~log n depth) is correct, but (a) PairJudge RM is a **supervised-fine-tuned**
reward model (PairJudge-432K, not 443K) — **not** a "prompted frozen model" — and (b) the
"all-pairs is stronger but O(N²)" claim is **not established** by the source (only named as an
untested future-work alternative).

**step3a-d2-6 (architecturally-diverse models decorrelate errors).** Correction: the cited paper
(arXiv 2510.20690, Neural Diversity / ND-LoRA) supports "reducing correlated errors governs
ensemble gain" but does **not** study cross-architecture decorrelation — its "diversity" is
decorrelated parallel LoRA streams **within one shared frozen backbone** (Barlow-Twins
regularized), not a comparison across distinct model architectures. **See §3 — touches the
δ_corr theory-hook grounding for the cross-model-verify lever.**

**step3a-d2-12 (AudioJudge per-dimension accuracy / correlation lift).** Correction: pairwise>
pointwise and audio-concatenation+few-shot gains are confirmed (up to ~0.91-0.93 Spearman), but
per-dimension audio-characteristic detection accuracy is **~55-74.5%, not 73-89%** (human ceiling
is only 76.2%). The "15-25% higher correlation vs traditional metrics" and "CoT significantly
raises agreement" figures are not established/measured quantities in the paper.

**step3a-d2-13 (ICR attention-reranking complexity).** Correction: ICR is O(1) (two forward passes
regardless of N) — correct — but the baseline comparison is **O(N)** forward passes for generative
listwise rerankers (e.g. RankGPT), **not O(N log N)**.

**step3a-d3-6 (Uncertainty-Aware Budget Allocation, UAB).** Correction: the per-question
uncertainty signal is **ANLL** (average negative log-likelihood), **not self-consistency
variance**; and there is **no** "stop when hardest-easiest gap < threshold" rule — allocation is a
two-round **concave-knapsack** solved by a marginal-greedy algorithm proven exact under KKT
conditions, not a greedy reallocation-with-stopping heuristic.

**step3a-d3-8 (conformal abstention family: PASC / SCOPE).** Correction: PASC (arXiv 2605.18812)
is **mischaracterized** — it is not a selective-risk-among-answered abstention gate but a
finite-sample guarantee that **all K stages of a multi-stage pipeline** are jointly covered.
SCOPE's guarantee is "error ≤ α under exchangeability" (marginal), not the PAC-style "probability
1-δ" the claim attributed to the family (that framing belongs to Learning-then-Test/conformal-risk-
control, not to PASC or SCOPE).

**step3a-d5-1 (s3 search-agent vs IRCoT margin).** Correction: the magnitude is overstated. s3
beats IRCoT-14B on the same frozen generator (Claude-3-Haiku) by **~+4.6 points (58.9 vs 54.7)**,
not +6.9pp vs an IRCoT average of 52.0 (no generator/IRCoT pairing in the paper produces 52.0
opposite s3's 58.9). All other specifics (frozen generator, RL-trained 7B searcher, Gain-Beyond-RAG
reward, 2.4k vs 170k/70k training examples) are correct.

**step3a-d5-7 (Adaptive-k "mitigates distractors / lost-in-the-middle").** Correction: neither
"distractor" nor "lost-in-the-middle"/"positional bias" appears anywhere in the paper. It frames
the benefit purely as avoiding under- or over-retrieval (up to 10x fewer tokens at equal-or-better
accuracy). Drop the distractor/positional attribution.

### 2.4 step3a track — 1 UNVERIFIABLE

**step3a-d1-15** — see §4 (待补).

## 3. Impact assessment against frozen decisions

Checked against `wiki/2026-07-10-step2-grid-draft.md` (the frozen step-2 34-arm/136-cell grid) and
`wiki/2026-07-09-step3a-tfrl-methods-survey.md` (the step-3 candidate-matrix framing), plus the
step-2a source survey `wiki/2026-07-09-step2a-mmknowledge-survey.md` that the grid draft cites for
its arm rationale.

**Two moderate-impact findings — documentation/citation fixes needed, no arm re-opened or
re-selected:**

1. **LLMLingua-2 is not training-free (step2a-d3-7).** The step-2 grid draft §2 (递送/delivery
   dimension) and the step-2a survey's "中成本裁决臂" list **both name this exact arm**:
   "LLMLingua-2 压缩注入（M 裁决臂）". LLMLingua-2's compressor is a token classifier trained via
   LLM-distillation, not the training-free perplexity-based method (that's the original
   LLMLingua). **This does not disqualify the arm** — we consume LLMLingua-2 as a frozen,
   off-the-shelf artifact and never train it ourselves, so "no weights changed by us" still holds
   — but the grid draft's characterization should be corrected from "training-free compression
   method" to "frozen pre-trained compressor (trained upstream by its authors, frozen at our
   inference time)" to avoid a category error when this arm is written up. Recommend the grid
   draft's §2 delivery-dimension text add a one-line footnote distinguishing "training-free by
   construction" (original LLMLingua) from "frozen but not training-free by construction"
   (LLMLingua-2), so any future write-up doesn't claim LLMLingua-2 as evidence for the project's
   training-free thesis.

2. **δ_corr grounding for the cross-model-verify lever (step3a-d2-6).** The step-3a candidate
   framing's lever-class table names `cross-model-verify | δ_corr | MERaLiON-2 + ASR-ensemble
   验证器臂` — i.e., the plan to use an architecturally-distinct model (MERaLiON-2) as a
   verifier explicitly to get error decorrelation from the 30B generator. The paper that was cited
   in the underlying candidate deck to support "architecturally diverse models decorrelate errors"
   (arXiv 2510.20690, Neural Diversity/ND-LoRA) does **not** establish that — it studies
   decorrelation **within** a single shared frozen backbone via parallel LoRA streams, not across
   distinct architectures. **This does not kill the cross-model-verify lever** (using a
   differently-trained model as an independent verifier remains a sound design instinct on general
   ensemble-diversity grounds), but the specific citation propping up the δ_corr theory-hook
   narrative needs replacing or softening — flag this as an assumption to verify empirically (a P3
   check item) rather than treat as literature-established when the theory doc / Lean convergence
   write-up next touches δ_corr.

**One cautionary (not decision-overturning) finding:**

3. **step2a-d4-18's reversal (verifier-guided selection vs self-consistency) is consistent with,
   not contradictory to, the already-frozen step-3 discipline.** The already-existing (pre-2026-
   07-11) step3a ledger entry for arXiv 2510.14913 (Budget-aware Test-time Scaling via
   Discriminative Verification) already distinguishes cheap discriminative verifiers (can add
   value) from expensive generative verifiers (need up to 8-128x compute to match
   self-consistency) — this new REFUTED finding (a different paper, on trained ORM/PRM reward
   models over legal MCQA, showing self-consistency remains strong and verifier gains shrink for
   larger generators) reinforces rather than undercuts the step-3 methodology's baked-in discipline
   of always running self-consistency/majority-vote as the mandatory baseline comparator for any
   verifier-based gating/reranking arm. No arm needs to change; this is a reminder to keep that
   baseline in every step-3 verifier experiment design, not a new requirement.

**No impact found (checked, ruled out):** step2a-d1-10 (Hearing-More, CONFIRMED) reinforces —
does not undercut — the grid's "retrieve-then-select 固定版" retrieval-strategy arm.
step2a-d3-11's convex-vs-RRF correction reinforces (does not undercut) the grid's choice of RRF for
the hybrid BM25+dense arm (RRF needs no calibration; convex blending would have needed score
normalization the grid never planned for). step2a-d2-12's REFUTED taxonomy claim and
step2a-d2-7/d2-19's PARTIAL corrections (NodeRAG, HiRAG/ArchRAG cost figures) touch only the
general "structural pedigree" evidence list in the step-2a survey, not the specific RAPTOR-lite/
HippoRAG-lite arm-choice citation (which draws on the already-verified, pre-existing RAPTOR/
HippoRAG-2 entries, untouched by this pass). step3a-d5-1's s3 magnitude correction (§2.3) only
updates a reference number in the D5 "RL-trained comparison-class" positioning table (explicitly
"not to be implemented, comparison only" per the step-3a survey) — no implementable arm changes.
All other PARTIAL corrections in §2 are citation-hygiene / implementation-detail fixes local to
their own candidate write-up and do not touch a named grid arm or candidate-matrix lever class.

**Bottom line: no REFUTED or PARTIAL claim in this 89-item pass requires re-opening the frozen
step-2 grid (ref-config, 34 arms/136 cells, H-a/H-b protocol) or the step-3 candidate framing's
lever-class table.** Two items (LLMLingua-2's training-free mischaracterization; the δ_corr
cross-model citation) need a documentation/citation correction next time those specific arms are
written up or implemented, and one item (the verifier-vs-self-consistency reversal) is a useful
reinforcement of an already-standing methodological discipline.

## 4. 待补 (UNVERIFIABLE — what was tried)

**step3a-d1-15** — Claim: no existing paper bundles self-consistency/majority-vote as a
training-free selection lever specifically for a frozen omni/audio-LLM doing QA (a negative-
existence / research-gap claim underpinning part of the step-3 thesis).

- **Verdict**: UNVERIFIABLE (absence-of-evidence claims cannot be conclusively proven from a
  literature sweep; this is expected and by design for research-gap claims, not a sweep failure).
- **What was tried**: adversarial web/arXiv searches crossing (speech-LLM OR audio-LLM OR
  omni-LLM) × (self-consistency OR majority-voting OR ensemble selection) × (QA) × (training-free
  OR frozen) × (2025-2026). No dedicated paper surfaced that performs this exact bundle.
- **Closest near-misses checked and ruled non-refuting**: AQA-TTRL (arXiv 2510.05478) uses
  majority voting only to build pseudo-labels for a test-time-RL **weight-updating** adaptation
  loop (not a frozen, training-free selection at inference); StableToken uses majority-voting for
  **quantization**, not QA answer selection; Ranked-Voting SC (arXiv 2505.10772) is text-only (no
  audio/speech modality).
- **Corroborating context**: the positive half of the claim (that the selection/voting/MBR
  machinery is well-established in text, VLM, and classical-ASR-ensemble work) is independently
  supported by several CONFIRMED entries in this same pass — CISC, USC, Ranked-Voting SC, RBoN
  (text); ROVER, ProGRes/H2T, GER/HyPoradise (ASR). So the gap claim is *consistent with* the rest
  of the survey even though it cannot itself be positively confirmed.
- **Next step if this needs to move past 待补**: this is exactly the kind of claim Stage-2
  (solution validation) is supposed to close by DOING the experiment rather than finding a paper
  that already did it — no further literature action is likely to resolve it; track it as "gap
  confirmed by absence of counterexample" and revisit only if a new 2026 paper surfaces in a future
  sweep.
