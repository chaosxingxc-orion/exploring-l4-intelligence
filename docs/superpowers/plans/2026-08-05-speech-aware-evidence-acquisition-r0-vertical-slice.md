# R0 Engineering Baseline Implementation Plan (speech-aware-evidence-acquisition)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

> Supersedes the same-day 14-task per-experiment layout (git history preserves it). Owner
> direction 2026-08-05: build the **reusable foundation first** (Part 1), then instantiate
> experiments as **configuration** (Part 2); maximize sharing, no fragmentation.

**Goal:** Deliver the R0 engineering baseline of the Stage-2 study as two layers: (Part 1) a single consolidated `core/` foundation package — one generic registry mechanism, one shared experiment driver `run_experiment()`, five abstraction seams (carrier/split, evidence source, transport, scorer, execution policy) — plus the shared data layer (splits freeze, Earnings21 loader, scoring-side references); then (Part 2) config-driven instantiation: the R0 smoke config set, model-free entrypoints, and the smoke runbook. **No model touch is executed by this plan** — every test uses fake transports; the first real call (R0 smoke, `SAEA-E-001`) is a separately-authorized, owner-visible action.

**Architecture:** Anti-fragmentation rules: ONE foundation package (`src/speech_aware_evidence_acquisition/core/`; the four stub packages `models/`, `evidence/`, `tracing/`, `experiments/` are deleted), ONE `Registry` class instantiated five times (CARRIERS, EVIDENCE_SOURCES, TRANSPORTS, POLICIES, SCORERS), ONE driver path used by every Stage-2 run (R0 smoke, R1, X probes, 2B deep digs). An experiment differs from another only by its four JSON config fragments and, rarely, one newly registered component. Deliberately NOT abstracted: `contracts.py` governance (gate, ExecutionPlan, boundary, TraceRecord), the frozen `scoring/` package, and the D2 per-arm visible-field shapes — policies compose on top of the three frozen arm shapes, never add arms. The `Policy` seam is defined now but only the `fixed` policy is implemented (X1 re-resolution, X3 verification loops, X4 reward-guided policies register later without driver changes).

**Tech Stack:** Python 3.12, stdlib-only runtime (JSON configs, `urllib` transport); `mlflow` optional extra imported lazily; pytest 8.

**Design authority:** umbrella `docs/superpowers/specs/2026-08-05-speech-aware-evidence-acquisition-stage2-discovery-slice1-design.md` (§5 lanes, §7 Stage-2 decomposition: this plan is 2A-R0.1 scaffolding + 2A-R0.2 engineering baseline) and `docs/superpowers/specs/2026-08-02-speech-aware-evidence-acquisition-stage2a-entry.md` (R0 deliverables).

## Global Constraints

- Study repo root (all `Files:` paths below are relative to it): `D:\chao_workspace\exploring-l4-intelligence\studies\speech-aware-evidence-acquisition`. Commit each task **in the study repo**; the umbrella repo is not touched by this plan.
- **Frozen scoring package:** never create, edit, or delete anything under `src/speech_aware_evidence_acquisition/scoring/`. Scorer adapters live in `core/scorers.py` and call the frozen stack.
- **Information boundary:** gold / reference / test-annotation / future-turn content never enters a runtime payload. `data/references.py` is scoring-side only; the ONLY module allowed to import it is `core/scorers.py` (AST contract test).
- **No general-audio:** `fsd50k`, `audioset-metadata-features`, `esc-50` never appear in any new source, config, or test.
- **No candidate IDs:** never write `R2` into package/module names or experiment IDs. Experiment namespace is `SAEA-E-<nnn>`.
- **No model touch:** nothing in this plan starts llama-server, sends it a request, or appends a non-model-free row to `docs/exposure-ledger.md`.
- **No committed data:** raw traces/outputs/audio stay under `SPEECHRL_DATA_DIR`; `TraceSink` refuses run directories inside the repo.
- **Split identity hash convention (verified 2026-08-05 against the E0 ledger anchor):** `sha256(("\n".join(sorted(prefixed_ids))).encode("utf-8"))`, each id `f"{lock_key}/{sample_id}"`, no trailing newline; the 213-id full set reproduces `99a896359a504f463a1657281aa71f4a28a51161c804422d8e2f192b0486ad3e`.
- Tests pass on Windows (`pytest` from repo root); POSIX-only behavior uses the existing `skipif(os.name == "nt")` pattern. Python imports stay light at package top level.
- Commit messages: `feat(r0): …` / `test(r0): …` / `docs(r0): …`, each ending with the trailer `Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>`.

---

# Part 1 — Foundation (`core/` + shared data layer)

### Task 1: Lane-A scaffolding — readiness memo template + innovation-candidates ledger

**Files:**
- Create: `docs/readiness/2026-08-05-prior-readiness-memo.md`
- Create: `docs/innovation-candidates.md`

**Interfaces:**
- Consumes: nothing.
- Produces: the per-axis memo skeleton the (separately-run) readiness survey fills; the append-only ledger all future gap memos reference by path `docs/innovation-candidates.md`.

- [ ] **Step 1: Write the readiness memo template**

Create `docs/readiness/2026-08-05-prior-readiness-memo.md`:

```markdown
# Prior readiness memo (per-axis, model-free)

Status: TEMPLATE — filled by the lane-A readiness survey; owner picks the R1
baseline from the completed OVERALL table. No model touch is involved in
filling this memo.

Contract basis: consolidated contract §4 (candidate lines: ConEC/contextual
ASR, RECOVER-style 1-best correction, Siskos entity resolution,
FlexCTC/TurboBias biasing); design spec §5 (per-axis inventory; three outcome
classes). A line that cannot run inside the API-only frozen-core boundary is
recorded as `INCONCLUSIVE_BASELINE_NOT_READY` — that record is itself
structural-gap evidence (design spec §6 source 3) and must be copied into
`docs/innovation-candidates.md`.

## Entry format (one table row per prior line, per axis section)

| field | meaning |
|---|---|
| line | paper/system name + year |
| axis | OBS / ORG / SUPPLY / USE (one primary) |
| runnable revision | exact repo URL + commit, or `NONE` |
| license | license of code + any shipped data |
| boundary compatibility | RUNNABLE_AS_ARM / RUNNABLE_R1_FULL / NOT_READY(reason) |
| scorer alignment | how its reported metric maps onto saea-scoring-v1 |
| visible fields | which D2 arm shape it needs |
| not-runnable reason | exact blocker, or `-` |

## OBS (X1 anchor candidates)

(fill)

## ORG / SUPPLY (X2 anchor candidates)

(fill)

## USE (X3 anchor candidates)

(fill)

## OVERALL — R1 full-protocol candidate ranking

(fill; owner decision recorded here with date)
```

- [ ] **Step 2: Write the innovation-candidates ledger**

Create `docs/innovation-candidates.md`:

```markdown
# Innovation-candidate ledger (append-only)

Every entry is a falsifiable delta claim with evidence pointers. Entries are
never edited or deleted; corrections append a new entry referencing the old
one. Sources (design spec §6): (1) reproduction failure modes from probe gap
memos, (2) the contract's three capability gaps (accessibility,
currency/proper-name, verifiability), (3) structural boundary gaps
(NOT_READY lines from the readiness memo).

Entry format:

## IC-<nnn> <short title> (<YYYY-MM-DD>)

- source: failure-mode | capability-gap | boundary-gap
- axis: OBS | ORG | SUPPLY | USE
- claim: "prior P has failure mode F under our boundary; axis control C removes F"
  (or the capability/boundary-gap analogue)
- null hypothesis: what result would falsify the claim
- evidence: receipt / ledger-row / memo paths
- status: OPEN | PROMOTED_TO_2B | RETIRED

---

(no entries yet)
```

- [ ] **Step 3: Commit**

```bash
git add docs/readiness/2026-08-05-prior-readiness-memo.md docs/innovation-candidates.md
git commit -m "docs(r0): lane-A scaffolding - readiness memo template + innovation-candidate ledger"
```

---

### Task 2: `data/splits.py` — split identity + frozen splits receipt

**Files:**
- Create: `src/speech_aware_evidence_acquisition/data/splits.py`
- Test: `tests/unit/test_splits.py`
- Test: `tests/contract/test_splits_receipt.py`

