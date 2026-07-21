"""Validation helpers for discriminative PDF page-anchor evidence."""

from __future__ import annotations

import re
import unicodedata
from collections import Counter
from collections.abc import Mapping

from sf_row_hash import row_hash


PAGE_NUMBER_RE = re.compile(r"\bp(?P<page>\d+)\b")
STRONG_PAGE_RE = re.compile(r"\bp(?P<page>\d+)\s+anchor='(?P<anchor>[^']+)'")
EVIDENCE_KINDS = {"canon", "tex", "pdf_page", "absence"}
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
ABSENCE_ALLOWED_VALUES = {
    "human_or_dev_label_model_selection": (False,),
    "selection_object": ("none",),
    "explicit_candidate_pool_selection": (False,),
    "inference_external_new_information": (False,),
    "external_component_weight_update": (False,),
    "controller_program_or_config_optimized_on_labels": (False,),
    "decision_rights": ([],),
}
ABSENCE_PROOF_OBLIGATIONS = {
    "human_or_dev_label_model_selection": {
        "proof_obligation_id": "NEG-HUMAN-OR-DEV-LABEL-MODEL-SELECTION",
        "required_inspection_targets": (
            "model/checkpoint selection procedure",
            "development and evaluation protocol",
        ),
        "search_terms_or_tables": (
            "human selection, manual selection, dev set, validation set",
            "checkpoint selection, model selection, best-of-run",
        ),
        "acceptable_explicit_negative_evidence": (
            "explicit fixed-model statement or exhaustive selection procedure "
            "showing no human/dev-label choice",
        ),
        "force_unresolved_if": (
            "selection procedure, appendix, or referenced implementation is "
            "unavailable or ambiguous",
        ),
    },
    "selection_object": {
        "proof_obligation_id": "NEG-SELECTION-OBJECT-NONE",
        "required_inspection_targets": (
            "method algorithm",
            "inference/decoding procedure",
        ),
        "search_terms_or_tables": (
            "candidate, sample, output, trajectory, select, rank, rerank, choose",
        ),
        "acceptable_explicit_negative_evidence": (
            "explicit single-output/direct-return procedure or exhaustive "
            "algorithm showing no candidate-object selection",
        ),
        "force_unresolved_if": (
            "candidate construction or terminal decision procedure is missing "
            "or ambiguous",
        ),
    },
    "explicit_candidate_pool_selection": {
        "proof_obligation_id": "NEG-EXPLICIT-CANDIDATE-POOL-SELECTION",
        "required_inspection_targets": (
            "candidate generation procedure",
            "terminal selection/ranking procedure",
        ),
        "search_terms_or_tables": (
            "best-of-N, sample, beam, pool, rank, rerank, majority, MBR, select",
        ),
        "acceptable_explicit_negative_evidence": (
            "explicit direct-return procedure or exhaustive algorithm showing "
            "no scored/tournament choice among generated candidates",
        ),
        "force_unresolved_if": (
            "multiple candidates may exist but their terminal handling cannot be "
            "resolved",
        ),
    },
    "inference_external_new_information": {
        "proof_obligation_id": "NEG-INFERENCE-EXTERNAL-NEW-INFORMATION",
        "required_inspection_targets": (
            "inference inputs and tool/retrieval interfaces",
            "environment-observation procedure",
        ),
        "search_terms_or_tables": (
            "retrieve, search, browse, tool, database, environment, observation",
        ),
        "acceptable_explicit_negative_evidence": (
            "closed-input inference declaration or exhaustive interface list "
            "showing no external new-information channel",
        ),
        "force_unresolved_if": (
            "tool, retrieval, environment, or referenced runtime behavior is "
            "unavailable or ambiguous",
        ),
    },
    "external_component_weight_update": {
        "proof_obligation_id": "NEG-EXTERNAL-COMPONENT-WEIGHT-UPDATE",
        "required_inspection_targets": (
            "training/setup section for every external component",
            "implementation or checkpoint provenance",
        ),
        "search_terms_or_tables": (
            "train, finetune, update, optimize, learned, checkpoint, frozen",
        ),
        "acceptable_explicit_negative_evidence": (
            "explicit frozen/off-the-shelf declaration covering every external "
            "component or a complete no-external-component architecture",
        ),
        "force_unresolved_if": (
            "any external component has unknown training or checkpoint provenance",
        ),
    },
    "controller_program_or_config_optimized_on_labels": {
        "proof_obligation_id": "NEG-CONTROLLER-OPTIMIZED-ON-LABELS",
        "required_inspection_targets": (
            "controller construction and tuning procedure",
            "development/evaluation protocol",
        ),
        "search_terms_or_tables": (
            "tune, optimize, search, sweep, validation, dev, label, reward",
        ),
        "acceptable_explicit_negative_evidence": (
            "explicit fixed controller/configuration declaration with provenance "
            "or exhaustive construction procedure showing no label optimization",
        ),
        "force_unresolved_if": (
            "controller/configuration selection provenance is unavailable or "
            "ambiguous",
        ),
    },
    "decision_rights": {
        "proof_obligation_id": "NEG-DECISION-RIGHTS-EMPTY",
        "required_inspection_targets": (
            "complete inference/control algorithm",
            "all signal consumers and termination rules",
        ),
        "search_terms_or_tables": (
            "retry, revise, branch, route, stop, select, tool, prompt, memory",
        ),
        "acceptable_explicit_negative_evidence": (
            "explicit observational-only role or exhaustive algorithm showing no "
            "control action owned by the external component",
        ),
        "force_unresolved_if": (
            "a signal exists whose consumer or downstream action is unavailable "
            "or ambiguous",
        ),
    },
}
ROW_REQUIRED_FIELDS = [
    "core_weight_update",
    "external_component_weight_update",
    "controller_program_or_config_optimized_on_labels",
    "human_or_dev_label_model_selection",
    "deployment_label_access",
    "test_item_gold_access",
    "inference_external_new_information",
    "internal_visibility",
    "core_topology",
    "core_native_modality",
    "control_horizon",
    "decision_rights",
    "candidate_pool_exists",
    "selection_policy",
    "selection_object",
    "explicit_candidate_pool_selection",
]
SIGNAL_REQUIRED_FIELDS = ["form", "source", "lifecycle", "uses"]
EDGE_REQUIRED_FIELDS = ["signal_use", "decision_right"]
_MISSING = object()


