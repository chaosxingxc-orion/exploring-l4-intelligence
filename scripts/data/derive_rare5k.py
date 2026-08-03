#!/usr/bin/env python3
"""Derive an auditable Rare5k-style vocabulary from local LibriSpeech train-960h.

The public paper description says the 5,000 most frequent words are common and the rest are rare.
It does not publish a canonical tokenizer or the claimed 209.2k-word artifact. This script therefore
creates a transparent local reconstruction and records any cardinality mismatch instead of claiming
paper-exact identity.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import unicodedata
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import pyarrow.parquet as pq


TOKEN_RE = re.compile(r"[A-Z]+(?:'[A-Z]+)?")
TRAIN_SPLITS = ("train.clean.100", "train.clean.360", "train.other.500")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normalize(text: str) -> list[str]:
    return TOKEN_RE.findall(unicodedata.normalize("NFKC", text).upper())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--librispeech", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--common-size", type=int, default=5000)
    args = parser.parse_args()

    parquet_files = [
        path
        for split in TRAIN_SPLITS
        for path in sorted((args.librispeech / "all" / split).glob("*.parquet"))
    ]
    if not parquet_files:
        raise SystemExit("no train-960h parquet files found under <librispeech>/all")

    counts: Counter[str] = Counter()
    utterances = 0
    tokens = 0
    for path in parquet_files:
        table = pq.read_table(path, columns=["text"])
        for text in table.column("text").to_pylist():
            words = normalize(text or "")
            counts.update(words)
            utterances += 1
            tokens += len(words)

    ordered = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    common = ordered[: args.common_size]
    rare = ordered[args.common_size :]

    args.output.mkdir(parents=True, exist_ok=True)
    common_path = args.output / "common-top5000.tsv"
    rare_path = args.output / "rare-after-top5000.tsv"
    manifest_path = args.output / "manifest.json"

    common_path.write_text("word\tcount\n" + "".join(f"{w}\t{n}\n" for w, n in common), encoding="utf-8")
    rare_path.write_text("word\tcount\n" + "".join(f"{w}\t{n}\n" for w, n in rare), encoding="utf-8")

    manifest = {
        "schema": "speechrl-derived-rare5k-v1",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source": {
            "dataset": "librispeech",
            "layout": "ModelScope openslr/librispeech_asr parquet",
            "splits": list(TRAIN_SPLITS),
            "parquet_files": len(parquet_files),
        },
        "normalization": {
            "unicode": "NFKC",
            "case": "uppercase",
            "token_regex": TOKEN_RE.pattern,
            "tie_break": "descending count, then ascending Unicode lexical order",
        },
        "counts": {
            "utterances": utterances,
            "tokens": tokens,
            "unique_words": len(ordered),
            "common_words": len(common),
            "rare_words": len(rare),
            "paper_reported_rare_words_approx": 209200,
        },
        "paper_exact": False,
        "claim_limit": (
            "Transparent reconstruction from the local train-960h transcripts. The paper did not "
            "release its tokenizer or 209.2k-word list; a count mismatch is evidence of an unresolved "
            "protocol dependency, not a license to synthesize missing entries."
        ),
        "outputs": {},
    }
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    manifest["outputs"] = {
        common_path.name: {"sha256": sha256(common_path), "bytes": common_path.stat().st_size},
        rare_path.name: {"sha256": sha256(rare_path), "bytes": rare_path.stat().st_size},
    }
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
