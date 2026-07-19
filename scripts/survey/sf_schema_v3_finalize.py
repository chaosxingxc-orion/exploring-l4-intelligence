#!/usr/bin/env python3
"""Validate independent schema-v3 adjudication and finalize active sidecars."""

from __future__ import annotations

import argparse
import copy
import sys
import warnings
from collections.abc import Mapping
from pathlib import Path

import sf_schema_v3_migrate as migration

with warnings.catch_warnings():
    warnings.simplefilter("ignore", ResourceWarning)
    from sf_identity_taxonomy_v5_test import row_hash


ARTIFACT_ID = "SF-SCHEMA-V3-ADJUDICATION-2026-07-19-01"
ARTIFACT_SCHEMA = "schema-v3-binding-delta-adjudication-v1"
ADJUDICATOR = "/root/a6_adjudicator"
SOURCE_HEAD = "418c738a721c69bcd827f8dadee8526e6dfbff87"
FINAL_STATUS = "ADJUDICATED_AGREE"
EXPECTED_BINDINGS = 70
EXPECTED_ANCHOR_RULES = 6
EXPECTED_ANCHOR_OCCURRENCES = 8
EXPECTED_RESOLUTIONS = 13
SUCCESS_LINE = (
    "schema-v3 finalization: PASS (8 sidecars, 11 rows, 70 bindings; "
    "adjudicator=/root/a6_adjudicator)"
)

REPO_ROOT = Path(__file__).resolve().parents[2]
ADJUDICATION_PATH = (
    REPO_ROOT / "wiki" / "survey" / "current" / "data" /
    "schema-v3-adjudication.json"
)
OUTPUT_DIR = migration.OUTPUT_DIR
EXPECTED_DESTINATION_NAMES = frozenset(
    {
        "2026.findings-acl.1243.sidecar.json",
        "2026.findings-acl.1724.sidecar.json",
        "2026.findings-acl.511.sidecar.json",
        "2602.16485.sidecar.json",
        "2604.16529.sidecar.json",
        "2605.08083.sidecar.json",
        "2606.01667.sidecar.json",
        "2606.03054.sidecar.json",
    }
)

_TOP_LEVEL_KEYS = {
    "artifact_id",
    "schema",
    "reviewer_id",
    "reviewer_role",
    "source_head",
    "initial_review",
    "scope",
    "binding_verdicts",
    "anchor_verdicts",
    "resolution_log",
    "summary",
}
_BINDING_KEYS = {
    "method_path_id",
    "owner",
    "field",
    "encoded_value",
    "evidence_kind",
    "verdict",
    "reason",
    "source_pointer",
}
_ANCHOR_KEYS = {
    "old_locator",
    "new_locator",
    "occurrences",
    "verdict",
    "reason",
    "source_pointer",
}
_INITIAL_REVIEW = {
    "source_head": "ca00b0dd5a050be61f96423326366a5cf1053030",
    "artifact_sha256": (
        "ed03597a9b92baf15116d3e0471854e9eeb3f5969b10f39cc263397eced352a8"
    ),
    "binding_counts": {"agree": 59, "disagree": 11},
    "anchor_counts": {"agree": 5, "disagree": 1},
    "status": "DISAGREEMENTS_FOUND",
}
_SCOPE = {
    "method_paths": 11,
    "signals": 12,
    "edges": 18,
    "binding_verdicts": 70,
    "anchor_rules": 6,
    "anchor_occurrences": 8,
}
_SUMMARY = {
    "agree": 70,
    "disagree": 0,
    "anchor_agree": 6,
    "anchor_disagree": 0,
    "status": "ALL_AGREE",
}
_RESOLUTION_IDS = frozenset(
    [*(f"binding-{index:02d}" for index in range(1, 12)), "anchor-01", "coupled-01"]
)


class FinalizationError(ValueError):
    """Raised when adjudication or finalized destinations fail closed."""


def _require_mapping(value, owner):
    if not isinstance(value, Mapping):
        raise FinalizationError(f"{owner}: expected JSON object")
    return value


