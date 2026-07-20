#!/usr/bin/env python3
"""Prepare the 22 schema-v3 absence claims for independent semantic review.

This migrator binds existing negative claims to frozen fulltext bytes, exact
locators, proof obligations, owner rows, and stable future adjudication IDs. It
does not create an adjudicator identity, independence attestation, or verdict.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import tempfile
from copy import deepcopy
from pathlib import Path

from sf_evidence_contract import (
    ABSENCE_ALLOWED_VALUES,
    ABSENCE_PROOF_OBLIGATIONS,
    validate_bound_values,
    values_equal,
)
from sf_json_contract import read as read_strict_json
from sf_row_hash import row_hash


REPO = Path(__file__).resolve().parents[2]
SIDECAR_DIR = REPO / "wiki/survey/current/data/schema-v3/sidecars"
ADJUDICATION_PATH = (
    REPO / "wiki/survey/current/data/absence-evidence-adjudication-v2.json"
)
SIDECAR_REPO_PREFIX = "wiki/survey/current/data/schema-v3/sidecars"
PENDING_STATUS = "PENDING_INDEPENDENT_REVIEW"


def _proof(locators, reason, status="READY_FOR_REVIEW", concern=""):
    return {
        "inspected_locators": locators,
        "reason": reason,
        "implementer_assessment": {"status": status, "concern": concern},
    }


PROOF_PREPARATIONS = {
    ("2026.findings-acl.1243#closed-prompt-only", "human_or_dev_label_model_selection"): _proof(
        [
            "p4 anchor='framework consists of a decomposition agent a verification agent and a judge agent'",
            "p5 anchor='after completing each task the agent verifies its own outputs using deepverifier'",
            "p6 anchor='we mainly use claude 3 7 sonnet as the backbone model of deep verifier'",
        ],
        "The inspected deployed workflow exhaustively names automated decomposition, verification, judging, retry, and stopping operations; it contains no human or developer choice among model checkpoints based on labeled development outcomes.",
    ),
    ("2026.findings-acl.1243#closed-prompt-only", "selection_object"): _proof(
        [
            "p5 anchor='uses it to guide further retries'",
            "p6 anchor='a satisfactory answer is reached or a predefined retry limit is exceeded'",
        ],
        "The complete test-time procedure carries one current answer through verify-feedback-retry and returns on acceptance or the retry cap; it defines no simultaneously constructed objects from which a selector chooses.",
    ),
    ("2026.findings-acl.1243#closed-prompt-only", "explicit_candidate_pool_selection"): _proof(
        [
            "p5 anchor='uses it to guide further retries'",
            "p6 anchor='a satisfactory answer is reached or a predefined retry limit is exceeded'",
        ],
        "The exhaustive inference loop revises a single current answer sequentially and exposes no scored, ranked, voted, or tournament candidate pool selection operation.",
    ),
    ("2026.findings-acl.1243#open-sft-variant", "human_or_dev_label_model_selection"): _proof(
        [
            "p5 anchor='after completing each task the agent verifies its own outputs using deepverifier'",
            "p6 anchor='we fine tune qwen3 8b on a mixture'",
        ],
        "The inspected open-model construction specifies automated trajectory filtering, a fixed Qwen3-8B fine-tuning target, and an automated feedback loop; it gives no human or developer labeled checkpoint-selection step.",
    ),
    ("2026.findings-acl.1243#open-sft-variant", "selection_object"): _proof(
        [
            "p5 anchor='uses it to guide further retries'",
            "p6 anchor='a satisfactory answer is reached or a predefined retry limit is exceeded'",
        ],
        "The open variant retains the same single-answer verify-feedback-retry loop; the complete described inference path contains no candidate object compared by a selector.",
    ),
    ("2026.findings-acl.1243#open-sft-variant", "explicit_candidate_pool_selection"): _proof(
        [
            "p5 anchor='uses it to guide further retries'",
            "p6 anchor='a satisfactory answer is reached or a predefined retry limit is exceeded'",
        ],
        "The open variant's exhaustive inference procedure is sequential revision of one answer and specifies no scored, ranked, voted, or tournament choice over an explicit candidate pool.",
    ),
    ("2026.findings-acl.1724#pipeline", "inference_external_new_information"): _proof(
        [
            "p2 anchor='the pipeline takes raw data and produces a final report with curated charts'",
            "p4 anchor='the data profiling stage produces multiple metadata reports'",
            "p4 anchor='evaluator ranks candidates and discards a fixed'",
        ],
        "The complete pipeline transforms the provided raw dataset into profiles, charts, insights, and reports; code execution and judging operate on those task-provided artifacts and no retrieval, browsing, or external evidence channel is described.",
    ),
    ("2604.16529#rtv", "human_or_dev_label_model_selection"): _proof(
        [
            "tex: 'to select the strongest attempt from a population of rollouts without access to ground-truth outcomes'",
            "tex: 'RTV selects the final remaining rollout as its output'",
        ],
        "The complete RTV procedure is an automated tournament over rollout summaries and explicitly operates without ground-truth outcomes; it contains no human or developer labeled model-selection step.",
    ),
    ("2604.16529#rtv", "decision_rights"): _proof(
        [
            "tex: 'RTV selects the final remaining rollout as its output'",
            "tex: 'repeating the process in a tournament-like manner until one rollout remains from the entire population'",
        ],
        "The isolated RTV method path terminates by returning the final remaining rollout; after that terminal selection the source specifies no downstream route, retry, branch, tool, memory, supply, stop, synthesis, or execute-skip control action.",
    ),
    ("2604.16529#pdr-random-k", "human_or_dev_label_model_selection"): _proof(
        [
            "tex: 'for random-K, we follow PDR and randomly sample K previous summaries'",
            "tex: 'using K randomly sampled summaries from previous iteration rollouts'",
        ],
        "Random-K forms refinement context by parameter-free random sampling from prior summaries; no human or developer uses labels to choose a model, checkpoint, or sampled summary.",
    ),
    ("2604.16529#pdr-random-k", "selection_object"): _proof(
        [
            "tex: 'for random-K, we follow PDR and randomly sample K previous summaries into the previous-iteration rollouts'",
            "tex: 'provide as refinement context for executing each next-iteration rollout'",
        ],
        "The operation randomly samples summaries solely as context supply and does not compare, score, rank, vote on, or select a winning candidate object under the taxonomy's explicit selector semantics.",
    ),
    ("2604.16529#pdr-random-k", "explicit_candidate_pool_selection"): _proof(
        [
            "tex: 'for random-K, we follow PDR and randomly sample K previous summaries'",
            "tex: 'for select-K, we run RTV on the N parallel rollouts via tournament voting'",
        ],
        "The paper explicitly contrasts Random-K sampling with Select-K tournament voting; this method path uses the former and therefore has no scored or tournament candidate-pool selection.",
    ),
    ("2604.16529#rtv-pdr-pipeline", "human_or_dev_label_model_selection"): _proof(
        [
            "tex: 'RTV is then applied to these summaries to select the top-K summaries'",
            "tex: 'without access to ground-truth outcomes'",
        ],
        "The combined pipeline uses automated RTV to select summaries without ground-truth outcomes and supplies them to the next iteration; no human or developer label-based model choice appears in the complete recipe.",
    ),
    ("2605.08083#discovered-controller", "human_or_dev_label_model_selection"): _proof(
        [
            "p4 anchor='the discovery loop searches over code defined controllers'",
            "p5 anchor='value that achieves the highest accuracy'",
        ],
        "Controller and beta selection is an automated accuracy-based operation inside the discovery loop; the source describes no human or developer manually choosing among model checkpoints using labeled outcomes.",
    ),
    ("2605.08083#discovered-controller", "inference_external_new_information"): _proof(
        [
            "p4 anchor='the resulting execution histories are stored in memory'",
            "p5 anchor='fixed and evaluated on held out environments'",
        ],
        "After discovery, the fixed controller observes only branch state, probe answers, depth, and budget from the current task execution; the deployed inference procedure adds no retrieval, browsing, database, or external evidence source.",
    ),
    ("2606.03054#trained-gate", "human_or_dev_label_model_selection"): _proof(
        [
            "p6 anchor='each proposed tool call in a logged trajectory becomes one training instance'",
            "p6 anchor='the label is derived from forced answer probes before and after tool execution'",
            "p9 anchor='the diagnostic annotation of tool correctness is automatic and noisy'",
        ],
        "Training labels and diagnostic annotations are generated automatically from forced-answer probes, episode correctness, and a VLM judge; no human or developer label-based model or checkpoint selection step is described.",
    ),
    ("2606.03054#trained-gate", "inference_external_new_information"): _proof(
        [
            "p5 anchor='it does not see image pixels hidden states system prompts decoding log probabilities internal uncertainty estimates or the future tool output'",
            "p6 anchor='the tool suite includes six perceptual tools ocr'",
        ],
        "The system's tools only read out the task-provided image and the gate sees the existing trajectory plus pending call before execution; no retrieval, browsing, database, or information source external to the task input is introduced.",
    ),
    ("2606.03054#trained-gate", "selection_object"): _proof(
        [
            "p2 anchor='toolgate does not choose which tool to call given a call already proposed'",
            "p5 anchor='decides whether to execute the tool call'",
        ],
        "ToolGate receives one already-proposed call and makes a binary execute-or-skip action; it constructs no candidate output, trajectory, plan, tool-agent, or other pool object for terminal selection.",
    ),
    ("2606.03054#trained-gate", "explicit_candidate_pool_selection"): _proof(
        [
            "p2 anchor='toolgate does not choose which tool to call given a call already proposed'",
            "p5 anchor='decides whether to execute the tool call'",
        ],
        "The complete gate interface evaluates a single pending tool call and exposes no scored, ranked, voted, or tournament choice among an explicit pool of candidate outputs.",
    ),
}


def canonical_value(value):
    """Return a type-preserving canonical JSON scalar/list representation."""
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _source_tuple(pid, field, value):
    return (pid, "row", field, "absence", canonical_value(value))


def load_sidecars(sidecar_dir=SIDECAR_DIR):
    """Load strict JSON sidecars in filename order."""
    directory = Path(sidecar_dir)
    paths = sorted(directory.glob("*.sidecar.json"))
    if not paths:
        raise ValueError(f"no sidecars under {directory}")
    return [(path.name, read_strict_json(path)[0]) for path in paths]


def collect_absence_records(sidecars):
    """Collect every row-level absence binding without changing its owner."""
    records = []
    for filename, sidecar in sidecars:
        for row in sidecar.get("method_paths", []):
            pid = row.get("method_path_id")
            evidence = row.get("claim_evidence", {})
            for field, entry in evidence.items():
                if not isinstance(entry, dict) or entry.get("kind") != "absence":
                    continue
                source_tuple = _source_tuple(pid, field, entry.get("value"))
                records.append(
                    {
                        "filename": filename,
                        "method_path_id": pid,
                        "owner_kind": "row",
                        "field": field,
                        "kind": "absence",
                        "value": entry.get("value"),
                        "source_tuple": source_tuple,
                    }
                )
    return sorted(records, key=lambda record: record["source_tuple"])


def source_tuples(records):
    return sorted(record["source_tuple"] for record in records)


def _adjudication_row_id(source_tuple):
    payload = json.dumps(source_tuple, ensure_ascii=False, separators=(",", ":"))
    return "ABS2-" + hashlib.sha256(payload.encode("utf-8")).hexdigest()[:20]


def _assert_inventory(records):
    if len(records) != 19:
        raise ValueError(f"expected 19 active absence records, found {len(records)}")
    preparation_keys = set(PROOF_PREPARATIONS)
    record_keys = {
        (record["method_path_id"], record["field"]) for record in records
    }
    if record_keys != preparation_keys:
        missing = sorted(record_keys - preparation_keys)
        extra = sorted(preparation_keys - record_keys)
        raise ValueError(f"proof preparation mismatch missing={missing} extra={extra}")
    for record in records:
        allowed = ABSENCE_ALLOWED_VALUES.get(record["field"], ())
        if not any(values_equal(record["value"], value) for value in allowed):
            raise ValueError(f"disallowed absence source tuple: {record['source_tuple']}")


def prepare_migration(sidecars):
    """Return migrated sidecars and reviewer-ready proof rows, without verdicts."""
    migrated = deepcopy(sidecars)
    records = collect_absence_records(migrated)
    _assert_inventory(records)
    record_index = {
        (record["filename"], record["method_path_id"], record["field"]): record
        for record in records
    }
    proof_rows = []

    for filename, sidecar in migrated:
        sidecar_has_absence = False
        fulltext = {
            key: sidecar["fulltext"].get(key) for key in ("id", "kind", "sha256")
        }
        owner_sidecar = f"{SIDECAR_REPO_PREFIX}/{filename}"
        for row in sidecar.get("method_paths", []):
            pid = row["method_path_id"]
            fields = [
                field
                for field, entry in row.get("claim_evidence", {}).items()
                if isinstance(entry, dict) and entry.get("kind") == "absence"
            ]
            if not fields:
                continue
            sidecar_has_absence = True
            row["absence_review_status"] = PENDING_STATUS
            coder = row.get("coder", sidecar.get("coder"))
            for field in fields:
                source = record_index[(filename, pid, field)]
                preparation = PROOF_PREPARATIONS[(pid, field)]
                obligation = ABSENCE_PROOF_OBLIGATIONS[field]["proof_obligation_id"]
                adjudication_row_id = _adjudication_row_id(source["source_tuple"])
                row["claim_evidence"][field] = {
                    "kind": "absence",
                    "value": source["value"],
                    "reason": preparation["reason"],
                    "proof_obligation_id": obligation,
                    "inspected_locators": deepcopy(preparation["inspected_locators"]),
                    "owner_method_path_id": pid,
                    "owner_sidecar": owner_sidecar,
                    "fulltext": deepcopy(fulltext),
                    "coder_identity": coder,
                    "owner_row_sha256": "0" * 64,
                    "adjudication_row_id": adjudication_row_id,
                }
            owner_hash = row_hash(row)
            for field in fields:
                entry = row["claim_evidence"][field]
                entry["owner_row_sha256"] = owner_hash
                source = record_index[(filename, pid, field)]
                preparation = PROOF_PREPARATIONS[(pid, field)]
                proof_rows.append(
                    {
                        "adjudication_row_id": entry["adjudication_row_id"],
                        "source_tuple": list(source["source_tuple"]),
                        "method_path_id": pid,
                        "owner_kind": "row",
                        "field": field,
                        "value": deepcopy(entry["value"]),
                        "proof_obligation_id": entry["proof_obligation_id"],
                        "inspected_locators": deepcopy(entry["inspected_locators"]),
                        "reason": entry["reason"],
                        "owner_sidecar": owner_sidecar,
                        "fulltext": deepcopy(fulltext),
                        "coder_identity": coder,
                        "owner_row_sha256": owner_hash,
                        "implementer_assessment": deepcopy(
                            preparation["implementer_assessment"]
                        ),
                    }
                )
            row["adjudication_row_sha256"] = owner_hash
            failures = validate_bound_values(row)
            if failures:
                raise ValueError(f"migrated row contract failed {pid}: {failures}")
        if sidecar_has_absence:
            sidecar["absence_review_status"] = PENDING_STATUS

    proof_rows.sort(key=lambda row: tuple(row["source_tuple"]))
    ids = [row["adjudication_row_id"] for row in proof_rows]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate absence adjudication_row_id")
    return migrated, proof_rows


def review_artifact(proof_rows, reviewer_rows):
    """Build the scaffold while preserving only externally supplied review rows."""
    status = (
        "INDEPENDENT_REVIEW_RECORDED_UNVALIDATED"
        if reviewer_rows
        else PENDING_STATUS
    )
    return {
        "artifact_id": "SF-ABSENCE-EVIDENCE-ADJUDICATION-V2-2026-07-21-02",
        "schema": "v2: 19 active generated proof_rows plus externally authored review rows; three retired negatives bind to the semantic-correction artifact",
        "generated_by": "scripts/survey/sf_absence_provenance_migrate.py",
        "original_proof_inventory_count": 22,
        "retired_by_semantic_correction_count": 3,
        "active_proof_inventory_count": len(proof_rows),
        "semantic_correction_artifact": "wiki/survey/current/data/negative-evidence-semantic-corrections-v1.json",
        "status": status,
        "independence_requirement": (
            "A non-implementer must review frozen fulltext for every proof row and "
            "supply TEAM_ATTESTATION identity, nonparticipation scope, timestamp, "
            "conflict declaration, per-row reason, and AGREE or DISAGREE."
        ),
        "review_row_required_fields": [
            "adjudication_row_id",
            "method_path_id",
            "owner_kind",
            "field",
            "proof_obligation_id",
            "owner_sidecar",
            "fulltext",
            "coder_identity",
            "owner_row_sha256",
            "adjudicator_identity",
            "verdict",
            "review_reason",
            "independence",
        ],
        "proof_obligation_catalog": deepcopy(ABSENCE_PROOF_OBLIGATIONS),
        "proof_rows": deepcopy(proof_rows),
        "rows": deepcopy(reviewer_rows),
    }


def _json_bytes(value):
    return (json.dumps(value, ensure_ascii=False, indent=1) + "\n").encode("utf-8")


def _atomic_write(path, payload):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, staging = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(staging, path)
        staging = None
    finally:
        if staging is not None:
            try:
                os.unlink(staging)
            except FileNotFoundError:
                pass


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--write", action="store_true")
    parser.add_argument("--sidecar-dir", default=os.fspath(SIDECAR_DIR))
    parser.add_argument("--adjudication", default=os.fspath(ADJUDICATION_PATH))
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    sidecar_dir = Path(args.sidecar_dir)
    adjudication_path = Path(args.adjudication)
    current = load_sidecars(sidecar_dir)
    migrated, proof_rows = prepare_migration(current)

    reviewer_rows = []
    if adjudication_path.exists():
        existing = read_strict_json(adjudication_path)[0]
        reviewer_rows = existing.get("rows", [])
        if not isinstance(reviewer_rows, list):
            raise ValueError("adjudication rows must be a list")
    artifact = review_artifact(proof_rows, reviewer_rows)

    expected = {
        sidecar_dir / filename: _json_bytes(sidecar)
        for filename, sidecar in migrated
    }
    expected[adjudication_path] = _json_bytes(artifact)
    stale = [
        path
        for path, payload in expected.items()
        if not path.exists() or path.read_bytes() != payload
    ]

    if args.check:
        if stale:
            print("[FAIL] absence migration stale: " + ", ".join(map(str, stale)))
            return 1
        print(
            f"[OK] absence migration exact: {len(proof_rows)} proof rows; "
            f"review rows={len(reviewer_rows)}"
        )
        return 0

    for path, payload in expected.items():
        _atomic_write(path, payload)
    print(
        f"wrote {len(migrated)} sidecars and {adjudication_path}; "
        f"proof rows={len(proof_rows)}; review rows preserved={len(reviewer_rows)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
