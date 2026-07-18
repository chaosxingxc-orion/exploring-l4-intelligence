#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Single-write coding generator (v7 doctoral review Gate MAJOR-2, contract A).

Projects the canonical per-paper sidecars (wiki/survey/sidecars/*.sidecar.json)
into the flat coding table wiki/survey/2026-07-19-sf-known-item-coding-v5.json.

The sidecars are the ONLY hand-authored source; the coding file is a GENERATED
projection — hand edits to it are a reconciliation failure (taxonomy v4
single_write_pipeline). Output is deterministically ordered (sidecars by
paper_work_id, rows by method_path_id) and byte-stable: repeated runs produce
zero diff. No derived fields are emitted — derivation happens only in the
contract test (sf_identity_taxonomy_v4_test.py).

Usage (from repo root):
  python scripts/survey/sf_coding_generator.py            # write coding v5
  python scripts/survey/sf_coding_generator.py --check    # verify zero diff, no write
"""
import glob
import io
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SIDECAR_DIR = os.path.join(REPO, "wiki", "survey", "sidecars")
OUT = os.path.join(REPO, "wiki", "survey", "2026-07-19-sf-known-item-coding-v5.json")

ROW_KEY_ORDER = [
    "method_path_id", "paper_work_id", "component_path_ids", "core_topology",
    "core_native_modality", "internal_visibility", "core_io_modality",
    "core_weight_update", "external_component_weight_update",
    "controller_program_or_config_optimized_on_labels", "human_or_dev_label_model_selection",
    "deployment_label_access", "test_item_gold_access", "inference_external_new_information",
    "signal_form", "signal_source", "signal_lifecycle", "signal_use", "control_horizon",
    "decision_rights", "control_edges", "selection_object", "terminal_operator",
    "explicit_candidate_pool_selection", "candidate_pool_exists", "selection_policy",
    "includes_speech_audio", "adjudication_required", "load_bearing", "field_evidence",
    "fulltext_ref", "canonical_record_id", "source_locator", "coder",
    "semantic_adjudicator", "adjudication_status", "adjudication_provenance", "note",
]


def load_sidecars():
    paths = sorted(glob.glob(os.path.join(SIDECAR_DIR, "*.sidecar.json")))
    if not paths:
        raise SystemExit(f"no sidecars under {SIDECAR_DIR}")
    return [(os.path.basename(p), json.load(io.open(p, encoding="utf-8"))) for p in paths]


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


def render(sidecars):
    rows = project(sidecars)
    doc = {
        "artifact_id": "SF-KNOWN-ITEM-CODING-V5-2026-07-19-01",
        "title": "known-item coding v5 — GENERATED single-write projection of per-paper sidecars (taxonomy v4; v7 doctoral review Gate MAJOR-1/-2 remediation)",
        "taxonomy": "wiki/survey/2026-07-19-sf-identity-taxonomy-v4.json",
        "generated_by": "scripts/survey/sf_coding_generator.py — DO NOT HAND-EDIT; edit the sidecar and regenerate",
        "generated_from": [name for name, _ in sorted(sidecars, key=lambda t: t[1]["paper_work_id"])],
        "supersession": "v5 supersedes coding-v4 (dated supersession; v4 retained for audit). Deltas: control_edges + field_evidence + candidate_pool_exists/selection_policy per taxonomy v4; Selective TTS decision_rights ['stop']->['branch'] (edge-evidence dated correction, see sidecar); actor ids replace W1; all rows load_bearing with independent adjudication status.",
        "rows": rows,
    }
    return json.dumps(doc, ensure_ascii=False, indent=1) + "\n"


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    text = render(load_sidecars())
    if "--check" in sys.argv:
        current = io.open(OUT, encoding="utf-8").read() if os.path.exists(OUT) else None
        if current != text:
            print("[FAIL] coding v5 is NOT byte-identical to generator output (hand edit or stale)")
            return 1
        print("[OK] coding v5 byte-identical to generator output")
        return 0
    io.open(OUT, "w", encoding="utf-8", newline="\n").write(text)
    print(f"wrote {os.path.relpath(OUT, REPO)} ({text.count(chr(10))} lines)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
