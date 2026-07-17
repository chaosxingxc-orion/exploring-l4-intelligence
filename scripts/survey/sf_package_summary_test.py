#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Mutation harness for the fail-closed package summary (correction #4B / P0-1.5
+ P0-4.3).

Builds an isolated copy of every input the summary chain consumes, asserts the
baseline is green, then applies each adversarial mutation the doctoral
re-review #4A demonstrated (plus the C4B additions) to a FRESH copy and asserts
the summary exits non-zero:

  m1 seed manifest truncated to 2 rows          (canon exact-count kill)
  m2 route audit evidence emptied               (EVIDENCE_PRESENT + adjudication kill)
  m3 forbidden token + historical marker on ONE line of an active file
                                                (occurrence-level scan kill)
  m4 record-validator evidence replaced by a hand-written {"verdict":"PASS"}
                                                (producer byte-compare kill)
  m5 active file deleted                        (missing-file = FAIL kill)
  m6 one byte flipped inside the frozen query prefix (prefix-hash kill)
  m7 bundle-manifest MACHINE_COUNT off by one   (cardinality reconciliation kill)

Plus the P0-4.3 boundary pair, run against the sentinel runner directly:
  b+ synthetic sentinel with a complete BOUNDARY_REG line -> REGISTERED_BOUNDARY,
     runner exit 0;
  b- same sentinel, registration file exists but lacks the paper id ->
     UNRESOLVED_MISS, runner exit 1.

Run from repo root:  python scripts/survey/sf_package_summary_test.py
Persists docs/checks/2026-07-17-sf-package-summary-mutations.json. Exit 0 iff
baseline green AND every mutation fails closed.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(REPO, "docs", "checks", "2026-07-17-sf-package-summary-mutations.json")
COPY_TREES = ["scripts/survey", "wiki/survey", "docs/checks", "docs/survey-provenance"]
# wiki-root files enumerated in the manifest #4B section — the summary's
# existence checks (manifest reconciliation + active surface) need them present
WIKI_ROOT_FILES = ["wiki/Research-Objective.md", "wiki/Decision-Log.md",
                   "wiki/2026-07-16-gate-s1-p0r8-rereview-doctoral-review.md"]
SEEDS = "wiki/survey/2026-07-15-sf-seed-manifest.jsonl"
QUERIES = "wiki/survey/2026-07-15-sf-queries.jsonl"
ROUTE_AUDIT = "docs/checks/2026-07-16-sf-t1-routes-status-audit.json"
RV_EVIDENCE = "docs/checks/2026-07-16-sf-record-validator-test.json"
README = "wiki/survey/README.md"
BLANKS = "wiki/survey/2026-07-15-sf-blank-templates.md"
MANIFEST = "wiki/survey/2026-07-15-sf-bundle-manifest.md"
SENTINELS = "wiki/survey/2026-07-16-sf-sentinel-data.json"


