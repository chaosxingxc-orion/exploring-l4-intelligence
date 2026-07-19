"""Validation helpers for discriminative PDF page-anchor evidence."""

from __future__ import annotations

import re
import unicodedata
from collections import Counter
from collections.abc import Mapping


PAGE_NUMBER_RE = re.compile(r"\bp(?P<page>\d+)\b")
STRONG_PAGE_RE = re.compile(r"\bp(?P<page>\d+)\s+anchor='(?P<anchor>[^']+)'")
EVIDENCE_KINDS = {"canon", "tex", "pdf_page", "absence"}
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
