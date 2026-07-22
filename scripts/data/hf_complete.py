#!/usr/bin/env python3
"""Diff an HF repo against local bytes and emit a pinned, Xet-safe aria2 manifest.

The primary recursive-tree API is efficient but some mirrors intermittently terminate its TLS
connection.  A metadata-rich repo-info call is the bounded fallback.  Both routes resolve a commit
SHA so downloads never float on ``main``.
"""

from __future__ import annotations

import os
import sys
import time
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import quote

from huggingface_hub import HfApi


def _info(api: HfApi, repo: str, repo_type: str, *, files_metadata: bool) -> Any:
    if repo_type == "dataset":
        return api.dataset_info(repo, files_metadata=files_metadata)
    return api.model_info(repo, files_metadata=files_metadata)


def list_remote_files(
    api: HfApi,
    repo: str,
    repo_type: str,
    *,
    retry_delays: tuple[float, ...] = (2, 5, 10, 20),
) -> tuple[str, list[tuple[str, int]]]:
    """Return resolved revision and regular files, with a repo-info TLS fallback."""

    try:
        entries = list(api.list_repo_tree(repo, repo_type=repo_type, recursive=True))
        files = [
            (entry.path, entry.size)
            for entry in entries
            if getattr(entry, "size", None) is not None
        ]
        revision = getattr(_info(api, repo, repo_type, files_metadata=False), "sha", None)
        return revision or "main", sorted(files)
    except Exception:  # noqa: BLE001 - the fallback is for transport/API failures
        last_error: Exception | None = None
        info = None
        for delay in (0, *retry_delays):
            if delay:
                time.sleep(delay)
            try:
                info = _info(api, repo, repo_type, files_metadata=True)
                break
            except Exception as error:  # noqa: BLE001 - bounded transport retry
                last_error = error
        if info is None:
            assert last_error is not None
            raise last_error
        files = [
            (sibling.rfilename, sibling.size)
            for sibling in info.siblings
            if getattr(sibling, "size", None) is not None
        ]
        return info.sha, sorted(files)


def write_missing_manifest(
    *,
    repo: str,
    repo_type: str,
    endpoint: str,
    revision: str,
    remote_files: Iterable[tuple[str, int]],
    destination: Path,
    output: Path,
) -> dict[str, int]:
    """Write only missing/short files and return deterministic completeness totals."""

    files = list(remote_files)
    missing: list[tuple[str, int]] = []
    total_bytes = have_bytes = 0
    have_files = 0
    for relative, size in files:
        total_bytes += size
        try:
            present = (destination / relative).stat().st_size == size
        except OSError:
            present = False
        if present:
            have_files += 1
            have_bytes += size
        else:
            missing.append((relative, size))

    prefix = "datasets/" if repo_type == "dataset" else ""
    encoded_revision = quote(revision, safe="")
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="\n") as handle:
        for relative, _ in missing:
            encoded_path = quote(relative, safe="/")
            handle.write(
                f"{endpoint}/{prefix}{repo}/resolve/{encoded_revision}/{encoded_path}\n"
            )
            parent = os.path.dirname(relative)
            if parent:
                handle.write(f"  dir={parent}\n")
            handle.write(f"  out={os.path.basename(relative)}\n")
            handle.write("  split=1\n  max-connection-per-server=1\n")

    missing_bytes = sum(size for _, size in missing)
    return {
        "total_files": len(files),
        "total_bytes": total_bytes,
        "have_files": have_files,
        "have_bytes": have_bytes,
        "missing_files": len(missing),
        "missing_bytes": missing_bytes,
    }


def main(argv: list[str] | None = None) -> int:
    arguments = sys.argv[1:] if argv is None else argv
    if len(arguments) not in {3, 4}:
        print(
            "usage: hf_complete.py <repo_id> <dest_dir> <out_list> [repo_type]",
            file=sys.stderr,
        )
        return 2
    repo, destination_text, output_text = arguments[:3]
    repo_type = arguments[3] if len(arguments) == 4 else "dataset"
    endpoint = os.environ.get("HF_ENDPOINT", "https://hf-mirror.com")
    retry_text = os.environ.get("HF_COMPLETE_RETRY_DELAYS")
    retry_delays = (
        tuple(float(value) for value in retry_text.split(",") if value.strip())
        if retry_text is not None
        else (2, 5, 10, 20)
    )
    api = HfApi(endpoint=endpoint)
    try:
        revision, files = list_remote_files(
            api,
            repo,
            repo_type,
            retry_delays=retry_delays,
        )
        summary = write_missing_manifest(
            repo=repo,
            repo_type=repo_type,
            endpoint=endpoint,
            revision=revision,
            remote_files=files,
            destination=Path(destination_text),
            output=Path(output_text),
        )
    except Exception as error:  # noqa: BLE001 - surface transport failures to the caller
        print(f"SUMMARY repo={repo} ERROR remote_metadata: {error}", file=sys.stderr)
        return 3
    print(
        f"SUMMARY repo={repo} revision={revision} "
        f"total_files={summary['total_files']} total_GB={summary['total_bytes']/1e9:.2f} "
        f"have={summary['have_files']} missing={summary['missing_files']} "
        f"missing_GB={summary['missing_bytes']/1e9:.2f}",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
