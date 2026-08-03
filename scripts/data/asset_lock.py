#!/usr/bin/env python3
"""Validate, fetch and inventory assets from docs/datasets.lock.json only."""

from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_LOCK = ROOT / "docs" / "datasets.lock.json"
DEFAULT_DATA = Path(
    os.environ.get(
        "SPEECHRL_DATA_DIR",
        "/mnt/e/chao_workspace/exploring-l4-intelligence/speechrl-data",
    )
)
ALLOWED_STATUS = {"COMPLETE", "PARTIAL", "MISSING", "BLOCKED"}
ALLOWED_LIFECYCLE = {
    "FROZEN_BASELINE",
    "LOCAL_CANDIDATE",
    "STAGE2_CORE",
    "DIAGNOSTIC",
    "SECONDARY_CARRIER",
    "ANNOTATION_ONLY",
    "DERIVED",
    "DEFERRED",
    "RESTRICTED",
    "SOURCE_UNSTABLE",
    "UNAVAILABLE",
    "AUXILIARY",
}
FETCHABLE = {"hf", "modelscope", "git", "gdrive", "direct", "derived"}


def load_lock(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def assets(lock: dict[str, Any]) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for section, default_kind in (
        ("datasets", "dataset"),
        ("models", "model"),
        ("ref_repos", "ref-repo"),
    ):
        for raw in lock.get(section, []):
            item = dict(raw)
            item.setdefault("kind", default_kind)
            item.setdefault("lifecycle", "FROZEN_BASELINE")
            item.setdefault("profiles", ["frozen-baseline"])
            item.setdefault("status", "COMPLETE")
            result.append(item)
    for raw in lock.get("asset_catalog", []):
        item = dict(raw)
        item.setdefault("kind", "dataset")
        result.append(item)
    return result


def source_id(item: dict[str, Any]) -> str:
    source = item.get("source") or {}
    return str(source.get("id") or source.get("hf_id") or source.get("url") or "-")


def validate(lock: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if lock.get("schema") != "speechrl-asset-lock-v2":
        errors.append("schema must be speechrl-asset-lock-v2")
    profile_names = set((lock.get("profiles") or {}).keys())
    seen: set[tuple[str, str]] = set()
    for item in assets(lock):
        label = f"{item.get('kind')}:{item.get('name')}"
        key = (str(item.get("kind")), str(item.get("name")))
        if not item.get("name"):
            errors.append("asset without name")
            continue
        if key in seen:
            errors.append(f"duplicate identity: {label}")
        seen.add(key)
        if item.get("status") not in ALLOWED_STATUS:
            errors.append(f"{label}: invalid status {item.get('status')!r}")
        if item.get("lifecycle") not in ALLOWED_LIFECYCLE:
            errors.append(f"{label}: invalid lifecycle {item.get('lifecycle')!r}")
        if not item.get("local_subdir"):
            errors.append(f"{label}: missing local_subdir")
        for profile in item.get("profiles", []):
            if profile not in profile_names:
                errors.append(f"{label}: unknown profile {profile!r}")
        source = item.get("source") or {}
        method = source.get("kind")
        if not method:
            errors.append(f"{label}: missing source.kind")
        if method in {"hf", "git"} and item.get("lifecycle") != "FROZEN_BASELINE":
            revision = str(item.get("revision") or "")
            if len(revision) != 40 or any(c not in "0123456789abcdef" for c in revision):
                errors.append(f"{label}: {method} source needs a 40-hex revision")
        if method == "hf" and not source.get("id"):
            errors.append(f"{label}: hf source needs id")
        if method == "git" and not source.get("url"):
            errors.append(f"{label}: git source needs url")
        if method in {"restricted", "source-unstable", "unavailable"} and item.get("status") == "COMPLETE":
            errors.append(f"{label}: non-fetchable source cannot be COMPLETE")
    return errors


def selected_assets(
    lock: dict[str, Any], names: list[str], profile: str | None
) -> list[dict[str, Any]]:
    catalog = assets(lock)
    if names:
        wanted = set(names)
        selected = [item for item in catalog if item["name"] in wanted]
        missing = wanted - {item["name"] for item in selected}
        if missing:
            raise SystemExit(f"unknown asset name(s): {', '.join(sorted(missing))}")
        return selected
    profile = profile or "frozen-baseline"
    if profile not in (lock.get("profiles") or {}):
        raise SystemExit(f"unknown profile: {profile}")
    return [item for item in catalog if profile in item.get("profiles", [])]


def run(
    command: list[str],
    dry_run: bool = False,
    env: dict[str, str] | None = None,
    cwd: Path | None = None,
) -> None:
    print("+", " ".join(command), flush=True)
    if not dry_run:
        subprocess.run(command, check=True, env=env, cwd=cwd)


def marker_path(data_root: Path, item: dict[str, Any]) -> Path:
    local = data_root / item["local_subdir"]
    return local / ".speechrl-asset.json" if local.is_dir() else local.with_suffix(local.suffix + ".speechrl-asset.json")


def write_marker(data_root: Path, item: dict[str, Any], lock_path: Path) -> None:
    marker = marker_path(data_root, item)
    marker.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema": "speechrl-local-asset-receipt-v1",
        "name": item["name"],
        "kind": item["kind"],
        "revision": item.get("revision"),
        "source": item.get("source"),
        "completed_at": datetime.now(timezone.utc).isoformat(),
        "lockfile": str(lock_path),
    }
    marker.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def git_root(data_root: Path, item: dict[str, Any]) -> Path:
    source = item["source"]
    return data_root / source.get("checkout_root", item["local_subdir"])


def fetch_git(data_root: Path, item: dict[str, Any], dry_run: bool) -> None:
    source = item["source"]
    target = git_root(data_root, item)
    revision = item["revision"]
    if not (target / ".git").exists():
        target.parent.mkdir(parents=True, exist_ok=True)
        command = ["git", "clone"]
        if source.get("sparse_paths"):
            command += ["--filter=blob:none", "--no-checkout"]
        command += [source["url"], str(target)]
        env = os.environ.copy()
        if source.get("lfs_include"):
            env["GIT_LFS_SKIP_SMUDGE"] = "1"
        run(command, dry_run, env)
    run(["git", "-C", str(target), "fetch", "origin", revision], dry_run)
    if source.get("sparse_paths"):
        run(["git", "-C", str(target), "sparse-checkout", "init", "--cone"], dry_run)
        run(["git", "-C", str(target), "sparse-checkout", "set", *source["sparse_paths"]], dry_run)
    run(["git", "-C", str(target), "checkout", "--detach", revision], dry_run)
    local_attributes = source.get("local_lfs_attributes", [])
    if local_attributes:
        attributes_path = target / ".git" / "info" / "attributes"
        print(f"+ ensure local Git attributes: {attributes_path}", flush=True)
        if not dry_run:
            attributes_path.parent.mkdir(parents=True, exist_ok=True)
            existing = (
                attributes_path.read_text(encoding="utf-8").splitlines()
                if attributes_path.exists()
                else []
            )
            additions = [line for line in local_attributes if line not in existing]
            if additions:
                attributes_path.write_text(
                    "\n".join([*existing, *additions]) + "\n", encoding="utf-8"
                )
    if source.get("lfs_include"):
        run(
            ["git", "-C", str(target), "lfs", "pull", "--include", ",".join(source["lfs_include"])],
            dry_run,
        )
    if source.get("materialize_pointer_roots"):
        materializer = ROOT / "scripts" / "data" / "materialize_lfs_pointers.py"
        run(
            [
                sys.executable,
                str(materializer),
                str(target),
                *source["materialize_pointer_roots"],
                "--jobs",
                os.environ.get("SPEECHRL_LFS_JOBS", "8"),
            ],
            dry_run,
        )


def fetch_hf(data_root: Path, item: dict[str, Any], dry_run: bool) -> None:
    source = item["source"]
    target = data_root / item["local_subdir"]
    target.mkdir(parents=True, exist_ok=True)
    differ = ROOT / "scripts" / "data" / "hf_complete.py"
    aria2 = shutil.which("aria2c")
    if aria2 and differ.exists():
        manifest = target / ".hfd" / "missing.locked.txt"
        env = os.environ.copy()
        env["HF_ENDPOINT"] = os.environ.get(
            "SPEECHRL_HF_ENDPOINT", "https://huggingface.co"
        )
        env["HF_COMPLETE_REVISION"] = item["revision"]
        env["HF_COMPLETE_INCLUDE"] = ",".join(source.get("include", []))
        env["HF_COMPLETE_CONNECTIONS_PER_FILE"] = os.environ.get(
            "SPEECHRL_HFD_CONNECTIONS_PER_FILE", "1"
        )
        jobs = os.environ.get("SPEECHRL_HFD_JOBS", "16")
        for round_number in range(1, 5):
            run(
                [
                    sys.executable,
                    str(differ),
                    source["id"],
                    str(target),
                    str(manifest),
                    source.get("repo_type", "dataset"),
                ],
                dry_run,
                env,
                target,
            )
            if dry_run:
                return
            missing = sum(
                1
                for line in manifest.read_text(encoding="utf-8").splitlines()
                if line.startswith("http")
            )
            if missing == 0:
                print(f"HF complete after round {round_number - 1}: {item['name']}")
                return
            print(f"HF round {round_number}: {item['name']} missing_files={missing}")
            run(
                [
                    aria2,
                    "-i",
                    str(manifest),
                    "-j",
                    jobs,
                    "--auto-file-renaming=false",
                    "--allow-overwrite=true",
                    "--file-allocation=none",
                    "--console-log-level=warn",
                    "--summary-interval=20",
                    "--max-tries=10",
                    "--retry-wait=3",
                    "--connect-timeout=30",
                    "--timeout=120",
                ],
                dry_run,
                env,
                target,
            )
        raise RuntimeError(f"HF asset incomplete after 4 rounds: {item['name']}")
    cli = shutil.which("hf") or "hf"
    command = [
        cli,
        "download",
        source["id"],
        "--repo-type",
        source.get("repo_type", "dataset"),
        "--revision",
        item["revision"],
    ]
    for pattern in source.get("include", []):
        command += ["--include", pattern]
    command += ["--local-dir", str(target)]
    env = os.environ.copy()
    env.setdefault("HF_HUB_DISABLE_XET", "1")
    run(command, dry_run, env)


def fetch_modelscope(data_root: Path, item: dict[str, Any], dry_run: bool) -> None:
    source = item["source"]
    target = data_root / item["local_subdir"]
    target.mkdir(parents=True, exist_ok=True)
    flag = "--model" if item["kind"] == "model" else "--dataset"
    run(["modelscope", "download", flag, source["id"], "--local_dir", str(target)], dry_run)


def fetch_gdrive_file(file_id: str, output: Path, dry_run: bool) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    python = sys.executable
    run([python, "-m", "gdown", f"https://drive.google.com/uc?id={file_id}", "-O", str(output)], dry_run)


def fetch_direct(data_root: Path, item: dict[str, Any], dry_run: bool) -> None:
    target = data_root / item["local_subdir"]
    target.mkdir(parents=True, exist_ok=True)
    pending: list[dict[str, Any]] = []
    for remote in item["source"].get("files", []):
        output = target / remote["filename"]
        if output.exists():
            size_ok = (
                not remote.get("size_bytes")
                or remote["size_bytes"] == output.stat().st_size
            )
            hash_ok = governed_hash_ok(output, remote)
            if size_ok and hash_ok:
                print(f"skip verified local file: {output}")
                continue
        pending.append(remote)
    if not pending:
        return

    aria2 = shutil.which("aria2c")
    if aria2:
        manifest = target / ".hfd" / "direct.locked.txt"
        print(f"+ write pinned direct manifest: {manifest}", flush=True)
        if not dry_run:
            manifest.parent.mkdir(parents=True, exist_ok=True)
            target_resolved = target.resolve()
            with manifest.open("w", encoding="utf-8", newline="\n") as handle:
                for remote in pending:
                    output = (target / remote["filename"]).resolve()
                    if not output.is_relative_to(target_resolved):
                        raise RuntimeError(
                            f"direct filename escapes governed target: {remote['filename']}"
                        )
                    output.parent.mkdir(parents=True, exist_ok=True)
                    handle.write(f"{remote['url']}\n")
                    handle.write(f"  dir={output.parent}\n")
                    handle.write(f"  out={output.name}\n")
                    if remote.get("sha256"):
                        handle.write(f"  checksum=sha-256={remote['sha256']}\n")
                    elif remote.get("md5"):
                        handle.write(f"  checksum=md5={remote['md5']}\n")
        run(
            [
                aria2,
                "-i",
                str(manifest),
                "-j",
                os.environ.get("SPEECHRL_DIRECT_JOBS", "4"),
                "--continue=true",
                "--split",
                os.environ.get("SPEECHRL_DIRECT_SPLIT", "4"),
                "--max-connection-per-server",
                os.environ.get("SPEECHRL_DIRECT_SPLIT", "4"),
                "--auto-file-renaming=false",
                "--allow-overwrite=true",
                "--file-allocation=none",
                "--console-log-level=warn",
                "--summary-interval=20",
                "--max-tries=10",
                "--retry-wait=5",
                "--connect-timeout=30",
                "--timeout=120",
            ],
            dry_run,
            cwd=target,
        )
    else:
        for remote in pending:
            output = target / remote["filename"]
            run(
                [
                    "curl",
                    "-fL",
                    "--retry",
                    "5",
                    "-C",
                    "-",
                    "-o",
                    str(output),
                    remote["url"],
                ],
                dry_run,
                cwd=target,
            )

    if not dry_run:
        for remote in pending:
            output = target / remote["filename"]
            if not output.exists() or (
                remote.get("size_bytes")
                and output.stat().st_size != remote["size_bytes"]
            ):
                raise RuntimeError(f"direct file incomplete: {output}")
            if not governed_hash_ok(output, remote):
                raise RuntimeError(f"direct file checksum mismatch: {output}")


def fetch_attachments(data_root: Path, item: dict[str, Any], dry_run: bool) -> None:
    for attachment in item.get("source", {}).get("attachments", []):
        output = data_root / item["local_subdir"] / attachment["filename"]
        if attachment["kind"] == "gdrive":
            fetch_gdrive_file(attachment["id"], output, dry_run)
        elif attachment["kind"] == "direct":
            run(["curl", "-fL", "--retry", "5", "-C", "-", "-o", str(output), attachment["url"]], dry_run)
        else:
            raise RuntimeError(f"unsupported attachment kind: {attachment['kind']}")


def fetch_derived(data_root: Path, item: dict[str, Any], dry_run: bool) -> None:
    source = item["source"]
    script = ROOT / source["script"]
    command = [sys.executable, str(script)]
    for arg in source.get("args", []):
        command.append(arg.replace("${DATA_ROOT}", str(data_root)))
    run(command, dry_run)


def fetch_one(data_root: Path, item: dict[str, Any], lock_path: Path, dry_run: bool) -> None:
    source = item.get("source") or {}
    method = source.get("kind")
    observed, detail = verify_item(data_root, item)
    if item.get("status") == "COMPLETE" and observed == "COMPLETE":
        print(f"SKIP complete: {item['name']} ({detail})")
        return
    if method not in FETCHABLE:
        print(f"SKIP {item['name']}: source={method}, lifecycle={item['lifecycle']}")
        return
    print(f"FETCH {item['kind']}:{item['name']} [{method}] -> {item['local_subdir']}")
    if method == "git":
        fetch_git(data_root, item, dry_run)
    elif method == "hf":
        fetch_hf(data_root, item, dry_run)
    elif method == "modelscope":
        fetch_modelscope(data_root, item, dry_run)
    elif method == "gdrive":
        fetch_gdrive_file(source["id"], data_root / item["local_subdir"] / source["filename"], dry_run)
    elif method == "direct":
        fetch_direct(data_root, item, dry_run)
    elif method == "derived":
        fetch_derived(data_root, item, dry_run)
    fetch_attachments(data_root, item, dry_run)
    if not dry_run:
        write_marker(data_root, item, lock_path)


def sha256(path: Path) -> str:
    return file_digest(path, "sha256")


def file_digest(path: Path, algorithm: str) -> str:
    digest = (
        hashlib.md5(usedforsecurity=False)
        if algorithm == "md5"
        else hashlib.new(algorithm)
    )
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def governed_hash_ok(path: Path, remote: dict[str, Any]) -> bool:
    if remote.get("sha256"):
        return sha256(path) == remote["sha256"]
    if remote.get("md5"):
        return file_digest(path, "md5") == remote["md5"]
    return True


def verify_item(data_root: Path, item: dict[str, Any], full: bool = False) -> tuple[str, str]:
    local = data_root / item["local_subdir"]
    if not local.exists():
        if item.get("status") == "BLOCKED":
            return "BLOCKED", item.get("blocking_reason", "acquisition blocked")
        return "MISSING", "path absent"
    scan_roots = [local]
    cache = local / ".cache"
    hfd = local / ".hfd"
    if not full:
        scan_roots = [path for path in (cache, hfd) if path.exists()]
    incomplete: list[Path] = []
    for scan_root in scan_roots:
        incomplete.extend(scan_root.rglob("*.incomplete"))
        incomplete.extend(scan_root.rglob("*.part"))
        incomplete.extend(scan_root.rglob("*.aria2"))
    if not full:
        for pattern in ("*.incomplete", "*.part", "*.aria2"):
            incomplete.extend(local.glob(pattern))
    if incomplete:
        return "PARTIAL", f"{len(incomplete)} partial marker(s)"
    source = item.get("source") or {}
    git_verified = False
    if source.get("kind") == "git":
        root = git_root(data_root, item)
        try:
            head = subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip()
        except subprocess.CalledProcessError:
            return "PARTIAL", "git HEAD unreadable"
        if head != item.get("revision"):
            return "PARTIAL", f"git HEAD {head[:12]} != lock"
        pointers = 0
        if source.get("lfs_include"):
            for path in local.rglob("*"):
                if path.is_file() and path.stat().st_size < 1024:
                    try:
                        if path.read_bytes().startswith(
                            b"version https://git-lfs.github.com/spec/v1"
                        ):
                            pointers += 1
                    except OSError:
                        pass
        if pointers:
            return "PARTIAL", f"{pointers} Git LFS pointer(s) remain"
        git_verified = True
    governed_files = [
        *source.get("files", []),
        *source.get("attachments", []),
    ]
    for attachment in governed_files:
        path = local / attachment["filename"]
        if not path.exists():
            return "PARTIAL", f"missing governed file {attachment['filename']}"
        if attachment.get("size_bytes") and path.stat().st_size != attachment["size_bytes"]:
            return "PARTIAL", f"governed file size mismatch: {attachment['filename']}"
        if full and not governed_hash_ok(path, attachment):
            return "PARTIAL", f"governed file hash mismatch: {attachment['filename']}"
    if git_verified:
        return "COMPLETE", "matching Git revision; no LFS pointers or missing attachments"
    marker = marker_path(data_root, item)
    if marker.exists():
        try:
            receipt = json.loads(marker.read_text(encoding="utf-8"))
            if receipt.get("revision") == item.get("revision"):
                return "COMPLETE", "matching local receipt"
        except (OSError, json.JSONDecodeError):
            pass
    if item.get("status") == "COMPLETE":
        observed = (item.get("verification") or {}).get("observed_at", "lock snapshot")
        return "COMPLETE", f"present; lock fingerprint observed {observed}"
    return "PARTIAL", "present without matching completion receipt"


def command_validate(args: argparse.Namespace) -> int:
    lock = load_lock(args.lock)
    errors = validate(lock)
    if errors:
        for error in errors:
            print(f"ERROR {error}")
        return 1
    print(f"OK {len(assets(lock))} assets; canonical lock {args.lock}")
    return 0


def command_list(args: argparse.Namespace) -> int:
    lock = load_lock(args.lock)
    selected = selected_assets(lock, args.names, args.profile)
    for item in selected:
        print(
            "\t".join(
                [
                    item["name"],
                    item["kind"],
                    item["lifecycle"],
                    item["status"],
                    str((item.get("source") or {}).get("kind", "-")),
                    source_id(item),
                    item["local_subdir"],
                ]
            )
        )
    return 0


def command_fetch(args: argparse.Namespace) -> int:
    lock = load_lock(args.lock)
    errors = validate(lock)
    if errors:
        raise SystemExit("lock validation failed; run asset_lock.py validate")
    selected = selected_assets(lock, args.names, args.profile)
    completed_groups: set[str] = set()
    failures = 0
    for item in selected:
        group = (item.get("source") or {}).get("fetch_group", f"{item['kind']}:{item['name']}")
        if group in completed_groups:
            print(f"SKIP duplicate fetch group: {item['name']} -> {group}")
            continue
        try:
            fetch_one(args.data_root, item, args.lock, args.dry_run)
            completed_groups.add(group)
        except (OSError, RuntimeError, subprocess.CalledProcessError) as exc:
            failures += 1
            print(f"FAILED {item['name']}: {exc}", file=sys.stderr)
    print(f"fetch summary: selected={len(selected)} groups={len(completed_groups)} failed={failures}")
    return int(failures != 0)


def command_inventory(args: argparse.Namespace) -> int:
    lock = load_lock(args.lock)
    selected = selected_assets(lock, args.names, args.profile) if (args.names or args.profile) else assets(lock)
    counts = {status: 0 for status in ALLOWED_STATUS}
    drift = 0
    for item in selected:
        observed, detail = verify_item(args.data_root, item, args.full)
        counts[observed] += 1
        if observed != item["status"]:
            drift += 1
        print(f"{item['name']}\tlock={item['status']}\tobserved={observed}\t{detail}")
    print("inventory summary:", " ".join(f"{k}={counts[k]}" for k in sorted(counts)), f"drift={drift}")
    return int(args.fail_on_drift and drift != 0)


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser()
    result.add_argument("--lock", type=Path, default=DEFAULT_LOCK)
    result.add_argument("--data-root", type=Path, default=DEFAULT_DATA)
    sub = result.add_subparsers(dest="command", required=True)

    validate_parser = sub.add_parser("validate")
    validate_parser.set_defaults(func=command_validate)

    list_parser = sub.add_parser("list")
    list_parser.add_argument("names", nargs="*")
    list_parser.add_argument("--profile")
    list_parser.set_defaults(func=command_list)

    fetch_parser = sub.add_parser("fetch")
    fetch_parser.add_argument("names", nargs="*")
    fetch_parser.add_argument("--profile")
    fetch_parser.add_argument("--dry-run", action="store_true")
    fetch_parser.set_defaults(func=command_fetch)

    inventory_parser = sub.add_parser("inventory")
    inventory_parser.add_argument("names", nargs="*")
    inventory_parser.add_argument("--profile")
    inventory_parser.add_argument("--full", action="store_true")
    inventory_parser.add_argument("--fail-on-drift", action="store_true")
    inventory_parser.set_defaults(func=command_inventory)
    return result


def main() -> int:
    args = parser().parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
