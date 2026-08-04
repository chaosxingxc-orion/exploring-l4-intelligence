# Residual gates closure — G0/G1 evidence (2026-08-04)

Closure evidence for the residual gates raised by the independent review
`PROGRAM-DIRECTORY-POST-MIGRATION-INDEPENDENT-REVIEW-2026-08-03`
(`docs/checks/program-architecture/2026-08-03-post-reorg-remediation-independent-review/feedback.md`,
reviewed at umbrella `75406d4` / study `ac75a61`). Since that review the study was renamed and
narrowed to the speech domain (`speech-aware-evidence-acquisition`, owner contract 2026-08-04);
the fixes below were applied on top of that state.

## Gate dispositions

| Gate | Disposition | Where |
|---|---|---|
| G0 model-touch gate accepts fabricated receipts (BLOCKER) | **CLOSED** | study commit `0d86ddc` |
| G1 legacy validator lacks semantic binding (MAJOR) | **CLOSED** | umbrella commit `c9c9f6f` |
| G2 local commits not pushed (RELEASE BLOCKER) | **OPEN — push requires explicit owner authorization**; local closure evidence below | this report |
| G3.1 remediation proposal status | closed: `IMPLEMENTED_WITH_RESIDUAL_GATES` + status banner | umbrella (this commit) |
| G3.2 stale Stage-2A handoff package | closed: `IMPLEMENTED_AND_SUPERSEDED_2026-08-03` banner + routing | umbrella (this commit) |
| G3.3 old check report immutability | honored: `2026-08-03-post-reorg-remediation/report.md` left byte-identical; this new release-scoped directory carries the final outputs | this report |
| G3.4 PEP 639 license metadata | closed: `license = "LicenseRef-Proprietary"`, `license-files`, setuptools>=77 | study commit `0d86ddc` |

## G0 closure — receipts are verified, not trusted

`FrozenCoreGate` now requires versioned schemas with study identity
(`saea-e0-closure-receipt-v1`, `saea-runtime-receipt-v1`); binds D1–D4 to artifact files with
recomputed SHA-256; binds the runtime receipt to the frozen lock key
`qwen3-omni-30b-a3b-instruct-gguf` (canonical `local_subdir`, file count and total bytes from the
umbrella `datasets.lock.json` entry); resolves model files only as relative paths strictly inside
the controlled data root; re-reads every model file and the llama.cpp build binary to recompute
size and SHA-256; and rejects absolute paths, drive letters, `..` traversal, resolved escapes,
duplicates and extra/missing files. The reviewer's counterexample
(`/definitely/does/not/exist/model.gguf` + fabricated 64-hex digest) is now a named negative test.

Rejection evidence (WSL, Python 3.12 speechrl venv):

```text
test_fully_valid_receipts_open_the_gate PASSED
test_gate_refuses_when_receipts_are_missing PASSED
test_gate_refuses_nonexistent_model_file PASSED
test_gate_refuses_fabricated_hash_and_size PASSED
test_gate_refuses_model_byte_drift_on_disk PASSED
test_gate_refuses_absolute_and_traversal_paths[/definitely/does/not/exist/model.gguf] PASSED
test_gate_refuses_absolute_and_traversal_paths[C:/leak/model.gguf] PASSED
test_gate_refuses_absolute_and_traversal_paths[../outside.gguf] PASSED
test_gate_refuses_absolute_and_traversal_paths[models/../../escape.gguf] PASSED
test_gate_refuses_duplicate_and_extra_model_files PASSED
test_gate_refuses_lock_key_mismatch_and_missing_lock_entry PASSED
test_gate_refuses_path_outside_lock_subdir PASSED
test_gate_refuses_unbacked_build_commit PASSED
test_gate_refuses_e0_artifact_hash_drift PASSED
test_gate_refuses_open_deliverable_and_missing_artifact PASSED
test_gate_refuses_schema_or_identity_mismatch PASSED
test_gate_refuses_lock_total_size_mismatch PASSED
25 passed (gate file) / 57 passed (study suite)
```

G0 acceptance matrix: nonexistent path → refused; byte/size drift → refused; lock-key mismatch →
refused; valid E0 + runtime receipts + the frozen model files → allowed.

## G1 closure — bindings are proven, not formatted

Default mode now asserts, per resolved entry, `path == legacy_path_prefix + "/" + repo_path` and
`uri == git+<registered remote>@<commit>#path=<repo_path>` (exact equality). The new offline
`--verify-bundles` mode re-hashes all four registered bundles against
`docs/integrity/retired-repository-registry.json`, clones each into a temporary bare repository,
requires the registered final commit to be contained, and proves
`commit:repo_path -> git_blob` for every entry via `git ls-tree`. No network branch tip is
consulted. `--verify-bundles` is the primary-dev-machine default (client guides).

Real-repo acceptance run (matches the review's expected format):

```text
python scripts/checks/legacy_asset_resolution_check.py --verify-bundles \
    --data-root E:\chao_workspace\exploring-l4-intelligence\speechrl-data

574 bindings verified
0 unresolved
0 waived
4 bundle hashes verified
legacy asset resolution: PASS
```

Fault-injection rejection evidence (`scripts/checks/test_legacy_asset_resolution.py`):

```text
test_bundle_mode_disproves_blob_tampering PASSED            (git_blob = 40 zeros)
test_bundle_mode_rejects_bundle_hash_drift PASSED
test_bundle_mode_rejects_missing_bundle_and_final_commit_absence PASSED
test_bundle_mode_rejects_unreachable_commit PASSED
test_default_mode_rejects_prefix_remote_and_uri_path_tampering PASSED
test_reviewer_combined_injection_is_rejected PASSED         (blob+remote+path together)
test_valid_world_passes_both_modes PASSED
7 passed, 3 subtests passed
```

## Full local acceptance (2026-08-04)

```text
== umbrella (Windows) ==
code graph: PASS (22 trusted nodes)
study workspace and experiment assets: PASS  [--require-installed]
legacy asset resolution: PASS  [--verify-bundles: 574 bindings, 4 bundle hashes]
AI context surface: PASS (0 failures)
AI context manifest: PASS
scripts/checks suite: 143 passed, 2 skipped, 202 subtests passed
== WSL (Python 3.12 speechrl venv) ==
common/tests: 21 passed, 1 skipped
study tests:  57 passed
study build:  sdist + wheel built (PEP 639 metadata); quarantine entries in wheel: 0
uv lock:      resolves; lockfile unchanged
```

## G2 status — pending explicit push authorization

Push is a protected operation; not executed in this transaction. Ready state at report time:
umbrella local HEAD carries T0–T5, the rename transaction, the recorded independent review and
the G0/G1 closures; study local HEAD is `0d86ddc` on top of the rename commit `3f10289`. After
owner authorization: push both repositories, confirm `git ls-remote` branch tips equal the audited
local commits, run the study GitHub CI (`test` + `clean-clone-reproduction`), then create the
final-closure release directory (review F6) recording the two remote commits and CI run IDs —
only that report may claim `R0 engineering foundation ready` eligibility.

Execution rulings unchanged: model-free E0 D1–D4 allowed; first model touch withheld until the
runtime receipts are produced and reviewed; no experiment results claimed.
