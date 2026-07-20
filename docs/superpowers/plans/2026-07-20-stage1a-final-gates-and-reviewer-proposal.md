# Stage-1A Final Gates and Reviewer Proposal Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Close the three reviewer-named Stage-1A gate majors, publish one immutable dual-track research proposal for independent review, and merge the verified package to `origin/master` without starting or authorizing Stage-1B.

**Architecture:** Preserve every released audit artifact and evidence-v6 report byte-for-byte. Add a fail-closed evidence kind/value compatibility layer and structured absence provenance to the mutable CURRENT evidence data, issue a new evidence-v7 report, generate one machine-readable bridge from the legacy corpus into the current claim flow, and generate the reviewer bibliography and proposal from bound sources. Register the supplied design review as round 13 and the proposal as the round-14 active review transaction; reserve round 15 for a genuinely independent reviewer report. A fresh non-implementer must adjudicate the changed absence-row hashes before the proposal package may report `PACKAGE_READY_FOR_REVIEW`.

**Tech Stack:** Python standard library, JSON/JSONL and Markdown artifacts, `unittest`, existing survey/check scripts, Git blob immutability, Windows Python plus WSL2 Ubuntu-24.04 Python 3.12, GitHub CLI/Git over WSL2.

**Design spec:** `docs/superpowers/specs/2026-07-20-reviewer-proposal-and-master-release-design.md`

---

## File map

**Create**

- `scripts/survey/sf_absence_provenance_migrate.py` — deterministic, checkable enrichment of the 22 current absence bindings.
- `scripts/survey/test_sf_absence_provenance_migrate.py` — migration idempotence, provenance, and semantic-equivalence tests.
- `scripts/survey/sf_identity_taxonomy_v7_test.py` — evidence-v7 integration and mutation harness; taxonomy derivation remains v6.
- `scripts/survey/test_sf_identity_taxonomy_v7_harness.py` — counterexample, occupancy, input-binding, and report tests.
- `wiki/survey/current/data/absence-evidence-adjudication-v2.json` — fresh non-implementer verdicts for all changed row hashes.
- `docs/checks/system-first-stage1a/evidence-v7/identity-taxonomy-v7-test.json` — canonical aggregate evidence-v7 result.
- `docs/checks/system-first-stage1a/evidence-v7/identity-taxonomy-v7-test.nt.json` — Windows result.
- `docs/checks/system-first-stage1a/evidence-v7/identity-taxonomy-v7-test.posix.json` — WSL2 result.
- `scripts/survey/sf_existing_corpus_disposition.py` — deterministic census/seed/bibliography/claim/full-text crosswalk generator and checker.
- `scripts/survey/test_sf_existing_corpus_disposition.py` — denominator, alias, orphan, grade-preservation, and no-query tests.
- `wiki/survey/current/data/existing-corpus-disposition-v1.json` — the only CURRENT bridge to legacy survey assets.
- `docs/checks/system-first-stage1a/context-v2/existing-corpus-disposition-check.json` — bound source receipt and crosswalk verdict.
- `scripts/survey/test_sf_bibliography_generator.py` — official metadata, placeholder, role, and frozen-query separation tests.
- `wiki/survey/current/bibliography.md` — generated reviewer-visible bibliography with no author placeholders.
- `scripts/survey/sf_reviewer_proposal_check.py` — proposal structure, source-binding, claim-diff, authority, and forbidden-claim checker.
- `scripts/survey/test_sf_reviewer_proposal_check.py` — negative and positive proposal contract tests.
- `wiki/survey/current/data/reviewer-proposal-source-manifest-v1.json` — exact proposal inputs with Git blobs/SHA-256/locators.
- `docs/checks/system-first-stage1a/context-v2/reviewer-proposal-check.json` — proposal checker receipt.
- `wiki/audit/system-first-stage1a/round-13/reviewer-proposal-design-stage1a-doctoral-review.md` — byte-preserved user-supplied design review.
- `wiki/audit/system-first-stage1a/round-14/research-proposal-and-stage1b-signoff-request.md` — immutable dual-track submission.
- `docs/checks/system-first-stage1a/context-v2/current-package-check.json` — integrated release gate.

**Modify**

- `scripts/survey/sf_evidence_contract.py`
- `scripts/survey/test_sf_evidence_contract.py`
- `scripts/survey/sf_identity_taxonomy_v6_test.py` only if a reusable entry point must be factored without changing v6 output.
- `wiki/survey/current/data/schema-v3/sidecars/*.sidecar.json`
- `wiki/survey/current/data/known-item-coding-v7.json`
- `scripts/survey/sf_bibliography_generator.py`
- `scripts/survey/sf_campaign_audit_index.py`
- `scripts/survey/test_sf_campaign_audit_index.py`
- `wiki/survey/sf-audit-artifact-registry.json`
- `wiki/audit/system-first-stage1a/campaign-index.json`
- `wiki/audit/system-first-stage1a/INDEX.md`
- `scripts/checks/ai_context_inventory.py`
- `scripts/checks/build_ai_context_manifest.py`
- `scripts/checks/test_ai_context_surface.py`
- `scripts/survey/sf_current_manifest.py`
- `scripts/survey/sf_current_package_check.py`
- `scripts/survey/test_sf_current_layer.py`
- `scripts/survey/test_sf_current_package_check.py`
- `scripts/survey/test_sf_manifest_consumers.py`
- `docs/checks/2026-07-19-sf-audit-immutability-check.json`
- `wiki/survey/current/manifest.json`
- `wiki/survey/current/README.md`
- `wiki/survey/current/status.md`
- `wiki/Research-Objective.md`
- generated AI context and current-package reports selected by the existing builders.

