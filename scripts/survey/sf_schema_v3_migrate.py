#!/usr/bin/env python3
"""Deterministically migrate pinned system-first sidecars to schema v3."""

from __future__ import annotations

import argparse
import copy
import json
import re
import sys
from collections import Counter
from pathlib import Path

from sf_evidence_contract import (
    EDGE_REQUIRED_FIELDS,
    ROW_REQUIRED_FIELDS,
    SIGNAL_REQUIRED_FIELDS,
    validate_bound_values,
)


ANCHOR_REPLACEMENTS = {
    "p4 probe": "p4 anchor='create extend probe and prune branches'",
    "p5 cost": "p5 anchor='accuracy cost trade off'",
    "p3 Algorithm": "p3 anchor='every decision auditable'",
    "p8 Fig": "p8 anchor='natural stop time aligns with correct majority emergence'",
    "p14 delegated": "p14 anchor='asymmetric delegated architecture'",
    "p4 explore": "p4 anchor='decides every explore and stop action'",
}
POSITIVE_SELECTION_EVIDENCE = {
    "2026.findings-acl.1724#pipeline": "selection_policy",
    "2026.findings-acl.511#prm-guided-search": "selection_policy",
    "2602.16485#calibrated-orchestration": "candidate_pool_exists",
    "2604.16529#rtv": "selection_policy",
    "2604.16529#rtv-pdr-pipeline": "selection_policy",
    "2605.08083#discovered-controller": "selection_policy",
    "2606.01667#agentic-orchestration": "selection_policy",
}
NO_EXPLICIT_SELECTION = {
    "2026.findings-acl.1243#closed-prompt-only",
    "2026.findings-acl.1243#open-sft-variant",
    "2604.16529#pdr-random-k",
    "2606.03054#trained-gate",
}

SCHEMA_TEXT = (
    "v3 (taxonomy v6: row16 + signal4 + edge2 field-bound evidence; "
    "strong PDF anchors)"
)
SCHEMA_V3_BINDING_STATUS = "PENDING_INDEPENDENT_ADJUDICATION"
ABSENCE_SELECTION_NOTE = (
    "No explicit scored/tournament candidate selection is encoded for this method "
    "path; candidate-pool existence alone is not explicit selection."
)
ABSENCE_SELECTION_SCOPE = "complete pinned method path"
EXPECTED_SIDECARS = 8
EXPECTED_ROWS = 11
EXPECTED_SIGNALS = 12
SUCCESS_LINE = (
    "schema-v3 migration: PASS (8 sidecars, 11 rows, 12 signals; "
    "pending adjudication)"
)

REPO_ROOT = Path(__file__).resolve().parents[2]
SOURCE_DIR = REPO_ROOT / "wiki" / "survey" / "sidecars"
OUTPUT_DIR = (
    REPO_ROOT / "wiki" / "survey" / "current" / "data" / "schema-v3" / "sidecars"
)
EDGE_QUOTE_RE = re.compile(r"\b(?P<kind>canon|tex):\s*'(?P<quote>[^']+)'", re.DOTALL)


class MigrationError(ValueError):
    """Raised when the pinned corpus cannot be migrated without ambiguity."""


def replace_anchors(value, counts):
    """Return a deep replacement of all anchor shorthands and record occurrences."""
    if isinstance(value, str):
        migrated = value
        for source, replacement in ANCHOR_REPLACEMENTS.items():
            occurrence_count = migrated.count(source)
            if occurrence_count:
                counts[source] = counts.get(source, 0) + occurrence_count
                migrated = migrated.replace(source, replacement)
        return migrated
    if isinstance(value, dict):
        return {key: replace_anchors(item, counts) for key, item in value.items()}
    if isinstance(value, list):
        return [replace_anchors(item, counts) for item in value]
    return copy.deepcopy(value)


def _require_mapping(value, owner):
    if not isinstance(value, dict):
        raise MigrationError(f"{owner}: expected JSON object")
    return value


