#!/usr/bin/env python3
"""P0-R8 repo-level fail-closed state-gate validator (umbrella repo).

Machine gate intended to intercept the defect classes repeated doctoral
reviews kept finding in this repo's wiki (overclaimed/stale numbers asserted
without a "do not re-cite this" qualifier, unresolved-identity rows paired
with an "exact N papers" claim, malformed claim-ledger rows, signoff slots
silently filled in instead of left PENDING, "decision ready" asserted as
already-achieved, dangling provenance anchors, bare banned tokens missing
their required qualifying suffix, and a stale protocol doc not properly
voided).

Design constraints (see task spec):
  - stdlib only, no network, deterministic.
  - exit 0 iff ALL 8 rules (R1..R8) pass, else exit 1.
  - stdout only: one 'PASS|FAIL <rule_id> <detail-count>' line per rule (in
    order), then detail lines for any FAILs, then 'OVERALL: PASS|FAIL'.
  - writes nothing to disk.

Each rule is implemented literally against the task's rule text. Some rules
are intentionally strict (e.g. same-line qualifier requirement, or flagging
CLAIM_LOCATED_FULLTEXT rows whose source_locator merely *mentions* "abstract"
alongside real fulltext loci) -- that strictness is the point of a
fail-closed gate and must not be loosened just to make the run go green.
"""

from __future__ import annotations

import fnmatch
import json
import re
import subprocess
import sys
from pathlib import Path

# Repo root is derived from this file's own location (scripts/integrity/..),
# not from the process cwd, so the gate is deterministic regardless of where
# it is invoked from.
REPO_ROOT = Path(__file__).resolve().parents[2]

HOT_FILES = [
    "wiki/Research-Objective.md",
    "wiki/Per-Work-Status.md",
]

# R1 banned patterns (verbatim from the task spec).
BANNED_PATTERNS = [
    "43 条 discrepancy",
    "43 discrepancies",
    "35 全文",
    "35 fulltext",
    "92 resolved",
    "精确 92",
    "精确 94 篇",
    "P0 八项全部",
    "P0_R_COMPLETE",
    "prerequisites_met",
]

# Qualifier tokens shared by R1 / R2 / R7 (verbatim from the task spec).
QUALIFIER_TOKENS = [
    "撤回",
    "勿再引",
    "do_not_claim",
    "误计",
    "作废",
    "不再",
    "停用",
]

# R5 uses its own, separately-specified qualifier set.
R5_QUALIFIER_TOKENS = ["申请", "待", "门", "后", "not", "未"]

R2_JSONL = "wiki/survey/2026-07-14-canonical-census-v2/paper_works.jsonl"
R3_JSONL = "wiki/survey/2026-07-14-claim-ledger-v2/claim_ledger_v2.jsonl"

R3_DISCREPANCY_ENUM = {"NONE", "MINOR", "MATERIAL", "CRITICAL", "UNVERIFIED"}
R3_EVIDENCE_ENUM = {
    "CLAIM_LOCATED_FULLTEXT",
    "ABSTRACT_ONLY",
    "FULLTEXT_UNREACHABLE_THIS_ROUND",
    "SYNTHESIS_PENDING_REVIEW",
}

R5_RESP04 = "wiki/2026-07-14-resp04-gate-a-execution.md"

R6_ANCHOR_PAIRS = [
    (
        "78d048550080bb3131b3d1db9646ff4dfbf0c0f0",
        "wiki/2026-07-14-1b-probe-protocol-v1.md",
    ),
    (
        "f5c736e9a9dffd9ddc3312a789291f9f3e110d6c",
        "wiki/2026-07-14-p0r-progress-review-submission.md",
    ),
]

R8_FILE = "wiki/2026-07-14-identity-contracts-amendment-1.md"

R2_REGEX = re.compile(r"精确\s*9[0-9]\s*(篇|works)")
R7_TOKEN_RE = re.compile(r"NO_DIRECT_MATCH")
R7_OK_SUFFIXES = ("_AMONG_RETAINED_RECORDS", "_WITHIN")


def read_text(path: Path) -> str | None:
    """Read a file as UTF-8. Returns None (caller must handle) if missing."""
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return None


def has_any(line: str, tokens: list[str]) -> bool:
    return any(tok in line for tok in tokens)


# ---------------------------------------------------------------------------
# R1_HOT_CLAIM_QUALIFIERS
# ---------------------------------------------------------------------------
def rule_r1() -> list[str]:
    fails: list[str] = []
    for rel in HOT_FILES:
        path = REPO_ROOT / rel
        text = read_text(path)
        if text is None:
            fails.append(f"{rel}: FILE_MISSING")
            continue
        for lineno, line in enumerate(text.splitlines(), 1):
            matched = [pat for pat in BANNED_PATTERNS if pat in line]
            if not matched:
                continue
            if has_any(line, QUALIFIER_TOKENS):
                continue
            fails.append(
                f"{rel}:{lineno}: banned={matched} line={line.strip()[:200]!r}"
            )
    return fails


