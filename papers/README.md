# Paper project workspace

`papers/` is the local checkout root for independently admitted Stage‑3 paper projects. The umbrella
owns this README and `registry.json`; every child paper directory is a separate Git/GitHub repository
and is ignored by the umbrella.

## Promotion rule

A paper repository is created only by promotion from a qualified study candidate under
`OWNER_GO_AND_PAPER_EXECUTION_CONTRACT` (Decision-Log 续91). It owns Stage‑3 work: large-scale
pre-registered confirmatory experiments, final evidence, manuscripts, submission and publication
releases. Candidate IDs (R1/R2…) and venue/year tokens never become repository names. An empty
registry is legal; an empty paper repository is not — no pre-created placeholder repos.

A paper's success criterion is a reproducible, adequately powered verdict on its pre-registered
claim; positive, null and negative results are equally legal completions.

## Current state

No paper project is admitted; `registry.json` is empty. Promotion schema, workspace checks and the
promotion receipt machinery are intentionally deferred until the first real candidate approaches
(trigger: a study candidate reaches paper-candidate readiness, or the owner starts the first paper
admission). Program-level experiment assets are routed by
[`wiki/Experiment-Assets.md`](../wiki/Experiment-Assets.md).