def _require_exact_keys(value, expected, owner):
    mapping = _require_mapping(value, owner)
    actual = set(mapping)
    if actual != set(expected):
        raise FinalizationError(
            f"{owner}: keys mismatch (missing={sorted(set(expected) - actual)}, "
            f"extra={sorted(actual - set(expected))})"
        )
    return mapping


def _require_nonempty_string(value, owner):
    if not isinstance(value, str) or not value.strip():
        raise FinalizationError(f"{owner}: must be a non-empty string")
    return value


def _values_identical(left, right):
    if type(left) is not type(right):
        return False
    if isinstance(left, Mapping):
        return set(left) == set(right) and all(
            _values_identical(left[key], right[key]) for key in left
        )
    if isinstance(left, list):
        return len(left) == len(right) and all(
            _values_identical(left_item, right_item)
            for left_item, right_item in zip(left, right, strict=True)
        )
    return left == right


def _binding_owner(row, owner):
    if owner == "row":
        return row
    owner_kind, separator, owner_id = owner.partition(":")
    if not separator or not owner_id:
        raise FinalizationError(f"malformed generated binding owner {owner!r}")
    if owner_kind == "signal":
        matches = [
            signal
            for signal in row["signals"]
            if signal.get("signal_id") == owner_id
        ]
        if len(matches) == 1:
            return matches[0]
    elif owner_kind == "edge" and owner_id.isdigit():
        index = int(owner_id)
        if 0 <= index < len(row["control_edges"]):
            return row["control_edges"][index]
    raise FinalizationError(f"generated binding owner does not exist: {owner!r}")


def _expected_binding_rows(outputs):
    expected = {}
    owner_counts = {"row": 0, "signal": 0, "edge": 0}
    for _, sidecar in outputs:
        for row in sidecar["method_paths"]:
            pid = row["method_path_id"]
            keys = [
                ("row", "selection_object"),
                ("row", "explicit_candidate_pool_selection"),
            ]
            keys.extend(
                (f"signal:{signal['signal_id']}", "source")
                for signal in row["signals"]
            )
            keys.extend(
                (f"edge:{index}", field)
                for index, _ in enumerate(row["control_edges"])
                for field in ("signal_use", "decision_right")
            )
            for owner, field in keys:
                target = _binding_owner(row, owner)
                evidence = target["claim_evidence"][field]
                key = (pid, owner, field)
                if key in expected:
                    raise FinalizationError(
                        f"duplicate generated binding tuple: {key!r}"
                    )
                expected[key] = (copy.deepcopy(target[field]), evidence["kind"])
                owner_counts[owner.partition(":")[0]] += 1
    if len(expected) != EXPECTED_BINDINGS or owner_counts != {
        "row": 22,
        "signal": 12,
        "edge": 36,
    }:
        raise FinalizationError(
            "fresh pending outputs do not expose exact binding scope "
            f"(count={len(expected)}, owners={owner_counts})"
        )
    return expected


def _validate_binding_verdicts(verdicts, expected):
    if not isinstance(verdicts, list) or len(verdicts) != EXPECTED_BINDINGS:
        found = len(verdicts) if isinstance(verdicts, list) else "non-list"
        raise FinalizationError(
            f"binding_verdicts: expected exactly 70 rows, found {found}"
        )
    seen = set()
    for index, raw in enumerate(verdicts):
        owner = f"binding_verdicts:{index}"
        row = _require_exact_keys(raw, _BINDING_KEYS, owner)
        key = tuple(row[field] for field in ("method_path_id", "owner", "field"))
        if any(not isinstance(part, str) or not part for part in key):
            raise FinalizationError(f"{owner}: malformed binding tuple")
        if key in seen:
            raise FinalizationError(f"{owner}: duplicate binding tuple {key!r}")
        seen.add(key)
        if key not in expected:
            raise FinalizationError(f"{owner}: unknown or extra binding tuple {key!r}")
        if row["verdict"] != "AGREE":
            raise FinalizationError(f"{owner}: verdict must be AGREE")
        _require_nonempty_string(row["reason"], f"{owner}:reason")
        _require_nonempty_string(row["source_pointer"], f"{owner}:source_pointer")
        expected_value, expected_kind = expected[key]
        if not _values_identical(row["encoded_value"], expected_value):
            raise FinalizationError(
                f"{owner}: encoded_value mismatch for {key!r}"
            )
        if row["evidence_kind"] != expected_kind:
            raise FinalizationError(
                f"{owner}: evidence_kind mismatch for {key!r}"
            )
    missing = sorted(set(expected) - seen)
    if missing:
        raise FinalizationError(f"binding_verdicts: missing tuples {missing}")


