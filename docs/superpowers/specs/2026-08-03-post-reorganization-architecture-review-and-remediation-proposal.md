---
title: "Post-reorganization architecture review and remediation proposal"
proposal_id: "PROGRAM-DIRECTORY-POST-MIGRATION-REVIEW-V1"
date: "2026-08-03"
addressed_to: "research engineering team, Fable5, and the research owner"
reviewed_umbrella_commit: "772e6ed15ac0006ddd34e0600b6f994230692eb8"
reviewed_study_commit: "53d9283d92059e7561c60a2b402af7bd5af074b8"
proposal_status: "IMPLEMENTED_WITH_RESIDUAL_GATES"  # updated 2026-08-04; see status note below
overall_assessment: "CONDITIONAL_ACCEPT_WITH_REMEDIATION"
execution_authority: "DOCUMENTATION_AND_GOVERNANCE_PROPOSAL_ONLY"
model_execution_effect: "NO_NEW_AUTHORITY"
---

# Post-reorganization architecture review and remediation proposal

> **Status (2026-08-04): `IMPLEMENTED_WITH_RESIDUAL_GATES`.** The team accepted this proposal and has
> implemented T0–T5 (receipts: `docs/checks/program-architecture/2026-08-03-post-reorg-remediation/`). The
> independent review
> (`docs/checks/program-architecture/2026-08-03-post-reorg-remediation-independent-review/feedback.md`)
> confirmed the local remediation is effective and raised the residual gates G0/G1/G2; G0/G1 were closed on
> 2026-08-04 (receipt: `docs/checks/program-architecture/2026-08-04-residual-gates-closure/`), and G2 (push
> and remote CI) awaits explicit owner authorization. Once G0–G2 are all closed this status is upgraded to
> `IMPLEMENTED_AND_CLOSED`. The original design body is retained unchanged.

## 1. Conclusion for the team

**The main architectural choice of this reorganization is correct**: the umbrella carries Stage‑1, research
governance, shared assets and the experiment index; a formal research object gets its own Git repository under
a semantic name; R/W numbering no longer serves as engineering identity; the W1–W4 local checkouts have left
the active workspace. Starting over is not recommended, and neither is merging the study back into the umbrella.

However, the present rating can only be `CONDITIONAL_ACCEPT_WITH_REMEDIATION`. The physical directory
boundaries are in order, but governance truth, historical asset resolution, independent build capability and
automated checks have not been brought into line with them. Entering model contact now would let experiments
run, but would not guarantee that another machine could rebuild the same environment from the two
repositories' commit records, nor that historical evidence references still resolve.

Recommendation: **the model-free E0 work of D1–D4 may continue; the P0/P1 items in this document must be
closed before the first model contact and before any R0 result is generated.** This does not reopen the
research direction and involves no novelty or methodological ruling; it merely makes the already-chosen
directory architecture genuinely reproducible and auditable.

## 2. What this review found to be correct

1. Both the umbrella and `studies/audio-aware-evidence-acquisition/` are clean Git worktrees; the study has its
   own `.git`, `origin` matches the registry URL, and the remote `master` is the same commit `53d9283d...`.
2. The umbrella ignores study contents through `studies/*/` and tracks only `studies/README.md` and
   `studies/registry.json`.
3. `projects/` has disappeared from the active directory; W1–W4 remotes are retained as cold backups, and the
   four `master` HEADs agree with the retirement tombstone registration.
4. `Research-Objective.md`, the study registry, the experiment index and the owner execution contract now route
   the first study to its semantic name, and R2 has not been written into the repository name, package name or
   experiment namespace.
5. All four current umbrella gates pass: code graph, study workspace, AI context surface, AI context manifest;
   `common/tests` is 21 passed, 1 skipped; all 13 SHA‑256 values of the W1 snapshot verify.

These results show the "two repository classes + three asset planes" direction does not need to change. The
problem is that the existing checks mainly verify that structure exists; they do not yet verify cross-file
semantic consistency, that remote dependencies can be rebuilt, or that the study has a minimum executable
quality gate.

