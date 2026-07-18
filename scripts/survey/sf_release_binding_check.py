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
    "wiki/survey/2026-07-19-gate-s1-v9-response.md",
]
BLOCK = re.compile(r"<!--\s*release_binding:\s*(\{.*?\})\s*-->", re.S)
GEN_BLOCK = re.compile(r"<!--\s*generated_headline_begin\s*-->(.*?)<!--\s*generated_headline_end\s*-->", re.S)


def render_headline(report):
    """Canonical reader-visible headline table, rendered from the persisted
    test output (v9-review P0-C: the prose table is GENERATED, never hand
    copied; the checker re-renders and byte-compares)."""
    occ = report["occupancy"]["policy_A"]
    pool = occ["strict_AND_reward_AND_pool_BY_selection_object(mechanism)"]
    rows = [
        ("is_reward_guided", occ["is_reward_guided"]["n_paths"],
         occ["is_reward_guided"]["n_works"]),
        ("is_rq_sys_control_compatible", occ["is_rq_sys_control_compatible"]["n_paths"],
         occ["is_rq_sys_control_compatible"]["n_works"]),
        ("is_project_method_candidate", occ["is_project_method_candidate"]["n_paths"],
         occ["is_project_method_candidate"]["n_works"]),
        ("reward_guided_selection", occ["reward_guided_selection"]["n_paths"],
         occ["reward_guided_selection"]["n_works"]),
        ("strict∧reward∧pool (trajectory)", pool.get("trajectory", {}).get("n_paths", "0/?"),
         pool.get("trajectory", {}).get("n_works", "0/?")),
    ]
    lines = ["| 派生量 | method-path 分母 | unique-work 分母 |", "|---|---|---|"]
    lines += [f"| {k} | {p} | {w} |" for k, p, w in rows]
    return "\n".join(lines)

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
    # v9-review P0-C: if the artifact carries a generated headline block, the
    # reader-visible table must byte-match a fresh render from the bound source.
    for gm in GEN_BLOCK.finditer(text):
        want = render_headline(report).strip()
        got = gm.group(1).strip()
        if got != want:
            fails.append(f"{name}: generated headline block differs from fresh render "
                         f"(reader-visible numbers are stale or hand-edited)")
    return fails


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    cache = {}
    # oracle-can-fail proofs: wrong declared value AND a hand-edited generated
    # block must both be flagged
    src = "docs/checks/2026-07-19-sf-identity-taxonomy-v5-test.json"
    fixture = (f'<!-- release_binding: {{"source": "{src}", "reward_guided": "999/11"}} -->')
    if not any("declared 999/11" in f for f in check_artifact(fixture, "<fixture>", cache)):
        print("[FAIL] negative fixture NOT flagged — release-binding oracle broken")
        return 1
    if cache.get(src):
        good = render_headline(cache[src]).replace("6/11", "99/11", 1)
        fixture2 = (f'<!-- release_binding: {{"source": "{src}"}} -->\n'
                    f"<!-- generated_headline_begin -->\n{good}\n<!-- generated_headline_end -->")
        if not any("generated headline block differs" in f
                   for f in check_artifact(fixture2, "<fixture2>", cache)):
            print("[FAIL] prose-block fixture NOT flagged — E5 oracle broken")
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
