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

- **Current frontier, 2026-09-17:** Fable 5.1 took over coordination from Codex by local files
  (study `docs/superpowers/plans/experiment-handoff/OWNER-FABLE-TAKEOVER-2026-09-16.md`, receipt
  `docs/handoff/2026-09-16-fable51/TAKEOVER-FABLE51-20260917T010325Z.md`, coordination generation 169).
  Owner decisions of 2026-09-16: acceptance bar SLU-F1 >= 64 and intent >= 78 replicated on the same
  roster; the four-row candidate-bound slot-view proof declined for now; the TRAIN A direct score of
  `SAEA-SLURP-DIRECT-MAX512-TRAIN-FOLD-A-SOURCE-RECOVERY-V1` released as the direct anchor; a
  Reviewer-off ablation flies first. The program is the study spec
  `docs/superpowers/specs/2026-09-16-slurp-v2-base-program-design.md` (Phase A offline audits and
  engineering in worktrees, then one-factor Phase B admission cells on TRAIN A 1,080, combination,
  same-roster replication and DEV1000 confirmation, then the v2 lock before any Stage 3 work). The
  Codex-era handoff v4 package remains the historical record of the 2026-09-09 to 2026-09-16 recovery.
  Cells B0 and B0r (review loop off) flew 2026-09-17: nil effect, HARMFUL under the measured TRAIN A
  own null (study `docs/results/2026-09-17-slurp-b0-review-off-redecision-v2.md`); the loop is
  retained as a NEUTRAL module with a SLURP default plan, projection v3 is the fixed post-processing
  of every official number (owner decisions 6-10 of 2026-09-17), and cells B1/B2/B4 re-register on
  the anchor; GPU order B1 -> B2 -> B4b -> B4a -> B4c (conditional), one cell in flight.
  Results of 2026-09-17 (study `docs/results/`): **B4b (slot store v2) ADMITTED**, official SLU +2.55 pp
  CI95 [+1.13, +3.98], provisional until a same-roster replicate; **B1 (twenty speech-keyed TRAIN
  exemplars supplied to the Solver) SLU 48.53 -> 61.14, +12.61 pp CI95 [+10.54, +14.60]**, intent 80.19,
  projection v3 62.67, symmetric 62.97, all 18 scenarios gaining, +27.25 over direct, **ADMITTED after the
  derangement-twin read of 2026-09-18** (B1 minus twin +7.83 pp CI95 [+5.85, +9.75]; the twin alone +4.77
  over the anchor with nil intent, so the speech key carries 62 % of the SLU gain and nearly all of the
  intent gain; study `docs/results/2026-09-18-slurp-b1-twin-verdict.md`; harness-admission entry M1,
  provisional until the combination pair replicates); its first attempt aborted on a Solver-revisit
  phase-supply refusal fixed by E3c. Owner directive 11: one unified Node Context Policy before every agent node (audit
  `docs/results/2026-09-17-slurp-node-context-audit-v1.md`, design
  `docs/superpowers/specs/2026-09-17-node-context-policy-design.md`, E8a/E8b/E8c merged; B7a's first arm aborted on an illegal Planner action, its
  recovery smoke passed, arm held; B7r/B7c/B7b registered). Owner decisions 12-17 fixed the order B1 twin
  -> B2 v3 -> B7a -> B4b replicate -> B4a -> B7r -> B7c -> B7b -> B5 -> B5r -> B6; owner decisions 18-21
  (2026-09-18) make it bar-first: B4b replicate (flying) -> B5e (M1 + M4b, the early combination) -> B5er
  -> lock "SLURP base v2.0" -> B6 DEV1000 -> B2 v3, B7a, B4a, B4c, B7r, B7c, B7b as v2.1 admissions;
  the bar is never lowered on a B5e miss (B5b reads first). Both recovery smokes (B2 v3 on the E2d fix,
  B7a on the E8c fix) passed structurally on 2026-09-18. Owner decisions 22-24 (2026-09-18): every
  registered cell must support checkpoint resume (item E10: trace replay of the aborted attempt, kept rows
  without selection, merged manifest with a declared predecessor; the B4b replicate, aborted at 577/1,080
  rows when the inherited server died, is its first use); the program bar and every final evaluation read
  the OFFICIAL unprojected SLURP evaluate.py number, projection v3 beside as a diagnostic, and gains are
  never assumed additive (B1 61.14 + B4b 2.55 = 63.69 official if additive, so B5e is expected to miss by
  a few tenths and route through decision 20); the serving wrapper, its monitor and every campaign run as
  Windows Scheduled Tasks with the battery and idle conditions disabled, AC sleep off. B5e's smoke passed;
  its first arm attempt aborted at 25 contacts on a coordinator-caused task stop and re-flies as its one
  recovery.
