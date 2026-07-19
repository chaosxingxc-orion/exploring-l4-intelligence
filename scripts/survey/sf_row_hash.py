"""Side-effect-free canonical method-path adjudication hash."""

from __future__ import annotations

import hashlib
import json


ADJ_EXCLUDE = {
    "semantic_adjudicator",
    "adjudication_status",
    "adjudication_row_sha256",
    "adjudication_provenance",
}


def row_hash(method_path):
    """Return the canonical SHA-256 for a method-path adjudication row."""
    core = {
        key: value
        for key, value in method_path.items()
        if key not in ADJ_EXCLUDE
    }
    blob = json.dumps(
        core,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()
