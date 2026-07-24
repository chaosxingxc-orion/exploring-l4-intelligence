#!/usr/bin/env python3
"""Validate, freeze, then compare Agentic calibration R1 raw outputs.

This module enforces ordering: two exact completed N=56 files must validate
before either is frozen into the calibration release and before agreement is
computed.  It performs literature coding governance only, never research
execution, benchmarks, reproduction or prototypes.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import sf_stage1c_v2_calibration_agreement_v5 as agreement_v5
    import sf_stage1c_v2_precalibration_rc2r3 as rc2r3
else:
    from scripts.survey import sf_stage1c_v2_calibration_agreement_v5 as agreement_v5
    from scripts.survey import sf_stage1c_v2_precalibration_rc2r3 as rc2r3


class CalibrationRunError(RuntimeError):
    """Raised when raw-output ordering or identity is invalid."""


def _sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def validate_response_file(
    package: dict[str, Any], path: Path, *, coder_id: str, transaction_id: str,
) -> dict[str, Any]:
    if not path.is_file():
        raise CalibrationRunError(f"response file is missing: {path}")
    raw = path.read_bytes()
    try:
        rows = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise CalibrationRunError(f"response file is not UTF-8 JSON: {path}") from error
    if not isinstance(rows, list) or len(rows) != 56:
        raise CalibrationRunError("response file must contain exact N=56 objects")
    expected_ids = [item["canonical_id"] for item in package["blind_packet"]["items"]]
    actual_ids = [row.get("paper_id") if isinstance(row, dict) else None for row in rows]
    if actual_ids != expected_ids or len(set(actual_ids)) != 56:
        raise CalibrationRunError("response file paper order/identity differs from frozen exact N=56")
    response_ids: list[str] = []
    for row in rows:
        if row.get("coder_id") != coder_id or row.get("coder_transaction_id") != transaction_id:
            raise CalibrationRunError("response coder binding differs from assigned transaction")
        try:
            rc2r3.validate_completed_response(
                row, package["response_schema"], package["source_manifest"]
            )
        except (rc2r3.ContractError, ValueError) as error:
            raise CalibrationRunError(f"completed response validation failed: {error}") from error
        response_id = row.get("response_id")
        if not isinstance(response_id, str) or not response_id:
            raise CalibrationRunError("completed response lacks response_id")
        response_ids.append(response_id)
    if len(set(response_ids)) != 56:
        raise CalibrationRunError("response file contains duplicate response_id")
    return {
        "path": str(path), "bytes": len(raw), "sha256": _sha256(raw),
        "response_count": len(rows), "coder_id": coder_id,
        "coder_transaction_id": transaction_id, "schema_valid": True,
        "_raw": raw, "_rows": rows,
    }


def inspect_response_pair(
    package: dict[str, Any], coder_a_path: Path, coder_b_path: Path, *,
    expected_bindings: dict[str, tuple[str, str]],
) -> dict[str, Any]:
    if set(expected_bindings) != {"A", "B"}:
        raise CalibrationRunError("expected bindings must contain exact A/B slots")
    files = {"A": coder_a_path, "B": coder_b_path}
    present = {slot: path.is_file() for slot, path in files.items()}
    if not all(present.values()):
        return {
            "status": "RESPONSES_PENDING", "present": present,
            "both_raw_outputs_valid": False, "agreement_computed": False,
        }
    validated: dict[str, Any] = {}
    for slot in ("A", "B"):
        coder_id, transaction_id = expected_bindings[slot]
        validated[slot] = validate_response_file(
            package, files[slot], coder_id=coder_id, transaction_id=transaction_id
        )
    return {
        "status": "BOTH_RAW_OUTPUTS_VALID_NOT_FROZEN",
        "present": present, "both_raw_outputs_valid": True,
        "agreement_computed": False, "validated": validated,
    }


def _public_record(record: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in record.items() if not key.startswith("_")}


def _nested_value(value: dict[str, Any], path: str) -> Any:
    current: Any = value
    for part in path.split("."):
        if not isinstance(current, dict) or part not in current:
            raise CalibrationRunError(f"disagreement input lacks critical path: {path}")
        current = current[part]
    return current


def _object_map(row: dict[str, Any], array_name: str) -> dict[str, dict[str, Any]]:
    indexed: dict[str, dict[str, Any]] = {}
    objects = row.get(array_name, [])
    if not isinstance(objects, list):
        raise CalibrationRunError(f"{array_name} must be an array")
    for obj in objects:
        if not isinstance(obj, dict):
            raise CalibrationRunError(f"{array_name} contains a non-object")
        key = obj.get("object_match_key")
        if not isinstance(key, str) or not key:
            raise CalibrationRunError(f"{array_name} object lacks object_match_key")
        if key in indexed:
            raise CalibrationRunError(f"duplicate {array_name} object_match_key: {key}")
        indexed[key] = obj
    return indexed


def build_disagreement_package(
    coder_a: list[dict[str, Any]], coder_b: list[dict[str, Any]],
) -> dict[str, Any]:
    """Preserve exact pre-adjudication paper and object disagreements.

    This is an evidence export, not an adjudicator.  Values from both coders
    remain visible so an owner can distinguish label disagreement from object
    segmentation or match-key failure.
    """
    if len(coder_a) != len(coder_b):
        raise CalibrationRunError("disagreement inputs must have equal paper counts")
    left_by_id = {row.get("paper_id"): row for row in coder_a}
    right_by_id = {row.get("paper_id"): row for row in coder_b}
    if (
        None in left_by_id or None in right_by_id
        or len(left_by_id) != len(coder_a) or len(right_by_id) != len(coder_b)
        or set(left_by_id) != set(right_by_id)
    ):
        raise CalibrationRunError("disagreement inputs must bind the same unique paper IDs")

    paper_disagreements: list[dict[str, Any]] = []
    for paper_id in left_by_id:
        left_labels = left_by_id[paper_id]["paper_labels"]
        right_labels = right_by_id[paper_id]["paper_labels"]
        for field in (*agreement_v5.SINGLE_LABEL_FIELDS, *agreement_v5.MULTILABEL_FIELDS):
            left_value = _nested_value(left_labels, field)
            right_value = _nested_value(right_labels, field)
            if left_value != right_value:
                paper_disagreements.append({
                    "paper_id": paper_id,
                    "field": field,
                    "coder_a": left_value,
                    "coder_b": right_value,
                })

    object_types: dict[str, Any] = {}
    for array_name in agreement_v5.OBJECT_ARRAYS:
        left_objects: dict[str, dict[str, Any]] = {}
        right_objects: dict[str, dict[str, Any]] = {}
        left_key_papers: dict[str, str] = {}
        right_key_papers: dict[str, str] = {}
        for paper_id in left_by_id:
            for key, obj in _object_map(left_by_id[paper_id], array_name).items():
                if key in left_objects:
                    raise CalibrationRunError(f"duplicate cross-paper {array_name} key: {key}")
                left_objects[key] = obj
                left_key_papers[key] = paper_id
            for key, obj in _object_map(right_by_id[paper_id], array_name).items():
                if key in right_objects:
                    raise CalibrationRunError(f"duplicate cross-paper {array_name} key: {key}")
                right_objects[key] = obj
                right_key_papers[key] = paper_id
        left_keys = sorted(left_objects)
        right_keys = sorted(right_objects)
        matched_keys = sorted(set(left_keys) & set(right_keys))
        field_disagreements: list[dict[str, Any]] = []
        for key in matched_keys:
            for field in agreement_v5.CRITICAL_OBJECT_FIELDS[array_name]:
                left_value = _nested_value(left_objects[key], field)
                right_value = _nested_value(right_objects[key], field)
                if left_value != right_value:
                    field_disagreements.append({
                        "object_match_key": key,
                        "paper_id": left_key_papers[key],
                        "field": field,
                        "coder_a": left_value,
                        "coder_b": right_value,
                    })
        only_a = sorted(set(left_keys) - set(right_keys))
        only_b = sorted(set(right_keys) - set(left_keys))
        object_types[array_name] = {
            "coder_a_objects": len(left_keys),
            "coder_b_objects": len(right_keys),
            "matched_objects": len(matched_keys),
            "matched_keys": matched_keys,
            "coder_a_keys": left_keys,
            "coder_b_keys": right_keys,
            "coder_a_only": [
                {"paper_id": left_key_papers[key], "object_match_key": key,
                 "object": left_objects[key]}
                for key in only_a
            ],
            "coder_b_only": [
                {"paper_id": right_key_papers[key], "object_match_key": key,
                 "object": right_objects[key]}
                for key in only_b
            ],
            "matched_field_disagreements": field_disagreements,
        }
    return {
        "schema": "sf-stage1c-v2-calibration-disagreement-package-v1",
        "adjudication_applied": False,
        "paper_count": len(coder_a),
        "paper_disagreements": paper_disagreements,
        "object_types": object_types,
    }


def freeze_and_compute(
    package: dict[str, Any], inspection: dict[str, Any], *,
    runtime_intake: dict[str, Any], delivery_receipts: list[dict[str, Any]],
    destination: Path,
) -> dict[str, Any]:
    if not inspection.get("both_raw_outputs_valid") or "validated" not in inspection:
        raise CalibrationRunError("both raw outputs must validate before freeze or agreement")
    if destination.exists():
        raise CalibrationRunError(f"freeze destination already exists: {destination}")
    destination.mkdir(parents=True)
    frozen_paths = {
        "A": destination / "coder-a-responses.json",
        "B": destination / "coder-b-responses.json",
    }
    try:
        for slot in ("A", "B"):
            record = inspection["validated"][slot]
            frozen_paths[slot].write_bytes(record["_raw"])
            if (
                frozen_paths[slot].stat().st_size != record["bytes"]
                or _sha256(frozen_paths[slot].read_bytes()) != record["sha256"]
            ):
                raise CalibrationRunError(f"frozen coder {slot} bytes differ from validated raw output")
        agreement = agreement_v5.compute_agreement(
            inspection["validated"]["A"]["_rows"],
            inspection["validated"]["B"]["_rows"],
            runtime_intake=runtime_intake,
            frozen_contract=package["frozen_package_contract"],
            response_schema=package["response_schema"],
            source_manifest=package["source_manifest"],
            distribution_manifest=package["distribution_manifest"],
            delivery_receipt_schema=package["delivery_receipt_schema"],
            delivery_receipts=delivery_receipts,
        )
        agreement_path = destination / "pre-adjudication-agreement.json"
        agreement_path.write_bytes(rc2r3.json_bytes(agreement))
        freeze_manifest = {
            "schema": "sf-stage1c-v2-calibration-raw-output-freeze-v1",
            "status": "BOTH_RAW_OUTPUTS_FROZEN_AGREEMENT_COMPUTED",
            "coder_outputs": {
                slot: {**_public_record(inspection["validated"][slot]),
                       "frozen_path": str(frozen_paths[slot])}
                for slot in ("A", "B")
            },
            "agreement_path": str(agreement_path),
            "agreement_bytes": agreement_path.stat().st_size,
            "agreement_sha256": _sha256(agreement_path.read_bytes()),
        }
        (destination / "freeze-manifest.json").write_bytes(rc2r3.json_bytes(freeze_manifest))
    except Exception:
        # The caller must treat any partially materialized destination as invalid.
        raise
    return {
        "both_raw_outputs_frozen": True,
        "agreement": agreement,
        "freeze_manifest": freeze_manifest,
    }


if __name__ == "__main__":
    raise SystemExit("Import this module from the controlled calibration transaction.")
