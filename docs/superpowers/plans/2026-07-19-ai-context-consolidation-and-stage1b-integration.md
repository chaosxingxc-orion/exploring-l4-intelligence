# AI Context Consolidation and Stage-1B Integration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the amendment-dependent working surface with a small self-contained current layer, cold-route or safely archive the legacy chain, and integrate the schema-v3 evidence repair into an honest Stage-1A re-review package.

**Architecture:** A generated AI-context manifest defines the only default/targeted active surface. Stable files under `wiki/survey/current/` carry effective protocol, state, tables, and machine routing; historical reviewer transactions live behind one campaign audit index. Executable checks enforce budgets, placement, hashes, legacy exceptions, protocol equivalence, archive safety, and release bindings.

**Tech Stack:** Python standard library, JSON/Markdown, `unittest`, Git blob hashes, PowerShell, WSL2 `Ubuntu-24.04`, existing survey checks and wiki sync dry-run.

**Design spec:** `docs/superpowers/specs/2026-07-19-stage1b-readiness-and-context-consolidation-design.md`

**Depends on:** `docs/superpowers/plans/2026-07-19-stage1b-evidence-contract-remediation.md` through its Plan-A checkpoint.

---

## File map

**Create**

- `scripts/checks/ai_context_surface_check.py` — pure context-budget, routing, placement, and hot-link oracle.
- `scripts/checks/build_ai_context_manifest.py` — deterministic active-entry and legacy-cold inventory builder.
- `scripts/checks/test_ai_context_surface.py` — negative fixtures for context and placement failures.
- `scripts/survey/test_sf_query_compiler_profiles.py` — protocol-v1/v2 equivalence regression.
- `scripts/survey/sf_current_manifest.py` — deterministic current survey asset manifest.
- `scripts/survey/sf_current_tables.py` — generated opening/headline table from the v6 report.
- `scripts/survey/sf_archive_candidates.py` — registry/reference/hash safety oracle for archival moves.
- `scripts/survey/sf_current_package_check.py` — non-network integration runner and persisted report.
- `docs/integrity/ai-context-manifest.json` — generated AI load surface and legacy exceptions.
- `wiki/survey/current/README.md` — current survey router.
- `wiki/survey/current/protocol.md` — self-contained effective protocol v2.
- `wiki/survey/current/status.md` — short Stage-1A state and next action.
- `wiki/survey/current/manifest.json` — active survey machine assets and hashes.
- `wiki/survey/current/tables/opening-guarantees.md` — generated reader-facing table.
- `wiki/audit/system-first-stage1a/INDEX.md` — campaign-level cold audit index.
- `wiki/audit/system-first-stage1a/round-12/stage1a-readiness-correction.md` — immutable correction and re-review request.
- `wiki/archive/working/system-first-stage1a/INDEX.md` — physical-move record for eligible legacy working files.
- `docs/checks/system-first-stage1a/context-v1/current-package-check.json` — integrated local verdict.

**Modify**

- `scripts/survey/sf_query_compiler.py` — explicit protocol/output/check paths.
- `scripts/survey/sf_release_binding_check.py` — current-manifest-driven active release list.
- `scripts/survey/sf_quantifier_scan.py` — current-manifest-driven prose surface.
- `AGENTS.md`, `CLAUDE.md` — concise routing and placement pointer, kept mirrored.
- `wiki/AI-Collaboration.md` — durable document placement, lifecycle, and consolidation policy.
- `wiki/Research-Objective.md` — compact current Stage-1A truth.
- `wiki/Per-Work-Status.md` — compact current per-work state.
- `wiki/survey/README.md` — routing-only survey entry.
- `wiki/Decision-Log.md` — one append-only ADR after all claims are evidenced.
- `wiki/survey/sf-audit-artifact-registry.json` — append the committed round-12 correction blob.
- `CONTRIBUTING.md` — route new documentation to current/audit/archive/workbench locations.

**Leave at legacy paths**

- All 77 paths already pinned by `sf-audit-artifact-registry.json`.
- Protocol v1, amendments 1 and 3-8, old opening tables, the v5 evidence chain, and the old bundle manifest when registered audit artifacts or legacy replay tools still refer to their paths.
- The above remain cold and absent from the AI active-entry list; path retention is not active status.

