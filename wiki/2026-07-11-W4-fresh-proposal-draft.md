---
title: "W4 Fresh Research Proposal (DRAFT) — frozen omni speech representation: selectivity & irreducible ceiling"
date: 2026-07-11
stage: 1-problem-definition → 2-solution-validation (proposal draft)
status: "DRAFT — owner sign-off required; NOT preregistered until signed"
template: Research-Proposal-Template.md
responds-to:
  - 2026-07-10-stage1-adversarial-research-audit.md (§7.1, Phase 3)
  - 2026-07-11-stage1-audit-response-and-rulings.md (G0: W4 = independent line, no shared headline)
ticket: "#29"
---

# W4 Fresh Proposal (DRAFT) — how selective can a *frozen* omni speech representation be made, and where is its ceiling?

> ⚠️ **DRAFT — owner sign-off required. This is NOT preregistered until the owner signs §0.**
> Nothing here is a frozen criterion yet; every threshold below is a *proposed* value awaiting sign-off.
> Per the G0 ruling (2026-07-11), **W4 is an independent flagship line — it does NOT share a headline
> with W1** and does not inherit any Stage-1 freeze as a Stage-2 prereg.

## 0. Front-matter

```
> project: speech-mllm-omni-embedding-rl (W4)  ·  study: frozen-readout-selectivity-ceiling  ·  owner: <sign here>  ·  date: 2026-07-11
> status: planned (DRAFT — unsigned)  ·  version: v0.1-draft
> companion docs: [[Project-Thesis]] · [[W4-Research-Plan]] · [[W4-Training-Free-RL-Feasibility]] ·
>   [[Decision-Log]] · [[Per-Work-Status]] · claim_ledger.yaml (C-W4-EMO-GROUPED, C-W4-PARA-RESTATED)
```

Sign-off checklist (all must be initialled before status → `planned(preregistered)`): primary question ·
H1–H4 · L0–L4 promotion criteria · SESOI/MCID per factor · split table + acquisition items · multiplicity
plan · kill criteria · Information-Boundary-Guard clause.

## 1. Research idea & primary question

**Primary question (verbatim, audit §7.1):**

> **How far can weight-frozen, task-conditioned readout make an omni speech representation selective for
> content, speaker, emotion, and intent — and where does the frozen representation impose an irreducible
> ceiling?**

This is stronger than "we already disentangle it" because **both positive and negative results are
publishable**: we expect content strong, emotion partial, speaker weak-but-non-zero, instruction-steering
null — a *map* of the frozen representation's readable surface and its ceiling, not a single win.

No weights and no structure change: the only levers are (i) which layer/frames, (ii) which weight-free
pooling, (iii) a task-name/template *instruction* prepended to the audio (never an eval-derived one).

### Preregistered hypotheses (proposed; updated with what we NOW know)

Fresh verified evidence that constrains the priors (umbrella `docs/claim_ledger.yaml`, Stage-1 directional):
- **C-W4-EMO-GROUPED** (`_repro/emotion_pool_grouped_v1.json`, commit `d04bb89`): speaker-grouped
  `GroupKFold(5)` over the full CREMA-D corpus (7442 clips / 91 speakers). Weight-free attentive
  mean+std pooling (`audio_attn`) vs weight-free masked-mean (`audio`): pooled Δ **+0.0270**, cluster
  (=speaker) bootstrap 95% CI **[+0.0141, +0.0401]** (excludes 0) — **but bounded below the pre-declared
  SESOI of 0.05** (TOST-style "practically equivalent to no effect"). 2/5 folds individually significant,
  3 span 0; single fold-seed; content-correlated features partially present at the emotion-selected layer
  (content-ID acc ≈0.42–0.48 at L16, logged per fold).
- **C-W4-PARA-RESTATED** (`_repro/speaker_probe_restatement.json`, commit `d04bb89`): the frozen pooled
  embedding is **NOT speaker-free** — speaker readout ≈0.033 vs chance 0.011 (~3× chance, 91-way), with
  2/3 seeds' stored bootstrap CIs excluding chance from below (the conservative n=3 across-seed t-CI
  [0.0034, 0.0633] spans chance, directional-only). Phrasings "no speaker information / never written /
  measured-zero" are **retired**.

