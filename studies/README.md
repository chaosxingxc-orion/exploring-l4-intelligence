# Study repository workspace

`studies/` is the local checkout root for independently admitted research studies. The umbrella owns
this README and `registry.json`; every child study directory is a separate Git/GitHub repository and is
ignored by the umbrella.

## Admission rule

A study repository is created only after `OWNER_GO_AND_EXECUTION_CONTRACT`. Stage-1 candidate labels
such as R1 or R2 are provenance identifiers, not engineering identities, and must not appear as tokens
in repository names. A candidate that sunsets before admission receives no empty repository.

An admitted repository uses the semantic name frozen in its execution contract. Register it in
`registry.json`, bind its owner decision record and `wiki/experiments/<slug>/README.md`, then clone or
initialize the independent repository at `studies/<slug>/`.

## Current state

One study is admitted: **speech-aware-evidence-acquisition**. The owner GO was signed on 2026-08-03;
the effective speech-only scope and semantic identity were frozen on 2026-08-04 (see `registry.json`
and `wiki/experiments/speech-aware-evidence-acquisition/2026-08-04-owner-speech-domain-scope-and-identity-contract.md`).
Its checkout lives at `studies/speech-aware-evidence-acquisition/` with its own Git history and private
remote. General/environmental-audio tasks are outside this study; downloaded cross-domain assets remain
in the canonical lock. R1 remains sunset provenance and has no engineering repository.

Program-level experiment assets and their storage boundaries are routed by
[`wiki/Experiment-Assets.md`](../wiki/Experiment-Assets.md).