def _expected_anchor_rows(outputs):
    expected = {}
    for shorthand, replacement in migration.ANCHOR_REPLACEMENTS.items():
        old_locator = shorthand.split()[0]
        occurrences = migration._count_text_occurrences(
            [sidecar for _, sidecar in outputs], replacement
        )
        key = (old_locator, replacement)
        if key in expected:
            raise FinalizationError(f"duplicate generated anchor rule: {key!r}")
        expected[key] = occurrences
    if len(expected) != EXPECTED_ANCHOR_RULES or sum(expected.values()) != 8:
        raise FinalizationError(
            "fresh pending outputs do not expose exact anchor scope "
            f"(rules={len(expected)}, occurrences={sum(expected.values())})"
        )
    return expected


def _validate_anchor_verdicts(verdicts, expected):
    if not isinstance(verdicts, list) or len(verdicts) != EXPECTED_ANCHOR_RULES:
        found = len(verdicts) if isinstance(verdicts, list) else "non-list"
        raise FinalizationError(
            f"anchor_verdicts: expected exactly 6 rows, found {found}"
        )
    seen = set()
    total_occurrences = 0
    for index, raw in enumerate(verdicts):
        owner = f"anchor_verdicts:{index}"
        row = _require_exact_keys(raw, _ANCHOR_KEYS, owner)
        key = (row["old_locator"], row["new_locator"])
        if any(not isinstance(part, str) or not part for part in key):
            raise FinalizationError(f"{owner}: malformed anchor row")
        if key in seen:
            raise FinalizationError(f"{owner}: duplicate anchor row {key!r}")
        seen.add(key)
        if key not in expected:
            raise FinalizationError(f"{owner}: anchor mismatch or unknown row {key!r}")
        if row["verdict"] != "AGREE":
            raise FinalizationError(f"{owner}: verdict must be AGREE")
        _require_nonempty_string(row["reason"], f"{owner}:reason")
        _require_nonempty_string(row["source_pointer"], f"{owner}:source_pointer")
        if type(row["occurrences"]) is not int or row["occurrences"] != expected[key]:
            raise FinalizationError(f"{owner}: occurrences mismatch for {key!r}")
        total_occurrences += row["occurrences"]
    if set(expected) != seen:
        raise FinalizationError("anchor_verdicts: missing anchor rows")
    if total_occurrences != EXPECTED_ANCHOR_OCCURRENCES:
        raise FinalizationError(
            f"anchor_verdicts: expected 8 occurrences, found {total_occurrences}"
        )


