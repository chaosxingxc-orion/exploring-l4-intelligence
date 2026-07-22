#!/usr/bin/env python3
"""Build deterministic bounded Stage-1B abstract-analysis rounds.

The sampler is a cost-bounded research aid. It never downloads a paper and never rewrites the frozen
D0 source. Every sampled abstract receives transparent speech-task, local-dataset, control-path, and
reproducibility features plus an explicit abstract disposition. Only SELECT_FULLTEXT rows authorize a
later downloader. Non-speech rows need both a transferable control path and abstract-level open-source
evidence before direct full-text authorization.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


ARXIV_ID = re.compile(r"(?<!\d)(\d{4}\.\d{4,5})(?:v\d+)?(?!\d)")
URL = re.compile(r"https?://[^\s<>\])}]+", re.IGNORECASE)

SPEECH_TERMS = (
    "speech", "audio", "spoken", "voice", "acoustic", "auditory", "speaker",
    "paralinguistic", "automatic speech recognition", "speech recognition", "asr",
    "text-to-speech", "speech synthesis", "speech translation", "voice agent",
)
ACOUSTIC_PRIMARY_TERMS = tuple(term for term in SPEECH_TERMS if term != "speech") + (
    "speech enhancement", "speech separation", "speech processing", "speech language model",
    "speech model", "speech-to-speech", "speech to speech", "speech signal", "speech quality",
    "speech coding", "speech compression", "speech generation",
    "speech source separation", "speech understanding", "speech language model",
    "speech-language model", "speechllm", "speechllms", "audio language model",
    "audio-language model", "brain-to-speech", "brain to speech", "decoding speech",
    "transcribing speech",
)
NON_ACOUSTIC_SPEECH_TERMS = (
    "hate speech", "counter speech", "counter-speech", "free speech", "political speech",
    "speech act", "hateful speech",
)
NON_SPEECH_DATASET_TASKS = {"text-reasoning-eval"}
SIGNAL_TERMS = (
    "reward", "verifier", "verification", "feedback", "critic", "judge", "confidence",
    "uncertainty", "self-evaluation", "self evaluation", "self-reflection", "self reflection",
    "consensus", "value model", "value function", "biometric", "speaker encoder", "similarity",
    "score", "scoring",
)
DECISION_TERMS = (
    "search", "select", "selection", "prune", "resampl", "routing", "route", "allocate",
    "decoding", "steering", "revise", "revision", "refine", "regenerate", "re-observe",
    "reobserve", "tool use", "tool-use", "tool calling", "planning", "memory", "stop",
    "stopping", "abstain", "fallback", "best-of-n", "best of n", "majority voting", "mcts",
)
NO_UPDATE_TERMS = (
    "training-free", "training free", "tuning-free", "tuning free", "frozen", "test-time",
    "test time", "inference-time", "inference time", "without training", "without fine-tuning",
    "without finetuning", "off-the-shelf", "zero-shot",
)
TRANSFER_TERMS = (
    "multimodal", "multi-modal", "omni", "vision-language", "vision language", "vlm", "mllm",
    "agent", "robot", "embodied", "image generation", "video", "gui",
)
REPRO_CLAIMS = (
    "open-source", "open source", "code is available", "code available", "release our code",
    "code and data", "repository", "implementation is available",
)
ADVERSE_TERMS = (
    "failure", "fails", "limitation", "degrade", "no improvement", "unreliable", "plateau",
    "reward hacking", "overthinking", "bias", "oracle", "upper bound", "negative result",
)

TASK_TERMS = {
    "asr": ("automatic speech recognition", "speech recognition", "transcription", "word error rate", "asr"),
    "st": ("speech translation", "spoken language translation", "speech-to-text translation"),
    "ser": ("speech emotion", "emotion recognition", "emotion classification", "ser"),
    "speaker": ("speaker identification", "speaker recognition", "speaker verification", "diarization"),
    "tts": ("text-to-speech", "speech synthesis", "voice cloning"),
    "slu_intent": ("spoken language understanding", "speech intent", "intent classification", "slot filling", "slu"),
    "spoken_qa_reasoning": ("spoken question", "audio question answering", "audio reasoning", "audio understanding"),
    "spoken_agent_dialogue": ("voice agent", "speech agent", "spoken dialogue", "full-duplex", "voice assistant"),
    "audio_generation": ("text-to-audio", "video-to-audio", "audio generation", "sound generation"),
}

MANUAL_ALIASES = {
    "librispeech": ("libri speech",),
    "covost2": ("covost 2", "covost-2"),
    "fleurs-r": ("fleurs r", "fleurs"),
    "crema-d": ("crema d",),
    "speech-massive": ("speech massive",),
    "mmau-mini": ("mmau",),
    "air-bench": ("air bench", "airbench"),
    "big-bench-audio": ("big bench audio", "bbaudio"),
    "heysquad": ("hey squad",),
    "spoken-squad": ("spoken squad",),
    "uro-bench": ("uro bench", "urobench"),
    "vocalbench-zh": ("vocalbench zh",),
    "voiceassistant-eval": ("voice assistant eval",),
    "soulx-duplug": ("soulx duplug",),
    "tau2-bench": ("tau2 bench", "tau 2 bench"),
    "seed-tts-eval": ("seed tts",),
}

AMBIGUOUS_ACRONYM_TERMS = {"asr", "ser", "tts"}
STRONG_SIGNAL_TERMS = frozenset(SIGNAL_TERMS) - {"score", "scoring", "similarity"}


class SamplingError(RuntimeError):
    """Fail-closed sampling or input error."""


def _norm(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


def _phrase_hits(text: str, terms: Iterable[str]) -> list[str]:
    normalized = _norm(text)
    hits = []
    for term in terms:
        needle = _norm(term)
        if re.search(rf"(?<![a-z0-9]){re.escape(needle)}(?![a-z0-9])", normalized):
            hits.append(term)
    return sorted(set(hits))


@dataclass(frozen=True)
class DatasetCatalog:
    entries: tuple[dict[str, Any], ...]
    aliases: tuple[tuple[str, str], ...]
    present_names: frozenset[str]

    @classmethod
    def from_rows(
        cls,
        rows: list[dict[str, Any]],
        present_names: set[str] | None = None,
    ) -> "DatasetCatalog":
        present = frozenset(present_names or set())
        entries = tuple(sorted((dict(row) for row in rows), key=lambda row: row["name"]))
        alias_pairs: set[tuple[str, str]] = set()
        for row in entries:
            name = str(row["name"])
            candidates = {name, name.replace("-", " ")}
            source = row.get("source") or {}
            source_id = source.get("id") or source.get("hf_id")
            if source_id:
                candidates.add(str(source_id).split("/")[-1])
            candidates.update(MANUAL_ALIASES.get(name, ()))
            for alias in candidates:
                normalized = _norm(alias)
                if len(normalized) >= 4:
                    alias_pairs.add((normalized, name))
        return cls(entries, tuple(sorted(alias_pairs)), present)

    @classmethod
    def from_lock(cls, lock_path: Path, data_root: Path) -> "DatasetCatalog":
        payload = json.loads(lock_path.read_text("utf-8"))
        rows = payload.get("datasets")
        if not isinstance(rows, list) or not rows:
            raise SamplingError("dataset lock has no datasets")
        present = {
            str(row["name"])
            for row in rows
            if (data_root / Path(str(row["local_subdir"]))).is_dir()
        }
        return cls.from_rows(rows, present)

    def match(self, text: str) -> list[dict[str, Any]]:
        normalized = _norm(text)
        matched_names = {
            name
            for alias, name in self.aliases
            if re.search(rf"(?<![a-z0-9]){re.escape(alias)}(?![a-z0-9])", normalized)
        }
        by_name = {str(row["name"]): row for row in self.entries}
        return [
            {
                "canonical_name": name,
                "task": by_name[name].get("task"),
                "factor_family": by_name[name].get("factor_family"),
                "lock_status": by_name[name].get("status"),
                "local_present": name in self.present_names,
                "local_subdir": by_name[name].get("local_subdir"),
            }
            for name in sorted(matched_names)
        ]


def analyze_abstract(row: dict[str, Any], datasets: DatasetCatalog) -> dict[str, Any]:
    title = str(row.get("title", ""))
    abstract = str(row.get("abstract", ""))
    text = f"{title} {abstract}"
    speech_hits = _phrase_hits(text, SPEECH_TERMS)
    acoustic_primary_hits = _phrase_hits(text, ACOUSTIC_PRIMARY_TERMS)
    signal_hits = _phrase_hits(text, SIGNAL_TERMS)
    decision_hits = _phrase_hits(text, DECISION_TERMS)
    no_update_hits = _phrase_hits(text, NO_UPDATE_TERMS)
    transfer_hits = _phrase_hits(text, TRANSFER_TERMS)
    adverse_hits = _phrase_hits(text, ADVERSE_TERMS)
    repro_hits = _phrase_hits(text, REPRO_CLAIMS)
    urls = sorted(set(URL.findall(text)))
    repo_urls = [url for url in urls if any(host in url.lower() for host in ("github.com", "gitlab.com", "huggingface.co"))]
    dataset_mentions = datasets.match(text)
    speech_dataset_mentions = [
        item for item in dataset_mentions if str(item.get("task") or "").lower() not in NON_SPEECH_DATASET_TASKS
    ]
    speech_related = bool(speech_hits)
    task_tags = [name for name, terms in TASK_TERMS.items() if _phrase_hits(text, terms)]
    title_speech_hits = [
        term for term in _phrase_hits(title, ACOUSTIC_PRIMARY_TERMS)
        if term not in AMBIGUOUS_ACRONYM_TERMS
    ]
    contribution_sentences = [
        sentence
        for sentence in re.split(r"(?<=[.!?])\s+", abstract)
        if re.search(
            r"\b(?:we|our|this (?:paper|work|study|report)|the proposed)\b.*"
            r"\b(?:propose|present|introduce|develop|study|investigate|address|show|demonstrate|evaluate|method|framework|approach)",
            sentence,
            re.IGNORECASE,
        )
    ]
    contribution_speech_hits = [
        term for term in _phrase_hits(" ".join(contribution_sentences), ACOUSTIC_PRIMARY_TERMS)
        if term not in AMBIGUOUS_ACRONYM_TERMS
    ]
    speech_primary_reasons = []
    if title_speech_hits:
        speech_primary_reasons.append("SPEECH_IN_TITLE")
    if contribution_speech_hits:
        speech_primary_reasons.append("SPEECH_IN_CONTRIBUTION_STATEMENT")
    if speech_dataset_mentions and acoustic_primary_hits:
        speech_primary_reasons.append("NAMED_SPEECH_DATASET")
    speech_primary_object = bool(speech_primary_reasons)
    non_acoustic_speech_sense = bool(_phrase_hits(text, NON_ACOUSTIC_SPEECH_TERMS)) and not speech_primary_object

    if repo_urls:
        repro_status = "EXPLICIT_REPO_URL"
    elif repro_hits:
        repro_status = "EXPLICIT_OPEN_SOURCE_CLAIM"
    elif urls:
        repro_status = "PROJECT_PAGE_OR_URL"
    else:
        repro_status = "NO_ABSTRACT_EVIDENCE"

    if speech_primary_object and speech_dataset_mentions:
        local_status = (
            "LOCAL_MATCH"
            if any(item["local_present"] for item in speech_dataset_mentions)
            else "LOCK_MATCH_NOT_PRESENT"
        )
    elif speech_primary_object:
        local_status = "NOT_STATED_IN_ABSTRACT"
    else:
        local_status = "NOT_APPLICABLE_NON_SPEECH"

    strong_signal = bool(set(signal_hits) & STRONG_SIGNAL_TERMS)
    control_path = bool(signal_hits and decision_hits)
    frozen_path = bool(no_update_hits and decision_hits)
    transferable = bool(transfer_hits and (control_path or frozen_path))
    reason_codes: list[str] = []

    if speech_primary_object:
        reason_codes.append("PRIMARY_SPEECH_OR_AUDIO_TASK")
        if local_status == "LOCAL_MATCH":
            reason_codes.append("LOCAL_DATASET_MATCH")
        if control_path or (frozen_path and signal_hits) or (decision_hits and speech_dataset_mentions):
            disposition = "SELECT_FULLTEXT"
            reason_codes.append("SPEECH_CONTROL_PATH")
        elif signal_hits or decision_hits or no_update_hits:
            disposition = "DEFER_ABSTRACT"
            reason_codes.append("SPEECH_RELEVANCE_CONTROL_PATH_AMBIGUOUS")
        else:
            disposition = "EXCLUDE_ABSTRACT"
            reason_codes.append("SPEECH_WITHOUT_TARGET_CONTROL_PATH")
    else:
        if speech_related:
            reason_codes.append("NON_ACOUSTIC_SPEECH_SENSE" if non_acoustic_speech_sense else "INCIDENTAL_SPEECH_MENTION")
        if (
            transferable
            and repro_status in {"EXPLICIT_REPO_URL", "EXPLICIT_OPEN_SOURCE_CLAIM"}
            and strong_signal
            and (no_update_hits or adverse_hits)
        ):
            disposition = "SELECT_FULLTEXT"
            reason_codes.extend(("NON_SPEECH_TRANSFER_PATH", "ABSTRACT_REPRODUCIBILITY_EVIDENCE"))
        elif transferable or (adverse_hits and decision_hits):
            disposition = "DEFER_REPRO_CHECK"
            reason_codes.append("TRANSFER_PATH_REPRODUCIBILITY_UNRESOLVED")
        else:
            disposition = "EXCLUDE_ABSTRACT"
            reason_codes.append("NO_SPEECH_OR_REPRODUCIBLE_TRANSFER_PATH")

    relevance_score = (
        12 * speech_primary_object
        + 2 * bool(speech_hits)
        + 6 * bool(signal_hits)
        + 6 * bool(decision_hits)
        + 5 * bool(no_update_hits)
        + 4 * bool(transfer_hits)
        + 4 * bool(speech_dataset_mentions)
        + 4 * (repro_status != "NO_ABSTRACT_EVIDENCE")
        + 3 * bool(adverse_hits)
        + min(3, len(set(row.get("source_query_ids") or [])))
    )

    kept = {
        key: row.get(key)
        for key in (
            "arxiv_id", "title", "abstract", "authors", "published", "updated", "categories",
            "primary_category", "source_query_ids", "query_recall_credit",
        )
        if key in row
    }
    kept.update(
        {
            "abstract_policy_version": "sf-stage1b-abstract-policy-v6",
            "speech_related": speech_related,
            "speech_primary_object": speech_primary_object,
            "speech_primary_reasons": speech_primary_reasons,
            "non_acoustic_speech_sense": non_acoustic_speech_sense,
            "speech_task_tags": sorted(task_tags),
            "speech_evidence_terms": speech_hits,
            "acoustic_primary_terms": acoustic_primary_hits,
            "dataset_mentions": dataset_mentions,
            "speech_dataset_mentions": speech_dataset_mentions,
            "dataset_local_status": local_status,
            "control_signal_terms": signal_hits,
            "decision_action_terms": decision_hits,
            "frozen_or_test_time_terms": no_update_hits,
            "transfer_object_terms": transfer_hits,
            "adverse_terms": adverse_hits,
            "reproducibility_terms": repro_hits,
            "abstract_urls": urls,
            "repo_urls": repo_urls,
            "reproducibility_abstract_status": repro_status,
            "abstract_relevance_score": relevance_score,
            "abstract_disposition": disposition,
            "abstract_reason_codes": reason_codes,
            "fulltext_authorized": disposition == "SELECT_FULLTEXT",
            "decision_origin": "DETERMINISTIC_POLICY_SCREEN_REQUIRES_AUDIT",
        }
    )
    return kept


def _tie(seed: str, lane: str, arxiv_id: str) -> str:
    return hashlib.sha256(f"{seed}|{lane}|{arxiv_id}".encode()).hexdigest()


def id_set_sha256(ids: Iterable[str]) -> str:
    """Hash a canonical, newline-delimited ID set for replay provenance."""
    payload = "".join(f"{value}\n" for value in sorted(set(ids))).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _rank(rows: list[dict[str, Any]], seed: str, lane: str) -> list[dict[str, Any]]:
    return sorted(
        rows,
        key=lambda row: (
            -int(row["abstract_relevance_score"]),
            _tie(seed, lane, str(row["arxiv_id"])),
            str(row["arxiv_id"]),
        ),
    )


def _take(
    preferred: list[dict[str, Any]],
    fallback: list[dict[str, Any]],
    used: set[str],
    count: int,
) -> list[dict[str, Any]]:
    chosen: list[dict[str, Any]] = []
    for source in (preferred, fallback):
        for row in source:
            aid = str(row["arxiv_id"])
            if aid in used:
                continue
            chosen.append(row)
            used.add(aid)
            if len(chosen) == count:
                return chosen
    raise SamplingError(f"cannot fill {count} unique rows for a sampling round")


def build_rounds(
    candidates: list[dict[str, Any]],
    datasets: DatasetCatalog,
    handled_ids: set[str],
    round_size: int = 1000,
    round_count: int = 3,
    exhaust_remaining: bool = False,
    seed: str = "stage1b-bounded-three-rounds-v1",
) -> list[list[dict[str, Any]]]:
    if round_size < 1:
        raise SamplingError("round_size must be positive")
    if round_count < 1:
        raise SamplingError("round_count must be positive")
    seen: set[str] = set()
    analyzed = []
    for row in sorted(candidates, key=lambda item: str(item.get("arxiv_id", ""))):
        aid = str(row.get("arxiv_id", ""))
        if not ARXIV_ID.fullmatch(aid):
            raise SamplingError(f"invalid arXiv ID: {aid!r}")
        if aid in seen:
            raise SamplingError(f"duplicate arXiv ID: {aid}")
        seen.add(aid)
        if aid not in handled_ids:
            analyzed.append(analyze_abstract(row, datasets))
    if exhaust_remaining:
        full_rounds, tail_size = divmod(len(analyzed), round_size)
        round_sizes = [round_size] * full_rounds
        if tail_size:
            round_sizes.append(tail_size)
        if not round_sizes:
            raise SamplingError("no unique unhandled rows remain to exhaust")
    else:
        round_sizes = [round_size] * round_count
    if len(analyzed) < sum(round_sizes):
        raise SamplingError(
            f"cannot fill {round_count} rounds of {round_size}: "
            f"only {len(analyzed)} unique unhandled rows"
        )

    used = set(handled_ids)
    all_ranked = _rank(analyzed, seed, "all")
    speech = _rank([row for row in analyzed if row["speech_primary_object"]], seed, "speech")
    transfer = _rank(
        [
            row for row in analyzed
            if not row["speech_primary_object"]
            and row["reproducibility_abstract_status"] != "NO_ABSTRACT_EVIDENCE"
            and row["control_signal_terms"]
            and row["decision_action_terms"]
        ],
        seed,
        "transfer",
    )
    selected_rounds: list[tuple[str, list[dict[str, Any]]]] = []
    lane_cycle = ("SPEECH_TASK_AND_DATASET", "TRANSFER_REPRODUCIBLE", "TAIL_CALIBRATION")
    for round_offset, target_size in enumerate(round_sizes):
        lane = lane_cycle[round_offset % len(lane_cycle)]
        if lane == "SPEECH_TASK_AND_DATASET":
            selected = _take(speech, all_ranked, used, target_size)
        elif lane == "TRANSFER_REPRODUCIBLE":
            selected = _take(transfer, all_ranked, used, target_size)
        else:
            remaining = [row for row in analyzed if str(row["arxiv_id"]) not in used]
            # Each calibration round interleaves score bands, then hashes within each band.
            bands: dict[int, list[dict[str, Any]]] = {}
            for row in remaining:
                bands.setdefault(int(row["abstract_relevance_score"]) // 10, []).append(row)
            for band, rows in bands.items():
                bands[band] = sorted(rows, key=lambda row: _tie(seed, f"tail-{band}", row["arxiv_id"]))
            tail: list[dict[str, Any]] = []
            active = sorted(bands, reverse=True)
            while active:
                next_active = []
                for band in active:
                    if bands[band]:
                        tail.append(bands[band].pop(0))
                    if bands[band]:
                        next_active.append(band)
                active = next_active
            selected = _take(tail, all_ranked, used, target_size)
        selected_rounds.append((lane, selected))

    result = []
    for round_index, (lane, rows) in enumerate(selected_rounds, start=1):
        batch = []
        for rank, row in enumerate(rows, start=1):
            enriched = dict(row)
            enriched.update(
                {
                    "sampling_schema": "sf-stage1b-bounded-sample-v6",
                    "sample_round": round_index,
                    "sampling_lane": lane,
                    "sample_rank": rank,
                    "sample_key_sha256": _tie(seed, lane, str(row["arxiv_id"])),
                }
            )
            batch.append(enriched)
        result.append(batch)
    return result


def write_rounds(
    output_dir: Path,
    rounds: list[list[dict[str, Any]]],
    source_sha256: str,
    dataset_lock_sha256: str,
    *,
    sampling_seed: str,
    handled_ids: set[str],
    eligible_unhandled_count: int | None = None,
) -> dict[str, Any]:
    if not rounds:
        raise SamplingError("at least one round is required")
    output_dir.mkdir(parents=True, exist_ok=True)
    paths = []
    all_ids = []
    disposition_counts = []
    for index, rows in enumerate(rounds, start=1):
        path = output_dir / f"round-{index}-abstract-sample.jsonl"
        payload = "".join(
            json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"
            for row in rows
        )
        path.write_text(payload, encoding="utf-8", newline="\n")
        paths.append(
            {
                "round": index,
                "path": path.as_posix(),
                "bytes": len(payload.encode("utf-8")),
                "sha256": hashlib.sha256(payload.encode("utf-8")).hexdigest(),
            }
        )
        all_ids.extend(str(row["arxiv_id"]) for row in rows)
        disposition_counts.append(
            {
                decision: sum(row["abstract_disposition"] == decision for row in rows)
                for decision in ("SELECT_FULLTEXT", "DEFER_ABSTRACT", "DEFER_REPRO_CHECK", "EXCLUDE_ABSTRACT")
            }
        )
    if len(all_ids) != len(set(all_ids)):
        raise SamplingError("round outputs overlap")
    handled_payload = "".join(f"{value}\n" for value in sorted(handled_ids))
    handled_path = output_dir / "handled-ids.txt"
    handled_path.write_text(handled_payload, encoding="utf-8", newline="\n")
    round_sizes = [len(rows) for rows in rounds]
    legacy_three_round_shape = (
        len(rounds) == 3
        and len(set(round_sizes)) == 1
        and eligible_unhandled_count is None
    )
    summary = {
        "schema": (
            "sf-stage1b-bounded-sampling-summary-v6"
            if legacy_three_round_shape
            else "sf-stage1b-bounded-sampling-summary-v7"
        ),
        "source_sha256": source_sha256,
        "dataset_lock_sha256": dataset_lock_sha256,
        "sampling_seed": sampling_seed,
        "handled_ids_count": len(handled_ids),
        "handled_ids_sha256": id_set_sha256(handled_ids),
        "handled_ids_artifact": {
            "path": handled_path.as_posix(),
            "bytes": len(handled_payload.encode("utf-8")),
            "sha256": hashlib.sha256(handled_payload.encode("utf-8")).hexdigest(),
        },
        "round_sizes": round_sizes,
        "sampled_unique": len(all_ids),
        "disposition_counts": disposition_counts,
        "round_artifacts": paths,
        "downloads_in_this_step": 0,
    }
    if not legacy_three_round_shape:
        summary["round_count"] = len(rounds)
    if eligible_unhandled_count is not None:
        remaining = eligible_unhandled_count - len(all_ids)
        if remaining < 0:
            raise SamplingError("sampled more rows than the eligible unhandled population")
        summary.update(
            {
                "eligible_unhandled_before_sampling": eligible_unhandled_count,
                "remaining_unhandled_after_sampling": remaining,
                "corpus_exhausted_within_frozen_source": remaining == 0,
            }
        )
    summary_path = output_dir / (
        "three-round-sampling-summary.json" if legacy_three_round_shape else "bounded-sampling-summary.json"
    )
    summary_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return summary


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    for line_no, line in enumerate(path.read_text("utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise SamplingError(f"{path}: line {line_no}: invalid JSON: {exc}") from exc
    return rows


def _handled_ids(paths: list[Path], explicit: list[str]) -> set[str]:
    result = set(explicit)
    for path in paths:
        if path.suffix.lower() == ".jsonl":
            for line_no, row in enumerate(_read_jsonl(path), start=1):
                value = str(row.get("arxiv_id", ""))
                if not ARXIV_ID.fullmatch(value):
                    raise SamplingError(f"{path}: line {line_no}: missing or invalid arxiv_id")
                result.add(value)
        else:
            result.update(ARXIV_ID.findall(path.read_text("utf-8")))
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--dataset-lock", type=Path, required=True)
    parser.add_argument("--data-root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--handled-notes", type=Path, action="append", default=[])
    parser.add_argument("--handled-id", action="append", default=[])
    parser.add_argument("--round-size", type=int, default=1000)
    parser.add_argument("--round-count", type=int, default=3)
    parser.add_argument(
        "--exhaust-remaining",
        action="store_true",
        help="sample every eligible unhandled row, emitting a final partial round when needed",
    )
    parser.add_argument("--seed", default="stage1b-bounded-three-rounds-v1")
    args = parser.parse_args()

    input_bytes = args.input.read_bytes()
    lock_bytes = args.dataset_lock.read_bytes()
    catalog = DatasetCatalog.from_lock(args.dataset_lock, args.data_root)
    handled_ids = _handled_ids(args.handled_notes, args.handled_id)
    candidates = _read_jsonl(args.input)
    rounds = build_rounds(
        candidates,
        catalog,
        handled_ids,
        round_size=args.round_size,
        round_count=args.round_count,
        exhaust_remaining=args.exhaust_remaining,
        seed=args.seed,
    )
    summary = write_rounds(
        args.output_dir,
        rounds,
        hashlib.sha256(input_bytes).hexdigest(),
        hashlib.sha256(lock_bytes).hexdigest(),
        sampling_seed=args.seed,
        handled_ids=handled_ids,
        eligible_unhandled_count=(
            sum(str(row.get("arxiv_id", "")) not in handled_ids for row in candidates)
            if args.exhaust_remaining
            else None
        ),
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