**Interfaces:**
- Consumes: `data.lock` (`load_lock`, `asset_dir`, `data_root`, `umbrella_lock_path` — follow the module's actual export names, do not rename existing code), `data.loader.load_earnings22/earnings22_subset10_ids`, `e0.artifacts.write_json_artifact`.
- Produces (consumed later by the driver in Task 11):
  - `SPLITS_SCHEMA = "saea-splits-v1"`, `SPLITS_RECEIPT_NAME = "splits.json"`
  - `split_identity_hash(prefixed_ids: Iterable[str]) -> str`
  - `prefixed(lock_key: str, ids: Iterable[str]) -> list[str]` (sorted)
  - `SplitSpec` dataclass: `name`, `carrier_lock_key`, `split_role`, `ids: tuple[str, ...]` (carrier-prefixed, sorted), `identity_hash`, `count` property
  - `discovery_split(lock, root) -> SplitSpec` (earnings21, all), `dev_split(lock, root) -> SplitSpec` (earnings22 subset10), `confirmatory_split(lock, root) -> SplitSpec` (earnings22 minus subset10; **file names only, no annotation content read**)
  - `freeze_splits(lock, root, receipts_dir) -> dict` writing `docs/receipts/splits.json`
  - CLI: `python -m speech_aware_evidence_acquisition.data.splits`

- [ ] **Step 1: Write the failing unit tests**

`tests/unit/test_splits.py`:

```python
"""Split identity: convention stability, membership, and receipt generation."""

import json

from speech_aware_evidence_acquisition.data.lock import load_lock
from speech_aware_evidence_acquisition.data.splits import (
    SPLITS_SCHEMA,
    confirmatory_split,
    dev_split,
    discovery_split,
    freeze_splits,
    prefixed,
    split_identity_hash,
)


def test_split_identity_hash_convention_is_frozen():
    # Known vector: sha256 over LF-joined sorted ids, no trailing newline.
    # Changing the convention breaks comparability with the E0 ledger row and
    # must fail loudly here.
    assert (
        split_identity_hash(["b/2", "a/1"])
        == "8bd12b24d6eb14c9a141597ec482f69a14c9a5024036441d727b4a968e67a33f"
    )


def test_prefixed_uses_lock_key_and_slash():
    assert prefixed("earnings21-original", ["2", "1"]) == [
        "earnings21-original/1",
        "earnings21-original/2",
    ]


def test_splits_partition_the_carriers(synthetic_world):
    lock = load_lock(synthetic_world.lock_path)
    root = synthetic_world.data_root
    disc = discovery_split(lock, root)
    dev = dev_split(lock, root)
    conf = confirmatory_split(lock, root)
    # Synthetic world (tests/unit/conftest.py): 3 e21 samples, 12 e22, subset10 = 10.
    assert disc.carrier_lock_key == "earnings21-original"
    assert disc.split_role == "discovery"
    assert disc.count == 3
    assert dev.split_role == "dev"
    assert dev.count == 10
    assert conf.split_role == "confirmatory"
    assert conf.count == 2
    assert all(i.startswith("earnings22-original/") for i in dev.ids + conf.ids)
    assert set(dev.ids).isdisjoint(conf.ids)
    assert disc.identity_hash == split_identity_hash(disc.ids)


def test_freeze_splits_writes_receipt(synthetic_world, tmp_path):
    lock = load_lock(synthetic_world.lock_path)
    receipts = tmp_path / "receipts"
    document = freeze_splits(lock, synthetic_world.data_root, receipts)
    on_disk = json.loads((receipts / "splits.json").read_text(encoding="utf-8"))
    assert on_disk == document
    assert document["schema"] == SPLITS_SCHEMA
    assert set(document["splits"]) == {"discovery", "dev", "confirmatory"}
    for split in document["splits"].values():
        assert split["identity_hash"] == split_identity_hash(split["ids"])
```

`tests/contract/test_splits_receipt.py`:

```python
"""Contract: the committed splits receipt (once frozen) is internally coherent."""

import json
from pathlib import Path

import pytest

from speech_aware_evidence_acquisition.data.splits import (
    SPLITS_SCHEMA,
    split_identity_hash,
)

RECEIPT = Path(__file__).resolve().parents[2] / "docs" / "receipts" / "splits.json"


@pytest.mark.skipif(not RECEIPT.is_file(), reason="splits not frozen yet")
def test_committed_splits_receipt_is_coherent():
    document = json.loads(RECEIPT.read_text(encoding="utf-8"))
    assert document["schema"] == SPLITS_SCHEMA
    splits = document["splits"]
    assert set(splits) == {"discovery", "dev", "confirmatory"}
    for name, split in splits.items():
        assert split["ids"] == sorted(split["ids"]), name
        assert split["identity_hash"] == split_identity_hash(split["ids"]), name
    assert splits["dev"]["count"] == 10
    assert set(splits["dev"]["ids"]).isdisjoint(splits["confirmatory"]["ids"])
    assert splits["discovery"]["split_role"] == "discovery"
    assert splits["confirmatory"]["split_role"] == "confirmatory"
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/unit/test_splits.py -v`
Expected: FAIL with `ModuleNotFoundError: ... data.splits`

- [ ] **Step 3: Implement `data/splits.py`**

```python
"""Split identity and the frozen discovery/dev/confirmatory partition (R0).

Convention (matches the E0 ledger row SAEA-E0-CLOSURE-2026-08-04 exactly):
a split's identity hash is SHA-256 over the LF-joined sorted list of
carrier-prefixed sample ids ``f"{lock_key}/{sample_id}"`` with no trailing
newline. The confirmatory split is enumerated from media file names only —
no annotation content is read here.
"""

from __future__ import annotations

import hashlib
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping

from ..e0.artifacts import write_json_artifact
from .loader import LoaderError, earnings22_subset10_ids, load_earnings22
from .lock import asset_dir, data_root, load_lock, umbrella_lock_path

SPLITS_SCHEMA = "saea-splits-v1"
SPLITS_RECEIPT_NAME = "splits.json"
_CONVENTION = (
    "sha256 over LF-joined sorted carrier-prefixed sample ids "
    "(f'{lock_key}/{sample_id}', UTF-8, no trailing newline)"
)


def split_identity_hash(prefixed_ids: Iterable[str]) -> str:
    return hashlib.sha256("\n".join(sorted(prefixed_ids)).encode("utf-8")).hexdigest()


def prefixed(lock_key: str, ids: Iterable[str]) -> list[str]:
    return sorted(f"{lock_key}/{sample_id}" for sample_id in ids)


@dataclass(frozen=True)
class SplitSpec:
    name: str
    carrier_lock_key: str
    split_role: str
    ids: tuple[str, ...]
    identity_hash: str

    @property
    def count(self) -> int:
        return len(self.ids)


def _spec(name: str, lock_key: str, role: str, raw_ids: Iterable[str]) -> SplitSpec:
    ids = tuple(prefixed(lock_key, raw_ids))
    if not ids:
        raise LoaderError(f"split {name!r} resolved to zero samples")
    return SplitSpec(
        name=name,
        carrier_lock_key=lock_key,
        split_role=role,
        ids=ids,
        identity_hash=split_identity_hash(ids),
    )


def discovery_split(lock: Mapping[str, object], root: Path) -> SplitSpec:
    media_dir = asset_dir(lock, "earnings21-original", root) / "media"
    if not media_dir.is_dir():
        raise LoaderError(f"earnings21 media directory missing: {media_dir}")
    ids = [
        path.name[: -len(".mp3")]
        for path in media_dir.glob("*.mp3")
        if path.is_file()
    ]
    return _spec("discovery", "earnings21-original", "discovery", ids)


def dev_split(lock: Mapping[str, object], root: Path) -> SplitSpec:
    return _spec(
        "dev", "earnings22-original", "dev", earnings22_subset10_ids(lock, root)
    )


def confirmatory_split(lock: Mapping[str, object], root: Path) -> SplitSpec:
    all_ids = {sample.sample_id for sample in load_earnings22(lock, root)}
    subset10 = set(earnings22_subset10_ids(lock, root))
    if not subset10 <= all_ids:
        raise LoaderError("subset10 is not a subset of earnings22 media identity")
    return _spec(
        "confirmatory", "earnings22-original", "confirmatory", all_ids - subset10
    )


def freeze_splits(
    lock: Mapping[str, object], root: Path, receipts_dir: Path
) -> dict[str, object]:
    splits = {
        spec.name: {
            "carrier_lock_key": spec.carrier_lock_key,
            "split_role": spec.split_role,
            "count": spec.count,
            "ids": list(spec.ids),
            "identity_hash": spec.identity_hash,
        }
        for spec in (
            discovery_split(lock, root),
            dev_split(lock, root),
            confirmatory_split(lock, root),
        )
    }
    document: dict[str, object] = {
        "schema": SPLITS_SCHEMA,
        "convention": _CONVENTION,
        "splits": splits,
        "note": (
            "confirmatory ids are enumerated from media file names only and "
            "remain unread; any confirmatory result read requires Stage-3 "
            "authority or a dated owner allowance (consolidated contract §7)"
        ),
    }
    write_json_artifact(Path(receipts_dir) / SPLITS_RECEIPT_NAME, document)
    return document


def main() -> int:
    lock = load_lock(umbrella_lock_path())
    root = data_root()
    receipts = Path(__file__).resolve().parents[3] / "docs" / "receipts"
    document = freeze_splits(lock, root, receipts)
    for name, split in document["splits"].items():
        print(f"{name}: {split['count']} samples, {split['identity_hash']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/unit/test_splits.py tests/contract/test_splits_receipt.py -v`
Expected: unit PASS; contract SKIPPED (receipt not frozen yet). If the known-vector assertion mismatches, recompute the constant from the implementation and fix **the test constant**, never the convention.

- [ ] **Step 5: Freeze the real splits receipt (model-free, dev machine)**

```powershell
$env:SPEECHRL_DATA_DIR = "E:\chao_workspace\exploring-l4-intelligence\speechrl-data"
python -m speech_aware_evidence_acquisition.data.splits
```

Expected: `discovery: 44 …` / `dev: 10 …` / `confirmatory: 115 …`; `docs/receipts/splits.json` created. Re-run `pytest tests/contract/test_splits_receipt.py -v` — now PASS.

- [ ] **Step 6: Commit**

```bash
git add src/speech_aware_evidence_acquisition/data/splits.py tests/unit/test_splits.py tests/contract/test_splits_receipt.py docs/receipts/splits.json
git commit -m "feat(r0): split identity + frozen discovery/dev/confirmatory receipt"
```

---

### Task 3: Data layer completion — `load_earnings21` + scoring-side `references.py`

**Files:**
- Modify: `src/speech_aware_evidence_acquisition/data/loader.py` (append after `load_earnings22`)
- Create: `src/speech_aware_evidence_acquisition/data/references.py`
- Test: `tests/unit/test_identity_and_loader.py` (append), `tests/unit/test_references.py`

**Interfaces:**
- Consumes: existing `_metadata_rows`, `_float_field`, `SampleRef`, `lock_entry`, `asset_dir`.
- Produces:
  - `load_earnings21(lock, root) -> list[SampleRef]` — metadata CSV `earnings21-file-metadata.csv`, columns `file_id`/`audio_length`/`sample_rate`; identity-drift fail-closed.
  - `references.ReferenceError(RuntimeError)`; `references.reference_tokens(lock, root, carrier_lock_key, sample_id) -> list[str]` — raw tokens from the carrier's pipe-delimited `.nlp` file (header-driven, requires a `token` column). Only `core/scorers.py` may import this module.

- [ ] **Step 1: Write the failing loader tests** (append to `tests/unit/test_identity_and_loader.py`)

```python
def test_load_earnings21_returns_identity_checked_samples(synthetic_world):
    from speech_aware_evidence_acquisition.data.loader import load_earnings21
    from speech_aware_evidence_acquisition.data.lock import load_lock

    lock = load_lock(synthetic_world.lock_path)
    samples = load_earnings21(lock, synthetic_world.data_root)
    assert [s.sample_id for s in samples] == sorted(s.sample_id for s in samples)
    assert len(samples) == 3
    first = samples[0]
    assert first.carrier_lock_key == "earnings21-original"
    assert first.media_relpath.endswith(f"media/{first.sample_id}.mp3")
    assert first.audio_seconds == 100.5
    assert first.sample_rate_hz == 16000
    assert first.runtime_view()["speech_ref"] == f"earnings21-original/{first.sample_id}"


def test_load_earnings21_fails_closed_on_identity_drift(synthetic_world):
    import pytest

    from speech_aware_evidence_acquisition.data.loader import LoaderError, load_earnings21
    from speech_aware_evidence_acquisition.data.lock import load_lock

    (synthetic_world.e21 / "media" / "9999999.mp3").write_text("orphan", encoding="utf-8")
    lock = load_lock(synthetic_world.lock_path)
    with pytest.raises(LoaderError, match="identity drift"):
        load_earnings21(lock, synthetic_world.data_root)
```

- [ ] **Step 2: Write the failing references tests**

`tests/unit/test_references.py`:

```python
"""Scoring-side reference reading (never imported by runtime-phase modules)."""

import pytest

from speech_aware_evidence_acquisition.data.lock import load_lock
from speech_aware_evidence_acquisition.data.references import (
    ReferenceError,
    reference_tokens,
)


def test_reads_tokens_from_nlp_header(synthetic_world):
    nlp = synthetic_world.e21 / "transcripts" / "nlp_references" / "4000001.nlp"
    nlp.write_text("token|speaker|tags\nhello|A|\nworld|A|\n", encoding="utf-8")
    lock = load_lock(synthetic_world.lock_path)
    tokens = reference_tokens(
        lock, synthetic_world.data_root, "earnings21-original", "4000001"
    )
    assert tokens == ["hello", "world"]


def test_missing_token_column_fails_closed(synthetic_world):
    nlp = synthetic_world.e21 / "transcripts" / "nlp_references" / "4000001.nlp"
    nlp.write_text("word|speaker\nhello|A\n", encoding="utf-8")
    lock = load_lock(synthetic_world.lock_path)
    with pytest.raises(ReferenceError, match="token"):
        reference_tokens(
            lock, synthetic_world.data_root, "earnings21-original", "4000001"
        )


def test_unknown_carrier_fails_closed(synthetic_world):
    lock = load_lock(synthetic_world.lock_path)
    with pytest.raises(ReferenceError, match="carrier"):
        reference_tokens(lock, synthetic_world.data_root, "conec", "4000001")
```

- [ ] **Step 3: Run tests to verify they fail**

Run: `pytest tests/unit/test_identity_and_loader.py -k earnings21 tests/unit/test_references.py -v`
Expected: FAIL (`ImportError` / `ModuleNotFoundError`)

- [ ] **Step 4: Implement both**

Append to `loader.py` (mirror of `load_earnings22`):

```python
def load_earnings21(lock: Mapping[str, object], root: Path) -> list[SampleRef]:
    """All Earnings21 samples, sorted by sample id, identity-checked against media."""

    entry = lock_entry(lock, "earnings21-original")
    carrier_dir = asset_dir(lock, "earnings21-original", root)
    subdir = str(entry["local_subdir"]).rstrip("/")
    rows = _metadata_rows(carrier_dir / "earnings21-file-metadata.csv", "file_id")
    media_dir = carrier_dir / "media"
    media_ids = {
        path.name[: -len(".mp3")] for path in media_dir.glob("*.mp3") if path.is_file()
    }
    if media_ids != set(rows):
        raise LoaderError(
            "earnings21 media/metadata identity drift: "
            f"media_only={sorted(media_ids - set(rows))[:5]} "
            f"metadata_only={sorted(set(rows) - media_ids)[:5]}"
        )
    samples = []
    for sample_id in sorted(rows):
        row = rows[sample_id]
        samples.append(
            SampleRef(
                carrier_lock_key="earnings21-original",
                sample_id=sample_id,
                media_relpath=f"{subdir}/media/{sample_id}.mp3",
                audio_seconds=_float_field(row, "audio_length", sample_id),
                sample_rate_hz=int(_float_field(row, "sample_rate", sample_id)),
            )
        )
    return samples
```

Before finalizing, verify the real CSV header once (`Get-Content E:\chao_workspace\exploring-l4-intelligence\speechrl-data\datasets\earnings21-22\earnings21\earnings21-file-metadata.csv -TotalCount 1`); the synthetic world mirrors the real layout — if the real header differs, fix **both** conftest and this function in this task.

Create `data/references.py`:

```python
"""Scoring-side reference access. RUNTIME-FORBIDDEN.

Reads reference transcript tokens for offline scoring only. The ONLY module
allowed to import this is core/scorers.py — an AST contract test enforces
that. References never cross the runtime boundary; they meet the hypothesis
only inside the scoring phase.
"""

from __future__ import annotations

from pathlib import Path
from typing import Mapping

from .lock import asset_dir


class ReferenceError(RuntimeError):
    """A reference layer is missing, malformed, or requested for an unknown carrier."""


_NLP_SUBDIR = {
    "earnings21-original": Path("transcripts") / "nlp_references",
    "earnings22-original": Path("transcripts") / "nlp_references",
}


def reference_tokens(
    lock: Mapping[str, object], root: Path, carrier_lock_key: str, sample_id: str
) -> list[str]:
    subdir = _NLP_SUBDIR.get(carrier_lock_key)
    if subdir is None:
        raise ReferenceError(f"no reference layer registered for carrier {carrier_lock_key!r}")
    path = asset_dir(lock, carrier_lock_key, root) / subdir / f"{sample_id}.nlp"
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError) as error:
        raise ReferenceError(f"cannot read reference {path}: {error}") from error
    if not lines:
        raise ReferenceError(f"reference {path} is empty")
    header = lines[0].split("|")
    if "token" not in header:
        raise ReferenceError(f"reference {path} lacks a 'token' column: {header}")
    column = header.index("token")
    tokens: list[str] = []
    for number, line in enumerate(lines[1:], start=2):
        if not line.strip():
            continue
        cells = line.split("|")
        if len(cells) <= column:
            raise ReferenceError(f"reference {path}: malformed line {number}")
        tokens.append(cells[column])
    if not tokens:
        raise ReferenceError(f"reference {path} has no token rows")
    return tokens
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `pytest tests/unit/test_identity_and_loader.py tests/unit/test_references.py -v`
Expected: PASS

- [ ] **Step 6: Commit**

```bash
git add src/speech_aware_evidence_acquisition/data/loader.py src/speech_aware_evidence_acquisition/data/references.py tests/unit/test_identity_and_loader.py tests/unit/test_references.py
git commit -m "feat(r0): earnings21 loader + scoring-side reference reader"
```

---

### Task 4: `core/base.py` — the ONE registry mechanism + shared types

**Files:**
- Create: `src/speech_aware_evidence_acquisition/core/__init__.py` (minimal for now; finalized in Task 12)
- Create: `src/speech_aware_evidence_acquisition/core/base.py`
- Test: `tests/unit/test_core_base.py`

**Interfaces:**
- Consumes: `contracts.assert_information_boundary`.
- Produces (every later task consumes these — this file is the single import root for the seams):
  - `class CoreError(RuntimeError)`
  - `class Registry`: `__init__(kind: str)`, `register(name: str, entry) -> entry` (refuses blank/duplicate names), `resolve(name: str)` (fail-closed with the sorted known names), `names() -> list[str]`
  - The five registry instances: `CARRIERS` (name = carrier lock key → loader callable `(lock, root) -> list[SampleRef]`), `EVIDENCE_SOURCES` (name → callable `(lock, root, sample_id) -> list[EvidenceItem]`), `TRANSPORTS` (name → factory `(config_values: Mapping, data_root: Path) -> Callable[[bytes], bytes]`), `POLICIES` (name → policy instance with `run_sample(ctx) -> SampleOutcome`), `SCORERS` (name → callable `(outputs_path, lock, root) -> dict`)
  - `@dataclass(frozen=True) EvidenceItem`: `evidence_id`, `source_uri`, `content`, `provenance: Mapping[str, str]` (required keys `lock_key`/`relpath`/`sha256`); `validate()`, `runtime_view()`, `provenance_view()`; `class EvidenceError(RuntimeError)`
  - `@dataclass(frozen=True) SampleOutcome`: `sample_id: str`, `request_ids: tuple[str, ...]`, `text: str`, `admitted: bool`, `request_sha256: str`, `response_sha256: str`
  - `@dataclass(frozen=True) RunResult`: `run_id: str`, `arm: str`, `outputs_path: Path`, `trace_manifest_hash: str`, `cost: Mapping[str, object]`
  - `@dataclass SampleContext` (mutable is fine): `sample`, `evidence: list[EvidenceItem]`, `adapter`, `sink`, `arm: str`, `task_instruction: str`, `decoding_params: Mapping[str, object]`, `request_id_base: str`, `retrieval_query: str | None`

- [ ] **Step 1: Write the failing tests**

`tests/unit/test_core_base.py`:

```python
"""One registry mechanism; boundary-safe evidence items."""

import pytest

from speech_aware_evidence_acquisition.contracts import BoundaryViolation
from speech_aware_evidence_acquisition.core.base import (
    CoreError,
    EvidenceError,
    EvidenceItem,
    Registry,
)


def test_registry_registers_resolves_and_fails_closed():
    registry = Registry("widget")
    registry.register("a", 1)
    assert registry.resolve("a") == 1
    assert registry.names() == ["a"]
    with pytest.raises(CoreError, match="duplicate"):
        registry.register("a", 2)
    with pytest.raises(CoreError, match="blank"):
        registry.register("", 3)
    with pytest.raises(CoreError, match="unknown widget 'zz'"):
        registry.resolve("zz")


def _item(provenance=None):
    return EvidenceItem(
        evidence_id="ev-1",
        source_uri="conec://earnings21/contexts/4000001.txt",
        content="context text",
        provenance=provenance
        or {"lock_key": "conec", "relpath": "earnings21/contexts/4000001.txt", "sha256": "0" * 64},
    )


def test_evidence_item_validates_and_projects_views():
    item = _item().validate()
    assert set(item.runtime_view()) == {"evidence_id", "source_uri", "content"}
    assert set(item.provenance_view()) == {"lock_key", "relpath", "sha256"}


def test_evidence_item_refuses_missing_provenance_keys():
    with pytest.raises(EvidenceError, match="provenance"):
        _item(provenance={"lock_key": "conec"}).validate()


def test_evidence_item_refuses_forbidden_field_smuggling():
    bad = _item(
        provenance={"lock_key": "conec", "relpath": "r", "sha256": "0" * 64, "reference": "x"}
    )
    with pytest.raises(BoundaryViolation):
        bad.validate()
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/unit/test_core_base.py -v`
Expected: FAIL with `ModuleNotFoundError`

- [ ] **Step 3: Implement `core/base.py`** (and a placeholder `core/__init__.py` containing only a docstring `"""Shared Stage-2 engineering foundation (R0)."""`)

```python
"""Foundation seams: ONE registry mechanism + shared value types (R0).

Anti-fragmentation contract (owner direction 2026-08-05): every pluggable
dimension of a Stage-2 experiment — carrier, evidence source, transport,
policy, scorer — registers here through the same Registry class, and every
run flows through core.driver.run_experiment(). A new experiment is config
plus at most one newly registered component, never new wiring.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Mapping

from ..contracts import assert_information_boundary


class CoreError(RuntimeError):
    """A foundation seam refuses: unknown/duplicate registration or wiring misuse."""


class Registry:
    def __init__(self, kind: str) -> None:
        self._kind = kind
        self._entries: dict[str, object] = {}

    def register(self, name: str, entry: object) -> object:
        if not isinstance(name, str) or not name.strip():
            raise CoreError(f"{self._kind} registry: blank name")
        if name in self._entries:
            raise CoreError(f"{self._kind} registry: duplicate name {name!r}")
        self._entries[name] = entry
        return entry

    def resolve(self, name: str) -> object:
        try:
            return self._entries[name]
        except KeyError:
            raise CoreError(
                f"unknown {self._kind} {name!r}; registered: {self.names()}"
            ) from None

    def names(self) -> list[str]:
        return sorted(self._entries)


CARRIERS = Registry("carrier")
EVIDENCE_SOURCES = Registry("evidence source")
TRANSPORTS = Registry("transport")
POLICIES = Registry("policy")
SCORERS = Registry("scorer")

_REQUIRED_PROVENANCE = ("lock_key", "relpath", "sha256")


class EvidenceError(RuntimeError):
    """An evidence item is malformed or an evidence source is unavailable."""


@dataclass(frozen=True)
class EvidenceItem:
    evidence_id: str
    source_uri: str
    content: str
    provenance: Mapping[str, str]

    def validate(self) -> "EvidenceItem":
        for label, value in (
            ("evidence_id", self.evidence_id),
            ("source_uri", self.source_uri),
            ("content", self.content),
        ):
            if not isinstance(value, str) or not value:
                raise EvidenceError(f"evidence {label} must be a non-empty string")
        if not isinstance(self.provenance, Mapping):
            raise EvidenceError("evidence provenance must be a mapping")
        missing = [key for key in _REQUIRED_PROVENANCE if key not in self.provenance]
        if missing:
            raise EvidenceError(f"evidence provenance lacks required keys {missing}")
        assert_information_boundary(self.runtime_view())
        assert_information_boundary(dict(self.provenance))
        return self

    def runtime_view(self) -> dict[str, object]:
        return {
            "evidence_id": self.evidence_id,
            "source_uri": self.source_uri,
            "content": self.content,
        }

    def provenance_view(self) -> dict[str, object]:
        return dict(self.provenance)


@dataclass(frozen=True)
class SampleOutcome:
    sample_id: str
    request_ids: tuple[str, ...]
    text: str
    admitted: bool
    request_sha256: str
    response_sha256: str


@dataclass(frozen=True)
class RunResult:
    run_id: str
    arm: str
    outputs_path: Path
    trace_manifest_hash: str
    cost: Mapping[str, object]


@dataclass
class SampleContext:
    sample: object
    evidence: list[EvidenceItem]
    adapter: object
    sink: object
    arm: str
    task_instruction: str
    decoding_params: Mapping[str, object]
    request_id_base: str
    retrieval_query: str | None = None
    extras: dict[str, object] = field(default_factory=dict)
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/unit/test_core_base.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/speech_aware_evidence_acquisition/core tests/unit/test_core_base.py
git commit -m "feat(r0): core foundation - single registry mechanism + shared value types"
```

---

### Task 5: `core/tracing.py` — append-only four-axis trace sink

**Files:**
- Create: `src/speech_aware_evidence_acquisition/core/tracing.py`
- Test: `tests/unit/test_trace_sink.py`

**Interfaces:**
- Consumes: `contracts.TraceRecord`, `e0.artifacts.REPO_ROOT/write_json_artifact`.
- Produces:
  - `class TraceSinkError(RuntimeError)`
  - `class TraceSink`: `__init__(run_dir: Path, run_id: str)` — creates `run_dir`; **refuses any `run_dir` inside the repo**; property `run_id`; `emit(channel, record_id, payload) -> str` (content hash; refuses duplicate ids and post-close emits); `manifest() -> dict[str, str]` (insertion-ordered); `close() -> str` (writes `<run_id>.trace-manifest.json`, returns its file hash).

- [ ] **Step 1: Write the failing tests**

`tests/unit/test_trace_sink.py`:

```python
"""Trace sink: append-only JSONL, hash manifest, repo-refusal, close semantics."""

import json

import pytest

from speech_aware_evidence_acquisition.contracts import TraceContractError
from speech_aware_evidence_acquisition.e0.artifacts import REPO_ROOT
from speech_aware_evidence_acquisition.core.tracing import TraceSink, TraceSinkError


def test_emit_appends_validated_lines_and_manifest(tmp_path):
    sink = TraceSink(tmp_path / "run", "SAEA-E-000-test")
    assert sink.run_id == "SAEA-E-000-test"
    h1 = sink.emit("OBS", "s1/obs", {"obs_speech_ref": "earnings21-original/1"})
    h2 = sink.emit("COST", "s1/cost", {"calls": 1, "latency_seconds": 0.5})
    lines = (tmp_path / "run" / "SAEA-E-000-test.trace.jsonl").read_text(
        encoding="utf-8"
    ).splitlines()
    assert len(lines) == 2
    assert json.loads(lines[0])["channel"] == "OBS"
    assert sink.manifest() == {"s1/obs": h1, "s1/cost": h2}


def test_axis_prefix_violations_propagate(tmp_path):
    sink = TraceSink(tmp_path / "run", "SAEA-E-000-test")
    with pytest.raises(TraceContractError):
        sink.emit("OBS", "bad", {"supply_evidence": "smuggled"})


def test_duplicate_record_id_refused(tmp_path):
    sink = TraceSink(tmp_path / "run", "SAEA-E-000-test")
    sink.emit("OBS", "dup", {"obs_x": 1})
    with pytest.raises(TraceSinkError, match="duplicate"):
        sink.emit("OBS", "dup", {"obs_x": 2})


def test_run_dir_inside_repo_refused():
    with pytest.raises(TraceSinkError, match="repository"):
        TraceSink(REPO_ROOT / "docs" / "sneaky-run", "SAEA-E-000-test")


def test_close_writes_manifest_and_freezes(tmp_path):
    sink = TraceSink(tmp_path / "run", "SAEA-E-000-test")
    sink.emit("OBS", "s1/obs", {"obs_x": 1})
    manifest_hash = sink.close()
    assert len(manifest_hash) == 64
    document = json.loads(
        (tmp_path / "run" / "SAEA-E-000-test.trace-manifest.json").read_text("utf-8")
    )
    assert document["records"] == sink.manifest()
    with pytest.raises(TraceSinkError, match="closed"):
        sink.emit("OBS", "s2/obs", {"obs_x": 2})
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/unit/test_trace_sink.py -v`
Expected: FAIL with `ModuleNotFoundError`

- [ ] **Step 3: Implement `core/tracing.py`**

```python
"""Append-only four-axis trace sink writing outside the repository (R0)."""

from __future__ import annotations

from pathlib import Path
from typing import Mapping

from ..contracts import TraceRecord
from ..e0.artifacts import REPO_ROOT, write_json_artifact


class TraceSinkError(RuntimeError):
    """The sink refuses: bad run directory, duplicate record id, or closed sink."""


class TraceSink:
    def __init__(self, run_dir: Path, run_id: str) -> None:
        run_dir = Path(run_dir)
        resolved = run_dir.resolve()
        if resolved == REPO_ROOT or REPO_ROOT in resolved.parents:
            raise TraceSinkError(
                f"trace run directory {resolved} is inside the repository; raw "
                "traces are never committed (study contract) — use SPEECHRL_DATA_DIR"
            )
        if not run_id or "/" in run_id or "\\" in run_id:
            raise TraceSinkError(f"invalid run id {run_id!r}")
        run_dir.mkdir(parents=True, exist_ok=True)
        self._run_dir = run_dir
        self._run_id = run_id
        self._path = run_dir / f"{run_id}.trace.jsonl"
        self._hashes: dict[str, str] = {}
        self._closed = False

    @property
    def run_id(self) -> str:
        return self._run_id

    def emit(self, channel: str, record_id: str, payload: Mapping[str, object]) -> str:
        if self._closed:
            raise TraceSinkError("sink is closed")
        if record_id in self._hashes:
            raise TraceSinkError(f"duplicate trace record id {record_id!r}")
        record = TraceRecord(channel=channel, record_id=record_id, payload=payload)
        line = record.serialize()
        digest = record.content_hash()
        with self._path.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write(line + "\n")
        self._hashes[record_id] = digest
        return digest

    def manifest(self) -> dict[str, str]:
        return dict(self._hashes)

    def close(self) -> str:
        self._closed = True
        return write_json_artifact(
            self._run_dir / f"{self._run_id}.trace-manifest.json",
            {"run_id": self._run_id, "records": self.manifest()},
        )
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/unit/test_trace_sink.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/speech_aware_evidence_acquisition/core/tracing.py tests/unit/test_trace_sink.py
git commit -m "feat(r0): append-only four-axis trace sink with repo refusal"
```

---

### Task 6: `core/carriers.py` + `core/evidence.py` — registered data components

**Files:**
- Create: `src/speech_aware_evidence_acquisition/core/carriers.py`
- Create: `src/speech_aware_evidence_acquisition/core/evidence.py`
- Test: `tests/unit/test_core_components.py`

**Interfaces:**
- Consumes: `core.base` registries + `EvidenceItem`, `data.loader.load_earnings21/load_earnings22`, `data.lock.asset_dir`, `e0.artifacts.sha256_file`.
- Produces (all via registries — no direct imports needed downstream):
  - `CARRIERS`: `"earnings21-original"` → `load_earnings21`, `"earnings22-original"` → `load_earnings22`
  - `EVIDENCE_SOURCES`: `"none"` → returns `[]`; `"conec-contexts"` → the ConEC supplementary context for one Earnings21 call (`earnings21/contexts/<id>.txt`, fail-closed if absent)
  - `rotated_mismatch(evidence_by_sample: Mapping[str, list[EvidenceItem]]) -> dict[str, list[EvidenceItem]]` — deterministic derangement decorator over ANY source's table (each sample gets the next sorted sample's evidence; requires ≥2 samples). Exported as a function (the driver applies it on a config flag), NOT a separate source per base source — that is the anti-fragmentation move.
  - `class OracleEvidenceError(RuntimeError)`; `EVIDENCE_SOURCES` name `"oracle"` → callable that **always raises** `OracleEvidenceError` (the oracle upper bound is scoring-side analysis; it never enters a runtime arm; its computation is specified with the probe that first uses it).

- [ ] **Step 1: Write the failing tests**

`tests/unit/test_core_components.py`:

```python
"""Registered carriers and evidence sources resolve through the ONE registry."""

import pytest

from speech_aware_evidence_acquisition.core import carriers, evidence  # noqa: F401 (registration)
from speech_aware_evidence_acquisition.core.base import (
    CARRIERS,
    EVIDENCE_SOURCES,
    EvidenceError,
    EvidenceItem,
)
from speech_aware_evidence_acquisition.core.evidence import (
    OracleEvidenceError,
    rotated_mismatch,
)
from speech_aware_evidence_acquisition.data.lock import load_lock


def test_carriers_are_registered_and_load(synthetic_world):
    lock = load_lock(synthetic_world.lock_path)
    e21 = CARRIERS.resolve("earnings21-original")(lock, synthetic_world.data_root)
    e22 = CARRIERS.resolve("earnings22-original")(lock, synthetic_world.data_root)
    assert len(e21) == 3 and len(e22) == 12


def test_none_source_returns_empty(synthetic_world):
    lock = load_lock(synthetic_world.lock_path)
    assert EVIDENCE_SOURCES.resolve("none")(lock, synthetic_world.data_root, "x") == []


def test_conec_source_loads_and_hashes(synthetic_world):
    lock = load_lock(synthetic_world.lock_path)
    items = EVIDENCE_SOURCES.resolve("conec-contexts")(
        lock, synthetic_world.data_root, "4000001"
    )
    assert len(items) == 1
    assert items[0].content == "ctx"
    assert items[0].provenance["lock_key"] == "conec"
    assert len(items[0].provenance["sha256"]) == 64


def test_conec_source_fails_closed_when_missing(synthetic_world):
    lock = load_lock(synthetic_world.lock_path)
    with pytest.raises(EvidenceError, match="missing"):
        EVIDENCE_SOURCES.resolve("conec-contexts")(
            lock, synthetic_world.data_root, "0000000"
        )


def _item(evidence_id):
    return EvidenceItem(
        evidence_id=evidence_id, source_uri="u://x", content=evidence_id,
        provenance={"lock_key": "conec", "relpath": "r", "sha256": "0" * 64},
    )


def test_rotated_mismatch_is_a_derangement():
    table = {"a": [_item("ev-a")], "b": [_item("ev-b")], "c": [_item("ev-c")]}
    rotated = rotated_mismatch(table)
    assert set(rotated) == set(table)
    for sample_id, items in rotated.items():
        assert items != table[sample_id], sample_id
    with pytest.raises(EvidenceError, match="at least 2"):
        rotated_mismatch({"a": [_item("ev-a")]})


def test_oracle_source_never_enters_runtime(synthetic_world):
    lock = load_lock(synthetic_world.lock_path)
    with pytest.raises(OracleEvidenceError, match="scoring-side"):
        EVIDENCE_SOURCES.resolve("oracle")(lock, synthetic_world.data_root, "4000001")
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/unit/test_core_components.py -v`
Expected: FAIL with `ModuleNotFoundError`

- [ ] **Step 3: Implement both modules**

`core/carriers.py`:

```python
"""Carrier loaders registered under their lock keys (the carrier seam)."""

from __future__ import annotations

from .base import CARRIERS
from ..data.loader import load_earnings21, load_earnings22

CARRIERS.register("earnings21-original", load_earnings21)
CARRIERS.register("earnings22-original", load_earnings22)
```

`core/evidence.py`:

```python
"""Evidence sources (the evidence seam): conec contexts, none, oracle refusal,
and the deterministic mismatch decorator applied by the driver on a config flag."""

from __future__ import annotations

from pathlib import Path
from typing import Mapping

from ..data.lock import asset_dir
from ..e0.artifacts import sha256_file
from .base import EVIDENCE_SOURCES, EvidenceError, EvidenceItem


class OracleEvidenceError(RuntimeError):
    """Oracle evidence was requested on the runtime path."""


def _none_source(
    lock: Mapping[str, object], root: Path, sample_id: str
) -> list[EvidenceItem]:
    return []


def _conec_contexts(
    lock: Mapping[str, object], root: Path, sample_id: str
) -> list[EvidenceItem]:
    relpath = f"earnings21/contexts/{sample_id}.txt"
    path = asset_dir(lock, "conec", root) / "earnings21" / "contexts" / f"{sample_id}.txt"
    if not path.is_file():
        raise EvidenceError(f"conec context missing for {sample_id}: {path}")
    try:
        content = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        raise EvidenceError(f"cannot read conec context {path}: {error}") from error
    item = EvidenceItem(
        evidence_id=f"conec/{sample_id}",
        source_uri=f"conec://{relpath}",
        content=content,
        provenance={"lock_key": "conec", "relpath": relpath, "sha256": sha256_file(path)},
    )
    return [item.validate()]


def _oracle_refusal(
    lock: Mapping[str, object], root: Path, sample_id: str
) -> list[EvidenceItem]:
    raise OracleEvidenceError(
        "oracle evidence is a scoring-side upper-bound analysis interface; it "
        "never enters a runtime arm (entry contract R0; design spec §2). Its "
        "computation is specified with the probe that first uses it."
    )


def rotated_mismatch(
    evidence_by_sample: Mapping[str, list[EvidenceItem]],
) -> dict[str, list[EvidenceItem]]:
    """Each sample receives the next sorted sample's evidence — a deterministic
    derangement (mismatched-evidence negative control), no randomness involved."""

    ordered = sorted(evidence_by_sample)
    if len(ordered) < 2:
        raise EvidenceError("rotated mismatch needs at least 2 samples")
    return {
        sample_id: list(evidence_by_sample[ordered[(index + 1) % len(ordered)]])
        for index, sample_id in enumerate(ordered)
    }


EVIDENCE_SOURCES.register("none", _none_source)
EVIDENCE_SOURCES.register("conec-contexts", _conec_contexts)
EVIDENCE_SOURCES.register("oracle", _oracle_refusal)
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/unit/test_core_components.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/speech_aware_evidence_acquisition/core/carriers.py src/speech_aware_evidence_acquisition/core/evidence.py tests/unit/test_core_components.py
git commit -m "feat(r0): registered carriers + evidence sources with mismatch decorator and oracle refusal"
```

---

### Task 7: `core/model.py` — gate-bound adapter (D2 allowlist choke point) + llama-server transport

**Files:**
- Create: `src/speech_aware_evidence_acquisition/core/model.py`
- Create: `tests/contract/gate_fixture.py` (move `GateFixture` here from `tests/contract/test_exposure_and_gate.py` — byte-identical class body plus the imports it needs; update `test_exposure_and_gate.py` to `from gate_fixture import GateFixture`. A plain helper module, NOT `conftest.py` — two conftest modules from different test dirs would collide on the `conftest` import name)
- Modify: `tests/contract/test_exposure_and_gate.py` (import the moved fixture)
- Test: `tests/unit/test_frozen_core_adapter.py`, `tests/unit/test_llama_server_transport.py`, `tests/contract/test_frozen_core_adapter.py`

**Interfaces:**
- Consumes: `contracts.FrozenCoreGate/ExecutionPlan/assert_information_boundary`, `e0.d2_leakage.ARM_VISIBLE_FIELDS` (single D2 source), `core.tracing.TraceSink`, `core.base.TRANSPORTS/CoreError`.
- Produces:
  - `class FrozenCoreError(RuntimeError)`
  - `@dataclass(frozen=True) CoreResponse`: `text`, `usage: Mapping[str, int]`, `request_sha256`, `response_sha256`, `latency_seconds`
  - `class FrozenCoreAdapter`: `__init__(gate, plan, arm, transport, sink)` — validates `arm in ARM_VISIBLE_FIELDS`; calls `gate.assert_model_touch_allowed(plan)` in the same process that will send requests (TOCTOU discipline). `request(payload) -> CoreResponse` — the ONLY request path: payload keys must **exactly equal** the arm's allowlist; boundary check; cumulative call + audio-second budget metering against the plan; canonical JSON; MODEL_REQUEST / MODEL_RESPONSE / COST trace records; parses the transport's `{"text","usage"}` contract. `cost_summary() -> dict` (`calls_used`, `audio_seconds_used`, `latency_seconds_total`, `prompt_tokens_total`, `completion_tokens_total`).
  - `class LlamaServerTransport`: `__init__(base_url, data_root, timeout_seconds=300.0, post=None)` — maps a boundary payload to an OpenAI-style `/v1/chat/completions` body (system = `task_instruction`; user content = base64 `input_audio` from `data_root / media_relpath` + one text part per evidence item; `decoding_params` passed through top-level); `post(url, body) -> bytes` defaults to stdlib urllib, injectable for tests; `__call__(request_bytes) -> bytes` returns canonical `{"text","usage"}` bytes.
  - Registered: `TRANSPORTS.register("llama-server", factory)` where `factory(values: Mapping, data_root: Path)` builds `LlamaServerTransport(values["base_url"], data_root, values.get("timeout_seconds", 300.0))`.

- [ ] **Step 1: Write the failing adapter unit tests**

`tests/unit/test_frozen_core_adapter.py`:

```python
"""Adapter choke point: allowlist exact-set, boundary, budgets, tracing."""

import json

import pytest

from speech_aware_evidence_acquisition.contracts import (
    BoundaryViolation,
    ExecutionPlan,
)
from speech_aware_evidence_acquisition.e0.d2_leakage import ARM_VISIBLE_FIELDS
from speech_aware_evidence_acquisition.core.model import FrozenCoreAdapter, FrozenCoreError
from speech_aware_evidence_acquisition.core.tracing import TraceSink


class _OpenGate:
    def __init__(self):
        self.checked_plans = []

    def assert_model_touch_allowed(self, plan):
        self.checked_plans.append(plan)


def _plan(**overrides):
    base = dict(
        run_id="SAEA-E-000-adapter",
        execution_profile="bounded-discovery-probe",
        carrier_lock_key="earnings22-original",
        split_role="dev",
        split_identity_hash="a" * 64,
        planned_model_calls=2,
        planned_gpu_hours=0.5,
        planned_speech_audio_seconds=250,
        protocol_hash="b" * 64,
    )
    base.update(overrides)
    return ExecutionPlan(**base)


def _payload(arm="bare-core", **overrides):
    payload = {
        "request_id": "req-1",
        "carrier_lock_key": "earnings22-original",
        "sample_id": "5000001",
        "speech_ref": "earnings22-original/5000001",
        "media_relpath": "datasets/earnings21-22/earnings22/media/5000001.mp3",
        "audio_seconds": 100.0,
        "sample_rate_hz": 16000,
        "task_instruction": "Transcribe the speech verbatim.",
        "history": [],
        "decoding_params": {"temperature": 0, "seed": 20260803},
    }
    assert set(payload) == set(ARM_VISIBLE_FIELDS[arm])
    payload.update(overrides)
    return payload


def _fake_transport(request_bytes):
    assert isinstance(request_bytes, bytes)
    return json.dumps(
        {"text": "hello world", "usage": {"prompt_tokens": 5, "completion_tokens": 2}}
    ).encode()


def _adapter(tmp_path, gate=None, plan=None, arm="bare-core"):
    sink = TraceSink(tmp_path / "run", "SAEA-E-000-adapter")
    return FrozenCoreAdapter(
        gate=gate or _OpenGate(),
        plan=plan or _plan(),
        arm=arm,
        transport=_fake_transport,
        sink=sink,
    ), sink


def test_gate_is_checked_at_construction(tmp_path):
    gate = _OpenGate()
    _adapter(tmp_path, gate=gate)
    assert len(gate.checked_plans) == 1


def test_request_round_trip_traces_and_counts(tmp_path):
    adapter, sink = _adapter(tmp_path)
    response = adapter.request(_payload())
    assert response.text == "hello world"
    assert len(response.request_sha256) == 64
    assert list(sink.manifest()) == ["req-1/request", "req-1/response", "req-1/cost"]
    summary = adapter.cost_summary()
    assert summary["calls_used"] == 1
    assert summary["audio_seconds_used"] == 100.0
    assert summary["completion_tokens_total"] == 2


def test_extra_field_refused_before_transport(tmp_path):
    adapter, _ = _adapter(tmp_path)
    with pytest.raises(FrozenCoreError, match="allowlist"):
        adapter.request(_payload(supplied_evidence=[{"content": "x"}]))


def test_missing_field_refused(tmp_path):
    adapter, _ = _adapter(tmp_path)
    payload = _payload()
    del payload["decoding_params"]
    with pytest.raises(FrozenCoreError, match="allowlist"):
        adapter.request(payload)


def test_forbidden_field_inside_value_refused(tmp_path):
    adapter, _ = _adapter(tmp_path)
    with pytest.raises(BoundaryViolation):
        adapter.request(_payload(history=[{"reference_transcript": "gold"}]))


def test_call_budget_exhaustion_fails_closed(tmp_path):
    adapter, _ = _adapter(tmp_path, plan=_plan(planned_model_calls=1))
    adapter.request(_payload())
    with pytest.raises(FrozenCoreError, match="call budget"):
        adapter.request(_payload(request_id="req-2"))


def test_audio_budget_exhaustion_fails_closed(tmp_path):
    adapter, _ = _adapter(tmp_path, plan=_plan(planned_speech_audio_seconds=150))
    adapter.request(_payload())
    with pytest.raises(FrozenCoreError, match="audio budget"):
        adapter.request(_payload(request_id="req-2"))


def test_unknown_arm_refused(tmp_path):
    with pytest.raises(FrozenCoreError, match="arm"):
        _adapter(tmp_path, arm="oracle-arm")
```

- [ ] **Step 2: Write the failing transport unit tests**

`tests/unit/test_llama_server_transport.py`:

```python
"""Transport maps boundary payloads to chat-completions bodies without network."""

import base64
import json

import pytest

from speech_aware_evidence_acquisition.core.model import LlamaServerTransport


def _boundary_payload(tmp_path, **overrides):
    media = tmp_path / "media" / "5000001.mp3"
    media.parent.mkdir(parents=True, exist_ok=True)
    media.write_bytes(b"fake-mp3-bytes")
    payload = {
        "request_id": "req-1",
        "carrier_lock_key": "earnings22-original",
        "sample_id": "5000001",
        "speech_ref": "earnings22-original/5000001",
        "media_relpath": "media/5000001.mp3",
        "audio_seconds": 10.0,
        "sample_rate_hz": 16000,
        "task_instruction": "Transcribe the speech verbatim.",
        "history": [],
        "decoding_params": {"temperature": 0, "seed": 20260803},
    }
    payload.update(overrides)
    return payload


def _canned_response():
    return json.dumps(
        {
            "choices": [{"message": {"content": "hello world"}}],
            "usage": {"prompt_tokens": 7, "completion_tokens": 2},
        }
    ).encode()


def test_body_mapping_and_response_projection(tmp_path):
    captured = {}

    def fake_post(url, body):
        captured["url"] = url
        captured["body"] = json.loads(body)
        return _canned_response()

    transport = LlamaServerTransport("http://127.0.0.1:8080", tmp_path, post=fake_post)
    raw = transport(json.dumps(_boundary_payload(tmp_path)).encode())
    result = json.loads(raw)
    assert result == {
        "text": "hello world",
        "usage": {"prompt_tokens": 7, "completion_tokens": 2},
    }
    assert captured["url"] == "http://127.0.0.1:8080/v1/chat/completions"
    body = captured["body"]
    assert body["temperature"] == 0
    assert body["seed"] == 20260803
    assert body["messages"][0] == {
        "role": "system",
        "content": "Transcribe the speech verbatim.",
    }
    audio_part = body["messages"][1]["content"][0]
    assert audio_part["type"] == "input_audio"
    assert audio_part["input_audio"]["format"] == "mp3"
    assert base64.b64decode(audio_part["input_audio"]["data"]) == b"fake-mp3-bytes"


def test_evidence_items_become_text_parts(tmp_path):
    def fake_post(url, body):
        parts = json.loads(body)["messages"][1]["content"]
        assert parts[1] == {"type": "text", "text": "[evidence ev-1] context text"}
        return _canned_response()

    transport = LlamaServerTransport("http://127.0.0.1:8080", tmp_path, post=fake_post)
    payload = _boundary_payload(
        tmp_path,
        supplied_evidence=[
            {"evidence_id": "ev-1", "source_uri": "conec://x", "content": "context text"}
        ],
        evidence_provenance=[{"lock_key": "conec", "relpath": "x", "sha256": "0" * 64}],
    )
    transport(json.dumps(payload).encode())


def test_missing_media_fails_closed(tmp_path):
    transport = LlamaServerTransport(
        "http://127.0.0.1:8080", tmp_path, post=lambda u, b: _canned_response()
    )
    payload = _boundary_payload(tmp_path, media_relpath="media/absent.mp3")
    with pytest.raises(FileNotFoundError):
        transport(json.dumps(payload).encode())
```

- [ ] **Step 3: Run tests to verify they fail**

Run: `pytest tests/unit/test_frozen_core_adapter.py tests/unit/test_llama_server_transport.py -v`
Expected: FAIL with `ModuleNotFoundError`

- [ ] **Step 4: Implement `core/model.py`**

```python
"""Frozen-core adapter and transports: the ONLY model request path (R0).

Discipline (docs/engineering.md): the gate is checked in the same process
that sends requests (no check-then-run-elsewhere TOCTOU gap); the D2 per-arm
visible-field allowlist is enforced as an exact key set on every request —
the choke point that makes a leakage a hard error rather than a convention.
The real llama-server endpoint shape is confirmed at R0 smoke time against
the receipt-pinned build — tests inject `post` and never open a socket.
"""

from __future__ import annotations

import base64
import hashlib
import json
import time
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Mapping

from ..contracts import ExecutionPlan, assert_information_boundary
from ..e0.d2_leakage import ARM_VISIBLE_FIELDS
from .base import TRANSPORTS
from .tracing import TraceSink


class FrozenCoreError(RuntimeError):
    """The adapter refuses: unknown arm, allowlist violation, or exhausted budget."""


@dataclass(frozen=True)
class CoreResponse:
    text: str
    usage: Mapping[str, int]
    request_sha256: str
    response_sha256: str
    latency_seconds: float


def _canonical(payload: Mapping[str, object]) -> bytes:
    return json.dumps(
        payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


class FrozenCoreAdapter:
    def __init__(
        self,
        gate: object,
        plan: ExecutionPlan,
        arm: str,
        transport: Callable[[bytes], bytes],
        sink: TraceSink,
    ) -> None:
        if arm not in ARM_VISIBLE_FIELDS:
            raise FrozenCoreError(
                f"unknown arm {arm!r}; D2-frozen arms are {sorted(ARM_VISIBLE_FIELDS)}"
            )
        gate.assert_model_touch_allowed(plan)
        self._plan = plan
        self._arm = arm
        self._allowlist = frozenset(ARM_VISIBLE_FIELDS[arm])
        self._transport = transport
        self._sink = sink
        self._calls_used = 0
        self._audio_seconds_used = 0.0
        self._latency_total = 0.0
        self._prompt_tokens = 0
        self._completion_tokens = 0

    def request(self, payload: Mapping[str, object]) -> CoreResponse:
        keys = set(payload)
        if keys != self._allowlist:
            raise FrozenCoreError(
                f"arm {self._arm!r} allowlist violation: "
                f"extra={sorted(keys - self._allowlist)} "
                f"missing={sorted(self._allowlist - keys)}"
            )
        assert_information_boundary(dict(payload))
        audio_seconds = payload["audio_seconds"]
        if not isinstance(audio_seconds, (int, float)) or audio_seconds <= 0:
            raise FrozenCoreError("payload audio_seconds must be a positive number")
        if self._calls_used + 1 > self._plan.planned_model_calls:
            raise FrozenCoreError(
                f"call budget exhausted: plan {self._plan.run_id} allows "
                f"{self._plan.planned_model_calls} calls"
            )
        if (
            self._audio_seconds_used + float(audio_seconds)
            > self._plan.planned_speech_audio_seconds
        ):
            raise FrozenCoreError(
                f"audio budget exhausted: plan {self._plan.run_id} allows "
                f"{self._plan.planned_speech_audio_seconds} speech audio seconds"
            )
        request_id = str(payload["request_id"])
        request_bytes = _canonical(payload)
        request_sha256 = hashlib.sha256(request_bytes).hexdigest()
        self._sink.emit(
            "MODEL_REQUEST",
            f"{request_id}/request",
            {"arm": self._arm, "payload": dict(payload), "payload_sha256": request_sha256},
        )
        started = time.monotonic()
        response_bytes = self._transport(request_bytes)
        latency = time.monotonic() - started
        response_sha256 = hashlib.sha256(response_bytes).hexdigest()
        try:
            parsed = json.loads(response_bytes.decode("utf-8"))
            text = parsed["text"]
            usage = {str(k): int(v) for k, v in dict(parsed.get("usage", {})).items()}
        except (KeyError, TypeError, ValueError, UnicodeError) as error:
            raise FrozenCoreError(
                f"transport returned a malformed response: {error}"
            ) from error
        self._sink.emit(
            "MODEL_RESPONSE",
            f"{request_id}/response",
            {"response_sha256": response_sha256, "text": text, "usage": usage},
        )
        self._calls_used += 1
        self._audio_seconds_used += float(audio_seconds)
        self._latency_total += latency
        self._prompt_tokens += usage.get("prompt_tokens", 0)
        self._completion_tokens += usage.get("completion_tokens", 0)
        self._sink.emit(
            "COST",
            f"{request_id}/cost",
            {
                "calls": 1,
                "audio_seconds": float(audio_seconds),
                "latency_seconds": latency,
                "prompt_tokens": usage.get("prompt_tokens", 0),
                "completion_tokens": usage.get("completion_tokens", 0),
            },
        )
        return CoreResponse(
            text=text,
            usage=usage,
            request_sha256=request_sha256,
            response_sha256=response_sha256,
            latency_seconds=latency,
        )

    def cost_summary(self) -> dict[str, object]:
        return {
            "calls_used": self._calls_used,
            "audio_seconds_used": self._audio_seconds_used,
            "latency_seconds_total": self._latency_total,
            "prompt_tokens_total": self._prompt_tokens,
            "completion_tokens_total": self._completion_tokens,
        }


def _default_post(timeout_seconds: float) -> Callable[[str, bytes], bytes]:
    def post(url: str, body: bytes) -> bytes:
        request = urllib.request.Request(
            url, data=body, headers={"Content-Type": "application/json"}, method="POST"
        )
        with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
            return response.read()

    return post


class LlamaServerTransport:
    def __init__(
        self,
        base_url: str,
        data_root: Path,
        timeout_seconds: float = 300.0,
        post: Callable[[str, bytes], bytes] | None = None,
    ) -> None:
        self._url = base_url.rstrip("/") + "/v1/chat/completions"
        self._data_root = Path(data_root)
        self._post = post or _default_post(timeout_seconds)

    def __call__(self, request_bytes: bytes) -> bytes:
        payload: Mapping[str, object] = json.loads(request_bytes.decode("utf-8"))
        media = self._data_root / str(payload["media_relpath"])
        if not media.is_file():
            raise FileNotFoundError(f"media missing for transport: {media}")
        audio_b64 = base64.b64encode(media.read_bytes()).decode("ascii")
        content: list[dict[str, object]] = [
            {
                "type": "input_audio",
                "input_audio": {"data": audio_b64, "format": media.suffix.lstrip(".").lower()},
            }
        ]
        for field in ("supplied_evidence", "retrieved_evidence"):
            for item in payload.get(field, []):  # type: ignore[union-attr]
                content.append(
                    {"type": "text", "text": f"[evidence {item['evidence_id']}] {item['content']}"}
                )
        body: dict[str, object] = {
            "messages": [
                {"role": "system", "content": payload["task_instruction"]},
                {"role": "user", "content": content},
            ],
        }
        for key, value in dict(payload.get("decoding_params", {})).items():  # type: ignore[arg-type]
            body[key] = value
        raw = self._post(self._url, json.dumps(body).encode("utf-8"))
        parsed = json.loads(raw.decode("utf-8"))
        text = parsed["choices"][0]["message"]["content"]
        usage = {str(k): int(v) for k, v in dict(parsed.get("usage", {})).items()}
        return json.dumps({"text": text, "usage": usage}).encode("utf-8")


def _llama_server_factory(values: Mapping[str, object], data_root: Path):
    return LlamaServerTransport(
        str(values["base_url"]), data_root, float(values.get("timeout_seconds", 300.0))
    )


TRANSPORTS.register("llama-server", _llama_server_factory)
```

- [ ] **Step 5: Run unit tests to verify they pass**

Run: `pytest tests/unit/test_frozen_core_adapter.py tests/unit/test_llama_server_transport.py -v`
Expected: PASS

- [ ] **Step 6: Move `GateFixture` and add the real-gate contract test**

Move the `GateFixture` class from `tests/contract/test_exposure_and_gate.py` into `tests/contract/gate_fixture.py` (byte-identical, plus its imports); update `test_exposure_and_gate.py` to `from gate_fixture import GateFixture`. Run `pytest tests/contract/test_exposure_and_gate.py -v` — all pre-existing tests must still pass before continuing.

Create `tests/contract/test_frozen_core_adapter.py`:

```python
"""Contract: the adapter is inseparable from the real gate (fail-closed end to end)."""

import json

import pytest

from gate_fixture import GateFixture

from speech_aware_evidence_acquisition.contracts import ExecutionScopeError, GateClosed
from speech_aware_evidence_acquisition.core.model import FrozenCoreAdapter
from speech_aware_evidence_acquisition.core.tracing import TraceSink


def _fake_transport(request_bytes):
    return json.dumps({"text": "ok", "usage": {}}).encode()


def test_adapter_construction_passes_through_a_real_open_gate(tmp_path):
    fixture = GateFixture(tmp_path)  # adapt to the fixture's actual constructor
    adapter = FrozenCoreAdapter(
        gate=fixture.gate,
        plan=fixture.registered_plan,
        arm="bare-core",
        transport=_fake_transport,
        sink=TraceSink(tmp_path / "run", fixture.registered_plan.run_id),
    )
    assert adapter.cost_summary()["calls_used"] == 0


def test_adapter_refuses_when_the_gate_is_closed(tmp_path):
    fixture = GateFixture(tmp_path)
    fixture.break_e0_receipt()  # adapt to the fixture's actual tamper helper
    with pytest.raises(GateClosed):
        FrozenCoreAdapter(
            gate=fixture.gate,
            plan=fixture.registered_plan,
            arm="bare-core",
            transport=_fake_transport,
            sink=TraceSink(tmp_path / "run", fixture.registered_plan.run_id),
        )


def test_adapter_refuses_model_free_profiles(tmp_path):
    fixture = GateFixture(tmp_path)
    plan = fixture.plan_with(execution_profile="model-free-check")  # adapt likewise
    with pytest.raises(ExecutionScopeError):
        FrozenCoreAdapter(
            gate=fixture.gate,
            plan=plan,
            arm="bare-core",
            transport=_fake_transport,
            sink=TraceSink(tmp_path / "run", "SAEA-E-000-x"),
        )
```

The three `# adapt` comments mark the only allowed divergence: read `tests/contract/test_exposure_and_gate.py` and use `GateFixture`'s **actual** construction/tamper/plan helpers (they already exist for the existing refusal tests); do not invent new fixture behavior. Remove the comments once wired.

- [ ] **Step 7: Run the full contract suite, then commit**

Run: `pytest tests/contract -v` — Expected: PASS (all pre-existing + 3 new).

```bash
git add src/speech_aware_evidence_acquisition/core/model.py tests/unit/test_frozen_core_adapter.py tests/unit/test_llama_server_transport.py tests/contract/gate_fixture.py tests/contract/test_exposure_and_gate.py tests/contract/test_frozen_core_adapter.py
git commit -m "feat(r0): gate-bound frozen-core adapter + llama-server transport (one request path)"
```

---

### Task 8: `core/config.py` — deterministic JSON config composition + seed fragments

**Files:**
- Create: `src/speech_aware_evidence_acquisition/core/config.py`
- Create: `configs/model/qwen3-omni-llamacpp.json`
- Create: `configs/dataset/earnings22-dev-subset10.json`
- Create: `configs/baseline/bare-core.json`
- Create: `configs/experiment/r0-smoke.json`
- Test: `tests/unit/test_config_composition.py`

**Interfaces:**
- Consumes: `scoring.SCORING_STACK_VERSION` (frozen stack, read-only).
- Produces:
  - `class ConfigError(RuntimeError)`
  - `@dataclass(frozen=True) ComposedConfig`: `values: Mapping`, `config_hash: str`, `fragments: Mapping[str, str]`
  - `compose(repo_root, model, dataset, baseline, experiment) -> ComposedConfig` — reads `configs/<kind>/<name>.json`; top-level keys must be **disjoint** across fragments (collision → `ConfigError`, no override semantics); `config_hash` = sha256 over canonical JSON of the merged mapping.
  - `protocol_hash(config_hash, arm, split_identity_hash) -> str` — sha256 over canonical JSON `{"arm", "config", "scoring": SCORING_STACK_VERSION, "split"}`.

Fragment contents (exact):

`configs/model/qwen3-omni-llamacpp.json`

```json
{
  "model_lock_key": "qwen3-omni-30b-a3b-instruct-gguf",
  "transport": "llama-server",
  "base_url": "http://127.0.0.1:8080",
  "timeout_seconds": 300.0,
  "decoding_params": {"temperature": 0, "seed": 20260803}
}
```

`configs/dataset/earnings22-dev-subset10.json`

```json
{
  "carrier_lock_key": "earnings22-original",
  "split_name": "dev"
}
```

`configs/baseline/bare-core.json`

```json
{
  "arm": "bare-core",
  "policy": "fixed",
  "evidence_source": "none",
  "evidence_mismatch": false,
  "scorers": ["asr-wer"],
  "task_instruction": "Transcribe the speech verbatim. Output only the transcript text."
}
```

`configs/experiment/r0-smoke.json`

```json
{
  "experiment_id": "SAEA-E-001",
  "execution_profile": "bounded-discovery-probe",
  "purpose": "R0 wiring and measurement-integrity smoke on the dev subset10; no superiority claim"
}
```

- [ ] **Step 1: Write the failing tests**

`tests/unit/test_config_composition.py`:

```python
"""Deterministic config composition: disjoint fragments, stable hashes."""

import json

import pytest

from speech_aware_evidence_acquisition.core.config import (
    ComposedConfig,
    ConfigError,
    compose,
    protocol_hash,
)
from speech_aware_evidence_acquisition.scoring import SCORING_STACK_VERSION


def _write_fragments(root, experiment_extra=None):
    for kind, name, body in (
        ("model", "m", {"transport": "llama-server", "base_url": "http://x"}),
        ("dataset", "d", {"carrier_lock_key": "earnings22-original", "split_name": "dev"}),
        ("baseline", "b", {"arm": "bare-core", "policy": "fixed", "task_instruction": "t"}),
        ("experiment", "e", {"experiment_id": "SAEA-E-001", **(experiment_extra or {})}),
    ):
        path = root / "configs" / kind / f"{name}.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(body), encoding="utf-8")


def test_compose_merges_disjoint_fragments_deterministically(tmp_path):
    _write_fragments(tmp_path)
    first = compose(tmp_path, "m", "d", "b", "e")
    second = compose(tmp_path, "m", "d", "b", "e")
    assert isinstance(first, ComposedConfig)
    assert first.values["arm"] == "bare-core"
    assert first.values["experiment_id"] == "SAEA-E-001"
    assert first.config_hash == second.config_hash
    assert first.fragments == {"model": "m", "dataset": "d", "baseline": "b", "experiment": "e"}


def test_key_collision_fails_closed(tmp_path):
    _write_fragments(tmp_path, experiment_extra={"arm": "sneaky-override"})
    with pytest.raises(ConfigError, match="collision"):
        compose(tmp_path, "m", "d", "b", "e")


def test_missing_fragment_fails_closed(tmp_path):
    _write_fragments(tmp_path)
    with pytest.raises(ConfigError, match="missing"):
        compose(tmp_path, "m", "d", "b", "absent")


def test_protocol_hash_binds_scoring_version():
    first = protocol_hash("a" * 64, "bare-core", "b" * 64)
    assert len(first) == 64
    assert first != protocol_hash("a" * 64, "fixed-retrieval", "b" * 64)
    assert SCORING_STACK_VERSION  # bound inside the hash; a version bump changes it


def test_repo_fragments_compose():
    from speech_aware_evidence_acquisition.e0.artifacts import REPO_ROOT

    composed = compose(
        REPO_ROOT, "qwen3-omni-llamacpp", "earnings22-dev-subset10", "bare-core", "r0-smoke"
    )
    assert composed.values["experiment_id"] == "SAEA-E-001"
    assert composed.values["arm"] == "bare-core"
    assert composed.values["policy"] == "fixed"
    assert composed.values["transport"] == "llama-server"
    assert composed.values["model_lock_key"] == "qwen3-omni-30b-a3b-instruct-gguf"
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/unit/test_config_composition.py -v`
Expected: FAIL with `ModuleNotFoundError`

- [ ] **Step 3: Implement `core/config.py` + the four fragment files (exact JSON above)**

```python
"""Deterministic four-fragment config composition (model/dataset/baseline/experiment).

JSON, stdlib-only, no override semantics: top-level keys must be disjoint
across fragments so a later fragment can never silently rewrite an earlier
one. The composed hash and the protocol hash are the identity cells every
formal ledger row carries.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping

from ..scoring import SCORING_STACK_VERSION

_KINDS = ("model", "dataset", "baseline", "experiment")


class ConfigError(RuntimeError):
    """A config fragment is missing, unreadable, or collides with another."""


@dataclass(frozen=True)
class ComposedConfig:
    values: Mapping[str, object]
    config_hash: str
    fragments: Mapping[str, str]


def _canonical_hash(document: Mapping[str, object]) -> str:
    blob = json.dumps(document, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def compose(
    repo_root: Path, model: str, dataset: str, baseline: str, experiment: str
) -> ComposedConfig:
    names = dict(zip(_KINDS, (model, dataset, baseline, experiment)))
    merged: dict[str, object] = {}
    origins: dict[str, str] = {}
    for kind in _KINDS:
        path = Path(repo_root) / "configs" / kind / f"{names[kind]}.json"
        if not path.is_file():
            raise ConfigError(f"missing config fragment: {path}")
        try:
            fragment = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as error:
            raise ConfigError(f"cannot read config fragment {path}: {error}") from error
        if not isinstance(fragment, dict):
            raise ConfigError(f"config fragment {path} must be a JSON object")
        for key, value in fragment.items():
            if key in merged:
                raise ConfigError(
                    f"config key collision: {key!r} defined by {origins[key]} and {kind}"
                )
            merged[key] = value
            origins[key] = kind
    return ComposedConfig(values=merged, config_hash=_canonical_hash(merged), fragments=names)


def protocol_hash(config_hash: str, arm: str, split_identity_hash: str) -> str:
    return _canonical_hash(
        {
            "arm": arm,
            "config": config_hash,
            "scoring": SCORING_STACK_VERSION,
            "split": split_identity_hash,
        }
    )
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/unit/test_config_composition.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/speech_aware_evidence_acquisition/core/config.py configs tests/unit/test_config_composition.py
git commit -m "feat(r0): deterministic JSON config composition + r0-smoke fragments"
```

---

### Task 9: `core/policies.py` — arm payload builder + the `fixed` policy

**Files:**
- Create: `src/speech_aware_evidence_acquisition/core/policies.py`
- Test: `tests/unit/test_policies.py`

**Interfaces:**
- Consumes: `core.base.POLICIES/SampleContext/SampleOutcome/EvidenceItem/CoreError`, `e0.d2_leakage.ARM_VISIBLE_FIELDS`.
- Produces:
  - `class ArmError(RuntimeError)`
  - `build_arm_payload(arm, ref, request_id, task_instruction, decoding_params, evidence=None, retrieval_query=None) -> dict` — starts from `ref.runtime_view()`; adds `request_id`/`task_instruction`/`history: []`/`decoding_params`; `fixed-legal-context` requires evidence → `supplied_evidence` + `evidence_provenance`; `fixed-retrieval` requires evidence + query → `retrieval_query` + `retrieved_evidence` + `evidence_provenance`; `bare-core` refuses both. Output keys are asserted **exactly equal** to `ARM_VISIBLE_FIELDS[arm]`.
  - `class FixedPolicy` — one request per sample, always admits: builds the payload, calls `ctx.adapter.request(...)`, emits the `USE` record (`use_response_sha256`, `use_admitted: True`), returns `SampleOutcome`. Registered as `POLICIES.register("fixed", FixedPolicy())`. (X1 multi-request re-resolution, X3 verification loops, X4 reward-guided policies register here later — the driver never changes.)

- [ ] **Step 1: Write the failing tests**

`tests/unit/test_policies.py`:

```python
"""Arm payload builder emits exactly the D2-frozen field sets; fixed policy runs one request."""

import json

import pytest

from speech_aware_evidence_acquisition.core import policies  # noqa: F401 (registration)
from speech_aware_evidence_acquisition.core.base import (
    POLICIES,
    EvidenceItem,
    SampleContext,
)
from speech_aware_evidence_acquisition.core.policies import ArmError, build_arm_payload
from speech_aware_evidence_acquisition.core.tracing import TraceSink
from speech_aware_evidence_acquisition.data.loader import SampleRef
from speech_aware_evidence_acquisition.e0.d2_leakage import ARM_VISIBLE_FIELDS

_REF = SampleRef(
    carrier_lock_key="earnings21-original",
    sample_id="4000001",
    media_relpath="datasets/earnings21-22/earnings21/media/4000001.mp3",
    audio_seconds=100.5,
    sample_rate_hz=16000,
)
_EVIDENCE = [
    EvidenceItem(
        evidence_id="conec/4000001",
        source_uri="conec://earnings21/contexts/4000001.txt",
        content="ctx",
        provenance={
            "lock_key": "conec",
            "relpath": "earnings21/contexts/4000001.txt",
            "sha256": "0" * 64,
        },
    )
]
_DECODING = {"temperature": 0, "seed": 20260803}


def test_bare_core_exact_fields():
    payload = build_arm_payload("bare-core", _REF, "req-1", "Transcribe.", _DECODING)
    assert set(payload) == set(ARM_VISIBLE_FIELDS["bare-core"])
    assert payload["history"] == []
    assert payload["speech_ref"] == "earnings21-original/4000001"


def test_bare_core_refuses_evidence():
    with pytest.raises(ArmError, match="bare-core"):
        build_arm_payload("bare-core", _REF, "req-1", "T.", _DECODING, evidence=_EVIDENCE)


def test_fixed_legal_context_carries_evidence_and_provenance():
    payload = build_arm_payload(
        "fixed-legal-context", _REF, "req-1", "T.", _DECODING, evidence=_EVIDENCE
    )
    assert set(payload) == set(ARM_VISIBLE_FIELDS["fixed-legal-context"])
    assert payload["supplied_evidence"] == [_EVIDENCE[0].runtime_view()]
    assert payload["evidence_provenance"] == [_EVIDENCE[0].provenance_view()]


def test_fixed_legal_context_requires_evidence():
    with pytest.raises(ArmError, match="evidence"):
        build_arm_payload("fixed-legal-context", _REF, "req-1", "T.", _DECODING)


def test_fixed_retrieval_requires_query_and_evidence():
    payload = build_arm_payload(
        "fixed-retrieval", _REF, "req-1", "T.", _DECODING,
        evidence=_EVIDENCE, retrieval_query="acme q2",
    )
    assert set(payload) == set(ARM_VISIBLE_FIELDS["fixed-retrieval"])
    assert payload["retrieval_query"] == "acme q2"
    with pytest.raises(ArmError, match="retrieval_query"):
        build_arm_payload(
            "fixed-retrieval", _REF, "req-1", "T.", _DECODING, evidence=_EVIDENCE
        )


def test_unknown_arm_refused():
    with pytest.raises(ArmError, match="unknown arm"):
        build_arm_payload("oracle-arm", _REF, "req-1", "T.", _DECODING)


class _OpenGate:
    def assert_model_touch_allowed(self, plan):
        pass


def test_fixed_policy_runs_one_request_and_admits(tmp_path):
    from speech_aware_evidence_acquisition.contracts import ExecutionPlan
    from speech_aware_evidence_acquisition.core.model import FrozenCoreAdapter

    sink = TraceSink(tmp_path / "run", "SAEA-E-000-policy")
    plan = ExecutionPlan(
        run_id="SAEA-E-000-policy",
        execution_profile="bounded-discovery-probe",
        carrier_lock_key="earnings21-original",
        split_role="discovery",
        split_identity_hash="a" * 64,
        planned_model_calls=5,
        planned_gpu_hours=1.0,
        planned_speech_audio_seconds=1000,
        protocol_hash="b" * 64,
    )
    adapter = FrozenCoreAdapter(
        gate=_OpenGate(),
        plan=plan,
        arm="bare-core",
        transport=lambda b: json.dumps({"text": "hi", "usage": {}}).encode(),
        sink=sink,
    )
    ctx = SampleContext(
        sample=_REF, evidence=[], adapter=adapter, sink=sink, arm="bare-core",
        task_instruction="T.", decoding_params=_DECODING, request_id_base="req-0001",
    )
    outcome = POLICIES.resolve("fixed").run_sample(ctx)
    assert outcome.sample_id == "4000001"
    assert outcome.admitted is True
    assert outcome.request_ids == ("req-0001",)
    assert "req-0001/use" in sink.manifest()
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/unit/test_policies.py -v`
Expected: FAIL with `ModuleNotFoundError`

- [ ] **Step 3: Implement `core/policies.py`**

```python
"""Execution policies over the three D2-frozen arm shapes (the policy seam).

R0 implements exactly one policy: ``fixed`` — one request per sample, always
admit. X1 re-resolution (multiple requests), X3 verification/rejection loops
and X4 reward-guided action selection register here later; the arm payload
vocabulary never grows without a new D2 receipt.
"""

from __future__ import annotations

from typing import Mapping

from ..data.loader import SampleRef
from ..e0.d2_leakage import ARM_VISIBLE_FIELDS
from .base import POLICIES, EvidenceItem, SampleContext, SampleOutcome


class ArmError(RuntimeError):
    """An arm builder was given inputs its D2-frozen field set cannot carry."""


def build_arm_payload(
    arm: str,
    ref: SampleRef,
    request_id: str,
    task_instruction: str,
    decoding_params: Mapping[str, object],
    evidence: list[EvidenceItem] | None = None,
    retrieval_query: str | None = None,
) -> dict[str, object]:
    if arm not in ARM_VISIBLE_FIELDS:
        raise ArmError(f"unknown arm {arm!r}; D2-frozen arms are {sorted(ARM_VISIBLE_FIELDS)}")
    payload: dict[str, object] = dict(ref.runtime_view())
    payload["request_id"] = request_id
    payload["task_instruction"] = task_instruction
    payload["history"] = []
    payload["decoding_params"] = dict(decoding_params)
    if arm == "bare-core":
        if evidence is not None or retrieval_query is not None:
            raise ArmError("bare-core carries no evidence and no retrieval query")
    else:
        if not evidence:
            raise ArmError(f"arm {arm!r} requires non-empty evidence")
        validated = [item.validate() for item in evidence]
        provenance = [item.provenance_view() for item in validated]
        if arm == "fixed-legal-context":
            if retrieval_query is not None:
                raise ArmError("fixed-legal-context carries no retrieval query")
            payload["supplied_evidence"] = [item.runtime_view() for item in validated]
        else:  # fixed-retrieval
            if retrieval_query is None or not retrieval_query.strip():
                raise ArmError("fixed-retrieval requires a retrieval_query")
            payload["retrieval_query"] = retrieval_query
            payload["retrieved_evidence"] = [item.runtime_view() for item in validated]
        payload["evidence_provenance"] = provenance
    if set(payload) != set(ARM_VISIBLE_FIELDS[arm]):
        raise ArmError(
            f"arm {arm!r} builder produced a field set that diverges from the D2 freeze: "
            f"{sorted(set(payload) ^ set(ARM_VISIBLE_FIELDS[arm]))}"
        )
    return payload


class FixedPolicy:
    """One request per sample; the response is always admitted (R0 wiring)."""

    def run_sample(self, ctx: SampleContext) -> SampleOutcome:
        evidence = ctx.evidence if ctx.arm != "bare-core" else None
        payload = build_arm_payload(
            ctx.arm,
            ctx.sample,
            ctx.request_id_base,
            ctx.task_instruction,
            ctx.decoding_params,
            evidence=evidence,
            retrieval_query=ctx.retrieval_query,
        )
        response = ctx.adapter.request(payload)
        ctx.sink.emit(
            "USE",
            f"{ctx.request_id_base}/use",
            {"use_response_sha256": response.response_sha256, "use_admitted": True},
        )
        return SampleOutcome(
            sample_id=ctx.sample.sample_id,
            request_ids=(ctx.request_id_base,),
            text=response.text,
            admitted=True,
            request_sha256=response.request_sha256,
            response_sha256=response.response_sha256,
        )


POLICIES.register("fixed", FixedPolicy())
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/unit/test_policies.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/speech_aware_evidence_acquisition/core/policies.py tests/unit/test_policies.py
git commit -m "feat(r0): arm payload builder + fixed policy (policy seam defined, one impl)"
```

---

### Task 10: `core/scorers.py` — registered scorer adapters + import isolation

**Files:**
- Create: `src/speech_aware_evidence_acquisition/core/scorers.py`
- Test: `tests/unit/test_scorers.py`
- Test: `tests/contract/test_reference_import_isolation.py`

**Interfaces:**
- Consumes: `data.references.reference_tokens` (**the only permitted importer**), frozen `scoring.align/tokens_v1`, `core.base.SCORERS`.
- Produces:
  - `class ScoringPhaseError(RuntimeError)`
  - `SCORERS` name `"asr-wer"` → `score_asr_outputs(outputs_path, lock, root) -> dict` — reads the run's outputs JSONL; per sample loads reference tokens, computes `align(tokens_v1(" ".join(ref)), tokens_v1(text))`; returns `{"per_sample": [{sample_id, wer, hits, substitutions, deletions, insertions, ref_hit_mask}], "aggregate": {"mean_wer", "samples"}}`.
  - `transition_report(baseline: dict, treatment: dict) -> dict` — pairs `per_sample` by `sample_id`, compares `ref_hit_mask`s positionally; fail-closed on differing sample sets or mask lengths; returns the four transition totals.

- [ ] **Step 1: Write the failing unit tests**

`tests/unit/test_scorers.py`:

```python
"""Scorer adapters over the frozen stack; transition accounting from hit masks."""

import json

import pytest

from speech_aware_evidence_acquisition.core import scorers  # noqa: F401 (registration)
from speech_aware_evidence_acquisition.core.base import SCORERS
from speech_aware_evidence_acquisition.core.scorers import (
    ScoringPhaseError,
    transition_report,
)
from speech_aware_evidence_acquisition.data.lock import load_lock


def _write_outputs(tmp_path, rows):
    path = tmp_path / "x.outputs.jsonl"
    path.write_text(
        "".join(json.dumps(row, sort_keys=True) + "\n" for row in rows), encoding="utf-8"
    )
    return path


def test_asr_wer_scores_against_references(synthetic_world, tmp_path):
    nlp = synthetic_world.e21 / "transcripts" / "nlp_references" / "4000001.nlp"
    nlp.write_text("token|tags\nhello|\nworld|\n", encoding="utf-8")
    outputs = _write_outputs(
        tmp_path,
        [{"sample_id": "4000001", "carrier_lock_key": "earnings21-original",
          "arm": "bare-core", "request_id": "req-0001", "text": "hello world",
          "request_sha256": "0" * 64, "response_sha256": "0" * 64}],
    )
    lock = load_lock(synthetic_world.lock_path)
    scores = SCORERS.resolve("asr-wer")(outputs, lock, synthetic_world.data_root)
    assert scores["aggregate"] == {"mean_wer": 0.0, "samples": 1}
    assert scores["per_sample"][0]["ref_hit_mask"] == [True, True]


def test_empty_outputs_fail_closed(tmp_path, synthetic_world):
    path = tmp_path / "empty.outputs.jsonl"
    path.write_text("", encoding="utf-8")
    lock = load_lock(synthetic_world.lock_path)
    with pytest.raises(ScoringPhaseError, match="empty"):
        SCORERS.resolve("asr-wer")(path, lock, synthetic_world.data_root)


def test_transition_report_counts_mask_flips():
    baseline = {"per_sample": [{"sample_id": "a", "ref_hit_mask": [True, False, True]}]}
    treatment = {"per_sample": [{"sample_id": "a", "ref_hit_mask": [True, True, False]}]}
    report = transition_report(baseline, treatment)
    assert report == {
        "correct_to_correct": 1,
        "correct_to_wrong": 1,
        "wrong_to_correct": 1,
        "wrong_to_wrong": 0,
    }


def test_transition_report_fails_closed_on_mismatch():
    with pytest.raises(ScoringPhaseError, match="differ"):
        transition_report(
            {"per_sample": [{"sample_id": "a", "ref_hit_mask": [True]}]},
            {"per_sample": [{"sample_id": "b", "ref_hit_mask": [True]}]},
        )
```

- [ ] **Step 2: Write the failing import-isolation contract test**

`tests/contract/test_reference_import_isolation.py`:

```python
"""Contract: only core/scorers.py may import the scoring-side reference reader."""

import ast
from pathlib import Path

SRC = Path(__file__).resolve().parents[2] / "src" / "speech_aware_evidence_acquisition"
ALLOWED = {SRC / "core" / "scorers.py", SRC / "data" / "references.py"}


def _imports_references(path: Path) -> bool:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            module = node.module or ""
            if module.endswith("references") or any(
                alias.name == "references" for alias in node.names
            ):
                return True
        if isinstance(node, ast.Import):
            if any("references" in alias.name for alias in node.names):
                return True
    return False


def test_only_the_scoring_phase_imports_references():
    offenders = [
        str(path)
        for path in sorted(SRC.rglob("*.py"))
        if path not in ALLOWED and _imports_references(path)
    ]
    assert offenders == [], f"runtime-phase modules import data.references: {offenders}"
```

- [ ] **Step 3: Run tests to verify they fail**

Run: `pytest tests/unit/test_scorers.py tests/contract/test_reference_import_isolation.py -v`
Expected: unit FAIL (`ModuleNotFoundError`); the contract test passes trivially now — it exists to lock the rule repo-wide (it scans every source file, including future ones).

- [ ] **Step 4: Implement `core/scorers.py`**

```python
"""Scoring phase: outputs JSONL + reference layers -> frozen-scoring results.

This is the ONLY module allowed to import data.references (AST contract
test). It runs strictly after the runtime phase, on recorded outputs — never
inside a request loop.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Mapping

from ..data.references import reference_tokens
from ..scoring import align, tokens_v1
from .base import SCORERS


class ScoringPhaseError(RuntimeError):
    """Outputs are malformed or reference/hypothesis pairing is impossible."""


def score_asr_outputs(
    outputs_path: Path, lock: Mapping[str, object], root: Path
) -> dict[str, object]:
    try:
        lines = Path(outputs_path).read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError) as error:
        raise ScoringPhaseError(f"cannot read outputs {outputs_path}: {error}") from error
    if not lines:
        raise ScoringPhaseError(f"outputs file {outputs_path} is empty")
    per_sample: list[dict[str, object]] = []
    for number, line in enumerate(lines, start=1):
        try:
            row = json.loads(line)
        except json.JSONDecodeError as error:
            raise ScoringPhaseError(f"outputs line {number} malformed: {error}") from error
        ref = tokens_v1(
            " ".join(reference_tokens(lock, root, row["carrier_lock_key"], row["sample_id"]))
        )
        result = align(ref, tokens_v1(row["text"]))
        per_sample.append(
            {
                "sample_id": row["sample_id"],
                "wer": result.wer,
                "hits": result.hits,
                "substitutions": result.substitutions,
                "deletions": result.deletions,
                "insertions": result.insertions,
                "ref_hit_mask": list(result.ref_hit_mask),
            }
        )
    mean_wer = sum(entry["wer"] for entry in per_sample) / len(per_sample)
    return {
        "per_sample": per_sample,
        "aggregate": {"mean_wer": mean_wer, "samples": len(per_sample)},
    }


def transition_report(
    baseline: Mapping[str, object], treatment: Mapping[str, object]
) -> dict[str, int]:
    base_by_id = {entry["sample_id"]: entry for entry in baseline["per_sample"]}
    treat_by_id = {entry["sample_id"]: entry for entry in treatment["per_sample"]}
    if set(base_by_id) != set(treat_by_id):
        raise ScoringPhaseError("baseline/treatment sample sets differ")
    totals = {
        "correct_to_correct": 0,
        "correct_to_wrong": 0,
        "wrong_to_correct": 0,
        "wrong_to_wrong": 0,
    }
    for sample_id, base in base_by_id.items():
        base_mask = base["ref_hit_mask"]
        treat_mask = treat_by_id[sample_id]["ref_hit_mask"]
        if len(base_mask) != len(treat_mask):
            raise ScoringPhaseError(
                f"{sample_id}: reference masks differ in length — not the same reference"
            )
        for before, after in zip(base_mask, treat_mask):
            if before and after:
                totals["correct_to_correct"] += 1
            elif before and not after:
                totals["correct_to_wrong"] += 1
            elif not before and after:
                totals["wrong_to_correct"] += 1
            else:
                totals["wrong_to_wrong"] += 1
    return totals


SCORERS.register("asr-wer", score_asr_outputs)
```

- [ ] **Step 5: Run tests to verify they pass, then commit**

Run: `pytest tests/unit/test_scorers.py tests/contract/test_reference_import_isolation.py -v` — Expected: PASS.

```bash
git add src/speech_aware_evidence_acquisition/core/scorers.py tests/unit/test_scorers.py tests/contract/test_reference_import_isolation.py
git commit -m "feat(r0): registered scorer adapters + repo-wide reference import isolation"
```

---

### Task 11: `core/driver.py` — the ONE experiment driver + CLI

**Files:**
- Create: `src/speech_aware_evidence_acquisition/core/driver.py`
- Test: `tests/unit/test_driver.py`

**Interfaces:**
- Consumes: everything above via `core.base` registries; `data.splits.SPLITS_RECEIPT_NAME/split_identity_hash`; `contracts.ExecutionPlan`; `contracts.FrozenCoreGate.for_study_repo` (CLI live mode only).
- Produces:
  - `load_split(repo_root, split_name) -> tuple[set[str], str]` — reads the frozen `docs/receipts/splits.json`; returns (bare sample ids, identity hash); fail-closed if absent.
  - `run_experiment(composed: ComposedConfig, plan: ExecutionPlan, gate, lock, root, run_dir, transport, repo_root=REPO_ROOT) -> RunResult` — the single shared path: resolve carrier + split (**refuses a plan whose `split_identity_hash` differs from the frozen receipt**); resolve evidence source (+ `rotated_mismatch` when `evidence_mismatch` is true); resolve policy; build `TraceSink` + `FrozenCoreAdapter`; per sample emit `OBS` (+ `ORG`/`SUPPLY` when evidence present), delegate to `policy.run_sample`, append one outputs JSONL line; close sink; return `RunResult` with `adapter.cost_summary()`.
  - CLI (`python -m speech_aware_evidence_acquisition.core.driver …`): subcommand `score --outputs <path> --scorers asr-wer` (model-free; prints aggregate JSON) and subcommand `run --model … --dataset … --baseline … --experiment … --plan <plan.json> --run-dir <dir>` (live: builds the real gate via `FrozenCoreGate.for_study_repo`, the transport from the registry, and calls `run_experiment`; exercised only at smoke time).

- [ ] **Step 1: Write the failing end-to-end test**

`tests/unit/test_driver.py`:

```python
"""End-to-end wiring on the synthetic world with a fake transport."""

import json

import pytest

import speech_aware_evidence_acquisition.core  # noqa: F401 (populate registries)
from speech_aware_evidence_acquisition.contracts import ExecutionPlan
from speech_aware_evidence_acquisition.core.base import CoreError, RunResult
from speech_aware_evidence_acquisition.core.config import ComposedConfig
from speech_aware_evidence_acquisition.core.driver import load_split, run_experiment
from speech_aware_evidence_acquisition.data.lock import load_lock
from speech_aware_evidence_acquisition.data.splits import discovery_split, freeze_splits


class _OpenGate:
    def assert_model_touch_allowed(self, plan):
        pass


def _composed(**overrides):
    values = {
        "carrier_lock_key": "earnings21-original",
        "split_name": "discovery",
        "arm": "bare-core",
        "policy": "fixed",
        "evidence_source": "none",
        "evidence_mismatch": False,
        "scorers": ["asr-wer"],
        "task_instruction": "Transcribe.",
        "decoding_params": {"temperature": 0, "seed": 20260803},
        "experiment_id": "SAEA-E-000",
    }
    values.update(overrides)
    return ComposedConfig(
        values=values, config_hash="d" * 64,
        fragments={"model": "m", "dataset": "d", "baseline": "b", "experiment": "e"},
    )


def _plan(split_hash, **overrides):
    base = dict(
        run_id="SAEA-E-000-driver",
        execution_profile="bounded-discovery-probe",
        carrier_lock_key="earnings21-original",
        split_role="discovery",
        split_identity_hash=split_hash,
        planned_model_calls=10,
        planned_gpu_hours=1.0,
        planned_speech_audio_seconds=1000,
        protocol_hash="b" * 64,
    )
    base.update(overrides)
    return ExecutionPlan(**base)


def _transport(request_bytes):
    return json.dumps({"text": "token tags", "usage": {"prompt_tokens": 3}}).encode()


def _frozen_world(synthetic_world, tmp_path):
    lock = load_lock(synthetic_world.lock_path)
    receipts = tmp_path / "repo" / "docs" / "receipts"
    freeze_splits(lock, synthetic_world.data_root, receipts)
    return lock, tmp_path / "repo"


def test_run_experiment_end_to_end(synthetic_world, tmp_path):
    lock, repo_root = _frozen_world(synthetic_world, tmp_path)
    ids, split_hash = load_split(repo_root, "discovery")
    assert len(ids) == 3
    result = run_experiment(
        composed=_composed(),
        plan=_plan(split_hash),
        gate=_OpenGate(),
        lock=lock,
        root=synthetic_world.data_root,
        run_dir=tmp_path / "run",
        transport=_transport,
        repo_root=repo_root,
    )
    assert isinstance(result, RunResult)
    lines = result.outputs_path.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 3
    assert result.cost["calls_used"] == 3
    manifest = json.loads(
        (tmp_path / "run" / "SAEA-E-000-driver.trace-manifest.json").read_text("utf-8")
    )["records"]
    assert any(record_id.endswith("/obs") for record_id in manifest)
    assert any(record_id.endswith("/use") for record_id in manifest)


def test_run_experiment_refuses_wrong_split_hash(synthetic_world, tmp_path):
    lock, repo_root = _frozen_world(synthetic_world, tmp_path)
    with pytest.raises(CoreError, match="split"):
        run_experiment(
            composed=_composed(),
            plan=_plan("f" * 64),
            gate=_OpenGate(),
            lock=lock,
            root=synthetic_world.data_root,
            run_dir=tmp_path / "run",
            transport=_transport,
            repo_root=repo_root,
        )


def test_run_experiment_supplies_evidence_with_org_and_supply_traces(
    synthetic_world, tmp_path
):
    lock, repo_root = _frozen_world(synthetic_world, tmp_path)
    _, split_hash = load_split(repo_root, "discovery")
    result = run_experiment(
        composed=_composed(arm="fixed-legal-context", evidence_source="conec-contexts"),
        plan=_plan(split_hash),
        gate=_OpenGate(),
        lock=lock,
        root=synthetic_world.data_root,
        run_dir=tmp_path / "run2",
        transport=_transport,
        repo_root=repo_root,
    )
    manifest = json.loads(
        (tmp_path / "run2" / "SAEA-E-000-driver.trace-manifest.json").read_text("utf-8")
    )["records"]
    assert any(record_id.endswith("/org") for record_id in manifest)
    assert any(record_id.endswith("/supply") for record_id in manifest)
    assert result.arm == "fixed-legal-context"
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `pytest tests/unit/test_driver.py -v`
Expected: FAIL with `ModuleNotFoundError` (`core.driver`; the `core` package import may also fail until `__init__` is finalized — finalize it in Step 3)

- [ ] **Step 3: Implement `core/driver.py` and finalize `core/__init__.py`**

`core/driver.py`:

```python
"""The ONE experiment driver: config + plan -> gate -> run -> outputs (R0).

Every Stage-2 run (R0 smoke, R1 reproduction, X probes, 2B deep digs) goes
through run_experiment(); an experiment differs from another only by its four
config fragments and, rarely, a newly registered component. RUNTIME PHASE:
this module never imports data.references.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Callable, Mapping

from ..contracts import ExecutionPlan
from ..e0.artifacts import REPO_ROOT
from ..data.splits import SPLITS_RECEIPT_NAME
from .base import (
    CARRIERS,
    EVIDENCE_SOURCES,
    POLICIES,
    SCORERS,
    TRANSPORTS,
    CoreError,
    RunResult,
    SampleContext,
)
from .config import ComposedConfig, compose
from .evidence import rotated_mismatch
from .model import FrozenCoreAdapter
from .tracing import TraceSink


def load_split(repo_root: Path, split_name: str) -> tuple[set[str], str]:
    receipt_path = Path(repo_root) / "docs" / "receipts" / SPLITS_RECEIPT_NAME
    if not receipt_path.is_file():
        raise CoreError(f"splits receipt missing: {receipt_path} (freeze splits first)")
    document = json.loads(receipt_path.read_text(encoding="utf-8"))
    try:
        split = document["splits"][split_name]
    except KeyError:
        raise CoreError(
            f"unknown split {split_name!r}; frozen splits: {sorted(document['splits'])}"
        ) from None
    ids = {prefixed.split("/", 1)[1] for prefixed in split["ids"]}
    return ids, split["identity_hash"]


def run_experiment(
    composed: ComposedConfig,
    plan: ExecutionPlan,
    gate: object,
    lock: Mapping[str, object],
    root: Path,
    run_dir: Path,
    transport: Callable[[bytes], bytes],
    repo_root: Path = REPO_ROOT,
) -> RunResult:
    values = composed.values
    arm = str(values["arm"])
    sample_ids, split_hash = load_split(repo_root, str(values["split_name"]))
    if plan.split_identity_hash != split_hash:
        raise CoreError(
            "plan split identity hash does not match the frozen splits receipt "
            f"for split {values['split_name']!r}"
        )
    loader = CARRIERS.resolve(str(values["carrier_lock_key"]))
    samples = [s for s in loader(lock, root) if s.sample_id in sample_ids]
    if {s.sample_id for s in samples} != sample_ids:
        raise CoreError("split ids missing from the carrier's loaded samples")
    source = EVIDENCE_SOURCES.resolve(str(values.get("evidence_source", "none")))
    evidence_by_sample = {
        s.sample_id: source(lock, root, s.sample_id) for s in samples
    }
    if values.get("evidence_mismatch", False):
        evidence_by_sample = rotated_mismatch(evidence_by_sample)
    policy = POLICIES.resolve(str(values["policy"]))
    sink = TraceSink(run_dir, plan.run_id)
    adapter = FrozenCoreAdapter(
        gate=gate, plan=plan, arm=arm, transport=transport, sink=sink
    )
    outputs_path = Path(run_dir) / f"{plan.run_id}.outputs.jsonl"
    with outputs_path.open("w", encoding="utf-8", newline="\n") as outputs:
        for index, sample in enumerate(sorted(samples, key=lambda s: s.sample_id), start=1):
            request_id_base = f"req-{index:04d}"
            view = sample.runtime_view()
            sink.emit(
                "OBS",
                f"{request_id_base}/obs",
                {
                    "obs_speech_ref": view["speech_ref"],
                    "obs_audio_seconds": view["audio_seconds"],
                },
            )
            evidence = evidence_by_sample.get(sample.sample_id, [])
            if evidence:
                sink.emit(
                    "ORG",
                    f"{request_id_base}/org",
                    {
                        "org_evidence_count": len(evidence),
                        "org_source_lock_keys": sorted(
                            {item.provenance["lock_key"] for item in evidence}
                        ),
                    },
                )
                sink.emit(
                    "SUPPLY",
                    f"{request_id_base}/supply",
                    {
                        "supply_evidence_ids": [item.evidence_id for item in evidence],
                        "supply_content_bytes": sum(
                            len(item.content.encode("utf-8")) for item in evidence
                        ),
                    },
                )
            ctx = SampleContext(
                sample=sample,
                evidence=evidence,
                adapter=adapter,
                sink=sink,
                arm=arm,
                task_instruction=str(values["task_instruction"]),
                decoding_params=dict(values.get("decoding_params", {})),
                request_id_base=request_id_base,
                retrieval_query=values.get("retrieval_query"),
            )
            outcome = policy.run_sample(ctx)
            outputs.write(
                json.dumps(
                    {
                        "request_id": request_id_base,
                        "sample_id": outcome.sample_id,
                        "carrier_lock_key": sample.carrier_lock_key,
                        "arm": arm,
                        "text": outcome.text,
                        "admitted": outcome.admitted,
                        "request_sha256": outcome.request_sha256,
                        "response_sha256": outcome.response_sha256,
                    },
                    ensure_ascii=False,
                    sort_keys=True,
                )
                + "\n"
            )
    manifest_hash = sink.close()
    return RunResult(
        run_id=plan.run_id,
        arm=arm,
        outputs_path=outputs_path,
        trace_manifest_hash=manifest_hash,
        cost=adapter.cost_summary(),
    )


def _cli_score(args: argparse.Namespace) -> int:
    from ..data.lock import data_root, load_lock, umbrella_lock_path

    lock = load_lock(umbrella_lock_path())
    root = data_root()
    for name in args.scorers.split(","):
        scores = SCORERS.resolve(name.strip())(Path(args.outputs), lock, root)
        print(json.dumps({name.strip(): scores["aggregate"]}, indent=2, sort_keys=True))
    return 0


def _cli_run(args: argparse.Namespace) -> int:
    from ..contracts import FrozenCoreGate
    from ..data.lock import data_root, load_lock, umbrella_lock_path

    lock = load_lock(umbrella_lock_path())
    root = data_root()
    composed = compose(REPO_ROOT, args.model, args.dataset, args.baseline, args.experiment)
    plan = ExecutionPlan(**json.loads(Path(args.plan).read_text(encoding="utf-8")))
    gate = FrozenCoreGate.for_study_repo(REPO_ROOT, root, Path(args.runtime_root))
    transport_factory = TRANSPORTS.resolve(str(composed.values["transport"]))
    transport = transport_factory(composed.values, root)
    result = run_experiment(
        composed, plan, gate, lock, root, Path(args.run_dir), transport
    )
    print(json.dumps({"run_id": result.run_id, "cost": dict(result.cost)}, indent=2))
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="saea-driver")
    sub = parser.add_subparsers(dest="command", required=True)
    score = sub.add_parser("score", help="model-free scoring of recorded outputs")
    score.add_argument("--outputs", required=True)
    score.add_argument("--scorers", default="asr-wer")
    score.set_defaults(func=_cli_score)
    run = sub.add_parser("run", help="gate-enforced live run (requires a plan file)")
    run.add_argument("--model", required=True)
    run.add_argument("--dataset", required=True)
    run.add_argument("--baseline", required=True)
    run.add_argument("--experiment", required=True)
    run.add_argument("--plan", required=True)
    run.add_argument("--run-dir", required=True)
    run.add_argument("--runtime-root", required=True)
    run.set_defaults(func=_cli_run)
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
```

Check `FrozenCoreGate.for_study_repo`'s actual signature in `contracts.py` before wiring `_cli_run` (it exists as the canonical factory; follow its real parameter names — do not change contracts.py).

Finalize `core/__init__.py`:

```python
"""Shared Stage-2 engineering foundation (R0): one registry, one driver.

Importing this package registers all built-in components (carriers, evidence
sources, transports, policies, scorers).
"""

from . import carriers, evidence, model, policies, scorers  # noqa: F401 (registration)
from .base import (
    CARRIERS,
    EVIDENCE_SOURCES,
    POLICIES,
    SCORERS,
    TRANSPORTS,
    CoreError,
    EvidenceError,
    EvidenceItem,
    RunResult,
    SampleContext,
    SampleOutcome,
)
from .config import ComposedConfig, ConfigError, compose, protocol_hash
from .driver import load_split, run_experiment
from .model import CoreResponse, FrozenCoreAdapter, FrozenCoreError, LlamaServerTransport
from .tracing import TraceSink, TraceSinkError

__all__ = [
    "CARRIERS", "EVIDENCE_SOURCES", "POLICIES", "SCORERS", "TRANSPORTS",
    "ComposedConfig", "ConfigError", "CoreError", "CoreResponse",
    "EvidenceError", "EvidenceItem", "FrozenCoreAdapter", "FrozenCoreError",
    "LlamaServerTransport", "RunResult", "SampleContext", "SampleOutcome",
    "TraceSink", "TraceSinkError", "compose", "load_split", "protocol_hash",
    "run_experiment",
]
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/unit/test_driver.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/speech_aware_evidence_acquisition/core tests/unit/test_driver.py
git commit -m "feat(r0): single experiment driver + CLI - config in, gated run out"
```

---

### Task 12: `core/tracking.py` (MLflow + ledger row) + delete the stub packages

**Files:**
- Create: `src/speech_aware_evidence_acquisition/core/tracking.py`
- Modify: `src/speech_aware_evidence_acquisition/core/__init__.py` (add tracking exports)
- Modify: `pyproject.toml` (add `[project.optional-dependencies] tracking = ["mlflow>=2.14"]`)
- Delete: `src/speech_aware_evidence_acquisition/models/`, `.../evidence/`, `.../tracing/`, `.../experiments/` (the four one-line stub packages)
- Test: `tests/unit/test_tracking.py`

**Interfaces:**
- Consumes: `core.base.RunResult`, `core.config.ComposedConfig`, `contracts.ExecutionPlan`.
- Produces:
  - `LEDGER_COLUMNS: tuple[str, ...]` — exactly the 21 umbrella experiment-index columns in order: `("experiment_id", "date", "speech task/carrier", "changed axes", "study commit", "shared code revision", "config hash", "protocol hash", "model rev", "dataset rev", "split role", "split identity hash", "consumed", "MLflow run", "artifact location", "artifact hashes", "effectiveness", "reasonableness", "efficiency", "deviations", "decision")`
  - `ledger_row(cells: Mapping[str, str]) -> str` — one markdown row; requires exactly the `LEDGER_COLUMNS` keys; refuses `|` inside cells.
  - `class MlflowUnavailable(RuntimeError)`; `log_run(result, composed, plan, protocol, tracking_uri, metrics=None) -> str` — lazy `import mlflow`; logs params (`arm`, `config_hash`, `protocol_hash`, `split_role`, `split_identity_hash`, `execution_profile`, `carrier_lock_key`), metrics (numeric cost + optional extra), artifacts (outputs + trace manifest); returns the MLflow run id.

- [ ] **Step 1: Write the failing tests**

`tests/unit/test_tracking.py`:

```python
"""MLflow linkage (stubbed) and the umbrella ledger row renderer."""

import sys
import types

import pytest

from speech_aware_evidence_acquisition.core.tracking import (
    LEDGER_COLUMNS,
    MlflowUnavailable,
    ledger_row,
)


def test_ledger_columns_match_the_umbrella_table_exactly():
    assert len(LEDGER_COLUMNS) == 21
    assert LEDGER_COLUMNS[0] == "experiment_id"
    assert LEDGER_COLUMNS[-1] == "decision"
    assert "split identity hash" in LEDGER_COLUMNS


def test_ledger_row_renders_and_validates():
    cells = {column: f"v{i}" for i, column in enumerate(LEDGER_COLUMNS)}
    row = ledger_row(cells)
    assert row.startswith("| v0 |") and row.endswith("| v20 |")
    with pytest.raises(ValueError, match="exactly"):
        ledger_row({"experiment_id": "x"})
    bad = dict(cells)
    bad["decision"] = "a|b"
    with pytest.raises(ValueError, match="pipe"):
        ledger_row(bad)


def test_log_run_requires_mlflow(monkeypatch):
    # sys.modules["mlflow"] = None makes `import mlflow` raise ImportError even
    # when mlflow IS installed in this environment.
    monkeypatch.setitem(sys.modules, "mlflow", None)
    from speech_aware_evidence_acquisition.core import tracking

    with pytest.raises(MlflowUnavailable, match="tracking"):
        tracking._require_mlflow()


def test_log_run_with_stub_mlflow(tmp_path, monkeypatch):
    calls = {"params": {}, "metrics": {}, "artifacts": []}
    stub = types.SimpleNamespace(
        set_tracking_uri=lambda uri: calls.setdefault("uri", uri),
        set_experiment=lambda name: calls.setdefault("experiment", name),
        start_run=lambda run_name: types.SimpleNamespace(
            __enter__=lambda s: types.SimpleNamespace(
                info=types.SimpleNamespace(run_id="mlrun-1")
            ),
            __exit__=lambda s, *a: False,
        ),
        log_params=lambda params: calls["params"].update(params),
        log_metrics=lambda metrics: calls["metrics"].update(metrics),
        log_artifact=lambda path: calls["artifacts"].append(path),
    )
    monkeypatch.setitem(sys.modules, "mlflow", stub)

    from speech_aware_evidence_acquisition.contracts import ExecutionPlan
    from speech_aware_evidence_acquisition.core.base import RunResult
    from speech_aware_evidence_acquisition.core.config import ComposedConfig
    from speech_aware_evidence_acquisition.core.tracking import log_run

    outputs = tmp_path / "SAEA-E-000-x.outputs.jsonl"
    outputs.write_text("{}\n", encoding="utf-8")
    (tmp_path / "SAEA-E-000-x.trace-manifest.json").write_text("{}", encoding="utf-8")
    result = RunResult(
        run_id="SAEA-E-000-x", arm="bare-core", outputs_path=outputs,
        trace_manifest_hash="c" * 64,
        cost={"calls_used": 2, "audio_seconds_used": 20.0,
              "latency_seconds_total": 1.0, "prompt_tokens_total": 5,
              "completion_tokens_total": 4},
    )
    composed = ComposedConfig(
        values={"arm": "bare-core"}, config_hash="d" * 64,
        fragments={"model": "m", "dataset": "d", "baseline": "b", "experiment": "e"},
    )
    plan = ExecutionPlan(
        run_id="SAEA-E-000-x", execution_profile="bounded-discovery-probe",
        carrier_lock_key="earnings22-original", split_role="dev",
        split_identity_hash="a" * 64, planned_model_calls=5, planned_gpu_hours=1.0,
        planned_speech_audio_seconds=100, protocol_hash="b" * 64,
    )
    run_id = log_run(result, composed, plan, "b" * 64, tracking_uri=str(tmp_path / "mlruns"))
    assert run_id == "mlrun-1"
    assert calls["params"]["arm"] == "bare-core"
    assert calls["metrics"]["calls_used"] == 2
    assert len(calls["artifacts"]) == 2
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/unit/test_tracking.py -v`
Expected: FAIL with `ModuleNotFoundError`

- [ ] **Step 3: Implement `core/tracking.py`**

```python
"""MLflow linkage and the umbrella experiment-index row renderer (R0).

mlflow is an optional extra (`pip install -e ".[tracking]"`); the import is
lazy so the model-free test environment never needs it.
"""

from __future__ import annotations

from typing import Mapping

from ..contracts import ExecutionPlan
from .base import RunResult
from .config import ComposedConfig

LEDGER_COLUMNS: tuple[str, ...] = (
    "experiment_id", "date", "speech task/carrier", "changed axes", "study commit",
    "shared code revision", "config hash", "protocol hash", "model rev", "dataset rev",
    "split role", "split identity hash", "consumed", "MLflow run", "artifact location",
    "artifact hashes", "effectiveness", "reasonableness", "efficiency", "deviations",
    "decision",
)


class MlflowUnavailable(RuntimeError):
    """mlflow is not installed in this environment."""


def _require_mlflow():
    try:
        import mlflow
    except ImportError as error:
        raise MlflowUnavailable(
            'mlflow is required for run tracking: pip install -e ".[tracking]"'
        ) from error
    return mlflow


def ledger_row(cells: Mapping[str, str]) -> str:
    if set(cells) != set(LEDGER_COLUMNS):
        raise ValueError(
            f"ledger row must have exactly the columns {LEDGER_COLUMNS}; got {sorted(cells)}"
        )
    for column, value in cells.items():
        if "|" in value:
            raise ValueError(f"ledger cell {column!r} contains a pipe character")
    return "| " + " | ".join(cells[column] for column in LEDGER_COLUMNS) + " |"


def log_run(
    result: RunResult,
    composed: ComposedConfig,
    plan: ExecutionPlan,
    protocol: str,
    tracking_uri: str,
    metrics: Mapping[str, float] | None = None,
) -> str:
    mlflow = _require_mlflow()
    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment("speech-aware-evidence-acquisition")
    with mlflow.start_run(run_name=plan.run_id) as active:
        mlflow.log_params(
            {
                "arm": result.arm,
                "config_hash": composed.config_hash,
                "protocol_hash": protocol,
                "split_role": plan.split_role,
                "split_identity_hash": plan.split_identity_hash,
                "execution_profile": plan.execution_profile,
                "carrier_lock_key": plan.carrier_lock_key,
            }
        )
        numeric_cost = {
            key: float(value)
            for key, value in result.cost.items()
            if isinstance(value, (int, float))
        }
        mlflow.log_metrics({**numeric_cost, **(dict(metrics) if metrics else {})})
        mlflow.log_artifact(str(result.outputs_path))
        manifest = result.outputs_path.with_name(f"{result.run_id}.trace-manifest.json")
        mlflow.log_artifact(str(manifest))
        return active.info.run_id
```

Add to `core/__init__.py` exports: `from .tracking import LEDGER_COLUMNS, MlflowUnavailable, ledger_row, log_run` (+ `__all__` entries). Add to `pyproject.toml`:

```toml
tracking = ["mlflow>=2.14"]
```

- [ ] **Step 4: Delete the four stub packages**

First verify nothing references them: `grep -rn "speech_aware_evidence_acquisition\.\(models\|evidence\|tracing\|experiments\)" src tests docs scripts` must return nothing (the new code lives under `core.*`). Then `git rm -r src/speech_aware_evidence_acquisition/models src/speech_aware_evidence_acquisition/evidence src/speech_aware_evidence_acquisition/tracing src/speech_aware_evidence_acquisition/experiments`.

- [ ] **Step 5: Run the FULL suite (foundation gate), then commit**

Run: `pytest`
Expected: PASS, zero failures — the Part-1 foundation is complete.

```bash
git add -A src/speech_aware_evidence_acquisition tests/unit/test_tracking.py pyproject.toml
git commit -m "feat(r0): tracking linkage + ledger renderer; consolidate foundation into core/ (stub packages removed)"
```

---

# Part 2 — Config-driven instantiation

### Task 13: Entrypoints — `reproduce.sh` / `evaluate.sh` wrap the shared driver (model-free)

**Files:**
- Modify: `scripts/reproduce.sh`
- Modify: `scripts/evaluate.sh`
- Modify: `tests/contract/test_scripts_fail_closed.py`

**Interfaces:**
- Consumes: `python -m speech_aware_evidence_acquisition.e0.generate verify` (existing gate dry-run) and `python -m speech_aware_evidence_acquisition.core.driver score`.
- Produces: functional, **model-free** entrypoints. Neither script contains any model-touch path (no llama-server launch, no chat-completions call); the live `driver run` subcommand is reachable only by explicitly authoring a plan file, never from these scripts.

- [ ] **Step 1: Update the contract test first (it defines the new behavior)**

Rewrite `tests/contract/test_scripts_fail_closed.py`:

```python
"""Contract 7 (R0 form): entrypoints are model-free and fail closed on misuse."""

import os
import shutil
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]

