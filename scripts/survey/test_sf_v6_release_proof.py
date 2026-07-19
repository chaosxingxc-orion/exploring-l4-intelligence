#!/usr/bin/env python3
"""Adversarial tests binding the v6 proof to exact active input bytes."""
from __future__ import annotations

import copy
import hashlib
import importlib
import io
import json
import shutil
import sys
import tarfile
import tempfile
import unittest
from pathlib import Path
from unittest import mock


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))

import sf_identity_taxonomy_v6_test as harness  # noqa: E402


class StrictJsonContractTest(unittest.TestCase):
    def helper(self):
        return importlib.import_module("sf_json_contract")

    def test_strict_json_rejects_duplicate_nan_trailing_and_invalid_utf8(self):
        contract = self.helper()
        malformed = (
            b'{"x": 1, "x": 2}',
            b'{"x": NaN}',
            b'{} trailing',
            b'{"x": "\xff"}',
        )
        for raw in malformed:
            with self.subTest(raw=raw), self.assertRaises(
                contract.JsonContractError
            ):
                contract.loads(raw, "fixture")

    def test_jsonl_is_strict_per_nonblank_line(self):
        contract = self.helper()
        with self.assertRaises(contract.JsonContractError):
            contract.loads_jsonl(b'{"x": 1}\n{"x": NaN}\n', "ledger")

    def test_harness_ledger_loader_rejects_non_strict_jsonl(self):
        survey = REPO / "wiki/survey"
        with tempfile.TemporaryDirectory(dir=survey) as temporary:
            path = Path(temporary) / "ledger.jsonl"
            path.write_bytes(b'{"id":"x","id":"y"}\n')
            relative = path.relative_to(REPO).as_posix()
            self.assertIsNone(harness.ledger_index(relative))


class TaxonomyBindingTest(unittest.TestCase):
    def setUp(self):
        contract = importlib.import_module("sf_json_contract")
        self.taxonomy_contract = importlib.import_module("sf_taxonomy_v6_contract")
        self.v5 = contract.read(REPO / "wiki/survey/2026-07-19-sf-identity-taxonomy-v5.json")[0]
        self.v6 = contract.read(REPO / "wiki/survey/current/data/identity-taxonomy-v6.json")[0]

    def test_real_taxonomies_pass_the_reusable_contract(self):
        self.assertEqual(
            self.taxonomy_contract.validate_taxonomy_v6(self.v5, self.v6), []
        )

    def test_semantic_claim_and_extra_rule_mutations_are_rejected(self):
        mutations = []
        relations = copy.deepcopy(self.v6)
        relations["allowed_relations"] = {}
        mutations.append(relations)
        claims = copy.deepcopy(self.v6)
        claims["required_evidence_contract"]["claims"] = {}
        mutations.append(claims)
        extra = copy.deepcopy(self.v6)
        extra["unreviewed_release_rule"] = "accept anything"
        mutations.append(extra)
        for mutated in mutations:
            with self.subTest(keys=set(mutated) - set(self.v6)):
                self.assertTrue(
                    self.taxonomy_contract.validate_taxonomy_v6(self.v5, mutated)
                )

    def test_build_report_turns_taxonomy_mutations_red(self):
        mutations = []
        relations = copy.deepcopy(self.v6)
        relations["allowed_relations"] = {}
        mutations.append(relations)
        claims = copy.deepcopy(self.v6)
        claims["required_evidence_contract"]["claims"] = {}
        mutations.append(claims)
        extra = copy.deepcopy(self.v6)
        extra["unreviewed_release_rule"] = "accept anything"
        mutations.append(extra)
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "taxonomy.json"
            for mutated in mutations:
                path.write_text(
                    json.dumps(mutated, ensure_ascii=False, indent=1) + "\n",
                    encoding="utf-8",
                    newline="\n",
                )
                with mock.patch.object(harness, "TAX", str(path)):
                    self.assertEqual(harness.build_report()["verdict"], "FAIL")


