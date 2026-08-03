#!/usr/bin/env python3
"""Materialize Git LFS pointers even when upstream .gitattributes is incomplete."""

from __future__ import annotations

import argparse
import hashlib
import os
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path


POINTER_PREFIX = b"version https://git-lfs.github.com/spec/v1\n"
OID_PATTERN = re.compile(rb"^oid sha256:([0-9a-f]{64})$", re.MULTILINE)
SIZE_PATTERN = re.compile(rb"^size ([0-9]+)$", re.MULTILINE)


@dataclass(frozen=True)
class Pointer:
    path: Path
    relative: str
    oid: str
    size: int


def parse_pointer(path: Path, repo: Path) -> Pointer | None:
    if path.is_symlink() or not path.is_file() or path.stat().st_size >= 1024:
        return None
    content = path.read_bytes().replace(b"\r\n", b"\n")
    if not content.startswith(POINTER_PREFIX):
        return None
    oid_match = OID_PATTERN.search(content)
    size_match = SIZE_PATTERN.search(content)
    if not oid_match or not size_match:
        raise ValueError(f"malformed Git LFS pointer: {path}")
    return Pointer(
        path=path,
        relative=path.relative_to(repo).as_posix(),
        oid=oid_match.group(1).decode("ascii"),
        size=int(size_match.group(1)),
    )


def find_pointers(repo: Path, roots: list[str]) -> list[Pointer]:
    result: list[Pointer] = []
    for root_text in roots:
        root = (repo / root_text).resolve()
        try:
            root.relative_to(repo)
        except ValueError as error:
            raise ValueError(f"root escapes repository: {root_text}") from error
        if not root.exists():
            raise FileNotFoundError(root)
        paths = root.rglob("*") if root.is_dir() else [root]
        for path in paths:
            pointer = parse_pointer(path, repo)
            if pointer:
                result.append(pointer)
    return sorted(result, key=lambda item: item.relative)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def materialize(repo: Path, pointer: Pointer) -> tuple[str, str]:
    temporary = pointer.path.with_name(pointer.path.name + ".speechrl-lfs.part")
    environment = os.environ.copy()
    environment.pop("GIT_LFS_SKIP_SMUDGE", None)
    with pointer.path.open("rb") as source, temporary.open("wb") as destination:
        process = subprocess.run(
            ["git", "-C", str(repo), "lfs", "smudge", pointer.relative],
            stdin=source,
            stdout=destination,
            stderr=subprocess.PIPE,
            env=environment,
            check=False,
        )
    if process.returncode != 0:
        return pointer.relative, process.stderr.decode("utf-8", errors="replace").strip()
    if temporary.stat().st_size != pointer.size:
        return pointer.relative, (
            f"size mismatch: expected {pointer.size}, got {temporary.stat().st_size}"
        )
    if sha256(temporary) != pointer.oid:
        return pointer.relative, "SHA-256 mismatch"
    os.replace(temporary, pointer.path)
    return pointer.relative, "OK"


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser()
    result.add_argument("repo", type=Path)
    result.add_argument("roots", nargs="+", help="repository-relative paths to scan")
    result.add_argument("--jobs", type=int, default=8)
    result.add_argument("--dry-run", action="store_true")
    return result


def main() -> int:
    args = parser().parse_args()
    repo = args.repo.resolve()
    if not (repo / ".git").exists():
        raise SystemExit(f"not a Git checkout: {repo}")
    if args.jobs < 1:
        raise SystemExit("--jobs must be >= 1")
    try:
        pointers = find_pointers(repo, args.roots)
    except (OSError, ValueError) as error:
        print(f"ERROR {error}", file=sys.stderr)
        return 2
    print(
        f"pointers={len(pointers)} bytes={sum(pointer.size for pointer in pointers)}",
        flush=True,
    )
    if args.dry_run or not pointers:
        for pointer in pointers:
            print(f"{pointer.relative}\t{pointer.size}\t{pointer.oid}")
        return 0

    failures = 0
    with ThreadPoolExecutor(max_workers=args.jobs) as executor:
        futures = {
            executor.submit(materialize, repo, pointer): pointer for pointer in pointers
        }
        for future in as_completed(futures):
            relative, detail = future.result()
            print(f"{relative}\t{detail}", flush=True)
            failures += int(detail != "OK")
    remaining = find_pointers(repo, args.roots)
    print(
        f"materialize summary: selected={len(pointers)} failures={failures} "
        f"remaining_pointers={len(remaining)}"
    )
    return int(failures != 0 or bool(remaining))


if __name__ == "__main__":
    raise SystemExit(main())