**Do not modify or create**

- Any file already registered as an immutable audit artifact, including `wiki/audit/system-first-stage1a/round-12/stage1a-readiness-correction.md`.
- `docs/checks/system-first-stage1a/evidence-v6/*` or `docs/checks/system-first-stage1a/context-v1/*`.
- `wiki/audit/system-first-stage1a/round-15/research-proposal-independent-doctoral-review.md`; only the independent reviewer may create it.
- `wiki/survey/2026-07-15-sf-queries.jsonl`, its 65 frozen query terms, or query compiler semantics.
- `docs/integrity/experiment_attempt_registry.jsonl` and every research-model, smoke, prototype, or Stage-1B execution surface.
- The remote GitHub Wiki.

---

### Task 1: Make the evidence-kind/value counterexample fail closed

**Files:**

- Modify: `scripts/survey/test_sf_evidence_contract.py`
- Modify: `scripts/survey/sf_evidence_contract.py`
- Test: `scripts/survey/test_sf_identity_taxonomy_v6_contract.py`

- [ ] **Step 1: Add red unit tests for the compatibility matrix**

Add tests that call `validate_bound_values` with otherwise-valid fixtures and assert:

```python
self.assertIn(
    "paper#path:signal:s:form:absence-incompatible-positive-value",
    validate_bound_values(row_with_signal_form("text_critique", "absence")),
)
self.assertIn(
    "paper#path:signal:s:source:absence-incompatible-positive-value",
    validate_bound_values(row_with_signal_source("llm_judge", "absence")),
)
for value in (False, None, "", "none", "unknown", []):
    self.assertNotIn(
        "absence-incompatible-positive-value",
        "\n".join(validate_bound_values(row_with_negative_absence(value))),
    )
```

Add one subtest for each required absence field: `value`, `inspected_scope`, `reason`, `source_version`, `coder`, and `adjudicator_provenance`. Missing, empty, or malformed provenance must fail.

- [ ] **Step 2: Reproduce the exact green mutation before the fix**

Run:

```powershell
python -m unittest scripts.survey.test_sf_evidence_contract -v
```

Expected before implementation: the positive `form`/`source` absence tests fail because the validator returns no compatibility error.

- [ ] **Step 3: Implement the shared compatibility policy**

Add these public constants/helpers to `sf_evidence_contract.py` and call `_validate_absence_entry` from `_validate_binding` after value equality:

```python
ABSENCE_REQUIRED_FIELDS = {
    "value",
    "inspected_scope",
    "reason",
    "source_version",
    "coder",
    "adjudicator_provenance",
}


def absence_value_allowed(value):
    return (
        value is False
        or value is None
        or value == ""
        or value == "none"
        or value == "unknown"
        or value == []
    )


def _nonempty_mapping(value, required):
    return (
        isinstance(value, Mapping)
        and all(isinstance(value.get(key), str) and value[key].strip()
                for key in required)
    )


def _validate_absence_entry(owner, field, expected, entry, failures):
    if entry.get("kind") != "absence":
        return
    if not absence_value_allowed(expected):
        failures.append(
            f"{owner}:{field}:absence-incompatible-positive-value"
        )
    for key in ABSENCE_REQUIRED_FIELDS:
        if key not in entry:
            failures.append(f"{owner}:{field}:absence-{key}-missing")
    if not isinstance(entry.get("inspected_scope"), str) or not entry["inspected_scope"].strip():
        failures.append(f"{owner}:{field}:absence-inspected_scope-invalid")
    if not isinstance(entry.get("reason"), str) or not entry["reason"].strip():
        failures.append(f"{owner}:{field}:absence-reason-invalid")
    if not _nonempty_mapping(entry.get("source_version"), {"source_id", "version_binding"}):
        failures.append(f"{owner}:{field}:absence-source_version-invalid")
    if not _nonempty_mapping(entry.get("coder"), {"identity", "source_sidecar"}):
        failures.append(f"{owner}:{field}:absence-coder-invalid")
    if not _nonempty_mapping(
        entry.get("adjudicator_provenance"),
        {"identity", "artifact", "verdict"},
    ):
        failures.append(f"{owner}:{field}:absence-adjudicator_provenance-invalid")
```

Keep list-vs-scalar type equality in `values_equal`; compatibility never replaces encoded-value equality.

- [ ] **Step 4: Run the focused suite green**

```powershell
python -m unittest scripts.survey.test_sf_evidence_contract scripts.survey.test_sf_identity_taxonomy_v6_contract -v
```

Expected: all tests pass; positive absence fails before derivation and legitimate negative absence passes.

- [ ] **Step 5: Commit the generic contract before data migration**

```powershell
git add scripts/survey/sf_evidence_contract.py scripts/survey/test_sf_evidence_contract.py scripts/survey/test_sf_identity_taxonomy_v6_contract.py
git commit -m "fix(survey): reject incompatible absence evidence"
```

---

### Task 2: Migrate current absence evidence and obtain independent delta adjudication

**Files:**

- Create: `scripts/survey/sf_absence_provenance_migrate.py`
- Create: `scripts/survey/test_sf_absence_provenance_migrate.py`
- Modify: `wiki/survey/current/data/schema-v3/sidecars/*.sidecar.json`
- Modify: `wiki/survey/current/data/known-item-coding-v7.json`
- Create: `wiki/survey/current/data/absence-evidence-adjudication-v2.json`

- [ ] **Step 1: Add red migration tests**

The tests must prove all of the following:

```python
self.assertEqual(22, report["absence_entries"])
self.assertEqual(0, report["positive_absence_entries"])
self.assertEqual(0, report["missing_provenance_entries"])
self.assertEqual(0, report["semantic_tuple_changes"])
self.assertEqual(first_render, second_render)
```