| # | Hypothesis (proposed, falsifiable) | What the new evidence changed |
|---|---|---|
| **H1** | In the *final pooled* embedding, content readout ≫ emotion > speaker, when **content is re-measured open-vocab (WER), not as CREMA-D's 12-way sentence-ID**. | Ordering holds directionally (content near-ceiling on the closed 12-sentence set; emotion ~0.54 grouped; speaker ~3× chance). But CREMA-D content is a **closed 12-sentence ID** → near-1.0 is substrate-inflated; H1 now *requires* an open-vocab content substrate before the ordering is claimed. |
| **H2** | Layer/pooling/trajectory readout gives a **statistically reliable but sub-MCID** emotion gain, and recovers fine-grained speaker only **below any deployable EER**, though non-zero. | Tightened by C-W4-EMO-GROUPED: the pooling lever's emotion gain is reliable **yet bounded below SESOI 0.05** → the lever alone does not clear the MCID. And by C-W4-PARA-RESTATED: speaker is **low-but-non-zero**, so "cannot recover speaker" is restated as "recovers it too weakly to deploy," not "speaker-free." |
| **H3** | Instruction-only conditioning produces **no** cross-dataset / cross-backbone *target selectivity* (expected NULL). | Held as a directional prior from the first result: `diagonal_dominant=False`, instruction rows flat (C-W4-DISENTANGLE invalid, downgraded L0/L1). We predict this null replicates under grouped, powered evaluation. |
| **H4** | Multi-specialized keys (H-a) beat a single omni space (H-b) on **paralinguistic** tasks (emotion/speaker), while H-b stays competitive on **content/intent**. | H-b already shown competitive on **intent**: MInDS-14 en-US frozen bi-encoder selection reached Acc@1 **0.984**, +0.126 [0.077,0.181] over the raw-schema arm (`_repro/minds14_toolintent_paired.json`). The H-a advantage on paralinguistic remains untested. |

**Pre-committed thresholds (proposed):** per-factor MCID in §5; α = 0.05 two-sided; selectivity CIs are
cluster-bootstrap, Holm-corrected within factor family.

## 2. Claim ladder (L0–L4) — the study's spine

Selectivity is graded on the audit's ladder (audit R1-P0). A claim may only use the language of a tier it
has cleared; **"disentanglement" language is forbidden below L3; "deployable activation" below L4.**

| Tier | Claim licensed | **Promotion criterion (proposed, preregistered)** | Current evidence |
|---|---|---|---|
| **L0** factor decodability | some probe reads the label from some layer | any probe > chance on a held set | **CLEARED** — content (12-ID), emotion, speaker (3× chance) all decodable |
| **L1** accessible readout | low-complexity probe **stable on group-held-out** | kNN/linear probe CI excludes chance under **speaker-grouped nested CV**, ≥2 folds | **emotion CLEARED** (C-W4-EMO-GROUPED, grouped CV, 0.54–0.57 stable); speaker at L0 only (weak); content pending open-vocab |
| **L2** task selectivity | matched conditioning beats **all** mismatched | **paired cluster-bootstrap CI on `matched − max(mismatched)` selectivity excludes 0**, ≥2 datasets | **NOT cleared** (`diagonal_dominant=False`) |
| **L3** disentanglement | target ↑, nuisance not ↑, counterfactual holds | **target-sufficiency ↑ AND nuisance-leakage not-↑ (MDL/probe) AND counterfactual-invariance pass**, all three, ≥2 datasets/backbones | **untested** |
| **L4** deployable activation | label-free per-instance selector, stable gain | label-free selector realizes calibrated positive fraction on a **locked** test surface, no eval-gold | **untested** |

