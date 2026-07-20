# Stage-1B Readiness and AI Context Consolidation Design

**Date:** 2026-07-19
**Status:** Approved for planning
**Scope:** Stage-1A remediation only; no Stage-1B execution authority

## 1. Problem statement

The current branch already contains the round-11 response to the v9 doctoral review and a v10
sign-off application. A fresh read-only audit found that two of v10's closure claims still exceed
the implementation:

1. the locator validator accepts the reviewer's exact weak-anchor counterexample `p1 the`; and
2. a load-bearing signal's `source` can change from `learned_rm_prm` to `llm_judge`, receive a
   legitimate new adjudication row hash, and still pass both `validate()` and `reconcile()`.

The same audit confirmed that the evidence contract does not explicitly bind the remaining fields
named in review section 4.1: edge `signal_use`, edge `decision_right`, `selection_object`, and
`explicit_candidate_pool_selection`.

The documentation architecture also makes current truth expensive to recover. The effective survey
protocol is a 51.9 KB base document plus fourteen amendment files. `Research-Objective.md` is 17.8 KB
against its 5 KB trial budget, `Per-Work-Status.md` is 29 KB, and `wiki/survey/README.md` is 26 KB.
Seventy-seven dated audit artifacts are byte-and-path pinned by the immutability registry. They are
valuable as evidence, but they must not remain part of the AI's routine working context.

This design closes both problems together: finish the narrow evidence-contract repair, then distill
the active protocol and context surface without deleting or rewriting audit evidence.

## 2. Goals

1. Make every review-named load-bearing signal, edge, and selection field explicitly evidence-bound.
2. Reject bare, generic, or overly frequent PDF page anchors, including `p1` and `p1 the`.
3. Validate a new method-path row without relying on any expectation keyed to the existing eleven
   rows.
4. Preserve the existing derivation semantics and headline occupancy unless the corrected evidence
   itself requires a scientific recoding.
5. Replace the amendment chain with one self-contained effective protocol v2.
6. Give future AIs a small, machine-checked current-context manifest.
7. Keep registered audit artifacts at their pinned paths and bytes while removing them from all
   active-context routing.
8. End in Stage-1A with a truthful, dated correction and a package ready for independent sign-off.

## 3. Non-goals

- No systematic discovery or mapping query.
- No model call, smoke test, dataset experiment, prototype, or Stage-2 activity.
- No owner approval or reviewer signature is inferred from this work.
- No new proposal and no amendment 16.
- No change to the query universe, opening guarantees, research question tree, or frozen derivation
  definitions.
- No physical relocation of the 77 path-pinned audit artifacts. Relocation-capable registry v2 is a
  separate future project.
- No broad rewrite of older research campaigns outside the current Gate-S1 context surface.

### 3.1 Delivery decomposition

The design is delivered as two independently testable work packages plus one integration gate:

1. **Evidence-contract remediation** produces taxonomy v6, schema-v3 sidecars, coding v7, the new
   mutation suite, and dual-platform reports. It must pass before any readiness language is written.
2. **AI-context consolidation** produces protocol v2, the current-context manifest, compact hot
   layers, the cold audit index, and safe moves of unregistered historical files. It consumes the
   final artifact paths from work package 1.
3. **Integration and truthful supersession** binds both packages into the dated correction, durable
   records, release checks, and wiki publication.

A failure in context cleanup cannot be hidden by evidence tests, and a clean directory cannot be
used to claim the scientific gate is repaired. Each package has its own implementation plan and
verification checkpoint.

## 4. Knowledge architecture

### 4.1 Current working surface

The active surface will be rooted at:

- `wiki/Research-Objective.md` — current stage, blockers, next action, and canonical pointers;
- `wiki/Project-Thesis.md` — unchanged north star;
- `wiki/Per-Work-Status.md` — current per-work status only;
- `wiki/survey/current/README.md` — survey-current routing page;
- `wiki/survey/current/protocol.md` — complete effective protocol with `protocol_version: 2`;
- `wiki/survey/current/manifest.json` — current machine assets and hashes; and
- `docs/integrity/ai-context-manifest.json` — the files an AI may load by default.

