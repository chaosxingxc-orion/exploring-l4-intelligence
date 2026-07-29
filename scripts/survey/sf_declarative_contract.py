#!/usr/bin/env python3
"""Declarative contract engine for prose/JSONL Stage-1A survey contracts.

Schema ``sf-declarative-contract-v1``.  Contract documents live under
``docs/contracts/<contract_id>.json`` and are parsed with the strict,
duplicate-key-rejecting loader in ``sf_json_contract``.  Each contract is an
ordered list of ``cases``; every case expresses exactly one of four
primitives that previously lived as bespoke ``unittest`` assertions in
``scripts/survey/test_sf_r1_problem_definition.py``,
``scripts/survey/test_sf_r2_problem_definition.py``, and part of
``scripts/survey/test_sf_stage1c_common_rubric.py``:

* ``must_contain`` / ``must_not_contain`` — every string in ``strings``
  (checked verbatim, no normalization) is present (or absent) in the exact
  UTF-8 text of one ``target`` file or every file in a ``targets`` list.
* ``jsonl_key_set_equality`` — across every row of a JSONL ``target``, the
  set of ``field`` values equals the configured ``values`` set, and the
  ``unique_field`` values are pairwise distinct.
* ``registry_ledger_binding`` — replicates the retired R1 registry <->
  fulltext-ledger hash binding.  For every row of the ``registry`` JSONL and
  every entry in ``kinds``, a ledger row keyed by ``(id_field, "kind")`` must
  exist with ``http_status == 200``, ``error`` null, a nonempty
  ``stored_at``, and a ``sha256`` equal to the registry row's
  ``provenance.<kind>_sha256``.  Every registry row's own ``schema`` field
  must equal the configured ``schema``.

The engine is stdlib-only, performs no network access, and never writes to
the repository.  Exit 0 means every case in every checked contract passed;
exit 1 means at least one case failed or a contract/target was malformed.
"""

from __future__ import annotations

import sys

# Direct script execution always places an attacker-controllable script directory
# at sys.path[0]. Remove it before importing anything except built-in ``sys``;
# module imports retain their caller-managed import path unchanged.
if __name__ == "__main__" and sys.path:
    del sys.path[0]
sys.dont_write_bytecode = True

import argparse
from pathlib import Path, PurePosixPath
from typing import Any

REPO = Path(__file__).resolve().parents[2]
SURVEY_DIR = Path(__file__).resolve().parent
if str(SURVEY_DIR) not in sys.path:
    sys.path.insert(0, str(SURVEY_DIR))

from sf_json_contract import (  # noqa: E402
    JsonContractError,
    loads as strict_json_loads,
    loads_jsonl as strict_jsonl_loads,
)

CONTRACTS_DIR = REPO / "docs" / "contracts"
KNOWN_CASE_TYPES = (
    "must_contain",
    "must_not_contain",
    "jsonl_key_set_equality",
    "registry_ledger_binding",
)


class DeclarativeContractError(ValueError):
    """A contract document, case, or target file violates the engine's schema."""