For every entry compare the tuple `(method_path_id, owner, field, kind, value)` before and after. Only `note -> reason`, `scope -> inspected_scope`, and provenance enrichment are allowed. Assert that `wiki/survey/2026-07-19-sf-queries.jsonl` is neither read nor written by the migration module.

- [ ] **Step 2: Implement a deterministic `--check`/`--write` migration**

For each absence entry derive:

```json
{
  "kind": "absence",
  "value": false,
  "inspected_scope": "the exact former scope text",
  "reason": "the exact former note text",
  "source_version": {
    "source_id": "the sidecar fulltext.id",
    "version_binding": "the sidecar fulltext.sha256 or canonical record locator"
  },
  "coder": {
    "identity": "the sidecar coder",
    "source_sidecar": "the repository-relative source sidecar path"
  },
  "adjudicator_provenance": {
    "identity": "/root/a6_adjudicator",
    "artifact": "wiki/survey/current/data/schema-v3-adjudication.json",
    "verdict": "AGREE"
  }
}
```

The renderer must preserve UTF-8 and stable key ordering. It must reject any absence tuple not found with `AGREE` in the prior adjudication artifact. Restamp rows with `sf_row_hash.py`, regenerate `known-item-coding-v7.json`, and emit a machine summary including old/new hashes.

- [ ] **Step 3: Run migration tests, write once, and prove idempotence**

```powershell
python -m unittest scripts.survey.test_sf_absence_provenance_migrate -v
python scripts/survey/sf_absence_provenance_migrate.py --write
python scripts/survey/sf_absence_provenance_migrate.py --check
python scripts/survey/sf_coding_generator.py --check
git diff --check
```

Expected: 22 enriched absence entries, zero semantic tuple changes, zero second-pass diff.

- [ ] **Step 4: Commit the mechanically reviewable delta**

```powershell
git add scripts/survey/sf_absence_provenance_migrate.py scripts/survey/test_sf_absence_provenance_migrate.py wiki/survey/current/data/schema-v3/sidecars wiki/survey/current/data/known-item-coding-v7.json
git commit -m "data(survey): bind absence evidence provenance"
```

- [ ] **Step 5: Stop for a fresh non-implementer delta review**

The reviewer receives the pre-migration commit, migration commit, 22 old/new tuples, old/new row hashes, the prior adjudication artifact, and the replay commands. The reviewer—not the implementer—creates `absence-evidence-adjudication-v2.json` with stable identity, nonparticipation and conflict declarations, exact reviewed commits/blobs, 22 per-entry `AGREE|DISAGREE` verdicts, and a summary. Any disagreement stops the release and returns to Step 2.

- [ ] **Step 6: Validate and commit the independent adjudication**

Add a test that requires 22/22 entries, exact new row hashes, stable reviewer identity, nonparticipation, conflict declaration, and `ALL_AGREE`. Run:

```powershell
python -m unittest scripts.survey.test_sf_absence_provenance_migrate -v
python scripts/survey/sf_absence_provenance_migrate.py --check
git add wiki/survey/current/data/absence-evidence-adjudication-v2.json scripts/survey/test_sf_absence_provenance_migrate.py
git commit -m "audit(survey): record absence evidence adjudication"
```

Expected: the adjudication is independently authored and every changed hash is covered. Do not continue if the file is absent, self-authored, incomplete, or contains `DISAGREE`.

---

### Task 3: Issue evidence-v7 without rewriting evidence-v6

**Files:**

- Create: `scripts/survey/sf_identity_taxonomy_v7_test.py`
- Create: `scripts/survey/test_sf_identity_taxonomy_v7_harness.py`
- Create: `docs/checks/system-first-stage1a/evidence-v7/identity-taxonomy-v7-test*.json`

- [ ] **Step 1: Add red end-to-end counterexample tests**

Copy only reusable fixture construction from the v6 harness. Add the exact reviewer mutation:

```python
row = find_row("2026.findings-acl.1724#pipeline")
signal = find_signal(row, "s_stage_judge")
signal["form"] = "text_critique"
signal["claim_evidence"]["form"] = {
    "kind": "absence",
    "value": "text_critique",
    "inspected_scope": "paper full text",
    "reason": "not contradicted",
    "source_version": {"source_id": "2026.findings-acl.1724", "version_binding": "fixture"},
    "coder": {"identity": "fixture", "source_sidecar": "fixture.json"},
    "adjudicator_provenance": {"identity": "fixture", "artifact": "fixture.json", "verdict": "AGREE"},
}
```

Restamp the row, then assert structure/binding/source validation is nonzero before occupancy derivation. Add a positive control using `value=False` and complete provenance.

- [ ] **Step 2: Implement the v7 harness as a release wrapper**

The harness must consume the current v6 taxonomy and schema-v3 sidecars, plus `absence-evidence-adjudication-v2.json`; keep the scientific derivation unchanged. Emit:

```json
{
  "schema": "sf-identity-taxonomy-evidence-v7-test",
  "verdict": "PASS",
  "absence_contract": {
    "entries": 22,
    "positive_entries": 0,
    "provenance_failures": 0,
    "independent_adjudication": "ALL_AGREE"
  },
  "counterexample": "REJECTED_BEFORE_DERIVATION",
  "occupancy_equal_to_v6": true
}
```

Bind every input path, Git blob or working-tree SHA-256, and output hash. The expected occupancy remains `RQ-SYS 5/11`, `reward_guided_selection 4/11`, and `trajectory_pool 2/11`.