def _validate_resolution_log(rows):
    if not isinstance(rows, list) or len(rows) != EXPECTED_RESOLUTIONS:
        found = len(rows) if isinstance(rows, list) else "non-list"
        raise FinalizationError(
            f"resolution_log: expected exactly 13 rows, found {found}"
        )
    seen = set()
    for index, raw in enumerate(rows):
        owner = f"resolution_log:{index}"
        row = _require_mapping(raw, owner)
        resolution_id = _require_nonempty_string(
            row.get("resolution_id"), f"{owner}:resolution_id"
        )
        if resolution_id in seen:
            raise FinalizationError(f"{owner}: duplicate resolution_id")
        seen.add(resolution_id)
        resolution_type = row.get("resolution_type")
        detail_key = {
            "original_binding_disagreement": "tuple",
            "original_anchor_disagreement": "locator",
            "coupled_semantic_review": "review_scope",
        }.get(resolution_type)
        if detail_key is None:
            raise FinalizationError(f"{owner}: unknown resolution_type")
        expected_keys = {
            "resolution_id",
            "resolution_type",
            detail_key,
            "remediation_commit",
            "original_issue",
            "actual_repair",
            "re_review_verdict",
            "re_review_reason",
        }
        _require_exact_keys(row, expected_keys, owner)
        if row["remediation_commit"] != SOURCE_HEAD:
            raise FinalizationError(f"{owner}: remediation_commit mismatch")
        if row["re_review_verdict"] != "AGREE":
            raise FinalizationError(f"{owner}: re_review_verdict must be AGREE")
        for field in ("original_issue", "actual_repair", "re_review_reason"):
            _require_nonempty_string(row[field], f"{owner}:{field}")
        detail = row[detail_key]
        if detail_key == "tuple":
            _require_exact_keys(
                detail, {"method_path_id", "owner", "field"}, f"{owner}:tuple"
            )
            for field in ("method_path_id", "owner", "field"):
                _require_nonempty_string(
                    detail[field], f"{owner}:tuple:{field}"
                )
        elif detail_key == "locator":
            _require_exact_keys(
                detail,
                {"old_locator", "rejected_locator", "repaired_locator", "occurrences"},
                f"{owner}:locator",
            )
            for field in ("old_locator", "rejected_locator", "repaired_locator"):
                _require_nonempty_string(
                    detail[field], f"{owner}:locator:{field}"
                )
            if type(detail["occurrences"]) is not int or detail["occurrences"] < 1:
                raise FinalizationError(
                    f"{owner}:locator:occurrences must be a positive integer"
                )
        else:
            if not isinstance(detail, list) or len(detail) != 2:
                raise FinalizationError(
                    f"{owner}: review_scope must contain exactly two rows"
                )
            for detail_index, item in enumerate(detail):
                _require_exact_keys(
                    item,
                    {"method_path_id", "owner", "field", "encoded_value"},
                    f"{owner}:review_scope:{detail_index}",
                )
                for field in ("method_path_id", "owner", "field"):
                    _require_nonempty_string(
                        item[field],
                        f"{owner}:review_scope:{detail_index}:{field}",
                    )
                if item["encoded_value"] in (None, "", [], {}):
                    raise FinalizationError(
                        f"{owner}:review_scope:{detail_index}:encoded_value "
                        "must be non-empty"
                    )
    if seen != _RESOLUTION_IDS:
        raise FinalizationError(
            "resolution_log: resolution ids mismatch "
            f"(missing={sorted(_RESOLUTION_IDS - seen)}, "
            f"extra={sorted(seen - _RESOLUTION_IDS)})"
        )


def _validate_adjudication(artifact, outputs):
    artifact = _require_exact_keys(artifact, _TOP_LEVEL_KEYS, "adjudication")
    exact_scalars = {
        "artifact_id": ARTIFACT_ID,
        "schema": ARTIFACT_SCHEMA,
        "reviewer_id": ADJUDICATOR,
        "reviewer_role": "fresh non-implementer",
        "source_head": SOURCE_HEAD,
    }
    for field, expected in exact_scalars.items():
        if artifact[field] != expected:
            raise FinalizationError(
                f"adjudication:{field}: expected {expected!r}, found {artifact[field]!r}"
            )
    _require_nonempty_string(artifact["reviewer_id"], "adjudication:reviewer_id")
    if not _values_identical(artifact["initial_review"], _INITIAL_REVIEW):
        raise FinalizationError("adjudication:initial_review mismatch or malformed")
    if not _values_identical(artifact["scope"], _SCOPE):
        raise FinalizationError("adjudication:scope mismatch or malformed")
    summary = _require_exact_keys(artifact["summary"], _SUMMARY, "summary")
    for field, expected in _SUMMARY.items():
        if not _values_identical(summary[field], expected):
            raise FinalizationError(
                f"summary:{field}: expected {expected!r}, found {summary[field]!r}"
            )
    _validate_binding_verdicts(
        artifact["binding_verdicts"], _expected_binding_rows(outputs)
    )
    _validate_anchor_verdicts(
        artifact["anchor_verdicts"], _expected_anchor_rows(outputs)
    )
    _validate_resolution_log(artifact["resolution_log"])


