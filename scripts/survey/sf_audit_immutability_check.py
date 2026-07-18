#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Audit-artifact immutability check (v7 doctoral review Gate MAJOR-3).

Asserts that every audit-layer dated artifact registered in
wiki/survey/sf-audit-artifact-registry.json still has its pinned git blob
at HEAD, and has no uncommitted working-tree drift. Any change to a
registered path FAILS: corrections must be NEW dated supersession files,
appended to the registry — never in-place rewrites.

Scope note: this guards the correct-workflow audit semantics only; it does
not defend against malicious metadata tampering (out of scope per review
§6.3). The registry itself is append-only: duplicate path rows fail.

Self-test: an in-memory fixture with a wrong pinned blob must be detected,
else exit 1 (oracle-can-fail proof).

Run from anywhere:
  python scripts/survey/sf_audit_immutability_check.py
Writes docs/checks/2026-07-19-sf-audit-immutability-check.json.
"""
import io
import json
import os
import subprocess
import sys

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
REGISTRY = os.path.join(REPO, "wiki", "survey", "sf-audit-artifact-registry.json")
OUT = os.path.join(REPO, "docs", "checks", "2026-07-19-sf-audit-immutability-check.json")


def git(*args):
    return subprocess.run(["git", *args], cwd=REPO, capture_output=True,
                          text=True, encoding="utf-8", errors="replace")


def head_blobs():
    out = git("ls-tree", "-r", "HEAD", "--", "wiki/").stdout
    blobs = {}
    for line in out.splitlines():
        meta, path = line.split("\t", 1)
        blobs[path] = meta.split()[2]
    return blobs


def evaluate(artifacts, blobs, dirty_paths):
    """Pure evaluation so the negative fixture can reuse the real oracle."""
    failures = []
    seen = set()
    for a in artifacts:
        p, pin = a["path"], a["git_blob"]
        if p in seen:
            failures.append(f"{p}: duplicate registry row (append-only violated)")
        seen.add(p)
        actual = blobs.get(p)
        if actual is None:
            failures.append(f"{p}: missing at HEAD (registered artifact deleted)")
        elif actual != pin:
            failures.append(f"{p}: blob {actual[:12]} != pinned {pin[:12]} — "
                            f"in-place rewrite; use a NEW dated supersession file")
        if p in dirty_paths:
            failures.append(f"{p}: uncommitted working-tree drift")
    return failures


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    reg = json.load(io.open(REGISTRY, encoding="utf-8"))
    blobs = head_blobs()
    status = git("status", "--porcelain", "--", "wiki/").stdout
    dirty = {l[3:].strip().strip('"') for l in status.splitlines() if l.strip()}

    # oracle-can-fail proof: a wrong pin MUST be flagged by the same oracle
    fx = [{"path": reg["artifacts"][0]["path"], "git_blob": "0" * 40}]
    if not evaluate(fx, blobs, set()):
        print("[FAIL] negative fixture NOT flagged — immutability oracle broken")
        return 1

    failures = evaluate(reg["artifacts"], blobs, dirty)
    result = {
        "check": "sf-audit-immutability",
        "registry": os.path.relpath(REGISTRY, REPO).replace(os.sep, "/"),
        "registered": len(reg["artifacts"]),
        "head": git("rev-parse", "HEAD").stdout.strip(),
        "failures": failures,
        "status": "FAIL" if failures else "PASS",
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    io.open(OUT, "w", encoding="utf-8", newline="\n").write(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    for f in failures:
        print(f"[IMMUTABILITY] {f}")
    print(f"audit immutability: {result['status']} "
          f"({len(reg['artifacts'])} registered, {len(failures)} failures)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
