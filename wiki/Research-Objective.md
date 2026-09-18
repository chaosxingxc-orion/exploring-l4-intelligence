---
title: "Research Objective & Current State"
role: "HOT single current-state entry; supersede in place"
last_refresh: "2026-09-17"
---

# Research Objective & Current State

> Default reading order: client guide → this page → `wiki/Project-Thesis.md`. The Wiki owns
> experiment identity and decisions, the study repo owns code/config/tests, `SPEECHRL_DATA_DIR` and
> MLflow own large artifacts; route detail through `wiki/Experiment-Assets.md`.

## Current gate and authority

Stage accounting is direction-local. Endpoint:
`DIRECTION_LOCAL_PIPELINE__R1_SUNSET__SPEECH_AWARE_EVIDENCE_ACQUISITION_OWNER_GO__STAGE2A_R0_CLOSED__R1_RELEASED`.
Core = Qwen3-Omni-30B through local llama.cpp; study domain = speech and spoken-language tasks.

The first semantic object, **speech-aware evidence acquisition** (R2 audit provenance), is
`PASS_STAGE1C_FORMAL_OPENING` and admitted under `OWNER_GO_AND_EXECUTION_CONTRACT`. Owner GO was
signed 2026-08-03; the single self-contained authority (GO + speech-only identity + Stage‑3 stop
line) is
`wiki/experiments/speech-aware-evidence-acquisition/2026-08-04-owner-consolidated-execution-contract.md`.
Repository: `studies/speech-aware-evidence-acquisition/`; remote is private.

No parameter modification, task-trained model or additional answering LLM is allowed. Model-facing
execution stays fail-closed behind E0 D1–D4 and a runtime receipt (closed 2026-08-04,
gate-verified). D0 is closed for Earnings21, Earnings22 and ConEC. FSD50K, AudioSet and ESC-50 are
local governed bytes outside this study and can never enter an experiment, baseline or claim.
`docs/datasets.lock.json` is the only live asset authority.

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
accessibility, proper-name and verifiability gaps; controls must measure the new risks of irrelevant
evidence, context pollution and reward hacking.

The evaluation contract has three inseparable parts:

- effectiveness: task/entity/QA scores, wrong-to-correct and correct-to-wrong, stability and tails;
- reasonableness: factorial attribution, legal information boundary, provenance, negative/oracle
  controls and evidence-use verification;
- efficiency: calls, tokens, latency, GPU/CPU, processed speech seconds, evidence volume, unit gain.

## Next action

Focus SLURP; E21 and Audio2Tool held. Base = the sealed dual-store anchor
(TRAIN A SLU 48.53 / intent 77.96). Bar: OFFICIAL SLU-F1 >= 64 and intent >= 78, replicated
(decision 23: v3 beside, never the bar; gains never assumed additive). Program: study
`docs/superpowers/specs/2026-09-16-slurp-v2-base-program-design.md`. B0/B0r HARMFUL (loop retained);
**B4b (slot store v2) ADMITTED +2.55 [+1.13, +3.98]**; **B1 (speech-keyed exemplars) SLU 61.14,
+12.61 [+10.54, +14.60], intent 80.19, ADMITTED after its twin (B1 - twin +7.83 [+5.85, +9.75])**.
Directive 11: node context policy (B7a-B7b). Order: B5e (M1+M4b, recovery flying) -> B5er -> v2.0
lock -> B6 -> B4b replicate resume -> B2 v3, B7a, B4a, B7r/c/b as v2.1. Decision 22: every cell
supports checkpoint resume (E10); 24: task-owned, no sleep.

## Formal, legacy and routing boundaries

Carriers bind stages (Decision-Log continuation entry 91): Stage‑1 = umbrella; Stage‑2 =
`studies/<slug>`, endpoint = qualified paper candidates; Stage‑3 = `papers/<slug>` under
`OWNER_GO_AND_PAPER_EXECUTION_CONTRACT`. One papers carrier is admitted:
**`papers/meeting-minutes-agent/`** (owner GO 2026-08-17; from-scratch object; private remote).
The Stage‑1B program-level Lean layer is retired; formal work is rebuilt per admitted study and
claim in Stage‑2; the fixed Stage‑1B v5 320-work union stays historical evidence and H5 stays
`WITHHOLD_NON_LOAD_BEARING`. Candidate IDs are audit provenance, not engineering identities;
admitted repos live at `studies/<semantic-name>/`. R2R1 remains
`RETIRED_WITHOUT_DISTRIBUTION_OR_INDEPENDENT_ACCEPTANCE`. Literature work is a bounded delta lane
through `wiki/survey/README.md`; retired:
`wiki/archive/working/system-first-survey-current/`. It reopens Stage‑1 only if new evidence
invalidates the problem, carrier legality, information boundary or reproducibility contract.

## Supersession rule

Supersede this HOT page in place when study admission, execution authority, speech-only boundary,
reliability objective, formal assumptions or direction priority moves. Preserve transactions in cold
audit and dated decision records.