def normalized_tokens(text):
    """Return Unicode lexical tokens after case-insensitive normalization."""
    folded = unicodedata.normalize("NFKC", text or "").casefold()
    return re.findall(r"[^\W_]+", folded, flags=re.UNICODE)


def normalized_phrase(text):
    """Return normalized lexical tokens joined by one space."""
    return " ".join(normalized_tokens(text))


def _anchor_strength_failure(anchor):
    tokens = normalized_tokens(anchor)
    if len(tokens) < 2 or sum(len(token) for token in tokens) < 12:
        return "page-anchor-too-weak"
    return None


def _page_text(reader, index):
    try:
        return normalized_phrase(reader.pages[index].extract_text())
    except Exception:
        return ""


def _document_text(reader):
    """Return normalized pages and whether every extraction succeeded."""
    document = []
    for index in range(len(reader.pages)):
        try:
            document.append(normalized_phrase(reader.pages[index].extract_text()))
        except Exception:
            return document, False
    return document, True


def _phrase_pattern(needle):
    return re.compile(r"(?:^| )" + re.escape(needle) + r"(?= |$)")


def check_page_locator(locator, reader, pid, what, failures):
    """Append evidence-contract failures for each PDF page locator in *locator*."""
    locator = locator or ""
    strong_locators = {
        match.start(): match for match in STRONG_PAGE_RE.finditer(locator)
    }
    document = None
    document_readable = None

    for page_match in PAGE_NUMBER_RE.finditer(locator):
        if any(
            match.start() < page_match.start() < match.end()
            for match in strong_locators.values()
        ):
            continue
        strong_match = strong_locators.get(page_match.start())
        page_number = int(page_match.group("page"))
        if strong_match is None:
            failures.append(f"{pid}:{what}:page-token-without-anchor:p{page_number}")
            continue

        anchor = strong_match.group("anchor")
        strength_failure = _anchor_strength_failure(anchor)
        if strength_failure is not None:
            failures.append(
                f"{pid}:{what}:{strength_failure}:p{page_number}:{anchor}"
            )
            continue

        if reader is None:
            failures.append(f"{pid}:{what}:pdf-unreadable-for-page-check")
            continue

        page_count = len(reader.pages)
        if not 1 <= page_number <= page_count:
            failures.append(
                f"{pid}:{what}:page-out-of-range:p{page_number}/{page_count}"
            )
            continue

        if document is None:
            document, document_readable = _document_text(reader)
        if not document_readable:
            failures.append(f"{pid}:{what}:pdf-unreadable-for-page-check")
            continue

        needle = normalized_phrase(anchor)
        pattern = _phrase_pattern(needle)
        occurrences = sum(
            sum(1 for _ in pattern.finditer(text)) for text in document
        )
        if occurrences > 3:
            failures.append(
                f"{pid}:{what}:page-anchor-not-discriminative:"
                f"p{page_number}:{anchor}:{occurrences}"
            )
            continue

        window_start = max(0, page_number - 2)
        window_end = min(page_count, page_number + 1)
        window = document[window_start:window_end]
        if not any(pattern.search(text) for text in window):
            failures.append(
                f"{pid}:{what}:page-anchor-missing:p{page_number}:{anchor}"
            )


