"""Validation helpers for discriminative PDF page-anchor evidence."""

from __future__ import annotations

import re
import unicodedata
from collections import Counter


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


def check_page_locator(locator, reader, pid, what, failures):
    """Append evidence-contract failures for each PDF page locator in *locator*."""
    locator = locator or ""
    strong_locators = {
        match.start(): match for match in STRONG_PAGE_RE.finditer(locator)
    }

    for page_match in PAGE_NUMBER_RE.finditer(locator):
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

        needle = normalized_phrase(anchor)
        document = [_page_text(reader, index) for index in range(page_count)]
        occurrences = sum(text.count(needle) for text in document)
        if occurrences > 3:
            failures.append(
                f"{pid}:{what}:page-anchor-not-discriminative:"
                f"p{page_number}:{anchor}:{occurrences}"
            )
            continue

        window_start = max(0, page_number - 2)
        window_end = min(page_count, page_number + 1)
        window = document[window_start:window_end]
        if not any(needle in text for text in window):
            failures.append(
                f"{pid}:{what}:page-anchor-missing:p{page_number}:{anchor}"
            )


def values_equal(expected, declared):
    """Compare lists as multisets and all other values normally."""
    if isinstance(expected, list) and isinstance(declared, list):
        return Counter(expected) == Counter(declared)
    return expected == declared