The protocol v2 is an effective specification, not another response letter. It must be understandable
without reading protocol v1, amendments 1-15, proposals, reviews, or responses.

### 4.2 Cold audit surface

Registered dated artifacts remain at their current paths because the existing immutability oracle
pins both path and blob. A new cold index at
`wiki/audit/system-first-stage1a/INDEX.md` records, per round:

- verdict and disposition;
- supersession target;
- original path;
- pinned blob; and
- the current protocol section that carries the surviving rule.

Current canonical files may link to the cold index as a whole, but may not enumerate or depend on
individual amendments, reviews, or responses. Exact provenance lookups use the index and a targeted
`rg`; full audit documents are never part of default context.

Historical files that are not path-pinned may be moved into the same archive only when all of these
conditions hold:

1. they are absent from the audit registry;
2. they are absent from the current manifest;
3. no active script depends on the old path; and
4. a repository-wide reference check identifies and updates every live link.

Moves use `git mv`; content bytes are not edited merely to add archive banners.

### 4.3 Context budgets and routing rules

The context checker will enforce:

- `AGENTS.md` and `CLAUDE.md`: at most 12 KB each and byte-mirrored in their shared guidance;
- `wiki/Research-Objective.md`: at most 5 KB;
- `wiki/Per-Work-Status.md`: at most 8 KB;
- `wiki/survey/README.md`: at most 4 KB and routing-only;
- `wiki/survey/current/README.md`: at most 4 KB; and
- the AI context manifest: at most 30 active entries.

`AGENTS.md` and `CLAUDE.md` will explicitly prohibit broad loading of `wiki/20*.md`, historical
reviews/responses/amendments, and the full Decision Log. Historical evidence is accessed only through
an exact pointer or targeted search.

## 5. Evidence-contract architecture

### 5.1 Versioned artifacts

Historical round-11 evidence remains unchanged. The repaired chain is versioned as:

- identity taxonomy v6;
- schema-v3 sidecars in `wiki/survey/current/data/schema-v3/sidecars/`;
- generated known-item coding v7;
- the v6 contract test and platform-stamped reports; and
- a new compact dated correction bound to the v6 report.

The derivation functions and occupancy definitions remain semantically identical to taxonomy v5.
Version 6 denotes the stronger evidence contract and locator grammar.

### 5.2 Required evidence

Every load-bearing row must bind these 16 row-level fields:

```text
7 strict bits
+ internal_visibility
+ core_topology
+ core_native_modality
+ control_horizon
+ decision_rights
+ candidate_pool_exists
+ selection_policy
+ selection_object
+ explicit_candidate_pool_selection
= 16
```

Every signal must bind:

```text
form, source, lifecycle, uses
```

Every control edge must bind:

```text
signal_use, decision_right
```

A binding contains the encoded value plus a supported evidence kind (`canon`, `tex`, `pdf_page`, or
`absence`). The same quote may support multiple fields, but each field must name the binding
explicitly. Structural consistency and evidence truth remain separate checks: a structurally valid
edge with an unbound or mismatched value still fails.

### 5.3 Generic validation boundary

The implementation will separate three responsibilities:

1. `validate_structure(row)` checks enums, identities, cross-field constraints, edge relations, and
   duplicate IDs without consulting source files.
2. `validate_bound_values(row)` checks that every required row, signal, and edge field has a binding
   whose declared value equals the encoded value. It is source-independent and therefore testable on
   a synthetic twelfth row.
3. `resolve_evidence(row, source_context)` verifies the bound quote, page, anchor, ledger row, and
   source hash against pinned source material.

`reconcile()` composes all three. Derivation and reporting consume only rows that pass the complete
load-bearing contract and adjudication checks. No invalid edge or unbound field may be silently
discarded to produce a lower occupancy count.

## 6. PDF locator contract

Free page locators use this explicit grammar:

```text
pN anchor='multi-word phrase'
```

After case-folding, Unicode normalization, punctuation removal, and whitespace collapse, an anchor
must satisfy all of the following:

1. at least two lexical tokens;
2. at least twelve alphanumeric characters in total;
3. at least one occurrence in the declared page window N-1 through N+1; and
4. no more than three occurrences in the complete PDF.

