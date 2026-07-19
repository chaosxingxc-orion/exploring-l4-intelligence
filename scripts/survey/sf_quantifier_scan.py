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
  python scripts/survey/sf_quantifier_scan.py [--manifest PATH] [file ...]
Default file set = ``prose_scan_paths`` in the current manifest. Positional
files bypass the manifest only for focused diagnostics.
"""
import argparse
import re
import sys
from pathlib import Path

from sf_current_manifest import (
    CurrentManifestError,
    canonical_consumer_path,
    load_consumer_manifest,
)


REPO = Path(__file__).resolve().parents[2]
DEFAULT_MANIFEST = "wiki/survey/current/manifest.json"
TOKEN = re.compile(r"全量|唯一|零项|持续缺位")
SCOPE = re.compile(
    r"已检视|下界|集合|快照|机器重算|机器可数|合取|每查询|主类目|"
    r"独立复核唯一\s+MAJOR|"
    r"≥|>=|〔SCOPED〕|〔HIST:|不称|禁止|不再|禁用|撤回|矛盾|forbidden"
)
NEG_FIXTURE = "本项目对该问题的解决是全量且唯一的。"


def scan_text(name, text):
    hits = []
    for i, line in enumerate(text.splitlines(), 1):
        if TOKEN.search(line) and not SCOPE.search(line):
            hits.append((name, i, line.strip()[:90]))
    return hits


def _parser():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest")
    parser.add_argument("files", nargs="*")
    return parser


def main(argv=None, *, repo=REPO):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = _parser()
    args = parser.parse_args(argv)
    if args.manifest is not None and args.files:
        parser.error("--manifest cannot be combined with focused positional files")
    if not scan_text("<fixture>", NEG_FIXTURE):
        print("[FAIL] negative fixture NOT flagged — scanner oracle broken")
        return 1

    repo = Path(repo)
    try:
        if args.files:
            from ai_context_surface_check import TrustedRepoReader

            reader = TrustedRepoReader(repo)
            files = tuple(
                canonical_consumer_path(path, label="focused prose path")
                for path in args.files
            )
            read_bytes = reader.read_bytes
            scope = "focused-positional"
        else:
            manifest_path = (
                DEFAULT_MANIFEST if args.manifest is None else args.manifest
            )
            view = load_consumer_manifest(repo, manifest_path)
            files = view.paths("prose_scan_paths")
            read_bytes = view.read_bytes
            scope = "current-manifest"
    except (CurrentManifestError, OSError, ValueError) as error:
        print(f"[QUANTIFIER] manifest/path load failed: {error}")
        print("quantifier scan: FAIL (1 input failures, 0 unscoped)")
        return 1

    all_hits = []
    input_failures = []
    for f in files:
        try:
            text = read_bytes(f).decode("utf-8")
        except (CurrentManifestError, OSError, UnicodeDecodeError, ValueError) as error:
            input_failures.append(f"{f}: missing, invalid, or untrusted: {error}")
            continue
        all_hits += scan_text(f, text)
    for failure in input_failures:
        print(f"[QUANTIFIER] {failure}")
    for name, i, line in all_hits:
        print(f"[UNSCOPED] {name}:{i}: {line}")
    failed = bool(input_failures or all_hits)
    print(
        f"quantifier scan: {'FAIL' if failed else 'PASS'} "
        f"({len(input_failures)} input failures, {len(all_hits)} unscoped; "
        f"scope={scope})"
    )
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
