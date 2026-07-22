#!/usr/bin/env python3
"""Build a deterministic Stage-1B abstract-review priority queue from D0.

This is a queueing aid, not a screener.  It uses explicit lexical evidence, query-lane provenance,
and recency to order records for human abstract review.  It never emits INCLUDED/EXCLUDED or changes
the D0 source snapshot.  Forced known items enter with their reason and no forced-query recall credit.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


ARXIV_ID = re.compile(r"(?<!\d)(\d{4}\.\d{4,5})(?:v\d+)?(?!\d)")
REQUIRED = {"arxiv_id", "title", "abstract", "published", "source_query_ids"}

TERM_GROUPS = {
    "multimodal_object": (
        "multimodal", "multi-modal", "omni", "audio", "speech", "spoken", "voice",
        "vision-language", "vision language", "vlm", "mllm",
    ),
    "control_signal": (
        "reward", "verifier", "verification", "critic", "critique", "judge", "feedback",
        "reflection", "self-evaluation", "self evaluation", "value model", "value-guided",
        "value guided", "uncertainty", "confidence",
    ),
    "decision_action": (
        "search", "routing", "route", "select", "selection", "stopping", "stop", "retry",
        "tool use", "tool-use", "tool calling", "planning", "orchestration", "decoding",
        "steering", "best-of-n", "best of n", "self-consistency", "self consistency",
        "test-time scaling", "inference-time scaling", "reobserve", "re-observe", "abstain",
    ),
    "frozen_or_test_time": (
        "training-free", "training free", "tuning-free", "tuning free", "frozen",
        "without fine-tuning", "without finetuning", "no fine-tuning", "inference-time",
        "inference time", "test-time", "test time", "off-the-shelf",
    ),
    "adverse_or_boundary": (
        "failure", "fail", "limitation", "no improvement", "unreliable", "reward hacking",
        "overoptimization", "over-optimization", "robustness", "regression", "bias",
        "leakage", "ablation", "upper bound", "oracle",
    ),
}

GROUP_WEIGHTS = {
    "multimodal_object": 4,
    "control_signal": 5,
    "decision_action": 5,
    "frozen_or_test_time": 5,
    "adverse_or_boundary": 3,
}


class PriorityBuildError(RuntimeError):
    """Fail-closed input or queue construction error."""


def _contains(text: str, term: str) -> bool:
    pattern = r"(?<![a-z0-9])" + re.escape(term) + r"(?![a-z0-9])"
    return re.search(pattern, text) is not None


def _hits(text: str, terms: tuple[str, ...]) -> list[str]:
    return [term for term in terms if _contains(text, term)]


def load_candidates(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    seen: set[str] = set()
    for line_no, line in enumerate(path.read_text("utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise PriorityBuildError(f"line {line_no}: invalid JSON: {exc}") from exc
        missing = sorted(REQUIRED - row.keys())
        if missing:
            raise PriorityBuildError(f"line {line_no}: missing required fields {missing}")
        arxiv_id = str(row["arxiv_id"])
        if arxiv_id in seen:
            raise PriorityBuildError(f"line {line_no}: duplicate arXiv ID {arxiv_id}")
        seen.add(arxiv_id)
        rows.append(row)
    return rows


def score_candidate(row: dict[str, Any]) -> dict[str, Any]:
    text = f"{row.get('title', '')} {row.get('abstract', '')}".lower()
    evidence = {name: _hits(text, terms) for name, terms in TERM_GROUPS.items()}
    present = {name: bool(hits) for name, hits in evidence.items()}
    query_ids = sorted(set(row.get("source_query_ids") or []))
    lane14_15 = [qid for qid in query_ids if qid.startswith(("SF-L14", "SF-L15"))]

    components = {
        name: GROUP_WEIGHTS[name] if present[name] else 0 for name in TERM_GROUPS
    }
    components.update(
        {
            "object_control_interaction": 5
            if present["multimodal_object"]
            and (present["control_signal"] or present["decision_action"])
            else 0,
            "method_lane_provenance": 5 * len(lane14_15),
            "multi_query_lineage": min(4, len(query_ids)),
            "agent_era_recency": 4 if str(row.get("published", ""))[:4] >= "2025" else 0,
        }
    )

    trigger_suggestions = []
    if present["multimodal_object"]:
        trigger_suggestions.append("T-a")
    if present["control_signal"] and present["decision_action"]:
        trigger_suggestions.append("T-b")
    if present["decision_action"] or present["frozen_or_test_time"]:
        trigger_suggestions.append("T-c")
    if present["adverse_or_boundary"]:
        trigger_suggestions.append("T-d")

    keep = {
        key: row.get(key)
        for key in (
            "arxiv_id", "title", "abstract", "authors", "published", "updated", "categories",
            "primary_category", "source_query_ids", "query_recall_credit",
        )
        if key in row
    }
    keep.update(
        {
            "priority_score": sum(components.values()),
            "score_components": components,
            "lexical_evidence": evidence,
            "trigger_suggestions": trigger_suggestions,
            "review_state": "ABSTRACT_REVIEW_PENDING",
            "not_a_screening_decision": True,
            "forced_entry": False,
            "forced_reason": None,
            "query_recall_credit_for_forced_entry": None,
        }
    )
    return keep


def _date_key(value: Any) -> int:
    digits = "".join(ch for ch in str(value)[:10] if ch.isdigit())
    return int(digits or 0)


def rank_candidates(
    candidates: list[dict[str, Any]],
    excluded_ids: set[str],
    forced_ids: dict[str, str] | None = None,
) -> list[dict[str, Any]]:
    forced_ids = forced_ids or {}
    ranked = []
    for row in candidates:
        arxiv_id = str(row["arxiv_id"])
        if arxiv_id in excluded_ids:
            continue
        scored = score_candidate(row)
        if arxiv_id in forced_ids:
            scored["forced_entry"] = True
            scored["forced_reason"] = forced_ids[arxiv_id]
            scored["query_recall_credit_for_forced_entry"] = False
        ranked.append(scored)

    # Stable passes make the final tie-break arXiv ID ascending while higher-priority fields descend.
    ranked.sort(key=lambda item: item["arxiv_id"])
    ranked.sort(key=lambda item: _date_key(item.get("published")), reverse=True)
    ranked.sort(key=lambda item: item["priority_score"], reverse=True)
    ranked.sort(key=lambda item: item["forced_entry"], reverse=True)
    return ranked


def write_queue(path: Path, ranked: list[dict[str, Any]], limit: int) -> dict[str, Any]:
    if limit < 1:
        raise PriorityBuildError("limit must be >= 1")
    chosen = ranked[:limit]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(
            json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"
            for row in chosen
        ),
        encoding="utf-8",
        newline="\n",
    )
    return {
        "schema": "sf-stage1b-abstract-priority-v1",
        "eligible_candidates": len(ranked),
        "queue_rows_written": len(chosen),
        "forced_rows_written": sum(1 for row in chosen if row["forced_entry"]),
        "screening_decisions_made": 0,
        "queue_semantics": "ORDER_FOR_MANUAL_ABSTRACT_REVIEW_NOT_A_SCREENING_DECISION",
    }


def _ids_from_notes(paths: list[Path]) -> set[str]:
    found: set[str] = set()
    for path in paths:
        found.update(ARXIV_ID.findall(path.read_text("utf-8")))
    return found


def _parse_forced(values: list[str]) -> dict[str, str]:
    result = {}
    for value in values:
        arxiv_id, separator, reason = value.partition("=")
        if not separator or not ARXIV_ID.fullmatch(arxiv_id) or not reason.strip():
            raise PriorityBuildError("--force-id must be ARXIV_ID=nonempty reason")
        result[arxiv_id] = reason.strip()
    return result


def main() -> int:
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--input", type=Path, required=True)
    cli.add_argument("--output", type=Path, required=True)
    cli.add_argument("--summary", type=Path)
    cli.add_argument("--limit", type=int, default=100)
    cli.add_argument("--exclude-id", action="append", default=[])
    cli.add_argument("--exclude-notes", type=Path, action="append", default=[])
    cli.add_argument("--force-id", action="append", default=[])
    args = cli.parse_args()

    excluded = set(args.exclude_id) | _ids_from_notes(args.exclude_notes)
    ranked = rank_candidates(load_candidates(args.input), excluded, _parse_forced(args.force_id))
    summary = write_queue(args.output, ranked, args.limit)
    summary.update(
        {
            "input": args.input.as_posix(),
            "output": args.output.as_posix(),
            "excluded_ids": len(excluded),
        }
    )
    if args.summary:
        args.summary.parent.mkdir(parents=True, exist_ok=True)
        args.summary.write_text(
            json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
            newline="\n",
        )
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