def _migrate_row_evidence(row):
    pid = row.get("method_path_id", "?")
    evidence = _require_mapping(row.get("claim_evidence"), f"{pid}:claim_evidence")
    legacy_fields = ROW_REQUIRED_FIELDS[:-2]
    if set(evidence) != set(legacy_fields):
        missing = sorted(set(legacy_fields) - set(evidence))
        extra = sorted(set(evidence) - set(legacy_fields))
        raise MigrationError(
            f"{pid}: legacy row evidence is not exact row14 "
            f"(missing={missing}, extra={extra})"
        )

    if pid in POSITIVE_SELECTION_EVIDENCE:
        clone_field = POSITIVE_SELECTION_EVIDENCE[pid]
        if clone_field not in evidence:
            raise MigrationError(
                f"{pid}: positive selection clone source {clone_field!r} is missing"
            )
        selection_object = copy.deepcopy(evidence[clone_field])
        explicit_selection = copy.deepcopy(evidence[clone_field])
        selection_object["value"] = copy.deepcopy(row.get("selection_object"))
        explicit_selection["value"] = copy.deepcopy(
            row.get("explicit_candidate_pool_selection")
        )
    elif pid in NO_EXPLICIT_SELECTION:
        selection_object = {
            "value": copy.deepcopy(row.get("selection_object")),
            "kind": "absence",
            "scope": ABSENCE_SELECTION_SCOPE,
            "note": ABSENCE_SELECTION_NOTE,
        }
        explicit_selection = {
            "value": copy.deepcopy(row.get("explicit_candidate_pool_selection")),
            "kind": "absence",
            "scope": ABSENCE_SELECTION_SCOPE,
            "note": ABSENCE_SELECTION_NOTE,
        }
    else:
        raise MigrationError(f"{pid}: method path is absent from selection policy maps")

    row["claim_evidence"] = {
        **{field: copy.deepcopy(evidence[field]) for field in legacy_fields},
        "selection_object": selection_object,
        "explicit_candidate_pool_selection": explicit_selection,
    }


def _migrate_signal_evidence(row):
    pid = row.get("method_path_id", "?")
    signals = row.get("signals")
    if not isinstance(signals, list):
        raise MigrationError(f"{pid}: signals must be a JSON array")
    for index, signal in enumerate(signals):
        signal = _require_mapping(signal, f"{pid}:signal:{index}")
        sid = signal.get("signal_id", index)
        evidence = _require_mapping(
            signal.get("claim_evidence"), f"{pid}:signal:{sid}:claim_evidence"
        )
        legacy_fields = ("form", "lifecycle", "uses")
        if set(evidence) != set(legacy_fields):
            missing = sorted(set(legacy_fields) - set(evidence))
            extra = sorted(set(evidence) - set(legacy_fields))
            raise MigrationError(
                f"{pid}:signal:{sid}: legacy evidence is not exact signal3 "
                f"(missing={missing}, extra={extra})"
            )
        source = copy.deepcopy(evidence["form"])
        source["value"] = copy.deepcopy(signal.get("source"))
        signal["claim_evidence"] = {
            "form": copy.deepcopy(evidence["form"]),
            "source": source,
            "lifecycle": copy.deepcopy(evidence["lifecycle"]),
            "uses": copy.deepcopy(evidence["uses"]),
        }


def _extract_edge_quote(locator, pid, index):
    if not isinstance(locator, str):
        raise MigrationError(
            f"{pid}:edge:{index}: cannot extract canon/tex quoted evidence from "
            "non-string source_locator"
        )
    match = EDGE_QUOTE_RE.search(locator)
    if match is None:
        raise MigrationError(
            f"{pid}:edge:{index}: cannot extract an existing canon or tex quote "
            "from source_locator"
        )
    return match.group("kind"), match.group("quote")


def _migrate_edge_evidence(row):
    pid = row.get("method_path_id", "?")
    edges = row.get("control_edges")
    if not isinstance(edges, list):
        raise MigrationError(f"{pid}: control_edges must be a JSON array")
    for index, edge in enumerate(edges):
        edge = _require_mapping(edge, f"{pid}:edge:{index}")
        kind, quote = _extract_edge_quote(edge.get("source_locator"), pid, index)
        edge["claim_evidence"] = {
            field: {
                "value": copy.deepcopy(edge.get(field)),
                "kind": kind,
                "quote": quote,
            }
            for field in EDGE_REQUIRED_FIELDS
        }


def migrate_sidecar(source, anchor_counts=None):
    """Return one independently migrated sidecar without mutating *source*."""
    source = _require_mapping(source, "sidecar")
    counts = anchor_counts if anchor_counts is not None else Counter()
    migrated = replace_anchors(source, counts)
    migrated["schema"] = SCHEMA_TEXT
    migrated["schema_v3_binding_status"] = SCHEMA_V3_BINDING_STATUS
    migrated.pop("schema_v3_adjudicator", None)

    rows = migrated.get("method_paths")
    if not isinstance(rows, list):
        raise MigrationError("sidecar: method_paths must be a JSON array")
    for index, row in enumerate(rows):
        row = _require_mapping(row, f"method_paths:{index}")
        _migrate_row_evidence(row)
        _migrate_signal_evidence(row)
        _migrate_edge_evidence(row)
        failures = validate_bound_values(row)
        if failures:
            raise MigrationError(
                f"{row.get('method_path_id', '?')}: bound-value validation failed: "
                + "; ".join(failures)
            )
    return migrated


