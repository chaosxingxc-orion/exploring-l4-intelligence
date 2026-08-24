---
title: "Experiment index: speech-aware evidence acquisition"
study_slug: "speech-aware-evidence-acquisition"
study_repo: "https://github.com/chaosxingxc-orion/speech-aware-evidence-acquisition.git"
local_checkout: "studies/speech-aware-evidence-acquisition"
decision_record: "wiki/experiments/speech-aware-evidence-acquisition/2026-08-04-owner-consolidated-execution-contract.md"
experiment_id_namespace: "SAEA-E-<nnn>"
source_candidate_provenance: "R2 (system-first-stage1c-v2; provenance only)"
domain: "speech-only; general/environmental audio excluded"
---

# Experiment index: speech-aware evidence acquisition

This page is the experiment lifecycle control plane for this study. The effective research object is
**speech-aware evidence acquisition** on a frozen speech-capable omni core; audio files are only
carriers of the speech signal, and general-audio data such as FSD50K, AudioSet and ESC-50 must never
enter an experiment in this ledger.

## Current authoritative routing

- **The single self-contained contract currently in force** (the registry pin points at this file):
  [2026-08-04-owner-consolidated-execution-contract.md](2026-08-04-owner-consolidated-execution-contract.md)
- Study-repo boundary adoption (continuation entry 92 guard + continuation entry 93 semantic
  ExecutionPlan gate and contract-field exposure ledger
  + 2026-08-04 E0 closure and four adversarial hardening rounds: runtime-receipt-v2 full build/bin
  binding, D3 freeze machine-enforced including total-order rejection of symbolic links, exposure
  rows verified field by field, first-slice budget enforced against slice totals with a mandatory
  gpu-hours column and finite non-negative budget cells
  + 2026-08-05 R0 engineering baseline and five adversarial rounds driven to zero: a single `core/`
  foundation package (five registry seams, gate binding a unique request path including the D2 exact
  set and a decoding-key allowlist, four-segment driver plan↔config↔receipt binding, non-finite audio
  rejection, rerun fail-closed), split freeze receipt (discovery 44 / dev 10 / confirmatory 115,
  `docs/receipts/splits.json`), model-free entry point demonstrated (gate dry-run exit 0), smoke runbook
  `docs/runbooks/2026-08-05-r0-smoke.md` not executed):
  study commit `b0635aa9736d2cbf3a581fc9295110172672c833` (the previous value `c86f62bb…` is superseded by this line)
- Historical source records (facts are inherited, never written back; blobs are listed in the consolidated contract §9):
  [2026-08-04-owner-stage3-boundary-and-paper-gate-contract.md](2026-08-04-owner-stage3-boundary-and-paper-gate-contract.md),
  [2026-08-04-owner-speech-domain-scope-and-identity-contract.md](2026-08-04-owner-speech-domain-scope-and-identity-contract.md),
  [2026-08-03-owner-go-and-execution-contract.md](2026-08-03-owner-go-and-execution-contract.md)
- Stage-2A entry sequence:
  `docs/superpowers/specs/2026-08-02-speech-aware-evidence-acquisition-stage2a-entry.md`
- Data scope, experiment roles and retention policy:
  [2026-08-04-speech-domain-dataset-scope-and-retention-plan.md](2026-08-04-speech-domain-dataset-scope-and-retention-plan.md)
- Single source of truth for dataset identity/download state: `docs/datasets.lock.json`
- D0 acquisition receipt: `docs/checks/speech-aware-evidence-acquisition/2026-08-02-acquisition/`
- E0 closure + runtime receipt (closed 2026-08-04, verified by gate dry-run): study repo `docs/receipts/`
  (`e0-closure.json`, `runtime.json`; closure event ledger row `SAEA-E0-CLOSURE-2026-08-04`)
- Model/tool exposure: study repo `docs/exposure-ledger.md`
- Published-baseline comparison table (R0.1 survey product; the ours rows are filled in after each probe):
  [published-baselines.md](published-baselines.md)
