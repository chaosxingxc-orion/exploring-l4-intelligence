# Cluster D — Copying / Verification Behavior and Evidence-Use Control

Workbench note (non-authoritative, exploration only). Campaign:
`2026-08-16-deep-reading-adversarial-check`. Author: deep-reading agent, Cluster D.
Scope: adversarial prior-art check on the SAEA P2 VOID finding (instruction-framed verification
collapsed to text-following; wrong-reference copy parity between verify and bias framings on a
frozen Qwen3-Omni core with ~10 s audio present).

All timestamps UTC. Repositories were read-only; this file is the only artifact written.

---

## 1. Fetch log

| # | UTC | Kind | Query / URL | One-line result |
|---|-----|------|-------------|-----------------|
| 1 | 2026-08-17T00:52Z | fetch | `https://arxiv.org/abs/2607.21943` | HIT — "Listen, Do Not Copy: Internalizing Audio-Grounded Scaffold Context for Robust Omni-Model Speech Understanding"; defines **perception bypass**; frozen Qwen3-Omni 30B among the three probed models. |
| 2 | 2026-08-17T00:52Z | fetch | `https://arxiv.org/abs/2606.15141` | HIT — "EChO-Agent: Evidence Chain Orchestration Agent for Audio Reasoning", Interspeech 2026; plan → tool → evidence → verify; MMAR benchmark. |
| 3 | 2026-08-17T00:54Z | fetch | `https://arxiv.org/html/2607.21943v1` | Full text — blind-copy table, silent-audio control, GDPO reward decomposition; **no prompt-only mitigation baseline**. |
| 4 | 2026-08-17T00:54Z | fetch | `https://arxiv.org/html/2606.15141v1` | Full text — verification = DeepSeek-V3 re-prompted (model-judged), tools frozen, fully training-free; ablation numbers. |
| 5 | 2026-08-17T00:56Z | fetch | `https://arxiv.org/html/2607.21943v1` (targeted 2nd pass) | Confirmed: blind-copy 94.2 / 99.8 / 47.0; no instruction-only or verify-prompt arm anywhere; v1 dated 24 Jul 2026. |
| 6 | 2026-08-17T00:56Z | fetch | `https://arxiv.org/abs/2504.14858` | AlignRAG = "Retrieval is Not Enough: Enhancing RAG Reasoning through Test-Time Critique and Optimization"; **trained** 8B Critic LM; text-only. |
| 7 | 2026-08-17T00:56Z | fetch | `https://openreview.net/forum?id=9U51rOnGko` | BLOCKED — OpenReview bot-verification interstitial, no content. Recovered via search #1. |
| 8 | 2026-08-17T00:58Z | search | `CF-RAG counterfactual retrieval augmented generation evidence misuse OpenReview 2026` | Resolved CF-RAG = "Counterfactual Reasoning for Retrieval-Augmented Generation", ICLR 2026 poster; "Correlation Trap"; counterfactual query generation + parallel arbitration. |
| 9 | 2026-08-17T00:58Z | search | `audio LLM ignores audio follows text prompt prior sycophancy verification prompt fails 2026` | **THREE MAJOR ADVERSARIAL HITS**: arXiv 2602.11488 (ALME / Text Dominance Ratio, prompt-framing factorial), arXiv 2607.13477 (protocol-level shortcuts in LALM judges, Qwen3-Omni), arXiv 2606.18924 (mechanistic text bias). |
| 10 | 2026-08-17T00:59Z | fetch | `https://arxiv.org/html/2602.11488v3` | Full text — TDR formula, 57,602 conflict stimuli, 8 languages, **four prompt framings with per-framing TDR**; models GPT-4o-audio, Gemini 2.0 Flash, Ultravox, Qwen2-Audio. |
| 11 | 2026-08-17T00:59Z | fetch | `https://arxiv.org/html/2607.13477v1` | Full text — reference-follow rate RF(M) on **wrong supplied references**, six judges incl. **Qwen3-Omni-Instruct / -Thinking**; verification-by-frozen-LALM declared unreliable. |
| 12 | 2026-08-17T00:59Z | fetch | `https://arxiv.org/abs/2606.18924` | Abstract — "Who Wins the Conflict?"; text pathway *suppresses* intact audio representations; back-patching (weights-access intervention) reduces text dominance. |
| 13 | 2026-08-17T01:00Z | search | `LLM ASR error correction contextual biasing list over-correction harmful edits copies wrong entity 2026` | Confirms over-correction / error-propagation lineage (arXiv 2512.21828, 2604.12398, 2606.00507, 2505.16212); SNR augmentation used to "curb over-reliance on the LLM's text prior". |
| 14 | 2026-08-17T01:00Z | search | `large language models cannot self-correct reasoning without external feedback intrinsic self-verification failure negative result` | Anchor prior: Huang et al., "LLMs Cannot Self-Correct Reasoning Yet" (arXiv 2310.01798, ICLR 2024) — intrinsic self-correction degrades performance without external feedback. |

