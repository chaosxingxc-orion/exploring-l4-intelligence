#!/usr/bin/env python3
"""Cache only frozen bibliography identities from official metadata endpoints.

Validated current receipts and legacy Atom bytes are always reused first. The
script never downloads PDFs or e-prints: later D2 content work must reuse the
hash-bound local fulltext ledger (TeX/e-print first, local PDF fallback) and
fetch fulltext only when that separate gate explicitly requires a missing item.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import sf_bibliography_generator as bibliography  # noqa: E402


USER_AGENT = "exploring-l4-intelligence Stage-1A known-ID provenance fetch"
MAX_ATTEMPTS = 3
LEGACY_ATOM_DIR = bibliography.ROOT / "docs/survey-provenance/atom"
LEGACY_ATOM_LEDGER = bibliography.ROOT / "docs/survey-provenance/atom-ledger.jsonl"


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def fetch(url: str, *, pause_seconds: float = 1.0) -> tuple[bytes, str]:
    last_error = None
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            request = urllib.request.Request(
                url,
                headers={"User-Agent": USER_AGENT, "Accept": "*/*"},
            )
            with urllib.request.urlopen(request, timeout=90) as response:
                body = response.read()
                if response.status != 200 or not body:
                    raise RuntimeError(f"HTTP {response.status}, bytes={len(body)}")
                accessed = utc_now()
                time.sleep(pause_seconds)
                return body, accessed
        except (urllib.error.URLError, TimeoutError, RuntimeError) as error:
            last_error = error
            if attempt < MAX_ATTEMPTS:
                time.sleep(2 ** attempt)
    raise RuntimeError(f"official fetch failed after {MAX_ATTEMPTS} attempts: {url}: {last_error}")


def raw_binding(path: Path, body: bytes, media_type: str) -> dict[str, Any]:
    return {
        "path": path.relative_to(bibliography.ROOT).as_posix(),
        "bytes": len(body),
        "sha256": hashlib.sha256(body).hexdigest(),
        "media_type": media_type,
    }


def receipt(
    policy: dict[str, Any],
    *,
    official_url: str,
    accessed: str,
    raw: dict[str, Any],
    parsed: dict[str, Any],
) -> dict[str, Any]:
    return {
        "receipt_id": f"OMR-{policy['identity']['kind'].upper()}-{policy['identity']['id']}",
        "identity": policy["identity"],
        "official_url": official_url,
        "access_time_utc": accessed,
        "access_class": policy["access_class"],
        "query_recall_credit": False,
        "source_version": parsed["source_version"],
        "year_basis": parsed["year_basis"],
        "raw": raw,
        "normalized": {
            key: parsed[key] for key in ("title", "authors", "year", "stable_url")
        },
        "bibliography": {
            key: policy[key]
            for key in (
                "reference_role",
                "chain",
                "direct_neighbor",
                "next_action",
                "load_bearing",
            )
        },
        "source_provenance": policy["source_locator"],
    }


def legacy_atom_rows() -> dict[str, dict[str, Any]]:
    rows: dict[str, dict[str, Any]] = {}
    if not LEGACY_ATOM_LEDGER.is_file():
        return rows
    for line in LEGACY_ATOM_LEDGER.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        if row.get("persisted") and row.get("sha256") and row.get("entry_check") == "ok":
            rows[row["arxiv_id"]] = row
    return rows


def reuse_legacy_atom(policy: dict[str, Any], ledger: dict[str, dict[str, Any]]) -> dict[str, Any] | None:
    identity_id = policy["identity"]["id"]
    row = ledger.get(identity_id)
    path = LEGACY_ATOM_DIR / f"{identity_id}.xml"
    if row is None or not path.is_file():
        return None
    body = path.read_bytes()
    if hashlib.sha256(body).hexdigest() != row["sha256"]:
        raise RuntimeError(f"legacy Atom cache hash mismatch for {identity_id}")
    parsed = bibliography.parse_official_payload(
        policy["identity"], body, "application/atom+xml"
    )
    print(f"[cache:Atom] {identity_id}: {len(body)} bytes, network=0")
    return receipt(
        policy,
        official_url=row["url"],
        accessed=row["time_utc"],
        raw=raw_binding(path, body, "application/atom+xml"),
        parsed=parsed,
    )


def fetch_arxiv_oai(policy: dict[str, Any], raw_dir: Path) -> dict[str, Any]:
    identity_id = policy["identity"]["id"]
    url = (
        "https://export.arxiv.org/oai2?verb=GetRecord&identifier="
        f"oai:arXiv.org:{identity_id}&metadataPrefix=arXiv"
    )
    body, accessed = fetch(url, pause_seconds=1.0)
    path = raw_dir / f"arxiv-oai-{identity_id}.xml"
    path.write_bytes(body)
    parsed = bibliography.parse_official_payload(
        policy["identity"], body, "application/xml"
    )
    print(f"[arXiv:OAI] {identity_id}: {len(body)} bytes")
    return receipt(
        policy,
        official_url=url,
        accessed=accessed,
        raw=raw_binding(path, body, "application/xml"),
        parsed=parsed,
    )


def reusable_current_receipt(
    policy: dict[str, Any],
    cached: dict[str, dict[str, Any]],
) -> dict[str, Any] | None:
    row = cached.get(policy["identity"]["id"])
    if row is None:
        return None
    binding = row.get("raw", {})
    path = bibliography.ROOT / binding.get("path", "__missing__")
    if not path.is_file():
        return None
    body = path.read_bytes()
    if hashlib.sha256(body).hexdigest() != binding.get("sha256"):
        return None
    parsed = bibliography.parse_official_payload(
        policy["identity"], body, binding["media_type"]
    )
    expected = receipt(
        policy,
        official_url=row["official_url"],
        accessed=row["access_time_utc"],
        raw=binding,
        parsed=parsed,
    )
    if expected != row:
        return None
    print(f"[cache:receipt] {policy['identity']['id']}: network=0")
    return row


def recover_current_raw(policy: dict[str, Any], raw_dir: Path) -> dict[str, Any] | None:
    identity = policy["identity"]
    if identity["kind"] == "arxiv":
        path = raw_dir / f"arxiv-oai-{identity['id']}.xml"
        media_type = "application/xml"
        official_url = (
            "https://export.arxiv.org/oai2?verb=GetRecord&identifier="
            f"oai:arXiv.org:{identity['id']}&metadataPrefix=arXiv"
        )
    elif identity["kind"] == "acl":
        path = raw_dir / f"acl-{identity['id']}.bib"
        media_type = "application/x-bibtex"
        official_url = f"https://aclanthology.org/{identity['id']}.bib"
    else:
        path = raw_dir / ("github-" + identity["id"].replace("/", "--") + ".json")
        media_type = "application/json"
        official_url = f"https://api.github.com/repos/{identity['id']}"
    if not path.is_file():
        return None
    body = path.read_bytes()
    parsed = bibliography.parse_official_payload(identity, body, media_type)
    accessed = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )
    print(f"[cache:raw] {identity['id']}: {len(body)} bytes, network=0")
    return receipt(
        policy,
        official_url=official_url,
        accessed=accessed,
        raw=raw_binding(path, body, media_type),
        parsed=parsed,
    )


def fetch_acl(policy: dict[str, Any], raw_dir: Path) -> dict[str, Any]:
    identity_id = policy["identity"]["id"]
    url = f"https://aclanthology.org/{identity_id}.bib"
    body, accessed = fetch(url, pause_seconds=0.5)
    path = raw_dir / f"acl-{identity_id}.bib"
    path.write_bytes(body)
    parsed = bibliography.parse_official_payload(
        policy["identity"], body, "application/x-bibtex"
    )
    print(f"[ACL] {identity_id}: {len(body)} bytes")
    return receipt(
        policy,
        official_url=url,
        accessed=accessed,
        raw=raw_binding(path, body, "application/x-bibtex"),
        parsed=parsed,
    )


def fetch_github(policy: dict[str, Any], raw_dir: Path) -> dict[str, Any]:
    identity_id = policy["identity"]["id"]
    url = f"https://api.github.com/repos/{identity_id}"
    body, accessed = fetch(url, pause_seconds=0.5)
    path = raw_dir / ("github-" + identity_id.replace("/", "--") + ".json")
    path.write_bytes(body)
    parsed = bibliography.parse_official_payload(
        policy["identity"], body, "application/json"
    )
    print(f"[GitHub] {identity_id}: {len(body)} bytes")
    return receipt(
        policy,
        official_url=url,
        accessed=accessed,
        raw=raw_binding(path, body, "application/json"),
        parsed=parsed,
    )


def write_receipts(rows: list[dict[str, Any]], path: Path) -> None:
    rows.sort(key=lambda row: (row["identity"]["kind"], row["identity"]["id"]))
    data = b"".join(
        (json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n").encode("utf-8")
        for row in rows
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=bibliography.RECEIPTS_PATH)
    parser.add_argument("--raw-dir", type=Path, default=bibliography.RAW_DIR)
    parser.add_argument(
        "--offline",
        action="store_true",
        help="reuse validated receipts and legacy Atom only; fail instead of accessing the network",
    )
    args = parser.parse_args(argv)
    output = args.output if args.output.is_absolute() else bibliography.ROOT / args.output
    raw_dir = args.raw_dir if args.raw_dir.is_absolute() else bibliography.ROOT / args.raw_dir
    raw_dir.mkdir(parents=True, exist_ok=True)

    policies = sorted(
        bibliography.all_policies().values(),
        key=lambda policy: (policy["identity"]["kind"], policy["identity"]["id"]),
    )
    cached_rows = {}
    if output.is_file():
        cached_rows = {
            row["identity"]["id"]: row for row in bibliography.load_receipts(output)
        }
    atom_ledger = legacy_atom_rows()
    counts = {
        kind: sum(policy["identity"]["kind"] == kind for policy in policies)
        for kind in ("arxiv", "acl", "github")
    }
    print(
        "local-first known-ID provenance only: "
        f"arxiv={counts['arxiv']} acl={counts['acl']} github={counts['github']}; "
        "systematic discovery queries=0; query recall credit=false"
    )
    rows = []
    missing = []
    for policy in policies:
        cached = reusable_current_receipt(policy, cached_rows)
        if cached is not None:
            rows.append(cached)
            continue
        recovered = recover_current_raw(policy, raw_dir)
        if recovered is not None:
            rows.append(recovered)
            continue
        if policy["identity"]["kind"] == "arxiv":
            atom = reuse_legacy_atom(policy, atom_ledger)
            if atom is not None:
                rows.append(atom)
                continue
        if args.offline:
            missing.append(policy["identity"]["id"])
            continue
        if policy["identity"]["kind"] == "arxiv":
            rows.append(fetch_arxiv_oai(policy, raw_dir))
        elif policy["identity"]["kind"] == "acl":
            rows.append(fetch_acl(policy, raw_dir))
        else:
            rows.append(fetch_github(policy, raw_dir))
    if missing:
        print(json.dumps({"verdict": "FAIL", "offline_missing": missing}, indent=2))
        return 1
    write_receipts(rows, output)
    failures = bibliography.validate_receipts(rows)
    if failures:
        print(json.dumps({"verdict": "FAIL", "failure_codes": failures}, indent=2))
        return 1
    try:
        output_label = output.relative_to(bibliography.ROOT).as_posix()
    except ValueError:
        output_label = str(output)
    print(f"PASS wrote {output_label}: {len(rows)} receipts")
    return 0


if __name__ == "__main__":
    sys.exit(main())
