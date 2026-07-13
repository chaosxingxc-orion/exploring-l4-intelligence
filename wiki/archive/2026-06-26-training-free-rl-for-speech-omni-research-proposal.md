# Training-Free RL for Speech/Omni Models — Capability Activation across Model Classes

> project: exploring-l4-intelligence (cross-work: **W4** vector arm + **W1** generative arm) ·
> study: `tfrl-omni-capability-activation` · owner: Charmer · date: 2026-06-26
> status: **running** · version: **v1.0** (§1/§2/§5(T)/§6 **pre-registered/FROZEN @ v1.0**; §3 reflects the
>   Step-2 survey; §4 results / §5(E) / §7 remain **blocked-pending-provisioning**)
> companion docs: [[Project-Thesis]] · [[W4-Training-Free-RL-Feasibility]] · [[W4-Research-Plan]] ·
>   [[Decision-Log]] · [[Per-Work-Status]] · [[Validation-Experiment-Matrix]] · [[Research-Proposal-Template]] ·
>   survey archive → `wiki/survey/` ([README](survey/README.md))

> **This is a _living_ proposal, built step-by-step (never one-shot).** It follows the three core gates of
> [[Research-Proposal-Template]]. Sections are marked **[FROZEN @ vX.Y]** (pre-registered; change only by a
> logged rollback), **[TBD]** (awaiting an observation), or **[blocked]** (needs the compute env). The
> §"Belief-State" table and §"Trajectory log" are the live state of the build.

**Central question.** Which capabilities did omni / speech multimodal LLMs absorb in pretraining, and how
far can **training-free RL** (inference-time, reward-guided, **no weight or structure change**) *activate*
them — across the **two model classes** (vector/embedding vs thinker-talker/generative) — using
**in-context conditioning** (explicit task definition + few-shot demonstrations), selected by a verifiable
reward, as the primary lever?

---

## Process model — research-building as a partially-observed decision process (POMDP)

This proposal is built by the same kind of process it studies: **inference-time, reward-guided search under
partial information**, ordered by **value-of-information (VOI)**. Hidden state `s` = the true activation
landscape; belief `b(s)` = the Belief-State table (updated every step); actions = survey / feasibility-probe
/ pilot / write / rollback; observations = survey findings, pilot Δ+CI, feasibility yes/no (noisy, partial);
a contradicting observation triggers a dated **rollback**. Git commits are the rollback substrate. Terminal
= each hypothesis confirmed / refuted / scoped with reproducible, adversarially-verified evidence.

---

## Belief-State `b(s)` — live (updated every step)

Status: `prior` (assumed) · `lit` (literature-informed, Step-2 survey) · `observed` (in-house pilot) ·
`confirmed` · `refuted` · `scoped`. Confidence: low / med / high. The bold rows are this study's **open,
high-VOI** cells. Inline `(arXiv:ID)` → full link in `wiki/survey/`.

| Capability | Class | Lever (action `z`) | Estimate | Conf. | Status | Source |
|---|---|---|---|---|---|---|
| Content/ASR | vector | conditioning / pooling | probe ~1.0 | high | confirmed (native) | in-house; Whisper 2212.04356 |
| Content/ASR | generative | best-of-N / MBR (−WER) | WER↓, O(√logN) | high | lit+observed | MBR-ASR 2510.19471; BoN 2401.01879 |
| Emotion/SER | vector | pooling / layer (Op A) | 0.39→0.49 (Δ+0.097) | med | scoped-positive | in-house; layer-probe 2107.04734 |
| Emotion/SER | vector | ICL few-shot | 0.217→0.150 (hurts) | high | **refuted (closed)** | in-house; bge-en-icl 2409.15700 (corrob.) |
| **Emotion/SER** | **generative** | **task-def + k-shot + reward-select** | **present-but-suppressed** | **low-med** | **lit → pilot** | neurons 2601.03115; ALICE 2603.20433; SER-ICL 2509.08344 |
| Speaker/SID | vector | all levers | ≤0.067 (~chance) | high | **refuted (suppressed)** | in-house; mean-pool no 2nd-order stats 1803.10963 |
| **Speaker/SID** | **generative** | **ICL enrollment + reward-select** | **near-chance, ICL barely helps** | **med** | **lit (likely resists)** | spk-verif-LLM 2603.10827 |
| Language·Intent | vector | conditioning | present 0.25, not steerable | high | scoped (present-not-steerable) | in-house; INSTRUCTOR 2212.09741 |
| Intent/SLU | generative | policy-surface Op-B | MInDS +0.132; SLURP +0.330 | high | confirmed-positive | in-house cross-team |
| **Intent/SLU** | **generative** | **task-def + k-shot + reward-select** | **lexical-recoverable → easiest** | **med** | **lit → pilot** | ND11; GER+TAP 2309.15649 |
| Spoken-QA | generative | Op-B rerank | URO +0.335 | high | confirmed-positive | in-house cross-team |
| Translation/ST | both | native conditioning | strong / near-saturated | med | confirmed (native) | SeamlessM4T 2308.11596 |
| **Audio-reasoning (MCQ)** | **generative** | **task-def + k-shot + reward-select** | **under-exposed even on (B)** | **low** | **lit → pilot** | MMAU 2410.19168 |
| *mechanism* | — | inference-time RL tilts `q0` | needs a **stochastic base dist** | high | lit | KL-RL=Bayes 2205.11275; CD 2310.17022 |

