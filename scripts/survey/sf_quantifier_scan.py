#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Unscoped-quantifier scan for reviewer-facing artifacts (v5-review lesson:
sixth completion-language failure was the unscoped-quantifier class 全量/唯一/零项).

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

FILES = [
    "wiki/2026-07-18-system-first-research-proposal-v5-consolidated.md",
    "wiki/2026-07-18-inherited-prior-exposure-union.md",
    "wiki/survey/2026-07-18-gate-s1-v5-response.md",
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
