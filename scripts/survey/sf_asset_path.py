#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Canonical asset-path resolver (v8 doctoral review Gate MAJOR-3 / P0-C).

Ledgers record asset paths as written on the platform that fetched them
(historically Windows drive paths like ``E:/...``). The repo's canonical
compute environment is WSL2 Ubuntu-24.04, where the same volume is mounted
at ``/mnt/e/...``. This module is the SINGLE place that maps between the
two, so every consumer (TeX quote verification, PDF page checks) reads the
same registered asset bytes on either platform.

Self-test: ``python scripts/survey/sf_asset_path.py`` exercises both
directions and exits non-zero on any mismatch (oracle-can-fail).
"""
import os
import re

_WIN_DRIVE = re.compile(r"^([A-Za-z]):[/\\](.*)$")
_WSL_MNT = re.compile(r"^/mnt/([A-Za-z])/(.*)$")


def resolve_asset_path(p, platform=None):
    """Map a registered asset path to the current (or given) platform.

    platform: "nt" or "posix"; defaults to os.name.
    Unrecognized shapes are returned unchanged (relative paths untouched).
    """
    plat = platform or os.name
    p = (p or "").strip()
    if plat == "nt":
        m = _WSL_MNT.match(p)
        if m:
            return f"{m.group(1).upper()}:/{m.group(2)}"
        return p
    m = _WIN_DRIVE.match(p)
    if m:
        return f"/mnt/{m.group(1).lower()}/{m.group(2).replace(chr(92), '/')}"
    return p


def _selftest():
    cases = [
        ("E:/data/x/y.eprint", "posix", "/mnt/e/data/x/y.eprint"),
        ("E:\\data\\x\\y.pdf", "posix", "/mnt/e/data/x/y.pdf"),
        ("/mnt/e/data/x/y.eprint", "nt", "E:/data/x/y.eprint"),
        ("E:/data/x/y.eprint", "nt", "E:/data/x/y.eprint"),
        ("/mnt/e/data/x/y.eprint", "posix", "/mnt/e/data/x/y.eprint"),
        ("relative/path.json", "posix", "relative/path.json"),
    ]
    bad = [(src, plat, want, resolve_asset_path(src, plat))
           for src, plat, want in cases if resolve_asset_path(src, plat) != want]
    if bad:
        for b in bad:
            print("[FAIL]", b)
        return 1
    print(f"resolver self-test: PASS ({len(cases)} cases)")
    return 0


if __name__ == "__main__":
    raise SystemExit(_selftest())