- **Current frontier, 2026-09-09:** owner-directed recovery after Fable5.1 exhausted its allowance.
  Codex recovered the completed Wave 9 integration, KU-S3 exact-arithmetic norm cache and Audio2Tool
  preprocessing fixes into the study's local `master`. The existing results ledger is the
  study-side index of decided and pending cells:
  `studies/speech-aware-evidence-acquisition/docs/results/stage2-results-ledger.md` (JSON twin beside it).
  The working plan and preserved-worktree inventory are
  `studies/speech-aware-evidence-acquisition/docs/superpowers/plans/experiment-handoff/RECOVERY-PLAN.md`.
  These links supersede the older arc's next-action summaries below as current operational routing.
- **Execution is not a verdict:** all seven SLURP KV cells have finalized attempts and successful
  whole-manifest score batches on study commit `2afb4b5c`; their scientific read/decision and ledger
  closure remain pending. Source:
  `studies/speech-aware-evidence-acquisition/docs/checks/speech-aware-evidence-acquisition/2026-09-09-owner-recovery/runtime-snapshot.json`.
  Reconcile missing predecessor-decision evidence and the declared null/estimator binding before
  interpreting the results; preserve the flown protocol and sealed bytes. No automatic re-flight.
- **Current module boundaries:** KC-E1f scientific replication is MET, with its separate default-plan
  switch-form proof still UNMET. SLURP tail and the original whole-answer logprob primary are NOT
  ADMITTED. LP-2 is a prepared successor, not an admitted replacement. KU-S4 exemplar arms still need
  packet promotion; the unfinished worktree is preserved. The owner order remains Decisions 13-14 in
  [2026-09-07-owner-go-stage2-cells-and-foundation-fixes.md](2026-09-07-owner-go-stage2-cells-and-foundation-fixes.md).
  This recovery changes coordination and engineering integration, not scientific execution scope.
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
`b0635aa`), and the smoke `SAEA-E-001` was executed on 2026-08-09 against the frozen dev subset10 and is
registered in the ledger above (the previous clause "the first formal experiment was to be the smoke
`SAEA-E-001` (runbook prepared, not yet executed)", written 2026-08-05 at `047cf39` and true until the run
landed at `7f9725a`, is superseded by this line). Every model contact must still carry a valid
`ExecutionPlan` and be pre-registered in the study repo exposure ledger first, enforced fail-closed by
`contracts.FrozenCoreGate`.

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

### Fifth arc: the DEV-1000 baseline lock and the Audio2Tool second carrier (2026-08-25)

- **BASELINE LOCKED — DEV-1000 one-touch read** (study `docs/readiness/2026-08-25-baseline-lock-verdict.md`,
  lock commit `d9fef537`; row `SAEA-SN-MF-DEV1000-LOCK-READ`, campaign row
  `SAEA-DEV1000-BASELINE-LOCK` consumed=yes; artifacts
  `docs/checks/speech-aware-evidence-acquisition/2026-08-25-dev1000-lock-read/`). Primary
  statistic on the **500 UNEXPOSED** samples (DEV-1000 minus DEV-500): M0 278/500 = 55.60% →
  BLEND 379/500 = 75.80%, **+101 samples = +20.20 pp, 90% CI [+17.20,+23.40]** (0 of 10,000
  replicates ≤ 0), 95% CI [+16.60,+24.00], McNemar exact **p = 1.04e-25**, W→C 106 / C→W 5.
  **Lock condition (90% CI lower bound ≥ +10 pp) MET with +7.20 pp of margin.** Scale-stable:
  DEV-500 unexposed-400 +19.75 [+16.50,+23.00] σ̂ 2.0563 vs DEV-1000 unexposed-500 +20.20
  [+17.20,+23.40] σ̂ 1.8986 — each point estimate lies inside the other's interval. Mechanism
  unchanged across tiers: the dead-direct dispatch subgroup carries the gain (3.13% → 62.50%,
  +59.38 pp on 160 samples), the retain subgroup is safe (+2.37 pp), 17 of 18 scenarios
  non-negative (play +26, recommendation +23, qa +12; weather −1).