**Reading of `b` after Step 2.** The survey *sharpens, and partly tempers,* H1: inference-time RL methods
all tilt a stochastic base distribution toward `q*(z) ∝ q0(z)·exp(R/β)`, which **only the generative class
possesses** (the vector class emits one deterministic vector — mechanistic basis for the asymmetry,
arXiv:2205.11275 / 2310.17022). BUT naive few-shot demos on generative audio LLMs mostly fix *format*, not
task accuracy (ALICE, arXiv:2603.20433), and audio LLMs "read rather than listen" (VoxParadox,
arXiv:2605.27772) — so the activation lever is **explicit task definition + instruction richness + reward
selection**, not raw demos, and **speaker may resist even on (B)** (arXiv:2603.10827). Easiest→hardest
activation is predicted **content/intent → emotion → speaker** (lexical-recoverable beats purely acoustic;
ND11).

---

## 1. Research Idea & Falsifiable Hypothesis **[FROZEN @ v1.0]**

**Idea.** Treat each pretrained omni model as fixed; ask, per capability and per model class, whether a
verifiable-reward inference-time search over **in-context conditioning** activates the capability. The
generative class possesses a stochastic generation distribution to tilt (Operator B); the vector class does
not (only discrete Operator-A selection over a finite pooled set).

- **H1 — model-class asymmetry of capability activation.** For an under-exposed capability `t`, training-free
  reward-guided in-context conditioning (explicit task definition + k-shot demos), selected by a **verifiable
  reward**, yields a generative-class lift `Δ_gen(t) ≥ δ_t` (paired bootstrap, p<0.05, CI LB>0) while the
  vector-class lift `Δ_vec(t)` has a CI covering 0 or is negative. *Mechanism:* the generative class is an
  autoregressive instruction-follower whose distribution is tiltable (arXiv:2205.11275, 2310.17022, 2401.01879);
  the vector class is a label-free contrastive masked-mean bi-encoder whose conditioning channel is collapsed
  (corroborated by bge-en-icl needing contrastive training, arXiv:2409.15700; INSTRUCTOR/InBedder, 2212.09741/2402.09642).
- **H2 — capability-presence map + activation ordering.** Each family's presence (probe / zero-shot > chance)
  per class, and a falsifiable **ordering of generative-class activability: content/intent ≥ emotion ≥ speaker**
  (lexical-recoverable capabilities activate more than purely-acoustic ones; arXiv:2510.10444, ND11). Speaker
  is predicted to *resist* activation even on (B) (arXiv:2603.10827) — a falsifiable boundary of the thesis.
- **H3 — lever decomposition + label-sensitivity diagnostic.** Decompose `Δ_gen` into (a) explicit
  task-definition / label-set / rubric, (b) k-shot demos, (c) instruction richness. Survey-informed prediction:
  **(a)+reward-selection dominate (b)** on vanilla frozen audio LLMs (demos mostly fix format, arXiv:2603.20433);
  and **label-sensitivity** (gold vs shuffled demo labels, arXiv:2202.12837/2205.12685) is the cross-class
  diagnostic — high on (B), ~0 on (A) (in-house: move 0.336 / label-sens 0.047).
- **Thresholds** `δ_t`, `α`: see §2 (pre-registered).

