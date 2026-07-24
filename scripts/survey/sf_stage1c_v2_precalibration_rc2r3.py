#!/usr/bin/env python3
"""Build and verify Agentic RC2R3 runtime-integrity contract.

RC2R3 is an immutable successor to RC2R2.  It changes only the frozen
agreement threshold, receiver-side delivery proof, and structural path model.
It does not distribute coders or execute research.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Iterable, TypeAlias

from jsonschema import Draft202012Validator, ValidationError

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import sf_stage1c_v2_precalibration_rc2r2 as rc2r2
else:
    from scripts.survey import sf_stage1c_v2_precalibration_rc2r2 as rc2r2


REPO = Path(__file__).resolve().parents[2]
WORKBENCH = REPO / "wiki/survey/workbench/system-first-stage1c-v2-precalibration-rc2r3"
CHECK_DIR = REPO / "docs/checks/stage1c-v2-precalibration/2026-07-24-rc2r3"
REPORT_PATH = CHECK_DIR / "contract-report.json"
REVIEW_MANIFEST_PATH = WORKBENCH / "review-package-manifest-rc2r3.json"
OWNER_AUTHORIZATION = REPO / (
    "wiki/audit/system-first-stage1c-v2-precalibration/"
    "owner-rc2r3-runtime-integrity-repair-authorization/"
    "2026-07-24-owner-rc2r3-runtime-integrity-repair-authorization.md"
)
RC2R2_REVIEW = REPO / (
    "wiki/audit/system-first-stage1c-v2-precalibration/"
    "agentic-rc2r2-independent-method-review/"
    "2026-07-24-stage1c-v2-agentic-rc2r2-independent-method-review.md"
)
RC2R2_REVIEW_MANIFEST = (
    REPO / "wiki/survey/workbench/system-first-stage1c-v2-precalibration-rc2r2/"
    "review-package-manifest-rc2r2.json"
)

ARTIFACT_PATHS = {
    "response_schema": WORKBENCH / "calibration-response-schema-v4-inherited.json",
    "schema_bundle": WORKBENCH / "schema-bundle-v4-inherited.json",
    "source_manifest": WORKBENCH / "calibration-source-byte-manifest-v4-inherited.json",
    "acl_acquisition_receipts": WORKBENCH / "acl-acquisition-receipts-v2-inherited.json",
    "calibration_manifest": WORKBENCH / "calibration-manifest-v5.json",
    "blind_packet": WORKBENCH / "calibration-blind-packet-v4-inherited.json",
    "assignment_manifest": WORKBENCH / "calibration-assignment-manifest-v4-inherited.json",
    "claim_templates": WORKBENCH / "claim-template-registry-v4-inherited.json",
    "claim_template_coder_view": WORKBENCH / "claim-template-coder-view-v4-inherited.json",
    "coder_codebook": WORKBENCH / "coder-codebook-v4-inherited.json",
    "coder_prompt": WORKBENCH / "coder-prompt-v4-inherited.json",
    "agreement": WORKBENCH / "agreement-contract-v5.json",
    "agreement_intake_contract": WORKBENCH / "agreement-intake-contract-v5.json",
    "delivery_receipt_schema": WORKBENCH / "delivery-receipt-schema-v2.json",
    "delivery_receipt_template": WORKBENCH / "delivery-receipt-template-v2.json",
    "frozen_package_contract": WORKBENCH / "frozen-package-contract-v2.json",
    "coder_transaction": WORKBENCH / "coder-transaction-contract-v5.json",
    "reproduction_readiness": WORKBENCH / "reproduction-readiness-v4-inherited.json",
    "distribution_manifest": WORKBENCH / "calibration-distribution-manifest-v5.json",
}

CODER_DISTRIBUTION_ALLOWED_ARTIFACTS = rc2r2.CODER_DISTRIBUTION_ALLOWED_ARTIFACTS
CODER_DISTRIBUTION_FORBIDDEN_KEYS = rc2r2.CODER_DISTRIBUTION_FORBIDDEN_KEYS
CODER_VIEW_FORBIDDEN_NAMED_EXPECTATIONS = rc2r2.CODER_VIEW_FORBIDDEN_NAMED_EXPECTATIONS
BASE_CALIBRATED_OBJECT_ARRAYS = rc2r2.BASE_CALIBRATED_OBJECT_ARRAYS

AGREEMENT_MINIMUM = 0.85
CALIBRATION_MANIFEST_ID = "SF-STAGE1C-V2-CALIBRATION-PACKET-56-RC2R3"
DISTRIBUTION_MANIFEST_ID = "SF-STAGE1C-V2-CALIBRATION-DISTRIBUTION-RC2R3"
AGREEMENT_INTAKE_ID = "SF-STAGE1C-V2-AGREEMENT-INTAKE-RC2R3"
DELIVERY_RECEIPT_SCHEMA_ID = "sf-stage1c-v2-delivery-receipt-schema-v2"


class ContractError(RuntimeError):
    """Raised when the RC2R3 contract cannot prove a closed gate."""


json_bytes = rc2r2.json_bytes
sha256_bytes = rc2r2.sha256_bytes
sha256_path = rc2r2.sha256_path
load_json = rc2r2.load_json
write_json = rc2r2.write_json
_rendition_map = rc2r2._rendition_map


PathSegment: TypeAlias = tuple[str, str | int]
TypedPath: TypeAlias = tuple[PathSegment, ...]
PathPattern: TypeAlias = tuple[PathSegment, ...]
ANY_INDEX = "*"


def _pattern(*segments: PathSegment) -> PathPattern:
    return segments


_IDENTITY_PATH_PATTERNS: dict[str, tuple[PathPattern, ...]] = {
    "source_manifest": (
        _pattern(("key", "source_manifest"), ("key", "items"), ("index", ANY_INDEX), ("key", "canonical_id")),
        _pattern(("key", "source_manifest"), ("key", "items"), ("index", ANY_INDEX), ("key", "source_item_id")),
        _pattern(("key", "source_manifest"), ("key", "items"), ("index", ANY_INDEX), ("key", "source_revision")),
        _pattern(("key", "source_manifest"), ("key", "items"), ("index", ANY_INDEX), ("key", "primary_rendition"), ("key", "rendition_id")),
        _pattern(("key", "source_manifest"), ("key", "items"), ("index", ANY_INDEX), ("key", "primary_rendition"), ("key", "locator")),
        _pattern(("key", "source_manifest"), ("key", "items"), ("index", ANY_INDEX), ("key", "alternate_renditions"), ("index", ANY_INDEX), ("key", "rendition_id")),
        _pattern(("key", "source_manifest"), ("key", "items"), ("index", ANY_INDEX), ("key", "alternate_renditions"), ("index", ANY_INDEX), ("key", "locator")),
        _pattern(("key", "source_manifest"), ("key", "items"), ("index", ANY_INDEX), ("key", "ledger_binding"), ("key", "source_url")),
        _pattern(("key", "source_manifest"), ("key", "items"), ("index", ANY_INDEX), ("key", "ledger_binding"), ("key", "independent_receipt_id")),
    ),
    "assignment_manifest": tuple(
        _pattern(("key", "assignment_manifest"), ("key", "items"), ("index", ANY_INDEX), ("key", field))
        for field in ("source_item_id", "source_revision", "packet_item_id")
    ),
    "blind_packet": (
        *tuple(
            _pattern(("key", "blind_packet"), ("key", "items"), ("index", ANY_INDEX), ("key", field))
            for field in ("canonical_id", "source_item_id", "source_revision", "packet_item_id", "title")
        ),
        *tuple(
            _pattern(("key", "blind_packet"), ("key", "items"), ("index", ANY_INDEX), ("key", "blank_response"), ("key", field))
            for field in ("paper_id", "packet_item_id", "source_manifest_id")
        ),
    ),
}


def _path_matches(path: TypedPath, pattern: PathPattern) -> bool:
    if len(path) != len(pattern):
        return False
    return all(
        actual_kind == expected_kind
        and (expected_value == ANY_INDEX and expected_kind == "index" or actual_value == expected_value)
        for (actual_kind, actual_value), (expected_kind, expected_value) in zip(path, pattern)
    )


def _identity_value_allowed(artifact: str, path: TypedPath) -> bool:
    return any(_path_matches(path, pattern) for pattern in _IDENTITY_PATH_PATTERNS.get(artifact, ()))


def _display_path(path: TypedPath) -> str:
    rendered = "$"
    for kind, value in path:
        if kind == "index":
            rendered += f"[{value}]"
        else:
            escaped = str(value).replace("~", "~0").replace("/", "~1")
            rendered += f"/{escaped}"
    return rendered


def _scan_value(value: Any, *, artifact: str, path: TypedPath) -> list[str]:
    leaks: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = (*path, ("key", key))
            if key in CODER_DISTRIBUTION_FORBIDDEN_KEYS:
                leaks.append(f"FORBIDDEN_KEY:{artifact}:{_display_path(child_path)}")
            leaks.extend(_scan_value(child, artifact=artifact, path=child_path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            leaks.extend(_scan_value(child, artifact=artifact, path=(*path, ("index", index))))
    elif isinstance(value, str) and not _identity_value_allowed(artifact, path):
        folded = value.casefold()
        for forbidden in CODER_VIEW_FORBIDDEN_NAMED_EXPECTATIONS:
            if forbidden.casefold() in folded:
                leaks.append(f"FORBIDDEN_VALUE:{artifact}:{_display_path(path)}:{forbidden}")
    return leaks


def scan_coder_bundle_leaks(package: dict[str, Any], names: tuple[str, ...] | list[str]) -> list[str]:
    names = tuple(names)
    leaks: list[str] = []
    if names != CODER_DISTRIBUTION_ALLOWED_ARTIFACTS:
        leaks.append(f"ARTIFACT_ALLOWLIST_MISMATCH:{names!r}")
    for name in names:
        if name not in package:
            leaks.append(f"MISSING_ARTIFACT:{name}")
            continue
        leaks.extend(_scan_value(package[name], artifact=name, path=(("key", name),)))
    return sorted(set(leaks))


def coder_bundle_sha256_from_raw(raw_artifacts: dict[str, bytes], names: tuple[str, ...]) -> str:
    digest = hashlib.sha256()
    for name in names:
        raw = raw_artifacts[name]
        digest.update(name.encode("utf-8"))
        digest.update(b"\0")
        digest.update(len(raw).to_bytes(8, "big"))
        digest.update(raw)
    return digest.hexdigest()


def coder_bundle_sha256(package: dict[str, Any], names: tuple[str, ...]) -> str:
    return coder_bundle_sha256_from_raw({name: json_bytes(package[name]) for name in names}, names)


def build_agreement_contract(predecessor: dict[str, Any]) -> dict[str, Any]:
    value = copy.deepcopy(predecessor)
    value.update({
        "schema": "sf-stage1c-v2-agreement-contract-v5",
        "artifact_id": "SF-STAGE1C-V2-AGREEMENT-CONTRACT-RC2R3",
        "agreement_intake_contract_id": AGREEMENT_INTAKE_ID,
        "minimum_gate_value": AGREEMENT_MINIMUM,
        "agreement_minimum": AGREEMENT_MINIMUM,
        "threshold_override_prohibited": True,
        "receiver_actual_bytes_required": True,
        "typed_structural_path_allowlist_required": True,
    })
    return value


def build_distribution_manifest(package: dict[str, Any]) -> dict[str, Any]:
    names = CODER_DISTRIBUTION_ALLOWED_ARTIFACTS
    raw = {name: json_bytes(package[name]) for name in names}
    return {
        "schema": "sf-stage1c-v2-calibration-distribution-manifest-v5",
        "artifact_id": DISTRIBUTION_MANIFEST_ID,
        "status": "FROZEN_INPUT_BYTES_PREPARED_NOT_DISTRIBUTED",
        "scope": "CODER_VISIBLE_SHARED_CONTENT",
        "artifacts": [{
            "artifact_name": name,
            "path": ARTIFACT_PATHS[name].relative_to(REPO).as_posix(),
            "bytes": len(raw[name]), "sha256": sha256_bytes(raw[name]),
        } for name in names],
        "content_bundle_sha256": coder_bundle_sha256_from_raw(raw, names),
        "coder_prompt_sha256": sha256_bytes(raw["coder_prompt"]),
        "receiver_must_hash_actual_artifact_bytes": True,
        "receiver_must_hash_actual_prompt_bytes": True,
        "both_coders_must_receive_byte_identical_content": True,
        "typed_path_identity_allowlist_required": True,
        "distribution_authorized": False,
        "post_accept_owner_authorization_recorded": True,
    }


def _strict_object(required: list[str], properties: dict[str, Any]) -> dict[str, Any]:
    return {"type": "object", "additionalProperties": False, "required": required, "properties": properties}


def build_delivery_receipt_schema() -> dict[str, Any]:
    text = {"type": "string", "minLength": 1}
    sha = {"type": "string", "pattern": "^[0-9a-f]{64}$"}
    artifact = _strict_object(
        ["artifact_name", "bytes", "sha256"],
        {"artifact_name": text, "bytes": {"type": "integer", "minimum": 1}, "sha256": sha},
    )
    properties = {
        "schema": {"const": "sf-stage1c-v2-delivery-receipt-v2"},
        "receipt_id": text, "coder_slot": {"enum": ["A", "B"]},
        "coder_id": text, "coder_transaction_id": text, "process_id": text, "task_id": text,
        "model": {"enum": ["gpt-5.6-sol", "gpt-5.6-terra"]},
        "distribution_manifest_id": {"const": DISTRIBUTION_MANIFEST_ID},
        "received_content_bundle_sha256": sha, "received_prompt_sha256": sha,
        "received_artifacts": {"type": "array", "items": artifact, "minItems": 8, "maxItems": 8},
        "delivered_at": text, "submitted_at": text,
        "status": {"const": "FROZEN_SUBMITTED"}, "receipt_sha256": sha,
    }
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": DELIVERY_RECEIPT_SCHEMA_ID,
        **_strict_object(list(properties), properties),
    }


def _receipt_projection(receipt: dict[str, Any]) -> dict[str, Any]:
    value = copy.deepcopy(receipt)
    value.pop("receipt_sha256", None)
    return value


def build_delivery_receipt_template() -> dict[str, Any]:
    return {
        "schema": "sf-stage1c-v2-delivery-receipt-template-v2",
        "artifact_id": "SF-STAGE1C-V2-DELIVERY-RECEIPT-TEMPLATE-RC2R3",
        "status": "TEMPLATE_ONLY_NOT_A_RECEIPT",
        "delivery_receipt_schema_id": DELIVERY_RECEIPT_SCHEMA_ID,
        "receipt_source": "RECEIVER_SIDE_ACTUAL_BYTES_ONLY",
        "runtime_required_fields": [
            "receipt_id", "coder_slot", "coder_id", "coder_transaction_id", "process_id",
            "task_id", "model", "distribution_manifest_id", "received_content_bundle_sha256",
            "received_prompt_sha256", "received_artifacts", "delivered_at", "submitted_at",
            "status", "receipt_sha256",
        ],
        "receipt_digest_rule": "SHA256_OF_CANONICAL_PRETTY_JSON_WITHOUT_RECEIPT_SHA256",
    }


def build_agreement_intake_contract(package: dict[str, Any]) -> dict[str, Any]:
    predecessor = rc2r2.build_agreement_intake_contract(package)
    predecessor.update({
        "schema": "sf-stage1c-v2-agreement-intake-contract-v5",
        "artifact_id": AGREEMENT_INTAKE_ID,
        "calibration_manifest_id": CALIBRATION_MANIFEST_ID,
        "distribution_manifest_id": DISTRIBUTION_MANIFEST_ID,
        "delivery_receipt_schema_id": DELIVERY_RECEIPT_SCHEMA_ID,
        "agreement_minimum": AGREEMENT_MINIMUM,
        "actual_receiver_bytes_required": True,
    })
    for slot in predecessor["coder_slots"]:
        slot["task_id"] = None
    return predecessor


def static_intake_projection(intake: dict[str, Any]) -> dict[str, Any]:
    fixed = (
        "schema", "artifact_id", "calibration_manifest_id", "response_schema_id",
        "source_manifest_id", "distribution_manifest_id", "delivery_receipt_schema_id",
        "content_bundle_sha256", "prompt_hash", "agreement_minimum",
        "actual_receiver_bytes_required", "N", "canonical_paper_ids", "items",
        "completed_response_validator_required", "raw_outputs_frozen_before_agreement",
    )
    try:
        projection = {key: copy.deepcopy(intake[key]) for key in fixed}
        projection["coder_slots"] = [{
            "coder_slot": slot["coder_slot"], "planned_model": slot["planned_model"],
            "expected_content_bundle_sha256": slot["expected_content_bundle_sha256"],
            "expected_prompt_hash": slot["expected_prompt_hash"],
        } for slot in intake["coder_slots"]]
    except (KeyError, TypeError) as error:
        raise ContractError("agreement intake lacks frozen RC2R3 base fields") from error
    return projection


def build_frozen_package_contract(package: dict[str, Any]) -> dict[str, Any]:
    distribution = package["distribution_manifest"]
    intake = package["agreement_intake_contract"]
    return {
        "schema": "sf-stage1c-v2-frozen-package-contract-v2",
        "artifact_id": "SF-STAGE1C-V2-FROZEN-PACKAGE-CONTRACT-RC2R3",
        "status": "COMPILED_ROOT_OF_TRUST_INPUT",
        "agreement_minimum": AGREEMENT_MINIMUM,
        "calibration_manifest_id": CALIBRATION_MANIFEST_ID,
        "calibration_manifest_sha256": sha256_bytes(json_bytes(package["calibration_manifest"])),
        "source_manifest_id": package["source_manifest"]["artifact_id"],
        "source_manifest_sha256": sha256_bytes(json_bytes(package["source_manifest"])),
        "distribution_manifest_id": DISTRIBUTION_MANIFEST_ID,
        "distribution_manifest_sha256": sha256_bytes(json_bytes(distribution)),
        "response_schema_id": package["response_schema"]["$id"],
        "response_schema_sha256": sha256_bytes(json_bytes(package["response_schema"])),
        "delivery_receipt_schema_id": DELIVERY_RECEIPT_SCHEMA_ID,
        "delivery_receipt_schema_sha256": sha256_bytes(json_bytes(package["delivery_receipt_schema"])),
        "base_intake_static_sha256": sha256_bytes(json_bytes(static_intake_projection(intake))),
        "paper_rendition_map_sha256": sha256_bytes(json_bytes(_rendition_map(package["source_manifest"]))),
        "content_bundle_sha256": distribution["content_bundle_sha256"],
        "prompt_sha256": distribution["coder_prompt_sha256"],
        "N": 56,
        "canonical_paper_ids_sha256": sha256_bytes(json_bytes(intake["canonical_paper_ids"])),
        "compiled_into_agreement_engine": True,
    }


def build_package() -> dict[str, Any]:
    package = copy.deepcopy(rc2r2.build_package())
    package["calibration_manifest"].update({
        "schema": "sf-stage1c-v2-calibration-manifest-v5",
        "artifact_id": CALIBRATION_MANIFEST_ID,
        "status": "AGENTIC_RC2R3_CODER_READY_NOT_DISTRIBUTED",
        "rc2r2_predecessor_immutable": True,
    })
    package["agreement"] = build_agreement_contract(package["agreement"])
    package["delivery_receipt_schema"] = build_delivery_receipt_schema()
    package["delivery_receipt_template"] = build_delivery_receipt_template()
    package["distribution_manifest"] = build_distribution_manifest(package)
    package["coder_transaction"].update({
        "schema": "sf-stage1c-v2-coder-transaction-contract-v5",
        "artifact_id": "SF-STAGE1C-V2-CODER-INTAKE-RC2R3",
        "distribution_manifest_id": DISTRIBUTION_MANIFEST_ID,
        "delivery_receipt_schema_id": DELIVERY_RECEIPT_SCHEMA_ID,
        "shared_content_bundle_sha256": package["distribution_manifest"]["content_bundle_sha256"],
        "receiver_actual_bytes_required": True,
    })
    for slot in package["coder_transaction"]["coder_slots"]:
        slot["expected_content_bundle_sha256"] = package["distribution_manifest"]["content_bundle_sha256"]
        slot["expected_prompt_hash"] = package["distribution_manifest"]["coder_prompt_sha256"]
        slot["task_id"] = None
    package["agreement_intake_contract"] = build_agreement_intake_contract(package)
    package["frozen_package_contract"] = build_frozen_package_contract(package)
    return package


def validate_completed_response(response: dict[str, Any], schema: dict[str, Any], source_manifest: dict[str, Any]) -> None:
    try:
        rc2r2.validate_completed_response(response, schema, source_manifest)
    except (rc2r2.ContractError, ValidationError) as error:
        raise ContractError(str(error)) from error


def build_delivery_receipt(
    package: dict[str, Any], *, received_artifacts: dict[str, bytes], received_prompt_bytes: bytes,
    slot: str, coder_id: str, transaction_id: str, process_id: str, task_id: str,
    model: str, delivered_at: str, submitted_at: str,
) -> dict[str, Any]:
    names = CODER_DISTRIBUTION_ALLOWED_ARTIFACTS
    if not isinstance(received_artifacts, dict) or set(received_artifacts) != set(names):
        raise ContractError("delivery receipt requires exact actual received artifact set")
    if not isinstance(received_prompt_bytes, bytes):
        raise ContractError("actual received prompt must be bytes")
    for name in names:
        if not isinstance(received_artifacts[name], bytes):
            raise ContractError(f"actual received artifact {name} must be bytes")
    distribution = package["distribution_manifest"]
    expected = {row["artifact_name"]: row for row in distribution["artifacts"]}
    actual_rows = [{
        "artifact_name": name, "bytes": len(received_artifacts[name]),
        "sha256": sha256_bytes(received_artifacts[name]),
    } for name in names]
    for row in actual_rows:
        if row != {key: expected[row["artifact_name"]][key] for key in ("artifact_name", "bytes", "sha256")}:
            raise ContractError(f"actual received artifact differs: {row['artifact_name']}")
    actual_bundle = coder_bundle_sha256_from_raw(received_artifacts, names)
    if actual_bundle != distribution["content_bundle_sha256"]:
        raise ContractError("actual received artifact bundle differs")
    actual_prompt = sha256_bytes(received_prompt_bytes)
    if actual_prompt != distribution["coder_prompt_sha256"]:
        raise ContractError("actual received prompt differs")
    if received_prompt_bytes != received_artifacts["coder_prompt"]:
        raise ContractError("actual received prompt differs from coder_prompt artifact")
    receipt = {
        "schema": "sf-stage1c-v2-delivery-receipt-v2",
        "receipt_id": f"RC2R3-DELIVERY-{slot}-{transaction_id}-{task_id}",
        "coder_slot": slot, "coder_id": coder_id, "coder_transaction_id": transaction_id,
        "process_id": process_id, "task_id": task_id, "model": model,
        "distribution_manifest_id": distribution["artifact_id"],
        "received_content_bundle_sha256": actual_bundle,
        "received_prompt_sha256": actual_prompt,
        "received_artifacts": actual_rows,
        "delivered_at": delivered_at, "submitted_at": submitted_at,
        "status": "FROZEN_SUBMITTED",
    }
    receipt["receipt_sha256"] = sha256_bytes(json_bytes(_receipt_projection(receipt)))
    try:
        Draft202012Validator(package["delivery_receipt_schema"]).validate(receipt)
    except ValidationError as error:
        raise ContractError(f"invalid actual-byte delivery receipt: {error.message}") from error
    return receipt


def bind_runtime_intake(
    package: dict[str, Any], bindings: Iterable[dict[str, str]], receipts: list[dict[str, Any]],
) -> dict[str, Any]:
    intake = copy.deepcopy(package["agreement_intake_contract"])
    binding_by_slot = {row["slot"]: row for row in bindings}
    receipt_by_slot = {row["coder_slot"]: row for row in receipts}
    if set(binding_by_slot) != {"A", "B"} or set(receipt_by_slot) != {"A", "B"}:
        raise ContractError("runtime intake requires exact A/B bindings and actual-byte receipts")
    intake["status"] = "BOUND_FOR_PRE_ADJUDICATION_AGREEMENT"
    for target in intake["coder_slots"]:
        slot = target["coder_slot"]
        binding, receipt = binding_by_slot[slot], receipt_by_slot[slot]
        for receipt_key, binding_key in (
            ("coder_id", "coder_id"), ("coder_transaction_id", "transaction_id"),
            ("process_id", "process_id"), ("task_id", "task_id"), ("model", "model"),
        ):
            if receipt.get(receipt_key) != binding.get(binding_key):
                raise ContractError(f"runtime binding differs from receipt {receipt_key}")
        target.update({
            "model": binding["model"], "coder_id": binding["coder_id"],
            "coder_transaction_id": binding["transaction_id"], "process_id": binding["process_id"],
            "task_id": binding["task_id"], "assignment_status": "FROZEN_SUBMITTED",
            "distribution_receipt_id": receipt["receipt_id"],
            "submission_receipt_id": f"SUBMISSION-{receipt['receipt_id']}",
            "delivery_receipt_id": receipt["receipt_id"],
            "delivery_receipt_sha256": receipt["receipt_sha256"],
            "received_content_bundle_sha256": receipt["received_content_bundle_sha256"],
            "received_prompt_sha256": receipt["received_prompt_sha256"],
        })
    return intake


def verify_rc2r2_immutable() -> None:
    commit = "9652d98eade798903be6c5d007591d2602a2f5c3"
    manifest_rel = RC2R2_REVIEW_MANIFEST.relative_to(REPO).as_posix()
    try:
        manifest = json.loads(subprocess.check_output(["git", "show", f"{commit}:{manifest_rel}"], cwd=REPO))
    except (subprocess.CalledProcessError, json.JSONDecodeError) as error:
        raise ContractError("cannot load commit-bound RC2R2 review manifest") from error
    for row in manifest["artifacts"]:
        try:
            blob = subprocess.check_output(["git", "show", f"{commit}:{row['path']}"], cwd=REPO)
        except subprocess.CalledProcessError as error:
            raise ContractError(f"missing commit-bound RC2R2 artifact: {row['path']}") from error
        if len(blob) != row["bytes"] or sha256_bytes(blob) != row["sha256"]:
            raise ContractError(f"commit-bound RC2R2 artifact differs: {row['path']}")
        path = REPO / row["path"]
        if not path.is_file() or path.read_bytes() != blob:
            raise ContractError(f"committed RC2R2 review input changed: {row['path']}")


_BLIND_PACKET_KEYS = {
    "artifact_id", "calibration_response_schema_id", "contains_prior_labels", "items", "purpose",
    "repository_access_should_be_withheld", "schema", "source_byte_manifest_id", "status",
}


def validate_package(package: dict[str, Any]) -> None:
    verify_rc2r2_immutable()
    calibration = package["calibration_manifest"]
    if calibration.get("N") != 56 or len(calibration.get("canonical_ids", [])) != 56:
        raise ContractError("RC2R3 calibration set is not exact N=56")
    if len(set(calibration["canonical_ids"])) != 56:
        raise ContractError("RC2R3 calibration set contains duplicate canonical IDs")
    extra_blind = set(package["blind_packet"]) - _BLIND_PACKET_KEYS
    if extra_blind:
        raise ContractError(f"unexpected blind packet key: {sorted(extra_blind)}")
    distributed_names = tuple(row["artifact_name"] for row in package["distribution_manifest"]["artifacts"])
    leaks = scan_coder_bundle_leaks(package, distributed_names)
    if leaks:
        raise ContractError(f"coder-visible leakage detected: {leaks}")
    distribution = package["distribution_manifest"]
    if distribution.get("distribution_authorized"):
        raise ContractError("RC2R3 distributed coders before independent acceptance")
    raw = {name: json_bytes(package[name]) for name in distributed_names}
    if distribution["content_bundle_sha256"] != coder_bundle_sha256_from_raw(raw, distributed_names):
        raise ContractError("RC2R3 coder bundle hash is stale")
    for row in distribution["artifacts"]:
        actual = raw[row["artifact_name"]]
        if row["bytes"] != len(actual) or row["sha256"] != sha256_bytes(actual):
            raise ContractError(f"RC2R3 distribution artifact is stale: {row['artifact_name']}")
    intake = package["agreement_intake_contract"]
    if intake.get("agreement_minimum") != AGREEMENT_MINIMUM:
        raise ContractError("RC2R3 agreement minimum is not frozen")
    if intake.get("status") != "PREPARED_NOT_DISTRIBUTED" or any(
        slot.get("assignment_status") != "UNASSIGNED" for slot in intake["coder_slots"]
    ):
        raise ContractError("RC2R3 intake escaped prepared-not-distributed gate")
    if package["agreement"].get("agreement_minimum") != AGREEMENT_MINIMUM:
        raise ContractError("RC2R3 agreement contract threshold differs")
    if package["frozen_package_contract"] != build_frozen_package_contract(package):
        raise ContractError("RC2R3 frozen package contract is stale")
    readiness = package["reproduction_readiness"]
    if any(row["method_anchor_eligible"] or row["reproduction_eligible"] for row in readiness["candidates"]):
        raise ContractError("RC2R3 promoted a reproduction anchor")
    if any(row["research_execution_performed"] for row in readiness["candidates"]):
        raise ContractError("research execution was recorded during RC2R3")


def build_report(package: dict[str, Any]) -> dict[str, Any]:
    validate_package(package)
    return {
        "schema": "sf-stage1c-v2-precalibration-contract-report-v5",
        "artifact_id": "SF-STAGE1C-V2-PRECALIBRATION-CONTRACT-REPORT-RC2R3",
        "as_of": "2026-07-24", "status": "AGENTIC_RC2R3_CODER_READY_NOT_DISTRIBUTED",
        "predecessor": {
            "release": "AGENTIC_RC2R2", "commit": "9652d98eade798903be6c5d007591d2602a2f5c3",
            "immutable_verified": True,
        },
        "authority": {
            "runtime_integrity_repair_authorized": True,
            "post_accept_calibration_distribution_authorized": True,
            "coder_distributed": False, "agreement_computed": False,
            "research_model_called": False, "benchmark_metric_run": False,
            "paper_reproduction_run": False, "prototype_created": False,
            "novelty_verdict_made": False, "full_mapping_signed": False,
            "push_authorized": False,
        },
        "bounded_defect_closure": {
            "compiled_frozen_agreement_minimum_0_85": True,
            "receiver_actual_artifact_bytes_hashed": True,
            "receiver_actual_prompt_bytes_hashed": True,
            "typed_structural_path_allowlist": True,
            "structural_alias_attacks_rejected": True,
        },
        "surface": {
            "calibration_N": 56,
            "coder_visible_artifacts": len(CODER_DISTRIBUTION_ALLOWED_ARTIFACTS),
            "agreement_minimum": AGREEMENT_MINIMUM,
            "frozen_contract_sha256": sha256_bytes(json_bytes(package["frozen_package_contract"])),
            "reproduction_anchors": 0,
        },
        "remaining_before_distribution": [
            "CREATE_LOCAL_COMMIT_WITHOUT_PUSH",
            "OBTAIN_ACCEPT_AGENTIC_RC2R3_METHOD_CONTRACT_FOR_CODER_INTAKE",
            "MATERIALIZE_TWO_ISOLATED_RECEIVER_SIDE_ACTUAL_BYTE_RECEIPTS",
        ],
    }


def build_review_manifest(report: dict[str, Any]) -> dict[str, Any]:
    paths = [
        OWNER_AUTHORIZATION, RC2R2_REVIEW, RC2R2_REVIEW_MANIFEST,
        WORKBENCH / "README.md", WORKBENCH / "codebook-v5.md",
        WORKBENCH / "stage1c-v2-precalibration-contract-rc2r3-zh.md",
        REPO / "scripts/survey/sf_stage1c_v2_precalibration_rc2r3.py",
        REPO / "scripts/survey/sf_stage1c_v2_calibration_agreement_v5.py",
        REPO / "scripts/survey/test_sf_stage1c_v2_precalibration_rc2r3.py",
        *ARTIFACT_PATHS.values(), REPORT_PATH, CHECK_DIR / "verification-summary.json",
    ]
    missing = [path for path in paths if not path.is_file()]
    if missing:
        raise ContractError(f"RC2R3 review inputs missing: {missing}")
    return {
        "schema": "sf-stage1c-v2-precalibration-review-manifest-v5",
        "artifact_id": "SF-STAGE1C-V2-PRECALIBRATION-REVIEW-PACKAGE-RC2R3",
        "status": report["status"], "artifact_count": len(paths),
        "predecessor_rc2r2_commit": "9652d98eade798903be6c5d007591d2602a2f5c3",
        "compiled_frozen_contract_sha256": report["surface"]["frozen_contract_sha256"],
        "artifacts": [{
            "path": path.relative_to(REPO).as_posix(),
            "bytes": path.stat().st_size, "sha256": sha256_path(path),
        } for path in paths],
        "requested_review_verdict": "ACCEPT_AGENTIC_RC2R3_METHOD_CONTRACT_FOR_CODER_INTAKE_OR_WITHHOLD_WITH_BOUNDED_DEFECTS",
        "authority_withheld": [
            "AGREEMENT_BEFORE_TWO_RAW_OUTPUTS_FROZEN", "OWNER_ADJUDICATION",
            "SIGN_STAGE1C_V2_EXPERIMENT_MAPPING", "320_PAPER_FULL_MAPPING", "RESEARCH_EXECUTION",
            "SIGN_STAGE1C_V2_FAMILY_BRANCH_PORTFOLIO", "STAGE2A", "PUSH",
        ],
    }


def load_package() -> dict[str, Any]:
    return {name: load_json(path) for name, path in ARTIFACT_PATHS.items()}


def run(*, write: bool) -> dict[str, Any]:
    expected = build_package()
    validate_package(expected)
    report = build_report(expected)
    if write:
        for name, path in ARTIFACT_PATHS.items():
            write_json(path, expected[name])
        write_json(REPORT_PATH, report)
        write_json(REVIEW_MANIFEST_PATH, build_review_manifest(report))
    else:
        actual = load_package()
        validate_package(actual)
        for name in ARTIFACT_PATHS:
            if actual[name] != expected[name]:
                raise ContractError(f"materialized RC2R3 artifact is stale: {ARTIFACT_PATHS[name]}")
        if load_json(REPORT_PATH) != report:
            raise ContractError("RC2R3 contract report is stale")
        if load_json(REVIEW_MANIFEST_PATH) != build_review_manifest(report):
            raise ContractError("RC2R3 review manifest is stale")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    try:
        report = run(write=args.write)
    except (ContractError, OSError, ValueError, ValidationError) as error:
        print(f"FAIL: {error}")
        return 1
    print(json.dumps({"status": report["status"], **report["surface"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
