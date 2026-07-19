#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Deterministic single-write coding generator for legacy and active profiles.

Projects canonical per-paper sidecars into a flat coding table.  The public
``render(sidecars)`` call remains the byte-stable legacy-v6 projection; the
command-line interface defaults to the active schema-v3/v7 projection.

The sidecars are the ONLY hand-authored source; the coding file is a GENERATED
projection — hand edits to it are a reconciliation failure (taxonomy v4
single_write_pipeline). Output is deterministically ordered (sidecars by
paper_work_id, rows by method_path_id) and byte-stable: repeated runs produce
zero diff. No derived fields are emitted — derivation happens only in the
contract test (sf_identity_taxonomy_v4_test.py).

Usage (from repo root):
  python scripts/survey/sf_coding_generator.py            # write active coding v7
  python scripts/survey/sf_coding_generator.py --check    # verify zero diff, no write
"""
import argparse
import glob
import io
import json
import os
import sys
import tempfile

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LEGACY_SIDECAR_DIR = os.path.join(REPO, "wiki", "survey", "sidecars")
LEGACY_OUT = os.path.join(
    REPO, "wiki", "survey", "2026-07-19-sf-known-item-coding-v6.json"
)
LEGACY_TAXONOMY = "wiki/survey/2026-07-19-sf-identity-taxonomy-v5.json"
ACTIVE_SIDECAR_DIR = os.path.join(
    REPO, "wiki", "survey", "current", "data", "schema-v3", "sidecars"
)
ACTIVE_OUT = os.path.join(
    REPO, "wiki", "survey", "current", "data", "known-item-coding-v7.json"
)
ACTIVE_TAXONOMY = "wiki/survey/current/data/identity-taxonomy-v6.json"

# Compatibility names for consumers that imported the old module constants.
SIDECAR_DIR = LEGACY_SIDECAR_DIR
OUT = LEGACY_OUT

ROW_KEY_ORDER = [
    "method_path_id", "paper_work_id", "component_path_ids", "core_topology",
    "core_native_modality", "internal_visibility", "core_io_modality",
    "core_weight_update", "external_component_weight_update",
    "controller_program_or_config_optimized_on_labels", "human_or_dev_label_model_selection",
    "deployment_label_access", "test_item_gold_access", "inference_external_new_information",
    "signals", "control_horizon", "decision_rights", "control_edges",
    "selection_object", "terminal_operator",
    "explicit_candidate_pool_selection", "candidate_pool_exists", "selection_policy",
    "includes_speech_audio", "adjudication_required", "load_bearing", "claim_evidence",
    "fulltext_ref", "canonical_record_id", "source_locator", "coder",
    "semantic_adjudicator", "adjudication_status", "adjudication_row_sha256",
    "adjudication_provenance", "note",
]


def load_sidecars(sidecar_dir=LEGACY_SIDECAR_DIR):
    paths = sorted(glob.glob(os.path.join(sidecar_dir, "*.sidecar.json")))
    if not paths:
        raise SystemExit(f"no sidecars under {sidecar_dir}")
    sidecars = []
    for path in paths:
        with io.open(path, encoding="utf-8") as handle:
            sidecars.append((os.path.basename(path), json.load(handle)))
    return sidecars


def project(sidecars):
    rows = []
    for _, sc in sorted(sidecars, key=lambda t: t[1]["paper_work_id"]):
        ft = sc["fulltext"]
        for mp in sc["method_paths"]:
            r = dict(mp)
            r["paper_work_id"] = sc["paper_work_id"]
            r["fulltext_ref"] = {"ledger": ft["ledger"], "id": ft["id"],
                                 "kind": ft["kind"], "sha256": ft["sha256"]}
            r["canonical_record_id"] = sc["canonical_record_id"]
            r.setdefault("coder", sc["coder"])
            ordered = {k: r[k] for k in ROW_KEY_ORDER if k in r}
            extras = {k: r[k] for k in sorted(r) if k not in ordered}
            ordered.update(extras)
            rows.append(ordered)
    rows.sort(key=lambda r: r["method_path_id"])
    ids = [r["method_path_id"] for r in rows]
    if len(ids) != len(set(ids)):
        raise SystemExit("duplicate method_path_id across sidecars")
    return rows


def render(sidecars, taxonomy=LEGACY_TAXONOMY, profile="v6"):
    rows = project(sidecars)
    if profile == "v6":
        artifact_id = "SF-KNOWN-ITEM-CODING-V6-2026-07-19-01"
        title = (
            "known-item coding v6 — GENERATED single-write projection of schema-v2 "
            "sidecars (taxonomy v5; v8 doctoral review Gate MAJOR-1/-2/-3 remediation)"
        )
        supersession = (
            "v6 supersedes coding-v5 (dated supersession; v5 retained in git for audit "
            "of the v4-era claims). Deltas per taxonomy v5: flat signal fields replaced "
            "by signals[] instances (AutoTTS state/consensus phase split; Selective TTS "
            "stage/final judge split); control_edges reference signal_id; claim_evidence "
            "covers every load-bearing field (positive/tex/absence kinds); "
            "adjudication_row_sha256 binds adjudication to row content."
        )
    elif profile == "v7":
        artifact_id = "SF-KNOWN-ITEM-CODING-V7-2026-07-19-01"
        title = "known-item coding v7 — GENERATED projection of schema-v3 sidecars"
        supersession = (
            "v7 supersedes coding-v6 as the active projection; coding-v6 remains the "
            "byte-stable legacy regression artifact. Schema-v3 adds adjudicated "
            "row16 + signal4 + edge2 field-bound evidence and strong PDF anchors "
            "without changing frozen derivation semantics."
        )
    else:
        raise ValueError(f"unsupported coding profile: {profile}")
    doc = {
        "artifact_id": artifact_id,
        "title": title,
        "taxonomy": taxonomy,
        "generated_by": "scripts/survey/sf_coding_generator.py — DO NOT HAND-EDIT; edit the sidecar and regenerate",
        "generated_from": [name for name, _ in sorted(sidecars, key=lambda t: t[1]["paper_work_id"])],
        "supersession": supersession,
        "rows": rows,
    }
    return json.dumps(doc, ensure_ascii=False, indent=1) + "\n"


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", choices=("v6", "v7"), default="v7")
    parser.add_argument("--sidecar-dir", default=ACTIVE_SIDECAR_DIR)
    parser.add_argument("--out", default=ACTIVE_OUT)
    parser.add_argument("--taxonomy", default=ACTIVE_TAXONOMY)
    parser.add_argument("--check", action="store_true")
    return parser.parse_args(argv)


def _repo_path(path):
    return path if os.path.isabs(path) else os.path.join(REPO, path)


def _display_path(path):
    try:
        return os.path.relpath(path, REPO)
    except ValueError:  # Different Windows drive.
        return path


def _write_all(handle, payload):
    view = memoryview(payload)
    offset = 0
    while offset < len(view):
        written = handle.write(view[offset:])
        if written is None or written <= 0:
            raise OSError("staging write made no progress")
        offset += written


def _publish_bytes(out, payload):
    """Atomically publish exact bytes without exposing a partial destination."""
    directory = os.path.dirname(out)
    os.makedirs(directory, exist_ok=True)
    descriptor, staging = tempfile.mkstemp(
        prefix=f".{os.path.basename(out)}.", suffix=".tmp", dir=directory
    )
    descriptor_owned = True
    try:
        handle = os.fdopen(descriptor, "wb")
        descriptor_owned = False
        with handle:
            _write_all(handle, payload)
            handle.flush()
            os.fsync(handle.fileno())
        with io.open(staging, "rb") as handle:
            staged = handle.read()
        if staged != payload:
            raise OSError("staging verification failed: bytes differ from projection")
        os.replace(staging, out)
        staging = None
    finally:
        if descriptor_owned:
            try:
                os.close(descriptor)
            except OSError:
                pass
        if staging is not None:
            try:
                os.unlink(staging)
            except FileNotFoundError:
                pass


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    args = parse_args(argv)
    sidecar_dir = _repo_path(args.sidecar_dir)
    out = _repo_path(args.out)
    text = render(
        load_sidecars(sidecar_dir),
        taxonomy=args.taxonomy,
        profile=args.profile,
    )
    payload = text.encode("utf-8")
    if args.check:
        if os.path.exists(out):
            with io.open(out, "rb") as handle:
                current = handle.read()
        else:
            current = None
        if current != payload:
            print("[FAIL] coding is NOT byte-identical to generator output (hand edit or stale)")
            return 1
        print("[OK] coding byte-identical to generator output")
        return 0
    _publish_bytes(out, payload)
    print(f"wrote {_display_path(out)} ({text.count(chr(10))} lines)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
