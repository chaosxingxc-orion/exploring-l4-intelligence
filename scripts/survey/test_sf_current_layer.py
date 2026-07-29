#!/usr/bin/env python3
"""Contract tests for the manifest-driven Stage-1A current survey layer."""

from __future__ import annotations

import hashlib
import importlib.util
import inspect
import json
import re
import copy
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
SURVEY_SCRIPTS = REPO / "scripts" / "survey"
CURRENT = REPO / "wiki" / "survey" / "current"
CURRENT_PACKAGE_REPORT_PATH = (
    "docs/checks/system-first-stage1a/context-v1/current-package-check.json"
)
WIKI_SYNC_INCIDENT_PATH = (
    "docs/checks/system-first-stage1a/context-v1/wiki-sync-dry-run-incident.json"
)


def load_module(name: str):
    path = SURVEY_SCRIPTS / f"{name}.py"
    if not path.is_file():
        raise AssertionError(f"implementation module missing: {path}")
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise AssertionError(f"cannot load implementation module: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def git_blob_oid(raw: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()


class CurrentManifestContractTests(unittest.TestCase):
    def setUp(self):
        self.manifest = load_module("sf_current_manifest")
        self.payloads = {
            spec.path: f"payload:{spec.path}\n".encode("utf-8")
            for spec in self.manifest.BASE_FILE_SPECS
        }
        anchor_path = "scripts/checks/ai_context_inventory.py"
        if anchor_path in self.payloads:
            self.payloads[anchor_path] = REPO.joinpath(*anchor_path.split("/")).read_bytes()
        self.head_payloads = {anchor_path: self.payloads[anchor_path]}
        for carrier_path in (
            "wiki/survey/current/protocol.md",
            "wiki/survey/current/status.md",
            CURRENT_PACKAGE_REPORT_PATH,
            WIKI_SYNC_INCIDENT_PATH,
        ):
            if carrier_path in self.payloads:
                self.payloads[carrier_path] = REPO.joinpath(
                    *carrier_path.split("/")
                ).read_bytes()
        self.blobs = {}
        self.base_index = {}
        for path, raw in self.payloads.items():
            blob = git_blob_oid(raw)
            self.blobs[blob] = raw
            self.base_index[path] = self.manifest.GitIndexEntry("100644", blob)

    def read_bytes(self, path: str) -> bytes:
        try:
            return self.payloads[path]
        except KeyError as error:
            raise FileNotFoundError(path) from error

    def read_blob(self, blob: str) -> bytes:
        return self.blobs[blob]

    def read_head_path(self, path: str) -> bytes:
        return self.head_payloads[path]

    def inventory(self, extra_paths=()):
        inventory = dict(self.base_index)
        for path in extra_paths:
            raw = self.payloads.get(path, f"placeholder:{path}\n".encode("utf-8"))
            blob = git_blob_oid(raw)
            self.blobs[blob] = raw
            inventory[path] = self.manifest.GitIndexEntry("100644", blob)
        return inventory

    def build(self, tracked=()):
        return self.manifest.build_manifest(
            self.read_bytes,
            self.inventory(tracked),
            self.read_blob,
            self.read_head_path,
        )

    def audit_paths(self):
        paths = set()
        for spec in self.manifest._AUDIT_FILE_SPECS:
            raw = REPO.joinpath(*spec.path.split("/")).read_bytes()
            self.payloads[spec.path] = raw
            paths.add(spec.path)
        return paths

    def test_manifest_entries_have_exact_contract(self):
        document = self.build()
        entries = document["files"]
        self.assertTrue(entries)
        for entry in entries:
            self.assertEqual(
                {"role", "path", "sha256", "mutability", "load_policy"},
                set(entry),
            )
            self.assertRegex(entry["sha256"], r"^[0-9a-f]{64}$")
            self.assertNotEqual("wiki/survey/current/manifest.json", entry["path"])

    def test_manifest_has_no_retired_dual_platform_checker_entry(self):
        document = self.build()
        entries = document["files"]
        self.assertFalse(
            any(entry["role"] == "dual_platform_aggregate_checker" for entry in entries)
        )
        self.assertFalse(
            any(entry["path"] == "scripts/survey/sf_dual_platform_check.py" for entry in entries)
        )

    def test_stage1b_release_products_are_current_and_release_bound(self):
        document = self.build()
        by_path = {entry["path"]: entry for entry in document["files"]}
        expected = {
            "wiki/survey/current/data/stage1b-speech-omni-prior-coverage-v1.json",
            "wiki/survey/current/data/stage1b-known-prior-reconciliation-v1.json",
            "wiki/survey/current/data/stage1b-eligible-bundle-reconciliation-v1.json",
            "wiki/survey/current/data/stage1b-speech-direct-prior-supplement-v3.json",
            "wiki/survey/current/data/stage1b-direct-control-basis-v2.json",
            "wiki/survey/current/stage1b-transition-reference-appendix.md",
            "wiki/survey/current/tables/stage1b-mapping-release.md",
            "wiki/survey/current/tables/stage1c-eligible-inputs.md",
            "docs/stage1b-v5-gate-assets.lock.json",
            "docs/checks/stage1b-closeout/2026-07-23-v5/speechrl-data-layered-inventory-python.json",
            "docs/checks/stage1b-closeout/2026-07-23-v5/speechrl-data-layered-inventory-powershell.json",
            "docs/checks/stage1b-closeout/2026-07-23-v5/speechrl-data-content-accounting.json",
            "docs/checks/stage1b-closeout/2026-07-23-v5/release-manifest.json",
        }
        self.assertTrue(expected <= set(by_path))
        self.assertTrue(expected <= set(document["release_bound_artifacts"]))

    def test_integration_evidence_has_exact_targeted_routes(self):
        document = self.build()
        by_path = {entry["path"]: entry for entry in document["files"]}
        expected = {
            WIKI_SYNC_INCIDENT_PATH: (
                "wiki_sync_dry_run_incident",
                "immutable-after-first-commit",
            ),
        }
        self.assertNotIn(
            CURRENT_PACKAGE_REPORT_PATH,
            by_path,
            "the package report must not be an input to its own command graph",
        )
        for path, (role, mutability) in expected.items():
            with self.subTest(path=path):
                self.assertIn(path, by_path)
                self.assertEqual(
                    (role, mutability, "targeted"),
                    (
                        by_path[path]["role"],
                        by_path[path]["mutability"],
                        by_path[path]["load_policy"],
                    ),
                )
                self.assertNotIn(path, document["release_bound_artifacts"])
                self.assertNotIn(path, document["prose_scan_paths"])

    def _integration_spec(self, path, role, mutability):
        return self.manifest.FileSpec(role, path, mutability, "targeted")

    def test_integration_evidence_uses_staged_blob_as_hash_authority(self):
        specs = (
            self._integration_spec(
                WIKI_SYNC_INCIDENT_PATH,
                "wiki_sync_dry_run_incident",
                "immutable-after-first-commit",
            ),
        )
        for spec in specs:
            raw = REPO.joinpath(*spec.path.split("/")).read_bytes()
            blob = git_blob_oid(raw)
            index = {spec.path: self.manifest.GitIndexEntry("100644", blob)}
            for label, worktree_reader in (
                (
                    "missing-worktree",
                    lambda _path: (_ for _ in ()).throw(FileNotFoundError(spec.path)),
                ),
                ("crlf-or-dirty-worktree", lambda _path: raw + b" "),
            ):
                with self.subTest(path=spec.path, case=label):
                    entry = self.manifest._file_entry(
                        spec,
                        worktree_reader,
                        index,
                        lambda _blob: raw,
                    )
                    self.assertEqual(hashlib.sha256(raw).hexdigest(), entry["sha256"])

    def test_integration_evidence_rejects_wrong_schema(self):
        specs = (
            (
                self._integration_spec(
                    WIKI_SYNC_INCIDENT_PATH,
                    "wiki_sync_dry_run_incident",
                    "immutable-after-first-commit",
                ),
                "wiki-sync-dry-run-incident-v1",
            ),
        )
        for spec, expected_schema in specs:
            document = json.loads(REPO.joinpath(*spec.path.split("/")).read_bytes())
            self.assertEqual(expected_schema, document["schema"])
            document["schema"] = "wrong-schema"
            raw = (json.dumps(document, separators=(",", ":")) + "\n").encode("utf-8")
            blob = git_blob_oid(raw)
            with self.subTest(path=spec.path):
                with self.assertRaisesRegex(
                    self.manifest.CurrentManifestError,
                    "integration-evidence-schema-invalid",
                ):
                    self.manifest._file_entry(
                        spec,
                        lambda _path: raw,
                        {spec.path: self.manifest.GitIndexEntry("100644", blob)},
                        lambda _blob: raw,
                    )

    def test_manifest_expands_exactly_eight_sidecars(self):
        sidecars = [
            entry
            for entry in self.build()["files"]
            if entry["role"].startswith("schema_v3_sidecar:")
        ]
        self.assertEqual(8, len(sidecars))
        self.assertEqual(sorted(entry["path"] for entry in sidecars), [
            entry["path"] for entry in sidecars
        ])

    def test_release_and_prose_arrays_are_current_only(self):
        document = self.build()
        self.assertEqual(
            [
                "wiki/survey/current/data/stage1b-speech-omni-prior-coverage-v1.json",
                "wiki/survey/current/data/stage1b-known-prior-reconciliation-v1.json",
                "wiki/survey/current/data/stage1b-eligible-bundle-reconciliation-v1.json",
                "wiki/survey/current/data/stage1b-speech-direct-prior-supplement-v3.json",
                "wiki/survey/current/data/stage1b-direct-control-basis-v2.json",
                "wiki/survey/current/stage1b-transition-reference-appendix.md",
                "wiki/survey/current/tables/stage1b-mapping-release.md",
                "wiki/survey/current/tables/stage1c-eligible-inputs.md",
                "docs/stage1b-v5-gate-assets.lock.json",
                "docs/checks/stage1b-closeout/2026-07-23-v5/speechrl-data-layered-inventory-python.json",
                "docs/checks/stage1b-closeout/2026-07-23-v5/speechrl-data-layered-inventory-powershell.json",
                "docs/checks/stage1b-closeout/2026-07-23-v5/speechrl-data-content-accounting.json",
                "docs/checks/stage1b-closeout/2026-07-23-v5/release-manifest.json",
            ],
            document["release_bound_artifacts"],
        )
        self.assertEqual(
            [
                "wiki/survey/current/README.md",
                "wiki/survey/current/protocol.md",
                "wiki/survey/current/status.md",
                "wiki/survey/current/research-directions.md",
                "wiki/survey/current/stage1b-transition-reference-appendix.md",
                "wiki/survey/current/tables/stage1b-mapping-release.md",
                "wiki/survey/current/tables/stage1c-eligible-inputs.md",
                "wiki/survey/current/tables/stage1c-common-rubric-comparison.md",
            ],
            document["prose_scan_paths"],
        )
        for path in (
            document["release_bound_artifacts"] + document["prose_scan_paths"]
        ):
            self.assertTrue(
                path.startswith("wiki/survey/current/")
                or path.startswith("docs/checks/stage1b-closeout/2026-07-23-v5/")
                or path == "docs/stage1b-v5-gate-assets.lock.json"
            )
            self.assertNotRegex(path, r"amendment|review|response")

    def test_audit_contract_lifecycle_is_absent_complete_or_fail_closed(self):
        index = self.manifest.AUDIT_CAMPAIGN_INDEX_PATH
        correction = self.manifest.ACTIVE_REVIEW_TRANSACTION
        before = self.build()
        self.assertNotIn(index, [entry["path"] for entry in before["files"]])
        self.assertNotIn(correction, before["release_bound_artifacts"])

        audit_paths = self.audit_paths()
        for missing in audit_paths:
            with self.assertRaisesRegex(
                self.manifest.CurrentManifestError,
                "audit-activation-incomplete",
            ):
                self.build(audit_paths - {missing})

        after = self.build(audit_paths)
        paths = [entry["path"] for entry in after["files"]]
        self.assertIn(index, paths)
        self.assertIn(correction, paths)
        self.assertIn(correction, after["release_bound_artifacts"])
        self.assertIn(correction, after["prose_scan_paths"])

    def test_manifest_render_is_deterministic_canonical_and_timestamp_free(self):
        inventory = self.inventory()
        first = self.manifest.render_manifest(
            self.read_bytes, inventory, self.read_blob, self.read_head_path
        )
        second = self.manifest.render_manifest(
            self.read_bytes, inventory, self.read_blob, self.read_head_path
        )
        self.assertEqual(first, second)
        self.assertTrue(first.endswith(b"\n"))
        self.assertNotIn(b"generated_at", first)
        parsed = json.loads(first)
        self.assertEqual(parsed, self.build())
        self.assertEqual(first, (
            json.dumps(parsed, ensure_ascii=False, indent=2, allow_nan=False)
            + "\n"
        ).encode("utf-8"))

    def test_git_index_inventory_requires_stage_zero_entries(self):
        self.assertTrue(
            hasattr(self.manifest, "_parse_git_index"),
            "Git index parser is missing",
        )
        good = (
            b"100644 0123456789012345678901234567890123456789 0\t"
            b"wiki/audit/system-first-stage1a/INDEX.md\0"
        )
        self.assertEqual(
            {
                "wiki/audit/system-first-stage1a/INDEX.md":
                    self.manifest.GitIndexEntry(
                        "100644", "0123456789012345678901234567890123456789"
                    )
            },
            self.manifest._parse_git_index(good),
        )
        bad = good.replace(b" 0\t", b" 1\t")
        with self.assertRaisesRegex(
            self.manifest.CurrentManifestError, "non-stage-0"
        ):
            self.manifest._parse_git_index(bad)

    def test_windows_worktree_gitdir_pointer_translates_for_wsl(self):
        self.assertTrue(
            hasattr(self.manifest, "_resolved_gitdir"),
            "worktree gitdir resolver is missing",
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            dot_git = Path(temp_dir) / ".git"
            dot_git.write_text(
                "gitdir: D:/repo/.git/worktrees/review\n", encoding="utf-8"
            )
            self.assertEqual(
                Path("/mnt/d/repo/.git/worktrees/review"),
                self.manifest._resolved_gitdir(dot_git, platform="posix"),
            )
            self.assertEqual(
                Path("D:/repo/.git/worktrees/review"),
                self.manifest._resolved_gitdir(dot_git, platform="nt"),
            )


class ManifestGitBindingContractTests(unittest.TestCase):
    def setUp(self):
        self.manifest = load_module("sf_current_manifest")
        signature = inspect.signature(self.manifest.build_manifest)
        self.assertIn(
            "read_blob",
            signature.parameters,
            "manifest builder lacks staged-blob reader",
        )
        self.assertIn(
            "read_head_path",
            signature.parameters,
            "manifest builder lacks HEAD-path reader for anchor lineage",
        )
        self.payloads = {
            spec.path: f"payload:{spec.path}\n".encode("utf-8")
            for spec in self.manifest.BASE_FILE_SPECS
        }
        anchor_path = "scripts/checks/ai_context_inventory.py"
        if anchor_path in self.payloads:
            self.payloads[anchor_path] = REPO.joinpath(*anchor_path.split("/")).read_bytes()
        self.head_payloads = {anchor_path: self.payloads[anchor_path]}
        self.head_reads = []
        for carrier_path in (
            "wiki/survey/current/protocol.md",
            "wiki/survey/current/status.md",
            CURRENT_PACKAGE_REPORT_PATH,
            WIKI_SYNC_INCIDENT_PATH,
        ):
            if carrier_path in self.payloads:
                self.payloads[carrier_path] = REPO.joinpath(
                    *carrier_path.split("/")
                ).read_bytes()
        self.blobs = {}
        self.index = {}
        for path, raw in self.payloads.items():
            blob = git_blob_oid(raw)
            self.blobs[blob] = raw
            self.index[path] = self.manifest.GitIndexEntry("100644", blob)

    def read_bytes(self, path):
        return self.payloads[path]

    def read_blob(self, blob):
        return self.blobs[blob]

    def read_head_path(self, path):
        self.head_reads.append(path)
        return self.head_payloads[path]

    def build(self, index=None):
        return self.manifest.build_manifest(
            self.read_bytes,
            self.index if index is None else index,
            self.read_blob,
            self.read_head_path,
        )

    def add_audit_contract(self, index):
        for spec in self.manifest._AUDIT_FILE_SPECS:
            raw = REPO.joinpath(*spec.path.split("/")).read_bytes()
            self.payloads[spec.path] = raw
            blob = git_blob_oid(raw)
            self.blobs[blob] = raw
            index[spec.path] = self.manifest.GitIndexEntry("100644", blob)

    def stage_raw(self, index, path, raw):
        self.payloads[path] = raw
        staged_blob = git_blob_oid(raw)
        self.blobs[staged_blob] = raw
        index[path] = self.manifest.GitIndexEntry("100644", staged_blob)

    def anchor_raw(self, count, prefix):
        raw = self.head_payloads[self.manifest.CAMPAIGN_SEMANTIC_ANCHOR_PATH]
        text = raw.decode("utf-8")
        text = re.sub(
            r"^CAMPAIGN_INDEX_BASELINE_COUNT = \d+$",
            f"CAMPAIGN_INDEX_BASELINE_COUNT = {count}",
            text,
            flags=re.MULTILINE,
        )
        text = re.sub(
            r'^CAMPAIGN_INDEX_BASELINE_PREFIX_SHA256 = "[0-9a-f]{64}"$',
            f'CAMPAIGN_INDEX_BASELINE_PREFIX_SHA256 = "{prefix}"',
            text,
            flags=re.MULTILINE,
        )
        return text.encode("utf-8")

    def test_every_base_entry_must_be_tracked(self):
        with self.assertRaisesRegex(
            self.manifest.CurrentManifestError, "manifest-input-untracked"
        ):
            self.build({})

    def test_wrong_mode_and_malformed_blob_are_rejected(self):
        self.assertTrue(
            hasattr(self.manifest, "_validate_index_entry"),
            "injected Git index entries are not validated",
        )
        path = next(iter(self.index))
        wrong_mode = dict(self.index)
        wrong_mode[path] = self.manifest.GitIndexEntry(
            "120000", wrong_mode[path].blob
        )
        with self.assertRaisesRegex(
            self.manifest.CurrentManifestError, "not a regular Git mode"
        ):
            self.build(wrong_mode)

        wrong_blob = dict(self.index)
        wrong_blob[path] = self.manifest.GitIndexEntry("100644", "not-a-blob")
        with self.assertRaisesRegex(
            self.manifest.CurrentManifestError, "malformed blob"
        ):
            self.build(wrong_blob)

        malformed = (
            b"100644 not-a-blob 0\t"
            + path.encode("utf-8")
            + b"\0"
        )
        with self.assertRaisesRegex(
            self.manifest.CurrentManifestError, "malformed blob"
        ):
            self.manifest._parse_git_index(malformed)

    def test_staged_blob_remains_authority_when_worktree_differs(self):
        before = self.build()
        path = next(iter(self.index))
        self.payloads[path] += b"changed-after-stage\n"
        self.assertEqual(before, self.build())

    def test_crlf_worktree_variant_preserves_staged_lf_identity(self):
        before = self.build()
        path = next(
            path for path, raw in self.payloads.items() if b"\n" in raw
        )
        self.payloads[path] = self.payloads[path].replace(b"\n", b"\r\n")
        self.assertEqual(before, self.build())

    def test_audit_contract_requires_complete_freshly_staged_bytes(self):
        index_path = self.manifest.AUDIT_CAMPAIGN_INDEX_PATH
        correction = self.manifest.ACTIVE_REVIEW_TRANSACTION
        index = dict(self.index)
        raw = REPO.joinpath(*index_path.split("/")).read_bytes()
        blob = git_blob_oid(raw)
        self.payloads[index_path] = raw
        self.blobs[blob] = raw
        index[index_path] = self.manifest.GitIndexEntry("100644", blob)
        with self.assertRaisesRegex(
            self.manifest.CurrentManifestError, "audit-activation-incomplete"
        ):
            self.build(index)

        self.add_audit_contract(index)
        correction_raw = self.blobs[index[correction].blob]
        correction_blob = index[correction].blob
        self.payloads[correction] = correction_raw + b"edited-after-stage\n"
        document = self.build(index)
        correction_entry = next(
            entry for entry in document["files"] if entry["path"] == correction
        )
        self.assertEqual(
            hashlib.sha256(correction_raw).hexdigest(),
            correction_entry["sha256"],
        )
        self.assertEqual(correction_blob, index[correction].blob)

    def test_staged_campaign_index_must_match_staged_semantic_contract(self):
        index = dict(self.index)
        self.add_audit_contract(index)
        index_path = self.manifest.AUDIT_CAMPAIGN_INDEX_PATH
        stale = self.payloads[index_path] + b"stale\n"
        stale_blob = git_blob_oid(stale)
        self.payloads[index_path] = stale
        self.blobs[stale_blob] = stale
        index[index_path] = self.manifest.GitIndexEntry("100644", stale_blob)
        with self.assertRaisesRegex(
            self.manifest.CurrentManifestError, "campaign-audit-index-stale"
        ):
            self.build(index)

    def test_campaign_semantic_anchor_is_unique_literal_and_stage_bound(self):
        anchor_path = "scripts/checks/ai_context_inventory.py"
        self.assertIn(anchor_path, self.index)
        raw = self.payloads[anchor_path]
        count, prefix = self.manifest._campaign_semantic_anchor_from_source(raw)
        self.assertEqual(44, count)
        self.assertRegex(prefix, r"^[0-9a-f]{64}$")

        duplicate = raw + f"\nCAMPAIGN_INDEX_BASELINE_COUNT = {count}\n".encode()
        with self.assertRaisesRegex(
            self.manifest.CurrentManifestError, "campaign-anchor-invalid"
        ):
            self.manifest._campaign_semantic_anchor_from_source(duplicate)

        index = dict(self.index)
        self.add_audit_contract(index)
        tampered = raw.replace(prefix.encode("ascii"), b"0" * 64)
        self.assertNotEqual(raw, tampered)
        tampered_blob = git_blob_oid(tampered)
        self.payloads[anchor_path] = tampered
        self.blobs[tampered_blob] = tampered
        index[anchor_path] = self.manifest.GitIndexEntry("100644", tampered_blob)
        with self.assertRaisesRegex(
            self.manifest.CurrentManifestError, "same-count anchor restamp"
        ):
            self.build(index)
        self.assertIn(anchor_path, self.head_reads)

    def test_gate_accepts_one_standalone_receipt_with_atomic_anchor_growth(self):
        index = dict(self.index)
        self.add_audit_contract(index)
        registry_path = "wiki/survey/sf-audit-artifact-registry.json"
        contract_path = self.manifest.campaign_audit_index.CONTRACT_PATH.relative_to(
            REPO
        ).as_posix()
        index_path = self.manifest.AUDIT_CAMPAIGN_INDEX_PATH
        registry = json.loads(self.payloads[registry_path])
        contract = json.loads(self.payloads[contract_path])

        receipt_path = (
            "wiki/audit/system-first-stage1a/epoch-16/consolidation-receipt.json"
        )
        receipt_raw = b'{"campaign":"system-first-stage1a","epoch":13}\n'
        receipt_blob = git_blob_oid(receipt_raw)
        registry["artifacts"].append(
            {"path": receipt_path, "git_blob": receipt_blob}
        )
        contract["rounds"].append(
            {
                "round": 16,
                "verdict": "PENDING_INDEPENDENT_REREVIEW",
                "disposition": "NON_ACTIVE_PREREQUISITE",
                "supersession": {
                    "mode": "current-carrier",
                    "target": "wiki/survey/current/status.md",
                    "target_current_carrier": "wiki/survey/current/status.md",
                    "target_current_carrier_section": "Current Survey Status",
                    "transfer_rule": "same-carrier-section",
                },
                "current_carrier": "wiki/survey/current/status.md",
                "current_carrier_section": "Current Survey Status",
                "artifacts": [
                    {
                        "path": receipt_path,
                        "git_blob": receipt_blob,
                        "type": "consolidation-receipt",
                    }
                ],
            }
        )
        count = len(
            self.manifest.campaign_audit_index.semantic_entries(contract["rounds"])
        )
        prefix = self.manifest.campaign_audit_index.semantic_prefix_sha256(
            contract["rounds"], count
        )
        registry_raw = (
            json.dumps(registry, ensure_ascii=False, indent=2) + "\n"
        ).encode("utf-8")
        contract_raw = (
            json.dumps(contract, ensure_ascii=False, indent=2) + "\n"
        ).encode("utf-8")
        index_raw = self.manifest.campaign_audit_index.render_index(contract)
        self.stage_raw(index, registry_path, registry_raw)
        self.stage_raw(index, contract_path, contract_raw)
        self.stage_raw(index, index_path, index_raw)
        self.stage_raw(
            index,
            self.manifest.CAMPAIGN_SEMANTIC_ANCHOR_PATH,
            self.anchor_raw(count, prefix),
        )
        self.stage_raw(index, receipt_path, receipt_raw)

        document = self.build(index)
        self.assertEqual(
            12,
            self.manifest.campaign_audit_index.derived_current_round(
                contract["rounds"]
            ),
        )
        self.assertIn(
            self.manifest.CAMPAIGN_SEMANTIC_ANCHOR_PATH,
            [entry["path"] for entry in document["files"]],
        )

    def assert_gate_rejects_post_head_opaque_type(
        self,
        *,
        artifact_type,
        disposition,
        basename,
    ):
        index = dict(self.index)
        self.add_audit_contract(index)
        registry_path = "wiki/survey/sf-audit-artifact-registry.json"
        contract_path = self.manifest.campaign_audit_index.CONTRACT_PATH.relative_to(
            REPO
        ).as_posix()
        index_path = self.manifest.AUDIT_CAMPAIGN_INDEX_PATH
        registry = json.loads(self.payloads[registry_path])
        contract = json.loads(self.payloads[contract_path])

        opaque_path = f"wiki/audit/system-first-stage1a/round-16/{basename}"
        opaque_raw = f"opaque {artifact_type}\n".encode("utf-8")
        opaque_blob = git_blob_oid(opaque_raw)
        registry["artifacts"].append(
            {"path": opaque_path, "git_blob": opaque_blob}
        )
        contract["rounds"].append(
            {
                "round": 16,
                "verdict": "PENDING_INDEPENDENT_REREVIEW",
                "disposition": disposition,
                "supersession": {
                    "mode": "current-carrier",
                    "target": "wiki/survey/current/status.md",
                    "target_current_carrier": "wiki/survey/current/status.md",
                    "target_current_carrier_section": "Current Survey Status",
                    "transfer_rule": "same-carrier-section",
                },
                "current_carrier": "wiki/survey/current/status.md",
                "current_carrier_section": "Current Survey Status",
                "artifacts": [
                    {
                        "path": opaque_path,
                        "git_blob": opaque_blob,
                        "type": artifact_type,
                    }
                ],
            }
        )
        count = len(
            self.manifest.campaign_audit_index.semantic_entries(contract["rounds"])
        )
        prefix = self.manifest.campaign_audit_index.semantic_prefix_sha256(
            contract["rounds"], count
        )
        self.stage_raw(
            index,
            registry_path,
            (json.dumps(registry, ensure_ascii=False, indent=2) + "\n").encode(
                "utf-8"
            ),
        )
        self.stage_raw(
            index,
            contract_path,
            (json.dumps(contract, ensure_ascii=False, indent=2) + "\n").encode(
                "utf-8"
            ),
        )
        self.stage_raw(
            index,
            index_path,
            self.manifest.campaign_audit_index.render_index(contract),
        )
        self.stage_raw(
            index,
            self.manifest.CAMPAIGN_SEMANTIC_ANCHOR_PATH,
            self.anchor_raw(count, prefix),
        )
        self.stage_raw(index, opaque_path, opaque_raw)

        with self.assertRaisesRegex(
            self.manifest.CurrentManifestError, "path/type"
        ):
            self.build(index)

    def test_gate_rejects_post_head_non_active_opaque_active_type(self):
        self.assert_gate_rejects_post_head_opaque_type(
            artifact_type="amendment",
            disposition="HISTORICAL_COLD",
            basename="opaque-note.md",
        )

    def test_gate_rejects_post_head_opaque_receipt_type(self):
        self.assert_gate_rejects_post_head_opaque_type(
            artifact_type="consolidation-receipt",
            disposition="NON_ACTIVE_PREREQUISITE",
            basename="receipt.json",
        )

    def test_coordinated_allowed_semantic_restamps_fail_against_head_anchor(self):
        raw = self.head_payloads[self.manifest.CAMPAIGN_SEMANTIC_ANCHOR_PATH]
        head_count, head_prefix = self.manifest._campaign_semantic_anchor_from_source(raw)
        contract = json.loads(
            REPO.joinpath(
                *self.manifest.campaign_audit_index.CONTRACT_PATH.relative_to(REPO).parts
            ).read_bytes()
        )
        mutations = {}

        verdict = copy.deepcopy(contract)
        verdict["rounds"][0]["verdict"] = "WITHHOLD_STAGE1B"
        mutations["allowed-value"] = verdict

        artifact_type = copy.deepcopy(contract)
        artifact_type["rounds"][0]["artifacts"][0]["type"] = "review"
        mutations["allowed-type"] = artifact_type

        artifact_round = copy.deepcopy(contract)
        first = artifact_round["rounds"][0]["artifacts"][0]
        second = artifact_round["rounds"][1]["artifacts"][0]
        artifact_round["rounds"][0]["artifacts"][0] = second
        artifact_round["rounds"][1]["artifacts"][0] = first
        mutations["allowed-round"] = artifact_round

        for label, changed in mutations.items():
            staged_prefix = self.manifest.campaign_audit_index.semantic_prefix_sha256(
                changed["rounds"], head_count
            )
            with self.subTest(label=label):
                with self.assertRaisesRegex(
                    self.manifest.CurrentManifestError,
                    "same-count anchor restamp",
                ):
                    self.manifest._validate_campaign_anchor_lineage(
                        changed["rounds"],
                        head_count,
                        head_prefix,
                        head_count,
                        staged_prefix,
                    )


class TrustedCurrentPathContractTests(unittest.TestCase):
    def setUp(self):
        path = SURVEY_SCRIPTS / "sf_current_path_contract.py"
        self.assertTrue(path.is_file(), f"trusted path helper missing: {path}")
        self.paths = load_module("sf_current_path_contract")
        self.manifest = load_module("sf_current_manifest")

    def symlink_or_skip(self, target: Path, link: Path, *, directory=False):
        try:
            link.symlink_to(target, target_is_directory=directory)
        except OSError as error:
            self.skipTest(f"symlink unavailable: {error}")

    def test_manifest_output_rejects_leaf_and_ancestor_symlinks(self):
        cases = (
            (
                "wiki/survey/current/manifest.json",
                self.manifest._resolve_output_path,
            ),
        )
        for relative, resolver in cases:
            with self.subTest(relative=relative), tempfile.TemporaryDirectory() as temp_dir:
                repo = Path(temp_dir) / "repo"
                outside = Path(temp_dir) / "outside"
                outside.mkdir()
                outside_file = outside / "output"
                outside_file.write_bytes(b"outside\n")
                leaf = repo.joinpath(*relative.split("/"))
                leaf.parent.mkdir(parents=True)
                self.symlink_or_skip(outside_file, leaf)
                for allow_missing in (False, True):
                    with self.assertRaises(self.paths.TrustedCurrentPathError):
                        resolver(
                            repo, leaf, allow_missing_leaf=allow_missing
                        )

                leaf.unlink()
                current = repo / "wiki/survey/current"
                shutil.rmtree(current)
                current_target = outside / "current"
                current_target.mkdir()
                self.symlink_or_skip(current_target, current, directory=True)
                for allow_missing in (False, True):
                    with self.assertRaises(self.paths.TrustedCurrentPathError):
                        resolver(
                            repo, repo / relative,
                            allow_missing_leaf=allow_missing,
                        )

    def test_write_allows_only_a_missing_leaf_under_safe_existing_parents(self):
        relative = "wiki/survey/current/manifest.json"
        with tempfile.TemporaryDirectory() as temp_dir:
            repo = Path(temp_dir) / "repo"
            target = repo.joinpath(*relative.split("/"))
            target.parent.mkdir(parents=True)
            self.assertEqual(
                target,
                self.paths.resolve_fixed_output(
                    repo, target, relative, allow_missing_leaf=True
                ),
            )
            with self.assertRaises(self.paths.TrustedCurrentPathError):
                self.paths.resolve_fixed_output(
                    repo, target, relative, allow_missing_leaf=False
                )


class RouterContentContractTests(unittest.TestCase):
    def test_readme_is_short_and_contains_only_required_routing_content(self):
        path = CURRENT / "README.md"
        self.assertTrue(path.is_file(), f"missing router: {path}")
        raw = path.read_bytes()
        text = raw.decode("utf-8")
        self.assertLessEqual(len(raw), 4096)
        for required in (
            "Stage‑1C research-direction confirmation",
            "STAGE1C_R1_SUNSET_OWNER_CONFIRMED_20260729_R2R9_UNVERIFIED_OWNER_COWORK_PENDING",
            "Qwen3-Omni-30B",
            "capability-first candidate",
            "direction-viability criterion (2026-07-29",
            "OWNER_UNVERIFIED",
            "datasets and metrics are",
            "status.md",
            "research-directions.md",
            "stage1c-eligible-inputs.md",
            "protocol.md",
            "manifest.json",
            "targeted",
            "wiki/audit/system-first-stage1b/INDEX.md",
            "H5 remains withheld and non-load-bearing",
            "Historical proposals, reviews, responses and amendments are cold audit",
        ):
            self.assertIn(required, text)
        self.assertNotRegex(text, r"sf-protocol-amendment-\d+|gate-s1-v\d+-response")
        self.assertLessEqual(len(text.splitlines()), 32)

    def test_status_is_short_and_preserves_stage1c_execution_boundary(self):
        path = CURRENT / "status.md"
        self.assertTrue(path.is_file(), f"missing status: {path}")
        raw = path.read_bytes()
        text = raw.decode("utf-8")
        self.assertLessEqual(len(raw), 4096)
        for required in (
            "Stage‑1C research-direction confirmation",
            "STAGE1C_R1_SUNSET_OWNER_CONFIRMED_20260729_R2R9_UNVERIFIED_OWNER_COWORK_PENDING",
            "Qwen3-Omni-30B",
            "general ASR",
            "analysis/synthesis only",
            "reference papers",
            "NO_GO_AS_STANDALONE_DIRECTION__SUNSET_BEFORE_STAGE2",
            "owner-confirmed (2026-07-29",
            "OWNER_UNVERIFIED",
            "AudioRAG/Omni-DeepSearch",
            "R5+R6+R8 Stage‑2A",
            "no model/API execution, metric run, reproduction or prototype occurred",
            "model/API calls",
            "RETIRED_WITHOUT_DISTRIBUTION_OR_INDEPENDENT_ACCEPTANCE",
            "H5 remains withheld and non-load-bearing",
            "Stage‑2A/2B execution",
            "Next action",
        ):
            self.assertIn(required, text)
        self.assertNotRegex(text, r"Stage-1B.*(?:unstarted|unauthorized)")
        self.assertNotIn("execution_authorized: false", text)
        self.assertLessEqual(len(text.splitlines()), 40)


if __name__ == "__main__":
    unittest.main(verbosity=2)