**Success / kill / pivot (pre-registered, §7.1 spine):**
- **Go (per factor):** clear L2 selectivity (CI on `matched − max(mismatched)` excludes 0 and exceeds MCID)
  on ≥2 datasets; for a disentanglement claim, clear L3 on ≥2 datasets/backbones.
- **Kill (verbatim, audit Phase 3.2 W4-kill):** *"若 target selectivity 的 powered CI 在至少两个 dataset
  或两个 backbone 上都不超过预注册 MCID，则放弃 'task-conditioned disentanglement'，转投 'limits/
  suppression' 论文；这仍是成功收官，不继续换 prompt 直到显著。"* — i.e. if the powered target-selectivity
  CI fails to exceed the pre-registered MCID on ≥2 datasets **or** ≥2 backbones, **abandon the
  disentanglement claim and pivot to a limits/suppression paper — counted as a successful conclusion**; do
  NOT keep swapping prompts until something is significant.
- **Pivot zone:** L1 cleared but L2 mixed (one dataset up, one flat) → report as a **selectivity-ceiling
  map**, still a valid paper, no disentanglement wording.

## 3. Survey & positioning

**Value + challenge.** Frozen-representation *probing* is a mature methodology; the value here is applying
it as a **controlled selectivity ladder on a modern omni LLM's speech states** and honestly bounding the
ceiling. The strongest challenge (which we adopt): *probe-can-read ≠ representation-is-selective*
— high probe accuracy can reflect probe capacity or shortcut features, not the representation. We answer it
with control tasks, MDL, and counterfactual intervention (below), and by refusing L2/L3 language until the
selectivity/nuisance/counterfactual triad passes.

**Foundational probing controls we MUST cite (missing from prior W4 chain — audit §2.3):**
- Locatello et al. 2019, *Challenging Common Assumptions in Unsupervised Disentanglement*, arXiv:1811.12359
  (unsupervised disentanglement is non-identifiable without inductive bias/supervision).
- Hewitt & Liang 2019, *Designing and Interpreting Probes with Control Tasks*, arXiv:1909.03368
  (**selectivity = task-acc − control-task-acc**; a probe that also fits random labels proves nothing).
- Voita & Titov 2020, *Information-Theoretic Probing with MDL*, arXiv:2003.12298 (report **description
  length / compression**, not just accuracy).
- Speech-specific: ContentVec (2204.09224), CCSRD (2023.findings-emnlp.394), *Large-Scale Probing of
  Speaker-Specific Attributes* (2501.05310), *Disentangling Textual & Acoustic Features* (2410.03037).
- Backbone/encoder cards: Omni-Embed-Nemotron (2510.03458 — **note: task-trained bi-encoder, non-commercial;
  case-study substrate, not "raw omni pretraining"**), Qwen2.5-Omni (2503.20215).
- Stats/repro: reusable-holdout (1506.02629), Dror et al. *Hitchhiker's Guide* (P18-1128), Demšar 2006.

**Baselines named.** model · method · data: (a) raw final-pooled omni state · weight-free mean-pool ·
CREMA-D; (b) specialized frozen encoders (WavLM/ContentVec speaker/content, Emotion2Vec emotion,
ERes2NetV2 speaker) as the *readable-ceiling* reference; (c) small trained probe / LoRA as an explicit
**out-of-scope upper bound**.

**Novelty delta (one sentence).** Closest prior is generic speech-probing work (e.g. 2501.05310); this
study is the first to run the **L0→L4 selectivity ladder with matched-vs-mismatched task-conditioning,
nuisance-leakage, and counterfactual controls on a *frozen omni LLM's* states**, with a preregistered
pivot-to-limits kill — not a claim of achieved disentanglement.

## 4. Design

**Proven machinery.** Reuse `scripts/pool_method_probe_grouped.py` verbatim as the backbone (it already
implements: full-corpus pool = union(train.csv,test.csv) verified disjoint; `GroupKFold(5)` over actor ID
with asserted no speaker leakage; **inner speaker-grouped layer selection on train speakers only**; paired
per-clip rows; **cluster(=speaker) bootstrap** CIs; pre-declared SESOI + TOST verdict; atomic provenance
write with git SHA/dirty, model+config hash, per-fold speaker/clip manifests + sha256). Extend it with the
control-matrix arms and the nuisance/counterfactual probes below; keep the atomic-provenance discipline.

