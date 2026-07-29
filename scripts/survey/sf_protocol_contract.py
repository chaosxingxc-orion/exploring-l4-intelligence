#!/usr/bin/env python3
"""Structured, offline contract oracle for the effective survey protocol.

The query compiler intentionally treats most byte-preserved §4 prose as cold
history.  This oracle therefore validates exact normalized clauses only in the
effective sections outside §4.  It is stdlib-only, performs no network access,
and never writes repository files.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

from sf_json_contract import JsonContractError, loads as _strict_json_loads


REPO_ROOT = Path(__file__).resolve().parents[2]
CURRENT_PROTOCOL = REPO_ROOT / "wiki" / "survey" / "current" / "protocol.md"
CONTRACTS_DATA_PATH = REPO_ROOT / "docs" / "integrity" / "protocol-contracts.json"
CONTRACTS_DATA_SCHEMA = "protocol-contracts-v1"


@dataclass(frozen=True)
class Contract:
    name: str
    section: str
    clause: str


@dataclass(frozen=True)
class OrderedContract:
    name: str
    section: str
    clauses: tuple[str, ...]


def normalize_clause(text: str) -> str:
    """Remove presentation-only Markdown and normalize wrapping and case."""
    return " ".join(text.casefold().replace("*", "").replace("`", "").split())


class ContractDataError(ValueError):
    """Raised when the externalized contract table is missing or malformed."""


def _require_nonempty_str(value: object, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise ContractDataError(f"{label} must be a non-empty string")
    return value


def load_contracts_data(
    path: Path = CONTRACTS_DATA_PATH,
) -> tuple[tuple[Contract, ...], tuple[OrderedContract, ...]]:
    """Strict-load the externalized contract/ordered-contract tables.

    Fails closed: any missing file, invalid strict-JSON bytes, schema
    mismatch, or wrong-shaped row raises ``ContractDataError`` rather than
    silently returning a partial or empty table.
    """
    try:
        raw = path.read_bytes()
    except OSError as error:
        raise ContractDataError(f"cannot read {path}: {error}") from error
    try:
        document = _strict_json_loads(raw, str(path))
    except JsonContractError as error:
        raise ContractDataError(f"{path}: {error}") from error
    if not isinstance(document, dict) or set(document) != {
        "schema",
        "contracts",
        "ordered_contracts",
    }:
        raise ContractDataError(f"{path}: unexpected top-level schema")
    if document["schema"] != CONTRACTS_DATA_SCHEMA:
        raise ContractDataError(
            f"{path}: expected schema {CONTRACTS_DATA_SCHEMA!r}, found {document['schema']!r}"
        )

    contracts_raw = document["contracts"]
    if not isinstance(contracts_raw, list) or not contracts_raw:
        raise ContractDataError(f"{path}: contracts must be a non-empty list")
    contracts: list[Contract] = []
    for index, item in enumerate(contracts_raw):
        label = f"{path}: contracts[{index}]"
        if not isinstance(item, dict) or set(item) != {"name", "section", "clause"}:
            raise ContractDataError(f"{label} must have exact name/section/clause fields")
        contracts.append(
            Contract(
                _require_nonempty_str(item["name"], f"{label}.name"),
                _require_nonempty_str(item["section"], f"{label}.section"),
                _require_nonempty_str(item["clause"], f"{label}.clause"),
            )
        )

    ordered_raw = document["ordered_contracts"]
    if not isinstance(ordered_raw, list) or not ordered_raw:
        raise ContractDataError(f"{path}: ordered_contracts must be a non-empty list")
    ordered_contracts: list[OrderedContract] = []
    for index, item in enumerate(ordered_raw):
        label = f"{path}: ordered_contracts[{index}]"
        if not isinstance(item, dict) or set(item) != {"name", "section", "clauses"}:
            raise ContractDataError(f"{label} must have exact name/section/clauses fields")
        clauses_raw = item["clauses"]
        if not isinstance(clauses_raw, list) or not clauses_raw:
            raise ContractDataError(f"{label}.clauses must be a non-empty list")
        clauses = tuple(
            _require_nonempty_str(clause, f"{label}.clauses[{clause_index}]")
            for clause_index, clause in enumerate(clauses_raw)
        )
        ordered_contracts.append(
            OrderedContract(
                _require_nonempty_str(item["name"], f"{label}.name"),
                _require_nonempty_str(item["section"], f"{label}.section"),
                clauses,
            )
        )

    return tuple(contracts), tuple(ordered_contracts)


CONTRACTS, ORDERED_CONTRACTS = load_contracts_data()


def _extract_numbered_sections(text: str) -> tuple[dict[str, str], list[str]]:
    # A numbered section ends at *any* following H2, including §4bis and
    # Appendix headings.  Otherwise §10 could incorrectly borrow a required
    # clause moved into a cold appendix at EOF.
    headings = list(
        re.finditer(r"^##(?:[ \t]+[^\r\n]*)?$", text, flags=re.MULTILINE)
    )
    sections: dict[str, str] = {}
    errors: list[str] = []
    for index, heading in enumerate(headings):
        numbered = re.fullmatch(
            r"##[ \t]+(§(?:10|[0-9]))(?:[ \t]+[^\r\n]*)?",
            heading.group(0),
        )
        if numbered is None:
            continue
        section_id = numbered.group(1)
        end = headings[index + 1].start() if index + 1 < len(headings) else len(text)
        if section_id in sections:
            errors.append(f"duplicate-section:{section_id}")
            continue
        sections[section_id] = text[heading.start():end]
    expected = {f"§{number}" for number in range(11)}
    for section_id in sorted(expected - sections.keys()):
        errors.append(f"missing-section:{section_id}")
    return sections, errors


def validate_protocol_contracts(text: str) -> list[str]:
    """Return stable failure codes; an empty list means all contracts hold."""
    sections, errors = _extract_numbered_sections(text)
    normalized = {
        section_id: normalize_clause(section_text)
        for section_id, section_text in sections.items()
        if section_id != "§4"
    }
    for contract in CONTRACTS:
        haystack = normalized.get(contract.section, "")
        needle = normalize_clause(contract.clause)
        # Exact lexical boundaries matter: the contract "<= 3" must not be
        # satisfied by "<= 30", nor may a longer identifier satisfy a frozen
        # enum member.  Punctuation inside the clause remains literal.
        pattern = rf"(?<![\w]){re.escape(needle)}(?![\w])"
        if not re.search(pattern, haystack):
            errors.append(f"missing-contract:{contract.name}:{contract.section}")
    for contract in ORDERED_CONTRACTS:
        haystack = normalized.get(contract.section, "")
        cursor = 0
        ordered = True
        for clause in contract.clauses:
            needle = normalize_clause(clause)
            pattern = rf"(?<![\w]){re.escape(needle)}(?![\w])"
            match = re.search(pattern, haystack[cursor:])
            if match is None:
                ordered = False
                break
            cursor += match.end()
        if not ordered:
            errors.append(f"ordered-contract:{contract.name}:{contract.section}")
        if contract.name == "stage1b-execution-sequence":
            observed_indices = [
                int(match.group(1))
                for match in re.finditer(
                    r"^(\d+)\.[ \t]",
                    sections.get(contract.section, ""),
                    flags=re.MULTILINE,
                )
            ]
            failure = f"ordered-contract:{contract.name}:{contract.section}"
            if observed_indices != list(range(1, 10)) and failure not in errors:
                errors.append(failure)
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--protocol", type=Path, default=CURRENT_PROTOCOL)
    parser.add_argument("--check", action="store_true", help="validate without writing")
    args = parser.parse_args(argv)
    try:
        text = args.protocol.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        print(f"[sf_protocol_contract] READ FAIL: {args.protocol}: {exc}", file=sys.stderr)
        return 1
    failures = validate_protocol_contracts(text)
    if failures:
        for failure in failures:
            print(f"[sf_protocol_contract] FAIL: {failure}", file=sys.stderr)
        return 1
    print(
        f"[sf_protocol_contract] PASS ({len(CONTRACTS)} exact normalized + "
        f"{len(ORDERED_CONTRACTS)} ordered contracts)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