- [ ] **Step 3: Run focused and platform-specific evidence checks**

```powershell
python -m unittest scripts.survey.test_sf_identity_taxonomy_v7_harness -v
python scripts/survey/sf_identity_taxonomy_v7_test.py --output docs/checks/system-first-stage1a/evidence-v7/identity-taxonomy-v7-test.nt.json
python scripts/survey/sf_identity_taxonomy_v7_test.py --output docs/checks/system-first-stage1a/evidence-v7/identity-taxonomy-v7-test.json
wsl -d Ubuntu-24.04 bash -lc "source ~/.venvs/speechrl/bin/activate && cd /mnt/d/chao_workspace/exploring-l4-intelligence/.worktrees/stage1b-readiness-remediation && python scripts/survey/sf_identity_taxonomy_v7_test.py --output docs/checks/system-first-stage1a/evidence-v7/identity-taxonomy-v7-test.posix.json"
```

Expected: all three reports say `PASS`, exact occupancy is identical, and the reviewer mutation is red.

- [ ] **Step 4: Prove evidence-v6 bytes were untouched and commit**

```powershell
git diff 2f16b23 -- docs/checks/system-first-stage1a/evidence-v6
git diff --check
git add scripts/survey/sf_identity_taxonomy_v7_test.py scripts/survey/test_sf_identity_taxonomy_v7_harness.py docs/checks/system-first-stage1a/evidence-v7
git commit -m "test(survey): issue fail-closed evidence v7"
```

Expected: first command has no output.

---

### Task 4: Generate the legacy-corpus disposition bridge

**Files:**

- Create: `scripts/survey/sf_existing_corpus_disposition.py`
- Create: `scripts/survey/test_sf_existing_corpus_disposition.py`
- Create: `wiki/survey/current/data/existing-corpus-disposition-v1.json`
- Create: `docs/checks/system-first-stage1a/context-v2/existing-corpus-disposition-check.json`

- [ ] **Step 1: Add red tests for exact denominators and orphan handling**

Assert these frozen observations from the current repository:

```python
self.assertEqual(95, report["census"]["total"])
self.assertEqual(92, report["seeds"]["total"])
self.assertEqual(65, report["bibliography"]["total"])
self.assertEqual(62, report["claim_ledger"]["rows"])
self.assertEqual(44, report["claim_ledger"]["unique_sources"])
self.assertEqual(31, report["claim_ledger"]["census_clusters"])
self.assertEqual(0, report["unexplained_orphans"])
```

Add failure tests for duplicate census disposition, unexplained seed/bibliography destination, silent exact-ID/alias merge, evidence-grade upgrade, and a query-file write attempt.

- [ ] **Step 2: Implement explicit identity and disposition records**

The generator reads the canonical census, seed records, bibliography v1, claim ledger/version pins, full-text ledger, and reviewer-known-item input. Each census work appears once. Each record contains:

```json
{
  "stable_id": "source-native stable identity",
  "version": "pinned source version or IDENTITY_UNRESOLVED",
  "source_campaign": "originating census/seed/bibliography/claim campaign",
  "inherited_evidence_grade": "original grade, never upgraded",
  "role": "DEEPLY_READ",
  "relevant_section": "the exact RQ or proposal section",
  "disposition_reason": "inclusion reason or REC-0 exclusion reason",
  "next_stage_action": "carry, verify, queue, or exclude",
  "locator": "available exact locator or empty string",
  "conflict_status": "NONE, MATERIAL, CRITICAL, UNVERIFIED, or IDENTITY_UNRESOLVED",
  "invalidating_condition": "condition that invalidates this routing"
}
```

Allowed roles are exactly `DEEPLY_READ`, `KNOWN_QUEUE`, `MEASUREMENT_INSTRUMENT`, and `BOUNDARY/NEGATIVE_PRIOR`. Identity links must state `EXACT_ID`, `EXPLICIT_ALIAS`, or `UNRESOLVED`; aliases carry both source IDs and provenance.

- [ ] **Step 3: Bind inputs and emit the check report**

The output records input path, `git hash-object` blob, SHA-256, generator version, and output SHA-256. It must reproduce and disclose:

- census: 95 total, 94 resolved, 1 unresolved, 83 arXiv/version-pinned;
- claim ledger: 62 rows, 44 unique sources, 31 census clusters, all 62 double-review-pending;
- census→seed 13/95, census→bibliography 3/95, seed→bibliography 9/92;
- seed arXiv→full text 19/88, bibliography arXiv→full text 16/47, census arXiv→full text 0/83;
- 15 MATERIAL, 2 CRITICAL, 6 UNVERIFIED, 19 MINOR, and 20 NONE discrepancies.

Run:

```powershell
python -m unittest scripts.survey.test_sf_existing_corpus_disposition -v
python scripts/survey/sf_existing_corpus_disposition.py --write
python scripts/survey/sf_existing_corpus_disposition.py --check
```

Expected: `census=95/95 seeds=92/92 bibliography=65/65 unexplained_orphans=0 verdict=PASS`.

- [ ] **Step 4: Commit the generated bridge**

```powershell
git add scripts/survey/sf_existing_corpus_disposition.py scripts/survey/test_sf_existing_corpus_disposition.py wiki/survey/current/data/existing-corpus-disposition-v1.json docs/checks/system-first-stage1a/context-v2/existing-corpus-disposition-check.json
git commit -m "data(survey): route existing corpus into current claims"
```

---

### Task 5: Complete the reviewer bibliography without changing frozen recall

**Files:**

- Modify: `scripts/survey/sf_bibliography_generator.py`
- Create: `scripts/survey/test_sf_bibliography_generator.py`
- Create: `wiki/survey/current/bibliography.md`
- Modify: `wiki/survey/current/tables/opening-guarantees.md`

