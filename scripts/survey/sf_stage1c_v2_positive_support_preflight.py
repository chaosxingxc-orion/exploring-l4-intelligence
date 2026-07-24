#!/usr/bin/env python3
"""Fail-closed positive-support audit for Stage-1C calibration packets.

The audit is reviewer-only.  It verifies that every mandatory object class has
at least one source-supported positive in the frozen N=56 packet and detects
fields that a blind coder cannot observe under the packet access contract.  It
does not change the sample, assign expected coder labels, or execute research.
"""

from __future__ import annotations

from typing import Any


class PreflightError(RuntimeError):
    """Raised when reviewer-only preflight evidence is malformed or leaks labels."""


REVIEWER_ONLY_VISIBILITY = "REVIEWER_ONLY_NOT_DISTRIBUTED"
LOCAL_ONLY_BLIND_FIELDS = frozenset({"local_asset_state"})
FORBIDDEN_LEDGER_KEYS = frozenset(
    {
        "expected_label",
        "expected_labels",
        "selection_rationale",
        "coder_instruction",
        "prior_label",
        "readiness",
    }
)
OBJECT_DEFINITION_NAMES = {
    "dataset_edges": "dataset_edge",
    "reproduction_evidence": "reproduction_evidence",
}


def _scan_forbidden_keys(value: Any, path: str = "$") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            if key in FORBIDDEN_LEDGER_KEYS:
                raise PreflightError(f"forbidden leakage key at {path}.{key}")
            _scan_forbidden_keys(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _scan_forbidden_keys(child, f"{path}[{index}]")


def _rendition_ids(item: dict[str, Any]) -> set[str]:
    renditions = [item.get("primary_rendition"), *item.get("alternate_renditions", [])]
    return {
        rendition["rendition_id"]
        for rendition in renditions
        if isinstance(rendition, dict) and isinstance(rendition.get("rendition_id"), str)
    }


def _validate_evidence_row(
    row: Any, *, object_class: str, source_items: dict[str, dict[str, Any]],
) -> None:
    required = {
        "paper_id", "rendition_id", "locator", "support_type", "evidence_summary"
    }
    if not isinstance(row, dict) or set(row) != required:
        raise PreflightError(
            f"{object_class} evidence row must contain exact {sorted(required)}"
        )
    paper_id = row["paper_id"]
    if paper_id not in source_items:
        raise PreflightError(f"unknown paper in {object_class} evidence: {paper_id!r}")
    if row["rendition_id"] not in _rendition_ids(source_items[paper_id]):
        raise PreflightError(
            f"unknown rendition for {paper_id}: {row['rendition_id']!r}"
        )
    locator = row["locator"]
    if not isinstance(locator, dict) or set(locator) != {"page", "section"}:
        raise PreflightError(f"{object_class} locator must contain exact page/section")
    if isinstance(locator["page"], bool) or not isinstance(locator["page"], int) or locator["page"] <= 0:
        raise PreflightError(f"{object_class} locator requires a positive page")
    for field in ("section",):
        if not isinstance(locator[field], str) or not locator[field].strip():
            raise PreflightError(f"{object_class} locator {field} must be nonempty")
    for field in ("support_type", "evidence_summary"):
        if not isinstance(row[field], str) or not row[field].strip():
            raise PreflightError(f"{object_class} {field} must be nonempty")


def _validate_inputs(
    *, response_schema: dict[str, Any], blind_packet: dict[str, Any],
    source_manifest: dict[str, Any], evidence_ledger: dict[str, Any],
) -> tuple[list[str], dict[str, list[dict[str, Any]]], dict[str, dict[str, Any]]]:
    if evidence_ledger.get("visibility") != REVIEWER_ONLY_VISIBILITY:
        raise PreflightError("positive-support ledger must remain reviewer-only")
    _scan_forbidden_keys(evidence_ledger)
    mandatory = evidence_ledger.get("mandatory_object_classes")
    if (
        not isinstance(mandatory, list) or not mandatory
        or any(not isinstance(name, str) or not name for name in mandatory)
        or len(set(mandatory)) != len(mandatory)
    ):
        raise PreflightError("ledger requires a nonempty unique mandatory object-class list")
    unsupported = sorted(set(mandatory) - set(OBJECT_DEFINITION_NAMES))
    if unsupported:
        raise PreflightError(f"unsupported mandatory object classes: {unsupported}")
    evidence = evidence_ledger.get("evidence")
    if not isinstance(evidence, dict) or set(evidence) != set(mandatory):
        raise PreflightError("ledger evidence must contain the exact mandatory object classes")
    if not isinstance(source_manifest.get("items"), list):
        raise PreflightError("source manifest lacks items")
    source_items: dict[str, dict[str, Any]] = {}
    for item in source_manifest["items"]:
        paper_id = item.get("canonical_id") if isinstance(item, dict) else None
        if not isinstance(paper_id, str) or not paper_id or paper_id in source_items:
            raise PreflightError("source manifest paper IDs must be nonempty and unique")
        source_items[paper_id] = item
    packet_ids = [item.get("canonical_id") for item in blind_packet.get("items", [])]
    if packet_ids != list(source_items) or len(set(packet_ids)) != len(packet_ids):
        raise PreflightError("blind packet and source manifest must bind the same ordered papers")
    definitions = response_schema.get("$defs")
    if not isinstance(definitions, dict):
        raise PreflightError("response schema lacks definitions")
    for object_class in mandatory:
        definition = definitions.get(OBJECT_DEFINITION_NAMES[object_class])
        if not isinstance(definition, dict) or not isinstance(definition.get("required"), list):
            raise PreflightError(f"response schema lacks {object_class} object definition")
        rows = evidence[object_class]
        if not isinstance(rows, list):
            raise PreflightError(f"{object_class} evidence must be an array")
        for row in rows:
            _validate_evidence_row(row, object_class=object_class, source_items=source_items)
    return mandatory, evidence, source_items


def evaluate_preflight(
    *, response_schema: dict[str, Any], blind_packet: dict[str, Any],
    source_manifest: dict[str, Any], evidence_ledger: dict[str, Any],
    coder_responses: dict[str, list[dict[str, Any]]] | None = None,
) -> dict[str, Any]:
    """Evaluate blind observability and mandatory positive support.

    When frozen R1 responses are supplied, their object counts are diagnostic
    only; they never turn a source-support preflight failure into a pass.
    """
    mandatory, evidence, _ = _validate_inputs(
        response_schema=response_schema,
        blind_packet=blind_packet,
        source_manifest=source_manifest,
        evidence_ledger=evidence_ledger,
    )
    if coder_responses is not None and set(coder_responses) != {"A", "B"}:
        raise PreflightError("coder response diagnostics require exact A/B slots")

    defects: list[str] = []
    definitions = response_schema["$defs"]
    repository_withheld = blind_packet.get("repository_access_should_be_withheld") is True
    object_classes: dict[str, Any] = {}
    for object_class in mandatory:
        definition_name = OBJECT_DEFINITION_NAMES[object_class]
        required = set(definitions[definition_name]["required"])
        if repository_withheld:
            for field in sorted(required & LOCAL_ONLY_BLIND_FIELDS):
                defects.append(
                    "BLIND_FIELD_DEPENDS_ON_WITHHELD_REPOSITORY_STATE:"
                    f"{object_class}.{field}"
                )
        rows = evidence[object_class]
        support_count = len(rows)
        if support_count == 0:
            defects.append(f"MANDATORY_CLASS_ZERO_POSITIVE:{object_class}")
        coder_counts: dict[str, int] | None = None
        if coder_responses is not None:
            coder_counts = {}
            for slot in ("A", "B"):
                responses = coder_responses[slot]
                if not isinstance(responses, list):
                    raise PreflightError(f"coder {slot} responses must be an array")
                count = 0
                for response in responses:
                    objects = response.get(object_class) if isinstance(response, dict) else None
                    if not isinstance(objects, list):
                        raise PreflightError(
                            f"coder {slot} response lacks {object_class} array"
                        )
                    count += len(objects)
                coder_counts[slot] = count
            if support_count > 0 and coder_counts == {"A": 0, "B": 0}:
                defects.append(
                    f"POSITIVE_SUPPORT_MISSED_BY_BOTH_CODERS:{object_class}"
                )
        object_classes[object_class] = {
            "support_count": support_count,
            "support_status": "SUPPORTED" if support_count else "ZERO_POSITIVE",
            "coder_object_counts": coder_counts,
        }
    return {
        "schema": "sf-stage1c-v2-positive-support-preflight-result-v1",
        "status": "FAIL" if defects else "PASS",
        "reviewer_only": True,
        "sample_size": len(source_manifest["items"]),
        "mandatory_object_classes": mandatory,
        "object_classes": object_classes,
        "defects": defects,
        "sample_modified": False,
        "coder_packet_modified": False,
        "research_execution": False,
    }


if __name__ == "__main__":
    raise SystemExit("Import this reviewer-only checker from a controlled audit transaction.")
