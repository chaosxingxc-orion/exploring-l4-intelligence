# Research-engineering directory reorganization proposal for Fable5

> **Status (2026-08-03): `IMPLEMENTED_AND_SUPERSEDED_2026-08-03`.** This proposal was fully implemented by
> the 2026-08-03 directory reorganization and is retained only as a historical design rationale; it is no
> longer operating instructions. The target tree below (including `projects/`), `PROPOSED_FOR_REVIEW` and
> `remote_repository_creation: WITHHELD` all describe the pre-implementation state. The current
> authoritative entry points: `docs/architecture.md`, the owner execution contract
> (`wiki/experiments/audio-aware-evidence-acquisition/2026-08-03-owner-go-and-execution-contract.md`)
> and the post-reorganization review proposal
> (`docs/superpowers/specs/2026-08-03-post-reorganization-architecture-review-and-remediation-proposal.md`).

## Document status

```yaml
proposal_id: FABLE5-STUDY-DIRECTORY-REORGANIZATION-V1
date: 2026-08-02
addressee: Fable5
decision_owner: research owner
scope: umbrella and future semantic study repositories
proposal_status: IMPLEMENTED_AND_SUPERSEDED_2026-08-03
execution_authority: DOCUMENTATION_ONLY
remote_repository_creation: WITHHELD  # at issuance; repo created 2026-08-03 under OWNER_GO_AND_EXECUTION_CONTRACT
model_or_api_execution: WITHHELD
```

This proposal turns already-settled research governance principles into an executable directory and asset
migration plan. Fable5 is asked to review and return `ACCEPT`, `ACCEPT_WITH_AMENDMENTS` or
`REJECT_WITH_ALTERNATIVE`; before the owner issues `OWNER_GO_AND_EXECUTION_CONTRACT`, no remote repository is
created, no formal study checkout is initialized, no code is migrated, and no model experiment is run.

## 1. Why reorganization is needed

The current directory carries three different identities at once: the historical/supporting engineering of
W1–W4, the research-argument numbering R1–R9, and the engineering implementation of future formal research
objects. Continuing to use W or R directly as engineering directories produces four structural problems:

1. **Argument numbering is mistaken for engineering identity.** R1 was already sunset before Stage‑2, which
   shows that a candidate number does not naturally correspond to an engineering repository; R2 is likewise
   only the source provenance of `audio-aware evidence acquisition`, not a long-term research name.
2. **False serial dependencies are manufactured between directions.** R2 entering engineering should not wait
   for the R3–R9 research to complete, and later directions should not be forced into a single so-called
   R2→R3→… code chain.
3. **Git lifecycles get mixed together.** A formal research object needs its own issues, CI, releases,
   reproduction-experiment commits and paper history; treating it as an ordinary umbrella subdirectory ties
   governance documents and experiment code to the same release cycle.
4. **Wiki management and file storage are easily confused.** The Wiki should manage experiment identity,
   protocols, asset links and decisions; it should not copy models, data, raw traces or the complete code of
   another Git repository.

The recommendation is therefore: **the umbrella owns research governance and the experiment-asset graph; each
admitted semantic research object has its own GitHub repository; local checkouts are unified under the
umbrella's `studies/`.** `studies/` is a local workspace container and registration surface, not a merging of
all research back into one Git repository.

## 2. Proposed target topology

```text
exploring-l4-intelligence/                    # umbrella Git repo
├── studies/
│   ├── README.md                             # umbrella tracked
│   ├── registry.json                         # umbrella tracked; admitted studies only
│   └── audio-aware-evidence-acquisition/     # independent Git repo; only after owner GO
├── projects/
│   ├── speech-mllm-training-free-rl/          # W1; unchanged independent repo
│   ├── speech-mllm-efficient-rl-alignment/    # W2; unchanged independent repo
│   ├── speech-mllm-multitask-rl/              # W3; unchanged independent repo
│   └── speech-mllm-omni-embedding-rl/         # W4; unchanged independent repo
├── common/                                   # stable, genuinely cross-study utilities only
├── wiki/
│   ├── Research-Objective.md                 # HOT program state
│   ├── Experiment-Assets.md                  # program-wide experiment router
│   ├── experiments/<semantic-study-slug>/    # admitted-study lifecycle ledger
│   ├── survey/                               # Stage-1 evidence and candidate provenance
│   └── audit/                                # immutable reviewer transactions
├── docs/
│   ├── datasets.lock.json                    # canonical program-level data identity
│   ├── superpowers/specs/                    # engineering contracts and plans
│   └── checks/<study-slug>/<release-id>/     # reproducibility receipts
└── scripts/                                  # umbrella governance and shared asset tooling
```