pytestmark = pytest.mark.skipif(
    os.name == "nt" or shutil.which("bash") is None,
    reason="entrypoint behavior is exercised in the POSIX runtime environment",
)


@pytest.mark.parametrize("script", ["reproduce.sh", "evaluate.sh"])
def test_help_is_model_free_and_exits_zero(script):
    completed = subprocess.run(
        ["bash", str(REPO_ROOT / "scripts" / script), "--help"],
        check=False, capture_output=True, text=True,
    )
    assert completed.returncode == 0
    assert "model-free" in completed.stdout


def test_evaluate_without_outputs_refuses_with_exit_2():
    completed = subprocess.run(
        ["bash", str(REPO_ROOT / "scripts" / "evaluate.sh")],
        check=False, capture_output=True, text=True,
    )
    assert completed.returncode == 2
    assert "usage" in completed.stderr.lower()


@pytest.mark.parametrize("script", ["reproduce.sh", "evaluate.sh"])
def test_entrypoints_contain_no_model_touch_path(script):
    text = (REPO_ROOT / "scripts" / script).read_text(encoding="utf-8")
    assert "llama-server" not in text
    assert "chat/completions" not in text
    assert "driver run" not in text
```

- [ ] **Step 2: Run to verify the new expectations fail (WSL)**

Run: `wsl -d Ubuntu-24.04 -- bash -lc "cd /mnt/d/chao_workspace/exploring-l4-intelligence/studies/speech-aware-evidence-acquisition && source ~/.venvs/speechrl/bin/activate && pytest tests/contract/test_scripts_fail_closed.py -v"`
Expected: FAIL (`--help` currently exits 2 without "model-free")

- [ ] **Step 3: Rewrite the scripts**

`scripts/reproduce.sh`:

```bash
#!/usr/bin/env bash
# Model-free reproduction entrypoint (R0). This script never touches the model:
# a model-facing run additionally requires a validated ExecutionPlan file and a
# pre-registered exposure ledger row, driven explicitly from Python — never here.
set -euo pipefail