---

### Task 1: Add failing context-surface and placement tests

**Files:**

- Create: `scripts/checks/test_ai_context_surface.py`
- Create later: `scripts/checks/ai_context_surface_check.py`

- [ ] **Step 1: Create repository-fixture tests**

Use `tempfile.TemporaryDirectory` and import these future public functions:

```python
from ai_context_surface_check import classify_path, evaluate_manifest
```

The fixture manifest contains:

```python
def manifest(active, budgets=None, legacy=None, active_review=None):
    return {
        "schema": "ai-context-manifest-v1",
        "active_entries": active,
        "budgets_bytes": budgets or {},
        "legacy_cold_paths": legacy or [],
        "active_review_transaction": active_review,
    }
```

Add these exact tests and failure substrings:

```text
one HOT file within budget -> no failures
31 active entries -> active-entry-budget-exceeded
an ARCHIVE path in active_entries -> cold-path-on-active-surface
an oversized file -> file-budget-exceeded
a HOT markdown link to wiki/audit/campaign/round-1/review.md -> direct-audit-round-link
a HOT link to wiki/audit/campaign/INDEX.md -> passes
a review-named file outside wiki/audit and outside legacy_cold_paths -> new-audit-artifact-outside-audit-root
a review-named file listed in legacy_cold_paths -> passes as AUDIT_LEGACY
a fourth new amendment outside the frozen legacy list -> unconsolidated-amendment-forbidden
a missing active path -> active-path-missing
a hash mismatch -> active-hash-mismatch
```

Use SHA-256 of raw bytes in every passing active entry. The fixture scans only files explicitly
passed through `tracked_paths`, so the unit test never invokes Git.

- [ ] **Step 2: Run the red test**

```powershell
python scripts/checks/test_ai_context_surface.py
```

Expected: non-zero exit with `ModuleNotFoundError: No module named 'ai_context_surface_check'`.

- [ ] **Step 3: Commit the red test**

```powershell
git add scripts/checks/test_ai_context_surface.py
git commit -m "test(docs): specify AI context routing failures"
```

---

### Task 2: Implement the context oracle and deterministic manifest builder

**Files:**

- Create: `scripts/checks/ai_context_surface_check.py`
- Create: `scripts/checks/build_ai_context_manifest.py`
- Test: `scripts/checks/test_ai_context_surface.py`

- [ ] **Step 1: Implement pure classification and evaluation**

Expose:

```python
def classify_path(path, legacy_cold_paths): ...
def evaluate_manifest(repo, manifest, tracked_paths): ...
def normalize_agent_guide(text): ...
```

Use this precedence:

```text
exact stable hot files -> HOT
wiki/survey/current/** -> CURRENT
wiki/survey/registry/** or wiki/survey/sidecars/** -> REGISTRY
wiki/audit/** -> AUDIT
wiki/archive/** -> ARCHIVE
wiki/survey/workbench/** -> WORKBENCH
explicit legacy_cold_paths -> AUDIT_LEGACY or REGISTRY_LEGACY as declared
everything else -> UNCLASSIFIED
```

`evaluate_manifest` must emit the Task-1 failure codes, enforce `len(active_entries) <= 30`, verify
raw-byte hashes and configured byte budgets, ensure no active entry class is audit/archive/workbench,
and scan HOT/CURRENT Markdown for direct round-level audit links. Allow only the campaign `INDEX.md`
or the one exact `active_review_transaction` declared in the manifest.

Normalize `AGENTS.md` and `CLAUDE.md` by replacing only these three client-specific lines before
byte comparison: the H1 filename, the one-sentence client description, and the Research-skills
marketplace line. Any other difference emits `agent-guides-not-mirrored`.

- [ ] **Step 2: Implement the builder**

`build_ai_context_manifest.py` accepts `--write` and `--check`. It owns a constant list with no more
than 30 entries. Each entry has `path`, `class`, `load_policy` (`default` or `targeted`), `purpose`,
and `sha256`. The default set is exactly:

```text
AGENTS.md (or CLAUDE.md, client-select-one)
wiki/Research-Objective.md
wiki/Project-Thesis.md
```

