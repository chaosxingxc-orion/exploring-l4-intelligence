#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Active identity-taxonomy v6 integration, mutation, and occupancy harness.

Taxonomy v6 deliberately keeps taxonomy-v5 derivation semantics.  This module
therefore imports the frozen derivation, structural validator, fixtures, and
expectation runner from the v5 harness while replacing only the active evidence
contract seams: schema-v3 field bindings, discriminative PDF locators, active
artifact paths, and adjudicated schema-v3 sidecars.
"""
from __future__ import annotations

import copy
import gzip
import hashlib
import io
import json
import logging
import os
import re
import sys
import tarfile
import tempfile
from pathlib import Path


REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from sf_coding_generator import render  # noqa: E402
from sf_asset_path import resolve_asset_path  # noqa: E402
from sf_evidence_contract import (  # noqa: E402
    EDGE_REQUIRED_FIELDS,
    ROW_REQUIRED_FIELDS,
    SIGNAL_REQUIRED_FIELDS,
    check_page_locator,
    normalized_phrase,
    validate_bound_values,
    values_equal,
)
from sf_identity_taxonomy_v5_test import (  # noqa: E402
    adapt,
    base_row,
    check_quotes,
    derive,
    fx_edge,
    run_expectations,
    validate,
)
from sf_json_contract import (  # noqa: E402
    JsonContractError,
    canonical_bytes,
    read as read_strict_json,
    read_jsonl,
)
from sf_row_hash import row_hash  # noqa: E402
from sf_schema_v3_release_contract import (  # noqa: E402
    ADJUDICATION_RELATIVE_PATH,
    load_active_release,
    validate_canonical_record_id,
    validate_coding_lineage,
    validate_repo_relative_path,
)
from sf_taxonomy_v6_contract import (  # noqa: E402
    FROZEN_TAXONOMY_V5_SHA256,
    validate_taxonomy_v6,
)


logging.getLogger("pypdf").setLevel(logging.ERROR)


TAX = os.path.join(
    REPO, "wiki", "survey", "current", "data", "identity-taxonomy-v6.json"
)
TAX_V5 = os.path.join(
    REPO, "wiki", "survey", "2026-07-19-sf-identity-taxonomy-v5.json"
)
CODING = os.path.join(
    REPO, "wiki", "survey", "current", "data", "known-item-coding-v7.json"
)
SIDECAR_DIR = os.path.join(
    REPO, "wiki", "survey", "current", "data", "schema-v3", "sidecars"
)
ADJUDICATION = os.path.join(REPO, *ADJUDICATION_RELATIVE_PATH.split("/"))
ACTIVE_TAXONOMY = "wiki/survey/current/data/identity-taxonomy-v6.json"
INDEP = os.path.join(
    REPO, "wiki", "survey", "2026-07-18-sf-independent-counterexamples-v1.json"
)
INDEP2 = os.path.join(
    REPO, "wiki", "survey", "2026-07-19-sf-independent-counterexamples-v2.json"
)
INDEP3 = os.path.join(
    REPO, "wiki", "survey", "2026-07-19-sf-independent-counterexamples-v3.json"
)
OUT_DIR = os.path.join(
    REPO, "docs", "checks", "system-first-stage1a", "evidence-v6"
)
OUT = os.path.join(OUT_DIR, "identity-taxonomy-v6-test.json")


def _repo_display_path(path):
    path = Path(path).resolve()
    try:
        return path.relative_to(Path(REPO).resolve()).as_posix()
    except ValueError:
        return str(path)


def _provenance_entry(path, raw_bytes):
    return {
        "path": _repo_display_path(path),
        "sha256": hashlib.sha256(raw_bytes).hexdigest(),
    }


def _read_snapshot_json(path):
    path = Path(path)
    if path.is_symlink():
        raise ValueError(f"active JSON input may not be a symlink: {path}")
    return read_strict_json(path)


def _load_input_snapshot():
    taxonomy_v5, taxonomy_v5_raw = _read_snapshot_json(TAX_V5)
    taxonomy_v5_sha256 = hashlib.sha256(taxonomy_v5_raw).hexdigest()
    if taxonomy_v5_sha256 != FROZEN_TAXONOMY_V5_SHA256:
        raise ValueError(
            "frozen taxonomy-v5 SHA-256 mismatch "
            f"(expected={FROZEN_TAXONOMY_V5_SHA256}, "
            f"found={taxonomy_v5_sha256})"
        )
    taxonomy_v6, taxonomy_v6_raw = _read_snapshot_json(TAX)
    coding, coding_raw = _read_snapshot_json(CODING)
    try:
        coding_text = coding_raw.decode("utf-8")
    except UnicodeDecodeError as error:  # Defensive; strict loader already checked.
        raise JsonContractError(f"{CODING}: {error}") from error
    release = load_active_release(REPO, SIDECAR_DIR, ADJUDICATION)
    validate_coding_lineage(coding, REPO)
    rows = coding.get("rows") if isinstance(coding, dict) else None
    if not isinstance(rows, list):
        raise ValueError("active coding rows container invalid")
    sidecars = [(name, document) for name, document, _ in release.sidecars]
    provenance = {
        "taxonomy_v5": _provenance_entry(TAX_V5, taxonomy_v5_raw),
        "taxonomy": _provenance_entry(TAX, taxonomy_v6_raw),
        "coding": _provenance_entry(CODING, coding_raw),
        "adjudication": _provenance_entry(
            ADJUDICATION, release.adjudication_raw
        ),
        "sidecars": [
            {
                "path": _repo_display_path(Path(SIDECAR_DIR) / name),
                "sha256": hashlib.sha256(raw).hexdigest(),
            }
            for name, _, raw in release.sidecars
        ],
    }
    return {
        "taxonomy_v5": taxonomy_v5,
        "taxonomy_v6": taxonomy_v6,
        "coding": coding,
        "coding_text": coding_text,
        "rows": rows,
        "sidecars": sidecars,
        "adjudication": release.adjudication,
        "input_provenance": provenance,
        "input_snapshot_sha256": hashlib.sha256(
            canonical_bytes(provenance)
        ).hexdigest(),
    }


def load_sidecar_docs():
    return _load_input_snapshot()["sidecars"]


def load_current_inputs():
    snapshot = _load_input_snapshot()
    return snapshot["sidecars"], snapshot["coding_text"], snapshot["rows"]


def render_v7(sidecars):
    return render(sidecars, taxonomy=ACTIVE_TAXONOMY, profile="v7")


def ledger_index(relative_path):
    """Copy of v5 ledger resolution with deterministic handle ownership."""
    try:
        path = validate_repo_relative_path(relative_path, REPO)
        entries, _ = read_jsonl(path)
    except (ValueError, JsonContractError):
        return None
    index = []
    for entry in entries:
        if not isinstance(entry, dict):
            return None
        entry_id = entry.get("arxiv_id") or entry.get("id")
        kind = entry.get("kind") or (
            "pdf" if str(entry.get("url", "")).endswith(".pdf") else None
        )
        index.append(
            {
                "id": entry_id,
                "kind": kind,
                "sha256": entry.get("sha256"),
                "stored_at": entry.get("stored_at"),
            }
        )
    return index


def canon_sections(relative_path):
    """Copy of v5 canonical-section resolution with owned file handles."""
    path = validate_repo_relative_path(relative_path, REPO)
    with io.open(path, encoding="utf-8") as handle:
        text = handle.read()
    sections = {}
    current_key = None
    current_lines = []
    for line in text.splitlines():
        match = re.match(r"^##\s+(\S+)", line)
        if match and not line.startswith("###"):
            if current_key:
                sections[current_key] = "\n".join(current_lines)
            current_key, current_lines = match.group(1), [line]
        elif current_key:
            current_lines.append(line)
    if current_key:
        sections[current_key] = "\n".join(current_lines)
    return sections


class _CachedPage:
    def __init__(self, text=None, error=None):
        self._text = text
        self._error = error

    def extract_text(self):
        if self._error is not None:
            raise self._error
        return self._text


class _CachedReader:
    def __init__(self, pages):
        self.pages = pages


class EvidenceCache:
    """One explicit input-snapshot/run cache; never shared implicitly."""

    def __init__(self):
        self.pdf = {}
        self.tex = {}


def _asset_cache_key(asset_path, ledger_sha256, kind, extractor_identity):
    asset_path = Path(asset_path).resolve(strict=True)
    stat = asset_path.stat()
    return (
        os.path.normcase(str(asset_path)),
        ledger_sha256,
        kind,
        extractor_identity,
        stat.st_size,
        stat.st_mtime_ns,
        getattr(stat, "st_ino", None),
        getattr(stat, "st_dev", None),
    )


def _open_pdf_reader(path):
    import pypdf

    return pypdf.PdfReader(path)


def _pdf_extractor_identity():
    import pypdf

    return f"pypdf:{pypdf.__version__}:PdfReader.extract_text:v1"


def _cached_pdf_reader(stored_at, ledger_sha256, kind, cache):
    """Cache page extraction only under path+hash+kind+extractor+stat identity."""
    try:
        asset_path = Path(resolve_asset_path(stored_at)).resolve(strict=True)
        key = _asset_cache_key(
            asset_path,
            ledger_sha256,
            kind,
            _pdf_extractor_identity(),
        )
    except (OSError, ValueError):
        return None
    if key in cache.pdf:
        return cache.pdf[key]
    try:
        raw_reader = _open_pdf_reader(asset_path)
    except Exception:
        cache.pdf[key] = None
        return None
    pages = []
    for page in raw_reader.pages:
        try:
            pages.append(_CachedPage(normalized_phrase(page.extract_text() or "")))
        except Exception as error:  # check_page_locator must still fail closed.
            pages.append(_CachedPage(error=error))
    reader = _CachedReader(pages)
    cache.pdf[key] = reader
    return reader


def _norm_tex(text):
    text = re.sub(r"\\[a-zA-Z]+", " ", text)
    return re.sub(r"\s+", " ", re.sub(r"[\\${}~]", "", text)).strip().lower()


def _cached_tex_text(stored_at, ledger_sha256, kind, cache):
    try:
        asset_path = Path(resolve_asset_path(stored_at)).resolve(strict=True)
        key = _asset_cache_key(
            asset_path,
            ledger_sha256,
            kind,
            "tarfile+gzip.tex-normalize:v1",
        )
    except (OSError, ValueError):
        return ""
    if key in cache.tex:
        return cache.tex[key]
    text = ""
    try:
        with tarfile.open(asset_path, "r:gz") as archive:
            for member in archive.getmembers():
                if member.name.endswith(".tex"):
                    extracted = archive.extractfile(member)
                    if extracted is not None:
                        text += extracted.read().decode("utf-8", errors="replace")
    except tarfile.ReadError:
        try:
            with gzip.open(asset_path, "rb") as handle:
                text = handle.read().decode("utf-8", errors="replace")
        except OSError:
            text = ""
    cache.tex[key] = _norm_tex(text)
    return cache.tex[key]


def _check_evidence_entry_v6(
    entry,
    expected,
    field,
    section_text,
    tex_norm,
    reader,
    pid,
    what,
    failures,
):
    """Resolve one field binding while preserving v5 canon/TeX/absence rules."""
    if not isinstance(entry, dict):
        failures.append(f"{pid}:{what}:evidence-entry-invalid")
        return
    if not values_equal(expected, entry.get("value")):
        failures.append(f"{pid}:{what}:evidence-value-mismatch")

    kind = entry.get("kind")
    if kind == "canon":
        quote = entry.get("quote", "")
        if not (section_text and quote in section_text):
            failures.append(f"{pid}:{what}:evidence-quote-missing")
    elif kind == "tex":
        # Reuse v5's exact TeX normalization and quote resolution by presenting
        # the binding as a locator to its frozen resolver.
        check_quotes(
            f"tex: '{entry.get('quote', '')}'",
            section_text,
            tex_norm,
            pid,
            what,
            failures,
        )
    elif kind == "pdf_page":
        page = entry.get("page")
        anchor = entry.get("anchor")
        if not isinstance(page, int) or isinstance(page, bool) or not anchor:
            failures.append(f"{pid}:{what}:pdf-page-entry-incomplete")
        else:
            check_page_locator(
                f"p{page} anchor='{anchor}'", reader, pid, what, failures
            )
    elif kind == "absence":
        if not entry.get("note") or not entry.get("scope"):
            failures.append(f"{pid}:{what}:absence-entry-incomplete")
    else:
        failures.append(f"{pid}:{what}:evidence-kind-invalid")


def reconcile_v6(sidecars, coding_text, evidence_cache=None):
    """Reconcile active schema-v3 sidecars against pinned source material."""
    failures = []
    evidence_cache = evidence_cache or EvidenceCache()
    try:
        expected = render(
            sidecars, taxonomy=ACTIVE_TAXONOMY, profile="v7"
        )
    except (SystemExit, ValueError) as error:
        return [f"generator:{error}"]
    if coding_text != expected:
        failures.append("single-write:coding-not-byte-identical-to-generator-output")

    ledgers = {}
    sections_cache = {}
    for _, sidecar in sidecars:
        work_id = sidecar.get("paper_work_id")
        status = sidecar.get("schema_v3_binding_status")
        if status != "ADJUDICATED_AGREE":
            failures.append(f"{work_id}:schema-v3-binding-status:{status}")

        fulltext = sidecar.get("fulltext", {})
        ledger_ref = fulltext.get("ledger")
        if ledger_ref not in ledgers:
            ledgers[ledger_ref] = ledger_index(ledger_ref) if ledger_ref else None
        ledger = ledgers[ledger_ref]
        ledger_row = None
        if ledger is None:
            failures.append(f"{work_id}:ledger-missing:{ledger_ref}")
        else:
            ledger_row = next(
                (
                    row
                    for row in ledger
                    if row["id"] == fulltext.get("id")
                    and row["kind"] == fulltext.get("kind")
                    and row["sha256"] == fulltext.get("sha256")
                    and row["sha256"]
                ),
                None,
            )
            if ledger_row is None:
                failures.append(
                    f"{work_id}:ledger-row-binding-failed:id+kind+sha256"
                )
        if fulltext.get("id") != work_id:
            failures.append(f"{work_id}:fulltext-id-mismatch:{fulltext.get('id')}")

        canonical_id = sidecar.get("canonical_record_id") or ""
        canonical_file, _, anchor = canonical_id.partition("#")
        try:
            validate_canonical_record_id(canonical_id, REPO)
        except ValueError as error:
            failures.append(f"{work_id}:canonical-record-id-invalid:{error}")
        if canonical_file not in sections_cache:
            try:
                sections_cache[canonical_file] = canon_sections(canonical_file)
            except (OSError, ValueError):
                sections_cache[canonical_file] = None
        sections = sections_cache[canonical_file]
        section_text = None
        if sections is None:
            failures.append(f"{work_id}:canon-file-missing:{canonical_file}")
        elif anchor not in sections:
            failures.append(f"{work_id}:canon-heading-unresolved:#{anchor}")
        else:
            section_text = sections[anchor]
        if anchor != work_id:
            failures.append(f"{work_id}:anchor-vs-work-id:{anchor}")

        tex_norm = ""
        reader = None
        if ledger_row and ledger_row.get("stored_at"):
            if fulltext.get("kind") == "eprint":
                tex_norm = _cached_tex_text(
                    ledger_row["stored_at"],
                    ledger_row["sha256"],
                    fulltext.get("kind"),
                    evidence_cache,
                )
                if not tex_norm:
                    failures.append(
                        f"{work_id}:eprint-unreadable:{ledger_row['stored_at']}"
                    )
            elif fulltext.get("kind") == "pdf":
                reader = _cached_pdf_reader(
                    ledger_row["stored_at"],
                    ledger_row["sha256"],
                    fulltext.get("kind"),
                    evidence_cache,
                )

        for method_path in sidecar.get("method_paths", []):
            pid = method_path.get("method_path_id", "?")
            if not pid.startswith(work_id + "#"):
                failures.append(
                    f"{pid}:method-path-prefix-vs-work-id:{work_id}"
                )
            check_quotes(
                method_path.get("source_locator"),
                section_text,
                tex_norm,
                pid,
                "row-locator",
                failures,
            )
            check_page_locator(
                method_path.get("source_locator"),
                reader,
                pid,
                "row-locator",
                failures,
            )

            signal_ids = set()
            for signal in method_path.get("signals", []):
                signal_id = signal.get("signal_id")
                signal_ids.add(signal_id)
                check_quotes(
                    signal.get("evidence"),
                    section_text,
                    tex_norm,
                    pid,
                    f"signal:{signal_id}",
                    failures,
                )
                check_page_locator(
                    signal.get("evidence"),
                    reader,
                    pid,
                    f"signal:{signal_id}",
                    failures,
                )
                claim_evidence = signal.get("claim_evidence") or {}
                for field in SIGNAL_REQUIRED_FIELDS:
                    entry = claim_evidence.get(field)
                    if entry is None:
                        failures.append(
                            f"{pid}:signal:{signal_id}:{field}:"
                            "required-evidence-missing"
                        )
                        continue
                    _check_evidence_entry_v6(
                        entry,
                        signal.get(field),
                        field,
                        section_text,
                        tex_norm,
                        reader,
                        pid,
                        f"signal-binding:{signal_id}:{field}",
                        failures,
                    )

            for edge_index, edge in enumerate(method_path.get("control_edges", [])):
                if edge.get("signal_id") not in signal_ids:
                    failures.append(
                        f"{pid}:edge-references-unknown-signal:"
                        f"{edge.get('signal_id')}"
                    )
                check_quotes(
                    edge.get("source_locator"),
                    section_text,
                    tex_norm,
                    pid,
                    "edge-locator",
                    failures,
                )
                check_page_locator(
                    edge.get("source_locator"),
                    reader,
                    pid,
                    "edge-locator",
                    failures,
                )
                claim_evidence = edge.get("claim_evidence") or {}
                for field in EDGE_REQUIRED_FIELDS:
                    entry = claim_evidence.get(field)
                    if entry is None:
                        failures.append(
                            f"{pid}:edge:{edge_index}:{field}:"
                            "required-evidence-missing"
                        )
                        continue
                    _check_evidence_entry_v6(
                        entry,
                        edge.get(field),
                        field,
                        section_text,
                        tex_norm,
                        reader,
                        pid,
                        f"edge-binding:{edge_index}:{field}",
                        failures,
                    )

            row_evidence = method_path.get("claim_evidence") or {}
            for field in ROW_REQUIRED_FIELDS:
                entry = row_evidence.get(field)
                if entry is None:
                    failures.append(
                        f"{pid}:row:{field}:required-evidence-missing"
                    )
                    continue
                _check_evidence_entry_v6(
                    entry,
                    method_path.get(field),
                    field,
                    section_text,
                    tex_norm,
                    reader,
                    pid,
                    f"row-binding:{field}",
                    failures,
                )

            coder = method_path.get("coder") or sidecar.get("coder")
            adjudicator = method_path.get("semantic_adjudicator")
            if coder in (None, "", "W1") or adjudicator in (None, "", "W1"):
                failures.append(f"{pid}:actor-id-invalid")
            if method_path.get("load_bearing"):
                if method_path.get("adjudication_status") != "adjudicated_agree":
                    failures.append(
                        f"{pid}:load-bearing-not-adjudicated:"
                        f"{method_path.get('adjudication_status')}"
                    )
                elif method_path.get("adjudication_row_sha256") != row_hash(
                    method_path
                ):
                    failures.append(
                        f"{pid}:adjudication-row-hash-mismatch "
                        "(post-adjudication change)"
                    )
                if coder == adjudicator:
                    failures.append(
                        f"{pid}:coder==adjudicator on load-bearing row"
                    )
    return failures


def validate_load_bearing_contract(
    rows, sidecars, coding_text, evidence_cache=None
):
    """Run the three contract layers in their required fail-closed order."""
    structure_failures = validate(rows)
    binding_failures = sum(
        (validate_bound_values(row) for row in rows), []
    )
    if evidence_cache is None:
        source_failures = reconcile_v6(sidecars, coding_text)
    else:
        source_failures = reconcile_v6(sidecars, coding_text, evidence_cache)
    return {
        "structure": structure_failures,
        "bindings": binding_failures,
        "source": source_failures,
    }


def occupancy(policy, rows):
    """Frozen verbatim v5 occupancy computation, lifted out of v5 main()."""
    derived_rows = [dict(adapt(row), **derive(row, policy)) for row in rows]
    works = sorted({row["paper_work_id"] for row in derived_rows})
    n_paths, n_works = len(derived_rows), len(works)
    by_selection_object = {}
    for row in derived_rows:
        if (
            row["data_access_strict_bits"]
            and row["is_reward_guided"]
            and row["explicit_candidate_pool_selection"]
        ):
            by_selection_object.setdefault(row["selection_object"], []).append(
                row["method_path_id"]
            )

    def dual(paths):
        unique_works = sorted(
            {
                next(
                    row["paper_work_id"]
                    for row in derived_rows
                    if row["method_path_id"] == path
                )
                for path in paths
            }
        )
        return {
            "method_paths": sorted(paths),
            "n_paths": f"{len(paths)}/{n_paths}",
            "unique_works": unique_works,
            "n_works": f"{len(unique_works)}/{n_works}",
        }

    return {
        "n_method_paths": n_paths,
        "n_unique_works": n_works,
        "is_reward_guided": dual(
            [
                row["method_path_id"]
                for row in derived_rows
                if row["is_reward_guided"]
            ]
        ),
        "is_rq_sys_control_compatible": dual(
            [
                row["method_path_id"]
                for row in derived_rows
                if row["is_rq_sys_control_compatible"]
            ]
        ),
        "is_s0_core_compatible": dual(
            [
                row["method_path_id"]
                for row in derived_rows
                if row["is_s0_core_compatible"]
            ]
        ),
        "is_project_method_candidate": dual(
            [
                row["method_path_id"]
                for row in derived_rows
                if row["is_project_method_candidate"]
            ]
        ),
        "strict_AND_reward_AND_pool_BY_selection_object(mechanism)": {
            key: dual(value)
            for key, value in sorted(by_selection_object.items())
        },
        "reward_guided_selection": dual(
            [
                row["method_path_id"]
                for row in derived_rows
                if row["reward_guided_selection"]
            ]
        ),
        "learned_rm_prm_AND_pool": dual(
            [
                row["method_path_id"]
                for row in derived_rows
                if any(
                    signal.get("source") == "learned_rm_prm"
                    for signal in row.get("signals", [])
                )
                and row["explicit_candidate_pool_selection"]
            ]
        ),
        "core_native_audio_or_omni": dual(
            [
                row["method_path_id"]
                for row in derived_rows
                if row["core_native_modality"] in ("audio_native", "omni_native")
            ]
        ),
    }


def _binding(value):
    return {"kind": "canon", "value": copy.deepcopy(value), "quote": "fixture"}


def generic_row():
    """Generic schema-v3 row used only for the ID-independent 12th-row check."""
    row = {
        "method_path_id": "__fx12__#path",
        "paper_work_id": "__fx12__",
        "core_topology": "single_core",
        "core_native_modality": "omni_native",
        "internal_visibility": "api_only",
        "core_io_modality": "text_in_text_out",
        "core_weight_update": False,
        "external_component_weight_update": False,
        "controller_program_or_config_optimized_on_labels": False,
        "human_or_dev_label_model_selection": False,
        "deployment_label_access": False,
        "test_item_gold_access": False,
        "inference_external_new_information": False,
        "control_horizon": "sequential",
        "decision_rights": ["branch"],
        "selection_object": "candidate_output",
        "terminal_operator": "select_one",
        "explicit_candidate_pool_selection": True,
        "candidate_pool_exists": True,
        "selection_policy": "scored_select",
        "includes_speech_audio": False,
        "adjudication_required": False,
        "load_bearing": False,
        "fulltext_ref": "fixture",
        "canonical_record_id": "fixture",
        "source_locator": "fixture",
        "coder": "fixture-coder",
        "semantic_adjudicator": "fixture-adjudicator",
        "adjudication_status": "adjudicated_agree",
    }
    row["claim_evidence"] = {
        field: _binding(row[field]) for field in ROW_REQUIRED_FIELDS
    }
    signal = {
        "signal_id": "s1",
        "form": "scalar_score",
        "source": "llm_judge",
        "lifecycle": "online_step",
        "uses": ["prune"],
        "evidence": "fixture",
    }
    signal["claim_evidence"] = {
        field: _binding(signal[field]) for field in SIGNAL_REQUIRED_FIELDS
    }
    edge = {
        "signal_id": "s1",
        "signal_use": "prune",
        "decision_right": "branch",
        "source_locator": "fixture",
        "edge_semantics": "fixture signal prunes a branch",
    }
    edge["claim_evidence"] = {
        field: _binding(edge[field]) for field in EDGE_REQUIRED_FIELDS
    }
    row["signals"] = [signal]
    row["control_edges"] = [edge]
    return row


def _sidecar(sidecars, work_id):
    return next(sidecar for _, sidecar in sidecars if sidecar["paper_work_id"] == work_id)


def _restamp(sidecars):
    for _, sidecar in sidecars:
        for row in sidecar["method_paths"]:
            row["adjudication_row_sha256"] = row_hash(row)


def run_mutation_suite(sidecars, coding_text):
    """Run frozen and schema-v3 mutations against a clean simulated snapshot."""
    stamped = copy.deepcopy(sidecars)
    for _, sidecar in stamped:
        for row in sidecar["method_paths"]:
            row["semantic_adjudicator"] = "sim-adj:harness"
            row["adjudication_status"] = "adjudicated_agree"
            row["adjudication_row_sha256"] = row_hash(row)
    stamped_coding = render_v7(stamped)
    evidence_cache = EvidenceCache()
    clean_contract = validate_load_bearing_contract(
        json.loads(stamped_coding)["rows"],
        stamped,
        stamped_coding,
        evidence_cache,
    )
    baseline = {key: set(value) for key, value in clean_contract.items()}
    results = {}

    def mutate(name, mutate_sidecars=None, mutate_coding=None, restamp=False):
        mutated = copy.deepcopy(stamped)
        current_coding = stamped_coding
        if mutate_sidecars is not None:
            mutate_sidecars(mutated)
            if restamp:
                _restamp(mutated)
            current_coding = render_v7(mutated)
        if mutate_coding is not None:
            current_coding = mutate_coding(current_coding)
        rows = json.loads(current_coding)["rows"]
        contract = validate_load_bearing_contract(
            rows, mutated, current_coding, evidence_cache
        )
        new_failures = set()
        for layer, failures in contract.items():
            new_failures.update(set(failures) - baseline[layer])
        results[name] = sorted(new_failures)

    def row(sidecars_, work_id, index=0):
        return _sidecar(sidecars_, work_id)["method_paths"][index]

    def wrong_work(sidecars_):
        sidecar = _sidecar(sidecars_, "2606.01667")
        sidecar["paper_work_id"] = "bogus-work"
        sidecar["fulltext"]["id"] = "bogus-work"

    def horizon(sidecars_):
        row(sidecars_, "2026.findings-acl.1243", 1)["control_horizon"] = "terminal"

    def horizon_double(sidecars_):
        method = row(sidecars_, "2026.findings-acl.1243", 1)
        method["control_horizon"] = "terminal"
        method["claim_evidence"]["control_horizon"]["value"] = "terminal"

    def fake_page(sidecars_):
        row(sidecars_, "2606.01667")["source_locator"] = (
            "p9999 anchor='distinctive but impossible page locator phrase'"
        )

    def lifecycle(sidecars_):
        row(sidecars_, "2026.findings-acl.1243", 1)["control_edges"][0][
            "signal_lifecycle"
        ] = "terminal"

    def signal_identity(sidecars_):
        row(sidecars_, "2026.findings-acl.511")["control_edges"][0][
            "signal_id"
        ] = "s_ghost"

    def wrong_right(sidecars_):
        row(sidecars_, "2026.findings-acl.1724")["decision_rights"] = [
            "memory_write"
        ]

    def wrong_policy(sidecars_):
        row(sidecars_, "2604.16529", 1)["selection_policy"] = "scored_select"

    def wrong_modality(sidecars_):
        row(sidecars_, "2606.01667")["core_native_modality"] = "text_only"

    def wrong_sha(sidecars_):
        _sidecar(sidecars_, "2606.01667")["fulltext"]["sha256"] = "0" * 64

    def wrong_kind(sidecars_):
        _sidecar(sidecars_, "2606.01667")["fulltext"]["kind"] = "eprint"

    def nonsense(sidecars_):
        row(sidecars_, "2606.01667")["source_locator"] = "nonsense"

    def e1(sidecars_):
        row(sidecars_, "2026.findings-acl.1724")["control_edges"][0][
            "signal_use"
        ] = "select"

    def e2(sidecars_):
        row(sidecars_, "2606.01667")["signals"][0]["evidence"] = "p9999"

    def e3(sidecars_):
        row(sidecars_, "2606.01667")["source_locator"] = "p1"

    def e3b(sidecars_):
        row(sidecars_, "2606.01667")["source_locator"] = "p1 anchor='the'"

    def e3c(sidecars_):
        row(sidecars_, "2606.01667")["source_locator"] = (
            "p1 anchor='the orchestrator'"
        )

    def e4(sidecars_):
        row(sidecars_, "2026.findings-acl.1724")["signals"][0][
            "form"
        ] = "text_critique"

    def e6(sidecars_):
        row(sidecars_, "2026.findings-acl.1724")["signals"][0][
            "source"
        ] = "consensus"

    def e7(sidecars_):
        method = row(sidecars_, "2026.findings-acl.1724")
        signal = method["signals"][0]
        signal["uses"] = ["select"]
        signal["claim_evidence"]["uses"]["value"] = ["select"]
        method["control_edges"][0]["signal_use"] = "select"

    def e8(sidecars_):
        method = row(sidecars_, "2026.findings-acl.1724")
        method["decision_rights"] = ["supply"]
        method["claim_evidence"]["decision_rights"]["value"] = ["supply"]
        method["control_edges"][0]["decision_right"] = "supply"

    def e9(sidecars_):
        row(sidecars_, "2026.findings-acl.1724")["selection_object"] = "trajectory"

    def e10(sidecars_):
        row(sidecars_, "2026.findings-acl.1724")[
            "explicit_candidate_pool_selection"
        ] = False

    def e11(sidecars_):
        del row(sidecars_, "2026.findings-acl.1724")["signals"][0][
            "claim_evidence"
        ]["source"]

    def e12(sidecars_):
        del row(sidecars_, "2026.findings-acl.1724")["control_edges"][0][
            "claim_evidence"
        ]["decision_right"]

    for name, mutation, restamp in (
        ("E1_edge_use_flip", e1, True),
        ("E2_signal_evidence_p9999", e2, True),
        ("E3_bare_in_range_page", e3, True),
        ("E3b_generic_anchor_the", e3b, True),
        ("E3c_frequent_phrase", e3c, True),
        ("E4_signal_form_flip", e4, True),
        ("E6_signal_source_flip", e6, True),
        ("E7_edge_use_coherent_flip", e7, True),
        ("E8_edge_right_coherent_flip", e8, True),
        ("E9_selection_object_flip", e9, True),
        ("E10_explicit_selection_flip", e10, True),
        ("E11_missing_signal_source_binding", e11, True),
        ("E12_missing_edge_right_binding", e12, True),
        ("wrong_horizon", horizon, False),
        ("double_flip_horizon_plus_evidence", horizon_double, False),
        ("fake_page_p9999", fake_page, False),
        ("edge_signal_lifecycle_mismatch", lifecycle, False),
        ("edge_signal_identity_mismatch", signal_identity, False),
        ("wrong_decision_right", wrong_right, False),
        ("wrong_selection_policy", wrong_policy, False),
        ("wrong_work", wrong_work, False),
        ("wrong_modality", wrong_modality, False),
        ("wrong_sha", wrong_sha, False),
        ("wrong_kind", wrong_kind, False),
        ("nonsense_locator", nonsense, False),
    ):
        mutate(name, mutate_sidecars=mutation, restamp=restamp)

    mutate(
        "E5_coding_hand_edit",
        mutate_coding=lambda text: text.replace(
            '"control_horizon": "sequential"',
            '"control_horizon": "terminal"',
            1,
        ),
    )

    expected_codes = {
        "E1_edge_use_flip": "edge-use-not-in-signal",
        "E2_signal_evidence_p9999": "page-token-without-anchor",
        "E3_bare_in_range_page": "page-token-without-anchor",
        "E3b_generic_anchor_the": "page-anchor-too-weak",
        "E3c_frequent_phrase": "page-anchor-not-discriminative",
        "E4_signal_form_flip": "evidence-value-mismatch",
        "E5_coding_hand_edit": "single-write:coding-not-byte-identical",
        "E6_signal_source_flip": "signal:s_stage_judge:source:evidence-value-mismatch",
        "E7_edge_use_coherent_flip": "edge:0:signal_use:evidence-value-mismatch",
        "E8_edge_right_coherent_flip": "edge:0:decision_right:evidence-value-mismatch",
        "E9_selection_object_flip": "row:selection_object:evidence-value-mismatch",
        "E10_explicit_selection_flip": (
            "row:explicit_candidate_pool_selection:evidence-value-mismatch"
        ),
        "E11_missing_signal_source_binding": (
            "signal:s_stage_judge:source:required-evidence-missing"
        ),
        "E12_missing_edge_right_binding": (
            "edge:0:decision_right:required-evidence-missing"
        ),
        "wrong_horizon": "row-hash",
        "double_flip_horizon_plus_evidence": "row-hash",
        "fake_page_p9999": "page-out-of-range",
        "edge_signal_lifecycle_mismatch": "lifecycle-mismatch",
        "edge_signal_identity_mismatch": "unknown-signal",
        "wrong_decision_right": "edge-right-not-in-row",
        "wrong_selection_policy": "evidence-value-mismatch",
        "wrong_work": "method-path-prefix-vs-work-id",
        "wrong_modality": "evidence-value-mismatch",
        "wrong_sha": "ledger-row-binding-failed",
        "wrong_kind": "ledger-row-binding-failed",
        "nonsense_locator": "locator-unverifiable",
    }
    clean = {key: sorted(value) for key, value in baseline.items()}
    ok = not any(clean.values()) and all(
        results[name]
        and any(code in failure for failure in results[name])
        for name, code in expected_codes.items()
    )
    for name in (
        "E6_signal_source_flip",
        "E7_edge_use_coherent_flip",
        "E8_edge_right_coherent_flip",
        "E9_selection_object_flip",
        "E10_explicit_selection_flip",
        "E11_missing_signal_source_binding",
        "E12_missing_edge_right_binding",
    ):
        ok = ok and not any("row-hash" in failure for failure in results[name])
    return clean, results, ok


def _frozen_fixture_checks(rows):
    """Return K1-K7 and A1-A8 results without changing v5 fixture inputs."""
    checks = []

    def add(check_id, description, ok, detail=""):
        checks.append(
            {
                "id": check_id,
                "check": description,
                "result": "PASS" if ok else "FAIL",
                "detail": str(detail),
            }
        )

    unknown_modality = derive(base_row(core_native_modality="unknown"))
    unknown_strict = derive(
        base_row(core_native_modality="omni_native", core_weight_update="unknown")
    )
    add(
        "V2",
        "unknown never satisfies topology or strict access bits",
        unknown_modality["is_project_method_candidate"] is False
        and unknown_strict["data_access_strict_bits"] is False
        and unknown_strict["is_s0_core_compatible"] is False,
    )

    k1 = base_row(core_native_modality="audio_native")
    k2 = base_row(
        core_native_modality="omni_native",
        signal_form="verifiable_outcome",
        signal_source="environment",
        signal_lifecycle="online_step",
        signal_use=["tool_call", "stop_budget"],
        control_horizon="sequential",
        decision_rights=["tool_call", "stop"],
        control_edges=[
            fx_edge("tool_call", "tool_call"),
            fx_edge("stop_budget", "stop"),
        ],
    )
    k3 = base_row(
        signal_form="verifiable_outcome",
        signal_source="environment",
        signal_lifecycle="online_step",
        signal_use=["retry", "stop_budget"],
        control_horizon="sequential",
        decision_rights=["retry", "stop"],
        control_edges=[fx_edge("retry", "retry")],
    )
    k4 = base_row(
        signal_form="scalar_score",
        signal_source="llm_judge",
        signal_lifecycle="online_step",
        signal_use=["select"],
        control_horizon="sequential",
        decision_rights=["memory_write"],
    )
    k5 = base_row(
        signal_form="scalar_score",
        signal_source="llm_judge",
        signal_lifecycle="online_step",
        signal_use=["select"],
        control_horizon="sequential",
        decision_rights=["memory_write"],
        control_edges=[fx_edge("select", "memory_write")],
    )
    k6 = base_row(
        signal_form="pairwise_comparison",
        signal_source="llm_judge",
        signal_lifecycle="terminal",
        signal_use=["select"],
        control_horizon="sequential",
        decision_rights=["memory_write"],
    )
    k7 = base_row(
        core_native_modality="omni_native",
        signal_form="pairwise_comparison",
        signal_source="llm_judge",
        signal_lifecycle="terminal",
        signal_use=["select"],
        control_horizon="sequential",
        decision_rights=["branch"],
        control_edges=[fx_edge("select", "branch")],
    )
    killers = {
        name: derive(value)
        for name, value in {
            "k1": k1,
            "k2": k2,
            "k3": k3,
            "k4": k4,
            "k5": k5,
            "k6": k6,
            "k7": k7,
        }.items()
    }
    add(
        "V3",
        "frozen killers K1-K7",
        killers["k1"]["is_s0_core_compatible"]
        and not killers["k1"]["is_project_method_candidate"]
        and killers["k2"]["is_rq_sys_control_compatible"]
        and killers["k2"]["is_project_method_candidate"]
        and killers["k3"]["is_reward_guided"]
        and not killers["k4"]["is_rq_sys_control_compatible"]
        and not killers["k5"]["is_rq_sys_control_compatible"]
        and not killers["k6"]["is_rq_sys_control_compatible"]
        and not killers["k7"]["is_rq_sys_control_compatible"]
        and killers["k7"]["is_reward_guided"],
        {
            key: value["is_rq_sys_control_compatible"]
            for key, value in killers.items()
        },
    )

    a1_row = base_row(
        signal_form="scalar_score",
        signal_source="llm_judge",
        signal_lifecycle="online_step",
        signal_use=["revise"],
        control_horizon="sequential",
        decision_rights=["retry"],
        control_edges=[fx_edge("revise", "retry", "terminal")],
    )
    a1_derive = derive(a1_row)
    a1_validate = validate(
        [
            dict(
                adapt(a1_row),
                load_bearing=False,
                adjudication_status="adjudicated_agree",
                fulltext_ref="x",
                canonical_record_id="x",
                source_locator="x",
                coder="fx",
                semantic_adjudicator="fx2",
            )
        ]
    )
    a2 = base_row(
        core_native_modality="omni_native",
        signals=[
            {
                "signal_id": "s_reward",
                "form": "scalar_score",
                "source": "llm_judge",
                "lifecycle": "terminal",
                "uses": ["select"],
                "evidence": "fixture",
            },
            {
                "signal_id": "s_route",
                "form": "text_critique",
                "source": "llm_judge",
                "lifecycle": "online_step",
                "uses": ["route"],
                "evidence": "fixture",
            },
        ],
        control_horizon="sequential",
        decision_rights=["tool_call"],
        control_edges=[
            {
                "signal_id": "s_route",
                "signal_use": "route",
                "decision_right": "tool_call",
                "source_locator": "fixture-locator",
                "edge_semantics": "route signal controls tool call",
            }
        ],
    )
    a2_derive = derive(a2)
    a3 = derive(
        base_row(
            signal_form="scalar_score",
            signal_source="llm_judge",
            signal_lifecycle="online_step",
            signal_use=["revise"],
            control_horizon="sequential",
            decision_rights=["retry"],
            control_edges=[fx_edge("revise", "retry")],
        )
    )
    a4 = derive(
        base_row(
            signal_form="pairwise_comparison",
            signal_source="llm_judge",
            signal_lifecycle="terminal",
            signal_use=["select", "prune"],
            control_horizon="sequential",
            decision_rights=["stop"],
            control_edges=[fx_edge("prune", "stop")],
        )
    )
    a6_bad = derive(
        base_row(
            signal_form="scalar_score",
            signal_source="llm_judge",
            signal_lifecycle="online_step",
            signal_use=["revise"],
            selection_object="candidate_output",
            explicit_candidate_pool_selection=True,
            candidate_pool_exists=True,
            selection_policy="scored_select",
        )
    )
    a7 = derive(
        base_row(
            signal_form="scalar_score",
            signal_source="llm_judge",
            signal_lifecycle="offline_calibration",
            signal_use=["select"],
            selection_object="candidate_output",
            explicit_candidate_pool_selection=True,
            candidate_pool_exists=True,
            selection_policy="scored_select",
        )
    )
    add(
        "V3a",
        "frozen acceptance A1-A7",
        any("lifecycle-mismatch" in failure for failure in a1_validate)
        and a1_derive["is_rq_sys_control_compatible"] is False
        and a2_derive["is_reward_guided"]
        and not a2_derive["is_rq_sys_control_compatible"]
        and not a2_derive["is_project_method_candidate"]
        and a3["is_rq_sys_control_compatible"]
        and a4["is_rq_sys_control_compatible"]
        and not a6_bad["reward_guided_selection"]
        and not a7["reward_guided_selection"]
        and not a7["is_reward_guided"],
    )

    author_cases = {
        "2604.16529#pdr-random-k": {
            "expect": {
                "is_reward_guided": False,
                "n_signals": 0,
                "candidate_pool_exists": True,
                "reward_guided_selection": False,
            }
        },
        "2604.16529#rtv": {
            "expect": {
                "is_reward_guided": True,
                "is_rq_sys_control_compatible": False,
                "reward_guided_selection": True,
            }
        },
        "2604.16529#rtv-pdr-pipeline": {
            "expect": {
                "is_reward_guided": True,
                "is_rq_sys_control_compatible": True,
            }
        },
        "2602.16485#calibrated-orchestration": {
            "expect": {
                "is_reward_guided": False,
                "is_rq_sys_control_compatible": False,
            }
        },
        "2606.03054#trained-gate": {
            "expect": {
                "signal_form": "binary_gate",
                "is_reward_guided": False,
                "is_rq_sys_control_compatible": False,
                "n_valid_live_edges": 1,
            }
        },
        "2606.01667#agentic-orchestration": {
            "expect": {
                "is_reward_guided": False,
                "is_rq_sys_control_compatible": False,
                "n_valid_live_edges": 3,
            }
        },
        "2605.08083#discovered-controller": {
            "expect": {
                "is_reward_guided": False,
                "n_signals": 2,
                "is_rq_sys_control_compatible": False,
                "n_valid_live_edges": 2,
            }
        },
        "2026.findings-acl.1724#pipeline": {
            "expect": {
                "is_reward_guided": True,
                "n_signals": 2,
                "is_rq_sys_control_compatible": True,
                "data_access_strict_bits": False,
            }
        },
        "2026.findings-acl.1243#closed-prompt-only": {
            "expect": {"is_rq_sys_control_compatible": True}
        },
        "2026.findings-acl.1243#open-sft-variant": {
            "expect": {
                "is_rq_sys_control_compatible": True,
                "core_native_modality": "text_only",
            }
        },
        "2026.findings-acl.511#prm-guided-search": {
            "expect": {"is_rq_sys_control_compatible": True}
        },
    }
    author_failures = run_expectations(author_cases, rows, "author")
    add(
        "V3b",
        "frozen author expectations including multi-signal A5",
        not author_failures,
        author_failures,
    )

    mutated_form = copy.deepcopy(rows)
    for method in mutated_form:
        if method["method_path_id"] == "2026.findings-acl.1724#pipeline":
            for signal in method["signals"]:
                signal["form"] = "consensus_vote"
    mutated_pdr = copy.deepcopy(rows)
    for method in mutated_pdr:
        if method["method_path_id"] == "2604.16529#pdr-random-k":
            method["signals"] = [
                {
                    "signal_id": "s_bad",
                    "form": "pairwise_comparison",
                    "source": "llm_judge",
                    "lifecycle": "online_step",
                    "uses": ["prune", "supply"],
                    "evidence": "x",
                }
            ]
    add(
        "V4",
        "frozen author negative controls",
        bool(run_expectations(author_cases, mutated_form, "author"))
        and bool(run_expectations(author_cases, mutated_pdr, "author")),
    )

    independent_failures = []
    n_cases = 0
    for path in (INDEP, INDEP2, INDEP3):
        if os.path.exists(path):
            independent, _ = read_strict_json(path)
            independent_failures.extend(
                run_expectations(
                    independent["cases"], rows, os.path.basename(path)
                )
            )
            n_cases += len(independent["cases"])
    add(
        "V5",
        f"independent counterexamples x{n_cases}, including A8",
        n_cases > 0 and not independent_failures,
        independent_failures[:6],
    )

    atlas = next(
        row
        for row in rows
        if row["method_path_id"] == "2606.01667#agentic-orchestration"
    )
    atlas_omni = dict(atlas, core_native_modality="omni_native")
    sensitivity_a = derive(
        atlas_omni, ("single_core", "single_core_multi_call")
    )["is_s0_core_compatible"]
    sensitivity_b = derive(atlas_omni, ("single_core",))[
        "is_s0_core_compatible"
    ]
    add(
        "V5b",
        "topology sensitivity is non-vacuous",
        sensitivity_a is True and sensitivity_b is False,
        f"A={sensitivity_a} strict={sensitivity_b}",
    )
    return checks


def _generic_row_check():
    good = generic_row()
    source = copy.deepcopy(good)
    source["signals"][0]["source"] = "learned_rm_prm"
    use = copy.deepcopy(good)
    use["signals"][0]["uses"] = ["select"]
    use["signals"][0]["claim_evidence"]["uses"]["value"] = ["select"]
    use["control_edges"][0]["signal_use"] = "select"
    selection = copy.deepcopy(good)
    selection["selection_object"] = "trajectory"
    missing = copy.deepcopy(good)
    del missing["control_edges"][0]["claim_evidence"]["decision_right"]
    checks = {
        "good_structure": validate([good]),
        "good_bindings": validate_bound_values(good),
        "source": validate_bound_values(source),
        "use": validate_bound_values(use),
        "selection": validate_bound_values(selection),
        "missing": validate_bound_values(missing),
    }
    ok = (
        not checks["good_structure"]
        and not checks["good_bindings"]
        and any("signal:s1:source:evidence-value-mismatch" in f for f in checks["source"])
        and any("edge:0:signal_use:evidence-value-mismatch" in f for f in checks["use"])
        and any("row:selection_object:evidence-value-mismatch" in f for f in checks["selection"])
        and any("edge:0:decision_right:required-evidence-missing" in f for f in checks["missing"])
    )
    return ok, checks


def build_report():
    snapshot = _load_input_snapshot()
    sidecars = snapshot["sidecars"]
    coding_text = snapshot["coding_text"]
    rows = snapshot["rows"]
    checks = []

    def add(check_id, description, ok, detail=""):
        checks.append(
            {
                "id": check_id,
                "check": description,
                "result": "PASS" if ok else "FAIL",
                "detail": str(detail),
            }
        )

    taxonomy_failures = validate_taxonomy_v6(
        snapshot["taxonomy_v5"], snapshot["taxonomy_v6"]
    )
    add(
        "V0",
        "taxonomy v6 exact delta over frozen taxonomy-v5 semantics",
        not taxonomy_failures,
        taxonomy_failures,
    )
    contract = validate_load_bearing_contract(
        rows, sidecars, coding_text, EvidenceCache()
    )
    add(
        "V1",
        "ordered structure -> row16/signal4/edge2 binding -> source contract",
        not any(contract.values()),
        {key: value[:8] for key, value in contract.items()},
    )
    checks.extend(_frozen_fixture_checks(rows))

    policy = ("single_core", "single_core_multi_call")
    occupancy_block = {
        "policy_A": occupancy(policy, rows),
        "sensitivity_strict_topology": occupancy(("single_core",), rows),
    }
    occupancy_repeat = {
        "policy_A": occupancy(policy, rows),
        "sensitivity_strict_topology": occupancy(("single_core",), rows),
    }
    add(
        "V6",
        "frozen occupancy recomputes deterministically with dynamic denominators",
        occupancy_block == occupancy_repeat
        and occupancy_block["policy_A"]["n_method_paths"] == len(rows)
        and occupancy_block["policy_A"]["n_unique_works"]
        == len({row["paper_work_id"] for row in rows}),
    )
    add(
        "V7",
        "active single-write, ledger/hash/canon/TeX/PDF, actors, and status reconcile",
        not contract["source"],
        contract["source"][:8],
    )

    clean, mutations, mutations_ok = run_mutation_suite(sidecars, coding_text)
    add(
        "V8",
        "frozen and schema-v3 mutations all fail closed with legitimate rehash",
        mutations_ok,
        {"baseline": clean, "cases": len(mutations)},
    )
    generic_ok, generic_detail = _generic_row_check()
    add(
        "V9",
        "generic twelfth row passes and generic value/missing-binding mutations fail",
        generic_ok,
        {key: value[:2] for key, value in generic_detail.items()},
    )

    policy_a = occupancy_block["policy_A"]
    mechanism = policy_a[
        "strict_AND_reward_AND_pool_BY_selection_object(mechanism)"
    ]
    exact_occupancy = (
        policy_a["is_reward_guided"]["n_paths"] == "6/11"
        and policy_a["is_rq_sys_control_compatible"]["n_paths"] == "5/11"
        and policy_a["is_project_method_candidate"]["n_paths"] == "0/11"
        and policy_a["reward_guided_selection"]["n_paths"] == "4/11"
        and mechanism["trajectory"]["n_paths"] == "2/11"
    )
    add(
        "V10",
        "taxonomy-v6 occupancy equals the frozen taxonomy-v5 baseline",
        exact_occupancy,
        {
            "reward_guided": policy_a["is_reward_guided"]["n_paths"],
            "rq_sys_compatible": policy_a["is_rq_sys_control_compatible"]["n_paths"],
            "method_candidate": policy_a["is_project_method_candidate"]["n_paths"],
            "reward_guided_selection": policy_a["reward_guided_selection"]["n_paths"],
            "trajectory_pool": mechanism["trajectory"]["n_paths"],
        },
    )

    n_pass = sum(check["result"] == "PASS" for check in checks)
    return {
        "artifact_id": "SF-IDENTITY-TAXONOMY-V6-TEST-2026-07-19-01",
        "inputs": {
            "taxonomy": snapshot["input_provenance"]["taxonomy"]["path"],
            "coding": snapshot["input_provenance"]["coding"]["path"],
            "adjudication": snapshot["input_provenance"]["adjudication"][
                "path"
            ],
            "sidecars": [name for name, _ in sidecars],
        },
        "input_provenance": snapshot["input_provenance"],
        "input_snapshot_sha256": snapshot["input_snapshot_sha256"],
        "platform": {"os": os.name, "python": sys.version.split()[0]},
        "topology_policy": "A(frozen) + strict-topology sensitivity dual-computed",
        "checks": checks,
        "occupancy": occupancy_block,
        "mutation_results": mutations,
        "summary": f"{n_pass}/{len(checks)} PASS",
        "verdict": "PASS" if n_pass == len(checks) else "FAIL",
    }


def encode_report(report):
    return (
        json.dumps(
            report,
            ensure_ascii=False,
            indent=1,
            allow_nan=False,
        )
        + "\n"
    ).encode("utf-8")


def write_report(report, output=Path(OUT)):
    output = Path(output)
    payload = encode_report(report)
    output.parent.mkdir(parents=True, exist_ok=True)
    descriptor, staging_name = tempfile.mkstemp(
        prefix=f".{output.name}.", suffix=".tmp", dir=output.parent
    )
    staging = Path(staging_name)
    descriptor_owned = True
    try:
        handle = os.fdopen(descriptor, "wb")
        descriptor_owned = False
        with handle:
            view = memoryview(payload)
            offset = 0
            while offset < len(view):
                written = handle.write(view[offset:])
                if written is None or written <= 0:
                    raise OSError("staged report write made no progress")
                offset += written
            handle.flush()
            os.fsync(handle.fileno())
        if staging.read_bytes() != payload:
            raise OSError("staged report bytes differ from deterministic payload")
        os.replace(staging, output)
    finally:
        if descriptor_owned:
            try:
                os.close(descriptor)
            except OSError:
                pass
        try:
            staging.unlink()
        except FileNotFoundError:
            pass


def _failure_report(error):
    return {
        "artifact_id": "SF-IDENTITY-TAXONOMY-V6-TEST-2026-07-19-01",
        "platform": {"os": os.name, "python": sys.version.split()[0]},
        "checks": [
            {
                "id": "INPUT",
                "check": "strict active input snapshot",
                "result": "FAIL",
                "detail": f"{type(error).__name__}: {error}",
            }
        ],
        "summary": "0/1 PASS",
        "verdict": "FAIL",
        "failure": {
            "type": type(error).__name__,
            "message": str(error),
        },
    }


def main(output=Path(OUT)):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    try:
        report = build_report()
    except Exception as error:
        report = _failure_report(error)
    write_report(report, output)
    if report["verdict"] != "PASS" or "occupancy" not in report:
        print(
            json.dumps(
                {
                    "summary": report["summary"],
                    "verdict": report["verdict"],
                    "platform": report["platform"],
                    "failure": report.get("failure"),
                },
                ensure_ascii=False,
                indent=1,
            )
        )
        return 1
    policy = report["occupancy"]["policy_A"]
    mechanism = policy[
        "strict_AND_reward_AND_pool_BY_selection_object(mechanism)"
    ]
    print(
        json.dumps(
            {
                "summary": report["summary"],
                "verdict": report["verdict"],
                "platform": report["platform"],
                "policy_A_key_numbers": {
                    "reward_guided": policy["is_reward_guided"]["n_paths"],
                    "rq_sys_compatible": policy[
                        "is_rq_sys_control_compatible"
                    ]["n_paths"],
                    "method_candidate": policy["is_project_method_candidate"][
                        "n_paths"
                    ],
                    "reward_guided_selection": policy[
                        "reward_guided_selection"
                    ]["n_paths"],
                    "trajectory_pool": mechanism["trajectory"]["n_paths"],
                },
            },
            ensure_ascii=False,
            indent=1,
        )
    )
    return 0 if report["verdict"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
