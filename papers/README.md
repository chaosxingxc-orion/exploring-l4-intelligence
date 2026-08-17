# Paper project workspace

`papers/` is the local checkout root for independently admitted Stage‑3 paper projects. The umbrella
owns this README and `registry.json`; every child paper directory is a separate Git/GitHub repository
and is ignored by the umbrella.

## Promotion rule

A paper repository is created under `OWNER_GO_AND_PAPER_EXECUTION_CONTRACT` — by default through
promotion from a qualified study candidate (Decision-Log continuation entry 91), or by direct
owner admission recorded in the registry entry's authorization record (first exercised
2026-08-17). It owns its topic's research work end to end, including pre-registered confirmatory
experiments, final evidence, manuscripts, submission and publication releases. Candidate IDs
(R1/R2…) and venue/year tokens never become repository names. An empty registry is legal; an
empty paper repository is not — no pre-created placeholder repos.

A paper's success criterion is a reproducible, adequately powered verdict on its pre-registered
claim; positive, null and negative results are equally legal completions.

## Current state

One paper project is admitted: **`meeting-minutes-agent`** (2026-08-17, direct owner admission;
authorization record under `wiki/experiments/papers/meeting-minutes-agent/`). The continuation
entry 92 trigger fired with this admission, so `scripts/checks/paper_workspace_check.py` now runs
in admission mode: per-entry schema, name policy, checkout and authorization-record existence,
ignore rule, and control-plane count consistency are machine-enforced; unregistered checkouts
still fail closed. Candidate-bundle and promotion-receipt machinery remains deferred until the
first promotion-path admission. Program-level experiment assets are routed by
[`wiki/Experiment-Assets.md`](../wiki/Experiment-Assets.md).