# ---------------------------------------------------------------------------
# R2_UNRESOLVED_VS_EXACT
# ---------------------------------------------------------------------------
def rule_r2() -> list[str]:
    fails: list[str] = []
    jsonl_path = REPO_ROOT / R2_JSONL
    text = read_text(jsonl_path)
    has_unresolved = False
    if text is None:
        fails.append(f"{R2_JSONL}: FILE_MISSING")
    else:
        for lineno, line in enumerate(text.splitlines(), 1):
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                fails.append(f"{R2_JSONL}:{lineno}: JSON_DECODE_ERROR: {exc}")
                continue
            if row.get("status") == "IDENTITY_UNRESOLVED":
                has_unresolved = True

    if not has_unresolved:
        return fails

    for rel in HOT_FILES:
        path = REPO_ROOT / rel
        hot_text = read_text(path)
        if hot_text is None:
            fails.append(f"{rel}: FILE_MISSING")
            continue
        for lineno, line in enumerate(hot_text.splitlines(), 1):
            for m in R2_REGEX.finditer(line):
                if has_any(line, QUALIFIER_TOKENS):
                    continue
                fails.append(
                    f"{rel}:{lineno}: match={m.group(0)!r} "
                    f"line={line.strip()[:200]!r}"
                )
    return fails