- **The δ retain-override is FALSIFIED out of sample and REMOVED.** The v2 candidate's δ ≥ 0.14
  retain-override held on every exposed population but out of sample failed: of 14 fires, the 3
  in the unexposed half recovered **0** and damaged **3** (net −3 samples, −0.60 pp), while the
  11 in the previously-exposed half recovered 11/11. **The locked baseline is therefore the v1
  frozen cell `configs/policy/kb-policy-v1-dev100.json`** (sha256 `d68afd2c…a919`), not v2;
  without the override the unexposed-500 margin is +20.80 pp (382/500). The δ signal is recorded
  as fit-not-validated, not discarded as a direction.
- **What the lock pins**: α 0.45, τ 0.65, recall top-k 5, fusion m 5 / c 2 / top_l 3, rrf
  0.5/0.3/0.2, TRAIN priors, pair-boundary stage off, facet-side percept admission, the f1060078
  label-identity repair — over the KB-BUILD v1 full TRAIN snapshot
  (`docs/receipts/knowledge/slurp-kb-size-full.json`), served by the BASE `llama.cpp-featcache`
  binary at the np8 profile, executed through the openJiuwen AgentLoop (`openjiuwen-workflow-v1`)
  in the two-contact knowledge-conditioned form. Scope: **authorizes** the Audio2Tool generality
  campaign against the locked form, training-free RL over a fixed environment, and DEV-tier
  engineering optimization; **does NOT authorize** test contact, superiority or generalization
  claims, or Stage-3 activity. FINAL60 stays reserved-unread.
- **RANKER SCALE DEFECT FOUND AND REPAIRED** (study `docs/readiness/2026-08-25-a2t-admission-scale-sweep.md`,
  audit landed `21926b5f`, repair commit `1341c2db`; row `SAEA-SN-MF-A2T-ADMISSION-SCALE-SWEEP`
  registered at `e9656577` before any computation; receipt
  `docs/checks/speech-aware-evidence-acquisition/2026-08-25-a2t-admission-scale-sweep/sweep-report.json`
  sha256 `88f606fe…a74d66`; **0 contacts of any kind**). The ranker
  `saea-rank-wcos-prior-agree-v1` summed an **unbounded** prior-mass dimension with a cosine
  **bounded by 1** inside one weighted sum. Commensurability invariant
  `sup(prior) < w_cos·τ / w_prior = 1.08333`: SLURP's sup is **1.0000** (inside, margin +0.0833,
  a probability by construction), Audio2Tool's is **4.1000** (a 3.78× violation). Consequence on
  A2T: prior-mass facets filled the whole top-m=5 window and **0 content facets were admitted on
  all 104 trajectories**; on SLURP, 0 of 500 trajectories were affected. The landed repair
  (`_dimension_scales`, variant A6-DIMSUP-FLOOR1) divides each ranker dimension by
  `max(1.0, sup over the recalled set)`.
- **The repair is IDENTITY-PRESERVING on the locked SLURP cell, proved by measurement, not
  asserted.** All 15 candidate variants replayed over the sealed DEV-1000 NEW500 flight through
  the identical code path: **admitted set differs on 0/500, supply differs on 0/500, dispatch
  differs on 0/500.** Regression obligations run against the landed fix: SLURP flight-replay
  decisions **497/500** (the 3 being explained v2 override fires), SLURP flown supply reproduced
  **163/163**, the SLURP `V0-FROZEN` gate still PASSes, SLURP dispatch 160; on A2T the
  `V0-FROZEN` gate now FAILS by design, dispatch goes **0 → 15** matching the 15 label-free ids
  exactly, 104/104 trajectories admit a content facet, supplied-value distribution 2:35 3:28 4:36
  5:5, gold-bearing supply 68. FIX-2 (fail-closed invariant assertion) and FIX-3 (the upstream
  `prior_score` repair) remain open and block nothing.
