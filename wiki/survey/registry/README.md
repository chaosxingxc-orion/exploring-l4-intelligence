# Survey paper registry

This directory contains long-lived, metadata-only paper records. Registry rows are append-only;
later decisions supersede an earlier row explicitly rather than deleting historical evidence.

For the bounded Stage-1B campaign, each retained paper record stores canonical identity, arXiv
download links, decision role, normalized speech task and dataset status, method-path terms,
paper-linked repository evidence, PDF hash, and page locators. PDF/e-print bytes, abstracts,
extracted text, and evidence snippets remain under `SPEECHRL_DATA_DIR` and are never Git artifacts.

The registry is evidence storage, not the default survey router and not a novelty verdict. Load it
only for targeted paper verification, coding, experiment selection, or writing. Current stage and
next action remain in `wiki/Research-Objective.md`; executable survey rules remain under
`wiki/survey/current/`.

The first immutable shard is `stage1b-bounded-2026-07-22-papers.jsonl` (159 records). The second
owner-authorized shard is `stage1b-bounded-batch2-2026-07-22-papers.jsonl` (25 disjoint records).
The third owner-authorized shard is `stage1b-bounded-batch3-2026-07-22-papers.jsonl` (21 disjoint
records). The final D0-exhaustion shard is
`stage1b-bounded-batch4-exhaustive-2026-07-22-papers.jsonl` (21 disjoint records). The current
combined view is `views/stage1b-bounded-exhaustive-2026-07-22.json` (226 records; 19 exact local
task-match facets, 45 open transfer records, 126 falsifiers, and 43 instruments). The older
through-batch-3 view remains a replayable historical derivative, not current truth.
Regenerate views with `scripts/survey/sf_stage1b_registry_views.py`; do not hand-edit or duplicate
canonical paper rows across shards.

`stage1b-targeted-anchor-scan-2026-07-24-papers.jsonl` is a separate 24-record, metadata-only
projection of the unsigned targeted-anchor scan RC. It is disjoint from the frozen 226-work registry,
the CURRENT appendix/priority union and the unsigned 14-work capability delta. It is not consumed by
the frozen registry views and is not a Stage-1C input before independent
`SIGN_STAGE1B_TARGETED_ANCHOR_SCAN_RELEASE`. Regenerate and verify this projection only with
`scripts/survey/sf_stage1b_targeted_anchor_scan.py`; do not fold it into a frozen v5 shard.
