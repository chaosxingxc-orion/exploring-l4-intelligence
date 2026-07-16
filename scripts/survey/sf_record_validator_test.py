#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Record-validator acceptance test, v2 (correction #4B / P0-2.6).

Asserts, at SUBPROCESS level (real exit codes, no in-process shortcuts):
  - fixtures-c4b/positive_package.json  -> exit 0, zero violations;
  - every fixtures-c4b/N*.json negative -> exit != 0 with >=1 violation;
  - the negative set has exactly the cardinality sf_fixtures_c4b_gen.py
    generates, and every fixture's sha256 is pinned in the report.

The C4A version of this test proved only that 14 written negatives fail; the
C4B set adds the adversarial mutations doctoral re-review #4A demonstrated
against the v1 oracle (cross-wire / orphan / many-to-one / empty D2 block /
illegal inner enum / seed-threat loss / duplicate-target holes / disagreements
type crash / unbound seeds / duplicated publication_status). fixtures-c4a/ is
retained untouched as the historical C4A asset; it is no longer asserted green
(the v2 oracle is deliberately stricter).

Run from repo root:  python scripts/survey/sf_record_validator_test.py
Persists docs/checks/2026-07-16-sf-record-validator-test.json. Exit 0 iff all pass.
"""
import glob
import hashlib
import json
import os
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FIX = os.path.join(REPO, "wiki", "survey", "fixtures-c4b")
VALIDATOR = os.path.join(REPO, "scripts", "survey", "sf_record_validator.py")
OUT = os.path.join(REPO, "docs", "checks", "2026-07-16-sf-record-validator-test.json")
EXPECTED_NEGATIVES = 25


def run_validator(pkg_path):
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    r = subprocess.run([sys.executable, VALIDATOR, "--package", pkg_path],
                       capture_output=True, env=env)
    try:
        rep = json.loads(r.stdout.decode("utf-8", errors="replace"))
    except json.JSONDecodeError:
        rep = {"verdict": "UNPARSEABLE", "n_violations": None,
               "stderr": r.stderr.decode("utf-8", errors="replace")[-400:]}
    return r.returncode, rep


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    cases = []
    ok = True

    pos = os.path.join(FIX, "positive_package.json")
    code, rep = run_validator(pos)
    passed = (code == 0 and rep.get("n_violations") == 0)
    ok &= passed
    cases.append({"fixture": "positive_package.json", "expect": "exit 0",
                  "exit_code": code, "n_violations": rep.get("n_violations"),
                  "result": "PASS" if passed else "FAIL"})

    negatives = sorted(glob.glob(os.path.join(FIX, "N*.json")))
    if len(negatives) != EXPECTED_NEGATIVES:
        ok = False
        cases.append({"fixture": "(negative set cardinality)",
                      "expect": f"{EXPECTED_NEGATIVES} negatives on disk",
                      "exit_code": None, "n_violations": len(negatives),
                      "result": "FAIL"})
    for neg in negatives:
        code, rep = run_validator(neg)
        nv = rep.get("n_violations")
        passed = (code != 0 and isinstance(nv, int) and nv >= 1)
        ok &= passed
        cases.append({"fixture": os.path.basename(neg),
                      "expect": "subprocess exit != 0, >=1 structured violation",
                      "exit_code": code, "n_violations": nv,
                      "first_violation": (rep.get("violations") or [{}])[0],
                      "result": "PASS" if passed else "FAIL"})

    fixture_sha256 = {}
    for path in sorted(glob.glob(os.path.join(FIX, "*.json"))):
        with open(path, "rb") as f:
            fixture_sha256[os.path.basename(path)] = hashlib.sha256(f.read()).hexdigest()

    n_pass = sum(1 for c in cases if c["result"] == "PASS")
    report = {
        "artifact_id": "SF-RECORD-VALIDATOR-TEST-2026-07-16-02",
        "test": "scripts/survey/sf_record_validator_test.py",
        "validator": "scripts/survey/sf_record_validator.py (v2-c4b)",
        "fixtures_dir": "wiki/survey/fixtures-c4b",
        "generator": "scripts/survey/sf_fixtures_c4b_gen.py",
        "summary": f"{n_pass}/{len(cases)} (1 positive exit-0 + {EXPECTED_NEGATIVES} "
                   f"negatives subprocess non-zero)",
        "cases": cases,
        "fixture_sha256": fixture_sha256,
        "verdict": "PASS" if ok else "FAIL",
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "wb") as f:
        f.write((json.dumps(report, ensure_ascii=False, indent=1, sort_keys=True)
                 + "\n").encode("utf-8"))
    print(f"record validator test: {report['verdict']} ({report['summary']})")
    for c in cases:
        if c["result"] != "PASS":
            print(f"  FAIL: {c['fixture']} exit={c['exit_code']} nv={c['n_violations']}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