def load_adjudication(path=ADJUDICATION_PATH):
    """Strict-load the reviewer-owned adjudication artifact."""
    return migration._load_sidecar(Path(path))


def finalize_outputs(pending, artifact):
    """Validate *artifact* and stamp deep copies of fresh pending outputs."""
    _validate_adjudication(artifact, pending)
    finalized = copy.deepcopy(pending)
    for _, sidecar in finalized:
        sidecar["schema_v3_binding_status"] = FINAL_STATUS
        sidecar["schema_v3_binding_adjudicator"] = ADJUDICATOR
        for row in sidecar["method_paths"]:
            row["adjudication_row_sha256"] = row_hash(row)
    names = {path.name for path, _ in finalized}
    if names != EXPECTED_DESTINATION_NAMES:
        raise FinalizationError(
            "finalized destination names mismatch "
            f"(missing={sorted(EXPECTED_DESTINATION_NAMES - names)}, "
            f"extra={sorted(names - EXPECTED_DESTINATION_NAMES)})"
        )
    return finalized


def build_finalized_outputs(
    source_dir=migration.SOURCE_DIR,
    adjudication_path=ADJUDICATION_PATH,
):
    """Build fresh pending outputs, validate ALL_AGREE, and stamp deep copies."""
    pending = migration.build_outputs(source_dir)
    artifact = load_adjudication(adjudication_path)
    return finalize_outputs(pending, artifact)


def _render_finalized_outputs(outputs):
    rendered = migration._render_outputs(outputs)
    names = {name for name, _ in rendered}
    if names != EXPECTED_DESTINATION_NAMES:
        raise FinalizationError("rendered destination names mismatch")
    return rendered


def write_finalized_outputs(
    source_dir=migration.SOURCE_DIR,
    adjudication_path=ADJUDICATION_PATH,
    output_dir=OUTPUT_DIR,
):
    """Validate and atomically write the exact finalized sidecar set."""
    outputs = build_finalized_outputs(source_dir, adjudication_path)
    rendered = _render_finalized_outputs(outputs)
    migration._write_rendered_outputs(rendered, output_dir)


def check_finalized_outputs(
    source_dir=migration.SOURCE_DIR,
    adjudication_path=ADJUDICATION_PATH,
    output_dir=OUTPUT_DIR,
):
    """Byte-compare fresh finalized output with all active destinations."""
    outputs = build_finalized_outputs(source_dir, adjudication_path)
    rendered = _render_finalized_outputs(outputs)
    output_dir = Path(output_dir)
    if not output_dir.is_dir():
        raise FinalizationError(f"output destination is not a directory: {output_dir}")
    actual_names = {path.name for path in output_dir.glob("*.sidecar.json")}
    unexpected = sorted(actual_names - EXPECTED_DESTINATION_NAMES)
    missing = sorted(EXPECTED_DESTINATION_NAMES - actual_names)
    if unexpected:
        raise FinalizationError(
            f"unexpected destination sidecars in {output_dir}: {unexpected}"
        )
    if missing:
        raise FinalizationError(
            f"missing destination sidecars in {output_dir}: {missing}"
        )
    for name, expected_bytes in rendered:
        actual_bytes = (output_dir / name).read_bytes()
        if actual_bytes != expected_bytes:
            raise FinalizationError(f"finalized sidecar byte drift: {name}")


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="validate committed bytes")
    mode.add_argument("--write", action="store_true", help="validate and write outputs")
    return parser.parse_args(argv)


def main(
    argv=None,
    source_dir=migration.SOURCE_DIR,
    adjudication_path=ADJUDICATION_PATH,
    output_dir=OUTPUT_DIR,
):
    args = parse_args(argv)
    try:
        if args.write:
            write_finalized_outputs(source_dir, adjudication_path, output_dir)
        else:
            check_finalized_outputs(source_dir, adjudication_path, output_dir)
    except (FinalizationError, migration.MigrationError, OSError) as error:
        print(f"schema-v3 finalization: ERROR: {error}", file=sys.stderr)
        return 1
    print(SUCCESS_LINE)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