## 2. Success / Kill / Pivot Criteria (pre-registered) **[FROZEN @ v1.0]**

Per family, on the **sampled, locked test** (selection only on dev; demos drawn from a **disjoint** pool).
Significance = **paired bootstrap, 1000 resamples, α=0.05, CI lower bound > 0**; lifts reported as a function
of budget N (expected-max curve), re-scored on the held-out labels (winner's-curse guard, arXiv:1909.03004).

| Family | Metric | δ (min effect) | Go | Kill | Pivot |
|---|---|---|---|---|---|
| Content/ASR | WER↓ | 1.0 abs WER pt | Δ≥δ, CI LB>0 | CI covers 0 @ N* | escalate selector |
| ST | chrF↑ | +1.0 chrF | as above | as above | as above |
| Intent/SLU/LID | exact-match / macro-F1 | +0.05 | as above | as above | richer task-def |
| Emotion/SER | macro-F1 | +0.05 | as above | CI covers 0 @ N* | Operator-B export / accept ceiling |
| Speaker/SID | closed-set acc over chance | +0.05 | as above | CI covers 0 (expected) | report as boundary (negative result) |
| Audio-reasoning | MCQ acc | +0.05 | as above | as above | richer task-def |

**H1 cross-class gate:** H1 is *confirmed* for `t` iff `Δ_gen(t)≥δ_t` (CI LB>0) **and** `Δ_vec(t)` CI covers 0
or negative. **Mandatory controls (all must pass, else result void):** (i) **random-reward null** lift < δ
(arXiv:2506.10947); (ii) **cross-model sign-consistency** on ≥2 generative backbones; (iii) **acoustic-grounding
control** — label-shuffled demos and a transcript-only baseline to rule out lexical-prior wins (arXiv:2605.27772,
2510.10444); (iv) **contamination check** — demos/test disjoint, dataset date vs model cutoff (arXiv:2406.04244).
A met **Kill** is reported as a **negative result** (valid outcome — §7).

## 3. Survey & Positioning **[v1.0 — Step-2 survey; full archive `wiki/survey/`]**

*Produced by a 5-lane multi-agent survey workflow with per-lane adversarial verification (run `wf_d76b4901-23c`);
80 verified claims / 93 real sources archived under `wiki/survey/` ([README](survey/README.md)). Every cited id
below resolves to a real paper (verifier-checked).*

**Value of the direction.** Omni/speech LLMs acquire a broad pretraining stack — ASR/ST/LID/VAD natively
(arXiv:2212.04356, 2308.11596), SLU/spoken-QA, audio reasoning, and *weakly* paralinguistics — made explicit by
SUPERB / Dynamic-SUPERB taxonomies (arXiv:2105.01051, 2411.05361). Two classes diverge **mechanistically**: the
generative Thinker-Talker (arXiv:2503.20215, 2509.17765) keeps token-level, instruction-conditioned access and
exhibits emergent few-shot ICL (arXiv:2310.13289, 2512.23808); the vector bi-encoder (omni-embed-nemotron-3b =
Qwen2.5-Omni Thinker + masked-mean → one L2-normalized vector, arXiv:2510.03458) optimizes InfoNCE
alignment+uniformity (arXiv:2206.04769, 2005.10242), which **provably discards** features not needed to separate
contrastive positives (arXiv:2008.05659) — and mean-pooling discards the 2nd-order statistics speaker-ID needs
(arXiv:1803.10963, 2005.07143). This explains the in-house map (content ~1.0; emotion liftable by mid-layer
pooling but ICL-insensitive; speaker ~chance; intent present-not-steerable) and grounds H1's mechanism.

**Adversarial challenge (what tempers the claim).** (1) On the generative class, **off-the-shelf demos mostly
improve format compliance, not task accuracy, and can degrade it** across 6 LALMs (ALICE, arXiv:2603.20433);
(2) audio LLMs **"read rather than listen,"** following lexical priors over acoustic truth (arXiv:2605.27772,
2510.10444) — so an apparent emotion lift may be a linguistic-prior artifact; (3) genuine few-shot leverage is
**scale-emergent** (arXiv:2512.23808) or **installed by RL training** (FSA-GRPO, arXiv:2606.02615), i.e. *not
free* in a frozen base; (4) **speaker resists** even on generative LLMs (arXiv:2603.10827); (5) apparent
reward-driven lifts can be **optimization artifacts** that don't transfer across models (Spurious Rewards,
arXiv:2506.10947). These directly motivate H3 (task-definition + reward-selection over raw demos) and the §2/§6
controls (random-reward, cross-model, acoustic-grounding). Positive counter-evidence keeps H1 alive: enrollment
utterance-**label** demos help SER on a speech-LM (arXiv:2509.08344); explicit "task-activating prompting" helps
generative ASR error-correction (arXiv:2309.15649); a frozen LLM *can* perceive paralinguistics when the token
channel exposes it (arXiv:2410.01162).

