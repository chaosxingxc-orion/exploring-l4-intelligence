# Survey Router — literature commons

This page routes literature material by lifecycle role. The Stage‑1 survey package (its gate,
protocol, tables and data) closed on 2026-08-03 and is archived; what remains here is the
program's cumulative literature infrastructure.

| Need | Route | Loading rule |
|---|---|---|
| Fulltext fetch ledger (append-only; every FETCH is registered) | `2026-07-17-sf-fulltext-ledger.jsonl` | Targeted `rg` only; payload bytes live outside Git under `$SPEECHRL_DATA_DIR/survey-fulltext/` |
| Long-lived paper census, claims, evidence records, official-metadata receipts | `registry/` | Targeted lookup only; append-only, cross-campaign |
| Audit artifact blob registry | `sf-audit-artifact-registry.json` | Machinery for `scripts/survey/sf_audit_immutability_check.py` |
| Mutable exploration for a live campaign | `workbench/<campaign>/` | Never default context and never a completion claim |
| Reviewer transaction and round history | `../audit/<campaign>/INDEX.md` | Open the campaign index first; load one exact round only for provenance |
| Closed Stage‑1 survey package and superseded working material | `../archive/working/system-first-survey-current/` and sibling campaign dirs | Cold; load only for a named historical/replay question |

Fetch tooling: `scripts/survey/sf_fulltext_fetch.py` and `scripts/survey/sf_official_metadata_fetch.py`
(receipts land in `registry/`). The full placement policy is canonical in
[`../AI-Collaboration.md`](../AI-Collaboration.md); the current research stage and authorization
boundary are canonical in [`../Research-Objective.md`](../Research-Objective.md).