## 3. Defects and severity

| ID | Severity | Defect | Direct consequence |
|---|---|---|---|
| P0-1 | BLOCKER | HOT/management documents conflict with the actual directory | An AI or the team may treat an admitted study as unadmitted, or keep routing work to the deleted `projects/` |
| P0-2 | BLOCKER | All 574 legacy experiment assets are `unresolved`, yet the workspace gate still PASSes | Historical claims appear to exist while their paths do not resolve; the audit chain is broken |
| P1-1 | MAJOR | The study's independence holds at the Git layer but not at the build/dependency layer | Cloning the study alone cannot rebuild the declared environment; `../../common` is an unpinned implicit dependency |
| P1-2 | MAJOR | The study has no tests, lockfile, CI or license/notice | `pytest` outputs `no tests ran`; the remote repository is currently only a directory skeleton and cannot serve as an R0 fail-closed baseline |
| P1-3 | MAJOR | The registry/workspace checker performs only shallow existence checks | A fake `.git`, a wrong origin, a missing registered checkout, and Wiki/registry state drift can all go undetected |
| P1-4 | MAJOR | The W1 snapshot's count, source commits and remote state disagree with the migration record | 13 files are written up as "ten"; the 3 additions have no adoption registration at equal granularity, and the provenance narrative contradicts itself |
| P2-1 | MINOR | `common/`'s identity is still "the shared library of four work repos" | Retired W/W4 terminology keeps shaping the new study; there is no machine-checkable evidence that a module is genuinely shared across studies |
| P2-2 | MINOR | Already-implemented old proposals/specs remain in active specs speaking of `WITHHELD` / no repository / retaining projects | Later collaborators may follow stale implementation instructions rather than the current architecture/contract |

## 4. P0-1: unify current truth

### 4.1 Evidence

- `wiki/Research-Objective.md` and `studies/registry.json`: 1 study has owner GO and is currently at Stage‑2A E0.
- `wiki/Experiment-Assets.md`: still says "Admitted study repositories: 0", still waits on the execution
  contract, and still says W1–W4 are located in `projects/`.
- `wiki/Project-Thesis.md`: the repository table still lists the deleted local paths of W1–W4 as current
  repository classes.
- `docs/superpowers/specs/2026-08-02-study-repositories-and-experiment-assets.md`: still says "keep W1–W4 in
  projects" and "create no nested study repository yet".
- `docs/superpowers/specs/2026-08-02-fable5-study-directory-reorganization-proposal.md`: still
  `PROPOSED_FOR_REVIEW`, `remote_repository_creation: WITHHELD`, and its target tree still contains `projects/`.

### 4.2 Suggested changes

Complete these within one umbrella truth-alignment transaction:

1. Update `wiki/Experiment-Assets.md` to: 1 admitted study, owner GO signed, E0 in progress, W1–W4 locally
   retired with remotes as cold backups; delete stale statistics such as "573 live / 1 history-only".
2. Change the repository table in `wiki/Project-Thesis.md` to three classes: umbrella, admitted studies, and
   retired cold-backup provenance. W1–W4 no longer appear as active paths.
3. Mark both 2026-08-02 architecture proposals as `IMPLEMENTED_AND_SUPERSEDED_2026-08-03`, with a pointer at
   the top of the body to `docs/architecture.md`, the owner contract and this proposal. Retain the historical
   design rationale, but they must no longer serve as current operating instructions.
4. The sentence in the owner contract stating "W1–W4 are unaffected after a rollback" must not be rewritten in
   place; add a dated amendment clarifying that the local repositories are retired and that a rollback affects
   only the study and the umbrella registry and will not restore the old worktrees.
5. Update the stale "four works / W4 flagship / each work repo" semantics in `common/README.md`.
6. Rebuild the AI context manifest and add cross-source fact assertions: the registry study count, the
   Experiment‑Assets count, the HOT endpoint and the study index frontmatter must agree.

## 5. P0-2: turn legacy evidence from an "existence list" into a "resolvable asset"

### 5.1 Evidence

