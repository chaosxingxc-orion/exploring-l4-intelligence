#!/usr/bin/env python3
"""Regression contract for the effective protocol and offline query compiler.

This suite deliberately contains a human-auditable amendment coverage matrix.
Appendix A is routing-only: every matrix assertion is scoped to the target
normative section, so an appendix disposition row can never satisfy coverage.
"""

from __future__ import annotations

import contextlib
import io
import os
import re
import stat
import subprocess
import sys
import tempfile
import unittest
from dataclasses import dataclass
from pathlib import Path
from unittest import mock


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))

import sf_query_compiler as compiler  # noqa: E402
from sf_archive_candidates import (  # noqa: E402
    ARCHIVE_TRANSITIONS,
    resolve_transition_read_paths,
)


LEGACY_PROTOCOL = REPO / "wiki/survey/2026-07-15-system-first-survey-protocol-v1.md"
CURRENT_PROTOCOL = REPO / "wiki/survey/current/protocol.md"
FROZEN_QUERIES = REPO / "wiki/survey/2026-07-15-sf-queries.jsonl"

EXPECTED_FRONTMATTER = (
    "---\n"
    "protocol_id: SF-SYSTEM-FIRST-STAGE1B\n"
    "protocol_version: 3\n"
    "effective_date: 2026-07-21\n"
    "stage: Stage-1B systematic mapping\n"
    "execution_authorized: true\n"
    "authorization_commit: c01fba751b56588ed2f62cb6d01f6c25f3e95539\n"
    "h5_load_bearing_use: WITHHOLD\n"
    "supersedes_effective_chain: protocol-v1 plus amendments 1 and 3-15\n"
    "audit_index: wiki/audit/system-first-stage1a/INDEX.md\n"
    "---\n"
).encode("utf-8")

AMENDMENT_NUMBERS = (1, *range(3, 16))
_TRANSITION_READ_PATHS = resolve_transition_read_paths(REPO, ARCHIVE_TRANSITIONS)
_ARCHIVED_AMENDMENT_PATHS = {
    int(re.search(r"amendment-(\d+)\.md$", path).group(1)): REPO / path
    for path in _TRANSITION_READ_PATHS
}

AMENDMENT_PATHS = {
    1: REPO / "wiki/survey/2026-07-15-sf-protocol-amendment-1.md",
    3: REPO / "wiki/survey/2026-07-16-sf-protocol-amendment-3.md",
    4: REPO / "wiki/survey/2026-07-16-sf-protocol-amendment-4.md",
    5: REPO / "wiki/survey/2026-07-16-sf-protocol-amendment-5.md",
    6: REPO / "wiki/survey/2026-07-17-sf-protocol-amendment-6.md",
    7: REPO / "wiki/survey/2026-07-17-sf-protocol-amendment-7.md",
    8: REPO / "wiki/survey/2026-07-18-sf-protocol-amendment-8.md",
    **_ARCHIVED_AMENDMENT_PATHS,
}


@dataclass(frozen=True)
class CoverageItem:
    amendment: int
    source_locator: str
    target_section: str
    required_phrases: tuple[str, ...]


