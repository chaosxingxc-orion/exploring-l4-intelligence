#!/usr/bin/env python3
"""Adversarial tests for the dual-platform evidence-v6 aggregator."""
from __future__ import annotations

import contextlib
import copy
import hashlib
import io
import json
import os
import stat
import tempfile
import unittest
from pathlib import Path
from unittest import mock


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]

import sys

sys.path.insert(0, str(HERE))

import sf_dual_platform_check as dual  # noqa: E402
from sf_json_contract import canonical_bytes  # noqa: E402


REPORT_BASE = (
    REPO
    / "docs/checks/system-first-stage1a/evidence-v6/identity-taxonomy-v6-test"
)


class DualPlatformCheckTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.nt_report = json.loads(
            Path(f"{REPORT_BASE}.nt.json").read_text(encoding="utf-8")
        )

    def report(self, platform):
        report = copy.deepcopy(self.nt_report)
        report["platform"] = {
            "os": platform,
            "python": "3.14.3" if platform == "nt" else "3.12.3",
        }
        return report

    def repo_temporary(self):
        return tempfile.TemporaryDirectory(prefix="a10-dual-", dir=REPO)

    def write_pair(self, base, nt=None, posix=None):
        for platform, report in (
            ("nt", nt if nt is not None else self.report("nt")),
            ("posix", posix if posix is not None else self.report("posix")),
        ):
            Path(f"{base}.{platform}.json").write_text(
                json.dumps(report, ensure_ascii=False) + "\n",
                encoding="utf-8",
                newline="\n",
            )

    def run_main(self, base=None, *, legacy=False):
        argv = []
        if base is not None:
            argv.extend(("--base", str(base)))
        if legacy:
            argv.append("--legacy-regression")
        stream = io.StringIO()
        with contextlib.redirect_stdout(stream):
            result = dual.main(argv)
        return result, stream.getvalue()

    def test_matching_v6_snapshots_pass_with_required_confirmations(self):
        result, output = self.run_main()
        self.assertEqual(result, 0, output)
        self.assertIn("current release binding: CONFIRMED", output)
        self.assertIn("frozen report semantics: CONFIRMED", output)
        self.assertIn("input snapshot equality: CONFIRMED", output)
        self.assertIn("occupancy equality: CONFIRMED", output)
        self.assertIn("dual-platform check: PASS (0 failures)", output)

    def test_platform_suffix_must_match_report_platform(self):
        with self.repo_temporary() as temporary:
            base = Path(temporary) / "identity-taxonomy-v6-test"
            spoofed = self.report("posix")
            self.write_pair(base, nt=spoofed)
            result, output = self.run_main(base)
        self.assertNotEqual(result, 0)
        self.assertIn("nt: platform.os posix does not match suffix nt", output)

    def test_both_reports_cannot_self_attest_the_same_forged_provenance(self):
        with self.repo_temporary() as temporary:
            base = Path(temporary) / "identity-taxonomy-v6-test"
            reports = []
            for platform in ("nt", "posix"):
                report = self.report(platform)
                report["input_provenance"]["taxonomy"]["sha256"] = "f" * 64
                report["input_snapshot_sha256"] = hashlib.sha256(
                    canonical_bytes(report["input_provenance"])
                ).hexdigest()
                reports.append(report)
            self.write_pair(base, nt=reports[0], posix=reports[1])
            result, output = self.run_main(base)
        self.assertNotEqual(result, 0, output)
        self.assertIn("current release", output)

    def test_both_reports_cannot_share_the_same_forged_occupancy(self):
        with self.repo_temporary() as temporary:
            base = Path(temporary) / "identity-taxonomy-v6-test"
            nt = self.report("nt")
            posix = self.report("posix")
            for report in (nt, posix):
                report["occupancy"]["policy_A"]["n_method_paths"] = 12
            self.write_pair(base, nt=nt, posix=posix)
            result, output = self.run_main(base)
        self.assertNotEqual(result, 0, output)
        self.assertIn("frozen", output)

    def test_frozen_report_shape_and_internal_results_fail_closed(self):
        def delete_checks(report):
            del report["checks"]

        def delete_mutations(report):
            del report["mutation_results"]

        def delete_summary(report):
            del report["summary"]

        def delete_artifact(report):
            del report["artifact_id"]

        def internal_fail(report):
            report["checks"][0]["result"] = "FAIL"

        for label, mutate in (
            ("checks", delete_checks),
            ("mutations", delete_mutations),
            ("summary", delete_summary),
            ("artifact", delete_artifact),
            ("internal-fail", internal_fail),
        ):
            with self.subTest(label=label), self.repo_temporary() as temporary:
                base = Path(temporary) / "identity-taxonomy-v6-test"
                nt = self.report("nt")
                posix = self.report("posix")
                mutate(nt)
                mutate(posix)
                self.write_pair(base, nt=nt, posix=posix)
                result, output = self.run_main(base)
                self.assertNotEqual(result, 0, output)
                self.assertIn("dual-platform check: FAIL", output)

    def test_verdict_snapshot_and_cross_platform_mutations_fail_closed(self):
        def verdict(report):
            report["verdict"] = "FAIL"

        def snapshot(report):
            report["input_snapshot_sha256"] = "0" * 64

        def provenance(report):
            report["input_provenance"]["taxonomy"]["sha256"] = "f" * 64
            report["input_snapshot_sha256"] = hashlib.sha256(
                canonical_bytes(report["input_provenance"])
            ).hexdigest()

        for label, mutate in (
            ("verdict", verdict),
            ("snapshot", snapshot),
            ("provenance", provenance),
        ):
            with self.subTest(label=label), self.repo_temporary() as temporary:
                base = Path(temporary) / "identity-taxonomy-v6-test"
                posix = self.report("posix")
                mutate(posix)
                self.write_pair(base, posix=posix)
                result, output = self.run_main(base)
                self.assertNotEqual(result, 0, output)
                self.assertIn("dual-platform check: FAIL", output)

    def test_missing_and_non_strict_snapshots_are_controlled_failures(self):
        malformed_inputs = (
            None,
            b'{"verdict":"PASS","verdict":"PASS"}\n',
            b'{"x": NaN}\n',
            b'{} trailing\n',
            b'{"x":"\xff"}\n',
        )
        for malformed in malformed_inputs:
            with self.subTest(malformed=malformed), self.repo_temporary() as temporary:
                base = Path(temporary) / "identity-taxonomy-v6-test"
                self.write_pair(base)
                posix = Path(f"{base}.posix.json")
                if malformed is None:
                    posix.unlink()
                else:
                    posix.write_bytes(malformed)
                result, output = self.run_main(base)
                self.assertNotEqual(result, 0)
                self.assertIn("dual-platform check: FAIL", output)

    def test_platform_report_leaf_and_ancestor_symlinks_are_rejected(self):
        with self.repo_temporary() as temporary:
            root = Path(temporary)
            real = root / "real"
            real.mkdir()
            base = real / "identity-taxonomy-v6-test"
            self.write_pair(base)

            leaf = root / "leaf-test"
            Path(f"{leaf}.posix.json").write_bytes(
                Path(f"{base}.posix.json").read_bytes()
            )
            try:
                Path(f"{leaf}.nt.json").symlink_to(Path(f"{base}.nt.json"))
            except OSError as error:
                self.skipTest(f"symlink creation unavailable: {error}")
            result, output = self.run_main(leaf)
            self.assertNotEqual(result, 0, output)
            self.assertIn("symlink", output)

            alias = root / "alias"
            alias.symlink_to(real, target_is_directory=True)
            result, output = self.run_main(alias / base.name)
            self.assertNotEqual(result, 0, output)
            self.assertIn("symlink", output)

    def test_mocked_leaf_and_ancestor_symlinks_are_rejected_on_all_platforms(self):
        with self.repo_temporary() as temporary:
            root = Path(temporary)
            base = root / "identity-taxonomy-v6-test"
            self.write_pair(base)
            real_lstat = Path.lstat
            targets = (
                f"{base.name}.nt.json",
                root.name,
            )
            for target_name in targets:
                def injected(path, target_name=target_name):
                    result = real_lstat(path)
                    if path.name == target_name:
                        fields = list(result)
                        fields[0] = stat.S_IFLNK | 0o777
                        return os.stat_result(fields)
                    return result

                with (
                    self.subTest(target_name=target_name),
                    mock.patch.object(
                        Path, "lstat", autospec=True, side_effect=injected
                    ),
                ):
                    result, output = self.run_main(base)
                    self.assertNotEqual(result, 0, output)
                    self.assertIn("symlink", output)

    def test_legacy_requires_flag_and_exact_declared_path_literal(self):
        relative = "docs/checks/2026-07-19-sf-identity-taxonomy-v5-test"
        for denied in (relative, str(dual.LEGACY_BASE)):
            with self.subTest(no_flag=denied):
                result, output = self.run_main(denied)
                self.assertNotEqual(result, 0, output)
                self.assertNotIn(
                    "legacy provenance compatibility: ENABLED", output
                )

        for accepted in (relative, str(dual.LEGACY_BASE)):
            with self.subTest(accepted=accepted):
                result, output = self.run_main(accepted, legacy=True)
                self.assertEqual(result, 0, output)
                self.assertIn("legacy provenance compatibility: ENABLED", output)

        result, output = self.run_main(legacy=True)
        self.assertNotEqual(result, 0, output)
        self.assertIn("legacy", output.lower())

    def test_legacy_rejects_traversal_case_backslash_and_symlink_aliases(self):
        relative = "docs/checks/2026-07-19-sf-identity-taxonomy-v5-test"
        aliases = (
            "docs/checks/../checks/2026-07-19-sf-identity-taxonomy-v5-test",
            relative.replace("/", "\\"),
            relative.replace("checks", "CHECKS"),
            str(dual.LEGACY_BASE.parent / "." / dual.LEGACY_BASE.name) + os.sep,
        )
        for value in aliases:
            with self.subTest(value=value):
                result, output = self.run_main(value, legacy=True)
                self.assertNotEqual(result, 0, output)
                self.assertIn("legacy", output.lower())

        with self.repo_temporary() as temporary:
            alias = Path(temporary) / "legacy-alias"
            try:
                alias.symlink_to(dual.LEGACY_BASE.parent, target_is_directory=True)
            except OSError as error:
                return
            result, output = self.run_main(
                alias / dual.LEGACY_BASE.name, legacy=True
            )
            self.assertNotEqual(result, 0, output)
            self.assertIn("legacy", output.lower())


if __name__ == "__main__":
    unittest.main()
