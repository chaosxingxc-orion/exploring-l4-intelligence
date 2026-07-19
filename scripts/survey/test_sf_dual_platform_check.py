#!/usr/bin/env python3
"""Adversarial tests for the dual-platform evidence-v6 aggregator."""
from __future__ import annotations

import contextlib
import hashlib
import io
import json
import tempfile
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent

import sys

sys.path.insert(0, str(HERE))

import sf_dual_platform_check as dual  # noqa: E402
from sf_json_contract import canonical_bytes  # noqa: E402


class DualPlatformCheckTest(unittest.TestCase):
    def report(self, platform):
        provenance = {
            "taxonomy_v5": {"path": "taxonomy-v5.json", "sha256": "1" * 64},
            "taxonomy": {"path": "taxonomy-v6.json", "sha256": "2" * 64},
            "coding": {"path": "coding-v7.json", "sha256": "3" * 64},
            "adjudication": {"path": "adjudication.json", "sha256": "4" * 64},
            "sidecars": [
                {
                    "path": f"sidecar-{index}.json",
                    "sha256": f"{index + 5:x}" * 64,
                }
                for index in range(8)
            ],
        }
        return {
            "platform": {"os": platform, "python": "3.14.3"},
            "verdict": "PASS",
            "occupancy": {"policy_A": {"n_method_paths": 11}},
            "input_provenance": provenance,
            "input_snapshot_sha256": hashlib.sha256(
                canonical_bytes(provenance)
            ).hexdigest(),
        }

    def write_pair(self, base, nt=None, posix=None):
        for platform, report in (
            ("nt", nt or self.report("nt")),
            ("posix", posix or self.report("posix")),
        ):
            Path(f"{base}.{platform}.json").write_text(
                json.dumps(report, ensure_ascii=False) + "\n",
                encoding="utf-8",
                newline="\n",
            )

    def run_main(self, base):
        stream = io.StringIO()
        with contextlib.redirect_stdout(stream):
            result = dual.main(["--base", str(base)])
        return result, stream.getvalue()

    def test_matching_v6_snapshots_pass_with_required_confirmations(self):
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary) / "identity-taxonomy-v6-test"
            self.write_pair(base)
            result, output = self.run_main(base)
        self.assertEqual(result, 0, output)
        self.assertIn("input snapshot equality: CONFIRMED", output)
        self.assertIn("occupancy equality: CONFIRMED", output)
        self.assertIn("dual-platform check: PASS (0 failures)", output)

    def test_platform_suffix_must_match_report_platform(self):
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary) / "identity-taxonomy-v6-test"
            spoofed = self.report("posix")
            self.write_pair(base, nt=spoofed)
            result, output = self.run_main(base)
        self.assertNotEqual(result, 0)
        self.assertIn("nt: platform.os posix does not match suffix nt", output)

    def test_mutations_fail_closed(self):
        def verdict(report):
            report["verdict"] = "FAIL"

        def occupancy(report):
            report["occupancy"]["policy_A"]["n_method_paths"] = 12

        def snapshot(report):
            report["input_snapshot_sha256"] = "0" * 64

        def provenance(report):
            report["input_provenance"]["taxonomy"]["sha256"] = "f" * 64
            report["input_snapshot_sha256"] = hashlib.sha256(
                canonical_bytes(report["input_provenance"])
            ).hexdigest()

        for label, mutate in (
            ("verdict", verdict),
            ("occupancy", occupancy),
            ("snapshot", snapshot),
            ("provenance", provenance),
        ):
            with (
                self.subTest(label=label),
                tempfile.TemporaryDirectory() as temporary,
            ):
                base = Path(temporary) / "identity-taxonomy-v6-test"
                posix = self.report("posix")
                mutate(posix)
                self.write_pair(base, posix=posix)
                result, output = self.run_main(base)
                self.assertNotEqual(result, 0, output)
                self.assertIn("dual-platform check: FAIL", output)

    def test_missing_snapshot_is_a_controlled_failure(self):
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary) / "identity-taxonomy-v6-test"
            Path(f"{base}.nt.json").write_text(
                json.dumps(self.report("nt")) + "\n", encoding="utf-8"
            )
            result, output = self.run_main(base)
            self.assertNotEqual(result, 0)
            self.assertIn("missing platform snapshot", output)

    def test_non_strict_snapshot_is_a_controlled_failure(self):
        for malformed in (
            b'{"verdict":"PASS","verdict":"PASS"}\n',
            b'{"x": NaN}\n',
            b'{} trailing\n',
            b'{"x":"\xff"}\n',
        ):
            with (
                self.subTest(malformed=malformed),
                tempfile.TemporaryDirectory() as temporary,
            ):
                base = Path(temporary) / "identity-taxonomy-v6-test"
                self.write_pair(base)
                Path(f"{base}.posix.json").write_bytes(malformed)
                result, output = self.run_main(base)
                self.assertNotEqual(result, 0)
                self.assertIn("strict snapshot load failed", output)

    def test_exact_historical_v5_base_has_explicit_legacy_compatibility(self):
        base = dual.LEGACY_BASE
        result, output = self.run_main(base)
        self.assertEqual(result, 0, output)
        self.assertIn("legacy provenance compatibility: ENABLED", output)
        self.assertIn("occupancy equality: CONFIRMED", output)


if __name__ == "__main__":
    unittest.main()
