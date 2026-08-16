# Paper project workspace

`papers/` is the local checkout root for independently admitted Stage‑3 paper projects. The umbrella
owns this README and `registry.json`; every child paper directory is a separate Git/GitHub repository
and is ignored by the umbrella.

## Promotion rule

A paper repository is created only by promotion from a qualified study candidate under
`OWNER_GO_AND_PAPER_EXECUTION_CONTRACT` (Decision-Log continuation entry 91). It owns Stage‑3 work: large-scale
pre-registered confirmatory experiments, final evidence, manuscripts, submission and publication
releases. Candidate IDs (R1/R2…) and venue/year tokens never become repository names. An empty
registry is legal; an empty paper repository is not — no pre-created placeholder repos.

A paper's success criterion is a reproducible, adequately powered verdict on its pre-registered
claim; positive, null and negative results are equally legal completions.

## Current state

No paper project is admitted; `registry.json` is empty. The zero state is machine-enforced by
`scripts/checks/paper_workspace_check.py` (strict empty registry, no child checkouts, ignore rule,
count consistency; any registered entry fails closed). The admission-mode extension of that checker
— full entry schema, candidate bundle, promotion receipt, origin/branch proof — is intentionally
deferred until the first real candidate approaches (trigger continuation entry 92: the earliest of the four
pre-exposure events, or the owner starting the first paper admission). Program-level experiment assets are routed by
[`wiki/Experiment-Assets.md`](../wiki/Experiment-Assets.md).