Targeted entries include Per-Work status, the current survey router/protocol/status/manifest, v6
taxonomy/coding/adjudication, the frozen query file, current opening table, v6 reports, campaign
audit index, and the manifest itself only as metadata without a self-hash. Do not list an individual
legacy review, response, proposal, or amendment as active.

Populate `legacy_cold_paths` deterministically from:

1. all 77 registered paths and their `AUDIT_LEGACY` class;
2. the exact retained protocol/amendment/opening-table/v5-replay paths declared in a constant; and
3. no wildcard that could silently grandfather a future review file.

Set these budgets:

```json
{
  "AGENTS.md": 12288,
  "CLAUDE.md": 12288,
  "wiki/Research-Objective.md": 5120,
  "wiki/Per-Work-Status.md": 8192,
  "wiki/survey/README.md": 4096,
  "wiki/survey/current/README.md": 4096
}
```

Builder output is deterministic: no wall-clock timestamp, absolute path, or platform separator.

- [ ] **Step 3: Run unit tests**

```powershell
python scripts/checks/test_ai_context_surface.py
```

Expected: all tests `OK`.

- [ ] **Step 4: Commit the oracle before applying it to the repository**

```powershell
git add scripts/checks/ai_context_surface_check.py scripts/checks/build_ai_context_manifest.py scripts/checks/test_ai_context_surface.py
git commit -m "feat(docs): enforce AI context surface policy"
```

---

### Task 3: Consolidate protocol v2 and prove query equivalence

**Files:**

- Create: `wiki/survey/current/protocol.md`
- Modify: `scripts/survey/sf_query_compiler.py`
- Create: `scripts/survey/test_sf_query_compiler_profiles.py`
- Compare: `wiki/survey/2026-07-15-system-first-survey-protocol-v1.md`
- Compare: `wiki/survey/2026-07-15-sf-queries.jsonl`

- [ ] **Step 1: Write one self-contained effective protocol**

Start with this exact frontmatter:

```yaml
---
protocol_id: SF-SYSTEM-FIRST-STAGE1B
protocol_version: 2
effective_date: 2026-07-19
stage: Stage-1A survey-ready gate
execution_authorized: false
supersedes_effective_chain: protocol-v1 plus amendments 1 and 3-15
audit_index: wiki/audit/system-first-stage1a/INDEX.md
---
```

The body must be interpretable without any amendment. Use this fixed section map:

```text
§0 authority, current gate, no model/smoke and no discovery-query execution
§1 research questions and scope
§2 unit of analysis, method-path identity, I1-I4/UMBRELLA rules
§3 sources, dates, coverage lanes, and access logging
§4 exact compiled query declarations
§5 deduplication, screening, conflicts, and stopping
§6 coding schema, signal/edge identity, information boundary
§7 schema-v3 evidence/adjudication contract and strong PDF anchors
§8 systematic-mapping execution procedure and exposure accounting
§9 outputs, denominators, occupancy, negative results, and release binding
§10 document lifecycle, correction, re-review, and sign-off authority
Appendix A: one disposition row for each amendment 1 and 3-15 -> carrying v2 section
```

Copy the complete existing `## §4` query block byte-for-byte into v2. Fold every surviving rule from
amendments 1 and 3-15 into the applicable section; do not append the amendments or reproduce their
chronology in prose. Appendix A is an audit routing table, not a dependency: each row names the v2
section that is sufficient by itself.

- [ ] **Step 2: Parameterize the compiler without altering assembly semantics**

Add `argparse` options:

```text
--protocol PATH   default wiki/survey/current/protocol.md
--out PATH        default wiki/survey/2026-07-15-sf-queries.jsonl
--check-against PATH
--check           compile in memory and compare, never write
```

Change `load_protocol_text()` to accept a `Path`; pass paths through `main(argv=None)`. Do not change
`ADDITIONS`, `ADDITION_LANES`, category maps, record ordering, JSON formatting, or record hashes.
For `--check`, require `--check-against` and emit a non-zero exit on any byte difference.

- [ ] **Step 3: Add legacy/current equivalence tests**

The new test imports the compiler, compiles both protocol paths in memory, renders them with the same
newline/JSON function, and asserts:

```text
legacy protocol -> exactly 65 rows
current protocol -> exactly 65 rows
legacy bytes == current bytes
current bytes == raw bytes of wiki/survey/2026-07-15-sf-queries.jsonl
all 65 record_sha256 values recompute
```

Add a negative fixture that changes one §4 term and assert the byte comparison fails.

- [ ] **Step 4: Run the regression and check-only CLI**

```powershell
python scripts/survey/test_sf_query_compiler_profiles.py
python scripts/survey/sf_query_compiler.py --check --check-against wiki/survey/2026-07-15-sf-queries.jsonl
git diff --exit-code -- wiki/survey/2026-07-15-sf-queries.jsonl
```

Expected: tests `OK`, compiler `PASS (65 byte-identical records)`, and no frozen-query diff.

- [ ] **Step 5: Commit protocol consolidation**

```powershell
git add wiki/survey/current/protocol.md scripts/survey/sf_query_compiler.py scripts/survey/test_sf_query_compiler_profiles.py
git commit -m "docs(survey): consolidate effective protocol v2"
```

---

### Task 4: Build the current survey router, state, tables, and manifest

**Files:**

- Create: `wiki/survey/current/README.md`
- Create: `wiki/survey/current/status.md`
- Create: `wiki/survey/current/tables/opening-guarantees.md`
- Create: `wiki/survey/current/manifest.json`
- Create: `scripts/survey/sf_current_tables.py`
- Create: `scripts/survey/sf_current_manifest.py`

- [ ] **Step 1: Generate the opening table from the v6 report**

`sf_current_tables.py` reads
`docs/checks/system-first-stage1a/evidence-v6/identity-taxonomy-v6-test.json` and writes/checks
`wiki/survey/current/tables/opening-guarantees.md`. Reuse `render_headline` from
`sf_release_binding_check.py` and add a machine comment binding to the report path and SHA-256. CLI:

```text
--write  write deterministic Markdown
--check  compare expected bytes to disk
```

The document states Stage-1A evidence grade, exact method-path and unique-work denominators, no
Stage-1B execution, and no readiness/signature claim.

- [ ] **Step 2: Implement the active survey manifest**

`sf_current_manifest.py` owns role/path entries for:

```text
protocol v2
frozen 65-query JSONL
seed manifest
canon registry
fulltext ledger
schema-v3 sidecar directory (expanded to eight file entries)
identity taxonomy v6
known-item coding v7
schema-v3 adjudication
Windows/WSL v6 reports
dual-platform aggregate
current opening table
current status
campaign audit index
```

Each file entry contains `role`, `path`, `sha256`, `mutability`, and `load_policy`. The manifest also
contains arrays `release_bound_artifacts` and `prose_scan_paths`; both arrays list current artifacts,
never individual legacy amendments. The manifest does not hash itself. CLI is `--write`/`--check`,
with deterministic ordering and no timestamps.

- [ ] **Step 3: Write the two routing pages**

`current/README.md` contains only: current gate, three-file reading order (`status`, `protocol`,
`manifest`), targeted data instructions, audit-index pointer, and the rule that legacy files are not
default context. `current/status.md` contains only: Stage-1A, unresolved owner/reviewer sign-off,
zero Stage-1B executions in this repair, Plan-A v6 verdict pointer, current blockers, and next action.

- [ ] **Step 4: Generate and verify**

```powershell
python scripts/survey/sf_current_tables.py --write
python scripts/survey/sf_current_tables.py --check
python scripts/survey/sf_current_manifest.py --write
python scripts/survey/sf_current_manifest.py --check
git diff --check
```

- [ ] **Step 5: Commit the current layer**

```powershell
git add scripts/survey/sf_current_tables.py scripts/survey/sf_current_manifest.py wiki/survey/current
git commit -m "feat(survey): establish manifest-driven current layer"
```

---

### Task 5: Make prose and release checks consume the current manifest

**Files:**

- Modify: `scripts/survey/sf_release_binding_check.py`
- Modify: `scripts/survey/sf_quantifier_scan.py`
- Modify: `wiki/survey/current/manifest.json` through its generator

- [ ] **Step 1: Replace the hard-coded active lists**