- **CORRECTION — the A2T zero-dispatch was an IMPLEMENTATION DEFECT, not a finding** (study
  `docs/checks/speech-aware-evidence-acquisition/2026-08-25-a2t-g1/README.md`, CORRECTION section,
  commit `401418cd`, after the owner ruling). The BLEND attempt-3 "paired first signal" measured a
  broken configuration; its −1.92 pp delta is the documented multi-slot decode-variance channel and
  **no paradigm-level conclusion about Audio2Tool follows from it**. The earlier coordinator wording
  framing it as "the paradigm's boundary precisely located" is withdrawn. What stands unaffected:
  the mechanics (the derived serving geometry, prompt-fit margin +12,331, packet promotion, KB
  vectors), the two-pass co-residency design, the VRAM-oversubscription diagnosis, the replay
  machinery, the M0 arm's own numbers, and every spend and rail record.
- **A2T G1 BLEND attempt 4 — the post-repair flight: THE SUPPLY PATH FIRES** (study
  `docs/checks/speech-aware-evidence-acquisition/2026-08-25-a2t-g1/g1-read-attempt4.json` sha256
  `cb5e5658…d086f89`, landed `26307ee9`; registered under row `SAEA-A2T-G1` at `3e12e8c4`
  **before any contact**; launcher `6bbd6e62`; attempt `attempt-20260825T144405Z-a2tg1blend`;
  mechanical report `arm2-blend-mechanical-report-attempt4.json` sha256 `641c4b5e…459436`).
  Population **A2T-G1-104, EXPOSED**, split identity hash `516f92d9…`; the policy cell is
  byte-identical to the locked SLURP cell and the rails pin moved to the repair commit
  `1341c2db` as a takeoff gate; serving geometry is the §8.1-derived `-c 65536 -np 2`
  (32,768 tokens/slot, margin +12,183); composed config hash `df6bf4d4…38f9`.
  **Mechanics: 104/104 trajectories, 15 of 104 dispatched and 15 real evidence contacts flown
  where the defective ranker dispatched 0**; dispatch lands exactly on the 15 dead-direct
  (label-free) trajectories, decision replay holds 104/104, branch-only replay holds 15/15, and a
  content facet enters the admission window on 104/104 (τ 0.65, best content cosine 0.759–0.957).
  **Paired signal vs the landed M0 on the same 104: tool accuracy 0.5962 (62/104) → 0.6058
  (63/104) = +0.96 pp, CI90 [−2.88,+4.81], McNemar p 1.0, W→C 3 / C→W 2 — the interval does NOT
  separate from zero. Exact match is not merely flat but IDENTICAL to the sample, 0.2788 (29/104)
  in both arms, CI90 [−1.92,+1.92].** Empty-call rate collapses 0.1346 (14) → 0.0288 (3) and
  unparsed answers 4 → 0; mean slot F1 0.3766 → 0.3738. **Attribution: all three tool-accuracy
  wrong→correct flips are on trajectories that dispatched AND whose direct text was byte-identical
  to M0, so only the evidence contact can account for them**; one C→W is decode-variance (divergent,
  never dispatched) and one is reported AMBIGUOUS and not counted for the method.
  Spend: 18 core contacts (2 canary + 15 evidence + 1 resend; Pass A replayed at 0 contacts against
  attempt 3's hashed messages documents, 104/104 matched), 58.247 metered audio s, 0 embedding tool
  contacts, 0.004626 GPU active hours; campaign cumulative 321/400 core contacts.
- **The bound on that reading, carried verbatim in substance.** The report's own hard stop: *"G1
  authorizes MECHANICS AND FIRST SIGNAL ONLY. No generality claim, no superiority claim, no test
  contact, no knob change and no Stage-3 activity follows from this report."* The plan's smuggling
  guard is applied to the result itself — a tool-accuracy gain that leaves exact match flat is a
  DIFFERENT claim and must not be smuggled, and the empty-call collapse is a different metric that
  must not be substituted for the primary one. Stated limitations, inherited whole: the tier is
  EXPOSED so every number is a secondary reading; n=104 is below the plan's own n ≥ 400 power floor
  so the intervals are descriptive, not confirmatory; the `a2t-gold-v1` scorer's semantics are
  interpretation, not ground truth; the corpus and its speaker assignments are synthetic; and no
  ablation arm flew, so nothing here attributes the effect to retrieval as opposed to the second
  contact (ABL-RANDRET answers that at G2). Two reporting artifacts are disclosed rather than left
  to be found: the imported `bootstrap_gain` hard-codes a "over the 100 DEV-100 ids" resampling
  label while the actual universe is the 104 A2T-G1-104 ids, and the A0 comparator was read on the
  parent 400-item split, so it is an anchor and not a paired comparison.
- **Open decision and standing debt.** The G1 report recommends **not** opening G2 as scoped and
  taking cheaper decisions to the owner first; the unexposed Audio2Tool tier (n ≥ 400) and
  training-free RL over the now-live dispatch channel both remain open. Operational debt carried
  from G1: the SLURP np8 service was stopped for the A2T np2 flight and **remains DOWN — a later
  mission must respawn it before any SLURP arm flies.**

### Sixth arc: the limit located by measurement, and the matured synthesis (2026-08-25, after the G1 flight)

- **ONE CONSOLIDATING RECORD, AND ITS VERIFICATION IS PART OF THE PRODUCT** (study
  `docs/readiness/2026-08-25-stage2a-matured-synthesis.md`, landed `3f131afd`; row
  `SAEA-SN-MF-STAGE2A-MATURED-SYNTHESIS` registered **before** any verification ran; receipt
  `docs/checks/speech-aware-evidence-acquisition/2026-08-25-stage2a-synthesis/verification-report.json`;
  verifier `src/speech_aware_evidence_acquisition/analysis/stage2a_synthesis_verification.py`).
  Seven registered model-free diagnostic rungs landed after the A2T G1 attempt-4 flight —
  cross-carrier ceiling decomposition (`54ed885c`, precision pass `2bf4ccb7`), A2T gold-absence
  diagnosis (`aaa366ad`, correction `36ad85c2`), matching-vs-extraction (`d4c75c7a`), query-key
  degeneracy cross-carrier (`27129962`), extraction conditioned on dispatch (`6c6ec719`),
  field-level supply accounting (`27b2be09`) and the A2T oracle query bound (`5020adce`, correction
  `274ce62a`) — each registered in the study exposure ledger before any computation. The synthesis is
  the document written to be read, in its own words, "instead of the nine" readiness documents of the
  day. **351 checks passed / 0 failed** — 332 receipt-field claims, 6 reductions over per-sample
  lists, 2 live-artifact digests and 11 source-line assertions — across **12 SHA-256-verified
  receipts**, fail-closed (any mismatch raises and no report is written); the offline guard was armed
  before the first input was opened and recorded **0 outbound connection attempts against 0 targets**.
  Seven quantities are declared unverified and omitted rather than carried, and five disagreements
  between the landed documents are stated with the receipt that settles each. Spend across the arc:
  **0 frozen-core / 0 embedding-tool / 0 tokenizer contacts, 0 HTTP or socket requests, 0 audio
  seconds, 0.0 GPU hours, 0 gold labels newly opened**; no knob changed, nothing written under
  `configs/`, `rails/` or `core/`; `consumed` stays **no**.
- **The locked SLURP cell is UNCHANGED.** DEV-1000 unexposed-500 **+20.20 pp, 90% CI
  [+17.20,+23.40]** stands exactly as landed at `d9fef537`. Every unexposed-500 statistic in this arc
  is a **SECONDARY reading on the locked baseline's own population**: descriptive, and it revises,
  re-tunes and re-opens nothing.
- **NEW — WHERE SUPPLY IS ACTUALLY DELIVERED, THE GAIN OPERATES ON THE EXTRACTION AXIS TOO, AND THE
  DELIVERY RATE TRAVELS WITH EVERY NUMBER.** Only a DISPATCHED trajectory receives evidence; a
  RETAINED one stops at contact 0 and is handed nothing (the two sets are proved equal, not assumed).
  Delivery: **SLURP DEV-1000-NEW500 163 of 500 = 32.60%**, Audio2Tool **15 of 104 = 14.42%**.
  **Nothing in this bullet is a population effect.** On the delivered SLURP stratum (n = 163):
  matching `scenario_action_exact` 7 → 100 = **+57.0552 pp**, CI90 [+50.3067,+63.8037]; extraction
  macro `slot_f1_exact_mean` **+9.4391 pts**, CI90 [+4.3558,+14.5194]; official micro `slu_f1`
  **+13.7570 pts**, CI90 [+8.8840,+18.6695] — both extraction intervals exclude zero. **The
  matching-free cell still moves**: both arms matching-WRONG *and* supply delivered, n = **59**, macro
  **+6.7797 pts** CI90 [+1.6949,+11.8644] and official **+15.2312 pts** CI90 [+8.2127,+22.9778], both
  excluding zero — no matching movement can explain either. Three-way decomposition of the
  +3.5438-point aggregate: matching-attributable **+2.5438** (n = 111), supply-attributable
  **+0.9333** (n = 62), unsupplied residue +0.0667 (n = 327) — the matching term still dominates at
  71.78% and that finding is untouched; what is new is that 93.33% of the remaining point is
  supply-attributable. The retained stratum (n = 337, no evidence delivered) moves **+0.6924** macro
  points with a CI90 that does **not** exclude zero. Cells conditioned on the arms' matching outcome
  **and** on the dispatch decision are conditioned on post-treatment variables twice over, so they
  carry collider bias and are **mechanism readings, never effect sizes** — a rule fixed in each row's
  ledger entry before any n was known. (Study
  `docs/readiness/2026-08-25-extraction-conditioned-on-dispatch.md`, receipt
  `.../2026-08-25-extraction-conditioned-on-dispatch/read-report.json` sha256 `7662fbc3…6a337525`;
  delivery rates `.../2026-08-25-field-level-supply-accounting/accounting-report.json` sha256
  `ca973be8…0766de4c6`.)
- **THE STRONGEST CAUTION, AND IT MUST TRAVEL WITH THE EXTRACTION CLAIM: THE EXPOSED HALF DOES NOT
  REPLICATE THE SLURP SUPPLY TERM.** Same carrier, same policy cell, same flight — the
  supply-attributable term is **+0.9333 pts on the unexposed 500 (n = 62)** against **−0.0533 pts on
  the prior-exposed nested DEV-500 (n = 57)**, and the exposed matching-free cell (n = 55) reads
  **−0.4848** macro points with a CI90 that does not exclude zero. **Until that is explained, the
  extraction result is one population's result.**
- **THE LIMITING FACTOR IS NOW LOCATED BY MEASUREMENT — four candidate explanations each REFUSED with
  a number, rather than argued away.** (R1) **KB build coverage — 0 of 11**: of the 11 gold-absent
  dispatched A2T trajectories, 0 are a BUILD defect and 11 are a RANKING defect, and over all 104
  trajectories 0 have a gold tool with no KB value and 0 have one with no vectored facet — a
  build-coverage lever has nothing to fix on this population. (R2) **Retrieval width and depth — no
  admissible depth reaches gold**: under the locked `top_l` = 3, **0 of 11** gold values enter the
  supply at any depth in the 12,601-vector KB; lifting `top_l` entirely reaches 2 of 11; reachability
  rises from 0 at k = 5 to 1.000 at k = 512 and none of that rise converts into an admitted supply —
  with K-WIDEN K1's standing prior (supply changed on 32 of 100 trajectories, **0 width-attributable
  flips**) making the refusal decisive rather than merely arithmetical. (R3) **The τ percept gate — a
  runtime-legal query clears τ on 15/15 and supplies gold on 0/15**: the oracle rung's N1 query uses
  no gold at all (the L2-normalized mean of the vectored content facets of the trajectory's own tier,
  determined by the sample id alone) and lifts the gold-facet cosine from the landed below-τ band
  0.565332–0.635625 to 0.7209 / 0.7898 / 0.8587 — yet it supplies gold to none, binding at the recall
  window every time, because the lift raises **148–150 τ-passing targets simultaneously** and the gold
  target lands at rank **11–99** among them. **τ is a threshold on similarity, and similarity is not
  the scarce resource — DISCRIMINATION is**; any argument from "the gold cosine is only 0.0144–0.0847
  below the bar" to "a small improvement converts" is refuted, at zero cost, on this carrier. (R4) **A
  hand-fit dispatch override — 11/11 in sample, 0/3 with 3 damaged out of sample**: the δ ≥ 0.14
  retain-override recovered 11 of 11 on the prior-exposed half and recovered 0 while damaging 3 on the
  unexposed half (realized −0.60 pp); its registered zero-loss-by-construction property reads `false`
  in the receipt. **In-sample perfection is not evidence, and every future dispatch-widening proposal
  inherits this prior and must be gated out of sample.**