def _canonical_relative(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise DeclarativeContractError(f"{label} must be a nonempty string")
    path = PurePosixPath(value)
    if (
        "\\" in value
        or path.is_absolute()
        or value != path.as_posix()
        or any(part in ("", ".", "..") for part in path.parts)
    ):
        raise DeclarativeContractError(
            f"{label} is not a canonical repository-relative path: {value!r}"
        )
    return value


def _resolve(relative: str) -> Path:
    return REPO.joinpath(*relative.split("/"))


def _read_text(relative: str) -> str:
    relative = _canonical_relative(relative, "target")
    path = _resolve(relative)
    try:
        raw = path.read_bytes()
    except OSError as error:
        raise DeclarativeContractError(f"cannot read {relative}: {error}") from error
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError as error:
        raise DeclarativeContractError(f"{relative} is not valid UTF-8: {error}") from error


def _read_jsonl(relative: str) -> list[dict]:
    relative = _canonical_relative(relative, "target")
    path = _resolve(relative)
    try:
        raw = path.read_bytes()
    except OSError as error:
        raise DeclarativeContractError(f"cannot read {relative}: {error}") from error
    try:
        rows = strict_jsonl_loads(raw, relative)
    except JsonContractError as error:
        raise DeclarativeContractError(str(error)) from error
    for row in rows:
        if not isinstance(row, dict):
            raise DeclarativeContractError(f"{relative}: every JSONL row must be a JSON object")
    return rows


def _string_list(case: dict, key: str) -> list[str]:
    value = case.get(key)
    if not isinstance(value, list) or not value or not all(
        isinstance(item, str) and item for item in value
    ):
        raise DeclarativeContractError(
            f"case {case.get('id')!r}: {key!r} must be a nonempty list of nonempty strings"
        )
    return value


def _target_list(case: dict) -> list[str]:
    has_target = "target" in case
    has_targets = "targets" in case
    if has_target == has_targets:
        raise DeclarativeContractError(
            f"case {case.get('id')!r}: exactly one of 'target' or 'targets' is required"
        )
    if has_target:
        return [_canonical_relative(case["target"], "target")]
    targets = case["targets"]
    if not isinstance(targets, list) or not targets:
        raise DeclarativeContractError(f"case {case.get('id')!r}: 'targets' must be a nonempty list")
    return [_canonical_relative(item, "targets[]") for item in targets]


def _run_must_contain(case: dict, *, negate: bool) -> list[str]:
    targets = _target_list(case)
    strings = _string_list(case, "strings")
    failures: list[str] = []
    for target in targets:
        text = _read_text(target)
        for needle in strings:
            present = needle in text
            if negate and present:
                failures.append(f"{target}: unexpectedly contains {needle!r}")
            elif not negate and not present:
                failures.append(f"{target}: missing {needle!r}")
    return failures


def _run_jsonl_key_set_equality(case: dict) -> list[str]:
    target = _canonical_relative(case.get("target"), "target")
    field = case.get("field")
    unique_field = case.get("unique_field")
    values = case.get("values")
    if not isinstance(field, str) or not field:
        raise DeclarativeContractError(f"case {case.get('id')!r}: 'field' must be a nonempty string")
    if not isinstance(unique_field, str) or not unique_field:
        raise DeclarativeContractError(
            f"case {case.get('id')!r}: 'unique_field' must be a nonempty string"
        )
    if not isinstance(values, list) or not values:
        raise DeclarativeContractError(f"case {case.get('id')!r}: 'values' must be a nonempty list")

    rows = _read_jsonl(target)
    failures: list[str] = []
    expected = set(values)
    try:
        observed = {row[field] for row in rows}
    except KeyError as error:
        raise DeclarativeContractError(f"{target}: row is missing field {error}") from error
    if observed != expected:
        missing = expected - observed
        extra = observed - expected
        failures.append(
            f"{target}: field {field!r} set mismatch (missing={sorted(missing)}, extra={sorted(extra)})"
        )
    try:
        unique_values = [row[unique_field] for row in rows]
    except KeyError as error:
        raise DeclarativeContractError(f"{target}: row is missing field {error}") from error
    if len(unique_values) != len(set(unique_values)):
        seen: set = set()
        duplicates = sorted({value for value in unique_values if value in seen or seen.add(value)})
        failures.append(f"{target}: field {unique_field!r} has duplicate values: {duplicates}")
    return failures


def _run_registry_ledger_binding(case: dict) -> list[str]:
    registry_relative = _canonical_relative(case.get("registry"), "registry")
    ledger_relative = _canonical_relative(case.get("ledger"), "ledger")
    id_field = case.get("id_field")
    kinds = case.get("kinds")
    schema = case.get("schema")
    if not isinstance(id_field, str) or not id_field:
        raise DeclarativeContractError(f"case {case.get('id')!r}: 'id_field' must be a nonempty string")
    if not isinstance(kinds, list) or not kinds or not all(
        isinstance(item, str) and item for item in kinds
    ):
        raise DeclarativeContractError(
            f"case {case.get('id')!r}: 'kinds' must be a nonempty list of nonempty strings"
        )
    if not isinstance(schema, str) or not schema:
        raise DeclarativeContractError(f"case {case.get('id')!r}: 'schema' must be a nonempty string")

    records = _read_jsonl(registry_relative)
    ledger_rows = _read_jsonl(ledger_relative)

    failures: list[str] = []
    ids = {record.get(id_field) for record in records}
    ledger: dict[tuple[Any, Any], dict] = {}
    for row in ledger_rows:
        if row.get(id_field) in ids:
            key = (row.get(id_field), row.get("kind"))
            ledger[key] = row

    expected_count = len(kinds) * len(ids)
    if len(ledger) != expected_count:
        failures.append(
            f"{ledger_relative}: expected {expected_count} matching rows "
            f"({len(ids)} ids x {len(kinds)} kinds), found {len(ledger)}"
        )

    for record in records:
        record_id = record.get(id_field)
        if record.get("schema") != schema:
            failures.append(
                f"{registry_relative}: {record_id!r} schema {record.get('schema')!r} != {schema!r}"
            )
        provenance = record.get("provenance")
        if not isinstance(provenance, dict):
            failures.append(f"{registry_relative}: {record_id!r} is missing a 'provenance' object")
            provenance = {}
        for kind in kinds:
            key = (record_id, kind)
            row = ledger.get(key)
            if row is None:
                failures.append(
                    f"{ledger_relative}: no row for {id_field}={record_id!r} kind={kind!r}"
                )
                continue
            if row.get("http_status") != 200:
                failures.append(
                    f"{ledger_relative}: {record_id!r}/{kind} http_status={row.get('http_status')!r} != 200"
                )
            if row.get("error") is not None:
                failures.append(
                    f"{ledger_relative}: {record_id!r}/{kind} error={row.get('error')!r} is not null"
                )
            if not row.get("stored_at"):
                failures.append(f"{ledger_relative}: {record_id!r}/{kind} stored_at is empty")
            expected_sha256 = provenance.get(f"{kind}_sha256")
            if row.get("sha256") != expected_sha256:
                failures.append(
                    f"{ledger_relative}: {record_id!r}/{kind} sha256={row.get('sha256')!r} != "
                    f"provenance.{kind}_sha256={expected_sha256!r}"
                )
    return failures


_CASE_RUNNERS = {
    "must_contain": lambda case: _run_must_contain(case, negate=False),
    "must_not_contain": lambda case: _run_must_contain(case, negate=True),
    "jsonl_key_set_equality": _run_jsonl_key_set_equality,
    "registry_ledger_binding": _run_registry_ledger_binding,
}


def _validate_case_shape(case: Any) -> dict:
    if not isinstance(case, dict):
        raise DeclarativeContractError("every case must be a JSON object")
    case_id = case.get("id")
    if not isinstance(case_id, str) or not case_id:
        raise DeclarativeContractError("every case needs a nonempty string 'id'")
    case_type = case.get("type")
    if case_type not in KNOWN_CASE_TYPES:
        raise DeclarativeContractError(
            f"case {case_id!r}: unknown 'type' {case_type!r}, expected one of {KNOWN_CASE_TYPES}"
        )
    return case


def load_contract(contract_id: str) -> dict:
    """Read and strictly parse one contract document; never mutates state."""

    if not contract_id or "/" in contract_id or "\\" in contract_id:
        raise DeclarativeContractError(f"invalid contract id: {contract_id!r}")
    path = CONTRACTS_DIR / f"{contract_id}.json"
    try:
        raw = path.read_bytes()
    except OSError as error:
        raise DeclarativeContractError(f"cannot read contract {contract_id!r}: {error}") from error
    try:
        document = strict_json_loads(raw, str(path))
    except JsonContractError as error:
        raise DeclarativeContractError(str(error)) from error
    if not isinstance(document, dict):
        raise DeclarativeContractError(f"contract {contract_id!r}: document must be a JSON object")
    if document.get("schema") != "sf-declarative-contract-v1":
        raise DeclarativeContractError(
            f"contract {contract_id!r}: schema must be 'sf-declarative-contract-v1', "
            f"found {document.get('schema')!r}"
        )
    cases = document.get("cases")
    if not isinstance(cases, list) or not cases:
        raise DeclarativeContractError(f"contract {contract_id!r}: 'cases' must be a nonempty list")
    seen_ids: set[str] = set()
    for case in cases:
        validated = _validate_case_shape(case)
        if validated["id"] in seen_ids:
            raise DeclarativeContractError(f"contract {contract_id!r}: duplicate case id {validated['id']!r}")
        seen_ids.add(validated["id"])
    return document


def run_contract(contract_id: str) -> bool:
    """Run one contract's cases in order; print PASS/FAIL lines; return overall success."""

    try:
        document = load_contract(contract_id)
    except DeclarativeContractError as error:
        print(f"[FAIL] {contract_id}: {error}")
        return False

    all_passed = True
    for case in document["cases"]:
        case_id = case["id"]
        runner = _CASE_RUNNERS[case["type"]]
        label = f"{contract_id}::{case_id}"
        try:
            failures = runner(case)
        except DeclarativeContractError as error:
            print(f"[FAIL] {label}: {error}")
            all_passed = False
            continue
        if failures:
            print(f"[FAIL] {label}")
            for failure in failures:
                print(f"       - {failure}")
            all_passed = False
        else:
            print(f"[PASS] {label}")
    return all_passed


def discover_contract_ids() -> list[str]:
    try:
        paths = sorted(CONTRACTS_DIR.glob("*.json"))
    except OSError as error:
        raise DeclarativeContractError(f"cannot list {CONTRACTS_DIR}: {error}") from error
    return [path.stem for path in paths]


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--check-all", action="store_true", help="run every contract under docs/contracts/"
    )
    group.add_argument("--check", metavar="CONTRACT_ID", help="run exactly one contract by id")
    return parser


def main(argv: list[str] | None = None) -> int:
    arguments = _parser().parse_args(argv)
    try:
        contract_ids = discover_contract_ids() if arguments.check_all else [arguments.check]
    except DeclarativeContractError as error:
        print(f"[FAIL] {error}")
        return 1
    if not contract_ids:
        print(f"[FAIL] no contracts found under {CONTRACTS_DIR}")
        return 1

    overall = True
    for contract_id in contract_ids:
        overall &= run_contract(contract_id)
    verdict = "PASS" if overall else "FAIL"
    print(f"declarative contract: {verdict}")
    return 0 if overall else 1


if __name__ == "__main__":
    sys.exit(main())