**Control matrix (audit Phase 3.1 — every factor compared against all eight):**
1. final pooled **raw** (no instruction);
2. **random / format-matched** instruction (negative control — must NOT produce selectivity);
3. **target** instruction vs **mismatched** instructions (the L2 selectivity test);
4. **layer × pooling** grid: {early, mid, late} × {mean, mean+std, attentive, trajectory};
5. **random-projection + PCA/whitening** control (matched dimensionality, no learned readout);
6. **specialized frozen encoders**: ContentVec / WavLM (content, speaker), Emotion2Vec (emotion),
   ERes2NetV2 (speaker) — the readable-ceiling reference;
7. **small trained probe / LoRA** upper bound — explicitly labelled out-of-scope (it updates weights);
8. **no-audio / audio-blind** control (instruction-only; must collapse to chance).

**Disentanglement evidence per conditioned view (audit 3.2 — all four required for L3):**
- *target sufficiency*: target-task metric ↑;
- *nuisance leakage*: linear + MLP + kNN + **MDL** probe of every OTHER factor — must NOT rise;
- *selectivity*: paired cluster-bootstrap CI on `target_gain − max(off_target_gain)`;
- *counterfactual invariance*: same sentence / swap speaker or emotion; same speaker / swap sentence or
  emotion (CREMA-D's crossed (speaker×sentence×emotion) design makes this feasible);
- *cross-group/OOD*: unseen speaker / session / language;
- *geometry* (CKA / subspace angle): **descriptive only — never substitutes for the causal test.**

**Datasets & splits (audit split table; ✅ on disk / ⚠️ needs acquisition).**

| Factor | Dev / calibration | Locked test | External replication |
|---|---|---|---|
| **emotion** | ✅ **CREMA-D** speaker-grouped nested CV (frozen manifest; the proven substrate) | ⚠️ **IEMOCAP** LOSO or held-actor fold — **NOT in `datasets.lock.json`; acquire (USC license request; not auto-fetchable)** | ✅ **MELD** (frozen manifest — natural, external) · optional ⚠️ ESD/CSEmotions (gap-candidate, verify on-disk) |
| **content/ASR** | ✅ **LibriSpeech** dev (frozen) — **open-vocab WER, replacing CREMA-D 12-ID** | ✅ LibriSpeech test-clean/other + noise strata (frozen) | ✅ FLEURS-R / ⚠️ AISHELL (candidate) or a 2nd backbone |
| **speaker** | ⚠️ **VoxCeleb1** enrollment/test — only `voxceleb1-test-split` (gap-candidate, ~1.4 GB) is on disk; **full enroll/test EER protocol needs the full set → verify/acquire** | EER / **minDCF** protocol (not 91-way kNN) | ✅ **CN-Celeb1** (candidate, byte-verified 2026-07-09) · CREMA-D speaker diagnostic |
| **intent** | ✅ **MInDS-14** / ✅ **SLURP** official dev (frozen; W4 already ran MInDS-14) | official test, speaker/template group check | ✅ **Speech-MASSIVE** (2nd language/corpus) |

**Backbones (critical — audit R1-P1).** Primary = `omni-embed-nemotron-3b`, but it is a **task-trained
bi-encoder**, so it is a case study, not proof of "omni LLMs generally have these factors." **Add ≥1 RAW
omni hidden-state backbone** (Qwen3-Omni-30B GGUF hidden states / Qwen2.5-Omni-Thinker) and, for the L3/L5
generalization claim, a **second lineage**. No cross-backbone claim without ≥2 lineages.

**Metrics (per factor, not just accuracy).** emotion: accuracy + **UAR** + macro-F1; speaker: **EER +
minDCF** + retrieval R@k (audit: stop reporting 91-way kNN as the speaker headline); content: **WER** on
open vocab; intent: Acc@1 + F1. Cross-cutting: **MDL / compression** (Voita–Titov) and **selectivity =
task-acc − control-task-acc** (Hewitt–Liang control tasks) for every readout.

**Repro manifest (required, template §4).** Every artifact carries: `datasets.lock.json` revision + any
acquired-set fingerprint; code git SHA + dirty flag; model id + config sha256; venv/torch/CUDA versions
+ RTX 5090 / WSL2-Ubuntu-24.04; fixed seeds (`FOLD_SEED=20260711`, `BOOTSTRAP_SEED=42`); a single
`reproduce:` line; MLflow run id. Committed summary **atomically written by the same script** (no hand
transcription — the grouped probe already enforces this).

## 5. SESOI, power, multiplicity, theory gate

- **SESOI / MCID (proposed, per factor — freeze on sign-off):** emotion **0.05** absolute accuracy
  (already pre-declared and used in C-W4-EMO-GROUPED — note the current pooling gain +0.027 is *reliable
  but sub-SESOI*, which is exactly why the pooling lever alone is not enough and instruction-conditioning
  must be tested); speaker **EER MCID ≈ 2 pts absolute** (or minDCF equiv.); content **WER MCID ≈ 1 pt**;
  intent **Acc@1 MCID ≈ 0.03**. The selectivity CI must exceed the MCID, not merely exclude 0.
- **Power sketch.** Inference is cluster-bootstrap with **speaker as the cluster** → power is governed by
  the **number of speaker clusters**, not clip count. CREMA-D 91 speakers gives usable width (observed
  half-widths ≈ ±0.013). **Flag: IEMOCAP LOSO has ~10 actors → very few clusters → wide CIs**; treat
  IEMOCAP as a directional replication, not a powered confirmation, and pre-register that limitation.
- **Multiplicity.** **Holm within each factor family** (all emotion arms Holm-corrected together, etc.);
  layer×pooling grid selection via the **inner grouped nested CV** (never on held-out speakers); across
  datasets use **hierarchical / random-effects** aggregation, not pooled Bernoulli; seeds are a random
  effect, never independent n. Winner-selection error is handled by nested CV + external replication, not
  by the bootstrap CI (which only quantifies sampling error — audit R2-P0).
- **(T) Theory gate (template §5T).** This is a **one-shot finite selector / readout**, not an iterative
  optimizer → the required object is a **well-posedness note + the relevant bound**, NOT a convergence
  proof (template §5T; forcing convergence where it is undefined is wrong). Finitary lemma candidate for
  Lean: **finite-argmax well-posedness** of the layer/pooling selector + a **no-regression / monotonicity**
  bound of grouped-CV selection over the arm set. Assumptions to mark "verify empirically": factor presence,
  linear-accessibility, and that task-conditioning is steerable at all (H3 predicts it is not).

## 6. Risks, threats to validity, boundary & ethics

| Risk | L×I | Resolving gate |
|---|---|---|
| probe capacity mistaken for selectivity (Goodhart) | H×H | Hewitt–Liang control tasks + MDL; L2/L3 language gated on the triad |
| speaker/content shortcut leakage across split | H×H | **speaker-grouped nested CV** (already enforced in machinery); counterfactual swaps |
| reusable-holdout decay from repeated test looks | M×H | locked test opened **once**, after all arms fixed; script-locked manifest |
| single specialized backbone over-extrapolated | H×M | ≥1 raw omni + 2nd lineage before any cross-backbone claim |
| content ceiling inflation (12-sentence ID) | H×M | H1 re-measured on **open-vocab WER**, not CREMA-D sentence-ID |
| eval-derived conditioning (info-boundary breach) | H×H | Information-Boundary-Guard clause below |

**Information-Boundary-Guard (applied).** The conditioning instruction may contain only the **generic task
name / template** (e.g. "identify the emotion"), **never** the test item's gold label, transcript, or
answer, and never a statistic derived from the eval set. Layer / pooling / instruction are selected on the
**dev / inner grouped split only**; the locked test is touched **once**. The MInDS-14 tool-intent arms use
**task-schema candidate cards (task-level, item-gold-free)** — permissible; but each new arm must pass an
explicit read-out-vs-new-info check: does this lever add information the deployment lacks? If yes, it is a
headroom/oracle arm and is labelled as such, never as a deployable result. **No eval-derived conditioning.**

**Ethics / licensing / data governance.** CREMA-D (research), MELD (declare-lab), MInDS-14/SLURP/
Speech-MASSIVE (open) per manifest; **omni-embed-nemotron-3b is research/non-commercial** (case-study only);
IEMOCAP requires a USC license request (gate acquisition on it); VoxCeleb/CN-Celeb underlying CC BY-SA.
**Sensitive attributes: this study reads speaker identity (biometric/voiceprint) and affect/emotion** — a
per-clip nuisance-leakage report is itself a privacy surface; keep artifacts internal, no re-identification
use. Dual-use: selectivity readouts could enable speaker profiling — intended-use scope is measurement of a
frozen representation's limits, not building a deployable identifier.

## 7. Explicit NOT-claims

- **No "disentanglement" wording below L3** — until target-↑ + nuisance-not-↑ + counterfactual all pass on
  ≥2 datasets/backbones, the object is "factor availability / accessible readout / selective-readout
  limits," not disentanglement.
- **No "deployable activation" / "training-free RL improves deployment" claims below L4** — no label-free
  per-instance selector has been shown; oracle/dev-selected numbers are labelled headroom, never gains.
- **No extrapolation from CREMA-D's 12-sentence-ID content to open-vocab content activation.**
- **No "speaker-free / no speaker information / measured-zero" language** (retired by C-W4-PARA-RESTATED);
  speaker is **low-but-non-zero (~3× chance)**, framed as "below a deployable EER," with both a superiority
  and an equivalence (TOST) statement.
- **No cross-backbone generality claim from a single task-trained bi-encoder.**
- **No "system convergence proved in Lean"** — only the finite-selector well-posedness/no-regression lemma,
  if formalized, may be cited.

## 8. AI tooling & verification hooks

- **Survey §3:** every cited claim resolves to a real arXiv/DOI (the five foundational probing refs above
  are the minimum add over the prior W4 chain); AI-suggested citations verified before use.
- **Reproduce §4:** independent third-party re-run from a **clean checkout** (not the author's warm
  session) landing in the tolerance band; code-review log against the claim checklist (ground-truth-derived
  score, no leakage, seed/env pinned, `reproduce:` runs clean).
- **Theory §5T:** finite-argmax well-posedness / no-regression lemma → Lean, `#print axioms` whitelist in CI.
- **Adversarial panel:** Statistician · Reproducibility auditor · Theory critic · Speech-probing domain
  expert · **Anti-gaming red-teamer** — recorded sign-off before any locked-test open.
- **On-accept hooks:** append [[Decision-Log]], update [[Per-Work-Status]] + claim_ledger, publish via
  `scripts/wiki-sync.sh`. **Memory: shared record = Wiki; personal notes never substitute.**

---

### Acquisition / open-item checklist before sign-off
1. **IEMOCAP** — not in `datasets.lock.json`; USC license request + fetch (blocks emotion locked test).
2. **VoxCeleb1 full enroll/test** — only `voxceleb1-test-split` (gap-candidate) confirmed; verify/acquire
   the full enrollment protocol set for EER/minDCF.
3. Verify on-disk status of gap-candidates **ESD / CSEmotions / CN-Celeb1** (memory says candidate campaign
   byte-verified 2026-07-09, but they are NOT in the frozen lock — confirm before prereg).
4. Stand up a **raw omni hidden-state backbone** (Qwen3-Omni-30B GGUF / Qwen2.5-Omni) — required for any
   claim beyond a single bi-encoder case study.
5. Freeze per-factor MCIDs (§5) and the multiplicity plan; then flip status to `planned(preregistered)`.
