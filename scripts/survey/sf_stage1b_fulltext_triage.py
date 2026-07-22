#!/usr/bin/env python3
"""Extract and triage locally downloaded Stage-1B full texts.

PDFs and extracted text remain outside Git. The JSONL output is a derived decision ledger with page
locators; its decisions are deterministic pre-decisions that still require a bounded human audit.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import logging
import re
from pathlib import Path
from typing import Any, Iterable

import sf_stage1b_bounded_sampling as sampling

logging.getLogger("pypdf").setLevel(logging.ERROR)


TRAINING_TERMS = (
    "fine-tune", "fine tune", "finetune", "training", "trained", "gradient update",
    "reinforcement learning", "supervised learning",
)
INSTRUMENT_TERMS = (
    "benchmark", "evaluation", "evaluate", "metric", "word error rate", "wer",
    "test set", "test split", "toolkit",
)
REPO_HOSTS = ("github.com", "gitlab.com", "huggingface.co")
MAX_EVIDENCE = 8
STRONG_NO_UPDATE_TERMS = {
    "training-free", "training free", "tuning-free", "tuning free", "frozen",
    "without training", "without fine-tuning", "without finetuning", "off-the-shelf",
}


def _safe_utf8(text: str) -> str:
    return text.encode("utf-8", errors="replace").decode("utf-8")


def _urls(text: str) -> list[str]:
    compact = re.sub(r"(?<=\w)-\s*\n\s*(?=\w)", "", text)
    compact = re.sub(r"(?<=/)[\s\n]+(?=[A-Za-z0-9_.-])", "", compact)
    return sorted(set(url.rstrip(".,;:") for url in sampling.URL.findall(compact)))


def _evidence(pages: list[str], terms: Iterable[str], label: str) -> list[dict[str, Any]]:
    result = []
    needles = tuple(terms)
    for page_no, page in enumerate(pages, start=1):
        normalized = re.sub(r"\s+", " ", page)
        lowered = normalized.lower()
        for term in needles:
            position = lowered.find(term.lower())
            if position < 0:
                continue
            start = max(0, position - 120)
            end = min(len(normalized), position + len(term) + 180)
            result.append(
                {
                    "page": page_no,
                    "evidence_type": label,
                    "matched_term": term,
                    "snippet": normalized[start:end].strip(),
                }
            )
            if len(result) >= MAX_EVIDENCE:
                return result
    return result


def _repo_state(repo_urls: list[str], verification: dict[str, Any]) -> tuple[str, list[dict[str, Any]]]:
    if not repo_urls:
        return "NO_REPOSITORY_EVIDENCE", []
    details = []
    for url in repo_urls:
        raw = verification.get(url, "PAPER_LINKED_REPO_UNVERIFIED")
        if isinstance(raw, str):
            details.append({"url": url, "status": raw})
        else:
            details.append({"url": url, **dict(raw)})
    statuses = {item.get("status") for item in details}
    if "OPEN_SOURCE_VERIFIED" in statuses:
        return "OPEN_SOURCE_VERIFIED", details
    if "REPOSITORY_UNREACHABLE" in statuses:
        return "REPOSITORY_UNREACHABLE", details
    return "PAPER_LINKED_REPO_UNVERIFIED", details


def _paper_linked_repo_urls(row: dict[str, Any], pages: list[str]) -> list[str]:
    direct = {
        str(url)
        for url in (row.get("repo_urls") or [])
        if any(host in str(url).lower() for host in REPO_HOSTS)
    }
    for page in pages[:3]:
        compact = re.sub(r"\s+", " ", page)
        for url in _urls(page):
            if not any(host in url.lower() for host in REPO_HOSTS):
                continue
            position = compact.find(url)
            context = compact[max(0, position - 180): position + len(url) + 80].lower() if position >= 0 else ""
            release_cue = re.search(
                r"(?:our\s+)?(?:source\s+)?(?:code|implementation|repository|project\s+page)"
                r"\s*(?:is|are|will\s+be)?\s*(?:available|released|provided|at|on|:)",
                context,
            )
            dependency_cue = re.search(r"(?:builds?\s+on|based\s+on|depend(?:s|ency)|using|we\s+use)\b", context)
            if release_cue and not dependency_cue:
                direct.add(url)
    return sorted(direct)


def analyze_pages(
    row: dict[str, Any],
    pages: list[str],
    datasets: sampling.DatasetCatalog,
    repo_verification: dict[str, Any] | None = None,
) -> dict[str, Any]:
    verification_supplied = repo_verification is not None
    analysis_pages = []
    for page in pages:
        if re.search(r"(?:^|\n)\s*(?:references|bibliography)\b", page, re.IGNORECASE):
            break
        analysis_pages.append(page)
    if not analysis_pages:
        analysis_pages = pages[:1]
    text = "\n".join(analysis_pages)
    signal_hits = sampling._phrase_hits(text, sampling.SIGNAL_TERMS)
    decision_hits = sampling._phrase_hits(text, sampling.DECISION_TERMS)
    no_update_hits = sampling._phrase_hits(text, sampling.NO_UPDATE_TERMS)
    transfer_hits = sampling._phrase_hits(text, sampling.TRANSFER_TERMS)
    adverse_hits = sampling._phrase_hits(text, sampling.ADVERSE_TERMS)
    training_hits = sampling._phrase_hits(text, TRAINING_TERMS)
    instrument_hits = sampling._phrase_hits(text, INSTRUMENT_TERMS)
    dataset_mentions = datasets.match(text)
    speech_dataset_mentions = [
        item
        for item in dataset_mentions
        if str(item.get("task") or "").lower() not in sampling.NON_SPEECH_DATASET_TASKS
    ]
    repo_urls = _paper_linked_repo_urls(row, analysis_pages)
    repo_status, repo_details = _repo_state(repo_urls, repo_verification or {})

    primary_speech = bool(row.get("speech_primary_object"))
    local_status = "NOT_STATED_IN_FULLTEXT" if primary_speech else "NOT_APPLICABLE_NON_SPEECH"
    if primary_speech and speech_dataset_mentions:
        local_status = (
            "LOCAL_MATCH"
            if any(item["local_present"] for item in speech_dataset_mentions)
            else "LOCK_MATCH_NOT_PRESENT"
        )
    task_tags = set(row.get("speech_task_tags") or [])
    for item in dataset_mentions:
        dataset_task = str(item.get("task") or "").lower()
        by_tag = {
            tag: (
                "TASK_MATCH"
                if dataset_task and (tag in dataset_task or dataset_task in tag)
                else "REQUIRES_SPLIT_REVIEW"
            )
            for tag in sorted(task_tags)
        }
        item["task_suitability_by_tag"] = by_tag
        item["task_suitability"] = (
            "TASK_MATCH"
            if "TASK_MATCH" in by_tag.values()
            else "REQUIRES_SPLIT_REVIEW"
        )

    strong_signal = bool(set(signal_hits) & sampling.STRONG_SIGNAL_TERMS)
    control_path = any(
        bool(set(sampling._phrase_hits(page, sampling.SIGNAL_TERMS)) & sampling.STRONG_SIGNAL_TERMS)
        and bool(sampling._phrase_hits(page, sampling.DECISION_TERMS))
        for page in analysis_pages
    )
    no_update_path = bool(set(no_update_hits) & STRONG_NO_UPDATE_TERMS)
    training_conflict = bool(no_update_hits and training_hits)
    transferable = bool(transfer_hits) and control_path
    reasons = []

    if primary_speech and control_path and no_update_path:
        decision = "KEEP_CORE"
        reasons.extend(("PRIMARY_SPEECH_CONTROL_PATH", "NO_WEIGHT_UPDATE_EVIDENCE"))
    elif primary_speech and adverse_hits and control_path:
        decision = "KEEP_NEGATIVE"
        reasons.extend(("PRIMARY_SPEECH_CONTROL_PATH", "ADVERSE_OR_LIMITATION_EVIDENCE"))
    elif primary_speech and instrument_hits and (speech_dataset_mentions or control_path):
        decision = "KEEP_INSTRUMENT"
        reasons.extend(("PRIMARY_SPEECH_TASK", "LOCAL_OR_LOCKED_DATASET_INSTRUMENT"))
    elif not primary_speech and transferable and no_update_path:
        if repo_status == "OPEN_SOURCE_VERIFIED":
            decision = "KEEP_TRANSFER"
            reasons.extend(("TRANSFERABLE_CONTROL_PATH", "OPEN_SOURCE_VERIFIED"))
        elif repo_urls:
            if verification_supplied:
                decision = "DROP"
                reasons.extend(("TRANSFERABLE_CONTROL_PATH", "REPRODUCIBILITY_GATE_FAILED"))
            else:
                decision = "DEFER_REPO_VERIFY"
                reasons.extend(("TRANSFERABLE_CONTROL_PATH", "REPOSITORY_REQUIRES_VERIFICATION"))
        else:
            decision = "DROP"
            reasons.append("NON_SPEECH_WITHOUT_REPOSITORY")
    elif not primary_speech and adverse_hits and control_path:
        decision = "KEEP_NEGATIVE"
        reasons.append("TRANSFER_BOUNDARY_OR_ADVERSE_EVIDENCE")
    else:
        decision = "DROP"
        reasons.append("NO_RETAINABLE_FULLTEXT_PATH")

    locators = []
    for terms, label in (
        (signal_hits, "CONTROL_SIGNAL"),
        (decision_hits, "DECISION_ACTION"),
        (no_update_hits, "NO_UPDATE"),
        ([item["canonical_name"] for item in dataset_mentions], "DATASET"),
        (adverse_hits, "ADVERSE"),
    ):
        locators.extend(_evidence(pages, terms, label))
        if len(locators) >= MAX_EVIDENCE:
            break

    return {
        "schema": "sf-stage1b-fulltext-triage-v1",
        "arxiv_id": row.get("arxiv_id"),
        "title": row.get("title"),
        "sample_round": row.get("sample_round"),
        "speech_primary_object": primary_speech,
        "speech_task_tags": sorted(task_tags),
        "dataset_mentions": dataset_mentions,
        "speech_dataset_mentions": speech_dataset_mentions,
        "dataset_local_status": local_status,
        "control_signal_terms": signal_hits,
        "decision_action_terms": decision_hits,
        "no_update_terms": no_update_hits,
        "training_terms": training_hits,
        "training_conflict_requires_audit": training_conflict,
        "strong_no_weight_update_evidence": no_update_path,
        "transfer_object_terms": transfer_hits,
        "adverse_terms": adverse_hits,
        "instrument_terms": instrument_hits,
        "repo_urls": repo_urls,
        "repo_status": repo_status,
        "repo_details": repo_details,
        "fulltext_pages": len(pages),
        "analysis_pages_before_references": len(analysis_pages),
        "control_path_page_cooccurrence": control_path,
        "evidence_locators": locators[:MAX_EVIDENCE],
        "final_decision": decision,
        "final_reason_codes": reasons,
        "decision_origin": "DETERMINISTIC_FULLTEXT_TRIAGE_REQUIRES_AUDIT",
    }


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text("utf-8").splitlines() if line.strip()]


def _read_audit_promotions(path: Path | None) -> dict[str, dict[str, Any]]:
    if path is None:
        return {}
    rows = json.loads(path.read_text("utf-8"))
    if not isinstance(rows, list):
        raise ValueError("audit promotions must be a JSON array")
    promotions: dict[str, dict[str, Any]] = {}
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError("each audit promotion must be an object")
        aid = str(row.get("arxiv_id", "")).strip()
        if not aid or row.get("to_disposition") != "AUDIT_SELECT_FULLTEXT":
            raise ValueError("audit promotion requires arxiv_id and AUDIT_SELECT_FULLTEXT")
        if aid in promotions:
            raise ValueError(f"duplicate audit promotion: {aid}")
        promotions[aid] = row
    return promotions


def _load_repo_verifications(paths: Path | list[Path] | None) -> dict[str, Any]:
    if paths is None:
        return {}
    receipts = [paths] if isinstance(paths, Path) else list(paths)
    status_rank = {
        "REPOSITORY_UNREACHABLE": 0,
        "NON_GITHUB_REQUIRES_MANUAL_VERIFICATION": 1,
        "REPOSITORY_REACHABLE_LICENSE_UNRESOLVED": 2,
        "INSPECTABLE_BUT_REPRO_INCOMPLETE": 3,
        "OPEN_SOURCE_VERIFIED": 4,
    }
    merged: dict[str, Any] = {}
    for path in receipts:
        if not path.exists():
            continue
        payload = json.loads(path.read_text("utf-8"))
        if not isinstance(payload, dict):
            raise ValueError(f"repository verification receipt must be an object: {path}")
        for url, value in payload.items():
            prior = merged.get(url)
            if prior is None or status_rank.get(str(value.get("status")), -1) > status_rank.get(
                str(prior.get("status")), -1
            ):
                merged[url] = value
    return merged


def _extract_pdf(path: Path) -> list[str]:
    from pypdf import PdfReader

    return [_safe_utf8(page.extract_text() or "") for page in PdfReader(path).pages]


def run(args: argparse.Namespace) -> dict[str, Any]:
    catalog = sampling.DatasetCatalog.from_lock(args.dataset_lock, args.data_root)
    verification = _load_repo_verifications(getattr(args, "repo_verification", None))
    promotions = _read_audit_promotions(getattr(args, "audit_promotions", None))
    selected: dict[str, dict[str, Any]] = {}
    for manifest in args.manifest:
        for row in _read_jsonl(manifest):
            aid = str(row["arxiv_id"])
            if row.get("abstract_disposition") == "SELECT_FULLTEXT":
                selected[aid] = {
                    **row,
                    "fulltext_selection_origin": "DETERMINISTIC_SELECT_FULLTEXT",
                    "source_abstract_disposition": "SELECT_FULLTEXT",
                }
            elif aid in promotions:
                promotion = promotions[aid]
                source = str(row.get("abstract_disposition", ""))
                expected = str(promotion.get("from_disposition", ""))
                if expected and source != expected:
                    raise ValueError(
                        f"audit promotion source mismatch for {aid}: {source!r} != {expected!r}"
                    )
                selected[aid] = {
                    **row,
                    "abstract_disposition": "AUDIT_SELECT_FULLTEXT",
                    "fulltext_selection_origin": "AUDIT_PROMOTION",
                    "source_abstract_disposition": source,
                    "audit_promotion_reason": promotion.get("reason"),
                    "audit_promotion_repository_gate": promotion.get("repository_gate"),
                    "audit_promotion_repository_url": promotion.get("repository_url"),
                }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    text_dir = args.output_dir / "extracted-text"
    text_dir.mkdir(parents=True, exist_ok=True)
    results = []
    for aid, row in sorted(selected.items()):
        pdf_path = args.pdf_root / aid / f"{aid}.pdf"
        if not pdf_path.is_file() or pdf_path.stat().st_size < 1024:
            results.append(
                {
                    "schema": "sf-stage1b-fulltext-triage-v1",
                    "arxiv_id": aid,
                    "title": row.get("title"),
                    "sample_round": row.get("sample_round"),
                    "fulltext_selection_origin": row.get("fulltext_selection_origin"),
                    "source_abstract_disposition": row.get("source_abstract_disposition"),
                    "audit_promotion_reason": row.get("audit_promotion_reason"),
                    "fulltext_status": "PDF_MISSING",
                    "final_decision": "DEFER_DOWNLOAD",
                    "final_reason_codes": ["PDF_NOT_AVAILABLE_LOCALLY"],
                    "decision_origin": "DOWNLOAD_STATE",
                }
            )
            continue
        try:
            raw = pdf_path.read_bytes()
            pages = _extract_pdf(pdf_path)
            result = analyze_pages(row, pages, catalog, verification)
            result.update(
                {
                    "fulltext_selection_origin": row.get("fulltext_selection_origin"),
                    "source_abstract_disposition": row.get("source_abstract_disposition"),
                    "audit_promotion_reason": row.get("audit_promotion_reason"),
                    "audit_promotion_repository_gate": row.get(
                        "audit_promotion_repository_gate"
                    ),
                    "audit_promotion_repository_url": row.get(
                        "audit_promotion_repository_url"
                    ),
                }
            )
            extracted = _safe_utf8(
                "\n\n".join(f"=== PAGE {index} ===\n{text}" for index, text in enumerate(pages, 1))
            )
            text_path = text_dir / f"{aid}.txt"
            text_path.write_text(extracted, encoding="utf-8", newline="\n")
            result.update(
                {
                    "fulltext_status": "PDF_EXTRACTED",
                    "pdf_path": pdf_path.as_posix(),
                    "pdf_bytes": len(raw),
                    "pdf_sha256": hashlib.sha256(raw).hexdigest(),
                    "extracted_text_path": text_path.as_posix(),
                    "extracted_text_bytes": len(extracted.encode("utf-8")),
                }
            )
            results.append(result)
        except Exception as exc:  # fail closed and retain the item for retry
            results.append(
                {
                    "schema": "sf-stage1b-fulltext-triage-v1",
                    "arxiv_id": aid,
                    "title": row.get("title"),
                    "sample_round": row.get("sample_round"),
                    "fulltext_selection_origin": row.get("fulltext_selection_origin"),
                    "source_abstract_disposition": row.get("source_abstract_disposition"),
                    "audit_promotion_reason": row.get("audit_promotion_reason"),
                    "fulltext_status": "EXTRACTION_FAILED",
                    "extraction_error": f"{type(exc).__name__}: {exc}",
                    "final_decision": "DEFER_EXTRACTION",
                    "final_reason_codes": ["PDF_EXTRACTION_FAILED"],
                    "decision_origin": "EXTRACTION_STATE",
                }
            )

    output_path = args.output_dir / "fulltext-triage.jsonl"
    payload = "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in results)
    output_path.write_text(payload, encoding="utf-8", newline="\n")
    counts = {}
    for row in results:
        counts[row["final_decision"]] = counts.get(row["final_decision"], 0) + 1
    summary = {
        "schema": "sf-stage1b-fulltext-triage-summary-v1",
        "selected_unique": len(selected),
        "deterministic_selected": sum(
            row.get("fulltext_selection_origin") == "DETERMINISTIC_SELECT_FULLTEXT"
            for row in selected.values()
        ),
        "audit_promotions_selected": sum(
            row.get("fulltext_selection_origin") == "AUDIT_PROMOTION"
            for row in selected.values()
        ),
        "processed_rows": len(results),
        "decision_counts": dict(sorted(counts.items())),
        "ledger_path": output_path.as_posix(),
        "ledger_bytes": len(payload.encode("utf-8")),
        "ledger_sha256": hashlib.sha256(payload.encode("utf-8")).hexdigest(),
    }
    (args.output_dir / "fulltext-triage-summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, action="append", required=True)
    parser.add_argument("--audit-promotions", type=Path)
    parser.add_argument("--dataset-lock", type=Path, required=True)
    parser.add_argument("--data-root", type=Path, required=True)
    parser.add_argument("--pdf-root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--repo-verification", type=Path, action="append")
    args = parser.parse_args()
    print(json.dumps(run(args), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