def build_copy():
    root = tempfile.mkdtemp(prefix="sfpkg_")
    for tree in COPY_TREES:
        shutil.copytree(os.path.join(REPO, tree), os.path.join(root, tree))
    for rel in WIKI_ROOT_FILES:
        dst = os.path.join(root, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copyfile(os.path.join(REPO, rel), dst)
    return root


def run_summary(root):
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    r = subprocess.run([sys.executable,
                        os.path.join(root, "scripts", "survey", "sf_package_summary.py")],
                       capture_output=True, env=env, cwd=root)
    return r.returncode, r.stdout.decode("utf-8", errors="replace")


def m1_two_seeds(root):
    p = os.path.join(root, SEEDS)
    lines = open(p, "rb").read().split(b"\n")
    open(p, "wb").write(b"\n".join(lines[:2]) + b"\n")


def m2_empty_route_evidence(root):
    p = os.path.join(root, ROUTE_AUDIT)
    open(p, "w", encoding="utf-8").write(
        '{"n_routes": 50, "rows": [], "note": "no probes and no adjudication"}\n')


def m3_same_line_marker_token(root):
    p = os.path.join(root, README)
    # the forbidden token is assembled at runtime so THIS source file (itself on
    # the active scan surface) never carries the literal
    token = "55 条" + "编译冻结查询"
    with open(p, "a", encoding="utf-8") as f:
        f.write(f"\nACTIVE CANON: {token} remains live; 历史口径 HISTORICAL_SUPERSEDED\n")


def m4_hand_written_verdict(root):
    p = os.path.join(root, RV_EVIDENCE)
    open(p, "w", encoding="utf-8").write(
        '{"verdict": "PASS", "summary": "hand-written green light, no test was run"}\n')


def m5_delete_active_file(root):
    os.remove(os.path.join(root, BLANKS))


def m6_flip_prefix_byte(root):
    p = os.path.join(root, QUERIES)
    data = bytearray(open(p, "rb").read())
    lines = data.split(b"\n")
    row = bytearray(lines[2])
    idx = row.find(b'"lane"')
    row[idx + 1:idx + 2] = b"L"
    lines[2] = bytes(row)
    open(p, "wb").write(b"\n".join(lines))


def m7_machine_count_off_by_one(root):
    import re
    p = os.path.join(root, MANIFEST)
    t = open(p, encoding="utf-8").read()
    # the summary parses the LAST dated-correction section (canon section_marker),
    # so the mutation must hit the LAST MACHINE_COUNT line, not the first (#4B)
    matches = list(re.finditer(r"(MACHINE_COUNT:\s*files=)(\d+)", t))
    if not matches:
        raise RuntimeError("MACHINE_COUNT line not found — dated correction section missing")
    m = matches[-1]
    t = t[:m.start(2)] + str(int(m.group(2)) + 1) + t[m.end(2):]
    open(p, "w", encoding="utf-8", newline="").write(t)


MUTATIONS = [m1_two_seeds, m2_empty_route_evidence, m3_same_line_marker_token,
             m4_hand_written_verdict, m5_delete_active_file, m6_flip_prefix_byte,
             m7_machine_count_off_by_one]


def boundary_pair():
    """P0-4.3: REGISTERED_BOUNDARY must require a complete per-paper BOUNDARY_REG
    line — run the sentinel runner directly on a synthetic package."""
    results = []
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    for label, include_id in (("boundary_positive", True), ("boundary_negative", False)):
        root = build_copy()
        try:
            sid = "2604.99999"
            donor = "2604.13552"
            atom_src = os.path.join(root, "docs", "survey-provenance", "atom", f"{donor}.xml")
            atom_dst = os.path.join(root, "docs", "survey-provenance", "atom", f"{sid}.xml")
            shutil.copyfile(atom_src, atom_dst)
            digest = hashlib.sha256(open(atom_dst, "rb").read()).hexdigest()
            reg_rel = "wiki/survey/boundary-reg-fixture.md"
            reg_line = ('BOUNDARY_REG {"paper": "%s", "boundary": "OUT_OF_SCOPE_TEST", '
                        '"reason": "harness fixture", "adjudicator": "harness", '
                        '"date": "2026-07-17"}' % (sid if include_id else "0000.00000"))
            open(os.path.join(root, reg_rel), "w", encoding="utf-8").write(
                "# fixture\n" + reg_line + "\n")
            sp = os.path.join(root, SENTINELS)
            data = json.load(open(sp, encoding="utf-8"))
            data["papers"][sid] = {
                "title": "Zqxjkv unmatched synthetic title",
                "source_normalized_abstract": "Zqxjkv wvutsr qponml — no lane family term "
                                              "appears in this synthetic abstract.",
                "categories": ["cs.CL"], "primary_category": "cs.CL",
                "atom_xml": f"docs/survey-provenance/atom/{sid}.xml",
                "atom_sha256": digest, "held_out": False, "in_seed_batch": None,
                "used_in_query_design": False,
                "reviewer_role": "harness boundary fixture (P0-4.3)",
                "accepted_boundary": {"registered_in": reg_rel},
            }
            json.dump(data, open(sp, "w", encoding="utf-8"), ensure_ascii=False, indent=1,
                      sort_keys=True)
            r = subprocess.run([sys.executable,
                                os.path.join(root, "scripts", "survey",
                                             "sf_sentinel_recall_test.py")],
                               capture_output=True, env=env, cwd=root)
            rep = json.load(open(os.path.join(root, "docs", "checks",
                                              "2026-07-16-sf-sentinel-recall.json"),
                                 encoding="utf-8"))
            outcome = rep["sentinels"].get(sid, {}).get("outcome")
            if include_id:
                ok = (r.returncode == 0 and outcome == "REGISTERED_BOUNDARY")
                expect = "exit 0 + REGISTERED_BOUNDARY"
            else:
                ok = (r.returncode != 0 and outcome == "UNRESOLVED_MISS")
                expect = "exit != 0 + UNRESOLVED_MISS"
            results.append({"case": label, "expect": expect, "exit_code": r.returncode,
                            "outcome": outcome, "result": "PASS" if ok else "FAIL"})
        finally:
            shutil.rmtree(root, ignore_errors=True)
    return results


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    cases = []
    ok = True

    root = build_copy()
    try:
        code, out = run_summary(root)
        passed = code == 0
        ok &= passed
        cases.append({"case": "baseline", "expect": "exit 0 (all green)",
                      "exit_code": code, "result": "PASS" if passed else "FAIL",
                      "tail": out.splitlines()[-1] if out else ""})
    finally:
        shutil.rmtree(root, ignore_errors=True)

    for fn in MUTATIONS:
        root = build_copy()
        try:
            fn(root)
            code, out = run_summary(root)
            passed = code != 0
            ok &= passed
            cases.append({"case": fn.__name__, "expect": "exit != 0 (fail closed)",
                          "exit_code": code, "result": "PASS" if passed else "FAIL",
                          "tail": out.splitlines()[0] if out else ""})
        except Exception as e:  # noqa: BLE001 — harness must report, not die
            ok = False
            cases.append({"case": fn.__name__, "expect": "exit != 0 (fail closed)",
                          "exit_code": None, "result": "FAIL",
                          "tail": f"harness error: {type(e).__name__}: {e}"})
        finally:
            shutil.rmtree(root, ignore_errors=True)

    bres = boundary_pair()
    for c in bres:
        ok &= c["result"] == "PASS"
    cases.extend(bres)

    n_pass = sum(1 for c in cases if c["result"] == "PASS")
    report = {
        "artifact_id": "SF-PACKAGE-SUMMARY-MUTATIONS-2026-07-17-01",
        "test": "scripts/survey/sf_package_summary_test.py",
        "summary": f"{n_pass}/{len(cases)} (baseline green + {len(MUTATIONS)} mutations "
                   "fail closed + boundary pair)",
        "cases": cases,
        "verdict": "PASS" if ok else "FAIL",
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "wb") as f:
        f.write((json.dumps(report, ensure_ascii=False, indent=1) + "\n").encode("utf-8"))
    print(f"package summary mutation harness: {report['verdict']} ({report['summary']})")
    for c in cases:
        flag = "PASS" if c["result"] == "PASS" else "FAIL"
        print(f"  [{flag}] {c['case']}: exit={c['exit_code']} ({c.get('tail', '')[:90]})")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
