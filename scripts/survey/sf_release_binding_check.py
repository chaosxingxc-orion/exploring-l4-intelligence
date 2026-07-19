#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Release-binding check for manifest-selected current artifacts.

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

The default active set comes only from ``wiki/survey/current/manifest.json``.
The historical hard-coded set is available only through ``--legacy-regression``.
"""
import argparse
import json
import re
import sys
from pathlib import Path

from sf_current_manifest import (
    CurrentManifestError,
    canonical_consumer_path,
    load_consumer_manifest,
)
from sf_json_contract import JsonContractError, loads as strict_json_loads

REPO = Path(__file__).resolve().parents[2]
DEFAULT_MANIFEST = "wiki/survey/current/manifest.json"
LEGACY_BOUND = (
    "wiki/survey/2026-07-19-gate-s1-v8-response.md",
    "wiki/2026-07-19-system-first-research-proposal-v9-consolidated.md",
    "wiki/survey/2026-07-19-gate-s1-v9-response.md",
    "wiki/2026-07-19-system-first-research-proposal-v10-consolidated.md",
)
BLOCK = re.compile(r"<!--\s*release_binding:\s*(\{.*?\})\s*-->", re.S)
BINDING_MARKER = re.compile(r"<!--\s*release_binding\b")
HEADLINE_BEGIN = "<!-- generated_headline_begin -->"
HEADLINE_END = "<!-- generated_headline_end -->"
HEADLINE_BEGIN_COMMENT = re.compile(r"<!--\s*generated_headline_begin\b")
HEADLINE_END_COMMENT = re.compile(r"<!--\s*generated_headline_end\b")
GEN_BLOCK = re.compile(
    re.escape(HEADLINE_BEGIN) + r"(.*?)" + re.escape(HEADLINE_END), re.S
)


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
BINDING_KEYS = {"source", *KEYMAP}


def _read_report(src, cache, read_bytes, allowed_paths):
    if src in cache:
        return cache[src], None
    try:
        canonical_consumer_path(src, label="release_binding source")
    except CurrentManifestError as error:
        return None, str(error)
    if src.startswith("wiki/archive/"):
        return None, f"bound source points to archive path: {src}"
    if allowed_paths is not None and src not in allowed_paths:
        return None, f"bound source is absent from current manifest files: {src}"
    try:
        raw = read_bytes(src)
        report = strict_json_loads(raw, src)
    except (CurrentManifestError, JsonContractError, OSError, KeyError) as error:
        return None, f"bound source missing, invalid, or untrusted: {src}: {error}"
    if not isinstance(report, dict):
        return None, f"bound source root is not an object: {src}"
    cache[src] = report
    return report, None


def check_artifact(
    text,
    name,
    cache,
    *,
    read_bytes=None,
    allowed_paths=None,
    mode="current-manifest",
):
    fails = []
    if mode not in {"current-manifest", "legacy-compat"}:
        return [f"{name}: unknown release validation mode {mode!r}"]
    markers = list(BINDING_MARKER.finditer(text))
    blocks = list(BLOCK.finditer(text))
    if len(markers) != 1 or len(blocks) != 1:
        return [
            f"{name}: release_binding must be exactly one strict JSON comment "
            f"(markers={len(markers)}, strict_blocks={len(blocks)})"
        ]
    m = blocks[0]
    try:
        binding = strict_json_loads(
            m.group(1).encode("utf-8"), f"{name} release_binding"
        )
    except (JsonContractError, UnicodeEncodeError) as e:
        return [f"{name}: release_binding unparsable: {e}"]
    if not isinstance(binding, dict):
        return [f"{name}: release_binding must be an object"]
    if set(binding) != BINDING_KEYS:
        fails.append(
            f"{name}: release_binding keys must be exact: "
            f"expected {sorted(BINDING_KEYS)}, found {sorted(binding)}"
        )
    src = binding.get("source")
    if not isinstance(src, str) or not src:
        return [f"{name}: release_binding lacks source"]
    if read_bytes is None:
        def read_bytes(path):
            return REPO.joinpath(*path.split("/")).read_bytes()
    report, report_error = _read_report(src, cache, read_bytes, allowed_paths)
    if report_error:
        return [f"{name}: {report_error}"]
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
        try:
            actual = fn(occ)
        except (KeyError, TypeError, AttributeError) as error:
            fails.append(f"{name}: bound occupancy contract incomplete for {k}: {error}")
            continue
        if actual != v:
            fails.append(f"{name}: {k} declared {v} but generated output says {actual}")
    begin_comments = list(HEADLINE_BEGIN_COMMENT.finditer(text))
    end_comments = list(HEADLINE_END_COMMENT.finditer(text))
    headline_blocks = list(GEN_BLOCK.finditer(text))
    expected_counts = {1} if mode == "current-manifest" else {0, 1}
    marker_count_valid = (
        len(begin_comments) == len(end_comments)
        and len(begin_comments) in expected_counts
        and len(headline_blocks) == len(begin_comments)
        and text.count(HEADLINE_BEGIN) == len(begin_comments)
        and text.count(HEADLINE_END) == len(end_comments)
    )
    if not marker_count_valid:
        fails.append(
            f"{name}: generated headline markers must form an exact complete pair "
            f"for mode={mode} (begin={len(begin_comments)}, end={len(end_comments)}, "
            f"pairs={len(headline_blocks)})"
        )
        return fails

    for gm in headline_blocks:
        try:
            want = "\n" + render_headline(report) + "\n"
        except (KeyError, TypeError, AttributeError) as error:
            fails.append(f"{name}: cannot render generated headline: {error}")
            continue
        got = gm.group(1)
        if got != want:
            fails.append(
                f"{name}: generated headline block differs; body must exact-byte-match "
                f"fresh render "
                f"(reader-visible numbers are stale, hand-edited, or whitespace-drifted)"
            )
    return fails


def _oracle_report():
    return {
        "verdict": "PASS",
        "occupancy": {
            "policy_A": {
                "is_reward_guided": {"n_paths": "6/11", "n_works": "5/8"},
                "is_rq_sys_control_compatible": {
                    "n_paths": "5/11", "n_works": "4/8"
                },
                "is_project_method_candidate": {
                    "n_paths": "0/11", "n_works": "0/8"
                },
                "reward_guided_selection": {
                    "n_paths": "4/11", "n_works": "3/8"
                },
                "strict_AND_reward_AND_pool_BY_selection_object(mechanism)": {
                    "trajectory": {"n_paths": "2/11", "n_works": "1/8"}
                },
            }
        },
    }


def _run_oracle_fixtures():
    src = "docs/checks/oracle-fixture.json"
    cache = {src: _oracle_report()}
    fixture = "<!-- release_binding: " + json.dumps(
        {"source": src, "reward_guided": "999/11"},
        separators=(",", ":"),
    ) + " -->"
    if not any(
        "declared 999/11" in failure
        for failure in check_artifact(fixture, "<fixture>", cache)
    ):
        return "negative occupancy fixture NOT flagged - release-binding oracle broken"
    edited = render_headline(cache[src]).replace("6/11", "99/11", 1)
    fixture2 = (
        "<!-- release_binding: "
        + json.dumps({"source": src}, separators=(",", ":"))
        + " -->\n<!-- generated_headline_begin -->\n"
        + edited
        + "\n<!-- generated_headline_end -->"
    )
    if not any(
        "generated headline block differs" in failure
        for failure in check_artifact(fixture2, "<fixture2>", cache)
    ):
        return "edited-headline fixture NOT flagged - release-binding oracle broken"
    return None


def _parser():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--manifest")
    mode.add_argument("--legacy-regression", action="store_true")
    return parser


def main(argv=None, *, repo=REPO):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    args = _parser().parse_args(argv)
    oracle_error = _run_oracle_fixtures()
    if oracle_error:
        print(f"[FAIL] {oracle_error}")
        return 1

    repo = Path(repo)
    cache = {}
    try:
        if args.legacy_regression:
            from ai_context_surface_check import TrustedRepoReader

            reader = TrustedRepoReader(repo)
            paths = LEGACY_BOUND
            read_bytes = reader.read_bytes
            allowed_paths = None
            validation_mode = "legacy-compat"
        else:
            manifest_path = (
                DEFAULT_MANIFEST if args.manifest is None else args.manifest
            )
            view = load_consumer_manifest(repo, manifest_path)
            paths = view.paths("release_bound_artifacts")
            read_bytes = view.read_bytes
            allowed_paths = set(view.artifacts)
            validation_mode = "current-manifest"
    except (CurrentManifestError, OSError, ValueError) as error:
        print(f"[BINDING] manifest load failed: {error}")
        print("release binding: FAIL (1 failures)")
        return 1

    all_fails = []
    for rel in paths:
        try:
            raw = read_bytes(rel)
            text = raw.decode("utf-8")
        except (CurrentManifestError, OSError, UnicodeDecodeError, ValueError) as error:
            all_fails.append(f"{rel}: artifact missing, invalid, or untrusted: {error}")
            continue
        all_fails += check_artifact(
            text,
            rel,
            cache,
            read_bytes=read_bytes,
            allowed_paths=allowed_paths,
            mode=validation_mode,
        )
    for f in all_fails:
        print(f"[BINDING] {f}")
    print(
        f"release binding: {'FAIL' if all_fails else 'PASS'} "
        f"({len(all_fails)} failures; mode={validation_mode})"
    )
    return 1 if all_fails else 0


if __name__ == "__main__":
    sys.exit(main())
