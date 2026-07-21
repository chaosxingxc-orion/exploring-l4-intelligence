#!/usr/bin/env python3
"""Freeze and replay the dual-platform PDF text-extractor contract."""
from __future__ import annotations

import hashlib
import io
import json
import os
import sys
from pathlib import Path
from typing import Any

from sf_asset_path import resolve_asset_path
from sf_evidence_contract import normalized_phrase


ROOT = Path(__file__).resolve().parents[2]
CONTRACT_PATH = ROOT / "wiki/survey/current/data/pdf-extractor-environment-v1.json"
LEDGER_PATH = ROOT / "wiki/survey/2026-07-17-sf-fulltext-ledger.jsonl"
TOOLGATE_SIDECAR_PATH = (
    ROOT / "wiki/survey/current/data/schema-v3/sidecars/2606.03054.sidecar.json"
)
EXTRACTOR_SUFFIX = "PdfReader.extract_text:v1"
CANONICAL_ENVIRONMENTS = {
    "nt": {
        "os": "nt",
        "sys_platform": "win32",
        "python_version": "3.14.3",
        "pypdf_version": "6.14.0",
        "extractor_identity": "pypdf:6.14.0:PdfReader.extract_text:v1",
    },
    "posix": {
        "os": "posix",
        "sys_platform": "linux",
        "python_version": "3.12.3",
        "pypdf_version": "6.14.2",
        "extractor_identity": "pypdf:6.14.2:PdfReader.extract_text:v1",
    },
}
TOOLGATE_PROBE = {
    "paper_id": "2606.03054",
    "kind": "pdf",
    "pdf_sha256": "8025d9126a14e6a07dab30fa93183bf1aa25fa9df2b753d18653549b50caa857",
    "page": 11,
    "anchor": "logistic regression classifier we train with l2",
    "owner_sidecar": "wiki/survey/current/data/schema-v3/sidecars/2606.03054.sidecar.json",
}


def load_contract(path: Path = CONTRACT_PATH) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def runtime_stamp() -> dict[str, str]:
    import pypdf

    return {
        "os": os.name,
        "sys_platform": sys.platform,
        "python_version": sys.version.split()[0],
        "pypdf_version": pypdf.__version__,
        "extractor_identity": f"pypdf:{pypdf.__version__}:{EXTRACTOR_SUFFIX}",
    }


def _ledger_pdf_row() -> dict[str, Any]:
    for line in LEDGER_PATH.read_text(encoding="utf-8").splitlines():
        row = json.loads(line)
        if row.get("arxiv_id") == "2606.03054" and row.get("kind") == "pdf":
            return row
    return {}


def _contains_probe_binding(value: Any, probe: dict[str, Any]) -> bool:
    if isinstance(value, dict):
        if all(value.get(key) == probe[key] for key in ("kind", "page", "anchor")):
            return True
        return any(_contains_probe_binding(child, probe) for child in value.values())
    if isinstance(value, list):
        return any(_contains_probe_binding(child, probe) for child in value)
    return False


def validate_contract(document: dict[str, Any]) -> list[str]:
    failures: set[str] = set()
    if document.get("schema") != "sf-pdf-extractor-environment-v1":
        failures.add("PDF_EXTRACTOR_SCHEMA_MISMATCH")
    environments = document.get("canonical_environments")
    if not isinstance(environments, dict) or set(environments) != {"nt", "posix"}:
        failures.add("PDF_EXTRACTOR_ENVIRONMENT_INVENTORY_MISMATCH")
        environments = environments if isinstance(environments, dict) else {}
    for role, expected in CANONICAL_ENVIRONMENTS.items():
        if environments.get(role) != expected:
            failures.add(f"PDF_EXTRACTOR_IDENTITY_MISMATCH:{role}")
    if document.get("version_policy") != "EXACT_MATCH_FAIL_CLOSED":
        failures.add("PDF_EXTRACTOR_VERSION_POLICY_MISMATCH")
    probe = document.get("toolgate_probe")
    if probe != TOOLGATE_PROBE:
        failures.add("PDF_EXTRACTOR_PROBE_CONTRACT_MISMATCH")
        probe = probe if isinstance(probe, dict) else {}
    ledger = _ledger_pdf_row()
    if (
        ledger.get("sha256") != probe.get("pdf_sha256")
        or ledger.get("http_status") != 200
    ):
        failures.add("PDF_EXTRACTOR_PROBE_LEDGER_MISMATCH")
    try:
        sidecar = json.loads(TOOLGATE_SIDECAR_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        sidecar = {}
    if not _contains_probe_binding(
        sidecar,
        {"kind": "pdf_page", "page": probe.get("page"), "anchor": probe.get("anchor")},
    ):
        failures.add("PDF_EXTRACTOR_PROBE_SIDECAR_MISMATCH")
    return sorted(failures)


def validate_runtime(
    document: dict[str, Any], stamp: dict[str, str] | None = None
) -> list[str]:
    stamp = stamp or runtime_stamp()
    role = stamp.get("os")
    expected = document.get("canonical_environments", {}).get(role)
    return [] if stamp == expected else ["PDF_EXTRACTOR_RUNTIME_MISMATCH"]


def replay_toolgate_probe(document: dict[str, Any]) -> dict[str, Any]:
    import pypdf

    stamp = runtime_stamp()
    probe = document["toolgate_probe"]
    ledger = _ledger_pdf_row()
    result = {
        "paper_id": probe["paper_id"],
        "page": probe["page"],
        "anchor": probe["anchor"],
        "pdf_sha256": probe["pdf_sha256"],
        "runtime": stamp,
        "asset_sha256_matches": False,
        "anchor_found": False,
        "result": "FAIL",
    }
    try:
        asset = Path(resolve_asset_path(ledger["stored_at"])).resolve(strict=True)
        raw = asset.read_bytes()
        result["asset_sha256_matches"] = (
            hashlib.sha256(raw).hexdigest() == probe["pdf_sha256"]
        )
        reader = pypdf.PdfReader(io.BytesIO(raw))
        page_text = normalized_phrase(
            reader.pages[probe["page"] - 1].extract_text() or ""
        )
        result["anchor_found"] = normalized_phrase(probe["anchor"]) in page_text
    except (OSError, KeyError, IndexError, ValueError):
        return result
    if (
        not validate_contract(document)
        and not validate_runtime(document, stamp)
        and result["asset_sha256_matches"]
        and result["anchor_found"]
    ):
        result["result"] = "PASS"
    return result
