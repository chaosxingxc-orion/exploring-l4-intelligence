#!/usr/bin/env python3
"""Structured, offline contract oracle for the effective survey protocol.

The query compiler intentionally treats most byte-preserved §4 prose as cold
history.  This oracle therefore validates exact normalized clauses only in the
effective sections outside §4.  It is stdlib-only, performs no network access,
and never writes repository files.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
CURRENT_PROTOCOL = REPO_ROOT / "wiki" / "survey" / "current" / "protocol.md"


@dataclass(frozen=True)
class Contract:
    name: str
    section: str
    clause: str


@dataclass(frozen=True)
class OrderedContract:
    name: str
    section: str
    clauses: tuple[str, ...]


def normalize_clause(text: str) -> str:
    """Remove presentation-only Markdown and normalize wrapping and case."""
    return " ".join(text.casefold().replace("*", "").replace("`", "").split())


CONTRACTS = (
    Contract(
        "stage1b-scoped-mapping-authorization",
        "§0",
        "frozen discovery queries, T1 routes, identity/deduplication, REC-0 screening, citation "
        "traversal, non-H5 method-path coding, "
        "D2 full-text work, and ordinary mapping synthesis are authorized;",
    ),
    Contract(
        "stage1b-no-model-dataset-or-prototype",
        "§0",
        "Stage-1B means systematic-mapping execution. Stage-1B runs no research model or smoke and, "
        "more explicitly, no research-model call, model smoke, dataset inference/metric experiment, "
        "headroom test, or directional prototype may run anywhere in this stage.",
    ),
    Contract(
        "incremental-boundaries-and-append-only",
        "§3",
        "Date coverage is incremental and replayable. First execution searches through the execution "
        "date. Before synthesis freeze, scan from the first-execution date through the freeze date. "
        "If Stage-1A spans more than one period, cross-period incremental batches are append-only and "
        "carry their own dates and source provenance; old decisions change only by dated supersession.",
    ),
    Contract(
        "section4-normative-input-fence",
        "§3",
        "Only the frozen compiler profile's ordered lane declarations and backtick query literal "
        "declarations in §4 are normative compiler input. The canonical compiled result is exactly "
        "the current frozen JSONL's 65 ordered records and their record_sha256 values; compiler output "
        "is append-prefix stable, and raw byte equality, not semantic JSON equality, is the release "
        "condition.",
    ),
    Contract(
        "section4-narrative-is-non-normative",
        "§3",
        "All other byte-preserved §4 narrative is NON-NORMATIVE historical annotation, including old "
        "55/61/other counts, dated JSONL canonical claims, amendment/batch labels, and Decision-Log "
        "references. It does not override §§0–3 or §§5–10, create an external dependency, or require "
        "opening a legacy file. The interpretation fence and §§0–3 and §§5–10 have priority over "
        "non-normative §4 narrative.",
    ),
    Contract(
        "mapping-exit-e1-complete-decisions",
        "§5",
        "E1: all frozen queries and registered routes are complete and every hit has a REC-0 decision;",
    ),
    Contract(
        "mapping-exit-e2-two-round-count",
        "§5",
        "E2: backward references extracted from archived e-print plus date-stamped forward citation "
        "snapshots produce zero new INCLUDED works for K=2 consecutive closure rounds; and",
    ),
    Contract(
        "mapping-exit-e3-zero-unresolved",
        "§5",
        "E3: every registered sentinel and supplied counterexample has a disposition and zero "
        "UNRESOLVED items remain.",
    ),
    Contract(
        "e2-resolution-counts-and-preregistration",
        "§5",
        "E2 identifier resolution is an OPEN precondition until its report closes. Before any E2 claim, "
        "resolve every entry by DOI, ACL ID, OpenReview ID, or normalized title. The report gives the "
        "four work-level counts total / resolved / ambiguous / unresolved, includes a DOI-only mutation "
        "fixture, and freezes a pre-registered unresolved ceiling before resolution results are inspected.",
    ),
    Contract(
        "e2-k2-is-not-closure",
        "§5",
        "K=2 zero growth on the resolved subgraph is not closure exhaustion and cannot be described as "
        "closure dryness or a complete citation graph.",
    ),
    Contract(
        "information-boundary",
        "§6",
        "The information boundary is absolute: test-item gold may not enter prompt, retrieval, candidate "
        "construction, selector, reward, verifier, tool routing, memory, or stopping. read-out uses "
        "information already supplied to the frozen core; new-info injects answer-bearing information "
        "and is excluded from strict identity.",
    ),
    Contract(
        "native-speech-audio-omni-set",
        "§6",
        "Topology policy A admits single_core and single_core_multi_call. Native speech is represented "
        "by audio_native; the native speech/audio/omni set is therefore {audio_native, omni_native}.",
    ),
    Contract(
        "frozen-derivation-formulas",
        "§6",
        "data_access_strict_bits = seven_strict_bits_all_false AND internal_visibility == api_only "
        "is_s0_core_compatible = data_access_strict_bits AND core_topology IN "
        "{single_core, single_core_multi_call} AND core_native_modality IN "
        "{audio_native, omni_native} is_reward_guided = EXISTS qualifying_reward_signal(s) "
        "is_rq_sys_control_compatible = control_horizon == sequential AND EXISTS valid LIVE edge e "
        "driven by the same qualifying reward signal s AND e.signal_use IN s.reward_uses "
        "is_project_method_candidate = is_s0_core_compatible AND is_rq_sys_control_compatible "
        "reward_guided_selection = candidate_pool_exists == true AND selection_policy IN "
        "{scored_select, tournament_select} AND selection_object != none AND EXISTS qualifying reward "
        "signal s used for select or prune",
    ),
    Contract(
        "offline-calibration-exclusion",
        "§6",
        "The canonical policy label is tournament_select; “tournament” is only a noncanonical shorthand. "
        "offline_calibration signals never qualify for is_reward_guided, RQ-SYS control, or "
        "reward-guided selection.",
    ),
    Contract(
        "direct-threat-dual-coding",
        "§6",
        "DIRECT_THREAT requires threat_dual_coding, two distinct extractors, and a resolvable rec5_ref; "
        "disagreements > 0 requires a nonempty adjudicator. A missing actor, duplicate extractor, "
        "missing REC-5 link, or unresolved disagreement fails before the row can support a claim.",
    ),
    Contract(
        "strong-pdf-anchor-machine-limits",
        "§7",
        "anchor_lexical_tokens >= 2 anchor_alphanumeric_characters >= 12 "
        "anchor_page_window = N-1..N+1 complete_pdf_occurrences <= 3",
    ),
    Contract(
        "reviewer-facing-reference-contract",
        "§9",
        "Every reviewer-facing artifact has a self-contained reference appendix with author, year, and "
        "stable link. Numeric claims require a page, table, or figure locator. A non-contiguous "
        "quotation is explicitly marked as stitched rather than presented as one continuous span. "
        "Consistent, dominant, or ceiling claims are limited to the model, task, and setting reported "
        "by the paper; evidence from one reported setting cannot silently become a universal statement.",
    ),
    Contract(
        "third-correction-and-fourth-amendment-lifecycle",
        "§10",
        "Consolidation is mandatory when a third correction would otherwise accumulate on one effective "
        "document; that third item is frozen as audit evidence and its surviving rule is folded into "
        "the effective file immediately. A fourth amendment is forbidden before consolidation.",
    ),
)


ORDERED_CONTRACTS = (
    OrderedContract(
        "stage1b-execution-sequence",
        "§8",
        (
            "When and only when §0's three authorizations are present, Stage-1B proceeds in this order:",
            "1. record the execution commit, frozen protocol/query hashes, current registries, platform, "
            "actor, and exposure declaration;",
            "2. run the first-step interface and phrase-behavior checks without a research model;",
            "3. execute each frozen query with pagination and deterministic overflow splitting, "
            "logging every page;",
            "4. scan registered T1 routes and resolve candidates without discarding duplicate provenance;",
            "5. create REC-0 rows, screen BFS, then run the triggered DFS and citation-closure procedure "
            "in §5;",
            "6. fetch and register PDF + e-print for included, core, sentinel, or claim-bearing work—FETCH "
            "is registered immediately and an unregistered fetch does not count as read;",
            "7. create per-paper sidecars during coding—the locator is recorded during coding, never "
            "appended after interpretation; a row without a locator does not enter an occupancy denominator;",
            "8. generate coding, reconcile evidence, complete independent adjudication, and only then "
            "derive tables;",
            "9. rerun E1/E2/E3, release binding, immutability, context, and dual-platform gates before "
            "synthesis.",
        ),
    ),
)


def _extract_numbered_sections(text: str) -> tuple[dict[str, str], list[str]]:
    # A numbered section ends at *any* following H2, including §4bis and
    # Appendix headings.  Otherwise §10 could incorrectly borrow a required
    # clause moved into a cold appendix at EOF.
    headings = list(
        re.finditer(r"^##(?:[ \t]+[^\r\n]*)?$", text, flags=re.MULTILINE)
    )
    sections: dict[str, str] = {}
    errors: list[str] = []
    for index, heading in enumerate(headings):
        numbered = re.fullmatch(
            r"##[ \t]+(§(?:10|[0-9]))(?:[ \t]+[^\r\n]*)?",
            heading.group(0),
        )
        if numbered is None:
            continue
        section_id = numbered.group(1)
        end = headings[index + 1].start() if index + 1 < len(headings) else len(text)
        if section_id in sections:
            errors.append(f"duplicate-section:{section_id}")
            continue
        sections[section_id] = text[heading.start():end]
    expected = {f"§{number}" for number in range(11)}
    for section_id in sorted(expected - sections.keys()):
        errors.append(f"missing-section:{section_id}")
    return sections, errors


def validate_protocol_contracts(text: str) -> list[str]:
    """Return stable failure codes; an empty list means all contracts hold."""
    sections, errors = _extract_numbered_sections(text)
    normalized = {
        section_id: normalize_clause(section_text)
        for section_id, section_text in sections.items()
        if section_id != "§4"
    }
    for contract in CONTRACTS:
        haystack = normalized.get(contract.section, "")
        needle = normalize_clause(contract.clause)
        # Exact lexical boundaries matter: the contract "<= 3" must not be
        # satisfied by "<= 30", nor may a longer identifier satisfy a frozen
        # enum member.  Punctuation inside the clause remains literal.
        pattern = rf"(?<![\w]){re.escape(needle)}(?![\w])"
        if not re.search(pattern, haystack):
            errors.append(f"missing-contract:{contract.name}:{contract.section}")
    for contract in ORDERED_CONTRACTS:
        haystack = normalized.get(contract.section, "")
        cursor = 0
        ordered = True
        for clause in contract.clauses:
            needle = normalize_clause(clause)
            pattern = rf"(?<![\w]){re.escape(needle)}(?![\w])"
            match = re.search(pattern, haystack[cursor:])
            if match is None:
                ordered = False
                break
            cursor += match.end()
        if not ordered:
            errors.append(f"ordered-contract:{contract.name}:{contract.section}")
        if contract.name == "stage1b-execution-sequence":
            observed_indices = [
                int(match.group(1))
                for match in re.finditer(
                    r"^(\d+)\.[ \t]",
                    sections.get(contract.section, ""),
                    flags=re.MULTILINE,
                )
            ]
            failure = f"ordered-contract:{contract.name}:{contract.section}"
            if observed_indices != list(range(1, 10)) and failure not in errors:
                errors.append(failure)
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--protocol", type=Path, default=CURRENT_PROTOCOL)
    parser.add_argument("--check", action="store_true", help="validate without writing")
    args = parser.parse_args(argv)
    try:
        text = args.protocol.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        print(f"[sf_protocol_contract] READ FAIL: {args.protocol}: {exc}", file=sys.stderr)
        return 1
    failures = validate_protocol_contracts(text)
    if failures:
        for failure in failures:
            print(f"[sf_protocol_contract] FAIL: {failure}", file=sys.stderr)
        return 1
    print(
        f"[sf_protocol_contract] PASS ({len(CONTRACTS)} exact normalized + "
        f"{len(ORDERED_CONTRACTS)} ordered contracts)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
