# SURVEY-RESP-2026-07-14-01 — Survey v2 replay bundle

## What this is

This is a machine-regenerated **replay bundle** for Survey v2 (Stage-1A, workflow `wf_c6ed06f2`), built under the doctoral-review remediation P0 opened against the 2026-07-14 review of Survey v2. It exists to answer one question mechanically, not by assertion: *given the two artifacts the survey actually produced — the 305-line search/fetch query log and the 113-row scout ledger — what can be reconstructed, and what honestly cannot?*

Every file in this directory except `build_and_validate.py` itself is generated output. Nothing here was hand-edited after generation. The single generating script is committed alongside its output so any reviewer can rerun it and diff the result.

Bundle status token for this round: **`ROUND1_SCOUT_COMPLETE`**.

BUNDLE_STATUS_TOKEN: ROUND1_SCOUT_COMPLETE
Per the replayability template §4 this permits forming a candidate map; it explicitly does **not** permit claiming saturated / unique / complete / decision-ready for Survey v2 as a whole — those claims require `LOCALLY_SATURATED_WITHIN_PROTOCOL` or `STAGE1C_DECISION_READY`, which this bundle does not establish.

The formal point-by-point response letter to the review lives at
`wiki/2026-07-14-survey-v2-response-and-p0-remediation.md` (authored separately by the coordinator; not part of this bundle).

## Headline numbers (all machine-recomputed — see `flow_report.yaml`)

| Quantity | Value |
|---|---|
| Search/fetch events logged (A) | 305 (SEARCH=218, FETCH=87) |
| Events classified FAILED | 18 |
| Events OUTCOME_UNVERIFIED_RAW_UNAVAILABLE | 287 |
| Ledger paper-rows (B) | 113 |
| → after exact-id dedup (Stage 1) | 110 |
| → after arXiv-id regex grouping (Stage 2) | 104 |
| → after explicit alias clusters (Stage 3, final) | 94 |
| Historical estimate in B (`_est`) | ~93 — **not reproducible**, see `dedup_report.json` |
| claim_evidence rows | 113 base + 5 corrections = 118 |
| UNVERIFIED-CITATION rows | 2 (2512.10170, 2512.10403) |

## FAILED-event classification method (search_events.jsonl `status`)

A `note` is classified `FAILED` only if it contains one of these substrings (word-boundary matched, case as shown except `denied` which is matched case-insensitively): `FAILED`, `BLOCKED`, `Blocked`, `NOT_RESOLVED`, `socket-failed`, `denied`. This is narrower than a bare case-insensitive `fail`/`block` search on purpose — lower-case `fail`/`block` inside running prose (e.g. row 116 'First attempt **failed** (socket closed); retried later successfully', or notes describing some *other* paper's name/finding, e.g. 'judge-BoN-**fail**') do not mark this event's own outcome as failed; only the deliberate ALL-CAPS/marker-style annotations the log author actually used for that purpose do. Every event that is not classified FAILED is honestly marked `OUTCOME_UNVERIFIED_RAW_UNAVAILABLE` — the log records what was learned, not a raw HTTP/tool status code, so "not FAILED" is not the same claim as "succeeded".

Matched-substring counts across the 18 classified FAILED events:

- `BLOCKED`: 2 event(s)
- `Blocked`: 1 event(s)
- `FAILED`: 13 event(s)
- `denied`: 1 event(s)
- `socket-failed`: 1 event(s)

## What is honestly missing forever (`RAW_EVENT_UNAVAILABLE`)

The following are **not reconstructable** from A/B and are not guessed at anywhere in this bundle:

- Raw request/response bodies for all 305 search/fetch events (A records only the query, engine, date, result_cap and a human-written note, never the raw payload).
- The search-results universe (ranked candidate lists actually returned per query) — A logs the query, not the result set.
- Any screening/include-exclude decision trail (B records a final grade per row, not the reasoning steps that produced it).
- Intra-day timestamps — A carries date-only granularity (`2026-07-14` for every row); `timestamp_utc` is `null` throughout, never fabricated.
- Per-query agent identity — only the workflow-level `agent_id` (`wf_c6ed06f2`) is known; which of possibly several session agents ran any individual query is unrecorded.
- A pre-registered search protocol (`protocol.yaml` in the template's suggested layout) — none was frozen before searching, so this bundle does not include one rather than backfill a retrospective one and call it preregistered.
- `search_results.jsonl` / `screening_decisions.jsonl` from the template's suggested layout — both require raw data this round never captured; omitted rather than faked.

## Input provenance note (found during the build, recorded honestly)

The build task specified all three inputs as "canonical at commit 233dc7eb". This is **verified true** for A (`wiki/survey/2026-07-14-search-query-log.jsonl`) and B (`wiki/survey/2026-07-14-scout-ledger-round2.json`) — their on-disk bytes are byte-identical to the git blob at 233dc7eb. It is **verified false** for the template spec (`wiki/2026-07-14-survey-response-replayability-template.md`): that file does not exist at commit 233dc7eb at all (`git show 233dc7eb:<path>` fails); it was introduced two commits later at `b41f9f85db359fa5b13cadbcb4024c130d43542e` and is unchanged through current HEAD. See `manifest.yaml` → `inputs` for the full detail. This is reported rather than silently assumed correct, consistent with this bundle's own no-fabrication rule.

## How to rebuild

From this directory:

```
C:\Python314\python.exe build_and_validate.py
```

The script is deterministic (no network, no wall-clock, stdlib only) and regenerates every other file in this directory byte-for-byte from the two canonical inputs plus the literal, clearly-labeled correction facts hardcoded near the top of the script. It exits 0 iff every check in `validation_report.txt` passes, non-zero otherwise.

## Files in this bundle

| File | Lines | Purpose |
|---|---|---|
| `build_and_validate.py` | 1617 | the one generator/validator script (this is the only file not itself generated) |
| `search_events.jsonl` | 305 | one row per query-log event in A, honestly graded |
| `papers.jsonl` | 94 | 94 deduplicated canonical works, full merge evidence trail |
| `claim_evidence.jsonl` | 118 | 113 base rows (1 per B row) + 5 correction rows |
| `round2_new_targets.jsonl` | 8 | 8 round-2 candidates surfaced by five-lens verification, not yet graded |
| `dedup_report.json` | — (JSON, not JSONL) | full 3-stage dedup pipeline trace + historical-estimate reconciliation attempt |
| `flow_report.yaml` | — | machine-recomputed flow counts only |
| `manifest.yaml` | — | bytes/lines/sha256 for every generated file + input provenance |
| `validation_report.txt` | — | the actual check run, PASS/FAIL, exit code |
| `README.md` | — | this file |

`survey_response.md` is intentionally **not** in this bundle; per the task it is added after the build by the coordinator and lives at `wiki/2026-07-14-survey-v2-response-and-p0-remediation.md`.