# Surviving normative topics, not historical verdict prose.  Keep locators
# precise enough for a reviewer to jump back to the cold artifact.  Later
# amendments override earlier values; the required phrase records the final
# effective form (for example schema-v3's 16/4/2 binding surface).
AMENDMENT_COVERAGE = (
    # Amendment 1 file (also contains the historical amendment-2 append).
    CoverageItem(1, "A1-1", "§3", ("category mapping", "cs.CV", "cs.RO", "eess.AS")),
    CoverageItem(1, "A1-2", "§4", ("2026-07-15-sf-queries.jsonl", "65")),
    CoverageItem(1, "A1-3", "§3", ("raw responses", "external uncertainty")),
    CoverageItem(1, "A1-4", "§3", ("totalResults", "year → month → day", "no silent truncation")),
    CoverageItem(1, "A1-6", "§3", ("foundational lineage", "recent novelty pool")),
    CoverageItem(1, "A1-8", "§5", ("threat queue", "not a hard cap", "discovery provenance")),
    CoverageItem(1, "A1-9", "§6", ("most_threatened_rq", "none requires a reason")),
    CoverageItem(1, "A2-1", "§3", ("arXiv-primary", "free official source rescue", "REMOVED_PAYWALLED_UNOBTAINABLE")),
    CoverageItem(1, "A2-4", "§1", ("how to build omni agentic system", "speech", "element")),
    CoverageItem(1, "A2-5", "§5", ("BFS", "triggered DFS", "T-d")),
    CoverageItem(1, "A2-6", "§6", ("method_gist", "improvement_space", "borrowable")),
    CoverageItem(1, "A2-7", "§3", ("T1 proceedings", "50 routes")),
    CoverageItem(1, "A2-9", "§5", ("full text", "claim-bearing")),
    CoverageItem(1, "A2-11", "§5", ("COMMON_NODE", "visited-set", "forward-comparison")),

    # Amendment 3.
    CoverageItem(3, "A3-1", "§3", ("arXiv-primary systematic mapping", "removal counts")),
    CoverageItem(3, "A3-2", "§6", ("venue_tier", "zero evidence weight", "study_quality")),
    CoverageItem(3, "A3-3", "§3", ("route_id", "wordlist")),
    CoverageItem(3, "A3-4", "§8", ("REC-0", "REC-7")),
    CoverageItem(3, "A3-5", "§6", ("source_axes", "omni_axes", "rl_identity", "evidence_axes")),
    CoverageItem(3, "A3-6", "§3", ("API_LIMIT_SINGLE_DAY_OVER_2000", "parent_query_sha256")),
    CoverageItem(3, "A3-10", "§10", ("object-and-anchor-qualified", "internal convergence is not sign-off")),
    CoverageItem(
        3,
        "A3-11",
        "§0",
        ("Stage-1B systematic-mapping execution", "Stage-1A performs identity, routing"),
    ),
    CoverageItem(3, "A3-12", "§10", ("LATE_RECONSTRUCTED_REVIEW_SUMMARY",)),

    # Amendment 4.
    CoverageItem(4, "C4-2", "§6", ("publication_status", "seven dimensions", "claim_evidence_match")),
    CoverageItem(4, "C4-4", "§5", ("one REC-0 row per canonical work", "dedup provenance")),
    CoverageItem(4, "C4-5", "§8", ("ROOT → YEAR → MONTH → DAY", "checkpoint resume", "at least 3 seconds")),
    CoverageItem(4, "C4-6", "§3", ("SF-L10", "cs.SE", "cs.HC")),
    CoverageItem(4, "ID_DEREFERENCE", "§3", ("ID_DEREFERENCE", "not a discovery query", "MISMATCH")),
    CoverageItem(4, "编码深度纪律", "§6", ("D0", "D1", "D2", "code-on-use")),

    # Amendment 5.
    CoverageItem(5, "P0-R1", "§9", ("machine-derived", "missing evidence fails")),
    CoverageItem(5, "P0-R2", "§8", ("parent_from_frozen_row", "record_sha256", "query_sha256")),
    CoverageItem(5, "P0-R3", "§6", ("INCLUDED REC-0 ↔ REC-2", "DIRECT_THREAT", "flow counts")),
    CoverageItem(5, "V13", "§6", ("threat_dual_coding", "rec5_ref", "two distinct extractors", "disagreements > 0")),
    CoverageItem(5, "P0-R5", "§3", ("SF-L11", "cs.MM", "cs.MA", "held-out")),
    CoverageItem(5, "P0-R6", "§8", ("discovery_queries_executed", "id_dereference_accesses", "access class")),
    CoverageItem(5, "P0-R8", "§9", ("completion claims", "persistent evidence")),

    # Amendment 6.
    CoverageItem(6, "P0-1", "§9", ("producer replay", "byte-identical", "fail closed")),
    CoverageItem(6, "P0-2", "§6", ("one-to-one", "orphan", "typed NA")),
    CoverageItem(6, "P0-3", "§3", ("SF-L12", "SF-L13", "vocabulary drift")),
    CoverageItem(6, "P0-4", "§7", ("raw Atom", "REGISTERED_BOUNDARY", "held-out")),
    CoverageItem(6, "访问类注册", "§8", ("PROVENANCE_FETCH", "FULLTEXT_FETCH", "HELD_OUT_SENTINEL_SOURCING")),
    CoverageItem(6, "agent-era", "§5", ("2025+", "priority", "not study_quality")),

    # Amendment 7.
    CoverageItem(7, "E1", "§5", ("E1", "all frozen queries", "REC-0")),
    CoverageItem(7, "E2", "§5", ("E2", "K=2", "backward", "forward")),
    CoverageItem(7, "E3", "§5", ("E3", "UNRESOLVED")),
    CoverageItem(7, "引用交集", "§5", ("NO_CORE_CITATION_OVERLAP", "cannot be the discovery entrance")),
    CoverageItem(7, "全文强制细则", "§8", ("PDF + e-print", "FETCH is registered immediately")),
    CoverageItem(7, "vocabulary-drift", "§3", ("three examples on the same axis", "controlled lane evaluation")),

    # Amendment 8.
    CoverageItem(8, "SF-L14/SF-L15", "§4", ("SF-L14", "SF-L15", "13")),
    CoverageItem(8, "PRESS", "§10", ("independent query review", "term freeze", "sign-off application")),
    CoverageItem(8, "fresh L12 held-out", "§3", ("pre-registered held-out", "used in query design")),
    CoverageItem(8, "债务表", "§10", ("owner", "deadline gate", "OPEN")),
    CoverageItem(8, "D-1", "§5", ("DOI", "ACL", "OpenReview", "total", "resolved", "ambiguous", "unresolved")),
    CoverageItem(8, "可回放性矩阵", "§8", ("bundle-only", "local-data", "network-dependent")),

    # Amendment 9.
    CoverageItem(9, "阶段正典", "§0", ("Stage-1B", "no research-model", "model smoke")),
    CoverageItem(9, "exposure", "§8", ("current_activity_stage", "new_model_touches_since_gate_freeze", "INHERITED_PRIOR_EXPOSURE")),
    CoverageItem(9, "claim-evidence", "§9", ("MACHINE_RECOMPUTED_LOCAL", "SOURCE_REPORTED_TRACEABLE", "TEAM_ATTESTATION")),
    CoverageItem(9, "system-control", "§6", ("13-axis", "decision rights", "information boundary")),
    CoverageItem(9, "known-item", "§5", ("REVIEWER_KNOWN_ITEM", "carry-forward ledger")),
    CoverageItem(9, "Stage-2A", "§0", ("Stage-2A reproduction-first", "no present execution force")),
    CoverageItem(9, "双向证据", "§9", ("supporting evidence", "contradicting evidence", "kill criterion")),
    CoverageItem(9, "引用自包含", "§9", ("author", "year", "stable link", "page, table, or figure", "non-contiguous quotation")),

    # Amendment 10.
    CoverageItem(10, "exposure union v2", "§8", ("four-repository scoped", "held-out", "exposure")),
    CoverageItem(10, "identity taxonomy", "§6", ("method path", "mixed-path")),
    CoverageItem(10, "量词扫描", "§9", ("prose lint", "denominator", "analysis unit")),
    CoverageItem(10, "Stage-1B 首批", "§5", ("taxonomy before prioritization", "does not alter the frozen queries")),
    CoverageItem(10, "owner 重申", "§0", ("Stage-1B runs no research model or smoke",)),

    # Amendment 11.
    CoverageItem(11, "正典投影", "§6", ("canonical projection", "REC-2", "control edges")),
    CoverageItem(11, "分析单位", "§6", ("selection_object", "never aggregate across pool types")),
    CoverageItem(11, "独立语义反例", "§7", ("non-implementer", "append-only fixture")),
    CoverageItem(11, "三张开局保证表", "§9", ("method paths", "measurement instruments", "negative-result priors")),
    CoverageItem(11, "附录角色", "§9", ("DEEPLY_READ", "BOUNDARY_COMPARATOR")),

    # Amendment 12.
    CoverageItem(12, "taxonomy v3", "§2", ("same frozen core", "strict-topology sensitivity", "terminal selector")),
    CoverageItem(12, "三分派生", "§6", ("is_s0_core_compatible =", "is_rq_sys_control_compatible =", "is_project_method_candidate =")),
    CoverageItem(12, "coding v4", "§6", ("random-K", "no selection signal", "component_path_ids")),
    CoverageItem(12, "lineage 最小实现", "§7", ("paper_work_id", "fulltext_ref", "canonical_record_id")),
    CoverageItem(12, "单写原则", "§7", ("per-paper sidecar", "generated", "coder ≠ semantic_adjudicator")),
    CoverageItem(12, "locator 前置", "§8", ("locator is recorded during coding", "not enter an occupancy denominator")),

    # Amendment 13.
    CoverageItem(13, "审计层", "§10", ("audit registry", "immutable from first commit", "dated supersession")),
    CoverageItem(13, "control_edges", "§6", ("signal_use", "decision_right", "allowed relation")),
    CoverageItem(13, "sidecar 单写链", "§7", ("single handwritten layer", "byte-identical", "reconciliation")),
    CoverageItem(13, "actor 纪律", "§7", ("stable actor ID", "adjudicated_agree", "conflict queue")),
    CoverageItem(13, "oracle 等强", "§10", ("oracle-strength audit", "demonstrated failing input")),

    # Amendment 14, superseded where Plan A strengthens 14 fields to 16/4/2.
    CoverageItem(14, "信号实例身份", "§6", ("signals[].signal_id", "same signal", "reward_uses")),
    CoverageItem(14, "required-evidence", "§7", ("16 row-level", "4 signal-level", "2 edge-level")),
    CoverageItem(14, "locator 真解析", "§7", ("pN anchor='multi-word phrase'", "N-1 through N+1")),
    CoverageItem(14, "裁决行哈希", "§7", ("adjudication row hash", "any load-bearing change invalidates")),
    CoverageItem(14, "跨环境", "§8", ("Windows", "WSL2 Ubuntu-24.04", "same occupancy")),
    CoverageItem(14, "敏感面突变", "§7", ("derived-formula sensitive surface", "clean stamped baseline")),

    # Amendment 15 plus the schema-v3 repair that supersedes its narrower contract.
    CoverageItem(15, "validator", "§6", ("edge-use-not-in-signal", "right-not-declared", "relation-not-allowed")),
    CoverageItem(15, "signal 证据", "§7", ("form", "source", "lifecycle", "uses")),
    CoverageItem(15, "pdf_page", "§7", ("pdf_page", "page-anchor-not-discriminative")),
    CoverageItem(15, "release binding", "§9", ("generated_headline_begin", "re-render", "whole-block")),
    CoverageItem(15, "carry-forward", "§9", ("carry-forward", "trained reward instrument")),
    CoverageItem(15, "双平台", "§8", ("two platform-stamped reports", "both PASS")),
)