`docs/integrity/experiment-asset-inventory.json` currently records:

```text
recorded_entries = 574
worktree_present = 0
history_only = 0
unresolved = 574
```

This is the true result after deleting the local W1, but `study_workspace_check.py` only compares "does the
generated result match the file" and does not treat a non-zero unresolved as a failure, so it still reports
PASS. Meanwhile `docs/claim_ledger.yaml` and `docs/corpus.lock.json` still contain many `projects/...` paths
and local reproduction commands that no longer work.

The W1–W4 cold-backup remotes were still reachable during this review, and `master` agrees with the tombstone's
final HEAD. So the evidence has not been lost; rather, **the resolver does not understand retired remote
authority**.

### 5.2 Suggested changes

1. Create `docs/integrity/retired-repository-registry.json`, registering for each retired repository at least:
   `repo_id`, remote URL, final branch/commit, retention policy, verified_at, tombstone, local state.
2. Extend the legacy resolver from two states to four:
   `WORKTREE_PRESENT`, `LOCAL_GIT_HISTORY`, `COLD_BACKUP_RESOLVED`, `UNRESOLVED`.
   `projects/<repo>/<path>` should resolve to `remote@final_commit:path` rather than being judged unresolved.
3. Generate `docs/integrity/legacy-asset-resolution.json`: all 574 entries bound item by item to remote, commit,
   path and an optional blob hash. The target is `unresolved = 0`; entries genuinely unrecoverable must carry an
   owner waiver and a reason and must not pass silently.
4. Add a fail-closed rule to `study_workspace_check.py`: `UNRESOLVED > 0` fails unless every item has a dated
   waiver; branch-HEAD drift on a cold backup does not affect an already-frozen commit, but commit
   retrievability should be verified periodically.
5. `docs/claim_ledger.yaml` need not copy the 574 entries back; upgrade dead paths to a resolution key or a
   `git+https://...@commit#path=` URI. The regeneration commands in `docs/corpus.lock.json` must point at a
   still-retrievable commit/snapshot, or be explicitly marked retired/non-runnable.
6. To avoid GitHub becoming the only backup, keep four `git bundle` files under
   `SPEECHRL_DATA_DIR/program-archives/` and register the bundle SHA‑256 values in the umbrella manifest. The
   bundles do not enter Git.

## 6. P1-1: repair the independent study's dependency contract

### 6.1 Evidence

The study `pyproject.toml` has no runtime/dev dependencies and does not declare `speechrl-common`; yet the
README, AGENTS and the migration manifest all require:

```bash
uv pip install -e ../../common -e .
```

This means it works only within the current umbrella's adjacent-directory layout, and each installation consumes
the umbrella `common/` current worktree with no commit pin. An independent Git history cannot explain on its own
which version of common an experiment used.

### 6.2 Suggested changes

In the short term, adopt "**an exact remote pin + a local editable override**":

1. Declare the actually used dependencies and a dev extra in the study `pyproject.toml`; before the first real
   import of `speechrl_common`, bind it to an exact umbrella commit/subdirectory and generate and commit `uv.lock`.
2. `../../common` serves only as a development override; CI and release reproduction must install from the
   locked commit.
3. Add `shared_code_revision` to every experiment record, so common drift is identifiable even when the study
   commit is unchanged.
4. The current study source does not yet import `speechrl_common`, so the "ACTIVE dependency" declaration may
   also simply be removed before R0; add it back with an exact pin when the first module is genuinely consumed,
   avoiding a premature dependency on the whole legacy-rich common package.
5. Only after at least two admitted studies genuinely consume the same capability should `common/` be extracted
   into an independently versioned repository/package; do not create another repository nobody reuses merely for
   the appearance of independence.

## 7. P1-2: turn the study skeleton into a minimum executable engineering baseline

### 7.1 Evidence

- `pytest` collected no tests in the prescribed WSL2 Python 3.12 environment.
- `configs/*` and `tests/*` contain only `.gitkeep`.
- `scripts/reproduce.sh` and `scripts/evaluate.sh` only print "R0 slice not delivered" and exit 2.
- There is no `uv.lock`, CI workflow, `LICENSE` or third-party notice.