def values_equal(expected, declared):
    """Compare lists as multisets and all other values normally."""
    if type(expected) is not type(declared):
        return False
    if isinstance(expected, list) and isinstance(declared, list):
        try:
            return Counter((type(item), item) for item in expected) == Counter(
                (type(item), item) for item in declared
            )
        except TypeError:
            return False
    return expected == declared


def _validate_binding(owner, field, expected, evidence, failures):
    """Append failures when a required claim-evidence binding is invalid."""
    field_missing = expected is _MISSING
    if field_missing:
        failures.append(f"{owner}:{field}:encoded-field-missing")
    if not isinstance(evidence, Mapping):
        failures.append(f"{owner}:{field}:evidence-container-invalid")
        return

    entry = evidence.get(field, _MISSING)
    if entry is _MISSING:
        failures.append(f"{owner}:{field}:required-evidence-missing")
        return
    if not isinstance(entry, Mapping):
        failures.append(f"{owner}:{field}:evidence-entry-invalid")
        return
    if entry.get("kind") not in EVIDENCE_KINDS:
        failures.append(f"{owner}:{field}:evidence-kind-invalid")
    if not field_missing and not values_equal(expected, entry.get("value")):
        failures.append(f"{owner}:{field}:evidence-value-mismatch")
    if entry.get("kind") == "absence":
        _validate_absence_entry(owner, field, entry, failures)


def _nonempty_string(value):
    return isinstance(value, str) and bool(value.strip())


def _valid_sha256(value):
    return isinstance(value, str) and SHA256_RE.fullmatch(value) is not None


def _validate_absence_entry(owner, field, entry, failures):
    """Validate local shape and field/value compatibility of one absence."""
    allowed = ABSENCE_ALLOWED_VALUES.get(field, ())
    if not any(values_equal(entry.get("value"), value) for value in allowed):
        failures.append(f"{owner}:{field}:absence-field-value-not-allowed")

    obligation = ABSENCE_PROOF_OBLIGATIONS.get(field)
    expected_obligation = obligation and obligation["proof_obligation_id"]
    if entry.get("proof_obligation_id") != expected_obligation:
        failures.append(f"{owner}:{field}:absence-proof-obligation-mismatch")

    locators = entry.get("inspected_locators")
    if not (
        isinstance(locators, list)
        and locators
        and all(_nonempty_string(locator) for locator in locators)
    ):
        failures.append(f"{owner}:{field}:absence-locators-invalid")

    reason = entry.get("reason")
    weak_phrases = ("not contradicted", "not seen")
    if not _nonempty_string(reason) or any(
        phrase in normalized_phrase(reason) for phrase in weak_phrases
    ):
        failures.append(f"{owner}:{field}:absence-reason-weak")

    fulltext = entry.get("fulltext")
    if not isinstance(fulltext, Mapping):
        failures.append(f"{owner}:{field}:absence-fulltext-invalid")
    else:
        if not _nonempty_string(fulltext.get("id")) or not _nonempty_string(
            fulltext.get("kind")
        ):
            failures.append(f"{owner}:{field}:absence-fulltext-identity-invalid")
        if not _valid_sha256(fulltext.get("sha256")):
            failures.append(f"{owner}:{field}:absence-fulltext-sha256-invalid")

    required_strings = {
        "owner_method_path_id": "absence-owner-row-invalid",
        "owner_sidecar": "absence-owner-sidecar-invalid",
        "coder_identity": "absence-coder-identity-invalid",
        "adjudication_row_id": "absence-adjudication-row-id-invalid",
    }
    for key, failure in required_strings.items():
        if not _nonempty_string(entry.get(key)):
            failures.append(f"{owner}:{field}:{failure}")
    if not _valid_sha256(entry.get("owner_row_sha256")):
        failures.append(f"{owner}:{field}:absence-owner-row-hash-invalid")