def _count_text_occurrences(sidecars, needle):
    return sum(
        json.dumps(sidecar, ensure_ascii=False).count(needle) for sidecar in sidecars
    )


def _validate_policy_maps(method_ids):
    positive = set(POSITIVE_SELECTION_EVIDENCE)
    absent = set(NO_EXPLICIT_SELECTION)
    overlap = sorted(positive & absent)
    unknown = sorted((positive | absent) - method_ids)
    missing = sorted(method_ids - (positive | absent))
    if overlap or unknown or missing or len(positive | absent) != EXPECTED_ROWS:
        raise MigrationError(
            "selection policy maps must cover exactly 11 method paths with no overlap "
            f"(overlap={overlap}, unknown={unknown}, missing={missing})"
        )


def build_outputs(source_dir=SOURCE_DIR):
    """Read, migrate, and fully validate all pinned inputs in memory."""
    paths = sorted(source_dir.glob("*.sidecar.json"), key=lambda path: path.name)
    if len(paths) != EXPECTED_SIDECARS:
        raise MigrationError(
            f"expected exactly {EXPECTED_SIDECARS} input sidecars in {source_dir}, "
            f"found {len(paths)}"
        )

    sources = []
    for path in paths:
        try:
            sources.append(json.loads(path.read_text(encoding="utf-8")))
        except (OSError, json.JSONDecodeError) as error:
            raise MigrationError(f"cannot read {path}: {error}") from error

    anchor_counts = Counter()
    outputs = [migrate_sidecar(source, anchor_counts) for source in sources]
    rows = [row for sidecar in outputs for row in sidecar.get("method_paths", [])]
    signals = [signal for row in rows for signal in row.get("signals", [])]
    if len(outputs) != EXPECTED_SIDECARS:
        raise MigrationError(f"output sidecar count mismatch: {len(outputs)}")
    if len(rows) != EXPECTED_ROWS:
        raise MigrationError(f"expected {EXPECTED_ROWS} method paths, found {len(rows)}")
    if len(signals) != EXPECTED_SIGNALS:
        raise MigrationError(f"expected {EXPECTED_SIGNALS} signals, found {len(signals)}")

    method_ids = [row.get("method_path_id") for row in rows]
    if len(set(method_ids)) != len(method_ids):
        duplicates = sorted(
            method_id
            for method_id, count in Counter(method_ids).items()
            if count > 1
        )
        raise MigrationError(f"duplicate method_path_id values: {duplicates}")
    _validate_policy_maps(set(method_ids))

    for source, replacement in ANCHOR_REPLACEMENTS.items():
        before = anchor_counts[source]
        if before < 1:
            raise MigrationError(
                f"anchor replacement source {source!r} does not occur in pinned inputs"
            )
        legacy_after = _count_text_occurrences(outputs, source)
        replacement_after = _count_text_occurrences(outputs, replacement)
        if legacy_after != 0 or replacement_after != before:
            raise MigrationError(
                f"anchor replacement {source!r} -> {replacement!r} did not conserve "
                f"occurrences (before={before}, legacy_after={legacy_after}, "
                f"replacement_after={replacement_after})"
            )

    return list(zip(paths, outputs, strict=True))


def write_outputs(outputs, output_dir=OUTPUT_DIR):
    """Write validated outputs as deterministic UTF-8 LF JSON; remove nothing."""
    output_dir.mkdir(parents=True, exist_ok=True)
    for source_path, sidecar in outputs:
        rendered = json.dumps(sidecar, ensure_ascii=False, indent=1) + "\n"
        (output_dir / source_path.name).write_bytes(rendered.encode("utf-8"))


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="validate without writing")
    mode.add_argument("--write", action="store_true", help="validate and write outputs")
    return parser.parse_args(argv)


def main(argv=None, source_dir=SOURCE_DIR, output_dir=OUTPUT_DIR):
    args = parse_args(argv)
    try:
        outputs = build_outputs(source_dir)
        if args.write:
            write_outputs(outputs, output_dir)
    except (MigrationError, OSError) as error:
        print(f"schema-v3 migration: ERROR: {error}", file=sys.stderr)
        return 1
    print(SUCCESS_LINE)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
