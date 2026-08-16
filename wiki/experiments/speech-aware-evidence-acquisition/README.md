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