class ReleaseInventoryTest(unittest.TestCase):
    def module(self):
        return importlib.import_module("sf_schema_v3_release_contract")

    def copy_release(self, root):
        source = REPO / "wiki/survey/current/data/schema-v3/sidecars"
        destination = root / "sidecars"
        shutil.copytree(source, destination)
        adjudication = root / "schema-v3-adjudication.json"
        shutil.copy2(
            REPO / "wiki/survey/current/data/schema-v3-adjudication.json",
            adjudication,
        )
        return destination, adjudication

    def test_real_release_has_exact_hash_work_and_row_inventory(self):
        release = self.module()
        snapshot = release.load_active_release(
            REPO,
            REPO / "wiki/survey/current/data/schema-v3/sidecars",
            REPO / "wiki/survey/current/data/schema-v3-adjudication.json",
        )
        self.assertEqual(tuple(name for name, _, _ in snapshot.sidecars), release.FINAL_SIDECAR_NAMES)
        self.assertEqual(len(snapshot.method_path_ids), 11)

    def test_ninth_missing_modified_duplicate_work_and_row_are_rejected(self):
        release = self.module()
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            sidecars, adjudication = self.copy_release(root)
            ninth = sidecars / "ninth.sidecar.json"
            ninth.write_bytes((sidecars / release.FINAL_SIDECAR_NAMES[0]).read_bytes())
            with self.assertRaises(release.ReleaseContractError):
                release.load_active_release(REPO, sidecars, adjudication)
            ninth.unlink()

            missing = sidecars / release.FINAL_SIDECAR_NAMES[0]
            saved = missing.read_bytes()
            missing.unlink()
            with self.assertRaises(release.ReleaseContractError):
                release.load_active_release(REPO, sidecars, adjudication)
            missing.write_bytes(saved)

            for label, mutate in (
                ("modified", lambda doc: doc.update(note="drift")),
                (
                    "duplicate-work",
                    lambda doc: doc.update(
                        paper_work_id="2026.findings-acl.1724"
                    ),
                ),
                (
                    "duplicate-row",
                    lambda doc: doc["method_paths"][0].update(
                        method_path_id="2026.findings-acl.1724#pipeline"
                    ),
                ),
            ):
                with self.subTest(label=label):
                    target = sidecars / release.FINAL_SIDECAR_NAMES[0]
                    original = target.read_bytes()
                    doc = json.loads(original.decode("utf-8"))
                    mutate(doc)
                    target.write_text(
                        json.dumps(doc, ensure_ascii=False, indent=1) + "\n",
                        encoding="utf-8",
                        newline="\n",
                    )
                    with self.assertRaises(release.ReleaseContractError):
                        release.load_active_release(REPO, sidecars, adjudication)
                    target.write_bytes(original)

    def test_symlinked_active_sidecar_is_rejected(self):
        release = self.module()
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            sidecars, adjudication = self.copy_release(root)
            target = sidecars / release.FINAL_SIDECAR_NAMES[0]
            real = root / "real-sidecar.json"
            target.replace(real)
            try:
                target.symlink_to(real)
            except OSError as error:
                self.skipTest(f"symlink creation unavailable: {error}")
            with self.assertRaises(release.ReleaseContractError):
                release.load_active_release(REPO, sidecars, adjudication)

    def test_mocked_symlinked_active_sidecar_is_rejected_on_every_platform(self):
        release = self.module()
        target_name = release.FINAL_SIDECAR_NAMES[0]
        real_is_symlink = Path.is_symlink

        def injected(path):
            return path.name == target_name or real_is_symlink(path)

        with mock.patch.object(Path, "is_symlink", autospec=True, side_effect=injected):
            with self.assertRaises(release.ReleaseContractError):
                release.load_active_release(
                    REPO,
                    REPO / "wiki/survey/current/data/schema-v3/sidecars",
                    REPO / "wiki/survey/current/data/schema-v3-adjudication.json",
                )


