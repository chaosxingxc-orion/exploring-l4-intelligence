#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Dual-platform evidence aggregator (v9-review P2).

The contract test writes a platform-stamped copy of its report
(…-v5-test.nt.json / …-v5-test.posix.json) so neither platform's run
overwrites the other's evidence. This aggregator asserts BOTH snapshots
exist, both verdicts are PASS, and their occupancy blocks are equal —
replacing the previous single-file-last-writer-wins prose claim.
"""
import io
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASE = os.path.join(REPO, "docs", "checks", "2026-07-19-sf-identity-taxonomy-v5-test")


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    reports = {}
    fails = []
    for plat in ("nt", "posix"):
        p = f"{BASE}.{plat}.json"
        if not os.path.exists(p):
            fails.append(f"missing platform snapshot: {os.path.basename(p)}")
            continue
        reports[plat] = json.load(io.open(p, encoding="utf-8"))
        if reports[plat].get("verdict") != "PASS":
            fails.append(f"{plat}: verdict {reports[plat].get('verdict')}")
    if len(reports) == 2:
        if reports["nt"]["occupancy"] != reports["posix"]["occupancy"]:
            fails.append("occupancy blocks differ between platforms")
        else:
            print(f"nt: {reports['nt']['platform']}  posix: {reports['posix']['platform']}")
            print("occupancy equality: CONFIRMED")
    for f in fails:
        print(f"[DUAL] {f}")
    print(f"dual-platform check: {'FAIL' if fails else 'PASS'} ({len(fails)} failures)")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