The last condition operationalizes the review's "minimum discriminativeness" requirement. A caller
can always choose a longer claim-bearing phrase when a method term is too frequent. `pdf_page`
evidence uses the same normalized anchor policy.

Failure codes distinguish:

- `page-token-without-anchor`;
- `page-anchor-too-weak`;
- `page-anchor-missing`;
- `page-anchor-not-discriminative`;
- `page-out-of-range`; and
- `pdf-unreadable-for-page-check`.

The eight current single-token locators will migrate to claim-bearing phrases verified against the
pinned PDFs. Canonical and TeX quote locators retain their existing exact-quote semantics.

## 7. Data flow

```text
schema-v3 sidecars
  -> deterministic coding generator
  -> coding v7
  -> structure + bound-value + source reconciliation
  -> adjudicated load-bearing rows
  -> unchanged taxonomy derivation
  -> v6 platform report
  -> dual-platform equality aggregator
  -> generated reader-visible headline block
  -> dated correction and current manifest
```

The protocol path follows a separate deterministic flow:

```text
protocol v2
  -> existing query compiler
  -> frozen 65-query output
  -> byte-equality assertion against the pre-consolidation output
```

If protocol consolidation changes compiled query bytes, the migration fails. No semantic query
change is allowed in this task.

## 8. Error handling and fail-closed behavior

- Missing required evidence is a row failure, not a warning.
- Unknown evidence kinds fail.
- A valid adjudication hash never suppresses a structure, binding, or locator failure.
- A row with a failure is excluded from all load-bearing reports, and the overall contract verdict is
  `FAIL`; the tooling must not publish a partial headline as if it were complete.
- Current-context files that reference individual amendments or archived operational files fail the
  context-surface check.
- A missing current-manifest path or hash mismatch fails the package check.
- A registered artifact with HEAD, stage-0, or worktree byte drift continues to fail the
  immutability check. Its default/`--check` mode is strictly zero-write and compares a deterministic
  tracked report; only an explicit registry/anchor transaction may use `--write`, then stage the
  report and prove it with `--check`. The report binds registry/anchor Git mode and blob plus the
  complete registry prefix count/hash, and contains no current-HEAD or self-hash field.
- Any failed gate leaves the canonical stage at Stage-1A and forbids a "ready for sign-off" statement.

## 9. Verification design

### 9.1 New-row counterexamples

All semantic mutations simulate a newly encoded row: the adjudication row hash is legitimately
recomputed, so the expected failure must come from the named contract.

Required negative controls:

1. bare `p1` -> `page-token-without-anchor`;
2. `p1 the` -> `page-anchor-too-weak`;
3. a long but document-frequent phrase -> `page-anchor-not-discriminative`;
4. signal `source` flip -> signal evidence value mismatch;
5. structurally coherent edge `signal_use` flip -> edge evidence value mismatch;
6. structurally coherent edge `decision_right` flip -> edge evidence value mismatch;
7. `selection_object` flip -> row evidence value mismatch;
8. `explicit_candidate_pool_selection` flip -> row evidence value mismatch;
9. deletion of any row/signal/edge binding -> required-evidence failure;
10. hand-edited generated headline -> release-binding failure; and
11. a generic twelfth-row good/bad pair with no per-ID expectation -> good passes, each bad mutation
    is rejected by the generic validators.

Existing E1-E5, A1-A8, K1-K7, independent counterexamples, row-hash mutations, and occupancy checks
remain regression controls.

### 9.2 Platform and package verification

Run the contract in:

- Windows `nt`, Python 3.14; and
- WSL2 `Ubuntu-24.04`, `~/.venvs/speechrl`, Python 3.12.

Persist independent platform snapshots. The aggregator requires both verdicts `PASS` and identical
occupancy blocks. Additional package gates are:

- deterministic sidecar-to-coding byte equality;
- protocol-v2 query output byte equality;
- release generated-block negative fixture;
- audit immutability oracle;
- AI context budget and cold-reference oracle;
- repository link validation;
- archive candidate safety check; and
- `bash scripts/wiki-sync.sh`.