def _normalized_path(value):
    return value.replace("\\", "/") if isinstance(value, str) else value


def _fulltext_identity(fulltext):
    if not isinstance(fulltext, Mapping):
        return None
    return {
        "id": fulltext.get("id"),
        "kind": fulltext.get("kind"),
        "sha256": fulltext.get("sha256"),
    }


def _absence_entries(row):
    evidence = row.get("claim_evidence", {})
    if isinstance(evidence, Mapping):
        for field, entry in evidence.items():
            if isinstance(entry, Mapping) and entry.get("kind") == "absence":
                yield "row", field, entry
    signals = row.get("signals", [])
    if isinstance(signals, list):
        for signal in signals:
            if not isinstance(signal, Mapping):
                continue
            evidence = signal.get("claim_evidence", {})
            if isinstance(evidence, Mapping):
                for field, entry in evidence.items():
                    if isinstance(entry, Mapping) and entry.get("kind") == "absence":
                        yield f"signal:{signal.get('signal_id', '?')}", field, entry
    edges = row.get("control_edges", [])
    if isinstance(edges, list):
        for index, edge in enumerate(edges):
            if not isinstance(edge, Mapping):
                continue
            evidence = edge.get("claim_evidence", {})
            if isinstance(evidence, Mapping):
                for field, entry in evidence.items():
                    if isinstance(entry, Mapping) and entry.get("kind") == "absence":
                        yield f"edge:{index}", field, entry