In both tools add `--manifest`, defaulting to `wiki/survey/current/manifest.json`.
`sf_release_binding_check.py` reads `release_bound_artifacts`; `sf_quantifier_scan.py` reads
`prose_scan_paths`. Explicit positional files remain supported by the quantifier scanner for focused
diagnostics. Missing manifest paths fail; never print `[skip]` and return green.

Keep the historical release-bound list only under a `--legacy-regression` option. The default current
run must include the round-12 correction after Task 8 and must not include amendment 15 or opening
tables v4.

- [ ] **Step 2: Add manifest-negative fixtures**

Extend the tools' existing self-tests so that:

```text
missing active artifact -> failure
hand-edited generated headline -> failure
stale occupancy value -> failure
manifest that points to an archive path -> failure
```

- [ ] **Step 3: Run legacy regression before switching the current list**

```powershell
python scripts/survey/sf_release_binding_check.py --legacy-regression
python scripts/survey/sf_quantifier_scan.py wiki/2026-07-19-system-first-research-proposal-v10-consolidated.md wiki/survey/2026-07-19-gate-s1-v9-response.md
```

Expected: both exit zero.

- [ ] **Step 4: Commit manifest-driven checks**

```powershell
git add scripts/survey/sf_release_binding_check.py scripts/survey/sf_quantifier_scan.py scripts/survey/sf_current_manifest.py
git commit -m "refactor(survey): route active prose checks through manifest"
```

---

### Task 6: Physically archive only safe legacy working files

**Files:**

- Create: `scripts/survey/sf_archive_candidates.py`
- Create: `wiki/archive/working/system-first-stage1a/INDEX.md`
- Move: amendments 9-15 listed below.

- [ ] **Step 1: Implement the archive safety oracle**

The tool accepts `--write-plan`, `--check-plan`, and `--check-applied`. The plan contains exact source,
destination, and pre-move `git hash-object` for each file. Before a move it fails if a source:

```text
is in sf-audit-artifact-registry.json
is in wiki/survey/current/manifest.json
has an inbound reference from a HOT/CURRENT file
has an inbound reference from a registered audit artifact
is missing or already dirty
```

After a move it requires source absence, destination presence, identical blob hash, and no active old
path reference. The oracle scans tracked files with `git grep`; it does not rewrite references.

- [ ] **Step 2: Generate and inspect the exact safe plan**

The only planned sources are:

```text
wiki/survey/2026-07-18-sf-protocol-amendment-9.md
wiki/survey/2026-07-18-sf-protocol-amendment-10.md
wiki/survey/2026-07-18-sf-protocol-amendment-11.md
wiki/survey/2026-07-18-sf-protocol-amendment-12.md
wiki/survey/2026-07-19-sf-protocol-amendment-13.md
wiki/survey/2026-07-19-sf-protocol-amendment-14.md
wiki/survey/2026-07-19-sf-protocol-amendment-15.md
```

Destinations preserve basenames under
`wiki/archive/working/system-first-stage1a/amendments/`. Amendments 1 and 3-8 remain in place because
legacy documents still point to them; the current router classifies them cold.

Run:

```powershell
python scripts/survey/sf_archive_candidates.py --write-plan
python scripts/survey/sf_archive_candidates.py --check-plan
```

Expected: seven safe candidates and zero registry/current/audit inbound blockers. If any candidate is
not safe at execution time, remove it from the physical-move batch and record the exact blocker in
the archive index; never force the move.

- [ ] **Step 3: Move with Git and prove byte preservation**

Create the destination directory, then use one `git mv` per explicit source/destination. Do not edit
the moved bytes. Run:

```powershell
python scripts/survey/sf_archive_candidates.py --check-applied
python scripts/survey/sf_audit_immutability_check.py
git diff --summary
```

Expected: seven renames, identical hashes, and immutability `PASS`.

- [ ] **Step 4: Write the archive index**

For each moved file record source, destination, blob, superseding `current/protocol.md` section, and
move commit intent. Also list the retained cold legacy exceptions and why path movement is unsafe.

- [ ] **Step 5: Commit physical cleanup**

```powershell
git add scripts/survey/sf_archive_candidates.py wiki/archive/working/system-first-stage1a
git commit -m "chore(wiki): archive safe legacy amendments"
```

---

### Task 7: Compact the hot layer and codify future document placement

