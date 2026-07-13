#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/checks/build_release_manifest.py -> docs/integrity/release_manifest.json (2026-07-13,
ticket #38 item 4, v4.2 doctoral review §6 P0_INTEGRITY_FREEZE `required_artifacts` +
M-8 "今后 release manifest 必须列各 repo SHA，并由脚本从该 SHA fresh checkout 重建状态表").

Records, for THIS run:
  - repo SHAs of umbrella + W1 (+ any other project repo passed via --extra-repo), each with its
    OWN dirty flag (`git status --porcelain` non-empty) -- the review's M-8 finding was exactly a
    release-snapshot / actual-repo-state mismatch (a commit subject saying "converged" while a
    contemporaneous doc snapshot said "现有 4 errors"); this manifest exists so that mismatch is
    mechanically checkable going forward, not narrated by hand.
  - the STANDARD test entry result: `PYTHONPATH=src pytest -q` run for real, inside W1, captured
    verbatim (never assumed/copied from a prior report).
  - the checker verdict: `scripts/checks/v42_conformance.py` re-run for real against
    `docs/checks/v42-rules.yaml` (if both are present) -- its own `summary.overall_verdict` folded
    in verbatim; this manifest does NOT re-implement conformance-checking logic, only re-invokes
    the existing checker and records what it said.
  - key artifact hashes: sha256 of the outputs this remediation package produces/depends on
    (docs/corpus.lock.json, docs/claim_ledger.yaml, the sibling P0 registers) — each is None (not
    "0000...") when the file does not exist, so a missing artifact is never mistaken for a hashed
    empty one.

Usage (WSL venv):
    python scripts/checks/build_release_manifest.py --umbrella-root . \\
        --w1-root projects/speech-mllm-training-free-rl \\
        --out docs/integrity/release_manifest.json
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import os
import subprocess
import sys


def _utc_now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def git_sha_of(repo_root: str) -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=repo_root, text=True
        ).strip()
    except Exception as exc:  # pragma: no cover
        return "UNKNOWN (%s)" % exc


def git_dirty_of(repo_root: str):
    try:
        out = subprocess.check_output(["git", "status", "--porcelain"], cwd=repo_root, text=True)
        return bool(out.strip())
    except Exception:  # pragma: no cover
        return None


def git_dirty_files(repo_root: str, limit: int = 40):
    try:
        out = subprocess.check_output(["git", "status", "--porcelain"], cwd=repo_root, text=True)
        lines = [l for l in out.splitlines() if l.strip()]
        return lines[:limit]
    except Exception:  # pragma: no cover
        return None


def sha256_of(path: str):
    if not os.path.isfile(path):
        return None
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_of_blob(repo_root: str, relpath: str):
    """SHA-256 over the git BLOB bytes at HEAD -- the repo's CANONICAL hash convention
    (2026-07-13 self-check finding: Windows working trees can hold CRLF copies of
    LF-normalized text files, so on-disk hashes produce non-reproducible variants that a
    clean clone cannot verify; `git show HEAD:<path> | sha256sum` always reproduces the
    blob hash). Returns None when the path is not tracked at HEAD."""
    try:
        proc = subprocess.run(
            ["git", "-C", repo_root, "show", "HEAD:%s" % relpath],
            capture_output=True, timeout=60,
        )
        if proc.returncode != 0:
            return None
        return hashlib.sha256(proc.stdout).hexdigest()
    except Exception:  # pragma: no cover
        return None


def run_standard_test_entry(w1_root: str) -> dict:
    """Runs `PYTHONPATH=src pytest -q` FOR REAL inside W1 and captures the outcome verbatim --
    never copied from a prior/cached report (M-8's exact failure mode: a stale count quoted
    instead of a fresh re-check)."""
    env = dict(os.environ)
    env["PYTHONPATH"] = os.path.join(w1_root, "src")
    try:
        proc = subprocess.run(
            [sys.executable, "-m", "pytest", "-q"], cwd=w1_root, env=env,
            capture_output=True, text=True, timeout=3600,
        )
        stdout_tail = "\n".join(proc.stdout.strip().splitlines()[-15:])
        return {
            "command": "PYTHONPATH=src pytest -q",
            "cwd": w1_root,
            "returncode": proc.returncode,
            "passed": proc.returncode == 0,
            "stdout_tail": stdout_tail,
            "ran_at_utc": _utc_now(),
        }
    except Exception as exc:  # pragma: no cover
        return {"command": "PYTHONPATH=src pytest -q", "cwd": w1_root, "ran": False,
                 "error": str(exc)}


def run_conformance_checker(umbrella_root: str) -> dict:
    """Re-invokes the EXISTING scripts/checks/v42_conformance.py (if present) against
    docs/checks/v42-rules.yaml, for real -- never re-implements its logic here. Returns
    {"ran": False, "reason": ...} if either file is missing (this manifest generator must not
    itself require the v4.2 package to exist)."""
    checker = os.path.join(umbrella_root, "scripts", "checks", "v42_conformance.py")
    manifest = os.path.join(umbrella_root, "docs", "checks", "v42-rules.yaml")
    if not (os.path.isfile(checker) and os.path.isfile(manifest)):
        return {"ran": False, "reason": "v42_conformance.py or v42-rules.yaml not found"}
    try:
        proc = subprocess.run(
            [sys.executable, checker, "--manifest", manifest, "--root", umbrella_root],
            capture_output=True, text=True, timeout=600,
        )
        try:
            report = json.loads(proc.stdout)
        except Exception:
            report = None
        out = {
            "ran": True, "returncode": proc.returncode,
            "ran_at_utc": _utc_now(),
        }
        if report is not None:
            out["overall_verdict"] = report.get("summary", {}).get("overall_verdict")
            out["total_rules"] = report.get("summary", {}).get("total")
            out["failed_ids"] = report.get("summary", {}).get("failed_ids")
        else:
            out["stdout_tail"] = "\n".join(proc.stdout.strip().splitlines()[-10:])
        return out
    except Exception as exc:  # pragma: no cover
        return {"ran": False, "reason": str(exc)}


