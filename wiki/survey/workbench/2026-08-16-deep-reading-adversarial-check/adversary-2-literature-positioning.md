# Adversary 2 — Literature Positioning

Role: hostile-reviewer attack on the surviving SAEA plan (N1 routing gate, N2 targeted-supply block at
n=44, DEMO lane), using the four cluster digests (A RECOVER, B metrics/memory, C biasing/supply,
D copying/verification) as armory, plus a bounded independent web sweep to find priors the clusters
missed.

Session: 2026-08-16, ~21:11–21:17 local. Repositories read-only; nothing under `studies/` touched;
no git commands run. This file is the only file this agent wrote.

---

## 1. Fetch log

Every query/URL, timestamp, one-line result. Tool = WebSearch (WS) or WebFetch (WF).

| # | Time | Tool | Query / URL | Result |
|---|------|------|-------------|--------|
| 1 | 21:11 | WF | `https://arxiv.org/abs/2607.26410` | Voice Memory confirmed: Yang, Z-C. Chen, Zelasko, Zhehuai Chen, Balam, Ginsburg; 2026-07-29; "Preprint. Technical report and open source available on Hugging Face" (`huckiyang/voice-memory`). Numbers as in Cluster B: 64%→35% over-correction, 8.36→7.52 weighted WER, ATIS 8.40→3.40, CHiME-4 12.69→10.46. |
| 2 | 21:11 | WF | `https://arxiv.org/abs/2607.21943` | "Listen, Do Not Copy: Internalizing Audio-Grounded Scaffold Context for Robust Omni-Model Speech Understanding"; Pengfei Zhang, Biao Tian, Tianxin Xie, Minghao Yang, Xiangang Li, Li Liu; v1 2026-07-24, v2 2026-07-29; 9pp, 4 figs; no code link in abstract page. Confirms AGSC 3-stage: build clues w/o revealing answers → answer-overlap + **silence** leakage tests → remove clues at inference. mpWER 25–71% → 9–15%. |
| 3 | 21:12 | WF | `https://arxiv.org/html/2607.26410v1` | Voice Memory internals: ρ = (WER_1best − WER_ŷ)/(WER_1best − WER_oracle); HER = fraction of token edits that are harmful. **Abstain is rule-text in `memory.md`, not a per-utterance model decision.** Memory built on disjoint train/selection/test with a score-gated optimizer accepting edits only on strict held-out improvement (gold used for scoring). Domains = HyPoradise 10 (atis, wsj, chime4, cv, lrs2, coraal, td3, ls_other, ls_clean, swbd) + CHiME-4, VoiceBank-DEMAND, LS+FreeSound, NOIZEUS, CoVoST-2, FLEURS. **No Earnings21, no entity/keyword corpus. Corrector sees N-best text only, never audio. No entity rosters.** |
| 4 | 21:12 | WS | `arXiv August 2026 speech-conditioned contextual biasing frozen omni LLM training-free entity retrieval` | Surfaced two priors absent from all four cluster digests: **2603.25460 CLAR** (CIF-localized speech-text retriever) and **2604.12398** (IBM, bias-word *position prediction* from acoustic cues). Also re-surfaced 2512.21828 (GLCLAP+GRPO, already in Cluster C). |
| 5 | 21:13 | WF | `https://arxiv.org/abs/2604.12398` | IBM (Novitasari, Fukuda, Kurata, Saon), 2026-04-14, IEEE copyright line. Acoustic cues from **common words with similar pronunciation** to target bias words; **bias-word positional prediction via multi-output learning**; 16.3% bias-word error reduction incl. out-of-domain. Multi-output learning ⇒ trained. |
| 6 | 21:14 | WF | `https://arxiv.org/html/2603.25460v1` | CLAR (BRVoice/Bairong, 2026-03-26). Dual-tower CLAP: Paraformer speech encoder + Chinese-RoBERTa text encoder, **both trained**, CIF quantity constraint, global+local contrastive loss. Query = **audio** (log-mel → frame-level hiddens) matched to hotword text embeddings. Top-K hotwords prepended as text prompt; **Speech LLM (Step-Audio2-mini) LoRA-fine-tuned**, CLAR frozen at inference. AISHELL-1-NE: CER 0.92, B-WER 2.78, retrieval F1 97.03. Table 3: false-positive hotwords perturb non-bias decoding (U-CER →1.03/1.01). |
| 7 | 21:14 | WS | `"Earnings-21" contextual biasing entity WER 2026 frozen LLM prompt roster deployment-legal metadata` | Surfaced **2604.07354 Contextual Earnings-22** — a 2026 benchmark with custom vocabulary on our own sister corpus key. Not in any cluster digest. |
| 8 | 21:15 | WF | `https://arxiv.org/html/2604.07354v1` | Argmax Inc. + UCLA, 2026-03-28, CC BY-SA 4.0, "code and dataset released upon acceptance". **Vocabulary built by GPT-5 NER over the Earnings-22 gold transcripts** (person/company/product). Val 130 samples / 134 unique keywords; test 630 samples / 738 unique keywords / 46 files. Systems: Deepgram Nova-3, Whisper-1, AssemblyAI (prompting); Whisper large-v3-turbo, NVIDIA CTC-WS, Argmax Parakeet-v2+CTC-WS (boosting). Metrics WER + keyword P/R/F. **"Local context is systematically easier"; "global context primarily stresses precision"; distractor-induced false positives; hallucination / partial output / language switching when the keyword list perturbs decoding.** Notes ConEC's lists come "largely from external sources (slides, earnings releases, participant metadata)". |
| 9 | 21:15 | WS | `selective contextual biasing decide when to bias ASR gating detector rare word likely present utterance-level` | Establishes that **utterance-level bias gating is settled prior art**: Nature Sci Rep 2025 s41598-025-12121-4 "adaptive context biasing" with a **bias detector over encoder features** deciding whether a segment needs biasing; plus entity detectors / confidence-activated decoders that enable-disable biasing per utterance. Also surfaced 2605.18222 CTC-WS streaming. |
| 10 | 21:15 | WS | `"omni" speech LLM context copying perception bypass replication August 2026 negative result prompt mitigation` | No newer replication than 2607.21943. Confirms 2607.21943 also ships **gate-only training ("learns whether and when to use a clue")** and a **Context-Speech Bench covering gating**. Surfaced OmniACBench 2603.23938 (context-grounded acoustic control) as adjacent. |
| 11 | 21:16 | WF | `https://www.nature.com/articles/s41598-025-12121-4` | 303 redirect to `idp.nature.com` authorize interstitial — not followed (no logins). Bias-detector claim therefore rests on the search-result summary at row 9; **flagged as unverified-at-source, do not cite from this file without a first-hand read.** |
| 12 | 21:16 | WF | `https://arxiv.org/abs/2605.18222` | Tsai, Lo, Sun, Chen; 2026-05-18/19. Streaming CTC-WS: keywords detected **directly from CTC log-probabilities**, stateful token passing across chunks, incremental commitment. Abstract verbatim: "does not require modifications to the underlying acoustic model or additional training". ⇒ **A training-free, acoustically-conditioned keyword router already exists — but it needs frame-level CTC posteriors.** |
| 13 | 21:16 | WS | `llama.cpp llama-server API logit_bias n_probs logprobs parameters completion endpoint` | llama-server exposes `logit_bias` (per-token bias, string form supported, `false` = hard ban) and `n_probs` / `top_probs` (top-N per generated token). ⇒ **Our own serving stack does expose logit control over output text tokens.** |