def _extract_h2_block(raw: bytes, heading_prefix: bytes) -> bytes:
    """Return one LF-only H2 block, stopping at the next H2."""
    if b"\r" in raw:
        raise AssertionError("protocol bytes must use LF, not CRLF")
    pattern = re.compile(
        rb"^## " + re.escape(heading_prefix) + rb"[^\n]*\n.*?(?=^## |\Z)",
        flags=re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(raw)
    if not match:
        raise AssertionError(f"missing H2 block: {heading_prefix!r}")
    return match.group(0)


def _section_text(protocol_text: str, section_id: str) -> str:
    match = re.search(
        rf"^## {re.escape(section_id)}\b.*?(?=^## |\Z)",
        protocol_text,
        flags=re.MULTILINE | re.DOTALL,
    )
    if not match:
        raise AssertionError(f"missing section {section_id}")
    return match.group(0)


def _normalize_prose(text: str) -> str:
    """Normalize presentation-only case and Markdown line wrapping."""
    return " ".join(text.casefold().replace("*", "").replace("`", "").split())


def _compile(path: Path) -> tuple[list[dict], bytes]:
    text = compiler.load_protocol_text(path)
    base, additions, lane_additions, _ = compiler.parse_all_queries(text)
    records = (
        compiler.compile_records(base)
        + compiler.compile_records(additions)
        + compiler.compile_records(lane_additions)
    )
    return records, compiler.render_records(records)


class ProtocolStructureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.raw = CURRENT_PROTOCOL.read_bytes()
        cls.text = cls.raw.decode("utf-8")

    def test_exact_frontmatter_and_fixed_section_map(self) -> None:
        self.assertTrue(self.raw.startswith(EXPECTED_FRONTMATTER))
        headings = re.findall(r"^## (.+)$", self.text, flags=re.MULTILINE)
        section_ids = [heading.split(maxsplit=1)[0] for heading in headings]
        self.assertEqual(section_ids, [*(f"§{n}" for n in range(11)), "Appendix"])
        self.assertIn("Appendix A", headings[-1])

    def test_section_4_is_exact_raw_lf_copy_to_next_h2(self) -> None:
        legacy = _extract_h2_block(LEGACY_PROTOCOL.read_bytes(), "§4".encode("utf-8"))
        current = _extract_h2_block(self.raw, "§4".encode("utf-8"))
        self.assertEqual(current, legacy)
        self.assertNotIn("## §4bis".encode("utf-8"), current)

    def test_appendix_has_exactly_the_14_explicit_dispositions(self) -> None:
        appendix = _section_text(self.text, "Appendix")
        rows = re.findall(r"^\|\s*Amendment\s+(\d+)\s*\|", appendix, flags=re.MULTILINE)
        self.assertEqual(tuple(map(int, rows)), AMENDMENT_NUMBERS)
        for row in appendix.splitlines():
            if re.match(r"^\|\s*Amendment\s+\d+\s*\|", row):
                self.assertIn("legacy", row.lower())
                self.assertRegex(row, r"§(?:[0-9]|10)")

    def test_appendix_routes_through_cold_indexes_without_physical_paths(self) -> None:
        appendix = _section_text(self.text, "Appendix")
        self.assertNotRegex(
            appendix,
            r"wiki/survey/[^`|\s]*protocol-amendment-[0-9]+\.md",
        )
        self.assertIn(
            "Exact physical paths are resolved only through the named cold index on demand; "
            "neither index nor any legacy artifact is part of default context.",
            appendix,
        )
        rows = {
            int(match.group(1)): match.group(2)
            for match in re.finditer(
                r"^\|\s*Amendment\s+(\d+)\s*\|\s*([^|]+?)\s*\|",
                appendix,
                flags=re.MULTILINE,
            )
        }
        for number in (1, *range(3, 9)):
            self.assertEqual(f"campaign audit index / A{number}", rows[number])
        for number in range(9, 16):
            self.assertEqual(f"working archive index / A{number}", rows[number])

    def test_protocol_is_self_contained_not_amendment_dependent(self) -> None:
        normative = self.text[: self.text.index("## Appendix A")]
        forbidden = (
            "must read amendment",
            "read amendment",
            "see amendment",
            "查阅 amendment",
            "依赖 amendment",
            "amendment required",
        )
        for phrase in forbidden:
            self.assertNotIn(phrase.casefold(), normative.casefold())

    def test_coverage_matrix_sources_exist_and_normative_targets_carry_rules(self) -> None:
        self.assertEqual(set(AMENDMENT_PATHS), set(AMENDMENT_NUMBERS))
        seen_amendments = set()
        for item in AMENDMENT_COVERAGE:
            seen_amendments.add(item.amendment)
            source = AMENDMENT_PATHS[item.amendment].read_text(encoding="utf-8")
            self.assertIn(item.source_locator, source, f"missing source locator: {item}")
            target = _section_text(self.text, item.target_section)
            normalized_target = _normalize_prose(target)
            for phrase in item.required_phrases:
                self.assertIn(
                    _normalize_prose(phrase),
                    normalized_target,
                    f"uncovered amendment topic: {item}",
                )
        self.assertEqual(seen_amendments, set(AMENDMENT_NUMBERS))

    def test_exact_final_derivation_formulas(self) -> None:
        section = _normalize_prose(_section_text(self.text, "§6"))
        formulas = (
            "data_access_strict_bits = seven_strict_bits_all_false AND internal_visibility == api_only",
            "is_s0_core_compatible = data_access_strict_bits AND core_topology IN {single_core, single_core_multi_call} AND core_native_modality IN {audio_native, omni_native}",
            "is_reward_guided = EXISTS qualifying_reward_signal(s)",
            "is_rq_sys_control_compatible = control_horizon == sequential AND EXISTS valid LIVE edge e driven by the same qualifying reward signal s AND e.signal_use IN s.reward_uses",
            "is_project_method_candidate = is_s0_core_compatible AND is_rq_sys_control_compatible",
            "reward_guided_selection = candidate_pool_exists == true AND selection_policy IN {scored_select, tournament_select} AND selection_object != none AND EXISTS qualifying reward signal s used for select or prune",
            "offline_calibration signals never qualify",
        )
        for formula in formulas:
            self.assertIn(_normalize_prose(formula), section, formula)

    def test_e2_requires_complete_identifier_resolution_contract(self) -> None:
        section = _normalize_prose(_section_text(self.text, "§5"))
        required = (
            "before any E2 claim, resolve every entry by DOI, ACL ID, OpenReview ID, or normalized title",
            "total / resolved / ambiguous / unresolved",
            "DOI-only mutation fixture",
            "pre-registered unresolved ceiling",
            "K=2 zero growth on the resolved subgraph is not closure exhaustion",
        )
        for phrase in required:
            self.assertIn(_normalize_prose(phrase), section, phrase)

    def test_direct_threat_requires_exact_dual_coding_contract(self) -> None:
        section = _normalize_prose(_section_text(self.text, "§6"))
        required = (
            "DIRECT_THREAT requires threat_dual_coding",
            "two distinct extractors",
            "rec5_ref",
            "disagreements > 0 requires a nonempty adjudicator",
        )
        for phrase in required:
            self.assertIn(_normalize_prose(phrase), section, phrase)

    def test_reviewer_facing_reference_contract_is_explicit(self) -> None:
        section = _normalize_prose(_section_text(self.text, "§9"))
        required = (
            "author, year, and stable link",
            "numeric claims require a page, table, or figure locator",
            "non-contiguous quotation is explicitly marked as stitched",
            "consistent, dominant, or ceiling claims are limited to the model, task, and setting reported by the paper",
        )
        for phrase in required:
            self.assertIn(_normalize_prose(phrase), section, phrase)

    def test_incremental_scan_contract_covers_both_execution_boundaries(self) -> None:
        sources = _normalize_prose(
            _section_text(self.text, "§3") + "\n" + _section_text(self.text, "§8")
        )
        required = (
            "first execution searches through the execution date",
            "before synthesis freeze, scan from the first-execution date through the freeze date",
            "cross-period incremental batches are append-only",
            "old decisions change only by dated supersession",
        )
        for phrase in required:
            self.assertIn(_normalize_prose(phrase), sources, phrase)

    def test_section_4_has_an_explicit_normative_interpretation_fence(self) -> None:
        section = _normalize_prose(_section_text(self.text, "§3"))
        required = (
            "only the frozen compiler profile's ordered lane declarations and backtick query literal declarations in §4 are normative compiler input",
            "the canonical compiled result is exactly the current frozen JSONL's 65 ordered records and their record_sha256 values",
            "all other byte-preserved §4 narrative is NON-NORMATIVE historical annotation",
            "does not override §§0–3 or §§5–10, create an external dependency, or require opening a legacy file",
            "the interpretation fence and §§0–3 and §§5–10 have priority over non-normative §4 narrative",
        )
        for phrase in required:
            self.assertIn(_normalize_prose(phrase), section, phrase)

    def test_structured_protocol_contract_oracle_accepts_current_protocol(self) -> None:
        from sf_protocol_contract import validate_protocol_contracts

        self.assertEqual(validate_protocol_contracts(self.text), [])

    def test_structured_protocol_contract_oracle_rejects_semantic_mutations(self) -> None:
        from sf_protocol_contract import validate_protocol_contracts

        mutations = {
            "anchor-total-3-to-30": (
                "complete_pdf_occurrences <= 3",
                "complete_pdf_occurrences <= 30",
            ),
            "offline-negation-removed": (
                "offline_calibration signals never qualify",
                "offline_calibration signals qualify",
            ),
            "native-set-member-changed": (
                "{audio_native, omni_native}",
                "{audio_native, vision_native}",
            ),
            "incremental-append-only-negated": (
                "cross-period incremental batches are append-only",
                "cross-period incremental batches are not append-only",
            ),
            "fourth-amendment-negation-removed": (
                "A fourth amendment is forbidden before consolidation",
                "A fourth amendment is allowed before consolidation",
            ),
        }
        for name, (old, new) in mutations.items():
            with self.subTest(name=name):
                self.assertIn(old, self.text)
                mutated = self.text.replace(old, new, 1)
                self.assertTrue(validate_protocol_contracts(mutated), name)

    def test_section_contracts_stop_before_appendix_h2(self) -> None:
        from sf_protocol_contract import validate_protocol_contracts

        lifecycle = re.search(
            r"Consolidation is mandatory when a third correction.*?"
            r"A fourth amendment is forbidden before consolidation\.",
            self.text,
            flags=re.DOTALL,
        )
        self.assertIsNotNone(lifecycle)
        appendix = "## Appendix A — Legacy disposition routing (not an interpretive dependency)"
        self.assertIn(appendix, self.text)
        moved = self.text.replace(lifecycle.group(0), "", 1).replace(
            appendix,
            appendix + "\n\n" + lifecycle.group(0),
            1,
        )
        failures = validate_protocol_contracts(moved)
        self.assertIn(
            "missing-contract:third-correction-and-fourth-amendment-lifecycle:§10",
            failures,
        )

    def test_section_8_execution_steps_are_exact_and_strictly_ordered(self) -> None:
        from sf_protocol_contract import validate_protocol_contracts

        step_2 = (
            "2. run the first-step interface and phrase-behavior checks without a "
            "research model;"
        )
        step_3 = (
            "3. execute each frozen query with pagination and deterministic overflow "
            "splitting, logging every page;"
        )
        for step in (step_2, step_3):
            self.assertIn(step, _normalize_prose(self.text))
        marker = "2. __ORDER_SWAP_SENTINEL__;"
        mutated = self.text.replace(step_2, marker, 1)
        mutated = mutated.replace(step_3, step_2, 1).replace(marker, step_3, 1)
        failures = validate_protocol_contracts(mutated)
        self.assertIn("ordered-contract:stage1b-execution-sequence:§8", failures)

    def test_non_normative_section_4_narrative_mutations_do_not_change_contract(self) -> None:
        from sf_protocol_contract import validate_protocol_contracts

        baseline_records, baseline_bytes = _compile(CURRENT_PROTOCOL)
        mutations = (
            ("55 条查询", "550 条历史叙事查询"),
            ("Decision-Log 续59", "legacy://cold-audit-pointer"),
        )
        for old, new in mutations:
            with self.subTest(old=old):
                self.assertIn(old, self.text)
                mutated = self.text.replace(old, new, 1)
                self.assertEqual(validate_protocol_contracts(mutated), [])
                base, additions, lanes, _ = compiler.parse_all_queries(mutated)
                records = (
                    compiler.compile_records(base)
                    + compiler.compile_records(additions)
                    + compiler.compile_records(lanes)
                )
                self.assertEqual(len(records), len(baseline_records))
                self.assertEqual(compiler.render_records(records), baseline_bytes)

    def test_producer_replay_contract_appears_once(self) -> None:
        section = _normalize_prose(_section_text(self.text, "§9"))
        self.assertEqual(
            len(re.findall(r"deterministic producers? replay", section)),
            1,
        )


class CompilerProfileTests(unittest.TestCase):
    def test_legacy_current_and_frozen_bytes_are_identical(self) -> None:
        legacy_records, legacy_bytes = _compile(LEGACY_PROTOCOL)
        current_records, current_bytes = _compile(CURRENT_PROTOCOL)
        self.assertEqual(len(legacy_records), 65)
        self.assertEqual(len(current_records), 65)
        self.assertEqual(current_bytes, legacy_bytes)
        self.assertEqual(current_bytes, FROZEN_QUERIES.read_bytes())

    def test_all_record_hashes_recompute(self) -> None:
        records, _ = _compile(CURRENT_PROTOCOL)
        self.assertEqual(len(records), 65)
        for record in records:
            expected = compiler.compute_record_hash(
                {key: value for key, value in record.items() if key != "record_sha256"}
            )
            self.assertEqual(record["record_sha256"], expected, record["query_id"])

    def test_one_section_4_term_change_changes_compiled_bytes(self) -> None:
        legacy_text = compiler.load_protocol_text(LEGACY_PROTOCOL)
        mutated = legacy_text.replace('abs:"language agent"', 'abs:"language agents"', 1)
        self.assertNotEqual(mutated, legacy_text)
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "mutated.md"
            path.write_text(mutated, encoding="utf-8", newline="\n")
            _, baseline = _compile(LEGACY_PROTOCOL)
            _, changed = _compile(path)
        self.assertNotEqual(changed, baseline)

    def test_section_4_extraction_requires_exactly_one_exact_h2(self) -> None:
        text = compiler.load_protocol_text(LEGACY_PROTOCOL)
        block = compiler.extract_section_4(text)
        self.assertNotIn("## §4bis", block)
        with self.assertRaisesRegex(ValueError, "exactly one"):
            compiler.extract_section_4(text + "\n" + block)
        missing = text.replace("## §4 ", "## §X ", 1)
        with self.assertRaisesRegex(ValueError, "exactly one"):
            compiler.extract_section_4(missing)

    def test_hash_and_render_reject_nan_and_infinity(self) -> None:
        for value in (float("nan"), float("inf"), float("-inf")):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    compiler.compute_record_hash({"value": value})
                with self.assertRaises(ValueError):
                    compiler.render_records([{"value": value}])


class CompilerCliTests(unittest.TestCase):
    def _run(self, *args: str) -> subprocess.CompletedProcess[str]:
        env = os.environ.copy()
        env["PYTHONUTF8"] = "1"
        return subprocess.run(
            [sys.executable, str(HERE / "sf_query_compiler.py"), *args],
            cwd=REPO,
            text=True,
            encoding="utf-8",
            capture_output=True,
            check=False,
            env=env,
        )

    def test_check_mode_is_no_write_and_byte_exact(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "must-not-exist.jsonl"
            result = self._run(
                "--protocol", str(CURRENT_PROTOCOL),
                "--out", str(out),
                "--check",
                "--check-against", str(FROZEN_QUERIES),
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("PASS (65 byte-identical records)", result.stdout)
            self.assertFalse(out.exists())

    def test_check_requires_check_against(self) -> None:
        result = self._run("--check", "--protocol", str(CURRENT_PROTOCOL))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("--check-against", result.stderr + result.stdout)

    def test_check_against_requires_check_and_never_writes(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "must-not-exist.jsonl"
            result = self._run(
                "--protocol", str(CURRENT_PROTOCOL),
                "--out", str(out),
                "--check-against", str(FROZEN_QUERIES),
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("--check", result.stderr + result.stdout)
            self.assertFalse(out.exists())

    def test_missing_and_duplicate_section_4_are_controlled_cli_failures(self) -> None:
        text = compiler.load_protocol_text(CURRENT_PROTOCOL)
        variants = {
            "duplicate": text + "\n" + compiler.extract_section_4(text),
            "missing": text.replace("## §4 ", "## §X ", 1),
        }
        for name, variant in variants.items():
            with self.subTest(name=name), tempfile.TemporaryDirectory() as td:
                protocol = Path(td) / f"{name}.md"
                protocol.write_text(variant, encoding="utf-8", newline="\n")
                result = self._run(
                    "--protocol", str(protocol),
                    "--check", "--check-against", str(FROZEN_QUERIES),
                )
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("PARSE FAILURE", result.stderr + result.stdout)

    def test_check_rejects_crlf_even_when_json_records_are_equivalent(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            baseline = Path(td) / "crlf.jsonl"
            baseline.write_bytes(FROZEN_QUERIES.read_bytes().replace(b"\n", b"\r\n"))
            result = self._run(
                "--protocol", str(CURRENT_PROTOCOL),
                "--check", "--check-against", str(baseline),
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("byte difference", result.stdout + result.stderr)

    def test_atomic_write_preserves_old_destination_on_replace_failure(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            destination = Path(td) / "queries.jsonl"
            destination.write_bytes(b"old\n")
            with mock.patch.object(compiler.os, "replace", side_effect=OSError("injected")):
                with self.assertRaises(OSError):
                    compiler.atomic_write_bytes(destination, b"new\n")
            self.assertEqual(destination.read_bytes(), b"old\n")
            self.assertEqual([path.name for path in Path(td).iterdir()], ["queries.jsonl"])

    def test_atomic_write_cleans_only_new_empty_parent_chain_on_failures(self) -> None:
        failure_patches = (
            mock.patch.object(compiler.tempfile, "mkstemp", side_effect=OSError("stage")),
            mock.patch.object(compiler.os, "fsync", side_effect=OSError("write")),
            mock.patch.object(compiler.os, "replace", side_effect=OSError("replace")),
        )
        for index, failure_patch in enumerate(failure_patches):
            with self.subTest(index=index), tempfile.TemporaryDirectory() as td:
                existing = Path(td) / "existing"
                existing.mkdir()
                destination = existing / "new" / "deep" / "queries.jsonl"
                with failure_patch:
                    with self.assertRaises(OSError):
                        compiler.atomic_write_bytes(destination, b"new\n")
                self.assertTrue(existing.is_dir())
                self.assertFalse((existing / "new").exists())

    def test_parent_directory_fsync_is_posix_only(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            parent = Path(td)
            with (
                mock.patch.object(compiler.os, "name", "posix"),
                mock.patch.object(compiler.os, "open", return_value=91) as open_mock,
                mock.patch.object(compiler.os, "fsync") as fsync_mock,
                mock.patch.object(compiler.os, "close") as close_mock,
            ):
                compiler.fsync_parent_directory(parent)
            open_mock.assert_called_once()
            fsync_mock.assert_called_once_with(91)
            close_mock.assert_called_once_with(91)

            with (
                mock.patch.object(compiler.os, "name", "nt"),
                mock.patch.object(compiler.os, "open") as open_mock,
            ):
                compiler.fsync_parent_directory(parent)
            open_mock.assert_not_called()

    def test_successful_publish_keeps_parent_fsync_and_leaves_no_debris(self) -> None:
        for existing_target, expected_fsyncs in ((False, 1), (True, 2)):
            with self.subTest(existing_target=existing_target), tempfile.TemporaryDirectory() as td:
                parent = Path(td)
                destination = parent / "queries.jsonl"
                if existing_target:
                    destination.write_bytes(b"old\n")
                with mock.patch.object(
                    compiler, "fsync_parent_directory"
                ) as fsync_mock:
                    compiler.atomic_write_bytes(destination, b"new\n")
                self.assertEqual(fsync_mock.call_count, expected_fsyncs)
                self.assertEqual(destination.read_bytes(), b"new\n")
                self.assertEqual([path.name for path in parent.iterdir()], ["queries.jsonl"])

    def test_parent_fsync_failure_restores_existing_target_bytes_and_mode(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            destination = Path(td) / "queries.jsonl"
            destination.write_bytes(b"old\n")
            destination.chmod(0o640)
            old_mode = stat.S_IMODE(destination.stat().st_mode)
            with mock.patch.object(
                compiler,
                "fsync_parent_directory",
                side_effect=[None, OSError("publish-fsync"), None],
            ) as fsync_mock:
                with self.assertRaisesRegex(OSError, "publish-fsync"):
                    compiler.atomic_write_bytes(destination, b"new\n")
            self.assertEqual(destination.read_bytes(), b"old\n")
            self.assertEqual(stat.S_IMODE(destination.stat().st_mode), old_mode)
            self.assertEqual(fsync_mock.call_count, 3)
            self.assertEqual([path.name for path in Path(td).iterdir()], ["queries.jsonl"])

    def test_parent_fsync_failure_removes_fresh_target_and_new_parent_chain(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            existing = Path(td) / "existing"
            existing.mkdir()
            destination = existing / "new" / "deep" / "queries.jsonl"
            with mock.patch.object(
                compiler,
                "fsync_parent_directory",
                side_effect=[OSError("publish-fsync"), None],
            ) as fsync_mock:
                with self.assertRaisesRegex(OSError, "publish-fsync"):
                    compiler.atomic_write_bytes(destination, b"new\n")
            self.assertEqual(fsync_mock.call_count, 2)
            self.assertTrue(existing.is_dir())
            self.assertFalse((existing / "new").exists())

    def test_rollback_replace_failure_is_composite_and_keeps_recovery_backup(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            parent = Path(td)
            destination = parent / "queries.jsonl"
            destination.write_bytes(b"old\n")
            real_replace = compiler.os.replace
            replace_calls = 0

            def fail_second_replace(source, target):
                nonlocal replace_calls
                replace_calls += 1
                if replace_calls == 2:
                    raise OSError("rollback-replace")
                return real_replace(source, target)

            with (
                mock.patch.object(compiler.os, "replace", side_effect=fail_second_replace),
                mock.patch.object(
                    compiler,
                    "fsync_parent_directory",
                    side_effect=[None, OSError("publish-fsync")],
                ),
            ):
                with self.assertRaises(compiler.AtomicPublishRollbackError) as caught:
                    compiler.atomic_write_bytes(destination, b"new\n")

            message = str(caught.exception)
            self.assertIn("publish-fsync", message)
            self.assertIn("rollback-replace", message)
            self.assertEqual(destination.read_bytes(), b"new\n")
            backups = list(parent.glob(".queries.jsonl.*.bak"))
            self.assertEqual(len(backups), 1)
            self.assertEqual(backups[0].read_bytes(), b"old\n")
            self.assertEqual(list(parent.glob("*.tmp")), [])

    def test_rollback_fsync_failure_is_composite_without_backup_debris(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            parent = Path(td)
            destination = parent / "queries.jsonl"
            destination.write_bytes(b"old\n")
            with mock.patch.object(
                compiler,
                "fsync_parent_directory",
                side_effect=[
                    None,
                    OSError("publish-fsync"),
                    OSError("rollback-fsync"),
                ],
            ):
                with self.assertRaises(compiler.AtomicPublishRollbackError) as caught:
                    compiler.atomic_write_bytes(destination, b"new\n")
            message = str(caught.exception)
            self.assertIn("publish-fsync", message)
            self.assertIn("rollback-fsync", message)
            self.assertEqual(destination.read_bytes(), b"old\n")
            self.assertEqual([path.name for path in parent.iterdir()], ["queries.jsonl"])

    def test_main_turns_atomic_oserror_into_controlled_failure(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "queries.jsonl"
            stderr = io.StringIO()
            with (
                mock.patch.object(
                    compiler, "atomic_write_bytes", side_effect=OSError("injected")
                ),
                contextlib.redirect_stderr(stderr),
                contextlib.redirect_stdout(io.StringIO()),
            ):
                result = compiler.main(
                    ["--protocol", str(CURRENT_PROTOCOL), "--out", str(out)]
                )
            self.assertEqual(result, 1)
            self.assertIn("WRITE FAIL", stderr.getvalue())
            self.assertFalse(out.exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
