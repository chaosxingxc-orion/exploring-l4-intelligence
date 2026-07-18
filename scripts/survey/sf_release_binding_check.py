#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Release-binding check (v8 doctoral review Gate MAJOR-2, §5.5 last paragraph).

A dated reviewer-facing artifact that quotes headline occupancy numbers must
carry a machine-readable binding block:

  <!-- release_binding: {"source": "docs/checks/<test-output>.json",
       "reward_guided": "6/11", "rq_sys_compatible": "5/11",
       "method_candidate": "0/11", "reward_guided_selection": "4/11",
       "trajectory_pool": "2/11"} -->

This script parses the block from every bound artifact and compares each
value against the referenced persisted test output. Stale prose numbers fail
— data can no longer change while a dated artifact keeps quoting old
headlines. Self-test: an in-memory fixture with a wrong value must be
flagged (oracle-can-fail), else exit 1.

Bound artifacts are listed in BOUND (update when a new dated submission or
response letter is published).
"""
import io
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BOUND = [
    "wiki/survey/2026-07-19-gate-s1-v8-response.md",
    "wiki/2026-07-19-system-first-research-proposal-v9-consolidated.md",
]
BLOCK = re.compile(r"<!--\s*release_binding:\s*(\{.*?\})\s*-->", re.S)

KEYMAP = {
    "reward_guided": lambda occ: occ["policy_A"]["is_reward_guided"]["n_paths"],
    "rq_sys_compatible": lambda occ: occ["policy_A"]["is_rq_sys_control_compatible"]["n_paths"],
    "method_candidate": lambda occ: occ["policy_A"]["is_project_method_candidate"]["n_paths"],
    "reward_guided_selection": lambda occ: occ["policy_A"]["reward_guided_selection"]["n_paths"],
    "trajectory_pool": lambda occ: occ["policy_A"][
        "strict_AND_reward_AND_pool_BY_selection_object(mechanism)"].get(
        "trajectory", {}).get("n_paths", "0/?"),
}


def check_artifact(text, name, cache):
    fails = []
    m = BLOCK.search(text)
    if not m:
        return [f"{name}: release_binding block missing"]
    try:
        binding = json.loads(m.group(1))
    except json.JSONDecodeError as e:
        return [f"{name}: release_binding unparsable: {e}"]
    src = binding.get("source")
    if not src:
        return [f"{name}: release_binding lacks source"]
    if src not in cache:
        p = os.path.join(REPO, src.replace("/", os.sep))
        cache[src] = json.load(io.open(p, encoding="utf-8")) if os.path.exists(p) else None
    report = cache[src]
    if report is None:
        return [f"{name}: bound source missing: {src}"]
    occ = report.get("occupancy", {})
    if report.get("verdict") != "PASS":
        fails.append(f"{name}: bound test output verdict is {report.get('verdict')} (must be PASS)")
    for k, v in binding.items():
        if k == "source":
            continue
        fn = KEYMAP.get(k)
        if fn is None:
            fails.append(f"{name}: unknown binding key {k}")
            continue
        actual = fn(occ)
        if actual != v:
            fails.append(f"{name}: {k} declared {v} but generated output says {actual}")
    return fails


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    cache = {}
    # oracle-can-fail proof: wrong declared value must be flagged
    fixture = ('<!-- release_binding: {"source": "docs/checks/2026-07-19-sf-identity-taxonomy-v5-test.json", '
               '"reward_guided": "999/11"} -->')
    if not any("declared 999/11" in f for f in check_artifact(fixture, "<fixture>", cache)):
        print("[FAIL] negative fixture NOT flagged — release-binding oracle broken")
        return 1
    all_fails = []
    for rel in BOUND:
        p = os.path.join(REPO, rel.replace("/", os.sep))
        if not os.path.exists(p):
            print(f"[skip] {rel} (missing)")
            continue
        all_fails += check_artifact(io.open(p, encoding="utf-8").read(), rel, cache)
    for f in all_fails:
        print(f"[BINDING] {f}")
    print(f"release binding: {'FAIL' if all_fails else 'PASS'} ({len(all_fails)} failures)")
    return 1 if all_fails else 0


if __name__ == "__main__":
    sys.exit(main())
