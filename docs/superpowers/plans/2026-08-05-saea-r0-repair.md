# SAEA R0 Repair Implementation Plan (trust boundary + run transaction)

> **For agentic workers:** REQUIRED SUB-SKILL: superpowers:subagent-driven-development. Steps use checkbox (`- [ ]`) tracking.

**Goal:** Close every P0/P1 finding of the 2026-08-05 independent review so that the five probes flip ACCEPT→REJECT and a formal run becomes an auditable transaction.

**Design authority:** `docs/superpowers/specs/2026-08-05-saea-r0-repair-trust-boundary-design.md` (invariants I1–I9, probes P1–P5, root causes).

**Method change (root-cause driven):** tasks below specify **invariants + required regression probes + interfaces**, NOT verbatim code. Implementers derive the implementation; reviewers check against the invariants and probe outcomes, not against literal code blocks. Any task whose invariant cannot be met as specified must report BLOCKED with evidence rather than approximate it.

## Global Constraints

- Study repo: `D:\chao_workspace\exploring-l4-intelligence\studies\speech-aware-evidence-acquisition`, branch `r0-repair` (create from master). Commit per task.
- **May modify** `src/.../contracts.py` (gate hardening is in scope this campaign — see spec §2). **Never modify** `src/.../scoring/**`, `src/.../e0/**`, `docs/receipts/*.json`, `docs/exposure-ledger.md`.
- No model touch anywhere in this plan: no llama-server start except the fake-binary tests in T5, no HTTP to a real model, no ledger append.
- No general-audio dataset may be *consumed*; naming `fsd50k`/`audioset-metadata-features`/`esc-50` inside a **denylist constant or a refusal test** is required and allowed (that is the point of the fix) — the governance test that forbids these strings must be updated to allow the denylist/refusal sites and only those.
- Never write raw traces/outputs/data into the repo. Attempt/session state lives under `SPEECHRL_DATA_DIR`.
- Every task ends with: focused tests green, full Windows suite green, and (for tasks touching POSIX behavior) WSL suite green — run WSL FOREGROUND via `wsl.exe -d Ubuntu-24.04 bash /mnt/...helper.sh` from PowerShell.
- Commit messages: `hardening(r0-repair): …` / `feat(r0-repair): …` / `docs(r0-repair): …`, each ending with `Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>`.
- Receipts must still verify after each task: `python -m pytest tests/contract/test_real_receipts.py -q`.

---

### T1 — Split receipt authenticity (invariant I1, probe P2)

**Files:** new `src/.../core/split_receipt.py`; modify `core/driver.py`; tests `tests/unit/test_split_receipt.py`, extend `tests/unit/test_driver.py`.

**Interfaces to produce:**
- `class SplitReceiptError(RuntimeError)`
- `@dataclass(frozen=True) VerifiedSplit`: `name`, `carrier_lock_key`, `split_role`, `ids: tuple[str,...]` (bare ids), `prefixed_ids: tuple[str,...]`, `identity_hash`
- `verify_receipt_document(document: Mapping) -> dict[str, VerifiedSplit]` — strict: `schema == "saea-splits-v1"`; splits key set exactly `{discovery, dev, confirmatory}`; per split: `split_role` matches its name's contract role, `count == len(ids)`, ids sorted + unique + every id prefixed `"{carrier_lock_key}/"`, `identity_hash` recomputed from ids (same convention as `data/splits.py`) equals stored; same-carrier splits pairwise disjoint.
- `load_verified_split(repo_root, split_name, lock, root) -> VerifiedSplit` — verifies the document AND recomputes the split live via `data.splits.discovery_split/dev_split/confirmatory_split`, requiring identical prefixed ids and identity hash; any drift → `SplitReceiptError` naming the split.
- `core/driver.py`: `run_experiment` uses `load_verified_split` (live recomputation included) instead of the current `load_split`; keep the existing plan-hash/role/carrier/protocol checks. `load_split` may remain as a thin wrapper only if it delegates to the verified path.

**Required probes (must FAIL before the fix, PASS after):**
1. dev ids swapped for other real same-carrier ids (take 2 real ids from the confirmatory list) while keeping the stored hash → refused (this is the case the old downstream loader check could NOT catch).
2. stale hash (ids edited, hash kept) → refused. 3. wrong prefix (`conec/…` inside an earnings22 split) → refused. 4. duplicate id → refused. 5. `count` mismatch → refused. 6. wrong `schema` tag → refused. 7. live-recomputation drift (receipt valid internally but ids differ from live loader) → refused.

