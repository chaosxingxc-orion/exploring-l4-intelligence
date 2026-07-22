# Stage-1B → Stage-1C knowledge-base and provisional reproduction-input plan

**Status:** Stage-1B preparatory input only. Metadata and environment identity may be recorded, but
Stage-1B does not choose a problem, rank or freeze reproduction slices, run a research model, compute
a dataset metric, execute a smoke run, or build a prototype.

## Outcome contract

Stop discovery after the three registered 1,000-paper rounds. Consolidate no more than 1,000 unique
retained works; the cap is not a quota. Build one metadata-only paper registry and one reproducible
experiment-environment manifest from that roster. PDFs, e-prints, datasets, model weights, extracted
text, and run outputs stay under `SPEECHRL_DATA_DIR` and never enter Git.

## Phase 1 — close the evidence portfolio

- [x] Verify every abstract-authorized PDF or retain an explicit bounded failure.
- [x] Finish local page-level extraction and emit `KEEP_CORE`, `KEEP_TRANSFER`, `KEEP_NEGATIVE`,
  `KEEP_INSTRUMENT`, or `DROP`; unresolved download/extraction/repository states cannot silently enter
  the roster.
- [x] For speech/audio papers, bind task tags, named datasets, exact lock identity, local presence, and
  task/split suitability. A directory-name match alone is not reproduction readiness.
- [x] For non-speech papers, retain a transfer candidate only when the paper-linked repository is
  reachable, licensed, contains inspectable source and an environment specification, and the
  transferable signal→decision path is explicit. Record weights/data/config/eval-entrypoint gaps.
- [x] Deduplicate by canonical arXiv ID and freeze the capped roster hash. Stop broad scanning.

## Phase 2 — build the knowledge base

- [x] Export one append-only `sf-paper-registry-record-v1` row per retained paper under
  `wiki/survey/registry/`; include the five durable fields: conclusion, reasoning summary, purpose
  chain, provenance, and invalidation conditions.
- [x] Store only metadata, normalized method-path terms, dataset/repository status, hashes, and page
  locators in Git. Keep abstracts, snippets, PDFs/e-prints, and extracted text external.
- [x] Build views from the registry rather than copying facts into prose:
  task × dataset × method-path; signal × decision action; local-executable speech; open transfer;
  negative/falsifier; and instrumentation/evaluation.
- [x] Treat mixed papers as one canonical work with multiple method-path facets. Do not duplicate the
  paper merely to populate multiple cells.

## Phase 3 — materialize the reproduction environment

- [x] Reuse WSL2 `Ubuntu-24.04`, Python 3.12 `~/.venvs/speechrl`, the shared editable `common/`, and
  the existing project-specific Hydra composition. Record exact Python, CUDA, torch, transformers,
  pypdf, git commit, and GPU identities in a release-scoped check report.
- [x] Reconcile the retained speech task/data matrix with `docs/datasets.lock.json`; verify file-level
  inventory only for the first reproduction slice rather than re-hashing all 381 GB on every pass.
- [x] Reconcile the model requirements of the first reproduction slice with the three locked local
  model directories. Missing model/data artifacts require a new lock entry and explicit acquisition
  decision; they are not fetched implicitly.
- [x] Vendor no third-party paper repository into the umbrella. Pin upstream URL, commit, license,
  environment manifest, and adaptation notes; create integration code only in the owning work repo.
- [ ] Define a no-model dry gate first: config composition, path resolution, dataset schema/sample
  metadata, model artifact presence, output isolation, and MLflow routing. Model load/smoke remains a
  separate authority gate.

## Phase 4 — record provisional reproduction inputs for Stage-1C

The following order is a non-binding feasibility heuristic that Stage-1C may accept, revise or
discard after problem selection. It is not a ranking of research problems:

1. speech/audio `KEEP_CORE` with an exact local task-compatible dataset and frozen/test-time path;
2. speech `KEEP_INSTRUMENT` needed to measure the same path;
3. non-speech `KEEP_TRANSFER` with verified code/environment and a small, separable component;
4. strongest `KEEP_NEGATIVE` that can falsify the transfer before expensive integration.

For each provisional input, record a reproduction worksheet with upstream commit, target claim, minimal
dataset split, metric, expected artifact, compute bound, adaptation delta, pass/fail criterion, and
abort condition. A worksheet becomes a reproduction card only after Stage-1C owner selection. Stage-2A
reproduces the nearest prior before introducing a new technical mechanism.

The comparator-first ASR worksheet is a `PROVISIONAL_INPUT / NOT_STAGE_FROZEN` artifact at
`docs/checks/stage1b-handoff/2026-07-22-bounded-scan/reproduction-priority.md`. Stage-1C has not
selected it. Its model/data smoke and metric remain unexecuted behind both stage and authority gates.

## Release gates

- Registry count equals the retained roster count and is ≤1,000.
- Registry canonical IDs are unique; every row has PDF hash and at least one page locator.
- Every `KEEP_TRANSFER` has a paper-linked repository record; no generic dependency/references URL can
  satisfy the gate.
- Every local dataset claim states `TASK_MATCH` or `REQUIRES_SPLIT_REVIEW`.
- Git contains no PDF, e-print, extracted text, dataset, model, or output bytes.
- New survey/pipeline code reaches at least 80% test coverage.
- Current HOT/CURRENT status says that broad scanning stopped and names Stage-1B mapping release and
  independent Stage-1C transition review as the next actions.