**Baselines.** *Models:* vector = omni-embed-nemotron-3b (arXiv:2510.03458); generative = Qwen3-Omni / Qwen2.5-Omni
(arXiv:2509.17765, 2503.20215), Qwen2-Audio (2407.10759), SALMONN (2310.13289). *Algorithms:* best-of-N /
soft-BoN / MBR / controlled decoding / self-consistency / TTRL / TPO / JitRL (arXiv:2401.01879, 2505.03156,
2502.12685, 2310.17022, 2203.11171, 2504.16084, 2501.12895, 2601.18510); Operator-A erasure = LEACE
(arXiv:2306.03819). *Data:* SUPERB/Dynamic-SUPERB axes; CREMA-D/MELD (SER), SLURP/MInDS-14 (intent), LibriSpeech
(ASR), CoVoST2/FLEURS (ST/LID), MMAU/MMAR/MMSU (reasoning), HeySQuAD/URO (spoken-QA), AIR-Bench (2402.07729).

**Novelty-delta (one sentence).** No prior work runs a **controlled cross-model-class** test of *training-free,
reward-selected* ICL as a capability-activation lever on a **shared frozen omni backbone**: the closest priors
each cover one axis only — bge-en-icl shows embedders need *training* to use ICL (arXiv:2409.15700), MiMo-Audio
shows audio ICL emerges from *pretraining* not frozen activation (arXiv:2512.23808), and TTRL/TPO/JitRL are
*text-only, single-class* (arXiv:2504.16084, 2501.12895, 2601.18510).

**Citation registry.** Full per-claim registry with verified links: `wiki/archive/survey/2026-06-26-proposal/` — lanes
[capability-map](archive/survey/2026-06-26-proposal/2026-06-26-survey-capability-map.md) · [icl-fewshot](archive/survey/2026-06-26-proposal/2026-06-26-survey-icl-fewshot.md)
· [tfrl-theory](archive/survey/2026-06-26-proposal/2026-06-26-survey-tfrl-theory.md) · [rewards-eval](archive/survey/2026-06-26-proposal/2026-06-26-survey-rewards-eval.md)
· [novelty-delta](archive/survey/2026-06-26-proposal/2026-06-26-survey-novelty-delta.md).

## 4. Reproduced Results (Baseline + Method Pilot) **[pre-registered plan; results blocked-pending-provisioning]**

**Repro Manifest (per run).** pinned data revision (`docs/datasets.lock.json`) · code git SHA · exact env
(llama.cpp build + GGUF/mmproj rev for the generative arm; transformers/vLLM for the vector arm) · fixed seed ·
single `reproduce:` command · MLflow run ID · hardware. **(a) Baseline Reproduction** — reproduce each family's
known number on the sampled dev/test within a tolerance band; vector-arm baselines reuse the W4 archives,
generative-arm baselines = greedy decode. **(b) Method Pilot (new work)** — generative ICL-activation: action
space `𝒵_B` = {task-def / label-set / rubric} × {k-shot demos k∈{0,2,4,8}, **disjoint** pool} × {instruction
variants}; selectors `best_of_n` / `soft_bon_select` / `mbr` / `plurality_gate` (`common/.../rl/decode.py`);
verifiable rewards `asr_reward` / `exact_match_reward` / `macro_f1` / `chrf` (`rl/{reward,metrics}.py`). Locked
test once; full sweep + expected-max curve; re-score the deployed artifact; controls per §2. Each family pilot →
its own dated experiment-archive doc in the **W1/W4 repo** + a [[Validation-Experiment-Matrix]] row.

## 5. Theory & Effectiveness Gate (two-tier)

