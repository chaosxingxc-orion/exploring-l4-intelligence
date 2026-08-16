# Fable5 verdict: response to the research-engineering directory reorganization proposal and the Stage-2A handoff package

> **Status (2026-08-04): `IMPLEMENTED_AND_SUPERSEDED_2026-08-03`.** This verdict/handoff package was fully
> implemented by the 2026-08-03 directory reorganization and is retained only as a historical design and
> handoff rationale; it is no longer the current entry point. The values below such as
> `study_repository: NOT_CREATED` and `uv pip install -e ../../common -e .` describe the pre-implementation
> state (the study repository has since been created and was narrowed on 2026-08-04 to
> `speech-aware-evidence-acquisition`, and it does not depend on `speechrl_common`). The current
> authoritative entry points: the owner contract
> (`wiki/experiments/speech-aware-evidence-acquisition/2026-08-04-owner-speech-domain-scope-and-identity-contract.md`),
> the Stage-2A entry contract (`docs/superpowers/specs/2026-08-02-speech-aware-evidence-acquisition-stage2a-entry.md`),
> the study repo `README.md`, and the independent re-review feedback
> (`docs/checks/program-architecture/2026-08-03-post-reorg-remediation-independent-review/feedback.md`).

## Document status

```yaml
artifact_id: FABLE5-STUDY-DIRECTORY-REORGANIZATION-VERDICT-V1
implementation_status: IMPLEMENTED_AND_SUPERSEDED_2026-08-03  # added 2026-08-04; see banner
date: 2026-08-02
responds_to: docs/superpowers/specs/2026-08-02-fable5-study-directory-reorganization-proposal.md
verdict: ACCEPT_WITH_AMENDMENTS
umbrella_reorganization: COMMITTED
study_repository: NOT_CREATED__GATED_ON_OWNER_GO_AND_EXECUTION_CONTRACT
remote_repository_creation: WITHHELD
model_or_api_execution: WITHHELD
inventory_source_commits:
  umbrella: b9d7a30
  w1_training_free_rl: 7ed41f6
```

## 1. Verdict

The directory reorganization proposal receives **`ACCEPT_WITH_AMENDMENTS`**.

The accepted core: the umbrella owns research governance and the experiment-asset graph; each admitted
semantic research object gets its own GitHub repository; local checkouts are unified under `studies/`;
candidate numbering serves only as provenance; migration follows authority rather than "looks related". This
topology is fully self-consistent with the existing gates (registry admitted-only, fail-closed workspace
check, immutable audit).

What this transaction executed: the entire umbrella-side reorganization batch is in HEAD and passes three
gates (`study_workspace_check` PASS, `sf_current_package_check --check` PASS, `ai_context_surface_check` PASS,
check suite 131 tests green).

What this transaction explicitly did not execute: `studies/audio-aware-evidence-acquisition/` was **not
created**. That is not an omission but a consistent requirement of the proposal and the gates — the registry
accepts only admitted repositories, and the workspace check strictly requires every checkout to be
registered, to carry a real GitHub remote URL, and to have its own `.git`. Before the owner issues
`OWNER_GO_AND_EXECUTION_CONTRACT`, a study directory in any form (placeholder, seed, unregistered local repo)
would either turn the fail-closed gates red or force a false entry into the registry. Creating the
engineering directory is mechanized by the runbook in section 5 below into a single-transaction operation; all
that is awaited is one owner ruling.

## 2. Answers to the proposal's six questions

### Q1 — Repository name and package name

Accept `audio-aware-evidence-acquisition` (repository/slug) and `audio_aware_evidence_acquisition`
(Python package). The slug passes the workspace check's semantic kebab-case validation and contains no
candidate token.

### Q2 — Existing implementations to be consumed by the new study (file level)

Adoption falls into two classes: **DEPEND** (the study consumes it as an editable dependency, no copying) and
**COPY_AND_VERIFY** (copied and verified item by item at R0 per the protocol in the proposal's section 6, and
recorded in `migration-manifest.md`). All entries are currently in CANDIDATE state; this list does not
constitute migration authorization.