- **What remains after the four refusals: DISCRIMINATION UNDER A DEGENERATE RETRIEVAL QUERY — and it
  is carrier-scoped, measured rather than assumed.** The 15 A2T dead-direct trajectories carry **5
  distinct query vectors = 0.3333 per trajectory**, **11 of the 15 share ONE key** (73.33% of the
  group) and that whole cluster carries **one** distinct supply between them, against **0.9438**
  distinct keys per trajectory on the 89 label-recovered. The cause is the α veto and it is arithmetic, not an empirical
  regularity: at α = 0.45 a recovered direct label beats every rival by a guaranteed `1 − 2α` =
  **+0.10** margin and the worst margin actually observed **attains** that structural floor
  (0.10000000000000003), so `retain == direct-label-recovered` is structural, evidence can only ever
  reach the label-free set, and **93.33%** of that set's A2T contact-0 answers are structurally empty —
  the α veto selects exactly the trajectories whose answer is empty, and **the answer IS the query**.
  The pathology does **not** transfer: dead-over-live degeneracy ratio **0.353** on Audio2Tool against
  **1.240** (unexposed) and **1.027** (exposed) on SLURP, whose dead-direct answers are structurally
  empty at 1.25% / 1.81%, whose τ refuses the gold facet on only 10 and 14 of those trajectories, and
  whose dead-direct median gold-facet position is **1** against Audio2Tool's **83** — SLURP's keys
  repeat because short labels **collide**, benignly, and the collision happens *more* in its healthy
  label-recovered group.