usage() {
  cat <<'EOF'
usage: reproduce.sh [--help]

Runs the model-free verification chain: the E0 closure + runtime receipt gate
dry-run (authorizes nothing). Requires SPEECHRL_DATA_DIR and the pinned
runtime per docs/engineering.md.
EOF
}

if [[ "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

export PYTHONDONTWRITEBYTECODE=1
python -m speech_aware_evidence_acquisition.e0.generate verify
```

`scripts/evaluate.sh`:

```bash
#!/usr/bin/env bash
# Model-free scoring entrypoint (R0): scores a recorded outputs JSONL against
# the frozen scoring stack via the shared driver. Never touches the model.
set -euo pipefail

usage() {
  cat <<'EOF'
usage: evaluate.sh <outputs.jsonl> [scorers]

model-free scoring of a recorded run outputs file (frozen saea-scoring-v1).
Default scorers: asr-wer. Requires SPEECHRL_DATA_DIR for reference layers.
EOF
}

if [[ "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi
if [[ $# -lt 1 ]]; then
  usage >&2
  exit 2
fi

export PYTHONDONTWRITEBYTECODE=1
python -m speech_aware_evidence_acquisition.core.driver score \
  --outputs "$1" --scorers "${2:-asr-wer}"
```

- [ ] **Step 4: Run the contract test to verify it passes (WSL), then commit**

Run: same WSL command as Step 2 — Expected: PASS.

```bash
git add scripts/reproduce.sh scripts/evaluate.sh tests/contract/test_scripts_fail_closed.py
git commit -m "feat(r0): model-free reproduce/evaluate entrypoints wrap the shared driver"
```

---

### Task 14: R0 smoke runbook + engineering doc + full-suite gate on both OSes

**Files:**
- Create: `docs/runbooks/2026-08-05-r0-smoke.md`
- Modify: `docs/engineering.md` (append an "R0 engineering baseline" subsection after the E0 closure section)

**Interfaces:**
- Consumes: everything delivered above; `docs/receipts/splits.json` (dev split hash).
- Produces: the runbook a **future, owner-visible session** follows for the first model touch. This task performs **no model touch and appends no ledger row**.

- [ ] **Step 1: Write `docs/runbooks/2026-08-05-r0-smoke.md`**

```markdown
# R0 smoke runbook (SAEA-E-001) — NOT EXECUTED BY THE R0 DELIVERY PLAN

Purpose: first model touch — wiring and measurement-integrity smoke of the
bare-core arm on the dev subset10. Bounded-discovery-probe; no superiority
claim. Executing this runbook is an owner-visible action: it appends an
exposure ledger row before any result is read.

## Preconditions (all machine-checked at the gate)

1. Clean study tree at the delivered R0 commit; receipts intact
   (`pytest tests/contract/test_real_receipts.py`).
2. `docs/receipts/splits.json` frozen (dev split hash read from the file).
3. WSL Ubuntu-24.04; `source ~/.venvs/speechrl/bin/activate`;
   `SPEECHRL_DATA_DIR=/mnt/e/chao_workspace/exploring-l4-intelligence/speechrl-data`.
4. Bytecode discipline: `export PYTHONDONTWRITEBYTECODE=1`; remove any
   `src/speech_aware_evidence_acquisition/scoring/__pycache__`.
5. llama-server from the receipt-pinned build (`/home/chao/llama.cpp`, commit
   `fdbd6abee20e408de21e90ca77a24cd50a6ea073`) serving the lock-pinned GGUF;
   `llama-server --version` must report `(fdbd6ab)` before starting.

## Execution plan file (values to instantiate verbatim)

Write `$SPEECHRL_DATA_DIR/runs/SAEA-E-001-r0-smoke/plan.json`:

- run_id: `SAEA-E-001-r0-smoke`
- execution_profile: `bounded-discovery-probe`
- carrier_lock_key: `earnings22-original`
- split_role: `dev`
- split_identity_hash: the `dev` hash in `docs/receipts/splits.json`
- planned_model_calls: `12` (10 samples + 2 retries)
- planned_gpu_hours: `2.0`
- planned_speech_audio_seconds: sum of subset10 `audio_seconds` from
  `load_earnings22` filtered to `earnings22_subset10_ids`, rounded up
- protocol_hash: `protocol_hash(compose(REPO_ROOT, "qwen3-omni-llamacpp",
  "earnings22-dev-subset10", "bare-core", "r0-smoke").config_hash,
  "bare-core", <dev split hash>)`

## Sequence

1. Append the exposure ledger row (consumed=no, budgets as above) — BEFORE
   any request.
2. Run through the ONE driver path:
   `python -m speech_aware_evidence_acquisition.core.driver run
   --model qwen3-omni-llamacpp --dataset earnings22-dev-subset10
   --baseline bare-core --experiment r0-smoke
   --plan <plan.json> --run-dir $SPEECHRL_DATA_DIR/runs/SAEA-E-001-r0-smoke
   --runtime-root /home/chao/llama.cpp`
3. Score: `bash scripts/evaluate.sh <outputs.jsonl>`; log to MLflow
   (`core.tracking.log_run`, tracking dir on ext4 per umbrella policy).
4. Draft the umbrella experiment-index row with `core.tracking.ledger_row`;
   register it in the umbrella wiki (separate umbrella commit).
5. Write the wiring-integrity memo: traces complete (OBS/USE per sample;
   ORG/SUPPLY absent for bare-core), budgets respected, hashes recorded —
   the R0 exit criterion is measurement integrity, not a result claim.
```

- [ ] **Step 2: Append to `docs/engineering.md`** (after the E0 closure section)

```markdown
## R0 engineering baseline (delivered 2026-08-05)

Two-layer structure (owner direction 2026-08-05: maximize reuse, no
fragmentation). Layer 1 — ONE foundation package `core/`: one `Registry`
mechanism with five seams (CARRIERS, EVIDENCE_SOURCES, TRANSPORTS, POLICIES,
SCORERS), one gate-bound request path (`FrozenCoreAdapter` — D2 allowlist
exact-set choke point, per-plan budget metering), one experiment driver
(`core.driver.run_experiment`), append-only trace sink (repo-refusal), lazy
MLflow linkage + umbrella ledger-row renderer. Shared data layer:
`data/splits.py` (frozen partition, receipt `docs/receipts/splits.json`,
hash convention identical to the E0 ledger row), `data/references.py`
(scoring-side; only `core/scorers.py` may import it — AST contract test).
Layer 2 — experiments are configuration: four disjoint JSON fragments
(`configs/{model,dataset,baseline,experiment}/`); a new experiment is config
plus at most one newly registered component. Policies compose over the three
D2-frozen arm shapes; only `fixed` is implemented (X1/X3/X4 policies register
later without driver changes). Entrypoints `scripts/reproduce.sh` /
`scripts/evaluate.sh` are functional and model-free. First model touch:
`docs/runbooks/2026-08-05-r0-smoke.md` (owner-visible; requires ExecutionPlan
+ pre-registered exposure row; not executed by the delivery plan).
```

- [ ] **Step 3: Run the full suite on Windows**

Run: `pytest`
Expected: PASS, zero failures.

- [ ] **Step 4: Run the full suite in WSL (POSIX-only tests included)**

Run: `wsl -d Ubuntu-24.04 -- bash -lc "cd /mnt/d/chao_workspace/exploring-l4-intelligence/studies/speech-aware-evidence-acquisition && source ~/.venvs/speechrl/bin/activate && uv pip install -e '.[dev]' -q && pytest -q"`
Expected: PASS including the entrypoint contract and the real-receipt suite.

- [ ] **Step 5: Commit**

```bash
git add docs/runbooks/2026-08-05-r0-smoke.md docs/engineering.md
git commit -m "docs(r0): smoke runbook (not executed) + engineering map for the two-layer baseline"
```

---

## Self-Review Notes (kept for the executor)

- **Spec coverage:** design §5 lane A → Task 1; §3 splits → Task 2; §7 2A-R0.2 two-layer baseline → Tasks 4–12 (Layer 1) + 8/13/14 (Layer 2); entry-contract R0 deliverables: deterministic loaders → Task 3; evidence schema + negative/oracle controls → Tasks 4+6; four-axis trace → Tasks 5+11; frozen-core adapter → Task 7; config composition → Task 8; three engineering controls → Task 9 (arms) + Task 8 (configs); discovery/confirmatory paths → Tasks 2+11 (driver refuses plans whose split hash mismatches the frozen receipt; confirmatory stays unread); scorer adapters → Task 10; MLflow/umbrella linkage + cost accounting → Tasks 7+12; entrypoints → Task 13; smoke preparation (not execution) → Task 14. R1/X probes are **out of scope by design** — planned after the readiness memo and the owner's R1 decision, as configs + registered components over this foundation.
- **Anti-fragmentation invariants** (report any violation instead of working around it): exactly one `Registry` class; exactly one request path (`FrozenCoreAdapter.request`); exactly one driver (`run_experiment`); the four stub packages are gone after Task 12; no experiment-specific wiring module ever gets added — if a task seems to need one, the seam is wrong, stop and surface it.
- **Known intentional deferrals** (not placeholders): entity/QA reference extraction from `wer_tags`/ConEC annotations — specified with the probe that first consumes it (readiness memo pins the format); oracle-evidence computation — the registered source refuses at runtime until then; GPU/CPU accounting at R0 = registered plan ceilings + per-request latency totals (server is GPU-resident, latency is the occupancy proxy; direct GPU sampling specified with R1 if the memo shows it matters); X1/X3/X4 policies — the seam exists, implementations register later.
- **Adaptation points** (bounded to "follow the existing code, don't invent"): Task 2 (lock.py export names), Task 3 (real CSV header check), Task 7 Step 6 (GateFixture helper names), Task 11 (`FrozenCoreGate.for_study_repo` parameter names).
