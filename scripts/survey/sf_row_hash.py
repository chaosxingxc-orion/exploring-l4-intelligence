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


def _without_self_hash(value):
    """Remove only nested absence-row self hashes before canonical hashing.

    An absence record carries the hash of its owner row. Including that scalar in
    the row hash would create an impossible fixed-point requirement. Every other
    evidence and adjudication-reference field remains hash-bearing.
    """
    if isinstance(value, dict):
        return {
            key: _without_self_hash(item)
            for key, item in value.items()
            if key != "owner_row_sha256"
        }
    if isinstance(value, list):
        return [_without_self_hash(item) for item in value]
    return value


def row_hash(method_path):
    """Return the canonical SHA-256 for a method-path adjudication row."""
    core = _without_self_hash({
        key: value
        for key, value in method_path.items()
        if key not in ADJ_EXCLUDE
    })
    blob = json.dumps(
        core,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()
