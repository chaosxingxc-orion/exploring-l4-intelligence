# Claim Ledger v2 — Restructure Report (Gate-A)

- **Date:** 2026-07-14
- **Status token:** `CLAIM_LEDGER_V2_SINGLE_PASS_AI`
- **generated_by:** `claim-ledger-v2 restructure, single-pass AI` (stamped on every row)
- **verification_status:** `SINGLE_PASS_AI_RESTRUCTURED`; **verified_by:** `null`; **double_review_pending:** `true` (all rows)
- **Ledger file:** `claim_ledger_v2.jsonl` (62 rows, one JSON object per line, ordered by `claim_id` CL2-0001..CL2-0062)
- **Drops pointer:** `claim_extract_exclusions.jsonl` (11 rows; see §Drops below)
- **Source:** restructure of `../2026-07-14-claim-ledger-v1/claim_ledger_v1.jsonl` (44 rows) per the doctoral adversarial re-review §4.1–4.5 (`../../2026-07-14-p0r-progress-submission-doctoral-adversarial-rereview.md`).
- **Scope of edits:** only files inside `wiki/survey/2026-07-14-claim-ledger-v2/`. No upstream artifact, protocol, census, hot-state, or v1 file was modified.

## Binding review-status line

**Every kill and every occupancy/whitespace verdict in this ledger is DIRECTION-ONLY
(hypothesis-grade) until human double review completes.** This is a single-pass AI
*restructure* of the v1 single-pass AI extraction — no independent second reviewer has signed
any row. No verdict here may be quoted as settled in any owner-facing decision document.
Synthesis-level verdicts (5 rows, `evidence_grade=SYNTHESIS_PENDING_REVIEW`) are especially
non-final: they aggregate component rows and are carried at `MINOR`/`MATERIAL`/`UNVERIFIED`
discrepancy status, never inheriting a component's grade.

All counts below are reported **separately, never aggregated**. In particular the three
non-synthesis evidence grades must not be summed into any combined "verified" figure, and the
discrepancy five-way counts REPLACE the retracted "43 discrepancies" headline.

---

## Headline counts (reported separately, per the reviewer's rule)

| Headline | Value |
|---|---|
| **Rows** (one per claim × paper_work × evidence_span) | **62** |
| **Unique claims** (`source_key`, after `-a/-b/-c` dedup) | **44** |
| **Paper works covered** (distinct `paper_work_id`) | **31** |
| Rows dropped at extract stage (pointer only, not counted above) | 11 → `claim_extract_exclusions.jsonl` |

Row-level split: `SINGLE` 39 · `PER_WORK_COMPONENT` 18 · `SYNTHESIS` 5.

### Row → claim reconciliation (v1 → v2)

- v1 had 44 rows / 40 unique `claim_key`s.
- **3 duplicated keys deduplicated** with distinct scopes (old key kept as `source_key`, suffixed):
  - `open-strict-i2-same-core` → `-a` (P-0075 READ external-TTS), `-b` (P-0031 scaling-auditory, scorer unverified), `-c` (P-0005 jia-SER, scorer unverified).
  - `open-i3-combined-goodhart-speech` → `-a` (P-0080 text Goodhart owned-in-text), `-b` (P-0034 frozen-ALLM abstention occupied).
  - `op-speechqe-hydraqe-trained-scorers` → `-a` (P-0017 SpeechQE), `-b` (P-0018 HydraQE).
- **5 composite (multi-work) rows split** into per-work rows + one synthesis row each:
  - `kill-i1-i2-audio-understanding` → P-0031 + P-0032 + P-0036 (per-work) + synthesis (4 rows).
  - `occupy-supply-type-analogy-only` → P-0087 (ColdStart) + P-0085 (GenRM) + synthesis (3 rows).
  - `occupy-text-training-free-rl` → P-0091 + P-0092 + P-0066 + synthesis (4 rows).
  - `open-umbrella-intersection` → P-0064 + P-0031 + P-0091 + P-0092 + P-0066 + synthesis (6 rows).
  - `reanchor-coordinator-verified-depth-cap` → P-0071 + P-0075 + P-0031 + P-0064 + P-0005 + synthesis (6 rows).
- Net: 44 → 62 rows; 40 → 44 unique `source_key`s (40 − 3 dup + 7 scoped = 44).
- **Synthesis rows never inherit the strongest component grade** — each is `SYNTHESIS_PENDING_REVIEW` and `REFERENCE`s its components via `component_refs`.

