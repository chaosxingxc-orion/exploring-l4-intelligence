#!/usr/bin/env python3
"""Validate the honest workbench proposal and its stricter release boundary."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from sf_h5_calibration_contract import validate_completion as validate_h5_completion
from sf_pdf_extractor_contract import validate_contract as validate_pdf_contract


ROOT = Path(__file__).resolve().parents[2]
PROPOSAL_PATH = (
    ROOT
    / "wiki/survey/workbench/system-first-stage1a/"
    "2026-07-21-stage1a-reviewer-brief.md"
)
ROUND16_PATH = (
    ROOT
    / "wiki/audit/system-first-stage1a/round-16/"
    "research-proposal-and-stage1b-signoff-request.md"
)
ABSENCE_PATH = ROOT / "wiki/survey/current/data/absence-evidence-adjudication-v3.json"
CORRECTIONS_PATH = ROOT / "wiki/survey/current/data/negative-evidence-semantic-corrections-v2.json"
H5_PATH = ROOT / "wiki/survey/current/data/modality-specificity-calibration-v1.json"
PDF_EXTRACTOR_PATH = ROOT / "wiki/survey/current/data/pdf-extractor-environment-v1.json"
REVIEWER_KNOWN_PATH = ROOT / "wiki/survey/current/data/reviewer-known-items-v3.json"
MAPPING_METHODS_PATH = ROOT / "wiki/survey/current/mapping-methods-adaptation.md"
MODALITY_CODEBOOK_PATH = ROOT / "wiki/survey/current/modality-specificity-codebook.md"
UNION_CHECK_PATH = (
    ROOT
    / "docs/checks/system-first-stage1a/context-v2/"
    "existing-corpus-disposition-check.json"
)
RECEIPTS_PATH = ROOT / "wiki/survey/current/data/official-metadata-receipts-v1.jsonl"
SELECTION_PATH = ROOT / "wiki/survey/current/data/reviewer-bibliography-selection-v1.json"
V7_DIRECTORY = ROOT / "docs/checks/system-first-stage1a/evidence-v7"
V7_NAMES = (
    "identity-taxonomy-v7-test.nt.json",
    "identity-taxonomy-v7-test.posix.json",
    "identity-taxonomy-v7-test.json",
)

EVIDENCE_BINDINGS = {
    "wiki/Project-Thesis.md": "wiki/Project-Thesis.md",
    "wiki/Research-Objective.md": "wiki/Research-Objective.md",
    "v10 proposal": "wiki/2026-07-19-system-first-research-proposal-v10-consolidated.md",
    "round-14 adversarial review": "wiki/audit/system-first-stage1a/round-14/stage1a-final-gates-plan-doctoral-adversarial-review.md",
    "round-15 independent review": "wiki/audit/system-first-stage1a/pre-round-15/2026-07-21-independent-doctoral-review-of-stage1a-research-proposal.md",
    "round-16 precheck rereview": "wiki/audit/external-reviews/2026-07-21-round16-precheck-rereview-of-stage1a-research-proposal.md",
    "revised release design": "docs/superpowers/specs/2026-07-20-reviewer-proposal-and-master-release-design.md",
    "revised implementation plan": "docs/superpowers/plans/2026-07-20-stage1a-final-gates-and-reviewer-proposal.md",
    "negative-evidence review artifact": "wiki/survey/current/data/absence-evidence-adjudication-v3.json",
    "semantic-correction artifact": "wiki/survey/current/data/negative-evidence-semantic-corrections-v2.json",
    "lossless union graph": "wiki/survey/current/data/existing-corpus-disposition-v1.json",
    "union machine check": "docs/checks/system-first-stage1a/context-v2/existing-corpus-disposition-check.json",
    "reviewer-known items": "wiki/survey/current/data/reviewer-known-items-v3.json",
    "official metadata receipts": "wiki/survey/current/data/official-metadata-receipts-v1.jsonl",
    "generated 90-work bibliography": "wiki/survey/current/bibliography.md",
    "bibliography selection receipt": "wiki/survey/current/data/reviewer-bibliography-selection-v1.json",
    "mapping methods adaptation": "wiki/survey/current/mapping-methods-adaptation.md",
    "speech/omni specificity codebook": "wiki/survey/current/modality-specificity-codebook.md",
    "H5 calibration artifact": "wiki/survey/current/data/modality-specificity-calibration-v1.json",
    "PDF extractor environment": "wiki/survey/current/data/pdf-extractor-environment-v1.json",
    "current protocol": "wiki/survey/current/protocol.md",
    "current status": "wiki/survey/current/status.md",
    "frozen evidence-v6 aggregate": "docs/checks/system-first-stage1a/evidence-v6/identity-taxonomy-v6-test.json",
    "frozen query bytes": "wiki/survey/2026-07-15-sf-queries.jsonl",
    "attempt registry": "docs/integrity/experiment_attempt_registry.jsonl",
    "wiki dry-run incident": "docs/checks/system-first-stage1a/context-v1/wiki-sync-dry-run-incident.json",
}

DIRECT_NEIGHBORS = (
    "AudioToolAgent",
    "Audio-Mind",
    "Agent-Omni",
    "EChO-Agent",
    "AuTAgent",
    "Speech-Copilot",
    "VoxMind",
    "WavReward",
    "GSRM",
    "Thinking While Listening",
    "Native Active Perception",
    "Llasa",
    "OmniGAIA",
    "Sandboxed Coding Agents are Competitive Omni-modal Task Solvers",
    "Inference-Time Scaling for Joint Audio-Video Generation",
    "Agentic Reward Modeling",
    "TMAS",
    "AgentTTS",
)


def load_inputs() -> dict[str, Any]:
    receipts = [
        json.loads(line)
        for line in RECEIPTS_PATH.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    return {
        "absence": json.loads(ABSENCE_PATH.read_text(encoding="utf-8")),
        "corrections": json.loads(CORRECTIONS_PATH.read_text(encoding="utf-8")),
        "union": json.loads(UNION_CHECK_PATH.read_text(encoding="utf-8")),
        "receipts": receipts,
        "selection": json.loads(SELECTION_PATH.read_text(encoding="utf-8")),
        "h5": json.loads(H5_PATH.read_text(encoding="utf-8")),
        "pdf_extractor": json.loads(PDF_EXTRACTOR_PATH.read_text(encoding="utf-8")),
        "reviewer_known": json.loads(REVIEWER_KNOWN_PATH.read_text(encoding="utf-8")),
    }


def _git_blob_binding(path: str) -> tuple[str, str]:
    blob = subprocess.run(
        ["git", "rev-parse", f"HEAD:{path}"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    raw = subprocess.run(
        ["git", "show", f"HEAD:{path}"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    ).stdout
    return blob, hashlib.sha256(raw).hexdigest()


def _evidence_binding_failures(text: str) -> list[str]:
    failures = []
    lines = text.splitlines()
    for label, path in EVIDENCE_BINDINGS.items():
        matching = []
        for line in lines:
            if not line.startswith("|"):
                continue
            first_cell = line.split("|", 2)[1].strip().strip("`")
            if first_cell == label:
                matching.append(line)
        if len(matching) != 1:
            failures.append("EVIDENCE_BINDING_MISMATCH")
            continue
        blob, sha256 = _git_blob_binding(path)
        if blob not in matching[0] or sha256 not in matching[0]:
            failures.append("EVIDENCE_BINDING_MISMATCH")
    return failures


def _required_structure_failures(text: str) -> list[str]:
    required = {
        "TRACK_A_MISSING": "## Track A",
        "TRACK_B_MISSING": "## Track B",
        "FALSIFIERS_MISSING": "## 8. 证伪条件",
        "RISKS_AND_LIMITATIONS_MISSING": "## 9. 风险、限制与博士价值",
        "RQ_STAGE_MATRIX_MISSING": "answering_stage",
        "METHODS_ADAPTATION_MISSING": "mapping-methods-adaptation.md",
        "MODALITY_CODEBOOK_MISSING": "modality-specificity-codebook.md",
        "H5_CALIBRATION_ARTIFACT_MISSING": "modality-specificity-calibration-v1.json",
        "PDF_EXTRACTOR_CONTRACT_MISSING": "pdf-extractor-environment-v1.json",
        "STAGE1C_OWNERSHIP_MISSING": "Stage-1C owns the final 3–5 candidate cards",
        "BIBLIOGRAPHY_SELECTION_MISSING": "reviewer-bibliography-selection-v1.json",
        "YEAR_POLICY_MISSING": "year_basis",
        "ACTIVE_CORPUS_SCOPE_MISSING": "seven registered active corpora",
        "PROPOSAL_SOURCE_PACKAGE_MISSING": "proposal-source-manifest-v1.json",
        "PROPOSAL_PACKAGE_REPORT_MISSING": "proposal-package-check.json",
    }
    failures = [code for code, token in required.items() if token not in text]
    response_lines = (
        "SCIENTIFIC_RATIONALE_FOR_CONTINUING_MAPPING = ADEQUATE|REVISE|INADEQUATE",
        "SEARCH_DESIGN_SIGNOFF = SIGN|WITHHOLD",
    )
    if any(line not in text for line in response_lines):
        failures.append("RESPONSE_SCHEMA_MISSING")
    return failures


def _forbidden_claim_failures(text: str, inputs: dict[str, Any]) -> list[str]:
    failures = []
    if re.search(
        r"(?m)^SCIENTIFIC_RATIONALE_FOR_CONTINUING_MAPPING\s*=\s*(?:ADEQUATE|REVISE|INADEQUATE)\s*$",
        text,
    ) or re.search(
        r"(?m)^SEARCH_DESIGN_SIGNOFF\s*=\s*(?:SIGN|WITHHOLD)\s*$",
        text,
    ):
        failures.append("ACTUAL_REVIEWER_VERDICT_FORBIDDEN")
    if "execution_authorized=true" in text or "STAGE1B_READY" in text:
        failures.append("STAGE1B_AUTHORIZATION_FORBIDDEN")
    if "EXACT_PACKAGE_SIGNED=true" in text:
        failures.append("EXACT_PACKAGE_SIGNOFF_FORBIDDEN")
    if "SUBMITTED_FOR_INDEPENDENT_REVIEW" in text:
        failures.append("FORMAL_SUBMISSION_CLAIM_FORBIDDEN_IN_DRAFT")
    return failures


def _numeric_failures(text: str, inputs: dict[str, Any]) -> list[str]:
    failures = []
    union = inputs["union"]
    summary = union["summary"]
    union_phrases = (
        f"{summary['source_rows']} 个物理 source rows",
        f"{summary['canonical_work_nodes']} 个 canonical work nodes",
        f"{summary['claim_edges']} 条 claim row",
        f"{summary['load_bearing_unresolved']}。`unexplained_orphans=0`",
    )
    if any(phrase not in text for phrase in union_phrases):
        failures.append("UNION_NUMERIC_DRIFT")

    receipts = inputs["receipts"]
    identity_counts = Counter(row["identity"]["kind"] for row in receipts)
    bibliography_phrases = (
        f"{len(receipts)} 个 unique works",
        f"{identity_counts['arxiv']} 个 arXiv、{identity_counts['acl']} 个 ACL、{identity_counts['github']} 个 GitHub identity",
    )
    if any(phrase not in text for phrase in bibliography_phrases):
        failures.append("BIBLIOGRAPHY_NUMERIC_DRIFT")
    selection = inputs["selection"]
    selection_phrases = (
        f"{selection['union_population']} 个 active-union nodes",
        f"{selection['selected_from_union']} 个 selected",
        f"{selection['union_reason_code_counts']['NOT_SELECTED_NONPRIORITY_KNOWN_QUEUE']} 个 `NOT_SELECTED_NONPRIORITY_KNOWN_QUEUE`",
        f"{selection['union_reason_code_counts']['NOT_SELECTED_UNRESOLVED_IDENTITY']} 个 `NOT_SELECTED_UNRESOLVED_IDENTITY`",
    )
    if any(phrase not in text for phrase in selection_phrases):
        failures.append("BIBLIOGRAPHY_SELECTION_NUMERIC_DRIFT")

    absence = inputs["absence"]
    proof_count = len(absence.get("proof_rows", []))
    review_count = len(absence.get("rows", []))
    absence_phrases = (
        f"{proof_count} 个 proof rows、{review_count} 个 reviewer rows",
        f"coverage {review_count}/{proof_count}",
        absence.get("inventory_identity", ""),
    )
    if any(phrase not in text for phrase in absence_phrases):
        failures.append("ABSENCE_COUNT_DRIFT")
    corrections = inputs["corrections"]
    correction_phrases = (
        f"exactly {len(corrections.get('corrections', []))}/22 semantic corrections",
        f"{len(corrections.get('corrections', []))} 个 correction rows、{len(corrections.get('review_rows', []))} 个 reviewer rows",
        corrections.get("inventory_reconciliation", {}).get("identity", ""),
    )
    if any(phrase not in text for phrase in correction_phrases):
        failures.append("CORRECTION_COUNT_DRIFT")
    h5 = inputs["h5"]
    h5_phrases = (
        f"H5 calibration status={h5.get('status')}",
        f"planned denominator={h5.get('agreement_report', {}).get('planned_denominator')}",
        f"observed comparable denominator={h5.get('agreement_report', {}).get('observed_comparable_denominator')}",
    )
    if any(phrase not in text for phrase in h5_phrases):
        failures.append("H5_CALIBRATION_STATE_DRIFT")
    reviewer_known = inputs["reviewer_known"]
    if f"{len(reviewer_known.get('items', []))} reviewer-known items" not in text:
        failures.append("REVIEWER_KNOWN_COUNT_DRIFT")
    environments = inputs["pdf_extractor"].get("canonical_environments", {})
    for role in ("nt", "posix"):
        version = environments.get(role, {}).get("pypdf_version")
        if f"pypdf {version}" not in text:
            failures.append("PDF_EXTRACTOR_VERSION_DRIFT")
    return failures


def validate_draft(text: str, inputs: dict[str, Any] | None = None) -> list[str]:
    inputs = inputs or load_inputs()
    failures = []
    failures.extend(_required_structure_failures(text))
    failures.extend(_forbidden_claim_failures(text, inputs))
    failures.extend(_numeric_failures(text, inputs))
    failures.extend(_evidence_binding_failures(text))
    if 'lifecycle: "WORKBENCH_REVIEW_DRAFT"' not in text:
        failures.append("DRAFT_LIFECYCLE_MISSING")
    if any(neighbor not in text for neighbor in DIRECT_NEIGHBORS):
        failures.append("DIRECT_NEIGHBOR_CLOSURE_MISSING")
    exposure_tokens = (
        "systematic discovery-query execution 为 0",
        "research-model calls 为 0",
        "known-ID metadata/provenance access 非零",
        "INHERITED_PRIOR_EXPOSURE",
        "429",
    )
    if any(token not in text for token in exposure_tokens):
        failures.append("EXPOSURE_OR_INCIDENT_DISCLOSURE_MISSING")
    return sorted(set(failures))


def validate_release(text: str, inputs: dict[str, Any] | None = None) -> list[str]:
    inputs = inputs or load_inputs()
    failures = validate_draft(text, inputs)
    absence = inputs["absence"]
    proof_ids = {
        row.get("adjudication_row_id") for row in absence.get("proof_rows", [])
    }
    review_ids = {
        row.get("adjudication_row_id") for row in absence.get("rows", [])
    }
    if (
        absence.get("status") != "INDEPENDENT_REVIEW_RECORDED_UNVALIDATED"
        or len(proof_ids) != inputs["absence"].get("active_proof_inventory_count")
        or review_ids != proof_ids
        or any(
            row.get("verdict") not in {"AGREE", "AGREE_WITH_CAUTION"}
            for row in absence.get("rows", [])
        )
    ):
        failures.append("ABSENCE_REVIEW_PENDING")
    corrections = inputs["corrections"]
    correction_ids = {
        row.get("retired_adjudication_row_id")
        for row in corrections.get("corrections", [])
    }
    correction_review_ids = {
        row.get("retired_adjudication_row_id")
        for row in corrections.get("review_rows", [])
    }
    if (
        corrections.get("inventory_reconciliation", {}).get("identity")
        != f"22 = {len(correction_ids)} + {len(proof_ids)}"
        or len(correction_ids) + len(proof_ids) != 22
        or correction_review_ids != correction_ids
        or any(
            row.get("verdict") not in {"AGREE", "DISAGREE_RECODE_REQUIRED"}
            for row in corrections.get("review_rows", [])
        )
    ):
        failures.append("SEMANTIC_CORRECTION_REVIEW_PENDING")
    correction_index = {
        row.get("retired_adjudication_row_id"): row
        for row in corrections.get("corrections", [])
    }
    for row in corrections.get("review_rows", []):
        if row.get("verdict") == "DISAGREE_RECODE_REQUIRED" and row.get(
            "required_recode"
        ) != correction_index.get(row.get("retired_adjudication_row_id"), {}).get(
            "corrected_value"
        ):
            failures.append("SEMANTIC_CORRECTION_REVIEW_PENDING")
    if validate_h5_completion(inputs.get("h5", {})):
        failures.append("H5_CALIBRATION_PENDING")
    if validate_pdf_contract(inputs.get("pdf_extractor", {})):
        failures.append("PDF_EXTRACTOR_ENVIRONMENT_UNFROZEN")
    reviewer_known = inputs.get("reviewer_known", {})
    required_known_ids = {
        "2606.00579", "2606.03183", "2502.19328", "2605.10344", "2508.00890"
    }
    known_rows = {
        row.get("arxiv_id"): row
        for row in reviewer_known.get("items", [])
        if isinstance(row, dict)
    }
    if not required_known_ids <= set(known_rows) or any(
        not known_rows[item_id].get("current_disposition", {}).get("reason")
        or not known_rows[item_id].get("current_disposition", {}).get("next_action")
        or known_rows[item_id].get("query_recall_credit") is not False
        for item_id in required_known_ids
    ):
        failures.append("REVIEWER_KNOWN_ITEMS_UNDISPOSITIONED")
    if any(not (V7_DIRECTORY / name).is_file() for name in V7_NAMES):
        failures.append("EVIDENCE_V7_LEAVES_OR_AGGREGATE_MISSING")
    if not ROUND16_PATH.is_file() or PROPOSAL_PATH == ROUND16_PATH:
        failures.append("PROPOSAL_NOT_PROMOTED_TO_ROUND16")
    return sorted(set(failures))


def _write_report(path: Path, mode: str, failures: list[str]) -> None:
    report = {
        "artifact_id": "SF-REVIEWER-PROPOSAL-CHECK-DRAFT-2026-07-21-01",
        "mode": mode,
        "proposal": PROPOSAL_PATH.relative_to(ROOT).as_posix(),
        "verdict": "PASS" if not failures else "FAIL",
        "failure_codes": failures,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=("draft", "release"), required=True)
    parser.add_argument("--proposal", type=Path, default=PROPOSAL_PATH)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    proposal = args.proposal if args.proposal.is_absolute() else ROOT / args.proposal
    text = proposal.read_text(encoding="utf-8")
    inputs = load_inputs()
    failures = (
        validate_draft(text, inputs)
        if args.mode == "draft"
        else validate_release(text, inputs)
    )
    if args.output:
        output = args.output if args.output.is_absolute() else ROOT / args.output
        _write_report(output, args.mode, failures)
    print(
        json.dumps(
            {
                "mode": args.mode,
                "verdict": "PASS" if not failures else "FAIL",
                "failure_codes": failures,
            },
            ensure_ascii=False,
        )
    )
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