**(T) Theory [FROZEN @ v1.0].** One objective, two action spaces: `q*(z) ∝ q0(z)·exp(R(g_θ(x,z))/β)`
(KL-regularized RL = Bayesian inference, arXiv:2205.11275; controlled decoding samples it on a frozen base,
arXiv:2310.17022). **Operator A** (vector): search over conditioning / pooling / layer / linear-subspace
projection (erasure = LEACE, **arXiv:2306.03819** — corrects the `2104.01767` brief id) / candidate selection.
**Operator B** (generative): best-of-N (KL ≤ log N − (N−1)/N, win-rate ≤ N/(N+1), arXiv:2401.01879; soft-BoN
O(1/n), 2505.03156; smoothing-lens regret, 2507.05913) / MBR (SLLN O(n^−1/2), 2502.12685) / reward-guided
decoding / JitRL logit-tilt (2601.18510). **Over-optimization** is provable — gold reward peaks then falls at a
unique N* (HedgeTune 2506.19248, Gao 2210.10760) → cap N at N*. Reuse in-house Lean **T1–T6**. **New theoretical
element (the H1 mechanism):** inference-time tilting requires a stochastic base distribution; the generative
class has one, the deterministic single-vector bi-encoder does not (only finite Operator-A selection) — so the
asymmetry is structural, not incidental (arXiv:2205.11275/2310.17022/2505.03156). Finite best-of-N selectors get
a well-posedness note + the BoN bound, not a "convergence" proof.

**(E) Effectiveness [pre-registered @ v1.0; measured-not-proven].** Per family: paired Δ>0, bootstrap CI LB>0,
controls pass (§2), eval reproduces train. Established empirically on the pilot — never a theorem.

## 6. Risks, Threats to Validity & Ethics **[FROZEN @ v1.0]**

| Risk | L×I | Resolving gate |
|---|---|---|
| R1 **RESOLVED 2026-06-30 — NOT a blocker; the empirical track is ready in-place.** Earlier "unprovisioned" was a triple probe error (wrong distro: default `wsl`=WSL1, real=`Ubuntu-24.04`/WSL2; wrong data path: real root is the **D-drive** `/mnt/d/chao_workspace/exploring-l4-intelligence/speechrl-data`, not `~/speechrl-data` ext4; and the GGUF was wrongly thought missing). **Verified present:** RTX 5090 + torch 2.9.1+cu128 (cuda available); py3.12 venv/uv/MLflow; **all 5 models** incl. `omni-embed-nemotron-3b`, `qwen3-omni-30b` (vLLM) **and `qwen3-omni-…-gguf` (Q8_0 32 GB + mmproj 2.2 GB — llama.cpp audio path ready)**; **all 28 datasets** (crema-d/minds14/slurp/librispeech/…). | resolved | run via `wsl -d Ubuntu-24.04`, activate the venv, `export SPEECHRL_DATA_DIR=/mnt/d/chao_workspace/exploring-l4-intelligence/speechrl-data`; no download needed |
| R2 **lexical-prior artifact** — emotion "lift" is read-not-listen | high×high | acoustic-grounding control: label-shuffled demos + transcript-only baseline (arXiv:2605.27772, 2510.10444) |
| R3 **optimization artifact** — spurious-reward gains that don't transfer | med×high | random-reward null + cross-model sign-consistency (arXiv:2506.10947) |
| R4 **selection / winner's curse** — demos/prompts/N tuned on test | med×high | selection on disjoint dev; expected-max curve; re-score on held-out (arXiv:2105.11447, 1909.03004) |
| R5 **over-optimization (N\*)** | med×med | cap N at N\*; KL/β trust region (arXiv:2506.19248, 2210.10760) |
| R6 **contamination / leakage** — pretraining saw the benchmark; demo↔test overlap | med×med | demos/test disjoint; date vs cutoff; dedup (arXiv:2406.04244) |
| R7 **small-sample noise** — sampled dev/test, single seed | high×med | power/MDE check; multiple resampled splits + seeds; paired bootstrap CIs (arXiv:2010.06595, P19-1267, 1709.06560) |

- **Controls & ablations:** per family, a negative control (label-shuffled demos) where the effect should not
  appear; ablate each `𝒵_B` axis (task-def / demos / instruction). Report per NeurIPS checklist (arXiv:2003.12206).