**Steps:** write the seven refusal tests first (RED), implement, GREEN, full suite, commit.

---

### T2 — Carrier scope + exposure carrier binding (invariant I2, probe P1)

**Files:** modify `src/.../contracts.py`; tests extend `tests/contract/test_exposure_and_gate.py` (or a new `tests/contract/test_carrier_scope.py`).

**Interfaces to produce (in `contracts.py`):**
- `GENERAL_AUDIO_DENY_LOCK_KEYS = frozenset({"fsd50k", "audioset-metadata-features", "esc-50"})`
- `ALLOWED_CARRIER_PROFILES` — derive the allowed set from the umbrella lock's `profiles` field. **First read the real `docs/datasets.lock.json`** and use the actual profile strings for the study's speech carriers (core/secondary/diagnostic/optional as they really appear); a carrier whose lock entry has no `profiles` field fails closed.
- Gate changes in `assert_model_touch_allowed` / `_require_exposure_preregistration`:
  - plan carrier must resolve to a lock **dataset** entry whose profiles intersect `ALLOWED_CARRIER_PROFILES` and whose name is not in the denylist (message must name the study's speech-only scope);
  - the exposure row's carrier column (header cell `speech carrier + split`) must be parsed and must reference `plan.carrier_lock_key` (substring match on the lock key is acceptable, but the check must fail when the row names a different carrier).

**Required probes:** P1 (exposure=earnings21 + plan carrier `fsd50k`) → refused; plan carrier = a lock *model* entry (e.g. the GGUF key) → refused; plan carrier valid but exposure row names a different carrier → refused; the legitimate SAEA row + earnings22 plan → still accepted.

**Note:** update `tests/contract/test_governance_alignment.py` (or whichever test forbids general-audio strings in source) so the denylist constant and its refusal tests are the *only* permitted occurrences.

---

### T3 — Payload↔plan↔split binding and media confinement (invariants I3/I4, probes P3, P5)

**Files:** modify `src/.../core/model.py` (adapter + transport); modify `core/driver.py` (pass the binding context); tests `tests/unit/test_frozen_core_adapter.py`, `tests/unit/test_llama_server_transport.py`.

**Interfaces:** `FrozenCoreAdapter.__init__` gains a binding context (e.g. `allowed_sample_ids: frozenset[str]`, `carrier_root: Path`, `sample_facts: Mapping[str, tuple[float,int]]` mapping sample_id → (audio_seconds, sample_rate_hz), or an equivalent immutable object the driver builds from the verified split + loader). `request()` must additionally enforce:
- `payload["carrier_lock_key"] == plan.carrier_lock_key`;
- `payload["sample_id"] in allowed_sample_ids`;
- `payload["speech_ref"] == f"{plan.carrier_lock_key}/{payload['sample_id']}"`;
- `payload["audio_seconds"]`/`sample_rate_hz` equal the loader facts for that sample;
- `media_relpath` is a normalized POSIX **relative** path (no drive letter, no backslash, no leading `/`, no `..` segment) and `(data_root / media_relpath).resolve(strict=True)` is inside `carrier_root.resolve()` (symlink escape refused).
Transport keeps an independent second rail: refuse absolute/backslash/traversal paths and anything resolving outside its data root.

**Required probes:** P5 (payload carrier ≠ plan carrier) → refused; P3 (absolute media path) → refused at BOTH adapter and transport; sample not in split → refused; forged `speech_ref` → refused; audio_seconds ≠ loader fact → refused; symlink inside data root pointing outside → refused; the legitimate driver path still runs end to end (existing driver tests must stay green — update them to build the binding context).

---

### T4 — One-time attempt accounting (invariant I6, probe P4)

**Files:** modify `src/.../contracts.py` (ExecutionPlan gains `attempt_id`; gate performs atomic reservation), new `src/.../core/attempts.py` (durable attempt store), modify `core/model.py` (usage persisted pre-send), `core/driver.py`; tests new `tests/contract/test_attempt_accounting.py` + adapter tests.

**Design constraints:** attempt state lives OUTSIDE the repo, under `SPEECHRL_DATA_DIR/attempts/<run_id>/<attempt_id>.json`, created with `O_EXCL` (atomic); reopening the same `(run_id, attempt_id)` fails closed; the gate writes `RESERVED→OPENED` and the finalizer (T6) writes `FINALIZED`/`ABORTED`; every request persists actual calls/audio **before** the transport call (append-only, fsync not required but the write must precede the send); a fresh attempt requires a new `attempt_id` and its reserved budget is checked against the ledger row's registration; slice-cap accounting takes the conservative maximum of registered reservations and summed actual usage across attempt files.

**Required probes:** P4 (same run_id+attempt_id opened twice) → second refused; two adapters over the same attempt → second refused (or counters continue from persisted usage, never reset — choose the stricter design and justify it in the report); a new attempt whose actuals would exceed the row registration → refused; a crashed attempt (state OPENED, no finalize) → subsequent open of a NEW attempt still refused unless the previous attempt's persisted actuals are counted; ExecutionPlan without `attempt_id` → refused.

---

### T5 — Runtime session attestation (invariant I5)

**Files:** new `src/.../core/session.py`; modify `core/model.py` (transport requires a session receipt), `core/driver.py` CLI; tests `tests/unit/test_session.py` (+ POSIX-only spawn test using a fake executable script, as `tests/unit/test_e0_generators.py` already does for `llama-server --version`).

**Interfaces:** `class SessionError(RuntimeError)`; `@dataclass(frozen=True) SessionReceipt` binding: binary path + sha256 (must equal the runtime receipt's pinned binary hash), argv, pid, port, host, model/mmproj canonical paths + hashes (from the runtime receipt), start time, startup stdout hash, and `session_id`; `start_session(runtime_root, receipt, host, port, …) -> SessionReceipt` spawning the pinned binary; `attach_session(receipt_path) -> SessionReceipt` for a resident server, valid only if the receipt exists, its binary hash matches the runtime receipt, its pid is alive, and its host is loopback; `require_loopback(base_url)`.

**Required probes:** non-loopback `base_url` (e.g. `http://10.0.0.5:8080` or a public host) → refused; missing session receipt → transport refuses to send; session receipt whose binary hash ≠ runtime receipt → refused; attach to a dead pid → refused; spawn of a binary whose hash ≠ pinned → refused. The spawn test must use a fake shell-script "binary" (POSIX-only, skip on Windows) — **never** the real llama-server.

---

### T6 — Atomic run bundle + finalizer (invariant I7)

**Files:** new `src/.../core/bundle.py` (manifest build/verify), modify `core/driver.py` (write manifest per attempt; `finalize` subcommand), modify `core/scorers.py` (manifest-entry verification), modify `core/tracking.py` (upload raw trace + scores; ledger row derived from the verified manifest only); tests `tests/unit/test_bundle.py`, extend scorer/tracking tests.

**Interfaces:** `run-manifest.json` (schema `saea-run-manifest-v1`) binding: study commit, config fragments + config_hash, protocol_hash, plan (all fields incl. attempt_id), exposure row identity, split identity hash, session receipt hash, outputs path+sha256, raw trace path+sha256, trace manifest sha256, scores path+sha256 (after scoring), actual cost, status (`COMPLETED`/`ABORTED`), and failure reason if any. `verify_bundle(manifest_path) -> VerifiedBundle` recomputing every hash from bytes on disk. `finalize` CLI: verify bundle → run registered scorers → write scores artifact → re-verify → MLflow upload (outputs, raw trace, trace manifest, scores, manifest) → emit machine-generated ledger row (markdown + JSON) → mark attempt FINALIZED.

**Required probes:** outputs text mutated with stale `response_sha256` → scorer/finalizer refuses; outputs sample set ≠ frozen split (missing/extra/duplicate) → refused; trace manifest not matching raw trace → refused; manifest hash mismatch on any artifact → refused; aborted attempt produces an auditable bundle that cannot be finalized as COMPLETED; `ledger_row` rejects hand-supplied cells that conflict with the verified manifest.

---

### T7 — Cost accounting completion (invariant I8)

**Files:** new `src/.../core/resources.py` (sampler), modify `core/model.py`/`core/driver.py`/`core/bundle.py`; tests `tests/unit/test_resources.py`.

**Interfaces:** `ResourceSampler` protocol with an injectable implementation: `NvidiaSmiSampler` (polls `nvidia-smi --query-gpu=utilization.gpu,memory.used --format=csv,noheader` at a fixed interval in a background thread; records gpu_seconds, peak VRAM MiB) and `NullSampler` (records `NOT_AVAILABLE`). Run aggregate must add: `gpu_seconds`, `peak_vram_mib`, `cpu_seconds` (process + children via `os.times()` or `resource`), `supplied_evidence_bytes`, `admitted_evidence_bytes`, `tool_calls`, `gate_setup_seconds`, `failed_attempt_calls`/`failed_attempt_audio_seconds`. Sampling must be model-free testable (inject a fake sampler; never call nvidia-smi in tests).

**Deviation rule:** if a metric genuinely cannot be measured on this machine, the cost record must carry the literal `NOT_AVAILABLE` plus a reason string, and the task report must list it for owner disposition — silent omission is a task failure.

---

### T8 — Formal control configs + scorer seam (invariant I8 partial, P1-3)

**Files:** new `configs/baseline/fixed-legal-context.json`, `configs/baseline/fixed-retrieval.json`, `configs/baseline/mismatched-evidence.json`; modify `core/scorers.py` (register `cost` scorer; entity/QA adapters per the decision below); tests extend `tests/unit/test_config_composition.py`, `tests/unit/test_driver.py` (a fixed-retrieval synthetic driver run), `tests/unit/test_scorers.py`.

**Requirements:** each new baseline fragment composes with the existing model/dataset/experiment fragments (disjoint keys) and drives a synthetic end-to-end run through `run_experiment` with the fake transport; `mismatched-evidence` sets `evidence_mismatch: true`. Register a `cost` scorer that consumes the run manifest's cost block. For entity/QA: attempt an adapter only if the reference layer format can be frozen from data already on disk (`wer_tags`, ConEC contexts); if it cannot be frozen without new owner input, register nothing and instead write `docs/owner-decisions-pending.md` with an explicit scope item — do not fake an adapter.

---

### T9 — CI, lint, documentation alignment (invariant I9, P1-5/P2)

**Files:** `.github/workflows/ci.yml`, `README.md`, `configs/baseline/README.md`, legacy YAML fragments under `configs/`, `docs/engineering.md`, `pyproject.toml` (ruff config if needed).

**Requirements:** replace the pre-R0 clean-clone job with (a) a `contracts` job that installs the package (`uv sync --frozen`) and runs the model-free contract tests plus asserts `reproduce.sh --help` / `evaluate.sh --help` exit 0 and `evaluate.sh` with no args exits 2; (b) a `lint` job running `ruff check` over the active tree with the quarantined W1 snapshot excluded (fix the 4 active-source findings; never reformat the snapshot); (c) keep the test/build job. README: remove deleted package rows, describe `core/`; `configs/baseline/README.md`: JSON, not YAML; reconcile the legacy YAML fragments (either delete them with a note or document them as non-composer legacy) so there is exactly one live config namespace; `docs/engineering.md`: add the repair section. Coverage/type-check remain unconfigured → state `NOT_CONFIGURED` explicitly in the docs, never as "clean".

---

### T10 — Governance record and current-truth correction

**Files (umbrella repo — this task only):** `wiki/Research-Objective.md`, `wiki/experiments/speech-aware-evidence-acquisition/README.md`, new `wiki/audit/speech-aware-evidence-acquisition-r0-review/independent-review-2026-08-05/2026-08-05-implementation-response.md`, plus `docs/integrity/ai-context-manifest.json` rebuild.

**Requirements:** replace every "five adversarial rounds / zero defects" style claim with the accurate form ("internal review waves completed; independent R0 review returned REPAIR; repair campaign <commit> closed P0/P1 with probes P1–P5 flipped, pending fresh independent rereview"); record the accepted verdict, the confirmed findings, the root causes (spec §1), and the owner-decision items (spec §6). Advance the boundary pin only after T1–T9 land. Re-run all six umbrella gates and keep `Research-Objective.md` ≤ 5120 bytes.

---

## Closing gates for the campaign

1. All ten tasks committed with per-task review clean.
2. Five probes flipped ACCEPT→REJECT, each as a permanent test.
3. Windows + WSL full suites green; receipts re-verified; real `reproduce.sh` dry-run still exits 0.
4. A fresh adversarial review run under an **externally derived** threat model (contract promises + external-input trust boundaries), not the implementer's checklist.
5. Fresh-rereview submission package assembled per the independent review §12.