| Source (commits in the frontmatter) | Target location | Method | Reason |
|---|---|---|---|
| `common/src/speechrl_common/` (audio/io, rl/metrics, models/generative_omni, models/prompts, tracking/mlflow_logger, utils/seed) | study depends on `../../common` | DEPEND | Already a program-level shared layer, same mechanism as W1–W4 |
| W1 `scripts/baselines/two_pass_runner.py` | `src/.../models/` frozen-core adapter reference | COPY_AND_VERIFY | The real runnable call path for llama-server + input_audio lives here |
| W1 `scripts/baselines/provenance.py` | `src/.../tracing/` | COPY_AND_VERIFY | The request/response/cost provenance accounting primitive |
| W1 `scripts/baselines/metrics.py`, `stats.py`, `deterministic_draw.py` | `src/.../scoring/` and experiment statistics | COPY_AND_VERIFY | Scoring and deterministic-sampling primitives, measured in practice during the probe campaign |
| W1 `scripts/loaders/_common.py`, `registry.py` | `src/.../data/` loader skeleton | COPY_AND_VERIFY (pattern only) | The registration/common-layer pattern for carrier loaders; the carriers themselves are all written fresh |
| W1 `scripts/knowledge/kb_retrieve.py`, `kb_schema.py`, `corpus_lock.py` | `src/.../evidence/` candidate | DEFER_TO_METHOD | Evidence-supply-side candidates; not adopted before the method converges (full KB construction is PARKED) |

**Explicitly not migrated**: W1's 27 probe-era dataset loaders, the baselines wave/cell one-off experiment
scripts, the full KB construction pipeline, and any `_repro` history. Earnings21, Earnings22 and ConEC have no
existing loader and are new study code.

### Q3 — The program-level / study-only division

- **Program-level (stays in the umbrella)**: the `scripts/data/` acquisition and asset-lock tooling,
  `docs/datasets.lock.json`, the `docs/checks/` receipts, the three governance gates, and the
  `speechrl_common` shared layer.
- **Study-only (independent repository)**: the three carrier loaders and split management, the frozen-core API
  adapter, the evidence schema (provenance / OBS-SUPPLY separation / admission / final use), the scorer
  adapter, the trace, and the experiment composition layer.

### Q4 — Recommendation for the first closest-prior reproduction

Recommend the **ConEC context biasing / contextual-ASR line** as the first reproduction: a public GitHub
artifact, the same lineage as the already-locked carriers Earnings21/22 (the highest readiness among the
candidates), and an information boundary isomorphic to this research. The RECOVER-style correction line and
the Siskos entity-resolution line are queued second and third; Corona 2017, Raghuvanshi 2019, Flemotomos 2024
and COALA 2026 are first assessed as threat/reproduction candidates per the entry contract, and only then is
the mandatory table frozen. The final freezing of the mandatory table is a ruling of the owner execution
contract.

### Q5 — Fields the execution contract still needs the owner to freeze

| Field | Suggested value (directly adoptable) | Must be ruled by the owner |
|---|---|---|
| Remote repository | — | GitHub org/URL |
| Runtime | llama.cpp llama-server resident + Qwen3-Omni-30B GGUF (`-ngl 28`, the existing measured path) | Pinning the build commit and the GGUF file hashes |
| Carriers | The three keys Earnings21/22/ConEC inside the lock | The discovery/confirmatory split seed and freezing procedure |
| Baseline | The Q4 queue order | The mandatory list + exact revisions |
| Budget | — | Calls/GPU/audio-seconds/first-slice ceilings and the stop-go checkpoints |
| Exposure | The inherited exposure exclusion table continues with current accounting | Confirming the per-run contact ledger format |

### Q6 — Overall reply

`ACCEPT_WITH_AMENDMENTS`; the amendments are in the next section.

## 3. Amendments

- **A1 (Phase-1 atomicity raised to an explicit constraint)**: the workspace check requires a registry entry to
  carry a real GitHub URL and the local checkout to have its own `.git`, so "local checkout first, remote added
  later" is mechanically infeasible. The six steps of Phase 1 (issue the contract → create the remote → checkout
  → registry → experiment index → gates) must complete as a single transaction.
- **A2 (clarifying where pre-GO research happens)**: before the owner GO, all research for this direction
  (literature delta lane, the D1–D4 model-free data closure, contract field preparation) has its home in the
  **umbrella root** — the authority for that work already lies in the umbrella. No temporary directory may
  masquerade as the study repository. The startup surface is in section 6.
- **A3 (the migration list is in candidate state)**: the Q2 list is ruled on item by item at R0 under the
  copy-and-verify protocol and recorded in `migration-manifest.md`; adoption depends on the new repository's
  tests passing, and nothing is migrated automatically just because it is on the list.

## 4. Prerequisites to freeze before Owner GO

The owner need only do one thing: review the Q5 table, write concrete values for the six entries in the
"must be ruled by the owner" column, and issue `OWNER_GO_AND_EXECUTION_CONTRACT` as a dated decision record.
Everything else is mechanized.

## 5. GO transaction runbook (executed as a single transaction after issuance)

1. Create the remote repository `https://github.com/<org>/audio-aware-evidence-acquisition.git` (requires
   explicit owner authorization);