- **The oracle bound: the KB itself can deliver — and it NAMES NO LEGAL FIX.** The pre-registered O3
  oracle (every vectored content facet targeting the gold tool, each withheld from the retrievable
  pool in turn) supplies gold to **11 of the 11** gold-absent trajectories, against decision bands
  fixed in the registration before any number was seen (≤ 1 refutes, ≥ 8 survives) — registered
  outcome **SURVIVES**; **twin-free 11 of 11**; and in the typical case a *randomly chosen* same-tool
  sibling query delivers **1,596 / 1,871 = 85.30%**. Under the oracle no stage binds: τ, `k`, `m`, `c`
  and `top_l` are all sufficient once the query is right, so **the cell is not the ceiling, the query
  is**. But every oracle query is built from the trajectory's own gold tool identity — information no
  runtime query could legally have — so **it bounds from above and proposes nothing**; whether any
  legal contact-0 construction can produce a tool-identifying query is explicitly declared unverified
  and would need a model contact. Decontamination was **measured, not asserted** (the rung's first
  version asserted it from the builder's source and its own successor commit `274ce62a` corrected
  that): 0 of 104 evaluation units are in the KB, **6 of 104** evaluation utterance *texts* appear
  verbatim as a KB content facet, and **0** of those six are among the 15 dispatched trajectories the
  bound measures.
