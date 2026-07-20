#!/usr/bin/env python3
"""Generate and verify the System-first Stage-1A campaign audit index."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path, PurePosixPath


REPO = Path(__file__).resolve().parents[2]
REGISTRY_PATH = REPO / "wiki" / "survey" / "sf-audit-artifact-registry.json"
CONTRACT_PATH = REPO / "wiki" / "audit" / "system-first-stage1a" / "campaign-index.json"
OUTPUT_PATH = REPO / "wiki" / "audit" / "system-first-stage1a" / "INDEX.md"

ROOT_KEYS = {"schema", "campaign", "current_carriers", "rounds"}
ROUND_KEYS = {
    "round",
    "verdict",
    "disposition",
    "supersession",
    "current_carrier",
    "artifacts",
}
ARTIFACT_KEYS = {"path", "git_blob", "type"}
SUPERSESSION_KEYS = {"mode", "target"}
EXPECTED_CARRIERS = {
    "rules": "wiki/survey/current/protocol.md",
    "state": "wiki/survey/current/status.md",
}
ALLOWED_VERDICTS = {
    "STAGE1A_PROTOCOLIZATION_ONLY",
    "WITHHOLD_STAGE1B",
    "WITHHOLD_STAGE1B_NARROW_REMEDIATION",
    "PENDING_INDEPENDENT_REREVIEW",
}
ALLOWED_DISPOSITIONS = {
    "HISTORICAL_COLD",
    "SUPERSEDED_BY_LATER_ROUND",
    "ACTIVE_REVIEW_TRANSACTION",
}
ALLOWED_TYPES = {
    "proposal",
    "review",
    "response",
    "application",
    "query-review",
    "correction",
}
HEX40 = re.compile(r"[0-9a-f]{40}\Z")
PRESS_QUERY_REVIEW = "wiki/survey/2026-07-18-sf-press-query-review-c4c.md"


class CampaignIndexError(RuntimeError):
    """The campaign contract, registry, or generated index is inconsistent."""


def _require_keys(value: object, expected: set[str], label: str) -> dict:
    if not isinstance(value, dict) or set(value) != expected:
        actual = sorted(value) if isinstance(value, dict) else type(value).__name__
        raise CampaignIndexError(
            f"{label} keys must be exactly {sorted(expected)}; found {actual}"
        )
    return value


def _canonical_path(value: object, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise CampaignIndexError(f"{label} must be a nonempty path")
    pure = PurePosixPath(value)
    if (
        "\\" in value
        or pure.is_absolute()
        or value != pure.as_posix()
        or any(part in ("", ".", "..") for part in pure.parts)
    ):
        raise CampaignIndexError(f"{label} is not a canonical repository path: {value!r}")
    return value


def is_campaign_artifact(path: str) -> bool:
    """Return whether one registered path belongs to this campaign."""

    name = PurePosixPath(path).name
    return (
        path == PRESS_QUERY_REVIEW
        or "system-first-research-proposal-" in name
        or "gate-s1-" in name
        or (
            path.startswith("wiki/audit/system-first-stage1a/round-")
            and path.endswith(".md")
        )
    )


def validate_contract(registry: object, contract: object) -> None:
    if not isinstance(registry, dict) or "artifacts" not in registry:
        raise CampaignIndexError("registry must be an object containing artifacts")
    contract = _require_keys(contract, ROOT_KEYS, "contract")
    if contract["schema"] != "sf-campaign-audit-index-v1":
        raise CampaignIndexError("unsupported campaign contract schema")
    if contract["campaign"] != "system-first-stage1a":
        raise CampaignIndexError("unexpected campaign id")
    if contract["current_carriers"] != EXPECTED_CARRIERS:
        raise CampaignIndexError("current_carriers must equal the canonical rules/state paths")

    registry_rows = registry["artifacts"]
    if not isinstance(registry_rows, list):
        raise CampaignIndexError("registry artifacts must be an array")
    registry_campaign: dict[str, str] = {}
    for index, row in enumerate(registry_rows):
        row = _require_keys(row, {"path", "git_blob"}, f"registry artifact {index}")
        path = _canonical_path(row["path"], f"registry artifact {index} path")
        pin = row["git_blob"]
        if not isinstance(pin, str) or not HEX40.fullmatch(pin):
            raise CampaignIndexError(f"registry artifact {path} has invalid git blob")
        if is_campaign_artifact(path):
            if path in registry_campaign:
                raise CampaignIndexError(f"duplicate campaign path in registry: {path}")
            registry_campaign[path] = pin

    rounds = contract["rounds"]
    if not isinstance(rounds, list) or not rounds:
        raise CampaignIndexError("contract rounds must be a nonempty array")
    round_numbers = [
        row.get("round") if isinstance(row, dict) else None for row in rounds
    ]
    expected_rounds = list(range(1, len(rounds) + 1))
    if round_numbers != expected_rounds:
        raise CampaignIndexError(
            f"round coverage must be unique, ordered, and contiguous: "
            f"expected {expected_rounds}, found {round_numbers}"
        )

    contract_campaign: dict[str, tuple[str, int]] = {}
    artifact_round: dict[str, int] = {}
    for row in rounds:
        round_number = row["round"]
        row = _require_keys(row, ROUND_KEYS, f"round {round_number}")
        if row["verdict"] not in ALLOWED_VERDICTS:
            raise CampaignIndexError(f"round {round_number} has invalid verdict")
        if row["disposition"] not in ALLOWED_DISPOSITIONS:
            raise CampaignIndexError(f"round {round_number} has invalid disposition")
        if row["current_carrier"] not in EXPECTED_CARRIERS.values():
            raise CampaignIndexError(f"round {round_number} has invalid current carrier")
        artifacts = row["artifacts"]
        if not isinstance(artifacts, list) or not artifacts:
            raise CampaignIndexError(f"round {round_number} must contain artifacts")
        for artifact_index, artifact in enumerate(artifacts):
            artifact = _require_keys(
                artifact,
                ARTIFACT_KEYS,
                f"round {round_number} artifact {artifact_index}",
            )
            path = _canonical_path(
                artifact["path"], f"round {round_number} artifact path"
            )
            pin = artifact["git_blob"]
            if not isinstance(pin, str) or not HEX40.fullmatch(pin):
                raise CampaignIndexError(f"round {round_number} artifact has invalid blob")
            if artifact["type"] not in ALLOWED_TYPES:
                raise CampaignIndexError(f"round {round_number} artifact has invalid type")
            if not is_campaign_artifact(path):
                raise CampaignIndexError(f"non-campaign artifact appears in contract: {path}")
            if path in contract_campaign:
                raise CampaignIndexError(f"duplicate campaign path in contract: {path}")
            contract_campaign[path] = (pin, round_number)
            artifact_round[path] = round_number

    if set(registry_campaign) != set(contract_campaign):
        missing = sorted(set(registry_campaign) - set(contract_campaign))
        extra = sorted(set(contract_campaign) - set(registry_campaign))
        raise CampaignIndexError(
            f"registry/contract campaign paths differ; missing={missing}, extra={extra}"
        )
    for path, registry_pin in registry_campaign.items():
        contract_pin = contract_campaign[path][0]
        if contract_pin != registry_pin:
            raise CampaignIndexError(
                f"campaign blob pin mismatch for {path}: "
                f"registry={registry_pin}, contract={contract_pin}"
            )

    last_round = len(rounds)
    for row in rounds:
        number = row["round"]
        disposition = row["disposition"]
        supersession = _require_keys(
            row["supersession"], SUPERSESSION_KEYS, f"round {number} supersession"
        )
        mode = supersession["mode"]
        target = _canonical_path(
            supersession["target"], f"round {number} supersession target"
        )
        if number == last_round and disposition != "ACTIVE_REVIEW_TRANSACTION":
            raise CampaignIndexError("latest round must be the active review transaction")
        if number < last_round and disposition == "ACTIVE_REVIEW_TRANSACTION":
            raise CampaignIndexError("only the latest round may be active")
        if mode == "later-round-artifact":
            target_round = artifact_round.get(target)
            if target_round is None or target_round <= number:
                raise CampaignIndexError(
                    f"round {number} supersession must target an artifact in a later round"
                )
            if disposition != "SUPERSEDED_BY_LATER_ROUND":
                raise CampaignIndexError(
                    f"round {number} later-round supersession has wrong disposition"
                )
        elif mode == "current-carrier":
            if target not in EXPECTED_CARRIERS.values():
                raise CampaignIndexError(
                    f"round {number} supersession must target a current carrier"
                )
            if disposition == "SUPERSEDED_BY_LATER_ROUND":
                raise CampaignIndexError(
                    f"round {number} later-round disposition lacks a later target"
                )
        else:
            raise CampaignIndexError(f"round {number} has invalid supersession mode")


def render_index(contract: dict) -> bytes:
    lines = [
        "# System-first Stage-1A campaign audit index",
        "",
        "This cold audit router is generated from `campaign-index.json`; do not edit it by hand.",
        "Every registered campaign artifact is mapped exactly once to its round, type, verdict,",
        "disposition, supersession target, and current surviving-rule/state carrier. Presence here",
        "does not authorize Stage-1B and does not make a historical artifact active context.",
        "",
        "| Round | Artifact bindings (`type`: `path` @ `git_blob`) | Verdict | Disposition | Supersession | Current carrier |",
        "|---:|---|---|---|---|---|",
    ]
    for row in contract["rounds"]:
        artifacts = "<br>".join(
            f"`{artifact['type']}`: `{artifact['path']}` @ `{artifact['git_blob']}`"
            for artifact in row["artifacts"]
        )
        supersession = row["supersession"]
        lines.append(
            f"| {row['round']} | {artifacts} | `{row['verdict']}` | "
            f"`{row['disposition']}` | `{supersession['mode']}` → "
            f"`{supersession['target']}` | `{row['current_carrier']}` |"
        )
    lines.extend(
        [
            "",
            "## Routing and authority",
            "",
            "- Effective survey rules: `wiki/survey/current/protocol.md`.",
            "- Current review and execution state: `wiki/survey/current/status.md`.",
            "- Registered artifacts remain immutable at their exact registry paths and Git blobs.",
            "- A later correction appends a new registry row and contract round, then regenerates this index.",
            "- Search-design sign-off belongs to an independent reviewer; Stage-1B authorization belongs separately to the owner. This index supplies neither.",
            "",
        ]
    )
    return "\n".join(lines).encode("utf-8")


def _load_json(path: Path) -> dict:
    try:
        value = json.loads(path.read_bytes())
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise CampaignIndexError(f"cannot read {path}: {error}") from error
    if not isinstance(value, dict):
        raise CampaignIndexError(f"{path} must contain a JSON object")
    return value


def check_repository(*, write: bool) -> None:
    registry = _load_json(REGISTRY_PATH)
    contract = _load_json(CONTRACT_PATH)
    validate_contract(registry, contract)
    expected = render_index(contract)
    if write:
        OUTPUT_PATH.write_bytes(expected)
        return
    try:
        actual = OUTPUT_PATH.read_bytes()
    except OSError as error:
        raise CampaignIndexError(f"cannot read generated index: {error}") from error
    if actual != expected:
        raise CampaignIndexError(
            "campaign INDEX is stale; stage source changes and run "
            "sf_campaign_audit_index.py --write"
        )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    arguments = parser.parse_args()
    try:
        check_repository(write=arguments.write)
    except CampaignIndexError as error:
        print(f"campaign audit index: FAIL ({error})", file=sys.stderr)
        return 1
    print("campaign audit index: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
