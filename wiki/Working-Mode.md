# Working Mode

This is a multi-repository workspace. Commit every change to the repository that owns it.

## Ownership

- Umbrella governance, Wiki, `common/`, `docs/`, `scripts/`, `studies/README.md` and
  `studies/registry.json` → umbrella repo.
- Admitted study code/config/README → its independent semantically named repo under
  `studies/<semantic-study>/`.
- Models, datasets and large/raw outputs → `SPEECHRL_DATA_DIR`, never Git.
- Run tracking → local MLflow; the Wiki pins run IDs and asset hashes.

Do not create an engineering repo from a conditional candidate. Repository creation requires a semantic
identity, owner GO and an execution contract. Candidate IDs remain survey/audit provenance.

## Git and checks

The umbrella uses `master`; each admitted study records its own branch policy.
Branch non-trivial changes and keep a commit/PR within one repository. Preserve LF normalization and the
lazy-import boundary in `common/`. Run `pytest common/tests`, the owning repository's tests, and the
relevant umbrella gate.

Never create remotes, push, or publish the Wiki without explicit authorization. The repository Wiki
source is authoritative; the web Wiki is a mirror.

## Research flow

Each study advances independently from survey through validation. Once one study enters engineering,
survey of the next candidate may proceed in parallel. Record durable state in [[Research-Objective]],
experiment assets in [[Experiment-Assets]], and detailed placement/lifecycle rules in
[[AI-Collaboration]].
