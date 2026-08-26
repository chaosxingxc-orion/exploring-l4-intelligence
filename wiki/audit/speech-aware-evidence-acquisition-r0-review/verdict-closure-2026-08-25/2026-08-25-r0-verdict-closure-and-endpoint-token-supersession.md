---
title: "R0 verdict closure and endpoint-token supersession"
date: "2026-08-25"
artifact_type: "STATUS_CLOSURE_RECORD"
campaign: "speech-aware-evidence-acquisition-r0-review"
round: "verdict-closure-2026-08-25"
responds_to: "independent-rereview-2026-08-07"
verdict_disposition: "AT_ISSUE_STATUS_CLOSED"
owner_authority_claimed: false
model_touch_performed: false
---

# R0 verdict closure and endpoint-token supersession

## 1. What this record is, and what it is not

The `independent-rereview-2026-08-07` round returned the at-issue status

```
R0_OVERALL_INCOMPLETE__R0_2_REPAIR_REQUIRED_FOR_BROKEN_OPERATOR_PATH__R1_MODEL_FACING_EXECUTION_WITHHELD
```

and the implementation response accepted it in full. Both round artifacts are correct as of
2026-08-07 and **neither is amended, corrected or rewritten here**. Registered audit bytes are
immutable from their first commit (`wiki/AI-Collaboration.md` §2); this record supersedes the
*status* those artifacts carried, not their content.

This is a status closure record. It claims no owner signature, no new execution authority and no
verdict of its own. It performed no model contact and no tool contact.

## 2. Why a new round artifact, and not an epoch iteration

`wiki/AI-Collaboration.md` reserves `wiki/audit/<campaign>/epoch-<N>/<round-id>/<name>-<ordinal>.md`,
with a `consolidation-receipt.json` and a registry pin, for **amendments and corrections to audit
artifacts themselves**. Nothing in the 2026-08-07 round is being amended or corrected: the reviewer's
findings were true, the response's acceptance was true, and the withholding was correctly applied.
What changed is the world the verdict was measured against.

The campaign index states the applicable rule directly — "corrections append a new round artifact
rather than editing one" — and the placement table routes ordinary transactions to
`wiki/audit/<campaign>/<round-id>/`. This record therefore takes the ordinary round form the campaign
already uses (`<round-id>/<date>-<name>.md`) and is registered by an appended index row.

## 3. Each withheld condition, closed at source

| Condition from the 2026-08-07 verdict | State on 2026-08-25 | Verified at |
|---|---|---|
| `R0.1` readiness memo + innovation ledger were an empty `(fill)` template | **CLOSED.** Survey product exists with zero remaining `(fill)` placeholders | `wiki/experiments/speech-aware-evidence-acquisition/published-baselines.md`, front matter `source_surveys: "study repo docs/readiness/2026-08-07-*.md (R0.1, model-free)"` |
| `R0.2` official CLI entry point unexecutable (B1); runbook not self-consistent (B2) | **CLOSED.** `core/driver/__main__.py` present, `saea-driver` console script registered, subprocess-level dispatch contract test present | study repo `master`: `src/speech_aware_evidence_acquisition/core/driver/__main__.py`, `pyproject.toml` `saea-driver = ...cli:main`, `tests/contract/test_cli_module_dispatch.py` |
| `R0.3` smoke `SAEA-E-001` not authorized, not run | **CLOSED.** Executed 2026-08-09, registered with receipts; decision column reads "R0 exit criterion (measurement integrity) MET" | `wiki/experiments/speech-aware-evidence-acquisition/README.md`, ledger row `SAEA-E-001` |
| `R1` model-facing execution withheld pending the above | **RELEASED** by owner directive, which adopts the R1 re-plan (P0–P4) as the execution form and sets the execution sequence beginning with `SAEA-E-001` | `wiki/experiments/speech-aware-evidence-acquisition/2026-08-08-owner-go-baseline-reproduction.md` |

Every mechanism the verdict relied on remains in force. Release of the withholding is not a waiver:
each model contact still requires its own `ExecutionPlan`, its own exposure pre-registration row and
the fail-closed gates, exactly as the 2026-08-08 owner record states.

## 4. The endpoint token

`wiki/Research-Objective.md` carried the program stage-accounting endpoint

```
DIRECTION_LOCAL_PIPELINE__R1_SUNSET__SPEECH_AWARE_EVIDENCE_ACQUISITION_OWNER_GO__STAGE2A_R0_INCOMPLETE__R1_WITHHELD
```

whose two trailing fields entered from this campaign: `STAGE2A_R0_INCOMPLETE` at `26386cb`
(2026-08-07, from this rereview) and `R1_WITHHELD` at `28d6736` (2026-08-05, from the first
independent review). Both are closed by §3, so the pair is superseded to

```
DIRECTION_LOCAL_PIPELINE__R1_SUNSET__SPEECH_AWARE_EVIDENCE_ACQUISITION_OWNER_GO__STAGE2A_R0_CLOSED__R1_RELEASED
```

`R1` in the trailing field denotes the study's first post-R0 experiment round, **not** the sunset
direction R1, which is the separate leading `R1_SUNSET` field. That distinction is unchanged.

The string had three carriers. Two are live and move together in one commit —
`wiki/Research-Objective.md` and the `required_truth` tuple of
`scripts/checks/test_ai_context_surface.py` — and the third is
`independent-rereview-2026-08-07/2026-08-07-implementation-response.md` §4, which records the token
it wrote on 2026-08-07 and keeps its original bytes. This record is that third carrier's successor.

## 5. Not claimed here

- No Stage-2B qualification. The study's own current language is "Stage-2A discovery in flight
  (standing GO)".
- No superiority, generality or publication-grade claim, and no Stage-3 activity.
- No owner ruling. The owner authority relied on in §3 is the pre-existing 2026-08-08 record, cited,
  not extended.