The long-term identity of the first engineering project is proposed to be frozen as:

```yaml
research_name: audio-aware evidence acquisition
repository_slug: audio-aware-evidence-acquisition
python_package: audio_aware_evidence_acquisition
source_provenance: R2
```

`R2` must never appear in the remote repository name, the Python package, the primary MLflow experiment
namespace or a formal experiment ID. It is retained only in the provenance fields of proposals, reviews, the
Decision‑Log and the registry. R1 gets no empty repository and no placeholder directory.

## 3. Why an independent GitHub repository rather than just an umbrella subdirectory

A local directory and a GitHub repository are not mutually exclusive. The recommended form is
"**an independent GitHub repository + a local checkout under `studies/`**":

| Requirement | As an ordinary umbrella directory | Independent repo checked out into `studies/` |
|---|---|---|
| Independent issues, CI, releases, paper versions | Coupled to the governance repo | Managed independently |
| Sunsetting, splitting or merging research | Easily leaves half-finished directories | Can be archived or redirected independently |
| Code review and reproduction-experiment commits | Diluted by Wiki/governance changes | Every commit belongs to that research object |
| Cross-research reuse | Invites copy-paste | Promoted to `common/` only once stable |
| Local collaboration convenience | Convenient | Equally convenient, held together by `studies/` |
| Umbrella status cleanliness | Easily picks up stray experiment files | The nested repo is ignored by the umbrella |

An independent repository does not weaken the Wiki. On the contrary, the Wiki becomes the cross-repository
experiment control plane: it links questions, protocols, study commits, dataset/model revisions, MLflow runs,
external artifacts, results, deviations and decisions into one auditable asset graph.

## 4. Asset ownership and migration judgment

| Current or future asset | Target authority | Action this round |
|---|---|---|
| The R2 v20 proposal, the round‑22 review/permission | umbrella Wiki/audit | Stay in place, not copied into the study repo |
| Current research state, GO/NO-GO, stage rulings | umbrella Wiki | Retained and superseded in place over time |
| program-level dataset identity/hash/license | `docs/datasets.lock.json` | Stays in place; the study references it by key only |
| Data, models, audio, raw generations/traces | `SPEECHRL_DATA_DIR` | Never migrated into Git; referenced via manifest/hash |
| study-specific loaders, scorers, adapters, controllers | independent study repo | Created fresh or explicitly migrated after owner GO |
| study config, tests, CI, lockfile, run entrypoint | independent study repo | Created after owner GO |
| Formal experiment records, protocol deviations and research decisions | `wiki/experiments/<slug>/` | Created in the admission transaction |
| Run metadata and large results | MLflow / external artifact store | The Wiki stores IDs, URIs and hashes |
| release reproduction receipts | study release or umbrella `docs/checks/` | Generated per release |
| Existing W1–W4 code and `_repro` history | the original work repo | History is not moved; referenced or explicitly adopted as needed |
| Lightweight capabilities genuinely shared by multiple studies | `common/` | Promoted only after at least two real consumers |

The core rule is: **migrate by authority, not by "looks related".** Literature, decisions and the experiment
index belong to the umbrella; executable research code belongs to the study repository; large-byte assets
belong to the external data root; W1 history is not renamed or moved just because a new direction was approved.

## 5. Phased implementation proposal

### Phase 0 — doable now: model-free, no-repository preparation

1. Close D1–D4 for Earnings21, Earnings22 and ConEC: sample identity, information boundary/leakage, scorer,
   and a ten-sample trace.
2. Complete the exact fields of the Stage‑2A execution contract: remote URL, runtime/model revision, baseline
   revision, split, prompt, metric, budget, stop conditions and exposure.
3. Build a read-only inventory for code that may be migrated in: source repo, current commit, license,
   dependencies, test status, target ownership.
4. Do not create a `studies/audio-aware-evidence-acquisition/` placeholder directory; an empty directory
   creates the illusion that admission has already happened.

### Phase 1 — the owner GO transaction: creating the research identity

The following actions must complete within one reviewable transaction:

1. The owner issues `OWNER_GO_AND_EXECUTION_CONTRACT`;
2. Create the independent GitHub repository `audio-aware-evidence-acquisition`;
3. Check it out to `studies/audio-aware-evidence-acquisition/` and confirm it has its own `.git`;
4. Register the URL, default branch, decision record and Wiki experiment index in `studies/registry.json`;
5. Create `wiki/experiments/audio-aware-evidence-acquisition/README.md`;
6. Run the study-workspace, context-surface and registry fail-closed checks.