**Files:**

- Modify: `wiki/AI-Collaboration.md`
- Modify: `AGENTS.md`
- Modify: `CLAUDE.md`
- Modify: `CONTRIBUTING.md`
- Modify: `wiki/Research-Objective.md`
- Modify: `wiki/Per-Work-Status.md`
- Modify: `wiki/survey/README.md`
- Create: `docs/integrity/ai-context-manifest.json`

- [ ] **Step 1: Add the durable placement/lifecycle policy**

In `wiki/AI-Collaboration.md`, add the design's location table and six-step lifecycle as the canonical
policy. It must explicitly cover HOT, CURRENT, REGISTRY, AUDIT, ARCHIVE, WORKBENCH, engineering
specs/plans, check reports, executable rules, and ephemeral scratch. Include these triggers verbatim
in meaning: third amendment, budget exceedance, reviewer major contract change, handoff ambiguity,
stage/release boundary, or competing active claims. State: the third correction is immediately
folded into the effective spec; a fourth is forbidden before consolidation.

Add the concise routing table to `CONTRIBUTING.md`. In `AGENTS.md` and `CLAUDE.md`, keep only the
default-load rule, context budgets, path routing summary, and pointer to `AI-Collaboration.md`; do not
duplicate the full table. Apply the same shared guidance edit to both files.

- [ ] **Step 2: Rewrite hot state in place**

`Research-Objective.md` must contain only:

```text
current Stage-1A gate and explicit no-Stage-1B-approval statement
north-star purpose chain
current E6-E12/anchor remediation result and exact v6 report pointer
remaining independent re-review and owner-signature blockers
exposure accounting: zero discovery queries and zero model/smoke runs in this repair
current survey router and campaign audit index pointers
next authorized action
invalidation conditions
```

`Per-Work-Status.md` retains one short current block per W1-W4 and moves historical narration to
existing archive/index pointers. `wiki/survey/README.md` becomes a routing page to `current/`,
`registry/`, `workbench/`, `audit`, and archive; it contains no live protocol rules or copied numbers.

- [ ] **Step 3: Build and run the real context manifest**

```powershell
python scripts/checks/build_ai_context_manifest.py --write
python scripts/checks/build_ai_context_manifest.py --check
python scripts/checks/ai_context_surface_check.py
```

Expected:

```text
active entries <= 30
AGENTS.md <= 12288 bytes
CLAUDE.md <= 12288 bytes
Research-Objective.md <= 5120 bytes
Per-Work-Status.md <= 8192 bytes
survey README files <= 4096 bytes
0 direct legacy-round links on HOT/CURRENT surface except active_review_transaction
```

- [ ] **Step 4: Commit context consolidation**

```powershell
git add AGENTS.md CLAUDE.md CONTRIBUTING.md wiki/AI-Collaboration.md wiki/Research-Objective.md wiki/Per-Work-Status.md wiki/survey/README.md docs/integrity/ai-context-manifest.json scripts/checks/ai_context_surface_check.py scripts/checks/build_ai_context_manifest.py scripts/checks/test_ai_context_surface.py
git commit -m "docs(wiki): consolidate AI working context"
```

---

### Task 8: Publish the correction into its permanent audit path and register it

**Files:**

- Create: `wiki/audit/system-first-stage1a/INDEX.md`
- Create: `wiki/audit/system-first-stage1a/round-12/stage1a-readiness-correction.md`
- Modify: `wiki/survey/current/status.md`
- Modify: `wiki/survey/current/manifest.json` through `scripts/survey/sf_current_manifest.py`
- Modify: `docs/integrity/ai-context-manifest.json` through `scripts/checks/build_ai_context_manifest.py`
- Modify: `wiki/survey/sf-audit-artifact-registry.json` in a second commit

- [ ] **Step 1: Write the bounded correction**

The correction must contain:

```text
the exact p1 the false-green reproduction
the legitimate-restamp signal-source false-green reproduction
withdrawal of v10's “E1-E5 fully closed” statement
schema-v3 row16/signal4/edge2 and strong-anchor repair
non-implementer adjudication identity and verdict
Windows/WSL v6 report paths and equal occupancy
protocol-v2 query byte-equivalence result
context manifest/budget result and physical archive result
zero discovery queries; zero model/smoke runs; inherited exposure unchanged
request for independent re-review
explicit statement that this is not owner Stage-1B execution approval or signature
```