- [ ] **Step 1: Add failing metadata and separation tests**

Tests require zero occurrences of `authors on official page` and exact official identities for:

```python
P1_HIGH = {
    "arXiv:2605.04531",
    "ACL:2025.acl-long.775",
    "ACL:2026.acl-industry.87",
    "arXiv:2605.23261",
}
P2_ADDITIONS = {"arXiv:2602.01381", "ACL:2026.acl-srw.1"}
```

Require the six existing P2 items, the four v9 boundary/measurement items, the ACL/arXiv Reinforced Agent identity binding, correct provenance and role for each reviewer-known item, and a statement that these items are not frozen-query recall.

- [ ] **Step 2: Replace placeholders with official metadata in the generator**

Keep one structured record per work: stable ID, title, full official author list, official URL, role, provenance (`V9_REQUIRED` or `REVIEWER_KNOWN_ITEM`), boundary hypothesis, and `query_recall_credit=false` for reviewer-known items. Do not change the 65-query file or compiler.

- [ ] **Step 3: Generate and verify the bibliography and opening roles**

```powershell
python -m unittest scripts.survey.test_sf_bibliography_generator -v
python scripts/survey/sf_bibliography_generator.py --output wiki/survey/current/bibliography.md
python scripts/survey/sf_bibliography_generator.py --check --output wiki/survey/current/bibliography.md
rg -n -i "author(s)? on official page|placeholder|unknown author" wiki/survey/current/bibliography.md
git diff 2f16b23 -- wiki/survey/2026-07-15-sf-queries.jsonl
```

Expected: tests pass; placeholder scan and frozen-query diff have no output. P1 is complete; P2 is visibly nonblocking.

- [ ] **Step 4: Commit bibliography closure**

```powershell
git add scripts/survey/sf_bibliography_generator.py scripts/survey/test_sf_bibliography_generator.py wiki/survey/current/bibliography.md wiki/survey/current/tables/opening-guarantees.md
git commit -m "docs(survey): complete reviewer bibliography metadata"
```

---

### Task 6: Build and validate the dual-track proposal

**Files:**

- Create: `scripts/survey/sf_reviewer_proposal_check.py`
- Create: `scripts/survey/test_sf_reviewer_proposal_check.py`
- Create: `wiki/survey/current/data/reviewer-proposal-source-manifest-v1.json`
- Create: `docs/checks/system-first-stage1a/context-v2/reviewer-proposal-check.json`
- Create later in this task: `wiki/audit/system-first-stage1a/round-14/research-proposal-and-stage1b-signoff-request.md`

- [ ] **Step 1: Add red proposal-contract tests**

Tests must reject a proposal that:

- omits either Track A or Track B;
- contains actual values for either requested verdict;
- claims Stage-1B is authorized, started, or signed;
- lacks the independence contract or owner-authorization provenance;
- lacks a complete v9 claim-diff row;
- uses an unbound numeric claim;
- includes `first-ever`, `novelty established`, `SOTA`, or contribution-as-result wording;
- credits reviewer-known items to frozen-query recall;
- omits the wiki dry-run incident or inherited prior exposure.

The positive fixture must expose only:

```text
REQUESTED_SCIENTIFIC_RATIONALE_FOR_CONTINUING_MAPPING = ADEQUATE|REVISE|INADEQUATE
REQUESTED_SEARCH_DESIGN_SIGNOFF = SIGN|WITHHOLD
```

- [ ] **Step 2: Implement the source manifest builder/checker**

Bind `Project-Thesis`, `Research-Objective`, current protocol/status, v9 proposal/review/response, round-12 correction, evidence-v7 reports, context-v2 corpus receipt, current bibliography/opening roles, context-v1 wiki incident, frozen query bytes, campaign index, and the design spec. For each input record repository-relative path, Git blob when tracked, SHA-256, purpose, and locator. Reject dirty mismatch between manifest bytes and proposal source references.

- [ ] **Step 3: Write the self-contained proposal**

Track A contains the north-star question, motivation, scoped gap, RQs, contribution hypotheses, staged method, falsifiers, risks, limitations, and doctoral value. Track B maps v9 E1–E5 and P0-A/B/C to contracts, negative tests, exact artifacts, Windows/WSL replay, context consolidation, frozen execution boundary, incident disclosure, P1 closure, and nonblocking P2 queue.

The v9 claim-diff table has exact columns:

```text
v9 claim ID and section | UNCHANGED|CORRECTED|WITHDRAWN|NEW | rationale | canonical evidence path + hash/locator | hypothesis_only|readiness_only
```

State only `PACKAGE_READY_FOR_REVIEW` / `SUBMITTED_FOR_INDEPENDENT_REVIEW`; explicitly keep `REVIEWED_SIGN_OR_WITHHOLD` and `OWNER_AUTHORIZED_STAGE1B` pending. State repair exposure as zero new discovery queries, zero research-model calls, and zero smoke runs within this repair, plus unchanged `INHERITED_PRIOR_EXPOSURE`.

- [ ] **Step 4: Run the proposal checker and hostile string scan**

```powershell
python -m unittest scripts.survey.test_sf_reviewer_proposal_check -v
python scripts/survey/sf_reviewer_proposal_check.py --write-report
rg -n -i "first[- ]ever|novelty (is )?established|state[- ]of[- ]the[- ]art|stage-1b (is )?(authorized|started|signed)" wiki/audit/system-first-stage1a/round-14/research-proposal-and-stage1b-signoff-request.md
```