# ---------------------------------------------------------------------------
# R3_LEDGER_ENUMS
# ---------------------------------------------------------------------------
def rule_r3() -> list[str]:
    fails: list[str] = []
    path = REPO_ROOT / R3_JSONL
    text = read_text(path)
    if text is None:
        return [f"{R3_JSONL}: FILE_MISSING"]

    abstract_re = re.compile(r"abstract", re.IGNORECASE)
    for lineno, line in enumerate(text.splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            fails.append(f"{R3_JSONL}:{lineno}: JSON_DECODE_ERROR: {exc}")
            continue

        claim_id = row.get("claim_id", f"<no claim_id at line {lineno}>")

        ds = row.get("discrepancy_status")
        if ds not in R3_DISCREPANCY_ENUM:
            fails.append(f"{claim_id}: invalid discrepancy_status={ds!r}")

        eg = row.get("evidence_grade")
        if eg not in R3_EVIDENCE_ENUM:
            fails.append(f"{claim_id}: invalid evidence_grade={eg!r}")

        if eg == "CLAIM_LOCATED_FULLTEXT":
            locator = row.get("source_locator") or ""
            if isinstance(locator, str) and abstract_re.search(locator):
                fails.append(
                    f"{claim_id}: evidence_grade=CLAIM_LOCATED_FULLTEXT but "
                    f"source_locator matches /abstract/i: {locator!r}"
                )
    return fails


# ---------------------------------------------------------------------------
# R4_SIGNOFF_SLOTS
# ---------------------------------------------------------------------------
def rule_r4() -> list[str]:
    fails: list[str] = []
    wiki_dir = REPO_ROOT / "wiki"
    if not wiki_dir.is_dir():
        return ["wiki/: DIRECTORY_MISSING"]

    candidates: list[Path] = []
    for path in sorted(wiki_dir.glob("2026-07-14-*.md")):
        name_lower = path.name.lower()
        name_matches = (
            "resp" in name_lower
            or "submission" in name_lower
            or fnmatch.fnmatch(name_lower, "p0r-*.md")
        )
        if name_matches:
            candidates.append(path)

    for path in candidates:
        text = read_text(path)
        if text is None:
            continue
        rel = path.relative_to(REPO_ROOT).as_posix()
        for lineno, line in enumerate(text.splitlines(), 1):
            if "integrity_reviewer" not in line:
                continue
            if "owner_adjudications" in line:
                # Owner-adjudication lines are a separate, allowed pattern.
                continue
            if "PENDING" in line:
                continue
            fails.append(f"{rel}:{lineno}: {line.strip()[:200]!r}")
    return fails


# ---------------------------------------------------------------------------
# R5_DECISION_READY
# ---------------------------------------------------------------------------
def rule_r5() -> list[str]:
    fails: list[str] = []

    # Per the rule spec, the newest RESP file (RESP-04) is *assumed* to
    # contain a non-empty blockers/未做/PENDING statement -- the gate is
    # unconditionally active. We still surface a note if the anchor file is
    # missing, since that would undermine the premise the rule is built on.
    resp04_path = REPO_ROOT / R5_RESP04
    if read_text(resp04_path) is None:
        fails.append(f"{R5_RESP04}: FILE_MISSING (rule premise assumed true regardless)")

    wiki_dir = REPO_ROOT / "wiki"
    if not wiki_dir.is_dir():
        fails.append("wiki/: DIRECTORY_MISSING")
        return fails

    for path in sorted(wiki_dir.glob("*.md")):
        text = read_text(path)
        if text is None:
            continue
        rel = path.relative_to(REPO_ROOT).as_posix()
        for lineno, line in enumerate(text.splitlines(), 1):
            if "STAGE1C_DECISION_READY" not in line:
                continue
            if has_any(line, R5_QUALIFIER_TOKENS):
                continue
            fails.append(f"{rel}:{lineno}: {line.strip()[:200]!r}")
    return fails


# ---------------------------------------------------------------------------
# R6_ANCHOR_EXISTS
# ---------------------------------------------------------------------------
def rule_r6() -> list[str]:
    fails: list[str] = []
    for commit, rel in R6_ANCHOR_PAIRS:
        spec = f"{commit}:{rel}"
        try:
            result = subprocess.run(
                ["git", "cat-file", "-e", spec],
                cwd=str(REPO_ROOT),
                capture_output=True,
            )
        except FileNotFoundError:
            fails.append(f"{spec}: git executable not found on PATH")
            continue
        if result.returncode != 0:
            stderr = result.stderr.decode("utf-8", errors="replace").strip()
            fails.append(f"{spec}: MISSING (git exit={result.returncode} stderr={stderr!r})")
    return fails


# ---------------------------------------------------------------------------
# R7_BARE_TOKEN
# ---------------------------------------------------------------------------
def rule_r7() -> list[str]:
    fails: list[str] = []
    wiki_dir = REPO_ROOT / "wiki"
    if not wiki_dir.is_dir():
        return ["wiki/: DIRECTORY_MISSING"]

    for path in sorted(wiki_dir.glob("*.md")):
        name_lower = path.name.lower()
        if "review" in name_lower or "rereview" in name_lower:
            continue

        text = read_text(path)
        if text is None:
            continue
        lines = text.splitlines()
        head = "\n".join(lines[:40])
        if "SUPERSESSION" in head:
            continue

        rel = path.relative_to(REPO_ROOT).as_posix()
        for lineno, line in enumerate(lines, 1):
            for m in R7_TOKEN_RE.finditer(line):
                after = line[m.end():]
                if after.startswith(R7_OK_SUFFIXES):
                    continue
                if has_any(line, QUALIFIER_TOKENS):
                    continue
                fails.append(f"{rel}:{lineno}: {line.strip()[:200]!r}")
    return fails


# ---------------------------------------------------------------------------
# R8_PROTOCOL_V1_VOID
# ---------------------------------------------------------------------------
def rule_r8() -> list[str]:
    path = REPO_ROOT / R8_FILE
    text = read_text(path)
    if text is None:
        return [f"{R8_FILE}: FILE_MISSING"]

    missing = [tok for tok in ("SUPERSEDED", "prerequisites_met") if tok not in text]
    if missing:
        return [f"{R8_FILE}: MISSING_TOKENS={missing}"]
    return []


RULES = [
    ("R1_HOT_CLAIM_QUALIFIERS", rule_r1),
    ("R2_UNRESOLVED_VS_EXACT", rule_r2),
    ("R3_LEDGER_ENUMS", rule_r3),
    ("R4_SIGNOFF_SLOTS", rule_r4),
    ("R5_DECISION_READY", rule_r5),
    ("R6_ANCHOR_EXISTS", rule_r6),
    ("R7_BARE_TOKEN", rule_r7),
    ("R8_PROTOCOL_V1_VOID", rule_r8),
]


def main() -> int:
    # Force deterministic UTF-8 stdout regardless of the host console's
    # active code page (Windows consoles are frequently not UTF-8 by
    # default, which would otherwise crash on the CJK content this gate
    # inspects).
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass

    all_results: list[tuple[str, list[str]]] = []
    overall_pass = True

    for rule_id, fn in RULES:
        details = fn()
        status = "PASS" if not details else "FAIL"
        if details:
            overall_pass = False
        all_results.append((rule_id, details))
        print(f"{status} {rule_id} {len(details)}")

    for rule_id, details in all_results:
        for detail in details:
            print(f"  {rule_id}: {detail}")

    print(f"OVERALL: {'PASS' if overall_pass else 'FAIL'}")
    return 0 if overall_pass else 1


if __name__ == "__main__":
    sys.exit(main())
