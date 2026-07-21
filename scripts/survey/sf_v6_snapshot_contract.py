"""Side-effect-free current-input snapshot contract for evidence v6."""
from __future__ import annotations

import hashlib
from pathlib import Path

from sf_json_contract import canonical_bytes, read as read_strict_json
from sf_schema_v3_release_contract import (
    ADJUDICATION_RELATIVE_PATH,
    SIDECAR_DIRECTORY_RELATIVE_PATH,
    load_active_release,
    resolve_trusted_repo_path,
    validate_coding_lineage,
)
from sf_taxonomy_v6_contract import FROZEN_TAXONOMY_V5_SHA256


TAXONOMY_V5_RELATIVE_PATH = (
    "wiki/survey/2026-07-19-sf-identity-taxonomy-v5.json"
)
TAXONOMY_V6_RELATIVE_PATH = (
    "wiki/survey/current/data/identity-taxonomy-v6.json"
)
CODING_V7_RELATIVE_PATH = (
    "wiki/survey/current/data/known-item-coding-v7.json"
)
CURRENT_INPUT_SNAPSHOT_SHA256 = (
    "7db14cdd7c842bd284d8bb3015627da8e6cb7e296a78fecc19f90425861751e0"
)


def _repo_path(repo_root, relative):
    return Path(repo_root).joinpath(*relative.split("/"))


def read_snapshot_json(repo_root, path, expected_relative):
    """Strict-load exact bytes from one prescribed non-symlink repo path."""
    resolved = resolve_trusted_repo_path(
        repo_root,
        path,
        expected_relative=expected_relative,
        expected_kind="file",
    )
    return read_strict_json(resolved)


def _provenance_entry(relative_path, raw_bytes):
    return {
        "path": relative_path,
        "sha256": hashlib.sha256(raw_bytes).hexdigest(),
    }


def load_v6_input_snapshot(
    repo_root, *, read_snapshot=None, expected_snapshot_sha256=None
):
    """Load and bind the complete current v6 input release from raw bytes.

    ``read_snapshot`` is an injection seam retained for the A9 adversarial
    tests.  Production callers omit it and use prescribed trusted paths.
    """
    repo_root = Path(repo_root)
    if read_snapshot is None:
        read_snapshot = lambda path, relative: read_snapshot_json(
            repo_root, path, relative
        )

    taxonomy_v5_path = _repo_path(repo_root, TAXONOMY_V5_RELATIVE_PATH)
    taxonomy_v6_path = _repo_path(repo_root, TAXONOMY_V6_RELATIVE_PATH)
    coding_path = _repo_path(repo_root, CODING_V7_RELATIVE_PATH)
    sidecar_dir = _repo_path(repo_root, SIDECAR_DIRECTORY_RELATIVE_PATH)
    adjudication_path = _repo_path(repo_root, ADJUDICATION_RELATIVE_PATH)

    taxonomy_v5, taxonomy_v5_raw = read_snapshot(
        taxonomy_v5_path, TAXONOMY_V5_RELATIVE_PATH
    )
    taxonomy_v5_sha256 = hashlib.sha256(taxonomy_v5_raw).hexdigest()
    if taxonomy_v5_sha256 != FROZEN_TAXONOMY_V5_SHA256:
        raise ValueError(
            "frozen taxonomy-v5 SHA-256 mismatch "
            f"(expected={FROZEN_TAXONOMY_V5_SHA256}, "
            f"found={taxonomy_v5_sha256})"
        )
    taxonomy_v6, taxonomy_v6_raw = read_snapshot(
        taxonomy_v6_path, TAXONOMY_V6_RELATIVE_PATH
    )
    coding, coding_raw = read_snapshot(coding_path, CODING_V7_RELATIVE_PATH)
    try:
        coding_text = coding_raw.decode("utf-8")
    except UnicodeDecodeError as error:  # Defensive; strict loader checked it.
        raise ValueError(f"{coding_path}: {error}") from error

    release = load_active_release(repo_root, sidecar_dir, adjudication_path)
    validate_coding_lineage(coding, repo_root)
    rows = coding.get("rows") if isinstance(coding, dict) else None
    if not isinstance(rows, list):
        raise ValueError("active coding rows container invalid")
    sidecars = [(name, document) for name, document, _ in release.sidecars]
    provenance = {
        "taxonomy_v5": _provenance_entry(
            TAXONOMY_V5_RELATIVE_PATH, taxonomy_v5_raw
        ),
        "taxonomy": _provenance_entry(
            TAXONOMY_V6_RELATIVE_PATH, taxonomy_v6_raw
        ),
        "coding": _provenance_entry(CODING_V7_RELATIVE_PATH, coding_raw),
        "adjudication": _provenance_entry(
            ADJUDICATION_RELATIVE_PATH, release.adjudication_raw
        ),
        "sidecars": [
            _provenance_entry(
                f"{SIDECAR_DIRECTORY_RELATIVE_PATH}/{name}", raw
            )
            for name, _, raw in release.sidecars
        ],
    }
    input_snapshot_sha256 = hashlib.sha256(
        canonical_bytes(provenance)
    ).hexdigest()
    if (
        expected_snapshot_sha256 is not None
        and input_snapshot_sha256 != expected_snapshot_sha256
    ):
        raise ValueError(
            "current input snapshot SHA-256 mismatch "
            f"(expected={expected_snapshot_sha256}, "
            f"found={input_snapshot_sha256})"
        )
    return {
        "taxonomy_v5": taxonomy_v5,
        "taxonomy_v6": taxonomy_v6,
        "coding": coding,
        "coding_text": coding_text,
        "rows": rows,
        "sidecars": sidecars,
        "adjudication": release.adjudication,
        "input_provenance": provenance,
        "input_snapshot_sha256": input_snapshot_sha256,
    }
