from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.survey import sf_stage1c_v2_calibration_r1 as run_r1
from scripts.survey.test_sf_stage1c_v2_precalibration_rc2r3 import (
    Stage1cV2PrecalibrationRc2r3Tests,
)


class Stage1cV2CalibrationR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        Stage1cV2PrecalibrationRc2r3Tests.setUpClass()
        cls.fixture = Stage1cV2PrecalibrationRc2r3Tests()
        cls.fixture.package = Stage1cV2PrecalibrationRc2r3Tests.package
        cls.package = cls.fixture.package

    def write_rows(self, path: Path, coder: str, transaction: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        rows = self.fixture.submitted_rows(coder, transaction)
        path.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def test_missing_second_output_keeps_agreement_closed(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            self.write_rows(root / "coder-a/output/responses.json", "CODER-A", "TX-A")
            status = run_r1.inspect_response_pair(
                self.package,
                root / "coder-a/output/responses.json",
                root / "coder-b/output/responses.json",
                expected_bindings={"A": ("CODER-A", "TX-A"), "B": ("CODER-B", "TX-B")},
            )
            self.assertEqual("RESPONSES_PENDING", status["status"])
            self.assertFalse(status["both_raw_outputs_valid"])
            with self.assertRaisesRegex(run_r1.CalibrationRunError, "both raw outputs"):
                run_r1.freeze_and_compute(
                    self.package, status, runtime_intake={}, delivery_receipts=[], destination=root / "frozen"
                )

    def test_exact_two_complete_outputs_validate_and_freeze_before_agreement(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            left = root / "coder-a/output/responses.json"
            right = root / "coder-b/output/responses.json"
            self.write_rows(left, "CODER-A", "TX-A")
            self.write_rows(right, "CODER-B", "TX-B")
            status = run_r1.inspect_response_pair(
                self.package, left, right,
                expected_bindings={"A": ("CODER-A", "TX-A"), "B": ("CODER-B", "TX-B")},
            )
            self.assertEqual("BOTH_RAW_OUTPUTS_VALID_NOT_FROZEN", status["status"])
            self.assertTrue(status["both_raw_outputs_valid"])
            intake, receipts = self.fixture.runtime()
            result = run_r1.freeze_and_compute(
                self.package, status, runtime_intake=intake,
                delivery_receipts=receipts, destination=root / "frozen",
            )
            self.assertEqual(56, result["agreement"]["paper_count"])
            self.assertTrue(result["both_raw_outputs_frozen"])
            self.assertTrue((root / "frozen/coder-a-responses.json").is_file())
            self.assertTrue((root / "frozen/coder-b-responses.json").is_file())

    def test_wrong_count_or_binding_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            path = root / "responses.json"
            rows = self.fixture.submitted_rows("CODER-A", "TX-A")
            path.write_text(json.dumps(rows[:-1]), encoding="utf-8")
            with self.assertRaisesRegex(run_r1.CalibrationRunError, "exact N=56"):
                run_r1.validate_response_file(
                    self.package, path, coder_id="CODER-A", transaction_id="TX-A"
                )
            rows[0]["coder_id"] = "OTHER"
            path.write_text(json.dumps(rows), encoding="utf-8")
            with self.assertRaisesRegex(run_r1.CalibrationRunError, "coder binding"):
                run_r1.validate_response_file(
                    self.package, path, coder_id="CODER-A", transaction_id="TX-A"
                )

    def test_invalid_json_order_and_duplicate_response_ids_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            path = Path(raw) / "responses.json"
            path.write_bytes(b"not-json")
            with self.assertRaisesRegex(run_r1.CalibrationRunError, "not UTF-8 JSON"):
                run_r1.validate_response_file(
                    self.package, path, coder_id="CODER-A", transaction_id="TX-A"
                )
            rows = self.fixture.submitted_rows("CODER-A", "TX-A")
            rows[0], rows[1] = rows[1], rows[0]
            path.write_text(json.dumps(rows), encoding="utf-8")
            with self.assertRaisesRegex(run_r1.CalibrationRunError, "paper order/identity"):
                run_r1.validate_response_file(
                    self.package, path, coder_id="CODER-A", transaction_id="TX-A"
                )
            rows[0], rows[1] = rows[1], rows[0]
            rows[1]["response_id"] = rows[0]["response_id"]
            path.write_text(json.dumps(rows), encoding="utf-8")
            with self.assertRaisesRegex(run_r1.CalibrationRunError, "duplicate response_id"):
                run_r1.validate_response_file(
                    self.package, path, coder_id="CODER-A", transaction_id="TX-A"
                )

    def test_pair_binding_and_existing_freeze_destination_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            left = root / "coder-a/output/responses.json"
            right = root / "coder-b/output/responses.json"
            self.write_rows(left, "CODER-A", "TX-A")
            self.write_rows(right, "CODER-B", "TX-B")
            with self.assertRaisesRegex(run_r1.CalibrationRunError, "exact A/B"):
                run_r1.inspect_response_pair(
                    self.package, left, right, expected_bindings={"A": ("CODER-A", "TX-A")}
                )
            status = run_r1.inspect_response_pair(
                self.package, left, right,
                expected_bindings={"A": ("CODER-A", "TX-A"), "B": ("CODER-B", "TX-B")},
            )
            destination = root / "already-exists"
            destination.mkdir()
            intake, receipts = self.fixture.runtime()
            with self.assertRaisesRegex(run_r1.CalibrationRunError, "already exists"):
                run_r1.freeze_and_compute(
                    self.package, status, runtime_intake=intake,
                    delivery_receipts=receipts, destination=destination,
                )


if __name__ == "__main__":
    unittest.main()