Expected: checker `PASS`; hostile scan has no unauthorized assertion. Requested response values may appear only as schemas, never as filled verdicts.

- [ ] **Step 5: Keep the proposal uncommitted until the audit transaction is assembled**

Do not commit round 14 alone. Its first committed bytes must be registered and campaign-routed in Task 7 in the same commit.

---

### Task 7: Register rounds 13–14 and route the active review transaction

**Files:**

- Create: round-13 review and round-14 proposal paths.
- Modify: `scripts/survey/sf_campaign_audit_index.py`
- Modify: `scripts/survey/test_sf_campaign_audit_index.py`
- Modify: `wiki/survey/sf-audit-artifact-registry.json`
- Modify: `wiki/audit/system-first-stage1a/campaign-index.json`
- Modify: `wiki/audit/system-first-stage1a/INDEX.md`
- Modify: `scripts/checks/ai_context_inventory.py`

- [ ] **Step 1: Preserve the supplied review bytes at the final audit path**

Before editing, record the source SHA-256. Read the source, then use `apply_patch` to add the final
round-13 file with the exact same bytes; do not create or stage a root-level legacy path. Compare the
two SHA-256 values before continuing:

```powershell
Get-FileHash 'D:/chao_workspace/exploring-l4-intelligence/wiki/2026-07-20-reviewer-proposal-and-master-release-design-stage1a-doctoral-review.md' -Algorithm SHA256
Get-FileHash 'wiki/audit/system-first-stage1a/round-13/reviewer-proposal-design-stage1a-doctoral-review.md' -Algorithm SHA256
```

Expected: hashes match. The untracked root source is never staged.

- [ ] **Step 2: Add red campaign tests for an active proposal**

Add tests proving one `proposal` or `application` may be `ACTIVE_REVIEW_TRANSACTION`, that a `review` cannot be active, that two active transactions fail, and that a later review event cannot be appended into the same round. Preserve existing amendment/correction behavior.

- [ ] **Step 3: Narrowly extend campaign validation**

Replace the active-type assertion with:

```python
ACTIVE_REVIEW_TYPES = {"amendment", "correction", "proposal", "application"}
```

Keep exact-one-active, monotonic round, append-only prefix, carrier, verdict, and registered-blob checks. Route round 13 as a historical design review with the existing withholding semantics, and round 14 as a proposal with `PENDING_INDEPENDENT_REREVIEW` and `ACTIVE_REVIEW_TRANSACTION`.

- [ ] **Step 4: Pin both artifacts without a circular commit dependency**

Compute Git blobs from working-tree bytes:

```powershell
git hash-object wiki/audit/system-first-stage1a/round-13/reviewer-proposal-design-stage1a-doctoral-review.md
git hash-object wiki/audit/system-first-stage1a/round-14/research-proposal-and-stage1b-signoff-request.md
```

Append both path/blob pairs to `sf-audit-artifact-registry.json`; append round 13 and 14 semantic events to `campaign-index.json`; regenerate `INDEX.md`. Advance the registry baseline from 78 to 80 and the campaign baseline from 41 to 43 only after calculating and testing the exact new prefix SHA-256 values with `ai_context_inventory.py` helpers.

- [ ] **Step 5: Run audit contract checks**

```powershell
python -m unittest scripts.survey.test_sf_campaign_audit_index scripts.survey.test_sf_audit_immutability_check -v
python scripts/survey/sf_campaign_audit_index.py --write
python scripts/survey/sf_campaign_audit_index.py --check
python scripts/survey/sf_audit_immutability_check.py --write
python scripts/survey/sf_audit_immutability_check.py --check
```

Expected: registry `80 artifacts / 0 failures`; one active review transaction at round 14; no historical artifact changed.

- [ ] **Step 6: Commit the atomic audit transaction**

```powershell
git add wiki/audit/system-first-stage1a/round-13 wiki/audit/system-first-stage1a/round-14 wiki/survey/sf-audit-artifact-registry.json wiki/audit/system-first-stage1a/campaign-index.json wiki/audit/system-first-stage1a/INDEX.md scripts/survey/sf_campaign_audit_index.py scripts/survey/test_sf_campaign_audit_index.py scripts/checks/ai_context_inventory.py wiki/survey/current/data/reviewer-proposal-source-manifest-v1.json scripts/survey/sf_reviewer_proposal_check.py scripts/survey/test_sf_reviewer_proposal_check.py docs/checks/system-first-stage1a/context-v2/reviewer-proposal-check.json docs/checks/2026-07-19-sf-audit-immutability-check.json
git commit -m "docs(research): submit stage1b reviewer proposal"
```

Immediately rerun immutability against committed Git blobs. If any pinned blob differs, add a new later corrective audit event; never amend a committed audit artifact.

After that committed check succeeds, use `apply_patch` to delete the original untracked primary-worktree
copy at `wiki/2026-07-20-reviewer-proposal-and-master-release-design-stage1a-doctoral-review.md`.
Before deletion, prove its SHA-256 equals the registered round-13 bytes. After deletion, prove the
round-13 file remains tracked and hash-identical. This cleanup is safe because the exact review is now
recoverable from the immutable Git blob and removes the root-level duplicate from the AI browsing surface.

---

### Task 8: Publish context-v2 and honest current state

**Files:**

- Modify: `scripts/checks/build_ai_context_manifest.py`
- Modify: `scripts/checks/test_ai_context_surface.py`
- Modify: `scripts/survey/sf_current_manifest.py`
- Modify: `scripts/survey/sf_current_package_check.py`
- Modify: related current-layer/package/consumer tests.
- Modify: `wiki/survey/current/manifest.json`, `README.md`, `status.md`, `wiki/Research-Objective.md`
- Create: `docs/checks/system-first-stage1a/context-v2/current-package-check.json`