- **Ethics, licensing & data governance:** datasets pinned (`docs/datasets.lock.json`; NVIDIA OneWay-Noncommercial
  + Qwen-Research, research/eval only); speaker-ID = biometric voiceprint, SER = affective state — sensitive; no
  redistribution; research-only scope.

## 7. Decision & Outcome **[blocked-pending-provisioning]**

Per-family verdicts (go/pivot/kill) + the consolidated capability-activation map + H1/H2/H3 final status,
appended after the pilots; notable updates mirrored to [[Decision-Log]].

## 8. AI Tools & Verification

| Stage | AI role | Tooling | Verification gate |
|---|---|---|---|
| Survey §3 | synthesize + challenge | survey workflow · `deep-research` | every claim → real arXiv/DOI (verifier-checked); archived in `wiki/survey/` |
| Reproduce §4 | implement + run | coding + code-review; llama.cpp / transformers | independent reproduction from pinned data + `reproduce:` |
| Theory §5(T) | draft proof | Lean (finitary lemmas) | `lake build` sorry-free / cited written proof |
| Validation | 5-role adversarial review | multi-agent | recorded panel sign-off (Statistician · Reproducibility-auditor · Theory-critic · Domain-expert · Reward-hacking red-teamer) |

- **Anti-hallucination:** AI-generated numbers/code accepted only after independent reproduction from pinned data
  + a `reproduce:` one-liner. The Step-2 survey already enforced this (per-lane adversarial source verification).
- **Memory protocol:** durable findings → this Wiki (publish via `scripts/wiki-sync.sh`); mem0 = personal only.

---

## Trajectory log (POMDP path; newest at bottom)

| Step | Date | Belief before → action → observation → update | Rollback? |
|---|---|---|---|
| 0 | 2026-06-26 | `b₀` seeded from W4/W1 archives → **scaffold the living proposal (v0.1)** → (no external obs) → high-VOI open cells = generative-class ICL rows | no |
| 1 | 2026-06-26 | `b₀` → **feasibility probe: WSL env for the generative arm** → **obs: this WSL is UNPROVISIONED — no GPU (RTX 5090 not visible), no CUDA/`nvcc`/`uv`, no venv, `~/speechrl-data/{models,datasets,repos}` empty, no llama.cpp; only py3.14. llama.cpp Qwen3-Omni audio path IS supported (libmtmd).** → **update: binding constraint = _provisioning_, not the audio path. Empirical track BLOCKED-pending-provisioning; analytical track runnable.** | partial — empirical deferred |
| 2 | 2026-06-26 | `b₀` → **5-lane survey workflow + per-lane adversarial verification (`wf_d76b4901-23c`), 80 verified claims / 93 sources archived to `wiki/survey/`** (synthesis agent hit a transient 401; synthesized in-loop) → **obs: (i) mechanism for H1 — inference-time RL needs a stochastic base dist the vector class lacks (2205.11275); (ii) naive demos fix _format_ not accuracy on generative audio LLMs (ALICE 2603.20433), audio LLMs read-not-listen (2605.27772); (iii) speaker resists even on (B) (2603.10827); (iv) activation order content/intent ≥ emotion ≥ speaker (ND11); (v) corrected LEACE id → 2306.03819.** → **update: H1 lever refined to task-def + reward-select (not raw demos); added H2 ordering + speaker boundary; added §6 controls (random-reward, cross-model, acoustic-grounding); §3 filled.** | **partial rollback of H1's "demos activate" framing** |
| 3 | 2026-06-26 | post-survey belief → **pre-register: freeze §1 hypotheses, §2 per-family δ/α + go/kill/pivot + mandatory controls, §5(T) theory, §6 risks → v1.0** → (no external obs) → criteria locked before any pilot (anti-HARKing) | no |

> **Status for the owner (resume here):** v1.0 is **pre-registered and compute-ready**. The only remaining work
> is the **empirical track** (Step-1 feasibility round-trip + Steps 4..N pilots), hard-blocked on an
> R1, which is now **RESOLVED** (2026-06-30): the env is fully ready in WSL2 `Ubuntu-24.04` — 5090 + torch cu128,
> all 5 models (incl. the Qwen3-Omni GGUF+mmproj for llama.cpp) and all 28 datasets are on the D-drive
> `speechrl-data`. **The pilots can run in-place now** (no download). Pre-registration stands; execution is unblocked.
