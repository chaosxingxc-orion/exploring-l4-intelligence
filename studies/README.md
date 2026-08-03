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

No study repository is admitted yet. The audio-aware-evidence-acquisition direction has passed Stage‑1C
and received formal-opening permission, but its Stage‑2A execution contract and owner GO remain pending.
Its future remote repository must not be created by this workspace refresh. R1 remains sunset provenance
and has no engineering repository.

Program-level experiment assets and their storage boundaries are routed by
[`wiki/Experiment-Assets.md`](../wiki/Experiment-Assets.md).