2. `git init` the local repository, make the seed initial commit, and check it out to
   `studies/audio-aware-evidence-acquisition/`;
3. Write the entry into `studies/registry.json` (template below; `decision_record` points at the decision record
   the owner issued):

```json
{
  "name": "audio-aware evidence acquisition",
  "slug": "audio-aware-evidence-acquisition",
  "local_path": "studies/audio-aware-evidence-acquisition",
  "github_repo": "https://github.com/<org>/audio-aware-evidence-acquisition.git",
  "lifecycle": "engineering",
  "decision_record": "wiki/<owner-go-decision-record>.md",
  "experiment_index": "wiki/experiments/audio-aware-evidence-acquisition/README.md"
}
```

4. Create `wiki/experiments/audio-aware-evidence-acquisition/README.md` (the experiment ledger index);
5. Run `study_workspace_check`, `sf_current_package_check --check` and `ai_context_surface_check`;
6. Close with a single umbrella commit; the study repository advances the R0 vertical chain along the
   proposal's Phase 2 skeleton.

Seed `CLAUDE.md` content for the study repository (written to disk verbatim at GO, thereafter evolved
autonomously by that repository):

```markdown
# CLAUDE.md — audio-aware-evidence-acquisition

Standalone research repository: audio-aware evidence acquisition on a frozen speech/omni core
(provenance: see the umbrella wiki audit layer).

## Research boundary (immutable)
- The frozen Qwen3-Omni core is reached across an API-shaped service boundary; zero parameter
  modification; no task-trained model; no second answering LLM.
- Gold answers / reference transcripts / test annotations / future turns must never cross the runtime
  boundary.
- OBS re-parsing and external evidence supply are separately traceable; every external response / tool
  action / model request is versioned and hashable.
- discovery and confirmatory are disjoint; confirmatory criteria are frozen before results are read.

## Routing
- Current research state and experiment ledger: umbrella `wiki/Research-Objective.md`,
  `wiki/Experiment-Assets.md`, `wiki/experiments/audio-aware-evidence-acquisition/README.md`.
- Dataset identity: umbrella `docs/datasets.lock.json` (referenced by key, hashes never copied); bytes live
  under `SPEECHRL_DATA_DIR` and never enter Git.
- Execution contract (the sole authorization surface for model contact, budget, baselines and stop
  conditions): umbrella
  `docs/superpowers/specs/2026-08-02-audio-aware-evidence-acquisition-stage2a-entry.md`
  and the GO decision record issued by the owner.

## Environment
- WSL2 `Ubuntu-24.04` + `~/.venvs/speechrl` (Python 3.12); inference goes through llama.cpp llama-server
  (GGUF, `-ngl 28` resident). Install: `uv pip install -e ../../common -e .`.

## Prohibited
- Any model/API contact without the execution contract (including a single-sample smoke); committing data /
  weights / raw traces to this repository; moving W1–W4 code in around the migration-manifest; pushing
  without umbrella authorization.
```

## 6. Pre-GO phase: the startup surface for an R2 direction research session

When opening a dedicated session for this direction before GO, take the **umbrella root** as the working
directory and load, in order:

1. `CLAUDE.md` (loaded automatically) → `wiki/Research-Objective.md` → `wiki/Project-Thesis.md`;
2. This verdict;
3. `docs/superpowers/specs/2026-08-02-audio-aware-evidence-acquisition-stage2a-entry.md`
   (the E0/R0/R1/X sequence and the freeze sheet);
4. The formal opening permission note (path in the governance section) — including the literature cutoff
   `2026-08-02`, the four STOP_THE_LINE triggers, and the delta ledger rules.

Work permitted in that session: the literature delta lane (bounded weekly), the D1–D4 model-free data closure,
prior readiness assessment, and contract field preparation. Forbidden: model contact, creating a repository,
and writing research output into `studies/`.

## 7. Governance and supporting evidence

- Proposal: `docs/superpowers/specs/2026-08-02-fable5-study-directory-reorganization-proposal.md`
- Architecture specification: `docs/superpowers/specs/2026-08-02-study-repositories-and-experiment-assets.md`
- Formal opening permission: `wiki/audit/system-first-stage1c-v2/round-22/2026-08-02-audio-aware-evidence-acquisition-formal-opening-permission-note.md`
  (`FORMAL_OPENING_APPROVED` and `STAGE2A_EXECUTION_WITHHELD` are simultaneously in force)
- Umbrella reorganization landing: commits `c4a26a6` (the 46-item governance batch), `b9d7a30` (re-stamping the
  stage-0 report); three gates PASS, check suite 131 tests green.
