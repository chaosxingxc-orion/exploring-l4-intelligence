# Paralinguistic Suppression in Omni Speech-LLMs — Adversarial Survey (W4)

How speech is injected into / read out of a frozen omni model, and **whether** text-alignment + pooling
suppress speaker/emotion. Answers the two questions behind the ICL finding ("the model over-attends to
the speech/content stream and ignores the text instruction"). Companion to [[Omni-Embed-Model-Dossier]]
(architecture/I-O contract), [[W4-Training-Free-RL-Feasibility]] (operator math),
[[2026-06-23-omni-embed-speech-disentanglement-1.2.1]] (ICL diagnostics).

## 0. How to read this page (the adversarial method) — for humans AND AIs

**This page is written adversarially: nothing here is asserted without its strongest counter-argument.**
Every load-bearing claim is laid out as **Claim → For (steelman) → Against (the attack) → Verdict +
confidence → Decisive test (what would falsify/confirm it)**. The point is that a human or an AI agent
picking this up can see not just *what we believe* but *how hard it was attacked and where it could still
break* — so the next contributor knows exactly which front to push.

**Provenance & attrition (the adversary did real work).** The literature half (§4) is the output of a
77-agent workflow (`wf_6694eca5-de9`): 7 blind exploration angles → **62 candidate sources** → deep-read
**12** → **76 extracted claims** → each load-bearing claim faced **3 independent skeptics prompted to
*refute* it** (default `refuted=true` if unsubstantiated), majority-refute = killed → **11 claims
survived**. What the adversary killed: single-source over-generalizations, mis-quoted numbers,
cherry-picked benchmark subsets, and several plausible-but-unverifiable 2026 arXiv IDs. The empirical
half (§3) is our own weight-free probe, run on two seeds precisely to attack its own first result.

**Status legend:** ✅ self-verified (own run) · ◐ workflow / 3-vote-verified · ⚠ inferred / assumption ·
✗ refuted. **Confidence:** high / med / low. Citations are bare arXiv IDs (e.g. `2602.23136`).

## 1. The assertion → five falsifiable sub-claims (the frame)

User assertion: *"all omni/speech LLMs align audio to text, so on speaker-ID (SID) and emotion (SER)
their statistics drop sharply, and the paralinguistic signal is lost at the pooling stage."* We refuse
to grade this as one yes/no — it bundles five separable claims, and they do **not** get the same verdict:

- **C1 — training objective:** ASR/contrastive alignment lowers linearly-decodable emotion/speaker info
  in the final/pooled vector *relative to an SSL acoustic baseline* (wav2vec2/HuBERT/WavLM/emotion2vec).
- **C2 — pooling method:** plain **mean** pooling is *itself* a loss term — a better pooling over the
  *same* frames recovers accuracy, independent of the training objective.
- **C3 — suppressed vs destroyed:** the info is *present in intermediate layers but attenuated at the
  output* (recoverable by layer/probe), versus genuinely *absent* (destroyed). May differ per factor.
- **C4 — monotonicity:** degradation tracks the *degree/type* of text-alignment across model families.
- **C5 — fixes:** which targeted methods recover the gap, by what mechanism, and at what license cost.

## 2. D1 — How the embedding is injected & read out (✅ verified on our own model)

**Claim.** Speech enters the model as a *sequence of N audio-token vectors*; the embedding it returns is
*one pooled 1-D vector* — and conflating the two is what makes "give emotion/speaker a 1-D vector, less
interference" sound reasonable.

**For (own run, `1005_MTI_NEU_XX.wav`, 3.37 s).** Injection = **51 contiguous `<|AUDIO|>` tokens**
(id 151646), BOS/EOS-wrapped (151647/151648), interleaved with text in one **bidirectional** Qwen2.5-Omni
Thinker sequence (len 69); count ~fixed (~51) for 2.5–3.5 s clips, not linear in duration. Read-out =
**masked-mean → L2-norm → one 2048-d vector**; the model exposes **37 hidden states** each (1, 69, 2048).
✅

**Against (the honest caveat).** Is the "one pooled vector" really the whole story? A manual masked-mean
of the final layer reproduces `encode_document` at cosine **0.879**, *not* 1.0 — because `encode_document`
auto-prepends the `passage:` prompt and our manual path didn't. So the readout is prompt-sensitive; the
"single pooled vector" abstraction is exact only with the matching prompt (rises to ≈1.0). This
*corroborates* the Dossier rather than contradicting it, but it means the pooled vector is a function of
(audio ⊕ prompt), not audio alone.

**Verdict.** HOLDS ✅. **Consequence that reframes the user's premise:** the pooled 1-D final-layer vector
is *exactly where speaker/emotion die* (§3), because masked-**mean** lets content variance dominate.
"Collapse to 1-D" is not noise reduction — it is where the loss happens. The lever is **pooling-method ×
layer × source**, not dimensionality; and for a generative readout the *full N-token sequence* is better
for paralinguistics (the LM can attend to salient frames), the opposite of "give it 1-D."

## 3. D3 — Our pooling-method probe (✅ own run, two seeds, self-attacked)

**Claim.** Plain mean pooling is the loss term; a better weight-free pooling over the same frames recovers
speaker/emotion (tests C2/C3 on *our* model, the ablation the literature never ran).

**Setup.** `scripts/pool_method_probe.py` + `layer_probe.extract_pooled` (W4 repo). Frozen
`omni-embed-nemotron-3b`, CREMA-D, dev 600 / test 300, kNN (k=5), 95% bootstrap CIs, **weight-free**.
Best-layer accuracy (chance: emotion .167, speaker .011, content .083), seed 42:

| pooling (audio-token) | emotion | speaker | content |
|---|---|---|---|
| mean (full-seq, deployed) | 0.400 (L0) `[.350,.453]` | 0.043 (L36) `[.023,.070]` | 0.990 |
| audio-token mean | 0.400 (L0) | 0.043 (L32) | 0.990 |
| audio **std** only | 0.367 | 0.040 | 0.997 |
| audio **stats** (mean+std) | 0.403 | 0.047 | 0.990 |
| audio **attentive-stats** (weight-free) | **0.513 (L16)** `[.460,.570]` | 0.067 (L16) | 0.933 |

**For.** mean=std=stats tie (2nd-order statistics alone do nothing), but **attentive-statistics at
mid-layer L16 lifts emotion 0.40 → 0.513**, CI-separated from baseline; at that same L16 **content
collapses 0.99 → 0.26** — the attention re-weights frames toward the paralinguistic-salient ones the mean
washes out. Directionally this is the C2 mechanism.

**Against (we attacked our own result with a second seed).** Seed 7: attentive again **peaks at L16 for
emotion (0.447)** and content again collapses — but the gain is **0.447 `[.393,.500]` vs mean 0.407
`[.353,.460]`, CIs now OVERLAP**. So the emotion gain is *directionally robust but modest and
seed-sensitive* (CI-separated at seed 42, within noise at seed 7), not a clean win. And **speaker stays
floored ≤0.067 under every method × layer × seed** — attentive pooling cannot lift it.

**Verdict.** C2 **partially holds (hedged)** ✅ — uniform mean is the loss term, attentive *mid-layer* is
the best weight-free lever but helps only *emotion*, modestly; std/stats don't help. C3 **holds,
per-factor (both seeds)** ✅ — emotion suppressed-but-recoverable, speaker destroyed. **Decisive next
test:** an *ordered-trajectory / multi-vector* readout (literature's C-Gate gets +61pp that way) vs our
single-vector attentive +0.04–0.11 → does multi-vector close the gap, and does it ever lift speaker?
(Predicted: helps emotion a lot, speaker not at all.) MLflow `2c61b2f1` (seed42), `21453cb1` (seed7).

## 4. D2 — Literature adjudication, adversarial (◐ 3-vote verified)

**Headline:** the assertion is **right in direction, too strong in mechanism, and sharply per-factor.**
Paralinguistics is mostly **suppressed/unread at the pooled-vector + decoder stage — not "lost at
pooling" nor "destroyed."** "Lost at pooling" is correct for **emotion** (fix the readout) and *wrong* for
**fine speaker-ID** (the objective never wrote a usable speaker direction — fix the source/encoder).

---
**C1 — alignment suppresses paralinguistics vs SSL.**
- **For:** through the aligned stack, content amplified **+92–95%** while speaker degraded **−8 to −39%**
  `2602.23136`; CLAP-contrastive encoder preserves paralinguistics where ASR encoders degrade `2605.27772`;
  SSL baselines retain it (emotion2vec ~71.8% IEMOCAP linear probe `2312.15185`; speaker survives SSL
  final layers `2501.05310`; `2111.02735`); omni-LLMs collapse to lexical cues, near-chance on pure
  paralinguistics `2510.10444`.
- **Against:** **no omni-LLM paper runs the strict same-audio same-probe SSL-vs-aligned contrast** — the
  "relative to SSL" clause is assembled across different papers/audio/metrics, i.e. *inferred*. And the
  strong form is partly false: the info often **survives to the final aligned layer** (probes 3–55×
  chance `2602.23136`), so it is *present-but-unread at the readout*, not "reduced in the representation."
- **Verdict:** PARTIALLY HOLDS · MED. **Falsifier (our planned baseline):** run emotion2vec/WavLM/ECAPA
  vs the omni pooled vector on the *same* CREMA-D split, *same* probe. SSL ≫ aligned ⇒ C1; comparable ⇒ ✗.

**C2 — mean pooling is the loss; better pooling recovers.**
- **For:** C-Gate ordered-trajectory **16.8 → 77.7%** (+61pp) on RAVDESS, frame-shuffle collapses it to
  22% — causal proof for emotion; mean vector near-degenerate (per-frame cos~0.98 to the LLM mean token)
  `2606.09366`; attentive pooling SER +0.85–2.35 UA `2602.06000`,`1803.10963`; PCLM layer-mix AF3 17.4 →
  65% `2605.27772`; **our D3** (attentive mid-layer lifts emotion).
- **Against:** **split by factor and hedged.** Speaker: mean pooling stays chance, audio-only pooling
  ±2.1% `2602.23136`, stats helps speaker only *inside* a disentangled codec `2508.08399`. The two
  dedicated layer-wise omni studies `2603.11947`,`2602.23136` **use mean pooling only and run no ablation
  — they cannot be cited FOR C2.** Our D3: std/stats tie with mean; attentive helps only emotion, modest,
  seed-sensitive.
- **Verdict:** PARTIALLY HOLDS (refined) · MED. **Falsifier:** mean-vs-stats-vs-attentive-vs-trajectory
  ablation on one frozen omni for *both* factors (D3 did the first three; trajectory/multi-vector open).

**C3 — suppressed-but-present vs destroyed.**
- **For (best-evidenced):** speaker/coarse-paralinguistic probes run **3–55× chance at every layer
  including the final one**, and the mechanism is explicitly *a decoder with no learned response to
  non-text directions, NOT active deletion* `2602.23136`; Whisper layer-9 KNN multi-speaker **detection
  36 → 99% F1** `2508.15882`; live signal in layers 0–14 `2603.11947`; SSL speaker survives final layers
  `2501.05310`; our D3 anchor.
- **Against (defeats the blanket version):** holds for emotion + coarse speaker *presence*, but **fine
  speaker-IDENTITY is NOT recovered by any layer/probe** (our 37-layer × 4-pooling sweep ≤0.067;
  Modality-Collapse + Whisper-probe agree) — closer to "inaccessible / effectively destroyed in the
  pooled vector."
- **Verdict:** HOLDS, per-factor · HIGH. **Falsifier:** *any* weight-free readout that lifts fine
  speaker-ID off the floor on a frozen ASR-aligned vector. None found across 4 independent lines.

**C4 — monotonicity with degree of alignment.**
- **For:** encoder-objective gradient (CLAP AF2 30.85% > ASR AF3 17.4% / Qwen2-Audio 14.85% `2605.27772`;
  paralinguistic-augmented Step-Audio2 top, StepEval 76.55 vs Qwen-Omni 44.18 `2507.16632`); theoretical
  mechanism (degradation ~ encoder↔text distance) `2602.23136`.
- **Against:** **no controlled cross-paradigm curve**; two instruction-tuned LALMs show *identical*
  suppression `2603.11947`; the ordering is a cross-study patchwork (different audio/tasks/metrics). The
  confident "tracks the degree of alignment" overstates.
- **Verdict:** PARTIALLY HOLDS · LOW (weakest claim). **Falsifier:** one study sweeping ASR-contrastive →
  instruction-tuned → paralinguistic-augmented on the *same* audio/metric.

**C5 — targeted fixes recover the gap.**
- **For:** quantified recovery across all six mechanism classes (§6), with a consistent asymmetry —
  emotion recoverable by (b)(d)(e)(f); fine speaker-ID only by (a)/(c). E.g. ECAPA-LLM **1.03% EER**
  `2603.10827`; C-Gate +61pp; PE-FT emotion PA-rate **74.5–80.5%** `2603.11947`; forced-choice LoRA
  CREMA-D emotion **17.3 → 61.8%** (+44.5pp) while **speaker unmoved** `2602.23136`.
- **Against (the training-free caveat that matters for us):** most strong fixes **modify weights**
  (LoRA/selective FT) — they bound what is *recoverable*, **not what is *training-free*-recoverable**; the
  training-free-readout vs weight-tuned ceilings are unseparated. And several 2026 method papers are
  paper-only / unreplicated. So "fixes exist" is solid; "*training-free* fixes exist for speaker" is **not
  supported** — every speaker fix needs training or an external encoder.
- **Verdict:** HOLDS · HIGH (with the training-free caveat). **Falsifier:** a purely training-free method
  that surfaces fine speaker-ID from a frozen aligned vector. None exists; evidence leans toward impossible.

## 5. Verifiable-claim registry (machine-readable, for AIs)

| id | claim (paraphrased) | factor | verdict | conf | key FOR | key AGAINST | decisive test |
|---|---|---|---|---|---|---|---|
| C1 | alignment lowers decodable paralinguistics vs SSL | spk,emo | partial | med | 2602.23136, 2605.27772, 2312.15185, 2501.05310 | no same-audio SSL contrast; info survives final layer | same-audio SSL-vs-aligned probe on CREMA-D |
| C2 | mean pooling is the loss; better pooling recovers | emo (not spk) | partial(refined) | med | 2606.09366, 2602.06000, D3 | std/stats tie; speaker fails; omni studies mean-only | trajectory/multi-vector readout, both factors |
| C3 | present mid-stack, attenuated at output, recoverable | emo + coarse-spk yes; fine-spk no | holds(per-factor) | high | 2602.23136, 2508.15882, 2603.11947, D3 | fine speaker-ID unrecovered by any readout | any weight-free fine-speaker readout |
| C4 | degradation monotone in alignment degree | all | partial | low | 2605.27772, 2507.16632, 2602.23136 | no controlled curve; identical suppression across 2 LALMs | one same-audio cross-paradigm sweep |
| C5 | targeted fixes recover the gap | emo broadly; fine-spk only (a)/(c) | holds | high | 2603.10827, 2606.09366, 2603.11947, 2602.23136 | most fixes train weights; speaker has no training-free fix | training-free fine-speaker recovery |
| D1 | injection = N-token seq; readout = pooled 1-D | n/a | holds | high(✅) | own run (51 tokens, 37 layers, 2048-d) | parity 0.879 w/o `passage:` prompt | — |
| D3 | attentive mid-layer pooling recovers emotion weight-free | emo (not spk) | partial(hedged) | med(✅) | seed42 0.513 CI-sep | seed7 0.447 CI-overlap; speaker floored | multi-vector / more seeds / MELD |

## 6. The six-class fix taxonomy — with public availability (so collaborators can act)

Emotion is recoverable by almost every class; **fine speaker-ID only by (a) external encoder or (c)
disentangled codec.** Availability verdicts (web-checked): OPEN = code+weights public.

| class | mechanism | best for | representative recovery | refs | obtainable? |
|---|---|---|---|---|---|
| (a) external speaker/paralinguistic encoder fused in | inject frozen ECAPA / x-vector (or emotion encoder) | **fine speaker-ID (only lever)** | ECAPA-LLM **1.03% EER** (vs 21.9–45.6% off-the-shelf) | 2603.10827, 2005.07143 | ECAPA **OPEN** (SpeechBrain, Apache-2.0); ECAPA-LLM method PAPER-ONLY |
| (b) pooling / aggregation fix | ordered-trajectory / attentive / layer-mix | **emotion** | C-Gate 16.8→77.7%; PCLM AF3 17.4→65%; attentive +0.85–2.35 UA | 2606.09366, 2605.27772, 1803.10963 | PCLM PARTIAL (code); C-Gate PAPER-ONLY; attentive-pool trivial to reimplement (our D3) |
| (c) disentangled codec / representation | dedicated speaker/prosody stream | speaker, prosody | SKQ3+ SV EER 2.36%; FACodec factorization | 2403.03100, 2308.16692, 2505.19273 | FACodec/SpeechTokenizer **OPEN** (MIT/Apache); Eta-WavLM method-only |
| (d) auxiliary-loss / multi-task | SER/SV head or RL objective | emotion + coarse | PE-FT 74.5–80.5%; forced-choice LoRA +44.5pp; PALLM RL | 2603.11947, 2602.23136, 2603.15981 | Step-Audio2 **OPEN**; PE-FT/PALLM PAPER-ONLY |
| (e) paralinguistic adapter / localized tuning | LoRA on the live-signal band | emotion + coarse (efficient) | PE-FT layers 0–14 beats full at ~46% fewer params | 2603.11947 | PAPER-ONLY (reimplementable) |
| (f) generative readout / probe-select | decode / probe a salient layer | emotion + coarse; speaker *presence* | WavBench emotion 75–93%; Whisper KNN detection 99% F1 | 2410.01162, 2508.15882 | base omni models **OPEN** (Qwen-Omni/Step-Audio2/etc.) |

**Frozen feature extractors immediately usable (OPEN, permissive):** emotion2vec (`2312.15185`),
ECAPA-TDNN (`2005.07143`), WavLM/HuBERT/wav2vec2, Whisper, FACodec (`2403.03100`), SpeechTokenizer
(`2308.16692`). These — not the paper-only method names — are what we can actually wire in.

## 7. Residual open adversarial fronts (where to attack next)

1. **No strict same-audio SSL baseline** exists in the literature (C1 is inferred). → run emotion2vec /
   WavLM / ECAPA on the *same* CREMA-D split as the omni vector. Our natural W4 baseline.
2. **C2 ablation incomplete:** mean/std/attentive done (D3); **ordered-trajectory / multi-vector** readout
   untested on a frozen omni — the literature's biggest emotion lever (+61pp) and our likely emotion win.
3. **Single-vector vs multi-vector retrieval conflict:** can an emotion-trajectory readout coexist with a
   single retrieval embedding (W4's design)? Late-interaction vs single-vector is untested.
4. **Is fine speaker-ID *ever* training-free-recoverable** from a frozen aligned vector, or is the
   direction simply never written? Evidence leans "never written," but no impossibility proof exists.
5. **emotion2vec-fusion** (the emotion analogue of ECAPA-LLM) is unquantified — does external-encoder
   fusion give emotion the same near-complete recovery it gives speaker-ID?
6. **The W1→W4 RL bridge** (RL / same-different-speaker auxiliary that rewards the orthogonal speaker
   subspace) is *proposed-only* in the literature — the highest-value unmeasured fix for our own thesis.

## 8. Implication for W4 (per-factor routing — D1+D2+D3 converged)

- **Emotion → Operator A is viable, but NOT via the current single mean vector.** The mean vector is
  near-degenerate; the big lever is **ordered-trajectory / multi-vector / late-interaction readout**
  (C-Gate +61pp) + layer selection (0–14) + generative readout — all W1-pattern-compatible. Tension: a
  single retrieval vector vs trajectory preservation; W4 likely needs a multi-vector / per-factor head.
- **Speaker → the hard wall and the boundary of the training-free thesis.** The anchor ~0.04 is *expected*:
  no pooling/layer/readout on an ASR-aligned pooled vector surfaces fine identity (convergent: our sweep,
  `2602.23136`, `2605.27772`). Speaker subspace is ~orthogonal to content (|cos|~0.13, `2305.12464`) — good
  geometry, but the objective never wrote a usable speaker direction. Only **external speaker encoder** or
  **disentangled codec** work, both non-training-free — or the **W1→W4 RL bridge**.
- **Net correction:** "lost at pooling" is right for **emotion** (fix the pool/readout) and wrong for
  **speaker** (fix the source/encoder). Updates [[Per-Work-Status]]: emotion → "**Operator A with a richer
  readout** (multi-vector/trajectory/layer/generative) before B"; fine speaker → B / external channel.

## 9. 探针有效性基础文献（审计补课，2026-07-11） — Probing-validity foundations

**Why this page is the home (not the Dossier or the Research-Plan).** The 2026-07-10 adversarial audit
(ticket #28) found that the W4 literature chain nowhere cites the methodological results that separate
*"a probe can read a factor"* from *"the representation is disentangled"* — they appear only inside the
audit docs themselves. Of the three W4-facing pages, **this survey is where that exact inference is
made**: every load-bearing verdict here (C1/C2/C3 in §4, D3 in §3, the §5 registry) is *derived from
probe accuracy* across layer × pooling. [[Omni-Embed-Model-Dossier]] is a model fact-sheet
(architecture / I-O) and [[W4-Research-Plan]] is an execution-wave plan; neither converts probe read-outs
into suppression/disentanglement claims, so the foundations belong here, adjacent to §4/§5. These five
references are the controls that gate the audit's **L0–L4 claim ladder**
([[2026-07-10-stage1-adversarial-research-audit]]: L0 factor-decodability → L1 accessible-readout →
L2 task-selectivity → L3 disentanglement → L4 deployable-activation). The thesis of this whole section:
**probe accuracy is L0 only; §3/§4's numbers do not by themselves clear L1, let alone L3.**

- **Locatello et al. 2019 `1811.12359` (ICML 2019) — "Challenging Common Assumptions in the Unsupervised
  Learning of Disentangled Representations."** Proves (theorem + a ~12,000-model study) that *without*
  inductive biases or supervision, disentanglement is fundamentally **unidentifiable** — infinitely many
  equally-good factorizations fit the same data, so high downstream/probe scores never *imply* a
  disentangled representation. **L-ladder implication:** this is the impossibility result behind the **L3**
  bar — a diagonal-dominant conditioning×probe matrix (§8, however high its accuracy) is *not* evidence of
  disentanglement; L3 needs the audit's supervision-grounded controls (target-up **and**
  nuisance-leakage-down **and** counterfactual intervention), because probe accuracy alone (L0) is
  identifiability-blind.

- **Hewitt & Liang 2019 `1909.03368` (EMNLP 2019) — "Designing and Interpreting Probes with Control
  Tasks."** A probe's accuracy conflates what the *representation* encodes with what the *probe* itself can
  learn; they add **control tasks** (random label assignments) and score **selectivity = task-acc −
  control-acc**, showing high-capacity probes reach high accuracy even on random labels. **L-ladder
  implication:** our kNN/linear numbers (§3, C1–C3) are uninterpretable without a selectivity control —
  **L1** ("accessible readout") must be redefined as *high selectivity on a matched control task*, not raw
  accuracy; a "speaker ≈ chance" floor and an emotion "gain" only count if they beat their own control
  task.

- **Voita & Titov 2020 `2003.12298` (EMNLP 2020) — "Information-Theoretic Probing with Minimum Description
  Length."** Replaces accuracy with **MDL** — the codelength to transmit labels given the representation —
  which jointly measures *how well* and *how easily* a factor is extracted and is far more stable to
  probe/hyper-parameter/**seed** choices than accuracy. **L-ladder implication:** MDL is the concrete
  **L1** control ("low-complexity probe stable on group-held-out"), and it directly disciplines D3's
  **seed-sensitive** attentive-pooling emotion result (0.513 vs 0.447 across seeds → one
  codelength verdict instead of two accuracies); adopt MDL as the *primary* read-out metric for any L1/L2
  claim, accuracy as secondary.

- **Pimentel et al. 2020 `2004.03061` (ACL 2020) — "Information-Theoretic Probing for Linguistic
  Structure"** *(probe-capacity ref 1).* Frames probing as estimating mutual information
  I(representation; factor), under which the *most expressive* probe is the correct choice and control-task
  selectivity is theoretically questioned — the opposite prescription to Hewitt & Liang. **L-ladder
  implication:** the **L0→L1** boundary is genuinely contested, so W4 should report *both* a
  capacity-controlled selectivity number (Hewitt–Liang) *and* an MI/MDL estimate (Pimentel /
  Voita–Titov): a factor present in the MI sense but readable only by a high-capacity probe is **L0**, not
  the **L1** "accessible readout" the disentanglement story needs.

- **Belinkov 2022 `2102.12452` (Computational Linguistics) — "Probing Classifiers: Promises, Shortcomings,
  and Advances"** *(probe-capacity ref 2 / synthesis).* The field survey tying the above together: probing
  shows correlation, not causal use; accuracy is **capacity-confounded**; it prescribes control tasks,
  information-theoretic measures, and **causal/intervention** probing before any "the model represents X"
  claim. **L-ladder implication:** this is the checklist for the whole **L0→L3** climb — it underwrites the
  audit's demotion of W4 from "disentanglement" to "readout availability / suppression / selective-readout
  limits," and its intervention requirement *is* the **L3** gate; cite it as the umbrella justification
  that probe accuracy (L0) is the weakest rung.

**Consequence for this survey (registry patch).** C1/C2/C3 and D3 stay *directionally* valid but are
**L0 / near-L1 evidence** — probe-accuracy read-outs with no selectivity, MDL, or counterfactual control.
Before any §8 wording climbs to L2/L3 ("selective", "disentangled"), re-establish each on: (a)
Hewitt–Liang selectivity vs a CREMA-D control task, (b) Voita–Titov MDL/codelength in place of raw
accuracy (kills the D3 seed-sensitivity), (c) a counterfactual/interventional check for L3. This adds a
**residual front** to §7: *no probe on this page is capacity- or selectivity-controlled — the single
largest validity gap under §3/§4.*

---

## 中文

冻结 omni 模型如何「注入/读出」语音，以及文本对齐+池化是否压制说话人/情感。**本页用对抗方式撰写：任何
结论都连同它最强的反驳一起给出。** 每条关键论断的结构是 **断言 → 支持(steelman) → 反驳(进攻) → 裁决+
置信度 → 决定性证伪实验**——这样人或 AI 接手时不仅看到「我们信什么」，还看到「被攻击到什么程度、还可能
从哪里崩」。配套 [[Omni-Embed-Model-Dossier]]、[[W4-Training-Free-RL-Feasibility]]、
[[2026-06-23-omni-embed-speech-disentanglement-1.2.1]]。

**§0 对抗方法与衰减：** 文献部分(§4)是 77-agent workflow 产物——7 个盲角 → 62 候选 → 深读 12 → 76 条
断言 → 每条承重断言被 **3 个独立怀疑者主动证伪**（默认 refuted），多数证伪即 kill → **存活 11 条**。被
杀的：单源过度泛化、引错数字、挑拣基准子集、查无实据的 2026 arXiv ID。实测部分(§3)用两个 seed 自我攻击。
状态标记 ✅自验证 ◐工作流核验 ⚠推断 ✗已证伪；置信度 高/中/低。

**§1 五个可证伪子命题：** C1 训练目标（对齐降低末层情感/说话人线性可解码信息，对照 SSL）；C2 池化方法
（均值池化本身是损失项，更好池化能在同一批帧上找回）；C3 压制 vs 销毁（中层在场末层衰减=可恢复 ↔ 全程
缺失=销毁，逐因子不同）；C4 单调性（随对齐程度变化）；C5 修复（哪些方法、什么机制、许可代价）。
**它们不共享同一个裁决。**

**§2 注入形态（D1，已自验证）：** 断言=注入是 N 个音频 token 向量序列、读出是 pooled 1 维。支持：3.37s
片段 51 个连续 `<|AUDIO|>`、37 个 hidden states、2048 维。反驳：手动末层均值 vs `encode_document` 余弦
**0.879**（缺 `passage:` 前缀），故 pooled 向量是 (音频⊕提示) 的函数。裁决：成立 ✅，且**重构了用户前提
——pooled 1 维末层正是说话人/情感被销毁最狠处**，杠杆是 池化方法×层×来源，不是维度；生成读出反而要喂完整
N 序列。

**§3 池化方法探针（D3，两 seed 自攻）：** 断言=均值是损失、更好池化能找回。支持(seed42)：均值=std=stats
打平，**attentive-统计在中层 L16 把情感 0.40→0.513**（CI 分离，同层内容 0.99→0.26）。反驳(seed7)：仍在
L16 峰值但 **0.447 vs 均值 0.407、CI 重叠**——增益温和且 seed 敏感；**说话人全方法全层 ≤0.067**。裁决：
C2 部分成立(打折) ✅，C3 逐因子成立 ✅；下一决定性实验=有序轨迹/多向量读出（文献 C-Gate +61pp）。

**§4 文献对抗裁决（◐ 3 票核验）：** 总判=方向对、机制太强、强烈逐因子；副语言是「pooled 向量+解码读出」
阶段被**压制/未读出**，非销毁。**C1** 部分(中)：方向有据（内容+92~95% / 说话人−8~−39%；CLAP>ASR；SSL
保留），但无严格同音频 SSL 对照、且信息常存活到末层 → 「表征里减少」过强。**C2** 部分修正(中)：情感的均值
退化有因果证据，但说话人失败、二阶统计打平、两篇逐层 omni 研究只用均值不能引为支持。**C3** 逐因子成立
(高)：粗粒度可恢复，细粒度说话人任何读出都救不回（≈销毁）。**C4** 部分(低，最弱)：有编码器目标梯度但无
受控曲线、两个 LALM 压制相同。**C5** 成立(高，但有 training-free 警告)：多数强修复**改权重**，只界定「可
恢复」而非「免训练可恢复」；说话人没有任何免训练修复。每条都附**决定性证伪实验**（见英文 §4/§5）。

**§6 六类修复 + 可获得性：** 情感几乎被每类救；细粒度说话人只有 (a)外接编码器 或 (c)解耦 codec。可直接用
的冻结提取器（OPEN/宽松许可）：emotion2vec、ECAPA-TDNN、WavLM/HuBERT/wav2vec2、Whisper、FACodec、
SpeechTokenizer。2026 方法论文多 PAPER-ONLY（要自己复现）。**§7 残余对抗战线：** ①缺同音频 SSL 基线
②C2 轨迹/多向量未测 ③单向量 vs 多向量检索冲突 ④细粒度说话人是否「从未写入」无证 ⑤emotion2vec 融合未量化
⑥W1→W4 RL 桥仅提案。**§8 W4 路由：** 情感→A 富读出（多向量/轨迹/层/生成）再 B；细粒度说话人→B/外接通道
或 RL 桥；「池化丢失」对情感对、对说话人错。

**§9 探针有效性基础文献（审计补课，2026-07-11）：** 本 survey 每条承重结论（§3 D3、§4 C1/C2/C3、§5 登记表）
都由 probe accuracy 推出，而 2026-07-10 审计(#28)指出全 W4 文献链缺失「probe 可读 ≠ representation
disentangled」的方法论基础（仅存于审计文档），故补入此处——[[Omni-Embed-Model-Dossier]] 是模型事实表、
[[W4-Research-Plan]] 是执行波次，都不把 probe 读出转成 disentanglement 主张。五篇及其对
**L0–L4 阶梯**（见 [[2026-07-10-stage1-adversarial-research-audit]]）的意义：Locatello 2019 `1811.12359`
（无监督解耦**不可辨识**→高 probe 分不等于解耦，是 **L3** 的不可能性底线）；Hewitt–Liang 2019 `1909.03368`
（**control task + selectivity**；高容量 probe 对随机标签也高分→**L1** 须以「匹配 control 上的 selectivity」
而非裸 accuracy 定义）；Voita–Titov 2020 `2003.12298`（**MDL/codelength** 比 accuracy 稳、抗 seed→D3 的
0.513/0.447 seed 敏感应换成 codelength；MDL = **L1** 所需控制）；Pimentel 2020 `2004.03061` 与 Belinkov 2022
`2102.12452`（probe capacity 两篇：MI 视角主张最大容量 probe、与 Hewitt–Liang 相反→L0/L1 边界有争议，须
同时报 selectivity 与 MI/MDL；Belinkov 综述把 control task + 信息论 + **因果/干预** probing 列为「表示 X」
主张的前置，其干预要求即 **L3** 闸门）。**后果：** C1/C2/C3/D3 仍方向成立但属 **L0/近 L1**，升 L2/L3 前须补
selectivity + MDL + counterfactual 控制（§7 新增残余战线：本页无一 probe 做过容量/选择性控制）。