---

## Evidence-grade distribution (recounted after downgrades — separate buckets, do not sum)

| evidence_grade | count |
|---|---|
| CLAIM_LOCATED_FULLTEXT | 35 |
| ABSTRACT_ONLY | 20 |
| FULLTEXT_UNREACHABLE_THIS_ROUND | 2 |
| SYNTHESIS_PENDING_REVIEW | 5 |

**Downgrades applied (reviewer §4.4 — the 5 abstract-locator rows named by the reviewer):**
- `occupy-umbrella-system-audiotoolagent` (CL2-0029): `CLAIM_LOCATED_FULLTEXT` → `ABSTRACT_ONLY`
  (version + locator both cite the abstract).
- `occupy-i3-conformal-ser-trained` (CL2-0021): `CLAIM_LOCATED_FULLTEXT` → `ABSTRACT_ONLY`
  (locator pins only the abstract).
- `occupy-text-training-free-rl` (3 per-work CL2-0025/0026/0027): all `ABSTRACT_ONLY`
  (locators are component abstracts); its synthesis CL2-0028 = `SYNTHESIS_PENDING_REVIEW`.
- `open-umbrella-intersection` (5 per-work CL2-0047..0051): all `ABSTRACT_ONLY` (component
  abstracts); its synthesis CL2-0052 = `SYNTHESIS_PENDING_REVIEW`.
- `reanchor-coordinator-verified-depth-cap`: the 2 fulltext-reached-this-round works
  (mbr-asr P-0071 CL2-0053, READ P-0075 CL2-0054) keep `CLAIM_LOCATED_FULLTEXT`; the 3
  existence-check-only works (P-0031/P-0064/P-0005 CL2-0055/0056/0057) = `ABSTRACT_ONLY`;
  synthesis CL2-0058 = `SYNTHESIS_PENDING_REVIEW`.

**Rows keeping `CLAIM_LOCATED_FULLTEXT`** do so because their locator names a table/section in
fetched fulltext (rule from re-review §4.5, item 5). The two `FULLTEXT_UNREACHABLE_THIS_ROUND`
rows (CL2-0045 scaling-auditory, CL2-0046 jia-SER, under `open-strict-i2-same-core`) retain that
grade — fulltext socket-closed this round.

## Discrepancy_status five-way counts (this REPLACES the retracted "43 discrepancies")

| discrepancy_status | count | meaning |
|---|---|---|
| NONE | 20 | v1 field began "None"/"None material" (the 11 no-discrepancy singles) or component confirmed with no discrepancy |
| MINOR | 19 | confirm-only / additional-detail / descriptor fix; verdict unaffected |
| MATERIAL | 15 | wrong numbers or mischaracterization affecting a verdict/number; requires upstream fix |
| CRITICAL | 2 | overturns a prior kill/occupancy label (both are reanchor corrections) |
| UNVERIFIED | 6 | fulltext unreachable / existence-only / absence claim not independently verifiable |

**The v1 "43" was a `nonempty_discrepancy_field_count`, not a defect count** — 11 of those 43
strings began with "None"/"None material" and several others were confirm-only. That headline is
retracted and replaced by the five-way table above. The 2 `CRITICAL` rows are:
- CL2-0060 `reanchor-progres-candidate-expansion` — overturns the prior kill-I1 DIRECT
  in-pool-selector label (ProGRes is candidate-expansion, not in-pool selection).
- CL2-0062 `reanchor-tap-ger-out-of-pool` — overturns the prior kill-I1 DIRECT label
  (TAP-GER is generative out-of-pool correction; 8.72 < 9.78 n-best oracle).

Three per-row booleans supplement the enum (counts of `true`):
`affects_identity_verdict` = 13 · `affects_numeric_claim` = 12 · `requires_upstream_correction` = 27.

## Claim_class distribution (explicit on every row)

| claim_class | count |
|---|---|
| KILL | 10 |
| NUMERIC_HEADLINE | 9 |
| OCCUPANCY | 10 |
| OPERATOR_CLASS | 11 |
| WHITESPACE_VERDICT | 12 |
| CORRECTION_REANCHOR | 10 |

Synthesis rows carry their family's class (KILL / OCCUPANCY×2 / WHITESPACE_VERDICT /
CORRECTION_REANCHOR).

