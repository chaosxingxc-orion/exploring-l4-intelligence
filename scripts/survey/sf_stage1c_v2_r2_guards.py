"""Pure P0/P1 guards for the Stage-1C Agentic calibration R2 contract."""

from __future__ import annotations

from typing import Any, Iterable, Sequence


MANDATORY_POSITIVE_CLASSES = ("dataset_edges", "paper_reproduction_support")


class GuardError(ValueError):
    """Raised when a bounded R2 guard is violated."""


def require_exact_positive_classes(
    mandatory: list[str], evidence: dict[str, list[dict[str, Any]]]
) -> tuple[str, str]:
    if tuple(mandatory) != MANDATORY_POSITIVE_CLASSES:
        raise GuardError("R2 requires the exact mandatory classes in frozen order")
    if any(not evidence.get(name) for name in MANDATORY_POSITIVE_CLASSES):
        raise GuardError("every mandatory class requires source-supported positive evidence")
    return MANDATORY_POSITIVE_CLASSES


def require_paper_local_observability_split(
    response_schema: dict[str, Any], coder_visible_artifacts: Iterable[str],
    local_readiness_artifact: str,
) -> None:
    properties = response_schema["$defs"]["paper_reproduction_support"]["properties"]
    if "local_asset_state" in properties:
        raise GuardError("blind paper reproduction support must not require local state")
    if local_readiness_artifact in set(coder_visible_artifacts):
        raise GuardError("reviewer-only artifact cannot enter the coder-visible bundle")


def object_gate_status(
    left_total: int, right_total: int, critical_statuses: Sequence[str]
) -> str:
    if left_total == 0 and right_total == 0:
        return "NOT_CALIBRATED"
    if critical_statuses and all(status == "PASS" for status in critical_statuses):
        return "PASS"
    return "FAIL"