- [ ] **Step 1: Add red routing/version tests**

Require:

```python
self.assertEqual(
    "wiki/audit/system-first-stage1a/round-14/research-proposal-and-stage1b-signoff-request.md",
    manifest.ACTIVE_REVIEW_TRANSACTION,
)
self.assertEqual(
    "docs/checks/system-first-stage1a/context-v2/current-package-check.json",
    manifest.CURRENT_PACKAGE_REPORT,
)
```

Require evidence-v7, the corpus bridge, reviewer bibliography, proposal source manifest, proposal check, and round-14 proposal in the release graph. Require context-v1 incident as historical evidence, but do not mutate it. Assert the AI default load surface remains exactly AGENTS/CLAUDE → Research-Objective → Project-Thesis.

- [ ] **Step 2: Update builders and mutable current manifests**

Point active review to round 14 and current package to context-v2. Add all new CURRENT/gate sources with unique roles. Remove evidence-v6 from active release bindings while retaining it as cold historical evidence. Keep legacy census/seed/claim/bibliography assets outside the default AI load; only `existing-corpus-disposition-v1.json` bridges them.

- [ ] **Step 3: Write the state once, without amendment prose**

`Research-Objective.md` and `current/status.md` must state:

```text
The three locally verifiable remediation gates are closed and the round-14 proposal is submitted for independent review. Both requested reviewer judgments remain pending. Stage-1B is unstarted and unauthorized; the first systematic query remains forbidden until independent search-design SIGN and separate owner authorization of the exact execution package.
```

Do not say the scientific rationale is adequate, the search design is signed, or Stage-1B is ready to execute.

- [ ] **Step 4: Generate context-v2 and run focused tests**

```powershell
python -m unittest scripts.survey.test_sf_current_layer scripts.survey.test_sf_current_package_check scripts.survey.test_sf_manifest_consumers scripts.checks.test_ai_context_surface -v
python scripts/checks/build_ai_context_manifest.py --write
python scripts/survey/sf_current_manifest.py --write
python scripts/survey/sf_current_package_check.py --write
python scripts/survey/sf_current_package_check.py --check
python scripts/checks/ai_context_surface_check.py --check
```

Expected: current package `PASS`, AI context surface `PASS`, default context count exactly 3, no active amendment chain.

- [ ] **Step 5: Check budgets and commit current state**

```powershell
python -c "from pathlib import Path; p=Path('wiki/Research-Objective.md'); print(len(p.read_bytes()))"
python -c "from pathlib import Path; p=Path('wiki/survey/current/status.md'); print(len(p.read_text(encoding='utf-8').splitlines()))"
git diff --check
```

Expected: Research-Objective ≤5120 bytes; status ≤16 lines.

```powershell
git add scripts/checks scripts/survey wiki/survey/current wiki/Research-Objective.md docs/checks/system-first-stage1a/context-v2
git commit -m "docs(research): publish stage1a review package state"
```

---

### Task 9: Perform adversarial release verification

**Files:**

- Verify all modified and generated files; do not change audit artifacts.

- [ ] **Step 1: Use the required verification skill and inspect the full diff**

Invoke `superpowers:verification-before-completion`, then run:

```powershell
git diff 2f16b23..HEAD --stat
git diff 2f16b23..HEAD -- . ':(exclude)wiki/audit/system-first-stage1a/round-13/reviewer-proposal-design-stage1a-doctoral-review.md'
git diff --check
```

Check for duplicated numeric canon, actual reviewer verdicts in the proposal, stale context-v1 active references, and any mutation outside the approved scope.

- [ ] **Step 2: Run all focused Windows checks fresh**

```powershell
python -m unittest discover -s scripts/survey -p 'test_sf_*.py' -v
python -m unittest scripts.checks.test_ai_context_surface -v
python scripts/survey/sf_absence_provenance_migrate.py --check
python scripts/survey/sf_identity_taxonomy_v7_test.py --output docs/checks/system-first-stage1a/evidence-v7/identity-taxonomy-v7-test.nt.json
python scripts/survey/sf_existing_corpus_disposition.py --check
python scripts/survey/sf_bibliography_generator.py --check --output wiki/survey/current/bibliography.md
python scripts/survey/sf_reviewer_proposal_check.py --check
python scripts/survey/sf_campaign_audit_index.py --check
python scripts/survey/sf_audit_immutability_check.py --check
python scripts/survey/sf_current_package_check.py --check
python scripts/checks/ai_context_surface_check.py --check
```

Expected: zero failures and every release verdict `PASS`.

- [ ] **Step 3: Run the same headline gates in WSL2**

```powershell
wsl -d Ubuntu-24.04 bash -lc "source ~/.venvs/speechrl/bin/activate && cd /mnt/d/chao_workspace/exploring-l4-intelligence/.worktrees/stage1b-readiness-remediation && python -m unittest discover -s scripts/survey -p 'test_sf_*.py' && python -m unittest scripts.checks.test_ai_context_surface && python scripts/survey/sf_identity_taxonomy_v7_test.py --output docs/checks/system-first-stage1a/evidence-v7/identity-taxonomy-v7-test.posix.json && python scripts/survey/sf_current_package_check.py --check && python scripts/survey/sf_audit_immutability_check.py --check && python scripts/checks/ai_context_surface_check.py --check"
```

Expected: zero failures/skips relevant to contract behavior; evidence occupancy identical to Windows.

- [ ] **Step 4: Prove the execution boundary**

