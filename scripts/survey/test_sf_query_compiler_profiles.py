#!/usr/bin/env python3
"""Regression contract for the effective protocol and offline query compiler.

This suite deliberately contains a human-auditable amendment coverage matrix.
Appendix A is routing-only: every matrix assertion is scoped to the target
normative section, so an appendix disposition row can never satisfy coverage.
"""

from __future__ import annotations

import os
import re
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


LEGACY_PROTOCOL = REPO / "wiki/survey/2026-07-15-system-first-survey-protocol-v1.md"
CURRENT_PROTOCOL = REPO / "wiki/survey/current/protocol.md"
FROZEN_QUERIES = REPO / "wiki/survey/2026-07-15-sf-queries.jsonl"

EXPECTED_FRONTMATTER = (
    "---\n"
    "protocol_id: SF-SYSTEM-FIRST-STAGE1B\n"
    "protocol_version: 2\n"
    "effective_date: 2026-07-19\n"
    "stage: Stage-1A survey-ready gate\n"
    "execution_authorized: false\n"
    "supersedes_effective_chain: protocol-v1 plus amendments 1 and 3-15\n"
    "audit_index: wiki/audit/system-first-stage1a/INDEX.md\n"
    "---\n"
).encode("utf-8")

AMENDMENT_NUMBERS = (1, *range(3, 16))
AMENDMENT_PATHS = {
    1: REPO / "wiki/survey/2026-07-15-sf-protocol-amendment-1.md",
    3: REPO / "wiki/survey/2026-07-16-sf-protocol-amendment-3.md",
    4: REPO / "wiki/survey/2026-07-16-sf-protocol-amendment-4.md",
    5: REPO / "wiki/survey/2026-07-16-sf-protocol-amendment-5.md",
    6: REPO / "wiki/survey/2026-07-17-sf-protocol-amendment-6.md",
    7: REPO / "wiki/survey/2026-07-17-sf-protocol-amendment-7.md",
    8: REPO / "wiki/survey/2026-07-18-sf-protocol-amendment-8.md",
    9: REPO / "wiki/survey/2026-07-18-sf-protocol-amendment-9.md",
    10: REPO / "wiki/survey/2026-07-18-sf-protocol-amendment-10.md",
    11: REPO / "wiki/survey/2026-07-18-sf-protocol-amendment-11.md",
    12: REPO / "wiki/survey/2026-07-18-sf-protocol-amendment-12.md",
    13: REPO / "wiki/survey/2026-07-19-sf-protocol-amendment-13.md",
    14: REPO / "wiki/survey/2026-07-19-sf-protocol-amendment-14.md",
    15: REPO / "wiki/survey/2026-07-19-sf-protocol-amendment-15.md",
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
    CoverageItem(3, "A3-11", "§0", ("Stage-1A survey-ready gate", "not Stage-1A close")),
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
    CoverageItem(8, "可回放性矩阵", "§8", ("bundle-only", "local-data", "network-dependent")),

    # Amendment 9.
    CoverageItem(9, "阶段正典", "§0", ("Stage-1B", "no research-model", "no smoke")),
    CoverageItem(9, "exposure", "§8", ("current_activity_stage", "new_model_touches_since_gate_freeze", "INHERITED_PRIOR_EXPOSURE")),
    CoverageItem(9, "claim-evidence", "§9", ("MACHINE_RECOMPUTED_LOCAL", "SOURCE_REPORTED_TRACEABLE", "TEAM_ATTESTATION")),
    CoverageItem(9, "system-control", "§6", ("13-axis", "decision rights", "information boundary")),
    CoverageItem(9, "known-item", "§5", ("REVIEWER_KNOWN_ITEM", "carry-forward ledger")),
    CoverageItem(9, "Stage-2A", "§0", ("Stage-2A reproduction-first", "no present execution force")),
    CoverageItem(9, "双向证据", "§9", ("supporting evidence", "contradicting evidence", "kill criterion")),

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


if __name__ == "__main__":
    unittest.main(verbosity=2)