### Phase 2 — engineering infrastructure: build a reproducible vertical chain first

The proposed initial structure of the independent repository:

```text
audio-aware-evidence-acquisition/
├── README.md
├── LICENSE
├── pyproject.toml
├── src/audio_aware_evidence_acquisition/
│   ├── data/                 # lock-key based loaders; no dataset bytes
│   ├── models/               # frozen-core API adapter
│   ├── evidence/             # schema, provenance and admission
│   ├── scoring/              # official/registered metrics
│   ├── tracing/              # request/tool/response/cost trace
│   └── experiments/          # composition, not raw outputs
├── configs/
│   ├── model/
│   ├── dataset/
│   ├── baseline/
│   └── experiment/
├── scripts/
│   ├── reproduce.sh
│   └── evaluate.sh
├── tests/
│   ├── unit/
│   ├── integration/
│   └── contract/
└── docs/
    ├── engineering.md        # repository-local implementation facts
    └── migration-manifest.md # adopted files and provenance
```

The first two-week slice delivers only the reproduction-zero vertical chain
loader→frozen-core adapter→trace→scorer→artifact link, plus one readiness-qualified closest-prior attempt. It
does not execute v20's full search and forms no novelty conclusion.

### Phase 3 — reproduction-first Stage‑2A

1. First reproduce the closest, strongest, readiness-qualified public prior;
2. A failed reproduction must distinguish implementation defect, carrier mismatch and baseline-not-ready;
3. Only after at least one prior path is credible does work move to directional prototypes for OBS,
   ORG/SUPPLY and USE/CONTROL;
4. Use experiments to decide whether the three pillars are retained, merged, split or sunset, and begin
   converging on a concrete method and novelty claim;
5. Stage‑2B is entered only after the final approach is frozen.

## 6. Safe migration protocol

When any existing code enters the new study repository, run the following copy-and-verify flow rather than
moving it directly:

1. Register the source repo, commit, original path, license and migration rationale in `migration-manifest.md`;
2. Copy the minimum necessary files, keep the source, and delete no W1–W4 history;
3. Verify content before and after the copy by hash or Git blob;
4. Get the new repository's tests passing first, then update umbrella Wiki/registry references;
5. Extract a general implementation into `common/` only after confirming at least two real consumers exist;
6. If initializing the new repository fails, rolling back is simply deleting the not-yet-registered temporary
   checkout; the umbrella and W1–W4 are unaffected.

Prohibited: rewriting history across repositories, bulk-moving `_repro`, putting data or models into Git,
creating an empty repository before authorization arrives, renaming W1 directly into the new study, and using
R2 or Stage‑2 as a long-term engineering directory name.

## 7. The feedback Fable5 needs to give

Fable5 is asked to reply point by point on the following:

1. Are `audio-aware-evidence-acquisition` / `audio_aware_evidence_acquisition` accepted as the repository and
   package names?
2. Which existing implementations genuinely need to be consumed by the new study from W1 or the umbrella?
   Give a file-level list with source commits; no whole-repository migration.
3. Which data/scoring/trace tooling is program-level shared tooling, and which belongs to this study only?
4. Which item is recommended as the first runnable closest-prior reproduction, and what is the rationale and
   public-artifact readiness?
5. Which choices that must be frozen by the owner are still missing from the execution contract?
6. Return one of `ACCEPT`, `ACCEPT_WITH_AMENDMENTS` or `REJECT_WITH_ALTERNATIVE` for this proposal.

## 8. Acceptance conditions

The directory reorganization counts as complete only when all of the following hold simultaneously:

- The umbrella tracks no file of any study sub-repository, only `studies/README.md` and `studies/registry.json`;
- study slugs and package names contain no R number, W number or stage number;
- Every checkout is in the registry and has its own `.git`;
- The Wiki experiment index resolves to study commit, protocol/config hash, data/model revision and artifacts;
- W1–W4 history and unarchived user assets have not been moved or deleted;
- Data, models and large outputs have not entered Git;
- The study workspace, AI context, CURRENT manifest and audit immutability checks pass;
- A formal opening permission has not been miswritten as a novelty ruling or a model-experiment authorization.

## 9. Recommended ruling

It is recommended that the owner first approve this proposal's **directory and authority model** and require
Fable5 to submit a file-level migration list and an execution contract amendment; only after both are reviewed
should remote repository creation and the Stage‑2A execution GO be issued. This ends the directory debate
immediately while retaining independent oversight of the experiment carrier, budget and closest-prior choice.