- Stage-1C historical evidence: `wiki/archive/working/stage1c-portfolio/2026-08-03-archive-digest.md`

## Registration requirements

Every formal experiment must resolve to: `experiment_id`, study commit, shared-code revision, config hash,
protocol hash, model revision, dataset revision, **split role (discovery|confirmatory|dev),
split identity hash, consumed flag**, MLflow run, artifact location, artifact hashes,
result summary, deviations and decision. Large bytes live under `SPEECHRL_DATA_DIR` or MLflow; the Wiki
registers only URIs, versions and hashes. A confirmatory sample is marked `consumed=yes` in this ledger as
soon as it is read (2026-08-03 program visibility discipline; consolidated contract §7); the exposure event
is recorded at the same time in the study repo `docs/exposure-ledger.md`, and inherited exposure is
monotonically non-decreasing.

Every record must also declare:

- the speech task and carrier;
- which of `OBS / ORG / SUPPLY / USE` actually changed in this run;
- the runtime visible-field and forbidden-field checks;
- results in all three classes: effectiveness, reasonableness and efficiency;
- confirmation that no general-audio data was loaded.

## Ledger

| experiment_id | date | speech task/carrier | changed axes | study commit | shared code revision | config hash | protocol hash | model rev | dataset rev | split role | split identity hash | consumed | MLflow run | artifact location | artifact hashes | effectiveness | reasonableness | efficiency | deviations | decision |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| SAEA-E-001 | 2026-08-09 | long-form earnings ASR / earnings22-original dev subset10 (10 calls) | OBS only (obs-agent-loop segmentation); ORG/SUPPLY absent by design in the bare-core arm; USE traced | `1602f55a091ded6c3c764d70491c1b8f4263b781` | none (study repo only) | `56f5a0d42a7b558c…` | `aae46aee1b3e24db…` | **qwen3-omni-30b-a3b-instruct-gguf-q4km** (INT4 local requant, umbrella lock 2026-08-09; runtime receipt `runtime-q4km.json` sha256 `7be32a78…`), llama.cpp `fdbd6abee20e408de21e90ca77a24cd50a6ea073` | earnings22-original (umbrella lock), frozen dev subset10 | dev | `89b178d6b1ef46d9…` | no | `9bb81ee87a8a4ffdbc00663971fec937` | `$SPEECHRL_DATA_DIR/runs/SAEA-E-001-r0-smoke/attempt-20260809T061349Z-3f3d36` | outputs=`40b384ef…`; raw_trace=`708b10c7…`; trace_manifest=`5f6ff8bb…`; scores=`35c40467…`; session_receipt=`bd5b5cc1…` | **mean WER 0.2674** over 10 calls (per-call 0.2157–0.3252) — a REFERENCE FLOOR for the bare-core arm, no superiority claim. Substantive finding: the retired whole-call protocol produced 2–106-word transcripts for 40–75-min calls, the obs-agent-loop produces 7,556–11,036 words against 9,128–11,827-word references | bare-core arm; gold never in runtime; D3-frozen scoring stack; trace shows OBS 813 / MODEL_REQUEST 805 / MODEL_RESPONSE 805 / COST 795 / USE 10 with ORG+SUPPLY correctly absent; all six wiring-integrity checks PASS (`docs/readiness/2026-08-08-e001-wiring-memo.md`) | actual 795 calls / 47,393 audio-s / 2.53 gpu-h against a registered 2000 / 150,000 / 30.0; 2.7 h wall at `obs_batch_samples=4` | protocol switched from whole-call to obs-agent-loop (owner directive; whole-call record retained as boundary evidence); executor = openJiuwen 0.1.16.post2 after a byte-equivalence + determinism gate; model switched Q8_0 → INT4 (4.17× faster; Q4-vs-Q8 agreement 1.50% WER, entity names identical); all switches annotated in the exposure row before results were read | R0 exit criterion (measurement integrity) MET; this floor is the baseline the SAEA-E-002 R4 context-dose arms move against |

