#!/usr/bin/env python3
"""Adversarial tests binding the v6 proof to exact active input bytes."""
from __future__ import annotations

import copy
import hashlib
import importlib
import io
import json
import os
import shutil
import stat
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
        baseline = harness._load_input_snapshot()
        for mutated in mutations:
            snapshot = dict(baseline, taxonomy_v6=mutated)
            empty_contract = {"structure": [], "bindings": [], "source": []}
            with (
                mock.patch.object(
                    harness, "_load_input_snapshot", return_value=snapshot
                ),
                mock.patch.object(
                    harness,
                    "validate_load_bearing_contract",
                    return_value=empty_contract,
                ),
                mock.patch.object(
                    harness,
                    "run_mutation_suite",
                    return_value=(empty_contract, {}, True),
                ),
            ):
                self.assertEqual(harness.build_report()["verdict"], "FAIL")


class ReleaseInventoryTest(unittest.TestCase):
    def module(self):
        return importlib.import_module("sf_schema_v3_release_contract")

    def materialize_trusted_repo(self, root):
        """Copy the exact release plus every repo-relative lineage dependency."""
        release = self.module()
        sidecars = (
            root
            / "wiki/survey/current/data/schema-v3/sidecars"
        )
        sidecars.parent.mkdir(parents=True)
        shutil.copytree(
            REPO / "wiki/survey/current/data/schema-v3/sidecars",
            sidecars,
        )
        adjudication = root / release.ADJUDICATION_RELATIVE_PATH
        shutil.copy2(
            REPO / release.ADJUDICATION_RELATIVE_PATH,
            adjudication,
        )
        for path in sidecars.iterdir():
            document = json.loads(path.read_text(encoding="utf-8"))
            relative_paths = {
                document["fulltext"]["ledger"],
                document["canonical_record_id"].partition("#")[0],
            }
            for relative in relative_paths:
                destination = root / relative
                destination.parent.mkdir(parents=True, exist_ok=True)
                if not destination.exists():
                    shutil.copy2(REPO / relative, destination)
        return sidecars, adjudication

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
            sidecars, adjudication = self.materialize_trusted_repo(root)
            ninth = sidecars / "ninth.sidecar.json"
            ninth.write_bytes((sidecars / release.FINAL_SIDECAR_NAMES[0]).read_bytes())
            with self.assertRaises(release.ReleaseContractError):
                release.load_active_release(root, sidecars, adjudication)
            ninth.unlink()

            missing = sidecars / release.FINAL_SIDECAR_NAMES[0]
            saved = missing.read_bytes()
            missing.unlink()
            with self.assertRaises(release.ReleaseContractError):
                release.load_active_release(root, sidecars, adjudication)
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
                        release.load_active_release(root, sidecars, adjudication)
                    target.write_bytes(original)

    def test_symlinked_active_sidecar_is_rejected(self):
        release = self.module()
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            sidecars, adjudication = self.materialize_trusted_repo(root)
            target = sidecars / release.FINAL_SIDECAR_NAMES[0]
            real = root / "real-sidecar.json"
            target.replace(real)
            try:
                target.symlink_to(real)
            except OSError as error:
                self.skipTest(f"symlink creation unavailable: {error}")
            with self.assertRaises(release.ReleaseContractError):
                release.load_active_release(root, sidecars, adjudication)

    def test_mocked_symlinked_active_sidecar_is_rejected_on_every_platform(self):
        release = self.module()
        target_name = release.FINAL_SIDECAR_NAMES[0]
        real_lstat = Path.lstat

        def injected(path):
            result = real_lstat(path)
            if path.name == target_name:
                fields = list(result)
                fields[0] = stat.S_IFLNK | 0o777
                return os.stat_result(fields)
            return result

        with mock.patch.object(Path, "lstat", autospec=True, side_effect=injected):
            with self.assertRaises(release.ReleaseContractError):
                release.load_active_release(
                    REPO,
                    REPO / "wiki/survey/current/data/schema-v3/sidecars",
                    REPO / "wiki/survey/current/data/schema-v3-adjudication.json",
                )

    def test_mocked_ancestor_symlink_is_rejected_before_active_release_read(self):
        release = self.module()
        real_lstat = Path.lstat

        def injected(path):
            result = real_lstat(path)
            if path.name == "current":
                fields = list(result)
                fields[0] = stat.S_IFLNK | 0o777
                return os.stat_result(fields)
            return result

        with mock.patch.object(
            Path, "lstat", autospec=True, side_effect=injected
        ):
            with self.assertRaises(release.ReleaseContractError):
                release.load_active_release(
                    REPO,
                    REPO / "wiki/survey/current/data/schema-v3/sidecars",
                    REPO / "wiki/survey/current/data/schema-v3-adjudication.json",
                )

    def test_real_ancestor_symlink_to_exact_release_is_rejected(self):
        release = self.module()
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            sidecars, adjudication = self.materialize_trusted_repo(root)
            current = root / "wiki/survey/current"
            real_current = root / "wiki/survey/real-current"
            current.replace(real_current)
            try:
                current.symlink_to(real_current, target_is_directory=True)
            except OSError as error:
                self.skipTest(f"symlink creation unavailable: {error}")
            with self.assertRaises(release.ReleaseContractError):
                release.load_active_release(root, sidecars, adjudication)


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
        real_lstat = Path.lstat

        def injected(path):
            result = real_lstat(path)
            if path.name == "survey":
                fields = list(result)
                fields[0] = stat.S_IFLNK | 0o777
                return os.stat_result(fields)
            return result

        with mock.patch.object(Path, "lstat", autospec=True, side_effect=injected):
            with self.assertRaises(release.ReleaseContractError):
                release.validate_repo_relative_path(value, REPO)


