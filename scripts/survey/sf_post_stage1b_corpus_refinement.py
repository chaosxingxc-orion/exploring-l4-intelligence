#!/usr/bin/env python3
"""Exhaustively refine every locally downloaded survey PDF after Stage-1B.

The tool inventories every source artifact, treats each unique arXiv PDF as one paper, extracts
page-marked text outside Git, joins the metadata-only registry when available, and emits conservative
execution-screening signals. Automatic dispositions are prefilters, not novelty or final inclusion
verdicts; ambiguous and failed items remain visible in explicit review queues.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import logging
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Iterable

import sf_stage1b_bounded_sampling as sampling

logging.getLogger("pypdf").setLevel(logging.ERROR)


ARXIV_ID = re.compile(r"^(?P<id>\d{4}\.\d{4,5})(?:v\d+)?$", re.IGNORECASE)
MAX_EVIDENCE_PER_TYPE = 4

BLACK_BOX_CUES = (
    "training-free",
    "training free",
    "tuning-free",
    "tuning free",
    "without fine-tuning",
    "without finetuning",
    "without training",
    "no training",
    "frozen",
    "black-box",
    "black box",
    "api-only",
    "api only",
    "off-the-shelf",
)
INTERNAL_ACCESS_CUES = (
    "hidden state",
    "hidden states",
    "attention weights",
    "attention maps",
    "attention scores",
    "intermediate activations",
    "internal activations",
    "layer-wise entropy",
    "layerwise entropy",
    "logit lens",
    "logits",
    "log probabilities",
    "log-probabilities",
    "logprobs",
    "model weights",
)
SIGNAL_CUES = (
    "reward",
    "verifier",
    "verification",
    "feedback",
    "confidence",
    "uncertainty",
    "critique",
    "judge",
    "score",
    "scoring",
    "consensus",
)
ACTION_CUES = (
    "select",
    "selection",
    "choose",
    "rank",
    "rerank",
    "search",
    "revise",
    "revision",
    "refine",
    "route",
    "routing",
    "tool use",
    "tool-use",
    "stop",
    "stopping",
    "continue",
    "planning",
    "candidate generation",
    "prune",
    "memory",
)
INSTRUMENT_CUES = (
    "benchmark",
    "evaluation framework",
    "evaluation protocol",
    "metric",
    "test set",
    "test split",
    "leaderboard",
)
SPEECH_OMNI_CUES = (
    "speech",
    "audio",
    "voice",
    "spoken",
    "automatic speech recognition",
    "asr",
    "speech translation",
    "tts",
    "omni-modal",
    "omnimodal",
    "omni model",
    "multimodal",
)
SPEECH_PRIMARY_CUES = (
    "speech",
    "audio",
    "voice",
    "spoken",
    "automatic speech recognition",
    "asr",
    "speech translation",
    "tts",
)

LOAD_BEARING_TRAINING_PATTERNS = (
    r"\bwe\s+(?:fine[- ]?tune|train|optimi[sz]e)\b",
    r"\bour\s+(?:method|model|system|framework|adapter|module|encoder|decoder|controller(?: agent)?|verifier|policy|reward model)\s+(?:is\s+|are\s+)?(?:fine[- ]?tuned|fine[- ]?tunes|trains|trained|uses? lora)\b",
    r"\b(?:our|the proposed)\s+(?:training|fine[- ]?tuning|optimization)\s+(?:procedure|objective|stage|pipeline)\b",
    r"\bwe\s+(?:use|apply|perform)\s+(?:supervised\s+)?fine[- ]?tuning\b",
    r"\bwe\s+(?:use|apply|compute)\s+(?:the\s+)?gradient(?:s)?\b",
    r"\bupdate(?:s|d|ing)?\s+(?:the\s+)?(?:model\s+|backbone\s+)?weights\b",
    r"\bwe\s+(?:add|insert|train|learn|optimi[sz]e)\b.{0,100}\blearnable\s+(?:adapter|prompt|projection|layer|module)\b",
)
ARCHITECTURE_PATTERNS = (
    r"\b(?:we|our method|our model|our system|the proposed method|the proposed model)\b.{0,140}\b(?:add|adds|insert|inserts|introduce|introduces|use|uses)\b.{0,120}\b(?:adapter|q-former|projection layer|cross-attention|encoder layer|decoder layer|learnable (?:soft )?prompt)\b",
    r"\b(?:we|our method|our model|the proposed method|the proposed model)\b.{0,160}\b(?:modified model architecture|architecture modification)\b",
)
INTERNAL_ACCESS_PATTERNS = (
    r"\bwe\s+(?:compute|extract|use|access|inspect|aggregate|modify|manipulate|store|subtract|combine|inject|visuali[sz]e|examine)\b.{0,100}\b(?:decoder |encoder |model |transformer |backbone |llm |vlm )?(?:hidden states?|attention weights|attention maps|attention scores|intermediate activations|internal activations|layer[- ]wise entropy|logit lens|logits|log probabilities|log-probabilities|logprobs)\b",
    r"\b(?:our method|our system|the proposed method|the proposed system)\b.{0,180}\b(?:decoder|encoder|model|transformer|backbone|llm|vlm)(?:'s)?\s+(?:hidden states?|attention weights|attention maps|attention scores|intermediate activations|internal activations|layer[- ]wise entropy|logits|log probabilities|log-probabilities|logprobs)\b",
    r"\b(?:reward|signal|score|selector|policy)\b.{0,120}\b(?:from|uses?|based on|computed from)\b.{0,120}\b(?:decoder|encoder|model|transformer|backbone|llm|vlm)(?:'s)?\s+(?:hidden states?|attention weights|attention maps|attention scores|intermediate activations|internal activations|layer[- ]wise entropy|logits|log probabilities|log-probabilities|logprobs)\b",
    r"\brequires?\s+(?:direct\s+)?access\s+to\s+(?:the\s+)?(?:model(?:'s)?\s+)?(?:hidden states?|attention|activations|logits|weights)\b",
    r"\b(?:decoder|encoder)[- ](?:only\s+)?attention\s+(?:policy|intervention|editing|routing)\b",
    r"\b(?:self|cross)-attention\b.{0,100}\b(?:signal|score|policy)\b",
)
INSTRUMENT_PATTERNS = (
    r"\bwe\s+(?:introduce|present|release|develop)\s+(?:a|an|the|our|new)?\s*(?:[A-Za-z0-9_-]+,?\s+)?(?:benchmark|metric|evaluation framework|evaluation protocol|test suite|dataset)\b",
    r"\bwe\s+release\s+(?:a|an|the|our|new)?\s*(?:benchmark|metric|dataset|test suite)\b",
)
RESTRICTED_DATA_PATTERNS = (
    r"\bprivate\s+(?:clinical|patient|hospital|educational|student)\b.{0,30}\b(?:dataset|data|records?|transcripts?)\b",
    r"\b(?:data|dataset|records?)\s+(?:is|are|was|were)\s+not publicly available\b",
    r"\b(?:cannot|can not|could not)\s+be\s+(?:released|shared|made public)\b",
    r"\bconfidential\s+(?:dataset|data|records?)\b",
    r"\brestricted[- ]access\s+(?:dataset|data|records?)\b",
    r"\bprivate\s+servers?\s+behind\s+an?\s+institutional\s+firewall\b",
)
PUBLIC_DATA_PATTERNS = (
    r"\bpublicly available\b.{0,40}\b(?:datasets?|data|benchmarks?)\b",
    r"\bopen[- ]source\b.{0,40}\b(?:datasets?|data|benchmarks?)\b",
    r"\bwe (?:release|released|will release)\s+(?:the\s+)?(?:dataset|data|benchmark)\b",
)
VERTICAL_DOMAINS = {
    "medical": (
        "clinical", "patient", "diagnosis", "medical", "healthcare", "biomedical",
        "radiology", "pathology", "electronic health record", "ehr",
    ),
    "education": (
        "education", "educational", "student", "tutoring", "tutor", "classroom",
        "learning analytics",
    ),
    "3d_spatial": (
        "3d", "point cloud", "nerf", "neural radiance field", "spatial reasoning",
        "3d scene", "3d object",
    ),
    "world_or_embodied": (
        "world model", "world data", "embodied", "robot", "robotic", "navigation",
        "autonomous driving", "driving dataset", "simulation environment",
    ),
    "legal": ("legal", "law", "court", "judicial", "contract review"),
    "finance": ("financial", "finance", "trading", "stock market", "credit risk"),
    "science_engineering": (
        "chemistry", "molecule", "materials science", "scientific discovery", "engineering design",
    ),
}


@dataclass(frozen=True)
class SourceArtifact:
    path: Path
    relative_path: str
    size_bytes: int
    extension: str
    artifact_kind: str
    arxiv_id: str | None


@dataclass
class PaperArtifact:
    arxiv_id: str
    pdf_path: Path
    pdf_relative_path: str
    eprint_relative_path: str | None = None
    related_artifact_paths: list[str] = field(default_factory=list)


def _canonical_arxiv_id(stem: str) -> str | None:
    match = ARXIV_ID.fullmatch(stem)
    return match.group("id") if match else None


def _artifact_kind(path: Path) -> str:
    extension = path.suffix.lower()
    if extension == ".pdf":
        return "PAPER_PDF"
    if extension == ".eprint":
        return "PAPER_SOURCE_EPRINT"
    if extension == ".txt":
        return "EXTRACTED_OR_AUXILIARY_TEXT"
    if extension in {".json", ".jsonl"}:
        return "METADATA_OR_LEDGER"
    if extension in {".png", ".jpg", ".jpeg"}:
        return "IMAGE_OR_RENDER"
    return "CONTROL_OR_LOG"


def discover_artifacts(root: Path) -> tuple[list[SourceArtifact], dict[str, PaperArtifact]]:
    if not root.is_dir():
        raise FileNotFoundError(f"full-text root not found: {root}")
    artifacts: list[SourceArtifact] = []
    papers: dict[str, PaperArtifact] = {}
    related: dict[str, list[str]] = defaultdict(list)
    eprints: dict[str, list[str]] = defaultdict(list)
    for path in sorted((item for item in root.rglob("*") if item.is_file()), key=lambda item: item.as_posix()):
        relative = path.relative_to(root).as_posix()
        aid = _canonical_arxiv_id(path.stem)
        kind = _artifact_kind(path)
        artifact = SourceArtifact(
            path=path,
            relative_path=relative,
            size_bytes=path.stat().st_size,
            extension=path.suffix.lower(),
            artifact_kind=kind,
            arxiv_id=aid,
        )
        artifacts.append(artifact)
        if aid:
            related[aid].append(relative)
        if kind == "PAPER_SOURCE_EPRINT" and aid:
            eprints[aid].append(relative)
        if kind != "PAPER_PDF":
            continue
        if not aid:
            raise ValueError(f"PDF filename does not carry a canonical arXiv ID: {relative}")
        if aid in papers:
            raise ValueError(
                f"duplicate PDF identity {aid}: {papers[aid].pdf_relative_path} and {relative}"
            )
        papers[aid] = PaperArtifact(aid, path, relative)
    for aid, paper in papers.items():
        candidates = sorted(eprints.get(aid, []), key=lambda value: (value.count("/"), len(value), value))
        paper.eprint_relative_path = candidates[0] if candidates else None
        paper.related_artifact_paths = sorted(related.get(aid, []))
    return artifacts, papers


def _safe_utf8(text: str) -> str:
    return text.encode("utf-8", errors="replace").decode("utf-8")


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def _pages_before_references(pages: list[str]) -> list[str]:
    kept = []
    for page in pages:
        if re.search(r"(?:^|\n)\s*(?:references|bibliography)\s*(?:\n|$)", page, re.IGNORECASE):
            break
        kept.append(page)
    return kept or pages[:1]


def _phrase_hits(text: str, terms: Iterable[str]) -> list[str]:
    hits = set()
    for term in terms:
        escaped = re.escape(term).replace(r"\ ", r"\s+")
        prefix = r"(?<!\w)" if term[:1].isalnum() else ""
        suffix = r"(?!\w)" if term[-1:].isalnum() else ""
        if re.search(prefix + escaped + suffix, text, re.IGNORECASE):
            hits.add(term)
    return sorted(hits)


def _pattern_hits(text: str, patterns: Iterable[str]) -> list[str]:
    hits = []
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if match:
            hits.append(_normalize(match.group(0))[:180])
    return hits


def _control_relation_pages(pages: list[str]) -> list[int]:
    signal = r"(?:reward|verifier|verification|feedback|confidence|uncertainty|critique|judge|score|scoring|consensus)"
    action = r"(?:select|selection|choose|rank|rerank|search|revise|revision|refine|route|routing|tool use|tool-use|stop|stopping|continue|planning|candidate generation|prune|memory)"
    forward = re.compile(rf"\b{signal}\b.{{0,240}}\b{action}\b", re.I | re.S)
    reverse = re.compile(rf"\b{action}\b.{{0,240}}\b{signal}\b", re.I | re.S)
    return [
        page_number
        for page_number, page in enumerate(pages, start=1)
        if forward.search(_normalize(page)) or reverse.search(_normalize(page))
    ]


def _evidence(pages: list[str], terms: Iterable[str], evidence_type: str) -> list[dict[str, Any]]:
    result = []
    for page_number, page in enumerate(pages, start=1):
        normalized = _normalize(page)
        lowered = normalized.lower()
        for term in terms:
            position = lowered.find(term.lower())
            if position < 0:
                continue
            start = max(0, position - 100)
            end = min(len(normalized), position + len(term) + 140)
            result.append(
                {
                    "page": page_number,
                    "evidence_type": evidence_type,
                    "matched_term": term,
                    "snippet": normalized[start:end],
                }
            )
            if len(result) >= MAX_EVIDENCE_PER_TYPE:
                return result
    return result


def _infer_title(first_page: str, registry_record: dict[str, Any]) -> tuple[str, str]:
    registered = str(registry_record.get("title") or "").strip()
    if registered:
        return registered, "STAGE1B_REGISTRY"
    lines = [_normalize(line) for line in first_page.splitlines() if _normalize(line)]
    skip = re.compile(r"^(?:arxiv:|preprint|proceedings|accepted|submitted|https?://|www\.)", re.I)
    candidates = [line for line in lines[:30] if 5 <= len(line) <= 240 and not skip.search(line)]
    if not candidates:
        return "UNKNOWN_TITLE", "PDF_TEXT_UNRESOLVED"
    return candidates[0], "PDF_FIRST_PAGE_HEURISTIC"


def _registry_local_datasets(record: dict[str, Any]) -> list[dict[str, Any]]:
    return [dict(item) for item in (record.get("datasets") or []) if item.get("local_present")]


def analyze_pages(
    arxiv_id: str,
    pages: list[str],
    registry_record: dict[str, Any],
    dataset_catalog: Any,
) -> dict[str, Any]:
    analysis_pages = _pages_before_references(pages)
    text = "\n".join(analysis_pages)
    normalized = _normalize(text)
    first_page = pages[0] if pages else ""
    front_text = "\n".join(analysis_pages[:2])
    fulltext_black_box_hits = _phrase_hits(front_text, BLACK_BOX_CUES)
    registry_no_update = [
        str(item)
        for item in ((registry_record.get("method_path") or {}).get("no_update_evidence") or [])
        if str(item).strip()
    ]
    black_box_hits = sorted(set(fulltext_black_box_hits + registry_no_update))
    if fulltext_black_box_hits and registry_no_update:
        black_box_evidence_source = "FULLTEXT_OR_STAGE1B_REGISTRY"
    elif registry_no_update:
        black_box_evidence_source = "STAGE1B_REGISTRY"
    elif fulltext_black_box_hits:
        black_box_evidence_source = "FULLTEXT"
    else:
        black_box_evidence_source = "NONE"
    internal_hits = _pattern_hits(normalized, INTERNAL_ACCESS_PATTERNS)
    training_hits = _pattern_hits(normalized, LOAD_BEARING_TRAINING_PATTERNS)
    architecture_hits = _pattern_hits(normalized, ARCHITECTURE_PATTERNS)
    signal_hits = _phrase_hits(normalized, SIGNAL_CUES)
    action_hits = _phrase_hits(normalized, ACTION_CUES)
    instrument_hits = _phrase_hits(front_text, INSTRUMENT_CUES)
    speech_omni_hits = _phrase_hits(first_page, SPEECH_OMNI_CUES)
    speech_primary_hits = _phrase_hits(first_page, SPEECH_PRIMARY_CUES)
    restricted_hits = _pattern_hits(normalized, RESTRICTED_DATA_PATTERNS)
    public_hits = _pattern_hits(normalized, PUBLIC_DATA_PATTERNS)
    vertical_domains = sorted(
        domain for domain, terms in VERTICAL_DOMAINS.items() if _phrase_hits(first_page, terms)
    )
    catalog_matches = [dict(item) for item in dataset_catalog.match(text)]
    registry_local = _registry_local_datasets(registry_record)
    local_by_name = {
        str(item.get("canonical_name")): item
        for item in [*catalog_matches, *registry_local]
        if item.get("local_present")
    }
    local_matches = [local_by_name[key] for key in sorted(local_by_name)]
    registry_datasets = [dict(item) for item in (registry_record.get("datasets") or [])]

    control_pages = _control_relation_pages(analysis_pages)
    external_control_path = bool(control_pages)

    if training_hits or architecture_hits:
        model_operability = "MODEL_OR_COMPONENT_OPERABLE"
    elif internal_hits:
        model_operability = "INTERNAL_ACCESS_REQUIRED_OR_AMBIGUOUS"
    elif black_box_hits:
        model_operability = "BLACK_BOX_COMPATIBLE"
    else:
        model_operability = "UNKNOWN"

    if local_matches:
        data_feasibility = "LOCAL_MATCH"
    elif vertical_domains and restricted_hits:
        data_feasibility = "RESTRICTED_VERTICAL_DATA"
    elif public_hits:
        data_feasibility = "PUBLIC_OR_RELEASED_NOT_LOCAL"
    elif registry_datasets:
        data_feasibility = "NAMED_DATA_NOT_LOCAL"
    else:
        data_feasibility = "NO_MATCHING_LOCAL_DATA_EVIDENCE"

    registered_role = str(registry_record.get("role") or "UNREGISTERED_LOCAL_FULLTEXT")
    title, title_source = _infer_title(first_page, registry_record)
    instrument_pattern_hits = _pattern_hits(front_text, INSTRUMENT_PATTERNS)
    instrument_title_term = bool(
        re.search(r"\b(?:benchmark(?:ing)?|evaluation framework|evaluation protocol|metric|dataset)\b", title, re.I)
    )
    instrument_title = instrument_title_term and (
        title_source == "STAGE1B_REGISTRY"
        or (len(title) < 160 and not title.lower().startswith(("we ", "our ")))
    )
    instrument = registered_role == "KEEP_INSTRUMENT" or bool(instrument_pattern_hits) or instrument_title
    speech_or_omni = bool(registry_record.get("speech_primary_object")) or bool(speech_omni_hits)
    speech_primary = bool(registry_record.get("speech_primary_object")) or bool(speech_primary_hits)
    reason_codes = []
    if training_hits:
        reason_codes.append("LOAD_BEARING_TRAINING")
    if architecture_hits:
        reason_codes.append("ARCHITECTURE_MODIFICATION")
    if internal_hits:
        reason_codes.append("MODEL_INTERNAL_ACCESS")
    if black_box_hits:
        reason_codes.append("BLACK_BOX_OR_FROZEN_EVIDENCE")
    if external_control_path:
        reason_codes.append("REWARD_OR_EVALUATION_CONTROL_PATH")
    if local_matches:
        reason_codes.append("LOCAL_DATA_MATCH")
    if vertical_domains:
        reason_codes.append("VERTICAL_DOMAIN")
    if restricted_hits:
        reason_codes.append("RESTRICTED_DATA_EVIDENCE")
    if instrument:
        reason_codes.append("MEASUREMENT_INSTRUMENT_SIGNAL")

    if model_operability == "MODEL_OR_COMPONENT_OPERABLE":
        disposition = "EXCLUDE_MODEL_OPERABLE"
    elif model_operability == "INTERNAL_ACCESS_REQUIRED_OR_AMBIGUOUS":
        disposition = "EXCLUDE_MODEL_INTERNAL_ACCESS"
    elif data_feasibility == "RESTRICTED_VERTICAL_DATA":
        disposition = "EXCLUDE_VERTICAL_DATA_BARRIER"
    elif registered_role == "KEEP_NEGATIVE":
        disposition = "BOUNDARY_OR_NEGATIVE_ONLY"
    elif instrument:
        disposition = "INSTRUMENT_ONLY"
    elif external_control_path and model_operability == "BLACK_BOX_COMPATIBLE" and local_matches and speech_primary:
        disposition = "PRIORITY_DIRECT"
    elif external_control_path and model_operability == "BLACK_BOX_COMPATIBLE":
        disposition = "TRANSFER_ONLY"
    elif external_control_path:
        disposition = "MANUAL_REVIEW_ACCESS_AMBIGUOUS"
    else:
        disposition = "LOW_PRIORITY_NO_CONTROL_PATH"

    locators = []
    for terms, label in (
        (training_hits, "LOAD_BEARING_TRAINING"),
        (architecture_hits, "ARCHITECTURE_MODIFICATION"),
        (internal_hits, "MODEL_INTERNAL_ACCESS"),
        (black_box_hits, "BLACK_BOX_OR_FROZEN"),
        (restricted_hits, "RESTRICTED_DATA"),
        (signal_hits, "CONTROL_SIGNAL"),
        (action_hits, "CONTROL_ACTION"),
    ):
        locators.extend(_evidence(analysis_pages, terms, label))

    return {
        "schema": "sf-post-stage1b-corpus-refinement-v1",
        "arxiv_id": arxiv_id,
        "title": title,
        "title_source": title_source,
        "registry_match": bool(registry_record),
        "stage1b_role": registered_role,
        "speech_or_omni_signal": speech_or_omni,
        "speech_primary_signal": speech_primary,
        "vertical_domains": vertical_domains,
        "model_operability": model_operability,
        "data_feasibility": data_feasibility,
        "external_control_path": external_control_path,
        "control_path_pages": control_pages,
        "execution_disposition": disposition,
        "reason_codes": reason_codes,
        "black_box_terms": black_box_hits,
        "black_box_evidence_source": black_box_evidence_source,
        "training_evidence": training_hits,
        "architecture_evidence": architecture_hits,
        "internal_access_terms": internal_hits,
        "control_signal_terms": signal_hits,
        "control_action_terms": action_hits,
        "instrument_terms": instrument_hits,
        "instrument_evidence": instrument_pattern_hits,
        "speech_omni_terms": speech_omni_hits,
        "restricted_data_evidence": restricted_hits,
        "public_data_evidence": public_hits,
        "local_dataset_matches": local_matches,
        "registry_datasets": registry_datasets,
        "analysis_pages_before_references": len(analysis_pages),
        "evidence_locators": locators,
        "decision_origin": "DETERMINISTIC_SECONDARY_PREFILTER_REQUIRES_HUMAN_AUDIT",
    }


def _hash_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _extract_pdf(path: Path) -> list[str]:
    from pypdf import PdfReader

    return [_safe_utf8(page.extract_text() or "") for page in PdfReader(path).pages]


def _load_registry(paths: list[Path]) -> dict[str, dict[str, Any]]:
    records: dict[str, dict[str, Any]] = {}
    for path in paths:
        for line in path.read_text("utf-8").splitlines():
            if not line.strip():
                continue
            record = json.loads(line)
            aid = str(record.get("arxiv_id") or "")
            if not aid:
                raise ValueError(f"registry row lacks arxiv_id: {path}")
            if aid in records:
                raise ValueError(f"duplicate registry identity across inputs: {aid}")
            records[aid] = record
    return records


def _write_jsonl(path: Path, rows: Iterable[dict[str, Any]]) -> tuple[int, str]:
    payload = "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows)
    path.write_text(payload, encoding="utf-8", newline="\n")
    return len(payload.encode("utf-8")), hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _write_queue_report(path: Path, rows: list[dict[str, Any]], summary: dict[str, Any]) -> None:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[str(row["execution_disposition"])].append(row)
    lines = [
        "# Post-Stage-1B local full-text refinement queues",
        "",
        "> Deterministic prefilter only. Exclusion means excluded from the execution shortlist, not deleted from the evidence portfolio.",
        "",
        f"Coverage: {summary['processed_paper_rows']}/{summary['discovered_unique_pdfs']} unique PDFs; "
        f"source artifacts: {summary['source_artifacts']}; extraction failures: {summary['extraction_failed_pdfs']}.",
        "",
    ]
    for disposition in sorted(grouped):
        items = sorted(grouped[disposition], key=lambda row: str(row["arxiv_id"]))
        lines.extend((f"## {disposition} ({len(items)})", "", "| arXiv ID | Title | Stage-1B role | Reasons |", "|---|---|---|---|"))
        for row in items:
            title = str(row.get("title") or "UNKNOWN_TITLE").replace("|", "\\|")
            reasons = ", ".join(row.get("reason_codes") or [])
            lines.append(f"| {row['arxiv_id']} | {title} | {row.get('stage1b_role')} | {reasons} |")
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8", newline="\n")


def run(
    pdf_root: Path,
    output_dir: Path,
    registry_paths: list[Path],
    dataset_catalog: Any,
    *,
    extract_pdf: Callable[[Path], list[str]] = _extract_pdf,
) -> dict[str, Any]:
    if output_dir.exists():
        raise FileExistsError(f"refusing to overwrite corpus-refinement output: {output_dir}")
    artifacts, papers = discover_artifacts(pdf_root)
    registry = _load_registry(registry_paths)
    output_dir.mkdir(parents=True)
    text_dir = output_dir / "extracted-text"
    text_dir.mkdir()

    artifact_rows = []
    artifact_hashes = {}
    for artifact in artifacts:
        sha256 = _hash_file(artifact.path)
        artifact_hashes[artifact.relative_path] = sha256
        artifact_rows.append(
            {
                "schema": "sf-local-fulltext-source-artifact-v1",
                "relative_path": artifact.relative_path,
                "size_bytes": artifact.size_bytes,
                "sha256": sha256,
                "extension": artifact.extension,
                "artifact_kind": artifact.artifact_kind,
                "arxiv_id": artifact.arxiv_id,
            }
        )
    artifact_bytes, artifact_ledger_sha = _write_jsonl(output_dir / "source-artifacts.jsonl", artifact_rows)

    rows = []
    extracted_count = 0
    extraction_failed = 0
    low_text_count = 0
    for aid in sorted(papers):
        paper = papers[aid]
        record = registry.get(aid, {})
        base = {
            "schema": "sf-post-stage1b-corpus-refinement-v1",
            "arxiv_id": aid,
            "pdf_relative_path": paper.pdf_relative_path,
            "eprint_relative_path": paper.eprint_relative_path,
            "related_source_artifacts": paper.related_artifact_paths,
            "pdf_bytes": paper.pdf_path.stat().st_size,
            "pdf_sha256": artifact_hashes[paper.pdf_relative_path],
            "registry_match": bool(record),
            "stage1b_role": record.get("role", "UNREGISTERED_LOCAL_FULLTEXT"),
        }
        try:
            pages = extract_pdf(paper.pdf_path)
            extracted = _safe_utf8(
                "\n\n".join(f"=== PAGE {index} ===\n{text}" for index, text in enumerate(pages, 1))
            )
            text_path = text_dir / f"{aid}.txt"
            text_path.write_text(extracted, encoding="utf-8", newline="\n")
            row = analyze_pages(aid, pages, record, dataset_catalog)
            extracted_bytes = extracted.encode("utf-8")
            row.update(
                {
                    **base,
                    "fulltext_status": "PDF_EXTRACTED",
                    "fulltext_pages": len(pages),
                    "extracted_text_relative_path": text_path.relative_to(output_dir).as_posix(),
                    "extracted_text_bytes": len(extracted_bytes),
                    "extracted_text_sha256": hashlib.sha256(extracted_bytes).hexdigest(),
                }
            )
            extracted_count += 1
            if len(_normalize(extracted)) < 500:
                row["fulltext_status"] = "PDF_EXTRACTED_LOW_TEXT"
                row["execution_disposition"] = "MANUAL_REVIEW_LOW_TEXT"
                row["reason_codes"] = ["EXTRACTED_TEXT_BELOW_500_CHARS"]
                low_text_count += 1
            rows.append(row)
        except Exception as exc:  # retain the identity and fail closed
            extraction_failed += 1
            rows.append(
                {
                    **base,
                    "title": record.get("title", "UNKNOWN_TITLE"),
                    "title_source": "STAGE1B_REGISTRY" if record.get("title") else "UNRESOLVED_EXTRACTION_FAILED",
                    "fulltext_status": "EXTRACTION_FAILED",
                    "extraction_error": f"{type(exc).__name__}: {exc}",
                    "model_operability": "UNKNOWN",
                    "data_feasibility": "UNKNOWN",
                    "vertical_domains": [],
                    "external_control_path": False,
                    "execution_disposition": "MANUAL_REVIEW_EXTRACTION_FAILED",
                    "reason_codes": ["PDF_EXTRACTION_FAILED"],
                    "evidence_locators": [],
                    "decision_origin": "EXTRACTION_STATE_FAIL_CLOSED",
                }
            )

    paper_bytes, paper_ledger_sha = _write_jsonl(output_dir / "paper-analysis.jsonl", rows)
    paper_ids = {str(row["arxiv_id"]) for row in rows}
    coverage_complete = len(rows) == len(papers) and paper_ids == set(papers)
    dispositions = dict(sorted(Counter(str(row["execution_disposition"]) for row in rows).items()))
    operability = dict(sorted(Counter(str(row.get("model_operability")) for row in rows).items()))
    feasibility = dict(sorted(Counter(str(row.get("data_feasibility")) for row in rows).items()))
    domain_counts = Counter(domain for row in rows for domain in (row.get("vertical_domains") or []))
    extension_counts = dict(sorted(Counter(artifact.extension or "[no_extension]" for artifact in artifacts).items()))
    source_kind_counts = dict(sorted(Counter(artifact.artifact_kind for artifact in artifacts).items()))
    registry_matched = sum(bool(row.get("registry_match")) for row in rows)
    summary = {
        "schema": "sf-post-stage1b-corpus-refinement-summary-v1",
        "source_root": pdf_root.as_posix(),
        "source_artifacts": len(artifacts),
        "source_bytes": sum(artifact.size_bytes for artifact in artifacts),
        "source_extension_counts": extension_counts,
        "source_artifact_kind_counts": source_kind_counts,
        "source_artifact_ledger_bytes": artifact_bytes,
        "source_artifact_ledger_sha256": artifact_ledger_sha,
        "discovered_unique_pdfs": len(papers),
        "processed_paper_rows": len(rows),
        "extracted_pdfs": extracted_count,
        "extraction_failed_pdfs": extraction_failed,
        "low_text_pdfs": low_text_count,
        "registry_input_records": len(registry),
        "registry_matched_pdfs": registry_matched,
        "registry_unmatched_pdfs": len(rows) - registry_matched,
        "pdfs_with_eprint": sum(bool(paper.eprint_relative_path) for paper in papers.values()),
        "coverage_complete": coverage_complete,
        "execution_disposition_counts": dispositions,
        "model_operability_counts": operability,
        "data_feasibility_counts": feasibility,
        "vertical_domain_counts": dict(sorted(domain_counts.items())),
        "paper_analysis_ledger_bytes": paper_bytes,
        "paper_analysis_ledger_sha256": paper_ledger_sha,
        "decision_scope": "EXECUTION_SHORTLIST_PREFILTER_ONLY_REQUIRES_HUMAN_AUDIT",
    }
    if not coverage_complete:
        raise RuntimeError("coverage invariant failed: discovered PDF IDs do not equal output paper IDs")
    (output_dir / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    _write_queue_report(output_dir / "screening-queues.md", rows, summary)
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pdf-root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--registry", type=Path, action="append", default=[])
    parser.add_argument("--dataset-lock", type=Path, required=True)
    parser.add_argument("--data-root", type=Path, required=True)
    args = parser.parse_args()
    catalog = sampling.DatasetCatalog.from_lock(args.dataset_lock, args.data_root)
    summary = run(args.pdf_root, args.output_dir, args.registry, catalog)
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
