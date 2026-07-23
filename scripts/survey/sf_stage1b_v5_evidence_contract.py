#!/usr/bin/env python3
"""Validate the bounded Stage-1B v5 literature, inventory, and asset repair."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any


REL = {
    "reconciliation": "wiki/survey/current/data/stage1b-eligible-bundle-reconciliation-v1.json",
    "supplement": "wiki/survey/current/data/stage1b-speech-direct-prior-supplement-v3.json",
    "control": "wiki/survey/current/data/stage1b-direct-control-basis-v2.json",
    "appendix": "wiki/survey/current/stage1b-transition-reference-appendix.md",
    "metadata": "wiki/survey/current/data/official-metadata-receipts-v1.jsonl",
    "mapping": "wiki/survey/current/tables/stage1b-mapping-release.md",
    "eligible": "wiki/survey/current/tables/stage1c-eligible-inputs.md",
    "inventory_python": "docs/checks/stage1b-closeout/2026-07-23-v5/speechrl-data-layered-inventory-python.json",
    "inventory_powershell": "docs/checks/stage1b-closeout/2026-07-23-v5/speechrl-data-layered-inventory-powershell.json",
    "content": "docs/checks/stage1b-closeout/2026-07-23-v5/speechrl-data-content-accounting.json",
    "asset_lock": "docs/stage1b-v5-gate-assets.lock.json",
}


def _json(root: Path, key: str) -> dict[str, Any]:
    return json.loads((root / REL[key]).read_text(encoding="utf-8"))


def _normalized_inventory(document: dict[str, Any]) -> dict[str, Any]:
    normalized = dict(document)
    normalized["layers"] = []
    for source in document["layers"]:
        layer = dict(source)
        layer["entries"] = sorted(
            layer.get("entries", []),
            key=lambda row: (str(row.get("local_path", "")), str(row.get("name", ""))),
        )
        normalized["layers"].append(layer)
    return normalized


def _layer_facts(document: dict[str, Any]) -> tuple[int, int, int, int]:
    layers = {row["layer_id"]: row for row in document["layers"]}
    baseline = layers["FROZEN_BASELINE"]
    return (
        int(baseline["observed_entries"]),
        int(layers["LOCAL_CANDIDATE_UNFROZEN"]["observed_entries"]),
        len(layers["SURVEY_AND_REPRO_AUXILIARY"]["entries"]),
        len(baseline["missing_locked_paths"]),
    )


def validate_repository(root: Path, *, data_root: Path) -> dict[str, Any]:
    root = root.resolve()
    failures: list[str] = []
    reconciliation = _json(root, "reconciliation")
    supplement = _json(root, "supplement")
    control = _json(root, "control")
    inv_python = _json(root, "inventory_python")
    inv_powershell = _json(root, "inventory_powershell")
    content = _json(root, "content")
    asset_lock = _json(root, "asset_lock")

    rows = reconciliation.get("rows", [])
    ids = [str(row.get("paper_work_id")) for row in rows]
    gate = [row for row in rows if row.get("gate_work")]
    route = [row for row in rows if not row.get("gate_work")]
    if len(rows) != 18 or len(set(ids)) != 18 or len(gate) != 6 or len(route) != 12:
        failures.append("RECONCILIATION_NOT_18_UNIQUE_6_GATE_12_ROUTE")
    if any(row.get("seed_action") != "REUSE_CANONICAL_WORK_ID_NO_DUPLICATE_CLAIM_WORK" for row in rows):
        failures.append("DUPLICATE_CLAIM_WORK_POLICY_VIOLATION")

    fulltext_verified = 0
    for row in rows:
        ref = row.get("fulltext_ref", {})
        paper_id = str(row.get("paper_work_id"))
        path = data_root / "survey-fulltext" / paper_id / f"{paper_id}.pdf"
        try:
            raw = path.read_bytes()
        except OSError:
            failures.append(f"FULLTEXT_MISSING:{paper_id}")
            continue
        if len(raw) != ref.get("bytes") or hashlib.sha256(raw).hexdigest() != ref.get("sha256"):
            failures.append(f"FULLTEXT_HASH_MISMATCH:{paper_id}")
            continue
        fulltext_verified += 1

    role_counts = Counter(row.get("analysis_role") for row in supplement.get("rows", []))
    supplement_roles = {
        "direct": role_counts["DIRECT_CONTROL_METHOD"],
        "instrument": role_counts["MEASUREMENT_INSTRUMENT"],
        "boundary": role_counts["BOUNDARY_COMPARATOR"],
    }
    if len(supplement.get("rows", [])) != 46 or supplement_roles != {"direct": 26, "instrument": 18, "boundary": 2}:
        failures.append("SUPPLEMENT_ROLE_COUNTS_MISMATCH")

    control_rows = control.get("rows", [])
    basis_counts = Counter(row.get("control_basis") for row in control_rows)
    control_basis = {
        "orchestration": basis_counts["EXTERNAL_ORCHESTRATION_ONLY"],
        "state_event": basis_counts["STATE_OR_EVENT_GATED"],
        "evaluator_verifier": basis_counts["EVALUATOR_OR_VERIFIER_GATED"],
        "reward_guided": basis_counts["REWARD_GUIDED_SELECTION"],
    }
    if len(control_rows) != 26 or control_basis != {"orchestration": 9, "state_event": 9, "evaluator_verifier": 8, "reward_guided": 0}:
        failures.append("CONTROL_BASIS_COUNTS_MISMATCH")
    if any("reward_or_evaluator_identity" in row for row in control_rows):
        failures.append("LEGACY_REWARD_OR_EVALUATOR_FIELD_PRESENT")

    appendix = (root / REL["appendix"]).read_text(encoding="utf-8")
    appendix_ids = re.findall(r"<!-- work:([^ ]+) -->(?:DP|ROUTE)-", appendix)
    if len(appendix_ids) != 59 or len(set(appendix_ids)) != 59:
        failures.append("APPENDIX_NOT_59_UNIQUE_ROUTES")
    for identity in ids:
        if not re.search(rf"<!-- work:{re.escape(identity)} -->(?:DP|ROUTE)-{re.escape(identity)}", appendix):
            failures.append(f"APPENDIX_MISSING:{identity}")
    if "<!-- work:2303.11381 -->ROUTE-2303.11381" not in appendix or "<!-- work:2602.13685 -->ROUTE-2602.13685" not in appendix:
        failures.append("APPENDIX_MISSING_LEGACY_BOUNDARY")

    metadata_rows = [json.loads(line) for line in (root / REL["metadata"]).read_text(encoding="utf-8").splitlines() if line]
    metadata_ids = [f"{row.get('identity', {}).get('kind')}:{row.get('identity', {}).get('id')}" for row in metadata_rows]
    if len(metadata_rows) != 135 or len(set(metadata_ids)) != 135:
        failures.append("OFFICIAL_METADATA_NOT_135_UNIQUE")

    inventory_parity = _normalized_inventory(inv_python) == _normalized_inventory(inv_powershell)
    inventory_facts = _layer_facts(inv_python)
    if not inventory_parity:
        failures.append("INVENTORY_IMPLEMENTATIONS_DIVERGE")
    if inventory_facts != (31, 33, 5, 0):
        failures.append("INVENTORY_COUNTS_NOT_31_33_5_0")

    audio2tool = content.get("entries", [{}])[0]
    if audio2tool.get("remote_content") != {"files": 71441, "bytes": 10410773494, "missing": 0}:
        failures.append("AUDIO2TOOL_REMOTE_CONTENT_MISMATCH")
    if audio2tool.get("auxiliary_content") != {"files": 11, "bytes": 62611468}:
        failures.append("AUDIO2TOOL_AUXILIARY_CONTENT_MISMATCH")
    if audio2tool.get("extraneous_content") != {"files": 610, "bytes": 1158458}:
        failures.append("AUDIO2TOOL_EXTRANEOUS_CONTENT_MISMATCH")
    if audio2tool.get("hygiene_action") != "DO_NOT_DELETE; STAGE2_LOADER_MUST_USE_REVISION_BOUND_ALLOWLIST":
        failures.append("AUDIO2TOOL_HYGIENE_POLICY_MISMATCH")

    if len(asset_lock.get("datasets", [])) != 1 or len(asset_lock.get("ref_repos", [])) != 3 or len(asset_lock.get("unavailable_assets", [])) != 4:
        failures.append("GATE_ASSET_LOCK_COUNTS_MISMATCH")
    dataset = asset_lock.get("datasets", [{}])[0]
    dataset_root = data_root / str(dataset.get("local_subdir", ""))
    dataset_manifest = dataset_root / ".hfd" / "manifest"
    manifest_files = 0
    manifest_bytes = 0
    manifest_missing = 0
    try:
        for line in dataset_manifest.read_text(encoding="utf-8").splitlines():
            size, relative = line.split("\t", 1)
            manifest_files += 1
            manifest_bytes += int(size)
            manifest_missing += int(not (dataset_root / relative).is_file())
    except (OSError, UnicodeDecodeError, ValueError):
        failures.append("UNISRM_BENCH_MANIFEST_UNREADABLE")
    if (
        manifest_files != dataset.get("expected_files")
        or manifest_bytes != dataset.get("expected_bytes")
        or manifest_missing != 0
    ):
        failures.append("UNISRM_BENCH_NOT_REVISION_COMPLETE")

    reference_revisions: dict[str, str] = {}
    for repo in asset_lock.get("ref_repos", []):
        name = str(repo.get("name"))
        try:
            actual = subprocess.check_output(
                ["git", "-C", str(data_root / str(repo.get("local_subdir", ""))), "rev-parse", "HEAD"],
                text=True,
                stderr=subprocess.DEVNULL,
            ).strip()
        except (OSError, subprocess.CalledProcessError):
            failures.append(f"REFERENCE_REPO_UNREADABLE:{name}")
            continue
        reference_revisions[name] = actual
        if actual != repo.get("revision"):
            failures.append(f"REFERENCE_REPO_REVISION_MISMATCH:{name}")

    current_text = "\n".join(
        (root / REL[key]).read_text(encoding="utf-8") for key in ("mapping", "eligible")
    )
    for identity in ids:
        if f"DP-{identity}" not in current_text:
            failures.append(f"CURRENT_LAYER_MISSING_ROUTE:{identity}")
    for marker in ("46-row", "26 direct", "18 instruments", "9 orchestration-only", "8 evaluator/verifier"):
        if marker not in current_text:
            failures.append(f"CURRENT_LAYER_MISSING_COUNT:{marker}")

    return {
        "schema": "sf-stage1b-v5-evidence-contract-v1",
        "scope": "BOUNDED_STAGE1B_V5_TRANSITION_REPAIR",
        "facts": {
            "closed_reconciliation_works": len(rows),
            "gate_works": len(gate),
            "route_works": len(route),
            "fulltext_hashes_verified": fulltext_verified,
            "official_metadata_receipts": len(metadata_rows),
            "appendix_unique_routes": len(set(appendix_ids)),
            "supplement_roles": supplement_roles,
            "control_basis": control_basis,
            "inventory_semantic_parity": inventory_parity,
            "inventory_counts": {"baseline": inventory_facts[0], "candidate": inventory_facts[1], "auxiliary": inventory_facts[2], "missing": inventory_facts[3]},
            "audio2tool_remote_files": audio2tool.get("remote_content", {}).get("files"),
            "audio2tool_extraneous_files_retained": audio2tool.get("extraneous_content", {}).get("files"),
            "unisrm_bench": {"files": manifest_files, "bytes": manifest_bytes, "missing": manifest_missing, "revision": dataset.get("revision")},
            "reference_repo_revisions": reference_revisions,
        },
        "claim_limit": "Literature and asset gate repair only; no model run, metric result, reproduction, ranking, novelty verdict, or Stage-2 authority.",
        "failures": failures,
        "status": "PASS" if not failures else "FAIL",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--data-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    receipt = validate_repository(args.repo, data_root=args.data_root)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Stage-1B v5 evidence contract: {receipt['status']}")
    for failure in receipt["failures"]:
        print(f"  - {failure}")
    return 0 if receipt["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