```powershell
git diff 2f16b23..HEAD -- wiki/survey/2026-07-15-sf-queries.jsonl docs/integrity/experiment_attempt_registry.jsonl
git log --all --oneline -- wiki/audit/system-first-stage1a/round-15/research-proposal-independent-doctoral-review.md
rg -n "Stage-1B.*(authorized|started)|OWNER_AUTHORIZED_STAGE1B.*(true|complete)|REQUESTED_SEARCH_DESIGN_SIGNOFF\s*=\s*SIGN$" wiki/Research-Objective.md wiki/survey/current/status.md wiki/audit/system-first-stage1a/round-14/research-proposal-and-stage1b-signoff-request.md
```

Expected: all commands have no output except explicitly negated/pending statements inspected manually.

- [ ] **Step 5: Run one hostile self-review round to zero new findings**

Review G1, G2, G3, authority separation, audit immutability, context routing, legacy corpus orphans, P1 metadata, P2 nonblocking status, query immutability, and Windows/WSL parity. If any finding appears, fix it with a failing test and repeat until one full pass yields zero new findings.

---

### Task 10: Repair Git worktree metadata, merge, verify, and push `master`

**Files:**

- Git metadata and branch history only; no GitHub Wiki publication.

- [ ] **Step 1: Record and remove the erroneous shared `core.worktree`**

Run in WSL2 against the primary repository:

```powershell
wsl -d Ubuntu-24.04 bash -lc "git --git-dir=/mnt/d/chao_workspace/exploring-l4-intelligence/.git config --get core.worktree; git --git-dir=/mnt/d/chao_workspace/exploring-l4-intelligence/.git config --unset core.worktree"
wsl -d Ubuntu-24.04 bash -lc "git -C /mnt/d/chao_workspace/exploring-l4-intelligence rev-parse --show-toplevel && git -C /mnt/d/chao_workspace/exploring-l4-intelligence/.worktrees/stage1b-readiness-remediation rev-parse --show-toplevel"
```

Expected: old value is `/mnt/d/chao_workspace/exploring-l4-intelligence/.worktrees/stage1b-readiness-remediation`; afterward each command reports its own correct root.

- [ ] **Step 2: Prove both worktrees are clean and fetch remote state**

```powershell
wsl -d Ubuntu-24.04 bash -lc "git -C /mnt/d/chao_workspace/exploring-l4-intelligence status --short && git -C /mnt/d/chao_workspace/exploring-l4-intelligence/.worktrees/stage1b-readiness-remediation status --short && git -C /mnt/d/chao_workspace/exploring-l4-intelligence fetch origin --prune && git -C /mnt/d/chao_workspace/exploring-l4-intelligence symbolic-ref refs/remotes/origin/HEAD && git -C /mnt/d/chao_workspace/exploring-l4-intelligence rev-parse origin/master && git -C /mnt/d/chao_workspace/exploring-l4-intelligence/.worktrees/stage1b-readiness-remediation rev-parse HEAD"
```

Expected: both status outputs empty; default remote is `origin/master`. Stop on relevant remote divergence.

- [ ] **Step 3: Merge with a normal merge commit**

```powershell
wsl -d Ubuntu-24.04 bash -lc "git -C /mnt/d/chao_workspace/exploring-l4-intelligence switch master && git -C /mnt/d/chao_workspace/exploring-l4-intelligence merge --no-ff codex/stage1b-readiness-remediation -m 'merge: stage1a reviewer proposal readiness'"
```

No force, reset, rebase, or audit-artifact rewrite is allowed.

- [ ] **Step 4: Re-run headline gates on the merged tree**

```powershell
wsl -d Ubuntu-24.04 bash -lc "source ~/.venvs/speechrl/bin/activate && cd /mnt/d/chao_workspace/exploring-l4-intelligence && python scripts/survey/sf_current_package_check.py --check && python scripts/survey/sf_audit_immutability_check.py --check && python scripts/checks/ai_context_surface_check.py --check && git diff --check && git status --short"
```

Expected: all PASS and clean status.

- [ ] **Step 5: Push and prove remote readback**

```powershell
wsl -d Ubuntu-24.04 bash -lc "git -C /mnt/d/chao_workspace/exploring-l4-intelligence push origin master && local_head=$(git -C /mnt/d/chao_workspace/exploring-l4-intelligence rev-parse master) && remote_head=$(git -C /mnt/d/chao_workspace/exploring-l4-intelligence ls-remote origin refs/heads/master | cut -f1) && test \"$local_head\" = \"$remote_head\" && printf '%s\n' \"$local_head\""
```

Expected: non-force push succeeds and remote `master` exactly equals the local merge commit.

- [ ] **Step 6: Report the bounded outcome**

Report the proposal path, merge commit, remote branch, verification results, and state `SUBMITTED_FOR_INDEPENDENT_REVIEW`. Explicitly state that no Stage-1B query/model/smoke execution occurred, the requested reviewer verdicts remain pending, owner authorization remains pending, and GitHub Wiki was not published.

---

## Mandatory stop conditions

Stop without merge/push if any of these is true:

- positive absence evidence can still reach derivation;
- any of the 22 changed row hashes lacks independent `AGREE` adjudication;
- the corpus bridge has an unexplained orphan or silently merged identity;
- any author placeholder remains in reviewer-visible bibliography;
- proposal checker finds an actual verdict, unsupported contribution claim, or missing source binding;
- audit registry, campaign index, current manifest, or AI manifest is inconsistent;
- frozen queries or experiment attempts changed;
- Windows/WSL headline results disagree;
- the primary or feature worktree is dirty at merge time;
- remote `master` has relevant unexpected divergence;
- any command would require force push, audit rewrite, GitHub Wiki publication, or Stage-1B execution.