## 10. Documentation and supersession

The task produces one short dated correction, not an amendment or proposal. It must:

1. reproduce the two newly found false-greens;
2. withdraw v10's statement that E1-E5 were fully closed;
3. describe the complete field-binding and anchor repair;
4. point to exact v6 machine outputs;
5. state that protocol v2 consolidates the active amendment chain;
6. report zero discovery queries and zero model/smoke executions; and
7. request independent re-review without claiming signature or owner execution approval.

After implementation, durable records are updated in repository order:

1. append one Decision-Log ADR with context, decision, rationale, consequences, provenance, and
   invalidation conditions;
2. rewrite the Research-Objective hot layer in place;
3. compact Per-Work-Status to current state;
4. refresh the archive index and current manifests;
5. run the archive scan and all checks; and
6. publish through wiki-sync.

## 11. Document placement and lifecycle policy

### 11.1 Placement rules

Every persistent document must have exactly one declared role. A file may not act as both the current
effective specification and the audit history of how that specification evolved.

| Document type | Required location | Mutability | Registration and movement rule |
|---|---|---|---|
| Program north star and hot status | `wiki/Project-Thesis.md`, `wiki/Research-Objective.md`, `wiki/Per-Work-Status.md` | Supersede in place | Never date-version these files. Keep only current truth and archive pointers. |
| Cross-project methodology and collaboration rules | `wiki/Research-Methodology.md`, `wiki/AI-Collaboration.md` | Supersede in place with dated tombstones for changed rules | Do not copy their rules into campaign documents. |
| Current survey router | `wiki/survey/current/README.md` | Supersede in place | Contains only current stage, effective assets, and cold-index pointers. |
| Current effective protocol | `wiki/survey/current/protocol.md` | Supersede in place until a release freeze | Stable filename; `protocol_version` lives in frontmatter. It must be self-contained. |
| Current survey status | `wiki/survey/current/status.md` | Supersede in place | Short operational state only: gate, blockers, execution counts, and next action. |
| Current machine manifest | `wiki/survey/current/manifest.json` | Generated/supersede in place | The sole machine entry to active schemas, queries, ledgers, reports, and hashes. |
| Current opening guarantees and human-readable tables | `wiki/survey/current/tables/` | Generated or supersede in place | One active version per table; old versions do not remain beside the current one. |
| Current survey schemas, coding, query sets, and ledgers | `wiki/survey/current/data/` | Generated or controlled append-only according to schema | Must be enumerated by the current manifest; AI reads them only for a named task. |
| Long-lived paper census and claim registry | `wiki/survey/registry/` | Append-only plus explicit supersession fields | Shared across campaigns; never copied into protocol prose. |
| Reviewer submission, reviewer report, response, correction, or sign-off snapshot | `wiki/audit/<campaign>/<round-id>/` | Immutable from first commit | Create directly at its permanent path, register its blob, and never move or edit it. Active state links to it temporarily; the file itself is always cold. |
| Audit round index | `wiki/audit/<campaign>/INDEX.md` | Append-only | One row per round with verdict, supersession, paths, blobs, and surviving-rule pointer. |
| Superseded working protocol, table, schema, or unregistered intermediate | `wiki/archive/<knowledge-layer>/<campaign>/` | Immutable after archival move | Move with `git mv` only after the current manifest has stopped referencing it and link checks pass. |
| Exploratory survey notes and paper dossiers | `wiki/survey/workbench/<campaign>/` while active | Mutable working knowledge | Distill at campaign close; retained dossiers move to `wiki/archive/survey/<campaign>/`, disposable scratch is not committed. |
| Engineering design specification | `docs/superpowers/specs/` | Versioned through Git review | One design per bounded project; it does not become research canon. |
| Engineering implementation plan | `docs/superpowers/plans/` | Checkboxes may change during execution | Archive by Git history after completion; current research pages link only to delivered artifacts, not plans. |
| Reproducibility and validation report | `docs/checks/<campaign>/<release-id>/` | Immutable after a release references it | Generate directly into a release-scoped directory; never use one last-writer-wins filename for multiple platforms. |
| Executable policy or validation logic | `scripts/` | Normal code lifecycle | A prose rule that can be checked must point to its executable check; do not maintain a second prose-only implementation. |
| Temporary AI reasoning or scratch notes | Not committed | Ephemeral | Promote only distilled conclusions with provenance; otherwise discard before handoff. |

