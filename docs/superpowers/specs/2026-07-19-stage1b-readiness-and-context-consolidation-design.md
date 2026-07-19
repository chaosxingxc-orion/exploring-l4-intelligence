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
- `wiki/survey/current/system-first-survey-protocol-v2.md` — complete effective protocol;
- `wiki/survey/current/manifest.json` — current machine assets and hashes; and
- `docs/integrity/ai-context-manifest.json` — the files an AI may load by default.

The protocol v2 is an effective specification, not another response letter. It must be understandable
without reading protocol v1, amendments 1-15, proposals, reviews, or responses.

### 4.2 Cold audit surface

Registered dated artifacts remain at their current paths because the existing immutability oracle
pins both path and blob. A new cold index at
`wiki/archive/survey/gate-s1-stage1a/INDEX.md` records, per round:

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
- schema-v3 sidecars in a new versioned directory;
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
- A registered artifact with path or byte drift continues to fail the existing immutability check.
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

## 11. Success criteria

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
