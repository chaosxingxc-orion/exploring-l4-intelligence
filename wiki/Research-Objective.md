---
title: "Research Objective & Current State"
role: "HOT single current-state entry; supersede in place"
last_refresh: "2026-08-24 — DEV-500 CONFIRMED: +19.75pp held-out, CI excludes zero"
---

# Research Objective & Current State

> Default reading order: client guide → this page → `wiki/Project-Thesis.md`. Load campaign or
> experiment detail only through the CURRENT router or `wiki/Experiment-Assets.md`.

## Current gate and authority

Stage accounting is direction-local. Endpoint:
`DIRECTION_LOCAL_PIPELINE__R1_SUNSET__SPEECH_AWARE_EVIDENCE_ACQUISITION_OWNER_GO__STAGE2A_R0_INCOMPLETE__R1_WITHHELD`.
Core = Qwen3-Omni-30B through local llama.cpp; study domain = speech and spoken-language tasks.

The first semantic object, **speech-aware evidence acquisition** (R2 audit provenance), is
`PASS_STAGE1C_FORMAL_OPENING` and admitted under `OWNER_GO_AND_EXECUTION_CONTRACT`. Owner GO was
signed 2026-08-03; the single self-contained effective authority (GO + speech-only identity +
Stage‑3 stop line) is
`wiki/experiments/speech-aware-evidence-acquisition/2026-08-04-owner-consolidated-execution-contract.md`.
Repository: `studies/speech-aware-evidence-acquisition/`; remote is private.

No parameter modification, task-trained model or additional answering LLM is allowed. Model-facing
execution stays fail-closed behind E0 D1–D4 and a runtime receipt (closed 2026-08-04,
gate-verified). D0 is closed for Earnings21, Earnings22 and ConEC.
FSD50K, AudioSet and ESC-50 remain local governed bytes but are outside this study and cannot enter an
experiment, baseline or claim. `docs/datasets.lock.json` is the only live asset authority.

R1 is `NO_GO_AS_STANDALONE_DIRECTION__SUNSET_BEFORE_STAGE2`; R3–R9 remain `OWNER_UNVERIFIED` and do not
block this study.

## Research object

For an API-only frozen speech-capable omni core, build an external reward-guided control plane that
improves speech-domain capability by separately controlling:

1. `OBS` — speech observation and re-resolution;
2. `ORG` — knowledge organization and provenance;
3. `SUPPLY` — evidence selection, amount, order and timing;
4. `USE` — evidence admission, verification, iteration and stopping.

The motivating failure is speech-specific, not “audio in general”: a misheard entity can produce
correlated-but-wrong evidence and reinforce the original error. External knowledge addresses
accessibility, current/proper-name and verifiability gaps, while controls must measure the new risks
of irrelevant evidence, context pollution and reward hacking.

The evaluation contract has three inseparable parts:

- effectiveness: task/entity/QA scores, wrong-to-correct and correct-to-wrong, stability and tails;
- reasonableness: factorial attribution, legal information boundary, provenance, negative/oracle
  controls and evidence-use verification;
- efficiency: calls, tokens, latency, GPU/CPU, processed speech seconds, evidence volume and unit gain.

## Next action

Stage-2A discovery in flight (standing GO). 2026-08-24: the DEV-100 campaign froze at 72/100
vs 48 direct; the **DEV-500 confirmatory one-touch read then CONFIRMED the frozen cell on
held-out data: unexposed-400 +19.75 pp (52.50→72.25%), 90% CI [+16.5,+23.0] excludes zero,
McNemar p 7e-22, W→C 81 / C→W 2; ablations attribute the gain to the retrieval signal
(random exemplars are NEGATIVE); BLEND operates at the k=5 reachability ceiling.** Verdicts:
study `docs/readiness/2026-08-24-dev500-confirmatory-verdict.md` (+ dev100 campaign verdict
and reviewer/literature audits). **DEV-1000 and Audio2Tool gates OPEN.** Stage-2B freeze
`bb995d5` awaits owner approval. Digest:
`wiki/experiments/speech-aware-evidence-acquisition/README.md`.

The Wiki controls experiment identity and decisions; the study repo owns code/config/tests;
`SPEECHRL_DATA_DIR` and MLflow own large artifacts. Route through `wiki/Experiment-Assets.md`.

## Formal, legacy and routing boundaries

Carriers bind stages (Decision-Log continuation entry 91): Stage‑1 = umbrella; Stage‑2 = `studies/<slug>`, endpoint =
qualified paper candidates; Stage‑3 = `papers/<slug>` under `OWNER_GO_AND_PAPER_EXECUTION_CONTRACT`.
One papers carrier is admitted: **`papers/meeting-minutes-agent/`** (owner GO 2026-08-17;
from-scratch research object; private remote). The Stage‑1B program-level Lean layer is retired; formal work is
rebuilt per admitted study and claim in Stage‑2. The fixed Stage‑1B v5 320-work union remains
historical evidence; H5 remains `WITHHOLD_NON_LOAD_BEARING`. Candidate IDs are audit provenance, not
engineering identities; admitted repos live at `studies/<semantic-name>/`. R2R1 remains
`RETIRED_WITHOUT_DISTRIBUTION_OR_INDEPENDENT_ACCEPTANCE`. Literature work is a bounded delta lane
through `wiki/survey/README.md`; the retired package is at
`wiki/archive/working/system-first-survey-current/`. It reopens Stage‑1 only if new evidence
invalidates the problem, carrier legality, information boundary or reproducibility contract.

## Supersession rule

Supersede this HOT page in place when study admission, execution authority, speech-only boundary,
reliability objective, formal assumptions or direction priority changes. Preserve transactions in cold
audit and dated decision records.