One formal experiment is registered (SAEA-E-001, completed 2026-08-09). E0 D1–D4 and the runtime receipt
were closed on 2026-08-04 and verified by gate dry-run (study repo `docs/receipts/`); the R0 engineering
baseline was delivered on 2026-08-05 with five adversarial self-check rounds driven to zero (study
`b0635aa`), and the first formal experiment was to be the smoke `SAEA-E-001` (runbook prepared, not yet
executed). Every model contact must still carry a valid `ExecutionPlan` and be pre-registered in the study
repo exposure ledger first, enforced fail-closed by `contracts.FrozenCoreGate`.

## Second-arc probe verdicts (routing tier + embedder path, consumed 2026-08-19 – 2026-08-20)

The study also runs a lighter `bounded-discovery-probe` track with its own `SAEA-PROBE-<name>-<n>`
exposure rows (study repo `docs/exposure-ledger.md`), evidenced in `docs/readiness/` and consolidated
in the study's living `docs/readiness/2026-08-19-scheme-scoreboard.md`. These are not `SAEA-E-<nnn>`
formal ledger rows.

- **P-FEW** — `INCONCLUSIVE-FEW` (consumed 2026-08-19, study `docs/readiness/2026-08-19-pfew-verdict.md`).
  Few-shot demo supply on the closed-set SLURP decode router: BAL−NONE = **+0.0000**, 90% CI
  **[−0.0667, +0.0667]** (n=60 SLURP devel; the point sits inside the ±0.05 equivalence band but the
  CI overhangs it, so neither FS-HELPS nor a certified FS-INERT fires). Skew-label capture is **0/59
  incremental** (predicted-label marginal unmoved 3→3→3 across arms); a small, CI-separated ICL-noise
  cost (NONE−SKEW +0.0667) is real but is not label-prior capture. Closed-set decode routing itself
  reproduces `{exact: 60}` mapping under three prompt constructions (2/2 confirmations), gold agreement
  measured at **0.78–0.82 across two sessions** (cross-session reproduction noise ±2 samples on n=60).
- **P-EMB-1** — `EMB-WEAK` (consumed 2026-08-19, study `docs/readiness/2026-08-19-pemb1-verdict.md`).
  Bare mean-pooled cosine matching on the frozen core, SLURP 18-way: **3/60 = 0.0500**, below uniform
  chance (0.0556); two-attractor collapse (`general`+`play` = 91.7% of predictions); permutation test
  P=0.8774 (observed agreement fully explained by the prediction marginal, not content).
- **P-EMB-2** — `EMB-CLOSED` (consumed 2026-08-19, study `docs/readiness/2026-08-19-pemb2-verdict.md`).
  Same construction on Audio2Tool tool selection (152 registry rows), scored on the 183 tool-wrong ids
  the V4 supply account cannot otherwise reach: **2/183 = 0.0109** top-1, top-5 **below** chance,
  **400/400 winning cosines negative**. The 183 stay closed; the informational 217-id degradation figure
  carries no clause. P-EMB-1/2 together put bare generation-core mean-pooled embedding routing at 0/2,
  both clean rather than marginal.