Sources used, as markdown links:
[2607.26410 abs](https://arxiv.org/abs/2607.26410) ·
[2607.26410 html](https://arxiv.org/html/2607.26410v1) ·
[2607.21943 abs](https://arxiv.org/abs/2607.21943) ·
[2607.21943 html](https://arxiv.org/html/2607.21943v1) ·
[2603.25460 CLAR](https://arxiv.org/html/2603.25460v1) ·
[2604.12398 IBM](https://arxiv.org/abs/2604.12398) ·
[2604.07354 Contextual Earnings-22](https://arxiv.org/html/2604.07354v1) ·
[2605.18222 streaming CTC-WS](https://arxiv.org/abs/2605.18222) ·
[2509.19567 Siskos](https://arxiv.org/html/2509.19567) ·
[2603.16411 RECOVER](https://arxiv.org/pdf/2603.16411) ·
[Nature adaptive context biasing (unverified, paywall redirect)](https://www.nature.com/articles/s41598-025-12121-4) ·
[llama.cpp server README](https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md)

---

## 2. Three priors the cluster digests missed

These are the load-bearing additions from this sweep. All three land on the conjunct the clusters
unanimously called our strongest survivor.

**(i) CLAR, arXiv 2603.25460 (Bairong, 2026-03-26).** A *speech-conditioned* hotword retriever:
audio → frame-level hiddens → CIF-localized alignment → contrastive match against hotword text
embeddings → top-K injected as a text prompt to a Speech LLM. This is SAEA's C2 mechanism drawn as
an architecture diagram, published five months ago. Escape hatch: the retriever is fully trained
(dual-tower contrastive + CIF constraint) and the consumer is LoRA-fine-tuned. It is not in our
regime, but it removes any claim that *the idea* of selecting supply from the speech signal is new.

**(ii) IBM 2604.12398 (Novitasari, Fukuda, Kurata, Saon, 2026-04-14).** "Bias word **position
prediction** via multi-output learning" — i.e. predict *where* a bias word occurs from acoustic
cues, without G2P. This is N1's routing signal, learned. 16.3% bias-word error reduction including
out-of-domain. Again trained, again an idea-level pre-emption of the routing framing.

**(iii) Contextual Earnings-22, arXiv 2604.07354 (Argmax + UCLA, 2026-03-28).** A 2026 contextual-ASR
benchmark **on our own locked corpus key `earnings22-original`**, CC BY-SA 4.0, harness promised.
Two things matter. First, its custom vocabulary is built by **GPT-5 NER over the gold transcripts** —
the newest benchmark in our exact area sits on the *illegal* rung of our provenance ladder, which is
the single best concrete exhibit we have for making legality a live axis rather than a slogan.
Second, and more dangerous, it already runs the **local-vs-global supply aperture** comparison and
reports the conclusion N1 was going to discover: *"local context is systematically easier"*, *"global
context primarily stresses precision"*, with distractor-induced false positives and decoding-trajectory
damage (hallucination, partial output, language switching). N1's aperture result now has a published
comparator on a sister corpus.

Supporting: **streaming CTC-WS (2605.18222)** is a *training-free, acoustically conditioned* keyword
router — the exact adjective pair we intended to own — differing only in that it consumes frame-level
CTC posteriors. And **"Listen, Do Not Copy" (2607.21943)** does not stop at the copying phenomenon:
it also ships gate-only GDPO training that "learns whether and when to use a clue" and a benchmark
whose axes explicitly include gating. The paper that scooped C3 is also standing on C2.

---

## 3. Per-rung positioning table (C1–C4)

Reviewer stance assumed: a hostile Interspeech/ICASSP/ACL reviewer who has read RECOVER, ConEC,
Voice Memory, "Listen Do Not Copy", and at least one of CLAR / Siskos.

### C1 — legal coverage (currently "partial")

| Field | Content |
|---|---|
| **Claim as stated** | Deployment-legal, zero-gold rosters (company + speaker names from dataset-shipped CSVs) give usable entity coverage. |
| **Closest prior** | **ConEC (LREC-COLING 2024)** — per-call Earnings-21 bags from slides, earnings releases and **participant names/affiliations scraped from Seeking Alpha**, with the **coverage ledger already published** (Table 1: PERSON 82%, ORG 66%, GPE 61% … FAC 29%; PERSON drops to 30% without the roster). Runners-up: Siskos 2509.19567 (fully legal generic 466,358-word public vocabulary, no gold at all, on Earnings21) and RECOVER's BERT-NER-over-hypotheses recipe. |
| **Survives?** | **No, not as a claim.** ConEC published both the substance (participant metadata) and the measurement (coverage-by-entity-type) on our exact corpus. Our planned evidence — a roster built from shipped CSVs plus a coverage number — is a *cheaper sourcing* of ConEC's list, not a different object. A reviewer will write: "the contribution is that the authors used a CSV instead of a scraper." |
| **Required evidence to make anything survive** | Legality must become a **measured axis with a price**, not a property. Minimum: a four-rung provenance ladder run head-to-head at matched token budget on one vehicle — (a) zero, (b) shipped-metadata roster, (c) auto-NER over our *own* baseline hypotheses (RECOVER/DeRAGEC's legal recipe — the rung most competitors silently occupy), (d) gold-derived oracle roster (the rung **Contextual Earnings-22 openly occupies**). Pre-register (d)−(b) and (c)−(b) with sign-agnostic reporting. The publishable object is then "what deployment legality costs in entity-WER", which nobody has priced; (c) is also our cheapest capability upgrade if (b) is underpowered. Additionally: publish the roster coverage ledger in **ConEC's exact per-entity-type schema** before the block runs, so the comparison is direct rather than rhetorical. |

### C2 — speech-aware routing (currently "open") — *the only rung with real upside, and it is now crowded*

| Field | Content |
|---|---|
| **Claim as stated** | Routing/flagging *which* windows get supply, conditioned on the speech signal, inside a training-free black-box control plane. |
| **Closest prior** | Four, in decreasing similarity: **CLAR 2603.25460** (audio-conditioned hotword retrieval → prompt injection; trained retriever + LoRA consumer); **IBM 2604.12398** (acoustic-cue bias-word *position* prediction; trained, multi-output); **streaming CTC-WS 2605.18222** (**training-free**, acoustic, gates which keywords are committed — but consumes CTC log-probs); **2607.21943's gate-only GDPO** ("learns whether and when to use a clue"). Background: utterance-level bias detectors over encoder features are settled practice (Nature s41598-025-12121-4, unverified-at-source; entity detectors / confidence-activated decoders generally). Text-conditioned selection is fully occupied (Siskos previous-hypothesis embeddings; DeRAGEC GLiNER-on-1-best; RECOVER three-signal lexical score over the hypothesis). |
| **Survives?** | **Only in one strictly-scoped form**, and our planned evidence does **not** currently reach it. "Speech-conditioned selection" is occupied (trained). "Training-free acoustic routing" is occupied (CTC-WS, white-box). What is unoccupied is *training-free routing conditioned on the speech signal through an output-only interface* — no logits, no encoder features, no CTC posteriors, no second answering LLM. That is a genuinely empty cell. But an "offline flag-recall measurement" is not evidence for it; it is a diagnostic, and Contextual Earnings-22 already published the qualitative aperture conclusion (local easier, global stresses precision). |
| **Required evidence** | Three things, all currently missing. **(1) A matched text-conditioned selector as an in-study control.** Every prior selects from text. If our speech-conditioned flag does not beat a text-conditioned flag built from our own baseline hypotheses, at matched supply budget, on the same vehicle, C2 is asserted rather than shown — and Siskos's killer secondary result (context *overlap* does not predict WER) says the intuition can fail. This is the single most important missing arm in the whole plan. **(2) A demonstration that the flag actually reads the audio.** With an API-only omni, "speech-conditioned" is at risk of meaning "conditioned on the omni's own text output", which is text-conditioned with extra steps. A silence / shuffled-audio flag control settles it: if flag behaviour is unchanged when the audio is replaced, the routing is not speech-aware. **(3) Price the regime constraint.** See §5 — `logit_bias` is available on our own stack, so "API-only" is currently an unfalsified self-handicap of exactly the kind Cluster A attacked our legality claim for. |

### C3 — verified use (VOIDED as operator; narrowed)

| Field | Content |
|---|---|
| **Claim as stated (post-VOID)** | Prompt-level verification against the audio does not work on a frozen omni; a perfect training-free guard is worth −0.28 pp entity-WER at the current aperture vs −12 pp for oracle supply. |
| **Closest prior** | **2607.21943** — priority on the phenomenon (perception bypass; **Qwen3-Omni 30B 94.2% blind-copy under a wrong contextual answer**; silence control at 100%), plus the remedy. **2607.13477** — frozen Qwen3-Omni-Instruct/-Thinking as judges follow wrong references, with a chance-normalized RF metric. **2602.11488** — prompt-framing factorial moving TDR 19.0%→3.8%. **Voice Memory 2607.26410** — HER and ρ as named diagnostics, abstain, restraint-by-rule. **RECOVER 2603.16411** — Tool 3 is deterministic *specifically because* they would not let an LLM verify an LLM. |
| **Survives?** | **As an operator claim, no — decisively dead.** As a *system-level allocation bound*, **yes, and it is the most original single number in the plan.** Nobody in the four clusters or this sweep computes what a perfect guard is worth end-to-end against the alternative use of the same budget. Voice Memory measures HER but never prices the guard against supply; 2607.21943 prices nothing (it trains the fix); EChO-Agent's ablation ordering (evidence integration −5.6 acc vs verification −1.9) corroborates the ordering but not the magnitude. |
| **Required evidence** | The bound must be stated as a *bound*, not as a null: "under a routed aperture of X% of reachable error mass, guard-chain perfection is worth ≤0.28 pp; the same effort spent on supply is worth 12 pp." Requirements: the aperture must be measured, not assumed (that is N1); the −12 pp oracle arm and the −0.28 pp guard arm must be computed on **one** vehicle with **one** ledger; and the copy evidence must carry a **silence control** on our own aperture (now table stakes — its absence is the cheapest desk-reject available to a reviewer who has read 2607.21943). 7/9 vs 7/9 and 49/53 cannot support a parity claim; either run a pre-registered equivalence test with a declared bound, or stop calling it parity and call it "no detectable framing effect at n=9, bounded by [·]". |

### C4 — task conversion (unproven; SLURP admitted)

| Field | Content |
|---|---|
| **Claim as stated** | ASR/entity gains from the control plane convert into downstream speech-task capability (SLURP slot-SLU). |
| **Closest prior** | **FSA-GRPO 2606.02615** — frozen Qwen2.5-Omni 35.42 → **27.29 with 3-shot audio-text demonstrations, before any RL** (i.e. the training-free part alone converts). **DeRAGEC 2506.07510** — STOP (SLU) 8.9→5.9 from retrieval-augmented correction with a frozen LLM. **Voice Memory** — ATIS (intent/command) 8.40→3.40. |
| **Survives?** | **Not as a conversion claim.** That entity-level ASR improvement propagates to SLU is demonstrated three times over, twice on frozen models. Our planned evidence (run SLURP after N2) reproduces a known implication. |
| **Required evidence** | The only defensible form is a **coupling** claim, not a conversion claim: that the *same routing decision* optimized on the ASR ledger transfers to the task ledger without re-tuning — i.e. transfer of the *controller*, not of the *gain*. That requires the routing policy to be frozen across the two carriers and reported as such, plus a negative control where a task-tuned router is shown to be no better. If we cannot commit to freezing the router across carriers, C4 should be demoted out of the claim ladder to "downstream sanity check" and not defended. |

---

## 4. Gap-statement verdict, conjunct by conjunct

Gap under attack: *no runnable prior combines* **training-free** + **black-box** + **legal provenance**
+ **speech-conditioned targeting** + **audio-grounded verification** + **harmful-edit accounting** +
**task conversion** *on a frozen omni core*. (Seven, counting the carrier; the brief names six plus
the now-negative verification term.)

| Conjunct | Verdict | Why |
|---|---|---|
| **training-free** | **TABLE STAKES — carries zero weight.** | RECOVER, DeRAGEC (frozen LLM ICL, zero training), Voice Memory (zero parameters on the inference path), EChO-Agent, streaming CTC-WS, Siskos's retrieval stage — all training-free. In 2026 this is a setting, not a contribution. Stating it as novelty signals unfamiliarity with the last twelve months. |
| **black-box / API-only** | **LIVE BUT UNDEFENDED — the strongest sub-form is not the one we are claiming.** | Two distinct constraints are being bundled. (a) *No logit access*: real for commercial omni APIs, but **falsified on our own stack** — llama-server exposes `logit_bias` and `n_probs`, so LOGIC-style trie bonuses are implementable here. Unpriced, this reads as a self-imposed handicap. (b) **No second answering LLM**: this is the genuinely rare conjunct and we are under-weighting it. RECOVER calls GPT-4o once per segment; DeRAGEC uses Llama-3.1-70B / GPT-4o-mini; Voice Memory uses a separate frozen corrector; EChO-Agent re-prompts DeepSeek-V3; Siskos consumes through a *trained* CB module; CLAR fine-tunes the consumer. **Single-core is the least-occupied conjunct in the whole statement.** Promote it; price the logit constraint. |
| **legal provenance** | **NEAR-TABLE-STAKES — survives only if converted from property to measured axis.** | ConEC did external-source lists on Earnings-21 in 2024, with the coverage ledger. Siskos used a fully public 466k dictionary. RECOVER shipped a BERT-NER auto-derivation recipe. The live residue is that *nobody prices it*: Contextual Earnings-22 (2026, our sister corpus) builds vocabulary from gold transcripts and does not discuss deployment sourcing at all; RECOVER states provenance for only 2 of 5 carriers and none for Earnings-21. So the contribution is the **ladder and the price**, never the constraint. |
| **speech-conditioned targeting** | **THE ONLY CONJUNCT STILL CARRYING REAL WEIGHT — and it narrowed this week.** | Occupied when trained (CLAR, BR-ASR, IBM position prediction, GLCLAP+GRPO, 2607.21943's gate). Occupied when white-box training-free (CTC-WS on CTC posteriors). Occupied when text-conditioned (Siskos, DeRAGEC, RECOVER). The empty cell is precisely *training-free × output-only × speech-conditioned*. That is defensible — but it is now a three-way intersection, not a property, and it **must be demonstrated against a matched text-conditioned control** or it collapses into "we prompted the model and called it speech-aware". |
| **audio-grounded verification** | **DEAD AS A POSITIVE CONJUNCT; usable only as a measured negative with a bound.** | 2607.21943 has priority and a stronger control on the same model family. Do not carry this word in the gap statement. |
| **harmful-edit accounting** | **DEAD AS NOVELTY — keep as hygiene, claim nothing.** | HER and ρ are NVIDIA's, same acronyms, same semantics, three weeks older, and HER is `1 − Precision` on the survey's own §5.2 alignment. Also occupied: LOGIC's FAR, IBM's U-WER, ConEC's non-entity WER, ProfASR's NE-WER, Improve@Edit / Worsen@Edit (2606.13464), Contextual Earnings-22's precision drops and error-mode table. Rename ours (the *denominator* change — delivered-correct opportunities rather than the 1-best→oracle gap inside an N-best list — is the only defensible residue, framed as *necessary*, not *better*), cite Yang et al. 2026 in the metrics section, not the tail. |
| **task conversion** | **WEAK — reproduces a known implication.** | FSA-GRPO, DeRAGEC-on-STOP, Voice Memory-on-ATIS. Survives only as controller transfer (see C4). |

**Verdict on the statement as a whole.** Of seven conjuncts, **two carry weight** (speech-conditioned
targeting in the output-only regime; single-core / no-second-answering-LLM), **one is salvageable as a
measured axis** (legality-as-price), **one is salvageable as a bound** (guard futility), and **three are
table stakes or dead**. A seven-way conjunction with two live terms is the textbook "novelty by
intersection" tell, and a hostile reviewer will name it as such — the more conjuncts we list, the more
obviously each one is individually occupied. **Recommendation: collapse the gap statement to two
conjuncts and one number.** Something of the shape: *"speech-conditioned supply routing on a frozen
omni core reached only through an output-only interface, with no second answering model, and the
first measurement of what the routing aperture — not the guard chain — is worth."* Everything else
moves from the gap statement into the experimental design, where it is a control rather than a claim.

---

## 5. The `logit_bias` problem (new, and sharp)

Cluster B and C both leaned on "LOGIC is excluded by our API-only boundary" and "every published fix
needs logits or weights". Row 13 of the fetch log breaks that defence on our own stack: llama-server
accepts `logit_bias` (including string-form tokens and hard bans) and returns `n_probs`/`top_probs`.
A reviewer who runs llama.cpp — a large fraction of the speech community — will observe that
trie-constrained or biased decoding over entity tokens is a config change away, and that we excluded
the strongest published mechanism by fiat.

Two honest responses, and we must pick one before N2 registers:

1. **Price it.** Add a `logit_bias` upper-reference arm (roster tokens biased at decode) alongside the
   prompt-supply arm, exactly as Cluster A proposed pricing legality. The API-only constraint then
   becomes a *measured* deployment posture with a known cost, not an assertion. This also gives us the
   prompt-vs-logit comparison **LOGIC asserted without a baseline table** ("cannot support large phrase
   lists… may leak the whole phrase list… not only Phi-4-mini but also GPT-4o" — assertion, anecdote,
   internal sets, no prompt baseline). Supplying that missing table is a real, citable contribution and
   it costs one arm.
2. **Re-scope the constraint** from "API-only" to "prompt-level supply", and justify it by the target
   deployment (commercial omni endpoints — GPT-Audio, Gemini Live — expose no audio-aligned logit
   control). Weaker, but honest.

Do **not** leave it implicit. One architectural point is worth keeping either way: CTC-WS is
inapplicable to a decoder-only omni because there are no frame-level CTC posteriors to spot in — that
exclusion is architectural and holds regardless of `logit_bias`.

---

## 6. Negative-result publishability verdict

**Verdict: not publishable as a standalone negative result at any of Interspeech, ICASSP, or
ACL/EMNLP. Publishable as one figure inside a systems/analysis paper whose headline is the allocation
bound.** This concurs with Cluster D and hardens it with venue-specific reasoning.

Why it fails standalone:

- **Priority is lost by three weeks and the priority holder has a stronger design.** 2607.21943 names
  the phenomenon (perception bypass), reports **94.2% blind-copy on Qwen3-Omni 30B** — the same model
  family — carries a **silence control** we lack, tests three omnis, uses n=150, and ships a remedy.
  A null that arrives second, with a weaker control and n=9 windows, has no path.
- **The finding is consensus, not news.** "No reliable self-verification without training" holds across
  text (Huang 2310.01798), RAG (AlignRAG's *trained* critic), omni speech (2607.21943), judging
  (2607.13477), and mechanism (2606.18924, where the text pathway actively suppresses intact audio
  representations). RECOVER's Tool 3 is the same conclusion implemented as engineering. The survey
  2508.07285 §6 gap #1 already names text-only refinement causing overcorrection.
- **Our statistics cannot carry a parity claim.** 7/9 vs 7/9 windows is not equivalence; 49/53
  byte-identical is a strong descriptive fact but a small n. 2602.11488 moved TDR 19.0%→3.8% by
  framing at much larger n, so "framing does not matter" is *contradicted in the neighbouring setting*.
- **Venue fit.** ICASSP (4 pages, method-and-numbers culture) is the worst fit for a null and should be
  dropped from consideration. Interspeech tolerates analysis papers but at 4 pages a scooped
  phenomenon with a weaker control will not clear the bar. ACL/EMNLP Findings plus an Analysis or
  Resource paper type is the only realistic home, and only if the null is *not* the headline.

**What must be foregrounded for the finding to survive as a component** — in priority order, all four
of the deltas the brief names, plus one:

1. **The allocation bound as the headline** (−0.28 pp perfect guard vs −12 pp oracle supply, RIR 0/54,
   at a measured aperture). This is the only element no prior computes. Lead with it; the copy parity
   is the *reason* the bound is what it is, not the result.
2. **Frozen-omni carrier + real long-form clean audio at a pre-localized routing aperture.** Every
   prior measures copying on isolated clips (2607.13477), synthetic overlap/noise mixtures
   (2607.21943), or 1.5–8 s forced-choice items (2602.11488). Nobody measures it at the aperture a
   *real flag gate* produces on real long-form speech. The acoustic-difficulty excuse is unavailable
   to us — our audio is clean — which makes the copying result stronger, not weaker, than theirs.
   State the aperture construction explicitly; it is the delta that cannot be replicated from their
   setups.
3. **Supply form: narrow entity reference vs whole answer-bearing transcript.** 2607.21943 supplies
   answer-bearing context; RECOVER supplies a *constrained vocabulary* plus offset-anchored edits and
   a rejection filter. Our voided chain supplied a whole candidate reference — the cheapest possible
   action is emission. Foreground this as *the mechanism of the null*: whole-reference supply is a copy
   trap under which verification is unmeasurable. It narrows the claim honestly and it explains why
   the field's deployed systems (RECOVER Tool 2/3, LOGIC's trie) all constrain the edit vocabulary.
4. **The framing factorial at fixed correctness, including a verify rung.** 2602.11488's four rungs are
   all *attribution-strength* variants ("may contain errors" → "DELIBERATELY CORRUPTED" → explicit
   ignore → audio-first); none says "verify this against the audio". 2607.21943's single fallibility
   instruction is unablated setup. Our verify-vs-bias contrast at fixed reference correctness is
   genuinely unrun — but it must be reported as **bounded**: no detectable effect *within the
   attribution-neutral framing family*, with our verify rung located explicitly near their *baseline*
   rung, not their adversarial rung. Their non-monotone result (audio-first *raised* TDR to 33.0%) is
   our best supporting evidence that prompt control is not a dial.
5. **Wrong-reference derangement as an open-vocabulary copy metric.** All priors use forced-choice or
   closed labels where chance is nonzero; ours is literal byte-identical string reproduction in
   open-vocabulary transcription where chance ≈ 0. Keep the derangement construction and report the
   byte-identity rate as the primary copy statistic — but adopt 2607.13477's `RF` vocabulary rather
   than minting a fourth name, the same discipline as the HER/ρ caveat.
6. **(Addition) A silence control on our own aperture, before any write-up.** Non-negotiable. Its
   absence is the single easiest desk-reject, and it doubles as the C2 evidence that the routing flag
   reads the audio at all.

---

## 7. Mandatory-baseline list for N2 (what the deep reads revealed and the plan lacks)

Ordered by how badly the block dies without them. Items 1–4 are, in my judgement, block-blocking.

| # | Baseline / arm | Why mandatory | Prior that forces it |
|---|---|---|---|
| **1** | **Text-conditioned selector at matched supply budget** — roster selected per window from our own baseline hypotheses (lexical/NER scoring), vs the speech-conditioned flag. | Without it, C2 — the only rung with upside — is asserted. Every published selector is text-conditioned; a reviewer's first question is whether the audio contributed anything. | Siskos (prev-hypothesis embeddings), DeRAGEC (GLiNER on 1-best), RECOVER (three-signal lexical score), and Siskos's "overlap does not predict WER" result. |
| **2** | **Silence / shuffled-audio control**, on both the supply arm and the routing flag. | Table stakes since 2607.21943 used it as their leakage test; also the only clean proof that "speech-conditioned" is not "text-conditioned with extra steps". Pre-register a kill threshold. | 2607.21943 (all three omnis 100% on silence); 2604.07354's answer-overlap logic. |
| **3** | **Distractor / mismatched roster** — a same-format roster drawn from a *different* Earnings-21 call. | Separates "the names helped" from "any occupied context changed decoding". Both published Earnings-corpus works report supply *harming* under distractors. Also the placebo control for the Voice Memory reading that content substance may not be what matters. | ConEC row 3 (shared distractor list degrades GPE/NORP/FAC below no-context); Contextual Earnings-22 (global context stresses precision; hallucination / language switching); CLAR Table 3 (FP hotwords perturb non-bias decoding). |
| **4** | **Provenance ladder: zero / shipped-metadata / auto-NER-over-own-hypotheses / gold-oracle**, matched token budget. | Converts C1 from a dead claim into the one measurable thing nobody has: the price of legality. Rung (c) is also the fallback capability if the metadata roster is underpowered at n=44. | RECOVER (BERT-NER recipe, provenance unstated for Earnings-21); Contextual Earnings-22 (GPT-5 NER over gold); ConEC (external sources); Siskos (public dictionary). |
| **5** | **ConEC's public context bag as an explicit third supply arm** on the same frozen-omni vehicle, at n=44 = ConEC's own eval set, reported in **ConEC's per-entity-type schema**. | Pre-empts "this is ConEC row 4 with a chat wrapper" — the most likely single-sentence rejection. Also converts ConEC from a competitor into our strongest supporting citation (their consumer is a 71.5M zipformer with shallow fusion; ours is a frozen omni — same context, two consumers). **Blocker: ConEC's repo states no license — resolve before consuming.** | ConEC (LREC-COLING 2024). |
| **6** | **Roster-size dose sweep** with pre-registered sizes. | Our "full bag = no gain at 4× tokens" is currently an isolated observation; three published works give it a shape and one contradicts it. Pre-registering the sweep makes compact rosters a consequence of a known scaling law rather than a lucky pick — and the *consumer-dependence* of the dose response (trained CB modules dose-robust, frozen prompt-readers dose-fragile) is our most defensible framing. | Ren/Shi/Li 2506.06252 (EWER 1.80 / 4.16 / 5.61); RLBR 2601.13409; DeRAGEC U-shape at k=15; LOGIC's 50–100 assertion; **counterexample** Siskos (c=100→250 helps, 15× oracle token count still wins). |
| **7** | **Multi-hypothesis / self-consistency-only control at matched compute**, plus the crossed cell. | Pre-empts "your gain is confounded with hypothesis diversity you never harvested". Cheap and pre-armed: on Earnings-21 RECOVER's four fusion strategies span 15.59–15.90 E-WER and plain 1-Best gets 33.2% vs LLM-Select's 33.4% — diversity buys ~0.2 pp of a 33 pp effect on our exact carrier. | RECOVER (5 decodes at T ∈ {0.0…0.8}, ROVER, LLM-Select). |
| **8** | **`logit_bias` upper-reference arm** (roster tokens biased at decode on llama-server). | Prices the API-only constraint instead of asserting it, and supplies the prompt-vs-logit baseline table LOGIC never ran. Without it, "black-box" is an unfalsified self-handicap. | LOGIC 2601.15397; llama.cpp server README (`logit_bias`, `n_probs`). |
| **9** | **Local (routed) vs global (whole-call) supply aperture**, reported as a pair. | Contextual Earnings-22 already published the qualitative version on our sister corpus; if we do not run the pair explicitly, our aperture result is unpositioned relative to a 2026 benchmark. Running it turns their qualitative claim into our quantitative one on a frozen omni. | 2604.07354 ("local context is systematically easier"; "global context primarily stresses precision"). |
| **10** | **Copy-rate / byte-identity as a first-class reported metric on every supply arm**, not only the voided verify arm. | If any N2 gain coexists with elevated copy rate, the gain is attackable as parroting. Reporting it pre-emptively converts the strongest attack into a result. | 2607.21943; our own 49/53. |

**Non-baselines worth pre-registering anyway:** entity-WER as primary with macro WER demoted to a
pre-registered non-inferiority guardrail (n=44 cannot detect sub-0.5 pp macro effects; Siskos beat us
on macro relative gain, 17% vs our 2.3%, so macro is the field we lose on and entity-WER is the field
nobody else reports on Earnings-21); paired within-call bootstrap with a pre-declared decisive ledger;
and **fraction-of-oracle-headroom-recovered** as the effect size, which is dimensionless, survives
small n, and is directly comparable to ConEC row 5, DeRAGEC Table 4, and Voice Memory's ρ.

---

## 8. Residual risks and open items

- **Nature s41598-025-12121-4 bias detector is unverified at source** (paywall redirect, no logins).
  The claim that trained per-utterance bias gating is settled practice rests on CLAR + IBM 2604.12398
  + 2607.21943's gate independently, so the conclusion holds without it; but do not cite the Nature
  paper from this file.
- **Contextual Earnings-22's dataset is under embargo** ("released upon acceptance"). If it releases
  before we register, it becomes a mandatory comparator on `earnings22-original` and its GPT-5-over-gold
  vocabulary becomes our named illegal rung. Re-check before N2 registers.
- **ConEC license still unresolved** (repo states none). Arm #5 is blocked on it.
- **CLAR is Mandarin (AISHELL)**; the language mismatch is a legitimate distancing argument but not a
  novelty defence — the architecture transfers.
- **DEMO lane** remains the part of the plan most eroded: Voice Memory executes the gold-permitted
  offline accept/reject construction at scale with an acceptance gate, and FSA-GRPO publishes the
  3-shot audio-text demonstration mechanism on a frozen omni (35.42 → 27.29 with no RL). Combined with
  2607.21943's finding that answer-bearing context is exactly what perception bypass copies, DEMO needs
  a fresh justification beyond "owner-proposed" before it consumes a slot.