- **Audio2Tool remains MECHANICS ONLY — the population verdict is unchanged.** Tool accuracy 62 → 63
  of 104 = **+0.9615 pp**, CI90 [−2.8846,+4.8077], **41.56% of replicates at or below zero**, McNemar
  mid-p 0.6875; exact match **29 → 29 = 0.0000 pp**, CI90 [−1.9231,+1.9231] — and the tool-accuracy
  line must never be reported without the exact-match line beside it. Where supply is delivered (15 of
  104 = 14.42%) the dispatched slot micro-F1 is **+12.1212 pts but its CI90 [0.0000,+23.0769] touches
  zero at n = 15**, so it is carried as **NOT established**; the retained 89 read −3.0250 pts
  [−6.1940,−0.5941], and the population aggregate slot micro-F1 falls 0.437870 → 0.412088. The two
  carriers' magnitudes are accounted for arithmetically, and nothing is left over for "the method is
  weaker on Audio2Tool" as a separate hypothesis: reachable share 14.42% vs 32.00% (**2.2187×**) times
  within-reach conversion +13.3333 pp vs +59.3750 pp (**4.4531×**), both decompositions closing
  exactly against their observed population deltas. The channels are separated: **form repair alone
  converts 1 of the 11 that changed form; gold-bearing supply converts 2 of 4** (n = 4 is a mechanism
  reading and nothing extrapolates it), and the empty-call collapse 14/104 → 3/104 is the FORM channel
  working and **must never be substituted for an accuracy claim**. K3 stays **REFUSED** on Audio2Tool
  — its own carve-out preserves 1 of the 15, and projected dispatch falls 15/104 → 3/104 on the arm
  that measures actual form repair — and unprojected on SLURP.
