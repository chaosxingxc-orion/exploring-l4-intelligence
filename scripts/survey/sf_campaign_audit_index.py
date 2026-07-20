#!/usr/bin/env python3
"""Generate and verify the System-first Stage-1A campaign audit index."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path, PurePosixPath


REPO = Path(__file__).resolve().parents[2]
CHECKS_DIR = REPO / "scripts" / "checks"
if str(CHECKS_DIR) not in sys.path:
    sys.path.insert(0, str(CHECKS_DIR))

from ai_context_inventory import (  # noqa: E402
    CAMPAIGN_INDEX_BASELINE_COUNT,
    CAMPAIGN_INDEX_BASELINE_PREFIX_SHA256,
    campaign_index_prefix_sha256,
)


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
    "current_carrier_section",
    "artifacts",
}
ARTIFACT_KEYS = {"path", "git_blob", "type"}
SUPERSESSION_KEYS = {
    "mode",
    "target",
    "target_current_carrier",
    "target_current_carrier_section",
    "transfer_rule",
}
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
    "receipt",
}
HEX40 = re.compile(r"[0-9a-f]{40}\Z")
PRESS_QUERY_REVIEW = "wiki/survey/2026-07-18-sf-press-query-review-c4c.md"
AUDIT_ROOT = "wiki/audit/system-first-stage1a/"
GENERATED_AUDIT_PATHS = {
    f"{AUDIT_ROOT}INDEX.md",
    f"{AUDIT_ROOT}campaign-index.json",
}


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
        or (path.startswith(AUDIT_ROOT) and path not in GENERATED_AUDIT_PATHS)
    )


def semantic_entries(rounds: list[dict]) -> list[dict]:
    """Flatten round semantics so an independent prefix hash can freeze every field."""

    entries = []
    for row in rounds:
        for artifact in row["artifacts"]:
            entries.append(
                {
                    "path": artifact["path"],
                    "git_blob": artifact["git_blob"],
                    "round": row["round"],
                    "type": artifact["type"],
                    "verdict": row["verdict"],
                    "disposition": row["disposition"],
                    "supersession": dict(row["supersession"]),
                    "current_carrier": row["current_carrier"],
                    "current_carrier_section": row["current_carrier_section"],
                }
            )
    return entries


def semantic_prefix_sha256(rounds: list[dict], count: int) -> str:
    return campaign_index_prefix_sha256(semantic_entries(rounds), count)


def _markdown_headings(raw: object, carrier: str) -> set[str]:
    if not isinstance(raw, bytes):
        raise CampaignIndexError(f"carrier {carrier} must be supplied as exact bytes")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as error:
        raise CampaignIndexError(f"carrier {carrier} is not UTF-8: {error}") from error
    headings = set()
    for line in text.splitlines():
        match = re.fullmatch(r"#{1,6}[ \t]+(.+?)(?:[ \t]+#+)?", line)
        if match:
            headings.add(match.group(1).strip())
    return headings


def validate_contract(
    registry: object,
    contract: object,
    carrier_documents: object,
    *,
    baseline_count: int = CAMPAIGN_INDEX_BASELINE_COUNT,
    baseline_prefix_sha256: str = CAMPAIGN_INDEX_BASELINE_PREFIX_SHA256,
) -> None:
    if not isinstance(registry, dict) or "artifacts" not in registry:
        raise CampaignIndexError("registry must be an object containing artifacts")
    contract = _require_keys(contract, ROOT_KEYS, "contract")
    if contract["schema"] != "sf-campaign-audit-index-v2":
        raise CampaignIndexError("unsupported campaign contract schema")
    if contract["campaign"] != "system-first-stage1a":
        raise CampaignIndexError("unexpected campaign id")
    if contract["current_carriers"] != EXPECTED_CARRIERS:
        raise CampaignIndexError("current_carriers must equal the canonical rules/state paths")
    if not isinstance(carrier_documents, dict):
        raise CampaignIndexError("carrier documents must be an exact path/bytes map")
    carrier_headings = {
        path: _markdown_headings(carrier_documents.get(path), path)
        for path in EXPECTED_CARRIERS.values()
    }

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
    rows_by_round: dict[int, dict] = {}
    for raw_row in rounds:
        round_number = raw_row["round"]
        row = _require_keys(raw_row, ROUND_KEYS, f"round {round_number}")
        rows_by_round[round_number] = row
        if row["verdict"] not in ALLOWED_VERDICTS:
            raise CampaignIndexError(f"round {round_number} has invalid verdict")
        if row["disposition"] not in ALLOWED_DISPOSITIONS:
            raise CampaignIndexError(f"round {round_number} has invalid disposition")
        carrier = row["current_carrier"]
        if carrier not in EXPECTED_CARRIERS.values():
            raise CampaignIndexError(f"round {round_number} has invalid current carrier")
        section = row["current_carrier_section"]
        if not isinstance(section, str) or not section.strip():
            raise CampaignIndexError(
                f"round {round_number} current_carrier_section must be nonempty"
            )
        if section not in carrier_headings[carrier]:
            raise CampaignIndexError(
                f"round {round_number} carrier section does not exist: "
                f"{carrier}#{section}"
            )
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

    if rounds[-1]["disposition"] != "ACTIVE_REVIEW_TRANSACTION":
        raise CampaignIndexError("latest round must be the active review transaction")
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
        target_carrier = supersession["target_current_carrier"]
        target_section = supersession["target_current_carrier_section"]
        if supersession["transfer_rule"] != "same-carrier-section":
            raise CampaignIndexError(
                f"round {number} has unsupported carrier-section transfer rule"
            )
        if mode == "later-round-artifact":
            target_round = artifact_round.get(target)
            if target_round is None or target_round <= number:
                raise CampaignIndexError(
                    f"round {number} supersession must target an artifact in a later round"
                )
            target_row = rows_by_round[target_round]
            if (
                target_carrier != target_row["current_carrier"]
                or target_section != target_row["current_carrier_section"]
            ):
                raise CampaignIndexError(
                    f"round {number} later target carrier/section does not match target round"
                )
            if (
                row["current_carrier"] != target_carrier
                or row["current_carrier_section"] != target_section
            ):
                raise CampaignIndexError(
                    f"round {number} same-carrier-section rule does not preserve row carrier"
                )
            if disposition != "SUPERSEDED_BY_LATER_ROUND":
                raise CampaignIndexError(
                    f"round {number} later-round supersession has wrong disposition"
                )
        elif mode == "current-carrier":
            if (
                target != row["current_carrier"]
                or target_carrier != row["current_carrier"]
                or target_section != row["current_carrier_section"]
            ):
                raise CampaignIndexError(
                    f"round {number} current supersession target must equal row carrier+section"
                )
            if disposition == "SUPERSEDED_BY_LATER_ROUND":
                raise CampaignIndexError(
                    f"round {number} later-round disposition lacks a later target"
                )
        else:
            raise CampaignIndexError(f"round {number} has invalid supersession mode")

    entries = semantic_entries(rounds)
    if (
        isinstance(baseline_count, bool)
        or not isinstance(baseline_count, int)
        or baseline_count <= 0
        or baseline_count > len(entries)
    ):
        raise CampaignIndexError(
            f"invalid campaign baseline count: {baseline_count} for {len(entries)} entries"
        )
    if not isinstance(baseline_prefix_sha256, str) or not re.fullmatch(
        r"[0-9a-f]{64}", baseline_prefix_sha256
    ):
        raise CampaignIndexError("invalid campaign baseline prefix SHA-256")
    actual_prefix = campaign_index_prefix_sha256(entries, baseline_count)
    if actual_prefix != baseline_prefix_sha256:
        raise CampaignIndexError(
            "campaign baseline prefix mismatch: "
            f"expected {baseline_prefix_sha256}, found {actual_prefix}"
        )
    baseline_last_round = entries[baseline_count - 1]["round"]
    if any(entry["round"] <= baseline_last_round for entry in entries[baseline_count:]):
        raise CampaignIndexError(
            "campaign baseline may grow only by appending a new round/epoch"
        )


def render_index(contract: dict) -> bytes:
    lines = [
        "# System-first Stage-1A campaign audit index",
        "",
        "This cold audit router is generated from `campaign-index.json`; do not edit it by hand.",
        "Every registered campaign artifact is mapped exactly once to its round, type, verdict,",
        "disposition, supersession target, and exact current surviving-rule/state carrier section.",
        "Presence here does not authorize Stage-1B and does not make a historical artifact active context.",
        "",
        "| Round | Artifact bindings (`type`: `path` @ `git_blob`) | Verdict | Disposition | Supersession | Current carrier | Current carrier section |",
        "|---:|---|---|---|---|---|---|",
    ]
    for row in contract["rounds"]:
        artifacts = "<br>".join(
            f"`{artifact['type']}`: `{artifact['path']}` @ `{artifact['git_blob']}`"
            for artifact in row["artifacts"]
        )
        supersession = row["supersession"]
        supersession_binding = (
            f"`{supersession['mode']}` -> `{supersession['target']}`; "
            f"carrier=`{supersession['target_current_carrier']}`; "
            f"section=`{supersession['target_current_carrier_section']}`; "
            f"rule=`{supersession['transfer_rule']}`"
        )
        lines.append(
            f"| {row['round']} | {artifacts} | `{row['verdict']}` | "
            f"`{row['disposition']}` | {supersession_binding} | "
            f"`{row['current_carrier']}` | `{row['current_carrier_section']}` |"
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
    try:
        carrier_documents = {
            path: REPO.joinpath(*path.split("/")).read_bytes()
            for path in EXPECTED_CARRIERS.values()
        }
    except OSError as error:
        raise CampaignIndexError(f"cannot read current carrier: {error}") from error
    validate_contract(registry, contract, carrier_documents)
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
