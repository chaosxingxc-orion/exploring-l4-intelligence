#!/usr/bin/env python3
"""Verify paper-linked repositories for bounded Stage-1B transfer decisions.

The verifier performs read-only metadata/tree requests. A repository is marked OPEN_SOURCE_VERIFIED
only when the paper-linked GitHub repository is reachable, has a declared license, contains source
code, documentation, and an environment/dependency specification. This establishes inspectability;
actual reproduction remains a later experiment-environment task.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


CODE_SUFFIXES = (".py", ".ts", ".js", ".sh", ".ipynb", ".cpp", ".cc", ".cu", ".java", ".rs")
ENV_NAMES = (
    "requirements.txt", "pyproject.toml", "setup.py", "setup.cfg", "environment.yml",
    "environment.yaml", "conda.yml", "poetry.lock", "package.json", "dockerfile",
)
CONFIG_SUFFIXES = (".yaml", ".yml", ".json", ".toml")


def canonical_repository_url(url: str) -> str | None:
    parsed = urlparse(url.strip())
    host = parsed.netloc.lower().removeprefix("www.")
    parts = [part for part in parsed.path.split("/") if part]
    if len(parts) >= 2:
        parts[1] = re.sub(r"(?:\.git)?[.,;:]+$", "", parts[1], flags=re.IGNORECASE)
    if host == "github.com" and len(parts) >= 2:
        return f"https://github.com/{parts[0]}/{parts[1].removesuffix('.git')}"
    if host == "gitlab.com" and len(parts) >= 2:
        return f"https://gitlab.com/{parts[0]}/{parts[1].removesuffix('.git')}"
    if host == "huggingface.co" and len(parts) >= 2:
        if parts[0] in {"datasets", "spaces"} and len(parts) >= 3:
            return f"https://huggingface.co/{parts[0]}/{parts[1]}/{parts[2]}"
        return f"https://huggingface.co/{parts[0]}/{parts[1]}"
    return None


def classify_github_repository(url: str, metadata: dict[str, Any], paths: list[str]) -> dict[str, Any]:
    lowered = [path.lower() for path in paths]
    license_obj = metadata.get("license") or {}
    spdx = license_obj.get("spdx_id") if isinstance(license_obj, dict) else None
    license_visible = bool(spdx and spdx not in {"NOASSERTION", "OTHER"})
    readme_present = any(Path(path).name.lower().startswith("readme") for path in paths)
    code_present = any(path.endswith(CODE_SUFFIXES) for path in lowered)
    environment_present = any(Path(path).name.lower() in ENV_NAMES for path in paths)
    config_present = any(
        path.endswith(CONFIG_SUFFIXES) and ("config" in path or "eval" in path or "experiment" in path)
        for path in lowered
    )
    weights_or_download_present = any(
        path.endswith((".pt", ".pth", ".ckpt", ".safetensors"))
        or "download" in Path(path).name.lower()
        or "checkpoint" in path
        for path in lowered
    )
    evaluation_entrypoint_present = any(
        any(token in Path(path).name.lower() for token in ("eval", "test", "benchmark"))
        and path.endswith(CODE_SUFFIXES)
        for path in lowered
    )
    if not license_visible:
        status = "REPOSITORY_REACHABLE_LICENSE_UNRESOLVED"
    elif code_present and readme_present and environment_present:
        status = "OPEN_SOURCE_VERIFIED"
    else:
        status = "INSPECTABLE_BUT_REPRO_INCOMPLETE"
    return {
        "url": url,
        "status": status,
        "reachable": True,
        "license_spdx": spdx,
        "license_visible": license_visible,
        "code_present": code_present,
        "readme_present": readme_present,
        "environment_present": environment_present,
        "config_present": config_present,
        "weights_or_download_present": weights_or_download_present,
        "evaluation_entrypoint_present": evaluation_entrypoint_present,
        "archived": bool(metadata.get("archived")),
        "default_branch": metadata.get("default_branch"),
        "tree_entries": len(paths),
        "reproduction_scope": "STRUCTURE_VERIFIED_EXECUTION_NOT_YET_RUN",
    }


def _gh_api(gh: Path, endpoint: str) -> Any:
    completed = subprocess.run(
        [str(gh), "api", endpoint],
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=45,
    )
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.strip() or f"gh api failed for {endpoint}")
    return json.loads(completed.stdout)


def verify_github(url: str, gh: Path) -> dict[str, Any]:
    match = re.fullmatch(r"https://github\.com/([^/]+)/([^/]+)", url)
    if not match:
        return {"url": url, "status": "INVALID_REPOSITORY_URL", "reachable": False}
    owner, repo = match.groups()
    try:
        metadata = _gh_api(gh, f"repos/{owner}/{repo}")
        branch = metadata.get("default_branch") or "main"
        tree = _gh_api(gh, f"repos/{owner}/{repo}/git/trees/{branch}?recursive=1")
        paths = [str(item.get("path")) for item in tree.get("tree", []) if item.get("type") == "blob"]
        result = classify_github_repository(url, metadata, paths)
        result["tree_truncated"] = bool(tree.get("truncated"))
        return result
    except Exception as exc:  # retain failure rather than infer absence
        return {
            "url": url,
            "status": "REPOSITORY_UNREACHABLE",
            "reachable": False,
            "error": f"{type(exc).__name__}: {exc}",
        }


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text("utf-8").splitlines() if line.strip()]


def run(triage_path: Path, output_path: Path, gh: Path) -> dict[str, Any]:
    source_rows = _read_jsonl(triage_path)
    originals = sorted({url for row in source_rows for url in (row.get("repo_urls") or [])})
    canonical_to_originals: dict[str, list[str]] = {}
    invalid = []
    for original in originals:
        canonical = canonical_repository_url(original)
        if canonical:
            canonical_to_originals.setdefault(canonical, []).append(original)
        else:
            invalid.append(original)

    verified: dict[str, Any] = {}
    canonical_results = {}
    for canonical in sorted(canonical_to_originals):
        if canonical.startswith("https://github.com/"):
            result = verify_github(canonical, gh)
        else:
            result = {
                "url": canonical,
                "status": "NON_GITHUB_REQUIRES_MANUAL_VERIFICATION",
                "reachable": None,
            }
        canonical_results[canonical] = result
        for original in canonical_to_originals[canonical]:
            verified[original] = {**result, "canonical_url": canonical, "paper_link_url": original}
    for original in invalid:
        verified[original] = {
            "url": original,
            "canonical_url": None,
            "status": "INVALID_REPOSITORY_URL",
            "reachable": False,
        }

    payload = json.dumps(verified, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(payload, encoding="utf-8", newline="\n")
    counts = {}
    for result in canonical_results.values():
        status = result["status"]
        counts[status] = counts.get(status, 0) + 1
    return {
        "schema": "sf-stage1b-repository-verification-summary-v1",
        "paper_link_urls": len(originals),
        "canonical_repositories": len(canonical_results),
        "invalid_urls": len(invalid),
        "status_counts": dict(sorted(counts.items())),
        "output_path": output_path.as_posix(),
        "output_bytes": len(payload.encode("utf-8")),
        "output_sha256": hashlib.sha256(payload.encode("utf-8")).hexdigest(),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--triage", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--gh", type=Path, default=Path(r"C:\Program Files\GitHub CLI\gh.exe"))
    args = parser.parse_args()
    print(json.dumps(run(args.triage, args.output, args.gh), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