- **Owner correction (2026-08-19, `833b6c9`) + adjudication (2026-08-20,
  `docs/readiness/2026-08-20-embedder-charter-adjudication.md`)**: the P-EMB-1/2 refutation is **scoped
  to generation-core pooled embeddings only**, not to embedding routing as a family. Dedicated embedding
  models — including ones derived from generative thinkers, e.g. LCO-Embedding-Omni — enter under the
  charter's frozen tool-level retriever clause; binding condition: the integration must **structurally
  forbid generation** (`encode()`-only, fail-closed machine check, never convention), final answer
  authority stays with the frozen core. The owner also approved the **P-EMB-3M** multi-model
  routing-comparison design named in the adjudication text (local dedicated embedders — LCO-3B primary,
  GLAP, CLSP, omni-embed-nemotron control — plus a CASCADE arm: core self-transcription → local text
  embedder (qwen3-embedding class) → text-text label matching), gated on an **E-1 feasibility/identity
  report that has not yet been produced**. Caution for this refresh: the study's 2026-08-20 selection
  ticket (`docs/readiness/2026-08-20-omni-embedding-selection.md`) surveys LCO-Embedding-Omni-3B as a
  `sentence-transformers`/safetensors model for a new isolated venv, not a GGUF served on the pinned
  llama.cpp core, and never names GLAP or CLSP among its candidates (LCO-3B, jina-v5-omni, SONAR,
  omni-embed-nemotron-3b, LCO-7B, Tevatron OmniEmbed, BidirLM, CLAP — rejected); no LCO-Embedding-Omni
  GGUF-servability check exists anywhere in the study's records as of this refresh. Only
  `qwen3-embedding-0.6b-gguf` (the CASCADE arm's text embedder, see acquisitions below) has a recorded
  llama.cpp servability sanity check.
- **P-EMB-3L** — registered (study `docs/readiness/2026-08-20-pemb3l-preregistration-REGISTERED.md`,
  commit `18da9a9`; exposure row `SAEA-PROBE-pemb3l-234`). Question: does any training-free
  construction on the LOCAL core form a usable SLURP routing space. **Superseded: flown and
  consumed 2026-08-20 with verdict `LOCAL-EXHAUSTED` — see the third-arc section below.**
- **Stage-2B qualification freeze candidate** — study commit `bb995d5` (2026-08-19,
  `docs/readiness/2026-08-18-stage2b-candidate-qualification-DRAFT.md`): speech-term program complete,
  regression term measured (36/97 regressions vs a 0/97 re-fly baseline), acoustic-mediation risk
  demonstrated (P-TRAP, a USE-side risk), refusal claim inverted per V1. **Awaiting owner freeze
  approval** — not yet an owner decision.

### Third arc: embedder closure and the speech-native AgentLoop line (2026-08-20 → 2026-08-23)

- **P-EMB-3L** — `LOCAL-EXHAUSTED` (consumed 2026-08-20, study
  `docs/readiness/2026-08-20-pemb3l-verdict.md`): all three local constructions 3/60 = 0.0500;
  the local branch is closed. A build defect was found and later reproduced on a second model:
  `--pooling` is inert on this llama.cpp build's audio side, so LCO audio verdicts are
  stack-scoped, never model-level.
- **P-EMB-3M** — `EMB-WEAK-SCOPED (M1) + CASCADE-ROUTES (M4)` (consumed 2026-08-20, study
  `docs/readiness/2026-08-20-pemb3m-verdict.md`): LCO-3B audio 3/60 = 0.0500 (pooling-override
  scoped); GLAP control 0.1333; CASCADE — core self-transcript → qwen3-embedding-0.6b text↔text
  — **45/60 = 0.7500** (text-mediated, not speech-native); CLSP dropped on a runtime error.
- **P-CORR-F** — `CORRECTIVE-PERCEPT + DOSE-INSUFFICIENT` (consumed 2026-08-20, study
  `docs/readiness/2026-08-20-pcorrf-verdict.md`): percept-keyed train-mined type-corrective
  supply Δ₁ = **+0.0508**, 90% CI [+0.0098, +0.0968]; the percept gate is near-binary (96.7%
  self vs 0.0% cross capture); supply-side FILTERING becomes the open duty (85.7% wrong-entry
  admission). Disclosure: byte-identical resends diverged 6/20 at temperature 0, `-np 4`.
- **P-EMB-4R** — `REGISTER-RESCUE(a-glap) + KNN-BEATS-LABEL-MATCH` (consumed 2026-08-21, study
  `docs/readiness/2026-08-21-pemb4r-verdict.md`): register-aligned utterance↔utterance kNN
  rescues a weak GLAP audio signal (0.3167, recall@5 0.5667); LCO arms stay weak/scoped; T-QW
  text kNN 0.8667 is a text-mediated diagnostic only; C-DECODE canceled by owner pre-read with
  zero contacts. Successor named: decoder-joint speech-feature × text-key matching.
- **Speech-native AgentLoop / training-free-RL line (M5→M11, 2026-08-21→23; study
  `docs/readiness/2026-08-21-speech-native-agent-loop-training-free-rl-plan.md`)**: the
  decoder-joint successor executed at scale on train-only discovery splits. Strongest result
  (EFFECT-C108, read 2026-08-22): embedded **K1-M1 90/108 vs direct K0-M0 77/108** (net +13;
  key-text shuffle collapses to 0/108; speech-swap 75/108), mmproj-free, every contact carrying
  the original speech packet. Five external controller generations (M5-v2, M6, M7, M8, M9)
  were all rejected against preregistered bars on this near-ceiling surface; the GPU 95/90
  serving gate remained unmet after 7+ engineering cells (mean occupancy 94–96% throughout).
  The task-independent knowledge contracts (`KnowledgeSnapshot`/`QueryState` BUILD/USE
  separation), the shared speech-native agent runner, and the openJiuwen executor
  (`openjiuwen-workflow-v1`) landed model-free through study commit `8f51e95d`.
- **2026-08-23 owner rulings — knowledge-plane baseline program** (study
  `docs/readiness/2026-08-23-knowledge-plane-baseline-rulings.md`, commit `418ec684`): Q-K-V
  organization (speech-primary Q; multi-dimensional K with a ranking layer; un-embedded
  prior-bearing V); construction-on-TRAIN / use-on-DEV / report-on-TEST separation with a DEV
  100/500/1000 optimization ladder; train tiers renamed T108/T500; **E108 GPU gate decoupled
  from scientific admission** (95/90 retained as the engineering-baseline acceptance
  criterion); Audio2Tool admitted as the second surface; scoreboard v5; the 2026-08-19 design
  queue superseded (P-CORR-R / P-TARGET-P1 / P-STRIP-AUG parked, never registered); 29-item
  cross-modal retrieval survey landed
  (`docs/readiness/2026-08-23-cross-modal-retrieval-survey.md`).

### Fourth arc: the DEV-100 iterative campaign (2026-08-24, complete and frozen)

- **DEV ladder governance landed** (study `2d07139b`): FINAL60 reserved-unread + nested
  DEV-100/500/1000 identity receipts (devel side, probe-60 excluded at utterance
  granularity); train-scale KB-BUILD v1 (`70897f8e`, 11.5k-utterance distribution-modeled
  snapshot, 100% label coverage, decontaminated); the first cross-task policy registered in
  all four knowledge registries (`bbdb9902`, two-contact α-blend form).
- **DEV-100 campaign** (`SAEA-DEV100-KB-ALPHA-BLEND-CAMPAIGN`, 6 rounds, frozen 2026-08-24,
  study `docs/readiness/2026-08-24-dev100-campaign-verdict.md`): **BLEND 72/100 vs direct
  48/100 (+24), C→W 0 at the frozen α-.45 cell, exact replication Δ=0**. Ladder
  63→63→65→67→72→72; knob science: τ inert, rank weights mathematically inert, α live only
  after the label-identity binding repair (f1060078; damage 11→5→0; retain-primary 0→67).
  Reviewer elevation: paired 90% CI [+11,+27] (0/10k replicates ≤0), conservative
  variance-channel floor +15 [+6,+24], McNemar p 5.5e-4, train-prior rule control 39-41;
  literature-consistent, upper-middle envelope (closest: kNN-Prompt; HyDE-pedigree retrieval
  keys). Frozen knobs: study `configs/policy/kb-policy-v1-dev100.json`.
- **Serving/engineering legacy**: the sustained-decode pathology was isolated BUILD-BOUND to
  the 2026-08-23 zero-copy custom llama.cpp build (quarantined; base featcache binary
  healthy at identical ~24.1 GiB peaks — the zero-copy build's serving measurements carry a
  pathology annotation); two-leg resident hosting (systemd user unit + Windows keepalive;
  WSL VM powers off ~14 s after the last client detaches); decode-rate sentinel + canary +
  clock/VRAM sampling preflight suite; run-cumulative ExecutionPlan semantics; prompt-cache
  reuse measured 0.83-0.88 (near structural ceiling). Nine byte-identical canary
  confirmations establish single-slot decode determinism across restarts, VM/Windows
  reboots, and binaries; the 8-slot direct-decode byte-variance channel (±2 samples) is the
  characterized residual noise term.
- **DEV-500 CONFIRMATORY (same day, complete)**: four arms flown mechanically clean (2,506
  core contacts, zero rail incidents), then the preregistered one-touch read — **unexposed-400
  M0 52.50% → frozen BLEND 72.25% (+19.75 pp), 90% CI [+16.5, +23.0] excludes zero, McNemar
  p 7.2e-22, W→C 81 / C→W 2 — CLAIM CONDITION MET**. Bracketing ablations attribute the gain
  to the retrieval SIGNAL: vs random-retrieval +15.75 pp; random-exemplar ICL is NEGATIVE
  (−5.5 vs M0). Dispatched-subgroup surgical profile: 62.31% vs 2.31% (W→C 78 / C→W 0).
  BLEND operates AT the k=5 retrieval-reachability ceiling (71.5%; k=32 → 84.25% — the next
  tier's quantified headroom). Verdict: study
  `docs/readiness/2026-08-24-dev500-confirmatory-verdict.md`. **Gates open: DEV-1000
  (baseline-lock tier; optional k-widening mini-campaign on DEV-100/500 first) and
  Audio2Tool (generality surface).** The training-free RL space stays open above the frozen
  cell (the retain/dispatch channel: 33% dispatch rate, +78/0 flips).

### Related umbrella acquisitions (2026-08-18 to 2026-08-20)

- `diar-sortformer-4spk-v2` (umbrella `docs/datasets.lock.json`, commit `6ca5f50`,
  meeting-minutes-tools profile) — owner-locked primary diarization tool for the
  `papers/meeting-minutes-agent` topic.
- `qwen3-embedding-0.6b-gguf` (umbrella `docs/datasets.lock.json`, commit `0d4865b`,
  speech-aware-tools profile) — Q8_0 single-file GGUF, dim 1024, the local text embedder for the SAEA
  P-EMB-3M CASCADE arm; sanity-served once on the pinned llama.cpp-featcache llama-server (`--embedding
  --pooling last`) against one synthetic string only, zero corpus contact; first contact on any study
  corpus stays gated behind its own exposure-ledger row.

### Meeting line (papers/meeting-minutes-agent — no dedicated wiki ledger exists yet; noted here per
### the study-adjacent routing convention pending `wiki/experiments/papers/meeting-minutes-agent/`)

- G1 floors campaign scored (2026-08-19, `papers/meeting-minutes-agent`
  `docs/readiness/2026-08-19-g1-floors-verdict.md`, commit `6a9485e`; descriptive one-shot read, no
  branch verdict computed): pooled over 18 dev-18 meetings, **Z-turn cpWER 0.6099** vs **Z-oracle
  cpWER 0.6061** (deployment-gap CI **[-0.0124,+0.0193]** includes zero — the diarization tool costs
  ~nothing on cpWER; the primary confusion-cost gap alone is CI-separated from zero at −0.0090).
  Removing turn metadata from the prompt (arm Z-free) costs **+0.2627 cpWER** on identical audio, CI
  excludes zero, roughly three quarters of it speaker assignment. QA macro F1 **0.0725 (Z-turn) /
  0.0970 (Z-oracle)**. SAER-M was `NOT SCOREABLE` on this campaign's replies (id-join failure);
  repaired to definition **v1.1** the same day (`3d5e2e1`, content-based bullet-to-gold alignment) —
  re-score against this campaign not yet flown.
- PRECOMP wave-1 **18/18** meetings complete (`4631f68`); wave-2 **75/76 PARTIAL** (`b26b9be`,
  2026-08-20): `ES2005d` refused fail-closed on a float-epsilon transport-slice overrun (1.1e-13 s
  over a strict 120.0 s bound); the fix is sequenced for the coordinator, deliberately not applied
  mid-wave (would cold-start the slice cache). Feature cache `ami-q4km` grew to **52,071 entries**
  (+28.92 GiB).