Search budget: 4 bounded searches authorized, 4 used (#8, #9, #13, #14).

---

## 2. Deep reading — primary targets

### 2.1 "Listen, Do Not Copy" (arXiv 2607.21943v1, 24 Jul 2026)

Full title: *Listen, Do Not Copy: Internalizing Audio-Grounded Scaffold Context for Robust
Omni-Model Speech Understanding*. Zhang, Tian, Xie, Yang, Li, Liu. cs.SD.

**This is the closest prior art to the SAEA VOID and it predates our read by three weeks.**

- **Phenomenon named**: *perception bypass* — "An overly informative `c` can make `a` irrelevant".
  Framed as shortcut learning: "answer-bearing text lets the model copy instead of listen, so the
  score rises although nothing has been heard; a silent test exposes this shortcut at once."
- **Carrier**: overlapping + noisy multi-speaker "who said what" transcription. Sources:
  LibriSpeech, SparseLibriMix2, AISHELL-3, WHAM, AMI. Evaluation split n=150; hardest-third
  n=50/model; clue-maturity study n=55 clips. Per-clip durations not stated in the main text.
- **Frozen / untrained condition** (Table 1, primary-transcript task; blind-copy measured
  **under a wrong contextual answer**):

  | Model | No context | +Answer-bearing context | Blind-copy rate |
  |---|---|---|---|
  | Qwen3-Omni 30B | 65.6 | 93.3 | **94.2** |
  | MiniCPM-o 4.5 (9B) | 53.4 | 96.8 | **99.8** |
  | Ming-flash-omni 2.0 | 40.1 | 91.1 | 47.0 |

- **Silent-audio control**: with audio replaced by silence, "all three still reached 100%
  primary-transcript accuracy." Design criterion stated as `mpWER(y, M(a_∅, c)) ≥ η`, with η = 1
  for transcription.
- **Copy metrics**: blind-copy rate (wrong-context following), the silent-audio control, and an
  answer-overlap screen that rejects directly copyable answer strings.
- **Prompt safeguard used, not ablated**: "The audio-first instruction marks every clue as
  automatic and fallible." The exact wording is not published, and there is **no instruction-only,
  prompt-warning, self-check, or verify-prompt baseline row anywhere in the paper**. Copying
  persists at 94.2–99.8% *despite* that fallibility instruction.
- **What training fixes**: AGSC + GDPO (group reward-decoupled normalization).
  `A^{j,i} = (r_{j,i} − μ_j)/(σ_j + δ)`, `A_i = Σ_j w_j A^{j,i}`; gate reward
  `r_gate = 1[u = u*]·r_fmt`; ASR reward `r_asr = (1 − min(1, mpWER))·r_fmt`; conditional coupling
  `r_asr ← r_asr · r_gate` blocks transcript credit unless the use/ignore gate is right.
- **Their own novelty claim**: prior work "shows that large audio models can answer from text alone
  and uses that signal to split training data. We instead use silence as a design criterion." They
  claim no prior work explicitly tests textual-context answer leakage in speech/omni models with a
  silent-audio control.

### 2.2 EChO-Agent (arXiv 2606.15141, Interspeech 2026)

*EChO-Agent: Evidence Chain Orchestration Agent for Audio Reasoning*. Zhang, Zong, Wang, Jiang,
Yan, Zhang, Wang, Wang, Wang, Dang. Interspeech 2026 Audio Reasoning Challenge, Agent Track (5th).

- **Pipeline**: Tool (LLM orchestrator, question-type-conditioned **static** dispatch) → Evidence
  (DeepSeek-V3 distils tool outputs: relevance filtering, cross-observation synthesis, structuring)
  → Reason (Qwen3-Omni-Instruct answers conditioned on audio + question + evidence + prior
  feedback) → Verify.
- **Verification is model-judged, by a TEXT LLM, not audio-grounded.** The verifier is DeepSeek-V3
  re-prompted (`π_ver`): format compliance (malformed outputs repaired by rule-based
  post-processing), CoT/answer consistency ("contradictions between the evidence cited in the CoT
  and the final answer"), and dual-pass arbitration selecting "the candidate whose reasoning
  exhibits stronger evidence alignment and internal coherence." **Nothing in the verify stage
  re-consults the waveform.** No verification prompt is published.
- **Tools**: YAMNet (AED), Whisper (ASR), SpeechBrain (SER), Essentia (music). All frozen; ≤2
  retries then `[UNAVAILABLE]`.
- **Training**: none. Fully training-free prompting.
- **Results (MMAR)**: full 71.0 acc / 63.0 rubric vs Qwen3-Omni baseline 68.7 / 58.7 (+2.3 / +4.3).
  Ablations: w/o evidence integration 65.4 / 56.9 (**below baseline**); w/o observation 69.2 / 60.2;
  **w/o verification 69.1 / 61.5 — verification is worth only +1.9 acc / +1.5 rubric**, the smallest
  of the three components.
- **No copying or verification-failure case is reported.** Stated limitation is perception-tool
  granularity (coarse YAMNet labels), not evidence misuse.
- Modality note: MMAR is sound + music + speech + composite — **general audio**, outside the SAEA
  research boundary as a consumption target; usable only as a citation.

### 2.3 The three papers search #9 surfaced (these are the real threat)

**(A) arXiv 2602.11488v3 — "When Audio-LLMs Don't Listen: A Cross-Linguistic Study of Modality
Arbitration"** (Jayadev Billa, v3 23 Mar 2026).

- ALME: 57,602 controlled audio–text conflict stimuli, eight languages, four scripts. Stimulus =
  Common Voice speech (**1.5–8 s**, 3–25 words) + a transcript with **exactly one semantic element
  flipped** (number / negation / adjective / time) + a binary forced-choice question.
- `TDR = followed_text / (followed_text + followed_audio)`. Overall: Gemini 2.0 Flash 16.6%,
  GPT-4o-audio 23.2%, Ultravox 48.8%, Qwen2-Audio-7B 63.2%. Text–text cascade baseline: 1.6% / 0.9%
  — i.e. text dominance is modality-specific, ~10–26× the text-only arbitration rate.
- **This paper already runs a prompt-framing factorial at fixed conflict** (Gemini, EN+JA,
  n=14,369):

  | Framing | Wording gist | TDR | Cohen's h |
  |---|---|---|---|
  | Baseline | transcript "may contain errors" | 19.0% | — |
  | Adversarial | transcript is "DELIBERATELY CORRUPTED" | **3.8%** | −0.51 |
  | Explicit-ignore | "COMPLETELY IGNORE the transcript" | 7.9% | −0.33 |
  | Audio-first | force explicit transcription before answering | **33.0%** | +0.32 |

  EN 8.1 → 2.0; JA 30.2 → 5.7. Adversarial floor 3.8% still 2.2 pp above the cascade baseline.
- Not tested: Qwen3-Omni or any omni model; free-form transcription; verbatim/byte-level copying
  (answers are binary and parsed by exact string match); any self-check or verification framing.

**(B) arXiv 2607.13477v1 — "Auditing Protocol-Level Shortcuts in Large Audio Language Model Judges
for Speech Evaluation"** (Park, Chan, Saito, Saruwatari; 15 Jul 2026).

- Audits three shortcut families in LALM-as-judge protocols: feature-blueprint copying (reproducing
  specialist classifier labels), **reference-anchor bias** (following supplied reference labels even
  when wrong, strength varying with **prompt placement**), and position-lock in pairwise A/B.
- Metric: `RF(M) = Pr[ŷ_M(x) = r(x) | r(x) ≠ y(x)]` — exactly the "copies the wrong supplied
  reference" quantity, chance-normalized as
  `RF̃(M) = max(0, (RF(M) − 1/(K−1)) / (1 − 1/(K−1)))`.
- Judges: Gemini-3-Flash, GPT-Audio, **Qwen3-Omni-Instruct, Qwen3-Omni-Thinking**, Audio-Flamingo-3,
  Voxtral-Small-24B. Tasks: emotion (RAVDESS, 240 clips), language ID (FLEURS, 3–15 s), naturalness
  (BVCC), speaker similarity (VoxCeleb1).
- Results: wrong specialist labels drive five judges' emotion accuracy to ≤0.10; GPT-Audio hits
  0.94–0.99 chance-normalized reference-follow; five judges exceed 0.30 normalized at some prompt
  position; Qwen3-Omni-Thinking position-locks under order swap.
- Conclusion, verbatim: "A judge may instead rely on specialist labels or reference data supplied by
  the evaluation protocol itself, taking a shortcut in place of listening to the audio"; "high
  agreement with human ratings does not guarantee that their verdicts are grounded in the audio."
  No prompt-level mitigation attempted; remedy proposed is matched shortcut probes per
  model–protocol pair.

**(C) arXiv 2606.18924 — "Who Wins the Conflict? Mechanistic Interpretability of Text Bias in Audio
LLMs"** (Cho, Yoo, Jang, Kim, Chung; 17 Jun 2026).

- Mechanism: text and audio use functionally distinct pathways converging in late layers; **the text
  pathway does not erase audio information, it actively suppresses intact audio representations**.
- Remedy: back-patching (training-free but **requires weight/activation access**) routes late-layer
  audio activations back to earlier layers, reducing text dominance.
- Relevance to SAEA: this is the mechanistic explanation for why *prompt-level* verification cannot
  work on an API-only core — the audio evidence survives inside the model but is suppressed at the
  decision layer, and the only demonstrated lever is an internal-access intervention we are
  contractually barred from.

### 2.4 Text-RAG evidence-misuse controls (skim)

- **AlignRAG (arXiv 2504.14858)** — *Retrieval is Not Enough: Enhancing RAG Reasoning through
  Test-Time Critique and Optimization*. Targets **Reasoning Misalignment** (reasoning diverging from
  retrieved evidence). Fix = a **trained** retrieval-augmented Critic LM (8B), built by contrastive
  critique synthesis over labeled aligned/misaligned reasoning; AlignRAG-auto self-terminates
  refinement. +12.1% over Self-Refine OOD; 8B CLM beats an untrained 72B CLM by 2.2%. Text-only.
  Pattern: **test-time critique works only once the critic is trained**; plug-and-play at the
  pipeline level, not at the prompt level.
- **CF-RAG (OpenReview 9U51rOnGko, ICLR 2026 poster)** — *Counterfactual Reasoning for
  Retrieval-Augmented Generation*. Names the **Correlation Trap**: pipelines cannot separate causally
  decisive evidence from overwhelmingly correlated but misleading evidence. Fix = generate and
  evaluate **counterfactual queries** to isolate causally relevant distinctions, plus parallel
  arbitration over conflicting evidence. Text-only. (OpenReview forum page was blocked by a
  bot-verification interstitial; content recovered via search snippets + ICLR virtual page —
  treat the CF-RAG details as *unverified from primary text*.)
- Common shape across both: text-RAG has moved past "instruct the model to check" to either a
  **trained critic** or **structured counterfactual controls executed by the harness**. Neither
  relies on an untrained model's willingness to distrust supplied evidence. Both corroborate the
  SAEA branch decision to move control out of the prompt and into the external plane.
- Anchor negative result: Huang et al., *LLMs Cannot Self-Correct Reasoning Yet* (arXiv 2310.01798,
  ICLR 2024) — intrinsic self-correction without external feedback degrades performance. Our VOID is
  the speech-carrier instance of a two-year-old, well-cited text finding.

---

## 3. Question 1 — has anyone published our specific measurement?

**Substantially yes; a narrow slice remains.** Decomposing the SAEA VOID claim:

| Component of our claim | Published prior | Verdict |
|---|---|---|
| Frozen omni copies a **wrong** supplied reference at high rate, with audio present | 2607.21943 Table 1: Qwen3-Omni blind-copy **94.2%** under wrong contextual answer; 2607.13477 RF on Qwen3-Omni judges | **SCOOPED.** Same model family, same direction, published 24 Jul 2026 and 15 Jul 2026. |
| Score inflation from answer-bearing context is not audio understanding | 2607.21943 silent-audio control (100% accuracy on silence) | **SCOOPED**, and with a cleaner control than ours. |
| Prompt framing modulates text-following under audio–text conflict | 2602.11488 four-framing factorial (19.0 / 3.8 / 7.9 / 33.0% TDR) | **SCOOPED for the general effect** — and it reports the *opposite* sign to our null: framing mattered a lot there. |
| A **verification-instruction** framing specifically, vs a **bias/hint** framing, at fixed wrong-reference exposure | None. 2602.11488's four framings are all *source-attribution strength* (trust/ignore/corrupted/transcribe-first), never "verify against the audio". 2607.21943 has no framing arm at all. 2607.13477 varies **placement**, not framing semantics. | **OPEN — ours.** |
| **Byte-identical parroting rate** of a supplied free-form transcript reference (49/53) | Nobody measures verbatim reproduction: 2602.11488 is binary forced choice; 2607.13477 is closed-label classification; 2607.21943 measures mpWER-based blind-copy, not exact-match | **OPEN — ours**, though it is a measurement refinement, not a new phenomenon. |
| **Pre-localized routing aperture**: copy behavior measured only inside flag-triggered ~10 s windows carved from long-form real speech (Earnings21/22), not on isolated clips or synthetic mixtures | All three priors use short isolated clips (1.5–8 s Common Voice, 3–15 s FLEURS, acted RAVDESS) or synthetic overlap mixtures (SparseLibriMix2 + WHAM) | **OPEN — ours.** No prior measures copying *at the aperture a real routing gate would produce*. |
| **System-level utility bound on verification**: a perfect guard chain is worth −0.28 pp entity-WER on the reachable flag aperture vs −12 pp for oracle supply; RIR = 0 recovery over 54 delivered-correct opportunities | Nobody. 2607.21943 stops at copy rate; 2607.13477 stops at judge validity; 2602.11488 stops at TDR; EChO-Agent reports only a +1.9 acc verification ablation on general-audio MC-QA | **OPEN — ours, and this is the strongest surviving piece.** |
| Entity-level harmful-edit accounting on real long-form business speech | Post-ASR edit-quality lineage exists (Edit Rate / Improve@Edit / Worsen@Edit, survey arXiv 2508.07285); contextual-biasing over-correction is known (2512.21828, 2604.12398, 2606.00507) | **Partial** — metrics not novel (as already flagged); the *application to a routed-supply control plane* is. |

**Bottom line.** The headline "frozen speech LLM copies wrong references instead of listening" is
**no longer ours to claim**. What survives is: (i) the *verify-vs-bias framing contrast at fixed
correctness*, (ii) *byte-identical parroting* as the copy metric, (iii) the *pre-localized flag
aperture* as the measurement locus, and (iv) the *utility bound* showing that even a perfect
verification guard cannot pay for itself relative to supply. (iv) is the only one large enough to
carry a contribution on its own.

## 4. Question 2 — is a negative-result publication defensible?

**Not as a standalone paper. Defensible only as a bounded section inside the N1/N2 supply+routing
paper.**

Against:

1. **Priority.** 2607.21943 (24 Jul 2026) documents the phenomenon on Qwen3-Omni, adds a stronger
   control (silence), *and* ships the fix (GDPO). A negative-only paper appearing after it is a
   weaker replication with no remedy.
2. **The "no verification without training" thesis is already the field's consensus.** Huang et al.
   2023 for text, AlignRAG for RAG (trained critic), 2607.21943 for omni speech (training fix),
   2606.18924 for the mechanism (internal intervention). Restating it on one more carrier is not a
   contribution.
3. **Our null is contradicted in the neighbouring setting.** 2602.11488 shows framing moves TDR from
   19.0% to 3.8% (Cohen's h = −0.51). A reviewer will ask why our verify framing produced parity,
   and the most parsimonious answer is that our framing was under-powered, not that verification is
   impossible.
4. **Statistical thinness.** 7/9 vs 7/9 windows and 49/53 replay outputs cannot support a
   parity claim; the priors run n=150, n=14,369, n=240×6.

For (what is genuinely defensible):

- **"Verification is not where the headroom is" is a resource-allocation result, not a phenomenon
  result.** The −0.28 pp vs −12 pp decomposition and RIR = 0 are the publishable core, and no prior
  computes them. Frame as: *given* the copying prior (cite 2607.21943, 2607.13477), we quantify what
  a perfect training-free guard would be worth end-to-end inside a routed control plane, and show it
  is negligible relative to targeted supply — therefore route+supply, not verify.
- EChO-Agent independently corroborates this at the ablation level: verification contributes the
  least of its three components (+1.9 acc), and evidence integration the most (−5.6 when removed).
  That is the same ordering our forensics produced, on a different carrier.

**Recommendation.** Retire the standalone negative-result angle. Fold the VOID into N2 as a
pre-registered *negative control* motivating the supply lane, with an explicit citation block
(2607.21943, 2607.13477, 2602.11488, 2606.18924, 2310.01798). Move the C3 claim from
"verified use" to "**bounded futility of prompt-level verification under a routed aperture**",
supported by the utility bound rather than by the copy rate.

## 5. Question 3 — three attacks and neutralizing evidence

### Attack 1 (fatal to the headline) — "Your copying finding is a replication of arXiv 2607.21943, on the same model, three weeks late, without their silence control."

Force: **high**. Same core (Qwen3-Omni), same wrong-reference direction, blind-copy 94.2%
vs our 49/53 parroting. Their silent-audio control is a stronger separator than our
audio-present-only design, and they also deliver the training remedy we cannot.

Neutralizing evidence and posture:
- **Concede priority explicitly and cite them as the phenomenon reference.** Do not re-claim it.
- Retain three separators, each verifiable from their text: (a) their carrier is *synthetic
  overlap + noise* multi-speaker attribution (SparseLibriMix2 + WHAM, AMI); ours is *clean-ish real
  long-form monologue* with named-entity references from Earnings21/22 — a regime where the audio is
  *not* degraded, so copying cannot be excused as acoustic difficulty; (b) their context is the
  **full answer-bearing transcript**, ours is a **narrow entity-shaped reference** at a routed
  aperture, i.e. a deployment-legal supply object rather than a leak; (c) they never test a
  verification framing — their only prompt safeguard, "clues are automatic and fallible", is
  *unablated setup*, and copying persists at 94.2% *despite* it. Point (c) can be turned into
  supporting evidence for our claim rather than a threat.
- Run the **silence control** on our own aperture before any write-up. It is cheap, it is now
  the field-standard control, and its absence is the easiest desk-reject.

### Attack 2 (fatal to the null) — "arXiv 2602.11488 shows prompt framing moves text dominance from 19.0% to 3.8%. Your verify-vs-bias parity just means both your framings were weak."

Force: **high**, and this is the most actionable attack.

Neutralizing evidence and posture:
- **Partially concede.** Our verify framing most plausibly sits near their *baseline* rung
  ("transcript may contain errors", TDR 19.0%), not near their *adversarial* rung ("DELIBERATELY
  CORRUPTED", 3.8%). Our factorial did not include an adversarial-corruption rung, so we cannot
  claim we exhausted the framing space. Restate the claim as bounded: *within the
  attribution-neutral framing family, verify and bias framings are indistinguishable at wrong-
  reference exposure* — not *no framing can work*.
- Counter-evidence we do hold: their **audio-first** framing (force transcription before answering)
  *raised* TDR to 33.0%, i.e. the intuitively-correct "listen first" instruction is actively
  harmful. That is direct support for our conclusion that prompt-level control of evidence use is
  unreliable and non-monotone in the intuitive direction.
- Second counter: their task is a **binary forced choice** over a single flipped semantic element on
  1.5–8 s clips. Framing has an easy lever there (pick the other option). In **free-form
  transcription** of entity-dense long-form speech there is no alternative hypothesis to fall back
  on — the model must *generate* the un-copied string. Our 49/53 byte-identical rate is evidence
  that the copy pressure is stronger in generation than in selection. That regime difference is a
  defensible reason the framing lever fails for us and works for them.
- **Concrete remedy, not just a rebuttal:** if the verify lane is ever reopened, pre-register an
  adversarial-corruption framing rung ("the supplied reference is deliberately corrupted") plus a
  neutral and a bias rung, measure byte-identical parroting per rung, and treat 2602.11488 as the
  registered expected-effect prior. This converts Attack 2 into an experiment.

### Attack 3 (fatal to the framing of C3) — "arXiv 2607.13477 already showed frozen Qwen3-Omni judges follow wrong supplied references and are not audio-grounded, with a chance-normalized metric you don't have. Your 'verification does not exist' is their conclusion."

Force: **medium-high**. They audit Qwen3-Omni-Instruct and -Thinking directly, define
`RF(M) = Pr[ŷ = r | r ≠ y]` with chance normalization, vary prompt placement, and conclude that
LALM verdicts are not audio-grounded.

Neutralizing evidence and posture:
- Their carrier is **closed-label classification judging** — 8-way emotion on 240 acted RAVDESS
  clips, 4-way language ID, MOS, speaker triplets. Guessing baselines exist, hence their
  chance-normalization. Our carrier is **open-vocabulary transcript content** where chance
  agreement is ~0 and the copy is *literal string reproduction*; RF has no direct analogue and
  byte-identity is the natural metric. The two audits are complementary, not duplicative.
- They vary **placement**, we vary **framing semantics**; neither subsumes the other.
- Decisive separator: they stop at "the judge is not grounded". **We are the only ones who ask what
  the ungroundedness costs the end task.** RIR = 0 over 54 delivered-correct opportunities and the
  −0.28 pp vs −12 pp decomposition are not derivable from their audit. Lead with the utility bound
  and cite them for the grounding failure.
- Adopt their vocabulary rather than minting ours: "reference-anchor bias" / "reference-follow rate"
  (2607.13477), "perception bypass" / "blind-copy rate" (2607.21943), "text dominance" / TDR
  (2602.11488). Coining a fourth name for the same behaviour is a credibility cost with no gain.
  This mirrors the existing HER/RIR caveat: cite the lineage (Edit Rate / Improve@Edit /
  Worsen@Edit, arXiv 2508.07285), claim no metric novelty.

---

## 6. Consequences for the SAEA plan

1. **C3 must be rewritten, not merely narrowed.** "Verified use" as an operator is dead *and* the
   death is prior-published. Replace with a measured, cited bound: prompt-level verification on an
   API-only frozen core is (a) known to fail — three 2026 priors — and (b) worth ≤0.28 pp on our
   aperture even if perfected. C3 becomes a *closed* negative sub-claim with external support,
   which is cheaper to defend than an open one.
2. **The differentiation load shifts further onto N1 routing + N2 targeted supply + legal
   provenance.** Reinforced by two independent sources: 2607.21943's answer-overlap screen (they
   reject directly copyable answer strings — the same deployment-legality instinct as our
   zero-gold metadata rosters) and EChO-Agent's ablation ordering (evidence integration ≫
   verification).
3. **Mandatory additions before any write-up touching the copy finding**: a silent-audio control on
   our own aperture (2607.21943 makes this table stakes), and adoption of at least one prior metric
   name so the result is legible to reviewers.
4. **The DEMO lane inherits a warning.** 2602.11488's audio-first result (forcing transcription
   *raises* text dominance to 33.0%) and 2607.21943's perception bypass both say that
   demonstrations containing answer-bearing text can be copied rather than learned from. If the DEMO
   bank is built, the mandatory reject-case demonstrations must be paired with a silence control and
   an answer-overlap screen, or the whole lane will replicate perception bypass at few-shot scale.
5. **Do not consume MMAR / EChO-Agent's tool stack.** MMAR is sound+music+speech composite —
   outside the SAEA research boundary. EChO-Agent is a citation and a design corroboration only.

---

## 7. Reference list assembled by this cluster

| ID | Title | Date | Role for SAEA |
|---|---|---|---|
| arXiv 2607.21943 | Listen, Do Not Copy: Internalizing Audio-Grounded Scaffold Context… | 24 Jul 2026 | **Priority holder** for the copying phenomenon on frozen Qwen3-Omni; source of the silent-audio control; GDPO training fix. |
| arXiv 2607.13477 | Auditing Protocol-Level Shortcuts in LALM Judges for Speech Evaluation | 15 Jul 2026 | **Priority holder** for "frozen LALM verification is not audio-grounded"; reference-follow rate; Qwen3-Omni judges. |
| arXiv 2602.11488 | When Audio-LLMs Don't Listen: Cross-Linguistic Modality Arbitration | Feb–Mar 2026 | **Priority holder** for prompt-framing × audio-text conflict; TDR; the adversarial-framing remedy we did not test. |
| arXiv 2606.18924 | Who Wins the Conflict? Mechanistic Interpretability of Text Bias | 17 Jun 2026 | Mechanism: text suppresses intact audio in late layers; the only working lever needs weight access — supports our API-only futility argument. |
| arXiv 2606.15141 | EChO-Agent (Interspeech 2026) | Jun 2026 | Training-free agentic audio QA; **verification is text-LLM-judged, never re-consults audio**; ablation ranks verification last. |
| arXiv 2504.14858 | AlignRAG / Retrieval is Not Enough | Apr 2025 | Text-RAG: evidence misalignment fixed by a **trained** critic, not by prompting. |
| OpenReview 9U51rOnGko | Counterfactual Reasoning for RAG (CF-RAG), ICLR 2026 | 2026 | Text-RAG: "Correlation Trap"; harness-executed counterfactual controls + arbitration. *Primary text not retrieved — verify before citing.* |
| arXiv 2310.01798 | LLMs Cannot Self-Correct Reasoning Yet (ICLR 2024) | Oct 2023 | Anchor negative result; our VOID is its speech-carrier instance. |
| arXiv 2508.07285 | Post-ASR edit-quality survey (Edit Rate / Improve@Edit / Worsen@Edit) | 2025 | Existing lineage for HER/RIR; no metric-novelty claim. |
| arXiv 2512.21828 / 2604.12398 / 2606.00507 / 2505.16212 | Contextual biasing & LLM ASR correction (hotword retrieval + RL; bias-word position prediction; latent reasoning; child conversations) | 2025–2026 | Over-correction / error-propagation lineage for the N2 supply lane; "SNR augmentation curbs over-reliance on the LLM text prior". |

**Unverified items flagged for follow-up**: CF-RAG details (search snippets only, OpenReview
blocked); exact clip durations in 2607.21943; the verbatim audio-first instruction in 2607.21943
(not published); EChO-Agent verification prompt (not published).