These placeholders may exist during E0, but they cannot be called a completed engineering foundation, and tests
must not be added only after the first model call, because by then the information boundary and trace contracts
may already have been implemented incorrectly.

### 7.2 Suggested changes

Deliver at least the following **model-free contract tests** before the first model contact:

1. The registry, owner contract, experiment index, study origin and package identity are mutually consistent;
2. The three carrier lock keys and the model lock key exist, and the loader does not write dataset bytes into Git;
3. gold/reference transcript/test annotation/future turn fields fail closed in the runtime request schema;
4. OBS and SUPPLY trace fields are separated, and request/response/tool/cost are all serializable and hashable;
5. The exposure ledger schema validates, and the model entry point must refuse when the E0/runtime receipt is
   missing;
6. `reference/w1-snapshot/` is not on the package discovery/import path;
7. The pre-E0 refusal behavior of `reproduce.sh`/`evaluate.sh` is itself tested rather than relying on human
   reading.

Also:

- Replace the config `.gitkeep` files with minimal real YAML/schema/README;
- Commit `uv.lock` and add `python -m build` and `pytest` CI;
- State the license policy for the private phase and add source license/NOTICE for the W1 snapshot;
- Have the quality gate require "at least one test collected and all passing", so `no tests ran` is not
  mistaken for success by CI.

## 8. P1-3: upgrade the registry and workspace checker

The current checker covers slug, path, field set, existence of the decision/index files and "no unregistered
directory may appear", but four blind spots remain:

1. A registered study that is not installed does not fail; only `installed - registered` is checked, never the
   reverse difference;
2. `.git` is checked only for path existence, not verified to be a real Git repository;
3. The nested repo's `origin`, branch and remote HEAD are not verified against the registry;
4. The experiment index frontmatter is not parsed, and the admitted count/state in Experiment‑Assets is not
   checked.

Registry schema v2 should add stable identity fields: `default_branch`, `package_name`, `created_at`,
`experiment_namespace`, and the decision-record Git blob. Do not put every experiment commit into the registry;
experiment commits still belong to the Wiki ledger.

The checker should gain two modes:

- Default mode: allows a private study that is not checked out, but verifies the registry, Wiki, decision and
  remote identity;
- `--require-installed`: for the main development machine, requiring every study with
  lifecycle=`engineering|validation` to be installed, `git rev-parse` to succeed, origin to match, and the
  branch policy to be legal.

Each study repository should also configure its own CI; the umbrella `code_graph_check.py` covers only the
umbrella's 20 trusted nodes and must not be read as having verified nested study code.

## 9. P1-4: repair the W1 snapshot provenance

The snapshot's SHA‑256 values are complete and 13/13 pass; the problem is in the record layer:

- The migration manifest and the retirement tombstone say "ten files"; there are in fact 13;
- `repro_asr_best_of_n_v2.py`, `repro_asr_best_of_n_llamacpp.py` and `gpu_session.sh` come from different
  historical commits and never entered the table at the same granularity as the other candidates;
- The snapshot documentation still says the remote was deleted, while the tombstone addendum and on-site
  verification confirm the remote was retained;
- The two legacy runners contain a hardcoded `/mnt/d/.../common/src`, currently harmless because they are not
  integrated, but they must not be promoted into `src/` as they are.

Suggestions:

1. Change the snapshot manifest to one row per file: original repo, original path, source commit, SHA‑256,
   license, current status, adoption target; unify the count to 13.
2. Standardize the wording as "local checkout retired; remote retained as cold backup".
3. Set all 13 items to `QUARANTINED_REFERENCE_NOT_EXECUTABLE`; any file entering `src/` must add a dated
   adoption row, remove absolute paths, add tests and be re-hashed.
4. Add a static check forbidding production source from importing `reference.w1-snapshot` or adding the
   reference directory to `sys.path`.

## 10. P2: shrink common and clean up stale instructions

`common/` may stay in the umbrella, but it should undergo another module-level ownership audit:

- `audio/io`, the data root, lightweight tracking and similar may be retained if they are genuinely program
  infrastructure;
- Modules consumed only by retired works, such as `omni_embed`, `disentanglement` and the W4 probes, should be
  marked legacy and moved out of the active API, or await a real new consumer before being restored;
- A new capability is promoted to shared only after two admitted studies actually consume it;
- Adding `common/OWNERSHIP.md` is recommended, recording per module the consumer study, owner, stability and
  deprecation status.

Old proposals/specs need not be deleted. Historical rationale has value, but their implementation status must be
made explicit through frontmatter/tombstone; current operations enter only from `docs/architecture.md`,
`wiki/Research-Objective.md`, `wiki/Experiment-Assets.md` and the owner contract.

## 11. Suggested implementation transaction order

| Transaction | Owning repo | Content | Blocks model contact? |
|---|---|---|---|
| T0 truth alignment | umbrella | Correct Experiment‑Assets, Project‑Thesis, active spec status and the common README; rebuild the manifests | Yes |
| T1 legacy resolution | umbrella | Retired repo registry, remote-aware resolver, resolution of all 574 entries, claim/lock routing, checker fail-closed | Yes |
| T2 minimum study gate | study | Dependencies/lock, contract tests, CI, license/NOTICE, a real config skeleton | Yes |
| T3 dependency pin | study + umbrella | An exact common revision; add a shared-code pin to the experiment ledger | Yes |
| T4 snapshot correction | study + umbrella tombstone/amendment | Per-file provenance for all 13 items, remote status and the quarantine rule | Complete before R0 |
| T5 common module audit | umbrella | Consumer/ownership/deprecation list and module shrinkage | May be completed after R0 and before X |

Cross-repository work cannot pretend to be an atomic commit. The coordination order should be: first let the
referenced authority commit in its own repository and obtain a commit/blob, then let the consuming repository pin
it, and finally have the umbrella Wiki ledger record the study commit. Never write "latest" in both repositories.

## 12. Acceptance criteria

### Umbrella

```text
python scripts/checks/code_graph_check.py
python scripts/checks/study_workspace_check.py --require-installed
python scripts/checks/legacy_asset_resolution_check.py
python scripts/checks/ai_context_surface_check.py
python scripts/checks/build_ai_context_manifest.py --check
pytest common/tests
```

Requirements: no conflicts in current truth; legacy `UNRESOLVED=0`; the installed study's origin/branch agrees
with the registry; the AI manifest is green; every active module of common has a consumer/owner status.

### Study

```text
uv sync --frozen
python -m build
pytest -q
```

Requirements: the number of collected tests is greater than 0; the model-free contract tests are all green; the
model entry point fails closed when the E0/runtime receipt is missing; the snapshot is not importable; the
lockfile and dependency pins are committed; CI reproduces in a clean clone.

### Documentation and audit

- The registry, Research‑Objective, Experiment‑Assets and the experiment index agree on the admitted count/state;
- The owner contract is not rewritten in place, and post-retirement clarifications go through a dated amendment;
- Both old proposals explicitly state superseded/implemented;
- D1–D4 continue to be registered as E0, with no claim of novelty, method effectiveness or experimental results.

## 13. Ruling requested from the team

The team is asked to reply point by point:

1. Is the overall ruling `CONDITIONAL_ACCEPT_WITH_REMEDIATION` accepted?
2. Is it agreed that T0–T3 are hard gates before the first model contact?
3. Should the legacy cold backups also be made as offline `git bundle` files, or is relying on the GitHub private
   remotes sufficient?
4. Should `common` use an exact umbrella commit pin in the short term, or should the dependency be deferred until
   a second study appears?
5. Who owns umbrella T0/T1, and who owns study T2/T3/T4?

After the team approves this remediation proposal, the recommendation is to execute T0 and T1 first, with Fable5
executing T2–T4 in parallel in the study repository. A post-remediation review then issues "R0 engineering
foundation ready", rather than treating the existence of directories as completed engineering infrastructure.