For this design's first consolidation release, the current-context routing page is
`wiki/survey/current/README.md`; machine assets are placed under `wiki/survey/current/data/` or
referenced there through the current manifest when a path cannot yet move safely; and the legacy
Gate-S1 index is created at
  `wiki/audit/system-first-stage1a/INDEX.md`, while the 77 already registered legacy paths remain
  exceptional path-pinned entries referenced by that index.

### 11.2 Document lifecycle

Every campaign follows this sequence:

1. **Draft:** mutable working material lives under `wiki/survey/workbench/<campaign>/`. It is absent
   from the audit registry and cannot carry a completion claim.
2. **Effective:** accepted working rules are distilled into stable files under `wiki/survey/current/`.
   The current manifest is updated in the same commit; active documents cannot require a workbench or
   archive file to be interpreted.
3. **Review freeze:** anything sent to, received from, or signed by a reviewer is copied once into
   `wiki/audit/<campaign>/<round-id>/`, registered, and immutable from that commit onward. It is not
   first created in an active directory and moved later.
4. **Correction:** the current effective files are corrected in place, while the historical claim is
   superseded by a new audit correction. Historical audit bytes are never edited.
5. **Campaign close:** after the final verdict or stage transition, run the distillation and archive
   scan in the same closeout batch. Remove individual audit-round links from current pages, retain one
   audit-index pointer, move eligible unregistered intermediates with `git mv`, and prove that the
   current manifest and active scripts have no old-path dependency.
6. **Next campaign:** create a new workbench and audit namespace. Do not reuse the prior campaign's
   response, amendment, or check-output filenames.

### 11.3 Mandatory consolidation and archive triggers

Consolidation is required at the earliest of these events:

- a third amendment or correction would otherwise be added to one effective document;
- the protocol, router, or hot-state file exceeds its context budget;
- a reviewer round closes a Gate MAJOR or changes an executable contract;
- an AI or human handoff requires more than the current protocol and status page to determine the next
  action;
- a stage boundary, campaign verdict, sign-off request, or publication release is reached; or
- two active files make competing claims about the same current field.

The third amendment may be preserved as an audit artifact, but its effective rules must be folded
into the current specification immediately. A fourth amendment is forbidden until consolidation has
completed.

Archive movement is required when a working or generated document is both superseded and absent from
the current manifest. The move occurs in the same commit as the replacement when safe; otherwise it
is a named closeout blocker and must complete before sign-off. Registered audit documents are the
exception: they never move under the current registry contract and become cold solely by removing
them from active routing.

### 11.4 Routing enforcement

The context-surface checker will classify every persistent document as `HOT`, `CURRENT`, `REGISTRY`,
`AUDIT`, `ARCHIVE`, or `WORKBENCH`. It fails when:

- a document is unclassified;
- a hot/current file points to an individual audit round instead of the campaign index, except for an
  explicitly active review transaction;
- an archived or workbench file appears in the default AI context manifest;
- multiple current versions of the same protocol, table, schema, or status document exist;
- a new review artifact is created outside `wiki/audit/`;
- an audit artifact is modified or moved after registration;
- an eligible superseded unregistered file remains in an active directory after campaign close; or
- a fourth unconsolidated amendment appears.

## 12. Success criteria

The remediation is complete only when:

- every review-named field is explicitly bound and every new counterexample fails for its designated
  reason;
- the generic twelfth-row test proves the contract does not rely on existing row IDs;
- both platform reports pass with equal occupancy;
- protocol v2 compiles to the unchanged frozen query bytes;
- active context is self-contained and within budget;
- registered audit artifacts remain byte-and-path identical;
- unregistered archive moves have no live dependents;
- all canonical files state Stage-1A and zero new execution; and
- the dated correction is truthful and ready for an independent reviewer, without self-signing.
