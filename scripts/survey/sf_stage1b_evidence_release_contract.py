#!/usr/bin/env python3
"""Validate the bounded speech supplement and Stage-1B v3 evidence release."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


SUPPLEMENT_SCHEMA = "sf-stage1b-speech-direct-prior-supplement-v1"
COVERAGE_SCHEMA = "sf-stage1b-speech-omni-prior-coverage-v1"
SUPPLEMENT_PATH = Path(
    "wiki/survey/current/data/stage1b-speech-direct-prior-supplement-v1.json"
)
CURRENT_SUPPLEMENT_V2_PATH = Path(
    "wiki/survey/current/data/stage1b-speech-direct-prior-supplement-v2.json"
)
COVERAGE_PATH = Path(
    "wiki/survey/current/data/stage1b-speech-omni-prior-coverage-v1.json"
)
REFERENCE_PATH = Path("wiki/survey/current/stage1b-transition-reference-appendix.md")
MAPPING_PATH = Path("wiki/survey/current/tables/stage1b-mapping-release.md")
ELIGIBLE_PATH = Path("wiki/survey/current/tables/stage1c-eligible-inputs.md")
RELEASE_SPEC_PATH = Path(
    "wiki/survey/workbench/system-first-stage1b/2026-07-22-stage1b-release-v3-spec.json"
)

ALLOWED_ROLES = {
    "DIRECT_CONTROL_METHOD",
    "MEASUREMENT_INSTRUMENT",
    "BOUNDARY_COMPARATOR",
}
COVERAGE_ALLOWED_ROLES = {
    *ALLOWED_ROLES,
    "EXCLUDE_WITH_REASON",
    "H5_HELD",
}
SUPPLEMENT_MANDATORY_ROLES = {"DIRECT_CONTROL_METHOD"}
ALLOWED_FAMILIES = {
    "budget_stop_repair",
    "evaluator_reliability",
    "interactive_full_duplex",
}
REQUIRED_PAPER_ROLES = {
    "2509.16971": "DIRECT_CONTROL_METHOD",
    "2606.15141": "DIRECT_CONTROL_METHOD",
    "2607.07985": "MEASUREMENT_INSTRUMENT",
    "2603.13686": "MEASUREMENT_INSTRUMENT",
    "2510.07978": "MEASUREMENT_INSTRUMENT",
    "2605.13841": "MEASUREMENT_INSTRUMENT",
    "2607.16610": "BOUNDARY_COMPARATOR",
    "2603.02206": "DIRECT_CONTROL_METHOD",
    "2603.05413": "DIRECT_CONTROL_METHOD",
}

# The bounded universe is the union of the named manual decisions in the frozen-D0
# rescue, every paper explicitly audited in the local-451 rescue, and the opening
# D2/reviewer-delta direct-prior set.  This is intentionally an identity hard gate,
# not a novelty verdict or an instruction to reproduce every row.
TYPICAL_IDS_BY_ROLE = {
    "DIRECT_CONTROL_METHOD": (
        "2305.13738",
        "2503.16492",
        "2506.23049",
        "2509.16971",
        "2509.21749",
        "2510.02995",
        "2510.06223",
        "2510.11454",
        "2511.02834",
        "2512.16978",
        "2512.23646",
        "2601.20230",
        "2602.10656",
        "2603.02206",
        "2603.05413",
        "2603.21013",
        "2604.09121",
        "2605.28192",
        "2605.28480",
        "2605.29430",
        "2606.07264",
        "2606.15141",
        "2607.11433",
    ),
    "MEASUREMENT_INSTRUMENT": (
        "2502.19759",
        "2507.23159",
        "2508.02013",
        "2510.07978",
        "2510.11098",
        "2512.16250",
        "2601.02391",
        "2602.22897",
        "2603.13686",
        "2604.04847",
        "2604.15037",
        "2604.22821",
        "2605.06897",
        "2605.08762",
        "2605.13841",
        "2605.16909",
        "2605.18758",
        "2606.19595",
        "2607.07985",
    ),
    "BOUNDARY_COMPARATOR": (
        "2305.13040",
        "2404.04066",
        "2408.03047",
        "2410.17196",
        "2501.09645",
        "2505.22053",
        "2507.02755",
        "2507.10859",
        "2507.22898",
        "2508.04361",
        "2509.19676",
        "2511.07392",
        "2511.18405",
        "2601.06235",
        "2602.00675",
        "2603.11545",
        "2603.16411",
        "2603.23625",
        "2603.27706",
        "2604.12647",
        "2605.08480",
        "2605.22012",
        "2606.13049",
        "2606.19341",
        "2606.30294",
        "2607.05511",
        "2607.16610",
    ),
    "EXCLUDE_WITH_REASON": (
        "2401.03945",
        "2410.21620",
        "2509.06502",
        "2510.02044",
        "2511.07397",
        "2601.19952",
        "2603.16086",
        "2604.15710",
        "2605.20755",
        "2606.12902",
        "2606.21453",
    ),
    "H5_HELD": ("2505.17862",),
}
REQUIRED_TYPICAL_PAPER_ROLES = {
    paper_id: role
    for role, paper_ids in TYPICAL_IDS_BY_ROLE.items()
    for paper_id in paper_ids
}
FAMILY_ROLE_REQUIREMENTS = {
    "budget_stop_repair": "DIRECT_CONTROL_METHOD",
    "evaluator_reliability": "MEASUREMENT_INSTRUMENT",
    "interactive_full_duplex": "MEASUREMENT_INSTRUMENT",
}
STRICT_COMPARABLE_FIELDS = {
    "evidence_id",
    "paper_work_id",
    "method_path_id",
    "title",
    "analysis_role",
    "eligible_input_families",
    "bundle_load_bearing",
    "core_topology",
    "core_native_modality",
    "includes_speech_audio",
    "speech_audio_role",
    "internal_visibility",
    "core_weight_update",
    "external_component_weight_update",
    "controller_program_or_config_optimized_on_labels",
    "signals",
    "decision_rights",
    "control_edges",
    "selection_object",
    "terminal_operator",
    "stop_repair_semantics",
    "load_bearing",
    "fulltext_ref",
    "source_locator",
    "limitation",
}
RELEASE_REQUIRED_ROLES = {
    "strict_method_path_coding",
    "speech_prior_coverage",
    "speech_direct_prior_supplement",
    "transition_reference_appendix",
    "mapping_release",
    "eligible_inputs",
}
RELEASE_FORBIDDEN_ROUTER_ROLES = {"hot_state", "current_status", "current_router"}

TOKEN_RE = re.compile(r"DP-\d{4}\.\d{4,5}")
SHA256_RE = re.compile(r"[0-9a-f]{64}")
LOCATOR_RE = re.compile(r"p\d+ anchor='[^']{12,}'")
YEAR_RE = re.compile(r"(?:19|20)\d{2}")


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_coverage(document: Any) -> list[str]:
    failures: list[str] = []
    if not isinstance(document, dict):
        return ["COVERAGE_DOCUMENT_NOT_OBJECT"]
    if document.get("schema") != COVERAGE_SCHEMA:
        failures.append("COVERAGE_SCHEMA_INVALID")
    if document.get("scope") != "BOUNDED_EXISTING_LOCAL_AND_FROZEN_D0_POOL":
        failures.append("COVERAGE_SCOPE_INVALID")

    inventories = document.get("source_inventories")
    if not isinstance(inventories, list) or not inventories:
        return [*failures, "COVERAGE_SOURCE_INVENTORIES_INVALID"]
    inventory_ids: set[str] = set()
    inventory_memberships: dict[str, set[str]] = {}
    routed_source_ids: set[str] = set()
    for position, inventory in enumerate(inventories):
        if not isinstance(inventory, dict):
            failures.append(f"COVERAGE_SOURCE_NOT_OBJECT:{position}")
            continue
        inventory_id = inventory.get("inventory_id")
        if not isinstance(inventory_id, str) or not inventory_id:
            failures.append(f"COVERAGE_SOURCE_ID_INVALID:{position}")
            continue
        if inventory_id in inventory_ids:
            failures.append(f"COVERAGE_SOURCE_ID_DUPLICATE:{inventory_id}")
        inventory_ids.add(inventory_id)
        if not isinstance(inventory.get("source_path"), str) or not inventory["source_path"]:
            failures.append(f"COVERAGE_SOURCE_PATH_MISSING:{inventory_id}")
        sha = inventory.get("source_sha256")
        if not isinstance(sha, str) or SHA256_RE.fullmatch(sha) is None:
            failures.append(f"COVERAGE_SOURCE_SHA_INVALID:{inventory_id}")
        denominator = inventory.get("denominator")
        if not isinstance(denominator, int) or denominator <= 0:
            failures.append(f"COVERAGE_SOURCE_DENOMINATOR_INVALID:{inventory_id}")
        if not isinstance(inventory.get("coverage_claim"), str) or len(
            inventory["coverage_claim"].strip()
        ) < 12:
            failures.append(f"COVERAGE_SOURCE_CLAIM_MISSING:{inventory_id}")
        named = inventory.get("named_candidate_ids")
        if not isinstance(named, list) or not named:
            failures.append(f"COVERAGE_SOURCE_NAMED_IDS_INVALID:{inventory_id}")
            continue
        normalized = [str(paper_id) for paper_id in named]
        if len(normalized) != len(set(normalized)):
            failures.append(f"COVERAGE_SOURCE_NAMED_IDS_DUPLICATE:{inventory_id}")
        inventory_memberships[inventory_id] = set(normalized)
        routed_source_ids.update(normalized)

    rows = document.get("rows")
    if not isinstance(rows, list):
        return [*failures, "COVERAGE_ROWS_NOT_ARRAY"]
    by_id: dict[str, dict[str, Any]] = {}
    row_counts: dict[str, int] = {}
    for position, row in enumerate(rows):
        if not isinstance(row, dict):
            failures.append(f"COVERAGE_ROW_NOT_OBJECT:{position}")
            continue
        paper_id = str(row.get("paper_work_id", f"position-{position}"))
        row_counts[paper_id] = row_counts.get(paper_id, 0) + 1
        if row_counts[paper_id] > 1:
            failures.append(f"COVERAGE_DUPLICATE_PAPER_ID:{paper_id}")
        by_id.setdefault(paper_id, row)
        for field in (
            "paper_work_id",
            "title",
            "analysis_role",
            "source_inventories",
            "depth",
            "supplement_status",
            "reason",
        ):
            if field not in row:
                failures.append(f"COVERAGE_REQUIRED_FIELD_MISSING:{paper_id}:{field}")
        role = row.get("analysis_role")
        if role not in COVERAGE_ALLOWED_ROLES:
            failures.append(f"COVERAGE_ROLE_INVALID:{paper_id}")
        sources = row.get("source_inventories")
        if not isinstance(sources, list) or not sources:
            failures.append(f"COVERAGE_ROW_SOURCES_INVALID:{paper_id}")
            sources = []
        for inventory_id in sources:
            if inventory_id not in inventory_ids:
                failures.append(f"COVERAGE_ROW_SOURCE_UNKNOWN:{paper_id}:{inventory_id}")
            elif paper_id not in inventory_memberships.get(inventory_id, set()):
                failures.append(
                    f"COVERAGE_ROW_SOURCE_MEMBERSHIP_MISMATCH:{paper_id}:{inventory_id}"
                )
        reason = row.get("reason")
        if role in {"EXCLUDE_WITH_REASON", "H5_HELD"} and (
            not isinstance(reason, str) or len(reason.strip()) < 12
        ):
            failures.append(f"COVERAGE_REASON_MISSING:{paper_id}")
        status = row.get("supplement_status")
        if status not in {"INCLUDED", "ROUTED_ONLY", "NOT_APPLICABLE"}:
            failures.append(f"COVERAGE_SUPPLEMENT_STATUS_INVALID:{paper_id}")
        if role in SUPPLEMENT_MANDATORY_ROLES and status != "INCLUDED":
            failures.append(f"COVERAGE_DIRECT_NOT_INCLUDED:{paper_id}")
        if role in {"EXCLUDE_WITH_REASON", "H5_HELD"} and status == "INCLUDED":
            failures.append(f"COVERAGE_EXCLUDED_ROW_INCLUDED:{paper_id}")

    for paper_id, expected_role in REQUIRED_TYPICAL_PAPER_ROLES.items():
        row = by_id.get(paper_id)
        if row is None:
            failures.append(f"COVERAGE_REQUIRED_ID_MISSING:{paper_id}")
        elif row.get("analysis_role") != expected_role:
            failures.append(
                f"COVERAGE_REQUIRED_ROLE_MISMATCH:{paper_id}:{expected_role}"
            )
    for paper_id in sorted(routed_source_ids):
        if row_counts.get(paper_id, 0) == 0:
            failures.append(f"COVERAGE_SOURCE_ID_UNROUTED:{paper_id}")
        elif row_counts[paper_id] > 1:
            failures.append(f"COVERAGE_SOURCE_ID_MULTIPLE_ROUTES:{paper_id}")
    for paper_id in sorted(set(by_id) - routed_source_ids):
        failures.append(f"COVERAGE_ROW_NOT_IN_SOURCE_INVENTORY:{paper_id}")
    return failures


def validate_coverage_supplement_link(coverage: Any, supplement: Any) -> list[str]:
    failures: list[str] = []
    coverage_rows = coverage.get("rows", []) if isinstance(coverage, dict) else []
    supplement_rows = supplement.get("rows", []) if isinstance(supplement, dict) else []
    coverage_by_id = {
        row.get("paper_work_id"): row
        for row in coverage_rows
        if isinstance(row, dict) and isinstance(row.get("paper_work_id"), str)
    }
    supplement_ids = {
        row.get("paper_work_id")
        for row in supplement_rows
        if isinstance(row, dict) and isinstance(row.get("paper_work_id"), str)
    }
    required_ids = {
        paper_id
        for paper_id, row in coverage_by_id.items()
        if row.get("analysis_role") in SUPPLEMENT_MANDATORY_ROLES
        or row.get("supplement_status") == "INCLUDED"
    }
    for paper_id in sorted(required_ids - supplement_ids):
        failures.append(f"COVERAGE_SUPPLEMENT_ROW_MISSING:{paper_id}")
    for paper_id in sorted(supplement_ids - set(coverage_by_id)):
        failures.append(f"SUPPLEMENT_COVERAGE_ROW_MISSING:{paper_id}")
    for paper_id in sorted(supplement_ids & set(coverage_by_id)):
        if coverage_by_id[paper_id].get("analysis_role") in {
            "EXCLUDE_WITH_REASON",
            "H5_HELD",
        }:
            failures.append(f"SUPPLEMENT_COVERAGE_ROLE_FORBIDDEN:{paper_id}")
    return failures


def validate_supplement(document: Any) -> list[str]:
    failures: list[str] = []
    if not isinstance(document, dict):
        return ["SUPPLEMENT_DOCUMENT_NOT_OBJECT"]
    if document.get("schema") != SUPPLEMENT_SCHEMA:
        failures.append("SUPPLEMENT_SCHEMA_INVALID")
    if document.get("scope") != "BOUNDED_NON_H5_STAGE1C_INPUT_SUPPORT":
        failures.append("SUPPLEMENT_SCOPE_INVALID")
    if document.get("occupancy_rule") != (
        "ONLY_DIRECT_CONTROL_METHOD_ROWS_ENTER_METHOD_OCCUPANCY"
    ):
        failures.append("SUPPLEMENT_OCCUPANCY_RULE_INVALID")

    rows = document.get("rows")
    if not isinstance(rows, list):
        return [*failures, "SUPPLEMENT_ROWS_NOT_ARRAY"]
    by_id: dict[str, dict[str, Any]] = {}
    evidence_ids: set[str] = set()
    for position, row in enumerate(rows):
        if not isinstance(row, dict):
            failures.append(f"SUPPLEMENT_ROW_NOT_OBJECT:{position}")
            continue
        paper_id = str(row.get("paper_work_id", f"position-{position}"))
        if paper_id in by_id:
            failures.append(f"SUPPLEMENT_DUPLICATE_PAPER_ID:{paper_id}")
        by_id[paper_id] = row
        missing = sorted(STRICT_COMPARABLE_FIELDS - set(row))
        failures.extend(
            f"SUPPLEMENT_REQUIRED_FIELD_MISSING:{paper_id}:{field}"
            for field in missing
        )
        if missing:
            continue

        evidence_id = row["evidence_id"]
        if evidence_id != f"DP-{paper_id}":
            failures.append(f"SUPPLEMENT_EVIDENCE_ID_INVALID:{paper_id}")
        if evidence_id in evidence_ids:
            failures.append(f"SUPPLEMENT_DUPLICATE_EVIDENCE_ID:{evidence_id}")
        evidence_ids.add(evidence_id)

        role = row["analysis_role"]
        if role not in ALLOWED_ROLES:
            failures.append(f"SUPPLEMENT_ROLE_INVALID:{paper_id}")
        families = row["eligible_input_families"]
        if not isinstance(families, list) or not families:
            failures.append(f"SUPPLEMENT_FAMILIES_INVALID:{paper_id}")
            families = []
        for family in families:
            if family not in ALLOWED_FAMILIES:
                failures.append(f"SUPPLEMENT_FAMILY_INVALID:{paper_id}:{family}")
        if row["bundle_load_bearing"] is not True:
            failures.append(f"SUPPLEMENT_BUNDLE_NOT_LOAD_BEARING:{paper_id}")
        if row["includes_speech_audio"] is not True:
            failures.append(f"SUPPLEMENT_NOT_SPEECH_AUDIO_RELEVANT:{paper_id}")

        method_load_bearing = row["load_bearing"]
        if role == "DIRECT_CONTROL_METHOD":
            if method_load_bearing is not True:
                failures.append(f"SUPPLEMENT_DIRECT_METHOD_NOT_LOAD_BEARING:{paper_id}")
            if not row["decision_rights"] or not row["control_edges"]:
                failures.append(f"SUPPLEMENT_DIRECT_METHOD_EDGE_MISSING:{paper_id}")
        elif method_load_bearing is not False:
            failures.append(f"SUPPLEMENT_NON_METHOD_LOAD_BEARING:{paper_id}")

        fulltext = row["fulltext_ref"]
        if not isinstance(fulltext, dict):
            failures.append(f"SUPPLEMENT_FULLTEXT_REF_INVALID:{paper_id}")
        else:
            if fulltext.get("id") != paper_id:
                failures.append(f"SUPPLEMENT_FULLTEXT_ID_MISMATCH:{paper_id}")
            sha = fulltext.get("sha256")
            if not isinstance(sha, str) or SHA256_RE.fullmatch(sha) is None:
                failures.append(f"SUPPLEMENT_FULLTEXT_SHA_INVALID:{paper_id}")
            if not isinstance(fulltext.get("ledger"), str) or not fulltext["ledger"]:
                failures.append(f"SUPPLEMENT_FULLTEXT_LEDGER_MISSING:{paper_id}")
        locator = row["source_locator"]
        if not isinstance(locator, str) or LOCATOR_RE.fullmatch(locator) is None:
            failures.append(f"SUPPLEMENT_SOURCE_LOCATOR_INVALID:{paper_id}")

    for paper_id, expected_role in REQUIRED_PAPER_ROLES.items():
        row = by_id.get(paper_id)
        if row is None:
            failures.append(f"SUPPLEMENT_REQUIRED_ID_MISSING:{paper_id}")
        elif row.get("analysis_role") != expected_role:
            failures.append(
                f"SUPPLEMENT_REQUIRED_ROLE_MISMATCH:{paper_id}:{expected_role}"
            )

    for family, required_role in FAMILY_ROLE_REQUIREMENTS.items():
        if not any(
            row.get("analysis_role") == required_role
            and family in row.get("eligible_input_families", [])
            for row in by_id.values()
        ):
            failures.append(f"SUPPLEMENT_FAMILY_ROLE_MISSING:{family}:{required_role}")
    return failures


def validate_reference_appendix(text: str, document: Any) -> list[str]:
    failures: list[str] = []
    rows = document.get("rows", []) if isinstance(document, dict) else []
    lines = text.splitlines()
    for row in rows:
        evidence_id = row.get("evidence_id")
        paper_id = row.get("paper_work_id")
        matches = [line for line in lines if f"| {evidence_id} |" in line]
        if len(matches) != 1:
            failures.append(f"REFERENCE_ROW_COUNT:{evidence_id}:{len(matches)}")
            continue
        line = matches[0]
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        author_year = cells[2] if len(cells) > 2 else ""
        if "unknown" in author_year.casefold() or YEAR_RE.search(author_year) is None:
            failures.append(f"REFERENCE_AUTHOR_YEAR_MISSING:{evidence_id}")
        stable = f"https://arxiv.org/abs/{paper_id}"
        if stable not in line:
            failures.append(f"REFERENCE_STABLE_LINK_MISSING:{evidence_id}")
        if row.get("source_locator") not in line:
            failures.append(f"REFERENCE_LOCATOR_MISSING:{evidence_id}")
    return failures


def validate_reference_tokens(texts: list[str], document: Any) -> list[str]:
    failures: list[str] = []
    resolved = {
        row.get("evidence_id")
        for row in document.get("rows", [])
        if isinstance(row, dict)
    } if isinstance(document, dict) else set()
    observed = set()
    for text in texts:
        observed.update(TOKEN_RE.findall(text))
    for token in sorted(observed - resolved):
        failures.append(f"REFERENCE_TOKEN_UNRESOLVED:{token}")
    for token in sorted(resolved - observed):
        failures.append(f"REFERENCE_TOKEN_UNUSED:{token}")
    return failures


def validate_release_spec(spec: Any) -> list[str]:
    failures: list[str] = []
    if not isinstance(spec, dict):
        return ["RELEASE_SPEC_NOT_OBJECT"]
    if spec.get("release_id") != "system-first-stage1b-2026-07-22-v3":
        failures.append("RELEASE_ID_INVALID")
    if spec.get("scientific_release_scope") != (
        "EXCLUDES_MUTABLE_HOT_AND_STATUS_ROUTERS"
    ):
        failures.append("RELEASE_SCIENTIFIC_SCOPE_INVALID")
    artifacts = spec.get("artifacts")
    if not isinstance(artifacts, list):
        return [*failures, "RELEASE_ARTIFACTS_NOT_ARRAY"]
    roles: list[str] = []
    for position, row in enumerate(artifacts):
        if not isinstance(row, dict) or not isinstance(row.get("role"), str):
            failures.append(f"RELEASE_ARTIFACT_ROLE_INVALID:{position}")
            continue
        roles.append(row["role"])
    if len(roles) != len(set(roles)):
        failures.append("RELEASE_DUPLICATE_ROLE")
    for role in sorted(RELEASE_REQUIRED_ROLES - set(roles)):
        failures.append(f"RELEASE_REQUIRED_ROLE_MISSING:{role}")
    for role in sorted(RELEASE_FORBIDDEN_ROUTER_ROLES & set(roles)):
        failures.append(f"RELEASE_MUTABLE_ROUTER_INCLUDED:{role}")
    return failures


def validate_repository(repo: Path) -> list[str]:
    repo = Path(repo)
    paths = [
        COVERAGE_PATH,
        SUPPLEMENT_PATH,
        REFERENCE_PATH,
        MAPPING_PATH,
        ELIGIBLE_PATH,
        RELEASE_SPEC_PATH,
    ]
    failures: list[str] = []
    for relative in paths:
        if not repo.joinpath(relative).is_file():
            failures.append(f"REPOSITORY_ARTIFACT_MISSING:{relative.as_posix()}")
    if failures:
        return failures
    try:
        coverage = _load_json(repo / COVERAGE_PATH)
        supplement = _load_json(repo / SUPPLEMENT_PATH)
        release_spec = _load_json(repo / RELEASE_SPEC_PATH)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        return [f"REPOSITORY_JSON_INVALID:{error}"]
    references = (repo / REFERENCE_PATH).read_text(encoding="utf-8")
    mapping = (repo / MAPPING_PATH).read_text(encoding="utf-8")
    eligible = (repo / ELIGIBLE_PATH).read_text(encoding="utf-8")
    failures.extend(validate_coverage(coverage))
    failures.extend(validate_supplement(supplement))
    failures.extend(validate_coverage_supplement_link(coverage, supplement))
    failures.extend(validate_reference_appendix(references, supplement))
    token_document = supplement
    if repo.joinpath(CURRENT_SUPPLEMENT_V2_PATH).is_file():
        try:
            token_document = _load_json(repo / CURRENT_SUPPLEMENT_V2_PATH)
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
            failures.append(f"REPOSITORY_JSON_INVALID:{error}")
    failures.extend(validate_reference_tokens([mapping, eligible], token_document))
    failures.extend(validate_release_spec(release_spec))
    return failures


def main() -> int:
    repo = Path(__file__).resolve().parents[2]
    failures = validate_repository(repo)
    for failure in failures:
        print(f"[STAGE1B-EVIDENCE] {failure}")
    print(f"Stage-1B evidence release contract: {'FAIL' if failures else 'PASS'}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