def validate_absence_cross_bindings(row, sidecar_path, sidecar, adjudication):
    """Cross-check absence entries against their owner sidecar and review rows.

    The function verifies bindings. Human nonparticipation remains a named
    ``TEAM_ATTESTATION`` supplied by the review artifact, not a machine proof.
    """
    if not isinstance(row, Mapping):
        return ["?:row:container-invalid"]
    pid = row.get("method_path_id", "?")
    failures = []
    actual_path = _normalized_path(sidecar_path)
    if not isinstance(sidecar, Mapping):
        return [f"{pid}:sidecar:container-invalid"]
    sidecar_fulltext = _fulltext_identity(sidecar.get("fulltext"))
    sidecar_coder = sidecar.get("coder")
    sidecar_rows = sidecar.get("method_paths", [])
    owner_row = next(
        (
            candidate
            for candidate in sidecar_rows
            if isinstance(candidate, Mapping)
            and candidate.get("method_path_id") == pid
        ),
        None,
    ) if isinstance(sidecar_rows, list) else None
    actual_row_hash = row_hash(row)

    adjudication_rows = (
        adjudication.get("rows") if isinstance(adjudication, Mapping) else None
    )
    if not isinstance(adjudication_rows, list):
        adjudication_rows = []

    for owner_kind, field, entry in _absence_entries(row):
        owner = f"{pid}:{owner_kind}"
        if entry.get("owner_method_path_id") != pid:
            failures.append(f"{owner}:{field}:absence-owner-row-mismatch")
        if _normalized_path(entry.get("owner_sidecar")) != actual_path:
            failures.append(f"{owner}:{field}:absence-owner-sidecar-mismatch")
        if entry.get("coder_identity") != sidecar_coder or (
            row.get("coder") is not None
            and entry.get("coder_identity") != row.get("coder")
        ):
            failures.append(f"{owner}:{field}:absence-coder-binding-mismatch")
        if _fulltext_identity(entry.get("fulltext")) != sidecar_fulltext:
            failures.append(f"{owner}:{field}:absence-fulltext-binding-mismatch")
        if owner_row is None or row_hash(owner_row) != actual_row_hash:
            failures.append(f"{owner}:{field}:absence-owner-sidecar-row-mismatch")
        if entry.get("owner_row_sha256") != actual_row_hash:
            failures.append(f"{owner}:{field}:absence-owner-row-hash-mismatch")

        row_id = entry.get("adjudication_row_id")
        review = next(
            (
                candidate
                for candidate in adjudication_rows
                if isinstance(candidate, Mapping)
                and candidate.get("adjudication_row_id") == row_id
            ),
            None,
        )
        if review is None:
            failures.append(f"{owner}:{field}:absence-adjudication-row-missing")
            continue

        expected_review_bindings = {
            "method_path_id": pid,
            "owner_kind": owner_kind,
            "field": field,
            "proof_obligation_id": entry.get("proof_obligation_id"),
            "owner_sidecar": entry.get("owner_sidecar"),
            "fulltext": _fulltext_identity(entry.get("fulltext")),
            "coder_identity": entry.get("coder_identity"),
            "owner_row_sha256": actual_row_hash,
        }
        actual_review_bindings = {
            "method_path_id": review.get("method_path_id"),
            "owner_kind": review.get("owner_kind"),
            "field": review.get("field"),
            "proof_obligation_id": review.get("proof_obligation_id"),
            "owner_sidecar": review.get("owner_sidecar"),
            "fulltext": _fulltext_identity(review.get("fulltext")),
            "coder_identity": review.get("coder_identity"),
            "owner_row_sha256": review.get("owner_row_sha256"),
        }
        if actual_review_bindings != expected_review_bindings:
            failures.append(f"{owner}:{field}:absence-adjudication-binding-mismatch")
        if review.get("verdict") not in {"AGREE", "AGREE_WITH_CAUTION"}:
            failures.append(f"{owner}:{field}:absence-verdict-not-agree")
        if not _nonempty_string(review.get("review_reason")):
            failures.append(f"{owner}:{field}:absence-review-reason-invalid")
        adjudicator = review.get("adjudicator_identity")
        if not _nonempty_string(adjudicator):
            failures.append(f"{owner}:{field}:absence-adjudicator-identity-invalid")
        elif adjudicator == entry.get("coder_identity"):
            failures.append(f"{owner}:{field}:absence-actor-collision")

        independence = review.get("independence")
        attestation_fields = (
            "nonparticipation_scope",
            "conflict_declaration",
            "timestamp",
        )
        if not (
            isinstance(independence, Mapping)
            and independence.get("classification") == "TEAM_ATTESTATION"
            and all(_nonempty_string(independence.get(key)) for key in attestation_fields)
        ):
            failures.append(
                f"{owner}:{field}:absence-independence-attestation-invalid"
            )

    return failures


def validate_bound_values(row):
    """Validate that required row, signal, and edge claims bind their values."""
    if not isinstance(row, Mapping):
        return ["?:row:container-invalid"]

    pid = row.get("method_path_id", "?")
    failures = []

    for field in ROW_REQUIRED_FIELDS:
        _validate_binding(
            f"{pid}:row",
            field,
            row.get(field, _MISSING),
            row.get("claim_evidence"),
            failures,
        )

    signals = row.get("signals", [])
    if not isinstance(signals, list):
        failures.append(f"{pid}:signals:container-invalid")
    else:
        for index, signal in enumerate(signals):
            if not isinstance(signal, Mapping):
                failures.append(f"{pid}:signal:{index}:entry-invalid")
                continue
            sid = signal.get("signal_id", "?")
            for field in SIGNAL_REQUIRED_FIELDS:
                _validate_binding(
                    f"{pid}:signal:{sid}",
                    field,
                    signal.get(field, _MISSING),
                    signal.get("claim_evidence"),
                    failures,
                )

    control_edges = row.get("control_edges", [])
    if not isinstance(control_edges, list):
        failures.append(f"{pid}:control_edges:container-invalid")
    else:
        for index, edge in enumerate(control_edges):
            if not isinstance(edge, Mapping):
                failures.append(f"{pid}:edge:{index}:entry-invalid")
                continue
            for field in EDGE_REQUIRED_FIELDS:
                _validate_binding(
                    f"{pid}:edge:{index}",
                    field,
                    edge.get(field, _MISSING),
                    edge.get("claim_evidence"),
                    failures,
                )

    return failures
