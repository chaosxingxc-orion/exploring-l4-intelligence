"""Side-effect-free strict UTF-8 JSON and JSONL loading helpers."""
from __future__ import annotations

import json
import math
from collections.abc import Mapping
from pathlib import Path


class JsonContractError(ValueError):
    """Raised when input bytes are not portable strict JSON."""


def _unique_object(pairs):
    value = {}
    for key, child in pairs:
        if key in value:
            raise JsonContractError(f"duplicate key {key!r}")
        value[key] = child
    return value


def _reject_constant(value):
    raise JsonContractError(f"non-finite JSON constant {value}")


def _validate_portable(value):
    if isinstance(value, float) and not math.isfinite(value):
        raise JsonContractError("non-finite JSON number decoded from numeric token")
    if isinstance(value, str) and any(
        0xD800 <= ord(character) <= 0xDFFF for character in value
    ):
        raise JsonContractError("unpaired surrogate code point in JSON string")
    if isinstance(value, Mapping):
        for key, child in value.items():
            _validate_portable(key)
            _validate_portable(child)
    elif isinstance(value, list):
        for child in value:
            _validate_portable(child)


def loads(raw_bytes, source="JSON input"):
    """Decode and parse one complete strict UTF-8 JSON byte sequence."""
    if not isinstance(raw_bytes, bytes):
        raise JsonContractError(f"{source}: raw bytes are required")
    try:
        text = raw_bytes.decode("utf-8")
        value = json.loads(
            text,
            object_pairs_hook=_unique_object,
            parse_constant=_reject_constant,
        )
        _validate_portable(value)
        return value
    except (UnicodeDecodeError, json.JSONDecodeError, JsonContractError) as error:
        if isinstance(error, JsonContractError) and str(error).startswith(
            f"{source}:"
        ):
            raise
        raise JsonContractError(f"{source}: {error}") from error


def read(path):
    """Read a path once and parse the exact bytes returned to the caller."""
    path = Path(path)
    try:
        raw_bytes = path.read_bytes()
    except OSError as error:
        raise JsonContractError(f"{path}: cannot read: {error}") from error
    return loads(raw_bytes, str(path)), raw_bytes


def loads_jsonl(raw_bytes, source="JSONL input"):
    """Parse each nonblank UTF-8 JSONL line under the same strict contract."""
    if not isinstance(raw_bytes, bytes):
        raise JsonContractError(f"{source}: raw bytes are required")
    try:
        text = raw_bytes.decode("utf-8")
    except UnicodeDecodeError as error:
        raise JsonContractError(f"{source}: {error}") from error
    rows = []
    for line_number, line in enumerate(text.splitlines(), 1):
        if not line.strip():
            continue
        rows.append(loads(line.encode("utf-8"), f"{source}:line {line_number}"))
    return rows


def read_jsonl(path):
    path = Path(path)
    try:
        raw_bytes = path.read_bytes()
    except OSError as error:
        raise JsonContractError(f"{path}: cannot read: {error}") from error
    return loads_jsonl(raw_bytes, str(path)), raw_bytes


def canonical_bytes(value):
    """Return portable canonical JSON bytes for hashes and equality proofs."""
    try:
        return json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8")
    except (TypeError, ValueError, UnicodeEncodeError) as error:
        raise JsonContractError(f"canonical JSON encoding failed: {error}") from error