def key_artifact_hashes(umbrella_root: str, w1_root: str) -> dict:
    """Canonical (git-blob-at-HEAD) hashes of the key artifacts. `hash_basis` records the
    convention explicitly so a verifier knows to use `git show HEAD:<path> | sha256sum`,
    never an on-disk read that may see platform EOL variants."""
    candidates = {
        "docs/corpus.lock.json": (umbrella_root, "docs/corpus.lock.json"),
        "docs/claim_ledger.yaml": (umbrella_root, "docs/claim_ledger.yaml"),
        "docs/integrity/prior_exposure_registry.json":
            (umbrella_root, "docs/integrity/prior_exposure_registry.json"),
        "docs/integrity/experiment_attempt_registry.jsonl":
            (umbrella_root, "docs/integrity/experiment_attempt_registry.jsonl"),
        "docs/integrity/discrepancy_register.md":
            (umbrella_root, "docs/integrity/discrepancy_register.md"),
        "projects/speech-mllm-training-free-rl/scripts/knowledge/corpus_lock.py":
            (w1_root, "scripts/knowledge/corpus_lock.py"),
        "projects/speech-mllm-training-free-rl/scripts/baselines/deterministic_draw.py":
            (w1_root, "scripts/baselines/deterministic_draw.py"),
    }
    out = {}
    for rel, (repo_root, repo_rel) in candidates.items():
        blob = sha256_of_blob(repo_root, repo_rel)
        out[rel] = {
            "sha256": blob,
            "hash_basis": "git_blob_at_HEAD" if blob is not None else None,
            "exists": os.path.isfile(os.path.join(repo_root, repo_rel)),
        }
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--umbrella-root", default=".")
    ap.add_argument("--w1-root", default="projects/speech-mllm-training-free-rl")
    ap.add_argument("--out", default="docs/integrity/release_manifest.json")
    ap.add_argument("--extra-repo", action="append", default=[],
                     help="repeatable: name=relpath of an additional project repo to record "
                          "(e.g. W2/W3/W4) -- not required, this remediation package only touches "
                          "W1")
    ap.add_argument("--skip-tests", action="store_true",
                     help="debug only: skip the (slow, real) standard pytest re-run")
    args = ap.parse_args()

    umbrella_root = os.path.abspath(args.umbrella_root)
    w1_root = args.w1_root if os.path.isabs(args.w1_root) else os.path.join(umbrella_root, args.w1_root)
    out_path = args.out if os.path.isabs(args.out) else os.path.join(umbrella_root, args.out)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    repos = {
        "umbrella": {
            "path": ".", "sha": git_sha_of(umbrella_root), "dirty": git_dirty_of(umbrella_root),
            "dirty_files": git_dirty_files(umbrella_root),
        },
        "W1_speech-mllm-training-free-rl": {
            "path": os.path.relpath(w1_root, umbrella_root).replace("\\", "/"),
            "sha": git_sha_of(w1_root), "dirty": git_dirty_of(w1_root),
            "dirty_files": git_dirty_files(w1_root),
        },
    }
    for spec in args.extra_repo:
        name, _, relpath = spec.partition("=")
        abspath = relpath if os.path.isabs(relpath) else os.path.join(umbrella_root, relpath)
        repos[name] = {
            "path": relpath, "sha": git_sha_of(abspath), "dirty": git_dirty_of(abspath),
            "dirty_files": git_dirty_files(abspath),
        }

    standard_test_entry = (
        {"ran": False, "reason": "--skip-tests"} if args.skip_tests
        else run_standard_test_entry(w1_root)
    )
    checker_verdict = run_conformance_checker(umbrella_root)
    artifacts = key_artifact_hashes(umbrella_root, w1_root)

    manifest = {
        "_comment": ("P0 release manifest (2026-07-13, v4.2 doctoral review §6 "
                     "P0_INTEGRITY_FREEZE + M-8) -- repo SHAs/dirty-flags, the REAL standard-entry "
                     "test result, the REAL conformance-checker verdict, and key artifact hashes, "
                     "ALL captured live by this run (never copied from a prior report). Regenerate "
                     "with `python scripts/checks/build_release_manifest.py`."),
        "generated_at": _utc_now(),
        "generated_by": "scripts/checks/build_release_manifest.py",
        "repos": repos,
        "standard_test_entry": standard_test_entry,
        "conformance_checker": checker_verdict,
        "key_artifact_hashes": artifacts,
    }
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, ensure_ascii=False, indent=2, sort_keys=False)
        fh.write("\n")

    print(json.dumps({
        "out": out_path,
        "umbrella_sha": repos["umbrella"]["sha"], "umbrella_dirty": repos["umbrella"]["dirty"],
        "w1_sha": repos["W1_speech-mllm-training-free-rl"]["sha"],
        "w1_dirty": repos["W1_speech-mllm-training-free-rl"]["dirty"],
        "standard_test_entry_passed": standard_test_entry.get("passed"),
        "checker_overall_verdict": checker_verdict.get("overall_verdict"),
    }, indent=2, ensure_ascii=False))
    return 0 if standard_test_entry.get("passed", True) else 1


if __name__ == "__main__":
    sys.exit(main())