Include a `release_binding` block sourced from the v6 report and a generated headline block produced
by `sf_current_tables.py`; do not hand-copy the table.

- [ ] **Step 2: Create the append-only campaign index**

Add one row per registered system-first Stage-1A round. Each row gives round id, artifact type,
verdict/disposition, original path, pinned blob, supersession target, and the current protocol section
that carries surviving rules. The current layer links only to this index and the active round-12
transaction.

- [ ] **Step 3: Refresh current manifests and run pre-registration checks**

Pre-stage exactly the new audit pair before either manifest is refreshed. This lets
`git ls-files -s` provide the trusted blob inventory required to activate the pair; it is not
permission to commit a failed check run.

```powershell
git add wiki/audit/system-first-stage1a/INDEX.md wiki/audit/system-first-stage1a/round-12/stage1a-readiness-correction.md
python scripts/survey/sf_current_tables.py --check
python scripts/survey/sf_current_manifest.py --write
python scripts/checks/build_ai_context_manifest.py --write
python scripts/survey/sf_release_binding_check.py
python scripts/survey/sf_quantifier_scan.py
python scripts/checks/ai_context_surface_check.py
```

Expected: all pass; the correction is the only allowed direct active-review transaction. If any
check fails, do not commit: repair the failure, pre-stage the exact audit pair again if its bytes
changed, and rerun the complete Step 3 check sequence.

- [ ] **Step 4: Commit the immutable artifact before registering its blob**

```powershell
git add wiki/survey/current docs/integrity/ai-context-manifest.json
git commit -m "docs(audit): issue stage1a readiness correction"
git rev-parse HEAD:wiki/audit/system-first-stage1a/round-12/stage1a-readiness-correction.md
```

Step 4 stages the remaining generated files; the commit then includes them together with the audit
pair already staged in Step 3. Capture the returned 40-character blob id from Git itself.

- [ ] **Step 5: Append the exact committed blob to the audit registry**

Append one artifact object with the permanent correction path and captured `git_blob`. Do not
register `INDEX.md`, because that index is intentionally append-only across future rounds rather than
immutable after this round.

```powershell
python scripts/survey/sf_audit_immutability_check.py
git add wiki/survey/sf-audit-artifact-registry.json docs/checks/2026-07-19-sf-audit-immutability-check.json
git commit -m "audit(wiki): register round12 correction blob"
```

Expected: registry count 78 and immutability `PASS`.

---

### Task 9: Record the durable decision and update current state

**Files:**

- Modify: `wiki/Decision-Log.md`
- Modify: `wiki/Research-Objective.md`
- Modify: `wiki/Per-Work-Status.md`
- Modify: `wiki/survey/current/status.md`
- Regenerate: both current manifests

- [ ] **Step 1: Re-read the recording contract before durable edits**

Read `wiki/AI-Collaboration.md` completely, then append one Decision-Log ADR with exactly these
headings:

```text
Context
Decision
Rationale
Consequences
Purpose chain
Provenance
Invalidation conditions
Supersedes
```

The decision records protocol-v2 consolidation, future permanent audit placement, third-amendment
trigger, the seven physically archived safe amendments, retained path-pinned exceptions, and
schema-v3 readiness evidence. Do not paste the correction or implementation chronology.

- [ ] **Step 2: Update the hot state with the committed correction**

Keep `Research-Objective` and `Per-Work-Status` within Task-7 budgets. State the actual machine
verdicts and that Stage-1A remains awaiting independent re-review/owner signature. Do not say Stage-1B
has started or is owner-approved.

- [ ] **Step 3: Regenerate manifests and verify hashes**

```powershell
python scripts/survey/sf_current_manifest.py --write
python scripts/checks/build_ai_context_manifest.py --write
python scripts/survey/sf_current_manifest.py --check
python scripts/checks/build_ai_context_manifest.py --check
python scripts/checks/ai_context_surface_check.py
```

- [ ] **Step 4: Commit durable state**

