#!/usr/bin/env python
"""RI-G0 evidence-freeze inventory.

Walks a configured list of roots (umbrella proofs/, papers/, docs/; W1 _repro/;
W4 _repro/; and, if reachable, the E: drive's speechrl-data/_repro and
speechrl-data/mlruns) and emits a read-only JSON manifest: for every file,
{relpath, size, mtime_iso, sha256}, except files bigger than 1GB, which get
{size, mtime_iso, sha256: null, note: 'size-only (>1GB)'} instead of being
hashed.

Purpose (RI-G0, wiki/2026-07-10-research-integrity-forensic-audit.md): let an
independent reviewer or a later AI locate the exact bytes behind any headline
number, and detect any post-freeze tamper (re-run this script, diff the two
manifests; any changed sha256 for an existing relpath is a red flag that must
be explained and logged, never silently accepted).

This script only reads and hashes; it never modifies, deletes, or renames
anything it walks.

Usage:
    python scripts/evidence_freeze.py --timestamp 2026-07-11T02:00:00+08:00

    # override output path / excluded dirs / roots if needed
    python scripts/evidence_freeze.py --timestamp ... --out _repro/foo.json \\
        --exclude-dir .lake --exclude-dir __pycache__
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import socket
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ONE_GB = 1024 ** 3

# Directory basenames skipped everywhere by default: regenerable build/vcs/
# cache directories that are not themselves research evidence. Most notably
# proofs/tfrl/.lake/ is a gitignored Lean/Mathlib build cache (~121k files,
# ~7GB) that is fully reproducible from proofs/tfrl/lake-manifest.json and
# carries no forensic value for this audit; walking+hashing it would dominate
# the run for no benefit. Override with --exclude-dir (repeatable) / --no-default-excludes.
DEFAULT_EXCLUDE_DIRS = {
    ".git",
    ".lake",
    "__pycache__",
    ".venv",
    "venv",
    "node_modules",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
}

# (label, path) — label is the manifest-relpath prefix so entries are
# unambiguous about which repo/root they came from regardless of absolute
# filesystem layout.
def default_roots(repo_root: Path) -> list[tuple[str, Path]]:
    w1 = repo_root / "projects" / "speech-mllm-training-free-rl"
    w4 = repo_root / "projects" / "speech-mllm-omni-embedding-rl"
    e_data = Path("E:/chao_workspace/exploring-l4-intelligence/speechrl-data")
    return [
        ("umbrella/proofs", repo_root / "proofs"),
        ("umbrella/papers", repo_root / "papers"),
        ("umbrella/docs", repo_root / "docs"),
        ("W1/_repro", w1 / "_repro"),
        ("W4/_repro", w4 / "_repro"),
        ("E/_repro", e_data / "_repro"),
        ("E/mlruns", e_data / "mlruns"),
    ]


def git_head(repo_dir: Path) -> str:
    if not repo_dir.exists():
        return "UNAVAILABLE (path missing)"
    try:
        out = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=str(repo_dir),
            capture_output=True,
            text=True,
            check=True,
        )
        return out.stdout.strip()
    except Exception as e:  # noqa: BLE001 - best-effort header field
        return f"UNAVAILABLE ({e})"


def sha256_file(path: Path, buf_size: int = 4 * 1024 * 1024) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(buf_size)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def mtime_iso(st: os.stat_result) -> str:
    return datetime.fromtimestamp(st.st_mtime, tz=timezone.utc).isoformat()


def walk_root(label: str, root_path: Path, exclude_dirs: set[str]):
    """Returns (entries, status) where status is 'OK' or 'MISSING'."""
    entries = []
    if not root_path.exists():
        return entries, "MISSING"
    for dirpath, dirnames, filenames in os.walk(root_path):
        dirnames[:] = [d for d in dirnames if d not in exclude_dirs]
        for fname in sorted(filenames):
            fpath = Path(dirpath) / fname
            relpath = f"{label}/{fpath.relative_to(root_path).as_posix()}"
            try:
                st = fpath.stat()
            except OSError as e:
                entries.append({"relpath": relpath, "error": str(e)})
                continue
            size = st.st_size
            entry = {"relpath": relpath, "size": size, "mtime_iso": mtime_iso(st)}
            if size > ONE_GB:
                entry["sha256"] = None
                entry["note"] = "size-only (>1GB)"
            else:
                try:
                    entry["sha256"] = sha256_file(fpath)
                except OSError as e:
                    entry["sha256"] = None
                    entry["note"] = f"unreadable: {e}"
            entries.append(entry)
    return entries, "OK"


def parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--timestamp",
        required=True,
        help="PLANNED label stamped into the manifest header as 'planned_label' (ISO-8601, e.g. "
        "2026-07-11T02:00:00+08:00) -- a coordinator/human-supplied planning tag, hand-typed, NOT "
        "read from the system clock (2026-07-12, RI item 11: this field was previously named "
        "'generated_at' and conflated with the actual observation time; a prior forensic finding "
        "noted 'freeze 时间戳为手填标签' -- the freeze timestamp was a hand-filled label. Fixed by "
        "separating this planned label from 'observed_at_utc' below, which IS read from the "
        "system clock at the moment this script actually runs).",
    )
    p.add_argument(
        "--out",
        default=None,
        help="output manifest path, relative to the umbrella repo root unless absolute. "
        "Default: _repro/evidence_freeze_<YYYYMMDD from --timestamp>.json",
    )
    p.add_argument(
        "--exclude-dir",
        action="append",
        default=[],
        help="additional directory basename to skip while walking (repeatable).",
    )
    p.add_argument(
        "--no-default-excludes",
        action="store_true",
        help="do not skip the built-in build/vcs/cache directory list (.git, .lake, "
        "__pycache__, venvs, ...); only --exclude-dir entries are skipped.",
    )
    return p.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    repo_root = Path(__file__).resolve().parent.parent

    exclude_dirs = set(args.exclude_dir)
    if not args.no_default_excludes:
        exclude_dirs |= DEFAULT_EXCLUDE_DIRS

    if args.out:
        out_path = Path(args.out)
        if not out_path.is_absolute():
            out_path = repo_root / out_path
    else:
        date_tag = args.timestamp[:10].replace("-", "")
        out_path = repo_root / "_repro" / f"evidence_freeze_{date_tag}.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    w1_root = repo_root / "projects" / "speech-mllm-training-free-rl"
    w4_root = repo_root / "projects" / "speech-mllm-omni-embedding-rl"

    # 2026-07-12 (RI item 11): git heads are captured HERE, at the moment of this walk/observation
    # (same as before -- git_head() always ran live), now under a name that says so explicitly and
    # paired with observed_at_utc (the same moment, from the real system clock) rather than only
    # the hand-typed planned_label.
    git_heads_at_observation = {
        "umbrella": git_head(repo_root),
        "W1_speech-mllm-training-free-rl": git_head(w1_root),
        "W4_speech-mllm-omni-embedding-rl": git_head(w4_root),
    }
    observed_at_utc = datetime.now(timezone.utc).isoformat()

    header = {
        # 2026-07-12 (RI item 11, forensic finding "freeze 时间戳为手填标签"): separated fields --
        # `planned_label` is the hand-supplied --timestamp (a planning tag, may be typed ahead of
        # or after the actual run; NOT authoritative); `observed_at_utc` is the REAL system clock
        # reading at the moment this script executed the walk; `git_heads_at_observation` are the
        # repo HEADs read at that same moment. `generated_at` is kept, set equal to `planned_label`,
        # ONLY for backward compatibility with the pre-2026-07-12 manifest schema (e.g.
        # _repro/evidence_freeze_20260711.json) -- new consumers should read the three fields
        # above, not `generated_at`.
        "planned_label": args.timestamp,
        "observed_at_utc": observed_at_utc,
        "git_heads_at_observation": git_heads_at_observation,
        "generated_at": args.timestamp,  # deprecated alias of planned_label -- see comment above
        "git_heads": git_heads_at_observation,  # deprecated alias of git_heads_at_observation
        "hostname": socket.gethostname(),
        "excluded_dirs": sorted(exclude_dirs),
        "one_gb_threshold_bytes": ONE_GB,
        "script": "scripts/evidence_freeze.py",
    }

    roots = default_roots(repo_root)
    all_entries: list[dict] = []
    root_status = []
    for label, root_path in roots:
        entries, status = walk_root(label, root_path, exclude_dirs)
        root_status.append({"label": label, "path": str(root_path), "status": status, "n_files": len(entries)})
        all_entries.extend(entries)
        print(f"[{status}] {label} ({root_path}) -> {len(entries)} files", file=sys.stderr)

    header["roots"] = root_status

    total_bytes = sum(e.get("size", 0) for e in all_entries)
    hashed_bytes = sum(e.get("size", 0) for e in all_entries if e.get("sha256"))
    size_only = [e for e in all_entries if e.get("size", 0) > ONE_GB]
    summary = {
        "n_files": len(all_entries),
        "total_bytes": total_bytes,
        "hashed_bytes": hashed_bytes,
        "size_only_count": len(size_only),
        "error_count": sum(1 for e in all_entries if "error" in e),
    }
    header["summary"] = summary

    manifest = {"header": header, "files": all_entries}

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print(f"Wrote manifest: {out_path}", file=sys.stderr)
    print(json.dumps(summary, indent=2), file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