## Support_relation (separate buckets)

| support_relation | count |
|---|---|
| SUPPORTS | 56 |
| LIMITS | 3 |
| RELATED_ONLY | 3 |

---

## Schema changes implemented (re-review §4.1–4.5)

1. **One row per (claim × paper_work × evidence_span)** — 5 composite rows split into 18
   per-work component rows; 5 synthesis rows added with `component_refs` pointing to their
   components and `evidence_grade=SYNTHESIS_PENDING_REVIEW` (never inherit strongest component
   grade). `row_level` ∈ {SINGLE, PER_WORK_COMPONENT, SYNTHESIS}.
2. **Globally unique `claim_id`** CL2-0001..CL2-0062; old `claim_key` kept as `source_key`; the
   3 duplicated keys deduplicated with `-a/-b/-c` suffixes, each carrying a distinct `scope`.
3. **`claim_class` on every row** (KILL / OCCUPANCY / NUMERIC_HEADLINE / OPERATOR_CLASS /
   CORRECTION_REANCHOR / WHITESPACE_VERDICT).
4. **`exact_claim_text` split** into `verbatim_span` (truly verbatim quotes; empty where the v1
   text was a restatement — e.g. CL2-0003/0005/0014 have empty `verbatim_span`) and
   `structured_extraction` (numbers/tables restated); `reviewer_inference` added to mark where
   the row is our interpretation (kill/occupancy verdicts, rho arithmetic, operator calls).
   `team_interpretation` retained verbatim for provenance.
5. **Evidence grade re-derived per span honestly** — the 5 reviewer-named abstract-locator rows
   downgraded to `ABSTRACT_ONLY` (or `SYNTHESIS_PENDING_REVIEW` for their synthesis rows); rows
   whose locator names a table/section in fetched fulltext keep `CLAIM_LOCATED_FULLTEXT`.
6. **`discrepancy_status` enum** (NONE/MINOR/MATERIAL/CRITICAL/UNVERIFIED) derived from the v1
   `discrepancy` strings (kept verbatim in `discrepancy_text`), plus the 3 booleans
   `affects_identity_verdict` / `affects_numeric_claim` / `requires_upstream_correction`.
7. **`paper_version_used = PIN_PENDING_CENSUS_V2`** wherever v1 wrote unversioned/latest/current
   or "version tag not captured", and on every synthesis row (no single pinnable version).
   16 rows carry `PIN_PENDING_CENSUS_V2` (5 synthesis + 8 unpinned singles + 3 existence-only
   coordinator components); a `paper_version_pin_status` flag marks each. Nothing invented —
   concrete v1 pins (vN, PMLR v204, dated) are preserved as-is.
8. **`verified_by=null`, `verification_status="SINGLE_PASS_AI_RESTRUCTURED"`,
   `double_review_pending=true`** on every row.

## Drops (§4.3)

`claim_extract_exclusions.jsonl` holds 11 rows — one per v1 extract-stage drop. v1 recorded only
the aggregate "Items dropped at extract stage: 11" with no per-item ID/content/reason, and the
per-item detail is not present in the repo. Each drop is therefore logged as
`RAW_DROP_DETAIL_UNAVAILABLE` (recoverable=false) to preserve the denominator without inventing
content; recovery requires the original extract-stage workflow logs (P1). This is a structural
stub, not a reconstruction of the dropped claims.

## Status

`CLAIM_LEDGER_V2_SINGLE_PASS_AI` — single-pass AI restructure of the v1 single-pass AI
extraction; human double review (P1) pending; **all kill / occupancy / whitespace verdicts
remain direction-only until human double review signs off row by row.**

---

## ⚠ Coordinator correction (2026-07-14, pre-commit)

The `claim_extract_exclusions.jsonl` in this directory was regenerated as the RECOVERED itemized
version (11 drops with verbatim raw_claim + drop_reason_code, recovered from the archived extract-agent
journal at docs/checks/2026-07-14-claim-ledger-v1-workflow-journal.jsonl) — the build agent's
"all RAW_DROP_DETAIL_UNAVAILABLE" stub is superseded; zero drops are unrecoverable.
Also note: 16 rows carry PIN_PENDING_CENSUS_V2 — census v2 (paper_works.jsonl, 95 works, 83 pinned)
is now available; the version-pin join is a Gate-A acceptance-pass item, not yet performed.