```powershell
git add wiki/Decision-Log.md wiki/Research-Objective.md wiki/Per-Work-Status.md wiki/survey/current docs/integrity/ai-context-manifest.json
git commit -m "docs(research): record consolidated stage1a state"
```

---

### Task 10: Add and run the integrated current-package gate

**Files:**

- Create: `scripts/survey/sf_current_package_check.py`
- Create: `docs/checks/system-first-stage1a/context-v1/current-package-check.json`

- [ ] **Step 1: Implement a fail-closed subprocess runner**

Run these commands in order, capture exit code/stdout tail, and persist one JSON row per command:

```text
python scripts/survey/test_sf_evidence_contract.py
python scripts/survey/sf_schema_v3_migrate.py --check
python scripts/survey/sf_coding_generator.py --check
python scripts/survey/sf_identity_taxonomy_v6_test.py
python scripts/survey/sf_dual_platform_check.py
python scripts/survey/test_sf_query_compiler_profiles.py
python scripts/survey/sf_query_compiler.py --check --check-against wiki/survey/2026-07-15-sf-queries.jsonl
python scripts/survey/sf_current_tables.py --check
python scripts/survey/sf_current_manifest.py --check
python scripts/survey/sf_release_binding_check.py
python scripts/survey/sf_quantifier_scan.py
python scripts/survey/sf_archive_candidates.py --check-applied
python scripts/survey/sf_audit_immutability_check.py
python scripts/checks/build_ai_context_manifest.py --check
python scripts/checks/ai_context_surface_check.py
```

The overall verdict is `PASS` only if every exit code is zero. Add a self-test that substitutes one
non-zero fixture command and proves the aggregator returns `FAIL`.

- [ ] **Step 2: Run Windows integration**

```powershell
python scripts/survey/sf_current_package_check.py
```

Expected: `current package: PASS`.

- [ ] **Step 3: Re-run canonical WSL checks**

```powershell
wsl -d Ubuntu-24.04 bash -lc "source ~/.venvs/speechrl/bin/activate && cd /mnt/d/chao_workspace/exploring-l4-intelligence && python scripts/survey/test_sf_evidence_contract.py && python scripts/survey/test_sf_query_compiler_profiles.py && python scripts/checks/ai_context_surface_check.py"
```

Expected: all pass under Python 3.12.x.

- [ ] **Step 4: Run publication simulation without pushing**

```powershell
wsl -d Ubuntu-24.04 bash -lc "cd /mnt/d/chao_workspace/exploring-l4-intelligence && bash scripts/wiki-sync.sh --dry-run"
```

Expected: wiki mirror diff is shown and the script ends with `[dry-run] not committing or pushing.`
Do not run publishing mode without separate user authorization.

- [ ] **Step 5: Commit the integration report**

```powershell
git add scripts/survey/sf_current_package_check.py docs/checks/system-first-stage1a/context-v1
git commit -m "test(survey): gate consolidated stage1a package"
```

---

### Task 11: Final no-execution and cleanliness verification

**Files:**

- Verify the complete Plan-A + Plan-B delivery.

- [ ] **Step 1: Invoke verification-before-completion**

Read and follow `superpowers:verification-before-completion` before making any completion or readiness
claim. Re-run every command whose output supports the final claim; do not rely on earlier logs.

- [ ] **Step 2: Prove the research execution boundary was untouched**

```powershell
git diff 4af9052..HEAD -- docs/integrity/experiment_attempt_registry.jsonl wiki/survey/2026-07-15-sf-queries.jsonl
```

Expected: no diff. Also inspect `git diff --name-status 4af9052..HEAD` and confirm no dataset fetch,
discovery output, model rollout, smoke result, or work-repo code change exists.

- [ ] **Step 3: Re-run the headline gates from a clean tree**

```powershell
python scripts/survey/sf_current_package_check.py
python scripts/survey/sf_audit_immutability_check.py
python scripts/checks/ai_context_surface_check.py
git diff --check
git status --short
```

Expected: all checks pass and the tree is clean after committing any freshly regenerated reports.

- [ ] **Step 4: State the bounded outcome accurately**

The handoff may say the package is technically repaired for independent Stage-1A re-review and that
the active context is consolidated. It must also say Stage-1B has not begun and still requires the
independent verdict/owner authorization defined by the protocol.
