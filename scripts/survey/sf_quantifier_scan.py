#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Unscoped-quantifier PROSE LINT for reviewer-facing artifacts.

SCOPE OF THIS TOOL (v5-response re-review P1-1): this is a lexical lint that
catches obviously-unscoped quantifier tokens. It is NOT a semantic defense —
it can be escaped by rephrasing or a hollow 〔SCOPED〕 marker. Set/denominator/
analysis-unit/construct correctness is owned by the reviewer checklist and the
identity-taxonomy contract tests, never by this lint.
(Origin: sixth completion-language failure was the unscoped-quantifier class.)

A quantifier token on a line is UNSCOPED unless the same line carries a scope
marker (已检视 / 下界 / 集合 / 快照 / 机器重算 / 本表合取 / ≥ / 〔SCOPED〕) or a
historical wrapper 〔HIST:. Findings are FAILURES — reviewer-facing prose must
quote machine-derived conjunctions instead of free quantifiers.

Self-test: an embedded negative fixture line must be flagged, else exit 1
(oracle-can-fail proof). Run from repo root:
  python scripts/survey/sf_quantifier_scan.py [file ...]
Default file set = the current reviewer-facing actives listed in FILES.
"""
import io
import re
import sys

# Default set = CURRENT reviewer-facing actives. MUST be updated when the
# submission artifact changes — a bare run that scans a stale file set passes
# vacuously (v7 internal review MAJOR-1: the lint attested green on v5 while
# the actual submission v7 had a hit). Keep this list pointing at what is
# actually being submitted.
FILES = [
    "wiki/survey/2026-07-19-gate-s1-v9-response.md",
    "wiki/survey/2026-07-19-sf-protocol-amendment-15.md",
    "wiki/survey/2026-07-19-sf-stage1b-opening-tables-v4.md",
    "wiki/survey/2026-07-19-sf-bibliography-v1.md",
    "wiki/survey/2026-07-18-sf-v5-claim-evidence-matrix.md",
    "wiki/2026-07-18-inherited-prior-exposure-union.md",
]
TOKEN = re.compile(r"全量|唯一|零项|持续缺位")
SCOPE = re.compile(r"已检视|下界|集合|快照|机器重算|机器可数|合取|≥|>=|〔SCOPED〕|〔HIST:|不称|禁止|不再|禁用|撤回|矛盾|forbidden")
NEG_FIXTURE = "本项目对该问题的解决是全量且唯一的。"


def scan_text(name, text):
    hits = []
    for i, line in enumerate(text.splitlines(), 1):
        if TOKEN.search(line) and not SCOPE.search(line):
            hits.append((name, i, line.strip()[:90]))
    return hits


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if not scan_text("<fixture>", NEG_FIXTURE):
        print("[FAIL] negative fixture NOT flagged — scanner oracle broken")
        return 1
    files = sys.argv[1:] or FILES
    all_hits = []
    for f in files:
        try:
            text = io.open(f, encoding="utf-8").read()
        except FileNotFoundError:
            print(f"[skip] {f} (missing)")
            continue
        all_hits += scan_text(f, text)
    for name, i, line in all_hits:
        print(f"[UNSCOPED] {name}:{i}: {line}")
    print(f"quantifier scan: {'FAIL' if all_hits else 'PASS'} ({len(all_hits)} unscoped)")
    return 1 if all_hits else 0


if __name__ == "__main__":
    sys.exit(main())
