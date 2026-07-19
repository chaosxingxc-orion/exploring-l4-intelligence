#!/usr/bin/env python3
"""Deterministically migrate pinned system-first sidecars to schema v3."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
from collections import Counter
from collections.abc import Mapping
from pathlib import Path

from sf_evidence_contract import (
    EDGE_REQUIRED_FIELDS,
    EVIDENCE_KINDS,
    ROW_REQUIRED_FIELDS,
    SIGNAL_REQUIRED_FIELDS,
    validate_bound_values,
)
from sf_json_contract import JsonContractError, loads as strict_json_loads


ANCHOR_REPLACEMENTS = {
    "p4 probe": "p4 anchor='create extend probe and prune branches'",
    "p5 cost": "p5 anchor='accuracy cost trade off'",
    "p3 Algorithm": "p3 anchor='every decision auditable'",
    "p8 Fig": "p8 anchor='natural stop time aligns with correct majority emergence'",
    "p14 delegated": "p14 anchor='asymmetric delegated architecture'",
    "p4 explore": (
        "p4 anchor='repeatedly decides whether to call explore or to stop and "
        "synthesize'"
    ),
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
BINDING_OVERRIDES = {
    (
        "2026.findings-acl.511#prm-guided-search",
        "row",
        "selection_object",
    ): {
        "value": "trajectory",
        "kind": "pdf_page",
        "page": 15,
        "anchor": "return path with highest reward",
    },
    (
        "2602.16485#calibrated-orchestration",
        "signal:s_profile",
        "source",
    ): {
        "value": "llm_judge",
        "kind": "pdf_page",
        "page": 7,
        "anchor": "each tool agent performs a self audit",
    },
    (
        "2602.16485#calibrated-orchestration",
        "edge:1",
        "signal_use",
    ): {
        "value": "route",
        "kind": "pdf_page",
        "page": 5,
        "anchor": "agents profiles to select only the most compatible tools",
    },
    ("2604.16529#rtv", "row", "selection_object"): {
        "value": "trajectory",
        "kind": "tex",
        "quote": (
            "where each round reduces a population of rollouts into a subset by "
            "dividing the population into groups of size $G$ and selecting a rollout "
            "from each group."
        ),
    },
    (
        "2604.16529#rtv-pdr-pipeline",
        "row",
        "explicit_candidate_pool_selection",
    ): {
        "value": True,
        "kind": "tex",
        "quote": (
            "apply \\textbf{RTV} to obtain a high-quality subset of $K$ summaries;"
        ),
    },
    ("2604.16529#rtv-pdr-pipeline", "row", "selection_object"): {
        "value": "trajectory",
        "kind": "tex",
        "quote": (
            "apply \\textbf{RTV} to the refined rollouts and return the final "
            "top-$1$ rollout."
        ),
    },
    ("2604.16529#rtv-pdr-pipeline", "edge:1", "decision_right"): {
        "value": "supply",
        "kind": "tex",
        "quote": (
            "\\textbf{RTV} is then applied to these summaries to select the top-$K$ "
            "summaries, which define the refinement context for the next iteration."
        ),
    },
    ("2605.08083#discovered-controller", "row", "selection_object"): {
        "value": "trajectory",
        "kind": "canon",
        "quote": (
            "每(model,problem)预采 128 轨迹;selector=controller 终态共识型 Agg"
        ),
    },
    ("2606.01667#agentic-orchestration", "row", "selection_object"): {
        "value": "candidate_output",
        "kind": "pdf_page",
        "page": 3,
        "anchor": "returned candidate ct answer reasoning approach confidence",
    },
    ("2606.01667#agentic-orchestration", "edge:2", "signal_use"): {
        "value": "synthesize_input",
        "kind": "pdf_page",
        "page": 2,
        "anchor": (
            "stop and synthesis decisions both rest on this single stateful in "
            "context view"
        ),
    },
    ("2606.03054#trained-gate", "signal:s_gate", "source"): {
        "value": "trained_classifier",
        "kind": "pdf_page",
        "page": 11,
        "anchor": "logistic regression classifier we train with l2",
    },
}
BINDING_OVERRIDE_PRECONDITIONS = {
    (
        "2026.findings-acl.511#prm-guided-search",
        "row",
        "selection_object",
    ): {
        "value": "trajectory",
        "row_sha256": "3cbe47a4136693202aa49f3433a25de3fb572889bfd4d2972a7d3e09833d8fc5",
    },
    (
        "2602.16485#calibrated-orchestration",
        "signal:s_profile",
        "source",
    ): {
        "value": "llm_judge",
        "row_sha256": "87656952432d5ff2482e1e40702511c1ec6b6bb2f67ba635d22c824121a423f7",
    },
    (
        "2602.16485#calibrated-orchestration",
        "edge:1",
        "signal_use",
    ): {
        "value": "synthesize_input",
        "row_sha256": "f497ba60c76f3b0f57adf7bc33d1a722eb9cce7bf78430788c4b05a2b5101b77",
    },
    ("2604.16529#rtv", "row", "selection_object"): {
        "value": "trajectory",
        "row_sha256": "65517ccbdc2f9d468a714ca00c1b4a1c90f62310f11126b206c09d3fa5456f26",
    },
    (
        "2604.16529#rtv-pdr-pipeline",
        "row",
        "explicit_candidate_pool_selection",
    ): {
        "value": True,
        "row_sha256": "7d5273b10d9818ff79070f562e656d6b41c2e14472b2d2451670d6fe2e7f3dca",
    },
    ("2604.16529#rtv-pdr-pipeline", "row", "selection_object"): {
        "value": "trajectory",
        "row_sha256": "570bcaf75ebbd245a4f4eddb67375cbcac85f62d3056719a83fc922984ef8cbb",
    },
    ("2604.16529#rtv-pdr-pipeline", "edge:1", "decision_right"): {
        "value": "supply",
        "row_sha256": "e83a22e7b6ab080d1aad4a921ec424f406e82cb06a216279c730839efc3c6d1f",
    },
    ("2605.08083#discovered-controller", "row", "selection_object"): {
        "value": "trajectory",
        "row_sha256": "e86de882489434345bff344d8ccb17bbbe4a79aec5a5da02eccc9e9c97b61346",
    },
    ("2606.01667#agentic-orchestration", "row", "selection_object"): {
        "value": "candidate_output",
        "row_sha256": "f1bdd4b46f11f64304434d04d3e2de8a3c49e9c6b9456b6d76368da217b218b3",
    },
    ("2606.01667#agentic-orchestration", "edge:2", "signal_use"): {
        "value": "synthesize_input",
        "row_sha256": "5047cc2d5490a254747f4d1d6e74e5268309197977759c0df685aa0e5b50bd75",
    },
    ("2606.03054#trained-gate", "signal:s_gate", "source"): {
        "value": "trained_classifier",
        "row_sha256": "3c13cb005ac6113d0cc4359280cb6c69d95719d2e97b59d769aeb12f2129680a",
    },
}

_PROFILE_ROUTE_BINDING = {
    "kind": "pdf_page",
    "page": 5,
    "anchor": "agents profiles to select only the most compatible tools",
}
_PIPELINE_SELECT_K_QUOTE = (
    "apply \\textbf{RTV} to obtain a high-quality subset of $K$ summaries;"
)
_PIPELINE_REFINEMENT_QUOTE = (
    "\\textbf{RTV} is then applied to these summaries to select the top-$K$ "
    "summaries, which define the refinement context for the next iteration."
)
_ATLAS_SYNTHESIS_ANCHOR = (
    "stop and synthesis decisions both rest on this single stateful in context view"
)
COUPLED_OVERRIDES = {
    (
        "2602.16485#calibrated-orchestration",
        "edge:1",
        "signal_use",
    ): {
        "bindings": {
            ("signal:s_profile", "uses"): {
                "value": ["route"],
                **_PROFILE_ROUTE_BINDING,
            },
            ("edge:1", "decision_right"): {
                "value": "tool_call",
                **_PROFILE_ROUTE_BINDING,
            },
        },
        "fields": {
            ("edge:1", "source_locator"): (
                "p5 anchor='agents profiles to select only the most compatible tools'"
            ),
            ("edge:1", "edge_semantics"): (
                "capability profiles route the query to compatible tool agents and "
                "thereby control which tool calls are dispatched"
            ),
        },
    },
    (
        "2604.16529#rtv-pdr-pipeline",
        "row",
        "explicit_candidate_pool_selection",
    ): {
        "bindings": {
            ("row", "selection_policy"): {
                "value": "tournament_select",
                "kind": "tex",
                "quote": _PIPELINE_SELECT_K_QUOTE,
            },
        },
        "fields": {
            ("row", "source_locator"): (
                f"tex: '{_PIPELINE_SELECT_K_QUOTE}'"
            ),
        },
    },
    ("2604.16529#rtv-pdr-pipeline", "edge:1", "decision_right"): {
        "bindings": {},
        "fields": {
            ("edge:1", "source_locator"): (
                f"tex: '{_PIPELINE_REFINEMENT_QUOTE}'"
            ),
            ("edge:1", "edge_semantics"): (
                "the selected top-K summaries define the refinement context supplied "
                "to the next iteration"
            ),
        },
    },
    ("2606.01667#agentic-orchestration", "edge:2", "signal_use"): {
        "bindings": {},
        "fields": {
            ("edge:2", "source_locator"): (
                "canon: '直接合成终答' "
                f"(p2 anchor='{_ATLAS_SYNTHESIS_ANCHOR}')"
            ),
        },
    },
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
EXPECTED_EDGES = 18
SUCCESS_LINE = (
    "schema-v3 migration: PASS (8 sidecars, 11 rows, 12 signals; "
    "pending adjudication)"
)

REPO_ROOT = Path(__file__).resolve().parents[2]
SOURCE_DIR = REPO_ROOT / "wiki" / "survey" / "sidecars"
OUTPUT_DIR = (
    REPO_ROOT / "wiki" / "survey" / "current" / "data" / "schema-v3" / "sidecars"
)
EDGE_QUOTE_RE = re.compile(
    r"^\s*(?P<kind>canon|tex):\s*'(?P<quote>[^']+)'", re.DOTALL
)
EDGE_LABEL_RE = re.compile(r"(?<!\S)(?:canon|tex)\s*:")
ANCHOR_QUOTE_RE = re.compile(r"(?<!\S)anchor\s*=\s*'[^']+'", re.DOTALL)


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
    if not isinstance(value, Mapping):
        raise MigrationError(f"{owner}: expected JSON object")
    return value


def _validate_binding_shape(binding, owner):
    """Fail closed unless an evidence binding has its kind-specific structure."""
    if not isinstance(binding, Mapping):
        raise MigrationError(f"{owner}: binding must be a JSON object")
    kind = binding.get("kind")
    if not isinstance(kind, str) or kind not in EVIDENCE_KINDS:
        raise MigrationError(f"{owner}: binding kind {kind!r} is unsupported")
    if kind in {"canon", "tex"}:
        quote = binding.get("quote")
        if not isinstance(quote, str) or not quote.strip():
            raise MigrationError(f"{owner}: {kind} binding quote must be non-empty")
    elif kind == "absence":
        for field in ("scope", "note"):
            value = binding.get(field)
            if not isinstance(value, str) or not value.strip():
                raise MigrationError(
                    f"{owner}: absence binding {field} must be non-empty"
                )
    elif kind == "pdf_page":
        page = binding.get("page")
        anchor = binding.get("anchor")
        if type(page) is not int or page < 1:
            raise MigrationError(
                f"{owner}: pdf_page binding page must be a positive integer"
            )
        if not isinstance(anchor, str) or not anchor.strip():
            raise MigrationError(
                f"{owner}: pdf_page binding anchor must be non-empty"
            )
    return binding


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
    for field in legacy_fields:
        _validate_binding_shape(evidence[field], f"{pid}:row:{field}")

    if pid in POSITIVE_SELECTION_EVIDENCE:
        selection_object_value = row.get("selection_object")
        if (
            not isinstance(selection_object_value, str)
            or not selection_object_value.strip()
            or selection_object_value.strip() == "none"
            or row.get("explicit_candidate_pool_selection") is not True
        ):
            raise MigrationError(
                f"{pid}: POSITIVE_SELECTION_EVIDENCE requires selection_object "
                "other than 'none' and explicit candidate selection"
            )
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
        if (
            row.get("selection_object") != "none"
            or row.get("explicit_candidate_pool_selection") is not False
        ):
            raise MigrationError(
                f"{pid}: NO_EXPLICIT_SELECTION requires selection_object='none' "
                "and no explicit candidate selection"
            )
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
        for field in legacy_fields:
            _validate_binding_shape(
                evidence[field], f"{pid}:signal:{sid}:{field}"
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
    failure = (
        f"{pid}:edge:{index}: cannot extract exactly one complete canon or tex "
        "single-quoted quote from source_locator"
    )
    if not isinstance(locator, str):
        raise MigrationError(failure)
    if len(EDGE_LABEL_RE.findall(locator)) != 1:
        raise MigrationError(failure)
    matches = list(EDGE_QUOTE_RE.finditer(locator))
    if len(matches) != 1 or not matches[0].group("quote").strip():
        raise MigrationError(failure)
    quoted_spans = [*matches, *ANCHOR_QUOTE_RE.finditer(locator)]
    consumed_quotes = {
        position
        for match in quoted_spans
        for position in range(match.start(), match.end())
        if locator[position] == "'"
    }
    all_quotes = {position for position, char in enumerate(locator) if char == "'"}
    if consumed_quotes != all_quotes:
        raise MigrationError(failure)
    return matches[0].group("kind"), matches[0].group("quote")


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


def _resolve_override_owner(row, owner):
    pid = row.get("method_path_id", "?")
    if owner == "row":
        return row
    owner_kind, separator, owner_id = owner.partition(":")
    if not separator or not owner_id:
        raise MigrationError(f"{pid}:{owner}: malformed binding override owner")
    if owner_kind == "signal":
        matches = [
            signal
            for signal in row.get("signals", [])
            if signal.get("signal_id") == owner_id
        ]
        if len(matches) != 1:
            raise MigrationError(
                f"{pid}:{owner}: binding override requires exactly one signal owner"
            )
        return matches[0]
    if owner_kind == "edge" and owner_id.isdigit():
        edges = row.get("control_edges", [])
        index = int(owner_id)
        if 0 <= index < len(edges):
            return edges[index]
    raise MigrationError(f"{pid}:{owner}: binding override owner does not exist")


def _set_override_binding(row, owner, field, binding):
    pid = row.get("method_path_id", "?")
    target = _resolve_override_owner(row, owner)
    if field not in target:
        raise MigrationError(
            f"{pid}:{owner}:{field}: encoded override field is missing"
        )
    evidence = _require_mapping(
        target.get("claim_evidence"), f"{pid}:{owner}:claim_evidence"
    )
    if field not in evidence:
        raise MigrationError(
            f"{pid}:{owner}:{field}: override evidence field is missing"
        )
    replacement = copy.deepcopy(binding)
    _validate_binding_shape(replacement, f"{pid}:{owner}:{field}:override")
    target[field] = copy.deepcopy(replacement["value"])
    evidence[field] = replacement


def _canonical_sha256(value):
    try:
        encoded = json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8")
    except (TypeError, ValueError, UnicodeEncodeError) as error:
        raise MigrationError(
            "override precondition cannot canonically encode the migrated row"
        ) from error
    return hashlib.sha256(encoded).hexdigest()


def _assert_override_precondition(row, key):
    method_path_id, owner, field = key
    precondition = BINDING_OVERRIDE_PRECONDITIONS.get(key)
    if precondition is None:
        raise MigrationError(f"override precondition is missing for {key!r}")
    target = _resolve_override_owner(row, owner)
    if field not in target:
        raise MigrationError(
            f"override precondition drift for {key!r}: encoded field is missing"
        )
    actual_value = target[field]
    expected_value = precondition["value"]
    if type(actual_value) is not type(expected_value) or actual_value != expected_value:
        raise MigrationError(
            f"override precondition value drift for {key!r}: "
            f"expected {expected_value!r}, found {actual_value!r}"
        )
    actual_row_sha256 = _canonical_sha256(row)
    expected_row_sha256 = precondition["row_sha256"]
    if actual_row_sha256 != expected_row_sha256:
        raise MigrationError(
            f"override precondition row drift for {method_path_id!r} before "
            f"{owner}:{field}: expected {expected_row_sha256}, "
            f"found {actual_row_sha256}"
        )


def _apply_binding_overrides(row, used_overrides=None):
    pid = row.get("method_path_id", "?")
    for key, binding in BINDING_OVERRIDES.items():
        method_path_id, owner, field = key
        if method_path_id != pid:
            continue
        if used_overrides is not None and key in used_overrides:
            raise MigrationError(f"binding override used more than once: {key!r}")
        _assert_override_precondition(row, key)
        _set_override_binding(row, owner, field, binding)
        coupled = COUPLED_OVERRIDES.get(key, {})
        for (coupled_owner, coupled_field), coupled_binding in coupled.get(
            "bindings", {}
        ).items():
            _set_override_binding(
                row, coupled_owner, coupled_field, coupled_binding
            )
        for (coupled_owner, coupled_field), coupled_value in coupled.get(
            "fields", {}
        ).items():
            target = _resolve_override_owner(row, coupled_owner)
            if coupled_field not in target:
                raise MigrationError(
                    f"{pid}:{coupled_owner}:{coupled_field}: coupled field is missing"
                )
            target[coupled_field] = copy.deepcopy(coupled_value)
        if used_overrides is not None:
            used_overrides.add(key)


def _validate_binding_override_coverage(used_overrides):
    expected = set(BINDING_OVERRIDES)
    used = set(used_overrides)
    preconditions = set(BINDING_OVERRIDE_PRECONDITIONS)
    unknown_coupled = sorted(set(COUPLED_OVERRIDES) - expected)
    missing_preconditions = sorted(expected - preconditions)
    unexpected_preconditions = sorted(preconditions - expected)
    missing = sorted(expected - used)
    unexpected = sorted(used - expected)
    if (
        unknown_coupled
        or missing_preconditions
        or unexpected_preconditions
        or missing
        or unexpected
    ):
        raise MigrationError(
            "binding overrides must cover every adjudication disagreement exactly once "
            f"(unknown_coupled={unknown_coupled}, "
            f"missing_preconditions={missing_preconditions}, "
            f"unexpected_preconditions={unexpected_preconditions}, "
            f"missing={missing}, unexpected={unexpected})"
        )


def _validate_generated_binding_shapes(row):
    pid = row.get("method_path_id", "?")
    for field in ROW_REQUIRED_FIELDS:
        _validate_binding_shape(row["claim_evidence"][field], f"{pid}:row:{field}")
    for index, signal in enumerate(row["signals"]):
        sid = signal.get("signal_id", index)
        for field in SIGNAL_REQUIRED_FIELDS:
            _validate_binding_shape(
                signal["claim_evidence"][field], f"{pid}:signal:{sid}:{field}"
            )
    for index, edge in enumerate(row["control_edges"]):
        for field in EDGE_REQUIRED_FIELDS:
            _validate_binding_shape(
                edge["claim_evidence"][field], f"{pid}:edge:{index}:{field}"
            )


def migrate_sidecar(source, anchor_counts=None, used_overrides=None):
    """Return one independently migrated sidecar without mutating *source*."""
    source = _require_mapping(source, "sidecar")
    counts = anchor_counts if anchor_counts is not None else Counter()
    migrated = replace_anchors(source, counts)
    migrated["schema"] = SCHEMA_TEXT
    migrated["schema_v3_binding_status"] = SCHEMA_V3_BINDING_STATUS
    migrated.pop("schema_v3_binding_adjudicator", None)
    migrated.pop("schema_v3_adjudicator", None)

    rows = migrated.get("method_paths")
    if not isinstance(rows, list):
        raise MigrationError("sidecar: method_paths must be a JSON array")
    for index, row in enumerate(rows):
        row = _require_mapping(row, f"method_paths:{index}")
        _migrate_row_evidence(row)
        _migrate_signal_evidence(row)
        _migrate_edge_evidence(row)
        _apply_binding_overrides(row, used_overrides)
        _validate_generated_binding_shapes(row)
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


def _load_sidecar(path):
    try:
        return strict_json_loads(path.read_bytes(), str(path))
    except (
        OSError,
        JsonContractError,
    ) as error:
        raise MigrationError(f"cannot read {path}: {error}") from error


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
        sources.append(_load_sidecar(path))

    anchor_counts = Counter()
    used_overrides = set()
    outputs = [
        migrate_sidecar(source, anchor_counts, used_overrides) for source in sources
    ]
    _validate_binding_override_coverage(used_overrides)
    rows = [row for sidecar in outputs for row in sidecar.get("method_paths", [])]
    signals = [signal for row in rows for signal in row.get("signals", [])]
    edges = [edge for row in rows for edge in row.get("control_edges", [])]
    if len(outputs) != EXPECTED_SIDECARS:
        raise MigrationError(f"output sidecar count mismatch: {len(outputs)}")
    if len(rows) != EXPECTED_ROWS:
        raise MigrationError(f"expected {EXPECTED_ROWS} method paths, found {len(rows)}")
    if len(signals) != EXPECTED_SIGNALS:
        raise MigrationError(f"expected {EXPECTED_SIGNALS} signals, found {len(signals)}")
    if len(edges) != EXPECTED_EDGES:
        raise MigrationError(f"expected {EXPECTED_EDGES} control edges, found {len(edges)}")

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


def _render_outputs(outputs):
    rendered = []
    names = []
    for source_path, sidecar in outputs:
        name = source_path.name
        names.append(name)
        try:
            text = (
                json.dumps(sidecar, ensure_ascii=False, indent=1, allow_nan=False)
                + "\n"
            )
            data = text.encode("utf-8")
        except UnicodeEncodeError as error:
            raise MigrationError(
                f"cannot render {name} as strict UTF-8 JSON: invalid Unicode scalar"
            ) from error
        except (TypeError, ValueError) as error:
            raise MigrationError(
                f"cannot render {name} as strict UTF-8 JSON: "
                f"unsupported or non-finite value ({type(error).__name__})"
            ) from error
        rendered.append((name, data))
    duplicates = sorted(name for name, count in Counter(names).items() if count > 1)
    if duplicates:
        raise MigrationError(f"duplicate output sidecar names: {duplicates}")
    return rendered


def _verify_rendered_directory(directory, rendered, label):
    expected_names = {name for name, _ in rendered}
    actual_names = {path.name for path in directory.iterdir()}
    if actual_names != expected_names:
        raise MigrationError(
            f"{label} sidecar names mismatch: expected {sorted(expected_names)}, "
            f"found {sorted(actual_names)}"
        )
    for name, expected_bytes in rendered:
        path = directory / name
        if not path.is_file():
            raise MigrationError(f"{label} entry is not a regular file: {path}")
        actual_bytes = path.read_bytes()
        if actual_bytes != expected_bytes:
            raise MigrationError(f"{label} sidecar bytes mismatch: {path}")


def _remove_transaction_directory(path, parent, prefix):
    if path.parent.resolve() != parent.resolve() or not path.name.startswith(prefix):
        raise MigrationError(f"refusing to remove non-transaction directory: {path}")
    if path.exists():
        shutil.rmtree(path)


def _write_rendered_outputs(rendered, output_dir):
    """Publish a verified set with process-error rollback via directory renames.

    Publication changes the destination with one directory-pointer rename.  If an
    existing destination was first moved aside and that publication rename fails,
    the old directory is renamed back.  This is process-error rollback, not a
    claim of crash-proof durability across power loss or operating-system failure.
    """
    output_dir = Path(output_dir)
    expected_names = {name for name, _ in rendered}
    if output_dir.exists() and not output_dir.is_dir():
        raise MigrationError(f"output destination is not a directory: {output_dir}")
    existing_names = (
        {path.name for path in output_dir.iterdir()}
        if output_dir.exists()
        else set()
    )
    unexpected = sorted(existing_names - expected_names)
    if unexpected:
        raise MigrationError(
            f"unexpected old destination sidecars in {output_dir}: {unexpected}"
        )

    parent = output_dir.parent
    parent.mkdir(parents=True, exist_ok=True)
    staging_prefix = f".{output_dir.name}.staging."
    backup_prefix = f".{output_dir.name}.backup."
    staging_dir = Path(
        tempfile.mkdtemp(prefix=staging_prefix, dir=parent)
    )
    try:
        for name, data in rendered:
            with (staging_dir / name).open("wb") as handle:
                handle.write(data)
                handle.flush()
                os.fsync(handle.fileno())
        _verify_rendered_directory(staging_dir, rendered, "staging")

        if output_dir.exists():
            backup_dir = Path(
                tempfile.mkdtemp(prefix=backup_prefix, dir=parent)
            )
            backup_dir.rmdir()
            os.replace(output_dir, backup_dir)
            try:
                os.replace(staging_dir, output_dir)
            except OSError as publish_error:
                try:
                    os.replace(backup_dir, output_dir)
                except OSError as rollback_error:
                    raise MigrationError(
                        "staged-directory publication and rollback both failed; "
                        f"the prior destination remains at {backup_dir}: "
                        f"publish={publish_error}; rollback={rollback_error}"
                    ) from rollback_error
                raise
            _remove_transaction_directory(backup_dir, parent, backup_prefix)
        else:
            os.replace(staging_dir, output_dir)
    finally:
        _remove_transaction_directory(staging_dir, parent, staging_prefix)


def write_outputs(outputs, output_dir=OUTPUT_DIR):
    """Render deterministic UTF-8 LF JSON and publish one verified directory set."""
    _write_rendered_outputs(_render_outputs(outputs), output_dir)


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
        rendered = _render_outputs(outputs)
        if args.write:
            _write_rendered_outputs(rendered, output_dir)
    except (MigrationError, OSError) as error:
        print(f"schema-v3 migration: ERROR: {error}", file=sys.stderr)
        return 1
    print(SUCCESS_LINE)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