class LineagePathTest(unittest.TestCase):
    def module(self):
        return importlib.import_module("sf_schema_v3_release_contract")

    def test_repo_relative_path_rejects_escape_absolute_drive_and_backslash(self):
        release = self.module()
        bad = (
            "",
            "../wiki/survey/ledger.jsonl",
            "/wiki/survey/ledger.jsonl",
            "D:/wiki/survey/ledger.jsonl",
            "wiki\\survey\\ledger.jsonl",
            "wiki/survey/./ledger.jsonl",
        )
        for value in bad:
            with self.subTest(value=value), self.assertRaises(
                release.ReleaseContractError
            ):
                release.validate_repo_relative_path(value, REPO)

    def test_canonical_record_requires_safe_path_and_nonempty_fragment(self):
        release = self.module()
        bad = (
            "wiki/survey/2026-07-18-sf-known-item-dfs-systemcontrol.md",
            "wiki/survey/2026-07-18-sf-known-item-dfs-systemcontrol.md#",
            "../outside.md#row",
            "/outside.md#row",
        )
        for value in bad:
            with self.subTest(value=value), self.assertRaises(
                release.ReleaseContractError
            ):
                release.validate_canonical_record_id(value, REPO)

    def test_symlink_component_is_rejected(self):
        release = self.module()
        with tempfile.TemporaryDirectory(dir=REPO) as temporary:
            root = Path(temporary)
            real = root / "real"
            real.mkdir()
            (real / "ledger.jsonl").write_text("{}\n", encoding="utf-8")
            link = root / "link"
            try:
                link.symlink_to(real, target_is_directory=True)
            except OSError as error:
                self.skipTest(f"symlink creation unavailable: {error}")
            relative = link.relative_to(REPO).as_posix() + "/ledger.jsonl"
            with self.assertRaises(release.ReleaseContractError):
                release.validate_repo_relative_path(
                    relative,
                    REPO,
                    allowed_root=root.relative_to(REPO),
                )

    def test_mocked_lineage_symlink_component_is_always_rejected(self):
        release = self.module()
        value = "wiki/survey/2026-07-17-sf-fulltext-ledger.jsonl"
        real_is_symlink = Path.is_symlink

        def injected(path):
            return path.name == "survey" or real_is_symlink(path)

        with mock.patch.object(Path, "is_symlink", autospec=True, side_effect=injected):
            with self.assertRaises(release.ReleaseContractError):
                release.validate_repo_relative_path(value, REPO)