class ProvenanceAndPublicationTest(unittest.TestCase):
    def passing_report(self, platform=None):
        policy = {
            "is_reward_guided": {"n_paths": "6/11"},
            "is_rq_sys_control_compatible": {"n_paths": "5/11"},
            "is_project_method_candidate": {"n_paths": "0/11"},
            "reward_guided_selection": {"n_paths": "4/11"},
            "strict_AND_reward_AND_pool_BY_selection_object(mechanism)": {
                "trajectory": {"n_paths": "2/11"},
            },
        }
        return {
            "summary": "1/1 PASS",
            "verdict": "PASS",
            "platform": {
                "os": platform or os.name,
                "python": sys.version.split()[0],
            },
            "occupancy": {"policy_A": policy},
        }

    def test_snapshot_json_reader_rejects_exact_bytes_at_unprescribed_path(self):
        with tempfile.TemporaryDirectory() as temporary:
            redirected = Path(temporary) / "identity-taxonomy-v6.json"
            redirected.write_bytes(Path(harness.TAX).read_bytes())
            with self.assertRaisesRegex(ValueError, "prescribed repo-relative path"):
                harness._read_snapshot_json(
                    redirected,
                    harness.TAX_RELATIVE_PATH,
                )

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

    def test_harness_and_shared_contract_load_the_same_current_raw_snapshot(self):
        shared = importlib.import_module("sf_v6_snapshot_contract")
        harness_snapshot = harness._load_input_snapshot()
        shared_snapshot = shared.load_v6_input_snapshot(REPO)
        self.assertEqual(
            harness_snapshot["input_provenance"],
            shared_snapshot["input_provenance"],
        )
        self.assertEqual(
            harness_snapshot["input_snapshot_sha256"],
            shared_snapshot["input_snapshot_sha256"],
        )
        self.assertEqual(
            shared_snapshot["input_snapshot_sha256"],
            shared.CURRENT_INPUT_SNAPSHOT_SHA256,
        )
        enforced = shared.load_v6_input_snapshot(
            REPO,
            expected_snapshot_sha256=shared.CURRENT_INPUT_SNAPSHOT_SHA256,
        )
        self.assertEqual(
            enforced["input_provenance"],
            shared_snapshot["input_provenance"],
        )

        def changed_reader(path, expected_relative):
            document, raw = shared.read_snapshot_json(
                REPO, path, expected_relative
            )
            if expected_relative == shared.TAXONOMY_V6_RELATIVE_PATH:
                raw += b" \n"
            return document, raw

        with self.assertRaisesRegex(ValueError, "input snapshot SHA-256 mismatch"):
            shared.load_v6_input_snapshot(
                REPO,
                read_snapshot=changed_reader,
                expected_snapshot_sha256=shared.CURRENT_INPUT_SNAPSHOT_SHA256,
            )

    def test_any_valid_input_byte_change_changes_snapshot(self):
        baseline = harness._load_input_snapshot()["input_snapshot_sha256"]
        real_reader = harness._read_snapshot_json

        def changed_taxonomy(path, expected_relative):
            document, raw = real_reader(path, expected_relative)
            if expected_relative == harness.TAX_RELATIVE_PATH:
                raw += b" \n"
            return document, raw

        with mock.patch.object(
            harness, "_read_snapshot_json", side_effect=changed_taxonomy
        ):
            changed = harness._load_input_snapshot()["input_snapshot_sha256"]
        self.assertNotEqual(changed, baseline)

        def changed_coding(path, expected_relative):
            document, raw = real_reader(path, expected_relative)
            if expected_relative == harness.CODING_RELATIVE_PATH:
                raw += b" \n"
            return document, raw

        with mock.patch.object(
            harness, "_read_snapshot_json", side_effect=changed_coding
        ):
            changed_coding = harness._load_input_snapshot()[
                "input_snapshot_sha256"
            ]
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
            output = root / "report.json"
            output.write_bytes(b'{"verdict":"PASS"}\n')
            contract = importlib.import_module("sf_json_contract")
            real_reader = harness._read_snapshot_json

            def duplicate_taxonomy(path, expected_relative):
                if expected_relative == harness.TAX_RELATIVE_PATH:
                    return contract.loads(
                        b'{"artifact_id":"x","artifact_id":"y"}\n',
                        "active taxonomy fixture",
                    )
                return real_reader(path, expected_relative)

            with mock.patch.object(
                harness,
                "_read_snapshot_json",
                side_effect=duplicate_taxonomy,
            ):
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

    def test_main_writes_platform_stamp_identical_to_base_for_custom_output(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "custom.json"
            with mock.patch.object(
                harness, "build_report", return_value=self.passing_report()
            ):
                self.assertEqual(harness.main(output=output), 0)
            stamp = output.with_name(f"custom.{os.name}.json")
            self.assertEqual(stamp.read_bytes(), output.read_bytes())
            self.assertEqual(
                json.loads(stamp.read_text(encoding="utf-8"))["platform"]["os"],
                os.name,
            )

    def test_main_failure_replaces_platform_stamp_with_fail(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "custom.json"
            stamp = output.with_name(f"custom.{os.name}.json")
            stamp.write_bytes(b'{"verdict":"PASS"}\n')
            with mock.patch.object(
                harness, "build_report", side_effect=ValueError("invalid input")
            ):
                self.assertNotEqual(harness.main(output=output), 0)
            self.assertEqual(output.read_bytes(), stamp.read_bytes())
            self.assertEqual(
                json.loads(stamp.read_text(encoding="utf-8"))["verdict"], "FAIL"
            )

    def test_mid_publication_failure_removes_old_stamp_fail_closed(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "custom.json"
            stamp = output.with_name(f"custom.{os.name}.json")
            output.write_bytes(b'{"verdict":"PASS"}\n')
            stamp.write_bytes(b'{"verdict":"PASS"}\n')
            real_write = harness.write_report

            def fail_stamp(report, destination):
                if Path(destination) == stamp:
                    raise OSError("injected stamp failure")
                return real_write(report, destination)

            with (
                mock.patch.object(
                    harness,
                    "build_report",
                    return_value=self.passing_report(),
                ),
                mock.patch.object(harness, "write_report", side_effect=fail_stamp),
                self.assertRaisesRegex(OSError, "stamp failure"),
            ):
                harness.main(output=output)
            self.assertFalse(stamp.exists())
            self.assertEqual(
                json.loads(output.read_text(encoding="utf-8"))["verdict"], "PASS"
            )


class CacheIsolationTest(unittest.TestCase):
    def test_asset_cache_key_binds_path_actual_sha_kind_and_extractor(self):
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
                harness._asset_cache_key(path, "c" * 64, "pdf", "extractor-v1"),
            )

    def test_pdf_cache_isolated_between_runs_and_sha_changes(self):
        cache_one = harness.EvidenceCache()
        cache_two = harness.EvidenceCache()
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "asset.pdf"
            path.write_bytes(b"pdf")
            sha_one = hashlib.sha256(path.read_bytes()).hexdigest()
            fake_reader = mock.Mock(pages=[])
            with (
                mock.patch.object(harness, "resolve_asset_path", return_value=str(path)),
                mock.patch.object(
                    harness, "_open_pdf_reader", return_value=fake_reader
                ) as opener,
            ):
                harness._cached_pdf_reader("stored", sha_one, "pdf", cache_one)
                harness._cached_pdf_reader("stored", sha_one, "pdf", cache_one)
                path.write_bytes(b"pd2")
                sha_two = hashlib.sha256(path.read_bytes()).hexdigest()
                harness._cached_pdf_reader("stored", sha_two, "pdf", cache_one)
                harness._cached_pdf_reader("stored", sha_two, "pdf", cache_two)
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
            sha_one = hashlib.sha256(path.read_bytes()).hexdigest()
            with mock.patch.object(
                harness, "resolve_asset_path", return_value=str(path)
            ):
                first = harness._cached_tex_text(
                    "stored", sha_one, "eprint", cache_one
                )
                again = harness._cached_tex_text(
                    "stored", sha_one, "eprint", cache_one
                )
                payload_two = b"A \\textbf{critique} signal"
                with tarfile.open(path, "w:gz") as archive:
                    info = tarfile.TarInfo("paper.tex")
                    info.size = len(payload_two)
                    archive.addfile(info, io.BytesIO(payload_two))
                sha_two = hashlib.sha256(path.read_bytes()).hexdigest()
                harness._cached_tex_text(
                    "stored", sha_two, "eprint", cache_one
                )
                harness._cached_tex_text(
                    "stored", sha_two, "eprint", cache_two
                )
            self.assertEqual(first, again)
            self.assertIn("reward signal", first)
            self.assertEqual(len(cache_one.tex), 2)
            self.assertEqual(len(cache_two.tex), 1)

    def test_pdf_same_metadata_byte_swap_cannot_hit_old_parse(self):
        cache = harness.EvidenceCache()
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "asset.pdf"
            original = b"pdf-one-contents"
            path.write_bytes(original)
            expected_sha256 = hashlib.sha256(original).hexdigest()
            before = path.stat()
            fake_reader = mock.Mock(pages=[])

            def open_same_bytes(source):
                self.assertIsInstance(source, io.BytesIO)
                self.assertEqual(source.getvalue(), original)
                return fake_reader

            with (
                mock.patch.object(
                    harness, "resolve_asset_path", return_value=str(path)
                ),
                mock.patch.object(
                    harness, "_open_pdf_reader", side_effect=open_same_bytes
                ) as opener,
            ):
                harness._cached_pdf_reader(
                    "stored", expected_sha256, "pdf", cache
                )
                mutated = b"pdf-two-contents"
                self.assertEqual(len(mutated), len(original))
                path.write_bytes(mutated)
                os.utime(
                    path,
                    ns=(before.st_atime_ns, before.st_mtime_ns),
                )
                self.assertEqual(path.stat().st_ino, before.st_ino)
                with self.assertRaisesRegex(ValueError, "sha256|SHA-256"):
                    harness._cached_pdf_reader(
                        "stored", expected_sha256, "pdf", cache
                    )
            self.assertEqual(opener.call_count, 1)

    def test_tex_same_metadata_byte_swap_cannot_hit_old_parse(self):
        cache = harness.EvidenceCache()
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "asset.eprint"
            payload = b"A \\textbf{reward} signal"
            with tarfile.open(path, "w:gz") as archive:
                info = tarfile.TarInfo("paper.tex")
                info.size = len(payload)
                archive.addfile(info, io.BytesIO(payload))
            original = path.read_bytes()
            expected_sha256 = hashlib.sha256(original).hexdigest()
            before = path.stat()
            real_tar_open = tarfile.open

            def open_same_bytes(*args, **kwargs):
                source = kwargs.get("fileobj")
                self.assertIsInstance(source, io.BytesIO)
                self.assertEqual(source.getvalue(), original)
                return real_tar_open(*args, **kwargs)

            with (
                mock.patch.object(
                    harness, "resolve_asset_path", return_value=str(path)
                ),
                mock.patch.object(
                    harness.tarfile, "open", side_effect=open_same_bytes
                ),
            ):
                self.assertIn(
                    "reward signal",
                    harness._cached_tex_text(
                        "stored", expected_sha256, "eprint", cache
                    ),
                )
                mutated = bytearray(original)
                mutated[-1] ^= 1
                path.write_bytes(mutated)
                os.utime(
                    path,
                    ns=(before.st_atime_ns, before.st_mtime_ns),
                )
                self.assertEqual(path.stat().st_ino, before.st_ino)
                with self.assertRaisesRegex(ValueError, "sha256|SHA-256"):
                    harness._cached_tex_text(
                        "stored", expected_sha256, "eprint", cache
                    )


if __name__ == "__main__":
    unittest.main()