- **THE EPISTEMIC RECORD — four claims made and WITHDRAWN in one day, each refuted by a measurement,
  each caught by a gate fixed before the number was seen** (the synthesis carries the table). (1)
  *"The A2T zero-dispatch is a paradigm boundary"* — refuted: it was a ranker commensurability defect,
  `sup(prior_score)` 4.1 against a required bound of 1.08333, with 0 content facets reaching the
  top-`m` window on 104/104 trajectories; caught because G1 published its mechanism invariants as
  FALSIFIED rather than quietly passing them, which forced an implementation audit instead of a
  conclusion about the paradigm. (2) *"KB coverage is the lever"* — refuted at 0 BUILD / 11 RANKING;
  caught because the BUILD/RANKING partition and its 104/104 fidelity gate were pre-registered, so a
  negative could not be re-partitioned after the numbers were seen. (3) *"SLURP's prior code was
  correct"* — refuted against source rather than restated from landed prose: **both** builders divide
  one globally accumulated counter by another, differently keyed, with no restriction of the numerator
  to the denominator's key, and SLURP's ratio is a probability only because
  `intent = f"{scenario}_{action}"` nests intent inside scenario in the **label vocabulary** — the
  local name `intent_total_in_scenario` asserts a restriction the expression never performs, so the
  SLURP builder carries the identical latent defect and would break under a non-nesting label scheme.
  Caught by the synthesis's own rule of re-checking every claim against its source. (4) *"The supply
  does not serve extraction"* — refuted: the landed conditioned read was measured where **no supply
  had been delivered** (its cell held 3 dispatched of 273 on SLURP unexposed, 2 of 255 on the exposed
  half and **0 of 60** on Audio2Tool); caught by a successor row that reproduced the landed
  arithmetic to the digit before challenging its interpretation, leaving the matching-dominance
  finding untouched. **These four rows are evidence that the gating discipline works, and they belong
  in this ledger as much as the numbers do.**
- **What this arc does NOT authorize, carried at its source strength.** No generality claim, no
  superiority claim, no cross-carrier transfer claim, and no conclusion about capability beyond the
  two already-read populations — "the locked cell generalizes" is neither established nor implied
  here. No knob change: α, τ, `k`, `m`, `c`, `top_l`, `top_k` and the rank weights were read and
  reported, never written. No flight, re-flight or G2 opening; no revision of the lock; **no new
  agenda item** — the obvious reading of the degeneracy finding is a design observation, and any
  key-construction item needs its own registration, its own two-sided falsifier, its own
  dispatch-preservation clause and an owner decision. **No test contact: FINAL60 stays
  reserved-unread.** No Stage-3 activity of any kind.
- **Open owner decisions the synthesis frames and explicitly does not make.** **D1 — the α trade**:
  widening dispatch buys reach (with no α gate, 68 of 104 A2T trajectories would carry gold-bearing
  supply, but 64 of those sit in the retained set, where 60 of the 89 retained are already correct
  under BLEND), against two costs — the adverse out-of-sample prior of the δ override above, and the
  fact that a per-carrier α **breaks the byte-identical transfer claim**, itself a scientific asset.
  **D2 — whether to open a new Audio2Tool contact cell at all**: the mechanism caps the population
  effect near **+1.9231 pp** (reach × within-reach conversion), so a whole-population design is the
  wrong thing to power against, and the cheapest thing that would make any A2T number interpretable is
  a repeated-decode replication at fixed config. **D3 — a hash-manifested release freeze** of the
  locked baseline (policy config, KB snapshot, `rails/kb_policy.py` at `1341c2db`, serving profile)
  into a single artifact. **D4 — the umbrella `required_truth` token list and the stale endpoint-token
  fields**, which is an owner call the study repository does not touch: umbrella
  `docs/superpowers/specs/2026-08-25-research-objective-required-truth-reconciliation-decision-request.md`
  is OPEN and unresolved. Standing operational debt from G1 is unchanged: the SLURP np8 service
  remains DOWN and a later mission must respawn it before any SLURP arm flies.

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