class ProvenanceAndPublicationTest(unittest.TestCase):
    def test_report_contains_recomputable_exact_order_input_snapshot(self):
        report = harness.build_report()
        provenance = report["input_provenance"]
        self.assertIn("taxonomy", provenance)
        self.assertIn("coding", provenance)
        self.assertIn("adjudication", provenance)
        self.assertEqual(len(provenance["sidecars"]), 8)
        canonical = json.dumps(
            provenance,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        self.assertEqual(
            report["input_snapshot_sha256"], hashlib.sha256(canonical).hexdigest()
        )

    def test_any_valid_input_byte_change_changes_snapshot(self):
        baseline = harness.build_report()["input_snapshot_sha256"]
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "taxonomy.json"
            path.write_bytes(Path(harness.TAX).read_bytes() + b" \n")
            with mock.patch.object(harness, "TAX", str(path)):
                changed = harness.build_report()["input_snapshot_sha256"]
        self.assertNotEqual(changed, baseline)

        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "coding.json"
            path.write_bytes(Path(harness.CODING).read_bytes() + b" \n")
            with mock.patch.object(harness, "CODING", str(path)):
                changed_coding = harness.build_report()["input_snapshot_sha256"]
        self.assertNotEqual(changed_coding, baseline)

    def test_invalid_input_replaces_old_pass_with_explicit_fail(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "report.json"
            harness.write_report({"verdict": "PASS"}, output)
            with mock.patch.object(
                harness, "build_report", side_effect=ValueError("invalid input")
            ):
                self.assertNotEqual(harness.main(output=output), 0)
            report = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(report["verdict"], "FAIL")
            self.assertIn("invalid input", report["failure"]["message"])

    def test_actual_duplicate_taxonomy_input_replaces_old_pass(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            invalid = root / "taxonomy.json"
            invalid.write_bytes(b'{"artifact_id":"x","artifact_id":"y"}\n')
            output = root / "report.json"
            output.write_bytes(b'{"verdict":"PASS"}\n')
            with mock.patch.object(harness, "TAX", str(invalid)):
                self.assertNotEqual(harness.main(output=output), 0)
            report = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(report["verdict"], "FAIL")
            self.assertIn("duplicate", report["failure"]["message"])

    def test_publish_failure_preserves_old_report_and_leaves_no_debris(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "report.json"
            old = b'{"verdict":"PASS"}\n'
            output.write_bytes(old)
            with mock.patch.object(
                harness.os,
                "replace",
                side_effect=OSError("injected replace failure"),
            ):
                with self.assertRaisesRegex(OSError, "replace failure"):
                    harness.write_report({"verdict": "FAIL"}, output)
            self.assertEqual(output.read_bytes(), old)
            self.assertEqual(list(Path(temporary).iterdir()), [output])


class CacheIsolationTest(unittest.TestCase):
    def test_asset_cache_key_binds_path_sha_kind_extractor_and_stat(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "asset.pdf"
            path.write_bytes(b"first")
            one = harness._asset_cache_key(path, "a" * 64, "pdf", "extractor-v1")
            self.assertNotEqual(
                one,
                harness._asset_cache_key(path, "b" * 64, "pdf", "extractor-v1"),
            )
            self.assertNotEqual(
                one,
                harness._asset_cache_key(path, "a" * 64, "eprint", "extractor-v1"),
            )
            self.assertNotEqual(
                one,
                harness._asset_cache_key(path, "a" * 64, "pdf", "extractor-v2"),
            )
            path.write_bytes(b"second-longer")
            self.assertNotEqual(
                one,
                harness._asset_cache_key(path, "a" * 64, "pdf", "extractor-v1"),
            )

    def test_pdf_cache_isolated_between_runs_and_sha_changes(self):
        cache_one = harness.EvidenceCache()
        cache_two = harness.EvidenceCache()
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "asset.pdf"
            path.write_bytes(b"pdf")
            fake_reader = mock.Mock(pages=[])
            with (
                mock.patch.object(harness, "resolve_asset_path", return_value=str(path)),
                mock.patch.object(
                    harness, "_open_pdf_reader", return_value=fake_reader
                ) as opener,
            ):
                harness._cached_pdf_reader("stored", "a" * 64, "pdf", cache_one)
                harness._cached_pdf_reader("stored", "a" * 64, "pdf", cache_one)
                harness._cached_pdf_reader("stored", "b" * 64, "pdf", cache_one)
                harness._cached_pdf_reader("stored", "a" * 64, "pdf", cache_two)
            self.assertEqual(opener.call_count, 3)

    def test_tex_cache_isolated_between_runs_and_sha_changes(self):
        cache_one = harness.EvidenceCache()
        cache_two = harness.EvidenceCache()
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "asset.eprint"
            payload = b"A \\textbf{reward} signal"
            with tarfile.open(path, "w:gz") as archive:
                info = tarfile.TarInfo("paper.tex")
                info.size = len(payload)
                archive.addfile(info, io.BytesIO(payload))
            with mock.patch.object(
                harness, "resolve_asset_path", return_value=str(path)
            ):
                first = harness._cached_tex_text(
                    "stored", "a" * 64, "eprint", cache_one
                )
                again = harness._cached_tex_text(
                    "stored", "a" * 64, "eprint", cache_one
                )
                harness._cached_tex_text(
                    "stored", "b" * 64, "eprint", cache_one
                )
                harness._cached_tex_text(
                    "stored", "a" * 64, "eprint", cache_two
                )
            self.assertEqual(first, again)
            self.assertIn("reward signal", first)
            self.assertEqual(len(cache_one.tex), 2)
            self.assertEqual(len(cache_two.tex), 1)


if __name__ == "__main__":
    unittest.main()
